# sol-exit-contract-simulated-current-trail-provably-wrong-replacement-undetermined

_2026-08-01 15:24 UTC_

---

# MERCURY-SOL — EXIT CONTRACT SIMULATED ON SOL'S OWN DATA, 2026-08-01

**READ-ONLY. Nothing applied, nothing proposed, nothing changed.** Titan was not touched and
none of its parameters were imported; every constant below is read from
`/mnt/volume_nyc1_1780480650620/mercury-sol/config.py`.

Companion to the 14:46 diagnosis
(`2026-08-01-1446-mercury-sol-diagnosis-barely-trades-and-the-trail-gives-back.md`). Its §0.2
(measurement defects) and §4b (exit distribution) are the inputs to this one. Book state
re-verified before simulating: **18 positions, id 7–24, none open, last close 2026-07-30
12:03:30 UTC — unchanged since 14:46.**

The established fact this rests on: `TRAIL_MULT_ATR = 2.5` is arithmetically identical to
`SL_BUFFER_ATR = 2.5`, so **the trail's callback distance is exactly 1.00R**, and its first
trigger after arming at +1R sits back at the entry price. That is arithmetic and it is not in
question. Everything below is about what to do with it — and most of it does not resolve.

---

# §1 — THE SAMPLE, BEFORE ANY NUMBER

## 1.1 What exists

| | positions | ids |
|---|---|---|
| full price PATH (`position_excursion_samples`) | **10** | 15–24 |
| MFE/MAE scalars only (`water_mark` / `max_adverse_price`) | **8** | 7–14 |

## 1.2 But the exit contract only touches positions that ARMED

Trail width, partial realisation, no-trail and arm-point are all downstream of the +1R
breakeven arm. A position that never reached +1R never engages any of them. I verified this by
exhaustive sweep rather than by assertion — every combination of `trail_mult` ∈ {0.5, 0.75, 1.0,
1.5, 2.5} × `partial` ∈ {0, ⅓, ½} × `use_trail` ∈ {T,F} × `arm_R` ∈ {1.0, 1.25, 1.5} against the
7 unarmed path positions:

```
R moved under ANY variant: NONE — all 7 invariant, as expected
```

**So 12 of the 18 positions are fixed by construction.** The entire question lives in the 6 that
armed. And here is the problem:

| armed position | realised R | path? |
|---|---|---|
| vpos 7 | **+2.089** | ❌ none |
| vpos 11 | **+1.133** | ❌ none |
| vpos 13 | **+1.337** | ❌ none |
| vpos 15 | +0.140 | ✅ 247 samples |
| vpos 17 | +0.004 | ✅ 401 samples |
| vpos 21 | +0.285 | ✅ 234 samples |

🔴 **Every trail simulation in this document rests on three trades — vpos 15, 17 and 21, worth
+0.429R between them. The three positions that carry +4.559R (91% of the book's entire positive
R) have no path data at all.** They are exactly the runners, and a narrower trail's only real
risk is cutting a runner short. That risk is untestable on this book. I say this before quoting
a single result because it survives all of them.

## 1.3 The grid, and why it nearly disqualified the simulator

`_record_excursion_sample` throttles to `EXCURSION_SAMPLE_SEC` (60s) for the first
`EXCURSION_DENSE_UNTIL_SEC` (900s), then **5× that**. Measured across all 2,603 gaps:

```
median 305s | mean 294s | p90 311s | max 749s      live poller cadence = 10s
-> the simulation grid is ~31x coarser than the mechanism it is simulating
```

A trail is a pure function of the *running peak*. A 5-minute grid does not see the peak:

| vpos | stored water_mark | best sampled price | peak missed | in R |
|---|---|---|---|---|
| 15 | 76.260 | 76.360 | 0.100 | 0.051R |
| **21** | 77.350 | 77.080 | **0.270** | **0.298R** |
| 17 | 74.140 | 74.150 | 0.010 | 0.007R |
| 24 | 72.260 | 72.370 | 0.110 | 0.068R |

