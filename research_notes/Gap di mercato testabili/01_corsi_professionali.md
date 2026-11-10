# Professional / semi-professional intraday trading curricula: falsifiable claims about ES/NQ intraday behavior

Scope: ES/NQ (or SPY/QQQ) intraday, minutes-to-hours horizon, retail latency, flat by 16:10 ET. Costs per round trip: ES 0.33 pt, NQ 0.45 pt.
Research date: 2026-11-10.

**How to read this file**
- [VERIFIED-SOURCE] means a source fetched or seen in search snippets during this session says this.
- [UNVERIFIED-MEMORY] means it comes from prior knowledge of the books and was NOT re-checked against the primary text in this session. Check it against the book before building a test on it.
- [MARKETING] means a vendor, educator or indicator-seller page. [SECONDARY] means a quant blog or aggregator. [ACADEMIC] means peer-reviewed or a working paper.

**Network limits in this session.** These hosts failed DNS (blocked by the session's allowlist): nexusfi.com, mql5.com, oxfordstrat.com, cxoadvisory.com, concretumgroup.com. Their content below comes only from search-result snippets, not full pages. To read the full NexusFi 80%-rule test, the mql5 ORB replication, the Oxford Strat Turtle Soup/NR7 results and the CXO summaries, those hosts must be allowed in the session's network settings.

**Rough cost scale (an assumption, not a sourced fact).**
- ES at roughly 6,000–7,000 with an average daily range near 1% gives about 60–70 pt per day. A typical first-hour initial balance (IB) is then about 25–35 pt.
- So 0.33 pt is about 1–1.5% of a typical IB, or 3.3% of a 10-pt stop (1R).
- NQ: 0.45 pt is negligible against a daily range of about 250–350 pt. A 40-pt stop gives a cost near 0.011R.
- Implication: commissions are not what kills IB- or day-scale setups on these contracts. What kills them is the lack of a gross edge, plus stop slippage on fast breaks.
- A setup needs gross expectancy above about 0.03–0.05R per trade on ES (less on NQ) to survive costs at IB-scale stops. Scalps with 2–4 pt targets on ES are where costs bite (8–16% of the target).

---

## 1. Market Profile / Auction Market Theory (Steidlmayer; Dalton, *Mind Over Markets* 1990/2013, *Markets in Profile* 2007)

### Takeaway
Market Profile makes many qualitative, structural claims: value area, IB, open types, poor highs/lows, single prints, day types. Only two come with numbers that can be pinned down, the "80% rule" and the IB/normal-day range proportions. No peer-reviewed or academic test of any Market Profile claim turned up. Third-party ES statistics exist only in forum posts and indicator dashboards. Those that exist show the 80% figure collapsing under strict definitions and IB "break" frequencies that say nothing about payoff.

### Cited Findings
**Origin and framework**
- Auction market theory is attributed to J. Peter Steidlmayer (CBOT, 1980s) and expanded by Jim Dalton in *Mind Over Markets*. [SECONDARY] — [TradingView AMT explainer](https://br.tradingview.com/chart/BTCUSDT/dvElFPVS-Auction-Market-Theory)
- Value area (VA) is defined as about 68–70% of TPOs (time-price opportunities) or volume around the POC (point of control), justified by a "one standard deviation" Gaussian analogy. Sources disagree (68% vs 70%), and the Gaussian framing is an assumption, not a tested result. — [TradingView AMT](https://br.tradingview.com/chart/BTCUSDT/dvElFPVS-Auction-Market-Theory); [Traders' (S&C) 2009 Alexander](https://traders.com/Documentation/FEEDbk_docs/2009/11/Alexander.html)
- Core behavioral claim: when price moves outside value it "is likely" to return to the value area. No test of this was found. [MARKETING/practitioner] — same sources

**The 80% rule** (the most-quantified Market Profile claim)
- Rule: the session opens outside the prior day's VA, then re-enters it and is accepted there for two consecutive 30-minute TPO periods. The claim is then an 80% chance of traversing to the opposite side of the VA.
- The rule is usually traced to Dalton's *Profile Reports* (1987–91) and *Mind Over Markets*. Definitions of "acceptance" vary across vendors: one TPO vs two, close vs touch. — [LuxAlgo 80% Rule](https://www.luxalgo.com/library/concept/80-percent-rule.md); [marketcalls](https://www.marketcalls.in/market-profile/market-profile-how-to-play-80-percentage-rule.html); [teamlbr 2008 blog citing MoM p.280](https://teamlbr.blogspot.com/2008/09/mp-value-area-rule-80-rule.html)
- Independent check: a NexusFi article (search snippet only; host blocked) states that "the 80% figure dissolves under rigorous testing." Under strict criteria the rule "triggers on a small handful of days per year on ES." The methodology could not be read. — [NexusFi 80% rule](https://nexusfi.com/a/concepts/80-percent-rule)
- The 80% figure is repeated in promotional posts with no test. [MARKETING] — [Substack note](https://substack.com/@ryanbaileyedge/note/c-198868765)
- An open-source TradingView "80 Rule Backtest" script exists. Its results were not retrieved. — [TradingView 80 Rule Backtest](https://my.tradingview.com/script/rsTzArCv-80-Rule-Backtest)

**Initial balance (IB) statistics** (third-party, ES)
- Self-reported dashboard, ES, Aug 2015–Aug 2025, 2,577 days. Methodology not disclosed. [MARKETING/unverified]
  - IB high broken on 67.1% of days, IB low on 72.4%, both sides on 40.1%.
  - If the IB closes above its midpoint, an upside break follows 83.5% of the time.
  - A 25% IB extension is hit 85.3% of the time and a 50% extension 69.5%, apparently conditional on a break.
  - Source: [Initial Balance Dashboard](https://trevor-trades.vercel.app/analysis)
- Reddit r/FuturesTrading (2024): over three years ES broke only one side of the IB about 70% of the time. A commenter notes that a 1:1 breakout trade still loses more than 50%. This conflicts with the dashboard, which implies about 59% one-side-only. — [Reddit thread mirror](https://lr.eu.psf.lt/r/FuturesTrading/comments/1bycosx/this_is_how_ess_price_moves_70_of_the_time)
- NQ IB extension percentiles, with a median extension of +0.31% beyond the IB high when broken. The author warns the numbers do not transfer to ES. — [TradingView IB Statistical Mapping](https://www.tradingview.com/script/2iuvi66N-Initial-Balance-Statistical-Mapping/)

**Open types (Dalton)**
- The four types, as chapter structure in *Mind Over Markets*: Open-Drive, Open-Test-Drive, Open-Rejection-Reverse, and Open-Auction (in or out of range).
- Claim: Open-Drive and Open-Test-Drive signal high conviction and should be traded in the drive direction. Open-Auction signals low conviction and rotation.
- Practitioners cannot reliably tell Open-Test-Drive from Open-Rejection-Reverse, so the categories are hard to operationalize.
- Sources: [LuxAlgo Open Types](https://www.luxalgo.com/library/concept/open-types/); [readingthemarkets 2009 review](https://readingthemarkets.blogspot.com/2009/10/dalton-jones-mind-over-markets.html); [leveltrading blog quoting MoM p.267](https://leveltrading.blogspot.com/2014/03/opening-types-pg267-open-drive-if.html); [O'Reilly MoM index](https://www.oreilly.com/library/view/mind-over-markets/9781118659762/index.html)

**Poor highs/lows and single prints**
- Poor high/low: a flat extreme with two or more TPOs at the same price and no single-print tail. It is "unfinished business" that "may be revisited." Single prints are "often price magnets" that get "filled."
- All claims are qualitative. No revisit-rate statistics were found. — [LuxAlgo poor high/low](https://www.luxalgo.com/library/concept/poor-high-poor-low.md); [NexusFi single prints/poor highs](https://nexusfi.com/a/market-structure/single-prints-poor-highs-poor-lows-market-profile)

**Academic coverage**
- A search for academic or empirical tests of value area or AMT returned only practitioner material. — searched; see the [NexusFi AMT page](https://nexusfi.com/a/market-structure/auction-theory-futures-trading) as an example of what comes up.

**[UNVERIFIED-MEMORY] Day types**
- Steidlmayer/Dalton day types: Normal, Normal Variation, Trend, Double-Distribution Trend, Neutral, Non-Trend.
- Normal day: the IB (first hour) contains roughly 85% of the day's range. Normal variation: range extension up to about 2x IB. Trend day: open near one extreme, close near the other, with repeated range extension.
- The "85% of range" figure dates from the pit era, when floor locals dominated. Electronic ES with an 18:00–17:00 Globex session and a different IB definition (RTH 09:30–10:30) likely changes it materially. No modern test was found.

### Inferences
**Effect size vs costs, first estimate**
- 80% rule:
  - If the strict version fires only about 3–10 times per year on ES (per NexusFi), it is untestable at useful statistical power. Ten years gives fewer than 100 events.
  - Looser versions (one TPO of acceptance) fire much more often. They are probably close to "price inside yesterday's VA mean-reverts to the opposite VA edge," which overlaps with the dead PDH/PDL and VWAP-magnet tests.
  - Payoff: target = VA width, about 15–30 pt on ES; stop = re-exit of the VA, about 5–10 pt. Costs are about 2–5% of R, small.
  - Verdict: testable but low-frequency. Prior expectation is weak, given the NexusFi snippet.
- IB break and extension:
  - "IB breaks 67–72%" is a statement about range, not about direction. Most days extend the range on some side by construction.
  - The tradeable claim is the conditional one: "IB close above mid → 83.5% upside break." But conditional break frequency, without the adverse excursion, says nothing about expectancy.
  - First estimate: the edge is unknown and likely small. It is cheap to test from 1-minute data.
- Single prints / poor highs:
  - These are the most promising "materially different" variant relative to the dead PDH/PDL test. The level is defined by profile shape (flat extreme, no tail), not just the price extreme.
  - Test: for prior-day RTH extremes classified poor vs not poor, compare next-session revisit probability and the post-revisit reaction (break vs sweep).
  - If poor extremes are revisited much more often than clean ones, but behave identically after the touch, there is no tradeable gap. That is a likely outcome, given the PDH/PDL result.
- Open types:
  - Operationalizable as follows: Open-Drive = no trade back through the 09:30 open within N minutes after a move of k × ATR(open-to-extreme).
  - This overlaps heavily with the dead 5-minute ORB and the gap tests. A materially different variant would be "Open-Drive + open outside prior VA + no return to the open in the first 30 minutes → hold to 15:55." That is closer to a trend-day classifier and needs a fresh test.

### Gaps
- Exact Dalton wording and any numbers in *Mind Over Markets* (2013 edition) for the 80% rule, open-type follow-through and the IB proportion were not read in this session (no primary text access).
- The NexusFi 80%-rule test methodology and its numbers were not readable (host blocked).
- No academic paper testing value-area mean reversion, IB extension or poor-extreme revisits on ES/NQ was found.

---

## 2. Al Brooks price action (*Trading Price Action: Trends / Trading Ranges / Reversals*, Wiley 2012; *Reading Price Charts Bar by Bar* 2009; Brooks Trading Course)

### Takeaway
Brooks gives many explicit probabilities ("60% measured move," "80% of trading-range breakouts fail," "75% of channel breakouts fail"). By his own framing, these are discretionary estimates, not backtested statistics. No independent systematic test of his setups (H2/L2, first pullback, measured move) turned up. His own community argues that naive backtests are invalid because context (with-trend vs countertrend) is discretionary. That makes most claims hard to falsify unless they are re-defined mechanically.

### Cited Findings
**The trader's equation**
- Probability × reward must exceed (1 − probability) × risk. At a 60% win rate the reward must be at least equal to the stop. Setups with no more than 40% probability (most reversals) need about 2:1 reward-to-risk. — [MoneyShow interview transcript](https://moneyshow.com/articles/videotranstr-26221); [Brooks forum](https://www.brookstradingcourse.com/support-forum/general-trading-discussion/traders-equation-can-a-11-trade-have-higher-success-rate-than-60/)

**Specific claimed probabilities** (secondhand; conflicting)
- After a strong breakout there is about a 60% chance of a measured move equal to the breakout height. Forum paraphrase; members dispute it. — [Brooks forum: BO 60% MM](https://www.brookstradingcourse.com/support-forum/41-trading-breakouts/bo-has-60-probability-of-reaching-mm-target-but-is-it-really/); [Brooks forum: measured move](https://www.brookstradingcourse.com/support-forum/general-trading-discussion/measued-move/)
- About 75% of bull breakouts above a bull channel fail within about 5 bars. [user flashcards] — [Brainscape deck](https://api.brainscape.com/flashcards/38-20716854/packs/23133273)
- "Most breakout attempts during a trading range fail (80%)." [forum] — same search; see the [Brooks forum](https://www.brookstradingcourse.com/support-forum/general-trading-discussion/probability-and-riskreward/)
- Another deck gives a "40% chance it will fail and reverse." The figures conflict. — [Brainscape deck](https://api.brainscape.com/flashcards/30-20716624/packs/23133273)

**H2/L2 (second entry)**
- The first attempt to resume a trend often fails, so the second attempt (H2 in a bull trend, L2 in a bear trend) is the better entry. — [LuxAlgo bar counting](https://www.luxalgo.com/library/concept/bar-counting-h1-h2/)
- Brooks-community caution: backtesting "H2 at the EMA" blindly mixes with-trend and countertrend cases, so the results "will be wrong." — [Brooks forum: backtesting software](https://www.brookstradingcourse.com/support-forum/general-trading-discussion/backtesting-software/)
- TradingView "Al Brooks Second Entry" scripts exist but show no out-of-sample statistics. — [TradingView script](https://www.tradingview.com/script/YUixSlPL-Al-Brooks-Second-Entry/)

**[UNVERIFIED-MEMORY] Other recurring Brooks claims** (verify page numbers)
- About 80% of attempts to reverse a strong trend fail. The first reversal is usually followed by a test of the extreme ("lower high / higher low major trend reversal" needs a second leg).
- About 80% of attempts to break out of a trading range fail.
- The market is in a trading range about 70–80% of the time.
- "Always in" direction. The first 1–2 hours often set the day's high or low. A strong trend from the open gives about a 70%+ chance the trend extends.
- He uses 5-minute ES as his main chart.

### Inferences
- Mechanizable and falsifiable on 5-minute ES/NQ RTH:
  - (a) "Trading-range breakout failure ≈ 80%." Define the range as N bars with a high–low span under k × ATR. Define failure as a return inside the range within 5 bars. This is a frequency claim, so test the failure rate first, then the fade trade.
  - (b) "Strong breakout → 60% measured move before the stop." Define "strong" as 3 or more consecutive trend bars closing near their extremes with a combined size of at least x × ATR.
  - (c) "First pullback (H1/L1) in a strong trend underperforms the second (H2/L2)." Compare the two directly on the same trend days.
- Effect size vs costs:
  - These are 5-minute setups with ES stops of about 3–8 pt, so costs are 4–11% of R. That is the cost-sensitive zone.
  - A 60% win rate at 1:1 gives gross 0.2R and net about 0.1–0.15R on ES. That survives costs if the 60% figure were true.
  - But a strict 60% at 1:1 is a strong claim that, if true, would be well arbitraged. The prior is that true rates are near 50% after defining terms.
- Overlap with dead tests:
  - The dead 5-minute FVG with a 2R target is structurally similar to Brooks' "gap" bars.
  - The fade of "trading-range breakout failure" partly overlaps the dead PDH/PDL sweep test, but at intraday ranges rather than prior-day levels. That makes it a materially different variant.
- Marketing risk: the probabilities are ex-cathedra estimates from a discretionary trader selling a course. There is survivorship bias in who gets quoted, and no audited track record was found.

### Gaps
- No primary-text verification of the exact percentages and page numbers in the trilogy.
- No independent systematic backtest of any Brooks claim on ES/NQ with out-of-sample testing was found.

---

## 3. Order-flow education (Jigsaw Trading / Peter Davies; Axia Futures; Trader Dale; volume profile)

### Takeaway
Order-flow courses teach absorption (passive liquidity holding against aggressive flow, often icebergs), delta divergence, initiative vs responsive activity, and HVN/LVN behavior ("price rotates at HVN, moves fast through LVN"). These claims are qualitative and come from vendors that sell platforms. Academic microstructure research confirms that order-flow imbalance (OFI) drives contemporaneous price changes. Its predictive power decays within about a second on the E-mini and within minutes in equities. That sits below retail latency, so the order-flow "edge" taught to retail is largely unverified, at least at minutes-to-hours horizons.

### Cited Findings
**Jigsaw / Peter Davies**
- Absorption, meaning firm offers holding against continued buying (often icebergs), is taught as a key reversal component, with a check of the opposite side of the book for spoofing. [MARKETING] — [Jigsaw deck Pt2](https://jigsawtrading.com/wp-content/uploads/2014/03/PracticalApplicationOfOrderFlow-Pt2.pdf)
- "Delta can keep rising while price stalls" is presented as a signal for confirming levels. [MARKETING] — [Jigsaw: Confirming Levels](https://www.jigsawtrading.com/wp-content/uploads/2013/11/ConfirmingLevelsWithOrderFlow.pdf)
- Platform pages list iceberg and absorption detection as features. Vendor claim. — [AMP Futures Jigsaw page](https://www.ampfutures.com/trading-platform/jigsaw-trading?hsLang=en)
- Users questioned the claimed Level 2 backtesting capability. No independent verification of an edge was found. — [NexusFi AMA thread](https://nexusfi.com/showthread.php?p=309844)

**HVN/LVN (Trader Dale, Jigsaw)**
- Price rotates around HVNs and moves faster through LVNs, but "an LVN may not actually stop price." [MARKETING] — [Jigsaw blog](https://www.jigsawtrading.com/?p=39122)
- Trader Dale's *Volume Profile: The Insider's Guide to Trading* covers POC, HVN and LVN. No backtest was published. — [9Natree summary](https://9natree.castos.com/episodes/review-volume-profile-the-insiders-guide-to-trading-trader-dale-summarized)

**Academic microstructure**
- Cont, Kukanov & Stoikov: price changes over short intervals are mainly driven by OFI at the best bid/ask, with a near-linear relation (contemporaneous). [ACADEMIC] — cited via [Cross-impact of OFI, arXiv 2112.13213](https://arxiv.org/html/2112.13213v4)
- Cont, Cucuringu & Zhang: cross-impact terms forecast returns up to several minutes ahead, but "predictability decays quickly." Equities, not futures. [ACADEMIC] — [arXiv 2112.13213](https://arxiv.org/html/2112.13213v4)
- S&P 500 E-mini, one-second BBO data: price and flow impacts are significant at one second, and impulse responses "dissipate almost entirely within a second." Macro announcements reshape the dynamics. [ACADEMIC, working paper] — [arXiv 2508.06788](https://arxiv.org/abs/2508.06788v4)
- SPY: short-horizon efficiency is only partially restored after order-flow shocks. This is a lag-resolved anomaly that does not show in unconditional returns. [ACADEMIC, preprint] — search result [arXiv 2511.06177](https://arxiv.org/pdf/2511.06177v1)

### Inferences
- **Effect size vs costs:** the documented OFI predictability on the E-mini lives at sub-second horizons. At 0.33 pt per ES round trip (1.3 ticks), any absorption scalp targeting 2–4 ticks loses 33–66% of its target to costs, before adverse selection on passive fills. Not viable for a retail-latency trader as a pure microstructure play.
- **Materially different testable variant:** use order flow only as a slow-moving filter, e.g. cumulative delta divergence over 30–60 minutes at a structural level such as a prior VA edge or a single-print zone, with a target of 10–20 pt. This is testable with tick data (aggressor-flagged trades). The prior is weak: aggregated signed volume over minutes is largely reflected in price already.
- **HVN/LVN claim:** falsifiable as a speed and rotation claim: time-per-point inside prior-day LVNs is lower than inside HVNs, and reversals cluster at HVN edges. The speed half is almost tautological, because LVNs are where price spent little time. The tradeable half ("LVN rejection") is unverified.

### Gaps
- No public statistics from Axia Futures or Jigsaw on absorption-setup win rates were found. Axia was not searched specifically, given the limited budget.
- No study tests "absorption" as a predictor on ES/NQ at minute horizons.

---

## 4. Prop-desk and classic setup books (SMB/Bellafiore; T3 Live; Raschke & Connors *Street Smarts* 1995/96; Larry Williams; Toby Crabel 1990; Zarattini & Aziz / Bear Bull Traders)

### Takeaway
The classic setups (Raschke's Holy Grail, 80-20, Turtle Soup; Williams' Oops; Crabel's ORB with NR4/NR7/inside-day filters and "stretch") are precisely defined and testable, but their original publications give few if any win-rate statistics. Raschke herself says results are "difficult to quantify." SMB's *One Good Trade* teaches process (in-play stocks, risk discipline) rather than falsifiable ES/NQ claims.

The only modern, quantified, ES/NQ-relevant claims from the educator world come from Zarattini & Aziz (Bear Bull Traders, Concretum). Their 5-minute QQQ ORB is already dead in our program. Their SPY "Noise Area" intraday momentum (2024/2025) is a materially different variant of intraday momentum from the dead last-half-hour test, and it is the strongest candidate in this file.

### Cited Findings
**Raschke & Connors, *Street Smarts* (1996)**
- Holy Grail: ADX(14) above 30 and rising, price pulls back to the 20-period EMA, enter on a break of the pullback bar's high (long). Some versions use the 20 SMA. "No reliable published figure" for performance exists. — [TradingView Holy Grail script](https://in.tradingview.com/script/emQdbShi-Linda-Raschke-s-Holy-Grail); [therighttrader Holy Grail](https://therighttrader.com/learn/trading-strategies/holy-grail-setup)
- Turtle Soup: price makes a new 20-day extreme, the prior 20-day extreme is at least 3 days old (other sources say 4), and the trader fades the break. — [Traders' Online 2005 article](https://technical.traders.com/tradersonline/display.asp?art=2414); [therighttrader Turtle Soup](https://therighttrader.com/learn/trading-strategies/turtle-soup)
- The original author's view on the patterns: "difficult to quantify the results... profitability depends at least on your money management rules." — [Traders' Online 2005](https://technical.traders.com/tradersonline/display.asp?art=2414)
- Oxford Strat ran a quantified Turtle Soup test (profit factor, Sharpe, win rate). The values could not be read (host blocked). — [oxfordstrat Turtle Soup](https://oxfordstrat.com/?p=5614)
- An independent personal study of an ICT-style Turtle Soup (daily EURUSD) found poor results with low signal counts. Different market and variant. — [quant-study-notes turtle soup](https://tamaraabu4-cell.github.io/quant-study-notes/projects/turtle-soup.html)
- 80-20: an intraday strategy published in *Street Smarts*. No statistics were found. — [Traders' Online 2005](https://technical.traders.com/tradersonline/display.asp?art=2414)
- [UNVERIFIED-MEMORY] 80-20 rule:
  - Prior day opens in its top 20% and closes in its bottom 20% of range.
  - Today trades at least 5–15 ticks below the prior low, then a buy stop at the prior low; mirror rule for shorts.
  - Derived from George Taylor's "Book Method" observation: after such a day there is an 80–90% chance of trading below the low the next day, but only about 50% of closing lower.
  - This is a prior-day-low sweep with a candle-shape filter, so it overlaps the dead PDH/PDL sweep test. Only the "open-top / close-bottom" filter is new.

**Toby Crabel, *Day Trading with Short-Term Price Patterns and Opening Range Breakout* (1990) and S&C articles (1988–89)**
- Hypothesis: inside days precede trend days and hence successful ORBs. Tested on T-bonds, S&P 500, soybeans and cattle (Figure 3, S&C ORB series Part 4). The table was not retrieved. — [S&C V.7:2 ORB Part 4](https://store.traders.com/-v07-c02-orb-pdf.html); [S&C V.7:4 ORB Part 5](https://store.traders.com/-v07-c04-orb-pdf.html)
- NR7 = the narrowest daily range of the last 7 days; trade the ORB the next day. — [therighttrader NR7](https://therighttrader.com/learn/trend-analysis/nr7)
- Oxford Strat NR7 breakout test: 42 futures markets, 1980–2016. Values not readable. — [oxfordstrat NR7](https://oxfordstrat.com/?p=8238)
- Independent code and backtest of Crabel's ORB on Nasdaq (Unger Academy). Content not retrieved. [MARKETING-adjacent education] — [Unger Academy](https://ungeracademy.com/?p=7020)
- [UNVERIFIED-MEMORY] Crabel's "stretch" = the 10-day average of the smaller of (open − low, high − open). Entry stops sit at open ± stretch, not at the opening-range high/low.
- [UNVERIFIED-MEMORY] Crabel's own tables report per-pattern percentages (ID/NR4, NR7, 2-bar NR) for S&P futures in 1982–1989, often in the 60–80% "profitable at close" range. These are in-sample, pit-era and pre-electronic, with no cost model. Treat them as historical curiosity.

**Larry Williams [UNVERIFIED-MEMORY]**
- Oops: open gaps below the prior day's low, then a buy stop at the prior low. Again a PDL reclaim, so it overlaps the dead tests.
- Volatility breakout: open ± x% of the prior range, often 0.5–0.6 × the prior day's range. Long Thursday-close-to-Friday-open-style day-of-week biases are multi-day, so out of scope.

**Zarattini & Aziz (Bear Bull Traders) / Concretum**
- "Can Day Trading Really Be Profitable?" (SSRN 4416622, 2023): 5-minute ORB on QQQ, 1% risk per trade, exit at the close. Reported 33.2% CAGR vs 14.9% buy-and-hold, Jan 2016–Feb 2023, 1,795 trades, zero slippage assumed. [ACADEMIC working paper; authors run a trading-education business] — [SSRN 4416622](https://papers.ssrn.com/abstract=4416622); summary via [CXO Advisory](https://www.cxoadvisory.com/technical-trading/day-trading-with-an-opening-range-breakout-strategy)
- Independent replication on five index CFDs: "gross reproduced, net zero." Snippet only. — [mql5 blog replication](https://www.mql5.com/en/blogs/post/776235)
  - This is consistent with our own result (weak positive on NQ only).
- "Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)" (Zarattini, Aziz, Barbon; SFI WP 24-97, May 2024, revised Feb 2025)
  - Rules: noise boundaries = today's open × (1 ± the average absolute open-to-minute-t move over the last 14 days). The upper or lower bound is adjusted by the overnight gap. Go long or short on a break outside the "Noise Area." Trailing stop = max(boundary, VWAP) for longs, min for shorts. Flat at the close.
  - Reported results: 19.6% net annualized, Sharpe 1.33, max drawdown −25%, May 2007–Apr 2024. Commissions and slippage are included. Also won 4th place in the Quantpedia Awards 2025.
  - Sources: [SFI WP 24-97](https://www.sfi.ch/de/publications/n-24-97-beat-the-market-an-effective-intraday-momentum-strategy-for-s-p500-etf-spy); [IDEAS/RePEc](https://ideas.repec.org/p/chf/rpseri/rp2497.html); [CXO summary](https://www.cxoadvisory.com/momentum-investing/complex-intraday-time-series-momentum-strategy-applied-to-spy/); [U. St. Gallen news on Quantpedia award](https://fsi.unisg.ch/de/newsdetail/news/quantpedia-awards-2025-fsis-barbon-and-team-secure-4th-place-with-intraday-momentum-strategy/)
  - [UNVERIFIED-MEMORY] Signals are checked only at :00 and :30 (every 30 minutes), and exposure is sized by inverse daily volatility.

**SMB Capital / Bellafiore, *One Good Trade* (2010), *The PlayBook* (2013)**
- [UNVERIFIED-MEMORY] The books teach "stocks in play," reading the tape at key levels, and risk/process discipline. They contain no published ES/NQ win-rate claims. They are single-stock focused and out of scope for ES/NQ.
- T3 Live: no search done (budget). Not covered.

### Inferences
**Candidate shortlist, with rough effect size vs costs**

| # | Candidate | How it differs from what we killed | Effect size vs costs | Priority |
|---|---|---|---|---|
| A | Noise-Area intraday momentum (Zarattini/Aziz/Barbon 2024) on ES/NQ | Our dead tests were last-half-hour momentum and the 5-minute ORB. This uses a volatility-scaled, time-of-day-varying boundary, 30-minute checkpoints, a VWAP/boundary trailing stop and all-day holding. It is a different signal construction. | Reported Sharpe 1.33 net on SPY. Average trade is likely in the tens of basis points; per-trade cost at SPY ~0.6 bp-equivalent vs ES 0.33/6500 ≈ 0.5 bp. Costs should not kill it. The risk is in-sample overfitting (14-day lookback, 30-minute grid) and post-2024 decay. | Highest |
| B | Crabel ORB conditioned on NR7 / ID-NR4, with stretch-based entry instead of the 5-minute range | The dead 5-minute ORB was unconditional. This adds a volatility-compression day filter and a different trigger distance. | Fires on about 15–25% of days. Targets are full-day, so costs are under 2% of R. Original evidence is pit-era and in-sample. | Medium |
| C | Raschke Holy Grail on 5–15-minute ES/NQ (ADX above 30 and rising + 20-EMA pullback) | No equivalent in the dead list | 5-minute stops give a cost burden of 5–10% of R. 15-minute is better. No evidence base at all. | Low–medium |
| D | Turtle Soup intraday (new 20-bar extreme of a 15-minute series where the prior extreme is at least N bars old; fade) | Different from PDH/PDL sweep: it uses a rolling N-bar extreme, not session levels. But the sweep logic is similar, and that died. | Unknown | Low |
| E | 80-20 (prior-day candle-shape filter + PDL reclaim) | Only the candle filter is new | Low frequency | Low (variant of a dead test) |

- Survivorship and marketing:
  - Zarattini and Aziz are tied to Bear Bull Traders and Concretum, which are education and fund businesses.
  - The ORB paper assumed zero slippage, and an independent replication found net about zero.
  - The Noise-Area paper includes costs and has a long sample (2007–2024), but its parameters were chosen in-sample.
  - The Raschke and Crabel setups survived decades of retelling because they are memorable, not because they were validated.

### Gaps
- The Oxford Strat numeric results (Turtle Soup, NR7), Crabel's original tables and the Unger Academy ORB results were not readable in this session.
- No out-of-sample replication of the Noise-Area strategy on ES/NQ futures was found (search budget). The exact cost assumptions in the SFI paper (per-share commission and slippage) were not verified, because the CXO and Concretum hosts were blocked.
- T3 Live and Axia Futures curricula were not specifically researched.

---

## 5. CMT curriculum: what it says has evidence

### Takeaway
The CMT program cites the academic literature on technical-analysis profitability. The key references are Park & Irwin (2007) and Lo, Mamaysky & Wang (2000). That literature finds positive results in a majority of older studies, but flags data snooping, ex-post rule selection, and risk and cost estimation as pervasive problems. An official CMT reading list mapping intraday ES/NQ claims to evidence was not found in this session.

### Cited Findings
- Park & Irwin (2007), "What do we know about the profitability of technical analysis?", *Journal of Economic Surveys* 21(4):786–826. The review flags "data snooping, ex post selection of trading rules or search technologies, and difficulties in estimation of risk and transaction costs." [ACADEMIC] — [RePEc](https://econpapers.repec.org/RePEc:bla:jecsur:v:21:y:2007:i:4:p:786-826)
  - Reported tally: 59% positive, 21% negative, 20% mixed. From a secondary source, not checked against the paper.
- Lo, Mamaysky & Wang (2000), "Foundations of Technical Analysis," *Journal of Finance* 55(4):1705–1765: kernel-regression detection of chart patterns finds some incremental information in daily US stock data. [ACADEMIC] — [PDF](https://bashtage.github.io/kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Lo_Mamaysky_Wang.pdf)
- A literature review by CMT holders (Scott, Carr, Cremonini) covers "Publications Reviewed for the Revised CMT Curriculum." The full list was not seen. — [Scribd SSRN 2202060](https://www.scribd.com/document/665775431/SSRN-id2202060)
- CMT program overview (Level I–III structure). — [Efficient Learning CMT overview](https://efficientlearning.com/cmt/resources/program-overview/)

### Inferences
- The CMT curriculum is largely daily and weekly in horizon and generic across asset classes. It offers no specific, quantified ES/NQ intraday claims. Its main contribution here is methodological: data-snooping corrections and out-of-sample discipline, which should be applied to every candidate in this file.
- The academic evidence pattern holds that older studies, often pre-1990s and before costs, found profits that shrink or vanish in later samples. That matches the replication outcomes seen here: ORB gross reproduced, net zero.

### Gaps
- An official CMT Level I–III reading list and its specific positions on intraday patterns were not retrieved.
- The Park & Irwin 59/21/20 tally was not verified against the primary paper.

---

## 6. Independent rigorous tests, survivorship bias and marketing flags (cross-cutting)

### Takeaway
Across all curricula, independent rigorous testing exists for only three items: OFI microstructure (academic, sub-second, not retail-tradeable), the Zarattini/Aziz ORB (replicated: gross yes, net zero), and the Zarattini/Aziz/Barbon Noise-Area momentum (academic working paper with costs; independent futures replication not found). Everything in Market Profile, Brooks, order-flow and Raschke/Crabel is untested in public, or tested only by forum users and indicator vendors.

### Cited Findings
- 80% rule: "dissolves under rigorous testing"; a handful of days per year on ES under strict rules. [forum, snippet] — [NexusFi](https://nexusfi.com/a/concepts/80-percent-rule)
- ORB on QQQ: 33.2% CAGR with zero slippage. [ACADEMIC] — [SSRN 4416622](https://papers.ssrn.com/abstract=4416622). Replication: "gross reproduced, net zero." [SECONDARY] — [mql5](https://www.mql5.com/en/blogs/post/776235)
- Noise-Area SPY momentum: 19.6% net annualized, Sharpe 1.33, 2007–2024. [ACADEMIC] — [SFI WP 24-97](https://www.sfi.ch/de/publications/n-24-97-beat-the-market-an-effective-intraday-momentum-strategy-for-s-p500-etf-spy)
- E-mini OFI effects decay within one second. [ACADEMIC] — [arXiv 2508.06788](https://arxiv.org/abs/2508.06788v4)
- IB statistics come from a self-published dashboard without methodology. [MARKETING] — [trevor-trades](https://trevor-trades.vercel.app/analysis). The figures conflict with a Reddit 3-year count. — [Reddit mirror](https://lr.eu.psf.lt/r/FuturesTrading/comments/1bycosx/this_is_how_ess_price_moves_70_of_the_time)
- Holy Grail / 80-20: no reliable published figures. Raschke herself calls them "difficult to quantify." — [Traders' Online 2005](https://technical.traders.com/tradersonline/display.asp?art=2414); [therighttrader](https://therighttrader.com/learn/trading-strategies/holy-grail-setup)

### Inferences
**Bias flags to carry into testing**
1. Definitional elasticity. Most Market Profile and Brooks claims survive because their terms (acceptance, strong breakout, context) are flexible after the fact. Pre-register exact definitions.
2. Frequency vs payoff confusion. "IB breaks 70%" or "80% traverse" are touch frequencies. Always measure maximum adverse excursion and net R.
3. Regime. Crabel, Steidlmayer and the early Dalton work are pit-era S&P (1980s–90s). The electronic, 23-hour Globex, 0DTE-heavy market of 2023–2026 differs structurally. Post-2022 0DTE dealer-gamma flows plausibly change intraday momentum and reversal behavior; candidate A should be tested by sub-period.
4. Seller incentives. Jigsaw, Trader Dale, Brooks, Bear Bull Traders and indicator vendors sell products. Their claims are hypotheses, not evidence.

**Recommended test order** (by prior × testability × difference from dead tests)
1. Noise-Area momentum on ES and NQ: 1-minute data, 30-minute checkpoints, VWAP/boundary trail, flat by 15:59 ET. Test out-of-sample on 2024-05 to 2026-11 (after publication).
2. Crabel NR7 / ID-NR4–conditioned stretch breakout.
3. Poor-extreme vs clean-extreme revisit and reaction (a profile-shape variant of the dead PDH/PDL test).
4. A mechanized Brooks trading-range-breakout failure fade on 5-minute bars.
5. The strict 80% rule, accepting low power.

### Gaps
- No independent futures-level (ES/NQ) out-of-sample replication of the Noise-Area paper was located. It may exist on Quantpedia or Concretum; those hosts were not reachable or not searched.
- Gao, Han, Li & Zhou (2018, *JFE*) "Market intraday momentum" (first half-hour predicts the last half-hour) is the academic basis of the already-dead last-half-hour momentum test. [UNVERIFIED-MEMORY; no URL retrieved in this session]
- Baltussen, Da, Lammers & Martens (2021, *JFE*) link intraday momentum to dealer gamma hedging. [UNVERIFIED-MEMORY; no URL retrieved] This would be the mechanism for candidate A and for any gamma-conditioned variant.
