# sol-phase3-preflip-diffs-for-approval

_2026-08-01 20:35 UTC_

---

# MERCURY-SOL — PHASE 3 DIFFS. **NOTHING APPLIED. STOPPED FOR APPROVAL.**

**No code changed.** `main.py` (19:26), `virtual_trader.py` (19:27), `tor_retry.py`,
`stop_loss.py`, `config.py`, `claude_advisor.py` untouched since Phase 2. SOL is PAPER, the entry
prompt and its inputs are frozen, the window stands at **4 of 200**, vpos 25 open and undisturbed.
Titan untouched. Only read-only queries were run.

---

# RISK ORDER, AND THE TWO INTERACTIONS THAT MATTER

| rank | item | why here |
|---|---|---|
| **1** | **§1 partial fill on entry** | poisons **every** downstream number — 1R, breakeven, the partial's ⅓, the close size |
| **2** | **§4 stop never re-verified** | the naked-position class; nothing notices until the stop fails to fire |
| **3** | **§5b risk gate reads the wrong number** | it is a *brake*, and the "safe direction" claim turns out to be false (below) |
| **4** | **§3 unchecked trail return** | a position with no trail — but the stop still protects, so lower |
| **5** | **§2 fee fallback to 0.0** | silent, biases every paper-vs-live comparison |
| **6** | **§5a duplicate armed-exit row** | accounting hygiene; §5b removes its worst consequence |
| **7** | **§6 arm consumed on a failed close** | a signal thrown away for a network reason |
| — | **§7 news gate** | decision only, no code |

## Interaction A — §1 must land with or before §4

`sl_price` is computed from `fill_price` (`compute_initial_sl`). §4 compares the exchange's
`stopLoss` against `sl_price`. If the entry booked a **fiction** (requested size, ticker price),
§4 would faithfully verify the stop against a level derived from that fiction — and report
"protected" while the real position sits at a different size and basis. **Fixing §4 without §1
makes §4 confidently wrong.**

## Interaction B — §5b supersedes §5a's worst consequence, and §2 feeds into §5b

§5b moves the brake off `trades` entirely and onto the position ledger, so the duplicate row
(§5a) stops mattering **to the risk gate** — which is the only place it was dangerous. §5a
remains worth fixing for other readers, but it drops out of the critical path.

Conversely, §5b makes `virtual_positions.net_pnl` the brake's input — and §2's fee handling feeds
`net_pnl`. **A fee we could not read now flows into a risk gate**, which is an argument for §2's
"modelled and labelled" option over "unverified and null".

---

# 🔴 A CORRECTION I OWE YOU ON §5b BEFORE THE DIFF

I told you at 18:05 that the double-count's error direction is **safe** — "a doubled loss halts
earlier, not later". **The data says that is not universally true, and one historical day proves
it.**

Daily PnL, current query vs the position ledger:

| day | trades sum (current) | ledger (truth) | difference |
|---|---|---|---|
| 2026-06-15 | +988.4012 | +494.2006 | +494.2006 |
| 2026-06-20 | −354.6823 | −177.3411 | −177.3411 |
| 2026-06-21 | −117.4233 | −58.7117 | −58.7117 |
| 2026-06-23 | +602.3124 | +301.1562 | +301.1562 |
| 🔴 **2026-07-16** | **−56.0379** | **−145.0391** | **+89.0012** |
| 2026-07-28 | −186.4866 | −93.2433 | −93.2433 |

**On 2026-07-16 the brake read a loss of −$56.04 when the truth was −$145.04.** The armed exit
that day was a **win** (+$89.00), and double-counting a win *offsets* real losses. The brake was
reading a **smaller** loss than reality — the **unsafe** direction, not the safe one. My earlier
statement covered the pure-loss case and I generalised it too far.

**Does it change any historical decision? No — and I checked rather than assumed.** Account
equity is **$811.90**, so the 5% limit is **$40.60**. All four losing days breach it under *both*
readings:

```
2026-06-20: current -354.68 (halt) | ledger -177.34 (halt)
2026-06-21: current -117.42 (halt) | ledger  -58.71 (halt)
2026-07-16: current  -56.04 (halt) | ledger -145.04 (halt)
2026-07-28: current -186.49 (halt) | ledger  -93.24 (halt)
```

