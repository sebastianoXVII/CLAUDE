# Intraday return predictability and intraday anomalies in US equity index futures (ES/NQ) and SPY/QQQ — replication, decay, 2020-2026 status

Research date: 2026-11-06. Method: web search plus secondary summaries. SSRN, nd.edu and dev.to could not be fetched from this session (blocked by the network), so several primary-paper numbers come from abstracts or secondary summaries and are marked that way. Items marked **[UNVERIFIED]** come from background knowledge and were not confirmed against a source in this session. Re-check them before relying on them.

## 1. Intraday time-series momentum (Gao-Han-Li-Zhou 2018; Baltussen-Da-Lammers-Martens 2021)

### Takeaway
The "first half-hour (plus 12th half-hour / rest-of-day) predicts last half-hour" effect is well documented in-sample for 1993-2013 (SPY) and 1974-2020 (60+ futures). It has a credible mechanism (gamma hedging and leveraged-ETF rebalancing): the effect concentrates on days when dealers are net short gamma. The 2020-2026 evidence points to a sharp decline in the *unconditional* US index effect in the 0DTE era. The best available evidence is weak (non-peer-reviewed vendor tests, plus one OOS SSRN test of a related strategy). Treat the effect as **conditional at best (negative-gamma or large-move days), not a standalone edge**.

