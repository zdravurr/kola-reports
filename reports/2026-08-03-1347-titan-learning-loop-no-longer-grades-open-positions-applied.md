# titan learning loop no longer grades open positions applied ca90c2f

_2026-08-03 13:47 UTC_

---

# TITAN — THE LEARNING LOOP NO LONGER GRADES OPEN POSITIONS · APPLIED, LIVE, `ca90c2f`

_2026-08-03 · HEAD `ca90c2f` (was `3316e8a`) · LIVE, real money · one file changed, nine proofs by execution_

---

## DECISION LINE

**Applied and running.** `signal_weights.audit_pending` now requires the position to be **closed**
before a trade is graded, and `_evaluate_trade_pnl` **refuses** instead of inventing an outcome.
`AUDIT_MAX_AGE_HOURS` 24 → 96, because requiring closure would otherwise have silently thrown away
every long hold. **One file, 86 insertions, 54 deletions. The trade path is byte-identical.**

🔴 **The defect was four times larger than §2e of the 13:30 report said.** That report found the
*live* symptom — the unrealized-P&L fallback. Tracing the same function's other branch found the
paper-era symptom, and it is the dominant one:

> `_evaluate_trade_pnl` looked the position up on the **exchange**. In PAPER mode there has never
> been an exchange position to find, so it fell to `return 0.0, 'closed_unknown'` and graded the
> trade **zero**. That branch fired on **44 of the 65 engine-owned entries**, and **32 of those 44**
> had a realised outcome that the store's own +20 / −15 thresholds call a **win or a loss** — trade
> 19021 graded **0.0** against a realised **−143.67**; trade 10369 graded **0.0** against **+370.45**.

**Total: 47 of 65 entries (72%) were graded while their position was still open. The weight store
has been learning from 18 trades — only the ones that happened to close inside the 2-hour grace.
That is a sample selected for FAST closers, which is not a neutral subsample of anything.**

🔴 **vpos 91 closed while this work was in progress, and it settled the question by outcome rather
than by projection.** The exit advisor closed it at **13:41:07 UTC, net −0.6410**. Its grade,
written at 08:48:51 while it was open, is **+0.5015 — a WIN**. **The sign is inverted, confirmed.**
And because `audit_score IS NULL` is the queue predicate, that row is now **permanently stuck at
the wrong grade** — the fix prevents the next one, it does not repair this one.

**One correction to the premise, because it changes how urgent the repair is:** `weight_used` is
**not** read by the gate's arithmetic and **does not scale position size** — `scaled_step_margin` is
deprecated with no callers, and `main.py:1998` says so verbatim. It reaches trading through exactly
one channel: it is printed to the entry advisor as `Combo weight: 1.00 (1.0 baseline; <1 =
historical loser, >1 = winner)`. A wrong weight can mislead the advisor's judgement. It cannot
silently resize a position or move a threshold.

**Nothing was re-graded. The correction plan in §2 is written and NOT executed.**

---

## 1. THE FIX

### 1.1 How closure is identified — one predicate, both modes, no join

`trades.pnl IS NOT NULL`.

**Why that is reliable, traced rather than asserted:**

| step | evidence |
|---|---|
| There is exactly **one** writer of `virtual_positions.status='closed'` in the codebase | `virtual_trader.py:1230` — grep across every `.py` confirms it is the only one |
| That same statement's transaction also writes `trades.pnl` | `virtual_trader.py:1242`, `UPDATE trades SET pnl=? WHERE id=? AND pnl IS NULL`, using the cross-link `trades_entry_row_id` populated at entry |
| It is **mode-agnostic** | the engine owns the position in both modes (`engine_owns_position()`, item 12), so `_do_close` runs for paper and live alike; `order_adapter` decides only whether the fills underneath were simulated |
| **Nothing else writes that column** | the only other two writers, `main.py:2970` and `main.py:3321`, are both inside `if realized_pnl is not None:` on close paths |
| The intent was already documented — three times | all three write sites carry a comment saying the audit loop keys on a non-NULL `pnl`, e.g. *"Propagate realized PnL to the entry trades row so the signal_weights audit loop (which scores rows with combo_key + non-NULL pnl) sees the virtual outcome."* **The comments were right. The query never enforced them.** |

