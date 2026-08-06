# TITAN — THE FOUR THAT COST MONEY, FIXED AND PROVEN BY EXECUTION

**2026-08-06 00:10 UTC · APPLIED · code `acf579e`, described in `38cd64c` · from `22a085e`**

Acts on `reports/2026-08-05-2320-titan-order-adapter-live-semantics-audited-against-the-sol-checklist.md`.
**F1, F3, F4 and F7 are applied.** F2 is **answered and deliberately not implemented**. F5, F6, F9a/b/c
are recorded untouched.

---

## §0 — NOTHING WAS HALF-APPLIED (checked before touching anything)

| check | result |
|---|---|
| **`openitems_guard.py`** | **exit 0** — canon `/mnt/…/kola-reports/reports/OPEN-ITEMS.md`, runtime HEAD `22a085e`, 11 watched values, header and current-state table agree. |
| **HEAD** | `22a085e` — the last confirmed commit. Nothing landed beyond it. |
| **Working tree** | `git status` **clean**. |
| **Service** | `active (running)` since **22:48:36 UTC**, `NRestarts=0`. |
| **Errors since 22:48:36** | **0** across 95 journal lines (traceback/error/exception/critical). |
| **Four boot gates** | green: `[ORDER-MODE] 🔴 LIVE ORDERS` · `[RECONCILE-XDB] ✅ 0 positions, 0 rows` · `[RECONCILE] boot reconciliation` LONG+SHORT · `[STOP-CLEANUP] no orphaned orders` both sides. |
| **Exchange, BOTH probes** | `fetch_positions` **0**, raw `swapV2PrivateGetUserPositions` **0**, open orders **0**, hedge mode `dualSidePosition=true`. |
| **`virtual_positions`** | **0** rows `status='open'`; last close vpos 92, 2026-08-04. |

**Runtime flags, read by IMPORTING `config`:**

```
LIVE_TRADING_ENABLED = True     EMA_ENVELOPE_GATE_ENABLED = True    LONG_PARTIAL_ENABLED  = True
ORDER_ADAPTER_LIVE   = True     EXIT_ADVISOR_DRYRUN       = False   LONG_PARTIAL_FRACTION = 0.3333…
SL_ATR_MULT          = 2.25     AI_ADVISOR_HIDE_1H        = False   LONG_PARTIAL_LEVEL_R  = 1.0
TRAIL_MULT_ATR       = 1.6875   EQH_EQL_SMART_TP_ENABLED  = False
```

All match the canon. **§0 clean — proceeded.**

---

## §1 — 🔴 F1: A FAILED READ NO LONGER CANCELS THE PROTECTIVE STOP

### (a) Three outcomes, decided AT THE READER

`main._fetch_open_position` returned `None` for two different facts. It now sits on top of a reader
that separates them, in the shape Mercury-SOL's Phase 1 used:

```python
POS_OPEN, POS_FLAT, POS_UNKNOWN = 'OPEN', 'FLAT', 'UNKNOWN'

def _fetch_position_state(symbol, position_side, double_probe=False, attempts=1, gap_s=2.0):
    """(state, pos) — POS_UNKNOWN means the read FAILED: the caller knows
    NOTHING and must not act."""
```

**FLAT is now a positive answer** ("the exchange replied and reported no position"). **UNKNOWN is its
own outcome and nothing destructive may key off it.**

SOL *deleted* its ambiguous helper so no future caller could reach for the shorter name. Titan has
nine consumers and eight of them are read-only, so deleting it would have meant rewriting eight call
sites the brief explicitly says to leave alone. The shim is kept and **labelled** instead:

```python
def _fetch_open_position(symbol, position_side):
    """🔴 THIS SHIM CONFLATES FLAT WITH READ-FAILED, ON PURPOSE AND VISIBLY. …
    DO NOT USE IT WHERE THE None BRANCH TAKES AN ACTION — cancelling, closing,
    finalising a row. Call `_fetch_position_state` there …"""
    state, pos = _fetch_position_state(symbol, position_side)
    return pos if state == POS_OPEN else None
```

