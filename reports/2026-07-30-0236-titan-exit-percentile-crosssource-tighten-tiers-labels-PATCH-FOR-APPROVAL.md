# TITAN — PATCH FOR APPROVAL: the exit-side percentile inversion, the terminal 'tightened', and four lying labels

_2026-07-30 02:36 UTC · HEAD `12b4df2` · 🔴 LIVE, REAL MONEY · vpos 86 OPEN_

---

## DECISION LINE

**Nothing has been applied. Six files are staged and proven in a scratchpad; the live tree is
byte-identical to `12b4df2`.** Read the diffs below and say go. On approval I restart, confirm the
🔴 LIVE banner at $150, confirm vpos 86 and its exchange stop are intact, and show the next hourly
consult's book section with correct percentiles.

**Two things I found that the forensics did not, both about the same no-op TIGHTEN:**

1. 🔴 **It cancelled and re-placed the REAL exchange stop for a zero-point move.** Verified against
   BingX: order `...809867436032` CANCELLED at `00:50:31.409`, `...881359347712` created at
   `00:50:31.765`. **356 ms with no protective stop on a live $147 short, bought for nothing.**
2. **The exit advisor has since said CLOSE twice** — 01:50:24 (`hourly`) and 02:00:10
   (`15m_exit_confirm`), both `close=True conf=0.72`, "entry thesis broken/compromised". Both were
   blocked by `EXIT_ADVISOR_DRYRUN=True`, which is the deliberate setting. **I did not act on it.**
   Flagging because it is your call, not mine, and it is running against a live position now.

---

## PART 0 — VERIFICATION (read-only, all clean)

| # | check | result |
|---|---|---|
| 1 | git clean · HEAD · origin sync | clean · `12b4df2` · `main...origin/main` **0 ahead 0 behind** |
| 2 | runtime = commit **by hash** | all 7 touched files `sha256`-identical to HEAD; latest mtime **22:45:55** precedes proc start **22:47:24** |
| 3 | boot banner (live journal) | `🔴 LIVE ORDERS — REAL MONEY`, `LIVE_TRADING_ENABLED=True`, `ORDER_ADAPTER_LIVE=True`, **margin $30 x 5 = $150** |
| 4 | service · restarts · errors · breaker | `active` · `NRestarts=0` · **0** tracebacks/CRITICAL since start · breaker never tripped (`0` UNSAFE lines) |
| 5 | exchange — **both probes** | unified `fetch_positions`: 1 SHORT 0.0023 @ 63686.0 · raw `swapV2`: `positionId 2082629807737368578` amt 0.0023 avg 63686.0 — **agree** |
| 6 | orders — **both probes** | unified: 1 open · raw: `STOP_MARKET BUY posSide=SHORT qty=0.0023 stopPrice=64767.1 closePosition=true workingType=MARK_PRICE status=NEW` — exactly one, no orphans |
| 7 | vpos 86 vs exchange | DB `stop_order_id=2082629881359347712` == the live order · size, side, entry, SL all reconcile · **1 open row, id 86** |
| 8 | balance | USDT free 481.73 · **used 29.30** (= the $30 margin) · total 511.03 |
| 9 | Mercury-SOL | `active since 2026-07-21 06:39`, `NRestarts=0` — **untouched** |
| 10 | RECONCILE-XDB gate at boot | `✅ exchange and DB agree for BTC/USDT:USDT` |

**Position now (02:36 UTC):** mark 64202.9 · uPnL **−$1.19** · **−0.478R** · stop **+0.522R away**
at 64767.1 · trail **NOT ARMED** (arms at 62604.9) · breakeven not applied · MAE 64368.7 (−0.632R).

**Recheck ledger for vpos 86 — the defect, in the data:**

```
recheck_events: ONE row.  tier_sec=10  verdict=TIGHTEN  health=-5
                sl_before=64767.1  sl_after=64767.1  sl_tightened_pct=0.0
                reasons=[{"rule":"adx_below_floor","value":11.271,"threshold":20.0,"points":-5}]
virtual_positions.recheck_status = 'tightened'   <-- terminal. T+60s and T+300s never ran.
```

---
## PART 1 — THE EXIT-SIDE PERCENTILE CROSS-SOURCE BUG

**What was wrong.** `_build_exit_context` fetched walls from `microstructure.fetch_pre_trade_walls`
(BingX, depth 100, contracts) and ranked them with `_exit_pct` against `orderbook_density` (OKX
books-full 4000, USDT). OKX imbalance sd 0.046 vs BingX depth-100 sd 0.238 — five times wider — so
a foreign value pins to 0 or 100.

**How it was fixed — the entry pattern, copied, not a second one invented.** `_entry_book_pct`
already feeds the OKX dict to the OKX baseline. The exit context now calls the same
`liquidity_zones.fetch_pre_trade_walls(symbol)`.

**The trap in the obvious version of this fix, and how it is handled.** `virtual_positions.entry_sup_wall_mult`
and `entry_ob_imbalance` are **BingX** values written at fill. Simply switching "now" to OKX would
have paired a BingX entry against an OKX now and rendered it as one trend arrow — re-creating the
defect in a new place. vpos 86's stored `0.2914` against a live OKX `0.5008` would have read as a
dramatic **FLIPPED** that never happened. So the entry reference is taken instead from the
`orderbook_density` row nearest the fill — the baseline's own measurement — bounded to ±10 min, with
the actual age printed. For vpos 86 the nearest row is **21 s from the fill**.

**The structural guard (item 3), stated exactly.** `_exit_pct(col, value, source)` — `source` is now
a **required positional argument** AND is **ANDed into the WHERE clause**:

- *Required positional* → a future caller that has not thought about provenance cannot write a
  working call; it raises `TypeError` at the call site instead of silently ranking a foreign number.
  The value and its origin travel together or not at all.
- *In the SQL predicate* → this is what makes it a guard rather than a convention. Even a caller
  that passes a **wrong** source string cannot borrow another book's distribution: it gets that
  book's rows, or none. `BOOK_SRC_BINGX_100` matches zero baseline rows, so a BingX percentile is
  not merely omitted by policy — **it is unobtainable**.

**Item 2 — no percentile rather than a wrong one.** When OKX is unavailable the block falls back to
the BingX book, renders it RAW with its source named, and prints no percentile at all; the prompt
says so in words and tells the model not to infer "extreme" or "ordinary" from a bare multiple.

