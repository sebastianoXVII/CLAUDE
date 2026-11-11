import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data"))
import daily_quality as Q  # noqa: E402


def test_gaps_longer_than_5_business_days():
    idx = pd.DatetimeIndex(list(pd.bdate_range("2015-01-05", periods=5)) + list(pd.bdate_range("2015-02-02", periods=3)))
    g = Q.gaps(idx, min_bdays=5)
    assert len(g) == 1 and g[0][0] == pd.Timestamp("2015-01-09") and g[0][1] == pd.Timestamp("2015-02-02")


def test_top_outliers_ranked_by_return_over_prior_vol():
    idx = pd.bdate_range("2015-01-01", periods=300)
    r = pd.Series(np.random.default_rng(0).normal(0, 0.01, 300), index=idx)
    r.iloc[200] = 0.15
    c = pd.Series(100 * np.cumprod(1 + r.values), index=idx)
    top = Q.top_outliers(c, k=3)
    assert top[0]["date"] == str(idx[200].date()) and top[0]["z"] > 10
