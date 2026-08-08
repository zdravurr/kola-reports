# sol-opposing-wall-does-not-separate-filter-21-refused

_2026-08-08 16:44 UTC_

---

# Mercury-SOL — the opposing wall does NOT separate. Filter #21 is refused. But the advisor finding is worse than you thought.

**§1 answer: NOTHING SEPARATES. Not one contrast survives Bonferroni, the realised-R
test is not computable at all (n=2), and the whole signal is confounded with six days.
So per your own §3 I have built NOTHING and there is no diff to approve.**

🔴 **§3 answer, and this is the real result: the advisor's execute decision is
*exactly* statistically independent of the wall data it is given — Fisher exact
p = 1.0000. It mentions walls in 81.6% of its reasons and uses the percentile in
6.6%. The three false claims are not three slips; they are a visible symptom of a
channel that is decorative end to end.**

Read-only pass. Nothing was changed, nothing restarted, vpos 29 untouched, Titan untouched.

Prior: [§1b/§1e of the 15:30 report](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1530-sol-0850-reasoning-judged-apply-guard-and-adoption-diffs.md)

---

## 1(a) THE NEAREST OPPOSING WALL AT DECISION TIME, PER ENTRY

Percentiles computed with `claude_advisor._wall_pctl` — the same function that rendered the prompt,
so these are the numbers the model was actually shown. 1R = `SL_BUFFER_ATR × ATR(1h)`.

```
   row  when              dir    entry   ATR1h |  opp wall  pctl   mult  dist%  distATR | outcome
 15410  2026-08-03 06:45  SHORT  72.53  0.3683 |     72.25   p99  x30.6  0.39%    0.76A | vpos27 R=-0.660
                                                     71.75   p37   x6.2  1.08%
                                                     70.75    p5   x4.2  2.45%
 16405  2026-08-06 19:00  SHORT  72.77  0.3944 |     72.75   p93  x19.1  0.03%    0.05A | vpos28 R=-0.153
                                                     72.25   p74  x12.9  0.71%
                                                     71.75    p7   x4.3  1.40%
 16748  2026-08-08 06:50  LONG   74.78  0.3934 |     75.25   p69  x11.5  0.63%    1.19A | emergency-closed
 16749  2026-08-08 06:50  LONG   74.78  0.3934 |     75.25   p69  x11.5  0.63%    1.19A | failed (dup thread)
 16765  2026-08-08 08:35  LONG   74.84  0.3676 |     75.25   p69  x11.6  0.55%    1.12A | failed (dup thread)
 16766  2026-08-08 08:35  LONG   74.84  0.3676 |     75.25   p69  x11.6  0.55%    1.12A | emergency-closed
 16767  2026-08-08 08:50  LONG   74.78  0.3676 |     75.25   p64  x10.6  0.63%    1.28A | vpos29 OPEN
                                                     75.75   p64  x10.5  1.30%
                                                     79.25    p5   x4.0  5.98%
```

**Every one of the seven had an opposing wall.** The two SHORTs had genuinely thick ones — **p99 at
0.76 ATR** and **p93 at 0.05 ATR** — and both lost. That is the most suggestive thing in this report
and it is n=2.

---

## 1(b) 🔴 THE OUTCOME SPLIT YOU ASKED FOR CANNOT BE RUN — AND THAT IS THE FINDING

```
closed positions, all time                          : 22
...whose ENTRY row carries an OKX-4000 book         : 2      <- both SHORT, both losers
```

**Why the other 20 are unusable.** All 22 outcomes were booked against the **old shallow book**, and
**19 of the 22 recorded ZERO walls on either side**. That is precisely the defect
`virtual_trader.py:1274` already names — *"row 15093 stored `walls_ask: []` from Bybit depth-20 at
the same instant the advisor was shown a ×20.3 wall at \$73.75 from OKX-4000."* The advisor saw one
book; the ledger stored another.

`advisor_book_json` (OKX-4000) only starts **2026-08-02 17:10**. Since then exactly two positions
have closed.

**Power, stated before any test:** with n=2 the minimum two-sided Fisher p is **1.0**. No
arrangement of two observations reaches an unadjusted 0.05, let alone
**α = 0.05/8 = 0.00625**. 🔴 **This is not a null result — it is an absence of data.** Reporting "no
effect" from n=2 would be the fabrication this book has a standing rule against.

### So I ran the honest substitute, and said so up front

**Forward return in the PROPOSED direction**, on all **396** OKX-4000 book rows — what the entry was
betting on, measured without a stop or a trail. It is *not* realised R and I am not calling it that.

**+12h (the median closed-position hold is 12.1 h), all sides:**

