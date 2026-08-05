# TITAN — `order_adapter` LIVE-ORDER SEMANTICS, AUDITED AGAINST THE MERCURY-SOL CHECKLIST

**2026-08-05 23:20 UTC · READ-ONLY · nothing changed, nothing committed · HEAD `22a085e`**

The 19:55 scope note left three things unaudited. This is the one that touches real money.
Mercury-SOL found four defects of this exact class on 2026-08-01 and fixed all four. Titan has
never been checked for them. **Two of the four are present here. One is present in a form SOL did
not have.** Three further defects were found by the same method as tonight's fourteen.

---

## §0 — NOTHING IS HALF-APPLIED

| check | result |
|---|---|
| **HEAD** | `22a085e` — the last confirmed commit. Nothing landed beyond it. |
| **Working tree** | `git status` **clean**. No uncommitted changes, no stray files. |
| **🔴 `openitems_guard.py`** | **exit 0** — canon `/mnt/…/kola-reports/reports/OPEN-ITEMS.md`, runtime HEAD `22a085e`, 11 watched values, header and current-state table **agree with runtime**. |
| **Service** | `active (running)`, up since **22:48:36 UTC**, `NRestarts=0`, 24 min uptime. |
| **Errors since 22:48:36** | **0** matches for traceback/error/exception/critical across all 51 journal lines. |
| **Four boot gates** | all green: `[ORDER-MODE] 🔴 LIVE ORDERS` · `[RECONCILE-XDB] ✅ exchange and DB agree (0 positions, 0 rows)` · `[RECONCILE] boot reconciliation` LONG+SHORT · `[STOP-CLEANUP] no orphaned orders` both sides. |
| **Exchange, both probes** | `fetch_positions` **and** raw `swapV2PrivateGetUserPositions`: **0 positions, 0 open orders, 0 probe errors**. |
| **`virtual_positions`** | **0 rows** with `status='open'`. Last position closed 2026-08-04 00:26 (vpos 92, `ai_exit`). **Exchange and DB reconcile.** |

**Runtime flags — read by IMPORTING config, not from the file:**

```
LIVE_TRADING_ENABLED      = True        EMA_ENVELOPE_GATE_ENABLED = True
ORDER_ADAPTER_LIVE        = True        EXIT_ADVISOR_DRYRUN       = False
SL_ATR_MULT               = 2.25        AI_ADVISOR_HIDE_1H        = False
TRAIL_MULT_ATR            = 1.6875      EQH_EQL_SMART_TP_ENABLED  = False
```

All eight match the canon. `TRAIL_MULT_ATR = 1.6875` is 0.75R × 2.25 — the 04.08 geometry, correct.
**§0 is clean. Proceeding.**

---

## THE SIZE OF WHAT IS BEING AUDITED

**Titan has taken exactly SEVEN live positions in its history** (vpos 86–92, 2026-07-30 → 2026-08-03).
All seven are closed. Every retry path, every failsafe and every emergency close audited below has
**NEVER EXECUTED ONCE**: `SL-RETRY`, `BE-SL-RETRY`, `SL-FAILSAFE`, `BE-FAILSAFE`, `ORPHAN STOP`,
`P3-CLOSE`, `P3-CLOSE-FALLBACK` — **0 occurrences across the entire journal.** Every finding below
concerns code that is armed and has never been fired.

**Today's fourteen commits touched NEITHER `order_adapter.py` NOR `breakeven_worker.py`** (verified
by `git log --since`). Nothing in this module changed tonight — which is why it was never checked.

---

## §1 — THE FOUR SOL DEFECTS, CHECKED HERE BY CODE

### 🔴 (a) FLAT vs READ-FAILED — **PRESENT, and one consumer does exactly what SOL's did**

Both position readers conflate the two outcomes. `main._fetch_open_position` (`main.py:1152`) and
its twin `breakeven_worker._fetch_open_position` (`breakeven_worker.py:182`) are identical:

```python
try:
    positions = exchange.fetch_positions([symbol])
except Exception as e:
    print(f"fetch_positions failed: {e}")
    return None                      # ← READ FAILED
return next((p for p in positions if …), None)   # ← GENUINELY FLAT
```

