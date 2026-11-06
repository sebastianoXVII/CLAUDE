# Futures prop firms (evaluation/funded model): rules, statistics, regulation, and real CME trading costs — as of 2026-11-06

**How these notes were researched (read first):** Notes written 2026-11-06. In this session, WebFetch could not reach any of the official domains I tried: topstep.com help center, databento.com, interactivebrokers.com, and the third-party guides il.ly, phidiaspropfirm.com and tradecovex.com all failed with DNS errors because they are outside the session's allowed network. So **nearly every figure below comes from search-engine summaries of mostly third-party, often affiliate-linked, review sites dated July–November 2026**. Two exceptions are closer to primary sources: the Tradeify commission schedule on help.tradeify.co and the Topstep Express Funded rules page on topstep.com. Both were seen only as search snippets. Prop rules change often, sometimes several times a year. **Check every number against the firm's official help center before buying an account.** If the official sources need fetching, these domains must be added to the session's allowed network: help.topstep.com, apextraderfunding.com, databento.com and cmegroup.com.

## Q1. Current rules per firm: the comparison table

### Takeaway
By late 2026 the market has settled on a $3,000 target and roughly a $2,000 drawdown for a 50K account, a 90/10 split (sometimes 100% on the first slice), and payouts after about 5 winning days. The firms differ mainly on four things: monthly vs one-time fees, intraday vs end-of-day (EOD) trailing drawdown, consistency rules, and the cap on funded accounts. 2026 brought major overhauls at Apex (4.0, March 1 2026) and Topstep (90/10 split from January 12, new payout paths from February 5, lower caps from April 28).

### Table (50K account unless noted; all from third-party summaries unless stated)

| Firm | Sizes | Eval cost | 50K target | Drawdown (type / 50K amount) | Daily loss limit | Consistency | Payout rules | Split | Max funded accounts | Automation / copy trading |
|---|---|---|---|---|---|---|---|---|---|---|
| **Topstep** | 50K/100K/150K | Monthly: $49/$99/$199 + $149 activation (Standard), or $95/$149/$229 with no activation fee | $3,000 (100K $6,000; 150K $9,000) | Max Loss Limit $2,000 (100K $3,000; 150K $4,500), EOD trailing | Optional on Combine and Express Funded Account (XFA) | Best day ≤50% (Combine; some sources say 55%) | Two paths since 2026-02-05: Standard (5 days ≥$150) or Consistency (3 days, ≤40%). Caps lowered 2026-04-28 (reported $2,000/$3,000 on new 50K/100K no-activation-fee Combines; sources conflict). After the first payout, the Max Loss Limit is set to $0 | 90/10 for traders who joined on or after 2026-01-12 | **5 XFAs** (official page) | Bots allowed via the TopstepX/ProjectX API ($29/month); reportedly no VPS and no API on Live Funded. Copying across your own accounts is allowed |
| **Apex Trader Funding (4.0, since 2026-03-01)** | 25K/50K/100K/150K (250K/300K dropped) | Not confirmed (3.0 was monthly; check 4.0) | not confirmed | EOD or intraday versions; Safety Net threshold (50K reportedly $52,600) | not confirmed | 50% single-day cap on new Performance Accounts (PAs), up from 30% | 5 qualifying days (≥$250/day EOD 50K; $200 intraday); minimum $500 per request; maximum 6 payouts per PA with a rising ladder (example for 100K: $2,000 → $4,000) | Conflicting: 100% of the first $25K then 90/10, or a flat 100% | **20 active PAs per household** | Fully automated bots reportedly banned (manual or semi-auto only). Copier allowed across your own PAs. Hedging banned |
| **Tradeify** | 25K–150K; Growth / Select / Lightning plans | One-time; Growth 50K $139–$145 | $3,000 | $2,000 EOD trailing | Growth 50K $1,250 (25K $600) | Growth: none in eval, 35% funded; Select: 40% in eval | Reportedly 5 days ≥$150 (unconfirmed) | 90/10 | **5 funded** (all plans combined, per person/household); evals unlimited or not stated | Copy trading allowed on your own accounts (details not verified) |
| **Lucid Trading** | 25K–150K; LucidFlex / LucidPro | One-time; ~$130 (Flex 50K) to $185 (Pro 50K) | $3,000 (25K $1,250) | $2,000 EOD trailing | None on 25K | Pro: none in eval, 40% funded; Flex: 40% in eval | Payout at profit goal above a buffer | 90/10 | **5 funded per household**; 10 evals; 10 accounts total; deleted after 30 days of inactivity | Reportedly now allows automation (single source) |
| **My Funded Futures (MFFU)** | 25K–150K; Rapid / Builder plans | not confirmed | not confirmed | not confirmed | not confirmed | not confirmed | not confirmed | not confirmed | **5** if all accounts are 25K/50K; **3** if any is 100K/150K; Rapid EOD 3; Builder 50K 1 | Copying across your own accounts generally allowed |
| **Take Profit Trader** | 25K–150K | Monthly; 50K Test $170/month | $3,000 | $2,000 EOD trailing ($1,500–$4,500 by size) | None reported | not confirmed | not confirmed | 80/20 (Test/PRO); 90/10 (PRO+) | 5 funded (comparison tables) | not confirmed |
| **Alpha Futures** | Zero / Premium / Advanced / Standard plans | Standard 50K $129/month, $0 activation | not confirmed | EOD trailing; floor reportedly fixed at $47,500 | not confirmed | not confirmed | not confirmed | 90% | 5 Standard accounts (bought since 27 July) | not confirmed. **Premium plan closed July 2026 without honoring pending payouts** |
| **Bulenox** | 25K–150K; Qualification / Fast Track / Momentum | One-time; 50K $143–$175, plus a $148 Master activation fee | not confirmed | $1,500/$2,500/$3,000/$4,500 (25K–150K), trailing or EOD option | 50K Option 2: $1,100 | not confirmed | Weekly (marketing claims 7-day payouts) | Conflicting: 90% (100% of the first $10K) vs 80% | 5 Master accounts; Qualification unlimited | Bots and copiers allowed if user-built for personal use; commercial or shared bots banned |

