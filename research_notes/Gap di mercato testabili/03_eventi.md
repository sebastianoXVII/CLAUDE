# Scheduled-event intraday effects in ES/NQ and SPY/QQQ: effect sizes, decay, testability (as of Nov 2026)

> **How to read these notes.** This session's network blocked full-text retrieval from almost every research host: ijcb.org, frbsf.org, federalreserve.gov, nber.org, arxiv.org, ssrn.com (403), cxoadvisory.com, quantseeker.com, repec, ecb.europa.eu and nd.edu. Every finding below therefore comes from search-engine abstracts and snippets, not from reading the papers. Tags:
> - **[abstract]**: the claim appears in the paper's abstract or summary as returned by search.
> - **[secondary]**: a blog, practitioner site or press report.
> - **[memory, unverified]**: recalled from training. It could not be confirmed in this session and must be checked before use.
>
> **Cost hurdle, used throughout.** This is an inference from assumed index levels. A round trip costs 0.33 ES points; at ES about 6,000–7,000 that is about 0.47–0.55 bp, so 3× cost is about 1.5–1.7 bp. A round trip costs 0.45 NQ points; at NQ about 21,000–26,000 that is about 0.17–0.21 bp, so 3× cost is about 0.5–0.65 bp. **The cost hurdle almost never binds for event trades. The binding constraint is statistical power.** With N events, t = (mean/sd)·√N, so t > 3 needs mean/sd > 3/√N.
>
> | Event | Events per year | Events 2016–2026 | Required mean/sd for t > 3 |
> |---|---|---|---|
> | FOMC | 8 | ≈ 85 | ≈ 0.33 |
> | CPI alone | 12 | ≈ 125 | ≈ 0.27 |
> | CPI + NFP + PCE pooled | — | ≈ 370 | ≈ 0.16 |
> | 7 mega-caps × 4 earnings per year | — | ≈ 280 | ≈ 0.18 |
> | Quad witching | 4 | ≈ 40 | ≈ 0.47 |
> | Monthly OpEx or VIX expiration | 12 | ≈ 120 | ≈ 0.27 |
>
> Yahoo hourly ES=F/NQ=F covers about 2 years, so it holds only about 16 FOMC meetings or about 24 CPI releases. That is useless for t > 3 on any single event type. Use it only as a futures-versus-ETF sanity check.

## FOMC: 14:00 statement, 14:30 press conference reversal or continuation, pre-FOMC drift, FOMC cycle, post-announcement reversal

### Takeaway
1. **Pre-FOMC drift.** The Lucca-Moench drift (long the 24h before 14:00) has largely disappeared after 2015 in peer-reviewed work. Practitioner analyses that call it alive are weaker evidence.
2. **FOMC cycle.** The Cieslak-Morse-Vissing-Jorgensen even-week cycle fails out of sample.
3. **Post-statement reversal.** This is the most promising surviving FOMC effect. The post-statement and press-conference windows tend to *reverse* the move that came before them (the pre-announcement run-up, or the initial statement jump), most clearly in the Powell/post-COVID era.
4. **Direction is knowable before entry.** You fade the prior 24h move at about 13:50, or you fade the 14:00–14:30 move at 14:30.
5. **Effect sizes.** Bp-level effect sizes could not be extracted from the full texts. This must be tested in-house on SPY 1-minute data.

