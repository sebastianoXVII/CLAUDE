# T5 — Ipotesi generate da T4, testate sull'hold-out 2024–2026 (esecuzione unica): **MORTO**

**Pre-registrazione:** `research/preregistration/T5_holdout_ipotesi_generate.md`. **Dati:** `T5_holdout.json`. **Periodo:** 2024-01-02 → 2026-11-06.

| | Trade | Netto $/trade | t NW | P&L pt per anno |
|---|---|---|---|---|
| ES continuazione VWAP | 480 | −10 | −0,16 | 2024 +187, 2025 −126, 2026 −159 |
| NQ continuazione VWAP | 623 | −77 | −0,86 | 2024 +674, 2025 −1.841, 2026 −1.232 |
| ES ORB | 707 | −16 | −0,38 | 2024 −361, 2025 −34, 2026 +172 |
| NQ ORB | 707 | +116 | 1,20 | 2024 +1.745, 2025 +2.384, 2026 −28 |

## Lettura
- **La continuazione dal VWAP non si replica.** Il t = −3,3 di "VWAP come calamita" su NQ in-sample era rumore, o un regime ormai finito. È la dimostrazione pratica del perché un'ipotesi nata dai dati va testata su dati mai visti.
- **L'ORB su NQ è l'unico segnale debole ma persistente** di tutto il programma: t = 1,74 in-sample (2017–23) e t = 1,20 fuori campione (2024–26), positivo in 7 anni su 10. Su ES però non esiste: è un indizio, non un edge. Possibili spiegazioni:
  - un premio specifico del Nasdaq (trend più forti);
  - il costo relativo più basso su NQ.

  Va trattato come **ipotesi a bassa priorità**, da verificare su NQ vero, con dati futures, prima di qualunque uso.
- **Hold-out 2024–fine:** ora consumato per queste due ipotesi.
