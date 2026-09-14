# mercury-sol-replay-opposed-entries-with-the-category-block

_2026-09-14 21:19 UTC_

---

# Mercury-SOL — replaying the opposed entries through the model with the category block

**2026-09-14 · READ-ONLY on both bots · a prompt-response measurement, nothing proposed, nothing applied** · `openitems_guard` EXIT 0 before (21:01) and after (21:20)

**Population:** the 12 entries of `reports/2026-09-14-2013-mercury-sol-show-the-advisor-the-opposing-category.md` §1b. Live: vpos 32, 35, 36, 45. Paper: vpos 7, 11, 13, 14, 18, 19, 21, 24.

> 🔴 **THIS IS NOT A BACKTEST AND MUST NOT BE READ AS ONE.**
> * It measures whether adding the category block to a stored prompt changes the model's **verdict**.
> * It does **not** measure whether a changed verdict would have made or lost money.
> * 🔴 **Even if all 12 flipped to skip, that would say nothing about whether skipping them was right.** §1c of the 2013 report showed opposed entries **LOST on live (n = 4)** and **WON on paper (n = 8)**.

> **THE ARITHMETIC, STATED BEFORE THE RESULT**
> * **Outcomes:** n = 12 rows, 4 live and 8 paper, **never pooled. No outcome cell ranks**, and none is tested here.
> * **What is tested:** only the model's response to the prompt change, one test per row.
>   - N = **10** calls per arm per row, so 12 × 2 × 10 = **240 calls**.
>   - Test: execute-count BEFORE vs AFTER, two-sided Fisher exact.
>   - **Bonferroni over 12 rows: α = 0.05/12 = 0.00417.**
>   - N = 10 was chosen so that a single row *can* clear that α. At N = 5 the smallest possible p is 0.0079 > α, and nothing would have been testable.
> * **The control that decides:** a row is **readable only if its BEFORE arm is stable**, meaning all 10 BEFORE runs gave the same verdict. If BEFORE alone flips between execute and skip, that row's effect is **not read**, whatever its p.
> * **When this was fixed:** the α, the readability rule and the mention rule were written into the analysis script while the replay was running. Only the first three calls had been looked at, and only to check for API errors.
> * **Cost and calls, stated before running:** 240 calls, upper bound **$0.69** (input chars ÷ 3 tokens at $1/MTok, plus every call hitting the 256-token output cap at $5/MTok). **Actual: 403,470 input + 28,170 output tokens = $0.5443.**

---

## VERDICT

**The block changes the verdict on some rows and not on others. It is neither inert nor uniform.**

**Readable rows (BEFORE stable at 10/10 execute): 9 of 12.** Live 2 of 4, paper 7 of 8.

- 🔴 **Flipped to skip, clearing α:** 4, namely vpos 36 (live, 10/10 → 1/10 execute, p 1.2e-04), vpos 7 (paper, 10/10 → 0/10 execute, p 1.1e-05), vpos 11 (paper, 10/10 → 0/10 execute, p 1.1e-05), vpos 13 (paper, 10/10 → 1/10 execute, p 1.2e-04).
- **Did not move at all:** 4, namely vpos 32 (live, 10/10 → 10/10), vpos 14 (paper, 10/10 → 10/10), vpos 18 (paper, 10/10 → 10/10), vpos 19 (paper, 10/10 → 10/10).
- **Moved partly, not clearing α:** vpos 24 (paper, 10/10 → 7/10, p 0.21).

**Unreadable rows (BEFORE itself not stable): 3.** Their effect is **not read**, per the rule declared above:
- **vpos 35** (live): BEFORE 7/10 execute → AFTER 4/10 execute (p 3.7e-01).
- **vpos 45** (live): BEFORE 9/10 execute → AFTER 0/10 execute (p 1.2e-04).
- **vpos 21** (paper): BEFORE 1/10 execute → AFTER 10/10 execute (p 1.2e-04).

Two facts about those three rows:
- **vpos 45 is the trade that started this.** BEFORE executed 9 of 10; AFTER executed 0 of 10.
- **vpos 21 moved the OTHER way.** BEFORE executed only 1 of 10, even though its stored live verdict was execute. With the block, it executed 10 of 10, and six of those ten reasons name the opposing LIQUIDITY and discount it: *"minority-zeroed"*, *"minor noise"*, *"aged (25min) and outvoted"*.

**By book, never pooled:**
- **Live, 4 rows:** readable 2. Of those, 1 flipped (vpos 36) and 1 did not move (vpos 32). BEFORE execute 36/40 → AFTER 15/40.
- **Paper, 8 rows:** readable 7. Of those, 3 flipped (vpos 7, 11, 13), 3 did not move (vpos 14, 18, 19) and 1 moved partly (vpos 24). BEFORE execute 71/80 → AFTER 48/80.

**Does the AFTER reason MENTION the opposing category? 28 of 120 AFTER reasons do, and 0 of 120 BEFORE reasons do.** This is a separate, weaker question from whether the verdict changed.

- **Where the verdict flipped, the narration mostly does not name the cause.**
  - vpos 36: 9 skips, 1 reason names the opposition.
  - vpos 11: 10 skips, 1.
  - vpos 13: 9 skips, 2.
  - vpos 45: 10 skips, 2.
  - vpos 7: 10 skips, 4.
  - The flipped skips cite ADX, walls, a stale 1H, or "1d NEUTRAL". Those facts were in the BEFORE prompt too, where the same model executed. This is the 2026-08-08 canon again: the reason correlates with the verdict, it does not explain it.
- **Where the verdict did NOT move, the narration names the opposition and discounts it.**
  - vpos 21: 6/10, e.g. *"Liquidity opposes but minority-zeroed. Execute…"*.
  - vpos 24: 5/10. vpos 18: 2/10, *"Liquidity signal minority"*. vpos 32: 2/10, *"LIQUIDITY category opposition is minority-zeroed"*. vpos 14 and 19: 1/10 each.
  - The word "zeroed" from the block is itself being cited as a reason the opposition does not count.

**A descriptive pattern, NOT declared and NOT tested:**
- **All four readable rows where the opposing LIQUIDITY was KEPT on a tie flipped:** vpos 36, 7, 11, 13.
- **None of the five readable rows where it was ZEROED as the minority flipped fully:** vpos 32, 14, 18, 19 did not move; 24 moved partly.
- It is confounded. The kept rows are also the ones with the lowest proposed-side scores (1.75–2.50, against 3.75–6.25 on the zeroed rows).
- n = 4 and 5 rows. **It is reported, not ranked.**

**The honest reading, against the three cases the question set out:**
- **"Most AFTER arms flip to skip and BEFORE is stable"**: NO. 4 of 9 readable rows flipped.
- **"Verdicts do not move, the block is inert"**: NO. On 4 readable rows it moved 10/10 execute to ≤ 1/10, each with p ≤ 1.2e-4 < α.
- **"BEFORE arms are unstable, unanswerable"**: for 3 of 12 rows, YES (35, 45, 21). For the other 9, NO.
- **So: the fact does change the decision on some rows, and only that.** It also changes the narration less than it changes the verdict.
- **What this measures:** the whole block, which names all four categories, intra-conflicts, ages and the gate arithmetic. Not the one OPPOSES line in isolation.
- **Outcome:** not measured. No change is recommended.

- For the record, and **only** as the caution the question asked for: the four readable rows the block flipped to skip are vpos 36 (live, −0.757R), 7 (paper, +2.089R), 11 (paper, +1.133R) and 13 (paper, +1.337R). **Three of the four were paper winners. n = 4, not ranked, not a backtest.**

---

## 1. THE PAIRS

**How each pair is built:**
- **BEFORE** = the row's stored `trades.ai_user_prompt`, verbatim.
- **AFTER** = the same stored prompt with the block inserted. The block comes from the **live** `claude_advisor._render_matrix_category_block` (source sha256 `dcd7426c470b7f44`, the file loaded at 20:06:05), applied to that row's own `trade_signal_matrix.breakdown_json` and `active_signals_json`. This is the method §2e used for vpos 45.
- `claude_advisor` was imported with bytecode writing off and `signal_matrix` stubbed, so no DB was opened and no file was written.
- **Insertion point:**
  - Rows in the tier-agreement format (live 32, 35, 36, 45): directly above *"The cascade gate, the score gate and the risk gate have already passed."* That is exactly where the live builder puts it, under the tally and matrix line.
  - Rows in the pre-2026-08-01 format (all 8 paper rows): the prompt has no tier-agreement block, so the block is inserted directly above *"The 3 timeframes are aligned (confluence has already passed)."* That is the same last-context position, before the question. This layout never existed live; stated, not hidden.
- **System prompt:** each row's own stored `ai_system_prompt`, verbatim, in BOTH arms. It is not today's, where they differ.
- **Model and settings:** identical to `claude_advisor._call`: `claude-haiku-4-5-20251001`, which is also the model all 12 rows ran under; `max_tokens` 256; system as one text block with `cache_control: ephemeral`; **no `temperature` sent**, so both arms and the live path use the same API default.
- **Differences from the live call, and neither is a model setting:** timeout 30 s instead of 10 s, and `max_retries` 2 instead of 0, so that no replay call is lost as 'unavailable'.
- **Order:** 10 rounds; within each round the 12 rows were shuffled, and BEFORE/AFTER order was shuffled per row (seed 20260914).
- **Timing:** calls were sequential and paused from 10 s before to 75 s after every 5-minute alert boundary, so the live advisor never competed for the key.
- **Result:** 240 of 240 calls returned `end_turn` with parseable JSON. 0 API errors. 0 cache writes (below the cache minimum).

| vpos | book | side | stored verdict | system prompt the row ran under (used in both arms) | anchor | BEFORE chars | AFTER chars | Δ | diff |
|---|---|---|---|---|---|---|---|---|---|
| 32 | live | SHORT | execute 0.78 | `_ENTRY_SYSTEM_V2_ALIGNED_SHORT` | tier-agreement | 2,356 | 3,562 | **+1,206** | **+7 / −0** |
| 35 | live | SHORT | execute 0.72 | `_ENTRY_SYSTEM` | tier-agreement | 3,037 | 4,219 | **+1,182** | **+7 / −0** |
| 36 | live | SHORT | execute 0.78 | `_ENTRY_SYSTEM` | tier-agreement | 3,055 | 4,241 | **+1,186** | **+7 / −0** |
| 45 | live | SHORT | execute 0.72 | `_ENTRY_SYSTEM` | tier-agreement | 2,745 | 3,871 | **+1,126** | **+7 / −0** |
| 7 | paper | LONG | execute 0.72 | `_ENTRY_SYSTEM` | pre-08-01 | 1,261 | 2,705 | **+1,444** | **+7 / −0** |
| 11 | paper | SHORT | execute 0.78 | `RETIRED (sha 04f982146a96, matches none of today's six)` | pre-08-01 | 1,282 | 2,765 | **+1,483** | **+7 / −0** |
| 13 | paper | SHORT | execute 0.78 | `RETIRED (sha 04f982146a96, matches none of today's six)` | pre-08-01 | 1,330 | 2,594 | **+1,264** | **+7 / −0** |
| 14 | paper | SHORT | execute 0.78 | `RETIRED (sha 04f982146a96, matches none of today's six)` | pre-08-01 | 1,294 | 2,509 | **+1,215** | **+7 / −0** |
| 18 | paper | LONG | execute 0.72 | `_ENTRY_SYSTEM_V2_ALIGNED` | pre-08-01 | 1,274 | 2,511 | **+1,237** | **+7 / −0** |
| 19 | paper | SHORT | execute 0.72 | `_ENTRY_SYSTEM_V2_ALIGNED_SHORT` | pre-08-01 | 1,299 | 2,582 | **+1,283** | **+7 / −0** |
| 21 | paper | LONG | execute 0.78 | `_ENTRY_SYSTEM_V2_ALIGNED` | pre-08-01 | 1,298 | 2,492 | **+1,194** | **+7 / −0** |
| 24 | paper | SHORT | execute 0.82 | `_ENTRY_SYSTEM_V2_ALIGNED_SHORT` | pre-08-01 | 1,279 | 2,566 | **+1,287** | **+7 / −0** |

**On every row the two arms differ ONLY by the block:** the unified diff is +7 / −0, and the added lines, joined, equal the block byte for byte (asserted in the build).
**System prompts vs today:** 4 rows ran under today's `_ENTRY_SYSTEM`, 3 under today's `_ENTRY_SYSTEM_V2_ALIGNED_SHORT`, 2 under today's `_ENTRY_SYSTEM_V2_ALIGNED`. **3 (vpos 11, 13, 14) ran under a system prompt that no longer exists** (sha `04f982146a96`); each was replayed under its own.

---

## 2. RESULTS PER ROW

α = 0.00417 (Bonferroni over 12 rows). "readable" = BEFORE stable (10/10 same verdict). "names opp." = reasons naming the opposing category (method in §2c).

