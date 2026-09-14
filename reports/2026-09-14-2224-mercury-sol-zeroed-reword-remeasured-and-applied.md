# mercury-sol-zeroed-reword-remeasured-and-applied

_2026-09-14 22:24 UTC_

---

# Mercury-SOL — the word "ZEROED" was read as "does not count": re-worded, re-measured, applied

**2026-09-14 · re-measured before applying · ONE wording change APPLIED FROM FLAT, LOADED** · `openitems_guard` EXIT 0 at 21:59 (first), after the restart (22:21), and at 22:24

**Basis:** `reports/2026-09-14-2119-mercury-sol-replay-opposed-entries-with-the-category-block.md`: its narration finding and its 12 rows.

> 🔴 **THIS PASS MEASURES THE MODEL'S READING OF A WORD. IT DOES NOT MEASURE WHETHER THE RESULTING TRADES MAKE MONEY.** No outcome claim of any kind is made.
> * 🔴 **Carried forward, verbatim in substance:** of the four readable rows the block flipped to skip at 21:19, **three were paper winners**: vpos 7 (+2.089R), 11 (+1.133R) and 13 (+1.337R). The fourth, vpos 36, was a live loss (−0.757R).
> * 🔴 **The kept-vs-zeroed split** (at 21:19, all four readable kept rows flipped and none of the five zeroed rows did) **is confounded with the proposed-side score** (kept 1.75–2.50 vs zeroed 3.75–6.25). **It is not ranked.**

> **THE ARITHMETIC, DECLARED BEFORE ANY ARM-C CALL** (file stamped 2026-09-14T22:01:11Z; first call 22:01:16)
> * **Setup:** 12 rows (live 32, 35, 36, 45; paper 7, 11, 13, 14, 18, 19, 21, 24).
>   - **A** = stored prompt, no block.
>   - **B** = the block as shipped at 20:06:18 (source sha `dcd7426c`).
>   - **C** = the re-worded block (staged sha `52feade7`).
> * **Size and cost:** N = **10** per arm per row = **360 calls**. Upper bound **$1.08**. Actual **635,880 in + 41,673 out tokens = $0.8442**.
> * **Method, exactly as at 21:19:** each row's own stored system prompt; `claude-haiku-4-5-20251001`; `max_tokens` 256; no temperature; rounds shuffled (seed 202609142); sequential calls paused from 10 s before to 75 s after every alert boundary.
> * **PRIMARY TEST: B vs C** execute counts per row, two-sided Fisher exact. **Bonferroni over 12 rows: α = 0.05/12 = 0.00417.**
> * **READABLE** = arm A stable at 10/10. Unreadable rows are reported, never ranked.
> * **APPLY RULE:** apply from flat only if ≥ 1 readable row has B-vs-C p < α. If C is indistinguishable from B on every readable row, **do not apply**.
> * **Dismissal count:** C and B reasons that name the opposing category and discount it with "zeroed", "minority", "outvoted" or "weak" (or close forms). Regex first, then every hit read by hand; exclusions listed.

---

## VERDICT

**1. The re-wording did NOT move the rows it was aimed at.**
- vpos 32: 10 → 10. vpos 14: 10 → 8 (p 0.47). vpos 18: 10 → 10. vpos 19: 10 → 10. vpos 24: 8 → 10 (p 0.47). B → C execute counts.
- **None clears α.** The model executes these rows whether the opposition is labelled "ZEROED" or explained through the gate.

**2. It moved exactly ONE readable row, and in the other direction.**
- **vpos 36** (live, kept tie): **B 0/10 → C 10/10 execute**, p 1.1e-05 < α. That is back to the no-block verdict (A 10/10).
- The C reasons on vpos 36 cite 4-TF bear alignment and "no opposing walls", and none of the ten names the opposing LIQUIDITY.
- vpos 45, 7, 11 and 13 stayed at 0 or 1 of 10 under both B and C.

**3. The dismissal narration mostly survived.**
- On readable rows, reasons that name the opposing LIQUIDITY and discount it with zeroed / minority / weak went from **7 (B) to 4 (C)**; one more C dismissal is on unreadable vpos 21.
- **A new form appeared under C:** *"Liquidity SHORT minority, ignored per gate rules."* (vpos 18). The fact that the gate never subtracts opposing points was itself taken as a licence to set the opposition aside.
- The word "minority" still reaches the model from the rule's own name. "Zeroed as the minority" still reaches it from the closing "Categories opposing…" line, which this pass was told not to touch.

**4. Applied, under the pre-declared rule.**
- One readable row differed B vs C at α, so the rule said apply. Applied **from flat** at 22:20:42, loaded and verified.
- 🔴 **Declining because of the direction of that one move would be an outcome lean, which this pass forbids.** The change was also justified on its own terms: "ZEROED" described card bookkeeping as if it were a dismissal.
- 🔴 **The honest reading:** a factual correction that changed one verdict, back toward the no-block answer, and did not stop the model discounting the opposition.

**5. Three cohorts, never pooled.**
- **A:** `trades.id ≤ 26793`, no block.
- **B:** 20:06:18 → 22:21:06, ids 26794–26814. A **short-lived cohort** holding only **2 entry consultations** (26808, 26812), neither with an opposing category.
- **C:** `trades.id > 26814`, from **22:21:06 UTC**.

**6. The shipped block (B) is now LIVE-PROVEN, which the 2013 pass could not yet say.**
- The first two live consultations after 20:06:18 (rows 26808 at 21:40, 26812 at 21:50, both LONG, both `ai_skipped`) carried it directly under the matrix line.
- **8 of 8 category claims agree with each row's stored matrix.** Neither had an opposing category, so neither exercised the OPPOSES line.
- 🔶 **The 2013 pass's background waiter had died silently** (empty log, no output), so nothing was appended to that report. Its orphaned launcher was stopped, and this report records the proof instead.

---

## 1. THE RE-WORDING

### 1a–1c. What changed: the two OPPOSING branches only

**The gate clause is now identical for a zeroed and a kept category.** They differ only in what the minority rule did to the card.
- **Unchanged:** the category list, signal names and ages, the AGREES and intra-conflict lines, the closing "Categories opposing…" line and the "Score gate arithmetic" sentence.
- **Facts only:** the contract's 18-word whole-word ban list still passes.

**vpos 45 (ZEROED row): the changed line, BEFORE (as shipped) and AFTER (re-worded), verbatim**

```
BEFORE: LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Imbalance Mitigated w0.5 20 of 30 min, Bullish Liquidity Grab w1.0 20 of 30 min)

AFTER:  LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT; the score gate uses only SHORT-side points and never subtracts LONG points, so these 2.50 LONG points leave the SHORT score unchanged whatever the minority rule does; that rule changes only the card and the stored breakdown, and it set this category's contribution there to 0 because LONG holds fewer categories (1) than SHORT (2) (Bullish Imbalance Mitigated w0.5 20 of 30 min, Bullish Liquidity Grab w1.0 20 of 30 min)
```

**vpos 45: unified diff of the whole prompt, B (shipped block) → C (re-worded block)**

```diff
--- vpos45_B_as_shipped
+++ vpos45_C_reworded
@@ -35,3 +35,3 @@
     MOMENTUM → no signal inside its 90-min window
-    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, ZEROED as the minority direction across categories (Bullish Imbalance Mitigated w0.5 20 of 30 min, Bullish Liquidity Grab w1.0 20 of 30 min)
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT; the score gate uses only SHORT-side points and never subtracts LONG points, so these 2.50 LONG points leave the SHORT score unchanged whatever the minority rule does; that rule changes only the card and the stored breakdown, and it set this category's contribution there to 0 because LONG holds fewer categories (1) than SHORT (2) (Bullish Imbalance Mitigated w0.5 20 of 30 min, Bullish Liquidity Grab w1.0 20 of 30 min)
     EXECUTION → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (Within Bearish OB w0.7 0 of 5 min)
```

**vpos 35 (KEPT row): the changed line, BEFORE (as shipped) and AFTER (re-worded), verbatim**

```
BEFORE: LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, not zeroed (the category counts are tied), counted only in the LONG score, which the score gate does not read for a SHORT entry (Bullish Liquidity Grab w1.0 5 of 30 min)

AFTER:  LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT; the score gate uses only SHORT-side points and never subtracts LONG points, so these 2.50 LONG points leave the SHORT score unchanged whatever the minority rule does; that rule changes only the card and the stored breakdown, and it left this category's contribution there at 2.50 because the category counts are tied (1–1) (Bullish Liquidity Grab w1.0 5 of 30 min)
```

**vpos 35: unified diff of the whole prompt, B (shipped block) → C (re-worded block)**

```diff
--- vpos35_B_as_shipped
+++ vpos35_C_reworded
@@ -36,3 +36,3 @@
     MOMENTUM → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (HyperWave Signal Down w0.7 65 of 90 min)
-    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT, not zeroed (the category counts are tied), counted only in the LONG score, which the score gate does not read for a SHORT entry (Bullish Liquidity Grab w1.0 5 of 30 min)
+    LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT; the score gate uses only SHORT-side points and never subtracts LONG points, so these 2.50 LONG points leave the SHORT score unchanged whatever the minority rule does; that rule changes only the card and the stored breakdown, and it left this category's contribution there at 2.50 because the category counts are tied (1–1) (Bullish Liquidity Grab w1.0 5 of 30 min)
     EXECUTION → 0 points, ZEROED: LONG and SHORT both inside its 5-min window (LONG 2.00: Bullish OB Entered w0.8 0 of 5 min; SHORT 2.50: Bearish I-BOS w0.7 0 of 5 min, Bearish OB Created w0.5 0 of 5 min)
```

### 1d. AST proof: only the prompt builder changed

```
top-level nodes: 53 -> 53
top-level nodes whose AST differs: ['_render_matrix_category_block']
consult_for_entry AST identical: True
system-prompt assignments identical: True (6/6)
text diff: +19 / -4 lines; function spans lines 572-665
changed line spans in new file: [(628, 638), (640, 644), (646, 647), (650, 650)] | all within function: True
AST PROOF PASS
```

- `signal_matrix.py`, `main.py`, `config.py`, every gate, the minority rule and the score are byte-identical. Their loaded bytecode headers still match unchanged sources (§3).
- The six system prompts are identical (AST above; sha256 pinned in the contract).

### 1e. Contract: updated, green as root and as botuser

