# Mercury-SOL — the stop is NOT too tight. Widening shrinks the payoff faster than it saves the stop-outs, and the noise hypothesis is refuted by its own test.

**2026-08-17 13:50 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · READ-ONLY THROUGHOUT — no `.py` written, no restart, no order, no DB write. Nothing proposed before §4, and nothing applied at all.**

Titan (`/root/titan-bot`): **not touched, not read for state, no numbers imported.** HEAD `897850b`, working tree clean.

Premise: [19:30 §1c and §2c](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-14-1930-sol-the-payoff-ratio-is-the-defect-and-the-moves-are-not-there.md) · range basis: [19:00 §1](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-14-1900-sol-where-in-the-range-it-enters-one-behaviour-per-side-and-it-does-not-decide-the-outcome.md)

---

## ⚡ THE SHORT VERSION

1. **🔴 THE NOISE HYPOTHESIS IS DEAD, AND ITS OWN TEST KILLED IT.** The brief's decisive question was: after the stop fired, did price come back through the entry? **If 10 of 14 came back, the geometry was wrong. One of 14 came back within 1h. Two within 4h. Three within 12h.** Meanwhile **11 of 14 went a further 0.25R+ AGAINST within four hours of the exit**, and the 24-hour adverse excursions run to −1.4R … −3.6R. The stop was not taken out before the move resolved. The move resolved, against.
2. **🔴 "14 OF 29 DIED ON THE STOP" IS FOUR MECHANISMS WEARING ONE LABEL.** `close_reason='sl'` covers: **10** deaths at the full 2.5×ATR stop (−10.845R), **3** at a stop the post-entry recheck had already **HALVED** (`recheck_status='tightened'`, −2.004R), and **1** at the **breakeven lock** (vpos 17, a +0.004R winner). The parameter under examination killed ten, not fourteen.
3. **🔴 WIDENING SAVES THE DEATHS AND LOSES MORE MONEY.** Within the booked life, a stop at 3.0×ATR would have missed **nine of the ten** deep MAEs (only vpos 10 needed >3.58×). Let the tape run on and **nine of the ten are stopped anyway, just later** — and the ten together are **worse**: −9.795R at b=3.0 vs −8.731R at b=2.5.
4. **🔴 THE UPPER BOUND SETTLES IT: NO STOP AT ALL IS WORSE.** Hold those same ten with the stop removed entirely and mark out 12h past the booked exit: **ΣR −11.594 against −8.731 at today's stop.** The stop is not costing money on this cohort. It is saving 2.86R of it.
5. **THE ASYMMETRY IS THE WHOLE MECHANISM.** At equal risk a wider stop means a proportionally smaller position, so **winners shrink almost exactly by 2.5/b** (mean winner 0.904 → 0.745 at b=3.0, pure-size prediction 0.753). **Losers do not**, because the losing move is big enough to reach the wider stop too (mean loser 0.717 → 0.710, pure-size prediction 0.597). **The stop moves; the loss does not follow it down.**
6. **🔴 SO WIDENING MAKES THE PAYOFF PROBLEM WORSE, MONOTONICALLY.** payoff 1.26 (b=2.5) → 1.05 (3.0) → 0.87 (3.5) → 0.85 (4.0). The gap the mean winner must close to break even **widens** from +0.269R to +0.728R. Positions that ever touched 1.5× their own R fall from **6 of 29 to 2 of 29**. This is the 19:30 conclusion arriving from the second direction the brief named.
7. **The curve is NON-MONOTONE and its maximum moves with the contract.** Under today's contract the best cell is **b=1.75**; under the 19:30 contract it is **2.25**; with the stop naked it is **4.0**. Three contracts, three different "optima". That is a noise surface, not a parameter.
8. **The b=1.75 cell fails every pre-registered condition anyway.** Δ +1.425R, but **LONG −1.882R**, **live −0.656R**, halves +1.877/−0.452, **sign-flip p = 0.5921**, and its neighbour at 1.50 is **6.03R worse**. A fence around twelve trades pulling in both directions.
9. **🔴 NOTHING IS PROPOSED. `SL_BUFFER_ATR` STAYS AT 2.5**, and §4c states what moving it would have done to the pre-registered 20-trade count, which now stands at **2 of 20** (vpos 36, 37 — both losers, Σ −1.983R).

---

## 0. METHOD — and the denomination, stated before any number

### 0a. 🔴 THE FIXED REFERENCE, and why it is the only thing that makes the columns comparable

**`SL_BUFFER_ATR` was never swept for exactly one reason: it defines 1R.** Every variant below therefore reports in one unit and one unit only:

```
R_ref (price) = 2.5 x ATR(1h at entry)      <- TODAY's multiplier, never varied
R_ref (USDT)  = initial_risk_usdt as booked <- the risk the bot actually took
```

