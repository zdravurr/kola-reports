# r2-prior-move-bucket-validation

_2026-07-26 17:48 UTC_

---

# TITAN R2 — prior-move entry-timing bucket: validation BEFORE build

**2026-07-26 · READ-ONLY. Nothing built, nothing proposed.** Tree clean at `b878535`. Paper mode.

**Verdict up front: DO NOT BUILD. The effect does not survive decomposition.** It is the same
class of artifact as the counter-short caution retired earlier today — an aggregate number with no
internal structure. Detail below; the decisive table is §6.

**I must also correct my own audit.** I reported the bucket effect at Fisher **p=0.011**, and
**p=0.027** "excluding the wall-trail era". That second figure was under-filtered: it removed the
wall-trail window but not recheck-tightened positions *outside* it (vpos 53, 55, 57, 74). With both
contaminations removed the result is **p=0.1544 — not significant**, and the mid bucket collapses
from n=8 to n=1.

---

## 5. How the bucket is derived (answering this first — it frames everything)

From `titan_prior_move_logger.py`:
```python
fav4 = dir * (entry_px - px_4h_ago) / px_4h_ago * 100      # dir = +1 LONG, -1 SHORT

fav4 is None      -> 'n/a'
fav4 < 0          -> 'pullback'   # entered on a dip AGAINST the trade direction
0 <= fav4 < 1.0   -> 'early'
1.0 <= fav4 < 2.0 -> 'mid'
fav4 >= 2.0       -> 'late'       # >2% already ran our way in the prior 4h
```

**Computable at entry time? Formally yes** — it needs only the entry price and the price 4h earlier.
No post-entry information is used. The label is not look-ahead.

**But the historical labels are a RECONSTRUCTION, not a measurement.** The logger back-computes
`px_4h_ago` from a price oracle assembled from `skip_drift_samples` + executed trade prices with a
**25-minute tolerance**, precisely so it needed no hook in the entry path. Consequences:
* No oracle sample within 25 min of T-4h ⇒ `bucket='n/a'`. That is **15 of 49** joined records.
* A live implementation would read OHLCV instead, so live values need not match the logged ones.
* **The oracle's density varies with time** — and that turns out to be fatal. See §1b.

---

## 1. Internal structure, per bucket (not collapsed)

All 49 closed positions with a prior-move record:

| bucket | n | win | net | mean | median | fav4 range |
|---|---|---|---|---|---|---|
| pullback | 3 | 1/3 | -61.04 | -20.35 | -62.03 | [-0.46, -0.10] |
| early | 21 | 11/21 | +69.89 | +3.33 | +0.78 | [+0.08, +0.97] |
| mid | 8 | **0/8** | -555.45 | -69.43 | -47.53 | [+1.00, +1.85] |
| late | 2 | 0/2 | -151.49 | -75.75 | -75.75 | [+2.12, +3.13] |
| **n/a** | **15** | **10/15** | **+1437.48** | **+95.83** | +8.34 | — |

**Not monotone.** The "Titan enters late" thesis predicts `pullback >= early > mid > late`.
Observed: `early (+3.33) > pullback (-20.35) > mid (-69.43) ~ late (-75.75)`. The pullback bucket —
the one the thesis says should be *best* — is negative. Only the early→mid→late leg is ordered.

**One bucket is carrying it, and it is `mid`, not `late`.** The -767.98 I quoted for the
"not-early" group decomposes as mid -555.45 (72%) + late -151.49 + pullback -61.04. The headline
"late entries lose" rests on **two trades**.

### 1b. The `n/a` bucket is a measurement artifact and it holds ALL the book's profit

```
n/a       : n=15  net=+1437.48   (the ENTIRE book is +739.40 — n/a is 194% of it)
n/a entry dates    : 2026-05-23 .. 2026-06-04
all other entries  : 2026-05-21 .. 2026-07-24

entries by month:   2026-05  n/a=10  bucketed= 3
                    2026-06  n/a= 5  bucketed=11
                    2026-07  n/a= 0  bucketed=20

first skip_attribution row (feeds the price oracle): 2026-06-07 13:20
```
Before J. the oracle is sparse, so the bucket is `n/a`; after June it is dense. **Bucket
assignment is correlated with DATE, and date is correlated with the profitable era** — the +$2119
TREND-short cohort of late May / early June (vpos 43, 44, 46, 48, 49, 50) sits almost entirely in
`n/a`. Any comparison across buckets is therefore also a comparison across eras. This alone would
invalidate the bucket comparison even if everything else held.

