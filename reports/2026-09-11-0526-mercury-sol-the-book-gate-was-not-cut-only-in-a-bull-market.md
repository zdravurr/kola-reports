# Mercury-SOL — the book gate was not cut only in a bull market, but it has never RUN in a bear one: the daily trend does not move the book's lean, a bear daily does make the bid wall under a short big — which the wall clause would bite on (predicted, not measured) — and in today's bull tape the gate already breaches its own side-ratio wire

_2026-09-11 05:26 UTC_

---

**2026-09-11 05:26 UTC · READ-ONLY · Mercury-SOL (LIVE, `is_paper=0`) · book gate armed 2026-08-10 18:25, re-cut 2026-08-14 18:28**

**Controls.** n is stated per cell before any result, and nothing is ranked below n = 8. Every ranked comparison is Bonferroni-corrected, with k and α in its header. Books repeat, because the same book is re-offered on consecutive 5m bars, so every test is also run on **one book per side per hour**. Only SOL data is used; the two bots are never pooled.

## 🔴 First, the premise and the plain answer to §1d

- **The live gate has never evaluated a single bear-daily book.** The last `trend_1d = BEAR` anywhere in the record is **2026-08-07 05:55**. The gate was armed on 2026-08-10 at 18:25. Of the 1,132 rows it has evaluated, 1,087 store a label: BULL 866, NEUTRAL 220, unknown 1. The 45 refused rows store none; 25 take a regime from the nearest row within 30 minutes (19 BULL, 6 NEUTRAL) and 20 have no such row. None of them can be BEAR, because no row anywhere reads BEAR after 2026-08-07 05:55. **From the gate's own evaluated rows, the question cannot be answered.**
- **The thresholds were not cut only under a bull daily.**
  - The **2026-08-10 design cut** drew on 3,454 books from 2026-06-08 → 08-10: **BEAR 1,313 (38 %)**, NEUTRAL 1,455, BULL 665, unknown 21.
  - The **2026-08-14 re-cut window** (rows that reached the gate, 2026-08-03 → 08-14) held **BEAR 137 (24 %)**, all 08-03 → 08-07, plus NEUTRAL 267 and BULL 157.
  - What is true is narrower: every refusal the gate has made, and the **realised** calibration that triggered the re-cut, came from a BULL/NEUTRAL tape.
- **So §2 is the route, and it is usable.** SOL stored the same OKX wall book the gate reads from 2026-06-08 onward. Its record holds **1,313 bear-daily books (664 LONG / 649 SHORT)**, in the exact shape `book_gate.read_book` accepts.

## The answer, decision-shaped

1. **The lean floors (clause B) are not bull-calibrated in any way the data can see.** The lean distribution does not move with the daily trend on either side. Medians sit within 0.7 pp of each other, and all six daily-axis Mann-Whitney tests are non-significant after Bonferroni. The bear-daily 2nd percentile sits **above** both live floors: **LONG 0.4340 vs floor 0.4238 (+1.02 pp); SHORT 0.4212 vs floor 0.3489 (+7.23 pp)**. In a bear daily, clause B would bite *less* often, not more.
2. **The wall clause (A) is where a bear market shows up, and only for SHORTS.** Under a bear daily, the nearest bid wall below a short entry is in the top decile for its side **29.1 % of the time, against 1.7 % under a bull daily** (one book per side per hour, n 182 vs 116, Fisher p = 5×10⁻¹¹). On the 4h axis it is 31.9 % vs 1.7 %. For longs there is no difference (11.6 % vs 9.2 %, p = 0.68). Resting liquidity **does** pile up below price in a falling market; it shows up as **bigger bid walls, not as a shifted imbalance**.
3. **Replayed at the live constants on the bear-daily books: LONG 1.20 %, SHORT 2.00 %, side ratio 1.66×** — inside the gate's alarm. Those books are the pre-gate population, though. On the same regimes, the population the gate actually evaluates refuses about 3× more. **Era-adjusted, a bear daily predicts SHORT ≈ 7.6 % (all clause A) and LONG ≈ 3.3 %.** That would breach the 5 % wire on SHORT and flip the side ratio to about 2.3× against shorts. 🔴 **This is a prediction, not a measurement.** The clause-A era factor rests on 0.24 % → 0.92 %, a handful of events.
4. **A separate finding, measured, not predicted: in today's bull/neutral tape the gate already breaches its own side-ratio wire.** Since the 2026-08-14 re-cut it refused **17 of 481 LONG (3.53 %) against 3 of 481 SHORT (0.62 %) — 5.67×, exact two-sided p = 0.0026.** The LONG refusals are 11 clause B and 6 clause A. The re-cut's review point was "200 further gate evaluations or 2026-09-14". It came on 2026-08-20 and was **never checked**: the 200th post-re-cut evaluation was at 2026-08-20 23:30:02: LONG 9/117 = 7.69 %, SHORT 3/83 = 3.61 %, ratio 2.13×. The count now stands at **962 evaluations**. The pre-registration says a breach is "grounds to revisit … re-cut the ruler and say so". This pass records the breach; it does not revisit.
5. **Watch item, stated in §4c:** when `trend_1d` first reads BEAR, re-measure the refusal rate per side over the first **N = 100 gate evaluations per side**, spanning at least 5 distinct days. That is about 6 days at the current 18 evaluations per side per day.

