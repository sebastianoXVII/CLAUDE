"""T5: ipotesi generate da T4, SOLO hold-out 2024-fine, esecuzione unica. Spec: research/preregistration/T5_holdout_ipotesi_generate.md"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t4 as R  # noqa: E402
import t1_engine as T1  # noqa: E402
import t4_engine as E  # noqa: E402

OUT = R.OUT / "T5_holdout.json"
SIGNALS = {"H5a_VWAP_cont": lambda g, pc: E.vwap_continuation(g), "H5b_ORB": lambda g, pc: E.orb(g)}
HO = "2024-01-01"


def main() -> None:
    if OUT.exists():
        sys.exit(f"T5 e' gia' stato eseguito ({OUT}): l'hold-out e' consumato, non si riesegue.")
    res, pvals = {}, {}
    for inst, (sym, k, usd, cost) in R.INSTR.items():
        tr = R.trades_for(sym, k, SIGNALS)
        tr = tr[tr["date"] >= HO]
        for c in SIGNALS:
            x = tr[tr["concept"] == c].set_index("date")
            traded = x["traded"]
            net = (x["gross_pts"] - cost).where(traded, 0.0)
            m = T1.metrics(net, traded, usd)
            m["periodo"] = f"{x.index.min().date()} -> {x.index.max().date()}"
            m["gross_pt_per_trade"] = float(x.loc[traded, "gross_pts"].mean())
            m["stress2x_media_pt"] = float((x["gross_pts"] - 2 * cost).where(traded, 0.0).mean())
            m["uscite"] = x.loc[traded, "reason"].value_counts(normalize=True).round(3).to_dict()
            yr = net.groupby(net.index.year).sum()
            m["pnl_pt_per_anno"] = {int(a): round(float(b), 1) for a, b in yr.items()}
            res[f"{inst}_{c}"] = m
            pvals[f"{inst}_{c}"] = m["p_unilaterale"]
    for key, p in T1.holm(pvals).items():
        m = res[key]
        m["p_holm"] = p
        m["passa_singolo"] = bool(m["t_nw"] > 2.0 and p < 0.05 and m["stress2x_media_pt"] > 0)
    for c in SIGNALS:
        both = res[f"ES_{c}"]["passa_singolo"] and res[f"NQ_{c}"]["passa_singolo"]
        for inst in R.INSTR:
            res[f"{inst}_{c}"]["SOPRAVVIVE"] = both
    cols = ["periodo", "trade", "win_rate", "payoff", "gross_pt_per_trade", "expectancy_pt_per_trade",
            "expectancy_usd_per_trade", "profit_factor", "sharpe_ann", "max_dd_usd", "t_nw", "p_holm", "stress2x_media_pt", "SOPRAVVIVE"]
    print("=== T5 HOLD-OUT (esecuzione unica) ===")
    print(pd.DataFrame(res).T.reindex(columns=cols).to_string(float_format=lambda v: f"{v:,.3f}"))
    for key, m in res.items():
        print(f"  {key}: uscite {m['uscite']} | P&L pt/anno {m['pnl_pt_per_anno']}")
    OUT.write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))
    surv = sorted({k.split('_', 1)[1] for k, m in res.items() if m["SOPRAVVIVE"]})
    print(f"\nSopravvissuti: {surv or 'NESSUNO -> T5 MORTO'}")


if __name__ == "__main__":
    main()
