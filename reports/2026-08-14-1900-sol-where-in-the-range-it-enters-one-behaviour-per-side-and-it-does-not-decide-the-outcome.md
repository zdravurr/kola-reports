# Mercury-SOL — where in the range it enters: ONE BEHAVIOUR per side, and it does not decide the outcome

**2026-08-14 19:00 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · READ-ONLY THROUGHOUT — no file written, no restart, no order, no DB write. Nothing proposed before §4.**

Titan (`/root/titan-bot`): **not touched, not read for state, no numbers imported.** HEAD `897850b`, clean, MainPID 2538048.

Parent: [17:50 §2a](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-14-1750-sol-the-duplicate-is-a-row-not-a-call-and-the-range-still-does-not-separate.md) — the `pos24` column computed there for all 29 and never analysed.

---

## ⚡ THE SHORT VERSION

1. **🔴 IT IS NOT A DISTRIBUTION. IT IS ONE BEHAVIOUR PER SIDE.** All **16 of 16** shorts sit in the bottom third of the prior 24 h range — **16 of 16 below 0.20**, 13 of 16 below 0.10, median **0.062**, four *at or below the 24 h low*. **Zero shorts, ever, above pos24 0.20.** All **13 of 13** longs sit at 0.379 or higher — 11 in the top third, 9 above 0.80, **four at or above the 24 h high**, median **0.905**. Three of the six side × third cells are **empty**. There is nothing to compare, and that is the finding.
2. **The bot buys the top and sells the bottom. Always.** Not a tendency — a rule it follows without exception across 62 days and two eras.
3. **🔴 AND THE OBVIOUS READING OF THAT IS WRONG.** The counts say the extreme holds most of the time — shorts bounced 9 of 16 at +4 h, top-longs failed 8 of 11. That looks like "systematically selling into support" until it is de-confounded against the tape itself: **the unconditional bounce rate at the bottom third is 80.2 %**, and the bot's shorts bounce only **56.2 %**. Its shorts break the 24 h low at **2.21× the base rate** at +4 h and **2.92×** at +1 h. **The placement is genuinely selective. It is not selling into support.**
4. **🔴 But the selectivity dies at 12 h — 0.83×, i.e. exactly the base rate** — and it never converts into money.
5. **What actually decides the outcome is whether the extreme gives way, and that separates enormously**: level broke by +4 h → n=10, ΣR **+4.585**, mean +0.459, 60 % win; level held → n=19, ΣR **−10.570**, mean −0.556, 21 % win. p = 0.0036, the **only** thing in this pass that clears Bonferroni. **And it is LOOK-AHEAD** — unknowable at entry, and close to a restatement of the outcome.
6. **🔴 Nothing known at entry predicts it.** pos24 → ρ = −0.147 (p = 0.59). ADX → −0.094 (p = 0.73). 24 h width → −0.506 (p = 0.049, nominal only). ER(4h) → −0.315 (p = 0.24). That closes the loop.
7. **Placement does not separate outcomes either.** pos24 vs R: SHORT ρ = +0.359 (p = 0.173), LONG ρ = +0.115 (p = 0.710). Both range extremes contain the book's best trades *and* its worst.
8. **The largest lopsided cell is n = 5, not n ≥ 8.** SHORT with pos24 < 0.046 is **0 winners of 5, ΣR −4.054** — real, but it needs **8** consecutive losers to be worth 5 % on its own and it has 5. **The §4b precondition is not met. Nothing is proposed.**
9. **So: the twenty-fifth dead branch.** Said plainly in §4a, not softened.

---

## 0. WHAT THIS IS MEASURED ON

| item | source |
|---|---|
| the 29 entries, `pos24`, `lo24`, `hi24`, R | the 17:50 report's own computed table — **not re-derived**, so the two documents cannot disagree |
| price paths after entry | Bybit SOLUSDT-perp 5m candles via Tor, refetched 2026-08-14 18:49, **35,074 bars** to 18:45 today |
| base rates | the same 1h tape, **2,922 bars** from 2026-04-15 |
| **`market_regime`** | **not used** |
| files modified in `mercury-sol` | **NONE.** Zero `.py` touched since the 18:28 restart. No DB write. |

**`pos24` recap:** `(entry price − low₂₄ₕ) / (high₂₄ₕ − low₂₄ₕ)` over the **24 closed 1 h bars before the entry bar**. Below 0 means the entry is beneath the whole prior 24 h range; above 1 means above it.

