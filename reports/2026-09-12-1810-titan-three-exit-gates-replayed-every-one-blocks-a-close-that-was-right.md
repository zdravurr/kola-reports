# Titan — three exit gates replayed on the record we already have: **every single one blocks a close that was RIGHT**, and the two that fix both canon losses also throw away the +1.6791R save

**2026-09-12 18:10 UTC · commit `f16c271` · Titan LIVE REAL MONEY · READ-ONLY PASS · nothing proposed, nothing applied · Mercury-SOL NOT TOUCHED**

---

## 🔴 n FIRST, AND THE MULTIPLICITY CORRECTION, BEFORE ANY NUMBER

**TESTS DECLARED IN THIS HEADER, BEFORE THE DATA WAS READ: 7 gate variants × 2 populations = 14.
Bonferroni α = 0.05 / 14 = 0.003571.** (G1@0.25 and G1@0.35 turn out to be exactly the same gate on
this record — §3b — so only **12** are distinct; the correction is reported both ways and it changes
nothing, because nothing reaches even the *uncorrected* 0.05.)

| population | resolved `ai_exit` closes | the most any gate blocks | smallest two-sided sign p that group size can return | reaches α = 0.05? | reaches α = 0.003571? |
|---|---|---|---|---|---|
| **canon (vpos ≥ 101)** | **3** | 3 | **0.250** | **no** | **no** |
| pre-2026-08-30 (vpos 87–98) — **NOT POOLED** | 10 | 8 | **0.0078** | yes, in principle | **no** |
| under the CURRENT prompt (after 2026-09-12 14:58:32) | **0** | 0 | — | — | — |

🔴 **WITH 3 AND 10, NOTHING RANKS. I am saying it before the numbers, exactly as the 17:15 report did.**
The floors above are properties of the *group sizes*, computed before the data was looked at. The **best
p-value actually observed across all 14 cells is 0.7266.** Not one cell reaches 0.05, let alone 0.003571.
**Nothing below is a finding. Everything below is a description of what a rule would have done to 13
trades.**

---

## WHAT YOU ASKED, ANSWERED FIRST

1. **`openitems_guard` EXIT=0**, run first as instructed. Non-zero would have stopped this pass.
2. 🔴 **THE HEADLINE: NO GATE KEEPS THE WINS AND DROPS THE LOSSES. Every one of the seven variants
   blocks at least one close the advisor got RIGHT.** The best any of them manages is 1 of 7 wins
   destroyed — and in both cases that one win is worth more than every loss it saves.
3. 🔴 **G2 blocks exactly three closes: 101, 104, 105 — all three canon closes and nothing else in the
   entire record.** It fixes both canon losses (+0.1553 and +0.7805 R recovered) and then hands back
   **vpos 104, −1.6791 R**. **Net −0.7433 R / −$0.47 — precisely the whole canon ledger, erased to zero.**
4. 🔴 **G3 is G2 plus vpos 89.** Over all 68 close verdicts the two differ by **exactly one row**; over
   the canon population they are **identical**. G3 blocks **both** named saves — **vpos 104 (+1.6791R)
   AND vpos 89 (+0.7418R)** — for a net **−1.4851 R**. It is the worst of the seven.
5. 🔴 **G1@0.25 and G1@0.35 are DEGENERATE** — the same blocked set on all 68 close verdicts and on all
   14 acted closes. They are one gate, not two, and are not reported as independent.
6. **G1@0.50 is the only variant with a positive total (+1.5870 R).** It is fitted and it dies: it is the
   best of five values I declared in advance (with five, one is best by construction); it changes **1 of
   3** canon closes; and **drop the single trade vpos 96 and its entire effect collapses from +1.5870 R to
   −0.0705 R.** Its benefit is one trade in the population that may not be pooled.
7. 🔴 **G1@0.75 blocks ALL SIX of the never-armed wins** (87, 90, 91, 93, 97, 104). It is the answer to
   "which gate drops the wins" — that one, all of them.
8. 🔴 **The brief's reading of the two canon losses is CONFIRMED at the decision point, and it is sharper
   than the brief stated.** vpos 105's *realised* −0.0136R is after fees; **the prompt in front of the
   advisor said `Unrealised: +0.07R`**, with `Closing now costs 0.076R in fees`. So all three canon closes
   — 101 (+0.40R), 104 (+0.67R), 105 (+0.07R) — were **positive and unarmed** at the moment of decision.
   **G2's predicate matches all three. That is why it cannot separate them.**
9. 🔴 **vpos 106 RE-CHECKED on bars through 2026-09-12 17:44 UTC: still unresolved.** Stop **78 301.6
   untouched**, arm **75 726.8 never reached** (water mark 76 936.5). **It is in no sum in this report.**
