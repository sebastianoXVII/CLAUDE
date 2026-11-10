# T8 e T13 — Concetti di sessione del committente: verdetto

**Esecuzione unica in-sample:** 2026-11-10 (`run_t8.py`, `run_t13.py`). **Risultati:** `T8_in_sample.json`, `T13_in_sample.json`.

## Verdetto: TUTTI MORTI. 0 test sopravvissuti su 10 su NQ (T8) e su 30 su forex e oro (T13).
Per pre-registrazione l'hold-out non si calcola, perché non c'è nessun sopravvissuto.

## Dati
- HistData M1 24 ore: NSXUSD e SPXUSD (CFD sugli indici), EURUSD, GBPUSD, XAUUSD.
  - In-sample: da fine 2010 (gli indici partono dal 14/11/2010) al 2023-12-31. Il 2024 resta intatto.
- **Fuso orario verificato sui soli prezzi, prima dei run** (T8 emendamento 5): l'orario dei dati è quello di New York con l'ora legale.
  - I picchi di volatilità cadono alle 09:30 ET (indici) e alle 08:30 ET (forex e oro), d'estate e d'inverno.
  - NSXUSD alle 15:59 ha correlazione 0,9997 con QQQ, con rapporto di prezzo 41,04.
- **Difetto della fonte:** da febbraio a luglio 2023 manca circa metà dei minuti nelle ore attive. La regola pre-registrata, che richiede almeno 300 barre RTH e la barra delle 15:59, ha escluso quei giorni senza guardare i rendimenti: nel 2023 restano 135 giorni validi su NQ e 144 su EURUSD, contro circa 230–255 negli altri anni.
- Due revisioni indipendenti del codice prima dei run. 132 test automatici passati.

## T8 — NQ (costo 0,45 pt; criterio t > 3, Holm sui 10 test)
| Ipotesi | Trade | Lordo pt/trade | t NW | Stress 2× | Anni + |
|---|---|---|---|---|---|
| H8a sweep di Londra dell'Asia | 1.473 | −0,02 | −1,17 | <0 | 5/14 |
| H8b rottura del box Asia (accettazione o riassorbimento) | 1.837 | −0,70 | −1,49 | <0 | 2/14 |
| H8c sweep del range di Londra a NY | 1.710 | +0,44 | −0,01 | <0 | 4/14 |
| H8d IFVG | 2.682 | −0,55 | −7,12 | <0 | 0/14 |
| H8e order block | 1.990 | −1,03 | −3,20 | <0 | 1/14 |

La riga riporta la variante base. Con il filtro di trend HTF il quadro non cambia: il t migliore è −0,45. ES, solo riportato, è peggiore: tutti i t sono negativi, da −1,5 a −16,6.

## T13 — forex e oro (Holm sui 30 test)
- **Nessun t positivo.** Il migliore: XAUUSD H8c con filtro HTF, t = −0,87.
- **Guadagno lordo per trade (prima dei costi) praticamente nullo:**
  - EURUSD e GBPUSD fra −1,6 e +0,6 decimi di pip;
  - oro fra −0,05 e +0,23 $/oz, contro un costo di 0,35 $.
- **IFVG (H8d):** è il peggiore ovunque, con t fra −9 e −17, perché fa molti trade con stop stretti e il costo li erode.

## Cosa significa (lettura del quant lead)
1. **Nella forma meccanica canonica questi concetti non hanno edge, nemmeno prima dei costi.** Il P&L lordo medio è circa zero su 5 mercati e 14 anni: è ciò che ci si aspetta da un segnale casuale con stop e target. Con circa 1.500–3.000 trade per test, un edge anche piccolo, per esempio +0,05 R per trade, sarebbe stato visibile.
2. **I costi trasformano lo zero in una perdita sicura.** I setup a stop stretto (IFVG, order block) sono quelli che perdono di più.
3. **Il risultato è coerente su tutti i mercati,** quindi non dipende dalla scelta dello strumento.
4. **Cosa NON è stato testato:** la versione discrezionale, cioè la selezione del contesto, la lettura dell'order flow e la gestione attiva della posizione. Quella non si può backtestare in modo onesto senza regole scritte. Qui è morta solo la versione con regole meccaniche.
5. **Niente salvataggi:** non si ritoccano finestre, target o filtri per far emergere un risultato. Sarebbe data mining.

## Diario
Il verdetto è stato calcolato senza grafici (`NO_JOURNAL=1`), per non dipendere dalla durata della generazione degli screenshot. Diario e screenshot si generano in un secondo passaggio, con lo stesso codice e gli stessi trade; i numeri non cambiano.