---

# 1. THE FULL PICTURE, ON ALL 29

## 1a. Every entry, sorted by where in the range it sat

### SHORT — 16 entries

| pos24 | vpos | era | opened (UTC) | R | ADX | 24h w% | closed by |
|---|---|---|---|---|---|---|---|
| **−0.210** | 20 | paper | 07-17 13:40 | −1.124 | 32.5 | 3.68 | sl |
| **−0.053** | 27 | paper | 08-03 06:45 | −0.660 | 15.5 | 2.33 | sl |
| **−0.045** | 34 | live | 08-13 16:40 | −0.643 | 12.7 | 1.78 | sl |
| **0.000** | 24 | paper | 07-29 20:05 | −1.050 | 21.7 | 2.52 | sl |
| 0.044 | 23 | paper | 07-28 11:05 | −0.577 | 36.5 | 6.47 | exit_signal |
| 0.046 | 17 | paper | 07-13 03:10 | +0.004 | 18.8 | 3.15 | sl |
| 0.052 | 28 | paper | 08-06 19:00 | −0.153 | 13.2 | 2.64 | exit_signal |
| 0.057 | 32 | live | 08-10 15:15 | −0.180 | 23.6 | 2.30 | exit_signal |
| 0.067 | 25 | paper | 08-01 17:20 | **+1.257** | 23.6 | 1.45 | trail |
| 0.073 | 35 | live | 08-14 14:20 | −0.701 | 17.6 | 2.01 | sl |
| 0.075 | 19 | paper | 07-16 00:25 | +0.463 | 23.7 | 2.76 | exit_signal |
| 0.076 | 11 | paper | 06-23 00:30 | **+1.133** | 15.8 | 5.35 | exit_signal |
| 0.087 | 15 | paper | 07-08 05:05 | +0.140 | 23.2 | 5.84 | trail |
| 0.139 | 10 | paper | 06-22 00:00 | −1.066 | 30.0 | 3.38 | sl |
| 0.144 | 13 | paper | 06-24 13:25 | **+1.337** | 25.4 | 3.05 | trail |
| **0.157** | 14 | paper | 06-25 14:00 | −1.032 | 19.3 | 8.74 | sl |

**The whole column spans −0.210 to 0.157.** Sixteen shorts, and the *highest* one ever taken sits at 15.7 % of the range.

### LONG — 13 entries

| pos24 | vpos | era | opened (UTC) | R | ADX | 24h w% | closed by |
|---|---|---|---|---|---|---|---|
| **0.379** | 12 | paper | 06-24 02:25 | −1.049 | 39.5 | 5.69 | sl |
| **0.503** | 31 | live | 08-10 08:10 | −1.155 | 31.4 | 2.27 | sl |
| 0.754 | 21 | paper | 07-19 06:50 | +0.285 | 27.4 | 2.77 | trail |
| 0.797 | 9 | paper | 06-21 02:50 | −0.264 | 39.3 | 6.59 | exit_signal |
| 0.844 | 30 | live | 08-08 21:10 | +0.762 | 52.9 | 4.29 | trail |
| 0.858 | 29 | live | 08-08 08:50 | **+1.355** | 31.9 | 3.01 | exchange_UNKNOWN |
| 0.905 | 8 | paper | 06-20 07:00 | −0.739 | 27.9 | 6.43 | exit_signal |
| 0.917 | 18 | paper | 07-14 15:45 | −1.074 | 26.3 | 4.83 | sl |
| 0.969 | 16 | paper | 07-10 08:30 | −1.146 | 25.9 | 2.82 | sl |
| **1.003** | 26 | paper | 08-02 05:00 | −1.085 | 29.9 | 4.07 | sl |
| **1.017** | 22 | paper | 07-21 03:10 | −1.064 | 25.4 | 3.70 | sl |
| **1.037** | 33 | live | 08-11 22:00 | −0.049 | 27.3 | 2.44 | exit_signal |
| **1.068** | 7 | paper | 06-14 23:50 | **+2.089** | 29.5 | 5.37 | exit_signal |

## 1b. 🔴 THIRDS OF THE RANGE, PER SIDE — n FIRST

