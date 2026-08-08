# sol-paper-weights-measured-not-in-the-gate

_2026-08-08 14:17 UTC_

---

# Mercury-SOL — how much does the paper-trained weight actually move live decisions?

## 🔴 FIRST, A CORRECTION TO MY OWN 14:05 REPORT

My §2 said: *"`main.py:3605` does `adj_score = direction_score + _w_adj`, **which is what the entry
threshold compares**."* **That second clause is wrong.** `_w_adj` is not applied to the entry gate.

```python
# main.py:3596
# Weighted score adjustment — informational only (logged + stored as confluence_score);
# NOT applied to the gate, per weight_engine docstring.
...
adj_score = round(direction_score + _w_adj, 2)      # 3605 — stored, not gating
...
_thr        = _get_live_param('CONFLUENCE_SCORE_THRESHOLD', CONFLUENCE_SCORE_THRESHOLD)  # 3709
_gate_score = direction_score if MACRO_GATE_DRYRUN else _macro_gated_score               # 3710
if _gate_score < _thr:                                                                   # 3711
```

`_gate_score` is `_macro_gated_score` (`MACRO_GATE_DRYRUN = False`, `config.py:389`) = raw score +
macro penalty. **`_w_adj` is in neither branch.** The below-threshold card literally prints
`adj={...} → final={...} (info only)`. `weight_engine.py:17` states the policy: *"weighted_adj() is
NEVER applied to the raw direction_score that gates entry. Only the stored confluence_score uses it."*

I read the assignment on line 3605 and asserted the consequence without reading line 3710. The
underlying finding — the weight table is 100% paper-trained and re-trains daily — stands. The claim
that it steers the entry gate does not.

**So the direct answer to §4 is: this is WRONG, NOT URGENT. `_w_adj` has never flipped a live entry
verdict, because it is structurally incapable of reaching the gate.** The rest of this report is the
measurement you asked for — including what it *would* do if anyone ever wired it in, which is the
number that matters for the decision.

---

## 1. HOW OFTEN WOULD `_w_adj` CHANGE THE VERDICT?

**Actual: 0 times, on every signal ever scored.** It is not in the gate expression.

**Counterfactual — had it been applied**, over every scored signal in journald (300 signals,
2026-08-05 18:05 → 2026-08-08 11:55; the journal starts Aug 5 17:55, which bounds this window).
Threshold `CONFLUENCE_SCORE_THRESHOLD = 2.0`, no `params.json` override exists.

| | LONG | SHORT |
|---|---|---|
| signals scored | 139 | 161 |
| **raw vs final** — would ADMIT what raw refused | **15** | 2 |
| **raw vs final** — would REFUSE what raw admitted | 2 | **18** |
| **vs the true gate quantity** (raw+macro) — ADMIT | **10** | 2 |
| **vs the true gate quantity** — REFUSE | 7 | **22** |

**37 of 300 (12.3%) would have flipped** on your raw-vs-final framing; **41 of 299** against the
real gate quantity. The asymmetry is the story: the weights **let LONGs in** (15 admits vs 2
refusals) and **keep SHORTs out** (18 refusals vs 2 admits). That is a directional bias learned from
a paper book, and it points the same way as today's three LONG entries.

### (a) Live era only — since 2026-08-07 22:25:18

n=47 signals (22 LONG, 25 SHORT).

| | LONG | SHORT |
|---|---|---|
| raw vs final — ADMIT / REFUSE | **2** / 0 | 0 / **11** |
| vs true gate — ADMIT / REFUSE | **1** / 0 | 0 / **10** |

**11 of 47 (23%) would have flipped in the live era** — and every SHORT flip is a refusal. The
weights would have suppressed 10-11 SHORT entries in 40 hours while admitting 1-2 extra LONGs.

**Did today's two entries cross? No — neither, and not close:**

```
06:50:13 LONG raw=4.25 adj=+0.6215 final=4.87  macro= 0.0  gate=4.25  vs thr 2.0  CROSSED=False
08:35:11 LONG raw=3.75 adj=-0.4094 final=3.34  macro=-1.0  gate=2.75  vs thr 2.0  CROSSED=False
08:35:11 LONG raw=5.00 adj=-0.4094 final=4.59  macro=-1.0  gate=4.00  vs thr 2.0  CROSSED=False
08:50:08 LONG raw=4.50 adj=-0.6983 final=3.80  macro=-1.0  gate=3.50  vs thr 2.0  CROSSED=False
```

All four cleared the gate on raw score alone, by 0.75-2.25 points. The ±0.62/−0.41 you quoted never
mattered — both to the gate (excluded) and arithmetically (nowhere near the boundary).

### (b) Distribution of `_w_adj` — this is a decision-maker, not noise