So no join to `virtual_positions` is needed, and no mode branch. **The fix makes the code do what
three of its own comments already claim it does.**

### 1.2 Two doors, deliberately

1. **In the query** — `AND pnl IS NOT NULL`. An open position cannot be *selected*. This is the
   same shape as the `_exit_pct(source)` guard from `625fedc`: the invariant lives in the WHERE
   clause, not in a convention a later caller can forget.
2. **In the resolver** — it returns `None`, and the caller `continue`s. So even a future edit that
   loosens the query cannot produce a grade for an open position.

### 1.3 What happens to a position that never closes

**It is left ungraded, permanently, and it never blocks anything.**

The window is a **moving 2..96 h band on `trades.timestamp`** — not a queue, not a backlog. A
still-open position is simply not selected on each 10-minute pass. When its entry drifts past 96 h
it falls out of the lower bound and **no grade is ever written for it**.

That is the deliberate choice, in the operator's terms: **an ungraded trade teaches nothing; a
trade graded on a mark teaches something false.** No timeout writes a value. No "abandoned" score.
Nothing is graded on a mark, ever.

### 1.4 Why `AUDIT_MAX_AGE_HOURS` had to go 24 → 96

Requiring closure while keeping a 24 h entry-anchored window would have been a **regression I
introduced**: a position held longer than the window closes *outside* its own window and is never
graded at all. Measured over the 58 closed positions with an entry row:

```
median hold  6.33h   |   p90 31.20h   |   p95 43.16h   |   max 74.33h
held > 24h : 14 of 58  (24%)      held > 48h : 2       held > 72h : 1
```

**24 h would have permanently discarded a quarter of all positions.** 96 h covers the observed
maximum with 29% headroom. `AUDIT_MIN_AGE_HOURS` stays at **2** — deliberately unchanged, so the
grading *timing* of the rows that were already correct is identical to before.

### 1.5 The diff — `signal_weights.py`, the only file touched

```diff
@@ Audit window
+# 🔴 MIN_AGE IS NO LONGER WHAT MAKES THE OUTCOME REAL (2026-08-03). Closure is:
+# `audit_pending` now requires `pnl IS NOT NULL`. MIN_AGE stays at 2 h purely so
+# the grading TIMING of already-correct rows is byte-identical to before this
+# change — it is a delay, not a guarantee, and it never was one.
 AUDIT_MIN_AGE_HOURS = 2
-AUDIT_MAX_AGE_HOURS = 24
+# 🔴 24 -> 96. WIDENED BECAUSE REQUIRING CLOSURE WOULD OTHERWISE LOSE DATA.
+# ... 14 (24%) were held longer than 24 h ... the longest is 74.33 h.
+# What happens to a position still open when its entry passes 96 h: it is
+# **LEFT UNGRADED, PERMANENTLY** ... an ungraded trade teaches nothing, a
+# trade graded on a mark teaches something FALSE.
+AUDIT_MAX_AGE_HOURS = 96

@@ the resolver
-def _intent_to_position_side(intent):
-    ...                                        # dead once the branches below go
-
-def _evaluate_trade_pnl(exchange, trade_row):
-    """Determine the trade's current PnL for audit purposes.
-    Prefer the recorded realized pnl ... Otherwise look up the live position on
-    the exchange and use unrealized PnL. If no matching position is open ...
-    fall back to 0.0 and mark neutral.
-    """
-    _, _, symbol, intent, entry_price, amount, recorded_pnl = trade_row[:7]
-    if recorded_pnl is not None:
-        return float(recorded_pnl), 'realized'
-    pos_side = _intent_to_position_side(intent)
-    if not pos_side:
-        return 0.0, 'unknown_intent'
-    try:
-        positions = exchange.fetch_positions([symbol])
-    except Exception as e:
-        print(f"audit fetch_positions failed: {e}")
-        raise
-    pos = next((p for p in positions if ... float(p.get('contracts') or 0) > 0), None)
-    if pos is None:
-        return 0.0, 'closed_unknown'
-    upnl = pos.get('unrealizedPnl') or (pos.get('info') or {}).get('unrealizedProfit')
-    return float(upnl or 0.0), 'unrealized'
+def _evaluate_trade_pnl(trade_row):
+    """The trade's REALISED PnL, or None when the position has not closed.
+
+    🔴 A GRADE IS AN OUTCOME, AND AN OPEN POSITION HAS NO OUTCOME (2026-08-03).
+    [full provenance of both deleted branches, with the row ids and the numbers]
+
+    Returns `(pnl, 'realized')`, or **None meaning NOT GRADABLE YET**. Never a
+    fabricated 0.0.
+    """
+    recorded_pnl = trade_row[6]
+    if recorded_pnl is None:
+        return None
+    return float(recorded_pnl), 'realized'

@@ audit_pending — the query
             "WHERE status='executed' AND combo_key IS NOT NULL "
             "  AND audit_score IS NULL "
+            "  AND pnl IS NOT NULL "
             "  AND timestamp <= ? AND timestamp >= ?",

@@ audit_pending — the call
-        try:
-            outcome_pnl, source = _evaluate_trade_pnl(exchange, eval_row)
-        except Exception:
-            continue  # network blip; try again next interval
+        # SECOND DOOR, deliberately kept alongside the query predicate: the
+        # resolver refuses rather than invents, and a refusal SKIPS the row
+        # instead of grading it. ... There is no network call here any more.
+        graded = _evaluate_trade_pnl(eval_row)
+        if graded is None:
+            continue  # position not closed -> NOT GRADABLE. Retry next pass.
+        outcome_pnl, source = graded
```