---

# §2 — SIMULATION

## 2a — BASELINE: can it reproduce the actual book?

The simulator mirrors `virtual_trader._process_position` in the live order — watermark → BE arm
→ stop → trail — with SOL's own constants (`SL_BUFFER_ATR` 2.5, arm distance =
`SL_BUFFER_ATR × atr` per `trail_arm.activation_distance`, BE target = entry ± 0.20%,
`trail_pct = round(TRAIL_MULT_ATR × atr / entry × 100, 3)`, taker fee 0.055%/side, no timeout
since `MAX_POSITION_DURATION_MINS = 0`). The recorded 15m armed exit fires exogenously at its
recorded time.

**First attempt — watermark taken from the sampled path:**

```
reasons reproduced 8/10 | total R actual -5.141  sim -5.141  err +0.000R
  vpos 15  actual trail  -> sim CENSORED   NO
  vpos 21  actual trail  -> sim CENSORED   NO
```

Eight of ten exact — and **it failed on both trail exits, which are the only two exits that
matter here.** Cause is §1.3: the grid understates the peak, the trail level sits too low, the
trigger never fires. On vpos 21 the miss is 0.298R against a trail 1.00R wide.

**Second attempt — peak-corrected** (at the sampled-peak instant, adopt the stored
`water_mark`, which the live poller recorded at 10s resolution):

```
reasons reproduced 10/10 | total R actual -5.141  sim -5.141  err +0.000R
```

**Match: 10/10 exit reasons, R error 0.000.** The simulator is qualified — but only with a
correction that anchors the true peak at the *observed* peak time. That is an approximation, and
it is the reason every number below carries a wider error bar than its decimals suggest. A trail
narrower than ~0.3R is finer than the grid's own peak error and **cannot be simulated honestly
on this data at all.**

## 2b — NARROWER TRAIL

Units first, because they matter: **trail width in R = `trail_mult` / 2.5.** The current
2.5×ATR is 1.00R wide; 1.5×ATR is 0.60R; 1.0×ATR is 0.40R; 0.75×ATR is 0.30R; 0.5×ATR is 0.20R.

**(i) Simulated — the 3 armed positions with a path:**

| trail | avg % | vpos 15 | vpos 17 | vpos 21 | sum R | vs 2.5 |
|---|---|---|---|---|---|---|
| **2.5×ATR** | 1.88% | +0.140 trail | +0.004 be | +0.285 trail | **+0.429** | — (current) |
| 1.5×ATR | 1.13% | +0.474 trail | +0.445 trail | +0.518 trail | +1.436 | **+1.007** |
| 1.0×ATR | 0.75% | +0.746 trail | +0.718 trail | +0.529 trail | +1.993 | +1.563 |
| 0.75×ATR | 0.56% | +0.797 trail | +0.818 trail | +0.529 trail | +2.144 | +1.715 |
| 0.5×ATR | 0.38% | +0.879 trail | +0.912 trail | +0.707 trail | +2.497 | +2.068 |

- **winners cut short: zero** — but only because none of these three is a runner. Their peaks
  were 1.18R, 1.18R and 1.44R. Monotonic improvement is the *expected* result when the peak is
  never exceeded after the retracement; it is not evidence that a narrower trail is safe.
- **losers improved: zero, structurally** — the trail cannot touch a position that never armed.
- The 0.75× and 0.5× rows are below the grid's own peak-resolution error and should be read as
  "narrower keeps helping on these three", not as numbers.

**(ii) Bounded — the 3 armed runners with no path. UPPER BOUNDS. Never pooled with (i).**

The bound is peak-minus-width-minus-fees: the trail is assumed to survive every intermediate
retracement and fire exactly once, at the very top. It cannot be beaten; a real trail exits at
the *first* retracement of its own width, usually far earlier.

