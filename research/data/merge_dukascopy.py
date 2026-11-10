"""Unisce i file annuali di Dukascopy (branch data-dukascopy) in un unico parquet 24h.
Uso: python3 research/data/merge_dukascopy.py USATECHIDXUSD"""
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def main(sym: str) -> None:
    tmp = ROOT / "data" / "dukascopy_branch"
    tmp.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(ROOT), "fetch", "-q", "origin", "data-dukascopy"], check=True)
    files = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "--name-only", "origin/data-dukascopy", "dukascopy/"],
                           check=True, capture_output=True, text=True).stdout.split()
    frames = []
    for f in sorted(x for x in files if Path(x).name.startswith(sym + "_")):
        out = tmp / Path(f).name
        out.write_bytes(subprocess.run(["git", "-C", str(ROOT), "show", f"origin/data-dukascopy:{f}"], check=True, capture_output=True).stdout)
        frames.append(pd.read_parquet(out))
    df = pd.concat(frames).sort_index()
    df = df[~df.index.duplicated()]
    dst = ROOT / "data" / "bars" / f"{sym}_1m_24h.parquet"
    df.to_parquet(dst)
    print(f"{sym}: {len(files)} file, {len(df)} barre {df.index.min()} -> {df.index.max()} -> {dst}")


if __name__ == "__main__":
    main(sys.argv[1])
