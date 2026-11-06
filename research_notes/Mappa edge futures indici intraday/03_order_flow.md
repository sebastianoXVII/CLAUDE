# Order flow and LOB information as short-term predictors in ES/NQ: academic evidence vs retail folklore, and what is usable at minutes-to-hours horizons

Research note, 2026-11-06. Method: web search (about 20 calls). **Network limits:** `arxiv.org` and `databento.com` would not resolve from this session, so I could not open full texts or the live Databento pricing page. Paper claims below come from abstracts and indexed summaries (RePEc, SSRN, ar5iv/emergentmind snippets, Kellogg, NBER). Databento prices come from third-party pages and should be checked against https://databento.com/pricing. Statements tagged [UNVERIFIED / background knowledge] come from my prior knowledge and could not be re-confirmed this session.

---

## Q1. Order flow imbalance (OFI), long memory of order flow, propagator: at what horizon does it predict, and is the effect contemporaneous or predictive?

### Takeaway
The strongest OFI result in the literature is **contemporaneous**. Over the same interval, price change ≈ β·OFI, with β inversely proportional to depth and an in-sample R² of roughly 65-70% on US stocks. **Predictive** (lagged) OFI power is small, short-lived and decays rapidly: seconds to a few price changes, not minutes to hours. Trade-sign autocorrelation is very persistent (long memory), but it is offset by liquidity responses, so it does **not** turn into a simple return-predictability edge.

