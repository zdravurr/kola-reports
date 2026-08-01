# sol-phase1-dangerous-semantics-diffs-for-approval

_2026-08-01 18:25 UTC_

---

# MERCURY-SOL — PHASE 1 DIFFS FOR APPROVAL. **NOTHING APPLIED. STOPPED AS INSTRUCTED.**

**No code was changed.** `main.py`, `virtual_trader.py`, `tor_retry.py`, `stop_loss.py` and
`config.py` are untouched since 18:00:08. The only write this session is documentation: the two
pre-existing defects recorded in `OPEN-ITEMS-SOL.md` per the "record, do not fix" instruction.
SOL is PAPER, the entry prompt and every input feeding it are untouched and frozen, the
200-window is intact, and **vpos 25 was not disturbed.** Titan untouched.

---

# YOUR PAPER-MODE EXPECTATION: **CORRECT, with one nuance**

> *"my expectation is that item 1 and item 2 are inert in paper, and only item 3 changes a paper
> number, via the partial's rounding."*

| item | inert in paper? | evidence |
|---|---|---|
| **1** — flat vs unknown | ✅ **inert** | The live monitor iterates `_active_positions`, and paper positions are **structurally barred** from that registry (`main.py:2889-2895`, explicit invariant). The table holds **0 rows**. `_execute_close_position`, `_open_side_for_arming` take the paper branch before reaching it. |
| **2** — order-write retry | ✅ **inert** | All four wrapped write calls live in the **live-only branch** of `_execute_single_entry` / `_execute_close_position`, which return before them in observation mode. No order exists to duplicate. |
| **3** — lot size | 🔶 **changes one paper number** | The partial's ⅓ leg. Entry sizing is unchanged (`amount_to_precision` already truncates 137.98813 → 137.9); only logging is added there. |

**The nuance on item 1:** one path is *reachable* in paper even though the monitor is not.
`_handle_5m_close` is a webhook handler — a 5m Group B signal in paper reaches it, gets `None`
from the empty exchange, and calls `_cancel_stop_orders(symbol)`, **a real Bybit API call.**

It is harmless today (no real orders exist to cancel) and — checked, not assumed — **it has never
once run**: zero `%group_b%` rows in the entire book, and zero
`STOP-CLEANUP … from _handle_5m_close` lines in the journal. So *in practice* inert, but the
correct statement is **"reachable but never triggered"**, not "unreachable". After the fix it
would additionally stop making that call on a failed read.

---

# 🔴 TWO CORRECTIONS TO MY OWN 17:46 STUDY

Found while designing these diffs. Both change the shape of the fix, so they come first.

## Correction 1 — §3.2 UNDER-COUNTED. There are **two** stop-cancel-on-unknown paths, and the second is worse.

The study named `_handle_5m_close`. It missed `_monitor_positions` (`main.py:3524-3567`):

```python
pos = _fetch_open_position(symbol, position_side)
if pos is None:
    # Position closed externally — SL or trailing stop fired on exchange.
    ...  writes a close row from fetch_my_trades ...
    _cancel_stop_orders(symbol)          # line 3566
    _unregister_active_position(...)     # line 3567
```

On a failed read this path does **three** damaging things where `_handle_5m_close` does one:

1. **fabricates a close row** with PnL, from whatever `fetch_my_trades` last returned;
2. **cancels the real stops** of a still-open position;
3. **unregisters it from the monitor** — so nothing manages it ever again, and no later cycle
   re-arms the stop.

This is the primary naked-position path, and it runs **every 10 seconds** against every live
position, versus `_handle_5m_close` which needs a specific webhook. **It is the more important of
the two and the study missed it.**

## Correction 2 — the duplicate-order risk is narrower than §4 stated, and the SL/close carry a *different*, worse defect

§4 said a retried close could produce "a reversed position". Checking each of the four wrapped
writes properly:

| call | retry-safe? | why |
|---|---|---|
| **entry** `create_market_order` (1660) | 🔴 **NO** | A duplicate is a genuine **double-size position**. This is the real duplication risk. |
| **SL** `create_order` (1566) | ⚠️ partly | A duplicate leaves a second resting stop — an orphan, not an immediate loss. |
| **close** `create_market_order` (1792) | ⚠️ partly | Hedge mode binds the order to `positionIdx`, so it reduces that slot rather than opening a reverse. **"Reversed position" overstated it.** |
| **trail** `private_post_v5_position_trading_stop` (1593) | ✅ **YES — safe** | It **sets** a value rather than appending an order. It is idempotent by construction. **No change needed.** |