| vpos | actual exit | peak (R) | actual R | ×2.5 | ×1.5 | ×1.0 | ×0.75 | ×0.5 |
|---|---|---|---|---|---|---|---|---|
| 7 | exit_signal | 2.998 | **+2.089** | 1.952 | 2.352 | 2.552 | 2.652 | 2.752 |
| 11 | exit_signal | 1.712 | **+1.133** | 0.671 | 1.071 | 1.271 | 1.371 | 1.471 |
| 13 | trail | 2.351 | **+1.337** | 1.306 | 1.706 | 1.906 | 2.006 | 2.106 |
| **sum** | | | **+4.559** | 3.929 | 5.129 | 5.729 | 6.029 | 6.329 |

🔴 **On both signal-exit runners the 15m armed exit realised more than the current trail's
theoretical ceiling.** vpos 7 took +2.089R against a ceiling of +1.952R; vpos 11 took +1.133R
against a ceiling of +0.671R. On vpos 13 the trail fired essentially *at* its ceiling (+1.337
actual vs +1.306 bound, the +0.03 overshoot being grid slippage past the trigger).

## 2c — PARTIAL REALISATION AT +1R, remainder on the unchanged 2.5×ATR trail

| partial | vpos 15 | vpos 17 | vpos 21 | sum R | vs base |
|---|---|---|---|---|---|
| none | +0.140 | +0.004 | +0.285 | +0.429 | — |
| **⅓** | +0.426 | +0.333 | +0.522 | +1.281 | **+0.852** |
| **½** | +0.569 | +0.498 | +0.640 | +1.707 | **+1.277** |

This is the one variant whose *structure* guarantees it cannot cut a runner short: the remainder
runs on the identical rule, so a runner's tail is shaved, never truncated. Against the bounded
runners in 2b(ii) a ½ partial would have cost, at most, half of each one's excess over +1R — it
cannot invert their sign.

## 2d — NO TRAIL AT ALL

**The simulator cannot answer this, and the reason is structural, not a limitation I can code
around: the recorded price path ends at the actual exit.** Any variant that holds *longer* than
what happened has no data after that point.

```
                   variant  |  vpos15          vpos17          vpos21   | sum R
current (trail 2.5, BE on)  |  +0.140 trail    +0.004 be       +0.285 trail | +0.429
 d1 no trail, BE lock kept  |  +0.140 CENSORED +0.004 be       +0.285 CENSORED | +0.429
   d2 no trail, no BE lock  |  +0.140 CENSORED +0.004 CENSORED +0.285 CENSORED | +0.429
```

Every cell is censored at the last observed price, which *is* the actual close price. The
apparent "no change" is an artefact of running out of data, not a result.

**But the bot has been running this exact experiment for the whole book.** `post_exit_observatory`
documents its Shadow Exit as *"an alternative **no-trail** exit, ARMED AT ENTRY (Variant Y)"* —
it holds from entry and exits only on an opposite 15m BOS/CHOCH/Liquidity-Grab, a 1H trend
reversal, the **original** ATR stop, or a 72h cap. All 18 positions, status `completed`:

| vpos | real exit | real R | shadow reason | shadow R | Δ |
|---|---|---|---|---|---|
| 7 | exit_signal | +2.089 | 15m_signal | +0.012 | **−2.077** |
| 8 | exit_signal | −0.739 | 15m_signal | −0.220 | +0.519 |
| 9 | exit_signal | −0.264 | 15m_signal | +0.258 | +0.522 |
| 10 | sl | −1.066 | 15m_signal | −0.449 | +0.617 |
| 11 | exit_signal | +1.133 | 15m_signal | +0.095 | **−1.038** |
| 12 | sl | −1.049 | 15m_signal | −0.148 | +0.900 |
| 13 | trail | +1.337 | 1h_reversal | −0.048 | **−1.384** |
| 14 | sl | −1.032 | 15m_signal | −0.953 | +0.080 |
| 15 | trail | +0.140 | 15m_signal | +0.077 | −0.063 |
| 16 | sl | −1.146 | 15m_signal | −0.289 | +0.857 |
| 17 | sl | +0.004 | 15m_signal | −0.260 | −0.264 |
| 18 | sl | −1.074 | 15m_signal | −0.266 | +0.807 |
| 19 | exit_signal | +0.463 | 15m_signal | −0.061 | −0.524 |
| 20 | sl | −1.124 | 15m_signal | −0.391 | +0.733 |
| 21 | trail | +0.285 | 15m_signal | +0.100 | −0.185 |
| 22 | sl | −1.064 | 15m_signal | −0.120 | +0.944 |
| 23 | exit_signal | −0.577 | 1h_reversal | +0.008 | +0.585 |
| 24 | sl | −1.050 | 15m_signal | +0.043 | **+1.093** |
| **TOTAL** | | **−4.733** | | **−2.612** | **+2.121** |

