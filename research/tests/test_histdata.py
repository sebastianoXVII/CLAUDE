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


def test_parse_fixed_est_to_utc_without_dst():
    df = H.parse_zip(_zip(SAMPLE))
    # EST fisso = UTC-5 tutto l'anno, anche d'estate (nessuna ora legale)
    assert list(df.index) == [pd.Timestamp("2024-01-02 23:00", tz="UTC"), pd.Timestamp("2024-07-02 14:30", tz="UTC")]
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df.iloc[0]["low"] == 16818.25 and df.iloc[1]["close"] == 20002.0


def test_summer_bar_maps_to_1030_new_york():
    df = H.parse_zip(_zip(SAMPLE))
    ny = df.index.tz_convert("America/New_York")
    assert ny[1].strftime("%H:%M") == "10:30"  # 09:30 EST fisso = 10:30 EDT
    assert ny[0].strftime("%H:%M") == "18:00"  # d'inverno coincide


def test_duplicates_dropped_and_sorted():
    df = H.parse_zip(_zip(SAMPLE.splitlines()[1] + "\n" + SAMPLE))
    assert df.index.is_monotonic_increasing and not df.index.duplicated().any()
