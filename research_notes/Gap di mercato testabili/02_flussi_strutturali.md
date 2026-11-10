# Mechanical and structural order flows in US index futures and ETFs (status: November 2026)

Method note: these notes come from web searches only. Direct fetches of SSRN, EDHEC, Bloomberg Law and several other hosts were blocked in this session. Many effect sizes therefore come from abstracts, search snippets or secondary summaries rather than from full-text tables. Each item is marked [P] for primary academic or exchange material, [S] for secondary (sell-side via press, blogs, aggregators), or [U] for unverified.

Cost benchmark used throughout (from the assignment): ES 0.33 points and NQ 0.45 points per round trip, about 0.6–1.0 bp. Hurdle: gross effect at least 3× cost (about 2–3 bp per trade) and enough events for t > 3 within about 7 years.

Power arithmetic (my own inference, used in every "Inferences" block): t ≈ (mean/sd) × √N. Over 7 years:
- Daily event: N ≈ 1,760, so mean/sd must be at least 0.07.
- Monthly event: N ≈ 84, so mean/sd ≥ 0.33.
- Quarterly event: N ≈ 28, so mean/sd ≥ 0.57.
- Annual event: N ≈ 7, so it is untestable.

A full-day ES return has a standard deviation of about 1% (roughly 16% annualized vol). That figure is my assumption, not sourced. On that basis, monthly or quarterly events need a per-event edge of roughly 30–60 bp if held for a full day. They need roughly 5–10 bp if confined to a 10–30 minute window, depending on that window's volatility, which I could not source (see Gaps).

---

## 1. Closing auction and MOC imbalances (NYSE/Nasdaq publications from 15:50 ET): do they predict the 15:50–16:00 move in SPY/ES?

### Takeaway
No study I found tests published imbalances against the 15:50–16:00 return of SPY or ES. The stock-level literature finds that imbalance information adds only modestly to price discovery, mostly in small caps with weak evidence in large caps. Auction-price dislocations reverse mostly overnight, which the "flat by 16:10, no overnight" rule cannot capture. This flow has a weak prior for ES/NQ.

