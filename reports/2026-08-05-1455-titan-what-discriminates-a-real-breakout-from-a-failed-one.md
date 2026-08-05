# TITAN — WHAT DISCRIMINATES A REAL BREAKOUT FROM A FAILED ONE?

**2026-08-05 14:55 UTC · READ-ONLY · nothing changed, NOTHING PROPOSED · HEAD `b9081ad`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
Mercury-SOL never opened. `git status` on `titan-bot` clean before and after.

Parent: `2026-08-05-1210-titan-does-the-flat-gate-make-us-late-to-the-breakout.md`.
Part A companion: `2026-08-05-1425-titan-does-the-order-book-discriminate-real-breakouts.md`.

---

## 🔴 BONFERRONI HEADER — READ BEFORE ANY NUMBER BELOW

**The budget was set at 54. The 12:10 report was cell 56. The 14:25 report spent none.
This brief spends 59 cells, taking the book to cell 115. The bar was already crossed
before the question was asked.**

- Bonferroni α at the stated budget = 0.05 / 54 = **0.000926**.
- 🔴 **NOTHING BELOW CLEARS IT. NOT ONE CELL.** The smallest p in the whole set is 0.0052.
- **Every hit below is labelled NOMINAL and nothing else.** At 59 cells, ~3 nominal hits
  are expected from noise alone; ~7 appeared, and they fall into exactly **two families**,
  both of which are explained mechanically below rather than statistically.

---

## ANSWER IN ONE LINE

**Nothing can see what the flat gate cannot.** Across 105 squeeze episodes on 2.3 years of
BingX candles, **no candle-derived quantity separates a real breakout from a failed one** —
not volume, not box size, not squeeze depth or duration, not higher-timeframe direction, not
the pre-registered pair. **The question closes**, and it closes the §2.45 way — **on evidence,
each branch tested and each failed** — not the 14:25 way, for want of data.

**Two things died in a way worth remembering:**

1. 🔴 **Volume — the classic breakout discriminator — is FLAT AND NON-MONOTONE.** 43.4 % vs
   46.2 % failure across the median split (p = 0.85), and the quartiles run 46 / 38 / 54 / 41 %.
   It has never been tested here; now it has been, and it is nothing.
2. 🔴 **The one candidate with a consistent sign was the OUTCOME DEFINITION READ BACKWARDS.**
   Box size relative to ATR carried the same sign at 8 of 9 squeeze definitions and reached
   nominal at three. It is **entirely arithmetic**: `FAILED` means *"price traversed the
   entire box"*, so the adverse move required to score a failure **is the box width**. The
   adverse excursion actually observed is **identical** in both cells — 4.47 vs 4.53 ATR,
   p = 0.93 — and under every size-invariant criterion the effect vanishes and **the sign
   flips**. This one is worth more than the null it replaces.

---

## §0 — SOURCES, AND WHAT WAS AND WAS NOT RE-DERIVED

| item | provenance |
|---|---|
| the **105 episodes** (t0, box, direction, move) | 🔴 **REUSED, not re-derived** — the 12:10 report's `episodes.pkl`, under the definition fixed there before any result was seen |
| `FAILED` outcome | the 12:10 definition **verbatim** — price traversed the ENTIRE box the other way within 48 h. Independently recomputed here: **47 / 105 = 45 %**, matching 12:10 exactly |
| candles 1h | BingX, 19,921 bars, 2024-04-27 → 2026-08-05 — **the bot's own indicator source** (`main.py:555` `ccxt.bingx`), per §0 of the 12:10 report |
| candles **4h / 1d** | 🔴 **NEW this session** — BingX public REST, 6,599 and 1,299 closed bars, same fetcher shape as 12:10's |
| `ATR`, `trend_1d`, `trend_4h` | the **BOT'S OWN** `indicators.compute_tf_metrics`, imported and called on a 200-bar window (`CANDLE_LIMIT`) — nothing re-implemented (§0 standing rule) |
| `trades.db` | opened **read-only** (`file:…?mode=ro`) throughout — the bot is live and writing |

**The pre-registration is on disk and was written before any Part B number existed**
(`PREREG.md`): outcome variables, all six feature definitions, and — critically — **the one
multivariate pair, named in advance**.

### 🔴 TWO MEASUREMENT BUGS I HIT AND FIXED, RECORDED SO THEY ARE NOT REDISCOVERED

Both were caught by a sanity check, not by a p-value. Both are of the class §0 exists to catch.

