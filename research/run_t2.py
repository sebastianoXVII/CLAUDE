"""Esegue T2 in-sample (2017-2023) secondo research/preregistration/T2_livelli_di_stop.md.
Stadio 1 (effetto vs placebo) -> stadio 2 (tradabilita') solo per i sopravvissuti. Hold-out non incluso qui."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import t1_engine as T1  # noqa: E402
import t2_engine as E  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BARS, OUT = ROOT / "data" / "bars", ROOT / "research" / "results"
INSTR = {"ES": ("SPY", 10.0, 50.0, 0.33), "NQ": ("QQQ", 41.0, 20.0, 0.45)}  # simbolo, k, $/pt, costo base pt
IS = ("2017-01-01", "2023-12-31")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    evs, res = {}, {}
    for inst, (sym, k, _usd, _c) in INSTR.items():
        raw = pd.read_parquet(BARS / f"{sym}_1m_raw.parquet")
        for fam in ("PD", "PM"):
            for H in (15, 30):
                ev = E.events(raw, fam, H, k)
                ev = ev[(ev["date"] >= IS[0]) & (ev["date"] <= IS[1])]
                evs[(inst, fam, H)] = ev
                res[(inst, fam, H)] = E.stage1(ev)
                print(f"{inst} {fam} H={H}: eventi veri={res[(inst, fam, H)]['n_true']} placebo={res[(inst, fam, H)]['n_placebo']}", flush=True)
    surv = E.stage1_survivors(res)
    tab = pd.DataFrame({f"{a}_{b}_H{c}": v for (a, b, c), v in res.items()}).T
    print("\n=== STADIO 1 (in-sample 2017-2023): y = punti indice nella direzione della rottura ===")
    print(tab[["n_true", "n_placebo", "mean_y_true", "mean_y_placebo", "coef", "t", "p", "p_holm",
               "coef_adj", "t_adj", "sweep_true", "sweep_placebo"]].to_string(float_format=lambda v: f"{v:,.4f}"))
    print(f"\nSopravvissuti stadio 1: {surv or 'NESSUNO -> T2 MORTO'}")
    stage2 = {}
    lv_cache = {}
    for key in surv:
        inst, fam, H = key
        sym, _k, usd, cost = INSTR[inst]
        if sym not in lv_cache:
            lv_cache[sym] = E.day_levels(pd.read_parquet(BARS / f"{sym}_1m_raw.parquet"))
        valid = lv_cache[sym].dropna(subset=E.FAMILY_COLS[fam]).loc[IS[0]:IS[1]].index
        ev, d = evs[key], np.sign(res[key]["coef"])
        for kind in ("true", "placebo"):
            stage2[f"{inst}_{fam}_H{H}_{kind}"] = E.stage2(ev[ev["kind"] == kind], d, cost, valid, usd)
        t = stage2[f"{inst}_{fam}_H{H}_true"]
        pos, yrs = map(int, t["anni_positivi"].split("/"))
        # 'batte_placebo' e' automatico dopo lo stadio 1 (emendamento 1): riportato, non e' evidenza indipendente
        t["criteri"] = {"t>3": t["t_nw"] > 3, "stress2x>0": t["stress2x_media_pt"] > 0, "anni>=5/7": pos * 7 >= 5 * yrs}
        t["SOPRAVVIVE"] = all(t["criteri"].values())
    if stage2:
        print("\n=== STADIO 2 (tradabilita', costi base) ===")
        print(pd.DataFrame(stage2).T.reindex(columns=["n_trades", "trade_win_rate", "per_trade_pt", "per_trade_usd",
              "profit_factor", "sharpe_ann", "max_dd_usd", "t_nw", "stress2x_media_pt", "anni_positivi", "SOPRAVVIVE"]
              ).to_string(float_format=lambda v: f"{v:,.3f}"))
    out = {"stage1": {f"{a}_{b}_H{c}": v for (a, b, c), v in res.items()},
           "stage1_survivors": [f"{a}_{b}_H{c}" for a, b, c in surv], "stage2": stage2}
    (OUT / "T2_in_sample.json").write_text(json.dumps(out, indent=2, default=str, ensure_ascii=False))
    print(f"\nsalvato: {OUT / 'T2_in_sample.json'}")


if __name__ == "__main__":
    main()
