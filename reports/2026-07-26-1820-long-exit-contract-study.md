# long-exit-contract-study

_2026-07-26 18:20 UTC_

---

# TITAN — LONG-side exit-contract study (D4 → D2)

**2026-07-26 · READ-ONLY. No design proposals, no multipliers, no targets, no trail parameters.**
Tree clean at `b878535`. Paper mode.

**Your caveat was correct, and it overturns the headline.** The 0.38R figure was an artefact of the
bug we fixed today. On the clean sample **longs and shorts have essentially the SAME median
excursion — 0.93R vs 0.97R, a ratio of 1.04×, not 2.48×.** "Longs move less" is false at the median.

What survives is narrower and sharper: **longs have no right tail (0/10 reach 2R vs 29% of shorts),
they peak EARLIER than shorts and then stall, and the trail gives back ~1R by construction on both
sides — which is survivable on a 1.84R peak and fatal on a 1.16R peak.**

---

## 1. Clean excursion picture — truncation removed

Clean = lifetime never overlapped the wall-trail window (07-02 23:28 – 07-13 01:55) **and**
`recheck_status != 'tightened'`.
Clean LONG n=10 (vpos 35, 37, 39, 41, 45, 54, 59, 75, 78, 79) · clean SHORT n=21.

| | MFE med (R) | p25 | p75 | max | ≥1R | ≥2R |
|---|---|---|---|---|---|---|
| LONG — all 21 | 0.38 | 0.12 | 0.91 | 1.59 | 19% | **0%** |
| **LONG — clean 10** | **0.93** | 0.30 | 1.14 | 1.59 | **40%** | **0%** |
| SHORT — all 28 | 0.93 | 0.36 | 2.27 | 7.38 | 46% | 29% |
| **SHORT — clean 21** | **0.97** | 0.58 | 2.31 | 7.38 | **48%** | **29%** |

In percent: clean LONG MFE p25 0.33 / med 1.16 / p75 1.40 / max 2.54 · clean SHORT p25 0.81 /
med 1.52 / p75 3.16 / max 6.58.

**The median asymmetry all but vanishes: 1.04× on the clean sample against 2.48× on the full one.**
The long side's excursion distribution was understated by exactly the bug that was truncating it.

**What does survive is the tail.** No long in the book has ever reached 2R (best 1.59R); 6 of 21
clean shorts have, up to 7.38R. Significance of that gap: if longs shared the shorts' 28.6% rate,
P(0 of 10) = **0.035** — marginally significant. At n=10 we **cannot** exclude that the long side
simply has not had its runner yet. This is the single number that most needs more n.

Per-position, clean LONG (sorted by peak):
```
 vp reason     MFE R  exit R  SLd%      pnl        vp reason    MFE R exit R  SLd%      pnl
 79 trail       1.59    0.57  1.59   +80.10        41 sl         0.91  -1.05  1.23  -139.51
 39 trail       1.29    0.28  0.93   +15.53        75 external   0.43  -0.03  1.37   -14.52
 54 external    1.16    0.79  1.67  +117.71        37 sl         0.26  -1.01  0.94  -104.59
 45 sl          1.06    0.14  1.33    +5.34        78 sl         0.10  -1.08  0.87  -103.54
 35 external    0.94    0.56  1.44    +0.62        59 sl         0.09  -1.01  1.90  -201.83
```

---

## 2. Time-to-1R

Path data (`position_excursion_samples`, 2,205 rows) covers **vpos 61–82 only** — 22 positions, of
which just **8 are clean** (LONG 75, 78, 79 · SHORT 61, 76, 77, 80, 81). Everything in this section
is therefore anecdotal and is reported as such.

```
LONG   reached 1R: 1 of 13 with path data — vpos 79, at 16.6h
       did not reach: 12, median survival 3.7h
SHORT  reached 1R: 2 of 8  — vpos 68 at 1.5h, vpos 81 at 2.6h (median 2.1h)
       did not reach: 6, median survival 6.1h
```

Holding times over the whole book are firmer:
```
                    all        winners     losers
LONG   all n=21     5.2h        34.5h       3.2h
LONG   clean n=10   6.2h        38.6h       4.4h
SHORT  all n=28     8.4h        10.5h       3.7h
SHORT  clean n=21  10.1h        17.3h       9.7h
```
**A winning long takes 38.6h; a losing long is over in 4.4h — a 8.8× gap. For shorts the same gap
is 1.8× (17.3h vs 9.7h).** The long side is bimodal in time in a way the short side is not: either
it works over a day and a half, or it is dead inside four hours.

---

## 3. Excursion shape — longs are NOT slower; they peak earlier and stall

Path shape is real up to the moment of death even for machinery-killed positions, so all 22 are
used for shape; none of them is used for outcome.

