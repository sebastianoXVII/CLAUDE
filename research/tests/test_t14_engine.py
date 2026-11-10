import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import t14_engine as E  # noqa: E402

TZ = "America/New_York"


def bars(stamps, closes):
    idx = pd.DatetimeIndex([pd.Timestamp(s, tz=TZ) for s in stamps])
    return pd.DataFrame({"open": closes, "high": closes, "low": closes, "close": closes}, index=idx)


def test_config_counts_match_preregistration():
    assert len(E.configs("index")) == 396
    assert len(E.configs("fx")) == 828
    assert len(E.eh_pairs("index")) == 44 and len(E.eh_pairs("fx")) == 92


def test_index_close_hold_only_when_more_than_120_minutes_left():
    pairs = E.eh_pairs("index")
    assert (13 * 60 + 30, "close") in pairs and (14 * 60, "close") not in pairs
    assert (15 * 60 + 30, 30) in pairs and (15 * 60 + 30, 60) not in pairs


def test_fx_exit_not_after_1630():
    pairs = E.eh_pairs("fx")
    assert (14 * 60 + 30, 120) in pairs and (15 * 60, 120) not in pairs and (15 * 60 + 30, 60) not in pairs


def test_price_grid_uses_last_bar_between_t_minus_5_and_t_minus_1():
    b = bars(["2015-03-02 09:25", "2015-03-02 09:29", "2015-03-02 09:30", "2015-03-02 09:52"], [1.0, 2.0, 3.0, 4.0])
    g = E.price_grid(b, pd.DatetimeIndex(["2015-03-02"]), [570, 600])  # 09:30, 10:00
    assert g.loc["2015-03-02", 570] == 2.0          # bar 09:30 not yet known at 09:30
    assert np.isnan(g.loc["2015-03-02", 600])       # last bar 09:52 -> stale (>5 min)


def test_price_grid_negative_offset_is_previous_day():
    b = bars(["2015-03-01 17:59"], [7.0])
    g = E.price_grid(b, pd.DatetimeIndex(["2015-03-02"]), [-360])  # 18:00 previous day
    assert g.loc["2015-03-02", -360] == 7.0


def test_daily_pnl_seasonality_and_momentum_sign_and_cost():
    days = pd.DatetimeIndex(["2015-03-02", "2015-03-03"])
    grid = pd.DataFrame({540: [100.0, 100.0], 570: [101.0, 99.0], 600: [103.0, 98.0]}, index=days)
    s = E.daily_gross({"family": "S", "E": 570, "H": 30, "L": None}, grid, anchor=None)
    assert list(s) == [2.0, -1.0]
    m = E.daily_gross({"family": "M", "E": 570, "H": 30, "L": 30}, grid, anchor=None)
    assert list(m) == [2.0, 1.0]  # long after up move (+2), short after down move (+1)
    net = E.net(m, d=1, cost=0.5)
    assert list(net) == [1.5, 0.5]
    assert list(E.net(m, d=-1, cost=0.5)) == [-2.5, -1.5]


def test_no_trade_is_zero_not_cost():
    days = pd.DatetimeIndex(["2015-03-02"])
    grid = pd.DataFrame({540: [100.0], 570: [100.0], 600: [103.0]}, index=days)
    m = E.daily_gross({"family": "M", "E": 570, "H": 30, "L": 30}, grid, anchor=None)
    assert np.isnan(m.iloc[0])          # r_L == 0 -> no trade
    assert E.net(m, d=1, cost=0.5).iloc[0] == 0.0


def test_close_hold_and_anchor_lookback():
    days = pd.DatetimeIndex(["2015-03-02"])
    grid = pd.DataFrame({-480: [90.0], 570: [100.0], 960: [95.0]}, index=days)
    m = E.daily_gross({"family": "M", "E": 570, "H": "close", "L": "anchor"}, grid, anchor=-480)
    assert m.iloc[0] == -5.0  # up since prev 16:00 -> long, exit at 16:00


def test_conditioning_uses_only_strictly_prior_60_days():
    n = 80
    days = pd.bdate_range("2015-01-01", periods=n)
    r = np.full(n, 0.01)
    r[70] = 0.05   # big move today
    r[75] = 0.005  # small move
    grid = pd.DataFrame({540: 100.0, 570: 100.0 * (1 + r), 600: 100.0 * (1 + r) + 1}, index=days)
    big = E.big_move_mask(grid, {"family": "MC", "E": 570, "H": 30, "L": 30}, anchor=None)
    assert not big.iloc[:40].any()           # fewer than 40 prior observations
    assert big.iloc[70] and not big.iloc[75]
    grid2 = grid.copy()
    grid2.iloc[71:, :] = grid2.iloc[71:, :] * 5  # future changes must not affect day 70
    assert E.big_move_mask(grid2, {"family": "MC", "E": 570, "H": 30, "L": 30}, anchor=None).iloc[70]


def test_year_merge_and_positive_share():
    idx = pd.DatetimeIndex(list(pd.bdate_range("2010-12-01", periods=20)) + list(pd.bdate_range("2011-01-03", periods=100)))
    x = pd.Series(0.0, index=idx)
    x.iloc[0] = -1.0
    x.iloc[30] = 2.0
    assert E.year_sums(x) == {2011: 1.0}


def test_stage1_rule():
    good = {"t_nw": 3.1, "stress_mean": 0.1, "n_trades": 150, "years_pos": 5, "years": 7}
    assert E.stage1_pass(good)
    assert not E.stage1_pass({**good, "t_nw": 3.0})
    assert not E.stage1_pass({**good, "stress_mean": 0.0})
    assert not E.stage1_pass({**good, "n_trades": 149})
    assert not E.stage1_pass({**good, "years_pos": 4})


def test_price_grid_wall_clock_on_monday_after_dst_change():
    # domenica 2015-03-08 cambio ora: lunedi' l'ancora delle 18:10 di domenica e le 10:00 restano ore di parete
    b = bars(["2015-03-08 18:08", "2015-03-09 09:58"], [4.0, 5.0])
    g = E.price_grid(b, pd.DatetimeIndex(["2015-03-09"]), [-350, 600])
    assert g.loc["2015-03-09", -350] == 4.0 and g.loc["2015-03-09", 600] == 5.0


def test_tolerance_edges_t_minus_5_in_t_minus_6_out():
    d = pd.DatetimeIndex(["2015-03-02"])
    assert E.price_grid(bars(["2015-03-02 09:55"], [1.0]), d, [600]).iloc[0, 0] == 1.0
    assert np.isnan(E.price_grid(bars(["2015-03-02 09:54"], [1.0]), d, [600]).iloc[0, 0])


def test_anchors_per_amendment_1():
    assert E.ANCHOR == {"index": "prev_close", "fx": -350}
    assert all(isinstance(o, int) for o in E.offsets("index")) and min(E.offsets("index")) >= 450
    assert -350 in E.offsets("fx")