### Cited Findings
- Bogousslavsky & Muravyev, "Who Trades at the Close? Implications for Price Discovery and Liquidity," Journal of Financial Markets. Auction prices rarely settle inside the bid-ask spread, mainly because of the binding tick size, and auction price deviations "revert quickly and almost completely on average." [P] — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1386418123000502); [June 2021 working paper PDF](https://static1.squarespace.com/static/6310c0b9bb63a25599f4418c/t/634ffc92f81e226b2c30654f/1666186387645/who-trades-at-the-close_June2021.pdf)
- Same paper: on the day Tesla joined the S&P 500, the auction price was up to 3% away from the pre-close midpoint, with about $150.8B traded in the auction. The deviation fully reversed overnight, and auction buyers lost about $4.5B. [P/S] — [AEA 2021 listing](https://aeaweb.org/conference/2021/preliminary/paper/H9T4hef7); [Bloomberg/BQ coverage (S)](https://www.bloombergquint.com/markets/noise-for-sale-in-giant-u-s-auctions-used-to-end-stock-sessions)
- Same paper: the authors use the different start times of NYSE and Nasdaq imbalance dissemination as identification. Disseminated imbalance information adds to price discovery, but not enough to explain how uninformative closing price deviations are, and the evidence for large stocks is weak. The working paper uses 15:45 for NYSE and 15:50 for Nasdaq, while other sources put both at 15:50. The exact NYSE start time is inconsistent across sources and should be checked against the current NYSE rulebook. [P] — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1386418123000502); [WP PDF](https://static1.squarespace.com/static/6310c0b9bb63a25599f4418c/t/634ffc92f81e226b2c30654f/1666186387645/who-trades-at-the-close_June2021.pdf)
- Same paper: on S&P 500 rebalancing days there is "little evidence of abnormal price deviations at the auction relative to the volume traded." After an S&P 500 addition (deletion), a stock's closing-auction share of volume rises 20% (falls 15%) permanently. [P] — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1386418123000502)
- Price impact in the closing auction is lower than in continuous trading, except for Nasdaq microcaps, and is modeled as a square-root function of order size (Goyal, Jegadeesh & Wu, JFQA, December 2025). [P] — [JFQA PDF](https://jfqa.org/wp-content/uploads/2026/01/25551_Price_Impact.pdf)
- NYSE versus Nasdaq: closing-auction price changes are more likely to reverse on NYSE, attributed to late floor-broker orders. Another estimate says Nasdaq auction price impact was 58% larger than NYSE's over 2010–2020. Hu & Murphy (2020) find that NYSE pre-auction information is less accurate than Nasdaq's. [P] — [JFE "Closing auctions: Nasdaq versus NYSE"](https://www.sciencedirect.com/science/article/abs/pii/S0304405X21005092); [Management Science "Vestigial Tails?"](https://pubsonline.informs.org/doi/10.1287/mnsc.2023.00884)
- An Imperial College MSc thesis regresses forward returns on order-imbalance data published in the last 10 minutes for S&P 500 and Russell 2000 stocks. Results are mixed: predictability is stronger for NYSE and Russell names, and for several venue/index combinations the R² is not significantly different from zero. Not peer reviewed. [P, thesis] — [Imperial thesis PDF](https://t4awstest.cc.ic.ac.uk/media/imperial-college/faculty-of-natural-sciences/department-of-mathematics/math-finance/MORAND_CLEA_01805978.pdf)
- The indicative match price is strongly mean-reverting because the imbalance itself mean-reverts during the dissemination period. [P, arXiv] — [Dynamical regularities of US equities opening and closing auctions](https://arxiv.org/pdf/1802.01921)
- Earlier work on the information content of MOC imbalances: Spatt et al., NBER Market Microstructure 2009. [P] — [NBER conference PDF](https://conference.nber.org/confer/2009/mms09/spatt.pdf)
- BMLL: on Russell reconstitution day more than 34% of daily notional traded in the closing auction, and "auction dislocation" spiked across most Russell names. [S, vendor research] — [BMLL "Into the Close"](https://www.bmlltech.com/files/documents/Into-the-close_article.pdf)
- BlackRock reviews global MOC activity and the growth of closing-auction share (July 2020). [S] — [BlackRock ViewPoint](https://BlackRock.com/corporate/literature/whitepaper/viewpoint-a-global-perspective-on-market-on-close-activity-july-2020.pdf)

### Inferences
- The documented MOC effect is a dislocation of the auction print relative to the midpoint, and it reverses overnight. ES and NQ do not take part in the equity auction; they trade continuously around it. Any 15:50–16:00 effect would have to come from SPY/ES arbitrage pulling futures toward the auction print. The rule allows ES to be held 16:00–16:10, but the reversal evidence is overnight or next-open, not 16:00–16:10. No source documents a reversal inside 16:00–16:10.
- Directional predictability ex ante: the sign of the aggregate S&P 500 imbalance at 15:50 is known, so direction is predictable in principle. No index-level study shows that the sign maps to a 15:50–16:00 ES move larger than 2–3 bp. A daily test is cheap to run (about 1,760 events in 7 years, so power is good) if historical NOII/NYSE imbalance feeds can be bought. The prior is weak, and this overlaps heavily with the already-dead last-half-hour momentum test, because imbalances largely reflect LETF and other momentum flows.

### Gaps
- No study of aggregate (index-level) published imbalance versus the SPY/ES 15:50–16:00 or 16:00–16:10 return.
- The "close is the new open" phrase: no academic source found under that title. It appears to be market-commentary framing.
- Cushing & Madhavan (2000, "Stock returns and trading at the close," JFM): no URL was retrieved in this session, so its numbers are not reported here.

---

## 2. Leveraged and inverse ETF rebalancing (Cheng & Madhavan 2009; Ivanov & Lenkey 2018; Barbon et al. 2022): 2020–2026 sizes

### Takeaway
LETF rebalancing is fully predictable in direction once the day's return is known: it buys after up days and sells after down days, into the close. Its size has grown sharply in 2025–2026. However, the academic evidence on index-level price impact ranges from "negligible" (Ivanov & Lenkey, controlling for flows) to "economically meaningful but decaying over time" (Barbon et al.). This flow is essentially the mechanism behind the last-half-hour momentum the program has already found dead after costs. The residual opportunity, if any, is conditional on extreme days.

### Cited Findings
- Cheng & Madhavan (JOIM 2009, Barclays Global Investors WP): aggregate LETF rebalancing is a same-direction flow at the close. Secondary summaries report that a 1% broad-market move implies LETF demand of about 16.8–17% of MOC volume, and a 5% move about 50% (based on 2008–2009 MOC volumes). [P via S] — [JOIM PDF](https://joim.com/wp-content/uploads/emember/downloads/p0283.pdf); [JFP 2011 summary](https://www.financialplanningassociation.org/sites/default/files/2021-08/JAN11%20Inverse%20and%20Leveraged%20ETFs%20-%20Considering%20the%20Alternatives.pdf)
- Ivanov & Lenkey (JFM 2018, vol. 41, pp. 36–56): after controlling for capital flows and standard risk factors, LETF rebalancing has a negligible effect on late-day returns and volatility. [P] — [Penn State abstract](https://pure.psu.edu/en/publications/do-leveraged-etfs-really-amplify-late-day-returns-and-volatility/); [RePEc](https://ideas.repec.org/a/eee/finmar/v41y2018icp36-56.html)
- Rodier, Haryanto, Shum & Hejazi (2012): LETF rebalancing explains about one third of late-day volatility, and more than half on large-move days. A front-running backtest earned a 104% cumulative gross return (0.60% per trade) over June 2006–July 2011. That is gross, in a crisis-era sample, and across ETFs rather than ES. [S] — [CXO Advisory](https://www.cxoadvisory.com/volatility-effects/front-running-leveraged-etfs-at-the-end-of-the-day)
- Lenkey's 2024 survey (QFE) calls the literature mixed and notes methodological limitations in most papers. [P] — [AIMS Press](https://www.aimspress.com/article/id/676a38d5ba35de0ad141c3c3)
- Barbon, Beckmeyer, Buraschi & Moerke (SFI WP 22-40, April 2022): LETF rebalancing and option gamma hedging both create end-of-day momentum or reversal. The LETF effect is economically larger than the options channel, but it has decreased over time and attracts more liquidity provision, so its price effects are shorter-lived. Gamma effects persist through the sample. Effects revert at the next day's open. [P] — [SFI listing](https://www.sfi.ch/en/publications/n-22-40-liquidity-provision-to-leveraged-etfs-and-equity-options-rebalancing-flows-evidence-from-end-of-day-stock-prices); [SSRN 3925725](https://papers.ssrn.com/abstract=3925725); [FoFI 2022 PDF](https://wp.lancs.ac.uk/fofi2022/files/2022/08/FoFI-2022-027-Mathis-Moerke.pdf)
- Barbon et al. effect size (secondary extraction, garbled decimals): a one-standard-deviation increase in LETF flow raises end-of-day returns by about 3–4% of one standard deviation of end-of-day returns, described elsewhere as about 4× the average last-half-hour return. This is a stock-level (cross-sectional) result, not ES. [U] — [NFA portal](https://portal.northernfinanceassociation.org/viewp.php?n=2240036708); [ResearchGate](https://www.researchgate.net/publication/355381896_The_Role_of_Leveraged_ETFs_and_Option_Market_Imbalances_on_End-of-Day_Price_Dynamics)
- Sell-side size estimates per 1% move:
  - BofA: about $971M of S&P 500 and about $2.3B of Nasdaq-100 buying or selling per 1% move, undated in the snippet. [S] — [Seeking Alpha](https://seekingalpha.com/news/4505651-stocks-with-the-highest-amount-of-money-leveraged-that-could-sway-etfs-bofa)
  - A later note: about $979M S&P 500 and about $2.2B Nasdaq-100 per 1%. On one record day BofA estimated LETFs sold about $4B of S&P 500 and about $13B of Nasdaq-100 exposure into the close. [S] — [TheStreet Pro](https://pro.thestreet.com/market-commentary/the-week-ahead-cpi-and-equity-flows-test-a-shaken-market)
  - Morgan Stanley: about $7B per 1% drop across all equities, including single-stock LETFs, with LETF AUM at a record $117B (date likely 2024). [S] — [Nasdaq.com](https://www.nasdaq.com/articles/leveraged-etfs-trigger-volatility-market-rebalancing-intensifies); [iTiger/Bloomberg](https://www.itiger.com/news/2466019752)
  - JPMorgan warned of "billions" sold into the close (headline only; fetch blocked). [S] — [Bloomberg Law](https://news.bloomberglaw.com/capital-markets/jpmorgan-says-levered-etfs-set-to-sell-billions-into-stock-close)
- 2026: daily LETF rebalancing flows are reported to have risen fourfold since the start of 2026, to a record $50B (Benzinga, July 2026). A social-media relay of a Morgan Stanley estimate puts one day's selling at about $52B, the "second largest since 2020." [S/U] — [Benzinga](https://www.benzinga.com/etfs/broad-u-s-equity-etfs/26/07/60264868/leveraged-etf-rebalancing-hits-50-billion-as-traders-warn-of-a-powerful-force-now-driving-us-market-volatility); [X post (U)](https://x.com/MelvinInvests/status/2118424339225686516)
- TQQQ AUM is reported above $32B in 2026, and the leveraged ETF segment at about $500B. [S] — [24/7 Wall St, July 2026](https://247wallst.com/investing/2026/07/13/an-absolute-casino-the-500-billion-leveraged-etf-craze-proving-buffett-right/)
- 2011 benchmark: about $1.04B per 1% move on $20.14B total LETF NAV (December 2011). [S] — [Elite Trader thread](https://elitetrader.com/et/threads/leveraged-etf-returns-rebalancing.379657/)
- Zhao (arXiv 2608.03703, August 2026) argues that speculators "preying on" LETF closing rebalances contributed to extreme volatility in Korea in 2026. The paper also argues that spreading the rebalance through the day may backfire. Abstract only; Korean market. [P, preprint] — [arXiv](https://arxiv.org/pdf/2608.03703)

### Inferences
- Size: the index-only flow of about $1–2.3B per 1% move (BofA) is small next to ES/NQ notional turnover. A 2% day implies about $2B of S&P 500 exposure and about $4.5B of Nasdaq-100 exposure, mostly executed by swap dealers at or into the MOC. The 2026 record ($50B/day) is dominated by single-stock LETFs (NVDA, TSLA and similar). Those flows hit single names and hit the index only through their weights.
- Ex-ante direction: deterministic. Timing: 15:30–16:00, concentrated in MOC.
- Decay: Barbon et al. explicitly report decline over time, and dealers now pre-hedge, which pulls the flow earlier in the afternoon and makes it less predictable in time. This is consistent with the program's finding that last-half-hour momentum is dead.
- Possible residual test: only on |r(09:30–15:30)| > 2% days, with the Nasdaq-100 LETF ratio to NQ liquidity rising in 2025–2026. That gives about 15–30 events per year (my estimate), too few for t > 3 unless the edge is more than 15 bp per event. The program's dead "big-r1 filter" test already probes this. Do not prioritize.
- Fits the 16:10 rule: yes. Evidence of a profitable effect after costs in ES: no.

### Gaps
- No 2025–2026 academic estimate of ES/NQ-level price impact per $1B of LETF flow.
- No paper separates index LETFs (SPXL/TQQQ/SQQQ/UPRO) from single-stock LETFs in impact terms.
- The JPMorgan and Morgan Stanley primary notes were not accessible.

---

## 3. Options expiration: monthly OpEx, quarterly triple witching, 0DTE pinning, dealer gamma

### Takeaway
Classic pinning (Ni, Pearson & Poteshman 2005; Golez & Jackwerth 2012) is real but small, and the samples are old (1996–2002, and earlier futures data). It is a volatility and mean-reversion effect toward the strike, not a directional drift. The most recent 0DTE evidence (Dim, Eraker & Vilkov; Adams et al. 2024–2025) shows market-maker 0DTE gamma is on average positive and dampens intraday volatility, and the hedging flows are tiny relative to ES liquidity. Popular "gamma squeeze" narratives are not supported. The one statistically credible conditional signal is the sign of aggregate dealer gamma (Baltussen et al. 2021; Barbon et al. 2022), which modulates end-of-day momentum versus reversal. It persists over time.

### Cited Findings
- Ni, Pearson & Poteshman (JFE 2005, vol. 78, pp. 49–87): optionable stocks' closing prices cluster at strikes on expiration dates, 1996–2002. Attributed to market-maker delta-hedge rebalancing and to manipulation by proprietary traders. Single stocks; old sample. [P] — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X05000577); [SSRN 519044](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=519044)
- Golez & Jackwerth (JFE 2012), "Pinning in the S&P 500 Futures": futures move toward the at-the-money strike on serial (non-quarterly) option expiration days. The reverse ("anti-cross-pinning") occurs just before index option expiration. The notional futures shift is at least $115M per expiration day, which is tiny. Pinning weakens when futures volatility is high. [P] — [SSRN 1664261](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1664261); [Konstanz PDF](https://kops.uni-konstanz.de/server/api/core/bitstreams/b9492112-cab3-4217-a7d0-d2c4f5ba7825/content)
- Dim, Eraker & Vilkov, "0DTEs: Trading, Gamma Risk and Volatility Propagation" (SSRN 4692190, 2024): no evidence that 0DTE open-interest gamma propagates or unconditionally raises index volatility. Market-maker net gamma is on average positive and negatively related to future intraday volatility. The evidence is consistent with delta hedging, not information-based trading. [P] — [SSRN 4692190](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190)
- Adams, Fontaine & Ornthanalai (SSRN 4881008, 2024; 2019–2023 data): index volatility is 60–90 annualized bp lower on days with 0DTE trading, using exogenous variation in expiration days. The dampening comes from market makers hedging positions opened in longer-dated options that have become 0DTE. [P] — [SSRN 4881008](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4881008)
- Adams, Dim, Eraker, Fontaine, Ornthanalai & Vilkov (SSRN 5641974, October 2025): 0DTEs dampen market volatility through a shift in market makers' hedging needs. [P] — [SSRN 5641974](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5641974); [Fontaine PDF](https://www.jean-sebastienfontaine.com/papers/0dte-options-volatility.pdf)
- Contrary evidence: Brogaard, Han & Won report the opposite sign (0DTE raises volatility). A Princeton thesis concludes that 0DTE activity relates to intraday volatility but does not support the canonical gamma-feedback mechanism. A blog re-analysis of 1,083 SPX sessions found no significant same-day effect. [P/U] — [Princeton thesis](https://theses-dissertations.princeton.edu/entities/publication/61115cd1-cb09-4a8b-9230-ff488fc2a386); [Dev.to re-analysis (U)](https://dev.to/firmtape/does-0dte-options-trading-raise-volatility-a-published-9-claim-measures-06-on-1083-spx-nni); [Cboe-hosted 0DTE paper](https://cdn.cboe.com/resources/education/research_publications/gammasqueezes.pdf)
- Cboe (via secondary): market-maker net 0DTE gamma hedging was about 0.04%–0.17% of daily ES liquidity in 2023 and no more than 0.2% on two of the busiest futures days of April 2025. On the selloff of 20 December 2023, market makers were mostly long gamma. [S, not verified at Cboe] — reported in search summaries; Cboe primary note not retrieved. Related Cboe-hosted paper: [gammasqueezes.pdf](https://cdn.cboe.com/resources/education/research_publications/gammasqueezes.pdf)
- Vilkov, "0DTE Trading Rules" (SSRN 4641356, December 2023): 0DTE options are about half of S&P 500 option volume. They carry a high variance risk premium, driven mainly by upside risk, which negatively predicts market returns. [P] — [SSRN 4641356](https://ssrn.com/abstract=4641356); [ResearchGate](https://www.researchgate.net/publication/376157104_0DTE_Trading_Rules)
- Baltussen, Da, Lammers & Martens (JFE 2021, more than 60 futures, 1974–2020): last-30-minute return is positively predicted by the rest-of-day return. For the S&P 500, intraday momentum is present on negative-net-gamma days, grows as gamma becomes more negative, and is insignificant on positive-gamma days. It reverts over subsequent days. [P] — [JFE via RePEc](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403); [Notre Dame PDF](https://www3.nd.edu/~zda/intramom.pdf); [Alpha Architect summary (S)](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/)
- Barbon et al. (2022): a large negative gamma imbalance relative to average dollar volume produces end-of-day momentum, and a positive one produces reversal. The gamma channel persists through the sample, unlike LETFs. [P] — [SFI](https://www.sfi.ch/en/publications/n-22-40-liquidity-provision-to-leveraged-etfs-and-equity-options-rebalancing-flows-evidence-from-end-of-day-stock-prices)
- Monthly OpEx week (Stivers & Sun, JBF 2013): S&P 100 stocks earn higher returns in the third-Friday week. An earlier WP version (1996–2008, 28 large caps) shows the following week averaging −0.03% versus +0.18% in other non-expiration weeks. The final paper highlights modest underperformance in the fourth-Friday week. Weekly horizon; old sample. [P] — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0378426613003051); [CXO Advisory (S)](https://www.cxoadvisory.com/calendar-effects/option-expiration-week-stock-return-drill-down/); [Quantpedia (S)](https://quantpedia.com/strategies/option-expiration-week-effect)
- Triple witching:
  - Stoll & Whaley (1984–1985 sample) found a last-hour price effect of about 0.4% on expirations, before settlement moved to the open. [P via S] — [Atlanta Fed Review (FRASER)](https://fraser.stlouisfed.org/files/docs/publications/frbatlreview/pages/67107_1985-1989.pdf)
  - Cboe: in 2009–2024 the SPX Special Opening Quotation (SOQ) fell outside the day's high-low range about 30% of the time, most often above the high. [S, Cboe via summary] — [summary source](https://squawkflow.com/learn/triple-witching-explained)
  - Recent day-of returns conflict: median −0.36% on triple-witching days with a 25% win rate (Robinhood, small sample) versus "no different from an ordinary day" over the 11 expirations from March 2024 to September 2026 (Proflex). [S] — [Robinhood](https://robinhood.com/us/en/learn/weekly-rundown/1r8IbNYWLg5b50RZa2IabZ/); [Proflex](https://proflexfinance.com/insights/triple-witching-explained); [Schaeffer's 2024](https://www.schaeffersresearch.com/content/analysis/2024/09/11/historic-market-performance-during-triple-witching-weeks)

### Inferences
- 0DTE pinning: the best current evidence says positive dealer gamma dampens volatility. That favors short-volatility, mean-reversion option structures, not directional ES trades. Hedging flows of about 0.2% or less of ES liquidity are too small to create a 2–3 bp directional drift.
- The gamma-sign conditioning of end-of-day momentum is the only option-flow effect that (a) persists in recent samples per Barbon et al., (b) occurs daily, giving high power, and (c) fits the 16:10 rule. It differs from the program's dead tests, which conditioned on r1 size, not on dealer gamma. Requirements: a daily, ex-ante estimate of SPX/SPY net dealer gamma (from OPRA open interest with a sign assumption, or vendor data, which is costly and model-dependent), and a test of 15:30–16:00 ES continuation on negative-gamma days only. The risk is that the gamma-conditional mean in the last 30 minutes is a few bp, near the 2–3 bp hurdle. Baltussen et al.'s sample ends in 2020, before the 0DTE regime shift, and post-2022 market-maker gamma has been mostly positive, which shrinks the number of negative-gamma days.
- Monthly OpEx (12 per year) and triple witching (4 per year): too few events for t > 3 in 7 years unless the edge is very large, and the recent triple-witching evidence shows no consistent effect. Classic OpEx-week effects are multi-day and need overnight holds, so they fail the rule.

### Gaps
- No peer-reviewed 0DTE paper reports a directional intraday ES return (in bp) conditional on strike proximity or gamma that clears costs.
- Cboe's primary 0DTE gamma-to-liquidity estimates were not retrieved directly.
- The "August 2026 SSRN paper" on market-maker gamma and intraday reversals cited by Stockwirex could not be identified or verified. [U] — [Stockwirex](https://stockwirex.com/?p=43323)

---

## 4. Futures quarterly roll and index rebalancing (S&P quarterly rebalance, Russell reconstitution, Nasdaq-100 annual and special rebalances)

### Takeaway
Rebalance events generate record closing-auction volume: about $334B in the Nasdaq closing cross alone on Russell day in June 2026. They are, however, mostly cross-sectional (buy adds, sell deletes), with little net index-level direction. Auction dislocations reverse overnight, and the events are too rare (1–4 per year each) for t > 3. The quarterly ES roll is a calendar-spread event, not an outright price event; no academic price-pressure study was found.

### Cited Findings
- Russell 2026 reconstitution: Nasdaq closing-cross record of 4,594,880,616 shares, or $334.027B, executed in about 1.6 s. In 2025 the figures were about $102.5B on Nasdaq and $114.7B on NYSE. [P, exchange] — [Nasdaq IR 2026](https://ir.nasdaq.com/news-releases/news-release-details/record-trading-volume-nasdaq-closing-cross-during-june-2026); [Nasdaq IR 2025](https://ir.nasdaq.com/news-releases/news-release-details/record-notional-value-shares-traded-nasdaq-closing-cross-0); [LSEG 2026 key facts](https://www.lseg.com/en/about-us/new-at-lseg/more-key-facts-ahead-of-the-2026-russell-us-indexes-reconstitution)
- Russell moved to a semi-annual reconstitution in 2026 (reported as "a $217B day"). [S] — [ECM Source](https://ecmsource.com/russell-2026-reconstitution-semi-annual-217-billion-day/)
- LSEG: there is "undoubtedly some market impact," but past short-term price impact on constituents "hasn't reliably followed such a pattern." Methodology changes, including the Nasdaq closing cross, have reduced the impact. [P, index provider] — [LSEG Impacts of Reconstitution 2025](https://www.lseg.com/content/dam/ftse-russell/en_us/documents/other/russell-indexes-impacts-of-reconstitution-2025.pdf)
- S&P 500 index effect: there is reversal evidence in older samples. A 2023 JBF paper finds permanent effects post-2000 for "true" additions and deletions. Bogousslavsky & Muravyev find little abnormal auction deviation on rebalance days relative to volume. [P] — [JBF 2023](https://www.sciencedirect.com/science/article/abs/pii/S0378426623001747); [Reading WP](https://centaur.reading.ac.uk/18666/1/18666.pdf); [Petajisto 2011](https://www.petajisto.net/papers/petajisto%202011%20jef%20-%20hidden%20cost%20for%20index%20funds.pdf)
- A blog event study of 450 S&P 500 additions (2000–2025) finds a mean abnormal return of −0.80% at T+5 (t = −3.38); in the 2020s, −0.94% at T+5 and −1.82% at T+21. Single stocks, multi-day, not peer reviewed. [U] — [TradingStudio](https://blog.tradingstudio.finance/sp500-additions-event-study/)
- ES roll: Quantitative Brokers defines the roll period as the 6 trading days before near-contract expiry and forecasts calendar-spread changes. The ESZ26 last trade date is 18 December 2026, with the customary roll date of 14 December 2026. [S] — [Quantitative Brokers](https://www.quantitativebrokers.com/all-forecasts/cme-e-mini-sp-500-futures-roll-forecast); [BBN Times](https://bbntimes.com/financial/s-p-500-futures-end-the-week-near-7-402-as-traders-brace-for-cpi)
- ETF Action reports $40B of US equity outflows on index-rebalancing activity, indicating creation/redemption effects. [S] — [ETF Action](http://www.etfaction.com/u-s-equities-shed-40b-on-index-rebalancing-activity-fixed-income-commodities-see-inflows/)

### Inferences
- For ES and NQ outright, rebalances are near zero-sum at the index level. Exceptions are a large net float change or a Nasdaq-100 special rebalance (cutting mega-cap weights), where NQ versus ES relative value might move, but the direction is not obviously predictable for the index. Events per year: S&P quarterly 4, Russell 2 (from 2026), Nasdaq-100 annual 1 plus ad hoc specials. Testable for t > 3: no.
- The roll affects the spread, not the outright price. A trader who is flat by 16:10 and trades the front month is unaffected apart from slightly thinner books in the expiring contract.
- Rule fit: the timing (closing auction) fits, but the documented reversal is overnight. Verdict: not tradable in ES/NQ under the program's constraints.

### Gaps
- No academic study of Nasdaq-100 special or annual reconstitution impact on NQ futures was found. (The July 2023 special rebalance was searched with no result.)
- No study of ES outright price pressure during roll week.

---

## 5. Month-end and quarter-end pension rebalancing

### Takeaway
There is robust academic evidence that predictable calendar rebalancing moves prices (Harvey, Mazzoleni & Melone, NBER 2025: about 16–17 bp lower equity returns the next day given a selling signal; about $16B per year cost to investors). There is also evidence of a pre-month-end "dash for cash" (Etula et al., data to 2013). The effect has a daily-to-multi-day horizon, so capturing it needs overnight holds. Twelve events per year give too little power for t > 3 at intraday scale. Goldman's quarter-end estimates ($23–33B in 2026) are large in dollars but small next to ES/SPX turnover.

### Cited Findings
- Harvey, Mazzoleni & Melone, "The Unintended Consequences of Rebalancing" (NBER w33554; SSRN 5122748, revised January 2026; AFA): calendar- and threshold-based institutional rebalancing has market-wide impact and creates predictable price patterns that others front-run. They report a 17 bp decrease in equity returns over the next day following a rebalancing-sell signal (one snippet gives about 16–17 bp; exact scenario unverified). Costs are about $16B per year for US investors. [P] — [NBER PDF](https://www.nber.org/system/files/working_papers/w33554/w33554.pdf); [SSRN 5122748](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5122748); [AFA](https://afajof.org/management/viewp.php?n=144452); [FT, April 2025 (S)](https://people.duke.edu/~charvey/Media/2025/FT_April_2_2025.pdf); [Ohio State news](https://fisher.osu.edu/news/portfolio-rebalancing-and-its-unintended-consequences)
- An independent replication with S&P 500 and 10-year Treasury futures tests whether a negative month-end signal predicts a widening equity-bond spread the next day. [S] — [QuantReturns](https://quantreturns.com/strategy-review/front-running-the-rebalancers/); [Substack](https://quantreturns.substack.com/p/front-running-the-rebalancers)
- Etula, Rinne, Suominen & Vaittinen, "Dash for Cash" (WP 2015; later RFS 2020): pension-related month-end selling depresses prices before the turn of the month, followed by a rebound. Costs to US pensions are about $700M per year. The effect was strongest in 2007–2009 and persisted to 2013, the end of the data. [P via S] — [idw-online](https://idw-online.de/en/news633963); [ScienceDaily](https://sciencedaily.com/releases/2015/06/150630100702.htm)
- Graziani (job-market paper, November 2024): end-of-month S&P 500 returns negatively predict next-month returns, attributed to pension payments. [P, WP] — [CSEF PDF](https://csef.it/wp-content/uploads/JMP_GG_02Nov2024.pdf)
- An Aalto thesis finds pre-month-end effects grow with pension ownership. [P, thesis] — [Aalto](https://aaltodoc.aalto.fi/items/00fea0ae-963b-444c-8221-912121905b98)
- Goldman Sachs desk estimates of US pension equity rebalancing [S]:
  - About $33B of selling around end-September 2026, which Goldman puts in the 98th percentile since 2000. [S] — [roic.ai](https://www.roic.ai/news/goldman-sachs-warns-of-33-billion-pension-fund-equity-sell-off-as-quarter-end-looms-09-30-2026); [KSL/Reuters](https://www.ksl.com/article/51630948/bond-selloff-could-mean-outsized-portfolio-changes-at-quarters-end)
  - About $23B month-end selling in April 2026. [S] — [Longport/Wallstreetcn](https://longportapp.cn/news/283884283)
  - $32B for Q1 2024. [S] — [Bloomberg](https://www.bloomberg.com/news/articles/2024-03-27/pension-funds-seen-selling-32-billion-of-stock-into-quarter-end)
  - $76B in June 2020. [S] — [CNBC](https://www.cnbc.com/2020/06/23/theres-a-wave-of-selling-estimated-to-be-in-the-billions-thats-about-to-hit-the-stock-market.html)
  - Month-end flow primer. [S] — [Tickmill/GS](https://www.tickmill.com/blog/institutional-insights-goldman-sachs-month-end-rebalancing-flows-to-know)

### Inferences
- Direction is predictable ex ante from the month-to-date stock-versus-bond return spread. Timing is the last 1–3 trading days, with execution often at the closes (including MOC). The effect lands mostly on the next-day return, so capturing it requires an overnight position, which violates the rule.
- An intraday-only version (for example, short ES 15:00–16:00 on the last trading day when the signal says "sell equities") is untested in the literature I found. With 12 events per year (about 84 in 7 years), it needs mean/sd ≥ 0.33. If the last-hour sd is about 30–40 bp (my assumption), the effect must be about 10–13 bp per event, against roughly 2–3 bp of hurdle. That is implausible given that the full documented next-day effect is about 17 bp.
- Decay: the Etula et al. data end in 2013. Harvey et al.'s publicity (FT 2025) may accelerate front-running and arbitrage away the effect.

### Gaps
- No intraday decomposition (which hour of the last day) of the month-end rebalancing effect was found.
- Exact HMM tables (per-signal-decile bp, futures vs cash, post-2015 subsample) were not retrievable because the hosts were blocked.

---

## 6. CTA/trend-follower triggers and vol-control fund flows: any empirical intraday evidence?

### Takeaway
I found no peer-reviewed or exchange study measuring the intraday price impact of CTA or vol-control rebalancing in ES. Evidence is limited to sell-side flow models (Goldman, Nomura and others, via press and blogs) and index-provider methodology. The narrative is common; the empirical support is absent.

### Cited Findings
- S&P DJI vol-control indices on ES futures rebalance intraday, some up to 13 times per day using TWAP. This mechanism spreads flow and reduces any single-time impact. [P, methodology] — [S&P 500 Dynamic Intraday TCA methodology](https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-500-dynamic-intraday-TCA-index.pdf); [S&P 500 Futures 10% Vol Intraday Target](https://www.spglobal.com/spdji/en/indices/multi-asset/sp-500-futures-10-volatility-intraday-target-long-tca-index/)
- Sell-side estimates (unverified models): a 3% S&P 500 decline could trigger about $100B of CTA selling (Goldman-attributed); about $1.1B per 1% move from S&P-linked products. [S/U] — [AllWeatherFinance](https://allweatherfinance.com/u-s-stock-cta-buying-drops-sharply-a-3-decline-in-the-s-p-500-could-trigger-a-100-billion-selling-wave/); [Tickmill/GS positioning](https://www.tickmill.com/blog/institutional-insights-goldman-sachs-sp500-positioning-levels-update-10911)
- The Convex glossary's vol-control size of $300–500B and 8–9% vol thresholds are unsourced. [U] — [Convex](https://convextrade.com/glossary/volatility-control-rebalancing-flow)
- Adjacent academic evidence:
  - Bank of England: VIX ETP flows mostly do not spill over to the S&P 500. [P] — [Bank Underground 2018](https://bankunderground.co.uk/2018/04/24/is-the-tail-wagging-the-dog-the-impact-of-vix-exchange-traded-products-on-equity-volatility/)
  - CFTC: asset managers' long-volatility bias pushes up VIX futures. [P] — [CFTC OCE](https://www.cftc.gov/idc/groups/public/@economicanalysis/documents/file/oce_volderivatives.pdf)
  - SUERF: of the ETF rebalancing components, leverage rebalancing has the largest price effect. [P] — [SUERF policy note](https://www.suerf.org/wp-content/uploads/2023/12/f_aaa5ebec57257fa776a1990c2bd025c1_11687_suerf.pdf)
  - The February 2018 "Volmageddon" account. [S] — [CNBC 2018](https://www.cnbc.com/2018/02/07/volatility-trades-had-out-sized-influence-on-the-markets-free-fall.html)

### Inferences
- CTA trigger levels are model-dependent (lookbacks, vol scaling differ by fund) and not observable ex ante. The timing is not exact: execution is typically spread across the session or near the close. Direction is predictable only conditionally ("if price crosses X"), and those crossings coincide with momentum days the program has already tested.
- Vol-control flows are tied to realized vol (lagged), so they are predictable in direction after volatility spikes. The flow is spread over days, with no exact clock time.
- Verdict: no empirical basis to build a 3×-cost intraday ES strategy.

### Gaps
- No academic paper quantifies vol-target or CTA impact in bp on ES at intraday horizons. Moreira & Muir (2017) and related work study the strategy's returns, not its price impact.

---

## 7. Buyback blackouts, Treasury refunding, the 09:30 cash open and the 11:30 ET European close as liquidity events

### Takeaway
None of these has empirical support as an intraday directional effect in ES/NQ. A controlled buyback-blackout test found no significant effect. Treasury refunding research covers bond returns only. Index-futures return seasonality concentrates around the European open overnight (Bondarenko & Muravyev 2023; NY Fed overnight drift), not at 09:30 or 11:30 ET. That window is outside the rule and already tested dead after costs in the program.

### Cited Findings
- Buyback blackout:
  - Alpha Architect: no significant return difference for the highest-buyback S&P 500 quintile during blackout periods, versus an equal-weighted index (sample pre-2019). [S, practitioner research] — [Alpha Architect](https://alphaarchitect.com/buyback-blackout-periods-do-not-negatively-impact-market-performance/)
  - Deutsche Bank and others say more than 80% of S&P 500 firms are in blackout during peak weeks, but this is narrative and untested. [S] — [BNN Bloomberg](https://ampvideo.bnnbloomberg.ca/s-p-500-is-heading-for-a-rough-patch-as-buyback-blackouts-arrive-1.2058097); [RIA (advocacy)](https://realinvestmentadvice.com/resources/blog/blackout-of-buybacks-threatens-bullish-run/)
- Treasury refunding: Wang & Zhao find positive long-term Treasury returns on the day before Treasury Refunding Announcements, persistent since the 1990s. Bonds, not equities. [P, WP] — [EconPapers](https://econpapers.repec.org/RePEc:osf:socarx:xucf8)
- Equity effects of refunding: anecdotal only, for example the yield spikes on surprise coupon guidance in 2025, and Wells Fargo did not expect "fireworks" from the May refunding. [S] — [FXStreet](https://www.fxstreet.com/analysis/treasury-refunding-preview-taking-a-breather-202404221415)
- Bondarenko & Muravyev (JFQA 2023, "Market Return Around the Clock"): on E-mini futures, the 4 hours around the European open account for the entire average market return, with a Sharpe ratio of 1.67 over 2004–2018. Attributed to uncertainty resolution. Overnight window. [P] — [JFQA](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/market-return-around-the-clock-a-puzzle/089E33AC0B4D3B9A02CBA31EDF6505B3); [Alpha Architect (S)](https://alphaarchitect.com/market-return-around-the-clock/)
- NY Fed (Boyarchenko, Larsen & Whelan): the largest positive returns accrued 2–3 a.m. ET in 1998–2019. This is the program's already-dead overnight drift. [P] — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf)
- Intraday volatility is higher in the first and last hours of US trading (U-shape). US–Europe return correlation is strongest at European opening and closing hours and drops sharply between 13:00 and 13:30 CET (Innocenti et al. 2011). Volatility and co-movement findings, not drift. [P] — [Monash WP](https://ageconsearch.umn.edu/record/267773/files/monash-209.pdf)
- Bogousslavsky (JFE 2021): arbitrageurs cut mispricing positions before the close because of overnight margin and lending costs. This explains end-of-day cross-sectional return patterns. Heston, Korajczyk & Sadka (2010) find half-hour-interval return continuation at 24-hour multiples in the cross-section. [P] — [EconPapers Bogousslavsky](https://econpapers.repec.org/article/eeejfinec/v_3a141_3ay_3a2021_3ai_3a1_3ap_3a172-194.htm); [Springer, clientele and intraday patterns](https://link.springer.com/article/10.1007/s11156-024-01319-8)

### Inferences
- The 09:30 open and the 11:30 ET European close are liquidity and volatility events with no documented, ex-ante-signed drift at index level. Their cross-sectional half-hour periodicity (Heston, Korajczyk & Sadka) is a single-stock effect, not an index effect.
- Buyback blackouts are multi-week regimes with no intraday clock time; Treasury refunding (8 events per year counting announcement and auction) has no equity-intraday evidence. Neither reaches t > 3 within the rule.

### Gaps
- No academic study of ES/NQ returns specifically in windows around 11:30 ET (European cash close).
- No study of equity-futures intraday response to 10-year or 30-year refunding auctions (13:00 ET) was found in this session. Lou, Yan & Zhang (RFS 2013) on Treasury auction price pressure was searched but not retrieved, so it is not reported here.

---

## 8. Rule fit ("flat by 16:10 ET, no overnight") and verdict per flow

### Takeaway
Only intraday, daily-frequency flows have both the timing and the statistical power the program needs, and the main candidate (LETF/MOC end-of-day momentum) is the one already found dead. The one structural signal with persistent, recent academic support and daily frequency is dealer-gamma conditioning of the end-of-day move (Baltussen et al. 2021; Barbon et al. 2022). Everything else is either overnight-dependent, too infrequent, or unsupported empirically.

### Cited Findings
- LETF effect decays over time; gamma effect persists; both revert at the next open. — [SFI/Barbon et al.](https://www.sfi.ch/en/publications/n-22-40-liquidity-provision-to-leveraged-etfs-and-equity-options-rebalancing-flows-evidence-from-end-of-day-stock-prices)
- Intraday momentum is concentrated on negative-gamma days. — [Baltussen et al. JFE 2021](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403)
- 0DTE market-maker gamma is positive on average and dampens intraday volatility. — [SSRN 4692190](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190); [SSRN 4881008](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4881008)
- Auction dislocations reverse overnight. — [Bogousslavsky & Muravyev](https://www.sciencedirect.com/science/article/abs/pii/S1386418123000502)
- The month-end rebalancing effect is about 17 bp next day. — [NBER w33554](https://www.nber.org/system/files/working_papers/w33554/w33554.pdf)

### Inferences
Summary table. Effect sizes are as documented; "n/yr" is my count; "3×cost?" and "t>3 in 7y?" are my judgments using the power arithmetic at the top.

| Flow | Timing | Typical size | Documented impact | Direction ex ante | Decay | 16:10 rule | 3×cost? | t>3 in 7y? |
|---|---|---|---|---|---|---|---|---|
| MOC imbalance (index-aggregate) | 15:50–16:00 | Auction tens of $B per day; $100–330B on recon days | Auction-vs-midpoint deviations, reversed overnight; weak large-cap price-discovery evidence | Yes (sign published) | n/a | Fits, but reversal is overnight | Unknown, likely no | Testable (daily) but weak prior |
| LETF rebalance | 15:30–16:00 / MOC | ~$1B (SPX) and ~$2.2B (NDX) per 1%; 2026 records $50B/day (mostly single-stock) | Negligible (Ivanov & Lenkey) to modest and decaying (Barbon) | Yes | Decaying | Fits | No (program tested, dead) | n/a (dead) |
| Dealer-gamma-conditioned end-of-day momentum | 15:30–16:00 | Gamma ~$bn per 1%; 0DTE hedges ≤0.2% of ES liquidity | Momentum on negative-gamma days, none or reversal on positive (Baltussen; Barbon) | Conditional on gamma estimate | Persists to 2020 (Barbon); post-0DTE regime unclear | Fits | Unknown; the only open candidate | Possibly (daily) |
| 0DTE pinning | Expiry day, afternoon | ≥$115M futures notional per expiry (old) | Pull toward ATM strike (old samples); volatility dampening (new) | Toward strike, not up/down | n/a | Fits | Unlikely in futures | Unclear |
| Monthly OpEx / triple witching | 3rd Friday; quarterly | — | ~0.4% last hour in 1984–85; recent: no consistent effect | No | Largely gone | Partly (multi-day effects don't fit) | No | No (12 or 4 per yr) |
| Index rebalances / Russell recon | Close on rebalance day | $100–334B auction volume | Single-stock; index-level near zero; overnight reversal | No (index level) | Reduced by methodology changes | Overnight reversal | No | No (1–4 per yr) |
| ES quarterly roll | 8 days before expiry | Spread, not outright | No study found | n/a | n/a | n/a | n/a | No |
| Month/quarter-end pension rebalancing | Last 1–3 days; often MOC | $20–35B per quarter (GS) | ~17 bp next day (HMM); pre-month-end dip (Etula, to 2013) | Yes (stock/bond spread) | Possibly arbitraged post-publication | No (needs overnight) | Intraday version unknown | No (12 per yr) |
| CTA / vol-control | Spread; often near close | $1–100B (sell-side models) | No empirical intraday evidence | Conditional | n/a | Fits | Unknown | Unknown |
| Buyback blackout | Weeks around earnings | — | Null (Alpha Architect) | Weak | n/a | No clock time | No | No |
| Treasury refunding | Quarterly announcement; auctions 13:00 | — | Bonds only | No | n/a | Fits | No evidence | No |
| 09:30 open; 11:30 European close | Daily | — | Volatility and correlation events, no drift | No | n/a | Fits | No evidence | n/a |

- Recommended next test, if any: daily 15:30 (or 15:50)–16:00 ES/NQ return conditioned on the ex-ante sign and magnitude of aggregate SPX dealer gamma, plus the published 15:50 imbalance sign. Restrict to 2022–2026 to capture the 0DTE regime, and require an out-of-sample hold-out. Expect a small edge, and be suspicious of data-mined gamma definitions.

### Gaps
- No full-text verification of effect sizes for Barbon et al., Harvey et al., Cushing & Madhavan, or Cboe's 0DTE notes (host access blocked in this session: ssrn.com, edhec.edu, bloomberglaw.com).
- No sourced figure for the standard deviation of ES 15:50–16:00 returns; the power arithmetic uses my own approximation.
