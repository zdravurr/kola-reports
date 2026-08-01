# sol-phase2-design-one-manager-two-adapters

_2026-08-01 19:05 UTC_

---

# MERCURY-SOL — PHASE 2 DESIGN. **NO CODE WRITTEN. STOPPED FOR THE STOP-OWNERSHIP DECISION.**

Design pass only, as instructed. **Nothing was changed** — `main.py`, `virtual_trader.py`,
`tor_retry.py`, `stop_loss.py` and `config.py` are untouched since the 18:33:54 Phase 1 restart.
SOL is PAPER, the entry prompt and its inputs are frozen and untouched, the 200-window is intact,
vpos 25 was not disturbed. Titan untouched.

---

# THE ANSWER FIRST

**The design is tractable: 3 primitive adapter operations cover all 9 decision points, and 6 of
the 7 live implementations already exist.** Exactly one new primitive is needed — a partial
reduce-only close — because `_execute_close_position` only ever closes the *whole* position.

**And there is a third door, of exactly the shape you predicted.** It is not a stale row — it is
**active adoption logic that fires on a correctly-managed position at every restart**:

> `_load_active_positions_from_db()` runs at **module import, in the gunicorn MASTER**
> (`main.py:3943`, `preload_app=True`), and its tail block **adopts any exchange position that is
> not in `active_positions` into the live monitor's registry**, persists it, and stamps it
> `be_locked=False`, `entry_time=NOW`.

In Phase 2 a live position owned by the engine lives in `virtual_positions` and **not** in
`active_positions` — so it matches that condition exactly. Every restart would hand it to a second
manager, with its breakeven state reset and a timeout clock started. `start_monitor()` is **not
mode-gated**, so that second manager is always running.

**I recommend stop ownership Option C — the exchange holds the stop, the engine holds the
decisions.** Argument in §3. That is the question I need answered before writing code.

---

# §1 — EVERY DECISION POINT IN `_process_position`

Nine points. Four are observational and need nothing; five act.

| # | section | decision point | today (paper) | live equivalent needed |
|---|---|---|---|---|
| 1 | 1 | `water_mark` update | SQLite write | **none** — pure bookkeeping, works unchanged |
| 2 | 1b | MAE (`max_adverse_price`) | SQLite write | **none** |
| 3 | 1d | excursion sample (10 s grid) | SQLite insert | **none** — needs only to be *reachable* in live |
| 4 | 1e | smart-exit DRYRUN snapshot | SQLite insert, OKX-direct reads | **none** — same |
| 5 | 1c | **post-entry recheck → emergency close** | `_poller_close(..., 'post_entry_critical')` at `last` | **CLOSE** — real reduce-only market order |
| 6 | 1c | **post-entry recheck → SL tighten** | `UPDATE virtual_positions SET sl_price` | **MOVE STOP** — real `trading_stop` call |
| 7 | 2 | **breakeven lock** | `UPDATE ... sl_price = be_price` | **MOVE STOP** — real `trading_stop` call |
| 8 | 2 | **partial-at-arm ⅓** | arithmetic + SQLite (`partial_*` cols) | 🔴 **PARTIAL REDUCE** — reduce-only order for `qty` only |
| 9 | 2 | adaptive-trail one-shot recompute at +1R | `UPDATE ... trail_pct` (DRYRUN-inert today) | **SET TRAIL** — `trading_stop` trailing params |
| 10 | 3 | **stop-loss breach** | `_poller_close(..., 'sl')` at `last` | **CLOSE** (or reconcile — see §3) |
| 11 | 4 | **trailing-stop breach** | `_poller_close(..., 'trail')` at `last` | **CLOSE** (or reconcile — see §3) |
| 12 | 5 | **timeout** | `_poller_close(..., 'timeout')` — inert, `MAX_POSITION_DURATION_MINS=0` | **CLOSE** |

Plus three **external** close entry points that already funnel through the same place:

| where | today | live |
|---|---|---|
| exit signal / armed exit | `_virtual_close_for_side` → `close_position` | `_execute_close_position` — **already adapter-branched** |
| trend reversal (`main.py:3386`) | direct `virtual_trader.close_position`, DRYRUN-inert | 🔴 **the one place that bypasses the adapter** — must be routed through it in Phase 2 |
| SL fail-safe emergency close | `_execute_close_position` | already correct |

## The three primitives

Collapsing the table: **every acting decision point is one of three operations.**

| primitive | serves points | 
|---|---|
| **`close(pos, reason, price)`** | 5, 10, 11, 12 + all three external closes |
| **`move_stop(pos, new_sl)`** | 6, 7 |
| **`partial_reduce(pos, qty, price)`** | 8 |
| *(`set_trail(pos, pct)`)* | 9 — only if the adaptive recompute is ever taken out of DRYRUN |

`_process_position` keeps **every decision**. It stops calling `close_position` /
`UPDATE sl_price` directly and calls the adapter instead. The adapter dispatches on **who owns the
position**, not on "are we simulating" — which is the Titan framing you cited, and the reason all
six mechanisms come along for free: *the decision code is never touched.*

---

# §2 — WHAT ALREADY EXISTS. REUSE, DO NOT REIMPLEMENT.

| primitive | live implementation | status |
|---|---|---|
| **close** | `_execute_close_position` (`main.py:1855`) | ✅ **exists and is already Phase-1 hardened**: POS_UNKNOWN raises before any mutation, `reduceOnly` correct, idempotent write key, cancels companion stops after. Reuse as-is. |
| **move_stop** | the `private_post_v5_position_trading_stop` call inline in `_monitor_positions` (`main.py:3746-3752`) | ⚠️ **exists but is inline.** Needs *extracting* into a named function — reuse by extraction, not a rewrite. It already does `price_to_precision`, `slTriggerBy: MarkPrice`, and the `positionIdx`. |
| **set_trail** | `_place_trail_with_retry` (`main.py:1633`) | ✅ exists, 3 attempts. Note its return value is still unchecked at the entry site — a pre-existing defect, recorded, not in this phase. |
| **initial stop at entry** | `_place_sl_with_retry` (`main.py:1590`) | ✅ exists, 3 attempts + emergency-close fail-safe, Phase-1 idempotent key, `reduceOnly` fixed |
| **cancel stops** | `_cancel_stop_orders` (`main.py:1541`) | ✅ exists, V5 `cancel-all` with `orderFilter=StopOrder` |
| **position state** | `_fetch_position_state` (Phase 1) | ✅ exists, tri-state |
| **size quantisation** | `quantise_amount` (Phase 1, `stop_loss.py`) | ✅ exists, rounds down, refuses below min, no network call when a price is supplied |
| 🔴 **partial_reduce** | — | ❌ **DOES NOT EXIST.** `_execute_close_position` computes `close_amount = float(pos['contracts'])` — the whole position. This is the **one genuinely new primitive** in Phase 2. |

## The one new primitive, and its constraints

`_execute_partial_close(symbol, position_side, qty, price)`:

- must route through **`with_socks_retry_write`** with its own idempotency key (`sol-p-{vpos_id}`)
  — a duplicated partial would realise ⅔ instead of ⅓;
- must pass **`reduceOnly: True`** (camelCase — the Phase 1 2b lesson) and the hedge `positionIdx`;
- must **quantise `qty` to the venue step** via `quantise_amount`, passing the price the caller
  already holds so no network call is added;
- 🔴 must return the **actually filled** quantity, because the accounting invariant requires the
  fee split to follow the **realised** size. Phase 1 established `_frac = qty/size` against the
  *rounded* size; in live it must be against the *filled* size, which a partial fill can make
  smaller still.

That last point is the only place where live is genuinely harder than paper, and it is the reason
this primitive cannot be a thin wrapper.

---

# §3 — 🔴 WHO OWNS THE STOP IN LIVE? THE DECISION I NEED FROM YOU

