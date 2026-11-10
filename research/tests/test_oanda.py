"""Test del downloader OANDA v20 (candele M1). Scritti prima del codice; nessuna chiamata di rete."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data"))
import oanda as O  # noqa: E402


def candle(t, o, h, l, c, v=10, complete=True):
    return {"time": t, "volume": v, "complete": complete, "mid": {"o": str(o), "h": str(h), "l": str(l), "c": str(c)}}


def test_parse_candles_to_utc_ohlcv_and_drop_incomplete():
    payload = {"candles": [candle("2012-03-01T14:30:00.000000000Z", 2600, 2601, 2599, 2600.5),
                           candle("2012-03-01T14:31:00.000000000Z", 2600.5, 2602, 2600, 2601.75),
                           candle("2012-03-01T14:32:00.000000000Z", 1, 1, 1, 1, complete=False)]}
    df = O.parse(payload)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 2 and str(df.index.tz) == "UTC"
    assert df.index[1] == pd.Timestamp("2012-03-01 14:31", tz="UTC") and df["close"].iloc[1] == 2601.75


def test_fetch_paginates_from_last_time_until_end():
    calls = []

    def fake_get(params):
        calls.append(dict(params))
        if len(calls) == 1:
            return {"candles": [candle("2012-03-01T14:30:00.000000000Z", 1, 1, 1, 1),
                                candle("2012-03-01T14:31:00.000000000Z", 2, 2, 2, 2)]}
        if len(calls) == 2:
            assert params["from"].startswith("2012-03-01T14:31")
            return {"candles": [candle("2012-03-01T14:31:00.000000000Z", 2, 2, 2, 2),
                                candle("2012-03-01T14:32:00.000000000Z", 3, 3, 3, 3)]}
        return {"candles": []}

    df = O.fetch("NAS100_USD", "2012-03-01T14:30:00Z", "2012-03-01T14:33:00Z", get=fake_get, count=2)
    assert list(df["close"]) == [1, 2, 3]
    assert calls[0]["granularity"] == "M1" and calls[0]["price"] == "M"
