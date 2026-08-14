# Mercury-SOL — the four-hour edge is real, it is on the wrong side, and it is smaller than the cost of harvesting it

**2026-08-14 19:15 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · READ-ONLY THROUGHOUT — no file written, no restart, no order, no DB write. Nothing proposed before §4, and nothing applied at all.**

Titan (`/root/titan-bot`): **not touched, not read for state, no numbers imported.** HEAD `897850b`, clean.

Acts on [19:00 §2c and §4a](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-14-1900-sol-where-in-the-range-it-enters-one-behaviour-per-side-and-it-does-not-decide-the-outcome.md).

---

## ⚡ THE SHORT VERSION

1. **The reframe is right and I accept it.** At T+4h "has the level broken" is observable, the position is still open, and it is a thesis check rather than a forecast. The rule was replayed properly and charged real costs.
2. **🔴 IT DIES ON EVERY ONE OF THE THREE STATED CRITERIA, AND IT DIES ON THE SIDE THE EDGE WAS FOUND ON.**
   - **Only longs.** At +4h: LONG **+3.392R**, SHORT **−1.047R**. The four-hour edge in §2c was measured on **shorts** (2.21× more breaks than chance). The rule helps the side where no edge was ever found and hurts the side where one was.
   - **Only paper.** paper **+2.873R**, live **−0.529R** — and the live era is negative at **every horizon tested**, 1h through 24h.
   - **Non-monotone.** The sweep runs +1.136 (1h) → **−0.521 (2h)** → **+3.707 (3h)** → +2.344 (4h) → +2.960 (5h) → +1.701 (6h) → +1.623 (8h) → +1.458 (10h) → +1.921 (12h) → +0.928 (24h). The maximum is at **3h**, and 2h is negative. That is a fitted maximum, exactly the ADX-surface shape.
   - **It does not survive de-confounding.** Paired sign-flip on the 15 changed positions: mean **+0.156R, p = 0.4379**; day-clustered **p = 0.4413**. Nowhere near any bar.
3. **🔴 AND THE ANSWER TO THE QUESTION THE PASS EXISTS FOR: the four-hour edge is REAL and NOT SPENDABLE.** The bot's shorts do break the 24 h low at 2.21× the base rate — but **the mean short is at −0.050R gross at +4h**, because the 9 that hold lose −0.550R each against the 7 that break gaining +0.592R. **The edge exists in how often the level breaks. It does not exist in R.** Add the 0.116R round-trip taker and a perfect four-hour harvest of the short book is **−0.167R per trade**.
4. **Most of the damage is already done by +4h.** The 19 held-level positions average **−0.326R at +4h** and close at **−0.475R**. Cutting at four hours saves the last 0.149R of a loss that was 0.326R deep before the rule could act.
5. **The mechanism to do this already exists and has never once used it: the exit advisor has produced 35 verdicts since 2026-08-09 and every single one is `hold`. Zero `close`, ever.** Its prompt contains **no** reference to the 24 h range, the entry's placement, or any price level outside the position's own stop.
6. **Candidate twenty-six is dead.** Nothing proposed, nothing applied.

---

## 0. PROVENANCE AND COST MODEL

| item | source |
|---|---|
| positions, fills, partials, funding | `trades.db` opened `mode=ro` — `virtual_positions` |
| price paths | Bybit SOLUSDT-perp **5m** candles via Tor, 35,074 bars to 2026-08-14 18:45 |
| `pos24`, `lo24`, `hi24`, the break/held split | the 19:00 report's own computed table — **not re-derived** |
| **1R** | `|entry − original_sl_price|` in price terms; `initial_risk_usdt` = that × entry size (verified on all 29) |
| **taker** | **0.001 both legs**, the venue rate the bot reads at boot |
| **funding** | recorded `funding_paid` scaled by 8h stamps (00/08/16 UTC) crossed |