**And why the duplication is possible at all — verified in ccxt 4.5.52 source:** ccxt assigns
`request['orderLinkId'] = self.uuid16()` when the caller supplies no `clientOrderId`. So **every
retry gets a fresh random idempotency key**, and Bybit's own duplicate-`orderLinkId` rejection —
the exact protection that would make a retry safe — **never engages.**

### 🔴 A FOURTH DEFECT, found while verifying this. `reduce_only` is not being applied at all.

`main.py:1794` and `main.py:1571` pass `params={'reduce_only': True, ...}` — snake_case. **ccxt's
bybit module reads only `reduceOnly`** (18 references to `reduceOnly`, **0** to `reduce_only`), and
the base class does not normalise it for order params.

I built the exact requests ccxt would send, without sending them:

```
CLOSE  {"symbol":"SOLUSDT","side":"Buy","orderType":"Market","category":"linear",
        "qty":"1.3","reduce_only":true,"positionIdx":2}
   reduceOnly present? -> False        raw reduce_only leaked? -> True

SL     {"symbol":"SOLUSDT","side":"Sell","orderType":"Market","category":"linear",
        "qty":"1.3","triggerDirection":2,"triggerPrice":"73.2","triggerBy":"MarkPrice",
        "reduce_only":true,"positionIdx":1}
   reduceOnly present? -> False
```

The key is passed through verbatim as `reduce_only`, which Bybit V5 ignores — it expects
`reduceOnly`. **So neither the close nor the stop-loss is reduce-only.** The code believes it has
a protection it does not have. Hedge-mode `positionIdx` provides partial structural cover, which
is likely why nothing has ever looked wrong — and the bot has never placed a live order, so this
has never been exercised.

A stop-loss that is **not** reduce-only is the sharper end: if the position is already gone when
the stop triggers, a non-reduceOnly stop **opens a new position**.

This is a one-word fix and it belongs in Phase 1. **Diff 2b below.**

---

# DIFF 1 — "FLAT" AND "UNKNOWN" STOP BEING THE SAME VALUE

## Design

Separate structurally, not by convention: a tri-state read, and `_fetch_open_position` is
**deleted** rather than left as an ambiguous convenience that a future caller could reach for.

**The precedent already exists in this codebase.** `_smart_boot_cleanup` (`main.py:1540-1558`)
already gets this exactly right:

```python
    except Exception as e:
        # Conservative: if we cannot verify state, do NOT cancel anything.
        print(f"{LOG_PREFIX}[SMART-CLEANUP] failed: {e} — DOING NOTHING to be safe", flush=True)
```

Diff 1 generalises that one correct instance to every consumer.

```diff
+# ── Position read: THREE outcomes, never two ─────────────────────────────────
+# 2026-08-01 Phase 1. `_fetch_open_position` returned None BOTH when the account
+# was genuinely flat AND when the Bybit read raised — so a transient Tor failure
+# was indistinguishable from "you have no position". Two consumers then took
+# destructive action on that None: _handle_5m_close cancelled every StopOrder for
+# the symbol, and _monitor_positions ALSO wrote a close row and unregistered the
+# position. Either one, on a failed read, leaves a live position with no stop.
+# Trigger is routine: 285 SOCKS retries / 26 CloudFront 403s in two days.
+#
+# FLAT is now a POSITIVE answer ("the exchange replied and reported no position").
+# UNKNOWN is its own outcome and NOTHING destructive may key off it.
+# The ambiguous helper is REMOVED, not kept alongside — leaving it would let a
+# future caller re-introduce the same bug by reaching for the shorter name.
+POS_OPEN, POS_FLAT, POS_UNKNOWN = 'OPEN', 'FLAT', 'UNKNOWN'
+
+
+def _fetch_position_state(symbol, position_side):
+    """(state, pos). state is POS_OPEN / POS_FLAT / POS_UNKNOWN.
+    POS_UNKNOWN means the read FAILED — the caller knows nothing and must not act."""
+    try:
+        positions = tor_retry.with_socks_retry(
+            exchange, lambda ex: ex.fetch_positions([symbol]),
+            label='positions.fetch_open')
+    except Exception as e:
+        print(f"{LOG_PREFIX}[POS-UNKNOWN] {symbol} {position_side}: position read "
+              f"FAILED ({e}) — state UNKNOWN, taking NO action", flush=True)
+        return POS_UNKNOWN, None
+    pos = next(
+        (p for p in positions
+         if (p.get('side') or '').upper() == position_side
+         and float(p.get('contracts') or 0) > 0),
+        None,
+    )
+    return (POS_FLAT, None) if pos is None else (POS_OPEN, pos)
-
-def _fetch_open_position(symbol, position_side):
-    try:
-        positions = tor_retry.with_socks_retry(
-            exchange, lambda ex: ex.fetch_positions([symbol]),
-            label='positions.fetch_open')
-    except Exception as e:
-        print(f"{LOG_PREFIX}fetch_positions failed: {e}", flush=True)
-        return None
-    return next(
-        (p for p in positions
-         if (p.get('side') or '').upper() == position_side
-         and float(p.get('contracts') or 0) > 0),
-        None,
-    )
```