**Nothing is proposed and nothing is applied.**

---

## 1. Does the book's shape depend on the regime?

### 1a. Counts per regime cell

Every trades row with an OKX wall book in the shape the gate reads: **4,541 books**, 2026-06-08 00:40 → 2026-09-11 04:30. Each book carries the daily and 4h OHLCV trend labels stored on the same row, at that instant.

| window | BEAR daily | BULL daily | NEUTRAL daily | unknown |
|---|---|---|---|---|
| design window, 2026-06-08 → 08-10 18:25 | **1,313** | 665 | 1,455 | 21 |
| re-cut window, rows reaching the gate, 08-03 → 08-14 | **137** | 157 | 267 | — |
| gate era, ≥ 2026-08-10 18:25 | **0** | 866 | 220 | 1 |
| rows the live gate evaluated (stored `book_gate_*`) | **0** | 885 | 226 | 21 without a label |

Per side, all books, daily axis: BEAR 664 LONG / 649 SHORT · BULL 686 / 845 · NEUTRAL 734 / 941. 4h axis: BEAR 711 / 643 · BULL 506 / 964 · NEUTRAL 854 / 811. **Too thin to read:** the `unknown` cells (daily 7 LONG / 15 SHORT; 4h 20 / 32). The daily `unknown` LONG cell is below 8 and is not read. No regime cell is thin. **Every bear-daily book predates the gate.**

### 1b. The lean (±1 % imbalance, toward the proposed side) per regime

`lean` = bid share within ±1 % of mid for a LONG, 1 − that for a SHORT. This is exactly what clause B compares with `BOOK_GATE_LEAN_FLOOR` (LONG 0.4238, SHORT 0.3489).

Daily axis, all books:

| regime | side | n | lean med | q1 | q3 | p2 [95% boot CI] | p2−floor (pp) | sd |
|---|---|---|---|---|---|---|---|---|
| bear | LONG | 664 | 0.5058 | 0.4846 | 0.5331 | 0.4340 [0.4279,0.4494] | 1.02 | 0.0391 |
| bear | SHORT | 649 | 0.4991 | 0.4722 | 0.5237 | 0.4212 [0.4111,0.4298] | 7.23 | 0.0377 |
| bull | LONG | 686 | 0.5118 | 0.4853 | 0.5453 | 0.4398 [0.4356,0.4447] | 1.6 | 0.0487 |
| bull | SHORT | 845 | 0.4929 | 0.4658 | 0.5192 | 0.4006 [0.3879,0.4122] | 5.17 | 0.041 |
| neutral | LONG | 734 | 0.5120 | 0.483 | 0.5387 | 0.4307 [0.4259,0.4337] | 0.69 | 0.0411 |
| neutral | SHORT | 941 | 0.4953 | 0.4697 | 0.5245 | 0.4160 [0.4103,0.4241] | 6.71 | 0.0401 |

