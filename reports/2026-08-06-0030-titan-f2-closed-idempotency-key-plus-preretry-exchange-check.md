# TITAN — F2 CLOSED: A KEY, AND A CHECK THAT DOES NOT TRUST THE KEY

**2026-08-06 00:30 UTC · APPLIED · `7c2feac` · from `38cd64c`**

Closes the last money-path defect from the 23:20 order-adapter audit, plus **F9c**, which the F7
reorder moved nearer the money. Canon **§1a's open claim is closed** — restated to say what is
actually guaranteed and by which mechanism.

---

## §0 — STATE BEFORE TOUCHING ANYTHING

| check | result |
|---|---|
| **`openitems_guard.py`** | **exit 0** — runtime HEAD `38cd64c`, 11 watched values, canon agrees. |
| **HEAD / tree** | `38cd64c`, `git status` **clean**. |
| **Service** | `active`, since 23:59:39, `NRestarts=0`, **0** errors. |
| **Four boot gates** | all green, both sides. |
| **Exchange, BOTH probes** | positions `{}`, errors `[]`; open orders **0**. |
| **`virtual_positions`** | **0** rows `status='open'`. |

---

## §1 — 🔴 F2: THE DEFECT, AND WHY THE OBVIOUS FIX WAS NOT ENOUGH

`_place_stop_with_retry` retried three times with no key and no check. A failure returned **after**
the order reached BingX's matching engine — a timeout, a dropped response, a 5xx on the way back —
made attempt 2 place a **second `STOP_MARKET closePosition='true'`**. Only the second id was returned
and stored in `virtual_positions.stop_order_id`; the first was **invisible** and survived every later
`move_stop`, which cancels only the recorded id.

**The decision the operator made, and I think it is the right one:** build **both** halves, because
*BingX accepting `clientOrderID` is proven and BingX enforcing uniqueness on it is not*. A retry
guard resting on an unproven venue behaviour is the same shape as every "reads as armed" defect
found this week.

### (1) THE KEY — deterministic, stable across attempts, unique across positions

```python
def _stop_client_id(symbol, position_side, stop_price, anchor=''):
    key = f"{symbol}|{position_side}|{stop_price}|{anchor}"
    return 'titan-sl-' + hashlib.sha1(key.encode()).hexdigest()[:20]
```

**Format:** `titan-sl-<20 hex chars>` — **29 characters**, charset `[a-z0-9-]` only, well inside
BingX's field limits and free of anything needing escaping in a signed query string. Verified by
execution: `length = 29, charset ok = True`.

**Stable across attempts:** every input is fixed for the duration of one `_place_stop_with_retry`
call, so all three attempts compute the same id. That is the entire point of a key.

**Unique across positions — this is what `anchor` is for.** Without it the tuple is
(symbol, side, stop_price), which repeats the moment two positions ever compute the same stop level;
a venue that *does* enforce uniqueness would then reject the second position's **first** attempt.
Each caller passes something that cannot repeat:

| call site | anchor | why it cannot repeat |
|---|---|---|
| entry stop (`place_stop` ← `execute_entry`) | `entry:<ENTRY ORDER ID>` | a fresh exchange order id per position |
| breakeven / TIGHTEN (`move_stop_with_race_guard`) | `move:<OLD STOP ORDER ID>` | a fresh exchange order id per move |
| boot re-attach (`_reconcile_side`) | `reattach:<entry_price>:<amount>` | **deliberately repeatable** for the SAME naked position, so two restarts re-attaching it present one id, not two |

Proven:

```
format      : titan-sl-<20 hex>          length: 29 chars, charset ok = True
✅ same inputs                      -> SAME id (stable across all 3 attempts)
✅ different position (entry id)    -> DIFFERENT id
✅ same position, breakeven move    -> DIFFERENT id from the entry stop
```

### (2) 🔴 THE CHECK — the half that works whether or not BingX dedupes

Before **every** retry, and once more **after the final failure**, `_find_existing_stop` asks the
exchange whether a protective stop for this position already exists, and **adopts** it rather than
sending. It shares **`order_adapter._probe_stop_orders`** — the same two-probe union
(`fetch_open_orders` + raw `swapV2PrivateGetTradeOpenOrders`) the boot gate already uses — now also
carrying `clientOrderId`. Shared, not replicated, exactly as F1 shared `_probe_positions`.

