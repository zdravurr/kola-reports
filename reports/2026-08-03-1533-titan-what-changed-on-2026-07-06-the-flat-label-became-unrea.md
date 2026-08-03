# titan what changed on 2026-07-06 the flat label became unreachable not the tape

_2026-08-03 15:33 UTC_

---

# TITAN — WHAT CHANGED? THE TAPE DIDN'T. THE **LABEL** DID, ON 2026-07-06.

_2026-08-03 15:40 UTC · HEAD `489e0ac` · LIVE, flat · **READ-ONLY — nothing changed, nothing proposed**_

---

## DECISION LINE

**The premise is half true, and the half that is true has a date.**

**The tape at entry has NOT shifted.** Same measures, every entry, month by month — ADX(1h) 23.2 →
30.6 → 24.5, ADX(4h) 29.9 → 32.6 → 24.0, efficiency ratio 4h 0.48 → 0.58 → 0.50, 12h 0.41 → 0.59 →
0.57, ATR-vs-own-median 0.98 → 1.03 → 0.95. **Nothing trends. The bot is not entering a measurably
flatter tape than it did in May.**

**Two things DID shift, and both have the same date window.**

🔴 **1. Since `db71454` (2026-07-06 13:54, "enforce FLAT-regime score floor (5.0)"), ZERO entries
have carried the FLAT label.** 12 of 43 entries before it were FLAT-labelled (28%); **0 of 23
after**. Not fewer — none.

🔴 **2. The side mix flipped.** LONG share 26% (May) → 19% (June) → **59% (July)**, turning inside
the window **2026-07-02 → 07-10**. LONG is structurally the losing side across the whole book:
**n=25, 32% win, −0.289R mean, −7.22R** vs SHORT **n=33, 48.5%, +0.141R, +4.64R**.

**So what the operator is seeing is real, and it is not that the bot started entering ranges. It is
that the bot stopped CALLING them ranges.** The FLAT floor did not remove range entries — it removed
the FLAT *label*, because a signal labelled FLAT can essentially never reach 5.0. Entries continue at
an unchanged tape character; every one of them now carries a live 1H signal and is therefore called
TREND. **The category the operator would recognise as "range entry" no longer exists as a label, and
the trades it used to describe now arrive under the other name.**

**And three previously-recorded findings do not survive re-measurement over a proper window:**

| claim (2026-08-01) | measured over months |
|---|---|
| HTF cascade tightened ~73% → **82.2%** | **74.0% · 72.5% · 73.3% · 70.1%** — flat, August is *lower* |
| TREND signals at the gate fell ~21/day → **4/day** | **15.4 · 21.3 · 20.8 · 29.7** per day — August is the *highest* |
| the 3.0 bar cost **EXACTLY ZERO** entries | **45** signals sit in the 2.0–3.0 band; **16** with the score gate as the binding constraint |

**All three were 24-hour windows generalised. Both "unexplained shifts" chased in §3 do not exist.**

---

## §1 — IS THE PREMISE TRUE? THE TAPE, MONTH BY MONTH

All 65 entries, same measures throughout, medians within month, ADX at window 200.

| month | n | ADX1h | ADX4h | ER 4h | ER 12h | ATR/med | pos24 | cont |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-05 | 19 | 23.17 | 29.93 | 0.48 | 0.41 | 0.98 | 0.53 | 0.47 |
| 2026-06 | 16 | 30.64 | 32.56 | 0.58 | 0.59 | 1.03 | 0.14 | 0.13 |
| 2026-07 | 29 | 24.51 | 23.98 | 0.50 | 0.57 | 0.95 | 0.76 | 0.09 |
| 2026-08 | 1 | 18.87 | 26.87 | 0.92 | 0.64 | 0.83 | 0.01 | 0.01 |

**No monotone drift in any tape measure.** June was the *most* trending month by ADX and July fell
back to May's level. Efficiency ratio and ATR-vs-median are flat throughout. August is n=1 (vpos 91)
and carries no weight.

**The series that does move is the side mix and its outcome:**

| month | n | SHORT | LONG | LONG share | SHORT medR / win | LONG medR / win |
|---|---:|---:|---:|---:|---|---|
| 2026-05 | 19 | 14 | 5 | 26% | +0.057 / 57% | +0.040 / 60% |
| 2026-06 | 16 | 13 | 3 | 19% | **+0.571 / 69%** | −0.584 / 33% |
| 2026-07 | 29 | 12 | 17 | **59%** | **−0.432 / 25%** | −0.293 / 24% |
| 2026-08 | 1 | 1 | 0 | 0% | −0.484 / 0% | — |

Rolling 10-entry windows put the turn precisely: LONG 1/10 → 4/10 → 1/10 → 2/10 → 3/10 → **5/10
(2026-06-23→07-05)** → **8/10 (2026-07-02→07-10)** → 7/10 → 5/10 → 5/10 → 4/10.

