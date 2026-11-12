"""Motore T16: numeri tondi (Osler), rimbalzo (R) e accelerazione (S) su barre M1.
Spec: research/preregistration/T16_numeri_tondi.md. Piano: docs/superpowers/plans/2026-11-12-t16-numeri-tondi.md."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

TZ = "America/New_York"
MIN_BARS = 1000
EPS = 1e-9


def levels(lo: float, hi: float, scale: int, step: int, excl: tuple[int, ...]) -> np.ndarray:
    """Prezzi dei multipli di `step` (in unità intere = prezzo*scale) in [lo, hi], esclusi i multipli dei valori in excl."""
    k0, k1 = math.ceil(round(lo * scale, 6) / step), math.floor(round(hi * scale, 6) / step)
    units = [k * step for k in range(k0, k1 + 1) if not any((k * step) % x == 0 for x in excl)]
    return np.array([u / scale for u in units], dtype=float)


def trading_day(idx_et: pd.DatetimeIndex) -> np.ndarray:
    """Giorno di trading: dalle 17:00 ET del giorno prima alle 16:59, etichettato con la data di chiusura."""
    return (idx_et + pd.Timedelta(hours=7)).tz_localize(None).normalize().to_numpy()


def valid_days(bars_et: pd.DataFrame) -> pd.DatetimeIndex:
    d = pd.Series(1, index=pd.DatetimeIndex(trading_day(bars_et.index))).groupby(level=0).size()
    ok = (d.index.weekday < 5) & ~((d.index.month == 12) & (d.index.day == 25)) & ~((d.index.month == 1) & (d.index.day == 1))
    return d.index[ok & (d.to_numpy() >= MIN_BARS)]
