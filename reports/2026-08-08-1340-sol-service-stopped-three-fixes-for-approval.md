# sol-service-stopped-three-fixes-for-approval

_2026-08-08 13:40 UTC_

---

# Mercury-SOL — service STOPPED, three fixes designed. NOTHING APPLIED, NOTHING RESTARTED.

**Status: `mercury-sol` is `inactive (dead)`, exit code 0/SUCCESS, stopped 13:26:29 UTC after
14h27m. The venue position and its stop are untouched. Titan is unaffected and still running.
No file was edited — `main.py`, `tor_retry.py` and `gunicorn_mercury.conf.py` still carry their
pre-session mtimes. Awaiting your approval on the diffs below.**

Prior forensics this pass builds on:
https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1321-sol-live-forensics-three-entries-one-open.md

---

## 1. SERVICE STOPPED — AND THE POSITION IS UNTOUCHED

```
Active: inactive (dead) since Sat 2026-08-08 13:26:29 UTC; Duration 14h 27min 1.654s
Process: 3147176 ExecStart=/usr/local/bin/gunicorn ... (code=exited, status=0/SUCCESS)
port 5002 not bound     no mercury-sol gunicorn processes
gunicorn: master [titan-btc] / worker [titan-btc]   ← Titan untouched, still running
```

Venue re-read **after** the stop:

| field | before stop (13:11) | after stop (13:28) |
|---|---|---|
| size | 1.3 | **1.3** |
| avgPrice | 74.80 | **74.80** |
| **stopLoss** | **73.89** | **73.89** |
| openTime | 1786179014459 | **1786179014459** (unchanged) |
| conditional order | Untriggered 73.89 qty 1.3 | **Untriggered 73.89 qty 1.3** |
| unrealisedPnl | +0.832 | +0.8853 |

Only uPnL moved, because the mark moved (75.44 → 75.481). You were right that stopping costs
nothing: the stop is a **position-level** `trading_stop` attribute plus a venue-side conditional
order — both live on Bybit, neither in our process.

**One thing to decide separately:** the unit is still `enabled`, so a host reboot would start it.
Say the word and I mask it while it sits.

---

## 2. FIX #1 — THE FILL READ

### (a) THE CHOICE — and your reading needs one correction

You framed it as "`acknowledged=True` is the minimal change but silences a warning; `fetchClosedOrder`
is semantically correct." I checked what each one actually calls, and **that flips the argument**:

| call | ccxt endpoint |
|---|---|
| `fetch_order` | **`GET /v5/order/realtime`** |
| `fetch_order(acknowledged=True)` | **`GET /v5/order/realtime`** — same |
| `fetch_open_order` | `GET /v5/order/realtime` — same again |
| `fetch_closed_order` | **`GET /v5/order/history`** — a *different* endpoint |

`fetchClosedOrder` is not the same call with a better name. It is a **different endpoint**:
`order/history`, which Bybit documents for *older* records, not real-time ones. Every fill read in
this file happens **~1 second after its own order**. `order/realtime` is what Bybit documents for
exactly that case, and it is the endpoint the shipped code already meant to hit — the only thing
stopping it is a ccxt guard that never let the request be built.

So choosing `fetchClosedOrder` would trade a proven-working real-time read for one that may not have
propagated yet — a **new** way to land in the same "refuse to book" branch we are trying to leave.

And the warning being acknowledged is not a hazard notice. It says the lookup covers the **last 500
orders of any status**. An order placed one second ago is inside that window by construction.

**Chosen: `acknowledged=True`, set once as an exchange OPTION, not as a param at the call sites.**
ccxt reads it via `handle_option_and_params('fetchOrder','acknowledged')`, so one line fixes **all
four** call sites — `_read_entry_fill` (1959), entry fee (2405), close fee (2703), partial fill
(2797). **Three of those four sit in `except: pass` blocks** and have been failing *silently* all
along, which is why every close card today said "venue fee UNREADABLE — booking MODELLED". A
per-call-site param fixes whichever site you remember.

**The trap, and it is the one that would half-fix this:** `tor_retry.iso_exchange()` builds a
*second* ccxt client for 403 retries. Set the option only on the primary and every Tor-retried fill
read raises `ArgumentsRequired` again — the defect surviving in the retry path, where it is hardest
to see. Both objects are in the diff.

### (b) THE REFUSAL IS KEPT, UNTOUCHED