## The three options

**Option A — the engine decides and issues a market close on breach** (paper semantics, real
orders). One code path, perfect paper/live symmetry, all six mechanisms free.

🔴 **I recommend against it, and strongly.** It is *strictly worse than what live has today*:

- **If the process is down, nothing enforces the stop.** Today's live places a real Bybit
  conditional order at entry; it survives a crash, an OOM kill, a deploy, a `systemctl restart`.
  Option A would replace that with a Python comparison in a 10 s loop. We restarted this service
  **four times today alone**.
- **Latency and slippage.** Breach detection waits up to 10 s for the next tick, then a Tor
  round-trip to send the close. Bybit's own stop triggers on MarkPrice with neither delay.
- **Tor is the single point of failure.** 285 SOCKS retries and 26 CloudFront 403s in two days,
  and direct Bybit is CloudFront-blocked from this host — so a Tor outage would mean *no stop at
  all* rather than a degraded one.

**Option B — the stop rests on the exchange and the engine never touches it.** Maximum safety,
but it forfeits the six mechanisms: the breakeven move, the recheck tighten and the partial all
*are* engine decisions. This is what live does today, and it is exactly why the six mechanisms
don't exist there.

## ✅ **Option C — RECOMMENDED. The exchange holds the STOP; the engine holds the DECISIONS.**

The split is on *enforcement* versus *decision*, and it maps cleanly onto the adapter:

| | owner |
|---|---|
| **Enforcing** the stop (what happens if the process dies) | **the exchange** — a real conditional order, as today |
| **Deciding** where the stop should be (BE, recheck tighten, trail level) | **the engine** — same code as paper, expressed as `move_stop` |
| **Deciding** to exit early (recheck emergency, signal, timeout) | **the engine** — expressed as `close` |
| **Deciding** to take the partial | **the engine** — expressed as `partial_reduce` |

### How the close is detected in live, and why this is not a paper/live divergence

In live the **authoritative close event is "the position is no longer on the exchange"** — which
`_fetch_position_state` already reports as `POS_FLAT`, and which `_monitor_positions` already
handles today by recovering the real fill from `fetch_my_trades`. That logic moves into the
engine's tick:

1. read position state (Phase 1 tri-state);
2. **`POS_UNKNOWN` → do nothing** (Phase 1 semantics, unchanged);
3. **`POS_FLAT` → the exchange stop or trail fired.** Book the close from the real fill, through
   the *same* close accounting the paper path uses;
4. **`POS_OPEN` → run every decision** exactly as paper does.

The engine's own `last <= sl_price` comparison **stays in the code, unchanged, for both modes**.
In paper it *is* the executor. In live it becomes a **backstop**: if price is through the stop and
the exchange still reports the position open, the exchange stop is missing or failed, and the
engine closes. That is not divergence — it is the same comparison, with the exchange as a faster
first responder in live.

### What a worker restart with an open position means

| | Option A | **Option C (recommended)** |
|---|---|---|
| While the process is down | 🔴 **no stop exists anywhere** | ✅ **the stop rests on Bybit and enforces itself** |
| At boot | engine re-reads `virtual_positions` and resumes | engine re-reads `virtual_positions`, reconciles against the exchange, and resumes; the stop was never absent |
| If the position closed while down | detected at next tick | detected as `POS_FLAT` and booked from the real fill |
| If the boot read fails | position unmanaged, no stop | position unmanaged **but still stopped** |

That last row is the whole argument. **Under Option C the worst case is "unmanaged but protected".
Under Option A it is "unmanaged and naked".**

### The cost of Option C, stated honestly

- The engine must keep the resting stop **in sync** with `sl_price` after every BE move and
  recheck tighten. A `move_stop` that fails leaves the DB and the exchange disagreeing — the
  exchange stop is then *stale but present*, i.e. wider than intended. That is the safe direction,
  and it must be logged loudly rather than retried silently.
