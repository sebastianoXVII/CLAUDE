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


def _prev_index(mask: np.ndarray) -> np.ndarray:
    """Per ogni i: indice massimo j < i con mask[j], altrimenti -1."""
    idx = np.where(mask, np.arange(len(mask)), -1)
    acc = np.maximum.accumulate(idx)
    return np.concatenate(([-1], acc[:-1]))


def level_events(high: np.ndarray, low: np.ndarray, close: np.ndarray, L: float, D: float, delta: float,
                 kind: str) -> list[tuple[int, int]]:
    """Eventi R (rimbalzo, lato contro l'avvicinamento) o S (superamento di delta, lato del superamento) sul livello L.
    Evento in i se hit[i] e l'ultimo armamento (barra < i) è più recente dell'ultimo hit (barra < i)."""
    out = []
    for frm in ("below", "above"):
        if frm == "below":
            arm = close <= L - D + EPS
            hit = high >= (L if kind == "R" else L + delta) - EPS
            side = -1 if kind == "R" else 1
        else:
            arm = close >= L + D - EPS
            hit = low <= (L if kind == "R" else L - delta) + EPS
            side = 1 if kind == "R" else -1
        pa, ph = _prev_index(arm), _prev_index(hit)
        ev = hit & (pa >= 0) & (pa > ph)
        out += [(int(i), side) for i in np.flatnonzero(ev)]
    return sorted(out)


WIN_LO, WIN_HI = 2 * 60, 15 * 60 + 59          # T = ts + 1 min fra 02:00 e 15:59 ET
HOLD = pd.Timedelta(minutes=60)
EXIT_FROM = pd.Timedelta(minutes=56)          # uscita: ultima barra con ts in [ts+56, ts+60]
COLS = ["day", "entry_time", "side", "level", "p_in", "p_out", "gross", "net"]


def day_trades(day: pd.DataFrame, lv: np.ndarray, D: float, delta: float, kind: str, cost: float) -> pd.DataFrame:
    """Trade di un giorno di trading per un tier: eventi su tutti i livelli rilevanti, finestra, uscita a +60, nessuna sovrapposizione."""
    h, lo, c = (day[k].to_numpy(float) for k in ("high", "low", "close"))
    ts = day.index
    if len(ts) == 0:
        return pd.DataFrame(columns=COLS)
    rel = lv[(lv >= lo.min() - D - delta) & (lv <= h.max() + D + delta)]
    tmin = ts.hour * 60 + ts.minute + 1
    ns = ts.as_unit("ns").asi8                        # unità esplicita: pandas 3 può usare us o ns
    cand = []
    for L in rel:
        for i, side in level_events(h, lo, c, L, D, delta, kind):
            if not (WIN_LO <= tmin[i] <= WIN_HI):
                continue
            j = np.searchsorted(ns, ns[i] + HOLD.value, side="right") - 1
            if j <= i or ns[j] < ns[i] + EXIT_FROM.value:
                continue                                   # manca il prezzo di uscita: trade scartato
            cand.append((i, float(L), side, j))
    cand.sort(key=lambda e: (e[0], e[1], e[2]))
    rows, last_t = [], None
    for i, L, side, j in cand:
        t_in = ts[i] + pd.Timedelta(minutes=1)
        if last_t is not None and t_in < last_t + HOLD:
            continue
        last_t = t_in
        g = side * (c[j] - c[i])
        rows.append((pd.Timestamp(trading_day(ts[i:i + 1])[0]), t_in, side, L, c[i], c[j], g, g - cost))
    return pd.DataFrame(rows, columns=COLS)


def daily_pnl(trades: pd.DataFrame, days: pd.DatetimeIndex, cost_mult: float) -> pd.Series:
    """P&L giornaliero sui giorni validi (zero senza trade). Costo = gross - net, scalato da cost_mult."""
    if len(trades) == 0:
        return pd.Series(0.0, index=days)
    x = trades["gross"] - cost_mult * (trades["gross"] - trades["net"])
    return x.groupby(pd.DatetimeIndex(trades["day"])).sum().reindex(days, fill_value=0.0)