🔴 **The actual column is RE-COSTED, not the booked number.** The 22 paper rows were booked at the old `0.00055` constant; charging all 29 at the venue's real `0.001` moves the book from the familiar **−5.985R to −7.114R**. Both columns in every comparison below carry the same cost model, so the delta is clean.

---

# 1. HOW LONG IT HOLDS, AND WHERE THE R IS LOST

## 1a. Duration of all 29 (hours)

| cohort | n | min | q1 | **median** | q3 | max |
|---|---|---|---|---|---|---|
| ALL | 29 | 0.53 | 5.00 | **9.91** | 20.07 | 57.50 |
| SHORT | 16 | 0.53 | 3.01 | **6.06** | 13.99 | 33.33 |
| LONG | 13 | 5.81 | 7.19 | **15.00** | 25.45 | 57.50 |
| winners | 10 | 2.89 | 10.77 | **19.55** | 21.68 | 33.33 |
| losers | 19 | 0.53 | 4.33 | **7.12** | 14.10 | 57.50 |
| SHORT win | 6 | 2.89 | 7.08 | 16.70 | 20.76 | 33.33 |
| SHORT lose | 10 | 0.53 | 1.83 | **4.33** | 8.75 | 15.97 |
| LONG win | 4 | 9.91 | 16.75 | 20.47 | 22.80 | 25.45 |
| LONG lose | 9 | 5.81 | 6.50 | 13.20 | 25.66 | 57.50 |

**The premise holds: the median position lives 9.9 hours, well past the four-hour mark.** Longs live 15 hours median. **But losing shorts die in 4.33 h median** — the stop gets them before a four-hour rule could.

## 1d. 🔴 HOW MANY CLOSED BEFORE +4h — excluded from §2 explicitly

```
closed before + 1h :  1  (34)
closed before + 2h :  3  (10, 34, 35)
closed before + 4h :  5  (10, 20, 25, 34, 35)      <- a 4h rule CANNOT govern these
closed before + 6h : 10       before + 8h : 13       before +12h : 16
```

🔴 **One correction to the brief.** It says *"vpos 25 (+1.257) broke at +4h so the rule keeps it"*. vpos 25 **closed at 2.89 h**, before the rule could look. The rule never touches it either way — it is protected by having already ended, not by the break test. Same for vpos 10, 20, 34, 35 — all four losers that the rule also cannot help.

## 1b. Duration crossed with the +4h break/held split

| | n | ΣR | mean R | win | still OPEN at +4h | those stayed a further… |
|---|---|---|---|---|---|---|
| **HELD at +4h** | 19 | **−10.570** | −0.556 | 21 % | **15** (ΣR −7.035) | median **11.00 h** (q1 2.84, q3 19.22, max 36.49) |
| **BROKE at +4h** | 10 | **+4.585** | +0.459 | 60 % | **9** (ΣR +3.328) | median 6.99 h (q1 3.12, q3 16.07, max 53.50) |

**So the rule's real population is 15 positions, not 19.** Four of the held-level group (10, 20, 34, 35) were already stopped out before four hours, carrying −3.534R that no exit rule can reach.

## 1c. 🔴 THE R CURVE — where is R made and given back?

Gross R, no fees, from candles: `(entry − p)/|entry − original_SL|` for SHORT, mirrored for LONG.

| cohort | mean R **+1h** | mean R **+4h** | mean R **+12h** | mean R **at close** |
|---|---|---|---|---|
| ALL 29 | −0.064 | −0.033 | −0.158 | −0.123 |
| **HELD at +4h (19)** | −0.178 | **−0.326** | −0.296 | **−0.475** |
| **BROKE at +4h (10)** | +0.152 | **+0.522** | +0.091 | **+0.546** |
| HELD **and still open** at +4h (15) | −0.100 | −0.237 | −0.177 | −0.395 |
| SHORT (16) | −0.059 | −0.050 | −0.280 | −0.092 |
| LONG (13) | −0.071 | −0.012 | −0.017 | −0.161 |
| winners (10) | +0.125 | +0.405 | +0.373 | +0.967 |
| losers (19) | −0.164 | −0.264 | −0.453 | −0.697 |