| | all 300 | live era (47) |
|---|---|---|
| median | −0.3304 | −0.4253 |
| Q1 / Q3 | −0.9635 / +0.2197 | −0.5252 / +0.5815 |
| median \|adj\| | 0.5815 | 0.5252 |
| p90 \|adj\| | 1.5000 | 0.6983 |
| max \|adj\| | **1.5000** | **1.5000** |
| **\|adj\| > 0.10** | **278/300 = 92.7%** | **44/47 = 93.6%** |
| \|adj\| > 0.50 | 172 (57%) | 30 (64%) |
| \|adj\| > 1.00 | 104 (35%) | 5 (11%) |

By your own test — *"never exceeds ±0.1 is noise; regularly moves ±0.6 is a decision-maker"* — this
is emphatically **a decision-maker**: 93% of signals exceed ±0.1, the median absolute value is
±0.58, and it hits the ±1.5 clip (`weight_engine.py:192`) on 35% of all signals. Against a threshold
of 2.0, a ±1.5 term is 75% of the entire bar. **It is only harmless because it is not connected.**

---

## 2. WHAT MOVES A WEIGHT — DOLLARS, AND THE ANSWER IS WORSE THAN "MORE THAN A STOP-OUT"

### (a) The constants (`weight_engine.py:35-41`)

```python
LEARNING_RATE     = 0.10
BASELINE_WIN_RATE = 50.0
PNL_NORMALIZATION = 20.0   # ← USD
MIN_WEIGHT        = 0.20
MAX_WEIGHT        = 2.50
MIN_SAMPLE        = 5

win_signal = (win_rate − 50) / 100          → size-NEUTRAL
pnl_signal = tanh(avg_pnl / 20.0)           → DOLLARS
gradient   = 0.10 × (0.6×win_signal + 0.4×pnl_signal)
```

**It is a hybrid, and that distinction matters.** 60% of the gradient is win-rate — a $100 live trade
moves it exactly as much as a $10,000 paper trade. Only the 40% PnL half is dollar-denominated. So
this is *not* Titan's §2.40 case of a fully inert mechanism; it is a mechanism that goes **40% deaf**
at live size.

### (b) At $100 live notional

Measured: paper notional median **$9,994** (range $6,662-$10,000); live notional **$97.24**. That is
**103× — not 68×.** Live 1R = 1.3 × (74.80 − 73.89) = **$1.183**.

| | avg_pnl | pnl_signal | PnL half of gradient |
|---|---|---|---|
| paper trade (observed) | −$43.10 | −0.9735 | −0.03894 |
| paper trade (observed) | −$77.66 | −0.9992 | −0.03997 |
| **LIVE full stop-out (−1R)** | **−$1.18** | **−0.0591** | **−0.00236** |
| LIVE +5R win | +$5.91 | +0.2874 | +0.01150 |
| LIVE +10R win | +$11.83 | +0.5310 | +0.02124 |

**To match one typical paper trade's PnL signal, a live trade needs $43.07 = 36.4R.** To reach even
half-saturation of the tanh: **9.3R**. A full stop-out is 1R.

**So yes — the answer is "more than a full stop-out", by a factor of 36.** A live stop-out moves the
PnL half **16.5× less** than one paper trade. The paper trades sit at tanh saturation (−0.97 to
−0.999); live trades sit in the linear near-zero region.

**Consequence, stated as you framed it:** the moment paper stops accumulating, the PnL half of the
gradient effectively freezes at its paper values. It will not *fully* freeze, because the win-rate
half still moves — but a live cohort would need to out-vote a saturated paper history using only 60%
of the gradient, on a set of segments where **9 of 18 are already pinned at the `MIN_WEIGHT` floor of
0.20** and cannot go lower.

---

## 3. WHAT FREEZING OR NEUTRALISING WOULD COST

Current state of `optimizer/dynamic_weights.json` (rewritten 14:00:03 today):

```
18 segments — 18/18 (100%) are OFF the 1.0 baseline
weight range 0.200 .. 2.104   median 0.211
9 of 18 PINNED AT THE FLOOR (MIN_WEIGHT 0.20).  0 at the ceiling.
every avg_pnl driving them is paper money (all 22 closed rows are is_paper=1)
```

Most-displaced: `mc_funding_rate:funding_negative` **2.104** (n=9, +$30.60 avg);
`dxy_trend:STRONG_UPTREND`, `ema_status_1h:Bearish`, `ema9_slope_state_1h:Inclined_Up`,
`news_overall:POS`, `mtf_alignment_score:mtf_3`, `mc_funding_rate:funding_low`,
`ema_status_15m:Bullish`, `ema_status_1h:Bullish`, `macro_news_category:CRITICAL_NEGATIVE` — all
**0.200, floored** (−0.800 each).

