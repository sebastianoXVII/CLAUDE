"""Motore T15: time-series momentum diversificato su barre giornaliere. Spec: research/preregistration/T15_trend_following_diversificato.md."""
from __future__ import annotations

import numpy as np
import pandas as pd

MIN_BARS = 120
ANN = 261
TARGET_VOL, CAP = 0.40, 4.0
HORIZONS = {"V1": [252], "V2": [21, 63, 252]}


def returns(d: pd.DataFrame) -> pd.Series:
    c = d.loc[d["n_bars"] >= MIN_BARS, "close"]
    return (c / c.shift(1) - 1).iloc[1:]


def valid_close(d: pd.DataFrame) -> pd.Series:
    return d.loc[d["n_bars"] >= MIN_BARS, "close"]


def signal(close: pd.Series, variant: str) -> pd.Series:
    """Segnale al close di t sui giorni validi: media dei segni dei rendimenti sugli orizzonti della variante."""
    sigs = [np.sign(close / close.shift(h) - 1) for h in HORIZONS[variant]]
    return pd.concat(sigs, axis=1).mean(axis=1, skipna=False)


def ewma_vol(r: pd.Series) -> pd.Series:
    return np.sqrt((r**2).ewm(com=60).mean() * ANN)


def positions(sig: pd.Series, vol: pd.Series) -> pd.Series:
    return (sig * TARGET_VOL / vol).clip(-CAP, CAP)


def instrument_pnl(pos: pd.Series, r: pd.Series, cost: float, fin: float) -> pd.DataFrame:
    """pos e r sullo stesso indice (giorni validi). P&L del giorno t = pos(t-1) * r(t)."""
    held = pos.shift(1)
    change = (pos.fillna(0.0) - pos.fillna(0.0).shift(1).fillna(0.0)).abs()
    return pd.DataFrame({"gross": (held * r).fillna(0.0), "tcost": change * cost / 2,
                         "fcost": held.abs().fillna(0.0) * fin / 252, "avail": held.notna()}, index=pos.index)


def portfolio(parts: dict[str, pd.DataFrame], cost_mult: float = 1.0) -> pd.Series:
    idx = sorted(set().union(*[p.index for p in parts.values()]))
    num, den = pd.Series(0.0, index=idx), pd.Series(0.0, index=idx)
    for p in parts.values():
        q = p.reindex(idx)
        avail = q["avail"].astype("boolean").ffill().fillna(False).astype(bool)
        avail &= pd.Series(np.asarray(idx) <= p.index.max(), index=idx)  # fuori dal portafoglio dopo l'ultimo dato
        net = (q["gross"] - cost_mult * (q["tcost"] + q["fcost"])).fillna(0.0)
        num += net.where(avail, 0.0)
        den += avail.astype(float)
    return (num / den).where(den > 0).dropna()
