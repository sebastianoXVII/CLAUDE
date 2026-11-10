"""Esegue T14 (research/preregistration/T14_ricerca_sistematica.md) uno stadio alla volta:
    python3 research/run_t14.py scoperta | convalida | holdout
Ogni stadio calcola solo il proprio periodo, rifiuta di ripetersi e richiede lo stadio precedente."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import t14_engine as E  # noqa: E402
import t1_engine as T1  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BARS, OUT = ROOT / "data" / "bars", ROOT / "research" / "results"
INSTR = {"NQ": ("NSXUSD", "index", 0.45, 20.0), "ES": ("SPXUSD", "index", 0.5, 50.0),
         "EURUSD": ("EURUSD", "fx", 0.00010, 100_000.0), "GBPUSD": ("GBPUSD", "fx", 0.00013, 100_000.0),
         "XAUUSD": ("XAUUSD", "fx", 0.35, 100.0)}
PERIODS = {"scoperta": (None, "2017-12-31"), "convalida": ("2018-01-01", "2021-12-31"), "holdout": ("2022-01-01", "2024-12-31")}
FILES = {k: f"T14_{k}.json" for k in PERIODS}
PREV = {"convalida": "scoperta", "holdout": "convalida"}
TOP_K = 10
NYSE = frozenset(pd.Timestamp(d).tz_localize(None).normalize() for d in T1._XNYS.sessions)


def valid_days(bars_et: pd.DataFrame, kind: str) -> pd.DatetimeIndex:
    if kind == "index":
        w = bars_et.between_time("09:30", "15:59")
        n = w.groupby(pd.to_datetime(w.index.date)).size()
        ok = [d for d, c in n.items() if d in NYSE and d not in T1.EARLY_CLOSES and c >= 300]
    else:
        w = bars_et.between_time("00:00", "15:59")
        n = w.groupby(pd.to_datetime(w.index.date)).size()
        ok = [d for d, c in n.items() if d.weekday() < 5 and (d.month, d.day) not in {(12, 25), (1, 1)} and c >= 768]
    return pd.DatetimeIndex(sorted(ok))


def choose_d(gross: pd.Series) -> int:
    m = gross.mean()
    return -1 if (not np.isnan(m) and m < 0) else 1


def evaluate(gross: pd.Series, days: pd.DatetimeIndex, d: int, cost: float) -> dict:
    g = gross.reindex(days)
    nt = E.net(g, d, cost)
    stress = E.net(g, d, 2 * cost)
    ys = E.year_sums(nt)
    t = T1.nw_t(nt.values)
    return {"d": int(d), "n_trades": int(g.notna().sum()), "mean_net": float(nt.mean()), "stress_mean": float(stress.mean()),
            "gross_per_trade": float((d * g).mean()) if g.notna().any() else np.nan,
            "t_nw": t, "p_one": float(1 - stats.norm.cdf(t)) if not np.isnan(t) else 1.0,
            "years": len(ys), "years_pos": sum(v > 0 for v in ys.values()), "per_anno": {k: round(v, 6) for k, v in ys.items()}}


def stage2_pass(s: dict) -> bool:
    return s["p_holm"] < 0.05 and s["stress_mean"] > 0 and s["years_pos"] >= 2


def stage3_pass(s: dict) -> bool:
    return s["t_nw"] > 1.65 and s["p_holm"] < 0.05 and s["stress_mean"] > 0 and s["years_pos"] >= 2


def select(rows: list[dict], k: int = TOP_K) -> list[dict]:
    out = []
    for inst in dict.fromkeys(r["inst"] for r in rows):
        ok = sorted((r for r in rows if r["inst"] == inst and r["pass"]), key=lambda r: -r["t_nw"])
        out += ok[:k]
    return out


def key(c: dict) -> str:
    return f"{c['inst']}|{c['family']}|E{c['E']}|H{c['H']}|L{c['L']}"


def load(inst: str, end: str):
    sym, kind, cost, usd = INSTR[inst]
    b = pd.read_parquet(BARS / f"{sym}_1m_24h.parquet")
    b.index = b.index.tz_convert(E.TZ)
    b = b[b.index < pd.Timestamp(end, tz=E.TZ) + pd.Timedelta(days=1)]  # niente dati oltre la fine del periodo
    days = valid_days(b, kind)
    grid = E.price_grid(b, days, E.offsets(kind))
    if kind == "index":  # emendamento 1: ancora = P(16:00) della sessione NYSE precedente
        first = pd.Timestamp(b.index.min().date())
        sess = pd.DatetimeIndex(sorted(d for d in NYSE if first <= d <= pd.Timestamp(end)))
        p16 = E.price_grid(b, sess, [E.CLOSE])[E.CLOSE]
        grid["prev_close"] = p16.shift(1).reindex(days).to_numpy()
    return kind, cost, usd, days, grid


def period_days(days: pd.DatetimeIndex, stage: str) -> pd.DatetimeIndex:
    s, e = PERIODS[stage]
    return days[((days >= s) if s else True) & (days <= e)]


def main(argv: list[str]) -> None:
    stage = argv[0] if argv else ""
    if stage not in PERIODS:
        sys.exit("uso: run_t14.py scoperta | convalida | holdout")
    if stage in PREV and not (OUT / FILES[PREV[stage]]).exists():
        sys.exit(f"manca lo stadio precedente ({PREV[stage]}): non si esegue {stage}.")
    if (OUT / FILES[stage]).exists():
        sys.exit(f"stadio {stage} gia' eseguito: non si riesegue.")
    lock = OUT / f"T14_{stage}.started"
    if lock.exists():
        sys.exit(f"stadio {stage} gia' avviato in passato (lock presente): non si riesegue.")
    lock.write_text(pd.Timestamp.now(tz="UTC").isoformat())
    end = PERIODS[stage][1]
    if stage == "scoperta":
        rows = []
        for inst in INSTR:
            kind, cost, usd, days, grid = load(inst, end)
            pdays = period_days(days, stage)
            anchor = E.ANCHOR[kind]
            cfgs = E.configs(kind)
            for c in cfgs:
                g = E.daily_gross(c, grid, anchor).reindex(pdays)
                s = evaluate(g, pdays, choose_d(g), cost)
                rows.append({"inst": inst, **c, **s, "usd_per_trade_net": s["mean_net"] * len(pdays) / max(s["n_trades"], 1) * usd})
                rows[-1]["pass"] = E.stage1_pass(rows[-1])
            print(f"{inst}: {len(cfgs)} configurazioni, {len(pdays)} giorni, {sum(r['pass'] for r in rows if r['inst'] == inst)} passano", flush=True)
        expected = sum(len(E.configs(v[1])) for v in INSTR.values())
        assert len(rows) == expected, len(rows)
        sel = select(rows)
        res = {"n_config": len(rows), "n_passano_stadio1": int(sum(r["pass"] for r in rows)),
               "falsi_positivi_attesi_H0": round(len(rows) * 2 * (1 - stats.norm.cdf(3.0)), 1),
               "selezionate": [{**r, "key": key(r)} for r in sel]}
    else:
        prev = json.loads((OUT / FILES[PREV[stage]]).read_text())
        cand = prev["selezionate"] if stage == "convalida" else prev["sopravvissute"]
        evals = []
        for inst in dict.fromkeys(c["inst"] for c in cand):
            kind, cost, usd, days, grid = load(inst, end)
            pdays = period_days(days, stage)
            for c in (c for c in cand if c["inst"] == inst):
                g = E.daily_gross(c, grid, E.ANCHOR[kind]).reindex(pdays)
                s = evaluate(g, pdays, c["d"], cost)
                if stage == "holdout":
                    full = E.daily_gross(c, grid, E.ANCHOR[kind]).reindex(days)
                    s["t_nw_2010_2024"] = evaluate(full, days, c["d"], cost)["t_nw"]
                evals.append({**{k: c[k] for k in ("key", "inst", "family", "E", "H", "L", "d")}, **s})
        adj = T1.holm({e["key"]: e["p_one"] for e in evals}) if evals else {}
        for e in evals:
            e["p_holm"] = adj[e["key"]]
            e["pass"] = stage2_pass(e) if stage == "convalida" else stage3_pass(e)
        surv = [e for e in evals if e["pass"]]
        res = {"n_candidate": len(evals), "valutate": evals,
               ("sopravvissute" if stage == "convalida" else "EDGE_CANDIDATI"): surv}
    (OUT / FILES[stage]).write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))
    if stage == "scoperta":
        tab = pd.DataFrame([{k: v for k, v in r.items() if k != "per_anno"} for r in rows])
        tab[["H", "L"]] = tab[["H", "L"]].astype(str)
        tab.to_parquet(OUT / "T14_scoperta_tutte.parquet")
    summary = {k: v for k, v in res.items() if k not in ("valutate", "selezionate")}
    print(json.dumps(summary, indent=2, default=str)[:4000])
    if stage == "scoperta":
        for r in res["selezionate"]:
            print(r["key"], "d", r["d"], "t", round(r["t_nw"], 2), "trade", r["n_trades"], "$/trade", round(r["usd_per_trade_net"], 1))


if __name__ == "__main__":
    main(sys.argv[1:])
