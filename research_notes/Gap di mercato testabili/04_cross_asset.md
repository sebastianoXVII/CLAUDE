# Cross-asset lead-lag and intraday relative value for US index futures (5 min to a few hours, retail latency)

Scope note: I ran about 20 searches and fetches. Two fetches failed because the session's network blocked the hosts (libertystreeteconomics.newyorkfed.org and ideas.repec.org). Those sources are cited from search-result abstracts only, which the "[abstract-only]" tag marks. "[UNVERIFIED-memory]" marks items I recall from prior knowledge but could not confirm in this session. They need checking before anyone relies on them. "[secondary]" marks blogs, press and practitioner sources.

Bottom line across all questions: I did not find any peer-reviewed, post-2015 study showing a cross-asset lead-lag in US index futures that survives at horizons of 5 minutes or more and is large enough to clear 3x costs. The documented cross-asset lead-lags in ES, Treasuries and FX sit at millisecond, microwave-latency scales. Single-stock predictability from high-frequency data decays to a coin toss within about 5 minutes. The intraday effects that survive in the literature are not lead-lags. They are flow and positioning effects, such as dealer gamma hedging (conditional intraday momentum) and attention-driven retail flow at daily-to-monthly horizons. Our program can test every candidate below cheaply with Alpaca 1-minute ETF data. My prior is that they fail, so the tests are mainly for falsification.

## Q0. Cost hurdle: what effect size clears 3x costs?

### Takeaway
At late-2026 index levels, an ES round trip of 0.33 points is about 0.5 bp, and the 3x hurdle is about 1.5 bp per trade. A 5-minute signal needs an information coefficient (IC) of roughly 0.15 or more to clear it. A 60-minute signal needs an IC of about 0.05 to 0.07. An ES–NQ pair needs about 2 bp or more of expected spread convergence per round trip, net of both legs.

### Cited Findings
- No external source; this is arithmetic on the program's own cost inputs (ES 0.33 points, NQ 0.45 points per round trip). See Inferences.

### Inferences
- I assume ES is about 6,500 and NQ about 23,000 to 25,000 in Nov 2026; check against the program's data. On that basis, ES cost is 0.33/6500 ≈ 0.51 bp per round trip, so 3x ≈ 1.5 bp. NQ cost is 0.45/24000 ≈ 0.19 bp, so 3x ≈ 0.56 bp. In bp terms, NQ is cheaper per unit of notional.
- An ES+NQ pair at equal dollar notional costs about 0.7 bp in total, so 3x ≈ 2.1 bp of expected convergence. Contract sizes do not match: ES is about $325k of notional and NQ about $480k. A beta- or dollar-neutral hedge therefore needs MES/MNQ micros, which cost more per unit of notional. Recompute costs with the micros' real fees and tick sizes.
- Rough scale, assuming about 16% annualized vol and 1%/day: ES 5-minute returns have a std of about 11 bp, and 60-minute returns about 28 bp. The expected gain from a linear signal is about IC × σ × 0.8. Clearing 1.5 bp therefore needs an IC of about 0.17 at 5 minutes, about 0.07 at 60 minutes and about 0.05 at 2 to 3 hours. Published cross-asset ICs at these horizons, where they exist at all, are far below 0.1 (see below).
- The intraday SPY–QQQ return differential is volatile. I assume a daily differential vol of about 0.5% to 0.8%, which gives about 15 to 20 bp over 30 minutes. Costs alone therefore do not kill an ES–NQ pair; the binding question is whether there is any mean reversion.

### Gaps
- I did not verify the exact Nov-2026 ES and NQ levels or the MES/MNQ fees.

## Q1. ES–NQ (SPY–QQQ) intraday relative value, pairs and cointegration

### Takeaway
I found no peer-reviewed test of SPY–QQQ or ES–NQ intraday pairs or cointegration trading net of costs. Evidence from adjacent work (student theses, a 2026 critical preprint, and the HF lead-lag literature) is negative or neutral: stationarity does not imply profitability, and HF stock pairs lose money after costs in recent years. Verdict: unproven, prior negative; it can be tested cheaply with free data.