**Two kinds of evidence, strongest first:**

1. **an open order carrying OUR client id** — proof that *our* attempt landed;
2. **any live `STOP_MARKET closePosition='true'` on this `positionSide`** — sound because
   `MAX_POSITIONS_PER_SIDE = 1` **and** the DB unique index `ux_vpos_one_open_per_side` allow at most
   one position per side, so such an order can only be protecting the position we are protecting.

Rung 2 is not redundancy for its own sake: it is what covers the case where the order landed but
BingX echoed a different client id, or none at all. **Proven separately** — with the venue not
echoing the id, the side scan still adopts.

**`ABSENT` requires both probes to have answered.** Any probe error with nothing found is `UNKNOWN`.
For a caller about to *send*, absence must be evidenced, never inferred from silence — the same rule
F1 applied to positions, applied here to orders.

### (3) 🔴 WHEN THE CHECK ITSELF FAILS: NOTHING IS SENT

An unknown check result **never** licenses a second placement. It returns failure into the caller's
existing invariant and alerts.

**The argument, since the brief asked for one.** The cost of being wrong in one direction is **two
`closePosition` stops on one position** — the state canon §1a calls catastrophic, and which is
*invisible* to the bot because only one id is ever stored. The cost of stopping is a **loud, bounded
failure that every caller already handles**:

| caller | what it already does with a `None` |
|---|---|
| `order_adapter.place_stop` | fires `_emergency_close` — the item-11 invariant. Position closed, operator alerted. |
| `move_stop_with_race_guard` | old stop already cancelled → fires `_emergency_close`. |
| `main._reconcile_side` | alerts `🚨 Could not re-attach SL … MANUAL ACTION`, does not auto-close. |

**There is a designed response to "cannot protect". There is none to "silently protected twice".**
That asymmetry decides it. The check also re-probes twice with a 1 s gap before declaring `UNKNOWN`,
so a blip does not fire an emergency close.

**Why the check runs after the LAST failure too:** the final attempt is exactly as ambiguous as the
earlier ones. Returning `None` there would fire the emergency close on a position that is, in fact,
protected — closing a live position over a dropped HTTP response.

---

## §2 — PROVEN BY EXECUTION: THE TIMEOUT-AFTER-SUCCESS CASE

The venue **books the order and then fails the response** — the exact case that produced two stops.
Isolated DB copy, every module's `DB_PATH` patched, hard leak assert.

```
attempt 1 lands on the book, then the response fails (venue ECHOES our client id)
  ✅ create_order called          : 1
  ✅ 🔴 ORDERS ON THE BOOK        : 1
  ✅ returned the id that DID land: 'EX1'      ✅ no error reported

same, but the venue does NOT echo the client id (side-scan evidence)
  ✅ create_order called          : 1
  ✅ 🔴 ORDERS ON THE BOOK        : 1
  ✅ adopted by the positionSide + closePosition scan: 'EX1'

PRE-FIX comparison — the same venue, the check removed
     create_order called 2x, ORDERS ON THE BOOK = 2, returned 'EX2'
  ✅ 🔴 PRE-FIX leaves TWO closePosition stops on one position
     …and the first, EX1, is INVISIBLE to the bot: only 'EX2' is stored.

the order genuinely never landed -> a retry SHOULD send (the guard must not over-block)
  ✅ create_order called twice    ✅ exactly ONE order on the book    ✅ returned 'EX2'

all attempts fail AFTER landing -> adopt rather than report naked
  ✅ 🔴 ORDERS ON THE BOOK: 1     ✅ adopted, not reported as unprotected: 'EX1'
```

**Same venue, same failure: the old loop ends with 2, the shipped loop ends with 1.**

**When the check itself fails** (order landed, then both probes go down):

```
  ✅ create_order called ONCE — no second placement on an unknown check
  ✅ 🔴 ORDERS ON THE BOOK: 1
  ✅ returns failure into the caller's invariant: None
  ✅ error reported, not swallowed   ✅ operator alerted
  ✅ the alert says "No second stop was sent"
```