🔴 **Read the HELD row.** It is already at **−0.326R at four hours** and finishes at **−0.475R**. **Most of the loss is booked before the rule is allowed to speak.** The four-hour rule is not intercepting a slow bleed — it is arriving after two thirds of the damage, to save the last third.

**And the BROKE row peaks at +4h (+0.522) and sags to +0.091 by +12h before recovering to +0.546 at close** — the winners are made in the first four hours, given back by twelve, and re-made by the exit. That is a real and unflattering description of the current exit geometry, and it is the strongest argument in this whole pass for looking at exits rather than entries.

---

# 2. THE COUNTERFACTUAL

> **RULE, stated before the numbers:** at **T+4h**, if the 24 h extreme the entry was placed against has **not** been closed through **in the trade's favour**, close at market. Positions already closed at T+4h are untouched. Positions whose level *has* broken are left to run.

## 2a. Replayed over all 29

| vpos | side | era | dur_h | @4h | booked R | **re-costed R** | **rule R** | Δ |
|---|---|---|---|---|---|---|---|---|
| 7 | LONG | paper | 21.91 | BROKE | +2.089 | +2.050 | +2.050 | +0.000 |
| **8** | LONG | paper | 6.50 | HELD | −0.739 | −0.776 | −0.326 | **+0.450** |
| **9** | LONG | paper | 5.91 | HELD | −0.264 | −0.304 | −0.139 | **+0.165** |
| 10 | SHORT | paper | 1.42 | *closed* | −1.066 | −1.106 | −1.106 | +0.000 |
| **11** | SHORT | paper | 20.99 | HELD | +1.133 | +1.100 | **−0.265** | **−1.365** 🔴 |
| **12** | LONG | paper | 13.20 | HELD | −1.049 | −1.089 | +0.123 | **+1.212** |
| 13 | SHORT | paper | 5.00 | BROKE | +1.337 | +1.301 | +1.301 | +0.000 |
| **14** | SHORT | paper | 9.29 | HELD | −1.032 | −1.056 | −0.816 | **+0.239** |
| 15 | SHORT | paper | 20.07 | BROKE | +0.140 | +0.104 | +0.104 | +0.000 |
| **16** | LONG | paper | 5.81 | HELD | −1.146 | −1.198 | −0.229 | **+0.969** |
| **17** | SHORT | paper | 33.33 | HELD | +0.004 | −0.041 | −0.428 | **−0.387** 🔴 |
| **18** | LONG | paper | 40.49 | HELD | −1.074 | −1.114 | −0.239 | **+0.875** |
| 19 | SHORT | paper | 13.33 | BROKE | +0.463 | +0.417 | +0.417 | +0.000 |
| 20 | SHORT | paper | 3.05 | *closed* | −1.124 | −1.173 | −1.173 | +0.000 |
| **21** | LONG | paper | 19.03 | HELD | +0.285 | +0.208 | +0.053 | **−0.155** 🔴 |
| 22 | LONG | paper | 57.50 | BROKE | −1.064 | −1.110 | −1.110 | +0.000 |
| **23** | SHORT | paper | 4.16 | HELD | −0.577 | −0.633 | −0.514 | **+0.119** |
| **24** | SHORT | paper | 15.97 | HELD | −1.050 | −1.091 | −0.745 | **+0.346** |
| 25 | SHORT | paper | 2.89 | *closed* | +1.257 | +1.165 | +1.165 | +0.000 |
| **26** | LONG | paper | 25.66 | HELD | −1.085 | −1.155 | −0.752 | **+0.404** |
| 27 | SHORT | paper | 7.12 | BROKE | −0.660 | −0.729 | −0.729 | +0.000 |
| 28 | SHORT | paper | 10.99 | BROKE | −0.153 | −0.220 | −0.220 | +0.000 |
| 29 | LONG | **live** | 9.91 | BROKE | +1.355 | +1.329 | +1.329 | +0.000 |
| **30** | LONG | **live** | 25.45 | HELD | +0.762 | +0.736 | **−0.600** | **−1.336** 🔴 |
| **31** | LONG | **live** | 7.19 | HELD | −1.155 | −1.155 | −0.147 | **+1.009** |
| 32 | SHORT | **live** | 4.50 | BROKE | −0.180 | −0.180 | −0.180 | +0.000 |
| **33** | LONG | **live** | 15.00 | HELD | −0.049 | −0.049 | −0.250 | **−0.201** 🔴 |
| 34 | SHORT | **live** | 0.53 | *closed* | −0.643 | −0.643 | −0.643 | +0.000 |
| 35 | SHORT | **live** | 1.16 | *closed* | −0.701 | −0.701 | −0.701 | +0.000 |