### Cited Findings
- Cont, Kukanov & Stoikov (J. Financial Econometrics 2014, 12(1):47-88) find a linear relation between OFI at Level-I (best bid/ask: limit orders, market orders, cancellations) and price changes, with slope inversely proportional to market depth. It is robust to intraday seasonality and stable across time scales and across 50 NYSE stocks. The relation between price change and *trade volume* is noisier and less robust than the one based on OFI. — [arXiv 1011.6402](https://arxiv.org/abs/1011.6402); [HAL](https://hal.sorbonne-universite.fr/hal-00937055); [IDEAS](https://ideas.repec.org/a/oup/jfinec/v12y2013i1p47-88.html)
- The roughly 70% R² of Cont et al. is contemporaneous, measured over the same period, not forward-looking. — [Towards Data Science summary citing Cont et al.](https://towardsdatascience.com/price-impact-of-order-book-imbalance-in-cryptocurrency-markets-bf39695246f6) (secondary source)
- Cont, Cucuringu & Zhang, "Cross-impact of order flow imbalance in equity markets" (Quantitative Finance 2023, 23(10):1373-1393):
  - Multi-level OFI integrated by PCA gives better in- and out-of-sample results.
  - Once multi-level OFI is used, cross-asset terms add **no** contemporaneous explanatory power.
  - **Lagged** cross-asset OFIs do improve forecasts of future returns (R² and economic gains), but the effect occurs at **short horizons and decays rapidly**.
  - Earlier versions (v1, "Price impact of order flow imbalance: multi-level, cross-sectional and forecasting") made a stronger contemporaneous cross-impact claim that was later dropped.
  - Sources: [arXiv 2112.13213v4](https://arxiv.org/abs/2112.13213v4); [EconPapers QF](https://econpapers.repec.org/RePEc:taf:quantf:v:23:y:2023:i:10:p:1373-1393); [arXiv v1](https://arxiv.org/abs/2112.13213v1)
  - [UNVERIFIED / background knowledge] The forecasting horizons tested are on the order of 1 minute ahead, with out-of-sample R² for future returns at about 1% or less. I could not open the PDF to confirm the exact numbers.
- E-mini specific: Takahashi (arXiv 2508.06788, 2025) estimates a structural VAR of returns and OFI on 1-second BBO data for ES in 15-minute windows. Macro news announcements raise the price impact of OFI and reduce flow persistence ("flow impact"). This is a study of impact dynamics, not a trading backtest. — [arXiv 2508.06788](https://arxiv.org/abs/2508.06788)
- Easley, López de Prado & O'Hara (flow toxicity paper) report that the autocorrelation of E-mini order imbalance over 2008-2011 is only about 0.21 for time bars of 1 to 240 minutes. Imbalance at minute horizons is therefore only weakly persistent. — [NYU Stern PDF](https://www.stern.nyu.edu/sites/default/files/assets/documents/con_035928.pdf)
- Boyarchenko et al. (NY Fed Staff Report 917, "The Overnight Drift"): E-mini return autocorrelations are significant for at most about 30 minutes. Large negative order imbalances at the close relate to subsequent overnight returns. This is a horizon relevant to non-HFT traders, but the paper is about the overnight effect, not an intraday OFI strategy. — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf)
- Lillo & Farmer (Studies in Nonlinear Dynamics & Econometrics 2004), on the LSE:
  - Market-order signs have **long memory**: autocorrelation decays as a power law with exponent about 0.6 (Hurst about 0.7).
  - The memory is offset by anti-correlated fluctuations in transaction size and liquidity, which keeps returns roughly uncorrelated ("efficient").
  - Bouchaud et al. found the same property independently on the Paris Bourse.
  - Lillo, Mike & Farmer (2005) attribute the long memory to the splitting of large metaorders.
  - Sources: [arXiv cond-mat/0311053](https://arxiv.org/abs/cond-mat/0311053); [IDEAS](https://ideas.repec.org/a/bpj/sndecm/v8y2004i3n1.html); [arXiv cond-mat/0412708](https://arxiv.org/abs/cond-mat/0412708)
- In the propagator model, price diffusion is maintained by impact decaying over time in a way that offsets the long memory of the order flow. — [ar5iv 2506.07711](https://ar5iv.labs.arxiv.org/html/2506.07711)
  - [UNVERIFIED / background knowledge] Bouchaud, Gefen, Potters & Wyart (2004, Quantitative Finance, "Fluctuations and response in financial markets: the subtle nature of 'random' price changes") introduced the transient-impact propagator. Its core message is that sign predictability is "priced in" by liquidity providers.

### Inferences
- For a trader at the minute-to-hour horizon, OFI is mainly a **descriptive** variable: it explains why price moved, not where it will go. Its predictive component lives at the scale of seconds or a few price changes, which is HFT territory (see Q2 and Q5).
- Trade-sign autocorrelation (metaorder splitting) is real and persistent. But the market "knows" it: liquidity reacts, so persistent flow does not imply persistent returns. Reading "aggressive buyers keep coming" on a delta chart is a weak signal for direction at minutes or hours.
- Possible exceptions with some support: (a) end-of-session imbalance and overnight returns (NY Fed); (b) regime changes around macro news (Takahashi).

### Gaps
- I found no peer-reviewed study that runs OFI → future ES/NQ returns over 1-60 minute horizons **out of sample net of costs**. Most OFI studies use US stocks (NYSE/Nasdaq) or crypto.
- Exact out-of-sample R² and horizon numbers in Cont-Cucuringu-Zhang are not verified (arXiv blocked).

---

## Q2. Queue imbalance / book imbalance, Cartea-Donnelly-Jaimungal, deep learning on the LOB (DeepLOB, Kolm-Turiel-Westray): horizons and critiques

### Takeaway
Best-queue imbalance strongly predicts the **direction of the next mid-price move** (one tick ahead), especially in **large-tick** instruments, and ES is large-tick. Deep models add little beyond order-flow features. Predictability **peaks at about 2 price changes** and then declines. Practical use is to improve *execution* (fewer adverse fills, better timing of limit orders), not to forecast direction at minute or hour scale.

### Cited Findings
- Gould & Bonart (2016, arXiv 1512.03492): logistic regression of next-mid-move direction on queue imbalance across 10 liquid Nasdaq stocks.
  - The relationship is strongly significant.
  - Classification improvement is "considerable" for large-tick stocks and "moderate" for small-tick stocks.
  - Local logistic regression is slightly better.
  - Sources: [ar5iv 1512.03492](https://ar5iv.arxiv.org/html/1512.03492); [IDEAS](https://ideas.repec.org/p/arx/papers/1512.03492.html)
  - [UNVERIFIED] Improvements of 50-60% (large tick) and 10-30% (small tick) are reported by an aggregator, not checked against the paper. — [emergentmind](https://www.emergentmind.com/papers/1512.03492)
- Cartea, Donnelly & Jaimungal, "Enhancing trading strategies with order book signals" (Applied Mathematical Finance 2018, 25(1):1-35):
  - Volume imbalance on Nasdaq predicts the sign of the next market order and helps predict price moves.
  - Used in a strategy, it **reduces adverse selection costs** and helps limit orders capture favorable moves.
  - Calibration was on H1 2014 and testing on H2 2014. Caveats: the 2014 regime may not be representative, and the book can be manipulated by placing and cancelling orders (spoofing).
  - Sources: [IDEAS](https://ideas.repec.org/a/taf/apmtfi/v25y2018i1p1-35.html); [ORA Oxford full text](https://ora.ox.ac.uk/objects/uuid:006addde-3a03-4d75-89c1-04b59026e1c0/files/me4008e0ecca779b45d59231ebca3e69c); [CXO Advisory summary](https://www.cxoadvisory.com/?p=27752)
- DeepLOB (Zhang, Zohren & Roberts, IEEE Trans. Signal Processing 2019, arXiv 1808.03668): CNN+LSTM on the LOB.
  - On FI-2010 it reaches F1 of about 83% at horizon k=10 events.
  - The authors admit FI-2010 is only 10 days of downsampled, pre-normalized data from a less liquid market, "arguably not sufficient". They also test on LSE data.
  - The metrics are pure ML and **exclude costs**.
  - Sources: [ar5iv 1808.03668](https://ar5iv.arxiv.org/html/1808.03668); [emergentmind DeepLOB](https://www.emergentmind.com/topics/deeplob)
- Critiques:
  - LOBFrame (Briola, Bartolucci, Aste; UCL; arXiv 2502.15757): forecasts become operationally viable mainly in **large-tick** books. In small-tick, noisy books, high ML scores do **not** translate into profitable or feasible signals. — [UCL Discovery PDF](https://discovery.ucl.ac.uk/id/eprint/10218102/1/Deep%20limit%20order%20book%20forecasting%20a%20microstructural%20guide.pdf); [arXiv 2502.15757](https://pdf.arxiv.org/pdf/2502.15757)
  - An MDPI review calls for trading simulations with realistic costs, spread and impact. — [MDPI Mathematics 10(8):1234](https://mdpi.com/2227-7390/10/8/1234)
- Kolm, Turiel & Westray, "Deep order flow imbalance: extracting alpha at multiple horizons from the LOB" (Mathematical Finance 2023, 33(4):1044-1081):
  - Data: 115 Nasdaq stocks, LOBSTER, January 2019 to January 2020.
  - Models trained on stationary **order-flow** inputs (OFI by level) beat models trained on raw books. Simple architectures (MLP/LSTM) are enough.
  - The alpha term structure **peaks at about 2 price changes and then declines**.
  - "Information-rich" stocks, meaning more book updates per price change, are more predictable.
  - Sources: [SSRN 3900141](https://papers.ssrn.com/abstract=3900141); [EconPapers](https://econpapers.repec.org/RePEc:bla:mathfi:v:33:y:2023:i:4:p:1044-1081)
  - QuantPedia notes that trading costs must be considered before any practical use. — [QuantPedia](https://quantpedia.com/how-to-use-deep-order-flow-imbalance/?a=6080)
- A GCN-LSTM paper on ES and VX futures uses Cont-style OFI over 5-360 minute lookbacks as features. It is ML/arXiv with no confirmed peer review, and I did not verify its net results. — [arXiv 2408.05659](https://arxiv.org/pdf/2408.05659)

### Inferences
- ES is a large-tick contract (0.25 point tick with a very deep book), where queue imbalance is most informative, at the **next tick**. NQ has proportionally a much smaller tick relative to price and volatility, so it behaves more like a small-tick book, and queue imbalance is likely less useful there (inference based on Gould-Bonart and LOBFrame).
- A horizon of "about 2 price changes" in ES can last from seconds to a few minutes in quiet sessions, but the move is about 1 tick, which is below round-trip costs for an aggressive trader (spread of 1 tick plus fees). The edge is accessible only if you use it to **decide when and on which side to rest a limit order**, and that is constrained by queue position (Q5).

### Gaps
- No public study of DeepLOB / deep OFI on CME ES/NQ with net-of-cost results.
- I could not verify how many seconds "2 price changes" means for ES across sessions (it requires the data).

---

## Q3. VPIN and the Andersen-Bondarenko critique on the E-mini

### Takeaway
VPIN is the most widely cited "academic order-flow" indicator on ES, and also the most contested. Andersen & Bondarenko show that on the E-mini it peaked **after** the Flash Crash, not before. They also show that its predictive power for volatility comes from **classification errors** in Bulk Volume Classification (BVC), and that it disappears once you control for realized volatility. It is not a validated directional signal.

### Cited Findings
- Easley, López de Prado & O'Hara propose VPIN (order flow toxicity) using volume buckets and BVC. They claim historically high values before the May 6, 2010 Flash Crash. — [NYU Stern PDF "Flow toxicity and liquidity in a high frequency world"](https://www.stern.nyu.edu/sites/default/files/assets/documents/con_035928.pdf)
- Andersen & Bondarenko, "VPIN and the Flash Crash" (J. Financial Markets 2014): VPIN reached its all-time high **after**, not before, the crash, and it is a poor predictor of short-run volatility. — [CREATES rp11_50](https://repec.econ.au.dk/repec/creates/rp/11/rp11_50.pdf); [Kellogg](https://www.kellogg.northwestern.edu/academics-research/research/detail/2014/vpin-and-the-flash-crash/?p=1)
- Andersen & Bondarenko, "Assessing measures of order flow toxicity via perfect trade classification" (CREATES rp13_43) and a related paper in the Review of Finance (2015, 19(1):1-54):
  - VPIN predicts volatility only because rising volatility induces systematic BVC errors.
  - Built with accurate classification (BBO), VPIN behaves in the opposite way to BVC-VPIN.
  - Predictive power disappears after controlling for realized volatility.
  - Sources: [CREATES rp13_43](https://repec.econ.au.dk/repec/creates/rp/13/rp13_43.pdf); [EconPapers RevFin](https://econpapers.repec.org/RePEc:oup:revfin:v:19:y:2015:i:1:p:1-54.); [Kellogg 2015](https://www.kellogg.northwestern.edu/academics-research/research/detail/2015/assessing-measures-of-toxic-order-flow-and-early-warning)
- Counterpoint: a 2012 Berkeley/LBNL study found VPIN gave "strong signals" before the Flash Crash. Andersen himself says that with modifications "there is some encouragement". The debate is not fully closed. — [Strategy+Business](https://strategy-business.com/article/00144); [Kellogg Insight](https://insight.kellogg.northwestern.edu/article/the_trouble_with_vpin)

### Inferences
- For ES, the CME feed **has a native aggressor flag** (Q6), so BVC is not needed. The lesson from the critique is that "imbalance" measures should be benchmarked against plain realized volatility before they are credited with any edge.

### Gaps
- No recent study (2020-2026) found on VPIN net of costs on ES.

---

## Q4. Retail order-flow tools: cumulative delta, footprint, absorption, iceberg detection, volume profile/POC/value area, Market Profile, VWAP. Is there rigorous evidence?

### Takeaway
I found **no peer-reviewed study** that tests cumulative delta, footprint, "absorption", or volume profile/POC/value area as predictors of returns on ES/NQ, net of costs. Most content is vendor or trader material (ATAS, LuxAlgo, TradingView, NexusFi). For VWAP, the academic literature treats it as an **execution benchmark** and does not study it as "support" or an attractor. The pro-VWAP mechanism (VWAP-tracking algorithms) is plausible but has not been measured on intraday price paths.

### Cited Findings
- Volume profile: searching for academic tests of POC and value area as support or resistance returns only vendor and practitioner sources. The 70% value area is a convention (some use 68%). Claims of support and resistance are asserted without hit rates. — [LuxAlgo](https://www.luxalgo.com/library/concept/volume-profile.md); [Tickblaze](https://community.tickblaze.com/foundation-topics/post/understanding-volume-profiles-Cl7Fi34bptjVW1n); [NexusFi wiki](https://nexusfi.com/wiki/trading-wiki/Volume-Profile)
- The vendor itself admits that many "naked POCs" are never retested. — [LuxAlgo](https://www.luxalgo.com/library/concept/volume-profile.md) (vendor marketing; useful only as an admission against interest)
- Order-flow vendor content on ES (ATAS "ES Order Flow") is marketing or education with no out-of-sample tests. — [ATAS blog](https://atas.net/blog/es-order-flow-trading/) (vendor marketing)
- VWAP: academic studies use VWAP as the benchmark for institutional execution (Berkowitz et al. 1988, cited in a NYSE/AMEX study, 1993-2005). They do not test whether price reverts to VWAP. — [CORE PDF](https://core.ac.uk/download/201501336.pdf)
- The claim that VWAP algorithms create mean reversion around VWAP comes from broker and crypto blogs with no data. — [HeyGoTrade](https://www.heygotrade.com/en/learn/volume-weighted-average-price-vwap/); [KuCoin](https://www.kucoin.com/blog/es-what-is-vwap-and-how-to-use-it-in-practice-a-trader-s-guide) (vendor/education)
- Indirect but relevant academic evidence on "cumulative delta":
  - Signed flow is persistent (Lillo-Farmer), but returns remain nearly uncorrelated because liquidity offsets it. — [arXiv cond-mat/0311053](https://arxiv.org/abs/cond-mat/0311053)
  - The contemporaneous component (Cont et al.) dominates. — [arXiv 1011.6402](https://arxiv.org/abs/1011.6402)
  - In practice, cumulative delta is a time integral of trade-only OFI. Academic evidence says OFI that includes cancellations and limit orders explains more than trade volume alone. — [arXiv 1011.6402](https://arxiv.org/abs/1011.6402)
- Icebergs: the ES book is susceptible to placement and rapid cancellation (spoofing), which undermines "absorption" and "big lots on the DOM" readings. — [CXO on Cartea et al.](https://www.cxoadvisory.com/?p=27752)
- [UNVERIFIED / background knowledge] CME Globex does not offer a native iceberg order type to customers. Icebergs are implemented by ISVs or the client and are only partially visible in MBO, through refill patterns after trades. Academic literature on iceberg detection exists (for example, Frey & Sandås on Xetra; Christensen & Woodmansey on CME Globex, Journal of Futures Markets 2013, on GC). I did not verify it this session.
- [UNVERIFIED / background knowledge] Market Profile (Steidlmayer, CBOT 1980s): I know of no peer-reviewed test with a positive net result on ES.

### Inferences
- Cumulative delta and footprint are **trade-only, contemporaneous** visualizations of order flow. The academic evidence suggests they describe the move rather than anticipate it, and that a trade-only OFI is a weaker version of full OFI.
- POC, value area and VWAP may be useful as **reference levels and execution benchmarks**. Any "magnet" effect is an empirical hypothesis that is cheap to test with OHLCV-1m or trades data (Q6). It should be tested against a placebo, for example random levels or the previous day's mid, because levels near the price get "touched" mechanically.
- The prior for an edge net of costs from these tools is low. Treat them as folklore until tested.

### Gaps
- No peer-reviewed study found for cumulative delta, footprint, absorption, POC/VA or VWAP-as-attractor on ES/NQ. This is a true gap (absence of evidence), not a search limitation, but a dedicated search of the Journal of Futures Markets might find something.

---

## Q5. Latency reality: what predictability is left after HFT, retail platform latency, queue position, adverse selection of passive fills

### Takeaway
The window for ES microstructure signals, measured as the ES-SPY arbitrage window, went from about 97 ms to about 7 ms by 2011, and the speed race keeps raising the bar. A retail trader with tens of milliseconds of latency and no control over queue position competes at a structural disadvantage at the horizon where OFI and queue imbalance actually work. What remains for a non-HFT trader is the **minutes-hours** horizon, where the order-flow signal is weak and largely contemporaneous.

### Cited Findings
- Budish, Cramton & Shim (QJE 2015, 130(4):1547-1621), ES vs SPY, 2005-2011:
  - Median arbitrage duration fell from about 97 ms to about 7 ms, while median profit stayed constant at about 0.08 index points per unit.
  - There are about 1,000 opportunities per day.
  - The cause is the continuous limit order book itself, and the speed race only raises the threshold.
  - The physical lower bound is about 4 ms for light to travel Chicago-New York.
  - Sources: [NBER PDF](https://conference.nber.org/conf_papers/f69665.pdf); [EconPapers QJE](https://econpapers.repec.org/RePEc:oup:qjecon:v:130:y:2015:i:4:p:1547-1621); [Richmond Fed](https://www.richmondfed.org/publications/research/econ_focus/2015/q3/research_spotlight)
- Order-book signals are useful mainly to **reduce adverse selection** of limit orders (Cartea et al.), which requires reacting quickly to imbalance changes. — [IDEAS](https://ideas.repec.org/a/taf/apmtfi/v25y2018i1p1-35.html)
- [UNVERIFIED / background knowledge] On ES, matching is FIFO, so priority goes to whoever joins the queue first. Retail orders on a new level arrive behind HFTs, and they get filled mainly when the level is about to be "eaten". That is a classic adverse selection pattern: fill followed by price moving against you. Typical retail round-trip latency (NinjaTrader/Tradovate/Rithmic/Sierra from home) is in the tens of ms. Colocation at Aurora is microseconds. I found no rigorous public source with measured retail latencies on these platforms.

### Inferences
- With alpha at about 2 price changes (Kolm et al.) and windows under 10 ms for cross-asset signals (Budish), retail has no realistic access to directional microstructure alpha.
- Retail can use the LOB for: (a) execution timing (avoid resting a limit when the imbalance is strongly against you); (b) intraday regime and context (liquidity, depth, news); (c) features aggregated over minutes, which still need to be validated.

### Gaps
- I found no academic measurement of adverse selection on retail passive fills in ES specifically, and no study of real retail latencies.

---

## Q6. Data: CME MBO, Databento (schemas, prices), Rithmic/CQG, history costs, reconstructing delta with the aggressor flag

### Takeaway
CME's MDP 3.0 feed provides MBO, meaning individual orders and queue position, from 2017. It also has a **native aggressor flag** (tag 5797), so delta can be reconstructed exactly without tick-rule or BVC heuristics. Databento sells GLBX.MDP3 history pay-per-GB (third-party estimate of about $0.50-2/GB) or by subscription. ES MBO is about 50 GB per month (third-party estimate). Live depth for a non-professional costs about $12-13 per month in CME fees, plus vendor or connection fees.

### Cited Findings
- CME MBO is an order-based feed showing individual queue position, full depth and individual order sizes. Historical data is available "from launch date for each channel" through CME DataMine. Purchasing daily MBO updates does **not** include history. — [CME MBO education](https://www.cmegroup.com/education/market-by-order-mbo.html); [CME Confluence MBO FIX](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/46110437/MBO+FIX)
- Conflict on start date: Databento says MDP 3.0 began in May 2017 and was preceded by legacy FIX/FAST. A CME Confluence page says MBO FIX has been available on 4 exchanges since January 2017. Check per product. — [Databento GLBX.MDP3 docs](https://databento.com/docs/venues-and-datasets/glbx-mdp3); [CME Confluence](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/46110437/MBO+FIX)
- Databento provides a book snapshot at 00:00 UTC each weekday to make historical MBO easier to use. Its docs suggest deriving MBP-10 from MBO to reduce bandwidth and cost. — [Databento GLBX.MDP3](https://databento.com/docs/datasets/glbx-mdp3); [Databento MBP-10 schema](https://databento.com/docs/schemas-and-data-formats/mbp-10)
- Databento pricing:
  - Historical from "$0.50/GB" (homepage), pay-as-you-go or subscription. — [databento.com](https://databento.com/); [pricing](https://databento.com/pricing) (not fetched: blocked)
  - Third-party estimates: $0.50-2/GB depending on schema; ES front-month MBO about 50 GB per month and MBP-10 about 25 GB per month; break-even between pay-per-GB and subscription at about 90 GB per month. — [NexusFi on Databento](https://nexusfi.com/a/data/databento-futures-market-data) (third party; verify)
  - [UNVERIFIED / background knowledge] Databento usually gives about $125 in free credits to new accounts. Its plans (Standard/Plus/Unlimited) changed in 2025, so verify the current figures.
- Retail live fees:
  - CME non-professional Depth of Market for 1 exchange is $12.10 per device per month (June 2026 list), going to $12.50 (January 2027 list). All exchanges bundle: $36.50 going to $37.75. — [CME fee list June 2026](https://www.cmegroup.com/market-data/files/june-2026-market-data-fee-list.pdf); [CME fee list Jan 2027](https://www.cmegroup.com/market-data/files/january-2027-market-data-fee-list.pdf)
  - Brokers and vendors add their own charges: AMP lists $45 for a CME L2 bundle via CQG/Rithmic/TT; Ironbeam lists a $25 per month Rithmic connection fee. — [AMP](https://www.ampfutures.com/trading-info/platform-data-fees/); [Ironbeam](https://www.ironbeam.com/knowledge-base/rithmic-market-data-fees/)
  - Sierra Chart/Denali require a live funded account for CME non-pro fees. — [Sierra Chart support](https://www.sierrachart.com/SupportBoard.php?ThreadID=107159)
- Aggressor flag:
  - In MDP 3.0, Trade Summary carries AggressorSide (tag 5797): 0 = no aggressor, 1 = buy, 2 = sell. One CME page instead labels the values "1 bid / 2 ask", so check the template version.
  - Trades against implied orders and opening or re-open (Velocity Logic) trades may have **no aggressor**.
  - When there is an aggressor, the first Order Detail entry is the aggressing order.
  - Sources: [CME MDP3 Incremental Refresh Trade Summary](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457227733/MDP+3.0+-+Market+Data+Incremental+Refresh+-+Trade+Summary); [CME MDP3 Trade Summary](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457418925/MDP+3.0+-+Trade+Summary); [OnixS AggressorSide](https://ref.onixs.biz/net-cme-mdp3-market-data-handler-guide/f-onixs-cmemdhandler-tags-aggressorside.html)
  - [UNVERIFIED / background knowledge] In Databento's `trades`/`mbo` schemas the `side` field is mapped to A/B/N, where N means no aggressor.
- Delta reconstruction: delta = Σ size·(+1 if aggressor buy, −1 if sell), excluding N. With MBO you can also compute full Cont-style OFI, including cancellations and modifications, at multiple levels.

### Inferences
- A cheap minimal research stack:
  1. Databento `ohlcv-1m` plus `trades` for ES/NQ over several years. This is enough to test VWAP, POC/VA and minute-level delta.
  2. `mbp-1` or `tbbo` to compute Level-1 OFI and queue imbalance.
  3. `mbo` only on a sample of months, at about 50 GB per month for ES, to test multi-level OFI and queue position.
- Note: rolls and contract continuity (ESH/ESM...) and session (RTH vs ETH) affect VWAP and volume profile. Define both explicitly.

### Gaps
- Exact current Databento prices per schema and per dataset not verified (site blocked). CQG and Rithmic historical tick costs not found.

---

## Q7. Studies on the performance of (order-flow-based) discretionary traders

### Takeaway
There is no study isolating "order-flow traders". The best evidence on retail intraday traders in **index futures** (Brazil, mini-Ibovespa) is crushing: about 97% lose money, and there is no evidence of learning.

### Cited Findings
- Chague, De-Losso & Giovannetti, "Day trading for a living?" (SSRN 3423101; FGV EESP TD 525):
  - Data from the Brazilian SEC (CVM) on all individuals who started day trading mini-Ibovespa futures in 2013-2015.
  - Of 19,646 persistent traders, only about 3% had positive net earnings, and only about 0.5% earned more than a bank teller's minimum wage.
  - Average about US$310 per day with a standard deviation of US$2,560.
  - No evidence of learning.
  - Summaries disagree on the observation window (2012-2017 vs the 2013-2015 entry cohort).
  - Sources: [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101); [IDEAS](https://ideas.repec.org/p/spa/wpaper/2019wpecon47.html); [FGV](https://repositorio.fgv.br/items/e87d04fc-4b4c-4a56-ab5a-1c84c1afde1b/full); [QuantPedia](https://quantpedia.com/retail-day-trading-is-an-uphill-battle/)
- [UNVERIFIED / background knowledge] Barber, Lee, Liu & Odean (Taiwan, "Do day traders rationally learn about their ability?" and "The cross-section of speculator skill") find that fewer than 1% of day traders are persistently profitable net of fees.

### Inferences
- The base rate for retail intraday futures trading is strongly negative. An order-flow tool should be judged by its incremental effect against that baseline, and no such evidence exists.

### Gaps
- No study of the performance of users of footprint, delta or DOM tools (only vendor testimonials, which are anecdotal and survivorship-biased).

---

## Synthesis table (for the report writer)

| Signal | Evidence | Predictive horizon | Contemporaneous/predictive | Survives retail costs? |
|---|---|---|---|---|
| OFI Level-1 / multi-level (Cont et al.) | Strong, peer-reviewed | Seconds to about 1 minute, rapid decay | Mainly contemporaneous (R² about 70%) | No (directional); maybe as an execution filter |
| Queue imbalance (Gould-Bonart, CDJ) | Strong, peer-reviewed, large-tick (ES yes) | Next tick | Predictive, 1 tick | No for direction; yes for reducing adverse selection, if latency allows |
| Deep LOB / deep OFI | Peer-reviewed on stocks; ML-only metrics | About 2 price changes | Predictive, small | No public evidence net of costs |
| Trade-sign long memory | Robust stylized fact | Long (power law) | Offset by liquidity | Not an exploitable edge per se |
| VPIN | Contested; critiqued on ES | Not validated | Artifact of BVC | No |
| Cumulative delta / footprint / absorption | No peer review | n/a | Contemporaneous visualization | Unproven (folklore) |
| Volume profile / POC / VA / Market Profile | No peer review | n/a | n/a | Unproven (folklore); testable cheaply |
| VWAP as attractor | Benchmark only; attractor untested | n/a | n/a | Unproven; testable cheaply |
| Close imbalance → overnight (NY Fed) | Fed working paper | Hours, overnight | Predictive | To be evaluated (see other notes on overnight drift) |