**A variant with stop multiplier `b` does NOT get to redefine R.** It places its stop at `b × ATR`, and at equal risk the position must therefore shrink:

```
size_b = size_today x (2.5 / b)
```

so **b = 4.0 trades a 62.5 % position** and every price move it captures is worth 62.5 % of what it was. Taker is charged at the real **0.001 on every leg at the variant's own size**; funding is scaled by **both** the smaller notional **and** the 8h stamps the longer hold crosses. That is §2a and §2d discharged, and it is the reason a wider stop cannot be scored on stop-outs avoided alone.

**Verified, not assumed:** across all 31 closed positions `|entry − original_sl| / atr = 2.5000 ± 0.005` (lot-size rounding) and `|entry − original_sl| × size / initial_risk_usdt = 1.0000` exactly. The reference unit is clean.

### 0b. 🔴 WHAT MOVES WITH b, AND THE ONE THING THAT DOES NOT

The brief required the **whole contract** replayed at each level, not the stop alone. It is:

| term | keyed to | moves with b? |
|---|---|---|
| stop distance | `b × ATR` | **yes** |
| trail **arm** (`TRAIL_ARM_R` 0.75) | `0.75 × b × ATR` | **yes** |
| trail **giveback** (`TRAIL_MULT_ATR` 1.875 = 0.75 × 2.5) | `0.75 × b × ATR` | **yes** |
| partial at arm | off since 2026-08-14 | n/a |
| **breakeven-lock target** | `fill × (1 ± 0.0020)` | **🔴 NO** |

**The breakeven target is a fraction of PRICE, not of R** (`trail_arm._BE_TARGET_FRAC_ON`, made an explicit standalone policy number on 2026-08-08 precisely so it would stop being derived from something else). The brief listed it among the things that move with 1R; **in this codebase it does not, by construction.** It is stated here rather than smoothed over, because it means widening the stop makes the BE lock *relatively* tighter — a second-order effect that works mildly **in widening's favour** and still does not save it.

### 0c. The engine, and the two conventions it can run under

| item | value |
|---|---|
| replay resolution | Bybit SOLUSDT-perp **5m** candles via Tor, 35,875 bars, fetched 2026-08-17 13:37 UTC |
| intrabar order | 🔴 **adverse extreme assumed touched FIRST** — a stop always wins a tie |
| taker | **0.001 every leg**, on the variant's actual size |
| funding | recorded `funding_paid`, scaled by notional × 8h stamps crossed |
| signal exits | left in place — they do not depend on `b` |
| recheck tighten | **modelled**: vpos 27/34/35 had their stop halved inside the first 5m bar (tiers 10/60/300 s), and that halving is a fraction of the b-stop, so it scales with b |

🔴 **THE ONE CONVENTION THAT DECIDES THE ANSWER, AND WHY IT IS RUN BOTH WAYS.** When a position that was booked as a stop-out is *not* stopped by a wider stop, the tape has to keep going — and the booked close is exactly the moment the position was most adverse. Truncating there marks every survivor out at its own worst price, which silently rigs the sweep **against** widening.

So the sweep is run under both:

- **TRUNCATED** — exit at the booked close if nothing fires. This is the 19:30 convention. It is a **lower bound** on widening's value.
- **EXTENDED (+H h)** — for booked **stop-outs only**, keep walking real candles up to H hours past the booked close, then mark out at that bar's close. H ∈ {4, 12, 24, 48}. This is the **fair** test and the one quoted throughout. Signal exits are never extended, because a signal exit does not depend on `b`.

### 0d. The engine reproduces the book before it is asked to change anything

| contract at b=2.5 | replay ΣR | booked ΣR | mean Δ | median Δ | within ±0.15R |
|---|---|---|---|---|---|
| 19:30 contract (arm 1.0R, partial ⅓) | **−5.844** | −5.985 | **+0.005** | −0.016 | 23/29 |
| today's contract (arm 0.75R, partial off) | **−2.961** | — | — | — | — |

The first row is the 19:30 report's engine reproduced to **0.09R on 29 positions** (it reported −5.930; the 0.014R/position residual is this pass correcting the BE target from the engine's `2×taker+margin` = 0.0025 to the policy's actual **0.0020**, and modelling the recheck tighten). **The sweep's baseline is the second row: today's live contract, ΣR_ref −2.961 on n=29.**

### 0e. Which book

The 19:30 book is 29 positions (vpos 7–35). Two have closed since (**vpos 36** `exchange_market` −0.757R, **vpos 37** `sl` −1.226R), and both ran under the **new** contract applied 2026-08-14 19:54. **Every headline number below is the n=29 book**, so it is directly comparable to every prior sweep; the n=31 book is carried alongside and never changes a sign.

---

# 1. WHAT ACTUALLY KILLED THE STOPPED POSITIONS