**No historical brake decision changes.** But 07-16 shows the failure mode is real and present in
the data — it simply did not straddle the threshold. Had the true loss been −$45 with a doubled
+$89 win netting it to +$44, the brake would have stayed silent on a day it should have halted.

## 🔶 And a separate finding worth your attention

**The brake measures PAPER PnL against REAL equity.** Paper positions are `MARGIN 2000 × LEV 5 =
$10,000` notional; the account holds **$811.90**. So the 5% limit is $40.60 against a book whose
single positions move hundreds of dollars. **289 `risk_halt` rows exist.** Any paper loss day
larger than $40.60 halts entries for the rest of that day.

This is out of the scope you set — I am not changing it — but it means the paper book's entry
frequency is being shaped by a brake calibrated to a real balance it does not trade. It is a
plausible contributor to "barely trades" alongside the advisor's 97.7% refusal rate, and it
should be a conscious decision before the flip, not a discovery after it. **Not fixed, recorded.**

---

# §1 — PARTIAL FILL ON ENTRY (rank 1)

**Today** the position is booked from the *requested* amount and a price that falls back to the
pre-trade ticker:

```python
fill_price = float((order or {}).get('average') or (order or {}).get('price') or current_price)
# ... and `amount` (the REQUESTED size) is what gets recorded
```

```diff
+    # PHASE 3 (1): book the position from what the VENUE actually did, not from what
+    # we asked for. A partially-filled entry previously recorded a position the
+    # account does not have, and EVERY downstream number is derived from it — 1R
+    # (initial_risk_usdt), the breakeven level, the partial's 1/3 leg, and the close
+    # size. The partial primitive already reads its real fill; the entry did not.
+    filled_amt, avg_px = _read_entry_fill(order, symbol, want=amount,
+                                          fallback_px=current_price)
+    if filled_amt is None:
+        # Do NOT fabricate a position. The order may well have filled — we simply
+        # cannot substantiate it — so this is NOT a silent abort: the position is
+        # left to boot reconciliation, which reads the exchange and is the recovery
+        # path for exactly this state.
+        send_tg(f"🚨 <b>ENTRY FILL UNREADABLE</b> ({symbol} {position_side})\n"
+                f"The order was sent but its fill could NOT be read, so the position "
+                f"was NOT booked from a guess.\n"
+                f"<b>A position may be OPEN and UNSTOPPED.</b> Check the position and "
+                f"its stop on Bybit; the next restart will reconcile it from the "
+                f"exchange.")
+        raise RuntimeError(f'entry fill unreadable for {symbol} {position_side} '
+                           f'— refusing to book a fabricated position')
+    if abs(filled_amt - amount) > 1e-9:
+        print(f"{LOG_PREFIX}[ENTRY] PARTIAL FILL: requested {amount}, filled "
+              f"{filled_amt} — booking the FILLED size", flush=True)
+        send_tg(f"⚠️ <b>Partial entry fill</b> {symbol} {position_side}\n"
+                f"requested {amount}, filled {filled_amt} — position booked at the "
+                f"FILLED size; 1R, breakeven and the partial leg follow it")
+    amount     = filled_amt          # everything downstream now derives from reality
+    fill_price = avg_px
-    fill_price = float(
-        (order or {}).get('average') or (order or {}).get('price') or current_price
-    )
```

with the reader, which mirrors the partial primitive's contract:

```diff
+def _read_entry_fill(order, symbol, *, want, fallback_px):
+    """(filled_amount, average_price) from the VENUE, or (None, None) if it cannot
+    be substantiated. Never guesses a size.
+
+    A market order on Bybit is normally filled on return, so the common path costs
+    no extra call: `filled`/`average` are already on the order dict. Only when they
+    are missing do we re-read the order once.
+    """
+    o = order or {}
+    filled = float(o.get('filled') or 0) or None
+    avg    = float(o.get('average') or 0) or None
+    if filled is None or avg is None:
+        oid = o.get('id')
+        if not oid:
+            return None, None
+        try:
+            fetched = tor_retry.with_socks_retry(
+                exchange, lambda ex: ex.fetch_order(oid, symbol),
+                label='fetch_order.entryfill')
+        except Exception as e:
+            print(f"{LOG_PREFIX}[ENTRY] fill read FAILED ({e}) — NOT booking a "
+                  f"fabricated position", flush=True)
+            return None, None
+        filled = float(fetched.get('filled') or 0) or None
+        avg    = float(fetched.get('average') or 0) or None
+    if filled is None or filled <= 0:
+        return None, None
+    if avg is None or avg <= 0:
+        # Size is substantiated but the average is not. The size is the number that
+        # cannot be guessed; a price fallback to the pre-trade ticker is bounded and
+        # is what the code already did — but it is now LABELLED rather than silent.
+        print(f"{LOG_PREFIX}[ENTRY] filled {filled} but NO average price — using "
+              f"pre-trade ticker {fallback_px} as a LABELLED estimate", flush=True)
+        avg = float(fallback_px)
+    return filled, avg
```

