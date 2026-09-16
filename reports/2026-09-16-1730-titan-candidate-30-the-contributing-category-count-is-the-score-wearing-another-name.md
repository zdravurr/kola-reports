# Titan — **candidate 30: does a 3-of-3 entry behave differently from a 2-of-3? IT DIES.** The count is the **SCORE WEARING ANOTHER NAME** — ρ(count, score) = **+0.92**, and on the live book **no score value is shared by two count bands at all.** 🔴 The live book has **ONE** rankable cell of three. No diff, no gate, no proposal.

**2026-09-16 17:30 UTC · commit `f16c271` · Titan LIVE REAL MONEY · READ-ONLY PASS · Mercury-SOL NOT TOUCHED** · `openitems_guard` **EXIT=0**

**Basis:** my own `2026-09-16-1520` report, **§3b(i)** (11 of 17 live losers never printed +0.25R, −7.58R = 77 % of all live losses; zero losers ever reached +1R) and **§3d** (not one of the last five entries had all three categories counting).

---

## 🔴 CONTROLS, DECLARED IN THE HEADER — BEFORE ANY RESULT

* **Bonferroni over every count × side × book:** count (1/2/3/4) × side (LONG/SHORT) × book (LIVE/PAPER) = **16 cells, α = 0.05 / 16 = 3.125 × 10⁻³**.
* **A cell is ranked only if n ≥ 8.** Cells below that are printed and **refused a rank**, never quietly folded into a neighbour.
* **Survival requires ALL FOUR:** p < α · same sign in both chronological halves of each book · same sign in TREND and FLAT **with both legs populated** · **same sign on paper and live**.
* **Plus the confound (§3e):** the count must beat the SCORE, not merely track it.
* **Paper and live are NEVER pooled.** R = `net_pnl / initial_risk_usdt`. Population: **75 closed positions with a stored `matrix_breakdown_json` — 23 LIVE (vpos 86–108), 52 PAPER (vpos 27–85).** vpos 33 is excluded (NULL `initial_risk_usdt`), as in the 15:20 pass.

---

# 🔴 n FIRST, BEFORE ANY RESULT. READ THIS BEFORE THE NUMBERS.

**Contributing categories counted on the traded side, from `matrix_breakdown_json`. Two rulers, because the
matrix has FOUR categories and the operator's question names THREE tiers:**

| ruler | LIVE | PAPER |
|---|---|---|
| **3 TIER categories** (TREND=1H, MOMENTUM=15m, EXECUTION=5m) | 1 → **5** · 2 → **16** · 3 → 🔴 **2** | 1 → 14 · 2 → 29 · 3 → 9 |
| **all 4 categories** (+ LIQUIDITY) | 1 → 5 · 2 → **12** · 3 → 🔴 **6** · 4 → 🔴 **0** | 1 → 13 · 2 → 28 · 3 → 10 · 4 → 🔴 1 |

> ## ☠️ **THE LIVE BOOK CANNOT RANK THIS. ONE CELL OF THREE REACHES n = 8.**
> **The entire 3-of-3 population on live money is TWO POSITIONS — vpos 86 and vpos 95. Both LOST**
> (−1.022R and −0.533R, ΣR **−1.5548**, win rate **0 of 2**). On the 4-category ruler the 4-of-4 cell is
> **EMPTY on both books but one paper row**.
> **Nothing below that cites a live count cell other than n3=2 is a ranking. It is a description.**

**Paper has three rankable cells (14 / 29 / 9) and is the only book that can carry the question at all.
Every paper figure below is labelled PAPER and is never allowed to stand in for live.**

---

# 1. CLASSIFY EVERY ENTRY BY WHAT ACTUALLY COUNTED

## 1a. THE MECHANISM, READ OUT OF `signal_matrix.compute_score`, NOT ASSUMED

A category contributes to the traded side only if it survives two passes: **intra-category** (a category
holding both LONG and SHORT points is contradictory → zeroed) and **inter-category** (a category whose net
direction is the MINORITY direction → zeroed). A signal that has aged out of its window is simply **not in
`get_active_signals`**, so it arrives as `signal_count = 0`.

