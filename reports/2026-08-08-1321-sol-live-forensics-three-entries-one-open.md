# sol-live-forensics-three-entries-one-open

_2026-08-08 13:21 UTC_

---

# Mercury-SOL — LIVE forensics, 2026-08-08 (read-only, nothing changed, no restart)

**THE ANSWER TO THE HEADLINE QUESTION: THERE WERE THREE ENTRY EVENTS, NOT TWO — AND FIVE MARKET
ORDERS. The alerts you are holding come from different events. Nothing contradicts itself once
they are separated. One position — the third — is still open and has no manager.**

Everything below is read from the venue (Bybit v5), the journal and `trades.db`. No write call was
made: no order, no stop, no cancel, no close, no restart. The service is the same pid 3282921 that
has been running since 04:28:37.

---

## 1. FROM THE VENUE (read at ~13:11 UTC)

`GET /v5/position/list category=linear symbol=SOLUSDT` → `retCode 0`

**positionIdx 1 (LONG / Buy) — OPEN:**

| field | value |
|---|---|
| size | **1.3 SOL** |
| avgPrice (entry) | **74.80** |
| markPrice | **75.44** |
| unrealisedPnl | **+0.832 USDT** |
| **stopLoss** | **73.89** ← on the position, live |
| positionValue | 98.072 |
| leverage | 5 |
| positionIM | 19.692192 |
| breakEvenPrice | 74.94974974 |
| curRealisedPnl | -0.09724 (entry fee only) |
| tradeMode | **0 = CROSS** |
| openTime | 1786179014459 = **08:50:14.459 UTC** |
| positionStatus | Normal |
| liqPrice | "" (empty — cross) |

**positionIdx 2 (SHORT / Sell): size 0.** Empty. Nothing there.

**Open / conditional orders** — `GET /v5/order/realtime openOnly=0` → exactly ONE object:

- orderId `671eee37-…`, stopOrderType **StopLoss**, createType `CreateByStopLoss`,
  orderStatus **Untriggered**, triggerPrice **73.89**, triggerBy **MarkPrice**,
  triggerDirection 2 (falling), qty **1.3**, reduceOnly **true**, closeOnTrigger **true**,
  positionIdx 1, tpslMode Full, createdTime 1786179014843 = **08:50:14.843 UTC**.

There is exactly one stop, it is the right size, it is on the right index, and it is armed.
No orphan conditional orders, no second stop, nothing on the SHORT index.

**Wallet vs 811.90195236 — it reconciles exactly.**

- USDT `walletBalance` = **810.96162336** (settled)
- USDT `equity` = **811.75462336** (= walletBalance + uPnL 0.793 at mark 75.44)
- USDT `cumRealisedPnl` = -1350.35750228 (lifetime, all history)
- Account: totalEquity 1307.51, totalAvailableBalance 1250.34, totalInitialMargin 19.67
  (other coins present: USDC 246.48, ENA 2747.17 ≈ $249.73, dust)

Your figure **811.90195236 = 810.96162336 + 0.94032900**, and 0.94032900 / 1.3 = 0.7233, i.e.
mark = 74.80 + 0.7233 = **75.5232**. So 811.90195236 is USDT **equity** read at a moment when the
mark was ~75.52. Same wallet, different mark. It is not a discrepancy and nothing is missing.

---

## 2. THE ALERTS RECONCILED — THREE EVENTS, NOT ONE

The four alert texts you have are **not four claims about one stop**. They are claims about
**three different entry events**, two of which are dead and one of which is live. Venue execution
list (`/v5/execution/list`), to the millisecond:

| # | time UTC | side | qty | price | orderId | what it was |
|---|---|---|---|---|---|---|
| 1 | 06:50:20.408 | Buy | 0.3 + 1.0 | 74.79 | `bcf63671` | event A, thread 1 |
| 2 | 06:50:21.466 | Buy | 1.3 | 74.80 | `af20a53c` | **event A, thread 2 — the duplicate** |
| 3 | 06:50:25.350 | Sell | **2.6** | 74.78 | `e7ec215a` | emergency close, flattened BOTH |
| 4 | 08:35:16.460 | Buy | 1.3 | 74.85 | `6e489d1f` | event B, thread 1 |
| 5 | 08:35:16.749 | Buy | 1.3 | 74.85 | `45efd112` | **event B, thread 2 — the duplicate** |
| 6 | 08:35:20.336 | Sell | **2.6** | 74.84 | `1ed83d66` | emergency close, flattened BOTH |
| 7 | 08:50:14.456 | Buy | 1.3 | 74.80 | `12ed23b7` | **event C — STILL OPEN** |

