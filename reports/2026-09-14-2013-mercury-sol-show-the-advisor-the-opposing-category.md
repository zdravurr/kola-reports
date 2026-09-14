# mercury-sol-show-the-advisor-the-opposing-category

_2026-09-14 20:13 UTC_

---

# Mercury-SOL — show the advisor the opposing category

**2026-09-14 · §1 measured read-only · §2 ONE prompt block APPLIED FROM FLAT, LOADED · §3–§4 read-only / recorded** · `openitems_guard` **EXIT 0 before (19:53) and after (20:07)**

**Basis:** `reports/2026-09-14-1904-mercury-sol-why-shorts-not-longs-minority-rule-erased.md`, §1 and Appendix A.

> **CONTROLS, DECLARED IN THE HEADER**
> * **Family (Bonferroni): 10 cells, α = 0.05/10 = 0.005.**
>   - §1c: any opposing category vs none, ALL/LONG/SHORT × 2 books = 6.
>   - §3: SHORT with a BEAR daily vs not, and LONG with a BULL daily vs not, × 2 books = 4.
> * **Paper and live are never pooled.** Paper is the independent sample.
> * **No cell is ranked unless both legs have n ≥ 8.**
> * A cell **survives** only if all four hold: the permutation p is below α; the sign is the same in both chronological halves; the sign is the same in TREND and FLAT; and the sign is the same on paper and live.
> * Book: 39 closed `virtual_positions`, 17 live (vpos 29–45) and 22 paper (vpos 7–28). R = `net_pnl / initial_risk_usdt`.

---

## VERDICT

🔴 **§1c first, before any conclusion: the sign inverts between the books, and live n = 4 ranks nothing.**
- **Live:** entries with an opposing category n = 4, ΣR −2.770, 0/4. Entries without, n = 13, ΣR +8.391, 7/13.
- **Paper:** entries with an opposing category n = 8, ΣR **+2.151**, 5/8. Entries without, n = 14, ΣR −7.525, 3/14.
- On paper an opposed entry did **better**. That paper cell is the only rankable one, and it gives p = 0.058, which does not clear α.
- **Nothing in this report shows that an opposing category predicts a loss.** The block was shipped as a **fact** the advisor was missing, not as an edge.

**1. MEASURED: the advisor was never shown the opposition.**
- Over **4,811** stored entry consultations (2026-06-08 → 09-14), **838 (17.4 %)** had a non-NEUTRAL category opposing the proposed side.
- LONG proposals: 342 of 2,237 (15.3 %). SHORT proposals: 496 of 2,574 (19.3 %).
- **838 of 838 were LIQUIDITY, and 838 of 838 were not rendered.** The minority rule zeroed 594 of them; 244 were kept on the other side because of a tie.
- Since the matrix line appeared (09-11 19:40): **53 of 213** prompts were opposed, 0 rendered it, and 0 carried a "ZEROED as the minority" line.
- The advisor said execute on 33 of the 838. **12 became book positions: live 4, paper 8.** The other 21 were `observed_skipped` rows that placed no order.
- In all 12 positions, none of the opposing signals' names appear anywhere in the stored prompt.

**2. APPLIED: one block of facts under the matrix line.**
- It names all four scored categories, with points and each signal's age against its window.
- A category that **OPPOSES** is marked as such, along with whether it was zeroed as the minority or kept on the other side.
- It states that **the score gate never subtracts opposing points.**
- Only the prompt builder changed. The AST proof passes; the six system prompts are byte-identical by sha256; `signal_matrix.py`, `main.py`, `config.py`, every gate and the score are unchanged.
- Contracts: 3/3 green as root and 3/3 as botuser.
- Restarted **from flat** at 20:05:45, verified from the loaded bytecode.
- 🔴 **COHORT BOUNDARY: 2026-09-14 20:06:18 UTC** (`trades.id > 26793`).
- 🔴 **What it cannot do:** stop the model concluding wrongly from correct facts. On 2026-08-31 the zeroed-tier label was already on all nine live SOL cases, and the narration built on the tier anyway.
- ⏳ **Live proof pending:** no entry consultation had arrived by publication. A read-only waiter appends the first one to **this file, at this URL**.

**3. THE SHORT SIDE: the daily label does not explain it, and the live book cannot answer the question.**
- **Live:** 8 shorts, **0 with a BEAR daily** (2 BULL, 6 NEUTRAL).
- **Paper:** 13 shorts. With a BEAR daily **n = 7, ΣR −0.878, 2/7, mean −0.125**. With a NEUTRAL daily **n = 6, ΣR −0.450, 4/6, mean −0.075**.
- **Paper shorts with the daily in their favour did no better than paper shorts with a NEUTRAL daily.**
- At the **same** NEUTRAL label, live shorts went 0/6 (mean −1.002) and paper shorts 4/6 (mean −0.075). **The gap is between books, not between daily labels.**
- **Every cell is n < 8. Nothing is ranked.**
- **A rule of "no SHORT unless the daily is BEAR":**
  - Live: it refuses all 8 shorts (ΣR −6.832) and no winners. Live would then have taken **zero shorts, ever**.
  - 🔴 **Paper: it refuses 4 WINNERS** (vpos 11 +1.133R, 15 +0.140R, 17 +0.004R, 19 +0.463R) out of 6 refused shorts (ΣR −0.450).
- 🔴 **The live book has never seen a BEAR daily.** Any claim about shorts in a bear regime rests on 7 paper trades, and those 7 were not better.

**4. RECORDED, NOT FIXED: the book-vs-venue gap is in the canon.**
- New section `OPEN-ITEMS-SOL.md §LIVE-BOOK-VS-VENUE-GAP-2026-09-14`, with row ids.
- 🔴 **Every live-era P&L figure read from the DB is overstated by ≈ $1.16 against Bybit:** DB +$13.7167 vs venue +$12.5563.

---

## 1. MEASURE FIRST (READ-ONLY)

### 1a. Consultations whose opposing category was not rendered

