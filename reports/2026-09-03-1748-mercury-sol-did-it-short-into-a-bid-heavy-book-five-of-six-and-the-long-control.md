# mercury-sol-did-it-short-into-a-bid-heavy-book

_2026-09-03 17:48 UTC_

---

# DID MERCURY-SOL SHORT INTO A BID-HEAVY BOOK? Six live shorts, counted — and the control that closes the line

## 🔴 THE ANSWER, AT THE TOP, AS INSTRUCTED

**FIVE of the six. Not six of six.** vpos 32, 34, 35, 37 and 42 entered books leaning against
them; **vpos 36 entered an ASK-heavy book — liquidity leaning WITH the short — and lost −0.757 R
anyway.**

And the control kills the line before the arithmetic even starts: **five of the eight live LONGS
also entered books leaning AGAINST them, and those five returned ΣR +7.092** — they include the
three largest winners in the book. The three longs whose book leaned *with* them returned
+3.638 R and contain the only losing long. **Books leaning against the trade were associated with
the book's best outcomes on one side and its worst on the other. That is direction, not
liquidity.**

**MULTIPLE-COMPARISON DECLARATION.** Family as executed: entry-lean rule 2 thresholds ×
{all, LONG, SHORT} × {live, paper} = 12; exit-lean rule 2 thresholds × {live, paper} = 4;
base-rate binomial 1; long control 1; tape/book agreement 1; regime split 1. **FAMILY = 20,
Bonferroni α = 0.05/20 = 0.0025.**

🔴 **n = 6 SHORTS AND n = 8 LONGS CANNOT RANK. No test is run and none could pass.** Six is a
count and is reported as a count. Everything below is descriptive. Two results are structural
facts about the *base rate* rather than about outcomes, and are marked ⚖️ — those do not depend
on n at all.

**READ-ONLY.** DB `file:…?mode=ro`, SELECT only. `config.py` read as text with line citations,
never imported. Titan touched only by the mandated guard. **No venue call was made.** Controls at
the foot. Titan pre-flight `tools/openitems_guard.py` → **exit 0, clean**.

**Basis:** my own `2026-09-03-1637` §1d (the vpos 42 book, and the unexamined contradiction in
it) and `2026-08-09-1625-sol-book-liquidity-measured-filter-22-refused-facts-on-the-card.md`.

**🔴 One correction to the brief's premise, stated up front because it matters.** The brief says
*"the short side has never been measured separately."* It was — filter-22 §2(b) reports a full
LONG/SHORT split at three horizons. What was never measured separately is the short side **on
taken entries**; filter-22 measured **refusals** (post-skip drift). That distinction is real and
the brief is right to want the entries counted. But the refusal-side result is not neutral
evidence and must be carried into this one: on 260–355 short refusals filter-22 found the effect
**with the wrong sign** — shorts whose book leaned AGAINST them drifted *better*, at every
horizon (4 h −0.013, 12 h −0.095, 24 h −0.673), and its verdict was: *"A liquidity effect that
helps longs and hurts shorts by the same mechanism is not a liquidity effect — it is direction."*

---

# PART 1 — THE SIX LIVE SHORTS, ONE BY ONE

Orientation used throughout, taken from filter-22 so the two reports are comparable:
`imbalance` = Σ(price×size) of bids within −1 % of mid ÷ Σ both sides within ±1 %
(`liquidity_zones.py:210-216`). **> 0.5 = bid-heavy.** `lean_WITH` = `imbalance` for a LONG,
`1 − imbalance` for a SHORT — higher always means the book favours the trade being proposed.

## 1a/1b. The rendered book at each entry

**vpos 32 · SHORT · mid 76.16 · imbalance 0.6569 · lean_WITH 0.3431 · R −0.180**
🔴 **BID-HEAVY — against the short. The most lopsided book of the six, and of all fourteen live entries.**
```
OPPOSING (bid) 4 walls : $76.25 ×17.3 · $75.75 ×13.1 · $75.25 ×5.5 · $74.75 ×5.7
SUPPORTING (ask) 6     : $76.25 ×11.0 · $76.75 ×5.2 · $78.25 ×5.1 · $78.75 ×4.0 · $79.25 ×5.1 · $100.25 ×4.7
```