Better on 11 of 18. But the aggregate hides the only thing that matters:

```
  the 6 that ARMED       real +4.988R   shadow -0.024R   delta  -5.012R
  the 12 that never armed real -9.721R   shadow -2.588R   delta  +7.133R
```

🔴 **The no-trail shadow annihilates the winners (−5.01R) and rescues the losers (+7.13R).** The
trail and BE lock are doing real, large work on armed positions — removing them is not a marginal
change, it costs five R on six trades. The +2.12R headline is the residue of two much larger
opposing effects and should never be quoted on its own.

**⚠️ Semantics, stated precisely so this is not over-read:** the shadow is **not** "stop + the
15m armed exit". The live armed exit requires a 1h `Exit Signal` to arm the side *first*; the
shadow fires on the first opposite 15m structure signal with no arming requirement. It is a
strictly more trigger-happy rule, and that is why it cuts both losers and winners early.

**Post-exit drift adds a third fact.** After each of the three trail exits, price continued in
the trade's favour: vpos 15 **+0.79R** further, vpos 13 **+1.43R**, vpos 21 **+2.14R**. The trail
was not exiting late into a reversal — it was being shaken out of moves that then resumed. No
trail width captures that; it is an argument about the exit *family*, not its parameter.

## 2e — BREAKEVEN ARM POINT

**Also unanswerable, same censoring.** Raising the arm disarms positions, and a disarmed position
holds past the point where the data ends.

| arm | vpos 15 | vpos 17 | vpos 21 |
|---|---|---|---|
| 1.00R (current) | ARM → trail | ARM → be | ARM → trail |
| 1.25R | **no-arm, CENSORED** | **no-arm, CENSORED** | ARM |
| 1.50R | **no-arm, CENSORED** | **no-arm, CENSORED** | **no-arm, CENSORED** |

Peaks reached: vpos 15 **1.181R**, vpos 17 **1.180R**, vpos 21 **1.437R**. Arming at 1.25R
disarms two of the three; arming at 1.50R disarms all three. What is *knowable* without
simulation: two of the six armed positions in the entire book cleared +1R by less than 20%, so a
1.25R arm would have removed a third of the armed population. What happens to them afterwards is
not in the data.

---

# §3 — INTERACTIONS

Cells are the summed R over vpos 15/17/21 under **combined** settings — not sums of separate
variants.

| partial ＼ trail | ×2.5 | ×1.5 | ×1.0 | ×0.75 | ×0.5 |
|---|---|---|---|---|---|
| **none** | +0.429 | +1.436 | +1.993 | +2.144 | +2.497 |
| **⅓** | +1.281 | +1.952 | +2.323 | +2.424 | +2.660 |
| **½** | +1.707 | +2.210 | +2.489 | +2.564 | +2.741 |

**Marginal value of each lever given the other — the question asked:**

```
  narrowing 2.5 -> 1.0, no partial      +1.563R
  narrowing 2.5 -> 1.0, with 1/2 partial  +0.782R   <- 50% of the standalone gain
  adding 1/2 partial at trail 2.5       +1.277R
  adding 1/2 partial at trail 1.0       +0.496R   <- 39% of the standalone gain
  both together                          +2.059R
  naive SUM of the two separately        +2.841R   <- OVERSTATES by +0.782R
```