**Population:** every `open_long` / `open_short` row with a stored `ai_user_prompt`, 4,811 in all. Every one also stores `matrix_breakdown_json`.

**Opposing:** the category's `net_direction` is LONG or SHORT and is not the proposed side.

**Rendered:** a category counts as rendered only if a tier the prompt shows maps to it.
- The shown tiers are the `1H:` / `15m:` / `5m trigger:` slot lines. Each slot's signal is classified by its dictionary category; an empty 1H slot counts as TREND and an empty 15m slot as MOMENTUM, exactly as `_render_matrix_tier_line` does.
- In the matrix-line era, the result was also checked against the categories the line actually names.

| side | consultations | **with an opposing category** | … **not rendered** | by category | zeroed by minority / kept (tie) | advisor verdict on those |
|---|---|---|---|---|---|---|
| LONG | 2,237 | **342 (15.3 %)** | **342 (100 % of opposed)** | LIQUIDITY 342 | 247 / 95 | skip 333 · execute 9 |
| SHORT | 2,574 | **496 (19.3 %)** | **496 (100 %)** | LIQUIDITY 496 | 347 / 149 | skip 472 · execute 24 |
| **ALL** | **4,811** | **838 (17.4 %)** | **838 (100 %)** | **LIQUIDITY 838** | 594 / 244 | skip 805 · execute 33 |

- **Rendered opposing categories (tied to a shown tier): 0.** The cascade removes every opposing TREND, MOMENTUM and EXECUTION before the advisor, and no shown tier maps to LIQUIDITY unless the 5m trigger is itself a LIQUIDITY signal, which is then the proposed side.
- By month (consultations, opposed and not rendered): June 843 / 175 · July 2,075 / 346 · August 1,170 / 193 · September 723 / 124.

**Matrix-line era** (prompts carrying the 2026-09-11 line; first at 19:40:06):

| side | prompts | opposed | opposing category absent from the matrix line | zeroed / kept | verdicts | prompts with "ZEROED as the minority" |
|---|---|---|---|---|---|---|
| LONG | 117 | 34 (29.1 %) | **34 (100 %)**, LIQUIDITY | 27 / 7 | skip 34 | 0 |
| SHORT | 96 | 19 (19.8 %) | **19 (100 %)**, LIQUIDITY | 18 / 1 | skip 18 · **execute 1 (vpos 45)** | 0 |
| ALL | 213 | 53 (24.9 %) | **53** | 45 / 8 | skip 52 · execute 1 | **0** |

The 33 advisor executes on opposed consultations split into 12 `executed` rows (the book entries below) and 21 `observed_skipped` rows, which placed no order (June–July paper era).

### 1b. Which of them became ENTRIES (zeroed ∪ kept), live and paper separately

For each entry: the opposing signals with weight and age from `trade_signal_matrix.active_signals_json`, and whether any opposing signal name, or `→ LIQUIDITY`, appears in the stored prompt.

**LIVE, n = 4:**

| vpos | side | opened (UTC) | opposing | rule | proposed raw | opposing signals (weight, age of window) | in prompt? | R |
|---|---|---|---|---|---|---|---|---|
| 32 | SHORT | 08-10 15:15 | LIQUIDITY LONG 2.50 | **zeroed** | 4.25 | Bullish Liquidity Grab w1.0 0.1/30 min (0 %); Bullish Imbalance Mitigated w0.5 14.8/30 (49 %) | no | **−0.180** |
| 35 | SHORT | 08-14 14:20 | LIQUIDITY LONG 2.50 | **kept** (1–1 tie) | 1.75 | Bullish Liquidity Grab w1.0 4.9/30 (16 %) | no | **−0.701** |
| 36 | SHORT | 08-15 07:50 | LIQUIDITY LONG 2.50 | **kept** (1–1 tie) | 2.50 | Bullish Liquidity Grab w1.0 15.0/30 (50 %) | no | **−0.757** |
| **45** | SHORT | 09-14 00:50 | LIQUIDITY LONG 2.50 | **zeroed** | 4.25 | Bullish Liquidity Grab w1.0 19.8/30 (66 %); Bullish Imbalance Mitigated w0.5 19.8/30 (66 %) | no | **−1.133** |

**PAPER, n = 8:**

| vpos | side | opened (UTC) | opposing | rule | proposed raw | opposing signals (weight, age of window) | in prompt? | R |
|---|---|---|---|---|---|---|---|---|
| 7 | LONG | 06-14 23:50 | LIQUIDITY SHORT 2.50 | kept | 2.50 | Bearish Liquidity Grab w1.0 20.0/30 (67 %) | no | +2.089 |
| 11 | SHORT | 06-23 00:30 | LIQUIDITY LONG 1.25 | kept | 2.50 | Bullish Imbalance Mitigated w0.5 15.1/30 (50 %) | no | +1.133 |
| 13 | SHORT | 06-24 13:25 | LIQUIDITY LONG 2.50 | kept | 1.75 | Bullish Imbalance Mitigated w0.5 10.0/30 (34 %); Bullish Liquidity Grab w1.0 10.1/30 (34 %) | no | +1.337 |
| 14 | SHORT | 06-25 14:00 | LIQUIDITY LONG 1.25 | zeroed | 3.75 | Bullish Imbalance Mitigated w0.5 25.1/30 (84 %) | no | −1.032 |
| 18 | LONG | 07-14 15:45 | LIQUIDITY SHORT 2.50 | zeroed | 6.25 | Bearish Liquidity Grab w1.0 15.1/30 (50 %); Broken U. w0.7 25.1/30 (84 %) | no | −1.074 |
| 19 | SHORT | 07-16 00:25 | LIQUIDITY LONG 2.50 | zeroed | 4.25 | Bullish Liquidity Grab w1.0 5.0/30 (17 %); Broken D. w0.7 15.0/30 (50 %) | no | +0.463 |
| 21 | LONG | 07-19 06:50 | LIQUIDITY SHORT 2.50 | zeroed | 4.75 | Bearish Liquidity Grab w1.0 25.0/30 (83 %) | no | +0.285 |
| 24 | SHORT | 07-29 20:05 | LIQUIDITY LONG 2.50 | zeroed | 5.00 | Bullish Imbalance Mitigated w0.5 25.0/30 (83 %); Bullish Liquidity Grab w1.0 29.9/30 (100 %) | no | −1.050 |