| vpos | book | side | opposing (rule) | BEFORE execute / skip | AFTER execute / skip | BEFORE stable? | Fisher p | reading | names opp. BEFORE / AFTER | mean conf B / A |
|---|---|---|---|---|---|---|---|---|---|---|
| **32** | live | SHORT | LIQUIDITY LONG 2.50 (zeroed) | 10 / 0 | 10 / 0 | yes | 1.0e+00 | no change | 0 / 2 | 0.78 / 0.78 |
| **35** | live | SHORT | LIQUIDITY LONG 2.50 (kept (tie)) | 7 / 3 | 4 / 6 | **no** | 3.7e-01 | **UNREADABLE** — BEFORE unstable | 0 / 1 | 0.73 / 0.73 |
| **36** | live | SHORT | LIQUIDITY LONG 2.50 (kept (tie)) | 10 / 0 | 1 / 9 | yes | 1.2e-04 | **flipped** toward skip | 0 / 1 | 0.75 / 0.73 |
| **45** | live | SHORT | LIQUIDITY LONG 2.50 (zeroed) | 9 / 1 | 0 / 10 | **no** | 1.2e-04 | **UNREADABLE** — BEFORE unstable | 0 / 2 | 0.73 / 0.72 |
| **7** | paper | LONG | LIQUIDITY SHORT 2.50 (kept (tie)) | 10 / 0 | 0 / 10 | yes | 1.1e-05 | **flipped** toward skip | 0 / 4 | 0.76 / 0.77 |
| **11** | paper | SHORT | LIQUIDITY LONG 1.25 (kept (tie)) | 10 / 0 | 0 / 10 | yes | 1.1e-05 | **flipped** toward skip | 0 / 1 | 0.77 / 0.82 |
| **13** | paper | SHORT | LIQUIDITY LONG 2.50 (kept (tie)) | 10 / 0 | 1 / 9 | yes | 1.2e-04 | **flipped** toward skip | 0 / 2 | 0.78 / 0.78 |
| **14** | paper | SHORT | LIQUIDITY LONG 1.25 (zeroed) | 10 / 0 | 10 / 0 | yes | 1.0e+00 | no change | 0 / 1 | 0.77 / 0.74 |
| **18** | paper | LONG | LIQUIDITY SHORT 2.50 (zeroed) | 10 / 0 | 10 / 0 | yes | 1.0e+00 | no change | 0 / 2 | 0.77 / 0.78 |
| **19** | paper | SHORT | LIQUIDITY LONG 2.50 (zeroed) | 10 / 0 | 10 / 0 | yes | 1.0e+00 | no change | 0 / 1 | 0.77 / 0.74 |
| **21** | paper | LONG | LIQUIDITY SHORT 2.50 (zeroed) | 1 / 9 | 10 / 0 | **no** | 1.2e-04 | **UNREADABLE** — BEFORE unstable | 0 / 6 | 0.76 / 0.72 |
| **24** | paper | SHORT | LIQUIDITY LONG 2.50 (zeroed) | 10 / 0 | 7 / 3 | yes | 2.1e-01 | partial, not significant | 0 / 5 | 0.80 / 0.76 |

- **Stored live verdict vs replayed BEFORE arm:** the stored verdict was `execute` on all 12 rows.
  - The BEFORE arm reproduced it on 10/10 runs for 9 rows and 9/10 for vpos 45.
  - It reproduced it on 7/10 for vpos 35.
  - **It reproduced it on only 1/10 for vpos 21: that row's live execute was the minority outcome of its own prompt.**
- No run returned anything other than `execute` or `skip`.

### 2c. How "names the opposing category" was counted

**Rule:** a reason counts only if it contains `liquidity` used as the category or signal, or the opposing signal's own name (e.g. "Liquidity Grab", "Imbalance Mitigated", "Broken U."), or "minority" / "opposing categor…".
- Excluded automatically: "liquidity" after bid / ask / resting / support / absorb / thin / book / deep, or before wall / zone / pool / cluster.
- Every remaining hit was then read. These were excluded by hand as wall or market talk, listed by call id:

- call 71 (vpos 11 AFTER): wall talk: "blocks downside liquidity"
- call 208 (vpos 11 AFTER): wall talk: "blocks downside liquidity"
- call 100 (vpos 13 AFTER): market talk: "no clear short breakout liquidity"
- call 166 (vpos 36 AFTER): wall talk: "absorbs downside liquidity"
- call 34 (vpos 7 BEFORE): depth talk: "slippage for liquidity depth"
- call 69 (vpos 35 BEFORE): wall talk: "blocks upside liquidity"
- call 186 (vpos 36 BEFORE): wall talk: "ask-side liquidity at p59–p74"

**Result:** BEFORE 0/120, AFTER 28/120.
- By row (AFTER): 32: 2 · 35: 1 · 36: 1 · 45: 2 · 7: 4 · 11: 1 · 13: 2 · 14: 1 · 18: 2 · 19: 1 · 21: 6 · 24: 5.
- **Live 6/40, paper 22/80.**

---

## 3. EVERY REASON, VERBATIM (all 240)

Per row, BEFORE then AFTER. Call id `k` is the chronological call order; ✱ marks a reason counted as naming the opposing category.

### vpos 32 · live · SHORT · stored R -0.180 · opposing Bullish Imbalance Mitigated, Bullish Liquidity Grab

**BEFORE** — execute 10/10 · skip 0/10

```
k 14 execute 0.78   3/3 TF confluence (1H/15m/5m all SHORT), TREND regime (ADX 23-26, expanding gaps), 1H/15m/5m aligned. 1D bull is headwind but weak (ADX 12.6). 4H neutral with contracting gap; 1H/15m/5m override. Bid walls (p89, p75) are support in downtrend path—soft caution only. High volume ratio (3.61x), combo weight 1.0, MTF score 3/4. Entry justified.
k 27 execute 0.78   3-way LuxAlgo confluence (1H/15m/5m all SHORT) + TREND regime (ADX 23-26, expanding EMA-gaps) + strong MTF alignment (4H/1H/15m/5m agree). 1d BULL is secondary (low ADX 12.6, contracting); 4h NEUTRAL with high ADX supports lower-TF bearish. Bid walls are p89/p75 (thick but not impassable); volume ratio 3.61x, ATR expanding. Soft FLAT guard does NOT apply: ADX >23, ATR% expanding, market_regime=TREND. Combo weight 1.0 baseline. Execute with typical swing risk.
k 59 execute 0.78   3/3 TF confluence, TREND regime, 1h/15m/5m BEAR aligned. 1d bull is distant noise; 4h neutral. Bid walls below are support-path absorption—not a skip trigger.
k 76 execute 0.78   3-tier confluence (1h/15m/5m all SHORT), ADX rising above 23 on 1h/15m, EMA-gaps expanding, market_regime=TREND, volume 3.61x. Mild headwind: 1d BULL (low ADX 12.6) vs 4h NEUTRAL (high ADX 28.4), but 1h/15m/5m dominance + MTF alignment 3/4 support entry. Bid wall at $76.25 (p89, x17.3) is support-path friction; weight against strong confluence & vol. Execute.
k107 execute 0.78   3/3 LuxAlgo tiers agree SHORT. 1h/15m/5m BEAR with expanding EMA-gap & ADX 23-26. Bid walls p89/p75 below entry absorb downward move. 1d BULL vs SHORT is offset by strong 4h/1h/15m/5m bear alignment (3/4 MTF). Volume 3.61x avg, regime TREND, combo 1.0. Execute.
k140 execute 0.78   3/3 LuxAlgo confluence (1H/15m/5m all SHORT), TREND regime confirmed (ADX 23–26, EMA expanding), 4H/1H/15m/5m aligned. 1D bull is minor friction but lower-TF dominates. Bid walls (p89, p75) are path-support, not blockers. Volume 3.61x, combo 1.0. Go.
k155 execute 0.78   3/3 LuxAlgo confluence (1H/15m/5m all SHORT), 1h/15m/5m BEAR trend, ADX 23–26 + expanding EMA-gaps confirm momentum. 4h NEUTRAL + 1d BULL oppose, but 3/4 lower-MTF alignment supports entry. Bid walls (p89, p75) are in the path but volume ratio 3.61x + ATR spike indicate breakout strength. TREND regime + combo 1.0 justify execution despite higher-TF friction.
k184 execute 0.78   3/3 LuxAlgo tiers aligned SHORT. 1h/15m/5m BEAR trend, ADX ~23-26, EMA expanding. 4h neutral but not opposed. Bid walls below entry are support noise, not hard block per WALL RULE. Volume 3.61x avg, regime=TREND, MTF=3. 1d bull is only weak concern; lower-TF confluence strong enough to override. Execute.
k194 execute 0.78   3-way LuxAlgo confluence (1H/15m/5m all SHORT), BEAR trend on 1H/15m/5m, expanding EMA-gaps, ADX 23-26 (trend active), combo 1.0, 3.61x vol. 1d BULL is soft headwind but 4H neutral & 3/4 MTF align SHORT. Bid walls (p89, p75) are support below—SOFT caution per rule, not skip. ATR% low but consistent with low-vol era; market_regime=TREND confirms. Execute.
k218 execute 0.78   3-way LuxAlgo confluence (1H/15m/5m all SHORT), 1H/15m BEAR trend, ADX 23-24 (trend-confirming), Expanding EMA-gaps lower-TF, combo 1.0, high 5m vol ratio 3.61x. 1d BULL is friction but 4h/1h/15m/5m align SHORT (3/4 excl. 1d). Bid walls below entry (p89, p75) are support-path—weaken but don't block given strong momentum and vol. Market regime=TREND with MTF=3. Execute.
```
**AFTER** — execute 10/10 · skip 0/10

```
k 15 execute 0.78   3/3 LuxAlgo tiers agree SHORT; 1h/15m BEAR trend with expanding EMA-gap, ADX 23-25 (trending); 5m vol 3.61x. 1d BULL opposes but weak (ADX 12.6). 4h NEUTRAL. Bid walls at p89/p75 are support but price routinely breaks through; score 4.25 passes. Execute.
k 26 execute 0.78   3/3 tier confluence (1H/15m/5m all SHORT). 1H/15m ADX ~24 + Expanding EMA-gap = genuine trend, not flat. 4H NEUTRAL is soft friction; 1d BULL opposes but is weak (ADX 12.6, contracting). Lower-TF dominance + high volume ratio (3.61x) + combo weight 1.0 overcomes. Bid wall at p89 is support-in-path; ignore per WALL RULE. Execute.
k 58 execute 0.78   3-way confluence (1H/15m/5m all SHORT), 1h ADX 23.4 & expanding EMA-gap confirm trend, 5m vol 3.61x, combo 1.0. 1d BULL opposes but 4h/1h/15m/5m agree SHORT (3/4 alignment). Bid walls (p89, p75) below entry are support-path softness, not skip trigger given strong momentum. Flat-market guard inactive: ADX adequate, expanding gaps, TREND regime. Execute.
k 77 execute 0.78 ✱ 3-tier confluence (1H BEAR, 15m BEAR, 5m BEAR) + expanding EMA gaps + ADX 23-26 confirm trend. 1d BULL is overridden by 4h/1h/15m/5m agreement. Bid walls (p89, p75) are within expected support; volume 3.61x avg and ATR momentum support downside penetration. LIQUIDITY category opposition is minority-zeroed. Execute.
k106 execute 0.78   1H/15m/5m bear confluence solid; 1h ADX 23.4 at trend threshold; EMA gaps expanding; 4.25 score passes. 1d bull opposes but weak (ADX 12.6). Bid walls below (p89, p75) are support in downtrend path—normal absorption. Volume 3.61x avg supports momentum. MTF alignment 3/4 (excl 1d). Entry valid.
k141 execute 0.78 ✱ Multi-TF bear confluence (1h/15m/5m all SHORT-aligned); ADX 23-26 confirms trend; EMA gaps expanding; 3.61x volume; combo 1.0. Daily BULL opposes but weakly (ADX 12.6, contracting). Bid walls (p89, p75) are support below—acceptable in downtrend. LIQUIDITY category shows residual LONG signals (zeroed/minority) but entry tier agreement is solid 3/3. Execute.
k154 execute 0.78   1h/15m/5m confluence (3/3 tier agree), TREND regime (ADX 23.4/24.7, EMA Expanding), 1d opposes but 4h/1h/15m align SHORT. Score 4.25. Bid walls (p89, p75) are support—acceptable in downtrend. Volume 3.61x supports momentum. 1d BULL is soft headwind but lower-TF dominance is strong. Execute.
k185 execute 0.78   3-way confluence (1H/15m/5m all SHORT); 1H/15m/5m trend aligned BEAR; ADX 23-26 confirms trend; combo 1.0; bid wall at p89 is support in downtrend path—acceptable for SHORT. 1d BULL is cross-TF headwind but 4h NEUTRAL + lower TF agreement strong enough to override. Volume 3.61x supports entry. Execute.
k195 execute 0.78   3/3 tier confluence (1h BEAR, 15m BEAR, 5m BEAR trigger), combo 1.0, ADX expanding, regime TREND. 1d BULL is soft headwind but 4h/1h/15m all BEAR & expanding—lower TF alignment strong. Bid walls (p89, p75) below entry are path support; volume 3.61x supports absorption. Momentum brief conflict resolved; score gate 4.25 SHORT. Execute.
k219 execute 0.78   3/3 LuxAlgo tiers align SHORT. 1h/15m/5m BEAR trend (ADX 23-26, EMA expanding). 1d opposes but 4h neutral; 4h ADX 28.4 supports downside. Combo 1.0. Volume 3.61x. Bid walls p89/p75 below are support-in-path (SOFT rule applies); falling price absorbs bids. Market TREND regime, MTF alignment 3/4. Execute.
```

### vpos 35 · live · SHORT · stored R -0.701 · opposing Bullish Liquidity Grab

**BEFORE** — execute 7/10 · skip 3/10