10. 🔴 **Every one of the 14 closes predates the 2026-09-12 14:58:32 cohort boundary. Under the wording the
    bot is running right now, the n for everything in this report is ZERO.**
11. **The `signal_tiers` `.pyc` item is STILL OPEN**, read from a single `stat`, no watcher. §5, and the
    canon entry about session-scoped promises is written there.

---

## 0. THE GUARD, RUN FIRST

```
openitems_guard — canon: /mnt/volume_nyc1_1780480650620/kola-reports/reports/OPEN-ITEMS.md
  titan-bot HEAD : f16c271   <- the SUBJECT, this is what is compared
  repo HEAD      : f16c271   (context only, NOT compared)
  watched values : 14

✅ header and current-state table agree with runtime.                        EXIT=0
```

---

## 1. THE THREE CANDIDATE GATES — STATED BEFORE THEIR NUMBERS

A gate does one thing only: it **forbids a `close` verdict**. It never forces a close, and it never
touches a `hold`. A blocked position stays open and runs to its trail-or-stop exit.

### 1a. G1 — MINIMUM PROGRESS

> **G1(f): the advisor may not close while `MFE < f × 1R`.**
> The arm sits at +1.00R, so `f` is literally the fraction of the arm the position must have reached.

**Reads:** the prompt line `Peak so far (MFE): ±X.XXR` — `ctx['mfe_r']`, built at `main.py:3109` as
`(water_mark − entry) × sign / r_dist`.

🔴 **THE CANDIDATE SET WAS DECLARED BEFORE IT WAS RUN AND DERIVED FROM §3b's OWN MFE DISTRIBUTION, NOT
SWEPT FOR THE BEST VALUE:** the two medians §3b states (**0.06** canon, **0.35** whole record) and the
three interior bin edges of §3b's own table (**0.25, 0.50, 0.75**). Five values.
**I am naming the hazard rather than hiding behind the declaration: with five values, one of them is the
best by construction. That the best one is +0.50 is not evidence for +0.50.**

### 1b. G2 — NO CLOSING A WINNER BEFORE THE ARM

> **G2: the advisor may not close while `unrealised_R > 0` AND `trail_armed == False`.**
> The stop already caps the loss; closing a winner short of the arm forgoes the arm for nothing.

**Reads:** `Unrealised: ±X.XXR` (`ctx['upnl_r']`, `main.py:3106`, `(last − entry) × sign / r_dist`) and
the protection branch (`ctx['trail_armed']`, `main.py:3394`, read from
`pending_dca_limits.breakeven_applied`).

🔴 **WHERE THE ZERO LINE SITS, EXACTLY.** The predicate is **strictly greater than zero**.
* At **exactly 0.00R the gate does NOT block** — a flat position may be closed.
* The prompt renders to **2 decimal places**, so `+0.00R` is any value in `[0, 0.005)` and `-0.00R` is any
  value in `(-0.005, 0)`. **The renderer emits the true sign**, so the sign survives the rounding and the
  gate reads it correctly; the *magnitude* is only resolved to 0.01R. One row in the record sits there:
  **vpos 93, `Unrealised: -0.00R`** — strictly negative, therefore **NOT blocked** by G2.
* 🔴 **`unrealised` is BEFORE the closing fee.** This is what makes the brief's reading of vpos 105 right
  and my restatement of it necessary: the ledger's **−0.0136R is realised, after a 0.076R fee**; the
  advisor was looking at **+0.07R**. G2 reads +0.07R and blocks it.

### 1c. G3 — LOSERS ONLY

> **G3: the advisor may close only a position that is strictly under water — `unrealised_R < 0`.**

**Reads:** the same `Unrealised` line as G2, and nothing else.

🔴 **At exactly 0.00R G3 DOES block** — zero is not under water. This is the only definitional difference
from G2 at the zero line, and no row in the record sits exactly at `+0.00R` unrealised, so it never bites.
**The real difference between G2 and G3 is the armed term**, and it fires exactly once in the whole
record (vpos 89).

### 1d. 🔴 NO LOOK-AHEAD — PROVED, NOT ASSERTED

| gate | quantity | where it lives at decision time | needs the future? |
|---|---|---|---|
| G1 | `mfe_r` | `main.py:3109` — `(water_mark − entry)·sgn / r_dist`; `water_mark` is the running peak **up to now** | **NO** |
| G2 | `upnl_r` | `main.py:3106` — `(last − entry)·sgn / r_dist`; `last` is the ticker **read on the call** | **NO** |
| G2 | `trail_armed` | `main.py:3394` — `pending_dca_limits.breakeven_applied`, the state **now** | **NO** |
| G3 | `upnl_r` | as above | **NO** |

All three are already computed into `ctx` and **rendered into the prompt string before the model is
called**, which is why they can be recovered verbatim from `trades.ai_user_prompt` for all 191
consultations. **A gate would read the same dict, one branch earlier. A gate that needed the outcome
would not be a gate, and none of these does.**