**Union: live 4 (zeroed 2 + kept 2), paper 8 (zeroed 5 + kept 3).** Every one of the 12 had the advisor say execute on a prompt that named none of it.

### 1c. OUTCOMES: any opposing category (zeroed or kept) vs none

> 🔴 **THE SIGN INVERTS BETWEEN THE BOOKS.** On live, the opposed entries did worse; on paper, they did better. **Live n = 4 ranks nothing.** This is stated before any conclusion.

| book | side | opposed (zeroed ∪ kept) | none |
|---|---|---|---|
| live | ALL | **n = 4** · ΣR −2.770 · 0/4 · mean −0.693 · **NOT RANKED** | n = 13 · ΣR +8.391 · 7/13 · mean +0.645 |
| live | LONG | n = 0 | n = 9 · ΣR +12.453 · 7/9 · mean +1.384 |
| live | SHORT | n = 4 · ΣR −2.770 · 0/4 · **NOT RANKED** | n = 4 · ΣR −4.062 · 0/4 · mean −1.015 · **NOT RANKED** |
| paper | ALL | **n = 8** · ΣR **+2.151** · 5/8 · mean +0.269 | n = 14 · ΣR −7.525 · 3/14 · mean −0.538 |
| paper | LONG | n = 3 · ΣR +1.300 · 2/3 · **NOT RANKED** | n = 6 · ΣR −5.347 · 0/6 · **NOT RANKED** |
| paper | SHORT | n = 5 · ΣR +0.851 · 3/5 · **NOT RANKED** | n = 8 · ΣR −2.179 · 3/8 · mean −0.272 |

**Ranked** (the only cell where both legs have n ≥ 8): paper ALL, 8 vs 14.
- Permutation **p = 0.0579 ≥ α 0.005**, so it **does not clear**.
- The sign (+, opposed did better) holds in both paper halves and in both paper regimes.
- **It is the opposite of live** (−), so it fails the paper/live control as well.

On the live SHORT side, the 4 opposed shorts (ΣR −2.770) did **no worse per trade** than the 4 unopposed shorts (ΣR −4.062). All 8 live shorts lost.

### 1d. Does the opposing signal's age matter? (descriptive)

Age fraction = age of the **freshest** opposing signal ÷ its category window (LIQUIDITY 30 min).

| book | freshest opposing signal | n · ΣR · wins | entries (vpos, side, fraction) |
|---|---|---|---|
| live | < 1/3 of window | 2 · −0.881 · 0/2 · **NOT RANKED** | 32 SHORT 0.00; 35 SHORT 0.16 |
| live | 1/3 – 2/3 | 2 · −1.890 · 0/2 · **NOT RANKED** | 36 SHORT 0.50; **45 SHORT 0.66** |
| live | ≥ 2/3 | 0 | — |
| paper | < 1/3 | 1 · +0.463 · 1/1 · **NOT RANKED** | 19 SHORT 0.17 |
| paper | 1/3 – 2/3 | 4 · **+3.485** · 3/4 · **NOT RANKED** | 7 LONG 0.67 (20.0 of 30); 11 SHORT 0.50; 13 SHORT 0.34; 18 LONG 0.50 |
| paper | ≥ 2/3 | 3 · −1.798 · 1/3 · **NOT RANKED** | 14 SHORT 0.84; 21 LONG 0.83; 24 SHORT 0.83 |

**No pattern that survives reading.**
- Live lost at every age: a 6-second-old grab (vpos 32), a 5-minute one (35) and a 20-minute one (45).
- Paper's middle bucket won 3 of 4.
- Every cell is n ≤ 4. vpos 45's 19.8 of 30 minutes is mid-window, not stale.
- **The age is rendered as a fact because it is one. It is not evidence of anything here.**

---

## 2. THE FIX: ONE PROMPT BLOCK, FACTS ONLY. APPLIED FROM FLAT

### 2a–2c. What is rendered, and its exact wording

**What was changed:**
- `claude_advisor.py` gained `_render_matrix_category_block(direction, matrix_result)` and a `_MATRIX_CATEGORIES` constant (== `signal_matrix.CATEGORIES`).
- In `consult_for_entry`: one assignment, `_category_block = _render_matrix_category_block(direction, matrix_result)`, and one `+ _category_block` term directly after `+ _matrix_line`.
- The data is `matrix_result['breakdown']` and `matrix_result['active_signals']`, already passed in since 2026-09-11. `main.py` was **not** touched.

**For each of the four categories**, in the matrix's own order:

| category state | rendered as |
|---|---|
| no signal | `{CAT} → no signal inside its {W}-min window` |
| intra-conflict | `{CAT} → 0 points, ZEROED: LONG and SHORT both inside its {W}-min window (LONG {pts}: …; SHORT {pts}: …)` |
| on the proposed side, counted | `{CAT} → {DIR} {pts} points, AGREES with the proposed {P}, counted in the {P} score (…)` |
| **opposing, zeroed** | `{CAT} → {DIR} {pts} points, OPPOSES the proposed {P}, ZEROED as the minority direction across categories (…)` |
| **opposing, kept (tie)** | `{CAT} → {DIR} {pts} points, OPPOSES the proposed {P}, not zeroed (the category counts are tied), counted only in the {DIR} score, which the score gate does not read for a {P} entry (…)` |

**Every signal** is listed as `Name w{weight} {age} of {window} min`, freshest first, with none dropped.

