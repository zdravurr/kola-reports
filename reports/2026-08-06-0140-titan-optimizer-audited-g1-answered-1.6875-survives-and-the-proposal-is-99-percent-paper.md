# TITAN — THE OPTIMIZER, AUDITED. G1 IS ANSWERED: **1.6875 SURVIVES.** THE OPTIMIZER'S OWN PROPOSAL DOES NOT.

**2026-08-06 01:40 UTC · READ-ONLY · nothing changed, nothing committed · HEAD `999572a`**

The last of the three areas the 19:55 scope note left unaudited. **`openitems_guard.py` exit 0** —
runtime HEAD `999572a`, 11 watched values, canon agrees. Tree clean, service `active`,
`NRestarts=0`, 0 open positions.

---

# §1 — 🔴 G1 IS ANSWERED. THE GRID MODELLED THE REAL MECHANISM.

## (a) The trail model, quoted verbatim

🔴 **The 17:05 script that produced §2.53's published table is NOT on disk.** Two scripts from the
same session's lineage survive in that session's scratchpad, and §2.53 is described in the canon as
**§2.50's grid re-run on §2.52's honest instrument** — so the trail model is the part they share.

**`geom.py` (2026-08-04 16:18 — the §2.50 grid):**

```python
30:    trail_pct = trail_r * (sl_dist / entry) * 100.0
…
61:        wm = max(wm, h) if long else min(wm, l)
62:        if be_on and trail_pct > 0:
63:            trig = wm * (1 - trail_pct / 100) if long else wm * (1 + trail_pct / 100)
64:            if (long and trig > sl) or (not long and trig < sl):
65:                sl = trig
```

**`three_methods.py` (2026-08-04 16:45 — the §2.52 three-basis study):**

```python
52:    trail_pct = trail_r * (d / r['f']) * 100.0          # r['f'] = initial_fill_price
…
72:        wm = max(wm, hi) if long else min(wm, lo)
73:        if be_on and trail_pct > 0:
74:            trig = wm * (1 - trail_pct / 100) if long else wm * (1 + trail_pct / 100)
```

**Both compute `trail_pct` as a fraction of the ENTRY and apply it to the WATER MARK.** Set against
the engine:

| | engine | grid |
|---|---|---|
| the percentage | `_trail_pct_for`: `TRAIL_MULT_ATR * atr / initial_fill_price * 100` | `trail_r * (sl_dist / entry) * 100` |
| | *(and `trail_r × sl_dist` = `(TRAIL_MULT_ATR/SL_ATR_MULT) × SL_ATR_MULT × atr` = `TRAIL_MULT_ATR × atr` — algebraically the same)* | |
| the base it is applied to | `trigger = water_mark * (1 ∓ trail_pct/100)` | `trig = wm * (1 ∓ trail_pct/100)` |
| the ratchet | trigger recomputed from a monotone `water_mark`, so monotone | `if trig > sl: sl = trig` — never loosens |
| breakeven stop | `fill * (1 ± 2·TAKER + BUFFER)` | `f * (1 ± 2*TAKER + BE_BUF)` |

**Identical.** The only difference is that the engine rounds `trail_pct` to 3 dp (G8, ±0.08%) and
the grid does not.

## 🔴 (a′) A SECOND PROOF THAT DOES NOT DEPEND ON FINDING THE 17:05 FILE

Since the exact script is missing, the source quote alone is inference. **So here is a proof from the
published numbers themselves: an entry-based trail CANNOT have produced §2.53's table, because under
an entry base the trail axis is FLAT.**

Re-running the reconstructed grid with the trail applied to the entry instead:

| cell | water-mark base (mech-24 / clean-40) | **entry base** |
|---|---|---|
| SL 2.0 · 0.75R | +6.62 / +6.32 | **+2.97 / +2.83** |
| SL 2.0 · 1.0R | +4.92 / +4.48 | **+2.97 / +2.83** |
| SL 2.0 · 1.25R | +3.28 / +3.14 | **+2.97 / +2.83** |
| SL 2.25 · 0.75R | +5.27 / +5.46 | **+2.08 / +2.48** |
| SL 2.25 · 1.0R | +3.01 / +3.41 | **+2.08 / +2.48** |
| SL 2.25 · 1.25R | +2.12 / +2.52 | **+2.08 / +2.48** |

