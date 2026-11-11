# T15 — Trend following diversificato (time-series momentum) su 23 CFD, orizzonte giornaliero (pre-registrazione)

**Stato:** PRE-REGISTRATO; dati giornalieri non ancora scaricati, nessun rendimento guardato. **Data:** 2026-11-11.

## 1. Perché
L'intraday sui mercati liquidi è chiuso (T1–T14, circa 80 test più 3.276 configurazioni, nessun edge). Il time-series momentum ha la documentazione più ampia della finanza empirica:
- **Moskowitz, Ooi e Pedersen (2012, JFE):** 58 futures dal 1985 al 2009, Sharpe circa 1;
- **Hurst, Ooi e Pedersen (2017, "A Century of Evidence on Trend-Following Investing"):** risultati positivi in ogni decennio dal 1880. Dopo il 2010 il rendimento si è però ridotto, a uno Sharpe di circa 0,3–0,6 negli indici dei CTA. **[NV: i valori post-2010 sono una stima da fonti secondarie; da verificare.]**

Orizzonte di giorni o settimane, quindi costi di transazione trascurabili. Qui **non si ottimizza nulla**: si usano le due regole standard della letteratura.

## 2. Universo e dati
- HistData M1 (copia pubblica su Google Drive) convertiti in barre giornaliere. La giornata chiude alle **17:00 di New York** (`research/data/histdata_daily.py`).
- **23 strumenti:**

  | Classe | Strumenti |
  |---|---|
  | Indici | SPXUSD, NSXUSD, GRXEUR (DAX), UKXGBP (FTSE), FRXEUR (CAC), ETXEUR (Euro Stoxx 50), JPXJPY (Nikkei), AUXAUD (ASX 200), HKXHKD (Hang Seng) |
  | Materie prime | XAUUSD, XAGUSD, WTIUSD, BCOUSD |
  | Forex | EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, NZDUSD, EURJPY, EURGBP, AUDJPY |

  Tutti sono negoziabili come CFD presso le prop CFD.
- **Giorno valido per uno strumento:** da lunedì a venerdì, con almeno 120 barre M1 nella giornata. Il rendimento r_t = close_t / close_(giorno valido precedente) − 1.
- **Disponibilità:** uno strumento entra nel portafoglio solo dopo 252 giorni validi di storia. Ogni giorno il portafoglio è equipesato sugli strumenti disponibili (N_t). Se uno strumento non ha dati per tutto il periodo, si dichiara.

## 3. Regole (nessun parametro libero)
Tutto è calcolato alla chiusura del giorno t. La posizione è tenuta dalla chiusura di t alla chiusura del giorno valido successivo: nessuna anticipazione.
- **Volatilità ex ante:** σ_t = radice della media esponenziale dei rendimenti quadratici (center of mass 60 giorni, come in MOP 2012), annualizzata con √261.
- **Posizione:** pos_i,t = segnale_i,t × 0,40 / σ_i,t, con |pos| ≤ 4. È la scala di MOP: 40% di volatilità per strumento. La scala non cambia il t.
- **Segnali (2 varianti):**
  - **V1 (MOP 2012):** segnale = segno del rendimento degli ultimi 252 giorni validi;
  - **V2 (HOP 2017):** segnale = media dei segni dei rendimenti a 21, 63 e 252 giorni validi.
- **Rendimento del portafoglio:** R_t+1 = (1/N_t) × Σ_i pos_i,t × r_i,t+1, meno i costi.

## 4. Costi (CFD, stimati e dichiarati)
**Transazione:** |Δpos| × c_i / 2 per ogni cambio di posizione. c_i è il costo di un round trip, in frazione del prezzo:

| c_i | Strumenti |
|---|---|
| 1 bp | Forex major (EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, NZDUSD) |
| 1,5 bp | Cross (EURJPY, EURGBP, AUDJPY) |
| 2 bp | SPX, NSX, DAX, FTSE, CAC, Euro Stoxx 50, oro |
| 3 bp | Nikkei, ASX, Hang Seng |
| 4 bp | WTI, Brent |
| 5 bp | Argento |

**Finanziamento overnight:** |pos| × 3% annuo / 252 a ogni giorno valido. È il markup tipico del broker CFD, che si paga sia long sia short.

**Limite dichiarato:** non si modellano il differenziale dei tassi nel forex (carry), né dividendi e tassi negli indici. I prezzi HistData sono spot o CFD senza queste componenti.

**Stress:** 2× entrambi i costi.

## 5. Periodi e criteri
**In-sample, 2011-01-01 → 2019-12-31.** Il 2010 serve solo per la storia iniziale. Una variante sopravvive se valgono TUTTE:
1. t di Newey-West (5 lag) sul rendimento giornaliero netto **> 3,0**, con **Holm sulle 2 varianti**;
2. media > 0 con costi 2×;
3. almeno 6 anni positivi su 9.

**Hold-out, 2020-01-01 → 2024-12-31.** Si calcola solo per le varianti sopravvissute, in un'esecuzione unica. Una variante è **EDGE** se valgono:
- t > 1,65;
- media > 0 con costi 2×;
- almeno 3 anni positivi su 5.

**Potenza, dichiarata prima:** con Sharpe 1,0 il t atteso in 9 anni è 3,0; con lo Sharpe post-2010 dei CTA, 0,3–0,6, è 0,9–1,8. **La probabilità di superare t > 3 è bassa**, ed è detto prima. Se il risultato è positivo ma sotto soglia, l'esito è "INCONCLUSIVO" e non si mette denaro.

**Indicatori per la prop (descrittivi, non decisionali):** con il portafoglio scalato a una volatilità del 10% annuo si riportano:
- max drawdown;
- giorno peggiore;
- frequenza dei giorni sotto −2% e −5%;
- quota dei periodi di 14 giorni positivi, che è il ritmo dei payout.

## 6. Esecuzione
Due invocazioni separate (`insample`, `holdout`), ognuna con un file di guardia e un lock di avvio. L'in-sample non legge dati successivi al 2019-12-31. Codice sviluppato con TDD e sottoposto a code review indipendente prima dell'esecuzione.

## Emendamento 1 — 2026-11-11, registrato PRIMA del download (nessun dato giornaliero esiste ancora)
Dall'elenco dei file su Drive (`research/data/histdata_manifest.json`) risultano queste lacune:
- **ETXEUR** finisce nel 2019, con l'ultimo anno probabilmente parziale;
- **WTIUSD** non ha il 2024;
- **AUDJPY** ha il 2012 quasi vuoto;
- per i 7 indici, WTI e Brent il 2010 è parziale, perché le serie partono a fine 2010.

**Regola:** uno strumento è nel portafoglio solo fra la sua storia minima di 252 giorni validi e il suo **ultimo giorno di dati**. Dopo quel giorno esce dal conteggio N_t. Nei buchi interni la posizione resta aperta, e il rendimento si misura da close a close fra due giorni validi consecutivi. Gli indici che partono a fine 2010 entrano nel portafoglio solo verso fine 2011. Tutto il resto è invariato.
