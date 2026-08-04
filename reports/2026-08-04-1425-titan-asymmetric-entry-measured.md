# ASYMMETRIC ENTRY — MEASURED IN FULL. THE PRE-REGISTERED ANSWER IS: APPLY NOTHING.

**2026-08-04 14:25 UTC · Titan HEAD `44731be`, LIVE, real money, flat (0 open positions)**
**NO CODE WAS CHANGED. The running binary is the same one as at 14:00.**

Brief: measure the LONG/SHORT asymmetry and apply the rule the operator pre-registered *before* the
numbers arrived. Branch 4 of that pre-registration fired: *"If neither survives its own n → apply
nothing, say so, and I will take the EMA envelope decision instead."*

**That is a decision, not a deferral, and it is the operator's own — I am not entitled to override a
pre-registration because the alternative would look more like work.**

Companions: `reports/2026-08-04-1300-titan-forensics-what-used-to-gate.md` ·
canonical OPEN-ITEMS updated in the same commit (**§2.46** new, **§2.45c** corrects §2.45a) ·
dated snapshot `reports/2026-08-04-1425-open-items.md`.

---

## 🔴 THE FIVE FINDINGS THAT DECIDE IT

1. **No LONG bar level works.** Kept-book sumR across 3.0 → 5.5: **−6.00 · −4.04 · −2.51 · −2.03 ·
   −1.44 · −0.77.** It approaches zero from below and never crosses. At 5.5 it leaves **3 longs**
   and they still lose. **Score ≥5.0 vs <5.0 on the long book: p = 0.487.**
2. **The three highest-scoring longs in the entire book lose money** (scores 7.50, 7.75, 8.50 →
   −0.48, −0.41, +0.12R). Every score quartile of the long book is negative.
3. **The headline fact does not clear its own significance bar.** SHORT−LONG Δmean **+0.446,
   p = 0.062** on all 59 — and **p = 0.189 on the §0-clean 40**, the cohort §0 requires for entry
   statistics. The largest fact in the book **was never tested before being called established.**
4. **Location is collinear with side, so it cannot subsume it.** 24 of 26 longs entered in the
   *upper* half of the prior 24h range; 32 of 33 shorts in the *lower* half. There is no band with
   both sides in it. The proposed rule refuses **3 of 59** trades and its LONG half has the **wrong
   sign**.
5. **The book contains exactly ONE bull episode** (07-10 → 07-28, 19 days of 73). A permanent LONG
   rule fitted here is fitted to a single bear regime.

---

## 0. VALIDATION FIRST — the replay reproduces the book before it predicts anything

§0's standing methodology: *a replay that cannot reproduce the past has no standing to predict the
future.* Two checks, both passed before any counterfactual was computed:

| check | result |
|---|---|
| Reproduce the operator's headline from `virtual_positions` | **LONG n=26 win 30.8 % sumR −7.95R · SHORT n=33 win 48.5 % sumR +4.64R** — exact |
| Every entry cleared the score bar in force at its own timestamp (2.0 before `dee6cee`, 3.0 after; 5.0 FLAT floor after `db71454`) | **59 of 59** |

**Cohorts used throughout:** all-with-computable-R **59** · §0-clean (wall-trail lifetime overlap +
recheck TIGHTEN removed) **40** · live era (`stop_order_id IS NOT NULL`) **7**.
**Price data: real BingX `BTC/USDT:USDT` candles** — 1d/4h/1h, the same venue that executed the
trades. **Only CLOSED candles are used at each entry timestamp** (no forming-candle leakage, §0).

---

## 1. IS IT REGIME OR IS IT STRATEGY?

### 1a. The LONG book split by BTC's own trend at entry

Regime from closed BingX candles, EMA9 vs EMA21 with a slope condition:
`bull` = EMA9 > EMA21 and EMA21 rising · `bear` = mirror · `flat` = everything else.

**DAILY**