**The state check in isolation:** both probes answer + stop present → `FOUND`; both answer + nothing
→ `ABSENT`; probes down + nothing seen → **`UNKNOWN`, never `ABSENT`**.

**The key on the wire** — built through `_place_stop_with_retry` itself with ccxt's real signer and
`exchange.fetch` intercepted, so this is the request the bot would actually send, and none of it left
the box:

```
POST /openApi/swap/v2/trade/order
  clientOrderID = titan-sl-b601d45e86da29d522f8
  closePosition = true      positionSide = LONG      quantity = 0.0023
  side = SELL               stopPrice = 62000.0      symbol = BTC-USDT      type = STOP_MARKET

✅ clientOrderID on the wire   ✅ closePosition still true   ✅ type still STOP_MARKET
✅ every attempt used the SAME client id
```

---

## §3 — 🔴 §1a's OPEN CLAIM, CLOSED

Canon §1a asserted *"exactly ONE `closePosition` order exists at any moment"* from three numbered
points that enumerate **creation sites**. **The gap: they never ask whether one site can create two
orders from one logical call.** The claim was about *sites*; the risk was about *attempts*.

The canon now carries a boxed correction under that line stating what is actually guaranteed:

| # | mechanism | rests on | proven? |
|---|---|---|---|
| 1 | **THE KEY** — deterministic `clientOrderID`, identical across all three attempts | BingX **enforcing** uniqueness | 🔴 **NO.** Only that the field is **ACCEPTED** is proven, on the real signed request. Cannot be proven without sending two real orders. |
| 2 | **THE CHECK** — pre-retry exchange lookup + adopt | reads the bot already performs at boot, plus `MAX_POSITIONS_PER_SIDE = 1` and `ux_vpos_one_open_per_side` | ✅ **YES, by execution** — one order where the old loop left two |

**Mechanism 2 is load-bearing.** The honest statement of the claim is now: *exactly one
`closePosition` order exists at any moment* — guaranteed **by construction** for the trail door (the
three original points, unchanged and still correct) and **by an exchange-state check before every
retry** for the retry door, **not** by trusting BingX to dedupe.

**Still open, and named as such:** whether BingX rejects a duplicate `clientOrderID`. If that is ever
established, mechanism 1 becomes a second independent guarantee; until then it is a belt whose braces
do the work. The 🔴 warning about the exchange trail (`_attempt_trail` creates a
`TRAILING_STOP_MARKET` and never cancels the breakeven `STOP_MARKET`) is **untouched and still
stands** — that door remains shut only by configuration.

---

## §4 — 🔴 F9c: THE DEGRADED CLOSE NO LONGER BETS ON AN UNTESTED BEHAVIOUR

The P3 close fallback sent a plain `MARKET` order with `closePosition='true'` and a **placeholder
quantity** (the market minimum, 0.0001), on the claim that `closePosition='true'` *"makes the exchange
the source of truth and ignores quantity"* — **proven for `STOP_MARKET`, never tested for a plain
`MARKET` order.**

**Traced to the end, rather than left at "it closes too little".** If the claim is wrong:

1. it closes **0.0001 of 0.0023** — 4.3%;
2. it reports `amount` from the order response as the **full close**, and the shared tail writes the
   row up as closed;
3. **it then falls through to the cancel loop**, which strips every `STOP_MARKET` /
   `TRAILING_STOP_MARKET` on the side.

End state: **~96% of a live position still open, its row written up as closed, and NO protective
stop.** That is strictly worse than the 2026-07-29 naked short, because the book also believes the
position is gone. The audit rated this 🟡 7; traced through the cancel loop it belongs with the money
defects, and the F7 reorder had just moved it inside the block.

**It now alerts and sends nothing.** I agree with the brief and did not argue the other way — and the
reason is specific rather than general: **since the F7 reorder the cancel loop runs only AFTER a
close**, so returning early leaves the position **open and still protected by its exchange stop**.
That is a genuinely safe resting state, not merely a less-bad one. An unsent close that shouts is
recoverable on the next signal or by hand; a close that silently moved 4% of the position **and
cancelled its stop** is not.

The dead `amount` recovery below it (`(order).get('filled') or (order).get('amount') or 0`) is
**deleted**, not left dangling — it existed solely to paper over the placeholder close, and code that
still reads a variable its guard no longer produces is the exact class this bot keeps finding.

