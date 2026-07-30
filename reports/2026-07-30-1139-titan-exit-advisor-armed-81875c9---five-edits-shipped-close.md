# TITAN exit advisor ARMED 81875c9 - five edits shipped, close-first ordering, 5m Group-B repointed

_2026-07-30 11:39 UTC_

---

### the off-switch was also the mute button — five edits shipped, advisor armed on a live position

**2026-07-30 11:32 UTC · `957f980` → `81875c9` · LIVE, REAL MONEY · vpos 86 open**

---

## DECISION LINE

**All five edits applied, plus the 5m Group-B repoint you asked for as a sixth. Committed `81875c9`,
pushed, service restarted deliberately at 11:32:45.** `EXIT_ADVISOR_DRYRUN = False`. The advisor can
now close a real position, and on the next `close` verdict it will.

**Your reasoning on the fifth edit is right and I have nothing to push back on.** Cancel-then-close
fails *certainly* whenever the close raises, and it has already cost real money here. Close-then-cancel
needs a ~1s coincidence, and the `_fetch_open_position` guard eliminates the common case before the
order is ever sent. **Trading a proven failure for an unproven one is correct when the proven one is
the worse of the two** — and the unproven one is unproven in the direction of a venue *rejection*,
not a venue *reversal*.

---

## YOUR THREE CONDITIONS, CONFIRMED FROM THE SHIPPED CODE

### 1. Emergency close is NOT collateral ✅

`breakeven_worker._emergency_close` calls:

```python
result = main._execute_close_position(symbol, position_side, _from_adapter=True)
```

**Unchanged — the reorder moved a block *inside* that function, not its signature or its routing.**
It still reaches the raw mechanics via `_from_adapter=True`, which remains mandatory: it fires before
the `virtual_positions` row exists, so engine-routing would find no row, return `None`, and leave a
real position open with no stop.

**Under the new ordering its behaviour is IDENTICAL, and here is why rather than an assertion:** it
fires precisely when the stop **failed to place**. There is therefore nothing for the cancel loop to
cancel — it is a no-op under the old ordering and a no-op under the new one. The only sub-case where
the two differ is when a *stale* order does exist, and there the new ordering is **strictly better**:
the close now happens before any cancel, so a failed close cannot strip a stop that was protecting
something.

### 2. The fetch guard still runs FIRST ✅

Proven by position inside the shipped `_execute_close_position` (line numbers relative to the
function):

```
39:  pos = _fetch_open_position(symbol, position_side)
41:      return None                      ← position closed between ticks: NEVER traded against
63:  order = exchange.create_market_order(...)      ← close sent, STOP STILL LIVE
69:  fee_cost = fetch_order_fee(order['id'], symbol)
78:  for o in exchange.fetch_open_orders(symbol):   ← cancel loop, NOW after the fill
87:          exchange.cancel_order(o['id'], symbol)
95:  _cancel_stop_orders(symbol, position_side)     ← second-pass orphan sweep
```

### 3. 5m Group B — **REPOINTED, not disabled.** I picked repoint. ✅

**Why repoint:** a dormant path is not a dead one. The failure mode of leaving it was a
*close-capable* trigger judging on a weaker prompt than the sample the criterion is built from —
which is precisely how this session's defects were seeded. Disabling would have removed the symptom
and left a `DRYRUN` reference stranded in a dead branch for the next reader to misinterpret.

**And repointing alone was not enough — that would have been a half-fix that created a NEW label
defect.** The path's close routes through `_execute_close_position(symbol, open_side)` with
`_from_adapter=False`, which engine-routes to `virtual_trader.close_position(...)` whose `reason`
defaults to **`'external'`**. An advisor close on that path would have been filed among manual and
exchange-side closes — invisible in exactly the cut the criterion is measured on. So:

- `_vpos` now falls back to `virtual_trader._open_position(symbol, open_side)` before consulting, so
  `consult_exit_advisor` (the enriched prompt, with the book block) is used — same as the other two.
- The unenriched `consult_for_close` survives **only** for the case it was always right for: no
  engine row exists at all.
- `_execute_close_position` gained an explicit `reason` parameter **defaulting to `'external'`**, so
  **no existing caller changes stamp**, and the AI branch passes `reason='ai_exit'`.

