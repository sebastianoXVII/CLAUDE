# Sensibilità ai parametri della Noise Area su NQ (QQQ×41): diagnostico, NON decisionale

**Dati:** QQQ 2017–2026, già visti in T6, quindi questa analisi non è evidenza nuova. Costo MNQ 0,85 punti; Sharpe per 1 MNQ. Il codice congelato del forward test (`t6_engine.py`) non è stato modificato: i parametri sono stati cambiati solo in memoria.

| Frequenza delle decisioni | Lookback (giorni) | 2017–2024 Sharpe (t) | 2025–2026 Sharpe (t) |
|---|---|---|---|
| 15 min | 7 / 10 / 14 / 20 / 30 | 1,28 / 1,22 / 1,24 / 1,26 / 1,12 (t 3,5–4,0) | 0,37 / 0,49 / 0,54 / 0,37 / 0,20 |
| **30 min** | 7 / 10 / **14** / 20 / 30 | 1,65 / 1,45 / **1,50** / 1,48 / 1,38 (t 4,5–5,1) | 0,62 / 0,65 / **1,07** / 0,68 / 0,58 |
| 60 min | 7 / 10 / 14 / 20 / 30 | 1,56 / 1,49 / 1,63 / 1,47 / 1,53 (t 4,7–5,3) | 0,90 / 0,90 / 1,18 / 1,08 / 1,18 |

## Lettura
- **La strategia non è fragile.** In 2017–2024 tutte le 15 combinazioni sono positive, con t fra 3,5 e 5,3. Nel 2025–2026 lo sono di nuovo tutte e 15. Il segnale non dipende dai valori esatti scelti dagli autori: è la firma di un fenomeno reale (trend intraday su NQ), non di un risultato ottimizzato. Il rischio di overfitting sui parametri è basso.
- **La frequenza a 15 minuti è peggiore:** più trade, quindi più costi e più falsi segnali. Le frequenze a 30 e 60 minuti si equivalgono.
- **Disciplina: i parametri restano 14 giorni e 30 minuti**, come da pre-registrazione e da codice congelato. Passare ora a 60 minuti perché nel 2025–26 sembra rendere leggermente di più sarebbe una scelta a posteriori. Un'eventuale variante andrebbe pre-registrata e testata su dati nuovi.
- **La conferma decisiva resta T7**, su NQ 2008–2016, dati mai visti.
