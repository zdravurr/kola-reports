# SHOULD MERCURY-SOL TRADE LONG ONLY? — candidate 32, the five controls

**2026-09-17 15:16 UTC · READ-ONLY pass · subject: Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · Titan untouched**

`openitems_guard` → **exit 0**, header and current-state table agree with runtime (titan-bot HEAD `f16c271`).

---

## 🔴 FIRST: THE COUNT IS WRONG. IT IS NOT NINE FOR NINE.

The brief says the live SHORT side stood at **0 wins in 8 (ΣR −6.832)** and that the −$3.2388 stop-out makes it
**0 in 9**. The first half is exact — I reproduce ΣR = −6.832 to three decimals over exactly those 8 trades.
The second half drops a trade.

Between the 8-trade snapshot and today, **two** live shorts closed, not one:

| # | opened | closed | side | entry → exit | R | $ | why |
|---|---|---|---|---|---|---|---|
| **46** | 2026-09-15 11:40 | 2026-09-15 15:25 | SHORT | 100.45 → 99.58 | **+0.368** | **+0.6030** | trail |
| 47 | 2026-09-15 20:10 | 2026-09-17 07:11 | SHORT | 97.28 → 100.31 | −1.069 | −3.2388 | sl |

Position **#46** is `is_paper=0`, `symbol=SOL/USDT:USDT`, `close_reason=trail`, breakeven applied, funding read
from the venue. Bybit confirms it independently: `2026-09-15 15:25 side=Buy qty=0.9 avgEntry=100.45
avgExit=99.58 closedPnl=+0.6030`. It is a live short. It won.

> ### THE LIVE SHORT SIDE IS **1 WIN IN 10**, ΣR **−7.533**. NOT 0 IN 9.
> Live LONG is **7 of 9, ΣR +12.453** — that figure I reproduce exactly.

Nine-for-nine was the headline the candidate was built on, and it is not what the book says. The record is still
bad — 10% win rate, −0.753R per trade — but "never once" and "once in ten" are different claims, and only one of
them is true. Everything below uses **10 live shorts**.

Second correction, smaller: **−$3.2388 is the largest single live loss in dollars, but only the 4th-worst in R**
(−1.069R). It was the largest because it carried the largest risk on the book ($3.03 vs a $1.64 median), not
because it was the worst-managed trade. #37 (−1.226R), #45 (−1.133R) and #44 (−1.110R) each lost more of their
own stop.

---

## 1. THE TWO BOOKS, SIDE BY SIDE

### 1a) LIVE — every position, from Bybit `/v5/position/closed-pnl` (GET only)

**LIVE LONG — n=9, 7 wins (77.8%), ΣR +12.453**

| # | opened → closed | entry → exit | R | MFE | MAE | why | `trend_1d` |
|---|---|---|---|---|---|---|---|
| 29 | 08-08 08:50 → 08-08 18:45 | 74.80 → 76.09 | +1.355 | +1.82R | +0.00R | exchange_UNKNOWN | neutral |
| 30 | 08-08 21:10 → 08-09 22:37 | 76.29 → 77.08 | +0.762 | +1.67R | −0.64R | trail | neutral |
| 31 | 08-10 08:10 → 08-10 15:21 | 76.96 → 75.90 | −1.155 | +0.13R | −0.98R | sl | bull |
| 33 | 08-11 22:00 → 08-12 13:00 | 76.50 → 76.61 | −0.049 | +0.61R | −0.55R | exit_signal | bull |
| 38 | 08-18 22:20 → 08-19 15:17 | 77.06 → 81.22 | +4.031 | +4.99R | −0.47R | trail | bull |
| 39 | 08-20 23:30 → 08-21 09:03 | 87.82 → 91.45 | +1.604 | +2.54R | −0.14R | trail | bull |
| 40 | 08-21 21:15 → 08-22 04:45 | 92.23 → 100.18 | +2.549 | +3.42R | −0.01R | trail | bull |
| 41 | 08-27 03:50 → 08-27 18:21 | 101.04 → 106.69 | +1.633 | +2.57R | −0.11R | trail | bull |
| 43 | 09-05 13:05 → 09-06 03:58 | 103.24 → 105.87 | +1.723 | +2.66R | −0.48R | trail | bull |

