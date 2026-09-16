# Titan — **candidate 31, INDEPENDENTLY RE-VERIFIED FROM THE DB. Every number reproduces to the digit; TWO factual errors in the 19:00 edition are corrected here.** 🔴 The verdict is unchanged: **ZERO of the 9 live trigger names reaches n = 8**, the eleven never-green losers were fired by **FIVE different names**, and **`Bullish OB Created` — 4 entries, 17.4 % of live volume — carries ΣR −3.6745 = 70.9 % of the entire live book's loss**, same sign on paper (n = 9, −4.6067R). It is **NOT the score** (ρ ≈ 0) — it **IS the side** (15 of 15 names map to one side). **It still cannot be convicted.** No unsubscription proposed. No diff.

**2026-09-16 20:15 UTC · published 16:15 UTC · commit `f16c271` · Titan LIVE REAL MONEY · READ-ONLY PASS · Mercury-SOL NOT TOUCHED** · `openitems_guard` **EXIT=0**

> ## 🔴 WHAT THIS EDITION IS, IN ONE PARAGRAPH
> The 19:00 edition of this pass was published but **never verified by a second, independent read of the
> database.** This edition is that read. **Every population count, every ΣR, every per-name cell, all 23 live
> MFEs, the eleven never-green losers and their names, the four +1R mirrors, both side tables, every Spearman
> ρ and every permutation p was recomputed from `trades.db` from scratch in a separate session and compared
> against the published text.** Result: **the analysis stands — and two statements in it were wrong.** Both
> are corrected in place below, flagged 🔴 **CORRECTION 1 OF 2** (§ population) and 🔴 **CORRECTION 2 OF 2**
> (§3a). **Neither moves the verdict.** One was a mislabelled vpos range; the other understated how small the
> smallest live p was. **This file supersedes the 19:00 edition, which is left on the record unaltered.**

**Basis:** my own `2026-09-16-1520` §3b(i) (11 of 17 live losers never printed +0.25R, −7.5805R = 77 % of all live losses; zero losers ever reached +1R; every large loser peaked in the first 1–7 % of its life) and `2026-09-16-1730` (candidate 30, whose five-control frame this pass adopts verbatim).

---

## 🔴 WHY THIS IS NOT THE THIRTY-FIRST FILTER — AND WHY IT IS NOT THE 2026-08-19 PASS EITHER

Candidates 1–30 each asked *"given this signal, should we enter?"* — a **CONDITION bolted on top of the
trigger**. This pass asks whether a particular **TRIGGER NAME** is worth subscribing to at all. A filter is
a rule; unsubscribing is a **subtraction**. Different object, and the second has never been examined on the
book.

> ### 🔴 AND THE THING THAT MUST NOT BE CONFLATED, STATED BEFORE ANY NUMBER
> The **2026-08-19 23:30** pass (`reports/2026-08-19-2330-titan-sol-signal-set-has-no-edge.md`) measured
> **48 name cells on 32 246 raw SIGNALS** — 17 861 Titan + 14 385 SOL — scoring each name by **where price
> went afterwards**, and found **0 of 48 significant even without correction**. Its Bonferroni was α = 0.00104.
>
> **THAT MEASURED SIGNALS. THIS MEASURES POSITIONS.** Here the population is the **75 closed positions** that
> a signal actually became, the outcome is the position's **own realised R and its own MFE excursion**, and
> the sample is **three orders of magnitude smaller**. The 08-19 result is not re-run, not re-used, and does
> not license anything below; equally, nothing below overturns it. **They are different questions on
> different populations and neither answers the other.**

---

## 🔴 CONTROLS, DECLARED IN THE HEADER — BEFORE ANY RESULT

* **Bonferroni over every name × side × book.** 15 distinct names × 2 sides × 2 books = **60 nominal cells**,
  of which **23 are populated** (LIVE 9 + PAPER 14). **α_populated = 0.05 / 23 = 2.174 × 10⁻³**;
  **α_full-grid = 0.05 / 60 = 8.333 × 10⁻⁴.** Survival requires the stricter.
  🔴 *The name × side half of that grid is structurally degenerate — see §3e: a name determines its side
  exactly, so 30 of the 60 cells can never be occupied. Both α are reported so nobody can pick the kind one.*
* **A cell is ranked only if n ≥ 8.** Below that it is printed and **refused a rank**, never folded into a neighbour.
* **Survival requires ALL FIVE:** p < α · same sign in both chronological halves of each book · same sign in
  TREND and FLAT **with both legs populated** · **same sign on paper and live** · and it must not be the
  **score**, the **side**, or the **era** in disguise.
* **Paper and live are NEVER pooled.** R = `net_pnl / initial_risk_usdt`.
  MFE in R = `(water_mark − entry) / (entry − original_sl_price)`, sign-flipped for SHORT.

**Population: 75 closed positions — 23 LIVE (vpos 86–108), 52 PAPER (vpos 34–85).** vpos 33 excluded (NULL
`initial_risk_usdt`); **vpos 27–32 are the 6 `archived_pre_geometry_fix` rows and are not in the closed set.**
Identical to the 15:20 and 17:30 passes.

> 🔴 **CORRECTION 1 OF 2 vs the 19:00 edition, which printed the paper range as "vpos 27–85".** The closed
> paper population begins at **vpos 34**, not 27: 27–32 are archived and 33 is the NULL-risk exclusion.
> **No number anywhere in either edition changes** — the same 52 rows were always in the set; only the
> printed range label was wrong.

> **THE STAND WAS VALIDATED BEFORE IT WAS TRUSTED.** Rebuilt from the DB it reproduces the 15:20 report
> exactly: LIVE ΣR **−5.1796** / PAPER **−1.4165**; every close-reason cell (live `ai_exit` 15 / −0.9063,
> `sl` 4 / −4.4910, `trail` 2 / +1.2821, `external` 2 / −1.0644; paper `sl` 27 / −18.7323, `trail`
> 14 / +16.2901, `external` 10 / +1.0108, `post_entry_critical` 1 / +0.0150); and **all 23 live MFEs to the
> digit** (median LIVE 0.427R, PAPER 0.731R; 4 of 23 and 17 of 52 reach +1R). That, and only that, licenses
> the numbers below.

---

# 🔴 n FIRST, BEFORE ANY RESULT. READ THIS BEFORE THE NUMBERS.

> ## ☠️ **NOT ONE LIVE TRIGGER NAME REACHES n = 8. ZERO RANKABLE CELLS OF NINE. The largest is n = 6.**
> **The live book cannot rank this question, and I am saying so at the top exactly as the brief demands.**
> Two cells in the entire study reach n = 8, and **both are on PAPER**:
> `Within Bearish OB` (n = 12) and `Bullish OB Created` (n = 9).
> **Everything in §2 that cites a live name is a DESCRIPTION, not a ranking.** The descriptive table is
> given anyway, in full, because the operator needs to see which names fired the dead entries even when the
> sample cannot convict them.