**Under the entry base every trail width gives the SAME number.** The reason is mechanical:

```
SL 2.25, trail 0.75R : entry-based trigger 64,236.96  vs  breakeven stop 64,785.51  -> ratchet fires? False
SL 2.25, trail 1.0R  : entry-based trigger 64,097.21  vs  breakeven stop 64,785.51  -> False
SL 2.25, trail 1.25R : entry-based trigger 63,957.46  vs  breakeven stop 64,785.51  -> False
```

The trail only arms **at breakeven**, where the stop is already `entry × (1 + 0.002)`. An
entry-based trigger sits **below** that forever, so `if trig > sl` never fires and **the trail is
inert**. §2.53's published trail axis **varies** — `+6.62 → +4.92 → +2.77` at SL 2.0. **An inert
trail cannot produce a varying axis.** The grid must have used the water-mark base.

**Corroboration from the reconstruction:** rebuilding §2.53 as *§2.50's cells + §2.52's closes basis
+ truncation at the real close + a fixed R_ref* reproduces the canon's mech-24 column **exactly** at
two cells — **SL 2.0 / 0.75R = +6.62** (canon +6.62) and **SL 2.0 / 1.0R = +4.92** (canon +4.92) —
and the cohorts come out **clean = 40, mech = 24**, matching the canon's labels. Other cells drift
0.1–2.7R, which I attribute to truncation-horizon details I cannot recover without the original
file. **I am not claiming a full reproduction. I am claiming the trail model, and that claim has two
independent supports.**

## (b) 🔴 THEREFORE: G1 COLLAPSES TO A WRONG LABEL. **1.6875 SURVIVES.**

`TRAIL_MULT_ATR = 1.6875` was **calibrated against the quantity the engine actually produces**. The
grid is not offset. §2.53's decision stands. **Nothing about the applied geometry needs revisiting.**

What is wrong is only the **name**. The realised giveback is **0.7560R at the arming moment**, rising
with MFE on longs and falling on shorts — not 0.7500R. These documents carry the wrong label:

| document | the wrong text |
|---|---|
| **`config.py:226`** | `TRAIL_MULT_ATR = 1.6875  # 0.75R trail (1.6875 / 2.25); was 2.5 = exactly 1.00R` |
| **`config.py:175`** | *"trail-in-R = TRAIL_MULT_ATR / SL_ATR_MULT"* — true of the ratio, not of the giveback |
| **`config.py:219`** | *"trail-in-R = 1.6875 / 2.25 = 0.75R (it was exactly 1.00R, because both were 2.5)"* |
| **canon §2.53** | *"TRAIL 1.00R→0.75R"* in the heading and throughout |
| **canon §0.1** | my own entry from 01:15, which framed this as possibly a calibration error |
| **my 00:50 and 01:15 reports** | both state the question as open |

**"was exactly 1.00R" is wrong in the same way**, and the book proves it: on the 7 live rows
`trail_pct × entry == 1R_price` exactly, yet the 14 trailed exits gave back **1.0160R (LONG)** and
**0.9591R (SHORT)**.

## (c) Not applicable

The grid did not use `pct × entry`, so there is no counterfactual re-run to report and no question
of 1.6875 failing. *(For completeness, the entry-base counterfactual above still selects SL 2.0 /
0.75R as its top cell — but only because the trail is inert in it, which makes the axis meaningless.)*

## (d) 🔴 THE SIDE-DEPENDENT SKEW **WAS** IN THE GRID

Measured **inside the grid's own replay**, at the cell that was applied (SL 2.25 / trail 0.75R),
across the mech-24 cohort's trail-closed positions:

| side | n | mean giveback in the GRID | nominal | skew | mean water_mark / entry |
|---|---|---|---|---|---|
| **LONG** | 4 | **0.7615R** | 0.7500R | **+1.53%** | 1.01531 |
| **SHORT** | 9 | **0.7195R** | 0.7500R | **−4.07%** | 0.95932 |

Set against the live book measured in the 00:50 audit — **LONG +1.63% / SHORT −4.09%** — these are
the same numbers. **The grid reproduced the asymmetry rather than being blind to it**, and the
decision rule made it load-bearing: conjunct (b) required *both sides on both cohorts* to improve
(`geom.py:144`), so LONG and SHORT were scored separately with the skew present in each.

**Both levers were scored on the same mechanism. Neither was mis-scored.**

---

# §2 — THE OPTIMIZER ITSELF, BY THE SAME METHOD

🔴 **FIRST, A CORRECTION THAT REFRAMES THE WHOLE SECTION: `optimizer.py` IS NOT THE THING THAT CHOSE
THE GEOMETRY.** It has never proposed, moved or evaluated `SL_ATR_MULT`, `TRAIL_MULT_ATR`, or any
geometry constant — grep confirms neither name appears in it. It is a **segment analyser**: it pairs
closed trades, groups them by 24 candidate fields, and reports the worst-performing group. The
geometry grid was ad-hoc session work. **Two different machines, and the canon's §2.5x sections do
not distinguish them.**

## (a) Does it reproduce the book before predicting? **NO — and it has no instrument to.**

There is **no replay, no counterfactual and no validation step anywhere in `optimizer.py`.** It never
reproduces an outcome; it only aggregates recorded `pnl`. §0's "validate first" rule is therefore not
violated so much as **inapplicable** — but that is itself the finding: its conclusions are pure
in-sample segment splits with no out-of-sample or reproduction check of any kind.

## (b) 🔴 §0's five contamination filters: **0 of 5 applied**

| filter | applied? |
|---|---|
| forming candle | **NO** — it reads no candles at all |
| wall-trail lifetime overlap | **NO** — no date-window predicate exists |
| recheck TIGHTEN | **NO** — 🔴 and the geometry grid *did* apply it (`recheck_status != 'tightened'`) |
| excursion truth | **NO** — `position_excursion_samples` is never queried |
| indicator window | **NO** — `srv_adx_1h` / `srv_atr_1h` read as stored, no window check |

The grid also excluded the 2026-07-13/07-02 overlap cohort. **The optimizer applies neither of the
two filters its sibling study considered mandatory on the same table.**

## (c) 🔴 Pooling: **there is no predicate at all — and the paper/live mix is fatal**

The query is `SELECT * FROM trades WHERE id IN (SELECT trades_entry_row_id FROM virtual_positions
WHERE status='closed')`. **No `is_virtual`, no `stop_order_id`, no date bound.**

- **1R boundary (2026-08-04 17:01:29):** not crossed *in the R sense*, because the optimizer works in
  **dollars**, not R. But the dollar risk per trade fell ~10% at the boundary, so a dollar sum still
  mixes two risk sizes. **No predicate.**
- 🔴 **PAPER / LIVE:** measured on its own current cohort:

```
PAPER pairs:  30   total pnl $ -733.3840   mean $-24.4461
LIVE  pairs:   7   total pnl $   -4.1476   mean $ -0.5925
PAPER share of |total dollar PnL|:  99.4%
mean |pnl| ratio paper/live:        68.7x
```

`find_worst_segment` ranks segments by **raw summed dollars**. Paper positions are ~0.15 BTC
(~$10k notional); live are 0.0023 BTC ($150). **Every proposal the optimizer has ever made is
decided 99.4% by paper trades, and its output is a filter that would block LIVE entries.**

## (d) `confluence_score` — read directly, and the buckets are calibrated for a different scale

`_bucket_confluence` reads `o['confluence_score']` raw. §0's rule is *"reconstruct the score from
`matrix_breakdown_json`, never from `confluence_score`"* — **the rule is violated.**

