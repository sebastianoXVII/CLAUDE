# T5 — Ipotesi generate da T4, testate SOLO sull'hold-out (pre-registrazione)

**Stato:** PRE-REGISTRATO. **Data:** 2026-11-10. Il commit precede l'esecuzione.
**Natura:** queste ipotesi sono nate **guardando i dati in-sample 2017–2023** di T4, quindi lì non hanno valore di evidenza. L'unico test onesto è sul campione **2024-01-01 → fine dati**, che nessun test ha mai calcolato (T1, T2 e T4 sono morti in-sample, quindi i loro hold-out non sono stati eseguiti). **Si esegue una sola volta.** Comunque vada, non si ritoccano le regole: il campione verrebbe consumato.

## Ipotesi
- **H5a — Continuazione dal VWAP:** è la regola C3 di T4 **con il segno invertito**. Dalle 10:00 alle 14:30, alla prima barra il cui close dista almeno lo 0,3% dal VWAP di sessione, si entra al close **nella direzione della deviazione** (lontano dal VWAP).
  - **Stop:** VWAP al momento dell'ingresso (è il target di C3 invertito).
  - **Target:** nessuno.
  - **Uscita:** 15:55.
  - È la stessa regola con le posizioni scambiate: chi entrava verso il VWAP ora esce dove quel trade prendeva profitto.
- **H5b — ORB a 5 minuti:** identico a C1 di T4, con tutti gli emendamenti. Su NQ era il migliore in-sample (t = 1,74), ma non significativo.

## Dati, simulatore, costi
Identici a T4, emendamenti 1–2 compresi: Alpaca SPY/QQQ grezzi, k = 10 e 41, costi ES 0,33 e NQ 0,45 punti, stress 2×, simulatore conservativo con stop realistico sui gap.

## Criteri (4 test: 2 ipotesi × 2 strumenti)
Un'ipotesi sopravvive solo se valgono TUTTE queste condizioni:
1. t di Newey-West (5 lag) sul P&L giornaliero netto > 2,0 su **entrambi** gli strumenti. La soglia è più bassa di 3 perché il campione è di circa 2,8 anni ed è una conferma fuori campione di un'ipotesi già nota, non una scoperta.
2. p unilaterale corretto con Holm sui 4 test < 0,05 su entrambi.
3. Media > 0 con stress 2× su entrambi.

## Conseguenze
- **Se un'ipotesi sopravvive:** diventa **candidato**, non strategia. Il passo successivo è la conferma su futures CME veri, poi la simulazione Monte Carlo della challenge e infine la demo.
- **Se nessuna sopravvive:** T5 MORTO, e l'hold-out 2024–fine è consumato per queste ipotesi.
