# volume-ceiling-not-built

_2026-07-26 23:30 UTC_

---

# TITAN — the volume-spike entry floor: validated, and it does NOT survive

**2026-07-26 23:35 UTC · READ-ONLY. Nothing built, no diff, no proposal.** Tree clean at `ef7fa10`.

**Verdict up front: STOP. Do not build.** Both angles collapse onto the same **seven** positions,
and on the clean, correctly-measured sample the SHORT separation is **2 winners vs 2 losers,
p = 0.333**, while LONG points the wrong way. This is the third aggregate artifact of the day, and it
fails for exactly the reason R2 and the counter-short caution failed — the number was computed over
rows that could not carry it.

---

## The filtering, and how little survives it

Two exclusions, both mandatory and both stated in the brief:

* **Corrupted metric.** The forming-candle fix (`55d9c7f`) landed **2026-07-04 11:58**. Every
  `srv_vol_ratio_5m` before that is the broken metric — it read the *forming* candle, so the value
  is not comparable with anything measured after.
* **Contamination.** Wall-trail window (07-02 23:28 – 07-13 01:55) or `recheck_status='tightened'` —
  outcomes decided by a moved stop, not by the entry.

```
all closed positions                                       49
with the CORRECTED metric (entry after 07-04 11:58)        17   vpos 65-81
AND uncontaminated                                          7   vpos 75, 76, 77, 78, 79, 80, 81
```

**Seven. That is the entire evidence base for both angles.**

| vpos | side | vol5m | PnL | exit | score | MTF | ADX-1h |
|---|---|---|---|---|---|---|---|
| 75 | LONG | 0.53 | -14.52 | external | 4.00 | 4 | 34.2 |
| 76 | SHORT | 1.38 | +45.36 | external | 6.00 | 3 | 21.3 |
| 77 | SHORT | 3.51 | -132.75 | sl | 2.25 | 4 | 30.3 |
| 78 | LONG | 5.01 | -103.54 | sl | 2.50 | 4 | 25.1 |
| 79 | LONG | 3.18 | +80.10 | trail | 4.25 | 4 | 21.7 |
| 80 | SHORT | 2.98 | -116.58 | sl | 4.00 | 4 | 30.4 |
| 81 | SHORT | 1.54 | +75.24 | trail | 2.50 | 4 | 20.5 |

## Angle (a) — the entry-book logger

```
SHORT, clean + corrected:  n=4  (2 winners, 2 losers)
   winners: 1.38, 1.54        losers: 2.98, 3.51
   separation: CLEAN, no overlap
   Fisher at a 2.0 threshold: p = 0.333
```
The separation is still perfect — **on two trades against two.** Perfect separation of 2 and 2 has a
one-in-six chance of happening by coin flip. **p = 0.333.**

The originally quoted **p = 0.048 at n=7** counted vpos **66, 68 and 74** — and all three are
contaminated (66 and 68 inside the wall-trail window, 74 carrying the recheck TIGHTEN whose stop
move is what closed it). The significance came entirely from rows whose outcome the entry did not
determine.

Outlier test: drop the single best and single worst trade and the SHORT cohort is **one winner
(1.38) against one loser (2.98)**. There is nothing left to test.

```
LONG, clean + corrected:  n=3  (1 winner, 2 losers)
   winner: 3.18            losers: 0.53, 5.01
   OVERLAPPING — and the sole winner has HIGHER volume than one of the losers
```
**LONG points the opposite way.** The one winning long entered on 3.18× volume; a loser entered on
0.53×. Whatever the short side shows, the long side does not show it — which is the mandatory
side-split the brief asked for, and it fails.

## Angle (b) — the SL-death comparison from tonight

This was the second, "independent" confirmation. It is not independent, and it is not clean:

```
as computed tonight (whole book):   SL n=25 median 2.42   ·   trail n=14 median 0.95
corrected metric AND uncontaminated: SL n=3  (77, 78, 80)  ·   trail n=2  (79, 81)
     SL vol5m:    3.51, 5.01, 2.98
     trail vol5m: 3.18, 1.54
```
**Of the 25 SL deaths, three have a usable measurement. Of the 14 trail exits, two.** And those five
are a subset of the same seven above — so angle (b) is not a second look at the question, it is the
same four data points re-sorted by exit reason. The 2.54-vs-0.95 gap was computed almost entirely on
the pre-07-04 corrupted metric.

I reported that comparison tonight without checking the metric's validity window. That was my error,
and it is corrected here.

## Confounding

On the clean seven, `vol_ratio_5m` correlates **r = -0.48 with confluence score**, r = -0.10 with
ADX-1h, r = +0.28 with the 1h volume ratio. The score correlation is the notable one: high-volume
entries also tend to be low-score entries — i.e. the volume signal partly overlaps something the
score gate already sees. At n=7 that correlation is itself untrustworthy, but it is the right thing
to look at when the sample eventually exists.

---

## Verdict

**Not a real, side-specific, structurally-sound effect on the current evidence. It is a third
aggregate artifact.**

* **SHORT:** direction is right, sample is 2 vs 2, p = 0.333, and one trade removed either way ends
  the test. Suggestive, nothing more.
* **LONG:** contradicts, on n=3.
* **The two "independent" angles are the same seven positions.**

**Nothing is built. No diff, no A/B arm, no threshold, no config flag.** The A/B design in the brief
is sound and should be used when this is revisited — the point about the counter-short caution being
unmeasurable because it only fired on overdetermined setups still holds, and a volume caution on
otherwise-fine TREND entries genuinely would be measurable. But there is nothing yet to A/B.

**What would change the answer:** ~8-10 clean, correctly-measured SHORT closes with a mix of winners
and losers. Current count: 4. At roughly one short close every four days, **6-10 weeks** — and only
if the wall-trail and recheck fixes shipped today hold, since it was contamination that inflated the
original figure.

The entry-book logger and the `volfloor` sensor keep running unchanged. They are doing their job;
the cohort simply is not ready, and the sensor's own firing threshold (6 per side) counts rows the
decontamination removes. **That threshold should count CLEAN rows** — noted for the sensor, not
acted on here.

---

## Recorded in OPEN-ITEMS

Review date for this statistic, so it cannot go stale the way the counter-short one did: **re-cut at
~10 clean corrected SHORT closes, and in any case no later than 2026-09-30.** If the cohort has not
reached n by then, the finding expires rather than waiting indefinitely.

---

Nothing applied. Tree clean at `ef7fa10`; `titan.service`, `nginx` and `mercury-sol.service` healthy.