🔴 **But being fair about the consequence:** the four-quantities problem is about comparing *across
statuses*, and this cohort is **all `status='executed'`**, where §0 measured the column to be RAW on
**66 of 66** rows. So it is homogeneous here. **The mixture is not what bites. The bucket edges are:**

```
bucket edges          : 6.0 / 7.5 / 9.0
live confluence range : 2.25 .. 7.75    (n=37)
CONFLUENCE_SCORE_THRESHOLD (the live gate) = 3.0
```

**The edges were calibrated for a scale this bot no longer uses.** Consequence in §2 below.

## (e) `atr` and `market_regime` — **both clean**

- It does **not** read the position's `atr` column, so **G5 does not reach it**. `_bucket_atr_1h_pct`
  uses `srv_atr_1h` — the 1h server indicator, the correct timeframe.
- `market_regime` is **non-NULL on 37 of 37** cohort rows. The NULL-on-refused defect does not bite,
  because the optimizer only ever sees `status='executed'` rows.

## (f) Paths that never execute, and flags that read as armed

- 🔴 **The CONFIRM path has never applied a filter.** `filters.json` is `{"version": 1, "filters": []}`
  and **untouched since 2026-05-16**. `optimizer_listener.apply_proposal` — the only writer — has
  never completed.
- 🔴 **…yet `settings.virtual_cycle_start_id = 8634`**, and that marker is documented as *"advanced
  ONLY by optimizer_listener.apply_proposal on a CONFIRM tap"*. **The two halves of one function
  disagree: the marker moved, the filter file did not.** Either it half-ran once or the marker was
  set outside it. Recorded, not resolved.
- **Two dead candidate fields:** `ai_decision` is `'execute'` on **37 of 37** and `tv_tf` is `'5m'` on
  **37 of 37**. A field with one value can never form a segment; both are permanently inert.
- **`is_filter_active` never returns True** (empty filters file), so the "already filtered" branch of
  `fmt_report` has never rendered.

---

# §3 — WHAT THE OPTIMIZER CAN ACTUALLY MOVE

| lever | mechanism | needs confirmation? | has it ever moved? | still in force? |
|---|---|---|---|---|
| **segment filter** (`filters.json`) | proposal → Telegram CONFIRM → `apply_proposal` | **YES** | **NO** — file empty, untouched since 2026-05-16 | n/a |
| **`dynamic_weights.json`** | `weight_engine.save_weights` on **every run** | 🔴 **NO** | **YES** — all **26 of 26** segments moved off 1.0, range **0.2 … 2.5**, last written 2026-08-05 12:00 | **written, but see below** |
| `virtual_cycle_start_id` | listener, on CONFIRM | YES | marker is at 8634 (inconsistent, above) | — |
| **geometry constants** | — | — | 🔴 **NEVER. It has no such lever.** | — |

🔴 **THE WEIGHT LEVER IS THE §2.40 CLASS, AND WIDER THAN §2.40 DESCRIBED.** It is the only thing the
optimizer moves without a human, it moves every single day, and its output reaches **no decision**:

1. `weight_engine.weighted_adj`'s own docstring: *"total_adj is clipped to [−1.5, +1.5] and added to
   direction_score before storing as confluence_score. **Never applied to the gate check.**"*
2. Its only consumer is `adj_score = round(direction_score + _w_adj, 2)`, which is **stored** as
   `confluence_score` and **printed** in the entry Telegram (`Score: {adj_score}/10`). It is never
   compared to a threshold.
3. 🔴 And §0 records that the stored value is then **overwritten with the raw matrix score, 154 lines
   later, on 66 of 66 engine-owned entries.**

**So the loop closes on nothing: excluded from the gate by policy, then erased from the record by an
overwrite.** §2.40 said the *combo* weight is inert at live size; this is broader — **the entire
`weighted_adj` output is inert, by two independent mechanisms.** And the weights themselves are
learned from paper-scaled `avg_pnl` (−27.65, +36.57, +43.89 — live trades are ±$0.59), so the
numbers being written are paper numbers.

---

# §4 — VERDICT

