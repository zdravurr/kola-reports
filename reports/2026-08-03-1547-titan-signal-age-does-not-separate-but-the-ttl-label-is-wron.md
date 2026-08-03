# titan signal age does not separate but the TTL label is wrong 77 of 77

_2026-08-03 15:47 UTC_

---

# TITAN — DOES SIGNAL AGE SEPARATE? **NO.** BUT THE TTL LABEL IS WRONG 77 TIMES OUT OF 77.

_2026-08-03 16:05 UTC · HEAD `489e0ac` · LIVE, flat · **READ-ONLY — nothing changed, nothing proposed**_

---

## DECISION LINE

**Age does not separate outcomes, and neither does age weighted by what price did since. Add both to
the dead branches.**

- **§2 — 1H tier age is non-monotone.** `<1h` **+0.293R** (n=8) · `1–3h` **−0.036R** (n=14) ·
  `3–6h` **+0.370R** (n=10) · `≥6h` **−0.584R** (n=7). Median split separates by 0.13R. Only the
  `≥6h` tail is clearly bad, on **n=7**.
- **🔴 §2d — the two cases that defeat everything are ORDINARY on age.** vpos 86: 1H age **3.83h,
  62nd percentile**. vpos 91: **2.66h, 51st percentile**. Per the operator's own instruction: they
  are ordinary, so **age is not the answer, and I am saying so.**
- **§3 — the mechanism fails in the opposite direction to the prediction.** The hypothesis was "old
  signal + nothing happened since = stale". The **worst** cell is old signal **and price moved
  cleanly since** (n=5, **−0.473R**); "old + chopped" is **−0.028R** (n=9). Direction-aware is also
  inverted: entries where price had moved **against** the eventual trade did **better** (+0.315R,
  n=4) than those where it had moved with it (+0.052R, n=23).
- **5m age has zero variance** — it is the trigger, 0.00h on all 65 entries. It cannot separate
  anything and was not analysed.

🔴 **And the one real finding, which is not about age at all:**

> **`counted_by_gate: false` renders to the entry advisor as "NOT counted by the gate — matrix TTL
> expired". Across the 87 rows carrying the structured record, that string appears 77 times and is
> WRONG 77 times. Zero are TTL expiry.** 70 (91%) are **intra-conflict** — the signal was present and
> well inside its TTL — and 7 (9%) are **no signal in that category at all**.

**vpos 91 is the case in the operator's question.** Its 15m tier was **25 minutes old** against a
**90-minute** MOMENTUM TTL. It had not expired. It was intra-conflicted (L2.5 / S1.75, 3 signals).
**The advisor was told a false reason, and the question I was asked repeated it** — "vpos 91's 15m
was OPPOSING and expired-TTL" — because the prompt says so. **It was opposing. It was not expired.**

This is a **sixth** instance of "the label does not say what it means", and unlike the analytic ones
it is in a **live prompt the entry advisor reads on every entry**.

---

## §1 — RECONSTRUCTION, AND ITS COVERAGE, BEFORE ANY ANALYSIS

**Method.** `combo_key` carries each tier's signal name at entry (`1H:X|15M:Y|5M:Z`). For each tier I
take the **latest** `trades` row with that `tv_action` on that tier's `tv_tf` at or before the fill,
and age = fill − that arrival. That is the arrival the state machine's slot would hold, because the
slot keeps the most recent matching signal.

| tier | resolved | coverage |
|---|---:|---:|
| **1H** | 65 of 65 | **100%** |
| 15m | 7 of 65 | **11%** |
| **5m** | 65 of 65 | **100%** |

🔴 **The 15m gap is real and dated, not a parsing failure.** 15m HyperWave alerts first appear as
`tv_tf='15m'` rows on **2026-07-26**; before that the 15m tier was set without leaving a separately
timestamped arrival row.

| month | entries | 1H resolved | 15m | 5m |
|---|---:|---:|---:|---:|
| 2026-05 | 19 | 19 | **0** | 19 |
| 2026-06 | 16 | 16 | **0** | 16 |
| 2026-07 | 29 | 29 | 6 | 29 |
| 2026-08 | 1 | 1 | 1 | 1 |

**15m age is not analysable before 2026-07-26 and I have not modelled it.**

### The reconstruction was validated before use (§0 standing methodology)

Against the 7 entries that carry the authoritative `entry_tiers_json`:

| vpos | stated 1H / 15m / 5m | reconstructed |
|---|---|---|
| 85 | 5.8h / 2.8h / 0m | 5.83h / 2.83h / 0.00h |
| 86 | 3.8h / 5m / 0m | 3.83h / 0.08h / 0.00h |
| 87 | 2.1h / 5m / 0m | 2.08h / 0.08h / 0.00h |
| 88 | 35m / 1.6h / 0m | 0.58h / 1.58h / 0.00h |
| 89 | 3.3h / 20m / 0m | 3.33h / 0.33h / 0.00h |
| 90 | 5.4h / 25m / 0m | 5.42h / 0.41h / 0.00h |
| 91 | 2.7h / 25m / 0m | 2.66h / 0.42h / 0.00h |

**7 of 7 match to the minute.** Only then was it used.

---

## §2 — DOES AGE SEPARATE?

**2a. 1H age at entry**, clean cohort n=39: min **0.00h** · p25 **1.25h** · median **2.58h** ·
p75 **5.16h** · max **49.33h**.

**2b. Outcomes by bucket** — fixed buckets, not smoothed:

| 1H age | n | win | mean R | med R |
|---|---:|---:|---:|---:|
| < 1h | 8 | 75.0% | **+0.293** | +0.119 |
| 1–3h | 14 | 42.9% | −0.036 | −0.273 |
| 3–6h | 10 | 70.0% | **+0.370** | +0.200 |
| **≥ 6h** | 7 | 28.6% | **−0.584** | −1.076 |

Per side, split at 3h: SHORT `<3h` +0.262 (n=13) vs `≥3h` +0.091 (n=12); LONG `<3h` −0.174 (n=9) vs
`≥3h` −0.295 (n=5).

**2c. Shape.** **Not monotone — it zigzags.** `<1h` good, `1–3h` bad, `3–6h` good, `≥6h` bad. The
median split gives **+0.102 vs −0.023**, a spread of 0.13R on n=19/20 — nothing. **The only cell that
stands out is the `≥6h` tail at −0.584R on n=7**, and a 7-row tail in a 39-row sample is not a rule,
it is four losing trades.

**2d. 🔴 The two cases that defeat every other filter:**

```
vpos 86 : 1H age 3.83h -> 62nd percentile   ADX1h 11.38   R -1.022
vpos 91 : 1H age 2.66h -> 51st percentile   ADX1h 18.87   R -0.484
```

**Both sit in the middle of the distribution. Age does not identify either of them.**

---

## §3 — AGE AGAINST WHAT PRICE ACTUALLY DID SINCE THE SIGNAL

The first measure in any of these studies anchored to the **signal's own timestamp** rather than a
fixed lookback: efficiency ratio over the interval **[1H signal fired → fill]**, on 1h candles.
n=27 (entries whose 1H signal fired ≥2 candles before the fill).

ER distribution: min 0.051 · p25 0.129 · median **0.502** · p75 0.659 · max 0.908.

| ER since the signal fired | n | win | mean R | med R | sum R |
|---|---:|---:|---:|---:|---:|
| < 0.30 — chopped since | 8 | 50.0% | +0.096 | −0.024 | +0.77 |
| 0.30–0.60 | 10 | 70.0% | **+0.476** | +0.457 | +4.76 |
| ≥ 0.60 — moved cleanly since | 9 | 33.3% | **−0.341** | −0.440 | −3.07 |

**The middle bucket is best and both tails are worse.** Median split: +0.172 vs +0.015.

**Direction-aware — and it is inverted:**

| since the signal, price moved… | n | win | mean R |
|---|---:|---:|---:|
| **AGAINST** the eventual trade | 4 | 75.0% | **+0.315** |
| WITH the eventual trade | 23 | 47.8% | +0.052 |

**The cross-tab that tests the hypothesis directly:**

| | ER < median | ER ≥ median |
|---|---|---|
| **age < median** | n=4, **+0.624** | n=9, +0.287 |
| **age ≥ median** | n=9, **−0.028** | n=5, **−0.473** |

🔴 **The hypothesis predicted the worst cell would be "old signal + chopped since" (bottom-left). It
is −0.028R and the second-best of the four. The actual worst is "old signal + price moved cleanly"
(bottom-right, −0.473R, n=5) — the opposite.**

