"""T13: concetti di sessione (motore e runner di T8, invariati) su EURUSD, GBPUSD, XAUUSD.
Spec: research/preregistration/T13_concetti_sessione_forex_oro.md
    python3 research/run_t13.py             # in-sample 2010 -> 2023-12-31 (esecuzione unica)
    python3 research/run_t13.py --holdout   # solo per i sopravvissuti"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t8 as R8  # noqa: E402
import t1_engine as T1  # noqa: E402
from lab import journal  # noqa: E402

# file, $ per unità di prezzo (1 lotto standard), costo round trip in unità di prezzo (pre-registrazione §4)
INSTR = {"EURUSD": ("EURUSD", 100_000.0, 0.00010), "GBPUSD": ("GBPUSD", 100_000.0, 0.00013), "XAUUSD": ("XAUUSD", 100.0, 0.35)}
START = pd.Timestamp("2010-01-01")
OUT = R8.OUT
CHARTS = R8.ROOT / "data" / "charts" / "T13"


class _Renamer:
    """Diario di T8 con il nome strategia di T13: T13_<strumento>_<ipotesi>."""

    def __init__(self, jr):
        self.jr = jr

    def add(self, rec):
        rec["strategy"] = f"T13_{rec['instrument']}_{rec['strategy'].removeprefix('T8_')}"
        self.jr.add(rec)


def survives_is(m: dict) -> bool:
    pos, yrs = map(int, m["anni_positivi"].split("/"))
    return bool(m["t_nw"] > 3 and m["p_holm"] < 0.05 and m["stress2x_media_pt"] > 0 and pos * 3 >= 2 * yrs and m["n_trades"] >= 150)


def survives_ho(m: dict, n_days: int) -> str:
    if n_days < 200:
        return "INCONCLUSIVO"
    return "SOPRAVVIVE" if (m["t_nw"] > 2 and m["stress2x_media_pt"] > 0) else "MORTO"


def _run(inst, period, keep=None, jr=None):
    df, valid = R8.run(inst, period, keep=keep, jr=jr)
    if len(valid):
        mask = valid >= START
        df = df[df["date"] >= START] if len(df) else df
        valid = valid[mask]
    return df, valid


def main():
    R8.INSTR = INSTR
    R8.CHARTS = CHARTS
    jr0 = journal.Journal(OUT / "journal.sqlite")
    is_file = OUT / "T13_in_sample.json"
    if "--holdout" not in sys.argv:
        if is_file.exists():
            sys.exit("T13 in-sample gia' eseguito.")
        missing = [s for s, _u, _c in INSTR.values() if not (R8.BARS / f"{s}_1m_24h.parquet").exists()]
        if missing:
            sys.exit(f"Dati mancanti, T13 non eseguito: {missing}")
        for inst in INSTR:
            for h in R8.HYP:
                jr0.clear_strategy(f"T13_{inst}_{h}")
        res, pv = {}, {}
        for inst, (_s, usd, cost) in INSTR.items():
            df, valid = _run(inst, "IS", jr=_Renamer(jr0))
            for h in R8.HYP:
                for v in ("base", "HTF"):
                    key = f"{inst}_{h}_{v}"
                    m = R8.stats(df[df["key"] == key] if len(df) else df, valid, usd, cost)
                    m["giorni"] = int(len(valid))
                    res[key], pv[key] = m, m["p_unilaterale"]
        for key, p in T1.holm(pv).items():
            res[key]["p_holm"] = p
            res[key]["SOPRAVVIVE"] = survives_is(res[key])
        is_file.write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))
        cols = ["n_trades", "win_rate", "gross_pt_per_trade", "profit_factor", "sharpe_ann", "t_nw", "p_holm",
                "stress2x_media_pt", "anni_positivi", "SOPRAVVIVE"]
        print(pd.DataFrame(res).T.reindex(columns=cols).to_string(float_format=lambda v: f"{v:,.5f}"))
        surv = [k for k, m in res.items() if m["SOPRAVVIVE"]]
        print("Sopravvissuti:", surv or "NESSUNO -> T13 MORTO")
        return
    surv = [k for k, m in json.loads(is_file.read_text()).items() if m.get("SOPRAVVIVE")]
    if not surv:
        sys.exit("T13 MORTO in-sample: hold-out non calcolato.")
    ho_file = OUT / "T13_holdout.json"
    if ho_file.exists():
        sys.exit("T13 hold-out gia' eseguito.")
    res = {}
    for inst in sorted({k.split("_")[0] for k in surv}):
        _s, usd, cost = INSTR[inst]
        keep = {k for k in surv if k.startswith(inst)}
        df, valid = _run(inst, "HO", keep=keep, jr=_Renamer(jr0))
        for k in keep:
            m = R8.stats(df[df["key"] == k] if len(df) else df, valid, usd, cost)
            m["ESITO_HO"] = survives_ho(m, len(valid))
            res[k] = m
    ho_file.write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))
    print(pd.DataFrame(res).T.to_string())


if __name__ == "__main__":
    main()
