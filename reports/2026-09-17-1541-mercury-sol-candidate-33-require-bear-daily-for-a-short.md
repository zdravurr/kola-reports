# CANDIDATE 33 — "REQUIRE A BEAR DAILY FOR A SHORT, NOT MERELY NOT-BULL"

**2026-09-17 15:41 UTC · READ-ONLY pass · subject: Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · Titan untouched**

`openitems_guard` → **exit 0** (titan-bot HEAD `f16c271`). Same book, same frame, same five controls that killed
candidates 21, 22, 29, 30, 31 and left 32 unconvicted: [candidate 32 —
long-only](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-09-17-1516-mercury-sol-long-only-candidate-32.md).

---

## 🔴 VERDICT FIRST: **0 OF 5 CONTROLS PASS. CANDIDATE 33 FAILS HARDER THAN 32.**

Two facts sink it before any statistic:

1. **On the live book, candidate 33 is not a different rule from candidate 32. It is the same rule.**
   It refuses live positions `[32, 34, 35, 36, 37, 42, 44, 45, 46, 47]`. Long-only refuses
   `[32, 34, 35, 36, 37, 42, 44, 45, 46, 47]`. **Zero rows distinguish them.** The live book has no BEAR daily,
   so "require BEAR" and "take no shorts" are the same instruction on every row that exists.
2. **On paper — the only book that has a BEAR leg at all — the rule's premise is refuted, not merely
   unsupported.** Shorts with a BEAR daily did **worse** than shorts with a NEUTRAL one, on every measure.

---

## 0. THE CANDIDATE IS MIS-SPECIFIED: THERE IS NO "NOT-BULL" RULE TO IMPROVE ON

The name contrasts "require BEAR" against "merely not-bull". **Neither exists today.** `trend_1d` is recorded on
every trades row and **gates nothing**. The HTF alignment gate — the largest skip category in the live era,
3,698 rows — runs on the **1H / 15m / 5m** tiers only (`main.py:4126`, `_tiers = (('1H',_t1),('15m',_t15),('5m',_t5))`).
The daily never enters an entry decision.

That is not an inference from the code alone; the book proves it. **Two live shorts entered under a BULL daily**
— #32 (2026-08-10, `trend_1d=bull`) and #34 (2026-08-13, `trend_1d=bull`). A not-bull rule would have refused
them. Nothing did.

So candidate 33 does not tighten an existing daily filter. **It would put the daily into the entry path for the
first time.** And the weaker rule it claims to beat is, on the evidence:

| rule | LIVE shorts refused | PAPER shorts refused |
|---|---|---|
| require `trend_1d == bear` | **10 of 10** | 6 of 13 |
| require `trend_1d != bull` | 2 of 10 (#32, #34) | **0 of 13 — literal no-op** |

**The comparison the candidate is named after cannot be made on either book.** On live, require-BEAR collapses
into long-only. On paper, not-bull changes nothing at all — no paper short ever had a bull daily.

---

## 1. THE CELLS

| book | side | `trend_1d` | n | wins | ΣR | mean R | median MFE |
|---|---|---|---|---|---|---|---|
| **PAPER** | SHORT | **bear** | 7 | 2 (29%) | **−0.878** | **−0.125** | **+0.53R** |
| **PAPER** | SHORT | **neutral** | 6 | 4 (67%) | **−0.450** | **−0.075** | **+1.08R** |
| PAPER | SHORT | bull | 0 | — | — | — | — |
| LIVE | SHORT | **bear** | **0** | — | — | — | 🔴 **EMPTY** |
| LIVE | SHORT | neutral | 8 | 1 (12%) | −6.710 | −0.839 | +0.34R |
| LIVE | SHORT | bull | 2 | 0 (0%) | −0.823 | −0.411 | +0.31R |

**The BEAR cell is the worse cell on paper, on all four measures** — win rate 29% vs 67%, mean R −0.125 vs
−0.075, ΣR −0.878 vs −0.450, and median excursion +0.53R vs **+1.08R**. Paper shorts reached *twice as far*
under a NEUTRAL daily as under the BEAR daily the candidate wants to require.

* paper BEAR vs paper NEUTRAL, mean R: permutation **p = 0.9375**
* paper BEAR vs paper NEUTRAL, win counts: Fisher **p = 0.2861**

Not significant at 0.05, let alone at the corrected threshold — and **what sign there is points the wrong way.**

---

## 2. THE SUBTRACTION

| book | full book | with the rule | entries removed | short-side expectancy |
|---|---|---|---|---|
| **LIVE** | n=19, ΣR **+4.920**, $ +11.08 | n=9, ΣR **+12.453**, $ +24.32 | **10 of 19 (53%)** | −0.753R → **n/a (side extinct)** |
| **PAPER** | n=22, ΣR **−5.374**, $ −1128.46 | n=16, ΣR **−4.925**, $ −1098.21 | 6 of 22 (27%) | −0.102R → **−0.125R 🔴 WORSE** |

The live column is not evidence *for* candidate 33 — it is candidate 32's column, copied, because the two rules
select identical rows there.

The paper column is the one that carries information, and it is damning: **the rule improves ΣR only by cutting
volume, while making the surviving side's per-trade expectancy worse** (−0.102R → −0.125R). You pay 6 entries
to keep the cell that loses more per trade.

---

## 3. THE FIVE CONTROLS

> **BONFERRONI DECLARED IN THE HEADER.** Frame unchanged: side × regime × book = 2 × 3 × 2 = **m = 12**,
> corrected **α = 0.05/12 = 0.004167**. Two-sided permutation on mean R (200,000 resamples, seed 20260917) and
> Fisher exact on win counts.

### (a) Bonferroni — **FAILS**
The rule's defining test is BEAR vs NEUTRAL within the short side. Paper: **p = 0.9375** (mean R), **p = 0.2861**
(wins). Live: **untestable, BEAR leg n=0.** Nothing on the board approaches 0.004167, or even 0.05.

### (b) Chronological halves — **FAILS. Both cells flip sign inside themselves.**

| cell | H1 | H2 | same sign? |
|---|---|---|---|
| paper SHORT **bear** | n=4, ΣR **−1.322**, 1 win | n=3, ΣR **+0.444**, 1 win | ❌ **flips** |
| paper SHORT **neutral** | n=3, ΣR **+0.207**, 2 wins | n=3, ΣR **−0.657**, 2 wins | ❌ **flips** |

Neither cell is stable over its own life. There is no persistent BEAR effect to gate on — the sign is a
coin-flip on sub-samples of 3 and 4.

### (c) Regime split with BOTH legs populated — **FAILS, and fatally, because the candidate *is* the regime**
The live BEAR leg is **n = 0**. 38 live-era days carry signal rows; **not one contains a BEAR 1d row.** The last
BEAR daily anywhere in the database is **2026-08-07**, the day before live trading began.

For candidate 32 the empty BEAR leg was a missing control. **For candidate 33 the empty BEAR leg is the entire
proposed trigger.** The rule cannot be tested on the live book at all — it has never once been satisfiable.
Reported as a failure, not as a one-legged result.

### (d) PAPER AS THE INDEPENDENT SAMPLE — **FAILS, and worse than candidate 32 failed it**
Candidate 32 failed (d) because paper *inverted* the live finding. Candidate 33 fails it more directly: **paper
is the only book with any BEAR data at all, and it refutes the premise outright.** The bear daily did not help
paper shorts — 2 of 7 against 4 of 6 with neutral, mean R −0.125 against −0.075, median MFE +0.53R against
+1.08R.

This restates the 2026-09-14 finding, and the same caveat applies: **paper is frozen at 2026-08-07** and cannot
be re-run. But note the asymmetry — for candidate 32, frozen paper merely blocks re-testing. For candidate 33,
frozen paper is the *only* evidence that will ever exist until the live book sees its first BEAR daily, and
that evidence says no.

### (e) THE CONFOUND — **FAILS. Perfect collinearity, and with an already-unconvicted candidate**
On the live book, "require BEAR for a short" and "take no shorts" select **identical row sets. 0 distinguishing
rows.** Any live support candidate 33 appears to have *is* candidate 32's support — and candidate 32 was **not
convicted**. Borrowing the evidence of an unconvicted candidate does not make a new one.

This is the same structure that killed candidate 31, where a trigger name *was* its side, and it is one degree
worse here: there the two things merely co-occurred, here they are the same set.

---

## 4. WHAT WOULD SETTLE IT

Candidate 33 discards the entire −7.533R live short history as "traded in the wrong regime". **Its cell must
therefore stand alone** — it cannot inherit credit from trades it would have refused.

1. **n ≥ 8 live SHORT entries with `trend_1d = bear` at entry** — the book's own refuse-to-rank line. That cell
   is n=0 today and has been unsatisfiable for 41 days.
2. **Those 8 must be profitable on their own: mean R > 0, ΣR > 0.** Not "less bad" — the rule's whole claim is
   that the BEAR daily is what makes a short work.
3. **They must beat the live NEUTRAL cell (1 win in 8) by enough to clear Bonferroni.** The arithmetic:

| BEAR cell result | vs live NEUTRAL 1/8, Fisher p | clears α=0.004167? |
|---|---|---|
| 4 of 8 wins | 0.28205 | no |
| 5 of 8 | 0.11888 | no |
| 6 of 8 | 0.04056 | no |
| 7 of 8 | 0.01010 | no |
| **8 of 8** | **0.00140** | ✅ **yes** |
| 9 of 10 | 0.00288 | ✅ yes |
| 11 of 12 | 0.00077 | ✅ yes |

**At n=8 the rule needs a perfect 8-for-8 to convict.** At n=10, 9 of 10. That is the price of a 12-cell
correction against a baseline that has already won once in eight.

4. **To kill it permanently:** ≤ 3 of 8 winners with ΣR < 0 — the BEAR daily supplies nothing the NEUTRAL one
   did not, exactly as paper already says. Close the line.
5. **Control (d) can never be satisfied from live data.** Paper is frozen. A second independent sample requires
   re-opening a paper/shadow stream, or scoring the `skip_attribution` counterfactual — the live era already
   holds **3,880 SHORT skip rows** carrying `max_favorable_price` drift tracking, including every short the bot
   declined under a non-bear daily.

---

## 5. THE ONE FRAGMENT WITH LIVE SUPPORT — AND WHY IT IS NOT A CANDIDATE

The **weaker** rule, not the proposed one, is the only version with any live signal: refusing shorts under a
**BULL** daily would have cut #32 (−0.180R) and #34 (−0.643R), **both losers, ΣR −0.823**.

That is n=2. It is a quarter of the refuse-to-rank line, it is worth −0.823R against a −7.533R problem, and on
paper it is a literal no-op (0 of 13 rows). **I am not proposing it and it is not candidate 34.** It is recorded
here so the next pass does not rediscover it and mistake 2 rows for a finding.

---

## 6. RECORD

**CANDIDATE 33 — "require a BEAR daily for a short, not merely not-bull" — NOT CONVICTED. Nothing applied.**

Controls: **(a) FAIL** p=0.9375 · **(b) FAIL** both cells flip sign · **(c) FAIL** live BEAR leg n=0, the
trigger has never been satisfiable · **(d) FAIL** the only book with BEAR data refutes the premise · **(e) FAIL**
row-identical to candidate 32 on live.

**0 of 5.** Candidate 32 at least passed the chronological-halves control on its live short side; candidate 33
passes nothing. It is a rule whose trigger has never fired in the live book, whose premise is contradicted on
the only book where it could fire, and which — where it *can* be evaluated live — is arithmetically the same
instruction as a candidate that was already refused.

---

## READ-ONLY CONFIRMATION

| check | state |
|---|---|
| `openitems_guard` | **exit 0** — run first |
| SOL DB | `file:…/trades.db?mode=ro` + `PRAGMA query_only=1` (verified = 1). **No writes.** |
| SOL config | read via `ast.literal_eval` on source text. **Never imported.** sha256 `a308a130…149c7` unchanged |
| Venue | **GET only**, no new calls this pass (figures reused from the 15:16 pass) |
| `mercury-sol.service` | `NRestarts=0`, PID 2245907 — **unchanged, not restarted** |
| `titan.service` | `NRestarts=0`, PID 1572470 — **unchanged, not restarted** |
| `FLAT_ADX_GATE_DRYRUN` | **True** (`config.py:407`) — unchanged |
| `BOOK_GATE_DRYRUN` | **False** (`config.py:475`) — unchanged |
| **Titan** | **UNTOUCHED** |
| Applied | **nothing.** No diff, no flag, no proposal beyond the §5 note recorded as a non-candidate. |
