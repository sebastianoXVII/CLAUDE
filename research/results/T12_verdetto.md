# T12 — Noise Area su oro, Russell 2000 e Dow: verdetto

**Esecuzione unica:** 2026-11-10, `research/run_t12.py`. **Risultati:** `T12_risultati.json`. **Pre-registrazione:** `research/preregistration/T12_noise_area_altri_mercati.md`.

## Verdetto: NESSUNO STRUMENTO CONFERMA. La Noise Area resta un candidato solo per NQ.

## Dati e controlli
- Dati Alpaca SIP a 1 minuto, rettificati e grezzi, dal 2016-01-04 al 2026-11-09.
- 2.729 giorni di sessione regolare per ciascuno, di cui circa 2.710 con almeno 300 barre. Nessun duplicato.
- **Controllo della pipeline:** QQQ passato nello stesso codice in bp dà Sharpe 1,60 e t 5,17 nel 2017–2024, e Sharpe 1,08 e t 1,49 nel 2025+. Riproduce T6 (1,59 / 5,15 e 1,12 / 1,58), quindi il codice è corretto.
- Revisione indipendente del codice fatta prima dell'esecuzione: nessun problema bloccante.

## Risultati (P&L netto in punti base; la decisione si basa sul fuori campione 2025+)
| | Trade | Netto bp/trade | Sharpe | t NW | p Holm | Stress 2× (bp/giorno) | Conferma |
|---|---|---|---|---|---|---|---|
| **GLD 2025+** | 376 | +0,92 | 0,26 | 0,38 | 1,00 | −0,07 | NO |
| **IWM 2025+** | 417 | −2,99 | −0,82 | −1,18 | 1,00 | −4,17 | NO |
| **DIA 2025+** | 407 | −0,12 | −0,05 | −0,06 | 1,00 | −0,81 | NO |
| GLD 2017–24 (informativo) | 1.680 | −0,69 | −0,34 | −0,98 | | −1,44 | |
| IWM 2017–24 (informativo) | 1.924 | −2,91 | −0,80 | −2,12 | | −4,39 | |
| DIA 2017–24 (informativo) | 1.763 | −0,24 | −0,08 | −0,25 | | −0,93 | |

Anni positivi nel 2017–2024: GLD 3/8, IWM 2/8, DIA 3/8.

## Correlazioni del P&L giornaliero della strategia con QQQ
| | 2017–24 | 2025+ |
|---|---|---|
| GLD | 0,03 | −0,04 |
| IWM | 0,41 | 0,37 |
| DIA | 0,48 | 0,46 |

## Cosa significa (lettura del quant lead)
1. **La strategia non è un effetto generale.** Sugli indici azionari funziona solo sul Nasdaq-100: SPY è già morto in T6, IWM è negativo e DIA è a zero. Gli autori dichiarano uno Sharpe medio di 0,60 su 33 futures, ma noi non lo riproduciamo su questi tre mercati. Va precisato che usiamo ETF, non futures.
2. **È un segnale di allarme per NQ, non una prova contro.** Se un effetto esiste su 1 indice su 4, una parte del risultato di QQQ nel 2017–2024 può essere fortuna di selezione o il trend eccezionale del Nasdaq in quegli anni. La probabilità a priori che T7 confermi si abbassa. T7 resta il test decisivo, su dati che nessun test ha mai toccato.
3. **Diversificazione:** nessuno strumento è utilizzabile. GLD sarebbe scorrelato, ma non ha edge.
4. **Niente salvataggi:** per pre-registrazione non si provano altri parametri né altri strumenti per "trovare" quello che funziona.

## Note sulle unità
- I campi `*_usd*`, `win_rate` ed `expectancy_*` del JSON vengono da `T1.metrics`. Sono in bp e calcolati per giorno con trade; il valore per singolo trade è `netto_bp_per_trade`.
- I costi sono stime sui micro futures (GLD 1,0 bp, IWM 1,6 bp, DIA 0,8 bp).
