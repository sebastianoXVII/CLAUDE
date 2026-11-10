# Provenienza delle skill installate

Le skill sono state verificate prima dell'installazione il 2026-11-10: controllati gli script, le chiamate di rete e i comandi distruttivi.

| Skill | Fonte | Commit | Reputazione al 2026-11-10 |
|---|---|---|---|
| superpowers (15 skill) | https://github.com/obra/superpowers | 22f0b463e7a5e579904dd6211a520321035526f7 | ★315k, non archiviato, ultimo push 2026-11-03, licenza MIT |
| find-skills | https://github.com/vercel-labs/skills (skills/find-skills) | 26dc8e4755a11fea22ed788256c3db50001b013d | ★38,8k, mantenuto da Vercel Labs, ultimo push 2026-11-10 |

Esito del controllo: gli unici script sono quelli di superpowers.
- Il server di brainstorming ascolta solo su 127.0.0.1.
- `rm -rf` cancella solo le proprie directory temporanee in /tmp.
- Le uniche chiamate esterne sono letture pubbliche dell'API delle issue GitHub di obra/superpowers.

Nessuna esfiltrazione di dati o credenziali.

## Candidate valutate e scartate (find-skills, 2026-11-10)
Il registro skills.sh non è raggiungibile da questo ambiente, quindi la ricerca è stata fatta direttamente su GitHub.
- **agiprolabs/claude-trading-skills** (★520, un solo autore, ultimo push 2026-09-02). *Scartata.*
  - 68 skill, quasi tutte crypto/Solana/DeFi. Le skill con codice toccano wallet, firme e swap, e sono fuori ambito.
  - Le skill pertinenti (regime-detection, walk-forward-validation, position-sizing, slippage-modeling, market-microstructure-traditional) sono di livello retail: soglie fisse tipo "ADX > 25", nessun controllo per test multipli né significatività. Non aggiungono nulla a `research_notes/.../06_metodo_validazione.md`.
- **Altre:** finlab-ai (★426, Taiwan), xtquantai, joinquant-skill, AliceMarket, TradingAgents-AShare (mercati e piattaforme cinesi), mql-developer (★58, MetaTrader). *Scartate:* fuori dal mercato CME, poche stelle o legate a piattaforme proprietarie.
