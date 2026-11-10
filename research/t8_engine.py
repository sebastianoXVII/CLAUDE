"""Motore T8: concetti di sessione e liquidita' (box Asia, sweep di Londra, POI, IFVG, order block).
Specifica: research/preregistration/T8_sessioni_liquidita.md. Le barre sono a 1 minuto, indice ET, e coprono
dalle 18:00 del giorno precedente alle 15:59 del giorno D."""
from __future__ import annotations

import numpy as np
import pandas as pd

TZ = "America/New_York"
FIVE = pd.Timedelta(minutes=5)
ONE = pd.Timedelta(minutes=1)


def _ts(D, hhmm, prev=False):
    d = (pd.Timestamp(D) - pd.Timedelta(days=1)) if prev else pd.Timestamp(D)
    return pd.Timestamp(f"{d.date()} {hhmm}", tz=TZ)


def _r5(b: pd.DataFrame, D) -> pd.DataFrame:
    """Barre a 5 minuti allineate alla mezzanotte ET del giorno D (etichetta = inizio barra)."""
    r = b.resample("5min", origin=_ts(D, "00:00")).agg({"open": "first", "high": "max", "low": "min", "close": "last"})
    return r.dropna()


def _trade(side, p_in, stop, target, start, last, entry_bar_stop=False):
    return {"side": int(side), "p_in": float(p_in), "stop": None if stop is None else float(stop),
            "target": None if target is None else float(target), "start": start, "last": last,
            "entry_bar_stop": entry_bar_stop}


def asia_range(b, D):
    w = b.loc[_ts(D, "20:00", True):_ts(D, "23:59", True)]
    return float(w["high"].max()), float(w["low"].min())


def london_range(b, D):
    w = b.loc[_ts(D, "02:00"):_ts(D, "08:29")]
    return float(w["high"].max()), float(w["low"].min())


def htf_trend(prev_closes: pd.Series) -> int:
    """+1 se l'ultimo close delle 16:00 e' sopra la sua media a 20 giorni, -1 altrimenti."""
    last20 = prev_closes.iloc[-20:]
    return 1 if prev_closes.iloc[-1] > last20.mean() else -1


def simulate(b, start, side, p_in, stop=None, target=None, last=None, entry_bar_stop=False) -> dict:
    """Simulatore conservativo (come T4): stop prima del target; stop all'open se la barra apre oltre lo stop."""
    w = b.loc[start:last]
    for i, (_, bar) in enumerate(w.iterrows()):
        if stop is not None and ((side == 1 and bar["low"] <= stop) or (side == -1 and bar["high"] >= stop)):
            fill = stop if (i == 0 and entry_bar_stop) else (min(bar["open"], stop) if side == 1 else max(bar["open"], stop))
            return {"p_out": float(fill), "reason": "stop", "t_out": bar.name}
        if i == 0 and entry_bar_stop:
            continue
        if target is not None and ((side == 1 and bar["high"] >= target) or (side == -1 and bar["low"] <= target)):
            return {"p_out": float(target), "reason": "target", "t_out": bar.name}
    if w.empty:
        return {"p_out": float(p_in), "reason": "nessuna_barra", "t_out": start}
    return {"p_out": float(w["close"].iloc[-1]), "reason": "time", "t_out": w.index[-1]}


def _inside(c, hi, lo):
    return lo <= c <= hi


def _close_at(b, t):
    """Close dell'ultima barra a 1 minuto con inizio <= t (NaN se nessuna)."""
    s = b.loc[:t, "close"]
    return float(s.iloc[-1]) if len(s) else np.nan


def _starts_inside(b, t, hi, lo):
    """Emendamento 2: lo sweep/rottura vale solo se il close della barra prima della finestra sta dentro il range."""
    c = _close_at(b, t)
    return not np.isnan(c) and _inside(c, hi, lo)


def _sweep_and_reclaim(r, hi, lo, t0, t1, reclaim_until=None):
    """Primo superamento di hi/lo con barra che inizia in [t0, t1]; poi prima barra (anche la stessa) che chiude dentro,
    con inizio <= reclaim_until(t_sweep) (default: t1)."""
    w = r.loc[t0:t1]
    for i in range(len(w)):
        bar = w.iloc[i]
        if bar["high"] > hi or bar["low"] < lo:
            s = -1 if bar["high"] > hi else 1  # trade opposto allo sweep
            t_sw = w.index[i]
            limit = reclaim_until(t_sw) if reclaim_until else t1
            seg_all = r.loc[t_sw:limit]
            for j in range(len(seg_all)):
                if _inside(seg_all.iloc[j]["close"], hi, lo):
                    seg = seg_all.iloc[:j + 1]
                    extreme = seg["high"].max() if s == -1 else seg["low"].min()
                    return s, float(seg_all.iloc[j]["close"]), float(extreme), seg_all.index[j] + FIVE
            return None
    return None


def h8a(b, D, asia):
    hi, lo = asia
    if not _starts_inside(b, _ts(D, "01:59"), hi, lo):
        return None
    r = _r5(b, D)
    ev = _sweep_and_reclaim(r, hi, lo, _ts(D, "02:00"), _ts(D, "04:55"),
                            reclaim_until=lambda t: t + pd.Timedelta(minutes=25))
    if ev is None:
        return None
    s, p, ext, start = ev
    return _trade(s, p, ext, lo if s == -1 else hi, start, _ts(D, "10:59"))


