# titan-vpos-112-post-mortem-armed-exit-saved-0-69r-strategy-loss

_2026-09-26 16:39 UTC_

---

# Titan — vpos 112 post-mortem: a LONG closed at −0.37R. **STRATEGY LOSS, NO MECHANICAL DEFECT.** The armed exit closed it; holding would have hit the stop 6 h later at −1.06R, so the exit **saved +0.69R**. It **did** print +0.25R (peak +0.51R) and **never** reached the +1R arm. **Not an advisor decision, so the ledger is unchanged at 5 of 10, Σ +1.0497R.**

**2026-09-26 16:45 UTC · titan-bot HEAD `f53d048` · Titan LIVE REAL MONEY · READ-ONLY PASS · Mercury-SOL NOT TOUCHED · `openitems_guard` EXIT=0 (run first)**

# 🔴 vpos 112 — LONG 0.0017 BTC · entry 86 536.2 (2026-09-22 15:45:23 UTC) → exit 86 116.7 (2026-09-23 08:00:28 UTC) · `close_reason='armed_exit'` · −0.3736R / −$0.8615 (BingX)

It is the most recent closed LONG, and the most recent close of any kind: the DB has no row after vpos 112, and BingX shows 0 positions and 0 open orders right now.

---

## THE VERDICT FIRST

| question | answer |
|---|---|
| Mechanical defect? | **None found.** The fills match the DB. The stop sat where it was placed and was cancelled after the close. The armed exit fired inside its 6 h TTL. No failed-read state appears in any DB row. The only gap is a **$0.0003 funding charge** the DB missed (§1a). It is bookkeeping, not an order or exit fault, and I wrote no fix for it. |
| Entry fact or exit fact? | Under the brief's rule it is the smaller **"peaked, then gave it back"** shape, **not** the never-+0.25R shape. Peak +0.51R, arm never reached, closed at −0.37R. But the exit did not fail. The 0–1R zone is unprotected by design (arming earlier measured **−15.11R**, 2026-08-24), and the exit that fired beat holding by **+0.69R**. |
| What was weak about the entry | Recorded as description only. The matrix counted **1 of 3 tiers** (score 2.5 against a 3.0 bar). A **+1.0 news bump** ("Bitcoin ETFs Take N. $1B in a Day", classed STRONG_POSITIVE) cleared the bar at 3.5. The position spent **77 % of its life below entry**. It peaked **123 pts under** a swing high confirmed before entry, which it never broke. |
| Advisor ledger | **Unchanged: 5 RESOLVED of 10, Σ +1.0497R / +$1.72.** The armed exit consulted the advisor, which said **HOLD 0.72**, and then closed anyway. This is the vpos 99 shape and is out of the population by the 2026-09-21 second ruling. |
| Watched name `Bullish OB Created` | **Not the trigger** (`Bullish S-CHOCH+`), so the count **stays at 4 of 8**. But it fired **in the same second**, got `execute 0.78`, and was blocked only by the one-position cap. |
| New filter proposed? | **No.** One trade. |

---

# 1. WHAT HAPPENED, FROM THE VENUE FIRST

## 1a. BingX's own records (GET only: `allOrders`, `allFillOrders`, `user/income`; positionID `2102424022516199426`)

| leg | orderId | type | qty | avg price | time (UTC) | commission |
|---|---|---|---|---|---|---|
| entry | `2102424022491033600` | MARKET BUY, LONG | 0.0017 | **86 536.2** | 09-22 15:45:23 | −0.073556 |
| stop | `2102424024818233344` (`titan-sl-aed37c357021aa686a3d`) | STOP_MARKET SELL 85 179.8, reduce-only | 0.0017 | **not filled**, CANCELLED 09-23 08:00:29 | placed 15:45:23 | 0 |
| **exit** | **`2102669411899109376`** | **MARKET SELL, reduce-only** (the armed-exit close) | 0.0017 | **86 116.7** | 09-23 08:00:28 | −0.073199 |

**Income ledger:** REALIZED_PNL **−0.71315**. Fees −0.07355577 − 0.07319919 = **−0.14675496**. FUNDING_FEE ×3 at 09-22 16:00:13, 09-23 00:00:12 and 09-23 08:00:13 = −0.00102778 − 0.00029297 − 0.00029274 = **−0.00161349**.
**Venue net = −0.86151845 USDT.**

