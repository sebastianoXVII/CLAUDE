"""VWAP da profilo di volume (T7 emendamento 2): il volume di ogni barra RTH e' la mediana del volume QQQ in quel minuto."""
from __future__ import annotations

import pandas as pd


def _hhmm(idx: pd.DatetimeIndex) -> pd.Index:
    return pd.Index(idx.strftime("%H:%M"))


def volume_profile(bars_et: pd.DataFrame) -> pd.Series:
    """bars_et: barre a 1 minuto con indice ET. Mediana del volume per minuto del giorno, solo 09:30-15:59."""
    rth = bars_et.between_time("09:30", "15:59")
    return rth["volume"].groupby(_hhmm(rth.index)).median()


def with_profile_volume(bars_et: pd.DataFrame, profile: pd.Series) -> pd.DataFrame:
    """Copia di bars_et con volume = profilo del suo minuto (0 fuori profilo)."""
    out = bars_et.copy()
    out["volume"] = profile.reindex(_hhmm(out.index)).fillna(0.0).to_numpy(dtype=float)
    return out


def agreement(a: pd.DataFrame, b: pd.DataFrame, days: pd.DatetimeIndex) -> float:
    """Quota dei giorni in cui la lista dei trade (entry_time, side, exit_time) e' identica."""
    def key(t: pd.DataFrame, d) -> list:
        s = t[t["date"] == d]
        return list(zip(s["entry_time"], s["side"], s["exit_time"]))
    return sum(key(a, d) == key(b, d) for d in days) / len(days)
