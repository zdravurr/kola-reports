# titan-live-naked-short-nameerror

_2026-07-29 21:20 UTC_

---

# TITAN LIVE — NAKED SHORT: ONE NameError PUT $292 ON THE EXCHANGE WITH NO STOP AND NO ROW

**2026-07-29 21:17 UTC · HEAD cb3a8bb · READ-ONLY investigation, nothing placed / cancelled / changed**

**VERDICT:** A real SHORT is open on BingX with **no protective stop of any kind** and
**no `virtual_positions` row**. It is invisible to every automated manager the bot has.
Two entry orders were sent — the intended notional was $150, the actual is **$292**.
The single root cause is a `NameError` on `send_tg` in `virtual_trader.execute_entry`,
raised **after the fill and before the stop**. Awaiting operator decision: place the stop
or close the position.

---

## 1. IS THERE A POSITION? — YES, REAL

`exchange.fetch_positions(['BTC/USDT:USDT'])` → 1 position:

| field | value |
|---|---|
| symbol | BTC/USDT:USDT |
| side | **short** |
| contracts | **0.0046 BTC** |
| notional | **$291.69** |
| entryPrice | **63507.9** |
| markPrice | 63411.1 |
| unrealizedPnl | **+$0.4455** |
| leverage | 5.0 |
| marginMode | **cross** |
| initialMargin | $58.4273 |
| liquidationPrice | null (cross) |

Balance USDT: free 454.3022 · used 58.4272 · **total 512.7294**

Verified twice, ~12 minutes apart (21:05 and 21:17 UTC). Still open both times.

**The notional is double the configured size.** Config logged
`[VIRTUAL FIXED-NOTIONAL] margin=$30 × 5x = $150 notional` — twice. 0.0046 = 2 × 0.0023.

## 2. IS IT PROTECTED? — NO. ZERO ORDERS OF ANY KIND

Four independent probes, all agreeing:

```
fetch_open_orders('BTC/USDT:USDT')                  -> count: 0
fetch_open_orders(..., params={'stop': True})       -> 0
fetch_open_orders(..., params={'trigger': True})    -> 0
fetch_open_orders(..., params={'type': 'trigger'})  -> 0
raw swapV2PrivateGetTradeOpenOrders {'symbol':'BTC-USDT'}
    -> {"code":"0","msg":"","data":{"orders":[]}}
raw swapV2PrivateGetTradeOpenOrders {}   (all symbols)
    -> {"code":"0","msg":"","data":{"orders":[]}}
```

The raw endpoint was checked specifically because BingX conditional orders do not always
surface through the ccxt unified call. They are not hiding there either.

**NO STOP. NO TAKE-PROFIT. NO TRIGGER ORDER. The position is naked and has been since
20:05:13 UTC.**

## 3. virtual_positions — NO OPEN ROW EXISTS

```sql
SELECT ... FROM virtual_positions WHERE status='open';
-- (zero rows)
```

Last rows:

| id | side | size | entry | sl_price | stop_order_id | status | closed_at | reason |
|---|---|---|---|---|---|---|---|---|
| 85 | LONG | 0.1547 | 64604.4 | 63787.5 | *(null)* | closed | 2026-07-29T16:42:36Z | sl |
| 84 | LONG | 0.1562 | 63997.3 | 63129.9 | *(null)* | closed | 2026-07-29T13:30:08Z | external |
| 83 | SHORT | 0.1576 | 63449.7 | 64286.4 | *(null)* | closed | 2026-07-29T06:28:00Z | sl |

The question "is `stop_order_id` NULL?" has no answer, because **the row was never
written.** The last row (id=85) closed at 16:42 UTC — 3.5 hours *before* the live flip,
and it is a paper row at the paper size (0.1547 BTC).

`breakeven_jobs` is likewise **empty** — zero rows. The breakeven/trail worker polls
`SELECT * FROM breakeven_jobs`, so it has literally nothing to look at.

## 4. DO THEY MATCH? — NO. TOTAL DIVERGENCE

| | exchange | DB row |
|---|---|---|
| exists | **YES** | **NO** |
| side | short | — |
| size | 0.0046 | — |
| entry | 63507.9 | — |
| stop | **none** | — |

There is nothing to reconcile. The exchange holds a position the bot does not know exists.
`stop_order_id` cannot correspond to a live order because neither the id nor the order nor
the row exists.

