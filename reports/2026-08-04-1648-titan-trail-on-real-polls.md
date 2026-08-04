# THE TRAIL ON WHAT THE ENGINE SAW — NOTHING APPLIED, AND ARMING NEVER NEEDED INFERRING

**2026-08-04 16:48 UTC · Titan LIVE, real money, flat · HEAD `14319a5`, UNCHANGED — no code shipped**

Your branch fired: **the lower bound is negative on shorts → apply nothing, and record the axis as
undetermined-by-construction, not pending-more-data.** `TRAIL_MULT_ATR` stays **2.5**.

⚠️ **`SL_ATR_MULT` untouched (2.5 by runtime import) ⇒ 1R does not move, no §0 boundary.**
`git status` clean, 0 open positions.

Canon: **§2.52** added in the same commit. Snapshot: `reports/2026-08-04-1648-open-items.md`.

---

## 🔴 0. THE ANSWER TO THE WHOLE QUESTION WAS IN THE DATABASE ALL ALONG

`virtual_positions.pending_dca_limits` carries `mgmt_state.breakeven_applied` — **on all 59 closed
positions.** The engine recorded whether the trail ever armed. **No replay, no proxy, and none of my
wick reasoning was ever necessary.** Scored against that record:

| method | n | agrees | **FALSE-armed** | missed | accuracy |
|---|---|---|---|---|---|
| a) 5m candle **wicks** | 59 | 44 | **15** | 0 | 75 % |
| c) 5m candle **closes** — my 16:37 "ROBUST" proxy | 59 | 45 | **14** | 0 | **76 %** |
| b) **excursion samples** | 32 | 32 | **0** | 0 | 🔴 **100 %** |

**True arming rate, from the engine: LONG 5 of 26 = 19.2 % · SHORT 13 of 33 = 39.4 %** — §2.2's
independently measured 22 % for LONGs, confirmed.

**Two corrections to my 16:37 report, made here rather than left standing:**

1. 🔴 **My "ROBUST" proxy is 76 % accurate — barely better than the 75 % wick method it was invented
   to correct**, and it still false-arms 14 positions. I built a proxy for a fact that was already
   recorded. It should not be used again.
2. 🔴 **The excursion samples do NOT under-arm.** Your brief and my §2.51 both framed them as a lower
   bound on arming. **They reproduce the engine 32 of 32, exactly.** They are coarse only on the
   *path after* arming — not on arming itself.

## 1. §2a COVERAGE — STATED BEFORE ANY RESULT, AS YOU ASKED

- **32 of 59** positions have a usable sample path, **starting 2026-06-30**. §0-clean: **18**.
  Mechanical exits: **9**.
- **Sample cadence: ~62 s** for the first 15 min, **~307 s** after (`EXCURSION_SAMPLE_SEC = 60`,
  dense window 900 s, then 5×). **Live poller: 5 s.** So samples are **12×–61× coarser**.
- 🔴 **Only 5 of the 18 truly-armed positions have a sample path at all.** That, not the arming rate,
  is the binding number for this question.
- **§2c — the samples are a genuine time series**: `price` per row with `elapsed_s`/`ts`. `mae_pct`
  and `mfe_pct` *are* running extremes and do inherit §0's defect — **so `price` is used and they are
  not.** The approach does not fail on that count.

## 2. §2b VALIDATION — reproduce the book before reading any counterfactual

Current contract, mechanical exits with samples (n=9):

| basis | reproduced within ±0.15R | mean \|Δ\| |
|---|---|---|
| candle **closes** | **9 of 9** | 0.052R |
| candle wicks | 7 of 9 | 0.164R |
| excursion **samples** | 6 of 9 | 0.150R |

*(the candle replay's earlier figure was 18 of 24 on the larger mechanical cohort)*

**The sample path reproduces *arming* perfectly and *outcomes* least well** — its 62 s/307 s cadence
misses stop and trail touches that happen between polls. **Both facts are true at once, and they are
what makes this axis undecidable rather than merely unmeasured.**

## 3. §1 THE BRACKET — 0.75R vs 1.0R at unchanged SL

| basis | mech-9 | clean-18 | LONG (mech/clean) | **SHORT (mech/clean)** |
|---|---|---|---|---|
| a) wicks — over-arms, known upper bound | +0.72 | +1.62 | +0.34 / +0.59 | +0.39 / +1.03 |
| c) closes | +0.58 | +1.16 | +0.34 / +0.51 | +0.24 / +0.65 |
| **b) samples — exact on arming** | **+0.10** | **+0.10** | +0.13 / +0.13 | 🔴 **−0.02 / −0.02** |