**Proven structurally** (AST over the shipped file, not by reading):

```
P3 close — `close_amount is not None` (SEND path):
   order-sending calls: ['exchange.create_market_order']
P3 close — `else` (size UNREADABLE):
   order-sending calls: NONE — 🔴 nothing is sent
   ends in a return: True      sends a Telegram alert: True
Whole-file: placeholder `_min_amt` remains: False    `P3-CLOSE-FALLBACK` marker remains: False
Scope safety (NameError check): row_id ✅  combo ✅  symbol ✅  position_side ✅  close_amount ✅
```

---

## §5 — WHAT CHANGED, AND WHAT PROVABLY DID NOT

AST per-function diff against the pre-edit snapshot, docstrings stripped so a comment cannot hide a
code change:

```
main.py             CODE-CHANGED: _reconcile_side, webhook
order_adapter.py    CODE-CHANGED: _probe_stop_orders, place_stop
virtual_trader.py   CODE-CHANGED: execute_entry
breakeven_worker.py CODE-CHANGED: _place_stop_with_retry, move_stop_with_race_guard
                    ADDED:        _find_existing_stop, _stop_client_id
```

**7 changed, 2 added, nothing else.** `_probe_stop_orders` gained one key (`clientOrderId`) — purely
additive; every existing reader keys off `id`/`type`/`positionSide`/`trigger`/`closePosition` and is
unaffected, including `assert_exchange_matches_db_at_boot`.

**Untouched, checked by grepping the diff rather than asserted:** no added or removed line matches
`SL_ATR_MULT=`, `TRAIL_MULT_ATR=`, `*_ENABLED=`, `*_THRESHOLD=`, `CREATE TABLE`, `ALTER TABLE`,
`SYSTEM_PROMPT`, `PROMPT=`, `HARD RULE` or `SOFT RULE`. **Gates, geometry, score bars, both prompts
and every schema are untouched.**

`ast.parse` ✅ and `py_compile` ✅ on all four modules.

## §6 — RESTARTED DELIBERATELY, FROM FLAT

| | before | after |
|---|---|---|
| `virtual_positions` open rows | **0** | **0** |
| double probe (positions) | `{}`, errors `[]` | **`{}`, errors `[]`** |
| unified `fetch_positions` | 0 | **0** |
| raw `swapV2` positions | 0 | **0** |
| stop-order probe | 0 orders, 0 errors | **0 orders, 0 errors** |

Restarted **00:25:54 UTC**. `ActiveState=active`, `NRestarts=0`, **0** errors. Four boot gates green;
no `[POS-UNKNOWN]` and no `[BE-SL-*]` line — nothing degraded on the way up. **`openitems_guard.py`
exit 0** afterwards, canon header now `7c2feac`. Live `trades.db` `MAX(id)` still **92** — no test row
escaped the isolated copy.

---

## §7 — THE THROUGH-LINE

The four fixed at 00:10 were all *a number that came back from the exchange was replaced by a number
we had asked for*. **These two are a different sentence: a mechanism was trusted to behave a way
nobody had checked.**

- **F2** trusted a retry to be harmless — never asking what happens when the failure is on the way
  *back*. And the obvious fix, an idempotency key, would have replaced one unchecked assumption with
  another: *BingX dedupes on `clientOrderID`*. Proving the field is **accepted** is easy and I did it;
  proving it is **enforced** needs two real orders and nobody should send them to find out. So the
  guarantee is carried by the mechanism that needs no such proof, and the key rides along.
- **F9c** trusted `closePosition='true'` to ignore quantity on an order type it had only been observed
  on as `STOP_MARKET`. The fix is not to test the claim — it is to stop depending on it.

**The generalisable rule, and it is the week's rule:** when a guard rests on a claim about someone
else's system, either prove the claim or build the guard so the claim does not matter. Where both are
possible, do both — but be explicit about **which one is actually load-bearing**, because that is the
line a future session will quote.

---

*Applied and committed as `7c2feac`. No order was sent: the signed requests above were built through
ccxt's signer with `exchange.fetch` intercepted, and every venue in the proofs is a stub. Isolation
enforced with a hard assert across 19 `DB_PATH` attributes.*