## 1a. 🔴 FIRST: `close_reason='sl'` IS FOUR DIFFERENT DEATHS

| mechanism | n (of 14) | where the stop sat | ΣR |
|---|---|---|---|
| **full 2.5×ATR stop** | **10** | 1.000R | **−10.845** |
| recheck **TIGHTENED** (vpos 27, 34, 35) | 3 | 0.500R | −2.004 |
| **breakeven lock** (vpos 17) | 1 | 0.101R | **+0.004** |

**The parameter under examination is responsible for ten deaths, not fourteen.** Three died at a stop the *post-entry recheck* had halved on a health score — a different mechanism with its own constants — and one was a winner exiting at breakeven. The brief's premise number, −12.845R across 14, is **−10.845R across 10** once the label is unpacked.

## 1b. The 5m anatomy of every stop-out

| vpos | side | p/l | MFE R | MAE R | overshoot past the stop | back through ENTRY | pos24 | dur h | realised R |
|---|---|---|---|---|---|---|---|---|---|
| 10 | SHORT | P | 0.006 | −1.431 | **0.431** | never | 0.14 | 1.4 | −1.066 |
| 12 | LONG | P | 0.561 | −1.058 | 0.252 | never | 0.38 | 13.2 | −1.049 |
| 14 | SHORT | P | −0.075 | −1.027 | 0.114 | never | 0.16 | 9.3 | −1.032 |
| 16 | LONG | P | 0.193 | −1.141 | **0.733** | never | 0.97 | 5.8 | −1.146 |
| 17 | SHORT | P | 1.247 | −0.627 | 0.000 | **0.0 h** | 0.05 | 33.3 | +0.004 |
| 18 | LONG | P | 0.911 | −1.053 | 0.124 | never | 0.92 | 40.5 | −1.074 |
| 20 | SHORT | P | 0.174 | −1.072 | 0.101 | never | −0.21 | 3.0 | −1.124 |
| 22 | LONG | P | 0.300 | −1.107 | 0.340 | never | 1.02 | 57.5 | −1.064 |
| 24 | SHORT | P | 0.265 | −1.006 | 0.006 | never | 0.00 | 16.0 | −1.050 |
| 26 | LONG | P | 0.830 | −1.085 | 0.138 | **7.8 h** | 1.00 | 25.7 | −1.085 |
| 27 | SHORT | P | 0.649 | −0.585 | 0.000 | never | −0.05 | 7.1 | −0.660 |
| 31 | LONG | L | 0.143 | −1.086 | 0.124 | never | 0.50 | 7.2 | −1.155 |
| 34 | SHORT | L | −0.037 | −0.514 | 0.000 | never | −0.04 | 0.5 | −0.643 |
| 35 | SHORT | L | 0.113 | −0.512 | 0.000 | **2.4 h** | 0.07 | 1.2 | −0.701 |
| *37* | *SHORT* | *L* | *0.243* | *−1.043* | *0.043* | *never* | *0.24* | *3.0* | *−1.226* |

**Overshoot** = how far past the stop price the adverse extreme ran **before the first reversal back through that price**:

```
min 0.000R   median 0.124R   max 0.733R
<= 0.10R : 5/14     0.10-0.25R : 5/14     0.25-0.50R : 3/14     > 0.50R : 1/14
```

🔴 **This number is the trap in the brief, and it must be read with §1c or it will mislead.** Ten of fourteen overshot by less than a quarter of an R, which *looks* like the signature of a whisker takeout. **It is not.** Price came back through the *stop price* within minutes in 14 of 14 cases — because it was sitting on that level, oscillating across it. What it did **not** do was come back to the **entry**.

## 1c. 🔴 THE DECISIVE COUNT — did the thesis come back?

| horizon after the stop fired | back through **ENTRY** | back through the **stop price** |
|---|---|---|
| **1 h** | **1 / 14** | 14 / 14 |
| **4 h** | **2 / 14** | 14 / 14 |
| **12 h** | **3 / 14** | 14 / 14 |

*(n=31: 1/15, 2/15, 3/15 — identical.)*

**The brief set the bar itself: "If 10 of 14 came back, the stop is being taken out by noise and the thesis was not wrong — the geometry was." Three came back inside twelve hours, and one of those three (vpos 17) is the breakeven-lock exit, which was never a stop-out at all.**

And the other side of the same tape:

| within … of the exit | went green again | reached ≥ +0.5R | went a **further 0.25R+ AGAINST** |
|---|---|---|---|
| 4 h | 2/14 | 1/14 | **11 / 14** |
| 12 h | 3/14 | 2/14 | **11 / 14** |
| 24 h | 6/14 | 3/14 | **12 / 14** |