🔴 **ONE CASE THAT IS NEITHER, AND THAT I HAD TO FIND BEFORE ANY COUNT WAS RIGHT: THE TIE.** When the
category counts are level (1 LONG vs 1 SHORT), `majority` is NEUTRAL and **neither side is zeroed — both
keep their points.** The opposing category is then live, scoring, and pointing the wrong way. **8 of the 300
category-slots are in this state.** Counting `contribution > 0` alone would have mis-scored **8 of 75
positions**; counting `contribution > 0 AND net_direction == traded side` reconciles
**75 of 75 against the stored `confluence_score`, exactly.** That reconciliation is what licenses every
number below.

### The distribution — 75 positions × 4 categories = 300 slots

| book | category | **CONTRIB** | absent | intra_conflict | minority (zeroed) | opposing (tie, live) |
|---|---|---|---|---|---|---|
| **LIVE** | TREND | **17** | **6** | 0 | 0 | 0 |
| | MOMENTUM | 11 | 4 | **8** | 0 | 0 |
| | LIQUIDITY | **4** | 6 | 5 | 6 | 2 |
| | EXECUTION | 15 | **0** | **8** | 0 | 0 |
| **PAPER** | TREND | **43** | **9** | 0 | 0 | 0 |
| | MOMENTUM | 26 | 12 | **14** | 0 | 0 |
| | LIQUIDITY | **4** | 12 | 16 | 14 | 6 |
| | EXECUTION | 30 | **0** | **22** | 0 | 0 |

🔴 **THREE STRUCTURAL FACTS FALL OUT AND THEY ARE THE SAME ON BOTH BOOKS:**
1. **TREND is never conflicted. Ever.** 0 intra, 0 minority, on all 75 positions. When the 1H does not count,
   it is because it **aged out** — 6 of 6 live, 9 of 9 paper.
2. **EXECUTION is never absent.** 0 of 75. It is the trigger; a 5m signal is present by construction. When it
   does not count it is **always** intra_conflict — 8 live, 22 paper.
3. **LIQUIDITY barely participates**: it contributes on **4 of 23 live** and **4 of 52 paper**, and it is the
   ONLY category that is ever minority-zeroed or tied. It is why the 4-category ruler and the 3-tier ruler
   disagree on 7 positions.

## 1b. 🔴 "ABSENT" vs "PRESENT AND POINTING THE RIGHT WAY BUT DISALLOWED" — AND A CORRECTION TO MY OWN §3d

These are different events and the brief is right to separate them. **LIVE, 23 positions × 3 tiers = 69 slots:**

| tier | COUNTED | **ttl_expired** — present in the tier tracker, aged out of the matrix | **intra_conflict** — present and SPLIT | absent everywhere | reason unrecorded (pre-`7b17e11` rows) |
|---|---|---|---|---|---|
| **1H** (TREND) | 17 | 🔴 **6** | 0 | 0 | 0 |
| **15m** (MOMENTUM) | 11 | **2** | **8** | 1 | 1 |
| **5m** (EXECUTION) | 15 | 0 | **8** | 0 | 0 |
| **total** | **43** | **8** | **16** | **1** | **1** |

> ### 🔴 A CORRECTION TO MY OWN 15:20 REPORT, §3d. I WROTE IT LOOSELY AND THE DISTINCTION MATTERS.
> §3d said that on the last five entries the third tier was *"PRESENT and pointing the right way but
> disallowed."* **That is the TIER TRACKER's view, not the MATRIX's, and the matrix is what scores.**
> Of those five: **vpos 104, 105 and 107 were `ttl_expired` — in the matrix they were `signal_count = 0`,
> i.e. NOT PRESENT AT ALL.** Only **vpos 106 and 108** were present-and-split (`intra_conflict`).
> **Two different clocks, both real: the tier tracker still displays a signal the scorer has already
> expired.** The §3d observation stands — every one of the five scored 2 of 3 — but "present and pointing
> the right way" is true of **two** of them, not five.

🔴 **AND THE COVERAGE LIMIT, STATED BEFORE IT IS USED:** `entry_tiers_json` begins **2026-07-29**. The paper
book ran **2026-05-23 → 2026-07-29**; the live book **2026-07-30 → 2026-09-14**. **So `ttl_expired` can be
separated from `absent` on the LIVE book only. On paper the two collapse into one bucket by construction,
and no later pass may read the paper `absent` cell as if it were clean.**

