"""T1 — momentum dell'ultima mezz'ora. Implementa ESATTAMENTE research/preregistration/T1_momentum_ultima_mezzora.md.

Uso:
    python3 research/tests/t1_intraday_momentum.py            # solo in-sample 2017-2023
    python3 research/tests/t1_intraday_momentum.py --holdout  # anche hold-out 2024+ (solo dopo il verdetto 6a)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
BARS = ROOT / "data" / "bars"
OUT = ROOT / "research" / "results"
TZ = "America/New_York"

INSTR = {
    # simbolo: (nome, $/punto pieno, $/punto micro, costo base pt, costo micro pt)
    "USA500IDXUSD": ("ES", 50.0, 5.0, 0.33, 0.49),
    "USATECHIDXUSD": ("NQ", 20.0, 2.0, 0.45, 0.85),
}
IS_START, IS_END, HO_START = "2017-01-01", "2023-12-31", "2024-01-01"
TOL = pd.Timedelta(minutes=2)


def price_at(day_bars: pd.DataFrame, t: pd.Timestamp) -> float:
    """Close dell'ultima barra con timestamp <= t, se entro TOL; altrimenti NaN.
    Una barra a 1 minuto con timestamp t copre [t, t+1m): per avere il prezzo AL tempo t
    si usa la barra che inizia a t-1m (il suo close e' il prezzo a t)."""
    s = day_bars.loc[: t - pd.Timedelta(minutes=1), "close"]
    if s.empty or (t - pd.Timedelta(minutes=1)) - s.index[-1] > TOL:
        return np.nan
    return float(s.iloc[-1])


def daily_points(sym: str) -> pd.DataFrame:
    bars = pd.read_parquet(BARS / f"{sym}_1m.parquet")
    bars.index = bars.index.tz_convert(TZ)
    rows = []
    for day, g in bars.groupby(bars.index.date):
        if pd.Timestamp(day).weekday() >= 5:
            continue
        ts = {k: pd.Timestamp(f"{day} {k}", tz=TZ) for k in ("10:00", "15:00", "15:30", "16:00")}
        p = {k: price_at(g, v) for k, v in ts.items()}
        rows.append({"date": pd.Timestamp(day), **{f"p{k.replace(':', '')}": v for k, v in p.items()}})
    df = pd.DataFrame(rows).set_index("date").dropna()
    df["prev_close"] = df["p1600"].shift(1)
    df = df.dropna()
    df["r1"] = np.log(df["p1000"] / df["prev_close"])
    df["r12"] = np.log(df["p1530"] / df["p1500"])
    df["last_pts"] = df["p1600"] - df["p1530"]  # movimento in punti dell'ultima mezz'ora
    # soglia terzile superiore di |r1| sui 252 giorni validi PRECEDENTI
    df["thr"] = df["r1"].abs().shift(1).rolling(252, min_periods=252).quantile(2 / 3)
    return df.dropna(subset=["thr"])


def nw_t(x: np.ndarray, lags: int = 5) -> float:
    if len(x) < 30 or np.allclose(x, x[0]):
        return np.nan
    m = sm.OLS(x, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return float(m.tvalues[0])


def metrics(pnl_pts: pd.Series, traded: pd.Series, usd_per_pt: float) -> dict:
    """pnl_pts: P&L netto giornaliero in punti (0 nei giorni senza trade)."""
    x = pnl_pts.values
    tr = pnl_pts[traded]
    wins, losses = tr[tr > 0], tr[tr < 0]
    usd = pnl_pts * usd_per_pt
    eq = usd.cumsum()
    downside = usd[usd < 0]
    t = nw_t(x)
    return {
        "giorni": int(len(x)),
        "trade": int(traded.sum()),
        "win_rate": float((tr > 0).mean()) if len(tr) else np.nan,
        "payoff": float(wins.mean() / -losses.mean()) if len(wins) and len(losses) else np.nan,
        "expectancy_pt_per_trade": float(tr.mean()) if len(tr) else np.nan,
        "expectancy_usd_per_trade": float(tr.mean() * usd_per_pt) if len(tr) else np.nan,
        "profit_factor": float(wins.sum() / -losses.sum()) if len(losses) else np.nan,
        "sharpe_ann": float(usd.mean() / usd.std() * np.sqrt(252)) if usd.std() > 0 else np.nan,
        "sortino_ann": float(usd.mean() / np.sqrt((downside**2).sum() / len(usd)) * np.sqrt(252)) if len(downside) else np.nan,
        "max_dd_usd": float((eq - eq.cummax()).min()),
        "pnl_tot_usd": float(usd.sum()),
        "t_nw": t,
        "p_unilaterale": float(1 - stats.norm.cdf(t)) if not np.isnan(t) else np.nan,
    }


def run_variants(df: pd.DataFrame, cost: float) -> dict[str, tuple[pd.Series, pd.Series]]:
    sig_a = np.sign(df["r1"])
    sig_b = np.sign(df["r1"] + df["r12"])
    big = df["r1"].abs() > df["thr"]
    out = {}
    for name, sig, filt in (("V1", sig_a, None), ("V2", sig_a, big), ("V3", sig_b, None), ("V4", sig_b, big)):
        traded = sig != 0
        if filt is not None:
            traded &= filt
        pnl = (sig * df["last_pts"] - cost).where(traded, 0.0)
        out[name] = (pnl, traded)
    bench = pd.Series(True, index=df.index)
    out["BENCH_long"] = (df["last_pts"] - cost, bench)
    return out


def holm(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m, adj, running = len(items), {}, 0.0
    for i, (k, p) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        adj[k] = running
    return adj


def evaluate(period: str, start: str, end: str | None) -> dict:
    res, pvals = {}, {}
    for sym, (name, usd_full, usd_micro, c_base, c_micro) in INSTR.items():
        df_all = daily_points(sym)
        df = df_all.loc[start:end] if end else df_all.loc[start:]
        base = run_variants(df, c_base)
        stress2 = run_variants(df, 2 * c_base)
        micro = run_variants(df, c_micro)
        for v, (pnl, traded) in base.items():
            key = f"{name}_{v}"
            m = metrics(pnl, traded, usd_full)
            m["media_pt_stress2x"] = float(stress2[v][0].mean())
            m["media_pt_micro"] = float(micro[v][0].mean())
            m["expectancy_usd_micro"] = float(micro[v][0][traded].mean() * usd_micro)
            yearly = pnl.groupby(pnl.index.year).sum()
            m["pnl_pt_per_anno"] = {int(k): round(float(x), 2) for k, x in yearly.items()}
            m["anni_positivi"] = f"{int((yearly > 0).sum())}/{len(yearly)}"
            if v != "BENCH_long":
                diff = pnl - base["BENCH_long"][0]
                m["diff_vs_bench_pt_medio"] = float(diff.mean())
                pvals[key] = m["p_unilaterale"]
            res[key] = m
    for k, p in holm(pvals).items():
        res[k]["p_holm"] = p
    # verdetto secondo la pre-registrazione
    for k in pvals:
        m = res[k]
        n_pos, n_yrs = map(int, m["anni_positivi"].split("/"))
        if period == "in_sample":
            checks = {
                "t>3": m["t_nw"] > 3.0,
                "stress2x>0": m["media_pt_stress2x"] > 0,
                "holm<0.05": m["p_holm"] < 0.05,
                "anni>=5/7": n_pos >= 5,
                "batte_bench": m["diff_vs_bench_pt_medio"] > 0,
            }
        else:
            checks = {"media>0": m["t_nw"] > 0, "t>1.5": m["t_nw"] > 1.5}
        m["criteri"] = checks
        m["SOPRAVVIVE"] = all(checks.values())
    return res


def fmt(res: dict) -> str:
    cols = ["giorni", "trade", "win_rate", "payoff", "expectancy_pt_per_trade", "expectancy_usd_per_trade",
            "expectancy_usd_micro", "profit_factor", "sharpe_ann", "max_dd_usd", "t_nw", "p_holm", "anni_positivi", "SOPRAVVIVE"]
    t = pd.DataFrame(res).T.reindex(columns=cols)
    return t.to_string(float_format=lambda v: f"{v:,.3f}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"in_sample": evaluate("in_sample", IS_START, IS_END)}
    print("=== IN-SAMPLE 2017-2023 (costi base) ===")
    print(fmt(report["in_sample"]))
    if "--holdout" in sys.argv:
        report["holdout"] = evaluate("holdout", HO_START, None)
        print("\n=== HOLD-OUT 2024-fine ===")
        print(fmt(report["holdout"]))
    name = "T1_risultati" + ("_con_holdout" if "--holdout" in sys.argv else "_in_sample") + ".json"
    (OUT / name).write_text(json.dumps(report, indent=2, default=float, ensure_ascii=False))
    print(f"\nsalvato: {OUT / name}")


if __name__ == "__main__":
    main()