**vpos 34 · SHORT · mid 75.19 · imbalance 0.5052 · lean_WITH 0.4948 · R −0.643**
BID-heavy — but by **0.0052**, i.e. half a percent off dead neutral.
```
OPPOSING (bid) 4 : $75.25 ×14.2 · $74.75 ×16.7 · $74.25 ×5.6 · $73.25 ×4.4
SUPPORTING (ask) 3 : $75.25 ×16.1 · $75.75 ×7.3 · $100.25 ×4.2
```

**vpos 35 · SHORT · mid 75.15 · imbalance 0.5747 · lean_WITH 0.4253 · R −0.701**
BID-heavy, second-most lopsided of the six.
```
OPPOSING (bid) 4 : $75.25 ×17.7 · $74.75 ×15.4 · $74.25 ×6.8 · $73.25 ×4.4
SUPPORTING (ask) 5 : $75.25 ×15.6 · $75.75 ×5.0 · $76.25 ×6.4 · $79.25 ×4.1 · $100.25 ×4.3
```

**vpos 36 · SHORT · mid 75.19 · imbalance 0.4679 · lean_WITH 0.5321 · R −0.757**
🔴 **ASK-HEAVY — the book leaned WITH this short. It is the counter-example, and it lost anyway.**
```
OPPOSING (bid) 4 : $75.25 ×16.1 · $74.75 ×10.9 · $74.25 ×6.7 · $73.25 ×5.0
SUPPORTING (ask) 5 : $75.25 ×12.9 · $75.75 ×9.6 · $76.25 ×7.2 · $77.25 ×4.4 · $100.25 ×4.2
```

**vpos 37 · SHORT · mid 74.37 · imbalance 0.5461 · lean_WITH 0.4539 · R −1.226** (the worst loss on the side)
```
OPPOSING (bid) 3 : $74.25 ×21.3 · $73.75 ×9.4 · $73.25 ×6.5      <- the thickest single wall in the book, ×21.3
SUPPORTING (ask) 5 : $74.25 ×6.2 · $74.75 ×10.7 · $75.75 ×6.4 · $76.25 ×4.6 · $77.25 ×4.2
```

**vpos 42 · SHORT · mid 99.25 · imbalance 0.5333 · lean_WITH 0.4667 · R −1.083**
```
OPPOSING (bid) 5 : $99.25 ×8.8 (p55) · $98.75 ×5.7 (p31) · $98.25 ×5.5 (p29) · $96.25 ×6.9 (p42) · $95.25 ×4.6 (p15)
SUPPORTING (ask) 6 : $99.25 ×6.5 (p39) · $99.75 ×5.7 (p31) · $106.25 ×6.5 (p39) · $107.25 ×4.7 (p18) · $107.75 ×4.2 (p5) · $120.25 ×6.9
```
*(Percentiles are only rendered into the prompt, not stored per-wall; they are quoted here for
vpos 42 from its stored prompt. For the other five the multiples are stored and the percentiles
are not, so multiples alone are given — a limitation of the record, not of this pass.)*

🔴 **Worth naming, because it changes how the ×8.8 in the 1637 report should be read:** vpos 42's
thickest opposing wall, the one that prompted this question, is **the THINNEST thickest-opposing
wall of the six.** The other five carry opposing walls of ×17.3, ×16.7, ×17.7, ×16.1 and ×21.3.
On the raw multiple, vpos 42 had **the friendliest book of the six shorts** — and it produced the
second-worst loss.

## 1c. 🔴 THE COUNT

```
LIVE SHORTS INTO A BID-HEAVY BOOK :  5 OF 6   (vpos 32, 34, 35, 37, 42)
LIVE SHORTS INTO AN ASK-HEAVY BOOK:  1 OF 6   (vpos 36) -> lost -0.757 R
```

Five of six. And one of those five, vpos 34, is bid-heavy by 0.0052 — a rounding distance from
neutral. On any reading that treats "bid-heavy" as needing to *mean* something, the count is
**four of six**.

## 1d. Tape vs book

| vpos | book | tape `buy_share` / pressure | tape direction | agree? |
|---|---|---|---|---|
| 32 | AGAINST | 0.7038 buy | against the short | agree |
| 34 | AGAINST | 0.9046 buy | against the short | agree |
| 35 | AGAINST | 0.7500 buy | against the short | agree |
| 36 | WITH | 0.1504 sell | with the short | agree |
| 37 | AGAINST | 0.8000 buy | against the short | agree |
| **42** | AGAINST | **0.1781 sell** | **with the short** | 🔴 **CONTRADICT** |