## Every caller, and what it does under each of the three outcomes

**Caller 1 — `_execute_close_position` (`main.py:1780`), live branch**

```diff
-    pos = _fetch_open_position(symbol, position_side)
-    if pos is None:
-        return None
+    _state, pos = _fetch_position_state(symbol, position_side)
+    if _state is POS_UNKNOWN:
+        # MUST NOT return None here: every caller reads None as "no position" and
+        # records a successful no-op close. Raise so the existing try/except at each
+        # call site records status='failed' and alerts — the position is untouched.
+        raise RuntimeError(f'position state UNKNOWN for {symbol} {position_side} '
+                           f'— refusing to close blind')
+    if _state is POS_FLAT:
+        return None
```

| outcome | action |
|---|---|
| OPEN | close as today |
| FLAT | `return None` → callers report "no position" (correct, unchanged) |
| **UNKNOWN** | **raise.** All five call sites (1714, 1849, 2981, 3099, 3601) already wrap this in `try/except` → `status='failed'` + Telegram alert. **No new error handling is needed anywhere** — the existing handlers become correct for free. |

**Caller 2 — `_handle_liquidity_sweep` (`main.py:1838`)**

```diff
-    pos = _fetch_open_position(symbol, trigger_side)
-    if pos is None:
+    _state, pos = _fetch_position_state(symbol, trigger_side)
+    if _state is POS_UNKNOWN:
+        send_tg(f"⚠️ <b>{sweep_type} recorded — position state UNKNOWN</b>\\n"
+                f"{symbol}: Smart TP NOT evaluated (read failed). No action taken.")
+        return jsonify({'status': 'sweep_recorded', 'position': 'unknown'}), 200
+    if _state is POS_FLAT:
```

| outcome | action |
|---|---|
| OPEN | Smart TP closes, as today |
| FLAT | record sweep, no position (unchanged) |
| **UNKNOWN** | record sweep, **do nothing**, say so loudly. No order either way — this is a reporting-honesty fix. |

**Caller 3 — `_handle_5m_close` (`main.py:2915`, 2926-2931) — 🔴 the §3.2 path**

```diff
     open_pos = None
     open_side = None
+    _unknown = False
     for s in sides:
-        p = _fetch_open_position(symbol, s)
+        _st, p = _fetch_position_state(symbol, s)
+        if _st is POS_UNKNOWN:
+            _unknown = True
+            break
         if p:
             ...
+    if _unknown:
+        # 🔴 THE NAKED-POSITION GUARD. Previously a failed read fell through to the
+        # `open_pos is None` branch below and cancelled EVERY StopOrder for the
+        # symbol. On UNKNOWN we do NOTHING — no cancel, no consult, no close.
+        insert_signal(symbol, 'na', '5m_group_b', tv_tf=tf,
+                      tv_action=signal_name, status='position_unknown')
+        send_tg(f"⚠️ <b>5m Group B — position state UNKNOWN</b>\\n"
+                f"Read failed; stops NOT cancelled, nothing closed.\\n<i>{signal_name}</i>")
+        return jsonify({'status': 'position_unknown'}), 200
 
     if open_pos is None:
-        # Position not found — likely closed by SL/trail. The companion order may be orphaned.
+        # POSITIVE flat only — the exchange answered and reported no position. Safe
+        # to clear an orphaned companion stop.
         _cancel_stop_orders(symbol)
```