```
k  6 execute 0.72   4H/1H/15m/5m BEAR alignment (ADX rising 15m/5m), EMA expanding across TF. Market regime FLAT but 15m ADX 37.9 is strong. No opposing ask wall; bid walls above entry are ordinary (p83–p90). 1H signal stale (21.3h) but 15m/5m fresh and aligned. Volume 1.64x avg supports trigger. Execute with tight stop.
k 44 execute 0.72   4/4 lower-TF BEAR alignment (1h/15m/5m; 1d neutral). Market regime FLAT but 15m ADX 37.9 (strong). EMA-gap expanding across tiers. 1H signal stale but 15m/5m fresh and aligned. No opposing wall above entry.
k 69 skip    0.72   1H signal STALE (21.3h old, past 6h window); market regime FLAT with low 1h ADX (19.0); thick bid wall (p90, x17.7) at $75.25 directly above entry blocks upside liquidity.
k 73 skip    0.78   1h ADX 19.0 + flat regime + stale 1h signal override strong 15m/5m confluence. Bid wall p90 x17.7 at $75.25 = resistance.
k102 execute 0.72   4H/1H/15m/5m all BEAR with expanding EMA-gaps; 15m/5m confluence fresh & strong (ADX 37.9/28.2). 1H stale but supportive. Market regime nominally FLAT but 15m ADX 37.9 overrides—genuine trend present. No opposing walls above entry. Bid-heavy imbalance. Execute with awareness 1d NEUTRAL and 1H ADX low; risk position sizing.
k124 execute 0.72   4/4 lower-TF alignment (15m/5m fresh, 1h stale but still agrees). 4h BEAR + expanding EMA-gaps across all TFs support SHORT. Market regime is FLAT but 15m ADX 37.9 shows strong localized trend; 5m trigger fresh. No opposing ask walls block downside (thickest ask at p84, not blocking entry). Bid walls present but behind entry—acceptable for SHORT. Volume 1.64x avg. Execute with caution on stale 1h signal age.
k163 skip    0.72   1H signal STALE (21.3h old); market regime FLAT (1h ADX 19.0, low vol); bid wall p90 x17.7 at $75.25 blocks SHORT momentum upward from entry zone.
k189 execute 0.72   4H/1H/15m/5m aligned BEAR; 15m/5m fresh & strong (ADX 37.9/28.2); no opposing wall blocks SHORT; ATR% low but EMA-gap expanding across TFs supports trend continuation despite flat market_regime label.
k196 execute 0.72   4/4 MTF alignment (4h-5m all BEAR). 15m/5m fresh & agree. 1h stale but supportive. Market FLAT but EMA expanding across all TF; 15m ADX 37.9 strong. Bid wall at $75.25 (p90) is thick BUT sits ABOVE entry (short benefits from downside); ask walls thin. Vol ratio 1.64x healthy. Execute with tight stops.
k226 execute 0.72   4H/1H/15m/5m unanimous BEAR; 15m/5m fresh & aligned. 1H stale but supportive. Market FLAT but EMA expanding, 15m ADX strong (37.9). No opposing walls above entry. Execute.
```
**AFTER** — execute 4/10 · skip 6/10

```
k  7 skip    0.72   1H signal STALE (21.3h old); market regime FLAT (1h ADX 19.0, weak); 1d NEUTRAL opposes; ask walls x15.6 @ $75.25 block upside if short reverses.
k 45 skip    0.72   1H signal STALE (21.3h old); market regime FLAT with weak MTF alignment (4/10); 1d NEUTRAL opposes regime. Execute only if confluence exceptionally strong—it is not here.
k 68 skip    0.72   1H signal stale (21.3h); market regime FLAT despite lower-TF bear alignment; 1d NEUTRAL opposes SHORT; bid wall x17.7 at p90 absorbs downside.
k 72 skip    0.72   1H signal STALE (21.3h); market regime FLAT with weak MTF alignment (4/10); 1d NEUTRAL opposes; bid wall x17.7 at $75.25 blocks SHORT momentum.
k103 execute 0.72   4/4 lower-TF trend alignment (1H/15m/5m BEAR), 15m ADX 37.9 (strong), EMA expanding across 1H-5m, no opposing walls at entry; 1H stale but recent. FLAT regime (1h ADX 19) softened by strong 15m/5m momentum and expanding gaps. 1d NEUTRAL does not block. Execute with caution given 1H age and market regime label.
k125 execute 0.72   4/4 MTF alignment (4h-5m all BEAR), 15m/5m fresh signals agree, expanding EMA-gaps across all TFs support bearish regime. 1h ADX 19 is borderline weak but 15m ADX 37.9 is strong; market leans TREND not FLAT despite 1h label. 1d NEUTRAL does not block. Bid walls at $75.25 (p90, x17.7) sit AT mid, not above entry—no hard block. Execute with caution given 1h staleness and borderline volatility.
k162 skip    0.72 ✱ 1H signal STALE (21.3h old, >6h window). Market regime FLAT (ADX 1h 19.0, ATR% low), MTF alignment weak (score 4). Opposing liquidity signal (LONG 2.50pts). Execute only on fresh multi-TF confluence.
k188 skip    0.78   1H signal STALE (21.3h old); market regime FLAT with low 1H ADX (19.0); bid-wall congestion ($75.25 p90 x17.7) blocks SHORT momentum; weak MTF alignment (4/4 only on 4H-5m, 1D neutral). Skip.
k197 execute 0.72   4/4 lower-TF alignment (4h/1h/15m/5m all BEAR); 15m/5m fresh & strong (ADX 37.9/28.2); no opposing walls directly below SHORT entry; bid-heavy imbalance supportive. 1H stale (21.3h) but 15m/5m confluence compensates. Market regime FLAT with low 1h ADX (19.0) is a soft caution, but expanding EMA-gaps across tiers & strong 15m ADX override the flat read. No hard blockers.
k227 execute 0.72   4/4 MTF alignment (4h-5m all BEAR), expanding EMA-gaps, 15m ADX strong (37.9). 1h stale but 15m/5m fresh & coherent. Bid-heavy imbalance. No opposing wall directly below SHORT entry; p42 bid wall at $74.25 is ordinary, not blocking. Market_regime=FLAT & 1h ADX=19 offset by 15m trend strength & multi-TF bear agreement. Execute.
```

### vpos 36 · live · SHORT · stored R -0.757 · opposing Bullish Liquidity Grab

**BEFORE** — execute 10/10 · skip 0/10

```
k 11 execute 0.72   4H/1H/15m/5m BEAR aligned; 15m+5m SHORT confluence fresh & strong. 1H LONG stale (6.8h). Flat regime soft; ATR% low but EMA expanding & ADX 21-25 support trend. No opposing walls block short. Volume ratio weak but acceptable. Execute.
k 28 execute 0.78   4H/1H/15m/5m all BEAR trend (ADX 22.0–24.6, Expanding gaps). Fresh 15m/5m SHORT confluence overrides stale 1H LONG. No thick opposing walls block short. FLAT regime (ADX 21.1/14.7, low ATR%) is offset by strong lower-TF agreement and expanding EMA structure. Proceed.
k 50 execute 0.78   4H/1H/15m/5m all BEAR; fresh 15m/5m SHORT agree. Flat regime but expanding EMA & supportive HTF. Skip stale 1H long.
k 83 execute 0.78   4H/1H/15m/5m all BEAR, strong MTF alignment (4/4 excl 1d). Fresh 15m+5m confluence agrees SHORT. 1H signal stale (6.8h); ignore. Market regime FLAT but EMA expanding & ADX 21.1/24.6 show emerging trend—not compression squeeze. Bid wall at $75.25 (p85) sits ABOVE entry; ask walls above. No opposing wall directly below SHORT. Ask-heavy imbalance supports downside. Execute with standard risk mgmt.
k114 execute 0.72   4H/1H/15m/5m all BEAR-aligned; 15m+5m fresh agreement on SHORT. Stale 1H bullish overridden by lower-TF consensus and higher-TF regime. FLAT regime + low ADX (21.1, 14.7) mitigated by Expanding EMA-gaps and 24.6 ADX on 5m. No opposing walls blocking entry; ask-side walls p59–p74 are above mid, not critical. Volume ratio weak (1.13x) but acceptable. MTF alignment score 4 supports SHORT. Execute with moderate confidence.
k130 execute 0.72   4H/1H/15m/5m all BEAR-aligned; 15m/5m confluence strong & fresh. 1H signal stale/opposed but lower-TF agreement dominates. Market FLAT but EMA expanding, ADX 21-25 on lower TFs supports trend. No opposing walls block SHORT; bid walls at p85/p66 support downside. Volume adequate (1.13x). Execute with managed risk given low absolute volatility & FLAT regime label.
k167 execute 0.78   4H/1H/15m/5m aligned BEAR, 15m+5m fresh SHORT confluence, expanding EMA gaps, stale 1H bullish immaterial. Flat regime soft (ADX 21.1/14.7 borderline, ATR% low) but multi-TF alignment strong. Bid wall at 75.25 (p85, x16.1) is thick but positioned ABOVE entry; does not block SHORT. Execute.
k186 execute 0.72   4H/1H/15m/5m all BEAR-aligned; 15m+5m fresh SHORT agreement; flat regime but expanding EMA-gaps across lower TFs support directional conviction. 1H signal stale (6.8h old), so weight fresh 15m/5m confluence. No opposing walls blocking SHORT entry (bid walls are support, not resistance). Mild ask-side liquidity at p59–p74 is ordinary, not prohibitive. Volume ratio 1.13x adequate. Execute with caution: low absolute volatility (ATR% 0.146% on 15m) and flat regime flag suggest tight stops; MTF alignment 4/4 below 1d is strong enough to override FLAT classification here.
k214 execute 0.76   4H/1H/15m/5m all BEAR-aligned, 15m+5m fresh SHORT signals agree, stale 1H bullish opposes but expired. ATR% low but EMA expanding across MTF; mild FLAT regime offset by strong lower-TF confluence. No opposing walls above entry. Execute.
k237 execute 0.72   4H/1H/15m/5m aligned BEAR, fresh 15m/5m SHORT confluence, EMA expanding. 1H stale bullish ignored. Flat regime OK given strong lower-TF agreement. Bid walls p85/p66 above entry pose minor friction but not blocking. Volume thin but acceptable. Execute.
```
**AFTER** — execute 1/10 · skip 9/10

```
k 10 skip    0.78   1H signal STALE (6.8h); market FLAT (ADX 1h 21.1, 15m 14.7, ATR% low); 1d NEUTRAL opposes regime.
k 29 skip    0.72   1H tier stale (6.8h) opposes SHORT. Market regime FLAT (ADX 21.1/14.7 low, ATR% thin). Bid wall at $75.25 p85×16.1 directly above entry blocks upside relief if SHORT fails. 4H/1H/15m/5m BEAR alignment strong but insufficient to overcome stale opposition + flat regime + blocking wall.
k 51 execute 0.72   4H/1H/5m BEAR alignment strong. 1H stale but 15m/5m fresh & agree SHORT. Flat regime (ADX 21.1, 14.7) but EMA expanding—low-vol trend. No opposing walls block short. Bid walls above entry irrelevant to SHORT. Execute.
k 82 skip    0.72   1H signal STALE (6.8h); market FLAT (ADX 1h 21.1, ATR% low); 1d NEUTRAL opposes regime. Skip.
k115 skip    0.72   1H signal STALE (6.8h old, past 6h window); market regime FLAT (ADX 1h/15m <23, ATR% low, MTF alignment weak=4); 1d NEUTRAL opposes momentum; ask-wall p74 x12.9 at $75.25 blocks SHORT uptick relief.
k131 skip    0.72   1H LONG stale (6.8h old, discounted). 4h/1h/15m/5m all BEAR trend—strong regime agreement for SHORT. BUT: Market regime FLAT (ADX 1h 21.1 near threshold, 15m 14.7 weak; ATR% very low 0.073–0.392%). EMA-gaps expanding but absolute volatility compressed. Bid wall at $75.25 (p85, x16.1) sits directly above mid—strong resistance will absorb SHORT momentum. Imbalance ask-heavy (0.47) reinforces upside bias. Confluence strong (15m/5m agree SHORT), but flat regime + opposing wall structure + stale 1H LONG opposition create execution risk. Skip to await fresh trend confirmation with higher volatility.
k166 skip    0.72   1H signal STALE (6.8h); market FLAT (ADX 21.1/14.7, ATR% 0.392%/0.146%); 1D NEUTRAL opposes regime; bid wall p85×16.1 at $75.25 sits directly above SHORT entry point, absorbs downside liquidity.
k187 skip    0.72 ✱ 1H LONG stale (6.8h old, outside 6h TTL); market_regime FLAT w/ low ADX (1h 21.1, 15m 14.7) & weak MTF alignment (4/5); ask-wall cluster at p59–p74 (×9.6–×12.9) directly above entry blocks SHORT development. 4h/1h/15m BEAR agree, but insufficient to overcome flat regime + opposing liquidity structure.
k215 skip    0.72   1H signal stale (6.8h>6h window); market regime FLAT with low ADX (1h 21.1, 15m 14.7) & compressed volatility (ATR% 0.146-0.392%); thick bid wall at $75.25 (p85, x16.1) directly above SHORT entry absorbs downside; 1d NEUTRAL opposes momentum. Lower TF confluence (15m/5m SHORT) insufficient alone.
k236 skip    0.72   1H tier STALE (6.8h old) opposes SHORT. Market regime FLAT (ADX 1h 21.1, low ATR%), despite 4H/1H/15m/5m BEAR alignment. Ask walls p74/p59 (x12.9, x9.6) block upside escape; bid walls p85 (x16.1) block downside. Thin confluence (15m+5m only, fresh) insufficient for flat regime override.
```

### vpos 45 · live · SHORT · stored R -1.133 · opposing Bullish Imbalance Mitigated, Bullish Liquidity Grab

**BEFORE** — execute 9/10 · skip 1/10

