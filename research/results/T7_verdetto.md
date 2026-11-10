# T7 — Noise Area su NQ, campione mai usato 2010–2016: **INCONCLUSIVO** (debole, non tradabile)

**Data:** 2026-11-10. **Pre-registrazione:** `research/preregistration/T7_noise_area_nq_conferma.md`, emendamenti 2 e 3, registrati prima di qualsiasi esecuzione. **Dati:** `T7_risultati.json`, `T7_trades.parquet` e `T7_proxy_check.json`. **Fonte:** HistData NSXUSD a 1 minuto, con VWAP calcolato sul profilo di volume QQQ.

## 1. Validazione del proxy (vincolante): VALIDA
Su QQQ 2017–2024, con gli stessi prezzi, il VWAP vero e il VWAP da profilo producono:
- trade identici nel **96,5%** dei giorni, contro una soglia del 90%;
- un P&L giornaliero con correlazione **0,990**, contro una soglia di 0,90.

Regge anche la prova "fuori tempo", con il profilo 2021–2024 applicato al 2017–2019: accordo 95,7%, correlazione 0,995. Il VWAP approssimato non cambia la strategia.

## 2. Risultato sul periodo di test 2010-12-07 → 2016-12-30 (1.479 giorni)
Risultati con 1 NQ pieno, al netto dei costi base:

| Trade | Win rate | Lordo/trade | Netto/trade | Sharpe | t NW | Max DD | Stress 2× | MNQ |
|---|---|---|---|---|---|---|---|---|
| 1.275 | 36% | +1,03 pt | +0,58 pt (**+11,6 $**) | **0,55** | **1,35** | −6.340 $ | +0,11 pt/giorno | +0,16 pt/giorno |

P&L in punti per anno:

| Anno | P&L (pt) |
|---|---|
| 2010+2011 (accorpati) | +125 |
| 2012 | +284 |
| 2013 | −5 |
| 2014 | +206 |
| 2015 | +208 |
| 2016 | −78 |

Anni positivi: 4 su 6.

Criteri:

| Criterio | Esito |
|---|---|
| t > 3 | **no** |
| Stress 2× > 0 | sì |
| MNQ > 0 | sì |
| Almeno 2/3 degli anni positivi | sì |

**Esito pre-registrato: INCONCLUSIVO.**

Diagnostico: il P&L giornaliero di NSXUSD e quello di QQQ×41 hanno correlazione **0,973** sul 2017–2024. Il CFD riproduce fedelmente il segnale, quindi la debolezza del 2010–16 non è un artefatto della fonte dati.

## 3. Lettura
- **Il segno regge, la forza no.** Su un campione mai toccato la strategia è positiva, in 4 anni su 6 e anche a costi doppi. Lo Sharpe però è circa 0,55, contro l'1,6 del 2017–2024 e l'1,1 del 2025–26. Il risultato forte del periodo recente coincide con il periodo in cui gli autori hanno costruito la regola e con un regime di alta volatilità del Nasdaq. Non è un edge stabile.
- **L'acquisto di FirstRate non serve.** L'emendamento 1 prevedeva di comprare il 2008–2011 in caso di esito inconclusivo. Ma con Sharpe 0,55 servirebbero circa **30 anni** di dati per arrivare a t = 3. Tre anni in più non possono cambiare l'esito: spendere sarebbe un errore. **Raccomandazione: non comprare.**
- **Uso prop: no.** Con un MNQ il guadagno atteso è di circa 0,3 $ al giorno dopo i costi. Non sostiene un conto prop, e non si mette denaro su un segnale con t = 1,35.
- **Stato:** la Noise Area resta un *indizio* senza conferma. Il forward test notturno già attivo (`research/forward/`) continua senza costi, solo come osservazione.
