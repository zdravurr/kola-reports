# Titan — **THE RULE DOES NOT FIRE. 5 RESOLVED of 10, Σ +1.0497R / +$1.72 — POSITIVE.** Two outstanding counterfactuals resolved: vpos 106 **+0.7640R for the advisor**, vpos 108 **−0.4576R against it**. 🔴 And the newest data implicates **the ENTRY, not the exit**: 11 of the 17 live losers never printed +0.25R and carry **77 % of all live losses**.

**2026-09-16 15:20 UTC · commit `f16c271` · Titan LIVE REAL MONEY · READ-ONLY PASS · Mercury-SOL NOT TOUCHED**

---

## 🔴 THE DECISION, FIRST LINE, BEFORE ANY OPINION

`§0.EXIT-ADVISOR-RULE` decides at **10 RESOLVED closes**. The ledger stands at **5 RESOLVED of 10** and
its sum is **+1.0497R / +$1.72 — POSITIVE, IN THE ADVISOR'S FAVOUR.**

> ### ⛔ THE RULE HAS **NOT** REACHED 10 AND THE SUM IS **NOT** NEGATIVE.
> ### **DO NOT FLIP `EXIT_ADVISOR_DRYRUN`.** It stays **False**. Five resolved closes remain.
> At the measured rate — **3.24 days per `ai_exit` close** on an interval basis, 2.97 on a wall-clock
> basis — five more is **≈ 15–16 days, i.e. the first days of October 2026**, plus each counterfactual's
> own resolution lag (measured: 1.0 h, 6.7 h, 15.2 h, 48.6 h, 4.0 h; **median 6.7 h**).

The operator reports "early exits taking losses." **The ledger does not support that reading, and §3 says
why: the exit is not where the money goes.** Both new resolutions moved the sum, in opposite directions,
and the one that moved it most was **the advisor being RIGHT** — vpos 106, where holding would have cost
a further **−1.87 dollars**.

---

# 1. THE EXIT ADVISOR

## 1a. EVERY LIVE `ai_exit` CLOSE FROM vpos 101 ONWARD

| vpos | side | entry | exit | R | net $ | hold | trigger | trail ARMED at close? |
|---|---|---|---|---|---|---|---|---|
| 101 | SHORT | 77 661.0 | 77 282.2 | **+0.2956** | +0.57 | 1.75 h | **15m** `Bearish I-CHOCH` | ❌ no |
| 104 | LONG | 79 112.4 | 79 637.7 | **+0.5757** | +0.79 | 3.75 h | **15m** `Bullish I-BOS` | ❌ no |
| 105 | SHORT | 78 263.2 | 78 199.0 | **−0.0136** | −0.03 | 4.01 h | **periodic** (hourly) | ❌ no |
| 106 | SHORT | 77 014.2 | 77 329.8 | **−0.2963** | −0.72 | 11.25 h | **15m** `Bullish I-BOS` | ❌ no |
| **108** | **LONG** | **77 812.0** | **78 708.9** | **+1.1371** | **+1.54** | **9.25 h** | **15m** `Bullish I-BOS` | 🔴 **YES — the first ever** |

**Two closes are new since the 2026-09-12 reports: vpos 106 and vpos 108.** (vpos 107 also closed in the
window — on its **stop**, not by the advisor; it is not in this population.)

🔴 **THE TRIGGER PATTERN IS NOW LOPSIDED AND WORTH STATING.** Across every exit consultation since
2026-09-01: the **periodic hourly review returned `hold` 36 times and `close` ONCE**. **Five of the six
closes were fired by a 15m structure print**, and **three of those five by the same signal, `Bullish
I-BOS`**. Each triggered close reversed a `hold` taken minutes earlier — 44.6, 44.5, 13.4 and 13.9 minutes.
This is a description of 6 closes, not a finding; the 2026-09-12 17:15 report already established that
group sizes of 2 and 1 cannot rank anything, and 5-vs-1 cannot either.

🔴 **vpos 108 IS A FIRST: THE ADVISOR JUDGED A PROTECTED POSITION.** The 17:15 report of 2026-09-12 found
**0 of 33** era-C consultations and **0 of 32** canon-population consultations had ever seen an armed trail,
because no position in that population had ever come within reach of +1R (highest MFE at any decision:
+0.72R). vpos 108 armed at 78 523.1, its stop moved to breakeven 77 967.624, and **five consultations —
32609, 32612, 32613, 32624 and the closing 32630 — rendered the ARMED branch of the prompt.** The
canon-population count is no longer zero: it is **5 of 46**.

## 1b. EVERY OUTSTANDING COUNTERFACTUAL IS NOW RESOLVED. NOTHING IS LEFT RUNNING.

Replayed by the canon's own method: BingX `BTC/USDT:USDT` 1m candles in `bardir` order (rising bar → low
first, falling bar → high first), 1R off `original_sl_price`, arm at +1R, stop to breakeven
`entry × (1 ± 0.002)` on arming, trail `water_mark × (1 ∓ trail_pct/100)` tightening only, water mark seeded
from the row's value at the advisor's close, net = gross − 0.0005 × size × (entry + exit).

