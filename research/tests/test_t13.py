import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_t13 as R  # noqa: E402

BASE = {"t_nw": 3.5, "p_holm": 0.01, "stress2x_media_pt": 0.1, "anni_positivi": "10/14", "n_trades": 200}


def test_survives_is_requires_every_criterion():
    assert R.survives_is(BASE)
    for k, bad in (("t_nw", 2.9), ("p_holm", 0.06), ("stress2x_media_pt", -0.01), ("anni_positivi", "9/14"), ("n_trades", 149)):
        assert not R.survives_is({**BASE, k: bad}), k


def test_holdout_short_sample_is_inconclusive():
    m = {"t_nw": 2.5, "stress2x_media_pt": 0.1}
    assert R.survives_ho(m, 199) == "INCONCLUSIVO"
    assert R.survives_ho(m, 250) == "SOPRAVVIVE"
    assert R.survives_ho({**m, "t_nw": 1.0}, 250) == "MORTO"


def test_renamer_maps_strategy_name():
    got = []

    class J:
        def add(self, r):
            got.append(r)

    R._Renamer(J()).add({"strategy": "T8_H8a", "instrument": "EURUSD"})
    assert got[0]["strategy"] == "T13_EURUSD_H8a"
