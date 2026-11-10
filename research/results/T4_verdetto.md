# T4 — Concetti retail canonici (ORB, gap fill, VWAP come calamita, FVG): **MORTO**

**Data:** 2026-11-10. **Pre-registrazione:** `research/preregistration/T4_concetti_retail.md`, con gli emendamenti 1–2 registrati prima dei risultati. **Dati:** `T4_in_sample.json`. Giorni scartati: 21 per strumento (chiusure anticipate oppure meno di 300 barre).

## Esito in-sample 2017–2023, al netto dei costi base
| | Trade | Win rate | Lordo pt/trade | Netto $/trade | t NW | Anni + |
|---|---|---|---|---|---|---|
| ES ORB | 1.727 | 20% | +0,52 | +9,6 | 0,51 | 4/7 |
| ES gap fill | 1.172 | 56% | −0,36 | −34 | −1,63 | 2/7 |
| ES VWAP calamita | 1.152 | 63% | −0,88 | −60 | −2,11 | 2/7 |
| ES FVG | 1.363 | 34% | +0,13 | −9,8 | −0,71 | 2/7 |
| NQ ORB | 1.735 | 24% | +3,34 | +57,8 | 1,74 | 5/7 |
| NQ gap fill | 1.068 | 61% | +0,89 | +8,9 | 0,25 | 4/7 |
| NQ VWAP calamita | 1.484 | 63% | −5,81 | −125 | **−3,30** | 1/7 |
| NQ FVG | 1.347 | 35% | +0,71 | +5,2 | 0,21 | 5/7 |

Nessun concetto supera t > 3 con correzione di Holm su entrambi gli strumenti. **T4 MORTO; la mappa dei concetti retail su ES/NQ è chiusa.**

## Lettura
- **FVG (ICT):** lordo vicino a zero su entrambi gli strumenti. Lo stop scatta nel 64–65% dei casi e il target a 2R si raggiunge solo nel 31–32%. È folklore misurato.
- **Gap fill:** i gap fra 0,1% e 1% si chiudono entro le 12:00 solo nel 40–47% dei casi. Netto nullo o negativo.
- **ORB:** positivo su NQ ma non significativo, quasi nullo su ES. È coerente con la replica indipendente di Zarattini-Aziz: risultato lordo riprodotto, netto circa zero.
- **VWAP come calamita: l'idea è smentita, non solo non provata.** Il "ritorno al VWAP" è più frequente (63% di target raggiunti), ma quando il prezzo non torna scappa via, e i perdenti superano di gran lunga i vincenti (payoff 0,47–0,50). Su NQ la perdita è significativa (t = −3,3).

## Ipotesi generata (NON un risultato)
La smentita del VWAP suggerisce l'opposto: **continuazione lontano dal VWAP**. È nata guardando questi dati, quindi qui non vale come evidenza. Si testa come **T5**, pre-registrato e **solo sull'hold-out mai toccato (2024–fine)**, con una sola esecuzione.
