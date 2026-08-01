# sol-phase2-applied-one-manager-live

_2026-08-01 20:00 UTC_

---

# MERCURY-SOL — PHASE 2 APPLIED. ONE MANAGER, TWO ADAPTERS. LIVE.

Applied in the stated order — doors **A1→A5**, then **B**, then **C** — plus the two items you
added. Restarted **19:28:53** (worker pid 1160428), **zero tracebacks**. SOL stays **PAPER**. The
entry prompt and its inputs are untouched, **the window was not reset (4 of 200)**, vpos 25 is
open, reconciled, and byte-identical. Titan untouched.

---

# §0 — 🔴 ONE THING TO FLAG FIRST: MY IMPORT TEST WROTE TO THE LIVE DB

Before restarting I ran an import test with `DB_PATH` pointed at a **copy**, to catch import-time
errors without touching production. **It resolved to the live DB anyway.**

`main.py:42` is `load_dotenv('.env', override=True)`, and `.env` contains a `DB_PATH` entry. With
`override=True`, dotenv **overwrites the process environment** — so `DB_PATH=... python3` cannot
isolate `main`. `main.DB_PATH` printed the live path.

**What it did:** `init_db()` ran against the live DB and applied the `is_paper` migration —
`ALTER TABLE virtual_positions ADD COLUMN is_paper INTEGER DEFAULT 1`. It also ran
`_smart_boot_cleanup`, which issued a real `cancel-all/StopOrder` against Bybit.

**Impact: none beyond the intended change, verified.** The migration is exactly the one Phase 2
requires and is idempotent (`if col not in vp_cols`); all 19 rows backfilled to `is_paper=1`
(paper), which is what they are; **no row data was altered** — vpos 25's partial fields are
byte-identical below. The `cancel-all` was harmless: the venue reported **0 open orders**, and
SOL has never placed a live order.

**But it arrived via a test rather than the deliberate restart, and I am not going to describe
that as intended.** It also extends the 15:44 isolation lesson in a way worth recording:

> **`DB_PATH=… python3 -c "import main"` does NOT isolate this codebase.** `load_dotenv(...,
> override=True)` beats the process environment. The only safe isolation for `main` is to point
> `.env` itself elsewhere, or to patch `main.DB_PATH` *after* import and before any DB call.

Recorded in `OPEN-ITEMS-SOL.md`.

---

# §1 — THE TWO ITEMS YOU ADDED

## 1. 🔴 ADAPTIVE CADENCE — it was NOT there, and it is now

**Confirmed absent.** `virtual_trader._worker_loop` ended in a flat `time.sleep(interval)` with no
error tracking at all. Your read was right: with the engine now making a position read every tick
for every live row, on a link that produced 285 SOCKS retries and 26 CloudFront 403s in two days,
an outage would have become a hammering loop against a failing circuit.

**This was the monitor's THIRD unique behaviour**, and the design brief named only two. Absorbed
the same way as the other two:

| | |
|---|---|
| **Where it lives** | `virtual_trader._worker_loop` |
| **Cadence** | **10 s** normal (`MONITOR_POLL_SECONDS`) → **20 s** after **two consecutive** error cycles (`MONITOR_POLL_FALLBACK_SECONDS`), restored to 10 s on the first clean cycle |
| **Constants** | the **same two** the retired monitor used — no new tunables |
| **What counts as an error** | `_poll_once` now returns a boolean: a failed ticker fetch **or** any `_process_position` exception |

`_poll_once` was changed from returning `None` to returning `net_err`, so the loop can see failure
without swallowing it.

## 2. `_book_exchange_close` — it cannot book a close it cannot substantiate

This carries the monitor's most consequential absorbed behaviour, and the old version was
dangerous precisely because it wrote a close row from whatever `fetch_my_trades` returned. **Four
independent refusal paths, all returning `None` → the row stays OPEN and the engine retries next
tick.** No fabricated close, no unregister, no cancel.

