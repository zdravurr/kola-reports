# sol-live-order-scoping-study-read-only

_2026-08-01 17:46 UTC_

---

# MERCURY-SOL — WHAT IT TAKES TO PLACE REAL ORDERS. SCOPING STUDY.

**READ-ONLY. Nothing was changed, nothing is proposed as an action.** No file was written in
`mercury-sol` except this report's own publication path. The entry prompt was not touched; the
200-consultation window (opened 17:13:02) and its freeze are intact — this study read code and
the DB `?mode=ro`, and made no advisor call. **Titan was not touched and none of its numbers were
read.**

Sources: `main.py`, `virtual_trader.py`, `config.py`, `tor_retry.py`, `market_context.py`,
`liquidity_sweep.py`, `trades.db` (ro), the systemd journal, and Bybit's public
`instruments-info` endpoint.

---

# THE ANSWER FIRST

**The execution seam you asked for already exists and is clean. The position-management seam does
not exist at all — and that is the whole job.**

- `_execute_single_entry` and `_execute_close_position` **each already branch on
  `OBSERVATION_MODE` on their first line** and route to either the live order path or the paper
  engine. That is literally "one engine, two adapters", already built. **§6**
- But **the thing that manages a position after it opens is two different programs.** In paper it
  is `virtual_trader._process_position`; in live it is `_monitor_positions` plus Bybit-native
  orders. They implement **different feature sets**, and five mechanisms the paper book has
  **do not exist in the live path at all** — including the partial-at-arm ⅓ leg that shipped
  today. **§2**
- **Three paths are dead only because `_fetch_open_position` is always empty in paper. All three
  gain order authority on the flip**, and one of them contains the exact Titan naked-position
  class: **a Tor failure is indistinguishable from "no position", and the code responds by
  cancelling the real stop.** **§3**
- **Not a single line of minimum-order-size or step handling exists.** At the intended $100
  notional the quantisation error is **−5.79%** against **−0.064%** at paper size — a 90× worse
  instrument — and the partial-at-arm ⅓ leg computes a size that **is not a valid Bybit lot** and
  would be rejected. **§5, §8**
- **The news gate is already contaminated.** Its counter is not "stuck at 6 because SOL is paper";
  it is at 6 because **six paper closes were written with `is_virtual=0`** by a labelling bug. In
  live it counts both legs of every round trip, so it opens after roughly **12 live round trips**,
  not 30 trades — and that **changes the frozen prompt**. **§7**

**Honest sizing: 1–2 weeks of careful work, not a day.** The mechanical part is perhaps a day. The
part that can cost money is the management-path unification and the failure semantics. **§9**

---

# §1 — WHERE A FILL HAPPENS: EVERY ASSUMED PRICE

**Exact count: 8 sites assume a fill price. 2 more move a stop level with no exchange call. 10
total.**

Every paper price is the **same polled ticker `last`** — `_poll_once` fetches one ticker per
symbol per tick (`virtual_trader.py:1401-1403`) and passes that single float into everything below.

## The 8 assumed fill prices

| # | event | file:line | price used today | what must come from Bybit instead |
|---|---|---|---|---|
| 1 | **Entry fill** | `virtual_trader.py:171-172` | `fetch_ticker()['last']` | `order['average']` from the real `create_market_order` — actual VWAP of the fill |
| 2 | **Stop-loss execution** | `virtual_trader.py:1365-1367` | `last` at the tick the breach is *noticed* | the exchange's conditional-order fill price |
| 3 | **Trail execution** | `virtual_trader.py:1370-1376` | `last` at the tick | Bybit-native trailing-stop fill |
| 4 | **Timeout close** | `virtual_trader.py:1384-1387` | `last` | real close fill — **currently inert**, `MAX_POSITION_DURATION_MINS = 0` |
| 5 | **Partial-at-arm ⅓** | `virtual_trader.py:850-852` | `last` at the breakeven tick | a real reduce-only order fill — **and a valid lot size, see §8** |
| 6 | **Post-entry recheck emergency close** | `virtual_trader.py:~1172` (`_poller_close(..., last, 'post_entry_critical')`) | `last` | real close fill |
| 7 | **Exit-signal / armed-exit close** | `main.py:1754` (`_virtual_close_for_side`) | `fetch_ticker()['last']` | real close fill |
| 8 | **Trend-reversal close** | `main.py:3385-3386` | `fetch_ticker()['last']` | real close fill — **inert**, `TREND_REVERSAL_EXIT_DRYRUN = True` |