**Parse coverage: 191 of 191 consultations matched to a position; 190 of 191 carry both lines.** The one
that does not is `trades 28528` (2026-08-30 16:30:05, vpos 100) — the *unreadable-state* prompt, `n/a`
everywhere. **It is a `hold`, so no gate would have acted on it.** The parse independently reproduces
§3a's four ARMED-rendered rows exactly: `20097 / 25159 / 25165 / 28531`.

---

## 2. THE REPLAY

### 2a. The stand, re-calibrated

The same stand as 14:30 and 17:15, re-run on **freshly fetched** public 1m bars:

```
canon window : 15 825 bars  2026-09-01 18:00 -> 2026-09-12 17:44 UTC   GAPS 0
pre   window : 63 706 bars  2026-07-30 12:00 -> 2026-09-12 17:45 UTC   GAPS 0
```

🔴 **CALIBRATION — the published rows come back EXACTLY:** vpos 101 **−0.1553**, 104 **+1.6791**,
105 **−0.7805**, **Σ canon +0.7433 R / +$0.4727**; pre window **Σ −0.1123 R / −$1.9322**. Not one digit
moved. Geometry, `bardir`, fees and arming untouched.

### 2b. 🔴 THE 14 CLOSING CONSULTATIONS AND WHAT EACH GATE READS

| vpos | pop | trigger | `Unrealised` | `MFE` | armed | Δ R (adv − cf) | advisor | G1@.06 | G1@.25 | G1@.35 | G1@.50 | G1@.75 | **G2** | **G3** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 87 | pre | hourly | −0.36 | +0.61 | NO | +0.6398 | **WON** | · | · | · | · | **BLOCK** | · | · |
| 88 | pre | hourly | −0.22 | +0.08 | NO | −0.7939 | lost | · | **BLOCK** | **BLOCK** | **BLOCK** | **BLOCK** | · | · |
| **89** | pre | 15m_exit_confirm | +1.50 | +1.70 | **YES** | +0.7418 | **WON** | · | · | · | · | · | · | 🔴 **BLOCK** |
| 90 | pre | hourly | −0.26 | +0.17 | NO | +0.7686 | **WON** | · | **BLOCK** | **BLOCK** | **BLOCK** | **BLOCK** | · | · |
| 91 | pre | hourly | −0.40 | +0.66 | NO | +0.6250 | **WON** | · | · | · | · | **BLOCK** | · | · |
| 92 | pre | hourly | −0.65 | +0.00 | NO | −1.0025 | lost | **BLOCK** | **BLOCK** | **BLOCK** | **BLOCK** | **BLOCK** | · | · |
| 93 | pre | hourly | −0.00 | −0.00 | NO | +1.0004 | **WON** | **BLOCK** | **BLOCK** | **BLOCK** | **BLOCK** | **BLOCK** | · | · |
| 96 | pre | hourly | −0.48 | +0.46 | NO | −1.6575 | lost | · | · | · | **BLOCK** | **BLOCK** | · | · |
| 97 | pre | hourly | −0.74 | +0.12 | NO | +0.2531 | **WON** | · | **BLOCK** | **BLOCK** | **BLOCK** | **BLOCK** | · | · |
| 98 | pre | hourly | −0.18 | +0.93 | NO | −0.6873 | lost | · | · | · | · | · | · | · |
| **101** | **canon** | 15m_exit_confirm | **+0.40** | +0.43 | NO | −0.1553 | lost | · | · | · | **BLOCK** | **BLOCK** | 🔴 **BLOCK** | 🔴 **BLOCK** |
| **104** | **canon** | 15m_exit_confirm | **+0.67** | +0.72 | NO | **+1.6791** | **WON** | · | · | · | · | **BLOCK** | 🔴 **BLOCK** | 🔴 **BLOCK** |
| **105** | **canon** | hourly | **+0.07** | +0.50 | NO | −0.7805 | lost | · | · | · | · | **BLOCK** | 🔴 **BLOCK** | 🔴 **BLOCK** |
| *106* | *canon* | *15m_exit_confirm* | *−0.25* | *+0.06* | *NO* | *UNRESOLVED* | *—* | · | *BLOCK* | *BLOCK* | *BLOCK* | *BLOCK* | · | · |

