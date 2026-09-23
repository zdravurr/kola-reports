# mercury-sol-50-bought-under-a-level-arm-behind-it

_2026-09-23 17:45 UTC_

---

# DID #50 BUY UNDER A BIG LEVEL, AND DOES THE ARM SIT BEHIND IT? — **YES ON #50. ACROSS THE BOOK THE RECORD CANNOT SHOW THAT AVOIDING IT WOULD HAVE HELPED.**

**2026-09-23 17:45 UTC · Mercury-SOL · READ-ONLY · Titan untouched**

`openitems_guard` → **exit 0** (titan-bot HEAD `f53d048`), run first.

> 🔴 **WHAT IS NEW HERE.** On 2026-08-14 the pass measured entry placement inside the **24-hour** range (`pos24`).
> By construction longs enter at the top (median 0.905), and it did **not** decide outcome. That is **not re-run
> here.** This pass measures two things never measured before:
> * a **multi-day confirmed swing high or low**
> * **the 0.75R trail-arm's position relative to it**

---

## 🔴 THE ANSWER FIRST

**#50: yes, on both counts, confirmed on Bybit real candles.**
* It bought **1.91% (1.86 ATR) under the 120.07 swing high** of 2026-09-21 21:00.
* Its 0.75R arm sat at **120.0925, 2 cents above that high**. It could only become protected by breaking the
  resistance it entered beneath.
* It never did: the peak was a lower high at **119.72 (MFE 0.63R)**, and the stop filled at 114.75.

**Across the book: it does not separate.**
* **44 closed positions.** "Arm behind the nearest level" (Q2) and "entry within 1.015 ATR of a level" (Q1) fail
  Bonferroni in every cell. The smallest p is 0.111 against α = 0.00625, and most cells are under n=8.
* **The direction is consistent on LONGs:** "behind" is worse in all 4 chronological halves and all 3 regimes.
  But those splits overlap and every one is tiny, and the confound with side is strong: 70% of shorts are
  "behind", and shorts lost.
* 🔴 **A rule would refuse material winners.** The Q2 rule refuses **#29 +1.355R, #38 +4.031R, #40 +2.549R and
  #41 +1.633R: four live longs, +9.57R.** Live longs "behind" still made **+7.27R net**.
* **#48 (+5.431R) and #49 (+1.856R) were NOT behind a level.** Their arms sat 0.37 and 0.51 ATR *below* the
  nearest swing high.

**Plainly: #50 met a level and lost. The record cannot show that avoiding levels would have helped. On live longs,
refusing them would have cost 9.57R of winners to avoid 2.30R of losers.**

**One structural fact that frames everything:** the stop is 2.5 × ATR(1h), so the 0.75R arm always sits
**1.875 ATR** from entry. "Arm behind the level" is therefore exactly "a confirmed swing within 1.875 ATR". It is
the **common case (27 of 44)**, not an exception.

---

## 0. DEFINITIONS — fixed before any number was computed

* **Candles:** Bybit SOLUSDT linear **real** OHLC, 1h / 4h / 1d, 2026-05-01 → 2026-09-23 17:00. That is 3,498 /
  875 / 146 bars, complete with no gaps, fetched by public GET on a fresh isolated Tor circuit per request, 0 failed
  attempts. Heikin A. is not used.
* **Swing high/low, no look-ahead:** a bar whose high (low) is strictly above (below) the **k bars on each side**:
  * 1h: k = 12
  * 4h: k = 3
  * 1d: k = 2

  A swing is usable at an entry **only if it was confirmed before the fill**, i.e. its bar open + (k+1) bars ≤
  the fill time. The 1h fractal is confirmed 13h after its bar.
* **Q1 "near a level":** the distance from the fill to the nearest confirmed **1h** swing high above a LONG (swing
  low below a SHORT) within the prior **14 days**, in the position's own entry ATR(1h) (`virtual_positions.atr`).
  **Split at the pooled median of that distance, 1.015 ATR**, computed from distances only.
* **Q2 "arm behind the level":** the arm is `fill ± 0.75 × |fill − original_sl|`. It is "behind" if the arm is
  at or beyond that level, i.e. the position must break the level to arm.