**Five of six agree; vpos 42 is the single contradiction** — the one the 1637 report flagged as
"an unexamined contradiction". It is now measured and it is a sample of one. On the other five
the resting book and the live tape said the same thing, and it made no difference to the outcome:
those five went −0.180, −0.643, −0.701, −0.757, −1.226 R regardless of whether both pointed
against (four cases) or both pointed with (one case).

## 1e. What the book gate saw, and why it admitted

The gate's columns exist only from **vpos 33** onward — `book_gate_*` is NULL on vpos 32, which
predates the gate landing. For the five that carry it:

| vpos | `clause` | `opp_mult` | `opp_pctl` | `opp_dist_pct` | `lean` | `n_supporting` | verdict |
|---|---|---|---|---|---|---|---|
| 34 | `''` | 16.7 | 49.0 | — | 0.4948 | 3 | admitted |
| 35 | `''` | 15.4 | 36.7 | — | 0.4253 | 5 | admitted |
| 36 | `''` | 10.9 | 7.8 | — | 0.5321 | 5 | admitted |
| 37 | `''` | 21.3 | **81.8** | — | 0.4539 | 4 | admitted |
| 42 | `''` | 5.7 | **5.0** | 0.5038 | 0.4667 | 5 | admitted |

`book_gate_clause` is the empty string on all five: **no clause fired on any of them.**
`BOOK_GATE_DRYRUN = False` (config.py:475) — the gate was **armed** every time and **admitted
every time.**

🔴 **Why it admitted, and why that is not a failure of the gate.** The gate judges the **nearest
opposing WALL by percentile**; `book_gate_lean` is *recorded beside it but is not what decides*.
Even on vpos 37, whose opposing wall reached p81.8 — the highest of the six — the gate's own
threshold was not met. The gate is doing exactly what it was built to do. **The quantity the
operator is asking about, `lean`, is stored in that very row and no gate reads it.** That is the
gap, correctly identified. Part 3 asks what closing it would have bought.

---

# PART 2 — THE CONTROL

## 2a. 🔴 The eight live LONGS — and this is where the line closes

| vpos | mid | imbalance | book vs the trade | tape | **R** |
|---|---|---|---|---|---|
| 29 | 74.78 | 0.4847 | 🔴 **AGAINST** (ask-heavy) | n/a | **+1.355** |
| 30 | 76.30 | 0.5008 | with (bid-heavy by 0.0008) | 0.9472 buy | +0.762 |
| 31 | 76.95 | 0.5243 | with | 0.9178 buy | **−1.155** |
| 33 | 76.48 | 0.4815 | 🔴 **AGAINST** | 0.0977 sell | −0.049 |
| 38 | 77.06 | 0.5243 | with | 0.2841 sell | **+4.031** |
| 39 | 87.81 | 0.4851 | 🔴 **AGAINST** | 0.6725 buy | **+1.604** |
| 40 | 92.25 | 0.4841 | 🔴 **AGAINST** | 0.2063 sell | **+2.549** |
| 41 | 101.06 | 0.4870 | 🔴 **AGAINST** | 0.7888 buy | **+1.633** |

```
LONGS into a book leaning AGAINST them : 5 of 8   ΣR +7.092   (4 winners, incl. the top three)
LONGS into a book leaning WITH them    : 3 of 8   ΣR +3.638   (contains the only losing long)
```

🔴 **Longs entered books leaning against them five times out of eight and made +7.092 R doing
it — including vpos 39, 40 and 41, the three largest winners on the live book, all three with
ask-heavy books.** If a book leaning against the trade were the mechanism that sank the shorts,
it should have sunk these. It did the opposite.

**The line closes here.** Lean is not the discriminator. The same quantity that "explains" five
of six short losses simultaneously "explains" four of five long wins, with the opposite sign —
which is the exact shape filter-22 named on 2026-08-09 and refused: *not a liquidity effect, but
direction.*

## 2b. ⚖️ The base rate — and it is the real story

**1,107 rendered books, 2026-08-02 → 2026-09-03**, from every consultation that stored an
`advisor_book_json`:

```
imbalance: p1 0.4150  p5 0.4350  p25 0.4755  p50 0.5069  p75 0.5370  p95 0.5946  p99 0.6425
           mean 0.5099   sd 0.0499   full range 0.3905 - 0.7693
🔴 P(bid-heavy, i.e. > 0.5) = 55.9 %   overall
   on SHORT consultations : 53.1 %   (n = 599)
   on LONG  consultations : 59.3 %   (n = 508)
```

