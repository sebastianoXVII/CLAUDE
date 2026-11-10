"""T7 emendamenti 2-3: validazione del VWAP da profilo di volume su QQQ 2017-2024 (periodo gia' visto in T6).
Scrive research/results/T7_proxy_check.json. Esecuzione unica."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t6 as R6  # noqa: E402
import run_t7 as R7  # noqa: E402
import vwap_proxy as V  # noqa: E402


def compare(true_tr: pd.DataFrame, prox_tr: pd.DataFrame, armed: pd.DatetimeIndex, s: str, e: str) -> dict:
    days = armed[(armed >= s) & (armed <= e)]
    a, b = true_tr[true_tr["date"].isin(days)], prox_tr[prox_tr["date"].isin(days)]
    da = a.groupby("date")["net_pts"].sum().reindex(days, fill_value=0.0)
    db = b.groupby("date")["net_pts"].sum().reindex(days, fill_value=0.0)
    traded = days[days.isin(a["date"]) | days.isin(b["date"])]
    return {"periodo": f"{days.min().date()} -> {days.max().date()}", "n_giorni": int(len(days)),
            "accordo_giorni": float(V.agreement(a, b, days)), "corr_pnl_giornaliero": float(np.corrcoef(da, db)[0, 1]),
            "accordo_solo_giorni_con_trade": float(V.agreement(a, b, traded)), "n_giorni_con_trade": int(len(traded)),
            "n_trade_vero": int(len(a)), "n_trade_proxy": int(len(b))}


def main():
    if R7.PROXY_FILE.exists():
        sys.exit("validazione del proxy gia' eseguita.")
    prof = R7.qqq_profile()
    a, armed_a, _d, _n = R6.trades_for("QQQ", 41.0, R7.COST_NQ)
    b, armed_b, _d, _n = R6.trades_for("QQQ", 41.0, R7.COST_NQ, volume_fn=lambda x: V.with_profile_volume(x, prof))
    assert armed_a.equals(armed_b), "i giorni operativi non dipendono dal volume"
    res = compare(a, b, armed_a, "2017-01-01", "2024-12-31")
    res["soglie"] = {"accordo_giorni": R7.MIN_AGREE, "corr_pnl_giornaliero": R7.MIN_CORR}
    res["hash_profilo"] = R7.profile_hash(prof)
    res["PROXY_VALIDO"] = R7.proxy_ok(res)
    # diagnostico non vincolante (emendamento 3): profilo 2021-2024 applicato al 2017-2019
    prof_oot = R7.qqq_profile("2021-01-01", "2025-01-01")
    c, _ac, _d, _n = R6.trades_for("QQQ", 41.0, R7.COST_NQ, volume_fn=lambda x: V.with_profile_volume(x, prof_oot))
    res["diagnostico_fuori_tempo_profilo_2021_2024_su_2017_2019"] = compare(a, c, armed_a, "2017-01-01", "2019-12-31")
    R7.PROXY_FILE.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
