# state-verify-and-counterfactual

_2026-07-26 23:53 UTC_

---

# TITAN — state verification + counterfactual replay of today's fixes

**2026-07-26 23:55 UTC.** State check APPLIED (one push). Counterfactual READ-ONLY.

**The counterfactual result is the opposite of what I expected, and it corrects an earlier claim of
mine. On the subset that can actually be resolved, the moved stops SAVED money: -190.53 actual vs
-526.38 replayed, Δ -335.84.** Detail in §2.

---

# 1. State verification

| # | check | result |
|---|---|---|
| a | `git status` | **clean**, 0 changes |
| b | today's commits pushed | **🔴 NONE were pushed — origin/main was still at `6c35b9d`.** Pushed now: `6c35b9d..d12e276`, all six commits (incl. superseded `596fbdf`) verified present on origin |
| c | service running current code | PID 3226328, started **22:07:02**; last code write **22:06:59** — the running process post-dates the last edit |
| d | flags live at runtime | `LONG_PARTIAL_ENABLED=True` (1.0R, 1/3) · `EXIT_ADVISOR_PAPER_ENABLED/DRYRUN/ON_15M_CONFIRM/HOURLY = True` · `CONFLUENCE_FLAT_THRESHOLD=5.0` · `WALL_TRAIL_LIVE_ENABLED=False` · `ADX_BELOW_FLOOR=20.0` · `LIVE_TRADING_ENABLED=False` · `_tighten_sl` has **2** original-SL clamps, `original_sl=None` signature and the call site passes `original_sl=_orig_sl` |
| e | crontab matches `d12e276` | 4 Titan lines (bull-regime, chop-short, flat-high-adx, volfloor); 0 retired Titan sensors. One line matched my grep — `mercury_sol_prior_move_logger`, which is **SOL's** and was correctly left alone |
| f | nginx noquery active | format declared and applied; of all post-reload `/webhook` lines, **0 contain a query string** |

**(b) is the finding.** Everything was committed and nothing was pushed — the whole day's work
existed only on this box. Now on origin.

---

# 2. Counterfactual replay

Method: forward simulation of each position's management path — walk the excursion samples, then the
post-exit drift samples, with the stop **never moved below the original**, checking at each point for
(1) original SL hit, (2) +1R → breakeven + trail, (3) trail trigger. No arithmetic on endpoints.

## What is in scope

```
candidates (recheck TIGHTEN or lifetime overlapping the wall-trail window)   18
  with excursion path data                                                  13
  EXCLUDED — no path data (vpos 46, 47, 53, 55, 57), actual PnL +98.38       5
```

## What the replay could actually resolve

Of the 13, only **5 reached a genuine terminal condition** inside the available data. The other 8
ran out of data 25-43h in with the position still open — marking them to the last known price is
**not an exit**, so they are excluded rather than counted.

| vpos | side | actual | replayed | Δ | at | terminal condition |
|---|---|---|---|---|---|---|
| 66 | SHORT | -59.11 | -115.49 | **-56.38** | 17.3h | original SL |
| 67 | LONG | -32.73 | -128.31 | **-95.58** | 13.8h | original SL |
| 68 | SHORT | -4.52 | +10.00 | +14.52 | 3.4h | breakeven/trail |
| 69 | LONG | -50.64 | -191.16 | **-140.53** | 12.1h | original SL |
| 73 | LONG | -43.54 | -101.42 | **-57.88** | 29.2h | original SL |

```
LONG    n=3   actual -126.90  ->  replayed -420.89   Δ -293.98
SHORT   n=2   actual  -63.63  ->  replayed -105.49   Δ  -41.86
TOTAL   n=5   actual -190.53  ->  replayed -526.38   Δ -335.84
```

**Four of the five went on to hit the original stop anyway — and lost more, because the original
stop is further away.** Only vpos 68 was saved.

## This corrects an earlier claim of mine

Earlier today I reported that **"11 of 11 would have survived at their original SL"**, based on
`max_adverse_price` never reaching it. That was true **only up to the moment the position was
actually closed** — which is exactly when `max_adverse_price` stops being recorded. Carrying the
path forward past that point, price kept going and reached the original stop in four of the five
resolvable cases.

The moved stop was still wrong — it fired on noise, without evidence, and its trigger has been
removed. But **"they would all have survived" was an artefact of a metric that stops at the close.**
On this evidence the moved stops cut losses that would otherwise have been larger.

## What cannot be computed, and is not estimated

| item | why not |
|---|---|
| 8 of 13 replays | data ends 25-43h in, position still open. Actual PnL **-379.29** stands unchanged; the effect is unknown |
| 5 candidates without path data (46, 47, 53, 55, 57) | `position_excursion_samples` only covers vpos 61+. Actual **+98.38** stands |
| **counter-short retirement (`b878535`)** | a soft caution. Which of the 38 skips would have become entries is unknowable. **Not estimated** |
| **exit advisor** | dryrun, never ran historically. The 27-moment / 6-position backtest is a plausibility check and is **not extrapolated** |
| **15m persistence (`ef7fa10`)** | no PnL effect by construction |

## B. LONG partial — restated, not re-derived

The clean-sample simulation gave **-343.10 → -248.28 (+94.83)** on 10 clean longs, 0 winners cut.
It **cannot be extended** to the positions above: they are the contaminated set, which the clean-sample
study excluded by definition, and their replays are either unresolved or terminate at the original
stop before +1R. On the 5 resolved positions the partial changes nothing — none reached +1R.

## C. Combined

A and B on the same replay: **identical to A, Δ -335.84**, because no resolved position reached +1R
and the partial therefore never fires.

---

## Bottom line — stated without mixing computed and assumed

```
COMPUTED, n=5 resolved positions:
   actual   -190.53
   replayed -526.38
   Δ        -335.84     the recheck-bound fix would have LOST money on these five

NOT COMPUTED:
   8 positions, actual -379.29   — replay unresolved
   5 positions, actual  +98.38   — no path data
   counter-short retirement       — unknowable
   exit advisor                   — dryrun, no history
   15m persistence                — no PnL effect
```

**There is no headline number for "the book with today's fixes", and I will not manufacture one.**
Five positions out of 49 are replayable to a real conclusion. On those five the answer is negative,
which is worth knowing precisely because it runs against the story the day has been telling.

That does not argue for restoring the wall-trail or the recheck TIGHTEN. Both moved stops **on
evidence that did not exist** — a wall multiple that oscillated 17→8→11 in five minutes, and a
single ADX reading. A rule that cuts losses by accident is still a rule with no edge, and the
forward test that matters is the one now running: the exit advisor, in dryrun, against a criterion
recorded before any data existed.

---

Applied: `git push` only. Tree clean at `d12e276`, origin in sync. `titan.service`, `nginx`,
`mercury-sol.service` healthy.