| # | finding | runs | 🔴 **MISPLACES MONEY** / 📏 **CORRUPTS MEASUREMENT** | rank |
|---|---|---|---|---|
| **O1** | proposals are ranked by **raw dollars** across a cohort that is **99.4% paper**, paper being **68.7×** larger per trade | **every daily run** | 🔴 **MONEY IF CONFIRMED** — one Telegram tap turns a paper-derived segment into a live entry filter. Today: 📏, because CONFIRM has never fired | 🔴 **1** |
| **O2** | the standing proposal `conf<6.0` covers **32 of 37 = 86%** of the book; bucket edges 6.0/7.5/9.0 on a live scale of **2.25–7.75** | proposed **7 days running**, identical | 🔴 **MONEY IF CONFIRMED — it would filter 86% of all entries.** It is not a segment, it is the book | 🔴 **2** |
| **O3** | `weighted_adj` moves 26 weights daily with **no confirmation**, into a value excluded from the gate and then overwritten 66/66 | every run | 📏 **MEASUREMENT** — and strictly, not even that: the output survives nowhere | 🟠 **3** |
| **O4** | **0 of 5** contamination filters; the sibling grid applied two of them on the same table | every run | 📏 measurement | 🟠 **4** |
| **O5** | no validation/replay step of any kind | every run | 📏 measurement | 🟠 **5** |
| **O6** | reads `confluence_score` directly against §0's explicit rule | every run | 📏 — benign *today* only because the cohort is all-executed | 🟡 **6** |
| **O7** | `virtual_cycle_start_id = 8634` while `filters.json` is empty — one function's two writes disagree | once, historically | 📏 state inconsistency | 🟡 **7** |
| **O8** | `ai_decision` and `tv_tf` are single-valued on 37/37 — permanently inert candidate fields | every run | ⚪ noise | ⚪ **8** |

**Clean:** it does **not** touch the position `atr` column (G5 does not reach it), `market_regime` is
populated on every row it sees, `pair_trades`' 2026-06-16 counter-fix correctly excludes skip/block
rows, and the `_AMBIGUOUS_CLOSE_TYPES` P4 fix genuinely pairs armed-exit closes.

## 🔴 SHOULD ANYTHING BE WITHDRAWN?

**About the geometry: NO — and that is the headline.** `TRAIL_MULT_ATR = 1.6875` and
`SL_ATR_MULT = 2.25` were chosen on the mechanism the engine actually runs, with the side-dependent
skew present and scored on both sides. **G1 is downgraded from "possible calibration error" to
"wrong label", and §2.53 stands.** A third headline number is **not** due.

**About the optimizer's own output: YES, and it is standing right now.** The seven proposals of
2026-07-30 → 2026-08-05 all recommend the same filter, and it is unsound on two independent grounds —
**99.4% paper** and **86% of the book**. They should be treated as **withdrawn, not pending**: the
CONFIRM button on the most recent one is live in Telegram, and tapping it would filter almost every
future entry on the strength of paper dollars. **That is the one action this audit would stop.**

## The through-line

The three previous audits found *a number replaced by the one we asked for*, *a mechanism trusted
untested*, and *two quantities equal at one instant*. **This one is the fourth: a measurement whose
UNIT was never checked.**

The optimizer sums dollars across a book where one trade is 68.7× another, and buckets a score
against edges from a scale that no longer exists. Neither is a coding error — every line does what it
says. **The defect is that nobody asked "are these the same kind of number?" before adding them up.**

And the same question, asked of the geometry grid, is what cleared it: the grid *did* work in one
unit (`R_ref` fixed), *did* separate the sides, and *did* model the real trail base. **The two
machines were held to different standards, and only one of them was ever audited.**

---

*Read-only throughout: no file changed, no commit made, no order sent. The grid reconstruction ran
against an isolated copy of `trades.db` in the session scratchpad; the live database was opened
read-only and `MAX(id)` is still 92. Working tree clean at `999572a`; `openitems_guard.py` exit 0
before and after.*