```
BOOK    booked ΣR −5.985  |  re-costed actual ΣR −7.114  |  RULE ΣR −4.770   (Δ +2.344)
SHORT   n=16   actual −3.486   rule −4.534   Δ −1.047     5 positions touched
LONG    n=13   actual −3.628   rule −0.236   Δ +3.392    10 positions touched
paper   n=22   actual −6.451   rule −3.578   Δ +2.873    12 touched
live    n= 7   actual −0.663   rule −1.191   Δ −0.529     3 touched
```

## 2b. 🔴 WHAT IT COSTS — named, immediately

**It harms 5 positions and helps 10.** The count favours it; the two largest single deltas in the whole replay are both harms.

| harmed | what it was | what the rule makes it | cost |
|---|---|---|---|
| **vpos 11** SHORT | **+1.100R** — the level HELD at +4h and it won anyway, 21 h later | **−0.265R** | **−1.365R** |
| **vpos 30** LONG | **+0.736R** — held at +4h, trailed out 25 h later | **−0.600R** | **−1.336R** |
| **vpos 17** SHORT | −0.041R scratch, held 33 h | −0.428R | −0.387R |
| **vpos 33** LONG | −0.049R scratch | −0.250R | −0.201R |
| **vpos 21** LONG | +0.208R, trailed | +0.053R | −0.155R |
| | | **total harm** | **−3.444R** |

| helped | cost avoided |
|---|---|
| vpos 12 +1.212 · 31 +1.009 · 16 +0.969 · 18 +0.875 · 8 +0.450 · 26 +0.404 · 24 +0.346 · 14 +0.239 · 9 +0.165 · 23 +0.119 | **total help +5.788R** |

**Net +2.344R — and it is carried entirely by ten paper-era saves against two live-era mutilations.** The brief asked me to say so immediately if it cuts more winners than it saves losers: it does not, on count. **But it destroys the two best held-level outcomes in the book** — vpos 11, which held at four hours and then delivered +1.1R over the following 17 hours, and vpos 30, the second-best live trade.

## 2c. 🔴 THE HORIZON SWEEP — non-monotone, and the maximum is not at 4h

| h | touched | ΣR under rule | **Δ book** | SHORT Δ | LONG Δ | paper Δ | **live Δ** |
|---|---|---|---|---|---|---|---|
| 1 | 21 | −5.978 | **+1.136** | −1.026 | +2.162 | +2.702 | **−1.567** |
| **2** | 20 | −7.635 | **−0.521** 🔴 | −1.728 | +1.207 | +1.906 | **−2.427** |
| **3** | 20 | −3.407 | **+3.707** ← max | −0.336 | +4.043 | +4.522 | **−0.815** |
| 4 | 15 | −4.770 | +2.344 | **−1.047** | +3.392 | +2.873 | **−0.529** |
| 5 | 14 | −4.154 | +2.960 | +0.066 | +2.894 | +3.593 | **−0.633** |
| 6 | 13 | −5.413 | +1.701 | −0.684 | +2.384 | +2.514 | **−0.813** |
| 8 | 10 | −5.491 | +1.623 | +0.116 | +1.508 | +3.242 | **−1.619** |
| 10 | 8 | −5.656 | +1.458 | +0.580 | +0.878 | +2.508 | **−1.050** |
| 12 | 8 | −5.193 | +1.921 | +0.494 | +1.428 | +2.696 | **−0.775** |
| 18 | 2 | −5.313 | +1.801 | +0.000 | +1.801 | +1.801 | 0.000 |
| 24 | 2 | −6.186 | +0.928 | +0.000 | +0.928 | +0.928 | 0.000 |

