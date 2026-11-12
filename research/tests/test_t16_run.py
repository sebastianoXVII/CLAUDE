import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_t16 as R  # noqa: E402

TZ = "America/New_York"


def test_parameters_match_preregistration():
    e, g, x = R.INSTR["EURUSD"], R.INSTR["GBPUSD"], R.INSTR["XAUUSD"]
    assert (e["cost"], g["cost"], x["cost"]) == (0.00010, 0.00013, 0.35)
    assert (e["scale"], e["D"], e["delta"]) == (10000, 0.0020, 0.0005) and g["D"] == 0.0020
    assert (x["scale"], x["D"], x["delta"]) == (100, 3.0, 1.0)
    assert (e["A"], e["B"], e["C"]) == ((100, ()), (50, (100,)), (25, (50,)))
    assert (x["A"], x["B"], x["C"]) == ((5000, ()), (1000, (5000,)), (500, (1000,)))
    assert R.PERIODS == {"insample": ("2010-01-01", "2019-12-31"), "holdout": ("2020-01-01", "2024-12-31")}


def test_twelve_tests():
    k = R.test_keys()
    assert len(k) == 12 and "XAUUSD_B_S" in k and not any("_C_" in x for x in k)


def _m(**kw):
    m = dict(t_nw=3.5, p_holm=0.01, stress_mean=1e-5, years_pos=6, n_trades=200)
    m.update(kw)
    return m


def test_insample_rule_edges():
    assert R.insample_pass(_m())
    assert not R.insample_pass(_m(t_nw=3.0))
    assert not R.insample_pass(_m(p_holm=0.05))
    assert not R.insample_pass(_m(stress_mean=0.0))
    assert not R.insample_pass(_m(years_pos=5))
    assert not R.insample_pass(_m(n_trades=199))
    assert not R.insample_pass(_m(t_nw=float("nan")))


def test_holdout_rule_edges():
    assert R.holdout_pass(dict(t_nw=1.7, stress_mean=1e-6, years_pos=3))
    assert not R.holdout_pass(dict(t_nw=1.65, stress_mean=1e-6, years_pos=3))
    assert not R.holdout_pass(dict(t_nw=2.0, stress_mean=-1e-6, years_pos=3))
    assert not R.holdout_pass(dict(t_nw=2.0, stress_mean=1e-6, years_pos=2))


def _synthetic(path, start="2015-03-02", ndays=80, seed=0):
    """EURUSD sintetico: ogni giorno base 1.0975, tocco di 1.1000 alle 10:00 e rientro con rumore."""
    rng = np.random.default_rng(seed)
    frames = []
    for d in pd.bdate_range(start, periods=ndays):
        idx = pd.date_range(pd.Timestamp(d, tz=TZ) - pd.Timedelta(hours=7), periods=1440, freq="min")
        p = np.full(1440, 1.0975)
        f = pd.DataFrame({"open": p, "high": p.copy(), "low": p.copy(), "close": p.copy(), "volume": 0.0}, index=idx)
        t = pd.Timestamp(d, tz=TZ) + pd.Timedelta(hours=10)
        f.loc[t, ["high", "close"]] = [1.1001, 1.0999]
        ex = t + pd.Timedelta(minutes=60)
        v = 1.0975 + rng.normal(0, 0.0008)
        f.loc[ex, ["high", "low", "close"]] = [max(v, 1.0975), min(v, 1.0975), v]
        frames.append(f)
    b = pd.concat(frames)
    b.index = b.index.tz_convert("UTC")
    b.to_parquet(path / "EURUSD_1m_24h.parquet")
    return b


def test_load_truncates_by_trading_day(tmp_path, monkeypatch):
    _synthetic(tmp_path, ndays=10)
    monkeypatch.setattr(R, "BARS", tmp_path)
    b = R.load("EURUSD", "2015-03-06")
    assert b.index.tz.key == TZ
    assert b.index.max() == pd.Timestamp("2015-03-06 16:59", tz=TZ)


def test_guards_and_lock(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "OUT", tmp_path)
    with pytest.raises(SystemExit, match="insample"):
        R.main(["holdout"])
    (tmp_path / "T16_insample.started").write_text("x")
    with pytest.raises(SystemExit, match="lock"):
        R.main(["insample"])


def test_preflight_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "BARS", tmp_path)
    monkeypatch.setattr(R, "OUT", tmp_path)
    with pytest.raises(SystemExit, match="manca"):
        R.main(["insample"])
    assert not (tmp_path / "T16_insample.started").exists()


def test_end_to_end_synthetic(tmp_path, monkeypatch):
    _synthetic(tmp_path)
    monkeypatch.setattr(R, "BARS", tmp_path)
    monkeypatch.setattr(R, "OUT", tmp_path)
    monkeypatch.setattr(R, "INSTR", {"EURUSD": R.INSTR["EURUSD"]})
    monkeypatch.setattr(R, "COVERAGE", {"insample": ("2015-03-31", "2015-04-01")})
    R.main(["insample"])
    res = json.loads((tmp_path / "T16_insample.json").read_text())
    a = res["test"]["EURUSD_A_R"]
    assert a["n_trades"] == 80 and a["t_nw"] > 0 and "p_holm" in a
    assert res["test"]["EURUSD_B_R"]["n_trades"] == 0
    assert "EURUSD_R" in res["controlli"] and "welch_t_A_vs_C" in res["controlli"]["EURUSD_R"]
    assert (tmp_path / "T16_insample.started").exists()


def test_level_state_resets_at_trading_day_boundary():
    """Focus 5: armamento alle 16:00 del giorno 1, tocco alle 03:00 del giorno 2 -> nessun trade."""
    frames = []
    for d, base in (("2015-03-05", 1.0975), ("2015-03-06", 1.0990)):   # giorno 2: mai armato (close > 1.0980)
        idx = pd.date_range(pd.Timestamp(d, tz=TZ) - pd.Timedelta(hours=7), periods=1440, freq="min")
        p = np.full(1440, base)
        frames.append(pd.DataFrame({"open": p, "high": p.copy(), "low": p.copy(), "close": p.copy()}, index=idx))
    b = pd.concat(frames)
    t = pd.Timestamp("2015-03-06 03:00", tz=TZ)
    b.loc[t, ["high", "close"]] = [1.1001, 1.0995]
    tr = R.trades_all(b, "EURUSD")
    assert len(tr[("A", "R")]) == 0
    b2 = b.copy()
    b2.loc[pd.Timestamp("2015-03-06 02:00", tz=TZ), "close"] = 1.0975          # armamento nello stesso giorno
    assert len(R.trades_all(b2, "EURUSD")[("A", "R")]) == 1