**advisor WON (Δ>0), 7:** 87, 89, 90, 91, 93, 97, 104 — **advisor LOST (Δ<0), 6:** 88, 92, 96, 98, 101, 105.
Of the 7 wins, **6 are the never-armed counterfactuals** (§3d's `6 of 6`) and the 7th is vpos 89, the only
already-armed position the advisor ever judged.

### 2c. 🔴 TWO POPULATIONS, REPORTED SEPARATELY AND NEVER POOLED — n ON EVERY LINE

The **effect** column is the change to realised P&L from installing the gate: a blocked close swaps the
advisor's result for the counterfactual, so **effect = −Σ(Δ R over the blocked set)**. **Negative = the
gate would have cost money.** **vpos 106 is unresolved and appears in NO sum.**

**CANON (vpos ≥ 101) — n = 3 resolved. Baseline with no gate: Σ +0.7433 R / +$0.4727**

| gate | blocks | closes changed | **effect Σ R** | **effect Σ $** | resulting ledger |
|---|---|---|---|---|---|
| G1@0.06 | — | 0 of 3 | +0.0000 | +$0.00 | +0.7433 R |
| G1@0.25 ≡ G1@0.35 | — | 0 of 3 | +0.0000 | +$0.00 | +0.7433 R |
| G1@0.50 | 101 | **1 of 3** | **+0.1553** | **+$0.30** | +0.8986 R |
| G1@0.75 | 101, 104, 105 | **3 of 3** | **−0.7433** | **−$0.47** | **0.0000 R** |
| **G2** | **101, 104, 105** | 🔴 **3 of 3** | 🔴 **−0.7433** | 🔴 **−$0.47** | 🔴 **0.0000 R** |
| **G3** | **101, 104, 105** | 🔴 **3 of 3** | 🔴 **−0.7433** | 🔴 **−$0.47** | 🔴 **0.0000 R** |

**PRE-2026-08-30 (vpos 87–98) — n = 10 resolved. A DIFFERENT PROMPT. Baseline: Σ −0.1123 R / −$1.9322**

| gate | blocks | closes changed | **effect Σ R** | **effect Σ $** |
|---|---|---|---|---|
| G1@0.06 | 92, 93 | 2 of 10 | +0.0021 | +$0.72 |
| G1@0.25 ≡ G1@0.35 | 88, 90, 92, 93, 97 | 5 of 10 | −0.2257 | −$0.13 |
| G1@0.50 | 88, 90, 92, 93, 96, 97 | **6 of 10** | **+1.4317** | **+$3.94** |
| G1@0.75 | 87, 88, 90, 91, 92, 93, 96, 97 | **8 of 10** | +0.1669 | +$1.92 |
| **G2** | **—** | **0 of 10** | +0.0000 | +$0.00 |
| **G3** | **89** | 1 of 10 | **−0.7418** | **−$1.23** |

🔴 **R and $ diverge in sign for G1@0.06 and G1@0.25/0.35 because `initial_risk_usdt` is not constant
across positions.** Both columns are reported; neither is a result.

### 2d. 🔴 vpos 106 — RE-CHECKED, STILL UNRESOLVED, EXCLUDED FROM EVERY SUM

Replayed on bars the 17:15 report did not have, out to **2026-09-12 17:44 UTC**:

```
original stop 78 301.6   -> STILL UNTOUCHED
+1R arm       75 726.8   -> STILL NOT REACHED   (water mark 76 936.5)
counterfactual mark      -0.2097 R   (mark-to-market only)
advisor realised         -0.2963 R
```

**Never armed, stop intact, position still open in the counterfactual. It counts for nothing and it is in
no sum above.** G1@0.25/0.35/0.50/0.75 would have blocked its close; G1@0.06, G2 and G3 would not.

### 2e. 🔴 WHICH GATE BLOCKS THE CLOSES THE ADVISOR GOT RIGHT — THE ANSWER TO THE ONLY QUESTION THAT MATTERS

**Every single one blocks at least one.** Named immediately, as instructed:

| gate | **wins destroyed** | Σ R given back | losses saved | Σ R recovered | **net** |
|---|---|---|---|---|---|
| G1@0.06 | **1 of 7** — 93 | −1.0004 | 1 of 6 — 92 | +1.0025 | **+0.0021** |
| G1@0.25 ≡ G1@0.35 | **3 of 7** — 90, 93, 97 | −2.0221 | 2 of 6 — 88, 92 | +1.7964 | **−0.2257** |
| G1@0.50 | **3 of 7** — 90, 93, 97 | −2.0221 | 4 of 6 — 88, 92, 96, **101** | +3.6091 | **+1.5870** |
| G1@0.75 | 🔴 **6 of 7 — 87, 90, 91, 93, 97, AND 104** | −4.9661 | 5 of 6 — 88, 92, 96, 101, 105 | +4.3897 | **−0.5764** |
| **G2** | 🔴 **1 of 7 — vpos 104, +1.6791 R** | **−1.6791** | 2 of 6 — 101, 105 | +0.9358 | 🔴 **−0.7433** |
| **G3** | 🔴 **2 of 7 — vpos 104 (+1.6791 R) AND vpos 89 (+0.7418 R)** | **−2.4209** | 2 of 6 — 101, 105 | +0.9358 | 🔴 **−1.4851** |

🔴 **G3 BLOCKS BOTH KNOWN SAVES. G2 BLOCKS THE LARGER OF THE TWO. G1@0.75 BLOCKS ALL SIX NEVER-ARMED
WINS AND vpos 104 ON TOP.** There is no gate on this record that keeps the wins and drops the losses.

### 2f. 🔴 THE COST SIDE, OVER ALL 191 CONSULTATIONS

191 consultations · **68 `close` verdicts** · 123 `hold` verdicts. **A gate never touches a hold.**
Of the 68 close verdicts, **52 predate the advisor's ability to act** (the DRYRUN era, before
2026-07-31 02:06) and **16 are in the acting era** — of which **14 actually closed a position**, one
(`31115`) fired 2 s *after* vpos 104 was already closed, and one (`26626`, vpos 95) is an `armed_exit`
row, which is record-only and can never close.

