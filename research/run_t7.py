"""Esegue T7: Noise Area su NQ (HistData NSXUSD, VWAP da profilo di volume QQQ) sul periodo mai usato inizio -> 2016-12-31.
Spec: research/preregistration/T7_noise_area_nq_conferma.md (emendamento 2). Esecuzione unica (rifiuta di ripetere).
Richiede research/results/T7_proxy_check.json con proxy valido (run_t7_proxy_check.py)."""
from __future__ import annotations

import hashlib
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


NYSE_SESSIONS = frozenset(pd.Timestamp(d).tz_localize(None).normalize() for d in T1._XNYS.sessions)
MIN_YEAR_DAYS = 60


def proxy_ok(check: dict, profile_hash: str | None = None) -> bool:
    ok = check["accordo_giorni"] >= MIN_AGREE and check["corr_pnl_giornaliero"] >= MIN_CORR
    return ok and (profile_hash is None or check.get("hash_profilo") == profile_hash)


def profile_hash(profile: pd.Series) -> str:
    return hashlib.sha256(profile.sort_index().to_json().encode()).hexdigest()[:16]


def year_sums(daily: pd.Series) -> dict:
    """Emendamento 3: anni con meno di MIN_YEAR_DAYS giorni accorpati all'anno successivo; somme non arrotondate."""
    n = daily.groupby(daily.index.year).size()
    yr = pd.Series(daily.index.year, index=daily.index)
    for y in sorted(n.index):
        if n[y] < MIN_YEAR_DAYS and y + 1 in n.index:
            yr[yr == y] = y + 1
    return {int(a): float(b) for a, b in daily.groupby(yr.to_numpy()).sum().items()}


def outcome(t_nw: float, criteri: dict) -> str:
    if all(criteri.values()):
        return "CONFERMATO"
    return "MORTO" if t_nw < 0 else "INCONCLUSIVO"


def qqq_profile(start: str = "2016-01-01", end: str = "2025-01-01") -> pd.Series:
    """Mediana del volume QQQ per minuto, barre con start <= t < end (ET)."""
    q = pd.read_parquet(BARS / "QQQ_1m_raw.parquet")
    q.index = q.index.tz_convert(E.TZ)
    q = q[(q.index >= pd.Timestamp(start, tz=E.TZ)) & (q.index < pd.Timestamp(end, tz=E.TZ))]
    return V.volume_profile(q)


def trades(cost: float, profile: pd.Series):
    raw = pd.read_parquet(FILE)
    raw.index = raw.index.tz_convert(E.TZ)
    rth = raw[~raw.index.duplicated()].sort_index().between_time("09:30", "15:59")
    rth = V.with_profile_volume(rth, profile)
    days, rows, prev_ok = {}, [], False
    for d, g in rth.groupby(rth.index.date):
        ts = pd.Timestamp(d)
        if ts not in NYSE_SESSIONS:  # emendamento 3: festivi saltati senza rompere la catena del close
            continue
        if ts in T1.EARLY_CLOSES or len(g) < 300:
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
    prof = qqq_profile()
    if not PROXY_FILE.exists() or not proxy_ok(json.loads(PROXY_FILE.read_text()), profile_hash(prof)):
        sys.exit("proxy VWAP non validato o profilo diverso (emendamenti 2-3): T7 non si esegue su HistData.")
    tr, armed, _days = trades(COST_NQ, prof)
    if tr.empty:
        sys.exit("nessun trade generato: controllare i dati, nessun verdetto scritto.")
    test_days = armed[armed <= TEST_END]
    sub = tr[tr["date"] <= TEST_END]
    m = R6.evaluate(sub, test_days, USD_NQ, COST_NQ)
    mnq = (sub["gross_pts"] - COST_MNQ).groupby(sub["date"]).sum().reindex(test_days, fill_value=0.0)
    m["media_pt_costo_MNQ"] = float(mnq.mean())
    daily = sub.groupby("date")["net_pts"].sum().reindex(test_days, fill_value=0.0)
    yrs = year_sums(daily)
    m["pnl_pt_per_anno_accorpati"] = {a: round(b, 1) for a, b in yrs.items()}
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
        common = armed[armed > TEST_END].intersection(_qa[_qa <= "2024-12-31"])
        a = tr.groupby("date")["net_pts"].sum().reindex(common, fill_value=0.0)
        b = qtr.groupby("date")["net_pts"].sum().reindex(common, fill_value=0.0)
        m["diagnostico_corr_giornaliera_NSXUSD_vs_QQQ"] = float(np.corrcoef(a.loc[common], b.loc[common])[0, 1]) if len(common) > 30 else None
    except Exception as e:  # noqa: BLE001
        m["diagnostico_corr_giornaliera_NSXUSD_vs_QQQ"] = f"non calcolato: {e}"
    sub.to_parquet(OUT / "T7_trades.parquet")
    f.write_text(json.dumps(m, indent=2, default=str, ensure_ascii=False))
    print(json.dumps({k: m[k] for k in ("periodo", "n_giorni", "n_trades", "trade_win_rate", "net_usd_per_trade", "sharpe_ann",
                                        "max_dd_usd", "t_nw", "stress2x_media_pt", "media_pt_costo_MNQ", "pnl_pt_per_anno", "pnl_pt_per_anno_accorpati",
                                        "criteri", "SOPRAVVIVE", "ESITO", "diagnostico_corr_giornaliera_NSXUSD_vs_QQQ")}, indent=2, default=str))


if __name__ == "__main__":
    main()