| side | cell | **n** | win % | ΣR | mean R | vpos |
|---|---|---|---|---|---|---|
| SHORT | **bottom (<0.33)** | **16** | 37.5 % | −2.852 | −0.178 | 10,11,13,14,15,17,19,20,23,24,25,27,28,32,34,35 |
| SHORT | middle | **0** | — | — | — | *(empty)* |
| SHORT | top (>0.67) | **0** | — | — | — | *(empty)* |
| LONG | bottom | **0** | — | — | — | *(empty)* |
| LONG | middle | **2** | 0.0 % | −2.204 | −1.102 | 12, 31 |
| LONG | **top (>0.67)** | **11** | 36.4 % | −0.929 | −0.084 | 7,8,9,16,18,21,22,26,29,30,33 |

**Three of six cells are empty and a fourth holds two rows.** There is no comparison to make between thirds, because the bot never visits four of them. Everything below is therefore about *what the one occupied cell per side does*, not about which cell is better.

*(For the record: the two middle-third longs, vpos 12 and 31, are the only two longs not taken near the high, and both lost — −1.049 and −1.155. n = 2. Nothing is claimed from it.)*

## 1c / 1d. 🔴 CONCENTRATED OR SPREAD? — reported as counts, no test

```
SHORT  n=16   min −0.210   median +0.062   max +0.157   IQR [+0.033, +0.079]
       below 0.10 : 13 of 16          above 0.90 :  0 of 16
       below 0.15 : 15 of 16          above 0.85 :  0 of 16
       below 0.20 : 16 of 16          above 0.80 :  0 of 16
       below 0.33 : 16 of 16          above 0.67 :  0 of 16
       AT OR BELOW the 24h LOW (pos24 <= 0) :  4        AT OR ABOVE the 24h HIGH : 0

LONG   n=13   min +0.379   median +0.905   max +1.068   IQR [+0.797, +1.003]
       below 0.10 :  0 of 13          above 0.90 :  7 of 13
       below 0.20 :  0 of 13          above 0.80 :  9 of 13
       below 0.33 :  0 of 13          above 0.67 : 11 of 13
       AT OR BELOW the 24h LOW : 0             AT OR ABOVE the 24h HIGH (pos24 >= 1) : 4
```

🔴 **The operator's hypothesis was "if 14 of 16 shorts sit below 0.15, the bot has ONE BEHAVIOUR." It is 15 of 16 below 0.15 and 16 of 16 below 0.20.** The interquartile range of all sixteen shorts is **0.046 wide**. Sixteen independent entries across 62 days, two eras, three different exit geometries and a paper→live flip, and every one lands in the same twentieth of the range.

**The mirror holds on longs:** zero of thirteen anywhere below 0.379, and **four entries taken above the prior 24 h high** — buying a price that did not exist in the preceding day.

This is a mechanical fact about the entry cascade, not a statistical claim, and it needs no test.

---

# 2. CONTINUATION OR EXHAUSTION?

## 2a/2b. Definitions, stated before any number

> For a **SHORT** entered near the prior-24 h **LOW** `L`:
> **BROKE** (continuation) = the horizon's **closing** price is **below L**.
> **BOUNCED** (exhaustion) = the horizon's closing price is **at or above L**.
> *Pierced* = the horizon's low went below L at some point, whether or not it closed there.
> For a **LONG** near the prior-24 h **HIGH** `H`: the mirror — close above H = broke out.
> Horizons on 5 m closes strictly **after** the entry timestamp. `L` and `H` are the same 24 × 1 h closed-bar extremes that produced `pos24`; nothing is re-derived.

### Every SHORT (all 16 are in the bottom third) — close vs the 24 h low