Daily axis, one book per side per hour:

| regime | side | n | lean med | q1 | q3 | p2 [95% boot CI] | p2−floor (pp) | sd |
|---|---|---|---|---|---|---|---|---|
| bear | LONG | 189 | 0.5045 | 0.4837 | 0.5326 | 0.4317 [0.4105,0.4517] | 0.79 | 0.0385 |
| bear | SHORT | 182 | 0.4954 | 0.4674 | 0.5202 | 0.4217 [0.3957,0.4313] | 7.28 | 0.0379 |
| bull | LONG | 239 | 0.5113 | 0.4842 | 0.5347 | 0.4412 [0.4353,0.4507] | 1.74 | 0.0451 |
| bull | SHORT | 278 | 0.4933 | 0.4644 | 0.5164 | 0.3949 [0.3590,0.4119] | 4.6 | 0.0441 |
| neutral | LONG | 202 | 0.5103 | 0.4826 | 0.5363 | 0.4330 [0.4215,0.4415] | 0.92 | 0.0414 |
| neutral | SHORT | 223 | 0.4929 | 0.4654 | 0.5242 | 0.4000 [0.3802,0.4197] | 5.11 | 0.044 |

4h axis, all books:

| regime | side | n | lean med | q1 | q3 | p2 [95% boot CI] | p2−floor (pp) | sd |
|---|---|---|---|---|---|---|---|---|
| bear | LONG | 711 | 0.5140 | 0.4921 | 0.5373 | 0.4366 [0.4334,0.4452] | 1.28 | 0.038 |
| bear | SHORT | 643 | 0.4880 | 0.4647 | 0.5134 | 0.4122 [0.4079,0.4212] | 6.33 | 0.0357 |
| bull | LONG | 506 | 0.5114 | 0.4853 | 0.5339 | 0.4366 [0.4315,0.4433] | 1.28 | 0.0429 |
| bull | SHORT | 964 | 0.4980 | 0.4722 | 0.5275 | 0.4200 [0.4119,0.4272] | 7.11 | 0.0402 |
| neutral | LONG | 854 | 0.5061 | 0.4808 | 0.5418 | 0.4297 [0.4260,0.4352] | 0.59 | 0.0477 |
| neutral | SHORT | 811 | 0.4986 | 0.4701 | 0.5263 | 0.3971 [0.3891,0.4129] | 4.82 | 0.042 |

**Does the 2nd percentile move between regimes?** Not detectably. Tested with one book per side per hour (Bonferroni k = 12, α = 0.0042):

| comparison | LONG: median / p2 difference [Bonferroni CI] | SHORT: median / p2 difference [Bonferroni CI] |
|---|---|---|
| daily BEAR vs BULL | 0.5045 vs 0.5113, p = 0.34 / −0.95 pp [−3.95, +1.78] — ns | 0.4954 vs 0.4933, p = 0.42 / +2.68 pp [−1.58, +7.14] — ns |
| daily BEAR vs NEUTRAL | p = 0.79 / −0.14 pp — ns | p = 1.00 / +2.17 pp — ns |
| daily BULL vs NEUTRAL | p = 0.42 / +0.82 pp — ns | p = 0.44 / −0.51 pp — ns |
| 4h BEAR vs BULL | p = 0.46 / +0.33 pp — ns | **0.4847 vs 0.5002, p = 0.0003 — SIGNIFICANT** / +0.13 pp [−2.78, +2.82] — ns |
| 4h BEAR vs NEUTRAL | p = 0.23 / +1.05 pp — ns | p = 0.07 / +2.71 pp — ns |
| 4h BULL vs NEUTRAL | p = 0.59 / +0.72 pp — ns | p = 0.09 / +2.58 pp — ns |

