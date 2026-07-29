# titan-market-regime-label-study-can-it-be-redefined

_2026-07-29 10:55 UTC_

---

**READ-ONLY STUDY. Nothing was changed, nothing is proposed.** HEAD `8b15ecc`, `git status` clean,
`titan.service` untouched.

**VERDICT UP FRONT (§6 in full below).** The label really is a poor measure of the tape — but the
answer to "is there a better one?" is **no, not provably.** Four candidate definitions were built
from data the bot already has and tested on real candles. Three of them (`ADX≥25`, `|net|/range≥.5`,
a 2-of-3 vote) would have **lost** money on both sides of the change. The fourth looks good on the
endpoint statistic and **stops looking good the moment the price path and signal clustering are
handled honestly** — its result straddles zero. And the fact that matters most:

> 🔴 **All four candidate definitions still take vpos 83.** At that moment the tape genuinely *was*
> trending — ADX(1h) 25.8, |net|/range 0.72 over 12h, ATR 1.18× its 14-day median, EMA-gap
> Expanding. The label was right for the wrong reason. **Redefining it would not have prevented the
> trade that motivated this study.**

---

## 0. METHOD, AND ONE CORRECTION TO THE 10:11 REPORT

**Independent tape metrics.** Every tape measure here is recomputed from **real OKX OHLCV**
(2,700 1H bars, 1,200 4H bars, 2,700 15m bars) — Wilder ADX(14), ATR(14), EMA 9/21 gap, and
|net move|/range — evaluated on the **last fully CLOSED bar at or before** each timestamp. No
look-ahead, and no stored bot column is used as a tape measure.

Validated against the bot's own stored columns on 400 random rows: ADX(1h) median difference
**−0.006**, ADX(4h) **−0.129**, EMA-gap **+0.002**; |diff| > 5 in 0.8% of rows. The stored columns
are accurate — the reconstruction is not correcting them, it is making them independent and
look-ahead-free.

**§0 contamination filters applied.** All four, and where a filter does not apply I say so rather
than cargo-culting it:
- *Forming-candle* (`≥ 2026-07-04 11:58`): applied to every closed-trade statistic. It targets
  `srv_vol_ratio_5m`, which this study never reads — but the whole Q4 pool falls after that date
  anyway (earliest 2026-07-06), so it binds nothing there.
- *Wall-trail lifetime OVERLAP* — tested as overlap, not entry time, exactly as §0 warns.
- *Recheck TIGHTEN* excluded.
- *Excursion truth* — **no stored extremum is used anywhere in this report.** Every path question is
  answered on real 15m candles (§4).

**Sign convention** honoured: skip-drift **positive = the skipped signal would have won**.

**Populations.** `skip_attribution` turns out to store `market_regime` **including on
`below_threshold` rows** — 7,686 rows with drift at 15m/1h/4h/12h/24h. That closes **carry-forward
#4** of the 10:11 report: the gating question does *not* need reconstructing from
`matrix_breakdown_json`; the column exists, just in a different table.

| population | n | what it is |
|---|---|---|
| **Score-gate** | **2,679** | `ai_skipped` + `below_threshold` + `executed` — reached the 2.0/5.0 bar |
| **All rows** | **7,728** | + `htf_blocked` (5,049) — blocked *before* the score gate |
| **Clean closed trades** | **9** | all four §0 filters |

### 🔴 Correction to the 2026-07-29 10:11 report

That report stated ADX(1h) was **26.66 under FLAT vs 25.52 under TREND**, i.e. *anti*-correlated.
**That figure reproduces exactly** — but it was a 14-day, 387-row slice of the `trades` table, and
it was **never significant (Welch t = −1.18)**. On the full population the sign is the other way:

| window (skip_attribution, reconstructed ADX) | TREND | FLAT | diff | t |
|---|---|---|---|---|
| from 2026-06-01 (n=7,725) | 25.96 | 24.37 | **+1.59** | +9.02 |
| from 2026-07-01 (n=5,325) | 26.93 | 25.38 | +1.55 | +7.42 |
| from 2026-07-15 (n=2,423) | 25.96 | 24.43 | +1.53 | +4.93 |

