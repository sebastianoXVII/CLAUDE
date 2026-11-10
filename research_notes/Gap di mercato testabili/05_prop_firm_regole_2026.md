# Regole dei programmi di valutazione prop firm (novembre 2026) per Nasdaq-100 intraday: futures NQ/MNQ e CFD NAS100/US100, con classifica per una strategia trend-following

**Data di recupero di tutte le fonti: 2026-11-10.**

**Profilo della strategia, come da incarico:** circa 0,9 trade al giorno, win rate 40%, vincite medie circa 2,6 volte le perdite, serie perdenti fino a 20 giorni, flat entro le 16:00 ET, nessuna posizione overnight, regole interamente codificate e potenzialmente automatizzabili.

**Metodo e accesso alle fonti (da leggere prima del resto).** Il proxy di sessione rifiuta il CONNECT (403) verso quasi tutti i domini ufficiali delle prop firm. Ho verificato con `curl` i domini seguenti:

- **Bloccati dal proxy**, da aggiungere alla allowlist per una verifica primaria:
  - FundedNext: help.fundednext.com, helpfutures.fundednext.com, fundednext.com, www.fundednext.com, support.fundednext.com
  - FTMO: ftmo.com, www.ftmo.com, academy.ftmo.com, promo.ftmo.com
  - The5ers: the5ers.com, www.the5ers.com, help.the5ers.com
  - Lucid: lucidtrading.com, support.lucidtrading.com
  - MyFundedFutures: myfundedfutures.com, help.myfundedfutures.com
  - Altre firm: help.takeprofittrader.com, help.bulenox.com, help.alpha-futures.com, fundingpips.com
  - Reputazione e archivi: www.trustpilot.com, www.reddit.com, web.archive.org, intercom.help
- **Raggiungibili ma bloccati dalla challenge anti-bot di Cloudflare** (403 "Attention Required" o "Just a moment…"). Qui l'allowlist non basta: serve un browser vero.
  - apextraderfunding.com, support.apextraderfunding.com, help.tradeify.co
- **Raggiungibile e letto per intero:** help.topstep.com (via `curl` sul proxy). Lo strumento WebFetch invece falliva anche su questo host (ENOTFOUND), perché usa una rete diversa.
- **Raggiungibile, non usato:** www.cftc.gov.

**Etichette usate nel testo:**

- **[UFF-letto]**: pagina ufficiale scaricata e letta per intero in questa sessione. Vale solo per Topstep.
- **[UFF-snippet]**: pagina ufficiale vista solo come riassunto del motore di ricerca. È il dato più probabile, ma il testo integrale non è stato letto.
- **[SEC]**: fonte secondaria (review o affiliati), spesso in conflitto con altre fonti.
- **[MEM]**: ricordo mio precedente, NON verificato in questa sessione. Va controllato prima dell'uso.

Note precedenti dello stesso progetto, scritte il 2026-11-06 interamente su fonti secondarie: `research_notes/Mappa edge futures indici intraday/05_prop_firm_costi.md`.

---

## Q1. Topstep (futures NQ/MNQ): regole correnti verificate sul help center ufficiale

### Takeaway
Topstep è l'unica firm verificata integralmente su fonte primaria.

- **Struttura:** abbonamento mensile e drawdown trailing EOD (Maximum Loss Limit) di $2.000 su 50K, con target di $3.000. Consistency al 55% in valutazione, nessun limite di perdita giornaliero obbligatorio, split 90/10, cap per richiesta da $2.000 a $6.000 e massimo 5 account XFA.
- **Bot:** consentiti tramite API ($14,50 al mese con sconto).
- **Divieto di VPS e server remoti.** **Tutto l'order flow deve partire dal dispositivo personale.** È incompatibile con la regola del committente "solo cloud" se la strategia è automatizzata.