| | LIVE | PAPER |
|---|---|---|
| distinct trigger names | **9** | **14** |
| cells reaching n ≥ 8 | 🔴 **0 of 9** | **2 of 14** |
| largest cell | `Within Bullish OB`, **n = 6** | `Within Bearish OB`, **n = 12** |

---

# 1. NAME EVERY ENTRY'S TRIGGER

## 1a. WHERE THE NAME COMES FROM — READ, NOT INFERRED

The **5m trigger name** is `trades.tv_action` on the position's own entry row
(`virtual_positions.trades_entry_row_id` → `trades.id`). The **1H and 15m tier names** are
`entry_tiers_json → tiers['1H'].name` and `tiers['15m'].name`.

🔴 **THE TWO SOURCES WERE RECONCILED BEFORE EITHER WAS USED.** On every one of the **24 rows that carry
`entry_tiers_json`**, `tiers['5m'].name` equals `tv_action` — **24 of 24, zero mismatches**. That is what
licenses using `tv_action` as the 5m trigger name on the rows that have no tier JSON.

## 1b. 🔴 THE COVERAGE LIMIT, STATED UP FRONT AND EXACTLY

`entry_tiers_json` begins **2026-07-29**. The paper book ran **2026-05-23 → 2026-07-29**; the live book
**2026-07-30 → 2026-09-14**. So:

| | LIVE (n = 23) | PAPER (n = 52) |
|---|---|---|
| **5m trigger name** (`tv_action`) | 🔴 **23 of 23 = 100 %** | 🔴 **52 of 52 = 100 %** |
| **1H tier name** (`entry_tiers_json`) | **23 of 23** | ☠️ **1 of 52** |
| **15m tier name** (`entry_tiers_json`) | **22 of 23** *(vpos 100 has no 15m tier at all)* | ☠️ **1 of 52** |
| any `entry_tiers_json` at all | 23 of 23 | ☠️ **1 of 52 — vpos 85 only** (2026-07-29 13:50) |

> ### 🔴 THEREFORE: THE QUESTION THE BRIEF ASKS — *which trigger name fired the entry* — IS ANSWERABLE ON **75 OF 75** ROWS, BOTH BOOKS, IN FULL.
> **The 1H / 15m tier names beside it are a LIVE-ONLY column.** `matrix_breakdown_json` is present on all 75
> but carries **points only, never names** — it cannot fill the gap. **No paper 1H or 15m name is stated
> anywhere below except vpos 85's, and no later pass may read the paper book as if it had them.**

## 1c. DISTRIBUTION OF TRIGGER NAMES, PER BOOK, PER SIDE

### LIVE — 9 names over 23 positions

| trigger name | side | n | vpos |
|---|---|---|---|
| `Within Bullish OB` | LONG | **6** | 87, 92, 94, 98, 99, 100 |
| `Within Bearish OB` | SHORT | **4** | 86, 88, 89, 90 |
| `Bullish OB Created` | LONG | **4** | 95, 97, 102, 107 |
| `Bearish OB Created` | SHORT | 2 | 91, 101 |
| `Bearish I-CHOCH+` | SHORT | 2 | 93, 106 |
| `Bullish I-BOS` | LONG | 2 | 96, 104 |
| `Bullish OB Mitigated` | LONG | 1 | 103 |
| `Bearish I-BOS` | SHORT | 1 | 105 |
| `Bullish I-CHOCH+` | LONG | 1 | 108 |

**LIVE LONG n = 14** over 5 names · **LIVE SHORT n = 9** over 4 names.

### PAPER — 14 names over 52 positions

| trigger name | side | n | | trigger name | side | n |
|---|---|---|---|---|---|---|
| `Within Bearish OB` | SHORT | **12** | | `Bearish OB Entered` | SHORT | 2 |
| `Bullish OB Created` | LONG | **9** | | `Bullish OB Mitigated` | LONG | 2 |
| `Within Bullish OB` | LONG | 7 | | `Bullish S-BOS` | LONG | 2 |
| `Bearish OB Created` | SHORT | 6 | | `Bullish OB Entered` | LONG | 1 |
| `Bearish I-BOS` | SHORT | 5 | | `Bearish I-CHOCH+` | SHORT | 1 |
| `Bullish I-CHOCH+` | LONG | 2 | | `Bearish OB Mitigated` | SHORT | 1 |
| | | | | `Bearish S-CHOCH+` | SHORT | 1 |
| | | | | `Bullish S-CHOCH` | LONG | 1 |

**PAPER LONG n = 24** over 7 names · **PAPER SHORT n = 28** over 7 names.

---

# 2. OUTCOMES BY TRIGGER NAME

## 2a. THE MASTER TABLE. **Live and paper NEVER pooled. n is in the second column, before every result.**

### 🔴 LIVE (n = 23) — **NOT ONE ROW IS RANKED**

| trigger name | **n** | ΣR | mean R | win rate | **median MFE** | mean MFE | 🔴 **never +0.25R** | ever ≥ +1R | rank? |
|---|---|---|---|---|---|---|---|---|---|
| `Within Bullish OB` | 6 | −0.6773 | −0.113 | 2/6 | 0.772 | 0.788 | 2/6 = 33 % | 2/6 | ☠️ n<8 |
| `Within Bearish OB` | 4 | −0.2359 | −0.059 | 1/4 | 0.137 | 0.512 | 3/4 = 75 % | 1/4 | ☠️ n<8 |
| 🔴 **`Bullish OB Created`** | **4** | 🔴 **−3.6745** | 🔴 **−0.919** | **0/4 = 0 %** | **0.152** | 0.216 | 🔴 **3/4 = 75 %** | **0/4** | ☠️ n<8 |
| `Bearish OB Created` | 2 | −0.1888 | −0.094 | 1/2 | 0.544 | 0.544 | 0/2 = 0 % | 0/2 | ☠️ n<8 |
| `Bearish I-CHOCH+` | 2 | −0.4334 | −0.217 | 0/2 | 0.030 | 0.030 | 2/2 = 100 % | 0/2 | ☠️ n<8 |
| `Bullish I-BOS` | 2 | +0.0302 | +0.015 | 1/2 | 0.592 | 0.592 | 0/2 = 0 % | 0/2 | ☠️ n<8 |
| `Bullish OB Mitigated` | 1 | −1.1235 | −1.123 | 0/1 | 0.015 | 0.015 | 1/1 = 100 % | 0/1 | ☠️ n<8 |
| `Bearish I-BOS` | 1 | −0.0136 | −0.014 | 0/1 | 0.497 | 0.497 | 0/1 = 0 % | 0/1 | ☠️ n<8 |
| `Bullish I-CHOCH+` | 1 | +1.1371 | +1.137 | 1/1 | 1.463 | 1.463 | 0/1 = 0 % | 1/1 | ☠️ n<8 |