Both docstrings say *"or None"* and neither distinguishes. Nine consumers. Under the three outcomes:

| consumer | genuinely flat | **read failed** | position present |
|---|---|---|---|
| **`main._reconcile_side:5213`** | cancel orphan orders | **🔴 CANCELS EVERY ORDER ON THAT SIDE** | re-attach SL if naked |
| `main._execute_close_position:1235` | return None | return None → row left OPEN | close it |
| `main._handle_5m_close_via_ai:3175` | skip side | exit advisor **never consulted** | consult advisor |
| `main._handle_liquidity_sweep:3580` | "nothing to close" | **sweep close silently skipped** | Smart TP |
| `main._handle_exit_signal:3412` | — | **N/A** — routed to the DB via `engine_owns_position()` | — |
| `main._handle_state_machine:3803` | — | **N/A** — routed to the DB | — |
| `virtual_trader._reconcile_passive_fill:1152` | "position GONE" | **false 🚨 alarm** (see F5) | return False |
| `breakeven_worker` ×4 (`257/521/575/594`) | mark job closed | mark job closed — **stops managing** | manage |

The `breakeven_worker` consumers are **provably dead**: `breakeven_jobs` holds **0 rows** and
`_poll_once` returns immediately while `engine_owns_position()` is True. Not a live exposure.

**F1 — THE ONE THAT MATTERS. `main._reconcile_side` (`main.py:5212`):**

```python
def _reconcile_side(symbol, side):
    pos = _fetch_open_position(symbol, side)
    if pos is None:
        # No position → any surviving orders are genuine orphans (old behavior).
        _cancel_stop_orders(symbol, side)
        return
```

`_cancel_stop_orders` filters **only** on `positionSide` — no order-type filter — and cancels
everything it finds, including the item-11 protective `STOP_MARKET closePosition='true'`.

So: **an ordinary `fetch_positions` failure at boot, over a real open position, cancels that
position's protective stop and returns.** Nothing re-attaches it — the SL-recovery code at
`main.py:5295` sits *inside* the `pos is not None` branch. This is SOL's defect, same shape, same
consumer behaviour, on live money.

**It runs on every boot, both sides.** It ran 24 minutes ago (the `[STOP-CLEANUP]` lines in the boot
log are this function).

Three things sharpen it, and one blunts it:

1. **The same function already knows the rule and applies it ten lines lower.** For the *orders*
   read it does exactly the right thing — *"Can't confirm protection state → NEVER cancel; alert and
   leave alone."* The doctrine was written, then not applied to the read directly above it.
2. **It uses a SINGLE probe** while `assert_exchange_matches_db_at_boot`, running ~2 seconds earlier
   in the same boot, deliberately uses **two probes and three attempts** because *"one probe is not
   evidence"* (BingX conditional orders do not always surface through the unified call).
3. **The boot gate does not cover it.** The gate refuses to start only when `perr and not positions`
   — every probe failed. If the *unified* endpoint is down but the *raw* `swapV2` probe answers, the
   gate passes on the raw probe **with a warning** — and `_reconcile_side` then calls the unified
   endpoint that is still down. That is not a theoretical partial outage; it is the specific failure
   mode the double-probe exists for.
4. **Blunting it, and stated so this is not alarmist:** the position is not left with *no* protection.
   `virtual_trader._process_position:2702` evaluates `sl_price` in software on every 10-second poll
   in **both** modes and closes at market. So the real consequence is **degradation from an exchange
   stop to a 10-second-latency software stop** — no gap protection, no protection if the process
   dies, and the entire point of item 11 undone silently. Serious, not fatal.

### 🔴 (b) RETRIES WITHOUT AN IDEMPOTENCY KEY — **PRESENT, and it defeats the canon's §1a argument**

**There is no `clientOrderId`, `newClientOrderId` or idempotency key anywhere in the codebase.**
Grep returns zero hits across every module. Every order write is bare.

Three retry wrappers cover order-placing calls:

| wrapper | covers | attempts | key? | post-failure position/order check? |
|---|---|---|---|---|
| `breakeven_worker._place_stop_with_retry:206` | `create_order` STOP_MARKET closePosition | 3 × 1.0 s | **none** | **none** |
| `main._execute_entry:1465` (legacy, unreachable) | same | 3 × 1.0 s | **none** | **none** |
| `assert_exchange_matches_db_at_boot` probe loop | reads only | 3 × 2.0 s | n/a | n/a |

Entry (`market_entry`), close (`market_close`) and partial (`market_reduce`) are **not** retried —
a failure propagates. That is correct and deliberate.

**F2.** `_place_stop_with_retry` is reached from two places on the live path: `order_adapter.place_stop`
(every entry) and `move_stop_with_race_guard` (every breakeven, every recheck TIGHTEN). A failure
returned *after* the order reached BingX's matching engine — a timeout, a dropped response, a 5xx on
the way back — means attempt 2 places a **SECOND `STOP_MARKET closePosition='true'`**. Only the
second id is returned and stored in `virtual_positions.stop_order_id`; the first is invisible to the
bot.

**This is the state canon §1a calls catastrophic, and §1a's proof does not cover it.** §1a argues:

> *"a `TRAILING_STOP_MARKET` has exactly ONE creation site in the entire codebase … ⇒ **Exactly ONE
> `closePosition` order exists at any moment**: the item-11 `STOP_MARKET` (at breakeven it is
> cancelled and recreated, one at a time)."*

The argument enumerates **creation sites**. It never asks whether **one site can create two orders
from one logical call.** A three-attempt loop with no idempotency key can. Re-verified after
tonight's fourteen commits as §2c asks: **no new `closePosition` creation site landed** (the four
sites are `breakeven_worker.py:214`, `:531`, `main.py:1468`, `main.py:4821`, unchanged today) — but
the construction argument was **incomplete when it was written**, not broken by today's work.

Consequence if it happens: the invisible twin survives every subsequent `move_stop` (which cancels
only the recorded id), so a stop computed for the *entry* level rides alongside the breakeven stop
for the life of the position. On close, `_cancel_stop_orders`'s positionSide sweep *would* clean it —
but on the **passive-fill path** (`_reconcile_passive_fill`) no sweep runs at all.

**Never observed: 0 retries in the entire journal.** Unproven in both directions.

### ✅ (c) `reduce_only` — **NOT PRESENT. Checked by building the real request, not by reading the dict.**

SOL passed snake_case `reduce_only`; ccxt reads only `reduceOnly`; neither the close nor the stop was
reduce-only. **Titan does not have this defect, and the reason is stronger than "it got the case right":
Titan passes no reduce-only field at all, by explicit decision.**

- `grep reduce_only` across the codebase: **0 hits.** `reduceOnly`: 0 hits in Titan's own code.
- In ccxt 4.5.52's bingx module: `reduceOnly` appears 14 times, `reduce_only` **0** — confirming SOL's
  root cause and confirming Titan avoids it.
- `order_adapter.market_reduce:829` documents why: BingX **rejects** the field in hedge mode with
  `code 109400`, proven live 2026-07-29 while closing the naked short. Safety comes from
  `positionSide` instead: `sell` + `positionSide='LONG'` can only ever reduce.

**That argument depends entirely on the account being in hedge mode, so I verified it live rather
than trusting the comment:**

```
swapV1PrivateGetPositionSideDual() → {"code":"0","data":{"dualSidePosition":"true"}}
```

**Hedge mode is ON.** The reasoning holds.

**Requests built and inspected** (`exchange.fetch` intercepted; signed URL captured, nothing sent):

```
ENTRY    POST /openApi/swap/v2/trade/order
         positionSide=LONG  quantity=0.0014  side=BUY   symbol=BTC-USDT  type=MARKET
PARTIAL  POST /openApi/swap/v2/trade/order
         positionSide=LONG  quantity=0.0005  side=SELL  symbol=BTC-USDT  type=MARKET
STOP     POST /openApi/swap/v2/trade/order
         closePosition=true  positionSide=LONG  quantity=0.0014  side=SELL
         stopPrice=50000.0  symbol=BTC-USDT  type=STOP_MARKET
```

