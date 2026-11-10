# T1 — Momentum dell'ultima mezz'ora: **MORTO**

**Data:** 2026-11-10. **Pre-registrazione:** `research/preregistration/T1_momentum_ultima_mezzora.md` (emendamenti 1 e 2, entrambi registrati prima dei risultati). **Dati grezzi dei risultati:** `T1_in_sample.json`.

## Esito
In-sample 2017–2023: **0 varianti su 8 sopravvivono.** Su ES, tutte e 4 le varianti hanno un P&L netto medio negativo. Su NQ il P&L netto medio è negativo per tutte e 4, con t compreso fra −1,4 e −0,3. Secondo la sezione 6 e l'emendamento 2, **l'hold-out 2024–2026 non è stato calcolato** e resta intatto per eventuali ipotesi future diverse da questa.

| Variante | t (Newey-West) | Expectancy ES pieno / trade | Anni positivi |
|---|---|---|---|
| ES V1 segno(r1) | −2,05 | −28 $ | 2/7 |
| ES V2 V1 sui giorni grandi | −2,02 | −63 $ | 2/7 |
| ES V3 segno(r1+r12) | −2,24 | −30 $ | 1/7 |
| ES V4 V3 sui giorni grandi | −2,04 | −64 $ | 2/7 |
| NQ V1–V4 | da −1,37 a −0,32 | da −6 a −43 $ | 1–2/7 |

## Perché è morto: non è un problema di costi
- **Al lordo, senza costi, V1 è già negativo:** −0,23 punti a trade su ES, −0,88 su NQ.
- **Regressione del paper originale** r_ultima_mezz'ora ~ r1, 2017–2023: beta positivo ma non significativo (t = 0,60 su SPY, t = 1,05 su QQQ).
- **Il segnale vive solo nel 2020.** Su SPY la correlazione fra r1 e l'ultima mezz'ora è −0,08 nel 2017–19, **+0,17 nel 2020** e −0,07 nel 2021–23; su QQQ è −0,04, +0,27 e −0,05. È coerente con Baltussen et al. (2021), secondo cui l'effetto si concentra nei regimi di stress e di gamma negativa dei dealer. Fuori da quei regimi l'ultima mezz'ora tende leggermente a **invertire** il movimento.

## Controlli di qualità
- Giorni validi: circa 248–251 l'anno. Escluse le 23 chiusure anticipate NYSE (calendario `exchange_calendars`).
- Prezzi verificati a campione: SPY il 2023-12-29 vale 475,78 alle 15:29 e 475,35 alle 15:59.
- Motore sviluppato con TDD (30 test) e sottoposto a code review indipendente prima di vedere i dati. Rilievi corretti: barre after-hours nelle mezze sessioni, conversione in punti con i dividendi, definizione del benchmark, hold-out vincolato.

## Cosa NON si fa (disciplina)
- Non si cerca una "versione che funziona": niente filtri post-hoc sul 2020, niente orari diversi, niente stop. Ogni variazione sarebbe una nuova ipotesi (T1b) e conterebbe nella correzione per test multipli.
- Un'ipotesi legittima per il futuro, da pre-registrare a parte: **T1-regime**, momentum attivo solo con volatilità implicita alta (VIX sopra soglia, decisa ex ante). Ha una base teorica (Baltussen), ma va trattata con sospetto: è stata suggerita dai dati di questo test. Priorità bassa.

## Prossimo passo
T2: reazione ai livelli dove si accumulano gli stop (numeri tondi, massimo e minimo del giorno prima, massimo e minimo overnight), confrontati con livelli placebo.