Median MFE in R at each elapsed mark (n shrinks fast — read the counts):
```
    mark     LONG n/med      SHORT n/med
   0.25h     12 / 0.12R       7 / 0.03R
    0.5h     12 / 0.17R       7 / 0.03R
      1h     11 / 0.30R       7 / 0.13R
      2h      9 / 0.29R       7 / 0.21R
      4h      7 / 0.38R       5 / 0.21R
      8h      3 / 0.49R       2 / 0.95R     <- crossover
     16h      2 / 0.82R       2 / 1.42R
     24h      1 / 1.59R       1 / 1.87R
```

Share of the position's FINAL peak already reached by each mark:
```
LONG    0.5h  53%   ·  1h  67%   ·  2h  91%   ·  4h 100%   (n=12, 11, 9, 7)
SHORT   0.5h  44%   ·  1h  65%   ·  2h 100%   ·  4h 100%   (n= 5,  5, 5, 3)
```

**Answer to the question as posed: longs do not move slower and do not move in smaller steps.
They front-load like shorts — 91% of a long's eventual peak is in by hour 2 — and then they STALL.**
Shorts are behind longs in R terms for the first four hours and overtake somewhere around hour 8,
continuing to extend afterwards. Longs simply stop.

Caveat stated plainly: the crossover rests on **n=3 LONG and n=2 SHORT at the 8h mark, n=1 each at
24h**. The *front-loading* result (n=9–12) is solid; the *crossover* is a hypothesis, not a finding.

---

## 4. What the current contract costs

`trail_pct` is set equal to the original stop distance on **47 of 49** positions (medians identical
at 1.369%; max divergence 0.556pp). **So the trail gives back exactly one stop distance — 1R — by
construction, identically on both sides.** The observed givebacks confirm it.

Clean sample, positions that ever reached at least 0.5R:

| | n | giveback med (R) | giveback med (% of peak) | total given back |
|---|---|---|---|---|
| **LONG** | 6 | **0.97R** | **72%** | 5.67R |
| **SHORT** | 16 | **0.98R** | **54%** | 17.03R |

Winners only:

| | n | peak (R) | exit (R) | given back |
|---|---|---|---|---|
| **LONG** | 5 | 1.16 | 0.56 | **64%** |
| **SHORT** | 14 | 1.84 | 0.85 | **49%** |

**This is the crispest statement of the defect. The ABSOLUTE giveback is the same on both sides —
0.97R vs 0.98R — because the trail is 1R by construction. What differs is the peak it is subtracted
from. One R off a 1.84R short leaves 0.84R. The same one R off a 1.16R long leaves 0.16R.**

The same rule, applied identically, is survivable on one side and consumes almost the entire move
on the other. That is why 12 of 28 shorts exit on the trail and only 2 of 21 longs do.

Worked examples from the clean long sample:
```
vpos 79  peak 1.59R -> exit 0.57R   gave back 1.03R (64%)   +80.10  (best long in the book)
vpos 45  peak 1.06R -> exit 0.14R   gave back 0.92R (87%)    +5.34  (a full 1R move, +$5 realised)
vpos 39  peak 1.29R -> exit 0.28R   gave back 1.01R (79%)   +15.53
```
Compare the short side, where the identical rule leaves the trade intact:
```
vpos 58  peak 3.40R -> exit 2.45R   gave back 0.95R (28%)  +370.45
vpos 48  peak 2.98R -> exit 2.04R   gave back 0.94R (31%)  +441.84
```

---

## 5. What the data shows, and nothing more

1. **The 0.38R figure was truncation.** Clean medians are 0.93R (LONG) vs 0.97R (SHORT). The
   median-excursion asymmetry that motivated D2 **does not exist**. That hypothesis is retired.
2. **The real asymmetry is the tail.** 0/10 clean longs reached 2R against 29% of shorts
   (P = 0.035 under the shorts' rate). Marginal at n=10; needs more closes before it is safe to act on.
3. **Longs are not slow.** They reach 91% of their peak within 2h — marginally faster than shorts.
   Then they stall while shorts continue. The stalling is what the tail deficit is made of.
4. **The trail is 1R by construction on both sides** (47/49 positions), and it gives back what it is
   built to give back: 0.97R for longs, 0.98R for shorts. Nothing is malfunctioning.
5. **The defect is the interaction, not either part.** A 1R trail against a 1.16R median winner peak
   returns 36% of the move; against a 1.84R peak it returns 51%. Longs surrender 72% of every peak
   above 0.5R against the shorts' 54%.
6. **Which fix this points to is deliberately left open.** The shape rules out "longs need a longer
   minimum hold" (they peak by hour 2, not later). It is consistent with an earlier partial, a
   different trail-arming point, or a fixed target — and the data here cannot separate those three.
   That separation needs the same decomposition discipline we applied to R2 and R5, on a clean
   sample larger than n=10 with n=6 above 0.5R.

**Sample-size honesty, since it governs everything above:** clean LONG n=10, of which 6 ever exceeded
0.5R and 5 were winners. Path data exists for only 3 clean longs. Every conclusion in §2 and the
crossover in §3 rests on single-digit n. §1 and §4 are the parts that can bear weight.

---

Nothing was applied. Session commits: `93c20c3`, `596fbdf` (superseded), `b878535`.
`titan.service` healthy, Mercury-SOL untouched.
