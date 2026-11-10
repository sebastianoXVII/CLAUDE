# T1 — Momentum dell'ultima mezz'ora (pre-registrazione)

**Stato:** PRE-REGISTRATO, nessun risultato ancora osservato.
**Data di registrazione:** 2026-11-10. Il commit git che introduce questo file precede qualsiasi esecuzione del test e ne fa da timbro temporale.
**Regola:** tutto ciò che sta qui sotto è congelato. Qualsiasi modifica dopo aver visto i dati va registrata come *nuova* ipotesi (T1b, ...) e conta come test aggiuntivo nella correzione per test multipli.

## 1. Ipotesi

Il rendimento della prima mezz'ora della sessione cash USA (dalla chiusura del giorno prima alle 10:00 ET) predice con lo stesso segno il rendimento dell'ultima mezz'ora (15:30–16:00 ET). L'effetto è più forte nei giorni di movimento ampio.

Fonti: Gao, Han, Li & Zhou (JFE 2018), su SPY 1993–2013; Baltussen, Da, Lammers & Martens (JFE 2021), su più di 60 futures 1974–2020, con l'effetto concentrato quando i dealer sono corti di gamma. Le evidenze sul periodo dopo il 2020 sono deboli e in parte contrarie: un test di un vendor su 1.085 sessioni SPX trova la versione incondizionata piatta. Vedi `reports/Mappa edge futures indici intraday.md`.

**Ipotesi nulla H0:** il P&L medio giornaliero netto della regola è ≤ 0.

## 2. Dati

- **Fonte:** Dukascopy, barre BID a 1 minuto, gratuite. Gli strumenti sono i CFD `USA500IDXUSD` (proxy di ES) e `USATECHIDXUSD` (proxy di NQ).
- **Periodo:** dal 2016-01-01 all'ultima data disponibile (≤ 2026-11-06).
- **Orari:** convertiti da UTC a `America/New_York` con l'ora legale gestita da `zoneinfo`.
- **Giorni validi:** giorni feriali con barre presenti a 10:00, 15:00, 15:30 e 16:00 ET (±2 minuti), più la chiusura delle 16:00 del giorno valido precedente. Le mezze sessioni (chiusura alle 13:00) sono escluse perché manca la barra delle 16:00.
- **Prezzo di riferimento al tempo t:** il close dell'ultima barra con timestamp ≤ t. Nessun dato successivo a t entra nel segnale.

**Limite noto, dichiarato prima del test.** Il CFD non è il contratto CME. Il prezzo segue lo stesso indice, ma lo spread è di circa 0,5 punti contro 0,25 di ES. Per questo i costi NON si deducono dal prezzo Dukascopy: si modellano separatamente con i costi reali di ES/NQ (sezione 4).

## 3. Regole: 4 varianti, fisse, × 2 strumenti = 8 test

Definizioni:
- r1 = log(P[10:00] / P[16:00 del giorno precedente])
- r12 = log(P[15:30] / P[15:00])
- Ingresso a P[15:30], uscita a P[16:00], 1 contratto.

| Variante | Direzione | Filtro |
|---|---|---|
| V1 | segno(r1) | nessuno |
| V2 | segno(r1) | solo se \|r1\| è nel terzile superiore della distribuzione di \|r1\| dei 252 giorni validi **precedenti** (finestra mobile, nessun look-ahead; servono 252 giorni di storia) |
| V3 | segno(r1 + r12) | nessuno |
| V4 | segno(r1 + r12) | stesso filtro di V2, applicato su \|r1\| |

Nessun altro parametro. Nessuno stop e nessun target: la posizione dura esattamente 30 minuti. Per rendere confrontabili le varianti, il primo anno (servito per la finestra di V2/V4) è escluso anche da V1/V3.

## 4. Costi (per round trip, in punti indice)

| Scenario | ES / MES (proxy USA500) | NQ / MNQ (proxy USATECH) |
|---|---|---|
| Base: contratto pieno, 1 tick di slippage totale + commissione circa 4 $ RT | 0,25 + 4/50 = **0,33 pt** | 0,25 + 4/20 = **0,45 pt** |
| Stress: micro, 1 tick di slippage + commissione circa 1,2 $ RT | 0,25 + 1,2/5 = **0,49 pt** | 0,25 + 1,2/2 = **0,85 pt** |
| Stress 2×: doppio del base | 0,66 pt | 0,90 pt |

Le commissioni sono stime da fonti secondarie (vedi `05_prop_firm_costi.md`) e vanno verificate prima di andare live.

## 5. Campioni

- **In-sample + validazione:** 2017-01-01 → 2023-12-31. Il 2016 serve solo a riempire la finestra di 252 giorni.
- **Hold-out:** 2024-01-01 → fine dati. **Non viene calcolato** finché la sezione 6a non ha dato il suo verdetto. Il codice lo calcola solo se lanciato con il flag `--holdout`.

## 6. Criteri di decisione (kill)

**6a. In-sample (2017–2023).** Una variante sopravvive solo se valgono TUTTE queste condizioni:
1. Il P&L medio giornaliero netto (costi base) è > 0, con t di Newey-West (5 lag) **> 3,0** (soglia di Harvey-Liu-Zhu).
2. Il P&L medio resta > 0 anche con costi stress 2×.
3. Il p-value corretto con Holm sugli 8 test, al 5%, è significativo (test unilaterale).
4. Il P&L netto è positivo in almeno **5 anni su 7**.
5. La variante batte il benchmark "sempre long nell'ultima mezz'ora" (stessi giorni e costi) con una differenza media > 0. Serve a escludere che il risultato sia solo il drift di fine giornata.