## The 2 stop-level moves with no exchange call

| # | event | file:line | today | live |
|---|---|---|---|---|
| 9 | **Breakeven move** | `virtual_trader.py:1302-1305` → `_apply_breakeven` | writes `sl_price` in SQLite | live already does the real thing: `private_post_v5_position_trading_stop` (`main.py:3568-3574`) |
| 10 | **Recheck SL tighten** | `virtual_trader.py:1087` + the `UPDATE` | writes `sl_price` in SQLite | **no live equivalent exists** — see §2 |

## 🔴 Two structural facts about these prices, not just their source

**(a) Stops fill at the detection price, not the stop price.** #2 and #3 close at `last` — the
price *observed on the tick that noticed the breach* — not at `sl_price` or the trail level. On a
10 s poll this silently models a stop that **cannot gap and cannot slip**. A real Bybit stop
triggers on MarkPrice and fills wherever the book is. Paper's stop is strictly better than reality
by an amount that grows with volatility, and nothing in the book records the difference.

**(b) Fees are modelled, never observed.** `BYBIT_TAKER_FEE_RATE = 0.00055` (`config.py:528`) is
applied on both legs (`virtual_trader.py:214, 418, 850`). Live reads the real fee via
`fetch_order` — and **falls back to `None`** when that read fails (`main.py:1666-1672`), after
which every PnL formula does `(result['fee_cost'] or 0.0)` and **silently books a zero fee**.

---

# §2 — IS IT SEPARABLE? EXECUTION YES, MANAGEMENT NO

**This is the answer to the whole study, so it is stated plainly: execution is isolated behind two
functions; management is two independent programs with different features.**

## Execution — isolated, already adapter-shaped ✅

| seam | branch | call sites |
|---|---|---|
| `_execute_single_entry` | `if OBSERVATION_MODE:` → `virtual_trader.execute_entry` (`main.py:1628-1638`) | **1** (`main.py:2771`) |
| `_execute_close_position` | `if OBSERVATION_MODE:` → `_virtual_close_for_side` (`main.py:1776-1777`) | **5** (`1714, 1849, 2981, 3099, 3601`) |

Every entry in the system flows through one function. Every *signal-driven* close flows through
one function. The Op-X follow-through resolver correctly re-enters via `_handle_5m_trigger` rather
than calling the paper engine directly. **This part needs no new architecture.**

**One leak:** `main.py:3386` calls `virtual_trader.close_position` **directly**, having queried
`virtual_positions` itself, with **no `OBSERVATION_MODE` branch**. It is inert today
(`TREND_REVERSAL_EXIT_DRYRUN = True`, `config.py:496`). If it were ever enabled in live it would
close the **paper row** while the **real position stayed open** — a phantom close and a naked
position simultaneously. It is the one place the adapter discipline is already broken.

## Management — 🔴 not separable, because it is duplicated

