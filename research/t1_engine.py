"""Motore del test T1 (momentum dell'ultima mezz'ora). Specifica: research/preregistration/T1_momentum_ultima_mezzora.md.
Test: research/tests/test_t1_engine.py."""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

TZ = "America/New_York"
TOL = pd.Timedelta(minutes=2)
ONE_MIN = pd.Timedelta(minutes=1)
TIMES = ("10:00", "15:00", "15:30", "16:00")


def price_at(day_bars: pd.DataFrame, t: pd.Timestamp) -> float:
    """Prezzo al tempo t = close della barra a 1 minuto che inizia a t-1m (o l'ultima prima, entro TOL)."""
    target = t - ONE_MIN
    s = day_bars.loc[:target, "close"]
    if s.empty or target - s.index[-1] > TOL:
        return np.nan
    return float(s.iloc[-1])


def daily_points(bars: pd.DataFrame, window: int = 252) -> pd.DataFrame:
    """Da barre a 1 minuto (indice UTC) a una riga per giorno valido. 'thr' usa solo giorni precedenti;
    resta NaN finche' la finestra non e' piena (le righe si scartano in fase di valutazione)."""
    b = bars.copy()
    b.index = b.index.tz_convert(TZ)
    rows = []
    for d, g in b.groupby(b.index.date):
        if pd.Timestamp(d).weekday() >= 5:
            continue
        p = {k: price_at(g, pd.Timestamp(f"{d} {k}", tz=TZ)) for k in TIMES}
        rows.append({"date": pd.Timestamp(d), **{"p" + k.replace(":", ""): v for k, v in p.items()}})
    df = pd.DataFrame(rows).set_index("date").dropna()
    df["prev_close"] = df["p1600"].shift(1)
    df = df.dropna(subset=["prev_close"])
    df["r1"] = np.log(df["p1000"] / df["prev_close"])
    df["r12"] = np.log(df["p1530"] / df["p1500"])
    df["last_pts"] = df["p1600"] - df["p1530"]
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
    items = sorted(pvals.items(), key=lambda kv: kv[1])
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
        "profit_factor": float(wins.sum() / -losses.sum()) if len(losses) else np.nan,
        "sharpe_ann": float(usd.mean() / sd * np.sqrt(252)) if sd > 0 else np.nan,
        "sortino_ann": float(usd.mean() / np.sqrt((down**2).sum() / len(usd)) * np.sqrt(252)) if len(down) else np.nan,
        "max_dd_usd": float((eq - eq.cummax()).min()),
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
            "anni>=5/7": pos >= 5,
            "batte_bench": m["diff_vs_bench_pt_medio"] > 0,
        }
    else:
        checks = {"t>1.5": m["t_nw"] > 1.5}
    return checks, all(bool(v) for v in checks.values())
