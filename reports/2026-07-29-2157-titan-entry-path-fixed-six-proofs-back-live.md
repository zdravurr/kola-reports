# titan-entry-path-fixed-six-proofs-back-live

_2026-07-29 21:57 UTC_

---

# TITAN — ENTRY PATH FIXED AT THE CLASS LEVEL, SIX PROOFS GREEN, BACK LIVE

**2026-07-29 21:55 UTC · HEAD 4ce8664 (fix: 97a4fdb) · 🔴 LIVE ORDERS · $30 × 5 = $150 notional**

**OUTCOME:** All five parts done, all six proofs pass, live restored. The fix was not
"pass the parameter" — the irreversible window is now wrapped so protection no longer
depends on reaching `place_stop`, and the entry lock moved *before* the order so the
double-entry race cannot recur. The scope audit part 1 demanded found **a second live
NameError of the same class on the CLOSE path**, fixed here too.

---

## PART 1 — THE IMMEDIATE BUG

`execute_entry` now takes `send_tg`, threaded the way every other function in
`virtual_trader.py` receives it.

**How many callers: exactly ONE.** You said not to assume two, so this was enumerated
rather than guessed:

```
main.py:1298   virtual_trader.execute_entry(...)   <-- THE ONLY call site
main.py:2126   _execute_entry(...)   } these three call main's own wrapper
main.py:3760   _execute_entry(...)   } (main._execute_entry, line 1255), which
main.py:4143   _execute_entry(...)   } routes to virtual_trader at 1298
```

So there is one place to pass it, and one place it can ever be wrong. All three `send_tg`
references inside the function — the stop placement and **both** orphan-cancel branches —
are covered by the single signature change, which is why fixing 684 alone would have
surfaced 704 and 749 on the next pass.

```diff
 def execute_entry(exchange, symbol, side, position_side,
                   trades_entry_row_id=None, pre_trade_walls=None,
-                  entry_adx_1h=None, entry_atr_pct_1h=None):
+                  entry_adx_1h=None, entry_atr_pct_1h=None, send_tg=None):
```

The `None` default is deliberate and documented: a caller that cannot supply it degrades to
"acts correctly, stays quiet" rather than raising. The failure mode being prevented is not a
missing *value* — it is a missing *name*, which raises while the argument list is being
evaluated.

## PART 2 — THE CLASS FIX

The order is irreversible from `order_adapter.market_entry`. The protection sat behind an
argument list ~90 lines later. Python evaluates arguments **before** entering the callee, so
the item-11 invariant inside `place_stop` was never entered — skipped, not attempted.

The region from the fill to the `INSERT` is now wrapped:

```python
        _entry_fill = order_adapter.market_entry(...)
        if _entry_fill is None:
            return None
        # ================== IRREVERSIBLE FROM HERE ==================
        ...  # sl calc, place_stop, capacity re-check, INSERT
    except BaseException as _entry_exc:
        _entry_failsafe_close(exchange, symbol, position_side,
                              _entry_fill, _entry_exc)
        raise
    finally:
        _entry_lock.release()
```

`BaseException`, not `Exception` — a `KeyboardInterrupt` during a deploy or a `SystemExit`
mid-entry is exactly as capable of orphaning a position as a `NameError`. The exception is
re-raised after the close so the entry handler still reports it (now with a traceback, part
5) instead of the caller silently reading `None` as "capacity blocked".

**Protection no longer depends on reaching `place_stop`.** A bad name, a `None` attribute, an
f-string, a network error — all now land in the same handler.

### What the handler does, and what it does if the close ITSELF fails

`_entry_failsafe_close` and `_failsafe_alert` take **only plain values** and resolve
`main.send_tg` themselves. This is the specific lesson of the incident: *a failsafe reached
through an argument is a failsafe with a prerequisite.* The alerting machinery was
unreachable last night precisely because it was passed in.

