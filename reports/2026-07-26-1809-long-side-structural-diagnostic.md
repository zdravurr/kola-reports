# long-side-structural-diagnostic

_2026-07-26 18:09 UTC_

---

# TITAN — LONG side, full structural diagnostic

**2026-07-26 · READ-ONLY. Nothing changed, no thresholds proposed.** Tree clean at `b878535`.
Paper mode. Goal is to repair the long side, not to disable it.

**Headline: the long side is NOT handicapped by construction. Every mechanical parameter is
within noise of the short side. Two real defects were found instead — one already fixed today, one
still open — and the "no bull market" excuse survives in a narrower and more useful form.**

Single most important number: **10 of the 15 LONG stop-outs died on a stop the machinery had
MOVED, not on their original stop. That is -515.13 of the -856.48 book — 60% of the entire long-side
loss.** Both causes (wall-trail, recheck TIGHTEN) were shipped fixed earlier today.

---

## 1. Anatomy — all 21 closed LONGs

MFE / MAE are computed from `water_mark` / `max_adverse_price` vs the fill. `SLd%` is the ORIGINAL
stop distance. `hrs` is time held.

| vp | opened | closed | hrs | scr | regime | 1d | 4h | 1h | MTF | exit | MFE% | MAE% | SLd% | PnL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 35 | 05-24 00:50 | 05-25 19:05 | 42.2 | 2.2 | — | — | neutral | bull | 3 | external | 1.35 | n/a | 1.44 | +0.62 |
| 37 | 05-25 20:45 | 05-26 02:46 | 6.0 | 4.2 | — | — | bull | neutral | 1 | sl | 0.24 | n/a | 0.94 | -104.59 |
| 39 | 05-26 09:05 | 05-26 12:08 | 3.1 | 3.8 | — | — | neutral | bear | 0 | trail | 1.20 | n/a | 0.93 | +15.53 |
| 41 | 05-26 13:55 | 05-26 16:12 | 2.3 | 2.5 | — | — | neutral | neutral | 0 | sl | 1.12 | -1.30 | 1.23 | -139.51 |
| 45 | 05-28 12:25 | 05-29 18:52 | 30.4 | 6.0 | TREND | — | bear | bear | 0 | sl | 1.42 | -1.01 | 1.33 | +5.34 |
| 54 | 06-11 11:25 | 06-13 16:30 | 53.1 | 4.2 | TREND | bear | bull | bull | 4 | external | 1.94 | -1.28 | 1.67 | +117.71 |
| 55 | 06-15 00:15 | 06-15 01:04 | 0.8 | 4.2 | TREND | neutral | bull | bull | 4 | sl | 0.02 | -0.69 | 1.35 | -78.70 |
| 59 | 06-25 07:20 | 06-25 13:40 | 6.3 | 3.8 | TREND | bear | neutral | bull | 3 | sl | 0.17 | -1.92 | 1.90 | -201.83 |
| 62 | 07-02 13:20 | 07-03 02:30 | 13.2 | 2.2 | TREND | neutral | bull | bull | 4 | sl | 0.71 | -0.96 | 1.91 | -72.79 |
| 63 | 07-03 05:50 | 07-03 09:01 | 3.2 | 3.5 | FLAT | neutral | bull | bull | 4 | sl | 0.28 | -0.35 | 1.56 | -45.57 |
| 64 | 07-03 20:10 | 07-04 01:30 | 5.3 | 4.0 | TREND | neutral | bull | bull | 4 | external | 0.88 | -0.05 | 1.29 | +3.32 |
| 65 | 07-04 18:00 | 07-04 23:13 | 5.2 | 7.8 | TREND | neutral | bull | bull | 4 | sl | 0.29 | -0.31 | 1.00 | -41.35 |
| 67 | 07-05 22:35 | 07-06 00:24 | 1.8 | 3.5 | FLAT | neutral | bull | bull | 4 | sl | 0.61 | -0.23 | 1.18 | -32.73 |
| 69 | 07-06 21:10 | 07-06 21:15 | 0.1 | 3.8 | TREND | neutral | bull | bull | 4 | sl | 0.15 | -0.41 | 1.81 | -50.64 |
| 70 | 07-09 21:10 | 07-09 23:16 | 2.1 | 3.8 | TREND | neutral | bull | bull | 4 | sl | 0.08 | -0.34 | 1.45 | -44.42 |
| 71 | 07-10 01:50 | 07-10 20:26 | 18.6 | 2.5 | TREND | **bull** | bull | bull | 4 | sl | 1.37 | -0.21 | 1.57 | -30.78 |
| 72 | 07-11 14:25 | 07-11 15:37 | 1.2 | 4.2 | TREND | **bull** | bull | bull | 4 | sl | 0.22 | -0.65 | 0.75 | -74.61 |
| 73 | 07-11 17:35 | 07-11 22:49 | 5.2 | 7.5 | TREND | **bull** | bull | neutral | 3 | sl | 0.11 | -0.34 | 0.91 | -43.54 |
| 75 | 07-14 21:35 | 07-15 02:00 | 4.4 | 4.0 | TREND | **bull** | bull | bull | 4 | external | 0.60 | -0.25 | 1.37 | -14.52 |
| 78 | 07-20 00:15 | 07-20 00:52 | 0.6 | 2.5 | TREND | **bull** | bull | bull | 4 | sl | 0.08 | -0.94 | 0.87 | -103.54 |
| 79 | 07-20 15:45 | 07-22 06:21 | 38.6 | 4.2 | TREND | **bull** | bull | bull | 4 | trail | 2.54 | -0.37 | 1.59 | +80.10 |

