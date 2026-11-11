import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import t15_engine as E  # noqa: E402


def daily(closes, n_bars=1000, start="2015-01-01"):
    idx = pd.bdate_range(start, periods=len(closes))
    return pd.DataFrame({"close": np.asarray(closes, float), "n_bars": n_bars}, index=idx)


def test_returns_skip_days_with_few_bars():
    d = daily([100, 110, 121, 133.1])
    d.iloc[2, d.columns.get_loc("n_bars")] = 50
    r = E.returns(d)
    assert list(r.index) == [d.index[1], d.index[3]]
    assert np.isclose(r.iloc[0], 0.10) and np.isclose(r.iloc[1], 133.1 / 110 - 1)


def test_signal_v1_sign_of_252_day_return_and_nan_before():
    c = pd.Series(np.r_[np.full(252, 100.0), 101.0, 99.0], index=pd.bdate_range("2015-01-01", periods=254))
    s = E.signal(c, "V1")
    assert s.iloc[:252].isna().all()
    assert s.iloc[252] == 1 and s.iloc[253] == -1


def test_signal_v2_mean_of_three_signs():
    c = pd.Series(np.linspace(100, 200, 300), index=pd.bdate_range("2015-01-01", periods=300))
    c.iloc[-1] = c.iloc[-22] - 1  # 21-day return negative, 63 and 252 positive
    s = E.signal(c, "V2")
    assert np.isclose(s.iloc[-1], 1 / 3)


def test_vol_is_ewma_com60_annualised():
    r = pd.Series(0.01, index=pd.bdate_range("2015-01-01", periods=200))
    assert np.isclose(E.ewma_vol(r).iloc[-1], 0.01 * np.sqrt(261))


def test_positions_scale_and_cap():
    sig = pd.Series([1.0, -1.0, 1.0])
    vol = pd.Series([0.20, 0.40, 0.05])
    p = E.positions(sig, vol)
    assert list(p) == [2.0, -1.0, 4.0]


def test_instrument_pnl_uses_previous_position_costs_on_change_and_financing():
    idx = pd.bdate_range("2015-01-01", periods=4)
    pos = pd.Series([np.nan, 1.0, 1.0, -1.0], index=idx)
    r = pd.Series([0.0, 0.02, 0.01, -0.03], index=idx)
    out = E.instrument_pnl(pos, r, cost=0.0002, fin=0.03)
    # day 2: held 1.0 from day 1 -> +0.01 minus financing; day 3: +0.03 (short from day 3 applies from day 4)
    assert np.isclose(out["gross"].iloc[2], 0.01) and np.isclose(out["gross"].iloc[3], -0.03)
    assert np.isclose(out["tcost"].iloc[1], 1.0 * 0.0001) and np.isclose(out["tcost"].iloc[3], 2.0 * 0.0001)
    assert np.isclose(out["fcost"].iloc[2], 0.03 / 252)


def test_portfolio_equal_weight_over_available_instruments():
    idx = pd.bdate_range("2015-01-01", periods=3)
    a = pd.DataFrame({"gross": [0.0, 0.02, 0.02], "tcost": 0.0, "fcost": 0.0, "avail": [True, True, True]}, index=idx)
    b = pd.DataFrame({"gross": [0.0, 0.0, 0.04], "tcost": 0.0, "fcost": 0.0, "avail": [False, False, True]}, index=idx)
    p = E.portfolio({"A": a, "B": b}, cost_mult=1.0)
    assert np.isclose(p.iloc[1], 0.02) and np.isclose(p.iloc[2], 0.03)


def test_instrument_leaves_portfolio_after_its_last_data_day():
    idx = pd.bdate_range("2015-01-01", periods=4)
    a = pd.DataFrame({"gross": [0.0, 0.01, 0.01, 0.01], "tcost": 0.0, "fcost": 0.0, "avail": True}, index=idx)
    b = pd.DataFrame({"gross": [0.0, 0.03], "tcost": 0.0, "fcost": 0.0, "avail": True}, index=idx[:2])
    p = E.portfolio({"A": a, "B": b})
    assert np.isclose(p.iloc[1], 0.02) and np.isclose(p.iloc[3], 0.01)