`_failsafe_alert` prints **first**, unconditionally, then attempts Telegram inside
`try/except BaseException` — so the record survives even if Telegram is down.

Paper vs live is decided by the **fill's own `simulated` flag**, not a mode re-read — it is
the only value that knows what happened to *that particular order*. In paper there is
nothing to unwind and it says so.

If the close itself fails:

1. **Retry** `FAILSAFE_CLOSE_ATTEMPTS = 3` with a 1s gap.
2. **Trip `_UNSAFE_STATE`** — `execute_entry` then refuses *every* further entry until a
   human restarts the service. We may be holding a position we could not unwind; piling a
   second one on top is the one thing that makes it worse.
3. **Escalate loudest** — `🚨🚨 CRITICAL — POSITION MAY BE OPEN AND UNPROTECTED`, naming the
   entry error, the close error and the amount, and stating that entries are now refused.

It does **not** pretend to have closed anything. A tripped breaker plus a hands-required
alert is the honest outcome. Note this deliberately trades availability for safety: a failed
failsafe stops the bot trading until a human looks.

## PART 3 — THE DOUBLE-ENTRY RACE

Your diagnosis was right, and it is worth being precise about *why* both caps failed, because
they failed for different reasons:

- **The DB cap** (`virtual_trader.py:693`) sat *after* the failing line, and would have
  counted **zero** even if reached — the row is written later. The defect that created the
  unsafe state also erased the record the cap depends on.
- **The exchange cap** (`risk_manager.concurrent_position_halt`) asked the venue one second
  after the first fill, before the venue reported the position. It only fired at 20:10, on
  entry #3.

Both were asking a question that **had no true answer yet**. No amount of re-ordering the
checks fixes that; the answer has to be made to exist.

**The lock does not ask — it waits.** `_entry_lock` is now acquired *before* the order, with
an authoritative capacity re-check under it:

```python
    if not _entry_lock.acquire(timeout=ENTRY_LOCK_ACQUIRE_TIMEOUT_S):
        print("... another entry is in flight (lock not acquired in 2.0s)")
        return None
    _entry_fill = None
    try:
        # AUTHORITATIVE PRE-ORDER CAPACITY CHECK — under the lock, microseconds
        # before the irreversible call, so it is the check that actually decides.
        with sqlite3.connect(DB_PATH) as _cap_conn:
            _n_open_pre = ... COUNT(*) ... status='open' ...
        if _n_open_pre >= MAX_POSITIONS_PER_SIDE:
            print("... open under the lock — no order sent")
            return None
        _entry_fill = order_adapter.market_entry(...)
```

Thread B now waits for thread A to finish its INSERT, then re-checks and sees a row. The
answer exists by the time it is asked.

The old post-order check and the `ux_vpos_one_open_per_side` unique index are both retained
as the second and third doors — the index still matters against a hypothetical
multi-process deploy, where an in-process lock proves nothing.

### It cannot deadlock the webhook path — four reasons

1. **Exactly one lock, exactly one acquisition site.** `grep -n _entry_lock virtual_trader.py`
   → one `acquire` (line 752), one `release` (line 949). No second lock exists in the module,
   so no lock-ordering cycle is constructible.
2. **No reentrancy.** `threading.Lock` is not reentrant, so the risk would be the same thread
   re-acquiring. `virtual_trader.execute_entry` is called from exactly one place
   (`main.py:1298`), and nothing inside the guarded region reaches it — including the
   failsafe, which goes to `main._execute_close_position(..., _from_adapter=True)`, the raw
   close mechanics that deliberately do **not** re-enter the engine.
3. **Bounded acquire.** `acquire(timeout=2.0)` means a waiting webhook thread is *never*
   parked indefinitely, even if an exchange call hangs while the lock is held. It gives up
   and skips. With `MAX_POSITIONS_PER_SIDE == 1` a queued second entry is never wanted, so
   skipping is the correct direction — **skipping an entry is safe; stacking one is not.**
