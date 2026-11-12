"""T16: numeri tondi (Osler). Spec: research/preregistration/T16_numeri_tondi.md.
Uso: python3 research/run_t16.py insample | holdout
Ogni stadio rifiuta di ripetersi (file risultati o lock di avvio) e non legge barre oltre la fine del proprio periodo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import t1_engine as T1  # noqa: E402
import t14_engine as E14  # noqa: E402
import t16_engine as E  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BARS, OUT = ROOT / "data" / "bars", ROOT / "research" / "results"
_FX = dict(scale=10000, D=0.0020, delta=0.0005, A=(100, ()), B=(50, (100,)), C=(25, (50,)))
INSTR = {"EURUSD": dict(cost=0.00010, **_FX), "GBPUSD": dict(cost=0.00013, **_FX),
         "XAUUSD": dict(cost=0.35, scale=100, D=3.0, delta=1.0, A=(5000, ()), B=(1000, (5000,)), C=(500, (1000,)))}
TIERS, KINDS = ("A", "B"), ("R", "S")
PERIODS = {"insample": ("2010-01-01", "2019-12-31"), "holdout": ("2020-01-01", "2024-12-31")}
COVERAGE = {"insample": ("2010-01-31", "2019-12-30"), "holdout": ("2010-01-31", "2024-12-30")}  # prima data <=, ultima >=


def test_keys() -> list[str]:
    return [f"{s}_{t}_{k}" for s in INSTR for t in TIERS for k in KINDS]


def insample_pass(m: dict) -> bool:
    return bool(m["t_nw"] > 3.0 and m["p_holm"] < 0.05 and m["stress_mean"] > 0 and m["years_pos"] >= 6 and m["n_trades"] >= 200)


def holdout_pass(m: dict) -> bool:
    return bool(m["t_nw"] > 1.65 and m["stress_mean"] > 0 and m["years_pos"] >= 3)


def load(sym: str, end: str) -> pd.DataFrame:
    b = pd.read_parquet(BARS / f"{sym}_1m_24h.parquet")
    b = b[~b.index.duplicated(keep="first")].sort_index()
    b.index = b.index.tz_convert(E.TZ)
    return b[pd.DatetimeIndex(E.trading_day(b.index)) <= pd.Timestamp(end)]


def trades_all(bars_et: pd.DataFrame, sym: str) -> dict[tuple[str, str], pd.DataFrame]:
    """Trade per (tier, evento) per A, B e il controllo C, scorrendo i giorni validi (stato azzerato ogni giorno)."""
    p = INSTR[sym]
    days = set(E.valid_days(bars_et))
    td = pd.DatetimeIndex(E.trading_day(bars_et.index))
    out = {(t, k): [] for t in ("A", "B", "C") for k in KINDS}
    cuts = np.flatnonzero(td[1:] != td[:-1]) + 1
    for lo_i, hi_i in zip(np.r_[0, cuts], np.r_[cuts, len(td)]):
        if td[lo_i] not in days:
            continue
        day = bars_et.iloc[lo_i:hi_i]
        lo, hi = day["low"].min() - p["D"] - p["delta"], day["high"].max() + p["D"] + p["delta"]
        for t in ("A", "B", "C"):
            lv = E.levels(lo, hi, p["scale"], *p[t])
            for k in KINDS:
                tr = E.day_trades(day, lv, p["D"], p["delta"], k, p["cost"])
                if len(tr):
                    out[(t, k)].append(tr)
    return {key: (pd.concat(v, ignore_index=True) if v else pd.DataFrame(columns=E.COLS)) for key, v in out.items()}


def evaluate(trades: pd.DataFrame, days: pd.DatetimeIndex, s: str, e: str) -> dict:
    days = days[(days >= s) & (days <= e)]
    tr = trades[(pd.DatetimeIndex(trades["day"]) >= s) & (pd.DatetimeIndex(trades["day"]) <= e)] if len(trades) else trades
    r, st = E.daily_pnl(tr, days, 1.0), E.daily_pnl(tr, days, 2.0)
    t = T1.nw_t(r.values)
    ys = E14.year_sums(r)
    return {"giorni": int(len(r)), "n_trades": int(len(tr)), "media_giornaliera": float(r.mean()), "t_nw": t,
            "p_one": float(1 - stats.norm.cdf(t)) if np.isfinite(t) else 1.0, "stress_mean": float(st.mean()),
            "media_lorda_trade": float(tr["gross"].mean()) if len(tr) else None,
            "years": len(ys), "years_pos": sum(v > 0 for v in ys.values()), "per_anno": {k: round(v, 6) for k, v in ys.items()}}


def controls(tr: dict, s: str, e: str) -> dict:
    """Descrittivo: gross medio per trade su A, B, C e Welch A-C, B-C (lordo, per trade)."""
    def g(x):
        if not len(x):
            return np.array([])
        d = pd.DatetimeIndex(x["day"])
        return x.loc[(d >= s) & (d <= e), "gross"].to_numpy(float)
    out = {}
    for k in KINDS:
        a, b, c = g(tr[("A", k)]), g(tr[("B", k)]), g(tr[("C", k)])
        row = {f"n_{n}": int(len(v)) for n, v in zip("ABC", (a, b, c))}
        row.update({f"lordo_medio_{n}": (float(v.mean()) if len(v) else None) for n, v in zip("ABC", (a, b, c))})
        for n, v in (("A", a), ("B", b)):
            row[f"welch_t_{n}_vs_C"] = float(stats.ttest_ind(v, c, equal_var=False).statistic) if len(v) > 1 and len(c) > 1 else None
        out[k] = row
    return out


def preflight(stage: str) -> None:
    first_max, last_min = (pd.Timestamp(x, tz="UTC") for x in COVERAGE[stage])
    for sym in INSTR:
        f = BARS / f"{sym}_1m_24h.parquet"
        if not f.exists():
            sys.exit(f"manca il file di {sym} ({f}): nessuno stadio avviato.")
        idx = pd.read_parquet(f, columns=["close"]).index
        if not isinstance(idx, pd.DatetimeIndex) or idx.tz is None:
            sys.exit(f"indice non valido per {sym}: nessuno stadio avviato.")
        if idx.min() > first_max or idx.max() < last_min:
            sys.exit(f"copertura insufficiente per {sym} ({idx.min()} -> {idx.max()}): nessuno stadio avviato.")


def main(argv: list[str]) -> None:
    stage = argv[0] if argv else ""
    if stage not in PERIODS:
        sys.exit("uso: run_t16.py insample | holdout")
    if stage == "holdout" and not (OUT / "T16_insample.json").exists():
        sys.exit("manca lo stadio insample: holdout non eseguibile.")
    if (OUT / f"T16_{stage}.json").exists():
        sys.exit(f"stadio {stage} gia' eseguito.")
    lock = OUT / f"T16_{stage}.started"
    if lock.exists():
        sys.exit(f"stadio {stage} gia' avviato in passato (lock): non si riesegue.")
    keys = test_keys()
    if stage == "holdout":
        keys = json.loads((OUT / "T16_insample.json").read_text())["sopravvissuti"]
        if not keys:
            sys.exit("nessun test sopravvissuto all'in-sample: l'hold-out non si calcola.")
    preflight(stage)
    lock.write_text(pd.Timestamp.now(tz="UTC").isoformat())
    s, e = PERIODS[stage]
    res, ctrl = {}, {}
    for sym in INSTR:
        if not any(k.startswith(sym + "_") for k in keys):
            continue
        b = load(sym, e)
        days = E.valid_days(b)
        tr = trades_all(b, sym)
        for t in TIERS:
            for k in KINDS:
                if f"{sym}_{t}_{k}" in keys:
                    res[f"{sym}_{t}_{k}"] = evaluate(tr[(t, k)], days, s, e)
        for k, row in controls(tr, s, e).items():
            ctrl[f"{sym}_{k}"] = row
    if stage == "insample":
        adj = T1.holm({k: res[k]["p_one"] for k in res})
        for k in res:
            res[k]["p_holm"] = adj[k]
            res[k]["SOPRAVVIVE"] = insample_pass(res[k])
        out = {"periodo": f"{s} -> {e}", "test": res, "controlli": ctrl, "sopravvissuti": [k for k in res if res[k]["SOPRAVVIVE"]]}
    else:
        for k in res:
            res[k]["EDGE"] = holdout_pass(res[k])
        out = {"periodo": f"{s} -> {e}", "test": res, "controlli": ctrl, "EDGE": [k for k in res if res[k]["EDGE"]]}
    (OUT / f"T16_{stage}.json").write_text(json.dumps(out, indent=2, default=str, ensure_ascii=False))
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main(sys.argv[1:])
