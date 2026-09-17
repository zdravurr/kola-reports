# BULL-DAILY SHORT GATE — **ARMED AND LOADED**, restarted under an open position, 39 of 39 fields identical

**2026-09-17 16:59 UTC · Mercury-SOL · APPLIED · Titan untouched · COHORT BOUNDARY 2026-09-17 16:55:13 UTC**

`openitems_guard` → **exit 0** before, **exit 0** after.

---

## 🔴 RESULT: BOTH CHANGES LIVE. THE PROTECTIVE STOP WAS NOT TOUCHED.

| | |
|---|---|
| restart issued | **16:55:00.006 UTC** (5-min boundary, rc=0) |
| service up | 16:55:13 UTC · PID 2245907 → **3077029** · `NRestarts=0` |
| #48 fields compared | **39 / 39 IDENTICAL** |
| venue stop `orderId` | `d88cfa8d-41d0-4714-9ad9-347738bb7fba` — **unchanged** |
| venue stop `updatedTime` | `1789635920320` — **unchanged** 🔴 the restart did not write to the stop |
| armed exit | survived byte-identical |
| loaded-bytecode mismatches | **0** |

---

## 1. THE TWO CHANGES

### 1a) The bull-daily short gate — `main.py:5374`, ARMED
Refuse a SHORT when `trend_1d == 'bull'`. `bear` and `neutral` pass. LONG untouched, 4h untouched.
`BULL_DAILY_SHORT_BLOCK_ENABLED=True`, `BULL_DAILY_SHORT_BLOCK_DRYRUN=False`.

Placed at the corrected insertion point you approved — after the advisor falls through, immediately before
`# Execute single-entry order`. The last gate before the order leaves.

**Fail-open, proven by execution: 20 paths, 0 failures.** Missing key, `None`, `''`, `'   '`, `'bullish'`,
int/list/dict, `snap=None`, snap with no `.get`, a snap whose `.get()` **raises**, kill switch, DRYRUN — every
one ADMITS. The only route to a refusal is `side=='SHORT'` AND a normalised literal `'bull'`.

The config comment is in place **verbatim** as dictated, together with the pre-registration and the review
point.

### 1b) The 608 dropped refusals — fixed, and 🔴 **NOT back-filled**
`entry_gate_refused` added to `TRACKED_STATUSES`. The hook was already called at `main.py:4780`; only the
registration was missing.

**History is PARTIALLY recoverable and I have not touched it.** On the 608 rows (2026-08-08 20:10 → 2026-09-17
12:10):

* **survives 608/608:** `timestamp`, `side`, `signal_type`, `confluence_score`, `market_regime`, `error`
* **absent 0/608:** `price`, `matrix_direction`, `srv_adx_1h`, `trend_1d`, `trend_4h`, `orderbook_json`

The skip **anchor** is reconstructible, and `price_at_skip` plus the 15m/1h/4h/12h/24h drift could be
**recomputed from historical klines** — but *computed*, not *sampled*, unlike the 87,910 live-sampled drift
rows; mixing them silently would corrupt the observatory's comparability. The **order-book context**
(`nearest_wall_price`, `wall_strength`, `wall_distance_pct`) is **permanently lost** — historical depth is not
retrievable from any venue endpoint. Your call; any back-fill needs a provenance flag.

### 1c) AST walker — **8 of 8 ✅, 0 failures**
```
✅ ai_skipped (5338)   ✅ below_threshold (4725)  ✅ htf_blocked (4200)   ✅ risk_halt (4803)
✅ book_blocked (5076) ✅ flat_adx_blocked (4992) ✅ bull_daily_blocked (5387) ✅ entry_gate_refused (4780)
```
Both new statuses **registered AND called**. No abort condition.

---

## 2. THE RESTART UNDER AN OPEN POSITION

### 2a) Snapshot taken to file first
`snapshot_48_BEFORE.txt` — full 39-field `virtual_positions` row, `exit_pending`, `active_positions`, both
venue position indices, and the conditional order. **All three venue error lists EMPTY.**

### 2b) Mid-flight check — clear
No entry in progress (0 matching log lines in 10 min), no close, no partial (`partial_*` all NULL), no
consultation in flight. **The armed exit stood at 161 of 360 minutes** — armed 14:00:14, expires 20:00:14,
restart at 16:55, so ~3h05m of margin on either side. Next hourly advisor consult was 17:06:17, eleven minutes
clear of the restart.