4. **`release()` in `finally`.** The lock is released on every path — success, early return,
   `Exception`, `BaseException`.

Honest cost: the lock is now held across network IO (the order, the stop), where the old
comment correctly noted it previously cost microseconds. Entries are therefore serialized.
That is the intent, and with a per-side cap of 1 there is no throughput to lose. The
~12s of pre-trade IO (ticker/ohlcv/walls) remains **outside** the lock, unchanged.

One accepted trade-off, stated plainly: if thread A aborts below the exchange minimum, a
thread B that timed out waiting was skipped unnecessarily. A missed entry, never a naked one.

## PART 4 — `market_reduce`

```diff
     order = exchange.create_market_order(
         symbol, close_side, amt,
-        params={'positionSide': position_side, 'reduceOnly': True})
+        params={'positionSide': position_side})
```

BingX rejects the field in hedge mode (`code 109400`), proven live at 21:29 while closing the
naked short. The LONG 1/3 partial exit would have **raised instead of reducing**, and a
raising exit leaves a real position in place. It now matches
`main._execute_close_position`, which has always been right. The field was never needed —
the venue derives it from `positionSide`, and that same close came back reporting
`"reduceOnly": true` on an order that could not carry it.

## PART 5 — DIAGNOSTICS

`traceback.format_exc()` added to **all three** entry handlers. You named two; the P3 handler
at `main.py:4143` routes through the same `_execute_entry` and had the same bare `str(e)`
plus a label so generic (`ORDER ERROR`) it could not be attributed at all — same class, so it
got the same treatment.

The Telegram labels now name their own path:

| line | was | now |
|---|---|---|
| 2131 | `ORDER ERROR (confluence)` | `ORDER ERROR (plain-text 5m)` |
| 3771 | `ORDER ERROR (confluence)` ← **the wrong label** | `ORDER ERROR (state machine)` |
| 4302 | `ORDER ERROR` | `ORDER ERROR (P3)` |

## 🔴 BEYOND THE FIVE PARTS — A SECOND LIVE NameError, ON THE CLOSE PATH

The scope audit you required for proof 1 found one, and it is not hypothetical:

```
main.py:2594   if p is None and EXIT_ADVISOR_PAPER_ENABLED and not LIVE_TRADING_ENABLED:
```

`LIVE_TRADING_ENABLED` was **never imported into main.py** — absent from the
`from config import (...)` list at line 486 and defined nowhere in the module.
`hasattr(main, 'LIVE_TRADING_ENABLED')` → `False`, verified at runtime.

`EXIT_ADVISOR_PAPER_ENABLED` is `True`, so short-circuit evaluation does **not** save it: the
third operand is reached whenever `p is None` — i.e. whenever the exit advisor finds no
exchange position, which is the *normal paper path*. The comment above it records that this
fallback was added on 2026-07-26 to fix "the close advisor was never consulted in 65 days of
paper". **The fix raised `NameError` instead, so the advisor still never ran.** A repair that
silently failed the same way as the thing it was repairing.

Fixed by importing it. Same class as the entry bug, on the close path, and it would have
been live tonight.

### What this class endangers — the general answer

Any invariant implemented *inside* a callee, where the call site evaluates non-trivial
arguments, and where **the preceding statement already committed an irreversible side
effect**. The protected region starts at the function body; the risk window opened at the
caller. Everything in the argument list is a participant in the invariant — a name that may
be out of scope, an attribute that may be `None`, an f-string that may raise, a default
computed by a call, an unpacked dict — and all of it executes *outside* the protection.

Resolving arguments to locals before the risky region narrows the window; it does not close
it, and it should not be mistaken for a fix. Only moving the protection to the caller does.

The two instances found tonight had opposite symptoms — one opened a position it could not
protect, one silently disabled a feature for weeks — from identical causes. That is what
makes the class worth a permanent guard rather than two patches, and why the scope audit is
now a repeatable script rather than a one-off.

