# TITAN — THE GEOMETRY ARITHMETIC, AUDITED: 1R, THE STOP, THE TRAIL, THE PARTIAL

**2026-08-06 00:50 UTC · READ-ONLY · nothing changed, nothing committed · HEAD `7c2feac`**

The second of the three areas the 19:55 scope note left unaudited. `order_adapter` is closed
(F1/F2/F3/F4/F7/F9c); the optimizer remains.

**`openitems_guard.py` exit 0** — canon runtime HEAD `7c2feac`, 11 watched values, header and
current-state table agree. Working tree clean, service `active` since 00:25:54, `NRestarts=0`,
0 open positions.

**Runtime flags, read by importing `config`:** `SL_ATR_MULT = 2.25` · `TRAIL_MULT_ATR = 1.6875` ·
`SL_ATR_TF = 1h` · `TRAIL_ATR_TF = 1h` · `ATR_LEN = 14` · `FIXED_NOTIONAL_MODE = True` ·
`LONG_PARTIAL_ENABLED = True` · `ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True` ·
`WALL_TRAIL_LIVE_ENABLED = False`.

🔴 **The boundary is real and it is total: 0 positions opened after 2026-08-04 17:01:29, and 0
closed after it.** Every measurement below that involves a closed trade is measured on the OLD
geometry. Nothing in the new geometry has been exercised by a single trade.

---

## §1 — 1R: ONE DEFINITION, OR SEVERAL?

### (a) Every site that computes or recovers 1R — and the one with the divide

**The `|entry − sl| / SL_ATR_MULT` shape exists in exactly ONE place**, the one the canon names:
`main._resume_job_if_needed` (`main.py:5357`):

```python
atr_val = atr if atr else abs(entry_price - sl_price) / max(SL_ATR_MULT, 1e-9)
```

**Still unreachable, confirmed by execution, not by reading:** `virtual_trader.engine_owns_position()`
returns **True**, and `_resume_job_if_needed` returns at its first line under that guard;
`breakeven_jobs` holds **0 rows**. Both doors, independently. ✅

**No other site divides by `SL_ATR_MULT`.** Every other consumer of the constant *multiplies* it at
entry time. The full inventory:

| site | what it does | reachable? |
|---|---|---|
| `virtual_trader.execute_entry:758,855` | `sl_distance_price = SL_ATR_MULT × atr_sl`; `sl_price = fill ∓ …` | ✅ **the live entry path** |
| `main._execute_entry:1470,1522` | same arithmetic, legacy | ❌ routed away by `engine_owns_position()` |
| `main._resume_job_if_needed:5357` | ⬆ the divide | ❌ dead, two guards |
| `main._reconcile_side:5437` | `atr_sl = entry ∓ SL_ATR_MULT × atr_rec` — 3rd-choice fallback for reporting | ✅ but see **G5** |
| `main._reconcile_side:5460` | fallback-ATR re-attach | ✅ and see **G3** |
| `virtual_trader:865`, `main:1534` | `_sl5d`/`_sl1d` dryrun log lines | ✅ observational only |

### (b) `initial_risk_usdt` — written once, never recomputed ✅ (with one caveat, G4)

Written exactly once, in the `INSERT` at `virtual_trader.py:1011`, from `realized_risk_usdt`. **No
`UPDATE` anywhere touches it** — grepped across every module. **No consumer derives R from the
current constant**: `close_report.build_close_report` prefers the stored `initial_risk_usdt` and
falls back to `size × |entry − original_sl|` — both stored, neither `SL_ATR_MULT`.
`post_exit_observatory._compute_shadow_pnl` uses `|entry − original_sl_price|`. `main.py:352/436`
aggregate `vp.initial_risk_usdt`. **A post-boundary read of a pre-boundary row is therefore correct,
not wrong by 10%.** ✅

### (c) 🔴 The four +1R consumers — verified to be ONE number, not four that agree

All four read the **stored per-position `original_sl_price`**, and none of them touches
`SL_ATR_MULT` or re-derives an ATR:

| consumer | source | code |
|---|---|---|
| exit advisor `upnl_r` / `dist_sl_r` / `mfe_r` / `giveback_r` / `arm_level` | `main.py:2934` | `osl = vpos.get('original_sl_price') or vpos['sl_price']`; `r_dist = abs(fill − osl)` |
| LONG partial +1R trigger | `virtual_trader.py:2631` | `_fill_p + _one_r_distance(_fill_p, _orig_sl_p) × LONG_PARTIAL_LEVEL_R` |
| breakeven arm | `virtual_trader.py:2645` | `_breakeven_reached(side, fill, _orig_sl, last)` → `_one_r_distance(fill, original_sl)` |
| trail arm | **the same event** — the trail is armed inside the `if not be_applied` block, so it is not a fourth test at all | `virtual_trader.py:2688-2733` |
| *(breakeven_worker `r_dist = abs(entry − orig_sl)`, `:754`)* | dead — `breakeven_jobs` = 0 | |

**And the dollar 1R agrees with the price-distance 1R on every live row**, checked against the book
rather than asserted:

```
vpos 86: |entry−osl|=1081.10  initial_risk_usdt=2.4866  size×dist=2.4865
vpos 87:            809.90                     1.8628             1.8628
vpos 88:            779.10                     1.7918             1.7919
vpos 89:            722.20                     1.6610             1.6611
vpos 90:            873.50                     2.0091             2.0090
vpos 91:            575.40                     1.3234             1.3234
vpos 92:            780.90                     1.7960             1.7961
```

**7/7 agree to four decimals. §1 passes.** This is the cleanest part of the geometry.

---

## §2 — THE STOP AND THE TRAIL

### (a) Which ATR the stop is built from — and the forming candle, measured

`virtual_trader.execute_entry`: `atr = _true_atr(fetch_ohlcv('5m', 42), 14)`,
`atr_1h = _true_atr(fetch_ohlcv('1h', 42), 14)`, `atr_sl = atr_1h` (since `SL_ATR_TF = '1h'`).
Wilder, seeded on a simple mean of the first 14 TRs, over a **42-bar** window.

**The forming candle IS included — verified live, not inferred:**

```
bars returned       : 42          last bar open : 2026-08-06T00:00:00 UTC
now                 : 00:46:27    age of last bar: 46.5 min  -> FORMING
ATR incl forming bar (what the bot uses) = 248.4400
ATR on CLOSED bars only                  = 255.8200
difference                               = −7.3800 (−2.885%)
-> stop distance differs by −16.61 price units RIGHT NOW
```

Canon §0 records forming-candle reads as by-design for ATR/ADX/EMA, so this is consistent with the
design. **The consequence is a stop width that depends on WHEN IN THE HOUR the entry fires**: a
1h bar 5 minutes old contributes a nearly-empty true range and pulls ATR down, so the same market
gives a tighter stop and a smaller dollar 1R. The seven live entries fired at minute 50, 5, 35, 20,
25, 40 and 25 of their hour — spread across the range, with n=7 far too small to test the effect.
**I am recording the mechanism, not claiming the correlation.**

**The R arithmetic later does NOT re-derive this ATR** — it uses the frozen price distance
`|entry − original_sl|`. So the forming-candle read makes the stop width noisy but leaves R
internally consistent. That is the saving grace, and it is worth saying explicitly.

### (b) Trail-in-R on live values, not on the formula

```
ATR_1h = 248.4400   BTC = 64,656.20
stop distance  = 2.25   × ATR_1h = 558.99  (0.8646%)
trail_pct      = round(1.6875 × ATR_1h / px × 100, 3) = 0.648%  ->  418.97
TRAIL-IN-R ON LIVE VALUES = 0.749516     formula says 0.750000     Δ = −0.000484R
```

Both read the **same** `atr_1h` object inside one `execute_entry` call — no second fetch, no cache
divergence. The −0.000484R is **entirely** the 3-decimal rounding of `trail_pct` (see **G8**). The
formula holds. ✅

**But it holds only at the entry price — see G1, which is the largest finding in this audit.**

### (c) The wall-anchor question does not apply — the premise does not hold

The brief asks whether `initial_risk_usdt` on a wall-anchored stop is computed from the actual stop
or the ATR one. **Neither: the wall anchor never sets an entry stop at all.**

`_would_wall_stop` is called from `_record_smart_exit_dryrun` — a **per-tick, hourly-throttled
observation on an ALREADY-OPEN position**, long after `initial_risk_usdt` was written. It is a
pure function returning `(sl_price, route)` that is written to `smart_exit_dryrun_samples` and read
by nothing in the exit path. There is no wall-anchored entry stop in this codebase.