### Cited Findings
- Gao, Han, Li & Zhou, "Market intraday momentum", JFE 2018. The sample is S&P 500 ETF (SPY) high-frequency data, 1993-2013. The first half-hour return (measured from the previous close) predicts the last half-hour return, in and out of sample — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351); [working paper PDF](https://assets.super.so/e46b77e7-ee08-445e-b43f-4ffd88ae0a0e/files/ee7dac49-530b-4950-b5d0-e0b5eee08f2e.pdf)
- Reported R² is about 1.6-1.7% using the first half-hour alone, rising to about 2.6% when the 12th half-hour (the half-hour before the last) is added. The values come from a search summary of the SSRN version — [SSRN-id2440866 mirror](https://www.smallake.kr/wp-content/uploads/2015/01/SSRN-id2440866.pdf). The exact in-sample vs OOS split still needs checking against the paper **[partially verified]**
- From background knowledge: the original paper reports stronger predictability on high-volatility days, high-volume days, recession periods and major macro-news days, and reports that timing strategies beat always-long benchmarks **[UNVERIFIED in this session]**.
- Baltussen, Da, Lammers & Martens, "Hedging demand and market intraday momentum", JFE 142(1), 2021, pp. 377-403. The sample is 60+ futures (equity, bond, commodity, FX), 1974-2020. Rest-of-day return predicts the last 30 minutes, and the effect reverts over the following days — [EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403); [EUR repository](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/)
- The paper's mechanism is gamma hedging by option market makers and leveraged ETFs. A secondary summary (Alpha Architect, secondary) says momentum is much stronger on negative net-gamma-exposure days and **not significant on positive-NGE days**. The same summary gives timing-strategy Sharpe ratios of 0.87-1.73 at asset-class level — [Alpha Architect (secondary)](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/). These numbers were not verified against the paper; nd.edu could not be fetched.
- International replication: Li, Sakkas & Urquhart (global evidence) find the first half-hour predicts the last half-hour in 12 of 16 markets — [Lancaster FoFI 2020 WP](http://wp.lancs.ac.uk/fofi2020/files/2020/04/FoFI-2020-092-Zeming-Li.pdf); [Reading accepted version](https://centaur.reading.ac.uk/95566/1/Accepted-Version.pdf)
- A negative or weak replication: a Swedish single-stock study finds the effect weak and not robust across most stocks — [DiVA thesis](https://www.diva-portal.org/smash/get/diva2:1878991/FULLTEXT01.pdf) (student thesis, low weight).
- Hossain et al. (2021, S&P 500 and CSI300) find the last half-hour shows no significant intraday-momentum impact during the COVID shock — [ResearchGate](https://www.researchgate.net/publication/356901732_THE_IMPACT_OF_INTRADAY_MOMENTUM_ON_STOCK_RETURNS_EVIDENCE_FROM_SP500_AND_CSI300); [Murdoch](https://researchportal.murdoch.edu.au/esploro/outputs/journalArticle/The-impact-of-intraday-momentum-on/991005544842407891) (low-tier journal).
- 0DTE-era decay: a vendor (gex.live, posted on dev.to) tested 1,085 SPX sessions in the 0DTE era. It reports the unconditional effect is "gone, flat overall, flat in every single year, signs alternating" — [dev.to (vendor, not peer-reviewed; page could not be fetched, quoted via search snippet)](https://dev.to/firmtape/intraday-momentum-is-dead-in-the-0dte-era-we-measured-it-on-1085-spx-sessions-43g0)
- Adams et al. (0DTE, summarized by Quantpedia) report that intraday variation in market makers' hedging needs predicts stronger order-flow reversals and **lower momentum returns**. That is consistent with long-gamma dealer positioning suppressing intraday momentum — [Quantpedia (secondary)](https://quantpedia.com/do-sp500-0dtes-options-increase-market-volatility/)
- Iwanaga & Sakemoto (SSRN) document a related overnight-to-first-half-hour reversal pattern in US indices. It weakened after the 2010s and in the later pandemic phase — [SSRN 5807282](https://papers.ssrn.com/sol3/Delivery.cfm/5807282.pdf?abstractid=5807282)

### Inferences
- The mechanism (dealer short gamma leading to late-day momentum) implies the effect should be **state-dependent**. Since 2022, SPX 0DTE growth and long-gamma dealer positioning on many days should push toward suppression. That matches the weak 2020-2026 evidence.
- The edge is concentrated in the last 30 minutes and is a few basis points on average. A tiny R² (about 1-3%) means per-trade costs for ES (about 0.25 pt tick plus commission) eat a large share unless you filter for big-move or negative-gamma days.
- For an edge map: rank this as **"conditional, decayed"**. Use it only as a filter: trade in the rest-of-day direction when the day's move is large or dealer gamma is estimated negative. Validate on your own 2022-2026 ES data before using it.

### Gaps
- No peer-reviewed post-2020 US-index study directly measuring decay of the Gao et al. effect was found. The decay claim rests on vendor tests.
- The exact NGE-conditional coefficients and Sharpe ratios in Baltussen et al. could not be verified (nd.edu was blocked).
- No futures-specific (ES/NQ) post-2020 replication with transaction costs was found.

## 2. Opening range breakout (ORB) and first-hour behavior

### Takeaway
The academic support for ORB is thin and comes mostly from commodity futures. The popular Zarattini-Aziz(-Barbon) SSRN papers show impressive in-sample backtests. They are written by practitioners selling trading education/products, and they assume zero or idealized frictions. The first independent OOS test (May 2024 to March 2026) of the SPY "Beat the Market" strategy reports Sharpe 0.39 and a 9.4% total return against 29.5% for buy-and-hold. **Treat ORB as unproven or decayed.**

### Cited Findings
- Crabel (1990), *Day Trading with Short Term Price Patterns and Opening Range Breakout*, is a practitioner book with no peer-reviewed statistics **[UNVERIFIED; no source fetched]**.
- Holmberg, Lönnbark & Lundström, "Assessing the profitability of intraday opening range breakout strategies", Finance Research Letters 10(1), 2013, pp. 27-33. The test is on crude oil futures, using bootstrap and martingale tests — [IDEAS](https://ideas.repec.org/a/eee/finlet/v10y2013i1p27-33.html); [Umeå WP 845](https://econpapers.repec.org/RePEc:hhs:umnees:0845). From background knowledge, it finds statistically significant ORB profits in CL futures over 1983-2011 **[result figures UNVERIFIED in this session]**. Lundström's follow-ups apply ORB to CL and **S&P 500 index futures** conditioned on volatility states — [IDEAS 0861](https://ideas.repec.org/p/hhs/umnees/0861.html); [IDEAS 0974](https://ideas.repec.org/p/hhs/umnees/0974.html)
- Zarattini & Aziz, "Can Day Trading Really Be Profitable?" (SSRN 4416622, April 2023). It tests a 5-minute ORB on QQQ (and TQQQ), January 2016 to February 2023, with 1,795 trades: 33.2% vs 14.9% CAGR, **zero slippage assumed** — [SSRN](https://papers.ssrn.com/abstract=4416622); [CXO Advisory (secondary)](https://www.cxoadvisory.com/technical-trading/day-trading-with-an-opening-range-breakout-strategy)
- Zarattini, Aziz & Barbon, "Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)" (SFI Research Paper 24-98, May 2024). It uses noise-boundary breakouts with VWAP trailing stops. The volatility-targeted version reports 19.6% net annual return, Sharpe 1.33 and -25% max drawdown over May 2007 to April 2024, **in-sample** — [EconPapers](https://econpapers.repec.org/RePEc:chf:rpseri:rp2498); [CXO Advisory (secondary)](https://www.cxoadvisory.com/?p=46335)
- A QuantConnect community reimplementation reports Sharpe about 2.4 and beta about 0. This is third-party and in-sample, and the cost model is unknown — [QuantConnect](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/)
- **Independent OOS test**: Paz, "Out-of-Sample Evaluation of an Intraday Momentum Strategy for the S&P 500 ETF (SPY)" (SSRN 7290621). The in-sample replication matches the original. Out of sample, **May 2024 to March 2026**, it shows a 9.4% total return vs 29.5% buy-and-hold, Sharpe 0.39 — [SSRN 7290621](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7290621) (numbers from the search abstract snippet; the full text could not be fetched).

### Inferences
- The Zarattini papers fit a classic pattern: in-sample data mining across parameters (opening range length, stops, volatility targeting), frictionless or near-frictionless assumptions, and high publicity. The strategy reportedly kept its performance in the in-sample replication but failed in the ~2-year OOS window. That fits decay or overfitting, not a durable edge. Two years of data is short, so the OOS result is suggestive, not conclusive.
- The ORB logic overlaps with the gamma or intraday-momentum mechanism of section 1. If dealer long gamma dampens trend days, ORB should suffer in the same regimes.

### Gaps
- No peer-reviewed ORB study on ES/NQ with realistic costs and a post-2020 sample was found.
- Holmberg et al. 2013 effect sizes were not verified.
- No peer-reviewed evidence was found on first-hour reversal vs continuation in ES specifically after 2020.

## 3. Overnight vs intraday returns; overnight drift; gap behavior

### Takeaway
The robust finding (1993-2010s) is that essentially all of the US equity premium has accrued overnight (close-to-open), while intraday returns are near zero or negative. For futures, the overnight return is concentrated around the European open (2-3am ET). Explanations are contested (dealer inventory, news, retail/institutional clientele). No reliable peer-reviewed gap-fill statistics for ES/NQ were found.

### Cited Findings
- Cliff, Cooper & Gulen (2008, "Return differences between trading and non-trading hours: like night and day") find US equity returns are earned overnight (1993-2006) **[UNVERIFIED in this session — no source fetched]**.
- Lou, Polk & Skouras (2019, JFE, "A tug of war: overnight versus intraday expected returns") find momentum profits are earned overnight, while value, profitability and investment premia are earned intraday. This is described via a later paper — [arXiv 2507.04481](https://arxiv.org/pdf/2507.04481); [CEPR DP14462](https://repec.cepr.org/repec/cpr/ceprdp/DP14462.pdf)
- Boyarchenko, Larsen & Whelan, "The Overnight Drift" (NY Fed Staff Report 917, revised August 2022; later RFS). In S&P 500 (E-mini) futures, 1998-2019, the largest positive returns accrue 2-3am ET (about 3.6% annualized from that hour alone). The authors attribute this to dealer inventory risk after days of net selling, with a reversal of intraday sell-offs overnight — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf); [Liberty Street Economics](https://libertystreeteconomics.newyorkfed.org/2021/05/the-overnight-drift-in-us-equity-returns)
- A 2025 counter-paper argues the inventory explanation can't explain higher overnight returns for stocks with no prior-day loss, or the intraday/overnight continuation. It proposes overnight news instead — [arXiv 2507.04481](https://arxiv.org/html/2507.04481v1)
- The "market return around the clock" puzzle (JFQA) documents systematic patterns in market returns across the clock — [Cambridge JFQA](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/market-return-around-the-clock-a-puzzle/089E33AC0B4D3B9A02CBA31EDF6505B3)
- Kelly & Clark (2011, "Returns in trading versus non-trading hours: the difference is day and night", J. Asset Management) find ETF overnight returns exceed intraday returns **[UNVERIFIED in this session]**.

### Inferences
- For a minutes-to-hours ES/NQ trader, the overnight drift has some relevance during Globex hours: the European-open window, and reversal of RTH sell-offs overnight. It is a low-Sharpe, small-per-trade effect. Its 2020-2026 status is unverified.
- "Gap fill" statistics circulating among retail traders (e.g., "X% of ES gaps fill") lack academic sourcing. Treat them as unverified.

### Gaps
- No post-2019 update of the Boyarchenko et al. futures-hour decomposition was found.
- No peer-reviewed ES/NQ gap-fill study was found.
- Lou-Polk-Skouras and Cliff-Cooper-Gulen numbers were not verified from primary text.

## 4. Intraday mean reversion, volatility seasonality, end-of-day effects, MOC and leveraged-ETF flows

### Takeaway
The U-shaped intraday volatility pattern is the most robust "anomaly". It is useful for sizing and stops, not for direction. End-of-day mechanics are real: closing-auction pressure that reverts overnight, end-of-day reversal in single stocks (opposite to index momentum), and leveraged-ETF and option delta-hedging flows that create end-of-day momentum and next-day reversal. A 2024 survey warns the economic significance of leveraged-ETF rebalancing is overstated.

### Cited Findings
- Andersen & Bollerslev (1997, J. Empirical Finance, "Intraday periodicity and volatility persistence in financial markets") document the U-shaped intraday volatility periodicity in S&P 500 futures **[UNVERIFIED in this session — standard reference, not fetched]**.
- Bogousslavsky & Muravyev, "Should We Use Closing Prices? Institutional Price Pressure at the Close" (later "Who Trades at the Close?"). Closing prices often deviate significantly from closing quote midpoints, and these deviations fully revert overnight on average, half of the reversal shortly after the close. The deviations equal about 5% of the average daily return in exchange-listed stocks (Bloomberg summary) — [CAS catalog record](https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi...........c99219c3b8d0befc7e159b09f2439bea); [Bloomberg/BQ](https://www.bloombergquint.com/markets/noise-for-sale-in-giant-u-s-auctions-used-to-end-stock-sessions). The publication year and venue are inconsistent across sources (2019 / 2021 / 2023).
- Soebhag, Baltussen & Da, "End-of-Day Reversal" find a sharp cross-sectional reversal in individual stocks in the last 30 minutes. They attribute it to retail attention-induced buying and short-seller risk management. The authors call it distinct from, and complementary to, market-level intraday momentum. It won second place at the Quantpedia Awards 2025 — [EUR news](https://www.eur.nl/en/news/end-day-reversal-pattern-second-place-quantpedia-awards-2025); [OptionMetrics](https://optionmetrics.com/research/a-soebhag-g-baltussen-and-z-da-end-of-day-reversal/)
- Barbon, Beckmeyer, Buraschi & Moerke (2022, SFI WP 22-40): leveraged-ETF rebalancing and option delta-hedging cause significant end-of-day momentum and mean reversion in stock returns. The effects dissipate within the next trading day. Leveraged-ETF flows attract more liquidity provision and have a shorter-lived price impact — [SFI](https://www.sfi.ch/en/publications/n-22-40-liquidity-provision-to-leveraged-etfs-and-equity-options-rebalancing-flows-evidence-from-end-of-day-stock-prices); [SSRN 3925725](https://papers.ssrn.com/abstract=3925725)
- Rodier, Haryanto, Shum & Hejazi (2012): leveraged-ETF rebalancing explains about one-third of late-day volatility, and over 50% on days with a move of 3% or more by 3:30pm. Market adaptation may have reduced profitability — [CXO Advisory (secondary)](https://www.cxoadvisory.com/volatility-effects/front-running-leveraged-etfs-at-the-end-of-the-day)
- A 2024 literature survey (Penn State) finds the associations between leveraged-ETF rebalancing and late-day returns/volatility are statistically significant. It also finds most papers have "potentially serious methodological errors" and that the economic associations appear insignificant — [PSU survey](https://pure.psu.edu/en/publications/the-market-impact-of-leveraged-etfs-a-survey-of-the-literature/)
- Cheng & Madhavan (2009, "The dynamics of leveraged and inverse ETFs") is the foundational paper on the leveraged-ETF rebalancing mechanism (rebalancing demand ∝ L(L−1)·return) **[UNVERIFIED in this session]**.

### Inferences
- The U-shape helps with time-of-day volatility normalization (stops, sizing, comparing ORB ranges). Its stability across decades makes it the most "durable" item on the map, but it is not a directional edge.
- Index-level end-of-day effects push in opposite directions. Leveraged-ETF and short-gamma hedging push toward momentum into the close. The closing-auction pressure then reverts overnight. For ES traders, the actionable piece is reversion of close-related dislocations in the first minutes of Globex or the next open. No futures-specific cost-adjusted evidence was found.

### Gaps
- No ES-specific study of MOC imbalance publication (3:50pm ET) predictability with post-2020 data was found.
- Single-stock end-of-day reversal does not transfer directly to index futures.

## 5. Macro announcements: pre-FOMC drift and CPI/NFP

### Takeaway
The pre-FOMC drift (Lucca & Moench 2015) is **the best-documented case of post-publication decay**. Kurov, Wolfe & Gilbert (2021) find it essentially disappeared after 2015. Announcement-day volatility (CPI/NFP/FOMC) remains a risk-management fact rather than a directional edge.

### Cited Findings
- Lucca & Moench, "The Pre-FOMC Announcement Drift", JF 2015. The sample is 1994-2011, and S&P 500 returns are large in the 24 hours before scheduled FOMC announcements — [NBER conference version](https://conference.nber.org/confer/2013/MEs13/Lucca_Moench.pdf); [NY Fed / Boston Fed copy](https://www.bostonfed.org/-/media/Documents/conference/PDF/Lucca_preFOMCDrift.pdf). From background knowledge: about 49 bp in the pre-announcement window, accounting for a large share (about 80%) of the annual equity premium in the sample **[magnitudes UNVERIFIED in this session]**.
- Kurov, Wolfe & Gilbert, "The Disappearing Pre-FOMC Announcement Drift", Finance Research Letters 40 (2021), DOI 10.1016/j.frl.2020.101781. The drift appeared first at press-conference meetings, then **essentially vanished after 2015**, both with and without press conferences. The sample runs to December 2019, and the authors test reduced uncertainty as the explanation — [IDEAS](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html); [Skidmore PDF](https://www.skidmore.edu/economics/documents/KurovWolfeGilbert-TheDisappearingPre-FOMC-Announce-Drift-200914.pdf)
- A secondary summary reports the mean drift falling from about 0.49% to about 0.05% per meeting **[secondary, not verified against paper]** — [ResearchGate listing](https://www.researchgate.net/publication/345940053_The_Disappearing_Pre-FOMC_Announcement_Drift)
- Other work places the break earlier (after early 2011). The break date depends on the sample — [HHS working paper](http://arc.hhs.se/download.aspx?MediumId=3247); [Applied Economics 2024](https://www.tandfonline.com/doi/full/10.1080/00036846.2024.2322573)
- Boguth et al. found the drift limited to press-conference meetings. Cieslak, Morse & Vissing-Jorgensen (2019) attribute FOMC-cycle returns to news leakage — cited within [IDEAS/Kurov](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html)
- A JFQA paper explains the pre-announcement drift via disagreement resolution — [Cambridge JFQA](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/disagreement-and-scheduled-announcements-explaining-the-preannouncement-drift/D95FE7194D48A9430B26876EDEBBA9C3)

### Inferences
- Pre-FOMC drift should be rated **"dead after publication"** in the edge map, unless 2020-2026 data shows a revival. No such evidence was found.
- No peer-reviewed post-announcement drift in ES after CPI/NFP was found in this session. Treat claims of directional post-CPI continuation as unverified.

### Gaps
- There was no time to search for 2020-2026 studies on CPI/NFP intraday volatility in ES (the 2022-2023 CPI days were notably volatile), or for post-announcement drift in futures.
- No 2020-2026 update of the pre-FOMC drift was found.

## 6. Options-driven flows: dealer gamma (GEX), 0DTE, pinning, vanna/charm

### Takeaway
The academic and exchange evidence (2023-2026) converges on the following. Aggregate 0DTE and dealer-gamma effects tend to *dampen* intraday volatility and favor reversal over momentum, and Cboe estimates net market-maker 0DTE gamma hedging as tiny relative to ES liquidity. Some papers dispute this (Iannucci 2026 argues amplification). Specific retail narratives (vanna/charm flows, precise GEX flip levels, "pinning" to strikes as a tradable signal) have **little peer-reviewed support**. Most of that content comes from commercial vendors such as SpotGamma.

### Cited Findings
- Dim, Eraker & Vilkov, "0DTEs: Trading, Gamma Risk and Volatility Propagation" (2024 WP). Higher 0DTE and short-dated open-interest gamma is associated with **lower** intraday realized volatility. The effects do not carry into the overnight session, and 0DTE trades do not amplify moves via delta hedging — [Harbourfront Quant (secondary)](https://harbourfrontquant.substack.com/p/the-rise-of-0dte-options-cause-for) **[not verified against paper]**
- Adams, Fontaine & Ornthanalai (0DTE WP, via Quantpedia) find a robust negative relation between 0DTE trading and realized S&P 500 volatility. Market makers' intraday hedging needs predict stronger order-flow reversals, lower momentum returns and lower volatility, with effects dissipating after about 1 hour — [Quantpedia (secondary)](https://quantpedia.com/do-sp500-0dtes-options-increase-market-volatility/)
- Cboe (September 2023, "Much Ado About 0DTEs"): market makers' net gamma from SPX 0DTE is typically $170mm-$670mm intraday, against about $400bn of daily S&P futures volume. The flow is "remarkably balanced" — [Cboe](https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options). Conflict of interest: Cboe sells the product.
- Cboe (May 2025, "0DTEs Decoded"): retail is about 50-60% of SPX 0DTE volume. Net market-maker gamma hedging is "de minimis", at most about 0.2% of SPX daily liquidity — [Cboe](https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact)
- Practitioner research: JPMorgan and SpotGamma (2023) reported more intraday reversal behavior in the 0DTE era — [SpotGamma (vendor)](https://spotgamma.com/volmageddon-no-jpm-bofa-say-0-dte-options-are-suppressing-intraday-vol/); [Advisor Perspectives/Bloomberg](https://www.advisorperspectives.com/articles/2023/08/15/zero-day-options-cement-presence-reversal-ridden-stock-market)
- Dissent: a Princeton senior thesis (April 2026) finds 0DTE trading related to intraday volatility, but does not support gamma-hedging feedback as the main channel — [Princeton](https://theses-dissertations.princeton.edu/entities/publication/61115cd1-cb09-4a8b-9230-ff488fc2a386). Iannucci (2026) argues 0DTE can amplify moves (cited via a search summary; primary source not located) **[UNVERIFIED]**.
- Baltussen et al. (2021, section 1) remain the strongest peer-reviewed link between dealer gamma sign and the direction of intraday predictability (momentum on negative-gamma days) — [EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403)

### Inferences
- Evidenced: gamma sign conditions volatility and momentum vs reversal (long gamma dampens volatility and favors mean reversion; short gamma favors momentum). Not evidenced: precise vendor GEX levels, vanna/charm "flows" as timing signals, or strike pinning as a reliable intraday edge in SPX/ES. These should be flagged as retail narrative pending independent tests.
- Public GEX estimates rely on assumptions about who is long or short (customers buy calls, sell puts, and so on). Cboe's own data suggests SPX 0DTE flow is balanced. That weakens estimates computed from public open interest.

### Gaps
- No peer-reviewed tests of vanna/charm or pinning in SPX/ES after 2022 were found.
- The primary texts of Dim-Eraker-Vilkov, Adams et al. and Brogaard et al. (0DTE) could not be accessed (SSRN blocked). Brogaard et al. findings were not located in this session.

## 7. Day-of-week, turn-of-month and pre-holiday effects at intraday level

### Takeaway
No reliable 2020-2026 intraday-level evidence was found in this session. Calendar effects are classic candidates for post-publication decay (McLean-Pontiff style), and they should be ranked low unless validated on your own data.

### Cited Findings
- None located with a verifiable source in this session's search budget.

### Inferences
- Classic results (Monday effect, turn-of-month, pre-holiday) come from pre-2000 daily data. Most papers are daily, not intraday. Treat them as unverified for intraday ES trading.

### Gaps
- Searches for intraday turn-of-month or pre-holiday studies in ES/SPY were not completed (tool budget). This area needs a dedicated follow-up.

## 8. Volatility-targeting / CTA flows and intraday footprint

### Takeaway
Late-day rebalancing flows (leveraged ETFs, vol-control funds, CTAs) are frequently blamed for late-session ES moves in journalism and sell-side notes. No peer-reviewed study isolating vol-control or CTA intraday price impact in ES was found. The closest academic evidence is for leveraged ETFs (section 4), and a 2024 survey questions its economic significance.

### Cited Findings
- Bloomberg reported that Nomura attributed an ES drop of 34 points (to 5,516) in 17 minutes near the close partly to leveraged-ETF rebalancing. It also mentioned vol-targeting rebalancing and 0DTE activity as amplifiers. This is journalism, not a controlled study — [iTiger/Bloomberg repost](https://www.itiger.com/news/2466019752)
- Todorov (BIS WP 952): in VIX-related ETPs, leverage rebalancing has the largest futures price effects among ETF rebalancing types — [EconPapers BIS WP 952](https://econpapers.repec.org/RePEc:bis:biswps:952)
- The leveraged-ETF late-day volatility share (about 1/3, over 50% on ±3% days) comes from Rodier et al. 2012 — [CXO (secondary)](https://www.cxoadvisory.com/volatility-effects/front-running-leveraged-etfs-at-the-end-of-the-day); the survey caveat is in [PSU survey](https://pure.psu.edu/en/publications/the-market-impact-of-leveraged-etfs-a-survey-of-the-literature/)

### Inferences
- Vol-control or CTA flow forecasts (sell-side "CTA trigger levels") are not academically validated as intraday timing signals. The direction of the mechanism (selling into rising volatility or falling prices) is consistent with Baltussen-type short-gamma momentum on large-move days.

### Gaps
- No academic paper quantifying vol-control or CTA intraday price impact in ES was found.

## Summary edge-map ranking (author's inference, not a cited result)
1. **Durable but non-directional:** U-shaped volatility and announcement-time volatility (use for sizing and stops).
2. **Conditional, partially decayed:** last-30-minute momentum on large-move or negative-gamma days (Gao 2018; Baltussen 2021). The unconditional version is likely dead in the 0DTE era (weak evidence).
3. **Plausible microstructure:** reversion of close-auction or leveraged-ETF dislocations overnight or at the next open (Bogousslavsky-Muravyev; Barbon et al.). Effect sizes and costs for ES are unverified.
4. **Structural, low-frequency:** overnight drift around the European open (Boyarchenko et al.). 2020-2026 status is unverified.
5. **Likely overfit or decayed:** ORB / "Beat the Market" (in-sample, idealized costs; OOS 2024-2026 Sharpe 0.39).
6. **Dead after publication:** pre-FOMC drift (gone after about 2015).
7. **Unsupported retail narrative:** vanna/charm flows, precise GEX levels, strike pinning, intraday calendar effects.

Access notes: papers.ssrn.com, www3.nd.edu and dev.to were not reachable from this session. Allowing them in the network settings would let primary-text verification of the items marked [UNVERIFIED] or "secondary" happen.