## 1c. n PER CELL, RESTATED BEFORE ANY OUTCOME

**LIVE** — n3: 1 → **5** · 2 → **16** · 3 → **2**  ·  **PAPER** — n3: 1 → **14** · 2 → **29** · 3 → **9**
**Ranked cells (n ≥ 8): LIVE 1 of 3. PAPER 3 of 3.**

---

# 2. OUTCOMES BY THAT COUNT

## 2a. THE MASTER TABLE — per book, per count. Paper and live never pooled.

### 🔴 LIVE (n = 23) — **only the middle row is ranked**

| n3 | n | ΣR | mean R | win rate | median MFE | mean MFE | **ever ≥ +0.25R** | ever ≥ +1R | rank? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 5 | −0.7649 | −0.1530 | 1/5 = 20.0 % | 0.464 | 0.636 | **3/5 = 60 %** | 1/5 | ☠️ **n < 8** |
| **2** | **16** | **−2.8599** | **−0.1787** | 5/16 = 31.2 % | 0.307 | 0.507 | **8/16 = 50 %** | 3/16 | ✅ ranked |
| 3 | **2** | −1.5548 | **−0.7774** | **0/2 = 0.0 %** | 0.330 | 0.330 | 1/2 = 50 % | **0/2** | ☠️ **n < 8** |

per side, LIVE — **LONG** n3=1 (n=2) +0.160 · n3=2 (n=11) −0.372 · n3=3 (n=1) −0.533 · **SHORT** n3=1 (n=3) −0.361 · n3=2 (n=5) +0.247 · n3=3 (n=1) −1.022. **Five of six side cells are below n=8.**

### PAPER (n = 52) — three ranked cells

| n3 | n | ΣR | mean R | win rate | median MFE | mean MFE | **ever ≥ +0.25R** | ever ≥ +1R | rank? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 14 | **−7.2601** | −0.5186 | 3/14 = 21.4 % | 0.315 | 0.564 | 8/14 = **57 %** | 2/14 | ✅ |
| 2 | 29 | +2.9332 | +0.1011 | 13/29 = 44.8 % | 0.801 | 1.084 | 22/29 = **76 %** | 11/29 | ✅ |
| 3 | 9 | +2.9104 | **+0.3234** | 7/9 = **77.8 %** | 0.891 | 1.048 | 7/9 = **78 %** | 4/9 | ✅ |

*(4-category ruler, PAPER: 1 → n=13 mean −0.473 · 2 → n=28 +0.058 · 3 → n=10 **+0.352, win 90 %** · 4 → n=1.
LIVE: 1 → n=5 −0.153 · 2 → n=12 −0.118 · 3 → n=6 **−0.499** · 4 → **n=0**.)*

## 2b. 🔴 THE TEST THAT MATTERS — DOES THE COUNT PREDICT **GETTING MEANINGFULLY GREEN**?

§3b(i) established that 77 % of live losses sit on positions that never printed +0.25R. So the question is
not final R, it is **MFE**. Spearman, permutation p, 40 000 shuffles each:

| book | predictor | vs **MFE** | vs **ever ≥ +0.25R** | vs R |
|---|---|---|---|---|
| **LIVE** | n3 | ρ **−0.139**, p 0.523 | ρ **−0.073**, p **0.941** | ρ −0.171, p 0.436 |
| **LIVE** | n4 | ρ −0.297, p 0.170 | ρ −0.194, p 0.355 | ρ −0.174, p 0.428 |
| **PAPER** | n3 | ρ +0.210, p **0.135** | ρ +0.169, p **0.218** | ρ +0.377, p 0.0062 *(nominal)* |
| **PAPER** | n4 | ρ +0.186, p 0.190 | ρ +0.218, p 0.128 | ρ +0.346, p 0.0125 *(nominal)* |

> ### ☠️ **ON THE TEST THE BRIEF NAMES AS THE ONE THAT MATTERS, NOTHING REACHES EVEN NOMINAL SIGNIFICANCE ON EITHER BOOK.**
> LIVE: **every ρ is NEGATIVE** — the sign is the OPPOSITE of the hypothesis — and the largest p is **0.941**.
> PAPER: p = 0.135 on MFE and **0.218** on "ever went green", against a Bonferroni α of **3.125 × 10⁻³**.
> The only nominal hits are on final R, and §3e shows what is actually producing them.