* **Robustness definition (def2):** the union of 1h + 4h + 1d swings, 30-day lookback.
* **Outcomes:**
  * R = `net_pnl / initial_risk_usdt`
  * win = R > 0
  * MFE = `water_mark` excursion / stop distance
  * "armed" = MFE ≥ 0.75R
  * "printed +0.25R" = MFE ≥ 0.25R
* **Bonferroni:** m = 2 questions × 2 books × 2 sides = **8**, **α = 0.00625**. Exact permutation on mean R
  (random 50,000 when the split count exceeds 60,000), two-sided Fisher on wins. **Cells under n=8 are not ranked.**

---

## 1. #50 ON REAL CANDLES

**a) Every confirmed swing high above 117.82 at the fill (2026-09-22 18:00:43)**

| timeframe | 3 days | 7 days | 14 days | 30 days |
|---|---|---|---|---|
| **1h** (k=12) | **120.07 @ 09-21 21:00** | same, only one | same | same |
| **4h** (k=3) | **120.07 @ 09-21 20:00 bar** | same | same | same |
| **1d** (k=2) | none | none | none | none |

**120.07 is +1.91% above the fill, or 1.86 ATR(1h)** with ATR 1.2105. It is the only confirmed swing high above
entry on any timeframe within 30 days. There is no daily swing high above, because SOL had been making higher
daily highs (+61% rally), so 120.07 is an intraday level.

**b) The chart reading, checked against real candles: ✅ confirmed**

| claim (Heikin A. 1h) | real candles |
|---|---|
| swing high ~120.07 at 09-21 21:00 | ✅ **120.07 at 09-21 21:00** (1h); it is also the high of 09-20 → 09-23 |
| range ~115.5–120, 09-21 14:00 → 09-23 ~08:00 | ✅ **115.48 – 120.07** |
| entry 1.9% below that high | ✅ **1.91%** |
| lower high ~119.72 at 09-23 04:00 | ✅ **119.72 at 09-23 04:00**, which is also the post-entry peak |
| MFE ≈ +0.63R | ✅ **0.627R** on candles. The bot's own `water_mark` is 119.67 = 0.611R, as sampled by its 10s poller |
| breakdown 09-23 14:00 | ✅ the 14:00 bar ran 116.75 → **low 112.85**, close 115.08. It was the first bar through the stop (114.79), and the fill was 114.75 |

**c) 🔴 The arm against the level**

| | price | from entry |
|---|---|---|
| fill | 117.82 | — |
| 1R | 3.03 (= 2.5 × ATR) | |
| **0.75R arm** | **120.0925** | +1.93%, 1.875 ATR |
| **nearest swing high** | **120.07** | +1.91%, 1.86 ATR |
| **arm − level** | **+0.0225** | **+0.019 ATR, 0.02%** |

**The arm sat 2 cents beyond the swing high. To become protected, #50 had to trade through the exact high it bought
beneath.** It peaked 0.35 below it, at 119.72.

**d) The entry record** (`trades.id` 28972)
* **Signal:** `open_long`, combo `1H:Bearish Confirmation | 15M:HyperWave Signal Up | 5M:Within Bullish OB`.
* **Score and matrix:** confluence **4.51**. Matrix: MOMENTUM +1.75 L, EXECUTION +1.75 L, **LIQUIDITY 1.75
  SHORT** (inter-conflict), TREND 0.
* **Tiers and regime:** 1d / 4h / 1h / 15m **all bull**. ADX(1h) 23.4. Regime `FLAT`.
* **Advisor:** `claude-haiku-4-5`, **execute, 0.72**, verbatim:
  > *"1d/4h BULL regime + fresh 15m/5m LONG confluence + expanding EMA-gaps 1h/15m + **no opposing ask walls above
  > entry** justify execution despite stale 1h SHORT and low ADX(15m)."*
* 🔴 **That reason contradicts its own prompt.** The prompt listed five ask walls above entry:

  | ask wall | percentile | size | note |
  |---|---|---|---|
  | **118.25** | **p88** | **×17.1** | +0.35% |
  | 118.75 | p42 | ×6.9 | |
  | **119.75** | p41 | ×6.7 | **0.32 below the 120.07 high** |
  | 126.25 | p38 | ×6.3 | |
  | 117.75 | p25 | ×5.2 | |
* **Did it mention the level?** **No.** The prompt contains **no multi-day high, no swing level and no "120"**
  anywhere (0 matches). The bot does not give the advisor this information at all.
