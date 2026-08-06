# SOL P2 — THE TRAIL IS PROVABLY WRONG. THE REPLACEMENT IS NOT DETERMINED BY THIS BOOK.

**2026-08-06 14:20 UTC · Mercury-SOL (PAPER) · READ-ONLY. NOTHING WAS CHANGED.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`. No file modified — the most recent SOL source
mtime is still `main.py` 13:51:21 from the M4 deletion, which predates this work.
Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched, not read for state, not run** — clean at
`897850b`, workers 2538048/2538082 undisturbed.

## THE ANSWER FIRST

**No cell qualifies under the four conjuncts fixed before the numbers. I am not proposing a value.**

The structural fact stands and needs no statistics: `TRAIL_MULT_ATR = SL_BUFFER_ATR = 2.5` makes the
giveback exactly 1R by identity. **And the grid corroborates it structurally, not statistically:
at b=2.5, trail=1.25R is bit-identical to trail=1.0R in every cohort and on both sides — a trail at
or above 1R never fires before something else does. Above 1R the trail is not a loose mechanism; it
is an inert one.** The current setting sits exactly on that boundary.

The cell that passes all four conjuncts is **not a trail change** — 82% of its benefit comes from
narrowing the stop, and on the trail's own cohort its axis is non-monotone and flat.

---

# 1. THE INSTRUMENT — checked before any result

## a) 🔴 IS ARMING RECORDED? **YES. And it is used, never inferred.**

`mgmt_state_json.breakeven_applied` is present and populated on **all 21** closed positions:
**7 armed, 14 not.** Titan's replay-armed-on-wicks defect has no counterpart here, because the fact
was recorded all along — same as Titan's eventual discovery.

**Validated separately, because the counterfactual needs it.** For a *different* SL_BUFFER_ATR no
record can exist, so arming must be derived from `water_mark` at that b. Before trusting that, I
checked whether the derivation reproduces the record at the control b=2.5:

> **arming inferred from `water_mark` vs `entry ± 2.5×ATR` matches the recorded
> `breakeven_applied` on 21 of 21.**

Including the near-miss: vpos 19 (SHORT) had an arm price of 75.5606 and an MFE of 75.60 — 0.04 away,
inferred *not armed*, and the record agrees. **So `water_mark` is a faithful record of the MFE the
live poller actually saw, not a candle wick it never saw.** That is the precondition Titan paid for,
and it holds here.

## b) 🔴 IS THE REPLAY TRUNCATED AT THE REAL CLOSE? **Yes — and it cannot overrun by construction.**

Samples are written only while a position is open, so every path *ends before* its close. Measured
overruns are all negative (−0.0 s to −256 s). Anything that has not fired by the last sample closes
at the **actual close price at the actual time**.

🔶 **But the same fact has a cost, and it is the one that decides this report:** the path stops up to
five minutes *before* the close, and the trail fires in exactly that window.

## c) 🔴 THE USABLE n — STATED BEFORE ANY RESULT

| | |
|---|---|
| closed positions | **21** |
| with any price path (`position_excursion_samples`) | **13** |
| armed (recorded) | **7** |
| **armed AND with a path — the trail's real cohort** | **4** |
| trailed exits in the book | 4 (vpos 13, 15, 21, 25) |
| **trailed exits with a path** | **3** — vpos 13 has none |

**That is not a grid. It is four observations, three of which are trailed exits.** Said plainly, as
instructed.

🔴 **And the resolution is worse than the count suggests.** The sampler's effective cadence for
vpos 15–24 is a **median 305 s** — thirty times coarser than the 10 s poller whose decisions it is
supposed to reproduce. Only the three most recent positions (25/26/27) were recorded at 13–61 s.

**This is not a footnote — it destroyed one of the four observations:**

> **vpos 21 is the only trailed LONG in the book. Its last sample is at 68,273 s; it lived 68,499 s.
> The final 226 seconds — which contain the entire trail trigger — were never recorded.** The replay
> therefore reports "no change" for vpos 21 at every trail value. That is the sampler's silence, not
> the strategy's indifference.

## d) VALIDATE — reproduce the actual book before reading any counterfactual

**First pass: 20 of 21 reproduced to the cent; vpos 25 was off by exactly −$3.6449.**
Traced rather than waved away: that is precisely `partial_fees`. `partial_pnl` (31.7495) is **already
net** of `partial_fees` (35.3943 − 3.6449), while `total_fees` *includes* them — so my recomputation
double-charged the partial's fee. **The book was right and the formula was wrong.** With the correct
identity, **21 of 21 reproduce to the cent.**

*(Incidental corroboration of P1 from a new angle: `total_fees` includes the partial fee and `net_pnl`
already nets it, which is exactly why the card's Gross − Fees ≠ Net.)*

**Then the replay itself, at the control geometry, against the actual book:**

| | |
|---|---|
| 12 of 13 pathed positions | reproduced **to the cent** — exit reason and dollars |
| vpos 25 | −$1.81, **0.018 R_ref** (the partial modelled at the arming tick, not the exact adapter fill) |
| median \|ΔR_ref\| | **0.000 R** · max **0.018 R** |

**The instrument reproduces the book. Everything below stands on that.**

---

# 2. THE UNIT

Everything is denominated in **R_ref = 2.5 × ATR × size — TODAY's 1R, held FIXED across every cell.**

This is the check that saved Titan from shipping, and it matters here for a concrete reason: SOL's
paper size is `PAPER_FIXED_MARGIN × LEVERAGE / price`, so **size does not depend on `SL_BUFFER_ATR`
— but 1R does.** Ranking in each cell's own R would mean a cell that narrows the stop reports a
larger R on every unchanged trade without a dollar moving. Fees are charged in **real dollars** on
the real traded notional, so as 1R shrinks the fee share grows automatically.

🔶 **One clarification with practical consequence: a trail-only change does NOT move 1R.**
`1R = SL_BUFFER_ATR × ATR × size` contains no trail term. So changing `TRAIL_MULT_ATR` alone leaves R
comparable across the boundary — **no canon boundary is required for it.** Only a change to
`SL_BUFFER_ATR` breaks R comparability and would need the 2026-08-04-style boundary record.

---

# 3. THE GRID

`SL_BUFFER_ATR ∈ {2.0, 2.25, 2.5*}` × `trail-in-R ∈ {0.75, 1.0*, 1.25}`, partial ON (the live config).
The trail is modelled **as the engine runs it** — `trail_pct` a percentage *of the entry* applied *to
the water mark*, so the giveback drifts with MFE, as measured (+1.7% long, −2.5% to −5.8% short).

**sum R_ref (median R_ref) [positions changed]** — control marked `*`

| cohort | b | t=0.75 | t=1.0 | t=1.25 |
|---|---|---|---|---|
| **ALL-13** | 2.0 | −1.91 (−0.58) [10] | −2.44 (−0.58) [9] | −2.69 (−0.58) [10] |
| | 2.25 | −3.70 (−0.66) [9] | −4.12 (−0.66) [9] | −4.27 (−0.66) [9] |
| | 2.5 | −4.39 (−0.66) [3] | **−4.83 (−0.66) [0] \*** | −4.83 (−0.66) [0] |
| **ARMED-4** | 2.0 | 2.91 (0.56) [3] | 2.51 (0.47) [2] | 2.26 (0.43) [3] |
| | 2.25 | **2.94** (0.55) [3] | 2.52 (0.47) [3] | 2.37 (0.44) [3] |
| | 2.5 | 2.92 (0.53) [3] | **2.49 (0.46) [0] \*** | 2.49 (0.46) [0] |
| **LONG-5** | 2.0 | −1.86 [4] | −1.98 [4] | −1.98 [4] |
| | 2.25 | −3.56 [3] | −3.56 [3] | −3.56 [3] |
| | 2.5 | **−3.87 [0]** | **−3.87 [0] \*** | **−3.87 [0]** |
| **SHORT-8** | 2.0 | −0.06 [6] | −0.46 [5] | −0.71 [6] |
| | 2.25 | −0.14 [6] | −0.56 [6] | −0.72 [6] |
| | 2.5 | −0.53 [3] | −0.96 [0] \* | −0.96 [0] |

Win rates are flat across the trail axis (they move only with b: 5→6 of 13 at b=2.0), because the
trail changes *how much* a winner keeps, not *whether* it wins.

## 🔴 THE DECOMPOSITION — is the gain the trail, or a cheaper stop?

| axis | movement | ΔR_ref |
|---|---|---|
| **b alone** (t held at 1.0) | −4.83 → −4.12 → **−2.44** | **+2.39** |
| **t alone** (b held at 2.5) | −4.83 → **−4.39** | **+0.44** |
| corner cell b2.0/t0.75 total | −4.83 → −1.91 | +2.92 |

**≈82% of the corner cell's benefit is the stop-width change, not the trail.** On a cohort that is
ten stop-outs in thirteen, narrowing the stop reduces the loss per stop-out close to arithmetically.
That is not a discovery about the trail.

**And the giveaway is on the trail's own cohort.** On ARMED-4 at t=0.75 the b axis reads
**2.91 → 2.94 → 2.92** — a 0.03 R spread, and **non-monotone**. The stop-width change does
essentially *nothing* to armed positions; all of its apparent benefit lands on the nine unarmed
stop-outs. **It is a stop-width change wearing a trail change's clothes.**

## Which positions actually change under the pure trail change (b=2.5, t 1.0→0.75)

| vpos | side | control | → 0.75R | ΔR_ref |
|---|---|---|---|---|
| 15 | SHORT | trail @78.20 | trail @77.78 | **+0.144** |
| 17 | SHORT | sl @75.82 | trail @75.24 | **+0.182** |
| 25 | SHORT | trail @71.36 | trail @71.24 | **+0.110** |
| 21 | **LONG** | — | — | **unmeasurable — the sampler stopped 226 s before the close** |

**Three. All SHORT.**

---

# 4. THE DECISION — against the four conjuncts fixed in advance

## Candidate A — b=2.5 unchanged, **trail 0.75R**. *The actual P2 question.*

| | |
|---|---|
| (a) beats control on BOTH cohorts | ✅ ALL-13 −4.39 > −4.83 · ARMED-4 2.92 > 2.49 |
| (b) beats it on BOTH sides separately | 🔴 **FAIL** — LONG is **−3.87 vs −3.87, a dead tie, 0 changed.** A tie is not a beat, and the tie is the sampler's artefact (vpos 21) |
| (c) axis monotone through it | ⚠️ weakly — t=1.0 and t=1.25 are identical, so the axis is flat above 1R |
| (d) ≥4 positions change outcome | 🔴 **FAIL — 3** |

## Candidate B — b=2.0, trail 0.75R. *The grid corner.*

| | |
|---|---|
| (a) both cohorts | ✅ −1.91 > −4.83 · 2.91 > 2.49 |
| (b) both sides | ✅ LONG −1.86 > −3.87 · SHORT −0.06 > −0.96 |
| (c) axis monotone through it | 🔴 **FAIL** — on **ARMED-4** the b axis is **2.91 / 2.94 / 2.92**, non-monotone and flat. And on ALL-13 the axis is monotone **to the grid boundary and never turns** — that is a direction, not an optimum |
| (d) ≥4 change | ✅ 10 |

**Candidate B is also disqualified on the merits even where it passes:** it is not the change under
discussion. It moves 1R itself, the arming price, and 9 of 13 positions' outcomes — a new risk
profile, not a trail fix — and it would require the canon R-boundary that a trail-only change does not.

## 🔴 VERDICT: **NOTHING QUALIFIES.** Nothing was applied.

---

## What the STRUCTURAL argument alone would justify

**1. `TRAIL_MULT_ATR = SL_BUFFER_ATR` is an identity, not a statistic.** The trail returns the entire
initial risk by construction — confirmed on all four trailed exits at 1.0667 / 0.9762 / 0.9949 /
0.9866. **A trail that gives back 1R is a delayed breakeven stop.** No book is needed to know this is
wrong, and no book can make it right.

**2. The grid adds one structural corroboration.** At b=2.5, **trail=1.25R is bit-identical to
trail=1.0R** — same sum, same median, same zero positions changed, on every cohort and both sides.
**At or above 1R the trail never fires before the breakeven stop or an exit signal.** It only becomes
a mechanism below 1R. The current value is the largest setting at which the trail still exists at all.

**3. The book's direction — 7 armed positions, analytic, clearly labelled.** Because the replay is
blind on vpos 21 and on the three unpathed armed positions, I computed the trail trigger directly from
`water_mark` and the close, which needs no path:

| | ΔR_ref (t 1.0→0.75) | changed |
|---|---|---|
| LONG | **+0.314** | 2 of 2 |
| SHORT | **+0.966** | 4 of 5 |
| **all armed** | **+1.280 R_ref (+$234.98)** | **6 of 7** |

**Six of seven improve; none is harmed.** 🔶 **Stated bias:** this uses the *final* water mark, giving
the *latest* possible trigger, while the engine trails a *running* one — so a real earlier retrace
could fire sooner. It is an estimate outside the validated replay, and it is why it does not overturn
the conjuncts.

### So: **the current value is provably wrong, and the replacement is not determined by this book.**

The structural argument justifies **decoupling the two constants so the trail is strictly below 1R**.
It does not pick a number. **0.75R is the only value with any support and no counter-evidence** —
positive on both cohorts, positive on both sides analytically, six of seven armed positions improved
— but it rests on 7 observations of which 3 are estimates and one side has 2.

---

## 🔴 WHAT WOULD MAKE THIS DECIDABLE — and it is already half-done

The blocker is not the book's size. It is the **sampler's resolution**, and that has already been
fixed since these positions were recorded:

| | |
|---|---|
| effective cadence, vpos 15–24 | **~305 s** — lost vpos 21's entire trail event |
| vpos 25 / 26 / 27 (most recent) | 13 s / 61 s / 50 s |
| current config | `EXCURSION_SAMPLE_SEC = 10` dense for the first hour, then 50 s |

**The instrument was repaired before this question was asked; it just had not been repaired when the
trailed exits in this book happened.** So the honest recommendation is not to fix anything — it is to
**wait and re-run**.

At the observed rate — **21 closed positions in 49 days = 3.0/week, of which 0.57/week are trailed
exits** — doubling the trailed cohort from 4 to 8 takes **about 7 weeks**, and every one of those
would be recorded at 10–50 s instead of 305 s.

**Three options, and the choice is yours:**

1. **Apply the structural argument now**, decoupling to trail = 0.75R on the strength of the identity
   plus a 6-of-7 directional estimate. Cheap and reversible: it is one constant, it does not move 1R,
   and **no canon R-boundary is needed**.
2. **Wait ~7 weeks** for 8 trailed exits at proper resolution and re-run this exact grid.
3. **Split the difference** — apply now *and* re-run at n=8, since the change is R-boundary-free and
   the before/after cohorts stay directly comparable. This is the only one of the three that costs
   nothing to reverse and still buys the measurement.

I did not choose. **§4 was written to be refusable, and this is the case it was written for.**

---

## THE LESSON, NAMED

**Titan's discipline earned its keep twice here, in two different ways.**

The **unit** check behaved exactly as the canon predicted: a naive reading of the grid finds a
monotone axis running to the corner and would ship b=2.0/t=0.75. Denominated in a fixed R_ref and cut
on the trail's own cohort, that same axis goes **flat and non-monotone (2.91/2.94/2.92)** and the
decomposition shows 82% of its gain is a narrower stop on a book of stop-outs. **The grid was ranking
the losers, not the mechanism.**

The **instrument** check found something the canon did not anticipate. Titan's failure was a replay
that saw *too much* — wicks the poller never saw, and a life that outlived the real close. **SOL's is
the mirror: a replay that sees too little.** The sampler stopped 226 seconds before vpos 21 closed,
and the trail fires in the last few minutes of a position by definition — so the one measurement that
would have decided the LONG side was never recorded. A "no change" result and "no data" result look
identical in a sum; only opening the path tells them apart.

**And the most useful thing this produced is not a number.** It is the finding that at ≥1R the trail
is *inert* — 1.25R and 1.0R are bit-identical — which means the current setting is not "a trail that
is slightly too loose". **It is the exact point at which the mechanism stops existing.**
