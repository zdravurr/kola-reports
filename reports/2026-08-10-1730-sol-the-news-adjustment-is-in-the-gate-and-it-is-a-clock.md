# sol-the-news-adjustment-is-in-the-gate-and-it-is-a-clock

_2026-08-10 17:30 UTC_

---

# 🔴 IT IS IN THE GATE. IT FLIPS 9.1 % OF ALL VERDICTS. AND IT DOES NOT SURVIVE THE CLOCK.

**But the entry that triggered this brief was not decided by a headline — and three of the
brief's own numbers do not survive contact with the source.** Both halves are below, in that
order, because §1 said establish it before anything else.

```
§1  IS IT IN THE GATE?      YES — proved three ways, one of them live at 15:25 TODAY.
                            The DXY half is NOT. There is no DXY term in the gate at all.
§2  HOW OFTEN DOES IT DECIDE?  487 of 5,355 verdicts flipped (9.1 %). 7 of 167 live-era.
                            But only 2 of 31 rows that ever became an order, and 1 of 25
                            closed positions.
§3  DOES IT SEPARATE OUTCOMES? NO. Paper n=22 shows no separation; live n=3 is one row per
                            bucket. Refused to pool across four boundaries.
§4  THE REFUSAL COHORT      21 of 54 cells clear Bonferroni RAW.  🔴 0 of 54 survive
                            day-matching. news+ and news− drift the SAME way — the tell.
§5  THE PIPELINE            The classifier is INSTRUCTED to score BTC and to file
                            SOL-specific news as NEUTRAL. It is trading SOL.
§6  VERDICT                 It sits inside the noise. NOTHING PROPOSED, NOTHING CHANGED.
```

Prior: [2026-08-09 19:20 — the boot card stops lying](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1920-sol-the-boot-card-stops-lying-and-the-whole-class-is-swept.md) ·
[2026-08-08 14:17 — the paper weights, measured, not in the gate](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1417-sol-paper-weights-measured-not-in-the-gate.md)

---

## 0. 🔴 THE TRIGGER, CORRECTED BEFORE IT IS ANSWERED

The brief describes *"a LONG opened 2026-08-10 ~11:14 UTC at 76.96, $20 margin x5"* whose score
was lifted `4.50 → 6.00` by DXY and a Robinhood headline. **The position is real and the card
is quoted accurately. Three things about it are not what they look like.**

### (a) It opened at 08:10:20 UTC, and it is already closed — at a loss

```
2026-08-10T08:10:21  [LIVE-BOOK] vpos=31 BOOKED is_paper=0 LONG size=1.2 @ 76.96 sl=75.91 1R=$1.26
2026-08-10T15:21:44  [VIRTUAL] CLOSE vpos=31 LONG entry=76.96 exit=75.9 size=1.2
                     gross=-1.2720 fees=0.1834 net=-1.4554 reason=sl  (close_row=17296)
```

`trades` row **17201**, vpos **31**, **−$1.4554 = −1.155R**, stopped out. Seven hours and eleven
minutes, not three. Whatever this term is worth, this trade has already paid its own answer.

### (b) 🔴 `adj +1.50 → 6.00` IS NOT THE NEWS ADJUSTMENT. It is the paper-trained weight term — the one proved on 2026-08-08 to be OUTSIDE the gate

```
2026-08-10T08:10:11 [MERCURY-SOL] weighted_adj: dir=LONG raw=4.50 adj=+1.5000 final=6.00
   breakdown={'ema_cross_15m': 0.04, 'ema_cross_1h': 0.04, 'ema_slope_15m': 0.02,
              'ema_slope_1h': 0.02, 'dxy': 0.2234, 'news': 0.04, 'mtf': 0.02,
              'funding': 0.0, 'macro_category': 2.0}
```

The card's `📊 Score: 4.50 adj +1.50⚖️ → 6.00` is rendered at `main.py:4965` (tag built at
`:4883`) from `_w_adj` and
`adj_score` — **`weight_engine.weighted_adj`, clipped at ±1.5, informational only.** It is
stored as `confluence_score` and shown; it is in neither branch of the gate expression. That was
established on 2026-08-08 and is unchanged.

**The news adjustment is the OTHER number on the same card, and it is +1.00, not +1.50:**

```
📰 STRONG_POSITIVE → LONG +1.0 | "Robinhood brings crypto trading to UK…" | score 4.5→5.5
```

`4.5→5.5` is `macro_filter.news_impact_line(ctx, direction, direction_score, _macro_gated_score)`
— **the raw score and the deciding score, printed side by side.** The card already told you the
right answer; it sits three lines above the wrong one.

### (c) 🔴 DXY CONTRIBUTES ZERO TO THE GATE. There is no DXY term in it

