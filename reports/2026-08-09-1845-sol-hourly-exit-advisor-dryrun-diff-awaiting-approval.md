# sol-hourly-exit-advisor-dryrun-diff-awaiting-approval

_2026-08-09 18:45 UTC_

---

# The hourly exit advisor, ported to Mercury-SOL in DRYRUN. **DIFF ONLY — NOT APPLIED, NOT RESTARTED.** Awaiting your decision.

**Production is untouched. Nothing was edited, nothing restarted.** The only write to the
Mercury-SOL directory is the four `.bak` files you asked for, each md5-verified identical to the
live file. The port itself was built and proven in an isolated copy.

```
PROOF BY EXECUTION: 37 assertions, 0 failed.  LEAKS: 0.  exit 0.
18 vectors rewritten by DIRECTORY (17 .py + .env). 0 residual prod-path literals.
config.py +26 −0 · claude_advisor.py +70 −0 · main.py +132 −0 · virtual_trader.py +36 −0
🔴 ZERO DELETED LINES IN ALL FOUR FILES — the port is a pure addition.
```

🔴 **ONE THING I FOUND THAT CHANGES THE SHAPE OF THE PORT, AND YOU SHOULD SEE IT BEFORE APPROVING.**
SOL's existing `consult_for_close` is the **legacy 6-field prompt** — Titan's own comment calls it
*"6 fields, dollars, NO BOOK"*. It states unrealised PnL **in dollars** and age **in minutes**, and
it states **no stop, no trail, no MFE and no giveback**. Those are three of the four quantities
Titan's verdict is actually coupled to (giveback ρ=+0.523, upnl_r ρ=−0.448, stop_away_r ρ=−0.434).

**Hooking that prompt to an hourly timer would have measured an advisor with its eyes shut** — and
would not have reproduced Titan's result even if the mechanism works. So the port adds a **new
ledger-derived prompt** rather than reusing the legacy one. The legacy `consult_for_close` and its
5m Group-B path are **untouched, byte for byte**.

Prior: [18:30 — why it never ran](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1830-sol-why-the-exit-advisor-never-ran.md)

---

## 1. THE PORT

### (b) The flags, with the reasoning at the constant

```python
EXIT_ADVISOR_DRYRUN     = True   # 🔴 OBSERVE ONLY. No verdict reaches any close path.
EXIT_ADVISOR_HOURLY     = True   # consult once per hour per OPEN position
EXIT_ADVISOR_HOURLY_SEC = 3600
```

The comment block carries the argument on the record — that DRYRUN stays True because **SOL is the
only place in this project where the trail runs on live money**, that an acting advisor would
destroy that measurement on the strength of Titan's n=7, and that Titan itself ran DRYRUN from
2026-07-26 to 07-30 before letting a single verdict close anything.

### (a) It piggybacks the existing hook — no second timer

The consult sits in the **same poll tick**, immediately after the smart-exit sampler that already
runs on the same 3600 s period. One tick, one place. The two throttles are independent but share a
period, so no second timer is introduced on a position — the double-manager class this project
keeps closing.

```diff
@@ -1926,6 +1928,40 @@
         except Exception as e:
             print(f"[MERCURY-SOL] smart-exit dryrun failed vid={vpos_id}: {e}", flush=True)
 
+    # 1f) 🔴 HOURLY EXIT-ADVISOR CONSULT (2026-08-09) — DRYRUN, OBSERVE ONLY.
+    #     PIGGYBACKS THE SAMPLER'S HOOK, ON PURPOSE. This sits in the same poll
+    #     tick, immediately after the smart-exit sampler that already runs on the
+    #     same 3600s period, rather than introducing a second timer on one
+    #     position — the double-manager class this project keeps closing. One
+    #     tick, one place; the two throttles are independent but share a period.
+    #
+    #     🔴 THE VERDICT GOES NOWHERE. It is recorded and DISCARDED. There is no
+    #     branch below that reads `_adv`, and consult_exit_advisor itself holds no
+    #     close mechanic. Flipping EXIT_ADVISOR_DRYRUN to False changes NOTHING on
+    #     its own — acting would need a new call to a close path that does not
+    #     exist in this file. That is deliberate: a flag that silently arms a live
+    #     close is how a "dryrun" stops being one.
+    #
+    #     Best-effort, double wrapped, and the timestamp is stamped BEFORE the call
+    #     so a failure cannot re-enter every tick for an hour. It adds NO venue
+    #     call: `last` and `water_mark` are already in hand for this tick.
+    if EXIT_ADVISOR_HOURLY:
+        try:
+            _ea_last = mgmt_state.get('exit_advisor_last_ts')
+            _ea_now = datetime.now(timezone.utc).timestamp()
+            if _ea_last is None or (_ea_now - float(_ea_last)) >= EXIT_ADVISOR_HOURLY_SEC:
+                mgmt_state['exit_advisor_last_ts'] = _ea_now
+                with sqlite3.connect(DB_PATH) as _c:
+                    _c.execute("UPDATE virtual_positions SET mgmt_state_json=? "
+                               "WHERE id=? AND status='open'",
+                               (json.dumps(mgmt_state), vpos_id))
+                import main as _m          # lazy: avoids the module-load cycle
+                _m.consult_exit_advisor(row, row['symbol'], position_side, last,
+                                        trigger='hourly')
+        except Exception as e:
+            print(f"[MERCURY-SOL] exit-advisor hourly failed vid={vpos_id}: {e} "
+                  f"— position untouched", flush=True)
+
     # 1c) Post-entry multi-tier recheck (T+10/60/300s, A16 Titan parity).
```