The difference is the **population, not the window**: the `trades` table omits `below_threshold`
rows, which are overwhelmingly FLAT *and* low-ADX, so dropping them lifts the FLAT mean.
**"The label barely tracks the tape" survives. "Anti-correlated" does not — I withdraw it.**

---

## 1. HOW BADLY IS IT WRONG — the confusion matrix

Each independent criterion, cross-tabulated against the live label. "TREND wrong" = share of
TREND labels sitting on a tape that criterion calls ranging; "FLAT wrong" = share of FLAT labels on
a trending tape.

### Score-gate population (n = 2,679; label: TREND 1,096 / FLAT 1,583)

| independent criterion | TREND&trend | TREND&range | FLAT&trend | FLAT&range | **TREND wrong** | **FLAT wrong** | agree |
|---|---|---|---|---|---|---|---|
| ADX(1h) ≥ 25 | 556 | 540 | 733 | 850 | **49.3%** | **46.3%** | 52.5% |
| ADX(4h) ≥ 25 | 438 | 658 | 711 | 872 | **60.0%** | **44.9%** | 48.9% |
| \|net\|/range 12h ≥ .50 | 361 | 735 | 542 | 1041 | **67.1%** | **34.2%** | 52.3% |
| \|net\|/range 24h ≥ .50 | 495 | 601 | 708 | 875 | **54.8%** | **44.7%** | 51.1% |
| ATR(1h) ≥ 14d median | 326 | 770 | 423 | 1160 | **70.3%** | **26.7%** | 55.5% |
| EMA-gap 1h Expanding | 509 | 587 | 613 | 970 | **53.6%** | **38.7%** | 55.2% |

**Between half and seven-tenths of TREND labels sit on a ranging tape. Between a quarter and a
half of FLAT labels sit on a trending one. Agreement is 49–56% — coin-flip.**

### The consensus view — and the cleanest single number in this study

Counting how many of the six independent criteria call each moment "trending":

| votes (0–6) | TREND-labelled | FLAT-labelled | TREND share |
|---|---|---|---|
| 0 | 53 | 129 | 29.1% |
| 1 | 236 | 280 | 45.7% |
| 2 | 304 | 410 | 42.6% |
| 3 | 275 | 495 | 35.7% |
| 4 | 144 | 206 | 41.1% |
| 5 | 64 | 57 | 52.9% |
| 6 | 20 | 6 | 76.9% |

> **Mean votes: TREND-labelled 2.000. FLAT-labelled 2.000.** Identical to three decimals — and
> identical again, independently, on the 7,728-row population. A moment the bot calls TREND has, on
> average, *exactly* as much independent evidence of trending as a moment it calls FLAT.

There is a faint real signal at the extremes (6/6 votes → 77% TREND-labelled; 0/6 → 25%), but those
cells hold 26 and 182 rows.

### Effect size — the honest version

The correlation is not zero, it is **negligible**:

| population | Cramér's V (label × ADX≥25) | point-biserial r, ADX(1h) | best tape predictor of the label |
|---|---|---|---|
| score-gate, n=2,679 | **0.0435** | +0.072 | — |
| all rows, n=7,728 | **0.0661** | +0.101 | 61.6% accuracy vs a 59.1% always-guess-FLAT baseline = **+2.5 points** |

At n=7,728 a Welch t of +9.04 on ADX is easy to reach and means nothing about magnitude: the label
explains **under 1%** of the variance in any tape measure. Searching every threshold on every one of
the six metrics, the best possible tape-based *prediction of the label itself* beats doing nothing
by two and a half percentage points.

**Answer to Q1: the label is not measuring the tape. It is not inverted either — it is
uninformative.**

---

## 2. DOES THE LABEL PREDICT OUTCOMES — NOT COMPUTABLE, AND THAT IS THE FINDING

| filter step | n |
|---|---|
| all closed positions with a regime label | 41 |
| + forming-candle (≥ 07-04 11:58) | 19 |
| + wall-trail lifetime overlap | 10 |
| + recheck TIGHTEN excluded → **CLEAN** | **9** |

