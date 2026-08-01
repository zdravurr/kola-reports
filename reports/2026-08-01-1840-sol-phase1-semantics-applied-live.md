# sol-phase1-semantics-applied-live

_2026-08-01 18:40 UTC_

---

# MERCURY-SOL — PHASE 1 APPLIED AND LIVE. ALL THREE + 2b.

**Applied, compiled, restarted 18:33:54 (worker pid 1146889), zero tracebacks.** SOL stays PAPER.
The entry prompt and every input feeding it are untouched — **the 200-window was not reset and now
stands at 3 of 200**. vpos 25 open, reconciled, and provably unaltered. Titan untouched.

---

# WHAT SHIPPED

| diff | change | paper behaviour |
|---|---|---|
| **1** | `_fetch_open_position` **deleted**; `_fetch_position_state` returns `POS_OPEN / POS_FLAT / POS_UNKNOWN`; all 5 callers converted | **inert** |
| **2** | `with_socks_retry_write` — writes carry a stable venue idempotency key; reads unchanged | **inert** |
| **2b** | `reduce_only` → **`reduceOnly`** on the close and the stop-loss | **inert** |
| **3** | `quantise_amount` in `stop_loss.py`, applied at both sizing sites and the partial | **one number moves** |

Files changed: **4** — `main.py`, `virtual_trader.py`, `tor_retry.py`, `stop_loss.py`.
Snapshots: `*.bak_phase1_semantics_20260801`, all four md5-verified identical to pre-edit.
`py_compile` clean on all four plus `config.py`.

---

# §1 — YOUR CHANGE TO DIFF 3: NO NETWORK CALL ADDED. PROVEN, NOT ASSERTED.

You were right that a `fetch_ticker` inside `_apply_partial_at_arm` would be a bad trade — a
partial silently skipped because Tor hiccuped is worse than the rounding it fixes.

`quantise_amount` now takes an optional `price`, and **every one of the three call sites passes a
price it already holds**:

| site | price passed | already fetched? |
|---|---|---|
| `main._execute_single_entry` | `current_price` | yes — the entry ticker, line above |
| `virtual_trader.execute_entry` | `fill_price` | yes — the paper fill ticker |
| `virtual_trader._apply_partial_at_arm` | `price` (the poller's `last`) | yes — already a parameter |

The `fetch_ticker` fallback exists but is **unreachable from any current caller**.

**Proof rather than argument.** I pointed the exchange at a dead SOCKS port and re-ran the path:

```
market() with dead proxy            -> OK, local lookup. step= 0.1
amount_to_precision with dead proxy -> 45.9
quantise_amount(price=71.7)         -> qty: 45.9  err%: -0.145
```

`exchange.market()` and `amount_to_precision()` read the markets dict loaded at startup — no
network. **No site makes a call it did not previously make.**

---

# §2 — 🔴 CONFIRMATION 1: WHAT STATE A POSITION IS LEFT IN WHEN THE UNKNOWN-RAISE FIRES

You asked precisely. The answer is **untouched, still stopped, still registered, and nothing
retries.**

## The ordering matters, and I changed it

The original code unregistered the position *before* reading the exchange. That would have been
wrong under the new semantics — an UNKNOWN raise after unregistering would orphan a live position
from the monitor. So the read now happens **first**:

```python
    _state, pos = _fetch_position_state(symbol, position_side)
    if _state is POS_UNKNOWN:
        raise RuntimeError(...)          # nothing has been touched yet
    _unregister_active_position(symbol, position_side)
    if _state is POS_FLAT:
        return None
```

## What has and has not happened at the moment of the raise

| | state |
|---|---|
| Exchange position | **untouched** — no order of any kind was sent |
| Stop-loss / trailing stop | **still resting on the exchange.** `_cancel_open_orders_for_side` and `_cancel_stop_orders` both sit *below* the raise and are never reached |
| `_active_positions` registry | **still registered** — the unregister now sits below the raise |
| DB | `status='failed'` + the error text on the signal row |
| Operator | **Telegram alert sent** by the existing handler |

**Nothing is half-done.** The raise happens before the first mutating call in the function.

## Verified at all five call sites

Every caller already wrapped this in `try/except` — checked individually, not assumed:

| call site | handler | result on UNKNOWN |
|---|---|---|
| `main.py:1714` SL fail-safe emergency close | `try/except` → logs | logged, no second action |
| `_handle_liquidity_sweep` | `except` → `status='failed'` + TG | recorded + alerted |
| `_handle_5m_close` | `except` → `status='failed'` + TG | recorded + alerted |
| `_execute_armed_exit` | `except` → `status='failed'` + TG | recorded + alerted; **the arm is consumed** (see below) |
| `_monitor_positions` timeout close | `try/except` → logs | logged, retried next cycle |

**No new error handling was needed anywhere** — the existing handlers became correct for free.

## Does anything retry? — **Plainly: no, with one nuance**

**Nothing retries the close.** There is no retry loop around `_execute_close_position`. On UNKNOWN
the operation is abandoned and the system **waits for the next trigger** — the next 5m Group B
signal, the next sweep, the next monitor cycle.

The nuance, stated because it is a real asymmetry rather than a defect:

- **`_monitor_positions`** effectively *does* retry, because it re-reads every 10 s. Its own
  UNKNOWN branch (`continue`) is an explicit "retry next tick", and it now flags `cycle_net_err`
  so the adaptive cadence backs off 10 s → 20 s exactly as for any other fetch failure.
- **`_execute_armed_exit` consumes the arm regardless** — `state_machine.clear_exit_pending(side)`
  runs after the try/except. So an armed exit that hits UNKNOWN is **lost**, not retried. That is
  pre-existing behaviour and I did **not** change it: changing arm lifetime is a trading-behaviour
  decision, not a semantics fix, and it belongs to you. **Recorded as a Phase-2 candidate.**

The safe direction holds throughout: **on UNKNOWN the bot does nothing and says so loudly.**

---

# §3 — CONFIRMATION 2: vpos 25 UNTOUCHED, AND THE EXACT FUTURE-PARTIAL NUMBERS

## vpos 25 — verified after the restart, not before

```
           id = 25            status = open
         size = 91.9333333333333
 partial_size = 45.9666666666667      partial_price = 71.7
  partial_pnl = 31.7494754499998
   partial_at = 2026-08-01T17:34:57.241446+00:00
     sl_price = 72.32506
```

Byte-for-byte what it was before Phase 1. Re-entry is impossible by construction: the UPDATE
carries `WHERE id=? AND status='open' AND partial_at IS NULL`, and `partial_at` has been set since
17:34:57. The in-memory guard `mgmt_state['partial_done'] = true` is the second lock. **The old
`0.33333` fraction stays baked into this position's already-booked numbers — the change is not
retroactive and must not be read as though it were.**

## 🔴 THE NUMBERS THE FIRST FUTURE PARTIAL ON A 137.9 POSITION WILL USE

Computed through the shipped code path, not by hand:

| quantity | value |
|---|---|
| intended leg (`size × 1/3`) | 45.96667 |
| **quantised leg** | **45.9** |
| **realised fraction** (`qty / size`) | **0.332850** |
| **remainder** | **92.0** |
| step quantisation error | −0.145 % |

**Check the first one that fires against exactly these.** If it books `45.96667` / `0.333333` /
`91.93333`, the rounding did not take effect and Phase 1 diff 3 is not live.

The realised fraction is what now drives the fee split — `entry_fee_share = entry_fee_total *
_frac` and `f['fee'] *= (1.0 - _frac)` — so `net_pnl` still reconstitutes the whole position
exactly once. **Using the intended ⅓ against a rounded leg is precisely how that invariant would
have broken silently.**

---

# §4 — WHAT EACH DIFF ACTUALLY DOES

## Diff 1 — three outcomes, never two

`_fetch_open_position` is **deleted**, not deprecated — leaving it would let a future caller
re-introduce the bug by reaching for the shorter name. Residual grep shows only two *comment*
mentions and **zero code references**.

Per-caller behaviour under each outcome:

| caller | OPEN | FLAT | **UNKNOWN** |
|---|---|---|---|
| `_execute_close_position` | close | `return None` | **raise** — untouched, alerted (§2) |
| `_handle_liquidity_sweep` | Smart TP closes | record, no position | **do nothing**, `status='position_unknown'`, TG |
| `_handle_5m_close` | consult + maybe close | **cancel orphaned stops (positive flat only)** | **no cancel, no consult, no close** |
| `_open_side_for_arming` | arm | do not arm | **do not arm, and log it** |
| `_monitor_positions` | BE/timeout mgmt | write close row, cancel companion, unregister | **nothing; retry next tick; count as net error** |

`_handle_5m_close` short-circuits on the *first* unknown side: a half-known book is not a basis
for cancelling stops.

**The monitor was the worse path and is now fixed too** — it no longer fabricates a close row from
stale `fetch_my_trades` data, no longer cancels stops, and no longer unregisters a position it
cannot see.

## Diff 2 — writes cannot duplicate

New `with_socks_retry_write(exchange, call, *, label, idem_key)` hands the **same** key to every
attempt. Rationale in code: ccxt assigns `orderLinkId = self.uuid16()` when no `clientOrderId` is
given, so blind retries carried a fresh key and Bybit's duplicate rejection never engaged.

Keys: entry `sol-e-{row_id}`, SL `sol-sl-{row_id}`, close `sol-c-{side}-{ts}` (no `row_id` in
scope there).

`DuplicateSuppressed` is raised when a retry proves the first attempt landed, and is handled
differently per call because the right answer differs:

- **SL** → treated as **success**. The stop exists; the alternative would be the fail-safe
  emergency-closing a position that is in fact correctly stopped.
- **Entry** → **raise + explicit Telegram alert** saying a position may exist un-stopped and needs
  a manual look. Placing a second order is the one thing that must not happen.

**Reads keep `with_socks_retry` untouched** — they are safe to repeat and they are what keeps the
bot alive through Tor. **The trail stays on the read wrapper deliberately**: `position/trading-stop`
*sets* a value rather than appending an order, so it is idempotent by construction and moving it
would add risk, not remove it.

## Diff 2b — `reduceOnly`

Both the close (`main.py`) and the stop-loss now pass `reduceOnly`. Verified before the change by
building the request: it went out as `{"qty":"1.3","reduce_only":true,...}` with `reduceOnly`
absent, and Bybit V5 ignores the unknown key. **A stop that is not reduce-only can OPEN a position
when it triggers after the position is already gone** — which is why it stayed in this change
rather than becoming a "later".

## Diff 3 — lot size

`quantise_amount` lives in `stop_loss.py`, the module that already holds the shared
`compute_initial_sl` policy used by both engines — **no new file**. It rounds **down, never up**
(a smaller size is a sizing error; a larger one is unintended exposure), refuses rather than
guesses when below `minOrderQty`/`minNotionalValue`, and **logs the quantisation error** so it is
on the record instead of silently inside every R-multiple.

The live entry now aborts with a Telegram alert rather than sending an untradable size.

---

# §5 — PAPER IMPACT, AS PREDICTED

| diff | predicted | actual |
|---|---|---|
| 1 | inert | ✅ inert — the monitor iterates an empty registry (paper positions are barred by invariant); the other callers take the paper branch or have never run |
| 2 | inert | ✅ inert — all four writes are in live-only branches |
| 2b | inert | ✅ inert — same |
| 3 | one number moves | ✅ the partial leg only. Paper entry sizing is unchanged (137.9 either way); what is added there is the min check and the error log |

---

# §6 — STATE VERIFICATION

| check | result |
|---|---|
| Service / worker | **active**; master 1146835, worker **1146889 forked 18:33:54** |
| Tracebacks since restart | **0** |
| **`OBSERVATION_MODE`** | **True — proven live in the NEW pid**: `[VIRTUAL] poller started in pid 1146889`, whose alternative branch prints `poller not started (live mode)` and returns. **SOL is PAPER.** |
| **200-window NOT reset** | **3 of 200** — was 1 before this work; two consultations landed during it. Progress, not a reset. The window is defined by `timestamp >= 17:13:02`, which a restart cannot move |
| Prompt form unchanged | `AI_ADVISOR_HIDE_1H = False`; `claude_advisor.py` mtime **16:15:42** and `config.py` **17:12:14** — **neither touched by Phase 1**. Nothing the advisor reads changed, so no orphan set was created |
| **vpos 25** | **open, reconciled at boot**: `[VPOS-RECONCILE] OPEN vpos=25 SHORT entry=72.47 sl=72.32506 age=1.2h — poller continues managing it (no auto-close)`; partial fields byte-identical |
| `py_compile` | **OK** — `main.py`, `virtual_trader.py`, `tor_retry.py`, `stop_loss.py`, `config.py` |
| Snapshots | `*.bak_phase1_semantics_20260801` ×4, all md5-verified pre-edit |
| **Tor → Bybit** | ✅ `{"retCode":0,"retMsg":"OK","timeSecond":"1785609359"}` |
| **OKX book** | ✅ live, mid ≈ **$71.195** |

**Titan — untouched:** `git status` clean, `HEAD 3316e8a`, service active, **no `.py` modified**.

---

# §7 — WHAT PHASE 1 DOES NOT DO

Still required before any flip, unchanged from the 17:46 study:

- the **six management mechanisms that exist only in paper** (§2 of that study) — partial-at-arm,
  post-entry recheck, SL tighten, excursion sampling, smart-exit dryrun, water_mark/MAE;
- **partial-fill handling** on entry;
- the **fee fallback to 0.0** when `fetch_order` fails;
- the **unchecked `_place_trail_with_retry` return** — a live position can still run with no
  trailing stop and nothing says so;
- **news-gate sequencing**;
- the two pre-existing defects recorded in `OPEN-ITEMS-SOL.md` (duplicate armed-exit row;
  `_check_daily_loss_breaker` ignoring `is_virtual`).

**New Phase-2 candidate found while applying:** `_execute_armed_exit` consumes the arm even when
the close fails, so an armed exit that hits UNKNOWN is lost rather than retried (§2). Pre-existing,
deliberately not changed — arm lifetime is a trading-behaviour decision, not a semantics fix.

**Phase 1 fixed the semantics, not the capability.** SOL still cannot place an order, and that is
still the correct state.
