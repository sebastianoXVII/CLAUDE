import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_t14 as R  # noqa: E402

TZ = "America/New_York"


def _bars(day, start, end):
    idx = pd.date_range(f"{day} {start}", f"{day} {end}", freq="1min", tz=TZ)
    return pd.DataFrame({"open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0}, index=idx)


def test_valid_days_index_requires_nyse_session_and_300_rth_bars():
    b = pd.concat([_bars("2015-03-02", "09:30", "15:59"), _bars("2015-03-03", "09:30", "13:00"),
                   _bars("2015-01-19", "09:30", "15:59"),  # MLK: non e' sessione NYSE
                   _bars("2015-11-27", "09:30", "15:59")])  # chiusura anticipata
    assert list(R.valid_days(b, "index")) == [pd.Timestamp("2015-03-02")]


def test_valid_days_fx_requires_768_bars_and_excludes_xmas_newyear_weekend():
    b = pd.concat([_bars("2015-03-02", "00:00", "15:59"), _bars("2015-03-03", "00:00", "12:46"),
                   _bars("2015-03-04", "00:00", "12:47"), _bars("2015-12-25", "00:00", "15:59"),
                   _bars("2015-03-07", "00:00", "15:59")])
    assert list(R.valid_days(b, "fx")) == [pd.Timestamp("2015-03-02"), pd.Timestamp("2015-03-04")]


def test_choose_direction_follows_sign_of_mean_gross():
    assert R.choose_d(pd.Series([1.0, np.nan, -0.5])) == 1
    assert R.choose_d(pd.Series([-1.0, 0.2])) == -1
    assert R.choose_d(pd.Series([np.nan])) == 1


def test_evaluate_counts_trades_stress_and_years():
    days = pd.bdate_range("2015-01-01", periods=300)
    gross = pd.Series(np.where(np.arange(300) % 2 == 0, 1.0, np.nan), index=days)
    s = R.evaluate(gross, days, d=1, cost=0.25)
    assert s["n_trades"] == 150
    assert np.isclose(s["mean_net"], 150 * 0.75 / 300)
    assert np.isclose(s["stress_mean"], 150 * 0.5 / 300)
    assert s["years"] == 2 and s["years_pos"] == 2


def test_stage2_and_stage3_rules():
    s = {"p_holm": 0.04, "stress_mean": 0.1, "years_pos": 2, "years": 4}
    assert R.stage2_pass(s)
    assert not R.stage2_pass({**s, "p_holm": 0.05}) and not R.stage2_pass({**s, "years_pos": 1})
    h = {"t_nw": 1.7, "p_holm": 0.04, "stress_mean": 0.1, "years_pos": 2, "years": 3}
    assert R.stage3_pass(h)
    assert not R.stage3_pass({**h, "t_nw": 1.6}) and not R.stage3_pass({**h, "years_pos": 1})


def test_top_k_per_instrument():
    rows = [{"inst": "A", "t_nw": t, "pass": True} for t in range(15)] + [{"inst": "B", "t_nw": 5.0, "pass": False}]
    sel = R.select(rows, k=10)
    assert len(sel) == 10 and min(r["t_nw"] for r in sel) == 5


def test_stages_refuse_out_of_order_and_rerun(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "OUT", tmp_path)
    with pytest.raises(SystemExit, match="scoperta"):
        R.main(["convalida"])
    (tmp_path / "T14_scoperta.json").write_text(json.dumps({"selezionate": []}))
    with pytest.raises(SystemExit, match="gia'"):
        R.main(["scoperta"])
    with pytest.raises(SystemExit, match="convalida"):
        R.main(["holdout"])


def test_periods_match_preregistration():
    assert R.PERIODS == {"scoperta": (None, "2017-12-31"), "convalida": ("2018-01-01", "2021-12-31"),
                         "holdout": ("2022-01-01", "2024-12-31")}


def _synthetic_index(path, start="2017-06-01", end="2018-03-31", seed=1):
    sess = [d for d in R.T1._XNYS.sessions if pd.Timestamp(start) <= d <= pd.Timestamp(end)]
    idx = []
    for d in sess:
        idx += list(pd.date_range(f"{d.date()} 07:00", f"{d.date()} 16:30", freq="1min", tz=TZ))
    idx = pd.DatetimeIndex(idx)
    px = 1000 + np.cumsum(np.random.default_rng(seed).normal(0, 0.3, len(idx)))
    pd.DataFrame({"open": px, "high": px, "low": px, "close": px, "volume": 0.0}, index=idx.tz_convert("UTC")).to_parquet(path)
    return pd.DataFrame({"close": px}, index=idx)


@pytest.fixture
def one_index(tmp_path, monkeypatch):
    b = _synthetic_index(tmp_path / "XYZ_1m_24h.parquet")
    monkeypatch.setattr(R, "BARS", tmp_path)
    monkeypatch.setattr(R, "OUT", tmp_path)
    monkeypatch.setattr(R, "INSTR", {"NQ": ("XYZ", "index", 0.45, 20.0)})
    return tmp_path, b


def test_load_truncates_after_period_end_and_adds_prev_session_close(one_index):
    tmp, b = one_index
    kind, cost, usd, days, grid = R.load("NQ", "2017-12-31")
    assert days.max() <= pd.Timestamp("2017-12-31")
    # lunedi' 2017-06-12: ancora = P(16:00) di venerdi' 2017-06-09 (ultima barra 15:59)
    assert grid.loc["2017-06-12", "prev_close"] == b.loc["2017-06-09 15:59", "close"]
    # dopo il 4 luglio (festivo): mercoledi' 07-05 -> sessione precedente lunedi' 07-03
    assert grid.loc["2017-07-05", "prev_close"] == b.loc["2017-07-03 15:59", "close"]


def test_scoperta_end_to_end_writes_guard_lock_and_refuses_rerun(one_index):
    tmp, _b = one_index
    R.main(["scoperta"])
    res = json.loads((tmp / "T14_scoperta.json").read_text())
    assert res["n_config"] == 396
    assert (tmp / "T14_scoperta_tutte.parquet").exists() and (tmp / "T14_scoperta.started").exists()
    with pytest.raises(SystemExit):
        R.main(["scoperta"])


def test_started_lock_blocks_restart_after_crash(one_index):
    tmp, _b = one_index
    (tmp / "T14_scoperta.started").write_text("x")
    with pytest.raises(SystemExit, match="avviato"):
        R.main(["scoperta"])


def test_convalida_roundtrip_with_close_and_anchor_config(one_index):
    tmp, _b = one_index
    cfg = {"inst": "NQ", "family": "M", "E": 600, "H": "close", "L": "anchor", "d": 1}
    cfg["key"] = R.key(cfg)
    (tmp / "T14_scoperta.json").write_text(json.dumps({"selezionate": [cfg]}))
    R.main(["convalida"])
    res = json.loads((tmp / "T14_convalida.json").read_text())
    assert res["n_candidate"] == 1 and res["valutate"][0]["key"] == cfg["key"] and "p_holm" in res["valutate"][0]


def test_full_grid_is_3276_configs():
    assert sum(len(R.E.configs(v[1])) for v in R.INSTR.values()) == 3276
