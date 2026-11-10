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