MAE is unavailable for vpos 35/37/39 — the field was seeded at the entry price before MAE tracking
existed, so those three read 0.00 and are excluded from MAE statistics rather than counted as zero.

---

## 2. How they die — and it is mostly NOT the entry

Exit reasons: **LONG** sl=15 · external=4 · trail=2. **SHORT** trail=12 · sl=10 · external=5 ·
post_entry_critical=1. (Longs almost never reach a trailing exit: 2/21 vs 12/28.)

Decomposing the 15 LONG stop-outs by whether price actually reached the ORIGINAL stop:

| cause | n | vpos | net |
|---|---|---|---|
| **genuine original stop hit** | 3 | 41, 59, 78 | **-444.88** |
| breakeven/trail after +1R (working as designed) | 1 | 45 | +5.34 |
| **stop MOVED by the machinery, price never reached the original** | **10** | 55, 62, 63, 65, 67, 69, 70, 71, 72, 73 | **-515.13** |
| MAE data unavailable | 1 | 37 | -104.59 |

All 10 machinery deaths carry wall-trail or recheck-TIGHTEN exposure. **60% of the long side's
total loss came from stops that were tightened underneath live positions.**

> Method note, and a correction to my own earlier filtering: exposure must be judged by whether the
> position's **lifetime overlaps** the wall-trail window (07-02 23:28 – 07-13 01:55), not by its
> entry time. The wall-trail moved stops on positions that were already open. Filtering by entry
> time missed vpos 62, which entered at 13:20 and was still open when the ratchet went live at 23:28.
> Under the corrected filter: **LONG 11/21 positions machinery-touched (-511.80), SHORT 7/28 (+40.36).**

Were they wrong immediately, or right first? MFE says both problems exist:
```
LONG losers  n=15  MFE median 0.24%  mean 0.40%  max 1.37%   reached +1R: 0/15
LONG winners n= 6  MFE median 1.38%  mean 1.55%
SHORT losers n=12  MFE median 0.38%  mean 0.69%  max 1.72%   reached +1R: 1/12
SHORT winners n=16 MFE median 3.16%  mean 3.09%
```
**Losing longs and losing shorts look the same** — both are wrong almost immediately. The sides
diverge entirely in their **winners**: a winning short runs 3.09% on average, a winning long 1.55%.

**Verdict: this is BOTH a stop/exit problem AND a weak-entry problem, but they are separable.**
The stop problem is the larger one and is already fixed. The entry problem is real but of a
different shape than expected — see §5.

---

## 3. Winners vs losers — nothing separates them