The other three hunks add `_build_exit_ctx_from_ledger` and `consult_exit_advisor` to `main.py`,
`consult_for_close_state` plus its own system prompt to `claude_advisor.py`, and the three flags to
`config.py`. **Full unified diff: 306 lines, all additions.**

### (c) 🔴 THE VERDICT REACHES NOTHING — proven four ways, not by reading the flag

```
✅ exactly ONE call site in the poller                                    1 found
✅ its result is DISCARDED (a bare expression, never assigned)            parent node = Expr
✅ Titan's acting helper '_advisor_says_close' does NOT exist on SOL      []
✅ Titan's acting helper '_advisor_close'      does NOT exist on SOL      []
```

**And then by execution — a stub returning `close: True, confidence: 0.99` was driven through the
shipped hook lines:**

```
✅ the hook DID consult (the stub was reached)
✅ 🔴 a CLOSE verdict left EVERY protected field untouched     changed: none
✅   the trail state survives (breakeven_applied unchanged)
✅   the partial state survives (partial_done unchanged)
✅   the ONLY mgmt change is the throttle stamp                added ['exit_advisor_last_ts']
✅ a second tick within the hour does NOT consult again
```

Position state before and after a **CLOSE** verdict:

```
before mgmt: {"breakeven_applied": true, "partial_done": true}
after  mgmt: {"breakeven_applied": true, "partial_done": true,
              "exit_advisor_last_ts": 1786300332.818738}

protected fields compared: size, sl_price, water_mark, status, close_price, close_reason,
  net_pnl, initial_fill_price, original_sl_price, trail_pct, partial_size, partial_price,
  partial_pnl, partial_fees, max_adverse_price, is_paper, fills_json
CHANGED: none
```

🔴 **The stronger guarantee, and the one I would rely on: flipping `EXIT_ADVISOR_DRYRUN` to False
changes NOTHING by itself.** There is no branch that acts on the verdict, and `_advisor_close` — the
function that does the closing on Titan — **does not exist in SOL's tree at all.** Arming this
would require writing a new call to a close path, deliberately. A flag that silently arms a live
close is how a dryrun stops being one, and this one cannot.

🔶 **An honest note about my own harness:** the first re-run showed 4 failures. The cause was the
lab database still carrying `exit_advisor_last_ts` from the previous run, so the throttle correctly
refused a second consult. That is the throttle working, not a defect — but it means the harness must
reset the lab DB between runs, and I am recording it rather than quietly rebuilding.

---

## 2. 🔴 THE PROMPT — RENDERED FOR THE FIRST TIME, AGAINST vpos 30 AS IT STANDS

**No model call was made.** `_call` was stubbed and the exact f-string captured.

```
----- SYSTEM PROMPT -----
You are an automated trading decision module. You are reviewing an OPEN position on a
scheduled hourly check — NO new signal has arrived. Decide whether to close it now or hold
it (the bot's on-exchange stop and its trailing stop still protect the downside if you hold).

Every number you are given is measured from this position's own ledger: R is expressed
against the ORIGINAL stop distance, the high-water mark is the best price the position has
actually seen, and giveback is how much of that peak has been handed back. Judge the
position on those figures.

Respond with ONLY a single JSON object, no markdown, no prose. Fields: close (true|false),
confidence (float 0.0-1.0), reason (string, max 160 chars).

----- USER PROMPT -----
OPEN POSITION — decide CLOSE or HOLD.

Position
  Side: LONG   Entry: 76.29   Now: 77.28
  Unrealised: +1.12R   (1R = the ORIGINAL stop distance, 0.8800)
  Elapsed: 21.4h
  Current stop: 76.44258  ->  +0.95R away   (breakeven lock APPLIED)
  Peak so far (MFE): +1.37R   Giveback from peak: 0.25R

Trail
  The trailing stop is ARMED (this position reached +1R).
  It exits at 76.8296 = the high-water mark 77.5 less 0.865% of it.
  That is 0.58% below the price now.

Partial
  0.4 already realised at 77.25; 0.9 remains open.

EVERY figure above is computed from this position's own ledger row; `Now` is the last traded
price this poll tick.
Consultation trigger: hourly review (no signal fired).

Decide whether to close the remaining size now or hold it.
```