⚠️ **Note J.'s SHORTs also collapsed (−0.432R, 25% win).** So the side mix is not the whole story —
July was bad for both sides. **A side-mix change alone does not explain it.**

---

## §2 — THE DISCONTINUITY, AND WHAT SITS ON IT

**Date: 2026-07-06 13:54 — commit `db71454`, "fix(titan): enforce FLAT-regime score floor (5.0);
TREND stays 2.0".** It lands inside the LONG-turn window and is the only entry-gate change in it.

The other commits in 2026-06-25 → 07-20 are `19f9c94` (2026-07-02 23:28, wall-trail LIVE) and
`5f1b073`/`c845941` (2026-07-13, disabling it again) — **all exit-side**, and precisely the window
§0's wall-trail filter exists to exclude.

### What the floor did — regime label DERIVED from the breakdown, not read

*(the stored `market_regime` column is populated on only 2,610 of 3,978 gate-reaching rows, so it is
re-derived from `TREND.net_direction`, validated earlier at **2,613/2,613**.)*

| era | signals at gate | TREND | FLAT | FLAT% | **executed** | TREND | FLAT | **FLAT%** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A pre-floor (→ 07-06) | 2561 | 1023 | 1538 | 60.1% | 43 | 31 | 12 | **27.9%** |
| B floor 5.0 / TREND 2.0 | 1207 | 507 | 700 | 58.0% | 19 | 19 | 0 | **0.0%** |
| C TREND 3.0 (→ now) | 210 | 106 | 104 | 49.5% | 4 | 4 | 0 | **0.0%** |

**The supply of FLAT-labelled signals barely moved (60.1% → 58.0% → 49.5% of everything reaching the
gate). What changed is that none of them can execute any more.**

| era | FLAT signals at gate | median gated | clear 5.0 | **executed** |
|---|---:|---:|---:|---:|
| A | 1538 | 3.75 | 378 (24.6%) | **12** |
| B | 700 | 4.25 | 177 (25.3%) | **0** |
| C | 104 | 3.50 | 17 (16.3%) | **0** |

By month, entries by label: May **40% FLAT** → June 6.2% → July 10.3% → August 0%.

### 🔴 Does the label carry tape information at all?

| label | n | ADX1h | ADX4h | ER 4h | ER 12h |
|---|---:|---:|---:|---:|---:|
| TREND | 53 | 24.78 | 24.84 | 0.541 | 0.565 |
| FLAT | 12 | 24.22 | **32.76** | 0.298 | 0.351 |

TREND-minus-FLAT: ADX(1h) **+0.56** (nothing) · ADX(4h) **−7.92** (TREND-labelled sits on a *less*
trending 4h) · ER 4h +0.243 · ER 12h +0.213.

**Inconsistent and self-contradicting: two measures say TREND-labelled is more directional, ADX(4h)
says markedly less, and the FLAT cell is n=12.** The label is not a reliable statement about the
tape — which is what "signal presence, not a measurement" means, now confirmed on price and not only
in code.

---

## §3 — THE TWO UNEXPLAINED SHIFTS. **NEITHER EXISTS.**

### 3a. The HTF cascade did not tighten

| month | signals reaching HTF | htf_blocked | **block rate** |
|---|---:|---:|---:|
| 2026-05 | 2837 | 2100 | **74.0%** |
| 2026-06 | 5505 | 3993 | **72.5%** |
| 2026-07 | 5852 | 4289 | **73.3%** |
| 2026-08 | 578 | 405 | **70.1%** |

**Flat at ~73%, and August is the loosest month in the book.** The "~73% → 82.2%" of 2026-08-01 was a
24-hour reading.

Tier-by-tier opposition rate on the 10,783 usable blocked rows — **all four tiers move together and
all four ease slightly**, so no single tier tightened:

| month | 1H opposes | 4H opposes | 15m opposes | 5m opposes |
|---|---:|---:|---:|---:|
| 2026-05 | 31.4% | 31.5% | 29.9% | 25.5% |
| 2026-06 | 30.4% | 31.1% | 32.0% | 30.7% |
| 2026-07 | 25.4% | 25.5% | 25.6% | 25.5% |
| 2026-08 | 19.5% | 31.4% | 27.9% | 18.5% |

### 3b. 1H signals did not stop arriving

**305 1H alerts, May 15 → Aug 3.** Per day: **3.80 · 3.70 · 4.06 · 3.67**. By name, every signal
family continues at a stable rate — `Any Bullish Confirmation` 10/17/19/3, `Trend Catcher Up`
6/12/15/0, `Smart Trail Bearish` 2/5/7/0, and so on for all twelve. **Nothing stopped arriving.**

And the claim it was meant to explain:

| month | TREND at gate | **per day** | FLAT at gate | per day |
|---|---:|---:|---:|---:|
| 2026-05 | 262 | 15.4 | 474 | 27.9 |
| 2026-06 | 640 | 21.3 | 870 | 29.0 |
| 2026-07 | 645 | 20.8 | 914 | 29.5 |
| 2026-08 | 89 | **29.7** | 84 | 28.0 |