Adverse excursion measured from entry, 24h after the exit, for the ten full-stop deaths: **−1.43, −3.61, −3.55, −1.73, −1.91, −1.45, −2.36, −1.60, −1.71, −1.83 R_ref.** Two of them ran past **3R** against.

🔴 **That is not a noise takeout. That is the trade being wrong, exiting at −1R, and the market continuing in the direction it had already chosen.**

## 1d. Range position — the cross the brief asked for, and it is a null

| side | stopped | mean pos24 | not stopped | mean pos24 | diff | permutation p |
|---|---|---|---|---|---|---|
| SHORT (n=29) | 8 | 0.013 | 8 | 0.075 | −0.062 | **0.171** |
| LONG (n=29) | 6 | 0.798 | 7 | 0.895 | −0.097 | **0.428** |
| SHORT (n=31) | 9 | 0.038 | 9 | 0.119 | −0.080 | 0.237 |

**The stopped ones are NOT concentrated at the bottom third relative to the survivors — because ALL the shorts are there.** Across all 18 shorts in the closed book, 9 of 9 stopped and 8 of 9 not-stopped sit below pos24 0.333, and **0 of 18 sit above 0.667**. The 19:00 report's finding is confirmed exactly as it was written: **one behaviour per side, and it does not separate the outcome.** Range position explains where the bot enters. It explains nothing about what kills it.

---

# 2. THE SWEEP

**Baseline: today's live contract at b = 2.5 — ΣR_ref −2.961 (n=29).** Extension +12h past a booked stop.

## 2a. The five levels the brief named

| **b** | ΣR_ref | **Δ vs 2.5** | win % | mean W | mean L | **payoff** | exp | SHORT | LONG | paper | live | taker ΣR | median hold |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **2.0** | −3.241 | **−0.279** | 37.9 % | 1.001 | −0.792 | 1.26 | −0.112 | −0.276 | −2.965 | −3.009 | −0.232 | 4.342 | 6.5 h |
| **2.5 (now)** | **−2.961** | **0.000** | **37.9 %** | **0.904** | **−0.717** | **1.26** | **−0.102** | −1.981 | −0.981 | −2.381 | −0.580 | 3.476 | 9.5 h |
| **3.0** | −6.052 | **−3.091** | 34.5 % | 0.745 | −0.710 | **1.05** | −0.209 | −2.949 | −3.103 | −5.051 | −1.001 | 2.896 | 9.9 h |
| **3.5** | −7.278 | **−4.317** | 34.5 % | 0.613 | −0.706 | **0.87** | −0.251 | −3.743 | −3.535 | −6.637 | −0.641 | 2.483 | 11.0 h |
| **4.0** | −6.511 | **−3.550** | 34.5 % | 0.523 | −0.618 | **0.85** | −0.225 | −2.824 | −3.687 | −6.036 | −0.475 | 2.171 | 14.3 h |

Positions changed:

| b | changed > 0.05R | sign flips | **stop → winner** | winner → loser |
|---|---|---|---|---|
| 2.0 | 15/29 | 2 | 1 | 1 |
| 3.0 | 14/29 | 1 | **0** | 1 |
| 3.5 | 18/29 | 1 | **0** | 1 |
| 4.0 | 24/29 | 1 | **0** | 1 |

🔴 **Not one stop-out becomes a winner at any widening level.** The ≥8-changed-positions condition is met at every cell; the direction of the change is uniformly negative.

**n=31 (with vpos 36, 37), same engine:** baseline −4.923, and Δ = **−0.521 / −2.929 / −4.041 / −3.187** at 2.0 / 3.0 / 3.5 / 4.0; payoff 1.22 → 1.02 → 0.85 → 0.82; **stop-outs converted to winners: 0 at every widening level.** Same shape, same sign, nothing rescued.

## 2b. The truncation convention does not change the verdict — it *understates* the damage

| b | truncated at the booked close | extended +4h | **+12h** | +24h | +48h |
|---|---|---|---|---|---|
| 2.0 | −3.241 | −3.241 | −3.241 | −3.241 | −3.241 |
| **2.5** | **−2.961** | **−2.961** | **−2.961** | **−2.961** | **−2.961** |
| 3.0 | −4.678 | −6.052 | **−6.052** | −6.052 | −6.052 |
| 3.5 | −5.201 | −7.115 | **−7.278** | −8.003 | −8.003 |
| 4.0 | −4.449 | −5.378 | **−6.511** | −6.683 | −6.408 |

🔴 **Every cell above 2.5 gets WORSE the more rope the tape is given.** The truncated engine — the one that marks survivors out at their worst price and should therefore be biased *against* widening — is the **kindest** column widening has. That is the opposite of what a noise-takeout world would produce, and it is the same fact as §1c seen through the sweep.

## 2c. 🔴 THE WHOLE CONTRACT REPLAYED — and the "best" cell moves with it