**Item 4 — depth confirmed not broken.** Depth was always read straight from the latest
`orderbook_density` row, so it was already OKX-vs-OKX — the one percentile that was correct on
vpos 86 (6th pct). Only the mandatory `source` argument was added; the number is unchanged.

### Proven against the live baseline

```
GUARD
  OKX imbalance 0.5141, source=okx_books_full_4000   -> 71.0th pct  (n=24048)
  BingX 0.2914,         source=bingx_depth100        -> (None, 0)  = no percentile
  [OLD] BingX 0.2914 ranked against the whole table  -> 0.0th pct   <-- THE FABRICATION

WHAT THE 00:50:20 CONSULT SHOULD HAVE SAID  (OKX row 00:49:35, the baseline's own measurement)
  supporting wall (ask x5.6)  = 44th pct    prompt said 35th
  opposing  wall (bid x5.44)  = 50th pct    prompt said 93th   <-- INVERTED
  imbalance      (0.5008)     = 62th pct    prompt said  0th   <-- INVERTED
  depth          (2439.7 BTC) =  6th pct    prompt said  6th   <-- already correct
```

(The forensics quoted 69th/26th from a live fetch at 00:50:20; I quote 62nd/50th from the stored
00:49:35 baseline row, 45 s earlier. Both OKX, same conclusion: **the 0th and the 93rd were
inverted, and the advisor cited the phantom 93rd to justify holding.**)

### The rendered block, before and after

```
BEFORE (what the advisor actually read at 00:50:20)
  Supporting wall = 35th pct   Opposing wall = 93th pct
  Total depth = 2440 BTC = 6th pct (sampled 42s ago)   Imbalance = 0th pct

AFTER (OKX path)
Order book NOW vs AT ENTRY — source: OKX books-full depth-4000 (the percentile baseline)  (entry reference sampled 21s from fill, same book)
  Supporting wall: entry x5.7 -> now x5.6 (THINNED)
  Opposing wall:   now x5.4
  Imbalance:       entry 0.51 -> now 0.50 (same side)

Order-book PERCENTILE scale (baseline: 24048 snapshots of this SAME book)
  Supporting wall = 44th pct
  Opposing wall = 50th pct
  Total depth = 2440 BTC = 6th pct (sampled 42s ago)
  Imbalance = 62th pct

AFTER (BingX fallback — raw, and it says so)
Order-book PERCENTILE scale: NOT AVAILABLE for this consultation.
  The figures above are RAW multiples from a book that is not the baseline's
  instrument, so they cannot be ranked. Do NOT infer 'extreme' or 'ordinary'
  from a bare multiple — every book state contains a wall above 4x.
```

---

## PART 2 — 'tightened' IS TERMINAL AND ATE THE REMAINING TIERS

**The fix asks the question the old code never asked: did the number actually change?**

The `93c20c3` bound means `new_sl == current_sl` on every pre-breakeven path, and the recheck only
runs pre-breakeven — so **a zero-point TIGHTEN is the normal outcome here, not an edge case.** When
the move is zero the branch now writes `t+{tier}_ok` instead of `'tightened'`, **and does not call
`move_stop` at all** — which closes the 356 ms naked window as well as the tier-budget leak.
Tolerance is 0.0064 pts, **16× smaller than one BTC tick**, so it can only ever catch an exact
no-op, never a real move rounded small.

**Item 6 — the advisory is still recorded.** `sensor_events.log_recheck` still runs and the
`recheck_events` row still carries `verdict='TIGHTEN'`, the health score and the reasons, on both
paths. A distinct Telegram line (`🟨 TIGHTEN (advisory only)`) states that the stop was untouched
and that later tiers remain due. The data was never what was at risk; the follow-through was.

**`'tightened'` stays terminal, deliberately.** A tighten that really moved the stop has materially
changed the position's protection and the later tiers were never meant to re-litigate it. The bug
was never that `'tightened'` is terminal — it was that a **no-op was being recorded as one**.

**Item 5 — NOT retroactive, and it needs no special case.** vpos 86 already carries `'tightened'`
in the DB, so it stays terminal and no tier fires. I am **not** arguing for retroactive resumption:
its T+60s and T+300s windows elapsed around 00:51 and 00:55 UTC, and firing EMERGENCY_CLOSE now
would act on an hour-old health read — which is not what a T+60s tier is for, and not a decision
this code should make unprompted. **Elapsed windows stay skipped by construction, not by a flag.**

*Honest note on a pre-existing behaviour I did not change:* `_recheck_tier_due` returns the LARGEST
due tier, so a stalled poller returning at T+400s would fire tier 300 late. That is how the `_ok`
path has always worked for every position; my change routes no-op tightens into that same path
rather than inventing new timing behaviour.

### Proven

```
NO-OP DETECTION (vpos86's exact numbers)
  cur=64767.1 new=64767.1        -> no-op=True    (bounded, zero move)
  cur=64767.1 new=64700.0        -> no-op=False   (a real 67-pt tighten)
  tolerance 0.006369 pts = 16x smaller than one BTC tick (0.1)

TIER BUDGET, future position
  OLD  status='tightened' -> T+10 None · T+65 None · T+305 None      (2 tiers lost)
  NEW  status='t+10_ok'   -> T+65 fires tier 60 · T+305 fires tier 300
  => EMERGENCY_CLOSE reachable again.

vpos86 (status='tightened', elapsed ~5400s) -> tier due: None   <-- NOT resumed, as instructed
a REAL tighten  (status='tightened', T+305s) -> tier due: None   <-- still terminal, as designed
```

---

## PART 3 — THE LABELS THAT DO NOT SAY WHAT THEY MEAN

**7 · `LIQUIDITY` → `5M-STRUCTURE` on the card.** Display label only, via a new
`CATEGORY_DISPLAY_LABEL` map. The internal key is load-bearing — it is written into
`matrix_breakdown_json`, read by the optimizer and quoted in every historical report — so renaming
it would break the archive to fix a display string. **Membership, weights and the minority-zeroing
rule are untouched**, as instructed; whether that rule should fire at all is a separate study.

```
OLD   • LIQUIDITY: 🚫 minority-LONG zeroed (would've been 2.5)  (1 sig)
NEW   • 5M-STRUCTURE: 🚫 minority-LONG zeroed (would've been 2.5)  (1 sig)
```