| mechanism | paper (`virtual_trader._process_position`) | live (`_monitor_positions` + Bybit) |
|---|---|---|
| Stop-loss | poller compares `last` vs `sl_price` | **real conditional order** placed at entry (`_place_sl_with_retry`) |
| Trailing stop | poller compares `last` vs `water_mark` | **Bybit-native trailing stop** placed at entry (`_place_trail_with_retry`) |
| Breakeven lock | SQLite write | `trading_stop` API call ✅ both exist |
| Timeout killer | ✅ | ✅ (both inert at `MAX_POSITION_DURATION_MINS = 0`) |
| **Partial-at-arm ⅓** | ✅ `_apply_partial_at_arm` | ❌ **does not exist** |
| **Post-entry recheck (T+10/60/300)** | ✅ 3 tiers, can emergency-close | ❌ **does not exist** |
| **Recheck SL tighten** | ✅ `_tighten_sl` | ❌ **does not exist** |
| **Excursion sampling** | ✅ 10 s grid | ❌ **does not exist** |
| **Smart-exit DRYRUN snapshot** | ✅ hourly | ❌ **does not exist** |
| **Adaptive-trail one-shot recompute** | ✅ at +1R | ❌ removed by design (D10) — live uses the Bybit-native trail |
| **water_mark / MAE tracking** | ✅ | ❌ **does not exist** |

**Six mechanisms exist only in paper.** Going live with today's code does not "change where the
fill happens" — it **silently drops six behaviours**, including the ⅓ partial applied today and the
post-entry recheck that can emergency-close a bad entry in its first 300 seconds.

**So the real question is not "how do I place an order".** It is: *does the paper poller become
the single manager for both modes (issuing real orders at its decision points), or does the live
path grow the six missing mechanisms?* The operator's "one engine, two adapters" standing decision
points at the first — and that means `_process_position`'s six decision points each need an
adapter, not just the two execution functions. **That is the work.**

---

# §3 — 🔴 THE THREE PATHS THAT WAKE ON THE FLIP

All three decide by calling `_fetch_open_position` (`main.py:1480-1493`), which queries Bybit and
is empty in paper. Here is what each does the **first time a real position exists**.

## 3.1 `consult_for_close` — the exit advisor, never once invoked

**Exactly one call site: `main.py:2956`**, inside `_handle_5m_close`, downstream of the
`_fetch_open_position` bail. Confirmed by grep across the tree.

**First live behaviour:** a 5m Group B signal arrives while a real position is open → the bot
sends a **real Claude consultation** built by `claude_advisor.consult_for_close`
(`claude_advisor.py:640`) → on `decide == 'close'` it calls `_execute_close_position` → **a real
reduce-only market order.**

- On `'unavailable'` it **holds** (`main.py:2963-2969`) — fail-closed to hold, correct.
- On not-close it holds and logs `ai_hold`.

🔴 **This is code with order authority that has never executed once in the bot's life.** Its
prompt has never been rendered, its JSON has never been parsed from a real response, and its
return contract (`.get('close')`, `.get('decide')`) has never been exercised against live model
output. The first time it runs it will be deciding whether to close real money. **It is not
"dormant but proven" — it is unproven.**

## 3.2 `_handle_5m_close` — 🔴 contains the naked-position class

This is the one to look at hardest. `main.py:2926-2931`:

```python
    if open_pos is None:
        # Position not found — likely closed by SL/trail. The companion order may be orphaned.
        _cancel_stop_orders(symbol)
```

And `_fetch_open_position` (`main.py:1485-1487`):

```python
    except Exception as e:
        print(f"{LOG_PREFIX}fetch_positions failed: {e}", flush=True)
        return None
```

**A Tor/Bybit failure returns `None` — the identical value as "you are flat".** So on any 5m
Group B signal, if the position fetch fails transiently, the bot concludes there is no position
and calls `_cancel_stop_orders(symbol)`, which cancels **ALL** conditional StopOrders for the
symbol — including the live stop of a position that is still open.

**Result: a real open position with its stop cancelled, and nothing that re-places it.** The live
monitor does not re-arm a missing stop; it only detects that a position vanished. This is the same
class that on Titan left a live position with no stop, arrived at by a different route.

The journal shows **26 CloudFront 403s and 285 SOCKS-retry lines in the last two days**, so the
triggering condition is not hypothetical — it is routine.

## 3.3 `_handle_liquidity_sweep` — Smart TP, dead twice

`main.py:1838-1849`: on an EQH sweep with an open LONG (or EQL/SHORT) it calls
`_execute_close_position` → **a real market close.**

