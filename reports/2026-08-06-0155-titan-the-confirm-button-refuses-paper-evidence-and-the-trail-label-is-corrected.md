# TITAN — THE CONFIRM BUTTON NOW REFUSES PAPER EVIDENCE, AND THE TRAIL'S LABEL IS CORRECTED

**2026-08-06 01:55 UTC · APPLIED · `897850b` · from `999572a`**

Acts on the 01:40 optimizer audit. **`openitems_guard.py` exit 0** before (runtime `999572a`) and
after (`897850b`). Tree clean, 0 open positions at both ends.

---

## §1 — 🔴 THE LIVE CONFIRM BUTTON IS NEUTRALISED

Seven identical proposals (2026-07-30 → 08-05) recommended filtering `confluence_score < 6.0`. The
cohort behind them was **99.4% paper**, paper trades are **68.7× larger** per trade, proposals are
ranked by **raw summed dollars**, and the segment covered **32 of 37 = 86% of the book**. The CONFIRM
tap on the most recent was live in Telegram and would have turned that into a **live entry filter**.

### (a) `apply_proposal` refuses a paper-dominated cohort — a guard, fail-closed

**The predicate** is the canon's split: `virtual_positions.stop_order_id IS NOT NULL` **is live**
(paper leaves it NULL because the poller owns the stop there).

**The threshold** is a **strict majority on BOTH row count AND |PnL|**, plus `MIN_LIVE_PAIRS = 8`:

```python
MIN_LIVE_SHARE = 0.50
MIN_LIVE_PAIRS = 8          # mirrors optimizer.MIN_PATTERN_SAMPLE
```

**Why both, and why a majority:**

- **Both**, because a segment can be majority-live *by row count* and still 99% paper *by dollars* —
  and the dollar weighting is the actual defect. A rows-only test would have passed the very case
  that caused this.
- **A majority**, because below it the conclusion is *literally determined by the other instrument*.
  Stated plainly in the code: a majority is **the minimum defensible bar, not a sufficient one**.
  Paper is not "less precise live" — different size, simulated fills, no real slippage. Summing the
  two is a unit error.
- **`MIN_LIVE_PAIRS` on top**, so a handful of live rows cannot clear the bar by being a majority of
  almost nothing. It mirrors `MIN_PATTERN_SAMPLE = 8`, so the live evidence must meet the same
  sample bar the analyser already demands.

🔴 **IT FAILS CLOSED.** A proposal with no `live_evidence` block *cannot be shown* to rest on live
trades, so it is refused rather than trusted. **That single decision is what neutralises the seven
standing proposals** — none of them carries the block, because none could.

🔴 **The guard runs BEFORE any write** — before `filters.json` and before the cycle marker. A refusal
leaves both untouched, which matters because the audit found those two writes already disagreeing in
the stored state (O7).

### (b) The proposal no longer arises — and the analyser says why

`optimizer.py` now builds its cohort from live rows only:

```python
_live_ids = live_entry_row_ids()          # stop_order_id IS NOT NULL
cohort, _paper_cycle = split_live_paper(cycle_pairs, _live_ids)
```

With **7 live pairs** it falls below the 30-gate, so no segment analysis runs at all. And it **says
so** rather than going quiet or answering from paper — the live dry-run, run against the real
database after the restart:

```
⏳ Optimizer: INSUFFICIENT LIVE DATA
Live closed trades this cycle: 7/30
💰 Live PnL: $-4.1476   📊 Win-rate: 14.3%
30 paper pair(s) EXCLUDED — a filter blocks REAL entries, so only real trades may propose one.
Paper positions are ~68x larger per trade and would decide the ranking on their own.
No segment analysis until 30 live closes.
```

**An analyser that cannot conclude should say so; silence and a paper answer are both worse.**

🔴 **The weight path is deliberately untouched.** `weight_engine.compute_weight_updates(paired)` still
receives the full all-time set exactly as before. That lever is inert for separate reasons (§3a
below) and changing it is a design decision, not a guard.

When a proposal *can* eventually arise, it is stamped with the evidence the listener verifies —
stamped rather than assumed, so the guard checks the proposal instead of trusting the module that
wrote it. `paper_rows_excluded` is recorded for the reader and **deliberately does not feed the share
computation**.

### (c) Proven by execution — isolated DB *and* an isolated copy of the optimizer directory

