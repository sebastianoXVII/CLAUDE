# T2 — Reazione ai livelli di stop (PDH/PDL, massimo/minimo pre-market) contro placebo: **MORTO**

**Data:** 2026-11-10. **Pre-registrazione:** `research/preregistration/T2_livelli_di_stop.md`, con l'emendamento 1 registrato prima dei risultati. **Dati:** `T2_in_sample.json`.

## Esito in-sample 2017–2023
**0 combinazioni su 8 superano lo stadio 1**, quindi lo stadio 2 e l'hold-out non sono stati calcolati.

| Combinazione | Eventi veri / placebo | y medio vero / placebo (pt) | t | t con controlli | p Holm |
|---|---|---|---|---|---|
| ES PD 15m | 546 / 1.009 | +0,80 / −0,03 | 2,40 | 2,31 | 0,13 |
| ES PD 30m | 522 / 974 | +1,00 / +0,30 | 1,44 | 1,28 | 1,00 |
| ES PM 15m | 1.554 / 1.820 | +0,02 / −0,10 | 0,51 | 1,03 | 1,00 |
| ES PM 30m | 1.531 / 1.780 | −0,06 / −0,23 | 0,52 | 0,84 | 1,00 |
| NQ PD 15m | 569 / 1.029 | +1,96 / +1,47 | 0,35 | 0,49 | 1,00 |
| NQ PD 30m | 561 / 1.014 | +1,37 / +2,48 | −0,59 | −0,51 | 1,00 |
| NQ PM 15m | 1.453 / 1.768 | −0,73 / −0,39 | −0,34 | 0,04 | 1,00 |
| NQ PM 30m | 1.435 / 1.738 | −0,39 / −0,32 | −0,05 | −0,01 | 1,00 |

## Lettura
- **Né la "cascata di stop" (Osler) né lo "sweep" retail** producono, dopo l'attraversamento, un movimento diverso da quello di un livello qualsiasi. Il miglior candidato, ES PD 15m con +0,8 punti di continuazione, non supera la soglia ed è contraddetto da NQ.
- **Per lo sweep la frequenza di base è decisiva.** Dopo aver attraversato un livello *qualsiasi*, entro 15–30 minuti il prezzo torna dall'altra parte nel 75–88% dei casi. Ai livelli veri succede **meno spesso** che ai placebo: 75% contro 84% su ES PD 15m. Il "pattern sweep" che i trader retail vedono sui grafici è quindi il comportamento normale del prezzo attorno a qualsiasi linea, non un segnale. *(Dato descrittivo, non pre-registrato come test: genera ipotesi, non è evidenza.)*
- **Limite dichiarato:** SPY e QQQ come proxy, senza la sessione overnight di ES. I numeri tondi non sono stati testati, perché il proxy non li rappresenta.

## Controlli di qualità
- Il motore è sviluppato con TDD: 50 test in totale tra T1 e T2.
- La code review indipendente prima dell'esecuzione ha trovato un fattore confondente serio (distanza dall'apertura e ora dell'attraversamento) che poteva produrre un falso "sweep" con t fino a −3,2. È stato corretto con una regressione con controlli, verificata da un test su un confondente puro.
- Conteggi plausibili: PDH/PDL ammessi e attraversati in circa il 30% dei giorni per lato; livelli pre-market in circa il 90%.

## Cosa non si fa
Non si cercano soglie, orizzonti o livelli alternativi su questi dati: sarebbe data snooping. I livelli pre-sessione, cuore del concetto "ICT" con una base reale, rientrano nella famiglia PM e sono morti con T2.