Winners: vpos 35, 39, 45, 54, 64, 79 (n=6). Losers: n=15. Every continuous entry field **overlaps**:

| field | W mean | W range | L mean | L range |
|---|---|---|---|---|
| confluence_score | 4.083 | [2.25, 6.00] | 4.000 | [2.25, 7.75] |
| mtf_alignment_score | **2.500** | [0, 4] | **3.400** | [0, 4] |
| srv_adx_1h | 31.22 | [21.8, 44.3] | 27.45 | [20.8, 42.0] |
| srv_adx_15m | 28.90 | [19.5, 45.1] | 32.05 | [14.2, 51.3] |
| srv_vol_ratio_5m | **1.271** | [0, 3.18] | **3.141** | [0, 10.69] |
| srv_vol_ratio_1h | 0.607 | [0.07, 1.81] | 0.947 | [0.24, 3.25] |
| ema_gap_pct_1h | 0.404 | [0.11, 0.68] | 0.325 | [0.00, 0.89] |
| ai_confidence | 0.707 | [0.62, 0.78] | 0.753 | [0.62, 0.87] |
| macro_confidence | 0.803 | [0.78, 0.85] | 0.639 | [0.00, 0.92] |

**Say it plainly: no entry field separates winning longs from losing ones.** Not score, not ADX,
not ATR, not volume, not EMA-gap, not advisor confidence.

The categorical breakdown contains something worse than "no signal" — a **sign inversion on the
machinery's own alignment criteria**:
```
trend_4h        W: bull 3 / neutral 2 / bear 1     L: bull 13 / neutral 2
trend_1h        W: bull 4 / bear 2                 L: bull 12 / neutral 3
trend_15m       W: bull 4 / neutral 2              L: bull 13 / bear 1 / neutral 1
ema_status_1h   W: Bullish 4 / Bearish 2           L: Bullish 14 / Bearish 1
MTF alignment   W mean 2.50                        L mean 3.40
```
**The more bullish-aligned the setup, the more often the long lost.** Two of the six winners were
taken with `trend_1h = bear`. At n=6 winners this is suggestive, not proven — but it points the same
way as §4 and it is the opposite of what the machinery assumes.

---

## 4. The bull-regime failure — and what it actually was

Six longs entered under `trend_1d = 'bull'`, net **-186.89**, 1/6 win.

| vpos | score | MTF | 4h/1h/15m | ADX 1h/15m | vol5m | MFE | +1R | book at entry | PnL |
|---|---|---|---|---|---|---|---|---|---|
| 71 | 2.50 | 4 | bull/bull/bull | 25.1 / 22.2 | 9.12 | 1.37% | no | opp wall 0.016% above, sup 0.159% below | -30.78 |
| 72 | 4.25 | 4 | bull/bull/bull | 28.8 / 33.6 | 4.79 | 0.22% | no | opp wall 0.064% above | -74.61 |
| 73 | 7.50 | 3 | bull/neutral/bull | 24.0 / 30.5 | 3.28 | 0.11% | no | opp wall 0.044% above | -43.54 |
| 75 | 4.00 | 4 | bull/bull/bull | 34.2 / 41.4 | 0.53 | 0.60% | no | opp wall 0.048%, sup mult 16.0 | -14.52 |
| 78 | 2.50 | 4 | bull/bull/bull | 25.1 / 28.6 | 5.01 | 0.08% | no | opp wall 0.038% above | -103.54 |
| **79** | 4.25 | 4 | bull/bull/bull | **21.7 / 21.0** | 3.18 | **2.54%** | **YES** | imbalance **0.892**, only 2 ask walls | **+80.10** |

Four things stand out, and none of them is "bad setups":

1. **They were textbook-perfect by the machinery's own criteria.** MTF 4/4 on five of six, ADX
   21-34, expanding EMA gaps, and the advisor's own words: *"Multi-TF BULL alignment (1d-5m), ADX
   strong, Expanding EMA-gaps, Volume 4.79x, no opposing wall at entry."* Five of those six lost.
2. **Half were killed by the machinery, not the market.** 3 of 6 carry wall-trail / recheck-TIGHTEN
   exposure. **Excluding them, the bull cohort is -37.95 over 3 trades, not -186.89 over 6.**