| vpos | pos24 | R | +1h | +4h | +12h |
|---|---|---|---|---|---|
| 20 | −0.210 | −1.124 | +0.31 % BOUNCED | +1.36 % BOUNCED | +1.28 % BOUNCED |
| 27 | −0.053 | −0.660 | −0.14 % BROKE | −0.12 % BROKE | +1.91 % BOUNCED |
| 34 | −0.045 | −0.643 | +0.74 % BOUNCED | +1.28 % BOUNCED | +0.81 % BOUNCED |
| 24 | 0.000 | −1.050 | −0.21 % BROKE | +1.46 % BOUNCED | +0.92 % BOUNCED |
| 23 | 0.044 | −0.577 | +0.58 % BOUNCED | +0.92 % BOUNCED | +0.63 % BOUNCED |
| 17 | 0.046 | +0.004 | +0.13 % BOUNCED | +0.79 % BOUNCED | +0.21 % BOUNCED |
| 28 | 0.052 | −0.153 | +0.32 % BOUNCED | −0.03 % BROKE | +0.21 % BOUNCED |
| 32 | 0.057 | −0.180 | −0.42 % BROKE | −0.14 % BROKE | +0.09 % BOUNCED |
| 25 | 0.067 | **+1.257** | −1.30 % BROKE | −1.08 % BROKE | +1.62 % BOUNCED |
| 35 | 0.073 | −0.701 | +0.37 % BOUNCED | +0.13 % BOUNCED | *incomplete* |
| 19 | 0.075 | +0.463 | −0.12 % BROKE | −0.09 % BROKE | −0.88 % BROKE |
| 11 | 0.076 | **+1.133** | +0.86 % BOUNCED | +0.91 % BOUNCED | −2.97 % BROKE |
| 15 | 0.087 | +0.140 | +0.26 % BOUNCED | −1.16 % BROKE | −1.22 % BROKE |
| 10 | 0.139 | −1.066 | +1.69 % BOUNCED | +1.76 % BOUNCED | +2.67 % BOUNCED |
| 13 | 0.144 | **+1.337** | +1.00 % BOUNCED | −4.10 % BROKE | −1.07 % BROKE |
| 14 | 0.157 | −1.032 | +3.35 % BOUNCED | +4.44 % BOUNCED | +5.02 % BOUNCED |

```
+ 1h : BROKE  5 / BOUNCED 11  of 16   (69% bounced)   pierced the low at some point:  9
+ 4h : BROKE  7 / BOUNCED  9  of 16   (56% bounced)   pierced: 13
+12h : BROKE  4 / BOUNCED 11  of 15   (73% bounced)   pierced: 13   [vpos 35 incomplete]
```

### LONGS in the top third (11) — close vs the 24 h high

| vpos | pos24 | R | +1h | +4h | +12h |
|---|---|---|---|---|---|
| 21 | 0.754 | +0.285 | −0.57 % failed | −0.42 % failed | −1.28 % failed |
| 9 | 0.797 | −0.264 | −0.97 % failed | −1.43 % failed | −0.48 % failed |
| 30 | 0.844 | +0.762 | −0.86 % failed | −1.15 % failed | −0.49 % failed |
| 29 | 0.858 | **+1.355** | −0.37 % failed | +0.49 % **BROKE** | +1.38 % **BROKE** |
| 8 | 0.905 | −0.739 | −1.34 % failed | −1.19 % failed | −1.01 % failed |
| 18 | 0.917 | −1.074 | −0.60 % failed | −0.72 % failed | −0.04 % failed |
| 16 | 0.969 | −1.146 | −0.24 % failed | −0.28 % failed | −2.03 % failed |
| 26 | 1.003 | −1.085 | +0.08 % **BROKE** | −0.75 % failed | −0.49 % failed |
| 22 | 1.017 | −1.064 | −0.34 % failed | +0.34 % **BROKE** | −0.63 % failed |
| 33 | 1.037 | −0.049 | −0.26 % failed | −0.05 % failed | +0.35 % **BROKE** |
| 7 | 1.068 | **+2.089** | +0.41 % **BROKE** | +0.78 % **BROKE** | +2.76 % **BROKE** |

```
+ 1h : BROKE OUT 2 / FAILED  9  of 11   (82% failed)   pierced the high:  5
+ 4h : BROKE OUT 3 / FAILED  8  of 11   (73% failed)   pierced:  7
+12h : BROKE OUT 3 / FAILED  8  of 11   (73% failed)   pierced: 10
```

## 2c. 🔴 THE COUNTS — AND THE DE-CONFOUND THAT REVERSES THEIR MEANING

Read alone, those counts say the bot sells into support and buys into resistance and the level holds. **That reading is wrong, and the tape says so.**

**The unconditional base rate**, same definitions, applied to every closed 1 h bar of the tape (867–937 comparable moments per cell):

| horizon | bottom third: broke the low | **bounce rate** | top third: broke out | **failure rate** |
|---|---|---|---|---|
| +1 h | 93 / 869 = 10.7 % | **89.3 %** | 90 / 937 = 9.6 % | **90.4 %** |
| +4 h | 172 / 867 = 19.8 % | **80.2 %** | 175 / 937 = 18.7 % | **81.3 %** |
| +12 h | 275 / 861 = 31.9 % | **68.1 %** | 269 / 937 = 28.7 % | **71.3 %** |