**Answer: yes, strongly substitutive in both directions.** A ½ partial removes half the value of
narrowing the trail; a 1.0×ATR trail removes 61% of the value of the partial. Adding the two
variants together overstates the combined effect by **+0.78R, which is 38% of the true joint
gain**. They are two ways of attacking the same defect — giveback from the peak — and the book
cannot rank them, because on these three trades they land within ~0.4R of each other from either
direction.

**The composite that looked obvious does not work.** The 2d split suggests "use the structure
exit while the position is unarmed, switch to the trail once it reaches +1R" — capturing the
+7.13R on losers without the −5.01R on winners. Tested against arm times:

| vpos | armed at | shadow structure-exit at | order |
|---|---|---|---|
| 15 | 10.20h | **0.74h** | shadow fires FIRST |
| 17 | 18.42h | **2.00h** | shadow fires FIRST |
| 21 | 17.43h | **0.58h** | shadow fires FIRST |

On all three the structure exit fires **10–30× earlier than the arm**. The composite therefore
collapses into the shadow rule for exactly the positions it was meant to protect, and would have
destroyed them. (For the three runners without paths the arm time is unknown, so this cannot be
extended to them — but their shadow exits fired at 4.83h, 1.33h and 0.00h, and vpos 13's fired
immediately at entry.) **Negative result, and a clean one.**

---

# §4 — THE SMART-EXIT SAMPLER AS AN INDEPENDENT CHECK

`smart_exit_dryrun_samples`, running since 07-01: arm at MFE ≥ 1.2%, would-exit on ≥ 0.8%
giveback from the peak. I scored it at its own recorded would-exit price — the first sample where
`would_exit=1` — against what the live rule actually realised.

| vpos | n | armed | would-exit | 1st would-exit px | that R | real R | Δ |
|---|---|---|---|---|---|---|---|
| 15 | 21 | 17 | 9 | 77.260 | +0.623 | +0.140 | **+0.482** |
| 16 | 6 | 0 | 0 | — | — | −1.146 | — |
| 17 | 34 | 19 | 12 | 75.110 | +0.478 | +0.004 | **+0.474** |
| 18 | 41 | 26 | 25 | 77.490 | −0.039 | −1.074 | **+1.035** |
| 19 | 14 | 6 | 1 | 76.350 | +0.409 | +0.463 | −0.054 |
| 20 | 4 | 0 | 0 | — | — | −1.124 | — |
| 21 | 19 | 1 | 1 | 76.370 | +0.262 | +0.285 | −0.022 |
| 22 | 58 | 0 | 0 | — | — | −1.064 | — |
| 23 | 5 | 0 | 0 | — | — | −0.577 | — |
| 24 | 16 | 0 | 0 | — | — | −1.050 | — |
| **TOTAL** | | | | | **−3.227** | **−5.141** | **+1.915** |

