# T14 — Ricerca sistematica su 5 mercati (3.276 configurazioni): **MORTO**

**Data:** 2026-11-10. **Pre-registrazione:** `research/preregistration/T14_ricerca_sistematica.md`, con l'emendamento 1 registrato prima di qualsiasi calcolo. **Dati:** `T14_scoperta.json`, `T14_scoperta_tutte.parquet` (tutte le configurazioni), `T14_convalida.json`. Codice con TDD (173 test) e due code review indipendenti prima dell'esecuzione.

## Esito
| Stadio | Periodo | Risultato |
|---|---|---|
| 1. Scoperta | 2010 → 2017 | **15 / 3.276 passano** (t > 3 netto, stress 2× > 0, ≥ 150 trade, ≥ 2/3 anni). Sotto H0 se ne attendevano **8,8**. Tutti su EURUSD (11) e GBPUSD (4); **0 su NQ, ES e XAUUSD**. Al massimo 10 per strumento → 14 in convalida. |
| 2. Convalida | 2018 → 2021 | **0 / 14 sopravvivono.** Il migliore ha t = +1,01 (GBPUSD MC 11:00 H120), con p di Holm = 1. |
| 3. Hold-out | 2022 → 2024 | **Non calcolato**: nessun sopravvissuto. Resta intatto. |

## Il caso più istruttivo: un'anomalia che si è spenta
Il primo della scoperta è EURUSD, entrata alle 12:30 ET, uscita dopo 30 minuti, **contro** il movimento dalle 18:10 del giorno prima.
- **Scoperta 2010–2017:** t = +6,7.
- **Convalida 2018–2021:** t = −7,1.

Con un controllo diagnostico sui soli anni già visti (2010–2021) si vede che **non è un difetto dei dati**: è un'anomalia che decade.

Profitto lordo dell'inversione, in pip al giorno:

| Anno | Pip al giorno |
|---|---|
| 2010 | 4,8 |
| 2011 | 5,4 |
| 2012–2016 | 1–2,7 |
| 2017 | 0,8 |
| 2018–2021 | circa 0, con segno opposto (da −0,9 a +0,2) |

La strategia opera ogni giorno e paga 1 pip a ogni trade, quindi quando l'effetto sparisce il netto diventa negativo in modo molto significativo. È il destino tipico delle anomalie pubblicate o scoperte: nella seconda metà del campione non esistono più.

## Lettura per il programma
- **Indici (NQ, ES) e oro:** nessuna delle 396–828 configurazioni orarie di stagionalità, momentum o reversal raggiunge t > 3 netto nemmeno in scoperta. A queste frequenze e con costi retail non c'è nulla.
- **Forex:** le uniche tracce sono anomalie del 2010–2013 che oggi non esistono più.
- Dopo circa 80 test singoli più questa ricerca su 3.276 configurazioni, **l'intraday sui 5 mercati liquidi disponibili gratis non offre un edge dimostrabile al netto dei costi retail.**