**71 455 candles, 2026-07-29 00:00 → 2026-09-16 14:54 UTC, ZERO GAPS** (49 days × 1440 + 894 + 1 = 71 455,
exactly the count present).

> 🔴 **THE STAND WAS VALIDATED BEFORE IT WAS TRUSTED.** It re-derived all three canon-published rows from
> scratch and reproduced them **to the digit**: 101 → trail **77 124.0** at 09-01 19:00, **+0.4509R /
> +$0.87**; 104 → sl **78 350.1** at 09-09 15:11, **−1.1033R / −$1.51**; 105 → trail **77 393.9** at
> 09-10 14:56, **+0.7669R / +$1.50**. That, and only that, licenses the two new rows.

### 🔴 vpos 106 — RESOLVED. The advisor was RIGHT, and by more than any loss it has taken.

**The original stop 78 301.6 printed on 2026-09-14 09:53 UTC** (bar high 78 317.0; the highest print before
that bar was 78 264.2, 37.4 points short). The counterfactual **never armed**: the arm price was 75 726.8
and the lowest low over the whole 48.6 h hold-out was **76 350.0** — 623 points, **0.48R**, short of it.

**Counterfactual −1.0603R / −$2.59. Advisor −0.2963R / −$0.72. Δ = +0.7640R / +$1.87 FOR the advisor.**

🔴 **AND THE CRUEL DETAIL, STATED SO NOBODY CLAIMS THE SHORT WAS RIGHT.** BTC did eventually fall — to
**74 911.6 on 2026-09-15 18:50**, well below the 75 726.8 arm. But that was **33 hours after** the original
stop had already taken the position out. **The thesis was eventually correct and the stop killed it first.**
Holding would not have been rescued by patience.

### 🔴 vpos 108 — RESOLVED. The advisor was WRONG, and this one it closed while PROTECTED.

At the close the trail was **already armed** (water mark 78 852.2, arm 78 523.1, stop at breakeven
77 967.624). Held, the water mark ran on to **79 569.5** and the trail fired at
**79 024.4 on 2026-09-14 21:01 UTC**, four hours later. The lowest low in between was 78 675.0 — the
breakeven stop was never threatened.

**Counterfactual +1.5947R / +$2.15. Advisor +1.1371R / +$1.54. Δ = −0.4576R / −$0.62 AGAINST the advisor.**

**Nothing is UNRESOLVED. Every observation in the population has a settled counterfactual.**

## 1c. 🔴 THE LEDGER

| # | vpos | side | closed (UTC) | advisor R ($) | counterfactual exit | counterfactual R ($) | **Δ R** | **Δ $** |
|---|---|---|---|---|---|---|---|---|
| 1 | 101 | SHORT | 09-01 18:00 | +0.2956 (+0.57) | **trail** 77 124.0 @ 09-01 19:00 | +0.4509 (+0.87) | **−0.1553** | −0.30 |
| 2 | 104 | LONG | 09-09 08:30 | +0.5757 (+0.79) | **sl** 78 350.1 @ 09-09 15:11 | −1.1033 (−1.51) | **+1.6791** | +2.30 |
| 3 | 105 | SHORT | 09-09 23:46 | −0.0136 (−0.03) | **trail** 77 393.9 @ 09-10 14:56 | +0.7669 (+1.50) | **−0.7805** | −1.53 |
| 4 | **106** | SHORT | 09-12 09:15 | −0.2963 (−0.72) | 🔴 **NEW — sl** 78 301.6 @ 09-14 09:53 | −1.0603 (−2.59) | **+0.7640** | **+1.87** |
| 5 | **108** | LONG | 09-14 17:00 | +1.1371 (+1.54) | 🔴 **NEW — trail** 79 024.4 @ 09-14 21:01 | +1.5947 (+2.15) | **−0.4576** | **−0.62** |
| | | | | | **Σ RESOLVED (5 of 10)** | | **+1.0497** | **+$1.72** |

**5 RESOLVED of 10. Σ POSITIVE. THE RULE DOES NOT FIRE. FIVE MORE REQUIRED, ≈ 15–16 DAYS.**

🔴 **THE SUM IS NO LONGER CARRIED BY ONE TRADE.** On 2026-09-12 the +0.7433R was **entirely** vpos 104;
strip it and the rest were −0.9358R. Today, strip vpos 104 and the rest are **−0.6294R** — still negative,
but the positive side now has **two** members (104 and 106, +2.4431R together) against three negatives
(−1.3934R). **The one-trade dependency is weaker, not gone.**

🔴 **A SMALL CORRECTION TO THE CANON, SO IT IS NOT PROPAGATED.** `§0.EXIT-ADVISOR-RULE` records the three
resolution lags as "1h, 6.7h and 39h". The same paragraph's own timestamps give vpos 105 as 09-09 23:46 →
09-10 14:56 = **15.2 h**, not 39 h, and my replay reproduces that exit minute exactly. Nothing in the ledger
depends on it.

## 1d. THE COHORT BOUNDARY — 2026-09-12 14:58:32 UTC. **ONE CLOSE, AND IT DID NOT TAKE THE RE-WORDED BRANCH.**

**14 consultations** have occurred after the boundary: **9 took the new UNARMED wording, 5 took the ARMED
branch.** Exactly **ONE is a close** — vpos 108's, `trades 32630`.

