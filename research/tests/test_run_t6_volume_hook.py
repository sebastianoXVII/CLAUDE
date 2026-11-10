import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_t6 as R6  # noqa: E402


def _write(tmp: Path):
    idx = []
    for d in pd.bdate_range("2019-03-04", periods=3):
        idx += list(pd.date_range(f"{d.date()} 09:30", f"{d.date()} 15:59", freq="1min", tz="America/New_York"))
    idx = pd.DatetimeIndex(idx)
    px = 100 + np.arange(len(idx)) * 0.01
    df = pd.DataFrame({"open": px, "high": px, "low": px, "close": px, "volume": 1.0}, index=idx.tz_convert("UTC"))
    for name in ("XYZ_1m.parquet", "XYZ_1m_raw.parquet"):
        df.to_parquet(tmp / name)


def test_build_applies_volume_fn_to_rth_bars(tmp_path, monkeypatch):
    _write(tmp_path)
    monkeypatch.setattr(R6, "BARS", tmp_path)

    def first_bar_only(b):
        v = np.zeros(len(b))
        v[b.index.strftime("%H:%M") == "09:30"] = 1.0
        return b.assign(volume=v)

    _t, _s, days = R6.build("XYZ", volume_fn=first_bar_only)
    g, inp = next(iter(days.values()))
    assert np.isclose(inp["vwap"]["15:30"], g["close"].iloc[0])
    _t, _s, days0 = R6.build("XYZ")
    assert inp["vwap"]["15:30"] < next(iter(days0.values()))[1]["vwap"]["15:30"]
