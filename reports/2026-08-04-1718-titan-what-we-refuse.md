# WHAT ARE WE REFUSING THAT WE SHOULD NOT? — NOTHING THAT SURVIVES

**2026-08-04 17:18 UTC · Titan LIVE, real money, flat · HEAD `be53e63` · READ-ONLY, nothing applied**

**Bonferroni stated up front, not appended: 54 cells tested → α = 0.05/54 = 0.00093 → a cell needs
|t| > 3.31.** Sign convention (OPEN-ITEMS §0): **positive = the refused signal would have won.**

**Pre-registered branch 2 fired: no cohort survives. "The cascade is refusing correctly" is the
answer, and the question closes.**

Canon: **§2.54**. Snapshot: `reports/2026-08-04-1718-open-items.md`.

---

## 🔴 0. THE SHORT VERSION

Six pockets inside `htf_blocked` looked positive, and one cell in `ai_skipped` cleared Bonferroni
outright. **Every one of them is a clock artifact or a day-mix artifact.** The single most important
number in the pass is this one:

```
the 1H-alone pocket's excess drift, by control specification
  none (raw)        +0.0557%  t= +2.68   n=1595
  + day             +0.0868%  t= +3.95   n=1595
  + day+direction   +0.2170%  t= +9.08   n=1595
  + day+dir+6h      +0.2659%  t=+11.75   n=1434
  + day+dir+HOUR    -0.0858%  t= -3.23   n= 217    <-- THE SIGN FLIPS
```

**An effect whose sign depends on the control is not an effect.** Drift is a clock — the same shape
depth turned out to have on Mercury-SOL.

## 1. §1 — WHERE THE POSITIVE DRIFT IS INSIDE `htf_blocked` (raw, before de-confounding)

Aggregate: **+0.0200 % at 4h (t=+1.92, n=5982)** — and it decays with horizon: +0.0088 % at 12h,
+0.0057 % at 24h.

| split | cell | n | 4h drift | t |
|---|---|---|---|---|
| **§1e block kind** | **OPPOSING** | 3900 | **+0.0336 %** | +2.49 |
| | NEUTRAL/expired | 2082 | −0.0053 % | −0.33 |
| **§1a which tier** | blocked by **1H alone** | 1595 | **+0.0557 %** | +2.68 |
| | blocked by **15m alone** | 1891 | +0.0476 % | +2.48 |
| | NEUTRAL-only 1H+15m | 1452 | +0.0057 % | +0.32 |
| | 🔴 **1H AND 15m both opposing** | 414 | **−0.1160 %** | **−2.59** |
| **§1b direction** | SHORT | 3109 | +0.0429 % | +3.11 |
| | LONG | 2873 | −0.0047 % | −0.30 |
| **§1c regime** (per §0, from `matrix_breakdown_json`) | TREND | 2486 | +0.0380 % | +2.29 |
| | FLAT | 3496 | +0.0073 % | +0.54 |
| **§1d would-be score** | [1.75, 3.50) | 2571 | +0.0482 % | +3.07 |
| | [3.50, ∞) | 1624 | −0.0025 % | −0.13 |

**§1e is the most informative split and it answers the brief's suspicion:** the two halves *do*
behave differently — **OPPOSING +0.0336 % vs NEUTRAL/expired −0.0053 %** — and **when two tiers
oppose, refusing is emphatically right (−0.1160 %)**. The cascade's veto gets *better* the more tiers
agree on it.

## 2. §2 — THE SAME CUT ON THE OTHER GATES

| gate | cell | n | drift | t |
|---|---|---|---|---|
| `ai_skipped` | ALL 4h | 2000 | −0.0594 % | −3.23 |
| 🔴 | **ALL 12h** | 2000 | **+0.1802 %** | **+6.51** |
| | ALL 24h | 1991 | +0.1548 % | +3.88 |
| | regime TREND | 1075 | **−0.1609 %** | −6.89 |
| | blocked by 5m alone | 115 | **−0.3851 %** | −4.32 |
| `below_threshold` | ALL 4h | 875 | −0.0728 % | −2.75 |
| | regime TREND | 80 | **−0.4831 %** | −4.47 |

**The guard the brief asked for paid off immediately:** `ai_skipped`'s aggregate is *negative* at 4h
and strongly *positive* at 12h — **the only cell in the entire pass to clear Bonferroni raw.** Reading
the 4h aggregate as the whole story would have missed it.