**On a fill read that fails: do not fabricate, alert loudly, make it recoverable.** The raise
propagates to the existing `try/except` at the entry call site (`status='failed'` + alert), and
recovery is real rather than notional — `_load_active_positions_from_db`'s adoption path reads the
exchange at boot and imports a position that exists without a DB record. **That is precisely the
path Phase 2 kept alive for engine-owned rows** (it declines only when the engine already owns the
row; here it does not).

---

# §4 — RE-VERIFY THE STOP ON THE ENGINE'S TICK (rank 2)

**Adds no network call — confirmed.** The live branch of `_process_position` already calls
`_live_pos_state(symbol, position_side)` for the FLAT check, and that returns the **position
object**. The stop is a *field on it* (B1), so this is a read of data already in hand.

```diff
         if _st == 'FLAT':
             ...
+        if _st == 'OPEN':
+            # PHASE 3 (4): the stop was set at entry and never checked again. If it
+            # is cancelled, rejected late, or lost, nothing noticed until it failed
+            # to fire. Read the POSITION-LEVEL field (B1 — never an order list, or a
+            # protected position reads as naked) off the object we ALREADY have.
+            _ex_sl = None
+            try:
+                _raw = (_p.get('info') or {}).get('stopLoss')
+                _ex_sl = float(_raw) if _raw not in (None, '', '0') else None
+            except (TypeError, ValueError):
+                _ex_sl = None
+            if _ex_sl is None:
+                # 🔴 THE SERIOUS CASE: a live position with NO stop on the exchange.
+                # Treat it the way the entry fail-safe does — try to restore it, and
+                # if that fails, close rather than run naked.
+                print(f"{LOG_PREFIX}[STOP-VERIFY] vpos={vpos_id} has NO exchange stop "
+                      f"— restoring to {sl_price}", flush=True)
+                if _live_move_stop(symbol, position_side, sl_price, label='restore'):
+                    send_tg(f"🛡 <b>Stop RESTORED</b> {symbol} {position_side} → "
+                            f"{sl_price} (it was missing on the exchange)")
+                else:
+                    send_tg(f"🚨 <b>NAKED POSITION</b> {symbol} {position_side}\n"
+                            f"No stop on the exchange and it could NOT be restored. "
+                            f"Closing now rather than running unprotected.")
+                    return _exec_close(row, 'sl', last, send_tg)
+            elif abs(_ex_sl - sl_price) > max(1e-8, sl_price * 1e-6):
+                # Present but WRONG — e.g. a move_stop that failed earlier and was
+                # deliberately not retried silently. Re-set it and say so.
+                print(f"{LOG_PREFIX}[STOP-VERIFY] vpos={vpos_id} exchange stop "
+                      f"{_ex_sl} != intended {sl_price} — re-setting", flush=True)
+                if not _live_move_stop(symbol, position_side, sl_price, label='resync'):
+                    send_tg(f"⚠️ <b>Stop out of sync</b> {symbol} {position_side}\n"
+                            f"exchange {_ex_sl} · intended {sl_price} (WIDER side is "
+                            f"safe). Engine enforces {sl_price} while running; if the "
+                            f"bot restarts, protection reverts to {_ex_sl}.")
```

**Absence → restore, then close if restore fails.** That mirrors the entry fail-safe exactly:
a position that cannot be stopped must not run. **Mismatch → re-set and report**, never a silent
retry loop.