Not one line of that branch changes. `_read_entry_fill` still returns `(None, None)` on a real read
failure; the caller still refuses to book, still writes `naked_position_alerts`, still sends ENTRY
FILL UNREADABLE, still raises. That mechanism was the only thing working correctly today — it is
what kept a fabricated position out of the book three times.

### (c) PROOF, ON TODAY'S REAL ORDERS

Read back read-only, no order placed:

```
=== 12ed23b7-2ac1-464b-bb0a-eef71e384d45   (08:50 entry — THE LIVE POSITION)
    fetch_order (AS SHIPPED)      RAISED ArgumentsRequired: bybit fetchOrder() can only access...
    fetch_order acknowledged=True filled=1.3  average=74.8   status='closed' cost=97.24  fee=0.09724
    fetch_closed_order            filled=1.3  average=74.8   status='closed' cost=97.24  fee=0.09724
    fetch_open_order              filled=1.3  average=74.8   status='closed' cost=97.24  fee=0.09724

=== bcf63671-...  (06:50 thread 1 — TWO executions, 0.3 + 1.0)
    fetch_order (AS SHIPPED)      RAISED ArgumentsRequired
    fetch_order acknowledged=True filled=1.3  average=74.79  status='closed' cost=97.227 fee=0.097227

=== 6e489d1f-...  (08:35 thread 1)
    fetch_order (AS SHIPPED)      RAISED ArgumentsRequired
    fetch_order acknowledged=True filled=1.3  average=74.85  status='closed' cost=97.305 fee=0.097305
```

And the exchange-level option proven with the **call site unchanged**:

```
A) AS SHIPPED  options={'defaultType':'future'}
   -> RAISED ArgumentsRequired
B) PROPOSED    options={'defaultType':'future','fetchOrder':{'acknowledged':True}}
   -> filled=1.3 average=74.8 status=closed fee=0.09724 cost=97.24
   raw orderStatus=Filled cumExecQty=1.3 avgPrice=74.8 cumExecFee=0.09724
```

`average=74.8` and `fee=0.09724` match the live position's own `avgPrice` and `curRealisedPnl`
exactly. The read works, and the partial-fill case (0.3+1.0) aggregates correctly to 1.3 @ 74.79 —
which is the case `_read_entry_fill` exists for.

---

## 3. FIX #2 — 34040 IS SUCCESS

The important mechanical detail: **34040 arrives as a ccxt *exception*, not as a `resp` dict**. The
shipped `retCode` check never sees it; the raw JSON is printed from the `except Exception as e`
branch. The fix therefore has to sit in **both** places, and it matches on the **parsed** retCode,
not a substring — `34040` can occur inside a millisecond timestamp in the same payload.

### (b) AUDIT OF EVERY OTHER BYBIT PATH — clean

- `set_leverage` 110043 "leverage not modified" → caught, printed as `warn`, execution continues.
  Already correct; both entries today logged it twice and neither was harmed.
- `_cancel_stop_orders` → `retCode≠0` prints a warn and does nothing else; its docstring already
  says "Safe to call even when no stop orders exist". Correct.
- `_cancel_open_orders_for_side` → per-order cancel in its own try/except, loop continues. Correct.
- **`_move_stop_to` is the only path where an idempotent repeat both returns `False` AND has a
  caller that acts destructively on it.**

Worth stating precisely: `_move_stop_to` is *shared* by breakeven and the recheck-tighten, so those
hit the same 34040 whenever the stop already sits at the target — but per its own docstring those
callers only **alert**. `_place_sl_with_retry` → `_sl_failsafe` is the single caller that **closes a
position**. That is why only the entry path lost money.

### (c) YES — AND A WARNING ABOUT SHIPPING IT ALONE

This fix alone prevents both of today's emergency closes. But look at what would have happened
instead: thread 2 gets `True` on attempt 1, takes the normal path, and hits the fill-read refusal —
leaving a **2.6** position open and unbooked instead of 1.3. **#2 without #3 converts a wrong close
into a bigger orphan. #2 and #3 must ship together.**

---

## 4. FIX #3 — THE ENTRY RACE

### (a) PROCESS-LOCAL IS SUFFICIENT — AND EXACTLY WHAT BREAKS IT

`workers = 1, threads = 4, gthread`. Every webhook thread that can race lives in **one interpreter**,
so a single `threading.Lock` sees all of them. That is why this is sufficient — and it is sufficient
*only* because of that number.