| cell | n | win | sumR | meanR |
|---|---|---|---|---|
| LONG · daily bull | 8 | 37.5 % | **−2.19** | −0.274 |
| LONG · daily flat | 5 | 0.0 % | −1.50 | −0.300 |
| LONG · daily bear | 13 | 38.5 % | −4.25 | −0.327 |
| SHORT · daily bull | 6 | 33.3 % | −2.75 | −0.458 |
| SHORT · daily flat | 6 | 16.7 % | −0.83 | −0.139 |
| **SHORT · daily bear** | **21** | **61.9 %** | **+8.23** | **+0.392** |

**4-HOUR** — LONG · 4h bull **−5.78R** (n=14, win 14.3 %) · 4h flat −2.82 (n=7) · **4h bear +0.65
(n=5, win 80 %)**. SHORT · 4h bear +6.58 (n=22) · 4h bull +0.88 (n=8) · 4h flat −2.82 (n=3).

**§0-clean LONG:** bull −0.73 (n=6, win 50 %, mean −0.121) · flat −0.44 (n=1) · bear −2.61 (n=8,
mean −0.326).

**ANSWER: longs lose in ALL regimes, including a genuine daily uptrend.** The bull cell is the
least-bad on the clean cohort (−0.121 vs −0.326) but it is still negative, on n=6.

**Robustness — a second, independent regime definition** (price vs SMA20 vs SMA50, closed dailies):
LONG bull **n=1** (+1.04R) · flat n=19 (−7.39R) · bear n=6 (−1.59R). The conclusion does not change,
but **this definition puts almost the whole book in "flat"**, which is itself the answer to 1b.

### 1b. How many of the book's days were genuinely bull? 🔴 ONE EPISODE.

| daily regime | days | share |
|---|---|---|
| bear | 46 | 63.0 % |
| **bull** | **19** | **26.0 %** |
| flat | 8 | 11.0 % |

**Runs:** bear 05-23 → 07-03 · flat 07-04 → 07-09 · **bull 07-10 → 07-28** · flat 07-29 → 07-30 ·
bear 07-31 → 08-03. **The longest bull run is 19 days and it is the ONLY bull run.**

🔴 **Therefore the long side has been tested in exactly one uptrend, and every "longs lose in bull
too" statement rests on the 8 entries that fell inside it.** A permanent, regime-independent LONG
rule cannot be honestly written from this book — the pre-registration's first branch requires
"regime-independent" as a *recorded claim*, and the data does not support making it.

### 1c. The live era

| vpos | side | opened | R | daily | 4h | loc in 24h range |
|---|---|---|---|---|---|---|
| 86 | SHORT | 07-30 00:50 | −1.02 | flat | bear | 0.310 |
| **87** | **LONG** | 07-30 12:05 | **−0.44** | flat | flat | 0.988 |
| 88 | SHORT | 07-31 09:35 | −0.30 | flat | bull | −0.085 |
| 89 | SHORT | 07-31 12:20 | **+1.39** | flat | bear | 0.067 |
| 90 | SHORT | 07-31 14:25 | −0.30 | flat | bear | −0.274 |
| 91 | SHORT | 08-03 06:40 | −0.48 | bear | bear | −0.064 |
| **92** | **LONG** | 08-03 20:25 | **−0.73** | bear | flat | 0.925 |

**2 of the 7 live entries are LONG. Both lost, −1.17R combined.** Live SHORT: 5 entries, −0.72R.
**Five of the seven were taken in a daily-FLAT tape** — the live era is not the book's bear regime.

---

## 2. THE LONG BAR CURVE — SHORT held at 3.0 throughout

Replay quantity = **the quantity the gate actually compares**: `gated = raw matrix score + macro
penalty`. (Per §0's correction, `confluence_score` on an `executed` row holds the RAW score, and
`macro_gate_penalty` is stored beside it.)

Book span **72.3 days** · LONG n=26 · SHORT n=33.