| outcome | action |
|---|---|
| OPEN | consult the exit advisor, maybe close (unchanged) |
| FLAT | cancel orphaned stops (**now only on a positive flat**) |
| **UNKNOWN** | **do nothing, loudly.** No cancel, no consult, no close. |

*If either side's read is UNKNOWN the whole decision is unsafe, so it short-circuits — a
half-known book is not a basis for cancelling stops.*

**Caller 4 — `_open_side_for_arming` (`main.py:3033`), live branch only**

```diff
-    return _fetch_open_position(symbol, side)
+    _state, pos = _fetch_position_state(symbol, side)
+    if _state is POS_UNKNOWN:
+        print(f"{LOG_PREFIX}[EXIT-ARM] {side} state UNKNOWN — NOT arming "
+              f"(safe default: an un-armed exit places no order)", flush=True)
+        return None
+    return pos
```

| outcome | action |
|---|---|
| OPEN | arm the exit (unchanged) |
| FLAT | do not arm (unchanged) |
| **UNKNOWN** | **do not arm, and say so.** Failing to arm is the safe direction — it places no order. Behaviour is unchanged; the silence is what is fixed. |

**Caller 5 — `_monitor_positions` (`main.py:3524`) — 🔴 the path the study missed**

```diff
-                pos = _fetch_open_position(symbol, position_side)
-                if pos is None:
+                _state, pos = _fetch_position_state(symbol, position_side)
+                if _state is POS_UNKNOWN:
+                    # 🔴 Previously fell into the "closed externally" branch and
+                    # (a) wrote a close row from stale fetch_my_trades data,
+                    # (b) cancelled the real stops, (c) unregistered the position so
+                    # nothing managed it again. On a failed read we do NOTHING and
+                    # retry next tick; count it as a network error so the adaptive
+                    # cadence backs off exactly as it does for any other fetch failure.
+                    cycle_net_err = True
+                    print(f"{LOG_PREFIX}[MONITOR] {position_side} state UNKNOWN — "
+                          f"no close row, no stop cancel, no unregister. Retrying.",
+                          flush=True)
+                    continue
+                if _state is POS_FLAT:
```

| outcome | action |
|---|---|
| OPEN | breakeven / timeout management (unchanged) |
| FLAT | position closed externally → write the close row, cancel the orphaned companion, unregister (unchanged, and now correct because it is a *positive* flat) |
| **UNKNOWN** | **nothing. Retry next tick.** Position stays registered, stops stay in place, no phantom close row. |

**Paper impact of Diff 1: none.** Callers 1 and 4 take the paper branch first; caller 5 iterates
an empty registry (0 rows in `active_positions`, and paper positions are barred from it by
invariant); callers 2 and 3 are reachable but have never run.

---

# DIFF 2 — ORDER WRITES CANNOT BE DUPLICATED

## What I chose, and why

**A separate write path with a caller-supplied, deterministic idempotency key — not a blind
retry, and not "no retry at all".**

Rejected alternatives, with reasons:

- **Exclude writes from retry entirely.** Simple, but leaves the entry *ambiguous* on a 403: the
  order may or may not exist and nothing resolves it. It converts a duplication risk into an
  unknown-state risk, which Diff 1 exists to eliminate.
- **Post-failure position re-check before retry.** Sound, but the re-check reads through the same
  Tor path that just failed, so on a 403 storm it returns UNKNOWN and we are back where we
  started.
- **Deterministic `orderLinkId` ✅.** Bybit rejects a duplicate `orderLinkId`. Re-sending the same
  key is therefore a genuine no-op at the venue: if attempt 1 never landed the key is unused and
  attempt 2 succeeds; if attempt 1 *did* land, attempt 2 is rejected as a duplicate and we treat
  that rejection as **success** and fetch the existing order. **The venue itself enforces
  exactly-once** — which is the only place it can be enforced correctly.