The one significant result: **under a bear 4h, a short's book leans 1.5 pp further against it in the body**, meaning more bid share. **The 2nd percentile, the only number clause B uses, does not move** (+0.13 pp). The body shifts; the tail does not.

### 1c. The opposing wall, and depth

| regime | side | n | nearest opp mult p50 / p98 | share opp pctl ≥ 90 | share opp dist ≤ 0.20 % | both (clause A) | wall vol bid/ask p50 |
|---|---|---|---|---|---|---|---|
| bear | LONG | 664 | 14.8 / 22.0 | 10.1 % | 23.9 % | 0.15 % | 1.007 |
| bear | SHORT | 649 | 18.5 / 30.4 | 22.0 % | 25.4 % | 2.00 % | 1.065 |
| bull | LONG | 686 | 14.1 / 23.7 | 11.5 % | 26.5 % | 0.00 % | 1.004 |
| bull | SHORT | 845 | 12.8 / 25.8 | 3.7 % | 34.8 % | 0.00 % | 0.943 |
| neutral | LONG | 734 | 14.1 / 21.8 | 10.2 % | 29.8 % | 0.54 % | 1.125 |
| neutral | SHORT | 941 | 16.7 / 25.6 | 4.9 % | 24.5 % | 0.32 % | 1.147 |

- **For SHORTS under a bear daily, the opposing wall grows.** Its median nearest bid-wall multiple is ×18.5 against ×12.8 under a bull daily, and it sits at or above p90 of its side 22.0 % of the time against 3.7 %. With one book per hour the gap is 29.1 % against 1.7% (p = 5×10⁻¹¹). Its distance is not closer: it is within 0.20 % 25 % of the time against 35 %.
- **For LONGS the opposing ask wall does not change with the regime.**
- **Total depth per side is not stored.** The OKX record keeps only the ±1 % imbalance and the walls above 4× the average level. The bid/ask ratio of total wall volume is the closest proxy, and it hardly moves: median 1.065 for bear-daily SHORT books against 0.943 for bull.

---

## 2. The longer history

### 2a. What was stored, and when

- **`trades.orderbook_json`** holds the OKX wall book `{mid, imbalance, walls_bid[], walls_ask[], wall_threshold_mult, depth}` from **2026-06-08 00:40 (row 91)**. The stored `depth` field reads **8000 on all 4,541 books**. It is written on refused and advisor paths. On executed rows it is overwritten by a Bybit depth-20 microstructure dict, which the gate's own shape guard rejects. For those rows the **`advisor_book_json`** copy is used, and it exists from **2026-08-02 17:10**.
- 🔴 **The brief's "OKX-4000 depth collection began 2026-08-02" is not what the record shows.** The gate-shaped OKX wall book is stored from 2026-06-08. What began on 08-02 is `advisor_book_json`, the copy that identifies an admitted row, which is why the 08-14 re-cut could not reach further back than 08-03.
- **Bear-daily days inside the usable span:** the daily read BEAR on 425 June rows, 622 July rows and 274 August rows (all ≤ 08-07). In the replayed population that is **1,313 books across 2026-06-08 → 2026-08-07**.

### 2b. Bear-daily 2nd percentile against the live thresholds

| side | bear-daily n | lean p2 [95 % boot CI] | live floor | gap | one book / side / hour |
|---|---|---|---|---|---|
| LONG | 664 | **0.4340** [0.4279, 0.4494] | 0.4238 | **+1.02 pp** (floor below the bear p2) | 0.4317, +0.79 pp (n 189) |
| SHORT | 649 | **0.4212** [0.4111, 0.4298] | 0.3489 | **+7.23 pp** | 0.4217, +7.28 pp (n 182) |

In a bear daily, the fraction of books below the live floor is **LONG 1.05 %, SHORT 0.00 %**. The clause-A inputs, the percentile ruler `_NEAR_MULT_BREAKS` and the 0.20 % distance, were cut over the same 06-08 → 08-10 window that is 38 % bear-daily.

### 2c. Titan / BTC — not used