```
1c — THE LIVE CONFIRM BUTTON: A TAP NOW REFUSES
  the standing proposal: confluence_score=conf<6.0 n=32 net=$-1084.99
  carries a live_evidence block? False
  apply_proposal('prop-20260805-120002') -> ok=False
    🔴 REFUSED — confluence_score=conf<6.0
    this proposal carries NO live/paper evidence block — it predates the live-evidence
    guard (2026-08-06). It cannot be shown to rest on live trades, so it is REFUSED.
    Nothing was filtered and the cycle marker was NOT moved.

  ✅ the tap is REFUSED          ✅ filters.json STILL EMPTY
  ✅ cycle marker NOT moved (8634 unchanged)

  every one of the seven standing proposals:
    prop-20260730-120001 … prop-20260805-120002 : REFUSED  (7 of 7)

1a — THE GUARD'S PREDICATE
  ✅ no evidence block at all                                        -> refused
  ✅ 8 live / 0 paper, 100% live dollars                             -> ALLOWED
  ✅ 7 live — below MIN_LIVE_PAIRS                                   -> refused
  ✅ 🔴 majority live ROWS but 99% paper DOLLARS (the real defect)    -> refused
  ✅ majority paper rows                                             -> refused
  ✅ exactly 50/50 — not a strict majority                           -> refused

1b — THE COHORT
  cycle pairs 37  ->  LIVE cohort 7 · paper excluded 30
  ✅ says INSUFFICIENT LIVE DATA   ✅ states the excluded paper count
  ✅ find_worst_segment on the live cohort returns None
```

### (d) Nothing retro-applied

```
✅ the REAL filters.json is still empty: []
✅ version untouched: 1
   mtime: 2026-05-16 19:31:21 +0000
```

The proof harness copied the optimizer directory and asserted its paths no longer pointed at
`/root/titan-bot` before running. **`filters.json` stays empty and stays dated 2026-05-16.**

---

## §2 — 🔴 THE LABEL, CORRECTED EVERYWHERE IT IS CARRIED

### The corrected fact, in one quotable sentence

> **`TRAIL_MULT_ATR / SL_ATR_MULT = 0.75` is the RATIO OF THE CONSTANTS, not the giveback: the trail
> is a percentage OF THE ENTRY applied TO THE WATER MARK, so the realised giveback is 0.7560R at the
> arming moment and drifts with MFE — wider on longs, tighter on shorts (measured LONG +1.63% /
> SHORT −4.09% over 14 trailed exits).**

**"was exactly 1.00R" is wrong the same way.** On all 7 live rows `trail_pct × entry == 1R_price`
exactly — and those same trails gave back **1.0160R (LONG) / 0.9591R (SHORT)**.

### Carriers corrected

| carrier | now says |
|---|---|
| `config.py` `TRAIL_MULT_ATR` block | the quotable sentence above, the 14-exit measurement, the forward table (MFE 1R → 0.7560R · 2R → 0.7625R · 3R → 0.7690R), the "was exactly 1.00R" correction, **and that 1.6875 survives with why** |
| `config.py` `SL_ATR_MULT` block | "the **CONSTANT RATIO** is `TRAIL_MULT_ATR / SL_ATR_MULT` … 🔴 **THAT RATIO IS NOT THE GIVEBACK**" |
| `config.py:226` inline | `# ratio 1.6875/2.25 = 0.75; REALISED giveback 0.756R and side-dependent (see above)` |
| canon **§2.53** | heading now reads **TRAIL RATIO 1.00→0.75**, with a boxed correction stating the realised giveback and that **the decision is unaffected** |
| canon **§0.1** | **rewritten from "BLOCKED" to ANSWERED** — see below |

### §0.1 rewritten: the grid modelled the real mechanism, and 1.6875 survives

My 01:15 entry framed this as possibly a calibration error. It was not. The canon now records the
three-way evidence — **source** (both surviving scripts compute the percentage off entry and apply it
to the water mark, letter-for-letter the engine), **impossibility** (an entry base makes the trail
inert, so the axis would be flat while the published one varies), and **reconstruction** (mech-24
reproduced exactly at two cells, cohorts clean-40 / mech-24 as labelled) — plus the finding that
**the side skew was in the grid** (+1.53% / −4.07% on replay) and that the decision rule required
both sides to improve. **§2.53's decision stands. The geometry does not need revisiting.**

---

## §3 — RECORDED, NOT CHANGED

### (a) 🔴 O3 — the weight lever's loop closes on nothing, by two independent mechanisms

It is the **only** thing the optimizer moves **without a human**, it moves **every day** — all 26
segments are off 1.0, range 0.2–2.5, last written 2026-08-05 12:00 — and its output reaches **no
decision**:

1. `weight_engine.weighted_adj`'s own docstring: *"total_adj is clipped to [−1.5, +1.5] and added to
   direction_score before storing as confluence_score. **Never applied to the gate check.**"* Its only
   consumer, `adj_score`, is **stored and printed** (`Score: {adj_score}/10`), never compared to a
   threshold.
2. §0 records that the stored value is then **overwritten with the raw matrix score, 154 lines later,
   on 66 of 66 engine-owned entries.**

