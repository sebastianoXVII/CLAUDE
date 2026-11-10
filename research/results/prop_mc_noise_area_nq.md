# Monte Carlo della challenge Topstep 50K: candidato Noise Area su NQ (MNQ)

**Natura:** analisi di fattibilità **condizionata** a un candidato non ancora confermato (T6: morto su SPY; NQ promettente, conferma T7 in attesa dei dati OANDA). **Non è evidenza di edge.**

## Regole (verificate su help.topstep.com il 2026-11-10, salvo dove indicato)
- **Maximum Loss Limit:** 2.000 $, trailing sul saldo di fine giornata, violato anche intraday sul P&L non realizzato; smette di salire al saldo iniziale.
- **Consistency:** il giorno migliore deve restare sotto il 55% del target, altrimenti il target sale.
- **Massima esposizione:** 50 micro.
- **Target:** 3.000 $ (fonte secondaria, NON verificato).

## Metodo
- Giorni storici della strategia su QQQ convertiti in punti NQ (k = 41), 2017-01 → 2026-11, 2.672 giorni operativi.
- Costo MNQ 0,85 punti per round trip, 2 $ per punto MNQ.
- Minimo intraday di ogni giornata calcolato sulle barre a 1 minuto (low per i long, high per gli short).
- Block bootstrap con blocchi di 5 giorni, 4.000 simulazioni, orizzonte 120 giorni di borsa (circa 6 mesi).
- Codice: `research/lab/prop_sim.py` (testato, 6 test) e `research/run_prop_mc.py`.

## Risultati (probabilità entro 120 giorni)
Per 1 MNQ la media è 11,56 $ al giorno e la deviazione standard 153 $ (Sharpe annuo circa 1,2). Peggior drawdown storico con 1 MNQ: 3.418 $. Serie più lunga di giorni non positivi: 20.

| Contratti MNQ | Edge zero (confronto) | Edge storico | Edge dimezzato | Solo OOS 2025–26 |
|---|---|---|---|---|
| 1 | passa 3% / brucia 27% | 15% / 7% (78% ancora aperto) | 7% / 15% | 34% / 36% |
| **2** | 13% / 74% | **43% / 40%**, mediana 67 giorni | **25% / 57%** | 32% / 64% |
| 3 | 15% / 82% | 42% / 55%, mediana 44 giorni | 27% / 70% | 24% / 75% |
| 5 | 14% / 86% | 34% / 66% | 22% / 77% | 20% / 80% |
| 10 | — | 24% / 76% | 16% / 84% | 15% / 85% |

## Lettura fredda
- **L'edge, se reale, triplica la probabilità di passare** rispetto al caso (43% contro 13% a 2 MNQ). È la firma di un vantaggio vero, ma resta condizionato alla conferma T7.
- **La taglia ottimale è piccola, 2–3 MNQ.** Oltre, il drawdown trailing di 2.000 $ brucia il conto prima che l'edge emerga: è un sistema trend-following con molte piccole perdite e serie negative fino a 20 giorni.
- **È lento:** servono circa 2–3 mesi in mediana per passare. Non è compatibile con l'idea di passare in pochi giorni.
- **Con l'aspettativa dimezzata** (ipotesi prudente per il degrado dopo il backtest), a 2 MNQ passa nel 25% dei casi e brucia nel 57%. Con circa 49 $/mese di abbonamento (fonte secondaria) il costo atteso per ogni conto superato è nell'ordine delle centinaia di dollari, accettabile **solo se** T7 conferma.
- **Manca ancora** la fase funded (payout, regole XFA): va simulata prima di qualsiasi spesa.
