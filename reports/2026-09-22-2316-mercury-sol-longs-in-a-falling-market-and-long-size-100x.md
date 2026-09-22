# mercury-sol-longs-in-a-falling-market-and-long-size-100x

_2026-09-22 23:16 UTC_

---

# WHAT DO LONGS DO IN A FALLING MARKET? — AND WHAT $2,000 × 5 WOULD MEAN

**2026-09-22 23:20 UTC · READ-ONLY · subject: Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · Titan untouched**

`openitems_guard` → **exit 0** (titan-bot HEAD `f53d048`), run first. Same book, same five controls as candidates 32 and 33
([candidate 33](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-09-17-1541-mercury-sol-candidate-33-require-bear-daily-for-a-short.md)).

---

## 🔴 THE ANSWER FIRST

**On the only evidence that exists, nobody can say what longs do in a falling market. The one book that has any falling-market longs holds THREE of them.**

* **Paper longs with a BEAR daily: n = 3.** 1 win, ΣR −1.850, mean −0.617R. That is under the n=8 line, so **it is not ranked.**
* **Live longs with a BEAR daily: n = 0.** The live era has **zero BEAR rows anywhere**: 0 in `trades`, 0 in `skip_attribution`. The last BEAR row was 2026-08-07 05:55 UTC. The live book **cannot tell us anything** about this.
* **The two definitions of "falling" disagree with each other.** Longs *below the daily EMA21* made **+0.240R on n=4 (2 wins)**. Longs *after a falling 5 days* made **−3.268R on n=3 (0 wins)**. When two reasonable definitions of the same condition point opposite ways at n=3–4, the data is noise.
* **The paper era was not a bear market.** The book traded 2026-06-14 → 08-07. Over that span **SOL went +6.9%**, with 29 down days and 26 up days, inside a 31% range. That is a **chop**, not a decline. Paper longs lost **−0.450R/trade in a flat, choppy tape.** That is a different claim from "longs lose in a bear market", and it is the only one the data supports.
* **The labels are correct.** All 5,068 stored `trend_1d` values reproduce exactly from Bybit candles (§1c). Nothing here comes from a bad label.

**⚠️ The brief's live figure is out of date.** "7 wins in 9, +12.453R" was the book as of #43 (2026-09-06). As of tonight the live LONG book has **11 closed trades: 9 wins, ΣR +19.740**, plus #50 open. Both are shown in the dollar table. **All 11 traded a market that went +61.4% (73.63 → 118.83).**

**The size decision, in one line.** At $10,000 a LONG risks **~$135–$349** on each full stop-out. **In 6 of 12 live long entries and 6 of 9 paper long entries**, one ordinary stop-out is larger than the **live 5%-of-equity daily breaker ($206)**. That breaker then **halts every entry on both sides** for the rest of the UTC day (§4e).

---

## 1. LONGS IN A BEAR REGIME — the paper book is the only place they exist