## 2c. 🔴 SPLIT BY *WHY* THE THIRD CATEGORY WAS MISSING — stale (`ttl_expired`) vs genuinely split (`intra_conflict`)

Nobody has separated these. They are separated here, inside the **n3 = 2 cohort** — the only place where
exactly one tier is missing and the comparison is clean.

### LIVE, n3 = 2 (n = 16)

| why the third tier was missing | n | ΣR | mean R | win | median MFE | ever ≥ +0.25R |
|---|---|---|---|---|---|---|
| 🔴 **`ttl_expired`** (98, 99, 101, 102, 103, 104, 105, 107) | **8** | **−3.4030** | **−0.4254** | 2/8 | 0.307 | 4/8 = 50 % |
| `intra_conflict` (87, 89, 92, 93, 97, 106, 108) | **7** | +0.1259 | +0.0180 | 2/7 | 0.116 | 3/7 = 43 % |
| `absent` (100) | 1 | +0.4172 | — | 1/1 | 1.322 | 1/1 |

**The `ttl_expired` cohort is the ONLY live cell outside n3=2 as a whole that reaches n = 8, and it is the
worst block of eight on the live book: −3.40R, 2 winners, and it contains BOTH −1.1R stop-outs (102, 103)
and the never-green vpos 107.** That is a real and rankable-n observation.

> ☠️ **BUT IT CANNOT BE RANKED AGAINST ANYTHING. Its comparator, `intra_conflict`, is n = 7 — below the bar.**
> The difference is −0.4434R at **p = 0.298**. **REFUSED A RANK, as declared. It is recorded, not claimed.**

### PAPER, n3 = 2 (n = 29) — both cells ranked, and **there is no difference**

| why | n | mean R | median MFE | ever ≥ +0.25R |
|---|---|---|---|---|
| `absent`/stale *(cannot be separated on paper — see §1b)* | 15 | +0.1528 | 0.806 | 12/15 = 80 % |
| `intra_conflict` | 14 | +0.0458 | 0.629 | 10/14 = 71 % |
| **difference** | | **+0.1070, p 0.776** | **+0.3405, p 0.364** | **+0.0857, p 0.682** |

☠️ **NOT SIGNIFICANT ON ANY OF THE THREE, NOT EVEN NOMINALLY.** A stale third tier and a split third tier
behave the same on the only book that can rank them.

## 2d. 🔴 STATED AT THE TOP AND REPEATED HERE, AS THE BRIEF DEMANDS

> **THE LIVE BOOK CANNOT RANK THIS.** Two of its three count cells are n = 5 and n = 2. The 3-of-3 population
> on live money is **two positions and both lost**. The figures in §2a's paper table are **PAPER** and are
> labelled as such everywhere they appear.

---

# 3. THE FOUR CONTROLS

## 3a. BONFERRONI — declared in the header, applied here

**16 cells, α = 3.125 × 10⁻³.** Best p anywhere in the family: **PAPER n3 vs R, p = 0.0062 — a factor of 2.0
too large.** It **FAILS**. Every LIVE p is ≥ 0.170. ☠️ **CONTROL (a) FAILS.**

## 3b. 🔴 CHRONOLOGICAL HALVES

| book | half | n3=1 | n3=2 | n3=3 |
|---|---|---|---|---|
| **LIVE** H1 (→ 2026-08-24) | n=11 | n=5, **−0.153** | n=4, **+0.020** | n=2, **−0.777** |
| **LIVE** H2 (2026-08-24 →) | n=12 | 🔴 **n=0** | n=12, −0.245 | 🔴 **n=0** |
| PAPER H1 (→ 2026-06-25) | n=26 | n=6, −0.488 | n=14, +0.500 | n=6, +0.576 |
| PAPER H2 (2026-06-25 →) | n=26 | n=8, −0.542 | n=15, −0.271 | n=3, −0.182 |