**DB row beside it:** gross −0.71315 ✅ · total_fees 0.146755 ✅ · entry/exit prices ✅ · qty ✅ · stop_order_id ✅ · `funding_paid` **0.001321** vs venue **0.001613** · `net_pnl` **−0.861226** vs venue **−0.861518**.

🟡 **ONE DISCREPANCY: −$0.000293, which is 0.00013R.** The DB holds the first two funding charges (0.00102778 + 0.00029297 = 0.00132075, matching to 1e-6). It is missing the **08:00:13** charge, which posted **15 s before the close fill**. `close_report.funding_for_close` reads `fetch_funding_history` at close time. The most likely cause is that the settlement was not yet visible in that read. I cannot prove this: the journal for that minute is no longer retained (§1c).
This contradicts the canon's claim that `funding_paid == −totalFunding to 1e-6 on every one`. That claim now has one sub-cent exception. It is bookkeeping, not a fill, stop or exit fault, so it is below the §5 bar. **No fix written.** Across all 27 DB-matched live round trips, venue minus DB net sums to **−$0.0002**.

## 1b. The trade in numbers

| | value |
|---|---|
| 1R | entry − `original_sl_price` = 86 536.2 − 85 179.8 = **1 356.4 pts**; `initial_risk_usdt` **2.3059** |
| realised | **−0.3736R / −$0.8615** (venue). The DB gives −0.3735R. |
| hold | **16 h 15 m** (15:45:23 → 08:00:28) |
| water mark (stored) | **87 233.5**, so **MFE +0.514R** |
| MFE on BingX 1m | **87 244.6 at 09-23 04:36**, which is **+0.522R** |
| MAE (stored / 1m) | 85 968.8 (**−0.418R**) / 85 952.8 at 09-22 22:12 (**−0.430R**) |
| 🔴 printed +0.25R? | **YES.** The first 1m high ≥ 86 875.3 came at **09-23 03:40**, **11 h 55 m after entry**. It also passed +0.5R (87 214.4) at 04:33. |
| 🔴 reached the +1R arm? | **NO.** The arm was 87 892.6. The peak fell **648 pts (0.478R) short**. `breakeven_applied=false`, so the trail was never armed. |
| life below entry | **755 of 976 1m bars (77 %)** closed below entry |
| peak position in life | 12.85 h of 16.25 h = **79 %** |

## 1c. Alarms during its life

🔴 **The journal cannot be quoted.** `journalctl -u titan` now starts at **2026-09-25 03:35 UTC**, and the trade's whole life (09-22 15:45 → 09-23 08:00) has rotated out. `logs/trading.log` is empty. **I am not quoting journal lines I do not have.**

What the other sources show:
- **The same process ran the whole time:** MainPID **4007821** is the 2026-09-21 19:03:51 restart that loaded `f53d048`, and NRestarts is 0. So every failed-read fix of 2026-09-21 (`7798f51` → `f53d048`) was live for this whole trade.
- **DB, all 235 `trades` rows from entry to exit (34546–34780):** 0 rows with a non-NULL `error`, and 0 rows with any failed-read status (`position_read_failed`, `close_unconfirmed`, `sweep_read_failed`). The statuses were `htf_blocked` 125, `context_recorded` 37, `ema_envelope_blocked` 23, `exit_ai_dryrun` 22 (advisor consults, **all hold**), `confirm_recorded` 19, `exit_unarmed_noop` 4, `below_threshold` 4, `executed` 2, `virt_cap_blocked` 2, `trend_set` 2, `exit_armed` 1.
- **The close sequence is clean and ordered:** 34768/34770 at 08:00:11/17, the 1H trend flipped to `Bearish Confirmation` / `Any Bearish Confirmation` → 34772 at 08:00:26, the advisor was consulted on the armed-exit path and said **HOLD 0.72** → venue fill 08:00:28 → stop cancelled 08:00:29 → row closed 08:00:29.365 → 34773 at 08:00:35, `15m_armed_exit` `Bearish I-CHOCH` `executed`.
- 🟢 **This is the first close ever written as `armed_exit`.** The `40aad46` label is now proven on a live close. vpos 95 and 109 still carry `external`.

**What the DB can see shows no alarm class. The journal cannot be checked either way, and I am not treating its absence as evidence of silence.**