### PAPER (n = 52) — **two rows ranked**

| trigger name | **n** | ΣR | mean R | win rate | **median MFE** | mean MFE | 🔴 **never +0.25R** | ever ≥ +1R | rank? |
|---|---|---|---|---|---|---|---|---|---|
| `Within Bearish OB` | **12** | −4.7875 | −0.399 | 5/12 | 0.791 | 0.706 | 4/12 = 33 % | 2/12 | ✅ ranked |
| 🔴 **`Bullish OB Created`** | **9** | 🔴 **−4.6067** | 🔴 **−0.512** | 1/9 = 11 % | 🔴 **0.096** | 0.458 | 🔴 **6/9 = 67 %** | 1/9 | ✅ ranked |
| `Within Bullish OB` | 7 | −1.9297 | −0.276 | 2/7 | 0.290 | 0.497 | 2/7 = 29 % | 2/7 | ☠️ n<8 |
| `Bearish OB Created` | 6 | **+4.9565** | **+0.826** | 4/6 | **2.067** | 1.863 | 0/6 = 0 % | 5/6 | ☠️ n<8 |
| `Bearish I-BOS` | 5 | **+4.7368** | **+0.947** | 3/5 | **2.310** | 1.972 | 1/5 = 20 % | 3/5 | ☠️ n<8 |
| `Bullish I-CHOCH+` | 2 | +0.5363 | +0.268 | 2/2 | 0.811 | 0.811 | 0/2 | 0/2 | ☠️ n<8 |
| `Bearish OB Entered` | 2 | −1.0731 | −0.537 | 1/2 | 0.316 | 0.316 | 1/2 | 0/2 | ☠️ n<8 |
| `Bullish OB Mitigated` | 2 | −0.2601 | −0.130 | 1/2 | 0.590 | 0.590 | 0/2 | 0/2 | ☠️ n<8 |
| `Bullish S-BOS` | 2 | −1.1895 | −0.595 | 0/2 | 0.588 | 0.588 | 0/2 | 0/2 | ☠️ n<8 |
| `Bullish OB Entered` | 1 | +0.1677 | +0.168 | 1/1 | 1.290 | — | 0/1 | 1/1 | ☠️ n<8 |
| `Bearish I-CHOCH+` | 1 | +1.9743 | +1.974 | 1/1 | 2.981 | — | 0/1 | 1/1 | ☠️ n<8 |
| `Bearish OB Mitigated` | 1 | +0.1164 | +0.116 | 1/1 | 1.163 | — | 0/1 | 1/1 | ☠️ n<8 |
| `Bearish S-CHOCH+` | 1 | −0.5604 | −0.560 | 0/1 | 0.014 | — | 1/1 | 0/1 | ☠️ n<8 |
| `Bullish S-CHOCH` | 1 | +0.5026 | +0.503 | 1/1 | 1.591 | — | 0/1 | 1/1 | ☠️ n<8 |

## 2b. 🔴 THE TEST THAT MATTERS — **MFE AND THE NEVER-GREEN SHARE, NOT FINAL R**

Two-sided permutation, 40 000 shuffles, seed 20260916. **Only the two n ≥ 8 cells are tested against the rest
of their own book; everything else is refused a rank.**

| book | name | n vs rest | Δ mean R | p | Δ median MFE | p | 🔴 **Δ never-green share** | 🔴 **p** |
|---|---|---|---|---|---|---|---|---|
| PAPER | 🔴 **`Bullish OB Created`** | 9 vs 43 | −0.586 | 0.0863 | **−0.710** | **0.0432** | 🔴 **+0.457** | 🔴 **0.0120** |
| PAPER | `Within Bearish OB` | 12 vs 40 | −0.483 | 0.1184 | +0.136 | 0.7771 | +0.058 | 0.7274 |

> ### ☠️ **THE BEST p ANYWHERE IN THE FAMILY IS 0.0120, AGAINST α = 2.174 × 10⁻³.** It is **5.5× too large**
> against the populated-cell α and **14.4× too large** against the full-grid α = 8.333 × 10⁻⁴.
> **`Within Bearish OB` — the single largest cell in the study — shows NOTHING on the test that matters
> (Δ never-green +0.058, p = 0.727).** The volume is not where the signal is.

## 2c. 🔴🔴 **WHICH NAMES FIRED THE ELEVEN NEVER-GREEN LIVE LOSERS**

| vpos | side | 🔴 **5m TRIGGER** | 1H tier | 15m tier | MFE | R | closed by | score |
|---|---|---|---|---|---|---|---|---|
| 86 | SHORT | `Within Bearish OB` | Smart Trail Bearish | HyperWave Signal Down | 0.099 | −1.022 | `sl` | 5.75 |
| 88 | SHORT | `Within Bearish OB` | Smart Trail Bearish | Reversal Up + | 0.076 | −0.296 | `ai_exit` | 2.50 |
| 90 | SHORT | `Within Bearish OB` | Smart Trail Bearish | HyperWave Signal Down | 0.175 | −0.304 | `ai_exit` | 2.25 |
| 92 | LONG | `Within Bullish OB` | Smart Trail Bullish | HyperWave Signal Down | 0.001 | −0.728 | `ai_exit` | 4.25 |
| 93 | SHORT | `Bearish I-CHOCH+` | Trend Catcher Down | HyperWave Signal Down | 0.000 | −0.137 | `ai_exit` | 6.50 |
| 97 | LONG | 🔴 **`Bullish OB Created`** | Bullish Confirmation+ | Reversal Down | 0.116 | −0.796 | `ai_exit` | 5.00 |
| 99 | LONG | `Within Bullish OB` | Trend Catcher Up | HyperWave Signal Up | 0.060 | −0.532 | `external` | 5.25 |
| 102 | LONG | 🔴 **`Bullish OB Created`** | Smart Trail **Bearish** | HyperWave Signal Up | 0.188 | −1.158 | `sl` | 4.25 |
| 103 | LONG | `Bullish OB Mitigated` | Any Bullish Confirmation | HyperWave Signal Down | 0.015 | −1.123 | `sl` | 3.75 |
| 106 | SHORT | `Bearish I-CHOCH+` | Any Bearish Confirmation | HyperWave Signal Down | 0.060 | −0.296 | `ai_exit` | 5.00 |
| 107 | LONG | 🔴 **`Bullish OB Created`** | Any Bullish Confirmation | HyperWave Signal Up | 0.000 | −1.187 | `sl` | 5.50 |

