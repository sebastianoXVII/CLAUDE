"""Motore del test T1 (momentum dell'ultima mezz'ora). Specifica: research/preregistration/T1_momentum_ultima_mezzora.md.
Test: research/tests/test_t1_engine.py."""
from __future__ import annotations

import numpy as np
import pandas as pd
import exchange_calendars as xc
import statsmodels.api as sm
from scipy import stats

TZ = "America/New_York"
TOL = pd.Timedelta(minutes=2)
ONE_MIN = pd.Timedelta(minutes=1)
TIMES = ("10:00", "15:00", "15:30", "16:00")
# Emendamento 2: chiusure anticipate NYSE dal calendario ufficiale (le barre after-hours le farebbero sembrare valide)
_XNYS = xc.get_calendar("XNYS", start="2005-01-01", end="2030-12-31")
EARLY_CLOSES = frozenset(pd.Timestamp(d).tz_localize(None).normalize() for d in _XNYS.early_closes)


def price_at(day_bars: pd.DataFrame, t: pd.Timestamp) -> float:
    """Prezzo al tempo t = close della barra a 1 minuto che inizia a t-1m (o l'ultima prima, entro TOL)."""
    target = t - ONE_MIN
    s = day_bars.loc[:target, "close"]
    if s.empty or target - s.index[-1] > TOL:
        return np.nan
    return float(s.iloc[-1])


def session_prices(bars: pd.DataFrame) -> pd.DataFrame:
    """Prezzi alle ore chiave per giorno feriale, usando SOLO barre della sessione regolare (inizio in 09:30-15:59 ET),
    esclusi i giorni di chiusura anticipata NYSE (emendamento 2)."""
    b = bars.copy()
    b.index = b.index.tz_convert(TZ)
    assert b.index.is_monotonic_increasing, "barre non ordinate"
    b = b.between_time("09:30", "15:59")
    rows = []
    for d, g in b.groupby(b.index.date):
        if pd.Timestamp(d).weekday() >= 5 or pd.Timestamp(d) in EARLY_CLOSES:
            continue
        p = {"p" + hhmm.replace(":", ""): price_at(g, pd.Timestamp(f"{d} {hhmm}", tz=TZ)) for hhmm in TIMES}
        rows.append({"date": pd.Timestamp(d), **p})
    return pd.DataFrame(rows).set_index("date")


def daily_points(bars: pd.DataFrame, window: int = 252, k: float = 1.0, raw: pd.DataFrame | None = None) -> pd.DataFrame:
    """Una riga per giorno valido. r1/r12 dai prezzi in `bars` (rettificati); last_pts in punti indice equivalenti
    = (P16:00 - P15:30) * k, dai prezzi `raw` (non rettificati) se forniti (emendamenti 1 e 2).
    'thr' usa solo giorni precedenti e resta NaN finche' la finestra non e' piena."""
    df = session_prices(bars)
    if raw is not None:
        r = session_prices(raw)[["p1530", "p1600"]].rename(columns={"p1530": "raw1530", "p1600": "raw1600"})
        df = df.join(r, how="inner")
    df = df.dropna()
    df["prev_close"] = df["p1600"].shift(1)
    df = df.dropna(subset=["prev_close"])
    df["r1"] = np.log(df["p1000"] / df["prev_close"])
    df["r12"] = np.log(df["p1530"] / df["p1500"])
    hi, lo = ("raw1600", "raw1530") if raw is not None else ("p1600", "p1530")
    df["last_pts"] = (df[hi] - df[lo]) * k
    df["thr"] = df["r1"].abs().shift(1).rolling(window, min_periods=window).quantile(2 / 3)
    return df


def run_variants(df: pd.DataFrame, cost: float) -> dict[str, tuple[pd.Series, pd.Series]]:
    sig_a, sig_b = np.sign(df["r1"]), np.sign(df["r1"] + df["r12"])
    big = df["r1"].abs() > df["thr"]
    out = {}
    for name, sig, filt in (("V1", sig_a, None), ("V2", sig_a, big), ("V3", sig_b, None), ("V4", sig_b, big)):
        traded = sig != 0
        if filt is not None:
            traded = traded & filt
        out[name] = ((sig * df["last_pts"] - cost).where(traded, 0.0), traded)
    out["BENCH_long"] = (df["last_pts"] - cost, pd.Series(True, index=df.index))
    return out


