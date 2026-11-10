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

## Emendamento 1 — 2026-11-10, cambio di fonte registrato PRIMA di qualsiasi dato
**Motivo.** OANDA non concede l'accesso API al conto del committente, e FirstRate Data (NQ futures dal 2008) è a pagamento: per ora non si compra. Si usa **Dukascopy `USATECHIDXUSD`**, CFD sul Nasdaq-100, gratuito, scaricato tramite GitHub Actions.
- **Dati:** candele BID a 1 minuto, 24 ore. Il periodo di test è **dal primo giorno disponibile al 2016-12-31**; la data d'inizio effettiva sarà riportata. Si usano i prezzi BID: lo spread è circa costante e sposta tutti i livelli allo stesso modo, quindi è dichiarato come approssimazione. Il volume è il tick volume Dukascopy, usato per il VWAP come approssimazione, come era già previsto per OANDA.
- **Potenza statistica dichiarata prima.** Se i dati partono intorno al 2012, il campione è di circa 5 anni. Con uno Sharpe di 1,2 il t atteso è circa 2,7, sotto la soglia di 3. Per questo la regola decisionale passa da due a **tre esiti**:
  - **CONFERMATO:** t > 3, più gli altri criteri della sezione 5;
  - **INCONCLUSIVO:** 0 ≤ t ≤ 3. Non si dichiara né edge né morte. Serve il campione 2008–2011 dei futures veri (FirstRate), da acquistare solo in questo caso;
  - **MORTO:** t < 0, cioè P&L netto medio negativo su un periodo mai visto.
- **Resto invariato:** regole, costi e diagnostico di coerenza con QQQ sul periodo sovrapposto.

## Emendamento 2 — 2026-11-10, fonte HistData e VWAP da profilo di volume, registrato PRIMA di qualsiasi rendimento Noise Area sul periodo di test
**Motivo.** Dukascopy non è praticabile: dopo circa 85 minuti di download non era completato nemmeno un anno, e il job è stato annullato. HistData `NSXUSD` (Nasdaq-100 a 1 minuto, gratuito, già scaricato per T8, timezone verificata: ora di New York con ora legale) copre dal 2010-11-14. Sul 2010–2016 **nessun test Noise Area è mai stato eseguito**: T8 ha usato questi dati per altri setup (sessioni Asia e Londra), e nessun rendimento della Noise Area è stato calcolato o guardato. Unico controllo fatto finora: il numero di giornate valide per anno, cioè 31 nel 2010 e 247–251 nel 2011–2016.

**Volume.** HistData non ha volume (volume = 0 sul 100% delle barre). Il VWAP si calcola con un **profilo di volume**: il volume di ogni barra è sostituito dalla mediana del volume QQQ (file `QQQ_1m_raw`) in quel minuto del giorno (09:30…15:59 ET), calcolata su tutto il 2016-01-01 → 2024-12-31. Il profilo contiene solo la *forma* intraday del volume, non i prezzi. Che venga da anni successivi al periodo di test è dichiarato come approssimazione.

**Validazione del proxy (vincolante, prima dell'esecuzione).** Su QQQ 2017-01-01 → 2024-12-31 (periodo già visto in T6, quindi senza alcun consumo di campione) si confronta la strategia con il VWAP vero e con il VWAP da profilo, a parità di prezzi. Il proxy è valido solo se valgono ENTRAMBI:
1. nei giorni operativi, la lista dei trade (ora di entrata, lato, ora di uscita) è identica in almeno il **90%** dei giorni;
2. la correlazione fra i due P&L giornalieri netti è **≥ 0,90**.

Se il proxy fallisce, T7 **non si esegue** su HistData. Resta in attesa di dati con volume vero (FirstRate) e lo si dichiara.

**Periodo di test.** Dal primo giorno operativo (servono 14 giorni di riscaldamento per σ e un close precedente valido) al **2016-12-31**, cioè circa 6 anni e circa 1.500 giorni. **Potenza:** con Sharpe 1,2 il t atteso è circa 2,9. Restano i tre esiti dell'emendamento 1: **CONFERMATO** (tutti i criteri della sezione 5), **INCONCLUSIVO** (0 ≤ t ≤ 3, oppure t > 3 senza gli altri criteri) e **MORTO** (t < 0).

**Resto invariato:** regole T6 (emendamenti 1–2), nessun dividendo (indice CFD), costi NQ 0,45 punti, MNQ 0,85, stress 2×, prezzi in punti indice (k = 1, 20 $ a punto). Inclusione del giorno: almeno 300 barre RTH, esclusione di weekend e chiusure anticipate NYSE. Diagnostico non decisionale: correlazione del P&L giornaliero NSXUSD con QQQ×41 sul 2017–2024. Esecuzione unica, con un file di guardia.
