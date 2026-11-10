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