**Two closing lines, always rendered:**
- `Categories opposing the proposed {P} at scoring: … | none.`
- `Score gate arithmetic: the matrix score the score gate uses for this {P} entry is the {P}-side points only ({score}). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.`

**Facts only.** No instruction, threshold, "therefore", lean or outcome statistic. The contract bans 18 instruction words as whole words (`therefore, should, must, skip, execute, ignore, do not, trust, decide, weigh, recommend, avoid, consider, caution, beware, warning, better, worse`).
- "weight" is a fact and "weigh" is advice, hence whole-word matching.
- The 2026-08-05 line holds.

### 2d. AST proof: only the prompt builder changed

```
removed: {'helper': 1, 'const': 1, 'assign': 1, 'term': 1} (expected helper=1 const=1 assign=1 term=1)
after stripping ONLY the change: AST identical to backup = True
system-prompt assignments: bak 6/6 new 6/6 identical = True
top-level nodes: 51 -> 53
AST PROOF PASS
```

- The six system prompts are identical by sha256 (contract [7]).
- The other files are byte-identical before and after (md5, 19:53:10 → 20:09:12): all SOL `*.py` other than `claude_advisor.py`, including `signal_matrix.py`, `main.py`, `config.py`, `book_gate.py` and `virtual_trader.py`. Changed: `claude_advisor.py` only, `8dbe6511…` → `9e4f02be…`, sha256 `bff44d00fd0e0aa0` → `dcd7426c470b7f44`.
- Not touched: the minority rule, the score, every gate.

### 2e. BEFORE and AFTER on vpos 45's own stored prompt

**How this was built:**
- **BEFORE** is `trades.id 26586`'s stored `ai_user_prompt`, verbatim.
- **AFTER** is that same stored prompt with the block inserted exactly where the builder places it (directly under the matrix line). The block comes from the **live** `_render_matrix_category_block('SHORT', …)` applied to that row's own `trade_signal_matrix.breakdown_json` + `active_signals_json`.
- The builder cannot be re-run byte-for-byte on a past row: slot ages, walls and news are time-dependent.
- Contract [3] proves the builder's output equals the pre-change builder's output plus this block at exactly this position.

**BEFORE (verbatim, 2,745 chars):**
```
PROPOSED ENTRY: SHORT
Symbol: SOL/USDT:USDT
1H: Any Bearish Confirmation (direction: SHORT, set 1.8h ago — 110 of 360 min, 31% of its window, NOT stale)
15m: n/a (direction: n/a, age unknown)
5m trigger: Within Bearish OB (direction: SHORT)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.2642  |  Volume ratio 5m: 0.53x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 20.2 | 15m 37.9  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.695% | 15m 0.448% | 5m 0.265%
  EMA-gap: 1h 0.310% (Expanding) | 15m 0.406% (Contracting)  (Contracting/Flat = compression)
  LuxAlgo 1H trend slot: OCCUPIED (net 1H trend signal present in the matrix) | MTF alignment score: 3
  Measured beside it: 1h ADX 20.2 | OHLCV trend 1h BEAR / 4h BEAR
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: NEUTRAL, ADX 46.4, EMA-gap 1.746% (Contracting)
  4h: BEAR, ADX 18.2, EMA-gap 0.528% (Expanding)
  1h: BEAR, ADX 20.2, EMA-gap 0.310% (Expanding)
  15m: BEAR, ADX 37.9, EMA-gap 0.406% (Contracting)
  5m: NEUTRAL, ADX 32.6, EMA-gap 0.072% (Contracting)
  MTF alignment vs SHORT: 3/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $99.55  |  Imbalance ±1%: 0.49 (ask-heavy)
  Bid walls (>4x avg vol): $99.25 (p66, x11.0), $98.75 (p30, x5.6), $98.25 (p34, x5.9), $97.25 (p12, x4.5)
  Ask walls (>4x avg vol): $99.75 (p72, x12.4), $100.25 (p32, x5.8), $110.25 (p54, x8.6)
  Wall figures: pN = this wall's PERCENTILE among all walls this prompt has rendered (n=23,080; the primary figure), xN = the raw volume multiple (secondary). Every wall listed already passed the >4x filter, so the multiple alone does not distinguish an ordinary wall from a thick one — the percentile does. CALIBRATION: ~p50 is an ORDINARY wall, p90+ is genuinely thick. Judge thickness by the percentile, not by the word "massive" or by the multiple.

Tier agreement vs SHORT (computed for this consultation):
  1H: Any Bearish Confirmation -> SHORT = AGREES
  15m: ABSENT -> none = ABSENT
  5m trigger: Within Bearish OB -> SHORT = AGREES
  Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 2 agree, 0 oppose, 0 neutral, 1 absent.
  Score matrix, as the score gate counted these tiers (it counts every signal still inside its category window, not only the latest per slot): 1H → TREND SHORT +2.50, counted | 15m → MOMENTUM 0, no signal inside its 90-min window | 5m trigger → EXECUTION SHORT +1.75, counted
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.
```

