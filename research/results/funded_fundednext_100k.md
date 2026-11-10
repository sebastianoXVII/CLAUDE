# Fase funded FundedNext Stellar 100K: simulazione a 12 mesi (candidato Noise Area NQ)

**Natura:** analisi condizionata al candidato, valida solo se T7 conferma l'edge.

**Regole verificate su help.fundednext.com il 2026-11-10** (articolo "Stellar 2-Step Challenge"):
- **Challenge:** target 8% + 5%; perdita giornaliera 5%; perdita massima 10% sul saldo iniziale, statica; 5 giorni minimi per fase; nessun limite di tempo; 100K a 549,99 $.
- **Conto funded:** stessi limiti (5% giornaliera, 10% statica); rischio aperto massimo 3% in ogni momento; payout dopo 21 giorni, poi ogni 14 se il conto è in profitto; quota trader 80%; regola news: i trade a ±5 minuti da una news ad alto impatto contano solo al 40% dei profitti.
- **EA e bot non ammessi sui conti da 50K in su:** l'esecuzione è manuale, quindi nessun problema.
- **Ipotesi di modello:** a ogni payout si preleva tutto il profitto e il saldo torna al valore iniziale.

## Risultati (orizzonte 12 mesi, 3.000 simulazioni, costo CFD 2 punti per trade)
| Taglia | Edge storico: payout medio/anno · conto perso | Edge dimezzato: payout medio/anno · conto perso |
|---|---|---|
| **6 $/punto (≈ 3 MNQ)** | **6.907 $ · 2%** | **4.939 $ · 6%** |
| 8 $/punto (≈ 4 MNQ) | 9.149 $ · 9% | 6.495 $ · 20% |
| 12 $/punto (≈ 6 MNQ, la taglia ottimale della challenge) | 12.756 $ · 36% | 8.946 $ · 53% |

## Lettura
- **L'intuizione del committente di dimezzare la taglia nel conto funded è confermata dai numeri.** Con i payout il profitto viene prelevato e il cuscinetto sopra la perdita massima non cresce mai. Restare alla taglia della challenge (12 $/punto) significa perdere il conto nel 36–53% dei casi in un anno. A metà taglia (6 $/punto) il rischio scende al 2–6%, e il payout atteso è circa il 55% di quello a taglia piena.
- **Regola proposta:** challenge a circa 12 $/punto, funded a circa 6 $/punto, cioè circa 0,2% del conto per trade sulla perdita media. Si torna a 8 $/punto solo dopo aver accumulato un cuscinetto pari ad almeno il 5% del conto. La regola è da pre-registrare e verificare con la simulazione prima dell'uso.
- **Ordine di grandezza, per conto:**
  - payout circa 5–7 mila $ l'anno, con molta dispersione: 10° percentile fra 0 e 1.400 $;
  - meno i 550 $ di fee;
  - probabilità di superare la challenge del 41–63%, in circa 7 mesi;
  - prima che T7 confermi l'edge, il valore atteso netto è positivo **solo sulla carta**.
