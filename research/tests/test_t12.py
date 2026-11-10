import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_t12 as R  # noqa: E402


def test_to_returns_long_short_and_cost():
    tr = pd.DataFrame({"side": [1, -1], "entry": [100.0, 200.0], "exit": [101.0, 190.0]})
    out = R.to_returns(tr, 2.0)
    assert out["gross_ret"].tolist() == pytest.approx([0.01, 0.05])
    assert out["net_ret"].tolist() == pytest.approx([0.0098, 0.0498])


def test_evaluate_fills_flat_days_with_zero_and_counts_stress():
    d = pd.to_datetime(["2025-01-02", "2025-01-03", "2025-01-06"])
    tr = R.to_returns(pd.DataFrame({"date": [d[0], d[0]], "side": [1, 1], "entry": [100.0, 100.0], "exit": [101.0, 99.0]}), 1.0)
    m, daily = R.evaluate(tr, pd.DatetimeIndex(d), "2025-01-01", "2025-12-31", 1.0)
    assert len(daily) == 3 and daily.iloc[1:].tolist() == [0.0, 0.0]
    assert daily.iloc[0] == pytest.approx(-0.0002)
    assert m["stress2x_media_bp"] == pytest.approx(-4.0 / 3)
    assert m["n_trades"] == 2