### Cited Findings
- A Copenhagen Business School master's thesis backtested ETF pairs over 2007–2020. Cointegration-based ETF pairs beat single-stock pairs, but distance-method pairs of ETFs tracking the same index lost money after costs. Daily horizon, student work — [CBS thesis](https://research.cbs.dk/en/studentProjects/pairs-trading-with-etfs-backtested-from-2007-2020/) [abstract-only]
- An Erasmus thesis on high-frequency copula pairs trading in US stocks found that after transaction costs "strongly declining returns in recent years suggest that neither of the variants remain profitable." Student work — [Erasmus thesis (Landgraf)](https://thesis.eur.nl/pub/34694/Landgraf.pdf) [abstract-only]
- A 2026 preprint, "Stationary but not profitable: a critical look at pairs trading" (Pandini), argues that cointegration does not reliably predict out-of-sample alpha once costs and regime changes are modelled. It is hosted on a press-release CDN, the peer-review status is unknown, and I did not check whether it covers ETFs — [Pandini 2026 PDF](https://mma.prnewswire.com/media/2965868/2026_00G__StationaryButNotProfitable_ACriticalLookatPairsTrading_DavidePandini.pdf?p=pdf) [abstract-only, low confidence]
- A UNSW thesis on Australian ETFs used Johansen cointegration and an error-correction model on intraday ETF versus iNAV mispricing, including spreads and costs, with live paper trading. It is not US data and not cross-index — [UNSW thesis](https://unsworks.unsw.edu.au/bitstreams/102a8395-bec4-429e-b065-cd239c078a4b/download) [abstract-only]
- Huth & Abergel (Journal of Empirical Finance, 2014; arXiv 1111.7103) studied tick-by-tick data. Lead-lag effects are strongest in futures/stock pairs, and the most correlated assets are those of similar liquidity. A leader-based forecast reaches about 60% directional accuracy on the lagger's next mid-quote move, but "a naive market-order strategy" cannot profit because of the bid/ask spread. The effects fade at larger time scales — [arXiv 1111.7103](https://www.arxiv.org/abs/1111.7103v1)
- Buccheri, Corsi & Peluso (JBES 2021, 39(3):605–621) built a multi-asset lagged-adjustment model. They find lead-lag effects and a multi-asset price-formation mechanism among NYSE stocks at high frequency, i.e. sub-minute microstructure, not tradable at retail latency — [EconPapers record](https://econpapers.repec.org/RePEc:taf:jnlbes:v:39:y:2021:i:3:p:605-621) [abstract-only]

### Inferences
- ES and NQ are both futures with comparable, very deep liquidity. In Huth & Abergel's framework, similar-liquidity instruments are highly contemporaneously correlated, with little lead-lag left at tradable lags. Any ES–NQ edge would therefore have to come from spread mean reversion (relative overreaction), not from one leading the other.
- The SPY/QQQ log-price ratio is unlikely to be stationary over months: tech has re-rated structurally since 2016. Any intraday test should use an intraday-anchored spread, for example the spread's deviation from that day's 9:45 value or from a rolling 60–120-minute beta-adjusted residual, with a flat position at the close. That avoids long-horizon cointegration assumptions.
- Concrete test (Alpaca 1-minute SPY and QQQ, 2016 to 2026):
  - Spread construction: s_t = r_QQQ − β·r_SPY, cumulated from 09:45, with β from a rolling 20-day window of 5-minute returns.
  - Entry: when the z-score of s_t exceeds ±2, fade it.
  - Exit: at z = 0, after 60 minutes, or at 15:55.
  - Check: the edge per round trip must reach at least 2.1 bp, using about 0.7 bp of combined costs (or the micros' real costs).
  - Robustness: split by year, and separately exclude CPI, FOMC and NVDA/mega-cap earnings days. Mega-cap news is the main reason the spread trends rather than reverts.
- I expect the spread to trend on news days, when it carries idiosyncratic tech information, and to revert weakly on quiet days. The net result is likely near zero. Treat this as a prior, not a finding.

### Gaps
- No academic or credible practitioner test of SPY–QQQ or ES–NQ intraday spread mean reversion with costs was found. Any claimed Sharpe ratios on quant blogs for this exact pair were not found or verified.
- I was not able to verify Marshall, Nguyen & Visaltanachoti's intraday ETF-arbitrage work (SPY vs IVV, J. Banking & Finance ~2013) [UNVERIFIED-memory]. In any case it covers same-index ETFs, not SPY–QQQ.

## Q2. Bonds to equities: do TLT/ZN moves lead SPY at 5–60 minutes?

### Takeaway
The documented Treasury–equity cross-market dependence sits at microwave-latency (millisecond) lags. A Fed/AQR study using 2010–2024 data cannot reject independence at longer lags. Where cross-market leadership exists, the E-mini tends to lead cash Treasuries, not the reverse. I found no post-2015 evidence that TLT or ZN leads SPY or ES at 5–60 minutes.

### Cited Findings
- Dobrev (Federal Reserve Board) & Schaumburg (AQR), "High-Frequency Cross-Market Trading: Model Free Measurement and Testable Implications":
  - Price discovery in US Treasury and equity markets happens mainly in futures, not cash.
  - Using 2010–2024 data, cross-market dependencies are concentrated at lags matching microwave latency, and the authors "do not reject independence at more distant lags."
  - Cross-market activity rises during stress and around FOMC announcements.
  - [Atlanta Fed conference PDF (2018 version)](https://www.atlantafed.org/-/media/documents/news/conferences/2018/1018-financial-stability-implications-of-new-technology/papers/dobrev-schaumburg_high-frequency-cross-market-trading.pdf); later draft summarized in search results [abstract-only; the 2010–2024 sample comes from the later draft's abstract]
- NY Fed Liberty Street Economics post on Treasury price discovery:
  - Futures usually lead cash Treasuries, but the reverse is often true.
  - Cross-market activity between the 10-year note and E-mini S&P is much thinner, and when it happens, the E-mini appears to lead cash Treasuries.
  - [Liberty Street Economics](https://libertystreeteconomics.newyorkfed.org/?p=683) [abstract-only; host blocked in session]
- Huth & Abergel find that lead-lag effects shift at macro announcements and at the US open, and fade at larger time scales — [arXiv 1111.7103](https://www.arxiv.org/abs/1111.7103v1)

### Inferences
- The structural expectation is that ES and ZN reprice jointly within milliseconds of macro news. After that, 5–60-minute moves in TLT are contemporaneously correlated with SPY, with the sign changing by regime: positive stock-bond correlation in 2022–2023 inflation scares, negative in risk-off episodes. But they are not predictive.
- A slow channel is conceivable: duration-sensitive sectors (XLU, XLRE, small caps) might adjust to rates with a lag of minutes. Testing it means checking whether lagged TLT returns predict IWM/XLU minus SPY, not SPY itself. It is untested in any source I found.
- Concrete test (Alpaca 1-minute TLT, IEF, SPY, 2016–2026):
  - Regress the forward SPY return over k = 5, 15, 30 and 60 minutes on lagged TLT returns over the same windows, controlling for lagged SPY.
  - Use non-overlapping windows or HAC errors, with rolling-year subsamples.
  - Check against the Q0 hurdle (IC ≥ 0.07 at 60 minutes).
  - Note that TLT on Alpaca is less liquid than ES. Its stale 1-minute bars can create spurious "SPY leads TLT" patterns, so use a midquote or last trade with care.
- Yahoo ZN=F hourly data (about 2 years) is too short and too coarse to estimate a 5–60-minute effect with any power.

### Gaps
- No post-2015 academic study found testing Treasury→equity predictability at 5–60-minute horizons with retail execution.
- The Liberty Street post's date, authors and sample could not be verified because the fetch was blocked.

## Q3. Credit (HYG/LQD), dollar (UUP, USDJPY) and the VIX complex as intraday predictors for ES

### Takeaway
Credit ETF "leadership" of stocks is practitioner lore with no rigorous intraday test found. VIX-complex lead-lag literature is mixed and mostly concerns the VIX index vs VIX futures vs SPX options. A 2024 Journal of Financial Markets paper finds VIX and SPX futures only weakly connected in low-vol regimes. I found nothing for UUP or USDJPY at intraday horizons. None of these offers documented ES predictive content at 5 minutes or more.

### Cited Findings
- **HYG:**
  - The leading-indicator claim comes from strategist Matt Maley ("if you can see the HYG break meaningfully above that $85 level, this does mark a good leading indicator for the stock markets"). It is a technical opinion, not a test — [ETF Trends](https://www.etftrends.com/multi-asset-channel/is-this-high-yield-etf-forecasting-the-next-stock-market-moves/) [secondary]
  - An iShares (issuer) study says HYG added price discovery for junk bonds during the 2015 sell-off. That is ETF leading bonds, not ETF leading equities, and there is issuer bias — [Fox Business](https://www.foxbusiness.com/markets/think-twice-before-assailing-junk-bond-etf-liquidity) [secondary]
- **VIX futures and SPX futures:**
  - Kokholm (Journal of Financial Markets, vol. 67, 2024) analyzes the lead-lag relation between VIX futures and SPX futures. The markets are only weakly connected when volatility is low, relative liquidity strengthens a market's lead, and market-maker hedging affects the relation — [IDEAS/RePEc](https://ideas.repec.org/a/eee/finmar/v67y2024ics1386418123000496.html) [abstract-only; host blocked; which side leads on average not confirmed]
  - Time-dependent lead-lag between VIX and VIX futures (arXiv 1910.13729) cites Chen & Tsai (2017): VIX futures dominate intraday price discovery versus the VIX index — [arXiv 1910.13729](https://arxiv.org/pdf/1910.13729)
  - High-frequency causality in the VIX index and its derivatives (arXiv 2206.13138) cites Frijns, Tourani-Rad & Webb: leading relations are stronger on negative-S&P, high-VIX days — [arXiv 2206.13138](https://arxiv.org/pdf/2206.13138)
  - A Taiwanese thesis found S&P 500 returns leading VIX by about 15–60 minutes and VIX leading the index by about 5–45 minutes. It is a thesis, the sample was not checked, and the long lags are suspicious given the HF literature — [NCU thesis](https://etd.lib.ncu.edu.tw/detail/9767f90ee1716e08232331f696fdf1df) [abstract-only, low confidence]
  - A GCN-LSTM approach for ES-mini and VX futures forecasting (arXiv 2408.05659, 2024) notes that E-mini futures carry a higher information share than SPX ETFs in high-vol periods (citing Kurov & Lasser 2004) — [arXiv 2408.05659](https://arxiv.org/pdf/2408.05659)
  - Gehricke et al. on VIX futures ETNs' efficiency and causality (AFM 2016) — [AUT PDF](https://acfr.aut.ac.nz/__data/assets/pdf_file/0006/59613/38099-V3-S-Gehricke-VIX-Futures-ETNs-Efficiency%2C-Consistency-and-Causality-AFM2016.pdf) [abstract-only]

### Inferences
- **HYG:** HYG and LQD are ETFs whose underlying bonds trade rarely. Intraday, the ETF price reflects equity-like risk factors almost contemporaneously. If anything, ES likely leads HYG (ETF market makers hedge with ES), not the reverse. A test of "HYG/SPY divergence predicts SPY" over 30–120 minutes is feasible with Alpaca, but the prior is null.
- **VIX ETPs:** VXX and UVXY are derivatives of VX futures, which in turn are hedged with SPX options and ES. Their intraday moves are largely mechanical functions of ES (spot-vol beta). Lead-lag at retail latency is unlikely. Plausible, testable variants are conditional ones:
  - (a) Term-structure state, VIX/VIX3M (backwardation vs contango), as a regime filter for intraday reversal vs momentum in SPY.
  - (b) Residual moves: the VXX return not explained by SPY's spot-vol beta over the last 15–30 minutes, used as a predictor of the next 30–60-minute SPY return.
  - Neither variant appears in any study I found.
- **UVXY data:** UVXY reverse splits and the 2018/2019 VXX relaunch (old VXX matured Jan 2019; the new series initially traded as VXXB) [UNVERIFIED-memory] will contaminate naive 1-minute history. Use split-adjusted data and splice carefully, or use Yahoo ^VIX and ^VIX3M hourly as state variables instead.
- **USD/JPY and UUP:** these are risk-on/risk-off covariates. Their intraday correlation with ES is regime-dependent; the yen carry unwind of Aug 2024 is a stress example. I found no evidence of predictive lead at 5 minutes or more. UUP is thinly traded (stale prints). USDJPY is not on Alpaca; Yahoo JPY=X hourly offers about 2 years only.

### Gaps
- No rigorous intraday test of HYG/LQD → SPY or ES predictability found.
- No intraday dollar (DXY, UUP, USDJPY) → ES predictability study found.
- Kokholm (2024) full results, including leader direction, lag length and sample, could not be fetched.

## Q4. Breadth and internals: NYSE TICK, A/D, cumulative TICK, sector dispersion, mega-cap leadership

### Takeaway
I found no peer-reviewed test of NYSE TICK extremes as reversal signals. The material is practitioner lore (e.g. Tim Ord, 1992, ±500/±600 thresholds; ±1000 "extremes") without out-of-sample tests. The academic literature consistently shows that index futures lead constituents, not the reverse. The "NVDA leads NQ" idea has no rigorous support; idiosyncratic-news predictors in the cross-section are sparse and last minutes.

### Cited Findings
- **TICK practitioner material:**
  - Tim Ord, "Market Turns and Continuation Moves with the Tick Index" (Stocks & Commodities, 1992): rules based on TICK readings around ±500–600, with no out-of-sample test — [PDF mirror](https://c.mql5.com/forextsd/forum/118/market_turns.pdf) [secondary]
  - MoneyShow notes that TICK extremes (±1000) cluster in volatile periods. It gives counts per year but no reversal test — [MoneyShow](https://moneyshow.com/articles/daytraders-22523) [secondary]
- **Closest academic analogue:** an IJFS 2021 paper finds intraday price reversal after order imbalance is more frequent when liquidity is high. It concerns order imbalance, not TICK — [UiT repository](https://ninum.uit.no/handle/10037/22975) [abstract-only]
- **Futures lead cash:**
  - Stoll & Whaley (JFQA 1990): S&P 500 and MMI futures returns lead stock-index returns by about 5 minutes on average, occasionally 10 minutes or more, even after purging infrequent-trading effects. Sample 1980s — [EconPapers](https://econpapers.repec.org/RePEc:cup:jfinqa:v:25:y:1990:i:04:p:441-468_00)
  - Kawaller, Koch & Koch (JF 1987), minute data: S&P futures led the index by about 20–45 minutes, with little feedback beyond a minute. Pre-electronic-era sample — [scite author page](https://scite.ai/authors/paul-d-koch-LevEAr) [abstract-only]
  - E-mini S&P futures have dominated price discovery relative to floor futures and the spot index since mid-1999 — [American University thesis](https://aura.american.edu/articles/thesis/Price_discovery_Electronic_versus_floor_trading_in_the_equity_index_futures_market/23868588) [abstract-only]
- **Cross-section and decay:**
  - Chinco, Clark-Joseph & Ye, "Sparse Signals in the Cross-Section of Returns" (JF 2019, 74(1):449–492): rolling LASSO 1-minute-ahead forecasts using all NYSE stocks' lagged returns improve out-of-sample fit and forecast-implied Sharpe ratios. The selected predictors are "unexpected, short-lived, and sparse," often stocks with fundamental news. Reported sample 2005–2012 (secondary summary), about 12.7 predictors per forecast, 30-minute estimation windows — [NBER w23933](https://www.nber.org/papers/w23933.ack); [EconPapers](https://econpapers.repec.org/RePEc:bla:jfinan:v:74:y:2019:i:1:p:449-492)
  - Aït-Sahalia, Fan, Xue & Zhou, "How and When are High-Frequency Stock Returns Predictable?" (NBER w30366, 2022). High-frequency predictability is "large, systematic, and pervasive" at very short horizons. Press summaries add three figures: about 80% of predictability comes from the last 10 ms or 10 transactions; a small artificial lag sharply cuts accuracy; and prediction becomes no better than a coin toss within about 5 minutes or about 2,000 transactions — [NBER w30366](https://www.nber.org/papers/w30366); [IR Impact summary](https://www.ir-impact.com/2022/08/movement-lower-priced-stocks-easier-predict-hft-firms-finds-princeton-paper) [figures secondary]

### Inferences
- **TICK is a contemporaneous measure.** It counts NYSE stocks whose last trade was an uptick minus downticks, so it largely restates the ES move that the futures already led. A TICK extreme signals a program/basket flow burst. Whether that burst reverts over 5–30 minutes is an empirical question that nobody has published a rigorous answer to.
- **TICK proxy test.** True NYSE TICK and ADD are not in Alpaca or Yahoo. With Alpaca 1-minute bars for S&P 500 or sector ETF constituents, a proxy can be built: the share of constituents with a positive 1-minute close-to-close change, minus the share with a negative one. This is a "minute-TICK," not tick-level, and it suffers survivorship bias unless the constituent list is point-in-time.
  - Hypothesis: fade SPY when proxy-TICK is in the top/bottom 1% of its trailing distribution.
  - Forward windows: 5, 15 and 30 minutes.
  - Hurdle: Q0.
  - Caveat: NYSE TICK's original appeal relies on NYSE-listed stocks including many non-operating issues (closed-end funds, preferreds) [UNVERIFIED-memory], so a constituent proxy is not equivalent.
- **Sector dispersion test (feasible, untested):** cross-sectional std of the 11 SPDR sector ETFs' 30-minute returns as a regime variable for SPY reversal vs continuation.
- **Mega-cap leadership:**
  - Chinco et al. and Aït-Sahalia et al. imply that any stock-to-index lead at retail latency (≥1 minute) is small, news-driven, sparse and gone within minutes. "NVDA leads NQ by 5–30 minutes" contradicts the dominant finding that index futures lead constituents.
  - Exception worth testing: after-hours NVDA/mega-cap earnings. Single-stock price discovery at those times may lead NQ futures, but that is overnight, outside the same-day mandate, and close to the already-dead overnight work.

### Gaps
- No rigorous academic test of NYSE TICK or cumulative TICK reversal signals found (practitioner lore only).
- No study found of mega-cap (NVDA, AAPL, MSFT) returns leading NQ/ES at ≥5-minute horizons in recent data.
- Full-text verification of the Aït-Sahalia et al. decay figures (5 minutes, 80% from 10 ms) was not possible; they come from press coverage.

## Q5. Small-cap vs large-cap (IWM vs SPY) lead-lag: Lo–MacKinlay and its decay

### Takeaway
Lo–MacKinlay (1990) large→small cross-autocorrelation was a weekly/daily-frequency phenomenon tied to thin trading and slow information diffusion in small stocks. Chordia, Sarkar & Subrahmanyam (JFQA 2011) show it strengthens when large-stock illiquidity is high. Between two highly liquid ETFs (SPY and IWM, plus ES and RTY futures), arbitrage keeps the lag at sub-second microstructure scales. I found no recent evidence of an exploitable IWM–SPY lead-lag at 5 minutes or more.

### Cited Findings
- Lo & MacKinlay (1990) first documented that lagged large-firm returns correlate more with current small-firm returns than the reverse. Chordia & Swaminathan (2000) link the pattern to trading volume; thin trading explains part, not all, of it — [NY Fed Staff Report 303](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr303.html)
- Chordia, Sarkar & Subrahmanyam (NY Fed SR 303, 2007; JFQA 2011, 46(3):709–736): liquidity spillovers persist across size deciles, large-stock returns lead small-stock returns even after accounting for liquidity dynamics, and the lead-lag is strongest when large-stock spreads and illiquidity are high — [JFQA](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/liquidity-dynamics-and-crossautocorrelations/E25BA8F3D1B1CA7EEB3416BBA4E53D6F); [SR 303 PDF](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr303.pdf)
- Huth & Abergel: more liquid assets lead less liquid ones, but lead-lag fades at larger time scales and is not profitable with market orders because of the spread — [arXiv 1111.7103](https://www.arxiv.org/abs/1111.7103v1)

### Inferences
- **Where Lo–MacKinlay still applies:** it concerns portfolios of individual small stocks, many illiquid, not IWM, which is itself a liquid ETF with continuous creation/redemption arbitrage against Russell 2000 futures. The IWM–SPY ETF-level lead-lag should therefore be minimal at ≥1 minute. Any residual lag would be visible inside IWM's constituents, not in IWM's price.
- **Conditional variant that is testable:** per Chordia–Sarkar–Subrahmanyam, the lag should be larger when liquidity is poor, e.g. high-VIX stress days or the first 15 minutes after the open. Test: forward 5/15/30-minute IWM return on lagged SPY return, with interactions for VIX level or SPY spread proxies.
- **Trade:** long/short IWM (or RTY/M2K) vs SPY (ES/MES) for 5–30 minutes. Both legs' costs apply. RTY/M2K costs were not given; obtain them.

### Gaps
- No study found that quantifies the decay of size-based cross-autocorrelation at intraday horizons after decimalization (2001) or Reg NMS (2007), or post-2015. The searches returned only daily/weekly-frequency work.

## Q6. Retail order flow, attention and 0DTE at intraday horizons

### Takeaway
Retail-attention effects are real but documented at daily-to-monthly horizons in single stocks, mainly small caps, not intraday in index futures. Barber–Huang–Odean–Schwarz found Robinhood herding is followed by roughly 5% reversals over a month, with most of the abnormal return at the next open; small caps only, gross of costs. On 0DTE, the best-documented intraday channel is dealer gamma: Baltussen et al. (JFE 2021) find late-day market intraday momentum only when dealer net gamma exposure is negative. Evidence that 0DTE dealer gamma shapes intraday volatility is contested; a 2026 Princeton thesis finds no incremental predictive power.

### Cited Findings
- **Barber, Huang, Odean & Schwarz** ("Attention-Induced Trading and Returns: Evidence from Robinhood Users"):
  - Sample May 2018 to Aug 2020.
  - The top 0.5% of stocks bought by Robinhood users each day show reversals of about 5% over the next month, and about 9% for extreme herding.
  - 5-day abnormal returns are −3% and −6% for the two herding measures.
  - Most of the abnormal return occurs at the open.
  - Effects appear only for market caps under $1bn.
  - Returns are gross of costs.
  - [SSRN 3715077 mirror](https://www.smallake.kr/wp-content/uploads/2020/12/SSRN-id3715077.pdf); [CXO Advisory summary](https://www.cxoadvisory.com/?p=34654) [secondary for figures]
- **Baltussen, Da, Lammers & Martens** (JFE 2021, 142:377–403):
  - Uses more than 60 futures across equities, bonds, commodities and FX, 1974–2020.
  - The return in the rest of the day positively predicts the last-30-minute return.
  - This is attributed to short-gamma hedging by option market makers and leveraged ETFs.
  - For the S&P 500, momentum is present when the negative gamma exposure proxy is negative and stronger when it is more negative. Per a summary, it is absent on positive-gamma days.
  - Asset-class-level Sharpe ratios are about 0.87–1.73 (Alpha Architect summary).
  - The effect reverts over subsequent days.
  - [EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403); [authors' PDF](https://www3.nd.edu/~zda/intramom.pdf); [Alpha Architect](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/) [secondary]
- **0DTE dealer gamma:** an SSRN paper summarized by Quantpedia finds that higher market-maker net gamma predicts lower S&P 500 volatility over the next 10 minutes, with the effect fading after about 1 hour. Hedging needs also predict stronger order-flow reversals and weaker momentum — [Quantpedia](https://quantpedia.com/do-sp500-0dtes-options-increase-market-volatility/) [secondary; original paper not verified]
- **Princeton senior thesis (2026):** the canonical gamma-hedging feedback channel "does not add meaningful predictive power for intraday variance forecasts" — [Princeton thesis](https://theses-dissertations.princeton.edu/entities/publication/61115cd1-cb09-4a8b-9230-ff488fc2a386) [student work]
- **Beckmeyer, Branger & Gayda (2023):** CBOE trader-type data, Jan 2021 to Feb 2023. Retail traders lost about $70m in aggregate on 0DTE SPX options. Descriptive, not a predictability test — [CXO Advisory](https://www.cxoadvisory.com/?p=44172) [secondary]
- **Hizmeri (Liverpool seminar), "0DTE Asset Pricing":** 0DTE accounts for about half of SPX option volume, and the findings are consistent with a pricing kernel that is high for positive market returns — [Liverpool IFAM](https://liverpool.ac.uk/institute-for-financial-and-actuarial-mathematics/past-seminars/rodrigo-hizmeri) [abstract-only]

### Inferences
- **Gamma-conditioned last-half-hour momentum.** Our program found last-half-hour momentum dead unconditionally. Baltussen et al. say the effect lives only in negative-gamma states. A gamma-conditioned retest is the one variant not yet covered. It is genuinely different, not a re-run, but still at risk of being dead post-2020:
  - Dealer gamma could flip sign with 0DTE retail call buying.
  - Free daily GEX/DIX from SqueezeMetrics may serve as a proxy [UNVERIFIED-memory: availability and history].
  - A cheaper free proxy is the prior-day VIX level or VIX/VIX3M backwardation (negative gamma correlates with stress).
- **Gamma-conditioned reversal.** The Quantpedia-summarized paper implies that positive-gamma regimes produce intraday reversals and dampened volatility. A testable rule: in positive-GEX or contango regimes, fade 30–60-minute SPY moves. The hurdle is still IC ≥ 0.07 at 60 minutes.
- **Robinhood-style flow.** It cannot be exploited intraday in ES. The effects are in small-cap single stocks, occur at the next open (overnight, outside the same-day mandate) and are gross of shorting costs. The Robinhood Popularity data that powered these studies stopped around Aug 2020 [UNVERIFIED-memory].
- **Retail-flow proxy.** The Boehmer–Jones–Zhang–Zhang retail order-flow measure (sub-penny price improvement, JF 2021) [UNVERIFIED-memory] predicts single-stock returns at weekly horizons. It needs TAQ-level data (trade-price decimals), not 1-minute bars.

### Gaps
- No paper found that directly tests intraday retail 0DTE flow (e.g. Cboe customer-type volume) as a predictor of 5–60-minute ES returns. The original SSRN paper behind the Quantpedia summary was not identified by title or author in this session.
- Post-2022 out-of-sample performance of Baltussen-style gamma-conditioned momentum: not found.

## Q7. Machine-learning intraday prediction for index futures (2020–2026), out-of-sample and net of cost

### Takeaway
I found no 2020–2026 paper that predicts ES/NQ at 5-minute-to-hours horizons with a clean out-of-sample design, realistic futures costs and a positive net result I would trust. Typical papers are one of three kinds: daily-frequency futures (Waldow et al., 2021, break-even costs of about 6.3 bp); "intraday" open-to-close single-stock trades on daily features with long pre-2010 samples (Ghosh et al., 2020); or forecasting volume or volatility rather than direction. The serious academic HF predictability work (Aït-Sahalia et al.; Chinco et al.) shows predictability concentrated in milliseconds to a minute and vanishing by about 5 minutes.

### Cited Findings
- **Ghosh et al.** (arXiv 2004.10178), "Forecasting directional movements of stock prices for intraday trading using LSTM and random forests": S&P 500 constituents, positions held intraday, 0.05% slippage per half-turn (0.2% per day for the long-short book). The constituents are stocks, not futures — [arXiv 2004.10178](https://arxiv.org/abs/2004.10178). Sample 1993–2018 and reported daily returns around 0.5–0.6% before costs [UNVERIFIED-memory].
- **Waldow, Schnaubelt, Krauss & Fischer** (JRFM 2021), ML statistical arbitrage in futures: daily positions, statistically significant out-of-sample break-even costs of 6.3 bp. Daily, not intraday — [IDEAS](https://ideas.repec.org/a/gam/jjrfmx/v14y2021i3p119-d516207.html) [abstract-only]
- **GCN-LSTM for ES-mini and VX futures** (arXiv 2408.05659, 2024): an ES/VX intraday forecasting model. Net-of-cost out-of-sample trading results not verified — [arXiv 2408.05659](https://arxiv.org/pdf/2408.05659) [abstract-only]
- **arXiv 2603.01820 (2026):** benchmarks deep-learning architectures on end-of-day features of futures (commodity, FX, bonds, index). End-of-day, not intraday — [arXiv 2603.01820](https://arxiv.org/pdf/2603.01820.pdf) [abstract-only]
- **Aït-Sahalia et al.** (NBER w30366): high-frequency predictability is large at the tick level but reportedly decays to a coin toss in about 5 minutes — [NBER w30366](https://www.nber.org/papers/w30366) [figures secondary]
- **Chinco et al.** (JF 2019): LASSO gains are at the 1-minute-ahead horizon and come from short-lived, sparse predictors — [NBER w23933](https://www.nber.org/papers/w23933.ack)

### Inferences
- **Red flags to apply to any ML intraday futures paper:**
  - (a) Accuracy reported instead of net PnL.
  - (b) Costs in bp that ignore ES tick size and queue position, e.g. assuming mid-fills.
  - (c) Random train/test splits or k-fold on time series, which leak information through overlapping labels.
  - (d) Hyperparameter search on the test period.
  - (e) Samples ending before 2020, or dominated by 2008–2012.
  - (f) Features from the same bar as the label, which is look-ahead.
  - (g) No comparison with a naive AR or time-of-day benchmark.
- **Consistency with our program.** With an ES 5-minute IC hurdle of about 0.17 (Q0), and given Aït-Sahalia et al.'s decay result, an ML model at 5 minutes using only public bar data is very unlikely to clear costs. At 60 minutes to 3 hours the hurdle is lower, but the sample of independent observations shrinks: about 2,500 days × 3–6 windows. Overfitting dominates unless the features are few and economically motivated.
- **A defensible ML test with free data.** A gradient-boosted model or LASSO on a small feature set:
  - lagged 15/30/60-minute returns of SPY, QQQ, IWM, TLT, HYG, UUP, GLD and VXX;
  - sector dispersion;
  - a proxy TICK;
  - time-of-day;
  - VIX/VIX3M state.
  The design: predict the next 60-minute SPY return, use walk-forward annual retraining over 2016–2026, trade only when the prediction exceeds the hurdle, and report net PnL per trade with costs from Q0. Treat a deflated Sharpe ratio below about 0.5 as noise.

### Gaps
- No 2020–2026 ES/NQ intraday ML paper with credible out-of-sample, net-of-cost trading results was found in this session. Searching arXiv titles for "E-mini" and "intraday" turned up only the GCN-LSTM paper, whose trading results were not verified.
- Original sample and return figures for Ghosh et al. not verified.
- **Data caveats.** Alpaca's free tier historically offers SIP 1-minute bars from 2016 for historical queries, with an IEX-only feed for recent or real-time data on the free plan [UNVERIFIED-memory: confirm feed and adjustment flags]. Yahoo's 1-hour bars are limited to about the last 730 days [UNVERIFIED-memory]. Neither offers NYSE TICK/ADD, VX futures or USDJPY at 1 minute.