| LONG bar | longs kept | longs refused | sumR kept | sumR refused | win kept | meanR kept | longs/day |
|---|---|---|---|---|---|---|---|
| 3.0 (today) | 22 | 4 | **−6.00** | −1.95 | 31.8 % | −0.273 | 0.304 |
| 3.5 | 18 | 8 | **−4.04** | −3.91 | 33.3 % | −0.225 | 0.249 |
| 4.0 | 14 | 12 | **−2.51** | −5.44 | 35.7 % | −0.179 | 0.194 |
| 4.5 | 10 | 16 | **−2.03** | −5.92 | 30.0 % | −0.203 | 0.138 |
| 5.0 | 8 | 18 | **−1.44** | −6.51 | 37.5 % | −0.180 | 0.111 |
| 5.5 | 3 | 23 | **−0.77** | −7.18 | 33.3 % | −0.256 | 0.041 |

**§0-clean LONG cohort:** 3.0 → kept n=12 −2.02R · 4.0 → n=8 −0.47R · **4.5 → n=5 +0.03R** · 5.0 →
n=5 +0.03R · 5.5 → n=1 +0.12R.

### 🔴 THE ANSWER THE BRIEF ASKED FOR, PLAINLY

> *"State the level at which the long book stops losing, and how many longs survive there. If it
> takes 5.5 and leaves n=3, say that plainly — a bar that leaves nothing is not a fix."*

**There is no such level.** The kept book improves monotonically and **never reaches zero**: at 5.5
it is still **−0.77R on n=3**. On the §0-clean cohort it crosses to **+0.03R at 4.5 — on n=5**, which
is below the operator's own floor of 8 and is indistinguishable from zero.

**And the reason is not that the bar is too low — it is that the score does not rank the long book:**

| LONG score quartile | range | n | win | sumR | meanR |
|---|---|---|---|---|---|
| Q1 | 2.25–3.25 | 6 | 16.7 % | −3.32 | −0.554 |
| Q2 | 3.25–4.00 | 7 | 42.9 % | −2.09 | −0.299 |
| Q3 | 4.00–5.00 | 6 | 33.3 % | −1.05 | −0.176 |
| Q4 | 5.00–8.50 | 7 | 28.6 % | −1.48 | −0.211 |

**All four quartiles lose. The top quartile is not the best one.** The three highest-scored longs in
the book — vpos73 (7.50) −0.48R, vpos65 (7.75) −0.41R, vpos84 (8.50) +0.12R — sum to **−0.77R**.
Permutation test, LONG score ≥5.0 vs <5.0: **Δ+0.181, p = 0.487.** The score carries no information
about which long trade wins.

---

## 3. ENTRY LOCATION IN THE PRIOR 24h RANGE

**Definition (stated so it can be checked):** the 24 **closed** 1h BingX candles before the entry
timestamp; `loc = (fill − low) / (high − low)`; **0 = at the low, 1 = at the high; values outside
[0,1] mean the entry broke out of that range entirely.** Computable on **59 of 59** rows.

### 3a. Quartiles per side — and the shape nobody had looked at

**ALL 59**

| cell | range | n | win | sumR | meanR |
|---|---|---|---|---|---|
| LONG Q1 | 0.16–0.67 | 6 | 50.0 % | −2.97 | **−0.495** |
| LONG Q2 | 0.78–0.93 | 7 | 14.3 % | −2.50 | −0.357 |
| LONG Q3 | 0.93–1.01 | 6 | 33.3 % | −1.69 | −0.281 |
| LONG Q4 | 1.04–1.34 | 7 | 28.6 % | −0.79 | **−0.113** |
| SHORT Q1 | −0.27–0.03 | 8 | 37.5 % | −1.74 | −0.217 |
| SHORT Q2 | 0.03–0.10 | 8 | 50.0 % | +1.59 | +0.199 |
| SHORT Q3 | 0.10–0.16 | 8 | 62.5 % | **+6.48** | **+0.810** |
| SHORT Q4 | 0.17–0.85 | 9 | 44.4 % | −1.70 | −0.189 |