The brief required this and it is the single most informative table in the study.

| contract | engine | ΣR at 1.5 / 1.75 / 2.0 / 2.25 / **2.5** / 2.75 / 3.0 / 3.5 / 4.0 | best cell |
|---|---|---|---|
| **today** (arm 0.75R, partial off) | truncated | −7.57 / **−1.54** / −3.24 / −2.95 / **−2.96** / −3.81 / −4.68 / −5.20 / −4.45 | **1.75** |
| **today** | extended +12h | −7.57 / **−1.54** / −3.24 / −2.95 / **−2.96** / −4.27 / −6.05 / −7.28 / −6.51 | **1.75** |
| **19:30** (arm 1.0R, partial ⅓) | extended +12h | −10.15 / −6.09 / −5.47 / **−3.55** / −5.84 / −6.49 / −6.96 / −7.96 / −6.96 | **2.25** |
| **naked** (stop only, no arm/BE/trail) | extended +12h | −8.81 / −7.38 / −8.14 / −7.31 / −7.83 / −8.25 / −8.61 / −8.21 / **−7.19** | **4.0** |

🔴 **Three contracts, three different optima — 1.75, 2.25 and 4.0 — spanning the entire grid.** A parameter whose best value is decided by which trail you happen to be running is not a parameter with a best value on this sample. **And the naked row is the cleanest reading of the axis with nothing else in the way: it is flat.** Across a 2.7× range of stop widths (1.5 → 4.0) the whole grid spans **1.62R**, and its "best" cell (4.0, −7.19) is only **0.19R** better than the cell at the opposite end of the grid (1.75, −7.38) — two settings that differ by a factor of 2.3 in stop width and by a fifth of one R in outcome. **There is no stop-width signal in this book.**

## 2d. Costs, charged

| b | taker across the book (R_ref) | funding across the book (R_ref) | median hold |
|---|---|---|---|
| 2.0 | 4.342 | +0.028 | 6.5 h |
| **2.5** | **3.476** | **+0.022** | 9.5 h |
| 3.0 | 2.896 | +0.019 | 9.9 h |
| 3.5 | 2.483 | +0.016 | 11.0 h |
| 4.0 | 2.171 | +0.014 | 14.3 h |

**Widening does save real fees — 1.31R of taker across 29 positions going from 2.5 to 4.0**, because the position is 37.5 % smaller and every leg is charged on it. **That saving is already inside every ΣR above, and it is not close to paying for what widening costs.** Funding is a rounding error at every level (+0.022R over the whole book at b=2.5, and it *falls* with b despite the 4.8h longer median hold, because notional falls faster than stamps accumulate). It is reported so it is not assumed to be doing work it is not doing.

---

# 3. THE INTERACTION THAT MATTERS MOST

## 3a. The trade-off, stated numerically

Baseline b=2.5: **11 winners, ΣR +9.944** · **11 stop deaths, ΣR −10.784**.

| b | stop-outs → **winner** | stop-outs → flat | **Δ on the stop cohort** | **Δ on the winner cohort** | **net Δ** |
|---|---|---|---|---|---|
| 1.50 | 2 | 0 | **+1.168** | **−5.178** | −4.608 |
| 1.75 | 1 | 1 | +1.306 | +1.034 | +1.425 |
| 2.00 | 1 | 0 | +0.377 | +1.064 | −0.279 |
| 2.25 | 0 | 0 | −0.141 | +1.553 | +0.007 |
| **2.50** | **0** | **0** | **0.000** | **0.000** | **0.000** |
| 2.75 | 0 | 0 | +0.116 | −1.583 | −1.311 |
| **3.00** | **0** | **0** | **+0.212** | **−2.498** | **−3.091** |
| **3.50** | **0** | **0** | **+0.830** | **−4.618** | **−4.317** |
| **4.00** | **0** | **0** | **+2.193** | **−5.421** | **−3.550** |

🔴 **Read the two Δ columns against each other. That IS the answer.** At b=3.5 the wider stop hands back **+0.830R** to the cohort it was supposed to rescue and takes **−4.618R** off the winners. **The rescue is real and it is one fifth the size of the bill.**

## 3b. 🔴 Why the winners shrink and the losers do not

| b | mean winner | pure-size prediction (×2.5/b) | mean loser | pure-size prediction |
|---|---|---|---|---|
| 2.0 | 1.001 | 1.130 | −0.792 | −0.896 |
| **2.5** | **0.904** | — | **−0.717** | — |
| 3.0 | **0.745** | **0.753** | **−0.710** | −0.597 |
| 3.5 | **0.613** | **0.646** | **−0.706** | −0.512 |
| 4.0 | **0.523** | **0.565** | **−0.618** | −0.448 |