### Cited Findings
- **Apex 4.0** launched 2026-03-01 as a full product replacement; it offers 25K/50K/100K/150K sizes and dropped 250K/300K — [phidiaspropfirm (search summary)](https://phidiaspropfirm.com/education/apex-trader-funding-4-0-explained); [QuantVPS](https://www.quantvps.com/blog/apex-pa-account-rules)
- Apex: 20 active PAs per household; 5 qualifying days (≥$250 on 50K EOD, $200 intraday); minimum $500 request; Safety Net (50K at $52,600); 50% consistency for new PAs (was 30%); maximum 6 payouts per PA with a ladder (100K: $2,000, $2,500, $3,000, $3,000, $3,500, $4,000); legacy accounts bought before March 2026 keep the old rules — [propfirmsfinder](https://propfirmsfinder.com/prop-firm/apex-trader-funding/payouts/); [copilink (Nov 2026)](https://copilink.com/prop-firms/apex-trader-funding); [damnpropfirms](https://damnpropfirms.com/trading-guides/apex-trader-funding-profit-target-and-payout-ladder-rules-2026/); [lunefi](https://lunefi.com/blog/apex-trader-funding-complete-guide-to-rules-and-payouts)
- Apex split is **conflicting**: "100% of the first $25,000 then 90/10" vs a flat 100% — [h2tfunding](https://h2tfunding.com/apex-trader-funding-payout-rules/); [rbtrading](https://rbtrading.site/prop-firms/apex-trader-funding-rules)
- **Topstep** Standard path: $49/$99/$199 per month (50K/100K/150K) plus a $149 activation fee; no-activation-fee option $95/$149/$229; targets $3K/$6K/$9K; Max Loss Limit $2K/$3K/$4.5K; Daily Loss Limit optional — [proptradingvibes](https://proptradingvibes.com/blog/topstep-trading-combine-rules); [satotrades](https://satotrades.com/guides/topstep-rules)
- Topstep: 90/10 split for traders who joined on or after 2026-01-12; Standard (5×$150) and Consistency (3 days, 40%) payout paths since 2026-02-05; payout caps cut 2026-04-28; consistency is 50% vs 55% depending on the source — [tradecovex (search summary)](https://tradecovex.com/guides/topstep-rule-changes-2026); [stonkjournal](https://stonkjournal.com/articles/topstep-review); [tradebb](https://www.tradebb.ai/blog/topstep-rules)
- Topstep: "You can have up to 5 active Express Funded Accounts at one time. This number may change depending on your activity or participation in other Topstep programs" (official page, indexed version about 500 days old) — [Topstep XFA rules](https://www.topstep.com/express-funded-account-rules)
- Topstep API: $29/month (Live Funded account not supported) — [pickmytrade blog](https://blog.pickmytrade.io/topstep-api-getting-a-key-and-placing-your-first-automated-trade/); [pickmytrade FAQ](https://pickmytrade.trade/prop-firm-faq/topstep-faq/)
- **Account caps:** Lucid 5 funded / 10 eval / 10 total per household; Tradeify 5 funded across all plans; MFFU 5 (or 3 if any 100K/150K; Rapid EOD 3; Builder 50K 1) — [tradedupe](https://tradedupe.com/compare/tradeify-vs-lucid-trading); [bestprops](https://bestprops.com/rules/lucid-trading-rules/); [funded.now](https://funded.now/compare/lucid-trading-vs-tradeify); [lucidtrading.com](https://lucidtrading.com/)
- **Tradeify / Lucid** plan details (prices $139–$185, $2,000 EOD drawdown, consistency 35–40%, 90/10 split) — [propfirmgorilla](https://propfirmgorilla.com/blog/lucid-lucidpro-50k-vs-tradeify-growth-50k); [proptradingvibes](https://proptradingvibes.com/blog/lucid-trading-vs-tradeify); [damnpropfirms](https://damnpropfirms.com/trading-guides/tradeify-vs-lucid-trading/)
- **Bulenox, Take Profit Trader, Alpha Futures** figures as in the table — [QuantVPS Bulenox](https://www.quantvps.com/prop-firms/bulenox); [tradingfinder](https://tradingfinder.com/props/bulenox/rules/); [funded.now](https://funded.now/compare/bulenox-vs-takeprofit-trader); [pickmytrade TPT FAQ](https://pickmytrade.trade/prop-firm-faq/take-profit-trader-faq/); [tradetanto Alpha](https://tradetanto.com/learn/alpha-futures-rules-every-plan-rule-and-limit); [propscope](https://propscope.net/en/compare/bulenox-vs-alpha-futures/)

### Inferences
- The fee model matters for us. With a monthly fee (Topstep, Take Profit Trader, Alpha Futures), every month spent in evaluation costs money. A one-time fee (Tradeify, Lucid, Bulenox) suits a system that may need many attempts.
- An EOD trailing drawdown is far more forgiving for intraday strategies with large open-trade excursions (MAE) than an intraday trailing drawdown. Prefer EOD plans.
- Consistency rules of 35–50% penalize strategies whose P&L comes from a few big days, which is typical of breakout and trend systems.

### Gaps
- No official help-center pages could be read, so every rule is unverified at the primary source.
- Apex 4.0 evaluation pricing, target and drawdown amounts were not found. Full MFFU rules were not found.
- No information was found on news-trading restrictions, beyond the general point that Tier-1 news (FOMC, CPI, NFP) is restricted at some firms; not verified per firm.

## Q2. Pass rates, payout statistics and the business model

### Takeaway
The only firm-level disclosures found are Topstep's for 2025: 16.8% of Combines passed, 51.8% of people passed at least one Combine, 33.3% of funded-level traders got a payout, and 0.71% of XFA traders were moved to Live. Tradeify reports a 17.2% eval pass rate. The industry estimate of about 7% of all traders ever receiving a payout comes from an FPFX dataset, which mostly covers forex. The model is funded mainly by evaluation fees, with payouts as a cost.

### Cited Findings
- Topstep 2025: "16.8% of all Trading Combines initiated were successfully completed"; 51.8% counted per person; 33.3% of funded-level traders received a payout; 0.71% of XFA traders moved to a Live Funded Account — [alphaexcapital](https://www.alphaexcapital.com/prop-trading/topstep-review); [proptradingvibes](https://proptradingvibes.com/blog/is-topstep-legit); [audacity.capital](https://audacity.capital/trading-guides/prop-firm-pass-rate/); [fortunly](https://fortunly.com/statistics/prop-firm-challenge-pass-rate-statistics/)
- Tradeify: 17.2% pass rate for evals started August 2025 to July 2026. Across the three futures firms that publish a per-person payout rate, 28.5%–39.2% of funded traders received at least one payout — [il.ly (search summary)](https://il.ly/blog/prop-firm-pass-rates); [Tradeify blog](https://tradeify.co/post/futures-prop-firm-statistics-2026)
- Industry estimate (FPFX, more than 300,000 accounts): about 7% of all traders ever receive a payout; about 45% of funded traders get at least one; average payout about 4% of account size — [statistics.ge](https://statistics.ge/prop-firm-statistics); [atmosfunded](https://atmosfunded.com/prop-firm-statistics/)
- Counterpoint: no futures firm publishes an audited pass rate; most figures are estimates — [TraderPayout](https://traderpayout.com/prop-firms/prop-firm-pass-rate)

### Inferences
- Rough funnel at Topstep: 16.8% of Combines pass, then about a third of funded traders get paid. That puts roughly **5–6% of Combines leading to at least one payout** (my calculation: 0.168 × 0.333, though the denominators differ).
- The business is profitable if fees collected exceed payouts plus costs. The 2026 squeeze (lower payout caps, 90/10 splits, a maximum of 6 payouts at Apex, Live promotion at 0.71%) shows firms protecting their margin.
- Funded accounts are almost always simulated. Payouts are effectively a "rebate" funded by fees, so a consistently winning trader is a cost the firm limits with caps and by ending payouts after a set number.
- For a systematic edge: treat every account as an option with a capped payoff (maximum 6 payouts at Apex, caps per request). Expected value = P(pass) × E[payouts before blow-up or cap] − (fees + activation + data).

### Gaps
- I could not read Topstep's original disclosure page (help.topstep.com was blocked), so its exact wording and methodology are unverified.
- No disclosures were found for Apex, Lucid, MFFU, Bulenox or Take Profit Trader.

## Q3. Many accounts, copy trading and automation: is running ~20 funded accounts feasible?

### Takeaway
Only Apex allows 20 funded accounts (20 PAs per household) with a copier across your own accounts, but it reportedly bans fully automated bots. Elsewhere the cap is 5 per firm (Topstep, Tradeify, Lucid, Bulenox, Take Profit Trader, Alpha Futures; MFFU 3–5). Reaching 20 would mean either Apex alone (manual or semi-automated) or about 4 firms × 5 accounts with a copier. Topstep is the most automation-friendly firm (official API), but it caps at 5 XFAs.

### Cited Findings
- Apex: copying among your own PAs within the 20-account household limit is allowed; hedging is banned; fully automated bots are reportedly banned ("every order must be placed manually"); semi-automated execution with oversight is described as permitted — [pickmytrade](https://pickmytrade.io/faq/prop-firm-automation/); [prop-memo](https://prop-memo.com/en/articles/futures-prop-firms-ea-allowed-2026); [thortradecopier](https://thortradecopier.com/blog/automated-algo-trading-prop-firms-rules)
- Topstep: bots allowed via the TopstepX/ProjectX API; reportedly no VPS; no API on Live Funded; copy trading allowed across your own accounts; third-party copy services banned — [h2tfunding](https://h2tfunding.com/does-topstep-allow-automated-trading/); [pickmytrade API list](https://blog.pickmytrade.trade/every-prop-firm-with-a-public-trading-api-in-2026/)
- Bulenox: bots and copiers allowed if user-built for personal use; commercial or shared bots banned — [prop-memo](https://prop-memo.com/en/articles/futures-prop-firms-automation-2026-09); [quantcrawler](https://quantcrawler.com/learn/bulenox-review)
- Generally banned everywhere: mirroring or hedging between different people, third-party signals, and purchased bots — [hextrade](https://hextrade.io/blog/prop-firm-automation-copy-trading-rules-database); [whichprop](https://whichprop.co/)

### Inferences
- An automated system on 20 accounts would need to run across several firms: Topstep (5, API) + Bulenox (5) + Lucid (5, if automation is confirmed) + Tradeify (5). Each firm uses different platforms (TopstepX, Rithmic, Tradovate), so the system needs a multi-broker execution layer.
- Correlation risk: 20 copies of the same strategy are a single bet. When the strategy has a bad month, every account blows up together, so the evaluation cost multiplies without diversification.
- The "no VPS" rule (Topstep) and "manual only" rule (Apex) are a real operational constraint for an unattended algo.

### Gaps
- The automation policies of Tradeify, Lucid, MFFU and Take Profit Trader were not verified in official terms.
- Whether Topstep's 5-account cap changed in 2026 is unknown.

## Q4. Trading costs: CME fees, commissions, slippage, tick values

### Takeaway
On a full-size contract, fees are small relative to the tick ($12.50 ES, $5 NQ). On micros they are large: about $1.0–$1.8 round-turn (RT) vs a $1.25 MES tick, which is about 1–1.5 ticks per RT in fees alone. In RTH the spread is almost always 1 tick, and slippage on small market orders is 0–1 tick, rising sharply around news.

### Cited Findings
- **Tick values** (standard CME contract specs; from my own knowledge, not fetched): ES $50 × 0.25 = **$12.50**; MES $5 × 0.25 = **$1.25**; NQ $20 × 0.25 = **$5.00**; MNQ $2 × 0.25 = **$0.50** — [CME Group contract specs](https://www.cmegroup.com/markets/equities/sp/e-mini-sandp500.contractSpecs.html) (not fetched in this session)
- **CME exchange fee for micros (MES/MNQ):** about $0.35 per side per contract (non-member); IBKR passes through $0.353. The official CME schedule (2026-06-29 PDF) exists but could not be read — [TradeStation](https://tradestation.com/pricing/exchange-execution-and-clearing-fees/); [IBKR](https://www.interactivebrokers.com/en/accounts/fees/CME.php); [CME fee schedule 2026-06-29](https://www.cmegroup.com/company/files/cme-fee-schedule-2026-06-29.pdf); [Optimus community](https://community.optimusfutures.com/t/how-to-verify-official-cme-exchange-fees-for-micro-futures-mes-mnq-mgc/11570)
- NFA fee for non-members about $0.02 per side (forum, possibly dated) — same Optimus source
- **Prop RT commissions:** Tradeify (official help center) **$5.76 ES/NQ, $1.82 MES/MNQ** all-in. Topstep (third-party) $3.78 ES/NQ, $1.22 MES/MNQ. Apex about $3.10 NQ / $1.04 MNQ on Tradovate, or about $3.98 ES RT on Rithmic. Lucid $3.50 NQ / $1.00 MNQ — [Tradeify help](https://help.tradeify.co/en/articles/10468315-trading-commission-fees); [trackytrade](https://trackytrade.com/prop-firm-commission-rates); [dealpropfirm](https://dealpropfirm.com/apex-trader-funding/commissions); [wayofthetrader](https://wayofthetrader.com/education/futures/mnq-commission-futures-trading-fees)
- Tradeify warns that trading micros in multiples of 10 costs more than the corresponding mini — [Tradeify help](https://help.tradeify.co/en/articles/10468315-trading-commission-fees)
- **Spread and slippage (low reliability; blogs and forums):** ES/NQ spread is 1 tick in RTH; MES is almost always 1 tick, widening to 0.50 points around events. Slippage is 0–1 tick for market orders under 10 contracts; 1–3 ticks for stops; 10+ ticks for a few seconds around FOMC/CPI/NFP; 4–6 ticks for a 10-lot of micros overnight — [NexusFi](https://nexusfi.com/a/risk-management/slippage-futures-trading); [jxtngx MES microstructure](https://jxtngx.github.io/ib-interface/blog/mes-microstructure); [Optimus price impact](https://learn.optimusfutures.com/price-impact-analysis); [MetroTrade](https://www.metrotrade.com/?p=10181)
- **Margin:** in prop trading, the size limit comes from the firm's maximum contracts and drawdown rules, not exchange margin — [proptradingvibes max contracts](https://proptradingvibes.com/blog/topstep-maximum-contracts)

### Inferences
- **All-in cost per RT, my estimate (fee + 1 tick of slippage for a market entry and exit at the touch):**
  - MES ≈ $1.2–1.8 fee + ~$1.25–2.50 slippage ≈ **2–3.5 ticks**
  - MNQ ≈ $1.0–1.8 fee + ~$0.50–1.00 slippage ≈ **3–5.5 ticks** (fees ≈ 2–3.6 MNQ ticks)
  - ES ≈ $3.8–5.8 fee + ~$12.50 slippage ≈ **1.3–2.5 ticks**
  - NQ ≈ $3.1–5.8 fee + ~$5 slippage ≈ **1.6–2.2 ticks**
- Micros are much more expensive relative to the tick, so a strategy with a small gross edge per trade (scalping) only survives on minis. Backtests should model at least 1 tick of slippage per side for market orders plus the RT fees above.

### Gaps
- I could not read the exact CME fee for ES/NQ (non-member, roughly $1.3–1.4 per side from memory, unverified) because the PDF could not be fetched.
- No rigorous academic study of RTH slippage on MES/MNQ was found; it has to be measured on our own data (MBO).

## Q5. Data and platform costs

### Takeaway
Databento's CME (GLBX.MDP3) historical data is pay-as-you-go from $0.50 per GB (uncompressed), with MBO data from May 2017 and history back to 2010. Live data requires a subscription. CME non-professional fees are about $1.55 per month (top of book, single exchange) or $12.10 (depth). Rithmic adds $25–45 per month per account at some brokers; Sierra Chart costs about $25–46 per month.

### Cited Findings
- Databento: historical from $0.50/GB; usage-based billing on uncompressed binary size; CSV/JSON at no extra cost; live data needs a Standard, Plus or Unlimited plan — [Databento home](https://databento.com/); [pricing](https://databento.com/pricing); [usage FAQ](https://databento.com/docs/faqs/usage-pricing-and-data-credits.md); [subscription updates](https://databento.com/blog/updates-to-subscription-pricing)
- MBO from May 2017 (MDP 3.0); history extended to June 2010 (pre-2017 data from the legacy FIX/FAST feed) — [GLBX.MDP3 docs](https://databento.com/docs/datasets/glbx-mdp3); [CME history to 2010](https://databento.com/blog/CME-history-extended-to-2010)
- Third-party estimate: $0.50–$2 per GB depending on schema, around $2/GB blended — [NexusFi](https://nexusfi.com/a/data/databento-futures-market-data)
- CME non-professional (2026): top of book $1.55 per exchange or $4.65 for the 4-exchange bundle; depth $12.10 or $36.50 bundle; professional $134.50 per exchange per device — [NexusFi data fees](https://nexusfi.com/a/data/exchange-data-fees-market-data-costs); [AMP](https://www.ampfutures.com/trading-info/platform-data-fees/)
- Rithmic: $45 per month per account for new accounts from 2026-01-28 (one broker) vs $25 per month (another) — [pickmytrade Rithmic](https://pickmytrade.io/help/rithmic/rithmic-exchange-data-fees/); [Ironbeam](https://www.ironbeam.com/article-categories/rithmic-data-trading-platforms/)
- Sierra Chart: Package 3/5/11 at $24.60/$34.06/$43.53 or $26/$36/$46 per month — [Optimus support](https://support.optimusfutures.com/what-is-the-pricing-for-sierra-chart-platform-subscription-information); [PricingSaaS](https://pricingsaas.com/companies/sierrachart)
- NinjaTrader: data fees about $4 per exchange or $12 bundle (probably an older schedule); Rithmic routing $0.15–0.25 per contract — [Benzinga](https://www.benzinga.com/money/ninjatrader-data-fees)
- Prop firms usually include data in the fee, but some charge platform or data fees — [Elite Trader Funding help](https://help.elitetraderfunding.com/help/platformfee)

### Inferences
- A multi-year research dataset at OHLCV/trades level for ES/NQ/MES/MNQ costs little. Full MBO on ES/NQ over several years can reach hundreds or thousands of GB, so it is worth using the cost estimate on the Databento portal before downloading.

### Gaps
- No exact per-GB price for the MBO schema and no number of GB per day for ES/NQ were found, because the pricing page was blocked.

## Q6. Regulation and the 2023–2026 industry shakeout

### Takeaway
The CFTC's case against My Forex Funds (filed 2023) collapsed in May 2025: dismissed, with more than $3M in sanctions against the CFTC, but the judge did not rule that the model is legal. A CFTC consultation on challenge-based futures firms is open until 2026-11-30 (secondary source). Several futures firm closures and payout failures occurred in 2026.

### Cited Findings
- MFF: the complaint was dismissed in May 2025 with sanctions over the CFTC's conduct, which the court called reckless, and more than $3M in sanctions; there was no ruling on the funded-account model or on whether futures evaluation firms must register — [Finance Magnates](https://www.financemagnates.com/forex/mff-case-misconduct-embarrassment-for-the-cftc-but-not-yet-a-win-for-prop-trading/); [Tradovate prop blog](https://prop.tradovate.com/blogs/how-prop-futures-are-regulated); [daytradingtoolkit](https://daytradingtoolkit.com/market-insights/prop-firm-regulation-funded-traders-guide)
- CFTC consultation on challenge-based futures firms reportedly opened 2026-08-01, with comments due 2026-11-30. A possible rulemaking in 2027 is speculation. Reported SEC actions and an NFA notice on affiliate marketing have no primary source — [Track360 Q3 2026](https://track360.io/blog/prop-firm-regulation-news-roundup-q3-2026) (vendor; **not confirmed on cftc.gov**)
- Most funded-account firms operate without CFTC or NFA registration — [The Industry Spread](https://theindustryspread.com/retail-prop-trading-regulation-2026-my-forex-funds-cftc/)
- 2026 closures:
  - FundingTicks: announced 2026-01-20, support ended 2026-01-31, refunds — [TradeInformer](https://tradeinformer.com/broker-news/fundingpips-shuts-futures-prop-firm-fundingticks); [QuantVPS](https://www.quantvps.com/blog/funding-ticks-payout-rules)
  - Seacrest Markets: ended its prop business 2026-02-06 — [fundedfuturesfamily](https://www.fundedfuturesfamily.com/seacrest-markets-prop-firm/)
  - ATFunded: suspended its prop operation 2026-06-06
  - Alpha Futures: Premium plan closed July 2026 without honoring pending payouts
  - Rev One Trading: shut down August 2026
  - FundedSeat: announced closure 2026-09-28, with refunds — [damnpropfirms](https://damnpropfirms.com/futures-prop-firms/fundedseat/)
  - The Funded Trader: offline since September 2026 — [bestpropfirms](https://www.bestpropfirms.com/reviews/the-funded-trader/)
  - Overall lists — [propfirmscompared](https://www.propfirmscompared.com/blog/prop-firm-closures-payout-red-flags-2026); [thepropfirmguide](https://thepropfirmguide.com/prop-firms-that-shut-down/)

### Inferences
- Counterparty risk is real. Unpaid profit is a claim on an unregulated firm, so spread accounts across firms, withdraw often, and prefer firms with a long track record (Topstep, Apex).
- A CFTC rule change in 2027 could change the model, for example by making it more expensive or excluding certain jurisdictions.

### Gaps
- The original CFTC MFF press release (August 2023) and any 2026 CFTC consultation document were not verified on cftc.gov.
- The closure lists come from trackers, not regulators.
