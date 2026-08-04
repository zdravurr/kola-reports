# DOES ANY NUMBER THIS BOT PRODUCES RANK ITS OWN TRADES? — NOT PROVABLY. AND THAT IS NOT "NO".

**2026-08-04 17:31 UTC · Titan LIVE, real money, flat · HEAD `be53e63` · READ-ONLY, nothing applied**

**Bonferroni stated before any result: 34 tests (16 predictors × 2 sides + 2 pooled) → α = 0.05/34 =
0.00147. NOTHING SURVIVES CORRECTION.**

**Cohort: §0-clean n=40 (LONG 15 / SHORT 25). Entirely PRE-boundary — there are 0 entries after
2026-08-04 17:01:29 — so the whole book is one 1R unit and today's boundary does not bite yet.**
**Reconstruction validated first: the score rebuilt from `matrix_breakdown_json` equals the stored
value on 40 of 40 rows (mean |Δ| 0.000).**

Canon: **§2.55**. Snapshot: `reports/2026-08-04-1731-open-items.md`.

---

## 🔴 0. THE HEADLINE IS A CORRECTION TO §2.46

§2.46 said the confluence score has **no** ranking power on the long book — all four quartiles
negative, the three highest-scored longs losing, p=0.487. **That was measured on all 26 longs using
the gated score. On the §0-clean cohort with the reconstructed raw score, the score ranks BOTH
sides:**

| | Q1 | Q2 | Q3 | Q4 | Spearman ρ |
|---|---|---|---|---|---|
| §2.46 — ALL 26 longs, GATED score | −0.554 | −0.299 | −0.176 | −0.211 | +0.126 (p=0.54) |
| **CLEAN 15 longs, RAW score** | −0.569 | −0.550 | −0.085 | **+0.118** | **+0.405** (p=0.14) |
| **CLEAN 25 shorts, RAW score** | −0.257 | +0.290 | +0.079 | **+0.548** (win **100 %**) | **+0.378** (p=0.06) |

**The 11 non-clean longs flip the conclusion** — and §0's filters exist precisely because those
outcomes were decided by a moved stop rather than by the entry.

**So "the scoring system is decorative and the bar is arbitrary" is NOT supported.** The true
statement is weaker and less comfortable: **the score points the right way on both sides and cannot
prove it at n=15/25.** ⚠️ **The bar's LEVEL is still uncalibrated** — a monotone ranking is not a
calibrated threshold, and nothing here says 3.0 is the right number.

## 1. §1 — EVERY STORED PREDICTOR, RANKED AGAINST OUTCOME

Spearman ρ with R, permutation p (20 k), per side:

| predictor | LONG (n=15) | SHORT (n=25) |
|---|---|---|
| **confluence score** (reconstructed per §0) | **+0.405** (p=0.136) | **+0.378** (p=0.064) |
| **advisor confidence** | −0.098 (p=0.727) | +0.083 (p=0.698) |
| contributing categories | +0.386 (p=0.157) | +0.341 (p=0.102) |
| total signals in matrix | −0.202 (p=0.464) | +0.127 (p=0.544) |
| intra-conflicted categories | −0.216 (p=0.449) | −0.241 (p=0.245) |
| ATR % (1h) | +0.127 (n=10) | **+0.438** (p=0.072, n=18) |
| EMA gap % 1h | +0.418 (p=0.123) | +0.085 (p=0.679) |
| EMA gap % 15m / 5m | +0.200 / +0.214 | +0.043 / +0.212 |
| **vol_ratio 5m** | **−0.582 (p=0.025)** ← the only nominal hit | −0.129 (p=0.531) |
| vol_ratio 1h | −0.114 | −0.167 |
| book: supporting wall | −0.071 (n=8) | **−0.655** (p=0.063, n=9) |
| book: imbalance / n walls | +0.357 / +0.421 (n=8) | −0.200 / +0.227 (n=9) |
| **combo weight** | +0.363 (p=0.229) | 🔴 **ZERO VARIANCE — every clean short carries 1.0** |
| ADX(1h) @200 window | **n=1** | **n=4** — untestable |
| tier ages / agreement | `entry_tiers_json` on **7 of 40** — untestable | |

**Two structural facts fall out of the coverage rather than the correlations:**
- 🔴 **The combo weight cannot rank anything on the short book because it does not vary** — every
  clean short carries exactly 1.0. That is §2.40's inert mechanism, visible in the outcome data
  instead of inferred from thresholds.
