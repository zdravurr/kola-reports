# Titan — **candidate 31, THIRD INDEPENDENT PASS FROM THE DB. The line CLOSES.** 🔴 **ZERO of the 9 live trigger names reaches n = 8 — the live book cannot rank a single one.** The eleven never-green losers were fired by **FIVE different names**, largest cell **3 of 11**. One name stands out on BOTH books — **`Bullish OB Created`**, 4 live entries, **0 winners**, **ΣR −3.6745** — and it **still cannot be convicted**: it fails Bonferroni, it fails the regime split, and **its name IS its side**. Nothing proposed. No diff.

**2026-09-16 21:30 UTC · published 17:22 UTC · commit `f16c271` · Titan LIVE REAL MONEY · READ-ONLY PASS · Mercury-SOL NOT TOUCHED** · `openitems_guard` **EXIT=0**

**Basis:** my own `2026-09-16-1520` **§3b(i)** (11 of 17 live losers never printed +0.25R, −7.5805R = 77 % of all live losses; **zero** losers ever reached +1R; every large loser peaked in the first 1–7 % of its life) and `2026-09-16-1730` (candidate 30, whose five-control frame this pass adopts verbatim).

> ## 🔴 WHAT THIS EDITION IS
> Two editions of this pass already stand on the record — `2026-09-16-1900` and `2026-09-16-2015`, the second
> a verification of the first that corrected two statements in it. **This is a third, fully independent
> computation from `trades.db`, run in a fresh session with no state carried over.** Every population count,
> every per-name cell, all 23 live MFEs, the eleven never-green losers, the four +1R mirrors and all five
> controls were recomputed from scratch before the earlier editions were read.
> **Result: the verdict and every headline number reproduce.** Three things are stated here that the earlier
> editions did not state, all flagged 🟡 **NEW IN THIS EDITION** — the smallest p in the *whole* family
> (§3a), the two readings of control (b) and why they disagree (§3b), and the instability of the "70.9 %"
> framing (§4b). **None of them moves the verdict.**

---

## 🔴 WHY THIS IS NOT THE THIRTY-FIRST FILTER — AND WHY IT IS NOT THE 2026-08-19 PASS EITHER

Candidates 1–30 each asked *"given this signal, should we enter?"* — a **CONDITION bolted on top of the
trigger**. This pass asks whether a particular **TRIGGER NAME** is worth subscribing to at all. A filter is a
rule; unsubscribing is a **subtraction**. Different object, and the second has never been examined on the book.

🔴 **AND IT IS EXPLICITLY NOT A RE-RUN OF 2026-08-19, WHICH IS NOT RE-OPENED HERE.** That pass measured all
**48 names on 32 246 PROPOSALS** and found no edge in any. **It measured SIGNALS. This measures POSITIONS.**
The two populations are not the same object and their results are never pooled or compared:

| | 2026-08-19 pass | **this pass** |
|---|---|---|
| unit of observation | a **proposal** (a signal arriving) | a **closed position** (money at risk) |
| population size | **32 246** | **75** |
| outcome measured | whether the signal had edge | **MFE, never-green share, realised R of the position it opened** |
| status | ✅ **SETTLED. NOT RE-RUN, NOT RE-OPENED, NOT CITED AS EVIDENCE HERE.** | the subject of this file |

*(For scale, and only for scale: `trades.db` holds **32 143 rows carrying a `tv_action`** across **62 distinct
names**. Of those, **75** ever became a closed position with a stored breakdown. The position book is
**0.23 %** of the signal book. A name can be edgeless on 32 246 proposals and still be the one that fired the
four worst entries — and vice versa. Neither result constrains the other.)*

---

# 🔴 n FIRST, BEFORE ANY RESULT. READ THIS BEFORE THE NUMBERS.

> ## ☠️ **NOT ONE LIVE TRIGGER NAME REACHES n = 8. ZERO OF NINE.**
> The 23 live positions are spread over **9 names**. The largest cell is **n = 6**; the next are 4, 4, 2, 2,
> 2, 1, 1, 1. **The live book cannot rank a single trigger name, and nothing below that cites a live cell is
> a ranking — it is a description.** The operator asked for the descriptive table anyway, and it is given in
> full in §2.
>
> On **paper**, **2 of 14** names reach n = 8: `Within Bearish OB` (n = 12) and `Bullish OB Created` (n = 9).
> **Paper is the only book that can rank anything at all, and it can rank exactly two names.**

**Ranking rule, pre-registered:** a cell is ranked only if **n ≥ 8**. Cells below that are printed and
**refused a rank** — never quietly merged into a neighbour. **Paper and live are NEVER pooled.**

---

## 🔴 CONTROLS, DECLARED IN THE HEADER — BEFORE ANY RESULT

* **Bonferroni over every name × side × book.** Union of names across both books = **15**. Realised
  non-empty (name × side × book) cells = **23** → **α = 0.05 / 23 = 2.174 × 10⁻³**. Counted as the full
  combinatorial grid instead (15 × 2 × 2 = 60) it is **α = 8.333 × 10⁻⁴**, stricter. **Both are quoted
  against every result below.**
* **A cell is ranked only if n ≥ 8.**
* **Survival requires ALL FIVE:** p < α · same sign in both chronological halves of each book · same sign in
  TREND and FLAT **with both legs populated** · **same sign on paper and live** · and it must **not be the
  score, the side or the era in disguise**.
* **R = `net_pnl / initial_risk_usdt`.** MFE/MAE from the row's own stored `water_mark` / `max_adverse_price`
  against `original_sl_price`. **All 23 live MFE/MAE/R values reproduce the 15:20 report's §3a table to the
  digit** — that reconciliation, and only that, licenses everything below.
* **p-values are two-sided permutation tests, 100 000–200 000 draws, seed 20260916.** `scipy` is not
  installed on this box; the tests are exact-permutation Monte Carlo written against `numpy` 2.2.6.

---

# 1. NAME EVERY ENTRY'S TRIGGER

