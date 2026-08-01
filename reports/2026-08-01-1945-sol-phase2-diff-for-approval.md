# sol-phase2-diff-for-approval

_2026-08-01 19:45 UTC_

---

# MERCURY-SOL — PHASE 2 DIFF. **NOTHING APPLIED. STOPPED FOR REVIEW.**

**No code was changed.** `main.py` (18:29:22), `virtual_trader.py` (18:30:18), `tor_retry.py`,
`stop_loss.py`, `config.py`, `claude_advisor.py` are all untouched since Phase 1. SOL is PAPER,
the entry prompt and its inputs are frozen, the window stands at **4 of 200**, vpos 25 is open and
undisturbed. Titan untouched.

Two things were *run* rather than written: the venue queries in §1 (read-only) and the accounting
proof in §5 (throwaway DB, full module isolation, live DB verified untouched).

---

# §1 — 🔴 THE TWO OPEN QUESTIONS, ANSWERED FROM THE VENUE

## (a) Does the resting stop follow position size? — **NO, and the code uses BOTH mechanisms**

Asked the API directly (`GET /v5/position/list`, read-only, through Tor):

```json
{"symbol":"SOLUSDT","positionIdx":"1","tpslMode":"Full","stopLoss":"","trailingStop":"0"}
{"symbol":"SOLUSDT","positionIdx":"2","tpslMode":"Full","stopLoss":"","trailingStop":"0"}
open orders: 0
```

Hedge mode confirmed (two position slots), and **`tpslMode: "Full"`** — the position-level
`stopLoss` applies to the whole position and **follows its size automatically**.

Now what the code actually uses — and the answer is *both*, inconsistently:

| where | mechanism | follows size? |
|---|---|---|
| **entry SL** (`_place_sl_with_retry`) | `POST /v5/order/create` with `triggerPrice` + fixed `qty` → **a separate conditional StopOrder** | 🔴 **NO** |
| **breakeven move** (`_monitor_positions`) | `POST /v5/position/trading-stop` with `stopLoss` → **position-level** | ✅ **YES** |
| **trailing stop** (`_place_trail_with_retry`) | `POST /v5/position/trading-stop` with `trailingStop` | ✅ position-level |

**So the answer to your question is: the entry stop does NOT follow size.** Under your own
condition — *"a partial that reduces size while leaving a full-size stop resting is a defect worse
than no partial"* — the partial would have to cancel-and-replace it.

**🔴 And this uncovered a pre-existing defect.** Nothing cancels the entry conditional order when
breakeven fires. The BE path sets a *position-level* `stopLoss` and leaves the original
*conditional order* resting at the ATR level. **After breakeven a live position would carry TWO
stops** — one at BE (position-level) and an orphan at the original ATR distance. Never observed
because SOL has never placed a live order.

### Recommendation: move the entry SL to the position-level mechanism

Rather than teach the partial to cancel-and-replace a conditional order, **use the mechanism that
already follows size** — the same one BE and the trail already use:

- the partial needs **no stop resize at all**; Bybit shrinks it with the position;
- the **dual-stop defect disappears** — entry, BE and tighten all become one `trading_stop` call;
- the **level is unchanged** — `compute_initial_sl` / `SL_BUFFER_ATR` are untouched. This is a
  *mechanism* change, not a level change, and nothing in your "must not move" list is affected;
- the fail-safe is preserved exactly: 3 attempts, and emergency-close if it cannot be set.

This is embedded in the diff below (**B1**) and is the one substantive design choice inside it —
flagged because you asked to read the diff before it runs.

## (b) A failed `move_stop` — loud, no silent retry, and what you do about it

Agreed the direction is safe: a failed move leaves the exchange stop **stale-but-present, i.e.
wider than intended**. Never tighter, never absent.

**What the operator does when they see it** — and the honest answer is *usually nothing*, because
of Option C's structure:

> While the bot is running, the **engine's own comparison still enforces the intended level** —
> that is exactly the backstop you approved. The exchange stop is the wider safety net. So a failed
> `move_stop` degrades protection from "two stops at the intended level" to "engine at the intended
> level, exchange at the wider one".
>
> **The one case that needs you: if the bot is about to go down or be restarted.** Then the engine
> stops enforcing and the effective stop reverts to the wider exchange level. Either set the stop
> manually on Bybit first, or accept the wider risk for the duration.