* **Did the book gate see a wall near 120?** It saw the **118.25 ×17.1** wall at 0.348% and **passed**: clause
  empty, because the gate's distance rule is 0.2%. It recorded lean 0.447 and 3 supporting walls. The only wall near
  120 was 119.75 at ×6.7 (p41), outside the gate's reach and below its percentile bar. **Nothing in the bot looks at
  a multi-day swing high.**

---

## 2. ACROSS THE BOOK

**a) Every closed position** (22 paper #7–28, 22 live #29–50). `d` is the distance to the nearest confirmed 1h
swing (14 days) in ATR. `gap` is arm − level in ATR; + means the arm is **beyond** the level.

| # | book | side | R | MFE | armed | +.25R | exit | daily | level | d | gap | **Q2** | def2 d / Q2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 | P | L | +2.089 | 3.00 | Y | Y | exit_signal | neut | 75.68 | 6.99 | −5.12 | · | 6.99 / · |
| 8 | P | L | −0.739 | 0.02 | · | · | exit_signal | — | 74.44 | 3.46 | −1.58 | · | 3.46 / · |
| 9 | P | L | −0.264 | 0.31 | · | Y | exit_signal | neut | 74.44 | 1.75 | +0.13 | **B** | 1.75 / B |
| 10 | P | S | −1.066 | 0.05 | · | · | sl | neut | 72.28 | 0.43 | +1.44 | **B** | 0.43 / B |
| 11 | P | S | +1.133 | 1.71 | Y | Y | exit_signal | neut | 67.86 | 4.70 | −2.82 | · | 4.70 / · |
| 12 | P | L | −1.049 | 0.48 | · | Y | sl | bear | 69.69 | 0.23 | +1.65 | **B** | 0.23 / B |
| 13 | P | S | +1.337 | 2.36 | Y | Y | trail | bear | 68.05 | 0.86 | +1.01 | **B** | 0.86 / B |
| 14 | P | S | −1.032 | 0.09 | · | · | sl | bear | 64.66 | 0.19 | +1.69 | **B** | 0.19 / B |
| 15 | P | S | +0.140 | 1.18 | Y | Y | trail | neut | 71.86 | 8.60 | −6.72 | · | 8.06 / · |
| 16 | P | L | −1.146 | 0.16 | · | · | sl | neut | 82.40 | 5.60 | −3.73 | · | 5.60 / · |
| 17 | P | S | +0.004 | 1.18 | Y | Y | sl | neut | 75.59 | 0.53 | +1.34 | **B** | 0.53 / B |
| 18 | P | L | −1.074 | 0.89 | Y | Y | sl | neut | 78.19 | 1.07 | +0.81 | **B** | 1.07 / B |
| 19 | P | S | +0.463 | 0.97 | Y | Y | exit_signal | neut | 77.03 | 0.02 | +1.86 | **B** | 0.02 / B |
| 20 | P | S | −1.124 | 0.16 | · | · | sl | neut | none | — | — | · | 2.45 / · |
| 21 | P | L | +0.285 | 1.44 | Y | Y | trail | bear | 78.19 | 5.91 | −4.05 | · | 1.13 / B |
| 22 | P | L | −1.064 | 0.29 | · | Y | sl | bull | 78.83 | 0.70 | +1.17 | **B** | 0.70 / B |
| 23 | P | S | −0.577 | 0.53 | · | Y | exit_signal | bear | none | — | — | · | 2.37 / · |
| 24 | P | S | −1.050 | 0.25 | · | Y | sl | bear | 72.31 | 0.55 | +1.32 | **B** | 0.55 / B |
| 25 | P | S | +1.257 | 2.51 | Y | Y | trail | bear | 72.31 | 0.55 | +1.33 | **B** | 0.55 / B |
| 26 | P | L | −1.085 | 0.72 | · | Y | sl | bear | 74.50 | 2.59 | −0.71 | · | 2.59 / · |
| 27 | P | S | −0.660 | 0.59 | · | Y | sl | bear | 72.51 | 0.05 | +1.82 | **B** | 0.05 / B |
| 28 | P | S | −0.153 | 0.49 | · | Y | exit_signal | bear | 72.68 | 0.23 | +1.64 | **B** | 0.23 / B |
| 29 | L | L | **+1.355** | 1.82 | Y | Y | exchange | neut | 74.81 | 0.03 | +1.85 | **B** | 0.03 / B |
| 30 | L | L | +0.762 | 1.67 | Y | Y | trail | neut | 77.08 | 2.23 | −0.37 | · | 0.34 / B |
| 31 | L | L | −1.155 | 0.13 | · | · | sl | bull | 77.49 | 1.26 | +0.61 | **B** | 0.28 / B |
| 32 | L | S | −0.180 | 0.51 | · | Y | exit_signal | bull | 76.15 | 0.07 | +1.81 | **B** | 0.07 / B |
| 33 | L | L | −0.049 | 0.61 | · | Y | exit_signal | bull | 76.80 | 0.70 | +1.18 | **B** | 0.70 / B |
| 34 | L | S | −0.643 | 0.12 | · | · | sl | bull | 74.56 | 1.49 | +0.38 | **B** | 1.49 / B |
| 35 | L | S | −0.701 | 0.18 | · | · | sl | neut | 75.05 | 0.34 | +1.53 | **B** | 0.34 / B |
| 36 | L | S | −0.757 | 0.28 | · | Y | exchange | neut | 75.05 | 0.50 | +1.36 | **B** | 0.50 / B |
| 37 | L | S | −1.226 | 0.23 | · | · | sl | neut | 73.20 | 4.24 | −2.36 | · | 3.56 / · |
| 38 | L | L | **+4.031** | 4.99 | Y | Y | trail | bull | 77.37 | 0.78 | +1.09 | **B** | 0.05 / B |
| 39 | L | L | +1.604 | 2.54 | Y | Y | trail | bull | none | — | — | · | none / · |
| 40 | L | L | **+2.549** | 3.42 | Y | Y | trail | bull | 93.40 | 0.96 | +0.91 | **B** | 0.96 / B |
| 41 | L | L | **+1.633** | 2.57 | Y | Y | trail | bull | 102.74 | 1.28 | +0.59 | **B** | 1.28 / B |
| 42 | L | S | −1.083 | 0.73 | · | Y | sl | neut | 94.84 | 4.20 | −2.33 | · | 4.20 / · |
| 43 | L | L | +1.723 | 2.66 | Y | Y | trail | bull | 105.01 | 3.16 | −1.29 | · | 3.16 / · |
| 44 | L | S | −1.110 | 0.64 | · | Y | sl | neut | 98.30 | 1.30 | +0.57 | **B** | 1.30 / B |
| 45 | L | S | −1.133 | 0.24 | · | · | sl | neut | 99.35 | 0.32 | +1.56 | **B** | 0.32 / B |
| 46 | L | S | +0.368 | 1.35 | Y | Y | trail | neut | 100.07 | 0.52 | +1.36 | **B** | 0.33 / B |
| 47 | L | S | −1.069 | 0.40 | · | Y | sl | neut | none | — | — | · | 2.01 / · |
| 48 | L | L | **+5.431** | 6.41 | Y | Y | trail | neut | 102.32 | 2.25 | **−0.37** | · | 2.25 / · |
| 49 | L | L | +1.856 | 2.83 | Y | Y | trail | bull | 114.31 | 2.38 | **−0.51** | · | 2.38 / · |
| **50** | L | L | **−1.092** | 0.61 | · | Y | sl | bull | **120.07** | **1.86** | **+0.02** | **B** | 1.86 / B |

**b) Cells.** Q1 is split at 1.015 ATR (the pooled median of 40 finite distances; 4 positions had no level within
14 days and count as "far"). Q2 is binary. Cells under n=8 are not ranked.