**Winners track the size prediction to within 0.04R.** They are capped by a favourable move that is fixed in price, so shrinking the position shrinks them one-for-one.

**Losers refuse to.** At b=3.0 the size effect predicts −0.597 and the book delivers **−0.710** — 19 % worse. The reason is §1c: the adverse move keeps going, so it reaches the wider stop as well, and a full stop-out at 3.0×ATR on a 5/6-size position costs the same USDT as a full stop-out at 2.5×ATR on a full-size one. **Widening does not make the loss smaller. It only makes the loss take longer.**

## 3c. The ten full-stop deaths, followed all the way

Within the booked life, the MAE distribution says widening should be a massacre of avoided deaths:

```
positions whose 5m MAE would still breach a stop at 2.5 x ATR : 10/29
                                                     3.0 x ATR :  1/29   (vpos 10, needs 3.58)
                                                     3.5 x ATR :  1/29
                                                     4.0 x ATR :  0/29
```

**Nine of the ten would have survived their own worst moment at 3.0×ATR.** Now let the tape run on:

| vpos | b=2.5 | b=3.0 | b=3.5 | b=4.0 |
|---|---|---|---|---|
| 10 | −1.087 stop | −1.072 stop | −1.062 stop | −0.699 horizon |
| 12 | −1.090 stop | −1.075 stop | −1.065 stop | −1.057 stop |
| 14 | −1.051 stop | −1.042 stop | −1.036 stop | −1.032 stop |
| 16 | −1.119 stop | −1.100 stop | −1.086 stop | −1.075 stop |
| 18 | +0.071 trail | −0.000 trail | −0.804 horizon | −0.704 horizon |
| 20 | −1.107 stop | −1.089 stop | −1.077 stop | −0.724 horizon |
| 22 | −1.105 stop | −1.087 stop | −1.075 stop | −1.066 stop |
| 24 | −1.092 stop | −1.077 stop | −1.066 stop | −0.786 horizon |
| 26 | −0.000 trail | −1.125 stop | −1.107 stop | −1.093 stop |
| 31 | −1.150 stop | −1.126 stop | −0.642 horizon | −0.561 horizon |
| **ΣR** | **−8.731** | **−9.795** | **−10.020** | **−8.796** |
| still stopped | 8/10 | **9/10** | 8/10 | 5/10 |
| turned positive | 1/10 | **0/10** | **0/10** | **0/10** |

🔴 **Nine of the ten that a 3.0× stop would have saved inside their booked life are stopped anyway once the tape continues — and the cohort is 1.06R WORSE, not better.** vpos 26 is the sharpest case: at b=2.5 today's 0.75R arm rescues it to a breakeven scratch; **widen the stop and the arm moves out with it, the lock never arms, and the position dies at −1.125R.** That is what "replay the whole contract" catches and a stop-only sweep would have missed.

**And the upper bound, with the stop deleted entirely** and the same ten marked out 12h past their booked exit:

```
ΣR with NO STOP AT ALL : -11.594     (they realised -8.731 at today's stop)
positive: 1 of 10 (vpos 26, +0.279)
```

🔴 **Removing the stop altogether costs 2.86R more than keeping it. The stop is not the leak. It is the patch.**

## 3d. Is the curve monotone? — plainly, per the standing test

| axis | shape | best cell | is the best cell a spike? |
|---|---|---|---|
| `SL_BUFFER_ATR`, today's contract, extended | **NON-MONOTONE** (3 up, 5 down) | **1.75** | 🔴 **YES.** 1.50 is **6.03R worse**, 2.00 is **1.70R worse** |
| the same, 19:30 contract | **NON-MONOTONE** (4 up, 4 down) | 2.25 | **YES** — 2.0 is 1.92R worse, 2.5 is 2.29R worse |
| the same, naked stop | **NON-MONOTONE** (4 up, 4 down) | 4.0 | flat: whole grid spans 1.62R |
| **restricted to the five cells the brief named** | **NON-MONOTONE** (2 up, 2 down) | **2.5 = the incumbent** | n/a — nothing beats the current setting |

**On the grid the brief specified — {2.0, 2.5, 3.0, 3.5, 4.0} — the maximum is the setting already in the file, and it is not close: the nearest challenger is 0.279R worse and the rest are 3.1–4.3R worse.**

The b=1.75 cell, audited on the same conditions every prior candidate was killed on:

| condition | b=1.75 | b=2.25 |
|---|---|---|
| beats 2.5 on **BOTH sides** | ❌ SHORT +3.307, **LONG −1.882** | ❌ SHORT +0.584, **LONG −0.577** |
| **monotone** on its axis | ❌ **no — 1.50 is 6.03R worse** | ❌ no |
| survives era / halves de-confounding | ❌ paper +2.081, **live −0.656**; halves +1.877 / **−0.452** | ❌ halves +0.711 / −0.704 |
| ≥ **8 positions changed** | ✅ 23/29 | ✅ 14/29 |
| paired **sign-flip p** | ❌ **0.5921** | ❌ 0.9981 |
| worst leave-one-out Δ | +0.335 | −0.319 |