Gated by `EQH_EQL_SMART_TP_ENABLED`. But it is **dead a second time, independently**, and I
verified the mechanism rather than taking it from the standing note:

- the router tests `signal_name.upper() in liquidity_sweep.SWEEP_TYPES` (`main.py:3276`)
- `SWEEP_TYPES = ('EQH', 'EQL')` (`liquidity_sweep.py:21`)
- TradingView sends `"Equal Highs"` / `"Equal Lows"`

`"EQUAL HIGHS" not in ('EQH','EQL')` → **the handler is never reached at all**, in paper or live.
So on the flip this path stays dead — *unless* someone fixes the string comparison, at which point
it gains real order authority in the same commit. **Those two changes must never ship together.**

## Summary

| path | can it place/cancel an order in live? | under what condition |
|---|---|---|
| `consult_for_close` / `_handle_5m_close` | ✅ **close order** | 5m Group B signal + real position + model says close |
| `_handle_5m_close` (no-position branch) | 🔴 **cancels the real stop** | 5m Group B signal + `fetch_positions` fails *or* genuinely flat |
| `_handle_liquidity_sweep` | ✅ **close order** | EQH/EQL + open matching side + flag on — **but the router never routes to it** |

---

# §4 — THE STOP LIVES IN A PYTHON POLLER

**In live it does not.** This is the one item where the live path is *stronger* than paper.

| | paper (today) | live |
|---|---|---|
| Stop | `_process_position` compares `last` vs `sl_price` every 10 s | **real Bybit conditional order**, `triggerBy: MarkPrice`, placed at entry with 3 retries (`_place_sl_with_retry`) |
| If it can't be placed | n/a | **emergency market close** of the position (`main.py:1708-1717`) — the naked-position guard exists and is correct |
| Trail | poller vs `water_mark` | **Bybit-native trailing stop** (`trailingStop` + `activePrice`) |

**So the stop moves to the exchange, and it is already written.**

## What a worker restart with an open position means

| | paper | live |
|---|---|---|
| While the process is down | 🔴 **no stop exists anywhere.** The stop is a Python comparison; if the poller is not running, nothing enforces it. A restart is an unprotected gap. | ✅ **the stop is resting on Bybit** and enforces itself. This is strictly safer. |
| At boot | `_reconcile_open_virtual_positions` surfaces the open row | `_load_active_positions_from_db` (`main.py:290`) rebuilds the registry and reconciles against `fetch_positions`; DB-open + exchange-closed → `_reconcile_closed_position` recovers the real PnL |
| If the reconcile fetch fails | n/a | `live_positions = None` → **the reconcile is skipped** and the row is restored as if still open (`main.py:308-310`). Safe-ish, but it means a Tor failure at boot leaves the registry unverified. |

**Today's restart at 17:13:02 happened with an open paper position** (vpos 25 opened 17:20 — after
it, so no gap occurred this time). Under the paper stop model, that gap is real and unmeasured.

## What the Tor round-trip adds

🔴 **Tor is not an optimisation — it is the only route.** Direct Bybit from this host returns:

```
{ error: The Amazon CloudFront distribution is configured to block access from your country }
```

Every Bybit call — ticker, positions, **and every order** — goes through
`socks5h://127.0.0.1:9050`.

Measured over the last two days in the journal: **285 `SOCKS_RETRY` lines, 26 CloudFront 403s.**

🔴 **And the retry has no idempotency guard.** `tor_retry.with_socks_retry` (`tor_retry.py:60-85`)
retries the **whole call** through a fresh circuit on a 403, up to `SOCKS_RETRY_MAX = 2`. The
order-placing calls are wrapped in it:

- `create_market_order.entry` (`main.py:1660-1662`)
- `create_order.sl` (`main.py:1566-1575`)
- `create_market_order.close` (`main.py:1792-1795`)
- `trail.set` (`main.py:1593-1599`)

