"""Test del downloader Alpaca (scritti prima dell'implementazione)."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data"))
import alpaca as A  # noqa: E402


def page(sym, bars, token=None):
    return {"bars": {sym: bars}, "next_page_token": token}


B1 = {"t": "2016-01-04T14:30:00Z", "o": 200.49, "h": 200.53, "l": 200.26, "c": 200.41, "v": 2498430, "n": 4672, "vw": 200.46}
B2 = {"t": "2016-01-04T14:31:00Z", "o": 200.405, "h": 200.436, "l": 200.205, "c": 200.3151, "v": 850216, "n": 3744, "vw": 200.28}


def test_parse_page_builds_utc_ohlcv_frame():
    df = A.parse_page(page("SPY", [B1, B2]), "SPY")
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert str(df.index.tz) == "UTC"
    assert df.index[0] == pd.Timestamp("2016-01-04 14:30", tz="UTC")
    assert df["close"].iloc[1] == 200.3151


def test_parse_page_empty_or_missing_symbol():
    assert A.parse_page({"bars": {}, "next_page_token": None}, "SPY").empty
    assert A.parse_page({"bars": None, "next_page_token": None}, "SPY").empty


def test_fetch_follows_pagination_until_token_is_none():
    calls = []

    def fake_get(params):
        calls.append(dict(params))
        if "page_token" not in params:
            return page("SPY", [B1], token="abc")
        assert params["page_token"] == "abc"
        return page("SPY", [B2], token=None)

    df = A.fetch("SPY", "2016-01-04", "2016-01-05", get=fake_get)
    assert len(df) == 2 and len(calls) == 2
    assert calls[0]["feed"] == "sip" and calls[0]["adjustment"] == "all" and calls[0]["timeframe"] == "1Min"


def test_fetch_drops_duplicate_timestamps_and_sorts():
    def fake_get(params):
        return page("SPY", [B2, B1, B1], token=None)

    df = A.fetch("SPY", "2016-01-04", "2016-01-05", get=fake_get)
    assert len(df) == 2 and df.index.is_monotonic_increasing