The alert says precisely that, including both levels, so no interpretation is required:

```
⚠️ STOP MOVE FAILED — SOL/USDT:USDT SHORT
   intended SL 72.32506  ·  exchange still at 73.20 (WIDER, not absent)
   Engine enforces 72.32506 while running. If the bot restarts, protection
   reverts to 73.20 — set it manually on Bybit or accept the wider risk.
```

**No silent retry.** One attempt per tick; the next tick re-detects the mismatch and tries again,
which is visible in the log rather than hidden inside a loop.

---

# §2 — PART A: THE DOORS (applied first, per your ordering)

## A1 — retire `_monitor_positions`, absorbing its two unique behaviours

```diff
 def start_monitor():
-    """Start the position-monitor thread exactly once in the CURRENT process."""
-    global _monitor_thread, _monitor_started
-    if _monitor_started or (_monitor_thread is not None and _monitor_thread.is_alive()):
-        return
-    _monitor_thread  = threading.Thread(target=_monitor_positions, daemon=True)
-    _monitor_thread.start()
-    _monitor_started = True
-    print(f"{LOG_PREFIX}[MONITOR] thread started in pid {os.getpid()}", flush=True)
+    """RETIRED 2026-08-01 Phase 2 — ONE MANAGER, TWO ADAPTERS.
+
+    The live monitor was the SECOND manager. Its two unique behaviours are now in
+    the engine's own tick, so nothing is lost by retiring it:
+      • external-close detection + real-fill PnL recovery → the POS_FLAT branch of
+        _process_position (it already read the same fetch_my_trades data);
+      • the timeout killer → decision point 5 of _process_position, which already
+        implements it against the SAME MAX_POSITION_DURATION_MINS constant.
+
+    Deliberately kept as a NO-OP rather than deleted: post_fork calls it, and a
+    hard removal would make a future re-add silently resurrect a second manager.
+    """
+    print(f"{LOG_PREFIX}[MONITOR] RETIRED — the paper engine is the single "
+          f"position manager in BOTH modes (Phase 2)", flush=True)
```

`_monitor_positions` itself is left in the file, unreferenced, with a header comment marking it
dead — removing ~150 lines in the same change that rewires ownership would make the diff
unreviewable. It has no caller and cannot start.

## A2 — 🔴 the boot adoption block becomes engine-aware (Door 3)

The one that produces a wrong outcome while every component behaves as written.

```diff
     # Exchange shows open position not in DB — import with entry_time=NOW so timeout fires soon
     if live_positions is not None:
         for p in live_positions:
             p_side = (p.get('side') or '').upper()
             if float(p.get('contracts') or 0) > 0 and (DEFAULT_SYMBOL, p_side) not in _active_positions:
+                # 🔴 PHASE 2 DOOR 3. This block ADOPTS an exchange position that is
+                # absent from active_positions — which is EXACTLY the state of every
+                # engine-owned position, because the engine keeps its book in
+                # virtual_positions. Unguarded, it would hand a correctly-managed
+                # position to a second manager at EVERY restart, stamped
+                # be_locked=False (so BE would be re-applied over the engine's stop)
+                # and entry_time=NOW (starting a timeout clock). It also PERSISTS to
+                # the active_positions table and Telegrams — so it would resurrect
+                # the registry the moment anyone re-enabled the monitor, which is why
+                # retiring the monitor alone is not enough.
+                if _engine_owns_position(DEFAULT_SYMBOL, p_side):
+                    print(f"{LOG_PREFIX}[AP] {p_side} {DEFAULT_SYMBOL} open on exchange "
+                          f"and OWNED BY THE ENGINE (virtual_positions) — not adopting, "
+                          f"not persisting. The engine manages it.", flush=True)
+                    continue
                 print(f"{LOG_PREFIX}[AP] RECONCILE WARNING: ...
```

with the ownership test, deliberately independent of `OBSERVATION_MODE` so it is correct in both
modes:

```diff
+def _engine_owns_position(symbol, position_side):
+    """True when the engine's book has an OPEN row for this (symbol, side).
+    Ownership is a fact about the BOOK, not about the mode — which is the whole
+    Phase 2 framing: route on WHO OWNS THE POSITION, not on 'are we simulating'."""
+    try:
+        with sqlite3.connect(DB_PATH) as conn:
+            row = conn.execute(
+                "SELECT 1 FROM virtual_positions WHERE symbol=? AND position_side=? "
+                "AND status='open' LIMIT 1", (symbol, position_side)).fetchone()
+        return row is not None
+    except Exception as e:
+        # Fail SAFE: if we cannot tell, assume the engine owns it and do NOT adopt.
+        # Adopting on doubt creates the second manager; declining costs nothing.
+        print(f"{LOG_PREFIX}[AP] ownership check failed ({e}) — assuming ENGINE "
+              f"owns {symbol} {position_side}, not adopting", flush=True)
+        return True
```

## A3 — invert the two gates

```diff
 def start_virtual_poller():
-    if not OBSERVATION_MODE:
-        print(f"{LOG_PREFIX}[VIRTUAL] poller not started (live mode)", flush=True)
-        return
+    # PHASE 2: the engine is the single manager in BOTH modes. The mode no longer
+    # decides WHETHER it runs — only what its adapter does at each decision point.
+    print(f"{LOG_PREFIX}[VIRTUAL] engine poller starting "
+          f"({'PAPER' if OBSERVATION_MODE else 'LIVE'} adapter)", flush=True)
     virtual_trader.set_followthrough_hook(_followthrough_tick)
+    virtual_trader.set_live_adapter(_exec_close_live, _exec_partial_live,
+                                    _exec_move_stop_live, _fetch_position_state)
     virtual_trader.start_worker(exchange, send_tg=send_tg)
     _reconcile_open_virtual_positions()
```

```diff
 def _reconcile_open_virtual_positions():
-    if not OBSERVATION_MODE:
-        return
+    # PHASE 2: was gated OFF in live, so an engine-owned live position would not be
+    # surfaced at boot AT ALL — the same blind spot that once hid vpos 5.
```

## A4 — trend-reversal close routed through the adapter (Door 6)

```diff
                     if not TREND_REVERSAL_EXIT_DRYRUN:
-                        _last = float(tor_retry.with_socks_retry(exchange, lambda ex: ex.fetch_ticker(symbol), label='ticker.revexit')['last'])
-                        virtual_trader.close_position(_vid, _last, 'trend_reversal')
+                        # PHASE 2 DOOR 6: was a DIRECT paper-book close with no mode
+                        # branch — in live it would have closed the paper row while the
+                        # real position stayed open. Route through the adapter.
+                        _execute_close_position(symbol, _opp_side, reason='trend_reversal')
                         state_machine.clear_exit_pending(_opp_side)
```

which requires `_execute_close_position` to carry the reason through (it currently hard-codes
`'exit_signal'` on the paper branch):

```diff
-def _execute_close_position(symbol, position_side):
+def _execute_close_position(symbol, position_side, reason='exit_signal'):
     if OBSERVATION_MODE:
-        return _virtual_close_for_side(symbol, position_side, reason='exit_signal')
+        return _virtual_close_for_side(symbol, position_side, reason=reason)
```

## A5 — `_smart_boot_cleanup` re-verified under engine-owned stops (Door 5)

**Re-verified against the venue answer, and it is safe — for a reason worth recording.**
`_cancel_stop_orders` uses `cancel-all` with **`orderFilter=StopOrder`**, which cancels
*conditional orders*. A **position-level `trading_stop` stopLoss is a position attribute, not an
order** — so with B1 (entry SL moved to the position-level mechanism) `cancel-all/StopOrder`
**cannot clear an engine-owned stop.** It also only runs when the exchange reports flat, and
already does nothing on a failed read.

One comment added so the reasoning is not re-derived:

```diff
 def _smart_boot_cleanup(symbol):
     """Cancel ONLY orphaned stops. Skip if a position is still open on exchange.
+
+    PHASE 2 re-verification: safe against engine-owned stops. cancel-all uses
+    orderFilter=StopOrder, which targets CONDITIONAL ORDERS; the engine's stop is a
+    position-level trading_stop attribute (tpslMode=Full, confirmed from the venue)
+    and is NOT an order, so this cannot clear it. It also only fires when the
+    exchange reports FLAT — in which case there is no position stop to clear.
     """
```

---

