# Mercury-SOL — the payoff ratio is the defect, the breakeven lock arms too late, and the moves are not there

**2026-08-14 19:30 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · READ-ONLY THROUGHOUT — no file written, no restart, no order, no DB write. Nothing proposed before §4, and nothing applied at all.**

Titan (`/root/titan-bot`): **not touched, not read for state, no numbers imported.** HEAD `897850b`, clean.

Premise: [19:15 §4c](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-14-1915-sol-the-four-hour-edge-is-real-and-it-is-smaller-than-the-cost-of-harvesting-it.md).

---

## ⚡ THE SHORT VERSION

1. **The arithmetic in the brief is confirmed, and it is worse re-costed.** Win rate **34.5 %**, mean winner **+0.934R**, mean loser **−0.804R**, payoff **1.16 : 1**. Break-even at 34.5 % needs **1.90 : 1**. 🔴 **The mean winner must be +0.593R bigger — 63 % larger — for the book to be flat.**
2. **🔴 THE +1R LINE SEPARATES THE BOOK PERFECTLY.** Nine positions ever reached +1R gross; **all nine won** (ΣR +8.362). The other twenty never armed anything: **ΣR −14.347, one winner** (vpos 19, MFE 0.993R — a whisker short). **No loser in the book ever reached +1.0R.**
3. **The trail is not a decoration — it is starved.** It has closed 5 positions, all winners, +3.781R. But it arms at +1R and **only 31 % of the book gets there.** Meanwhile **14 of 29 died on the stop for −12.845R.**
4. **Winners capture 47 % of their own peak.** Mean MFE +1.869R → mean realised +0.883R: **0.986R given back per winner**, and the winner spends **54 % of its life past its peak**.
5. **🔴 17 of 19 losers were green at some point; 8 reached ≥ +0.5R and still lost.** Only 2 were never green. That is where the geometry's money is — not in bigger targets.
6. **The one axis with a robust direction is the BREAKEVEN LOCK's arm level, and its level is still a fitted maximum.** Every arm cell below 0.90R beats every cell at or above 1.00R (6 cells vs 4, no overlap). But the fine sweep is **non-monotone**, and the best cell (0.5R, Δ +5.377R) is a **spike carried by six positions whose peaks cluster at 0.51–0.57R**. Move it 0.1R either way and 2.5R of the gain evaporates. **The direction is real. The level is fitted.**
7. **🔴 AND THE HEADLINE ANSWER: THE MOVES ARE NOT THERE.** A fixed target is non-monotone and worth at most **+0.546R** at 2.5R — a level **2 of 29 positions have ever touched, and 0 of 7 live ones.** To reach break-even the average winner needs 1.53R; **only 6 of 29 positions ever touched 1.50R at all.** There is no target policy that pays for itself, because the excursions do not exist.
8. **Position sizing cannot help. Kelly is negative on every cohort** (book f\* = **−0.219**), which means the size-optimal bet is **zero**. Sizing is a multiplier on −0.2045R per trade; it changes the rate, never the sign.

---

## 0. METHOD, AND THE ONE THING THAT MAKES IT COMPARABLE

🔴 **1R IS HELD FIXED THROUGHOUT.** `SL_BUFFER_ATR = 2.5` is never swept, so 1R = `2.5 × ATR(1h)` at entry stays exactly what it is today for every position and every variant. Every number below is denominated in **that** R. No variant re-denominates the unit, which is why the columns can be compared at all.

| item | value |
|---|---|
| replay resolution | Bybit SOLUSDT-perp **5m** candles via Tor, 35,074 bars |
| intrabar order | 🔴 **adverse extreme assumed touched FIRST** — a stop always wins a tie against a target in the same bar |
| taker | **0.001 on every leg**, including the partial's extra leg |
| funding | recorded `funding_paid` scaled by 8h stamps (00/08/16 UTC) crossed |
| signal exits | left in place: if no geometry rule fires, the position exits at its **actual** close |
| current geometry | stop 1R · arm +1R · BE lock on arm (entry ± round-trip + 0.05 %) · partial ⅓ at arm · trail 0.75R |

### The engine reproduces the book before it is asked to change it

| | |
|---|---|
| mean Δ (replay − booked) | **+0.002R** |
| median Δ | −0.019R |
| within ±0.15R | **23 of 29** |
| ΣR | replay **−5.930** vs booked **−5.985** |