### 1.6 Nine proofs, by execution

| # | proof | result |
|---|---|---|
| 1 | `ast.parse` + import | ✅ OK; `_intent_to_position_side` gone; MIN/MAX = 2 / 96 |
| 2 | **the OPEN live position is not selectable** — row 20920 reset to ungraded on a DB **copy** | OLD predicate selects it: **True** · NEW predicate: **False** |
| 3 | a CLOSED row is still selectable — row 20100 (vpos 90, 71 h old, would have been outside the old 24 h window) | **True** |
| 4 | resolver behaviour | open row → **`None`** · closed row → **`(-0.60987, 'realized')`** |
| 5 | **`audit_pending` end-to-end with the exchange replaced by a TRIPWIRE** that raises on any attribute access | audited **1**; 20920 (open) left `(None, None)`; 20100 (closed) graded from realised pnl; **the tripwire never fired — the audit loop no longer touches the exchange at all** |
| 6 | thresholds at live size | `+20 / −15` against a live 1R of \$1.3–2.5 ⇒ every live grade classes **neutral**, weight delta **0.00** |
| 7 | **no backfill surge** on the real DB (read-only) | rows the OLD query picks now: **0** · NEW query: **0** · inside the widened 2..96 h band: **0**. Widening 24→96 backfills **nothing** |
| 8 | trade path untouched | gate reads `signal_weights.weight` / `hyperwave_weights.weight`; this change writes only `trades.audit_score/audit_at` and the `evaluations/total_pnl/wins/losses` counters — **disjoint**. `record_outcome`, `get_weight`, `engine_15m.evaluate`: **0 lines changed** |
| 9 | blast radius | `git diff --stat` = **1 file, +86 −54**. Nothing outside `signal_weights.py` |

Isolation for proofs 2–5 followed the 01.08 rule — **every module in the call graph** got the test
path (`signal_weights.DB_PATH` **and** `engine_15m.DB_PATH`), `LEARNING_ENABLED` was forced off and
`claude_advisor.consult_for_learning` was replaced with a raiser, so no Claude call and no write
could reach the live DB.

### 1.7 Deployed

```
commit ca90c2f  ·  restart 2026-08-03 13:42:33 UTC  ·  service active
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY      LIVE_TRADING_ENABLED = True · ORDER_ADAPTER_LIVE = True
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
[STOP-CLEANUP] no orphaned orders for LONG  ·  no orphaned orders for SHORT  ·  [RECONCILE] done
```

