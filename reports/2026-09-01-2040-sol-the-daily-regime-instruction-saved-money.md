# Mercury-SOL — what the daily-regime instruction has COST or SAVED: it SAVED, and the 6.35× "bias against shorts" was exposure, not bias

**2026-09-01 20:40 UTC · READ-ONLY MEASUREMENT · nothing was changed**
**Bonferroni declared: α = 0.05 over 79 cells tested in this report → per-cell threshold p < 0.00063. Every claim below is labelled against that threshold, not against 0.05.**

Subject: Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`), SOL/USDT:USDT on Bybit, LIVE real money.
`openitems_guard` run first → **exit 0**, header and current-state table agree with runtime.
Under measurement: the standing order at `claude_advisor.py:146-151`, and §3a/§3b of `2026-09-01-2016-sol-trend-1d-is-true-and-slow-not-lying.md`.

---

## THE ANSWER, FIRST

**The instruction SAVED money. On both sides. In every scope tested. Nothing it refused was profitable.**

* Replayed under SOL's own live exit contract, honouring `MAX_POSITIONS_PER_SIDE = 1` — **what would actually have happened** — the daily-regime refusals would have returned **SHORT −20.27 R (−$49.19), LONG −8.45 R (−$19.17)** over the full record; in the **live era alone, SHORT −13.90 R (−$31.64), LONG −2.21 R (−$2.28)**.
* The live-era short result is the only cell in this report that **survives Bonferroni**: mean R = **−0.556**, 95% CI **[−0.818, −0.278]**, P(mean ≥ 0) = **0.0001** against a required 0.00063.
* 🔴 **The 6.35× "lean against shorts" I reported at 20:16 was EXPOSURE, not bias.** Conditioned on whether 1d/4h actually *opposed* the proposed side, the pass rates are **SHORT 0.18% vs LONG 0.40% when opposed (Fisher p = 0.43)** and **SHORT 5.12% vs LONG 3.78% when not opposed (p = 0.16)** — no side difference in either leg, and shorts pass *more* when unopposed. Over the full record each side spent about half its consultations in the opposed bucket (SHORT 50.9%, LONG 53.3%). **In the live era that split to SHORT 89.5% vs LONG 25.2%** — SOL's daily uptrend, not the instruction, is what pointed the lean one way.
* 🔴 **The model almost never overrides it: 6 times in 4,093 consultations (0.15%).** Those 6 produced 5 positions: **1 winner, sum −2.672 R.** The two on the SHORT side are **live vpos 32 (−0.180 R) and vpos 34 (−0.643 R) — both lost.** The only direct evidence of what happens when the lean is not followed is uniformly bad.
* 🔴 **The lag hypothesis is REFUTED, and I am not softening it.** Skips on a *stale* label are not the wrong ones. Bucketed by hours since the label last changed, the **worst** bucket is 24–72 h (serial SHORT mean R −0.851), and the **least bad** is >72 h (−0.014). **No bucket is positive.** There is no actionable age split here.
* **What is NOT established:** the win rate is a coin flip (SHORT 45.8% full record, 40.0% live). A per-trade sign test is **not significant** (p = 0.60 / 0.42). The negative expectancy comes entirely from **payoff shape** — mean win +0.555 R against mean loss −1.101 R, a payoff ratio of **0.50**. The refused shorts were not wrong more often than right; they were **wrong bigger**.

---

## 0. THE CONTRACT USED, AND WHERE EACH CONSTANT CAME FROM

Read out of SOL's own files, not assumed. No SOL module was imported.

| term | value | source |
|---|---|---|
| SL distance = 1R | `SL_BUFFER_ATR` 2.5 × ATR(1h,14) | `config.py:62` |
| arm | `TRAIL_ARM_R` 0.75 × 2.5 × ATR = **1.875 ATR = 0.75R** | `config.py:231`, `trail_arm.py:135` |
| breakeven lock | fill × (1 ∓ 0.0020) — **entry −0.20% for SHORT** | `trail_arm.py:151-158` |
| trail | `round(round(1.875×atr,2)/fill×100, 3)` % from the watermark, **post-arm only** | `config.py:104`, `virtual_trader.py:2649,2226-2228` |
| fee | taker **0.100% both legs** (the venue-measured rate; `BYBIT_TAKER_FEE_RATE` 0.00055 is geometry-only and explicitly not the accounting rate) | `config.py:1184-1197` |
| notional | **$100** = `LIVE_FIXED_MARGIN` 20 × `LEVERAGE` 5 | `config.py:39,50` |
| partial at arm | **none** — `PARTIAL_AT_ARM_ENABLED = False` | `config.py:312` |
| time stop | **none** — `MAX_POSITION_DURATION_MINS = 0` | `config.py:582` |
| concurrency | `MAX_POSITIONS_PER_SIDE = 1` | `config.py:1263` |

Order within each 5 m bar, mirroring `virtual_trader._manage_one`: watermark → arm → **SL** → trail. **Adverse extreme evaluated first**, as specified. Candles: **25,591 real Bybit 5 m bars, 2026-06-05 → 2026-09-01 20:30 UTC, zero gaps**, fetched by a standalone `ccxt` object in `/tmp`.

**Two conservatisms, both biased AGAINST the instruction** (i.e. they make the refused trades look *better* than they were, so a negative result is a floor, not a ceiling): the live 10-second poller can arm and be breakeven-stopped inside one bar (`config.py:223`) while a bar-level adverse-first replay cannot; and no `exit_signal` closes are simulated, so every trade is allowed to run to its stop or trail.

---

## 1. THE POPULATION IT ACTUALLY GOVERNS

"Opposed" = the label contradicts the proposed side: `bull` against a SHORT, `bear` against a LONG. Either `trend_1d` **or** `trend_4h` opposing counts, because the instruction names both.

### 1a. Every consultation where 1d/4h opposed the proposed side

| scope | bucket | side | n | execute | skip | pass rate |
|---|---|---|---|---|---|---|
| **FULL RECORD** 2026-06-08 → 09-01 | **OPPOSED** | SHORT | 1,132 | 2 | 1,130 | **0.18%** |
| | **OPPOSED** | LONG | 995 | 4 | 991 | **0.40%** |
| | not opposed | SHORT | 1,093 | 56 | 1,037 | 5.12% |
| | not opposed | LONG | 873 | 33 | 840 | 3.78% |
| **LIVE ERA** ≥ 2026-08-07 22:25 | **OPPOSED** | SHORT | 334 | 2 | 332 | **0.60%** |
| | **OPPOSED** | LONG | 83 | 0 | 83 | **0.00%** |
| | not opposed | SHORT | 39 | 3 | 36 | 7.69% |
| | not opposed | LONG | 247 | 12 | 235 | 4.86% |

### 1b. 🔴 How often is it a lean, and how often a refusal in prose?

Of the **2,127** opposed consultations, **2,121 were skipped and 6 executed — an override rate of 0.28% inside the governed population, 0.15% of all 4,093 consultations.** Of the 2,121 skips, **1,933 (91.1%)** name the daily/4h regime in the stored reason — SHORT 976/1,130 = 86.4%, LONG 957/991 = 96.6%.

**It is a gate in prose.** A rule obeyed 2,121 times out of 2,127 is not a lean in any operational sense. The word "lean" describes the intent; 99.72% describes the behaviour.

### 1c. 🔴 The control — and it overturns my own 20:16 finding

| scope | when 1d/4h OPPOSE | when they do NOT oppose |
|---|---|---|
| full record | SHORT 0.18% vs LONG 0.40% — **Fisher p = 0.4274** | SHORT 5.12% vs LONG 3.78% — **Fisher p = 0.1579** |
| live era | SHORT 0.60% vs LONG 0.00% | SHORT 7.69% vs LONG 4.86% — p = 0.4397 |

**There is no side bias in either leg.** When the regime opposes, both sides are refused at ~0.2–0.4%. When it agrees, both pass at ~4–5%, with **shorts passing slightly more often than longs**. The 6.35× I reported at 20:16 came from comparing shorts-in-`bull` (opposed) against longs-in-`bull` (agreed) — two different buckets. Conditioning correctly, the effect disappears.

**What differs is exposure, and only in the live era:**

| | full record | live era |
|---|---|---|
| SHORT consultations with 1d/4h opposing | 1,132 / 2,225 = **50.9%** | 334 / 373 = **89.5%** |
| LONG consultations with 1d/4h opposing | 995 / 1,868 = **53.3%** | 83 / 330 = **25.2%** |

Over the whole record the two sides are exposed almost identically. SOL's August uptrend is what made the live-era split 89.5 / 25.2. **The instruction is symmetric; the market was not.**

---

## 2. 🔴 THE COUNTERFACTUAL — what did the refused ones do?

Population: every daily-regime skip with both a recorded price and an ATR — **SHORT 961, LONG 948** (of 976 / 957; the rest lack `srv_atr_1h`). Each replayed to its own exit.

### 2a / 2c. Every signal independently

| side | n | win | sum R | mean R | median R | sum $ | median hold |
|---|---|---|---|---|---|---|---|
| **SHORT** | 961 | 48.6% | **−267.74** | −0.279 | −1.039 | **−$753.47** | 10.7 h |
| **LONG** | 948 | 47.3% | **−104.15** | −0.110 | −0.000 | **−$128.95** | 11.8 h |

Exits — SHORT: 494 stop, 382 trail, 82 breakeven, 3 open at data end. LONG: 335 stop, 443 trail, 165 breakeven, 5 open.

**This number answers "was each refused signal individually a bad trade?" and nothing else.** 961 signals over 85 days is ~11/day of heavily overlapping entries; the sample is pseudo-replicated and its n is not an honest n. It is reported because it was asked for, and it must not be read as money.

### 2b. 🔴 Honouring `MAX_POSITIONS_PER_SIDE = 1` — what would ACTUALLY have happened

A signal is taken only if no position is already open on that side.

| scope | side | n | win | sum R | mean R | median R | sum $ |
|---|---|---|---|---|---|---|---|
| **full record** | SHORT | 59 | 45.8% | **−20.27** | −0.344 | −1.061 | **−$49.19** |
| | LONG | 53 | 39.6% | **−8.45** | −0.160 | −0.000 | **−$19.17** |
| | both | 112 | 42.9% | **−28.72** | −0.256 | — | **−$68.36** |
| **live era** | SHORT | 25 | 40.0% | **−13.90** | −0.556 | −1.064 | **−$31.64** |
| | LONG | 5 | 40.0% | −2.21 | −0.443 | −0.000 | −$2.28 ⚠️ n<8 |
| | both | 30 | 40.0% | **−16.11** | −0.537 | — | **−$33.92** |

The 25 live-era serial shorts, in full — 15 stopped, 10 did not:

```
08-08 01:20  73.75 -> 74.62  sl     -1.170R   08-19 14:20  78.65 -> 79.76  sl    -1.142R
08-08 11:10  75.12 -> 75.97  sl     -1.178R   08-19 17:00  81.59 -> 83.35  sl    -1.094R
08-08 22:00  76.20 -> 77.05  sl     -1.181R   08-19 23:45  85.55 -> 88.26  sl    -1.064R
08-09 18:45  77.12 -> 76.97  be     +0.000R   08-21 01:20  88.56 -> 90.77  sl    -1.081R
08-10 02:25  76.45 -> 76.30  be     +0.000R   08-21 08:25  91.38 -> 93.99  sl    -1.071R
08-11 03:05  76.16 -> 76.01  be     +0.000R   08-22 04:30  97.98 ->101.69  sl    -1.054R
08-11 10:50  75.97 -> 75.22  trail  +0.670R   08-22 10:20  91.97 -> 97.88  sl    -1.032R
08-11 20:15  76.05 -> 77.18  sl     -1.136R   08-25 09:55  99.53 -> 97.87  trail +0.345R
08-13 04:30  76.03 -> 75.79  trail  +0.089R   08-26 23:05 100.18 ->103.16  sl    -1.068R
08-13 22:05  76.30 -> 75.72  trail  +0.448R   08-27 08:05 102.45 ->105.50  sl    -1.068R
08-19 01:40  76.72 -> 77.68  sl     -1.160R   08-27 17:35 107.85 ->106.56  trail +0.254R
08-19 12:35  77.57 -> 78.47  sl     -1.174R   08-28 14:55 106.43 ->105.00  trail +0.309R
                                              08-31 02:15 102.15 ->100.01  open  +0.661R