| opposing wall | n | win% | mean | median | ΣR | med MFE (R) | med MAE (R) |
|---|---|---|---|---|---|---|---|
| none | – | – | – | – | – | – | – |
| p<50 | 3 | 33.3% | −0.748% | −1.709% | −2.2% | 0.69 | 2.15 |
| p50-79 | 146 | 62.3% | +0.220% | +0.406% | +32.1% | 0.70 | 0.51 |
| **p80+** | **247** | **59.5%** | **+0.000%** | **+0.297%** | **+0.1%** | 0.62 | 0.58 |

**By side:**

| | LONG n | LONG mean | SHORT n | SHORT mean |
|---|---|---|---|---|
| p50-79 | 85 | +0.119% | 59 | +0.369% |
| p80+ | 61 | **−0.165%** | 181 | +0.059% |

**By distance:** ≤1 ATR — n=331, 57.4% win, +0.003%; 1–2 ATR — n=65, 75.4% win, +0.446%.

Every contrast leans the same way: a thick overhead wall is *slightly* worse. Directionally
consistent. Now the bar.

---

## 1(d) DE-CONFOUNDING AND BONFERRONI — WHERE IT DIES

**Family = 12** (3 band contrasts × 2 sides × 2 horizons). **α = 0.05/12 = 0.00417.**

```
 +6h ALL    thick n=247 (med -0.041%) vs thin n=149 (med +0.163%)  z=-1.58 p=0.1145  not significant
 +6h LONG   thick n= 61 (med -0.436%) vs thin n= 88 (med +0.020%)  z=-2.08 p=0.0375  FAILS Bonferroni
 +6h SHORT  thick n=181 (med -0.000%) vs thin n= 59 (med +0.270%)  z=-1.54 p=0.1239  not significant
+12h ALL    thick n=247 (med +0.297%) vs thin n=149 (med +0.381%)  z=-1.24 p=0.2152  not significant
+12h LONG   thick n= 61 (med -0.256%) vs thin n= 88 (med -0.034%)  z=-0.86 p=0.3914  not significant
+12h SHORT  thick n=181 (med +0.390%) vs thin n= 59 (med +0.532%)  z=-1.84 p=0.0653  not significant
```

**Not one survives.** The best is LONG +6h at p=0.0375 — which is the best of six, and fails the bar
by a factor of nine.

**And the confound is fatal on its own.** The whole window is six days:

```
2026-08-02  n= 37  mean +0.256%   p80+ share 86.5%
2026-08-03  n= 46  mean -0.142%   p80+ share 82.6%
2026-08-04  n= 97  mean +0.277%   p80+ share 57.7%
2026-08-05  n= 76  mean +0.221%   p80+ share 69.7%
2026-08-06  n= 87  mean +0.035%   p80+ share 47.1%
2026-08-07  n= 24  mean -0.006%   p80+ share 41.7%
2026-08-08  n= 29  mean -0.676%   p80+ share 58.6%
```

The p80+ share swings 41.7%→86.5% **by day**, and the day's mean return swings −0.676%→+0.277%. The
band is a property of the book, which moves with the day's price level, so band and day are
entangled. **Rows are not independent: the effective n is nearer 6 (days) than 396.** This is the
same "independence is a DAY, not a signal" rule that killed earlier candidates on this book.

---

## 1(c) THE TWO CLAIMS, KEPT APART — AND THE SECOND ONE ANSWERED

You were right that these are different claims and only the second matters.

- *"Does the wall hold?"* — already measured: cited walls are traded through **95%** of the time
  within 24h. Not re-litigated.
- *"Does an entry that must EAT a wall do worse?"* — the tables above, at n=247 p80+ rows. **Answer:
  no separation at the bar.**

And the mechanism, measured directly — **price reaches the opposing wall within 12h either way**:

```
p<50     n=  3   reached the wall within 12h: 100.0%
p50-79   n=145   reached the wall within 12h:  79.3%
p80+     n=243   reached the wall within 12h:  82.3%
```

A p80+ wall is reached **just as often** as an ordinary one (82.3% vs 79.3%). It is not a barrier
that stops price arriving, and arriving there does not change the outcome distribution measurably.
The two findings agree: the wall is not load-bearing.

---

## 2. 🔴 NO GATE. NO DIFF. FILTER #21 IS REFUSED.

Your §2 was conditioned on §1 separating. **It did not**, so there is nothing to show and I have
written nothing. Building it anyway would mean:

- a hard pre-advisor refusal keyed to **P and D that the curve does not indicate** — the tables give
  no threshold, only a slope that dies at the bar;
- on a predicate whose realised-R evidence is **n=2**;
- confounded with **six days** of one regime;
- against a book that has already killed **twenty** filters that looked at least this good.