**Two facts that decide most of this report.**

1. 🔴 **The book is a coin flip.** On short consultations it is bid-heavy **53.1 %** of the time.
   "Bid-heavy" is not an event; it is the slightly-more-likely side of a near-fair coin.
2. 🔴 **The distribution is extremely tight.** sd = 0.0499, and the middle half of all books sits
   between 0.4755 and 0.5370. **Every one of the six shorts except vpos 32 (0.6569) sits inside
   the ordinary interquartile range of this instrument's book.** vpos 34 at 0.5052 is the 46th
   percentile of bid-heaviness. There was nothing to see on four of the six.

⚖️ **And the instrument's book is structurally bid-heavy: mean imbalance 0.5099.** Any symmetric
rule on lean will therefore fall harder on shorts than on longs before a single outcome is
consulted. That is Part 3's undoing and it is a property of the tape, not of the sample.

## 2c. 🔴 Expected count beside observed

```
p(bid-heavy | SHORT consultation) = 0.5309   (measured, n = 599)
EXPECTED bid-heavy shorts in 6    = 3.19
OBSERVED                          = 5

P(X = 6) = 0.0224      P(X = 5) = 0.1187      🔴 P(X >= 5) = 0.1411
```

**Five of six happens by chance about one time in seven.** It is not a coincidence worth
remarking on, and six of six — which did not occur — would have happened one time in 45. Against
a base rate of 53 %, **the observed count is unremarkable and is hereby named as such.** Had the
base rate been 90 %, as the brief warns, six of six would have meant nothing at all; at 53 % five
of six still means very little.

---

# PART 3 — WOULD A LEAN RULE HAVE HELPED, AT ENTRY

## 3a. The model, stated before the numbers

> **Refuse the entry when `lean_WITH` falls below X**, where `lean_WITH` = `imbalance` for a LONG
> and `1 − imbalance` for a SHORT. Symmetric by construction.

🔴 **X is taken from the base-rate distribution, not swept.** The `lean_WITH` distribution over
all 1,107 rendered consultations gives **p10 = 0.4473** and **p25 = 0.4730**. Both are reported;
neither was chosen after seeing outcomes. p10 is the primary — "refuse when the book supports you
less than nine books in ten support a trade". p25 is reported because it is the only threshold
that catches vpos 42, and the reader is entitled to see what that costs.

Book data exists from **vpos 27** onward, so the rule can be evaluated on **16 of the 36 closed
positions** (2 paper, 14 live). That is the whole evaluable set and it is stated before the
result, not after.

## 3b. What it refuses

**At p10 = 0.4473 — 3 refusals:**

| vpos | side | book | `lean_WITH` | R |
|---|---|---|---|---|
| 28 | SHORT | paper | 0.4252 | −0.153 |
| 32 | SHORT | LIVE | 0.3431 | −0.180 |
| 35 | SHORT | LIVE | 0.4253 | −0.701 |

**At p25 = 0.4730 — 5 refusals:** the three above plus vpos 37 (SHORT, 0.4539, −1.226) and
**vpos 42 (SHORT, 0.4667, −1.083)**.

**🔴 Winners refused: ZERO, at both thresholds.** Stated immediately, as instructed — and in the
opposite direction to the smart-exit rule, which capped three. Every live winner sits at
`lean_WITH` between 0.4841 and 0.5243; every refusal sits between 0.3431 and 0.4667. On this
sample the two groups do not overlap.

🔴 **AND THE RULE IS STILL DISQUALIFIED, FOR A REASON THAT HAS NOTHING TO DO WITH WINNERS.**

```
p10: refuses 3 of 3 SHORTS, 0 of 8 LONGS
p25: refuses 5 of 5 SHORTS, 0 of 8 LONGS   -> 4 of 6 live shorts (67 %), 0 of 8 live longs (0 %)
```

**Every refusal it has ever made, at either threshold, is a short.** And that is not the sample
talking — ⚖️ it is built into the base rate measured in §2b, before any outcome:

```
share of consultations below p10 = 0.4473 :  LONG 5.9 %   SHORT 13.5 %   -> 2.29x
share of consultations below p25 = 0.4730 :  LONG 20.7 %  SHORT 28.4 %   -> 1.37x
```