The six that differ by more than 0.15R (vpos 7, 11, 15, 17, 25, 29) are positions whose live exit was an `exit_signal` or a 10-second-poller trail that a 5m grid times differently; they cancel to roughly zero. 🔴 **Every variant below runs through the same engine, so this residual error largely cancels in the DIFFERENCES. Absolute levels carry it; deltas mostly do not.** That is stated because it is the load-bearing assumption of §3.

---

# 1. THE PAYOFF, DECOMPOSED

## 1a. At the re-costed 0.001 taker

| cohort | n | win % | mean winner | mean loser | **payoff** | expectancy | ΣR |
|---|---|---|---|---|---|---|---|
| ALL 29 *(booked)* | 29 | 34.5 % | +0.883 | −0.779 | 1.13 | −0.206 | −5.985 |
| **ALL 29 (re-costed)** | 29 | **34.5 %** | **+0.934** | **−0.804** | **1.16** | **−0.204** | **−5.930** |
| SHORT | 16 | 37.5 % | +0.868 | −0.744 | 1.17 | −0.140 | −2.235 |
| LONG | 13 | 30.8 % | +1.034 | −0.870 | 1.19 | −0.284 | −3.695 |
| paper (22) | 22 | 36.4 % | +0.926 | −0.897 | 1.03 | −0.234 | −5.150 |
| live (7) | 7 | 28.6 % | +0.969 | −0.544 | **1.78** | −0.111 | −0.780 |

*The live era's better payoff (1.78) is 7 trades and 2 winners. It is reported, not leaned on.*

## 1b. 🔴 THE BREAK-EVEN PAYOFF AND THE GAP — one number per cohort

Break-even payoff = `(1−p)/p`. The gap holds the mean loser and the win rate fixed and asks how much bigger the average winner must be.

| cohort | n | win p | payoff now | **BE payoff** | mean winner now | **needed** | **GAP** |
|---|---|---|---|---|---|---|---|
| **ALL 29 (re-costed)** | 29 | 34.5 % | 1.16 | **1.90** | 0.934R | **1.527R** | **+0.593R (+63 %)** |
| SHORT | 16 | 37.5 % | 1.17 | 1.67 | 0.868R | 1.241R | **+0.373R (+43 %)** |
| LONG | 13 | 30.8 % | 1.19 | 2.25 | 1.034R | 1.957R | **+0.924R (+89 %)** |
| paper (22) | 22 | 36.4 % | 1.03 | 1.75 | 0.926R | 1.569R | +0.644R |
| live (7) | 7 | 28.6 % | 1.78 | 2.50 | 0.969R | 1.359R | +0.390R |

**Equivalently, holding the payoff fixed, the book would need a 46.2 % win rate instead of 34.5 %.**

## 1c. How each position ended

| close reason | winners | losers | total | ΣR |
|---|---|---|---|---|
| **sl** | 1 | **13** | **14** | **−12.845** |
| exit_signal | 3 | 6 | 9 | +1.724 |
| **trail** | **5** | **0** | 5 | **+3.781** |
| exchange_UNKNOWN | 1 | 0 | 1 | +1.355 |

🔴 **The trail is 5 for 5 and has never closed a loser. The stop is 1 for 14.** Half the book dies on the stop and that single line is −12.845R against a book of −5.985R.

## 1d. 🔴 DID THEY EVER REACH +1R? — the trail's arm level

| threshold | reached | SHORT | LONG | vpos |
|---|---|---|---|---|
| MFE ≥ 0.50R | 18 / 29 (62 %) | 10/16 | 8/13 | 7,11,12,13,15,17,18,19,21,23,25,26,27,28,29,30,32,33 |
| MFE ≥ 0.75R | 13 / 29 (45 %) | 6/16 | 7/13 | 7,11,13,15,17,18,19,21,25,26,29,30,33 |
| **MFE ≥ 1.00R** | **9 / 29 (31 %)** | 5/16 | 4/13 | **7,11,13,15,17,21,25,29,30** |
| MFE ≥ 1.50R | 6 / 29 (21 %) | 3/16 | 3/13 | 7,11,13,25,29,30 |
| MFE ≥ 2.00R | 4 / 29 (14 %) | 2/16 | 2/13 | 7,13,25,29 |
| MFE ≥ 2.50R | **2 / 29 (7 %)** | 1/16 | 1/13 | 7,25 |