**LIVE SHORT — n=10, 1 win (10.0%), ΣR −7.533**

| # | opened → closed | entry → exit | R | MFE | MAE | why | `trend_1d` |
|---|---|---|---|---|---|---|---|
| 32 | 08-10 15:15 → 08-10 19:45 | 76.18 → 76.24 | −0.180 | +0.51R | −0.07R | exit_signal | bull |
| 34 | 08-13 16:40 → 08-13 17:12 | 75.21 → 75.76 | −0.643 | +0.12R | −0.49R | sl | bull |
| 35 | 08-14 14:20 → 08-14 15:30 | 75.16 → 75.57 | −0.701 | +0.18R | −0.37R | sl | neutral |
| 36 | 08-15 07:50 → 08-16 02:45 | 75.20 → 75.62 | −0.757 | +0.28R | −0.68R | exchange_market | neutral |
| 37 | 08-16 22:05 → 08-17 01:06 | 74.38 → 75.09 | −1.226 | +0.23R | −0.84R | sl | neutral |
| 42 | 09-01 21:40 → 09-03 13:42 | 99.24 → 101.87 | −1.083 | +0.73R | −0.98R | sl | neutral |
| 44 | 09-11 11:50 → 09-11 12:46 | 99.30 → 101.23 | −1.110 | +0.64R | −0.97R | sl | neutral |
| 45 | 09-14 00:50 → 09-14 03:12 | 99.56 → 101.24 | −1.133 | +0.24R | −0.99R | sl | neutral |
| **46** | 09-15 11:40 → 09-15 15:25 | 100.45 → 99.58 | **+0.368** | +1.35R | −0.47R | trail | neutral |
| 47 | 09-15 20:10 → 09-17 07:11 | 97.28 → 100.31 | −1.069 | +0.40R | −0.99R | sl | neutral |

*(A 20th live position, #48 LONG @ 100.37, opened 2026-09-17 09:05, is still open and excluded throughout.)*

### THE VENUE FIGURE, AND THE GAP

| | **BYBIT (venue)** | DB (`virtual_positions`) | DB − venue |
|---|---|---|---|
| LONG | **+$23.1556** | +$24.3161 | **+$1.1604** |
| SHORT | **−$13.2352** | −$13.2352 | **$0.0000** |
| **live book** | **+$9.9204** | **+$11.0808** | **+$1.1604** |

Canon `§LIVE-BOOK-VS-VENUE-GAP-2026-09-14` records the DB overstating by ≈$1.16. **Confirmed to the cent:
$1.1604.** It decomposes as:

* **−$0.8431 — two venue round-trips the book never recorded.** 2026-08-08 06:50 (`qty 2.6, 74.795→74.78,
  −$0.4279`) and 08:35 (`qty 2.6, 74.85→74.84, −$0.4152`). Fee-only scratches from the ccxt
  `acknowledged`/`fetch_order` failure documented in `main.py:77-95`. Real money, both **LONG**, absent from
  the book.
* **+$0.3173 — exit-fill slippage the DB modelled better than reality.** #40 +$0.2597 (DB says it exited
  100.18, the venue filled 99.92), #29 +$0.0246, #38 +$0.0240, #30 +$0.0090.

🔴 **The entire $1.16 sits on the LONG side. The SHORT side reconciles to zero.** Quoting the venue instead of
the DB makes the long-only case *weaker*, not stronger: the side the candidate wants to keep is the only side
whose book figure is inflated.

### 1b) PAPER — separate book, never pooled

**PAPER LONG — n=9, 2 wins (22.2%), ΣR −4.046, Σ$ −712.63**