Because the instrument's book carries a standing bid tilt (mean 0.5099), **a symmetric lean
threshold taxes shorts 2.3× harder than longs by arithmetic.** A rule that refuses only shorts,
on a side that is 0-for-6, is **a side ban wearing an indicator's name** — the precise
disqualifier this codebase already applied once, to the nominal p85 wall percentile
(config.py: *"a side ban is not a rule"*).

## 3c. ΣR and Σ$, per side, per era, never pooled

**Threshold p10 = 0.4473 (primary):**

```
LIVE  n=14  refused 2 (14 %)   ΣR  +6.141 -> +7.022   Δ +0.881 R
   LONG  n=8  refused 0        ΣR +10.730 -> +10.730   Δ  0.000
   SHORT n=6  refused 2        ΣR  −4.589 ->  −3.709   Δ +0.881 R
PAPER n=2   refused 1 (50 %)   ΣR  −0.813 ->  −0.660   Δ +0.153 R
```

**Threshold p25 = 0.4730:**

```
LIVE  n=14  refused 4 (29 %)   ΣR  +6.141 -> +9.331   Δ +3.190 R
   LONG  n=8  refused 0        ΣR +10.730 -> +10.730   Δ  0.000
   SHORT n=6  refused 4        ΣR  −4.589 ->  −1.400   Δ +3.190 R
PAPER n=2   refused 1 (50 %)   ΣR  −0.813 ->  −0.660   Δ +0.153 R
```

In dollars on the live book, p10 saves **+$0.89** (vpos 32 −$0.27 and vpos 35 −$0.73 not taken)
and p25 saves **+$4.79** on a book that has made $15.56.

**Sign stability, leave-one-out, live cell at p10 (n = 2 refusals):** +0.881 R → +0.701 R
dropping vpos 32, → +0.180 R dropping vpos 35. Sign holds, but **the entire result rests on two
positions and 79 % of it on one of them.** At n = 2 this is not a robustness check; it is a
statement of how little there is.

**Independent sample:** the paper cell has **n = 2** — one refusal. There is no out-of-sample
test available at all. This is the control that was decisive against the smart-exit rule and
**here it simply does not exist**, which is a weaker position, not a stronger one.

## 3d. Refusal rate

```
p10:  3 of 16 evaluable entries = 19 %   — on the SHORT side alone: 3 of 8 = 38 %
p25:  5 of 16                   = 31 %   — on the SHORT side alone: 5 of 8 = 63 %
```

🔴 **p25 breaches the 30 % line the brief sets, and it is worse than the headline number
suggests: 63 % of shorts refused, 0 % of longs.** By the brief's own criterion it must be named
as a side ban, and it is. **p10 sits at 19 % overall but still 38 % on the short side, and it
still refuses zero longs.** Neither threshold produces a rule; both produce a short-side filter
with an order-book label on it.

For the pre-registered comparison: the flat/ADX gate declared a pre-registered refusal rate of
33.2 % *symmetric by side* (config.py:392-397) and named asymmetry as grounds for removal. A lean
rule at p10 is **100 % asymmetric** from its first refusal.

---

# PART 4 — THE SAME QUESTION ON THE EXIT SIDE

## 4a. 🔴 The asymmetry, before any number

**At entry, a refusal is free.** There is no position, no fill, no fee. The worst case is a
foregone trade, and the record of foregone trades is already tracked (`skip_attribution`).

**At exit, a close costs 0.20 % round-trip on Mercury-SOL** — the real 0.100 % taker on both
legs — **and it forecloses a position that may still run.** An exit rule must therefore be right
by more than 0.20 % of notional *just to break even against doing nothing*, and it must be right
about the future, not merely about the present state of the book.

On this book 0.20 % of notional is ≈ **0.07–0.09 R** per close. That is the toll on every firing,
correct or not.

## 4b. Is lean sampled during a position's life?

🔴 **YES.** `smart_exit_dryrun_samples.ob_imbalance` is populated on **440 of 440 rows** across
28 positions, 2026-07-08 → 2026-09-03, from the same OKX-direct source as the entry book
(config.py:892-896). Coverage on all fourteen live positions: 4, 26, 8, 5, 15, 1, 2, 19, 4, 17,
10, 8, 15 and 40 samples respectively.