```
the 9 that reached +1R :  9 winners, 0 losers,  ΣR  +8.362
the 20 that did not    :  1 winner, 19 losers,  ΣR −14.347
```

🔴 **The +1R line separates the book without a single exception on the loser side.** Not one of the 19 losers ever touched +1.0R; the closest was vpos 18 at 0.911R. The one winner that never armed is vpos 19, whose peak was **0.993R** — three thousandths of an R short.

**So the answer to the brief's question is: the trail is not a decoration, but it is starved.** It never fires on a loser because a loser never gets near it, and it fires on 5 of the 9 that do. **The problem is not that the trail is wrong. It is that the arming condition sits above 69 % of the book's entire excursion distribution.**

---

# 2. THE PEAK, AND WHAT IS GIVEN BACK

## 2a. MFE / MAE in R for every position (5m resolution)

| vpos | side | **MFE R** | at h | MAE R | realised | captured | reason |
|---|---|---|---|---|---|---|---|
| 7 | LONG | **3.024** | 16.66 | −0.196 | +2.089 | 69 % | exit_signal |
| 8 | LONG | 0.006 | 4.83 | −0.769 | −0.739 | — | exit_signal |
| 9 | LONG | 0.325 | 0.50 | −0.380 | −0.264 | — | exit_signal |
| 10 | SHORT | 0.006 | 0.07 | −1.431 | −1.066 | — | sl |
| 11 | SHORT | 1.779 | 7.83 | −0.305 | +1.133 | 64 % | exit_signal |
| 12 | LONG | 0.561 | 9.33 | −1.058 | −1.049 | — | sl |
| 13 | SHORT | 2.363 | 4.33 | −0.482 | +1.337 | 57 % | trail |
| 14 | SHORT | **−0.075** | 0.08 | −1.027 | −1.032 | — | sl |
| 15 | SHORT | 1.190 | 10.33 | −0.118 | +0.140 | **12 %** | trail |
| 16 | LONG | 0.193 | 1.91 | −1.141 | −1.146 | — | sl |
| 17 | SHORT | 1.247 | 18.41 | −0.627 | +0.004 | **0 %** | sl |
| 18 | LONG | 0.911 | 21.58 | −1.053 | −1.074 | — | sl |
| 19 | SHORT | 0.993 | 7.83 | −0.378 | +0.463 | 47 % | exit_signal |
| 20 | SHORT | 0.174 | 0.07 | −1.072 | −1.124 | — | sl |
| 21 | LONG | 1.489 | 18.33 | −0.822 | +0.285 | **19 %** | trail |
| 22 | LONG | 0.300 | 3.41 | −1.107 | −1.064 | — | sl |
| 23 | SHORT | 0.568 | 2.66 | −0.610 | −0.577 | — | exit_signal |
| 24 | SHORT | 0.265 | 0.99 | −1.006 | −1.050 | — | sl |
| 25 | SHORT | **2.658** | 1.49 | +0.055 | +1.257 | 47 % | trail |
| 26 | LONG | 0.830 | 16.74 | −1.085 | −1.085 | — | sl |
| 27 | SHORT | 0.649 | 1.74 | −0.585 | −0.660 | — | sl |
| 28 | SHORT | 0.510 | 4.41 | −0.194 | −0.153 | — | exit_signal |
| 29 | LONG | 2.198 | 6.41 | −0.077 | +1.355 | 62 % | exchange_UNKNOWN |
| 30 | LONG | 1.750 | 24.99 | −0.659 | +0.762 | 44 % | trail |
| 31 | LONG | 0.143 | 0.24 | −1.086 | −1.155 | — | sl |
| 32 | SHORT | 0.553 | 1.07 | −0.070 | −0.180 | — | exit_signal |
| 33 | LONG | 0.813 | 14.49 | −0.551 | −0.049 | — | exit_signal |
| 34 | SHORT | **−0.037** | 0.08 | −0.514 | −0.643 | — | sl |
| 35 | SHORT | 0.113 | 0.08 | −0.512 | −0.701 | — | sl |

## 2b. WINNERS — the exit keeps 47 % of the peak