---

# 2. WHY IT ENTERED

## 2a. The full entry record (`trades 34546`, 2026-09-22 15:45:10, `tv_action='Bullish S-CHOCH+'`, 5m)

| tier | name | dir | weight | age vs window | counted by gate? |
|---|---|---|---|---|---|
| **1H** TREND | `Bullish Confirmation+` | LONG | 1.0 | 5.7 h | ✅ **counted** |
| **15m** MOMENTUM | `HyperWave Signal Up` | LONG | 0.7 | 30 of 90 min | ⚪ **NOT counted: `intra_conflict`**. LONG 1.75 / SHORT 1.75 across 2 signals; `HyperWave Signal Down` 60 of 90 min was also in the window. |
| **5m** EXECUTION | `Bullish S-CHOCH+` (trigger-capable) | LONG | 1.0 | 0 of 5 min | ⚪ **NOT counted: `intra_conflict`**. LONG 2.50 (`S-CHOCH+`, `Bullish OB Created`) / SHORT 2.00 (`Bearish OB Entered`, 0 of 5 min) |

**Score arithmetic** (rebuilt from `matrix_breakdown_json`, as the canon requires): TREND **+2.5** (3 signals) + MOMENTUM 0 + LIQUIDITY 0 + EXECUTION 0 = **raw 2.5**. Macro `total_gate_adj` **+1.0** comes from crypto news classed **STRONG_POSITIVE** ("Bitcoin ETFs Take N. $1B in a Day as Average H. Returns to Profit", Decrypt, confidence 0.85). **Gated 3.5** against the TREND bar **3.0**, so it passed. **Without the news bump it would have been `below_threshold`.**
🔴 **Only 1 of 3 tiers was counted.** Every close in the 09-16 §3d table (104–108) had 2 of 3.

| gate | verdict |
|---|---|
| **HTF cascade** | **PASS** (tolerate-NEUTRAL). Tiers 1H=LONG, 15m=NEUTRAL, 5m=NEUTRAL. No tier was OPPOSITE. 1H was not neutral, so the 15m-agree rule did not apply. |
| **EMA envelope** (1h, 15m must be `Expanding`) | **PASS**: 1h 0.428 % Expanding, 15m 0.183 % Expanding |
| **Book gate, six columns** | `book_gate_clause` = *(empty, admit)* · `opp_mult` 4.1 · `opp_pctl` **5.0** · `opp_dist_pct` **0.0908 %** · `lean` 0.4895 · `n_supporting` 10 |
| trend_1d / trend_4h | **bull** (ADX 44.5, EMA-gap 2.950 % Expanding) / **bull** (ADX 49.0, 2.261 % Flat). 1h/15m/5m also bull. MTF alignment 4/4. Regime TREND. |

**Not in the prompt, but in the row:** the 60 s tape showed **16.6 % buy share, pressure "sell"** ($15.7k buy / $78.7k sell). This is description only.

## 2b. The advisor: VERBATIM

**Model** `claude-haiku-4-5-20251001` · **decide `execute`, confidence 0.82**

**SYSTEM prompt, verbatim:**
```
You are an automated trading decision module for a BTC/USDT swap bot. You receive multi-timeframe LuxAlgo signal context (1H trend, 15m confirmation, 5m trigger) at the moment 3-way confluence has just fired and the bot is about to place a DCA grid entry on BingX in hedge mode. You also receive real-time market context: pre-trade order book walls and a multi-timeframe Volatility/regime block (ADX on 1h/15m, ATR% of price, EMA-gap compression, market_regime, MTF alignment) plus 5m ATR and volume ratio.

You also receive a 'Higher Timeframes Trend' block: an OHLCV-derived (EMA/ADX) trend label, ADX, and EMA-gap for 1d/4h/1h/15m/5m, independent of the LuxAlgo signals. Treat the 1d and 4h trends as the dominant regime: when they clearly oppose the proposed entry direction, lean toward 'skip' unless the lower-TF confluence is exceptionally strong; when 1d/4h agree with the entry, that is supportive context.

Your job is to gate that entry: vote 'execute' when the context looks coherent, 'skip' when it looks like a chop/false break or contradicts the higher-timeframe regime.

HARD RULE — opposing walls: a limit wall sitting directly above a LONG entry or directly below a SHORT entry is grounds to reply 'skip' ONLY when it is genuinely unusual for this book. Read that off the wall's OWN percentile, printed beside it: at or below the ~50th percentile a wall is ORDINARY and is NOT on its own a reason to skip; the 90th percentile and above is the region the word 'thick' is meant to describe; between the two, weigh it with everything else rather than treating it as decisive. Never judge by the raw multiplier: every book state contains a wall above 4x, so a large ×-figure on its own says nothing.

Respond with ONLY a single JSON object, no markdown, no prose. Fields: decide ("execute"|"skip"), confidence (float 0.0-1.0), reason (string, max 80 chars).
```

