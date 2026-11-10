# Forward test del candidato Noise Area su NQ

- **Cosa fa:** ogni giorno di borsa alle 22:40 UTC, GitHub Actions esegue `noise_area_forward.py`. Lo script scarica da Alpaca le sessioni recenti di QQQ, applica il codice **congelato** di T6 (`research/t6_engine.py`, la cui impronta è salvata nella colonna `code_version`) e aggiunge i giorni nuovi a `noise_area_nq_forward.csv`. I giorni senza trade sono registrati come `flat`.
- **Perché:** sono dati che non esistevano quando la strategia è stata costruita. Il periodo parte dal 2026-11-10.
- **Configurazione richiesta, una sola volta, dal committente:** in GitHub vai su Settings → Secrets and variables → Actions e crea i segreti `APCA_API_KEY_ID` e `APCA_API_SECRET_KEY`, con le chiavi Alpaca paper.
- **Regola:** se `t6_engine.py` cambia, cambia `code_version` e il forward test riparte da zero.
- **Unità:** il P&L è in punti NQ (QQQ × 41), al netto del costo MNQ di 0,85 punti.