> ### 🔴 **NO — ONE OR TWO NAMES DO *NOT* CARRY MOST OF THEM. THE ELEVEN ARE SPREAD OVER FIVE NAMES.**

| name | count of the 11 | ΣR of those | vpos |
|---|---|---|---|
| `Within Bearish OB` | **3** | −1.6221 | 86, 88, 90 |
| 🔴 **`Bullish OB Created`** | **3** | 🔴 **−3.1418** | 97, 102, 107 |
| `Within Bullish OB` | 2 | −1.2597 | 92, 99 |
| `Bearish I-CHOCH+` | 2 | −0.4334 | 93, 106 |
| `Bullish OB Mitigated` | 1 | −1.1235 | 103 |
| **total** | **11** | **−7.5805** | |

🔴 **BUT THE COUNTS ARE THE WRONG RULER, AND THE TWO THREES ARE NOT THE SAME EVENT.**
`Within Bearish OB` put **3 of its 4** positions in the never-green set — and its fourth is **vpos 89, the
best short on the book (+1.386R, MFE +1.697R)**. `Bullish OB Created` put **3 of its 4** in — and its fourth,
**vpos 95, also lost** (−0.533R, MFE 0.560R). **`Bullish OB Created` is the only live name that is 0-for-n,
never reached +1R once, and carries three of the four dead entries by a factor of two in R.**

> ## 🔴 THE SINGLE MOST STRIKING NUMBER IN THIS PASS
> **`Bullish OB Created`: 4 entries — 17.4 % of live volume — carrying ΣR −3.6745 of the live book's
> −5.1796 = 70.9 % OF EVERY R LOST ON LIVE MONEY.** Median MFE **0.152R**. Zero winners. Zero ever reached
> the arm. It contains **two of the four live stop-outs (102, 107)**, and vpos 107 is the never-green
> −1.187R that §3c of the 15:20 report already singled out as the one the book gate came closest to refusing.
> ☠️ **AND ITS n IS 4. IT IS REFUSED A RANK, AS DECLARED.**

## 2d. 🔴 STATED AT THE TOP, REPEATED HERE, AS THE BRIEF DEMANDS

> **THE LIVE BOOK CANNOT RANK THIS QUESTION. ZERO of its nine trigger names reaches n = 8; the largest is
> n = 6 and the leading suspect is n = 4.** Every live figure in §2a and §2c is a **description**. The paper
> book carries the only two rankable cells in the study, and §3 is where they are put under the controls.

## 2e. THE MIRROR — the four live positions that reached +1R

| vpos | side | 🔴 **5m TRIGGER** | 1H tier | 15m tier | MFE | R | closed by | score |
|---|---|---|---|---|---|---|---|---|
| 89 | SHORT | `Within Bearish OB` | Smart Trail Bearish | HyperWave Signal Down | **1.697** | +1.386 | `ai_exit` | 5.00 |
| 94 | LONG | `Within Bullish OB` | Smart Trail Bullish | Reversal Down | **1.802** | +0.865 | `trail` | 2.25 |
| 100 | LONG | `Within Bullish OB` | Smart Trail Bullish | *(none — no 15m tier)* | **1.322** | +0.417 | `trail` | 6.50 |
| 108 | LONG | `Bullish I-CHOCH+` | Bullish Confirmation+ | HyperWave Signal Up | **1.463** | +1.137 | `ai_exit` | 4.75 |

**Three names: `Within Bullish OB` (2), `Within Bearish OB` (1), `Bullish I-CHOCH+` (1).**

> ### 🔴 AND THIS IS THE FINDING THAT BLUNTS §2c: **THE TWO `Within …` NAMES APPEAR ON BOTH LISTS.**
> `Within Bearish OB` fired **3 of the 11 dead entries AND the single best short on the book**.
> `Within Bullish OB` fired **2 of the 11 dead entries AND half of all the live positions that ever armed**.
> **The two highest-volume live names are exactly the ones that cannot be characterised as good or bad —
> they are on both ends of the distribution.** Only `Bullish OB Created` is one-sided, and only at n = 4.
> 🔴 **`Bullish OB Created` and `Bullish OB Mitigated` are the ONLY live names with ZERO members on the +1R
> list and a majority on the never-green list — n = 4 and n = 1.**

---

# 3. THE FIVE CONTROLS — the same five that killed candidate 30

Applied to **`Bullish OB Created`**, the only name that is worth carrying this far.

## 3a. BONFERRONI — ☠️ **FAILS**

Declared in the header: α_populated = **2.174 × 10⁻³**, α_full-grid = **8.333 × 10⁻⁴**.
**Best p in the entire family: 0.0120** (PAPER, `Bullish OB Created`, never-green share vs the rest of its
book). ☠️ **5.5× and 14.4× too large respectively.** Every other p ≥ 0.0432.

> 🔴 **CORRECTION 2 OF 2 vs the 19:00 edition, which asserted here that "every LIVE p is ≥ 0.0456".**
> **That was wrong, and it was wrong in the direction that flatters the candidate.** 0.0456 is the
> *within-LONG* live mean-R p from §3e. The **whole-book** live permutation was never printed in the 19:00
> edition at all. Measured in this pass, it is:
>
> | LIVE, whole book | `Bullish OB Created` n = 4 vs 19 | Δ | **p** |
> |---|---|---|---|
> | mean R | −0.919 vs −0.079 | **−0.839** | 🔴 **0.0255** |
> | median MFE | 0.152 vs 0.464 | −0.312 | 0.5573 |
> | never-green share | 75 % vs 42 % | +0.329 | 0.3153 |
>
> **The smallest live p in the family is therefore 0.0255, not 0.0456.** It is still **11.7×** the
> populated-cell α and **30.6×** the full-grid α, it still sits on **n = 4**, and the best p anywhere in the
> family is still PAPER's **0.0120**. ☠️ **The verdict does not move — but the sentence was false and is
> corrected rather than left standing.**

☠️ **CONTROL (a) FAILS.**

## 3b. CHRONOLOGICAL HALVES — ⚖️ **SPLIT: holds on paper, flips on live**

Median split by entry timestamp within each book. LIVE H1 = 2026-07-30…08-24 (n = 11), H2 = 08-24…09-14
(n = 12). PAPER H1 = 05-23…06-25 (n = 26), H2 = 06-25…07-29 (n = 26).