### THE CLOSING VERDICT, IN FULL — `trades 32630`, 2026-09-14 17:00:23 UTC, `close` 0.72, `claude-haiku-4-5-20251001`, 1 120 chars, trigger `15m_exit_confirm` on `Bullish I-BOS`

> Entry thesis degradation. The 15m exit confirm trigger activates on thesis breakdown. Key evidence: (1)
> 15m regime shifted to NEUTRAL (was bull at entry); 5m also NEUTRAL (was bull). (2) 15m HyperWave category
> shows internal disagreement—both LONG and SHORT signals now sit equally within the 90-min momentum window,
> neutralizing that weight. (3) Recent 5m structure is dominantly bearish (6 of last 6 snapshots within
> Bearish OB or matching bearish bias), directly opposing the LONG. (4) Volume compression (1h: 1.51→1.26;
> 15m: 1.22→0.48) signals weakening conviction. (5) The 1H Bullish Confirmation+ (weight 1.0) remains, but
> it is ENTRY-ONLY and unsampled now—cannot assume it persists. (6) Position has captured +1.27R with
> giveback from peak only 0.19R; risk/reward now unfavorable given the loss of multi-timeframe confluence.
> (7) Order book imbalance fell to 12th percentile (extremely low), suggesting weak directional pressure.
> Stop at +1.05R away offers only 0.22R downside cushion but the thesis collapse warrants de-risking. Fee
> cost (0.111R / 9% of unrealised) is justified by removing thesis-failure risk.

*(That is the complete set: vpos 107, the only other close in the window, closed on its stop and has no
closing verdict. Its single consultation, `trades 32428` at 2026-09-13 21:25:27, was a `hold`.)*

### 🔴 DOES IT QUOTE THE ARM PRICE? **THE QUESTION DOES NOT APPLY TO THIS VERDICT, AND THAT IS THE ANSWER.**

**vpos 108 was ARMED.** Its prompt did not carry the re-worded "ARMS AT …" sentence at all — it carried the
**armed** block, which has no arm price to quote:

```
Trailing-stop arithmetic (this position's own constants)
  The trail exits 0.76R below the high-water mark, and the round trip costs 0.11R.
  For the trailing exit to land at or above the arm level (+1.00R), the peak must reach 1.87R.
  Peak so far: +1.46R.
```

🔴 **SO THE `§0.ARMLEAD` RE-WORDING HAS STILL NEVER BEEN IN FRONT OF A CLOSING DECISION. Zero closes have
taken the new unarmed branch. The inversion question is UNTESTED on closes, and no later pass may say
otherwise.**

### BUT ON THE HOLDS, THE RE-WORDING IS VISIBLY LANDING

Across the **9 post-boundary consultations that took the new unarmed branch** (all `hold`), the verdict
quotes the **arm PRICE** in **5 of 9 = 55.6 %**, against **1 of 33 = 3.0 %** over the whole preceding era C.

`trades 32585`, 2026-09-14 12:45:55, quotes the price **and** the distance, which no verdict had ever done:

> *"The trailing stop arms at 78523.1 (631.7 away, near recent MFE of 0.71R)"*

**This is 5 observations of a text property on ONE position's hold stream, produced by the same model call
that wrote the decision. It is legibility, exactly as `§0.ARMLEAD` said, and it is NOT a measured edge.**
None of the 9 used the trail's absence as a reason to close — but none of them closed at all, so there was
no opportunity to invert it. **0 inversions out of 0 chances is not evidence.**

---

# 2. THE TRAIL

## 2a. WHAT CLOSED EVERY TITAN POSITION — LIVE AND PAPER, NEVER POOLED

### LIVE (vpos 86–108, n = 23, all closed, book currently FLAT)

| closed by | n | ΣR | mean R | win rate | median hold |
|---|---|---|---|---|---|
| **`ai_exit`** (advisor) | **15** | **−0.9063** | −0.0604 | 4/15 = 26.7 % | 3.75 h |
| `sl` (stop) | 4 | **−4.4910** | −1.1228 | 0/4 = 0.0 % | 1.23 h |
| `trail` | 2 | **+1.2821** | +0.6411 | 2/2 = 100 % | 5.07 h |
| `external` | 2 | −1.0644 | −0.5322 | 0/2 = 0.0 % | 5.63 h |
| **TOTAL** | **23** | **−5.1796** | | **6/23 = 26.1 %** | |

per side — **LONG** n=14 ΣR **−4.3079**, 4/14, median hold 3.88 h · **SHORT** n=9 ΣR **−0.8717**, 2/9, median hold 2.01 h
per side × reason — LONG `ai_exit` 7 / −1.0568 · LONG `sl` 3 / −3.4689 · LONG `trail` 2 / +1.2821 · LONG `external` 2 / −1.0644 · SHORT `ai_exit` 8 / **+0.1505** · SHORT `sl` 1 / −1.0221

### PAPER (vpos 27–85, 52 usable of 53 closed; vpos 33 has a NULL `initial_risk_usdt` and is excluded; 6 more are `archived_pre_geometry_fix`)

