"""Converte gli zip HistData M1 in barre GIORNALIERE con giornata che chiude alle 17:00 di New York (convenzione forex).
La barra del giorno D contiene i minuti da D-1 17:00 a D 16:59 ET (i minuti di domenica sera vanno nel lunedi').
Uso: python research/data/histdata_daily.py OUT.parquet file1.zip [file2.zip ...]
     python research/data/histdata_daily.py --from-m1 M1_UTC.parquet OUT.parquet  (stessa conversione da un parquet M1 in UTC)"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import histdata as H  # noqa: E402

TZ = "America/New_York"


def to_daily(m1_utc: pd.DataFrame) -> pd.DataFrame:
    et = m1_utc.index.tz_convert(TZ)
    day = pd.DatetimeIndex((et + pd.Timedelta(hours=7)).date)
    g = m1_utc.groupby(day)
    d = pd.DataFrame({"open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(),
                      "close": g["close"].last(), "n_bars": g["close"].size()})
    d.index.name = "date"
    return d[d.index.weekday < 5]


def _write(m1: pd.DataFrame, out: str) -> None:
    m1 = m1[~m1.index.duplicated(keep="first")].sort_index()
    d = to_daily(m1)
    d.to_parquet(out)
    print(f"{out}: {len(d)} giorni, {d.index.min().date()} -> {d.index.max().date()}")


def main(out: str, files: list[str]) -> None:
    _write(pd.concat([H.parse_zip(Path(f).read_bytes()) for f in files]), out)


def from_m1(src: str, out: str) -> None:
    _write(pd.read_parquet(src), out)


if __name__ == "__main__":
    if sys.argv[1] == "--from-m1":
        from_m1(sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2:])