- The partial reduces position size, so the **resting stop's quantity must be reduced too**, or a
  stop sized for the full position sits against a ⅔ position. On Bybit a position-level
  `trading_stop` follows the position size automatically; a separate conditional order does not.
  **This needs deciding when I write the code, and I will confirm which mechanism the SL uses
  before relying on either.**

---

# §4 — 🔴 DOUBLE MANAGEMENT: THE DOORS, INCLUDING THE ONE NOBODY ANTICIPATED

You asked me to check every path that can reach a position, not just the obvious two. First, the
good news that bounds the problem: **all position mutation is confined to `main.py` and
`virtual_trader.py`.** No sampler, optimizer, observatory or the separate `optimizer_listener`
process (pid 939, up 19 days) touches a position — verified by sweep.

## Door 1 — the live monitor thread (obvious)

`_monitor_positions` iterates `_active_positions`. 🔴 **`start_monitor()` is NOT mode-gated** — it
runs unconditionally from `post_fork` in *both* modes. In paper it is harmless only because the
registry is empty. **In Phase 2 it must be retired**, not merely skipped: its two unique
behaviours (external-close detection with PnL recovery; the timeout killer) are exactly what
§3's `POS_FLAT` branch and decision point 12 absorb into the engine. Retiring it *is* "one
manager".

## Door 2 — the paper poller (obvious)

`start_virtual_poller` returns early when `not OBSERVATION_MODE`. **In Phase 2 this gate must
invert**: the engine becomes the manager in both modes, so the poller must start in live too.

## 🔴 Door 3 — BOOT RECONCILIATION ADOPTS THE OTHER MANAGER'S POSITION

**This is the one, and it is not a stale-state bug — it is active logic that fires on a perfectly
healthy, correctly-managed position.**

`main.py:3943` calls `_load_active_positions_from_db()` **at module import**, in the gunicorn
**MASTER** (`preload_app = True`), before any fork. Its tail block (`main.py:356-377`):

```python
    # Exchange shows open position not in DB — import with entry_time=NOW so timeout fires soon
    if live_positions is not None:
        for p in live_positions:
            if float(p.get('contracts') or 0) > 0 and (DEFAULT_SYMBOL, p_side) not in _active_positions:
                ... _persist_active_position(...) ...
                _active_positions[(DEFAULT_SYMBOL, p_side)] = {
                    'entry_time': now, 'be_locked': False,
                    'sl_price': float((p.get('info') or {}).get('stopLoss') or 0) or None, ...}
```

In Phase 2, an engine-owned live position lives in `virtual_positions` and **not** in
`active_positions` — which is precisely the adoption condition. So at **every restart**:

1. the master adopts it into `_active_positions` and **writes it to the `active_positions` table**;
2. the forked worker **inherits the populated registry** through `preload_app`;
3. `_monitor_positions` — unconditionally started — begins managing it **alongside the engine**;
4. it is stamped **`be_locked: False`**, so the live monitor will re-apply a breakeven the engine
   may already have moved past, **overwriting the engine's stop**;
5. it is stamped **`entry_time = NOW`**, and the log line says *"timeout will fire soon"*. Latent
   today because `MAX_POSITION_DURATION_MINS = 0`, but a live force-close by the second manager if
   that is ever enabled.

**Two managers, disagreeing about breakeven state, one of them able to force-close.** Retiring
Door 1 closes this too — but the adoption block must *also* be made engine-aware, because it
writes DB state, sends a Telegram warning, and would otherwise resurrect the registry the moment
anyone re-enables the monitor.

## Door 4 — the engine's own boot reconciliation is gated OFF in live

`_reconcile_open_virtual_positions` opens with `if not OBSERVATION_MODE: return`. So in Phase 2
live, the engine's open positions **would not be surfaced at boot at all** — no log line, no
Telegram. Not a double-manager, but the exact blind spot that once hid vpos 5's never-closing.
**Must become mode-independent.**

## Door 5 — `_smart_boot_cleanup` at import

