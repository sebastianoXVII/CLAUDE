"""Monte Carlo della challenge Topstep 50K per il candidato Noise Area su NQ (proxy QQQ), dimensionato in MNQ.
NON e' un risultato di edge: e' un'analisi di fattibilita' condizionata al candidato (vedi T6_verdetto.md)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t6 as R6  # noqa: E402
from lab import prop_sim as P  # noqa: E402

K, MNQ_USD, MNQ_COST = 41.0, 2.0, 0.85  # punti NQ per punto QQQ, $ per punto MNQ, costo round trip MNQ in punti


def daily_pool() -> pd.DataFrame:
    tr, armed, days, _ = R6.trades_for("QQQ", K, MNQ_COST)
    rows = []
    for d in armed:
        t = tr[tr["date"] == d]
        g = days[d][0]
        closed, worst = 0.0, 0.0
        for _, x in t.iterrows():
            t0 = pd.Timestamp(f"{d.date()} {x['entry_time']}", tz=R6.E.TZ)
            t1 = pd.Timestamp(f"{d.date()} {x['exit_time']}", tz=R6.E.TZ)
            path = g.loc[t0:t1 - pd.Timedelta(minutes=1)]
            adverse = path["low"].min() if x["side"] == 1 else path["high"].max()
            mtm_worst = x["side"] * (adverse - x["entry"]) * K if len(path) else 0.0
            worst = min(worst, closed + min(mtm_worst, 0.0) - MNQ_COST)
            closed += x["net_pts"]
            worst = min(worst, closed)
        rows.append({"date": d, "pnl_pts": closed, "intra_min_pts": worst})
    return pd.DataFrame(rows).set_index("date")


def main() -> None:
    pool = daily_pool()
    pool.to_parquet(R6.ROOT / "data" / "nq_noise_area_daily_pool.parquet")
    out = {}
    scen = {
        "storico_2017_2026": pool,
        "aspettativa_dimezzata": pool.assign(pnl_pts=pool["pnl_pts"] - 0.5 * pool["pnl_pts"].mean()),
        "solo_OOS_2025_2026": pool.loc["2025-01-02":],
    }
    rules = P.Rules()
    for name, df in scen.items():
        base = list(zip(df["pnl_pts"] * MNQ_USD, df["intra_min_pts"] * MNQ_USD))
        mean_day = float(np.mean([p for p, _ in base]))
        print(f"\n=== {name}: {len(base)} giorni, P&L medio/giorno per 1 MNQ = {mean_day:,.2f} $ ===")
        for n in (1, 2, 3, 4, 5, 6, 8, 10):
            r = P.monte_carlo(P.scale(base, n), rules, n_sims=4000, max_days=120, block=5, seed=7)
            out[f"{name}|{n}MNQ"] = r
            print(f"  {n:>2} MNQ: passa {r['p_pass']:.1%}  brucia {r['p_fail']:.1%}  aperto dopo 120 gg {r['p_open']:.1%}"
                  f"  | giorni mediani per passare {r['median_days_pass']:.0f}")
    (R6.OUT / "prop_mc_noise_area_nq.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