**So `WALL_ANCHOR_DRYRUN_ENABLED = True` is not the only thing preventing it — it is not even the
relevant switch.** The one that could move a stop is `WALL_TRAIL_LIVE_ENABLED`, which is **False**,
and even when true it moves `sl_price` (a *trail* on an open position), never `original_sl_price` —
which is what 1R is measured from. **R would stay correct even if it were enabled.** ✅

---

## §3 — THE PARTIAL

### (a) The +1R trigger reads the STORED stop, not the current ATR ✅

```python
_orig_sl_p = row['original_sl_price'] if … else row['sl_price']
_lvl = _fill_p + _one_r_distance(_fill_p, _orig_sl_p) * float(LONG_PARTIAL_LEVEL_R)
```

Frozen at entry. ATR moving afterwards cannot move the trigger. ✅

### (b) `initial_risk_usdt` is NOT shrunk by the partial ✅

`_take_long_partial`'s only write is
`UPDATE virtual_positions SET filled_legs=?, partial_taken=1, realized_partial_usdt=…`. It does not
touch `initial_risk_usdt`, `initial_fill_price` or `original_sl_price`, so 1R stays anchored to the
position's own entry and stays comparable to the other rows in the book. ✅

### (c) Breakeven fees — both legs, computed once ✅ (with G7)

`offset = 2 × TAKER_FEE_RATE + BREAKEVEN_BUFFER_PCT` = 2×0.05% + 0.1% = **0.20%**, applied as
`entry × (1 ± offset)`. Both round-trip taker legs plus a cushion. Computed **once**, structurally:
the whole block sits under `if not be_applied`, and the same transaction writes
`mgmt_state.breakeven_applied = True`. Identical formula in `breakeven_worker._breakeven_price`. ✅

*(The exit leg's fee is charged on a notional 0.2% larger than entry's, so `2 × taker` under-covers
by ~0.00005% — dwarfed by the 0.1% buffer. Not a finding.)*

---

## §4 — THE FINDINGS

### 🔴 G1 — THE TRAIL GIVES BACK A PERCENTAGE OF THE WATER MARK, NOT OF THE ENTRY. MEASURED SKEW: LONG +1.63%, SHORT −4.09%.

`trail_pct` is computed **against the entry price**:

```python
def _trail_pct_for(initial_fill_price, atr):
    return round(TRAIL_MULT_ATR * atr / initial_fill_price * 100, 3)
```

and then applied **against the water mark**:

```python
trigger = water_mark * (1.0 - trail_pct / 100.0)     # LONG
trigger = water_mark * (1.0 + trail_pct / 100.0)     # SHORT
```

Those are different bases. The giveback in R therefore **drifts with MFE, in opposite directions on
the two sides** — for a LONG the water mark rises above entry so the same percentage is a *larger*
absolute distance; for a SHORT it falls below entry so the same percentage is a *smaller* one.

**Measured on the 14 positions that actually closed on the trail** (mechanism isolated from
gap/slippage: `mechanism giveback = water_mark × trail_pct`):

| side | n | mechanism giveback | nominal (`pct × entry`) | skew |
|---|---|---|---|---|
| **LONG** | 3 | **1.0160R** | 0.9997R | **+0.0163R (+1.63%)** |
| **SHORT** | 11 | **0.9591R** | 1.0000R | **−0.0409R (−4.09%)** |

Modelled forward on today's live values, at the new 0.75R geometry:

```
MFE 1.0R -> trail gives back 0.7560R      MFE 2.0R -> 0.7625R      MFE 3.0R -> 0.7690R
documented/claimed = TRAIL_MULT_ATR / SL_ATR_MULT = 0.7500R
```

**0.7500R is exact only when `water_mark == entry` — which never happens, because the trail arms at
+1R.** The config comment, the canon and the 2026-08-04 change all describe the trail as "0.75R";
the mechanism delivers 0.756R at the arming moment and more as the trade runs, on longs, and less
on shorts.

🔴 **Why this one matters most: it is the exact parameter the 2026-08-04 optimization tuned.** That
run chose 1.6875 to buy a 0.75R giveback, on a grid whose R-axis is this quantity. If the backtest
computed giveback as `pct × entry` while the engine computes `pct × water_mark`, the chosen cell was
selected against a number the engine does not produce — and the side-asymmetry (+1.63% / −4.09%)
runs in the same direction as the LONG-vs-SHORT gap the partial exists to fix. **I have not read the
optimizer** — it is the third unaudited area — so I state this as the question the optimizer audit
must answer first, not as a conclusion.