**`closePosition=true` DOES reach the wire** — ccxt passes it through via `extend(request, params)`.
The one parameter the whole stop design rests on is confirmed present in the real signed request.
No reduce-only field is sent on any of the three. **This one is clean.**

### ✅ (d) LOT SIZE — **HANDLED. Both orders are valid at today's price.**

`order_adapter.check_size` runs in **both** modes (so paper rejects what live would reject), enforces
`limits.amount.min`, `limits.cost.min`, rounds through `amount_to_precision`, and **fails closed** if
the market is unreadable. It is called by `market_entry` and `market_reduce`.

Live market spec, read tonight: `amount.min = 0.0001`, `cost.min = $2.00`, `precision.amount = 0.0001`,
`contractSize = 1.0`. BTC last = **$64,625**.

| order | raw | rounded | notional | valid? |
|---|---|---|---|---|
| **$150 entry** ($30 × 5) | 0.00232108 | **0.0023** | $148.64 | ✅ 23× above min amount, 74× above min cost |
| **⅓ partial** | 0.00076667 | **0.0007** | $45.24 | ✅ 7× above min amount, 22× above min cost |

Both valid, with real headroom. `amount_to_precision` **truncates** (verified: `0.00079999 → 0.0007`),
which is the safe direction. **But the truncation on the partial is not free — see F3.**

*Note: `check_size`'s docstring still cites "the intended $200 notional (0.0031 BTC) … 31x headroom".
The size is $150 / 0.0023 / 23×. Stale by one geometry change; the arithmetic it guards is correct.*

---

## §2 — TITAN-SPECIFIC, FROM ITS OWN HISTORY

### (a) The 2026-07-29 naked position — path still correct; the failure-of-the-failsafe is alerted but NOT recoverable-by-code

The invariant is intact and now exists in two places that **delegate** rather than restate:
`order_adapter.place_stop` → `_bw._emergency_close` (entry), and `move_stop_with_race_guard` →
`_bw._emergency_close` (moves). `place_stop` returns `None`, and `virtual_trader.execute_entry:975`
correctly treats `None` as "no position, write no row".

**What happens if the emergency close ITSELF fails:** both copies (`main.py:1505`,
`breakeven_worker.py:313`) wrap it and, on exception, print `CRITICAL: emergency close itself failed`
and send a Telegram alert with the symbol, side and error. **The alert fires** (each `send_tg` is
itself wrapped so a Telegram failure cannot swallow the journal line). ✅

**The state is recoverable, but only by a human, and the code does not say so.** After that branch,
`execute_entry` returns `None` and **no row is written** — so a real position exists on the exchange
with no stop and no DB row. Recovery is the next restart: `assert_exchange_matches_db_at_boot` sees
a position with `NO_ROW`, prints `PROTECTION: 🔴 NONE — THE POSITION IS NAKED`, and refuses to start.
That is a *correct* and *loud* design. But the recovery requires a restart nobody is told to perform:
the CRITICAL alert names the error and stops. **Never executed — 0 occurrences.**

### (b) §2.20's 356 ms window — fixed correctly; one OTHER cancel-then-create exists and it is unguarded

The §2.20 fix is real and well-built. `virtual_trader.py:1934` asks *"did the number actually
change?"* at **exchange precision on both sides** (`price_to_precision` applied to `current_sl` as
well as `new_sl`), deliberately with no epsilon — the comment explains that a price-scaled epsilon
would equal one tick at BTC $1M. Correct, and correct for any tick size.

**Every cancel-then-create on the live path, checked:**

| site | ordering | guarded? |
|---|---|---|
| `move_stop_with_race_guard:252` (breakeven + TIGHTEN) | cancel old → create new | ✅ cancel-fail → **keep old stop**, `'retry'`, tier stays due; create-fail → emergency close |
| recheck TIGHTEN caller `virtual_trader:1934` | — | ✅ §2.20 no-op guard, exchange untouched |
| breakeven caller `virtual_trader:2620` | — | ✅ no no-op guard needed — breakeven price (entry ± fee offset) can never equal the ATR stop (entry ∓ 2.25×ATR) |
| `main._execute_close_position:1259` | **close first, cancel after** | ✅ this is the 2026-07-30 fix |
| **`main.webhook()` legacy P3 close, `main.py:4783`** | **🔴 cancel ALL triggers FIRST, then close** | **❌ unguarded** |

