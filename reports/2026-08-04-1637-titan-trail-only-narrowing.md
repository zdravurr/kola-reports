# TRAIL-ONLY 0.75R — NOTHING APPLIED. THE MARGIN *IS* THE ARMING BIAS.

**2026-08-04 16:37 UTC · Titan LIVE, real money, flat · HEAD `14319a5`, UNCHANGED — no code shipped**

Your §3 branch fired: **the arming bias swallows the margin → apply nothing.** `TRAIL_MULT_ATR` stays
**2.5** (trail = 1.00R).

⚠️ **`SL_ATR_MULT` was not touched, so 1R does not move and NO §0 boundary is created** — confirmed by
runtime import at 16:37: `SL_ATR_MULT 2.5 · TRAIL_MULT_ATR 2.5 · LONG_PARTIAL_ENABLED True`, `git
status` clean, 0 open positions.

Canon: **§2.51** added in the same commit. Snapshot: `reports/2026-08-04-1637-open-items.md`.

---

## 0. YOUR PREMISE WAS RIGHT, AND IT IS WORTH KEEPING

At unchanged `SL_ATR_MULT`, 1R is fixed, so R is directly comparable across trail widths. **The
methodological trap that rejected the grid genuinely does not apply here** — this pass measures a real
quantity, not a moving denominator. The cell clears (a) on both cohorts:
mech-24 **+2.25 → +4.94**, clean-40 **+2.92 → +5.40**.

## 1. HOW IT FAILS (b) — ON LONGS, NOT SHORTS

| cohort / side | 1.0R (today) | 0.75R | Δ | |
|---|---|---|---|---|
| mech-24 ALL | +2.25 | +4.94 | **+2.69** | pass |
| mech-24 LONG | −3.01 | −2.40 | +0.61 | pass |
| mech-24 SHORT | +5.26 | +7.34 | +2.08 | pass |
| clean-40 ALL | +2.92 | +5.40 | +2.48 | pass |
| **clean-40 LONG** | **−0.47** | **−1.09** | **−0.62** | 🔴 **FAIL** |
| clean-40 SHORT | +3.39 | +6.49 | +3.10 | pass |

**The entire failure is one row: vpos 54, −1.63R — and its actual `close_reason` is `external`.** The
contract never owned that exit, so the replay's number there is a substitution, not a measurement.
Every other long improves (+0.08 … +0.17). **The 9 longs the contract actually owned are +0.61R better
at 0.75R.**

**Your §2.2 suspicion about shorts is disconfirmed.** Its eight runners at 1.0R → 0.75R:

| vpos | 1.0R | 0.75R | Δ | |
|---|---|---|---|---|
| 43 | +1.28 | +1.41 | +0.13 | |
| 44 | +1.28 | +1.41 | +0.13 | |
| **46** | +2.25 | +1.35 | **−0.90** | **cut short** — and it fails §0's filters |
| 48 | +2.00 | +2.24 | +0.23 | |
| 49 | +2.00 | +2.24 | +0.23 | |
| 57 | +1.26 | +1.50 | +0.24 | |
| 58 | +2.39 | +2.63 | +0.24 | |
| 81 | +0.80 | +1.04 | +0.25 | |
| **total** | **+13.27** | **+13.82** | **+0.55** | **7 of 8 improve** |

**0.75R does not destroy the short tail. 0.5R did.** §2.2's exclusion of 0.5/0.6 was right and its
non-verdict on 0.75 was also right.

## 2. 🔴 §3 — WHY IT IS REJECTED ANYWAY. THIS IS THE LOAD-BEARING PART.

**Structural point first, because it narrows the exposure precisely:** the trail acts only *after*
breakeven arms, and the arming condition (+1R) is **independent of trail width**. So an over-armed
replay inflates the 1.0R and 0.75R branches **identically** — the margin between them can only come
from positions that armed. **Only those are at risk. That is exactly where the risk turns out to be.**