```
k  2 execute 0.72   4H/1H/15m bear alignment + 15m ADX 37.9 (strong) supports SHORT. 1H ADX 20.2 is weak but EMA expanding. Ask wall at 99.75 (p72) above entry is ordinary, not blocking. Volume ratio 0.53x is thin but not disqualifying in trend. 1D neutral is soft headwind. Confluence coherent.
k 42 execute 0.72   4H/1H/15m agree BEAR; 1H ADX 20.2 weak but 15m ADX 37.9 strong; ask wall $99.75 (p72) above entry is ordinary, not blocking; 1.8h-old 1H signal still fresh (31% window); volume ratio soft but confluence solid.
k 54 execute 0.72   Strong 3/4 MTF alignment (4h/1h/15m agree BEAR). 1h ADX 20.2 is weak but 15m ADX 37.9 is solid. Ask wall at $99.75 (p72) is ordinary, not blocking. LuxAlgo confluence 2/2 (1H+5m). 1d neutral is mild headwind but outweighed by lower-TF coherence.
k 85 execute 0.72   4H/1H/15m align SHORT; 15m ADX 37.9 confirms trend; ask wall p72 above entry is ordinary, not blocking.
k112 execute 0.72   3/4 HTF alignment (4h/1h/15m BEAR), 1h ADX weak (20.2) but 15m strong (37.9), 2/2 LuxAlgo tiers agree SHORT. Ask wall at $99.75 (p72, ordinary) poses minimal friction. 1d NEUTRAL is concern but lower TFs cohere. Low volume ratio (0.53x) acceptable given confluence strength. Flat 1h guard overridden by 15m trend + expanding EMA below 1h. Execute.
k143 skip    0.78   1h ADX 20.2 (weak/borderline) + 15m EMA contracting + 5m volume 0.53x + ask wall p72 x12.4 blocks SHORT
k149 execute 0.72   3/4 HTF alignment (4h/1h/15m bearish); 1h ADX weak (20.2) but 15m strong (37.9); ask wall p72 at $99.75 is ordinary, not blocking; 1d neutral is secondary to lower-TF confluence.
k171 execute 0.72   4H/1H/15m align BEAR; 1H ADX 20.2 weak but 15m ADX 37.9 strong; ask wall at $99.75 (p72) above entry is ordinary, not blocking; 5m vol ratio 0.53x is thin but confluence is solid across tiers.
k206 execute 0.72   4H/1H/15m bearish alignment, 15m ADX 37.9 strong, 5m trigger active. Ask wall $99.75 (p72) minor friction only. Skip 1d neutral—lower TFs dominate. Execute.
k228 execute 0.72   3/4 MTF bearish alignment (4h/1h/15m agree). 1h ADX 20.2 weak but 15m ADX 37.9 strong. Ask wall $99.75 (p72) only +0.2% above mid—not blocking. Skip 1d (NEUTRAL, high ADX 46.4 compression). LuxAlgo 1h+5m confluence solid, 31% into 1h window, combo=1.0. Volume 0.53x soft; 1h EMA expanding supports SHORT. Execute with moderate conviction.
```
**AFTER** — execute 0/10 · skip 10/10

```
k  3 skip    0.72   1h ADX 20.2 (weak trend), 15m EMA contracting, 5m vol 0.53x; ask wall $99.75 (p72) blocks SHORT
k 43 skip    0.72 ✱ 1H ADX 20.2 + 15m EMA contracting = weak trend compression. Ask wall $99.75 (p72, x12.4) blocks SHORT immediately above mid. Liquidity opposes.
k 55 skip    0.72   1h ADX 20.2 (weak/ranging threshold); 15m EMA-gap Contracting + ask wall x12.4 at p72 blocks SHORT momentum.
k 84 skip    0.72   1h ADX 20.2 + 15m EMA contracting + ask wall p72 x12.4 at $99.75 (1 tick above entry) blocks SHORT
k113 skip    0.72   1H ADX 20.2 (weak trend), 1D NEUTRAL (regime opposition), ask wall $99.75 (p72) blocks SHORT momentum.
k142 skip    0.72 ✱ 1h ADX 20.2 (weak/ranging threshold); 15m EMA contracting; ask wall x12.4 at p72 blocks upside; liquidity opposes SHORT.
k148 skip    0.72   1h ADX 20.2 + 15m EMA contracting + ask wall p72 x12.4 at $99.75 blocks short momentum.
k170 skip    0.72   1h ADX 20.2 (weak), 15m EMA contracting, 1d NEUTRAL opposes; ask wall x12.4 p72 blocks SHORT
k207 skip    0.72   1h ADX 20.2 (weak), 15m EMA contracting, ask wall $99.75 (p72, x12.4) blocks SHORT; 1d NEUTRAL opposes. Thin confluence.
k229 skip    0.72   1h ADX 20.2 + 15m EMA contracting + 5m volume weak (0.53x) = compression/chop risk. Ask wall $99.75 (p72, x12.4) blocks SHORT move. 1d NEUTRAL opposes. Skip.
```

### vpos 7 · paper · LONG · stored R +2.089 · opposing Bearish Liquidity Grab

**BEFORE** — execute 10/10 · skip 0/10

```
k  5 execute 0.72   Strong 4/4 MTF alignment (4H/1H/15m/5m all BULL). ADX trend confirmation solid (31.2→46.3→49.0). 1d NEUTRAL does not block lower-TF strength. Ask wall at $71.25 is above entry; bid-heavy book supports. Execute.
k 34 execute 0.78   4/4 lower-TF alignment (4h-5m all BULL), strong 15m/5m ADX (46.3/49.0), trend regime confirmed. 1d neutral but not opposing. Ask wall at 71.25 is 0.35% above entry—manageable slippage for liquidity depth.
k 66 execute 0.72   4H/1H/15m/5m aligned BULL, ADX 31-49 (strong trend), 1h EMA expanding. 1d NEUTRAL but lower-TF confluence strong. No opposing wall above entry.
k 80 execute 0.78   4/4 lower-TF alignment (4H/1H/15m/5m all BULL), strong ADX on 15m/5m (46.3/49.0), TREND regime, bid-heavy book. 1d NEUTRAL is acceptable given dominance of 4H+ agreement. Ask walls at $71.25+ are above entry, not blocking.
k105 execute 0.72   Strong 4h/1h/15m/5m BULL alignment, ADX 31.2–49.0 confirms trend, EMA expanding 1h. 1d neutral but non-opposing. Bid-heavy imbalance supports long. Ask wall $71.25 is above entry, no blocking short wall.
k139 execute 0.78   Multi-TF bullish alignment (4H/1H/15m/5m), strong ADX (31.2-49.0), TREND regime. 1d neutral but lower-TF confluence solid. No opposing ask wall blocks entry; bid-heavy order book supportive.
k146 execute 0.78   4/4 lower-TF alignment (4H/1H/15m/5m BULL). 1H ADX 31.2 + 15m ADX 46.3 confirm trend. Ask walls above entry are distant ($71.25+); bid-heavy book supports push. 1d NEUTRAL with contracting gap is mild headwind but does not contradict 4H+ agreement. Volume ratio weak but confluence strength compensates.
k178 execute 0.78   4H/1H/15m/5m BULL aligned, ADX 31-49 (trend), EMA expanding 1h/4h. Ask wall $71.25 above entry—manageable. Execute.
k210 execute 0.72   4H/1H/15m/5m BULL aligned, ADX strong (31.2-49.0), EMA expanding 1h/4h. 1d NEUTRAL not opposition. Bid-heavy book +0.52. Ask wall $71.25 is ×20.3 but >1% away; acceptable risk. Volume thin (0.01x) is concern but confluence robust.
k223 execute 0.78   Strong multi-TF LONG confluence: 4H/1H/15m/5m all BULL, ADX rising (31.2→46.3→49.0), MTF alignment 4/4. 1d NEUTRAL non-blocking. Bid-heavy book (0.52 imbalance). No opposing wall directly above entry—ask walls at +0.28/$71.25 allow development room. Soft low volume/flat 15m EMA acceptable given trend regime clarity and expanding 1h/4h structure.
```
**AFTER** — execute 0/10 · skip 10/10

```
k  4 skip    0.78   Massive ask wall (×20.3) at $71.25 directly above entry blocks upside momentum development.
k 35 skip    0.78   1d NEUTRAL + ADX 43.8 (contraction phase) opposes. Massive ask wall ×20.3 at $71.25 blocks upside. Volume ratio 0.01x is anemic.
k 67 skip    0.78   1d NEUTRAL + ADX 43.8 (extreme) contradicts LONG. 15m EMA-gap Flat. Momentum zeroed (conflicting HyperWave signals within 90m window). Skip.
k 81 skip    0.78 ✱ 1d NEUTRAL w/ contracting EMA opposes; momentum zeroed (HyperWave conflict); liquidity SHORT active. Risk/reward unfavorable.
k104 skip    0.82   1d NEUTRAL + contracting EMA conflicts with LONG; massive ask wall ×20.3 at $71.25 blocks upside momentum.
k138 skip    0.78   Momentum category zeroed (conflicting HyperWave signals within 90m window); massive ask wall at $71.25 (×20.3) directly above entry blocks development.
k147 skip    0.72   Momentum category zeroed (conflicting HyperWave signals); 1d NEUTRAL opposes; ask wall ×20.3 at $71.25 blocks upside.
k179 skip    0.78 ✱ Momentum category zeroed (HyperWave conflict); Liquidity opposes LONG. 1d NEUTRAL with contracting EMA-gap weakens regime.
k211 skip    0.78 ✱ 1d NEUTRAL + EMA contracting; 15m/5m EMA flat despite high ADX. Momentum zeroed (HyperWave conflict). Liquidity opposes. Skip.
k222 skip    0.72 ✱ Momentum zeroed; liquidity opposes LONG. 1d neutral/contracting. Massive ask wall $71.25×20.3 blocks upside.
```

### vpos 11 · paper · SHORT · stored R +1.133 · opposing Bullish Imbalance Mitigated

**BEFORE** — execute 10/10 · skip 0/10

```
k 16 execute 0.78   SHORT aligned: 15m/5m bearish signals + 1h/15m/5m BEAR trend (3/4 MTF). 15m ADX 42.2 strong. Ask wall at $71.75 is opposing but not blocking; bid-heavy book supports downside. Execute.
k 39 execute 0.78   SHORT confluence strong: 15m HyperWave + 5m I-BOS aligned; 15m/5m ADX >42/50 (trend); 4H/1H/15m all BEAR (3/4 MTF); bid-heavy book; ask wall at $71.75 is 0.45% above entry, manageable in strong downtrend.
k 70 execute 0.78   SHORT aligned: 15m/5m BEAR + strong confluence. 1h ADX 17.2 (weak) but 15m ADX 42.2 dominates. Ask wall at $71.75 (×15.0) is above entry; no opposing hard wall below SHORT. Bid-heavy book supports downside momentum.
k 90 execute 0.78   Strong multi-TF bearish confluence (15m HyperWave + 5m I-BOS). 15m/5m ADX elevated (42.2/50.4), BEAR regime 4H/1H/15m/5m aligned. 1h ADX 17.2 < 22 = hard wall veto applies to asks, but SHORT entry has no opposing wall below—ask walls above are irrelevant. Bid-heavy orderbook. Minor headwind: 1d NEUTRAL, 4h weak (ADX 18.6), but lower-TF signal strength overrides.
k 98 execute 0.78   SHORT aligned: 15m/5m BEAR + expanding EMA-gap, 15m ADX 42.2 (strong trend), ask wall $71.75 is not blocking entry. 1d/4h NEUTRAL non-oppositional. Execute.
k127 execute 0.72   SHORT confluence: 15m HyperWave + 5m Bearish I-BOS aligned. 15m ADX 42.2 (strong trend), 5m ADX 50.4 (very strong). 4h/1h/15m/5m all BEAR (3/4 MTF). Massive ask wall at $71.75 (×15.0) is ABOVE entry, not blocking SHORT. Bid-heavy book supports downside. 1h ADX 17.2 is weak but lower TFs dominate here with exceptional strength.
k156 execute 0.72   SHORT confluence strong: 15m HyperWave + 5m I-BOS aligned. 15m ADX 42.2 (strong trend), 5m ADX 50.4 (very strong). 4h/1h/15m/5m all BEAR (3/4 MTF). Ask wall at $71.75 (×15.0) is above entry, not blocking SHORT. Bid-heavy book supports downside. 1h ADX weak (17.2) but offset by exceptional lower-TF confluence and clear bearish regime. Execute.
k191 execute 0.78   Short-aligned regime: 1h/15m/5m BEAR with strong ADX (42.2/50.4), 3/4 MTF agree. Ask wall at $71.75 is directionally opposing but not blocking (×15.0, manageable). 1h ADX 17.2 is weak, but 15m/5m ADX are very strong trend. EMA gaps expanding across TFs. Combo weight 1.0 neutral. Volume ratio low (0.00x) is concern but LuxAlgo confluence (HyperWave + I-BOS) is coherent SHORT signal. Proceed with execution.
k209 execute 0.78   SHORT confluence strong: 15m/5m both bearish, 1h/15m/5m BEAR regime with high ADX (42.2/50.4). Ask wall at $71.75 is opposing but not hard-veto (SHORT entry, not exception case). Bid-heavy book supports downside. 1d NEUTRAL non-conflicting. Execute.
k216 execute 0.78   SHORT aligned across 15m/5m/1h BEAR trends; 15m ADX 42.2 strong; ask wall above entry is soft (1h ADX<22, SHORT exempt); bid-heavy book supports downside.
```
**AFTER** — execute 0/10 · skip 10/10