```python
def _book_exchange_close(symbol, position_side):
    """The exchange closed the position (resting stop or trail fired). Recover the
    REAL fill and hand it back so the engine books it through its own accounting.

    🔴 IT CANNOT BOOK A CLOSE IT CANNOT SUBSTANTIATE. ...
    """
    try:
        recent = tor_retry.with_socks_retry(
            exchange, lambda ex: ex.fetch_my_trades(symbol, limit=10),
            label='my_trades.enginedetect')
    except Exception as e:
        print(f"... exchange reports FLAT but the trade read FAILED ({e}) — NOT booking "
              f"a close, NOT unregistering. Retrying next tick.")
        return None                                          # ← refusal 1: read failed
    exp_side = 'sell' if position_side == 'LONG' else 'buy'
    close_t = next((t for t in reversed(recent or []) if t.get('side') == exp_side), None)
    if not close_t:
        print(f"... FLAT but NO matching {exp_side} fill found — NOT booking (refusing to "
              f"substantiate from stale or absent data). Retrying next tick.")
        return None                                          # ← refusal 2: no matching fill
    try:
        px  = float(close_t['price']);  amt = float(close_t['amount'])
    except (TypeError, ValueError, KeyError) as e:
        print(f"... close fill unparseable ({e}) — NOT booking. Retrying next tick.")
        return None                                          # ← refusal 3: unparseable
    if px <= 0 or amt <= 0:
        print(f"... close fill not usable (price={px} amount={amt}) — NOT booking.")
        return None                                          # ← refusal 4: not usable
    fee = float((close_t.get('fee') or {}).get('cost') or 0)
    print(f"... exchange close substantiated: {amt} @ {px} fee={fee}")
    return {'fill_price': px, 'amount': amt, 'fee_cost': fee}
```

And the caller honours it — `None` returns before any close is booked:

```python
        if _st == 'FLAT':
            _booked = _live_book_close(symbol, position_side)
            if _booked is None:
                return None          # unsubstantiated → leave OPEN, retry next tick
```

**Same discipline as POS_UNKNOWN: when we cannot substantiate, do nothing and say so.**

---

# §2 — B1 VERIFICATION: IS A PROTECTED POSITION EVER READ AS NAKED?

You were right to make this a confirmation item — the stop moved from an *order* to a *position
field*, so anything reading an order list would now conclude a protected position is naked.

**Audited every stop-presence check. None reads an order list. No change was needed.**

| check | what it reads | verdict |
|---|---|---|
| **boot reconciliation** (`main.py:376`) | `p['info']['stopLoss']` — **the position-level field** | ✅ already correct for B1 |
| **SL fail-safe** (`_execute_single_entry`) | `if sl_id is None` — the return of `_place_sl_with_retry`, now truthy/None | ✅ works unchanged; emergency close still fires |
| **`_smart_boot_cleanup`** | `fetch_positions` for `has_open`; cancels via `cancel-all/StopOrder` | ✅ cannot clear a position-level stop (not an order) — Door 5 |
| **`_cancel_stop_orders`** | `cancel-all` `orderFilter=StopOrder` | ✅ targets conditional orders only |
| **`_cancel_open_orders_for_side`** | `fetch_open_orders` | ✅ used to clear pending orders before a close, not to verify protection |
| **Telegram entry card** (`entry['sl_id']`) | truthiness | ✅ `True` is truthy |
| **engine tick** | never inspected stop presence | ✅ unaffected |

**The one honest gap, pre-existing and unchanged:** nothing re-verifies the stop is *still* present
after entry. Same family as the unchecked `_place_trail_with_retry` return. Recorded, not fixed —
it belongs to the pre-flip list, not to Phase 2.

---

# §3 — WHAT SHIPPED

## Doors (A1–A5)

**A1 — `_monitor_positions` retired.** `start_monitor()` is a logging no-op; `_monitor_positions`
is left in the file with **no caller** (grep shows only two doc-comment mentions). Kept rather than
deleted so a future re-add cannot silently resurrect a second manager. Its **three** behaviours are
absorbed: external-close detection → the POS_FLAT branch; timeout killer → decision point 5 (same
constant); **adaptive cadence → `_worker_loop`**.