🔴 **The curve oscillates: up, DOWN THROUGH ZERO, up to its maximum, down, up, down.** The best cell is **3h (+3.707)** and its immediate neighbour at 2h is **negative (−0.521)**. A rule whose value swings 4.2R between two adjacent hours is reading noise, and picking 4h out of that surface is picking a number off a fitted maximum — the exact objection the ADX + range-width surface died on.

**The SHORT side is negative at the chosen horizon and changes sign four times across the sweep.** **The LIVE era is negative at every single horizon tested.**

## 2d. The costs, charged and made explicit

```
round-trip taker at 0.001 both legs   = 0.120 R per position on average
                                        (min 0.051 R, max 0.199 R)  = 3.390 R across the book
re-costing the paper rows from 0.00055 to 0.001 alone   -1.129 R
funding recorded across the whole book                   0.045057 USDT total (live rows only)
   -> 0.51 % of live risk. It cannot move any conclusion here, and it is stated so it is not
      assumed to be doing work it is not doing.
```

🔴 **A point of precision that matters for reading §2a:** the taker cost is **not** a differential between "close at 4h" and "hold" — you pay one entry and one exit either way. The fee therefore does **not** explain the rule's failure. It explains something else, in §4c.

## 2e. 🔴 DE-CONFOUND per §2.54 — on the paired delta, the 15 changed positions

```
touched n=15   mean Δ +0.156R   ΣΔ +2.344R   positive in 10 of 15

  sign-flip permutation on the paired delta          mean +0.156   p = 0.4379
  DAY-CLUSTERED sign-flip (whole days flipped)       mean +0.156   p = 0.4413

  SHORT   n= 5   ΣΔ −1.047   mean −0.209   positive 3/5
  LONG    n=10   ΣΔ +3.392   mean +0.339   positive 7/10
  paper   n=12   ΣΔ +2.873   mean +0.239   positive 9/12
  live    n= 3   ΣΔ −0.529   mean −0.176   positive 1/3
  first half  n=7  ΣΔ +1.285  mean +0.184
  second half n=8  ΣΔ +1.060  mean +0.132
  hour buckets (6h)  means  {00-06h: +0.006, 06-12h: +0.478, 12-18h: +0.557, 18-24h: −0.397}
```

**p = 0.44.** The halves are at least stable in sign, which is more than the score correlation managed — but stability around a mean that is indistinguishable from zero is not evidence. **Three positions in the live era, one of them positive.**

---

# 3. WHAT ALREADY EXISTS THAT COULD DO THIS

## 3a. 🔴 THE EXIT ADVISOR HAS SAID `hold` 35 TIMES OUT OF 35

```
35 verdicts, 2026-08-09 18:42:33 -> 2026-08-14 15:20:48        decisions: {'hold': 35}
🔴 ZERO 'close' verdicts have ever been produced.
```

| vpos | held at +4h? | verdicts | what it said at ~+4h | verdict elapsed times (h) |
|---|---|---|---|---|
| 30 | **yes** | 4 | — *(alive only from 21.5 h)* | 21.5, 22.5, 23.5, 24.5 |
| 31 | **yes** | 9 | **hold** (3.0 h) | 0, 1, 2, 3, **4**, 5, 6, 7, 7.1 |
| 32 | no (broke) | 4 | hold (3.0 h) | 1, 2, 3, 4 |
| 33 | **yes** | 15 | **hold** (3.0 h) | 0 … 14 |
| 34 | **yes** | 1 | — *(stopped out at 0.53 h)* | 0 |
| 35 | **yes** | 2 | — *(stopped out at 1.16 h)* | 0, 1 |