**All four boot gates green. Zero errors, zero tracebacks since the restart.**

---

## 2. THE THREE EXISTING WRONG GRADES — PLAN, NOT EXECUTED

### 2.1 First, the fact that makes this tractable

**At live size no grade can move a weight.** `record_outcome` moves the weight only at
`pnl ≥ +20.0` or `pnl ≤ −15.0`. Live 1R is \$1.32–2.49. **All six live-era grades classified
`neutral`, delta `0.00`** — confirmed in the store itself: every affected combo row reads
`wins 0, losses 0`, and `weight` is untouched.

| trade | vpos | graded | class | realised | class | Δ to `total_pnl` | weight moved? |
|---|---|---:|---|---:|---|---:|---|
| 19589 | 86 | −1.2829 | neutral | **−2.541574** | neutral | **−1.258674** | **no** |
| 19713 | 87 | −0.3467 | neutral | **−0.819051** | neutral | **−0.472351** | **no** |
| 20920 | **91** | **+0.5015** | neutral | **−0.641000** | neutral | **−1.142500** | **no** |

*(One check worth stating because it looks alarming otherwise: combo
`1H:Bullish Confirmation+|15M:HyperWave Signal Up|5M:Within Bullish OB` shows `weight 0.90,
losses 1`. That −0.10 came from a **paper** evaluation of ≈ **−78.70**, not from trade 19713 — 19713
was already at 0.90 when it entered at 12:05, two hours before its own audit at 14:11.)*

### 2.2 Per store — what can be corrected, and what cannot

| store | polluted by these three | re-grade possible? | safe? |
|---|---|---|---|
| **`signal_weights.weight`** | **not at all** — all three neutral | n/a | n/a |
| `signal_weights.wins / losses` | not at all — all three neutral | n/a | n/a |
| **`signal_weights.evaluations`** | 3 rows carry one evaluation each that was scored on a mark | ✅ **yes** — the count itself is correct (the trade *was* evaluated); only the value behind it was wrong | ✅ trivially |
| **`signal_weights.total_pnl`** | **yes** — by exactly the Δ column above | ✅ **yes, exactly** — `total_pnl = total_pnl − old + new`, a pure sum with no order dependence and no clamp | ✅ safe |
| **`hyperwave_weights.weight`** | **not at all** — same neutral classification | n/a | n/a |
| **`hyperwave_weights.total_pnl`** | yes — `HW_SIGNAL_SHORT` −1.258674, `HW_SIGNAL_LONG` −0.472351, `HW_OS_LONG` −1.142500 | ✅ yes, same arithmetic | ✅ safe |
| **`trades.audit_score / audit_at`** | yes, all three | ✅ yes — overwrite with the realised pnl and stamp the correction time | ✅ safe |
| **`trades.learning_*`** (the Claude attribution) | **yes, and this one is a TEXT VERDICT, not a number** | ⚠️ **re-runnable, but it is a fresh LLM call** — a new verdict is not the old one corrected, it is a different verdict | ⚠️ see below |

**The `learning_*` case is the one that cannot simply be arithmetic.** Trade 20920's stored
attribution reads:

> *"Large ask wall (68.32 BTC at 62650.5) above entry created resistance, **enabling profitable
> short exit as price rejected upward pressure**."*

The position did not exit profitably — it closed at **−0.6410**. That sentence is not a wrong
number, it is a wrong *story*, and it is stored as text. Options: (a) clear the columns and let the
loop re-attribute on a corrected outcome; (b) leave them and mark them; (c) re-run
`consult_for_learning` with the realised pnl. **All three are decisions, not cleanups, and I am not
taking them here.** Note also that these columns are **read by nothing** — grep confirms
`signal_weights` is their only writer and there is no reader — so the cost of leaving them is
archival, not behavioural.

### 2.3 The plan (proposed, not run)