## 1a. THE SOURCE, AND WHY `tv_action` IS THE TRIGGER NAME AND NOT AN INFERENCE

The 5m trigger name is read from **`trades.tv_action`** on the position's own entry row
(`virtual_positions.trades_entry_row_id` → `trades.id`). It is **not inferred.**

🔴 **IT IS ALSO CROSS-VALIDATED.** Where `entry_tiers_json` exists, its `tiers.5m.name` field is the same
string as `tv_action` on **24 of 24 rows — zero disagreements.** `entry_tiers_json` additionally marks the
5m tier `"kind": "trigger-capable"`, confirming that this is the tier that fires the entry. So `tv_action`
carries the trigger name for **every row in the population**, including the ones written before
`entry_tiers_json` existed.

## 1b. 🔴 THE COVERAGE LIMIT, STATED UP FRONT, BEFORE IT IS USED

`entry_tiers_json` begins **2026-07-29**. That splits the two questions cleanly:

| | LIVE (23) | PAPER (52) |
|---|---|---|
| **5m trigger name** (`tv_action`) | 🟢 **23 / 23 = 100 %** | 🟢 **52 / 52 = 100 %** |
| **1H + 15m tier names** (`entry_tiers_json`) | 🟢 **23 / 23 = 100 %** | ☠️ **1 / 52 = 1.9 %** |

> ### 🔴 **SAY IT PLAINLY: THE TRIGGER-NAME QUESTION IS FULLY COVERED ON BOTH BOOKS. THE 1H/15m CONTEXT QUESTION IS COVERED ON LIVE ONLY.**
> The single paper row with tiers is **vpos 85**, entered **2026-07-29 13:50:11** — the last paper position
> ever opened, one day inside the window. The paper book runs **2026-05-23 → 2026-07-29** and the live book
> **2026-07-30 → 2026-09-14**; they **do not overlap by a single day**. **No 1H/15m finding may be carried
> across books, and none is attempted below.** §1d is a LIVE-ONLY table and is labelled as one.

**Population:** **75 closed positions with a stored `matrix_breakdown_json` and a non-NULL
`initial_risk_usdt` — 23 LIVE (vpos 86–108) and 52 PAPER (vpos 34–85).**
🔴 **Excluded: vpos 27–33, seven rows, all for NULL `initial_risk_usdt`** — R is undefined without it.
*(The 17:30 candidate-30 file names only vpos 33 and gives the paper range as 27–85; the correct exclusion is
the whole block 27–33 and the correct paper range is 34–85. Corrected in the 20:15 edition; restated here
because the 17:30 file is left on the record unaltered. Neither the count 52 nor any figure depends on it.)*

## 1c. DISTRIBUTION OF TRIGGER NAMES, PER BOOK, PER SIDE

### LIVE — 23 positions, 9 names

| trigger name | n | LONG | SHORT | rankable (n ≥ 8)? |
|---|---|---|---|---|
| `Within Bullish OB` | 6 | 6 | 0 | ☠️ no |
| `Within Bearish OB` | 4 | 0 | 4 | ☠️ no |
| **`Bullish OB Created`** | **4** | 4 | 0 | ☠️ no |
| `Bearish OB Created` | 2 | 0 | 2 | ☠️ no |
| `Bearish I-CHOCH+` | 2 | 0 | 2 | ☠️ no |
| `Bullish I-BOS` | 2 | 2 | 0 | ☠️ no |
| `Bullish OB Mitigated` | 1 | 1 | 0 | ☠️ no |
| `Bearish I-BOS` | 1 | 0 | 1 | ☠️ no |
| `Bullish I-CHOCH+` | 1 | 1 | 0 | ☠️ no |
| | **23** | **14** | **9** | 🔴 **0 of 9 rankable** |

### PAPER — 52 positions, 14 names

| trigger name | n | LONG | SHORT | rankable (n ≥ 8)? |
|---|---|---|---|---|
| `Within Bearish OB` | **12** | 0 | 12 | 🟢 **YES** |
| **`Bullish OB Created`** | **9** | 9 | 0 | 🟢 **YES** |
| `Within Bullish OB` | 7 | 7 | 0 | ☠️ no |
| `Bearish OB Created` | 6 | 0 | 6 | ☠️ no |
| `Bearish I-BOS` | 5 | 0 | 5 | ☠️ no |
| `Bullish I-CHOCH+` | 2 | 2 | 0 | ☠️ no |
| `Bearish OB Entered` | 2 | 0 | 2 | ☠️ no |
| `Bullish OB Mitigated` | 2 | 2 | 0 | ☠️ no |
| `Bullish S-BOS` | 2 | 2 | 0 | ☠️ no |
| `Bullish OB Entered` · `Bearish I-CHOCH+` · `Bearish OB Mitigated` · `Bearish S-CHOCH+` · `Bullish S-CHOCH` | 1 each | 3 | 2 | ☠️ no |
| | **52** | **24** | **28** | 🟢 **2 of 14 rankable** |

> ### 🔴 **THE STRUCTURAL FACT THAT DECIDES THIS WHOLE PASS, AND IT IS VISIBLE IN THE TWO TABLES ABOVE.**
> **Every name containing `Bullish` fired LONG. Every name containing `Bearish` fired SHORT. 75 of 75 rows,
> ZERO exceptions, on both books.** The name→side mapping is **deterministic**: as a dummy variable a trigger
> name correlates with side at **ρ = ±1 by construction**. **No amount of data in this book can separate
> "this name is bad" from "this side is bad".** That is control (e) and it is settled before §2 begins.

## 1d. THE 1H AND 15m TIER NAMES PRESENT AT THE MOMENT OF ENTRY — 🔴 **LIVE BOOK ONLY** (23 of 23)

`(C)` = counted by the score gate · `(–)` = present but **not** counted.