### (b) 🔴 On READ FAILED: cancel nothing, alert, say what to do

```python
def _reconcile_side(symbol, side):
    state, pos = _fetch_position_state(symbol, side, double_probe=True, attempts=3, gap_s=2.0)
    if state == POS_UNKNOWN:
        print(f"[RECONCILE] 🔴 {side} position state UNKNOWN after 3 double probes — "
              f"CANCELLING NOTHING …", flush=True)
        send_tg(… "<b>Nothing was cancelled</b> (a wrong cancel strips a live position's "
                  "stop; a skipped cleanup does not).\n"
                  "<b>Operator:</b> check BingX for an open {side} position on {symbol} and "
                  "whether it carries a STOP_MARKET. If it is open and naked, attach a stop by "
                  "hand or restart the bot once the API is answering — this reconcile re-runs "
                  "on every boot and will re-attach the SL itself.")
        return
    if state == POS_FLAT:
        _cancel_stop_orders(symbol, side)      # positive evidence of flatness
        return
```

This is the doctrine the same function already applied forty lines lower to the **orders** read —
*"Can't confirm protection state → NEVER cancel; alert and leave alone"* — finally applied to the
**positions** read that decides whether there is anything to protect. The asymmetry that justifies it:
an orphan order left alive for one boot is recoverable in one restart; a live position stripped of its
exchange stop is not.

### (c) 🔴 The double probe is SHARED, not replicated — and made stricter

`_fetch_position_state(double_probe=True)` calls **`order_adapter._probe_positions`**, the very object
`assert_exchange_matches_db_at_boot` calls two seconds earlier. Verified by identity, not by
inspection: `OA._probe_positions is sys.modules['order_adapter']._probe_positions` → **THE SAME
OBJECT**. One probe pair, one place to fix it.

**The gap that made sharing necessary, restated so the fix is checkable:** the boot gate refuses only
on `perr and not positions` — when *every* probe failed. If the **unified** endpoint is down and the
**raw** one answers, the gate passes on the raw probe with a warning, and the old single-probe
`_reconcile_side` then asked the unified endpoint that is still down.

So the rule here is deliberately **stricter than the gate's**, because this caller *cancels*:

| what the probes say | old (single probe) | now |
|---|---|---|
| both answered, neither saw our side | FLAT → cancel | **FLAT → cancel** (unchanged) |
| unified DOWN, raw answered, our side unseen | *unified errored → None → 🔴 CANCEL* | **UNKNOWN → cancel nothing** |
| a probe SAW the position, other probe errored | depends which one answered | **OPEN** — presence beats noise |
| every probe failed | 🔴 CANCEL | **UNKNOWN → cancel nothing** |

Absence is only believed when **both probes answered and neither saw it**. Presence is believed
immediately from **either** probe: a probe error weakens an assertion of *absence*, never one of
*presence*. `attempts=3` re-probes an UNKNOWN before believing it — the same reasoning the gate uses
for a mismatch: a blip clears in seconds, an outage does not.

### (d) The other eight consumers, and what each now does

The shim maps UNKNOWN→`None`, so **all eight are behaviourally unchanged**. Stated per the brief:

| consumer | on UNKNOWN | does UNKNOWN cause an ACTION? | changed? |
|---|---|---|---|
| **`_reconcile_side:5213`** | **cancels nothing, alerts** | **YES — it cancelled every order on the side** | 🔴 **FIXED** |
| `_execute_close_position:1235` | returns `None`; `_do_close` leaves the row open and the position keeps its stop | no — an omission, and it fails **safe** | no |
| `_handle_5m_close_via_ai:3175` | exit advisor not consulted this tick | no — a skipped consultation | no |
| `_handle_liquidity_sweep:3580` | reports "nothing to close", skips the sweep exit | no — read-only; and `EQH_EQL_SMART_TP_ENABLED=False` (**F6**, recorded) | no |
| `_handle_exit_signal:3412` | **N/A** — routed to the DB by `engine_owns_position()` | no | no |
| `_handle_state_machine:3803` | **N/A** — routed to the DB | no | no |
| `virtual_trader._reconcile_passive_fill:1152` | false 🚨 alarm; **shouts and touches nothing** | no — fail-safe direction (**F5**, recorded) | no |
| `breakeven_worker` ×4 (`257/521/575/594`) | would mark jobs closed — but `breakeven_jobs` = **0 rows** and `_poll_once` stands down by flag | **provably dead** | no |