### 2c) The venue read — succeeded this time, and here is why
The 16:16 pass failed 24/24 on CloudFront 403. That was **one Tor circuit reused 24 times**. The bot's own
`tor_retry` uses SOCKS-auth stream isolation — a random SOCKS username per attempt keys `IsolateSOCKSAuth` onto
a **new circuit and a new exit IP**. Reading through isolated circuits: **0 failed attempts on all four venue
reads, before and after.** The snapshot is real, not an absence.

### 2d) Timed to the boundary
Issued at **16:55:00.006 UTC**.

### 2e) 🔴 FIELD-BY-FIELD — 39 of 39 identical

| field | before | after |
|---|---|---|
| `water_mark` | **101.73** | **101.73** ✅ |
| `mgmt_state_json` | `{"breakeven_applied": false, "exit_advisor_last_ts": 1789661177.103648}` | identical ✅ |
| `fills_json` | `[{"price": 100.37, "size": 0.9, "fee": 0.090333, …}]` | identical ✅ |
| `sl_price` / `original_sl_price` | 98.2 / 98.2 | 98.2 / 98.2 ✅ |
| `size` / `status` | 0.9 / `open` | 0.9 / `open` ✅ |
| `max_adverse_price` | 99.5 | 99.5 ✅ |

**Venue:**

| | before | after |
|---|---|---|
| stop `orderId` | `d88cfa8d-41d0-4714-9ad9-347738bb7fba` | **unchanged** ✅ |
| stop `updatedTime` | `1789635920320` | **unchanged** ✅ |
| stop `createdTime` / `triggerPrice` / `qty` | `1789635919201` / 98.2 / 0.9 | unchanged ✅ |
| position `updatedTime` | `1789660800009` | **unchanged** ✅ |
| position size / avgPrice / stopLoss | 0.9 / 100.37 / 98.2 | unchanged ✅ |

The only moving value is `unrealisedPnl` 0.576 → 0.603, which is the market, not the restart.

🔴 **The boot log names the mechanism explicitly:**
```
16:55:31 [SMART-CLEANUP] Skipping stop cancel — position still open on exchange for SOL/USDT:USDT
16:55:31 [AP] Restored LONG SOL/USDT:USDT from DB (entry=2026-09-17T09:05:22.111839+00:00)
```
The boot path **checked for an open position and declined to cancel the stop.** That is why `updatedTime` is
unchanged — by design, not by luck. Sixth safe restart under an open position, 39 of 39.

### 2f) The armed exit survived — and it structurally cannot be cleared by a boot
`exit_pending` is a **DB table** (`CREATE TABLE IF NOT EXISTS`, never dropped). The only DELETE paths are
`clear_exit_pending(side)` on an actual exit execution (`main.py:4054/5611/5740/6048`) and lazy expiry on read
**only when `now >= expires_at`** (`state_machine.py:361-366`). **No boot path clears it.** Confirmed present
after restart, byte-identical: `LONG / 2026-09-17T14:00:14.945498+00:00 / 2026-09-17T20:00:14.945498+00:00 /
'Exit Signal'`.

### 2g) Boot line
```
Sep 17 16:55:13 systemd[1]: Started mercury-sol.service - Mercury-SOL SOL/USDT swing bot (Bybit, paper/observation).
Sep 17 16:55:32 [MERCURY-SOL] [BOOT] taker fee: 0.001 (0.1000%) source=venue
Sep 17 16:55:36 [MERCURY-SOL][VIRTUAL] [HEARTBEAT] alive ticks=1 cadence=10s open=1 mode=LIVE pid=3077058
```
`openitems_guard` after: **EXIT=0**.

---

## 3. PROVEN LOADED, NOT JUST ON DISK

### 3a) From the bytecode the running PID imported — **0 mismatches**
Sources written 16:45:46–16:46:27, `.pyc` regenerated 16:46:56, **process started 16:55:13** — the running
process loaded the patched bytecode. Read back out of `__pycache__/*.cpython-312.pyc`:

```
✅ BULL_DAILY_SHORT_BLOCK_ENABLED = True
✅ BULL_DAILY_SHORT_BLOCK_DRYRUN  = False
✅ TRACKED_STATUSES = ('ai_skipped','below_threshold','htf_blocked','risk_halt',
                       'book_blocked','flat_adx_blocked','bull_daily_blocked','entry_gate_refused')
```