# §3 — PART B: THE STOP MECHANISM

## B1 — entry SL becomes position-level, so it follows size

```diff
-def _place_sl_with_retry(symbol, close_side, sl_price, amount, pos_idx,
-                         position_side, max_attempts=3, idem_key=None):
-    """Place a conditional SL order with exponential backoff. Returns order ID or None."""
+def _place_sl_with_retry(symbol, close_side, sl_price, amount, pos_idx,
+                         position_side, max_attempts=3, idem_key=None):
+    """Set the POSITION-LEVEL stop-loss with exponential backoff. True on success.
+
+    PHASE 2 MECHANISM CHANGE (level unchanged — compute_initial_sl and SL_BUFFER_ATR
+    are untouched). Was POST /v5/order/create with a triggerPrice and a FIXED qty:
+    a separate conditional order that does NOT follow position size. Confirmed from
+    the venue that tpslMode='Full', so a position-level stopLoss DOES follow size.
+    Three things this buys:
+      1. the partial-at-arm leg needs NO stop resize — Bybit shrinks the stop with
+         the position. A full-size stop resting against a reduced position would be
+         a defect worse than no partial;
+      2. it removes a REAL pre-existing defect: nothing cancelled the entry
+         conditional order when breakeven fired, so a live position would have
+         carried TWO stops — one at BE and an orphan at the original ATR level;
+      3. entry, breakeven and the recheck tighten all become ONE mechanism, so
+         _move_stop_to is the only thing that ever touches the stop.
+    `amount` is retained in the signature (unused) so the call site is unchanged.
+    """
     for attempt in range(1, max_attempts + 1):
-        try:
-            sl_order = tor_retry.with_socks_retry_write(... create_order ...)
-            return sl_order.get('id')
+        if _move_stop_to(symbol, position_side, sl_price, label='entry-sl'):
+            print(f"{LOG_PREFIX}[SL] set on attempt {attempt}: {sl_price}", flush=True)
+            return True
+        if attempt < max_attempts:
+            time.sleep(0.5 * (2 ** (attempt - 1)))
+    print(f"{LOG_PREFIX}[SL] all {max_attempts} attempts failed", flush=True)
+    return None                      # → the existing emergency-close fail-safe fires
```

The `sl_id is None → emergency close` fail-safe at the call site is **unchanged** and still fires.

## B2 — `_move_stop_to`: the extracted primitive (reuse, not reimplementation)

Lifted from the inline BE call in `_monitor_positions:3746-3752`, unchanged in substance:

```diff
+def _move_stop_to(symbol, position_side, new_sl, *, label='move'):
+    """Set the position-level stopLoss. True on success, False on failure.
+
+    ONE attempt — NO silent retry. A failure leaves the exchange stop STALE BUT
+    PRESENT, i.e. WIDER than intended: never tighter, never absent. That is the safe
+    direction, and the caller alerts loudly rather than looping. The next tick
+    re-detects the mismatch and tries again, which is visible in the log.
+    """
+    pos_idx = 1 if position_side == 'LONG' else 2
+    try:
+        px = float(exchange.price_to_precision(symbol, new_sl))
+        resp = tor_retry.with_socks_retry(exchange, lambda ex:
+            ex.private_post_v5_position_trading_stop({
+                'category':    'linear',
+                'symbol':      exchange.market(symbol)['id'],
+                'positionIdx': str(pos_idx),
+                'stopLoss':    str(px),
+                'slTriggerBy': 'MarkPrice',
+            }), label=f'trading_stop.{label}')
+        ok = resp.get('retCode') in ('0', 0)
+        if not ok:
+            print(f"{LOG_PREFIX}[STOP-MOVE] {label} REJECTED {position_side} "
+                  f"→ {px}: {resp}", flush=True)
+        return ok
+    except Exception as e:
+        print(f"{LOG_PREFIX}[STOP-MOVE] {label} FAILED {position_side} → {new_sl}: {e}",
+              flush=True)
+        return False
```

**It stays on the READ wrapper deliberately.** `trading-stop` *sets* a value rather than appending
an order — idempotent by construction, exactly like the trail (Phase 1 §4 reasoning). No
idempotency key is needed or appropriate.

## B3 — 🔴 `_execute_partial_close`: the one new primitive

