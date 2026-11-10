"""Esegue T1 secondo la pre-registrazione (emendamenti 1 e 2).

    python3 research/run_t1.py             # passo 1: in-sample 2017-2023 -> salva il verdetto
    python3 research/run_t1.py --holdout   # passo 2: hold-out 2024-fine, SOLO per le varianti sopravvissute al passo 1
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
IS_FILE = OUT / "T1_in_sample.json"
# nome: (simbolo, k, $/pt pieno, $/pt micro, costo base pt, costo micro pt) — sezione 4 + emendamento 1
INSTR = {"ES": ("SPY", 10.0, 50.0, 5.0, 0.33, 0.49), "NQ": ("QQQ", 41.0, 20.0, 2.0, 0.45, 0.85)}
PERIODS = {"in_sample": ("2017-01-01", "2023-12-31"), "holdout": ("2024-01-01", None)}
COLS = ["giorni", "trade", "win_rate", "payoff", "expectancy_pt_per_trade", "expectancy_usd_per_trade",
        "expectancy_usd_micro", "profit_factor", "sharpe_ann", "sortino_ann", "max_dd_usd", "t_nw",
        "p_unilaterale", "p_holm", "media_pt_stress2x", "diff_vs_bench_pt_medio", "anni_positivi", "SOPRAVVIVE"]


def load_daily() -> dict[str, pd.DataFrame]:
    daily = {}
    for name, (sym, k, *_r) in INSTR.items():
        adj = pd.read_parquet(BARS / f"{sym}_1m.parquet")
        raw = pd.read_parquet(BARS / f"{sym}_1m_raw.parquet")
        d = E.daily_points(adj, window=252, k=k, raw=raw)
        daily[name] = d
        per_year = d.groupby(d.index.year).size().to_dict()
        print(f"{name} ({sym}): {len(d)} giorni validi {d.index[0].date()} -> {d.index[-1].date()} | per anno: {per_year}")
    return daily


def spec_for(daily: dict, period: str) -> dict:
    s, e = PERIODS[period]
    return {n: (daily[n].loc[s:e] if e else daily[n].loc[s:], *INSTR[n][2:]) for n in INSTR}


def show(title: str, res: dict) -> None:
    print(f"\n=== {title} ===")
    print(pd.DataFrame(res).T.reindex(columns=COLS).to_string(float_format=lambda v: f"{v:,.3f}"))
    for k, m in res.items():
        if "pnl_pt_per_anno" in m:
            print(f"  {k} P&L pt per anno: {m['pnl_pt_per_anno']}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if "--holdout" not in sys.argv:
        res = E.evaluate(spec_for(load_daily(), "in_sample"), "in_sample")
        show("IN-SAMPLE 2017-2023 (costi base)", res)
        IS_FILE.write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))
        surv = E.holdout_candidates(res)
        print(f"\nSopravvissute in-sample: {surv or 'NESSUNA -> T1 MORTO'}\nsalvato: {IS_FILE}")
        return
    if not IS_FILE.exists():
        sys.exit("Hold-out rifiutato: manca il verdetto in-sample. Eseguire prima senza --holdout.")
    surv = E.holdout_candidates(json.loads(IS_FILE.read_text()))
    if not surv:
        sys.exit("T1 MORTO: nessuna variante e' sopravvissuta in-sample. Hold-out NON calcolato (emendamento 2).")
    res = E.evaluate(spec_for(load_daily(), "holdout"), "holdout")
    res = {k: res[k] for k in surv}  # si mostrano solo le sopravvissute
    show("HOLD-OUT 2024-fine (solo sopravvissute in-sample)", res)
    final = {k: bool(res[k]["SOPRAVVIVE"]) for k in surv}
    print(f"\nVERDETTO FINALE (6a E 6b): {final}")
    (OUT / "T1_holdout.json").write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