1. **`orderbook_density.ts` stores ISO with a `T` separator.** My first coverage query built
   its bound with a **space** separator. `' '` (0x20) sorts before `'T'` (0x54), so
   `WHERE ts <= ?` silently returned the wrong neighbour and reported the nearest book
   snapshot as **359 / 719 / 1319 minutes** away on a feed with **zero gaps over 10 minutes**.
   The right answer is **0.5 min**. A lexical-ordering bug reads exactly like a data outage.
2. 🔴 **`indicators.TREND_BULL` is the string `'bull'`, not `'TREND_BULL'`.** Coding the HTF
   feature against the constant *names* made every non-neutral episode read bearish, which
   made `trend_1d` a **perfect copy of the breakout direction** — every DOWN "aligned", every
   UP "opposed", on both timeframes and both bases. **That is the §2.54 degenerate-control
   trap in a new costume**, and the only thing that caught it was the cross-tab looking too
   clean. The underlying data was healthy all along (bull 46 / neutral 32 / bear 27).

**No look-ahead anywhere.** Every feature is measured at or before t0. The t0 bar's own volume
is used because the breakout is only *knowable* at the t0 close — both are known at the same
instant. Where a label could contain the breakout bar, **both bases are reported** and the
clean one governs.

---

## PART A — THE ORDER BOOK. THE EXIT FIRES.

### A1 — COVERAGE, RE-MEASURED THIS SESSION RATHER THAN CITED

| | |
|---|---|
| table / source | `orderbook_density` — `okx_books_full_4000`, **one source, no mixing** |
| snapshots | **33,258** |
| window | **2026-07-13 02:34:56 → 2026-08-05 14:40:35** = **23.5 days** |
| cadence | **0.98 / min** against a 60 s collector |
| gaps > 10 min | 🔴 **ZERO** |
| episodes with t0 bar **OPEN** inside coverage | **4 of 105** |
| 🔴 episodes with t0 bar **CLOSE** inside coverage | **5 of 105 = 4.8 %** |

### A1c — THE AGE DISTRIBUTION, AS ASKED

| t0 (UTC, bar open) | dir | 48h move % | \|Δt\| to bar OPEN | \|Δt\| to bar CLOSE |
|---|---|---|---|---|
| 2026-07-13 02:00 | DOWN | 2.47 | 34.9 min | **0.5 min** |
| 2026-07-20 06:00 | DOWN | 0.51 | 0.5 min | **0.5 min** |
| 2026-07-23 12:00 | DOWN | 2.45 | 0.4 min | **0.5 min** |
| 2026-07-26 22:00 | UP | 1.24 | 0.5 min | **0.1 min** |
| 2026-08-02 02:00 | UP | 1.47 | 0.5 min | **0.5 min** |

**Within ±5 min of the t0 bar close: 5 of 5.** Of the bar open: 4 of 5 — the miss is the
07-13 episode, whose breakout bar opened 35 minutes before the collector's first snapshot ever.

🔴 **Freshness is not the constraint. Count is.** This reproduces the 14:25 report exactly,
from a query written independently.

### 🔴 A2 — THE PRE-REGISTERED EXIT FIRES. A3 AND A4 ARE NOT RUN.

**5 < ~10.** The operator named this exit in advance so it could not be rationalised
afterwards, and it is not being rationalised. **No book statistic was computed per outcome;
no p-value was produced in Part A.** The 14:25 report already established that the exit holds
at all nine squeeze definitions (two of which produce a cell of **zero**), that the three
alternative book stores hit **0 of 105** at every tolerance, and that pooling BingX readings
onto the OKX-4000 percentile scale would be the §2.19 cross-source inversion. **None of that
is re-litigated here.** The order book remains **UNMEASURED for want of coverage — mechanism
intact, evidence absent** — and this report adds no support for or against it.

---

## PART B — CANDLE-DERIVED, FULL COVERAGE. n = 105, NO EXIT AVAILABLE.

**Base rates:** FAILED **47 / 105 = 45 %** · mean 48 h move **3.30 %** · median 2.70 %.

### THE WHOLE RESULT IN ONE TABLE

Primary outcome is binary **FAILED**; secondary is the continuous **48 h MOVE %**.