There is **no `clientOrderId`, no idempotency key, and no post-retry position check.** If a 403 is
returned *after* the order reached Bybit's matching engine, the retry places a **second order**.
For an entry that is double size; for a close it is a reversed position. The read paths are safe
to retry; the write paths are not, and they share one wrapper.

---

# §5 — WHAT THE EXCHANGE ADDS, AND WHAT SOL HANDLES TODAY

| reality | handled today? | detail |
|---|---|---|
| **Partial fills** | 🔴 **no** | Entry assumes the full `amount` filled; `fill_price` reads `order['average'] or order['price'] or current_price`. A partially-filled entry records a size the position does not have. Close uses `pos['contracts']` (correct — reads the exchange). |
| **Order rejection** | ⚠️ **partial** | SL has 3 attempts + emergency close ✅. The **entry order has no retry at all** beyond the 403 wrapper — an exception propagates out of `_execute_single_entry`. The trail has 3 attempts and, on total failure, returns `False` which is **assigned to `tp_id` and never checked** (`main.py:1720`) — a position can run with no trailing stop and nothing says so. |
| **Slippage** | 🔴 **not modelled in paper**; live reads `order['average']` so it is real. The paper book has **zero** slippage in 18 positions. |
| **Real fees vs modelled 0.055%** | ⚠️ | Live fetches the true fee, but **falls back to `None` → booked as 0.0** on any `fetch_order` failure. |
| **Minimum order size / step** | 🔴 **no handling whatsoever** | Only `amount_to_precision`. No `limits['amount']['min']` check, no `minNotionalValue` check. Bybit SOLUSDT: **minOrderQty 0.1, qtyStep 0.1, minNotionalValue 5 USDT, tickSize 0.010.** See §8 for the numbers. |
| **Leverage / margin checks** | ⚠️ | `set_leverage` is wrapped in `try/except` that **only warns** (`main.py:1654-1657`) — if it fails, the order still goes at whatever leverage the account had. No free-margin precheck before ordering. |
| **Reconciliation after restart** | ✅ **yes, good** | `_load_active_positions_from_db` + `_reconcile_closed_position` + `_smart_boot_cleanup`. This is genuinely well built. |
| **Order filling during a restart** | ✅ | Covered by the same reconcile: DB-open + exchange-closed → recover real PnL from `fetch_my_trades`, write the close row (or flag for review under `RECONCILE_RECORD_DRYRUN`). |
| **API errors mid-management** | ✅ | `_monitor_positions` catches per-position, and backs cadence 10 s → 20 s after 2 error cycles, restoring on a clean cycle. |
| **Tor failing mid-order** | 🔴 **no** | See §4 — no idempotency, and §3.2 — a failed read is read as "flat". |

---

# §6 — WHAT ALREADY EXISTS, AND CAN IT BE THE ADAPTER

**Yes. The live path is not a sketch — it is complete, ordered code that predates observation
mode.** It should be the adapter, not a rewrite.

| function | file:line | what it already does |
|---|---|---|
| `_execute_single_entry` (live branch) | `main.py:1640-1733` | ticker → ATR → size → `set_leverage` → `create_market_order` (hedge `positionIdx`) → real fee via `fetch_order` → wall-anchored SL via the **shared** `compute_initial_sl` → SL order → trailing stop |
| `_execute_close_position` (live branch) | `main.py:1779-1816` | unregister → fetch position → cancel side orders → market close `reduce_only` → real fee → `_cancel_stop_orders` |
| `_place_sl_with_retry` | `main.py:1560-1585` | 3 attempts, exponential backoff, returns id or None |
| `_place_trail_with_retry` | `main.py:1588-1609` | 3 attempts against `position/trading-stop` |
| `_cancel_stop_orders` | `main.py:1511` | V5 `cancel-all` with `orderFilter=StopOrder` |
| `_fetch_open_position` | `main.py:1480` | the exchange-truth read (**and the §3.2 hazard**) |
| `_monitor_positions` | `main.py:3497` | BE lock via `trading_stop`, timeout killer, external-close detection + PnL recovery, adaptive cadence |
| `_load_active_positions_from_db` / `_reconcile_closed_position` / `_smart_boot_cleanup` | `main.py:290 / 214 / 1540` | full restart reconciliation |