### 🔴 G2 — THE PARTIAL'S BANKED PnL NEVER REACHES THE CLOSE REPORT. MEASURED: 0.365R AND $18.91 MISSING, ALREADY IN THE BOOK.

`virtual_trader._do_close`:

```python
report  = close_report.build_close_report(…)   # r_multiple computed HERE, from the remainder only
net_pnl = report.net_pnl
…
_rp = row['realized_partial_usdt'] or 0.0
if _rp:
    net_pnl += _rp                              # ← a LOCAL variable. `report` is never updated.
```

The corrected `net_pnl` goes to the DB row and to `trades.pnl`. **`report` keeps the
remainder-only figures**, and `report` is what three separate consumers read:

| consumer | reads | consequence |
|---|---|---|
| `send_tg(report.telegram())` | `net_pnl`, `r_multiple` | **the operator's close report understates both** |
| `main._running_block_fn` | `nets.append(report.net_pnl)`, `r_vals.append(report.r_multiple)` | the running batch block's PnL, win rate and mean-R |
| `post_exit_observatory.on_real_close` | `net`, `r_mult` | the observatory's record of the trade |

**Measured on vpos 82 — the only position in 92 that ever took a partial, and it is in the book right
now:**

```
stored net_pnl (whole, incl. partial)  = +53.7926      -> +1.0386R
realized_partial_usdt                   =  18.9071
remainder-only (what the report saw)    = +34.8855      -> +0.6736R
                                                   GAP  =  0.3651R  and  $18.91
```

`ClosedTrade`'s own docstring reads *"net_pnl is authoritative for DB + Telegram"* — the DB gets the
corrected number and Telegram gets the uncorrected one. **The comment describes a property the code
does not have** (that is **G6**, and it is the same root).

**Armed now:** `LONG_PARTIAL_ENABLED = True`, fires on the first live LONG at +1R. This is the
"ONE FACT, MANY JUDGES" class, with the judges already disagreeing on a row that exists.

### 🔴 G3 — THE BOOT RE-ATTACH FALLBACK USES THE 5m ATR WHILE THE ENTIRE GEOMETRY IS 1h. THE STOP WOULD BE 0.191× THE INTENDED DISTANCE.

`main._reconcile_side`, the naked-position branch:

```python
atr = true_atr(exchange.fetch_ohlcv(symbol, '5m', limit=ATR_LEN * 3))     # ← 5m
raw = entry_price - SL_ATR_MULT * atr           # LONG
trail_pct = round(TRAIL_MULT_ATR * atr / entry_price * 100, 3)            # ← 5m again
```

`SL_ATR_TF` and `TRAIL_ATR_TF` are **both `'1h'`**. Measured now:

```
ATR_5m = 47.5332      ATR_1h = 248.4400      ratio = 5.227×
intended stop = 2.25 × ATR_1h = 558.99  (0.8646%)
this branch   = 2.25 × ATR_5m = 106.95  (0.1654%)   -> 0.191× the intended distance
```

A stop **5.2× too tight**, re-attached to a live position that has just been found naked after a
restart — a 0.165% stop on BTC is inside ordinary minute-to-minute noise and would very likely be
taken out almost immediately. The trail it enqueues is wrong by the same factor.

It is alerted (`⚠️ fallback ATR SL used … Verify the level`), which is why this is **money-losing but
not silent**. **0 occurrences ever.** It is reachable: it needs a live position with no stop *and*
`_recover_sl_from_trades` to return nothing — a failed lookup or an entry price outside
`RECONCILE_ENTRY_TOLERANCE_PCT`.

### 🟠 G4 — `initial_risk_usdt` IS COMPUTED FROM THE REQUESTED SIZE, BEFORE THE FILL, AND NEVER RECOMPUTED.

In `execute_entry`, `realized_risk_usdt = amount × sl_distance_price` is computed at line ~770 using
the **pre-fill, requested** `amount`. At line ~853, after the order returns,
`amount = _entry_fill['amount']  # EXECUTED size, not the requested one`. **`realized_risk_usdt` is
not recomputed**, and the `INSERT` writes the stale value alongside the executed `amount`.

