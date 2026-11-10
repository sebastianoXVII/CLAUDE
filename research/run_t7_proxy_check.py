"""T7 emendamento 2: validazione del VWAP da profilo di volume su QQQ 2017-2024 (periodo gia' visto in T6).
Scrive research/results/T7_proxy_check.json. Esecuzione unica."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t6 as R6  # noqa: E402
import run_t7 as R7  # noqa: E402
import vwap_proxy as V  # noqa: E402

S, E_ = "2017-01-01", "2024-12-31"


def main():
    if R7.PROXY_FILE.exists():
        sys.exit("validazione del proxy gia' eseguita.")
    prof = R7.qqq_profile()
    a, armed_a, _d, _n = R6.trades_for("QQQ", 41.0, R7.COST_NQ)
    b, armed_b, _d, _n = R6.trades_for("QQQ", 41.0, R7.COST_NQ, volume_fn=lambda x: V.with_profile_volume(x, prof))
    assert armed_a.equals(armed_b), "i giorni operativi non dipendono dal volume"
    days = armed_a[(armed_a >= S) & (armed_a <= E_)]
    a, b = a[a["date"].isin(days)], b[b["date"].isin(days)]
    da = a.groupby("date")["net_pts"].sum().reindex(days, fill_value=0.0)
    db = b.groupby("date")["net_pts"].sum().reindex(days, fill_value=0.0)
    res = {"periodo": f"{days.min().date()} -> {days.max().date()}", "n_giorni": int(len(days)),
           "accordo_giorni": float(V.agreement(a, b, days)), "corr_pnl_giornaliero": float(np.corrcoef(da, db)[0, 1]),
           "n_trade_vero": int(len(a)), "n_trade_proxy": int(len(b)),
           "soglie": {"accordo_giorni": R7.MIN_AGREE, "corr_pnl_giornaliero": R7.MIN_CORR}}
    res["PROXY_VALIDO"] = R7.proxy_ok(res)
    R7.PROXY_FILE.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
