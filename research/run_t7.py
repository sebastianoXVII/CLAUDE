"""Esegue T7: Noise Area su NQ (HistData NSXUSD, VWAP da profilo di volume QQQ) sul periodo mai usato inizio -> 2016-12-31.
Spec: research/preregistration/T7_noise_area_nq_conferma.md (emendamento 2). Esecuzione unica (rifiuta di ripetere).
Richiede research/results/T7_proxy_check.json con proxy valido (run_t7_proxy_check.py)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t6 as R6  # noqa: E402
import t1_engine as T1  # noqa: E402
import t6_engine as E  # noqa: E402
import vwap_proxy as V  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BARS, OUT = ROOT / "data" / "bars", ROOT / "research" / "results"
FILE = BARS / "NSXUSD_1m_24h.parquet"  # emendamento 2: HistData
TEST_END = "2016-12-31"
COST_NQ, COST_MNQ, USD_NQ = 0.45, 0.85, 20.0
PROXY_FILE = OUT / "T7_proxy_check.json"
MIN_AGREE, MIN_CORR = 0.90, 0.90


def proxy_ok(check: dict) -> bool:
    return check["accordo_giorni"] >= MIN_AGREE and check["corr_pnl_giornaliero"] >= MIN_CORR


def outcome(t_nw: float, criteri: dict) -> str:
    if all(criteri.values()):
        return "CONFERMATO"
    return "MORTO" if t_nw < 0 else "INCONCLUSIVO"


def qqq_profile() -> pd.Series:
    q = pd.read_parquet(BARS / "QQQ_1m_raw.parquet")
    q.index = q.index.tz_convert(E.TZ)
    q = q[(q.index >= pd.Timestamp("2016-01-01", tz=E.TZ)) & (q.index < pd.Timestamp("2025-01-01", tz=E.TZ))]
    return V.volume_profile(q)


def trades(cost: float, profile: pd.Series):
    raw = pd.read_parquet(FILE)
    raw.index = raw.index.tz_convert(E.TZ)
    rth = raw[~raw.index.duplicated()].sort_index().between_time("09:30", "15:59")
    rth = V.with_profile_volume(rth, profile)
    days, rows, prev_ok = {}, [], False
    for d, g in rth.groupby(rth.index.date):
        ts = pd.Timestamp(d)
        if ts.weekday() >= 5 or ts in T1.EARLY_CLOSES or len(g) < 300:
            prev_ok = False
            continue
        inp = E.day_inputs(g)
        days[ts] = (g, inp)
        rows.append({"date": ts, "open": inp["open"], "prev_valid": prev_ok,
                     **{t: inp["prices"][t] for t in E.DECISION_TIMES}, "p1600": inp["prices"]["16:00"]})
        prev_ok = True
    tab = pd.DataFrame(rows).set_index("date")
    tab = tab[tab["p1600"].notna() & tab["open"].notna()]
    tab["prev_close"] = tab["p1600"].shift(1).where(tab["prev_valid"])
    sig = E.sigma_table(tab[E.DECISION_TIMES], tab["open"])
    out, armed = [], []
    for ts, row in tab.iterrows():
        if np.isnan(row["prev_close"]) or sig.loc[ts].isna().any():
            continue
        armed.append(ts)
        ub, lb = {}, {}
        for t in E.DECISION_TIMES:
            ub[t], lb[t] = E.bounds(row["open"], row["prev_close"], sig.loc[ts, t])
        _g, inp = days[ts]
        for tr in E.simulate_day(inp["prices"], inp["vwap"], ub, lb, row["p1600"]):
            gross = tr["side"] * (tr["exit"] - tr["entry"])
            out.append({"date": ts, **tr, "gross_pts": gross, "net_pts": gross - cost,
                        "ub_entry": ub[tr["entry_time"]], "lb_entry": lb[tr["entry_time"]]})
    return pd.DataFrame(out), pd.DatetimeIndex(armed), days


def main():
    f = OUT / "T7_risultati.json"
    if f.exists():
        sys.exit("T7 gia' eseguito: non si riesegue.")
    if not FILE.exists():
        sys.exit(f"manca {FILE}: nessun verdetto scritto.")
    if not PROXY_FILE.exists() or not proxy_ok(json.loads(PROXY_FILE.read_text())):
        sys.exit("proxy VWAP non validato (emendamento 2): T7 non si esegue su HistData.")
    tr, armed, _days = trades(COST_NQ, qqq_profile())
    test_days = armed[armed <= TEST_END]
    sub = tr[tr["date"] <= TEST_END]
    m = R6.evaluate(sub, test_days, USD_NQ, COST_NQ)
    mnq = (sub["gross_pts"] - COST_MNQ).groupby(sub["date"]).sum().reindex(test_days, fill_value=0.0)
    m["media_pt_costo_MNQ"] = float(mnq.mean())
    yrs = m["pnl_pt_per_anno"]
    pos = sum(1 for v in yrs.values() if v > 0)
    m["criteri"] = {"t>3": m["t_nw"] > 3, "stress2x>0": m["stress2x_media_pt"] > 0, "MNQ>0": m["media_pt_costo_MNQ"] > 0,
                    "anni>=2/3": pos * 3 >= 2 * len(yrs)}
    m["SOPRAVVIVE"] = all(m["criteri"].values())
    m["ESITO"] = outcome(m["t_nw"], m["criteri"])
    m["periodo"] = f"{test_days.min().date()} -> {test_days.max().date()}"
    m["n_giorni"] = int(len(test_days))
    # diagnostico non decisionale: coerenza col proxy QQQ sul periodo sovrapposto 2017-2024
    try:
        qtr, _qa, _d, _n = R6.trades_for("QQQ", 41.0, COST_NQ)
        a = tr[(tr["date"] > TEST_END)].groupby("date")["net_pts"].sum()
        b = qtr[qtr["date"] <= "2024-12-31"].groupby("date")["net_pts"].sum()
        common = a.index.intersection(b.index)
        m["diagnostico_corr_giornaliera_NSXUSD_vs_QQQ"] = float(np.corrcoef(a.loc[common], b.loc[common])[0, 1]) if len(common) > 30 else None
    except Exception as e:  # noqa: BLE001
        m["diagnostico_corr_giornaliera_NSXUSD_vs_QQQ"] = f"non calcolato: {e}"
    f.write_text(json.dumps(m, indent=2, default=str, ensure_ascii=False))
    print(json.dumps({k: m[k] for k in ("periodo", "n_giorni", "n_trades", "trade_win_rate", "net_usd_per_trade", "sharpe_ann",
                                        "max_dd_usd", "t_nw", "stress2x_media_pt", "media_pt_costo_MNQ", "pnl_pt_per_anno",
                                        "criteri", "SOPRAVVIVE", "ESITO", "diagnostico_corr_giornaliera_NSXUSD_vs_QQQ")}, indent=2, default=str))


if __name__ == "__main__":
    main()
