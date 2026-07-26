# both-advisors-audit

_2026-07-26 19:12 UTC_

---

# TITAN — both advisors audited: entry wall calibration + exit advisor

**2026-07-26 · READ-ONLY. Nothing applied, nothing proposed.** Tree clean at `f7df202`. Paper mode.

**Two headline answers, and they are opposite in kind.**

1. **The wall SIDE hypothesis is dead — exactly as on Mercury-SOL.** The skips that read an ask wall
   above as a headwind for a SHORT drifted **more negative than the control** (-0.270% / 4h,
   t = -4.6). They were the *better* vetoes. The load-bearing subset drifted **-1.509% / 24h**.
   Correcting the wall logic would convert good vetoes into losses. **Recommend no change.**
2. **The wall SCALE problem is real, measurable, and different from what was suspected.** The word
   "Massive" is in the **prompt template**, not the model's judgement — every wall above 4.0× is
   labelled that way. Against the 17,859-snapshot baseline, **100% of book states contain at least
   one "massive" wall**, the median max wall is 6.24×, and **12 of 18 real entries were told about a
   "massive" wall that sat BELOW the book's median.**
3. **The exit advisor has never run. Not once.** It is wired, but keyed to live exchange positions,
   which do not exist in paper mode.

---

# PART 1 — Entry advisor, wall logic

## 1.1 Classification across all stored reasons

2,760 decisions carry an `ai_reason`; **2,030 (73.6%) mention a wall.**

| pattern | n | share of that side's wall-mentions |
|---|---|---|
| **SHORT skip · ask wall ABOVE · framed as an obstacle** | **289** | **26.6%** of 1,086 |
| LONG skip · bid wall BELOW · framed as an obstacle | 12 | 1.3% of 944 |
| *control* — SHORT skip · bid wall BELOW (a genuine obstacle) | 66 | |
| *control* — LONG skip · ask wall ABOVE (a genuine obstacle) | 314 | |

**The 289 is an upper bound, not a confirmed error count.** Reading them in full, three things are
mixed together:
* Genuine confusion — *"massive ask walls above entry absorb momentum"* (id 3890, 14679, 8150).
  A short's momentum is downward; a wall above cannot absorb it.
* A **defensible** argument the classifier cannot distinguish — price may be pulled *up* into a
  large ask wall before reversing, stopping out a short entered below. Several reasons read that
  way (id 17906: *"blocks upside absorption"*).
* Mixed reasons where the wall is one clause among four (id 4024 cites bid walls below **and** ask
  walls above, correctly and incorrectly, in one sentence).

The mirror case on the long side is nearly absent: **12 instances, 1.3%**. Whatever this is, it is
overwhelmingly one-sided.

## 1.2 The replay — same method as Mercury-SOL 2026-06-30

Rather than re-running the model, the decisive test is what price did after those skips. Convention:
**drift > 0 = the skipped SHORT would have won**, i.e. the veto cost money.

| cohort | 4h | 12h | 24h |
|---|---|---|---|
| **"misread" cohort (n=289)** | **-0.270%** (t=-4.6) | **-0.200%** (t=-2.5) | **-0.473%** (t=-3.8) |
| control — all other SHORT skips | -0.051% | +0.067% | +0.037% |
| **load-bearing subset (n=37)** — wall is essentially the only objection | — | **-0.650%** (38% pos) | **-1.509%** (34% pos) |

**The cohort accused of misreading the book contains the BEST vetoes in the entire book.** They
drift 5× more negative than the control at 4h, and the subset where the wall is doing all the work
drifts -1.5% at 24h with only a third of cases positive.

**This is Mercury-SOL's result reproduced on Titan.** There, replaying 471 skips with corrected wall
logic flipped 6 (1.3%), all six into losers averaging -2.05%. Here the mechanism is visible directly
in the drift: any correction that converted these vetoes into entries would have entered short
positions immediately before price fell — no, worse: it would have entered them and then price
**continued in the direction that made the skip correct.**

**Recommendation: no change to the wall side logic.** The hypothesis is disproven twice, on two
bots, by two different methods.

## 1.3 Scale — the real miscalibration, and it is in OUR code, not the model's reading

**What the advisor actually receives** (`claude_advisor._format_pre_trade_walls`):
```
Order book (pre-trade, 4000 levels):
  Mid: $64,779.80  |  Imbalance ±1%: 0.87 (bid-heavy)
  Massive bid walls (>4x avg vol): $64,700.00 (×5.4), ...
  Massive ask walls (>4x avg vol): $64,850.00 (×4.9), ...
```
* `×mult` is a multiple of the mean of the **same snapshot** — there is no historical reference.
* **The adjective "Massive" is hard-coded in the template.** The model does not judge the wall to be
  massive; it is *told* so, for anything above `PRE_TRADE_WALL_MULTIPLIER = 4.0`.
* `imbalance` is raw, with a bid-heavy/ask-heavy split at 0.50 — also no baseline.

