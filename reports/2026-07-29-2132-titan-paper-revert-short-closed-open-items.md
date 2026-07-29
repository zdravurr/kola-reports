# titan-paper-revert-short-closed-open-items

_2026-07-29 21:32 UTC_

---

# TITAN — BACK TO PAPER, NAKED SHORT CLOSED, AND FIVE STRUCTURAL ITEMS FOR OPEN-ITEMS

**2026-07-29 21:30 UTC · HEAD 11055e2 · both actions executed and verified · NameError deliberately NOT repaired**

**OUTCOME:** Live path disarmed first, then the naked SHORT closed at market. The exchange
is flat: zero positions on any symbol, zero orders through both the unified and raw
endpoints, `used` margin 0.00. Round-trip cost **−$0.2645** on a 84-minute exposure.
The `NameError` is untouched, per instruction.

---

## STEP 1 — LIVE PATH DISARMED (done first)

`config.py`: `LIVE_TRADING_ENABLED = False` (line 17), `ORDER_ADAPTER_LIVE = False` (line 35).

Committed **11055e2**, pushed to `origin/main` (`cb3a8bb..11055e2`), `titan.service` restarted
and `active`. Boot banner, verbatim:

```
[TITAN][ORDER-MODE] 🧪 PAPER — simulated fills only — no order can be sent (LIVE_TRADING_ENABLED=False)
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = False
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = False
[TITAN][ORDER-MODE]   sizing: margin $2000 x 5 = $10000 notional per entry
```

Both flags False, banner reads 🧪 PAPER. The LONG-side exposure that motivated doing this
first is closed: no order can reach the exchange from any path now.

*(Side note, not an action item for tonight: the paper banner reports the pre-live paper
sizing, `$2000 × 5 = $10000 notional`. That is the paper book's own size and is correct for
paper — but it means the paper book resumes at 67× the $150 live notional, so live and paper
statistics are not comparable across the flip.)*

## STEP 2 — NAKED SHORT CLOSED

### A rejected first attempt, which is itself a finding

The instructed parameters were `reduceOnly` + `positionSide='SHORT'`. BingX refused it:

```
ccxt.base.errors.ExchangeError: bingx {"code":109400,
  "msg":"In the Hedge mode, the 'ReduceOnly' field can not be filled.","data":{}}
```

**Nothing was sent; the position was untouched.** In hedge mode BingX derives intent from
`positionSide` alone, and `reduceOnly` is rejected as a contradictory field. The
battle-tested close in `main._execute_close_position` (`main.py:1236`) already knows this —
it passes `positionSide` only. I used those proven parameters.

This is safe rather than a compromise: in hedge mode `buy` + `positionSide='SHORT'` can only
reduce or close a short, never open one, so the call is inherently reduce-only. The exchange
confirmed it — the filled order's own record reads **`"reduceOnly": true`**, applied
server-side from `positionSide` even though the field could not be passed.

**See item 6 — this same rejected parameter combination is hardcoded in a live code path.**

### The close

```python
exchange.create_market_order('BTC/USDT:USDT', 'buy', 0.0046,
                             params={'positionSide': 'SHORT'})
```

| | |
|---|---|
| order id | `2082579253678010368` |
| status | FILLED (`closed`) |
| **fill price** | **63501.9** |
| filled | 0.0046 / 0.0046 |
| cost | $292.10874 |
| exchange-reported `profit` | **+$0.0276** |
| commission | −0.146054 USDT |
| time | 2026-07-29 21:29:21 UTC |

### Read-back confirmation — all four checks

```
fetch_positions(['BTC/USDT:USDT'])            -> count: 0
fetch_positions()          (ALL symbols)      -> 0 non-zero positions
fetch_open_orders('BTC/USDT:USDT')            -> count: 0
raw swapV2PrivateGetTradeOpenOrders{'symbol'} -> {"code":"0","data":{"orders":[]}}
raw swapV2PrivateGetTradeOpenOrders{}  (all)  -> {"code":"0","data":{"orders":[]}}
USDT balance -> {"free": 512.6111, "used": 0.0, "total": 512.6111}
```

`used: 0.0` is the independent confirmation — no margin is committed anywhere.

DB after the close: `virtual_positions` open rows **0**, `breakeven_jobs` rows **0** — as
before, because no row ever existed. `titan.service` `active`.