```
FOR trade IN (19589, 19713, 20920):
  old := trades.audit_score          -- -1.2829 / -0.3467 / +0.5015
  new := trades.pnl                  -- -2.541574 / -0.819051 / -0.641000
  assert class(old) == class(new) == 'neutral'      -- ABORT if false: a class change
                                                    -- would mean a weight must move too,
                                                    -- and that is a different operation
  signal_weights.total_pnl    += (new - old)   WHERE combo_key   = trade.combo_key
  hyperwave_weights.total_pnl += (new - old)   WHERE subtype     = trade.hw_15m_subtype
  trades.audit_score := new ; trades.audit_at := <correction ts>
-- evaluations / wins / losses / weight: UNTOUCHED on both stores
-- learning_*: UNTOUCHED pending the operator's call on 2.2
```

**Preconditions I would insist on before running it:** a `trades.db` backup; the assert above
enforced per row, not assumed; and the whole thing in one transaction. **It is not run and no
column has been changed.**

### 2.4 🔴 THE MUCH BIGGER RE-GRADE — MEASURED, AND EXPLICITLY NOT RECOMMENDED AS A CLEANUP

The three rows above are the *small* half. The **44 paper rows graded `0.0`** are the other half,
and **those did have the magnitude to move weights**. Replaying `record_outcome` in audit order
over all 66 audited trades, once from the stored grades and once from realised P&L:

```
COMBO weights   : 29 of 53 would move   (26 by ±0.10, one 0.80 -> 0.60)
SUBTYPE weights :  4 of 16 would move
     HW_SIGNAL_SHORT  0.85 -> 1.00        HW_SIGNAL_LONG  0.75 -> 0.85
     HW_OB_SHORT      1.00 -> 0.90        REVERSAL_LONG   1.00 -> 0.95
```

**Both of the most-used subtypes are currently marked as losers and would stop being marked as
losers.** That is a real change to what the entry advisor is told, across the majority of the
weight table, derived from a 68× notional discontinuity between the paper and live eras. **It is a
strategy decision wearing a data-repair's clothes, and it is not in this task's scope.** Recorded
here so it is on the record with its number, and so it cannot later be slipped in as housekeeping.

---

## 3. 🔴 vpos 91 — IT CLOSED DURING THIS WORK, AND ITS GRADE IS PERMANENT

**Answer to the question as asked: `audit_score` is permanent once set. The fix does not re-grade
it, and it will never be re-picked.** The queue predicate is `audit_score IS NULL`; the row has
`0.5015`. Even now that `trades.pnl` is populated, the new query skips it — verified after the
restart:

```
post-restart: rows the NEW query picks : 0
trade 20920 : audit_score = 0.5015 , pnl = -0.64100000000001
              -> pnl now set, audit_score NOT NULL => never re-picked
```

**And the projection is no longer a projection.** While this task was in progress the exit advisor
closed the position:

```
13:41:02  [TITAN-WALL-TRAIL-DRYRUN] vpos=91 price=62878.80 ... real-SL=63224.60 tighter=1 breached_now=0
13:41:07  [EXIT-ADVISOR-LIVE] trigger=hourly SHORT close=True conf=0.72
          | "Entry thesis collapse: 15m was opposing at entry (HyperWave OS LONG vs SHORT trade);
             now 15m=bull, 5m=neutral with bullish structure (OB entered 11m ago, liquidity grab
             6m ago). Regime shifted: 15m/5m..."
13:41:07  [EXIT-ADVISOR-ACT] vpos=91 ... — CLOSING at market
13:41:10  VIRTUAL CLOSE vpos=91 SHORT avg_entry=62649.2000 exit=62871.4 net_pnl=-0.6410 reason=ai_exit
```

| | |
|---|---|
| closed | **2026-08-03 13:41:09.328 UTC**, `close_reason = ai_exit` |
| exit price | 62,871.4 (entry 62,649.2) |
| **net** | **−0.6410** (gross −0.51106 · fees 0.144349 · funding −0.014409) |
| MFE / MAE | 62,268.6 = **+0.661R** · 62,969.6 = **−0.557R** |
| **its grade** | **+0.5015, written 08:48:51 while open — a WIN** |
| **error** | **sign inverted; \$1.1425 wrong on a position whose whole 1R is \$1.32** |