| closed by | n | ΣR | mean R | win rate | median hold |
|---|---|---|---|---|---|
| `sl` | 27 | **−18.7323** | −0.6938 | 1/27 = 3.7 % | 3.18 h |
| **`trail`** | **14** | **+16.2901** | **+1.1636** | **14/14 = 100 %** | 17.63 h |
| `external` | 10 | +1.0108 | +0.1011 | 7/10 | 15.29 h |
| `post_entry_critical` | 1 | +0.0150 | +0.0150 | 1/1 | 0.02 h |
| **TOTAL** | **52** | **−1.4165** | | **23/52 = 44.2 %** | |

per side — **LONG** n=24 ΣR −6.7794, 8/24, median hold 5.23 h · **SHORT** n=28 ΣR **+5.3629**, 15/28, median hold 8.41 h

🔴 **THE TWO BOOKS DISAGREE ABOUT THE TRAIL ONLY IN HOW OFTEN IT GETS TO RUN, NEVER IN WHAT IT DOES WHEN IT
DOES.** On paper the trail closed **14 of 52 (26.9 %)** and every one of them won. Live it closed **2 of 23
(8.7 %)** and both won. **The trail has never lost money on either book. It simply almost never fires on the
live one.**

## 2b. 🔴 GIVEBACK FROM THE WATER MARK — THE LAW HOLDS, THE CONSTANT DOES NOT. RE-DERIVED, NOT ASSUMED.

**36 positions have ever armed** (breakeven applied) across both books; **16 of them were closed BY the
trail**.

| population | n | mean giveback | σ | **median residual vs `width_R + fee_R`** |
|---|---|---|---|---|
| **closed BY the trail (both books)** | **16** | **1.050R** | **0.079** | **+0.0025R** |
| … of which PAPER | 14 | 1.069R | — | +0.0025R |
| … of which LIVE (94, 100) | 2 | 0.921R | — | +0.0031R |
| all armed, any close reason | 36 | 0.861R | 0.284 | −0.0058R |

> ### 🔴 THE FORMULA IS UNBROKEN. `giveback = trail width in R + round-trip fee in R`
> On trail closes the median residual is **+0.0025R** and the worst absolute residual across all 16 is
> **0.149R**. The 2026-08-31 derivation stands verbatim on today's book.