☠️ **CONTROL (b) FAILS ON LIVE OUTRIGHT: the second live half contains ONLY n3 = 2. Both other cells are
EMPTY. No trend exists to have a sign.** Every live 1-of-3 and 3-of-3 position is in the first half — the
shape stopped occurring on live money after 2026-08-24.
On PAPER the mean-R ordering survives both halves, but **the MFE ordering does not**: H2 median MFE goes
**0.295 → 0.579 → 0.290**, which is not monotone, and H2's n3=3 cell is **n = 3**, below the bar.

## 3c. 🔴 REGIME SPLIT — BOTH LEGS CANNOT BE POPULATED

| book | regime | n | n3=1 | n3=2 | n3=3 |
|---|---|---|---|---|---|
| LIVE | TREND | 17 | n=5, −0.153 | n=10, −0.059 | n=2, −0.777 |
| LIVE | **FLAT** | 6 | 🔴 **n=0** | n=6, −0.378 | 🔴 **n=0** |
| PAPER | TREND | 39 | n=9, −0.420 | n=22, +0.272 | n=8, +0.357 |
| PAPER | **FLAT** | **4** | n=1 | n=3 | 🔴 **n=0** |
| PAPER | *(regime unrecorded)* | 9 | n=4 | n=4 | n=1 |

☠️ **CONTROL (c) FAILS. The FLAT leg is n = 6 on live with two empty cells and n = 4 on paper with one empty
cell.** The regime split cannot be run at all, on either book. Only PAPER-TREND is populated across all
three counts, and a control that runs on one leg is not a control.

## 3d. 🔴 PAPER AS THE INDEPENDENT SAMPLE — **THE SIGN INVERTS**

| book | n3=1 → n3=3, mean R | n3=1 → n3=3, ever-green % | direction |
|---|---|---|---|
| **PAPER** | **−0.519 → +0.323** | **57 % → 78 %** | 🔼 **UP** |
| **LIVE** | **−0.153 → −0.777** | **60 % → 50 %** | 🔽 **DOWN** |

☠️ **CONTROL (d) FAILS. The sign inverts between the books — on mean R and on the ever-green share alike.**
This is exactly what killed candidates **21, 22 and 29**, and the standing rule is that no threshold rescues
it. The live leg is n = 2 and therefore **not a ranking** — which makes the position worse, not better:
**there is no independent confirmation available at all, in either direction.**

## 3e. 🔴🔴 THE CONFOUND. **THIS IS WHERE IT ACTUALLY DIES.**

A 3-of-3 entry has a higher score **by construction** — each surviving category contributes up to 2.5 points,
so the count *is* a coarse bin of the score.

| | ρ(count, score) |
|---|---|
| LIVE, n3 | **+0.7936** |
| LIVE, n4 | 🔴 **+0.9201** |
| PAPER, n3 | **+0.8454** |
| PAPER, n4 | 🔴 **+0.9116** |

### The score ranges do not merely correlate — on live money they do not TOUCH

| book | n3=1 scores | n3=2 scores | n3=3 scores | shared values |
|---|---|---|---|---|
| **LIVE** | 2.25 – 2.50 | 3.50 – 6.50 | 5.75 – 6.75 | ☠️ **NONE. Not one.** |
| PAPER | 1.75 – 4.25 | 3.50 – 7.50 | 5.75 – 7.75 | only **4.25**, **6.0**, **7.5** |

> ## ☠️ **ON THE LIVE BOOK THE CONFOUND CANNOT BE SEPARATED AT ALL. No score value is shared by two count bands, so there is not one matched pair to compare.**

**On paper, the three shared score values hold this much:**

| score | n3=2 | n3=3 | who wins |
|---|---|---|---|
| 4.25 | n=**7**, mean −0.441, medMFE 0.801 | *(n3=1: n=**1**, −1.108)* | the **lower** count loses, n=1 |
| 6.0 | n=**1**, +0.075 | n=**2**, +0.192 | higher, on 1-vs-2 |
| 7.5 | n=**1**, **+0.122** | n=**1**, **−0.476** | 🔴 the **LOWER** count wins |

☠️ **Every matched cell is 1-vs-7, 1-vs-2 or 1-vs-1. Not one reaches n = 8 on either side, and the direction
is inconsistent across the three.** The confound survives intact.

### And the decisive number: **the score does the job at least as well, and on the test that matters, BETTER**