| label | n | win rate | net | mean | median |
|---|---|---|---|---|---|
| **TREND** | **9** | 4/9 = 44.4% | **−256.56** | −28.51 | −14.52 |
| **FLAT** | **0** | — | — | — | — |

> 🔴 **The clean FLAT cell is empty, and it is empty by construction.** The FLAT floor shipped
> 2026-07-06; since then **no FLAT-labelled signal has ever been executed**. The forming-candle
> filter starts 07-04. So the clean window contains only the era in which the floor already
> guaranteed the answer. **The current label censors its own control group** — you cannot accumulate
> evidence about FLAT-labelled trades while the floor that FLAT triggers is switched on. That is a
> permanent property of the design, not a shortage of time.

For contrast only — **do not quote this as the answer**, it fails three of the four §0 filters: the
4 unfiltered FLAT trades (all 2026-06-30 … 07-05, i.e. pre-floor) went **0/4 for −306.42**, against
37 TREND trades at 18/37 for +1,273.12. That is the whole basis on which the floor was ever
justified, it is n=4, and every one of those rows is inside the wall-trail contamination window.

**Answer to Q2: it cannot be determined whether the current label separates winners from losers,
because the mechanism it drives has made the comparison impossible.**

---

## 3. CANDIDATE REDEFINITIONS

All four are computable at entry time from data the bot already fetches (`srv_adx_1h`,
`ema_gap_dir_1h`, `srv_atr_1h`, and 12 closed 1H candles).

| id | definition |
|---|---|
| **A** | `ADX(1h) ≥ 25` — the textbook Wilder threshold |
| **B** | `\|net move\| / range over the prior 12h ≥ 0.50` — directional efficiency |
| **C** | `EMA-gap(1h) Expanding AND ADX(1h) ≥ 20` — structure plus a floor on strength |
| **D** | at least 2 of {`ADX(1h) ≥ 25`, `eff_12h ≥ 0.5`, `ATR(1h) ≥ 14d median`} |

### Classification of the 9 clean closed trades — ⚠️ n per cell is 4–5. Illustrative only.

| vpos | side | score | net | R | CURRENT | A | B | C | D |
|---|---|---|---|---|---|---|---|---|---|
| 75 | LONG | 4.00 | −14.52 | −0.11 | TREND | TREND | TREND | FLAT | TREND |
| 76 | SHORT | 6.00 | +45.36 | +0.34 | TREND | FLAT | TREND | FLAT | FLAT |
| 77 | SHORT | 2.25 | −132.75 | −1.09 | TREND | TREND | TREND | FLAT | TREND |
| 78 | LONG | 2.50 | −103.54 | −1.20 | TREND | FLAT | FLAT | TREND | FLAT |
| 79 | LONG | 4.25 | +80.10 | +0.50 | TREND | FLAT | FLAT | FLAT | FLAT |
| 80 | SHORT | 4.00 | −116.58 | −1.09 | TREND | TREND | TREND | TREND | TREND |
| 81 | SHORT | 2.50 | +75.24 | +0.77 | TREND | FLAT | FLAT | TREND | FLAT |
| 82 | LONG | 5.00 | +53.79 | +1.04 | TREND | FLAT | FLAT | FLAT | FLAT |
| 83 | SHORT | 4.25 | −143.67 | −1.09 | TREND | TREND | TREND | TREND | TREND |

Applying the **real** gate under each definition (TREND → 2.0 bar, FLAT → 5.0 bar, so a FLAT-labelled
signal scoring ≥ 5.0 still passes):

| definition | takes | win | net of taken | drops | worth | **delta vs CURRENT** |
|---|---|---|---|---|---|---|
| CURRENT | 9 | 4/9 | −256.56 | 0 | 0.00 | — |
| A | 6 | 2/6 | −308.36 | 3 | +51.81 | **−51.81** |
| B | 6 | 2/6 | −308.36 | 3 | +51.81 | **−51.81** |
| **C** | 6 | 3/6 | −189.39 | 3 | −67.17 | **+67.17** |
| D | 6 | 2/6 | −308.36 | 3 | +51.81 | **−51.81** |