| split | book · side | YES: n · wins · ΣR · mean | NO: n · wins · ΣR · mean | Δ mean | perm p | Fisher p |
|---|---|---|---|---|---|---|
| **Q1 near** | LIVE LONG | 4 · 3 · +7.886 · +1.971 | 8 · 6 · +10.762 · +1.345 | +0.626 | 0.606 | 1.0 — *not ranked* |
| | LIVE SHORT | 5 · 1 · −2.402 · −0.480 | 5 · 0 · −5.131 · −1.026 | +0.546 | **0.111** | 1.0 — *not ranked* |
| | PAPER LONG | 2 · 0 · −2.112 · −1.056 | 7 · 2 · −1.934 · −0.276 | −0.780 | 0.500 | 1.0 — *not ranked* |
| | PAPER SHORT | 9 · 4 · −0.900 · −0.100 | 4 · 2 · −0.428 · −0.107 | +0.007 | 0.993 | 1.0 — *not ranked* |
| | BOTH ALL | 20 · 8 · +2.471 · +0.124 | 24 · 10 · +3.270 · +0.136 | −0.013 | 0.979 | 1.0 |
| **Q2 arm behind** | LIVE LONG | 7 · 4 · +7.272 · +1.039 | 5 · 5 · +11.376 · +2.275 | −1.236 | 0.298 | 0.205 — *not ranked* |
| | LIVE SHORT | 7 · 1 · −4.155 · −0.594 | 3 · 0 · −3.378 · −1.126 | +0.532 | 0.142 | 1.0 — *not ranked* |
| | PAPER LONG | 4 · 0 · −3.450 · −0.863 | 5 · 2 · −0.596 · −0.119 | −0.743 | 0.405 | 0.444 — *not ranked* |
| | PAPER SHORT | 9 · 4 · −0.900 · −0.100 | 4 · 2 · −0.428 · −0.107 | +0.007 | 0.993 | 1.0 — *not ranked* |
| | BOTH LONG | 11 · 4 · +3.822 · +0.347 | 10 · 7 · +10.780 · +1.078 | −0.731 | 0.387 | 0.198 |
| | BOTH ALL | 27 · 9 · −1.233 · −0.046 | 17 · 9 · +6.974 · +0.410 | −0.456 | 0.340 | 0.225 |