```

### 2d. 🔴 THE HEADLINE — saved or cost, per side

**It SAVED money. Every scope. Both sides.**

| | SHORT | LONG | combined |
|---|---|---|---|
| **live era** (what the live book actually forwent) | **+13.90 R saved / +$31.64** | +2.21 R / +$2.28 ⚠️ n<8 | **+16.11 R / +$33.92** |
| **full record** | **+20.27 R / +$49.19** | +8.45 R / +$19.17 | **+28.72 R / +$68.36** |
| every-signal-independently (upper bound, pseudo-replicated) | +267.74 R / +$753.47 | +104.15 R / +$128.95 | +371.89 R / +$882.42 |

Dollars are at **live size ($100 notional) throughout**, including the pre-live-flip window, so paper-era rows are priced as if they had been live. For scale: SOL's entire realised live short book is **−$3.75**. The daily-regime instruction refused a further **−$31.64** of shorts in the same period — **it kept out roughly eight times the loss the five live shorts actually booked.**

🔴 **The shorts refused on daily-regime grounds would have lost. The instruction is earning its asymmetry, and that closes the question the operator posed.**

### 2e. Split by whether the label was CORRECT — did it persist the next 24 h?

Label recomputed hourly from candles; "persisted" = the recomputed daily label 24 h later is the same value.

| scope | side | label persisted | n | win | sum R | mean R |
|---|---|---|---|---|---|---|
| full record, independent | SHORT | **yes** | 708 | 43.1% | **−286.88** | −0.405 |
| | SHORT | **no** | 253 | 64.0% | **+19.14** | +0.076 |
| | LONG | yes | 698 | 46.4% | −98.62 | −0.141 |
| | LONG | no | 250 | 49.6% | −5.53 | −0.022 |
| full record, serial | SHORT | **yes** | 46 | 39.1% | **−22.19** | −0.482 |
| | SHORT | **no** | 13 | 69.2% | **+1.92** | +0.148 |
| | LONG | yes | 36 | 44.4% | −3.19 | −0.089 |
| | LONG | no | 17 | 29.4% | −5.26 | −0.309 |
| live era, serial | SHORT | yes | 23 | 34.8% | **−14.35** | −0.624 |
| | SHORT | no | 2 | — | — | — ⚠️ **n<8, NOT RANKED** |

**This is the one place a real distinction shows.** When the daily label was still saying the same thing 24 h later, refusing the trade was right and expensive to have taken (−0.482 R/trade serial). When the label flipped within 24 h, refusing it was mildly wrong (+0.148 R/trade, n=13). But **the sign flip is carried by only 13 serial cases**, it does **not** reproduce on the LONG side (where non-persistence is *worse*, −0.309 R), and in the live era the non-persist cell is n=2 and **is not ranked**. It is a lead, not a finding.

---

## 3. THE LAG, PRICED

### 3a. Age of the reading — hours since the recomputed `trend_1d` last CHANGED value

| side | n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|---|
| SHORT | 961 | 0.0 h | 13.8 h | **67.8 h** | 117.4 h | 325.8 h | 85.6 h |
| LONG | 948 | 0.0 h | 10.3 h | **32.2 h** | 130.7 h | 325.8 h | 78.9 h |

Bucket shares — SHORT: <24 h 283 (29.4%), 24–72 h 248 (25.8%), >72 h 430 (44.7%). LONG: <24 h 412 (43.5%), 24–72 h 159 (16.8%), >72 h 377 (39.8%).

### 3b / 3c. 🔴 Outcome by label age — **n stated before every result; nothing below n=8 is ranked**

**Independent** — SHORT n per bucket: <24 h = 283, 24–72 h = 248, >72 h = 430. LONG: 412 / 159 / 377.

| side | age | n | win | sum R | mean R |
|---|---|---|---|---|---|
| SHORT | <24 h | 283 | 66.4% | −9.57 | −0.034 |
| SHORT | **24–72 h** | 248 | 23.8% | **−174.77** | **−0.705** |
| SHORT | >72 h | 430 | 51.2% | −83.40 | −0.194 |
| LONG | <24 h | 412 | 47.1% | −33.58 | −0.081 |
| LONG | 24–72 h | 159 | 63.5% | +15.54 | +0.098 |
| LONG | >72 h | 377 | 40.6% | −86.11 | −0.228 |

**Serial, full record** — SHORT n per bucket: <24 h = 20, 24–72 h = 17, >72 h = 22. LONG: 22 / 10 / 21.

| side | age | n | win | sum R | mean R |
|---|---|---|---|---|---|
| SHORT | <24 h | 20 | 50.0% | −5.48 | −0.274 |
| SHORT | **24–72 h** | 17 | 17.6% | **−14.48** | **−0.851** |
| SHORT | >72 h | 22 | 63.6% | −0.31 | −0.014 |
| LONG | <24 h | 22 | 45.5% | +0.26 | +0.012 |
| LONG | 24–72 h | 10 | 40.0% | −1.36 | −0.136 |
| LONG | >72 h | 21 | 33.3% | −7.36 | −0.350 |

**Serial, live era** — SHORT n per bucket: <24 h = **6**, 24–72 h = 9, >72 h = 10. LONG: **2 / 1 / 2**.
SHORT 24–72 h: n=9, win 22.2%, sum R −7.78, mean −0.865. SHORT >72 h: n=10, win 50.0%, sum R −3.28, mean −0.328.
**SHORT <24 h (n=6) and all three LONG buckets (n=2/1/2) are BELOW n=8 and are NOT RANKED.**

🔴 **The hypothesis is refuted.** "Skips on a fresh label are right and skips on a 3-day-old label are wrong" is the opposite of what the data says. The stalest bucket (>72 h) is the **least** costly to have refused, in every scope. The **freshest-but-not-fresh** bucket (24–72 h) is the worst, by a wide margin, on both the independent and the serial cut. And **no SHORT bucket is positive in any scope** — there is no age at which refusing these shorts would have been a mistake. **There is nothing actionable here, and I am not going to dress up a non-monotonic pattern as one.**

---

## 4. WHAT REMOVING THE INSTRUCTION WOULD MEAN — descriptive only

### 4a. 🔴 It cannot be replayed. Saying otherwise would be a fabrication.

Deleting six lines from a system prompt changes what an LLM emits on every one of 4,093 consultations. There is no way to recover those counterfactual verdicts from stored data, and no replay in this report simulates them. **Every number in §2 is the outcome of the TRADES, not of the model's alternative decisions.** Nothing here is a prediction of what the advisor would have said.

### 4b. What CAN be bounded — the ceiling

§2 is the **full extent** of what the instruction held out: if *every* daily-regime skip had become an entry, the book would have taken **−28.72 R (−$68.36)** over the full record and **−16.11 R (−$33.92)** in the live era, serial. Since the model would certainly still have skipped some of them for the other reasons in the prompt (walls, flat-market guard, stale tiers), the instruction's true contribution lies somewhere in **[0, +28.72 R]** full record and **[0, +16.11 R]** live. **The ceiling is a saving and the floor is zero. There is no scenario in this data where removing it earns money.** That is a bound, not a forecast.

### 4c. 🔴 The lower bound with teeth — how the overrides actually performed

The 6 times the model refused to follow the instruction are the **only real evidence** of what happens when the lean is not obeyed. They produced 5 positions:

| vpos | book | side | opened | exit | R |
|---|---|---|---|---|---|
| 12 | paper | LONG | 2026-06-24 | sl | **−1.049** |
| 21 | paper | LONG | 2026-07-19 | trail | **+0.285** |
| 26 | paper | LONG | 2026-08-02 | sl | **−1.085** |
| **32** | **🔴 LIVE** | **SHORT** | 2026-08-10 | exit_signal | **−0.180** |
| **34** | **🔴 LIVE** | **SHORT** | 2026-08-13 | sl | **−0.643** |

**n = 5, one winner, sum −2.672 R, mean −0.534 R. The live subset is 0 for 2, −0.823 R.**

🔴 **And these are not hypothetical: vpos 32 and 34 are two of the five live shorts in SOL's book.** Two of the five live shorts the operator cited exist *because* the model overrode this instruction, and both lost. The remaining three live shorts (35, 36, 37) were entered with `trend_1d = neutral` and `trend_4h = bear` — the instruction **supported** those, and they lost −0.701, −0.757 and −1.226 R. **n=5 in total; it cannot be ranked, and it is stated only because it is the entire live short book.**

---

## 5. CONTROLS

**Bonferroni (declared in the header): α = 0.05 over 79 cells → p < 0.00063 required.**

### 5a. 12-window sign stability, equal-time windows, serial replay

| | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | W10 | W11 | W12 | tally |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SHORT | − | − | − | − | + | − | + | − | − | + | − | − | **9 neg / 3 pos** |
| LONG | − | + | − | ∅ | − | + | − | − | − | − | ∅ | + | **7 neg / 3 pos / 2 empty** |

Stable in sign but **not unanimous**. The three positive SHORT windows (07-06→07-13 +1.47 R, 07-20→07-28 +2.30 R, 08-11→08-18 +0.01 R) are real and are not being hidden.

### 5b. Regime test, both legs populated (recomputed label at the skip, serial)

| side | regime | n | win | sum R | mean R |
|---|---|---|---|---|---|
| SHORT | bull | 37 | 48.6% | −12.15 | −0.328 |
| SHORT | neutral | 24 | 45.8% | −8.58 | −0.357 |
| SHORT | bear | 7 | 42.9% | −0.98 | −0.140 ⚠️ **n<8, NOT RANKED** |
| LONG | bull | 5 | — | — | ⚠️ **n<8, NOT RANKED** |
| LONG | neutral | 25 | 40.0% | −5.80 | −0.232 |
| LONG | bear | 33 | 45.5% | −2.30 | −0.070 |

Negative in **every** rankable cell, on both sides, in all three regimes. The result is not a `bull`-regime artefact.

### 5c. Independent sample — disjoint eras

| side | paper era 06-08 → 08-07 | live era 08-07 → 09-01 |
|---|---|---|
| SHORT | n=35, win 48.6%, **−7.54 R**, mean −0.215 | n=25, win 40.0%, **−13.90 R**, mean −0.556 |
| LONG | n=48, win 39.6%, **−6.24 R**, mean −0.130 | n=5 ⚠️ **n<8** |

The sign holds out of sample on both rankable cells.

### 5d. Significance, honestly

| cell | n | mean R | 95% CI | P(mean ≥ 0) | vs Bonferroni 0.00063 |
|---|---|---|---|---|---|
| SHORT live era, serial | 25 | **−0.556** | [−0.818, −0.278] | **0.0001** | ✅ **SURVIVES** |
| SHORT full record, serial | 59 | −0.344 | [−0.570, −0.107] | 0.0028 | ❌ nominal only |
| LONG full record, serial | 53 | −0.160 | [−0.382, +0.072] | 0.0927 | ❌ not significant |
| SHORT independent | 961 | −0.279 | [−0.336, −0.220] | <0.0001 | ⚠️ pseudo-replicated — **n is not honest, do not cite** |
| LONG independent | 948 | −0.110 | [−0.162, −0.056] | <0.0001 | ⚠️ same caveat |

10,000-resample bootstrap, seed 20260901.

🔴 **And the negative that must not be softened: the win rate is a coin flip.** A two-sided sign test on per-trade R is **not significant anywhere** — SHORT full record p = 0.6029 (32 of 59 negative), SHORT live p = 0.4244 (15 of 25). The refused shorts were **not directionally wrong more often than right**. What makes them lose is payoff shape:

| cell | wins | losses | mean win | mean loss | payoff ratio |
|---|---|---|---|---|---|
| SHORT full record | 27 | 32 | +0.555 R | −1.101 R | **0.50** |
| SHORT live era | 10 | 15 | +0.278 R | −1.112 R | **0.25** |
| LONG full record | 21 | 32 | +0.654 R | −0.693 R | 0.94 |

A short that works trails out for a fraction of R; a short that fails pays the full stop. **The instruction is not filtering trades that were about to be wrong — it is filtering trades whose geometry was adverse in a rising market.** That is a real distinction and the report would be dishonest without it.

🔴 **n honestly: SOL's live short book is FIVE positions. It cannot rank anything.** Every live-era conclusion here rests on the 25-trade serial counterfactual, not on the realised book.

---

## VERDICT

🔴 **The daily-regime instruction has SAVED money. It is not obstructing the book; it is protecting it.**

Under SOL's own live exit contract, honouring its own one-position-per-side limit, the trades it refused on daily-regime grounds would have returned **−13.90 R (−$31.64) on the short side in the live era** and **−20.27 R (−$49.19) over the full record**; longs refused on the same grounds would have returned **−8.45 R (−$19.17)**. The live-era short cell is the one result in this report that **survives Bonferroni** (mean R −0.556, P(mean ≥ 0) = 0.0001 against a 0.00063 threshold). It holds out of sample in the paper era, holds in 9 of 12 time windows, and holds in every rankable regime cell on both sides. For scale, it kept out roughly **eight times** the −$3.75 the five realised live shorts actually cost.

**And the apparent bias against shorts was mine, not the instruction's.** Conditioned properly on whether the regime opposed the side, pass rates are statistically identical between sides in both legs (p = 0.43 opposed, p = 0.16 unopposed), and each side spent about half the full record in the opposed bucket. The 6.35× I published at 20:16 was **exposure to an August uptrend**, and I should have run this control before printing that ratio.

**Three negatives I will not soften.** The win rate of the refused shorts is a coin flip and the sign test is not significant — the edge is entirely in payoff shape (0.50, and 0.25 in the live era), which means the instruction is filtering *geometry in a trend*, not *directional error*. The lag hypothesis is refuted: the stalest labels produced the least costly refusals and no age bucket is positive, so there is no age split to act on. And the full-record short cell (p = 0.0028) does **not** survive the correction it is measured against — only the live-era cell does.

**What would settle the parts that cannot be ranked.** The live short book is n=5 and the live LONG daily-regime counterfactual is n=5. To rank the LONG leg in the live era at the observed effect size (mean −0.44 R, sd ≈ 0.6) at the Bonferroni threshold needs roughly **n ≈ 40 serial trades**. SOL produced **5 live-era serial LONG daily-regime opportunities in 25 days ≈ 0.2/day**, so that is **on the order of 200 days — about seven months**. The SHORT leg needs nothing further: it is already ranked and it is negative.

**No change is proposed. Nothing was applied.**

---

## READ-ONLY CONFIRMATION

* **DB read-only.** Every query opened `file:/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db?mode=ro` (`SQLITE_OPEN_READONLY`). SELECTs only.
* **cwd outside SOL's tree.** All work ran from `/tmp/claude-0/…/scratchpad` and `/root`. **SOL's config was never imported in any process** — every constant in §0 was read as text out of the source files and is cited to its line. The replay engine is standalone code in the scratchpad.
* **No writes attempted.** Not to files, not to the DB — including no probe write to demonstrate read-only mode, which would itself have been an attempt.
* **No orders placed or cancelled.** Venue traffic was **26 public `fetch_ohlcv` calls** (5 m history) plus the daily/hourly pulls, all through the local Tor SOCKS proxy on 127.0.0.1:9050. No private endpoint, no API key, no `fetch_positions`, no `fetch_open_orders`.
* **Service untouched.** `mercury-sol.service` — `SubState=running`, `MainPID=1196924` (unchanged), `ActiveEnterTimestamp=Mon 2026-08-24 13:29:27 UTC`, **`NRestarts=0`, unchanged.**
* **All 33 `.py` file hashes IDENTICAL** before and after — verified by full `md5sum` diff. `config.py` `ed7a14b0df440f2fc5040e87ea5b504b`, `main.py` `35b0201626303c730df6d1c2c3ec3f9e`, `claude_advisor.py` `a02ce04e6a12864bfcc0c6118137ebd7`, `virtual_trader.py` `dc2d75bdbf33f4217b005335bcd144ca`, `trail_arm.py` `f638384bcd295d74c827203aa30781b7`.
* 🔴 **`trades.db`'s hash changed** (`02500149…` → `09e347b3…`) and I am naming it rather than omitting it. **It was the live bot, not me.** `lsof` shows the file held by `gunicorn` PID **1196924** — the service's own `MainPID`. Row **23048** (`context_recorded`) was written at **20:40:03 UTC**, after my 20:31:33 baseline hash, by the running bot's normal scan. My connection was `mode=ro` and physically cannot write.
* **Titan not opened.** The single exception is the mandated `openitems_guard` pre-flight (`/root/titan-bot/tools/openitems_guard.py`) → **exit 0**. No other Titan file was read; nothing in `/root/titan-bot` was written.