**AFTER (3,871 chars):**
```
PROPOSED ENTRY: SHORT
Symbol: SOL/USDT:USDT
1H: Any Bearish Confirmation (direction: SHORT, set 1.8h ago — 110 of 360 min, 31% of its window, NOT stale)
15m: n/a (direction: n/a, age unknown)
5m trigger: Within Bearish OB (direction: SHORT)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.2642  |  Volume ratio 5m: 0.53x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 20.2 | 15m 37.9  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.695% | 15m 0.448% | 5m 0.265%
  EMA-gap: 1h 0.310% (Expanding) | 15m 0.406% (Contracting)  (Contracting/Flat = compression)
  LuxAlgo 1H trend slot: OCCUPIED (net 1H trend signal present in the matrix) | MTF alignment score: 3
  Measured beside it: 1h ADX 20.2 | OHLCV trend 1h BEAR / 4h BEAR
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: NEUTRAL, ADX 46.4, EMA-gap 1.746% (Contracting)
  4h: BEAR, ADX 18.2, EMA-gap 0.528% (Expanding)
  1h: BEAR, ADX 20.2, EMA-gap 0.310% (Expanding)
  15m: BEAR, ADX 37.9, EMA-gap 0.406% (Contracting)
  5m: NEUTRAL, ADX 32.6, EMA-gap 0.072% (Contracting)
  MTF alignment vs SHORT: 3/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $99.55  |  Imbalance ±1%: 0.49 (ask-heavy)
  Bid walls (>4x avg vol): $99.25 (p66, x11.0), $98.75 (p30, x5.6), $98.25 (p34, x5.9), $97.25 (p12, x4.5)
  Ask walls (>4x avg vol): $99.75 (p72, x12.4), $100.25 (p32, x5.8), $110.25 (p54, x8.6)
  Wall figures: pN = this wall's PERCENTILE among all walls this prompt has rendered (n=23,080; the primary figure), xN = the raw volume multiple (secondary). Every wall listed already passed the >4x filter, so the multiple alone does not distinguish an ordinary wall from a thick one — the percentile does. CALIBRATION: ~p50 is an ORDINARY wall, p90+ is genuinely thick. Judge thickness by the percentile, not by the word "massive" or by the multiple.

Tier agreement vs SHORT (computed for this consultation):
  1H: Any Bearish Confirmation -> SHORT = AGREES
  15m: ABSENT -> none = ABSENT
  5m trigger: Within Bearish OB -> SHORT = AGREES
  Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 2 agree, 0 oppose, 0 neutral, 1 absent.
  Score matrix, as the score gate counted these tiers (it counts every signal still inside its category window, not only the latest per slot): 1H → TREND SHORT +2.50, counted | 15m → MOMENTUM 0, no signal inside its 90-min window | 5m trigger → EXECUTION SHORT +1.75, counted
  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
    TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Any Bearish Confirmation w0.7 110 of 360 min, Bearish Confirmation+ w1.0 110 of 360 min)
    MOMENTUM → no signal inside its 90-min window
    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Imbalance Mitigated w0.5 20 of 30 min, Bullish Liquidity Grab w1.0 20 of 30 min)
    EXECUTION → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (Within Bearish OB w0.7 0 of 5 min)
  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (zeroed as the minority).
  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (4.25). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.
```

**Unified diff of the whole prompt (+7, −0):**
```diff
--- vpos45_stored_prompt (trades.id 26586, BEFORE)
+++ vpos45_prompt_with_category_block (AFTER)
@@ -30,5 +30,12 @@
   5m trigger: Within Bearish OB -> SHORT = AGREES
   Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 2 agree, 0 oppose, 0 neutral, 1 absent.
   Score matrix, as the score gate counted these tiers (it counts every signal still inside its category window, not only the latest per slot): 1H → TREND SHORT +2.50, counted | 15m → MOMENTUM 0, no signal inside its 90-min window | 5m trigger → EXECUTION SHORT +1.75, counted
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Any Bearish Confirmation w0.7 110 of 360 min, Bearish Confirmation+ w1.0 110 of 360 min)
+    MOMENTUM → no signal inside its 90-min window
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Imbalance Mitigated w0.5 20 of 30 min, Bullish Liquidity Grab w1.0 20 of 30 min)
+    EXECUTION → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (Within Bearish OB w0.7 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (zeroed as the minority).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (4.25). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
 Decide whether the bot should execute this entry now.
```

### 2f. Contract: `tests/test_entry_prompt_category_block.py` (new), green as root and as botuser

**How it runs:**
- Bytecode writing is off, `_call` is stubbed, and there is no network.
- **It opens no DB:** `signal_matrix` is replaced by a classify-only stub built from its own `SIGNAL_DICTIONARY` source, so its import-time `init_db` never runs.
- It is pinned to vpos 45 / 35 / 44 / 43's stored matrices, verbatim.
- **It goes red on the unpatched builder** (checked in a scratch copy: `AttributeError: module 'claude_advisor' has no attribute '_render_matrix_category_block'`, exit 1).

```
  [1] matrix_result=None == pre-change builder, byte for byte (1710 chars)
  [2] vpos 45 block rendered exactly as pinned, directly under the matrix line:
        Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
          TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Any Bearish Confirmation w0.7 110 of 360 min, Bearish Confirmation+ w1.0 110 of 360 min)
          MOMENTUM → no signal inside its 90-min window
          LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Imbalance Mitigated w0.5 20 of 30 min, Bullish Liquidity Grab w1.0 20 of 30 min)
          EXECUTION → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (Within Bearish OB w0.7 0 of 5 min)
        Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (zeroed as the minority).
        Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (4.25). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
  [3] prompt minus the block == pre-change builder prompt for the same matrix_result
  [5] kept-tie (vpos 35), all-intra (vpos 44), clean LONG (vpos 43) exactly as pinned
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): AttributeError: 'str' object has no attribute 'get'
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: direction or matrix_result has the wrong shape
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): AttributeError: 'str' object has no attribute 'get'
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): AttributeError: 'int' object has no attribute 'get'
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: direction or matrix_result has the wrong shape
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): AttributeError: 'int' object has no attribute 'get'
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): TypeError: 'in <string>' requires string as left operand, not NoneType
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: breakdown is not a dict or active_signals is not a list
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): TypeError: 'in <string>' requires string as left operand, not NoneType
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): AttributeError: 'NoneType' object has no attribute 'get'
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: breakdown is not a dict or active_signals is not a list
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): AttributeError: 'NoneType' object has no attribute 'get'
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: breakdown is not a dict or active_signals is not a list
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: breakdown is not a dict or active_signals is not a list
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: breakdown has no LIQUIDITY
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: could not convert string to float: 'abc'
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: TREND net_direction 'UP'
[MERCURY-SOL][MATRIX-CATEGORIES] render failed (non-fatal, block omitted): ValueError: an active signal is not a dict
  [6] malformed or absent matrix_result: no exception, no block, prompt == pre-change builder
OK — every scored category is named under the matrix line, opposing ones plainly; nothing else in the prompt moved; 6 system prompts byte-identical
```