| # | quantity, measured at or before t0 | cells (n) | FAILED Δ | perm-p | MOVE Δ | perm-p |
|---|---|---|---|---|---|---|
| **a** | **VOLUME** at t0 ÷ trailing 20-bar median | 53 / 52 | 2.8 pts | **0.849** | 0.45 % | 0.417 |
| **b** | **BOX SIZE ÷ ATR14** | 53 / 52 | 16.3 pts | 0.120 | 0.46 % | 0.404 |
| **c1** | **SQUEEZE DEPTH** (BBW ÷ p20 threshold) | 53 / 52 | 10.4 pts | 0.331 | 0.47 % | 0.395 |
| **c2** | **SQUEEZE DURATION** (bars) | 53 / 52 | 2.8 pts | **0.847** | 0.14 % | 0.806 |
| **d1** | **DAILY EMA trend**, forming basis | 53 / 52 | 6.6 pts | 0.557 | 1.27 % | 🟡 **0.018** |
| **d2** | **DAILY EMA trend**, closed basis | 59 / 46 | 1.6 pts | **1.000** | 0.87 % | 0.112 |
| **d3** | **4H EMA trend**, closed basis | 46 / 59 | 17.1 pts | 0.119 | 0.71 % | 0.201 |
| **f** | **DIRECTION** — UP vs DOWN breaks | 49 / 56 | 3.6 pts | **0.844** | 0.44 % | 0.431 |
| **PAIR** | (a) × (b), omnibus over 4 cells | 31/22/22/30 | — | 0.373 | — | 0.715 |

**One nominal hit in the entire primary suite, and it is on the SECONDARY outcome.** On the
question actually asked — real versus failed — **the largest gap in the table reaches p = 0.119**.

### a) 🔴 VOLUME — THE CLASSIC DISCRIMINATOR, TESTED HERE FOR THE FIRST TIME, AND IT IS NOTHING

| quartile | volume at t0 | n | FAILED | median move |
|---|---|---|---|---|
| Q1 | 0.40 – 2.06 × | 26 | 46.2 % | 2.37 % |
| Q2 | 2.13 – 3.74 × | 26 | 38.5 % | 2.64 % |
| Q3 | 3.76 – 5.61 × | 26 | **53.8 %** | 1.81 % |
| Q4 | 5.65 – 19.68 × | 27 | 40.7 % | 3.16 % |

**Not monotone, not ordered, not significant.** The textbook claim is that a genuine breakout
arrives on expanding volume. On this instrument, over 105 squeeze breakouts, **the volume of
the breakout bar carries no information about whether the breakout holds.** And across the
nine squeeze definitions its sign **flips** — 5 positive, 4 negative. That is a null, not a
weak effect.

### b) 🔴 BOX SIZE ÷ ATR — THE ONE CONSISTENT SIGN, AND IT IS ARITHMETIC

This is the finding that justifies the section. Across the nine (percentile × min-run)
variants, box/ATR carried **the same sign at 8 of 9** and reached nominal at three:

| pctl | min run | n | narrow / wide FAILED % | Δ pts | perm-p |
|---|---|---|---|---|---|
| 10 | 6 | 101 | 58.8 / 52.0 | +6.8 | 0.553 |
| 10 | 12 | 61 | 51.6 / 56.7 | **−5.1** | 0.796 |
| 10 | 24 | 27 | 57.1 / 46.2 | +11.0 | 0.703 |
| 20 | 6 | 178 | 48.3 / 41.6 | +6.7 | 0.455 |
| **20** | **12** *(canonical)* | **105** | **52.8 / 36.5** | **+16.3** | **0.117** |
| 20 | 24 | 51 | 61.5 / 28.0 | +33.5 | 🟡 0.024 |
| 30 | 6 | 225 | 47.8 / 31.2 | +16.5 | 🟡 0.013 |
| 30 | 12 | 145 | 45.2 / 29.2 | +16.0 | 0.059 |
| 30 | 24 | 82 | 48.8 / 24.4 | +24.4 | 🟡 0.038 |

⚠️ **Those nine samples overlap heavily — they are not nine independent tests**, so "3 nominal
where 0.9 was expected" is not a multiplicity argument in its favour. But the consistency was
real enough to demand a mechanism. **The mechanism is the outcome definition.**

🔴 **`FAILED` = *"price traversed the ENTIRE box the other way"*. The adverse move required to
score a failure IS the box width. Expressed in ATR, that threshold is exactly `box/ATR` — the
very quantity under test.**