def nw_t(x, lags: int = 5) -> float:
    x = np.asarray(x, dtype=float)
    if len(x) < 30 or np.allclose(x, x[0]):
        return np.nan
    fit = sm.OLS(x, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return float(fit.tvalues[0])


def holm(pvals: dict[str, float]) -> dict[str, float]:
    clean = {k: (1.0 if p is None or np.isnan(p) else p) for k, p in pvals.items()}
    items = sorted(clean.items(), key=lambda kv: kv[1])
    m, adj, running = len(items), {}, 0.0
    for i, (k, p) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        adj[k] = running
    return adj


def metrics(pnl: pd.Series, traded: pd.Series, usd_per_pt: float) -> dict:
    tr = pnl[traded]
    wins, losses = tr[tr > 0], tr[tr < 0]
    usd = pnl * usd_per_pt
    eq = usd.cumsum()
    down = usd[usd < 0]
    t = nw_t(pnl.values)
    sd = usd.std()
    return {
        "giorni": int(len(pnl)),
        "trade": int(traded.sum()),
        "win_rate": float((tr > 0).mean()) if len(tr) else np.nan,
        "payoff": float(wins.mean() / -losses.mean()) if len(wins) and len(losses) else np.nan,
        "expectancy_pt_per_trade": float(tr.mean()) if len(tr) else np.nan,
        "expectancy_usd_per_trade": float(tr.mean() * usd_per_pt) if len(tr) else np.nan,
        "profit_factor": float(wins.sum() / -losses.sum()) if len(losses) else (float("inf") if len(wins) else np.nan),
        "sharpe_ann": float(usd.mean() / sd * np.sqrt(252)) if sd > 0 else np.nan,
        "sortino_ann": float(usd.mean() / np.sqrt((down**2).sum() / len(usd)) * np.sqrt(252)) if len(down) else np.nan,
        "max_dd_usd": float((eq - np.maximum(eq.cummax(), 0.0)).min()),
        "pnl_tot_usd": float(usd.sum()),
        "t_nw": t,
        "p_unilaterale": float(1 - stats.norm.cdf(t)) if not np.isnan(t) else np.nan,
    }


def verdict(m: dict, period: str) -> tuple[dict[str, bool], bool]:
    if period == "in_sample":
        pos, yrs = map(int, m["anni_positivi"].split("/"))
        checks = {
            "t>3": m["t_nw"] > 3.0,
            "stress2x>0": m["media_pt_stress2x"] > 0,
            "holm<0.05": m["p_holm"] < 0.05,
            "anni>=5/7": pos * 7 >= 5 * yrs,
            "batte_bench": m["diff_vs_bench_pt_medio"] > 0,
        }
    else:
        checks = {"t>1.5": m["t_nw"] > 1.5}
    return checks, all(bool(v) for v in checks.values())


def evaluate(spec: dict, period: str) -> dict:
    """spec: {nome: (giornaliero, $/pt pieno, $/pt micro, costo base pt, costo micro pt)} gia' filtrato sul periodo."""
    res, pvals = {}, {}
    for name, (daily, usd_full, usd_micro, c_base, c_micro) in spec.items():
        df = daily.dropna(subset=["thr"])
        base, stress2, micro = run_variants(df, c_base), run_variants(df, 2 * c_base), run_variants(df, c_micro)
        for v, (pnl, traded) in base.items():
            key = f"{name}_{v}"
            m = metrics(pnl, traded, usd_full)
            m["media_pt_stress2x"] = float(stress2[v][0].mean())
            m["media_pt_micro"] = float(micro[v][0].mean())
            m["expectancy_usd_micro"] = float(micro[v][0][traded].mean() * usd_micro) if traded.any() else np.nan
            yearly = pnl.groupby(pnl.index.year).sum()
            m["pnl_pt_per_anno"] = {int(y): round(float(x), 2) for y, x in yearly.items()}
            m["anni_positivi"] = f"{int((yearly > 0).sum())}/{len(yearly)}"
            if v != "BENCH_long":
                # emendamento 2: solo giorni operati; (segnale - 1) * last_pts, i costi si annullano
                sig_minus_bench = pnl[traded] - base["BENCH_long"][0][traded]
                m["diff_vs_bench_pt_medio"] = float(sig_minus_bench.mean()) if traded.any() else np.nan
                pvals[key] = m["p_unilaterale"]
            res[key] = m
    for k, p in holm(pvals).items():
        res[k]["p_holm"] = p
        res[k]["criteri"], res[k]["SOPRAVVIVE"] = verdict(res[k], period)
    return res


def holdout_candidates(in_sample: dict) -> list[str]:
    """Emendamento 2: l'hold-out si calcola solo per le varianti sopravvissute in-sample."""
    return [k for k, m in in_sample.items() if m.get("SOPRAVVIVE") is True]
