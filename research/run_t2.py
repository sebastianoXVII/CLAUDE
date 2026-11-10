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
               "sweep_true", "sweep_placebo"]].to_string(float_format=lambda v: f"{v:,.4f}"))
    print(f"\nSopravvissuti stadio 1: {surv or 'NESSUNO -> T2 MORTO'}")
    stage2 = {}
    for key in surv:
        inst, fam, H = key
        _sym, _k, usd, cost = INSTR[inst]
        ev, d = evs[key], np.sign(res[key]["coef"])
        days = pd.bdate_range(*IS)
        for kind in ("true", "placebo"):
            e = ev[ev["kind"] == kind]
            per_trade = d * e["y"] - cost
            daily = per_trade.groupby(e["date"]).sum().reindex(days, fill_value=0.0)
            traded = daily != 0
            m = T1.metrics(daily, traded, usd)
            m["per_trade_pt"] = float(per_trade.mean())
            m["stress2x_media_pt"] = float((d * e["y"] - 2 * cost).groupby(e["date"]).sum().reindex(days, fill_value=0.0).mean())
            yr = daily.groupby(daily.index.year).sum()
            m["anni_positivi"] = f"{int((yr > 0).sum())}/{len(yr)}"
            stage2[f"{inst}_{fam}_H{H}_{kind}"] = m
        t, p = stage2[f"{inst}_{fam}_H{H}_true"], stage2[f"{inst}_{fam}_H{H}_placebo"]
        pos, yrs = map(int, t["anni_positivi"].split("/"))
        t["criteri"] = {"t>3": t["t_nw"] > 3, "stress2x>0": t["stress2x_media_pt"] > 0,
                        "anni>=5/7": pos * 7 >= 5 * yrs, "batte_placebo": t["per_trade_pt"] > p["per_trade_pt"]}
        t["SOPRAVVIVE"] = all(t["criteri"].values())
    if stage2:
        print("\n=== STADIO 2 (tradabilita', costi base) ===")
        print(pd.DataFrame(stage2).T.reindex(columns=["trade", "win_rate", "per_trade_pt", "expectancy_usd_per_trade",
              "profit_factor", "sharpe_ann", "max_dd_usd", "t_nw", "stress2x_media_pt", "anni_positivi", "SOPRAVVIVE"]
              ).to_string(float_format=lambda v: f"{v:,.3f}"))
    out = {"stage1": {f"{a}_{b}_H{c}": v for (a, b, c), v in res.items()},
           "stage1_survivors": [f"{a}_{b}_H{c}" for a, b, c in surv], "stage2": stage2}
    (OUT / "T2_in_sample.json").write_text(json.dumps(out, indent=2, default=str, ensure_ascii=False))
    print(f"\nsalvato: {OUT / 'T2_in_sample.json'}")


if __name__ == "__main__":
    main()