```diff
+def with_socks_retry_write(exchange, call, *, label, idem_key):
+    """Retry wrapper for ORDER-PLACING calls. Identical 403 isolation-retry to
+    with_socks_retry, with ONE structural difference: `call` receives the SAME
+    idempotency key on every attempt, so a retry that reaches the venue a second
+    time is rejected as a duplicate instead of creating a second order.
+
+    WHY THIS IS SEPARATE: the read wrapper retries blind, which is correct for
+    reads (idempotent) and WRONG for writes. ccxt assigns
+    `orderLinkId = self.uuid16()` when the caller passes no clientOrderId, so
+    every blind retry previously carried a FRESH key and Bybit's own duplicate
+    rejection — the protection that makes a retry safe — never engaged.
+
+    Reads keep using with_socks_retry unchanged. They are safe to repeat and they
+    are what keeps the bot alive through Tor (285 retries / 26 403s in two days).
+    """
+    if not SOCKS_RETRY_ENABLED:
+        return call(exchange, idem_key)
+    try:
+        return call(exchange, idem_key)
+    except Exception as e:
+        if not is_403_block(e):
+            raise
+        if SOCKS_RETRY_DRYRUN:
+            print(f"{LOG_PREFIX}[SOCKS_RETRY][DRYRUN] would-retry WRITE {label} "
+                  f"(403) idem={idem_key}", flush=True)
+            raise
+        last = e
+        for attempt in range(1, SOCKS_RETRY_MAX + 1):
+            try:
+                result = call(iso_exchange(exchange), idem_key)
+                print(f"{LOG_PREFIX}[SOCKS_RETRY] retried WRITE {label} via fresh "
+                      f"exit (attempt {attempt}) idem={idem_key} → ok", flush=True)
+                return result
+            except Exception as e2:
+                last = e2
+                if _is_duplicate_order(e2):
+                    # The FIRST attempt did reach the matching engine. The venue is
+                    # refusing to create a second order — which is the wrapper doing
+                    # its job. Surface it as duplicate-suppressed, never as failure.
+                    print(f"{LOG_PREFIX}[SOCKS_RETRY] WRITE {label} idem={idem_key} "
+                          f"already exists at venue — duplicate SUPPRESSED", flush=True)
+                    raise DuplicateSuppressed(idem_key) from e2
+                if not is_403_block(e2):
+                    raise
+        raise last
```

Call sites — entry gets a deterministic key derived from the trades row id, which is unique per
entry and stable across retries:

```diff
-    order = tor_retry.with_socks_retry(exchange, lambda ex: ex.create_market_order(
-        symbol, side, amount, params={'positionIdx': pos_idx}
-    ), label='create_market_order.entry')
+    _idem = f'sol-e-{row_id}'          # ≤36 chars; unique per entry, stable per retry
+    order = tor_retry.with_socks_retry_write(
+        exchange,
+        lambda ex, k: ex.create_market_order(
+            symbol, side, amount,
+            params={'positionIdx': pos_idx, 'clientOrderId': k}),
+        label='create_market_order.entry', idem_key=_idem)
```

`_place_sl_with_retry` and `_execute_close_position` take the same treatment with keys
`sol-sl-{row_id}` and `sol-c-{row_id}`.

**The trail is deliberately left on the read wrapper.** `position/trading-stop` *sets* a value
rather than appending an order — it is idempotent by construction, and re-sending it is harmless.
Changing it would add risk, not remove it.

## DIFF 2b — the `reduce_only` defect (one word, and it belongs here)

```diff
-        params={'reduce_only': True, 'positionIdx': 1 if position_side == 'LONG' else 2},
+        # ccxt's bybit module reads 'reduceOnly' ONLY — 'reduce_only' is passed
+        # through verbatim and Bybit V5 ignores it, so this order was NOT
+        # reduce-only despite the code saying so. Verified 2026-08-01 by building
+        # the request: {"qty":"1.3","reduce_only":true,...}, reduceOnly absent.
+        params={'reduceOnly': True, 'positionIdx': 1 if position_side == 'LONG' else 2},
```

…and identically at `_place_sl_with_retry` (`main.py:1571`). **A stop that is not reduce-only can
OPEN a position if it triggers after the position is already gone.**