```
k 17 skip    0.92   1h ADX 17.2 (weak), 4h NEUTRAL regime opposes SHORT. Massive bid wall at $71.25 (×19.6) below entry absorbs downside. HARD VETO.
k 38 skip    0.82   1h ADX 17.2 (weak trend) + 4h NEUTRAL (opposes SHORT). Massive bid wall $71.25 (×19.6) below entry absorbs downside. Skip.
k 71 skip    0.78   1h ADX 17.2 (weak trend); 4h NEUTRAL opposes SHORT; massive bid wall at $71.25 (×19.6) blocks downside liquidity.
k 91 skip    0.92   SHORT into bid-heavy book w/ massive $71.25 bid wall (×19.6) below entry absorbs downside momentum. 1h ADX 17.2 (weak trend) conflicts with strong 15m/5m bearish structure; 1d/4h NEUTRAL regime opposes. Skip.
k 99 skip    0.78   1h ADX 17.2 (weak trend) + 4h NEUTRAL ADX 18.6 undermine confluence. Massive ask wall $71.75 (×15.0) blocks short momentum. Skip.
k126 skip    0.82   1h ADX 17.2 (weak trend), 4h NEUTRAL oppose SHORT. Massive bid walls ($71.25 ×19.6) below entry absorb downside. Skip.
k157 skip    0.78   1h ADX 17.2 (weak trend); 4h NEUTRAL opposes SHORT; massive bid wall $71.25 (×19.6) below entry absorbs downside.
k190 skip    0.82 ✱ 1h ADX 17.2 (weak trend), 4h NEUTRAL, massive bid wall $71.25 (×19.6) below entry supports SHORT but contradicts momentum. MOMENTUM category zeroed; execution fresh but liquidity opposes. Flat-market guard applies: weak 1h ADX + low ATR% on 1h despite TREND label + 4h weakness = high chop risk despite lower-TF confluence.
k208 skip    0.82   1h ADX 17.2 (weak trend) + 4h NEUTRAL (17.6 ADX) oppose SHORT. Massive bid wall $71.25 (×19.6) below entry blocks downside liquidity. 5m volume 0.00x avg signals weak participation.
k217 skip    0.78   1h ADX 17.2 (weak trend) + 4h NEUTRAL regime conflict SHORT. Massive bid wall at $71.25 (×19.6) below entry acts as support floor, blocking downside development. Skip.
```

### vpos 13 · paper · SHORT · stored R +1.337 · opposing Bullish Imbalance Mitigated, Bullish Liquidity Grab

**BEFORE** — execute 10/10 · skip 0/10

```
k 23 execute 0.78   1d/4h/1h BEAR regime aligned with SHORT confluence. 15m/5m expanding EMA, 5m ADX 36.4 strong. Bid walls below support downside; ask walls above entry do not block SHORT. Execute.
k 31 execute 0.78   1d-4h BEAR + 1h BEAR ADX 24.7 align with SHORT. 15m/5m BEAR confirm. MTF 4/4. Massive bid walls below support liquidity; ask walls above are resistive but not blocking. Volume ratio weak (0.05x) but ADX >22 on 1h/15m indicates directional strength despite flat EMA-gaps. Market regime FLAT but multi-TF trend alignment is exceptional. Execute.
k 56 execute 0.78   Multi-TF BEAR alignment (1d/4h/1h/15m/5m all BEAR, MTF 4/4). 1h ADX 24.7 (>22) supports trend. 15m expanding EMA confirms momentum. No opposing wall—massive bid walls SUPPORT short below mid. Execute SHORT.
k 94 execute 0.78   Multi-TF BEAR alignment (1d/4h/1h/15m/5m all BEAR). SHORT direction matches. ADX 24.7–36.4 confirms trend strength. Ask walls above entry are secondary to downtrend momentum.
k101 execute 0.78   BEAR regime 1d/4h/1h align with SHORT. 15m/5m BEAR + HyperWave Down + Bearish OB confluence strong. ADX 24.7/24.1 above 23 confirms trend. Ask walls above entry are not hard veto—SHORT is trend-aligned. Modest ATR% and flat 1h EMA offset by multi-TF agreement and 5m ADX 36.4 spike. MTF 4/4 alignment on 4H-5m supports execution.
k137 execute 0.78   Multi-TF BEAR alignment (1d/4h/1h/15m/5m all BEAR, ADX 24.7-36.4), LuxAlgo confluence strong (15m HyperWave DOWN + 5m Bearish OB), no hard wall veto below price. Ask walls above are typical resistance, not a veto for SHORT. MTF alignment 4/4 on lower TFs, combo weight 1.0. Execute.
k158 execute 0.78   1d/4h/1h BEAR + 15m/5m BEAR aligned. 1h ADX 24.7 >22, trend-strong. Ask wall veto lifted for trend LONG, but this is SHORT—veto stays hard. No opposing wall below SHORT entry. 15m ADX 24.1 supports trend. Volume ratio weak (0.05x) is soft concern but confluence is multi-TF solid. Execute SHORT.
k182 execute 0.78   Multi-TF BEAR alignment (1d/4h/1h/15m/5m all BEAR, 4/4 MTF=4); 1h ADX 24.7>22 supports trend. 15m/5m confluence strong (HyperWave Down + Bearish OB). Opposing ask wall (×16.8 at $68.75) is soft-vetoed by trend strength & ADX. Flat regime compensated by clear directional agreement across all TFs. Execute SHORT.
k199 execute 0.78   BEAR alignment 4/4 (4h/1h/15m/5m), ADX 24.7/24.1 (trend-eligible), 15m Expanding EMA supports downside. Volume ratio low but confluence strong. Ask walls above entry present no hard veto (SHORT exempt). Execute.
k233 execute 0.78   Multi-TF BEAR alignment (1d/4h/1h/15m/5m all BEAR, 4/4 MTF=4). 1h ADX 24.7>22 supports trend. LuxAlgo SHORT confluence strong. Ask wall at $68.75 (×16.8) is above entry, not blocking downside. Bid walls support SHORT. Flat market_regime is soft constraint, overridden by ADX and alignment.
```
**AFTER** — execute 1/10 · skip 9/10

```
k 22 skip    0.78   BEAR regime across all TFs supports SHORT, but massive ask wall (×16.8 at $68.75) directly above entry blocks momentum. Volume ratio 0.05x avg too weak to break it.
k 30 skip    0.78   BEAR regime 1d/4h/1h opposes SHORT only if ask-wall blocks. Massive ask wall ×16.8 at $68.75 (entry level) vetos SHORT entry per hard rule.
k 57 skip    0.78   Massive ask wall (×16.8) at $68.75 directly above entry blocks SHORT. BEAR regime supportive but wall veto is hard.
k 95 skip    0.82   BEAR regime across all TFs + massive ask wall at $68.75 (×16.8) blocks SHORT. Flat 1h EMA + weak momentum score (1.75) insufficient.
k100 skip    0.78   FLAT market (1h ADX 24.7 borderline, 1h EMA-gap 0.281% Flat, regime FLAT, MTF 4/10). Weak confluence (1.75 MOMENTUM only; EXECUTION zeroed by conflicting signals). Massive ask wall (×16.8 at $68.75) sits at mid—no clear short breakout liquidity. Volume ratio 0.05x avg is critically low. Skip.
k136 execute 0.72   Multi-TF BEAR alignment (1d/4h/1h all BEAR, ADX 24-27) supports SHORT. 15m/5m confluence bearish. Ask wall at $68.75 (×16.8) sits above mid but not directly blocking downside. Flat 1h EMA-gap and FLAT regime are soft headwinds, but 5m ADX 36.4 + expanding gap + 4/4 lower-TF alignment override. Volume ratio low; momentum signal age acceptable. Execute.
k159 skip    0.78   Massive ask wall ×16.8 at $68.75 (entry price) blocks SHORT. Hard veto applies.
k183 skip    0.78 ✱ BEAR 1h/4h/1d regime + flat EMA compression + massive ask wall at $68.75 (×16.8) blocks SHORT. Low confluence score (1.75 MOMENTUM only; EXECUTION zeroed by LONG/SHORT tie; LIQUIDITY opposes). ADX >22 but EMA gaps flat across 1d-1h, no expansion until 5m. Ask wall is hard veto for SHORT entry—no exception applies. Skip.
k198 skip    0.78   Massive ask wall (×16.8) at $68.75 directly above entry blocks SHORT. HARD veto.
k232 skip    0.78 ✱ Massive ask wall (×16.8) at $68.75 blocks SHORT. BEAR regime supports SHORT, but execution setup is weak: EXECUTION category zeroed (conflicting OB signals), volume ratio 0.05x avg critically low, market regime FLAT with soft MTF alignment (4/5). Liquidity opposition unresolved.
```

### vpos 14 · paper · SHORT · stored R -1.032 · opposing Bullish Imbalance Mitigated

**BEFORE** — execute 10/10 · skip 0/10

```
k 18 execute 0.72   Multi-TF BEAR alignment (1d/1h/15m/5m all BEAR, 3/4 MTF). 15m ADX 33.1 strong. 5m trigger SHORT on OB mitigation. Expanding EMA-gaps confirm trend. Ask wall at 64.75 (×6.3) is manageable; primary resistance higher at 65.25. No hard veto applies.
k 46 execute 0.78   SHORT aligned: 1d/1h/15m/5m all BEAR; 15m ADX 33.1 (strong); EMA gaps expanding across TFs. No hard wall block below entry (bid walls support downside). High-quality confluence.
k 65 execute 0.76   Strong multi-TF SHORT confluence: 1d/1h/15m/5m all BEAR with rising ADX (15m 33.1, 5m 38.9). EMA gaps expanding across all TFs. 15m ADX 33.1 >> 22 threshold. Opposing ask walls ($65.25 ×15.2, $65.75 ×4.4) are ABOVE entry, not blocking SHORT. Bid-heavy order book (+0.51) supports downward pressure. Only minor drag: 1h ADX 21.1 (marginal), volume ratio 0.13x (weak), but lower-TF trend strength overrides. TREND regime confirmed.
k 87 execute 0.78   Strong multi-TF SHORT confluence (1d/1h/15m/5m all BEAR). 15m ADX 33.1 confirms trend. Bid-heavy book supports downside; no ask wall directly below entry (nearest $65.25). Proceed.
k111 execute 0.78   Multi-TF BEAR alignment (1d/1h/15m/5m all BEAR). 15m ADX 33.1 strong; EMA gaps expanding across TFs. 5m trigger SHORT confirmed by regime. No hard wall veto: ask walls sit above entry, not below. Supportive.
k132 execute 0.78   Multi-TF BEAR alignment (1d/1h/15m/5m all BEAR); 15m ADX 33.1 confirms trend strength. Massive bid wall at $64.75 sits BELOW entry, supporting SHORT. Expanding EMA-gaps across all TFs validate momentum. Low 5m volume ratio is soft concern but offset by strong regime coherence and LuxAlgo confluence weight 1.0.
k165 execute 0.78   Multi-TF BEAR alignment (1d/1h/15m/5m all BEAR); 15m ADX 33.1 strong; SHORT entry into expanding EMA gaps and trend regime. No hard wall veto: ask walls above entry, not below SHORT. Execute.
k175 execute 0.78   BEAR regime 1d/1h/15m/5m aligned; SHORT trigger valid. Ask wall at $64.75 (×6.3) is in direction of travel, not opposing. Bid-heavy book supports downside.
k212 execute 0.78   SHORT aligned: 1d/1h/15m/5m all BEAR, 15m/5m ADX strong (33.1/38.9). EMA gaps expanding across all TFs. Massive bid wall at $64.75 (×19.2) sits BELOW entry, supporting downside. No opposing ask wall veto applies (ask walls are above). MTF trend coherent, market in TREND regime. Vol ratio low but confluence overcomes.
k239 execute 0.78   Multi-TF BEAR alignment (1d/1h/15m/5m); 15m ADX 33.1 strong; EMA expanding; SHORT into bid-heavy book.
```
**AFTER** — execute 10/10 · skip 0/10

```
k 19 execute 0.72   1d/4h/1h/15m/5m all BEAR; 15m ADX 33.1 strong trend; 5m trigger fresh; bid walls support SHORT
k 47 execute 0.72   Multi-TF BEAR alignment (1d/1h/15m/5m), strong 15m ADX 33.1, expanding EMA-gaps, TREND regime. 1h ADX 21.1 is borderline but supported by lower TF strength. Massive bid wall at $64.75 sits at mid but does NOT block SHORT entry (opposing ask walls are support, not resistance). Score gate 3.75 SHORT points vs 0 LONG. Execute.
k 64 execute 0.72   SHORT aligned: 1d/1h/15m/5m all BEAR, 15m ADX 33.1 (strong), EMA expanding. No hard wall veto.
k 86 execute 0.72   Multi-TF BEAR alignment (1d/1h/15m/5m) + expanding EMA + 15m ADX 33.1 strong. 1h ADX 21.1 marginal but trend clear. Bid-wall at $64.75 (×19.2) sits BELOW mid, not blocking SHORT. Ask walls above do not oppose SHORT. Volume ratio low (0.13x) is soft concern but TREND regime + strong confluence overrides. Execute.
k110 execute 0.78   Multi-TF BEAR alignment (1d/1h/15m/5m all BEAR), strong 15m ADX 33.1, expanding EMA-gaps. 5m SHORT trigger fresh. Massive bid wall at $64.75 is support below entry, not opposing. Execute.
k133 execute 0.78   Multi-TF BEAR regime (1d/1h/15m/5m aligned), 15m ADX 33.1 strong, 5m trigger fresh. Bid-wall heavy at $64.75 (not blocking SHORT below mid). Execute.
k164 execute 0.78   1d/4h/1h/15m/5m all BEAR; 15m ADX 33.1 strong; 5m OB mitigated trigger fresh; bid wall at $64.75 absorbs downside momentum—supportive, not blocking SHORT.
k174 execute 0.72   1d/4h/1h/15m/5m all BEAR-aligned; 15m ADX 33.1 + 5m ADX 38.9 = strong trend. Massive bid wall at $64.75 (×19.2) sits BELOW entry, not opposing SHORT. No hard veto triggered.
k213 execute 0.72 ✱ Multi-TF BEAR regime (1d/1h/15m/5m all BEAR, ADX rising). SHORT aligns with trend. 1h ADX 21.1 is at threshold; 15m/5m ADX strong (33.1/38.9). EMA gaps expanding across TFs supports directional move. Massive bid wall at $64.75 (×19.2) is BELOW entry, not opposing. Ask walls above entry are soft resistance. Volume ratio low (0.13x) is minor concern but confluence weight 1.0 and score gate 3.75 are solid. Liquidity LONG opposition is weak (zeroed). Trend-driven entry with acceptable risk/reward setup.
k238 execute 0.78   Multi-TF BEAR alignment (1d/1h/15m/5m), strong 15m ADX 33.1, expanding EMA-gaps support SHORT. 1h ADX 21.1 borderline but 15m confluence strong. Bid-heavy book mitigates ask-wall concern. Execute.
```