**What breaks it, and it is one line in a config file: raising `workers` above 1.** Each worker is a
separate **process** with its own lock dict; the lock would then guard nothing across workers while
still *looking* like protection. Same for a second bot instance or a manual script on the same
account. `gunicorn_mercury.conf.py` already carries a "keep workers=1" note for the monitor — this is
a second, independent reason, and the diff says so in the code.

The genuinely cross-process guard would be the DB unique index `ux_vpos_one_open_per_side`, which
cannot help today because it sits **downstream of the fill read that refuses first**.

Note the lock is taken **before** `_risk_check`, per your spec, and the reason is that the read is
what goes stale: at 06:50 the cap was read at `:02` and the order left at `:18` — **sixteen seconds**.
Locking only the order would let both threads read zero and then queue politely to place two.

### (b) THE SECOND THREAD IS REFUSED, NOT QUEUED

`acquire(blocking=False)` — that is the whole point. A queued duplicate is the same defect with a
delay: it would wake seconds later, having missed nothing but the price, and place the very second
order this exists to prevent. The losing signal is **discarded with a stated reason**, recorded as
`status='entry_gate_refused'` on its `trades` row, registered with the Skip-Attribution O.
like every other gate, logged, and sent to Telegram as DUPLICATE ENTRY REFUSED.

### THE ONE THING YOU SHOULD WEIGH BEFORE APPROVING

The `try:` wrapper requires **re-indenting main.py lines 3632-4165 (~534 lines) by four spaces**. No
statement changes; every `return jsonify` inside is a clean exit and `finally` releases on all of
them, including the `EntryFailSafeError` and generic-exception paths. I would verify with
`git diff -w` showing zero non-whitespace changes plus `py_compile` — except **this directory is not
a git repo**, so verification would be a diff against a `.bak_` copy instead. I am flagging it
because a 534-line reindent in a money path is exactly the kind of diff that hides a one-character
mistake. Your call whether you want it in this pass or want the handler tail extracted into a
function first.

---

## 5. THE OPEN POSITION — UNTOUCHED, AS ORDERED

1.3 SOL LONG @ 74.80, stop 73.89 live, uPnL +0.89, no DB row, no manager. Nothing in any diff above
adopts, closes, moves or books it. Awaiting your adoption decision.

---

## THE DIFFS

================================================================================
FIX #1 — THE FILL READ
================================================================================
--- a/main.py
+++ b/main.py
@@ -74,7 +74,32 @@
 _TOR_PROXY = 'socks5h://127.0.0.1:9050'
 exchange = ccxt.bybit({
     'apiKey': os.environ['BYBIT_API_KEY'],
     'secret': os.environ['BYBIT_API_SECRET'],
-    'options': {'defaultType': 'future'},
+    # ── 🔴 2026-08-08 — WHY 'acknowledged' IS SET HERE AND NOT AT THE CALL SITES ──
+    # ccxt 4.5.52's bybit.fetch_order() raises ArgumentsRequired CLIENT-SIDE, before
+    # the request is built, on any UNIFIED account without params['acknowledged'].
+    # This account IS Unified, so EVERY fetch_order in this file raised without ever
+    # reaching Bybit: no HTTP request, no retCode, nothing for tor_retry to retry.
+    # On 2026-08-08 that took all three live entries into the "refuse to book" branch
+    # (06:50, 08:35, 08:50) and left the 08:50 position on the venue with no row.
+    #
+    # SET AS AN OPTION, NOT A PARAM, BECAUSE THERE ARE FOUR CALL SITES AND A FIFTH
+    # EXCHANGE OBJECT. ccxt reads it via handle_option_and_params('fetchOrder',
+    # 'acknowledged'), so one line here fixes _read_entry_fill (1959), the entry fee
+    # read (2405), the close fee read (2703) and the partial fill read (2797) at once.
+    # Three of those four sit in `except: pass` blocks — they were failing SILENTLY
+    # and booking MODELLED fees instead of the venue's, which is why the close cards
+    # said "venue fee UNREADABLE" all day. A per-call-site param would fix whichever
+    # site was remembered and leave the rest.
+    #
+    # NOT fetchClosedOrder, AND THE REASON IS THE ENDPOINT, NOT THE NAME:
+    # ccxt's fetch_order → privateGetV5OrderRealtime (/v5/order/realtime), which is
+    # the endpoint the shipped code already meant to call. fetch_closed_order →
+    # /v5/order/history, a DIFFERENT, non-real-time endpoint. Every fill read in this
+    # file happens ~1s after its own order; realtime is the endpoint Bybit documents
+    # for exactly that, history is the one it documents for older records. Swapping to
+    # history to gain a nicer method name would trade a proven read for one that may
+    # not have propagated yet — a new way to reach the same refusal branch.
+    # The ccxt warning being acknowledged says the lookup covers the last 500 orders
+    # of any status. An order placed one second ago is inside that window by
+    # construction. MEASURED 2026-08-08 on three of today's real order ids — see the
+    # proof block in the session report; all returned filled/average/fee correctly.
+    'options': {
+        'defaultType': 'future',
+        'fetchOrder': {'acknowledged': True},
+    },
     'proxies': {'https': _TOR_PROXY, 'http': _TOR_PROXY},
 })