`closedPnl`: 06:50:25 → **-0.427895** (qty 2.6, entry 74.795, exit 74.78);
08:35:20 → **-0.415194** (qty 2.6, entry 74.85, exit 74.84). Both closed sizes are **2.6 = 2 × 1.3**.
That is the proof that two orders were placed in each of events A and B.

### Event A — 06:50, DEAD (flat)

```
06:50:01     two 5m webhooks land in the same second: "Bullish I-CHOCH" and "Bullish OB Created"
06:50:02     both pass HTF; rows 16748 and 16749 both written
06:50:15     [STATE-CACHE] HIT/inflight — reusing the verdict ... LONG decide='execute'
06:50:18     [QTY] entry.live ... 1.3        ← printed TWICE
06:50:20.408 thread 1 market order fills 1.3 @ 74.79
06:50:21     [SL] position-level SL set on attempt 1: 73.81            ← thread 1, SUCCEEDS
06:50:21     [SL] PROVISIONAL stop set ... 74.79 → 73.81 ... position is protected   ← ALERT #1
06:50:21     [ENTRY] fill read FAILED ... NOT booking a fabricated position
06:50:21     ERR: entry fill unreadable ... (position IS stopped at 73.81)
06:50:21.466 thread 2 market order fills 1.3 @ 74.80  → venue position is now 2.6
06:50:22     [STOP-MOVE] entry-sl FAILED LONG -> 73.81: retCode 34040 "not modified"  ← thread 2
06:50:22     [SL] attempt 1/3 failed
06:50:22     [STOP-MOVE] entry-sl FAILED ... 34040        [SL] attempt 2/3 failed
06:50:24     [STOP-MOVE] entry-sl FAILED ... 34040        [SL] attempt 3/3 failed
06:50:24     [SL] all 3 attempts failed                                  ← ALERT #2
06:50:24     [SL-FAIL-SAFE] SL failed 3× (attempted 73.81) — emergency market close of LONG
06:50:26     [CLOSE] order carried no fill price — using ticker 74.78 as a LABELLED estimate ← ALERT #3
06:50:27     [STOP-CLEANUP] StopOrders cleared for SOLUSDT
06:50:27     [SL-FAIL-SAFE] recorded status=sl_failed_position_closed naked=False row=16748
```

### Event B — 08:35, DEAD (flat). Identical shape.

Webhooks "Bullish OB Created" + "Bullish I-BOS" at 08:35:01, rows 16765/16766, `[QTY]` twice,
two fills 0.289 s apart, SL 73.94 set on attempt 1 by thread 1, thread 2 gets 34040 ×3,
emergency close of 2.6 @ 74.84 at 08:35:20. **This event produced its own copy of all the same
alerts — with 73.94, not 73.81. It is the one you were not shown.**

### Event C — 08:50, **LIVE**

```
08:50:00     ONE 5m webhook: "Bullish OB Entered". One thread. Row 16767.
08:50:13     [QTY] entry.live ... 1.3        ← printed ONCE
08:50:14.456 market order fills 1.3 @ 74.80
08:50:15     [SL] position-level SL set on attempt 1: 73.89             ← SUCCEEDS
08:50:15     [SL] PROVISIONAL stop set ... 74.8 → 73.89 ... position is protected
08:50:15     [ENTRY] fill read FAILED ... NOT booking a fabricated position
08:50:15     ERR: entry fill unreadable ... (position IS stopped at 73.89)   ← ALERT #4
             — NO SL failure. NO emergency close. Nothing after this.
```

### So, mapped to your four alert texts

| your alert | belongs to | true? |
|---|---|---|
| "stop is on the exchange at **73.81**, it IS protected" | **event A**, 06:50:21 | true then; that position is now flat |
| "SL FAILED 3× — emergency close" | **event A**, 06:50:24 (and again in event B) | true — it was the DUPLICATE thread's stop that "failed" |
| "position CLOSED at **74.78**" | **event A**, 06:50:26 | true — closed 2.6, both threads' exposure |
| "position IS stopped at **73.89**" | **event C**, 08:50:15 | **true right now** — this is the live one |