### On the label debt — kept, and documented as deliberate ✅

`trades.status` stays **`exit_ai_dryrun'** even when acting, exactly as you directed. §2.23 now says
in as many words that it is the name of the **channel**, not a claim about what happened; that
`virtual_positions.close_reason='ai_exit'` is the separable field every future cut should use; and
that a future reader who finds a consumer treating `exit_ai_dryrun` as *"the advisor did not act"*
should **fix the consumer**, or migrate all 77 rows and §2.4's query in one commit — **not rename it
for one new query.**

---

## APPLY SEQUENCE, AS RUN

| step | result |
|---|---|
| snapshot | `/root/backups/pre-exit-advisor-act-20260730-113107/` — `config.py` `virtual_trader.py` `main.py` **and `trades.db`** |
| apply | 3 files · **186 insertions, 35 deletions** |
| `py_compile` | **3/3 pass** |
| symtable FUNCTION-scope audit (the 29.07 guard) | **0 unresolved names across all three touched files** |
| import smoke test | flags read back correctly; `_advisor_says_close` / `_advisor_close` present and callable |
| guard truth table | `unavailable → False` · `None → False` · `hold → False` · `close → True` |
| commit | **`81875c9`** |
| push | **origin/main in sync** |
| restart | **deliberate, 11:32:45 UTC** |

**The guard truth table matters more than it looks:** `_advisor_says_close` returns `False` for an
`unavailable` verdict, for `None`, and for a malformed advice dict. **A missing answer is never read
as an instruction to trade.**

---

## POST-RESTART VERIFICATION — EVERY ITEM YOU LISTED

**🔴 LIVE banner at $150 — verbatim from the journal:**
```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
[TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
```

**Four boot gates green:**
```
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 1 exchange position(s), 1 open row(s)
[RECONCILE] boot reconciliation starting
[RECONCILE] engine owns positions — NOT enqueueing a breakeven job for SHORT (item 12a: single owner)
[RECONCILE] SHORT open, SL present @ 64767.1 — kept.
[RECONCILE] done
```

**Runtime = commit by hash — 8/8 MATCH:**
```
MATCH main.py 903d90ffb312   MATCH config.py 0e1d3e9167c5   MATCH virtual_trader.py 1815c98dd2e9
MATCH order_adapter.py 93dfcf32b6f8   MATCH claude_advisor.py 85d26cc0518b
MATCH breakeven_worker.py 87e39b3a2157   MATCH close_report.py d023a31ad8a5
MATCH microstructure.py 5ebbf1a4578d
proc start Thu Jul 30 11:32:45 2026 · sources newer than proc start: 0
```
The first three hashes **changed** from the pre-restart run (`9ab9c918…`, `de96898a…`, `841a1289…`)
and match the new commit — proof the process is running the patched code, not the old modules.

**vpos 86 — SAME exchange stop order id across the restart:**

| | before restart (11:31) | after restart (11:33) |
|---|---|---|
| position | SHORT 0.0023 @ 63686.0, posId `2082629807737368578` | **identical** |
| stop order | `2082629881359347712` STOP_MARKET BUY stopPrice 64767.1 `closePosition=true` | **identical, status NEW** |
| DB row | `86 open · stop_order_id 2082629881359347712` | **identical** |
| probes | unified + raw `swapV2` agree | **both agree, 1 position / 1 order** |

**The stop was not cancelled and not re-placed.** Balance `free 481.31 · used 29.30 · total 510.61`.

**Errors / breaker / Mercury:**

| check | result |
|---|---|
| errors · tracebacks · CRITICAL · `REFUSING TO START` since restart | **0** |
| circuit breaker | **untripped** (0 hits) |
| `NRestarts` | **0** |
| Mercury-SOL | **active, untouched** — up since 2026-07-21 06:39:33, `NRestarts=0` |

**The advisor timer survived the restart** — `exit_advisor_last_ts` lives in the row
(`pending_dca_limits`), not in memory: last consult 10:51:11, next due **11:51:11**. The restart did
not reset the hourly cadence and did not cause an extra consult.

---

## 🔴 NOT FINISHED — THE FIRST LIVE VERDICT HAS NOT FIRED YET

**This report is published now, with the work incomplete, because the code is committed and pushed.
A commit without a delivered link is an unclosed task.** The remaining item is an observation, not a
change.

| | |
|---|---|
| next hourly consult due | **11:51:11 UTC** (timer persisted in the row, survived the restart) |
| at time of writing | **11:38:49 UTC** — no consult since the restart, `vpos 86` still `open` |
| what will be appended | the verdict verbatim, and **if it says `close`, the full close sequence with the REAL fill price and the REAL fee read back from BingX** |

**It may not get there.** Price is ~64534 against a stop at 64767.1 — **0.155R away**. If the
exchange stop fires first, the position resolves as `reason='sl'` through passive-fill
reconciliation, the advisor never acts, and vpos 86 contributes **zero** datapoints to the new §2.4
rather than one. That outcome is recorded here in advance so it cannot be presented later as
anything other than what it is.

**Noted for the record, as you framed it and I agree:** the first advisor close will land on a
position already nearly resolved — worth perhaps $1.60. **It is a thin first datapoint and it counts
as exactly one.** Arming on a weak case beats waiting for a strong one, because the alternative is
another seven hours of correct verdicts that cannot act.

---

## WHAT CHANGED, IN ONE PLACE

| # | edit | file |
|---|---|---|
| 1 | `EXIT_ADVISOR_DRYRUN = False` + the comment rewritten to say it gates **acting only** | `config.py` |
| 2 | hourly gate reads `EXIT_ADVISOR_HOURLY` alone; acts on `close`; **returns immediately** so recheck/breakeven/trail/partial never touch a closed row | `virtual_trader.py` |
| 3 | 15m gate reads `EXIT_ADVISOR_ON_15M_CONFIRM` alone; same act path | `main.py` |
| 4 | **`_advisor_close`** — the only code that closes on an advisor's say-so | `virtual_trader.py` |
| 5 | 🔴 **close-first / cancel-after** in the shared close path | `main.py` |
| 6 | 5m Group B repointed to the enriched prompt; `reason='ai_exit'`; `_execute_close_position` gains `reason` (default `'external'`) | `main.py` |
| + | `'ai_exit'` counted by the batch callback; `[EXIT-ADVISOR-DRYRUN]` → `[EXIT-ADVISOR-LIVE]` when it can act | both |

**The conditional label, as shipped** — the journal cannot claim DRYRUN next to a real close:
```python
print(f"[EXIT-ADVISOR-{'DRYRUN' if EXIT_ADVISOR_DRYRUN else 'LIVE'}] "
      f"trigger={trigger} {symbol} {side} "
      f"close={advice.get('close')} conf={advice.get('confidence')} | ...")
```

---

## THE FOUR GUARDS, AS SHIPPED

**1 · CLOSE only — by construction, not by promise.** `_advisor_close` has one mechanic: `_do_close`
on an already-open row. **No entry call, no side flip, and no size argument anywhere on the path** —
`_do_close` closes the whole size in `filled_legs`. It cannot reverse because it never chooses a
side; it cannot resize because it never passes a quantity.

**2 · The stop is the backstop until the close confirms.** The stop is untouched until a fill comes
back. A raised `create_market_order` leaves the position open **and still protected**, with a loud
log and a Telegram alert. Residual stated, not hidden: the stop can trigger inside the close window;
`closePosition=true` means the venue has nothing to open with once size is zero — **expected but
UNPROVEN**, and accepted because the alternative is proven and worse.

**3 · One attempt per verdict — mechanically.** `exit_advisor_last_ts` is stamped **before**
`_advisor_close` is called, and unconditionally. A failed close sees a fresh timestamp on this tick
and every tick for the next 3600s. **A retry can only come from a NEW verdict, on fresh numbers.**

**4 · Distinct stamp.** `close_reason='ai_exit'`, new and unused. Existing: `sl` 30 · `trail` 18 ·
`external` 10 · `post_entry_critical` 1. **Separable in every future cut**, and now covering all
three triggers rather than two.

---

## THE FULL PATCH AS SHIPPED — `957f980..81875c9`

```diff
diff --git a/titan-bot/config.py b/titan-bot/config.py
index a07f0bb..d182806 100755
--- a/titan-bot/config.py
+++ b/titan-bot/config.py
@@ -235,10 +235,22 @@ LONG_PARTIAL_FRACTION = 1.0/3   # fraction of the position realised at that leve
 # empty in paper. PAPER_ENABLED fixes (b); ON_15M_CONFIRM supplies a trigger that
 # actually fires (~2.2/day); HOURLY adds a full trajectory per position, reusing
 # the smart-exit sampler which already collects the 48 fields the prompt needs.
-# DRYRUN short-circuits before every close mechanic: the advisor cannot close
-# anything regardless of verdict. SL / trail / armed-exit remain sole authority.
+# 🔴 DRYRUN NOW GATES **ACTING ONLY** — and that is itself the change (2026-07-30).
+# It used to gate CONSULTING as well, on the only two triggers that ever fire:
+#     virtual_trader.py  `if EXIT_ADVISOR_HOURLY and EXIT_ADVISOR_DRYRUN:`
+#     main.py            `if EXIT_ADVISOR_ON_15M_CONFIRM and EXIT_ADVISOR_DRYRUN:`
+# Setting this False on its own would therefore have SILENCED the advisor — no
+# consult, no verdict, no close — while arming the ONE close-capable path (5m
+# Group B) on a trigger that has never arrived in this bot's history (0 rows,
+# and the comment 8 lines above already said so). Those two gates now read their
+# own flags, which is what they were always named for.
+#
+# With DRYRUN=False a `close` verdict CLOSES: at market, through the adapter,
+# stamped reason='ai_exit'. It may only CLOSE — never open, never reverse, never
+# resize. The exchange STOP_MARKET stays the backstop and is cancelled only
+# AFTER the close confirms. ONE attempt per verdict; no retry loop.
 EXIT_ADVISOR_PAPER_ENABLED  = True   # paper mode: find the position in virtual_positions
-EXIT_ADVISOR_DRYRUN         = True   # record the verdict; the exit proceeds EXACTLY as today
+EXIT_ADVISOR_DRYRUN         = False  # 🔴 ACTING — a `close` verdict closes the position
 EXIT_ADVISOR_ON_15M_CONFIRM = True   # also consult on the 15m exit-confirm / 1H-arm triggers
 EXIT_ADVISOR_HOURLY         = True   # consult once per hour per open position (sampler cadence)
 EXIT_ADVISOR_HOURLY_SEC     = 3600   # cadence; mirrors SMART_EXIT_DRYRUN_SAMPLE_SEC
diff --git a/titan-bot/main.py b/titan-bot/main.py
index 49bf9cf..3ec601b 100644
--- a/titan-bot/main.py
+++ b/titan-bot/main.py
@@ -1178,7 +1178,8 @@ def _cancel_stop_orders(symbol: str, position_side: str):
         print(f"[STOP-CLEANUP] no orphaned orders for {position_side} {symbol}")
 
 
-def _execute_close_position(symbol, position_side, _from_adapter=False):
+def _execute_close_position(symbol, position_side, _from_adapter=False,
+                            reason='external'):
     """Cancel pending triggers/limits for the side, market-close the live
     position, and return a result dict. Mirrors the close mechanics in the
     legacy webhook() path so we keep the same hedge-mode behavior. Returns
@@ -1209,8 +1210,11 @@ def _execute_close_position(symbol, position_side, _from_adapter=False):
     # while its fills are real. The simulator returns the same dict shape (or
     # None when no open row exists), so downstream close paths are unchanged.
     if not _from_adapter and virtual_trader.engine_owns_position():
+        # `reason` defaults to 'external', which is exactly what every existing
+        # caller passed implicitly — so no current close path changes stamp. Only
+        # the AI branch of _handle_5m_close_via_ai overrides it, to 'ai_exit'.
         return virtual_trader.close_position(exchange, send_tg,
-                                             symbol, position_side)
+                                             symbol, position_side, reason=reason)
 
     pos = _fetch_open_position(symbol, position_side)
     if pos is None:
@@ -1218,10 +1222,38 @@ def _execute_close_position(symbol, position_side, _from_adapter=False):
     close_amount = float(pos['contracts'])
     close_side = 'sell' if position_side == 'LONG' else 'buy'
 
-    # Cancel any pending triggers (SL / trail / TP) and unfilled DCA limits
-    # for this side. BingX does not auto-cancel TRAILING_STOP_MARKET when
-    # the position closes via opposing market order — leaving them creates
-    # an orphan against a flat position. (Memory: project_bingx_bot.md)
+    # 🔴 CLOSE FIRST, CANCEL AFTER (2026-07-30). The cancel loop below used to run
+    # BEFORE this market order. That ordering is cancel-then-fail: if
+    # create_market_order raises — rate limit, a 109400-class rejection, a network
+    # blip — the protective STOP_MARKET is ALREADY GONE and a REAL position is
+    # left naked. That is the exact state this bot ate on 2026-07-29, and it sat
+    # latent on EVERY close path (sl, trail, armed exit, emergency), not just this
+    # one. The close is now sent while the stop is still on the exchange, so a
+    # failed close changes nothing: the position stays open and stays protected.
+    #
+    # RESIDUAL, STATED RATHER THAN HIDDEN: the stop can trigger during the close
+    # window. It carries closePosition=true, so the venue applies it to the whole
+    # remaining size and has nothing to open with once that is zero. That
+    # rejection is EXPECTED but still UNPROVEN (§7 uncertainty 1 — the stop has
+    # never fired). It is accepted because the alternative failure mode is a naked
+    # live position, which is strictly worse and has actually happened here.
+    ticker = exchange.fetch_ticker(symbol)
+    current_price = float(ticker['last'])
+
+    order = exchange.create_market_order(
+        symbol, close_side, close_amount,
+        params={'positionSide': position_side},
+    )
+    fill_price = float((order or {}).get('average')
+                       or (order or {}).get('price') or current_price)
+    fee_cost = (fetch_order_fee((order or {}).get('id'), symbol)
+                if (order or {}).get('id') else None)
+
+    # The position is now flat. Cancel this side's pending triggers (SL / trail /
+    # TP) and unfilled DCA limits. BingX does not auto-cancel
+    # TRAILING_STOP_MARKET when the position closes via an opposing market
+    # order — leaving them creates an orphan against a flat position.
+    # (Memory: project_bingx_bot.md)
     try:
         for o in exchange.fetch_open_orders(symbol):
             info = o.get('info') or {}
@@ -1238,18 +1270,6 @@ def _execute_close_position(symbol, position_side, _from_adapter=False):
     except Exception as e:
         print(f"order cleanup failed: {e}")
 
-    ticker = exchange.fetch_ticker(symbol)
-    current_price = float(ticker['last'])
-
-    order = exchange.create_market_order(
-        symbol, close_side, close_amount,
-        params={'positionSide': position_side},
-    )
-    fill_price = float((order or {}).get('average')
-                       or (order or {}).get('price') or current_price)
-    fee_cost = (fetch_order_fee((order or {}).get('id'), symbol)
-                if (order or {}).get('id') else None)
-
     # Post-close second-pass: wipe any stop/trigger orders that survived the
     # pre-close cancel loop (race conditions, BingX propagation delay, etc.).
     _cancel_stop_orders(symbol, position_side)
@@ -2673,8 +2693,10 @@ def consult_exit_advisor(vpos_row, symbol, side, exit_signal_name, trigger):
     entry side does (system prompt, user prompt, reason, confidence).
 
     This function has no access to any close mechanic and can never close a
-    position. Whether an exit happens is decided by the callers, and while
-    EXIT_ADVISOR_DRYRUN is True every caller returns before its close path."""
+    position. Whether an exit happens is decided by the callers: while
+    EXIT_ADVISOR_DRYRUN is True none of them acts on the verdict, and when it is
+    False they hand the verdict to virtual_trader._advisor_close, which is the
+    ONLY code in this bot that closes on an advisor's say-so."""
     ctx = _build_exit_context(dict(vpos_row), symbol, side, exit_signal_name, trigger)
     advice = claude_advisor.consult_for_close_rich(ctx)
     try:
@@ -2687,7 +2709,12 @@ def consult_exit_advisor(vpos_row, symbol, side, exit_signal_name, trigger):
                                          'close' if advice.get('close') else 'hold'))
     except Exception as e:
         print(f"[EXIT-ADVISOR] persist failed: {e}", flush=True)