**So the rule is buildable from existing data and no new sampling is needed.** The cadence is
hourly (`SMART_EXIT_DRYRUN_SAMPLE_SEC = 3600`, config.py:926) — the same latency caveat as the
smart-exit record: the price the rule would trade on is up to 59 minutes stale.

## 4c. The replay — close when the book turns against you

Same thresholds, same orientation, close at the first hourly sample where `lean_WITH < X`, at
that sample's price, with the real round-trip charged:

**Threshold p10 = 0.4473 — fires on 7 of 16:**

| vpos | book | side | fires at | price | net R | actual R | Δ |
|---|---|---|---|---|---|---|---|
| 27 | paper | SHORT | 2.0 h | 72.18 | +0.288 | −0.660 | +0.947 |
| 28 | paper | SHORT | **0.0 h** | 72.80 | −0.112 | −0.153 | +0.041 |
| 30 | LIVE | LONG | 18.0 h | 76.89 | +0.341 | +0.762 | **−0.421** |
| 32 | LIVE | SHORT | **0.0 h** | 76.21 | −0.157 | −0.180 | +0.023 |
| 35 | LIVE | SHORT | **0.0 h** | 75.16 | −0.188 | −0.701 | +0.513 |
| 41 | LIVE | LONG | 13.0 h | 108.76 | +2.259 | +1.633 | +0.626 |
| 42 | LIVE | SHORT | 10.0 h | 100.03 | −0.379 | −1.083 | +0.704 |
```
ALL 16: ΣR +5.328 -> +7.761  (Δ +2.433)      net-positive closes: 3 of 7
```

**Threshold p25 = 0.4730 — fires on 11 of 16:**

| vpos | book | side | fires at | net R | actual R | Δ |
|---|---|---|---|---|---|---|
| 27 | paper | SHORT | 0.0 h | −0.085 | −0.660 | +0.575 |
| 28 | paper | SHORT | 0.0 h | −0.112 | −0.153 | +0.041 |
| 30 | LIVE | LONG | 18.0 h | +0.341 | +0.762 | −0.421 |
| 32 | LIVE | SHORT | 0.0 h | −0.157 | −0.180 | +0.023 |
| 33 | LIVE | LONG | 1.0 h | −0.325 | −0.049 | −0.276 |
| 35 | LIVE | SHORT | 0.0 h | −0.188 | −0.701 | +0.513 |
| 37 | LIVE | SHORT | 0.0 h | −0.212 | −1.226 | +1.014 |
| **38** | LIVE | LONG | 15.0 h | **+1.251** | **+4.031** | 🔴 **−2.780** |
| **40** | LIVE | LONG | 1.0 h | **+0.490** | **+2.549** | 🔴 **−2.059** |
| 41 | LIVE | LONG | 9.0 h | +1.004 | +1.633 | −0.629 |
| 42 | LIVE | SHORT | 0.0 h | −0.077 | −1.083 | +1.006 |
```
ALL 16: ΣR +5.328 -> +2.336  (Δ −2.992)      net-positive closes: 4 of 11
```

🔴 **THE SIGN FLIPS BETWEEN TWO ADJACENT, EQUALLY PRINCIPLED DECILES OF THE SAME BASE-RATE
DISTRIBUTION: +2.433 R at p10, −2.992 R at p25.** It flips for the reason the smart-exit rule
failed — at p25 it starts catching the long winners, taking vpos 38 from +4.031 R to +1.251 R and
vpos 40 from +2.549 R to +0.490 R. A result that reverses between p10 and p25 of its own
threshold distribution is not a finding; it is a threshold sitting on top of four positions.

🔴 **And a structural observation that undercuts the whole exit framing.** At p10, **3 of the 7
firings occur at elapsed 0.0 h** — the first hourly sample, i.e. essentially at entry. At p25,
**6 of 11 fire within one hour.** For those, the "exit rule" is the **entry rule arriving an hour
late and paying 0.20 % for the delay.** vpos 42 at p25 fires at 0.0 h and closes at 99.24 — the
entry price — booking −0.077 R purely in fees, where the entry rule at the same threshold would
have refused it for nothing.

## 4d. 🔴 Against the 0.20 % toll

From the 2026-09-03 17:12 pass: SOL's breakeven lock pays **exactly 0.00 R** at the real 0.100 %
taker, and the trail pays **`peak − 0.83 R`**. Any new exit mechanism must clear that same toll.

