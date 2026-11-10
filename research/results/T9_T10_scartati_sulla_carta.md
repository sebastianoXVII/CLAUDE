# T9 e T10: scartati sulla carta (nessun rendimento guardato)

**Data:** 2026-11-10.

## T9 — Momentum dell'ultima mezz'ora condizionato al gamma negativo dei dealer (Baltussen et al., JFE 2021)
- **Dati:** SqueezeMetrics GEX giornaliero (`squeezemetrics.com/monitor/static/DIX.csv`, gratuito), dal 2011 al 2026-11-09. Si è guardata **solo** la frequenza della variabile di condizionamento.
- **Giorni con GEX < 0:**
  - 2017–2023: 233 su 1.760 (13%);
  - **2024–2026: 19 su 717 (3%)**, cioè 1 nel 2024, 9 nel 2025, 9 nel 2026.
- **Verdetto: non perseguibile.**
  - L'hold-out ha solo 19 eventi, quindi non può confermare nulla.
  - Nel regime attuale la strategia opererebbe circa 9 giorni l'anno, incompatibile con l'obiettivo dei payout bisettimanali su conti prop.
  - Ridefinire il gamma "basso" con soglie relative sarebbe una deviazione dalla teoria scelta a posteriori.

## T10 — Fade del FOMC (Boguth et al.; IJCB sulla press conference)
- **Eventi:** circa 8 l'anno, circa 85 nel 2016–2026. Per t > 3 servirebbe un rapporto media/deviazione standard per evento di almeno 0,33.
- **Verdetto: declassato.** Anche se reale, 8 trade l'anno non sostengono il business. Potrà essere testato in futuro come **aggiunta** a una strategia principale confermata, con una pre-registrazione dedicata.

## Lezione (filtro sulla carta, ampliato)
Oltre a "effetto atteso ≥ 3× il costo", un'ipotesi deve generare abbastanza eventi **nel regime attuale** per servire l'obiettivo, cioè trade frequenti e payout regolari.