```diff
+def _execute_partial_close(symbol, position_side, qty, price):
+    """Reduce-only close of `qty` ONLY. Returns the ACTUALLY FILLED quantity (float),
+    or None if nothing was reduced.
+
+    THE RETURN CONTRACT IS THE POINT. The caller's fee split must follow what really
+    filled — not the intended fraction, not the quantised size. A partial fill makes
+    the realised fraction differ from BOTH, and net_pnl must still reconstitute the
+    whole position exactly once (proven by execution — see the report §5).
+    """
+    _state, pos = _fetch_position_state(symbol, position_side)
+    if _state is POS_UNKNOWN:
+        raise RuntimeError(f'position state UNKNOWN for {symbol} {position_side} '
+                           f'— refusing to partial-close blind')
+    if _state is POS_FLAT:
+        print(f"{LOG_PREFIX}[PARTIAL-LIVE] no position — nothing to reduce", flush=True)
+        return None
+    held = float(pos.get('contracts') or 0)
+    # Never reduce more than is held, and quantise to the venue step. `price` is the
+    # tick price the engine already holds — no network call added.
+    want, _qerr = quantise_amount(exchange, symbol, min(float(qty), held),
+                                  label='partial.live', price=price)
+    if want is None:
+        print(f"{LOG_PREFIX}[PARTIAL-LIVE] leg not tradable — SKIPPED, position "
+              f"rides the FULL trail", flush=True)
+        return None
+    close_side = 'sell' if position_side == 'LONG' else 'buy'
+    _idem = f'sol-p-{_vpos_id_for(symbol, position_side)}'[:36]
+    order = tor_retry.with_socks_retry_write(
+        exchange,
+        lambda ex, k: ex.create_market_order(
+            symbol, close_side, want,
+            params={'reduceOnly': True,
+                    'positionIdx': 1 if position_side == 'LONG' else 2,
+                    'clientOrderId': k}),
+        label='create_market_order.partial', idem_key=_idem)
+    # What ACTUALLY filled — never assume `want`.
+    filled = float((order or {}).get('filled') or 0) or None
+    if filled is None and (order or {}).get('id'):
+        try:
+            o = tor_retry.with_socks_retry(
+                exchange, lambda ex: ex.fetch_order(order['id'], symbol),
+                label='fetch_order.partial')
+            filled = float(o.get('filled') or 0) or None
+        except Exception as e:
+            print(f"{LOG_PREFIX}[PARTIAL-LIVE] fill read failed ({e}) — falling back "
+                  f"to requested {want}; accounting may differ from reality", flush=True)
+            filled = want
+    if filled and abs(filled - want) > 1e-9:
+        print(f"{LOG_PREFIX}[PARTIAL-LIVE] PARTIAL FILL: requested {want}, "
+              f"filled {filled} — accounting follows the FILLED size", flush=True)
+    return filled
```

The idempotency key is `sol-p-{vpos_id}` as you specified — one partial per position, so the key
is naturally unique and stable across retries.

---

# §4 — PART C: THE ADAPTER, AND THE 6 REDIRECTS

## C1 — how the engine reaches live code without an import cycle

`main` imports `virtual_trader`, never the reverse. **The codebase already solved this** with
`set_followthrough_hook`; Phase 2 uses the identical idiom rather than inventing one:

```diff
+_live_close = _live_partial = _live_move_stop = _live_pos_state = None
+
+
+def set_live_adapter(close_fn, partial_fn, move_stop_fn, pos_state_fn):
+    """main injects the live executors before start_worker. Keeps virtual_trader
+    free of any import of main — same pattern as set_followthrough_hook."""
+    global _live_close, _live_partial, _live_move_stop, _live_pos_state
+    _live_close, _live_partial = close_fn, partial_fn
+    _live_move_stop, _live_pos_state = move_stop_fn, pos_state_fn
```

## C2 — routing on OWNERSHIP, not on "are we simulating"

```diff
+def _is_paper(row):
+    """WHO OWNS THIS POSITION — the framing the whole phase turns on.
+    A row carries its own provenance, so a position opened in paper keeps being
+    managed as paper even if the mode is flipped underneath it. That is what makes
+    the switchover safe: ownership is a property of the POSITION, not of the process."""
+    return bool(row['is_paper']) if 'is_paper' in row.keys() else OBSERVATION_MODE_AT_OPEN
```