**F7.** The legacy P3 close block still carries the **pre-2026-07-30 ordering** that was fixed
everywhere else: it cancels every `STOP_MARKET`/`TAKE_PROFIT_MARKET`/`TRAILING_STOP_MARKET`/`LIMIT`
on the side, *then* fetches the ticker, *then* sends the close. If `create_market_order` raises after
that — rate limit, 109400-class rejection, network blip — **the protective stop is already gone and a
real position is left naked.** That is verbatim the state the 2026-07-30 commit describes as having
*"sat latent on EVERY close path"*; this one was not converted.

Its guard blocks **paper only** (`if not order_adapter.orders_are_real(): BLOCKED in paper mode`) —
so in live it is **reachable by construction**, and its own comment concedes *"dormant is a property
of the current alert format, not a guarantee."* **0 occurrences in the journal.**

### (c) A second `closePosition` order — the configuration claim still holds; the CONSTRUCTION ARGUMENT does not

Re-verified after the fourteen commits: `_attempt_trail` (the `TRAILING_STOP_MARKET` site) remains
unreachable — `breakeven_jobs` has **0 rows**, `_poll_once` stands down by flag at
`breakeven_worker.py:437`, the enqueue sites are guarded at `main.py:5195` and `main.py:1528`, and the
engine's trail is a poller **close trigger**, not an order. **§1a Blocker A is still shut, and no
commit today touched either file.** ✅

**But §1a's stronger claim — "exactly ONE `closePosition` order exists at any moment" — is not
established**, for the reason in F2: the un-keyed three-attempt retry loop can produce two from a
single call. The claim is about *sites*; the risk is about *attempts*.

### (d) Item 14, partial fills on entry — CONFIRMED not implemented; the exposure is smaller than the canon implies, and there is a worse sibling

Confirmed: the canon's *"item 14 is still NOT implemented"* is accurate. There is no top-up, no
re-size, no abort.

**What happens today if BingX partially fills an entry** — better than "not implemented" suggests:

1. `_live_fill` reads `o['filled']` and returns it as `amount`; `market_entry` prints
   `🔴 PARTIAL FILL on entry … asked X, filled Y`.
2. `execute_entry:851` writes `amount = _entry_fill['amount']  # EXECUTED size, not the requested one`
   — so the row records the **real** size.
3. `place_stop` is called with that same executed size, **and the stop is `closePosition='true'`**,
   which covers the whole position regardless of quantity.

So the position is **correctly sized in the book and fully protected**. The residual is that the
trade is smaller than intended and its R is computed off a smaller base — a measurement effect, not
a money one. **That is why this is low-severity, and the canon does not say so.**

**F4 — the sibling, and it is worse than item 14.** `_live_fill:741`:

```python
executed = filled if filled else float(amount)
```

`filled` is used for **truthiness**, not for `is not None`. If BingX returns `filled = 0.0` — or omits
the field, which BingX market-order responses often do — `executed` silently falls back to the
**REQUESTED** amount. And `partial_fill` is computed as `filled is not None and abs(executed - amount) > 1e-12`,
which is then `False`. **A zero or unreported fill is recorded as a full position, with no warning
printed.** The stop is still `closePosition='true'` so nothing is left unprotected — but the row, the
P&L, the R and every downstream measurement are built on a size that was never filled.

---

## §3 — THE SAME METHOD AS TONIGHT

**F3 — 🔴 THE PARTIAL EXIT SHRINKS THE BOOK BY THE FRACTION IT ASKED FOR, NOT BY WHAT IT SOLD. ARMED LIVE.**

`virtual_trader._take_long_partial:1661`:

```python
cut_size = total_size * frac                    # 0.0023 × ⅓ = 0.00076667
_cut_fill = order_adapter.market_reduce(…, cut_size, last)
cut_size  = _cut_fill['amount']                 # ← 0.0007, the ROUNDED-DOWN executed size. Correct.
…
for leg in legs:
    leg['size'] = leg['size'] * (1.0 - frac)    # ← 🔴 shrinks by ⅓, NOT by what was executed
```

The realised PnL is computed on the **executed** 0.0007. The remaining position is written down by
the **requested** ⅓. Those are different numbers, because `check_size` truncated:

| | exchange | book |
|---|---|---|
| after a ⅓ partial on 0.0023 BTC | **0.0016 BTC** | **0.00153333 BTC** |

**The book understates the live remainder by 4.3% for the rest of the position's life.** Every
number derived from it — final close PnL, R multiple, average entry, the risk figure the exit advisor
reads — is computed on a size that is not the one at risk. Money is not directly lost (the stop is
`closePosition='true'` and `market_close` reads the **real** on-exchange size in live), but the
measurement is corrupted, and it is corrupted in the direction that makes the position look smaller
than it is.

**This is armed right now:** `LONG_PARTIAL_ENABLED = True`, `FRACTION = 0.3333…`, `LEVEL_R = 1.0`.
It has fired **once ever — vpos 82, which was PAPER** (`stop_order_id IS NULL`), where the arithmetic
is exact because nothing is rounded. **It has never fired live**, and it will fire on the first live
LONG that reaches +1R. The defect is invisible in the entire paper history by construction.

**F5 — a guard that cannot guard, and whose comment says it does.** `_reconcile_passive_fill:1149`:

```python
try:
    pos = _m._fetch_open_position(row['symbol'], row['position_side'])
except Exception as e:
    # Cannot tell -> do NOT guess. Leaving the row open is recoverable;
    # inventing a close is not.
    return False
```

The doctrine is exactly right. **The code cannot execute it:** `_fetch_open_position` already catches
`Exception` around `fetch_positions` and returns `None`. The `except` here can essentially never fire
for the network failure it was written for — the failure arrives as `pos = None`, and the next branch
reads `None` as *"the position is GONE"*. The comment describes a protection that is not wired to
anything. **Tonight's exact class: the mechanism is real, the path to it is not.**

Consequence, traced rather than assumed: with the position genuinely open, our stop is *not* filled,
so `read_filled_protective_order` returns `None` and the code lands in the
`🚨 POSITION GONE, STOP DID NOT FILL … MANUAL ACTION REQUIRED` branch — it **shouts and touches
nothing**, leaving the row open. So the outcome is a **false alarm**, not a money action. The
fail-safe direction saves it; the guard does not.