```python
# macro_filter.py:477
ctx['total_gate_adj'] = round(
    ctx['crypto_gate_adj'] + ctx['macro_gate_adj'], 4
)
```

Two terms: **crypto news** and the **scheduled-macro blackout window**. `dxy_value` and
`dxy_trend` are fetched, stored and displayed — and never summed into anything the gate reads.
The card line the brief quotes,

```
🌍 MACRO: DXY=99.64 (DOWNTREND) | adj=+1.0pts
```

is `macro_filter.telegram_line:524` — `f"DXY={dxy_str} | adj={adj_str}"`, where `adj_str` is
`total_gate_adj`. **The DXY reading and the total adjustment share one line separated by a pipe;
they are not related.** That `+1.0` is the same news point printed on the NEWS line below it, not
a second one. DXY does appear as `+0.2234` inside `_w_adj` above — the term that is not in the gate.

### 🔴 So: was a third of the deciding score a headline?

```
raw direction_score              4.50   ← price
news (STRONG_POSITIVE, LONG)    +1.00   ← headline
DXY                              0.00   ← nothing
                                -----
_gate_score                      5.50   vs CONFLUENCE_SCORE_THRESHOLD = 2.0
```

**18 %, not a third — and it did not decide.** The raw score cleared the bar by **2.50 points**
on its own. Remove the headline entirely and this position still opens, still stops out, still
loses $1.4554.

**None of which makes the alarm wrong to raise.** The term is in the gate, it is large, and it
has never been measured. The rest of this file is that measurement.

---

## 1. IS IT IN THE GATE? — PROVED THREE WAYS

### (a) The gate comparison, verbatim

```python
# main.py:4372-4374
_thr = _get_live_param('CONFLUENCE_SCORE_THRESHOLD', CONFLUENCE_SCORE_THRESHOLD)
_gate_score = direction_score if MACRO_GATE_DRYRUN else _macro_gated_score
if _gate_score < _thr:
```

```python
# config.py:399
MACRO_GATE_DRYRUN = False   # A7 2026-06-08: apply macro penalty at gate (Titan parity)
```

```python
# main.py:4232-4234
_macro_ctx         = macro_filter.build_macro_context(direction)
_macro_gate_adj    = _macro_ctx['total_gate_adj']
_macro_gated_score = round(direction_score + _macro_gate_adj, 2)
```

**`_gate_score` holds the MACRO-GATED score.** Not raw, not weight-adjusted.
`MACRO_GATE_DRYRUN` is `False`, so the ternary takes the second branch every time.

### (b) The trace: computed at 4233, compared at 4374, nothing in between discards it

`build_macro_context` (4232) → `total_gate_adj` (4233) → `_macro_gated_score` (4234) →
persisted to `trades.macro_gate_penalty` (4241) → **`_gate_score` (4373) → `if _gate_score < _thr`
(4374)**. Unlike `_w_adj`, which is assigned at 4268 and appears in the gate expression **nowhere**,
`_macro_gated_score` is *literally the right-hand side of the branch that decides*.

### (c) 🔴 AND IT IS PROVED IN THE DATA, NOT ONLY IN THE SOURCE — which is the check I failed on 2026-08-08

Reading a second line is not proof; it is a second reading. So the verdict stored on every
row was predicted from `raw + penalty` and compared with what the bot actually did:

```
rows that reached build_macro_context           5,707
raw score recoverable                           5,355
  predicted verdict == stored verdict           5,355   ✅
  MISMATCHES                                        0
```

**If the gate compared the raw score, 487 of those 5,355 rows would be inconsistent** — those are
exactly the rows where raw and gated fall on opposite sides of 2.0. Zero are. The gate uses the
adjusted quantity, over 63 days and 5,355 decisions.

**And it fired today, two hours before this file was written:**

```
row 17299   2026-08-10 15:25:07   SHORT   raw=2.50  pen=-1.0  ->  1.50
            stored status = below_threshold
            🔴 raw alone would have ADMITTED it. The headline refused it.
```

### (d) Provenance of every raw score used above — no quantity travels without it

| status | n | where the RAW score came from |
|---|---|---|
| `below_threshold` | 1,878 | `skip_attribution.confluence_score` (`main.py:4385` passes `direction_score`) |
| `ai_skipped` | 3,390 | `skip_attribution.confluence_score` (`main.py:4815` passes `direction_score`) |
| `executed` / `observed_skipped` | 81 | `trade_signal_matrix.score` — written by `signal_matrix.snapshot` at `main.py:4867`, **before** the executed-row update overwrites `confluence_score` with `adj_score` at 4895 |
| `failed` / `sl_failed_position_closed` / `claude_unavailable` | 6 | `trades.confluence_score` — these paths write `direction_score` (4849, 4859) |
| `risk_halt` / `entry_gate_refused` | **352** | 🔴 **NOT RECOVERABLE** — both write `adj_score` and neither writes `weighted_adj` |