**Do not read C's +67.17 as a result.** It comes from dropping three trades — 75 (−14.52),
77 (−132.75) and 79 (+80.10) — and is **almost entirely one trade, vpos 77**. Give back vpos 79 and
the edge is 3 trades wide. Every cell here is 4–6 trades. n=9 supports no conclusion, and I am not
drawing one.

---

## 4. THE COST OF CHANGING IT — the load-bearing number

**The pool.** `below_threshold` + FLAT + gated score in `[2.0, 5.0)` = signals killed by the FLAT
floor **alone**: **n = 438**, all between 2026-07-06 and 2026-07-29. (Confirms the 10:11 figure from
a different table.)

| definition | relabelled TREND → would pass at 2.0 | share |
|---|---|---|
| A `ADX≥25` | **202** | 46% |
| B `eff_12h≥.5` | **200** | 46% |
| C `Expanding & ADX≥20` | **103** | 24% |
| D 2-of-3 | **156** | 36% |

### First: an extra gate-pass is not an extra trade

Over the FLAT-floor era (2026-07-06 →), of **610** signals that cleared the score gate, **17** became
trades — **2.79%**. The advisor and the position cap absorb the other 97%.

| relaxation | extra gate-passes | ≈ extra executed trades over 24 days | vs the 17 actually taken |
|---|---|---|---|
| all 438 | 438 | **~12** | +71% trade count |
| A / B | ~200 | ~5.6 | +33% |
| **C** | 103 | **~2.9** | **+17%** |
| D | 156 | ~4.3 | +25% |

This is an **upper bound** — the newly-passed signals carry lower scores, so the advisor would
plausibly skip them at a higher rate than 97%. **"400 borderline signals through" is not what any of
these definitions does to the bot.** The premise in the question overstates the blast radius by
roughly 35×.

### Second: the drift — and why it is not the answer

Drift of the skipped signals, positive = the skip would have won:

| definition | 24h drift of the NEWLY-PASSED | n | % positive | t | still-blocked |
|---|---|---|---|---|---|
| whole pool | +0.2025% | 424 | 55.7% | +2.25 | — |
| A | **−0.1536%** | 188 | 44.7% | −1.14 | +0.4861% (Welch **−3.57**) |
| B | +0.2203% | 200 | 54.0% | +1.99 | +0.1866% (Welch +0.19) |
| **C** | **+0.8431%** | 101 | **76.2%** | **+5.78** | +0.0022% (Welch **+4.65**) |
| D | +0.1902% | 142 | 52.1% | +1.52 | +0.2087% (Welch −0.11) |

C looks spectacular, and it survives several obvious attacks: both sides win (LONG +1.33% t=5.10;
SHORT +0.48% t=3.21 — so it is **not** a rising-tape artefact, since positive drift on a SHORT means
price fell), both halves of the window are positive, and leave-one-day-out keeps it at +0.57%,
t=3.85. Decomposed, the **Expanding half carries it** (Expanding alone +0.556% t=+4.53; ADX≥20 alone
**+0.065% t=+0.59 — nothing**), while `not-Expanding & ADX≥20` is **−0.382%, t=−2.73**.

Note also that A is **backwards**: ADX 25–30 drifts −0.34%, while ADX 20–25 (+0.53%, t=2.97) and
ADX < 20 (+0.46%, t=2.94) drift positive. High ADX marks the skips that were *right*. This
reproduces the pattern that retired the counter-trend caution (OPEN-ITEMS §4.5) and is a second,
independent reason not to reach for the textbook threshold.

**But the 438 fire in clusters.** Candidate C's 101 signals occupy **13 distinct days**:

| inference | n | mean 24h drift | t |
|---|---|---|---|
| per signal (pseudo-replication) | 101 | +0.756% | **+5.78** |
| **per DAY (mean of day-means)** | **13** | **+0.756%** | **+2.18** |

### Third: drift is an endpoint. The bot trades a PATH.

