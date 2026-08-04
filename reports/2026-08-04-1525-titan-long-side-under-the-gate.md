# THE LONG SIDE, MEASURED UNDER THE LIVE GATE — YOUR LEAK IS ALREADY 98.5 % CLOSED

**2026-08-04 15:25 UTC · Titan LIVE, real money, flat · HEAD `a637071`, UNCHANGED — no code shipped**

You reopened branch 2 and pre-registered four outcomes before the numbers existed. **Outcome 2
fired — *overlap near-total → apply nothing, and say the gate already does the work*.** This is that
statement, with the arithmetic that forces it.

Basis: `reports/2026-08-04-1425-titan-asymmetric-entry-measured.md` §1a · the EMA envelope gate
applied 14:41 (§2.47). Canon: **§2.48** added in the same commit; snapshot
`reports/2026-08-04-1525-open-items.md`.

---

## 🔴 THE ANSWER IN FOUR LINES

```
The daily-bear LONG leak you targeted, from the 14:25 report   n=13   sumR  -4.25
  ├─ ALREADY REMOVED by the EMA envelope gate (14:41)          n= 9   sumR  -4.19   ← 98.5% by R
  └─ still admitted — i.e. what your veto would refuse         n= 4   sumR  -0.06
```

**Your instinct about the leak was right. The gate you applied 24 minutes earlier already closes it.**
The four survivors are **all paper-era**, three of them fail §0's cleanliness filters, and the newest
is **2026-07-04**. A daily-bear LONG veto would refuse those four, worth **−0.06R**, and — measured
forward — **none of the last 25 entries**.

---

## 1. THE NUMBERS THAT DID NOT EXIST BEFORE THIS PASS

### 1a. PASS·LONG by DAILY regime — the bear cell is the LEAST bad, not the worst

Regime = your own definition: EMA9 vs EMA21 with an EMA21 slope condition, **closed daily candles
only**, real BingX candles.

**ALL 59**

| cell | n | win | sumR | meanR |
|---|---|---|---|---|
| PASS·LONG · daily **bull** | 4 | 50.0 % | −0.65 | **−0.162** |
| PASS·LONG · daily **flat** | 4 | 0.0 % | −1.19 | **−0.298** |
| PASS·LONG · daily **bear** | 4 | 50.0 % | **−0.06** | **−0.016** |
| *PASS·LONG total* | *12* | *33.3 %* | *−1.91* | *−0.159* |
| *FAIL·LONG total (the gate already refuses these)* | *14* | *28.6 %* | *−6.04* | *−0.432* |

**§0-CLEAN 40**

| cell | n | win | sumR | meanR |
|---|---|---|---|---|
| PASS·LONG · daily **bull** | 3 | 66.7 % | +0.34 | +0.115 |
| PASS·LONG · daily **flat** | 1 | 0.0 % | −0.44 | −0.440 |
| PASS·LONG · daily **bear** | 1 | 100 % | **+0.71** | +0.706 |
| *PASS·LONG total* | *5* | *60.0 %* | ***+0.61*** | *+0.122* |
| *FAIL·LONG total* | *10* | *40.0 %* | *−4.38* | *−0.438* |

**The ordering your rule assumes is not there.** Under the gate, daily-bear is the **best** of the
three long cells on the pooled book and the best on the clean cohort too. Permutation test,
PASS·LONG bear vs non-bear: **Δ+0.214, p = 0.603.**

The cells that carried "longs lose in bear" — **FAIL·LONG · daily bear, n=9, −4.19R** — are exactly
the ones the envelope already refuses.

### 1b. The 4h contradiction — it survives, and it collapses to n=1

You asked me to reconcile it or say plainly that the two timeframes disagree. **They disagree, and
under the gate the contrary cell is one trade.**

| 4h regime | LONG total | gate admits | gate refuses |
|---|---|---|---|
| bull | n=14 · −5.78R | **n=9 · −3.21R** | 5 |
| flat | n=7 · −2.82R | n=2 · +0.27R | 5 |
| **bear** | n=5 · **+0.65R** | **n=1 · +1.04R** | 4 |

The strange cell from the 14:25 report — longs doing best in a 4h downtrend — is **4 of its 5 members
removed by the envelope**. What remains is a single trade. **Neither timeframe can carry a rule
alone**, and the 4h reading is now too thin to contradict anything. I am not reconciling them with a
story; the honest statement is that they point opposite ways and only one of them has n.

*(Your standing instruction — that you would hold "do not buy in a daily downtrend" against a thin
contrary 4h reading, but never a rule that says buy INTO a 4h downtrend — is not reached: the daily
side of the trade-off did not survive its own measurement.)*

