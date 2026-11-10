# T2 — Reazione ai livelli dove si accumulano gli stop (pre-registrazione)

**Stato:** PRE-REGISTRATO, nessun risultato osservato. **Data:** 2026-11-10. Il commit di questo file precede qualsiasi esecuzione.
**Regola:** come T1. Il testo è congelato; ogni modifica successiva ai dati è una nuova ipotesi.

## 1. Ipotesi e meccanismo
Osler (2003 JF; 2005 JIMF, FX) documenta due cose. Gli ordini stop si accumulano appena oltre i livelli salienti; quando il prezzo li attraversa, gli stop scattano e il movimento accelera (*cascata*). I take-profit, invece, si accumulano *sui* livelli e producono rimbalzi. Il folklore retail della "liquidity sweep" predice il contrario della cascata: rottura del livello, raccolta degli stop, inversione. **Le due teorie predicono segni opposti**, quindi il test è **bilaterale**.

**H0:** dopo il primo attraversamento di un livello saliente, il rendimento nella direzione della rottura è uguale a quello dopo l'attraversamento di un livello *placebo*.

## 2. Dati
- Alpaca SIP a 1 minuto, SPY (proxy di ES) e QQQ (proxy di NQ), dal 2016. Valgono le convenzioni di T1 e degli emendamenti 1–2:
  - P(t) = close della barra che inizia a t−1m;
  - si escludono le chiusure anticipate NYSE (`exchange_calendars`);
  - punti indice = movimento non rettificato × k (10 per SPY, 41 per QQQ).
- I livelli e i rendimenti si calcolano sui prezzi **non rettificati** (`adjustment=raw`). I livelli sono relativi allo stesso giorno o al giorno prima, quindi lo stacco del dividendo conta solo nei giorni ex-dividendo; si accetta come rumore.
- **Numeri tondi esclusi.** SPY×10 e QQQ×41 non coincidono con i livelli dell'indice o dei futures (base e dividendi). Il test sui numeri tondi è rimandato a quando ci saranno dati futures CME.

## 3. Livelli (noti prima dell'apertura)
| Famiglia | Livello superiore U | Livello inferiore D |
|---|---|---|
| **PD** (previous day) | massimo della sessione regolare del giorno valido precedente | minimo della sessione regolare del giorno valido precedente |
| **PM** (pre-market) | massimo delle barre 04:00–09:29 ET dello stesso giorno | minimo delle barre 04:00–09:29 ET |

Un livello è ammesso solo se all'apertura (prezzo P[09:35]) il prezzo sta **dalla parte giusta**: sotto U per i livelli superiori, sopra D per quelli inferiori. I giorni con apertura già oltre il livello sono esclusi per quel livello.

**Placebo.** Per ogni livello vero si costruiscono 2 livelli placebo a distanza fissa: U ± 0,3 × R e D ± 0,3 × R, dove R è il range della sessione regolare del giorno precedente. Si applicano le stesse regole di ammissione.

## 4. Evento ed esito
- **Finestra:** barre che iniziano fra 09:35 e 15:59 − H.
- **Attraversamento:** la prima barra il cui high è ≥ U (per un livello superiore) o il cui low è ≤ D (per uno inferiore). Si conta solo il **primo** attraversamento di ciascun livello in ciascun giorno.
- **Ingresso:** P_in = close della barra di attraversamento.
- **Direzione:** s = +1 per U, −1 per D.
- **Esito:** y = s × (P[t_in + H] − P_in) × k, in punti indice, con H ∈ {15, 30} minuti.

## 5. Test
**Stadio 1 — l'effetto esiste?** 8 test: 2 famiglie (PD, PM) × 2 orizzonti × 2 strumenti.
- Regressione OLS di y su una costante e su un indicatore "livello vero" (1 = vero, 0 = placebo), con errori standard **clusterizzati per giorno**. La statistica è il t del coefficiente dell'indicatore.
- Sopravvive solo se valgono tutte e due le condizioni:
  - |t| > 3 e p bilaterale corretto con Holm sugli 8 test < 0,05;
  - il segno è uguale su ES e NQ per la stessa famiglia e lo stesso orizzonte.

**Stadio 2 — è tradabile?** Solo per le combinazioni sopravvissute allo stadio 1.
- **Regola:** a ogni attraversamento di un livello vero si entra a P_in nella direzione s × segno(effetto) e si esce dopo H minuti. Se ci sono più trade nello stesso giorno, si sommano nel P&L giornaliero.
- **Costi:** come T1, sezione 4 (ES base 0,33 pt; NQ base 0,45 pt; stress 2×).
- Sopravvive solo se valgono tutte queste condizioni:
  - t di Newey-West (5 lag) > 3 sul P&L giornaliero netto;
  - media > 0 con stress 2×;
  - almeno 5/7 anni positivi;
  - il P&L medio per trade sui livelli veri batte quello della stessa regola sui placebo.

## 6. Campioni
- **In-sample:** 2017-01-01 → 2023-12-31.
- **Hold-out:** 2024-01-01 → fine. Si calcola solo per le combinazioni sopravvissute agli stadi 1 e 2, con t > 1,5 sul P&L netto, e solo leggendo il verdetto in-sample salvato.
- **Esito:** se nessuna combinazione sopravvive, **T2 MORTO**.

## 7. Metriche riportate
Per ogni combinazione:
- N eventi veri e placebo;
- media di y vera e placebo;
- coefficiente, t e p dello stadio 1, con p corretto Holm;
- frequenza di "sweep": quota di eventi in cui entro H minuti il close torna dalla parte opposta del livello, per livelli veri e placebo.

Per lo stadio 2: le stesse metriche di T1, sezione 7.