### vpos 18 · paper · LONG · stored R -1.074 · opposing Bearish Liquidity Grab, Broken U.

**BEFORE** — execute 10/10 · skip 0/10

```
k 13 execute 0.78   1h/15m/5m BULL aligned, ADX strong (27.5/41.3/46.6), combo 1.0. 1d NEUTRAL is soft headwind but 4h ADX 28.9 supports. Overhead ask wall is trend-typical friction, not conviction blocker.
k 40 execute 0.78   1h/15m/5m bull confluence + rising ADX (27.5→41.3→46.6). 1h EMA expanding, market_regime TREND. 1d/4h neutral but 4h ADX 28.9 supports. Overhead ask wall soft caution only—trending price absorbs liquidity. Volume ratio 0.72x is mild drag. MTF alignment 3/4 solid.
k 48 execute 0.78   1h/15m/5m BULL confluence, ADX 27.5→41.3→46.6 rising, 1h EMA expanding. 4h neutral but 1h dominates. Ask wall $77.75 is soft overhead in strong trend context; volume ratio 0.72x is mild concern but combo weight 1.0 and MTF 3/4 alignment support entry. ATR% compressed 5m but market regime=TREND confirms validity.
k 74 execute 0.78   Strong lower-TF confluence (15m HyperWave + 5m OB, combo 1.0). 1h/15m BULL with high ADX (27.5/41.3), expanding 1h EMA-gap. 4h neutral with strong ADX (28.9) provides support. Massive ask wall ($77.75) is normal friction in trending market; high lower-TF ADX suggests absorption. 1d neutral is mild drag but 1h/15m dominance + MTF alignment (3/4) justify entry. Volume ratio 0.72x is softer but acceptable given trend strength.
k119 execute 0.72   1h/15m/5m aligned BULL, ADX strong (27.5/41.3/46.6), 1h EMA expanding. 4h neutral but 1h dominates. Overhead ask wall soft caution in trending context; volume ratio weak (0.72x) slightly offsets. MTF alignment 3/4 supports.
k122 execute 0.78   1h/15m/5m bull confluence with rising ADX (27.5→41.3→46.6), expanding 1h EMA-gap, TREND regime. 4h neutral but 1h strength dominates. Overhead ask wall ($77.75×15.0) is normal friction in trending market; strong lower-TF momentum should absorb. Volume ratio 0.72x is soft but combo weight 1.0 and MTF 3/4 alignment offset. Execute with awareness of ask resistance.
k144 execute 0.78   1h BULL + ADX 27.5 (strong trend), 15m/5m BULL confluent, 4h ADX 28.9 supports. Ask wall overhead is soft caution in trending market; volume ratio weak but combo=1.0 and MTF alignment 3/4 compelling. Execute.
k168 execute 0.78   1h/15m/5m bull confluence + ADX26-47 trend strength + MTF 3/4 alignment override neutral 1d/4h. Ask wall is overhead resistance in strengthening trend; volume ratio weak but combo=1.0. Execute.
k201 execute 0.78   Strong lower-TF confluence (15m HyperWave + 5m OB), 1h/15m/5m BULL, high ADX (27.5–46.6), expanding 1h EMA-gap, TREND regime. 1d/4h neutral but not opposing. Massive ask wall ($77.75) is soft caution in confirmed uptrend; ADX/momentum should absorb. Volume ratio weak (0.72x) is only minor drag against strong signal stack.
k224 execute 0.78   1h/15m/5m BULL confluence + rising ADX (27.5→41.3→46.6) + Expanding 1h EMA. 4h NEUTRAL but lower-TF momentum strong. Overhead ask wall is soft caution in trending context; volume ratio (0.72x) is marginal but ADX strength overrides. MTF 3/4 alignment supportive. Execute.
```
**AFTER** — execute 10/10 · skip 0/10

```
k 12 execute 0.78   1h/15m/5m BULL confluence, ADX rising (27.5→41.3→46.6), 1h EMA expanding. 4h neutral but not hostile. Score 6.25 LONG vs 2.5 SHORT (zeroed). Ask wall $77.75 is soft caution in confirmed uptrend—ATR% and ADX support breakup. Volume 0.72x is mild drag but not disqualifying. Execute.
k 41 execute 0.78 ✱ 1h/15m/5m bull confluence, ADX 27.5/41.3/46.6 strong trend, 1h EMA expanding. 1d/4h neutral but 4h ADX 28.9 supports. Liquidity SHORT signal minor. Ask wall overhead is soft caution in trending context—price breaking through is routine. Volume 0.72x and 5m ATR low are modest drags, but combo 1.0 + multi-TF alignment + strong momentum override. Execute with awareness of consolidation risk.
k 49 execute 0.78   1h/15m bull trend (ADX 27.5/41.3), expanding 1h EMA, LONG confluence 6.25pts. 1d/4h neutral but lower TF strongly aligned. Bid walls support, ask wall is trend-path friction only.
k 75 execute 0.78 ✱ Strong 3-TF confluence (15m HyperWave + 5m OB) + 1h/15m bull trend (ADX 27.5/41.3, EMA expanding). 1d/4h neutral, but 4h ADX 28.9 supports. Overhead ask wall ($77.75×15, $78.25×10.2) is soft caution in trend context. Volume ratio 0.72x and 5m ATR% 0.315% are modest but acceptable given expanding EMA-gap and high lower-TF ADX. MTF alignment 3/4 (4h+). Liquidity signal minority. Execute with trend confirmation.
k118 execute 0.78   1h/15m/5m BULL confluence, ADX 27.5/41.3/46.6 (strong trend), EMA expanding 1h. 1d/4h neutral but lower-TF dominance clear. Ask wall $77.75 overhead but trending ADX absorbs liquidity. Volume ratio weak (0.72x) is soft caution, not skip trigger. Combo 1.0 neutral. Execute with tight stop.
k123 execute 0.78   BULL 1h/15m/5m aligned, ADX 27.5–46.6 (strong trend), EMA expanding 1h, combo 1.0. 1d/4h neutral but lower TF dominates. Ask walls overhead but trending market absorbs. Volume ratio soft; execution signal fresh.
k145 execute 0.78   Strong multi-TF confluence (1h/15m/5m BULL aligned, ADX 27.5→41.3→46.6 rising). 1d NEUTRAL is soft headwind but 4h ADX 28.9 supports. Combo 1.0 is neutral. Ask wall $77.75 is overhead but trending ADX absorption typical. Volume ratio 0.72x and 5m ATR% low are minor cautions in low-vol era; market_regime=TREND + MTF alignment 3/4 override. Execute.
k169 execute 0.78   1h/15m/5m LONG confluence + strong ADX (27.5/41.3/46.6), TREND regime, 1.0 combo weight. 4h neutral but 1h expanding EMA & rising ADX support. Ask walls overhead (×15, ×10.2) are soft resistance in trending market; volume 0.72x mild but not disqualifying. 5m EMA contracting is minor concern but offset by lower-TF strength & execution trigger freshness (0 min). LONG score 6.25 solid. Execute.
k200 execute 0.78   1h/15m/5m LONG confluence strong; 1h ADX 27.5 expanding, 4h ADX 28.9 supportive. 1d neutral is soft headwind but lower-TF momentum dominates. Overhead ask wall ($77.75×15, $78.25×10.2) is secondary to trending ADX and multi-TF bull alignment. Volume ratio 0.72x and 5m ATR compression are minor concerns; score gate 6.25 LONG points solid. Execute with trailing stop discipline.
k225 execute 0.78   1h/15m/5m bull confluence, strong ADX (27.5→41.3→46.6), 1h EMA expanding. 4h neutral overhead. Ask walls are soft friction in confirmed uptrend; volume ratio weak but combo weight 1.0 & score 6.25 support. MTF alignment 3/4. Execute.
```

### vpos 19 · paper · SHORT · stored R +0.463 · opposing Broken D., Bullish Liquidity Grab

**BEFORE** — execute 10/10 · skip 0/10

```
k 20 execute 0.78   3TF SHORT confluence + 1h/15m/5m BEAR trend alignment. 1h ADX 22.2 = weak but expanding EMA-gap confirms trend initiation. Massive bid walls below are support absorption risk, not entry block. 4h/1d NEUTRAL is headwind but 5m ADX 20.1 + 1.74x volume + 1.0 combo weight mitigates. Execute with tight stop-loss above recent swing.
k 32 execute 0.78   3-TF confluence SHORT in confirmed 1h/15m/5m bear; 1h ADX 22.2 + expanding EMA justify entry despite 1d/4h neutral. Bid walls below are soft caution in downtrend—volume 1.74x and combo weight 1.0 are supportive. MTF alignment 3/4 strong.
k 52 execute 0.72   3TF SHORT confluence (15m HyperWave + 5m I-CHOCH) confirmed by 1h/15m BEAR trends, expanding EMA-gaps, ADX 22-26, TREND regime, MTF 3/4 alignment. Bid walls below are soft caution in downtrend path; 1.74x volume ratio supports break. 1d/4h neutral does not contradict. Execute with normal position sizing.
k 88 execute 0.78   Multi-TF confluence (15m HyperWave + 5m I-CHOCH+) aligned SHORT in confirmed 1h/15m/5m downtrend. 1h ADX 22.2 above range floor, EMA-gaps expanding on 1h/15m/5m. Combo weight 1.0 (baseline winner). Market regime TREND with strong 3/4 MTF alignment (4h-5m). Bid walls below entry are support in path of downmove—typical in shorts. 1d/4h neutral does not contradict; lower-TF confluence is coherent. Execute.
k116 execute 0.78   1h/15m/5m bear confluence strong; 4h neutral but 1h ADX expanding trend confirmed. Bid walls are support below, not a blocker for short. Volume 1.74x avg supports momentum. MTF alignment 3/4 backing the move.
k121 execute 0.78   3-TF bearish confluence (15m HyperWave, 5m I-CHOCH+) with 1h/15m/5m BEAR trend alignment, expanding EMA-gaps, combo weight 1.0, strong 5m volume (1.74x). Bid walls below are support in downtrend path—acceptable risk. 1d NEUTRAL is soft headwind but 4h NEUTRAL + 1h BEAR + lower-TF momentum override. Execute.
k150 execute 0.78   3-TF SHORT confluence on BEAR 1h/15m/5m; 1h/15m ADX expanding; TREND regime. 1d NEUTRAL is soft headwind but 4h/1h/15m strong alignment overrides. Massive bid walls below are expected support in downtrend path—not a skip trigger. Volume 1.74x avg, combo 1.0. Execute.
k181 execute 0.78   1h/15m/5m bear confluence, ADX 22-26 (trend), MTF alignment 3/4. Bid walls are support in downtrend path; vol 1.74x avg, combo 1.0. 1d neutral doesn't block.
k193 execute 0.72   3-TF SHORT confluence (15m HyperWave + 5m I-CHOCH) in confirmed downtrend (1h/15m/5m BEAR). 1h ADX 22.2 + 15m ADX 25.6 = trend strength. EMA-gap expanding on 1h/15m supports move. Combo 1.0 is neutral-positive. Bid walls below are support absorption risk, not entry blocker in downtrend. 1d/4h NEUTRAL is soft headwind but lower-TF alignment (3/4) dominates. Volume 1.74x avg is adequate. Execute.
k231 execute 0.78   3-TF SHORT confluence, 1h/15m/5m BEAR aligned, ADX 22-26 (trend active), combo 1.0, vol 1.74x. Bid walls soft; price absorbs support in downtrends. Execute.
```
**AFTER** — execute 10/10 · skip 0/10