**Note for §3:** the same object also carries `trailingStop`, so once this lands a missing trail
becomes *detectable* on the tick. I have not wired that — §3 as you scoped it is the entry-time
return check — but it is the natural follow-on.

---

# §5b — THE RISK GATE READS THE POSITION LEDGER (rank 3)

```diff
-        with sqlite3.connect(DB_PATH) as conn:
-            row = conn.execute(
-                "SELECT COALESCE(SUM(pnl), 0) FROM trades "
-                "WHERE pnl IS NOT NULL AND DATE(timestamp) = DATE('now') AND exchange='bybit'"
-            ).fetchone()
-        daily_pnl = float(row[0] or 0.0)
+        # PHASE 3 (5b): ONE CLOSE, ONE ROW. This summed `trades.pnl` with NO
+        # is_virtual filter, over a table where every armed exit is stored TWICE
+        # (same order_id/price/amount/pnl) — so six days were double-counted. The
+        # direction is NOT reliably safe: on 2026-07-16 the duplicated row was a WIN
+        # (+89.00), so the brake read -56.04 against a true -145.04 — a SMALLER loss
+        # than reality, which is the direction that DELAYS a halt.
+        # virtual_positions is the position ledger: exactly one row per position,
+        # net_pnl already whole (partial leg folded back), no duplicates possible.
+        with sqlite3.connect(DB_PATH) as conn:
+            row = conn.execute(
+                "SELECT COALESCE(SUM(net_pnl), 0) FROM virtual_positions "
+                "WHERE status='closed' AND DATE(closed_at) = DATE('now')"
+            ).fetchone()
+        daily_pnl = float(row[0] or 0.0)
```

**Historical impact — checked, not assumed: no brake decision changes.** All four losing days
breach the $40.60 limit under both readings (table above). The fix removes a real hazard that
happened not to bite.

---

# §3 — CHECK THE TRAIL RETURN (rank 4)

```diff
-    tp_id = _place_trail_with_retry(symbol, market_id, pos_idx, trail_cb, active_price)
+    tp_id = _place_trail_with_retry(symbol, market_id, pos_idx, trail_cb, active_price)
+    if not tp_id:
+        # PHASE 3 (3): the return was assigned and never inspected, so a position
+        # could run with NO trailing stop while the DB still showed a trail_pct.
+        # DELIBERATELY NOT an emergency close: the STOP is the protection, the trail
+        # is the improvement. Closing a correctly-stopped position because an
+        # improvement failed is the wrong trade.
+        print(f"{LOG_PREFIX}[TRAIL] NOT SET after 3 attempts — position runs on the "
+              f"stop alone", flush=True)
+        send_tg(f"⚠️ <b>Trailing stop NOT set</b> {symbol} {position_side}\n"
+                f"The position IS protected — its stop-loss is on the exchange at "
+                f"{sl_price}. What is missing is the trail, so profit will not be "
+                f"ratcheted automatically.\n"
+                f"<b>You can:</b> set a trailing stop manually on Bybit, or leave it "
+                f"— the position will exit on its stop, the breakeven move, or an "
+                f"exit signal. No action is required for safety.")
```

The DB write is left recording `trail_pct` as computed, but the alert makes the divergence
visible. (Making the DB reflect the failure would mean the engine's own trail comparison stops
running too — and in live that comparison is the backstop, so it should keep running.)

---

# §2 — FEE FALLBACK (rank 5)

**Chosen: fall back to the MODELLED rate and LABEL it.** Reasoning:

- A `NULL` fee would satisfy "never indistinguishable from zero", but §5b now makes `net_pnl` the
  **risk gate's** input, and a NULL there propagates into a brake calculation. A modelled fee is
  approximately right; a null is a hole in a safety input.
- The modelled rate is the *same* `BYBIT_TAKER_FEE_RATE` the paper book charges, so live and paper
  stay comparable — which is exactly what the silent zero destroyed.
- The label makes it visible in analysis, which is the actual requirement.