🔴 **The 352-row gap is stated, not papered over.** Bounded by `|_w_adj| ≤ 1.5`
(`weight_engine.py:289` — `total = round(max(-1.5, min(1.5, total)), 4)`), **at most 53** of them
could be flips. So §2's all-time flip count is
**487, and at most 540** — 9.1 % to 9.5 %. Every number below uses the 5,355 with a known raw score.

### (e) 🔴 THE SOURCE ITSELF SAYS THE OPPOSITE, IN THREE PLACES, IMMEDIATELY ABOVE THE CODE

This is the trap the brief warned about, planted in the tree:

```python
# config.py:396-398 — directly above MACRO_GATE_DRYRUN = False
# MACRO_GATE_DRYRUN: Mercury-SOL ships this gate in DRYRUN — build_macro_context
# is computed, logged, and persisted to trades.db, but the would-be adjustment
# is NOT applied at the score gate. Flip to False to apply it (Titan behaviour).
```

```python
# main.py:4199-4200
# fetches are TTL-cached; every branch fails open. weighted_adj remains
# STORAGE-ONLY — the score gate still uses raw direction_score (gate UNCHANGED).
```

```python
# macro_filter.py:37-40 (module docstring)
# Mercury-SOL wiring: the gate adjustment is computed and logged behind
# MACRO_GATE_DRYRUN (config). In DRYRUN it does NOT modify the entry gate…
```

**Anyone answering "is macro in the gate?" by reading prose gets NO three times.** The flag was
flipped on 2026-06-08 and the three comments describing the old behaviour were never touched.
`main.py:4200`'s clause *"the score gate still uses raw direction_score"* is simply false —
correct about `weighted_adj`, wrong about the gate. **Recorded, not fixed: this pass changes nothing.**

### (f) One more path, currently inert, that a future CONFIRM would arm

`macro_news_category` is an **ORIGINAL_6** key in `filter_enforcement` (`main.py:4302`), and
ORIGINAL_6 matches **HARD-BLOCK regardless of `FILTER_ENFORCEMENT_DRYRUN`** (`main.py:4331-4342`).

```
optimizer/filters.json   DOES NOT EXIST   -> zero filters -> inert today
```

**If the optimizer ever proposes and you ever CONFIRM a filter keyed on `macro_news_category`
or `dxy_trend`, news stops being a ±1.0 voice and becomes a veto that no threshold can outvote.**
Named here because it is a second door, not because it is open.

---

## 2. HOW OFTEN DOES IT DECIDE?

### (a) All time — 2026-06-08 → 2026-08-10, threshold 2.0

| | LONG | SHORT | TOTAL |
|---|---:|---:|---:|
| signals with a known raw score | 2,514 | 2,841 | **5,355** |
| **ADMITTED** what raw would have refused | 72 | 141 | **213** |
| **REFUSED** what raw would have admitted | 154 | 120 | **274** |
| **flip rate** | | | **487 / 5,355 = 9.1 %** |

**The asymmetry is the opposite of the weight table's.** `_w_adj` lets LONGs in and keeps SHORTs
out; the news term **refuses LONGs 2.1× more often than it admits them** (154 vs 72) and **admits
SHORTs more often than it refuses them** (141 vs 120). Mechanically obvious once stated: bullish
crypto headlines outnumber bearish ones in this feed, and `STRONG_POSITIVE` *penalises* SHORT
while `CRITICAL_NEGATIVE` *rewards* it.

### (b) Live era — since 2026-08-07 22:25:18

| | LONG | SHORT | TOTAL |
|---|---:|---:|---:|
| signals with a known raw score | 54 | 113 | **167** |
| ADMITTED what raw would refuse | 0 | 2 | **2** |
| REFUSED what raw would admit | 0 | 5 | **5** |
| flip rate | | | **7 / 167 = 4.2 %** |

🔴 **Today's entry is NOT one of them.** Named individually, all seven, all SHORT:

```
ADMIT   row 17051  2026-08-09 13:10:02  SHORT  raw=1.75  +1.0 -> 2.75  CRITICAL_NEGATIVE  -> ai_skipped
ADMIT   row 17060  2026-08-09 14:00:04  SHORT  raw=1.75  +1.0 -> 2.75  CRITICAL_NEGATIVE  -> ai_skipped
REFUSE  row 16777  2026-08-08 11:00:02  SHORT  raw=2.00  -1.0 -> 1.00  STRONG_POSITIVE
REFUSE  row 16843  2026-08-08 19:20:00  SHORT  raw=2.50  -1.0 -> 1.50  STRONG_POSITIVE
REFUSE  row 17062  2026-08-09 14:40:00  SHORT  raw=2.50  -1.0 -> 1.50  STRONG_POSITIVE
REFUSE  row 17072  2026-08-09 16:00:01  SHORT  raw=2.00  -1.0 -> 1.00  STRONG_POSITIVE
REFUSE  row 17299  2026-08-10 15:25:07  SHORT  raw=2.50  -1.0 -> 1.50  STRONG_POSITIVE
```