### 1c. Overlap — 69.2 % by count, **98.5 % by R**

| daily regime | LONG entries | gate refuses | % refused | survivors' sumR |
|---|---|---|---|---|
| bull | 8 | 4 | 50.0 % | −0.65 |
| flat | 5 | 1 | 20.0 % | −1.19 |
| **bear** | **13** | **9** | **69.2 %** | **−0.06** |

**The envelope is already regime-selective without being told about regime** — its refusal rate is
highest exactly where you wanted a second condition. That is the overlap, and it is why a second
condition buys −0.06R.

---

## 2. THE DECISION — outcome 2, and why not the others

**APPLIED: NOTHING. No constant, no status, no card, no restart.** `git status` clean at `a637071`,
the binary running since 15:08:30.

This is not "keep measuring". The rule you pre-registered would, measured against real stored trades,
**refuse four paper-era entries worth −0.06R and zero of the last 25**. The work it was meant to do
has already been done by a gate that is live.

| your branch | condition | verdict |
|---|---|---|
| 1 · refuse LONG in daily-bear | bear materially worse **and** overlap not near-total | **FAILS on both conjuncts.** Bear is the least-bad cell (p=0.603); overlap is 98.5 % by R |
| **2 · apply nothing, the gate does the work** | overlap near-total | 🔴 **FIRED** |
| 3 · apply the daily rule despite the 4h | daily and 4h contradict, neither clean | **Not reached.** It presupposes the daily result supports the veto; under the gate it does not |
| 4 · suspend the long side, auto re-arm at 3 bull days | PASS·LONG negative in **every** daily regime **with usable n** | **FAILS.** Cells are **n=4 each** — the guard you wrote is what excludes them — and on the §0-clean cohort two of three cells are **positive** |

### 🔴 What the veto would have cost you TODAY

The daily has been **bear since 08-01** (bull 07-29, flat 07-30 and 07-31). **A daily-bear LONG veto
applied now suspends the entire long side immediately** — on a measured residual of −0.06R, against a
cell whose sign is positive on the clean cohort. That is the concrete price of the rule, today, and
it is why "the gate already does the work" is the safer of the two errors available.

### Counterfactual pre-registration, recorded even though nothing shipped

- **Last 30 days:** 322 LONG signals reached the score gate; the envelope admits **51**; only
  **6 of those 51 (11.8 %)** sat in a daily-bear tape.
- **Of the last 25 entries it refuses: NONE.**
- **Entries/day after:** unchanged at **0.47/day** — the rule is inert on the current sample.
- **Review point had it been applied:** 20 executed LONG entries, not calendar time.

---

## 3. ⚠️ WHAT THIS IS NOT — read this before treating the long side as settled

**`PASS·LONG` is −1.91R (n=12) pooled and +0.61R (n=5) on the §0-clean cohort.** The two cohorts
disagree in sign. **The long side under the gate is not demonstrated profitable — it is undetermined
at this n**, and I am not dressing "undetermined" as "fine".

What "undetermined" does **not** license is a suspension: your branch 4 was written to require usable
n precisely so that four-trade cells could not trigger it. Holding to that is the same discipline
that made the pre-registration worth writing.

**What would change the decision, stated now so it cannot be invented later:**

1. **PASS·LONG accumulating negative across daily regimes at n ≥ 8 per cell** → branch 4's condition
   is met on its own terms, and the suspension with the 3-bull-day auto re-arm becomes the honest
   move.
2. **A daily-bear PASS·LONG cell that turns materially negative at n ≥ 8** → branch 1 re-opens, this
   time with the sign pointing the right way.
3. **A genuine second bull episode.** The book still holds exactly one (07-10 → 07-28, 19 of 73 days).
   Everything above is measured in a tape that has been bear for 63 % of the book and is bear again
   today.

**The measurement is mechanical to repeat** — it is the same offline replay inlined in the 14:25
report, plus the envelope predicate `ema_gap_dir_1h == 'Expanding' AND ema_gap_dir_15m == 'Expanding'`
read from the `trades` row. No code in the hot path, nothing to remember.

## 4. SCOPE

**Nothing was touched.** The EMA envelope gate (14:41), the HTF cascade, the FLAT floor, Variant-B,
the score bars, the risk gates, both advisor prompts and the entire exit side (unfrozen at 15:08 and
deliberately left alone in this pass) are all unchanged — there is no diff. All measurement ran
**read-only** against `trades.db` and the BingX candles already cached in scratch. **No table was
written.**
