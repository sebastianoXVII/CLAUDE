"""Converte gli zip HistData (Generic ASCII M1) in parquet UTC.
Formato riga: 'YYYYMMDD HHMMSS;open;high;low;close;volume', timestamp = inizio barra.
Fuso: la documentazione HistData dice EST fisso, ma i DATI di questa copia sono in orario di New York CON ora legale
(verificato: apertura forex domenica alle 17:00 tutto l'anno; prezzo NSXUSD alle 15:59 identico a QQQ, corr 1,000 contro 0,928 d'estate).
Le barre nell'ora inesistente (marzo) o ripetuta (novembre) si scartano.
Uso: python research/data/histdata.py OUT.parquet file1.zip [file2.zip ...]"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

COLS = ["open", "high", "low", "close", "volume"]


def parse_zip(raw: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
        df = pd.read_csv(z.open(name), sep=";", header=None, names=["ts", *COLS])
    idx = pd.DatetimeIndex(pd.to_datetime(df.pop("ts"), format="%Y%m%d %H%M%S"))
    df.index = idx.tz_localize("America/New_York", ambiguous="NaT", nonexistent="NaT")
    df = df[df.index.notna()]
    df.index = df.index.tz_convert("UTC")
    df = df[~df.index.duplicated(keep="first")].sort_index()
    return df.astype(float)


def main(out: str, files: list[str]) -> None:
    parts = [parse_zip(Path(f).read_bytes()) for f in files]
    df = pd.concat(parts).sort_index()
    df = df[~df.index.duplicated(keep="first")]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out)
    print(f"{out}: {len(df)} barre {df.index.min()} -> {df.index.max()}, volume>0: {(df['volume'] > 0).mean():.1%}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