Only one consumer turned an unknown read into an action. Only that one changed.

### Proven by execution

```
F1a — THE READER SEPARATES THREE OUTCOMES
  ✅ single probe, exchange replies empty          -> FLAT
  ✅ single probe, fetch_positions RAISES          -> UNKNOWN
  ✅ single probe, position present                -> OPEN
  ✅ shim on a FAILED read still returns None      (eight consumers unchanged)
  ✅ shim on a FLAT read still returns None
  ✅ shim on an OPEN read returns the dict         contracts=0.0023

F1b/c — THE DOUBLE PROBE IS SHARED, AND STRICTER THAN THE BOOT GATE
  order_adapter._probe_positions is THE SAME OBJECT the boot gate calls (no replica)
  ✅ both probes answered, neither saw it                    -> FLAT
  ✅ unified DOWN, raw answered, our side unseen             -> UNKNOWN (not FLAT)
  ✅ a probe SAW the position despite errors                 -> OPEN, contracts+entryPrice carried
  ✅ every probe failed                                      -> UNKNOWN

F1 — _reconcile_side: THE ACTION SITE. WHAT DOES IT CANCEL?
  CASE 1 — the read FAILS (the F1 defect: this used to cancel everything)
    ✅ orders cancelled on an UNKNOWN read: 0
    ✅ operator alerted: 1   ✅ alert says nothing was cancelled   ✅ alert says what to do
  CASE 2 — the exchange POSITIVELY reports flat
    ✅ orphan cleanup ran: [('BTC/USDT:USDT','LONG')]   ✅ no needless alert
  CASE 3 — a position IS present
    ✅ orders cancelled while a position is open: 0
    ✅ the pre-existing orders-read doctrine still alerts: 1
```

---

## §2 — 🔴 F3: THE PARTIAL NOW SHRINKS THE BOOK BY WHAT IT SOLD

### (a) The effective fraction is derived from the fill

```python
cut_size = _cut_fill['amount']          # the EXECUTED size — was already read correctly
eff_frac = float(cut_size) / float(total_size)
if not (0.0 < eff_frac < 1.0):
    …refuse, alert, leave the book UNCHANGED…      # sold nothing, or somehow everything
    return False
entry_fee_share = sum(leg.get('fee', 0.0) for leg in legs) * eff_frac
for leg in legs:
    leg['size'] = leg['size'] * (1.0 - eff_frac)   # was: (1.0 - frac)
    leg['fee']  = leg.get('fee', 0.0) * (1.0 - eff_frac)
```

The realised PnL was **always** computed on the executed size. Only the write-down used the requested
fraction, so one event was booked two different ways. The Telegram line now reports both — `30.4%
sold (asked 33.3%)` — so the truncation is visible rather than inferred.

### (b) Proven by execution — isolated DB, EVERY module's `DB_PATH` patched

The 2026-08-04 isolation lesson is enforced, not assumed: **19** `DB_PATH`/`_DB_PATH` attributes
patched to the copy, then a **hard assert** that no module still points at a `.db` other than the
isolated one. The live DB's `MAX(id)` is still **92** afterwards — the test row 93 never left the copy.

