"""Motore del test T4 (concetti retail canonici). Specifica: research/preregistration/T4_concetti_retail.md.
Le barre sono a 1 minuto, indice ET, solo sessione regolare, un giorno per chiamata. Gli orari sono stringhe 'HH:MM' (inizio barra)."""
from __future__ import annotations

import numpy as np
import pandas as pd

TZ = "America/New_York"


def _t(b: pd.DataFrame, hhmm: str) -> pd.Timestamp:
    return pd.Timestamp(f"{b.index[0].date()} {hhmm}", tz=TZ)


def _trade(side, p_in, stop, target, start, last_bar="15:55", entry_bar_stop=False) -> dict:
    return {"side": int(side), "p_in": float(p_in), "stop": stop, "target": target, "start": start,
            "last_bar": last_bar, "entry_bar_stop": entry_bar_stop}


def simulate(b: pd.DataFrame, start: str, side: int, p_in: float, stop=None, target=None,
             last_bar: str = "15:55", entry_bar_stop: bool = False) -> dict:
    """Scorre le barre da `start` a `last_bar`. Stop prima del target nella stessa barra (conservativo).
    entry_bar_stop=True: nella barra d'ingresso (start) si controlla solo lo stop."""
    w = b.loc[_t(b, start):_t(b, last_bar)]
    for i, (_, bar) in enumerate(w.iterrows()):
        if stop is not None and ((side == 1 and bar["low"] <= stop) or (side == -1 and bar["high"] >= stop)):
            return {"p_out": float(stop), "reason": "stop"}
        if i == 0 and entry_bar_stop:
            continue
        if target is not None and ((side == 1 and bar["high"] >= target) or (side == -1 and bar["low"] <= target)):
            return {"p_out": float(target), "reason": "target"}
    if w.empty:
        return {"p_out": float(p_in), "reason": "nessuna_barra"}
    return {"p_out": float(w["close"].iloc[-1]), "reason": "time"}


def orb(b: pd.DataFrame) -> dict | None:
    rng = b.loc[_t(b, "09:30"):_t(b, "09:34")]
    if len(rng) < 5:
        return None
    o, c = rng["open"].iloc[0], rng["close"].iloc[-1]
    if c == o:
        return None
    side = 1 if c > o else -1
    stop = float(rng["low"].min()) if side == 1 else float(rng["high"].max())
    return _trade(side, c, stop, None, "09:35")


def gap_fill(b: pd.DataFrame, prev_close: float) -> dict | None:
    first = b.loc[_t(b, "09:30"):_t(b, "09:34")]
    if len(first) < 5 or not prev_close:
        return None
    gap = first["open"].iloc[0] / prev_close - 1
    if not (0.001 <= abs(gap) <= 0.01):
        return None
    side = -1 if gap > 0 else 1
    p_in = float(first["close"].iloc[-1])
    if side * (prev_close - p_in) <= 0:  # gap gia' chiuso nei primi 5 minuti: niente da prendere
        return None
    return _trade(side, p_in, None, float(prev_close), "09:35", last_bar="11:59")


def vwap_magnet(b: pd.DataFrame) -> dict | None:
    tp = (b["high"] + b["low"] + b["close"]) / 3
    vwap = (tp * b["volume"]).cumsum() / b["volume"].cumsum()
    w = b.loc[_t(b, "10:00"):_t(b, "14:30")]
    dev = w["close"] / vwap.loc[w.index] - 1
    hit = dev.abs() >= 0.003
    if not hit.any():
        return None
    ts = hit.idxmax()
    side = -1 if dev.loc[ts] > 0 else 1
    nxt = (ts + pd.Timedelta(minutes=1)).strftime("%H:%M")
    return _trade(side, b.loc[ts, "close"], None, float(vwap.loc[ts]), nxt)


def fvg(b: pd.DataFrame) -> dict | None:
    r5 = b.resample("5min", origin=_t(b, "09:30")).agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    for i in range(len(r5) - 2):
        b1, b3 = r5.iloc[i], r5.iloc[i + 2]
        closes_at = r5.index[i + 2] + pd.Timedelta(minutes=5)
        if not (_t(b, "09:45") <= closes_at <= _t(b, "14:00")):
            continue
        if b3["low"] > b1["high"]:
            side, entry, stop = 1, float(b1["high"]), float(b1["low"])
        elif b3["high"] < b1["low"]:
            side, entry, stop = -1, float(b1["low"]), float(b1["high"])
        else:
            continue
        after = b.loc[closes_at:_t(b, "14:59")]
        touch = after["low"] <= entry if side == 1 else after["high"] >= entry
        if not touch.any():
            return None  # il primo FVG non viene mai ritestato: nessun trade
        ts = touch.idxmax()
        risk = abs(entry - stop)
        return _trade(side, entry, stop, entry + side * 2 * risk, ts.strftime("%H:%M"), entry_bar_stop=True)
    return None