**Is it monotone?** **LONG: yes on the full book** (−0.495 → −0.357 → −0.281 → −0.113, higher in the
range is less bad) **but every quartile still loses**, and on the §0-clean cohort it is **not**
monotone (−0.308 / −0.385 / −0.304 / −0.024). **SHORT: not monotone on either cohort** — the money
is in Q3 (+0.810), with Q1 and Q4 both negative. **An inverted-U is not a threshold rule.**

### 3b. Does location subsume the side split? 🔴 NO — THEY ARE COLLINEAR, NOT INDEPENDENT

| band | LONG | SHORT |
|---|---|---|
| [0.00, 0.25) | **n=2** (+0.21R) | n=23 (+6.21R) |
| [0.25, 0.50) | **n=0** | n=3 (−0.40R) |
| [0.50, 0.75) | n=4 (−3.18R) | **n=0** |
| [0.75, 1.01) | n=13 (−4.18R) | **n=1** |

**24 of 26 longs sit in the upper half; 32 of 33 shorts sit in the lower half. 9 longs entered ABOVE
the prior 24h high and 6 shorts BELOW the prior 24h low.** This bot enters at the breakout edge on
essentially every trade — *by construction*, not by accident.

**Consequence: the question "is it location or is it side?" is unanswerable on this book**, because
there is no cell with a usable n on both sides. **Location cannot subsume the side split, and the
side split cannot be re-described as location.** Any rule written on one is silently a rule on the
other.

### 3c. What the brief's rule would have cost and saved

> *"refuse LONG below the 40th percentile of the 24h range, refuse SHORT above the 60th"*

| | n | win | sumR |
|---|---|---|---|
| LONG refused (loc < 0.40) | **2** | 100 % | **+0.21** ← it removes a **winning** cell |
| LONG kept | 24 | 25.0 % | −8.15 |
| SHORT refused (loc > 0.60) | **1** | 0 % | −0.51 |
| SHORT kept | 32 | 50.0 % | +5.16 |

**It refuses 3 of 59 trades in 72 days, and the LONG half has the wrong sign.** It is not a rule;
it is a rounding error with a card attached.

### 3d. 🔴 THE QUOTED LOCATION NUMBERS COULD NOT BE REPRODUCED

The brief's "known" figures — SHORT near low **+0.702R** (n=12) vs near high −0.302R (n=13); LONG
near high +0.161R (n=7) vs near low −0.596R (n=7) — do **not** reproduce here:

| definition | clean SHORT lower half | clean SHORT upper half | clean LONG lower | clean LONG upper |
|---|---|---|---|---|
| prior 24 **closed** 1h candles | n=12 **−0.036** | n=12 **+0.247** | n=7 −0.352 | n=7 −0.172 |
| 24 candles **including** the entry bar | n=12 +0.053 | n=12 +0.158 | n=7 −0.353 | n=7 −0.259 |

**The n's match the §0-clean cohort exactly (12/13 and 7/7), so the cohort was right — but the R's do
not match, and the SHORT half INVERTS: shorts did better in the upper half, not the lower.** The
original measure's window and price source were never recorded, so the difference cannot be located.
**"Both sides favour continuation" survives only for LONG, in sign, not in magnitude.** Recorded in
canon as another number that travelled without its predicate.

---

## 4. THE DECISION — which pre-registered branch fired, and why

| branch | condition | verdict |
|---|---|---|
| 1 · permanent LONG bar | §1 shows longs lose in all regimes **AND** §2 identifies a level leaving ≥8 longs | **FAILS.** §1's antecedent holds, but **§2 identifies no level at all** — the long book never stops losing (−0.77R at 5.5, n=3). The action term is undefined |
| 2 · conditional LONG bar | longs lose **only** when the daily is not bull | **FAILS.** Longs lose in bull too (−2.19R, n=8). And conditioning is unwritable anyway: **one bull episode, 19 days** |
| 3 · location rule instead | §3b shows location subsumes the side split | **FAILS.** Collinear — 24/26 vs 32/33. Refuses 3 of 59, LONG half wrong-signed |
| **4 · apply nothing** | **neither survives its own n** | 🔴 **FIRED** |