**Nothing contradicts anything.** "CLOSED at 74.78" and "a position is open" are both true because
they are about different positions, 2 hours apart. The three stop prices are three different stops
on three different entries: 73.81 (gone), 73.94 (gone), 73.89 (live).

---

## 3. WHY THE FILL COULD NOT BE READ — not Tor, not an empty field, not a format surprise

The venue was **never asked**. The exception is raised by ccxt **client-side, before any HTTP
request for the order**.

`_read_entry_fill` (`main.py:1936`) takes `filled`/`average` off the order dict returned by
`create_market_order`. Bybit's v5 `POST /v5/order/create` returns only `orderId` and `orderLinkId` —
no fill data — so both are `None` and the code falls to its one re-read:

```python
fetched = tor_retry.with_socks_retry(exchange, lambda ex: ex.fetch_order(oid, symbol),
                                     label='fetch_order.entryfill')
```

ccxt 4.5.52, `ccxt/bybit.py::fetch_order`:

```python
acknowledge, params = self.handle_option_and_params(params, 'fetchOrder', 'acknowledged')
if not acknowledge:
    raise ArgumentsRequired(self.id + ' fetchOrder() can only access an order if it is in
        last 500 orders(of any status) for your account. Set params["acknowledged"] = True
        to hide self warning. Alternatively, we suggest to use fetchOpenOrder or fetchClosedOrder')
```

That `raise` sits **above** the request build, on the Unified-account branch. This account is
Unified (`accountType: UNIFIED`). So:

- **Exchange response: none.** No request for the order was ever sent.
- **retCode: none.** There is no Bybit retCode here — the error is `ccxt.base.errors.ArgumentsRequired`.
- **What `_read_entry_fill` saw:** `filled=None, average=None` on the create response, then an
  exception from the re-read, then it returned `(None, None)` and refused to book.
- **Tor: not involved.** `tor_retry` only retries on 403/CloudFront; it never got that far.
- **Format the parser did not expect: no.** The parser was correct and the venue was cooperative.

The retry wrapper is a red herring, and so is the network. **It failed 3 times out of 3 today, at
06:50, 08:35 and 08:50, with a byte-identical message.** On a Unified account this call cannot
succeed as written, so every live entry reaches the "refuse to book" branch. The refusal is the
mechanism working as designed — it is the read in front of it that is broken.

---

## 4. WHY THE SL "FAILED 3×" ON ONE PATH AND SUCCEEDED ON ANOTHER

**It is the same function, on the same position, one second apart — and the second call failed
*because the first one succeeded*.**

Both paths are `_place_sl_with_retry` → `_move_stop_to` (`main.py:1791`), which does:

```python
resp = ex.private_post_v5_position_trading_stop({
    'category': 'linear', 'symbol': 'SOLUSDT', 'positionIdx': '1',
    'stopLoss': str(px), 'slTriggerBy': 'MarkPrice'})
```

- **Thread 1** sets `stopLoss=73.81` on positionIdx 1 → `retCode 0` → `[SL] position-level SL set on attempt 1: 73.81`.
- **Thread 2**, ~1 s later, sets **the identical value on the identical position** (Bybit netted
  both orders into ONE position at positionIdx 1) → the state is already what is being asked for →

```json
{"retCode":34040,"retMsg":"not modified","result":{},"retExtInfo":{},"time":1786171821803}
```

ccxt raises on that, `_move_stop_to` catches it in a bare `except Exception` and returns `False`.
`_place_sl_with_retry` retries the same no-op twice more (0.5 s, 1.0 s backoff) and gets 34040 each
time — 3 identical responses at 06:50:22.690 and 06:50:24.118 — then returns `None`, which triggers
`_sl_failsafe` → emergency market close.

**34040 "not modified" means the stop is ALREADY AT THAT PRICE.** It is the success answer to an
idempotent set, and it is being counted as a failure. The irony is in `_move_stop_to`'s own
docstring, which argues that `/v5/position/trading-stop` "SETS a value rather than appending an
order, so it is idempotent by construction" — and the code then treats the venue's idempotent-repeat
response as an error.

Event B is the same, verbatim, with 73.94 at 08:35:17.087 / 08:35:17.953 / 08:35:19.278.

Event C succeeded and never entered the fail-safe **for one reason only: one webhook, one thread, so
there was no second identical set and no 34040.**