**Twelve positions carry the 1.75 cell and they pull in both directions** (vpos 26 −1.218, vpos 12 +1.090, vpos 13 +0.979, vpos 29 −0.917, vpos 11 +0.731, vpos 27 +0.657, vpos 23 +0.633 …), summing +1.700R inside a net of +1.425R. **One of four conditions met, on a p of 0.59. Dead on arrival, and it is a narrowing, not a widening.**

## 3e. 🔴 DOES WIDENING MAKE THE PAYOFF PROBLEM BETTER OR WORSE? — answered directly

The brief flagged this as possibly the whole answer. It is.

| b | win % | mean W | mean L | **payoff** | break-even payoff | **gap the mean winner must close** | **positions that ever touched 1.5× their OWN R** |
|---|---|---|---|---|---|---|---|
| 2.00 | 37.9 % | 1.001 | −0.792 | 1.26 | 1.64 | +0.295R | 8 / 29 |
| **2.50** | **37.9 %** | **0.904** | **−0.717** | **1.26** | **1.64** | **+0.269R** | **6 / 29** |
| 2.75 | 34.5 % | 0.836 | −0.665 | 1.26 | 1.90 | +0.427R | 6 / 29 |
| **3.00** | 34.5 % | 0.745 | −0.710 | **1.05** | 1.90 | **+0.605R** | **4 / 29** |
| **3.50** | 34.5 % | 0.613 | −0.706 | **0.87** | 1.90 | **+0.728R** | 4 / 29 |
| **4.00** | 34.5 % | 0.523 | −0.618 | **0.85** | 1.90 | +0.651R | **2 / 29** |

🔴 **WORSE, and monotonically so above 2.5.** The payoff falls from 1.26 to 0.85 — **through 1.00**, meaning at b ≥ 3.5 the average winner is *smaller than the average loser* — while the win rate does not move at all (34.5 % at every widening level; **zero** stop-outs are converted). And the excursion count, which the 19:30 report identified as the binding constraint, collapses: **6 of 29 positions ever touched 1.5R at today's stop; at b=4.0 only 2 of 29 ever touch 1.5× of the bigger R.**

**The 19:30 finding was "the moves are not there." Widening the stop makes R bigger, so the same moves become a smaller multiple of it. It does not manufacture excursions; it deflates the ones that exist.**

---

# 4. VERDICT

## 4a. No level beats 2.5. Nothing is proposed.

**On the pre-registered grid the brief specified, the incumbent is the maximum**, and the conditions the brief set — beats 2.5 on **both** sides, **monotone**, **≥8** positions changed, survives de-confounding — are met by **no cell at any level, in either direction**:

| candidate | both sides | monotone | ≥8 changed | de-confounded | verdict |
|---|---|---|---|---|---|
| b = 2.0 | ❌ LONG −1.984 | ❌ | ✅ 15 | ❌ p=0.887 | **dead** |
| b = 3.0 | ❌ both negative | ❌ | ✅ 14 | ❌ **significantly WORSE**, p=0.0115 | **dead** |
| b = 3.5 | ❌ both negative | ❌ | ✅ 18 | ❌ worse, p=0.0329 | **dead** |
| b = 4.0 | ❌ both negative | ❌ | ✅ 24 | ❌ worse, p=0.139 | **dead** |
| b = 1.75 *(off-grid)* | ❌ LONG −1.882 | ❌ **spike** | ✅ 23 | ❌ live −0.656, p=0.592 | **dead** |

**`SL_BUFFER_ATR` stays at 2.5. Nothing is proposed, nothing is applied, no file was written.**

## 4b. 🔴 WIDENING MAKES IT WORSE, AND THE BRIEF ASKED FOR THAT TO BE SAID PLAINLY

It is true, so it is said plainly.

```
widening 2.5 -> 3.0  saves  9 of the 10 deep MAEs inside their booked life
                     and    9 of those 10 are stopped anyway once the tape runs on
                     hands back  +0.212R  to the stop cohort
                     takes off   -2.498R  from the winners
                     net         -3.091R
deleting the stop entirely on those ten:  -11.594R  vs  -8.731R  with it
payoff 1.26 -> 1.05 -> 0.87 -> 0.85 ;  stop-outs converted to winners: 0, 0, 0
```

**The payoff shrinks faster than the stop-outs fall. The stop is not the defect.**