🔴 **BOTH live-era admits were then killed by the AI advisor.** The news term let them through the
score gate and the advisor refused them anyway. **In the live era the macro adjustment has admitted
exactly ZERO positions and refused five, all on the short side.**

### (c) Distribution — a decision-maker by your own test, but a two-state one

| | all time (5,707) | live era (217) |
|---|---|---|
| median | 0.00 | 0.00 |
| Q1 / Q3 | 0.00 / 0.00 | 0.00 / 0.00 |
| max abs | **3.50** | 1.00 |
| **\|adj\| > 0.10** | **2,734 / 5,707 = 47.9 %** | 82 / 217 = 37.8 % |
| \|adj\| ≥ 1.00 | 2,734 (47.9 %) | 82 (37.8 %) |

```
value counts, all time:   −3.5 : 9    −2.5 : 8    −1.5 : 2
                          −1.0 : 1,383   0.0 : 2,973   +1.0 : 1,332
```

🔴 **It has no small values.** Those two rows are identical — nothing ever lands between 0 and 1.0.
It is not a continuous nudge; it is a **switch that is off 52 % of the time and worth ±1.0 the
other 48 %**, against a threshold of **2.0**.

**By the brief's own test — "rarely exceeds ±0.2 is noise; regularly moves ±1.5 against a
threshold of 4.0 is a decision-maker" — this is a decision-maker: it moves ±1.0 against a
threshold of 2.0, which is 50 % of the entire bar, on nearly half of all signals.**

### (d) 🔴 AND YET IT HAS BUILT ALMOST NOTHING

The flip rate is a rate over *signals*. Over *orders* it collapses:

```
rows that ever became — or nearly became — a live order : 31
  of those, rows whose verdict the macro adjustment FLIPPED :  2
    row  4052  2026-06-23  SHORT  raw=1.75 +1.0 -> 2.75   observed_skipped (paper, no order)
    row 14988  2026-08-01  SHORT  raw=1.75 +1.0 -> 2.75   executed -> vpos 25
```

**One position in this bot's entire history exists because of this term.** The gap between 9.1 %
of verdicts and 1 of 31 orders is the AI advisor and the cascade downstream: almost everything the
news term admits at the score gate is refused again by something else.

---

## 3. DOES IT SEPARATE OUTCOMES?

### 🔴 (d) FIRST — THE BOUNDARIES, DECLARED BEFORE ANY POOLING

| | boundary | what it forbids |
|---|---|---|
| **B1** | book: `is_paper=1` (vpos 7–28, n=22) vs `is_paper=0` (vpos 29–31, n=3) | notional 105× apart — **not pooled** |
| **B2** | taker fee: vpos ≤29 understated 1.82×; vpos ≥30 read from the venue | **cuts inside the live set** — vpos 29 not pooled with 30/31 on any fee-sensitive statistic |
| **B3** | ADX window: vpos ≤28 = 42, vpos ≥29 = 200 | an entry **feature**, not an outcome — does not bind here, stated so it is not silently assumed to |
| **B4** | funding: `funding_paid` populated only from vpos 30 | vpos ≤29 R excludes funding; 30/31 include it |
| **B5** | exit advisor: live (DRYRUN) from `trades` row 17082 | only **vpos 31** was managed under it — its exit is not comparable to 29/30 |

**What was pooled:** the 22 paper rows with each other; nothing else.
**What was refused:** paper↔live; vpos 29↔30/31 on fees; any claim spanning B5.

🔴 **And a provenance note on vpos 29.** Its entry row **16767 has `status='failed'`** — it is the
orphan the bot adopted on 2026-08-08. On that path `confluence_score` holds the **raw** score and
`weighted_adj` was never written, so its 4.50 is a raw score where vpos 30/31's 4.92/6.00 are
adjusted ones. **Its macro context is valid** (written at enrichment, before the order threw).

### (a) By the NEWS component — PAPER cohort (n=22)

| cell | n | win | ΣR | median R |
|---|---:|---:|---:|---:|
| news **positive** for this side | 8 | 3/8 (38 %) | **−1.733** | −0.618 |
| news **zero** | 11 | 4/11 (36 %) | **−2.429** | −0.739 |
| news **negative** | 3 | 1/3 (33 %) | **−1.212** | −0.153 |

Per side:

```
LONG  news+  n=1   −1.074        SHORT news+  n=7  3/7  ΣR −0.659  med −0.577
LONG  news0  n=7   ΣR −1.909     SHORT news0  n=4  2/4  ΣR −0.520  med −0.293
LONG  news−  n=1   −1.064        SHORT news−  n=2  1/2  ΣR −0.149  med −0.074
```

**Win rate 38 % / 36 % / 33 % across the three buckets.** Monotone in the wrong direction, on a
spread of 5 percentage points, with cells of 8, 11 and 3. **This is noise with a shape.**

### (b) By DXY — observational only, because DXY is not in the gate

```
PAPER   DOWNTREND      n=6   3/6 (50 %)  ΣR −0.865
        NEUTRAL        n=4   0/4 ( 0 %)  ΣR −3.340
        STRONG_UPTREND n=10  4/10(40 %)  ΣR −2.113
        UPTREND        n=2   1/2 (50 %)  ΣR +0.944
LIVE    DOWNTREND      n=3   2/3         ΣR +0.962   ← all three live positions, one DXY state
```

The `NEUTRAL` 0/4 is the only eye-catching cell; it is four trades. **Every live position ever
opened was opened under `dxy=DOWNTREND`, so the live book cannot separate DXY at all** — there is
one level.

### (c) The pair — does the combination beat either alone?

The largest paper cell of the 3×4 cross is **n=5**; six of the twelve cells are n≤2. **The
question is not answerable at this sample and no number from that table should be quoted.**

### The LIVE book, row by row — because n=3 is not a cohort

```
vpos 29  LONG  2026-08-08 08:50  exchange_UNKNOWN  +$1.6025  1R=$1.183  R=+1.355
         news=−1 CRITICAL_NEGATIVE   dxy=DOWNTREND   (B2: fee understated; B4: no funding)
vpos 30  LONG  2026-08-08 21:10  trail             +$0.8720  1R=$1.144  R=+0.762
         news= 0 NEUTRAL             dxy=DOWNTREND   funding $0.02352
vpos 31  LONG  2026-08-10 08:10  sl                −$1.4554  1R=$1.260  R=−1.155
         news=+1 STRONG_POSITIVE     dxy=DOWNTREND   funding $0.00   (B5: under the exit advisor)
```

🔴 **Exactly one live position per news bucket, and they rank −1 > 0 > +1** — the *opposite* of
the term's own hypothesis, on n=1 per cell, across three different fee regimes and two different
exit regimes. **It means nothing. It is stated so that it cannot later be quoted as if it did.**

---

## 4. THE REFUSAL COHORT — WHERE THE SAMPLE ACTUALLY IS

### 🔴 (c) BONFERRONI, DECLARED BEFORE THE RESULTS

```
horizons  : 4h, 12h, 24h                                   (3)
sides     : LONG, SHORT, BOTH                              (3)
statuses  : below_threshold, ai_skipped, BOTH              (3)
contrasts : news+ vs news0 ,  news− vs news0               (2)
CELLS TESTED = 3 x 3 x 3 x 2 = 54
BONFERRONI   alpha = 0.05 / 54 = 0.000926
sign convention: skip_attribution.py:171 — drift_pct is "signed toward would-be dir".
                 POSITIVE = the refusal cost us.  NEGATIVE = the refusal saved us.

scope: 15,747 drift samples over 5,263 distinct refusals (7 degraded, kept and flagged)
```

### (a) RAW — and it looks spectacular

```
horizon side  status           contrast          nA    nB   meanA%  meanB%   diff%      t         p
4h      SHORT ai_skipped       news+ vs news0    660   945   0.1949 −0.0454  0.2403   4.69  2.70e-06  ✱
4h      SHORT ai_skipped       news− vs news0    259   945   0.3535 −0.0454  0.3989   6.63  3.28e-11  ✱
12h     SHORT ai_skipped       news+ vs news0    660   941   0.5131 −0.2093  0.7224   7.96  1.66e-15  ✱
12h     SHORT BOTH             news+ vs news0    747  1469   0.4920 −0.1510  0.6430   8.03  1.01e-15  ✱
24h     SHORT ai_skipped       news− vs news0    259   930   0.5155 −0.3227  0.8382   4.97  6.81e-07  ✱
…
cells tested 54    nominal p<0.05: 34    CLEARING BONFERRONI: 21
```

**Twenty-one of fifty-four cells clear a Bonferroni bar at t up to 8.03.** On its face this is the
strongest raw result any book measurement has produced on this bot.

### 🔴 (a2) AND IT IS WRONG, AND THE DATA SAYS SO BEFORE ANY CONTROL IS APPLIED

Look at the signs. **`news+` and `news−` drift the SAME WAY** — both positive, in nearly every
cell, at similar magnitudes:

```
12h SHORT BOTH   news+ vs news0   +0.6430   (t=8.03)
12h SHORT BOTH   news− vs news0   +0.4143   (t=5.01)
24h SHORT BOTH   news+ vs news0   +0.3906   (t=3.87)
24h SHORT BOTH   news− vs news0   +0.6009   (t=5.79)
```

**A directional signal cannot do that.** If a bullish headline means price rises, then a bearish
headline must mean it does not; a variable whose *opposite* values predict the *same* outcome is
not measuring direction. It is measuring **whether a headline exists at all** — and that is a
property of the day, not of the trade.

### 🔴 (b) DE-CONFOUNDED — 0 of 54 SURVIVE

Paired within-stratum contrasts (each stratum's news-cell mean minus its news0 mean, one
observation per stratum):

| control | cells tested | cells clearing α=0.000926 | best p |
|---|---:|---:|---:|
| **none (raw)** | 54 | **21** | 1.0e−15 |
| **DAY-matched** | 54 | **0** | 1.46e−02 |
| **DAY + DIRECTION-matched** | 18 | **0** | 6.37e−02 |
| **DAY + DIRECTION + HOUR-matched** | 18 | **0** | 5.45e−03 |

```
DAY-matched, the largest survivor of the 21:
  12h SHORT below_threshold news− vs news0   30 paired days   +0.5900   t=2.44  p=1.46e-02
  12h SHORT ai_skipped      news+ vs news0   43 paired days   −0.0297   t=0.15  p=8.79e-01
                                                              ^^^^^^^ was +0.7224, t=7.96

DAY+DIR+HOUR, best cell in the whole pass:
  12h BOTH  BOTH            news+ vs news0   58 paired cells  +0.1404   t=2.78  p=5.45e-03
                                                              still 6x above the Bonferroni bar
```

**t=7.96 becomes t=0.15 when the comparison is made inside a single day.** The entire raw effect
is between-day variation. **Every one of the 21 dies. Nothing survives.**

### 🔴 (b2) THE TIME-SPLIT — the test that reversed the liquidity-lean effect

Same contrast, early half vs late half of its own window (63 days, split at 2026-07-10):

```
horizon half   contrast          nA    nB     diff%     t         p
4h    early    news+ vs news0   407   951   +0.2099   2.41   1.58e-02
4h    late     news+ vs news0   762  1832   +0.0873   2.40   1.65e-02      2.4x smaller
12h   early    news+ vs news0   407   943   +0.6549   4.87   1.10e-06
12h   late     news+ vs news0   762  1827   +0.3681   6.38   1.83e-10      1.8x smaller
24h   early    news− vs news0   412   943   +0.3386   1.91   5.58e-02
24h   late     news− vs news0   896  1815   +0.0027   0.04   9.69e-01      🔴 GONE
```

**It does not reverse sign the way the liquidity lean did — it decays.** Every effect is smaller
in the second half, and the 24h `news−` cell vanishes entirely (+0.3386 → +0.0027). A stable
mechanism does not halve when you add data; a day-level artefact does.

### 🔴 (b3) THE DEPTH MEASURE TURNED OUT TO BE A CLOCK TWICE. SO DID THIS ONE — AND HERE IT IS

Share of signals carrying a **non-zero** macro adjustment, by UTC hour:

```
hour  00    01    02    03    04    05    06    07    08    09    10    11
      13.6% 12.3% 14.3% 21.5% 43.9% 44.3% 59.1% 52.2% 49.5% 45.9% 54.8% 59.7%
hour  12    13    14    15    16    17    18    19    20    21    22    23
      84.8% 87.6% 73.5% 54.6% 54.0% 48.4% 50.8% 47.4% 63.3% 42.4% 30.5% 11.8%
```

🔴 **11.8 % at 23:00 UTC → 87.6 % at 13:00 UTC. A 7.4× swing.** The adjustment is far more likely
to be non-zero during US/EU market hours, because that is when this wire publishes. **A variable
that is on at lunchtime and off overnight is a clock wearing a headline's clothes**, and any
uncontrolled comparison against it is a comparison of 13:00 to 23:00.

```
calendar days in the window                     : 63
days with no within-day contrast available      :  5
🔴 effective independent n for a day-matched test: at most 58 DAYS — not 5,263 refusals.
```

**This is the §2.54 lesson restated with new data: the refusal cohort's n is a DAY count, and 58
days will not resolve a 0.06 %-scale effect at a Bonferroni bar of 0.000926.**

---

## 5. THE NEWS PIPELINE — IS THE INPUT SOUND?

### (a) Where it comes from, how often, and how long one headline decides

