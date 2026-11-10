"""Statistiche di percorso di un trade: MFE/MAE in punti e in R."""
from __future__ import annotations

import pandas as pd


def path_stats(bars_in_trade: pd.DataFrame, side: int, entry: float, stop: float | None) -> dict:
    """bars_in_trade: le barre dall'ingresso all'uscita. MFE = massimo movimento favorevole, MAE = massimo avverso (<= 0)."""
    if side == 1:
        mfe, mae = bars_in_trade["high"].max() - entry, bars_in_trade["low"].min() - entry
    else:
        mfe, mae = entry - bars_in_trade["low"].min(), entry - bars_in_trade["high"].max()
    mfe, mae = max(float(mfe), 0.0), min(float(mae), 0.0)
    risk = abs(entry - stop) if stop is not None else None
    return {"mfe_pts": mfe, "mae_pts": mae,
            "mfe_r": mfe / risk if risk else None, "mae_r": mae / risk if risk else None,
            "minutes": int(len(bars_in_trade))}