**6b. Hold-out (2024–fine).** Si calcola solo per le varianti sopravvissute alla 6a. Il P&L medio netto con costi base deve essere > 0 con t > 1,5: il campione è più corto, quindi basta una conferma direzionale, non una nuova scoperta.

**Esito:**
- Nessuna variante supera 6a+6b → **T1 MORTO.** Si passa a T2 (livelli di stop) senza ritocchi di parametri.
- Almeno una supera → T1 passa alla conferma su dati CME veri (ES/NQ) e alla simulazione Monte Carlo della challenge, con expectancy dimezzata.

## 7. Metriche riportate in ogni caso

N giorni, N trade, win rate, payoff, expectancy in punti e in $ (ES e MES), profit factor, Sharpe annualizzato sul P&L giornaliero (√252), Sortino, max drawdown in $, t di Newey-West, p grezzo e p corretto con Holm, P&L per anno.

## Emendamento 1 — 2026-11-10, registrato PRIMA di qualsiasi risultato

**Motivo.** Dukascopy ha bannato l'IP del cloud dopo i limiti di velocità: il server accetta la connessione e non risponde, mentre il proxy funziona verso altri host. Sono stati scaricati 5 giorni di prova e nessun risultato T1 è stato calcolato.

**Modifica (solo la fonte dati).** Si usano le barre a 1 minuto di Alpaca, feed SIP consolidato (tutte le borse USA), con `adjustment=all` (split e dividendi), per gli ETF **SPY** (proxy di ES) e **QQQ** (proxy di NQ), dal 2016-01-01. Ipotesi, varianti, periodi, costi e criteri di kill restano **identici**.

**Conversione dei costi.** I costi restano in punti indice (sezione 4). Il P&L in punti indice equivalenti è `last_pts = (P16:00 − P15:30) × k`, con k = 10 per SPY (SPX ≈ 10 × SPY) e k = 41 per QQQ (NDX ≈ 41 × QQQ, rapporto stabile in un intervallo 40–42 dal 2016). L'errore sul peso dei costi è inferiore al 5%; vale come limite dichiarato.

**Vantaggio della modifica.** È un dato di borsa con volume reale, ed è lo stesso strumento (SPY) del paper originale di Gao et al. (2018).

## Emendamento 2 — 2026-11-10, registrato PRIMA di qualsiasi risultato

Deriva da una code review indipendente del motore. I rilievi sono stati verificati sui dati prima di accettarli. T1 non è ancora stato eseguito.

1. **Mezze sessioni.** È verificato che Alpaca SIP include barre after-hours anche nei giorni di chiusura anticipata: il 2017-11-24 ha 164 barre dopo le 13:00, fino alle 16:59. Per questo si usano **solo barre della sessione regolare**, con inizio in [09:30, 15:59] ET. Il filtro sull'orario però NON basta: un test ha mostrato che nei giorni di chiusura anticipata le barre after-hours cadono anche tra le 13:00 e le 16:00. Quei giorni si escludono quindi **in modo esplicito**, usando il calendario ufficiale NYSE della libreria `exchange_calendars` (XNYS, `early_closes`: 23 giorni dal 2016 al 2026, tra cui il 2017-11-24). Questo rispetta l'esclusione delle mezze sessioni prevista dalla sezione 2.
2. **Convenzione di prezzo, resa esplicita.** P(t) = close della barra che inizia a t−1 minuto. Se manca, si usa l'ultima barra precedente entro 2 minuti; la tolleranza guarda solo indietro. Questa è la lettura corretta di "ultima barra con timestamp ≤ t" per barre marcate all'inizio del minuto.
3. **Benchmark del criterio 5.** "Stessi giorni" significa i giorni in cui la variante opera. La differenza è la media, sui soli giorni operati, di (segnale − 1) × last_pts; i costi si annullano. Il criterio è soddisfatto se questa media è > 0. È la lettura più severa: esclude che una variante filtrata passi solo perché evita i costi nei giorni senza trade.
4. **Conversione in punti.** È verificato che `adjustment=all` sconta i dividendi in modo moltiplicativo: il 2017-01-03 SPY rettificato vale 194,30 contro 225,19 non rettificato (fattore 0,863); per QQQ il fattore è 0,931. Da qui in avanti:
   - r1 e r12 si calcolano sui prezzi **rettificati**, perché eliminano il gap ex-dividendo, che sui futures non esiste;
   - last_pts = (P_raw[16:00] − P_raw[15:30]) × k, sui prezzi **non rettificati** (`adjustment=raw`), con k = 10 / 41 come nell'emendamento 1.
5. **Hold-out vincolato.** L'hold-out si calcola solo leggendo il verdetto in-sample salvato, e solo per le varianti sopravvissute. Il verdetto finale è 6a E 6b. Se nessuna variante sopravvive, l'esito è "T1 MORTO" e l'hold-out non si calcola.

Rilievo respinto dopo verifica: la "perdita del 31 dicembre". Il 31/12 è presente in tutti gli anni (682–786 barre), perché Alpaca include la data di fine.