| book | half | n | Δ mean R vs rest | 🔴 Δ never-green vs rest | median MFE (name / rest) |
|---|---|---|---|---|---|
| LIVE | H1 | **1** | −0.362 | 🔴 **−0.500 — WRONG SIGN** | 0.560 / 0.319 |
| LIVE | H2 | 3 | −1.070 | **+0.667** | 0.116 / 0.497 |
| PAPER | H1 | 2 | −1.502 | **+0.292** | 0.498 / 1.112 |
| PAPER | H2 | 7 | 🔴 **−0.001 — ZERO** | **+0.504** | 0.096 / 0.579 |

☠️ **CONTROL (b) FAILS ON MEAN R AND IS UNRANKABLE ON THE REST.** On paper the mean-R effect is **entirely
in H1's two rows** — the second half's difference is **−0.001R, i.e. nothing at all**. On live the
never-green sign **inverts** between the halves. **On the never-green test the paper sign does hold in both
halves (+0.292, +0.504) — the one place this candidate survives a control — but the halves are n = 2 and
n = 7, both below the bar, so it is RECORDED, NOT CLAIMED.**

## 3c. REGIME SPLIT, BOTH LEGS POPULATED — ☠️ **FAILS**

| book | name | TREND | FLAT |
|---|---|---|---|
| LIVE | `Bullish OB Created` | n = 2, mean −0.665 | n = 2, mean −1.173 |
| PAPER | `Bullish OB Created` | n = 8, mean −0.435 | 🔴 **n = 0 — EMPTY** |

*(book regimes: LIVE TREND 17 / FLAT 6; PAPER TREND 39 / FLAT 4 / unrecorded 9.)*

☠️ **CONTROL (c) FAILS. The PAPER FLAT leg is EMPTY — not small, EMPTY.** The live legs are populated but
n = 2 each. **A control that runs on one leg is not a control, and I am reporting the failure rather than
the one leg, exactly as the brief instructs.** The paper book has only **4 FLAT positions in total**; the
split cannot be run on it for any name.

## 3d. 🔴 PAPER AS THE INDEPENDENT SAMPLE — ✅ **THE SIGN HOLDS. The first candidate in the series where it does.**

| book | n | mean R (name / rest) | **Δ** | 🔴 never-green (name / rest) | **Δ** | median MFE (name / rest) | volume | ΣR share of book |
|---|---|---|---|---|---|---|---|---|
| **LIVE** | 4 | −0.919 / −0.079 | **−0.840** | **75 % / 42 %** | **+0.330** | 0.152 / 0.464 | 17.4 % | 🔴 **70.9 %** of −5.1796 |
| **PAPER** | 9 | −0.512 / +0.074 | **−0.586** | **67 % / 21 %** | **+0.457** | 0.096 / 0.806 | 17.3 % | −4.6067R on a −1.4165R book |

> ### ✅ **CONTROL (d) PASSES ON SIGN — on mean R, on median MFE, and on the never-green share, both books.**
> This is what killed candidates 21, 22, 29 and 30, and **it does not kill this one.** The name takes the
> same **17 % of volume** on each book and is worse than its own book on every one of the three measures.
> ☠️ **BUT THE LIVE LEG IS n = 4 AND IS REFUSED A RANK. A sign that agrees is not a confirmation when one
> of the two legs cannot be ranked at all — it is one unranked leg agreeing with one ranked one.**

## 3e. 🔴🔴 THE CONFOUND — **IT IS NOT THE SCORE. IT IS THE SIDE, TOTALLY.**

### The score: ☠️ **CLEARED. Candidate 30's killer is absent here.**

| book | name | ρ(name-as-dummy, score) | p | name's score range | book's score range |
|---|---|---|---|---|---|
| LIVE | `Bullish OB Created` | **+0.340** | 0.1234 | 4.25 – 6.75 | 2.25 – 6.75 |
| PAPER | `Bullish OB Created` | **−0.140** | 0.3299 | 2.25 – 7.50 | 1.75 – 7.75 |
| LIVE | *largest |ρ| of any name* | +0.340 | — | — | — |
| PAPER | *largest |ρ| of any name* | +0.140 | — | — | — |

> ### 🔴 **CANDIDATE 30 DIED AT ρ(count, score) = +0.92. HERE THE LARGEST |ρ| ANYWHERE IS +0.34 AND NOT ONE IS SIGNIFICANT.**
> **The trigger name is NOT the score in disguise, and on paper it spans the book's full score range
> 2.25–7.50.** This part of the confound is genuinely cleared, and I am saying so rather than borrowing
> candidate 30's verdict.

### The side: ☠️ **TOTAL. Worse than candidate 30's, and structural.**

> ## ☠️ **EVERY TRIGGER NAME DETERMINES ITS SIDE EXACTLY. 15 of 15 names map to ONE side. ZERO names appear on both.**
> A name literally contains the word `Bullish` or `Bearish`. **ρ(name, side) = ±1 by construction**, against
> candidate 30's +0.92 by correlation. **There is not one row anywhere in either book that separates
> "this name is bad" from "this side is bad".**

And the side is not innocent:

| book | side | n | ΣR | mean R | never-green | median MFE |
|---|---|---|---|---|---|---|
| LIVE | LONG | 14 | **−4.3079** | −0.308 | 6/14 = 43 % | 0.512 |
| LIVE | SHORT | 9 | −0.8717 | −0.097 | 5/9 = 56 % | 0.175 |
| PAPER | LONG | 24 | **−6.7794** | −0.283 | 8/24 = 33 % | 0.404 |
| PAPER | SHORT | 28 | **+5.3629** | +0.192 | 7/28 = 25 % | 0.879 |

**LONG is the worse side on BOTH books, and every `Bullish …` name is LONG by construction.**

### The partial answer: **within LONG only** — the effect shrinks but does not vanish

| book | `Bullish OB Created` vs the REST OF LONG | n vs n | Δ mean R | p | Δ median MFE | p | 🔴 Δ never-green | 🔴 p |
|---|---|---|---|---|---|---|---|---|
| LIVE | | 4 vs 10 | −0.855 | 0.0456 | −0.516 | 0.2613 | **+0.450** | 0.2444 |
| PAPER | | 9 vs 15 | −0.367 | 0.1588 | −0.583 | 0.0901 | **+0.533** | **0.0197** |

**Inside its own side, on both books, the name is still roughly twice as likely to produce a position that
never goes green** — 75 % vs 30 % live, 67 % vs 13 % paper. ☠️ **But p = 0.0197 and 0.2444, against
α = 2.174 × 10⁻³. It clears nothing.**

### The era: ⚖️ mixed, and one name is fully confined

| book | name | first … last entry | book span |
|---|---|---|---|
| LIVE | `Bullish OB Created` | 2026-08-23 … 09-13 | 07-30 … 09-14 |
| PAPER | `Bullish OB Created` | 2026-05-26 … 07-29 | 05-23 … 07-29 |
| 🔴 LIVE | `Within Bearish OB` | **2026-07-30 … 07-31** | 07-30 … 09-14 |

