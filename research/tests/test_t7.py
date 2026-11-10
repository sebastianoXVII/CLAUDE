import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_t7 as R7  # noqa: E402


def test_proxy_ok_requires_both_thresholds():
    assert R7.proxy_ok({"accordo_giorni": 0.90, "corr_pnl_giornaliero": 0.90})
    assert not R7.proxy_ok({"accordo_giorni": 0.899, "corr_pnl_giornaliero": 0.99})
    assert not R7.proxy_ok({"accordo_giorni": 0.99, "corr_pnl_giornaliero": 0.899})


def test_outcome_three_way():
    ok = {"t>3": True, "stress2x>0": True, "MNQ>0": True, "anni>=2/3": True}
    assert R7.outcome(3.2, ok) == "CONFERMATO"
    assert R7.outcome(3.2, {**ok, "anni>=2/3": False}) == "INCONCLUSIVO"
    assert R7.outcome(1.0, {**ok, "t>3": False}) == "INCONCLUSIVO"
    assert R7.outcome(-0.1, {**ok, "t>3": False}) == "MORTO"


def test_uses_histdata_file_and_test_end():
    assert R7.FILE.name == "NSXUSD_1m_24h.parquet"
    assert R7.TEST_END == "2016-12-31"


import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
import t1_engine as T1  # noqa: E402

TZ = "America/New_York"


def _synthetic_nsx(path):
    sessions = [d for d in T1._XNYS.sessions if pd.Timestamp("2010-11-15") <= d <= pd.Timestamp("2011-01-31")]
    idx = []
    for d in sessions:
        idx += list(pd.date_range(f"{d.date()} 09:30", f"{d.date()} 15:59", freq="1min", tz=TZ))
    idx += list(pd.date_range("2011-01-17 09:30", "2011-01-17 11:59", freq="1min", tz=TZ))  # MLK: barre parziali
    idx = pd.DatetimeIndex(sorted(idx))
    rng = np.random.default_rng(0)
    px = 2000 + np.cumsum(rng.normal(0, 0.5, len(idx)))
    pd.DataFrame({"open": px, "high": px + 0.2, "low": px - 0.2, "close": px, "volume": 0.0},
                 index=idx.tz_convert("UTC")).to_parquet(path)


def test_day_after_holiday_with_partial_bars_is_armed_with_last_session_close(tmp_path, monkeypatch):
    f = tmp_path / "NSXUSD_1m_24h.parquet"
    _synthetic_nsx(f)
    monkeypatch.setattr(R7, "FILE", f)
    prof = pd.Series(1.0, index=[t.strftime("%H:%M") for t in pd.date_range("2000-01-01 09:30", "2000-01-01 15:59", freq="1min")])
    _tr, armed, days = R7.trades(0.45, prof)
    assert pd.Timestamp("2011-01-18") in armed
    assert pd.Timestamp("2011-01-17") not in days


def test_year_sums_merge_short_years_and_keep_unrounded_values():
    idx = pd.DatetimeIndex(list(pd.bdate_range("2010-12-07", periods=17)) + list(pd.bdate_range("2011-01-03", periods=100)))
    daily = pd.Series(0.0, index=idx)
    daily.iloc[0] = -1.0
    daily.iloc[20] = 1.04
    ys = R7.year_sums(daily)
    assert list(ys) == [2011]
    assert np.isclose(ys[2011], 0.04) and ys[2011] > 0


def test_proxy_ok_checks_profile_hash_when_given():
    chk = {"accordo_giorni": 0.95, "corr_pnl_giornaliero": 0.95, "hash_profilo": "abc"}
    assert R7.proxy_ok(chk, "abc")
    assert not R7.proxy_ok(chk, "xyz")


def test_profile_hash_is_deterministic_and_sensitive():
    p = pd.Series([1.0, 2.0], index=["09:30", "09:31"])
    assert R7.profile_hash(p) == R7.profile_hash(p.copy())
    assert R7.profile_hash(p) != R7.profile_hash(p * 2)


def test_main_refuses_without_proxy_check(tmp_path, monkeypatch):
    f = tmp_path / "x.parquet"
    f.write_bytes(b"")
    monkeypatch.setattr(R7, "OUT", tmp_path)
    monkeypatch.setattr(R7, "FILE", f)
    monkeypatch.setattr(R7, "PROXY_FILE", tmp_path / "T7_proxy_check.json")
    with pytest.raises(SystemExit, match="proxy"):
        R7.main()
    assert not (tmp_path / "T7_risultati.json").exists()


def test_qqq_profile_respects_date_bounds(tmp_path, monkeypatch):
    idx = pd.DatetimeIndex([pd.Timestamp("2016-06-01 09:30", tz=TZ), pd.Timestamp("2022-06-01 09:30", tz=TZ)])
    pd.DataFrame({"open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": [10.0, 99.0]},
                 index=idx.tz_convert("UTC")).to_parquet(tmp_path / "QQQ_1m_raw.parquet")
    monkeypatch.setattr(R7, "BARS", tmp_path)
    assert R7.qqq_profile()["09:30"] == 54.5
    assert R7.qqq_profile("2021-01-01", "2025-01-01")["09:30"] == 99.0


def test_compare_reports_agreement_corr_and_traded_days_only():
    import run_t7_proxy_check as P
    days = pd.to_datetime(["2018-01-02", "2018-01-03", "2018-01-04", "2018-01-05"])
    a = pd.DataFrame({"date": days[:2], "entry_time": ["10:00", "10:00"], "side": [1, 1], "exit_time": ["16:00", "16:00"],
                      "net_pts": [1.0, 2.0]})
    b = a.copy()
    b.loc[1, "exit_time"] = "12:00"
    r = P.compare(a, b, days, "2018-01-01", "2018-12-31")
    assert r["n_giorni"] == 4 and r["n_giorni_con_trade"] == 2
    assert np.isclose(r["accordo_giorni"], 0.75) and np.isclose(r["accordo_solo_giorni_con_trade"], 0.5)
    assert np.isclose(r["corr_pnl_giornaliero"], 1.0)
