# Risk management, gestione del trade e journaling per un trader sistematico intraday su conti prop (futures indici CME)

Nota di metodo. Ho fatto circa 20 ricerche, ma solo su abstract, record bibliografici e sintesi di terzi. Non ho aperto il testo integrale di nessun paper. I marcatori usati:
- **[abstract]**: affermazione presa da abstract o record bibliografico.
- **[secondario]**: blog, forum, siti di prop firm o di vendor.
- **[derivazione]**: calcolo mio a partire da formule citate. È verificabile e l'ho ricontrollato con Python.
- **[memoria]**: ricordo da letture precedenti, non verificato in questa sessione. Queste voci stanno nei Gap: vanno controllate sul testo prima di trasformarle in regole.

Tesi di fondo: la gestione del trade e il sizing non creano edge. Ridistribuiscono il rischio di un edge che c'è già, oppure lo distruggono. Lo dicono la teoria (teorema di arresto opzionale, Kaminski e Lo) e l'evidenza empirica (Lo e Remorov, Cederburg et al.). Nei conti prop la decisione di rischio che conta di più è la taglia **relativa alla distanza dal Maximum Loss Limit**. I numeri della MC del progetto (`research/results/prop_mc_noise_area_nq.md`) lo confermano.

## 1. Come dimensionare le posizioni sotto un vincolo di drawdown (fisso vs frazionario, Kelly, Kelly vincolato, optimal f, formule di rovina, volatility targeting)

### Takeaway
Nel conto prop l'unità di rischio giusta è il **cuscinetto**, cioè la distanza tra l'equity e il floor del drawdown (2.000 $ su un Topstep 50K). Il nominale da 50.000 $ è l'unità sbagliata. La regola teoricamente ottimale con un floor che segue il massimo (Grossman e Zhou 1993) è un'esposizione proporzionale al cuscinetto. Il Kelly pieno è troppo aggressivo e molto sensibile all'errore di stima; il Kelly frazionario o vincolato al rischio domina. Il volatility targeting riduce le code in modo affidabile, ma i suoi benefici sullo Sharpe sono fragili fuori campione.

