import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import vwap_proxy as V  # noqa: E402

TZ = "America/New_York"


def bars(day, minutes, vol):
    idx = pd.DatetimeIndex([pd.Timestamp(f"{day} {m}", tz=TZ) for m in minutes])
    return pd.DataFrame({"open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": vol}, index=idx)


def test_profile_is_median_volume_per_minute_of_day_within_rth():
    b = pd.concat([bars("2020-01-02", ["09:30", "09:31", "16:05"], [10, 1, 999]),
                   bars("2020-01-03", ["09:30", "09:31"], [30, 3]),
                   bars("2020-01-06", ["09:30", "09:31"], [20, 100])])
    p = V.volume_profile(b)
    assert p["09:30"] == 20 and p["09:31"] == 3
    assert "16:05" not in p.index


def test_profile_replaces_volume_by_minute_and_zero_outside():
    prof = pd.Series({"09:30": 5.0, "09:31": 7.0})
    b = bars("2012-03-05", ["09:30", "09:31", "09:32"], [0, 0, 0])
    out = V.with_profile_volume(b, prof)
    assert list(out["volume"]) == [5.0, 7.0, 0.0]
    assert list(b["volume"]) == [0, 0, 0]  # input not mutated


def test_agreement_counts_days_with_identical_trade_lists():
    a = pd.DataFrame({"date": pd.to_datetime(["2020-01-02", "2020-01-03", "2020-01-03"]),
                      "entry_time": ["10:00", "10:30", "12:00"], "side": [1, -1, 1],
                      "exit_time": ["16:00", "11:00", "16:00"]})
    b = a.copy()
    b.loc[2, "exit_time"] = "15:00"
    days = pd.to_datetime(["2020-01-02", "2020-01-03", "2020-01-06"])
    # 01-02 equal, 01-03 differs, 01-06 no trades in both -> equal
    assert np.isclose(V.agreement(a, b, days), 2 / 3)