It fired on 5 of the 10 positions it covers. Its single largest gain is **vpos 18, a loser** —
−0.039R instead of −1.074R — which it reaches because its arm bar (MFE ≥ 1.2%) is far below +1R
(vpos 18's 1R was 2.18% of entry), so it engages on positions the live trail never touches.

**As a check on the simulation, on the 3 positions both methods cover:**

```
  live rule (trail 2.5xATR)                    +0.429R
  my simulator, trail 1.5xATR                  +1.436R
  smart-exit sampler, its own recorded prices  +1.363R
  -> two independent methods, 0.073R apart
```

A month of independently-recorded counterfactual lands within **0.073R** of the peak-corrected
simulator on the same three trades. That is the strongest validation available here, and it is
what makes me willing to quote §2b(i) at all. It does not, however, extend the sample — the
sampler is blind to vpos 7, 11 and 13 for the same reason the simulator is.

---

# §5 — HONEST VERDICT ON n

**Enough to say the current value is wrong. Not enough to choose the replacement.**

## What is settled

**`TRAIL_MULT_ATR = 2.5` is provably wrong, and the proof is arithmetic, not statistical.** It
is identical to `SL_BUFFER_ATR`, so the callback is exactly 1.00R and the trail's first trigger
after arming at +1R lands on the entry price. Every armed position gave back ~1R
(1.02/1.04/1.16/1.18R measured at 14:46), and every method tried here — a peak-corrected path
simulation, an independent month-long sampler, and peak-minus-width bounds on the three
runners — moves in the same direction from that value. No result in this document supports
keeping 2.5.

## What is not settled, and why

1. **n = 3.** Trail width only touches armed positions; there are 6; only 3 have paths. Those 3
   realised +0.429R between them.
2. **Every runner is invisible.** vpos 7, 11 and 13 hold 91% of the book's positive R and have no
   path. The *only* risk a narrower trail carries — truncating a runner — cannot be tested on a
   single runner in this book. §2b(i)'s clean monotonic improvement is what you get when you
   simulate a trail on three trades that never ran; it is not evidence of safety.
3. **The two candidate structures are substitutive, not additive** (§3). Partial and narrower
   trail deliver 50% / 39% of their standalone value once the other is present, and their naive
   sum overstates by 38%. On this book they cannot be ranked against each other — they land
   within ~0.4R either way, on three trades.
4. **Two of the five questions are unanswerable, not merely uncertain.** No-trail (2d) and a
   later arm (2e) both require holding past the actual exit, and the price record stops there.
   The censoring is a property of the evidence, not of the method.
5. **The largest effect found is not about the trail.** The shadow's +7.13R on the 12 unarmed
   positions dwarfs everything measured on the armed ones — but it comes bundled with −5.01R of
   destroyed winners, and the obvious way to separate them (structure exit until armed, then
   trail) is disproved in §3: the structure exit fires 10–30× earlier than the arm.

## The one thing that is directionally clear, stated as an observation and nothing more

The 15m armed exit is the only mechanism in this book that has produced a large gain. It beat the
current trail's *theoretical ceiling* on both runners it handled (+2.089R vs 1.952R; +1.133R vs
0.671R), and the one runner the trail did take, it took at its ceiling (+1.337R vs 1.306R). At a
1.00R callback, the trail's ceiling is peak−1R — which on this book has been below what the
signal achieved. That is three observations, all from bounds rather than simulation, and it is
not enough to conclude the trail subtracts value. It is enough to say the question is open and
that "narrow the trail" is not obviously the right axis.

## What would close it

Not a bigger sweep of the same 18 trades — the answer is not in them. Two things are missing, and
both are measurement rather than analysis:

- **Armed positions with path data.** 6 armed in 55 days ≈ 1 per 9 days; 3 usable. At that rate a
  sample large enough to rank two substitutive structures is many months away — which is itself
  a finding, given the entry rate documented at 14:46 (0.33/day).
- **A finer excursion grid.** At a 305s median cadence the recorded peak misses the true peak by
  up to 0.298R. Any trail narrower than ~0.3R is finer than the instrument's own error, so the
  0.75× and 0.5× rows in §2b(i) are not measurements. The live poller already runs at 10s; the
  sampler's throttle is what discards the resolution.

**Verdict: the current 2.5 is provably wrong and the replacement is not yet determined.** I am
not going to invent a number to fill that gap.

---

*Method: peak-corrected replay of `virtual_trader._process_position` against
`position_excursion_samples`, validated at 10/10 exit reasons and 0.000R error on the 10 path
positions; upper bounds from `water_mark` for the 8 scalar-only positions; independent
counterfactuals read from `post_exit_observatory` (shadow exit, all 18) and
`smart_exit_dryrun_samples` (218 samples, vpos 15–24). Constants from SOL's own `config.py` and
`trail_arm.py`. All queries read-only (`file:...?mode=ro`). Simulator kept at
`scratchpad/solsim2.py`.*
