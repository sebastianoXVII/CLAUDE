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
    """prices: giorni x DECISION_TIMES. sigma(t, HH:MM) = media di |P/Open - 1| sui 14 giorni validi PRECEDENTI."""
    move = (prices.div(opens, axis=0) - 1).abs()
    return move.shift(1).rolling(LOOKBACK, min_periods=LOOKBACK).mean()


def bounds(open_: float, prev_close: float, sigma: float) -> tuple[float, float]:
    return max(open_, prev_close) * (1 + sigma), min(open_, prev_close) * (1 - sigma)


def simulate_day(prices: dict, vwap: dict, ub: dict, lb: dict, close: float) -> list[dict]:
    """Decisioni solo a HH:00/HH:30. Prima si gestisce la posizione (inversione sulla banda opposta, poi trailing stop
    max(UB, VWAP) / min(LB, VWAP)), poi l'eventuale ingresso se flat. Dopo uno stop non si rientra nello stesso istante."""
    trades, pos, cur = [], 0, None

    def close_pos(t, p, reason):
        cur.update(exit_time=t, exit=float(p), reason=reason)
        trades.append(cur)

    for t in DECISION_TIMES:
        p, u, l, v = prices[t], ub[t], lb[t], vwap[t]
        if any(np.isnan(x) for x in (p, u, l)):
            continue
        stopped = False
        if pos == 1:
            if p < l:
                close_pos(t, p, "reversal")
                pos, cur = -1, {"side": -1, "entry_time": t, "entry": float(p)}
                continue
            if p < max(u, v if not np.isnan(v) else u):
                close_pos(t, p, "stop")
                pos, cur, stopped = 0, None, True
        elif pos == -1:
            if p > u:
                close_pos(t, p, "reversal")
                pos, cur = 1, {"side": 1, "entry_time": t, "entry": float(p)}
                continue
            if p > min(l, v if not np.isnan(v) else l):
                close_pos(t, p, "stop")
                pos, cur, stopped = 0, None, True
        if pos == 0 and not stopped:
            if p > u:
                pos, cur = 1, {"side": 1, "entry_time": t, "entry": float(p)}
            elif p < l:
                pos, cur = -1, {"side": -1, "entry_time": t, "entry": float(p)}
    if pos != 0 and not np.isnan(close):
        close_pos("16:00", close, "close")
    return trades