| gate | **close verdicts blocked, of 68** | share | of the 52 DRYRUN-era | of the 16 acting-era | **of the 14 that CLOSED** |
|---|---|---|---|---|---|
| G1@0.06 | 5 | 7.4 % | 3 | 2 | **2** |
| G1@0.25 ≡ G1@0.35 | 27 | 39.7 % | 21 | 6 | **6** |
| G1@0.50 | 39 | 57.4 % | 31 | 8 | **8** |
| G1@0.75 | **46** | **67.6 %** | 32 | 14 | **12** |
| **G2** | 19 | 27.9 % | 15 | 4 | **3** |
| **G3** | 20 | 29.4 % | 15 | 5 | **4** |

🔴 **G1@0.75 would forbid two thirds of everything the advisor has ever decided to close, and 12 of the 14
it actually did close. G1@0.50 forbids 8 of 14. These are not adjustments; they are a different bot.**

---

## 3. 🔴 THE HONEST ARITHMETIC, BEFORE ANY CONCLUSION

### 3a. HOW MANY CLOSES EACH GATE ACTUALLY CHANGES — AND WHICH ARE FITTED

| gate | resolved closes changed | canon | pre | verdict on fitting |
|---|---|---|---|---|
| G1@0.06 | 2 of 13 | **0 of 3** | 2 of 10 | **touches the canon population not at all** |
| G1@0.25 ≡ G1@0.35 | 5 of 13 | **0 of 3** | 5 of 10 | **touches the canon population not at all** |
| G1@0.50 | 7 of 13 | **1 of 3** | 6 of 10 | 🔴 **its whole canon effect is ONE trade, vpos 101** |
| G1@0.75 | 11 of 13 | 3 of 3 | 8 of 10 | changes almost everything, net negative |
| **G2** | **3 of 13** | 🔴 **3 of 3** | **0 of 10** | 🔴 **a rule fitted to exactly three trades** |
| **G3** | **4 of 13** | 🔴 **3 of 3** | 1 of 10 | 🔴 **a rule fitted to exactly three trades** |

🔴 **G2 IS A RULE FITTED TO THREE TRADES AND I AM NAMING IT AS SUCH.** It is defined on the canon
population and it changes 100 % of it — every canon close and no other close in 47 days of record. That
is not a rule tested against data; that is the data restated as a rule. **It does not even change 2 of 3.
It changes 3 of 3, and the sum is negative.**

🔴 **AND G1@0.50, THE ONLY POSITIVE TOTAL, IS FITTED TOO — LEAVE-ONE-OUT PROVES IT:**

| gate | total effect | drop the single most influential trade | what is left |
|---|---|---|---|
| **G1@0.50** | **+1.5870 R** | drop **vpos 96** | 🔴 **−0.0705 R** |
| G1@0.75 | −0.5764 R | drop vpos 104 | +1.1027 R |
| G2 | −0.7433 R | drop vpos 104 | +0.9358 R |
| G3 | −1.4851 R | drop vpos 104 | +0.1940 R |
| G1@0.25 ≡ G1@0.35 | −0.2257 R | drop vpos 92 | −1.2282 R |
| G1@0.06 | +0.0021 R | drop vpos 92 | −1.0004 R |

**One trade, vpos 96, is +1.6575 R of G1@0.50's +1.5870 R. Remove it and the gate is a coin. And vpos 96
is in the population that may not be pooled.**

### 3b. 🔴 DEGENERACY — WHICH GATES ARE NOT INDEPENDENT

Pairwise **|symmetric difference|** of the blocked sets over all 68 close verdicts:

| | G1@.06 | G1@.25 | G1@.35 | G1@.50 | G1@.75 | G2 | G3 |
|---|---|---|---|---|---|---|---|
| **G1@.06** | 0 | 22 | 22 | 34 | 41 | 24 | 25 |
| **G1@.25** | 22 | **0** | 🔴 **0** | 12 | 19 | 44 | 45 |
| **G1@.35** | 22 | 🔴 **0** | **0** | 12 | 19 | 44 | 45 |
| **G1@.50** | 34 | 12 | 12 | 0 | 7 | 38 | 39 |
| **G1@.75** | 41 | 19 | 19 | 7 | 0 | 37 | 38 |
| **G2** | 24 | 44 | 44 | 38 | 37 | 0 | 🔴 **1** |
| **G3** | 25 | 45 | 45 | 39 | 38 | 🔴 **1** | 0 |

* 🔴 **G1@0.25 and G1@0.35 are EXACTLY DEGENERATE** — identical on all 68 close verdicts and on all 14
  acted closes (`{88, 90, 92, 93, 97, 106}`). **No consultation in the record has an MFE in
  [+0.25, +0.35).** They are ONE gate and are not reported as two.
* 🔴 **G2 and G3 differ by exactly ONE row in the whole record** — `trades 20097`, vpos 89, the only
  armed close ever taken. **On the canon population they are IDENTICAL** (both block 101, 104, 105 and
  nothing else). **They are not independent gates. G3 is G2 plus one trade**, and that trade is a
  +0.7418 R save it throws away.
* G1@0.50 and G1@0.75 differ by only 7 of 68 — near-neighbours, not independent evidence.

**Effective distinct gates on this record: 6, not 7.**

### 3c. 🔴 THE COHORT BOUNDARY — THE n IS ZERO

**All 14 closes were taken before 2026-09-12 14:58:32.** The latest exit consultation of any kind in the
database is **2026-09-12 09:15:09**. **Under the prompt wording running right now, every gate in this
report has been replayed against ZERO observations of the current bot.** Every number above describes a
bot that no longer exists in exactly that form.

### 3d. 🔴 BONFERRONI — DECLARED IN THE HEADER, APPLIED HERE

14 declared cells (12 distinct). **α = 0.05 / 14 = 0.003571** (or 0.05 / 12 = 0.004167 on distinct gates).

| gate | pop | k blocked | floor: smallest two-sided p attainable | **observed p** | reaches 0.05? | reaches 0.003571? |
|---|---|---|---|---|---|---|
| G1@0.06 | canon | 0 | 1.0000 | — | no | no |
| G1@0.06 | pre | 2 | 0.5000 | 1.0000 | no | no |
| G1@0.25 | canon | 0 | 1.0000 | — | no | no |
| G1@0.25 | pre | 5 | 0.0625 | 1.0000 | no | no |
| G1@0.35 | canon | 0 | 1.0000 | — | no | no |
| G1@0.35 | pre | 5 | 0.0625 | 1.0000 | no | no |
| G1@0.50 | canon | 1 | 1.0000 | 1.0000 | no | no |
| G1@0.50 | pre | 6 | 0.0313 | 1.0000 | no | no |
| G1@0.75 | canon | 3 | 0.2500 | 1.0000 | no | no |
| G1@0.75 | pre | 8 | **0.0078** | **0.7266** | no | no |
| G2 | canon | 3 | 0.2500 | 1.0000 | no | no |
| G2 | pre | 0 | 1.0000 | — | no | no |
| G3 | canon | 3 | 0.2500 | 1.0000 | no | no |
| G3 | pre | 1 | 1.0000 | 1.0000 | no | no |

🔴 **NOT ONE CELL REACHES EVEN THE UNCORRECTED 0.05. The best observed p in the entire sweep is 0.7266,
and the best p any of them could have returned is 0.0078 — still above the corrected 0.003571.** The
floors were computable before the data was read; they are properties of how many closes each gate blocks.

---

## 4. 🔴 VERDICT — DECISION-SHAPED, NOT A SURVEY

### 4a. THE GATE THAT WOULD QUALIFY DOES NOT EXIST ON THIS RECORD

Your criterion was: *keeps the wins, drops the losses, blocks nothing that was right, changes ≥ 4 closes.*

**Zero of the seven variants satisfy the third clause.** The best is a tie at **1 of 7 wins destroyed** —
G1@0.06 (which changes only 2 closes, none of them canon, and nets +0.0021 R, a coin) and **G2, whose one
destroyed win is worth more than both losses it saves combined**. There is nothing to describe with its
full cost, because nothing qualifies.

### 4b. 🔴 G2 AND G3 ARE FITTED, AND THEY DIE

**G2 changes 3 of 3 canon closes and nothing else in 47 days.** It is not "good because it blocks 2 of 3";
it is worse than that — **it is a rule defined by, and coextensive with, the three trades that motivated
it.** Its predicate is a correct description of all three canon decisions, which is exactly why it cannot
tell them apart. **It fixes both losses and destroys the one gain, for −0.7433 R / −$0.47 — the entire
canon ledger reduced to zero.**