**Against that:**

| horizon | the bot's bottom-third SHORTS broke | baseline | **ratio** | binomial p |
|---|---|---|---|---|
| +1 h | 5/16 = **31.2 %** | 10.7 % | **2.92×** | 0.0223 |
| +4 h | 7/16 = **43.8 %** | 19.8 % | **2.21×** | 0.0256 |
| +12 h | 4/15 = 26.7 % | 31.9 % | **0.83×** | 0.787 |

| horizon | the bot's top-third LONGS broke out | baseline | ratio | binomial p |
|---|---|---|---|---|
| +1 h | 2/11 = 18.2 % | 9.6 % | 1.89× | 0.286 |
| +4 h | 3/11 = 27.3 % | 18.7 % | 1.46× | 0.442 |
| +12 h | 3/11 = 27.3 % | 28.7 % | 0.95× | 1.000 |

🔴 **So the answer to 2c is: NO, the bot is not systematically selling into support.** When it shorts the bottom of the range, the low gives way **more than twice as often as at a random bottom-third moment** — 2.92× at one hour, 2.21× at four. **A "9 of 16 bounced" headline would have been a false alarm**: at the base rate you would expect 12.8 of 16 to bounce, and only 9 did.

🔴 **And two things immediately limit it.** The edge is **gone by 12 hours** (0.83×, i.e. the base rate — and SOL's median holding time is measured in hours to days, not four hours). And the long side never shows it at all: 1.89× / 1.46× / 0.95×, none distinguishable from chance. **This is a short-side, short-horizon selection effect, nominal at p ≈ 0.02–0.03 and failing the Bonferroni bar of 0.00714.**

---

# 3. WHAT DISTINGUISHES THE ONES THAT WORKED

## 3a. The book's best five

| vpos | side | R | pos24 | where |
|---|---|---|---|---|
| 7 | LONG | **+2.089** | 1.068 | **at/above the 24 h HIGH** |
| 29 | LONG | +1.355 | 0.858 | top of the range |
| 13 | SHORT | +1.337 | 0.144 | bottom of the range |
| 25 | SHORT | +1.257 | 0.067 | bottom of the range |
| 11 | SHORT | +1.133 | 0.076 | bottom of the range |

## 3b. The book's worst six

| vpos | side | R | pos24 | where |
|---|---|---|---|---|
| 31 | LONG | −1.155 | 0.503 | middle |
| 16 | LONG | −1.146 | 0.969 | top of the range |
| 20 | SHORT | −1.124 | −0.210 | **at/below the 24 h LOW** |
| 26 | LONG | −1.085 | 1.003 | **at/above the 24 h HIGH** |
| 18 | LONG | −1.074 | 0.917 | top of the range |
| 10 | SHORT | −1.066 | 0.139 | bottom of the range |

🔴 **Both extremes appear in both lists.** Buying above the 24 h high produced the book's single best trade (vpos 7, +2.089R) *and* its fourth worst (vpos 26, −1.085R). Shorting the bottom produced +1.337, +1.257 and +1.133 *and* −1.124, −1.066. **Placement alone does not sort them.**

## 3c. Every placement cell with n ≥ 3

| cell | n | W/L | win % | ΣR | mean R | vpos |
|---|---|---|---|---|---|---|
| **SHORT, pos24 ≤ 0.00 (at/below the 24h LOW)** | **4** | **0/4** | **0.0 %** | **−3.477** | −0.869 | 20, 24, 27, 34 🔴 **ZERO WINNERS** |
| LONG, pos24 ≥ 0.90 | 7 | 1/6 | 14.3 % | −3.067 | −0.438 | 7, 8, 16, 18, 22, 26, 33 |
| **SHORT, pos24 < 0.05** | **6** | 1/5 | 16.7 % | −4.050 | −0.675 | 17, 20, 23, 24, 27, 34 |
| LONG that FAILED to break out at +4h | 10 | 2/8 | 20.0 % | −5.513 | −0.551 | *(look-ahead)* |
| SHORT that BOUNCED at +4h | 9 | 2/7 | 22.2 % | −5.057 | −0.562 | *(look-ahead)* |
| LONG, pos24 ≥ 1.00 (at/above the 24h HIGH) | 4 | 1/3 | 25.0 % | −0.109 | −0.027 | 7, 22, 26, 33 |
| SHORT, pos24 > 0.10 | 3 | 1/2 | 33.3 % | −0.762 | −0.254 | 10, 13, 14 |
| LONG, 0.67 < pos24 < 1.00 | 7 | 3/4 | 42.9 % | −0.821 | −0.117 | 8, 9, 16, 18, 21, 29, 30 |
| SHORT, pos24 ≥ 0.05 | 10 | 5/5 | 50.0 % | **+1.198** | +0.120 | 10,11,13,14,15,19,25,28,32,35 |
| LONG, pos24 < 0.90 | 6 | 3/3 | 50.0 % | −0.067 | −0.011 | 9, 12, 21, 29, 30, 31 |
| SHORT, 0.00 < pos24 ≤ 0.10 | 9 | 5/4 | 55.6 % | **+1.387** | +0.154 | 11,15,17,19,23,25,28,32,35 |
| SHORT that BROKE the low by +4h | 7 | 4/3 | 57.1 % | +2.205 | +0.315 | *(look-ahead)* |
| LONG that BROKE out by +4h | 3 | 2/1 | 66.7 % | +2.380 | +0.793 | *(look-ahead)* |

**Scanning every possible pos24 threshold on each side for a zero-winner or zero-loser cell:**

```
SHORT   n=5   pos24 < 0.046   winners = 0   ΣR −4.054   [20, 23, 24, 27, 34]   <- the largest
        n=4   pos24 < 0.044   winners = 0   ΣR −3.477   [20, 24, 27, 34]
        n=3   pos24 < 0.000   winners = 0   ΣR −2.427   [20, 27, 34]
LONG    no zero-winner or zero-loser cell with n>=3 exists at ANY pos24 threshold
```

🔴 **The largest lopsided cell in the whole book is n = 5.** The operator's bar was n ≥ 8, and it is not met. For a 0-of-N run to be worth 5 % on its own against this book's 34.5 % base win rate you need **8 consecutive losers**; there are **5**. Its permutation p is 0.0361 against α = 0.00714.

**And the LONG mirror does not exist at all** — no threshold anywhere on the long side produces a cell that is all-winner or all-loser with three or more entries.

---

# 4. THE HONEST FRAME

## 4a. 🔴 PLACEMENT DOES NOT SEPARATE EITHER. THE TWENTY-FIFTH DEAD BRANCH.

**Bonferroni declared: 7 p-valued hypotheses, α = 0.05 / 7 = 0.00714.** The counts in §1 and §2c are counts and carry no p-value.

| # | hypothesis | result | p | clears α? |
|---|---|---|---|---|
| H1 | SHORT: pos24 ranks R | ρ = **+0.359**, n=16 | 0.173 | no |
| H2 | LONG: pos24 ranks R | ρ = **+0.115**, n=13 | 0.710 | no |
| H3 | SHORT pos24 < 0.046 vs the rest | ΣR −4.054 / +1.202, Δmean −0.920 | 0.0361 | no |
| H4 | LONG pos24 ≥ 0.90 vs the rest | ΣR −3.067 / −0.067, Δmean −0.427 | 0.504 | no |
| **H5** | **level BROKE by +4h vs level HELD** | **ΣR +4.585 / −10.570, Δmean +1.015** | **0.0036** | **YES** |
| H6 | pos24 predicts the break (SHORT) | ρ = −0.147 | 0.586 | no |
| H7 | bottom-shorts break the low above chance (+4h) | 43.8 % vs 19.8 %, 2.21× | 0.0256 | no |

**Only H5 clears — and H5 is look-ahead.** Whether the 24 h extreme gives way *after* the entry is not knowable at the entry, and "the level broke and the trade won" is barely more than a restatement of the outcome with extra steps. **It is a diagnosis, not a filter**, and it is reported as one.

**What it diagnoses is worth stating precisely, because it is the real answer to the brief's question:**

> **The outcome is decided almost entirely by whether the extreme gives way.** Level broke: 10 trades, ΣR **+4.585**, 60 % win. Level held: 19 trades, ΣR **−10.570**, 21 % win. The whole book's loss lives in the second group.
>
> **And nothing available at entry predicts which it will be.** pos24 ρ = −0.147 (p = 0.59) · ADX(1h,200) ρ = −0.094 (p = 0.73) · 24 h width ρ = −0.506 (p = 0.049, nominal, fails the bar) · ER(4h) ρ = −0.315 (p = 0.24).

**So the answer to the brief is: no, placement does not decide the outcome, and it is not improvable from this book.** It joins the list. Filters 1–19 died on Titan; filter 20 (the ADX + range-width pair), 21 (opposing wall band), 22 (book liquidity), 23 (EMA envelope re-run) and 24 (the ADX + range pair re-run) died on SOL's own book; **placement is the twenty-fifth.**

🔴 **What that means, stated rather than softened.** The entry decision on this bot is **not improvable by anything this book contains.** Twenty-five candidate discriminators have now been measured on SOL's own 29 positions and not one of them separates outcomes at a bar that survives multiplicity. The book is 29 trades and 62 days; the effects being hunted are a fraction of an R; the 17:50 power calculation already put the range effect at ~2,000 positions and 5.3 years. **The honest conclusion is that further entry-filter work on this book is not a research programme, it is a coin-flip generator with a report attached.** Where the remaining leverage lives — if it lives anywhere — is in the two places that are *not* selection: **exit geometry** (which decides how much of the 19 held-level losers you give back, and which the 0.75R trail change already touched) and **position sizing**. Neither is measured here and neither is proposed here.

## 4b. Does it separate structurally on n ≥ 8? **No — the precondition is not met.**

The instruction was to describe a rule only if a lopsided record appeared on **n ≥ 8**. The largest lopsided cell is **n = 5**. **So nothing is proposed, and nothing is applied.**

For completeness — because the operator will want to see its shape rather than take my word that it is too small — here is the one cell that came closest, stated as a description and **not** as a recommendation:

```
CELL      SHORT with pos24 < 0.046   (shorting essentially AT or BELOW the 24h low)
RECORD    0 winners of 5    ΣR −4.054    vpos 20, 23, 24, 27, 34
COST      refuses 5 of 16 shorts = 31% of the short side, 17% of the whole book
          at 1.02 entries/day that is 0.18 entries/day removed — one refusal every 5.7 days
EFFECT    book −5.985R  ->  −1.931R      (kept: 24 entries)
BAR       needs 8 consecutive losers to be worth 5% alone; has 5.  p = 0.0361 vs α = 0.00714
CAVEAT    3 of the 5 are the three lowest-placed shorts in the book (pos24 −0.210, −0.053,
          −0.045) and 2 of the 5 are live-era. It is the same five entries the 17:50 report's
          RANGE classification kept flagging, arrived at by a different route.
```

🔴 **Read the CAVEAT line before the EFFECT line.** A −4.054R improvement on n = 5 with no winners is exactly the shape that has killed twenty-four previous candidates: it is the *maximum* of a threshold scan over sixteen points, and the scan was told to look for lopsidedness. **A rule found by asking "where is the most one-sided cell?" is fitted by construction.** The pre-registration bar exists to stop that, and here it stops it.

## 4c. Where p-values were and were not used

Quoted p-values appear **only** in §4a's table and the two binomial comparisons in §2c, and all of them are judged against **α = 0.05 / 7 = 0.00714**. Everything in §1 (the placement counts, the empty cells, the IQR), and the raw broke/bounced tallies in §2a–2b, are **counts**, reported as counts. The 16-of-16 and 0-of-13 facts do not need a test and are not given one.

---

## STATE — nothing was changed by this pass

```
mercury-sol   active · master 2162333 / worker 2162408 · since 2026-08-14 18:28:16 · NRestarts=0
              🔴 NOT restarted by this pass. Same pid the 18:40 apply left running.
BOOK          29 closed · ΣR −5.985 · FLAT · active_positions EMPTY · max vpos 35
FILES         mercury-sol: ZERO .py modified since 18:30. No DB write. No order. No restart.
LOADED        (from the 18:40 pass, unchanged) ADVISOR_WALL_ALIGNED_RELAXATIONS=False ·
              BOOK_GATE_LEAN_FLOOR {'LONG': 0.4238, 'SHORT': 0.3489} · gate ARMED
titan         /root/titan-bot — NOT touched, NOT read for state, NO numbers imported.
              HEAD 897850b · working tree clean · MainPID 2538048
```

**Provenance: SOL's own `trades.db` opened `mode=ro`, the 17:50 report's own computed `pos24`/`lo24`/`hi24`, and Bybit SOLUSDT-perp candles fetched fresh through the bot's own venue over Tor. `market_regime` was not used. Titan was not read.**