| | narrow cell (n=53) | wide cell (n=52) |
|---|---|---|
| median box width | 3.51 ATR | 4.91 ATR |
| 🔴 **adverse move needed to be scored FAILED** | **3.51 ATR** | **4.91 ATR — 1.40× further** |
| **adverse excursion ACTUALLY observed** | **4.47 ATR** (median 3.54) | **4.53 ATR** (median 4.43) |
| Δ | \+0.06 ATR · **perm-p 0.935** | |

**The adverse excursion is flat. Only the yardstick moved.** Re-scoring with a size-invariant
criterion — a fixed adverse threshold in ATR, independent of box width — kills it and **flips
the sign**:

| failure criterion | narrow | wide | Δ pts | perm-p |
|---|---|---|---|---|
| box traverse (the 12:10 definition) | 52.8 % | 36.5 % | +16.3 | 0.119 |
| adverse > **1.0 × ATR** | 77.4 % | 82.7 % | **−5.3** | 0.626 |
| adverse > **1.5 × ATR** | 67.9 % | 71.2 % | **−3.2** | 0.832 |
| adverse > **2.0 × ATR** | 62.3 % | 65.4 % | **−3.1** | 0.842 |
| adverse > **2.5 × ATR** | 60.4 % | 61.5 % | **−1.2** | 1.000 |
| adverse > **3.0 × ATR** | 58.5 % | 57.7 % | +0.8 | 1.000 |

**Five criteria, four sign flips, nothing anywhere near significant.** Per §2.54's ruling — *an
effect whose sign depends on the control is not an effect* — this is dead, and it is dead for a
sharper reason than usual: **it was never a market fact, it was the scoring rule measured
against itself.**

⚠️ **Carry-forward, because it outlives this report:** the 12:10 report's *"45 % of squeeze
breakouts fail"* is a **box-relative** statistic. Under a fixed 1-ATR adverse criterion the
retracement rate on the same 105 episodes is **~80 %**. Both are true; they are answers to
different questions. Any future use of "the failure rate" must say which yardstick it means.

⚠️ Also recorded: **box/ATR is collinear with squeeze duration** (median 3.53 ATR on short runs
vs 4.88 on long). Candidates (b) and (c2) are substantially the same quantity, which is why the
pre-registered pair deliberately did **not** couple them.

### c) SQUEEZE DEPTH AND DURATION — NOTHING

Tighter squeezes fail 39.6 % vs 50.0 % for looser (p = 0.331); longer squeezes 46.2 % vs 43.4 %
(p = 0.847). **A longer or tighter squeeze does not resolve more decisively.** Move size is
equally flat (p = 0.395 / 0.806).

### d) HIGHER-TIMEFRAME DIRECTION — THE ONE NOMINAL HIT, AND IT DOES NOT SURVIVE

`trend` from the bot's own `compute_tf_metrics`, coded ALIGNED / OPPOSED / NEUTRAL against the
breakout direction. **Two bases are reported because one of them is endogenous:**

- **FORMING** — 199 closed bars plus the partial bar built from 1h candles up to the t0 close.
  This is what the live bot sees (§0: EMA reads the forming candle by design). 🔴 **But the
  forming daily/4h bar CONTAINS the breakout bar itself.**
- **CLOSED** — only bars fully closed at or before t0. Cannot contain the break.

They disagree on **19 of 105** episodes on the daily and **22 of 105** on the 4h.

🔴 **The 4h FORMING basis is DEGENERATE and was NOT tested:** ALIGNED 74 / NEUTRAL 31 /
**OPPOSED 0**. A label that never once opposes the break is not predicting it, it is restating
it. Recorded rather than reported as a 100 %-accurate signal, which is what a careless read
would have made of it.

**The nominal hit: daily EMA trend, FORMING basis, vs MOVE size — Δ +1.27 %, perm-p 0.0178.**
Put through §2.54's controls:

| control | result |
|---|---|
| **raw** | ALIGNED n=52 mean 3.95 % vs NOT n=53 mean 2.67 % · **Δ +1.27 %, p = 0.0178** |
| **+ direction** | UP Δ +1.26 % (p 0.085) · DOWN Δ +1.52 % (p 0.066) — sign **holds**, significance gone |
| 🔴 **+ hour (6h blocks)** | +2.74 (p 0.023) · +1.27 (p 0.286) · +2.54 (p 0.010) · 🔴 **−1.08** (p 0.242) — **THE SIGN FLIPS** |
| **+ era (thirds)** | +1.12 (p 0.380) · **+0.03** (p 0.965) · +2.01 (p 0.005) — carried entirely by the last third |
| 🔴 **day** | **UNAVAILABLE.** 102 distinct days hold the 105 episodes; **0 days hold both an ALIGNED and a NOT-ALIGNED episode.** A same-day control has no usable strata at all — §2.54 hit this wall at 16 % coverage, here it is zero |
| 🔴 **endogeneity** | of the 19 forming/closed disagreements, **7 were flipped TO aligned by the forming bar**, and those 7 average a **5.09 %** move vs 3.18 % for everything else (p = 0.070). **A big breakout bar is what MAKES the daily label read aligned** — reverse causation, not prediction |
| 🔴 **the clean (CLOSED) basis** | **Δ +0.87 %, p = 0.112 — NOT NOMINAL** |