| vpos | side | 1H (TREND) | 15m (MOMENTUM) | **5m TRIGGER (EXECUTION)** | R |
|---|---|---|---|---|---|
| 86 | SHORT | `Smart Trail Bearish` (C) | `HyperWave Signal Down` (C) | **`Within Bearish OB`** (C) | −1.022 |
| 87 | LONG | `Bullish Confirmation+` (C) | `HyperWave Signal Up` (–) | **`Within Bullish OB`** (C) | −0.440 |
| 88 | SHORT | `Smart Trail Bearish` (C) | `Reversal Up +` (–) | **`Within Bearish OB`** (–) | −0.296 |
| 89 | SHORT | `Smart Trail Bearish` (C) | `HyperWave Signal Down` (C) | **`Within Bearish OB`** (–) | **+1.386** |
| 90 | SHORT | `Smart Trail Bearish` (C) | `HyperWave Signal Down` (–) | **`Within Bearish OB`** (–) | −0.304 |
| 91 | SHORT | `Bearish Confirmation` (C) | `HyperWave OS Signal Up` (–) | **`Bearish OB Created`** (–) | −0.484 |
| 92 | LONG | `Smart Trail Bullish` (C) | `HyperWave Signal Down` (–) | **`Within Bullish OB`** (C) | −0.728 |
| 93 | SHORT | `Trend Catcher Down` (C) | `HyperWave Signal Down` (C) | **`Bearish I-CHOCH+`** (–) | −0.137 |
| 94 | LONG | `Smart Trail Bullish` (C) | `Reversal Down` (–) | **`Within Bullish OB`** (–) | **+0.865** |
| 95 | LONG | `Bullish Confirmation` (C) | `HyperWave Signal Up` (C) | 🔴 **`Bullish OB Created`** (C) | −0.533 |
| 96 | LONG | `Bullish Confirmation+` (C) | `HyperWave OB Signal Down` (–) | **`Bullish I-BOS`** (–) | −0.546 |
| 97 | LONG | `Bullish Confirmation+` (C) | `Reversal Down` (–) | 🔴 **`Bullish OB Created`** (C) | −0.796 |
| 98 | LONG | `Trend Catcher Up` (–) | `HyperWave Signal Up` (C) | **`Within Bullish OB`** (C) | −0.260 |
| 99 | LONG | `Trend Catcher Up` (–) | `HyperWave Signal Up` (C) | **`Within Bullish OB`** (C) | −0.532 |
| 100 | LONG | `Smart Trail Bullish` (C) | *(none)* | **`Within Bullish OB`** (C) | **+0.417** |
| 101 | SHORT | `Trend Catcher Down` (–) | `HyperWave Signal Down` (C) | **`Bearish OB Created`** (C) | +0.296 |
| 102 | LONG | `Smart Trail Bearish` (–) | `HyperWave Signal Up` (C) | 🔴 **`Bullish OB Created`** (C) | −1.158 |
| 103 | LONG | `Any Bullish Confirmation` (C) | `HyperWave Signal Down` (–) | **`Bullish OB Mitigated`** (C) | −1.123 |
| 104 | LONG | `Bullish Confirmation` (–) | `HyperWave Signal Up` (C) | **`Bullish I-BOS`** (C) | +0.576 |
| 105 | SHORT | `Smart Trail Bearish` (C) | `HyperWave Signal Down` (–) | **`Bearish I-BOS`** (C) | −0.014 |
| 106 | SHORT | `Any Bearish Confirmation` (C) | `HyperWave Signal Down` (C) | **`Bearish I-CHOCH+`** (–) | −0.296 |
| 107 | LONG | `Any Bullish Confirmation` (–) | `HyperWave Signal Up` (C) | 🔴 **`Bullish OB Created`** (C) | −1.187 |
| 108 | LONG | `Bullish Confirmation+` (C) | `HyperWave Signal Up` (–) | **`Bullish I-CHOCH+`** (C) | **+1.137** |

📋 **Recorded, not proposed:** vpos 102 entered **LONG on a 1H tier named `Smart Trail Bearish`** — the 1H was
pointing the other way and was not counted. It is one row, it is stated because it is visible, and it is
**not** a finding.

---

# 2. OUTCOMES BY TRIGGER NAME — LIVE AND PAPER **NEVER POOLED**

## 🔴 2b. THE TEST THAT MATTERS IS MFE AND THE NEVER-GREEN SHARE, NOT FINAL R

**77 % of the live losses are positions that never went anywhere.** A bad trigger shows up as a position
that **never moves** — not as one that moves and reverses. Final R conflates the trigger with the exit; MFE
and "did it ever print +0.25R" do not. **The `never +0.25R` column below is the primary column of this file;
`ΣR` is context.**

## 2a. LIVE — n = 23. ☠️ **EVERY CELL IS n ≤ 6. NOTHING HERE IS RANKED.**

| trigger name | n | ΣR | mean R | win rate | **median MFE** | **never +0.25R** |
|---|---|---|---|---|---|---|
| `Within Bullish OB` | 6 | −0.677 | −0.113 | 33 % | +0.772 | 2/6 = 33 % |
| 🔴 **`Bullish OB Created`** | **4** | 🔴 **−3.674** | 🔴 **−0.919** | 🔴 **0 %** | 🔴 **+0.152** | 🔴 **3/4 = 75 %** |
| `Within Bearish OB` | 4 | −0.236 | −0.059 | 25 % | +0.137 | 3/4 = 75 % |
| `Bearish I-CHOCH+` | 2 | −0.433 | −0.217 | 0 % | +0.030 | 2/2 = 100 % |
| `Bearish OB Created` | 2 | −0.189 | −0.094 | 50 % | +0.544 | 0/2 = 0 % |
| `Bullish I-BOS` | 2 | +0.030 | +0.015 | 50 % | +0.592 | 0/2 = 0 % |
| `Bearish I-BOS` | 1 | −0.014 | −0.014 | 0 % | +0.497 | 0/1 |
| `Bullish I-CHOCH+` | 1 | +1.137 | +1.137 | 100 % | +1.463 | 0/1 |
| `Bullish OB Mitigated` | 1 | −1.123 | −1.123 | 0 % | +0.015 | 1/1 = 100 % |
| **LIVE TOTAL** | **23** | **−5.1796** | −0.225 | 26 % | +0.427 | 11/23 = 48 % |

