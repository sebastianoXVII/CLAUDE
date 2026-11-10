"""Motore del test T2 (reazione ai livelli di stop). Specifica: research/preregistration/T2_livelli_di_stop.md.
Test: research/tests/test_t2_engine.py."""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

from t1_engine import EARLY_CLOSES, price_at

TZ = "America/New_York"
ONE_MIN = pd.Timedelta(minutes=1)
PLACEBO_F = 0.3


def _valid_day(d) -> bool:
    ts = pd.Timestamp(d)
    return ts.weekday() < 5 and ts not in EARLY_CLOSES


def day_levels(bars: pd.DataFrame) -> pd.DataFrame:
    """Per giorno valido: massimo/minimo RTH del giorno valido precedente e massimo/minimo pre-market 04:00-09:29."""
    b = bars.copy()
    b.index = b.index.tz_convert(TZ)
    rows = []
    for d, g in b.groupby(b.index.date):
        if not _valid_day(d):
            continue
        rth = g.between_time("09:30", "15:59")
        pm = g.between_time("04:00", "09:29")
        if rth.empty:
            continue
        rows.append({"date": pd.Timestamp(d), "rth_high": rth["high"].max(), "rth_low": rth["low"].min(),
                     "pm_high": pm["high"].max() if len(pm) else np.nan,
                     "pm_low": pm["low"].min() if len(pm) else np.nan})
    df = pd.DataFrame(rows).set_index("date")
    df["pd_high"] = df["rth_high"].shift(1)
    df["pd_low"] = df["rth_low"].shift(1)
    df["prev_range"] = df["pd_high"] - df["pd_low"]
    return df[["pd_high", "pd_low", "pm_high", "pm_low", "prev_range"]]


def candidate_levels(row: pd.Series, family: str) -> list[tuple[str, int, float]]:
    """(tipo, direzione, livello): 1 vero + 2 placebo a +-0,3 x range precedente, per lato."""
    up, dn = (row["pd_high"], row["pd_low"]) if family == "PD" else (row["pm_high"], row["pm_low"])
    off = PLACEBO_F * row["prev_range"]
    out = []
    for s, lvl in ((1, up), (-1, dn)):
        out += [("true", s, float(lvl)), ("placebo", s, float(lvl + off)), ("placebo", s, float(lvl - off))]
    return out


def admitted(day_bars: pd.DataFrame, level: float, s: int) -> bool:
    """Il prezzo a 09:35 deve stare dalla parte giusta: sotto i livelli superiori, sopra quelli inferiori."""
    d = day_bars.index[0].date()
    p = price_at(day_bars, pd.Timestamp(f"{d} 09:35", tz=TZ))
    return bool(not np.isnan(p) and s * (level - p) > 0)


def first_cross(day_bars: pd.DataFrame, level: float, s: int, H: int, k: float) -> dict | None:
    """Primo attraversamento nella finestra [09:35, 15:59-H]. Ingresso = close della barra; esito y in punti indice."""
    d = day_bars.index[0].date()
    t0 = pd.Timestamp(f"{d} 09:35", tz=TZ)
    t1 = pd.Timestamp(f"{d} 15:59", tz=TZ) - pd.Timedelta(minutes=H)
    w = day_bars.loc[t0:t1]
    hit = w["high"] >= level if s == 1 else w["low"] <= level
    if not hit.any():
        return None
    tau = hit.idxmax()
    p_in = float(day_bars.loc[tau, "close"].iloc[-1] if isinstance(day_bars.loc[tau, "close"], pd.Series) else day_bars.loc[tau, "close"])
    p_out = price_at(day_bars, tau + ONE_MIN + pd.Timedelta(minutes=H))
    if np.isnan(p_out):
        return None
    after = day_bars.loc[tau + ONE_MIN: tau + pd.Timedelta(minutes=H), "close"]
    swept = bool((s * (after - level) < 0).any())
    return {"t_in": tau, "p_in": p_in, "y": s * (p_out - p_in) * k, "swept": swept}


def events(bars: pd.DataFrame, family: str, H: int, k: float) -> pd.DataFrame:
    lv = day_levels(bars).dropna()
    b = bars.copy()
    b.index = b.index.tz_convert(TZ)
    rth = b.between_time("09:30", "15:59")
    rows = []
    for d, g in rth.groupby(rth.index.date):
        ts = pd.Timestamp(d)
        if ts not in lv.index:
            continue
        for kind, s, lvl in candidate_levels(lv.loc[ts], family):
            if not admitted(g, lvl, s):
                continue
            ev = first_cross(g, lvl, s, H, k)
            if ev:
                rows.append({"date": ts, "kind": kind, "s": s, "level": lvl, **ev})
    return pd.DataFrame(rows)


def p_two_sided(t: float) -> float:
    return float(2 * (1 - stats.norm.cdf(abs(t))))


def stage1(ev: pd.DataFrame) -> dict:
    """y ~ 1 + vero, errori standard clusterizzati per giorno."""
    df = ev.assign(is_true=(ev["kind"] == "true").astype(float), cl=pd.factorize(ev["date"])[0])
    fit = smf.ols("y ~ is_true", data=df).fit(cov_type="cluster", cov_kwds={"groups": df["cl"]})
    t = float(fit.tvalues["is_true"])
    tr, pl = df[df.is_true == 1], df[df.is_true == 0]
    out = {"coef": float(fit.params["is_true"]), "t": t, "p": p_two_sided(t),
           "n_true": int(len(tr)), "n_placebo": int(len(pl)),
           "mean_y_true": float(tr["y"].mean()), "mean_y_placebo": float(pl["y"].mean())}
    if "swept" in df:
        out["sweep_true"] = float(tr["swept"].mean())
        out["sweep_placebo"] = float(pl["swept"].mean())
    return out


def stage1_survivors(results: dict) -> list[tuple]:
    """results: {(strumento, famiglia, H): stage1 dict}. Aggiunge p_holm; sopravvive se |t|>3, p_holm<0.05
    e il segno del coefficiente e' uguale sull'altro strumento per la stessa (famiglia, H)."""
    from t1_engine import holm
    adj = holm({k: v["p"] for k, v in results.items()})
    for k, p in adj.items():
        results[k]["p_holm"] = p
    ok = {k for k, v in results.items() if abs(v["t"]) > 3 and v["p_holm"] < 0.05}
    out = []
    for k in ok:
        inst, fam, H = k
        twins = [o for o in ok if o[1:] == (fam, H) and o[0] != inst]
        if twins and all(np.sign(results[o]["coef"]) == np.sign(results[k]["coef"]) for o in twins):
            out.append(k)
    return sorted(out)