**Of the 19 held-level positions, the advisor was alive for five (30, 31, 33, 34, 35) and produced a ~+4h verdict on two of them (31 and 33). Both were `hold`.** vpos 31 went on to lose −1.155R; vpos 33 scratched at −0.049R.

**So the answer to 3a is no: the mechanism does not already say "close" on these.** It has never said close about anything. Flipping the dryrun flag today would change nothing, because there is nothing to promote — a gate with a 0 % firing rate is not a gate that is being held back by a flag, it is one that has never fired. (Same shape as the `WALL_AVOIDANCE_ENABLED` block that fired 0 times in 63 days.)

## 3b. 🔴 ITS PROMPT CANNOT SEE ANY OF THIS

Every one of these is **absent** from the exit prompt: `24h` · `range` · `high` · `low` · `extreme` · `pos24` · `breakout` · `support` · `resistance` · `level`.

The prompt, in full, as it was rendered at 15:20 today:

```
OPEN POSITION — decide CLOSE or HOLD.

Position
  Side: SHORT   Entry: 75.16   Now: 75.27
  Unrealised: -0.14R   (1R = the ORIGINAL stop distance, 0.8000)
  Elapsed: 1.0h
  Current stop: 75.56  ->  +0.36R away
  Peak so far (MFE): +0.18R   Giveback from peak: 0.31R

Trail
  The trailing stop is NOT ARMED — it arms only at +1R, which this
  position has not reached, so the stop above is the only protection.
  It would arm at 74.3600 (+1R).

Partial
  None taken; 1.3 open.

EVERY figure above is computed from this position's own ledger row; `Now` is the last traded
price this poll tick.
Consultation trigger: hourly review (no signal fired).

Decide whether to close the remaining size now or hold it.
```

🔴 **The advisor sees the position and nothing else.** It knows its entry, its unrealised R, its elapsed time, its stop, its peak, its giveback and its partial. It does not know what price level the entry was placed against, where in any range it sits, or what the market has done other than "Now". **It cannot form the thesis, so it cannot check it.**