```
p10:  3 of 7 closes net-positive after fees   =  43 %   -> 4 of 7 (57 %) close at a LOSS
p25:  4 of 11 closes net-positive after fees  =  36 %   -> 7 of 11 (64 %) close at a LOSS
```

**On the live cell alone** the picture is worse than the pooled figures: at p10 the live firings
are vpos 30 (+0.341 R), 32 (−0.157), 35 (−0.188), 41 (+2.259), 42 (−0.379) — **2 of 5 positive.**

## 4e. 🔴 The plain answer

**An exit lean rule would close the majority of its positions at a loss after fees — 57 % at p10,
64 % at p25 — and its total flips sign between two adjacent principled thresholds. On the
evidence available, the answer to the operator's question is NO.**

It is a real answer and it rests on three things that do not depend on n: **(1)** more than half
its closes are net-negative after a toll that is charged whether the rule is right or wrong;
**(2)** at both thresholds a large share of its firings land in the first hour, where it is
duplicating the entry decision at a cost the entry decision does not pay; **(3)** the one thing
an exit rule must do that an entry rule need not — be right about the *future* — is exactly where
it is worst, because the two firings that cost the most (vpos 38, vpos 40 at p25) closed
positions that went on to make +4.031 R and +2.549 R.

**The asymmetry in §4a is the whole finding.** The same quantity, applied at entry, costs nothing
when wrong. Applied at exit it costs 0.20 % every time and forecloses the runs. **If lean is ever
to be used, the entry side is the only side where being wrong is free — and §3 shows the entry
side is a side ban.**

---

# CONTROLS

| control | evidence |
|---|---|
| Titan pre-flight | `openitems_guard.py --quiet` → **exit 0**, clean |
| **DB read-only** | `sqlite3.connect('file:…/trades.db?mode=ro', uri=True)`; SELECT only; **zero** writes |
| **cwd outside SOL's tree** | scratchpad, `/root`, `/root/titan-bot`, `kola-reports`; never inside `/mnt/…/mercury-sol` |
| **config not imported** | `config.py`, `liquidity_zones.py` line references read as **text**; the only config import was Titan's own guard reading Titan's config |
| **no writes / no orders** | nothing opened for writing; **no venue call at all this pass** |
| **service untouched** | `systemctl show` only. SOL PID **1196924**; Titan PID **2610002** |
| **NRestarts unchanged** | SOL **0 → 0**; Titan **0 → 0** |
| **file hashes identical** | all **33** SOL `*.py` md5-identical before and after |
| Bonferroni | family **20**, α = **0.0025** — **no test run**; n = 6 shorts / 8 longs cannot rank, stated throughout |
| sign stability | entry rule p10 live cell: +0.881 → +0.701 / +0.180 under leave-one-out — sign holds on **n = 2 refusals**, reported as weakness not strength. Exit rule: **sign flips** p10 → p25 |
| regime split | the six shorts: 6/6 entered `market_regime = TREND`; there is no FLAT short in the live book, so no regime contrast exists on the side in question |
| paper vs live as independent sample | **unavailable** — book data begins at vpos 27, leaving a paper cell of **n = 2**. The control that decided the smart-exit question cannot be run here. |

**Nothing is proposed. Nothing is applied. No flag changed, no file edited.**

---

**Bottom line.** **Five of six, not six of six** — and vpos 36 shorted into an ask-heavy book and
lost anyway. The count is unremarkable against a base rate of 53.1 % (expected 3.19, P(X≥5) =
0.14), and four of the six sat inside the ordinary interquartile range of an instrument whose
book barely moves (sd 0.0499). **The control closes the line: five of eight live longs entered
books leaning AGAINST them and made +7.092 R, the three biggest winners among them.** A lean rule
at entry refuses zero winners on this sample — but refuses **only shorts, at both thresholds, 4
of 6 live shorts and 0 of 8 live longs** — and ⚖️ the base rate shows that asymmetry is
arithmetic, not sample: the instrument's book is structurally bid-heavy, so a symmetric threshold
taxes shorts 2.29× harder before any outcome is seen. **That is a side ban wearing an indicator's
name.** On the exit side the data exists (440/440 samples carry `ob_imbalance`), the rule is
buildable, and it should not be: **57–64 % of its closes are net-negative after the 0.20 % toll,
its sign flips between two adjacent deciles of its own threshold distribution, and a large share
of its firings are the entry decision arriving an hour late at full price.** The operator's
question, on the exit side, answers **no**.