**Shared-by-construction already:** `stop_loss.compute_initial_sl`, `trail_arm.activation_distance`,
`true_atr`, and the sizing formula are called **identically** by both paths — the paper engine's
docstrings explicitly say "IDENTICAL to `main._execute_single_entry`". That is real parity and it
is why this is a tractable job rather than a rewrite.

**What is missing is not entry/exit plumbing — it is the six management mechanisms of §2**, plus
the failure semantics of §3–§5.

**Dead weight worth knowing about:** `/_titan_brain/` is a **vendored copy of Titan's source**
(9 files including `main.py`, `config.py`) sitting inside `mercury-sol`. It is **imported nowhere**
— grep across every `.py` returns no reference. It is stale, it is not wired, and it is a standing
trap for anyone grepping this tree for "how does the live path work" and landing in the wrong
file. I did not read its parameters.

---

# §7 — 🔴 THE NEWS GATE: A FREEZE-BREAKING CONSEQUENCE OF GOING LIVE

`market_context.is_in_funding_news_observation()` (`market_context.py:280-299`) returns
`count < FUNDING_NEWS_OBSERVATION_TRADES`, where

```sql
SELECT COUNT(*) FROM trades WHERE status='executed' AND (is_virtual IS NULL OR is_virtual=0)
```

and `FUNDING_NEWS_OBSERVATION_TRADES = 30` (`config.py:209`). While it is `True`,
`main.py:2239` sets `_claude_news = None` — **news is withheld from the prompt entirely**, which
is why the 16:07 audit measured news missing on **100%** of 2,944 consultations.

## The counter is already contaminated — it is not "stuck at 6 because SOL is paper"

I expected 0. It is 6. Here is what those six rows are:

```
2148  2026-06-15  15m_armed_exit  executed   is_virtual=0
3318  2026-06-20  15m_armed_exit  executed   is_virtual=0
3507  2026-06-21  15m_armed_exit  executed   is_virtual=0
4220  2026-06-23  15m_armed_exit  executed   is_virtual=0
10309 2026-07-16  15m_armed_exit  executed   is_virtual=0
13716 2026-07-28  15m_armed_exit  executed   is_virtual=0
```

**All six are PAPER closes.** `_execute_armed_exit` writes its row via `insert_signal`, which does
not set `is_virtual`, so it takes the schema default **`is_virtual INTEGER DEFAULT 0`** — and
`update_trade` never corrects it. Every *other* paper row is correctly `is_virtual=1`
(`open_short` 11, `open_long` 8, `sl_triggered_short` 7, `sl_triggered_long` 5, `exit_*` 6).

**So a labelling bug in the armed-exit path has already advanced a live-mode gate by 6/30, using
paper trades.**

## When it opens, and what it adds

In live, entry rows stay `is_virtual=0` (only `virtual_trader` stamps 1) **and** every close row
written through `insert_signal` is `is_virtual=0`. **Both legs of a round trip count.** So:

- **24 more rows needed → roughly 12 live round trips**, not 30 trades.
- At that point `_claude_news` stops being `None` and the entry prompt gains a
  **`Recent news (last 2h):`** block of up to 500 characters (`claude_advisor.py:427-428`).

🔴 **This is inside the frozen surface.** The freeze covers *everything the advisor reads*, and
`news_summary` is an explicit named input. So:

> **Going live silently arms a change to the frozen entry prompt that will fire ~12 round trips
> later, without anyone touching the prompt.** The 200-consultation window would end up straddling
> two prompt forms again — exactly the pooling that today's window restart existed to prevent, and
> this time it would happen *by itself*.

**The sequencing decision must therefore be explicit.** The options are to finish the 200-window
before going live; or to pin `FUNDING_NEWS_OBSERVATION_TRADES` so the gate cannot open mid-window;
or to accept and pre-register the prompt change. **I am not choosing — I am flagging that doing
nothing is itself a choice, and the accidental outcome is the bad one.**