**F6 — one read that bypasses the routing.** `_handle_liquidity_sweep:3580` calls
`_fetch_open_position` **unconditionally**, while its four siblings (`3412`, `3803`, and both close
paths) correctly route through `virtual_trader.get_open_position()` when `engine_owns_position()`.
It is a read only, so nothing is mis-ordered — but under a `fetch_positions` failure it reports
*"No open LONG — nothing to close"* and silently skips a sweep-triggered exit.
(`EQH_EQL_SMART_TP_ENABLED = False` limits today's blast radius.)

**F9 — names and comments vs. code, minor:**
- `market_reduce`'s docstring and `_take_long_partial`'s both call it a **"reduce-only market order"**.
  It deliberately sends **no** reduce-only field — the body explains why, four lines below the
  docstring that contradicts it.
- `check_size`'s docstring cites `$200 notional (0.0031 BTC), 31x headroom`; the live size is `$150 /
  0.0023 / 23×`.
- `main.py:4823`'s degraded fallback rests on an **untested claim** — *"closePosition='true' … ignores
  quantity"* — for a plain `MARKET` order (proven only for `STOP_MARKET`). It passes `quantity = 0.0001`
  as a placeholder. If the claim is wrong, it closes **0.0001 BTC of a 0.0023 BTC position** and reports
  it as the full close. **Never executed.** It is the only path where a wrong assumption about
  `closePosition` converts directly into an unclosed live position.

**Paths that have never executed** (armed, unproven): every retry loop, both emergency closes, both
orphan-stop cancels, `_refuse_to_start`, `_alert_throttled`, the legacy P3 close, the degraded
fallback close, `_attempt_trail`, and all four `breakeven_worker` job handlers. **Flags that read as
armed and are inert:** `breakeven_worker`'s entire job machinery (`breakeven_jobs` = 0 rows,
permanently, by flag).

---

## §4 — VERDICT: RANKED BY HOW OFTEN THE PATH RUNS × WHAT IT COSTS

| # | finding | runs | cost if it fails | rank |
|---|---|---|---|---|
| **F1** | `_reconcile_side` cancels **every order on the side** when `fetch_positions` merely *fails* — single-probe, two seconds after a gate that triple-double-probes for this exact reason | **every boot, both sides** | exchange stop gone on a live position; degraded to a 10 s software stop, no gap protection, none at all if the process dies | 🔴 **1** |
| **F3** | ⅓ partial shrinks the book by the requested fraction, not the executed size → **book understates the live remainder by 4.3%** | **armed; first live LONG at +1R** | every downstream number wrong for the life of the position; invisible in all paper history | 🔴 **2** |
| **F2** | stop-placement retried 3× with **no idempotency key and no post-failure check** → two `closePosition` stops from one call; defeats §1a's construction proof | every entry + every breakeven + every TIGHTEN, **on failure only** | invisible twin stop survives every later `move_stop`; §1a calls this state catastrophic | 🔴 **3** |
| **F4** | `filled if filled else amount` — a `0.0`/absent fill is silently recorded as a **full** position, `partial_fill=False` | every live entry | position size, PnL, R built on a fill that never happened; **no warning printed** | 🟠 **4** |
| **F7** | legacy P3 close still **cancels all triggers before closing** — the ordering fixed everywhere else on 2026-07-30 | 0 so far; live-reachable by construction, guarded only against paper | failed close → naked live position | 🟠 **5** |
| **F5** | `_reconcile_passive_fill`'s "cannot tell → do not guess" guard is **unreachable** — the inner reader already swallowed the exception | every poll with a live stop | false 🚨 alarm; fail-safe direction saves it | 🟡 **6** |
| **F9c** | degraded fallback close relies on an **untested** `closePosition`-ignores-quantity claim for a plain MARKET order | 0 so far | closes 0.0001 of 0.0023 and reports it as the full close | 🟡 **7** |
| **F6** | `_handle_liquidity_sweep` reads the exchange unconditionally, bypassing the item-12 routing | per sweep signal | silently skipped exit under a read failure | 🟡 **8** |
| **F9a/b** | `market_reduce` documented "reduce-only" but sends none; `check_size` docstring cites the retired $200 geometry | — | reader is misled; code is correct | ⚪ **9** |

**Clean, and verified by construction rather than assertion:** SOL defect (c) — `reduceOnly` — is
**absent**, hedge mode is **live-confirmed ON**, and `closePosition=true` is **confirmed on the real
signed request**. SOL defect (d) — lot size — is **handled**, with 23× and 7× headroom on the two
live order sizes. Both `move_stop` callers are properly race-guarded, `_do_close` handles a `None`
from `market_close` correctly (row left open, position keeps its stop), and `_execute_close_position`
closes **before** cancelling.

**The through-line.** The four SOL defects sorted into two piles here. The ones about **what we send**
— reduce-only, lot size — Titan gets right, and gets right *deliberately*, with the reasoning written
down and the live facts (hedge mode, market limits) matching it. The ones about **what we believe we
read** — flat-vs-failed, retry-vs-duplicate — Titan gets wrong, in the same places SOL did, and in one
place (F5) it wrote the correct doctrine into a comment above code that cannot carry it out. F1 is the
sharpest instance: the identical function applies the rule correctly to the *orders* read and not to
the *positions* read directly above it.

**No fixes proposed. This is the map.**

---

*Read-only throughout: no order was sent, no file changed, no commit made. Requests were built through
ccxt's signer with `exchange.fetch` intercepted, so the signed URLs above are the real ones and none
of them left the box. Working tree clean at `22a085e`; `openitems_guard.py` exit 0.*