**And the tightness is a symptom of the instrument's move size, exactly as the brief anticipated.** The mechanism is arithmetic, not statistics: at equal risk the position is `2.5/b` of its size, so **every favourable excursion is worth `2.5/b` of what it was**, while the adverse excursion — which §1c shows keeps going — reaches the wider stop too and costs the same USDT. **A wider stop buys time on a move that has already decided against you, and pays for it with every move that decides for you.** That is the 19:30 conclusion — *SOL's average move after one of this bot's signals is too small to support this geometry at this win rate* — arriving from the second direction, and it arrives without needing a single new statistical claim.

**The honest counterweight, unchanged and still binding:** this is 29 positions of which 22 are paper, and the live sub-book is 7 (9 including the two new closes) with a standard error on the mean of ±0.31R. **Seven trades cannot tell a −0.11R edge from a +0.4R one, and they cannot tell 2.5 from 3.0 either.** What this pass establishes is not that 2.5 is optimal. It is that **there is no evidence in this book that any other value is better, that the one axis with a large effect points the wrong way, and that the mechanism by which widening loses is structural rather than sampled.**

## 4c. 🔴 WHAT A CHANGE TO `SL_BUFFER_ATR` WOULD DO TO THE PRE-REGISTERED STOPPING RULE

Named before anything is decided, as required.

**The rule as registered (2026-08-14):** *the next 20 LIVE closes — vpos 36 → 55, ~2026-09-03 — and if the book is still negative, stop trading this signal set rather than look for a 27th candidate.*

**Where the count stands right now: 2 of 20.**

```
vpos 36  exchange_market  -0.757 R
vpos 37  sl              -1.226 R
                    sum  -1.983 R
live book to date (vpos 29-37, n=9):  -2.593 R
whole closed book (n=31):             -7.967 R
```

🔴 **Moving `SL_BUFFER_ATR` mid-count would void the count, and not by convention — by arithmetic.**

1. **It re-denominates R.** `1R = SL_BUFFER_ATR × ATR × size`. vpos 36 and 37 are recorded in a 2.5× R. Positions 38–55 would be recorded in a different one. **Summing them is adding two different units**, and the rule's test — "is the book still negative" — would be evaluated on a sum that has no unit. Every prior report, every `initial_risk_usdt` in the table, and every R-multiple in this document would stop being comparable to what came after. This is precisely the §0 R-boundary that `TRAIL_ARM_R` and `TRAIL_MULT_ATR` were deliberately chosen to avoid needing (both are *fractions* of R; neither moves it).
2. **It changes the thing being tested.** The 20 closes are meant to judge *this signal set under this geometry*. Change the stop and they judge a new geometry on a sample that starts at 2, not 20 — the count would have to reset to 0/20 and the ~03.09 date would move out by roughly three weeks at the observed 1.02 entries/day.
3. **It also moves the arm and the trail**, because both are keyed to R (§0b) — so it is not one change under test but three, and §3c shows one of them (vpos 26) reverses sign on the arm alone.

**Therefore: if `SL_BUFFER_ATR` is ever moved, the stopping rule must be explicitly re-registered from zero on the new unit, with a stated §0 R-boundary, and vpos 36–37 must be excluded from the new count rather than carried into it.** Nothing in this pass gives any reason to do that.

---

## STATE — nothing was changed by this pass

```
mercury-sol   active - MainPID 2195203 - since 2026-08-14 19:54:37 UTC - NRestarts=0
              NOT restarted by this pass. FLAT: zero open positions.
GEOMETRY      unchanged and verified from the running module's own globals:
              SL_BUFFER_ATR 2.5 - TRAIL_ARM_R 0.75 - TRAIL_MULT_ATR 1.875 (=0.75R)
              PARTIAL_AT_ARM_ENABLED False - ATR_TF 1h
BOOK          31 closed - booked SumR -7.967 - live sub-book (vpos 29-37) -2.593
              stopping rule: 2 of 20 live closes done (vpos 36, 37), both losers
FILES         mercury-sol: ZERO .py modified. No DB write. No order. No restart.
              Read-only URI (mode=ro) on trades.db throughout.
CANDIDATES    26 entry-side (all dead) + the 19:30 geometry pass (1 monotone axis,
              1 unidentifiable level) + this pass: SL_BUFFER_ATR swept for the first
              time, 9 cells x 3 contracts x 5 engines. NOTHING PROPOSED.
titan         /root/titan-bot - NOT touched, NOT read for state, NO numbers imported.
              HEAD 897850b - working tree clean
```

**Provenance: SOL's own `trades.db` opened `mode=ro`; Bybit SOLUSDT-perp 5m candles pulled through the bot's own venue over Tor at 2026-08-17 13:37 UTC (35,875 bars); the replay engine re-validated against the booked book at mean Δ +0.005R on the 19:30 contract before any variant was run; the `recheck_status='tightened'` and `mgmt_state_json` fields read directly to separate the four mechanisms hiding under `close_reason='sl'`. Titan was not read.**