---

# §8 — POSITION SIZING

**Where it is decided — one formula, two copies, one constant:**

| path | line | code |
|---|---|---|
| live | `main.py:1649-1652` | `notional = MARGIN_USDT * LEVERAGE` → `amount_to_precision(notional / current_price)` |
| paper | `virtual_trader.py:182-183` | **identical** |

`MARGIN_USDT = 2000`, `LEVERAGE = 5` (`config.py:32-33`). **The same two constants size both
modes** — and `config.py:32` says so explicitly: *"this SAME constant sizes REAL orders once
un-paused."*

## Does it respect Bybit's minimum and step? **No check exists.**

Bybit SOLUSDT (fetched live): **`minOrderQty 0.1`, `qtyStep 0.1`, `minNotionalValue 5`,
`tickSize 0.010`**. ccxt reports `precision.amount = 0.1`, `limits.amount = {min: 0.1, max: 96000}`.

Measured through ccxt's own `amount_to_precision` at price $72.47:

| mode | notional | raw qty | quantised | actual notional | **error** |
|---|---|---|---|---|---|
| **PAPER** 2000×5 | $10,000 | 137.98813 | **137.9** | $9,993.61 | **−0.064%** |
| **LIVE** 20×5 | $100 | 1.37988 | **1.3** | $94.21 | 🔴 **−5.789%** |

**The intended live size sits at a 90× coarser quantisation than the paper book it will be
compared against.** $100 clears `minNotionalValue 5` comfortably, so it is legal — but every
R-multiple, every PnL%, and every optimizer statistic computed on live trades carries a −5.8%
size bias that paper does not have, and **nothing in the code notices or records it.**

## 🔴 The partial-at-arm ⅓ leg is not a valid lot size

`_apply_partial_at_arm` computes `qty = size * PARTIAL_AT_ARM_FRACTION` with **no rounding to
step** (`virtual_trader.py:839`):

| mode | size | ⅓ leg | step-valid? | remainder | step-valid? |
|---|---|---|---|---|---|
| PAPER | 137.9 | 45.96667 | ❌ | 91.93333 | ❌ |
| LIVE | 1.3 | **0.43333** | ❌ | **0.86667** | ❌ |

