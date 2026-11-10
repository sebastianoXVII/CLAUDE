"""Esegue T4 in-sample (2017-2023) secondo research/preregistration/T4_concetti_retail.md."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import t1_engine as T1  # noqa: E402
import t4_engine as E  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BARS, OUT = ROOT / "data" / "bars", ROOT / "research" / "results"
INSTR = {"ES": ("SPY", 10.0, 50.0, 0.33), "NQ": ("QQQ", 41.0, 20.0, 0.45)}
IS = ("2017-01-01", "2023-12-31")
CONCEPTS = ("C1_ORB", "C2_gap", "C3_VWAP", "C4_FVG")


def trades_for(sym: str, k: float) -> pd.DataFrame:
    raw = pd.read_parquet(BARS / f"{sym}_1m_raw.parquet")
    raw.index = raw.index.tz_convert(E.TZ)
    rth = raw.between_time("09:30", "15:59")
    rows, prev_close = [], None
    for d, g in rth.groupby(rth.index.date):
        ts = pd.Timestamp(d)
        if ts.weekday() >= 5 or ts in T1.EARLY_CLOSES or len(g) < 300:
            continue
        specs = {"C1_ORB": E.orb(g), "C2_gap": E.gap_fill(g, prev_close) if prev_close else None,
                 "C3_VWAP": E.vwap_magnet(g), "C4_FVG": E.fvg(g)}
        for c, t in specs.items():
            if t is None:
                rows.append({"date": ts, "concept": c, "traded": False, "gross_pts": 0.0, "reason": None})
                continue
            r = E.simulate(g, t["start"], t["side"], t["p_in"], t["stop"], t["target"], t["last_bar"], t["entry_bar_stop"])
            rows.append({"date": ts, "concept": c, "traded": True,
                         "gross_pts": t["side"] * (r["p_out"] - t["p_in"]) * k, "reason": r["reason"]})
        prev_close = float(g["close"].iloc[-1])
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    res, pvals = {}, {}
    for inst, (sym, k, usd, cost) in INSTR.items():
        tr = trades_for(sym, k)
        tr = tr[(tr["date"] >= IS[0]) & (tr["date"] <= IS[1])]
        for c in CONCEPTS:
            x = tr[tr["concept"] == c].set_index("date")
            traded = x["traded"]
            net = (x["gross_pts"] - cost).where(traded, 0.0)
            m = T1.metrics(net, traded, usd)
            m["gross_pt_per_trade"] = float(x.loc[traded, "gross_pts"].mean())
            m["stress2x_media_pt"] = float((x["gross_pts"] - 2 * cost).where(traded, 0.0).mean())
            reasons = x.loc[traded, "reason"].value_counts(normalize=True).round(3).to_dict()
            m["uscite"] = reasons
            yr = net.groupby(net.index.year).sum()
            m["anni_positivi"] = f"{int((yr > 0).sum())}/{len(yr)}"
            m["pnl_pt_per_anno"] = {int(a): round(float(b), 1) for a, b in yr.items()}
            res[f"{inst}_{c}"] = m
            pvals[f"{inst}_{c}"] = m["p_unilaterale"]
        print(f"{inst} fatto", flush=True)
    for key, p in T1.holm(pvals).items():
        m = res[key]
        m["p_holm"] = p
        pos, yrs = map(int, m["anni_positivi"].split("/"))
        m["criteri"] = {"t>3": m["t_nw"] > 3, "holm<0.05": p < 0.05, "stress2x>0": m["stress2x_media_pt"] > 0,
                        "anni>=5/7": pos * 7 >= 5 * yrs}
        m["passa_singolo"] = all(m["criteri"].values())
    for c in CONCEPTS:
        both = res[f"ES_{c}"]["passa_singolo"] and res[f"NQ_{c}"]["passa_singolo"]
        for inst in INSTR:
            res[f"{inst}_{c}"]["SOPRAVVIVE"] = both
    cols = ["trade", "win_rate", "payoff", "gross_pt_per_trade", "expectancy_pt_per_trade", "expectancy_usd_per_trade",
            "profit_factor", "sharpe_ann", "max_dd_usd", "t_nw", "p_holm", "stress2x_media_pt", "anni_positivi", "SOPRAVVIVE"]
    print("\n=== T4 IN-SAMPLE 2017-2023 (netto costi base, punti indice) ===")
    print(pd.DataFrame(res).T.reindex(columns=cols).to_string(float_format=lambda v: f"{v:,.3f}"))
    for key, m in res.items():
        print(f"  {key}: uscite {m['uscite']} | P&L pt/anno {m['pnl_pt_per_anno']}")
    surv = sorted({k.split('_', 1)[1] for k, m in res.items() if m["SOPRAVVIVE"]})
    print(f"\nSopravvissuti: {surv or 'NESSUNO -> T4 MORTO'}")
    (OUT / "T4_in_sample.json").write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
