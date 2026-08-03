# titan entry measured read-only: intra-conflict separates, ADX does not, no change proposed

_2026-08-03 15:08 UTC_

---

# TITAN — THE ENTRY, MEASURED. READ-ONLY. NO CHANGE PROPOSED.

_2026-08-03 15:20 UTC · HEAD `489e0ac` · LIVE, flat · **nothing was modified — no code, no config, no DB write**_

---

## DECISION LINE

**The clean cohort is n = 39.** Every outcome below is in **R** (`net_pnl / initial_risk_usdt`), never
USDT — the book spans a **68× notional change** and USDT is not poolable across it.

**Four things the numbers say, and two of them contradict the premise of the question:**

1. **🔴 Intra-conflict presence separates hard — but the DIRECTION of the suppressed dissent does
   not.** No conflict at all: **n=14, 85.7% win, +0.536R mean**. Any conflict: **n=25, ~36% win,
   negative**. Within the conflicted group, "the suppressed side OPPOSED the trade" (n=16, −0.051R)
   is the *best* sub-cell, better than "suppressed side AGREED" (n=3, −1.124R). **§1c's hypothesis —
   that suppressing opposing dissent is what costs money — is not supported. What costs money is
   being in a conflicted state at all.**
2. **🔴 Neither alternative rule can filter anything — both only RAISE scores.** Contribution is
   `|lp − sp| ≥ 0`, so un-zeroing dissent can only *add* points. Halving moves 8 of 39 trades by
   **+0.392** mean; majority-carry by **+0.781**. **There is no negative contribution anywhere in
   this scoring shape**, so "let the dissent speak" cannot block a bad trade — it can only admit
   more. That is a structural fact about the scorer, not a result about this sample.
3. **§1 and §2 are ONE lever, not two.** Jaccard 0.53, and the decisive cell is "no conflict, fewer
   than 3 contributing categories" at **n=6, +0.597R** — as good as the broad-based cell. **Breadth
   adds nothing once conflict is absent.** Ranking them separately would double-count.
4. **🔴 ADX still does not separate — the 2026-07-30 finding holds.** Sub-floor ADX(1h) is **not**
   the worst cell (n=7, −0.112R); **ADX(1h) 20–25 is the best** (n=14, +0.167R) and ADX(4h) **< 20**
   is the best 4h cell (n=11, +0.250R). **The FLAT floor is aimed at something the data does not
   show to be the problem.**

**On vpos 91 specifically:** it was a 2-zeroed-category, 2-contributing-category, one-tier-opposing
entry at ADX(1h) 18.58. The cell it belongs to (`2 zeroed`) runs **n=12, 41.7% win, −0.086R** — not a
disaster cell, just a mediocre one. **Three bad trades is not what the ranking below rests on.**

---

## 0. METHOD — FILTERS AND THEIR COST, STATED BEFORE ANY STATISTIC

```
positions with an entry row                65   (59 closed · 6 archived_pre_geometry_fix)
  -> closed with a net_pnl                 59
  -> wall-trail LIFETIME overlap filter    47   (dropped 12)   §0: lifetime, not entry time
  -> recheck TIGHTEN filter                40   (dropped  7)
  -> has matrix_breakdown_json             40
  -> has a usable 1R                       39   <- THE CLEAN COHORT
     LIVE 5 · PAPER 34 · 2026-05-21 -> 2026-08-03
```

🔴 **Only 5 of 39 are live-era.** Every cell below is therefore dominated by the paper era. R
normalises the size, but it does not normalise fill quality, fees-to-R, or the exit contract in
force. **Treat all of this as a paper-era measurement with a live-era tail.**

### The replay was validated before it was used (§0 standing methodology)

Re-implementing `signal_matrix.compute_score`'s category maths from each row's own stored
`long_points` / `short_points`:

```
rows compared                                 14,762
per-category CONTRIBUTION reproduced exactly  14,762 / 14,762
matrix_direction reproduced                   14,762 / 14,762
market_regime reproduced                       2,613 / 2,613   (NULL on the rest — not a mismatch)
```

**Only after that were inputs substituted.**

### One correction to the premise, because it moves where a fix would hang

The 3.0-vs-5.0 bar is **not** chosen by a separate regime measurement.
`signal_matrix.py:448` — `market_regime = 'TREND' if trend_net_dir != NEUTRAL else 'FLAT'` — and
`main._eff_thr` gates on that string. **The regime label IS "the TREND category has at least one
unconflicted signal".** The operator's description is exactly right in effect; the mechanism is the
TREND *category*, not a market measurement. **TREND intra-conflicts 0 times in 66 entries**, so the
bar chosen is untouched by anything in §1.