---

# THE SIX PROOFS — ALL PASS

Run in **PAPER**, against a **copy** of `trades.db` (`proof_trades.db`). The live book was
untouched and verified after: `0` open rows, `MAX(id)` still `85`.

## Proof 1 — no unresolved name anywhere in scope

Not just `send_tg`, and not just `execute_entry`: a `symtable` audit of every **function
scope** in the four order-path modules, asserting each free global resolves to a module
global or a builtin.

```
✅ all globals resolve  virtual_trader.py  (44 scopes checked)
✅ all globals resolve  order_adapter.py   (20 scopes checked)
✅ all globals resolve  breakeven_worker.py (20 scopes checked)
✅ all globals resolve  main.py            (72 scopes checked)
```

156 function scopes. This is the check that found the `LIVE_TRADING_ENABLED` defect above.

*Method note, since a proof is only worth its rigour:* the first version also flagged
`socket` at module scope. That was a **false positive** — `is_global()` is meaningless in the
module scope, where a function-local `import socket` (`main.reconcile_boot_state`) appears as
imported-but-unassigned. The checker was narrowed to function scopes and re-run. The
`LIVE_TRADING_ENABLED` finding was verified independently at runtime with `hasattr`.

## Proof 2 — paper entry reaches the INSERT, and `place_stop` is ENTERED

`place_stop` wrapped in a spy that records entry and delegates to the real function:

```
[SPY] place_stop ENTERED  amount=0.1572 stop=64714.5 send_tg=callable
VIRTUAL ENTRY vpos=89 SHORT amount=0.1572 @ 63595.5 sl=64714.5
returned: dict   place_stop entered: 1x, send_tg=callable
row sl_price=64714.5  stop_order_id=None (NULL in paper = correct)
==> PASS
```

**Entered, not skipped** — the distinction the incident turned on. `send_tg` arrives as a
callable. Row written with `sl_price` set, `stop_order_id` NULL because in paper the poller
still owns the stop.

## Proof 3 — both orphan-cancel branches, no NameError

Both reached deliberately, by making a competing row appear as a side effect of the fill:

```
-- 3a CAPACITY branch --
[SPY] cancel_stop id=None send_tg=callable
      reason=entry aborted: 1 position(s) already open on SHORT
returned=None  cancels=1  ==> PASS

-- 3b UNIQUE-INDEX branch --   (cap raised to 2 so the count check passes and
                                the partial unique index is what rejects)
[SPY] cancel_stop id=None send_tg=callable
      reason=entry aborted: unique index — another open position on this side won the race
returned=None  cancels=1  ==> PASS
```

Both formerly-latent sites now execute with `send_tg` resolved.

## Proof 4 — `place_stop` fails → the item-11 invariant genuinely runs

`_place_stop_with_retry` forced to return failure, with the stop treated as exchange-owned:

```
[ADAPTER] 🚨 STOP PLACEMENT FAILED — firing the emergency close invariant
[BE-FAILSAFE] BE SL recreate failed for BTC/USDT:USDT SHORT; emergency closing.
[SPY] _execute_close_position(BTC/USDT:USDT,SHORT,_from_adapter=True)
returned=None (entry aborted, no row)   open rows after: 0
send_tg received the BE alert: 1x -> '🚨 <b>BREAKEVEN SL RECREATE FAILED</b> 🚨...'
==> PASS
```

The invariant that never ran last night now runs, reaches the close with
`_from_adapter=True` (the raw mechanics, no recursion), writes no row, and **delivers its
alert** — the send that was impossible before.

## Proof 5 — exception between fill and INSERT → the wrapper closes the position

