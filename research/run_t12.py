"""T12: Noise Area (codice congelato T6) su GLD, IWM, DIA. Spec: research/preregistration/T12_noise_area_altri_mercati.md"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t6 as R6  # noqa: E402
import t1_engine as T1  # noqa: E402

OUT = R6.OUT / "T12_risultati.json"
INSTR = {"GLD": 1.0, "IWM": 1.6, "DIA": 0.8}  # costo base in bp
COST_QQQ_BP = 0.25  # solo per la correlazione: 0,45 pt NQ su circa 18.000 pt
PERIODS = {"info_2017_2024": ("2017-01-01", "2024-12-31"), "OOS_2025": ("2025-01-02", "2026-12-31")}


def to_returns(tr: pd.DataFrame, cost_bp: float) -> pd.DataFrame:
    tr = tr.copy()
    tr["gross_ret"] = tr["side"] * (tr["exit"] / tr["entry"] - 1)
    tr["net_ret"] = tr["gross_ret"] - cost_bp / 1e4
    return tr


def daily_returns(sym: str, cost_bp: float):
    tr, armed, _d, _n = R6.trades_for(sym, 1.0, 0.0)
    return to_returns(tr, cost_bp), armed


def evaluate(tr, armed, s, e, cost_bp):
    v = armed[(armed >= s) & (armed <= e)]
    sub = tr[(tr["date"] >= s) & (tr["date"] <= e)]
    daily = sub.groupby("date")["net_ret"].sum().reindex(v, fill_value=0.0)
    m = T1.metrics(daily * 1e4, daily.index.isin(sub["date"]), 1.0)  # in bp
    m["n_trades"] = int(len(sub))
    m["netto_bp_per_trade"] = float(sub["net_ret"].mean() * 1e4) if len(sub) else np.nan
    m["stress2x_media_bp"] = float((sub["gross_ret"] - 2 * cost_bp / 1e4).groupby(sub["date"]).sum().reindex(v, fill_value=0.0).mean() * 1e4)
    yr = daily.groupby(daily.index.year).sum() * 1e4
    m["bp_per_anno"] = {int(a): round(float(b), 0) for a, b in yr.items()}
    return m, daily


def main():
    if OUT.exists():
        sys.exit("T12 gia' eseguito.")
    res, pv, dailies = {}, {}, {}
    qtr, qarmed = daily_returns("QQQ", COST_QQQ_BP)
    for sym, c in INSTR.items():
        tr, armed = daily_returns(sym, c)
        for per, (s, e) in PERIODS.items():
            m, d = evaluate(tr, armed, s, e, c)
            res[f"{per}|{sym}"] = m
            dailies[(per, sym)] = d
        pv[sym] = res[f"OOS_2025|{sym}"]["p_unilaterale"]
    for per, (s, e) in PERIODS.items():
        _, dq = evaluate(qtr, qarmed, s, e, COST_QQQ_BP)
        dailies[(per, "QQQ")] = dq
    for sym, p in T1.holm(pv).items():
        m = res[f"OOS_2025|{sym}"]
        m["p_holm"] = p
        m["CONFERMA"] = bool(m["t_nw"] > 1.65 and p < 0.05 and m["stress2x_media_bp"] > 0)
    corr = {}
    for per in PERIODS:
        df = pd.DataFrame({k: dailies[(per, k)] for k in ("QQQ", *INSTR)}).dropna()
        corr[per] = df.corr().round(2).to_dict()
    out = {"risultati": res, "correlazioni_rendimenti_giornalieri": corr}
    OUT.write_text(json.dumps(out, indent=2, default=str, ensure_ascii=False))
    cols = ["n_trades", "trade", "win_rate", "netto_bp_per_trade", "sharpe_ann", "t_nw", "p_holm", "stress2x_media_bp", "CONFERMA"]
    print(pd.DataFrame(res).T.reindex(columns=cols).to_string(float_format=lambda v: f"{v:,.2f}"))
    for k, m in res.items():
        print(f"  {k}: bp per anno {m['bp_per_anno']}")
    for per, c in corr.items():
        print(f"\ncorrelazioni {per}:\n{pd.DataFrame(c)}")


if __name__ == "__main__":
    main()