| # | opened | entry → exit | R | MFE | MAE | why | `trend_1d` |
|---|---|---|---|---|---|---|---|
| 7 | 06-14 23:50 | 70.98 → 74.57 | +2.089 | +3.00R | −0.19R | exit_signal | neutral |
| 8 | 06-20 07:00 | 72.05 → 70.85 | −0.739 | +0.02R | −0.74R | exit_signal | *(null)* |
| 9 | 06-21 02:50 | 73.30 → 72.95 | −0.264 | +0.31R | −0.36R | exit_signal | neutral |
| 12 | 06-24 02:25 | 69.55 → 68.00 | −1.049 | +0.48R | −1.00R | sl | bear |
| 16 | 07-10 08:30 | 79.37 → 77.91 | −1.146 | +0.16R | −1.08R | sl | neutral |
| 18 | 07-14 15:45 | 77.47 → 75.74 | −1.074 | +0.89R | −1.02R | sl | neutral |
| 21 | 07-19 06:50 | 76.05 → 76.39 | +0.285 | +1.44R | −0.68R | trail | bear |
| 22 | 07-21 03:10 | 78.41 → 76.90 | −1.064 | +0.29R | −1.01R | sl | bull |
| 26 | 08-02 05:00 | 73.53 → 72.59 | −1.085 | +0.72R | −1.00R | sl | bear |

**PAPER SHORT — n=13, 6 wins (46.2%), ΣR −1.328, Σ$ −415.83**

| # | opened | entry → exit | R | MFE | MAE | why | `trend_1d` |
|---|---|---|---|---|---|---|---|
| 10 | 06-22 00:00 | 72.57 → 74.27 | −1.066 | +0.05R | −1.02R | sl | neutral |
| 11 | 06-23 00:30 | 71.43 → 69.20 | +1.133 | +1.71R | −0.29R | exit_signal | neutral |
| 13 | 06-24 13:25 | 68.63 → 66.31 | +1.337 | +2.36R | −0.48R | trail | bear |
| 14 | 06-25 14:00 | 64.85 → 67.41 | −1.032 | +0.09R | −1.00R | sl | bear |
| 15 | 07-08 05:05 | 78.56 → 78.20 | +0.140 | +1.18R | −0.11R | trail | neutral |
| 17 | 07-13 03:10 | 75.91 → 75.82 | +0.004 | +1.18R | −0.61R | sl | neutral |
| 19 | 07-16 00:25 | 77.04 → 76.27 | +0.463 | +0.97R | −0.33R | exit_signal | neutral |
| 20 | 07-17 13:40 | 73.58 → 75.05 | −1.124 | +0.16R | −1.07R | sl | neutral |
| 23 | 07-28 11:05 | 72.98 → 73.58 | −0.577 | +0.53R | −0.59R | exit_signal | bear |
| 24 | 07-29 20:05 | 72.67 → 74.29 | −1.050 | +0.25R | −1.00R | sl | bear |
| 25 | 08-01 17:20 | 72.47 → 71.36 | +1.257 | +2.51R | −0.01R | trail | bear |
| 27 | 08-03 06:45 | 72.53 → 73.07 | −0.660 | +0.59R | −0.57R | sl | bear |
| 28 | 08-06 19:00 | 72.77 → 72.84 | −0.153 | +0.49R | −0.18R | exit_signal | bear |

**Correction to the brief's premise.** "On PAPER, shorts BEAT longs" — true, and decisively, on every per-trade
measure: **46.2% vs 22.2% win rate, −0.102R vs −0.450R expectancy.** But paper shorts are **not profitable**:
ΣR −1.328, Σ$ −415.83. Both paper sides lost. The brief's stated kill-trigger is "if paper shorts are
profitable"; taken literally it does not fire. The trigger that *does* fire is the sign inversion — see §4d.
(Paper $ and live $ are not comparable: paper risked $100–390 per trade, live risks $0.91–3.03. **R is the only
common unit across the two books.**)

### 1c) 🔴 THE COLUMN THAT MATTERS — did they ever go green?

| book / side | MFE > 0 | **≥ +0.25R** | ≥ +0.5R | ≥ +1.0R | median MFE | mean give-back | went ≥+0.25R **then lost** |
|---|---|---|---|---|---|---|---|
| LIVE LONG | 9/9 | **8/9** | 8/9 | 7/9 | **+2.54R** | +0.89R | 1 |
| **LIVE SHORT** | **10/10** | **6/10** | 4/10 | **1/10** | **+0.34R** | **+1.22R** | **5** |
| PAPER LONG | 9/9 | 7/9 | 4/9 | 2/9 | +0.48R | +1.26R | 5 |
| PAPER SHORT | 13/13 | **10/13** | 8/13 | 5/13 | +0.59R | +1.03R | 4 |