def h8b(b, D, asia):
    hi, lo = asia
    if not _starts_inside(b, _ts(D, "02:59"), hi, lo):
        return None
    mid = (hi + lo) / 2
    r = _r5(b, D).loc[_ts(D, "03:00"):_ts(D, "10:55")]
    for k in range(len(r)):
        c = r.iloc[k]["close"]
        if _inside(c, hi, lo):
            continue
        d = 1 if c > hi else -1
        nxt = r.iloc[k + 1:k + 4]
        if len(nxt) < 3 or nxt.index[-1] - r.index[k] != 3 * FIVE:
            return None  # emendamento 2: 3 barre contigue
        for j in range(3):
            cj = nxt.iloc[j]["close"]
            if (d == 1 and cj < lo) or (d == -1 and cj > hi):
                return None  # emendamento 2: attraversa tutto il box -> nessun trade
            if _inside(cj, hi, lo):  # riassorbimento
                seg = r.iloc[k:k + 2 + j]
                ext = seg["high"].max() if d == 1 else seg["low"].min()
                return _trade(-d, cj, ext, lo if d == 1 else hi, nxt.index[j] + FIVE, _ts(D, "15:55"))
        p = nxt.iloc[2]["close"]  # accettazione
        risk = abs(p - mid)
        return _trade(d, p, mid, p + d * 2 * risk, nxt.index[2] + FIVE, _ts(D, "15:55"))
    return None


def h8c(b, D, london):
    hi, lo = london
    if not _starts_inside(b, _ts(D, "09:29"), hi, lo):
        return None
    r = _r5(b, D)
    ev = _sweep_and_reclaim(r, hi, lo, _ts(D, "09:30"), _ts(D, "10:55"))
    if ev is None:
        return None
    s, p, ext, start = ev
    risk = abs(p - ext)
    if risk == 0:
        return None
    return _trade(s, p, ext, p + s * 2 * risk, start, _ts(D, "15:55"))


def h8d(b, D):
    """Emendamento 2: FVG con barra 1 in 08:30-10:59; si usa quello INVALIDATO PER PRIMO nel tempo (parita': formato prima);
    ingresso al primo tocco del bordo entro la barra delle 11:28; se non toccato, nessun trade."""
    r = _r5(b, D)
    deadline = _ts(D, "11:28")
    cands = []
    w = r.loc[_ts(D, "08:30"):_ts(D, "10:59")]
    for i in range(len(w)):
        t1 = w.index[i]
        if t1 + 2 * FIVE not in r.index or t1 + FIVE not in r.index:
            continue
        b1, b3 = r.loc[t1], r.loc[t1 + 2 * FIVE]
        if b3["low"] > b1["high"]:
            edge, far, side = float(b1["high"]), float(b3["low"]), -1
        elif b3["high"] < b1["low"]:
            edge, far, side = float(b1["low"]), float(b3["high"]), 1
        else:
            continue
        after = r.loc[t1 + 3 * FIVE:deadline - FIVE]
        inv = after[after["close"] < edge] if side == -1 else after[after["close"] > edge]
        if inv.empty:
            continue
        cands.append((inv.index[0] + FIVE, t1, edge, far, side))
    if not cands:
        return None
    t_inv, _t1, edge, far, side = min(cands)
    m = b.loc[t_inv:deadline]
    touch = m["high"] >= edge if side == -1 else m["low"] <= edge
    risk = abs(far - edge)
    if not touch.any() or risk == 0:
        return None
    return _trade(side, edge, far, edge + side * 2 * risk, touch.idxmax(), _ts(D, "15:55"), entry_bar_stop=True)


def h8e(b, D):
    r = _r5(b, D)
    rng = r["high"] - r["low"]
    avg = rng.shift(1).rolling(20, min_periods=20).mean()
    w = r.loc[_ts(D, "08:30"):_ts(D, "10:55")]
    for t, bar in w.iterrows():
        a = avg.loc[t]
        rg = bar["high"] - bar["low"]
        if np.isnan(a) or a <= 0 or rg < 2 * a or abs(bar["close"] - bar["open"]) < 0.7 * rg:
            continue
        d = 1 if bar["close"] > bar["open"] else -1
        prior = r.loc[:t - FIVE]
        opp = prior[(prior["close"] < prior["open"])] if d == 1 else prior[(prior["close"] > prior["open"])]
        if opp.empty:
            return None  # emendamento 2: solo il primo displacement
        ob = opp.iloc[-1]
        edge, far = (float(ob["high"]), float(ob["low"])) if d == 1 else (float(ob["low"]), float(ob["high"]))
        m = b.loc[t + FIVE:_ts(D, "11:59")]
        touch = m["low"] <= edge if d == 1 else m["high"] >= edge
        if not touch.any():
            return None
        risk = abs(edge - far)
        if risk == 0:
            return None
        return _trade(d, edge, far, edge + d * 2 * risk, touch.idxmax(), _ts(D, "15:55"), entry_bar_stop=True)
    return None
