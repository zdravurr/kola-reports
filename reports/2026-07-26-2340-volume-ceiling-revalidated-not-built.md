# volume-ceiling-revalidated-not-built

_2026-07-26 23:40 UTC_

---

# TITAN — volume-spike entry ceiling: re-validated, verdict unchanged. DO NOT BUILD.

**2026-07-26 23:50 UTC · READ-ONLY. Nothing built, no diff.** Tree clean at `d12e276`.

**Note on provenance:** this same validation was run earlier tonight (23:30) and its verdict is
already recorded in `OPEN-ITEMS §11`. I re-ran it from scratch on current data rather than citing
the earlier result — no position has closed since (49 closed, 1 open), so the numbers are identical.
This report supersedes nothing; it confirms.

---

## What survives filtering

Two mandatory exclusions:
* **Corrupted metric** — the forming-candle fix (`55d9c7f`) landed **2026-07-04 11:58**. Every
  `srv_vol_ratio_5m` before that read the *forming* candle and is not comparable.
* **Contamination** — wall-trail window (07-02 23:28 – 07-13 01:55) or `recheck_status='tightened'`.

```
all closed                                    49
corrected metric (entry after 07-04 11:58)    17
AND uncontaminated                             7   -> vpos 75, 76, 77, 78, 79, 80, 81
```

| vpos | side | vol5m | PnL | exit | score | MTF | ADX-1h |
|---|---|---|---|---|---|---|---|
| 75 | LONG | 0.53 | -14.52 | external | 4.00 | 4 | 34.2 |
| 76 | SHORT | 1.38 | +45.36 | external | 6.00 | 3 | 21.3 |
| 77 | SHORT | 3.51 | -132.75 | sl | 2.25 | 4 | 30.3 |
| 78 | LONG | 5.01 | -103.54 | sl | 2.50 | 4 | 25.1 |
| 79 | LONG | 3.18 | +80.10 | trail | 4.25 | 4 | 21.7 |
| 80 | SHORT | 2.98 | -116.58 | sl | 4.00 | 4 | 30.4 |
| 81 | SHORT | 1.54 | +75.24 | trail | 2.50 | 4 | 20.5 |

## SHORT — direction right, sample fatal

```
n=4   winners 1.38, 1.54   losers 2.98, 3.51   separation CLEAN, no overlap
Fisher at a 2.0 threshold: p = 0.333
drop the best and worst trade -> one winner (1.38) vs one loser (2.98)
```
Perfect separation of two against two happens by coin flip one time in six.

**Where the quoted p = 0.048 came from.** That figure counted n=7 on the SHORT side, including
**vpos 66, 68 and 74** — and all three are contaminated. Their combined record is **0 wins in 3**,
all three high-volume, all three closed by a stop the machinery had moved. They supplied the losing
tail that made the separation significant, and their outcome was not determined by the entry.

## LONG — contradicts

```
n=3   winner 3.18   losers 0.53, 5.01   OVERLAPPING   Fisher p = 1.000
```
The sole winning long entered on the *second-highest* volume in the group. Direction is inconsistent,
so the mandatory side-split fails outright. The 7 contaminated LONGs (vpos 65, 67, 69–73) are **0 wins
in 7** — they cannot rescue it either, they are simply the wall-trail era.

## Angle (b) is not independent

The SL-vs-trail comparison (2.54 vs 0.95) was computed across the whole book. With the metric-validity
window and decontamination applied, **3 of 25 SL deaths and 2 of 14 trail exits remain** — and those
five are a subset of the same seven above. It is the same four data points re-sorted by exit reason,
not a second line of evidence. The 2.7× gap lived almost entirely in the pre-07-04 corrupted metric.

## Confounding — on the clean seven

```
vol5m vs confluence score   r = -0.48      <- the one worth watching
vol5m vs entry hour (UTC)   r = -0.41
vol5m vs vol_ratio_1h       r = +0.28
vol5m vs ADX-1h             r = -0.10      <- NOT the ADX signal in disguise
market_regime at entry      TREND on all 7 <- regime does not discriminate
```
It is **not** ADX wearing a different hat — that correlation is near zero. The notable entanglement
is with **confluence score**: high-volume entries also tend to be low-score entries, which the score
gate already sees. At n=7 the correlation itself is untrustworthy, but it is the first thing to test
when the sample exists.

---

## VERDICT — do not build

**Not a real, side-specific, structurally-sound effect. A third aggregate artifact**, failing for the
same reason as the prior-move bucket and the counter-short caution: the significance was computed
over rows that could not carry it.

* SHORT: 2 vs 2, p = 0.333, one trade either way ends the test.
* LONG: contradicts, p = 1.000.
* The two "independent" angles are the same seven positions.

**Nothing built. No diff, no A/B arm, no threshold, no config flag, no snapshot needed.**

The A/B design in the brief is right and should be used when this is revisited — the argument that
counter-short was unmeasurable because it fired only on overdetermined setups still holds, and a
volume caution on otherwise-clean TREND entries genuinely would be measurable. There is simply
nothing to A/B yet.

**What changes the answer:** ~8-10 clean, correctly-measured SHORT closes with a mix of outcomes.
Current: 4. At roughly one short close every four days, **6-10 weeks** — and only if today's
wall-trail and recheck fixes hold, since contamination is what inflated the original figure.

---

## Review date (already recorded, restated here)

`OPEN-ITEMS §11`: re-cut at ~10 clean corrected SHORT closes, and **in any case no later than
2026-09-30**. If the cohort has not reached n by then the finding **expires** rather than waiting
indefinitely — which is precisely the failure mode of the counter-short statistic, which sat
unreviewed from June until its sign had inverted.

Also noted there, not acted on: the `volfloor` sensor's threshold (6 per side) counts rows that
decontamination removes. It should count **clean** rows, or it will keep firing on evidence that
cannot be used.

---

Nothing applied. Tree clean at `d12e276`; `titan.service`, `nginx` and `mercury-sol.service` healthy.