---

## §1 — INTRA-CONFLICT ZEROING

### 1a. How often it fires — all 66 executed entries

| category | intra-conflict fires | share | contribution == 0 |
|---|---:|---:|---:|
| TREND | **0** | 0.0% | 12 (18.2%) |
| MOMENTUM | 19 | 28.8% | 32 (48.5%) |
| LIQUIDITY | 20 | 30.3% | 54 (81.8%) |
| EXECUTION | 26 | 39.4% | 26 (39.4%) |

| categories zeroed at once | entries | share |
|---|---:|---:|
| 0 | 27 | 40.9% |
| 1 | 18 | 27.3% |
| 2 | 16 | 24.2% |
| 3 | 5 | 7.6% |
| 4 | 0 | — |

**59.1% of entries have at least one category silenced by its own disagreement.**

### 1b. Outcomes by number of zeroed categories (clean cohort)

| zeroed | n | win | mean R | med R | sum R |
|---|---:|---:|---:|---:|---:|
| **0** | **14** | **85.7%** | **+0.536** | +0.145 | **+7.50** |
| 1 | 11 | 27.3% | −0.458 | −1.064 | −5.04 |
| 2 | 12 | 41.7% | −0.086 | −0.256 | −1.03 |
| 3 | 2 | 50.0% | +0.013 | +0.013 | +0.03 |

Per side: 0-zeroed SHORT **n=10, 80% win, +0.614R**; 0-zeroed LONG **n=4, 100%, +0.342R**.

⚠️ **Non-monotonic** — 1-zeroed is worse than 2-zeroed. At n=11 and n=12 that is well inside noise.
**The only robust statement is 0 versus ≥1.**

### 1c. 🔴 Did the suppressed dissent OPPOSE the trade? — the hypothesis is not supported

| cohort | n | win | mean R | med R | sum R |
|---|---:|---:|---:|---:|---:|
| **no conflict at all** | **14** | **85.7%** | **+0.536** | +0.145 | +7.50 |
| conflict, suppressed side **OPPOSED** | 16 | 43.8% | −0.051 | −0.158 | −0.82 |
| conflict, suppressed side **AGREED** | 3 | 0.0% | −1.124 | −1.087 | −3.37 |
| conflict, exactly **TIED** | 6 | 33.3% | −0.309 | −0.300 | −1.85 |

By count of opposing suppressed categories: **0 opposing → n=23, +0.099R**; **1 opposing → n=16,
−0.051R**. A spread of 0.15R on n=23 vs n=16.

🔴 **If suppressing dissent were costly, this is exactly where it would show, and it does not.** The
opposed cell is the *best* of the three conflicted cells. The separation lives in
**conflicted vs not**, worth **~0.6R**, not in **which way the dissent pointed**, worth ~0.15R and
inside noise.

### 1d. Halving, and majority-carry — replayed

Definitions, so they can be checked: `live` = conflict → 0 · `half` = conflict → `0.5×|lp−sp|`
toward the bigger side · `major` = conflict → `1.0×|lp−sp|`. Both rerun the full inter-category
resolution. TREND never conflicts, so the 3.0/5.0 bar is unchanged by both.

```
half  :  8 of 39 trades change score,  mean delta +0.392
major :  8 of 39 trades change score,  mean delta +0.781
direction flips:  1 of 39 under each  (vpos 78, NEUTRAL -> LONG)

applying TODAY'S bar (3.0 TREND / 5.0 FLAT) retrospectively:
  live  : kept n=31 sumR +5.90  | blocked n=8 sumR -4.44
  half  : kept n=31 sumR +5.90  | blocked n=8 sumR -4.44   (identical — no trade crosses)
  major : kept n=32 sumR +4.71  | blocked n=7 sumR -3.25   (admits ONE more, a loser)
```

🔴 **Both alternatives are loosenings, and cannot be otherwise.** `|lp−sp| ≥ 0` means un-zeroing can
only add points. **To make dissent cost something, the scorer would need a negative contribution,
which it does not have anywhere.** Halving changes no gate outcome at all; majority-carry admits one
extra trade and that trade lost.

⚠️ 35 of these 39 were taken under the **2.0** bar (raised to 3.0 on 2026-07-30, `dee6cee`).
Applying today's bar backwards is a counterfactual, not history.

---

## §2 — HOW MUCH COMES FROM ONE CATEGORY

**2a. Share of the raw score held by the single largest category**, all 66 executed entries:

| share | entries |
|---|---:|
| **100% — one category only** | 10 (15.2%) |
| 75–99% | 0 |
| 50–74% | 40 (60.6%) |
| < 50% | 16 (24.2%) |

**2b. Outcomes by number of contributing categories** (clean cohort):

| contributing | n | win | mean R | med R | sum R |
|---|---:|---:|---:|---:|---:|
| 1 | 5 | 20.0% | −0.512 | −0.484 | −2.56 |
| 2 | 25 | 44.0% | +0.001 | −0.209 | +0.02 |
| **3** | **9** | **100.0%** | **+0.444** | +0.116 | +4.00 |
| 4 | 0 | — | — | — | — |

**2c. A rule "at least TWO categories must contribute"** would have blocked **n=5, 20% win,
−0.512R mean, −2.56R total**, keeping n=34 at +0.118R. Across all 66 executed entries, **10 (15.2%)**
were carried by ≤1 category.

### 🔴 But §1 and §2 are the same lever

| | ncon=1 | ncon=2 | ncon=3 |
|---|---:|---:|---:|
| **nzero=0** | 0 | 6 | 8 |
| nzero=1 | 0 | 10 | 1 |
| nzero=2 | 3 | 9 | 0 |
| nzero=3 | 2 | 0 | 0 |

Disjoint cells:

```
no-conflict AND 3+ contributing : n=8   meanR +0.490  win 100%
no-conflict, FEWER than 3       : n=6   meanR +0.597  win  67%   <- just as good
3+ contributing, HAS conflict   : n=1   meanR +0.075
neither                         : n=24  meanR -0.255  win  33%
```

**Breadth adds nothing once conflict is absent** (+0.597 vs +0.490, n=6 vs n=8). **The separating
variable is the absence of intra-conflict.** A "two categories" rule is a partial proxy for it — all
5 one-category trades are conflicted ones.

---

## §3 — A TIER POINTING AGAINST THE TRADE

🔴 **Not measurable at usable n, and I am not going to pretend otherwise.** `entry_tiers_json` only
exists from **2026-07-29** (`7285c5d`); **6 of the 39** clean trades carry it.

```
§3a  15m opposed on 3 of 6 entries.  1H: 0.  5m: 0.
§3b  at least one tier OPPOSING : n=3  win 0.0%   meanR -0.622
     fully aligned              : n=3  win 33.3%  meanR +0.214
§3c  opposing AND expired-TTL   : n=3  win 0.0%   meanR -0.622
     opposing AND live (counted): n=0
```

**n=3 versus n=3. No conclusion is available, and the §3c question cannot be answered at all** —
there is not one entry in the record with a *live* opposing tier to compare against. The three
expired-opposing entries all lost, which is suggestive and nothing more.

**The measurable equivalent at scale is §1c** — dissent inside a category, n=39 — and there the
opposing cell was the *best* of the conflicted cells.

---

## §4 — IS "FLAT" MEASURABLE, INDEPENDENTLY OF THE BOT'S LABEL?

All recomputed from **real candles**, window **200** (the sanctioned ADX window), 2,536 × 1h and
634 × 4h fetched for the purpose.

### 4c. 🔴 The confound check first — is a low-ADX entry actually worse? **No.**

| ADX(1h) at entry | n | win | mean R | med R | sum R |
|---|---:|---:|---:|---:|---:|
| **< 20 (below the FLAT floor)** | 7 | 57.1% | −0.112 | **+0.015** | −0.78 |
| **20–25** | 14 | 64.3% | **+0.167** | +0.255 | +2.33 |
| ≥ 25 | 18 | 44.4% | −0.005 | −0.158 | −0.09 |

| ADX(4h) at entry | n | win | mean R | sum R |
|---|---:|---:|---:|---:|
| **< 20** | 11 | 63.6% | **+0.250** | +2.75 |
| 20–25 | 12 | 50.0% | −0.172 | −2.06 |
| ≥ 25 | 16 | 50.0% | +0.048 | +0.77 |

**The 2026-07-30 finding holds on the current clean sample.** Sub-floor ADX is not the worst cell on
either timeframe; on the 4h it is the **best**. **Low ADX is not the problem, and a FLAT floor hung
on ADX is aimed at the wrong thing.** That is the answer to the question the operator asked before
touching it.

### 4a/b. The other candidate measures — three of four separate nothing