Also runs at module import (`main.py:3939`), before the adoption block. It cancels **all**
StopOrders when the exchange reports flat, and already does the right thing on a failed read
("DOING NOTHING to be safe"). Correct today. **It must be re-verified once the engine owns the
stops**, because under Option C an engine-owned resting stop is exactly the kind of order it is
designed to clear.

## Door 6 — the trend-reversal close bypasses the adapter

`main.py:3386` calls `virtual_trader.close_position` **directly**, having queried
`virtual_positions` itself, with no mode branch. Inert today (`TREND_REVERSAL_EXIT_DRYRUN = True`)
and already flagged in the 17:46 study. **In Phase 2 it must route through the adapter** or it
will close the paper row while the real position stays open.

---

# §5 — WHAT PHASE 2 PRESERVES, BY CONSTRUCTION

Mapping your section 2 onto the design:

| requirement | how it is met |
|---|---|
| **All six mechanisms work in live as the SAME CODE** | `_process_position` is not modified in its decision logic at all. Only its three *actions* are redirected through the adapter. The recheck, the partial, the excursion sampler, the dryrun sampler and water_mark/MAE become live-reachable purely by the poller starting in live. |
| **POS_UNKNOWN never destructive** | The adapter's `close` is `_execute_close_position`, which already raises before any mutation on UNKNOWN. The engine's tick adds UNKNOWN → do nothing. |
| **Idempotency keys on writes** | Every adapter write routes through `with_socks_retry_write`; the new partial primitive gets `sol-p-{vpos_id}`. |
| **Quantised sizes, accounting follows the ROUNDED size** | `quantise_amount` at the partial, with `price` supplied so no network call. In live the fee split must follow the **filled** size — the stricter version of the Phase 1 rule. |
| **`initial_risk_usdt` untouched** | Not written by any adapter path. R stays comparable across the whole book. |
| **`net_pnl` keeps meaning total realised PnL incl. the partial** | The fold-back in `close_position` (`partial_pnl` / `partial_fees`) is untouched. The adapter changes *how the fill happens*, never *how the position is booked*. |

**Not moving:** the entry prompt and everything feeding it, the cascade, the score gate, the risk
gates, thresholds, `TRAIL_MULT_ATR`, `SL_BUFFER_ATR`, the arm point, `PARTIAL_AT_ARM_FRACTION`,
`OBSERVATION_MODE` (SOL is paper at the end of this phase), the optimizer, the samplers and the
observatory beyond making them reachable.

---

# §6 — SHAPE AND SIZE, IF OPTION C IS APPROVED

| work | detail |
|---|---|
| **New code** | one primitive — `_execute_partial_close` |
| **Extracted** | the breakeven `trading_stop` call → a named `_move_stop_to` reusable by BE *and* recheck tighten |
| **Redirected** | ~6 call sites inside `_process_position`, from direct DB/`close_position` to the adapter |
| **Retired** | `_monitor_positions` (its two unique behaviours absorbed) |
| **Gates inverted** | `start_virtual_poller`, `_reconcile_open_virtual_positions` |
| **Made engine-aware** | the boot adoption block, `_smart_boot_cleanup`, the trend-reversal close |
| **Files** | `main.py`, `virtual_trader.py` — **no new files** |
| **Effort** | ~3–5 days, matching the 17:46 study's estimate for this phase |

**Highest-risk item is not the code — it is Door 3.** It is the one that produces a wrong outcome
while every individual component behaves exactly as written.

---

# 🛑 THE DECISION I NEED

**Approve stop ownership Option C** — the exchange holds the stop, the engine holds the decisions,
the engine's own comparison stays as a backstop — **or tell me you want A or B instead.**

It determines everything downstream: whether `move_stop` exists at all, whether the engine's
`sl_hit` branch executes or reconciles, whether `_place_sl_with_retry` still runs at entry, and
what "restart with an open position" means for real money.

Nothing is written until you answer. SOL is paper, the window stands at **3 of 200**, vpos 25 is
open and untouched, and Titan is clean.