### (b) Checked against the failure classes already found on Titan

```
✅ states elapsed time                    ✅ states the giveback
✅ states the current stop                ✅ states the MFE
✅ states the trail armed state           ✅ names the R basis explicitly
✅ says NO signal fired (the hourly trigger is not a webhook)
✅ the system prompt does NOT claim a TradingView signal arrived
```

🔴 **That last one is a defect I had to fix rather than inherit.** The existing `_CLOSE_SYSTEM`
opens with *"A management/exit signal has arrived from TradingView while a position is open"*. On an
hourly review **no signal has arrived**, so reusing it would open every single consult with a
statement that is false — the exact class this week has been spent removing from the entry prompt.
The port adds a separate `_CLOSE_STATE_SYSTEM` and leaves `_CLOSE_SYSTEM` untouched for the 5m
Group-B path, where its wording is true.

**On Titan's trail-clause history:** its clause did not exist before 2026-07-29 and its arithmetic
is now clean (59/59 consistent, 58/58 on the arm level). SOL's clause is present from the first
consult and states the armed condition, the exit level, its derivation and its distance.

### (c) 🔴 EVERY NUMBER RECOMPUTED FROM THE ROW — one source, no second judge

```
✅ Unrealised R matches (last-entry)/risk           expected +1.12R
✅ MFE R matches (water_mark-entry)/risk            expected +1.37R
✅ Giveback matches MFE - uPnL                      expected 0.25R
✅ stop distance matches (last-stop)/risk           expected +0.95R
✅ trail trigger matches water_mark*(1-trail_pct)   expected 76.8296
✅ 1R is the ORIGINAL stop distance, not the moved one
     risk_px=0.8800 from original_sl 75.41, NOT the breakeven stop 76.44258
✅ the ONLY non-ledger field is `Now`, and the prompt says so
```

**The one field that is not from the ledger is `Now` — the last traded price the poller already
holds for this tick — and the prompt names it as such in its own text.** Everything else is
`virtual_positions` row 30 and nothing else. There is no order book, no percentile baseline and no
second opinion on any quantity, so a claim can always be checked against the row that produced it.
That is the design answer to "one fact, many judges": there is only one fact-source.

🔴 **One deliberate choice worth your eye: R is measured against `original_sl_price`, never the
current stop.** The current stop MOVED when breakeven locked (75.41 → 76.44258). An R that silently
re-bases mid-position is the same defect class as a fee that re-bases, and it would have made every
figure in this prompt incomparable with every figure in the book.

---

## 3. COST AND FAILURE MODES

### (a) One call per open position per hour

```
MAX_POSITIONS_PER_SIDE = 1, two sides  ->  at most 2 concurrent consults per hour
one position open continuously          ->  24 / day, ~730 / month
vpos 30 (open 21.4h)                    ->  21 consults would already exist
```

SOL's actual position-time is well below continuous: 22 paper closes over ~60 days, and 2 live
positions in 2 days. **A realistic figure is well under 730/month**, but 730 is the ceiling and the
ceiling is what should be budgeted.

### (b) 🔴 IT CANNOT BLOCK, DELAY OR ALTER THE POLLER TICK

All three failure modes driven through the shipped code:

```
✅ the model call RAISES (Tor timeout, HTTP error): the poller tick survives
✅    and the position is untouched
✅ the advisor returns None:                        the poller tick survives
✅    and the position is untouched
✅ the advisor returns malformed JSON (a bare string): the poller tick survives
✅    and the position is untouched
```

`[MERCURY-SOL] exit-advisor hourly failed vid=30: tor timeout — position untouched`

Three layers: `consult_for_close_state` returns an `unavailable` dict on a bad response rather than
raising; `consult_exit_advisor` wraps everything and returns `None`; the poller hook wraps *that*
and logs. **And the throttle stamp is written BEFORE the call**, so a hang or a failure cannot
re-enter on the next tick — it waits a full hour, exactly as Titan's does.