**`tests/test_entry_prompt_category_block.py` changes:**
- The pinned vpos 45 and vpos 35 blocks were re-pinned to the new wording.
- A new check: the zeroed and kept OPPOSES lines contain one identical gate clause and differ only in the rule action.
- A new check: no OPPOSES line contains "ZEROED", "not zeroed" or "minority direction across categories".
- Every other check is unchanged, including [1] no-matrix prompt == pre-block builder, [3] nothing else moved, [6] malformed or absent input renders NOTHING, and [7] six system prompts sha256.
- **It goes red on the previous wording** (checked in a scratch copy: `vpos 45 block wording differs from the pinned text`, `vpos 35 block differs from the pinned text`, exit 1).

```
  [1] matrix_result=None == pre-change builder, byte for byte (1710 chars)
  [2] vpos 45 block rendered exactly as pinned, directly under the matrix line:
        Every category the score gate scored for this consultation — all four, including any that no tier above shows; each signal with its weight and its age against that category's own window:
          TREND → SHORT 2.50 points, AGREES with the proposed SHORT, counted in the SHORT score (Any Bearish Confirmation w0.7 110 of 360 min, Bearish Confirmation+ w1.0 110 of 360 min)
          MOMENTUM → no signal inside its 90-min window
          LIQUIDITY → LONG 2.50 points, OPPOSES the proposed SHORT; the score gate uses only SHORT-side points and never subtracts LONG points, so these 2.50 LONG points leave the SHORT score unchanged whatever the minority rule does; that rule changes only the card and the stored breakdown, and it set this category's contribution there to 0 because LONG holds fewer categories (1) than SHORT (2) (Bullish Imbalance Mitigated w0.5 20 of 30 min, Bullish Liquidity Grab w1.0 20 of 30 min)
          EXECUTION → SHORT 1.75 points, AGREES with the proposed SHORT, counted in the SHORT score (Within Bearish OB w0.7 0 of 5 min)
        Categories opposing the proposed SHORT at scoring: LIQUIDITY LONG 2.50 points (zeroed as the minority).
        Score gate arithmetic: the matrix score the score gate uses for this SHORT entry is the SHORT-side points only (4.25). The gate never subtracts points from a category that opposes the proposed side, so an opposing category of any weight leaves that score unchanged.
  [3] prompt minus the block == pre-change builder prompt for the same matrix_result
  [5] kept-tie (vpos 35), all-intra (vpos 44), clean LONG (vpos 43) exactly as pinned; zeroed and kept opposing lines share one gate clause and differ only in the rule action
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
- root exit 0 · botuser exit 0. `test_entry_prompt_matrix_line.py` OK (root, botuser). `test_entry_prompt_regime_line_is_legible.py` OK (root, botuser).

---

## 2. THE RE-MEASUREMENT (360 calls, A / B / C)

360 of 360 calls returned `end_turn` with parseable JSON; 0 API errors. "names opp." = reasons naming the opposing category. "dismisses" = hand-read count of those that discount it (§2b).

| vpos | book | side | opposing (rule) | A exec | B exec | C exec | readable (A 10/10)? | **B-vs-C p** | reading | A-vs-B p | A-vs-C p | names opp. B / C | dismisses B / C |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **32** | live | SHORT | LIQUIDITY LONG 2.50 (zeroed) | 10/10 | 10/10 | 10/10 | yes | **1.0e+00** | C = B | 1.0e+00 | 1.0e+00 | 1 / 2 | 1 / 2 |
| **35** | live | SHORT | LIQUIDITY LONG 2.50 (kept) | 9/10 | 5/10 | 0/10 | **no** | **3.3e-02** | **UNREADABLE** | 1.4e-01 | 1.2e-04 | 0 / 7 | 0 / 0 |
| **36** | live | SHORT | LIQUIDITY LONG 2.50 (kept) | 10/10 | 0/10 | 10/10 | yes | **1.1e-05** | **C ≠ B** → execute | 1.1e-05 | 1.0e+00 | 0 / 0 | 0 / 0 |
| **45** | live | SHORT | LIQUIDITY LONG 2.50 (zeroed) | 10/10 | 0/10 | 0/10 | yes | **1.0e+00** | C = B | 1.1e-05 | 1.1e-05 | 1 / 0 | 0 / 0 |
| **7** | paper | LONG | LIQUIDITY SHORT 2.50 (kept) | 10/10 | 0/10 | 0/10 | yes | **1.0e+00** | C = B | 1.1e-05 | 1.1e-05 | 0 / 3 | 0 / 0 |
| **11** | paper | SHORT | LIQUIDITY LONG 1.25 (kept) | 10/10 | 0/10 | 0/10 | yes | **1.0e+00** | C = B | 1.1e-05 | 1.1e-05 | 0 / 0 | 0 / 0 |
| **13** | paper | SHORT | LIQUIDITY LONG 2.50 (kept) | 10/10 | 1/10 | 0/10 | yes | **1.0e+00** | moved, not significant | 1.2e-04 | 1.1e-05 | 3 / 2 | 0 / 0 |
| **14** | paper | SHORT | LIQUIDITY LONG 1.25 (zeroed) | 10/10 | 10/10 | 8/10 | yes | **4.7e-01** | moved, not significant | 1.0e+00 | 4.7e-01 | 0 / 0 | 0 / 0 |
| **18** | paper | LONG | LIQUIDITY SHORT 2.50 (zeroed) | 10/10 | 10/10 | 10/10 | yes | **1.0e+00** | C = B | 1.0e+00 | 1.0e+00 | 5 / 2 | 4 / 2 |
| **19** | paper | SHORT | LIQUIDITY LONG 2.50 (zeroed) | 10/10 | 10/10 | 10/10 | yes | **1.0e+00** | C = B | 1.0e+00 | 1.0e+00 | 0 / 0 | 0 / 0 |
| **21** | paper | LONG | LIQUIDITY SHORT 2.50 (zeroed) | 3/10 | 10/10 | 9/10 | **no** | **1.0e+00** | **UNREADABLE** | 3.1e-03 | 2.0e-02 | 1 / 2 | 0 / 1 |
| **24** | paper | SHORT | LIQUIDITY LONG 2.50 (zeroed) | 10/10 | 8/10 | 10/10 | yes | **4.7e-01** | moved, not significant | 4.7e-01 | 1.0e+00 | 5 / 2 | 2 / 0 |

**Replication of 21:19 (arm B then → arm B now, execute of 10):** 32 10→10 · 35 4→5 · 36 1→0 · 45 0→0 · 7 0→0 · 11 0→0 · 13 1→1 · 14 10→10 · 18 10→10 · 19 10→10 · 21 10→10 · 24 7→8. **The shipped block's effect reproduced row for row.**
- Arm A shifted a little on the rows unstable at 21:19 (35: 7→9, 45: 9→10, 21: 1→3).
- **vpos 45 is readable this time** (A 10/10); B and C both 0/10.
- vpos 35 and 21 remain unreadable. vpos 35 went B 5/10 → C 0/10 (p 0.033, not below α, and unreadable anyway).

**By book, never pooled (execute of all calls):**
- **Live:** A 39/40 · B 15/40 · C 20/40. The +5 is vpos 36 +10, 35 −5.
- **Paper:** A 73/80 · B 49/80 · C 47/80.

### 2a. The test that matters: the rows the block did NOT move

| vpos | book | rule | B exec | C exec | B-vs-C p |
|---|---|---|---|---|---|
| 32 | live | zeroed | 10/10 | 10/10 | 1.00 |
| 14 | paper | zeroed | 10/10 | 8/10 | 0.47 |
| 18 | paper | zeroed | 10/10 | 10/10 | 1.00 |
| 19 | paper | zeroed | 10/10 | 10/10 | 1.00 |
| 24 | paper | zeroed | 8/10 | 10/10 | 0.47 |

**None moved. The re-wording does not change the verdict on the rows the "ZEROED" reading was blamed for.**

### 2b. 🔴 Did the re-wording land? The dismissal count

**Rule:** a reason counts if it names the opposing LIQUIDITY (as a category or signal) and discounts it with zeroed / minority / outvoted / weak or a close form ("minoritized", "minor").
- The regex hit 29 reasons across B and C.
- Each was read, and **13 were excluded** as not a dismissal: they cite the opposition as a reason to SKIP, or "weak" / "zeroed" refers to ADX, volume, MOMENTUM or EXECUTION.

**Counted dismissals, verbatim:**

**Arm B** (7):

```
vpos 32 k297 execute: 3/3 tier agreement (1H/15m/5m SHORT), TREND regime confirmed, ADX 23-27 expanding, 3.61x vol. 1d BULL vs SHORT is soft friction but 4h/1h/15m/5m align. Bid walls (p89, p75) are support-path friction, not blockers per WALL RULE. Liquidity opposition zeroed. Strong confluence overrides flat-market guard (ATR% low but EMA expanding, MTF=3). Execute.
vpos 18 k62 execute: 1h/15m/5m BULL confluence strong (ADX 27.5/41.3/46.6). Trend regime active, MTF alignment 3/4. Liquidity opposition (2.50 pts) minority. 1d/4h neutral but not hostile. Ask wall $77.75 is soft caution in established uptrend; volume ratio weak (0.72x) is minor drag. Score gate 6.25 LONG points vs 0 opposing. Execute.
vpos 18 k280 execute: 1h/15m/5m aligned BULL, ADX strong (27.5/41.3/46.6), EMA expanding 1h. 4h neutral but 1d weak caps upside. Overhead ask walls ($77.75, $78.25) are trending resistance, not hard blocks given rising ADX. Volume ratio 0.72x is soft but combo weight 1.0 and execution signal fresh (0/5min) support. LIQUIDITY category opposes but minoritized. Execute with tight stops.
vpos 18 k291 execute: 1h/15m/5m LONG aligned, ADX strong (27.5/41.3/46.6), 1h EMA expanding. 4h neutral but 1h leads. Overhead ask wall is soft caution in trending context; absorbed by rising ADX. Volume ratio 0.72x is mild drag but combo weight 1.0 + liquidity minority (SHORT zeroed) support execution.
vpos 18 k352 execute: 1h/15m/5m LONG confluence, 1h ADX 27.5 (strong trend), 4h ADX 28.9 supportive. 1d neutral (not opposing). Ask wall overhead (×15 at $77.75) is soft caution in trending context; volume ratio 0.72x and ATR% modest but 15m ADX 41.3 confirms momentum. Liquidity signal minority, ignored. Score gate 6.25 LONG-heavy. Execute with trend.
vpos 24 k95 execute: Strong multi-TF bearish alignment (1d/4h/1h all BEAR, 4h ADX 21.6). 15m HyperWave + 5m S-CHOCH confluence, combo 1.0. Bid walls are support below entry; high volume ratio (2.72x) and 5m ADX 30.9 confirm momentum. 15m ADX weak (19.7) but 1h expanding gap + 4h ADX support trend. Minor liquidity opposition (2.50pts zeroed) does not override strong TREND+MOMENTUM (5.0pts). Execute.
vpos 24 k122 execute: Strong multi-TF SHORT confluence: 1d/4h/1h/5m all BEAR-aligned, ADX expanding (21.5-30.9 on lower-TF), combo 1.0. Bid walls are support noise; price falls through. Vol ratio 2.72x solid. Skip liquidity opposing; it's zeroed and minority. Execute.
```

**Arm C** (5):

```
vpos 32 k136 execute: 3-tier confluence (1H/15m/5m all SHORT); 1H/15m/5m BEAR trend with expanding EMA-gaps; ADX 23-26 confirms momentum; combo 1.0 baseline. Bid walls below are support-in-path (soft caution per rule); volume 3.61x supports break. 1d BULL opposes but 4h/1h/15m/5m align SHORT (3/4 MTF). Market regime TREND with MTF score 3. Liquidity LONG signals are minority/zeroed. Execute.
vpos 32 k157 execute: 3-way LuxAlgo confluence (1H/15m/5m all SHORT), expanding EMA-gaps 1H/15m, ADX 23-25 (trend threshold), 5m vol 3.61x, combo 1.0. 1d opposes but weak (ADX 12.6); 4h neutral. Bid walls (p89, p75) are path support in downtrend—not skip triggers per WALL RULE. Market regime TREND, MTF alignment 3/4 lower TFs. Momentum zeroed (conflicting signals) but execution + trend + liquidity opposition weak. High confluence, coherent lower-TF setup. Execute.
vpos 18 k177 execute: 1h/15m/5m bull confluence, ADX 27.5/41.3/46.6 strong trend, 1h EMA expanding. 1d/4h neutral but 4h ADX 28.9 supportive. Liquidity SHORT minority, ignored per gate rules. Ask wall $77.75 is trend-aligned resistance—high ADX absorbs it. Volume ratio soft (0.72x) but not disqualifying in trend. Execute.
vpos 18 k214 execute: 1h/15m strong bull trend (ADX 27.5/41.3), 1h EMA expanding, 3/4 MTF alignment, combo 1.0. 5m volume weak (0.72x) and EMA contracting, but overhead ask wall is soft caution in trending context. LIQUIDITY SHORT minority overridden by dominant TREND/MOMENTUM/EXECUTION agreement. Enter.
vpos 21 (unreadable) k358 execute: 1h/15m BULL confirmed, ADX 28.9/34.5 strong trend, 1h EMA expanding. 1d BEAR is offset by 4h NEUTRAL + lower-TF alignment (3/4). Volume 2.48x, combo 1.0, momentum zeroed (acceptable). Ask walls at $76.25–$77.25 are overhead resistance in trending price; ADX strength + 1h expansion supports breakthrough. Liquidity SHORT is minority, execution LONG fresh. Execute with measured confidence due to 1d bear context and 15m EMA flat.
```

**Excluded regex hits** (read, not dismissals):

- k73 (vpos 45, arm B, skip): cites the opposition as a reason to SKIP ("weak trend … liquidity block"); "weak" = trend
- k263 (vpos 13, arm B, skip): "weak liquidity (0.05x vol)" = volume, not the category
- k296 (vpos 13, arm B, skip): cites the opposing LIQUIDITY 2.50 as a reason to SKIP
- k6 (vpos 18, arm B, execute): score comparison "6.25 LONG vs 2.50 SHORT liquidity"; "weak" = volume
- k197 (vpos 24, arm B, skip): cites the opposition as a reason to SKIP; "weak" = ADX
- k316 (vpos 24, arm B, skip): cites the opposition as a reason to SKIP; "weak" = ADX
- k43 (vpos 35, arm C, skip): SKIP citing "opposing LIQUIDITY signal"; "weak" = confluence
- k63 (vpos 7, arm C, skip): SKIP citing "liquidity gate shows SHORT opposition"; "weak" = volume
- k211 (vpos 7, arm C, skip): SKIP citing "liquidity SHORT opposition unresolved"; "weak" = volume
- k313 (vpos 7, arm C, skip): SKIP citing "liquidity opposes LONG"; "zeroed" = MOMENTUM
- k191 (vpos 13, arm C, skip): SKIP citing "2.50 LONG liquidity opposition"; "weak" = confluence
- k294 (vpos 13, arm C, skip): SKIP citing "LIQUIDITY opposes SHORT"; "zeroed" = EXECUTION
- k2 (vpos 21, arm C, skip): SKIP citing "Liquidity SHORT active"; "zeroed" = MOMENTUM

**Result:**
- Readable rows: B 7 → C 4.
- Unreadable vpos 21: B 0 → C 1.
- **New under C:** *"ignored per gate rules"* (k177). The gate clause is quoted as a reason to set the opposition aside.
- **The re-wording did not land as a narration fix.**

---

## 3. APPLIED FROM FLAT, LOADED

```
22:19:31  FLAT CHECK   virtual_positions open 0 · active_positions 0 · exit_pending 0 · neutral1h_followthrough 0
                       Bybit GET /v5/position/list SOLUSDT: positionIdx 2 size 0 · positionIdx 1 size 0 (retCode 0)
