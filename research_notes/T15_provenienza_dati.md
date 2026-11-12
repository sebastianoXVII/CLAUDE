# T15 — Provenienza dei dati giornalieri (nota operativa, nessun rendimento guardato)

**Data:** 2026-11-11.

## Fonte
HistData M1, dalla copia pubblica su Google Drive (id in `research/data/histdata_manifest.json`). La conversione in barre giornaliere avviene con `research/data/histdata_daily.py`: la giornata chiude alle 17:00 di New York.

## Due percorsi di conversione equivalenti
- **Da zip.** Workflow `histdata-daily-download`, con pubblicazione nel branch `data-histdata` in `histdata_daily/`.
- **Da parquet M1 già scaricato.** `histdata_daily.py --from-m1`, applicato ai file `histdata/*_1m_24h.parquet` dello stesso branch, che vengono dagli stessi zip.

**Verifica di equivalenza.** Su NSXUSD (3.649 giorni) e SPXUSD (3.650 giorni) i due percorsi danno barre **identiche**: 0 differenze su open, high, low, close e n_bars.

## Da dove viene ogni strumento
- **Via `--from-m1`:** EURUSD, GBPUSD, XAUUSD. XAUUSD ha 3.877 giorni, lo stesso numero della conversione da zip nel primo run.
- **Via zip:** NSXUSD, SPXUSD, GRXEUR, e i 17 strumenti restanti.

## Incidente di download
Google Drive ha risposto **"Quota exceeded"** dopo circa 220 file scaricati in un'ora, nei run 42976213858 e 42985560293.

Il workflow ora fa due cose:
- al primo "Quota exceeded" si ferma, invece di insistere;
- pubblica comunque i risultati parziali.

I 17 strumenti restanti si riscaricano in due lotti, a circa 24 ore di distanza.

## Lotto 1 del 2026-11-12 (run 43199539096)
**Download.** 9 strumenti in 8 minuti, senza "Quota exceeded": AUXAUD, BCOUSD, ETXEUR, FRXEUR, HKXHKD, JPXJPY, UKXGBP, WTIUSD, XAGUSD.

**Controllo descrittivo** (solo prezzi, nessun P&L):
- **ETXEUR.** Fino al 2018-12-14 i livelli sono quelli dell'Euro Stoxx 50 (circa 2.000–3.750). Dal 2018-12-17 al 2019-02-01 il file contiene un'altra serie, a 8.500–9.100: è compatibile con l'IBEX 35, ma è un'ipotesi non verificata. Il rendimento al bordo è +186%.
  - La Regola 1 dell'Emendamento 2, scritta prima di vedere questo file, spezza la serie in automatico.
  - Il secondo segmento dura circa 35 giorni e non raggiunge mai 252 giorni di storia.
  - Di fatto ETXEUR esce dal portafoglio il 2018-12-14.
  - **Non serve un nuovo emendamento:** è lo stesso tipo di anomalia già regolato.
- **WTIUSD.** Il 2020-04-21 segna −38%. Nel file il prezzo non va mai sotto zero: il CFD sembra già sul contratto successivo. Il 2020-03-09 segna −27%, come BCOUSD (−27%). Sono movimenti reali e restano.
- **Buchi interni.** Il buco di febbraio 2017 e quello del Capodanno cinese 2019 su HKXHKD sono gestiti dall'Emendamento 1: la posizione resta aperta e il rendimento si misura fra due close.