**Applied: nothing. No constant, no status, no card, no restart. `git status` on `/root/titan-bot`
is clean at HEAD `44731be`, the same binary that has been running since 13:29.**

### Why I did not apply "the best available" anyway

A 5.0 LONG bar is the tempting compromise: it leaves n=8 and the smallest loss. **It fails on its
own live-era evidence** — of the 7 live entries it refuses **1** (vpos87, −0.44R) and **keeps
vpos92 at score 5.25** (−0.73R), so it does not touch the live long problem it was designed for. And
it would cost **59.3 % of all LONG signals** (191 of 322 in the last 30 days) to buy a book that
still loses **−1.44R**. That is a large permanent behavioural change bought with a statistic of
p = 0.49.

### The pre-registration numbers, recorded even though nothing shipped

- **Refusal rate per side, last 30 days** (730 signals passed the score gate): a LONG-specific 5.0
  bar refuses **191 of 322 LONG (59.3 %)**; the same bar applied to SHORT would refuse 100 of 383
  (26.1 %).
- **Entries per day after:** the long side falls to **0.111/day** (from 0.304 over the book).
  Current actual rate: **27 entries in 30 days = 0.90/day** (LONG 14 · SHORT 13).
- **Of the last 25 entries it would have refused 9** — vpos69 (−0.28), 70 (−0.31), 71 (−0.20),
  72 (−0.99), 78 (−1.20), **79 (+0.50)**, **82 (+1.04)**, 85 (−1.09), 87 (−0.44). Removes −2.96R of
  losses **and +1.54R of winners**; the kept book is still **−4.69R**.
- **Review point:** 20 executed entries **per side**, not calendar time.

---

## 5. WHAT THE BOOK ACTUALLY SEPARATES ON — recorded as a HYPOTHESIS, not applied

**`SHORT` in a daily-bear tape: +8.23R, n=21, win 61.9 %, Δ+0.695 vs everything else, perm-p = 0.0040.**
Every other cell of the 2×3 grid loses. Alignment-with-daily as a single predicate: **+0.519,
p = 0.029** (n=29 vs 30) — but it is carried entirely by the short-in-bear cell (LONG-in-bull is
−2.19R).

🔴 **NOT APPLIED, for three reasons that are each sufficient:**
1. **It is the best of a 6-cell grid** — the exact "best of N" construction that produced §4's items
   3, 9 and 10 in this book. p = 0.0040 sits *at* the Bonferroni line, not clear of it.
2. **It largely restates the tape:** 63 % of the book's days were daily-bear. "This bot made money
   shorting a falling market" is a description of the sample, not a discovered edge.
3. 🔴 **On the live era it refuses 6 of 7 entries — including the only winner** (vpos89, +1.39R, taken
   in a daily-**flat** tape). Five of the seven live entries were daily-flat; the rule has nothing to
   say about the regime the bot is actually trading now.

---

## 6. TWO CORRECTIONS TO THE RECORD

### 6a. 🔴 The headline asymmetry does not clear the significance bar

| cohort | Δmean (SHORT − LONG) | perm-p (20 k) |
|---|---|---|
| all 59 | +0.446 | **0.062** |
| **§0-clean 40** | +0.432 | **0.189** |

The fact was measured twice a month apart, and both measurements were of the **same untested
difference**. On the cohort §0 mandates for entry statistics it is **p = 0.19** — nowhere near the
Bonferroni-corrected bar this book applies to every other candidate. **12.6R of separation across 59
trades is inside what this book's variance produces by chance.**

### 6b. 🔴 §2.45a's "zero discriminating power on the live era" applies to the 1h leg only