- root exit 0 · botuser exit 0. The two outputs are identical apart from the non-fatal `[MATRIX-CATEGORIES] render failed` log lines that check [6] provokes on purpose.

**The existing contracts, re-run in place (root and botuser):**
- `test_entry_prompt_matrix_line.py`: **OK** (both).
  - 🔶 **Amended, check [3] only.** It compared "prompt minus the matrix line" with the no-matrix prompt, and the new block now sits under that line whenever `matrix_result` is present. It now strips the new block too before comparing, and still pins everything else.
  - Backup: `tests/test_entry_prompt_matrix_line.py.bak_categoryblock_20260914`.
- `test_entry_prompt_regime_line_is_legible.py`: **OK** (both), unchanged.

### 2g. Applied FROM FLAT, restarted, verified from the loaded bytecode

```
20:03:53  FLAT CHECK   virtual_positions open 0 · active_positions 0 · exit_pending 0 · neutral1h_followthrough 0
                       Bybit GET /v5/position/list SOLUSDT: positionIdx 2 size 0 · positionIdx 1 size 0 (retCode 0)
                       last trades row 26793 at 19:40:06 (5m no_trend)
20:04:15  PATCH        backups written and sha-verified FIRST:
                         claude_advisor.py.bak_categoryblock_20260914               sha256 bff44d00fd0e0aa0
                         tests/test_entry_prompt_matrix_line.py.bak_categoryblock_20260914   602672b37d70d679
                       os.replace (source ast.parse()d first):
                         claude_advisor.py                          -> dcd7426c470b7f44
                         tests/test_entry_prompt_matrix_line.py     -> 8eaa73ea3cdd6a73
                         tests/test_entry_prompt_category_block.py  -> 1e80700a35d7606d  (new)
20:04–20:05 CONTRACTS  3/3 root · 3/3 botuser · AST PROOF PASS (in place, backup vs live file)
20:05:26  RE-CHECK     open vpos 0 · active 0 · exit_pending 0 · no new trades row since 19:40:06 (20:05 boundary passed quiet)
20:05:45  systemctl restart mercury-sol     MainPID 1341949 -> 2216962 · worker 2217020 · active 20:06:02 · NRestarts 0
20:06:17  [MERCURY-SOL] [BOOT] taker fee: 0.001 (0.1000%) source=venue | geometry constant BYBIT_TAKER_FEE_RATE=0.00055 is unchanged and separate
20:06:18  [MERCURY-SOL] [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
20:06:18  [MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 2217020]
20:06:18  [MERCURY-SOL] [VPOS-RECONCILE] no open positions at boot — clean.
20:06:21  [MERCURY-SOL][VIRTUAL] [HEARTBEAT] alive ticks=1 (+1 in 4s) last_tick=3.6s max_tick=3.6s cadence=10s open=0 mode=LIVE pid=2217020
LOADED    __pycache__/claude_advisor.cpython-312.pyc written 20:06:05 — header mtime 1789416255 size 91841
            == claude_advisor.py (mtime 1789416255, size 91841, sha256 dcd7426c470b7f44)
            '_render_matrix_category_block' present in the module's bytecode names
          __pycache__/main.cpython-312.pyc          header == main.py          (sha 91dfa43f251c6245, unchanged, compiled 09-11 18:27:00)
          __pycache__/signal_matrix.cpython-312.pyc header == signal_matrix.py (sha a075ce05137f03b4, unchanged)
          __pycache__/config.cpython-312.pyc        header == config.py        (sha a308a130e4dde9f6, unchanged)
20:07     openitems_guard EXIT=0
```

**Rollback:**
- `cp claude_advisor.py.bak_categoryblock_20260914 claude_advisor.py`
- `cp tests/test_entry_prompt_matrix_line.py.bak_categoryblock_20260914 tests/test_entry_prompt_matrix_line.py`
- remove `tests/test_entry_prompt_category_block.py`
- restart **from flat**.

### 2h. 🔴 COHORT BOUNDARY, and what this CANNOT do

> 🔴 **COHORT BOUNDARY: 2026-09-14 20:06:18 UTC** (worker pid 2217020 booted with the patched builder). **Entry consultations with `trades.id > 26793` saw the block; ≤ 26793 did not.** Never pool the two cohorts when judging advisor verdicts. Recorded in `OPEN-ITEMS-SOL.md §PROMPT-CATEGORY-BLOCK-2026-09-14`.

**What it CANNOT do, stated plainly:**
- **It cannot stop the model concluding wrongly from correct facts.**
  - On 2026-08-31 the zeroed-tier label was already present on all nine live SOL cases, and the narration built on the tier anyway.
  - Putting a fact on the page is not the same as the model using it. The block names the opposing LIQUIDITY; it does not refuse the entry and was deliberately built so that it could not.
- **The book cannot tell whether naming it will help.** Opposed entries lost on live (n = 4) and won on paper (n = 8), and nothing ranks (§1c). The effect of this block is not measurable with the n this bot produces in weeks.
- **The 60-second state-verdict cache key is unchanged** (slot identities plus nearest opposing wall). Inside one minute, a reused verdict can come from a prompt whose block differed, for example if an opposing signal expired in between. Provenance is kept: `ai_user_prompt` names the prompt that produced the verdict, and `ai_verdict_reuse_json.rendered_user_prompt` is this row's.
- **It changes nothing mechanical.** The score gate still never nets opposition; the minority rule still zeroes it.

**Live proof: pending.**
- No entry consultation had arrived between the restart (20:06:18) and publication; the last trades row was 19:40:06.
- A **read-only** waiter (`trades.db ?mode=ro`, up to 6 h) will take the first entry consultation with `trades.id > 26793`. It checks that the block sits directly under the matrix line, and that every category line agrees with that row's own stored `matrix_breakdown_json`.
- **The result will be APPENDED to THIS file, at this same URL.**
- What IS proven now: the running worker imported the patched builder (§2g); the builder renders the block on vpos 45's stored inputs (§2e); the contract pins the wording and that nothing else moved (§2f).