**Is the ob-density baseline wired in? No.** `grep` over the whole tree: `orderbook_density` is
referenced only by its own collector and by a config comment which states the position explicitly —
*"Read by NO gate/exit/sizing/advisor."*

**What the baseline says** (17,859 snapshots since 07-13):
```
max_wall_mult_ask   p25 4.99   p50 6.24   p75 8.25   p90 13.02   p95 14.23
max_wall_mult_bid   p25 4.72   p50 5.52   p75 7.06   p90  9.85   p95 12.40

Snapshots whose largest wall is BELOW the 4.0x "massive" threshold:  0.0%   (both sides)
```
**In 100% of book states there is at least one wall the prompt will call "massive". The median
largest wall is 6.24× — comfortably above the threshold. The adjective carries no information.**

**Cross-check on the 18 real entries that have a stored book snapshot:**
```
vpos 65 LONG  ×4.6  -> 20th pct   [BELOW median]  called "massive": YES
vpos 68 SHORT ×4.3  ->  7th pct   [BELOW median]  called "massive": YES
vpos 76 SHORT ×4.7  -> 18th pct   [BELOW median]  called "massive": YES
vpos 81 SHORT ×4.9  -> 23rd pct   [BELOW median]  called "massive": YES
vpos 73 LONG  ×4.7  -> 24th pct   [BELOW median]  called "massive": YES
vpos 80 SHORT ×5.0  -> 25th pct   [BELOW median]  called "massive": YES
vpos 71 LONG  ×4.8  -> 28th pct   [BELOW median]  called "massive": YES
vpos 79 LONG  ×5.3  -> 44th pct   [BELOW median]  called "massive": YES
vpos 77 SHORT ×6.0  -> 45th pct   [BELOW median]  called "massive": YES
vpos 69 LONG  ×5.4  -> 47th pct   [BELOW median]  called "massive": YES
vpos 82 LONG  ×5.4  -> 47th pct   [BELOW median]  called "massive": YES
vpos 66 SHORT ×5.8  -> 42nd pct   [BELOW median]  called "massive": YES
--- above median ---
vpos 72 ×5.6 (52nd) · vpos 78 ×5.6 (52nd) · vpos 70 ×6.0 (60th)
vpos 74 ×14.6 (96th) · vpos 75 ×16.0 (99th) · vpos 67 ×30.8 (100th)
```
**All 18 entries were told about a "massive" wall. 12 of the 18 were below the book's median.**
Only three (vpos 74, 75, 67) were genuinely extreme — and vpos 74 and 75 both lost, while the two
lowest-percentile SHORTs (76 at 18th, 81 at 23rd) both won. That is a hint, at n=18, and nothing
more; it is item W3 on the open list.

**This is a defect in our prompt construction, not in the model's reasoning.** The model is being
handed an unconditional label and no scale, and is behaving reasonably given what it is told.

---

# PART 2 — Exit advisor

## 2.4 It is wired, and it has never run

```
claude_advisor.py:338   def consult_for_close(...)
main.py:2227            advice = claude_advisor.consult_for_close(...)
main.py:1539, 2956      -> _handle_5m_close_via_ai(...)
```
Invocations, ever: **zero.** Every status that path can write is absent from the database:
```
ai_pending · ai_hold · close_failed · no_position · ambiguous_side · group_b_logged   ->  0 rows each
```
(`claude_unavailable` = 26 rows all belong to the **entry** path.)

**Root cause** — `_handle_5m_close_via_ai` finds the position through `_fetch_open_position()`:
```python
positions = exchange.fetch_positions([symbol])      # the LIVE exchange
```
In paper mode there are no exchange positions. `open_pos` is always `None`, the handler returns
`trend_reset`/`group_b_logged` and **exits before the advisor line is ever reached**. The exit
advisor keys off live state while the entire book lives in `virtual_positions`.

Its payload and reason **would** be persisted like the entry side (`_ai_fields_from_advice` →
`ai_user_prompt` / `ai_reason`), but there is nothing to persist.

## 2.5 The 9 `external` closes — traced

| vpos | closed | close row | actual caller |
|---|---|---|---|
| 54, 60, 64, 75, 76 | 06-13 … 07-17 | 7726, 11622, 12961, 15955, 16373 | **`15m_armed_exit`** — signal-driven armed exit (`EXIT_CONFIRM_TF='15m'`) |
| 35, 36, 38, 42 | 05-25 … 05-27 | *(no close row linked)* | pre-dates `trades_close_row_id` linking; same external path |

**None** was the exit advisor.

## 2.6 What the exit advisor *would* see (verbatim, from the code)

```
Open position:
  Symbol: {symbol}
  Side: {position_side}
  Entry: {entry_price}
  Unrealized PnL: ${unrealized_pnl:.2f}
  Age: {age_minutes:.0f} minutes

Incoming 5m exit signal: {exit_signal_name!r}

Upper-timeframe state:
  1H: {signal_name} ({direction})
  15m: {signal_name} ({direction})

Decide whether to close the position now or hold it (on-exchange SL/trail are still active).
```
System prompt: *"…Decide whether to close the position now or hold… Respond with ONLY a single JSON
object… close (true|false), confidence, reason (max 80 chars)."*

