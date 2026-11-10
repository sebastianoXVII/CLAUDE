# Confronto dei programmi prop sul candidato Noise Area NQ

**Natura:** analisi **condizionata** al candidato (in attesa di T7), non evidenza di edge. Le regole Topstep sono verificate sul sito ufficiale; FTMO e FundedNext vengono da sintesi delle pagine ufficiali o da fonti secondarie (vedi `research_notes/Gap di mercato testabili/05_prop_firm_regole_2026.md`). Vanno **riverificate prima di comprare**.
**Metodo:** giorni reali della strategia 2017–2026 (QQQ→NQ), minimo intraday dalle barre a 1 minuto, block bootstrap con 3.000 simulazioni. Costi: MNQ 0,85 punti, CFD US100 2 punti per round trip (stress a 4).

| Programma | Taglia migliore | Probabilità di superare tutte le fasi (edge storico / dimezzato) | Tempo mediano |
|---|---|---|---|
| **FundedNext Stellar 2-Step 100K** (statico 10%, giornaliero 5%, target 8% + 5%) | 12 $/punto (≈ 6 MNQ) | **63% / 41%** | circa 150 giorni di borsa |
| FTMO 2-Step 100K CFD (statico 10%, giornaliero 5%, target 10% + 5%) | 12 $/punto | 58% / 35% (29% con spread raddoppiato) | circa 170 giorni |
| Topstep 50K (trailing 2K EOD, consistency 55%) | 2 MNQ | 41% / 26% | circa 64 giorni |
| FTMO Futures Pro 50K (trailing 3K, limite giornaliero 1K, consistency 40%) | 2 MNQ | 28% / 16% | circa 66 giorni |

## Decisione (quant lead), valida solo se T7 conferma l'edge
1. **Programma principale: FundedNext Stellar 2-Step 100K, CFD NDX100.** Il drawdown statico è il più adatto a una strategia trend con serie negative fino a 20 giorni: a parità di edge è quello che passa più spesso.
   - **Pro:** probabilità più alta e capitale finanziato più grande.
   - **Contro:** è **lento** (circa 7 mesi per le due fasi).
   - **Regola sulle news:** nel conto funded i trade entro ±5 minuti da una news ad alto impatto contano solo al 40%. La strategia decide alle :00 e alle :30, quindi i trade delle 10:00 coincidono con le news delle 10:00 ET. Va gestito con un filtro sulle news pre-registrato.
2. **Alternativa più rapida: Topstep 50K a 2 MNQ.** Circa 3 mesi, ma meno probabilità e massimali di payout bassi.
3. **Escluso:** FTMO Futures Pro, penalizzato dalla consistency al 40% e dal limite giornaliero di 1K su questa strategia.
4. **Rischio per trade:** non l'1% del nominale. Sul 100K statico, 6 MNQ equivalenti corrispondono a circa lo 0,4% del conto per trade (perdita media) e al 4% del drawdown disponibile.