```
n = 10        mean MFE +1.869R        mean realised +0.883R        CAPTURE 47.2 %
              given back 0.986R per winner      median capture 47.0 %
              worst 0 % (vpos 17: peaked +1.247R, closed +0.004R)   best 69 % (vpos 7)
peak arrives at a median 9.08h into a median 19.55h hold
  -> 🔴 the average winner spends 54 % of its life past its own peak
```

**That is the round trip the 19:15 report described (+0.522R at 4h → +0.091R at 12h → +0.546R at close), quantified per position: it costs 0.986R per winner.** Ten winners × 0.986R ≈ **9.9R** — against a book that is 5.9R short of flat.

## 2c. LOSERS — 17 of 19 were green

| threshold | losers that reached it |
|---|---|
| MFE > 0.00R | **17 of 19** |
| MFE > 0.25R | 11 of 19 |
| MFE > 0.50R | **8 of 19** — vpos 12, 18, 23, 26, 27, 28, 32, 33 |
| MFE > 0.75R | 3 of 19 |
| **MFE > 1.00R** | **0 of 19** |

```
NEVER GREEN AT ALL          : 2 of 19  (vpos 14, 34)  ΣR −1.676
WENT >= +0.5R AND STILL LOST: 8 of 19  peaks summing +5.395R, realised −4.826R
losers' mean MFE +0.358R, mean MAE −0.803R   |   winners' mean MAE −0.361R
```

🔴 **A loser that touched +0.5R and finished at −0.7R is a geometry failure. A loser that was never green is not.** There are eight of the first kind and two of the second. **Every single one of the eight peaked below the +1R arm**, so nothing in the current machinery was ever switched on for them.

## 2d. The aggregate — stated carefully, because the naive number lies

```
total MFE across the book        +25.609R
total realised (booked)           −5.985R
difference                       +31.594R
   of which the WINNERS' own give-back is  +9.864R
   the loser cohort's own peaks total       +6.919R  (they realised −14.811R)
```

🔴 **The +31.594R figure is an UPPER BOUND, not a target, and it must not be quoted as money the geometry left behind.** It is the sum of moments that were only identifiable afterwards; harvesting them requires knowing each peak in advance. **The honest, actionable number is the winners' give-back: 9.864R, and the eight green-then-red losers' 5.395R of peaks.**

---

# 3. THE SWEEPS

Baseline = today's geometry through the same engine: **ΣR −5.930**.

## 3a. Trail ARM level — the only axis with a robust direction, and its level is still fitted

| arm | ΣR | Δ | SHORT | LONG | paper | live | win % | mean W | mean L |
|---|---|---|---|---|---|---|---|---|---|
| 0.25R | −2.761 | +3.169 | −1.148 | −1.613 | −1.307 | −1.454 | 72.4 % | 0.232 | −0.954 |
| 0.40R | −3.780 | +2.150 | −1.540 | −2.240 | −3.048 | −0.732 | 62.1 % | 0.353 | −0.921 |
| **0.50R** | **−1.510** | **+4.420** | −0.980 | −0.530 | −0.911 | −0.599 | 62.1 % | 0.479 | −0.921 |
| 0.60R | −3.509 | +2.421 | −1.972 | −1.537 | −2.679 | −0.830 | 48.3 % | 0.624 | −0.817 |
| 0.75R | −3.602 | +2.328 | −2.576 | −1.027 | −2.922 | −0.680 | 44.8 % | 0.721 | −0.811 |
| 0.90R | −4.697 | +1.233 | −2.275 | −2.422 | −3.851 | −0.847 | 37.9 % | 0.862 | −0.788 |
| **1.00R (now)** | **−5.930** | 0.000 | −2.235 | −3.695 | −5.150 | −0.780 | 34.5 % | 0.934 | −0.804 |
| 1.25R | −6.172 | −0.242 | −3.032 | −3.140 | −5.559 | −0.614 | 31.0 % | 1.016 | −0.766 |
| 1.50R | −6.203 | −0.273 | −2.782 | −3.421 | −5.756 | −0.447 | 31.0 % | 1.012 | −0.766 |
| 2.00R | −5.818 | +0.113 | −2.461 | −3.357 | −5.268 | −0.549 | 31.0 % | 1.055 | −0.766 |