And on this measure the two flagged trades split apart rather than unifying: **vpos 86 ER 0.302
(30th pct)**, **vpos 91 ER 0.618 (67th pct)** — on opposite sides of the median.

**The mechanism does not hold. Not weakly — inverted, on n=27 with cells of 4–9.**

---

## §4 — THE TTL RULES, AND A LABEL THAT IS WRONG EVERY TIME

### The rules themselves are sound

`config.CATEGORY_TTL_MINUTES`:

| category | tier | TTL | set |
|---|---|---:|---|
| TREND | 1H | **360 min (6h)** | 2026-05-11 `adc44bc` |
| MOMENTUM | 15m | **90 min** | cut 240→90 on 2026-05-20 `aa16f7f` |
| LIQUIDITY | — | 30 min | 2026-05-11 |
| EXECUTION | 5m | 5 min | 2026-05-11 |

**Can an expired tier contribute to the score? No.** `signal_matrix.py:322` — `if age > _ttl_for(cat):
continue` — an expired signal is dropped from the matrix before scoring. The mechanism is correct.

### 🔴 But the explanation shown to the advisor is not

`signal_tiers.py:121` sets `counted_by_gate = (net_direction not in (None,'NEUTRAL'))`. A category's
net direction is NEUTRAL for **three** different reasons — TTL expiry, **intra-conflict**, or **no
signal at all**. `signal_tiers.py:187` renders **all three** as one sentence:

```
"NOT counted by the gate — matrix TTL expired"
```

Measured across all 87 rows carrying `entry_tiers_json`:

| the rendered reason | count | share |
|---|---:|---:|
| times "matrix TTL expired" was shown | **77** | 100% |
| …actually **INTRA-CONFLICT** (present, well inside TTL) | **70** | **91%** |
| …actually **no signal in that category** | **7** | 9% |
| …actually **TTL expiry** | **0** | **0%** |

**Not one occurrence is a TTL expiry.**

**vpos 91, the case in the question:**

```
15m tier: age shown to the advisor = "25m ago", counted_by_gate = False
  -> rendered as: "NOT counted by the gate — matrix TTL expired"
MOMENTUM in the matrix: L2.5  S1.75  sig=3  intra_conflict=TRUE
MOMENTUM TTL = 90 minutes.  The tier was 25 minutes old.
=> IT HAD NOT EXPIRED. The real cause was INTRA-CONFLICT.
```

The prompt showed the advisor **"25m ago"** and **"TTL expired"** in the same line, which cannot both
be true under a 90-minute TTL. **The advisor was given a self-contradicting fact and cited it.** So
did the question put to me. That is the cost of the mislabel: it propagates.

---

## §5 — VERDICT

**Age does not separate outcomes. Age weighted by what price did since the signal does not separate
outcomes — it separates in the opposite direction to the hypothesis.**

### Added to the dead branches — do not re-run these

| # | branch | why it is dead | n |
|---|---|---|---|
| 1 | **1H tier age** as an entry filter | non-monotone (`<1h` +0.29, `1–3h` −0.04, `3–6h` +0.37, `≥6h` −0.58); median split 0.13R; **both flagged trades sit at the 51st and 62nd percentile** | 39 |
| 2 | **5m tier age** | **zero variance** — it is the trigger, 0.00h on all 65 entries | 65 |
| 3 | **15m tier age** | **not reconstructible before 2026-07-26**; 7 of 65 covered | 7 |
| 4 | **ER over [signal → fill]** ("stale signal on a dead tape") | middle bucket best, both tails worse; **the predicted worst cell is second-best and the actual worst is its opposite** | 27 |
| 5 | **direction-aware move since signal** | inverted — price moving *against* the trade beforehand did better | 4 / 23 |

That is **five more dead branches on top of the five already recorded** (four `market_regime`
redefinitions, the ADX floor twice, ER at fixed 4h/12h, ATR-vs-median, intra-conflict as a range
proxy). **Ten measured attempts have now failed to identify the losing entries in advance.**

### What this study did find

**Not an entry filter — a defect.** The entry advisor is told "matrix TTL expired" on **77 of 77**
occasions when no TTL has expired, 91% of the time masking an **intra-conflict** and 9% masking an
absent signal. It is live, it is on the entry path, it fires on most entries, and it produced the
false premise inside the question I was asked.

**Nothing is proposed and nothing was changed.**