On a **full** fill they are identical — which is why all 7 live rows agree to four decimals. On a
**partial entry fill** the stored dollar 1R overstates the risk by the fill ratio, so every
`r_multiple` on that position is understated by the same ratio. Item 14 (partial fills on entry)
is confirmed not implemented; **this is a consequence of it that the item-14 note does not mention.**

### 🟠 G5 — THE STORED `atr` COLUMN IS THE 5m ATR; THE STOP IS BUILT FROM THE 1h ONE. A 5.35× TRAP.

`execute_entry` returns `'atr': atr` — the **5m** value — and that is what is written to both
`virtual_positions.atr` and `trades.atr`, on a position whose stop is `2.25 × ATR_1h`. Measured
against the book:

```
vpos 86: stored atr = 80.80    implied ATR_1h from the stop = 432.44   (5.35×)
vpos 90: stored atr = 162.23   implied ATR_1h              = 349.40   (2.15×)
vpos 91: stored atr = 54.35    implied ATR_1h              = 230.16   (4.23×)
```

Any code that reconstructs this position's geometry from the stored `atr` is wrong by that ratio.
Two consumers do:

- `main._recover_sl_from_trades` returns it as `atr`, and `_reconcile_side:5437` computes
  `atr_sl = entry ∓ SL_ATR_MULT × atr_rec` — third-choice fallback behind the real stop price, so it
  affects a reported level rather than a placed one today;
- the entry Telegram report renders `📈 ATR: {entry['atr']:.2f}` next to a stop the number does not
  explain. `config.py:192` already warns *"NOT the 5m atr shown in entry logs"* — **the warning
  exists precisely because the column is misleading, and the column was left misleading.**

### 🟡 G6 — `ClosedTrade`'s "authoritative for DB + Telegram" is false for the DB *and* Telegram simultaneously.

Same root as G2, named separately because it is the doc-vs-code instance: the two consumers the
docstring binds together receive **different numbers** whenever a partial was taken.

### 🟡 G7 — "the trade can no longer lose" ignores funding.

The breakeven offset covers 2 × taker + a 0.1% slippage cushion. It does **not** include
`funding_paid`, which is a tracked column (`close_report.funding_for_close`) and is subtracted from
`net_pnl` at close. A position held through enough funding periods **can** close below zero after
breakeven. The claim in `config.py:203` and in the Telegram message (*"trade can no longer lose"*)
is stronger than the arithmetic supports.

### ⚪ G8 — `trail_pct` is rounded to 3 decimal places.

`round(…, 3)` on a percentage. At BTC $64.6k one unit in the third decimal is $0.65, so the stored
trail is quantised to ±$0.32 on a ~$419 trail — **±0.08% of the trail width**, and the entire source
of the 0.749516-vs-0.750000 gap in §2b. Correct, small, and worth knowing before anyone hunts that
0.0005R.

### ⚪ G9 — the breakeven Telegram reads the stale row after the UPDATE.

`virtual_trader.py:2739` renders `trail {row['trail_pct']}% active` **after** the transaction wrote
`new_trail`. `row` is the pre-UPDATE snapshot. No-op today because
`ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True` writes the frozen value straight back — **wrong the moment
that flag is turned off**, which is exactly what the flag exists to enable.

### Arithmetic that has never executed

`_resume_job_if_needed`'s ATR recovery (2 guards) · every `breakeven_worker` job handler
(`breakeven_jobs` = 0) · `_reconcile_side`'s fallback-ATR branch (**G3**, 0 occurrences) ·
`adaptive_trail`'s fresh-value persistence (`DRYRUN = True`, so `chosen_pct` is computed, logged and
discarded) · the wall-anchor ratchet (`WALL_TRAIL_LIVE_ENABLED = False`) · the entire risk-based
sizing branch including the max-margin cap (`FIXED_NOTIONAL_MODE = True`) · `main._execute_entry`'s
whole geometry block (routed away by `engine_owns_position()`).

---

## §5 — VERDICT: RANKED BY RUNS × COST, AND SPLIT BY WHAT IT BREAKS