**TREND arrival at the gate is stable and August is the highest of the four months.** Day by day the
source of the 08-01 figure is visible: **2026-08-01 had TREND 0 / FLAT 56** — a single anomalous day,
flanked by 07-31 (17/14), 08-02 (53/15) and 08-03 (36/13). **The "collapse to 4/day" was one day.**

---

## §4 — COMPOSITION OF WHAT PASSES. **STABLE.**

Medians within month; MARGIN = gated score minus the bar it actually faced.

| month | n | raw | macro | gated | bar | **margin** | #cats | #sigs | #conflicted |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-05 | 20 | 4.25 | 0.00 | 5.38 | 2.0 | **+2.00** | 2.0 | 7.0 | 1.0 |
| 2026-06 | 16 | 4.25 | 1.00 | 5.25 | 2.0 | **+3.12** | 2.0 | 5.5 | 0.5 |
| 2026-07 | 29 | 4.00 | 0.00 | 4.25 | 2.0 | **+2.25** | 2.0 | 6.0 | 1.0 |
| 2026-08 | 1 | 2.50 | 1.00 | 3.50 | 3.0 | +0.50 | 1.0 | 12.0 | 3.0 |

**The bot is not clearing the bar by less than it used to, nor with fewer categories.** Median raw
score, category count, signal count and conflict count are all steady. The one row that looks
different is August — and August is **vpos 91 alone**, the trade that prompted the question.

---

## §5 — THE 3.0 BAR, RE-EXAMINED. **IT IS NOT COSMETIC.**

Window **2026-07-30 21:34 → now = 90.0 hours (3.8 days)**, against the 39 h measured on 2026-08-01.
834 signals with a breakdown; **328 TREND-labelled** — the only ones the 3.0 bar applies to.

```
refused by the 3.0 bar (TREND, gated < 3.0)      : 49
of those, would have PASSED at the old 2.0 bar   : 45      <- NOT zero
   their scores: 2.25, then 2.5 x43, then 2.75
   their statuses: htf_blocked 27 · below_threshold 16 · risk_halt 2
refusals below 2.0 (dead either way)             : 4   (all 1.5)
```

**The honest number is 16, not 45 and not 0.** 27 of the 45 were already killed by the HTF cascade
*before* the score gate, and 2 by the risk halt — for those the bar was not the binding constraint.
**For 16 signals the score gate was what stopped them, ≈4.2 per day, against 4 entries executed in
the same window.** The raise is refusing roughly as many signals per day as the bot executes.

Distribution of TREND gated scores in the window: `<2.0` 1.2% · **`2.0–3.0` 13.7%** · `3.0–4.0` 13.7%
· `≥4.0` 71.3%. **The 2.0–3.0 band is populated — the bar sits inside the distribution, not below
it.** The 2026-08-01 conclusion came from looking only at `below_threshold` rows over 39 hours.

---

## §6 — VERDICT

**The entries have NOT changed character on any tape measure. The premise, as stated, is not
supported — but the operator is not seeing three bad trades either.**

**What is real, with its date:**

**On 2026-07-06 13:54, `db71454` made the FLAT label unreachable.** Since that commit, **0 of 23
entries** have been FLAT-labelled, against 12 of 43 before. The supply of FLAT-labelled signals
reaching the gate barely moved (60% → 58% → 50%); what changed is that a FLAT-labelled signal now
needs 5.0, and in practice never gets there. **Every entry since is TREND-labelled, which means only
that a 1H signal was alive and unconflicted.**

**So the change the operator perceives is a change of NAME, not of behaviour.** The bot enters the
same tape it always did — ADX, efficiency ratio and ATR-vs-median all say so — but it no longer
labels any of those entries FLAT. What used to be visible as "a range entry" is now invisible,
because the only label it could have carried has been made unreachable. **The FLAT floor removed the
category, not the trades.**

**Second, smaller, and genuinely a behaviour change:** the side mix flipped to LONG-majority in the
window 2026-07-02 → 07-10, and LONG is the losing side across the whole book (−7.22R vs +4.64R).
That is not explained by anything measured here, and July's SHORTs were bad too, so it is a partial
explanation at best.

**What I got wrong before, corrected here:** the HTF cascade did not tighten (flat ~73%, August
loosest), 1H signals did not stop arriving (3.7–4.1/day all four months), TREND arrival at the gate
did not collapse (August is the highest month), and the 3.0 bar is not costless (16 binding refusals
in 3.8 days). **All four earlier figures were single-day windows read as trends** — the same error,
four times, and it is the error this study was built to avoid.

**Nothing is proposed and nothing was changed.** The one thing the numbers point at, if anything is
to be looked at next, is the date **2026-07-06** and the question of whether making a label
unreachable was the intended effect of putting a floor under it.
