# T4 — Concetti retail canonici: ORB, gap fill, VWAP come calamita, FVG (pre-registrazione)

**Stato:** PRE-REGISTRATO, nessun risultato osservato. **Data:** 2026-11-10. Il commit precede qualsiasi esecuzione.

## 0. Perché si testano nonostante il filtro sulla carta
Nessuno dei quattro concetti ha una stima credibile dell'effetto lordo: le uniche evidenze sono backtest di vendor o in-sample (vedi `04_concetti_retail.md`). Quindi non superano il filtro "effetto atteso ≥ 3 × costo". Si testano lo stesso, **per chiudere la mappa** su richiesta del committente, in **un'unica famiglia di test con correzione di Holm**, con regole canoniche e **nessun parametro ottimizzato**. Ci si aspetta che muoiano: se muoiono, non si riaprono.

## 1. Dati e convenzioni
Come T1 e T2 con i loro emendamenti:
- Alpaca SIP a 1 minuto, SPY (proxy di ES) e QQQ (proxy di NQ), prezzi non rettificati;
- solo sessione regolare 09:30–15:59 ET;
- chiusure anticipate NYSE escluse;
- punti indice = movimento × k (10 per SPY, 41 per QQQ);
- in-sample 2017–2023; hold-out 2024–fine, vincolato al verdetto in-sample.

## 2. Simulatore comune (conservativo)
- **Ingresso** al prezzo dichiarato dalla regola. Le barre successive si scorrono una alla volta.
- **Stop** toccato se low ≤ stop (long) o high ≥ stop (short): uscita al prezzo di stop.
- **Target** toccato se high ≥ target (long) o low ≤ target (short): uscita al prezzo di target.
- Se **nella stessa barra** si toccano sia stop sia target, **vale lo stop**.
- Se non si tocca né stop né target, si esce al close della barra delle 15:55.
- **Costi** per round trip: ES 0,33 punti, NQ 0,45 punti; stress 2×. Slippage e commissioni sono già inclusi nel costo.
- **Al massimo 1 trade al giorno per concetto.**

## 3. Regole (fisse, definizioni retail canoniche)
- **C1 — ORB a 5 minuti** (Crabel 1990; Zarattini-Aziz 2023).
  - Range = high/low delle barre 09:30–09:34.
  - Direzione: long se il close della barra 09:34 è sopra l'open della barra 09:30, short se è sotto; nessun trade se sono uguali.
  - Ingresso a P[09:35]; stop all'estremo opposto del range; nessun target; uscita alle 15:55.
- **C2 — Gap fill.**
  - Gap = open della barra 09:30 / close del giorno precedente (P[16:00]) − 1.
  - Si opera solo se 0,1% ≤ |gap| ≤ 1%.
  - Ingresso a P[09:35] **verso** la chiusura del gap; target = close del giorno precedente; nessuno stop; uscita al target o alle 12:00. In questa regola l'uscita alle 12:00 sostituisce quella delle 15:55.
- **C3 — VWAP come calamita.**
  - VWAP di sessione dalle 09:30, calcolato su (H+L+C)/3 × volume.
  - Dalle 10:00 alle 14:30: alla prima barra il cui close dista dal VWAP almeno lo 0,3%, si entra al close di quella barra **verso** il VWAP.
  - Target = VWAP al momento dell'ingresso; nessuno stop; uscita al target o alle 15:55.
- **C4 — FVG (Fair Value Gap) su barre a 5 minuti**, aggregate dalle barre a 1 minuto a partire dalle 09:30.
  - FVG rialzista: low(barra 3) > high(barra 1). FVG ribassista: high(barra 3) < low(barra 1).
  - Si considera il primo FVG la cui barra 3 si chiude fra le 09:45 e le 14:00.
  - Ingresso al primo ritorno nel gap dopo la sua formazione, su barre a 1 minuto, entro le 15:00: per il rialzista il low tocca high(barra 1) e si entra long a quel prezzo; per il ribassista è simmetrico.
  - Stop = low(barra 1) per il long, high(barra 1) per lo short. Target = 2 × il rischio. Uscita alle 15:55.

## 4. Test e criteri
La famiglia è di 8 test: 4 concetti × 2 strumenti.

**In-sample (2017–2023).** Un test sopravvive solo se valgono tutte queste condizioni:
1. t di Newey-West (5 lag) **> 3** sul P&L giornaliero netto (giorni validi, 0 nei giorni senza trade);
2. p unilaterale corretto con Holm sugli 8 test < 0,05;
3. media > 0 con stress 2×;
4. almeno 5/7 anni positivi;
5. il concetto sopravvive **su entrambi gli strumenti**.

**Hold-out (2024–fine).** Solo per i sopravvissuti, con t > 1,5.

**Esito:** se nessuno sopravvive, **T4 MORTO** e la mappa dei concetti retail su ES/NQ è chiusa.

## 5. Metriche riportate
Per ogni concetto e strumento:
- N trade, win rate, payoff, expectancy lorda e netta (punti e $), profit factor, Sharpe, max drawdown, t, p con Holm, anni positivi;
- frequenza di raggiungimento del target (C2–C4);
- frequenza di stop (C1, C4).

## Emendamento 1 — 2026-11-10, chiarimenti registrati PRIMA di qualsiasi risultato
Emersi scrivendo il codice; non cambiano le regole, colmano casi non specificati.
- **C2:** se a P[09:35] il gap è già chiuso (il prezzo ha già raggiunto o superato il close precedente), non si opera.
- **C4:** conta solo il primo FVG ammesso della giornata. Se non viene ritestato entro le 14:59, quel giorno non si opera e non si cerca un secondo FVG. Nella barra d'ingresso, toccata per contatto, si controlla solo lo stop (conservativo).
- **C3:** l'ingresso avviene al close della barra di deviazione; la simulazione parte dalla barra successiva.