**A2 — the adoption block is engine-aware (Door 3).** `_engine_owns_position()` checks the engine's
book and the adoption block `continue`s on a hit, so it neither adopts nor persists nor Telegrams.
It **fails safe to "engine owns it"**: on a DB error it declines to adopt, because adopting on
doubt creates the second manager while declining leaves "unmanaged but protected" — the acceptable
side under Option C.

**A3 — both gates inverted.** `start_virtual_poller` and `_reconcile_open_virtual_positions` no
longer return early on live. Verified by code inspection (0 real gates; the only textual match is
the comment recording the removal) **and at runtime** — the reconcile fired and surfaced vpos 25.

**A4 — trend-reversal routed through the adapter (Door 6).** `_execute_close_position` now carries
`reason` through to the paper branch, so `'trend_reversal'` survives instead of being flattened to
`'exit_signal'`.

**A5 — `_smart_boot_cleanup` re-verified**, with the reasoning recorded in its docstring so it is
not re-derived: `cancel-all/StopOrder` targets *conditional orders*; the engine's stop is a
position attribute and cannot be cleared by it.

## Stop mechanism (B)

**B2 — `_move_stop_to`**, extracted from the retired monitor's inline breakeven call. One attempt,
**no silent retry**; stays on the read wrapper because `trading-stop` *sets* a value and is
idempotent by construction.

**B1 — the entry SL is now position-level**, so it follows size (venue-confirmed `tpslMode: Full`).
The partial needs no stop resize; the dual-stop defect is gone; entry, breakeven and tighten are
one mechanism. **Level unchanged** — `compute_initial_sl` and `SL_BUFFER_ATR` untouched. The
emergency-close fail-safe is preserved (`return None` on total failure).

## Adapter and redirects (C)

**C1** — `set_live_adapter(...)` injected by `main`, the same hook idiom as
`set_followthrough_hook`; no import cycle. Confirmed at boot:
`live adapter registered (close/partial/move_stop/pos_state/book_close)`.

**C2** — `is_paper` on `virtual_positions`, stamped at entry (`1 if OBSERVATION_MODE else 0`).
Ownership is a property of the **position**, so a row opened in paper stays paper even if the mode
flips underneath it. `_is_paper()` also returns paper when no adapter is registered — fail-safe.

**C3/C4** — six redirects (BE move, partial, recheck tighten, SL, trail, timeout) plus the
POS_FLAT/POS_UNKNOWN branch. **No decision logic was modified** — only the action each decision
takes.

## Two bugs I caught in my own edits before restarting

1. **`_new_sl` vs `new_sl`** in the recheck-tighten redirect — a `NameError` that `py_compile`
   would not catch, found by the name-resolution audit. Also moved the call **outside** the DB
   transaction so a slow network call never holds the write lock.
2. **`OBSERVATION_MODE` was not imported into `virtual_trader`** — the `is_paper` stamp would have
   raised `NameError` on the first entry. Caught by importing the module and checking the symbol,
   not by reading the code.

Both are the class the standing lesson names: a name that resolves at *call* time, inside a
statement the compiler happily accepts.

---

# §4 — CONFIRMATION SET