**Paper impact of Diff 2 and 2b: none.** Every one of these calls is in a live-only branch.

---

# DIFF 3 — LOT SIZE: STEP, MINIMUM, AND ACCOUNTING THAT FOLLOWS THE ROUNDED SIZE

Bybit SOLUSDT, fetched live: **`minOrderQty 0.1`, `qtyStep 0.1`, `minNotionalValue 5`.**

## The shared helper

Placed in `stop_loss.py` — already the shared venue-aware policy module imported by **both**
engines (it owns `compute_initial_sl`). **No new file**, per the standing decision. The module
name is now slightly narrow for its contents; flagged rather than renamed, because renaming it
would touch both engines for no behavioural gain.

```diff
+def quantise_amount(exchange, symbol, raw_amount, *, label=''):
+    """Round an intended order size DOWN to the venue's lot step and validate it.
+
+    Returns (amount, err_pct) — or (None, err_pct) when the result is not tradable,
+    in which case the CALLER MUST NOT SEND AN ORDER.
+
+    Rounds DOWN, never up: an order slightly smaller than intended is a sizing
+    error; one slightly larger is unintended exposure.
+
+    The quantisation error is RETURNED and logged rather than swallowed. At the
+    intended live size ($100 notional) it is -5.79%, against -0.064% at the paper
+    size ($10,000) — a 90x coarser instrument that every R-multiple and every
+    optimizer statistic silently inherits unless it is on the record.
+    """
+    raw = float(raw_amount)
+    amount = float(exchange.amount_to_precision(symbol, raw))
+    err_pct = ((amount - raw) / raw * 100.0) if raw else 0.0
+    m = exchange.market(symbol)
+    min_amt = ((m.get('limits') or {}).get('amount') or {}).get('min')
+    if min_amt is not None and amount < float(min_amt):
+        print(f"[QTY] {label} REFUSED {symbol}: {raw:.6f} -> {amount} below "
+              f"minOrderQty {min_amt}", flush=True)
+        return None, err_pct
+    # Bybit exposes minNotionalValue under lotSizeFilter; ccxt leaves limits.cost
+    # empty for this market, so read it from the raw market info with a fallback.
+    try:
+        min_notional = float((m.get('info') or {}).get('lotSizeFilter', {})
+                             .get('minNotionalValue') or 0)
+    except (TypeError, ValueError):
+        min_notional = 0.0
+    if min_notional:
+        px = float(exchange.fetch_ticker(symbol)['last'])
+        if amount * px < min_notional:
+            print(f"[QTY] {label} REFUSED {symbol}: notional "
+                  f"${amount * px:.2f} below minNotionalValue ${min_notional}", flush=True)
+            return None, err_pct
+    if abs(err_pct) > 0.5:
+        print(f"[QTY] {label} {symbol}: {raw:.6f} -> {amount} "
+              f"(step quantisation {err_pct:+.3f}%)", flush=True)
+    return amount, err_pct
```

## Site A — live entry sizing (`main.py:1650`)

```diff
-    amount = float(exchange.amount_to_precision(
-        symbol, notional_usdt / current_price
-    ))
+    amount, _qerr = quantise_amount(exchange, symbol, notional_usdt / current_price,
+                                    label='entry.live')
+    if amount is None:
+        print(f"{LOG_PREFIX}[QTY] entry ABORTED — size not tradable at "
+              f"{notional_usdt} notional", flush=True)
+        send_tg(f"🚫 <b>Entry aborted</b> — size below venue minimum ({symbol})")
+        return None
```

## Site B — paper entry sizing (`virtual_trader.py:183`)

```diff
-    amount = float(exchange.amount_to_precision(symbol, notional_usdt / fill_price))
+    amount, _qerr = quantise_amount(exchange, symbol, notional_usdt / fill_price,
+                                    label='entry.paper')
+    if amount is None:
+        print(f"{LOG_PREFIX}[QTY] paper entry BLOCKED — size not tradable", flush=True)
+        return None
```

**No number changes at paper size** — `amount_to_precision` already produced 137.9. This adds the
minimum check and puts the quantisation error on the record.

## Site C — 🔴 the partial-at-arm leg (`virtual_trader.py:839`) — the one paper number that moves