```diff
+def _resolve_fee(order_fee, *, price, amount, label):
+    """Real fee when it could be read; otherwise the MODELLED fee, LABELLED.
+
+    PHASE 3 (2). `(fee_cost or 0.0)` booked a ZERO whenever fetch_order failed, so
+    live P&L read better than reality while paper always charged 0.055% — a silent
+    bias in every paper-vs-live comparison. A fee we could not read must never be
+    indistinguishable from a fee that was genuinely zero.
+    Returns (fee, verified: bool).
+    """
+    if order_fee is not None:
+        return float(order_fee), True
+    modelled = float(price) * float(amount) * BYBIT_TAKER_FEE_RATE
+    print(f"{LOG_PREFIX}[FEE] {label}: venue fee UNREADABLE — booking MODELLED "
+          f"{modelled:.6f} at {BYBIT_TAKER_FEE_RATE} (NOT verified)", flush=True)
+    return modelled, False
```

with a `fee_verified` column on `trades` (`INTEGER DEFAULT 1`, so history is unaffected) set to 0
on the modelled path, and the `(… or 0.0)` sites replaced by the resolved value. **Analysis can
then separate "fee = 0 because it was zero" from "fee = modelled because we could not read it".**

---

# §5a — ONE CLOSE, ONE ROW (rank 6)

The write fix — stop `_execute_armed_exit` inserting its own row when the engine has already
recorded the close:

```diff
+    # PHASE 3 (5a): ONE CLOSE, ONE ROW. _execute_armed_exit wrote its OWN
+    # '15m_armed_exit' row AND the close it triggered was recorded again by
+    # virtual_trader.close_position as an 'exit_{side}' VIRT-CLOSE row — same
+    # order_id, price, amount and pnl, since 2026-06-15. The engine's row is the
+    # authoritative one (it owns the position ledger), so this row is downgraded to
+    # a SIGNAL record: it keeps the armed-exit provenance and drops the duplicated
+    # money columns.
     update_trade(row_id, status='executed', price=result['fill_price'],
-                 amount=result['amount'], pnl=realized_pnl, fee=result['fee_cost'],
+                 amount=result['amount'],
+                 # pnl / fee deliberately NOT written — the VIRT-CLOSE row carries them
                  order_id=(result['order'] or {}).get('id'),
                  is_virtual=1 if OBSERVATION_MODE else 0)
```

Leaving `pnl` NULL is what removes it from every `SUM(pnl)` reader, including `optimizer.pair_trades`
(which requires `r['pnl'] is not None` on a close row) — so the engine's `exit_{side}` row becomes
the one that pairs, which is correct.

## 🔴 BACKFILL PLAN — shown, NOT executed, as instructed

Six rows: **2148, 3318, 3507, 4220, 10309, 13716**. All referenced in the 17:46, 18:05 and this
report.

| | |
|---|---|
| **Proposal** | `UPDATE trades SET pnl=NULL, fee=NULL WHERE id IN (…) AND signal_type='15m_armed_exit' AND order_id LIKE 'VIRT-CLOSE-%' AND pnl IS NOT NULL` |
| **Why NULL rather than delete** | the rows are cited by id in three published reports; deleting them would break those references. NULLing the money columns keeps the audit trail and removes them from every `SUM(pnl)`. |
| **Guard** | the `order_id LIKE 'VIRT-CLOSE-%'` clause means a genuine live armed exit can never be caught |
| **Backup** | a fresh `trades.db.bak_pre_5a_backfill_20260801` before touching anything |
| **Reversal** | the six prior values are already published in the 18:05 report and would be re-recorded in OPEN-ITEMS, so the change is exactly reversible |
| **Effect on §5b** | **none** — §5b reads `virtual_positions`, not `trades` |
| **Effect on the optimizer** | the `15m_armed_exit` row stops pairing (needs non-NULL pnl) and the sibling `exit_{side}` row pairs instead. **Same six positions, same six pairings, different row supplying it** |

**Not executed. Say the word separately and I will run it.**

---

# §6 — THE ARM SURVIVES AN UNKNOWN (rank 7)

**How the cases are distinguished:** `_execute_close_position` already separates them under Phase 1
— `POS_UNKNOWN` **raises**, `POS_FLAT` returns `None`, success returns a result dict. So the three
outcomes are already distinct at this call site; only the arm handling collapsed them.

