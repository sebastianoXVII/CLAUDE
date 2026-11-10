# Progetto: edge statistico intraday su futures indici CME, per prop firm

## Regole del committente (non negoziabili)
- Claude è il quant lead: decide in base ai dati e uccide le strategie che non superano i test. Niente accondiscendenza.
- Tutto passa da dati, statistica e test pre-registrati. Ogni numero ha una fonte, oppure è dichiarato come stima.
- Si coinvolge il committente solo per ciò che solo lui può fare: soldi, credenziali, account, decisioni di rischio.
- **Si lavora solo in cloud. Mai nulla sulla macchina locale del committente.**
- Budget: nessuna spesa senza necessità dimostrata. Preferire sempre le fonti di dati gratuite.
- Lingua delle comunicazioni e dei report: italiano.

## Skill: uso OBBLIGATORIO
Per ordine esplicito del committente, le skill in `.claude/skills/` vanno usate **sempre**:
- **superpowers** (obra/superpowers): all'inizio di ogni compito si applica `using-superpowers`, che impone di verificare e invocare ogni skill pertinente prima di agire. Le più rilevanti qui:
  - `brainstorming` prima di progettare qualcosa di nuovo;
  - `writing-plans` ed `executing-plans` per i compiti in più passi;
  - `test-driven-development` per tutto il codice di backtest e analisi;
  - `systematic-debugging` per ogni comportamento inatteso;
  - `verification-before-completion` prima di dichiarare un risultato;
  - `requesting-code-review` prima di fidarsi di un risultato statistico;
  - `dispatching-parallel-agents` per le ricerche indipendenti.
- **find-skills** (vercel-labs/skills): quando serve una capacità nuova, cercare prima una skill esistente e verificarne reputazione e codice prima di installarla. Registrare la provenienza in `.claude/skills/PROVENANCE.md`.

## Struttura
- `reports/`: report di ricerca (mappa dell'edge).
- `research_notes/`: note di ricerca con le fonti.
- `research/preregistration/`: ipotesi congelate PRIMA di vedere i risultati. Non modificarle: si crea una nuova versione.
- `research/data/`: downloader. I dati vanno in `data/` (gitignored, si riscaricano).
- `research/tests/`: motori dei test statistici. `research/results/`: risultati.

## Disciplina statistica
- t > 3 sul P&L giornaliero netto, correzione per test multipli, hold-out mai toccato prima del verdetto in-sample.
- Costi reali di ES/NQ e MES/MNQ, con stress test a 2×.
- Una strategia che fallisce i criteri pre-registrati è morta: non si ritoccano i parametri per salvarla.