| # | finding | runs | 🔴 **MISPLACES MONEY** / 📏 **CORRUPTS MEASUREMENT** | rank |
|---|---|---|---|---|
| **G1** | trail gives back `pct × water_mark`, not `pct × entry` — measured **LONG +1.63% / SHORT −4.09%** vs nominal | **every trailed exit** | 🔴 **BOTH.** It moves where the exit actually sits (money) **and** it makes the documented "0.75R" wrong (measurement) — and 0.75R is the number the 2026-08-04 change was chosen on | 🔴 **1** |
| **G2** | the partial's banked PnL never reaches `report` — Telegram, batch block and observatory all understate | **armed; first live LONG at +1R** | 📏 **MEASUREMENT ONLY** — the DB row and `trades.pnl` are correct. But it is the number the operator reads and the optimizer scores. **Already materialised: vpos 82, 0.365R / $18.91** | 🔴 **2** |
| **G3** | boot re-attach fallback uses the **5m** ATR — stop at **0.191×** the intended distance | 0 so far; every boot that finds a naked position with no recoverable stop | 🔴 **MONEY.** A 0.165% stop on a live position; near-certain immediate stop-out. Alerted, so not silent | 🔴 **3** |
| **G4** | `initial_risk_usdt` from the **requested** size, never recomputed after the fill | every entry; only *wrong* on a partial fill | 📏 **MEASUREMENT** — every R on that position off by the fill ratio | 🟠 **4** |
| **G5** | stored `atr` is 5m; the stop is 1h — **5.35×** on vpos 86 | every entry writes it; 2 consumers read it | 📏 **MEASUREMENT** today (a reported level, a Telegram line). Becomes 🔴 money if any future code sizes or places from it | 🟠 **5** |
| **G6** | `ClosedTrade` docstring claims one authoritative `net_pnl`; DB and Telegram get different ones | with G2 | 📏 measurement / doc | 🟡 **6** |
| **G7** | breakeven "can no longer lose" excludes funding | every breakeven | 🔴 small money, 📏 false claim | 🟡 **7** |
| **G8** | `trail_pct` quantised to 3 dp (±0.08% of trail width) | every position | 🔴 negligible money | ⚪ **8** |
| **G9** | breakeven Telegram reads the stale row | every breakeven | 📏 latent — wrong only once `ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN` is off | ⚪ **9** |

### What is clean, verified by construction rather than assertion

**§1 is the strongest part of this codebase's geometry.** The four +1R consumers are **one number**,
not four that happen to agree: all read the stored `original_sl_price`, none re-derives an ATR, and
the trail arm is not even a separate test — it fires inside the breakeven block. The dollar 1R and
the price-distance 1R **agree to four decimals on all 7 live rows**. `initial_risk_usdt` is written
once and never rewritten, and **no consumer anywhere derives R from the current constant** — so the
1R boundary does not corrupt any historical read. The `|entry − sl| / SL_ATR_MULT` divide the canon
warned about exists in exactly one place and is dead behind two independent guards. The partial
leaves 1R anchored to the position's own entry. The wall anchor cannot touch `initial_risk_usdt`
because it never sets an entry stop at all.

### The through-line

The last three audits found *a number that came back was replaced by a number we asked for*, then
*a mechanism trusted to behave a way nobody checked*. **This one is a third shape: two quantities
that are equal at one instant, and are then used as if they stayed equal.**

- **G1** — `trail_pct` is a fraction *of the entry*, applied *to the water mark*. Equal at entry,
  never again, and the divergence has a sign that depends on which side you are on.
- **G2** — `report.net_pnl` and the row's `net_pnl` are the same number until a partial is taken;
  the code corrects one and leaves three consumers reading the other.
- **G5** — the stored `atr` and the ATR the stop was built from were the same field before
  `SL_ATR_TF` moved to 1h. The config comment records the divergence; the column was never fixed.

**The boundary that makes all of this urgent is not the one the brief pointed at.** 1R itself
survives the 2.5 → 2.25 change cleanly — that was checked and it passes. What does *not* survive
inspection is the claim that the new geometry gives back **0.75R**: G1 says the engine gives back
0.756R and rising on longs, less on shorts, and **zero positions have closed on the new numbers**, so
nothing has yet contradicted it out loud.

**No fixes proposed. This is the map.**

---

*Read-only throughout: no file changed, no commit made, no order sent. Every number above was read
from the live exchange, the live `trades.db`, or by importing `config` at runtime — none copied from
a previous report. Working tree clean at `7c2feac`; `openitems_guard.py` exit 0 before and after.*