**So the answer to "its grade WILL be wrong whichever way it resolves" is: it resolved, and it is
wrong.** It is row 3 of the §2.3 plan, with `new = −0.641000`, and it is **not** corrected yet.

**Timeline of my restart against the position, stated plainly:** the close committed at 13:41:09;
I restarted at 13:42:33 — **84 seconds later**, and the boot reconciler found `0 exchange
position(s), 0 open row(s)`. The pre-restart check I printed reported `closed` before the restart
ran, but I should be exact: it was **informational, not a blocking gate** — the restart was chained
to run regardless. It was moot here. (For the record, a restart with an open position is a
documented-safe operation on this bot — the stop lives on the exchange under item 11 and survived a
restart with an unchanged order id on vpos 86 — but that is not the same as having enforced the
constraint, and I am not going to claim I enforced it.)

**Side note, outside this task's scope and not counted here:** this is the exit advisor's **5th**
close under the §2.4 criterion. Its held-branch counterfactual has not been computed — the position
closed 25 minutes ago and the held branch has not resolved. **n stays reported at 4 until that
replay is done properly.**

---

## 4. THE TRADE PATH IS UNTOUCHED — AND ONE CORRECTION TO THE PREMISE

**Confirmed, four ways:**

1. **`record_outcome` is byte-identical** — 0 lines changed. Same thresholds, same clamp, same
   `INSERT … ON CONFLICT`, same `weight = MAX(floor, MIN(ceiling, weight + delta))`.
2. **`get_weight` is byte-identical** — `SELECT weight FROM signal_weights WHERE combo_key=?`.
   **How** the gate reads the weight is untouched; this change only alters **when** a grade is
   written.
3. **`engine_15m.evaluate` / `_get_weight` are byte-identical** — `engine_15m.py` was not modified
   at all.
4. **The written and the read columns are disjoint.** This change can alter
   `trades.audit_score`, `trades.audit_at`, and the `evaluations / total_pnl / wins / losses`
   counters. The trading side reads only `signal_weights.weight` and `hyperwave_weights.weight`.

**The correction to the premise, because it changes the risk picture rather than the finding:**
`weight_used` is **not** read by the gate's score arithmetic and **does not size the position.**
`main.py:1998`, verbatim:

> *"Signal-quality weight is logged + shown to Claude for context only; it no longer scales position
> size (sizing is risk-based, computed in `_execute_entry` from config)."*

`scaled_step_margin` is marked DEPRECATED with no callers, and grep confirms none. `weight_used`
reaches trading through exactly **one** channel — it is rendered into the entry advisor's prompt:

```
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
```

That is a genuine influence channel — vpos 91's own entry prompt carried that line — and a wrong
weight there is a wrong hint to the model. **But it cannot resize a position, cannot move a
threshold, and cannot fire an order.** That is why §2.4's 29-combo re-grade is a decision to be
taken deliberately rather than an emergency.

**One incidental improvement worth naming:** the audit loop **no longer calls the exchange at all**.
`fetch_positions` is gone from it, which removes a network dependency — and with it the
`except: raise` → `continue` path that silently skipped a row on any API blip — from a loop that
runs every 10 minutes.

---

## APPENDIX — SCOPE HELD

| | |
|---|---|
| Book sources (OKX-4000 vs BingX-100 vs BingX-20) | **NOT TOUCHED.** `microstructure.py`, `liquidity_zones.py`, `orderbook_collector.py`, `main.py` unchanged. That remains the separate, attributable question from the 13:30 report |
| vpos 91 | not disturbed; it closed on the exit advisor's own verdict 84 s before the restart, and no column of it was written by hand |
| The three wrong grades | **plan written, NOT executed.** No `UPDATE` was run against `trades`, `signal_weights` or `hyperwave_weights` |
| Files changed | **`titan-bot/signal_weights.py` only** — +86 / −54 |
| Thresholds, clamps, weights, gates | unchanged |