**This would be number twenty-one and it would die the same way.** The honest action is to refuse it
now rather than ship it and discover that in a month.

**What I would accept as evidence later** — pre-registered here so it cannot be moved afterwards:

```
TEST      realised R of CLOSED positions whose entry row carries an OKX-4000 book,
          split p80+ vs thinner, per side, at >=30 per cell
BAR       Mann-Whitney two-sided, alpha = 0.05 / 12 = 0.00417, day-blocked
KILL      if the p80+ cohort is not worse by at least 0.25R median, it is dead
WHEN      closed positions accrue at 0.413/day (22 over 53.3 days), and 2 qualify today
            -> n=30  total  : ~68 days  (~2.3 months)
            -> n=120 (4x30) : ~286 days (~9.5 months)
```

At the current rate a properly powered split is **~9.5 months** away. That is the real cost of the
question, and it is worth knowing before anyone spends more time on it.

---

## 3. 🔴 THE FINDING IS ABOUT THE ADVISOR — AND IT IS BIGGER THAN THREE FALSE CLAIMS

Per your §3, first the part that follows from §1:

**The wall clause was never load-bearing, so the model's false claim cost nothing measurable.** On
the evidence available, saying "no opposing walls above entry" when two sat at p64 did not change
the expected outcome of those entries, because the wall band does not separate outcomes at all.
Recorded that way.

**Now the part that is true regardless, and it is worse than the three claims suggested.**

### (a) The decision is *exactly* independent of the wall data

```
                 execute   skip     P(execute)
  p80+ wall            8    239        3.24%
  thinner/none         5    144        3.36%

  two-sided Fisher exact p = 1.0000
```

**p = 1.0000.** Not "not significant" — the two rates are indistinguishable to the last decimal the
sample can express. If the advisor were using the percentile it is handed and told to judge by, a
genuinely thick opposing wall would suppress execution. It does not, at any bar, in either
direction. **n = 396, which is the one part of this pass that is properly powered.**

### (b) It talks about walls constantly and uses the calibrated figure almost never

```
rows with an OKX-4000 book and a stated reason : 396
reasons mentioning "wall"                      : 323   (81.6%)
reasons citing a PERCENTILE                    :  26   ( 6.6%)
```

The prompt states plainly that the percentile *"is the primary figure"* and that *"the multiple
alone does not distinguish an ordinary wall from a thick one"*. The model cites the percentile in
**one reason in fifteen**, while discussing walls in four out of five.

### (c) The false claims, counted honestly

```
reasons asserting "no opposing wall(s)"        : 5 rows / 3 distinct model calls
...TRUE                                        : 0
...FALSE (the book DID contain one)            : 5  = 100%
percentile of the thickest wall it denied      : min p64 / median p69 / max p69
```

Five rows, but **three distinct consultations** — 16748/16749 and 16765/16766 are duplicate webhook
threads sharing one cached verdict (`[STATE-CACHE] HIT/inflight`). I am not counting one model call
as two. Three calls, three falsehoods, on the only three occasions it made the claim.

### (d) What this means for everything else the advisor says

This is the part that does not depend on walls mattering. The advisor produced a **checkable,
falsifiable statement about its own input and got it wrong on 3 of 3 attempts**, while its decisions
show **zero measurable dependence** on that input across 396 consultations. Its `ai_reason` is
therefore **not evidence of a reasoning process** — it is post-hoc narration that happens to
correlate with the verdict. Any future analysis that treats a cited reason as a mechanism (including
attribution, `consult_for_learning`, and any read of the skip log) is reading a story, not a cause.

**And note what this does NOT license.** It does not follow that the advisor is worthless — its
execute/skip verdict may still carry information from the tiers and the regime. What it means is
narrower and firmer: **the order-book channel of the advisor is dead weight, both in what it says
and in what it does.**

---

## WHAT I DID NOT TOUCH

Read-only throughout. No file was written to `/mnt/volume_nyc1_1780480650620/mercury-sol`, no
service restarted, no prompt altered, no threshold moved, **vpos 29 untouched**, and Titan untouched
(`HEAD 897850b`, master pid 2538048 from Aug 6). Every venue call was a public kline read; the only
DB access was `mode=ro`.

## STATE

```
mercury-sol   active  pid 3533821 / worker 3533987 (since 16:08:56)  open=1  0 tracebacks
venue         LONG 0.9 @ 74.80 · stop 74.95 · vpos 29 managed · unchanged by this pass
titan         active · HEAD 897850b · git clean · NOT TOUCHED
```

**Nothing to approve. The gate was refused, not deferred — and the reason is written down so the
next person who has this idea can read why before spending the time.**