## 2a. PAPER — n = 52. 🟢 **TWO CELLS ARE RANKABLE (n = 12 and n = 9). THE OTHER TWELVE ARE NOT.**

| trigger name | n | ΣR | mean R | win rate | **median MFE** | **never +0.25R** | rank? |
|---|---|---|---|---|---|---|---|
| `Within Bearish OB` | **12** | −4.788 | −0.399 | 42 % | +0.791 | 4/12 = 33 % | 🟢 |
| 🔴 **`Bullish OB Created`** | **9** | 🔴 **−4.607** | 🔴 **−0.512** | 🔴 **11 %** | 🔴 **+0.096** | 🔴 **6/9 = 67 %** | 🟢 |
| `Within Bullish OB` | 7 | −1.930 | −0.276 | 29 % | +0.290 | 2/7 = 29 % | ☠️ |
| `Bearish OB Created` | 6 | **+4.957** | **+0.826** | 67 % | **+2.067** | 0/6 = 0 % | ☠️ |
| `Bearish I-BOS` | 5 | **+4.737** | **+0.947** | 60 % | **+2.310** | 1/5 = 20 % | ☠️ |
| `Bearish OB Entered` | 2 | −1.073 | −0.537 | 50 % | +0.316 | 1/2 | ☠️ |
| `Bullish I-CHOCH+` | 2 | +0.536 | +0.268 | 100 % | +0.811 | 0/2 | ☠️ |
| `Bullish OB Mitigated` | 2 | −0.260 | −0.130 | 50 % | +0.590 | 0/2 | ☠️ |
| `Bullish S-BOS` | 2 | −1.190 | −0.595 | 0 % | +0.588 | 0/2 | ☠️ |
| `Bearish I-CHOCH+` | 1 | +1.974 | +1.974 | 100 % | +2.981 | 0/1 | ☠️ |
| `Bullish S-CHOCH` | 1 | +0.503 | +0.503 | 100 % | +1.591 | 0/1 | ☠️ |
| `Bullish OB Entered` | 1 | +0.168 | +0.168 | 100 % | +1.290 | 0/1 | ☠️ |
| `Bearish OB Mitigated` | 1 | +0.116 | +0.116 | 100 % | +1.163 | 0/1 | ☠️ |
| `Bearish S-CHOCH+` | 1 | −0.560 | −0.560 | 0 % | +0.014 | 1/1 | ☠️ |
| **PAPER TOTAL** | **52** | **−1.4165** | −0.027 | 44 % | +0.679 | 15/52 = 29 % |

## 🔴 2c. WHICH NAMES FIRED THE ELEVEN NEVER-GREEN LIVE LOSERS

**vpos 86, 88, 90, 92, 93, 97, 99, 102, 103, 106, 107 — named, each one:**

| vpos | side | MFE | R | 🔴 **TRIGGER NAME** |
|---|---|---|---|---|
| 86 | SHORT | +0.099 | −1.022 | `Within Bearish OB` |
| 88 | SHORT | +0.076 | −0.296 | `Within Bearish OB` |
| 90 | SHORT | +0.175 | −0.304 | `Within Bearish OB` |
| 92 | LONG | +0.001 | −0.728 | `Within Bullish OB` |
| 93 | SHORT | **+0.000** | −0.137 | `Bearish I-CHOCH+` |
| 97 | LONG | +0.116 | −0.796 | 🔴 **`Bullish OB Created`** |
| 99 | LONG | +0.060 | −0.532 | `Within Bullish OB` |
| 102 | LONG | +0.188 | −1.158 | 🔴 **`Bullish OB Created`** |
| 103 | LONG | +0.015 | −1.123 | `Bullish OB Mitigated` |
| 106 | SHORT | +0.060 | −0.296 | `Bearish I-CHOCH+` |
| 107 | LONG | **+0.000** | −1.187 | 🔴 **`Bullish OB Created`** |

### 🔴 THE DIRECT ANSWER: **FIVE NAMES DID. NO SINGLE NAME CARRIES MOST OF THEM.**

| trigger name | count of the 11 | ΣR of those rows | vpos |
|---|---|---|---|
| `Within Bearish OB` | **3** of 11 | −1.622 | 86, 88, 90 |
| 🔴 **`Bullish OB Created`** | **3** of 11 | 🔴 **−3.142** | 97, 102, 107 |
| `Within Bullish OB` | **2** of 11 | −1.260 | 92, 99 |
| `Bearish I-CHOCH+` | **2** of 11 | −0.433 | 93, 106 |
| `Bullish OB Mitigated` | **1** of 11 | −1.123 | 103 |

> **BY COUNT the eleven split 3/3/2/2/1 — no concentration.**
> **BY MONEY they do not split evenly: `Bullish OB Created`'s three rows carry −3.1418R = 41.4 % of the
> entire −7.5805R never-green pool, from 3 of the 11 positions.** It is the only name where the count and
> the money point the same way.

*(Side-stripped, in case the operator wants the structural family rather than the polarity: `Within … OB`
**5 of 11** (−2.882R), `… OB Created` **3 of 11** (−3.142R), `I-CHOCH+` **2 of 11** (−0.433R), `OB Mitigated`
**1 of 11** (−1.123R). Recorded for completeness; the polarity-split table above is the one that matches the
mechanism, since the bot subscribes to the named signal, not to the family.)*

## 🔴 2e. THE MIRROR — WHICH NAMES FIRED THE FOUR LIVE POSITIONS THAT REACHED +1R

| vpos | side | MFE | R | 🔴 **TRIGGER NAME** |
|---|---|---|---|---|
| 89 | SHORT | +1.697 | +1.386 | **`Within Bearish OB`** |
| 94 | LONG | +1.802 | +0.865 | **`Within Bullish OB`** |
| 100 | LONG | +1.322 | +0.417 | **`Within Bullish OB`** |
| 108 | LONG | +1.463 | +1.137 | `Bullish I-CHOCH+` |

