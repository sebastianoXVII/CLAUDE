# T12 — Noise Area su altri mercati: oro, Russell 2000, Dow (pre-registrazione)

**Stato:** PRE-REGISTRATO, nessun dato di questi strumenti scaricato o guardato. **Data:** 2026-11-10.

## 1. Perché
- Il candidato Noise Area su NQ (T6) ha bisogno di conferme indipendenti.
- Gli autori dichiarano (FAQ Q13 del paper) un test su 33 futures fino a settembre 2024: Sharpe medio 0,60, solo 2 strumenti negativi, ma senza indicarne i nomi.
- Per la scala sui conti prop servono strumenti poco correlati con NQ.

## 2. Strumenti (scelti PRIMA di guardare, solo 3)
| ETF (dati Alpaca SIP a 1 minuto) | Mercato | Futures o CFD operabile |
|---|---|---|
| **GLD** | oro | MGC / XAUUSD |
| **IWM** | Russell 2000 | M2K / US2000 |
| **DIA** | Dow Jones 30 | MYM / US30 |

## 3. Regole
Sono **identiche a T6 con gli emendamenti 1–2**, cioè il codice congelato `t6_engine.py` con 14 giorni di lookback e decisioni ogni 30 minuti:
- segnale +1 / −1 / 0 secondo la banda **e** il VWAP;
- dividendo sottratto dal close precedente;
- chiusura alle 16:00;
- chiusure anticipate NYSE escluse.

## 4. Costi (per round trip, in punti base del prezzo; stima sui micro futures)
| | Commissione + 1 tick di slippage | Costo base | Stress 2× |
|---|---|---|---|
| Oro (MGC) | circa 1,2 $ + 1 $ su un nozionale di circa 26.000 $ | **1,0 bp** | 2,0 bp |
| Russell (M2K) | circa 1,2 $ + 0,5 $ su un nozionale di circa 11.000 $ | **1,6 bp** | 3,2 bp |
| Dow (MYM) | circa 1,2 $ + 0,5 $ su un nozionale di circa 22.000 $ | **0,8 bp** | 1,6 bp |

Queste sono stime, da verificare prima di andare live. Il P&L di ogni trade è in rendimento: lato × (P_uscita / P_ingresso − 1) − costo.

## 5. Criteri (famiglia di 3 test, correzione di Holm)
**Periodo decisionale:** 2025-01-02 → fine dati. È il fuori campione rispetto al paper, che arriva a dicembre 2024. Uno strumento **conferma** se valgono tutte queste condizioni:
1. t di Newey-West (5 lag) sul rendimento giornaliero netto > 1,65 e p corretto con Holm sui 3 test < 0,05;
2. media > 0 con stress 2×.

**Informativo, non decisionale:** il 2017–2024 è nel periodo degli autori. Si riportano anche la correlazione dei rendimenti giornalieri con NQ (QQQ, stesso periodo) e la correlazione fra gli strumenti.

**Esito:**
- **Uno o più strumenti confermano:** si candidano a strumenti aggiuntivi e diversificanti, ma restano da confermare con un forward test prima di qualsiasi uso.
- **Nessuno conferma:** la Noise Area resta un candidato solo per NQ.