In paper this is harmless — no order is placed and the arithmetic is exact. **In live both legs
would be rejected by Bybit** (or silently re-rounded by ccxt, which changes the accounting the
partial's whole invariant depends on). At $100 the leg is only 4.3 lots; rounding to 0.4 or 0.5 is
a **±15% error on the partial leg**. This mechanism, applied today, **cannot go live as written.**

## Can $100 live and $10,000 paper coexist in one engine?

Yes, and it is the *easy* part — but not by changing `MARGIN_USDT`, because both paths read it.
It needs a mode-dependent resolution at the two sizing sites (`main.py:1649`,
`virtual_trader.py:182`) — one small shared helper, two call sites. The **hard** part is not
coexistence; it is that the two books are then **not comparable** (§10).

---

# §9 — THE HONEST NUMBER

## Surface

| | count |
|---|---|
| Files needing change | **3–4** (`main.py`, `virtual_trader.py`, `config.py`, possibly `tor_retry.py`) |
| Functions touched | **~14–18** |
| New files | **0** — consistent with the standing decision, and genuinely unnecessary |

## Effort: **1–2 weeks of careful work.** Not a day; not a month.

| phase | work | time |
|---|---|---|
| Mechanical | mode-dependent sizing; step/min rounding helper; `clientOrderId` on the 4 write calls; check the `_place_trail_with_retry` return value | **~1 day** |
| Management unification (§2) | give the six paper-only mechanisms real-order adapters, or accept losing them and say so explicitly | **3–5 days** |
| Failure semantics (§3, §4) | separate "flat" from "unknown" in `_fetch_open_position`; make the §3.2 stop-cancel conditional on a *positive* flat; idempotency on retries | **2–3 days** |
| First-live exercise of `consult_for_close` | it has never run — prompt, parsing, contract | **1 day** |
| Sequencing the news gate (§7) | a decision plus a guard | **hours** |

## Risk class — which parts can cost money

**🔴 Genuinely dangerous (can lose money in a way you would not immediately see):**

1. **§3.2 — the stop-cancel on a failed position read.** A live position with a cancelled stop.
   This is the Titan class, and its trigger (a Tor 403) happens routinely.
2. **§4 — retry without idempotency on order writes.** Double entry or a reversed position.
3. **§2 — the six missing management mechanisms.** Going live *silently* drops the post-entry
   recheck (which can emergency-close a bad entry) and the ⅓ partial. Nothing errors; the position
   is simply managed less.
4. **§8 — the partial's invalid lot size.** Either a rejection at the worst moment (the +1R arm) or
   a silent re-round that breaks the accounting invariant `net_pnl` depends on.

**⚠️ Moderate:** fee fallback to 0.0; `set_leverage` failing with only a warning; the unchecked
trail-placement return; partial-fill handling on entry.

**✅ Mechanical:** sizing constants, step rounding, the news-gate sequencing decision, the
`is_virtual` labelling bug.

---

# §10 — WHAT COULD SILENTLY DIVERGE

Not crashes. Quiet differences nobody would notice — ordered by how long they would go unseen.

1. 🔴 **Stops that cannot gap or slip.** Paper closes at the price it *noticed* the breach
   (`last`), not at the stop level. Live fills wherever the book is. Every paper stop-out in the
   book is optimistic by an unrecorded amount, and the two books will be compared as if they
   measured the same thing. **18 closed positions already carry this.**

2. 🔴 **A −5.8% size bias in live that paper does not have** (§8). Every R-multiple and every
   optimizer statistic inherits it. Nothing logs the quantisation error.

3. 🔴 **The news gate opening by itself ~12 round trips into live** (§7), changing the frozen
   prompt with no commit, no restart, and no report.

4. 🔴 **`is_virtual=0` on paper armed-exit closes.** Already true, already 6 rows. Any analysis
   that separates real from paper by this column is **already wrong**, and going live makes the
   two populations genuinely indistinguishable in that column.

5. 🔴 **Fees booked as 0.0** whenever `fetch_order` fails (`or 0.0`). Live PnL quietly reads better
   than reality; paper always charges its modelled 0.055%.

6. **Six management mechanisms silently absent in live** (§2). The position is simply managed
   differently, with no log line saying so.

7. **The trail may not exist.** `_place_trail_with_retry` returning `False` is assigned to `tp_id`
   and never inspected. A live position can run with no trailing stop and the DB will still show
   a `trail_pct`.

8. **`MAX_POSITIONS_PER_SIDE` is enforced by two different counters** — `virtual_trader._open_count`
   (SQLite) in paper, `fetch_positions` in live (`_risk_check`). In a mixed state, or when the
   fetch fails, they disagree. `_risk_check` is fail-closed on error ✅, which is the right choice.

9. **The 5m Group B path becomes live-only behaviour.** It is a *no-op today* in paper. So the
   exit advisor's refusals and closes will appear in the book **only after the flip**, and any
   before/after comparison will attribute their effect to "going live" rather than to "a path that
   was previously dead".

10. **`main.py:3386`'s direct paper close** (§2). Inert behind a DRYRUN flag, but it is a
    documented way to close the paper book while a real position stays open.

---

# WHAT I DID NOT DO

Read-only throughout: no file in `mercury-sol` was modified, no service restarted, no advisor
call made, no order placed, no config touched. The frozen entry surface is untouched and the
200-window is intact (**1 of 200**, vpos 25 still open). Titan was not touched and none of its
parameters were read; I noted `/_titan_brain/` exists and is unwired, and did not read its values.

**Nothing here is a proposal.** It is what is there.