22:19:49  PATCH        backups written and sha-verified FIRST:
                         claude_advisor.py.bak_zeroedwording_20260914                        sha256 dcd7426c470b7f44
                         tests/test_entry_prompt_category_block.py.bak_zeroedwording_20260914  1e80700a35d7606d
                       os.replace (source ast.parse()d first):
                         claude_advisor.py                          -> 52feade7ec65e802
                         tests/test_entry_prompt_category_block.py  -> c7e212b928be1a24
22:20     CONTRACTS    3/3 root · 3/3 botuser · AST PROOF PASS (backup vs live file)
22:20:42  RE-CHECK     open vpos 0 · active 0 · exit_pending 0 · last row 26814 (22:20:03 htf_blocked) → systemctl restart mercury-sol
22:20:45  active · MainPID 2216962 -> 2245907 · NRestarts 0
22:21:06  [MERCURY-SOL] [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
22:21:06  [MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 2246062]
22:21:06  [MERCURY-SOL] [VPOS-RECONCILE] no open positions at boot — clean.
22:21:10  [MERCURY-SOL][VIRTUAL] [HEARTBEAT] alive ticks=1 (+1 in 4s) last_tick=4.0s max_tick=4.0s cadence=10s open=0 mode=LIVE pid=2246062
LOADED    __pycache__/claude_advisor.cpython-312.pyc written 22:20:48 — header == claude_advisor.py (sha 52feade7ec65e802)
            the new gate clause ("never subtracts", "changes only the card and the stored breakdown") is in the loaded function's constants;
            "ZEROED as the minority direction across categories" remains ONLY in the untouched AGREES branch (proposed side as the minority)
          main / signal_matrix / config .pyc headers == their unchanged sources (91dfa43f… / a075ce05… / a308a130…)
22:21     openitems_guard EXIT=0
```

### 3d. 🔴 Second cohort boundary

> **2026-09-14 22:21:06 UTC** (worker pid 2246062). Recorded in `OPEN-ITEMS-SOL.md §PROMPT-CATEGORY-WORDING-2026-09-14`.
> * **The 20:06:18 boundary now has a short-lived cohort between it and this one:** `trades.id` 26794–26814, holding **2 entry consultations** (26808, 26812), both LONG, both skipped, neither with an opposing category.
> * **Three wordings, three cohorts:** A ≤ 26793 · B 26794–26814 · C > 26814. **Never pool them.**

**Not live-proven for C yet.** No entry consultation had arrived between the 22:21:06 restart and publication.
- What IS proven now: the worker loaded the re-worded builder (bytecode above), and the contract pins the exact wording on vpos 45 and 35.
- The first cohort-C consultation that carries an opposing category is what will show the new line live. It can be found with `trades.id > 26814 AND ai_user_prompt LIKE '%OPPOSES the proposed%'`.

**Rollback:**
- `cp claude_advisor.py.bak_zeroedwording_20260914 claude_advisor.py`
- `cp tests/test_entry_prompt_category_block.py.bak_zeroedwording_20260914 tests/test_entry_prompt_category_block.py`
- restart **from flat**.

---

## 4. EVERY ARM-C REASON, VERBATIM, AND ARM B WHERE IT DIFFERS

"Where it differs" = rows whose B and C execute counts differ: vpos 35, 36, 13, 14, 21, 24. ✱ = counted dismissal.

### vpos 32 · live · SHORT · A 10/10 · B 10/10 · C 10/10 exec

**Arm C**

```
k  4 execute 0.78   3/3 LuxAlgo tiers agree SHORT. 1h/15m/5m all BEAR, ADX 23-26, EMA expanding. Combo 1.0. 1d opposes but weak (ADX 12.6); 4h neutral. Bid walls (p89, p75) are support, not blocker—price absorbs them in downtrends. Volume 3.61x, TREND regime, MTF alignment 3/4 strong. Slight caution: 1d bull, momentum zeroed. Execute.
k 41 execute 0.78   3-way confluence (1H/15m/5m all SHORT), BEAR trend on 1h/15m/5m, ADX 23-26 (trend confirmed), expanding EMA-gaps, volume 3.61x, combo 1.0. 1d BULL is context but 4h/1h/15m strong agreement dominates. Bid walls (p89, p75) are support-in-path; price absorbs bids in trending moves. Execute.
k 83 execute 0.78   3-way confluence, TREND regime (ADX 23-24 expanding gaps), 5m vol spike 3.61x. 1d BULL vs SHORT is soft friction; 4h/1h/15m/5m BEAR alignment compensates. Bid walls (p89, p75) are support below; price absorbs bids in downtrends. Combo 1.0, score gate passed. Slight caution: momentum zeroed (LONG/SHORT window conflict), but execution + trend + volume stack coherently.
k136 execute 0.78 ✱ 3-tier confluence (1H/15m/5m all SHORT); 1H/15m/5m BEAR trend with expanding EMA-gaps; ADX 23-26 confirms momentum; combo 1.0 baseline. Bid walls below are support-in-path (soft caution per rule); volume 3.61x supports break. 1d BULL opposes but 4h/1h/15m/5m align SHORT (3/4 MTF). Market regime TREND with MTF score 3. Liquidity LONG signals are minority/zeroed. Execute.
k157 execute 0.78 ✱ 3-way LuxAlgo confluence (1H/15m/5m all SHORT), expanding EMA-gaps 1H/15m, ADX 23-25 (trend threshold), 5m vol 3.61x, combo 1.0. 1d opposes but weak (ADX 12.6); 4h neutral. Bid walls (p89, p75) are path support in downtrend—not skip triggers per WALL RULE. Market regime TREND, MTF alignment 3/4 lower TFs. Momentum zeroed (conflicting signals) but execution + trend + liquidity opposition weak. High confluence, coherent lower-TF setup. Execute.
k180 execute 0.78   3/3 tier confluence, ADX>23 on 1h/15m, EMA expanding, TREND regime. 1d opposes but weak (ADX 12.6). Bid walls p89/p75 are thick but SHORT in confirmed downtrend—walls below absorb naturally. Volume ratio 3.61x, combo 1.0. Score gate 4.25pts SHORT. Proceed.
k223 execute 0.72   3-tier confluence (1H/15m/5m all SHORT), TREND regime (ADX 23-26, EMA expanding), 5m volume 3.61x; 1d BULL conflicts but 4H NEUTRAL & 1H/15m/5m BEAR align. Bid wall below (p89 at $76.25) is path friction, not hard block; price can absorb. Combo 1.0 neutral. Score 4.25 SHORT points vs 0 opposing. Enter.
k283 execute 0.78   3-tier SHORT confluence (1H bear trend, 15m HyperWave, 5m OB) with expanding EMA gaps on 1H/15m/5m, ADX 23-26 (trend threshold), high volume ratio (3.61x), and score 4.25. 1d bull opposes but weak (ADX 12.6). 4h neutral. Bid walls at p89/p75 are ordinary friction in downtrend path, not hard blocks. MTF alignment 3/4. Execute.
k298 execute 0.78   3/3 LuxAlgo tiers aligned SHORT. 1h/15m/5m BEAR confirmed; ADX ~23-26 (trend threshold met). 1d BULL opposes but weak (ADX 12.6). 4h NEUTRAL with strong ADX (28.4) but contracting EMA. Combo 1.0. Volume 3.61x. Bid wall at p89/p75 is support below—not blocking downside. EMA-gap expanding on lower TFs confirms momentum. Gate passes; execute.
k346 execute 0.78   3-tier SHORT confluence (1H/15m/5m all BEAR), ADX 23-26 trend, EMA expanding, combo 1.0. 1d BULL is weak drag (ADX 12.6), but 4H/1H/15m align SHORT. Bid walls are p89/p75 (thick, but SHORT breaks bids downward per rule). Volume 3.61x avg supports momentum. Trend regime confirmed, not flat. Execute.
```

### vpos 35 · live · SHORT · A 9/10 · B 5/10 · C 0/10 exec

**Arm B**

```
k 20 execute 0.72   4/4 MTF alignment (4h–5m all BEAR), 15m/5m fresh confluence, expanding EMA-gap despite flat regime label. 1H stale but directional stack strong. Bid-heavy OB, no opposing wall above entry. EXECUTE.
k 44 execute 0.72   4/4 lower-TF alignment (15m/5m/1h/4h all BEAR), 15m ADX 37.9 confirms trend, fresh 5m trigger. 1H stale but supportive. Bid wall at $75.25 (p90, x17.7) sits ABOVE entry—does not block SHORT. Flat regime label contradicted by expanding EMA-gaps and solid ADX 15m/5m; treat as low-vol trend environment. Execute.
k 75 skip    0.78   1H signal STALE (21.3h old, >6h window); market FLAT (ADX 1h=19.0, regime=FLAT, MTF=4); 1d NEUTRAL opposes regime.
k142 skip    0.72   1H signal STALE (21.3h); market regime FLAT (ADX 1h=19.0, ATR% low); bid wall x17.7 at $75.25 blocks SHORT
k168 execute 0.72   4/4 lower-TF alignment (15m/5m/1h/4h all BEAR). 15m ADX 37.9 strong; 5m trigger fresh. Stale 1H discounted. Market FLAT but EMA expanding across all TF. Bid wall at $75.25 (p90) opposes SHORT but sits at mid, not directionally blocking. Execution.
k183 execute 0.72   4/4 lower-TF alignment (4h/1h/15m/5m BEAR). 1H stale but 15m/5m fresh & strong. Market FLAT but EMA expanding & 15m ADX 37.9 confirms trend. No opposing wall above entry. Bid-heavy OB. Execute.
k229 skip    0.72   1H signal stale (21.3h); market regime FLAT with low 1h ADX (19.0); bid-wall pile at $75.25 (p90, x17.7) directly above entry blocks upside momentum absorption for short unwind.
k252 skip    0.72   1H signal STALE (21.3h old, past 6h window); market regime FLAT with low 1H ADX (19.0); bid-heavy imbalance contradicts SHORT momentum.
k309 execute 0.72   4/4 MTF align (4H/1H/15m/5m BEAR); 15m/5m fresh & strong (ADX 37.9/28.2); no opposing walls above entry; bid-heavy book. Stale 1H signal & FLAT regime label weaken conviction but don't block.
k339 skip    0.72   1H signal STALE (21.3h); market FLAT regime (1h ADX 19.0, low momentum); bid-side liquidity wall (p90, x17.7) at $75.25 near mid absorbs downside move.
```
**Arm C**

```
k 18 skip    0.78   FLAT market (1h ADX 19.0, low ATR%) + stale 1H signal + opposing LIQUIDITY signal override confluence strength.
k 43 skip    0.72   1H signal STALE (21.3h); Market regime FLAT w/ ADX 1h=19.0; opposing LIQUIDITY signal; weak confluence depth.
k 77 skip    0.72   1H signal stale (21.3h old, past 6h window); market regime FLAT with low 1h ADX (19.0) and weak MTF alignment (4/10); massive bid wall at $75.25 (p90, x17.7) directly above entry blocks short momentum.
k141 skip    0.72   1H signal STALE (21.3h old, 6h window). Market FLAT (ADX 1h 19.0, regime FLAT, MTF 4/5). Bid wall p90 x17.7 at $75.25 sits directly above SHORT entry point, blocking downside liquidity. LIQUIDITY opposes SHORT (2.50 LONG vs 1.75 SHORT momentum). Fresh 15m/5m agree, but stale trend + flat regime + thick opposing wall = execution risk too high.
k170 skip    0.72   1H signal STALE (21.3h old, past 6h window); market regime FLAT with low 1H ADX (19.0); bid-heavy order book with massive wall at $75.25 (p90, x17.7) directly above SHORT entry point acts as strong resistance absorption.
k185 skip    0.72   1H signal stale (21.3h); market_regime FLAT w/ low 1h ADX (19.0); opposing liquidity signal (2.50 LONG points) unresolved.
k230 skip    0.72   1H signal STALE (21.3h); market regime FLAT with weak MTF alignment (score 4); 1D neutral; bid wall x17.7 at $75.25 blocks SHORT move.
k253 skip    0.72   1H signal STALE (21.3h); market regime FLAT with low 1h ADX (19.0); opposing LIQUIDITY signal (2.50 LONG points); bid-wall at entry vicinity ($75.25, p90 x17.7) blocks SHORT momentum.
k311 skip    0.72   1H signal stale (21.3h); market_regime=FLAT w/ low 1h ADX 19.0; opposing LIQUIDITY signal; bid walls thick (p90 x17.7 at $75.25)
k340 skip    0.72   1H signal STALE (21.3h); market regime FLAT (ADX 1h=19.0, ATR% low); opposing LIQUIDITY signal; bid-heavy imbalance favors LONG.
```

### vpos 36 · live · SHORT · A 10/10 · B 0/10 · C 10/10 exec

**Arm B**

```
k 26 skip    0.72   FLAT market regime + stale 1H LONG opposes fresh 15m/5m SHORT. MTF trend (4H BEAR) supports SHORT but ADX weak across 1H/15m; EMA-gaps expanding but ATR% compressed. Ask-heavy imbalance + thick ask walls ($75.75 p59 x9.6, $76.25 p45 x7.2) block upside liquidity relief. Chop risk high; confluence insufficient to override flat guard.
k 38 skip    0.72   1H signal stale (6.8h); market regime FLAT with low ADX (1h:21.1, 15m:14.7); strong bid wall at $75.25 (p85, x16.1) absorbs SHORT momentum; 1d NEUTRAL opposes bearish setup.
k 79 skip    0.72   FLAT market (ADX 1h 21.1, ATR% low 0.392%/0.146%), stale 1H opposes, ask-wall p74 blocks SHORT
k125 skip    0.72   1H signal STALE (6.8h old, opposes SHORT); market FLAT (ADX 1h 21.1, ATR% low); ask wall p74 x12.9 at $75.25 blocks upside but order book ask-heavy. 4H/1H/15m/5m all BEAR-aligned (strong), but 1d NEUTRAL weakens regime. 2/2 fresh tiers agree SHORT, but stale opposition + flat regime + weak absolute momentum warrant caution.
k175 skip    0.72   FLAT market (ADX 1h/15m <23, ATR% low, regime=FLAT, MTF=4/10) + stale 1h LONG opposes. 4h BEAR supportive but insufficient to override flat chop. 2/2 fresh tiers agree SHORT, but in compression, execution risk high.
k203 skip    0.78   1H LONG stale+opposes; market FLAT (ADX 21.1/14.7, ATR% 0.392%/0.146%); bid wall x16.1 at $75.25 absorbs SHORT momentum.
k238 skip    0.78   1H tier stale (6.8h); market regime FLAT w/ low ADX (1h 21.1, 15m 14.7); ask-heavy imbalance; 1d NEUTRAL opposes momentum.
k271 skip    0.72   1H signal stale (6.8h old, past 6h window); market FLAT (ADX 21.1/14.7, ATR% low); 1d NEUTRAL opposes regime clarity. 15m/5m SHORT agree, but lack trend confirmation.
k321 skip    0.72   1H BEAR opposes 1H BULLISH signal (stale 6.8h); flat regime (ADX 21/15, ATR% 0.39%/0.15%) + ask-heavy imbalance (0.47) + thick ask walls (p74 x12.9, p59 x9.6) create friction. 4H/1H/15m/5m BEAR agrees, but weak 1H ADX + flat regime vs. strong lower-TF confluence marginal. Skip to avoid chop.
k324 skip    0.72   1H signal stale (6.8h); market FLAT (ADX 21.1/14.7, ATR% low); 1d NEUTRAL opposes. 15m/5m agree SHORT but weak confluence.
```
**Arm C**

```
k 25 execute 0.72   4H/1H/15m/5m aligned BEAR; 5m ADX 24.6 strong. 1H stale but 15m/5m fresh agree SHORT. Flat regime soft but EMA expanding across all TFs. No opposing wall blocks path down (bid walls above entry, ask walls above). Volume thin but confluence solid.
k 36 execute 0.72   4H/1H/5m bearish regime aligned. 15m/5m confluence fresh & strong. 1H stale (6.8h). Flat market (ADX 21.1, ATR% 0.39%) mitigated by expanding EMA-gaps & 4/4 lower-TF agreement. No opposing walls directly blocking SHORT. Bid walls above entry are ordinary (p22-p85), not thick. Ask-heavy imbalance mildly supportive. Volume ratio 1.13x adequate. Execute with caution in low-vol regime.
k 80 execute 0.72   4H/1H/15m/5m all BEAR, 5m ADX 24.6 (strong), 15m/5m fresh SHORT agreement. 1H stale LONG immaterial. Flat regime (ADX 21.1, 14.7) offset by multi-TF trend alignment & expanding EMAs. No opposing walls block SHORT. Volume 1.13x normal. Execution gate passed. Confidence tempered by low 1h ADX (21.1) & flat regime label, but lower-TF confluence coherent.
k124 execute 0.72   4H/1H/5m BEAR aligned; 15m+5m fresh SHORT confluence. 1H signal stale (6.8h). Market FLAT but EMA expanding. No opposing walls blocking SHORT. Execute.
k176 execute 0.72   4H/1H/5m BEAR regime + 15m/5m SHORT confluence override stale 1H LONG. Clean setup.
k201 execute 0.72   4/4 lower-TF (4H/1H/15m/5m) align SHORT. 1H stale LONG overridden. Flat regime but EMA expanding, ADX adequate. No opposing wall blocks entry.
k239 execute 0.72   4H/1H/5m BEAR alignment strong. 1H stale but 15m/5m fresh SHORT agreement. Flat regime (ADX 21.1, ATR% low) offset by Expanding EMA-gaps and lower-TF confluence. No opposing walls block SHORT. Execute.
k272 execute 0.72   4H/1H/5m BEAR regime aligned; 15m/5m confluence fresh & strong. 1H stale. Low vol/flat regime offset by expanding EMA-gaps & clear lower-TF agreement. No opposing walls block SHORT.
k323 execute 0.72   4H/1H/5m BEAR aligned. 15m+5m fresh SHORT confluence. Stale 1H bullish opposition discounted. Flat regime but EMA expanding, ADX rising on 5m (24.6). No thick opposing wall below entry.
k325 execute 0.72   4H/1H/5m BEAR trend aligned; 15m/5m confluence fresh & strong. 1H stale. Flat regime soft; EMA expanding supports move. Bid walls at p85 (x16.1) absorb short but p41–p22 exits remain viable. Execute.
```

### vpos 45 · live · SHORT · A 10/10 · B 0/10 · C 0/10 exec

**Arm C**

```
k 29 skip    0.72   1h ADX 20.2 (weak trend), 1d NEUTRAL regime, ask wall $99.75 (p72, x12.4) blocks SHORT path above entry.
k 58 skip    0.72   1h ADX 20.2 (weak trend), 15m EMA contracting, 5m volume 0.53x. Ask wall p72×12.4 blocks SHORT move. Flat-market compression dominates despite 4h/1h bear alignment.
k 74 skip    0.72   1h ADX 20.2 + 15m EMA contracting = flat compression; ask wall $99.75 (p72, x12.4) blocks SHORT momentum; 1d NEUTRAL opposes regime.
k133 skip    0.72   1h ADX 20.2 (weak trend) + 15m EMA contracting + 1d NEUTRAL (ADX 46.4 high but no clear direction) = flat/compressed regime. Ask wall at $99.75 (p72, x12.4) directly blocks SHORT. LuxAlgo confluence insufficient to override.
k151 skip    0.72   1h ADX 20.2 (weak trend), 15m EMA contracting, 5m volume 0.53x. Flat-market compression despite lower-TF bearish signals. Ask wall $99.75 (p72, x12.4) sits directly above entry; bid walls below absorb downside. Risk/reward poor.
k199 skip    0.72   1h ADX 20.2 (weak/ranging threshold); 15m EMA contracting + 5m NEUTRAL trend; ask wall x12.4 p72 blocks SHORT momentum.
k221 skip    0.72   1h ADX 20.2 (weak trend), 15m EMA-gap contracting, 5m volume 0.53x avg, ask wall $99.75 p72 (×12.4) blocks SHORT momentum. Flat compression overrides tier agreement.
k287 skip    0.72   1h ADX 20.2 (weak trend), 15m EMA contracting, 5m neutral ADX; ask wall x12.4 p72 blocks SHORT. Flat-market guard triggered.
k318 skip    0.72   1h ADX 20.2 (weak), 15m EMA contracting, 5m volume 0.53x (low). Flat-market compression with ask-heavy imbalance ($99.75 x12.4 ask wall at p72 blocks SHORT move). 1d NEUTRAL opposes. Execute only if confluence exceptional—it is not.
k338 skip    0.72   1h ADX 20.2 (weak trend), 15m EMA contracting, ask wall p72 x12.4 blocks short; 1d neutral opposes.
```

### vpos 7 · paper · LONG · A 10/10 · B 0/10 · C 0/10 exec

**Arm C**

```
k 17 skip    0.78   1d NEUTRAL + ADX 43.8 (overbought regime); 15m EMA flat despite 46.3 ADX suggests compression; massive ask wall ×20.3 at $71.25 blocks upside.
k 63 skip    0.78   1d NEUTRAL + high 1d ADX 43.8 (volatility compression) opposes; volume ratio 0.01x critically weak; liquidity gate shows SHORT opposition.
k102 skip    0.78   1d NEUTRAL + contracting EMA conflicts 4h/1h bullish; massive ask wall $71.25×20.3 blocks upside; low 5m vol 0.01x; MOMENTUM zeroed (HyperWave conflict).
k110 skip    0.78   1d NEUTRAL + EMA contraction; 15m ADX 46.3 but flat EMA + 5m vol 0.01x avg; massive ask wall at $71.25 (×20.3) blocks upside liquidity.
k162 skip    0.78   Massive ask wall ×20.3 at $71.25 blocks upside; 1d NEUTRAL + momentum zeroed conflict setup.
k211 skip    0.78   1d NEUTRAL + ADX 43.8 (overbought compression); 15m EMA flat; volume 0.01x avg is critically weak; liquidity SHORT opposition unresolved.
k216 skip    0.78   1d NEUTRAL + contracting EMA conflicts multi-TF bull setup; low 5m volume (0.01x) + massive ask wall at $71.25 (×20.3) blocks upside momentum.
k276 skip    0.78   1d NEUTRAL + contracting EMA opposes; 15m/5m EMA flat despite high ADX; massive ask wall ×20.3 at $71.25 blocks upside momentum. Momentum category zeroed (conflicting signals 50v65min). Execute risk outweighs confluence strength.
k313 skip    0.78   Massive ask wall ×20.3 at $71.25 directly above entry blocks upside; momentum zeroed (HyperWave OB Down active); liquidity opposes LONG
k354 skip    0.78   1d NEUTRAL w/ contracting EMA opposes regime; massive ask wall ×20.3 at $71.25 blocks upside; volume 0.01x avg too thin
```

### vpos 11 · paper · SHORT · A 10/10 · B 0/10 · C 0/10 exec

**Arm C**

```
k 11 skip    0.78   1h ADX 17.2 (weak trend), 4h NEUTRAL ADX 18.6. Massive bid wall ×19.6 below entry absorbs SHORT. Skip.
k 68 skip    0.82   1h ADX 17.2 (weak trend) + 4h NEUTRAL (regime opposition) + massive ask wall $71.75 (×15.0) above entry blocks SHORT momentum development.
k 97 skip    0.82   1h ADX 17.2 (weak trend); 4h NEUTRAL ADX 18.6 (no regime support); massive ask wall ×15.0 at $71.75 blocks SHORT momentum. Hard veto.
k127 skip    0.78   1h ADX 17.2 (weak trend), 4h NEUTRAL. Massive bid wall $71.25 (×19.6) below entry absorbs SHORT momentum. HARD veto.
k145 skip    0.82   1h ADX 17.2 (weak); 4h NEUTRAL conflicts SHORT; massive bid wall $71.25×19.6 below entry blocks downside liquidity.
k186 skip    0.78   1h ADX 17.2 (weak trend); 4h NEUTRAL ADX 18.6 opposes SHORT; massive bid wall at $71.25 (×19.6) below entry blocks downside.
k248 skip    0.78   1h ADX 17.2 (weak trend), 4h NEUTRAL + contracting EMA; massive bid wall $71.25 (×19.6) below entry absorbs downside momentum.
k265 skip    0.78   1h ADX 17.2 (weak trend) + 4h NEUTRAL ADX 18.6 conflict with SHORT. Massive bid wall $71.25 (×19.6) below entry blocks downside.
k307 skip    0.85   Massive ask wall (×15.0) at $71.75 directly above entry blocks SHORT momentum. 1h ADX 17.2 weak; 4h/1d NEUTRAL oppose.
k332 skip    0.92   1h ADX 17.2 (weak trend); 4h NEUTRAL ADX 18.6 opposes SHORT regime; massive bid wall at $71.25 (×19.6) blocks downside liquidity absorption for SHORT entry near $71.43.
```

### vpos 13 · paper · SHORT · A 10/10 · B 1/10 · C 0/10 exec

**Arm B**

```
k 35 skip    0.82   Flat market (1h ADX 24.7 edge, EMA-gaps all Flat except 15m/5m Expanding slightly) + massive ask wall (×16.8 at $68.75) blocks SHORT at mid. BEAR regime alignment is strong (1d/4h/1h all BEAR, 5m ADX 36.4), but volume ratio 0.05x is critically weak—no conviction. Execution category zeroed (LONG/SHORT both present). Momentum score 1.75 alone insufficient for flat-market confidence. Ask wall directly above entry price is soft-veto given marginal ATR% and low absolute volume. Pass.
k 50 skip    0.78   Massive ask wall (×16.8) at $68.75 directly above SHORT entry blocks downside. BEAR regime strong (1d-5m aligned), but wall veto is hard for SHORT. Skip.
k101 skip    0.78   BEAR regime dominance (1d/4h/1h all BEAR, ADX >24) + massive ask wall (×16.8 at $68.75) blocks SHORT. Flat 1h EMA + weak MOMENTUM (1.75 pts) insufficient.
k118 execute 0.72   BEAR regime 1d/4h/1h aligned. 15m/5m BEAR + SHORT signals strong. ADX 24.7/24.1/36.4 confirms trend. Flat 1h EMA but Expanding 15m/5m. Ask wall at $68.75 (×16.8) above mid is offset by 4/4 MTF alignment and clear bearish confluence. Volume ratio low (0.05x) but acceptable in BEAR regime. Liquidity category opposing does not override strong momentum agreement.
k173 skip    0.78   Massive ask wall (×16.8) at $68.75 directly above entry blocks SHORT. Hard veto applies.
k189 skip    0.78   FLAT regime (1h ADX 24.7, EMA-gap 0.281% Flat) + ask wall ×16.8 at entry-level $68.75 blocks SHORT momentum despite BEAR alignment.
k234 skip    0.78   FLAT market + massive opposing ask wall (×16.8 at $68.75) blocks SHORT. Weak momentum score (1.75) insufficient to override.
k263 skip    0.78   Massive ask wall ×16.8 at $68.75 (entry level) blocks SHORT. FLAT 1h regime + low ATR% + weak liquidity (0.05x vol) override weak momentum score.
k296 skip    0.78   Massive ask wall (×16.8 @ $68.75) directly above mid blocks SHORT. BEAR regime supports SHORT, but execution signal strength (MOMENTUM 1.75 pts) is weak vs opposing LIQUIDITY (2.50 pts). Volume 0.05x avg confirms thin market. Skip.
k334 skip    0.78   BEAR regime across all TFs + massive ask wall (×16.8 at $68.75) blocks SHORT. Weak momentum score (1.75 vs. typical 2.5+). Flat market.
```
**Arm C**

```
k 34 skip    0.85   Massive bid wall (×21.2 @ $68.25) blocks SHORT downside; weak execution score (1.75 pts); flat 1h EMA.
k 49 skip    0.78   Massive ask wall (×16.8) at mid price blocks SHORT. FLAT 1h EMA + weak MTF alignment (4/5) override confluence.
k 99 skip    0.72   BEAR regime 1d/4h/1h aligned; massive ask wall (×16.8) directly above SHORT; EXECUTION zeroed; weak confluence (1.75pts).
k117 skip    0.82   BEAR confluence strong (1d-5m aligned), but massive ask wall ×16.8 at $68.75 blocks SHORT. FLAT 1h regime + weak execution gate (LONG/SHORT zeroed) + ask-heavy book veto the entry.
k171 skip    0.78   Massive ask wall (×16.8) at $68.75 directly opposes SHORT. 1h ADX 24.7 > 22 but BEAR regime + flat 1h EMA + weak execution score (zeroed) override. Skip.
k191 skip    0.78   FLAT market (1h ADX 24.7 borderline, EMA-gap flat across 1d/4h/1h, regime FLAT, MTF 4) + weak confluence (score 1.75 SHORT vs 2.50 LONG liquidity opposition) + massive ask wall $68.75×16.8 directly above mid blocks SHORT development. Even though 1h trend is BEAR and 5m ADX is high, the flat EMA compression, low ATR%, low volume ratio (0.05x), and order-book resistance override weak signal strength. Skip this chop.
k235 skip    0.78   BEAR regime 1d/4h/1h support SHORT, but massive ask wall ×16.8 at $68.75 (entry level) blocks move. EXECUTION zeroed (LONG/SHORT tied). Skip.
k261 skip    0.82   Massive ask wall (×16.8) directly above SHORT entry blocks downside; flat 1h EMA + weak execution score (zeroed).
k294 skip    0.78   BEAR regime 1d/4h/1h aligned; massive ask wall ×16.8 at $68.75 blocks SHORT. Low combo weight (1.0), weak EXECUTION (zeroed by LONG/SHORT conflict), LIQUIDITY opposes SHORT (2.50 LONG). FLAT market regime + contracting 1h EMA despite ADX 24.7 suggests weak follow-through. Risk/reward unfavorable.
k335 skip    0.78   Massive ask wall ×16.8 at $68.75 (entry level) blocks SHORT. Hard veto.
```

### vpos 14 · paper · SHORT · A 10/10 · B 10/10 · C 8/10 exec

**Arm B**

```
k 31 execute 0.72   1d/4h/1h/15m/5m all BEAR; 15m ADX 33.1 strong; 5m trigger fresh; bid walls support SHORT
k 71 execute 0.72   Multi-TF BEAR alignment (1d/1h/15m/5m) + 15m ADX 33.1 + expanding EMA-gaps + strong SHORT confluence (3.75 score). 1h ADX 21.1 near threshold but 15m dominates. No hard wall veto (massive bids below, not above SHORT). TREND regime + MTF 3/4 alignment support SHORT. Volume ratio low (0.13x) is caution but not veto.
k 86 execute 0.72   1d/4h/1h/15m/5m all BEAR; 15m ADX 33.1 (strong); EMA expanding across MTF. Short-aligned. No hard wall veto.
k131 execute 0.72   Multi-TF BEAR alignment (1d/1h/15m/5m), 15m ADX 33.1 (strong trend), expanding EMA-gaps, SHORT confluence. Massive bid walls below entry (support) do not block SHORT. Execute.
k155 execute 0.78   1d/4h/1h/15m/5m all BEAR; 15m ADX 33.1 (strong); 5m trigger fresh; bid-wall at entry does not block SHORT.
k209 execute 0.72   Multi-TF BEAR alignment (1d/1h/15m/5m) + strong 15m ADX 33.1 + Expanding EMA supports SHORT. Opposing bid wall at $64.75 (×19.2) is soft veto under BEAR regime. LuxAlgo confluence strong (3.75 SHORT score). Execute.
k225 execute 0.72   Multi-TF BEAR alignment (1d/1h/15m/5m) + strong 15m ADX 33.1 + expanding EMA-gaps. 1h ADX 21.1 near threshold but 15m trend dominates. Massive bid wall at $64.75 sits at entry level—soft veto applies (counter-trend SHORT, 1h ADX ≤22). However, 5m trigger fresh, lower-TF confluence strong, and market regime=TREND support execution despite wall.
k274 execute 0.78   Multi-TF BEAR alignment (1d/1h/15m/5m all BEAR, ADX rising). 15m ADX 33.1 strong. SHORT aligned. Bid walls support drop.
k305 execute 0.72   1d/4h/1h/15m/5m all BEAR; 15m ADX 33.1 strong trend; 5m trigger fresh; bid-wall support below.
k327 execute 0.72   Multi-TF BEAR alignment (1d/1h/15m/5m) + 15m ADX 33.1 + expanding EMA-gaps support SHORT. Bid wall at $64.75 is thick but 1h ADX 21.1 is borderline; treat as soft veto. Confluence score 3.75 is strong. Execute.
```
**Arm C**

```
k 32 execute 0.72   Multi-TF SHORT aligned: 1d/1h/15m/5m all BEAR, 15m ADX 33.1 & 5m ADX 38.9 strong. Trend regime, expanding EMA-gaps. Massive bid wall at $64.75 (×19.2) is BELOW entry—supports downside. LuxAlgo confluence strong (TREND 2.50 + EXECUTION 1.25). 1h ADX 21.1 is borderline but 15m/5m dominance & trend alignment override. Low volume ratio acceptable in strong trending structure.
k 70 execute 0.72   SHORT aligned: 1d/1h/15m/5m all BEAR, ADX expanding (1h=21.1, 15m=33.1, 5m=38.9). TREND+EXECUTION confluence 3.75pts. Massive bid wall at $64.75 (×19.2) is BELOW entry, not opposing. Regime is TREND. Execute.
k 85 execute 0.78   Multi-TF BEAR alignment (1d/1h/15m/5m), ADX 21.1-38.9 expanding, strong SHORT confluence. Bid wall at $64.75 is soft (1h ADX 21.1 borderline; entry is trend-aligned SHORT, not exception case). Execute.
k129 skip    0.82   1d BEAR dominates; massive bid wall $64.75×19.2 blocks SHORT momentum. Low 1h ADX (21.1) weakens trend. Skip.
k153 execute 0.78   SHORT aligned: 1d/1h/15m/5m all BEAR; 15m ADX 33.1 strong; EMA expanding; TREND+EXECUTION 3.75pts. Bid wall at $64.75 (×19.2) is below entry, not opposing. Execute.
k208 execute 0.78   SHORT aligned: 1d/1h/15m/5m all BEAR, ADX elevated (15m 33.1, 5m 38.9), EMA expanding. LuxAlgo confluence strong (3.75 score). Bid wall at $64.75 (×19.2) below entry supports downside. TREND regime confirmed. Execute SHORT.
k227 execute 0.78   Multi-TF BEAR alignment (1d/1h/15m/5m) + 15m ADX 33.1 (strong trend) + Expanding EMA-gaps support SHORT. 1h ADX 21.1 is weak but 15m/5m ADX robust. Massive bid wall at $64.75 (×19.2) is SUPPORTING SHORT, not opposing. Volume ratio 0.13x is low but confluence is strong. Execute.
k273 skip    0.78   1d BEAR regime + massive bid wall at $64.75 (×19.2) blocks SHORT below entry. 1h ADX 21.1 at threshold.
k303 execute 0.78   SHORT aligned: 1d/1h/15m/5m all BEAR; 15m ADX 33.1 strong; EMA expanding; confluence fired. Massive bid wall at $64.75 is soft veto (1h ADX 21.1 ≤ 22, so SHORT veto stays hard) but entry is below mid; wall absorbs risk. TREND+EXECUTION score 3.75pts supports. Execute.
k329 execute 0.72   SHORT aligned: 1d/1h/15m/5m all BEAR, 15m ADX 33.1 strong, EMA expanding. Opposing ask wall at $64.75 (×6.3) is soft-vetoable given trend strength. Execute.
```

### vpos 18 · paper · LONG · A 10/10 · B 10/10 · C 10/10 exec

**Arm C**

```
k  7 execute 0.78   1h BULL trend (ADX 27.5, EMA expanding), 15m/5m confluence strong, 3/4 MTF alignment. 1d NEUTRAL is soft headwind but 4h ADX 28.9 supportive. Volume ratio 0.72x is mild drag. Overhead ask wall ($77.75×15, $78.25×10.2) is soft caution in trending market—ADX 27.5+ typically absorbs. Market regime TREND, combo weight 1.0. Execute with disciplined stops.
k 61 execute 0.78   Strong 1h/15m/5m bull confluence, ADX rising, 1h EMA expanding. 1d neutral but 4h ADX 28.9 supports. Ask wall soft caution.
k 91 execute 0.78   1h/15m/5m BULL confluence, ADX 27.5/41.3/46.6 strong trend, 1h EMA expanding. 4h neutral but 1h dominates. Overhead ask wall ($77.75×15, $78.25×10.2) is soft caution in trending market with rising ADX—expect absorption. Volume ratio 0.72x is modest but MTF alignment 3/4, combo 1.0, execution fresh (0min). Skip only if chop; this is coherent trend structure. Execute.
k114 execute 0.78   1h/15m BULL + rising ADX (27.5/41.3) + Expanding EMA (1h) + strong confluence (6.25 pts). 1d NEUTRAL is soft headwind but 4h ADX 28.9 supports. Ask wall overhead is resting liquidity in trending context—not a skip trigger. Volume 0.72x is mild concern but trend strength + MTF alignment (3/4) override. Execute.
k177 execute 0.78 ✱ 1h/15m/5m bull confluence, ADX 27.5/41.3/46.6 strong trend, 1h EMA expanding. 1d/4h neutral but 4h ADX 28.9 supportive. Liquidity SHORT minority, ignored per gate rules. Ask wall $77.75 is trend-aligned resistance—high ADX absorbs it. Volume ratio soft (0.72x) but not disqualifying in trend. Execute.
k214 execute 0.78 ✱ 1h/15m strong bull trend (ADX 27.5/41.3), 1h EMA expanding, 3/4 MTF alignment, combo 1.0. 5m volume weak (0.72x) and EMA contracting, but overhead ask wall is soft caution in trending context. LIQUIDITY SHORT minority overridden by dominant TREND/MOMENTUM/EXECUTION agreement. Enter.
k231 execute 0.78   1h/15m/5m bull confluence + 1h ADX 27.5 (trend), EMA expanding. 4h neutral but lower TF strongly aligned. Ask wall overhead is soft caution in trending market. Volume ratio weak (0.72x) is only material drag.
k281 execute 0.78   Strong 3TF confluence (1H bull ADX 27.5, 15m ADX 41.3, 5m trigger fresh). 1H EMA expanding, market regime TREND with MTF 3/4 alignment. 1D neutral is soft headwind but 4H ADX 28.9 supports. Ask walls overhead but trending price with rising ADX absorbs liquidity. Volume ratio 0.72x and 5m ATR% low are minor friction; combo weight 1.0 and score 6.25 LONG dominate. Execute.
k293 execute 0.78   1h/15m/5m BULL confluence, ADX 27.5/41.3/46.6 strong trend, 1h EMA expanding. 4h neutral but 1h dominates. Ask wall overhead is soft caution in strengthening uptrend—volume ratio weak (0.72x) is noted but trend structure solid. Execute.
k353 execute 0.78   1h/15m bull trend (ADX 27.5/41.3), expanding 1h EMA, strong LuxAlgo confluence (6.25pts). 1d neutral is soft headwind but 4h ADX 28.9 supports. Ask wall overhead is soft caution in trending market; volume ratio 0.72x is mild concern but trend structure intact.
```

### vpos 19 · paper · SHORT · A 10/10 · B 10/10 · C 10/10 exec

**Arm C**

```
k 12 execute 0.72   3TF SHORT confluence + BEAR 1h/15m/5m alignment. 1d/4h neutral (not opposing). Bid walls are support below move, not a skip trigger. TREND regime confirmed; ATR% low but EMA expanding on lower TFs. Combo 1.0, volume 1.74x. Execute with normal risk mgmt.
k 51 execute 0.72   3-TF confluence (15m HyperWave + 5m Bearish I-CHOCH) in confirmed BEAR regime (1h/15m/5m). 1h ADX 22.2 & expanding EMA-gap confirm trend. Bid walls are support-path friction, not blockers. Volume 1.74x, combo 1.0. 1d/4h neutral but lower-TF alignment 3/4 strong. Execute with mild caution on wall absorption.
k 89 execute 0.72   1h/15m/5m bear alignment strong; 4.25 SHORT score; ATR expanding; bid walls are support, not rejection—price breaks through; execute.
k111 execute 0.72   1h/15m/5m bear confluence + expanding EMA + 3/4 MTF align. Bid walls soft caution only; vol 1.74x, combo 1.0. Execute.
k148 execute 0.72   1h/15m/5m BEAR aligned; ADX rising (22–26); EMA expanding; combo 1.0; 3.74x vol. Bid walls are path support, not blocker.
k194 execute 0.72   3-TF confluence (15m HyperWave Down + 5m Bearish I-CHOCH+) aligns with 1h/15m/5m bear trend. 1h ADX 22.2 & 15m ADX 25.6 confirm momentum; EMA-gaps expanding on 1h/15m. Bid walls below are support in downtrend path—not a skip trigger. Combo weight 1.0 (neutral-positive historical). 1d/4h neutral but lower-TF alignment strong (3/4). Volume ratio 1.74x supports. Execution score 4.25 SHORT-side. Caveat: 1d/4h lack downtrend confirmation and ATR% compressed; if these walls hold hard, reversal risk rises.
k250 execute 0.72   3/4 MTF bear agreement (1h/15m/5m); 1h ADX 22.2 + expanding EMA confirms trend. Bid walls are support in downtrend path—acceptable. Volume 1.74x, combo 1.0. 1d neutral is soft headwind but lower TF confluence strong. Execute.
k258 execute 0.72   1h/15m/5m BEAR confluence, expanding EMA-gaps, ADX rising, TREND regime. 1d/4h neutral but not opposing. Bid walls below are support—acceptable for downtrend. Execute.
k288 execute 0.72   3-TF confluence SHORT, 1h/15m/5m BEAR aligned, ADX expanding 22–26, combo 1.0, vol 1.74x. Bid walls soft caution only.
k344 execute 0.72   3-TF confluence SHORT in confirmed 1h/15m/5m downtrend; 1d/4h neutral (not opposing); expanding EMA-gaps & MTF=3 support trend. Bid walls below entry are soft caution in downtrend path, not skip trigger. Volume 1.74x, combo 1.0, ADX 22-26 adequate. Execute with standard risk mgmt.
```

### vpos 21 · paper · LONG · A 3/10 · B 10/10 · C 9/10 exec

**Arm B**

```
k  0 execute 0.72   1h/15m strong trend (ADX 28.9/34.5), Expanding EMA, LONG confluence 4.75pts. 1d BEAR is headwind but 1h bull & expanding gap override. Ask wall overhead is soft caution in trending context. Execute.
k 45 execute 0.72   1h/15m strong trend (ADX 28.9/34.5), LONG confluence, 4.75 score. 1d bear is headwind but lower-TF momentum & execution override. Proceed with position sizing discipline given liquidity anomaly & ask wall.
k105 execute 0.72   1h/15m strong trend (ADX 28.9/34.5), 1h EMA expanding, 3-TF confluence, combo 1.0. 1d bear offsetting but 1h bull dominates. Ask walls are resting liquidity in trending mkt.
k140 execute 0.72   1h/15m strong trend (ADX 28.9/34.5), 1h EMA expanding, 3-way confluence fired, 2.48x vol. 1d BEAR headwind and 15m EMA flat are soft cautions but lower-TF momentum + 4.75 score gate weight overrides. Proceed.
k166 execute 0.72   Strong 1h/15m trend (ADX 28.9/34.5), expanding 1h EMA, 3/4 MTF align, 2.48x vol. 1d bear headwind offset by local confluence strength.
k205 execute 0.72   1h/15m BULL with rising ADX (28.9/34.5), Expanding EMA-gap. 1d BEAR is recessive; 4h NEUTRAL weak. Strong confluence (TREND 2.25 + EXECUTION 2.50 = 4.75). Massive bid walls ($75.75 ×21.5) provide support; ask walls at $76.25+ are inline with trend absorption. Volume 2.48x avg, ATR sufficient for move. MOMENTUM zeroed (conflicting signals last 90min) is sole caution but not blocking given regime strength. MTF alignment 3/4 favors entry.
k241 execute 0.72   Strong 1h/15m/5m confluence (TREND+EXECUTION 4.75pts), ADX rising (28.9→34.5), MTF bullish (3/4 lower-TF agree). 1d bear is offset by robust intraday momentum. Ask walls above are absorbed by trending price; volume 2.48x supports breakout. Execute.
k267 execute 0.72   1h/15m strong trend (ADX 28.9/34.5), 1h EMA expanding, 4.75 score gate LONG. 1d bear is headwind but 3/4 MTF bullish. Ask wall soft caution only.
k301 execute 0.72   Strong 1h/15m trend (ADX 28.9/34.5), expanding EMA-gap, LONG confluence 4.75pts. 1d bear opposes but 4h neutral+1h bull dominate. Ask walls are soft caution in trending market; volume 2.48x avg supports breakout. Execute.
k357 execute 0.72   1h/15m trend strong (ADX 28.9/34.5), 1h EMA expanding, 4.75 score. 1d bear context mild given 4h neutral & lower-TF bull alignment. Ask wall overhead but trending price absorbs. Execute.
```
**Arm C**

```
k  2 skip    0.72   1d BEAR regime + 4h NEUTRAL oppose LONG. Momentum zeroed (HyperWave conflict). Liquidity SHORT active. Overhead ask wall at $76.25 (×18.8) blocks path despite 1h trend.
k 47 execute 0.72   1h/15m BULL with rising ADX (28.9/34.5), Expanding EMA-gap support LONG. 1d BEAR is offset by strong 4h/1h/15m alignment (3/4). Massive ask wall at $76.25 is typical trending resistance, not a blocker. Volume 2.48x, combo 1.0, fresh 5m trigger (Bullish OB). Momentum neutral but TREND+EXECUTION score 4.75 is solid. Execute with caution on breakout above $76.25.
k107 execute 0.72   1h/15m bull trend (ADX 28.9/34.5 expanding), 3/4 MTF align, strong confluence (4.75 pts). 1d bear is caution but lower-TF dominates at entry. Volume 2.48x, momentum zeroed but execution strong. Ask walls notable but trending ADX absorbs liquidity. Flat 15m EMA-gap is soft concern; 1h expansion outweighs. Bias execute.
k139 execute 0.72   1h/15m/5m LONG confluence + TREND regime (ADX 28.9/34.5), 1h EMA expanding. 1d BEAR is headwind but 4h NEUTRAL+1h BULL dominate. Volume 2.48x, combo 1.0. Bid walls >4x at $76.25 provide support; massive ask wall at $76.25 (×18.8) is overhead but trending ADX absorbs it. 15m EMA flat—minor caution but not decisive. Execute with tight stop.
k167 execute 0.78   1h/15m strong bull (ADX 28.9/34.5), 1d bear is distant regime; 3-way confluence live, 4.75 score, volume 2.48x, ask wall overhead but trending price absorbs liquidity; execute.
k206 execute 0.72   1h/15m bull ADX 28.9/34.5 + Expanding 1h EMA-gap + TREND regime + 2.48x vol + 4.75 score supports LONG. 1d bear is offset by strong 1h-15m confluence. Massive ask wall at $76.25 is noted but trending ADX + rising momentum typically absorbs resting liquidity. Momentum zeroed (conflicting signals within window) is slight caution but not disqualifying. Execute with tight stop.
k242 execute 0.72   1h/15m strong bull (ADX 28.9/34.5, Expanding/Flat EMA), 5m trigger fresh, 2.48x vol. 1d bear is offset by 3/4 lower-TF alignment. Overhead ask wall ($76.25×18.8) is secondary to trending momentum.
k269 execute 0.72   1h/15m strong uptrend (ADX 28.9/34.5, Expanding EMA), 3/4 MTF align LONG. 1d BEAR is headwind but lower-TF confluence is coherent. Volume 2.48x, momentum zeroed by recency conflict. Massive ask walls overhead are soft caution in trending market—ADX strength should absorb. Execute with awareness of daily bearish regime.
k302 execute 0.72   1h/15m strong uptrend (ADX 28.9/34.5), 1h EMA expanding, 5m vol 2.48x, confluence fired. 1d bear is offset by 4h neutral + 3/4 MTF alignment. Massive ask wall at $76.25 is soft caution in strong trend context—ADX rising absorbs resistance. MOMENTUM zeroed (conflicting signals within 90m window) slightly dampens confidence but TREND+EXECUTION (4.75 pts) override. Execute with conviction but monitor $76.25 resistance closely.
k358 execute 0.72 ✱ 1h/15m BULL confirmed, ADX 28.9/34.5 strong trend, 1h EMA expanding. 1d BEAR is offset by 4h NEUTRAL + lower-TF alignment (3/4). Volume 2.48x, combo 1.0, momentum zeroed (acceptable). Ask walls at $76.25–$77.25 are overhead resistance in trending price; ADX strength + 1h expansion supports breakthrough. Liquidity SHORT is minority, execution LONG fresh. Execute with measured confidence due to 1d bear context and 15m EMA flat.
```

### vpos 24 · paper · SHORT · A 10/10 · B 8/10 · C 10/10 exec

**Arm B**

```
k 22 execute 0.78   Strong multi-TF bearish alignment (1d/4h/1h all BEAR, 5m ADX 30.9). Trend+Momentum 5.0pts, combo 1.0. Bid walls are support noise in downtrend path; volume 2.72x avg absorbs them. 15m ADX mild (19.7) but 1h expanding, 5m strong. MTF 4/4 agrees SHORT. Execute.
k 55 execute 0.78   Multi-TF bear alignment (1d/4h/1h all BEAR, ADX 4h=21.6), 15m HyperWave+5m Bearish S-CHOCH confluence, strong combo weight 1.0, volume 2.72x, momentum solid. 1h ADX 21.5 borderline but EMA-gap Expanding across 4h/1h/5m supports trend. Bid walls below are SOFT caution given downtrend context—price routinely absorbs. Liquidity minor headwind. Execute.
k 95 execute 0.78 ✱ Strong multi-TF bearish alignment (1d/4h/1h all BEAR, 4h ADX 21.6). 15m HyperWave + 5m S-CHOCH confluence, combo 1.0. Bid walls are support below entry; high volume ratio (2.72x) and 5m ADX 30.9 confirm momentum. 15m ADX weak (19.7) but 1h expanding gap + 4h ADX support trend. Minor liquidity opposition (2.50pts zeroed) does not override strong TREND+MOMENTUM (5.0pts). Execute.
k122 execute 0.78 ✱ Strong multi-TF SHORT confluence: 1d/4h/1h/5m all BEAR-aligned, ADX expanding (21.5-30.9 on lower-TF), combo 1.0. Bid walls are support noise; price falls through. Vol ratio 2.72x solid. Skip liquidity opposing; it's zeroed and minority. Execute.
k161 execute 0.78   Strong multi-TF bearish alignment (1d/4h/1h/5m BEAR); 5.0 SHORT score; 2.72x vol; massive bid walls are support, not exit block.
k197 skip    0.72   Weak ADX (1h 21.5, 15m 19.7 at/near 20-23 threshold), flat 15m EMA-gap, liquidity opposes SHORT; bid walls thick. Soft flat-market guard triggered despite TREND label. Confluence alone insufficient to override.
k245 execute 0.78   Multi-TF bearish alignment (1d/4h/1h/5m BEAR, MTF=4/4), combo=1.0, strong 5m momentum (ADX 30.9), volume 2.72x. Bid walls are support in downtrend path—soft caution only. 15m ADX 19.7 is marginal but 1h ADX 21.5 + expanding EMA-gaps across 4h/1h/5m confirm trend. Execute with standard risk.
k255 execute 0.78   Multi-TF bear alignment (1d/4h/1h/5m), strong 5m momentum (ADX 30.9), combo 1.0, volume 2.72x. Bid walls are support in downtrend path—soft caution only. 15m ADX/EMA flat but overridden by 1h trend + 5m trigger strength. Execute.
k316 skip    0.72   Weak ADX (1h 21.5, 15m 19.7) + flat 15m EMA + liquidity opposition override confluence.
k350 execute 0.78   Multi-TF bear alignment (1d/4h/1h all BEAR), 5m ADX 30.9 strong, combo 1.0, volume 2.72x. Bid walls soft caution only.
```
**Arm C**

```
k 23 execute 0.78   Multi-TF bearish alignment (1d/4h/1h/5m BEAR, ADX expanding), strong 5m momentum (S-CHOCH, ADX 30.9), combo weight 1.0, volume 2.72x. Bid walls are support in downtrend path—not a skip factor. 15m ADX 19.7 is soft but 1h/5m trend dominates. Execute with conviction.
k 54 execute 0.78   Strong multi-TF bearish alignment (1d/4h/1h/5m BEAR, MTF=4/4). 1h ADX 21.5 + Expanding EMA confirms trend. Combo 1.0, volume 2.72x, 5m ADX 30.9 sharp. Bid walls are support, not barrier in downtrend. TREND+MOMENTUM 5.0pts outweigh LIQUIDITY opposition. Execute.
k 93 execute 0.78   Multi-TF bear alignment (1d/4h/1h/5m), strong 5m momentum (ADX 30.9), combo 1.0, vol 2.72x. Bid walls are path support; 15m ADX weak but 1h trend solid.
k121 execute 0.78   Multi-TF bear alignment (1d/4h/1h all BEAR, 4h ADX 21.6), 5m trend/momentum agreement, strong confluence weight 1.00, volume 2.72x. Bid walls are support in downtrend path—soft caution only. 15m ADX weak (19.7) but 5m ADX 30.9 strong, EMA expanding across regime. Execute with discipline.
k159 execute 0.78   Strong multi-TF bearish alignment (1d/4h/1h/5m all BEAR), combo 1.0, 5m ADX 30.9 + volume 2.72x. Bid walls are support—price breaks through. Execute.
k195 execute 0.78   Strong multi-TF bearish alignment (1d/4h/1h all BEAR, 5m ADX 30.9). 15m HyperWave + 5m S-CHOCH confirm SHORT. Combo 1.0 baseline solid. Bid walls below are path-support, not barrier—volume ratio 2.72x and expanding EMA-gaps across 4h/1h/5m support downside. 15m ADX 19.7 is slightly soft but 1h ADX 21.5 + 5m momentum (ADX 30.9) compensate. Market regime TREND with MTF score 4 is coherent. Liquidity noise (imbalance) minor vs trend confluence weight. Execute with standard risk mgmt.
k243 execute 0.78   4/4 MTF bear alignment, 5m ADX 30.9 (strong), combo 1.0, 2.72x volume. Bid walls are support-path soft caution, not blocker. Execute SHORT.
k257 execute 0.78   Multi-TF bear alignment (1d/4h/1h all BEAR), 5m ADX 30.9 strong, combo 1.0, vol 2.72x. Bid walls soft caution only.
k315 execute 0.78   Multi-TF bearish alignment (1d/4h/1h all BEAR), 5m ADX 30.9 strong, combo 1.0, volume 2.72x. Bid walls are support—do not block downtrend.
k348 execute 0.78   Strong multi-TF bear alignment (1d/4h/1h/5m BEAR). 1h ADX 21.5 (trend threshold), EMA expanding across 1d-5m. Combo 1.0, volume 2.72x, LuxAlgo 3-way confluent. Bid walls are support, not rejection in downtrend. 15m ADX soft but 5m ADX 30.9 sharp. TREND regime confirmed. Execute.
```

---

## CONFIRMATION

| item | state |
|---|---|
| **`openitems_guard`** | EXIT **0** at 21:59, 22:21 and 22:24 |
| **SOL DB** | read only as `file:…?mode=ro` + `PRAGMA query_only=1` by every measurement and check; **no DB write by this session**. §3 wrote no row; the restarted bot writes its own rows as always |
| **SOL config** | **not imported by any measurement.** The replay and render scripts import `claude_advisor` with bytecode writing off and `signal_matrix` stubbed; that import pulls `config` read-only, as the contracts do. `config.py` md5 unchanged |
| **orders / venue** | **no orders**. Venue calls: signed **`GET /v5/position/list`** (flat check). External calls: 360 Anthropic M. API calls (Haiku 4.5) on SOL's advisor key, paused around every alert boundary |
| **restart** | **one**, authorised by §3 under the pre-declared rule, from flat: `mercury-sol` MainPID 2216962 → 2245907, **NRestarts 0 → 0** |
| **Titan** | **untouched**. `titan` **NRestarts 0**, MainPID 1572470 unchanged. md5 of `titan-bot/config.py` and every `titan-bot/*.py` unchanged. Titan's DB never opened. Titan's only read was the guard itself |
| **`FLAT_ADX_GATE_DRYRUN`** | **True** (config.py:407), unchanged |
| **`BOOK_GATE_DRYRUN`** | **False** (config.py:475), unchanged |
| **book-gate review counter** | **not written by this session.** Only its own 30-min cron ran (22:00:03). It now reads LONG 0/137 (0/135 at 21:00): the live bot's own two new LONG evaluations (the consultations 26808 / 26812 passed the book gate). SHORT 0/112; fired `review_point` only |
| **files written in SOL's tree** | `claude_advisor.py` (patched) · `tests/test_entry_prompt_category_block.py` (re-pinned) · `OPEN-ITEMS-SOL.md` (+1 section) · three `.bak_zeroedwording_20260914` backups · `__pycache__/claude_advisor.cpython-312.pyc` (rewritten by the service at boot). The only other newer file is `optimizer/tg_offset.txt`, written by the bot's own Telegram listener |
| **background processes** | the orphaned 2013 launcher (a scratch process that could no longer fire) was stopped. No waiter was left running by this pass |
