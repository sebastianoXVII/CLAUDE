import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data"))
import histdata as H  # noqa: E402

SAMPLE = ("20240102 180000;16820.5;16825.0;16818.25;16822.75;0\n"
          "20240702 093000;20001.0;20003.0;20000.0;20002.0;0\n")


def _zip(text: str) -> bytes:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr("DAT_ASCII_NSXUSD_M1_2024.csv", text)
        z.writestr("DAT_ASCII_NSXUSD_M1_2024.txt", "status report")
    return b.getvalue()


def test_parse_new_york_wall_clock_with_dst_to_utc():
    df = H.parse_zip(_zip(SAMPLE))
    # verificato sui dati (apertura forex domenica 17:00 tutto l'anno; 15:59 identico a QQQ): orario di New York CON ora legale
    assert list(df.index) == [pd.Timestamp("2024-01-02 23:00", tz="UTC"), pd.Timestamp("2024-07-02 13:30", tz="UTC")]
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df.iloc[0]["low"] == 16818.25 and df.iloc[1]["close"] == 20002.0


def test_summer_bar_stays_0930_new_york():
    df = H.parse_zip(_zip(SAMPLE))
    ny = df.index.tz_convert("America/New_York")
    assert ny[1].strftime("%H:%M") == "09:30" and ny[0].strftime("%H:%M") == "18:00"


def test_dst_gap_and_repeated_hour_bars_dropped():
    txt = "20240310 023000;1;1;1;1;0\n20241103 013000;1;1;1;1;0\n20241103 030000;2;2;2;2;0\n"
    df = H.parse_zip(_zip(txt))
    assert list(df["close"]) == [2.0]  # 02:30 del 10/3 non esiste, 01:30 del 3/11 e' ambiguo: scartati


def test_duplicates_dropped_and_sorted():
    df = H.parse_zip(_zip(SAMPLE.splitlines()[1] + "\n" + SAMPLE))
    assert df.index.is_monotonic_increasing and not df.index.duplicated().any()