--- a/tor_retry.py
+++ b/tor_retry.py
@@ -44,7 +44,13 @@ def iso_exchange(exchange):
     cred = os.urandom(8).hex()
     iso_proxy = f'socks5h://{cred}:{cred}@127.0.0.1:9050'
     iso = ccxt.bybit({
         'apiKey': os.environ['BYBIT_API_KEY'],
         'secret': os.environ['BYBIT_API_SECRET'],
-        'options': {'defaultType': 'future'},
+        # 🔴 2026-08-08 — MUST MIRROR main.py's options. This object is what a
+        # 403-retry actually runs on, so an 'acknowledged' set only on the primary
+        # would fix the happy path and leave every Tor-retried fill read raising
+        # ArgumentsRequired again — the defect, surviving in the retry path only,
+        # where it is hardest to see.
+        'options': {'defaultType': 'future',
+                    'fetchOrder': {'acknowledged': True}},
         'proxies': {'https': iso_proxy, 'http': iso_proxy},
     })

  (b) THE REFUSAL IS UNTOUCHED. _read_entry_fill still returns (None, None) on a real
      read failure, the caller still refuses to book, still records naked_position_alerts,
      still sends ENTRY FILL UNREADABLE. Not one line of that branch changes.

================================================================================
FIX #2 — 34040 "not modified" IS SUCCESS
================================================================================
--- a/main.py
+++ b/main.py
@@ -1788,6 +1788,30 @@
+# ── 🔴 2026-08-08 — 34040 IS THE ANSWER TO AN IDEMPOTENT REPEAT, NOT AN ERROR ──
+_RETCODE_RE = re.compile(r'"retCode"\s*:\s*"?(\d+)"?')
+
+
+def _stop_already_at_price(err_or_resp) -> bool:
+    """True when Bybit answered 'not modified' (34040) — i.e. THE STOP IS ALREADY
+    AT THE REQUESTED PRICE.
+
+    /v5/position/trading-stop SETS a value; it does not append an order. Asking it
+    for the state it already holds is a no-op, and the caller's goal — "the stop is
+    at this price" — is SATISFIED. Bybit says so with retCode 34040 / "not modified",
+    which ccxt raises as an exception, so the shipped code read the venue's success
+    answer out of an `except` block and returned False.
+
+    WHAT THAT COST, 2026-08-08: two live positions emergency-closed for nothing. A
+    second webhook thread set the SAME stop the first thread had just set, got 34040
+    three times, and _place_sl_with_retry's None drove _sl_failsafe into a market
+    close of a FULLY PROTECTED position (06:50 −0.427895, 08:35 −0.415194).
+
+    Matched on the parsed retCode, NOT on a substring: '34040' can occur inside a
+    millisecond timestamp in the same payload.
+    """
+    if isinstance(err_or_resp, dict):
+        return str(err_or_resp.get('retCode')) == '34040'
+    m = _RETCODE_RE.search(str(err_or_resp))
+    return bool(m) and m.group(1) == '34040'
+
+
 def _move_stop_to(symbol, position_side, new_sl, *, label='move'):
@@ -1817,13 +1841,27 @@
             }), label=f'trading_stop.{label}')
+        # (a) NEVER SILENT. A future reader must be able to tell "I set it" from
+        # "it was already set" — those are different facts about the venue, and
+        # collapsing them is how a race becomes invisible.
+        if _stop_already_at_price(resp):
+            print(f"{LOG_PREFIX}[STOP-MOVE] {label} {position_side} ALREADY AT {px} "
+                  f"— venue returned 34040 not-modified; the stop is in the requested "
+                  f"state, counting as SET (no change was needed)", flush=True)
+            return True
         ok = resp.get('retCode') in ('0', 0)
         if not ok:
             print(f"{LOG_PREFIX}[STOP-MOVE] {label} REJECTED {position_side} -> {px}: "
                   f"{resp}", flush=True)
         return ok
     except Exception as e:
+        # THIS is the branch that actually fired on 2026-08-08 — ccxt raises on 34040
+        # rather than returning it, so the retCode check above never saw it.
+        if _stop_already_at_price(e):
+            print(f"{LOG_PREFIX}[STOP-MOVE] {label} {position_side} ALREADY AT "
+                  f"{new_sl} — venue returned 34040 not-modified; the stop is in the "
+                  f"requested state, counting as SET (no change was needed)", flush=True)
+            return True
         print(f"{LOG_PREFIX}[STOP-MOVE] {label} FAILED {position_side} -> {new_sl}: {e}",
               flush=True)
         return False

  (b) AUDIT — no other Bybit path counts an idempotent repeat as an error:
      • set_leverage 110043 "leverage not modified" (2244-2247) — caught, printed as
        `set_leverage warn`, execution CONTINUES. Correct already. Both entries today
        logged it twice and neither was harmed by it.
      • _cancel_stop_orders (1732) — cancel-all/StopOrder; retCode≠0 prints a warn and
        nothing else. Its docstring already states "Safe to call even when no stop
        orders exist (retCode=0)". Correct.
      • _cancel_open_orders_for_side (1718) — per-order cancel wrapped in its own
        try/except, loop continues. Correct.
      • _move_stop_to — THE ONLY path where an idempotent repeat both returns False
        AND has a caller that acts destructively on it. Fixed above.
      Worth stating: _move_stop_to is also used by breakeven and the recheck-tighten,
      so those hit the same 34040 whenever the stop is already at the target — but per
      its own docstring those callers only ALERT. `_place_sl_with_retry` → `_sl_failsafe`
      is the single caller that closes a position. That is why only entry lost money.

  (c) Confirmed: this fix ALONE prevents both of today's emergency closes. Thread 2 in
      each event would have gotten True on attempt 1, taken the normal path, and hit the
      fill-read refusal instead — leaving a 2.6 position open and unbooked. So #2 without
      #3 turns a wrong close into a bigger orphan. #2 and #3 must ship together.

================================================================================
FIX #3 — THE ENTRY RACE
================================================================================
--- a/main.py
+++ b/main.py
@@ -84,6 +84,34 @@
 _active_lock      = threading.Lock()
 _active_positions = {}
+
+# ── 🔴 2026-08-08 — PER-SIDE ENTRY GATE (the 06:50 and 08:35 double entries) ──
+# Two TradingView 5m webhooks landed in the same second, both LONG. gunicorn runs
+# workers=1, threads=4, gthread — so BOTH ran concurrently in ONE process. The
+# advisor's state cache deduplicated the MODEL CALL ("[STATE-CACHE] HIT/inflight")
+# but not the EXECUTION, so both threads carried decide='execute'. Both then ran
+# _risk_check, both read fetch_positions BEFORE either order had landed, both saw
+# zero open, both passed MAX_POSITIONS_PER_SIDE=1, and both sent a market order.
+# The venue netted them: 2.6 SOL where 1.3 was intended, twice.
+#
+# WHY A PROCESS-LOCAL LOCK IS SUFFICIENT *HERE*: workers = 1. Every webhook thread
+# that can race lives in the same interpreter, so one threading.Lock sees all of
+# them. WHAT WOULD BREAK IT — and it must be said out loud, because it is one line
+# in a config file: raising `workers` in gunicorn_mercury.conf.py above 1. Each
+# worker is a separate PROCESS with its own _entry_gates dict, and this lock would
+# then guard nothing across workers while still LOOKING like protection. The same
+# is true of a second bot instance or a manual script hitting the same account.
+# (gunicorn_mercury.conf.py already carries a "keep workers=1" note for the monitor;
+# this is a second, independent reason.) A cross-process guard would have to be the
+# DB — the ux_vpos_one_open_per_side unique index — which cannot help today because
+# it sits DOWNSTREAM of the fill read that refuses first.
+_entry_gate_guard = threading.Lock()
+_entry_gates      = {}          # (symbol, position_side) → threading.Lock
+
+
+def _entry_gate(symbol, position_side):
+    """The one lock serialising decide → order → book for a single side."""
+    key = (symbol, position_side)
+    with _entry_gate_guard:
+        gate = _entry_gates.get(key)
+        if gate is None:
+            gate = _entry_gates[key] = threading.Lock()
+    return gate