**It fails on all four counts that matter:** the sign flips under the hour control, it is
concentrated in one era third, it is mechanically endogenous, and it disappears on the only
basis that cannot contain the breakout. **And it was never about the question anyway** — on
the binary real-vs-failed outcome the daily trend does **nothing** (Δ 6.6 pts p = 0.557
forming; Δ 1.6 pts **p = 1.000** closed).

### e) HOUR OF DAY — THE CONTROL, AS INSTRUCTED

Included because on Mercury-SOL depth turned out to be time-of-day wearing a costume.

| block (UTC) | n | FAILED | median move |
|---|---|---|---|
| 00–05 h | 27 | 44.4 % | 3.02 % |
| 06–11 h | 20 | 50.0 % | 1.78 % |
| 12–17 h | 28 | **32.1 %** | 2.72 % |
| 18–23 h | 30 | **53.3 %** | 2.34 % |

A 21-point spread across blocks on n≈25 cells — **noise of the same size as every "effect"
tested above, which is exactly what a control is for.** Neither of the two candidates that
went furthest is a time-of-day costume: box/ATR's WIDE share runs 46–56 % across the four
blocks, and the daily-trend ALIGNED share runs 39–55 %. **The costume is not the explanation
here; the sign flip and the definition are.**

### f) WHICH WAY — UP AND DOWN BREAKS FAIL AT THE SAME RATE

| | n | FAILED | mean move | median move |
|---|---|---|---|---|
| **UP** breaks | 56 | 46.4 % | 3.10 % | 2.53 % |
| **DOWN** breaks | 49 | 42.9 % | 3.54 % | 2.78 % |
| Δ | | 3.6 pts, **p = 0.844** | 0.44 %, p = 0.431 | |

**No asymmetry.** Worth stating plainly given §2.46 measured a LONG/SHORT asymmetry elsewhere
in the book and applied nothing: **at the squeeze breakout there is not even a nominal one.**

### THE MULTIVARIATE QUESTION, ASKED ONCE

**The pair was named in `PREREG.md` before any Part B number existed: (a) VOLUME × (b) BOX/ATR** —
chosen because they are the two most mechanically *independent* candidates, participation versus
structure. Every other pair is partly collinear ((c) is a relative of (b), (d) of (f)).

| cell | n | FAILED | mean move | median move |
|---|---|---|---|---|
| volLO / boxNARROW | 31 | 51.6 % | 2.82 % | 2.45 % |
| volLO / boxWIDE | 22 | 31.8 % | 3.45 % | 2.74 % |
| volHI / boxNARROW | 22 | 54.5 % | 3.44 % | 2.88 % |
| volHI / boxWIDE | 30 | 40.0 % | 3.60 % | 2.85 % |

**Omnibus permutation over the four cells: FAILED p = 0.373 · MOVE p = 0.715.**

The test is an omnibus on the whole partition, **not** best-corner-versus-rest — that would be
a four-way search wearing one p-value's clothes. **One pair, one test, no combination search,
and no second pair was opened when the first returned nothing.**

---

## §3 — VERDICT

### 🔴 NOTHING SURVIVES. THE QUESTION CLOSES — AND IT CLOSES ON EVIDENCE.

**Can anything see what the flat gate cannot? No.** Not on this data, and this time not for
want of data.

- **Part A: unmeasurable.** 5 of 105 episodes inside book coverage. Pre-registered exit fired.
  The order book is **UNMEASURED, not refuted** — mechanism intact, evidence absent. It becomes
  answerable around **2026-09** at n≈10 and 2026-11 at n≈20, on arrivals alone.
- **Part B: measured in full, on all 105, and negative.** Six candidate families, both outcomes,
  nine squeeze definitions, one pre-registered pair. **Zero cells clear Bonferroni. One reached
  nominal and died under control.** The single most-consistent-looking candidate turned out to
  be the scoring rule measured against itself.