SOL has 1,313 bear-daily books of its own, so there was no reason to borrow a mechanism from BTC. **Titan's database was not opened.** For the record, as the brief requires: **BTC constants are dead on SOL.** A different instrument, venue, tick size and wall scale mean none of Titan's numbers could set SOL's.

### 2d. Provenance of the thresholds — read from the reports, the canon and the DB by a separate agent

- **Design cut, 2026-08-10.** It covered scored signals with an OKX book from 2026-06-08 to 08-10: 3,449 reproducible rows, though the design report says 3,454. Lean p2 came out at LONG 0.4323 and SHORT 0.4129. Clause A used p90 on the per-side ruler and the distance was set at 0.20 %, the observed Q1. **The daily trend of that population was BEAR 1,311 / NEUTRAL 1,454 / BULL 663 / null 21 — only 19.2 % BULL.** The p2 per regime inside it was LONG bull 0.4404 / bear 0.4340 / neutral 0.4307, and SHORT bull 0.4105 / bear 0.4211 / neutral 0.4147.
- **Re-cut, 2026-08-14 18:28.** The population was every row that reached the gate. The DB reproduces n = 249 / 374 and the floors 0.4238 / 0.3489 **only when the window starts 2026-08-02 17:10**, at the first `advisor_book_json`; the report and config say 08-03. Its daily trend was LONG BEAR 95 / NEUTRAL 65 / BULL 89, and SHORT BEAR 73 / NEUTRAL 208 / BULL 93. **But the tail that sets the floor is bull-only.** All 8 SHORT rows below 0.3489 are bull-daily rows, mostly from the armed window of 08-11 → 08-14. Of the 5 LONG rows below 0.4238, 4 are bull and 1 is bear. The population was mixed; the 2nd percentile was set by bull days. That is the precise sense in which the operator's suspicion holds. It pushes the SHORT floor *down*, which makes clause B quieter, not louder, on bear-daily books.
- **The pre-registered wires (config and OPEN-ITEMS-SOL.md, verbatim):** *"IF THE REALISED RATE IS MATERIALLY DIFFERENT — ABOVE 5 % ON EITHER SIDE, OR A SIDE RATIO ABOVE 2× — THAT IS A FINDING ABOUT THE CALIBRATION AND GROUNDS TO REVISIT … the correct response is to re-cut the ruler and say so."* The re-registration expected LONG 2.01 % and SHORT 2.14 % (1.07×), with the review point at *"200 further gate evaluations, or 2026-09-14, whichever first"*.
- 🔴 **The review point was never checked.** No report or canon entry performs it. Measured here: the 200th post-re-cut evaluation was at 2026-08-20 23:30:02: LONG 9/117 = 7.69 %, SHORT 3/83 = 3.61 %, ratio 2.13×. **Both wires had tripped by then: LONG was above 5 %, and the side ratio was above 2×.** The full post-re-cut count now stands at 5.67× (§3b). The 2026-09-01 report's "1.03×" pools refusals from before and after the re-cut against pre-gate denominators, so it is not a test of the live floors.
- **Canon drift:** `OPEN-ITEMS-SOL.md` still states the 08-10 floors and pre-registration only. Config's own calibration comment gives SHORT "either 2.57 %", while the report and the pre-registration give 2.67 %. The re-registration says "clause A ~1.2 %", while the original said ~0.5 %.
- **No existing text discusses regime dependence of the book or the gate.** The nearest is report 2026-09-01-1926 §4b, which covers the *advisor* flipping sign with the daily regime.
- **Why the gate's refusals are invisible to a regime study:** `book_blocked` rows store no `trend_1d`. Every regime split that uses the row's own label silently drops all 45 refusals. §3b attaches their regime from the nearest row.


---

## 3. What the current thresholds would do in a bear market

### 3a. The live gate replayed over every stored book, split by regime

