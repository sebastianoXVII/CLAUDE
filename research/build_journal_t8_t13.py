"""Secondo passaggio: diario e screenshot dei trade in-sample di T8 (NQ) e T13 (EURUSD, GBPUSD, XAUUSD).
Stesso codice e stessi trade dei verdetti; non scrive né modifica i file dei risultati."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t8 as R8  # noqa: E402
import run_t13 as R13  # noqa: E402
from lab import journal  # noqa: E402

jr = journal.Journal(R8.OUT / "journal.sqlite")
which = sys.argv[1:] or ["T8", "T13"]
if "T8" in which:
    for h in R8.HYP:
        jr.clear_strategy(f"T8_{h}")
    R8.run("NQ", "IS", jr=jr)
    print("T8 diario fatto", flush=True)
if "T13" in which:
    R8.INSTR, R8.CHARTS = R13.INSTR, R13.CHARTS
    for inst in R13.INSTR:
        for h in R8.HYP:
            jr.clear_strategy(f"T13_{inst}_{h}")
        R13._run(inst, "IS", jr=R13._Renamer(jr))
        print(f"T13 {inst} diario fatto", flush=True)