> ## ☠️ **THE MIRROR KILLS TWO OF THE FIVE OUTRIGHT, AND IT IS THE CLEANEST RESULT IN THIS FILE.**
> **`Within Bearish OB` and `Within Bullish OB` fired the never-green losers AND the +1R winners.**
> `Within Bearish OB` fired 3 of the 11 dead entries **and vpos 89, the single best live trade on the book
> (+1.386R)**. `Within Bullish OB` fired 2 of the 11 **and both remaining +1R positions (94 and 100)**.
> **Together they are 5 of the 11 dead entries and 3 of the 4 live winners.** Unsubscribing from either would
> have removed the book's best trades along with its worst. **They are not candidates. They are noise
> generators in both directions.**
>
> 🔴 **`Bullish OB Created` is the one name that appears in the dead-entry list and NOWHERE in the mirror.**
> **0 of 4 live winners. 0 of 4 that ever reached +1R. Its best live MFE is +0.560R.**

---

# 3. THE FIVE CONTROLS — the same five that killed candidate 30

Applied to **`Bullish OB Created`**, the only name that is worse on both books and absent from the mirror.
Every other name either fails §2e outright or has n ≤ 2 on both books.

## 3a. CONTROL (a) — BONFERRONI · ☠️ **FAILS**

**α = 2.174 × 10⁻³** (23 realised cells) or **8.333 × 10⁻⁴** (60-cell grid).

| book | test | observed | p | vs α = 2.174 × 10⁻³ |
|---|---|---|---|---|
| LIVE | mean R vs rest of book | −0.919 vs −0.079 | **0.0254** | ☠️ **11.7× too large** |
| LIVE | median MFE vs rest | +0.152 vs +0.464 | 0.2633 | ☠️ 121× |
| LIVE | never-green share vs rest | 75 % vs 42 % | 0.3151 | ☠️ 145× |
| PAPER | mean R vs rest of book | −0.512 vs +0.074 | 0.0853 | ☠️ 39× |
| PAPER | median MFE vs rest | +0.096 vs +0.806 | 0.0861 | ☠️ 40× |
| PAPER | **never-green share vs rest** | **67 % vs 21 %** | 🔴 **0.0116** | ☠️ **5.3× too large** |

🟡 **NEW IN THIS EDITION — THE SMALLEST p IN THE ENTIRE 23-CELL FAMILY, NOT JUST THIS NAME'S.** Every cell
was scanned. The smallest p anywhere is **0.0091** — `Bearish OB Created`, PAPER, median MFE (+2.067 vs
+0.631), followed by **0.0094** (`Bearish I-BOS`, PAPER, median MFE) and **0.0116** (`Bullish OB Created`,
PAPER, never-green). **The best result in the whole family is 4.2× above α on the 23-cell count and 10.9×
above it on the 60-cell count. Not one cell on either book clears Bonferroni. ☠️ CONTROL (a) FAILS FOR
EVERY NAME, and the two smallest p-values in the family belong to names that are *good*, not bad.**

## 3b. CONTROL (b) — CHRONOLOGICAL HALVES · ☠️ **FAILS**

🟡 **NEW IN THIS EDITION: THERE ARE TWO DEFENSIBLE READINGS AND THEY DISAGREE. BOTH ARE GIVEN.**

**Reading 1 — "is the group's own mean the same sign in both halves?"** (the literal question):

| book | half | span | n | mean R | sign |
|---|---|---|---|---|---|
| LIVE | H1 | 07-30 → 08-24 | **1** | −0.533 | − |
| LIVE | H2 | 08-24 → 09-14 | 3 | −1.047 | − |
| PAPER | H1 | 05-23 → 06-25 | 2 | −1.097 | − |
| PAPER | H2 | 06-25 → 07-29 | 7 | −0.345 | − |

**Same sign in all four halves — but the live H1 cell is n = 1, which is not a measurement.**

**Reading 2 — "is the group still worse than the rest OF ITS OWN HALF?"** (the control candidate 30 used, and
the stricter one):

| book | half | name mean | rest of half | **Δ** | never-green: name vs rest |
|---|---|---|---|---|---|
| LIVE | H1 | −0.533 (n=1) | −0.171 (n=10) | −0.362 | **0 % vs 50 % → −50 pp** |
| LIVE | H2 | −1.047 (n=3) | +0.022 (n=9) | −1.070 | **100 % vs 33 % → +67 pp** |
| PAPER | H1 | −1.097 (n=2) | +0.405 (n=24) | −1.502 | 50 % vs 21 % → +29 pp |
| PAPER | H2 | −0.345 (n=7) | −0.344 (n=19) | 🔴 **−0.0006** | 71 % vs 21 % → +50 pp |

☠️ **CONTROL (b) FAILS ON READING 2, AND READING 2 IS THE ONE THAT BINDS.** In the **second paper half —
the half holding 7 of the name's 9 paper rows — the mean-R effect is Δ = −0.0006R. It is GONE.** The whole
paper mean-R gap is carried by **two** H1 rows. And on live the **never-green** signal **inverts between the
halves**: −50 pp in H1, +67 pp in H2. *(The paper never-green gap does hold in both halves, +29 pp and
+50 pp — recorded, n = 2 and n = 7, refused a rank.)*

## 3c. CONTROL (c) — REGIME SPLIT, BOTH LEGS POPULATED · ☠️ **FAILS**

Book regimes: **LIVE TREND 17 / FLAT 6 · PAPER TREND 39 / FLAT 4 / unrecorded 9.**

| book | TREND | FLAT | verdict |
|---|---|---|---|
| LIVE | n = 2, mean −0.665 | n = 2, mean −1.173 | 🟡 both legs populated, same sign — **but n = 2 per leg** |
| PAPER | n = 8, mean −0.435 | 🔴 **n = 0 — EMPTY** | ☠️ **the control cannot be run** |

