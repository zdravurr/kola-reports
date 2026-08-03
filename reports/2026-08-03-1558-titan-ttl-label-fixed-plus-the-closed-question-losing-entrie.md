# titan ttl label fixed plus the closed question losing entries not identifiable in advance

_2026-08-03 15:58 UTC_

---

# TITAN — THE TIER THAT DID NOT COUNT NOW SAYS WHY · AND A CLOSED QUESTION

_2026-08-03 16:10 UTC · HEAD `6d9281d` (was `489e0ac`) · LIVE, flat · one file, +85/−2_

---

## DECISION LINE

**Applied.** Four strings for four states, the real reason **captured into `entry_tiers_json`** so it
cannot be re-derived wrongly later, and the TTL minutes read from `config` so the printed number
cannot drift from the one that actually expires a signal.

**Close prompt byte-identical (md5). Gate arithmetic untouched. Freeze confirmed.**

🔴 **First, a correction to my own 16:05 report, stated before anything else.** It said the label was
wrong **77 of 77** — 0 genuine TTL expiries, 7 "no signal in the category". Splitting on the slot's
`present` flag shows those **7 are GENUINE TTL expiries**: the state-machine slot still holds the
signal, and the matrix dropped it on its own TTL (e.g. trade 19464's 15m tier, `HyperWave Signal
Down`, **2.8h old against a 90-minute MOMENTUM TTL**). **The honest split is 70 wrong / 7 right, not
77 / 0.** My earlier classifier could not tell "matrix has no signal because it expired" from "no
signal ever arrived", and I reported the weaker of the two as fact.

**The defect is still large and still real: 70 of 77 (91%).**

---

## 1. WHAT CHANGED

### Before — one sentence for three states

```
15m: HyperWave OS Signal Up  (LONG, weight 1.0, last set 25m ago,
     NOT counted by the gate — matrix TTL expired)
```

**"25m ago" and "TTL expired" on the same line, under a 90-minute MOMENTUM TTL.** Two facts that
cannot both be true.

### After — the actual reason, on vpos 91's real stored facts

```
15m: HyperWave OS Signal Up  (LONG, weight 1.0, last set 25m ago,
     NOT counted by the gate — this category's own signals disagree
     (LONG 2.50 / SHORT 1.75 across 3 signals), so it nets NEUTRAL)

5m:  Bearish OB Created  (SHORT, weight 0.5, last set 0m ago, trigger-capable,
     NOT counted by the gate — this category's own signals disagree
     (LONG 2.50 / SHORT 2.50 across 4 signals), so it nets NEUTRAL)
```

### The four strings

| state | rendered |
|---|---|
| **intra-conflict** | `NOT counted by the gate — this category's own signals disagree (LONG 2.50 / SHORT 1.75 across 3 signals), so it nets NEUTRAL` |
| **TTL expired** | `NOT counted by the gate — the matrix expired this signal on its category TTL (MOMENTUM TTL 90 min); the state-machine slot still holds it` |
| **absent** | `NOT counted by the gate — no signal in this category` |
| unrecognised | `NOT counted by the gate — the category nets NEUTRAL` |

The last one is the fallback: **vaguer than the truth, never a false reason.**

### Where the reason comes from

`build()` reads it from the matrix breakdown at capture time and stores it as `not_counted` (plus
`not_counted_detail` carrying the L/S split and signal count). **It is persisted into
`entry_tiers_json`, so this is a data improvement, not only a display one** — a later reader gets the
recorded reason instead of re-deriving it and getting it wrong the same way.

`render()` performs a lookup. **It never re-derives.**

TTL minutes come from `config.CATEGORY_TTL_MINUTES`, so the number in the sentence and the number
that expires the signal are the same object.

---

## 2. FACTS, NOT JUDGEMENT

Each string states what the bot's own registers hold — the L/S point split, the signal count, the
TTL window, whether the slot still holds the signal. **No win rate, no PnL, no hint that disagreement
is bad or that a fresh tier is good.** The advisor learns **why** the gate did not count a tier and
is told **nothing** about what that implies.

Same line already drawn by `f0a8d30` (1H identity: name and direction, never performance),
`8b15ecc` (book percentiles: *"CALIBRATION ONLY"*) and `a85733f` (the combo weight: count, date and
size, no verdict). **Four prompt changes, one rule.**

---

## 3. FREEZE CHECK — CONFIRMED, ENTRY SIDE

§2.4-OP freezes every figure rendered into the **close** prompt and states the **entire entry side is
not frozen**.

`signal_tiers` feeds **both** prompts, so this needed checking rather than asserting:

| function | feeds | reads `counted_by_gate` / `not_counted`? |
|---|---|---|
| `render()` | the **ENTRY** prompt | yes — this is what changed |
| `entry_thesis_lines()` | the **CLOSE** prompt's entry-thesis block | **0 references** — it prints name, direction, weight, age only |

Verified by md5, before and after:

```
entry-thesis block : e680a2a19a0aa66a59756d476b19da56  ==  e680a2a19a0aa66a59756d476b19da56
full close prompt  : de845c0994e21c54fb0659012832f8b0  ==  de845c0994e21c54fb0659012832f8b0
```

⚠️ Note the new `not_counted` field **does** land in `entry_tiers_json`, which the close path reads —
but `entry_thesis_lines` ignores it, which is why the rendered close prompt is unchanged. **The
window is not voided and needs no restatement.**

---

## 4. GATE ARITHMETIC UNTOUCHED

```
git diff --numstat  ->  85  2  titan-bot/signal_tiers.py      (the only file)
signal_matrix.py is NOT in the diff.
signal_matrix.py:322  ->  if age > _ttl_for(cat): continue    (unchanged)
```

**The mechanism is correct and stays exactly as it is:** an expired signal is dropped from the matrix
before scoring, so it cannot contribute. `CATEGORY_TTL_MINUTES` is unchanged — TREND 360, MOMENTUM
90, LIQUIDITY 30, EXECUTION 5. **Only the rendered explanation changed.**

**Deployed** 15:56:49 UTC from flat. Four boot gates green, zero errors.

---

# 5. 🔴 CLOSED QUESTION — RECORDED AS OPEN-ITEMS §2.45

## **THE LOSING ENTRIES ARE NOT IDENTIFIABLE IN ADVANCE ON THIS DATA**

**Ten measured attempts. All documented. All negative.**

| # | branch | result | n |
|---|---|---|---:|
| 1–4 | **four `market_regime` redefinitions** | all four still took the losing trade | — |
| 5 | **ADX floor**, 1st measurement (07-30) | sub-floor entries were the **BEST** cell (−0.02R vs −0.32R) | — |
| 6 | **ADX floor**, 2nd measurement (08-03) | holds — ADX1h <20 **not** worst (n=7, −0.112R); **20–25 best** (n=14, +0.167R); **ADX4h <20 is the best 4h cell** (n=11, +0.250R) | 39 |
| 7 | **efficiency ratio, fixed 4h / 12h** | flat: +0.066 vs +0.010 · −0.031 vs +0.102 | 39 |
| 8 | **ATR(1h) vs its own 14-day median** | flat: +0.002 vs +0.072 | 39 |
| 9 | **intra-conflict as a range proxy** | rejected four ways; **χ² ≤ 1.24**, and the **sign REVERSES** between the 4h and 12h windows | 65 |
| 10a | **1H tier age** | non-monotone: `<1h` +0.293 · `1–3h` −0.036 · `3–6h` +0.370 · `≥6h` −0.584 | 39 |
| 10b | **5m tier age** | **zero variance** — it is the trigger, 0.00h on all 65 | 65 |
| 10c | **15m tier age** | **not reconstructible before 2026-07-26** | 7 |
| 10d | **ER over [signal fired → fill]** | **INVERTED** — predicted-worst cell is 2nd best (−0.028R); actual worst is "old **and** price moved cleanly" (−0.473R) | 27 |

### The two flagged trades defeat all ten

- **On age** they sit at the **51st and 62nd percentile** — the middle of the distribution.
- **On ER-since-signal** they land on **opposite sides of the median** (vpos 86 at the 30th, vpos 91
  at the 67th) — so no single threshold covers both.
- **vpos 86 carries one of the highest scores in the book (5.75), with ZERO intra-conflicts, three
  agreeing categories, at ADX(1h) 11.12.** It passes every filter ever considered. It lost 1.02R.

### 🔴 What would change this — and it is the only thing that would

**Live-era observations.** The clean cohort is **39, of which 34 are paper**. The live era holds
**5–6**. Every positive cell that motivates any rule rests on paper trades at **68× the notional**,
and in the live era the no-conflict cell — the one worth +0.536R — is **empty**.

At the measured rate of **1.5 entries per active day**, **30 live entries is roughly three weeks.**

**Until that sample exists: do not re-run these branches, and do not fit a threshold to n=39.**

---

## WHAT CHANGED, AND WHAT DID NOT

| | |
|---|---|
| **Code** | `signal_tiers.py` only — **+85/−2**, commit `6d9281d`, live 15:56:49 |
| **Snapshot** | `signal_tiers.py.bak_ttllabel_20260803` |
| **Close prompt** | **byte-identical** (md5), §2.4 window not voided |
| **Gate arithmetic / TTL values** | **untouched** — `signal_matrix.py` not in the diff |
| **DB** | no writes; the new field appears on *future* `entry_tiers_json` rows only |
| **Historical rows** | not backfilled — the 87 existing records keep their old shape |
| **Position** | flat throughout |
| **§1d · §3 drift · §2.40/§2.41 · retire `entry_wall_baseline_mult`** | still deferred per §2.42a |