🔴 **BUT "≈ 1.038R CONSTANT" WAS NEVER THE LAW — IT WAS THE MEAN OF A COHORT, AND THE COHORT HAS CHANGED.**
The formula's first term is the trail width expressed in R, and that ratio is a **per-position** number.
Paper positions carry widths of **0.93–1.03R**; the live positions that armed carry **0.756–0.760R**, with a
larger fee share (0.11–0.16R against paper's 0.03–0.19R). So the live book's predicted giveback is
**≈ 0.87–0.92R, not 1.04R**. **The mean moved because the population moved. The formula did not move at all,
and that is exactly what a geometric identity should do.**

🔴 **THE EXCEPTION CLASS IS CONFIRMED AGAIN, BY vpos 108.** The 2026-08-31 report noted that positions
closed **not** by the trail give back **less** than the formula, because the trail never got to fire. Two
live rows now show it and both are advisor closes:

| vpos | closed by | MFE | realised | actual giveback | formula | **residual** |
|---|---|---|---|---|---|---|
| 89 | `ai_exit` | +1.697R | +1.386R | 0.311R | 1.068R | **−0.758R** |
| **108** | **`ai_exit`** | **+1.463R** | **+1.137R** | **0.326R** | **0.870R** | **−0.544R** |

**The advisor's close on vpos 108 handed back 0.33R where the trail would have handed back 0.87R — and it
still finished 0.46R WORSE, because the water mark kept rising after it left.** Giving back less is not the
same as keeping more.

## 2c. THE ARM LEVEL AND THE WIDTH — RE-STATED. **NOTHING IN THE NEW DATA TOUCHES THEM.**

| measurement | direction | date | result |
|---|---|---|---|
| SOL's 0.75R arm ported to Titan | **arm EARLIER** (1.0R → 0.75R) | 2026-08-24 | 🔴 **−15.11R** on the seventeen |
| arm-level sweep 1.25R … 2.25R | **arm LATER** (1.0R → 1.92R) | 2026-08-31 | 🔴 **−10.13R** (−12.10R at 2.00R), **monotone worse at every step** |
| trail-width sweep 0.75R → 2.0R | **WIDER** | 2026-08-24 | 🔴 **−19.49R**, hold unchanged at 1.8 h, capture share **fell** 26.9 % → 23.3 % |

**Arming at +1.0R is a LOCAL OPTIMUM: one step left −15.11R, one step right −10.13R. The width 0.750 is the
maximum on BOTH books, and the axis is a CLIFF between 4R and 5R, not a slope.**

🔴 **DOES THE NEWER DATA CONTRADICT THEM? NO — AND I DID NOT RE-RUN THE SWEEP, AS INSTRUCTED.** The sweeps
could only ever move positions that **arm**. Of the four closes since 2026-09-12 (105, 106, 107, 108),
exactly **one armed** — vpos 108. The 2026-08-31 sweep's movable set grows from **20 to 21 positions, a
5 % increase**, and the invariant tail (MFE < 1.0R, unmovable at any arm level ≥ 1.0R) grows with it. A
5 % change in n cannot overturn a −10.13R / −15.11R / −19.49R result, **and vpos 108 points the same way**:
it armed, the breakeven lock held, the trail then delivered **+1.5947R**. Arming later would have denied it
the lock; a wider trail would have exited it lower. **Nothing contradicts. Nothing is re-swept.**

## 2d. 🔴 HOW MANY POSITIONS EVER REACH +1R AT ALL? **ON THE LIVE BOOK, 4 OF 23.**

| book | n | reached +1R (the arm) | share |
|---|---|---|---|
| **LIVE** | **23** | **4** (vpos 89, 94, 100, 108) | 🔴 **17.4 %** |
| PAPER | 52 | 17 | 32.7 % |
| combined | 75 | 21 | 28.0 % |

median MFE — **LIVE 0.427R**, PAPER 0.731R. Live LONG 3/14 reach it, live SHORT 1/9.

> ### 🔴 THIS IS THE ANSWER TO THE BRIEF'S OWN TEST, AND IT IS BELOW THE THIRD IT NAMED.
> **Not a third — a sixth.** The trail touches **17.4 %** of live positions and closes **8.7 %** of them.
> **The trail is not the main exit and it cannot be what the operator is feeling.** Whatever "it exits
> early" describes, it is the ADVISOR's decision on the other 82.6 %, or it is the entry. §3 answers which.

---

# 3. THE ENTRY

## 3a. 🔴 MFE, MAE AND WHERE THE PEAK FELL — EVERY LIVE POSITION

| vpos | side | closed by | MFE R | MAE R | realised R | hold | peak at | % of life |
|---|---|---|---|---|---|---|---|---|
| 86 | SHORT | sl | +0.099 | −0.920 | −1.022 | 11.01 h | 0.11 h | 1 % |
| 87 | LONG | ai_exit | +0.615 | −0.486 | −0.440 | 14.03 h | 13.08 h | 93 % |
| 88 | SHORT | ai_exit | +0.076 | −0.232 | −0.296 | 1.00 h | 0.51 h | 51 % |
| 89 | SHORT | ai_exit | **+1.697** | −0.143 | **+1.386** | 1.92 h | 1.83 h | 95 % |
| 90 | SHORT | ai_exit | +0.175 | −0.333 | −0.304 | 2.01 h | 1.03 h | 51 % |
| 91 | SHORT | ai_exit | +0.661 | −0.557 | −0.484 | 7.01 h | 1.90 h | 27 % |
| 92 | LONG | ai_exit | +0.001 | −0.706 | −0.728 | 4.01 h | 0.05 h | 1 % |
| 93 | SHORT | ai_exit | **+0.000** | −0.000 | −0.137 | 0.00 h | — | — |
| 94 | LONG | trail | **+1.802** | −0.635 | **+0.865** | 5.92 h | 5.71 h | 96 % |
| 95 | LONG | external | +0.560 | −0.481 | −0.533 | 9.42 h | 4.90 h | 52 % |
| 96 | LONG | ai_exit | +0.464 | −0.500 | −0.546 | 1.00 h | 0.43 h | 43 % |
| 97 | LONG | ai_exit | +0.116 | −0.809 | −0.796 | 2.01 h | 0.02 h | 1 % |
| 98 | LONG | ai_exit | +0.929 | −0.357 | −0.260 | 5.01 h | 1.24 h | 25 % |
| 99 | LONG | external | +0.060 | −0.421 | −0.532 | 1.83 h | 0.08 h | 4 % |
| 100 | LONG | trail | **+1.322** | −0.280 | **+0.417** | 4.21 h | 3.86 h | 92 % |
| 101 | SHORT | ai_exit | +0.427 | −0.047 | +0.296 | 1.75 h | 1.73 h | 99 % |
| 102 | LONG | sl | +0.188 | −0.974 | −1.158 | 1.51 h | 0.01 h | 1 % |
| 103 | LONG | sl | +0.015 | −0.996 | −1.123 | 0.95 h | 0.01 h | 1 % |
| 104 | LONG | ai_exit | +0.721 | −0.403 | +0.576 | 3.75 h | 3.71 h | 99 % |
| 105 | SHORT | ai_exit | +0.497 | −0.041 | −0.014 | 4.01 h | 2.51 h | 63 % |
| 106 | SHORT | ai_exit | +0.060 | −0.258 | −0.296 | 11.25 h | 0.03 h | 0 % |
| 107 | LONG | sl | **+0.000** | −0.958 | −1.187 | 0.68 h | 0.05 h | 7 % |
| 108 | LONG | ai_exit | **+1.463** | −0.507 | **+1.137** | 9.25 h | 9.11 h | 98 % |

*(MFE/MAE from the row's own stored `water_mark` / `max_adverse_price`; peak minute located on the same
gap-free 1m candle set, within each position's own `opened_at`→`closed_at` window.)*

## 3b(i) — 🔴 **THE SPLIT THE BRIEF ASKED FOR. IT IS NOT CLOSE.**

| class | n of 23 | share | ΣR carried |
|---|---|---|---|
| **NEVER in profit at all** (MFE = 0) — vpos 93, 107 | **2** | 8.7 % | −1.324 |
| **never printed +0.25R** — 86, 88, 90, 92, 93, 97, 99, 102, 103, 106, 107 | 🔴 **11** | 🔴 **47.8 %** | 🔴 **−7.581** |
| reached ≥ +0.5R and still finished NEGATIVE — 87, 91, 95, 98 | **4** | 17.4 % | **−1.717** |
| reached ≥ +1R — 89, 94, 100, 108 | 4 | 17.4 % | **+3.805** (all four positive) |

> ### 🔴 **77 % OF EVERY DOLLAR LOST ON THE LIVE BOOK BELONGS TO POSITIONS THAT WERE NEVER MORE THAN A QUARTER-R IN PROFIT.**
> Live losers: **17, ΣR −9.8564**. Of them, **11 never passed +0.25R and carry −7.5805R = 76.9 %** of all
> losses. Only **4** ever passed +0.5R, and they carry **−1.7167R = 17.4 %**.
> 🔴 **NOT ONE LOSER EVER REACHED +1R.** Median MFE: **losers 0.116R, winners 1.392R.**

**There is no "peaked at +2R and closed at −0.3R" population on this book. The worst case of that shape is
vpos 98 — peak +0.93R, closed −0.26R — and the entire class is four trades and −1.72R.** An exit mechanism,
however bad, cannot lose money that was never on the table.

**The peak-timing column says the same thing twice over.** Every winner peaked at **92–99 % of its life** —
the position was still making highs when it was closed. Every large loser peaked in the **first 1–7 %** —
vpos 86, 92, 97, 102, 103, 106, 107 all made their high within minutes of entry and spent the rest of their
lives underwater. **That is the signature of a bad entry price, not a bad exit rule.** Median peak position
across all 23: **47 % of life**.

## 3b. THE BOOK GATE SINCE THE ARMING — **14 EVALUATIONS, ZERO REFUSALS**

Boundary **2026-09-10 14:36:20 UTC**. Rows before it are DRYRUN observations and are never pooled with these.

| | count |
|---|---|
| evaluations in the ARMED era | **14** |
| … `open_long` | **9** |
| … `open_short` | **5** |
| 🔴 **refusals (clause A), ARMED era** | 🔴 **0** |
| refusals in the bot's ENTIRE history, either era | **0** |
| counter against the 200-row review | **29 / 200** (15 DRYRUN + 14 ARMED; the counter is **not** reset at arming) |
| `[BOOK-GATE]` journal lines | **0** — by design; the print sits inside the refuse branch |

**Against its pre-registration — LONG 4.26 % / SHORT 3.81 % / ratio 1.12×, alarm above 5 % either side or
ratio above 2×:**

| side | expected refusals | observed | rate | alarm? |
|---|---|---|---|---|
| LONG | 0.38 of 9 | **0** | 0.0 % | ✅ below 5 % |
| SHORT | 0.19 of 5 | **0** | 0.0 % | ✅ below 5 % |
| ratio | 1.12× | undefined (0/0) | — | ✅ cannot exceed 2× |

🔴 **ZERO REFUSALS IS NOT EVIDENCE OF A DEAD GATE, AND THE ARITHMETIC SAYS SO.** At the pre-registered
rates, the expected number of refusals over these 14 rows is **0.57**, and the probability of observing
**zero** is **≈ 57 %**. This is the single most likely outcome. **The gate is not yet judgeable; the review
point is 200 rows and it stands at 29.**

🔴 **AND IT HAS COME CLOSE — TWICE, BOTH SINCE THE LAST REPORT.** Two rows cleared the percentile half of
clause A and were admitted only on the distance half:

| row | time (UTC) | side | opp_pctl | threshold | opp_dist | threshold | outcome |
|---|---|---|---|---|---|---|---|
| 32767 | 2026-09-15 07:45:08 | SHORT | **99.0** | ≥ 85.0 ✅ | 0.1655 % | ≤ 0.0597 % ❌ | admitted |
| 32768 | 2026-09-15 07:50:09 | SHORT | **94.7** | ≥ 85.0 ✅ | 0.1584 % | ≤ 0.0597 % ❌ | admitted |

**A 99th-percentile opposing wall sitting 2.8× further away than the distance cut is exactly what clause A
is built to let through — "unusually large AND very close", both or nothing.** Neither row became an entry;
both were `ai_skipped` by the entry advisor.

## 3c. ENTRIES SINCE THE ARMING — **THE GATE STAYED SILENT. NOTHING WAS OVERRIDDEN.**

Three entries executed in the armed window, and every one carried a gate row with an **empty**
`book_gate_clause` — an **admit**, not a pass-through:

| entry row | time (UTC) | side | → vpos | gate clause | opp_pctl / dist |
|---|---|---|---|---|---|
| 31759 | 2026-09-11 22:00:10 | SHORT | **106** | *(empty — admitted)* | 10.0 / 0.1119 % |
| 32426 | 2026-09-13 21:25:04 | LONG | **107** | *(empty — admitted)* | 40.0 / 0.0338 % |
| 32533 | 2026-09-14 07:45:05 | LONG | **108** | *(empty — admitted)* | 5.0 / 0.2654 % |

🔴 **IT HAS REFUSED ZERO IN THIS WINDOW. There was no refusal to override, and none was overridden.**
Note vpos 107 — the worst of the three, **−1.187R, never green for a single minute** — passed the gate on a
40th-percentile wall at 0.0338 %, **0.0032 percentage points above the LONG distance cut of 0.0306 %.** It
is the closest the gate has ever come to refusing a position that went on to lose, and it did not refuse.

## 3d. RECENT CLOSES BY TIER COMPOSITION

| vpos | score | 1H | 15m | 5m | categories COUNTED | zeroed, and why |
|---|---|---|---|---|---|---|
| 104 | 4.25 | ⚪ `Bullish Confirmation` 12.8h | ✅ `HyperWave Up` 30m | ✅ `Bullish I-BOS` 0m | **2 of 3** | 1H — `ttl_expired` |
| 105 | 5.00 | ✅ `Smart Trail Bearish` 45m | ⚪ `HyperWave Down` 1.5h | ✅ `Bearish I-BOS` 0m | **2 of 3** | 15m — `ttl_expired` |
| 106 | 5.00 | ✅ `Any Bearish Confirmation` 3.0h | ✅ `HyperWave Down` 0m | ⚪ `Bearish I-CHOCH+` 0m | **2 of 3** | 🔴 5m — **`intra_conflict`** (LONG 2.00 / SHORT 2.50, 3 signals) |
| 107 | 5.50 | ⚪ `Any Bullish Confirmation` 6.4h | ✅ `HyperWave Up` 55m | ✅ `Bullish OB Created` 0m | **2 of 3** | 1H — `ttl_expired` |
| 108 | 4.75 | ✅ `Bullish Confirmation+` 4.7h | ⚪ `HyperWave Up` 15m | ✅ `Bullish I-CHOCH+` 0m | **2 of 3** | 🔴 15m — **`intra_conflict`** (LONG 1.75 / SHORT 1.75, 2 signals) |

**Was the 15m tier present? YES, on all five. COUNTED on three (104, 106, 107); zeroed on two (105, 108).**
**Zeroed by `intra_conflict`: 2 of 5. By `ttl_expired`: 3 of 5.**

🔴 **NOT ONE OF THE LAST FIVE ENTRIES HAD ALL THREE CATEGORIES COUNTING. Every single one scored on two of
three** — and in each case the third tier was *present and pointing the right way*, just disallowed.

✅ **`§0.MATRIX-TIER-NAMES` (`7b17e11`) IS DOING ITS JOB, VISIBLY.** vpos 108's zeroed 15m tier now names
**both sides with their ages** — `SHORT: HyperWave Signal Down @ 59.9 min` against `LONG: HyperWave Signal
Up @ 14.9 min`, 1.75 / 1.75. Before that commit this was an unexplained zero.

📋 **RECORDED, NOT PROPOSED:** in all five the `agreement` sentence reads *"15m and 1H and 5m all point
LONG/SHORT; … all agree"* while the gate counted only two of the three. That is **by contract** — the
sentence describes signal DIRECTION, the counter describes the SCORE GATE, and `7b17e11` deliberately kept
it byte-identical. It is stated here as a fact about what a reader sees, **not as a defect and not as a
proposal.**

---

# 4. VERDICT

## 4a. 🔴 THE RULE

> ## **5 RESOLVED of 10. Σ = +1.0497R / +$1.72. POSITIVE.**
> ## **THE RULE DOES NOT FIRE. DO NOT FLIP `EXIT_ADVISOR_DRYRUN`. IT STAYS `False`.**
> **Five resolved closes remain, ≈ 15–16 days at the measured 3.24 d/close — the first days of October 2026.**
> Nothing is UNRESOLVED; every observation in the population has a settled counterfactual.
> **The rule exists so a run of bad closes cannot flip a mechanism. Here it is doing the opposite job
> equally well: a run of GOOD closes has not earned the advisor an early acquittal either.** The next
> review is still at 10, then at 20.

## 4b. 🔴 WHICH OF THE THREE DOES THE NEWEST DATA ACTUALLY IMPLICATE? **THE ENTRY.**

| mechanism | what the numbers say | verdict |
|---|---|---|
| **THE TRAIL** | Closes **2 of 23** live positions, **has never lost on either book** (16/16 trail closes positive across both). Only **17.4 %** of live positions ever reach the arm. Its geometry sits at a measured local optimum on **all three** axes, and the one new armed position agrees. | ✅ **NOT IMPLICATED.** It barely participates. |
| **THE ADVISOR** | Ledger **+1.0497R over 5 resolved**. On the two new resolutions it was right once (+0.7640R) and wrong once (−0.4576R). Its 15 live `ai_exit` closes total **−0.9063R** — but those closes were **taken on positions whose median MFE was 0.427R**. | ⚖️ **PARTIALLY, AND THE SIGN IS CURRENTLY IN ITS FAVOUR.** 5 of 10; not judged. |
| 🔴 **THE ENTRY** | **11 of 17 live losers never printed +0.25R**, carrying **−7.58R = 77 % of all live losses**. **ZERO losers ever reached +1R.** Every large loser peaked in the **first 1–7 %** of its life. Live ΣR **−5.1796** on 23 positions. | 🔴 **IMPLICATED, AND BY A MARGIN NOTHING ELSE COMES NEAR.** |

> ### 🔴 THE OPERATOR'S READING IS POINTING AT THE WRONG MECHANISM, AND I AM SAYING SO PLAINLY.
> "Early exits taking losses" describes a position that was in profit and gave it back. **On the live book
> that describes FOUR trades and −1.72R.** The other thirteen losers — **−8.14R** — were never in profit
> worth the name, and eleven of them never got a quarter of an R. **You cannot exit those well. There is
> nothing there to exit.**
>
> The advisor's 15 live closes sum to −0.9063R **because it is handed positions that are already losing**,
> not because it leaves too soon. Against the only standard that can judge it — what holding would have
> done — it is currently **ahead by +1.05R**.

🔴 **AND THE ONE PATTERN THAT NOW SEPARATES PERFECTLY, STATED AS A DESCRIPTION AND NOT AS A FINDING.**
The 2026-09-12 17:15 report observed that *whether the counterfactual was going to ARM* tracks the
advisor's outcome. **On the canon population it is now 5 for 5:**

| vpos | counterfactual armed? | Δ |
|---|---|---|
| 104 | ❌ never armed → ran to the original stop | **+1.6791** advisor WON |
| 106 | ❌ never armed → ran to the original stop | **+0.7640** advisor WON |
| 101 | ✅ armed → trailed | **−0.1553** advisor LOST |
| 105 | ✅ armed → trailed | **−0.7805** advisor LOST |
| 108 | ✅ already armed at the close → trailed higher | **−0.4576** advisor LOST |

**Perfect separation, and near-tautological — a position that arms is by construction one that ran far
enough to be worth holding.** But it joins §2d to make the operator's own case in reverse: **only 17.4 % of
live positions ever arm.** The advisor closes early into a book where five of six positions were never going
anywhere. **On this book, being early is right more often than it is wrong — and the ledger's +1.05R is
that arithmetic, not a talent.**

## 4c. NOTHING PROPOSED, NOTHING APPLIED

**No change is proposed and nothing was applied.** No flag was touched, no order placed, no process
restarted, no file on either bot modified. Everything above is a measurement.

---

## 🔴 READ-ONLY ATTESTATION

| claim | proof |
|---|---|
| `openitems_guard` run first | **EXIT=0** — *"✅ header and current-state table agree with runtime"*, titan-bot HEAD `f16c271`, 14 watched values |
| Titan DB read-only | opened `file:/root/titan-bot/trades.db?mode=ro` with `PRAGMA query_only=1`; **read back as `1`** at the start and again at the end of the pass |
| no writes | every DB handle opened `mode=ro`; zero `INSERT`/`UPDATE`/`DELETE` issued |
| no orders | no exchange write call made; the only network use was **public** BingX OHLCV (`fetch_ohlcv`), unauthenticated |
| no restart | `systemctl show titan` → **MainPID 1572470**, `NRestarts=0`, active since **2026-09-12 14:58:32 UTC** (the `§0.ARMLEAD` restart) — unchanged |
| `NRestarts` unchanged on BOTH | titan **NRestarts=0** · mercury-sol **NRestarts=0** |
| `EXIT_ADVISOR_DRYRUN` still False | read out of the loaded `__pycache__/config.cpython-312.pyc` (mtime 2026-09-10 14:34:54): **`False`** |
| `BOOK_GATE_DRYRUN` still False | same bytecode: **`False`** (`BOOK_GATE_ENABLED=True`, `CLAUSE_A=True`) |
| `CLAUSE_B` still False | same bytecode: **`BOOK_GATE_CLAUSE_B_ENABLED = False`** |
| **Mercury-SOL untouched** | 🔴 `/mnt/volume_nyc1_1780480650620/mercury-sol` **was not opened, read, listed or written**. The only command naming it was `systemctl show mercury-sol -p NRestarts` (**0**, MainPID 2245907, active since 2026-09-14 22:20:45) to satisfy the attestation. Its DB was never opened. |
| book state at the pass | **FLAT** — 0 open `virtual_positions`, 0 `exit_pending`, 0 `breakeven_jobs`; bot alive (last row `33084`, 2026-09-16 15:00:17 UTC) |

**Provenance.** Titan's own `trades.db` opened `mode=ro` with `query_only=1`; `config.py`, `virtual_trader.py`,
`main.py`, `book_gate.py` read from disk at revision `f16c271` and the flags re-read from the **bytecode the
running worker imported**; BingX `BTC/USDT:USDT` 1m candles fetched over the public ccxt endpoint
(71 455 bars, 2026-07-29 00:00 → 2026-09-16 14:54 UTC, **0 gaps**); the counterfactual stand validated by
reproducing all three canon-published rows to the digit before any new row was computed;
`journalctl -u titan` retains nothing before **2026-09-15 06:30**, which is why vpos 108's triggers are
established from the DB's own `tv_action` column rather than quoted from the journal. Canon read:
`§0.EXIT-ADVISOR-RULE`, `§0.ARMLEAD`, `§0.BOOK-GATE-ARMING`, `§0.MATRIX-TIER-NAMES`, and the
2026-09-12 **1430 / 1715 / 1840** reports.