**The upstream cause of the duplicate thread.** `gunicorn_mercury.conf.py` runs
`workers = 1, threads = 4, worker_class = 'gthread'`. In events A and B, two TradingView 5m webhooks
arrived in the same second, both LONG-directional, both passed HTF; the advisor's state cache
correctly deduped the *model call* — `[STATE-CACHE] HIT/inflight — reusing the verdict ... no model
call` — but not the *execution*, so both threads carried `decide='execute'` forward. Both then ran
`_risk_check`, both read `fetch_positions` **before either order had landed**, both saw 0 open, both
passed the `MAX_POSITIONS_PER_SIDE = 1` cap, and both placed a market order. The `[QTY] entry.live`
line printing twice is that race in the log. The DB-layer guard that exists for exactly this
(`ux_vpos_one_open_per_side`, `main.py:571`) never fired, because the INSERT it protects is
downstream of the fill read that refuses first.

**Net effect of the fail-safe:** it worked. Both duplicate positions were flattened within 4-5
seconds for -0.427895 and -0.415194. It was fired by a false alarm, but it left the book flat.

---

## 5. IS THERE AN `is_paper=0` ROW? — NO. NOT ONE, EVER.

```sql
SELECT ... FROM virtual_positions WHERE is_paper = 0;   -- 0 rows
SELECT ... FROM virtual_positions WHERE status = 'open'; -- 0 rows
```

Both empty. The newest row in the table is **id 28**, a **paper** SHORT (`is_paper=1`) closed
2026-08-07T06:00:10Z. `active_positions` is **empty**. So, plainly:

**The venue LONG has NO ledger row and therefore NO manager.** Confirmed against the code comment at
`main.py:2360` — nothing adopts it on restart either: `_reconcile_open_virtual_positions` reads the
DB only and never INSERTs, and `_reconcile_active_positions` returns early on an empty
`active_positions`. It gets no breakeven move, no partial, no trail recompute, no timeout, no
close. **The only thing standing between that position and the account is the 73.89 stop.**

What *was* recorded, correctly:

`naked_position_alerts` — 3 rows, all `resolved=0`:

| id | ts (UTC) | stage | detail |
|---|---|---|---|
| 1 | 06:50:21.070 | entry_fill_unreadable | provisional_sl=73.81 order_id=`bcf63671` |
| 2 | 08:35:17.105 | entry_fill_unreadable | provisional_sl=73.94 order_id=`6e489d1f` |
| 3 | 08:50:15.086 | entry_fill_unreadable | provisional_sl=73.89 order_id=`12ed23b7` |

`trades` — one row per event, plus the fail-safe rows:

| id | ts | status |
|---|---|---|
| 16748 | 06:50:02 | `sl_failed_position_closed` |
| 16749 | 06:50:02 | `failed` (entry fill unreadable) |
| 16765 | 08:35:01 | `failed` (entry fill unreadable) |
| 16766 | 08:35:01 | `sl_failed_position_closed` |
| **16767** | **08:50:00** | **`failed` (entry fill unreadable) ← the live position's only trace** |

Note what each alert order_id proves: the naked alert in events A and B was raised by the thread
that placed the **first** order; the **second** thread is the one that hit 34040 and ran the close.

---

## 6. WHAT THE LONG SIDE LOOKS LIKE TO THE ENTRY GATE RIGHT NOW

**BLOCKED.** I replayed the gate's own arithmetic read-only against the live venue:

```
side=long  contracts=1.3  entry=74.8  mark=75.42  uPnL=0.806  SL=73.89  idx=1
side=short contracts=0.0                                                idx=2

GATE open_count[LONG]  = 1  -> MAX_POSITIONS_PER_SIDE=1 -> BLOCKED: max 1 LONG position(s) already open
GATE open_count[SHORT] = 0  -> MAX_POSITIONS_PER_SIDE=1 -> passes
```

Blocked by **Gate 4** in `_risk_check` (`main.py:1580-1590`), the per-side position cap, with
`MAX_POSITIONS_PER_SIDE = 1` (`config.py:771`). It has already fired four times today —
`trades` rows 16769, 16770 (09:30:02, 09:30:03) and 16775, 16776 (10:50:01, 10:50:02), all
`status='risk_halt'`, all `error='max 1 LONG position(s) already open'`.