Consequence — and this is the part that matters more than the missing stop:
**no row means no manager.** `virtual_trader._poll_once` iterates open rows;
`breakeven_worker._poll_once` iterates `breakeven_jobs`. Both find nothing. The SL check,
the trail, the breakeven arm, the post-entry recheck and the passive-fill reconciliation
are all row-driven. Not one of them will ever look at this position.

---

## 5. WHERE send_tg BLEW UP — AFTER THE ORDER, BEFORE THE STOP

### The broken scope

`send_tg` **is** defined, at `main.py:538`. The failure is one of scope, not a missing
definition.

`virtual_trader.py` has **no module-level `send_tg`** — no definition, no import. Every
function in that module that needs it takes it as a **parameter**, threaded from
`gunicorn.conf.py:120` → `virtual_trader.start_worker(main.exchange, main.send_tg)`.

`execute_entry` is the exception. Its signature (`virtual_trader.py:496`):

```python
def execute_entry(exchange, symbol, side, position_side,
                  trades_entry_row_id=None, pre_trade_walls=None,
                  entry_adx_1h=None, entry_atr_pct_1h=None):
```

No `send_tg`. It is not a worker-loop function — it is called synchronously off the
webhook request path, so it never received the reference the poller gets. Yet its body
references `send_tg` in **three** places:

| line | call | reached? |
|---|---|---|
| `virtual_trader.py:684` | `order_adapter.place_stop(..., send_tg=send_tg)` | **YES — this is the one that fired** |
| `virtual_trader.py:704` | `order_adapter.cancel_stop(..., send_tg=send_tg)` — orphan cancel, capacity branch | latent |
| `virtual_trader.py:749` | `order_adapter.cancel_stop(..., send_tg=send_tg)` — orphan cancel, unique-index branch | latent |

All three are `NameError`. Lines 704/749 are unreachable today only because they sit
*after* line 684 — the moment 684 is fixed carelessly, they fire next.

### The exact position in the sequence

`execute_entry` body order:

```
line 593   _entry_fill = order_adapter.market_entry(...)   <-- REAL MARKET ORDER SENT
line 600   fill_price = _entry_fill['fill_price']
line 601   amount     = _entry_fill['amount']   # EXECUTED size
line 608   sl_price   = computed
line 618   print SL_DRYRUN                                 <-- logged, so we got here
line 683   with _entry_lock:
line 684       order_adapter.place_stop(..., send_tg=send_tg)   <-- NameError
line 692   ...  if _stop is None: return None
line 711   INSERT INTO virtual_positions (...)              <-- NEVER REACHED
```

**ANSWER: after the order, before the stop.** The market order was sent and filled at
line 593. The `NameError` fired 91 lines later at line 684. The `INSERT` at line 711 never
ran. That is precisely the one window in the whole function where a failure leaves real
money exposed — and it explains all three symptoms at once: real position, no stop, no row.

### 🔴 The invariant did not fail — it was never entered

This is the most important structural finding in the report.

`order_adapter.place_stop` carries the item-11 invariant, documented in its own docstring
as *"the one requirement of item 11 that may not be traded away"*: if the stop cannot be
placed after retries, fire `_bw._emergency_close(...)` and close the position at market
immediately.

**That invariant never ran.** Python evaluates keyword arguments *before* entering the
callee, so `send_tg=send_tg` raised at the **call site**. `place_stop` was never entered.
Its retry loop, its failure branch and its emergency close were all bypassed — not
attempted and failed, but never reached.

The journal proves it: there is **no `[ADAPTER] LIVE STOP` line** and **no `[BE-FAILSAFE]`
line** anywhere after the flip.

The invariant is sound. It is guarding the inside of a door that the failure opened around.

### Which caller, and a labelling bug

The journal says `ERR (state machine)` — `main.py:3764`. So the entry came through the
state-machine path, not the 5m confluence path. But the Telegram text one line above, at
`main.py:3763`, reads:

```python
send_tg(f"⚠️ <b>ORDER ERROR (confluence)</b>\n{err}\n<code>{combo}</code>")
```

The `(confluence)` label is copy-pasted from the sibling handler at `main.py:2126`. **The
Telegram alert named the wrong code path** — a real diagnostic hazard, cheap to fix.

Note also that the `send_tg` at the *catch* site works fine — module scope, `main.py`.
That is why the error reached Telegram at all.

## 6. DID IT BREAK OUR ALARMS? — TWO ARE INTACT, ONE SHARES THE DEAD SCOPE, AND ALL THREE ARE BLIND TO *THIS* POSITION

Answering the structural question and the practical one separately, because they differ.