**🔴 THE DIRECTION IS ROBUST: every cell below 0.90R beats every cell at or above 1.00R.** Six cells against four, ranges `[−4.697, −1.510]` vs `[−6.203, −5.818]` — **no overlap at all.**

**🔴 THE LEVEL IS NOT.** The surface is non-monotone (2 up, 7 down across ten cells), and the 0.50R cell is a **spike**: its neighbours at 0.40R and 0.60R are 2.27R and 2.00R worse. Six positions carry it — and here is why:

```
vpos  12  MFE 0.561R      vpos  23  MFE 0.568R
vpos  28  MFE 0.510R      vpos  32  MFE 0.553R
```

**Four of the six carriers have peaks between 0.510R and 0.568R.** An arm at 0.50R sits just underneath that cluster and converts them from full stops into breakeven scratches; an arm at 0.60R sits just above it and they revert. **That is not a level, it is a fence built around four data points**, and it is the same failure mode as the ADX grid's turn and the +4h sweep's 3h spike.

### What is actually doing the work — decomposed

| variant | ΣR | Δ |
|---|---|---|
| today: arm 1.0R, BE on, partial ⅓, trail 0.75R | −5.930 | 0.000 |
| arm 0.5R, everything else unchanged | −1.510 | **+4.420** |
| arm 0.5R, **BE lock OFF** | −3.102 | +2.828 |
| arm 0.5R, **partial OFF** | **−0.553** | **+5.377** |
| arm 0.5R, **trail OFF** (BE + partial only) | −2.232 | +3.698 |
| **BE lock alone at 0.5R** (no trail, no partial) | **−1.637** | **+4.293** |
| arm 1.0R, BE lock OFF | −5.930 | 0.000 |

🔴 **The breakeven lock alone at 0.5R delivers +4.293R of the +4.420R.** It is not the trail and it is not the partial. **The mechanism is exactly §2c: seventeen of nineteen losers were green, eight reached +0.5R, and the stop was still a full 1R away when they turned.** That the mechanism is *interpretable* is worth more than the p-value — but it does not rescue the level.

## 3b. Trail WIDTH at the current +1R arm — non-monotone, and today sits on the peak

| width | 0.25R | 0.50R | **0.75R (now)** | 1.00R | 1.50R |
|---|---|---|---|---|---|
| ΣR | −6.845 | −6.305 | **−5.930** | −6.799 | −6.918 |
| Δ | −0.915 | −0.375 | **0.000** | −0.868 | −0.988 |

**Rises then falls; the current setting is the maximum of the curve.** Nothing to take here — and a setting that happens to sit on the peak of a noisy surface is not evidence the setting is right, only that it cannot be improved on this book.

## 3c. 🔴 A FIXED TARGET — non-monotone, tiny, and the levels are not reached

| target | none | 1.0R | 1.5R | **2.0R** | **2.5R** | 3.0R |
|---|---|---|---|---|---|---|
| ΣR | −5.930 | −6.998 | −6.111 | −5.425 | **−5.384** | −5.447 |
| Δ | 0.000 | −1.068 | −0.181 | +0.505 | **+0.546** | +0.484 |

**And how often is each level actually touched?**

| target | reached | SHORT | LONG | **live** |
|---|---|---|---|---|
| 1.0R | 9 / 29 (31 %) | 5/16 | 4/13 | 2/7 |
| 1.5R | 6 / 29 (21 %) | 3/16 | 3/13 | 2/7 |
| 2.0R | 4 / 29 (14 %) | 2/16 | 2/13 | 1/7 |
| **2.5R** | **2 / 29 (7 %)** | 1/16 | 1/13 | **0/7** |
| 3.0R | 1 / 29 (3 %) | 0/16 | 1/13 | **0/7** |

🔴 **The best target cell is worth +0.546R and sits at a level two positions in the book's entire history have ever reached — neither of them live.** The curve rises to 2.5R and falls at 3.0R because there is nothing above 2.5R to catch. **This is the direct test the brief asked for, and it comes back negative: a bigger payoff is not available at this win rate, because the excursions that would pay for it do not exist.**

## 3d. The partial — the one MONOTONE axis, and it says take less

| partial | none | ¼ | **⅓ (now)** | ½ | full (= a 1R target) |
|---|---|---|---|---|---|
| ΣR | **−5.393** | −5.796 | −5.930 | −6.199 | −7.005 |
| Δ | **+0.538** | +0.134 | 0.000 | −0.269 | −1.075 |

