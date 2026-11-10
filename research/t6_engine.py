"""Motore T6: momentum intraday "Noise Area" (Zarattini-Aziz-Barbon). Specifica: research/preregistration/T6_noise_area_momentum.md."""
from __future__ import annotations

import numpy as np
import pandas as pd

from t1_engine import price_at

TZ = "America/New_York"
DECISION_TIMES = [f"{h:02d}:{m:02d}" for h in range(10, 16) for m in (0, 30)]  # 10:00 ... 15:30
LOOKBACK = 14


def day_inputs(b: pd.DataFrame) -> dict:
    """b: barre RTH di un giorno, indice ET. Prezzi P(HH:MM) e VWAP noto a ogni momento di decisione."""
    d = b.index[0].date()
    tp = (b["high"] + b["low"] + b["close"]) / 3
    cum_pv, cum_v = (tp * b["volume"]).cumsum(), b["volume"].cumsum()
    prices, vwap = {}, {}
    for t in DECISION_TIMES + ["16:00"]:
        ts = pd.Timestamp(f"{d} {t}", tz=TZ)
        prices[t] = price_at(b, ts)
        known = cum_v.loc[: ts - pd.Timedelta(minutes=1)]
        vwap[t] = float(cum_pv.loc[known.index[-1]] / known.iloc[-1]) if len(known) and known.iloc[-1] > 0 else np.nan
    first = b.loc[pd.Timestamp(f"{d} 09:30", tz=TZ):pd.Timestamp(f"{d} 09:30", tz=TZ)]
    return {"open": float(first["open"].iloc[0]) if len(first) else np.nan, "prices": prices, "vwap": vwap}


def sigma_table(prices: pd.DataFrame, opens: pd.Series) -> pd.DataFrame:
    """prices: giorni x DECISION_TIMES. sigma(t, HH:MM) = media di |P/Open - 1| sui 14 giorni COMPLETI precedenti
    (emendamento 2: un giorno incompleto viene saltato, non azzera i 14 successivi)."""
    move = (prices.div(opens, axis=0) - 1).abs()
    complete = move.dropna()
    sig_c = complete.rolling(LOOKBACK, min_periods=LOOKBACK).mean()
    # per ogni giorno: media dei 14 completi STRETTAMENTE precedenti
    pos = complete.index.searchsorted(move.index, side="left")  # numero di giorni completi prima di ciascun giorno
    out = pd.DataFrame(np.nan, index=move.index, columns=move.columns)
    for i, k in enumerate(pos):
        if k >= LOOKBACK:
            out.iloc[i] = sig_c.iloc[k - 1].values
    return out


def dividends_from_closes(adj_close: pd.Series, raw_close: pd.Series) -> pd.Series:
    """Dividendo nel giorno ex: D = close_raw(t-1) x (1 - f(t-1)/f(t)), con f = rettificato/grezzo (emendamento 2)."""
    f = adj_close / raw_close
    d = raw_close.shift(1) * (1 - f.shift(1) / f)
    d = d.where(d > 0.001 * raw_close.shift(1), 0.0)
    return d.fillna(0.0)


def bounds(open_: float, prev_close: float, sigma: float) -> tuple[float, float]:
    return max(open_, prev_close) * (1 + sigma), min(open_, prev_close) * (1 - sigma)


def simulate_day(prices: dict, vwap: dict, ub: dict, lb: dict, close: float) -> list[dict]:
    """Regola ufficiale degli autori (emendamento 2): a ogni HH:00/HH:30 la posizione DIVENTA il segnale:
    +1 se P > UB e P > VWAP, -1 se P < LB e P < VWAP, 0 altrimenti. Chiusura di tutto alle 16:00."""
    trades, pos, cur = [], 0, None
    for t in DECISION_TIMES:
        p, u, l, v = prices[t], ub[t], lb[t], vwap[t]
        if any(np.isnan(x) for x in (p, u, l, v)):
            continue  # prezzo mancante: la posizione resta invariata
        sig = 1 if (p > u and p > v) else -1 if (p < l and p < v) else 0
        if sig == pos:
            continue
        if pos != 0:
            cur.update(exit_time=t, exit=float(p), reason="reversal" if sig != 0 else "stop")
            trades.append(cur)
            cur = None
        if sig != 0:
            cur = {"side": sig, "entry_time": t, "entry": float(p)}
        pos = sig
    if pos != 0:
        cur.update(exit_time="16:00", exit=float(close), reason="close")
        trades.append(cur)
    return trades