**Wider than §2.40**, which named only the *combo* weight: **the entire `weighted_adj` output is
inert.** And the weights are learned from paper-scaled `avg_pnl` (−27.65, +36.57, +43.89 — live
trades are ±$0.59), so the numbers being written are paper numbers.
**Not wired and not stopped in this pass — it is a design decision.**

### (b) 🔴 Two different machines, and the grid's scripts are not in the repository

Recorded in the canon as **§0.2**:

- **`optimizer.py` never chose the geometry.** Neither `SL_ATR_MULT` nor `TRAIL_MULT_ATR` appears in
  the file. It has no such lever and cannot acquire one by accident.
- **The 2026-08-04 grid was ad-hoc session work** in `/tmp/claude-0/-root/<session-uuid>/scratchpad/`.
- 🔴 **The script that produced §2.53's published table — the one that chose the applied cell — IS
  ALREADY GONE FROM DISK.** Two neighbours from the same session survived and were enough to settle
  G1 today. **That was luck, not a property of the setup.**

**This is the §2.20 defect in a new place:** the artefact that decides a live constant is not under
version control, so the reasoning behind an applied number can evaporate while the number keeps
trading. Anything that moves a live constant should be committed with the change that applies it.

### (c) O4–O8 as measured

**0 of 5** of §0's contamination filters (the sibling grid applied two of them on the same table) ·
**no validation or replay step of any kind** — it never reproduces the book, it only aggregates
recorded `pnl` · reads `confluence_score` directly against §0's rule, benign *today* only because its
cohort is all-`executed` · `virtual_cycle_start_id = 8634` while `filters.json` is empty, so
`apply_proposal`'s two writes disagree in the stored state — **unresolved, and now moot for future
taps because the guard refuses before either write** · `ai_decision` and `tv_tf` are single-valued on
37/37 and can never form a segment. **Clean:** no read of the position `atr` column (G5 does not reach
it); `market_regime` populated on every row it sees.

---

## §4 — SCOPE: A GUARD AND COMMENT TEXT, NOTHING ELSE

```
optimizer.py           CODE-CHANGED: fmt_report, main
                       ADDED:        live_entry_row_ids, split_live_paper
optimizer_listener.py  CODE-CHANGED: apply_proposal
                       ADDED:        _live_evidence_ok
config.py              CODE-CHANGED: none
```

🔴 **`config.py` compared across ALL 113 uppercase names: NO VALUE CHANGED — comments only.** That is
the strongest available statement that the geometry constants and score bars did not move, and it is
a diff of the imported values, not a reading of the file.

Re-read by importing `config` after the restart: `SL_ATR_MULT = 2.25` · `TRAIL_MULT_ATR = 1.6875` ·
`SL_ATR_TF = 1h` · `TRAIL_ATR_TF = 1h` · `CONFLUENCE_SCORE_THRESHOLD = 3.0` ·
`CONFLUENCE_FLAT_THRESHOLD = 5.0` · `LIVE_TRADING_ENABLED = True` · `ORDER_ADAPTER_LIVE = True`.
**Gates, geometry constants, score bars, both prompts and every schema untouched.**

`ast.parse` ✅ and `py_compile` ✅ on all three files. **No DB schema change** — the evidence block
lives in the proposal JSON, not in a table.

## §5 — RESTARTED FROM FLAT

`titan` restarted **01:53:19**, `optimizer-listener` restarted with it. `ActiveState=active`,
`NRestarts=0`, **0 errors**, four boot gates green, 0 open rows before and after.

⚠️ **Worth knowing:** the listener came up with `offset=0` (`tg_offset.txt` holds `0`), so Telegram
may redeliver callback queries from the last 24h. **A replayed CONFIRM tap now refuses** — which is
precisely the scenario the guard was built for, and it is now covered rather than latent.

---

## §6 — THE THROUGH-LINE

The 01:40 audit named this class: **a measurement whose UNIT was never checked.** Both halves of this
pass are that, and they resolve in opposite directions.

- **The optimizer** summed dollars across a book where one trade is 68.7× another. Nothing was
  "broken" — every line did what it said. **Nobody asked whether the numbers were the same kind of
  number before adding them up**, and the answer would have become a live filter on one tap.
- **The grid** asked exactly that question and passed: one unit (`R_ref` fixed), sides kept separate,
  the real trail base modelled. **Its number survives; only its name was wrong.**

**Two machines, one question, opposite verdicts — and only one of them had ever been audited.** The
fix that matters most here is not the guard: it is that the canon now says which machine is which,
and that the one which chose a live constant **left no artefact behind**.

---

*Applied and committed as `897850b`. No order was sent. The proof harness copied both the database
and the optimizer directory and asserted its paths no longer pointed at the live tree before running;
`filters.json` is still empty and still dated 2026-05-16, and the cycle marker is still 8634.*
