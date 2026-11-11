import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_t15 as R  # noqa: E402


def test_universe_and_costs_match_preregistration():
    assert len(R.INSTR) == 23
    assert R.INSTR["EURUSD"] == 1e-4 and R.INSTR["EURJPY"] == 1.5e-4 and R.INSTR["SPXUSD"] == 2e-4
    assert R.INSTR["JPXJPY"] == 3e-4 and R.INSTR["WTIUSD"] == 4e-4 and R.INSTR["XAGUSD"] == 5e-4 and R.INSTR["XAUUSD"] == 2e-4
    assert R.FIN == 0.03 and R.PERIODS == {"insample": ("2011-01-01", "2019-12-31"), "holdout": ("2020-01-01", "2024-12-31")}


def test_insample_rule():
    ok = {"p_holm": 0.001, "t_nw": 3.2, "stress_mean": 1e-5, "years_pos": 6, "years": 9}
    assert R.insample_pass(ok)
    assert not R.insample_pass({**ok, "t_nw": 3.0}) and not R.insample_pass({**ok, "p_holm": 0.06})
    assert not R.insample_pass({**ok, "stress_mean": 0.0}) and not R.insample_pass({**ok, "years_pos": 5})


def test_holdout_rule():
    ok = {"t_nw": 1.7, "stress_mean": 1e-5, "years_pos": 3, "years": 5}
    assert R.holdout_pass(ok) and not R.holdout_pass({**ok, "t_nw": 1.6}) and not R.holdout_pass({**ok, "years_pos": 2})


def test_prop_descriptives_scale_to_10pct_vol():
    r = pd.Series(np.random.default_rng(0).normal(0.0005, 0.01, 2000), index=pd.bdate_range("2011-01-03", periods=2000))
    d = R.prop_descriptives(r)
    assert np.isclose(d["vol_ann_scalata"], 0.10, atol=1e-9)
    assert d["max_dd"] < 0 and 0 <= d["quota_finestre_10_giorni_borsa_positive"] <= 1


def _fake(tmp, sym, n=800, start="2010-01-04"):
    idx = pd.bdate_range(start, periods=n)
    px = 100 * np.exp(np.cumsum(np.random.default_rng(abs(hash(sym)) % 1000).normal(0, 0.01, n)))
    pd.DataFrame({"open": px, "high": px, "low": px, "close": px, "n_bars": 1000}, index=idx).to_parquet(tmp / f"{sym}_1d.parquet")


def test_load_truncates_at_period_end(tmp_path, monkeypatch):
    _fake(tmp_path, "EURUSD")
    monkeypatch.setattr(R, "DAILY", tmp_path)
    d = R.load("EURUSD", "2011-06-30")
    assert d.index.max() <= pd.Timestamp("2011-06-30")


def test_stages_guarded(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "OUT", tmp_path)
    with pytest.raises(SystemExit, match="insample"):
        R.main(["holdout"])
    (tmp_path / "T15_insample.started").write_text("x")
    with pytest.raises(SystemExit, match="lock"):
        R.main(["insample"])


def test_insample_end_to_end_on_synthetic(tmp_path, monkeypatch):
    for s in ("EURUSD", "XAUUSD"):
        _fake(tmp_path, s, n=2600)
    monkeypatch.setattr(R, "DAILY", tmp_path)
    monkeypatch.setattr(R, "OUT", tmp_path)
    monkeypatch.setattr(R, "INSTR", {"EURUSD": 1e-4, "XAUUSD": 2e-4})
    R.main(["insample"])
    res = json.loads((tmp_path / "T15_insample.json").read_text())
    assert set(res["varianti"]) == {"V1", "V2"} and "p_holm" in res["varianti"]["V1"]
    assert res["strumenti_usati"] == ["EURUSD", "XAUUSD"]


def test_preflight_refuses_missing_files_before_lock(tmp_path, monkeypatch):
    _fake(tmp_path, "EURUSD", n=2600)
    monkeypatch.setattr(R, "DAILY", tmp_path)
    monkeypatch.setattr(R, "OUT", tmp_path)
    monkeypatch.setattr(R, "INSTR", {"EURUSD": 1e-4, "XAUUSD": 2e-4})
    with pytest.raises(SystemExit, match="XAUUSD"):
        R.main(["insample"])
    assert not (tmp_path / "T15_insample.started").exists()


def test_preflight_refuses_short_coverage(tmp_path, monkeypatch):
    _fake(tmp_path, "EURUSD", n=600)  # finisce nel 2012
    monkeypatch.setattr(R, "DAILY", tmp_path)
    monkeypatch.setattr(R, "OUT", tmp_path)
    monkeypatch.setattr(R, "INSTR", {"EURUSD": 1e-4})
    with pytest.raises(SystemExit, match="copertura"):
        R.main(["insample"])
    assert not (tmp_path / "T15_insample.started").exists()


def test_holdout_coverage_exceptions_declared():
    assert R.min_end("ETXEUR", "holdout") is None
    assert R.min_end("WTIUSD", "holdout") == pd.Timestamp("2023-11-30")
    assert R.min_end("EURUSD", "holdout") == pd.Timestamp("2024-11-30")
    assert R.min_end("ETXEUR", "insample") == pd.Timestamp("2019-06-30")