### 3b) 🔴 UNTOUCHED AT RUNTIME — every protected value, from the same loaded bytecode

| | | | |
|---|---|---|---|
| ✅ `SL_BUFFER_ATR` 2.5 | ✅ `TRAIL_MULT_ATR` 1.875 | ✅ `TRAIL_ARM_R` 0.75 | ✅ `CONFLUENCE_SCORE_THRESHOLD` 2.0 |
| ✅ `FLAT_ADX_GATE_DRYRUN` **True** | ✅ `BOOK_GATE_DRYRUN` **False** | ✅ `BOOK_GATE_ENABLED` True | ✅ `BOOK_GATE_MIN_SUPPORTING` 1 |
| ✅ `BOOK_GATE_WALL_PCTL` 90.0 | ✅ `BOOK_GATE_WALL_DIST_PCT` 0.2 | ✅ `BOOK_GATE_LEAN_FLOOR` {LONG 0.4214, SHORT 0.3975} | ✅ `EXIT_ADVISOR_DRYRUN` True |
| ✅ `MAX_POSITIONS_PER_SIDE` 1 | ✅ `LIVE_FIXED_MARGIN` 20 | ✅ `LEVERAGE` 5 | |

**AST diff of `config.py`: 139 → 141 constants. ADDED 2, CHANGED 0, REMOVED 0.**
**`main.py`: functions 95 → 96, added `_bull_daily_short_halt`, removed none.**
**`skip_attribution.py`: functions 25 → 25, unchanged.**

**Advisor prompts:** `claude_advisor.py` was never opened for writing — mtime **2026-09-14T22:19:49**, sha256
`52feade7…6c36`, unchanged. That covers every prompt in the file definitively. *(My AST enumeration surfaced 4
module-level prompt constants, not 6 — `_ENTRY_SYSTEM`, `_CLOSE_SYSTEM`, `_CLOSE_STATE_SYSTEM`,
`_LEARNING_SYSTEM`; the other two are evidently built dynamically. I am not claiming six hashes I did not
compute — the untouched file hash is the stronger proof and it covers all of them.)*

### 3c) Backups
`config.py.bak_bulldaily_20260917`, `main.py.bak_bulldaily_20260917`,
`skip_attribution.py.bak_bulldaily_20260917`, `OPEN-ITEMS-SOL.md.bak_bulldaily_20260917`.

Pre-patch sha256: config `a308a130…`, main `91dfa43f…`, skip_attribution `f485c0cb…`.
Post-patch: config `0585a82c…`, main `f355fdea…`, skip_attribution `c5a669f5…`.

---

## 4. RECORDED IN CANON

Both entries written to `OPEN-ITEMS-SOL.md`:

* **`§BULL-DAILY-SHORT-GATE-2026-09-17`** — the discipline reasoning **verbatim**, the **MARGINAL** rate
  (~20% of executable shorts, ≈2 per 41 days), the alarm (**>50% of EXECUTABLE shorts** — with the 63.5%
  condition rate explicitly marked EXPECTED and NOT the alarm), and the review point at **10
  `bull_daily_blocked` rows**.
* **`§ENTRY-GATE-REFUSED-UNREGISTERED-2026-09-17`** — the 608-row count, the mirror-image half-fix, and the
  recoverability verdict.
* 🔴 **COHORT BOUNDARY 2026-09-17 16:55:13 UTC** recorded for **both** changes. Do not pool across it.

---

## WHAT TO WATCH FIRST

The gate has **not yet fired** — expected, at ~2 refusals per 41 days. The first `bull_daily_blocked` row is
the thing to look for; it will arrive as a Telegram card naming the daily label and the price. `entry_gate_refused`
rows should start appearing in `skip_attribution` immediately, since that path fires far more often — **that is
the first falsifiable prediction of this pass**, and if no such row appears within a few days the registration
did not take.

| final state | |
|---|---|
| `mercury-sol.service` | running, PID 3077029, `NRestarts=0`, open=1 LIVE |
| `titan.service` | **UNTOUCHED**, PID 1572470, `NRestarts=0` |
| #48 | open, LONG @ 100.37, stop 98.2 intact, armed exit intact until 20:00:14 |
