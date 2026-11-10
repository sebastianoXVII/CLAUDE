# T7 — Noise Area su NQ: conferma su dati mai usati (pre-registrazione)

**Stato:** PRE-REGISTRATO; dati non ancora scaricati (in attesa dell'accesso API OANDA). **Data:** 2026-11-10.

## 1. Perché
T6 è morto su SPY, ma su QQQ (proxy di NQ) la strategia, con i parametri degli autori e mai ottimizzata su NQ, è stata positiva in 10 anni su 10 (2017–2026), con t = 1,58 nel fuori campione 2025–26 (vedi `results/T6_verdetto.md`). Quel risultato è stato **osservato prima** di formulare questa ipotesi, quindi su quei dati non vale come prova. Serve un campione che nessun test del programma ha mai toccato.

## 2. Ipotesi
H7: la strategia Noise Area, con **regole identiche a T6 compresi gli emendamenti 1–2**, applicata al Nasdaq-100 ha P&L giornaliero netto medio > 0.

## 3. Dati
- **Fonte:** OANDA v20, strumento `NAS100_USD`, candele M1, prezzo mid.
- **Periodo di test:** dal primo giorno disponibile (atteso intorno al 2008) al **2016-12-31**. È un periodo che nessun test del programma ha usato: i dati Alpaca partono dal 2016, e in T6 il 2016 è servito solo a scaldare σ.
- **Orari:** ET, sessione regolare 09:30–15:59. Open = open della barra 09:30. Close precedente = P(16:00) del giorno valido precedente. Si escludono le chiusure anticipate NYSE.
- **Differenze dichiarate rispetto a T6:**
  - è un CFD sull'indice: niente dividendi da sottrarre e niente k (i prezzi sono già in punti indice);
  - il VWAP usa il **tick volume** OANDA, perché il CFD non ha un volume di borsa. È un'approssimazione dichiarata.
- **Diagnostico non decisionale:** sul periodo sovrapposto 2017–2026 si riporta la correlazione fra il P&L giornaliero OANDA e quello di QQQ×41 di T6. Serve a verificare che il CFD riproduca lo stesso segnale.

## 4. Costi
NQ 0,45 punti per round trip (MNQ 0,85); stress 2×.

## 5. Criteri (test unico, decisivo)
Sul periodo di test sopravvive solo se valgono TUTTE queste condizioni:
1. t di Newey-West (5 lag) **> 3,0** sul P&L giornaliero netto (costo NQ). Con circa 9 anni il t atteso, se lo Sharpe resta circa 1,2, è circa 3,6.
2. Media > 0 con costi stress 2× **e** con costi MNQ.
3. Almeno il 2/3 degli anni positivi.

**Esito:**
- **SOPRAVVIVE:** primo edge confermato del programma. Si passa alla simulazione della fase funded, poi al forward test in demo (minimo 3 mesi) prima di spendere per qualsiasi challenge.
- **MUORE:** la famiglia Noise Area è chiusa su tutti gli strumenti.

## 6. Diario
Ogni trade va in `research/results/journal.sqlite` (strategia `T7_noise_area_nq`), con screenshot e MFE/MAE.