### Round-trip result — THREE fees, not four

All three fills, from `fetch_my_trades`:

| # | time (UTC) | side | amount | price | cost | fee |
|---|---|---|---|---|---|---|
| 1 | 20:05:13 | sell | 0.0023 | 63503.2 | 146.05736 | 0.073029 |
| 2 | 20:05:14 | sell | 0.0023 | 63512.6 | 146.07898 | 0.073039 |
| 3 | 21:29:21 | **buy** | **0.0046** | **63501.9** | 292.10874 | **0.146054** |

There were **three fees, not four**: two entry fills, and the close executed as a **single**
fill for the whole 0.0046, so it carried one commission. (Its 0.146054 is ~2× each entry fee
simply because it is 2× the size — the rate is identical.)

```
average entry   = (63503.2 + 63512.6) / 2      = 63507.90   (matches exchange entryPrice)
gross P&L       = (63507.90 - 63501.9) x 0.0046 = +$0.0276   (matches exchange "profit")
total fees      = 0.073029 + 0.073039 + 0.146054 = $0.292122
NET ROUND TRIP  = 0.0276 - 0.292122             = -$0.264522
```

**Balance cross-check.** Post-close total 512.6111 − pre-close total 512.7294 = **−0.1183**,
which equals `profit 0.0276 − close fee 0.146054 = −0.118454` to rounding. The entry fees
were already out of the pre-close figure, so implied pre-entry equity was
512.7294 + 0.146068 = 512.875468, and 512.6111 − 512.875468 = **−0.264368** — the net above,
confirmed from the other direction.

**No funding was charged.** The balance arithmetic closes exactly without a funding term;
the position lived 84 min 8 s and BingX funds on 8-hour boundaries.

**Bottom line: the incident cost $0.26, and 97% of that was commission on an accidentally
doubled position.** The direction was right; only the plumbing failed.

---

# STRUCTURAL ITEMS FOR OPEN-ITEMS — READ-ONLY, NOT REPAIRED

## 1. An invariant inside a function cannot protect its own argument list

`order_adapter.place_stop` holds the item-11 invariant — *"if the stop cannot be placed after
`SL_RETRY_ATTEMPTS`, the position is closed at market IMMEDIATELY"* — and its docstring calls
it the one requirement of item 11 that may not be traded away. It is correctly implemented.
**It never ran.**

Python evaluates a call's arguments *before* transferring control to the callee. The
`NameError` was raised while evaluating the keyword argument `send_tg=send_tg` at
`virtual_trader.py:684`, so `place_stop` was never entered. Its retry loop, its failure
branch and its `_bw._emergency_close(...)` call were not attempted-and-failed; they were
never reached. Proof: no `[ADAPTER] LIVE STOP` and no `[BE-FAILSAFE]` line exists anywhere
in the journal after the flip.

**The class of code this endangers:** any invariant implemented *inside* a callee, where the
call site evaluates non-trivial arguments. The protected region begins one step too late —
it starts at the function body, but the risk window opened at the caller. Concretely, the
danger is highest wherever *the preceding statement already committed an irreversible side
effect* and the invariant call is what makes it safe. That is exactly this defect: the order
was irreversible from line 593, and the thing that made it survivable sat behind an argument
list at line 684.

Anything in that argument list is a participant in the invariant: a name that may be
out of scope, an attribute lookup that may be `None`, an f-string that may raise, a default
computed by a call, an unpacked dict. All of them execute *outside* the protection.

Where to look in this codebase — the same shape recurs:
- `order_adapter.place_stop(exchange, symbol, position_side, amount, sl_price, send_tg=send_tg)` — the one that fired
- `order_adapter.cancel_stop(..., send_tg=send_tg, reason=f'...{n_open}...')` (704, 749) — an f-string *and* a bad name in the arg list of the orphan-stop guard
- `breakeven_worker.move_stop_with_race_guard(exchange, send_tg, symbol, ...)` — the other holder of the same invariant, reached through `order_adapter.move_stop`

**The structural remedy, stated but NOT applied:** an invariant that must survive its own
invocation cannot live *inside* the thing that might not be invoked. Either the caller wraps
the irreversible region in `try/except BaseException` and fires the close from there, or the
sequence is restructured so nothing irreversible happens until after the protective call has
returned. A third option — resolving the arguments to locals before the risky region begins —
narrows the window but does not close it, and should not be mistaken for a fix.