### Cited Findings
- **Struttura del programma.** Trading Combine in abbonamento mensile, poi Express Funded Account (XFA) senza abbonamento, poi Live Funded Account su chiamata del Risk Team. Consistency target della Combine: "best trading day must stay below 55% of total profits" (pagina datata 10 set 2026) — [Topstep Program Overview](https://help.topstep.com/en/articles/8284099-topstep-program-overview) [UFF-letto]
- **Prezzi.** Combine Standard: $49 / $99 / $199 al mese per 50K / 100K / 150K, più $149 di attivazione per ogni XFA. Percorso No Activation Fee: $95 / $149 / $229 al mese. Reset agli stessi importi. Back2Funded: $599 / $699 / $829. Il percorso non si può cambiare dopo l'acquisto — [Topstep Pricing and Payment Questions](https://help.topstep.com/en/articles/14289835-topstep-pricing-and-payment-questions) [UFF-letto]
- **Rinnovo e rimborsi.** La Combine si rinnova ogni 30 giorni fino al superamento o alla cancellazione, senza limite di tempo e senza pausa. Le Combine contemporanee sono illimitate — [Trading Combine Subscriptions](https://help.topstep.com/en/articles/8284121-trading-combine-subscriptions) [UFF-letto]. Il rimborso è possibile solo entro 28 giorni e senza alcuna attività di trading — [Trading Combine Parameters](https://help.topstep.com/en/articles/8284197-trading-combine-parameters) [UFF-letto]
- **Target e posizione massima.** Target $3.000 / $6.000 / $9.000. Posizione massima 5 / 10 / 15 mini (50 / 100 / 150 micro, rapporto 10:1). Minimo 2 giorni per passare. Profili multipli vietati (Single Profile Policy). La giornata di trading va dalle 17:00 CT alle 15:10 CT — [Trading Combine Parameters](https://help.topstep.com/en/articles/8284197-trading-combine-parameters) [UFF-letto]
- **Maximum Loss Limit (MLL).** $2.000 / $3.000 / $4.500. "It rises as your end-of-day balance grows, but never moves down. Once it reaches your starting balance, it locks permanently." È monitorato in tempo reale su P&L realizzato e non realizzato: se lo tocchi intraday, scatta la liquidazione immediata. Nell'XFA il saldo parte da $0, l'MLL parte da −$2.000 e si blocca a $0. "After your first Payout: Your MLL is set to $0", quindi il saldo residuo diventa l'unico cuscinetto (pagina del 18 set 2026) — [What is the Maximum Loss Limit?](https://help.topstep.com/en/articles/8284204-what-is-the-maximum-loss-limit) [UFF-letto]
- **Daily Loss Limit (DLL).** Opzionale in Combine e XFA, automatico nel Live. Se scelto all'acquisto vale $1.000 / $2.000 / $3.000 ed è fisso. Calcolato sul Net P&L della giornata (17:00 CT – 15:10 CT). Toccarlo non è una violazione: si viene flattati fino alla sessione successiva (pagina del 30 giu 2026) — [Daily Loss Limit](https://help.topstep.com/en/articles/10490293-daily-loss-limit-in-the-trading-combine-and-express-funded-account) [UFF-letto]
- **Consistency nella Combine.** Si confronta il miglior giorno con il profitto totale. Sopra il 55% il target sale (target nuovo = miglior giorno / 0,55), ma non si viene squalificati. Esempio su 50K: miglior giorno $1.800, target $3.273. Il miglior giorno si fissa alle 15:10 CT — [Consistency at Topstep](https://help.topstep.com/en/articles/8284208-consistency-at-topstep) [UFF-letto]
- **XFA, due percorsi a scelta irrevocabile.** **Standard**: 5 giorni vincenti da almeno $150 e profitto netto positivo dall'ultimo payout. **Consistency**: almeno 3 giorni con un trade, e miglior giorno ≤40% del profitto netto della finestra. La consistency si azzera a ogni payout. Massimo 5 XFA attivi, taglie mescolabili. Back2Funded per riattivare fino a 2 volte. Scaling Plan sui contratti in base al saldo — [Express Funded Account Parameters](https://help.topstep.com/en/articles/8284215-express-funded-account-parameters) [UFF-letto]
- **Payout.** Minimo $125, split 90/10. Chi è entrato prima del 12 gen 2026 ha il 100% sui primi $10.000. Per richiesta si può prelevare fino al 50% del saldo, entro un cap:

  | Taglia | Standard | Consistency |
  |---|---|---|
  | 50K | $2.000 | $3.000 |
  | 100K | $3.000 | $4.000 |
  | 150K | $5.000 | $6.000 |

  - Offerta a tempo dal 2 giu 2026: chi aggiunge il DLL all'acquisto della Combine ottiene cap raddoppiati (50K Standard $4.000, 100K Consistency $8.000, ecc.).
  - Il giorno vincente si fissa alle 16:00 CT. Dopo ogni payout l'MLL si azzera a $0.
  - Live: nessun cap. Payout giornalieri dopo 30 giorni vincenti in Live.

  Fonte (aggiornata "this week") — [Topstep Payout Policy](https://help.topstep.com/en/articles/8284233-topstep-payout-policy) [UFF-letto]
- **Live Funded Account.** La taglia è la media degli XFA con almeno un payout, arrotondata per eccesso. Solo il 20% del capitale trasferito è subito tradabile (minimo $10K); l'80% resta in riserva e si sblocca a quote del 25% al raggiungimento del target. DLL obbligatorio. Alla chiamata in Live tutti gli XFA vengono chiusi — [Live Funded Account Parameters](https://help.topstep.com/en/articles/10657969-live-funded-account-parameters) [UFF-letto]
- **Automazione.** "Can I use automated trading strategies? Yes, with conditions." Il trade copier tra i propri account è consentito — [Trading Combine Parameters](https://help.topstep.com/en/articles/8284197-trading-combine-parameters) [UFF-letto]
- **API e VPS.** L'API costa $29 al mese ($14,50 con il codice topstep). Testualmente: "All trading activity must originate from your personal device. The use of VPS, VPNs, and remote servers is prohibited… Running automation on a VPS can result in account suspension". Un server privato può fare solo dati, backtest, log e copia dei fill, non trasmettere ordini (pagina del 17 set 2026) — [TopstepX API Access](https://help.topstep.com/en/articles/11187768-topstepx-api-access) [UFF-letto]
- **Strategie vietate.** Account stacking, ordini fuori dal best bid/offer, entrare a posizione massima dentro una notizia importante, sfruttamento dei fill simulati (centinaia di trade al giorno, durate di secondi) — [Prohibited Trading Strategies](https://help.topstep.com/en/articles/10305426-prohibited-trading-strategies-at-topstep) [UFF-letto]
- **News Tier 1 (CPI, FOMC, NFP, PPI).** Nella finestra da 5 minuti prima a 5 minuti dopo il rilascio, nessuna nuova apertura sui mini (NQ compreso). Sui micro (MNQ) le aperture sono limitate a 1 / 3 / 6 / 9 / 15 contratti per 25K / 50K / 100K / 150K / 250K. Le posizioni già aperte prima della finestra si possono gestire — [Risk Adjustments](https://help.topstep.com/en/articles/13613539-risk-adjustments-high-risk-high-volatility) [UFF-letto]
- **Orari.** Tutto va chiuso entro le 15:10 CT (16:10 ET) — [When and What Products Can I Trade](https://help.topstep.com/en/articles/8284206-when-and-what-products-can-i-trade) [UFF-letto]
- **Commissioni TopstepX round-turn.** NQ $3,78 e MNQ $1,22, così composte: borsa $2,76 / $0,70, NFA $0,02, commissione $1,00 / $0,50 (pagina del 30 set 2026) — [TopstepX Commissions and Fees](https://help.topstep.com/en/articles/8284213-topstepx-commissions-and-fees) [UFF-letto]

### Inferences
- **Il divieto di VPS è il vincolo dominante per noi.** Con una strategia automatizzata, l'esecuzione dovrebbe girare su un PC personale del committente, il che viola "mai nulla sulla macchina locale". Restano due vie compatibili:
  - **(a) esecuzione manuale** di segnali generati in cloud. Con 0,9 trade al giorno è fattibile, ma introduce errore umano e latenza;
  - **(b) scartare Topstep** per la parte automatizzata.
- **L'azzeramento dell'MLL dopo il primo payout penalizza la nostra strategia.** Ogni prelievo riduce il cuscinetto contro una serie perdente di 20 giorni. Nel Monte Carlo serve una policy di prelievo che lasci almeno circa 12-15R di saldo.
- **Il DLL è irrilevante per noi.** Con 0,9 trade al giorno e circa 1R di perdita massima per trade, un DLL di $1.000 su 50K non vincola se R ≤ $300. Conviene quindi aggiungerlo all'acquisto: raddoppia i cap di payout e dà lo sconto Responsible Trading.
- **Costo atteso del superamento.** Con l'abbonamento mensile, i 2-3 mesi stimati per passare (Q10) costano circa $100-150 più $149 di attivazione.

### Gaps
- La tabella dello Scaling Plan XFA (contratti per fascia di saldo) non è nel testo HTML: è probabilmente un'immagine.
- Il testo integrale del documento Terms of Use su VPS e automazione non è stato letto.

---

## Q2. FundedNext Futures (NQ/MNQ)

### Takeaway
L'automazione è dichiarata ammessa (EA e bot via integrazione Tradovate) in Challenge e nel funded, ma ogni EA deve avere una strategia distinta: niente trade identici tra account FundedNext.

- **Rapid Pro / Rapid Daily:** 25K / 50K / 100K a $79,99 / $149,99 / $249,99 one-time, target $1.500 / $3.000 / $5.000, MLL trailing EOD di $1.000 / $2.000 / $2.500 che si blocca al saldo iniziale +$100.
- **Flex:** consistency 40% in challenge, nessuna consistency nel funded, split 95%.
- **Limiti:** massimo 5 account attivi per household e $750K di allocazione in challenge.
- **Fonti:** tutto [UFF-snippet], perché helpfutures.fundednext.com è bloccato.

### Cited Findings
- **Account e allocazione.** Massimo 5 account FundedNext attivi contemporaneamente, a prescindere da taglia e modello, per utente e per household. Fino a 10 emessi per mese solare. Allocazione combinata in challenge fino a $750.000 alla volta — [How Many Accounts Can I Hold with FundedNext Futures](https://helpfutures.fundednext.com/en/articles/17225812-how-many-accounts-can-i-hold-with-fundednext-futures-and-what-is-the-maximum-allocation-available) [UFF-snippet]
- **Legacy dismesso.** Gli account Legacy non sono più acquistabili dall'11 ottobre — [Legacy FundedNext Account: All Rules](https://helpfutures.fundednext.com/en/articles/17229581-fundednext-futures-legacy-fundednext-account-all-rules) [UFF-snippet]
- **Rapid Pro / Rapid Daily: soglie e prezzi.**
  - Drawdown trailing EOD: si aggiorna una volta al giorno sul saldo massimo, ma il breach è istantaneo se la perdita flottante tocca l'MLL.
  - MLL $1.000 / $2.000 / $2.500. Si blocca a $25.100 / $50.100 / $100.100 (un post del blog parla invece di "never exceeds your initial balance": conflitto minore).
  - Rapid Pro non ha DLL, salvo add-on a pagamento da $500 / $1.000 / $1.250. Rapid Daily include il DLL.
  - Fee $79,99 / $149,99 / $249,99.

  Fonti — [Rapid Pro & Daily Explained](https://fundednext.com/blog/futures-rapid-pro-rapid-daily-explained); [Rapid Pro Challenge All Rules](https://helpfutures.fundednext.com/en/articles/17229677-fundednext-futures-rapid-pro-challenge-all-rules); [Rapid page](https://fundednext.com/futures/rapid) [UFF-snippet]
- **Rapid Pro / Rapid Daily: target, prelievi e cap.**
  - Target $1.500 / $3.000 / $5.000.
  - Rapid Pro: prelievi ogni 3 giorni, reward share 90%, consistency 40% come condizione di prelievo, almeno $500 di profitto nel ciclo.
  - Cap per ciclo: $600→$850 / $1.000→$1.250 / $2.000→$2.500, con aumento dal 4° prelievo. Prelievo minimo $250.
  - Rapid Daily: regola buffer invece della consistency.

  Fonti — [Rapid Pro Account: All Rules](https://helpfutures.fundednext.com/en/articles/17229713-fundednext-futures-rapid-pro-fundednext-account-all-rules); [Rapid Daily Account All Rules](https://helpfutures.fundednext.com/en/articles/17229779-fundednext-futures-rapid-daily-fundednext-account-all-rules) [UFF-snippet]
- **Flex.**
  - Taglie 50K / 100K / 150K, target $2.500 / $5.000 / $8.000, drawdown trailing EOD.
  - Consistency 40% in challenge: superarla alza il target a miglior giorno / 0,40, non squalifica.
  - Funded senza consistency. Payout dopo 5 benchmark day e $500 nel ciclo, share 95%.
  - Limiti di contratti 3 / 5 / 8 mini.
  - Prezzo in conflitto tra pagine ufficiali: $74,99-$141,99 per il 50K, probabilmente per effetto di promo.

  Fonti — [Flex page](https://fundednext.com/futures/flex); [Flex Explained](https://fundednext.com/blog/fundednext-futures-flex-explained); [Consistency rule](https://helpfutures.fundednext.com/en/articles/17230245-is-there-any-consistency-rule-to-be-followed-in-the-fundednext-futures-challenge-fundednext-account); [Contract Limits](https://helpfutures.fundednext.com/en/articles/17230194-contract-limits-and-contract-types-at-fundednext-futures) [UFF-snippet]
- **Direct (senza valutazione) e FNL:003 Instant.**
  - Direct: 50K, MLL $2.000, DLL $1.000.
  - Entrambi applicano una consistency "perpetua" del 20%: il miglior giorno ≤20% del profitto del ciclo, e il record si trascina tra i cicli.

  Fonti — [Futures Direct](https://fundednext.com/futures/direct); [FNL:003 50K Instant](https://help.fundednext.com/en/articles/16847874-what-is-the-fundednext-futures-fnl-003-50k-instant-account) [UFF-snippet]
- **Automazione.**
  - EA e bot ammessi in Challenge e funded, attraverso un'integrazione di piattaforma che si collega a Tradovate.
  - Vietati: EA che passano da Telegram o WhatsApp, latency abuse e order flooding, HFT, tick scalping, grid, hedging tra account o di gruppo.
  - Ogni EA deve avere una strategia distinta, quindi niente trade identici tra account FundedNext.
  - Non si può passare da EA a manuale tra challenge e funded.

  Fonti — [FundedNext Futures FAQ](https://helpfutures.fundednext.com/en/articles/17225788-fundednext-futures-most-frequently-asked-questions); [Futures General Rules](https://fundednext.com/general-rules/futures/what-is-allowed) [UFF-snippet]. Conflitto: un articolo generico MT4/MT5 dice che sopra i $50K si tradano solo a mano — [Is EA allowed](https://help.fundednext.com/en/articles/8020763-is-ea-allowed-in-fundednext) [UFF-snippet]. Si riferisce probabilmente ai CFD.
- **Conflitto sui target.** Una pagina dei Futures Challenge Terms di circa 46 giorni fa riporta target diversi, per esempio $1.250 sul 25K — [Futures Challenge Terms](https://fundednext.com/futures-challenge-terms) [UFF-snippet]

### Inferences
- Il divieto di trade identici tra account FundedNext significa che non si possono copiare 5 account con lo stesso EA. Di fatto la scala è 1 account per strategia, salvo un chiarimento scritto del supporto.
- Rapid Pro 50K, con un one-time di $149,99, target 1,5:1 sul drawdown, nessun DLL e prelievi ogni 3 giorni, è parametricamente vicino a Topstep 50K e senza il problema VPS, se Tradovate più una piattaforma cloud è ammessa. Il cap per ciclo di $1.000 non vincola una strategia che rende circa $50-60 al giorno su 50K (vedi Q10).
- La consistency 40% come condizione di prelievo in Rapid Pro, applicata a cicli brevi (3 giorni), mal si concilia con una strategia a code grasse: una vincita da 2,6R in un ciclo con poco profitto netto blocca il prelievo. Flex, senza consistency nel funded, è più adatto.

### Gaps
- Non ho trovato una dichiarazione esplicita sul permesso di usare VPS o cloud.
- Prezzo corrente Flex, importo del drawdown Flex, testo integrale delle regole Rapid.
- Le regole sulle news dei futures FundedNext non sono state trovate.

---

## Q3. FundedNext CFD (Stellar 2-Step, 1-Step, Lite, Instant) e disponibilità del NAS100

### Takeaway
Il Nasdaq-100 è tradabile come **NDX100**.

- **Max loss statico** nei programmi a valutazione, misurato dal saldo iniziale: 2-Step 10%, 1-Step 6%, Lite 8%. È il tratto più favorevole per una strategia con serie perdenti lunghe.
- **Daily loss** calcolata includendo il flottante, reset alle 00:00 server.
- **News nel funded:** i trade entro 5 minuti da una notizia ad alto impatto contano al 40% dei profitti.
- **Commissioni sugli indici:** probabilmente $0, solo spread, ma il dato è [SEC].
- **Leva sugli indici nel funded:** ridotta "temporaneamente" a 1:5 [SEC].
- **EA:** policy in conflitto tra le pagine ufficiali.

### Cited Findings
- **Indici disponibili.** SPX500, NDX100, GER30, US30. Gli spread live sono nella pagina Symbols — [FundedNext CFDs Symbols & Conditions](https://fundednext.com/general-rules/cfds/symbols-and-conditions); [Tradable Assets](https://help.fundednext.com/en/articles/8224087-fundednext-tradable-assets-what-can-i-trade-on-fundednext-cfd-accounts) [UFF-snippet]
- **Commissioni Stellar 1-Step e 2-Step.** $5 su forex e oil, 0,0016% sui metalli, 0,04% sulle crypto, 0,004% sulle azioni. Gli indici non compaiono nell'elenco. Struttura in vigore dal 01/12/2026, secondo un articolo — [Symbols & Conditions](https://fundednext.com/general-rules/cfds/symbols-and-conditions); [Commission charges](https://help.fundednext.com/en/articles/10701368-what-are-the-commission-charges-for-stellar-challenges-and-fundednext-accounts) [UFF-snippet]
- **Costo NDX100 [SEC].** Indici a $0 di commissione. Spread NDX circa 1,96 (unità non indicata) in una rilevazione, "40" in un'altra review: dati incoerenti — [proptradingvibes spreads](https://proptradingvibes.com/blog/fundednext-spreads-and-commissions); [fxverify spreads](https://fxverify.com/tools/prop-firm-spreads/fundednext-3405)
- **Stellar 2-Step.** Target 8% (fase 1) e 5% (fase 2). Daily loss 5% e max loss 10%, entrambi sul saldo iniziale. 5 giorni minimi per fase. Il blocco della seconda fonte dice invece che EA e indicatori sono ammessi — [Stellar 2-Step Challenge](https://help.fundednext.com/en/articles/17255124-stellar-2-step-challenge); [Stellar 2-Step page](https://fundednext.com/cfds/stellar-2-step) [UFF-snippet]
- **Stellar 1-Step.** Target 10%, daily loss 3%, max loss 6% statico (pavimento al 94% del saldo iniziale), 2 giorni minimi. Un articolo dice "EA e indicatori di terzi non ammessi" — [Stellar 1-Step Account](https://help.fundednext.com/en/articles/17252927-stellar-1-step-account); [1-Step rules](https://help.fundednext.com/en/articles/12673301-what-rules-do-i-need-to-follow-in-the-stellar-1-step-challenge-at-fundednext-cfd) [UFF-snippet]
- **Calcolo della daily loss.** Include il P&L flottante, swap, commissioni e fee. Reset alle 00:00 server time — [CFDs Trading Objectives](https://fundednext.com/general-rules/cfds/trading-objectives) [UFF-snippet]
- **Stellar Lite.**
  - Target 8% / 4%, daily loss 4%, max loss 8%.
  - EA add-on non disponibile da $50K in su. Conflitto con una pagina più vecchia, relativa a Match-Trader, che vieta gli EA.
  - Giorni minimi 2 o 5 a seconda della pagina.
  - News nel funded: profitti contati al 40% entro 5 minuti dalla notizia. In fase di challenge non si applica.

  Fonti — [Stellar Lite Account](https://help.fundednext.com/en/articles/17253939-stellar-lite-account); [Stellar Lite page](https://fundednext.com/cfds/stellar-lite); [News in Stellar Lite](https://help.fundednext.com/en/articles/10701615-is-news-trading-allowed-in-the-stellar-litechallenge-and-fundednext-account) [UFF-snippet]
- **Lite: prezzo, share e allocazione.** 100K a $399,99. Fee rimborsata al 3° reward. Reward share 80% in tabella, "fino al 95%" in marketing. Primo prelievo dopo 10 giorni lavorativi — [Stellar Lite page](https://fundednext.com/cfds/stellar-lite) [UFF-snippet]. Cap di allocazione Lite $200.000 — [propfirmbridge](https://propfirmbridge.com/education/fundednext-stellar-1-step-vs-2-step-vs-lite-vs-instant) [SEC]
- **Stellar Instant.**
  - Nessuna daily loss. Max loss trailing del 6% dal saldo massimo, che si ferma al saldo iniziale.
  - Rischio massimo 3% alla volta. Allocazione attiva totale massima $20.000.
  - EA tramite add-on, per al massimo $300.000 per singola strategia EA. Vietato copiare setup identici tra account.

  Fonti — [Stellar Instant Account](https://help.fundednext.com/en/articles/17253243-stellar-instant-account); [EA in Stellar Instant](https://help.fundednext.com/en/articles/11641338-can-i-use-ea-in-stellar-instant) [UFF-snippet]
- **Prezzi 100K [SEC].** 2-Step $549,99 (una guida dice $529,99), 1-Step $549,99-$569,99. Rimborso della fee: al 1° reward oppure al 3°, secondo la fonte — [proptradingvibes pricing](https://proptradingvibes.com/blog/fundednext-pricing); [propfirmdeals](https://propfirmdeals.org/fundednext-rules.html)
- **Split.** 80-95% a seconda del modello — [What is FundedNext](https://fundednext.com/blog/what-is-fundednext) [UFF-snippet]
- **Leva sugli indici nel funded.** Ridotta da 1:30 a 1:5 "temporaneamente" su 1-Step, 2-Step e Lite (aprile 2026). NAS100 resta tradabile a size minore. Su Lite niente posizioni nel weekend — [ptv-dev blog](https://ptv-dev.pages.dev/blog/fundednext-best-instruments) [SEC]; [ctrader.com](https://ctrader.com/id/prop-firms/fundednext) [SEC]
- **Tetto di allocazione CFD complessivo.** Circa $300.000 per trader [MEM]: non l'ho trovato in nessuna fonte di questa sessione.

### Inferences
- **2-Step 100K, stima del sizing.** Con il max loss statico al 10%, R ≈ 0,6-0,7% (circa 15R di cuscinetto) dà un cuscinetto di $10.000 contro i $2.000-3.000 dei futures 50K/100K. Stima di tempo: fase 1 circa 38 giorni, fase 2 circa 19 (vedi Q10).
- **Effetto della leva 1:5.** Su 100K il nozionale massimo è $500K. Con R = $666 e uno stop di circa 50 punti NAS100 servono circa 13 lotti da $1/punto, cioè circa $330K di nozionale a 25.000 punti. Sta sotto 1:5, ma senza margine per stop stretti.
- **Regola news al 40%.** Va evitata con un filtro calendario di ±5 minuti sulle notizie USD ad alto impatto. Per un trend-follower intraday il costo atteso è piccolo, ma va codificato.
- **Instant non è adatto.** Il trailing al 6% e il tetto di $20K lo rendono inutile per noi.

### Gaps
- Spread NDX100 reale in punti e in fasce orarie. Serve la pagina Symbols (bloccata) o una piattaforma demo.
- Policy EA definitiva per 1-Step e 2-Step.
- VPS consentito o no.
- Tetto di allocazione complessivo CFD.
- Frequenza dei payout per 2-Step e 1-Step.

---

## Q4. FTMO: programma CFD (2-Step, 1-Step) e FTMO Futures (Growth e Pro)

### Takeaway
**FTMO CFD 2-Step:**

- target 10% / 5%;
- daily loss 5% e max loss 10% statico, sul saldo iniziale;
- nessuna consistency;
- giorni minimi 4;
- tetto di $400.000 di capitale per trader e per strategia, ampliabile con scaling e Premium.

**FTMO CFD 1-Step:** target 10%, daily loss 3%, max loss 10% trailing EOD, nuova Consistency 50% dal 12 ott 2026 (oppure dal 5 ott, secondo un'altra pagina).

**FTMO Futures:**

- trailing EOD che si blocca al capitale iniziale;
- il **Pro** ha un rapporto target/drawdown 1:1 sul 50K ($3.000 / $3.000), DLL rigido di $1.000, consistency 40% solo in valutazione, prelievo del 100% del profitto;
- automazione ammessa [SEC].

Molti dettagli sono [UFF-snippet] o [SEC] perché ftmo.com è bloccato.

### Cited Findings
- **Daily e max loss CFD.** Max daily loss 5% sul 2-Step e 3% sul 1-Step, sul saldo iniziale. Reset a mezzanotte CE(S)T. Conta il chiuso più il flottante — [Maximum Daily Loss](https://academy.ftmo.com/lesson/maximum-daily-loss/); [Trading Objectives](https://ftmo.com/en/trading-objectives/) [UFF-snippet]
- **Max loss CFD.** 10% su entrambi. Sul 1-Step è "End-of-Day Trailing", sul 2-Step è ancorato al saldo iniziale (90%) in entrambe le fasi e nell'FTMO Account — [1-Step page](https://ftmo.com/en/1-step-challenge/); [Drawdowns blog](https://ftmo.com/en/blog/drawdowns/); [ML rule 1-Step FAQ](https://ftmo.com/au/faq/what-is-the-max-loss-ml-rule-in-ftmo-challenge-1-step/) [UFF-snippet]
- **Target CFD.** 2-Step: 10% in fase 1 e 5% in Verification, minimo 4 giorni di trading. 1-Step: target unico 10%, split 90% dal primo reward — [2-Step page](https://ftmo.com/en/2-step-challenge/); [Introducing 1-Step](https://ftmo.com/en/blog/introducing-the-1-step-ftmo-challenge/) [UFF-snippet]
- **Consistency 1-Step.** Dal 12 ott 2026 alle 9:00 la Consistency sostituisce la Best Day Rule sui nuovi ordini 1-Step (il blog dice dal 5 ott). Il miglior giorno ≤50% del profitto totale, che ora include i giorni in perdita. Superarla non è una violazione: si continua a tradare. Il 2-Step non ha consistency — [Trading Update 8 Oct 2026](https://ftmo.com/en/blog/trading-updates/trading-update-8-oct-2026/); [Consistency FAQ](https://ftmo.com/en/faq/how-does-your-consistency-rule-work/) [UFF-snippet]
- **News sul 1-Step.** Secondo la pagina promozionale "you may trade freely during all macroeconomic news releases" — [promo 1-Step](https://promo.ftmo.com/new-1-step-challenge/) [UFF-snippet]
- **Tetto di capitale.**
  - "The total capital allocation across all accounts and products is limited to $400,000 per trader or strategy (prior to any scaling)". Trading identico o simile tra account oltre il limite può portare alla sospensione.
  - Con il setup Aggressive il tetto è $200.000.
  - Scaling fino a $2.000.000. Premium Programme con livelli da $600K e $1M.
  - Un solo Instant Account per volta.

  Fonti — [How many accounts can I have?](https://ftmo.com/en/faq/how-many-accounts-can-i-have/); [Premium Programme](https://ftmo.com/en/premium-programme/) [UFF-snippet]
- **US100 CFD, costi [SEC].** Commissione sugli indici $0, solo spread. Spread US100 circa 1,66 (unità non indicata) in una rilevazione su conto raw; un post di forum del 2022 dice "at least 2 points" — [propspread FTMO](https://www.propspread.com/providers/ftmo); [Forex Factory thread](https://www.forexfactory.com/thread/707034-ftmo-for-serious-traders?page=445)
- **Commissioni e costi in generale.** Commissioni, spread e swap sono pubblicati sulle piattaforme. Per indici come DXY.cash un vecchio update indica lo 0,001% del nozionale round-trip — [Trading Update 16 Jan 2025](https://ftmo.com/en/blog/trading-updates/trading-update-16-jan-2025/) [UFF-snippet]
- **FTMO Futures, drawdown.** Growth e Pro usano un trailing EOD sull'equity che si blocca al capitale iniziale. Dal 5 nov 2026, sulle nuove valutazioni, il drawdown di Growth 100K passa da $3.500 a $3.000 e quello di Growth 150K da $5.000 a $4.500 — [Futures Trading Update 5 Nov 2026](https://ftmo.com/en/futures/blog/trading-updates/futures-trading-update-5-nov-2026/); [Futures Trading Objectives & Rules](https://ftmo.com/en/futures/trading-objectives-and-rules/) [UFF-snippet]
- **FTMO Futures Pro.**
  - 100K: target $6.000, drawdown $3.000, DLL $2.000. 50K: target $3.000, DLL rigido $1.000 (breach = chiusura).
  - Consistency 40% solo in valutazione. Nessun trailing intraday, nessuna fee di attivazione.
  - Prelievo fino al 100% del profitto, 90/10, cap per richiesta $5.000-8.000. 5 giorni qualificanti.
  - Growth: 4 giorni qualificanti, DLL "soft" nel funded e assente in valutazione.

  Fonti — [Comparison Table](https://ftmo.com/en/futures/comparison-table/); [Growth vs Pro](https://ftmo.com/en/futures/faq/how-do-the-growth-and-pro-products-differ/) [UFF-snippet]
- **FTMO Futures, dettagli secondari [SEC].**
  - Growth 50K: target $3.000, drawdown EOD $2.000, nessun DLL in valutazione, DLL soft di $1.000 nel funded, "$119/mo" senza fee di attivazione (non è chiaro se sia un abbonamento).
  - Prelievo del 50% del profitto, cap di $2.500 sul 50K, giorno qualificante da $150 o più.
  - Pro 50K: drawdown $3.000 (rapporto 1:1), giorno qualificante da $200 o più.
  - Nessun overnight.

  Fonti — [tradetanto](https://tradetanto.com/learn/ftmo-futures-rules); [fundedtrading](https://fundedtrading.com/propfirm/ftmo-futures/); [propfirmreviews](https://propfirmreviews.net/reviews/ftmo-futures/)
- **FTMO Futures, copy e automazione.** La pagina ufficiale vieta di incorporare decisioni di terzi: segnali, master account, copier di terzi — [Forbidden Trading Practices (futures)](https://ftmo.com/en/futures/forbidden-trading-practices/) [UFF-snippet]. Secondo fonti secondarie la stessa pagina dichiara "automated trading is permitted" e la copia tra i propri account FTMO Futures è ammessa — [prop-memo](https://prop-memo.com/en/articles/ftmo-futures-guide-2026-09); [tanjatrades](https://tanjatrades.com/articles/ftmo-futures/) [SEC]
- **Ricordi [MEM], da verificare.**
  - FTMO CFD consente EA e VPS.
  - Split 80%, che sale al 90% con lo scaling, sul 2-Step.
  - Payout su richiesta dopo 14 giorni, poi ogni 14 giorni.
  - Fee 2-Step 100K circa €540, rimborsata con il primo reward.
  - Sull'FTMO Account standard (2-Step funded) vale il divieto di aprire o chiudere nei 2 minuti prima e dopo le news ad alto impatto sullo strumento interessato. L'account "Swing" lo toglie in cambio di leva 1:30.

### Inferences
- **FTMO CFD 2-Step è la combinazione più adatta al nostro profilo:**
  - drawdown statico ampio (10%);
  - DLL al 5%, non vincolante con 0,9 trade al giorno;
  - nessuna consistency;
  - EA ammessi [MEM];
  - tetto di $400K, che consente per esempio 2 conti da $200K o 4 da $100K, con lo stesso EA, entro il tetto.
- **FTMO Futures Pro 50K** offre il miglior rapporto target/drawdown tra i futures (1:1, contro 1,5:1 di Topstep, Apex, Tradeify e Lucid). Riduce il tempo atteso di superamento di circa il 33%.
- **Regola news da ±2 minuti dell'FTMO Account [MEM]:** è facile da codificare per una strategia intraday, a patto di non tenere posizioni aperte attraverso CPI, NFP o FOMC. Va verificato se vale anche per chiudere una posizione: in quel caso uno stop dentro la finestra sarebbe un problema.

### Gaps
- Testo integrale di: Trading Objectives, regole news dell'FTMO Account, policy EA e VPS, prezzi correnti, frequenza dei payout. Tutto su ftmo.com, bloccato.
- Prezzi e piattaforma (Tradovate o Rithmic) di FTMO Futures.
- Spread US100 in punti.

---

## Q5. Apex Trader Funding (4.0, dal 1 mar 2026)

### Takeaway
**Apex va escluso per una strategia automatizzata.** La pagina ufficiale Prohibited Activities dice che "the use of automation is strictly prohibited on all account types", AI e bot inclusi.

Il resto è secondario:

- **Valutazione EOD 50K:** target $3.000, drawdown EOD $2.000, DLL $1.000.
- **Performance Account (PA):** 5 giorni qualificanti da $250 o più, consistency 50%, saldo minimo $52.600 per il primo payout, massimo 6 payout per PA su scala crescente, fino a 20 PA per household.
- **Contenzioso:** causa federale *Lawton v. Apex* del luglio 2026 [SEC].

### Cited Findings
- **Automazione.** "At Apex Trader Funding, the use of automation is strictly prohibited on all account types. This includes any form of AI…, Autobots, algorithms, fully automated trading systems, and high-frequency trading". La violazione comporta chiusura e perdita dei fondi. Le ATM strategy (bracket automatici di stop e target) sono invece incoraggiate — [Prohibited Activities](https://apextraderfunding.com/help-center/getting-started/prohibited-activities/); [Legacy PA Compliance](https://apextraderfunding.com/help-center/performance-accounts-pa/legacy-performance-account-pa-compliance/); [User Agreement](https://dashboard.apextraderfunding.com/legal/user-agreement) [UFF-snippet]. Alcune fonti secondarie dicono che il semi-automatico è ammesso e che la valutazione era tollerante — [quantvps](https://www.quantvps.com/blog/apex-trader-funding-automated-trading-bots) [SEC]
- **Valutazione intraday.** Il threshold segue il picco di saldo, inclusi gli utili non realizzati. Nessun DLL nella valutazione intraday; la versione EOD ha un DLL che sospende la sessione senza squalificare. Nessuna consistency in valutazione — [Intraday Trailing Drawdown Evaluations](https://support.apextraderfunding.com/hc/en-us/articles/45683414022299-Intraday-Trailing-Drawdown-Evaluations); [EOD Evaluations](https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-evaluations/); [Daily Loss Limit Explained](https://apextraderfunding.com/help-center/additional-helpful-items/daily-loss-limit-explained/) [UFF-snippet]
- **Consistency nel PA.** Nessun giorno profittevole può valere il 50% o più del profitto dall'ultimo payout — [PA and Compliance](https://support.apextraderfunding.com/hc/en-us/articles/31519788944411-Performance-Account-PA-and-Compliance) [UFF-snippet]
- **Payout Legacy.** Cap per taglia (50K: $2.000 per payout). Dal 6° payout il 100% senza cap. Nel Live nessun cap — [Legacy PA Payout Parameters](https://support.apextraderfunding.com/hc/en-us/articles/40507212951451-Legacy-PA-Payout-Parameters); [Apex Live FAQ](https://apextraderfunding.com/help-center/getting-started/apex-live-prop-trading-program-faq/) [UFF-snippet]
- **4.0, valutazione EOD 50K [SEC].** Target $3.000, drawdown $2.000, DLL $1.000. Fee one-time di importo non trovato. Nessun minimo di giorni — [tradetanto](https://tradetanto.com/learn/apex-trader-funding-rules-what-you-need-to-know); [copilink](https://copilink.com/prop-firms/apex-trader-funding)
- **4.0, PA [SEC].** 5 giorni da $250 o più (EOD 50K; $200 nella versione intraday). Consistency 50%. Saldo minimo $52.600 e primo payout minimo $500. Massimo 6 payout per PA. Cap 50K EOD da $1.500 a $3.000 (oppure "$13.000 totali", secondo la fonte). Split 100% oppure 100% dei primi $25K e poi 90/10: conflitto tra fonti. 20 PA per household. Hedging vietato — stesse fonti, più le note del 2026-11-06
- **Contenzioso [SEC].** *Lawton v. Apex Trader Funding Inc.*, W.D. Texas, depositata il 24 lug 2026: contesta il marketing "No Payout Denials" e "Simple Rules". Sono allegazioni, non accertamenti. *Riot v. Apex* (copyright) sospesa il 20 gen 2026. Trustpilot da 4,4 a 4,3 tra aprile e maggio 2026 — [propfirmbriefing](https://propfirmbriefing.com/apex-trader-funding-lawsuit/); [courtdocket](https://courtdocket.org/apex-trader-funding-lawsuit-counterclaims-contempt-and-sanctions/); [imantrading](https://www.imantrading.org/firmfaq/apex-trader-funding-problems)

### Inferences
- Il divieto ufficiale di automazione, il limite di 6 payout per PA e il contenzioso in corso escludono Apex come programma principale. Resta solo un'eventuale esecuzione manuale dei segnali, ma 20 PA a mano non sono gestibili con disciplina.

### Gaps
- Prezzi 4.0 e tabella ufficiale dei cap 4.0.
- Testo integrale della pagina Prohibited Activities: Cloudflare impedisce la lettura con `curl`.

---

## Q6. Tradeify (Select, Growth, Lightning)

### Takeaway
- **Drawdown:** tutti i piani usano un trailing EOD ($2.000 sul 50K), applicato in tempo reale, che si blocca al saldo iniziale +$100.
- **Select:** consistency 40% in valutazione (minimo 3 giorni, nessun DLL), poi nel funded Select Flex senza DLL né consistency e con 5 giorni vincenti.
- **Bot:** ammessi se il trader ne è l'unico proprietario, non HFT, e **non usati su più firm**.
- **Commissioni:** NQ $5,76 e MNQ $1,82 round-turn (ufficiale, da note precedenti).

### Cited Findings
- **Drawdown.** Tutti e tre i piani hanno un trailing EOD che sale alla chiusura della sessione ma si applica in tempo reale. Si blocca come minimo statico quando il saldo EOD supera il capitale iniziale più il drawdown più $100 — [Essential Trading Rules Overview](https://help.tradeify.co/en/articles/12268167-essential-trading-rules-overview); [EOD Trailing explained](https://tradeify.co/post/trailing-drawdown-explained-for-prop-firm-traders) [UFF-snippet]
- **Select.** Consistency 40% in valutazione, rimossa dopo il superamento. Nessun DLL in valutazione. Funded Select Flex: nessun DLL, 5 giorni vincenti per ciclo. Select Daily: DLL di $1.000 / $1.250 / $1.750 (50K / 100K / 150K) e payout giornalieri — [Select Evaluation Accounts](https://help.tradeify.co/en/articles/12853921-select-evaluation-accounts); [SELECT vs Growth](https://help.tradeify.co/en/articles/13252431-select-vs-growth-choosing-your-evaluation-type) [UFF-snippet]
- **Growth.** Nessuna consistency in valutazione. Consistency 35% sulle richieste di payout nel funded. 5 giorni profittevoli per ciclo. DLL soft che ferma il trading fino alle 18:00 ET — [GROWTH Evaluation Accounts](https://help.tradeify.co/en/articles/10495915-growth-evaluation-accounts); [Rules: Daily Loss Limit](https://help.tradeify.co/en/articles/10468321-rules-daily-loss-limit) [UFF-snippet]
- **Lightning (instant).** Consistency 20% al 1° payout, 25% al 2°, 30% dal 3°, per gli account acquistati dopo il 12 set 2025. Payout ogni 5 giorni — [Essential Trading Rules Overview](https://help.tradeify.co/en/articles/12268167-essential-trading-rules-overview) [UFF-snippet]
- **Attività minima.** Almeno 1 trade a settimana su tutti i piani — stessa fonte [UFF-snippet]
- **Bot.** "At Tradeify, we allow the use of bots and algorithms under certain conditions". Condizioni: unico proprietario, nessun altro ne ha accesso, niente uso su più firm, niente HFT, documentazione su richiesta. Copier di terzi "at your own risk" — [Guidelines for Traders](https://help.tradeify.co/en/articles/10468318-guidelines-for-traders); [Risk & Compliance FAQ](https://help.tradeify.co/en/articles/17069653-risk-compliance-guidelines-faq) [UFF-snippet]
- **Prezzi 50K di listino, ottobre 2026 [SEC].** Growth $145, Select $165, Lightning $492, one-time. Gli account funded falliti non sono resettabili — [shattered.io](https://shattered.io/tradeify-promo-code/); [Tradeify Pricing Reference](https://help.tradeify.co/en/articles/14369021-tradeify-pricing-reference) (ufficiale, contenuto non visto)
- **Account funded.** Massimo 5 su tutti i piani, per persona o household [SEC] — note del 2026-11-06 ([tradedupe](https://tradedupe.com/compare/tradeify-vs-lucid-trading))
- **Commissioni RT.** NQ $5,76, MNQ $1,82 — [Tradeify help](https://help.tradeify.co/en/articles/10468315-trading-commission-fees) [UFF-snippet, note del 2026-11-06]
- **Statistiche.** Pass rate delle valutazioni avviate tra ago 2025 e lug 2026: 17,2% — [Tradeify blog](https://tradeify.co/post/futures-prop-firm-statistics-2026) [UFF-snippet, note precedenti]

### Inferences
- **Select Flex è strutturalmente molto adatto:** consistency 40% solo per passare, poi nessun DLL e nessuna consistency.
- **Il divieto di usare lo stesso bot su più firm** è incompatibile con il piano "stesso EA su FTMO, FundedNext e Tradeify". Se si sceglie Tradeify, la strategia deve girare lì in esclusiva, almeno formalmente, oppure serve un chiarimento scritto.
- **Costi.** Le commissioni NQ più alte di Topstep ($5,76 contro $3,78) pesano poco con 0,9 trade al giorno.

### Gaps
- Policy sul VPS.
- Cap di payout Select Flex.
- Prezzi ufficiali.
- Tetto di account confermato sul help center.

---

## Q7. Lucid Trading (LucidFlex, LucidPro, LucidDirect)

### Takeaway
- **LucidFlex:** fee one-time (50K circa $115-130 [SEC]), target $1.250 / $3.000 / $6.000 / $9.000, MLL trailing EOD di $1.000 / $2.000 / $3.000 su 25K / 50K / 100K.
- **Consistency in valutazione:** 40% o 50%, scelta all'acquisto.
- **Funded Flex:** **nessuna consistency**, DLL opzionale, payout dopo 5 giorni da $100 / $150 / $200, fino al 50% del profitto con cap $1.000 / $2.000 / $2.500 / $3.000, 90/10.
- **Automazione:** ammessa [SEC].
- **Account:** 5 funded e 10 totali per household [SEC].

### Cited Findings
- **LucidFlex funded.** DLL opzionale, nessuna consistency, nessun buffer di payout. In valutazione la consistency è scelta al 40% o al 50% all'acquisto — [LucidFlex Funded Account](https://support.lucidtrading.com/en/articles/12945795-lucidflex-funded-account); [LucidFlex Customization](https://support.lucidtrading.com/en/articles/16226050-lucidflex-customization) [UFF-snippet]
- **LucidPro.** 90/10. Payout subordinato a profit goal, consistency 40% (35% per gli account acquistati prima del 28/11/2025) e buffer sopra l'MLL — [LucidPro Payouts](https://support.lucidtrading.com/en/articles/12890092-lucidpro-payouts); [LucidPro Consistency](https://support.lucidtrading.com/en/articles/12890109-lucidpro-consistency-percentage) [UFF-snippet]
- **LucidDirect (instant).** Consistency 20%. Nell'accordo di maggio 2025: minimo 10 giorni di trading, MLL che si blocca al saldo iniziale +$100 — [LucidDirect Consistency](https://support.lucidtrading.com/en/articles/12890178-luciddirect-consistency-percentage); [LucidDirect Agreement PDF](https://lucidtrading.com/wp-content/uploads/2025/05/LucidDirect-Account-Agreement-5-19.pdf) [UFF-snippet]
- **Live.** Nuova struttura Live; le regole di consistency non si applicano più in Live — [New Live Structure](https://support.lucidtrading.com/en/articles/16558826-new-live-structure) [UFF-snippet]
- **LucidFlex, numeri [SEC].** Target, MLL, giorni qualificanti e cap come nel Takeaway; il cap non cresce tra le richieste. Prezzi 25K / 50K / 100K: $100 / $130 / $225 di listino (un'altra fonte dice 50K a $115) — [bestprops](https://bestprops.com/lucidflex-rules-payouts/); [phidias](https://phidiaspropfirm.com/education/lucidflex-payout-rules); [copilink](https://copilink.com/prop-firms/lucid-trading)
- **Automazione e account [SEC].** Sistemi automatici e copier ammessi, con responsabilità sugli errori software a carico del trader. Vietati HFT, microscalping e hedging tra account. LucidDirect potrebbe richiedere l'approvazione scritta del software. Household: 10 account totali, al massimo 5 funded — [pickmytrade Lucid FAQ](https://pickmytrade.trade/prop-firm-faq/lucid-trading-faq/); [phidias copy trading](https://phidiaspropfirm.com/education/lucid-trading-copy-trading); [bestprops rules](https://bestprops.com/rules/lucid-trading-rules/)
- **Commissioni RT [SEC].** NQ circa $3,50, MNQ circa $1,00 — note del 2026-11-06

### Inferences
- LucidFlex 50K è parametricamente simile a Tradeify Select: one-time, valutazione con 40-50% di consistency, funded libero. Il cap di $2.000 per richiesta non vincola una strategia che produce circa $1.100 al mese su 50K.
- Lucid va verificato su VPS e automazione prima dell'uso: oggi non c'è fonte primaria.

### Gaps
- Testo ufficiale sull'automazione ("Other Trading Activities") e sul numero massimo di account.
- Prezzi correnti ufficiali.
- Regole sulle news.

---

## Q8. The5ers e altre firm rilevanti nel 2026 (MFFU, Bulenox, Alpha Futures, Take Profit Trader)

### Takeaway
**The5ers (CFD):**

- High Stakes 2-Step: max loss 10%, daily loss 5% (breach = chiusura), blocco degli ordini nei 2 minuti prima e dopo le news ad alto impatto, payout ogni 14 giorni, split dall'80% fino al 100%, scaling fino a $500K;
- Hyper Growth 1-Step: target 10%, stop-out 6%, pausa giornaliera al 3%;
- EA ammessi ma con conflitti tra fonti (una richiede l'approvazione scritta);
- NAS100 tradabile, commissione probabilmente $0 [SEC].

**MFFU:** regole in forte conflitto tra fonti.

Nessuna di queste firm è verificata su fonte primaria.

### Cited Findings
- **High Stakes.** 2-Step senza limite di tempo. Nessun ordine eseguito nei 2 minuti prima e dopo le news ad alto impatto (esempio: CPI alle 15:30 server, blocco 15:28-15:32). Perdita totale 10%. Una perdita giornaliera del 5% chiude l'account. FAQ aggiornata il 3 nov 2026 — [General rules High Stakes](https://the5ers.com/faqs/what-are-the-general-rules-for-the-high-stakes-program/); [Can I trade during news](https://the5ers.com/faqs/can-i-trade-during-news/); [High Stakes](https://the5ers.com/high-stakes/) [UFF-snippet]
- **Hyper Growth e Bootcamp.** Hyper Growth: 1-Step, target 10%, stop-out 6%, pausa giornaliera al 3% (una pagina in giapponese dice "nessuno stop giornaliero"). Bootcamp: 3 step, target 6% e max loss 5% per step. EA ammessi, ma vietati latency arbitrage, tick scalping e rollover scalping. Copia di segnali esterni vietata — [Challenge Programs explained](https://the5ers.com/challenge-programs-bootcamp-high-stakes-hyper-growth-explained/) [UFF-snippet]
- **Numero di account.** Pagine ufficiali esistenti ma contenuto non ottenuto — [How many The5ers accounts](https://help.the5ers.com/how-many-the5ers-accounts-can-i-have/); [How many High Stakes accounts](https://help.the5ers.com/how-many-high-stakes-accounts-can-i-have/) [UFF-snippet, contenuto non ottenuto]
- **Payout e scaling High Stakes [SEC].**
  - Payout ogni 14 giorni, minimo $150. Sul 100K, minimo $500 di P&L e cap $4.000.
  - Split dall'80%, poi 85%, 90% e 100% con lo scaling. Scaling fino a $500K ($4M solo per Hyper Growth).
  - EA: "Yes" secondo una fonte, "approvazione scritta" secondo un'altra.

  Fonti — [quantvps](https://www.quantvps.com/blog/the5ers-payout-rules); [myfxbook](https://www.myfxbook.com/prop-firms/the5ers); [pipster](https://www.pipster.io/research/firms/the5ers); [fxprop](https://fxprop.com/report/the-5ers/); [traderssecondbrain](https://traderssecondbrain.com/guides/the5ers-review)
- **NAS100 [SEC].** Commissione $0 (un report del 2024 dice $2 per lotto) — [myfxbook](https://www.myfxbook.com/prop-firms/the5ers); [fxprop report PDF](https://fxprop.com/wp-content/uploads/2024/10/The5ers1.3.pdf)
- **MFFU [SEC].**
  - Pro con trailing EOD; Rapid con trailing intraday (in una fonte, 4% sull'equity in tempo reale).
  - Account: massimo 10, fino a 5 sim funded da 25K o 50K (Rapid EOD: 3).
  - Pro: payout ogni 14 giorni, 80/20, cap $100.000 per utente.
  - Automazione non documentata.

  Fonti — [proptradingvibes MFFU](https://proptradingvibes.com/blog/myfundedfutures-payout-rules); [tradervana](https://www.tradervana.com/guides/myfundedfutures-rules); [pipback](https://pipback.com/blog/my-funded-futures-review)
- **Altre firm, dalle note del 2026-11-06 [SEC].**
  - Bulenox: bot e copier ammessi se costruiti in proprio; 5 Master account.
  - Alpha Futures: chiusura del piano Premium a luglio 2026 senza onorare i payout pendenti.
  - Take Profit Trader: abbonamento mensile, split 80/20.

  Fonte — `research_notes/Mappa edge futures indici intraday/05_prop_firm_costi.md`

### Inferences
- **The5ers High Stakes** è un'alternativa CFD a FTMO 2-Step con regole quasi identiche (statico 10%, daily 5%, news ±2 minuti), ma con policy EA incerta. È il ripiego se FTMO rifiuta o se si supera il suo tetto.
- **Alpha Futures va esclusa** per il precedente sui payout. MFFU Rapid, con trailing intraday, è inadatto a un trend-follower con escursioni avverse ampie (MAE).

### Gaps
- Prezzi The5ers, tetto di allocazione, policy EA e VPS definitiva, spread NAS100.
- Regole MFFU ufficiali.

---

## Q9. Reputazione, cambi di regole 2025-2026, rischio di controparte

### Takeaway
- **Cambi di regole frequenti** su tutte le firm grandi nel 2026: Apex 4.0 (marzo), Topstep (split 90/10 da gennaio, nuovi percorsi XFA, consistency al 55% senza buffer, DLL promozionale da giugno), FTMO (consistency 1-Step da ottobre, drawdown Growth ridotto il 5 nov 2026), FundedNext (Legacy dismesso in ottobre, commissioni nuove).
- **Rischio di payout negati:** concentrato in Apex (causa *Lawton*, lamentele su denials) e nelle firm minori chiuse nel 2026.
- **Nessuna azione regolatoria nuova** trovata contro le firm in lista.

### Cited Findings
- **Topstep.** Chi è entrato prima del 12 gen 2026 ha il 100% sui primi $10K. Offerta a tempo sui cap con DLL dal 2 giu. Consistency al 55% "hard line… What happened to the buffer? There is no buffer" — [Topstep Payout Policy](https://help.topstep.com/en/articles/8284233-topstep-payout-policy); [Consistency at Topstep](https://help.topstep.com/en/articles/8284208-consistency-at-topstep) [UFF-letto]
- **FTMO.** Consistency 1-Step dal 12 ott 2026 (5 ott secondo il blog). Drawdown di Growth 100K e 150K ridotto il 5 nov 2026 — [Trading Update 8 Oct 2026](https://ftmo.com/en/blog/trading-updates/trading-update-8-oct-2026/); [Futures Trading Update 5 Nov 2026](https://ftmo.com/en/futures/blog/trading-updates/futures-trading-update-5-nov-2026/) [UFF-snippet]
- **FundedNext.** Dichiara oltre $350M di payout cumulati, di cui circa il 64% verificato on-chain da un tracker indipendente. Penale di $1.000 se un payout supera le 24 ore — [traderpayout](https://traderpayout.com/prop-firm-news/fundednext-350-million-payout-claim-verification) [SEC]. Un denial del 2025 su HFT nel prodotto futures — [propfirmgauge](https://propfirmgauge.com/payouts/) [SEC]
- **Apex.** Causa *Lawton* (24 lug 2026), lamentele sui payout, regola del "30% negative P&L" — vedi Q5 [SEC]
- **Chiusure 2026.** FundingTicks (gennaio), Seacrest, MyFundedFX, ATFunded, Rev One, FundedSeat, The Funded Trader offline — [edge-ledger](https://edge-ledger.io/prop-firm-payout-tracker); note del 2026-11-06 [SEC]
- **Regolazione.** Il caso CFTC contro My Forex Funds è stato archiviato a maggio 2025 con sanzioni contro la CFTC. Una consultazione CFTC sulle challenge-based firm sarebbe aperta fino al 30 nov 2026, ma non è confermata su cftc.gov — note del 2026-11-06 [SEC]

### Inferences
- **Diversificare il rischio di controparte:** non più del 50% delle fee spese su una sola firm.
- **Congelare in preregistrazione** la versione delle regole con data, perché cambiano più volte all'anno.

### Gaps
- Trustpilot e Reddit sono bloccati: non ho dati diretti sulle lamentele recenti per FundedNext, Tradeify e Lucid.

---

## Q10. Classifica per il profilo della strategia e parametri per il Monte Carlo

### Takeaway
**Classifica (per una strategia trend-following intraday a 0,9 trade al giorno, 40% di win rate, rapporto 2,6:1, serie perdenti fino a 20 giorni, automatizzata e in cloud):**

1. **FTMO CFD 2-Step su US100.cash**, 100K oppure 2×100K entro il tetto di $400K.
2. **FTMO Futures Pro 50K su MNQ**.
3. **Tradeify Select (Flex) 50K oppure LucidFlex 50K su MNQ**, entrambi one-time con funded senza consistency.
4. **FundedNext Stellar 2-Step 100K su NDX100**, l'alternativa CFD.
5. **FundedNext Futures Rapid Pro / Flex**.
6. **Topstep**: il migliore documentato, ma vieta il VPS. Ha senso solo con esecuzione manuale.
7. **Apex**: escluso, perché vieta l'automazione.

**Da modellare nel Monte Carlo:**

- **(A)** FTMO 2-Step 100K, drawdown statico;
- **(B)** FTMO Futures Pro 50K, trailing EOD con rapporto 1:1;
- **(C)** Topstep 50K XFA Standard come benchmark a trailing EOD verificato su fonte primaria. In alternativa, o in aggiunta, LucidFlex 50K come variante one-time.

### Cited Findings
- I parametri vengono dalle sezioni Q1-Q8, con la loro etichetta di affidabilità. Nessuna fonte esterna in più.

### Inferences
**Aritmetica del profilo (stime mie, da verificare con il Monte Carlo sui trade reali del backtest):**
- **Expectancy.** Per trade E = 0,4×2,6 − 0,6×1 = **+0,44R**, deviazione standard circa 1,76R. Per giorno (0,9 trade) circa **+0,40R**, deviazione standard circa 1,68R.
- **Serie perdenti.** La serie massima attesa di trade perdenti consecutivi è circa 10 trade su 1 anno, circa 11 su 2 anni e circa 13 su 5 anni. Con le serie di 20 giorni osservate, un drawdown storico realistico è dell'ordine di 10-15R. **Sizing prudente: R ≈ drawdown consentito / 15.**
- **Tempo di superamento** (approssimazione con moto browniano con drift, edge assunto reale; la probabilità di passare, circa 97-98%, è ottimistica perché ignora l'incertezza sull'edge):

  | Programma | Barriere in R | Giorni attesi |
  |---|---|---|
  | Futures 50K, target $3.000 e drawdown $2.000 | R = $133, target 22,5R | ~57 (~2,7 mesi) |
  | FTMO Futures Pro 50K, $3.000 / $3.000 | R = $200, target 15R | ~38 |
  | FTMO 2-Step 100K, fase 1 (10% / 10%) | R = $667, target 15R | ~38 |
  | FTMO 2-Step 100K, fase 2 (5%) | R = $667 | ~19 |

- **Reddito atteso nel funded.** Su 50K futures a R = $133 sono circa $53 al giorno, cioè circa $1.100 al mese. Su un CFD da 100K a R = $667 sono circa $264 al giorno, cioè circa $5.500 al mese lordi prima dello split, a parità di edge. **Il drawdown statico del 10% rende per dollaro di fee 3-5 volte più dei futures da 50K.**

**Caratteristiche delle regole in ordine di importanza per questo profilo:**
1. **Tipo e ampiezza del drawdown rispetto alla serie perdente.**
   - Statico dal saldo iniziale (FTMO 2-Step, FundedNext 2-Step e Lite, The5ers High Stakes): il migliore, il pavimento non sale mai.
   - Trailing EOD che si blocca al saldo iniziale (+$100 per alcune firm): accettabile. Dopo +drawdown di profitto diventa statico.
   - Trailing intraday sul picco non realizzato (Apex intraday, MFFU Rapid, FundedNext Instant): da evitare, perché punisce il trend-follower che restituisce profitto aperto prima dell'uscita.
   - Topstep XFA: l'MLL si azzera a $0 dopo ogni payout, quindi ogni prelievo erode il cuscinetto.
2. **Automazione ammessa e possibile da cloud o VPS.**
   - Topstep vieta il VPS, quindi niente automazione in cloud. Apex vieta l'automazione.
   - Tradeify vieta lo stesso bot su più firm. FundedNext vieta EA identici su più account propri.
   - FTMO ammette EA e, per i futures, l'automazione [SEC/MEM]: la più compatibile.
3. **Consistency.**
   - In valutazione, 40-55% non è un problema: con circa 15-22 R di target e vincite da 2,6R, il miglior giorno vale circa il 12-17% del target.
   - Nelle finestre di payout brevi (Rapid Pro 3 giorni al 40%, LucidPro 40%, Tradeify Growth 35%, Direct e Lightning al 20%) una singola vincita da 2,6R su un profitto netto piccolo fa fallire la condizione: servono più giorni prima del prelievo. Da evitare 20-35%.
   - Preferibili i funded senza consistency: Lucid Flex, Tradeify Select Flex, FundedNext Flex, FTMO Futures, FTMO 2-Step.
4. **Daily loss limit.** Quasi irrilevante: con 0,9 trade al giorno la perdita giornaliera tipica è 1R, raramente 2R. Va solo controllato che DLL ≥ 3R. FTMO Pro 50K ha $1.000 = 5R: ok. FundedNext 1-Step ha il 3% = 4,5R a R = 0,67%: ok.
5. **Fee model e tempo atteso.** Con circa 40-60 giorni per passare, l'abbonamento mensile (Topstep $49-95, FTMO Futures Growth "$119/mo" [SEC]) costa 2-3 rate. Il one-time (Tradeify, Lucid, FundedNext, FTMO CFD con fee rimborsabile) è preferibile.
6. **Massimo di account e allocazione.**
   - Conta per la scala, ma gli account replicati sono un'unica scommessa correlata: con una serie perdente di 20 giorni saltano insieme.
   - Tetti: FTMO $400K per strategia; FundedNext Futures 5 account e $750K in challenge; Topstep 5 XFA; Tradeify e Lucid 5 funded; Apex 20 PA.
7. **News.** Finestre di ±2 minuti (FTMO Account [MEM], The5ers), ±5 minuti (Topstep Tier 1, solo nuove aperture) e la regola del 40% dei profitti entro 5 minuti (FundedNext CFD funded). Tutte codificabili come filtro calendario: costo atteso piccolo per un trend-follower, da quantificare nel backtest.

**Parametri per il Monte Carlo** (da congelare in `research/preregistration/` dopo una verifica primaria delle voci [UFF-snippet], [SEC] e [MEM]):

- **(A) FTMO CFD 2-Step 100K, US100.cash**
  - Fase 1: target +10% ($10.000). Fase 2: target +5% ($5.000). Minimo 4 giorni di trading per fase. Nessun limite di tempo [MEM].
  - Max loss **statico**: equity ≥ $90.000 in ogni istante, flottante incluso.
  - Daily loss: perdita del giorno (chiuso + flottante) ≤ $5.000, reset alle 00:00 CE(S)T, cioè alle 18:00 ET: irrilevante essendo flat alle 16:00.
  - Nessuna consistency.
  - Funded: stesse soglie, split 80% (90% con scaling) [MEM], payout ogni 14 giorni [MEM], fee circa €540 rimborsata al 1° payout [MEM].
  - Filtro news: nessuna apertura o chiusura da 2 minuti prima a 2 minuti dopo CPI, NFP e FOMC [MEM].
  - Costi: spread US100 da 1 a 2 punti indice per round-trip, commissione $0 [SEC]; stress 2× = 4 punti. Swap: nessuno, essendo flat.
  - Tetto: $400K, quindi al massimo 4 account da 100K con lo stesso EA.
  - Sizing da testare: R ∈ {0,4%; 0,5%; 0,67%; 0,8%} del saldo iniziale.
- **(B) FTMO Futures Pro 50K, MNQ**
  - Target $3.000.
  - Drawdown trailing EOD di $3.000: pavimento = max(saldo EOD) − $3.000, bloccato a $50.000. Il breach si verifica sull'equity intraday.
  - DLL rigido di $1.000: il breach chiude l'account.
  - Consistency 40% solo in valutazione: miglior giorno ≤40% del target.
  - Funded: 5 giorni qualificanti da $200 o più, prelievo fino al 100% del profitto, cap per richiesta circa $5.000, split 90/10.
  - Fee: da verificare (one-time o mensile).
  - Commissione MNQ: usare $1,22 round-turn come proxy (Topstep), stress 2×. Slippage di 1 tick per lato.
- **(C) Topstep 50K, MNQ** (benchmark verificato su fonte primaria)
  - Combine: $49 al mese + $149 di attivazione (oppure $95 al mese senza attivazione). Target $3.000. Consistency: miglior giorno ≤55% del profitto totale, altrimenti il target diventa miglior giorno / 0,55.
  - MLL di $2.000 trailing sul saldo EOD, monitorato intraday, bloccato al saldo iniziale.
  - DLL opzionale di $1.000: includerlo, perché raddoppia i cap.
  - XFA Standard: saldo da $0, MLL da −$2.000 bloccato a $0. Payout dopo 5 giorni vincenti da $150 o più, fino al 50% del saldo, cap $2.000 ($4.000 con il DLL all'acquisto), split 90/10. **Dopo ogni payout l'MLL si azzera a $0.**
  - Variante XFA Consistency: 3 giorni, best day ≤40% della finestra, cap $3.000 ($6.000 con DLL).
  - News Tier 1: nessuna apertura NQ da −5 a +5 minuti; MNQ fino a 3 contratti.
  - Flat alle 15:10 CT. Commissioni MNQ $1,22 / NQ $3,78 round-turn.
  - Nota: modellabile solo con esecuzione manuale, per il divieto di VPS.
- **(C′) LucidFlex 50K, MNQ** (alternativa one-time)
  - Fee circa $130 [SEC]. Target $3.000.
  - MLL trailing EOD di $2.000, bloccato al saldo iniziale +$100 [SEC/UFF-snippet].
  - Consistency in valutazione al 40% o al 50%.
  - Funded: nessuna consistency, 5 giorni da $150 o più, prelievo del 50% del profitto con cap $2.000, split 90/10.
  - Commissioni MNQ circa $1,00 round-turn [SEC].

**Metriche consigliate per il Monte Carlo:**

- probabilità di superamento;
- giorni al superamento;
- fee attese spese per account funded;
- distribuzione dei payout netti a 6 e 12 mesi;
- probabilità di perdere il funded prima del 1° e del 3° payout;
- EV netto per dollaro di fee.

Su ogni metrica va fatta una sensibilità all'incertezza dell'edge: per esempio win rate 35% invece del 40% e rapporto 2,2 invece di 2,6.

### Gaps
- Tutti i parametri di FTMO (A, B), Lucid e FundedNext vanno riconfermati sulle pagine ufficiali prima di congelarli. Gli host da aggiungere all'allowlist sono quelli elencati in testa al file.
- Policy VPS e cloud per FTMO, FundedNext, Lucid e Tradeify: è decisiva visto il vincolo "solo cloud" del committente.
- Non ho verificato se il comportamento intraday del CFD US100 (cash più fair value, orari e spread fuori RTH) replica a sufficienza il backtest su NQ. Va misurato su dati del broker della firm prima del Monte Carlo (A).