**Six fields, two of them names.** It does **not** receive: the order book (entry-time or current),
MFE / peak, giveback from peak, distance to SL, unrealised R (it gets dollars, not R), regime at
entry vs now, ADX/ATR/volume, or the entry rationale that justified the position in the first place.
It is asked to overrule a position it knows almost nothing about, on 80 characters of justification.

## 2.7 What actually decides exits, in priority order

From `virtual_trader._process_position`:
```
1)  water mark update            (observational)
1b) MAE update                   (observational)
1d) excursion sample             (observational — read by NO exit logic)
1c) post-entry recheck T+10/60/300s   -> EMERGENCY_CLOSE or TIGHTEN (bounded since 93c20c3)
1d) LONG partial @ +1R           (new, f7df202)
2)  breakeven at +1R             -> SL to breakeven, trail arms
3)  STOP-LOSS                    -> hard close
4)  TRAILING STOP                -> close  (only after breakeven)
```
Plus, from `main.py`, outside the poller: **1H exit-signal arms** (`exit_armed`, 24) → **15m
BOS/CHOCH/Liquidity-Grab in the opposite direction** fires the close (`15m_armed_exit`, reason
`external`). `exit_unarmed_noop` (327) = a 15m confirmation arrived with nothing armed.

**No model is in the exit path at all.** Exits are: SL, trail, armed-signal, and the recheck's
emergency branch.

---

# PART 3 — The gap

| signal | EXISTS | REACHABLE AT EXIT TIME | USED TODAY |
|---|---|---|---|
| **Position state** (entry, elapsed, uPnL, SL distance) | ✅ `virtual_positions` | ✅ in the poller every 10s | ⚠️ **partly** — SL distance and uPnL drive SL/trail/breakeven; elapsed time drives nothing |
| **Unrealised R** (uPnL ÷ original stop) | ✅ derivable | ✅ | ❌ — the trail works in % of water mark, never in R |
| **Excursion shape** — is the peak still advancing? | ✅ `position_excursion_samples`, 2,218 rows / 22 pos | ✅ sampled live | ❌ — the code comment says it outright: *"read by NO exit logic"* |
| **Giveback from peak** | ✅ `smart_exit_dryrun_samples.giveback_pct`, hourly on every open position | ✅ | ❌ — DRYRUN only, `would_exit` is logged and discarded |
| **Order-book DYNAMICS since entry** | ✅ **both halves exist**: entry snapshot (`entry_sup_wall_mult`, `entry_opp_wall_dist_pct`, `entry_ob_imbalance`, `entry_n_walls_*` — 18 of 56 positions, all since 07-04) **and** live book in the dryrun sampler | ✅ comparison is computable today | ⚠️ **computed, then discarded** — the recheck calculates `wall_ratio` (current ÷ entry) and its score weight is **0** since `c845941`; the dryrun logs the rest |
| **Book PERCENTILE context** (is this book full or empty?) | ✅ `orderbook_density`, 17,859 snapshots | ✅ | ❌ — *"Read by NO gate/exit/sizing/advisor"* |
| **HTF regime flip since entry** | ✅ entry regime stored; `trend_15m_live` / `trend_5m_live` / `mom_flip_15m` / `mom_flip_5m` sampled hourly | ✅ | ❌ — logged only. The 1H exit-signal arm is a *signal*, not a regime comparison |
| **Volume drying up** | ✅ `vol_ratio_1h`, `vol_ratio_15m`, `atr_change_pct` sampled hourly | ✅ | ❌ — logged only |
| **Entry thesis still valid** | ✅ `trades.ai_reason` + `ai_user_prompt` persisted per entry, cross-linked by `trades_entry_row_id` | ✅ one lookup by id | ❌ — nothing reads it after entry; the exit advisor's prompt does not include it |

**Summary of the gap.** Every input a competent exit decision would want **already exists and is
already being sampled**, on an hourly cadence, on every open position — the smart-exit dryrun logger
alone captures 48 columns including giveback, both walls, imbalance, ADX on three timeframes,
volume ratios, ATR change and live 15m/5m trend. **None of it reaches any exit decision.** The exit
path consumes exactly two numbers: current price versus a stop level, and current price versus the
water mark.

The one model that *could* consume more is asked instead for a yes/no on six fields — and has never
been invoked.

**Nothing proposed.** No thresholds, no new advisor design, no re-wiring. This report says only what
the two advisors see, what they miss, and what we already hold.

---

Session commits: `93c20c3` · `596fbdf` (superseded) · `b878535` · `f7df202`.
Tree clean, `titan.service` healthy, Mercury-SOL untouched.
Open items tracked in `reports/OPEN-ITEMS.md` — items 4 and 5 there are now answered by this report.