### Cited Findings
- **Grossman e Zhou (1993)**, *Mathematical Finance* 3(3):241–276. L'investitore impone che la ricchezza resti sopra α volte il massimo raggiunto (W_t ≥ α·M_t). Con utilità CRRA, la politica ottima investe nell'attivo rischioso **in proporzione al "surplus"** sopra il floor. Il floor è stocastico perché dipende dal massimo corrente, e in questo differisce dalla CPPI con floor fisso — [IDEAS/RePEc](https://ideas.repec.org/a/bla/mathfi/v3y1993i3p241-276.html); [EconPapers](https://econpapers.repec.org/RePEc:bla:mathfi:v:3:y:1993:i:3:p:241-276) [abstract]
- Klass e Nowicki (2005, *Statistics & Probability Letters*) mostrano che la strategia di Grossman e Zhou perde la proprietà di crescita ottima di lungo periodo in tempo discreto — [Lund University](https://www.lunduniversity.lu.se/lup/publication/37b108be-d2da-4ec8-a331-1b0c7cb46310); [EconPapers](https://econpapers.repec.org/RePEc:eee:stapro:v:74:y:2005:i:3:p:245-252) [abstract]
- Letteratura recente sul controllo del drawdown: l'esposizione è proporzionale alla distanza tra il valore del conto e un floor legato al massimo corrente. Avvicinandosi al limite, la politica si comporta come uno stop-loss e il trading si ferma, per cui è stato proposto un meccanismo di "restart" — [arXiv 2303.02613 (Hsieh e Barmish)](https://arxiv.org/pdf/2303.02613); [arXiv 2609.23272](https://arxiv.org/pdf/2609.23272) [abstract]
- **Busseti, Ryu e Boyd (2016)**, "Risk-Constrained Kelly Gambling", *Journal of Investing* 25(3). Estendono Kelly con un vincolo sulla probabilità che la ricchezza scenda sotto un livello. Un limite superiore a questa probabilità rende il problema convesso e garantisce il vincolo. Nelle simulazioni Monte Carlo il limite è vicino al rischio reale. Un solo parametro di avversione al rischio regola il compromesso crescita/drawdown. A pari rischio di drawdown o a pari crescita, le loro puntate battono il Kelly frazionario. L'approssimazione quadratica si collega a Markowitz — [arXiv 1603.06183](https://arxiv.org/pdf/1603.06183); [pagina di Boyd](https://web.stanford.edu/~boyd/papers/kelly.html)
- **Thorp**, "The Kelly Criterion in Blackjack, Sports Betting and the Stock Market". La versione 2006 contiene le sezioni "The case for fractional Kelly" e sulla probabilità che una strategia ne preceda un'altra dopo n prove. Non ho letto il contenuto di quelle sezioni — [PDF 2006 (gwern.net)](https://www.gwern.net/doc/statistics/decision/2006-thorp.pdf); [versione 1997](https://sites.oxy.edu/lengyel/M330/thorp/paper.htm); [Rotando e Thorp 1992](https://escholarship.org/content/qt2sf6m38g/qt2sf6m38g.pdf)
- Una rassegna sperimentale sulle strategie di scommessa sportiva trova che la variante Kelly vincolata al drawdown si comporta in modo molto simile al Kelly frazionario semplice. Conclude che il Kelly frazionario, con la frazione ben calibrata, è la scelta più adatta in pratica — [arXiv 2107.08827](https://arxiv.org/pdf/2107.08827)
- Il Kelly frazionario riduce la volatilità al prezzo di una crescita più lenta — [Wikipedia, Kelly criterion](https://en.wikipedia.org/wiki/Kelly_criterion) [secondario]
- **Optimal f di Vince**. La critica principale è che massimizza la crescita composta ignorando il drawdown. Il drawdown massimo atteso a f ottimo è almeno pari a f_opt (f = 0,5 implica un drawdown ≥ 50%). Piccoli errori di stima allontanano molto dall'ottimo. Il metodo dipende dalla singola peggiore perdita storica. Vince stesso propone una variante vincolata al drawdown, il "secure f" — [MultiCharts](https://www.multicharts.com/support/base/the-foundations-of-money-management-iii/) [secondario]; [NexusFi](https://nexusfi.com/a/risk-management/optimal-f-position-sizing) [secondario]
- Un paper sul *Journal of Risk* propone di sostituire la funzione obiettivo di optimal f con una basata sul drawdown corrente, che secondo gli autori serve meglio gli investitori avversi al rischio rispetto alla soluzione originale di Vince — [Risk.net](https://www.risk.net/journal-of-risk/5603246/risk-averse-fractional-trading-using-the-current-drawdown) [abstract]
- **Formule di barriera (moto browniano con drift).** Siano μ > 0 il drift, σ la volatilità, a la distanza dalla barriera superiore e b quella dalla barriera inferiore.
  - P(toccare mai −b) = exp(−2μb/σ²).
  - P(toccare +a prima di −b) = (e^{2μb/σ²} − 1)/(e^{2μb/σ²} − e^{−2μa/σ²}).
  - A drift zero la seconda formula si riduce a b/(a+b).
  
  Le formule si ricavano dalla martingala esponenziale e^{−2μX/σ²} — [quantvault](https://quantvault.org/problem-416-first-passage-probabilities-and-optimal-barriers-for-brownia.html) [secondario]; [cfrm17](https://cfrm17.github.io/barrierProb.html) [secondario]; [archive.org barrierProbability](https://ia904709.us.archive.org/8/items/barrierProbability/barrierProbability.pdf) [secondario]
- **Moreira e Muir (2017)**, "Volatility-Managed Portfolios", *Journal of Finance* 72(4):1611–1644. Scalare l'esposizione per l'inverso della varianza realizzata del mese precedente aumenta lo Sharpe di vari fattori: mercato, value, momentum, profitability, investment, BAB e carry. Il motivo è che le variazioni di volatilità non sono compensate da variazioni proporzionali del rendimento atteso — [PDF dell'autore](https://amoreira2.github.io/alan-moreira.github.io/VolPortfolios_published.pdf); [NBER w22208](https://www.nber.org/papers/w22208)
- **Cederburg, O'Doherty, Wang e Yan (2020)**, *JFE* 138(1):95–117. Su 103 strategie azionarie, i portafogli gestiti per volatilità **non battono sistematicamente** le versioni non gestite nei confronti diretti. Gli alpha delle spanning regression alla Moreira e Muir non sono implementabili in tempo reale. Le versioni fuori campione fattibili hanno Sharpe ed equivalente certo inferiori, a causa dell'instabilità strutturale delle regressioni — [EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:138:y:2020:i:1:p:95-117) [abstract]
- **Harvey, Hoyle, Korgaonkar, Rattray, Sargaison e Van Hemert (2018)**, "The Impact of Volatility Targeting", *JPM* 45(1):14–33.
  - Oltre 60 asset, con dati giornalieri dal 1926.
  - Lo Sharpe migliora per gli asset di rischio (azioni, credito), effetto legato al leverage effect. Per bond, valute e commodity l'effetto è trascurabile.
  - **La probabilità di rendimenti estremi si riduce in tutte le asset class**, e i drawdown massimi di 60/40 e risk parity si riducono.
  
  Sintesi secondarie riportano uno Sharpe dell'azionario USA che passa da circa 0,40 a 0,48–0,51 — [Duke Scholars](https://scholars.duke.edu/publication/1370354) [abstract]; [Alpha Architect](https://alphaarchitect.com/volatility-targeting-improves-risk-adjusted-returns/) [secondario]
- DeMiguel, Martín-Utrera e Uppal (2024, *JF*) estendono la gestione per volatilità a un contesto multifattoriale — [LBS PDF](https://lbsresearch.london.edu/id/eprint/3716/1/The%20Journal%20of%20Finance%20-%202024%20-%20DeMIGUEL%20-%20A%20Multifactor%20Perspective%20on%20Volatility%E2%80%90Managed%20Portfolios.pdf) [abstract]

### Inferences
- **[derivazione] Kelly e drawdown in tempo continuo.** Con rendimento μ e varianza σ², la leva di Kelly è f* = μ/σ². Usando una frazione c del Kelly:
  - la crescita logaritmica è g(c) = g*·(2c − c²), quindi metà Kelly dà il 75% della crescita massima con metà della volatilità;
  - dalla formula di barriera applicata al log-wealth, la probabilità che la ricchezza scenda **mai** a una frazione x del livello attuale è x^{(2/c − 1)}.
  
  Con Kelly pieno, P(perdere mai il 50%) = 50% e P(perdere mai il 20%) = 80%. Con metà Kelly le stesse probabilità scendono a 12,5% e 51%; con un quarto di Kelly a 0,8% e 21%. Questi numeri spiegano perché nessun professionista usa il Kelly pieno. In più, μ stimato da un backtest è quasi sempre gonfiato (vedi Harvey e Liu nella Q4), quindi il Kelly "vero" è più piccolo di quello stimato.
- **[derivazione] Kelly applicato al nostro candidato (MC NQ: 11,56 $/giorno di media e 153 $ di deviazione standard per 1 MNQ).**
  - Contratti di Kelly = C·μ/σ² = C·0,000494.
  - Con C = 50.000 $ nominali: ≈ 25 MNQ, che con un MLL di 2.000 $ vuol dire bruciarsi quasi certamente.
  - Con C = 2.000 $ di cuscinetto: ≈ 1 MNQ.
  
  Il nominale è l'unità sbagliata. Sul cuscinetto, Kelly dà 1 MNQ, mentre la MC del progetto trova l'ottimo per *passare la challenge* a 2–3 MNQ. La differenza c'è perché l'obiettivo della challenge non è la crescita logaritmica: è una barriera binaria con un costo di tempo (abbonamento mensile). È un problema diverso, che va risolto con la MC e non con Kelly.
- **[derivazione] Tetto teorico per la challenge, barriera statica.** Con target T = 3.000 $ e drawdown D = 2.000 $ statico (non trailing), su orizzonte infinito, P(passare) vale 0,87, 0,69, 0,60 e 0,52 per 1, 2, 3 e 5 MNQ. A edge zero vale D/(D+T) = 0,40.
  - Aumentare la taglia porta P(passare) **verso il valore a edge zero**. Con edge positivo, quindi, la taglia piccola aumenta la probabilità di passare ma allunga i tempi.
  - Con edge negativo vale il contrario: conviene la "bold play" (vedi Gap su Dubins e Savage). Chi ha un edge dubbio e punta grosso sta implicitamente scommettendo di non averlo.
- **[derivazione] Barriera trailing.** Per un moto browniano con drift, la probabilità che il massimo salga di T prima di un drawdown D dal massimo corrente è P = exp(−T·(2μ/σ²)/(e^{2μD/σ²} − 1)). A drift zero si riduce a exp(−T/D). La formula è di Taylor (1975) e Lehoczky (1977), citati da memoria; la verifica del limite a drift zero è mia.
  - Ottengo 0,62, 0,41, 0,35 e 0,29 per 1, 2, 3 e 5 MNQ, con 0,22 a edge zero. Il trailing quasi dimezza la probabilità a edge zero rispetto alla barriera statica (0,22 contro 0,40).
  - Il valore a 2 MNQ (0,41) è coerente con il 43% della MC a 120 giorni.
  - La formula ignora il blocco del MLL al saldo iniziale, che aiuta, e il limite di tempo, che penalizza. Va usata come **controllo di coerenza** dei simulatori, non come sostituto.
- **Fisso vs frazionario nel prop.** Il drawdown concesso è in dollari fissi e non è proporzionale all'equity. Prima del blocco del MLL, il "fixed-fractional" sul saldo nominale è privo di senso. La regola coerente con Grossman e Zhou è: **contratti = floor(k × cuscinetto / rischio in $ per contratto)**, con un tetto. Dopo il blocco del MLL al saldo iniziale, il floor diventa fisso e la regola diventa una CPPI classica.
- **Granularità.** Con 1 MNQ come taglia minima, la regola proporzionale degenera in "taglia fissa minima" quando il cuscinetto è piccolo. Le micro (MES/MNQ) sono necessarie proprio per poter applicare il sizing proporzionale.
- **Volatility targeting in intraday.** Le evidenze di Harvey et al. riguardano orizzonti giornalieri e mensili. Per noi la versione utile è la normalizzazione per trade: contratti tali che lo stop in punti (per esempio k × ATR) valga una quota fissa del cuscinetto in dollari. Le evidenze dicono che questo riduce le code (Harvey et al.). Non garantisce uno Sharpe migliore (Cederburg et al.), e lo Sharpe migliora soprattutto sugli indici azionari (leverage effect), che è il nostro caso.

### Gaps
- Non ho letto le sezioni di Thorp sul Kelly frazionario. La formula x^{(2/c−1)} è una mia derivazione sul moto browniano geometrico. [memoria] Ricordo che MacLean, Thorp e Ziemba ("Good and bad properties of the Kelly criterion", 2010) riportano risultati equivalenti.
- [memoria] Taylor (1975, *Annals of Probability*) e Lehoczky (1977, *Annals of Probability* 5(4)) per la formula del drawdown dal massimo: riferimenti da verificare.
- [memoria] Dubins e Savage, *How to Gamble If You Must* (1965): in un gioco sfavorevole la "bold play" massimizza la probabilità di raggiungere un obiettivo. Da verificare.
- [memoria] Carver (*Systematic Trading*, 2015) raccomanda di non superare metà Kelly e di scontare lo Sharpe del backtest. Chan (*Quantitative Trading*, 2008; *Algorithmic Trading*, 2013) usa f = m/s² e propone la CPPI per il vincolo di drawdown massimo. Vince (*The Mathematics of Money Management*, 1992; *The Leverage Space Trading Model*, 2009). Riferimenti non verificati sul testo.
- Non ho trovato studi sul volatility targeting a frequenza intraday sui futures indici.

## 2. Gestione del trade: cosa aiuta davvero (uscite parziali, break-even, trailing, time stop, MAE/MFE, R-multiple)

### Takeaway
Se il prezzo è una martingala, nessuna regola di uscita cambia il valore atteso lordo. Se ha drift positivo, ogni uscita anticipata lo riduce. Gli stop aggiungono valore **solo** in presenza di momentum o di cambi di regime nell'asset, e quelli stretti sono uccisi dai costi (Kaminski e Lo 2014; Lo e Remorov 2017). Uscite parziali e break-even cambiano la forma della distribuzione dei risultati, non la sua media. MAE e MFE sono utili per diagnosticare i trade, ma usarli per scegliere stop e target è una delle fonti di overfitting più comuni.

### Cited Findings
- **Kaminski e Lo (2014)**, "When do stop-loss rules stop losses?", *Journal of Financial Markets* 18:234–254.
  - Se i rendimenti seguono una passeggiata casuale, uno stop-loss semplice può solo ridurre il rendimento atteso.
  - Con momentum o regime switching, invece, lo stop può aggiungere valore.
  - Su dati mensili USA 1950–2004, alcune regole (passare ai bond dopo perdite cumulate) aggiungono 50–100 bp al mese nei periodi di stop-out, sfruttando un momentum condizionato alle perdite.
  
  Risultato coerente con gli abstract: [DSpace MIT (PDF)](https://dspace.mit.edu/bitstream/handle/1721.1/114876/Lo_When%20Do%20Stop-Loss.pdf); [EconPapers](https://econpapers.repec.org/RePEc:eee:finmar:v:18:y:2014:i:c:p:234-254) [abstract]. Secondo una sintesi, gli stop più lenti funzionano meglio — [hvst.com](https://www.hvst.com/posts/momentum-and-stop-losses-oNRTmKm1) [secondario]
- **Lo e Remorov (2017)**, *Journal of Financial Markets* 34:1–15.
  - Su un ampio campione di azioni USA, **gli stop stretti sottoperformano il buy-and-hold per eccesso di costi di trading**.
  - Possono sovraperformare solo per titoli con autocorrelazione dei rendimenti sufficientemente alta.
  - Riducono il rischio di ribasso, ma "non sostanzialmente".
  - Uno stop eseguito con un giorno di ritardo fa marginalmente meglio, e molto meglio per gli stop stretti, grazie alla reversione nel periodo di ritardo.
  
  [EconBiz](https://econbiz.de/Record/stop-loss-strategies-with-serial-correlation-regime-switching-and-transactions-costs-andrew/10013011284) [abstract]; [CXO Advisory](https://www.cxoadvisory.com/equity-premium/stop-losses-on-stock-positions-in-depth) [secondario]; [DSpace MIT](https://dspace.mit.edu/handle/1721.1/107017)
- Han, Zhou e Zhu ("Taming Momentum Crashes"): uno stop al 10% riduce la peggior perdita mensile del momentum equal-weighted da −49,79% a −11,34% (1926–2011). È un esempio di stop utile su una strategia con crash rari, ma a frequenza mensile e su una strategia cross-section — [crossingwallstreet](https://crossingwallstreet.com/?p=28384) [secondario]
- Sintesi di Lo e Remorov: gli stop aiutano con momentum forte e tendono a danneggiare nei mercati mean-reverting — [QuantSeeker](https://www.quantseeker.com/p/do-stop-loss-rules-add-value-in-tactical) [secondario, paywall]
- Una pagina TradingView sugli stop-loss nel retail cita numeri precisi (−67% di drawdown, una "meta-analisi") che non sono verificabili. È un esempio di folklore pseudo-scientifico, **da non usare** — [TradingView](https://www.tradingview.com/chart/ES1!/EshQukmT-Stop-Loss-Strategies-in-Retail-Trading) [secondario, inaffidabile]

### Inferences
- **Principio cardine (teorema di arresto opzionale).** Per un prezzo martingala, qualunque regola di uscita che dipende solo dalla storia passata (stop, target, trailing, break-even, uscita parziale) ha P&L atteso lordo pari a zero. Al netto dei costi ha P&L atteso negativo. La gestione può aggiungere valore solo sfruttando una dipendenza reale: il drift della strategia dopo l'ingresso, momentum condizionato, mean reversion o regime. È la generalizzazione del risultato di Kaminski e Lo. Conseguenza operativa: **ogni regola di gestione è un'ipotesi da pre-registrare e testare come una strategia**, non una best practice.
- **Uscite parziali e scaling out.** Uscire con metà posizione a +1R e con il resto a +3R equivale a gestire due strategie, una con target a 1R e una con target a 3R. Media e varianza sono combinazioni pesate delle due. Lo scaling out riduce la varianza e aumenta la percentuale di trade vincenti, ma non può superare la migliore delle due componenti. Si testa confrontando le due componenti pure sugli **stessi ingressi**, con un confronto appaiato. Non ho trovato letteratura peer-reviewed specifica.
- **Break-even stop.** In una martingala aumenta i trade chiusi a zero e i costi, e non cambia la media lorda. Nel prop ha un effetto reale: riduce la profondità dell'escursione avversa e quindi il consumo del MLL intraday. Va valutato sulla metrica della barriera (P di bruciarsi), non sulla media.
- **Trailing stop.** Funziona se la strategia è trend-following, perché sfrutta l'autocorrelazione. Danneggia se la strategia è mean-reverting (Lo e Remorov). Il candidato Noise Area/momentum è trend-following, quindi un trailing *largo* è un'ipotesi plausibile da testare. Uno stretto verrebbe probabilmente ucciso dai costi.
- **Time stop.** È giustificato solo se il P&L atteso condizionato decade con il tempo di permanenza. Va misurato con la curva E[r(t, t+h) | segnale] al variare di h: si esce quando il rendimento atteso marginale scende sotto il costo. Per i futures indici l'uscita a fine sessione è comunque obbligata dalle regole intraday delle prop.
- **MAE/MFE senza overfitting.**
  1. Le distribuzioni di MAE di vincenti e perdenti **dipendono dalla regola di uscita in uso**: cambiando lo stop cambia chi è "vincente". Scegliere lo stop "appena oltre la MAE tipica dei vincenti" è quindi circolare. Va ricalcolato rifacendo il percorso con il nuovo stop, cioè ri-simulando le barre.
  2. Va pre-registrata una piccola griglia (per esempio 3–5 multipli di ATR), non una ricerca continua.
  3. Bisogna cercare un **plateau** nella superficie di performance, non un picco.
  4. Si sceglie in-sample, si verifica una sola volta sull'hold-out e si conta la griglia nella correzione per test multipli.
  5. Si esprime tutto in R o in unità di volatilità, non in punti, così la regola resta stabile tra regimi di volatilità.
- **R-multiple ed expectancy (Tharp).**
  - R = P&L / rischio iniziale; expectancy = media degli R.
  - Il "System Quality Number" di Tharp, √N·media(R)/dev.std(R), è numericamente **una statistica t** sui trade.
  - Va quindi trattato con la stessa disciplina: t > 3, correzione per test multipli, autocorrelazione.
  
  L'R è utile come unità di misura per il journal e per confrontare setup, ma non è una teoria.

### Gaps
- Non ho trovato studi peer-reviewed su scaling out, break-even o target multipli in intraday sui futures. La letteratura sugli stop è su azioni e a frequenza giornaliera o mensile.
- [memoria] Sweeney, *Maximum Adverse Excursion: Analyzing Price Fluctuations for Trading Management* (Wiley, 1997), e *Campaign Trading* (1996), origine del concetto di MAE. Non verificato sul testo.
- [memoria] Tharp, *Trade Your Way to Financial Freedom* (1999; 2ª ed. 2007): R-multiple, expectancy, position sizing come "chiave"; SQN in pubblicazioni successive. Le affermazioni di Tharp sull'importanza del sizing non hanno supporto empirico peer-reviewed. Il sizing cambia la distribuzione della ricchezza, non l'edge per contratto.

## 3. Controlli sull'equity e sul rischio di rovina (stop giornaliero, de-risking da drawdown, filtri sull'equity curve, serie di perdite)

### Takeaway
Per un sistema con expectancy positiva e trade indipendenti, ogni riduzione condizionata della taglia (stop giornaliero, de-risking dopo un drawdown, filtro sull'equity curve) **riduce il P&L atteso** in proporzione al rischio tolto, e riduce anche la probabilità di rovina. È uno scambio, non un guadagno gratuito. Un controllo aggiunge valore netto solo se i risultati della strategia sono autocorrelati, oppure se il vincolo è una barriera (come nel prop), dove ridurre la varianza vicino al floor ha un valore proprio (Grossman e Zhou). Non ho trovato evidenze peer-reviewed a favore del "trade the equity curve".

### Cited Findings
- I filtri sull'equity curve (on/off con media mobile su 30–50 trade chiusi) vanno confrontati con la strategia intatta e con un **salto casuale dei trade**. Un filtro che smussa solo il rumore riduce l'expectancy — [LuxAlgo](https://www.luxalgo.com/library/concept/equity-curve-based-throttling/) [secondario]
- Sul forum ProRealCode c'è un'evidenza aneddotica: stare fuori finché la media non torna sotto l'equity avrebbe funzionato meglio che ridurre la taglia. Non è controllata — [ProRealCode](https://www.prorealcode.com/reply/60657/) [secondario, aneddotico]
- Per implementare un filtro sull'equity bisogna simulare tutti i segnali anche durante la pausa, così che la curva "ombra" continui ad aggiornarsi — [NinjaTrader forum](https://forum.ninjatrader.com/forum/ninjatrader-7/platform-technical-support/50331-equity-curve-sma) [secondario]
- Il controllo del drawdown basato sul cuscinetto (Grossman e Zhou; Hsieh e Barmish) è l'unica base teorica solida per il de-risking da drawdown. Vicino al limite equivale a uno stop e richiede una regola di ripartenza — [arXiv 2303.02613](https://arxiv.org/pdf/2303.02613) [abstract]
- Gli stop a livello di portafoglio dopo perdite cumulate aggiungono valore solo con momentum condizionato (Kaminski e Lo 2014) — [DSpace MIT](https://dspace.mit.edu/handle/1721.1/114876) [abstract]
- Anche un sistema a expectancy positiva può portare alla rovina se il rischio è mal gestito — [wiki.turtletrading.vn](https://wiki.turtletrading.vn/concepts/drawdown) [secondario]
- Regole prop pertinenti: il MLL di Topstep è trailing su base di fine giornata ma **monitorato in tempo reale sul P&L non realizzato**, e un tocco intraday chiude il conto. Sul Daily Loss Limit le fonti sono in conflitto: opzionale, oppure rimosso dagli account TopstepX nuovi dal 25 agosto 2024 — [Topstep help: MLL](https://intercom.help/topstep-llc/en/articles/8284204-what-is-the-maximum-loss-limit); [Topstep release notes](https://intercom.help/topstep-llc/en/articles/8284100-topstep-release-notes); [pickmytrade](https://blog.pickmytrade.io/topstepx-rules-payouts-drawdown-automation/) [secondario]

### Inferences
- **Stop giornaliero, sistema automatico.** Con trade i.i.d., interrompere dopo −X $ toglie trade con expectancy positiva e riduce la media giornaliera. Il beneficio è troncare la coda sinistra giornaliera, ed è prezioso quando un singolo giorno può toccare il MLL. Va calibrato sulla MC della barriera: lo stop giornaliero è utile se riduce P(bruciarsi) più di quanto riduca P(passare) entro l'orizzonte. Si testa come parametro pre-registrato.
- **Stop giornaliero, esecuzione umana.** Ci sono evidenze comportamentali di "loss chasing" dopo perdite intraday tra i trader professionisti (vedi Gap su Coval e Shumway 2005). Per qualsiasi componente discrezionale o di override manuale lo stop giornaliero è quindi una protezione contro un'autocorrelazione *indotta dal trader*, e il suo valore è reale.
- **Ridurre la taglia dopo un drawdown, sistema a expectancy positiva.**
  - Senza autocorrelazione: perdi crescita attesa e guadagni minore probabilità di rovina.
  - Con un vincolo di barriera (prop): è la politica di Grossman e Zhou, quindi corretta *in forma proporzionale al cuscinetto*. "Dimezzare dopo X%" ne è una discretizzazione grossolana.
  - Rischio specifico: ridurre la taglia nel drawdown e ripristinarla solo a un nuovo massimo rallenta il recupero. Su una strategia trend-following con serie negative fino a 20 giorni, come il candidato NQ, può trasformare un drawdown normale in un'uscita di fatto.
- **"Trade the equity curve".** Con risultati i.i.d. il filtro equivale statisticamente a saltare trade a caso: riduce la media e non migliora il rapporto rischio/rendimento. Ha senso solo se c'è autocorrelazione nei risultati per trade o per giorno. Va quindi testata **prima** l'autocorrelazione (vedi sotto), e solo se è significativa si pre-registra il filtro, confrontandolo con il salto casuale a parità di numero di trade saltati.
- **Test diagnostici da codificare (TDD):**
  1. Runs test di Wald-Wolfowitz su vincite e perdite.
  2. Autocorrelazione dei P&L giornalieri ai lag 1–5, con Ljung-Box.
  3. Confronto della distribuzione della serie negativa più lunga osservata con quella del bootstrap i.i.d. e a blocchi.
- **Statistiche delle serie di perdite [derivazione]:**
  - P(k perdite consecutive in uno specifico gruppo di k trade) = q^k.
  - La serie negativa più lunga su n trade ha valore atteso di circa log_{1/q}(n·(1−q)) (vedi Gap su Schilling).
  - Esempio con q = 0,55 di perdite e n = 500: ≈ log_{1/0,55}(225) ≈ 9 perdite di fila. Serie di 9–10 perdite sono quindi *normali* e non indicano che l'edge sia morto.
  - La MC del progetto trova già 20 giorni non positivi consecutivi nello storico NQ. Ogni regola di "kill" va calibrata su questa distribuzione, non sull'intuito.

### Gaps
- [memoria] Coval e Shumway (2005), "Do Behavioral Biases Affect Prices?", *Journal of Finance* 60(1): i market maker del CBOT che perdevano al mattino aumentavano il rischio nel pomeriggio. Locke e Mann (2005, *JFE*), "Professional trader discipline and trade disposition". Non verificati in questa sessione.
- [memoria] Schilling (1990), "The Longest Run of Heads", *College Mathematics Journal*, per la formula della serie più lunga. Non verificato.
- Non ho trovato alcuno studio peer-reviewed sul "trade the equity curve" né sul de-risking a gradini ("−50% dopo X% di drawdown") per sistemi a expectancy positiva. Le uniche basi sono la teoria (Grossman e Zhou, Kaminski e Lo) e aneddoti.
- Regole prop: le fonti secondarie sono in conflitto, quindi va verificata sul sito ufficiale la versione corrente di Daily Loss Limit e MLL degli account XFA (funded).

## 4. Journaling come strumento di ricerca (campi, tassonomia dei setup, ricerca per similarità, miglioramenti senza data snooping, forward test)

### Takeaway
Per un sistema automatico il journal è un **dataset di ricerca point-in-time**. Deve registrare cosa il sistema sapeva al momento della decisione (feature, versione della regola, prezzo atteso) e cosa è successo (fill, slippage, MAE/MFE, motivo di uscita). Ogni modifica a ingressi o uscite tratta dal journal è un nuovo test, da pre-registrare e contare nei test multipli. Il forward test di qualche mese **non può confermare statisticamente** un edge con Sharpe intorno a 1. Serve a verificare l'implementazione e la coerenza con il backtest. Per una conferma statistica servono anni (MinTRL).

### Cited Findings
- **Harvey e Liu (2015)**, "Backtesting", *JPM* 41(1):13–28.
  - Lo Sharpe si converte in una statistica t, il p-value si corregge per il numero di test e si riconverte.
  - Lo "sconto" (haircut) è non lineare: gli Sharpe alti sono penalizzati poco, quelli marginali molto. Il 50% fisso è solo una regola empirica.
  - Il paper fornisce anche una soglia minima di profitto.
  
  [PDF Duke](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF); [CME (copia)](https://www.cmegroup.com/content/dam/cmegroup/education/files/backtesting.pdf)
- **Bailey e López de Prado**, "The Sharpe Ratio Efficient Frontier", *Journal of Risk*. Lo Sharpe probabilistico permette di stabilire la lunghezza del track record necessaria per rifiutare, con una data confidenza, l'ipotesi che lo Sharpe vero sia sotto una soglia. La formula della lunghezza minima è:

  MinTRL = 1 + [1 − γ₃·SR + (γ₄−1)/4·SR²]·(z_α/(SR − SR*))²

  dove SR è lo Sharpe per periodo (non annualizzato), γ₃ la skewness e γ₄ la curtosi — [Risk.net](https://www.risk.net/journal-risk/2223785/sharpe-ratio-efficient-frontier) [abstract]; [Portfolio Optimizer](https://portfoliooptimizer.io/blog/the-probabilistic-sharpe-ratio-bias-adjustment-confidence-intervals-hypothesis-testing-and-minimum-track-record-length/) [secondario]; [PerformanceAnalytics MinTrackRecord](https://rdrr.io/cran/PerformanceAnalytics/man/MinTrackRecord.html)
- Deflated Sharpe Ratio: corregge per bias di selezione, overfitting del backtest e non normalità — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551) [abstract]

### Inferences
- **Campi del journal** (schema proposto, da implementare in `research/lab/journal.py`, che già esiste nel repo):
  1. *Identità.* trade_id, account_id, strategia, `setup_id` + versione della regola (hash del commit), modalità (backtest/paper/demo/live).
  2. *Decisione (point-in-time).* timestamp del segnale, vettore delle feature calcolato solo con dati ≤ t (timestamp della barra sorgente), regime (volatilità realizzata, gap di apertura, giorno macro sì/no, minuti dall'apertura).
  3. *Ordine.* tipo, prezzo atteso (decisione), prezzo inviato, prezzo eseguito, **slippage = implementation shortfall**, latenza, fill parziali.
  4. *Rischio.* stop e target iniziali, R in $, contratti, cuscinetto MLL all'ingresso, rischio/cuscinetto.
  5. *Percorso.* MAE e MFE in R e in $, tempo al MAE e al MFE, P&L non realizzato minimo rispetto al MLL intraday.
  6. *Uscita.* motivo (stop/target/trailing/tempo/fine sessione/override manuale), P&L lordo, commissioni, P&L netto in R.
  7. *Conformità.* flag di deviazione dalle regole con motivo. Per un sistema automatico deve essere sempre zero; se non lo è, si tratta di un bug o di un override da analizzare a parte.
  
  Il backtest scrive nello **stesso schema**, così il confronto backtest/live è un join.
- **Tassonomia dei setup.**
  - Ogni setup è una regola deterministica con id e versione: condizione di contesto, trigger, ingresso, stop, uscita.
  - Una gerarchia a 2–3 livelli basta, per esempio famiglia (momentum/reversal/evento) → setup → variante.
  - Non si creano categorie a posteriori guardando i risultati: sarebbe un test multiplo non contato.
  - Si definisce la tassonomia prima, la si congela in `research/preregistration/` e la si estende solo con una nuova versione.
- **Ricerca per similarità ("schematica" simile).**
  - *Feature.* Solo informazioni disponibili all'ingresso: rendimenti normalizzati per ATR delle ultime N barre, posizione nel range di apertura, distanza da VWAP o prior close in σ, volatilità relativa, ora, gap, contesto overnight. Si standardizzano con statistiche calcolate **solo** sul passato (rolling o espanding).
  - *Metodo.* k-NN (euclidea o Mahalanobis) sul vettore. Per la forma del prezzo, DTW o correlazione su finestre normalizzate.
  - *Anti-hindsight.* I vicini si cercano solo tra trade **strettamente precedenti**, con embargo di almeno un giorno per evitare sovrapposizioni di informazione. Niente feature che usano il resto della sessione (high o low del giorno, chiusura). Il risultato del vicino si osserva solo se il suo trade era chiuso prima di t.
  - *Valutazione.* Il predittore k-NN è un modello come un altro. Va valutato in walk-forward e confrontato con il tasso base del setup. k e le feature si fissano prima del test, e ogni combinazione provata entra nella correzione per test multipli.
  - *Uso realistico.* Come filtro di contesto (salta i trade i cui 30 vicini hanno expectancy ≤ 0), da pre-registrare e testare sull'hold-out.
- **Migliorare ingressi e uscite senza snooping (protocollo):**
  1. Si formula l'ipotesi dalla parte "esplorativa" del journal.
  2. Si pre-registra in `research/preregistration/` con regola esatta, metrica, soglia e campione minimo.
  3. Si testa su dati che non hanno generato l'ipotesi: hold-out temporale o trade futuri.
  4. Si correggono i test multipli con Harvey e Liu, Holm o il Deflated Sharpe.
  5. Si adotta o si scarta senza ritocchi.
- **[derivazione] Campione minimo per una modifica.** Per rilevare un miglioramento Δ della media in R con α = 5% bilaterale e potenza dell'80% servono n ≈ 2·(1,96+0,84)²·σ²_R/Δ² trade per braccio. Con σ_R = 1,2 e Δ = 0,1R: ≈ 2.260 trade per braccio.
  - Un test **appaiato** (stessi ingressi, uscita A contro B, possibile perché l'uscita si ri-simula sulle barre) usa la varianza della differenza, molto più piccola. È il modo corretto di testare le regole di uscita.
  - Per gli ingressi il test appaiato non è possibile, ed è per questo che i filtri d'ingresso sono più facili da sovra-adattare.
- **[derivazione] Lunghezza del forward test (MinTRL, ignorando skew e curtosi).**
  - Sharpe annuo 1,2 (giornaliero 0,0756): 474 giorni per z = 1,645 (95% unilaterale), 700 per z = 2 e **1.575 giorni (≈ 6 anni) per t = 3**.
  - Sharpe annuo 2: 170, 252 e 567 giorni.
  - Code grasse e skew negativo allungano ancora i tempi.
  
  Il forward test (paper o demo, 2–3 mesi) **non serve a provare l'edge**. Serve a:
  - verificare che fill e slippage reali stiano entro le ipotesi di costo;
  - verificare che la distribuzione giornaliera del forward sia coerente con quella del backtest, per esempio con il percentile del P&L cumulato e del drawdown forward nella distribuzione bootstrap del backtest;
  - fissare un criterio di stop sequenziale pre-registrato: per esempio, si uccide la strategia se il P&L forward cade sotto il 5° percentile della distribuzione bootstrap a pari durata.
- Mettere a confronto il P&L reale con quello del backtest nello stesso periodo (shadow backtest sui giorni live) separa gli errori di implementazione dall'assenza di edge.

### Gaps
- Non ho trovato fonti pubbliche e verificabili su quali campi registrino i desk professionali. Lo schema sopra è una mia sintesi.
- [memoria] Perold (1988), "The Implementation Shortfall: Paper versus Reality", *JPM*: definizione dello slippage come differenza decisione/esecuzione. Non verificato.
- [memoria] López de Prado, *Advances in Financial Machine Learning* (2018): purged k-fold ed embargo per evitare leakage tra osservazioni sovrapposte. Aronson, *Evidence-Based Technical Analysis* (2006): data-mining bias, White's Reality Check, permutazioni Monte Carlo. Non verificati sul testo.
- Non ho trovato studi empirici sull'efficacia della ricerca k-NN "per analogia" sui trade intraday.

## 5. Rischio specifico prop (conti multipli correlati, budget per le fee di valutazione, taglia nella fase funded)

### Takeaway
N conti sulla stessa strategia hanno una correlazione vicina a 1: sono **leva**, non diversificazione. Si bruciano insieme negli stessi giorni, e il numero effettivo di scommesse indipendenti resta circa 1. Il budget per le fee va trattato come capitale di rischio separato, con un tetto deciso prima e un criterio statistico di stop. Nella fase funded, payout limitati da cap e regole di consistenza, contro una perdita totale del conto, creano un payoff asimmetrico che giustifica una taglia *più prudente* che in valutazione. La forma corretta è proporzionale al cuscinetto, non un "dimezza" fisso.

### Cited Findings
- Le regole delle prop su copy trading e numero di conti sono riportate in modo contraddittorio dalle fonti secondarie:
  - Topstep: circa 5 conti; per alcune fonti il copy trading è ammesso, per altre no.
  - Apex: fino a 20 conti, con copy trading tra conti propri.
  - Topstep disattiverebbe il copy trading durante l'elaborazione di un payout (fonte singola).
  
  [propfirmpath](https://propfirmpath.pages.dev/compare/apex-vs-topstep) [secondario]; [futureshive](https://www.futureshive.com/blog/topstep-vs-apex-2026) [secondario]; [pickmytrade](https://blog.pickmytrade.io/topstepx-rules-payouts-drawdown-automation.md) [secondario]
- Topstep sarebbe tornato al drawdown trailing EOD a maggio 2026, dopo una breve fase statica. Apex ha cambiato le regole dal 1° marzo 2026 (consistenza al 30% per i conti "Legacy", 50% per i nuovi). Lo split dei payout varia per fonte (Topstep 90/10; Apex 100% fino a 10K o 25K, secondo la fonte) — [futureshive](https://www.futureshive.com/blog/topstep-vs-apex-2026) [secondario]; [propfirmescape](https://propfirmescape.pages.dev/blog/apex-evaluation-rules-2026) [secondario]; [curvedtrading](https://curvedtrading.com/articles/en/reviews/topstep-vs-apex/) [secondario]
- Express Funded Account di Topstep: se il conto scende al MLL o sotto, viene chiuso definitivamente. Il MLL sale con il saldo di fine giornata, non scende mai e si blocca al saldo iniziale — [Topstep XFA rules](https://topstep.com/express-funded-account-rules); [Topstep help MLL](https://intercom.help/topstep-llc/en/articles/8284204-what-is-the-maximum-loss-limit)
- Una fonte secondaria riporta che solo lo 0,71% "arriva in fondo" alle valutazioni Topstep. Il dato non è verificato e la fonte è di qualità ignota — [propfirm-escape-pod](https://propfirm-escape-pod.pages.dev/blog/topstep-evaluation-rules-decoded) [secondario, non verificato]

### Inferences
- **[derivazione] Conti correlati.** La varianza della somma è N·σ²·(1+(N−1)ρ) e il numero effettivo di scommesse è N_eff = N/(1+(N−1)ρ). Con ρ ≈ 1 su segnali identici, N_eff ≈ 1 qualunque sia N.
  - P(bruciare tutti i conti) ≈ P(bruciarne uno): i conti cadono negli stessi giorni.
  - Il costo in fee cresce come N, mentre la probabilità di avere *almeno un* conto che passa cresce pochissimo.
  - Partire in date diverse crea massimi trailing diversi e decorrela un poco gli esiti, ma i P&L giornalieri restano identici.
  - Più conti hanno senso solo come modo di **scalare la taglia oltre i limiti per conto o oltre i cap di payout**, dopo che l'edge è confermato. Mai come diversificazione.
  - La vera diversificazione richiede strategie con P&L giornalieri a bassa correlazione, misurata sui dati.
- **Budget per le fee di valutazione.** Ogni tentativo è un'opzione: perdi la fee (più i mesi di abbonamento) oppure ottieni un conto funded con un valore atteso di payout V. Il criterio di valore atteso è P(pass)·V > fee totale attesa. Regole proposte:
  1. Un tetto massimo di fee deciso in anticipo dal committente (è una decisione di rischio sua).
  2. P(pass) stimata dalla MC con l'edge **dimezzato**, per prudenza.
  3. **[derivazione] Stop statistico.** Se la MC dice P(pass) = 25%, la probabilità di 10 fallimenti consecutivi è 0,75¹⁰ = 5,6%, e di 11 è 4,2%. Dopo circa 11 fallimenti di fila si rifiuta p = 25% al 5%. Gli 11 tentativi necessari per uccidere la tesi devono stare *dentro* il budget, altrimenti il budget non basta neanche a imparare qualcosa.
  4. I tentativi si fanno in sequenza, non in parallelo sulla stessa strategia, così ogni esito aggiorna la stima prima della fee successiva.
- **Taglia nella fase funded.** Le differenze rispetto alla valutazione:
  - il conto ha un **valore di continuazione**, cioè i payout futuri: perderlo costa più della fee;
  - l'upside di un giorno eccezionale è limitato da cap e regole di consistenza, mentre il downside (chiusura del conto) è intero.
  
  Con un payoff concavo, la teoria (Grossman e Zhou: esposizione proporzionale al cuscinetto) indica di ridurre la taglia rispetto all'ottimo "da passaggio". Prima del blocco del MLL si parte piccoli (cuscinetto = D) e si cresce con il cuscinetto. Dopo il blocco al saldo iniziale, la taglia può crescere con il saldo accumulato sopra il floor, ma i prelievi riducono il cuscinetto (su questo punto vedi i Gap).
  
  "Dimezzare una volta funded" è quindi ragionevole come approssimazione. Quello che va codificato e simulato con le regole XFA reali è: contratti = f(cuscinetto, regole payout).

### Gaps
- Non ho verificato su fonti ufficiali le regole correnti di payout XFA di Topstep (cap, giorni minimi, consistenza, effetto dei prelievi sul MLL) né le regole di Apex sul copy trading. Le fonti secondarie si contraddicono. Va fatto sul sito ufficiale prima di simulare la fase funded, che la MC del progetto segnala come mancante.
- Non ho trovato letteratura accademica sulla gestione ottima di conti di valutazione a pagamento con barriere. Il problema somiglia all'arresto ottimo con costo per tentativo, ma non ho fonti specifiche.

## 6. Quali regole e quale codice derivano da queste evidenze?

### Takeaway
Le regole difendibili sono poche e tutte testabili:
- sizing proporzionale al cuscinetto MLL, con tetto;
- stop espressi in unità di volatilità e scelti da una griglia pre-registrata;
- nessuna regola di gestione "di folklore" senza test appaiato;
- diagnostica di autocorrelazione prima di qualsiasi filtro sull'equity;
- MinTRL e consistenza bootstrap come criteri del forward test;
- conti multipli solo dopo la conferma dell'edge.

### Cited Findings
- Base teorica del sizing proporzionale al cuscinetto — [Grossman e Zhou 1993](https://ideas.repec.org/a/bla/mathfi/v3y1993i3p241-276.html) [abstract]
- Base per testare gli stop come ipotesi e non come dogma — [Kaminski e Lo 2014](https://dspace.mit.edu/handle/1721.1/114876); [Lo e Remorov 2017](https://dspace.mit.edu/handle/1721.1/107017)
- Base per gli sconti ai test multipli — [Harvey e Liu 2015](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF)
- Base per la lunghezza del forward test — [Bailey e López de Prado, Journal of Risk](https://www.risk.net/journal-risk/2223785/sharpe-ratio-efficient-frontier)

### Inferences
- **Regole candidate**, ciascuna da pre-registrare e testare con TDD in `research/lab/`:
  - **R1 Sizing.** contratti = min(tetto, floor(κ · cuscinetto / (stop_punti · $/punto))). κ si sceglie con la MC della barriera (P(pass) e P(bruciarsi) a 120 giorni) con l'edge dimezzato. Controllo di coerenza con le formule di barriera statica e trailing della Q1.
  - **R2 Stop.** Multiplo di ATR intraday scelto da una griglia di ≤ 5 valori, in-sample, con verifica unica sull'hold-out. Si accetta solo se la superficie è un plateau.
  - **R3 Gestione.** Break-even, uscite parziali e trailing: ognuno è un'ipotesi separata, con un test appaiato sugli stessi ingressi e il P&L netto più P(bruciarsi) come metriche. Di default non si usano.
  - **R4 Stop giornaliero.** Parametro testato sulla MC. Obbligatorio per qualunque intervento manuale.
  - **R5 Filtro sull'equity.** Vietato a meno che runs test e Ljung-Box non mostrino autocorrelazione significativa. In quel caso va testato contro il salto casuale.
  - **R6 Kill switch.** P&L forward cumulato sotto il 5° percentile del bootstrap del backtest a pari durata, oppure slippage medio oltre 2× le ipotesi di costo.
  - **R7 Prop.** Tentativi sequenziali, budget di fee fissato dal committente, stop statistico binomiale. Conti multipli solo dopo la conferma (T7 e forward coerente), e dichiarati come leva.
- La sola cosa che può migliorare l'edge per contratto è l'ingresso o il filtro di contesto. Lì è più facile sovra-adattare, quindi lì serve la massima disciplina: campione grande, hold-out e niente test appaiati possibili.

### Gaps
- La calibrazione di κ, dello stop giornaliero e della taglia funded richiede le regole XFA ufficiali, non ancora verificate.
- Tutte le formule di barriera assumono un moto browniano con drift costante. I P&L intraday reali hanno code grasse e volatilità che cambia nel tempo, quindi la MC con bootstrap a blocchi resta lo strumento decisionale.