**8 · `Imbalance: 0.31 (Balanced)` → source + raw number, no judgement word.** `_imbalance_label`
is **deleted**, not deprecated — a lying label left in the file is an invitation to call it again,
and grep confirmed exactly one call site. No percentile is shown, and that is deliberate rather
than lazy: the only imbalance baseline the bot keeps is OKX depth-4000, and ranking a BingX top-20
value against it is precisely the inversion fixed in Part 1. This book's own history lives only
inside `trades.orderbook_json` blobs with no queryable column, so an honest own-distribution
percentile is not available at card-render time.

```
OLD   • Imbalance: 0.31 (Balanced)
NEW   • Imbalance: 0.31 — BingX top-20, raw (no baseline · not the advisor's book · context only)
```

**9 · ADX gets its timeframe, and the gate's figure beside it.** ATR and Volume are labelled too,
since they had the same silence. A missing 1h snapshot degrades to the labelled 5m number rather
than a dash that could read as "the gate saw nothing".

```
OLD   📊 Trend Strength (ADX): 25.87
NEW   📊 Trend Strength (ADX 5m): 25.87   |   1h: 11.12 ← the gates read this
      📉 Volatility (ATR 5m): 80.80
      🔊 Volume Profile (5m): Above Average (×4.92)
```

At vpos 86's entry that one line would have shown **11.12 against a floor of 20** — the same value
the recheck scored −5 eleven seconds later.

---
## RECORDED, NOT ACTED ON — for OPEN-ITEMS (items 10, 11, 12)

These go into `OPEN-ITEMS.md` on approval, alongside the volume forming-candle record.

**10 · ADX is computed on the FORMING candle on every timeframe, by explicit design.**
`indicators.py:210-223` — the July volume fix dropped the forming row for `vol_ratio` only and says
so verbatim: *"ATR/ADX/EMA above keep `iloc[-1]` on purpose — they are calibrated on the live
forming candle and are out of scope."* Measured effect at vpos 86's entry: 1h −0.59, 15m +0.31,
5m +1.07 (0.3–1.1 points). **Not a defect, not to be "fixed" — but it belongs written down next to
the volume forming-candle fix so the next person does not rediscover it as a bug.**

**11 · The volume ceiling killed at n=4 REPLICATES at a larger clean n. ENTRY filter — needs its
own study, not built now.**

| cohort | n | wins | net $ |
|---|---:|---:|---:|
| `vol_ratio_5m` ≥ 2.42 | **15** | **2 (13%)** | **−$708.72** |
| 1.30–1.60 band | 9 | 6 (67%) | +$241.07 |

vpos 86 entered at **4.92 = 92nd percentile**, inside the bad band near its top.
**Confounds, stated:** 11 of the 15 are LONGs, so direction is entangled with volume; the sample
spans **two sizing eras**. This is not a validated ceiling. **The point of the record is that the
original study was killed on a sample size that no longer applies.**

**12 · Open question: depth at the 6th percentile was the single most extreme book reading of the
trade — shown CORRECTLY to both advisors, and weighted by NEITHER.** 2,440 BTC, thinnest 6% of
24,001 snapshots. The entry advisor saw "Book depth: 2,440 BTC — 6th pct" and executed at 0.82; the
exit advisor saw "6th pct" and held. No gate reads depth on any path. Either it should carry weight
somewhere or we should stop rendering it as if it does.

---

## WHAT HAPPENS ON APPROVAL

1. Copy the six staged files over the live tree, `python3 -m py_compile` each, re-run the
   symtable/scope audit across all four order-path modules.
2. Commit (one commit per part) and push.
3. `systemctl restart titan` — deliberately, with the position open. The stop is a
   `closePosition=true STOP_MARKET` living **on the exchange**, so it survives the restart; the
   boot `RECONCILE-XDB` gate re-verifies exchange↔DB before anything else runs.
4. Confirm: 🔴 LIVE banner with **$30 × 5 = $150** · runtime == commit **by hash** · vpos 86 still
   open with `stop_order_id` present on the exchange · breaker untripped.
5. Show the next hourly consult's book section with the corrected percentiles.
6. Publish the final consolidated report as a **new dated file** and send the raw link.

**Risks I am accepting and naming:** the restart drops in-memory state for an open live position —
mitigated by the exchange-side stop and the boot reconciler, both proven tonight. `vpos 86` keeps
its terminal `'tightened'`, so it gains no new recheck protection from this patch; its stop and the
trail arming level are unchanged.

**Not touched:** entry logic, scoring, weights, the minority-zeroing rule, `EXIT_ADVISOR_DRYRUN`,
`WALL_TRAIL_LIVE_ENABLED`, the wall-rule zero weights, sizing, or Mercury-SOL.

---

## THE FULL PATCH — all six files, inline