🔴 **`Bullish OB Created` is NOT era-confined on paper** (it spans the whole book) and covers the back
two-thirds of live. ☠️ **But `Within Bearish OB` — the other name that fired three of the eleven — is
confined on live to a TWO-DAY window, the first two days the live book ever traded.** Any live reading of
that name is a reading of 30–31 July 2026 and nothing else.

## 3f. THE SIDE-NEUTRAL FAMILY RULER — collapsing the mirrored pairs does not rescue anything

Pooling `Bullish X` with `Bearish X` is the only way to raise live n, and it **destroys the result**:

| family | LIVE n | LIVE mean R (Δ vs rest) | PAPER n | PAPER mean R (Δ vs rest) | same sign? |
|---|---|---|---|---|---|
| `Within OB` | **10** ✅ | −0.091 (**+0.237**) | **19** ✅ | −0.354 (**−0.514**) | ☠️ **NO** |
| `OB Created` | 6 | −0.644 (**−0.566**) | **15** ✅ | +0.023 (**+0.071**) | ☠️ **NO** |
| `I-BOS` | 3 | +0.006 (+0.265) | 5 | +0.947 (+1.078) | ✅ |
| `I-CHOCH+` | 3 | +0.235 (+0.529) | 3 | +0.837 (+0.917) | ✅ |
| `OB Mitigated` | 1 | −1.123 | 3 | −0.048 | ✅ |

**Only one family cell is rankable on live — `Within OB`, n = 10 — and it shows nothing: Δ mean R +0.237
(p = 0.448), Δ median MFE −0.032 (p = 0.988), Δ never-green +0.038 (p = 1.000).**

☠️ **AND THE FAMILY RULER INVERTS EXACTLY WHERE THE RAW NAME DID NOT.** `OB Created` is −0.644 mean on live
and **+0.023 on paper**, because paper's `Bearish OB Created` (n = 6, **+0.826 mean, median MFE 2.067,
0 of 6 never-green**) is the mirror image of `Bullish OB Created`. **The same structural event on the
opposite side produced the best paper cell in the study.** That is the side confound in one line, and it is
why the family ruler cannot be used to rescue live n.

---

# 4. VERDICT

## ☠️ **CANDIDATE 31: NO TRIGGER NAME CAN BE CONVICTED. It fails Bonferroni, the chronological halves and the regime split, and the side confound is total. NOTHING IS PROPOSED AND NO DIFF IS WRITTEN.**

| control | result |
|---|---|
| **a. Bonferroni** (α = 2.174 × 10⁻³ / 8.333 × 10⁻⁴) | ☠️ **FAILS.** Best p anywhere 0.0120 — 5.5× / 14.4× too large. |
| **b. Chronological halves** | ☠️ **FAILS on mean R.** Paper H2 Δ = **−0.001**; live never-green **inverts** between halves. *(The paper never-green sign does hold in both halves — recorded, n = 2 and 7, refused a rank.)* |
| **c. Regime, both legs populated** | ☠️ **FAILS.** PAPER FLAT leg **EMPTY**; live legs n = 2 each. Paper has only 4 FLAT rows in total. |
| **d. 🔴 Paper as the independent sample** | ✅ **PASSES ON SIGN** — mean R, median MFE and never-green all point the same way on both books. **The first candidate in the series to survive this.** But the live leg is **n = 4**. |
| **e. 🔴 The confound** | ⚖️ **SPLIT. The SCORE is CLEARED** (largest |ρ| = 0.34, none significant — candidate 30 died at +0.92). ☠️ **The SIDE is a TOTAL confound: 15 of 15 names map to exactly one side, ρ = ±1 by construction.** |

> ## 🔴 **THE ANSWER THE OPERATOR ASKED FOR, GIVEN PLAINLY BECAUSE THE SAMPLE CANNOT GIVE THE OTHER ONE**
>
> **WHICH NAME FIRED THE DEAD ENTRIES? FIVE NAMES DID, AND NO SINGLE NAME CARRIES MOST OF THEM.**
> The eleven never-green live losers split 3 / 3 / 2 / 2 / 1 across `Within Bearish OB`,
> **`Bullish OB Created`**, `Within Bullish OB`, `Bearish I-CHOCH+` and `Bullish OB Mitigated`.
>
> **ONE NAME STANDS OUT AND IT IS `Bullish OB Created`:** 4 live entries, **zero winners**, **zero ever
> reached +1R**, median MFE **0.152R**, **three of the four never green**, **ΣR −3.6745 = 70.9 % of the
> entire live book's loss on 17.4 % of its volume** — and on the independent paper book, **the same sign on
> all three measures** (n = 9, −4.6067R, 67 % never green, median MFE 0.096R).
>
> ☠️ **AND IT STILL CANNOT BE CONVICTED. n = 4 on live. p = 0.0120 at best against α = 0.0022. The FLAT leg
> is empty. And its name is `Bullish`, so nothing in this book separates it from being LONG.**

## 🔴 WHAT UNSUBSCRIBING WOULD HAVE COST — on the record, **NOT a proposal**

The brief asks for this only if a name survives all five. **None did**, so the table below is a cost
statement for a subtraction **nobody should make on this evidence**:

| book | drop `Bullish OB Created` | volume lost | ΣR would go |
|---|---|---|---|
| **LIVE** | −4 entries | **17.4 %** | **−5.1796 → −1.5051** (Δ **+3.6745**) |
| **PAPER** | −9 entries | **17.3 %** | **−1.4165 → +3.1902** (Δ **+4.6067**) |

🔴 **AND THE LINE DIRECTLY BENEATH IT, WHICH IS WHY NO DIFF IS WRITTEN.** The same subtraction applied to the
two names that *look* similar by count destroys the book:

| book | drop | volume lost | ΣR would go |
|---|---|---|---|
| PAPER | `Bearish OB Created` | 11.5 % | −1.4165 → 🔴 **−6.3730** |
| PAPER | `Bearish I-BOS` | 9.6 % | −1.4165 → 🔴 **−6.1533** |
| LIVE | `Within Bearish OB` | 17.4 % | −5.1796 → −4.9437 *(and it costs vpos 89, +1.386R)* |

**Unsubscribing from a name is a subtraction with no threshold to soften it. On a book where the same
structural event is the best cell on one side and the worst on the other, a 4-position live sample is not a
licence to remove a fifth of the volume.**

## 🔴 WHAT THIS DOES **NOT** ADDRESS — named before anyone asks

