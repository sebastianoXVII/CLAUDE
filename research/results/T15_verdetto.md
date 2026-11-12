# T15: Trend following diversificato su 23 CFD, verdetto

**Esito:** **MORTO**, per entrambe le varianti. **Data:** 2026-11-12. L'esecuzione in-sample è unica (lock `T15_insample.started`). L'hold-out 2020–2024 **non è stato calcolato** e resta intatto, perché nessuna variante è sopravvissuta.

## Risultati in-sample (2011–2019, 2.335 giorni, 23 strumenti)
Costi: base pre-registrata (transazione più finanziamento al 3% annuo).

| | V1 (MOP, 12 mesi) | V2 (HOP, 1/3/12 mesi) | Soglia |
|---|---|---|---|
| t di Newey-West, netto | **−1,59** | **−1,95** | > 3,0 (Holm) |
| Sharpe annuo, netto | −0,52 | −0,63 | — |
| p di Holm | 1,00 | 1,00 | < 0,05 |
| Media con costi 2× | negativa | negativa | > 0 |
| Anni positivi | 2/9 | 1/9 | ≥ 6/9 |

**Diagnostica a costi zero** (calcolata dopo il verdetto, non decisionale):
- V1: t = 0,27, Sharpe 0,09;
- V2: t = −0,14, Sharpe −0,05.

**Anche senza nessun costo, il trend following su questo universo non ha avuto rendimento nel 2011–2019.** I costi spiegano il segno negativo, ma non l'assenza di edge.

Per anno, V1 netto (somma dei rendimenti giornalieri, scala di 40% di volatilità per strumento):

| 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|---|
| −24% | −9% | +14% | −3% | −1% | −31% | +16% | −23% | −13% |

**Indicatori prop** (descrittivi, V1 scalata a 10% di volatilità annua):
- rendimento −5,2% l'anno;
- max drawdown −44%;
- giorno peggiore −4,1%;
- quota di finestre di 10 giorni positive: 46%.

## Controlli: perché il risultato non è un bug
**Meccanica.** I grandi trend noti vengono catturati con P&L lordo positivo:

| Trend | Movimento del prezzo | P&L lordo dello strumento |
|---|---|---|
| WTI, 2° semestre 2014 | −55% | +1,14 |
| USDJPY, 2013 | +21% | +0,76 |
| EURUSD, 2014–2015 | −22% | +0,67 |
| Oro, 2013 | −29% | +0,73 |

**Processo:**
- due code review indipendenti;
- 211 test unitari;
- preflight sui dati;
- Emendamento 2, sulle rotture del dato, registrato prima di qualunque P&L e cieco su 17 strumenti su 23.

**Dati.** HistData verificata. Le due sostituzioni di serie trovate (DAX 2020–2023, Euro Stoxx 50 da dicembre 2018) sono escluse secondo la regola pre-registrata. Nell'in-sample tocca solo la coda di Euro Stoxx 50.

## Interpretazione
- **Perché va male.** Coerente con la letteratura: il trend following ha avuto un decennio 2011–2019 debole. Inoltre a questo universo mancano **obbligazioni e tassi**, che negli indici CTA hanno prodotto gran parte dei guadagni del 2014 e del 2019. Con i CFD retail non sono negoziabili in modo pulito.
- **Il costo che pesa di più è il finanziamento overnight.** Sul forex la posizione arriva al tetto di 4× di leva, e il 3% annuo sul nozionale costa circa il 12% l'anno per strumento, contro il 40% di volatilità. È strutturale per chi tiene posizioni a leva sui CFD.
- **Conclusione operativa.** Nessuna variante di trend following giornaliero su CFD è utilizzabile per la prop. Non si ritoccano parametri, universo o costi per salvarla.