```
source     : CryptoPanic API (60 s cache, macro_filter.py:96) -> RSS fallback if empty
classifier : Claude Haiku 4.5, temperature 0.0, 6 s timeout, top 12 headlines only
             (macro_filter.py:101, :273 — headlines[:12])
TTL        : CRITICAL_NEGATIVE / STRONG_POSITIVE  15 min   (_CLS_WINDOW_CRITICAL, was 45)
             NEUTRAL                               1 min   (_CLS_WINDOW_NEUTRAL,  was  5)
cache      : ONE module-level dict, process-wide (_cls_cache) — the same classification
             serves LONG and SHORT, every symbol, every thread
```

The card's *"14m left"* is `crypto_active_mins`, that 15-minute TTL counting down.

🔴 **But the TTL is not how long a headline decides.** When it expires the classifier re-runs
against a feed that still contains the same story, and re-picks it. Measured over every
headline-day episode that produced a non-zero adjustment:

```
episodes (headline x day)          436
median span                     15.0 min
mean span                       32.1 min
MAX span                       129.9 min   (2h10m)
mean signals touched              6.3
MAX signals touched                32
```

**One headline has decided as many as 32 consecutive scored signals over 2 hours.** Today's
Robinhood story ran **08:10:01 → 08:45:07** and touched **7 signals**, one of which became vpos 31.

### (b) 🔴 IS THE HEADLINE ABOUT THE TRADED INSTRUMENT? NO — AND THE PROMPT SAYS SO OUT LOUD

```python
# macro_filter.py:103-115 — _CLS_SYSTEM, verbatim
"Crypto-wide / BTC-led events are the dominant market-regime proxy: BTC drives the whole
 market (SOL included), so classify the broad crypto regime, not SOL-specific noise."
…
"• STRONG_POSITIVE — ETF approval (SEC/CFTC), government BTC reserve adoption,
   institutional BTC purchase >$1B, …"
"• NEUTRAL — routine price analysis, minor protocol upgrades, ALTCOIN-SPECIFIC NEWS,
   analyst opinions, already-priced macro data, general crypto commentary"
```

**SOL is an altcoin.** The classifier is instructed to file SOL-specific news as **NEUTRAL**
(adjustment 0.0) and to reserve ±1.0 for **BTC-led** events. The measurement matches the
instruction exactly:

```
distinct headlines that ever produced a non-zero adjustment : 433
  naming BTC / Bitcoin  : 153 headlines  ->  1,029 of 2,734 signals moved  (37.6 %)
  naming SOL / Solana   :  10 headlines  ->     50 of 2,734 signals moved  ( 1.8 %)
  naming neither        : 270 headlines
```

And all ten SOL-naming headlines qualify on their **BTC/TradFi** half, not their SOL half:

```
STRONG_POSITIVE  n=8  "Morgan Stanley debuts Ethereum and Solana ETFs with market's lowest fee…"
STRONG_POSITIVE  n=8  "BlackRock Launches Tokenized Money Market Funds on Solana, Ethereum"
STRONG_POSITIVE  n=6  "Morgan Stanley Launches Bitcoin, Ethereum, and Solana Trading on E*Trade"
CRITICAL_NEGATIVE n=2 "Solana Exchange Raydium Hit With $1.34 Million Exploit…"   ← the one genuinely SOL-specific row
```

🔴 **This is a design decision, not a bug — and it is the answer to the brief's question.** The
pipeline does **not** distinguish crypto-wide from instrument-specific sentiment; it deliberately
**discards** instrument-specific sentiment. **The bot is trading SOL/USDT and its news term is a
BTC-regime proxy, applied at ±1.0 with no attenuation for the fact that it is a proxy.**
Whether a BTC proxy is the right input for SOL is a real question. It is not measurable from this
book, because SOL-specific news has never produced a non-zero adjustment except twice.

### (c) Concentration — it is NOT one wire's schedule

```
433 distinct headlines moved 2,734 signals
  top-1  : 1.2 %      top-5 : 5.7 %      top-10 : 10.1 %
  largest single headline: 32 signals, one day
```

**Well spread — the concentration objection does not hold.** 433 distinct stories over 63 days is
roughly 7 a day, which is a plausible news rate, not a publication artefact. **The concentration
is in the SOURCES** (CoinDesk, Cointelegraph, The Block dominate) **and in the HOURS** (§4 b3),
not in the headlines.

### (d) One thing that is stored and never used

```
macro_confidence on non-zero rows:
   0.72:345   0.75:148   0.78:356   0.82:267   0.85:1216   0.92:399   0.95:3
```

🔴 **The adjustment is ±1.0 at confidence 0.72 and ±1.0 at confidence 0.95.** `_CRYPTO_ADJ`
(`macro_filter.py:69-82`) is a sign table keyed on category alone; `crypto_confidence` is
persisted, displayed, and multiplies nothing. Today's Robinhood story scored **0.78** and moved
the gate exactly as far as a 0.95 would have.

---

## 6. VERDICT

### 🔴 IT SITS INSIDE THE NOISE. And that is the finding, not a shrug.