🔶 **The one honest residual: latency.** The call is made **inline on the poller thread**, as
Titan's is. A slow LLM response delays that position's next tick by the call duration — the tick
cadence is ~12 s and the trail is evaluated on the next tick. It does not *alter* anything and it
cannot touch the stop, which is resting on the venue and independent of the process, but a
multi-second stall once an hour is real and I am naming it rather than claiming zero impact.

### (c) No venue call added

```
✅ the hook makes NO venue call   none — last/water_mark already in hand
```

`last` and `water_mark` are already computed for this tick, and the context builder reads only the
row it was handed. **Zero Bybit calls, zero Tor load.** The only new outbound traffic is the
Anthropic API call itself.

---

## 4. THE BOUNDARY

```
🔴 THE FIRST SOL EXIT-ADVISOR CONSULT OPENS A NEW MEASUREMENT ERA.

BEFORE it:  SOL's exit advisor has NEVER executed. Zero consults, ever. Every closed
            position in SOL's book — 22 paper, 1 live — was decided by the trail, the exit
            signal or the stop with NO advisory verdict in existence for it.
AFTER  it:  every open position carries hourly verdicts recorded alongside the mechanism
            that actually acts.

NOTHING BEFORE THE FIRST CONSULT MAY BE POOLED WITH ANYTHING AFTER IT in any study of exit
behaviour — not because the bot's behaviour changes (in DRYRUN it does not), but because the
POPULATION changes: before, a "no verdict" position is unobserved; after, it is observed and
held anyway. Treating those as the same cohort would read an observation gap as a decision.

This is the fourth boundary in SOL's book and they must not be conflated with one another:
   taker fee   vpos <=29 / >=30
   ADX window  vpos <=28 / >=29
   funding     every closed row so far is NULL; first booked at the next close
   exit advisor  first consult onward   <- THIS ONE
```

---

## PROOF BY EXECUTION — 18 VECTORS, SEARCHED BY DIRECTORY

```
LAB: full tree copy from the PORTED source. Every prod-directory literal rewritten.
  residual "/mnt/volume_nyc1_1780480650620/mercury-sol" literals : 0
  residual "/root/titan-bot" literals                            : 0
  files rewritten : 17   + .env  => 18 VECTORS

LOCK (installed first, never lifted):
  sqlite3.connect      -> raises on any path under PROD or /root/titan-bot
  open(mode=w/x/a/+)   -> same
  sys.dont_write_bytecode = True
  the Telegram sender replaced by a stub that RAISES if called

RESULT: 37 assertions ✅  0 ❌  LEAKS: 0  exit 0

AST vs production:
  config.py          added=[]  removed=[]  changed=[]      (constants only)
  claude_advisor.py  added=['consult_for_close_state']  removed=[]  changed=[]
  main.py            added=['_build_exit_ctx_from_ledger','consult_exit_advisor']
                     removed=[]  changed=[]
  virtual_trader.py  added=[]  removed=[]  changed=['_process_position']
```

🔴 **Only ONE existing function changes anywhere: `_process_position`, the poller tick, by the added
block.** `consult_for_close`, the 5m Group-B path, the trail, the breakeven lock, the partial, the
stop and every geometry constant are **byte-identical**.

**Backups `*.bak_exitadvisor_hourly_20260809_1845` for all four files, md5-verified identical to the
live files.** They are the only write to the Mercury-SOL directory in this pass.

---

## 🔴 STOPPED FOR APPROVAL — NOTHING IS APPLIED

```
$ find . -name "*.py" -newer <the 17:42:52 restart>
  (empty — production is exactly as the running worker loaded it)

mercury-sol   active · master 4037477 / worker 4037550 · since 17:42:38 · NOT restarted
vpos 30       OPEN · 0.9 @ 76.29 · sl 76.44258 · wm 77.50 · untouched
titan         active · pid 2538048 · HEAD 897850b · NOT TOUCHED, not read from by hand
```

**To land it:** copy the four files from the reviewed source and restart from flat, or accept a
restart with vpos 30 open on the same reasoning as the 17:42 one — the boot reconciler reads the DB
and the stop is a position-level attribute that survives the process. **That is your call and I have
not made it.**

**What I would still flag before you decide:** this adds an hourly LLM call to a live bot's poller
thread, on the strength of Titan's n=7. The measurement case is in the 18:30 report and I stand by
it — verdict-level evidence in ~2 weeks against close-level evidence months away — but *"not now,
the book is too young"* remains a defensible reading of the same numbers, and approving this is a
decision to spend a little latency and a little money to buy that measurement early.
