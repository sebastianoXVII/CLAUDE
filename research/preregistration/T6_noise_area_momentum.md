# T6 — Momentum intraday "Noise Area" (Zarattini, Aziz e Barbon): replica fuori campione (pre-registrazione)

**Stato:** PRE-REGISTRATO, nessun risultato osservato. **Data:** 2026-11-10.
**Fonte primaria, letta per intero:** C. Zarattini, A. Aziz, A. Barbon, *Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)*, Swiss Finance Institute RP 24-97. Prima versione 10 maggio 2024, revisione 3 febbraio 2025. PDF: alexandria.unisg.ch, bitstream a99aba00-f967-49b3-aceb-f544dc386e0b. Dati del paper: IQFeed, da maggio 2007 ad aprile 2024; un'appendice arriva a dicembre 2024.
**Risultato dichiarato (Tabella 3):**
- dimensione fissa al 100% ("Curr.Band + VWAP"): IRR 9,7%, Sharpe 1,24, hit ratio 43%, MDD 12%;
- con dimensione dinamica: IRR 19,6%, Sharpe 1,33.

## 1. Perché è un test onesto
Gli autori hanno scelto le regole su dati fino al 2024. Il periodo **2025-01-02 → fine dati (2026-11-06)** non era disponibile a nessuno quando la strategia è stata pubblicata e rivista: è un vero fuori campione **per loro e per noi**. Nessun nostro test precedente ha usato questa strategia.

## 2. Regole, citate dal paper (sezioni 3–4)
1. Per ogni giorno t−i (i = 1…14) e ogni ora del giorno HH:MM: move = |Close(t−i, HH:MM) / Open(t−i, 09:30) − 1|.
2. σ(t, HH:MM) = media dei 14 valori di move.
3. UpperBound(t, HH:MM) = max(Open(t, 09:30), Close(t−1, 16:00)) × (1 + σ); LowerBound(t, HH:MM) = min(Open(t, 09:30), Close(t−1, 16:00)) × (1 − σ).
4. **Decisioni solo a HH:00 e HH:30**, a partire dalle 10:00 ("takes its first position at 10:00"): long se il prezzo è sopra UB, short se è sotto LB.
5. **Trailing stop**, controllato **solo** a HH:00 e HH:30:
   - long: max(UB, VWAP);
   - short: min(LB, VWAP).

   Il VWAP usa solo le ore di mercato. Se il prezzo attraversa lo stop, si chiude. Se attraversa la banda opposta, si chiude e si apre nella direzione opposta.
6. Tutte le posizioni si chiudono alla chiusura delle 16:00.

## 3. Implementazione (convenzioni del programma)
- **Dati:** Alpaca SIP a 1 minuto, prezzi **non rettificati**, solo sessione regolare, chiusure anticipate NYSE escluse (`exchange_calendars`). Strumenti: **SPY** (lo strumento del paper; proxy di ES) e **QQQ** (proxy di NQ; non è il test principale del paper).
- **Prezzo a HH:MM:** P(HH:MM) = close della barra che inizia a HH:MM−1m, con tolleranza di 2 minuti all'indietro. Si usa per Open: Open(t, 09:30) = open della barra 09:30. Close(t−1, 16:00) = P(16:00) del giorno valido precedente.
- **σ:** si usano solo i 14 giorni **validi** precedenti con tutti i prezzi presenti; servono 14 giorni di storia.
- **Momenti di decisione:** 10:00, 10:30, …, 15:30. Le esecuzioni avvengono al prezzo P del momento di decisione. A ogni momento si controlla prima lo stop, poi l'eventuale nuovo ingresso o l'inversione.
- **VWAP:** cumulato dalle 09:30 con prezzo tipico (H+L+C)/3 × volume, fino alla barra precedente al momento di decisione.
- **Dimensione:** 1 contratto per trade (solo la versione "100%", senza leva dinamica: il test riguarda il segnale, non il sizing).
- **Costi** per round trip, in punti indice equivalenti, con k = 10 per SPY e 41 per QQQ: ES 0,33 pt e NQ 0,45 pt; stress 2×. Un'inversione conta come 2 trade.

## 4. Criteri (confermativi: ipotesi pubblicata, una famiglia di 2 test)
Il periodo di test è 2025-01-02 → fine. Sopravvive (**edge candidato**) se valgono tutte queste condizioni:
1. **SPY:** t di Newey-West (5 lag) > **1,65** sul P&L giornaliero netto, cioè unilaterale al 5%. La soglia è più bassa di 3 perché il test è confermativo: replica una strategia pubblicata con regole fisse, non una ricerca fra molte varianti. Per circa 1,85 anni il t atteso se l'effetto è intatto (Sharpe 1,24) è circa 1,7, quindi si dichiara che **il test ha potenza limitata**.
2. **QQQ:** stesso criterio, con p corretto con Holm sui 2 test < 0,05 per entrambi.
3. Media > 0 con stress 2× su entrambi.

**Esito.** SPY e QQQ entrambi validi → candidato forte. Solo SPY → candidato debole: si va alla conferma su futures veri. Nessuno dei due → **T6 MORTO**.

## 5. Informazioni aggiuntive (non decisionali)
- Si riporta anche il periodo 2017–2024: è **dentro il campione** degli autori, quindi non vale come evidenza. Serve solo a verificare che la nostra implementazione riproduca all'ingrosso il loro risultato.
- Ogni trade del periodo fuori campione va nel **diario** (`research/lab`), con MFE/MAE e screenshot.

## Emendamento 1 — chiarimenti registrati PRIMA di qualsiasi risultato
- **Rientro dopo uno stop:** si rientra dal momento di decisione **successivo**, non nello stesso. Il paper non specifica il caso; questa è la scelta meno soggetta a churn.
- **Ordine delle verifiche a ogni momento di decisione:** prima l'inversione sulla banda opposta, poi il trailing stop, poi l'eventuale nuovo ingresso.
- **Giorno precedente scartato:** se il giorno valido precedente è stato scartato (chiusura anticipata o meno di 300 barre), il close delle 16:00 non è disponibile e quel giorno non si opera.
- **Diario:** i trade fuori campione vengono salvati in `research/results/journal.sqlite`. Gli screenshot vanno in `data/charts/T6/`, fuori dal repository per dimensione, e si rigenerano dal diario.