Median MFE for BOTH ALL: behind 0.59R vs not 1.18R. "Printed +0.25R" is 21/27 vs 13/17, so behind-level trades
**did** go green about as often as the rest; they just went less far.

**c) 🔴 THE FIVE CONTROLS**

| control | result |
|---|---|
| **(a) Bonferroni** (α = 0.00625) | ❌ **FAIL everywhere.** Smallest p = **0.111** (Q1, LIVE SHORT, n=5/5). Q2 BOTH LONG p = 0.387. |
| **(b) Chronological halves** | ⚠️ **The direction holds but n is tiny.** Q2 LONG, "behind worse" in all 4 halves: LIVE H1 −0.138 (n 4/2), LIVE H2 −1.973 (3/3), PAPER H1 −1.332 (2/2), PAPER H2 −0.420 (2/3). All sides: it **flips** in PAPER H2 (+0.300). |
| **(c) Regime split, both legs populated** | ⚠️ LONG, behind worse under bull (−1.034, n 7/3), neutral (−1.779, 3/4) and bear (−0.648, 1/2). All sides: it **flips** under bear (+0.266, 7/3). Legs of 1–4 trades. |
| **(d) Paper as the independent sample** | ⚠️ **Same sign, not significant.** Paper LONG behind 0/4 wins (−0.863) vs not 2/5 (−0.119), p = 0.405. On shorts the effect is **absent** (−0.100 vs −0.107). |
| **(e) Confound: side / era / rally** | ❌ **Strong.** "Behind" is 70% of SHORTS (mean R −0.385) vs 52% of LONGS (+0.695), and 75% of bull-daily entries vs 56% of the rest. The all-sides result is largely **side**; the LONG-only result is too small to separate from the rally era. |

**Robustness (def2, 1h+4h+1d, 30 days):** the same direction. BOTH LONG behind +0.375 vs +1.217; LIVE LONG +1.004 vs
+2.653. The same verdict.

**d) 🔴 Every winner a rule would refuse, named**

A **Q2 rule ("refuse when the arm is behind the level")** refuses these winners:

| # | book | side | R | level | d (ATR) | arm beyond by |
|---|---|---|---|---|---|---|
| **29** | LIVE | LONG | **+1.355** | 74.81 | 0.03 | 1.85 ATR |
| **38** | LIVE | LONG | **+4.031** | 77.37 | 0.78 | 1.09 ATR |
| **40** | LIVE | LONG | **+2.549** | 93.40 | 0.96 | 0.91 ATR |
| **41** | LIVE | LONG | **+1.633** | 102.74 | 1.28 | 0.59 ATR |
| 46 | LIVE | SHORT | +0.368 | 100.07 | 0.52 | 1.36 ATR |
| 13, 17, 19, 25 | PAPER | SHORT | +1.337, +0.004, +0.463, +1.257 | | | |

