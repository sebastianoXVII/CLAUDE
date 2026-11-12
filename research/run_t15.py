"""Esegue T15 (research/preregistration/T15_trend_following_diversificato.md): python3 research/run_t15.py insample | holdout.
Ogni stadio rifiuta di ripetersi (file risultati o lock di avvio) e non legge dati oltre la fine del proprio periodo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import t14_engine as E14  # noqa: E402  (year_sums)
import t15_engine as E  # noqa: E402
import t1_engine as T1  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DAILY, OUT = ROOT / "data" / "bars" / "daily", ROOT / "research" / "results"
INSTR = {**{s: 1e-4 for s in ("EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD")},
         **{s: 1.5e-4 for s in ("EURJPY", "EURGBP", "AUDJPY")},
         **{s: 2e-4 for s in ("SPXUSD", "NSXUSD", "GRXEUR", "UKXGBP", "FRXEUR", "ETXEUR", "XAUUSD")},
         **{s: 3e-4 for s in ("JPXJPY", "AUXAUD", "HKXHKD")},
         "WTIUSD": 4e-4, "BCOUSD": 4e-4, "XAGUSD": 5e-4}
FIN = 0.03
PERIODS = {"insample": ("2011-01-01", "2019-12-31"), "holdout": ("2020-01-01", "2024-12-31")}
VARIANTS = ["V1", "V2"]


def insample_pass(s: dict) -> bool:
    return s["t_nw"] > 3.0 and s["p_holm"] < 0.05 and s["stress_mean"] > 0 and s["years_pos"] >= 6


def holdout_pass(s: dict) -> bool:
    return s["t_nw"] > 1.65 and s["stress_mean"] > 0 and s["years_pos"] >= 3


def prop_descriptives(r: pd.Series) -> dict:
    k = 0.10 / (r.std() * np.sqrt(E.ANN))
    x = r * k
    eq = (1 + x).cumprod()
    w = x.rolling(10).sum().dropna()
    return {"vol_ann_scalata": float(x.std() * np.sqrt(E.ANN)), "rend_ann_scalato": float(x.mean() * E.ANN),
            "max_dd": float((eq / eq.cummax() - 1).min()), "giorno_peggiore": float(x.min()),
            "quota_giorni_sotto_-2%": float((x < -0.02).mean()), "quota_giorni_sotto_-5%": float((x < -0.05).mean()),
            "quota_finestre_10_giorni_borsa_positive": float((w > 0).mean())}


def min_end(sym: str, stage: str):
    """Ultima data minima richiesta (emendamento 1: ETXEUR finisce nel 2019 con anno parziale, WTIUSD nel 2023). ETXEUR: il file 2019 finisce il 2019-02-01, soglia 2019-01-31 (nota in research_notes/T15_provenienza_dati.md)."""
    if stage == "insample":
        return pd.Timestamp("2019-01-31" if sym == "ETXEUR" else "2019-11-30")
    if sym == "ETXEUR":
        return None
    return pd.Timestamp("2023-11-30" if sym == "WTIUSD" else "2024-11-30")


def preflight(stage: str) -> None:
    """Controlli sui file PRIMA del lock: presenza, schema, copertura."""
    for sym in INSTR:
        f = DAILY / f"{sym}_1d.parquet"
        if not f.exists():
            sys.exit(f"manca il file di {sym} ({f}): nessuno stadio avviato.")
        d = pd.read_parquet(f)
        if not {"close", "n_bars"} <= set(d.columns) or not isinstance(d.index, pd.DatetimeIndex) or d.index.tz is not None:
            sys.exit(f"schema non valido per {sym}: nessuno stadio avviato.")
        need = min_end(sym, stage)
        if d.index.min() > pd.Timestamp("2010-12-31") or (need is not None and d.index.max() < need):
            sys.exit(f"copertura insufficiente per {sym} ({d.index.min().date()} -> {d.index.max().date()}): nessuno stadio avviato.")


# Emendamento 2 (research/preregistration/T15_emendamento_2.md): tratto del file GRXEUR che non è il DAX
EXCLUDE = {"GRXEUR": [("2020-06-15", "2023-12-01")]}


def load(sym: str, end: str) -> pd.DataFrame:
    d = pd.read_parquet(DAILY / f"{sym}_1d.parquet")
    return d[d.index <= pd.Timestamp(end)]


def parts_for(variant: str, end: str) -> tuple[dict, list]:
    parts, used = {}, []
    for sym, cost in INSTR.items():
        f = DAILY / f"{sym}_1d.parquet"
        if not f.exists():
            continue
        parts[sym] = E.instrument_parts(E.valid_close(load(sym, end)), variant, cost, FIN, EXCLUDE.get(sym))
        used.append(sym)
    return parts, used


def evaluate(parts: dict, s: str, e: str) -> dict:
    out = {}
    for mult, name in ((1.0, "base"), (2.0, "stress")):
        p = E.portfolio(parts, cost_mult=mult)
        out[name] = p[(p.index >= s) & (p.index <= e)]
    r = out["base"]
    ys = E14.year_sums(r)
    t = T1.nw_t(r.values)
    gross = E.portfolio({k: v.assign(tcost=0.0, fcost=0.0) for k, v in parts.items()})
    gross = gross[(gross.index >= s) & (gross.index <= e)]
    return {"giorni": int(len(r)), "media_giornaliera": float(r.mean()), "sharpe_ann": float(r.mean() / r.std() * np.sqrt(E.ANN)),
            "t_nw": t, "p_one": float(1 - stats.norm.cdf(t)), "stress_mean": float(out["stress"].mean()),
            "media_lorda": float(gross.mean()), "years": len(ys), "years_pos": sum(v > 0 for v in ys.values()),
            "per_anno": {k: round(v, 5) for k, v in ys.items()}, "prop_descrittivi": prop_descriptives(r)}


def main(argv: list[str]) -> None:
    stage = argv[0] if argv else ""
    if stage not in PERIODS:
        sys.exit("uso: run_t15.py insample | holdout")
    if stage == "holdout" and not (OUT / "T15_insample.json").exists():
        sys.exit("manca lo stadio insample: holdout non eseguibile.")
    if (OUT / f"T15_{stage}.json").exists():
        sys.exit(f"stadio {stage} gia' eseguito.")
    lock = OUT / f"T15_{stage}.started"
    if lock.exists():
        sys.exit(f"stadio {stage} gia' avviato in passato (lock): non si riesegue.")
    preflight(stage)
    lock.write_text(pd.Timestamp.now(tz="UTC").isoformat())
    s, e = PERIODS[stage]
    if stage == "insample":
        res, used = {}, []
        for v in VARIANTS:
            parts, used = parts_for(v, e)
            res[v] = evaluate(parts, s, e)
        adj = T1.holm({v: res[v]["p_one"] for v in VARIANTS})
        for v in VARIANTS:
            res[v]["p_holm"] = adj[v]
            res[v]["SOPRAVVIVE"] = insample_pass(res[v])
        out = {"periodo": f"{s} -> {e}", "strumenti_usati": used, "varianti": res,
               "sopravvissute": [v for v in VARIANTS if res[v]["SOPRAVVIVE"]]}
    else:
        prev = json.loads((OUT / "T15_insample.json").read_text())
        res = {}
        for v in prev["sopravvissute"]:
            parts, used = parts_for(v, e)
            res[v] = evaluate(parts, s, e)
            res[v]["EDGE"] = holdout_pass(res[v])
        out = {"periodo": f"{s} -> {e}", "varianti": res, "EDGE": [v for v in res if res[v]["EDGE"]]}
    (OUT / f"T15_{stage}.json").write_text(json.dumps(out, indent=2, default=str, ensure_ascii=False))
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main(sys.argv[1:])