@@ -3631,7 +3659,29 @@
-    # Portfolio risk gate
-    risk_ok, risk_reason = _risk_check(symbol, position_side)
+    # 🔴 2026-08-08 — TAKE THE GATE *BEFORE* THE POSITION READ, NOT AROUND THE ORDER.
+    # The read is the thing that goes stale: at 06:50 the cap was read at :02 and the
+    # order went out at :18, sixteen seconds later. Locking only the order would let
+    # both threads read zero and then queue politely to place two.
+    _gate = _entry_gate(symbol, position_side)
+    if not _gate.acquire(blocking=False):
+        # (b) REFUSED, NOT QUEUED — blocking=False is the whole point. A queued
+        # duplicate is the same defect with a delay: it would wake up seconds later,
+        # having missed nothing but the price, and place the second order this exists
+        # to prevent. The signal that lost the race is DISCARDED, with a reason.
+        _reason = (f'concurrent {position_side} entry already in flight for {symbol} '
+                   f'— refused, not queued')
+        update_trade(row_id, status='entry_gate_refused', combo_key=combo,
+                     confluence_score=adj_score, error=_reason)
+        _record_skip_attribution(row_id, symbol, direction, 'entry_gate_refused',
+                                 matrix_result=matrix_result,
+                                 confluence_score=adj_score, ai_reason=_reason)
+        print(f"{LOG_PREFIX}[ENTRY-GATE] {_reason}", flush=True)
+        send_tg(f"🔒 <b>DUPLICATE ENTRY REFUSED</b>\n💎 {symbol}  {direction}\n"
+                f"<i>{_reason}</i>\n<code>{combo}</code>")
+        return jsonify({'status': 'entry_gate_refused', 'reason': _reason,
+                        'combo': combo}), 200
+    try:
+        # Portfolio risk gate
+        risk_ok, risk_reason = _risk_check(symbol, position_side)
         ...
         [lines 3632-4165 indented one level — MECHANICAL, no logic change]
         ...
         return jsonify({'status': 'success', 'order': entry['order'],
                         'combo': combo}), 200
+    finally:
+        # Released after BOOKING, not after ordering: _register_active_position and
+        # the virtual_positions insert both live inside this span, so the next thread
+        # cannot read a venue that has the position but a DB that does not.
+        _gate.release()

  SIZE OF THAT HUNK, STATED PLAINLY: the `try:` requires re-indenting main.py lines
  3632-4165 (~534 lines) by four spaces. No statement changes; every `return jsonify`
  inside is already a clean exit and `finally` releases on all of them, including the
  EntryFailSafeError and generic-exception paths at 4018/4035. I would verify with
  `git diff -w` showing ZERO non-whitespace changes in that range plus `python3 -m
  py_compile`. I am flagging the size because a 534-line reindent in a money path is
  exactly the kind of diff that hides a one-character mistake, and you should decide
  whether you want it in this pass or want the handler tail extracted into a function
  first.

--------------------------------------------------------------------------------
OPTIONAL THIRD HUNK — yours to accept or drop. NOT part of what you asked for.
--------------------------------------------------------------------------------
The lock stops two of OUR threads racing each other. It does not make the cap read
fresh: 16 seconds still separate _risk_check from the order, and in that window a
manual order, a second instance, or an adopted position can appear. A re-read inside
the gate, immediately before the order, closes that:

--- a/main.py
+++ b/main.py
@@ -2270,6 +2270,18 @@ def _execute_single_entry(...):
+    # 🔴 Re-read the cap INSIDE the gate, immediately before ordering. _risk_check's
+    # read is ~16s old by now. Fail-closed on UNKNOWN, matching _risk_check's own D1
+    # policy: an unverifiable cap buys no order.
+    _state, _ = _fetch_position_state(symbol, position_side)
+    if _state is not POS_FLAT:
+        raise RuntimeError(
+            f'venue is not FLAT for {symbol} {position_side} at order time '
+            f'(state={_state}) — refusing to add to a side we cannot account for')
     try:
         order  = tor_retry.with_socks_retry_write(

  Cost: one extra fetch_positions per entry. Benefit: the check-then-act becomes atomic
  against the venue, not just against our own threads. Drop it if you want this pass
  minimal — the three fixes stand without it.

================================================================================
NOT IN THIS PASS
================================================================================
• The open position: untouched. 1.3 SOL LONG @ 74.80, stop 73.89, unmanaged, awaiting
  your adoption decision. No line above adopts, closes, moves or books it.
• mercury-sol.service is STOPPED and still `enabled` — a host reboot would start it.
  Say the word if you want it masked while it sits.