---

## 3. 🔴 THE SHORT SIDE HAS NEVER TRADED ITS OWN REGIME (READ-ONLY)

**Label check.** `trend_1d` at entry was recomputed from Bybit daily candles with the bot's own rule (`indicators._classify_trend`: EMA9/EMA21 plus 3-bar EMA9 slope over 200 bars), at the prior-day close and at the entry-day close.
- **37 of 39** stored labels are reproduced by one of the two.
- vpos 8 stored NULL. vpos 21 (a LONG) stored `bear`, recompute `neutral` at both closes. Intraday, the bot uses the forming candle.
- **Every short's label is reproduced.**

### 3a. Every SHORT, both books, by `trend_1d` at entry (n first)

| book | daily | n | ΣR | wins | mean | max MFE | vpos (R) |
|---|---|---|---|---|---|---|---|
| **live** | BULL | **2** | −0.823 | 0/2 (0 %) | −0.411 | 0.51R | 32 (−0.180), 34 (−0.643) · **NOT RANKED** |
| **live** | NEUTRAL | **6** | −6.009 | **0/6 (0 %)** | −1.002 | 0.73R | 35 (−0.701), 36 (−0.757), 37 (−1.226), 42 (−1.083), 44 (−1.110), 45 (−1.133) · **NOT RANKED** |
| **live** | **BEAR** | **0** | — | — | — | — | **the live book has never seen one** |
| paper | BULL | 0 | — | — | — | — | — |
| paper | NEUTRAL | **6** | −0.450 | **4/6 (67 %)** | −0.075 | 1.18R (4 sampled) | 10 (−1.066), 11 (+1.133), 15 (+0.140), 17 (+0.004), 19 (+0.463), 20 (−1.124) · **NOT RANKED** |
| paper | **BEAR** | **7** | −0.878 | **2/7 (29 %)** | −0.125 | 2.51R (5 sampled) | 13 (+1.337), 14 (−1.032), 23 (−0.577), 24 (−1.050), 25 (+1.257), 27 (−0.660), 28 (−0.153) · **NOT RANKED** |

MFE was not sampled for vpos 7–14.

### 3b. 🔴 Is the short side bad, or has it only traded a regime against it?

**What is measurable now does not support "it only traded the wrong regime".**
1. **On paper, where both labels exist, a BEAR daily did not help shorts.** BEAR daily: 2 of 7 won, mean −0.125. NEUTRAL daily: 4 of 6 won, mean −0.075.
2. **At the same NEUTRAL label, live and paper shorts are far apart:** 0 of 6 (mean −1.002) against 4 of 6 (mean −0.075). The label is the same; the book (era) is different. What separates the shorts is not what `trend_1d` reads.
3. **`trend_1d` is a lagging EMA stack.**
   - A NEUTRAL daily inside the paper era's 64–84 range and a NEUTRAL daily inside the live era's 73.6 → 103.6 rally are the same label on different markets.
   - All six live NEUTRAL shorts were entered in that rally, and none reached +1R (best 0.73R).
   - That is a description of the two eras, **not a test**. No cell has n ≥ 8.

**The honest answer:** the short side cannot be shown to be bad in a bear regime, and cannot be shown to be good in one. The only bear-regime shorts this bot has ever taken are 7 paper trades, and they were not better than the paper shorts without a bear daily.

### 3c. The same split for LONGS (the control)

| book | daily | n | ΣR | wins | mean | max MFE |
|---|---|---|---|---|---|---|
| live | BULL | **7** | **+10.336** | 5/7 (71 %) | +1.477 | 4.99R · NOT RANKED |
| live | NEUTRAL | 2 | +2.117 | 2/2 | +1.058 | 1.82R · NOT RANKED |
| live | BEAR | 0 | — | — | — | — |
| paper | BULL | 1 | −1.064 | 0/1 | −1.064 | 0.29R · NOT RANKED |
| paper | NEUTRAL | 4 | −0.394 | 1/4 (25 %) | −0.098 | 0.89R · NOT RANKED |
| paper | BEAR | 3 | −1.850 | 1/3 (33 %) | −0.617 | 1.44R · NOT RANKED |
| paper | NULL | 1 | −0.739 | 0/1 | — | n/a |

**The control shows the same shape.** Live longs with a BULL daily made +10.336R; the one paper long with a BULL daily lost. The daily label goes with good outcomes on live and not on paper, for longs as for shorts. What differs is the era.

### 3d. 🔴 What "no SHORT unless `trend_1d` is BEAR" would have refused

This is a first-order counterfactual on taken entries only. It does not model the entries a freed "max 1 SHORT" slot might have admitted instead.

| book | shorts refused | ΣR refused | **winners refused** | shorts kept | ΣR kept |
|---|---|---|---|---|---|
| **live** | **8 of 8** | **−6.832** | none | **0** | — |
| **paper** | 6 of 13 | −0.450 | 🔴 **4: vpos 11 (+1.133R), 15 (+0.140R), 17 (+0.004R), 19 (+0.463R)** | 7 | −0.878 |

🔴 **On paper it refuses four winners**, including two of the four paper shorts that won more than +0.4R (vpos 11 and 19; the other two, 13 and 25, had a BEAR daily).

**Entries per month that remain:**

| book | month | entries before → after | shorts before → after | book ΣR before → after |
|---|---|---|---|---|
| live | 2026-08 | 13 → 8 | 5 → 0 | +7.224 → +10.730 |
| live | 2026-09 | 4 → 1 | 3 → 0 | −1.603 → +1.723 |
| paper | 2026-06 | 8 → 6 | 4 → 2 | +0.408 → +0.342 |
| paper | 2026-07 | 10 → 6 | 6 → 2 | −5.141 → −4.625 |
| paper | 2026-08 | 4 → 4 | 3 → 3 | −0.641 → −0.641 |