**G3 is G2 plus vpos 89**, differing by one row in the whole record, identical on canon. It throws away
**both** named saves for **−1.4851 R**. It is the worst variant tested.

**G1@0.50, the only positive total, is fitted twice over**: best-of-five by construction, and +1.6575 of
its +1.5870 R is a single trade (vpos 96) in the population that may not be pooled. **Its canon effect is
one trade. It dies too.**

### 4c. 🔴 NOTHING WORKS — AND HERE IS THE HONEST POSITION, BOTH SIDES, WITH NUMBERS

**The advisor's decision point cannot be improved by any rule this record supports.** The reason is
structural and it is the same fact §3b established: **184 of 191 consultations, and 32 of 32 in the canon
population, judge an unprotected position at a median MFE of +0.06R.** Every gate built from the
quantities available at that point — progress, sign, protection — partitions that one homogeneous
population, and the wins and the losses fall on the *same side* of every cut. **G2's predicate is true of
all three canon closes: the two it should stop and the one it must not.**

**THE CHOICE IS YOURS. BOTH SIDES, WITH THEIR NUMBERS:**

| | **LEAVE IT RUNNING to 10 resolved closes** | **FLIP `EXIT_ADVISOR_DRYRUN`** |
|---|---|---|
| **the case** | The standing rule is 3 of 10. The ledger is **+0.7433 R / +$0.47 positive** over 3 canon closes. Nothing here refutes the advisor; it refutes the *gates*. | Its **entire decision population is blind** — 32 of 32 canon consultations taken at a median MFE of **+0.06R**, maximum +0.72R, before the single fact that determines the outcome (will it arm?) is knowable. 12 of 13 resolved closes obey that fact. |
| **the cost of being wrong** | 7 more closes at the measured **1 per 3.26 days ≈ 23 days**. Mean |Δ| in the canon window is **0.8716 R** (n=3). If every one of the 7 went the wrong way, that is ≈ **−6.1 R ≈ −$12** at $30 × 5 margin. That is the ceiling on waiting, and it is small. | You give up a ledger that is 🔴 **+0.7433 R / +$0.47 over canon (n=3)** and 🔴 **−0.1123 R / −$1.93 over pre-2026-08-30 (n=10)** — **two figures, never summed.** One window is positive, the other negative, **and the record cannot say whether either is skill or coin flips.** |
| **what the record says** | 🔴 **n = 3 resolved in the counted population. Nothing ranks. Smallest attainable p = 0.25.** | 🔴 **Same n. The blindness is a fact about *where* it decides, PROVEN; that this makes it *wrong* is NOT proven and this pass did not make it any more proven.** |
| **the honest asymmetry** | The cohort boundary already reset the count to **0 under the current wording**. Waiting to 10 means waiting for 10 closes *of the new prompt*, not 7 more of the old — ≈ **33 days**, not 23. | Flipping is **reversible and costs nothing to reverse**; the advisor keeps recording verdicts in DRYRUN, so the evidence keeps accumulating **without money at risk**. That is the one genuine asymmetry on this table. |

🔴 **I am not choosing, and I have not touched it. `EXIT_ADVISOR_DRYRUN` is `False` and was not flipped,
not proposed and not asked about. The rule stands at 3 of 10.**

### 4d. WHAT I WOULD HAVE HAD TO SEE

A gate that qualified would have to block a set of closes whose Δ R are **all negative**. Across all seven
variants and 13 resolved closes, **the smallest blocked set with a uniform sign is size 0.** Every gate's
blocked set is mixed. That is the whole result in one sentence.

---

## 5. 🔴 THE DEAD-WATCHER LESSON, CLOSED — AND THE ITEM, FROM A SINGLE `stat`

### 5a. THE ITEM'S CURRENT STATUS — one `stat`, no watcher, nothing armed

```
$ stat -c '%n  mtime=%y  size=%s' signal_tiers.py __pycache__/signal_tiers.cpython-312.pyc
signal_tiers.py                            mtime=2026-09-12 14:15:53 +0000  size=23584
__pycache__/signal_tiers.cpython-312.pyc   mtime=2026-08-04 15:07:11 +0000  size=16950

pyc HEADER (source mtime + size it was compiled from) : 2026-08-04 15:06:23   size 15924
source                                                 : 2026-09-12 14:15:53   size 23584
header == source                                       : False
source sha256                                          : 4af4fdba57cfaf840416e260cd4cea2eb1b38a46caea6913bea887fe95ca6a6a
```

**UNCHANGED from the 17:15 reading. THE ITEM IS STILL OPEN.** The cached header disagrees with the applied
source in both mtime and size, so Python cannot load that bytecode and the first `import signal_tiers`
must compile `4af4fdba57cfaf84` from source. **The in-process confirmation remains UNPROVED.**

