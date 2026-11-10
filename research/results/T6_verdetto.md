# T6 — "Noise Area" (Zarattini, Aziz e Barbon): **MORTO come da pre-registrazione, ma con un candidato su NQ**

**Pre-registrazione:** `research/preregistration/T6_noise_area_momentum.md`, con gli emendamenti 1–2 registrati prima dei risultati; l'emendamento 2 usa la regola presa dal codice ufficiale degli autori. **Dati:** `T6_risultati.json`. **Diario:** `journal.sqlite`, strategia `T6_noise_area`, campione `OOS_2025`, con screenshot di ogni trade in `data/charts/T6/`.

## Risultati (1 contratto, netto dei costi base)
| | Periodo | Trade | Win rate | Netto $/trade | PF | Sharpe | Max DD $ | t NW | P&L pt per anno |
|---|---|---|---|---|---|---|---|---|---|
| SPY→ES | 2017–2024 (periodo degli autori, solo informativo) | 1.733 | 39% | +57 | 1,30 | 1,04 | −14.230 | 3,22 | 2017 −102, 2018 +401, 2019 −28, 2020 +117, 2021 +351, 2022 +622, 2023 +419, 2024 +198 |
| **SPY→ES** | **2025-01 → 2026-11 (fuori campione)** | 423 | 36% | **−21** | 0,94 | −0,24 | −38.233 | **−0,35** | 2025 −28, 2026 −152 |
| QQQ→NQ | 2017–2024 | 1.694 | 41% | +143 | 1,50 | 1,59 | −14.618 | 5,15 | positivo in **8/8** anni |
| **QQQ→NQ** | **2025-01 → 2026-11 (fuori campione)** | 387 | 40% | **+223** | 1,35 | **1,12** | −32.960 | **1,58** | 2025 +1.688, 2026 +2.620 |

## Verdetto
- **La replica è fedele.** Sul periodo degli autori SPY rende con t = 3,2 e win rate per trade del 39%; il paper riporta il 37%, Sharpe 1,24 con dimensione fissa, e 1,8 cambi di esposizione al giorno, pari a circa 0,9 trade completi, come qui.
- **Fuori campione SPY non funziona** (t = −0,35). Per la regola decisionale a sequenza fissa (emendamento 2), SPY era lo strumento principale, quindi **T6 è MORTO**. La regola non si cambia dopo aver visto i dati.
- **NQ è il primo candidato serio del programma.**
  - È positivo in 10 anni su 10, con parametri **mai ottimizzati su NQ**: 14 giorni, 30 minuti e VWAP sono quelli scelti dagli autori su SPY.
  - Nel fuori campione 2025–26 ha Sharpe 1,1 e t = 1,58, appena sotto la soglia di 1,65 per un campione di soli 1,85 anni.
  - È coerente con l'ORB, positivo solo su NQ (T4/T5): il trend intraday sembra un fenomeno del Nasdaq, non dell'S&P.
- **Cautele:**
  - Il 2017–2024 su QQQ cade nel periodo in cui gli autori hanno costruito la regola, anche se su un altro strumento.
  - Il max drawdown con 1 NQ pieno arriva a circa 33.000 $: è incompatibile con un conto prop da 50K a 1 contratto pieno, e va dimensionato sui micro (MNQ).
  - NQ e SPY si sono comportati in modo opposto nel 2025–26: va escluso che sia un artefatto del proxy QQQ.

## Prossimo passo: T7
Conferma della strategia Noise Area **solo su NQ**, su dati **mai usati da nessuno** e con regole congelate oggi:
- **dati:** OANDA NAS100 a 1 minuto, periodo **2008–2016** (prima dei dati Alpaca);
- **verifica di coerenza:** confronto CFD contro QQQ sul periodo sovrapposto;
- **dimensionamento:** Monte Carlo della challenge prop con la distribuzione reale dei trade NQ su MNQ.