```diff
     try:
         result = _execute_close_position(symbol, side)
     except Exception as e:
         err = str(e)
+        # PHASE 3 (6): an arm must NOT be consumed because the close failed for an
+        # UNKNOWN state. That is a signal discarded for a network reason. It IS
+        # consumed on a close that genuinely completed, and on a positive FLAT
+        # (nothing to close — the arm has no target).
+        if 'UNKNOWN' in err:
+            print(f"{LOG_PREFIX}ARMED_EXIT position state UNKNOWN — arm PRESERVED "
+                  f"for retry on the next confirmation within its TTL", flush=True)
+            update_trade(row_id, status='position_unknown', error=err)
+            send_tg(f"⚠️ <b>Armed exit deferred</b> ({side}) — position state "
+                    f"UNKNOWN. Nothing closed, <b>arm KEPT</b>; it will fire on the "
+                    f"next confirmation while its TTL lasts.")
+            return jsonify({'status': 'position_unknown', 'arm': 'preserved'}), 200
         update_trade(row_id, status='failed', error=err)
         send_tg(f"⚠️ <b>ARMED EXIT CLOSE ERROR</b> ({side})\n{err}")
         return jsonify({'status': 'error', 'message': err}), 500
 
-    # The arm is consumed no matter what happens next.
+    # Consumed: the close either completed or the exchange positively reported FLAT.
     state_machine.clear_exit_pending(side)
```

**Can an arm survive forever? No — and no new lifetime had to be invented.**
`state_machine.arm_exit_pending` already stamps `expires_at = now + EXIT_PENDING_TTL_MINUTES`,
and **`EXIT_PENDING_TTL_MINUTES = 360` (6 hours)** already exists. A preserved arm dies at its
existing expiry exactly as an unfired one does. **I am not proposing a new constant** — the
existing TTL is the answer, and it is unchanged.

The narrow behaviour change: an arm now survives a *Tor hiccup* instead of being discarded, and
still expires on the same 6-hour clock.

---

# §7 — THE NEWS GATE: SEQUENCING, WRITTEN DOWN BEFORE THE FLIP

**No code in this phase.** Restating precisely.

**Current state.** With the `is_virtual` labelling fixed and the six rows backfilled, the counter
`SELECT COUNT(*) FROM trades WHERE status='executed' AND (is_virtual IS NULL OR is_virtual=0)`
reads **0**, against `FUNDING_NEWS_OBSERVATION_TRADES = 30`. While it is below 30,
`_claude_news = None` and **news is withheld from 100% of entry prompts**. **While SOL is paper
the counter cannot move at all** — every engine row is stamped `is_virtual=1`.

**What happens in live.** Entry rows are `is_virtual=0`, and every close row written through
`insert_signal` is too. **Both legs of a round trip count.** So 30 is reached after roughly
**12 live round trips** — and at that moment the frozen entry prompt gains a
`Recent news (last 2h):` block **with no commit, no restart and no report**.

## The options and their cost

| option | cost | what it protects |
|---|---|---|
| **A — finish the 200-window before flipping** | slowest. At the observed rate (4 consultations in ~3h) the window is days away | the cleanest: the experiment completes on one prompt form, and the flip is a separate, attributable change afterwards |
| **B — pin `FUNDING_NEWS_OBSERVATION_TRADES` so it cannot open mid-window** | one constant. But it disables a designed behaviour by side-effect, and someone must remember to unpin — the class of thing that gets forgotten | lets the flip and the window overlap without the prompt changing under the experiment |
| **C — accept it and pre-register the prompt change** | the 200-window straddles two prompt forms, which is exactly what we restarted it at 17:13 to avoid | fastest to live; costs the experiment's cleanliness |

**My reading, for what it is worth:** **A** is the only one that costs nothing but time, and the
window is days rather than weeks. **C** re-creates by choice the precise defect we spent this
afternoon eliminating. **B** works but leaves a disarmed safety behind a constant.

**Your decision. I have written it down before the flip is on the table, which was the point.**

---

# 🛑 STOPPED

Nothing applied. `main.py` 19:26, `virtual_trader.py` 19:27 — unchanged since Phase 2. Service
running Phase 2 code, SOL **PAPER**, window **4 of 200**, vpos 25 open with its partial booked at
17:34:57, Titan clean (`3316e8a`, active, no `.py` modified).

**Say go and I apply in the risk order above — §1, §4, §5b, §3, §2, §5a-write, §6 — with
snapshots, `py_compile`, a deliberate restart and the full confirmation set. §5a's backfill and
§7's decision stay separate and wait for you.**