## 2. There is no exchange→DB reconciler — the gap that let it persist

`order_adapter.assert_single_owner_at_boot` (line 121) is the boot-time mutual-exclusion
check, and it looks in exactly one direction:

```sql
SELECT id, symbol, position_side, initial_fill_price, opened_at
FROM virtual_positions
WHERE status='open' AND stop_order_id IS NULL
```

That is **DB → exchange**: an open row whose stop is not on the exchange, i.e. a paper-made
position at the moment of going live. Its discriminator is sound and its refusal path
(`_refuse_to_start`, never returns) is correct.

But the incident produced the mirror image: **an exchange position with no DB row.** The
query returns zero rows, the function returns `True`, and the service starts clean. A
restart at any point in those 84 minutes would have sailed straight past a naked live short
and printed a healthy banner.

**Nothing anywhere reconciles exchange → DB.** Every `fetch_positions` caller in the
codebase asks a narrower question:

| caller | question it asks |
|---|---|
| `risk_manager:123` | may I open another one? (cap) |
| `breakeven_worker:186` | is the position behind *this job row* still there? |
| `main:1131`, `main:4083` | what is the size of the position I am about to close? |
| `signal_weights:183` | outcome attribution for a known signal |

Not one of them asks *"is there a position on the exchange that I have no row for?"* — the
only question that would have surfaced this. Both pollers are row-driven
(`virtual_trader._poll_once` over open rows, `breakeven_worker._poll_once` over
`breakeven_jobs`), so a position without a row is not merely unmanaged, it is unobservable.

This is why the failure was silent for 84 minutes and would have survived a restart. It is
also the reason a manual stop would have been the weaker choice: it addresses the missing
protection but not the missing observability.

## 3. Exchange truth beat DB truth — an argument about where caps belong

Two caps guarded the same rule, `MAX_POSITIONS_PER_SIDE = 1`, reading two different sources.
They performed very differently.

**The DB cap** — `virtual_trader.py:693`, inside `execute_entry`:

```sql
SELECT COUNT(*) FROM virtual_positions WHERE symbol=? AND position_side=? AND status='open'
```

It failed twice over. It sits at line 693, *after* the failure at 684, so it was never
reached. And even if it had been reached, it would have counted **zero** — because the row
for entry #1 was never written. Entry #2 was therefore not merely unblocked, it was
*invisible* to the cap that exists to block it.

Note the compounding: the very defect that created the unsafe state also erased the record
the cap depends on. A cap whose source of truth is written by the code path it is guarding
fails **in exactly the scenario it exists for** — correlated failure, not independent.

**The exchange cap** — `risk_manager.concurrent_position_halt` via `check_risk`, calling
`exchange.fetch_positions(...)`. It worked:

```
2026-07-29T20:10:07 RISK HALT: position-cap halt: 1 SHORT already open (cap=1)
```

It saw the real position because it asked the exchange, and it blocked entry #3.

**The argument.** The two caps are not redundant copies of one rule at different layers —
they have different *epistemics*. The DB cap asks "what do I believe I did?"; the exchange
cap asks "what is actually true?". Under normal operation they agree, which is what made the
duplication look harmless. Under the failure they diverged, and only the one reading external
state was right.

For any cap whose violation costs real money, the source of truth should be the venue, not
our own bookkeeping — because our bookkeeping is written by the very path that fails. The DB
cap still has a legitimate job (it is fast, it holds `_entry_lock`, and it backs the
`ux_vpos_one_open_per_side` unique index against races), but it cannot be the *last* line of
defense before an irreversible order. Tonight the ordering was inverted: the weak cap ran
before the order and the strong cap ran on the next signal, five minutes later.

Worth stating plainly: **the `🚧 RISK HALT` alert was not a symptom of the incident, it was
the only gate that worked.** It read exchange truth. Had it also been DB-driven, this report
would be about three or more naked entries.

## 4. `except` blocks print `str(e)` only — no traceback

Both entry handlers swallow the frames:

```python
except Exception as e:
    err = str(e)
    ...
    send_tg(f"⚠️ <b>ORDER ERROR (confluence)</b>\n{err}\n<code>{combo}</code>")
    print(f"ERR (state machine): {err}")      # main.py:3764  (sibling: main.py:2126/2127)
```

So the entire diagnostic yield of a real-money incident was one line with no location:

```
[TITAN] ERR (state machine): name 'send_tg' is not defined
```

No file, no line, no frames. The failing site (`virtual_trader.py:684`) had to be
reconstructed by hand: grep every `send_tg` reference, read `execute_entry`'s signature to
prove the name was absent from that scope, then read the function body top-to-bottom to
establish that line 593 had already sent the order and line 711 had not yet written the row.
That reconstruction — not the exchange queries — was the bulk of the investigation.

A `traceback.format_exc()` in those two blocks would have named the line immediately, and
the "before the order or after?" question, the one that decides whether money is exposed,
would have been answered in seconds rather than derived from log ordering and arithmetic.
This is a diagnostic-latency defect on the live entry path, and it is three lines to fix.

## 5. The alert named the wrong code path

The Telegram alert read **`ORDER ERROR (confluence)`**. The failure was on the
**state-machine** path — the journal line one statement later says `ERR (state machine)`.

`main.py` has two structurally identical entry handlers:

| line | Telegram text | `print` label |
|---|---|---|
| 2126 / 2127 | `ORDER ERROR (confluence)` | `ERR (plain-text 5m)` |
| **3763 / 3764** | **`ORDER ERROR (confluence)`** | `ERR (state machine)` |

The `print` labels were localised; the Telegram label was copy-pasted and never was. So the
operator-facing alert — the one that arrives during an incident, when routing is the first
thing you need — attributed the failure to the wrong caller, while the correct attribution
existed only in the journal.

The cost was concrete: the opening hypothesis was that the confluence path was at fault, and
the state-machine path was only implicated after reading the code. Two alerts that cannot be
told apart also cannot be counted or alarmed on separately.

This is the "hardcoded the first example" class already on record from the platform
consolidation work: a sibling handler cloned with its identifying string intact.

## 6. 🔴 NEW — `market_reduce` passes a parameter BingX rejects in hedge mode

Found by executing the close, not by reading the code.

`order_adapter.market_reduce` (line 497), the **LONG 1/3 partial exit**, sends:

```python
order = exchange.create_market_order(
    symbol, close_side, amt,
    params={'positionSide': position_side, 'reduceOnly': True})
```

That is the exact parameter combination BingX refused for me minutes ago with
`code 109400 — "In the Hedge mode, the 'ReduceOnly' field can not be filled."` The account
is in hedge mode. **In live, the LONG partial exit would raise instead of reducing.**

It has never been exercised: `market_reduce` requires `orders_are_real()`, and live lasted 84
minutes during which the only entries were SHORT. The `reduceOnly` field is also unnecessary
— the exchange derives it from `positionSide`, as this very close proved by reporting
`"reduceOnly": true` on an order that could not carry the field.

Two reasons this belongs in OPEN-ITEMS above its apparent size. First, `market_close` on the
adjacent line delegates to `main._execute_close_position`, which has always passed
`positionSide` alone and is therefore correct — so **the two sibling exit paths disagree
about the venue's contract, and only the one that had live mileage is right.** Second, its
failure mode is the same shape as tonight's: an exit path that raises leaves a real position
in place, and the LONG partial is reached from `_process_position` while a live position is
open.

Same class as items 1 and 5 — an untested live path whose defect is invisible until real
money is on it.

---

## STATE AS OF 21:30 UTC

| | |
|---|---|
| exchange | **FLAT** — 0 positions (all symbols), 0 orders (unified + raw), `used` margin 0.00 |
| USDT balance | **512.6111** |
| incident cost | **−$0.2645** (gross +$0.0276, fees $0.292122) |
| mode | 🧪 **PAPER** — `LIVE_TRADING_ENABLED=False`, `ORDER_ADAPTER_LIVE=False` |
| `titan.service` | active, restarted 21:2x UTC on 11055e2 |
| HEAD | **11055e2**, pushed to `origin/main` |
| `virtual_positions` open | 0 · `breakeven_jobs` 0 |
| **the `NameError`** | **NOT repaired — deliberately.** Awaiting a designed fix |

Nothing else was changed. Items 1–6 are recorded, not fixed. The repair touches
`virtual_trader.execute_entry`'s signature and its three `send_tg` sites (684, 704, 749),
plus `main.py`'s callers, and item 1 argues the correct fix is not merely to pass the
parameter — so it should be designed rather than patched.