**Monotone decreasing in the fraction taken.** Every step toward taking more is worse, and taking none is best. **The partial has fired 3 times in 29 positions in reality** (vpos 25, 29, 30) — because it fires at the +1R arm, which 69 % of the book never reaches. Its extra exit leg costs about **0.031R** per position that takes it.

## 3e. Costs, charged

Taker 0.001 on the entry leg, on every exit leg, and on the partial's extra leg. Across the nine positions that take a partial in the replay, exit-leg fees total **0.5637R**. Funding is scaled by stamps crossed and totals **0.045 USDT** across the live book — 0.51 % of live risk, stated so it is not assumed to be doing work it is not doing.

## 3f. 🔴 MONOTONICITY, per axis, stated plainly

| axis | shape | best cell | values |
|---|---|---|---|
| trail **ARM** level | **NON-MONOTONE** (2 up, 7 down) | 0.50R | −2.761, −3.780, **−1.510**, −3.509, −3.602, −4.697, −5.930, −6.172, −6.203, −5.818 |
| trail **WIDTH** | **NON-MONOTONE** (2 up, 2 down) | 0.75R *(= today)* | −6.845, −6.305, **−5.930**, −6.799, −6.918 |
| fixed **TARGET** | **NON-MONOTONE** (3 up, 1 down) | 2.5R | −6.998, −6.111, −5.425, **−5.384**, −5.447 |
| **PARTIAL** fraction | **MONOTONE** | 0.0 | **−5.393**, −5.796, −5.930, −6.199, −7.005 |

**One axis of four is monotone, and it is the one with the smallest effect (+0.538R).**

---

# 4. VERDICT

## 4a. The best candidate, scored against the brief's own conditions

**Candidate: arm the breakeven lock at +0.5R instead of +1R, and drop the partial.** Δ **+5.377R** (−5.930 → −0.553).

| condition | result |
|---|---|
| beats the current geometry on **both sides** | ✅ SHORT +1.701 (7/9 positive), LONG +3.676 (6/7) |
| **monotone** on its axis | ❌ **NO — 2 up, 7 down; the best cell is a spike** |
| survives day / hour / era **de-confounding** | ⚠️ paired sign-flip **p = 0.0213**, day-clustered **p = 0.0277**; paper +4.932, **live +0.445 (3/3 positive)**, halves +1.745 / +3.631, all four hour-buckets positive |
| ≥ **8 positions changed** | ✅ **16 of 29** |

**Three of four. It fails on the one that has killed every previous candidate.**

🔴 **And the multiplicity is the selection, not the two p-values I quote.** This candidate is the maximum of a scan over four axes and ~25 cells. Against **α = 0.05/25 = 0.002** the day-clustered p = 0.0277 fails by 14×; even the lenient framing of four axis-families (α = 0.0125) fails it. **Nothing is proposed and nothing is applied.**

**What survives the level being fitted — stated separately, because it is a different claim:**

> **The DIRECTION is not a fitted maximum.** All six arm cells below 0.90R beat all four at or above 1.00R, with no overlap in their ranges. The mechanism is measured and interpretable: **17 of 19 losers went green, 8 reached +0.5R, and the stop stayed a full 1R away because the arming condition sits above 69 % of the book's excursion distribution.** The breakeven lock alone at 0.5R carries +4.293R of the +4.420R — it is not the trail, and it is not the partial.
>
> **What is NOT established is any specific level**, and the honest reason is visible in the data: four of the six positions that carry the 0.5R spike have peaks between 0.510R and 0.568R. **A rule tuned to sit under that cluster is fitted to four trades.**

**One methodological caveat that cuts against the candidate, recorded rather than buried:** within a single 5m bar the engine checks the adverse extreme against the *old* stop and only then arms the lock. A live 10-second poller could arm and be stopped at breakeven inside the same bar. **The 5m grid is therefore mildly optimistic about an earlier lock**, and the effect is largest exactly where the candidate gains — the eight green-then-red losers.

## 4b. 🔴 THE MOVES ARE NOT THERE. Said without softening.

The brief asked for this to be stated plainly if it were true, and it is true.