- **The sanctioned ADX(1h) at the 200-bar window exists on 5 of 40 clean rows**, and tier ages on 7.
  Two of the brief's questions are **unanswerable on the stored record**, not merely unanswered.

## 2. §1b — THE ADVISOR'S OWN CERTAINTY (nobody had ever checked this)

ρ ≈ 0 on both sides. But the rank test is weak here because the variable is coarse — **17 of 40 rows
are exactly 0.72** (0.62×6, 0.70×2, **0.72×17**, 0.78×13, 0.82×1, 0.87×1) — so the band split was run
too:

| cut | conf > 0.72 | conf ≤ 0.72 | Δ | p |
|---|---|---|---|---|
| ALL | +0.202R (n=15) | −0.092R (n=25) | +0.293 | 0.374 |
| SHORT | +0.388R (n=11) | +0.017R (n=14) | +0.370 | 0.400 |
| LONG | −0.310R (n=4) | −0.230R (n=11) | −0.080 | 0.870 |

**Not significant on any cut.** The second-largest gate's self-reported confidence does not rank its
own approvals — the direction is mildly encouraging on shorts and it is n=11 against n=14.

## 3. §2c — DE-CONFOUNDING THE ONE NOMINAL HIT

`vol_ratio_5m` on longs (ρ=−0.582, p=0.025) — lower 5m volume at entry, better outcome:

- **hour-bucket-demeaned: ρ=−0.579 (p=0.025) — survives the clock.** Unlike §2.54's pockets, this one
  is not a time-of-day artifact.
- **day-demeaned: ρ=−0.381 (p=0.353)** — weakens sharply, but on only **8** longs that share a day
  with another entry. Underpowered rather than refuted.
- **It still needs n≈39 per side to clear Bonferroni.** It does not clear it now.

⚠️ **§2.5's numbers do not reproduce in level.** It reported winners' median vol_ratio 0.95 vs losers'
1.57. Clean, in R, on this cohort: **winners 1.37 (n=7) vs losers 2.51 (n=8)**. **The direction holds;
the magnitudes are 40–60 % higher.** §2.5's figures came from a cohort spanning two sizing eras — the
re-measurement it asked for is done, and it moved.

## 4. §3 — WHAT THIS CANNOT ANSWER, AND WHAT WOULD

**34 of 40 observations are paper at 68× the live notional. The live era is 7 trades (2 LONG /
5 SHORT). The geometry changed 30 minutes before this pass.** A predictor that ranks the paper book
may not rank the live one, and nothing here can distinguish the two.

Power required on **live data alone**, 80 % power:

| effect size | uncorrected α=0.05 | at Bonferroni α=0.00147 |
|---|---|---|
| ρ = 0.58 (the strongest observed) | n ≈ 20/side | **n ≈ 39/side** |
| ρ = 0.40 (the score's) | n ≈ 46/side | **n ≈ 93/side** |
| ρ = 0.30 | n ≈ 84/side | n ≈ 171/side |
| ρ = 0.20 | n ≈ 193/side | n ≈ 396/side |

**At 0.47 entries/day: n=39/side ≈ 165 days. n=93/side ≈ 400 days.** The honest reading is that **this
question cannot be settled by waiting** at the current entry rate, in the same way §2.51's trail
question could not.

## 5. §4 — THE DECISION

**Branch 2 fires: nothing survives.** No predictor clears Bonferroni on either side; the only nominal
hit needs three times the sample to be believed.

**But the precise sentence matters, and it is not the one the brief offered.** "This bot's own numbers
do not rank its own trades" would overclaim in the other direction. What the data supports is:

> **This book cannot tell a ρ of +0.4 from zero.** The apparatus is **unfalsified, not validated**.
> The score and the category count point the right way on **both** sides; the advisor's confidence
> points nowhere; the combo weight cannot point anywhere because it does not vary; and two of the
> predictors asked about are not recorded densely enough to test at all.

**What that reframes:** every filter shipped today was justified by outcome differences on this same
n. **They rest on the same statistical foundation as the score they were built around** — which is to
say, on a foundation that cannot yet distinguish a real effect from none. That is an argument for
letting the live book accumulate under the current geometry before adding anything further, not for
tearing out the scoring system.

## 6. SCOPE

**Read-only.** `git status` clean at `be53e63`, 0 open positions, no restart, no table written.
Nothing was applied and nothing is proposed.
