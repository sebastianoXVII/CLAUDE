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
                         "fcost": held.abs().fillna(0.0) * fin / 252, "avail": held.notna() | pos.notna()}, index=pos.index)


BREAK_LOG = np.log(2.0)  # Emendamento 2: rottura se il prezzo raddoppia o si dimezza in un giorno


def segments(close: pd.Series, exclude: list[tuple[str, str]] | None = None) -> list[pd.Series]:
    """Emendamento 2. Spezza la serie dei close validi in segmenti indipendenti.
    Giorni non validi (close <= 0, o dentro una finestra esclusa) vengono tolti e creano una rottura;
    c'è rottura anche fra due giorni consecutivi con |ln r| > ln 2."""
    bad = close <= 0
    for a, b in exclude or []:
        bad |= (close.index >= pd.Timestamp(a)) & (close.index <= pd.Timestamp(b))
    removed_so_far = bad.cumsum()[~bad]
    c = close[~bad]
    jump = np.log(c / c.shift(1)).abs() > BREAK_LOG
    new_seg = jump | (removed_so_far.diff() > 0)
    seg_id = new_seg.cumsum()
    return [g for _, g in c.groupby(seg_id, sort=True)]


def instrument_parts(close: pd.Series, variant: str, cost: float, fin: float,
                     exclude: list[tuple[str, str]] | None = None) -> pd.DataFrame:
    """P&L per strumento con segmenti indipendenti: segnale e volatilità ripartono da zero dopo ogni rottura."""
    out = []
    segs = segments(close, exclude)
    for k, seg in enumerate(segs):
        r = seg / seg.shift(1) - 1
        part = instrument_pnl(positions(signal(seg, variant), ewma_vol(r)), r, cost, fin)
        # carry: cosa ereditano i giorni assenti dal file dopo questa riga. False dopo la fine di un segmento non finale
        part["carry"] = part["avail"]
        if k < len(segs) - 1:
            part.iloc[-1, part.columns.get_loc("carry")] = False
        out.append(part)
    if not out:
        return pd.DataFrame({"gross": 0.0, "tcost": 0.0, "fcost": 0.0, "avail": False, "carry": False}, index=close.index)
    res = pd.concat(out)
    # giorni tolti (close <= 0, finestre escluse): righe esplicite fuori portafoglio, così il ffill di portfolio() non le conta
    res = res.reindex(close.index)
    res[["gross", "tcost", "fcost"]] = res[["gross", "tcost", "fcost"]].fillna(0.0)
    for col in ("avail", "carry"):
        res[col] = res[col].astype("boolean").fillna(False).astype(bool)
    return res


def portfolio(parts: dict[str, pd.DataFrame], cost_mult: float = 1.0) -> pd.Series:
    idx = sorted(set().union(*[p.index for p in parts.values()]))
    num, den = pd.Series(0.0, index=idx), pd.Series(0.0, index=idx)
    for p in parts.values():
        q = p.reindex(idx)
        own = q["avail"].astype("boolean")                       # righe presenti: il loro avail
        carry = q["carry"] if "carry" in q else q["avail"]        # righe assenti dal file: ereditano carry (review F1)
        avail = own.fillna(carry.astype("boolean").ffill()).fillna(False).astype(bool)
        avail &= pd.Series(np.asarray(idx) <= p.index.max(), index=idx)  # fuori dal portafoglio dopo l'ultimo dato
        net = (q["gross"] - cost_mult * (q["tcost"] + q["fcost"])).fillna(0.0)
        num += net.where(avail, 0.0)
        den += avail.astype(float)
    return (num / den).where(den > 0).dropna()
