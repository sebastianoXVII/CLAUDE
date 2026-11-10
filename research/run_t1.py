"""Esegue T1 secondo la pre-registrazione (con emendamento 1). Hold-out solo con --holdout.

    python3 research/run_t1.py             # in-sample 2017-2023
    python3 research/run_t1.py --holdout   # + hold-out 2024-fine (solo dopo il verdetto in-sample)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import t1_engine as E  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BARS, OUT = ROOT / "data" / "bars", ROOT / "research" / "results"
# nome: (file, k, $/pt pieno, $/pt micro, costo base pt, costo micro pt) — sezione 4 + emendamento 1
INSTR = {"ES": ("SPY", 10.0, 50.0, 5.0, 0.33, 0.49), "NQ": ("QQQ", 41.0, 20.0, 2.0, 0.45, 0.85)}
PERIODS = {"in_sample": ("2017-01-01", "2023-12-31"), "holdout": ("2024-01-01", None)}
COLS = ["giorni", "trade", "win_rate", "payoff", "expectancy_pt_per_trade", "expectancy_usd_per_trade",
        "expectancy_usd_micro", "profit_factor", "sharpe_ann", "max_dd_usd", "t_nw", "p_holm",
        "media_pt_stress2x", "diff_vs_bench_pt_medio", "anni_positivi", "SOPRAVVIVE"]


def main() -> None:
    daily = {}
    for name, (sym, k, *_rest) in INSTR.items():
        bars = pd.read_parquet(BARS / f"{sym}_1m.parquet")
        daily[name] = E.daily_points(bars, window=252, k=k)
        d = daily[name]
        print(f"{name} ({sym}): {len(d)} giorni validi {d.index[0].date()} -> {d.index[-1].date()}")
    periods = ["in_sample"] + (["holdout"] if "--holdout" in sys.argv else [])
    report = {}
    for per in periods:
        s, e = PERIODS[per]
        spec = {n: (daily[n].loc[s:e] if e else daily[n].loc[s:], *INSTR[n][2:]) for n in INSTR}
        report[per] = E.evaluate(spec, per)
        print(f"\n=== {per} {s} -> {e or 'fine'} ===")
        print(pd.DataFrame(report[per]).T.reindex(columns=COLS).to_string(float_format=lambda v: f"{v:,.3f}"))
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / f"T1_{'_'.join(periods)}.json"
    f.write_text(json.dumps(report, indent=2, default=str, ensure_ascii=False))
    print(f"\nsalvato: {f}")


if __name__ == "__main__":
    main()