3. **The one winner is the odd one out in exactly the direction §3 suggests** — vpos 79 had the
   *lowest* ADX (21.7 vs 24-34) and by far the highest order-book imbalance (0.892), and it is the
   only one that reached +1R.
4. **The window was not a bull market.** `trend_1d='bull'` covered 15 calendar days in which BTC
   went from ~63,788 to ~65,254 — **+2.3%, with the entire range about 2.3%**. That is a drift
   inside a range, labelled "bull" by a daily EMA. Control: **shorts in the same window lost too**
   — n=5, **-201.82**. Neither side worked; it was a chop window, not a long-side failure.

**So the "no bull market" excuse is not dead — it was stated too loosely.** The correct statement:
*Titan has still never traded a real daily uptrend. What it traded in July was a 2.3% range with a
bull label, and both sides lost in it.*

---

## 5. Mechanical asymmetry — the key question, answered: NO handicap by construction

| parameter | LONG | SHORT |
|---|---|---|
| stop distance, % of entry | med 1.347 · mean 1.336 | med 1.379 · mean 1.532 |
| ATR-1h, % of price | med 0.546 · mean 0.533 | med 0.543 · mean 0.621 |
| **stop in ATR-1h units** | **med 2.491 · mean 2.502** | **med 2.515 · mean 2.449** |
| step margin, USDT | med 2000 · mean 1906 | med 2000 · mean 1789 |
| leverage | med 5.0 | med 5.0 |
| initial risk, USDT | med 133.1 · mean 126.7 | med 136.9 · mean 149.6 |
| trail_pct | med 1.347 | med 1.379 |
| confluence score at entry | med 3.75 · mean 4.02 | med 4.00 · mean 4.29 |
| MTF alignment | mean 3.14 | mean 3.14 |
| signal types | `open_long` ×21 | `open_short` ×28 |

Gate throughput over the whole signal stream (since 2026-05-21):
```
                  HTF cascade passed     threshold passed      ADVISOR approved
LONG    5,603 sig   1,530/5,569 = 27.5%   1,173/1,530 = 76.7%   22/1,173 = 1.88%
SHORT   6,560 sig   1,818/6,485 = 28.0%   1,360/1,818 = 74.8%   31/1,360 = 2.28%
                                              advisor LONG vs SHORT: Fisher p=0.4907
```

**Every mechanical parameter is within noise. Sizing, leverage, risk, stop geometry, trail, the
cascade, the score threshold and the advisor all treat the two sides the same.** The long side is
not being starved, under-sized, stopped tighter, or vetoed more often. That hypothesis is dead, and
that is worth knowing — it removes a whole class of proposed fixes.

**The asymmetry is entirely in what the two sides ACHIEVE:**
```
MFE in R units (MFE / original stop distance)
   LONG   median 0.38R   reached >=1R: 19%   reached >=2R:  0%
   SHORT  median 0.93R   reached >=1R: 46%   reached >=2R: 29%

MFE in %          LONG p25 0.17 · med 0.60 · p75 1.20 · max 2.54
                  SHORT p25 0.50 · med 1.48 · p75 3.16 · max 6.58

holding time      LONG  median 5.2h   winners median 34.5h
                  SHORT median 8.4h   winners median 10.5h
```
**A single stop geometry (~2.5× ATR-1h) is applied to both sides, but longs realise only 0.38R of
favourable excursion against the shorts' 0.93R.** The stop is not *tighter* for longs — it is sized
for an excursion distribution that longs do not produce. No long in the entire book has ever
reached 2R; 29% of shorts have. And winning longs need **3.3× longer** to work (34.5h vs 10.5h)
while being held for a *shorter* median time overall (5.2h vs 8.4h).

### Clean picture, machinery contamination removed
```
LONG   n=10  net  -344.68  win 5/10  PF 0.39
SHORT  n=21  net +1555.52  win 14/21 PF 3.66
```
The long side is still negative once the machinery damage is removed — so this is not *only* a
machinery story. But it is a **-345 problem, not an -856 problem**, and its win rate is 50%.