**Framed as the brief asked — a decision, not a survey:**

| the brief's three outcomes | which one holds |
|---|---|
| *it earns its place* | **No.** 21 of 54 cells clear Bonferroni raw; **0 of 54** survive day-matching. The effect is a clock — 11.8 % → 87.6 % non-zero rate by hour of day. `news+` and `news−` drift the **same way**, which a directional signal cannot do. |
| *it costs money* | **Not demonstrably.** Removing it deletes **one** position from the entire closed book — vpos 25, paper, **+1.257R** — and leaves the other 24 untouched, including all three live ones. The visible diff of removal is **−1.257R of paper**. |
| *it sits inside the noise* | **This one.** And the honest consequence: **a term that flips 9.1 % of all gate verdicts is unmeasurable at this sample, and will stay unmeasurable — because its effective n is 58 DAYS, not 5,263 refusals or 5,355 signals.** |

### The removal diff, shown and NOT applied

```
 vpos  book   side   raw   pen   gated       R   survives removal?
   25  paper  SHORT  1.75  +1.0   2.75  +1.257   🔴 NO — exists ONLY because of the news adj
   29  🔴LIVE LONG   4.50  −1.0   3.50  +1.355   yes
   30  🔴LIVE LONG   4.25  +0.0   4.25  +0.762   yes
   31  🔴LIVE LONG   4.50  +1.0   5.50  −1.155   yes
   … 21 further paper rows, all "yes"

positions surviving removal : 24        ΣR kept    paper −6.631 (n=21) · LIVE +0.962 (n=3)
positions never opened      :  1        ΣR removed paper +1.257 (n=1)  · LIVE  0.000 (n=0)
```

🔴 **THE DIFF IS ONE-SIDED AND MUST BE READ AS SUCH.** Removing the term also **admits** the 274
signals it currently refuses. Those have no outcome — they were never traded — so the other half
of the diff is **not computable from this book at any sample size**. What §4 measured on the
refusal side (forward drift) is the closest available substitute, and it de-confounds to zero.

### What is true, stated flatly

1. **The macro/news adjustment IS in the gate** — `main.py:4373`, `MACRO_GATE_DRYRUN=False`,
   proved on 5,355 stored verdicts with 0 mismatches and once live today at 15:25:07.
2. **The DXY half is not in the gate at all.** There is no DXY term in `total_gate_adj`. The card
   line that appears to say otherwise is two unrelated facts sharing a pipe character.
3. **The alarm's entry was not decided by the headline.** Raw 4.50 cleared a 2.0 bar by 2.50; the
   `+1.50` on its card is the weight term, which is outside the gate. The position closed at
   **−1.155R** seven hours later.
4. **It decides 9.1 % of verdicts and has built one position ever** — the AI advisor refuses
   nearly everything it admits, including both live-era admits.
5. **It is 48 % on / 52 % off with nothing in between**, worth 50 % of the entire threshold when on.
6. **It measures BTC while the bot trades SOL, by explicit instruction in its own prompt**, and
   files genuinely SOL-specific news as NEUTRAL.
7. **Its outcome effect does not survive a day control, a direction control, an hour control, or
   a time split.**
8. **Three source comments state the opposite of what the code does** (`config.py:396-398`,
   `main.py:4200`, `macro_filter.py:37-40`) — the flip-day documentation debt of 2026-06-08.

### 🔴 NOTHING PROPOSED. The map first, as with every audit this week.

No change is recommended in this pass. Points 6 and 8 are the two that would be worth a decision
later, and neither is a strategy change: one is a question about the right input, the other is
three stale comments.

---

## STATE — READ-ONLY THROUGHOUT

```
mercury-sol   active · master 4059454 / worker 4059524 · since 2026-08-09 18:42:12 · NRestarts=0
              NOT restarted, NOT edited, NO position touched, NO order placed
config.py     mtime 2026-08-09 18:41:54  <  service start 18:42:12  => the running process
              HAS MACRO_GATE_DRYRUN=False loaded. No deployment gap on the gate.
macro_filter.py  mtime 2026-06-23 09:54  — unchanged since June; nothing pending
main.py       mtime 2026-08-09 19:08 (the boot-card fix, on disk not loaded) — that edit
              touched _reconcile_open_virtual_positions only; the gate in memory == on disk
vpos 31       CLOSED 2026-08-10 15:21:44 · sl @ 75.90 · net −$1.4554 · −1.155R
open book     no open position at the time of writing
db            opened read-only for every query:  file:trades.db?mode=ro
titan         HEAD 897850b · git clean · NOT TOUCHED, NOT READ FOR STATE, NOT IMPORTED
```

**Every figure in this file comes from `/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db`
(read-only URI), `journalctl -u mercury-sol`, and the source files named inline. No write, no
restart, no order, no change of any kind.**