```
k 21 execute 0.72   3/4 HTF bear trend (1h/15m/5m aligned), expanding EMA-gaps, combo 1.0, strong confluence. Bid walls are support resting in downtrend path—acceptable. 1d neutral is minor headwind but lower-TF dominance + momentum + 1.74x vol confirm entry.
k 33 execute 0.72   3/4 HTF agree BEAR (4h NEUTRAL); 1h/15m expanding trends; combo 1.0; volume 1.74x; 4.25 score gate.
k 53 execute 0.72   1h/15m/5m bear alignment + combo 1.0 + expanding EMA gaps on 1h/15m + trend regime. 1d/4h neutral but lower TFs strong. Bid walls are support in downtrend path—not a skip trigger. Volume ratio 1.74x adequate. Proceed.
k 89 execute 0.72   3/4 HTF bears (1h/15m/5m), expanding EMA-gaps, combo 1.0, strong confluence. Bid walls soft caution only.
k117 execute 0.78   3TF confluence (15m HyperWave + 5m I-CHOCH+) aligns with 1h/15m/5m BEAR. 1h ADX 22.2 + expanding EMA confirms trend. Bid walls below are support—tolerable in downtrend. Combo 1.0 baseline solid. 1d/4h neutral but not opposed. Volume 1.74x avg healthy. Execute.
k120 execute 0.76   3-TF confluence (15m HyperWave Down + 5m I-CHOCH+) with BEAR 1h/15m/5m. Combo 1.0, ADX rising (22→25→20), EMA expanding. Bid walls are soft support in downtrend path—volume 1.74x and momentum score 4.25 override. 1d/4h neutral but 3/4 lower-TF alignment strong. Execute.
k151 execute 0.72   1h/15m/5m bearish confluence confirmed. 1h/15m ADX expanding, regime=TREND, MTF alignment 3/4. Bid walls are support below entry (soft caution only). 1d/4h neutral does not oppose SHORT. Execute.
k180 execute 0.72   3-TF confluence (15m HyperWave + 5m I-CHOCH+) aligns with 1h/15m/5m bear trend. Combo 1.0 neutral. 1d/4h neutral but not opposing. Bid walls are support in downtrend path—not a skip trigger. Volume 1.74x, ADX 22-26 on lower TFs (trending). Execute.
k192 execute 0.78   3/4 HTF align BEAR (1h/15m/5m). ADX expanding, regime TREND, combo 1.0. Bid walls soft vs momentum.
k230 execute 0.72 ✱ 3-TF confluence (15m HyperWave Down + 5m I-CHOCH+) aligns with 1h/15m/5m BEAR trend. 1h ADX 22.2 + Expanding EMA supports trend. Bid walls are support in downmove path—not a blocker. Combo weight 1.0 is neutral baseline; strong momentum score (1.75) + trend (2.50) outweighs liquidity opposition (zeroed). 1d NEUTRAL softens regime but 4h/1h agreement is sufficient. Execute.
```

### vpos 21 · paper · LONG · stored R +0.285 · opposing Bearish Liquidity Grab

**BEFORE** — execute 1/10 · skip 9/10

```
k  1 execute 0.78   1h/15m/5m bull confluence, ADX 28.9/34.5 strong trend, 1h EMA expanding. 1d bear is secondary; 4h neutral. Volume 2.48x avg supports. Ask wall at $76.25 is overhead resistance but trending ADX absorbs liquidity. Execute.
k 37 skip    0.78   1d BEAR regime opposes entry; 4h NEUTRAL with contracting EMA-gap. Lower-TF confluence strong but HTF headwind material.
k 63 skip    0.78   1d BEAR regime + 4h NEUTRAL contradict LONG entry. Lower-TF strength insufficient to override HTF headwind.
k 79 skip    0.72   1d BEAR trend + 4h NEUTRAL contradict LONG. 15m EMA flat. Ask-heavy OB at entry.
k109 skip    0.78   1d BEAR regime + 4h NEUTRAL override lower-TF bull confluence. Insufficient higher-TF support.
k135 skip    0.72   1d BEAR regime + 4h NEUTRAL override bullish lower-TF confluence; ask-heavy OB + flat 15m EMA-gap signal choppy, not clean trend setup.
k160 skip    0.78   1d BEAR + 4h NEUTRAL override lower-TF bull. Confluence strong but macro regime hostile.
k172 skip    0.78   1d BEAR regime + 4h NEUTRAL + massive ask wall overhead. LuxAlgo confluence strong, but HTF conflict + order-book friction outweigh.
k203 skip    0.72   1d BEAR regime contradicts LONG entry; 4h NEUTRAL weak. LuxAlgo confluence strong but higher-TF headwind material.
k221 skip    0.72   1d BEAR regime + 4h NEUTRAL override lower-TF bull confluence. Risk asymmetry unfavorable.
```
**AFTER** — execute 10/10 · skip 0/10

```
k  0 execute 0.72 ✱ 1h/15m trend strong (ADX 28.9/34.5), 1h EMA expanding, 1d bear vs 4h neutral opposition soft in lower-TF confluence. Volume 2.48x, combo 1.0. Liquidity opposes but minority-zeroed. Execute with caution on 1d headwind.
k 36 execute 0.72 ✱ 1h/15m strong bull (ADX 28.9/34.5, expanding gap). 1d bear is headwind but 4h neutral + 3/4 MTF align mitigate. Combo 1.0, vol 2.48x, fresh triggers. Bid walls absorb downside; ask wall is overhead but trending price breaks through. Liquidity signal aged (25min) and outvoted. Execute with caution on size.
k 62 execute 0.72 ✱ 1h/15m strong uptrend (ADX 28.9/34.5, Expanding EMA-gap). 1d BEAR headwind, but 4h/1h/15m aligned BULL. Massive ask wall overhead is soft caution in trending setup; strong volume ratio (2.48x) and combo weight 1.0 support breakthrough. Liquidity grab recent but MOMENTUM zeroed (conflicting signals 20/50min). Execute with elevated caution on 1d regime opposition.
k 78 execute 0.72   1h/15m BULL trend (ADX 28.9/34.5, Expanding EMA), strong confluence (1.0 combo), volume 2.48x. Daily BEAR is offset by 4h NEUTRAL and lower-TF agreement. Ask wall noted but typical for trending move; not a skip trigger given strong ADX and momentum. Execute with awareness of daily headwind.
k108 execute 0.72 ✱ Strong 1h/15m/5m bull alignment, high ADX (28.9/34.5), expanding EMA-gap 1h. 1d bear is lagging; 4h neutral. Combo 1.0, volume 2.48x, execution fresh. Ask wall overhead is soft caution in trending context—ADX/momentum sufficient to absorb. Liquidity SHORT signal minor noise vs. multi-TF confluence strength. Execute.
k134 execute 0.72   Strong 1h/15m trend (ADX 28.9/34.5), expanding EMA-gap, 3/4 MTF alignment, 2.48x volume, combo weight 1.0. Daily bear is headwind but lower-TF confluence is coherent.
k161 execute 0.72 ✱ 1h/15m strong trend (ADX 28.9/34.5, Expanding/Flat gap), LONG confluence 4.75pts. 1d bear neutral; 4h neutral but 1h bull dominates. Massive ask wall $76.25–$77.25 is soft caution in trending market with rising ADX; volume 2.48x supports breakthru. Liquidity SHORT zeroed as minority. Execute with awareness of overhead resistance.
k173 execute 0.72   1h/15m strong bull ADX (28.9/34.5), Expanding EMA, TREND regime, 4.75 score. 1d bear is offset by 1h momentum & execution confluence. Execute.
k202 execute 0.72   1h/15m strong uptrend (ADX 28.9/34.5, Expanding EMA), 5m trigger fresh, combo 1.0. 1d bear neutral; 4h weak. Ask wall overhead soft caution only given trend strength. Execute.
k220 execute 0.72 ✱ 1h/15m strong trend (ADX 28.9/34.5), 1h EMA expanding, 3-way confluence locked, combo 1.0. 1d bear is headwind but 4h neutral + 1h/15m bull override. Liquidity signal recent but minority-weighted. Execute.
```

### vpos 24 · paper · SHORT · stored R -1.050 · opposing Bullish Imbalance Mitigated, Bullish Liquidity Grab

**BEFORE** — execute 10/10 · skip 0/10

```
k  9 execute 0.82   Multi-TF bear alignment (4H/1H/15m/5m), strong 5m ADX 30.9, combo 1.0, vol 2.72x. Bid walls are resting support in downtrend path—acceptable for SHORT. 1H ADX 21.5 marginal but expanding gaps confirm trend. Execute.
k 24 execute 0.82   Strong multi-TF SHORT confluence (1d/4h/1h/5m BEAR aligned, MTF 4/4). ADX expanding on 4h/1h/5m. Combo weight 1.0 (neutral baseline). Bid walls below are support in downtrend path—not a blocker. Volume ratio 2.72x confirms conviction. 15m ADX slightly soft (19.7) but 5m ADX 30.9 strong; market is TREND-regime. Execute.
k 60 execute 0.78   Multi-TF BEAR regime (4h/1h/5m aligned), strong 5m trigger (S-CHOCH), 2.72x vol, combo 1.0. Bid walls are support-path friction; falling price absorbs them. ADX marginal but EMA expanding across 4h/1h/5m. Execute.
k 93 execute 0.82   Multi-TF bearish confluence (1H/15m/5m all BEAR), 4H BEAR regime support, combo 1.0, strong 5m volume (2.72x), 5m ADX 30.9 trending. Bid walls below are soft caution only—price absorbs them in trends. 1H ADX 21.5 + expanding gap confirms trend validity. Execute.
k 96 execute 0.82   3-TF confluence SHORT aligned with 4H/1H/5m BEAR regime. ADX rising 5m (30.9), volume 2.72x. Bid walls below are support—price absorbs resting bids downtrend. Slight 15m flatness offset by strong 1H/4H/5m trend coherence. Execute.
k129 execute 0.78   Multi-TF bear alignment (1d/4h/1h/5m all BEAR), strong 5m ADX 30.9, combo 1.0, vol 2.72x. 15m flat compression is minor drag; bid walls are resting support, not barrier to downtrend.
k152 execute 0.78   Strong multi-TF bearish confluence (1d-5m all BEAR, 4/4 MTF align). 1h/4h ADX >21 confirms trend. Combo 1.0 is baseline-solid. Bid walls below entry are support in downtrend path—not a blocker. Volume 2.72x healthy. 15m EMA-gap flatness is soft caution but overridden by 1h/4h/5m expanding gaps and rising 5m ADX 30.9. Execute.
k176 execute 0.82   Multi-TF bear alignment (1d/4h/1h all BEAR, 4/4 MTF score). 5m ADX 30.9 strong. Combo 1.0. Bid walls are support path—not blocking downside. Execute SHORT.
k205 execute 0.78   Multi-TF bear alignment (1d/4h/1h/5m); combo=1.0; strong 5m ADX 30.9; vol 2.72x. Bid walls are support in downtrend path—not a skip trigger. 15m ADX marginal but offset by 1h trending.
k234 execute 0.82   Strong multi-TF bear alignment (1d/4h/1h/5m), combo weight 1.0, vol ratio 2.72x, 5m ADX 30.9 trending. Bid walls are support in downtrend path—routine breakthrough. 15m ADX soft but 1h/5m strong.
```
**AFTER** — execute 7/10 · skip 3/10

```
k  8 execute 0.78 ✱ Strong 4/4 MTF alignment (4H/1H/15m/5m all BEAR). 1h ADX 21.5 + expanding EMA confirms trend. Combo 1.0, vol 2.72x, 5m ADX 30.9 sharp. Bid walls are support in downtrend path—not a block. Liquidity opposition minor. Execute.
k 25 skip    0.72 ✱ Liquidity headwind (2.50 LONG points) + bid-wall stack ($72.25×24.7) block momentum despite strong 5m/1h/4h bear alignment.
k 61 execute 0.78   Strong 4/4 MTF alignment (4h-5m all BEAR). Combo 1.0, volume 2.72x, 5m ADX 30.9 trending. Bid walls soft caution only.
k 92 execute 0.78   Multi-TF bear alignment (1d/4h/1h/5m all BEAR), strong confluence (15m HyperWave + 5m S-CHOCH), combo weight 1.0, volume 2.72x, MTF 4/4. Bid walls are support below; price absorbs. Execute SHORT.
k 97 execute 0.78   Strong multi-TF bearish alignment (1d/4h/1h/5m BEAR, MTF=4/4). Combo 1.0, vol 2.72x, ADX expanding. Bid walls are support below move, not rejection. Execute SHORT.
k128 execute 0.78 ✱ Strong 3-TF SHORT confluence (HyperWave+S-CHOCH), 4/4 MTF bearish alignment, 1h BEAR trend expanding EMA-gap, combo weight 1.0. Bid walls are soft caution in downtrend path; absorbed routinely. TREND+MOMENTUM score 5.0 vs liquidity opposition. Execu
k153 execute 0.78   Strong multi-TF bearish alignment (1d/4h/1h/5m all BEAR), 5.0 SHORT score, expanding EMA gaps across macro TFs, high 5m volume (2.72x), and 5m ADX 30.9 confirm trend. Bid walls are support in downtrend path—acceptable. 15m ADX/EMA flat is minor drag on confirmation but 1h/5m momentum decisive. Execute.
k177 skip    0.72 ✱ Flat 15m ADX (19.7) + bid-wall compression ($72.25 ×24.7) despite strong 5m/1h trend signal. Liquidity opposition unresolved.
k204 execute 0.78   Multi-TF bear alignment (1d/4h/1h/5m BEAR, ADX 21.5–30.9), strong confluence (SHORT 5.00 pts), high vol ratio (2.72x), expanding EMA. Bid walls are support in downtrend path—not blocking. TREND regime confirmed.
k235 skip    0.72 ✱ Liquidity headwind + weak lower-TF ADX override strong trend alignment. LIQUIDITY opposes SHORT (2.50pts zeroed); 15m ADX 19.7 is borderline weak; massive bid wall at $72.25 (24.7x) creates friction despite wall-rule mitigation. 1d ADX weak (11.8). TREND+MOMENTUM score 5.0 is solid, but execution clarity is absent (EXECUTION zeroed) and bid-wall friction + low 15m ADX suggest chop risk outweighs confluence strength in this regime.
```

---

## 4. THE BLOCK EACH AFTER ARM RECEIVED (the whole diff; nothing else differs)

### vpos 32 · +1,206 chars · +7/−0

```diff
--- vpos32_BEFORE
+++ vpos32_AFTER
@@ -30,2 +30,9 @@
   Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 3 agree, 0 oppose, 0 neutral, 0 absent.
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Trend Catcher Down w1.0 75 of 360 min)
+    MOMENTUM → 0 points, ZEROED: LONG and SHORT both inside its 90-min window (LONG 1.75: HyperWave Signal Up w0.7 45 of 90 min; SHORT 1.75: HyperWave Signal Down w0.7 0 of 90 min)
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Liquidity Grab w1.0 0 of 30 min, Bullish Imbalance Mitigated w0.5 15 of 30 min)
+    EXECUTION → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (Within Bearish OB w0.7 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (zeroed as the minority).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (4.25). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
```