| PAPER, predictor | vs R | vs MFE | vs **ever ≥ +0.25R** |
|---|---|---|---|
| n3 (the count) | ρ +0.377, p 0.0062 | ρ +0.210, p 0.135 | ρ **+0.169**, p **0.218** |
| **SCORE** | ρ +0.347, p 0.0117 | ρ **+0.270**, p **0.0533** | ρ **+0.327**, p **0.0186** |

> ## 🔴 **THE COUNT ADDS NOTHING OVER THE SCORE, AND ON "DOES THE POSITION EVER GO GREEN" THE SCORE IS STRICTLY BETTER — ρ +0.327 AGAINST +0.169, AND ROUGHLY TEN TIMES THE DISCRIMINATION IN p.**
> ☠️ **CONTROL (e) FAILS. The count is the score wearing another name, and a coarser name at that.**

---

# 4. VERDICT

## ☠️ **CANDIDATE 30 DIES. IT FAILS ALL FIVE CONTROLS. NO GATE IS PROPOSED AND NO DIFF IS WRITTEN.**

| control | result |
|---|---|
| **a. Bonferroni (α = 3.125 × 10⁻³)** | ☠️ **FAILS.** Best p in the family 0.0062 (PAPER, final R) — 2.0× too large. Every LIVE p ≥ 0.170. |
| **b. Chronological halves** | ☠️ **FAILS.** The live second half contains **only** n3=2; the other two cells are empty. On paper the mean-R order holds but the MFE order does not (0.295 → 0.579 → 0.290). |
| **c. Regime, both legs populated** | ☠️ **FAILS.** FLAT is n=6 live (2 empty cells) and n=4 paper (1 empty cell). The split cannot be run on either book. |
| **d. 🔴 Paper as the independent sample** | ☠️ **FAILS. THE SIGN INVERTS** — paper −0.519 → +0.323 and 57 % → 78 % green; live −0.153 → −0.777 and 60 % → 50 %. Same kill as candidates 21, 22 and 29. |
| **e. 🔴 The score confound** | ☠️ **FAILS, and this is the real cause of death.** ρ(count, score) = **+0.92**. **Zero shared score values on live.** On paper the score **beats** the count on the ever-green test, ρ +0.327 vs +0.169. |

**And underneath all five: the live book never had the n to answer the question.** Two of its three cells are
n=5 and n=2. **The entire live 3-of-3 population is vpos 86 and vpos 95, and both lost.** The single
best-shaped live position ever — **vpos 94, MFE +1.802R, closed +0.865R on the trail** — is a **1-of-3 at the
minimum score of 2.25**. That is not a counter-finding either; it is one trade. It is a warning against
reading this line the other way round.

## 🔴 WHAT WOULD IT HAVE COST, HAD ANYONE BUILT IT — stated so the volume cost is on the record, NOT as a proposal

| book | a 3-of-3 requirement keeps | ΣR kept, of the book's total |
|---|---|---|
| **LIVE** | **2 of 23 = 8.7 %** | **−1.5548** of −5.1796 |
| PAPER | 9 of 52 = 17.3 % | +2.9104 of −1.4165 |

**On live money it refuses 91 % of all entries to keep two losers.** *(A looser 3-of-4-categories form keeps
6 of 23 = 26.1 % and ΣR −2.9937 — still negative, still worse per trade than the book it filters.)*

## 🔴 WHAT THIS DOES **NOT** ADDRESS, NAMED BEFORE ANYONE ASKS

**The four live positions that peaked above +0.5R and still finished negative — ΣR −1.7167 — are untouched by
any count filter, and the count would not have caught one of them:**

| vpos | n3 | score | MFE | realised R |
|---|---|---|---|---|
| 87 | 2 | 4.25 | +0.615 | −0.440 |
| 91 | **1** | 2.50 | +0.661 | −0.484 |
| 95 | 🔴 **3** | 6.75 | +0.560 | −0.533 |
| 98 | 2 | 3.50 | +0.929 | −0.260 |

🔴 **They span EVERY count band — 1, 2 and 3 — and vpos 95 is one of only two live 3-of-3 entries ever. A
3-of-3 requirement would have KEPT it and discarded the other three.** That −1.72R is a different problem
with a different cause, and it belongs to the exit, not the entry. **Nothing in this pass touches it.**