| alarm | site | wiring | fires for this position? |
|---|---|---|---|
| Emergency close | `breakeven_worker._emergency_close` (283) | **intact** — `send_tg` is a positional param, threaded from `start_worker(main.exchange, main.send_tg)` via `gunicorn.conf.py:126` | **no** — never entered (see §5) |
| Orphan-stop cancel | `order_adapter.cancel_stop` (582) | callee intact, but **both callers** (`virtual_trader.py:704`, `:749`) are in the dead scope → `NameError` | **no** — unreachable past line 684 |
| Passive-fill "POSITION GONE" | `virtual_trader._reconcile_passive_fill` (876-878) | **intact** — param threaded `start_worker` → `_poll_once` → `_process_position` → `_reconcile_passive_fill` | **no** — it is row-driven; there is no row |

So the answer is **not** "all three hands-required alarms are broken." Two of the three are
correctly wired and would have delivered their Telegram message if reached.

**But the practical outcome is the one you feared, by a different mechanism.** All three
are silent right now:

- the emergency close was bypassed at the call site,
- the orphan cancel is behind it,
- and the passive-fill alert only ever examines rows in `virtual_positions`.

Additionally, both `_emergency_close` and `cancel_stop` guard their sends with
`if send_tg:` and `try/except Exception: pass`, and always `print()` first. So even a
`send_tg=None` would degrade to "acts correctly, stays quiet in Telegram" — it would not
skip the close. The danger in this incident was never a swallowed message; it was the
call-site raise that skipped the *action*.

### The gap that lets this persist

`order_adapter.assert_single_owner_at_boot` (121) is the boot reconciler, and it checks the
**opposite** direction: rows with `status='open' AND stop_order_id IS NULL` — a DB row with
no exchange stop. Here there is an **exchange position with no DB row**. The query returns
zero rows, `assert_single_owner_at_boot` returns `True`, and a restart would sail straight
past this naked short. There is no exchange→DB reconciler anywhere in the codebase.

## 7. JOURNALCTL SINCE THE FLIP — VERBATIM

Live flip confirmed in the boot block: `[TITAN][ORDER-MODE] ORDER_ADAPTER_LIVE = True`.
The entries did **not** happen at 19:14 — they happened at **20:05**, on the first
state-machine SHORT after the flip. 154 lines total in the window; every ADAPTER /
FAILSAFE / ORPHAN / VPOS-FILL / traceback line follows.

```
2026-07-29T20:05:11+00:00 titan[4173057]: [TITAN] [VIRTUAL FIXED-NOTIONAL] BTC/USDT:USDT SHORT: margin=$30 × 5x = $150 notional; derived risk $2.52
2026-07-29T20:05:13+00:00 titan[4173057]: [TITAN] [ADAPTER] LIVE ENTRY BTC/USDT:USDT SHORT 0.0023 @ 63503.2 fee=0.073029
2026-07-29T20:05:13+00:00 titan[4173057]: [TITAN] [VIRTUAL] SL_DRYRUN 1h=64601.01 (1.73%) | 5m=63967.99 (0.73%) | margin_1h=$23 cap=no | active=1h
2026-07-29T20:05:13+00:00 titan[4173057]: [TITAN] [VIRTUAL FIXED-NOTIONAL] BTC/USDT:USDT SHORT: margin=$30 × 5x = $150 notional; derived risk $2.52
2026-07-29T20:05:13+00:00 titan[4173057]: [TITAN] ERR (state machine): name 'send_tg' is not defined
2026-07-29T20:05:13+00:00 titan[4173057]: 127.0.0.1 - - [29/Jul/2026:20:05:13 +0000] "POST /webhook?key=REDACTED&tf=5m HTTP/1.0" 500 144 "-" "TradingView Webhook"
2026-07-29T20:05:14+00:00 titan[4173057]: [TITAN] [ADAPTER] LIVE ENTRY BTC/USDT:USDT SHORT 0.0023 @ 63512.6 fee=0.073039
2026-07-29T20:05:14+00:00 titan[4173057]: [TITAN] [VIRTUAL] SL_DRYRUN 1h=64610.41 (1.73%) | 5m=63977.39 (0.73%) | margin_1h=$23 cap=no | active=1h
2026-07-29T20:05:15+00:00 titan[4173057]: [TITAN] ERR (state machine): name 'send_tg' is not defined
2026-07-29T20:05:15+00:00 titan[4173057]: 127.0.0.1 - - [29/Jul/2026:20:05:15 +0000] "POST /webhook?key=REDACTED&tf=5m HTTP/1.0" 500 146 "-" "TradingView Webhook"
2026-07-29T20:10:07+00:00 titan[4173057]: [TITAN] RISK HALT: position-cap halt: 1 SHORT already open (cap=1)
2026-07-29T20:10:07+00:00 titan[4173057]: 127.0.0.1 - - [29/Jul/2026:20:10:07 +0000] "POST /webhook?key=REDACTED&tf=5m HTTP/1.0" 200 170 "-" "TradingView Webhook"
```