**All three agree in direction on longs and on the pooled book.** On **shorts** the accurate
instrument is **negative** — −0.02R, indistinguishable from zero, on 5 mechanical / 10 clean shorts
**of which only 1–2 ever armed**.

**And the bracket is one-sided by construction: 1.25R is 100 % truncated under the sample method**
(18 of 18). The sample path ends at the real close, so a *wider* trail — which would extend the trade
— cannot be evaluated at all. Narrowing can only shorten a trade, which is why 0.75R is measurable
and 1.25R is not.

**On the truly-armed cohort** (the engine's own flag, no proxy): wicks **+2.55R** (n=13) · closes
**+2.71R** (n=13) · **samples +0.10R (n=3)**.

> **The instrument that is right has almost no sample. The instruments that have sample are wrong in
> the direction of the answer.** That is the verdict, and it is a statement about the measuring
> apparatus, not about the trail.

**Pre-registered figures, sample method:** of the last 25 entries **2 change outcome, net +0.10R**
(vpos 79 +0.13, vpos 81 −0.02, both engine-armed). **Live era: Δ = +0.00R — only 1 of the 7 ever
armed.**

## 4. §3 RE-DATING THE PRIOR RESULTS — this is not housekeeping

**§2.2's STRUCTURE claim survives on every basis.** Narrowing helps longs, monotone under wicks,
closes and samples alike. **Its magnitude does not: the wick basis overstates the long margin ~2.6×**
(+0.34 vs +0.13 on the identical 9-position cohort).

🔴 **§2.2's partial-vs-trail SUBSTITUTION SHAPE does not reproduce.** On 15 clean longs the partial's
contribution is **U-shaped, not declining**:

| trail | wicks | closes |
|---|---|---|
| 1.25R | +1.03 | +0.82 |
| 1.0R | **+0.67** | **+0.48** |
| 0.75R | +0.98 | +0.90 |

§2.2 measured a monotone decline to negative on **5** longs, and its negative point was at **0.5R**,
which is excluded here and untested. **So the substitution result is not refuted at 0.5R — but it is
NOT supported between 0.75R and 1.25R**, and it is cited elsewhere as though it were general.

🔴 **§2.50's SL-axis TURN does not survive the change of basis.** On closes the axis is **monotone**
(trail 1.0R: +0.84 → +2.83 → +4.92; trail 0.75R: +3.55 → +5.20 → +6.62), where on wicks it turned at
2.25 — and that turn is what rejected all six cells in §2.50. **The non-monotonicity was an artifact
of the biased instrument.** This **re-opens the SL question**, on a 76 %-accurate instrument, so it
must be re-run on the accurate one before anyone acts. **Out of scope here and not acted on.**

## 5. 🔴 THE REVIEW POINT, AND WHAT SHORTENS IT OTHER THAN TIME

On the engine's own record: **18 truly-armed positions of 59 over 72 days**. At today's **0.47
entries/day** that is **0.14 armed/day → 20 armed per side ≈ 279 days.** (My 335-day proxy estimate
was pessimistic; the real figure is still nine months.)

**Waiting is not the fix, and the fix is cheap and already half-built.** Arming is *already* recorded
exactly. What is missing is the **path after arming at poll resolution** — and the only reason the
accurate instrument is coarse is `EXCURSION_SAMPLE_SEC = 60` with a 900 s dense window, while the
poller runs at **5 s**.

**Proposal, not applied:** raise the excursion sampler toward the poller's cadence, or extend the
dense window to cover the armed phase. It is an observational logger that gates nothing, and it would
make **every future position ground truth for this axis** instead of one in six. **I am not applying
it in this pass** — it is outside the stated scope and has no pre-registration, and this book's rule
is that those get written first, not afterwards.

## 6. SCOPE

Untouched: `SL_ATR_MULT`, `TRAIL_MULT_ATR`, the EMA envelope gate, the HTF cascade, the FLAT floor,
Variant-B, the score bars, the risk gates, both advisor prompts, the exit advisor's inputs, and the
excursion sampler's configuration. **There is no diff** — no snapshot, no `py_compile`, no restart,
because nothing is applied. All measurement read-only against `trades.db` and cached candles; **no
table was written.**