**On live, the rule "works" only because it deletes the entire short side:** 0 shorts in 38 days. On paper it cuts shorts from 13 to 7, gains +0.450R and refuses four winners.

**Nothing is proposed.**

### 3e. 🔴 What the live book CANNOT answer

- **The live book has never seen a BEAR daily.** The last BEAR daily close was 2026-08-06; live trading began 2026-08-07 22:25.
- **Any conclusion about shorts in a bear regime rests on paper alone, and paper is 7 trades:** 2 wins, ΣR −0.878. Those 7 did not beat the paper shorts that had no bear daily.
- The live book **cannot** say whether SOL's shorts work in a bear market. It can only say that 8 shorts in a rising market lost.

### 3f. Controls where anything is ranked

| cell | legs | ranked? |
|---|---|---|
| SHORT, BEAR daily vs not, live | 0 vs 8 | **NOT RANKED** |
| SHORT, BEAR daily vs not, paper | 7 vs 6 | **NOT RANKED** |
| LONG, BULL daily vs not, live | 7 vs 2 | **NOT RANKED** |
| LONG, BULL daily vs not, paper | 1 vs 8 | **NOT RANKED** |

**Nothing in §3 reaches n ≥ 8 on both legs**, so the chronological-halves, TREND/FLAT and paper/live controls have nothing to apply to. That is itself the finding: the question is not measurable on this bot's book today.

---

## 4. THE ACCOUNTING GAP: RECORDED IN THE CANON, NOT FIXED

New section **`OPEN-ITEMS-SOL.md §LIVE-BOOK-VS-VENUE-GAP-2026-09-14`**, inserted at the top of the dated sections.
- Backup: `OPEN-ITEMS-SOL.md.bak_categoryblock_20260914`.
- The `§BOOK-GATE-RECUT-2026-09-11` anchor that `scripts/sol_book_gate_review.py` cites is intact, once.

| component | row ids | venue − DB |
|---|---|---|
| Two LONG emergency closes at the venue with **no `virtual_positions` row**: 2026-08-08 06:50 (Bybit qty 2.6, 74.795 → 74.78, closedPnl −0.427895) and 08:35 (qty 2.6, 74.85 → 74.84, closedPnl −0.415194) | `trades` **16748** `sl_failed_position_closed` + **16749** `failed` ("entry fill unreadable…"); **16765** `failed` + **16766** `sl_failed_position_closed` | **−$0.8431** |
| vpos 40: DB close 100.18 vs venue avgExit **99.92**, qty 1.0 | `virtual_positions` **40**, entry row `trades` **20271**, `trades_close_row_id` NULL | **−$0.2597** |
| vpos 29 / 30 / 38: small leg and fee differences | vpos 29 (entry 16767), 30 (16857), 38 (19689) | −$0.0246 / −$0.0090 / −$0.0239 |
| the SHORT side, 8 closes | vpos 32, 34, 35, 36, 37, 42, 44, 45 | $0.0000, agrees to the cent |

🔴 **Every P&L figure quoted from the DB for the live era is overstated by ≈ $1.16.**
- Through vpos 45, the DB live book reads **+$13.7167**; Bybit `closed-pnl` for the same era reads **+$12.5563**.
- **No later pass may read the DB book as venue truth.** Quote the venue, or subtract the gap and say so.
- Venue `closedPnl` excludes funding, so the residual is approximate at the cent level.
- **Nothing was written to the DB:** no row added, adjusted or backfilled.

A second new section, `§PROMPT-CATEGORY-BLOCK-2026-09-14`, records §2: what was applied, the cohort boundary, what it cannot do, and the rollback.

---

## CONFIRMATION

| item | state |
|---|---|
| **`openitems_guard`** | EXIT **0** at 19:53 (first) and EXIT **0** at 20:07 (after the restart) |
| **SOL DB** | every measurement opened it `file:…?mode=ro` with `PRAGMA query_only=1` (verified `= 1`); **no write by this session**. §2 wrote no DB row; the restarted bot writes its own rows as always |
| **SOL config** | **not imported by any measurement**: `config.py` and `signal_matrix.py` were parsed with `ast`. The three prompt contracts import `claude_advisor`, which imports `config` read-only, exactly as the two pre-existing contracts do. `config.py` md5 unchanged |
| **orders / venue** | **no orders**. Venue calls this pass: signed **`GET /v5/position/list`** (flat check). The daily candles and `closed-pnl` used in §3/§4 were fetched by GET in the 19:04 pass |
| **restart** | **one**, authorised by §2g, from flat: `mercury-sol` MainPID 1341949 → 2216962, **NRestarts 0 → 0** |
| **Titan** | **untouched**. `titan` **NRestarts 0 → 0**, MainPID 1572470 unchanged. md5 of `titan-bot/config.py` and every `titan-bot/*.py` identical 19:53 → 20:09. Titan's DB never opened. Titan's only reads were the guard itself, which imports its config and reads git by design |
| **`FLAT_ADX_GATE_DRYRUN`** | **True** (config.py:407), unchanged |
| **`BOOK_GATE_DRYRUN`** | **False** (config.py:475), unchanged |
| **book-gate review counter** | **not written by this session.** `sol_book_gate_review.json` md5 changed 19:53 → 20:09 **only because its own 30-min cron ran at 20:00:05** (`last_run`); counts unchanged, LONG 0/135, SHORT 0/112, fired `review_point` only, `new=[]` |
| **files written in SOL's tree** | `claude_advisor.py` (patched) · `tests/test_entry_prompt_category_block.py` (new) · `tests/test_entry_prompt_matrix_line.py` (check [3] amended) · `OPEN-ITEMS-SOL.md` (+2 sections) · three `.bak_categoryblock_20260914` backups · `__pycache__/claude_advisor.cpython-312.pyc` (rewritten by the service at boot) |
| **still running** | the read-only live-proof waiter, which appends to this report at this URL |