Each arming event classified by whether a 5-second poller could have missed it — **ROBUST** = the
arming bar *closed* beyond +1R; **WICK** = only the high/low touched it:

| cohort | armed | ROBUST | WICK | total margin | **ROBUST-only margin** | WICK margin |
|---|---|---|---|---|---|---|
| mech-24 | 14 | 5 | 9 | +2.69R | **+0.84R** | +1.85R (69 %) |
| clean-40 | 23 | 9 | 14 | +2.48R | **−0.23R** | +2.71R (109 %) |

Wick penetrations run **0.0035R to 0.12R** — price kissed +1R by fractions of a percent of 1R and the
bar closed back below it. **On the corroborating cohort, the bias-proof margin is negative.**

### 🔴 The cross-check that makes this a measurement rather than a worry

§2.2 measured the **live** arming rate independently, from what actually happened: **22 % for LONGs
(5 of 23)**. This replay:

```
mech-24 LONG :  replay-armed 44.4%   ROBUST-armed 22.2%   <-- matches §2.2
mech-24 SHORT:  replay-armed 66.7%   ROBUST-armed 20.0%
all-59  LONG :  replay-armed 50.0%   ROBUST-armed 26.9%
```

**The ROBUST rate reproduces the live arming rate almost exactly; the naive replay rate is ~2.5×
too high.** The wick-armed events did not happen live — that is now evidence, not conjecture. And it
means **every trail result in this book that counted them is inflated**, including §2.2's own width
table and §2.50's grid.

**Pre-registration figures, recorded although nothing ships:**
- **Last 25 entries: 11 change, net +2.14R — of which +1.07R (50 %) is wick-armed.**
- **Live era (n=7): −3.04 → −2.55 (Δ+0.49R), of which only +0.25R is robust-armed.**

## 3. ON YOUR RELAXATION OF (b) — YOU ASKED ME TO PUSH BACK, SO: IT IS RIGHT, AND IT IS MOOT

The distinction you drew is **correct and worth keeping in the book**: *mechanical* asymmetry (shorts
have runners with MFE 1.87R–3.40R; longs arm at 22 %) is a different claim from *outcome* asymmetry
(p=0.19), and it is a legitimate basis for a side-specific trail. I would not have objected to it.

**It simply is not exercised here: the failure is on LONGS, not shorts.** If the evidence leaned
anywhere it would be toward a **SHORT-only** narrowing — shorts improve on both cohorts by +2.08R and
+3.10R — which is the mirror image of the rule your relaxation authorises. **I am not inventing that
rule from a discovery made after the fact**, and §2 above would reject it anyway: the short side's
margin is the most wick-dependent of all (9 of 10 armed shorts in mech-24 are wick-armed).

## 4. 🔴 THE REVIEW POINT IS THE REAL PROBLEM — AND WAITING WILL NOT FIX IT

In the unit you specified — **ARMED positions per side** — robustly-armed positions accrue at
**15 of 59 over 72 days = 0.12/day**. **20 armed per side ≈ 335 days.** At 0.47 entries/day behind the
EMA gate, **this axis cannot be settled by live accumulation in any useful horizon.** You were right
that arming is the binding constraint; it is more binding than §2.2's 5-month estimate because the
entry rate has since halved.

**What can settle it, and it is not waiting:** `position_excursion_samples` holds **3,492 rows of real
polled prices** at 60 s cadence, per position — the ground truth for what the engine actually saw. **A
replay validated against those samples instead of 5m candle wicks would answer the trail question
without waiting a year, and would re-date every prior trail result in this file.** That is the honest
successor to this pass, and it is recorded as such rather than promised.

## 5. SCOPE

Untouched: `SL_ATR_MULT`, the EMA envelope gate, the HTF cascade, the FLAT floor, Variant-B, the score
bars, the risk gates, both advisor prompts, and the exit advisor's inputs. **There is no diff** — no
snapshot, no `py_compile`, no restart, because nothing is applied. Measurement ran read-only against
`trades.db` and the cached BingX 5m candles; **no table was written**.