```
FIXTURE: LONG 0.0023 BTC @ 64625 · asked 0.0023 × 0.3333… = 0.0007666667
         executed 0.0007 (BingX truncates to 0.0001 precision)
         EXCHANGE REMAINDER = 0.0015999999999999999

--- PRE-FIX arithmetic (shrink by REQUESTED frac) ---
  BOOK remainder     : 0.0015333333333333334
  EXCHANGE remainder : 0.0015999999999999999
  difference         : -0.0000666667 BTC (-4.1667%)
  EXACT MATCH        : 🔴 NO

--- SHIPPED code (shrink by EXECUTED size) ---
  BOOK remainder     : 0.0015999999999999999
  EXCHANGE remainder : 0.0015999999999999999
  difference         : +0.0000000000 BTC (+0.0000%)
  EXACT MATCH        : ✅ YES
```

**Book remainder equals exchange remainder exactly** — bit-identical floats, not "within tolerance".

### (c) 🔴 PAPER IS **NOT** BYTE-IDENTICAL — the brief's premise is wrong, and I measured it

The brief said *"nothing rounds there, so the numbers must not move."* **It rounds.** `check_size` runs
in **both** modes by explicit design — *"so paper rejects what live would reject"* — and rounds through
`amount_to_precision` in both. Measured on the real paper geometry (vpos 82's 0.1543 BTC), with
`orders_are_real()` forced False:

```
requested cut       : 0.05143333333333333
simulated fill      : 0.0514         simulated=True
ROUNDS IN PAPER     : 🔴 YES   -> the premise is FALSE

PRE-FIX book leg    : 0.10286666666666668
SHIPPED book leg    : 0.10289999999999999
SIMULATED remainder : 0.10289999999999999   (total - the fill paper itself reported)
PRE-FIX vs sim fill : -0.000033333333 BTC (-0.0324%)
SHIPPED vs sim fill : +0.000000000000 BTC (+0.0000%)
PAPER NUMBERS MOVE  : 0.000033333333 BTC (0.0324% of the remainder)
```

**The pre-fix paper leg `0.10286666666666668` is EXACTLY what vpos 82 stores.** That is not a
coincidence — it is proof that **the one paper partial in history carries the same defect**, 129×
smaller only because paper's 0.1543 BTC sits further from the 0.0001 tick than live's 0.0023 does.
The audit's "invisible in all paper history by construction" is right about the *magnitude* and wrong
about the *mechanism*: it was there, at 0.03%, not absent.

**So I did not special-case paper, and I want that decision on the record.** Branching the arithmetic
on `orders_are_real()` would have preserved byte-identity by **deliberately keeping F3 alive in paper**
— making paper's book disagree with paper's own reported fill, which is the exact defect being fixed.
One arithmetic, both modes, matching `check_size`'s own reasoning for running everywhere.

**No historical row is rewritten.** `_take_long_partial` only runs forward; vpos 82 — the sole
`partial_taken=1` row, PAPER — keeps its stored legs and its `realized_partial_usdt` untouched. The
0.032% applies to **future** paper partials only.

---

## §3 — 🔴 F4: A ZERO OR ABSENT FILL NO LONGER BECOMES A FULL POSITION

### (a) Presence, not truthiness

```python
executed = filled if filled else float(amount)      # 🔴 was: 0.0 and None both fall through
```

`filled` is now parsed by `_coerce_filled` (`0.0` is a **value**, not an absence) and the three
outcomes are answered separately.

### (b) 🔴 What happens when the fill genuinely cannot be read — and where I disagree with the brief

**The ladder, as the brief asked:**

1. `filled` from the create response, tested with `is not None`.
2. **`filled` absent OR `0.0` → RE-READ IT FROM THE EXCHANGE** — `_readback_filled`, 2 attempts × 1 s
   via `fetch_order`, the same primitive `main.fetch_order_fee` already uses for the fee, applied to
   the number the whole book is built on. Re-reading a `0.0` matters as much as re-reading a `None`:
   a market order's create response can be ahead of settlement, so a create-time `0.0` is not proof of
   a non-fill either.
3. **Readback confirms `0.0` → the order did NOT fill.** `market_entry` returns **`None`** — which
   `execute_entry` already reads as *"no position, write no row"* — and alerts. This is the actual
   money defect closed: today a confirmed zero became a **full** position.
4. **Readback cannot answer at all → `fill_unreadable=True`.**

**On step 4 I disagree with the brief's reading, and here is the argument.** "Do not invent a size" is
right about the principle and, applied literally to `market_entry`, produces a worse state than the
one it prevents:

- `execute_entry`'s contract is explicit: `None` from the adapter means **the order was refused and
  nothing was sent** — the line right below it reads *"IRREVERSIBLE FROM HERE. A real order may now
  exist."* Returning `None` **after** a `create_market_order` that returned successfully makes the
  adapter lie about whether an order exists, and `execute_entry` responds by writing **no row and
  attaching no stop**. That is an unmanaged, **naked** live position — the 2026-07-29 state.
- The protective stop is `closePosition='true'`, so it covers the **whole** position **regardless of
  the quantity we pass**. Protection does not depend on getting the size right. Only the *book number*
  does.
- Reaching step 4 requires the order to be accepted and *then* two `fetch_order` calls to fail — a
  near-total outage in which no protective action is possible anyway.

So step 4 falls back to the requested size **as a declared, alerted estimate**: a `🔴 CRITICAL`
journal line plus a Telegram alert naming the order id, saying in words that the book carries the
**requested** size and that it is **NOT a confirmed fill**, and telling the operator to verify against
the exchange and reconcile the row. **The defect the audit named was the silence, not the fallback** —
*"recorded as a full position, with no warning printed."* The silence is gone; the number is now
labelled an estimate rather than presented as a fill.

I also considered a third rung — reading the **position** back and using its `contracts` as the
executed size. I rejected it: it is only unambiguous from flat, and nothing in `_live_fill` knows
whether the entry was from flat, so it would be a correct-looking number that silently breaks the
moment a top-up path exists. `market_reduce` has the same problem in reverse.

`market_reduce` uses the same ladder, with the same reasoning inverted at step 3: a confirmed zero
returns `None`, which `_take_long_partial` already reads as *"the partial did not happen"* — it banks
nothing, shrinks nothing, and correctly stays eligible to retry, because nothing left the book.

### (c) The stop is still `closePosition='true'` — confirmed on the real signed request

Rebuilt through ccxt's signer with `exchange.fetch` intercepted (nothing sent):

```
POST /openApi/swap/v2/trade/order
  closePosition = true   positionSide = LONG   quantity = 0.0023
  side = SELL            stopPrice = 50000.0   symbol = BTC-USDT   type = STOP_MARKET
```

Unchanged by this work. Nothing is left unprotected on any F4 branch.

### Proven by execution

```
  ✅ create response reports a real fill        -> amount 0.0023, no readback needed
  ✅ create response reports a PARTIAL fill     -> amount 0.0011 (executed), partial_fill=True
  🔴 create response OMITS `filled`             -> readback used, amount 0.0023, NOT flagged unreadable
  🔴 filled=0.0 and the READBACK CONFIRMS 0.0   -> zero_fill=True, amount 0.0, NOT the requested 0.0023
  🔴 filled absent AND the readback fails       -> fill_unreadable=True, requested booked as a DECLARED estimate
  ✅ market_entry  on a zero fill returns None  (== "no position, no row"), operator told
  ✅ market_reduce on a zero fill returns None  (== "nothing sold")
```

---

## §4 — 🔴 F7: THE LEGACY P3 CLOSE IS CONVERTED TO CLOSE-FIRST / CANCEL-AFTER

Order before → after:

| | before | after |
|---|---|---|
| 1 | fetch ticker | fetch ticker |
| 2 | **cancel every trigger on the side** | read the real on-exchange size |
| 3 | read the real on-exchange size | **send the close** |
| 4 | send the close | **cancel every trigger on the side** |
| 5 | `_cancel_stop_orders` sweep | `_cancel_stop_orders` sweep |

The cancel loop is moved below the close **verbatim in body**, identical to
`_execute_close_position`'s. A raise from `create_market_order` — rate limit, a 109400-class
rejection, a network blip — now changes nothing: the position stays open **and stays protected**.

**Converted, not made to refuse, and the reason is a money argument.** This branch exists to honour an
external close instruction. Making it refuse would convert a transport-ordering bug into a *trading*
decision — a live position left open against an explicit close signal — on a path whose own guard
concedes *"dormant is a property of the current alert format, not a guarantee."* The reorder is
behaviour-identical on every success and strictly safer on failure, which is the whole of the
2026-07-30 argument. Its `[P3-CLOSE] BLOCKED in paper mode` guard is untouched.

The degraded `closePosition='true'` fallback below it is **left exactly as it was** — that is F9c,
recorded below, not fixed.

---

## §5 — RECORDED, NOT FIXED

### 🔴 F2 — idempotency: **ANSWERED. BingX accepts a client order id, and ccxt passes it.**

The brief asked before fixing. Both halves are **yes**, established by building the real signed
request rather than by reading docs:

- **ccxt 4.5.52 `bingx.create_order_request`** maps a `clientOrderId` (or `clientOrderID`) param onto
  the request key `clientOrderID` for swap, and omits it from the leftover `params` sweep:
  `exchangeClientOrderId = 'newClientOrderId' if isSpot else 'clientOrderID'`.
- **It reaches the wire.** Signed URL captured with `exchange.fetch` intercepted, nothing sent:

```
POST /openApi/swap/v2/trade/order
  clientOrderID = titan-sl-vpos93-a1     closePosition = true   positionSide = LONG
  quantity = 0.0023   side = SELL   stopPrice = 50000.0   symbol = BTC-USDT   type = STOP_MARKET
```

`cancel_order` and `fetch_order` in the same ccxt module also accept it, so a post-failure *check* by
client id is available as well.

**So the fix is the key** — `_place_stop_with_retry` stamps a deterministic id (e.g.
`titan-sl-{vpos}-{attempt-independent nonce}`) reused across all three attempts. **Not implemented, per
the brief.**

🔴 **The one thing this does NOT prove, stated so nobody builds on it:** that BingX **rejects** a
duplicate `clientOrderID`. Accepting the field and enforcing uniqueness on it are different claims, and
only the first is proven here. It cannot be established without sending two real orders. **Verify that
before relying on the key alone** — otherwise the belt-and-braces form (key **plus** a post-failure
`fetch_order`-by-client-id check before attempt 2) is the safe construction. §1a's *"exactly one
`closePosition` order"* claim stays **unproven** until one of the two lands.

### The rest, untouched and unchanged by this work

- **F5** — `_reconcile_passive_fill`'s *"cannot tell → do NOT guess"* `except` is still unreachable:
  the inner reader already swallows the exception, so the failure arrives as `pos = None`. Outcome is
  a **false 🚨 alarm** that shouts and touches nothing. The shim preserves this exactly.
- **F6** — `_handle_liquidity_sweep` still reads the exchange unconditionally, bypassing the item-12
  routing. Read-only; `EQH_EQL_SMART_TP_ENABLED = False` bounds today's blast radius.
- **F9a/b** — `market_reduce`'s and `_take_long_partial`'s docstrings still say "reduce-only";
  `check_size`'s still cites the retired `$200 / 0.0031 / 31×` geometry (live is `$150 / 0.0023 / 23×`).
- **F9c** — 🔴 the degraded fallback at `main.py:4823` still rests on an **UNTESTED** claim: that
  `closePosition='true'` **ignores quantity on a plain MARKET order**. That is proven only for
  `STOP_MARKET`. If it is wrong, that path closes **0.0001 of a 0.0023 position and reports it as the
  full close**. Never executed. It is the only path where a wrong `closePosition` assumption converts
  directly into an unclosed live position — and it sits inside the block I just reordered, so it is
  now *nearer* the money, not further.

---

## §6 — WHAT CHANGED, AND WHAT PROVABLY DID NOT

**AST per-function diff against the pre-edit snapshot** — hashes over each function body with
docstrings stripped, so a comment cannot hide a code change:

```
main.py             79 functions   CODE-CHANGED: _fetch_open_position, _reconcile_side, webhook
                                   ADDED:        _fetch_position_state
order_adapter.py    28 functions   CODE-CHANGED: _live_fill, market_entry, market_reduce
                                   ADDED:        _alert_unreadable_fill, _coerce_filled, _readback_filled
virtual_trader.py   49 functions   CODE-CHANGED: _take_long_partial
breakeven_worker.py 19 functions   CODE-CHANGED: none
```

**7 changed, 4 added, nothing else.** `fetch_order_fee` and `_sim` appear only as diff *hunk headers*
(the enclosing def of an insertion point) and are byte-identical.

**Untouched, checked by grepping the diff rather than asserted:** no line matching `SL_ATR_MULT=`,
`TRAIL_MULT_ATR=`, `*_ENABLED=`, `CREATE TABLE`, `ALTER TABLE`, `SYSTEM_PROMPT`, `PROMPT=`, `score`,
`weight`, `threshold`, `HARD RULE` or `SOFT RULE` was added or removed. **Gates, geometry, score bars,
both prompts and every schema are untouched.**

`ast.parse` ✅ and `py_compile` ✅ on all four modules.

## §7 — RESTARTED DELIBERATELY, FROM FLAT

| | before restart | after restart |
|---|---|---|
| `virtual_positions` `status='open'` | **0** | **0** |
| unified `fetch_positions` | 0 | **0** |
| raw `swapV2PrivateGetUserPositions` | 0 | **0** |
| open orders | 0 | **0** |
| probes agree | ✅ | ✅ |

Restarted **23:59:39 UTC**. `ActiveState=active`, `NRestarts=0`, **0** errors in the boot log.

```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True · ORDER_ADAPTER_LIVE = True · $30 x 5 = $150
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
[RECONCILE] boot reconciliation starting
[STOP-CLEANUP] no orphaned orders for LONG BTC/USDT:USDT
[STOP-CLEANUP] no orphaned orders for SHORT BTC/USDT:USDT
[RECONCILE] done
```

**Four boot gates green.** No `[POS-UNKNOWN]` line — the double probe answered on both sides and both
took the `POS_FLAT` path, so orphan cleanup still ran exactly as before. **`openitems_guard.py` exit
0** afterwards.

🔴 **COMMIT PROVENANCE, because the log will confuse a session with no memory.** The midnight cron
(`Автоматический бэкап Титана`) fired at **00:00:02** while the working tree held these edits and swept
them into **`acf579e`** under its generic message. `acf579e` was already **pushed**, so it is **NOT**
rewritten; **`38cd64c`** is the description it should have carried. `acf579e` touches exactly the three
files above and nothing else — verified by `git show --stat`.

---

## §8 — THE THROUGH-LINE

The audit sorted Titan's defects into *what we send* (right) and *what we believe we read* (wrong).
All four fixed here are the second kind, and three of them are the same sentence: **a number that came
back from the exchange was replaced by a number we had asked for.**

- **F1** replaced "the exchange did not answer" with "the exchange said flat" — and cancelled a stop on it.
- **F3** replaced "what we sold" with "what we asked to sell" — for the life of the position.
- **F4** replaced "what filled" with "what we requested" — including when nothing filled.

**F7 is the odd one out and worth naming separately:** not a misread, but a conversion that was applied
to every close path on 2026-07-30 except one. It survived because its guard blocks **paper**, so it
never fired in testing and never fired in production — invisible to both. The lesson is the same one
F3 carries: **a path that has never executed is not a path that is safe**, and 0 occurrences measures
the alert configuration, not the code.

---

*Applied and committed. Isolation enforced with a hard assert across 19 `DB_PATH` attributes; live
`trades.db` `MAX(id)` still 92, so no test row escaped. Requests were built through ccxt's signer with
`exchange.fetch` intercepted, so the signed URLs above are real and none of them left the box. No order
was sent. `openitems_guard.py` exit 0; the canon header now reads `38cd64c`.*