**The ONE FACT that would have to be added** — stated as an answer to the question, **not proposed, and deliberately not drafted as a diff:** a single line naming the level the entry was placed against and whether it has been closed through, e.g. *"Entry thesis: SHORT placed at 0.073 of the prior 24h range (low 74.86). Since entry the 24h low has NOT been closed through."* That is one fact, already computed at entry (`lo24`/`hi24`/`pos24` exist in this report's own pipeline) and one comparison against the current price. **Whether it should be added is a separate decision, and §4 argues against it.**

## 3c. The armed exit path and the trail, on the 19 held-level positions

| vpos | R | dur_h | closed by | exit armed? | armed at h |
|---|---|---|---|---|---|
| 8 | −0.739 | 6.50 | exit_signal | yes | 2.00 |
| 9 | −0.264 | 5.91 | exit_signal | yes | 3.16 |
| 10 | −1.066 | 1.42 | sl | no | — |
| 11 | **+1.133** | 20.99 | exit_signal | yes | 6.49 |
| 12 | −1.049 | 13.20 | sl | no | — |
| 14 | −1.032 | 9.29 | sl | no | — |
| 16 | −1.146 | 5.81 | sl | no | — |
| 17 | +0.004 | 33.33 | sl | yes | 15.83 |
| 18 | −1.074 | 40.49 | sl | yes | 0.24 |
| 20 | −1.124 | 3.05 | sl | no | — |
| 21 | +0.285 | 19.03 | **trail** | no | — |
| 23 | −0.577 | 4.16 | exit_signal | yes | 0.91 |
| 24 | −1.050 | 15.97 | sl | no | — |
| 26 | −1.085 | 25.66 | sl | no | — |
| 30 | **+0.762** | 25.45 | **trail** | yes | 10.83 |
| 31 | −1.155 | 7.19 | sl | no | — |
| 33 | −0.049 | 15.00 | exit_signal | yes | 15.00 |
| 34 | −0.643 | 0.53 | sl | no | — |
| 35 | −0.701 | 1.16 | sl | no | — |

```
of the 19 HELD-at-4h : exit ARMED on 8 · closed by SL 12 · exit_signal 5 · trail 2
of the 15 HELD-at-4h LOSERS : SL 11 · exit_signal 4 · trail 0 · other 0
```

🔴 **Not one held-level loser was closed by the trail** — the trail arms at +1R and none of them ever reached +1R. **Eleven of fifteen went to the stop.** The exit-signal path armed on 8 of the 19 and only three of those armings landed inside the first four hours (vpos 18 at 0.24 h, 23 at 0.91 h, 8 at 2.00 h). **The existing exit machinery has essentially no presence in the four-hour window** — for a held-level loser, the stop is the only thing that ever acts.

---

# 4. VERDICT

## 4a. Which branch of the brief applies: **the second. It dies as candidate twenty-six.**

The brief's own conditions for a live proposal were: beats the actual book on **both sides**, **monotone** across the sweep, **surviving de-confounding**, with ≥8 positions changed. Scored honestly:

| condition | result |
|---|---|
| beats the book on **both sides** | ❌ **SHORT −1.047R** at +4h; positive on longs only |
| **monotone** across the sweep | ❌ **oscillates**; 2h is negative, the maximum is 3h |
| survives **de-confounding** | ❌ p = 0.4379 paired, **0.4413 day-clustered** |
| ≥ **8 positions changed** | ✅ 15 changed |
| *(implicit)* works in the **live** era | ❌ **negative at every horizon tested** |

**One of five.** It works only on longs, only in paper, at a non-monotone optimum, at p = 0.44. **Nothing is proposed and nothing is applied.**

🔴 **And the sharpest reason to disbelieve it is not any p-value — it is that the rule and the edge are on opposite sides.** §2c found the four-hour selection effect on **shorts** (2.21× more low-breaks than chance, 2.92× at one hour). This rule's entire benefit is on **longs**, where §2c measured 1.46× and 1.89×, neither distinguishable from chance. **A rule that pays off on the side with no measured edge, and loses on the side with one, is not the edge being harvested. It is the sample.**

## 4b. Not applicable — the precondition failed. For the record, here is what it would have been

Stated as a description, **not a proposal**, so the shape is inspectable rather than taken on trust:

```
RULE       at T+4h, if the 24h extreme the entry was placed against has not been closed
           through in the trade's favour, close at market
POPULATION 15 of 29 positions (5 had already closed; 9 had broken and are left to run)
BOOK       re-costed −7.114R  ->  −4.770R          (+2.344R, all of it paper-era longs)
COST       harms 5 positions for −3.444R, including the two largest deltas in the replay
           (vpos 11 −1.365R, vpos 30 −1.336R); helps 10 for +5.788R
VOLUME     changes no entry; it shortens 15 of 29 holds. Median hold 9.91h -> capped at 4h
           for the 15. No entry is refused, so entries/day is unchanged at 1.02
LIVE       −0.529R on the 7 live positions, and negative at every horizon from 1h to 24h
```

## 4c. 🔴 IS THE FOUR-HOUR EDGE SPENDABLE AT ALL? **NO. IT IS REAL AND IT IS SMALLER THAN THE COST OF HARVESTING IT.**

This is the question the pass exists to answer, so here it is with the arithmetic in the open. Cash every position at +4h and charge the round trip:

| cohort | n | mean **gross** R at +4h | mean fee R | **NET R if cashed at 4h** |
|---|---|---|---|---|
| ALL 29 | 29 | −0.033 | 0.120 | **−0.153** |
| **SHORT — the side the edge was found on** | 16 | **−0.050** | 0.116 | **−0.167** |
| LONG | 13 | −0.012 | 0.124 | −0.136 |
| SHORT that BROKE the low by +4h | 7 | +0.592 | 0.129 | +0.463 |
| SHORT that HELD at +4h | 9 | **−0.550** | 0.107 | −0.657 |
| live era | 7 | −0.072 | 0.155 | −0.227 |

**Gross R per side at every horizon, net of the round trip:**

| horizon | SHORT gross | SHORT net | LONG gross | LONG net |
|---|---|---|---|---|
| +1h | −0.059 | **−0.176** | −0.071 | **−0.195** |
| **+4h** | **−0.050** | **−0.167** | −0.012 | **−0.136** |
| +12h | −0.280 | −0.392 | −0.017 | −0.141 |
| at close | −0.092 | −0.208 | −0.161 | −0.285 |

🔴 **Every cell is negative.** There is no horizon at which the average trade on either side is gross-positive, let alone net-positive. **The four-hour mark is the least-bad moment in the life of a SOL trade — and it is still −0.050R gross on shorts before a 0.116R round trip.**

**So the two statements in §2c are both true and they do not combine:**

> **The selection edge exists in COUNTS.** The bot's bottom-third shorts break the 24 h low 43.8 % of the time at +4h against a 19.8 % base rate — a genuine 2.21×, and it is not an artefact.
>
> **It does not exist in R.** The seven that break earn +0.592R at +4h; the nine that do not lose −0.550R. **Nine beats seven.** The selectivity buys a better-than-chance *frequency* of being right, and the loss asymmetry gives it all back — the average short is negative at four hours, at one hour, at twelve hours and at close.

**The honest one-line answer: the entry does buy a four-hour edge, and the exit is not what spends it. The edge is spent by the 9-versus-7 arithmetic before any exit rule gets a vote, and the 0.120R round-trip taker then puts the result out of reach of anything an exit could recover.** For a four-hour harvest to be worth taking, the mean gross R at +4h would have to exceed 0.120R; on shorts it is −0.050R. **The gap is 0.17R per trade, which is not a tuning problem.**

**What this pass does establish, and it is not nothing:**

- **The exit machinery is absent exactly where the R is lost.** Held-level losers average −0.326R by +4h and −0.475R at close; 11 of 15 die on the stop; the trail never armed on a single one (it needs +1R and none got there); the exit advisor has said `hold` 35 times out of 35 and cannot see the thesis it would need to check.
- **Winners peak at +4h (+0.522R), sag to +0.091R by +12h, and are re-made by the exit to +0.546R.** That round trip through the middle of a trade's life is a real, measured property of the current geometry and it has nothing to do with entries.
- **Neither observation is a filter, and neither is proposed here.** They are the first evidence in this book that exit geometry has measurable structure, after twenty-six entry-side candidates that did not.

---

## STATE — nothing was changed by this pass

```
mercury-sol   active · master 2162333 / worker 2162408 · since 2026-08-14 18:28:16 · NRestarts=0
              NOT restarted by this pass.
BOOK          29 closed · booked ΣR −5.985 (re-costed at the real taker: −7.114) · FLAT
              active_positions EMPTY · max vpos 35
FILES         mercury-sol: ZERO .py modified since 18:30. No DB write. No order. No restart.
CANDIDATES    26 measured on this book, 26 dead. #25 placement (19:00), #26 the +4h exit rule.
titan         /root/titan-bot — NOT touched, NOT read for state, NO numbers imported.
              HEAD 897850b · working tree clean
```

**Provenance: SOL's own `trades.db` opened `mode=ro`; the 19:00 report's own `pos24`/`lo24`/`hi24` and break/held split, re-used rather than re-derived; Bybit SOLUSDT-perp 5m candles fetched through the bot's own venue over Tor. `market_regime` was not used. Titan was not read.**