-    print(f"[EXIT-ADVISOR-DRYRUN] trigger={trigger} {symbol} {side} "
+    # 🔴 THE LABEL MUST NOT LIE (2026-07-30). This line said DRYRUN unconditionally.
+    # Once the advisor can act, a log line claiming DRYRUN next to a verdict that
+    # is about to close a real position is the third instance of this bot's
+    # "the label does not say what it means" class. It now reports which it is.
+    print(f"[EXIT-ADVISOR-{'DRYRUN' if EXIT_ADVISOR_DRYRUN else 'LIVE'}] "
+          f"trigger={trigger} {symbol} {side} "
           f"close={advice.get('close')} conf={advice.get('confidence')} "
           f"| {(advice.get('reason') or '')[:200]}", flush=True)
     return advice
@@ -2770,7 +2797,18 @@ def _handle_5m_close_via_ai(parsed, symbol, signal_name, had_trend):
         except (TypeError, ValueError):
             pass
 
+    # 🔴 THE ENRICHED PROMPT ON EVERY PATH (2026-07-30, §2.23). This used to fall
+    # through to claude_advisor.consult_for_close — 6 fields, dollars, NO BOOK
+    # BLOCK — whenever `_vpos` was absent, which in LIVE mode is ALWAYS: the
+    # position is found via _fetch_open_position (the exchange), so the paper
+    # `_vpos` key is never set. The one close-capable trigger was therefore the
+    # only one judging on a poorer prompt than the 77 verdicts the activation
+    # criterion is cut from. It now asks the engine for its own row, exactly as
+    # the hourly and 15m triggers do. The unenriched call survives ONLY for the
+    # case it was always right for: no engine row exists at all.
     _vpos = (open_pos or {}).get('_vpos')
+    if _vpos is None:
+        _vpos = virtual_trader._open_position(symbol, open_side)
     if _vpos is not None:
         advice = consult_exit_advisor(_vpos, symbol, open_side, signal_name, '5m_group_b')
     else:
@@ -2820,9 +2858,13 @@ def _handle_5m_close_via_ai(parsed, symbol, signal_name, had_trend):
         return jsonify({"status": "ai_hold", "confidence": ai_conf,
                         "reason": ai_reason}), 200
 
-    # AI says close — run mechanics
+    # AI says close — run mechanics. reason='ai_exit' so this path is stamped
+    # identically to the hourly / 15m advisor closes: one advisor, one label, and
+    # `WHERE close_reason='ai_exit'` really means every advisor-driven exit. It
+    # was stamped 'external' before, which would have hidden it among manual and
+    # exchange-side closes in exactly the cut the criterion is measured on.
     try:
-        close = _execute_close_position(symbol, open_side)
+        close = _execute_close_position(symbol, open_side, reason='ai_exit')
     except Exception as e:
         err = str(e)
         update_signal_execution(row_id, status='close_failed', error=err,
@@ -3441,13 +3483,26 @@ def _handle_state_machine(data, action_field):
                 # operator's dedicated exit alert set and fires ~2.2x/day with a
                 # position open. Consulted here in DRYRUN only — the noop below is
                 # unchanged and remains the sole outcome.
-                if EXIT_ADVISOR_ON_15M_CONFIRM and EXIT_ADVISOR_DRYRUN:
+                # 🔴 THE GATE NO LONGER READS DRYRUN (2026-07-30) — same defect as
+                # the hourly gate: DRYRUN=False silenced the consult instead of
+                # arming it. DRYRUN is now read only where the verdict is ACTED on.
+                if EXIT_ADVISOR_ON_15M_CONFIRM:
                     for _s in ('LONG', 'SHORT'):
                         _vp = virtual_trader._open_position(symbol, _s)
                         if _vp:
                             try:
-                                consult_exit_advisor(_vp, symbol, _s, signal_name,
-                                                     '15m_exit_confirm')
+                                _adv = consult_exit_advisor(_vp, symbol, _s,
+                                                            signal_name,
+                                                            '15m_exit_confirm')
+                                if (not EXIT_ADVISOR_DRYRUN
+                                        and virtual_trader._advisor_says_close(_adv)):
+                                    # One attempt per verdict: each 15m signal is
+                                    # its own verdict, and _advisor_close never
+                                    # loops. A failure waits for the next signal.
+                                    _last = float(exchange.fetch_ticker(symbol)['last'])
+                                    virtual_trader._advisor_close(
+                                        exchange, _vp, _adv, _last, send_tg,
+                                        '15m_exit_confirm')
                             except Exception as _e:
                                 print(f"[EXIT-ADVISOR] 15m consult failed: {_e}", flush=True)
                 insert_signal(parsed, symbol, 'na', '15m_exit_confirm',
diff --git a/titan-bot/virtual_trader.py b/titan-bot/virtual_trader.py
index 20cae5b..49cfb51 100755
--- a/titan-bot/virtual_trader.py
+++ b/titan-bot/virtual_trader.py
@@ -1220,7 +1220,11 @@ def _do_close(exchange, row, close_price, reason, send_tg, _exit_fill=None):
     # intentionally unused: report.batch_line above is the richer block and is
     # set for ALL reasons. post_entry_critical IS a real outcome the optimizer
     # must see to learn poor entries, so it counts toward the cohort here.
-    if _batch_fn is not None and reason in ('sl', 'trail', 'post_entry_critical'):
+    # 'ai_exit' counts for the same reason post_entry_critical does: it is a REAL
+    # outcome on a REAL position, and an optimizer cohort that silently omitted
+    # every advisor exit would be scoring a strategy that no longer exists.
+    if _batch_fn is not None and reason in ('sl', 'trail', 'post_entry_critical',
+                                            'ai_exit'):
         try:
             _batch_fn(row_id=entry_row_id)
         except Exception as _bf_err:
@@ -2061,6 +2065,70 @@ def _record_smart_exit_dryrun(exchange, row, last, water_mark):
               f"— DRYRUN, position untouched", flush=True)
 
 
+def _advisor_says_close(advice):
+    """True ONLY for an explicit close verdict. A missing, failed or
+    'unavailable' consult is NOT a close — an absent answer must never be read
+    as an instruction to trade."""
+    return (bool(advice) and bool(advice.get('close'))
+            and advice.get('decide') != 'unavailable')
+
+
+def _advisor_close(exchange, row, advice, last, send_tg, trigger):
+    """THE EXIT ADVISOR'S ONLY HANDS. Close the whole open position, once.
+
+    CLOSE ONLY. There is no entry call, no side flip and no size argument
+    anywhere below: _do_close closes the WHOLE size recorded on the row. This
+    function cannot open, reverse or resize a position, by construction rather
+    than by promise.
+
+    THE STOP IS NOT TOUCHED HERE. The exchange STOP_MARKET remains the backstop
+    for the entire attempt — it is cancelled inside _execute_close_position only
+    AFTER the market close has returned a fill. If anything below raises, the
+    stop is still live on the exchange and the position is still protected.
+
+    ONE ATTEMPT PER VERDICT. The caller stamps exit_advisor_last_ts BEFORE
+    calling this, so a failure is never retried by the next 10s poll tick. The
+    next attempt can only come from the next VERDICT, on fresh numbers.
+    """
+    _reason = (advice.get('reason') or '')[:200]
+    _conf = float(advice.get('confidence') or 0.0)
+    print(f"[EXIT-ADVISOR-ACT] vpos={row['id']} {row['symbol']} "
+          f"{row['position_side']} trigger={trigger} conf={_conf:.2f} — CLOSING "
+          f"at market | {_reason}", flush=True)
+    try:
+        res = _do_close(exchange, row, last, 'ai_exit', send_tg)
+    except Exception as e:
+        # The close FAILED. The stop was never cancelled, so the position is
+        # still protected by it. Shout, and do NOT retry.
+        print(f"[EXIT-ADVISOR-ACT] 🔴 close FAILED vpos={row['id']}: {e} — "
+              f"position left OPEN, exchange stop still in place, NOT retried",
+              flush=True)
+        if send_tg:
+            try:
+                send_tg(f"🔴 <b>EXIT-ADVISOR CLOSE FAILED</b>\n"
+                        f"{row['symbol']} {row['position_side']} · vpos "
+                        f"{row['id']}\n<code>{e}</code>\n"
+                        f"Position left OPEN and the exchange stop is STILL the "
+                        f"backstop. Not retried — the next verdict decides.")
+            except Exception:
+                pass
+        return False
+    if res is None:
+        # market_close found no live position (already flat / stop just filled).
+        # The row is left for _reconcile_passive_fill. Not an error, not retried.
+        print(f"[EXIT-ADVISOR-ACT] vpos={row['id']}: no live position to close "
+              f"— left for passive-fill reconciliation, NOT retried", flush=True)
+        return False
+    if send_tg:
+        try:
+            send_tg(f"🤖 <b>EXIT ADVISOR CLOSED</b> ({_conf:.2f}) · {trigger}\n"
+                    f"{row['symbol']} {row['position_side']} · vpos {row['id']}\n"
+                    f"<i>{_reason}</i>")
+        except Exception:
+            pass
+    return True
+
+
 def _process_position(exchange, row, last, send_tg):
     """One position, one tick. Returns T. iff state changed (so caller can
     short-circuit logging). Single-entry model, mirroring the live
@@ -2143,23 +2211,39 @@ def _process_position(exchange, row, last, send_tg):
     # 1e) EXIT-ADVISOR hourly consultation (2026-07-26), DRYRUN only. Reuses the
     #     smart-exit sampler cadence — that sampler already collects the 48 fields
     #     the enriched prompt needs. Signal triggers alone give ~2.2 consultations
-    #     a day; hourly gives a full trajectory per position. Records a verdict and
-    #     NOTHING ELSE: this block has no close mechanic and cannot move a stop.
+    #     a day; hourly gives a full trajectory per position.
     #     main is imported lazily to avoid the circular import at module load.
-    if EXIT_ADVISOR_HOURLY and EXIT_ADVISOR_DRYRUN:
+    #
+    #     🔴 THE GATE NO LONGER READS DRYRUN (2026-07-30). It used to, so
+    #     EXIT_ADVISOR_DRYRUN=False silenced the consult instead of arming it —
+    #     this block produced 8 of the 9 clean `close` verdicts on vpos 86 and
+    #     would have stopped producing any. DRYRUN is now read ONLY below, where
+    #     it decides whether the verdict is ACTED ON.
+    if EXIT_ADVISOR_HOURLY:
         try:
             _st = mgmt_state.get('exit_advisor_last_ts')
             _now_ts = datetime.now(timezone.utc).timestamp()
             if _st is None or (_now_ts - float(_st)) >= EXIT_ADVISOR_HOURLY_SEC:
                 import main as _m
-                _m.consult_exit_advisor(row, row['symbol'], position_side,
-                                        'hourly review', 'hourly')
+                _adv = _m.consult_exit_advisor(row, row['symbol'], position_side,
+                                               'hourly review', 'hourly')
+                # THE TIMESTAMP IS STAMPED BEFORE THE CLOSE IS ATTEMPTED, and
+                # unconditionally. That is what makes 'one attempt per verdict'
+                # true: if the close below fails, this poll tick and every tick
+                # for the next hour see a fresh exit_advisor_last_ts and do not
+                # re-enter. A retry can only come from a NEW verdict.
                 mgmt_state['exit_advisor_last_ts'] = _now_ts
                 with sqlite3.connect(DB_PATH) as _c:
                     _c.execute("UPDATE virtual_positions SET pending_dca_limits=? "
                                "WHERE id=? AND status='open'",
                                (json.dumps(mgmt_state), row['id']))
                 changed = True
+                if not EXIT_ADVISOR_DRYRUN and _advisor_says_close(_adv):
+                    if _advisor_close(exchange, row, _adv, last, send_tg, 'hourly'):
+                        # The row is CLOSED. Everything below this point — the
+                        # recheck tiers, breakeven, the trail, the LONG partial —
+                        # would be operating on a position that no longer exists.
+                        return True
         except Exception as _e:
             print(f"[EXIT-ADVISOR] hourly consult failed vpos={row['id']}: {_e}", flush=True)
 
```

---

*Titan · 2026-07-30 11:40 UTC · HEAD `81875c9` · LIVE · vpos 86 open, verdict pending*