**The four live positions that peaked above +0.5R and still lost — ΣR −1.7167 — are an EXIT question, not a
trigger question, and no trigger name touches them:**

| vpos | side | trigger | MFE | realised R | closed by |
|---|---|---|---|---|---|
| 87 | LONG | `Within Bullish OB` | +0.615 | −0.440 | `ai_exit` |
| 91 | SHORT | `Bearish OB Created` | +0.661 | −0.484 | `ai_exit` |
| 95 | LONG | 🔴 `Bullish OB Created` | +0.560 | −0.533 | `external` |
| 98 | LONG | `Within Bullish OB` | +0.929 | −0.260 | `ai_exit` |

**They span three names, including two of the three that fired the +1R winners.** Unsubscribing the leading
suspect would have caught exactly **one of the four**. That −1.72R is a different problem with a different
cause and **nothing in this pass touches it.**

**It also does not address:** the 2026-08-19 signal-level result (different population, not re-run);
the exit advisor's ledger (**5 resolved of 10, Σ +1.0497R — unchanged by this pass**); the book gate
(**29/200, 0 refusals ever — unchanged**); or the 1H/15m tier names on the paper book, which **do not exist**
(§1b).

## 📋 RECORDED FOR THE NEXT PASS — MEASUREMENTS ONLY, NO ACTION PROPOSED

1. 🔴 **`Bullish OB Created` is the strongest same-sign-on-both-books observation this series has produced,
   and it is still n = 4 on live.** It is the one cell that would repay more n. **Six more live entries on
   that name would make it rankable** — and the name has produced 4 live entries in 7 weeks.
2. 🔴 **The side confound is structural and will never resolve on this data shape.** Every trigger name
   carries its direction in its own text. Any future name-level question must be asked **within a side**,
   and §3e gives the within-LONG frame to reuse.
3. **`Within Bearish OB` is live-confined to 2026-07-30…07-31** — two days. Any live claim about it is a
   claim about those two days.
4. **The two highest-volume live names sit on both tails** — `Within Bullish OB` fired 2 of the 11 dead
   entries **and** 2 of the 4 armers; `Within Bearish OB` fired 3 of the 11 **and** the best short on the
   book. **Volume does not concentrate the failure.**
5. **The score confound that killed candidate 30 is absent here** (largest |ρ| 0.34, none significant).
   Recorded so the next pass does not assume it.

**Nothing is proposed. Nothing is applied. No diff is written. Candidate 31 is recorded and the line closes.**

---

## 🔴 READ-ONLY ATTESTATION

| claim | proof |
|---|---|
| `openitems_guard` run first | **EXIT=0** — *"✅ header and current-state table agree with runtime"*, titan-bot HEAD `f16c271`, 14 watched values |
| Titan DB read-only | every handle opened `file:/root/titan-bot/trades.db?mode=ro` with `PRAGMA query_only=1`; **read back as `1`** at the start and again at the end of the pass |
| no writes | zero `INSERT` / `UPDATE` / `DELETE` issued; no file in `/root/titan-bot` modified; `git status` on `/root` **clean** |
| no orders | **no exchange call of any kind was made in this pass — not even a public one.** Every number comes from the DB. |
| no restart | `systemctl show titan` → **MainPID 1572470**, `NRestarts=0`, `ActiveState=active`, active since **2026-09-12 14:58:32 UTC** — unchanged |
| `NRestarts` unchanged on BOTH | titan **0** · mercury-sol **0** |
| `EXIT_ADVISOR_DRYRUN` still False | read from the loaded `__pycache__/config.cpython-312.pyc` (mtime **2026-09-10 14:34:54 UTC**): **`False`** |
| `BOOK_GATE_DRYRUN` still False | same bytecode: **`False`** (`BOOK_GATE_ENABLED=True`, `BOOK_GATE_CLAUSE_A_ENABLED=True`, `LIVE_TRADING_ENABLED=True`, `ORDER_ADAPTER_LIVE=True`) |
| `CLAUSE_B` still False | same bytecode: **`BOOK_GATE_CLAUSE_B_ENABLED = False`** |
| 🔴 **book-gate counter untouched at 29/200** | rows carrying `book_gate_opp_pctl`: **29**; refusals ever: **0**. Identical to the 15:20 and 17:30 passes. |
| **Mercury-SOL untouched** | 🔴 `/mnt/volume_nyc1_1780480650620/mercury-sol` **was not opened, read, listed or written — not one byte, no DB query, no restart, no venue call.** The only command naming it was `systemctl show mercury-sol -p NRestarts` (**0**, MainPID 2245907) for this table. |
| book state at the pass | **FLAT** — 0 open `virtual_positions`, 0 `exit_pending`, 0 `breakeven_jobs`; bot alive (last row `33091`, 2026-09-16 15:55:06 UTC) |

**Provenance.** `tv_action`, `entry_tiers_json`, `matrix_breakdown_json`, `market_regime` and
`confluence_score` read out of Titan's own `trades.db` (`mode=ro`, `query_only=1`) on the entry row of each
of the 75 closed positions, joined by `virtual_positions.trades_entry_row_id`; the 5m trigger name
**validated by reconciling `tv_action` against `entry_tiers_json → tiers['5m'].name` on 24 of 24 rows that
carry both, zero mismatches**; R and MFE **validated by reproducing the 2026-09-16 15:20 report's ΣR, every
close-reason cell and all 23 live MFEs to the digit before any new number was computed**; Spearman ρ with
two-sided permutation p, 40 000 shuffles per test (20 000 per dummy-vs-score ρ), seed 20260916; candidate
numbering continues from `reports/2026-09-16-1730-titan-candidate-30-the-contributing-category-count-is-the-score-wearing-another-name.md`,
whose five-control frame this pass adopts verbatim. The 2026-08-19 signal-level pass is cited from
`reports/2026-08-19-2330-titan-sol-signal-set-has-no-edge.md` and is **not** re-run.

---

# 🔴 INDEPENDENT VERIFICATION LOG — WHAT THIS SESSION ACTUALLY RE-RAN

A second session opened `trades.db` at `mode=ro` with `PRAGMA query_only=1` (**read back as `1` at the start
and again at the end**) and recomputed the study **from the raw tables, without reading the 19:00 report's
numbers first**. Then, and only then, the two were compared line by line.