Population: `virtual_positions` 7–28 (`is_paper=1`, 22 closed: 9 LONG, 13 SHORT) and 29–49 (`is_paper=0`, 21 closed: 11 LONG, 10 SHORT; #50 LONG open).
R = `net_pnl / initial_risk_usdt`. MFE and MAE come from `water_mark` / `max_adverse_price` over the stop distance (`entry − original_sl`).
This reproduces the brief's medians: paper LONG MFE **+0.48R**, live LONG (first 9) MFE **+2.54R**.

### 1a) Paper LONGS by stored `trend_1d` at entry — n stated first. 🔴 No cell reaches n=8, so none is ranked.

| cell | **n** | ids | wins | ΣR | mean R | median MFE | median MAE | never reached +0.25R |
|---|---|---|---|---|---|---|---|---|
| paper LONG **BULL** | **1** | 22 | 0 | −1.064 | −1.064 | +0.29R | −1.01R | 0/1 |
| paper LONG **NEUTRAL** | **4** | 7, 9, 16, 18 | 1 (25%) | −0.394 | −0.098 | +0.60R | −0.69R | 1/4 |
| paper LONG **BEAR** | **3** | 12, 21, 26 | 1 (33%) | **−1.850** | **−0.617** | +0.72R | −1.00R | 0/3 |
| paper LONG *unlabelled* | **1** | 8 | 0 | −0.739 | — | +0.02R | −0.74R | 1/1 |
| **paper LONG, all** | **9** | | **2 (22%)** | **−4.046** | **−0.450** | **+0.48R** | −1.00R | 2/9 |

#8's entry row (`trades.id` 3225) has no daily label stored. Rebuilt from candles, it is **NEUTRAL**: at the fill price, at the price an hour earlier, and at that hour's high and low. With #8 as neutral, the cell becomes n=5, ΣR −1.133, mean −0.227.

**Per trade:**

| # | opened | entry | exit | R | MFE | MAE | `trend_1d` |
|---|---|---|---|---|---|---|---|
| 7 | 06-14 23:50 | 70.98 | exit_signal | **+2.089** | +3.00 | −0.19 | neutral |
| 8 | 06-20 07:00 | 72.05 | exit_signal | −0.739 | +0.02 | −0.74 | *(none → neutral)* |
| 9 | 06-21 02:50 | 73.30 | exit_signal | −0.264 | +0.31 | −0.36 | neutral |
| 12 | 06-24 02:25 | 69.55 | sl | −1.049 | +0.48 | −1.00 | **bear** |
| 16 | 07-10 08:30 | 79.37 | sl | −1.146 | +0.16 | −1.08 | neutral |
| 18 | 07-14 15:45 | 77.47 | sl | −1.074 | +0.89 | −1.02 | neutral |
| 21 | 07-19 06:50 | 76.05 | trail | **+0.285** | +1.44 | −0.68 | **bear** |
| 22 | 07-21 03:10 | 78.41 | sl | −1.064 | +0.29 | −1.01 | bull |
| 26 | 08-02 05:00 | 73.53 | sl | −1.085 | +0.72 | −1.00 | **bear** |

**What the cells say, without ranking them:** the BEAR longs did not fail by going nowhere. **None of the three stayed below +0.25R**; median MFE was +0.72R, the highest of the populated cells. They went green and then came back. That is the paper book's general long pattern (+1.26R mean give-back, 5 of 9 went ≥+0.25R and still lost), not a BEAR-specific one.

### 1b) Control: paper SHORTS by the same split

| cell | **n** | wins | ΣR | mean R | median MFE | median MAE | never +0.25R |
|---|---|---|---|---|---|---|---|
| paper SHORT BULL | **0** | — | — | — | — | — | — |
| paper SHORT NEUTRAL | **6** | 4 (67%) | −0.450 | −0.075 | +1.08R | −0.47R | 2/6 |
| paper SHORT BEAR | **7** | 2 (29%) | −0.878 | −0.125 | +0.53R | −0.57R | 1/7 |
| **paper SHORT, all** | **13** | 6 (46%) | −1.328 | −0.102 | +0.59R | −0.57R | 3/13 |

Also under n=8 in every cell. **The pattern the operator fears is not there.** Paper shorts did *no better* with a BEAR daily than paper longs did. Paper shorts under BEAR made −0.125R/trade; paper longs under BEAR made −0.617R. On n=7 against n=3, that gap tells us nothing. In the paper era, **a BEAR daily did not help the side it favours and did not clearly hurt the side it opposes.**

### 1c) 🔴 THE LABEL, RECOMPUTED FROM CANDLES — ✅ it reproduces on every row

The label comes from `indicators._classify_trend`: **BULL** if close > EMA9 > EMA21 and the 3-bar EMA9 slope is above +0.05%. **BEAR** is the mirror of that. **NEUTRAL** is everything else. It uses 200 Bybit `1d` candles, and the forming candle counts as the last one.

I rebuilt it from Bybit SOLUSDT daily klines (GET only, over isolated Tor circuits) with the same `pandas_ta.ema`. I tested it two ways:

1. **All 5,068 labelled `trades` rows** (paper 3,369 + live 1,699). For each row I solved the stored `ema_gap_pct_1d` back to the forming-candle close the bot actually saw, and checked that the close falls inside that hour's real range.
   → **5,068 / 5,068 labels reproduce exactly. The implied close is in range on 5,068 / 5,068.** 84 rows fall in the first hour after 00:00 UTC and need the previous day's candle set. That is the documented `1d` cache TTL of 3,600 s (`indicators.py:63`), not an error.
2. **The 44 position-entry rows (#7–#50), at the actual fill price:** **42 of the 43 labelled rows match.** #8 is unlabelled (see §1a). The one miss is **#20, a SHORT**: stored neutral, bear at the fill price. Its stored label is still consistent with the cached snapshot. The EMA9/EMA21 gap was 0.004% at the time, so the label sat on the knife-edge between the two, and neither reading is wrong. **None of the 9 paper longs is affected.**

A naive check that uses the hourly close instead of the solved close still gives 95.5% agreement. Every one of its misses is a boundary row.
**No stored label is wrong. Nothing in this report rests on a bad label.**

### 1d) A SECOND DEFINITION OF "FALLING", fixed before computing

Declared before any number was run, neither uses the label:
* **(D2) price below the daily EMA21** at entry. The EMA21 is computed on the forming candle at the fill price.
* **(D3) prior 120-hour return < 0**: the fill price against the hourly close 120 h earlier.

| paper LONG cell | **n** | ids | wins | ΣR | mean R | median MFE |
|---|---|---|---|---|---|---|
| **D2: below EMA21** | **4** | 7, 12, 21, 26 | **2** | **+0.240** | **+0.060** | +1.08R |
| D2: above EMA21 | **5** | 8, 9, 16, 18, 22 | 0 | −4.286 | −0.857 | +0.29R |
| **D3: 120h return < 0** | **3** | 12, 16, 18 | **0** | **−3.268** | **−1.089** | +0.48R |
| D3: 120h return ≥ 0 | **6** | 7, 8, 9, 21, 22, 26 | 2 | −0.778 | −0.130 | +0.52R |
| D2 **and** D3 | **1** | 12 | 0 | −1.049 | — | — |

**Does it agree with (a)? No, and that disagreement is the finding.**
* By **D2**, the "falling" longs were the paper book's **only profitable cell** (+0.240R). #7, the best paper long at +2.089R, entered *below* the EMA21 on a +9.3% 5-day bounce.
* By **D3**, the "falling" longs were **three straight losers**.
* By the **label**, they were 1 win in 3.

Three definitions of one condition give three different answers on cells of 1–5 trades. **Paper cannot say what a long does in a falling market; it can only show how small the sample is.**

Live, for the record: no live long was ever below the daily EMA21 (**D2 n=0**). Exactly one live long had a negative 120 h return: **#48, the book's best trade, +5.431R.**

### 1e) 🔴 THE PAPER ERA'S OWN TAPE — flat, not falling

| window | SOL move | days | down days | up days | range (low → high) |
|---|---|---|---|---|---|
| 2026-05-23 → 08-07 (the brief's "paper era") | **−12.7%** (84.35 → 73.63) | 77 | **45** | 32 | 60.03 → 87.50 (45.8%) |
| 2026-06-03 → 08-07 (first DB row → end) | **−0.7%** | 66 | 36 | 30 | 60.03 → 83.95 |
| **2026-06-14 → 08-07 (first → last paper position)** | **+6.9%** (68.89 → 73.63) | 55 | **29** | **26** | 63.96 → 83.95 (31.3%) |
| 2026-08-08 → 09-22 (live) | **+61.4%** (73.63 → 118.83) | 46 | 19 | 27 | 73.53 → 120.07 |

Daily-close labels, rebuilt from candles: book span **30 neutral / 14 bear / 11 bull**; live span **29 bull / 16 neutral / 0 bear**. The last BEAR daily close was **2026-08-06**. The last BEAR row in the DB was 2026-08-07 05:55. 43 live-era days carry labelled rows, and **none of them is BEAR**.

**The brief's −12.7% happened mostly *before* the first paper position.** SOL fell from 84 to 60 during 05-23 → 06-13, and the paper book did not trade in that window. **While the paper book was trading, SOL was flat-to-up in a choppy 31% range.** So the accurate statement is: **paper longs lost −0.450R/trade in a flat, choppy market.** Nobody has watched longs trade through a sustained decline, on paper or live.

---

## 2. THE SECOND SOURCE — refused LONG signals and their forward drift

> 🔴 **DRIFT IS NOT REALISED R.** It is where price went after a refused signal, with no stop, no trail, no fees and no exit logic. On 2026-08-19, Titan's refused signals drifted **+0.64% in their own favour and lost −12.03R** once run as full-contract trades. Everything below is **drift. None of it is an edge.**

`skip_attribution` × `skip_drift_samples`. Drift is signed so that + means price moved the refused signal's way. Degraded samples are excluded. Rows are **not independent**: one signal burst writes many rows within minutes.

### 2a) Live-era refused LONGS (4,314 rows) by `trend_1d` at refusal

| `trend_1d` | rows | days | 1h mean / median / %>0 | 4h | 12h | 24h | median 24h max-favourable |
|---|---|---|---|---|---|---|---|
| bull | 1,490 | 33 | +0.10 / +0.04 / 53% | +0.31 / +0.09 / 54% | +0.54 / +0.07 / 51% | +0.91 / −0.04 / 50% | +1.58% |
| neutral | 664 | 20 | +0.04 / +0.03 / 52% | +0.15 / +0.19 / 62% | +0.12 / +0.15 / 54% | +0.61 / +0.43 / 59% | +1.13% |
| **bear** | **0** | **0** | — | — | — | — | — |
| *(not captured)* | 2,160 | 46 | +0.02 / 0.00 / 50% | +0.17 / +0.04 / 52% | +0.60 / +0.23 / 57% | +1.05 / +0.32 / 56% | +1.58% |

In a +61% market, refused longs drifted up. That is the tape, not the signal. At 24 h the bull-label median is **−0.04%**, a coin flip.

**The only BEAR-daily drift that exists is from the paper era, shown for completeness:**

| paper-era refused LONG | rows | days | 4h mean / median / %>0 | 24h mean / median / %>0 |
|---|---|---|---|---|
| bull | 498 | 12 | −0.22 / −0.14 / 41% | −0.75 / −0.30 / 45% |
| neutral | 736 | 20 | −0.06 / −0.05 / 47% | −0.78 / −1.17 / 31% |
| **bear** | **669** | **18** | −0.08 / −0.04 / 46% | **+0.26 / +0.49 / 58%** |

In the paper chop, refused longs under a BEAR daily drifted *up* by 24 h, and refused longs under BULL or NEUTRAL drifted *down*. That is what mean reversion inside a range looks like. **It is drift, from a flat market, in 18 correlated days. It is not evidence that longs work in a bear market.**

### 2b) Stated plainly
**Drift is not R.** The paper-era +0.49% median 24 h drift on BEAR-daily refused longs is smaller than one typical stop distance (1.8–2.2%). Nothing is known about how many of those signals would have hit their stop first. **I do not call any of it an edge.**

### 2c) Live-era rows with `trend_1d = bear`
**Zero.** 0 of 1,699 labelled `trades` rows and 0 of 4,275 labelled `skip_attribution` rows since 2026-08-08. On 72 live rows EMA9 sat below EMA21 (`ema_status_1d='Bearish'`), but price stayed above the EMA9, so the label never flipped.

---

## 3. 🔴 THE MIRROR GATE — "no LONG when `trend_1d` is bear" — MEASURED, NOT PROPOSED

> **BONFERRONI IN THE HEADER.** Frame unchanged from candidates 32/33: side × regime × book = **m = 12**, corrected **α = 0.05/12 = 0.004167**. Exact permutation on mean R (all 84 splits) and two-sided Fisher exact on wins.

### 3a) What it refuses

| book | longs refused | R |
|---|---|---|
| **PAPER** | **#12** (06-24) | −1.049 |
| | **#21** (07-19) | **+0.285 🔴 WINNER** |
| | **#26** (08-02) | −1.085 |
| **LIVE** | **none** — no live long ever had a bear daily | — |

**Paper LONG ΣR:** −4.046 → **−2.197** (n 9 → 6). **Paper book ΣR:** −5.374 → −3.525. The surviving longs' mean R goes −0.450 → −0.366.
In paper dollars at $10,000 notional, it removes **−$338.61**.

### 3b) 🔴 IT REFUSES A WINNER

**#21, +0.285R, trail exit, MFE +1.44R.** Filter 21 and candidate 31 were both killed for exactly this. Refusing 3 trades to drop 2 losers and 1 winner, on n=3, is not a filter.
If "bear" is defined by D2 (below EMA21), the mirror refuses **#7 (+2.089R), the best paper long**, together with #21. That version turns a −4.046R book into **−4.286R**.

### 3c) Volume cost
* **Paper: 3 of 9 longs refused (33%).**
* **Live: 0 of 11 (0%).** The gate has never been satisfiable in the live era.

### 3d) The five controls

| control | result |
|---|---|
| **(a) Bonferroni** | ❌ **FAIL.** Bear vs non-bear paper longs: mean-R difference −0.250R, **exact permutation p = 0.857**; wins 1/3 vs 1/6, **Fisher p = 1.000**. Nowhere near 0.004167, or even 0.05. |
| **(b) Chronological halves** | ❌ **FAIL. The ranking flips.** H1 (#7–#16): bear n=1, −1.049R **worse** than non-bear (n=4, −0.059R). H2 (#18–#26): bear n=2, −0.801R **better** than non-bear (n=2, −2.137R). |
| **(c) Both regime legs populated** | ⚠️ Paper: yes, but the bear leg is **n=3**. Live: **bear leg n=0.** The control cannot be run on live. |
| **(d) Live book as the independent sample** | 🔴 **CANNOT BE RUN. The live bear-long cell is EMPTY.** No sample exists to confirm or refute the paper result, so **the candidate cannot be convicted.** |
| **(e) Label vs era confound** | ❌ **FAIL.** All 3 bear-daily longs are paper-era, all in the 06-14 → 08-07 chop. All 11 live longs are in a +61% rally. "Bear daily" and "paper-era chop" are the same set of rows, and so are "not bear" and "live-era rally" on the live side. |

**0 of 5 pass. Two cannot even be run.**

### 3e) This is a measurement. **Nothing is proposed.**

---

## 4. THE SIZE QUESTION — numbers only, nothing applied

### 4a) 🔴 The account (GET only, isolated Tor circuits, 2026-09-22 ~23:30 UTC)

| field | value |
|---|---|
| account | **UNIFIED, `marginMode = REGULAR_MARGIN` (cross)**, hedge mode (positionIdx 1/2) |
| total equity (all coins, USD) | **$4,888.50** (includes WLD $252.42 + FIL $518.35, which carry ~no collateral value) |
| **USDT equity** (what the daily breaker reads) | **$4,118.34** |
| total margin balance | $4,117.69 |
| **total available balance** | **$4,098.57** |
| used initial margin | $19.12 (the open LONG #50, 0.8 SOL @ 117.82, SL 114.79 on venue) |
| maintenance margin | $0.55 |
| SHORT side | flat |

**Is $2,000 free for one LONG plus the SHORT's $20, with a buffer?** **Yes.**
$2,000 + $20 = **$2,020** initial margin against **$4,098.57** available, which leaves **~$2,078** after both are open. One full LONG stop-out costs at most ~$349 (worst live case), so the account keeps **~$1,730** of free margin after it.
**Nothing is missing.** Two stop-outs a day still leave >$1,300 free. The practical limit is the daily breaker (§4e), not margin.

**API key:** `Wallet: []`. **No transfer permission**, and nothing was changed. *(For information only: the key also holds Spot `SpotTrade` and Options `OptionsTrade`, which this bot does not use. I did not change them.)*

### 4b) Risk tier, maintenance margin, liquidation vs stop — at $10,000 on SOLUSDT, 5×

| item | value |
|---|---|
| risk-limit tier | **id 281, ≤ $50,000**. Lowest tier, **MMR 0.50%**, IMR 1% (max 100×). $10,000 is 20% of the tier cap. |
| initial margin at 5× | $2,000 |
| maintenance margin | **$50** |
| qty at the representative entry | 84.9 SOL (lot step 0.1; max market order 12,000) |

**Representative entry: the currently open LONG #50.** Entry **117.82**, ATR(1h) **1.2105**, stop = 117.82 − 2.5 × 1.2105 = **114.79** (−2.57%).

| | price | distance below entry |
|---|---|---|
| **stop (2.5 × ATR 1h)** | **114.79** | **−2.57%** |
| liquidation if **isolated** at 5× (approx.) | **94.85** | −19.5% |
| **liquidation as the account actually is (cross, $4,117 margin balance)** | **≈ 70.0** | **≈ −40.6%** |

**The stop sits well inside liquidation**: about 7.6× closer than the isolated liquidation price and about 16× closer than the cross one. Even the widest live-long stop (3.30%) is nowhere near.
⚠️ Under cross margin, liquidation is an **account** property. The $10k LONG would draw on the whole USDT balance, not a $2,000 slice. A stop that fails to fill therefore puts **the account** at risk, not just $2,000.

### 4c) Per LONG at $10,000 — from the live book's own ATR distribution (12 live long entries incl. #50)

| measure | median | p10 | p90 | range |
|---|---|---|---|---|
| ATR(1h) as % of price | 0.71% | | | 0.46 – 1.32% |
| stop distance (2.5 × ATR 1h) | **1.78%** | 1.22% | 3.21% | 1.15 – 3.30% |
| **1R in dollars** | **$178** | $122 | $321 | $115 – $330 |
| fee round trip (venue taker **0.100%** × 2 legs) | **≈ $20** | | | |
| **loss on a full stop-out** (1R + both taker legs) | **≈ $198** | | | **$135 – $349** |
| funding (mean of last 200 8h prints: +0.00227%) | ≈ $0.23 per 8h paid by a long | | | max +0.01% = $1 / 8h |

Paper longs for comparison: stop 2.18% median, **1R $218, full stop-out ≈ $238** (range $138–$260).
Note: `BYBIT_TAKER_FEE_RATE = 0.00055` in config is **geometry only** (`config.py:1243`). Real accounting uses the venue rate of 0.001, so the $20 figure is the real one.

### 4d) 🔴 ONE TABLE, BOTH BOOKS — the LONG side re-run at $10,000 notional

Each trade's realised result is scaled to $10,000 notional (net PnL × 10,000 / entry notional). It is then re-charged at the venue's true **0.100% taker on both legs**. The paper book was **already** $10,000 notional ($2,000 × 5), but was charged the old 0.055% fee model. This assumes the same fills, i.e. no extra slippage on 85 SOL.

| | **LIVE LONG, 11 closed (tonight)** | LIVE LONG, first 9 (the brief's figure) | **PAPER LONG, 9** |
|---|---|---|---|
| era / tape | 08-08 → 09-21, **SOL +61%** | 08-08 → 09-06 | 06-14 → 08-02, **SOL flat, choppy** |
| wins | 9 / 11 | 7 / 9 | **2 / 9** |
| ΣR | **+19.740** | +12.453 | **−4.046** |
| **Σ $ at $10,000** | **+$4,331** | **+$2,739** | **−$794** *(as recorded at 0.055%: −$713)* |
| mean $ / trade | +$394 | +$304 | **−$88** |
| best trade | +$1,175 (#48) | +$841 (#40) | +$486 (#7) |
| worst trade | −$158 (#31) | −$158 (#31) | −$243 (#12, #18) |
| **worst run of consecutive long losses** | **−$165** (2 trades: #31, #33) | **−$165** (2 trades) | **−$944 (5 trades: #8 → #18)** |

Per-trade $ at $10k, live: +245, +136, −158, −7, +518, +391, +841, +537, +234, +1,175, +417.
Per-trade $ at $10k, paper: +486, −187, −68, −243, −204, −243, +25, −213, −148.

**The two columns are the same logic in two different markets.** The live column is what $10,000 would have made in a +61% rally. The paper column is what it would have lost in a flat chop: a five-trade losing run of **−$944**, which is **23% of the USDT balance**. **Neither column contains a falling market.**

### 4e) 🔴 EVERY DOLLAR-DENOMINATED BRAKE AND ALARM — what each does at $10,000 LONG

This covers every threshold in the SOL tree, its cron scripts and `/home/botuser/.openclaw/workspace/scripts/sol_book_gate_review.py` whose meaning changes with size. I read the source and checked the key lines by hand.

**Key:** **TRIPS** = fires on the first ordinary stop-out · **DEAD** = becomes meaningless · **MIS-SCALES** = keeps working but distorted · **OK** = unaffected

| # | brake / alarm | where | value · unit | what it does | at $10,000 LONG |
|---|---|---|---|---|---|
| 1 | 🔴 **Daily loss breaker, clause 2: equity floor** | `config.py:1305`, `main.py:1944–1968` | **5% of USDT equity**, from `fetch_balance` USDT total ≈ **$4,118 → $206**. Summed in **$** over today's closed live positions, **both sides** | **Blocks ALL entries, LONG and SHORT, for the rest of the UTC day.** One TG alert. Fails closed if equity is unknown on a loss day. | 🔴 **TRIPS on the first ordinary stop-out in 6 of 12 live-long cases and 6 of 9 paper-long cases** (full stop-out $135–$349 vs a $206 line; the median live stop-out of $198 misses it by $8). A $10k LONG loss also makes any $100 SHORT result invisible in the $ sum. **DORMANT today** (one $100 stop is about $1–3). |
| 2 | Daily loss breaker, clause 1: R tail brake | `config.py:1304`, `main.py:1926` | **−3.0R**, per-trade `net_pnl / initial_risk_usdt` summed | Blocks all entries for the day | ✅ **OK, correct as is, it is in R.** A $100 SHORT R and a $10k LONG R weigh the same. |
| 3 | Loss-streak brake | `config.py:1310–1354`, `main.py:2181–2241` | 3 losses within 45.1 h, ΣR ≤ **−2.05R**, 4 h cooldown | Blocks entries | ✅ **OK, in R.** |
| 4 | Per-trade max $ loss | — | **does not exist** | — | Per-trade loss is bounded only by the venue stop plus cross margin. |
| 5 | Drawdown halt | — | **does not exist** | — | — |
| 6 | 🔴 **Balance/margin pre-check before entry** | `main.py:2925–2946` | **does not exist.** Sizing goes straight to `set_leverage` and the order | — | Today $2,000 IM fits ($4,098 available). If the balance falls below about $2,000 + fees, the order fails on the venue as an entry exception, with **no clean "insufficient balance" refusal.** |
| 7 | Combo-weight learning | `signal_weights.py:69–70`, used `:144` | **win ≥ +$20 / loss ≤ −$15** per trade | ±0.10 weight, clamped 0.5–2.0. It feeds the advisor prompt ("Combo weight"), so it **influences entries.** Shared by both sides, paper and live mixed. | ⚠️ **MIS-SCALES.** Every $10k LONG becomes a win or loss again. A $100 SHORT (±$1–3) is **always "neutral"** and never learns. At $100 today almost every live trade is neutral. |
| 8 | 15m HyperWave subtype weights | `engine_15m.py:56–57` | same **+$20 / −$15** | subtype weight, logged and shown | ⚠️ **MIS-SCALES**, same asymmetry as #7 |
| 9 | Feature-weight normalisation | `weight_engine.py:37`, used `:369` | `tanh(avg_pnl / $20)` | informational. **Not applied to the entry gate** | ⚠️ **MIS-SCALES.** Saturates at ±1 on any LONG-heavy segment. Harmless because nothing gates on it. |
| 10 | Optimizer worst-segment | `optimizer.py:42–43, 356–358` | ranks segments by **Σ $** | picks the proposal target | ⚠️ **MIS-SCALES.** A $100 SHORT segment can never be "worst", so every proposal becomes LONG-driven. |
| 11 | Optimizer listener live-evidence guard | `optimizer_listener.py:75–101` | `MIN_LIVE_SHARE = 0.50` of **\|$ PnL\|** live vs paper | gates proposals on live evidence | ⚠️ Gets easier to satisfy, because $10k LONG dollars swamp everything else |
| 12 | Venue minimums | `stop_loss.py:121–147` (`quantise_amount`) | 0.1 SOL min, $5 min notional; **no max-qty guard** | refuses sub-minimum orders | 💤 **DEAD at this size** (84.9 SOL is far above the floor). The venue market-order max is 12,000 SOL, so no max guard is needed. |
| 13 | Partial-fill alert | `main.py:3104, 3774, 3808` | `abs(filled − amount) > 1e-9` **SOL** | alerts only | ✅ OK. Fires more often at 85 SOL, which is correct. |
| 14 | Venue-stop match check | `virtual_trader.py:2001` | price tolerance 1e-6 relative | reconcile | ✅ OK, not a size tolerance |
| 15 | Naked / flat tests | `main.py:580, 618, 2108, 2287, 2352, 2806`; `naked_alert_resolver.py:138`; `silence_digest_sol.py:435` | `contracts > 0` | detects open or naked positions | ✅ OK. No size threshold. |
| 16 | 🔴 **Naked-position TG text** | `main.py:2691` | literal **"not the $100 notional"** | the text of the no-stop emergency alert | 🔴 **Wrong at $10k.** The one alert that must be accurate would understate the exposure 100×. |
| 17 | Open-position card | `main.py:5534` | `💵 ${active_fixed_margin()} margin` | display | 🔴 **Wrong:** it would print **$20** for a $2,000 LONG |
| 18 | Stored `margin_usdt` | `virtual_trader.py:2575, 2763` | `LIVE_FIXED_MARGIN` | stored, never read back | Would record $20 against a $2,000 position |
| 19 | Fee-rate sanity | `fee_rates.py:97` | `0.0001 ≤ rate ≤ 0.01` (a rate) | rejects an implausible venue rate | ✅ OK, a rate, not $ |
| 20 | Fee $ / funding $ sanity alarm | — | **does not exist.** Funding is read from the venue and booked (`virtual_trader.py:696–722`) | — | — |
| 21 | Reconcile qty/$ tolerance, DB-vs-venue PnL gap alarm | — | **does not exist.** `_adopt_derive` has no size or margin check | — | — |
| 22 | Advisor "Unrealized PnL: $x" | `claude_advisor.py:1450` | $ text in the exit-advisor prompt | **dry-run** | the text changes, nothing gates on it |
| 23 | Tape whale threshold | `config.py:868` | `MICROSTRUCTURE_WHALE_USDT = 50,000` | classifies *market* prints | ✅ OK, not our size |
| 24 | Cron / watch scripts | `sol_*_regime_watch.sh`, `/root/mercury_sol_30trade_reminder.sh`, `mercury_sol_prior_move_logger.py`, `healthcheck.py`, `sol_book_gate_review.py` | signal counts, trade counts, seconds | — | ✅ No $ or qty thresholds |
| 25 | Break-even lock target | `trail_arm.py:64` / `config.py:1243` | +0.20% of entry, from the 0.055% **geometry** fee | moves the stop to "BE" when the trail arms | ✅ In %, so it scales. But true round-trip costs are 0.20% + slippage, so a BE exit at $10k is ≈ −$0 to −$5, not $0. |

**Trips on the first ordinary stop-out:** **#1 only**, the daily 5%-of-equity breaker, and it halts both sides.
**Becomes meaningless:** #12 (venue minimums), and **#16/#17 become false** in exactly the alert that matters most.
**Mis-scales:** #7–#11. All four learning and ranking loops would start learning from LONG outcomes only.
**Correct as they are because they are in R:** #2 (daily −3R), #3 (loss streak), and the R denominator itself (`initial_risk_usdt = amount × |fill − sl|`).
**Absent:** per-trade $ cap, drawdown halt, fee/funding $ alarm, DB-vs-venue gap alarm, reconcile size tolerance, balance pre-check.

*Correction to a comment in the code:* `main.py:1933` mentions "an $811.90 balance". That was the paper-era figure. **Tonight the USDT equity is $4,118.34.**

### 4f) How the margin constant is read today — and what a per-side change would take

**There is one margin value per BOOK, and none per SIDE.** `config.py:38–39`: `PAPER_FIXED_MARGIN = 2000`, `LIVE_FIXED_MARGIN = 20`. `active_fixed_margin()` (`:42`) chooses by mode only. `LEVERAGE = 5` (`:50`) is shared by both books and both sides. Config was read as text; it was not imported.

**Every call site:**
* **Live sizing, the only place a live order's size comes from:** `main.py:2925`, `notional_usdt = LIVE_FIXED_MARGIN * LEVERAGE`, then `quantise_amount` at `:2928`. `position_side` is already in scope in that function.
* `main.py:2937`: `set_leverage(LEVERAGE, symbol)`, one value for the symbol.
* `main.py:5534`: open card, `active_fixed_margin()` (display).
* `main.py:2691`: literal "$100 notional" in the naked-position alert.
* `virtual_trader.py:2575` (stored `margin_usdt`) and `:2763` (adoption fields): `LIVE_FIXED_MARGIN`.
* Paper only: `virtual_trader.py:228` (sizing) and `:379` (stored), `PAPER_FIXED_MARGIN`.
* Other `quantise_amount` callers: `main.py:3694` (live partial, capped at the venue-held qty) and `virtual_trader.py:233, 1299` (paper and partial legs). **Closes are sized from the venue position**, so they need no change.

**What a per-side change would take (not written in this pass):**
1. A per-side constant or helper in `config.py`.
2. The pick by `position_side` at `main.py:2925`.
3. The stored `margin_usdt` at `virtual_trader.py:2575` and `:2763`. The adoption path needs a side too.
4. The display at `main.py:5534` and the alert text at `main.py:2691`.
5. `set_leverage` can stay one value while both sides stay at 5×.
6. For the **brakes** to mean the same thing afterwards, the change would also meet #1 (the equity-% breaker), #6 (no balance pre-check) and #7–#10 (the $-denominated learning and ranking loops).

---

## 5. VERDICT

**The operator's question: what do longs do in a falling market?**

**Nobody knows, and the data cannot say.**

* **The live era can tell us nothing.** 46 days, 11 closed longs, **0 BEAR daily rows, 0 longs below the daily EMA21**, and SOL +61%. Every live long traded one regime: a rising market.
* **The paper era can tell us very little.**
  * It holds **3 BEAR-daily longs** (1 win, −1.850R). By a second definition (D2) it holds **4 longs below the EMA21, and they were the paper book's only profitable cell** (+0.240R). By a third (D3) it holds 3 falling-tape longs, all losers.
  * The paper era itself was **a flat chop (+6.9%, 29 down / 26 up), not a decline.**
  * So paper shows that **longs lost −0.450R/trade in a sideways market**. It does not show what they do when the market falls.
* **Confidence: none.** No cell reaches n=8, the definitions contradict each other, and the only independent sample (live) is empty. The mirror gate, as a measurement, fails every control that can be run. It refuses a winner, and it cannot be convicted because it has never been tested.
* **What is true and relevant:** the gate added on 2026-09-17 refuses a SHORT under a BULL daily. **There is no mirror.** In a falling market the bot will take LONGs against the daily, and **that population has never been observed, live or at any size.** A 100× larger LONG would be the first thing to meet it.

**The dollar table for the decision** (from §4d):

| | Σ $ at $10k | mean $ | worst losing run |
|---|---|---|---|
| Live LONG, 11 (rally) | +$4,331 | +$394 | −$165 (2) |
| Paper LONG, 9 (chop) | −$794 | −$88 | **−$944 (5)** |
| Bear-daily LONG, any book | **n=3 paper (−$338 as recorded) / n=0 live** | — | — |

**Margin is not the constraint:** $4,098.57 is available against $2,020 needed. **The stop sits far inside liquidation:** 114.79 vs ≈70 (cross) or 94.85 (isolated). **The daily 5% breaker is the constraint that bites first** (§4e).
**No recommendation. The operator decides.**

---

## READ-ONLY CONFIRMATION

| check | state |
|---|---|
| `openitems_guard` | **exit 0**, run first |
| SOL DB | `file:…/trades.db?mode=ro` + `PRAGMA query_only=1` (asserted = 1 on every connection). **No writes.** |
| SOL config | read **as text** (grep/sed). **Never imported.** sha256 `0585a82c…bee730`, **unchanged** during the pass |
| Venue | **GET only**, every call on a **fresh isolated Tor circuit** (random SOCKS auth): `/v5/market/kline`, `/v5/account/wallet-balance`, `/v5/account/info`, `/v5/position/list`, `/v5/account/fee-rate`, `/v5/user/query-api`, `/v5/market/risk-limit`, `/v5/market/tickers`, `/v5/market/instruments-info`, `/v5/market/funding/history`, `/v5/order/realtime`. **No orders placed, amended or cancelled. Key permissions not changed.** |
| `mercury-sol.service` | `NRestarts=0`, `MainPID=3077029`, active since 2026-09-17 16:55:13, **identical before and after** |
| `titan.service` | `NRestarts=0`, `MainPID=4007821`, active since 2026-09-21 19:03:51, **identical before and after** |
| `FLAT_ADX_GATE_DRYRUN` | **True** (`config.py:407`), untouched |
| `BOOK_GATE_ENABLED / _DRYRUN` | **True / False** (`config.py:474–475`), untouched |
| `BULL_DAILY_SHORT_BLOCK_ENABLED / _DRYRUN` | **True / False** (`config.py:1387–1388`), untouched |
| **Titan** | **UNTOUCHED.** Only `tools/openitems_guard.py` was run, as ordered. It is read-only. |
| Applied | **nothing.** No diff, no flag, no restart, no proposal. |