The earlier gates are not what is stopping it: no macro halt, no DXY halt, no daily-loss breaker,
no loss-streak halt fired. **SHORT is not blocked** — `open_count[SHORT] = 0`, that side is open for
business, and a SHORT entry would take the same unreadable-fill path.

---

## 7. THE "RISK HALT" CARD — YOUR PREMISE IS THE ONE THING THAT IS WRONG

You wrote: *"That gate counts ROWS in virtual_positions, not venue positions. So a row EXISTS."*

**It does not count rows. It counts venue positions.** `main.py:1580`:

```python
positions = tor_retry.with_socks_retry(exchange, lambda ex: ex.fetch_positions([symbol]),
                                       label='positions.riskcheck')
open_count = sum(1 for p in positions
                 if (p.get('side') or '').upper() == position_side
                 and float(p.get('contracts') or 0) > 0)
if open_count >= MAX_POSITIONS_PER_SIDE:
    return False, f"max {MAX_POSITIONS_PER_SIDE} {position_side} position(s) already open"
```

That is a live `fetch_positions` call to Bybit. No DB query, no `virtual_positions`. So:

**a) Is there an OPEN row? NO — zero open rows, zero `is_paper=0` rows, ever.** There is nothing to
compare against the venue. The RISK HALT card and the ENTRY FILL UNREADABLE alert **do not
contradict each other**: the alert says "no row was booked" (true), the card says "the venue has a
LONG" (also true). Both describe the same thing from two different books. The card is the *venue*
speaking, not the ledger.

**b) N/A — no row exists, so the engine cannot be ticking it.** For completeness, it is not:
`active_positions` is empty, the paper engine's heartbeat has printed `open=0` continuously all day
(`open=0 mode=LIVE pid=3282921`, latest 13:07:10), and breakeven/partial are properties of a
`virtual_positions` row's `mgmt_state_json`, which does not exist. Nothing is armed. Nothing is
being evaluated.

**c) N/A — and this is the good news in an otherwise bad picture.** No dead row is blocking the
side. The block is *correct and load-bearing*: it is the live venue position blocking further LONGs,
which is precisely what stops a fourth unmanaged entry from stacking on top of an unmanaged third.
The block is the only reason events at 09:30 and 10:50 did not become entries 4, 5, 6 and 7.

**d) HOW MANY ENTRY ATTEMPTS, AND WHAT HAPPENED TO EACH — plainly:**

**Three entry events. Five market orders. Two emergency closes. One position still open.**

1. **06:50 — event A. TWO orders** (1.3 @ 74.79 + 1.3 @ 74.80 = 2.6), from two racing webhook
   threads. SL 73.81 set successfully by thread 1. Thread 2's identical set returned 34040 "not
   modified", was misread as 3 failures, and fired the emergency close. **Closed 2.6 @ 74.78.
   Realised -0.427895. Flat.**
2. **08:35 — event B. TWO orders** (1.3 + 1.3 @ 74.85 = 2.6), same race, same 34040, same fail-safe.
   **Closed 2.6 @ 74.84. Realised -0.415194. Flat.**
3. **08:50 — event C. ONE order** (1.3 @ 74.80). No race, so no 34040, so no emergency close. The
   fill read failed as it did in A and B, so the bot refused to book it. **STILL OPEN: 1.3 SOL
   LONG @ 74.80, stop 73.89 live on the venue, uPnL +0.83, no DB row, no manager.**
4. **09:30 (×2) and 10:50 (×2) — four further LONG signals, all REFUSED** by the position cap
   reading the live venue. Correct behaviour.

Realised cost of the two false-alarm closes: **-0.843089 USDT** plus the entry/exit fees already
inside those figures. The account is not at risk from what happened; it is exposed by what is
*still open and unmanaged*.

---

## STATE AS OF THIS READING

- Venue: **1.3 SOL LONG @ 74.80, stop 73.89 armed on the position and as an Untriggered
  reduce-only conditional, mark 75.44, uPnL +0.832.** Cross margin.
- Book: **nothing.** No row, no manager, no breakeven, no partial, no trail, no timeout.
- Gate: **LONG blocked** by the venue position. **SHORT open**, and a SHORT would hit the same
  unreadable-fill path.
- Service: untouched, pid 3282921, running since 04:28:37.
- 3 unresolved rows in `naked_position_alerts`.

Nothing was changed and nothing was proposed. Awaiting your decision.