| claim re-derived from the DB | published | re-measured | verdict |
|---|---|---|---|
| closed positions | 76 | 76 | ✅ |
| excluded for NULL/zero `initial_risk_usdt` | vpos 33 | vpos 33 | ✅ |
| `archived_pre_geometry_fix` rows | 6 | vpos 27–32 | ✅ |
| population | 75 | 75 | ✅ |
| LIVE n / vpos range | 23 / 86–108 | 23 / 86–108 | ✅ |
| PAPER n / vpos range | 52 / **27–85** | 52 / **34–85** | ☠️ **CORRECTION 1** |
| LIVE ΣR | −5.1796 | **−5.1796** | ✅ |
| PAPER ΣR | −1.4165 | **−1.4165** | ✅ |
| `entry_tiers_json` coverage | live 23/23, paper 1/52 | **23/23, 1/52** | ✅ |
| `tv_action` coverage | 23/23, 52/52 | **23/23, 52/52** | ✅ |
| 5m name reconciliation | 24 of 24, 0 mismatches | **24 rows, 0 mismatches** | ✅ |
| distinct names | live 9, paper 14, total 15 | **9 / 14 / 15** | ✅ |
| every per-name cell (n, ΣR, mean, win, median MFE, never-green, ever-1R, vpos list), **both books, all 23 rows** | — | **reproduced to the digit** | ✅ |
| the eleven never-green live losers | 86,88,90,92,93,97,99,102,103,106,107 · ΣR −7.5805 | **identical, ΣR −7.5805** | ✅ |
| their five names, 3/3/2/2/1 | — | **identical** | ✅ |
| the four live +1R mirrors | 89, 94, 100, 108 | **identical, same names** | ✅ |
| side tables, both books | — | **identical** | ✅ |
| ρ(name-dummy, score) | LIVE +0.340 p 0.1234 · PAPER −0.140 p 0.3299 | **+0.340 / 0.1234 · −0.140 / 0.3299** | ✅ |
| largest \|ρ\| any name | LIVE +0.340 · PAPER +0.140 | LIVE +0.340 · PAPER **+0.188** (`Bearish OB Mitigated`) | ⚠️ see note |
| PAPER permutation, `Bullish OB Created` | −0.586/0.0863 · −0.710/0.0432 · +0.457/0.0120 | **identical, all three** | ✅ |
| PAPER permutation, `Within Bearish OB` | −0.483/0.1184 · +0.136/0.7771 · +0.058/0.7274 | **identical, all three** | ✅ |
| LIVE whole-book permutation | 🔴 **never printed**; §3a claimed "every LIVE p ≥ 0.0456" | **mean R p = 0.0255** | ☠️ **CORRECTION 2** |
| within-LONG, both books | 4v10 −0.855/0.0456 · 9v15 +0.533/0.0197 | **identical** | ✅ |
| regime counts | LIVE 17/6 · PAPER 39/4/9 unrecorded | **identical** | ✅ |
| PAPER FLAT leg for the name | **EMPTY** | **n = 0 — EMPTY** | ✅ |
| chronological halves, all four rows | −0.362/−0.500 · −1.070/+0.667 · −1.502/+0.292 · −0.001/+0.504 | **identical** | ✅ |
| era confinement | `Within Bearish OB` live 07-30…07-31 | **07-30 … 07-31** | ✅ |
| family ruler, all five families | — | **identical, including the `OB Created` sign inversion** | ✅ |
| cost-of-dropping table, all five rows | — | **identical** | ✅ |
| names mapping to exactly one side | 15 of 15 | **15 of 15, zero on both sides** | ✅ |

⚠️ **The one cosmetic slip not worth a correction banner:** the 19:00 edition printed PAPER's largest
non-target |ρ| as +0.140 (the target's own value). The true largest is **+0.188**, on `Bearish OB Mitigated`,
**n = 1**. It is smaller than LIVE's +0.340, it is not significant, and it strengthens rather than weakens
the "not the score" finding — the point stands that **candidate 30 died at ρ = +0.92 and nothing here
exceeds +0.34.**

> ## ✅ **BOTTOM LINE OF THE VERIFICATION: THE ANALYSIS IS SOUND. 27 of 29 checked claims reproduce exactly; 2 were wrong and are corrected; NOT ONE correction moves the verdict.**
> `Bullish OB Created` remains the standout description and remains **unconvictable at n = 4**.

---

## 🔴 READ-ONLY ATTESTATION — **THIS SESSION, 2026-09-16 16:15 UTC**

| claim | proof |
|---|---|
| `openitems_guard` run FIRST, before anything else | **EXIT=0** — *"✅ header and current-state table agree with runtime"*, titan-bot HEAD `f16c271`, 14 watched values |
| Titan DB read-only | every handle `file:/root/titan-bot/trades.db?mode=ro` + `PRAGMA query_only=1`, **read back as `1`** at open and at close of the pass |
| no writes | zero `INSERT`/`UPDATE`/`DELETE`; newest `.py` in `/root/titan-bot` is `claude_advisor.py` **2026-09-12 14:57** — nothing touched today; `git status` on `/root` **clean** |
| no orders | **no exchange call of any kind, not even public.** Every number came from the DB. |
| no restart | `systemctl show titan` → MainPID **1572470**, `ActiveState=active`, active since **2026-09-12 14:58:32 UTC** — unchanged |
| `NRestarts` unchanged on BOTH | titan **0** · mercury-sol **0** |
| `EXIT_ADVISOR_DRYRUN` still False | **`False`** — *"🔴 ACTING — a `close` verdict closes the position"* |
| `BOOK_GATE_DRYRUN` still False | **`False`** (`BOOK_GATE_ENABLED=True`, `CLAUSE_A=True`, `LIVE_TRADING_ENABLED=True`, `ORDER_ADAPTER_LIVE=True`) |
| `CLAUSE_B` still False | **`BOOK_GATE_CLAUSE_B_ENABLED = False`** |
| 🔴 **book-gate counter untouched at 29/200** | rows carrying `book_gate_opp_pctl`: **29**; every one with `book_gate_clause = ''` ⇒ **0 refusals ever**. Identical to the 15:20, 17:30 and 19:00 passes. |
| **Mercury-SOL untouched** | 🔴 `/mnt/volume_nyc1_1780480650620/mercury-sol` **was not opened, read, listed, queried or written — not one byte, no DB query, no restart, no venue call.** The only command naming it was `systemctl show mercury-sol -p NRestarts` (**0**, MainPID 2245907) for the row above, which touches systemd, not the bot. |
| book state at the pass | **FLAT** — 0 open `virtual_positions`, 0 `exit_pending`, 0 `breakeven_jobs`; bot alive, last `trades` row **33091 @ 2026-09-16 15:55:06** |
| nothing proposed, nothing applied | **no diff written, no file in `/root/titan-bot` created or edited, no config flag read as anything other than its on-disk value** |

**Supersedes:** `reports/2026-09-16-1900-titan-candidate-31-no-live-trigger-name-reaches-n8-bullish-ob-created-carries-71-percent-of-the-loss.md`, which stays on the record unaltered so the corrections are auditable.