### Cited Findings
- **Original pre-FOMC drift:** Lucca and Moench (JF 2015) documented it over 1994–2011 — [ResearchGate](https://www.researchgate.net/publication/228316087_The_Pre-FOMC_announcement_drift).
  - The commonly quoted size is about 49 bp in the 24h window before 14:00, with about half of the 1980–2011 equity premium earned in that window — **[memory, unverified]** for the 49 bp figure.
  - The "half of excess return in the 24h before; post-announcement return ≈ 0" claim is restated in the Baglioni-Ribeiro thesis abstract — [Insper repository](https://repositorio.insper.edu.br/handle/11224/7532) [abstract].
- **Disappearance after 2015:** Kurov, Wolfe and Gilbert (Finance Research Letters, 2021), "The Disappearing Pre-FOMC Announcement Drift" — [RePEc](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html); [ResearchGate](https://www.researchgate.net/publication/345940053_The_Disappearing_Pre-FOMC_Announcement_Drift) [abstract].
  - The drift essentially disappeared after 2015 at meetings both with and without press conferences.
  - They link the change to lower uncertainty (VIX).
- **Counter-evidence (weaker):**
  - An Applied Economics (2024) paper finds the drift holds on press-conference days but is "not long-lasting" — [Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/00036846.2024.2322573) [abstract].
  - QuantSeeker argues the drift is "alive" and concentrated at press-conference meetings, citing Lucca-Moench's 2018 follow-up — [QuantSeeker](https://www.quantseeker.com/p/trading-the-fed-the-pre-fomc-drift) [secondary; full text not fetched, numbers unknown].
  - **The disagreement is unresolved. Treat the drift as not proven after 2015.**
- **Fade the pre-announcement move (FOMC announcement reversal):** Baglioni and Ribeiro, working paper and thesis — [Insper](https://repositorio.insper.edu.br/handle/11224/7532); [CXO summary](https://cxoadvisory.com/calendar-effects/stock-market-return-reversal-after-fomc-announcements) [abstract/secondary].
  - Data: E-mini S&P futures, 180 scheduled FOMC announcements, 1997–2020.
  - Rule: at 13:50 ET, go long if the prior-24h return was negative and short if it was positive. Exit at the close.
  - Reported Sharpe is about 2.5× the Lucca-Moench drift strategy.
  - Not peer-reviewed. Bp per trade and post-2015 sub-sample results were not retrievable.
- **Noisy FOMC returns:** Boguth, Fisher, Grégoire and Martineau, "Noisy FOMC Returns: Information, Price Pressure, and Post-Announcement Reversals" (working paper, Oct 2023 draft) — [Scribd copy of SSRN 4131740](https://www.scribd.com/document/704531555/SSRN-id4131740); [NHH seminar abstract](https://nhh.no/kalender/fin/2025-seminars/charles-martineau/) [abstract].
  - Predictive regressions estimate a **60% reversal of short-window FOMC event returns**.
  - Reversal predictors are VIX changes, abnormal volume and ETF flows.
  - Post-announcement equity returns resemble noise or overreaction more than information.
  - The exact reversal horizon (intraday or multi-day) was not visible in the snippet.
- **Press conference reverses the statement:** "The Market Impact of Fed Communications: The Role of the Press Conference" (International Journal of Central Banking, v22n1) — [IJCB PDF](https://www.ijcb.org/sites/default/files/journal/v22n1/ijcb-v22n1-market-impact-fed-communications-role-press-conference.pdf) [abstract].
  - Markets tend to move in the *opposite* direction during the press conference compared with their move after the statement.
  - The effect is driven largely by Powell's post-COVID press conferences. Earlier chairs' press conferences tended to *reinforce* the statement move.
  - Fixed schedule since March 2014: statement at 14:00, press conference at 14:30.
  - Effect sizes were not retrievable.
- **Bank research and practitioner claims on the 14:30 reversal:**
  - Citi intraday work, as reported by Investing.com: equities usually react positively to the statement and then reverse once the press conference begins — [Investing.com](https://www.investing.com/news/stock-market-news/trade-the-fomc-how-stocks-tend-to-perform-on-fed-hike-days-4903306) [secondary].
  - A trading-education site makes similar "4 stages" claims without methodology — [TOS Indicators](https://tosindicators.com/research/fomc-volatility-stages-day-trading-guide) [secondary, unverified].
- **Other FOMC communication evidence:** An SF Fed working paper (2025-30), "Financial Market Effects of FOMC Communication", is relevant, but its numbers could not be retrieved — [FRBSF](https://www.frbsf.org/wp-content/uploads/wp2025-30.pdf).
- **FOMC cycle:** Cieslak, Morse and Vissing-Jorgensen (JF 2019) find that over 1994–2016 the equity premium is earned entirely in even weeks of the FOMC cycle — [paper PDF](https://faculty.haas.berkeley.edu/morse/research/papers/cycle_paper_cieslak_morse_vissingjorgensen.pdf).
  - An Annual Review survey reports that even-week excess returns are about 12 bp per day higher than odd-week returns in the original sample — [Annual Review of Financial Economics](https://www.annualreviews.org/content/journals/10.1146/annurev-financial-090524-120826) [abstract].
- **Failed replication of the FOMC cycle:** Uppal's "Does the FOMC Cycle Still Drive Stock Returns?" replicates CMVJ and finds the cycle **no longer holds out of sample**, nor in the combined sample — [Uppal PDF](https://aliuppal.me/files/papers/Ali_Uppal_CB_Cycles.pdf) [abstract].

### Inferences
- **The FOMC cycle is dead.** The cycle is a daily, multi-week effect anyway, not an intraday one.
- **Two pre-specified, testable rules:**
  - **(A) Pre-announcement fade:** at 13:50, fade the 14:00(t−1) → 13:50(t) SPY return. Exit at 15:59.
  - **(B) Press-conference fade:** at 14:30, fade the 14:00 → 14:30 move. Exit at 15:59 or at 16:00.
  - Direction is known at entry for both.
  - Sizing: the post-14:30 window has a typical absolute move of about 30–80 bp **[memory, unverified]**. Even a 10–15 bp mean edge is more than 20× ES cost. Power is the problem: about 85 meetings need mean/sd ≥ 0.33.
  - Regime: the IJCB result says the reversal is concentrated after 2020. That is only about 50 meetings, which makes t > 3 very hard. Expect t ≈ 2 at best unless the effect is large.
- **Lower-priority checks:**
  - A pooled 2016–2026 test of the pre-FOMC drift as a decay check.
  - "FOMC day drift" (open to 14:00), which is the cash-hours portion of the drift.
- **Testability:**
  - Fully testable with Alpaca SPY/QQQ 1-minute data from 2016 (about 85 scheduled meetings). FOMC dates are on federalreserve.gov.
  - Not testable on Yahoo hourly ES/NQ. A 14:00–15:00 bar mixes the statement and the press conference, and there are only about 16 meetings.
- **Search for the drift-interaction filter before running it.** The predictors in Boguth et al. (VIX change, volume, ETF flows) suggest conditioning the fade on a VIX change between 14:00 and 14:30. This adds degrees of freedom, so pre-register it.

### Gaps
- No bp effect sizes or t-stats for the 14:30 reversal, the Baglioni-Ribeiro strategy (post-2015 sub-sample) or the reversal horizon in Boguth et al. The full texts were blocked; the IJCB and FRBSF PDFs are the first to read once the hosts are allowed.
- QuantSeeker's "drift is alive" numbers are unknown.
- No post-2020 study found that cleanly measures "post-announcement drift" (continuation from 14:30 to the close or to day t+1) in ES. The literature here mostly finds reversal, not drift.

## CPI, NFP and PCE at 08:30 ET: first 1–60 minutes of the cash session after a big surprise

### Takeaway
1. **Price discovery is fast.** Futures jump within minutes of the 08:30 surprise (ABDV). The best recent evidence on drift is negative: once the initial spike bars are excluded, there is no persistent post-news drift in micro Nasdaq futures, 2022–2025.
2. **Overreaction.** There is some evidence of overreaction to high-attention releases (CPI in 2021–2023), which suggests reversal rather than continuation. There is also asymmetry: downside CPI surprises produced significant gains, while upside surprises produced smaller declines that were not reliably significant.
3. **Overall.** A post-08:30 continuation rule is unlikely to work. A "fade the 08:30–09:30 move during the cash session" rule is a plausible but unproven hypothesis.

### Cited Findings
- **Andersen, Bollerslev, Diebold and Vega (2007), "Real-time price discovery in global stock, bond and foreign exchange markets"** (J. International Economics 73(2)) — [Fed IFDP 871](https://federalreserve.gov/econres/ifdp/real-time-price-discovery-in-global-stock-bond-and-foreign-exchange-markets.htm); [CREATES WP](https://repec.econ.au.dk/repec/creates/rp/07/rp07_20.pdf) [abstract].
  - Uses S&P 500 futures.
  - News surprises produce conditional-mean *jumps*.
  - The equity response depends on the business cycle: bad news is positive in expansions and negative in recessions.
  - Futures lead cash, because most releases come at 08:30 while cash equities are closed.
- **Investor attention and CPI:** Kroner (Fed FEDS 2025-022), "How Markets Process Macro News: The Importance of Investor Attention" — [FEDS PDF](https://www.federalreserve.gov/econres/feds/files/2025022pap.pdf); [FEDS summary](https://www.federalreserve.gov/econres/feds/how-markets-process-macro-news-the-importance-of-investor-attention.htm) [abstract].
  - Uses intraday data.
  - Yields and inflation expectations reacted far more strongly to CPI surprises during the 2021–2023 surge. Reactions to other releases were roughly unchanged.
  - Markets tend to **overreact to high-attention announcements**.
- **CPI asymmetry:** "Asymmetric S&P 500 reactions to CPI surprises in a high-inflation environment" (Applied Economics Letters, 2026) — [Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/13504851.2026.2624038) [abstract only].
  - Sample: 2021–2025, core CPI.
  - Downside surprises produced significant gains. Upside surprises produced smaller declines that were not reliably significant.
- **Pre-announcement drift (before 08:30):** Kurov, Sancetta, Strasser and Wolfe (ECB WP 1901), "Price drift before U.S. macroeconomic news" — [ECB WP 1901](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1901.en.pdf); [earlier draft](https://pages.stern.nyu.edu/~jh4/SternMicroMtg/Old/SternMicroMtg2015/Papers/Preannouncement_042015Strasser.pdf) [abstract].
  - Uses E-mini S&P and 10-year T-note futures, Jan 2008 – Mar 2014.
  - There is significant pre-announcement drift for some releases and none for others. It was stronger after 2008.
  - The drift starts minutes before the release, so it is not tradable by an ETF trader in the cash session.
- **Overnight returns before releases:** Hu, Pan, Wang and Zhu (draft) report large overnight returns before releases such as NFP and ISM — [MIT PDF](https://www.mit.edu/~zhuh/HuPanWangZhu_preannouncement.pdf) [abstract].
- **No post-news drift, 2022–2025:** "Structural Limits of OHLCV-Based Intraday Momentum Signals in MNQ Futures: A Systematic Falsification Study" (arXiv 2605.04004, 2026) — [arXiv](https://arxiv.org/pdf/2605.04004) [abstract/snippet; not peer-reviewed].
  - Covers high-impact USD events (including NFP and CPI), 2022–2025.
  - **No persistent post-news drift once the initial spike bars are excluded.**
  - This is a failed or negative result directly relevant to our program.
- **Anecdotal intraday reversal, 13 Oct 2022 (hot CPI):**
  - ES fell about 3% after the release, then the S&P closed +2.6% from an intraday low of −2.39% — [iVolatility](https://www.ivolatility.com/news/2775); [investingLive](https://investinglive.com/technical-analysis/what-are-the-day-major-indices-reverse-sharply-to-the-upside-20221013/) [secondary].
  - Counter-example of continuation: on 10 Nov 2022 (soft CPI, 7.7% vs 8.0% expected) the S&P ended about +5.4%, and on 13 Sep 2022 (hot CPI) about −4.4% — [Spokesman/AP](https://www.spokesman.com/stories/2022/nov/10/stocks-spike-by-most-in-two-years-on-cpi-relief/) [secondary].
  - Big surprises can therefore produce either full-day continuation or reversal.
- **Gürkaynak et al. (high-frequency surprise identification):** not retrieved in this session.

### Inferences
- **The direction is knowable before entry only as "the sign of the 08:30–09:30 move".** A true surprise measure needs consensus forecasts, which are not available in free data. Use the futures or ETF move itself as the surprise proxy.
- **Candidate rule.** At 09:30 (or 09:35/09:45), trade *against* the 08:30–09:29 SPY pre-market move when |move| > k·σ. Exit at 10:30, 12:00 or the close.
  - The asymmetry paper suggests splitting by sign: up-moves after soft prints may persist more than down-moves.
  - Pooling CPI, NFP and PCE gives about 370 events. That makes t > 3 reachable at mean/sd of about 0.16. CPI alone has about 125 events.
- **Mind the 2016–2026 sample.**
  - 2016–2020 was a low-sensitivity regime for equities to CPI.
  - 2021–2023 was high attention. Kroner implies overreaction, and so reversal, should be strongest then.
  - Expect regime-dependence. A full-sample t > 3 is uncertain.
- **Data caveats:**
  - SPY pre-market 1-minute bars (04:00–09:30) on Alpaca exist but are thin, especially before 2020. Use the first cash prints or the 09:30–09:35 open as the reference.
  - Yahoo hourly ES gives only about 24 CPI releases over 2 years, which is not enough. ES's 08:00–09:00 hourly bar would also blend pre-release and post-release prices.
- **Cost hurdle.** A 10 bp mean is about 20× ES cost.

### Gaps
- No peer-reviewed 2022–2026 study found that quantifies post-08:30 drift or reversal in ES/NQ in bp at 15/30/60-minute horizons.
- The Gürkaynak-Sack-Swanson style surprise-based intraday equity studies were not retrieved.
- PCE-specific evidence: none found. PCE is lower-attention, so smaller and less predictable effects should be expected.

## Treasury auctions (13:00 ET results) and spillover to equities

### Takeaway
No study was found that measures intraday equity (ES/SPY) reactions to 13:00 auction results or tails. Evidence is anecdotal. This is an open hypothesis, not a documented effect.

### Cited Findings
- **Definition of the tail:** high yield minus the when-issued yield at about 13:00 — [yieldcurve.pro](https://www.yieldcurve.pro/learn/treasury-auction) [secondary].
- **Supply shocks:** "U.S. Treasury Auctions: A High Frequency Identification of Supply Shocks" (AEA 2022 session paper) — [AEA](https://www.aeaweb.org/conference/2022/preliminary/paper/Gr5d93YA) [abstract fragments].
  - Identifies supply shocks from futures moves around auction *announcements*.
  - A net increase in supply is perceived as good news for stocks and lowers volatility.
  - It does not study the 13:00 result window.
- **Pandemic-era auctions:** stresses but "few surprises" — [Dallas Fed](https://www.dallasfed.org/research/economics/2021/0831) [secondary].
- **Anecdotes:**
  - A Substack claims the S&P 500 fell 60 points in 10 minutes after a weak auction — [Substack](https://whatworksintrading.substack.com/p/how-a-secret-bond-market-signal-predicts) [secondary, unverified].
  - A recent 3-year auction had little market impact — [ZeroHedge/Newsquawk](http://www.zerohedge.com/markets/stocks-rally-rebound-continues-while-crude-drops-usiran-optimism-newsquawk-us-market-wrap) [secondary].

### Inferences
- **Testability:**
  - About 10–12 long-end (10y/30y) auctions per year: 2016–2026 gives about 110–130 10y/20y/30y auctions, or about 400+ including 2y/5y/7y.
  - Tails need the when-issued yield, which is not free. Possible proxy: the TLT/IEF 1-minute move from 13:00 to 13:05 on Alpaca. Actual high yields are free from TreasuryDirect.
  - Rule to test: the SPY return from 13:05 to 13:30/14:00/close, conditional on the sign of the 13:00–13:05 TLT move.
- **Direction is knowable** only after the first minutes (sign of the bond move).
- **Prior:** small effects. Most auctions are non-events, and auction days overlap with FOMC and CPI weeks, so those must be excluded.

### Gaps
- No academic or Fed study found on 13:00 auction-result spillover to equity index futures. The evidence base here is essentially empty.

## Mega-cap earnings after the close (NVDA, AAPL, MSFT, META, AMZN, GOOGL, TSLA) and the next-day NQ open

### Takeaway
The academic evidence shows that bellwether earnings move the index, and that announcers' returns carry market-wide information. However, the index-level spillover has *declined* over 2004–2021, by one version of the key paper. No study was found on whether the next-day cash open continues or reverses the overnight move. Untested hypothesis, but well suited to free data.

### Cited Findings
- **Savor and Wilson (JF 2016), "Earnings Announcements and Systematic Risk"** — [vLex](https://law-journals-books.vlex.com/vid/earnings-announcements-and-systematic-855658475); [2011 draft](https://faculty.wharton.upenn.edu/wp-content/uploads/2012/04/Draft20111215p_edited.pdf) [abstract].
  - Firms scheduled to announce earn about 9.9% annualized abnormal return.
  - Announcers' returns forecast aggregate earnings growth.
- **Bellwether firms:** market-level effects are largest for large, highly correlated firms. Realized market returns are higher around their announcements — [UChicago dissertation](https://knowledge.uchicago.edu/record/163/files/Lombardi_uchicago_0330D_14112.pdf) [secondary summary].
- **Ogneva, Xia and Ye, "What moves the market?"** — [ScholarSpace](https://scholarspace.manoa.hawaii.edu/handle/10125/77070); [AUT version](https://acfr.aut.ac.nz/__data/assets/pdf_file/0012/686748/2b-Jingjing-Xia.pdf) [abstract].
  - Uses index futures with narrow intraday and overnight windows.
  - Large firms' earnings spill over to the index.
  - The aggregate market reaction **declined over 2004–2021**. An earlier 2004–2018 version described the contribution as *stable*, so the versions conflict.
- **Mechanics:** NQ/ES absorb after-hours earnings between 16:00 and 20:00 ET, and that move sets the next-morning gap — [TradingNewsTerminal](https://www.tradingnewsterminal.com/after-hours-earnings-tracker) [secondary].
- **Gap fades:** a blog claims moderate SPY/QQQ gaps of 1–2% fade partially more often, while very large gaps go either way — [SharePlanner](https://www.shareplanner.com/blog/strategies-for-trading/fading-the-gap-how-large-overnight-moves-in-spy-and-qqq-play-out-during-the-trading-day.html) [secondary, no stated sample].

### Inferences
- **Gap fill is already dead in our program**, so test only the *event-conditioned* version:
  - QQQ open to 10:00/10:30/close after a mega-cap report with |after-hours stock move| > X%.
  - Condition on the sign and size of the QQQ (or NQ) 16:00 → 09:29 move.
  - Also test whether the stock's own overnight-to-open move predicts QQQ's intraday move (lead-lag from the stock to the index).
- **Power:** about 280 events from 2016 to 2026. The mega-cap weight in QQQ has grown sharply since 2020, so the effect is non-stationary.
- **Data:**
  - Alpaca 1-minute bars include extended hours for both QQQ and the individual stocks, so this is testable.
  - Earnings dates and BMO/AMC timing must come from a free calendar (Nasdaq or Yahoo). Check AMC timing precisely, since AAPL, AMZN and META report at 16:30.
  - NQ hourly over 2 years gives about 56 events, enough only for a sanity check.

### Gaps
- No academic or practitioner statistic found on continuation versus reversal of the overnight QQQ/NQ move after mega-cap earnings.
- No study on NVDA-specific index impact.

## VIX expiration, monthly OpEx (Wednesday/Friday) and quad witching

### Takeaway
1. **Monthly OpEx week:** no reliable edge in recent long samples.
2. **Quad witching:** slightly better (secondary data only, about 40 quarterly events, so t > 3 is nearly impossible).
3. **Expiration-day reversals:** documented only in old (1980s–90s) data under PM settlement.
4. **VIX expiration (Wednesday):** no study found.
5. **Mechanism:** dealer hedging around the third Friday exists, but it does not translate into a clean intraday rule.

### Cited Findings
- **OpEx weeks, 2006–2026:** TradeIntel's backtest of 239 monthly OpEx weeks (Sep 2006 – Jul 2026) — [TradeIntel](https://tradeintel.ca/research/spx-monthly-opex-week.html) [secondary].
  - SPX was up in 57.3% of weeks, with a median of +0.19%: "the same as any other week."
  - Quad witching weeks: 63.7% up, median +0.69%.
- **Older backtests:** positive OpEx-week returns, but the effect is fading in recent years. Expiration day itself is weak (51.4% win rate, negative compounded returns on SPY) — [QuantifiedStrategies](https://www.quantifiedstrategies.com/options-expiration-week/); [Substack](https://quantifiedstrategies.substack.com/p/the-options-expiration-week-effect-e2a) [secondary].
- **Morning-after reversal (old data):** Stoll and Whaley (1987, FAJ) found the reversal on the morning after expiration averaged about 0.4% of the index in the 10 most recent quarterly expirations (mid-1980s) — [CFA Institute](https://rpc.cfainstitute.org/research/financial-analysts-journal/1987/program-trading-and-expiration-day-effects) [abstract via search].
  - A later FAJ (1991) piece, "Expiration-day effects: what has changed" — [CFA Institute](https://rpc.cfainstitute.org/research/financial-analysts-journal/1991/expiration-day-effects-what-has-changed).
  - Hancock (1993) found no difference after June 1987 [via search summary].
  - These are pre-AM-settlement effects and are obsolete for today's market structure.
- **Stoll and Whaley (1990), Monday reversal:** stocks falling in the last half hour on Friday rise at Monday's open. They attribute it mostly to bid-ask bounce — [RePEc](https://ideas.repec.org/a/ucp/jnlbus/v63y1990i1ps165-92.html) [abstract].
- **Day-before/day-after pattern:** Vipul (2005), as summarized by CESifo, finds negative returns the day before expiration and a significant reversal the next day — [CESifo WP 9360](https://cesifo.org/DocDL/cesifo1_wp9360.pdf) [abstract].
  - Index-level reversal was absent in Polish indices (Suliga 2017) — [RePEc](https://ideas.repec.org/a/agh/journl/v18y2017i2p201-225.html).
- **Mechanism:** Baltussen, Terstegge and Whelan, "The Derivative Payoff Bias", on market-maker hedging flows around expiry — [AFA](https://afajof.org/management/viewp.php?n=98196) [abstract].

### Inferences
- **Testability:** expiration dates are deterministic and SPY 1-minute data covers them, so this is trivially testable. Power:

  | Event | Events 2016–2026 | Comment |
  |---|---|---|
  | Monthly OpEx | ≈ 120 | Testable |
  | VIX Wednesday expiration | ≈ 120 | Testable |
  | Quad witching | ≈ 40 | Weak; t > 3 needs mean/sd ≈ 0.47 |

- **Rules to try**, with direction knowable at entry:
  - Fade the Thursday-to-Friday-11:00 move on OpEx Friday.
  - Fade the OpEx-Friday close-hour move into Monday's open.
  - Since 2022–2023, daily 0DTE options have diluted the monthly OpEx concentration. That is a likely reason for decay; expect a weaker effect after 2022.

### Gaps
- No academic study found on VIX-expiration (Wednesday, SOQ) effects on SPX/ES intraday returns.
- No modern (post-2015) peer-reviewed SPY intraday OpEx study found. Caporale and Plastun (2021) on US witching days were found, but their results were not retrieved.

## Day after extreme moves (|return| > 2σ): next-day intraday reversal or continuation

### Takeaway
1. **Opening reversal:** intraday, there is old but solid evidence that large *opening* moves in S&P futures partly reverse within 30–60 minutes.
2. **Next-day reversal:** the evidence is weak and mixed. Streak and one-day-abnormal-return effects are "not reliably exploitable", with one unverified journalist statistic.
3. **Mechanism:** conditioning on hedging pressure or the vol regime (next section) is the more promising angle.

### Cited Findings
- **Opening reversal:** "Intraday price reversals in the US stock index futures market: A 15-year study" — [ResearchGate](https://www.researchgate.net/publication/222520781_Intraday_price_reversals_in_the_US_stock_index_futures_market_A_15-year_study) [abstract].
  - Large S&P 500 futures price changes in the opening session are followed by significant reversals in the first 30–60 minutes.
  - Authors and journal are believed to be Fung, Mok and Lam, J. Banking & Finance, around 2000 **[memory, unverified]**.
- **Large vs small moves:** the sign of returns tends to reverse after large moves and continue after small ones — [arXiv 2501.16772](https://arxiv.org/pdf/2501.16772) [abstract].
- **End-of-day moves:** next-day returns are higher after large high-to-close changes in Dow stocks, but evidence for price effects after one-day abnormal returns in the US market is weak — [Economics Letters (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0165176512005666) [abstract].
- **Streaks:** little support for exploitable reactions after daily winning or losing streaks — [CXO Advisory](https://www.cxoadvisory.com/technical-trading/trade-stock-market-streak-reversals/) [secondary].
- **Journalist statistic (since 1997):** after S&P futures erased a drop of 2% or more intraday, they fell the next day nearly 2 of 3 times — [Yahoo Finance](https://finance.yahoo.com/markets/article/stocks-shrugged-off-the-blue-wave-overnight--history-says-dont-trust-the-bounce-yet-153846605.html) [secondary, unverified methodology].

### Inferences
- **Testable** with SPY/QQQ 1-minute data. Define σ on a trailing 20- or 60-day realized basis. Expect about 5–7% of days beyond ±2σ under fat tails, so about 125–175 events from 2016 to 2026.
- **Rule:** at 09:30 + N minutes on day t+1, trade with or against the day-t sign. Split by the sign of day t: crash-day rebounds versus up-day extremes behave differently.
- **Overlap with dead strategies.** Overlap with "gap fill" is high, since t+1 gaps are large after extreme days. Make sure the test is not a relabelled gap fill.

### Gaps
- No modern (post-2010) peer-reviewed study of next-day *intraday* behaviour in ES/NQ conditional on a >2σ prior day.

## High-volatility regime conditioning: does intraday momentum or reversal flip with VIX, realized vol or gamma?

### Takeaway
1. **What conditions the effect:** Baltussen et al. (JFE 2021) find that market intraday momentum (rest-of-day predicting the last 30 minutes) is present **only on negative-gamma (NGE < 0) days** and absent on positive-gamma days. It also reverts over the following days.
2. **Fit with our result:** this matches our finding of last-half-hour momentum only in 2020, a deeply negative-gamma, high-vol year. The literature conditions on *gamma or hedging pressure*, not on VIX per se.
3. **Original effect:** Gao et al. (JFE 2018) find it out of sample through 2013. Practitioner replications show tiny R² (about 1–2%) and economic sizes too small after frictions.
4. **Replications:** no rigorous VIX-conditioned replication after 2018 was found.

### Cited Findings
- **Baltussen, Da, Lammers and Martens, "Hedging Demand and Market Intraday Momentum"** (JFE 142(1), 2021, pp. 377–403) — [EUR Pure](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/); [working paper PDF](https://www3.nd.edu/~zda/intramom.pdf); [RePEc](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403) [abstract].
  - Data: 60+ futures, 1974–2020.
  - The last-30-minute return is predicted by the rest-of-day return, and the predictability reverts over subsequent days.
  - S&P momentum is present when NGE < 0, gets stronger as NGE becomes more negative, and is insignificant when NGE > 0.
  - Secondary commentary: the natural trade is to provide liquidity in anticipation of hedging flows — [Alpha Architect](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/); [Harbourfront Quant](https://harbourfrontquant.substack.com/p/market-intraday-momentum-and-hedging) [secondary].
- **Gao, Han, Li and Zhou, "Market Intraday Momentum"** (JFE 129(2), 2018) — [RePEc](https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414); [Alpha Architect](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/) [abstract/secondary].
  - Data: SPY, 1993–2013.
  - The first half-hour predicts the last half-hour, with OOS R² of about 1.4% (2.0% combined with the 12th half-hour).
  - The effect is stronger on high-volatility days **[memory, unverified in-session]**.
- **Practitioner replication:** CXO's 2012–2014 check (441 days) found R² of about 0.014, and last-half-hour returns after extreme first half-hours were "too small to exploit after frictions" — [CXO](https://cxoadvisory.com/calendar-effects/first-and-last-half-hours-of-trading-linked) [secondary]. **This is a weak replication: the economics fail.**
- **International replication:** first half-hour predictability holds in 12 of 16 developed markets, with OOS power in most — [Reading accepted version](https://reading-9.eprints-hosting.org/95566/1/Accepted-Version.pdf); [Nottingham repository](https://nottingham-repository.worktribe.com/OutputFile/5273196) [abstract].
- **Independent falsification (MNQ):** the MNQ study (arXiv 2605.04004, 2026) tests OHLCV intraday momentum signals and reports structural limits, a negative result — [arXiv](https://arxiv.org/pdf/2605.04004) [abstract].
- **VIX bands (practitioner):** a blog claims intraday reversals are "sharper" at VIX 20–30 and "shallow" below 15. It defines a regime as 5 consecutive closes in the band — [Volatility Box](https://volatilitybox.com/research/volatility-regimes-explained/) [secondary, unverified, no statistics].
- **Opening reversals:** the 15-year S&P futures study documents opening reversals (see the previous section), consistent with liquidity provision in calmer regimes — [ResearchGate](https://www.researchgate.net/publication/222520781_Intraday_price_reversals_in_the_US_stock_index_futures_market_A_15-year_study).

### Inferences
- **Our "only in 2020" result is consistent with Baltussen et al.** Momentum should appear only on negative-gamma days. Conditioning on VIX is a crude proxy, because high VIX correlates with dealer short gamma, but the mapping is not one-to-one.
- **Free test:** condition last-half-hour momentum on:
  - VIX above its 1-year median;
  - VIX term-structure inversion (VIX/VIX3M > 1, free on Cboe);
  - |rest-of-day return| > 1σ;
  - and, if a free gamma proxy exists, SqueezeMetrics GEX. A free DIX/GEX CSV history may exist; that is **[memory, unverified]**.
- **Risk of overfitting.** Pre-register a single conditioning variable, because subsample mining after a dead full-sample result is a classic overfitting trap.
- **Event counts:** negative-gamma or high-VIX days are about 15–25% of 2016–2026, so roughly 400–600 days. Power is adequate if the effect is real.
- **Alternative trade (Baltussen's "next days revert" leg):** in high-VIX regimes, fade the last-30-minute move into the next morning. This overlaps the overnight drift already found dead, so check before investing time.

### Gaps
- No peer-reviewed, post-2018 VIX-conditioned replication of US market intraday momentum found.
- No free historical NGE/GEX series confirmed in-session.
- Gao et al.'s exact high-volatility conditional coefficients were not retrieved.
- **Network note for follow-up.** These hosts were blocked in this session and need allow-listing to verify numbers: ijcb.org, frbsf.org, federalreserve.gov, nber.org, arxiv.org, papers.ssrn.com, cxoadvisory.com, quantseeker.com, ideas.repec.org, ecb.europa.eu, www3.nd.edu.