**USER prompt, verbatim:**
```
Symbol: BTC/USDT:USDT
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  Bullish Confirmation+  (LONG, weight 1.0, last set 5.7h ago)
  15m: HyperWave Signal Up  (LONG, weight 0.7, last set 30m ago, NOT counted by the gate — this category's own signals disagree (LONG 1.75 / SHORT 1.75 across 2 signals), so it nets NEUTRAL — both sides are inside the MOMENTUM 90-min window (LONG: HyperWave Signal Up 30 of 90 min; SHORT: HyperWave Signal Down 60 of 90 min))
  5m:  Bullish S-CHOCH+  (LONG, weight 1.0, last set 0m ago, trigger-capable, NOT counted by the gate — this category's own signals disagree (LONG 2.50 / SHORT 2.00 across 3 signals), so it nets NEUTRAL — both sides are inside the EXECUTION 5-min window (LONG: Bullish S-CHOCH+ 0 of 5 min, Bullish OB Created 0 of 5 min; SHORT: Bearish OB Entered 0 of 5 min))
  Agreement: 15m and 1H and 5m all point LONG; vs the proposed LONG: 15m+1H+5m agree.
Combo weight: 1.00  (1.00 = untouched. The store moves it by -0.10 per evaluation that lost more than $15 and +0.10 per one that gained more than $20. Those thresholds were set when this bot traded at ~68x its current size; at the current size they are 8-15R, beyond anything a single position here has produced, so this number does not currently move.)
  Based on: no evaluations yet — this is the untouched baseline.
ATR(14) 5m: 182.7608  |  Volume ratio 5m: 1.19x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 39.4 | 15m 12.2
  ATR% of price: 1h 0.681% | 15m 0.344% | 5m 0.211%
  EMA-gap: 1h 0.428% (Expanding) | 15m 0.183% (Expanding)  (Contracting/Flat = compression)
  Market regime: TREND | MTF alignment score: 4
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BULL, ADX 44.5, EMA-gap 2.950% (Expanding)
  4h: BULL, ADX 49.0, EMA-gap 2.261% (Flat)
  1h: BULL, ADX 39.4, EMA-gap 0.428% (Expanding)
  15m: BULL, ADX 12.2, EMA-gap 0.183% (Expanding)
  5m: BULL, ADX 19.8, EMA-gap 0.141% (Expanding)
  MTF alignment vs LONG: 4/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $86,533.95  |  Imbalance ±1%: 0.49 (ask-heavy)  — 49th pct
  Bid walls (>4x avg bucket vol): $86,532.50 — 8th pct (×4.1), $86,502.50 — 98th pct (×13.4), $86,432.50 — 93rd pct (×7.9), $86,382.50 — 34th pct (×4.5), $86,347.50 — 72nd pct (×5.6)
  Ask walls (>4x avg bucket vol): $86,612.50 — 7th pct (×4.1), $86,727.50 — 19th pct (×4.3), $86,827.50 — 24th pct (×4.4), $86,857.50 — 83rd pct (×7.2), $86,957.50 — 24th pct (×4.4)
  Book depth: 1,974 BTC — 19th pct, sampled 43s ago
Order-book PERCENTILE scale (baseline: 101273 snapshots of this same OKX depth-4000 book)
  Each wall's percentile ranks its multiple against the history of
  walls standing in the path on that side of this same book — so the
  walls on a line share one scale, and the nearest wall, the one a
  HARD RULE veto is normally about, is the most exactly ranked.
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile printed with each wall:
  ~50th percentile is ORDINARY and not significant; 90th+ is genuinely thick.

Recent news (last 2h):
[NEU] ECB, EU cenbanks seek changes in MiCA’s minimum bank deposit for stablecoins
[POS] Next for the U.S. SEC: Agency's chief crypto counsel illuminates path for custody
[POS] Bitcoin ETFs Take N. $1B in a Day as Average H. Returns to Profit
[NEG] European central banks push to expand stablecoin yield ban to crypto lending and staking
[POS] Coinbase adds fixed-rate bitcoin-backed loans through Morpho M.
[POS] CME adds Bitcoin C. and Uniswap futures as crypto derivatives push gro

The entry gate has already passed. Tier agreement is stated in the SIGNAL TIERS block above — read it there rather than assuming all three agree. Decide whether the bot should execute the DCA entry now.
```
*(The last news line is cut at "push gro" **in the stored prompt itself**. That is how it was sent, not a truncation in this report.)*

