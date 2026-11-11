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