### (a) Stop the timer

Weights freeze at today's paper values and keep influencing **what they already influence** — which,
per the correction above, is *not* the entry gate. What they do feed:

- **the stored `confluence_score`** on every row;
- **the optimizer's own `_bucket_confluence` segmentation** — a feedback loop where paper-weighted
  scores define the buckets the optimizer then learns from;
- **`claude_advisor.consult_for_learning`** — the POST-trade attribution consult receives
  `confluence_score` (`claude_advisor.py:1197`). Note the *entry* consult explicitly **dropped** it
  (D5c 2026-06-08, Titan parity, `claude_advisor.py:477`), so the AI entry veto does not see it.

Cost: zero entry verdicts change. The learning loop stays paper-anchored.

### (b) Neutralise `_w_adj` at the gate

**This is already the shipped behaviour — the change is a no-op at the gate.** Titan's accidental
behaviour is SOL's *documented* behaviour (`weight_engine.py:17`, `main.py:3596`).

**Entries whose verdict changes: 0 of 300.**

If you mean instead *stop adding it to the stored `confluence_score`*, the measurable cost is the
optimizer's bucketing:

```
all 300 journal signals : optimizer bucket changed by _w_adj in  21 (7.0%)
live era (47)           : optimizer bucket changed by _w_adj in   4 (8.5%)
```

The buckets are `<6.0 / 6.0-7.5 / 7.5-9.0 / >=9.0`, so only signals near 6.0 can move. Max final in
the live window was 8.25.

### (c) Live-only cohort

**It would not reset anything to 1.0 — it would freeze at today's paper values, identically to
option (a).** With 0 closed live rows and `MIN_SAMPLE = 5`, no segment qualifies for an update, so
the optimizer writes nothing and the existing file stands. Getting to a 1.0 baseline requires
clearing the file as a separate act.

**And clearing it does NOT zero `_w_adj`.** `get_weight()` returns 1.0 for an unknown segment
(`weight_engine.py:169-174`), so at baseline `_w_adj` becomes the **unweighted sum of the base
constants** — `_EMA_CROSS_BASE 0.20`/TF, `_EMA_SLOPE_BASE 0.10`/TF, `_NEWS_BASE 0.20`, MTF ±0.20,
funding ±0.10, DXY up to ±0.50 — still a term of order ±1.

🔴 **The counter-intuitive part: resetting to 1.0 makes `_w_adj` BIGGER, not smaller.** Nine of the
eighteen segments are floored at 0.20, i.e. their contribution is currently scaled to **one fifth**.
Restoring them to 1.0 multiplies those contributions by **5×**. The paper training has mostly been
*suppressing* this term; a reset un-suppresses it.

Combos currently off 1.0: **18 of 18.**

---

## 4. 🔴 URGENT, OR MERELY WRONG?

**Merely wrong. Not urgent. The timer firing tomorrow at 14:00 UTC cannot change a live entry
verdict.**

The evidence: `_w_adj` is excluded from the gate expression by design, in code, in the docstring, and
in the card text; today's four scored LONG signals all cleared on raw score by 0.75-2.25 points; and
`_w_adj` has never appeared in any branching decision anywhere in the tree — only in storage,
display, the optimizer's own bucketing, and the post-trade learning consult.

**What is genuinely wrong, and worth fixing calmly:**

1. The weight table is **100% paper-trained** — all 22 closed rows are `is_paper=1` — and re-trains
   daily on a book that is **103× the live notional**.
2. It is **loaded and ready**: median |adj| 0.58, hitting the ±1.5 clip on 35% of signals, against a
   threshold of 2.0. It carries a directional bias (admits LONGs, refuses SHORTs) that, if ever
   connected, would have flipped **23% of live-era signals**.
3. The guard that was supposed to cover this rests on a premise that **expired at the flip** —
   `optimizer.py:101` says "SOL runs in OBSERVATION_MODE" and it does not.
4. The PnL half of the learning signal is **dollar-denominated** and goes 16.5× deaf at live size,
   so live results cannot out-vote the paper history on that channel — while 9 of 18 segments are
   already floored and cannot move down at all.
5. The `is_virtual` cohort filter is absent in live mode, so **once live trades start closing they
   will be pooled with paper rows** in the filter-proposal path. That one is a live-fire defect
   waiting for the first closed live trade — and it is the only item here with a deadline.

**The gap between "wrong" and "urgent" is one line of code** — anyone adding `_w_adj` to
`_gate_score`, or flipping the gate to compare `adj_score`, converts every number in §1 from
counterfactual to real, instantly.

Nothing was changed. Every call in this pass was a read. Titan untouched.