## 📋 RECORDED FOR THE NEXT PASS — MEASUREMENTS ONLY, NO ACTION PROPOSED

1. 🔴 **The `ttl_expired` cohort is the worst rankable block on the live book** — 8 positions, **−3.4030R**,
   2 winners, containing both −1.1R stop-outs and the never-green vpos 107. **Its comparator is n = 7 and it
   is therefore REFUSED A RANK here.** It is the one thing in this pass that would repay more n.
2. **TREND never conflicts (0 of 75) and EXECUTION is never absent (0 of 75).** Those two facts are
   structural, identical on both books, and they are why the "count" has so few attainable values.
3. **LIQUIDITY contributes on 4 of 23 live and 4 of 52 paper** and is the only category ever minority-zeroed
   or tied — the sole source of disagreement between the two rulers.
4. **The tie case** (8 of 300 slots): the opposing category keeps its points and is never zeroed. Recorded as
   a fact about the scorer, **not** flagged as a defect.

**Nothing is proposed. Nothing is applied. No diff is written. The line closes.**

---

## 🔴 READ-ONLY ATTESTATION

| claim | proof |
|---|---|
| `openitems_guard` run first | **EXIT=0** — *"✅ header and current-state table agree with runtime"*, titan-bot HEAD `f16c271`, 14 watched values |
| Titan DB read-only | every handle opened `file:/root/titan-bot/trades.db?mode=ro` with `PRAGMA query_only=1`; **read back as `1`** at the start and again at the end |
| no writes | zero `INSERT` / `UPDATE` / `DELETE` issued; no file in `/root/titan-bot` modified |
| no orders | no exchange call of any kind was made in this pass — not even a public one |
| no restart | `systemctl show titan` → **MainPID 1572470**, `NRestarts=0`, active since **2026-09-12 14:58:32 UTC** — unchanged |
| `NRestarts` unchanged on BOTH | titan **0** · mercury-sol **0** |
| `EXIT_ADVISOR_DRYRUN` still False | read from the loaded `__pycache__/config.cpython-312.pyc` (mtime 2026-09-10 14:34:54 UTC): **`False`** |
| `BOOK_GATE_DRYRUN` still False | same bytecode: **`False`** (`BOOK_GATE_ENABLED=True`, `CLAUSE_A=True`) |
| `CLAUSE_B` still False | same bytecode: **`BOOK_GATE_CLAUSE_B_ENABLED = False`** |
| 🔴 **book-gate counter untouched at 29/200** | rows carrying `book_gate_opp_pctl`: **29**; refusals ever: **0**. Identical to the 15:20 pass. |
| **Mercury-SOL untouched** | 🔴 `/mnt/volume_nyc1_1780480650620/mercury-sol` **was not opened, read, listed or written.** The only command naming it was `systemctl show mercury-sol -p NRestarts` (**0**, MainPID 2245907) for this table. Its DB was never opened. Its candidate-29 report was read from **kola-reports**, not from the bot. |
| book state at the pass | **FLAT** — 0 open `virtual_positions`, 0 `exit_pending`, 0 `breakeven_jobs`; bot alive (last row `33085`, 2026-09-16 15:15:06 UTC) |

**Provenance.** `matrix_breakdown_json` and `entry_tiers_json` read out of Titan's own `trades.db` (`mode=ro`,
`query_only=1`) for all 82 positions that carry one, 75 of them usable; the contribution rule read from
`signal_matrix.compute_score` on disk at revision `f16c271` and **validated by reconciling the reconstructed
traded-side score against the stored `confluence_score` on 75 of 75 rows**; Spearman ρ with two-sided
permutation p, 40 000 shuffles per test and 60 000 per cohort difference, seed 20260916; candidate numbering
continues from `reports/2026-09-14-2239-mercury-sol-candidate-29-opposing-category-gate-died.md`, whose
four-control frame this pass adopts verbatim and extends with the score confound. Basis:
`reports/2026-09-16-1520-titan-the-exit-advisor-ledger-is-5-of-10-and-positive-the-entry-is-what-bleeds.md`
§3b(i) and §3d.