```
-- 5a PAPER fill (simulated=True) --
[ENTRY-FAILSAFE] 🚨 entry raised AFTER the fill ... simulated=True
re-raised to caller: RuntimeError   open rows: 0   paper alert: 1   ==> PASS

-- 5b REAL fill (simulated=False) --
[SPY] market_entry -> simulated=False amount=0.1571
[SPY] _execute_close_position(BTC/USDT:USDT,SHORT,_from_adapter=True)
🛑 ENTRY FAILSAFE CLOSE EXECUTED
close invoked: 1x · open rows: 0 · failsafe alert: 1 · breaker tripped: False   ==> PASS

-- 5c the close ITSELF fails --
[ENTRY-FAILSAFE] close attempt 1/3 FAILED  ... 2/3 FAILED ... 3/3 FAILED
🚨🚨 CRITICAL — POSITION MAY BE OPEN AND UNPROTECTED 🚨🚨
VIRTUAL ENTRY REFUSED: unsafe-state breaker is tripped
breaker=True  CRITICAL-alert=1  next-entry-refused=True   ==> PASS
```

5c is the answer to your question about the handler's own failure, demonstrated rather than
asserted: three retries, breaker tripped, hands-required alert, and the **next entry
actually refused**.

*One correction worth recording:* my first run of proof 5 reported FAIL while the behaviour
was correct in all three cases. The assertions watched the `send_tg` I passed in, but
`_failsafe_alert` resolves `main.send_tg` itself **by design** — so the test was wrong, not
the code. Fixing the test meant capturing `main.send_tg`, which also revealed that the first
run had delivered its test alerts to the real Telegram channel. You were told immediately.
The design decision that made my test wrong is the same one that makes the failsafe correct.

## Proof 6 — two simultaneous entries, exactly ONE order

Two threads calling `execute_entry` concurrently, counting `market_entry` invocations:

```
[SPY] market_entry CALLED (#1) t=1785361933.418
VIRTUAL ENTRY vpos=89 SHORT amount=0.1572 @ 63595.5
VIRTUAL ENTRY BLOCKED BTC/USDT:USDT SHORT: 1/1 open under the lock — no order sent
both threads done in 0.95s
market_entry CALLS: 1     results: {1: 'dict', 2: None}     open rows: 1
==> PASS
```

**One order, one row.** Thread 2 was blocked by the *pre-order* check under the lock — the
check that last night ran too late and against a record that did not exist.

---

## BACK LIVE — VERIFIED STATE

Exchange confirmed flat immediately before the flip: `0` positions (all symbols), `0` orders
(unified **and** raw `swapV2`), `used` margin `0.00`.

Deployed in two stages: restarted in PAPER first on the new code to confirm a clean boot,
then flipped and restarted. Boot banner:

```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
[TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
[RECONCILE] boot reconciliation starting
```

**The sizing line reads the LIVE number** (`$30 × 5 = $150`), not the paper `$2000 × 5 =
$10000`. No traceback, no NameError, no refusal, no tripped breaker in the boot log; one
worker, service `active`.

| | |
|---|---|
| HEAD | **4ce8664** (fix commit **97a4fdb**), pushed to `origin/main` |
| mode | 🔴 **LIVE ORDERS** — both flags True |
| sizing | **$30 × 5 = $150** notional (live number confirmed in banner) |
| exchange | flat — 0 positions, 0 orders, `used` 0.00 |
| USDT | 512.6111 |
| proofs | **6 / 6 PASS** |
| live book | untouched by testing — 0 open rows, `MAX(id)`=85 |

### Still open, NOT fixed tonight — carried from the 21:32 report

**There is still no exchange→DB reconciler.** `assert_single_owner_at_boot` checks
DB→exchange (open row with NULL `stop_order_id`); an exchange position with **no row**
returns zero rows and boots clean. Tonight's wrapper makes that state far harder to *create*
— every path out of the irreversible window either writes the row or closes the position, and
a failed close now trips the breaker — but nothing yet *detects* it if it ever exists. That
remains item 2 of the OPEN-ITEMS list, and it is the right next piece of work.