The gate logic was re-implemented from `book_gate.py` text with the live constants read from `config.py` text: `WALL_PCTL 90`, `WALL_DIST_PCT 0.20`, `MIN_SUPPORTING 1`, floors LONG 0.4238 / SHORT 0.3489. **Verified against the live gate's own stored columns:** the replay reproduces the stored `book_gate_lean` on 1,087 of 1,087 admitted rows. Applying the era-correct floors (the pre-re-cut 0.4323 / 0.4129 before 2026-08-14 18:28) to the stored facts reproduces the stored refusal decision on **1,132 of 1,132** evaluated rows, all 45 `book_blocked` included.

Daily axis, all books:

| regime | side | n | refuse A % | refuse B % | refuse any % |
|---|---|---|---|---|---|
| bear | LONG | 664 | 0.15 | 1.05 | 1.2 |
| bear | SHORT | 649 | 2.0 | 0.0 | 2.0 |
| bull | LONG | 686 | 0.0 | 0.15 | 0.15 |
| bull | SHORT | 845 | 0.0 | 0.12 | 0.12 |
| neutral | LONG | 734 | 0.54 | 0.82 | 1.23 |
| neutral | SHORT | 941 | 0.32 | 0.0 | 0.32 |

Daily axis, design window only (like for like — same collection, same pre-gate funnel):

| regime | side | n | refuse A % | refuse B % | refuse any % |
|---|---|---|---|---|---|
| bear | LONG | 664 | 0.15 | 1.05 | 1.2 |
| bear | SHORT | 649 | 2.0 | 0.0 | 2.0 |
| bull | LONG | 277 | 0.0 | 0.36 | 0.36 |
| bull | SHORT | 388 | 0.0 | 0.26 | 0.26 |
| neutral | LONG | 597 | 0.67 | 1.01 | 1.51 |
| neutral | SHORT | 858 | 0.35 | 0.0 | 0.35 |

4h axis, all books:

| regime | side | n | refuse A % | refuse B % | refuse any % |
|---|---|---|---|---|---|
| bear | LONG | 711 | 0.0 | 0.42 | 0.42 |
| bear | SHORT | 643 | 2.18 | 0.0 | 2.18 |
| bull | LONG | 506 | 0.59 | 0.4 | 0.99 |
| bull | SHORT | 964 | 0.21 | 0.0 | 0.21 |
| neutral | LONG | 854 | 0.23 | 1.05 | 1.17 |
| neutral | SHORT | 811 | 0.0 | 0.12 | 0.12 |

Side ratio, any refusal, daily axis: **BEAR 1.20 % L / 2.00 % S = 1.66×** · BULL 0.15 % / 0.12 % = 1.23× · NEUTRAL 1.23 % / 0.32 % = 3.85×. On the 4h axis the ratios run 4.8–9.5× in every regime, but the absolute rates are all ≤ 2.2 %. The ratio of two sub-1 % rates is noise; it is recorded, not read.

**The population correction.** The design-window books are *scored signals before the gate existed*. The 08-14 re-cut established that the population the gate actually evaluates has a fatter tail. On the same regimes (BULL + NEUTRAL, live floors) the gate era refuses **LONG 1.14 % → 3.53 % (×3.1)** and **SHORT 0.32 % → 0.92 % (×2.9)**. Per clause:

| side | clause A design → gate era | clause B design → gate era | bear-daily design rate | **predicted gate-era bear** |
|---|---|---|---|---|
| LONG | 0.46 % → 1.41 % (×3.1) | 0.80 % → 2.12 % (×2.6) | A 0.15 %, B 1.05 % | **A ≈ 0.5 % + B ≈ 2.8 % ≈ 3.3 %** |
| SHORT | 0.24 % → 0.92 % (×3.8) | 0.08 % → 0.00 % | A 2.00 %, B 0.00 % | **A ≈ 7.6 %** |

### 3b. The pre-registered alarm — above 5 % on either side, or a side ratio above 2×