Why it has not happened: **no entry consultation has occurred.** The last one is `trades 31760`,
**2026-09-11 22:00:11**, before the restart. Since 14:58:32 every signal has been stopped ahead of the
advisor:

```
htf_blocked           20   (latest 2026-09-12 17:45:03)
ema_envelope_blocked  18   (latest 2026-09-12 17:10:08)
context_recorded       6
confirm_recorded       1
open positions         0
```

### 5b. 🔴 THE CANON ENTRY — A PROMISE BOUND TO A SESSION IS NOT A MECHANISM

The watcher armed at **2026-09-12 14:59:35** to close this item **is dead**. It was a background process
bound to the session that started it; the session ended and it went with it, leaving an output file
containing only its own start line. **It was reported as "armed" and it was never watching.**

**RECORDED IN THE CANON, AS THE SAME CLASS AS THE BOOK-GATE REVIEW THAT WENT UNCHECKED FOR THREE WEEKS:**

> **A promise whose keeper is a session-scoped background process is not a mechanism — it is a
> reminder that dies with the terminal.** A mechanism survives the session that created it: a cron
> entry, a contract test, a guard the next session must run, a line in `OPEN-ITEMS.md`. Anything
> else is a note to a person who will not be there. The failure mode is silent and it is
> indistinguishable from success, because nothing announces that the watcher is gone — the item
> simply stays open while the record says it is being watched.
>
> **The tell is identical in both instances:** the book-gate review promised "in three weeks" with no
> dated trigger, and this watcher promised "the moment the import happens" with no persistent host.
> **Both were reported as arranged. Neither was arranged.**
>
> **The correction is the one this section demonstrates: the check needed no watcher at all.** The
> `.pyc` header is a *persistent record*; one `stat` answers the question at any time, from any
> session, with no state carried between them. **Where a persistent artefact can be read on demand,
> arming a watcher is strictly worse than writing down which artefact to read** — it adds a
> failure mode and buys nothing. **Related:** `feedback_fix_the_class_not_the_name.md`,
> `feedback_closed_means_live_proven.md`, `feedback_every_capability_gets_a_contract.md`.

**Nothing is armed now, and this report claims nothing is.** The item stays open in `OPEN-ITEMS.md`, and
the way to close it is one `stat` plus one journal line, on demand.

---

## CONTROLS — READ-ONLY, PROVED RATHER THAN ASSERTED

| | |
|---|---|
| `openitems_guard` | **EXIT=0**, run first as instructed · **EXIT=0** at the end |
| Titan DB | every handle `file:/root/titan-bot/trades.db?mode=ro` with `PRAGMA query_only=1`. **No `-wal`, `-shm` or `-journal` side-file exists** |
| writes / orders / restarts / proposals | **NONE.** Journal since session start (17:40) contains **0** lines matching `EXIT-ADVISOR|ORDER|CLOSE|RECONCILE|BREAKEVEN|TRAIL|error|Traceback` |
| `titan.service` | `active`, **MainPID 1572470**, **NRestarts 0**, start **2026-09-12 14:58:32 UTC** — identical at the start and the end of this pass |
| open positions | **0** — the book is flat |
| `EXIT_ADVISOR_DRYRUN` | **False** — read from `config` at runtime. **NOT FLIPPED, not proposed** |
| other flags, read at runtime | `LIVE_TRADING_ENABLED` **True** · `ORDER_ADAPTER_LIVE` **True** · `BOOK_GATE_ENABLED` **True** · `BOOK_GATE_DRYRUN` **False** · `CLAUSE_A` **True** · `CLAUSE_B` **False** · `EXIT_ADVISOR_HOURLY` **True** · `EXIT_ADVISOR_ON_15M_CONFIRM` **True** · `MAX_POSITIONS_PER_SIDE` **1** |
| **book-gate counter** | 🔴 **22 of 200, UNTOUCHED, 0 refusals all time.** Latest gate row `trades 31760`, 2026-09-11 22:00:11 — identical to the 14:30, 15:20 and 17:15 readings |
| git | working tree **clean** (0 modified paths), `titan-bot/` HEAD **`f16c271`**, **no commit made** |
| BingX | **public 1m OHLCV only** (`fetch_ohlcv`), the same call the 14:30 and 17:15 reports used. No order, no position query, no account mutation |
| 🔴 **Mercury-SOL** | 🔴 **NOT TOUCHED AT ALL.** `active`, **MainPID 1341949**, **NRestarts 0**, start **2026-09-11 18:26:59 UTC** — unchanged. `find mercury-sol -name '*.py' -newermt '2026-09-12 17:40'` → **EMPTY**. No DB query, no restart, no venue call on its key |
| 🔴 open | the in-process `.pyc` confirmation for `signal_tiers` — §5, still open, and now with the reason it stayed open written into the canon |