| measure (split at its own median) | below | at/above |
|---|---|---|
| \|net move\|/range, prior 4h (med 0.504) | n=19, +0.066R | n=20, +0.010R |
| \|net move\|/range, prior 12h (med 0.580) | n=19, −0.031R | n=20, +0.102R |
| ATR(1h) ÷ its own 14-day median (med 1.028) | n=19, +0.002R | n=20, +0.072R |
| **position in prior 24h range (med 0.188)** | **n=19, +0.373R, 68.4%** | **n=20, −0.281R, 40.0%** |

**Three of the four are flat to within noise.** The fourth looked strong — so I checked it.

### 🔴 The pos-in-range confound, checked rather than reported

```
side mix INSIDE each raw bucket:   below median: SHORT 18 / LONG  1
                                   at/above    : SHORT  7 / LONG 13
```

**The raw split is very nearly a side split.** But it survives within each side, in *opposite*
directions:

```
SHORT (own median 0.127)  low  n=12  win 66.7%  meanR +0.702      <- entering near the 24h LOW
                          high n=13  win 46.2%  meanR -0.302
LONG  (own median 0.752)  low  n= 7  win 42.9%  meanR -0.596
                          high n= 7  win 57.1%  meanR +0.161      <- entering near the 24h HIGH
```

**That is continuation, not mean reversion**, and it is **not a flatness measure** — it is a location
measure. It is the only one of the five candidates that survives its own confound check.

### The answer to §4b, plainly

**Flat is not measurable on this book.** Of five independent candidates, ADX(1h), ADX(4h),
efficiency-over-4h, efficiency-over-12h and ATR-vs-median **all fail to separate outcomes**. The one
that does separate is not a measure of flatness. **"Flat is not measurable here" is the honest
answer and I am giving it rather than fitting a threshold to n=39.**

---

## §5 — THE HONEST SUMMARY. RANKED. NO PROPOSAL.

Ranked by the size of the separation, with the n behind each and the risk of acting on it.

| # | lever | the separation | n behind it | risk of acting |
|---|---|---|---|---|
| **1** | **Intra-conflict presence** (any category silenced by its own disagreement) | **+0.536R vs −0.22R**, 85.7% vs ~36% win | **14 vs 25** — the largest n of any lever here | 🔴 **It would refuse 59.1% of all entries.** The kept cell is the best in the book, but the sample is 34/39 paper and the effect is non-monotonic in the 1-vs-2 cells |
| **2** | Entry *location* — continuation vs the prior 24h extreme | SHORT +0.702 vs −0.302 · LONG +0.161 vs −0.596 | 12/13 and 7/7 | 🔴 Thin per side, survives its confound check, and is **a new gate concept**, not a tightening of an existing one |
| **3** | "At least two categories must contribute" | +0.118R vs −0.512R | 34 vs **5** | Mostly a **proxy for lever 1** — all 5 blocked trades are conflicted. Blocking 15.2% of entries on n=5 |
| **4** | Today's 3.0/5.0 bar applied to the old book | kept +5.90R, blocked −4.44R | 31 vs 8 | **Already shipped** (`dee6cee`). Recorded here as the benchmark any new lever must beat |
| **5** | Halving / majority-carry the conflicted category | changes **0** gate outcomes (half) or admits 1 loser (major) | 8 of 39 move | **Cannot filter — it only raises scores.** Not a candidate for reducing bad entries |
| **6** | An ADX-based FLAT floor | **no separation on either timeframe**; sub-floor is the best 4h cell | 7 / 14 / 18 and 11 / 12 / 16 | 🔴 **Acting here would be aimed at the wrong variable** |
| **7** | Opposing-tier rule | n=3 vs n=3; the live-opposing comparison cell is **empty** | 6 total | **Not measurable.** Needs ~20 more entries carrying `entry_tiers_json` |

### What I am NOT saying

- **No change is proposed**, and none of the above is a recommendation.
- **Levers 1 and 3 are one effect**, not two. Counting them separately would overstate the case.
- **The sample is 34/39 paper**, spanning a 68× notional change. R normalises size and nothing else.
- **Every cell under n=8 is reported and not concluded on** — that covers 3-zeroed (n=2), the
  suppressed-AGREED cell (n=3), all of §3, and the LONG halves of §4's location split.
- **vpos 91 is not evidence.** It sits in the `2 zeroed` cell, which runs −0.086R on n=12 — an
  ordinary cell, not a disaster one. Three flagged trades cannot carry a gate change, which is why
  the ranking above rests on n=39 and states where n runs out.

**The one finding that would change what a fix should even target:** the scorer has **no negative
contribution**. Dissent, conflict and opposition can currently only fail to add — never subtract.
Any lever intended to make disagreement *cost* something is not a threshold change; it is a change
to the shape of the score.