| regime | status | LONG | SHORT | ratio | alarm |
|---|---|---|---|---|---|
| bear daily, pre-gate books | **measured** (n 664 / 649) | 1.20 % | 2.00 % | 1.66× | not breached |
| bear daily, gate-evaluated population | 🔴 **predicted** (era-adjusted) | ≈ 3.3 % | ≈ 7.6 % | ≈ 2.3× against SHORT | **would breach on SHORT (> 5 %) and on ratio** |
| bull/neutral, gate as it ran since the 08-14 re-cut | **measured** (n 481 / 481) | **3.53 %** | **0.62 %** | **5.67×** against LONG (p = 0.0026) | 🔴 **BREACHED — ratio wire** |
| bull/neutral, gate 08-11 → 08-14 (old floors) | measured (n 88 / 82) | 6.82 % | 23.17 % | 3.40× | breached, and led to the re-cut |

**The mechanism predicts a side flip.** Today the gate leans on LONGS: 11 of the 17 LONG refusals are clause B, from SOL's bid-heaviness under a bull tape. In a bear daily the lean floors go quiet, clause A starts biting SHORTS through the bigger bid walls below price, and the imbalance runs the other way. The alarm that would sound would be about shorts, not longs.

### 3c. Does liquidity sit below price in a falling market?

**Yes — as wall size, not as imbalance, and only on the side that faces it.**

- **Imbalance (bid share, side-free, one book per hour):** bear daily 0.5034, bull 0.5101, neutral 0.5088 — essentially flat, and if anything slightly *less* bid-heavy under a bear daily. On the 4h axis a bear 4h is slightly *more* bid-heavy (0.5119 vs 0.5064), which is where the significant SHORT-lean result in §1b comes from.
- **Walls:** the nearest bid wall below price reaches the top decile for a short 29.1 % of hours under a bear daily, against 1.7 % under a bull. Clause A therefore fires on **13 of 649 bear-daily SHORT books against 0 of 388 bull-daily** in the design window (Fisher p = 0.0028). With one book per hour that becomes 4 / 182 vs 0 / 116 (p = 0.16) — the repeats carry the significance of the *refusal* count, while the wall-size effect behind it is robust (p = 5×10⁻¹¹).
- **Longs:** no effect. The ask wall above a LONG is the same size in every regime.

In gate terms, the bid walls under a SHORT are **opposing**: they absorb the move down. The brief's phrasing, that a short "would more often face a supporting book", has the sign reversed under the gate's own definitions. The data shows shorts facing **more opposing structure** in a falling market.

### 3d. Independent cross-check of the replay

A second agent re-implemented the gate by hand from the text of `book_gate.py` and `config.py`. It imported nothing and read the DB only through `mode=ro` SELECTs. It then replayed every stored book on its own, and its numbers were compared with this pass cell by cell.

- **Against the live gate's own stored facts:** it matches the stored lean, opposing multiple, percentile, distance, supporting count, decision and clause **bit-exactly on 1,076 of 1,076** replayable rows, with 0 disagreements.
- **Bear-daily cells: identical.** LONG 8 refusals (1 A, 7 B) · SHORT 13 refusals (13 A, 0 B) · lean p2 0.4340 / 0.4211 against this pass's 0.4340 / 0.4212.
- **Other cells:** it differs by up to 7 books in six cells and by one refusal in two. The cause is that this pass also reads a book from `advisor_book_json` when `orderbook_json` has been overwritten at fill by the Bybit depth-20 dict. That adds **16 executed-path rows**, carrying 1 replayed refusal(s), all in BULL/NEUTRAL cells. No conclusion depends on those rows.
- **Its note, independently confirmed:** none of the gate's 45 real refusals can be replayed from a stored book. Those rows carry no `orderbook_json`, no `advisor_book_json` and no trend label; only the six `book_gate_*` facts survive. That is why §3b's measured row for the gate as it ran uses the stored facts, not a replay.


---

## 4. The honest frame

### 4a. What this can and cannot establish