**No traceback was emitted.** Both handlers catch `Exception as e` and print only
`str(e)` — hence the bare `name 'send_tg' is not defined` with no frames. The stack had to
be reconstructed by reading the code. Worth fixing: `traceback.format_exc()` in those
`except` blocks would have named `virtual_trader.py:684` instantly.

**No `[ADAPTER] LIVE STOP`, no `[BE-FAILSAFE]`, no `[ADAPTER] orphan stop`, no
`VPOS-FILL` line exists in the window** — consistent with §5 and §6.

### Reading the sequence

1. **20:05:13** — entry #1, 0.0023 @ 63503.2, fee 0.073029. `SL_DRYRUN` prints → past the
   fill. `NameError` → HTTP 500. No stop, no row.
2. **20:05:14** — entry #2, 0.0023 @ 63512.6, fee 0.073039. Identical path, identical
   failure, one second later.
3. **20:10:07** — third attempt **blocked** by `risk_manager.concurrent_position_halt`.

**Arithmetic check:** (63503.2 + 63512.6) / 2 = **63507.90** — exactly the exchange's
reported `entryPrice`. 0.0023 + 0.0023 = **0.0046** — exactly the reported size. Total
entry fees $0.146068. The two log lines and the exchange agree to the cent; there is no
third hidden fill.

### Why the second entry was not blocked, and what saved us from a third

Two different caps, reading two different sources:

- **The in-function cap** (`virtual_trader.py:693`) counts **DB rows**:
  `SELECT COUNT(*) FROM virtual_positions WHERE status='open'`. It sits *after* line 684,
  and no row was ever written — so it was neither reached nor able to see entry #1.
  It could not stop entry #2.
- **The risk gate** (`risk_manager.concurrent_position_halt`, via `check_risk`) calls
  `exchange.fetch_positions(...)` — **exchange truth**. By 20:10 the exchange showed a real
  SHORT, so it fired: `position-cap halt: 1 SHORT already open (cap=1)`.

**The RISK HALT in your Telegram is not a symptom — it is the one gate that worked.**
It read the exchange instead of the database and stopped entry #3. Without it this would be
three or more naked entries. It also means the bot will keep refusing new SHORTs while this
position lives, so there is no runaway risk from further webhooks — but LONG is a separate
side and is not capped by this position.

---

## OPEN DECISION — OPERATOR ONLY

The position is naked. Per instruction nothing was placed, cancelled or closed; this
investigation was read-only throughout.

Had the code worked, the stop for a 63507.9 SHORT entry would have been the 1h-ATR stop the
dry-run logged: **~64601–64610 (≈1.73% above entry, ≈$5.0 risk on 0.0046 BTC)**. The 5m
alternative was ~63968–63977 (0.73%). `SL_ATR_TF` is `1h`, so 1h is the live number.

Two coupled facts to weigh:

1. **The position is 2× the intended size** ($292 vs $150), so any risk figure computed for
   $150 understates it by half.
2. **Even with a stop attached manually, nothing manages the position** — no DB row means
   no breakeven, no trail, no post-entry recheck, no passive-fill reconciliation, and no
   close-report. A manual stop makes it survivable, not managed.

Also worth deciding: **the bot is still live.** `LIVE_TRADING_ENABLED` and
`ORDER_ADAPTER_LIVE` are both `True`, and the defect is in the shared entry path. A LONG
signal would take the same route through `virtual_trader.execute_entry:684` and produce a
second naked position — the SHORT cap does not protect the LONG side.

### The fix, when authorised (NOT applied)

Root cause is one missing parameter. `execute_entry` must receive `send_tg` the way every
other function in `virtual_trader.py` does, and `main.py`'s callers must pass it — covering
all three sites (684, 704, 749) at once. Two hardening items belong in the same change:
`traceback.format_exc()` in the two `except` blocks, and correcting the `(confluence)`
label at `main.py:3763`. Awaiting your word before touching anything.
