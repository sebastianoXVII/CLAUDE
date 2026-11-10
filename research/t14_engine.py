"""Motore T14: ricerca sistematica di predicibilita' intraday. Spec: research/preregistration/T14_ricerca_sistematica.md.
Tempi in minuti dalla mezzanotte ET del giorno (negativi = giorno precedente)."""
from __future__ import annotations

import numpy as np
import pandas as pd

TZ = "America/New_York"
LOOKBACKS = [30, 60, 120, "anchor"]
ANCHOR = {"index": -480, "fx": -360}  # 16:00 / 18:00 del giorno precedente
CLOSE = 960  # 16:00
MIN_YEAR_DAYS = 60


def eh_pairs(kind: str) -> list[tuple]:
    if kind == "index":
        out = []
        for e in range(570, 931, 30):  # 09:30 ... 15:30
            out += [(e, h) for h in (30, 60, 120) if e + h <= CLOSE]
            if CLOSE - e > 120:
                out.append((e, "close"))
        return out
    return [(e, h) for e in range(0, 901, 30) for h in (30, 60, 120) if e + h <= 990]  # 00:00 ... 15:00, uscita <= 16:30


def configs(kind: str) -> list[dict]:
    out = []
    for e, h in eh_pairs(kind):
        out.append({"family": "S", "E": e, "H": h, "L": None})
        for fam in ("M", "MC"):
            out += [{"family": fam, "E": e, "H": h, "L": lb} for lb in LOOKBACKS]
    return out


def offsets(kind: str) -> list[int]:
    s = {ANCHOR[kind], CLOSE}
    for e, h in eh_pairs(kind):
        s |= {e, CLOSE if h == "close" else e + h} | {e - lb for lb in (30, 60, 120)}
    return sorted(s)


def price_grid(bars_et: pd.DataFrame, days: pd.DatetimeIndex, offs: list[int]) -> pd.DataFrame:
    """P(t) = close dell'ultima barra con timestamp in [t-5min, t-1min]."""
    days = pd.DatetimeIndex(days)
    # ora di parete ET (corretta nei giorni di cambio ora), poi localizzata
    tgt = pd.DataFrame([(d, o, d + pd.Timedelta(minutes=o - 1)) for d in days for o in offs], columns=["day", "off", "ts"])
    tgt["ts"] = tgt["ts"].dt.tz_localize(TZ, ambiguous=True, nonexistent="shift_forward")
    tgt = tgt.sort_values("ts")
    b = bars_et[["close"]].sort_index()
    b = b.assign(ts=b.index.astype(tgt["ts"].dtype)).reset_index(drop=True)
    m = pd.merge_asof(tgt, b, on="ts", direction="backward", tolerance=pd.Timedelta(minutes=4))
    return m.pivot(index="day", columns="off", values="close").reindex(index=days, columns=offs)


def _exit(cfg) -> int:
    return CLOSE if cfg["H"] == "close" else cfg["E"] + cfg["H"]


def _ret(grid: pd.DataFrame, cfg, anchor) -> pd.Series:
    lo = anchor if cfg["L"] == "anchor" else cfg["E"] - cfg["L"]
    return grid[cfg["E"]] / grid[lo] - 1


def big_move_mask(grid: pd.DataFrame, cfg, anchor) -> pd.Series:
    a = _ret(grid, cfg, anchor).abs()
    thr = a.shift(1).rolling(60, min_periods=40).quantile(0.8)
    return (a > thr).fillna(False)


def daily_gross(cfg, grid: pd.DataFrame, anchor) -> pd.Series:
    """P&L lordo con d = +1 (NaN = nessun trade)."""
    move = grid[_exit(cfg)] - grid[cfg["E"]]
    if cfg["family"] == "S":
        return move
    side = np.sign(_ret(grid, cfg, anchor)).replace(0.0, np.nan)
    g = side * move
    if cfg["family"] == "MC":
        g = g.where(big_move_mask(grid, cfg, anchor))
    return g


def net(gross: pd.Series, d: int, cost: float) -> pd.Series:
    return (d * gross - cost).where(gross.notna(), 0.0)


def year_sums(daily: pd.Series) -> dict:
    n = daily.groupby(daily.index.year).size()
    yr = pd.Series(daily.index.year, index=daily.index)
    for y in sorted(n.index):
        if n[y] < MIN_YEAR_DAYS and y + 1 in n.index:
            yr[yr == y] = y + 1
    return {int(a): float(b) for a, b in daily.groupby(yr.to_numpy()).sum().items()}


def stage1_pass(s: dict) -> bool:
    return s["t_nw"] > 3.0 and s["stress_mean"] > 0 and s["n_trades"] >= 150 and 3 * s["years_pos"] >= 2 * s["years"]