*(A one-column migration on `virtual_positions`; existing rows default to paper, which is what
all 19 of them are.)*

## C3 — the six redirects inside `_process_position`

**No decision logic is modified.** Only the action each decision takes.

| # | today | Phase 2 |
|---|---|---|
| BE stop move | `_apply_breakeven(vpos_id, be_price, mgmt_state)` | `_exec_move_stop(row, be_price)` → paper: same DB write · live: `_move_stop_to` + the same DB write |
| partial leg | `_apply_partial_at_arm(exchange, vpos_id, row, last, mgmt_state)` | `+ filled=` from the adapter; paper passes `None` (filled == quantised) |
| recheck tighten | `UPDATE ... sl_price` | `_exec_move_stop(row, new_sl)` |
| recheck emergency close | `_poller_close(..., 'post_entry_critical')` | `_exec_close(row, 'post_entry_critical', last)` |
| SL breach | `_poller_close(..., 'sl')` | `_exec_close(row, 'sl', last)` |
| trail breach | `_poller_close(..., 'trail')` | `_exec_close(row, 'trail', last)` |
| timeout | `_poller_close(..., 'timeout')` | `_exec_close(row, 'timeout', last)` |

with the close adapter carrying the absorbed monitor behaviour:

```diff
+def _exec_close(row, reason, price):
+    """Close via the owner's executor. Paper books at `price`; live sends a real
+    reduce-only close and books at the REAL fill."""
+    if _is_paper(row):
+        return _poller_close(row['id'], price, reason, row['symbol'],
+                             row['position_side'], _send_tg)
+    res = _live_close(row['symbol'], row['position_side'], reason=reason)
+    if res is None:
+        return None
+    return close_position(row['id'], float(res['fill_price']), reason)
```

## C4 — the POS_FLAT branch: the monitor's external-close detection, absorbed

Added at the top of `_process_position`, live rows only:

```diff
+    # PHASE 2: absorbed from the retired _monitor_positions. In live the
+    # AUTHORITATIVE close event is "the position is no longer on the exchange" —
+    # the resting stop or the trail fired. Book it from the REAL fill.
+    if not _is_paper(row) and _live_pos_state is not None:
+        _st, _p = _live_pos_state(symbol, position_side)
+        if _st == 'UNKNOWN':
+            print(f"{LOG_PREFIX}[ENGINE] vpos={vpos_id} position state UNKNOWN — "
+                  f"no action this tick (Phase 1 semantics)", flush=True)
+            return None
+        if _st == 'FLAT':
+            return _book_exchange_close(row)      # fetch_my_trades → real fill → close_position
+    # POS_OPEN (or paper) → every decision below runs EXACTLY as before.
```

**The engine's own `sl_hit` / `trail_hit` comparisons are untouched in both modes** — in live they
are the backstop you approved: if price is through the stop and the exchange still reports the
position open, the resting stop is missing and the engine closes.

---

# §5 — 🔴 THE ACCOUNTING, PROVEN BY EXECUTION

Run against a **throwaway DB** built from the real schema, with a prototype carrying the proposed
filled-size accounting. **No network** (a fake exchange mirrors SOLUSDT: step 0.1, min 0.1,
minNotional 5).

## Isolation first — per the 15:44 lesson

```
ISOLATED: post_exit_observatory.DB_PATH, skip_attribution.DB_PATH, state_machine.DB_PATH,
          signal_matrix.DB_PATH, signal_weights.DB_PATH, liquidity_sweep.DB_PATH,
          optimizer.DB_PATH, engine_15m.DB_PATH, market_context._DB_PATH
LEAKS TO LIVE DB: NONE
```

Nine modules patched, then a sweep of **every loaded module** asserting none still points at the
live path. **And the lesson proved itself:** `post_exit_observatory` *did* attempt a write during
the run and hit the proof DB (`no such table: post_exit_observatory`). That traceback is the
evidence the isolation worked — unpatched, exactly that call would have written to the live DB.

Live DB verified untouched after the run: **19 positions, ids 7–25**, unchanged.

## Three scenarios, `size=137.9`, entry 72.47, partial @ 71.70, close @ 70.50