## 3. §3 — DE-CONFOUNDING, WHICH IS WHERE EVERYTHING DIED

**(a) Matched baseline — same day, same direction** (the method used on SOL's daily brake):

| cell | raw | excess vs same-day/same-direction | verdict |
|---|---|---|---|
| 🔴 `ai_skipped` 12h | +0.1802 % | **−0.0495 % (t=−2.50)** | **the days, not the selection** |
| `htf_blocked` SHORT | +0.0429 % | +0.0224 % (t=+1.86) | gone |
| blocked by 15m alone | +0.0476 % | +0.0013 % (t=+0.08) | gone |
| score [1.75,3.50) | +0.0482 % | +0.0460 % (t=+3.28) | under the 3.31 bar |
| blocked by 1H alone | +0.0557 % | +0.2170 % (t=+9.08) | survives (a) |
| OPPOSING | +0.0336 % | +0.0561 % (t=+4.66) | survives (a) |
| regime TREND | +0.0380 % | +0.0927 % (t=+6.00) | survives (a) |

**(b) Time of day — and a methodological trap I walked into and caught.** My first within-hour
control returned ≈ 0 for everything. **It was degenerate: the cell was 100 % of its own stratum at
the median** (85–93 % of strata >80 % cell), so it was comparing the cohort with itself. Re-run with
the baseline **excluding the cell's own rows**:

| cell | vs ADMITTED signals, same day+direction+hour | n usable |
|---|---|---|
| ALL `htf_blocked` | **+0.0105 % (t=+0.74)** | 670 |
| OPPOSING | +0.0118 % (t=+0.41) | 254 |
| regime TREND | +0.0593 % (t=+2.21) | 138 |
| **blocked by 1H alone** | — | **3 pairs. Untestable.** |

**Nothing significant.** And the three cells that survived (a) are precisely the ones whose (b) result
either vanishes or cannot be computed.

### 🔴 The structural limit that caps this question permanently on this data

- **(day, direction, hour) strata: 1,639. Only 234 (14 %) contain both a refused and an admitted
  signal. 902 (55 %) contain refusals only.**
- **Only 932 of 5,982 `htf_blocked` rows (16 %) have a same-hour admitted comparator.**

**The cascade refuses so much that its refusals *are* the hour.** There is no clean within-hour
control to be had, which is why the 6h-bucket and exact-hour specifications disagree so violently.

## 4. §4 — THE DECISION

**Branch 2: no cohort survives → nothing to propose, and the question closes.** Not "no cohort
reached significance this time" — **the effect reverses sign under the tightest control and the
control itself has 16 % coverage.** Re-running this on the same data will not produce a different
answer.

**De-confounded away, by name, so they are not rediscovered:** `htf_blocked` 1H-alone · OPPOSING ·
regime TREND · SHORT · score [1.75,3.50) · 15m-alone · and `ai_skipped`'s 12h aggregate.

**What is affirmatively supported instead:** the cascade's veto is *most* right where it is *most*
confident — two opposing tiers −0.1160 %, and the advisor's refusals in trending regimes −0.1609 %.
**The gates are not leaving money on the table in any way this data can detect.**

## 5. THE TWO CAVEATS THE BRIEF REQUIRED

⚠️ **DRIFT IS NOT PnL.** It measures whether price moved the refused signal's way — **no stop, no
trail, no fees, no partial**. A positive drift would have meant we refused a **move**, not
necessarily a **winner**. Every number above is in that weaker currency.

⚠️ **The geometry changed at 17:01:29 UTC**, so any forward-looking cost must use the **new 1R**
(§0 boundary). For scale only, since nothing is proposed: the 1H-alone pocket is **27 % of all
blocks = +37 signals/day** at the score gate → after the EMA envelope gate, the score bar and the
advisor, roughly **+0.45 entries/day**, which would about **double** today's 0.47/day. **That is the
risk class a cascade relaxation belongs to** — and it is why the brief said propose-and-stop, and why
nothing is proposed.

## 6. SCOPE

**Read-only.** `git status` clean at `be53e63`, 0 open positions, no restart, no table written. The
HTF cascade, the EMA envelope gate, the FLAT floor, Variant-B, the score bars, the risk gates and
both advisor prompts are untouched.
