"""Diagnostico NON decisionale: sensibilita' della Noise Area su QQQ->NQ (2017-2026, dati gia' visti) a lookback e frequenza.
NON modifica t6_engine.py (codice congelato del forward test): i parametri si cambiano solo in memoria in questo processo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t6 as R6  # noqa: E402
import t6_engine as E  # noqa: E402

GRID_LB = (7, 10, 14, 20, 30)
GRID_FREQ = (15, 30, 60)


def times(freq: int) -> list[str]:
    out, m = [], 10 * 60
    while m <= 15 * 60 + 30:
        out.append(f"{m // 60:02d}:{m % 60:02d}")
        m += freq
    return out


def main():
    res = {}
    for f in GRID_FREQ:
        for lb in GRID_LB:
            E.LOOKBACK, E.DECISION_TIMES = lb, times(f)
            tr, armed, _d, _n = R6.trades_for("QQQ", 41.0, 0.85)
            for per, (s, e) in {"2017-2024": ("2017-01-01", "2024-12-31"), "2025-2026": ("2025-01-02", "2026-12-31")}.items():
                v = armed[(armed >= s) & (armed <= e)]
                sub = tr[(tr["date"] >= s) & (tr["date"] <= e)]
                m = R6.evaluate(sub, v, 2.0, 0.85)  # per 1 MNQ
                res[f"f{f}_lb{lb}|{per}"] = {"sharpe": round(m["sharpe_ann"], 2), "t": round(m["t_nw"], 2),
                                             "trade": m["n_trades"], "usd_trade_MNQ": round(m["net_usd_per_trade"], 1)}
            print(f"freq {f:>2} min, lookback {lb:>2} gg: " + " | ".join(
                f"{p}: Sharpe {res[f'f{f}_lb{lb}|{p}']['sharpe']:+.2f} t {res[f'f{f}_lb{lb}|{p}']['t']:+.2f} ({res[f'f{f}_lb{lb}|{p}']['trade']} trade)"
                for p in ("2017-2024", "2025-2026")), flush=True)
    (R6.OUT / "sensitivity_noise_area_nq.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
