import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data"))
import histdata_daily as D  # noqa: E402

TZ = "America/New_York"


def m1(stamps, closes):
    idx = pd.DatetimeIndex([pd.Timestamp(s, tz=TZ) for s in stamps]).tz_convert("UTC")
    c = np.asarray(closes, dtype=float)
    return pd.DataFrame({"open": c, "high": c + 1, "low": c - 1, "close": c, "volume": 0.0}, index=idx)


def test_trading_day_ends_at_1700_new_york():
    b = m1(["2015-03-01 17:00", "2015-03-02 09:00", "2015-03-02 16:59", "2015-03-02 17:00", "2015-03-03 10:00"],
           [1, 2, 3, 4, 5])
    d = D.to_daily(b)
    assert list(d.index) == [pd.Timestamp("2015-03-02"), pd.Timestamp("2015-03-03")]
    assert d.loc["2015-03-02", "open"] == 1 and d.loc["2015-03-02", "close"] == 3
    assert d.loc["2015-03-02", "high"] == 4  # max(high) = 3 + 1
    assert d.loc["2015-03-02", "n_bars"] == 3
    assert d.loc["2015-03-03", "open"] == 4 and d.loc["2015-03-03", "close"] == 5


def test_daily_high_low_are_extremes_of_the_session():
    b = m1(["2015-03-02 01:00", "2015-03-02 02:00"], [10, 7])
    d = D.to_daily(b)
    assert d.iloc[0]["high"] == 11 and d.iloc[0]["low"] == 6


def test_weekend_bars_roll_into_monday_and_no_saturday_rows():
    b = m1(["2015-03-06 16:00", "2015-03-08 18:00", "2015-03-09 08:00"], [1, 2, 3])
    d = D.to_daily(b)
    assert list(d.index) == [pd.Timestamp("2015-03-06"), pd.Timestamp("2015-03-09")]
    assert d.loc["2015-03-09", "open"] == 2


def test_from_m1_parquet_dedups_sorts_and_matches_to_daily(tmp_path):
    b = m1(["2015-03-02 10:00", "2015-03-02 09:00", "2015-03-02 09:00", "2015-03-03 10:00"], [2, 1, 9, 5])
    p = tmp_path / "X_1m_24h.parquet"
    b.to_parquet(p)
    out = tmp_path / "X_1d.parquet"
    D.from_m1(str(p), str(out))
    d = pd.read_parquet(out)
    assert d.loc["2015-03-02", "n_bars"] == 2  # duplicato rimosso
    assert d.loc["2015-03-02", "open"] == 1 and d.loc["2015-03-02", "close"] == 2  # ordinato nel tempo, primo duplicato tenuto