**REASON, verbatim (the full `ai_raw_response`):**
> 1d/4h/1h all BULL with strong ADX (44.5/49.0/39.4); 15m+5m BULL confluence; 1H weight 1.0 untouched; ask wall at entry ($86,613) only 7th pct—ordinary. Volume 1.19x avg supports. Trend aligned 4/4 on lower TFs. No regime contradiction.

### Every checkable claim, checked against the prompt

| claim | prompt says | verdict |
|---|---|---|
| "1d/4h/1h all BULL with strong ADX (44.5/49.0/39.4)" | 1d 44.5, 4h 49.0, 1h 39.4, all BULL | ✅ exact |
| **"15m+5m BULL confluence"** | The trend block does say 15m BULL and 5m BULL, and the `Agreement:` line says all point LONG. **But the SIGNAL TIERS block says both 15m and 5m are "NOT counted by the gate … nets NEUTRAL".** The prompt's last line tells the model to read agreement there and not assume it. | 🟡 **Half-read.** The claim is supported by two lines of the prompt and contradicted by the block the prompt says is authoritative. A sibling consult on the **same second** (34547, `Bullish OB Created`) read it correctly: *"15m/5m neutral internally but not vetoing."* |
| "1H weight 1.0 untouched" | 1H weight 1.0. "untouched" is the **Combo weight 1.00** line. | 🟡 two facts merged; harmless |
| "ask wall at entry ($86,613) only 7th pct—ordinary" | $86,612.50, 7th pct | ✅ |
| "Volume 1.19x avg supports" | 1.19x | ✅ |
| "Trend aligned 4/4 on lower TFs" | "MTF alignment vs LONG: 4/4 (4H/1H/15m/5m)" | ✅ |
| "No regime contradiction" | 1d/4h BULL | ✅ |

🔴 **Did it repeat the SOL 2026-09-23 defect ("no opposing ask walls" while the prompt listed five)? NO.** The prompt listed **five** ask walls, including an **83rd-pct ×7.2 at 86 857.5** (+321 pts, **+0.24R**). The reason names only the nearest (7th pct) and **makes no claim that the others are absent**. It left out the 83rd-pct wall, the ask-heavy imbalance (0.49, 49th pct) and the thin book (19th pct), but it asserted nothing false about them. **Its one real misreading is the tier line above, not the walls.**

## 2c. The 5m trigger

