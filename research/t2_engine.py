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


def _reached(b: pd.DataFrame, level: float, s: int) -> bool:
    return bool(((b["high"] >= level) if s == 1 else (b["low"] <= level)).any())


def admitted(day_bars: pd.DataFrame, level: float, s: int, family: str = "PM") -> bool:
    """Ammesso se a 09:35 il prezzo sta dalla parte giusta E il livello non e' gia' stato raggiunto
    nelle barre 09:30-09:34 (emendamento 1); per PD neanche nel pre-market 04:00-09:29."""
    d = day_bars.index[0].date()
    p = price_at(day_bars, pd.Timestamp(f"{d} 09:35", tz=TZ))
    if np.isnan(p) or s * (level - p) <= 0:
        return False
    if _reached(day_bars.between_time("09:30", "09:34"), level, s):
        return False
    if family == "PD" and _reached(day_bars.between_time("04:00", "09:29"), level, s):
        return False
    return True


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
    p_in = float(day_bars.loc[tau, "close"])
    p_out = price_at(day_bars, tau + ONE_MIN + pd.Timedelta(minutes=H))
    if np.isnan(p_out):
        return None
    after = day_bars.loc[tau + ONE_MIN: tau + pd.Timedelta(minutes=H), "close"]
    swept = bool((s * (after - level) < 0).any())
    return {"t_in": tau, "p_in": p_in, "y": s * (p_out - p_in) * k, "swept": swept}


EV_COLS = ["date", "kind", "s", "level", "t_in", "p_in", "y", "swept", "dist", "bucket", "side"]
FAMILY_COLS = {"PD": ["pd_high", "pd_low", "prev_range"], "PM": ["pm_high", "pm_low", "prev_range"]}


def events(bars: pd.DataFrame, family: str, H: int, k: float) -> pd.DataFrame:
    """Eventi di primo attraversamento per livelli veri e placebo, con le variabili di controllo dell'emendamento 1."""
    assert bars.index.is_unique and bars.index.is_monotonic_increasing, "indice barre non unico/ordinato"
    lv = day_levels(bars).dropna(subset=FAMILY_COLS[family])
    b = bars.copy()
    b.index = b.index.tz_convert(TZ)
    b = b.between_time("04:00", "15:59")
    rows = []
    for d, g in b.groupby(b.index.date):
        ts = pd.Timestamp(d)
        if ts not in lv.index:
            continue
        p935 = price_at(g, pd.Timestamp(f"{d} 09:35", tz=TZ))
        for kind, s_, lvl in candidate_levels(lv.loc[ts], family):
            if not admitted(g, lvl, s_, family):
                continue
            ev = first_cross(g, lvl, s_, H, k)
            if ev:
                mins = (ev["t_in"] - pd.Timestamp(f"{d} 09:35", tz=TZ)).total_seconds() / 60
                rows.append({"date": ts, "kind": kind, "s": s_, "level": lvl, **ev,
                             "dist": abs(lvl - p935) / lv.loc[ts, "prev_range"], "bucket": int(mins // 30), "side": s_})
    return pd.DataFrame(rows, columns=EV_COLS)


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
    if {"dist", "bucket", "side"} <= set(df.columns):
        fa = smf.ols("y ~ is_true + dist + C(bucket) + C(side)", data=df).fit(
            cov_type="cluster", cov_kwds={"groups": df["cl"]})
        out["coef_adj"], out["t_adj"] = float(fa.params["is_true"]), float(fa.tvalues["is_true"])
    return out


def stage1_survivors(results: dict) -> list[tuple]:
    """results: {(strumento, famiglia, H): stage1 dict}. Aggiunge p_holm; sopravvive se |t|>3, p_holm<0.05
    e il segno del coefficiente e' uguale sull'altro strumento per la stessa (famiglia, H)."""
    from t1_engine import holm
    adj = holm({k: v["p"] for k, v in results.items()})
    for k, p in adj.items():
        results[k]["p_holm"] = p
    ok = {k for k, v in results.items() if abs(v["t"]) > 3 and v["p_holm"] < 0.05
          and abs(v.get("t_adj", 0.0)) > 3 and np.sign(v.get("coef_adj", 0.0)) == np.sign(v["coef"])}
    out = []
    for k in ok:
        inst, fam, H = k
        twins = [o for o in ok if o[1:] == (fam, H) and o[0] != inst]
        if twins and all(np.sign(results[o]["coef"]) == np.sign(results[k]["coef"]) for o in twins):
            out.append(k)
    return sorted(out)


def stage2(ev: pd.DataFrame, direction: float, cost: float, valid_days: pd.DatetimeIndex, usd_per_pt: float) -> dict:
    """Regola: a ogni attraversamento si entra nella direzione s x segno(effetto), uscita dopo H. P&L giornaliero
    sui soli giorni validi (emendamento 1). Metriche per trade calcolate per singolo trade."""
    from t1_engine import metrics
    per_trade = direction * ev["y"] - cost
    daily = per_trade.groupby(ev["date"]).sum().reindex(valid_days, fill_value=0.0)
    m = metrics(daily, daily.index.isin(ev["date"]), usd_per_pt)
    m["n_trades"] = int(len(ev))
    m["per_trade_pt"] = float(per_trade.mean()) if len(ev) else np.nan
    m["per_trade_usd"] = m["per_trade_pt"] * usd_per_pt
    m["trade_win_rate"] = float((per_trade > 0).mean()) if len(ev) else np.nan
    stress = (direction * ev["y"] - 2 * cost).groupby(ev["date"]).sum().reindex(valid_days, fill_value=0.0)
    m["stress2x_media_pt"] = float(stress.mean())
    yr = daily.groupby(daily.index.year).sum()
    m["anni_positivi"] = f"{int((yr > 0).sum())}/{len(yr)}"
    return m