**This is not the Titan pattern.** On Titan 77% of losses sit on positions that never moved. Here **every single
live short printed positive MFE** — the worst was +0.12R — and 6 of 10 reached +0.25R. Live shorts are **not
dead on arrival; the entry price is not the fault.**

What they cannot do is *go anywhere*. Median MFE **+0.34R**, and **only 1 of 10 ever reached +1.0R** — the one
that was banked (#46). Five went ≥+0.25R green and still lost. That is an exit/give-back signature layered on a
**shallow-excursion** one.

🔴 And the shallowness is not a property of the side. **The same side on paper reached nearly twice as far
(+0.59R median), while the same LONG side went from +0.48R on paper to +2.54R live — 5.3×.** Longs did not
become better traders between the two books. The tape changed. Hold that thought for §2c and §4e.

---

## 2. IS IT THE SIDE, OR THE REGIME, OR THE ERA?

### 2a) `trend_1d` at entry — every cell, both books

| book | side | `trend_1d` | n | wins | ΣR | mean R | |
|---|---|---|---|---|---|---|---|
| LIVE | LONG | bull | 7 | 5 | +10.336 | +1.477 | n<8 — **refuse to rank** |
| LIVE | LONG | neutral | 2 | 2 | +2.117 | +1.058 | n<8 — **refuse to rank** |
| LIVE | LONG | **bear** | **0** | — | — | — | 🔴 **EMPTY** |
| LIVE | SHORT | bull | 2 | 0 | −0.823 | −0.411 | n<8 — **refuse to rank** |
| LIVE | SHORT | neutral | **8** | 1 | −6.710 | −0.839 | ✅ only rankable cell on the board |
| LIVE | SHORT | **bear** | **0** | — | — | — | 🔴 **EMPTY** |
| PAPER | LONG | bull | 1 | 0 | −1.064 | −1.064 | n<8 — refuse to rank |
| PAPER | LONG | neutral | 4 | 1 | −0.394 | −0.098 | n<8 — refuse to rank |
| PAPER | LONG | bear | 3 | 1 | −1.850 | −0.617 | n<8 — refuse to rank |
| PAPER | SHORT | bull | 0 | — | — | — | empty |
| PAPER | SHORT | neutral | 6 | 4 | −0.450 | −0.075 | n<8 — refuse to rank |
| PAPER | SHORT | bear | 7 | 2 | −0.878 | −0.125 | n<8 — refuse to rank |

**1 of 12 cells clears n≥8.** The regime dimension is, on this data, not analysable.

### 2b) 🔴 Re-check of the 2026-09-14 bear-daily finding

**It still holds — and it holds trivially, which the re-check must say out loud.**

Paper SHORT with BEAR daily: **2 of 7, ΣR −0.878.** Paper SHORT with NEUTRAL daily: **4 of 6, ΣR −0.450.**
Identical to the 2026-09-14 pass, to the trade. The reason is that **paper has not traded since 2026-08-07**;
the paper book is frozen at 22 positions. A re-check against a frozen sample cannot move, so this is **not
independent confirmation** — it is the same measurement read twice.

What *is* new is the like-for-like across books, at the same label:

| cell | n | wins | ΣR | mean R |
|---|---|---|---|---|
| paper SHORT, **BEAR** daily | 7 | 2 (29%) | −0.878 | −0.125 |
| paper SHORT, **NEUTRAL** daily | 6 | 4 (67%) | −0.450 | −0.075 |
| **live SHORT, NEUTRAL daily** | 8 | 1 (12%) | **−6.710** | **−0.839** |

* same book, different label (paper bear vs paper neutral): permutation **p = 0.938** — the bear daily made
  **no difference at all** to paper shorts.
* **same label, different book** (paper neutral vs live neutral): **p = 0.066** — an 11× gap in mean R on
  identical labels.

**The 2026-09-14 conclusion stands: the gap is between BOOKS, not between LABELS.** The regime tag is inert;
the book/era is where the variance lives. Note also that paper shorts' *best* regime by win rate was NEUTRAL —
the very regime live shorts have been losing in.

### 2c) The tape over the live era

* First live entry **74.80** (2026-08-08 08:50). SOL now **100.55** (Bybit, 2026-09-17 15:06 UTC). **+34.4%.**
* Peak **110.61** (2026-08-27 high) = **+47.9%** from the first entry.
* **38 trading days carry signal rows in the live era. Zero contain a single BEAR 1d row.** The last BEAR daily
  label anywhere in the database is **2026-08-07** — the day before live trading began. Modal daily label
  across the live era: **23 days bull, 15 days neutral, 0 days bear.**

🔴 **The live book is one long rally.** A side that has never once had the market with it is not the same thing
as a side that does not work.

In fairness to the opposite reading: the rally was **not** monotonic. The largest live-era pullback ran
**110.61 → 95.69 = −13.5%** (2026-08-27 → 2026-09-15), and shorts #42, #44, #45, #46, #47 were all fired into
that chop. One of them (#46) caught the 2026-09-15 dump and won. #47 shorted 97.28 near that dump's low and was
run over on the bounce. So the shorts did get *down-legs* to trade — they just never got a **regime**, and the
book's own label agrees: not one of them was tagged BEAR.

### 2d) 🔴 Chronological halves within the live SHORT side

| half | trades | n | wins | ΣR | mean R |
|---|---|---|---|---|---|
| H1 (2026-08-10 → 08-16) | #32 #34 #35 #36 #37 | 5 | 0 | −3.506 | −0.701 |
| H2 (2026-09-01 → 09-17) | #42 #44 #45 #46 #47 | 5 | **1** | **−4.027** | −0.805 |

**Not front-loaded. If anything the back half is worse.** The single win sits in H2, and the mean loss deepens
from −0.70R to −0.81R. The character also changed: H1 was small bleeds (three closes inside 24h, two by
exit_signal); H2 is four near-full stop-outs (−1.083, −1.110, −1.133, −1.069R) and one banked trail. The side
is losing consistently over time, not because of one bad early cluster. **This control passes** — it is the
only one that does.

---

## 3. WHAT A LONG-ONLY RULE WOULD HAVE COST — as a subtraction

### 3a) Volume lost

| book | month | LONG | SHORT | total | shorts |
|---|---|---|---|---|---|
| PAPER | 2026-06 | 4 | 4 | 8 | 50% |
| PAPER | 2026-07 | 4 | 6 | 10 | 60% |
| PAPER | 2026-08 | 1 | 3 | 4 | 75% |
| LIVE | 2026-08 | 8 | 5 | 13 | 38% |
| LIVE | 2026-09 | 2 | 5 | 7 | **71%** |

Over the whole live era shorts are **10 of 20 entries = 50%**. In September alone, **5 of 7 = 71%**. On paper,
**13 of 22 = 59%**.

### 3b) ΣR and Σ$ with and without shorts

| book | full book | long-only | Δ | removed SHORT side |
|---|---|---|---|---|
| **LIVE** | n=19, ΣR **+4.920**, $ **+11.0808** (venue **+9.9204**) | n=9, ΣR **+12.453**, $ **+24.3161** (venue **+23.1556**) | **+7.533R / +$13.2352** | n=10, ΣR −7.533, $ −13.2352 |
| **PAPER** | n=22, ΣR **−5.374**, $ −1128.46 | n=9, ΣR **−4.046**, $ −712.63 | **+1.328R / +$415.83** | n=13, ΣR −1.328, $ −415.83 |

🔴 **The brief asks me to state plainly that on paper this removes a profitable side. I cannot — that is not
what the book says, and I will not fabricate it.** Paper shorts **lost**: ΣR −1.328, Σ$ −415.83. Removing them
*improves* paper's ΣR from −5.374 to −4.046.

What must be stated plainly is worse for the candidate, not better:

> **On paper, long-only keeps the side with WORSE expectancy and throws away the better one.**
> Paper LONG **−0.450R** per trade, 2 wins in 9. Paper SHORT **−0.102R** per trade, 6 wins in 13.
> The ΣR improves only because you are running 9 trades instead of 22. Per unit of risk deployed,
> long-only makes the paper book **4.4× worse per trade**. Matched trade-for-trade, a long-only paper
> book of 22 positions projects to **≈ −9.9R** against the actual **−5.37R**.

### 3c) Entries per day, and what stalls

| book | span | entries | /day | long-only | /day | volume kept |
|---|---|---|---|---|---|---|
| LIVE | 2026-08-08 → 09-17, 41 days | 20 | 0.488 | 10 | 0.244 | **50%** |
| PAPER | 2026-06-14 → 08-07, 55 days | 22 | 0.400 | 9 | 0.164 | 41% |

**It halves the book, exactly.** The named cost, measured in the tables that feed the learners:

* `smart_exit_dryrun_samples` — **230 of 505 rows are SHORT (46%).** `EXIT_ADVISOR_DRYRUN=True`, hourly per
  open position: halve the open positions, halve the advisor's evidence. The advisor is still trying to earn
  its way out of dry-run; this doubles that wait.
* `position_excursion_samples` — **12,355 of 25,387 are SHORT (49%).**
* `post_exit_observatory` — **23 of 44 are SHORT (52%).**
* `book_gate` is **ARMED** (`BOOK_GATE_DRYRUN=False`, clause A, `BOOK_GATE_MIN_SUPPORTING=1`). Its
  per-side lean floors (`BOOK_GATE_LEAN_FLOOR`) are calibrated on **each side's own** distribution; the SHORT
  distribution would freeze at today's sample and go stale.
* **Partial offset, and it is real:** a refusal at the risk gate still writes a `skip_attribution` row with
  `direction`, `max_favorable_price` and drift tracking. The live era already holds **3,880 SHORT skip rows**.
  So the *counterfactual* short sample keeps growing even under long-only — what dies is the **realised** one,
  which is the only sample that contains exits, fees, funding and slippage.

### 3d) 🔴 Is it reversible? **Yes — this is a config flag, not a removed subscription.**

The signal source is the TradingView webhook, which delivers both directions into the same handler
(`main.py:4367`, `position_side = direction`). Nothing would be unsubscribed. The book already contains the
exact precedent: `_dxy_halt(requested_side)` at `main.py:2003`, a **side-scoped halt with a DRYRUN twin**
(`DXY_HALT_DRYRUN=True`, `config.py:1359`), wired into the risk-gate chain at `main.py:2045` between the macro
halt and the daily-loss breaker.

A long-only rule is that same shape: one config constant plus a four-line gate in the same chain. Flipping it
back is one line and a restart. **Fully reversible.** *(Stated as a fact about the codebase; per §5 I am not
writing the diff, because the candidate does not survive.)*

---

## 4. THE FIVE CONTROLS

> 🔴 **BONFERRONI DECLARED IN THE HEADER.** The frame is every **side × regime × book** cell:
> 2 sides × 3 regimes (bull/neutral/bear) × 2 books = **m = 12**. Corrected threshold **α = 0.05/12 =
> 0.004167**. Tests are two-sided permutation on mean R (200,000 resamples, seed 20260917) and Fisher exact on
> win counts. Every p below is compared against 0.004167, not 0.05.

### (a) Bonferroni — **SPLIT: one test survives, one does not**

| test | statistic | p | vs α=0.004167 |
|---|---|---|---|
| LIVE LONG vs LIVE SHORT, mean R | +1.384R vs −0.753R (Δ 2.137R) | **0.00054** | ✅ **survives** |
| LIVE LONG vs LIVE SHORT, win counts | 7/9 vs 1/10 | **0.00548** | ❌ **fails** |
| PAPER LONG vs PAPER SHORT, mean R | −0.450R vs −0.102R | 0.4226 | — no effect |
| PAPER LONG vs PAPER SHORT, win counts | 2/9 vs 6/13 | 0.3802 | — no effect |
| LIVE SHORT vs PAPER SHORT, mean R | −0.753R vs −0.102R | 0.0583 | ❌ fails |

The live side effect is real in magnitude but **the headline count — the win record itself — does not clear the
correction.** The number the whole candidate is named after is the one that fails.

### (b) Chronological halves — **FAILS on the paper short side**

| book / side | H1 | H2 | same sign? |
|---|---|---|---|
| LIVE LONG | n=5, ΣR +4.944, 3 wins | n=4, ΣR +7.509, 4 wins | ✅ yes |
| LIVE SHORT | n=5, ΣR −3.506, 0 wins | n=5, ΣR −4.027, 1 win | ✅ yes |
| PAPER LONG | n=5, ΣR −1.108, 1 win | n=4, ΣR −2.938, 1 win | ✅ yes |
| **PAPER SHORT** | n=7, ΣR **+0.979**, **5 wins in 7** | n=6, ΣR **−2.307**, 1 win in 6 | ❌ **SIGN FLIPS** |

The paper short side was **profitable in its own first half** and then inverted. A side whose sign flips inside
its own book is not a stable side effect — it is a period effect. **Control fails.**

### (c) Regime split with BOTH legs populated — **FAILS. Reported as a failure, not as a one-legged result.**

**The live BEAR leg is n = 0. For both sides.** The live era has not seen a single BEAR 1d row in 38 days of
signals. 11 of 12 side × regime × book cells fall below the n≥8 refuse-to-rank line; the only cell that clears
it is LIVE/SHORT/neutral (n=8), and a control cannot be run on one leg.

I am not reporting "live shorts lose in NEUTRAL and BULL" as a regime result. **It is a regime control that
could not be run.**

### (d) 🔴 PAPER AS THE INDEPENDENT SAMPLE — **FAILS. The sign inverts.**

| book | LONG mean R | SHORT mean R | which side is better | margin |
|---|---|---|---|---|
| LIVE | **+1.384** | −0.753 | **LONG** | +2.137R |
| PAPER | −0.450 | **−0.102** | **SHORT** | **−0.347R** |

Win rates: live LONG 77.8% / SHORT 10.0%. Paper LONG 22.2% / **SHORT 46.2%**.

**On the independent sample the ranking reverses. Shorts are the better side on paper, on both expectancy and
win rate.** No softening: this is the same failure that killed candidates 21, 22, 29 and 30, and by the
standing rule it kills this one.

Two honest qualifiers, neither of which rescues the candidate:
1. **The inversion is not itself significant** (p = 0.4226). Paper says "no side effect", not "shorts win". But
   the standing rule tests whether the live finding **replicates**, and "no effect, opposite sign" is a
   non-replication either way.
2. **Paper shorts are not profitable** (ΣR −1.328). The brief's literal trigger — *"if paper shorts are
   profitable, the sign inverts"* — does not fire on the first clause. It fires on the second, which is the
   operative one.

### (e) 🔴 THE CONFOUND — **FAILS. "SHORT" is not separable from the live era.**

Every live short's `trend_1d` at entry: **8 neutral, 2 bull, 0 bear.** Every live long's: **7 bull, 2 neutral,
0 bear.** The last BEAR daily anywhere is 2026-08-07; live trading began 2026-08-08. **On this book, "SHORT"
and "traded a market that has not printed a bear daily in its entire existence" are the same set of rows.**
There is no row that separates them. That is textbook collinearity — the same structure that killed candidate
31, where a trigger name *was* its side.

The decisive evidence is the **same side across books**:

| side | median MFE, PAPER | median MFE, LIVE | ratio |
|---|---|---|---|
| LONG | +0.48R | **+2.54R** | **5.3×** |
| SHORT | +0.59R | **+0.34R** | 0.58× |

Longs did not acquire skill between 2026-08-07 and 2026-08-08. **The +34.4% rally arrived.** The same signal
generator, the same exit logic, the same risk model produced shallow +0.48R longs on paper and +2.54R longs
live. If the era can move one side by 5.3×, the era — not the side — is the live book's dominant term, and the
side coefficient cannot be read out from underneath it.

**Control (e) fails: the side and the era cannot be told apart on this data.**

---

## 5. VERDICT

### 🔴 CANDIDATE 32 — LONG-ONLY — **NOT CONVICTED.** Record it and do not apply it.

**Controls: (a) SPLIT — the mean-R test clears Bonferroni, the win-count test does not. (b) FAILS — the paper
short side flips sign inside its own book. (c) FAILS — the live BEAR leg is empty; the control could not be
run. (d) FAILS — the independent sample inverts the ranking. (e) FAILS — side and era are collinear.**

One control of five passes cleanly (2d: the live short losses are evenly spread, not front-loaded). Two of the
five fail in exactly the two ways the standing frame calls fatal: **paper inverts the sign, and the side cannot
be separated from the era.**

And the headline was wrong. **The live short side is 1 in 10, not 0 in 9** — and even 0-in-9 would not have
been a licence: candidate 31 was 0 winners in 13 **across both books** and could not be convicted either. This
one is 1-in-10 in **one** book, while the **other** book ranks the same side as the better of the two.

Nothing here says shorts are good. The live short side is genuinely bad — −0.753R per trade over 10 trades,
median excursion +0.34R, 1 win. What the evidence cannot do is tell you whether that is *the side* or *the
41 days in which it was the only side facing the tape*. Trading a −13.5% pullback inside a +34% rally is not a
test of shorting; it is a test of counter-trend timing in one regime, and the book's own labels never once
called that regime BEAR.

### 🔴 WHAT WOULD SETTLE IT

**n and condition, specifically:**

1. **8 live SHORT entries with `trend_1d = BEAR` at entry.** Eight is the book's own refuse-to-rank line, and
   it is the minimum that turns control (c) from *not run* into *run*. Today that cell is n=0 and the last
   BEAR daily was 41 days ago.
2. **The live SHORT side reaching n ≥ 20 overall**, so the Fisher win-count test — the one that actually
   failed Bonferroni at n=10 — can clear α=0.004167. *(The mean-R test already clears it: at the observed
   mean/sd, n=4 suffices. It is the win record, not the magnitude, that is underpowered.)*

**What those first 8 BEAR-daily shorts must show:**

* **To CONVICT long-only:** ΣR **< 0** with **≤ 2 winners** — shorts fail *even with the regime behind them*.
  That, and only that, separates the side from the era: it would show the side losing in the one condition the
  era has never supplied. Combined with an unchanged live long side, candidate 32 could then be re-opened with
  control (c) run and control (e) broken.
* **To ACQUIT it permanently:** **≥ 4 of 8 winners with ΣR ≥ 0.** The side works once the regime allows it,
  and the entire 1-in-10 record was the era. Close the question.
* **The arithmetic bar:** 8 BEAR-daily shorts would need **mean R ≥ +0.942** merely to bring the live SHORT
  side back to ΣR = 0 (10 shorts would need +0.753, 12 would need +0.628). Long-only stays *plausible* across a
  wide range of outcomes — but plausible is not convicted, and the five controls are what convict.

**What no amount of live data will fix:** the paper book is **frozen at 2026-08-07**. Control (d) cannot be
re-run against new paper trades because there are none. Re-opening a paper/shadow stream, or promoting the
`skip_attribution` counterfactual (3,880 live-era SHORT skip rows already carry `max_favorable_price` drift
tracking) into a scored second sample, is the only route to a genuinely independent re-test. **Until then, any
future long-only pass will fail control (d) the same way, on the same frozen data.**

---

## READ-ONLY CONFIRMATION

| check | state |
|---|---|
| `openitems_guard` | **exit 0** — clean, run first |
| SOL DB | opened `file:…/trades.db?mode=ro` with `PRAGMA query_only=1` (verified = 1). **No writes.** |
| SOL config | read via `ast.literal_eval` on the source text. **Never imported.** sha256 `a308a130…149c7`, unchanged |
| Venue | **GET only** — `/v5/market/time`, `/v5/market/tickers`, `/v5/market/kline`, `/v5/account/wallet-balance`, `/v5/position/closed-pnl`. **No orders placed, amended or cancelled.** |
| `mercury-sol.service` | `NRestarts=0`, `MainPID=2245907`, active since 2026-09-14 22:20:45 — **unchanged, not restarted** |
| `titan.service` | `NRestarts=0`, `MainPID=1572470`, active since 2026-09-12 14:58:32 — **unchanged, not restarted** |
| `FLAT_ADX_GATE_DRYRUN` | **True** (SOL `config.py:407`) — unchanged |
| `BOOK_GATE_DRYRUN` | **False** (SOL `config.py:475`; Titan also False) — unchanged |
| **Titan** | **UNTOUCHED.** Read only `tools/openitems_guard.py` (its own read-only self-check) and `config.py` as text. No file written, nothing applied, nothing restarted. |
| Proposals applied | **none.** No diff written, no flag changed, no change proposed beyond the §3d factual statement of shape. |

*Live open position #48 (LONG @ 100.37, opened 2026-09-17 09:05) was observed and excluded from every table.*