---

## 2. Side split — the effect exists only in aggregate

| SHORT | n | win | net | mean |
|---|---|---|---|---|
| pullback | 3 | 1/3 | -61.04 | -20.35 |
| early | 11 | 8/11 | +320.81 | +29.16 |
| mid | 3 | 0/3 | -184.47 | -61.49 |
| **late** | **0** | — | — | — |
| n/a | 11 | 7/11 | +1520.58 | +138.23 |

| LONG | n | win | net | mean |
|---|---|---|---|---|
| **pullback** | **0** | — | — | — |
| early | 10 | 3/10 | -250.91 | -25.09 |
| mid | 5 | 0/5 | -370.98 | -74.20 |
| late | 2 | 0/2 | -151.49 | -75.75 |
| n/a | 4 | 3/4 | -83.10 | -20.77 |

* **SHORT has ZERO `late` observations.** The profitable side has never taken a late entry.
* **LONG has ZERO `pullback` observations.**
* On LONG, `early` is also a loser (-250.91, 3/10) — so "early is good" is a SHORT-only statement,
  and on SHORT it cannot be contrasted against `late` at all.

The aggregate effect is built from two non-overlapping side-specific patterns. That is exactly the
shape the Boss flagged as suspect, and it is what it looks like here.

---

## 3. Outliers — the early bucket's profit is one trade

```
pullback  n=3  PnL: [-169.0, -62.0, +170.0]
   without the worst (vpos 61, -169.0): n=2 net=+107.98   <- sign FLIPS
early     n=21 PnL: [-139.5,-132.7,-116.6,-103.5,-74.6,-59.1,-45.6,-43.5,-30.8,-14.5,
                     +0.8,+2.7,+3.3,+7.1,+21.4,+45.4,+75.2,+80.1,+106.2,+117.7,+370.4]
   net +69.89; without the best (vpos 58, +370.4): net -300.55   <- sign FLIPS
mid       n=8  PnL: [-201.8,-106.9,-73.1,-50.6,-44.4,-41.4,-32.7,-4.5]
   all 8 negative; without the worst: still -353.62            <- the ONLY robust part
late      n=2  PnL: [-78.7, -72.8]
```
`early` being positive and `pullback` being negative both hinge on a single trade each. Only `mid`
is outlier-independent — and `mid` is the bucket that decontamination destroys (§4).

---

## 4. Contamination — 15 of 34 bucketed positions had their outcome decided by a broken stop

Excluded: entries inside the wall-trail window (07-02 23:28 .. 07-13 01:55) **and** any position
whose `recheck_status='tightened'`. Both classes exited on a self-tightened stop, not on entry
timing.

```
vpos 53 SHORT mid      -106.86  [recheck TIGHTEN]        vpos 68 SHORT mid       -4.52  [both]
vpos 55 LONG  late      -78.70  [recheck TIGHTEN]        vpos 69 LONG  mid      -50.64  [wall-trail]
vpos 57 SHORT pullback +170.01  [recheck TIGHTEN]        vpos 70 LONG  mid      -44.42  [wall-trail]
vpos 63 LONG  early     -45.57  [wall-trail]             vpos 71 LONG  early    -30.78  [both]
vpos 64 LONG  early      +3.32  [wall-trail]             vpos 72 LONG  early    -74.61  [both]
vpos 65 LONG  mid       -41.35  [wall-trail]             vpos 73 LONG  early    -43.54  [wall-trail]
vpos 66 SHORT early     -59.11  [wall-trail]             vpos 74 SHORT mid      -73.09  [recheck TIGHTEN]
vpos 67 LONG  mid       -32.73  [both]
```

