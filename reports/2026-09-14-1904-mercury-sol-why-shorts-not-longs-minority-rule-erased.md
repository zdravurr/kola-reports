# mercury-sol-why-shorts-not-longs-minority-rule-erased

_2026-09-14 19:04 UTC_

---

# Mercury-SOL: why shorts and not longs, and what the minority rule erased

**2026-09-14 · READ-ONLY · nothing proposed, nothing applied** · `openitems_guard` EXIT 0 (titan-bot HEAD `f16c271`, 14 watched values)

The trade is **vpos 45**, LIVE. SHORT 99.56 → 101.24, stopped. Net **−$1.8808 = −1.133R**. The live book went from +$15.5975 to **+$13.7167** in the DB. Entry row `trades.id 26586`, 2026-09-14 00:50:01 UTC, fill 00:50:16.

> **CONTROLS, DECLARED IN THE HEADER**
> * **Family (Bonferroni): 26 cells, α = 0.05/26 = 0.00192.** That is 4 entry shapes (erased opposition; entry against the card's tape; entry against the pre-gate tape; 15m tier not agreeing) × 3 cells (ALL/LONG/SHORT) × 2 books, plus 2 side contrasts (SHORT vs LONG, one per book).
> * **Paper and live are never pooled.** Paper is the independent sample.
> * **No cell is ranked unless both legs have n ≥ 8.**
> * A contrast **survives** only if all four hold: the permutation p clears α; the sign is the same in both chronological halves of its book; the sign is the same in the TREND and FLAT regimes; and the sign is the same on paper and live.
> * Book: 39 closed `virtual_positions`, **17 live (vpos 29–45) and 22 paper (vpos 7–28)**. R = `net_pnl / initial_risk_usdt`.

---

## VERDICT

🔴 **Nothing is mechanically wrong, and nothing here explains the stop-outs. The shorts simply lose.**

**1. The bot does not confuse longs with shorts.**
- In the DB, the traded side, the side the gate scored, `trades.side`, `signal_type` and `virtual_positions.side` agree on **39 of 39** entries.
- At the venue, Bybit `closed-pnl` (signed GET) shows **8 SHORT closes and 9 booked LONG positions**. Every one matches the DB side, entry and exit. The short side matches **to the cent**: venue −$10.5994, DB −$10.5994.

**2. The minority rule did erase vpos 45's LIQUIDITY +2.50 LONG. It changed no decision, here or anywhere.**
- The score gate reads **only the proposed side's points**. It never subtracts the other side, whether the rule fires or not.
- Of 8,242 scored rows that reached the bar, 1,696 carried an opposing category:
  - the rule zeroed it on **598**;
  - it kept it on **1,098** (1–1 category ties).
  - The gate ignored the opposition in exactly the same way in both groups.
- Removing the rule changes the proposed score on 0 current-funnel rows and the matrix winner on **0** rows at the bar.
- So the contested board was not passed by the minority rule. It was passed by a gate that has never netted opposition. The rule only changes what the card's header and `long_score`/`short_score` print.
- **The advisor never saw it either.** LIQUIDITY is not one of the tiers the entry prompt shows. vpos 45's prompt contains neither "LIQUIDITY" nor "Liquidity Grab". Since the matrix line first appeared in a prompt (2026-09-11 19:40), **0 of 213** entry prompts carried a "ZEROED as the minority" line.

**3. The 2026-08-22 conclusion stands, and it answered a different question.**
- It proved the rule cannot take points from the **proposed** side at the bar. That is still true: 0 rows in the current funnel.
- This card shows it taking points from the **opposing** side. Both are true at once.

**4. The tape is narration.** No gate, no prompt and no weight reads it. The card's "Buy 0.67" was captured **after the fill**. This is the same class as the order book before the book gate existed. Entering against it does not separate outcomes: p = 0.68 live and 0.21 paper, and in every rankable cell the sign is "against the tape did *better*".

**5. The short book.**
- **Live SHORT: 0 wins in 8. ΣR −6.832, −$10.5994.** Venue-confirmed. No live short ever reached +1R; the best was vpos 42 at about 0.73R.
- **Live LONG: 7 of 9. ΣR +12.453, +$24.3161 in the DB (+$23.9987 at the venue).**
- The 09-11 reading was 0 of 7 (−5.699R); vpos 45 makes it 0 of 8.

**6. The SHORT-vs-LONG gap is real on the live book and fails the independent sample.**
- Live: p = 0.0011 < α. The sign holds in both halves and in both regimes.
- **On paper the sign flips.** Paper SHORT mean is −0.102R, paper LONG −0.450R, p = 0.42.
- It does not survive, so it is not a side mechanism. It is the market the live book traded:
  - SOL went from **73.63 to 103.58** over the live era (high 110.61);
  - the last daily close classified BEAR was **2026-08-06**, two days before live trading began;
  - **not one live short was entered with the daily BEAR** (2 BULL, 6 NEUTRAL).

**7. Why shorts and not longs *now*: the daily has not turned BEAR. It went BULL → NEUTRAL on 09-09/10.**
- Every entry-advisor consultation since the 09-11 count reads NEUTRAL (**247 of 247** since 09-11 05:06). BEAR is still 0 since 08-10.
- Over the last 14 days the advisor admitted:
  - **1 LONG** of 375 consultations, with 1d BULL and 4h BULL;
  - **3 SHORTs** of 348, **all with 1d NEUTRAL and 4h BEAR**.
- With the daily NEUTRAL, only **2 of 195** LONG consultations had a BULL 4h, and neither was admitted.
- So the picture is **half-inverted**. Longs lost the daily's support, shorts lost the daily's opposition, and neither side has the daily with it.
- What the advisor now lets through is a 4h dip inside a daily that is still EMA-stacked bull. The three shorts it admitted were all stopped out.

---

## 0. THE TRADE, RE-READ FROM THE RECORD

| field | value |
|---|---|
| row / fill | `trades.id 26586`, 2026-09-14 00:50:01, vpos 45 opened 00:50:16, closed 03:12:07 |
| entry → exit | SHORT 99.56 → 101.24 (venue: avgEntry 99.56, avgExit 101.24, closedPnl −1.8808) |
| stop | 101.22 = entry + **2.5 × ATR(1h) 0.6654** (`SL_WALL_ANCHOR_ENABLED = False`) |
| R | −1.8808 / 1.66 = **−1.133R**. MFE +0.40 %, MAE 1.66 % |
| combo | `1H:Any Bearish Confirmation\|15M:None\|5M:Within Bearish OB` |
| OHLCV trends at consult | 1d **neutral** · 4h bear · 1h bear · 15m bear · ADX(1h) 20.2 · regime TREND |
| advisor | execute: *"4H/1H/15m align BEAR; 1H ADX 20.2 (weak) but EMA expanding; ask wall $99.75 (p72, ordinary) poses no hard block; 5m volume thin (0.53x) but confluence solid; 1d neutral does not contradict."* |

**The matrix at scoring**, from `trade_signal_matrix.active_signals_json`:

| category | signals inside window (weight, age) | raw | net | after minority rule |
|---|---|---|---|---|
| TREND | Bearish Confirmation+ (1.0, 109.9 min of 360); Any Bearish Confirmation (0.7, 109.9 min) | S 4.25 → cap **2.50** | SHORT | counted +2.50 |
| MOMENTUM | none in the 90-min window | 0 | NEUTRAL | — |
| LIQUIDITY | **Bullish Liquidity Grab (1.0, 19.8 min of 30); Bullish Imbalance Mitigated (0.5, 19.8 min)** | L 3.75 → cap **2.50** | **LONG** | 🚫 **zeroed** (2 SHORT categories vs 1 LONG) |
| EXECUTION | Within Bearish OB (0.7, 0.0 min) | S **1.75** | SHORT | counted +1.75 |

**The gate compared** `direction_score` 4.25 + macro 0.0 = **4.25 ≥ 2.0**. The card's "adj −0.11 → 4.14" is `weighted_adj`, which is storage-only (main.py:4484-4486).

- **The prompt the advisor judged** showed three tiers: `1H: Any Bearish Confirmation -> SHORT = AGREES`, `15m: ABSENT`, `5m trigger: Within Bearish OB -> SHORT = AGREES`.
- Its matrix line read `1H → TREND SHORT +2.50, counted | 15m → MOMENTUM 0, no signal inside its 90-min window | 5m trigger → EXECUTION SHORT +1.75, counted`.
- **The LONG liquidity grab 20 minutes earlier appears nowhere in it.**

---

## 1. THE MINORITY RULE

### 1a. The rule, verbatim

`signal_matrix.py:318-343`, inside `compute_score`:

```python
318    long_cats  = sum(1 for b in breakdown.values() if b['net_direction'] == LONG)
319    short_cats = sum(1 for b in breakdown.values() if b['net_direction'] == SHORT)
320    majority   = (LONG if long_cats > short_cats
321                  else SHORT if short_cats > long_cats
322                  else NEUTRAL)
323
324    long_total = short_total = 0.0
325    for cat, b in breakdown.items():
326        nd = b['net_direction']
327        if nd == NEUTRAL:
328            continue
329        if majority != NEUTRAL and nd != majority:
330            b['inter_conflict'] = True
331            b['contribution']   = 0.0
332            continue
333        if nd == LONG:
334            long_total  += b['contribution']
335        else:
336            short_total += b['contribution']
337
338    if long_total > short_total:
339        direction, score = LONG,  long_total
340    elif short_total > long_total:
341        direction, score = SHORT, short_total
342    else:
343        direction, score = NEUTRAL, max(long_total, short_total)
```

**When it fires:** a category is intra-conflicted (holds both LONG and SHORT signals) when it has points on both sides; that happens earlier (:299-301) and turns the category NEUTRAL. The rule then counts **categories, not points**, among the remaining LONG and SHORT categories. If one direction holds strictly more categories, **every category pointing the other way has its `contribution` set to 0 and is flagged `inter_conflict`**. On a tie (1–1 or 2–2), nothing is zeroed.

- `net_direction`, `long_points` and `short_points` are **not** changed. That is why the cascade, which reads `net_direction`, is unaffected, and why the erased weight is recoverable from the stored breakdown.

**Who reads what it changes:**

| consumer | code | reads |
|---|---|---|
| **score gate** | `main.py:4370-4371` `direction_score = signal_matrix.score_for_direction(matrix_result, direction)`; `main.py:4675-4676` `_gate_score = direction_score if MACRO_GATE_DRYRUN else _macro_gated_score` / `if _gate_score < _thr:` | **only the proposed side's total** (`signal_matrix.py:361-366`) |
| HTF cascade | `signal_matrix.py:369-399` | `net_direction` of TREND/MOMENTUM/EXECUTION: untouched by the rule |
| entry card | `signal_matrix.py:521-534`: `matrix net={res['score']} → {res['direction']}` and `🚫 minority-{b['net_direction']} zeroed (was +{raw:.2f})` | winner, winner score, the zeroed line |
| advisor prompt | `claude_advisor.py:887-888` `_shown = ([('1H', _h1)] if not AI_ADVISOR_HIDE_1H else []) + [('15m', _m15), ('5m trigger', _m5)]` (`AI_ADVISOR_HIDE_1H = False` on SOL); `:527-529` renders `ZEROED as the minority direction across categories` **only for a shown tier's category** | never LIQUIDITY unless the 5m trigger itself is a LIQUIDITY signal (in which case it is the proposed side) |
| storage | `trade_signal_matrix.score/direction`, `trades.matrix_direction` | winner |

### 1b. 🔴 The reading is confirmed from the code, and the earlier conclusion answered a different question

At any row that reaches the score bar, the cascade has already guaranteed that TREND, MOMENTUM and EXECUTION are each NEUTRAL or on the proposed side. **The only category that can oppose the proposal there is LIQUIDITY.** With k categories for the proposal and one opposing LIQUIDITY:

- **k ≥ 2:** majority is the proposal, so **the opposing LIQUIDITY is zeroed**. This is vpos 45: k = 2 (TREND, EXECUTION) against LIQUIDITY LONG 2.50. `long_score` prints 0.00 instead of 2.50, and the card header prints `matrix net=4.25/10 → SHORT`.
- **k = 1:** tie, so both sides keep their points. The matrix winner can then be the **opposite** side (vpos 13, vpos 35).

**So at the bar, the rule removes points only from the OPPOSING side.**

- The 2026-08-22 pass (`reports/2026-08-22-0300-titan-third-lock-does-not-exist-minority-rule-cannot-bind.md`) asked whether the rule can take points from the proposed side at the bar, and answered no: 0 of 781 on Titan, 0 of 5,288 on SOL. **That is correct and still holds.**
- It did not ask whether the rule erases opposition from the board. It does, on 598 bar rows.
- **Both statements are true together. The earlier conclusion answered a different question.**

**What the erasure costs in decisions: nothing, and the reason is the gate, not the rule.**

| rows that reached the score bar (stored breakdown, 2026-06-07 → 09-14) | n |
|---|---|
| total | **8,242** |
| with a non-NEUTRAL category opposing the proposal | **1,696** |
| … opposition **zeroed** by the rule | 598 |
| … opposition **kept** (category-count tie) | 1,098 |
| proposed score changes if the rule is removed | **3**: all `no_confluence` rows 2026-06-07/08, before the HTF-cascade/score-gate funnel existed |
| matrix winner changes if the rule is removed | **0** |
| rows where the rule zeroed the **proposed** side | 3: the same `no_confluence` rows |

On the 1,098 kept rows, the gate ignored the opposition exactly as it did on the 598 zeroed ones. The gate never nets.

- **Why the winner cannot flip at the bar:** the zeroed LIQUIDITY is at most 2.50 (the category cap). Two supporting categories are worth at least 1.25 + 1.50 = 2.75 under the dictionary's minimum weights. Measured: 0 flips.
- **Fidelity:** the rule re-implemented from stored `long_points`/`short_points` reproduces the stored `inter_conflict` flags on **18,103 of 18,103** rows.

### 1c. Across SOL's whole record: how often it zeroed an opposing category, per side, and the weight erased

18,103 `open_long`/`open_short` rows carry a stored breakdown, from 2026-06-07 20:10 to 2026-09-14 18:45.

**Coverage caveat:** 1,591 rows past the bar carry no stored breakdown and are not in these counts: `risk_halt` 611, `entry_gate_refused` 563, `flat_adx_blocked` 372, `book_blocked` 45.

**Reached the score bar** (below_threshold, ai_skipped, executed, observed_skipped, no_confluence, failed, sl_failed, claude_unavailable):

| side | rows | **opposing category zeroed** | which category | erased weight: 1.25 / 1.75 / 2.25 / 2.50 | median · mean | erased ÷ proposed score: median · max |
|---|---|---|---|---|---|---|
| LONG | 3,953 | **250 (6.3 %)** | LIQUIDITY 247, TREND 3* | 39 / 53 / 16 / **142** | 2.50 · 2.130 | 0.50 · 0.83 |
| SHORT | 4,289 | **348 (8.1 %)** | LIQUIDITY 347, MOMENTUM 1* | 66 / 85 / 25 / **172** | 2.25 · 2.062 | 0.50 · 0.83 |
| ALL | 8,242 | **598 (7.3 %)** | LIQUIDITY 594 | 105 / 138 / 41 / **314** | 2.50 · 2.090 | 0.50 · 0.83; never ≥ 1.0 |

\* The 4 non-LIQUIDITY zeroings at the bar are all `no_confluence` rows from 2026-06-07/08, before the cascade funnel.

- By month (bar rows, opposing zeroed): June 146 / 973 · July 247 / 3,393 · August 111 / 2,487 · September 94 / 1,389.

**Killed by the cascade first** (`htf_blocked`, 9,861 rows):
- opposing category zeroed on 2,744 (LONG 1,442, SHORT 1,302; MOMENTUM 1,392, TREND 1,245, EXECUTION 106, LIQUIDITY 1), median erased 2.50;
- **proposed side zeroed on 1,466**, all of them already dead.

On the dead rows the rule is bookkeeping, as the 08-22 pass said.

### 1d. 🔴 ENTRIES where the opposing side was zeroed by this rule

**Live, n = 2:**

| vpos | side | opened | zeroed | erased | proposed raw | erased ÷ raw | R |
|---|---|---|---|---|---|---|---|
| 32 | SHORT | 08-10 15:15 | LIQUIDITY LONG | 2.50 | 4.25 | 0.59 | **−0.180** |
| **45** | SHORT | 09-14 00:50 | LIQUIDITY LONG | 2.50 | 4.25 | 0.59 | **−1.133** |

**Paper, n = 5:**

| vpos | side | opened | zeroed | erased | proposed raw | erased ÷ raw | R |
|---|---|---|---|---|---|---|---|
| 14 | SHORT | 06-25 14:00 | LIQUIDITY LONG | 1.25 | 3.75 | 0.33 | −1.032 |
| 18 | LONG | 07-14 15:45 | LIQUIDITY SHORT | 2.50 | 6.25 | 0.40 | −1.074 |
| 19 | SHORT | 07-16 00:25 | LIQUIDITY LONG | 2.50 | 4.25 | 0.59 | +0.463 |
| 21 | LONG | 07-19 06:50 | LIQUIDITY SHORT | 2.50 | 4.75 | 0.53 | +0.285 |
| 24 | SHORT | 07-29 20:05 | LIQUIDITY LONG | 2.50 | 5.00 | 0.50 | −1.050 |

**Entries where an opposing LIQUIDITY was present but kept (tie):** live vpos 35 (−0.701), 36 (−0.757); paper vpos 7 (+2.089), 11 (+1.133), 13 (+1.337).

### 1e. OUTCOMES: erased opposition vs none (n first; below n = 8 not ranked)

| book | side | erased opposition | no erased opposition |
|---|---|---|---|
| live | LONG | n = 0 | n = 9 · ΣR +12.453 · 7/9 · mean +1.384 |
| live | SHORT | n = 2 · ΣR −1.313 · 0/2 · mean −0.656 · **NOT RANKED** | n = 6 · ΣR −5.519 · 0/6 · mean −0.920 · **NOT RANKED** |
| live | ALL | n = 2 · ΣR −1.313 · 0/2 · **NOT RANKED** | n = 15 · ΣR +6.934 · 7/15 · mean +0.462 |
| paper | LONG | n = 2 · ΣR −0.789 · 1/2 · **NOT RANKED** | n = 7 · ΣR −3.257 · 1/7 · **NOT RANKED** |
| paper | SHORT | n = 3 · ΣR −1.619 · 1/3 · **NOT RANKED** | n = 10 · ΣR +0.291 · 5/10 · mean +0.029 |
| paper | ALL | n = 5 · ΣR −2.408 · 2/5 · **NOT RANKED** | n = 17 · ΣR −2.966 · 6/17 · mean −0.174 |

**Nothing is ranked: the largest erased cell is n = 5.**

- Widening to *any* opposing category (zeroed or kept): live 4 (ΣR −2.770, 0/4) vs clean 13 (+8.391, 7/13); paper 8 (**+2.151**, 5/8) vs clean 14 (−7.525, 3/14).
- The sign **inverts between the books**. On paper, an opposed entry did better.

---

## 2. 🔴 DOES IT CONFUSE LONGS WITH SHORTS?

### 2a. Traded side vs scored side, every entry

⚠️ **A correction to the premise, stated first.** The "6 of 93 rows where the matrix winner was the opposite side, two of them entries" finding came from a **Mercury-SOL** pass (`reports/2026-09-11-1714-mercury-sol-the-entry-that-rested-on-one-signal.md` §3b: vpos 13 paper, vpos 35 live), not Titan. Titan was not opened in this pass. The check was re-run on SOL.

**The side the gate scored = the traded side, by construction and by record:**
- **Code:** the gate compares `score_for_direction(matrix_result, direction)`, where `direction` is the webhook's proposed side and becomes `position_side`.
- **Record:** stored `trades.confluence_score` equals the raw score of the **traded** side, recomputed from the stored breakdown, plus `weighted_adj`, on **38 of 38** entries that carry it. vpos 29's entry row is status `failed`, with no adj stored.
- `trades.side`, `signal_type`, `virtual_positions.position_side` and `virtual_positions.side` agree on **39 of 39**.
- The price-move sign agrees with the P&L sign on **38 of 39**. The exception is vpos 33: LONG 76.50 → 76.61, gross +$0.143, fees $0.199, net −$0.0677. That is fees, not a side error.

**The matrix *winner* vs the traded side:**

| | n |
|---|---|
| `trade_signal_matrix` rows | 96 (93 at the 09-11 pass) |
| winner is the **opposite** side | **6**: rows 4180, 4182, **4370 = vpos 13 (paper, +1.337R)**, 11698, 11700, **18345 = vpos 35 (live, −0.701R)**. The same six as on 09-11; **none new** |
| winner is **NEUTRAL** (exact tie) | 7: rows 1919, **1920 = vpos 7 (paper, +2.089R)**, 4388–4391, **18578 = vpos 36 (live, −0.757R)** |
| **vpos 45** | winner SHORT 4.25 = traded SHORT ✅ |

- Every winner≠traded case is a **1–1 tie in which the rule did not fire** and an opposing LIQUIDITY outweighed or equalled the proposal.
- The bot traded the proposed side, which is what the gate scores. This is the stored winner being a different quantity from the gate's, not a side swap.

**At the venue, non-circular.** Bybit `GET /v5/position/closed-pnl` (SOLUSDT, 2026-08-07 → now) returned 21 records:
- **8 SHORT closes** (Buy-side close orders) = vpos 32, 34, 35, 36, 37, 42, 44, 45, each entry, exit and closedPnl identical to the DB. **Σ −$10.5994 = DB.**
- **13 LONG close records** (Sell-side) = vpos 29 (2 legs), 30 (2 legs), 31, 33, 38, 39, 40, 41, 43, plus **2 LONG emergency closes on 08-08 06:50 and 08:35** with no book row (see "Found on the way").
- **No live position was ever the opposite side of what the DB says.**

### 2b. Entry counts by side

| book | window | LONG | SHORT |
|---|---|---|---|
| live | record (08-08 → 09-14) | 9 | 8 |
| live | last 14 days (since 08-31 18:48) | **1** (vpos 43) | **3** (vpos 42, 44, 45) |
| paper | record (06-14 → 08-06) | 9 | 13 |
| paper | last 14 days | 0 | 0 (the paper book ended 08-07) |

### 2c. 🔴 WHY NOT LONGS? Every LONG proposal in the last 14 days and where it died

Window: since 2026-08-31 18:48 UTC. A proposal is an `open_long`/`open_short` row, plus a 5m Group-A signal that died before the matrix (`5m_no_trend`, `5m_entry_suppressed_armed`, side from the signal name). SHORT is shown beside for symmetry.

| where it died | LONG | SHORT | verbatim reason (the bot's own strings) |
|---|---|---|---|
| **HTF cascade** `htf_blocked` | **636** | 703 | reconstructed in `_htf_cascade_gate`'s own format: LONG `"LONG blocked — 15m tier OPPOSES (needs LONG) [opposite]"` **317**, `"… 1H tier OPPOSES …"` **294**, `"… 5m tier OPPOSES …"` **25**. SHORT: 15m 391 · 1H 287 · 5m 25 |
| **entry advisor** `ai_skipped` | **374** | 345 | samples below |
| **score bar** `below_threshold` | **334** | 333 | LONG raw/macro most common: raw 1.75 + macro 0 (**131**), raw 0 (77), raw 1.75 + macro −1.0 (43), raw 0 + macro −1.0 (23), raw 2.50 + macro −1.0 (18) |
| duplicate webhook `entry_gate_refused` | 119 | 105 | `"concurrent LONG entry already in flight for SOL/USDT:USDT — refused, not queued"`. 221 of 224 have a same-side sibling row within 5 s, so they are **not independent proposals** |
| 1h trend not set `no_trend` | 82 | 101 | 5m signals: `Within Bullish OB` 32, `Bullish OB Entered` 14, `Bullish OB Mitigated` 8, `Bullish Imbalance Mitigated` 6 |
| flat-ADX gate `flat_adx_blocked` | 54 | 27 | e.g. `"flat market: 1h ADX 18.96 below the 20 floor — no trend, no trade"`. **All before 09-03 14:55. 0 since DRYRUN (19:30)** |
| risk gate `risk_halt` | 29 | 67 | `"max 1 LONG position(s) already open"` ×29 (during vpos 43). SHORT: `"max 1 SHORT position(s) already open"` ×64 + 3 macro blackouts |
| book gate `book_blocked` | 6 | 0 | e.g. `"book leans 0.421 against this side (< 0.424 = p2 for LONG)"`, `"… 0.388 …"`, `"… 0.400 …"`, `"… 0.383 …"` |
| `entry_suppressed_armed` | 6 | 2 | `Bullish Liquidity Grab` 4, `Bullish I-CHOCH` 1, `Bullish I-CHOCH+` 1 |
| **executed** | **1** | **3** | |
| **total** | **1,641** | **1,686** | |

**The two sides die in the same places at the same rates.** Only the advisor's four executes differ.

**Split by what the daily read:**

| window | LONG consults → executes | SHORT consults → executes |
|---|---|---|
| 08-31 → 09-08 (daily BULL) | 189 → **1** | 173 → **1** |
| 09-09 → 09-14 (daily NEUTRAL) | 186 → **0** | 175 → **2** |

**Advisor verdicts, last 14 days, by (1d, 4h):**

| side | 1d | 4h | skip | execute |
|---|---|---|---|---|
| LONG | bull | bull | 55 | **1** (vpos 43) |
| LONG | bull | neutral / bear / n/a | 81 / 42 / 1 | 0 |
| LONG | neutral | bear | 74 | 0 |
| LONG | neutral | neutral / bull / n/a | 117 / **2** / 2 | 0 |
| SHORT | bull | any | 191 | **0** |
| SHORT | neutral | **bear** | 67 | **3** (vpos 42, 44, 45) |
| SHORT | neutral | neutral / bull / n/a | 81 / 4 / 2 | 0 |

**Every execute in 14 days had the 4h agreeing and the daily not opposing.**
- A LONG needed a BULL 4h. With the daily NEUTRAL, only **2 of 195** LONG consultations had one.
- A SHORT needed a BEAR 4h. **70** SHORT consultations with a NEUTRAL daily had one, and 3 went through.

**The executes, verbatim:**
- vpos 42 SHORT 09-01 (1d neutral, 4h bear): *"4/4 MTF bear alignment (4h-5m), 15m/5m SHORT agree, strong ADX+trend. 1h rearm stale."*
- vpos 43 LONG 09-05 (1d bull, 4h bull): *"Strong multi-TF bullish confluence (1d-5m all BULL, 4/4 MTF align). 1h ADX 18.5 is weak but 15m ADX 28.0 + expanding EMA-gaps on 1h/15m confirm trend is active. Ask wall at $103.25 (p64, x10.4) is thi"*
- vpos 44 SHORT 09-11 (1d neutral, 4h bear): *"3-tier SHORT confluence (1H/15m/5m all bearish); 1h/4h BEAR regime supportive; 1h ADX 44.5 strong trend; no opposing wall blocks short entry; 15m ADX weak but overridden by lower-TF trigger + higher-T"*
- vpos 45 SHORT 09-14 (1d neutral, 4h bear): *"4H/1H/15m align BEAR; 1H ADX 20.2 (weak) but EMA expanding; ask wall $99.75 (p72, ordinary) poses no hard block; 5m volume thin (0.53x) but confluence solid; 1d neutral does not contradict."*

**LONG skips, 12 verbatim, sampled evenly across the window** (row, 1d/4h/1h):
- 23021 09-01 bull/–/bear: *"1H/15m/5m BEAR regime contradicts LONG; flat market (1h ADX 21.1, MTF align 0) with ask wall p72 above entry blocks upside."*
- 23346 09-02 neutral/bear/neutral: *"4H BEAR + 5m BEAR vs LONG entry; flat regime (ADX 1h=32.6 but EMA contracting, MTF=0); 15m opposes; stale 1H. Skip."*
- 23840 09-04 neutral/neutral/bear: *"1H bearish stale but lower-TF confluence opposes higher-TF regime. 1d/4h/1h/15m all BEAR; MTF=0. FLAT market (regime + MTF align score 0) despite ADX>30. Skip."*
- 24366 09-06 bull/bull/bull: *"1H Reversal Down opposes LONG; massive ask wall (p61, x9.8) at mid blocks upside momentum."*
- 24644 09-07 bull/neutral/neutral: *"FLAT market (ADX 1h 22, ATR% low, EMA-gap contracting 15m) + stale 1H SHORT opposes. Ask wall p84 x15.7 at $105.25 blocks upside. Lower MTF alignment (1/4). Skip."*
- 24856 09-08 bull/neutral/bear: *"Flat market (ADX 19.5/19.5, MTF 0/4), 1h/15m BEAR, massive ask wall x9.8@103.25 blocks entry."*
- 25094 09-08 bull/neutral/neutral: *"FLAT regime (ADX 1h/15m <20, EMA compressed, MTF=0) + 1H stale + ask wall $103.75 p72×12.3 blocks upside"*
- 25333 09-09 bull/bear/bear: *"4h/1h BEAR regime opposes LONG; 1h ADX 14.4 + flat regime + ask wall p79 at entry+ block momentum."*
- 25692 09-11 neutral/bear/neutral: *"4H BEAR regime + 15m opposes + massive ask wall $100.25 (p78) blocks upside. Weak MTF alignment (1/4)."*
- 25925 09-12 neutral/neutral/neutral: *"1H signal STALE (15.4h old, past 6h window); 15m BEAR trend opposes LONG; 1h/4h NEUTRAL regime; ADX weak (1h 19.2); EMA contracting across 1d/4h/1h; massive ask wall at $101.75 (p75, x13.0) blocks ups"*
- 26327 09-13 neutral/neutral/bear: *"4/4 lower TF (4h/1h/15m/5m) trend structure is BEAR; 1h signal STALE 10.5h; flat regime (ADX 1h=9.9, 15m=16.5); thick ask wall p76 x13.4 at $101.75 blocks upside."*
- 26499 09-13 neutral/bear/neutral: *"4H BEAR + 1H NEUTRAL + flat ADX/EMA compression + 15m opposes + weak MTF alignment (0/4)"*

**Keyword counts over all 374 LONG skip reasons:** 1h 339 · ADX/weak/flat/chop 331 · counter/against/oppose 309 · 4h 259 · wall 256 · bear 235 · 1d/daily 113.

**SHORT skips (345):** counter/against/oppose 323 · ADX/flat 321 · 1h 314 · **1d/daily 250** · 4h 179 · wall 146.

> **Reason text is narration, not mechanism** (canon 2026-08-08, `claude_advisor.py:575-593`). These keyword counts describe what the model *wrote*, not why it decided.

**`trend_1d` now, day by day, beside the actual daily candles.**
- Candles: Bybit SOLUSDT linear `1D` (GET via Tor).
- Recompute: the bot's own rule (`indicators.py:322-329`): BULL if close > EMA9 > EMA21 and EMA9 3-bar slope > +0.05 %; BEAR if the mirror; else NEUTRAL. Uses `pandas_ta.ema` and the 200 bars up to each close.
- Stored counts: `trades.trend_1d` is written on the advisor path; `skip_attribution.trend_1d` covers the other refusals.

| date | open | high | low | close | chg % | EMA9 | EMA21 | slope3 % | **recomputed @close** | stored `trades.trend_1d` | stored `skip_attribution.trend_1d` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 08-31 | 101.70 | 105.01 | 100.81 | 102.99 | +1.27 | 100.45 | 92.95 | +2.65 | bull | bull 40 | bull 171 |
| 09-01 | 102.99 | 104.35 | 98.27 | 99.93 | −2.97 | 100.35 | 93.58 | +1.00 | neutral (c<e9) | bull 6, neutral 2 | bull 88, neutral 8 |
| 09-02 | 99.93 | 100.67 | 97.29 | 100.40 | +0.47 | 100.36 | 94.20 | +0.54 | bull | neutral 27 | neutral 103 |
| 09-03 | 100.40 | 105.94 | 99.13 | 103.87 | +3.46 | 101.06 | 95.08 | +0.60 | bull | bull 6, neutral 7 | bull 53, neutral 45 |
| 09-04 | 103.87 | 104.73 | 100.01 | 101.85 | −1.94 | 101.22 | 95.70 | +0.86 | bull | bull 47, neutral 4 | bull 91, neutral 6 |
| 09-05 | 101.85 | 104.34 | 101.52 | 103.11 | +1.24 | 101.60 | 96.37 | +1.22 | bull | bull 61 | bull 69 |
| 09-06 | 103.11 | 107.32 | 103.10 | 106.49 | +3.28 | 102.57 | 97.29 | +1.48 | bull | bull 46 | bull 77 |
| 09-07 | 106.49 | 107.05 | 102.85 | 103.73 | −2.59 | 102.81 | 97.88 | +1.55 | bull | bull 79 | bull 76 |
| 09-08 | 103.73 | 104.79 | 101.63 | 103.31 | −0.40 | 102.91 | 98.37 | +1.27 | bull | bull 64, neutral 13 | bull 74, neutral 8 |
| 09-09 | 103.31 | 105.15 | 100.07 | 101.50 | −1.75 | 102.63 | 98.65 | +0.05 | **neutral** | bull 62, neutral 3 | bull 99, neutral 19 |
| 09-10 | 101.50 | 102.15 | 98.30 | 98.61 | −2.85 | 101.82 | 98.65 | −0.97 | neutral | neutral 40 | neutral 82 |
| 09-11 | 98.61 | 105.77 | 97.76 | 102.41 | +3.85 | 101.94 | 98.99 | −0.95 | neutral | neutral 52 | neutral 84 |
| 09-12 | 102.41 | 102.54 | 101.15 | 101.71 | −0.68 | 101.89 | 99.24 | −0.72 | neutral | neutral 84 | neutral 109 |
| 09-13 | 101.71 | 102.32 | 99.11 | 99.21 | −2.46 | 101.36 | 99.24 | −0.46 | neutral | neutral 77 | bull 3, neutral 119 |
| 09-14 | 99.21 | 103.83 | 98.90 | 103.58* | +4.40 | 101.80 | 99.63 | −0.14 | neutral | neutral 43 | neutral 88 |

\* forming candle at ~18:40 UTC. Intraday stored labels use the forming candle, so they can differ from the at-close recompute (e.g. 09-02).

- **Entry-advisor consultations since 2026-08-10, by `trend_1d`: BULL 880 · NEUTRAL 468 · BEAR 0** (1 n/a).
- The 09-11 reading was BULL 880 / NEUTRAL 218 / BEAR 0. Recounted today up to 09-11 05:06 it is 880 / 221 / 0. **Every one of the 247 entry consultations since then read NEUTRAL.**
- The last stored BEAR is 2026-08-07 05:55 in `trades` and 2026-08-07 19:05 in `skip_attribution`. The last BEAR daily close on the Bybit recompute is **2026-08-06**.

### 2d. 🔴 Has the daily turned BEAR? No.

**It is NEUTRAL, and it is not close to BEAR by the bot's own rule.**
- EMA9 **101.80** is still above EMA21 **99.63**: the stack is bull.
- BEAR needs close < EMA9 < EMA21 **and** slope < −0.05 %. The EMA stack alone is about 2.2 % from crossing.
- What turned is the EMA9 slope (negative since 09-10) and the close dipping below EMA9 on 09-10, 09-12 and 09-13.

**So the picture has not inverted.** It went from "the daily is with the longs" to "the daily is with nobody".
- Longs are refused now for the reason shorts were refused before: the 4h/1h/15m point the other way on most consultations.
- Shorts are no longer refused on the daily. When the 4h dips BEAR, the advisor lets one through.
- The three it let through (09-01, 09-11, 09-14) were entered at 99.24, 99.30 and 99.56, in the lower part of the 97.3–107.3 range those two weeks traded. All three were stopped at 101.2–101.9.

---

## 3. THE TAPE CONTRADICTION

### 3a. Is the tape read by any gate? No. It is narration only.

Every tape producer and reader in the non-backup code:

| where | code | role |
|---|---|---|
| `main.py:4187-4204` | `_fetch_tape_aggression`: last 100 trades → `ratio > 0.58 → 'bullish'`, `< 0.42 → 'bearish'` | fetched **before** the gates (:4445) … |
| `main.py:5417-5419` | `update_trade(… tape_buy_ratio=_tape_ratio, tape_aggression=_tape_aggression …)` | … and written **only on the executed row**. No gate reads either variable |
| `main.py:5424-5431` | `# 4C parity: post-trade microstructure capture …` / `SYNCHRONOUS at entry fill` / `honors MICROSTRUCTURE_ENABLED; never raises, never gates.` → `microstructure.capture_and_persist_sync(...)` → `format_telegram_block` | **the card's "Tape P.: Buy 0.67" is captured AFTER the order filled**. `microstructure.py:164-167`: `buy_share >= 0.60 → 'buy'`, `<= 0.40 → 'sell'` |
| `signal_weights.py:262-264` | `claude_advisor.consult_for_learning(row_dict, orderbook_summary=…, tape_summary=compact_tape)` | post-**close** attribution consult. Writes `learning_*` columns that **no .py reads** |

- Entry prompts: **0 of 4,978** stored `ai_user_prompt` mention tape, buy_share or aggression.
- **Plainly: the tape has no consumer on the entry path.** It is the same class as the order book before the book gate was built.
- On vpos 45, both readings said buying: the pre-gate tape was `bullish 0.6613` (stored only), and the post-fill capture was `buy 0.6681` (the card).

### 3b. How often does the bot enter against the tape, and what happened

**Card tape** (post-fill 60 s window):

| book | side | AGAINST | WITH | NEUTRAL | n/a |
|---|---|---|---|---|---|
| live | LONG | n=4 · ΣR +8.254 · 3/4 (vpos 33, 38, 40, 43) | n=4 · +2.845 · 3/4 | 0 | 1 |
| live | SHORT | **n=5 · ΣR −3.883 · 0/5** (vpos 32, 34, 35, 37, 45) | n=3 · −2.949 · 0/3 | 0 | 0 |
| live | ALL | n=9 · ΣR +4.371 · 3/9 · mean +0.486 | n=7 · −0.105 · 3/7 | 0 | 1 |
| paper | LONG | n=1 · −0.739 | n=5 · −1.458 · 1/5 | n=3 · −1.850 | 0 |
| paper | SHORT | n=8 · ΣR +1.422 · 5/8 | n=4 · −3.883 · 0/4 | n=1 · +1.133 | 0 |
| paper | ALL | n=9 · ΣR +0.683 · 5/9 | n=9 · −5.340 · 1/9 | n=4 · −0.717 | 0 |

**Pre-gate tape** (the one the bot *had* at decision time, never read by any gate):

| book | side | AGAINST | WITH | NEUTRAL | n/a |
|---|---|---|---|---|---|
| live | LONG | n=2 · +5.664 · 2/2 (vpos 38, 41) | n=5 · +3.711 · 3/5 | n=1 · +1.723 | 1 |
| live | SHORT | n=3 · −2.539 · 0/3 (vpos 32, 37, 45) | n=4 · −3.593 · 0/4 | n=1 · −0.701 | 0 |
| paper | LONG | n=2 · −2.231 · 0/2 | n=4 · −1.782 · 1/4 | n=3 · −0.033 | 0 |
| paper | SHORT | n=11 · −0.300 · 5/11 | n=2 · −1.028 · 1/2 | 0 | 0 |

**Ranked cells** (both legs n ≥ 8, α = 0.00192):
- card tape live ALL: 9 vs 8, **p = 0.68**;
- card tape paper ALL: 9 vs 13, **p = 0.21**;
- pre-gate paper ALL: 13 vs 9, **p = 0.78**.

**Nothing clears. In every rankable cell, entering against the tape did better, not worse.** On this book, tape pressure at entry does not separate outcomes. Every per-side cell is n < 8.

### 3c. 15m `None`: entries with no 15m tier

"15M: None" on the card is the **combo key's** 15m slot (`state_machine.py:504`), and it has no signal name. What the cascade actually reads is the matrix MOMENTUM category (90-min window). Three definitions:

| definition | live | paper |
|---|---|---|
| combo slot `15M:None` | **2**: vpos 31 LONG −1.155, **45 SHORT −1.133** (0/2) | 4: vpos 14, 17, 20, 28 · ΣR −2.306 · 1/4 |
| MOMENTUM had **no signal at all** | **1: vpos 45** | 1: vpos 17 (+0.004) |
| MOMENTUM **NEUTRAL for the cascade** (no signal or intra-zeroed) | **8** (29, 31, 32, 33, 36, 41, 44, 45) · ΣR −1.395 · 2/8 · mean −0.174 | 10 · ΣR +1.428 · 5/10 · mean +0.143 |
| MOMENTUM **agreeing** | 9 · ΣR +7.016 · 5/9 · mean +0.780 | 12 · ΣR −6.803 · 2/12 · mean −0.567 |

- Ranked: NEUTRAL vs agreeing, live **p = 0.22**, paper **p = 0.089**. **The sign flips between books** (live: NEUTRAL worse; paper: NEUTRAL better). It does not survive.

**The tolerate-NEUTRAL route overall** (any of 1H/15m/5m NEUTRAL, none opposing):

| route | live |
|---|---|
| tolerate-NEUTRAL | **15 of 17** entries (LONG 8, ΣR +10.730, 6/8; SHORT 7, ΣR −5.606, 0/7) |
| aligned | 2 (vpos 43 LONG +1.723, vpos 37 SHORT −1.226) |

- Paper: tolerated 17 (ΣR +0.060, 8/17), aligned 5 (ΣR −5.435, 0/5).
- **SOL cannot measure its admission paths against each other.** "Aligned" is n = 2 live and n = 5 paper.
- On what exists, the tolerated route is not the worse one on paper, and on live it holds every winner.
- Titan's finding does not transfer, and it is not contradicted either. It is unmeasurable here.

On vpos 45 the missing 15m was tolerated by design, not by a DRYRUN. The require-15m clause (`signal_matrix.py:434-439`) only applies when the **1H** tier is NEUTRAL. Here the 1H was SHORT, so `HTF_NEUTRAL_REQUIRE_15M_DRYRUN = True` played no part.

---

## 4. THE SHORT BOOK AS IT STANDS

### 4a. Every LIVE SHORT

| vpos | opened → closed (UTC) | entry → exit | SL0 | R | $ | close | MFE % |
|---|---|---|---|---|---|---|---|
| 32 | 08-10 15:15 → 08-10 19:45 | 76.18 → 76.24 | 77.32 | −0.180 | −0.2663 | exit_signal | 0.76 |
| 34 | 08-13 16:40 → 08-13 17:12 | 75.21 → 75.76 | 76.30 | −0.643 | −0.9113 | sl | 0.17 |
| 35 | 08-14 14:20 → 08-14 15:30 | 75.16 → 75.57 | 75.96 | −0.701 | −0.7289 | sl | 0.19 |
| 36 | 08-15 07:50 → 08-16 02:45 | 75.20 → 75.62 | 75.94 | −0.757 | −0.7278 | exchange_market | 0.28 |
| 37 | 08-16 22:05 → 08-17 01:06 | 74.38 → 75.09 | 75.08 | −1.226 | −1.1156 | sl | 0.22 |
| 42 | 09-01 21:40 → 09-03 13:42 | 99.24 → 101.87 | 101.86 | −1.083 | −2.8381 | sl | 1.91 |
| 44 | 09-11 11:50 → 09-11 12:46 | 99.30 → 101.23 | 101.22 | −1.110 | −2.1305 | sl | 1.23 |
| **45** | 09-14 00:50 → 09-14 03:12 | 99.56 → 101.24 | 101.22 | −1.133 | −1.8808 | sl | 0.40 |
| **Σ** | **n = 8** | | | **ΣR −6.832** | **Σ$ −10.5994** | 0 wins | |

- The identical 101.22 stop on vpos 44 and 45 is a coincidence of arithmetic: 99.30 + 2.5×0.7681 and 99.56 + 2.5×0.6654.
- **No live short ever reached +1R** (the trail arm). The best was vpos 42 at about 0.73R.

### 4b. Every LIVE LONG

| vpos | opened → closed (UTC) | entry → exit | SL0 | R | $ | close | MFE % |
|---|---|---|---|---|---|---|---|
| 29 | 08-08 08:50 → 08-08 18:45 | 74.80 → 76.09 | 73.89 | +1.355 | +1.6025 | exchange_UNKNOWN | 2.22 |
| 30 | 08-08 21:10 → 08-09 22:37 | 76.29 → 77.08 | 75.41 | +0.762 | +0.8720 | trail | 1.93 |
| 31 | 08-10 08:10 → 08-10 15:21 | 76.96 → 75.90 | 75.91 | −1.155 | −1.4554 | sl | 0.18 |
| 33 | 08-11 22:00 → 08-12 13:00 | 76.50 → 76.61 | 75.43 | −0.049 | −0.0677 | exit_signal | 0.85 |
| 38 | 08-18 22:20 → 08-19 15:17 | 77.06 → 81.22 | 76.07 | +4.031 | +4.7888 | trail | 6.41 |
| 39 | 08-20 23:30 → 08-21 09:03 | 87.82 → 91.45 | 85.68 | +1.604 | +3.7762 | trail | 6.19 |
| 40 | 08-21 21:15 → 08-22 04:45 | 92.23 → 100.18 | 89.19 | +2.549 | +7.7482 | trail | 11.29 |
| 41 | 08-27 03:50 → 08-27 18:21 | 101.04 → 106.69 | 97.72 | +1.633 | +4.8808 | trail | 8.43 |
| 43 | 09-05 13:05 → 09-06 03:58 | 103.24 → 105.87 | 101.84 | +1.723 | +2.1706 | trail | 3.61 |
| **Σ** | **n = 9** | | | **ΣR +12.453** | **Σ$ +24.3161** (venue +23.9987) | 7 wins | |

**Side by side, live:**

| | n | wins | ΣR | Σ$ (DB) |
|---|---|---|---|---|
| SHORT | 8 | **0** | **−6.832** | −10.5994 |
| LONG | 9 | 7 | **+12.453** | +24.3161 |

- **Update of 2026-09-11:** SHORT 0 of 7 (−5.699R) → **0 of 8 (−6.832R)**. LONG is unchanged at 7 of 9 (+12.453R); no long has been taken since 09-05.
- The independent sample, **paper**: SHORT 13, 6 wins, ΣR −1.328, −$415.83; LONG 9, 2 wins, ΣR −4.046, −$712.63.

### 4c. The count

**The live short side is 0 wins in 8 attempts.** That is a count, not a test, and it is the fact the operator is reacting to.
- For scale only, outside the family: if live shorts won at the paper short rate (6/13 = 46 %), eight straight losses would happen about 0.7 % of the time.
- The ranked contrast, with its controls, is in §5.

---

## 5. VERDICT, WITH n AND THE FOUR CONTROLS

**Family 26, α = 0.00192. Rank only when both legs n ≥ 8. Survive only if p < α, both halves agree, TREND/FLAT agree, and paper/live agree.**

| # | contrast (A vs B) | live: A n · B n · p | paper: A n · B n · p | halves (live) | TREND/FLAT (live) | paper = live sign? | **verdict** |
|---|---|---|---|---|---|---|---|
| 1 | entry with **erased opposition** vs none | 2 · 15 · — | 5 · 17 · — | — | — | — | **NOT RANKED** (every cell n < 8, all 6 cells) |
| 2 | entry **against the card's tape** vs not | 9 · 8 · **0.68** | 9 · 13 · **0.21** | − / + (**unstable**) | + / + | + / + (against did *better*) | **dies** (p) |
| 3 | entry **against the pre-gate tape** vs not | 5 · 12 · — | 13 · 9 · **0.78** | — | — | — | **dies** (p). Live not ranked |
| 4 | **15m not agreeing** (cascade NEUTRAL) vs agreeing | 8 · 9 · **0.22** | 10 · 12 · **0.089** | + / − (**unstable**) | − / − | **flips** (live −, paper +) | **dies** (p, halves, book) |
| 5 | **SHORT vs LONG**, live | 8 · 9 · **0.0011 < α** | — | − / − ✅ | − / − ✅ | — | see 6 |
| 6 | **SHORT vs LONG**, paper | — | 13 · 9 · **0.42** | (paper: + / +) | (paper: + / n/a) | **flips**: paper shorts did better | **#5 fails the independent sample → does not survive** |

Per-side cells of #1–#4 are all n < 8 and not ranked. The full cell list is in Appendix B.

**What is mechanically wrong: nothing that the data can attribute an outcome to.**
1. **Sides are not confused**: 39/39 in the DB, 17/17 at the venue.
2. **The minority rule changes no decision.** It erases opposing LIQUIDITY from the card's net and from `long_score`/`short_score`. The gate reads only the proposed side, so removing the rule would move 0 entries.
3. **The opposing LIQUIDITY and the tape both have no consumer on the entry path.**
   - Opposing LIQUIDITY is read by no gate, the gate never nets it even when the rule keeps it, and the advisor is never shown it.
   - The tape is read by no gate and appears in no prompt, and the card's figure is post-fill.
   - That is a fact about the design, not a defect this book can price: neither separates outcomes (#1 unrankable, #2–#3 die).

**If nothing is wrong, say so: the shorts simply lose.**
- Live they lose 0 for 8, and the gap to longs clears α and holds across halves and regimes.
- On paper, where the daily read BEAR on about half the short entries, shorts did *better* than longs.
- The live era was a 41 % SOL rally with the daily never BEAR.
  - Every live short was entered with the 1h BEAR, and 7 of 8 with the 4h BEAR.
  - 6 of 8 were stopped at the 2.5×ATR(1h) stop, and none reached +1R.
- Nothing is proposed, and nothing is applied.

---

## FOUND ON THE WAY (not asked; stated, not proposed)

**The DB live book and the venue disagree by $1.16.** The card's "+$15.60 → +$13.72" is the DB book. Bybit `closed-pnl` for the same era sums to **+$12.5563**.

| component | $ |
|---|---|
| SHORT side | agrees to the cent (−10.5994 both) |
| two LONG emergency closes on 2026-08-08 06:50 and 08:35 (rows 16748/16749 and 16765/16766, `sl_failed_position_closed` + `failed`), with no `virtual_positions` row | **−0.8431** at the venue, not in the book |
| vpos 40: DB close 100.18 vs venue avgExit 99.92 | **+0.2597** DB over venue |
| vpos 29, 30, 38: small leg/fee differences | +0.0246, +0.0090, +0.0239 |

Venue `closedPnl` excludes funding, so the residual is approximate at the cent level.

---

## READ-ONLY CONFIRMATION

| item | state |
|---|---|
| **`openitems_guard`** | run first, **EXIT 0** (it imports Titan's config and reads git by its own design; that was the prescribed first step) |
| **SOL DB** | opened **only** as `file:…/trades.db?mode=ro` with `PRAGMA query_only=1` (verified `query_only = 1`). **No write statement issued.** The DB's mtime moved 18:41:05 → 18:55:11 from the live bot's own writes |
| **SOL config** | **not imported**: read as text and parsed with `ast.literal_eval`. `signal_matrix.py` likewise parsed with `ast`, never imported |
| **file hashes** | md5 of every SOL `*.py` (incl. `config.py`), Titan `config.py` and the book-gate counter file, before (18:41:32) and after (18:55:19): **all 36 identical** |
| **orders / venue** | **no orders**. Venue calls: public `GET /v5/market/kline` (Bybit via Tor, OKX for a first attempt); signed **`GET /v5/position/closed-pnl`** only |
| **restarts** | **none**. `mercury-sol` NRestarts **0 → 0** (MainPID 1341949, active since 09-11 18:26:59) · `titan` NRestarts **0 → 0** (MainPID 1572470, since 09-12 14:58:32) · `mercury-sol-optimizer-listener` 0 → 0 |
| **`FLAT_ADX_GATE_DRYRUN`** | **True** (config.py:407), unchanged |
| **`BOOK_GATE_DRYRUN`** | **False** (config.py:475), unchanged |
| **book-gate review counter** | **untouched**. `sol_book_gate_review.json` identical before and after: `last_run 2026-09-14 18:30:02` (its own 30-min cron), LONG [135, 0], SHORT [112, 0], fired `review_point` (09-13 22:00:03) |
| **Titan** | **untouched, nothing written**. Its only reads were: the guard (imports Titan's config and reads git, by design), an md5 of `titan-bot/config.py`, a `stat` of its DB mtime, and `systemctl show titan`. **Titan's DB was never opened**; its mtime moved on Titan's own writes |
| **writes** | scratch files in this session's scratchpad; this report in `kola-reports` |

---

## APPENDIX A: every book entry

Raw score is taken from the breakdown on the traded side. 🚫 = zeroed by the minority rule; "intra L/S" = category zeroed by intra-conflict.

| vpos | book | side | opened (UTC) | entry→exit | R | $ | close | TREND | MOM | LIQ | EXEC | raw (traded side) | opposing cat | rule | winner (tsm) | cascade | tape card / pre-gate | 1d/4h/1h | regime | MFE% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 | paper | LONG | 2026-06-14 23:50 | 70.98→74.57 | +2.089 | +494.2006 | exit_signal | L2.5 | 0 (intra L1.75/S2.5) | S2.5 | 0 (intra L2.5/S1.75) | 2.50 | LIQUIDITY | kept (tie) | NEUTRAL 2.5 | tol-NEUTRAL | buy 0.7799 / neutral 0.4675 | neutral/bull/bull | TREND | n/a |
| 8 | paper | LONG | 2026-06-20 07:00 | 72.05→70.85 | -0.739 | -177.3411 | exit_signal | L2.25 | 0 (intra L1.75/S2.5) | L2.5 | — | 4.75 | — | — | LONG 4.75 | tol-NEUTRAL | sell 0.0496 / bullish 0.6799 | None/None/bull | TREND | n/a |
| 9 | paper | LONG | 2026-06-21 02:50 | 73.3→72.95 | -0.264 | -58.7117 | exit_signal | L2.25 | L1.75 | 0 (intra L1.75/S2.5) | 0 (intra L1.25/S1.75) | 4.00 | — | — | LONG 4.0 | tol-NEUTRAL | buy 0.6286 / bullish 0.7823 | neutral/bull/bull | TREND | n/a |
| 10 | paper | SHORT | 2026-06-22 00:00 | 72.57→74.27 | -1.066 | -245.2109 | sl | S2.5 | S1.75 | 0 (intra L2.5/S1.75) | S1.75 | 6.00 | — | — | SHORT 6.0 | aligned | sell 0.3119 / bullish 0.7048 | neutral/neutral/bear | TREND | n/a |
| 11 | paper | SHORT | 2026-06-23 00:30 | 71.43→69.2 | +1.133 | +301.1562 | exit_signal | S2.5 | 0 (intra L2.5/S1.75) | L1.25 | 0 (intra L2.0/S2.5) | 2.50 | LIQUIDITY | kept (tie) | SHORT 2.5 | tol-NEUTRAL | neutral 0.4087 / bullish 0.6816 | neutral/neutral/bear | TREND | n/a |
| 12 | paper | LONG | 2026-06-24 02:25 | 69.55→68.0 | -1.049 | -233.6063 | sl | L2.5 | 0 (intra L1.75/S2.5) | L1.25 | 0 (intra L2.5/S2.5) | 3.75 | — | — | LONG 3.75 | tol-NEUTRAL | neutral 0.5345 / neutral 0.5378 | bear/bear/neutral | TREND | n/a |
| 13 | paper | SHORT | 2026-06-24 13:25 | 68.63→66.31 | +1.337 | +327.2106 | trail | — | S1.75 | L2.5 | 0 (intra L2.5/S2.5) | 1.75 | LIQUIDITY | kept (tie) | LONG 2.5 | tol-NEUTRAL | buy 0.7948 / bullish 0.8019 | bear/bear/bear | FLAT | n/a |
| 14 | paper | SHORT | 2026-06-25 14:00 | 64.85→67.41 | -1.032 | -405.9690 | sl | S2.5 | 0 (intra L2.5/S1.75) | L1.25 🚫 | S1.25 | 3.75 | LIQUIDITY | zeroed | SHORT 3.75 | tol-NEUTRAL | sell 0.1905 / bearish 0.2348 | bear/None/bear | TREND | n/a |
| 15 | paper | SHORT | 2026-07-08 05:05 | 78.56→78.2 | +0.140 | +34.8251 | trail | S2.5 | 0 (intra L1.75/S1.75) | — | S1.75 | 4.25 | — | — | SHORT 4.25 | tol-NEUTRAL | buy 0.6821 / bullish 0.8334 | neutral/bear/bear | TREND | 2.93 |
| 16 | paper | LONG | 2026-07-10 08:30 | 79.37→77.91 | -1.146 | -194.7049 | sl | L2.25 | L1.75 | 0 (intra L1.75/S1.25) | L1.75 | 5.75 | — | — | LONG 5.75 | aligned | buy 0.8247 / bearish 0.1637 | neutral/neutral/bull | TREND | 0.28 |
| 17 | paper | SHORT | 2026-07-13 03:10 | 75.91→75.82 | +0.004 | +0.8624 | sl | S2.5 | — | 0 (intra L1.75/S1.75) | S1.25 | 3.75 | — | — | SHORT 3.75 | tol-NEUTRAL | buy 0.9806 / bearish 0.3336 | neutral/bear/bear | TREND | 2.33 |
| 18 | paper | LONG | 2026-07-14 15:45 | 77.47→75.74 | -1.074 | -234.0402 | sl | L2.5 | L1.75 | S2.5 🚫 | L2.0 | 6.25 | LIQUIDITY | zeroed | LONG 6.25 | aligned | buy 0.6712 / neutral 0.4201 | neutral/neutral/bull | TREND | 1.95 |
| 19 | paper | SHORT | 2026-07-16 00:25 | 77.04→76.27 | +0.463 | +89.0012 | exit_signal | S2.5 | S1.75 | L2.5 🚫 | 0 (intra L1.75/S2.25) | 4.25 | LIQUIDITY | zeroed | SHORT 4.25 | tol-NEUTRAL | buy 0.744 / bullish 0.686 | neutral/neutral/bear | TREND | 1.87 |
| 20 | paper | SHORT | 2026-07-17 13:40 | 73.58→75.05 | -1.124 | -210.8823 | sl | 0 (intra L2.5/S2.5) | S1.75 | 0 (intra L1.25/S1.75) | S1.25 | 3.00 | — | — | SHORT 3.0 | tol-NEUTRAL | sell 0.0572 / bullish 0.9764 | neutral/bear/bear | FLAT | 0.3 |
| 21 | paper | LONG | 2026-07-19 06:50 | 76.05→76.39 | +0.285 | +33.6592 | trail | L2.25 | 0 (intra L1.75/S1.75) | S2.5 🚫 | L2.5 | 4.75 | LIQUIDITY | zeroed | LONG 4.75 | tol-NEUTRAL | neutral 0.4938 / bullish 0.9454 | bear/neutral/bull | TREND | 1.71 |
| 22 | paper | LONG | 2026-07-21 03:10 | 78.41→76.9 | -1.064 | -203.4161 | sl | L2.25 | L1.75 | 0 (intra L1.75/S1.25) | L1.75 | 5.75 | — | — | LONG 5.75 | aligned | buy 0.8954 / bullish 0.7668 | bull/bull/bull | TREND | 0.55 |
| 23 | paper | SHORT | 2026-07-28 11:05 | 72.98→73.58 | -0.577 | -93.2433 | exit_signal | — | S1.75 | S1.75 | 0 (intra L2.5/S2.5) | 3.50 | — | — | SHORT 3.5 | tol-NEUTRAL | buy 0.7265 / bullish 0.6079 | bear/bear/bear | FLAT | 0.85 |
| 24 | paper | SHORT | 2026-07-29 20:05 | 72.67→74.29 | -1.050 | -234.0339 | sl | S2.5 | S2.5 | L2.5 🚫 | 0 (intra L1.75/S2.0) | 5.00 | LIQUIDITY | zeroed | SHORT 5.0 | tol-NEUTRAL | buy 0.9657 / bullish 0.849 | bear/bear/bear | TREND | 0.56 |
| 25 | paper | SHORT | 2026-08-01 17:20 | 72.47→71.36 | +1.257 | +126.5230 | trail | — | 0 (intra L1.75/S1.75) | S1.75 | — | 1.75 | — | — | SHORT 1.75 | tol-NEUTRAL | buy 0.7218 / bullish 0.9778 | bear/bear/bear | FLAT | 2.53 |
| 26 | paper | LONG | 2026-08-02 05:00 | 73.53→72.59 | -1.085 | -138.6677 | sl | L2.5 | L1.75 | — | L1.25 | 5.50 | — | — | LONG 5.5 | aligned | neutral 0.4806 / bearish 0.1069 | bear/neutral/bull | TREND | 0.92 |
| 27 | paper | SHORT | 2026-08-03 06:45 | 72.53→73.07 | -0.660 | -85.4470 | sl | S2.5 | 0 (intra L1.75/S1.75) | 0 (intra L2.5/S1.75) | — | 2.50 | — | — | SHORT 2.5 | tol-NEUTRAL | sell 0.0993 / bullish 0.5818 | bear/bear/bear | TREND | 0.76 |
| 28 | paper | SHORT | 2026-08-06 19:00 | 72.77→72.84 | -0.153 | -20.6217 | exit_signal | S2.25 | S1.75 | 0 (intra L1.25/S1.75) | — | 4.00 | — | — | SHORT 4.0 | tol-NEUTRAL | buy 0.7523 / bullish 0.971 | bear/bear/bear | TREND | 0.66 |
| 29 | **live** | LONG | 2026-08-08 08:50 | 74.8→76.09 | +1.355 | +1.6025 | exchange_UNKNOWN | L2.5 | 0 (intra L1.75/S1.75) | — | L2.0 | 4.50 | — | — | n/a (row `failed`) | tol-NEUTRAL | n/a / n/a | neutral/bull/bull | TREND | 2.22 |
| 30 | **live** | LONG | 2026-08-08 21:10 | 76.29→77.08 | +0.762 | +0.8720 | trail | — | L1.75 | — | L2.5 | 4.25 | — | — | LONG 4.25 | tol-NEUTRAL | buy 0.9472 / bullish 0.9401 | neutral/bull/bull | FLAT | 1.93 |
| 31 | **live** | LONG | 2026-08-10 08:10 | 76.96→75.9 | -1.155 | -1.4554 | sl | L2.5 | 0 (intra L1.75/S1.75) | — | L2.0 | 4.50 | — | — | LONG 4.5 | tol-NEUTRAL | buy 0.9178 / bullish 0.9996 | bull/bull/bull | TREND | 0.18 |
| 32 | **live** | SHORT | 2026-08-10 15:15 | 76.18→76.24 | -0.180 | -0.2663 | exit_signal | S2.5 | 0 (intra L1.75/S1.75) | L2.5 🚫 | S1.75 | 4.25 | LIQUIDITY | zeroed | SHORT 4.25 | tol-NEUTRAL | buy 0.7038 / bullish 0.9931 | bull/neutral/bear | TREND | 0.76 |
| 33 | **live** | LONG | 2026-08-11 22:00 | 76.5→76.61 | -0.049 | -0.0677 | exit_signal | L2.5 | 0 (intra L1.75/S2.5) | 0 (intra L1.75/S2.5) | 0 (intra L1.75/S1.75) | 2.50 | — | — | LONG 2.5 | tol-NEUTRAL | sell 0.0977 / bullish 0.6303 | bull/neutral/bull | TREND | 0.85 |
| 34 | **live** | SHORT | 2026-08-13 16:40 | 75.21→75.76 | -0.643 | -0.9113 | sl | — | S1.75 | — | 0 (intra L2.5/S2.5) | 1.75 | — | — | SHORT 1.75 | tol-NEUTRAL | buy 0.9046 / bearish 0.0915 | bull/bear/bear | FLAT | 0.17 |
| 35 | **live** | SHORT | 2026-08-14 14:20 | 75.16→75.57 | -0.701 | -0.7289 | sl | — | S1.75 | L2.5 | 0 (intra L2.0/S2.5) | 1.75 | LIQUIDITY | kept (tie) | LONG 2.5 | tol-NEUTRAL | buy 0.75 / neutral 0.4732 | neutral/bear/bear | FLAT | 0.19 |
| 36 | **live** | SHORT | 2026-08-15 07:50 | 75.2→75.62 | -0.757 | -0.7278 | exchange_market | — | 0 (intra L1.75/S1.75) | L2.5 | S2.5 | 2.50 | LIQUIDITY | kept (tie) | NEUTRAL 2.5 | tol-NEUTRAL | sell 0.1504 / bearish 0.3444 | neutral/bear/bear | FLAT | 0.28 |
| 37 | **live** | SHORT | 2026-08-16 22:05 | 74.38→75.09 | -1.226 | -1.1156 | sl | S2.5 | S1.75 | 0 (intra L2.5/S1.75) | S1.75 | 6.00 | — | — | SHORT 6.0 | aligned | buy 0.8 / bullish 0.9591 | neutral/bear/bear | TREND | 0.22 |
| 38 | **live** | LONG | 2026-08-18 22:20 | 77.06→81.22 | +4.031 | +4.7888 | trail | L2.25 | L1.75 | 0 (intra L2.5/S2.5) | — | 4.00 | — | — | LONG 4.0 | tol-NEUTRAL | sell 0.2841 / bearish 0.3003 | bull/bull/bull | TREND | 6.41 |
| 39 | **live** | LONG | 2026-08-20 23:30 | 87.82→91.45 | +1.604 | +3.7762 | trail | — | L1.75 | L1.75 | 0 (intra L2.5/S2.5) | 3.50 | — | — | LONG 3.5 | tol-NEUTRAL | buy 0.6725 / bullish 0.7751 | bull/bull/bull | FLAT | 6.19 |
| 40 | **live** | LONG | 2026-08-21 21:15 | 92.23→100.18 | +2.549 | +7.7482 | trail | — | L1.75 | — | 0 (intra L1.25/S1.75) | 1.75 | — | — | LONG 1.75 | tol-NEUTRAL | sell 0.2063 / bullish 0.7527 | bull/bull/bull | FLAT | 11.29 |
| 41 | **live** | LONG | 2026-08-27 03:50 | 101.04→106.69 | +1.633 | +4.8808 | trail | L2.5 | 0 (intra L1.75/S1.75) | — | L1.75 | 4.25 | — | — | LONG 4.25 | tol-NEUTRAL | buy 0.7888 / bearish 0.26 | bull/bull/bull | TREND | 8.43 |
| 42 | **live** | SHORT | 2026-09-01 21:40 | 99.24→101.87 | -1.083 | -2.8381 | sl | S2.25 | S1.75 | S1.75 | — | 5.75 | — | — | SHORT 5.75 | tol-NEUTRAL | sell 0.1781 / bearish 0.0573 | neutral/bear/bear | TREND | 1.91 |
| 43 | **live** | LONG | 2026-09-05 13:05 | 103.24→105.87 | +1.723 | +2.1706 | trail | L2.5 | L2.5 | 0 (intra L2.5/S2.5) | L1.75 | 6.75 | — | — | LONG 6.75 | aligned | sell 0.3835 / neutral 0.4672 | bull/bull/bull | TREND | 3.61 |
| 44 | **live** | SHORT | 2026-09-11 11:50 | 99.3→101.23 | -1.110 | -2.1305 | sl | 0 (intra L2.5/S2.5) | 0 (intra L1.75/S1.75) | 0 (intra L1.75/S1.25) | S2.0 | 2.00 | — | — | SHORT 2.0 | tol-NEUTRAL | sell 0.1175 / bearish 0.3333 | neutral/bear/bear | FLAT | 1.23 |
| 45 | **live** | SHORT | 2026-09-14 00:50 | 99.56→101.24 | -1.133 | -1.8808 | sl | S2.5 | — | L2.5 🚫 | S1.75 | 4.25 | LIQUIDITY | zeroed | SHORT 4.25 | tol-NEUTRAL | buy 0.6681 / bullish 0.6613 | neutral/bear/bear | TREND | 0.4 |

MFE n/a for vpos 7–14: excursion sampling began later.

## APPENDIX B: the 26-cell family, raw output

```
FAMILY = 4 shapes x 3 cells (ALL/LONG/SHORT) x 2 books + 2 side contrasts (SHORT vs LONG, per book) = 26; alpha = 0.05/26 = 0.00192; rank only when BOTH legs n>=8
erased_opposition                  ALL   live  A n=2 B n=15 NOT RANKED
erased_opposition                  ALL   paper A n=5 B n=17 NOT RANKED
erased_opposition                  LONG  live  A n=0 B n=9 NOT RANKED
erased_opposition                  LONG  paper A n=2 B n=7 NOT RANKED
erased_opposition                  SHORT live  A n=2 B n=6 NOT RANKED
erased_opposition                  SHORT paper A n=3 B n=10 NOT RANKED
against_tape_card(post-fill)       ALL   live  A n=9 ΣR=+4.371 mean=+0.486 | B n=8 ΣR=+1.250 mean=+0.156 | diff sign + | p=0.6793 ≥ α | halves ('-', '+') | regime TREND/FLAT ('+', '+')
against_tape_card(post-fill)       ALL   paper A n=9 ΣR=+0.683 mean=+0.076 | B n=13 ΣR=-6.057 mean=-0.466 | diff sign + | p=0.2087 ≥ α | halves ('+', '+') | regime TREND/FLAT ('+', '+')
against_tape_card(post-fill)       LONG  live  A n=4 B n=5 NOT RANKED
against_tape_card(post-fill)       LONG  paper A n=1 B n=8 NOT RANKED
against_tape_card(post-fill)       SHORT live  A n=5 B n=3 NOT RANKED
against_tape_card(post-fill)       SHORT paper A n=8 B n=5 NOT RANKED
against_tape_pregate               ALL   live  A n=5 B n=12 NOT RANKED
against_tape_pregate               ALL   paper A n=13 ΣR=-2.531 mean=-0.195 | B n=9 ΣR=-2.843 mean=-0.316 | diff sign + | p=0.7824 ≥ α | halves ('+', '+') | regime TREND/FLAT ('-', None)
against_tape_pregate               LONG  live  A n=2 B n=7 NOT RANKED
against_tape_pregate               LONG  paper A n=2 B n=7 NOT RANKED
against_tape_pregate               SHORT live  A n=3 B n=5 NOT RANKED
against_tape_pregate               SHORT paper A n=11 B n=2 NOT RANKED
15m_not_agreeing(cascade NEUTRAL)  ALL   live  A n=8 ΣR=-1.395 mean=-0.174 | B n=9 ΣR=+7.016 mean=+0.780 | diff sign - | p=0.2190 ≥ α | halves ('+', '-') | regime TREND/FLAT ('-', '-')
15m_not_agreeing(cascade NEUTRAL)  ALL   paper A n=10 ΣR=+1.428 mean=+0.143 | B n=12 ΣR=-6.803 mean=-0.567 | diff sign + | p=0.0888 ≥ α | halves ('+', '+') | regime TREND/FLAT ('+', '+')
15m_not_agreeing(cascade NEUTRAL)  LONG  live  A n=4 B n=5 NOT RANKED
15m_not_agreeing(cascade NEUTRAL)  LONG  paper A n=4 B n=5 NOT RANKED
15m_not_agreeing(cascade NEUTRAL)  SHORT live  A n=4 B n=4 NOT RANKED
15m_not_agreeing(cascade NEUTRAL)  SHORT paper A n=6 B n=7 NOT RANKED
SIDE SHORT-vs-LONG live  SHORT n=8 ΣR=-6.832 mean=-0.854 | LONG n=9 ΣR=+12.453 mean=+1.384 | sign - | p=0.0011 < α | halves ('-', '-') | regime TREND/FLAT ('-', '-')
SIDE SHORT-vs-LONG paper SHORT n=13 ΣR=-1.328 mean=-0.102 | LONG n=9 ΣR=-4.046 mean=-0.450 | sign + | p=0.4235 ≥ α | halves ('+', '+') | regime TREND/FLAT ('+', None)
```

Permutation test: 50,000 shuffles on R, two-sided, seed 11. Halves are chronological within each book. Regime is the matrix `market_regime` stored on the entry row. By `trend_1d` at entry, live: SHORT bull 2 (ΣR −0.823), neutral 6 (−6.009), bear 0; LONG bull 7 (+10.336), neutral 2 (+2.117), bear 0. Paper: SHORT neutral 6 (−0.450, 4 wins), bear 7 (−0.878, 2 wins); LONG bull 1, neutral 4, bear 3, n/a 1.

## APPENDIX C: Bybit closed-pnl (signed GET), live era

```
2026-08-08 06:50 closeOrderSide=Sell => position LONG  qty=2.6 avgEntry=74.795 avgExit=74.78 closedPnl=-0.427895
2026-08-08 08:35 closeOrderSide=Sell => position LONG  qty=2.6 avgEntry=74.85 avgExit=74.84 closedPnl=-0.415194
2026-08-08 15:40 closeOrderSide=Sell => position LONG  qty=0.4 avgEntry=74.8 avgExit=76.35 closedPnl=0.55954
2026-08-08 18:45 closeOrderSide=Sell => position LONG  qty=0.9 avgEntry=74.8 avgExit=76.09 closedPnl=1.0183266
2026-08-09 15:40 closeOrderSide=Sell => position LONG  qty=0.4 avgEntry=76.29 avgExit=77.25 closedPnl=0.31664356
2026-08-09 22:37 closeOrderSide=Sell => position LONG  qty=0.9 avgEntry=76.29 avgExit=77.07 closedPnl=0.54639628
2026-08-10 15:21 closeOrderSide=Sell => position LONG  qty=1.2 avgEntry=76.96 avgExit=75.9 closedPnl=-1.455432
2026-08-10 19:45 closeOrderSide=Buy  => position SHORT qty=1.3 avgEntry=76.18 avgExit=76.24 closedPnl=-0.26627497
2026-08-12 13:00 closeOrderSide=Sell => position LONG  qty=1.3 avgEntry=76.5 avgExit=76.61 closedPnl=-0.06770851
2026-08-13 17:12 closeOrderSide=Buy  => position SHORT qty=1.3 avgEntry=75.21 avgExit=75.76 closedPnl=-0.911261
2026-08-14 15:30 closeOrderSide=Buy  => position SHORT qty=1.3 avgEntry=75.16 avgExit=75.57 closedPnl=-0.728949
2026-08-16 02:45 closeOrderSide=Buy  => position SHORT qty=1.3 avgEntry=75.2 avgExit=75.62 closedPnl=-0.7278388
2026-08-17 01:06 closeOrderSide=Buy  => position SHORT qty=1.3 avgEntry=74.38 avgExit=75.09 closedPnl=-1.11559686
2026-08-19 15:17 closeOrderSide=Sell => position LONG  qty=1.2 avgEntry=77.06 avgExit=81.2 closedPnl=4.76486353
2026-08-21 09:03 closeOrderSide=Sell => position LONG  qty=1.1 avgEntry=87.82 avgExit=91.45 closedPnl=3.77621805
2026-08-22 04:45 closeOrderSide=Sell => position LONG  qty=1 avgEntry=92.23 avgExit=99.92 closedPnl=7.488478
2026-08-27 18:21 closeOrderSide=Sell => position LONG  qty=0.9 avgEntry=101.04 avgExit=106.69 closedPnl=4.8808262
2026-09-03 13:42 closeOrderSide=Buy  => position SHORT qty=1 avgEntry=99.24 avgExit=101.87 closedPnl=-2.83812167
2026-09-06 03:58 closeOrderSide=Sell => position LONG  qty=0.9 avgEntry=103.24 avgExit=105.87 closedPnl=2.17057833
2026-09-11 12:46 closeOrderSide=Buy  => position SHORT qty=1 avgEntry=99.3 avgExit=101.23 closedPnl=-2.13053
2026-09-14 03:11 closeOrderSide=Buy  => position SHORT qty=1 avgEntry=99.56 avgExit=101.24 closedPnl=-1.8808
venue SHORT closes 8 Σ -10.5994 · venue LONG records 13 Σ +23.1556 (of which 2 unbooked 08-08 closes Σ -0.8431) · venue total +12.5563
```
