import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import t16_engine as E  # noqa: E402

TZ = "America/New_York"


# --- Task 1: livelli e giorni validi ---
def test_levels_tier_a_fx():
    assert np.allclose(E.levels(1.0960, 1.1110, 10000, 100, ()), [1.10, 1.11])


def test_levels_tier_b_excludes_00():
    assert np.allclose(E.levels(1.0940, 1.1060, 10000, 50, (100,)), [1.095, 1.105])


def test_levels_control_excludes_50_and_00():
    assert np.allclose(E.levels(1.0990, 1.1030, 10000, 25, (50,)), [1.1025])


def test_levels_gold_tier_b():
    assert np.allclose(E.levels(1243, 1262, 100, 1000, (5000,)), [1260.0])


def test_trading_day_1700_belongs_to_next_day():
    idx = pd.DatetimeIndex([pd.Timestamp("2015-03-05 16:59", tz=TZ), pd.Timestamp("2015-03-05 17:00", tz=TZ)])
    d = E.trading_day(idx)
    assert list(pd.DatetimeIndex(d)) == [pd.Timestamp("2015-03-05"), pd.Timestamp("2015-03-06")]


def _bars(start, n, price=1.1):
    idx = pd.date_range(pd.Timestamp(start, tz=TZ), periods=n, freq="min")
    return pd.DataFrame({"open": price, "high": price, "low": price, "close": price}, index=idx)


def test_valid_days_rules():
    full = _bars("2015-03-04 17:00", 1440)             # giovedì 5 marzo: valido
    thin = _bars("2015-03-05 17:00", 900)              # venerdì 6: < 1000 barre
    sat = _bars("2015-03-06 17:00", 1440)              # sabato 7
    xmas = _bars("2015-12-24 17:00", 1440)             # 25 dicembre
    v = E.valid_days(pd.concat([full, thin, sat, xmas]))
    assert list(v) == [pd.Timestamp("2015-03-05")]