### Clean sample — both sides (n=19)
| bucket | n | win | net | mean |
|---|---|---|---|---|
| pullback | 2 | 0/2 | -231.05 | -115.52 |
| early | 15 | 10/15 | +320.17 | +21.34 |
| **mid** | **1** | 0/1 | -201.83 | -201.83 |
| **late** | **1** | 0/1 | -72.79 | -72.79 |

### Clean, by side
```
SHORT  pullback 2 (0/2, -231.05) · early 10 (8/10, +379.92) · mid 0 · late 0
LONG   pullback 0                · early  5 (2/5,  -59.75) · mid 1 · late 1
```

### Significance on the clean sample
```
BOTH sides   early 10/15 win, +320.17  |  mid+late 0/2 win, -274.63  |  Fisher p=0.1544
SHORT        untestable — early=10, mid+late=0
LONG         early  2/5  win,  -59.75  |  mid+late 0/2 win, -274.63  |  Fisher p=1.0000
```

Outliers on the clean sample:
```
SHORT early n=10 net=+379.92 (8/10 win)
   without the best (vpos 58, +370.4): net=+9.47   without the top two: net=-96.72
LONG  early n=5  net= -59.75 (2/5 win)
   without the best (vpos 54, +117.7): net=-177.46
```

Continuous `fav4` on the clean sample — winners and losers **overlap on every split**:
```
BOTH   W n=10 mean +0.539 [+0.14,+0.97] | L n=9 mean +0.600 [-0.46,+2.12]  overlap YES
SHORT  W n= 8 mean +0.521 [+0.14,+0.97] | L n=4 mean -0.062 [-0.46,+0.33]  overlap YES
LONG   W n= 2 mean +0.612 [+0.56,+0.67] | L n=5 mean +1.131 [+0.38,+2.12]  overlap YES
```

---

## 6. Verdict — the decisive table

Uncontaminated observations per bucket per side:

| | pullback | early | mid | late |
|---|---|---|---|---|
| **SHORT** | 2 | 10 | **0** | **0** |
| **LONG** | 0 | 5 | **1** | **1** |

**This is not a real, side-specific, structurally-sound effect. It is an aggregate artifact.**

Five independent reasons, any one of which would be enough to hold the build:

1. **Not monotone.** The `pullback` bucket, which the thesis says should be best, is negative.
2. **The bucket label is confounded with time.** 15 rows are `n/a` purely because the price oracle
   was sparse before June, and those 15 hold +1437 — 194% of the book's entire profit.
3. **Side split fails.** SHORT — the only profitable side — has **zero** mid and **zero** late
   observations after decontamination. The claim cannot be tested where it matters.
4. **Outlier-dependent.** `early`'s profit is one trade (vpos 58); remove it and the sign flips.
   `pullback`'s loss is one trade (vpos 61); remove it and that sign flips too.
5. **Contamination was doing the work.** 15 of 34 bucketed positions exited on a broken stop.
   Removing them collapses `mid` from n=8 to n=1 and takes the headline from p=0.011 to **p=0.1544**.

**Recommendation: do not build R2. Keep the logger running.** It costs nothing, it is already
accumulating, and it is the only thing that can change this answer.

**What would change the verdict:** SHORT observations in `mid` and `late`. There are currently
**zero**. At Titan's rate — 28 SHORT closes in 65 days, with mid+late roughly a quarter of bucketed
entries — reaching n≈8 per bucket on SHORT alone is a **multi-month** wait, not weeks. I am not
proposing a threshold, a caution, or an A/B arm on this evidence.

**One fixable defect, worth doing regardless of R2:** the `n/a` rate is a pure instrumentation
problem. If the bucket is ever to be usable, `px_4h_ago` should come from an OHLCV read at entry
time rather than from a reconstructed oracle with a 25-minute tolerance. That would also remove the
date confound from all future rows. That is a change to the *sensor*, not to the trade path — but
it is not proposed here either; it is noted for whenever R2 is revisited.

---

Nothing was applied. Session commits remain `93c20c3` (R1), `596fbdf` (superseded), `b878535`
(counter-short caution retired). Tree clean, `titan.service` healthy, Mercury-SOL untouched.