- **It can establish** the regime dependence of the *book*, from 1,313 SOL bear-daily books stored in the gate's exact input shape. The lean tail does not depend on the daily. The bid-wall size under a short does, strongly.
- **It can establish** what the *live constants* would do on those books: inside the alarm, at 1.20 % / 2.00 %.
- **It cannot measure** what the gate would do on the population it actually evaluates in a bear market, because that population has never existed. The ≈ 7.6 % SHORT figure is a **prediction**: bear-daily book shape from June–August, multiplied by an era factor from bull/neutral days. Both factors are real. Their product has never been observed.
- **It cannot rule out** a bear market unlike June–August 2026. Those bear dailies were a SOL at $66–78; the gate's walls are scaled by `mult` (× the average level), not by price, which limits but does not remove that concern.

### 4b. If the thresholds breach in a bear market — what the pre-registration would require

The pre-registration reads: *a realised rate above 5 % on either side, or a side ratio above 2×, is grounds to revisit; re-cut the ruler per side and say so.* **This pass does not apply a re-cut and does not propose one.** For the record, a re-cut would require:

1. **At least N evaluations per side under a bear daily**, from the gate's own evaluated population.
2. **Both cuts shown side by side.** The lean p2 per side over that bear-era population, and the clause-A ruler (`_NEAR_MULT_BREAKS`, nearest opposing wall per side) re-cut from the same quantity over the same rows.
3. **The regime-pooled alternative shown beside it**, with the replayed rate of each.

### 4c. 🔴 WATCH ITEM for the canon

> **SOL BOOK GATE — FIRST BEAR DAILY.** When `trades.trend_1d` first reads `BEAR` on a row the gate evaluates, count the next **N = 100 gate evaluations per side**, spanning **≥ 5 distinct days**. Compare the refusal rate per side and per clause with the re-registered expectation (LONG 2.01 %, SHORT 2.14 %, side ratio 1.07×) and with this pass's prediction (SHORT ≈ 7.6 % via clause A, LONG ≈ 3.3 %). Breach = above 5 % on a side or a side ratio above 2×, per the gate's own wording.
>
> **Why N = 100:** at the pre-registered 2.1 % the chance of reading above 5 % by luck is **1.9 %**. A true 10 % is detected **94 %** of the time, a true 7 % **71 %** of the time. At N = 50 the false alarm rises to 8.8 %; at N = 200 the detection of 7 % only reaches 83 %. At the current 18 evaluations per side per day, N = 100 takes **about 6 days**. The ≥ 5-days condition guards against one day's book dominating, as 2026-08-12 did for the old SHORT breach.

Open now, independent of the bear question: **the side-ratio wire is breached in the current tape** (§3b row 3), and the re-cut's review point has passed.

---

## Verification

- **Pre-flight:** `openitems_guard` EXIT=0 before anything else (titan-bot HEAD cd0f175), and EXIT=0 again at the end. **Titan untouched:** its database was not opened and its tree is clean in `git status`. The book gate armed on 2026-09-10 14:36:20 was left as is.
- **DB read-only:** every connection was `file:…/trades.db?mode=ro`, SELECTs only. This includes both agents, which were bound by the same rule and report the same conduct.
- **Working directory:** the session scratchpad, never inside SOL's tree.
- **Config and gate code read as text only:** `config.py` and `book_gate.py` were parsed with regex and copied by hand. Nothing from SOL was imported.
- **No network use at all in this pass.** Every number comes from stored books.
- **No writes, no orders, no restart.** MainPID 1084680 before and after, `NRestarts = 0` before and after, active since 2026-09-10 23:04:47.
- **File hashes: 35 of 36 byte-identical** against the 05:14:46 baseline. The one that changed is `trades.db`, written by the live bot itself (row 25648, a `15m_confirm`, 05:15:04). `optimizer/tg_offset.txt`, outside the hashed set, was written by the optimizer listener.
- **Book flat:** 0 open positions, 0 `active_positions`.
- **`FLAT_ADX_GATE_DRYRUN = True`** at `config.py:407`, unchanged.
- **Telegram:** the sender was imported from `/root/titan-bot` with bytecode writing disabled.