🔴 **That is four live longs worth +9.57R, including the book's second-best trade (#38 +4.031R) and #40 (+2.549R).**
The losers it would have avoided among live longs are #31 −1.155, #33 −0.049 and **#50 −1.092** (−2.30R). Live
longs "behind a level" made **+7.27R net**.
A **Q1 rule (< 1.015 ATR)** refuses #29, #38, #40 and #46, plus paper #13, #17, #19 and #25.

**Where the three named winners were:**

| # | R | nearest level | d (ATR) | arm vs level | behind? |
|---|---|---|---|---|---|
| **48** | +5.431 | 102.32 (09-13 01:00) | 2.25 | arm 102.00, **0.37 ATR below** | **No.** A rule would not refuse it |
| **40** | +2.549 | 93.40 (08-21 08:00) | 0.96 | arm 94.51, **0.91 ATR beyond** | **Yes. Refused** |
| **49** | +1.856 | 114.31 (09-18 19:00) | 2.38 | arm 113.80, **0.51 ATR below** | **No** |
| **38** | +4.031 | 77.37 (08-12 12:00) | 0.78 | 1.09 ATR beyond | **Yes. Refused** |

#40 and #38 broke straight through their levels and trailed out at +2.5R and +4.0R. **#50 and #40 had the same
geometry, and one of them made +2.549R.**

---

## 3. VERDICT

**🔴 It does not separate.** No cell reaches α; the smallest p is 0.111, and most cells have fewer than 8 trades.
LONG-side "behind the level" points the same way in every split. But each split holds 1–7 trades, the splits
overlap, and the all-sides version is mostly the long/short difference. **A rule built on it would refuse four live
winners worth +9.57R, including #38 and #40, to avoid 2.30R of losses.**

**#50 met a level and lost. The record cannot show that avoiding levels would have helped.** Nothing is proposed.

**One real, separate finding from #50's record:**
* The advisor justified the entry with *"no opposing ask walls above entry"* while its own prompt listed five,
  including a p88 ×17.1 wall 0.35% above.
* The prompt carries **no multi-day swing level at all**. The bot's only view of "resistance" is the live order book.

That is a fact about what the advisor sees and says. It is not evidence that a level rule would work.

**🔴 What a live TradingView on the server would add**, beyond Bybit candles on the server and TradingView cloud
alerts:
* **Levels: nothing.** Every number in this report (swing highs, ranges, MFE, the breakdown bar) came from Bybit
  **real** OHLC fetched on the server in seconds. TradingView's data for SOLUSDT is the same exchange feed. The
  operator's **Heikin A.** chart shows synthetic candles: its highs are averaged, not traded prices, so it is a
  worse source for levels, not a better one.
* **Indicator signals: nothing new.** Anything a Pine script computes can already reach the bot as a **cloud
  alert** webhook. That is how every `WEBHOOK_IN` signal arrives today ("Equal L.", "Within Bullish OB",
  "HyperWave OS Signal Up").
* **What it would add:** a rendered, interactive chart to look at, and indicators whose logic is closed-source and
  cannot be alerted on. It would **cost** a headless browser, a logged-in session on a 1 GB box, and a scraping
  surface.
* **If levels are ever wanted,** the path is to compute them from Bybit candles on the server, as done here, and
  put them in the advisor prompt. That is a separate decision, and this data does not support it yet.

---

## READ-ONLY CONFIRMATION

| | |
|---|---|
| `openitems_guard` | EXIT 0 before and after |
| SOL DB | `file:…/trades.db?mode=ro` + `PRAGMA query_only=1`, **asserted = 1** on every connection. **No writes.** |
| SOL config | not imported. sha256 `87fcc0ab…` unchanged |
| venue | **public GET only** (`/v5/market/kline`), a fresh isolated Tor circuit per request, 0 failed attempts. **No private calls, no orders.** |
| `mercury-sol.service` | PID 222221, `NRestarts=0`, active since 16:07:32. **Identical before and after** |
| `titan.service` | PID 4007821, `NRestarts=0`, active since 2026-09-21 19:03:51. **Identical before and after** |
| **Titan** | **UNTOUCHED.** Only `tools/openitems_guard.py` (read-only) was run |
| changed | **nothing.** No diff, no flag, no restart, no proposal |