OPEN-ITEMS §4.9/§4.10 killed two confident wrong numbers for exactly this reason. So every signal
was simulated as a real trade on **real 15m candles** with Titan's actual geometry — 1R = 2.5×ATR(1h),
trailing stop 2.5×ATR(1h) armed at +1R, 48h cap — intrabar ambiguity resolved **adversely** (worst
case first, which biases every number *against* claiming a relaxation pays), minus **0.10R** of
costs calibrated on the four real clean stop-outs (real −1.10R vs modelled −1.00R).

Simulator validation against the real clean trades: stop-outs reproduce at −1.00R vs real
−1.09/−1.20/−1.09; trails reproduce vpos 79 at +0.61 vs +0.50 real and vpos 81 at +0.90 vs +0.77.
414 of 438 have a complete 48h path (24 excluded, too recent).

| | per signal | | | deduped to 1 per direction per 12h | | |
|---|---|---|---|---|---|---|
| | n | mean R | total R | n | mean R | total R |
| **all 438 (what the floor blocks)** | 414 | **−0.024** | −10.1 | 65 | **−0.127** | −8.2 |
| A newly-passed | 178 | **−0.134** | −23.8 | 36 | −0.020 | −0.7 |
| B newly-passed | 197 | **−0.158** | −31.1 | 41 | **−0.280** | −11.5 |
| **C newly-passed** | 101 | **+0.213** | +21.5 | 25 | **−0.069** | −1.7 |
| D newly-passed | 139 | −0.091 | −12.7 | 28 | −0.075 | −2.1 |

**Sensitivity — the assumption dominates the result.** Candidate C's newly-passed set:

| intrabar assumption | per signal | deduped 12h |
|---|---|---|
| ADVERSE first (pessimistic) | +0.213R, t=+1.95 | **−0.069R**, t=−0.32 |
| FAVORABLE first (optimistic) | +0.807R, t=+5.70 | **+0.331R**, t=+1.19 |

And across dedup windows (pessimistic): no dedup +0.213R → 4h +0.098R → 8h +0.071R → 12h −0.069R →
24h −0.126R. There are only **14 distinct calendar days** in the set.

> **Answer to Q4, plainly.** Relaxing the floor under **A, B or D would have LOST money** — all three
> are negative per-signal and deduped, and A additionally lets through precisely the cohort whose
> drift says the skip was right. For **C the answer is indeterminate**: the sign flips with the
> intrabar convention and with the deduplication window, and the whole result rests on 13–14
> independent days. **On the strongest available evidence, no candidate makes money.** The floor
> itself blocks a set whose expectancy is −0.024R per signal and −0.127R deduped — mildly negative,
> i.e. **the floor is not obviously costing anything either.**

---

## 5. THE MIRROR CASE — what would become FLAT and be rejected

25 executed entries currently sit in the `TREND` + score `[2.0, 5.0)` band, i.e. they pass only
because of the label. **Only 7 of the 25 survive the §0 filters** — the rest fall in the wall-trail
window or are pre-forming-candle.

| definition | would REJECT | their net | would KEEP | their net |
|---|---|---|---|---|
| A | 11 | **+331.92** (win 6/11) | 14 | −380.25 (win 3/14) |
| B | 11 | **+735.23** (win 7/11) | 14 | −783.56 (win 2/14) |
| **C** | 13 | **−406.77** (win 4/13) | 12 | +358.45 (win 5/12) |
| D | 13 | **+385.80** (win 7/13) | 12 | −434.12 (win 2/12) |

*Rejecting a profitable trade is a cost.* So on this contaminated 25, **A, B and D reject the winners
and keep the losers** — switching to them makes the band worse by 332 / 735 / 386 respectively.
Only **C** rejects losers. On the **clean** subset (§3) C drops three trades worth −67.17, and, as
stated there, that is essentially vpos 77 alone.

### The one that matters

vpos 83 — the trade this whole question came from. The independent tape at 2026-07-28 01:00:

```
ADX(1h) 25.84   ADX(4h) 17.97   |net|/range 12h 0.717   |net|/range 24h 0.714
ATR(1h) / 14d median 1.177      EMA-gap(1h) Expanding    gated score 4.25
```

| definition | label | bar | outcome |
|---|---|---|---|
| CURRENT | TREND | 2.0 | **TAKEN** |
| A `ADX≥25` | TREND | 2.0 | **TAKEN** |
| B `eff_12h≥.5` | TREND | 2.0 | **TAKEN** |
| C `Expanding & ADX≥20` | TREND | 2.0 | **TAKEN** |
| D 2-of-3 | TREND | 2.0 | **TAKEN** |

🔴 **Not one of them rejects it.** The tape genuinely was trending — this is the same conclusion the
10:11 report reached independently on the candle path (a real 3% down-leg, |net|/range 0.84). The
loss did not come from a mislabelled regime. **vpos 83 is not evidence for redefining
`market_regime`,** and it should stop being cited as such. Its problem was *where in the leg* it
entered — within 0.7% of the low — which is a different open question and not one a regime label
addresses.

---

## 6. HONEST VERDICT

**Is there a definition that is both a real measure of the tape AND at least as good as the current
one at separating outcomes?**

**No — and the second half of that question cannot be answered at all.**

1. **The label is genuinely a poor measure of the tape.** Confirmed, and more precisely than before:
   not inverted, but uninformative — Cramér's V 0.04–0.07, r ≈ 0.10, identical mean consensus votes
   (2.000 vs 2.000), agreement with any independent criterion 49–56%. §1 is solid and is the one
   finding here I would defend without qualification.
2. **Whether the current label separates outcomes is not determinable.** The mechanism it drives has
   emptied its own control cell: 9 clean closed trades, 9 TREND, 0 FLAT (§2). No amount of waiting
   fixes this while the floor is on.
3. **No candidate is demonstrably better.** A, B and D lose money on both sides of the change
   (§4, §5). C is the only one that ever looks good, and it fails the two most decision-relevant
   tests: its path-simulated edge **straddles zero** once signals are deduplicated to opportunities
   the bot could actually have taken (−0.069R pessimistic / +0.331R optimistic), and its
   clean-data edge is **one trade**.
4. **The motivating case does not motivate it.** All four definitions take vpos 83 (§5).
5. **The blast radius is smaller than assumed, which cuts both ways.** Relaxing all 438 adds ~12
   trades over 24 days, not 438 (§4) — so a redefinition is *survivable*, but it is also far too
   small a change to be validated any time soon at ~0.7 trades/day.

**What the data does support, stated without a recommendation:** the only fragment with a consistent
sign across drift, both trade sides, both halves of the window and leave-one-day-out is
**`EMA-gap(1h) Expanding`** — and its partner `ADX(1h) ≥ 20` contributes nothing on its own
(+0.065%, t=+0.59), while `not-Expanding & ADX≥20` is significantly *negative*. If this question is
ever re-opened, that is the fragment to test, and the test it must pass is the one it currently
fails: **a positive path-simulated expectancy after deduplication**, on data that did not exist
today.

**"The label is wrong but we cannot prove a better one" is the finding.** I am not proposing a
change, a flag, or a follow-up patch.

---

### Reproducibility

Everything above comes from `trades.db` (`trades`, `virtual_positions`, `skip_attribution`,
`skip_drift_samples`) plus OKX public history candles. No bot file was read for a tape value, no
stored extremum was used for any path question, and no code was modified.

### Notes for OPEN-ITEMS

- **Carry-forward #4 is already solved** — `skip_attribution.market_regime` is populated for
  `below_threshold` rows (673 FLAT / 50 TREND). The `trades`-table gap is real but no longer blocking.
- **The 10:11 report's "ADX 26.66 FLAT vs 25.52 TREND, anti-correlated" is withdrawn** and replaced
  by §0 above. The conclusion it supported is unchanged; the direction of the difference was a
  small-sample artefact and should not be quoted again.
- **New, structural:** the FLAT floor censors its own control group (§2). Any future attempt to
  validate the regime label against outcomes has to reckon with this first.