☠️ **CONTROL (c) FAILS. THE PAPER FLAT LEG IS EMPTY — not small, EMPTY.** Not one of the name's 9 paper rows
carries `market_regime = 'FLAT'` (8 TREND, 1 unrecorded), and the paper book holds only **4 FLAT rows in
total** across all 52 positions. 🔴 **As the brief requires: an empty leg is a FAILED control, and it is
reported as a failure rather than as a one-legged result.** Across all 23 names the split runs on only
**5 of 9 live** and **3 of 14 paper** cells.

## 3d. CONTROL (d) — PAPER AS THE INDEPENDENT SAMPLE · 🟢 **PASSES ON SIGN**

**This control killed candidates 21, 22, 29 and 30. It does not kill this one.**

| name | LIVE mean R | PAPER mean R | LIVE medMFE | PAPER medMFE | LIVE never-green | PAPER never-green | agree? |
|---|---|---|---|---|---|---|---|
| 🔴 **`Bullish OB Created`** | **−0.919** | **−0.512** | **+0.152** | **+0.096** | **75 %** | **67 %** | 🟢 **ALL THREE** |
| `Within Bullish OB` | −0.113 | −0.276 | +0.772 | +0.290 | 33 % | 29 % | 🟢 sign holds |
| `Within Bearish OB` | −0.059 | −0.399 | +0.137 | +0.791 | 75 % | 33 % | 🟡 R holds, MFE inverts |
| `Bullish I-CHOCH+` | +1.137 | +0.268 | +1.463 | +0.811 | 0 % | 0 % | 🟢 sign holds |
| `Bullish OB Mitigated` | −1.123 | −0.130 | +0.015 | +0.590 | 100 % | 0 % | 🟡 R holds, MFE inverts |
| `Bearish OB Created` | −0.094 | **+0.826** | +0.544 | +2.067 | 0 % | 0 % | ☠️ **R INVERTS** |
| `Bearish I-BOS` | −0.014 | **+0.947** | +0.497 | +2.310 | 0 % | 20 % | ☠️ **R INVERTS** |
| `Bearish I-CHOCH+` | −0.217 | **+1.974** | +0.030 | +2.981 | 100 % | 0 % | ☠️ **R INVERTS** |

> ### 🟢 **CONTROL (d) PASSES FOR `Bullish OB Created` — on mean R, on median MFE AND on the never-green share, both books. It is the first candidate in this series to survive the paper test.**
> 8 of the 9 live names exist on paper; **`Bullish I-BOS` is live-only (n = 2) and has no independent sample
> at all.** Three names invert outright and are dead on arrival.

## 3e. CONTROL (e) — THE CONFOUND · ⚖️ **SPLIT: THE SCORE IS CLEARED, THE ERA IS CLEARED, THE SIDE IS TOTAL**

**(i) IS THE NAME THE SCORE IN DISGUISE? 🟢 NO — and this is the one place it differs from candidate 30.**

| | ρ(name-as-dummy, `confluence_score`) | p | mean score vs rest |
|---|---|---|---|
| LIVE `Bullish OB Created` | **+0.340** | 0.1205 | 5.375 vs 4.211 |
| PAPER `Bullish OB Created` | **−0.140** | 0.3258 | 3.889 vs 4.297 |
| *largest \|ρ\| anywhere in the family* | **0.340** (live) · **0.188** (paper) | — | — |

> 🔴 **Candidate 30 died at ρ(count, score) = +0.92. Here the largest |ρ| in the entire 23-cell family is
> 0.340, the two books carry OPPOSITE SIGNS, and not one of the 23 is significant at any threshold.**
> On live the name's rows **share score values with the rest of the book** (candidate 30's count bands shared
> none). **THE TRIGGER NAME IS NOT THE SCORE. That part of the confound is genuinely cleared.**

**(ii) IS THE NAME CONFINED TO ONE ERA? 🟢 NO.**
`Bullish OB Created` spans **2026-08-23 → 2026-09-13 = 21.2 d of the live book's 46 d (46 %)** and
**2026-05-26 → 2026-07-29 = 64.0 d of the paper book's 67 d (95 %)**. It is spread across both books.
*(Names that ARE era-confined, recorded so no later pass reads them as clean: LIVE `Within Bearish OB`
**1.6 d, 3 % of the book — all four rows inside 2026-07-30/31**, `Bearish I-BOS`, `Bullish I-CHOCH+`,
`Bullish OB Mitigated`, `Bullish I-BOS`; PAPER `Bearish OB Entered`, `Bullish S-BOS`, and five singletons.)*

**(iii) 🔴 IS THE NAME THE SIDE? ☠️ TOTALLY, AND THIS IS WHERE IT DIES.**

**75 of 75 rows: `Bullish*` → LONG, `Bearish*` → SHORT. Zero exceptions. ρ(name, side) = ±1 by
construction.** The books themselves carry a large side effect:

| book | LONG | SHORT | LONG vs SHORT mean R |
|---|---|---|---|
| LIVE | n = 14, ΣR **−4.308**, mean −0.308, medMFE +0.512 | n = 9, ΣR −0.872, mean −0.097, medMFE +0.175 | Δ −0.211, **p = 0.5025** |
| PAPER | n = 24, ΣR **−6.779**, mean −0.282, medMFE +0.404 | n = 28, ΣR **+5.363**, mean +0.192, medMFE +0.879 | Δ −0.474, **p = 0.0673** |

**The only partial escape is to test the name against the REST OF ITS OWN SIDE.** It does not dissolve the
effect — but it does not rescue it either:

| book | name vs same-side rest | mean R | p | never-green | p |
|---|---|---|---|---|---|
| LIVE | −0.919 (n=4) vs −0.063 (n=10 other LONGs) | Δ −0.856 | **0.0461** | 75 % vs 30 % | 0.2432 |
| PAPER | −0.512 (n=9) vs −0.145 (n=15 other LONGs) | Δ −0.367 | 0.1600 | **67 % vs 13 %** | **0.0213** |