```diff
--- a/main.py
+++ b/main.py
@@ -2234,12 +2234,56 @@
                     "combo": combo, "weight": weight_used}), 200
 
 
-def _exit_pct(col, value):
-    """Percentile of `value` within the orderbook_density baseline. Read-only."""
+# ---- ORDER-BOOK PROVENANCE (2026-07-30) -------------------------------------
+# The percentile baseline. `orderbook_density` is written by orderbook_collector
+# from exactly ONE instrument — the OKX books-full depth-4000 snapshot — and every
+# row carries that name in its `source` column.
+BOOK_SRC_OKX_4000 = 'okx_books_full_4000'
+# The BingX depth-100 book (microstructure.fetch_pre_trade_walls). It exists in
+# this file only as a VALUE source, never as a baseline: no row in
+# orderbook_density carries this name, so declaring it to _exit_pct() yields an
+# empty baseline and therefore NO percentile — which is the correct outcome, not
+# a failure. See the guard below.
+BOOK_SRC_BINGX_100 = 'bingx_depth100'
+
+
+def _exit_pct(col, value, source):
+    """Percentile of `value` within the orderbook_density baseline. Read-only.
+
+    🔴 `source` is MANDATORY, and it is part of the QUERY — not a comment.
+
+    2026-07-30: this function used to rank whatever it was handed against the
+    whole table. `_build_exit_context` handed it BingX depth-100 values while the
+    table holds OKX depth-4000 — imbalance sd 0.238 vs 0.046, five times wider —
+    so a foreign value pinned to 0 or 100 almost every time. On the live position
+    vpos 86 at 00:50:20 that printed `Imbalance = 0th pct` when the OKX book that
+    same second measured 0.5141 = 69th, and `Opposing wall = 93th pct` when the
+    OKX max bid wall was x4.8 = 26th. Both inverted, and the exit advisor quoted
+    the phantom 93rd-percentile wall as a reason to HOLD a live short.
+
+    The guard is structural in two independent ways, so the class cannot recur:
+
+      1. `source` is a REQUIRED POSITIONAL argument. A future caller that has not
+         thought about provenance cannot write a working call — it raises
+         TypeError at the call site instead of silently ranking a foreign number.
+         The value and its origin travel together or not at all.
+      2. `source` is ANDed into the WHERE clause, so a value is only ever ranked
+         against rows recorded from the SAME instrument. This is what makes it a
+         guard rather than a convention: even a caller that passes a WRONG source
+         string cannot borrow another book's distribution — it gets that book's
+         rows or none. If a second collector source is ever added to this table,
+         every value automatically keeps ranking against its own distribution
+         with no further code change.
+
+    A source with no rows returns (None, 0), which every renderer degrades to "no
+    percentile shown". That is the intended trade: a missing percentile costs
+    nothing, an inverted one changed a hold decision on live money.
+    """
     try:
         with sqlite3.connect(DB_PATH) as conn:
             r = conn.execute(f"SELECT SUM({col} < ?), COUNT(*) FROM orderbook_density "
-                             f"WHERE {col} IS NOT NULL", (value,)).fetchone()
+                             f"WHERE {col} IS NOT NULL AND source = ?",
+                             (value, source)).fetchone()
         return (100.0 * r[0] / r[1], r[1]) if r and r[1] else (None, 0)
     except Exception:
         return None, 0
@@ -2290,10 +2334,16 @@
                     for w in (walls.get('walls_ask') or [])), default=0.0)
         out['bid_max'] = _bid
         out['ask_max'] = _ask
-        out['bid_pct'], out['baseline_n'] = _exit_pct('max_wall_mult_bid', _bid)
-        out['ask_pct'], _ = _exit_pct('max_wall_mult_ask', _ask)
+        # The walls dict here is liquidity_zones' OKX depth-4000 snapshot — the
+        # baseline's own instrument — which is what the docstring above means by
+        # apples-to-apples. That was already true; 2026-07-30 only makes the claim
+        # MACHINE-CHECKED by naming the source in the call.
+        out['bid_pct'], out['baseline_n'] = _exit_pct(
+            'max_wall_mult_bid', _bid, BOOK_SRC_OKX_4000)
+        out['ask_pct'], _ = _exit_pct('max_wall_mult_ask', _ask, BOOK_SRC_OKX_4000)
         if walls.get('imbalance') is not None:
-            out['imb_pct'], _ = _exit_pct('imbalance', walls['imbalance'])
+            out['imb_pct'], _ = _exit_pct(
+                'imbalance', walls['imbalance'], BOOK_SRC_OKX_4000)
         with sqlite3.connect(DB_PATH) as conn:
             row = conn.execute(
                 "SELECT ts, total_depth_btc FROM orderbook_density "
@@ -2301,7 +2351,8 @@
             ).fetchone()
         if row:
             out['depth_btc'] = row[1]
-            out['depth_pct'], _ = _exit_pct('total_depth_btc', row[1])
+            out['depth_pct'], _ = _exit_pct(
+                'total_depth_btc', row[1], BOOK_SRC_OKX_4000)
             try:
                 out['depth_age_s'] = int((
                     datetime.now(timezone.utc) - datetime.fromisoformat(row[0])
@@ -2426,28 +2477,109 @@
         if vpos.get('opened_at'):
             ctx['elapsed_h'] = (datetime.now(timezone.utc) - datetime.fromisoformat(
                 vpos['opened_at'])).total_seconds() / 3600.0
-        walls = microstructure.fetch_pre_trade_walls(exchange, symbol)
+        # 🔴 THE BOOK MUST BE THE BOOK THE BASELINE IS BUILT FROM (2026-07-30).
+        #
+        # This block used to call microstructure.fetch_pre_trade_walls() — the
+        # BingX depth-100 book, measured in CONTRACTS — and then rank those numbers
+        # against orderbook_density, which is the OKX books-full depth-4000 book
+        # measured in USDT. Unrelated distributions (OKX imbalance sd 0.046 vs
+        # BingX depth-100 sd 0.238), so landing one on the other pinned it to 0 or
+        # 100. See _exit_pct() for the live proof on vpos 86.
+        #
+        # The ENTRY path never had this bug: _entry_book_pct() above feeds the OKX
+        # dict to the OKX baseline and documents the requirement. That pattern is
+        # COPIED here rather than a second one invented — same source function,
+        # same baseline, same _exit_pct(). The exit side now reads the identical
+        # snapshot orderbook_collector samples every 60s, so every percentile below
+        # is OKX-vs-OKX by construction.
+        walls = liquidity_zones.fetch_pre_trade_walls(symbol)
         if walls:
             b = [w.get('mult') for w in (walls.get('walls_bid') or []) if w.get('mult')]
             a = [w.get('mult') for w in (walls.get('walls_ask') or []) if w.get('mult')]
             sup = max(b or [0]) if side == 'LONG' else max(a or [0])
             opp = max(a or [0]) if side == 'LONG' else max(b or [0])
             ctx.update(sup_now=sup, opp_now=opp, imb_now=walls.get('imbalance'),
-                       sup_entry=vpos.get('entry_sup_wall_mult'),
-                       imb_entry=vpos.get('entry_ob_imbalance'))
-            if ctx['sup_entry']:
+                       book_src='OKX books-full depth-4000 (the percentile baseline)')
+            # THE ENTRY REFERENCE MUST BE THE SAME INSTRUMENT TOO. This is the trap
+            # in the obvious version of this fix: virtual_positions.entry_sup_wall_mult
+            # and entry_ob_imbalance are BingX depth-100 (written by the microstructure
+            # path at fill time), so pairing them with an OKX "now" would re-create the
+            # very defect being removed — one book at entry, a different one now,
+            # rendered as a single trend arrow with no hint that the two are
+            # incomparable. vpos 86's stored 0.2914 against a live OKX 0.51 would have
+            # read as a dramatic FLIP that never happened.
+            #
+            # The entry-side OKX reading is taken instead from the orderbook_density
+            # row nearest the fill — the baseline's own measurement, on a 60s cadence.
+            # Bounded to ±10 min so a collector outage degrades to "no entry reference"
+            # (renders n/a) rather than silently quoting a stale one; the actual age is
+            # carried and printed so the operator sees how close the match was.
+            try:
+                _t0 = datetime.fromisoformat(vpos['opened_at'])
+                _lo = (_t0 - timedelta(minutes=10)).isoformat()
+                _hi = (_t0 + timedelta(minutes=10)).isoformat()
+                with sqlite3.connect(DB_PATH) as conn:
+                    _rows = conn.execute(
+                        "SELECT ts, max_wall_mult_bid, max_wall_mult_ask, imbalance "
+                        "FROM orderbook_density WHERE source = ? AND ts BETWEEN ? AND ?",
+                        (BOOK_SRC_OKX_4000, _lo, _hi)).fetchall()
+                _best, _best_dt = None, None
+                for _r in _rows:
+                    try:
+                        _dt = abs((datetime.fromisoformat(_r[0]) - _t0).total_seconds())
+                    except (ValueError, TypeError):
+                        continue
+                    if _best_dt is None or _dt < _best_dt:
+                        _best, _best_dt = _r, _dt
+                if _best is not None:
+                    ctx['sup_entry'] = _best[1] if side == 'LONG' else _best[2]
+                    ctx['imb_entry'] = _best[3]
+                    ctx['book_entry_age_s'] = int(_best_dt)
+            except Exception as _e:
+                print(f"[EXIT-ADVISOR] entry book reference unavailable: {_e}",
+                      flush=True)
+            if ctx.get('sup_entry'):
                 ctx['sup_trend'] = 'THINNED' if sup < ctx['sup_entry'] else 'grew'
-            if ctx['imb_entry'] is not None and ctx['imb_now'] is not None:
+            if ctx.get('imb_entry') is not None and ctx['imb_now'] is not None:
                 ctx['imb_trend'] = ('FLIPPED'
                                     if (ctx['imb_entry'] - .5) * (ctx['imb_now'] - .5) < 0
                                     else 'same side')
             sc = 'max_wall_mult_bid' if side == 'LONG' else 'max_wall_mult_ask'
             oc = 'max_wall_mult_ask' if side == 'LONG' else 'max_wall_mult_bid'
-            ctx['sup_pct'], n = _exit_pct(sc, sup)
-            ctx['opp_pct'], _ = _exit_pct(oc, opp)
+            ctx['sup_pct'], n = _exit_pct(sc, sup, BOOK_SRC_OKX_4000)
+            ctx['opp_pct'], _ = _exit_pct(oc, opp, BOOK_SRC_OKX_4000)
             if ctx['imb_now'] is not None:
-                ctx['imb_pct'], _ = _exit_pct('imbalance', ctx['imb_now'])
+                ctx['imb_pct'], _ = _exit_pct(
+                    'imbalance', ctx['imb_now'], BOOK_SRC_OKX_4000)
             ctx['baseline_n'] = n
+        else:
+            # OKX unavailable. The rule: a figure that cannot be sourced from the
+            # baseline's instrument is shown RAW and NAMED, never ranked against a
+            # foreign scale. The BingX book is still worth showing as a live
+            # fallback — it is a real book — so it is fetched and rendered with its
+            # source stated and NO percentile. Note there is no discipline needed to
+            # keep it that way: declaring BOOK_SRC_BINGX_100 to _exit_pct() matches
+            # zero baseline rows, so a percentile is not merely omitted by choice
+            # here, it is unobtainable.
+            _bx = microstructure.fetch_pre_trade_walls(exchange, symbol)
+            if _bx:
+                b = [w.get('mult') for w in (_bx.get('walls_bid') or []) if w.get('mult')]
+                a = [w.get('mult') for w in (_bx.get('walls_ask') or []) if w.get('mult')]
+                ctx.update(
+                    sup_now=(max(b or [0]) if side == 'LONG' else max(a or [0])),
+                    opp_now=(max(a or [0]) if side == 'LONG' else max(b or [0])),
+                    imb_now=_bx.get('imbalance'),
+                    sup_entry=vpos.get('entry_sup_wall_mult'),
+                    imb_entry=vpos.get('entry_ob_imbalance'),
+                    book_src='BingX depth-100 — RAW, NOT the percentile baseline')
+                if ctx.get('sup_entry'):
+                    ctx['sup_trend'] = ('THINNED' if ctx['sup_now'] < ctx['sup_entry']
+                                        else 'grew')
+                if ctx.get('imb_entry') is not None and ctx['imb_now'] is not None:
+                    ctx['imb_trend'] = (
+                        'FLIPPED'
+                        if (ctx['imb_entry'] - .5) * (ctx['imb_now'] - .5) < 0
+                        else 'same side')
         # DEPTH — the "Total depth" line has rendered `n/a` on EVERY exit
         # consultation ever made, because nothing set `depth_pct` (2026-07-29).
         # Asymmetry by oversight, not design: the ENTRY advisor has carried depth
@@ -2467,7 +2599,14 @@
                 ).fetchone()
             if _d:
                 ctx['depth_btc'] = _d[1]
-                ctx['depth_pct'], _dn = _exit_pct('total_depth_btc', _d[1])
+                # DEPTH WAS ALREADY CORRECT and stays byte-identical in behaviour:
+                # it is read straight from the latest orderbook_density row, so it
+                # was always OKX-vs-OKX — the one percentile on this prompt that was
+                # right on vpos 86 (6th pct, and accurate). Naming the source here
+                # changes nothing about the number; it only brings the call in line
+                # with the now-mandatory signature.
+                ctx['depth_pct'], _dn = _exit_pct(
+                    'total_depth_btc', _d[1], BOOK_SRC_OKX_4000)
                 if not ctx.get('baseline_n'):
                     ctx['baseline_n'] = _dn
                 try:
--- a/claude_advisor.py
+++ b/claude_advisor.py
@@ -528,6 +528,62 @@
         the same treatment the entry side gives it (8b15ecc)."""
         a = c.get('depth_age_s')
         return f" (sampled {a}s ago)" if isinstance(a, int) else ''
+
+    def _book_block(c):
+        """The live book, its source, and ONLY the percentiles that are valid.
+
+        🔴 2026-07-30. This block used to print four percentiles unconditionally
+        with a fixed layout. Three of them were computed by ranking BingX
+        depth-100 values against the OKX depth-4000 baseline (fixed in
+        main._exit_pct), and the renderer had no way to express "unavailable" —
+        so a fabricated number was structurally guaranteed to appear. On vpos 86
+        it printed `Imbalance = 0th pct` for a book sitting at the 69th and
+        `Opposing wall = 93th pct` for one at the 26th, and the advisor cited the
+        phantom wall in its reason to HOLD.
+
+        Now: the SOURCE is named on the header line, and a percentile is rendered
+        only when `_exit_pct` actually produced one. When none are available the
+        block says so in words and explicitly tells the model not to read
+        'extreme' or 'ordinary' into a bare multiple — because a bare multiple is
+        exactly what the old NOTE line warned means nothing on its own.
+        """
+        src = c.get('book_src') or 'source not recorded'
+        _age = c.get('book_entry_age_s')
+        _ref = (f"  (entry reference sampled {_age}s from fill, same book)"
+                if isinstance(_age, int) else "")
+        out = [f"Order book NOW vs AT ENTRY — source: {src}{_ref}",
+               f"  Supporting wall: entry x{g('sup_entry','.1f')} -> "
+               f"now x{g('sup_now','.1f')} ({g('sup_trend')})",
+               f"  Opposing wall:   now x{g('opp_now','.1f')}",
+               f"  Imbalance:       entry {g('imb_entry','.2f')} -> "
+               f"now {g('imb_now','.2f')} ({g('imb_trend')})", ""]
+        pcts = []
+        if isinstance(c.get('sup_pct'), (int, float)):
+            pcts.append(f"Supporting wall = {c['sup_pct']:.0f}th pct")
+        if isinstance(c.get('opp_pct'), (int, float)):
+            pcts.append(f"Opposing wall = {c['opp_pct']:.0f}th pct")
+        if isinstance(c.get('depth_pct'), (int, float)):
+            pcts.append(f"Total depth = {g('depth_btc','.0f')} BTC = "
+                        f"{c['depth_pct']:.0f}th pct{_depth_age(c)}")
+        if isinstance(c.get('imb_pct'), (int, float)):
+            pcts.append(f"Imbalance = {c['imb_pct']:.0f}th pct")
+        if pcts:
+            out.append(f"Order-book PERCENTILE scale (baseline: {g('baseline_n')} "
+                       f"snapshots of this SAME book)")
+            out += [f"  {p}" for p in pcts]
+            out += ["  NOTE: EVERY book state contains a wall above 4x, so 'large "
+                    "multiple' means",
+                    "  nothing on its own. Judge by the percentile: ~50th is ORDINARY."]
+        else:
+            out += ["Order-book PERCENTILE scale: NOT AVAILABLE for this "
+                    "consultation.",
+                    "  The figures above are RAW multiples from a book that is not "
+                    "the baseline's",
+                    "  instrument, so they cannot be ranked. Do NOT infer 'extreme' "
+                    "or 'ordinary'",
+                    "  from a bare multiple — every book state contains a wall "
+                    "above 4x."]
+        return "\n".join(out) + "\n\n"
     user = (
         "OPEN POSITION — decide CLOSE or HOLD.\n\n"
         "Position\n"
@@ -536,16 +592,7 @@
         f"  Elapsed: {g('elapsed_h','.1f')}h\n"
         f"  Current stop: {g('sl','.1f')}  ->  {g('dist_sl_r','+.2f')}R away\n"
         f"  Peak so far (MFE): {g('mfe_r','+.2f')}R   Giveback from peak: {g('giveback_r','.2f')}R\n\n"
-        "Order book NOW vs AT ENTRY\n"
-        f"  Supporting wall: entry x{g('sup_entry','.1f')} -> now x{g('sup_now','.1f')} ({g('sup_trend')})\n"
-        f"  Opposing wall:   now x{g('opp_now','.1f')}\n"
-        f"  Imbalance:       entry {g('imb_entry','.2f')} -> now {g('imb_now','.2f')} ({g('imb_trend')})\n\n"
-        f"Order-book PERCENTILE scale (baseline: {g('baseline_n')} snapshots)\n"
-        f"  Supporting wall = {g('sup_pct','.0f')}th pct   Opposing wall = {g('opp_pct','.0f')}th pct\n"
-        f"  Total depth = {g('depth_btc','.0f')} BTC = {g('depth_pct','.0f')}th pct"
-        f"{_depth_age(ctx)}   Imbalance = {g('imb_pct','.0f')}th pct\n"
-        "  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means\n"
-        "  nothing on its own. Judge by the percentile: ~50th is ORDINARY.\n\n"
+        f"{_book_block(ctx)}"
         "Regime at ENTRY vs NOW\n"
         f"  At entry: {g('regime_entry')}\n"
         f"  Now:      {g('regime_now')}\n"
--- a/virtual_trader.py
+++ b/virtual_trader.py
@@ -1622,6 +1622,57 @@
             symbol, _tighten_sl(position_side, entry_price, current_sl,
                                 original_sl=_orig_sl)))
 
+        # 🔴 A TIGHTEN THAT MOVES NOTHING MUST NOT SPEND WHAT IT DID NOT USE
+        # (2026-07-30). The 93c20c3 bound above means new_sl == current_sl on every
+        # pre-breakeven path, and the recheck ONLY runs pre-breakeven — so a TIGHTEN
+        # that moves zero points is the NORMAL outcome here, not an edge case. Two
+        # consequences of that bound were never followed through; vpos 86 was the
+        # first position to reach this branch since it landed, and it hit both:
+        #
+        #   1. the branch wrote recheck_status='tightened', which the poller treats
+        #      as TERMINAL — so T+60s and T+300s never ran, including the
+        #      EMERGENCY_CLOSE branch, the only recheck path with teeth. A no-op
+        #      advisory consumed the entire remaining post-entry budget.
+        #   2. it still called move_stop(), which CANCELS the live exchange stop and
+        #      re-places it at the identical price. On vpos 86 that left a real
+        #      $147 short with NO protective stop between 00:50:31.409 (cancel) and
+        #      00:50:31.765 (replace) — 356 ms of naked risk bought for nothing.
+        #      Verified against the exchange: order ...809867436032 CANCELLED,
+        #      ...881359347712 created 356 ms later, same stopPrice 64767.1.
+        #
+        # Both fall out of asking the question the old code never asked: DID THE
+        # NUMBER ACTUALLY CHANGE? If not, touch neither the exchange nor the tier
+        # ledger — record the advisory and leave the position exactly as a normal
+        # 'OK' tier leaves it, so T+60s and T+300s stay due. The verdict, health
+        # score and reasons are still written to recheck_events either way: the DATA
+        # was never what was at risk, the follow-through was.
+        #
+        # This is the same class as the 29.07 finding — the failing thing was made
+        # safe, and a second consequence of it was not followed through.
+        #
+        # Tolerance is a fraction of a tick (BTC ticks at 0.1), so this can only
+        # ever catch an exact no-op, never a real move rounded small.
+        if abs(new_sl - current_sl) <= entry_price * 1e-7:
+            _set_recheck_status(vpos_id, f"t+{tier}_ok")
+            try:
+                sensor_events.log_recheck(sl_after=new_sl, **_evt)
+            except Exception as e:
+                print(f"[TITAN][SENSOR-EVT] recheck log call failed: {e}", flush=True)
+            print(f"[VIRTUAL] recheck vpos={vpos_id} T+{tier}s TIGHTEN advisory — "
+                  f"SL unchanged at {current_sl:.2f} (bounded by original "
+                  f"{float(_orig_sl):.2f}); exchange stop untouched, later tiers "
+                  f"stay due", flush=True)
+            if send_tg:
+                try:
+                    send_tg(f"🟨 <b>Post-entry T+{tier}s — TIGHTEN (advisory only)</b> "
+                            f"{symbol} {position_side}\n"
+                            f"Health {score} · SL stays {current_sl:.2f} "
+                            f"(bounded by original {float(_orig_sl):.2f}) · {reasons}\n"
+                            f"Stop untouched on the exchange. Later tiers remain due.")
+                except Exception as e:
+                    print(f"recheck tighten telegram failed: {e}", flush=True)
+            return None
+
         # STOP OWNERSHIP (item 11) — MOVER 2 of 2: the recheck TIGHTEN.
         # Same race guard as breakeven; in paper it is a no-op returning
         # ('moved', None) and the UPDATE below is byte-identical to today.
@@ -2102,6 +2153,22 @@
     #     once; tighten/critical-close are terminal. A new tier fires when its mark
     #     has elapsed and is newer than the last recorded tier; past the final tier
     #     with no action we mark 'done' and hand off to the trail.
+    #
+    #     'tightened' REMAINS TERMINAL, deliberately (2026-07-30). A tighten that
+    #     actually moved the stop has materially changed the position's protection,
+    #     and the later tiers were never meant to re-litigate it. What changed is
+    #     that a TIGHTEN verdict which moves ZERO points no longer writes this
+    #     status at all (see _run_recheck_tier) — it writes 't+{tier}_ok', so the
+    #     remaining tiers stay due. The bug was never that 'tightened' is terminal;
+    #     it was that a no-op was being recorded as one.
+    #
+    #     NOT RETROACTIVE, and that is a decision rather than an oversight: vpos 86
+    #     already carries 'tightened' in the DB and therefore stays terminal here.
+    #     Its T+60s and T+300s windows elapsed around 00:51 and 00:55 UTC; firing
+    #     an EMERGENCY_CLOSE branch an hour late on a live position would be acting
+    #     on an hour-old health read, which is not what a T+60s tier is for and is
+    #     not a decision this code should make unprompted. Elapsed windows stay
+    #     skipped. The fix governs positions opened from here on.
     if (POST_ENTRY_RECHECK_ENABLED and not be_applied
             and ('recheck_status' not in row.keys()
                  or row['recheck_status'] not in ('done', 'tightened', 'closed_critical'))):
--- a/signal_matrix.py
+++ b/signal_matrix.py
@@ -135,6 +135,32 @@
     'Bearish Imbalance Mitigated':  (CAT_LIQUIDITY, SHORT, 'imb_mit_bear', 0.5),
 }
 
+# ---- OPERATOR-FACING CATEGORY LABELS (2026-07-30) ---------------------------
+# 🔴 'LIQUIDITY' reads to an operator as ORDER BOOK. It is not. The category holds
+# the ten LuxAlgo 5m candlestick signals listed directly above — Liquidity Grab,
+# EQH/EQL, trendline breaks, imbalance — and ZERO order-book inputs. The book is
+# never scored, never weighted, and never enters confluence_score on any path.
+#
+# The cost was diagnostic, and it was paid: the card line
+# "LIQUIDITY: 🚫 minority-LONG zeroed" appeared on 22 of 73 executed trades, and
+# every one of them reads as "the order book was outvoted". On vpos 86 it sent a
+# live-money investigation looking for a book veto that had never existed — what
+# was actually zeroed was a Bullish Liquidity Grab candlestick from 15 minutes
+# earlier. Fourth instance of the "the label lies" class.
+#
+# The INTERNAL keys are load-bearing and deliberately unchanged: they are written
+# into trade_signal_matrix.matrix_breakdown_json, read by the optimizer, and
+# quoted in every historical report — renaming them would break the archive to fix
+# a display string. Only what the CARD prints changes.
+#
+# Membership, weights and the minority-zeroing rule are UNTOUCHED. Whether that
+# rule should fire at all is a separate open question (it silences this category
+# and effectively only this one on trades that execute) and needs its own study,
+# not a rename smuggling in a behaviour change.
+CATEGORY_DISPLAY_LABEL = {
+    CAT_LIQUIDITY: '5M-STRUCTURE',
+}
+
 # Map lowercased name -> canonical lookup for case-insensitive matching.
 _LOWER_LOOKUP = {k.lower(): k for k in SIGNAL_DICTIONARY}
 
@@ -537,7 +563,9 @@
         else:
             tag = (f"{b['net_direction']} +{b['contribution']:.2f}"
                    if b['contribution'] > 0 else "—")
-        parts.append(f"  • {cat}: {tag}  ({b['signal_count']} sig)")
+        # Display label only — `cat` stays the internal key everywhere else.
+        parts.append(f"  • {CATEGORY_DISPLAY_LABEL.get(cat, cat)}: {tag}  "
+                     f"({b['signal_count']} sig)")
     return "\n".join(parts)
 
 
--- a/microstructure.py
+++ b/microstructure.py
@@ -353,16 +353,15 @@
     return book_summary, tape_summary, saved
 
 
-def _imbalance_label(imbalance) -> str:
-    """Ask-Heavy / Balanced / Bid-Heavy classification matching the same
-    bands the analyzer uses for tape pressure (<.30 / .30-.70 / >.70)."""
-    if imbalance is None:
-        return 'N/A'
-    if imbalance < 0.30:
-        return 'Ask-Heavy'
-    if imbalance > 0.70:
-        return 'Bid-Heavy'
-    return 'Balanced'
+# 🔴 `_imbalance_label()` REMOVED 2026-07-30 — it returned Ask-Heavy / Balanced /
+# Bid-Heavy from hardcoded cutoffs (<.30 / .30-.70 / >.70) with no baseline, no
+# percentile and no source, and the card printed its word next to the number as
+# though it were a measurement. Same defect class as the 4.0x "Massive" wall label
+# fixed in 8b15ecc: a constant threshold read by an operator as a judgement.
+#
+# It was deleted rather than deprecated because a lying label left in the file is
+# an invitation to call it again; grep confirmed exactly one call site, below.
+# What replaces it is the number, its source, and nothing else.
 
 
 def format_telegram_block(book_summary, tape_summary, saved_status):
@@ -377,7 +376,28 @@
 
     if book_summary is not None:
         imb = book_summary.get('imbalance')
-        imb_str = (f"{imb:.2f} ({_imbalance_label(imb)})"
+        # SOURCE + RAW NUMBER, NO JUDGEMENT WORD (2026-07-30).
+        #
+        # Naming the source is half the fix. At 00:50:1x on vpos 86 the machine
+        # recorded THREE different "Imbalance" values for BTC in the same minute
+        # and showed them under one word, never saying they were different books:
+        # this card 0.31 (BingX top-20), the advisor prompt 0.51 (OKX depth-4000),
+        # and virtual_positions.entry_ob_imbalance 0.2914 (BingX depth-100).
+        #
+        # No percentile is shown, and that is deliberate rather than lazy. The only
+        # imbalance BASELINE the bot keeps is orderbook_density, which is OKX
+        # depth-4000 — ranking a BingX top-20 value against it is exactly the
+        # cross-source inversion fixed in main._exit_pct, which on this same
+        # position reported a 69th-percentile book as "0th pct". This book's own
+        # history exists only inside trades.orderbook_json blobs with no queryable
+        # column, so an honest own-distribution percentile is not available at card
+        # render time. Per the rule: a figure that cannot be ranked against its OWN
+        # distribution is printed RAW and NAMED, never dressed in a band that
+        # implies calibration it does not have.
+        #
+        # No gate reads this number — it is operator context only, and now says so.
+        imb_str = (f"{imb:.2f} — BingX top-{MICROSTRUCTURE_BOOK_DEPTH}, raw "
+                   f"(no baseline · not the advisor's book · context only)"
                    if imb is not None else 'N/A')
     else:
         imb_str = 'N/A'
--- a/indicators.py
+++ b/indicators.py
@@ -437,13 +437,31 @@
     return format(x, spec)
 
 
-def telegram_block(snap: Dict[str, Optional[float]], primary_tf: str = '5m') -> str:
+def telegram_block(snap: Dict[str, Optional[float]], primary_tf: str = '5m',
+                   gate_tf: str = '1h') -> str:
     """Three-line indicator block for trade-open Telegram reports.
 
     Pulls primary_tf (default 5m) for the headline values. ADX/ATR show
     raw numbers; volume profile renders as Above/Below Average against
-    the 20-bar SMA on the same TF."""
+    the 20-bar SMA on the same TF.
+
+    🔴 EVERY TIMEFRAME IS NAMED, AND THE GATE'S TIMEFRAME IS SHOWN (2026-07-30).
+    This block used to print "Trend Strength (ADX): 25.87" with no timeframe at
+    all, and the number was the 5m ADX — the one timeframe no gate reads. At
+    vpos 86's entry the card showed 25.87 while the 1h ADX the gates actually
+    read was 11.1, below the FLAT floor of 20; the post-entry recheck scored that
+    same 1h value -5 eleven seconds later and alerted "ADX 11.3<20". An operator
+    comparing the card against that alert saw 25.87 versus 11.3 and had no way to
+    tell they were different series rather than a stale reading. Both numbers
+    were correct; only the labelling was not.
+
+    The advisor prompt has always named its timeframes ("ADX(14): 1h 11.1 | 15m
+    13.0"). This card was the only surface printing a bare ADX, and it printed
+    the timeframe with the least authority. `gate_tf` is rendered alongside so
+    the figure the gates read is visible on the same line, not merely implied.
+    """
     adx = snap.get(f'srv_adx_{primary_tf}')
+    adx_gate = snap.get(f'srv_adx_{gate_tf}')
     atr = snap.get(f'srv_atr_{primary_tf}')
     vol_ratio = snap.get(f'srv_vol_ratio_{primary_tf}')
     if isinstance(vol_ratio, (int, float)) and vol_ratio == vol_ratio:
@@ -453,9 +471,15 @@
     else:
         vol_profile = "n/a"
     ema_line = ema_summary_str(snap, primary_tf)
+    # The gate figure is rendered only when present, so a missing 1h snapshot
+    # degrades to the labelled primary-TF number rather than to a dash that could
+    # be misread as "the gate saw nothing".
+    gate_str = (f"   |   <b>{gate_tf}: {_fmt(adx_gate)}</b> ← the gates read this"
+                if isinstance(adx_gate, (int, float)) and adx_gate == adx_gate
+                else "")
     return (
-        f"\n📊 Trend Strength (ADX): {_fmt(adx)}\n"
-        f"📉 Volatility (ATR): {_fmt(atr)}\n"
-        f"🔊 Volume Profile: {vol_profile}\n"
+        f"\n📊 Trend Strength (ADX {primary_tf}): {_fmt(adx)}{gate_str}\n"
+        f"📉 Volatility (ATR {primary_tf}): {_fmt(atr)}\n"
+        f"🔊 Volume Profile ({primary_tf}): {vol_profile}\n"
         f"📈 EMA Status ({primary_tf}): {ema_line}"
     )
```

_Staged and proven read-only. Live tree still `12b4df2`. Awaiting go._