---

## 6. Fixable defects, ranked by expected value

**None of these is "turn the long side off". All are repairs.** No thresholds are proposed —
each needs its own validation pass with the decomposition discipline we applied to R2 and R5.

**D1 — Stops tightened underneath live longs. -515.13, 10 of 21 positions. ALREADY FIXED TODAY.**
The largest single item in the entire diagnostic, and it required no new work: wall-trail was
disabled 07-13 (`5f1b073`), the phantom-wall recheck trigger zeroed 07-13 (`c845941`), and the
recheck TIGHTEN was bounded at the original stop distance today (`93c20c3`). **Action: none —
verify it stays fixed by re-running this decomposition after ~10 more long closes.** Longs were hit
roughly twice as often as shorts by this (11/21 vs 7/28), so the fix is worth more to the long side.

**D2 — Long-side exit geometry does not match long-side excursion. Est. large, needs design work.**
Longs realise 0.38R median MFE and have *never* reached 2R, yet carry a 2.5×ATR stop and a
trail_pct equal to the stop distance. The consequence is visible in the exit mix: **2/21 longs ever
reached a trailing exit vs 12/28 shorts**. This is the one place where "the same treatment" is
itself the defect — symmetric geometry on asymmetric behaviour. **Action: study whether the long
side needs a different exit contract (earlier partial, different trail arming, a target rather than
a trail), measured on the clean 10-position sample plus new closes. Do not guess a multiplier.**

**D3 — Entry criteria are anti-predictive on longs. Est. medium, evidence suggestive not proven.**
Nothing separates winning from losing longs (§3), and the machinery's alignment measures lean the
*wrong* way: losers have higher MTF alignment (3.40 vs 2.50), more `trend_4h/1h/15m = bull`, more
`ema_status_1h = Bullish`. The bull-regime cohort (§4) is the same story at maximum intensity —
five textbook 4/4-aligned setups, five losses, and the sole winner had the lowest ADX and the
highest book imbalance. **Action: treat "MTF alignment is bullish" as an unvalidated input on the
long side and test it explicitly, as its own hypothesis, against the clean sample. n=6 winners is
too thin to act on now.**

**D4 — Winning longs need far longer than losing longs are given. Est. medium.**
Winners held 34.5h median, but the overall long median is 5.2h and the shortest stop-outs died in
0.1h, 0.6h and 1.2h. Combined with 0/15 losers reaching +1R, the picture is longs being taken on
5m triggers and resolved before the thesis can play out. **Action: study time-to-1R for longs
specifically; this is measurable from `position_excursion_samples` (2,205 rows, 22 positions)
without any new instrumentation.**

**D5 — Entry into immediate overhead supply. Est. small-medium, data now exists.**
In the bull cohort every loser had an opposing ask wall **0.016–0.064% above entry** — essentially
touching the fill — while the sole winner had only 2 ask walls and an imbalance of 0.892. The
always-on order-book collector now has **19,000+ snapshots** for a percentile baseline, but only
9 entries overlap it. **Action: wait — this is the same "needs n" case as the audit's W3. Re-cut
when ~15-20 entries have book data.**

**D6 — `max_adverse_price` unavailable on early positions. Est. small, pure instrumentation.**
vpos 35/37/39 carry MAE seeded at the entry price, which silently reads as 0.00 and would corrupt
any automated MAE statistic. **Action: exclude explicitly in analysis (done here); consider a
NULL-vs-seed distinction in the schema so this cannot be misread later.**

### What is NOT a defect
Sizing, leverage, risk per trade, stop distance in ATR units, trail parameter, HTF cascade pass
rate, score threshold pass rate, advisor approval rate, and signal-type coverage. All measured, all
symmetric, all cleared. **The long side is not being handicapped by the machinery — it is being
given the short side's exit contract for a different excursion distribution, and its entry
criteria have never been validated on their own.**

---

Nothing was applied. Session commits: `93c20c3` (R1 recheck bound), `596fbdf` (superseded),
`b878535` (counter-short caution retired). `titan.service` healthy, Mercury-SOL untouched.