**This is the site where the accounting must follow the rounded size, and today it does not.**

```diff
     size = float(row['size'])
-    qty  = size * PARTIAL_AT_ARM_FRACTION
-    rem  = size - qty
+    # Quantise the leg to the venue's lot step. At paper size 137.9 the intended
+    # third is 45.96667, which is NOT a valid multiple of the 0.1 step; at the
+    # intended live size ($100) it is 0.43333, which Bybit would REJECT outright.
+    _raw_qty = size * PARTIAL_AT_ARM_FRACTION
+    qty, _qerr = quantise_amount(exchange, row['symbol'], _raw_qty, label='partial')
+    if qty is None:
+        print(f"{LOG_PREFIX}[PARTIAL] vpos={vpos_id} SKIPPED — leg {_raw_qty:.6f} "
+              f"is not tradable at this venue. Position rides the FULL trail, "
+              f"unchanged.", flush=True)
+        return None
+    rem = size - qty
+    # 🔴 ACCOUNTING FOLLOWS THE ROUNDED SIZE, NOT THE INTENDED FRACTION.
+    # Every fee split below must use the fraction ACTUALLY realised, or net_pnl
+    # stops reconstituting the whole position and the invariant this mechanism
+    # depends on silently breaks.
+    _frac = qty / size
     if qty <= 0 or rem <= 0:
         ...
-    entry_fee_share = entry_fee_total * PARTIAL_AT_ARM_FRACTION
+    entry_fee_share = entry_fee_total * _frac
     ...
     for f in fills:
         if f.get('kind') == 'entry':
-            f['fee']  = f.get('fee', 0.0) * (1.0 - PARTIAL_AT_ARM_FRACTION)
+            f['fee']  = f.get('fee', 0.0) * (1.0 - _frac)
```

`_apply_partial_at_arm` would take `exchange` as a parameter; its single caller in
`_process_position` already has it in scope.

### What this changes in paper, concretely

| | today | after |
|---|---|---|
| leg on a 137.9 position | 45.96667 (not a valid lot) | **45.9** |
| fraction used for the fee split | 0.33333 (the *intended* fraction) | **0.332850** (the *realised* fraction) |
| remainder | 91.93333 | **92.0** |

A small, real change to future paper partials — and the accounting becomes correct rather than
approximately correct.

🔴 **vpos 25 is NOT touched.** Its partial was booked at 17:34:57 and the DB guard
`WHERE ... AND partial_at IS NULL` makes re-entry impossible. The change affects **future**
partials only. **Verified against the live row before writing this.**

---

# WHAT THIS DOES AND DOES NOT COVER

**Phase 1 as scoped fixes the semantics of the three dangerous items** — plus the two corrections
above, which I would not ship separately because they are the same defects seen properly.

**It does not make SOL live-ready.** Untouched and still required before any flip: the six
management mechanisms that exist only in paper (17:46 study §2), partial-fill handling, the fee
fallback to 0.0, the unchecked trail-placement return, the news-gate sequencing, and the two
pre-existing defects now recorded in `OPEN-ITEMS-SOL.md`.

## Risk of the change itself

| diff | risk |
|---|---|
| 1 | **Low.** Deletes an ambiguous helper so the bug cannot be re-introduced; every UNKNOWN branch is "do nothing". The raise in `_execute_close_position` relies on existing `try/except` at all five call sites — **verified present at every one.** |
| 2 | **Low-moderate.** New wrapper, but reads are untouched. The one thing needing care is treating a duplicate-order rejection as success rather than failure. |
| 2b | **Trivial to write, high value.** One word each in two places. |
| 3 | **Low, and the only one that changes a paper number.** Rounds down (never up), refuses rather than guessing when not tradable. |

---

# 🛑 STOPPED FOR APPROVAL

Nothing above is applied. `main.py` still has mtime 18:00:08 — unchanged since the `is_virtual`
fix. The service is running the code it has been running since 18:01:55, vpos 25 is open and
undisturbed, the window stands at **1 of 200**, and SOL is PAPER.

**Say go and I apply all three plus 2b, snapshot first, `py_compile`, restart deliberately, and
confirm — or tell me to drop 2b to a separate change if you would rather keep this attributable to
exactly the three items you named.**