### vpos 35 · +1,182 chars · +7/−0

```diff
--- vpos35_BEFORE
+++ vpos35_AFTER
@@ -33,2 +33,9 @@
   Both readings are FACTS about this consultation. The first counts a tier the gate's own TTL would have discarded; the second drops it. Decide for yourself how much weight a tier that old deserves.
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → no signal inside its 360-min window
+    MOMENTUM → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (HyperWave Signal Down w0.7 65 of 90 min)
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, not zeroed (the category counts are tied), counted only in the LONG score, which the score gate does not read for a SHORT entry (Bullish Liquidity Grab w1.0 5 of 30 min)
+    EXECUTION → 0 points, ZEROED: LONG and SHORT both inside its 5-min window (LONG 2.00: Bullish OB Entered w0.8 0 of 5 min; SHORT 2.50: Bearish I-BOS w0.7 0 of 5 min, Bearish OB Created w0.5 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (kept on the LONG side).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (1.75). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
```

### vpos 36 · +1,186 chars · +7/−0

```diff
--- vpos36_BEFORE
+++ vpos36_AFTER
@@ -33,2 +33,9 @@
   Both readings are FACTS about this consultation. The first counts a tier the gate's own TTL would have discarded; the second drops it. Decide for yourself how much weight a tier that old deserves.
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → no signal inside its 360-min window
+    MOMENTUM → 0 points, ZEROED: LONG and SHORT both inside its 90-min window (LONG 1.75: HyperWave Signal Up w0.7 50 of 90 min; SHORT 1.75: HyperWave Signal Down w0.7 5 of 90 min)
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, not zeroed (the category counts are tied), counted only in the LONG score, which the score gate does not read for a SHORT entry (Bullish Liquidity Grab w1.0 15 of 30 min)
+    EXECUTION → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Bearish OB Created w0.5 0 of 5 min, Bearish I-BOS w0.7 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (kept on the LONG side).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (2.50). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
```

### vpos 45 · +1,126 chars · +7/−0

```diff
--- vpos45_BEFORE
+++ vpos45_AFTER
@@ -32,2 +32,9 @@
   Score matrix, as the score gate counted these tiers (it counts every signal still inside its category window, not only the latest per slot): 1H → TREND SHORT +2.50, counted | 15m → MOMENTUM 0, no signal inside its 90-min window | 5m trigger → EXECUTION SHORT +1.75, counted
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Any Bearish Confirmation w0.7 110 of 360 min, Bearish Confirmation+ w1.0 110 of 360 min)
+    MOMENTUM → no signal inside its 90-min window
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Imbalance Mitigated w0.5 20 of 30 min, Bullish Liquidity Grab w1.0 20 of 30 min)
+    EXECUTION → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (Within Bearish OB w0.7 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (zeroed as the minority).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (4.25). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
```

### vpos 7 · +1,444 chars · +7/−0

```diff
--- vpos7_BEFORE
+++ vpos7_AFTER
@@ -22,2 +22,9 @@
 
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → LONG 2.50 points, AGREES with the proposed LONG, counted in the LONG score (Bullish Confirmation+ w1.0 110 of 360 min, Trend Catcher Up w1.0 110 of 360 min, Neo C. Switch Bullish w0.9 110 of 360 min, Any Bullish Confirmation w0.7 110 of 360 min)
+    MOMENTUM → 0 points, ZEROED: LONG and SHORT both inside its 90-min window (LONG 1.75: HyperWave Signal Up w0.7 50 of 90 min; SHORT 2.50: HyperWave OB Signal Down w1.0 65 of 90 min)
+    LIQUIDITY → SHORT 2.50 points, OPPOSES the proposed LONG, not zeroed (the category counts are tied), counted only in the SHORT score, which the score gate does not read for a LONG entry (Bearish Liquidity Grab w1.0 20 of 30 min)
+    EXECUTION → 0 points, ZEROED: LONG and SHORT both inside its 5-min window (LONG 2.50: Bullish OB Created w0.5 0 of 5 min, Bullish I-BOS w0.7 0 of 5 min; SHORT 1.75: Within Bearish OB w0.7 0 of 5 min)
+  Categories opposing the proposed LONG at scoring: LIQUIDITY SHORT 2.50 points (kept on the SHORT side).
+  Score gate arithmetic: the matrix score the score gate uses for this LONG entry is the LONG-side points only (2.50). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

### vpos 11 · +1,483 chars · +7/−0

```diff
--- vpos11_BEFORE
+++ vpos11_AFTER
@@ -22,2 +22,9 @@
 
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Smart Trail Switch Bearish w0.9 90 of 360 min, Any Bearish Confirmation w0.7 270 of 360 min, Bearish Confirmation+ w1.0 270 of 360 min)
+    MOMENTUM → 0 points, ZEROED: LONG and SHORT both inside its 90-min window (LONG 2.50: HyperWave Signal Up w0.7 60 of 90 min, Reversal Up w0.7 75 of 90 min, Bullish Divergence w0.8 75 of 90 min; SHORT 1.75: HyperWave Signal Down w0.7 15 of 90 min)
+    LIQUIDITY → LONG 1.25 points, OPPOSES the proposed SHORT, not zeroed (the category counts are tied), counted only in the LONG score, which the score gate does not read for a SHORT entry (Bullish Imbalance Mitigated w0.5 15 of 30 min)
+    EXECUTION → 0 points, ZEROED: LONG and SHORT both inside its 5-min window (LONG 2.00: Bullish OB Entered w0.8 0 of 5 min; SHORT 2.50: Bearish I-BOS w0.7 0 of 5 min, Bearish OB Created w0.5 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 1.25 points (kept on the LONG side).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (2.50). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

### vpos 13 · +1,264 chars · +7/−0

```diff
--- vpos13_BEFORE
+++ vpos13_AFTER
@@ -22,2 +22,9 @@
 
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → no signal inside its 360-min window
+    MOMENTUM → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (HyperWave Signal Down w0.7 25 of 90 min)
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, not zeroed (the category counts are tied), counted only in the LONG score, which the score gate does not read for a SHORT entry (Bullish Imbalance Mitigated w0.5 10 of 30 min, Bullish Liquidity Grab w1.0 10 of 30 min)
+    EXECUTION → 0 points, ZEROED: LONG and SHORT both inside its 5-min window (LONG 2.50: Within Bullish OB w0.7 0 of 5 min, Bullish Breaker w0.7 0 of 5 min; SHORT 2.50: Bearish OB Created w0.5 0 of 5 min, Bearish I-CHOCH w0.7 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (kept on the LONG side).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (1.75). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

### vpos 14 · +1,215 chars · +7/−0

```diff
--- vpos14_BEFORE
+++ vpos14_AFTER
@@ -22,2 +22,9 @@
 
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Trend Catcher Down w1.0 0 of 360 min, Any Bearish Confirmation w0.7 0 of 360 min)
+    MOMENTUM → 0 points, ZEROED: LONG and SHORT both inside its 90-min window (LONG 2.50: HyperWave OS Signal Up w1.0 75 of 90 min; SHORT 1.75: HyperWave Signal Down w0.7 15 of 90 min)
+    LIQUIDITY → LONG 1.25 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Imbalance Mitigated w0.5 25 of 30 min)
+    EXECUTION → SHORT 1.25 points, AGREES with the proposed SHORT, counted in the SHORT score (Bearish OB Mitigated w0.5 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 1.25 points (zeroed as the minority).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (3.75). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

### vpos 18 · +1,237 chars · +7/−0

```diff
--- vpos18_BEFORE
+++ vpos18_AFTER
@@ -22,2 +22,9 @@
 
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → LONG 2.50 points, AGREES with the proposed LONG, counted in the LONG score (Smart Trail Switch Bullish w0.9 105 of 360 min, Any Bullish Confirmation w0.7 225 of 360 min, Bullish Confirmation w0.7 225 of 360 min)
+    MOMENTUM → LONG 1.75 points, AGREES with the proposed LONG, counted in the LONG score (HyperWave Signal Up w0.7 30 of 90 min)
+    LIQUIDITY → SHORT 2.50 points, OPPOSES the proposed LONG, ZEROED as the minority direction across categories (Bearish Liquidity Grab w1.0 15 of 30 min, Broken U. w0.7 25 of 30 min)
+    EXECUTION → LONG 2.00 points, AGREES with the proposed LONG, counted in the LONG score (Bullish OB Entered w0.8 0 of 5 min)
+  Categories opposing the proposed LONG at scoring: LIQUIDITY SHORT 2.50 points (zeroed as the minority).
+  Score gate arithmetic: the matrix score the score gate uses for this LONG entry is the LONG-side points only (6.25). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

### vpos 19 · +1,283 chars · +7/−0

```diff
--- vpos19_BEFORE
+++ vpos19_AFTER
@@ -22,2 +22,9 @@
 
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Any Bearish Confirmation w0.7 265 of 360 min, Trend Catcher Down w1.0 265 of 360 min, Bearish Confirmation w0.7 265 of 360 min)
+    MOMENTUM → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (HyperWave Signal Down w0.7 55 of 90 min)
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Liquidity Grab w1.0 5 of 30 min, Broken D. w0.7 15 of 30 min)
+    EXECUTION → 0 points, ZEROED: LONG and SHORT both inside its 5-min window (LONG 1.75: Within Bullish OB w0.7 5 of 5 min; SHORT 2.25: Bearish I-CHOCH+ w0.9 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (zeroed as the minority).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (4.25). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

### vpos 21 · +1,194 chars · +7/−0

```diff
--- vpos21_BEFORE
+++ vpos21_AFTER
@@ -22,2 +22,9 @@
 
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → LONG 2.25 points, AGREES with the proposed LONG, counted in the LONG score (Smart Trail Switch Bullish w0.9 350 of 360 min)
+    MOMENTUM → 0 points, ZEROED: LONG and SHORT both inside its 90-min window (LONG 1.75: HyperWave Signal Up w0.7 20 of 90 min; SHORT 1.75: HyperWave Signal Down w0.7 50 of 90 min)
+    LIQUIDITY → SHORT 2.50 points, OPPOSES the proposed LONG, ZEROED as the minority direction across categories (Bearish Liquidity Grab w1.0 25 of 30 min)
+    EXECUTION → LONG 2.50 points, AGREES with the proposed LONG, counted in the LONG score (Bullish OB Created w0.5 0 of 5 min, Bullish I-BOS w0.7 0 of 5 min)
+  Categories opposing the proposed LONG at scoring: LIQUIDITY SHORT 2.50 points (zeroed as the minority).
+  Score gate arithmetic: the matrix score the score gate uses for this LONG entry is the LONG-side points only (4.75). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

### vpos 24 · +1,287 chars · +7/−0

```diff
--- vpos24_BEFORE
+++ vpos24_AFTER
@@ -22,2 +22,9 @@
 
+  Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
+    TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Any Bearish Confirmation w0.7 245 of 360 min, Bearish Confirmation+ w1.0 245 of 360 min)
+    MOMENTUM → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (HyperWave Signal Down w0.7 35 of 90 min, Bearish Divergence w0.8 35 of 90 min)
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Imbalance Mitigated w0.5 25 of 30 min, Bullish Liquidity Grab w1.0 30 of 30 min)
+    EXECUTION → 0 points, ZEROED: LONG and SHORT both inside its 5-min window (LONG 1.75: Bullish Breaker w0.7 4 of 5 min; SHORT 2.00: Bearish S-CHOCH w0.8 0 of 5 min)
+  Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (zeroed as the minority).
+  Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (5.00). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
 The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

---

## CONFIRMATION

| item | state |
|---|---|
| **`openitems_guard`** | EXIT **0** at 21:01 (first) and EXIT **0** at 21:20 |
| **files in the bot trees** | **none written by this pass.** Every file this pass created is in the session scratchpad. `claude_advisor` was imported with bytecode writing off: `__pycache__/claude_advisor.cpython-312.pyc` is still dated 20:06:05. Files newer than 20:50 in either tree: only `mercury-sol/optimizer/tg_offset.txt` and `titan-bot/optimizer/tg_offset.txt`, each written by that bot's own Telegram listener, plus the bots' own `trades.db` |
| **hashes** | md5 of every SOL `*.py` (incl. `config.py`), `titan-bot/config.py` and every `titan-bot/*.py`, plus the service lines: **identical** to the 20:09:12 snapshot at 21:19 |
| **DB** | SOL read only as `file:…?mode=ro` + `PRAGMA query_only=1`; **no DB write**. Titan's DB never opened |
| **orders / venue** | **none**. No venue call of any kind in this pass. The only external calls were 240 Anthropic M. API calls (Haiku 4.5) on SOL's advisor key, paused around every alert boundary |
| **restart** | **none**. `mercury-sol` NRestarts **0**, MainPID 2216962 (unchanged since 20:06:02) · `titan` NRestarts **0**, MainPID 1572470 (unchanged) · `mercury-sol-optimizer-listener` NRestarts 0 |
| **`FLAT_ADX_GATE_DRYRUN`** | **True** (config.py:407) |
| **`BOOK_GATE_DRYRUN`** | **False** (config.py:475) |
| **book-gate review counter** | **untouched** by this pass. Its own cron ran at 20:30:04 and 21:00:03; counts unchanged, LONG 0/135, SHORT 0/112 |
| **Titan** | **untouched**: no Titan file, DB or service touched. Titan's only read was the guard itself, which imports its config and reads git by design |
| **the live category block** | still no live entry consultation since the 20:06:18 cohort boundary (0 rows with `trades.id > 26793` and a prompt at 21:19); 0 open positions. The read-only waiter from the 2013 pass is still watching and will append to *that* report |