```
to break even the average winner must be        1.527R      (it is 0.934R)
positions that ever touched 1.50R at all             6 of 29  (21%)   live:  2 of 7
positions that ever touched 2.00R at all             4 of 29  (14%)   live:  1 of 7
positions that ever touched 2.50R at all             2 of 29  ( 7%)   live:  0 of 7
best fixed-target cell in the whole sweep       +0.546R at 2.5R — a level 2 positions have reached
```

**SOL's average move after one of this bot's signals is too small to support a 1R stop at a 34.5 % win rate.** The excursion distribution is the binding constraint: the book needs winners averaging 1.53R and only a fifth of its positions have ever *touched* 1.50R, most of them in the paper era. **No target policy, no trail width and no arm level can manufacture an excursion that did not happen.** The 47 % capture rate on winners is a real inefficiency worth 9.9R — but even a perfect capture of every winner's peak leaves the eight green-then-red losers and the two never-green ones untouched, and the arithmetic still needs the peaks to be there.

**This is the finding that ends this line of work.** Twenty-six entry-side candidates died on selection; the geometry sweep now returns one monotone axis worth +0.538R and one interpretable direction whose level cannot be identified on 29 trades. **The instrument, not the logic, is the binding constraint** — and that is a statement about SOL at this signal set and this stop width, not a statement that the code is wrong.

## 4c. What this implies for POSITION SIZING

| cohort | n | p | payoff b | expectancy | **Kelly f\*** | needs payoff | or win rate |
|---|---|---|---|---|---|---|---|
| whole book | 29 | 34.5 % | 1.16 | −0.204R | **−0.219** | 1.90 | 46.2 % |
| SHORT | 16 | 37.5 % | 1.17 | −0.140R | **−0.161** | 1.67 | 46.2 % |
| LONG | 13 | 30.8 % | 1.19 | −0.284R | **−0.275** | 2.25 | 45.7 % |
| live (7) | 7 | 28.6 % | 1.78 | −0.111R | **−0.115** | 2.50 | 35.9 % |

🔴 **Kelly is negative on every cohort, which means the size-optimal bet is ZERO.** That is not rhetoric, it is what `f* = (p·b − q)/b` returns when `p·b < q`.

**So the honest answer on sizing is the uncomfortable one: sizing is a multiplier on −0.2045R per trade.** At the live rate of 1.02 entries/day that is **−0.209R/day, −6.3R/month**. Doubling risk-per-trade doubles that; halving it halves it; **nothing about sizing changes the sign.** The only sizing decisions that are defensible while expectancy is negative are the ones that reduce exposure — and the smallest of those is the one the bot is already at (`LIVE_FIXED_MARGIN` 20 × leverage 5 = $100 notional).

**And the honest counterweight, because seven trades deserve it:** the live era is **n = 7, mean −0.111R, sd 0.826, standard error 0.312R.** A 95 % interval on the live mean is **[−0.724, +0.501]R** — it contains zero and most of the plausible range in both directions. **Seven trades cannot tell a −0.11R/trade edge from a +0.4R one.** Everything above is measured on a book that is 76 % paper, and the live sub-book is too small to confirm or refute any of it. **That is the sample the whole series has been arguing with, and it has not changed.**

---

## STATE — nothing was changed by this pass

```
mercury-sol   active · master 2162333 / worker 2162408 · since 2026-08-14 18:28:16 · NRestarts=0
              NOT restarted by this pass.
BOOK          29 closed · booked ΣR −5.985 (re-costed at the real taker: −5.930 through the
              replay engine, −7.114 by the 19:15 direct method) · FLAT · max vpos 35
FILES         mercury-sol: ZERO .py modified since 18:30. No DB write. No order. No restart.
GEOMETRY      unchanged: SL_BUFFER_ATR 2.5 · arm +1R · BE lock on arm · partial 1/3 · trail 0.75R
CANDIDATES    26 entry-side (all dead) + this geometry pass: 1 monotone axis worth +0.538R,
              1 robust direction with no identifiable level. NOTHING PROPOSED.
titan         /root/titan-bot — NOT touched, NOT read for state, NO numbers imported.
              HEAD 897850b · working tree clean
```

**Provenance: SOL's own `trades.db` opened `mode=ro`; Bybit SOLUSDT-perp 5m candles through the bot's own venue over Tor; the replay engine validated against the booked book at mean Δ +0.002R before any variant was run. Titan was not read.**