| # | check | result |
|---|---|---|
| 1 | **engine poller in PAPER adapter mode** | ✅ `engine poller starting — PAPER adapter for NEW positions` · `live adapter registered` · `poller started in pid 1160428 (interval=10s)` |
| 2 | **`start_monitor` logs RETIRED; `_monitor_positions` has no caller** | ✅ `[MONITOR] RETIRED — the paper engine is the single position manager in BOTH modes` · grep: only doc-comment mentions, **no call site** |
| 3 | **adoption block declines on engine-owned rows** | ✅ `_engine_owns_position(DEFAULT_SYMBOL, p_side)` guard at `main.py:396`, `continue` on hit |
| 4 | **`_reconcile_open_virtual_positions` not mode-gated** | ✅ **0** real gates in either it or `start_virtual_poller`; proven at runtime by the reconcile firing |
| 5 | **`is_paper` defaults to paper on all 19 rows** | ✅ `is_paper=1 → 19 rows`, none at 0 |
| 6 | **vpos 25 open, reconciled, partial fields byte-identical** | ✅ `[VPOS-RECONCILE] OPEN vpos=25 SHORT entry=72.47 sl=72.32506 age=2.1h`; `size 91.9333333333333`, `partial_size 45.9666666666667`, `partial_price 71.7`, `partial_pnl 31.7494754499998`, `partial_fees 3.64485788333333`, `partial_at 2026-08-01T17:34:57.241446+00:00`, `initial_risk_usdt 100.667000000001`, `is_paper 1` |
| 7 | **window not reset** | ✅ **4 of 200**, measured before *and* after the restart |
| 8 | **`OBSERVATION_MODE` True proven live in the new pid** | ✅ `[VIRTUAL] poller started in pid 1160428` — the live-mode branch prints a different line and returns |
| 9 | **entry prompt frozen** | ✅ `AI_ADVISOR_HIDE_1H = False`; `claude_advisor.py` 16:15:42, `config.py` 17:12:14 — **neither touched by Phase 2** |
| 10 | **Tor → Bybit** | ✅ `{"retCode":0,"retMsg":"OK","timeSecond":"1785612614"}` |
| 11 | **OKX book** | ✅ live, mid ≈ **$71.235** |
| 12 | **tracebacks since restart** | ✅ **0** |
| 13 | **`py_compile`** | ✅ `main.py`, `virtual_trader.py`, `tor_retry.py`, `stop_loss.py`, `config.py` |
| 14 | **Titan untouched** | ✅ `git status` clean · `HEAD 3316e8a` · service **active** · **no `.py` modified** |

Snapshots: `main.py.bak_phase2_onemanager_20260801`, `virtual_trader.py.bak_phase2_onemanager_20260801`
(both md5-verified pre-edit), `trades.db.bak_pre_phase2_20260801`.

---

# §5 — YOUR PRESERVE LIST

| requirement | status |
|---|---|
| **Six mechanisms live-reachable as the SAME code, no decision logic modified** | ✅ `_process_position`'s decisions are unchanged; only the three actions are redirected. They become live-reachable because the poller now starts in both modes |
| **POS_UNKNOWN never destructive** | ✅ `_execute_partial_close` raises before any mutation; the engine's UNKNOWN branch returns; `_execute_close_position` already raised (Phase 1) |
| **Idempotency keys on every write incl. `sol-p-{vpos_id}`** | ✅ entry `sol-e-{row_id}`, close `sol-c-…`, **partial `sol-p-{vpos_id}`**. The SL is now a `trading_stop` — idempotent by construction, so no key is appropriate |
| **Quantised sizes, accounting follows the FILLED size** | ✅ `_filled_override` drives `_frac = filled/size`; proven to exact zero error in three scenarios incl. a partial fill (19:45 report §5) |
| **`initial_risk_usdt` untouched** | ✅ written by no adapter path; vpos 25 still `100.667000000001` |
| **`net_pnl` = total realised PnL incl. the partial** | ✅ the `partial_pnl`/`partial_fees` fold-back in `close_position` is unchanged |
| **SOL stays PAPER** | ✅ `OBSERVATION_MODE` untouched and proven True in the new pid |

---

# §6 — WHAT IS STILL OPEN BEFORE ANY FLIP

Unchanged from the 17:46 study, minus what Phase 2 closed:

- **partial-fill handling on entry** (the partial leg now handles it; the *entry* still assumes a
  full fill);
- the **fee fallback to 0.0** when `fetch_order` fails;
- the **unchecked `_place_trail_with_retry` return** — a live position can still run with no
  trailing stop and nothing says so;
- **nothing re-verifies the stop is still present after entry** (§2);
- **news-gate sequencing**;
- the two pre-existing defects recorded earlier (duplicate armed-exit row;
  `_check_daily_loss_breaker` ignoring `is_virtual`);
- `_execute_armed_exit` consuming the arm even when the close fails (Phase-2 candidate raised at
  18:40, deliberately not changed — arm lifetime is a trading-behaviour decision).

**Phase 2 unified the manager. It did not enable live trading, and SOL is still paper.** The
engine now runs one code path for both modes, so when the flip comes the six mechanisms come with
it — which was the whole point.