**`Bullish S-CHOCH+`.** It is **NOT** the watched name. **By the pre-registered definition (trigger = the entry row's `tv_action`), the `Bullish OB Created` live count STAYS AT 4 of the 8 needed.** No update. (vpos 109–111 were triggered by `Bullish S-BOS`, `Bullish I-BOS` and `Bullish OB Mitigated`, so none of them counts either.)

🔴 **But the record should show what happened in the same second.** `trades 34547`, **`Bullish OB Created`**, arrived at 15:45:10. The advisor returned **`execute` 0.78**, and the row was stopped only by **`virt_cap_blocked`**: `S-CHOCH+` had taken the one position slot first. (`34548 Bullish I-BOS` did the same at 15:45:11.) **Had the race gone the other way, this would be the watched name's 5th live entry and its 5th loss.** The count is a count of triggers, so it stays at 4. This is stated here so no later pass double-counts or misses it.

## 2d. Swing high above entry (BingX 1h, closed bars only, no look-ahead)

- **Nearest confirmed swing high above entry: 87 368.0 at 2026-09-21 20:00 UTC.** It is a ±12 h fractal, confirmed at 09-22 08:00, 7.75 h before entry. It is also the **highest high in the whole pre-entry dataset** (08-20 onward), so it sits **+831.8 pts = +0.613R** above entry.
- No ±24 h or ±48 h swing high above entry was confirmable before entry. The ±24 h version of the same peak confirms only at 09-22 20:00, **after** entry.
- **The +1R arm (87 892.6) sat BEYOND it, by 524.6 pts (0.387R).**
- **Price peaked at 87 244.6, 123.4 pts under that high, and never broke it.**
- **Recorded descriptively only.** On SOL on 2026-09-23 this measure did not separate winners from losers. One Titan trade does not change that.

---

# 3. WHY IT LOST

## 3a. 🔴 Entry-price failure or exit failure?

**It is NOT the never-+0.25R shape.** It printed +0.25R (at 11.9 h) and +0.5R (at 12.8 h). **Peak +0.51R (stored water mark) / +0.52R (1m). Close −0.37R. Given back: 0.89R.**
Under the brief's split, that puts it in the **"peaked and gave it back"** class. This is the 09-16 row *"reached ≥ +0.5R and still finished NEGATIVE"*, which now reads **87, 91, 95, 98, 112: 5 trades, ΣR −2.090**.

**But the exit did not fail, and the numbers say so:**
1. The +0.51R peak was **below the arm**. By design nothing protects 0–1R. Arming earlier was measured at **−15.11R** (2026-08-24) and arming later at **−10.13R** (2026-08-31). Both are settled and I have not re-run them.
2. **The exit that fired was the best one available.** The armed exit took −0.3736R. **Held, the position hit its original stop 85 179.8 at 09-23 14:10**, for **−1.0633R / −$2.4518** (canon fee method, taker 0.0005 both legs). The arm never printed after the close either: the post-exit high was 86 240.0 at 08:22. **The armed exit saved +0.6897R / +$1.59.** The advisor, consulted at 08:00:26, said **HOLD**: *"asymmetric risk/reward favours holding to the armed trail at +1R (87892.6)"*. Had its verdict been read, it would have cost those 0.69R.
3. **The entry shape explains most of it.** Admitted on 1 of 3 tiers, below the raw bar, and only via a news bump. MAE −0.43R came first (6.5 h in). **77 % of its life was below entry.** It peaked once, for about an hour, just under a pre-entry swing high, and reversed.

**Plainly: this is a strategy loss. The entry was marginal. It bought the top of a 33-day range into a one-hour push that failed under the prior high. The mechanical exit cut it at a third of its risk.**

**Updated 09-16 §3b(i) split, live book vpos 86–112 (27 positions; R from venue net / DB risk):**

| class | n | ΣR |
|---|---|---|
| never printed +0.25R (adds **110**: water mark +0.06R) | **12** | **−8.703** |
| reached ≥ +0.5R and finished negative (adds **112**) | **5** | **−2.090** |
| all live losers | **19** | **−11.353** |
| never-+0.25R share of losses | | **76.7 %** (was 76.9 %) |

The entry-side finding of 09-16 is unchanged. vpos 112 does not belong to it, and vpos 110 does.

## 3b. Overshoot beyond the stop

**Not applicable: it did not stop out.** The live position's low was 85 952.8, **773 pts (0.57R) above the stop**.
*For the record only, on the held counterfactual:* after the stop would have fired at 14:10, price ran on to **82 845.7 at 09-24 09:35**, which is **1.72R beyond the stop**. That is above the 1.49R floor of the 2026-08-30 pass, unlike vpos 110's 0.30R. It is a hypothetical stop, so it is **not added** to that population.

## 3c. Advisor counterfactual

**Not computed for the ledger, and it stays out.** The armed exit closed it (`close_reason='armed_exit'`). The advisor was consulted on that path and its verdict was **discarded**. Under the 2026-09-21 second ruling this is not an advisor decision. It has the same shape as vpos 99 (hold, then armed-exit close), except that the verdict here was hold.
**Ledger: 5 RESOLVED of 10, Σ +1.0497R / +$1.72. Unchanged. `EXIT_ADVISOR_DRYRUN` stays False.** No `ai_exit` close has happened since vpos 108 (09-14). The four closes since then were external, sl, trail and armed_exit.

---

# 4. THE LIVE BOOK AS IT STANDS (quoted from BingX)

29 round trips on BingX since go-live. **Σ net −$5.0366.** This includes two with no `virtual_positions` row: the first live trade on 07-29 (−$0.2645, `§0.FIRSTLIVE`) and the 09-21 05:30 failsafe round trip (−$0.1930, `§0.VENUE-VS-DB`).

**The 27 DB-matched positions (vpos 86–112), venue net, R = venue net / `initial_risk_usdt`:**

| | n | ΣR | Σ$ | win rate |
|---|---|---|---|---|
| **ALL** | **27** | **−1.8550** | **−$4.5791** | **8/27 = 29.6 %** |
| LONG | 18 | −0.9833 | −$2.2310 | 6/18 = 33.3 % |
| SHORT | 9 | −0.8717 | −$2.3480 | 2/9 = 22.2 % |

By close reason: `ai_exit` 15 / −0.9062R · `sl` 5 / −5.6138R · `trail` 3 / **+4.0979R** · `external` 3 / +0.9408R · `armed_exit` 1 / −0.3736R.
Since the 09-16 pass (vpos 109–112): n 4, **ΣR +3.3246, +$5.59**, 2 of 4 wins.

**Last five closes:**

| vpos | side | closed (UTC) | reason | R | $ |
|---|---|---|---|---|---|
| 108 | LONG | 09-14 17:00 | ai_exit | +1.1371 | +1.5364 |
| 109 | LONG | 09-18 23:45 | external (armed exit) | +2.0051 | +3.4340 |
| 110 | LONG | 09-21 01:51 | sl | −1.1228 | −1.6172 |
| 111 | LONG | 09-21 10:29 | trail | **+2.8159** | +4.6366 |
| **112** | **LONG** | **09-23 08:00** | **armed_exit** | **−0.3736** | **−0.8615** |

**Exit-advisor ledger:** 5 RESOLVED of 10, Σ **+1.0497R / +$1.72**. Rule does not fire; five more required.
**Book gate:** counter **57 / 200** against the review (15 DRYRUN + 42 ARMED since 2026-09-10 14:36:20; 20 `open_long` / 22 `open_short` armed). **Refusals: 0 in the armed era, 0 ever.**

---

# 5. VERDICT

**No mechanical defect. No fix written, nothing to apply.**
- No false alarm: none is visible in the DB. The journal is not retained, and I said so rather than claim silence.
- No dropped exit: the armed exit fired once, inside its TTL, and the close was confirmed at the venue.
- No wrong fill: venue and DB agree on price, qty, fees and realised PnL.
- The stop was placed at the designed 85 179.8, never touched, and cancelled after the close.
- The only discrepancy is a **$0.0003 funding charge** that posted 15 s before the close and is missing from the DB. It is named in §1a and left for your decision. It affects no order.

**It is a strategy loss.** The entry was marginal: 1 of 3 tiers, raw 2.5 under the 3.0 bar, cleared by a +1.0 news bump. It rallied to +0.51R once, under a pre-entry swing high, then reverted. The mechanical exit cut it at −0.37R, where holding would have taken −1.06R. **No filter is proposed. One trade is not evidence, and thirty-three entry candidates have already died on these books.**

## Confirmations

- **Writes:** scratchpad files only (`venue_112.json`, `candles.json`, `book_raw.json`, `book_rows.json`, the scripts, this report); this report published to `kola-reports`; one Telegram message. **No write to `trades.db`** (every open was `file:…?mode=ro` + `PRAGMA query_only=1`). **No canon edit.** No code or config change.
- **Venue:** GET only (`allOrders`, `allFillOrders`, `user/income`, `user/positions`, `openOrders`, public OHLCV). No read failed, so no Tor retry was needed and no figure is a 0 from an exception. **0 orders placed, 0 cancelled.**
- **No restart.** titan MainPID 4007821, **NRestarts 0**. mercury-sol MainPID 222221, **NRestarts 0**. Both the same at the start and end of the pass.
- `EXIT_ADVISOR_DRYRUN = False`, `BOOK_GATE_DRYRUN = False`, `BOOK_GATE_ENABLED = True`: **untouched.**
- **Mercury-SOL untouched:** not read, not opened, not queried.
- Book **flat** at report time: BingX 0 positions / 0 open orders, DB 0 open rows / 0 `exit_pending`.