🔴 **This is a §2.45-class closure, and it should be filed there — not next to the 14:25
report.** §2.45 killed ten branches on evidence; §2.45's ruling is *"do not re-run these
branches"*. **Six more join them**, each tested and each failed:

| branch | verdict |
|---|---|
| 11. **breakout-bar VOLUME** | flat, non-monotone across quartiles, sign flips across definitions |
| 12. **BOX SIZE ÷ ATR** | 🔴 **definitional artifact** — flat under any size-invariant criterion |
| 13. **SQUEEZE DEPTH** | flat (p 0.331 / 0.395) |
| 14. **SQUEEZE DURATION** | flat (p 0.847 / 0.806), and collinear with 12 |
| 15. **HTF DIRECTION (1d, 4h)** | nominal on the endogenous basis only; sign flips under the hour control; dead on the clean basis |
| 16. **VOLUME × BOX/ATR** *(pre-registered pair)* | omnibus p 0.373 / 0.715 |

**What that buys is a filter that does not get built.** The 12:10 report established that
**45 % of squeeze breakouts fail** and the flat gate is blind to which is which at t0 (44 % vs
50 %, n=34). The natural next move is to bolt a discriminator onto the gate. **There is nothing
to bolt on.** The gate's value stays exactly where 12:10 put it: **temporal, not predictive.**

### THE CURRENT SQUEEZE, AS OF THIS REPORT

| | value |
|---|---|
| latest closed 1h bar | 2026-08-05 **13:00 UTC** |
| 1h BB width | **0.698 %** (12:10 read 0.755 % at the 10:00 bar) |
| p20 threshold, trailing 90 d | 1.225 % |
| 🔴 **BBW percentile within trailing 90 d** | **3.4** — down from 5.0 three hours ago |
| consecutive squeezed hours ending now | **9** (an episode needs 12) |
| last four BBW readings | 0.755 · 0.765 · 0.720 · **0.698** |

**The squeeze is still deepening.** And the plain consequence of this report: **when it
resolves, nothing in the stack — and nothing that could be built from candles — will tell the
bot in advance whether the break is real.** The coin flip described in the brief is a real
coin flip, and it is now a measured one rather than an assumed one.

### 🔴 NOTHING IS PROPOSED

No filter, no gate, no weight, no advisor threshold, no new sensor, no change to the squeeze
definition. Per the brief: **if something had survived on a usable n, the shape would be shown
and nothing more. Nothing survived.** The pre-registered instruments from §2.47 are untouched
and remain the only things that may move the gate: **n ≥ 100 refusal rows** for the fast
trigger, and **20 executed entries per side** for the review point.

⚠️ **One caution for whoever reads this next.** Nothing here says squeeze breakouts are
unpredictable in general — it says **these six quantities, on this instrument, at n=105, do not
predict them.** The order book is still untested (Part A), and the live-era sample §2.45 and
§2.47 both wait on is still the thing that changes answers in this book.

---

## APPENDIX — WHAT WAS RUN

| file | purpose | cells |
|---|---|---|
| `PREREG.md` | pre-registration: outcomes, six feature definitions, **the pair named in advance** | — |
| `a1_coverage.py` | Part A: book window, uptime, 105 episodes against it, age distribution, the exit | 0 |
| `b1_features.py` | the feature table — all six quantities at or before t0, both HTF bases | — |
| `b2_tests.py` | separation per quantity, n per cell + permutation p, both outcomes | 16 |
| `b3_control.py` | §2.54 de-confounding of the one nominal hit + the endogeneity test | 12 |
| `b4_pair.py` | the pre-registered pair, omnibus, asked once | 2 |
| `b5_sens.py` | the two headline features rebuilt at all nine squeeze definitions | 18 |
| `b6_boxatr.py` | 🔴 the definitional test — adverse excursion in ATR, size-invariant criteria | 11 |

**Total cells spent: 59.** Permutation tests are 20,000 shuffles, two-sided, seed 20260805.

*Read-only. Episodes reused from the 12:10 report, not re-derived; candles from BingX public
REST (the bot's own indicator source), 4h and 1d fetched fresh this session; ATR and trend
labels produced by importing and calling the bot's own `indicators.compute_tf_metrics`;
`trades.db` opened read-only; `titan-bot` unmodified at `b9081ad`. Mercury-SOL never opened.*