Confirmed: all **7 of 7** live entries are 1h `Expanding`. **But the strongest form — 1h AND 15m both
Expanding, the one carrying p = 0.029 — admits only 4 of 7:**

| vpos | side | R | 1h | 15m | strong form |
|---|---|---|---|---|---|
| 86 | SHORT | −1.02 | Expanding | Contracting | **REFUSE** |
| 87 | LONG | −0.44 | Expanding | Expanding | admit |
| 88 | SHORT | −0.30 | Expanding | Expanding | admit |
| 89 | SHORT | **+1.39** | Expanding | Expanding | admit |
| 90 | SHORT | −0.30 | Expanding | Expanding | admit |
| 91 | SHORT | −0.48 | Expanding | Flat | **REFUSE** |
| 92 | LONG | −0.73 | Expanding | Contracting | **REFUSE** |

**Refused −2.23R, kept +0.35R, and it keeps the only winner.** Per side on all 59: PASS·SHORT
**+9.45R (n=12, win 75 %)** vs FAIL·SHORT −4.81R (n=21); PASS·LONG −1.91R (n=12) vs FAIL·LONG
−6.04R (n=14) — **it separates the short side; it does not rescue the long side.**

**This changes the sentence, not the ruling.** Three live refusals is not a sample, and §2.45a's
classification (hypothesis with a positive prior, promotable only by live-era data) stands. But the
operator taking that decision should have the corrected version in front of them.

---

## 7. FREEZE / SCOPE STATEMENT

**Entry side only was in scope, and nothing in scope was touched.** No change to the HTF cascade, the
FLAT floor, Variant-B, the risk gates, either advisor prompt, or anything on the exit side (§2.4
still frozen at 5 of 10). **No snapshot, no `py_compile`, no restart — because there is no diff.**
`git status` clean, HEAD `44731be`, `titan.service` running since 13:29:03 UTC, `virtual_positions`
holds **0 open rows**.

All measurement ran **read-only against `trades.db`** and against candles fetched from BingX into a
scratch directory. **No table was written.**

## 8. WHAT IS NOT CLOSED — and how the review is run without touching the bot

- **The long side is not fixed. It is unfixable *on this data*, which is a different claim.** 26
  longs, one bull episode, no ranking power in the score.
- **What would change it:** live-era entries. At **0.90 entries/day**, 20 live entries per side is
  roughly **six weeks** — the same order as §2.45's standing requirement.
- **The review needs no code in the hot path.** The whole measurement is an offline replay against
  `trades.db` + BingX candles; re-running it at the review point is mechanical. Its exact form is
  inlined below so a session with no memory can repeat it without rebuilding the definitions.

```python
# titan_asymmetry_replay.py — offline, read-only. No bot code, no hot path.
# Cohort:  virtual_positions status='closed' AND initial_risk_usdt>0     (R = net_pnl/initial_risk_usdt)
# §0-clean: recheck_status<>'tightened' AND NOT (opened_at<'2026-07-13T01:55'
#                                                AND closed_at>'2026-07-02T23:28')
# Live era: stop_order_id IS NOT NULL
# Gate quantity: gated = trades.confluence_score (RAW on executed rows, §0) + trades.macro_gate_penalty
# Regime:   BingX BTC/USDT:USDT 1d & 4h, CLOSED candles only, EMA9 vs EMA21 with EMA21 slope over 3 bars
#           bull = 9>21 and 21 rising · bear = mirror · flat = otherwise
# Location: 24 CLOSED 1h candles before the fill; loc = (fill-low)/(high-low); <0 or >1 = broke out
# Validation that must pass BEFORE any counterfactual is read:
#   (a) LONG n=26 -7.95R / SHORT n=33 +4.64R reproduce exactly
#   (b) every row's gated score clears the bar in force at its own timestamp (59/59)
# Significance: 20k-permutation on mean R, two-sided. Bonferroni across the cells actually tested.
```