| scenario | filled | realised fraction | remainder | net_pnl Δ | fees Δ |
|---|---|---|---|---|---|
| **A** filled == quantised (paper; live full fill) | 45.9 | 0.33284989 | 92.0 | **0.00e+00** | **0.00e+00** |
| **B** partial fill, filled < quantised (live only) | 31.4 | 0.22770123 | 106.5 | **0.00e+00** | **0.00e+00** |
| **C** fraction differs from BOTH intended and quantised | 12.7 | 0.09209572 | 125.2 | **0.00e+00** | **0.00e+00** |

```
================ ALL SCENARIOS: PASS ================
```

Each checked against an **independently computed** whole-position expectation:

```
expected = [(p_price-entry)·filled·d − entry_fee·frac − p_price·filled·rate]
         + [(c_price-entry)·rem·d   − entry_fee·(1−frac) − c_price·rem·rate]
```

`net_pnl` matched to **exactly zero difference** in all three, `total_fees` likewise, and
`initial_risk_usdt` was **untouched (100.0)** in all three — so R stays comparable across the
whole book.

**Scenario C is the one that matters**: the realised fraction (0.0921) differs from the intended
⅓ *and* from the quantised 0.3328, and the accounting still reconstitutes exactly once. That is
the property Phase 1 could not test, because paper has no partial fills.

---

# §6 — YOUR PRESERVE LIST, MAPPED

| requirement | how the diff meets it |
|---|---|
| **Six mechanisms live-reachable as the SAME code, no decision logic modified** | `_process_position`'s decisions are byte-identical; only the three *actions* are redirected. The recheck, partial, excursion sampler, dryrun sampler and water_mark/MAE become live-reachable purely because the poller now starts in live (A3) |
| **POS_UNKNOWN never destructive** | `_execute_partial_close` raises before any mutation; the new POS_FLAT/UNKNOWN branch returns without acting; `_execute_close_position` already raises (Phase 1) |
| **Idempotency keys on every write, incl. `sol-p-{vpos_id}`** | entry `sol-e-{row_id}`, SL — now a `trading_stop`, idempotent by construction, no key needed or appropriate; close `sol-c-…`; **partial `sol-p-{vpos_id}`** ✅ |
| **Quantised sizes, accounting follows the FILLED size** | `quantise_amount` in the partial primitive; `_frac = filled/size`. **Proven in §5 scenarios B and C** |
| **`initial_risk_usdt` untouched** | written by no adapter path; asserted in all three proof scenarios |
| **`net_pnl` = total realised PnL incl. the partial leg** | the `partial_pnl` / `partial_fees` fold-back in `close_position` is unchanged; proven to zero error in §5 |

**Not moved:** entry prompt and inputs, cascade, score gate, risk gates, thresholds,
`TRAIL_MULT_ATR`, `SL_BUFFER_ATR`, the arm point, `PARTIAL_AT_ARM_FRACTION`, `OBSERVATION_MODE`,
the optimizer, samplers and observatory beyond being reachable.

---

# §7 — WHAT I WANT YOU TO LOOK AT HARDEST

1. **B1 — moving the entry SL to the position-level mechanism.** It is the one substantive design
   choice inside the diff. It is *required* by your own condition once the venue said the
   conditional order does not follow size, and it removes a real dual-stop defect — but it changes
   how the stop is placed at entry in live, so it should be a conscious yes.
2. **A2 — the ownership test failing SAFE to "engine owns it".** On a DB error it declines to
   adopt. Adopting on doubt creates the second manager; declining costs nothing. I think that is
   right, but it is a judgement call.
3. **C2 — the `is_paper` column on `virtual_positions`.** Ownership becomes a property of the
   *position*, not the process, so a position opened in paper stays managed as paper even if the
   mode flips underneath it. This is what makes switchover safe, and it is a schema addition.

---

# 🛑 STOPPED

Nothing applied. `main.py` 18:29:22, `virtual_trader.py` 18:30:18 — untouched. Service running the
Phase 1 code, SOL PAPER, window **4 of 200**, vpos 25 open with its partial booked at 17:34:57,
Titan clean (`3316e8a`, active, no `.py` modified).

**Say go and I apply in the stated order — doors first (A1→A5), then B, then C — with snapshots,
`py_compile`, a deliberate restart, and the full confirmation set.**