> ☠️ **Both within-side p-values (0.0461 and 0.0213) are above α = 2.174 × 10⁻³ — 21× and 10× too large.**
> The name survives its own side in *direction* on both books and in neither case in *significance*. **On a
> 75-row book where every name maps to exactly one side, "this name is bad" and "LONG is bad" are the same
> hypothesis, and this book cannot tell them apart.** 🔴 **Note the shape of the trap: on paper the very same
> structural event is the WORST cell on the LONG side (`Bullish OB Created`, −4.607R) and among the BEST on
> the SHORT side (`Bearish OB Created`, +4.957R).**

---

# 4. VERDICT

## ☠️ **CANDIDATE 31: NO TRIGGER NAME CAN BE CONVICTED. THE LINE CLOSES.**

> ### 🔴 **STATED AT THE TOP, PLAINLY, AS THE BRIEF REQUIRES: n CANNOT RANK THIS ON THE LIVE BOOK.**
> **ZERO of the 9 live trigger names reaches n = 8.** The live cells are 6, 4, 4, 2, 2, 2, 1, 1, 1. Paper
> can rank exactly **2 of 14**. **The descriptive tables in §1c, §2a, §2c and §2e are given in full anyway —
> the operator asked to see which names fired the dead entries even where the sample cannot convict them,
> and §2c answers that by name, position by position.**

| control | result |
|---|---|
| **a. Bonferroni** (α = 2.174 × 10⁻³ / 8.333 × 10⁻⁴) | ☠️ **FAILS.** Smallest p in the whole 23-cell family **0.0091** — 4.2× / 10.9× too large. `Bullish OB Created`'s best is 0.0116. Every LIVE p ≥ 0.0254. |
| **b. Chronological halves** | ☠️ **FAILS.** Same sign in all four halves on the crude reading — but vs the rest of its own half the paper H2 effect is **Δ −0.0006R (gone)**, and the live never-green signal **inverts** (−50 pp → +67 pp). |
| **c. Regime, both legs populated** | ☠️ **FAILS.** **PAPER FLAT leg EMPTY** (0 of 9 rows); paper holds 4 FLAT rows in total. Live legs are n = 2 each. |
| **d. 🔴 Paper as the independent sample** | 🟢 **PASSES ON SIGN** — mean R, median MFE and never-green all agree across books. **The first candidate in the series to survive this.** But the live leg is **n = 4**. |
| **e. 🔴 The confound** | ⚖️ **SPLIT.** 🟢 **SCORE CLEARED** (max \|ρ\| 0.340, opposite signs across books, none significant — candidate 30 died at +0.92). 🟢 **ERA CLEARED** (46 % / 95 % of book span). ☠️ **SIDE IS TOTAL: 75/75 rows, ρ = ±1 by construction.** |

**THREE OF FIVE FAIL. The survival rule requires ALL FIVE. `Bullish OB Created` does not survive, and no other
name gets as far.**

## 🔴 4a. THE ANSWER THE OPERATOR ASKED FOR, GIVEN PLAINLY BECAUSE THE SAMPLE CANNOT GIVE THE OTHER ONE

> ### **WHICH SIGNAL NAME FIRED THE DEAD ENTRIES? FIVE NAMES DID — 3 / 3 / 2 / 2 / 1 — AND NO SINGLE NAME CARRIES MOST OF THEM BY COUNT.**
> `Within Bearish OB` (3) · **`Bullish OB Created` (3)** · `Within Bullish OB` (2) · `Bearish I-CHOCH+` (2) ·
> `Bullish OB Mitigated` (1).
>
> ### 🔴 **BY MONEY, AND IN THE MIRROR, ONE NAME SEPARATES: `Bullish OB Created`.**
> **4 live entries · 0 winners · 0 ever reached +1R · best MFE +0.560R · median MFE +0.152R · 3 of 4 never
> green · ΣR −3.6745.** On the independent paper book the **same sign on all three measures** — n = 9,
> −4.6067R, 11 % win rate, median MFE +0.096R, 67 % never green. **1 winner in 13 positions across both
> books.** It is the **only** name that fired dead entries and appears **nowhere** among the four live
> positions that reached +1R.
>
> ### ☠️ **AND IT STILL CANNOT BE CONVICTED, FOR FOUR SEPARATE REASONS, ANY ONE OF WHICH WOULD BE ENOUGH.**
> **n = 4 on live.** · **p = 0.0116 at best against α = 0.0022.** · **The paper FLAT leg is empty and the
> paper mean-R effect vanishes in the half that holds 7 of its 9 rows.** · **Its name is `Bullish`, so
> nothing in this book separates the trigger from the direction.**

## 🔴 4b. WHAT UNSUBSCRIBING WOULD HAVE COST — on the record, **NOT a proposal, and no diff is written**

The brief asks for this only if a name survives all five controls. **None did.** The table is a cost
statement for a subtraction **nobody should make on this evidence.**

| book | drop `Bullish OB Created` | volume lost | ΣR would go | Δ |
|---|---|---|---|---|
| **LIVE** | −4 of 23 entries | **17.4 %** | **−5.1796 → −1.5051** | **+3.6745** |
| **PAPER** | −9 of 52 entries | **17.3 %** | **−1.4165 → +3.1902** | **+4.6067** |

🟡 **NEW IN THIS EDITION — A FRAMING WARNING, SO THE HEADLINE NUMBER IS NOT MIS-CARRIED.** The 19:00 and
20:15 editions quote **"−3.6745R = 70.9 % of the entire live book's loss."** That arithmetic is correct —
3.6745 / 5.1796 — but it is a share of the book's **NET** result, and a net denominator near zero makes the
percentage explode. **The identical statistic on paper is 325 %**, because the paper book nets to −1.4165R.
**The stable framing is the share of GROSS losses: `Bullish OB Created` is 37.3 % of the −9.8564R live gross
loss and 23.5 % of the −19.6010R paper gross loss, on ~17 % of the volume in both books.** Both framings
are true; only the second one can be compared between books, and it is the one later passes should cite.

🔴 **AND THE LINE DIRECTLY BENEATH IT, WHICH IS WHY NO DIFF IS WRITTEN.** The same subtraction applied to
names that look similar by count **destroys** the book:

| book | drop | volume lost | ΣR would go |
|---|---|---|---|
| PAPER | `Bearish OB Created` | 11.5 % | −1.4165 → ☠️ **−6.3730** |
| PAPER | `Bearish I-BOS` | 9.6 % | −1.4165 → ☠️ **−6.1533** |
| LIVE | `Within Bearish OB` | 17.4 % | −5.1796 → −4.9437 — **and it costs vpos 89, +1.386R, the best trade on the book** |

**Unsubscribing from a name is a subtraction with no threshold to soften it.** On a book where the same
structural event is the worst cell on one side and among the best on the other, a 4-position live sample is
not a licence to remove a fifth of the volume.

## 🔴 4c. WHAT THIS DOES **NOT** ADDRESS — named before anyone asks

**The four live positions that peaked above +0.5R and still finished negative — ΣR −1.7167 — are an EXIT
question, not a trigger question. No trigger name in this file touches them:**

| vpos | side | trigger | MFE | realised R | closed by |
|---|---|---|---|---|---|
| 87 | LONG | `Within Bullish OB` | +0.615 | −0.440 | `ai_exit` |
| 91 | SHORT | `Bearish OB Created` | +0.661 | −0.484 | `ai_exit` |
| 95 | LONG | 🔴 `Bullish OB Created` | +0.560 | −0.533 | `external` |
| 98 | LONG | `Within Bullish OB` | +0.929 | −0.260 | `ai_exit` |

**Three different names, three of the four closed by three different mechanisms.** These positions had money
on the table and gave it back — that is the `§0.EXIT-ADVISOR-RULE` ledger's business (**5 resolved of 10,
Σ +1.0497R, POSITIVE — it does not fire**), not a trigger's. **Note also that vpos 95 is a
`Bullish OB Created` row: even the one named candidate owns one of the four exit-class losses, so removing
the name would not have been a clean subtraction of dead entries only.**

## 🔴 4d. RECORDED: THE LINE CLOSES

**CANDIDATE 31 — "is a particular TRIGGER NAME worth listening to at all?" — is recorded as CLOSED.**
It is the **31st consecutive candidate to fail its controls**, and the **first** to fail while passing the
paper test. **It does not close flat**, and the difference is worth recording for whoever opens candidate 32:

* **Candidates 21, 22, 29, 30 died on PAPER** — the sign inverted on the independent book.
* **Candidate 30 died on the SCORE** — the count was the score at ρ = +0.92.
* 🔴 **Candidate 31 dies on the SIDE and on n.** The score is cleared. The era is cleared. Paper agrees.
  **What is left is 4 live positions and a name that is perfectly collinear with its own direction.**

**The one thing that WOULD settle it is time, not cleverness: `Bullish OB Created` needs n ≥ 8 on the live
book and a populated FLAT leg on paper. It stands at 4 and 0.** Until then it is a **watched name, not a
convicted one.** 📋 **Nothing is proposed. No diff is written. No config value is touched.**

---

## 🔴 SAFETY CONFIRMATION — every item the brief demanded, verified, not asserted

| item | state | how verified |
|---|---|---|
| `openitems_guard` | ✅ **EXIT = 0**, header and current-state table agree with runtime, 14 watched values | run first, before anything else |
| Titan DB access | ✅ **`file:trades.db?mode=ro` URI + `PRAGMA query_only=1` on every connection** | `PRAGMA query_only` read back → **1** |
| writes / orders / restarts | ✅ **NONE.** Zero DML, zero venue calls, zero service commands issued | only `SELECT` and `PRAGMA table_info` were executed |
| `titan.service` NRestarts | ✅ **0**, `running`, active since **2026-09-12 14:58:32 UTC** — unchanged | `systemctl show -p NRestarts` |
| `mercury-sol.service` NRestarts | ✅ **0**, `running`, active since **2026-09-14 22:20:45 UTC** — unchanged | `systemctl show -p NRestarts` |
| 🔴 **Mercury-SOL** | ✅ **UNTOUCHED — not one byte.** No file read, no DB query, no restart, no venue call on its key | the only Mercury-SOL command in this session was the read-only `systemctl show -p NRestarts` the brief itself demanded |
| `EXIT_ADVISOR_DRYRUN` | ✅ **False** (`config.py:335`) | read, not modified |
| `BOOK_GATE_DRYRUN` | ✅ **False** (`config.py:1072`) | read, not modified |
| `BOOK_GATE_CLAUSE_B_ENABLED` | ✅ **False** (`config.py:1078`) | read, not modified |
| book-gate counter | ✅ **29 / 200** — untouched | `count(*) where book_gate_opp_pctl is not null` = 29 |
| commit | ✅ **`f16c271`**, working tree **clean** | `git rev-parse` + `git status --porcelain` empty |

**Provenance.** `virtual_positions` joined to `trades` on `trades_entry_row_id`. Trigger name from
`trades.tv_action`, cross-validated against `entry_tiers_json.tiers.5m.name` on 24/24 rows. Tier names,
`counted_by_gate` and `not_counted` from `entry_tiers_json`. `market_regime` and `confluence_score` from the
same entry row. R = `net_pnl / initial_risk_usdt`; MFE/MAE from `water_mark` / `max_adverse_price` against
`original_sl_price`. **All 23 live MFE/MAE/R reproduce the 2026-09-16 15:20 §3a table to the digit.**
Spearman ρ and all p-values are two-sided permutation Monte Carlo, 100 000–200 000 draws, seed **20260916**,
`numpy` 2.2.6 (`scipy` is not installed on this box). **Live ΣR −5.1796 · live losers 17, ΣR −9.8564 ·
never-green 11, ΣR −7.5805 — all three reconcile exactly with the 15:20 report.**

**Supersedes nothing.** The `2026-09-16-1900` and `2026-09-16-2015` editions stand on the record unaltered;
this file is a third independent confirmation of them plus the three additions flagged 🟡 above.
