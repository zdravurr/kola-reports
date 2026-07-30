# TITAN — APPLIED AND LIVE: the percentile inversion, the 356 ms naked stop, and four labels

_2026-07-30 03:00 UTC · `12b4df2` → **`957f980`** · 🔴 LIVE, REAL MONEY · vpos 86 still OPEN_

---

## DECISION LINE

**All three parts applied, pushed, and running.** Runtime == `957f980` **by hash**, banner 🔴 LIVE
at **$30 × 5 = $150**, vpos 86 intact with **the same exchange stop order it had before the restart**
(id unchanged — not cancelled, not re-placed), breaker untripped, zero errors, Mercury-SOL untouched.

**Two things need your eye, neither of which I acted on:**

1. **The exit advisor has now said `close` THREE times** on vpos 86 — 01:50, 02:00 and 02:50, all
   conf 0.72, all "entry thesis broken". All three were blocked by `EXIT_ADVISOR_DRYRUN = True`,
   which is the deliberate setting. **All three were also fed a corrupted book block** (they predate
   the fix), so they are logged but not counted.
2. **The activation criterion restarts from zero — item 6, answered below with data.**

---

## ITEM 6 — THE ACTIVATION CRITERION. YES, RESTART. AND YOUR PARTITION HAS AN EMPTY BUCKET.

You proposed: reset consults whose reason **cites a book figure**, keep those that do not, since the
corruption is confined to the book block. **I agree with the principle — and the data collapses it
into a full restart, because the second bucket does not exist:**

| cohort | n | closes | holds |
|---|---:|---:|---:|
| reason **CITES** a book figure | **68** | 43 | 25 |
| reason does **not** cite the book | **0** | — | — |

**68 of 68 exit consults ever recorded cite a book figure.** 64/68 say "wall" on its own; the
remainder cite imbalance or book. Verified against verbatim samples rather than trusting the
pattern-match: *"Supporting wall thinned (5.0→4.3x, 14th pct)"* · *"Order-book imbalance flipped
from 0.21 to 0.52 (76th pct—ask-heavy resistance)"*. These are real citations with percentiles
quoted inline.

**So there is no clean cohort to preserve and no judgement call to make.** Progress goes **1 → 0**;
the single post-`c307bb7` datapoint (vpos 84, NEUTRAL) is discarded with the rest, because its
consults carried the same corrupted block.

**One caveat I want on the record, because it cuts against the partition even though the outcome
is the same:** "the reason does not mention the book" would **not** have proven non-contamination.
The prompt is read whole, and a fabricated `0th percentile` is an extreme claim capable of moving a
verdict it is never quoted in. The empty bucket spares us a judgement we would otherwise have had
to defend. **The bar itself does not move.** Recorded in OPEN-ITEMS §2.4.

---

## YOUR FOUR CHECKS, ANSWERED BEFORE ANYTHING WAS APPLIED

**1 · New names verified at RUNTIME, not by grep.** Established first that importing `main` is safe
(no module-level threads; `app.run` is behind `if __name__ == '__main__'`; the only top-level calls
are `load_dotenv` and an idempotent `init_db()`). Then checked each name in **the calling function's
own `__globals__`** — the namespace that actually resolves at call time:

```
main._build_exit_context.__globals__:  timedelta True · datetime True · timezone True
                                       liquidity_zones True · microstructure True · sqlite3 True
                                       BOOK_SRC_OKX_4000 True · BOOK_SRC_BINGX_100 True
   timedelta(minutes=10) actually constructs -> datetime.timedelta(seconds=600)
microstructure.format_telegram_block.__globals__:  MICROSTRUCTURE_BOOK_DEPTH True, value=20
   _imbalance_label removed -> True
signal_matrix.format_for_telegram.__globals__:  CATEGORY_DISPLAY_LABEL True {'LIQUIDITY': '5M-STRUCTURE'}
```

`MICROSTRUCTURE_BOOK_DEPTH = 20` also **confirms the "top-20" wording** in the new label is factually
correct rather than assumed.

**2 · Scope audit widened to every touched file.** You were right that my plan named the wrong set.
Run over all six patched files **plus** the two order-path modules:

```
✅ main.py STAGED (90)        ✅ virtual_trader.py STAGED (53)   ✅ claude_advisor.py STAGED (22)
✅ signal_matrix.py STAGED (13) ✅ microstructure.py STAGED (20) ✅ indicators.py STAGED (25)
✅ order_adapter.py (27)      ✅ breakeven_worker.py (22)
272 function scopes checked across 8 modules.  EXIT=0
```

**3 · In-scope at the new branch, and the caller's contract.** All four bound well before the branch
at line 1655: `send_tg` is the function **parameter** (1547), `score` 1565, `reasons` 1570, `_evt`
1584. The branch `return None`s — structurally identical to the OK path's `return None` (1735). The
caller:

```python
if _run_recheck_tier(exchange, row, last, _tier, send_tg) == 'closed':
    return True
changed = True
```

`None != 'closed'` → `changed = True`, **exactly how an OK tier is already treated**. The
`log_recheck(sl_after=…, **_evt)` call matches the shape both existing paths use.

**4 · Tolerance arithmetic — your question found a real assumption, so I removed it.**

| instrument | price | tick | `price*1e-7` | tick/tol |
|---|---:|---:|---:|---:|
| BTC now | 63,686 | 0.1 | 6.4e-03 | 15.7× |
| BTC $200k | 200,000 | 0.1 | 2.0e-02 | 5.0× |
| **BTC $1M** | 1,000,000 | 0.1 | 1.0e-01 | **1.0× ← equals one tick** |
| SOL | 150 | 0.01 | 1.5e-05 | 667× |
| DOGE | 0.10 | 1e-05 | 1.0e-08 | 1000× |

**It is safe for every instrument this bot trades, and it is not BTC-specific in the direction you
might expect** — because it scales *with* price, low-priced symbols get *more* headroom, not less.
The real flaw is the opposite one: the tolerance grows with price while **BTC's tick is fixed at
0.1**, so the margin shrinks as price rises and **reaches exactly one tick at BTC $1M**, where a
genuine one-tick tighten would be misread as a no-op — in the one branch whose whole job is to
decide whether the stop moved.

**So I deleted the epsilon rather than tuning it.** Both sides now go through
`exchange.price_to_precision`, making the comparison exact on the exchange's own grid, correct for
any symbol and tick size:

```
cur=64767.1  new=64767.1  -> no-op=True    (vpos86: bounded, zero move)
cur=64767.1  new=64767.0  -> no-op=False   (ONE TICK tighter = a real move)
cur=64767.1  new=64700.0  -> no-op=False   (67-pt tighten)
BTC tick from market spec: 0.1
```

(`price_to_precision` truncates, so a sub-tick difference is treated as a **real** move — erring
toward doing the work rather than skipping it, which is the safe direction here.)

---

## POST-RESTART VERIFICATION

| check | result |
|---|---|
| HEAD · origin | `957f980` · `main...origin/main`, **0 ahead 0 behind** |
| runtime = commit **by hash** | all 8 order-path/touched files `sha256`-identical to HEAD |
| mtime vs proc start | latest source **02:49:33** precedes proc start **02:51:11** |
| boot banner | `🔴 LIVE ORDERS — REAL MONEY` · `LIVE_TRADING_ENABLED=True` · `ORDER_ADAPTER_LIVE=True` · **margin $30 x 5 = $150** |
| **RECONCILE-XDB** | `✅ exchange and DB agree: **1** exchange position(s), **1** open row(s)` — first time it has proven itself against a LIVE position, not 0/0 |
| boot reconciler | `SHORT open, SL present @ 64767.1 — kept.` · `engine owns positions — NOT enqueueing a breakeven job` |
| errors · breaker | **0** tracebacks/CRITICAL · **0** UNSAFE/breaker lines · `NRestarts=0` |
| position, both probes | unified `short 0.0023 @ 63686.0` · raw `positionId 2082629807737368578 SHORT 0.0023` — agree |
| **stop order** | `2082629881359347712 STOP_MARKET stop=64767.1 closePosition=true NEW` — **same id as before the restart. Not cancelled, not re-placed.** |
| vpos 86 row | `open · sl=64767.1 · stop_order_id=2082629881359347712 · recheck=tightened` (**not** resumed, as decided) |
| Mercury-SOL | `active since 2026-07-21 06:39` · `NRestarts=0` — untouched |

**Position at 03:00 UTC:** mark 64159.1 · uPnL **−$1.09** · **−0.438R** · stop **+0.562R away** ·
trail not armed.

---

## PART 1 PROVEN ON LIVE DATA

The 02:50:25 consult fired **46 seconds before** the restart, so it ran on the old code — it is not
evidence about the patch, and I am not presenting it as such. The next hourly is due ~03:50. Instead
I invoked the **running patched code** against vpos 86 read-only (no API call, no orders):

```
book_src         = OKX books-full depth-4000 (the percentile baseline)
book_entry_age_s = 21          <- entry reference from the baseline's OWN measurement
imb_entry        = 0.5086      <- OKX, NOT the BingX 0.2914 that would have faked a FLIP
sup_pct 74.0 · opp_pct 25.9 · imb_pct 0.93 · depth_pct 40.8 · baseline_n 24070

Order book NOW vs AT ENTRY — source: OKX books-full depth-4000 (the percentile baseline)  (entry reference sampled 21s from fill, same book)
  Supporting wall: entry x5.7 -> now x7.8 (grew)
  Opposing wall:   now x4.6
  Imbalance:       entry 0.51 -> now 0.39 (FLIPPED)

Order-book PERCENTILE scale (baseline: 24070 snapshots of this SAME book)
  Supporting wall = 74th pct
  Opposing wall = 26th pct
  Total depth = 2934 BTC = 41th pct (sampled 10s ago)
  Imbalance = 1th pct
```

Worth noting: **the imbalance really is at the 1st percentile now** — a genuine extreme, ask-heavy,
which actually *supports* the short. Contrast with the fabricated `0th pct` at 00:50, which was a lie
about a book sitting at the 62nd. The scale now reports extremes only when they exist. The `FLIPPED`
here is a **real** OKX-vs-OKX flip (0.5086 → 0.394), not the artefact the naive fix would have made.

---

## WHAT SHIPPED

| commit | part |
|---|---|
| `625fedc` | exit-side percentile cross-source + the `_exit_pct` provenance guard |
| `838481f` | no-op TIGHTEN: tier budget preserved, exchange stop no longer churned |
| `957f980` | three operator-card labels (`5M-STRUCTURE`, imbalance source, ADX timeframes) |

**OPEN-ITEMS updated** (§0 filters, §2.4, new §2.4a/2.19/2.20/2.21/2.22, §2.5): the criterion
restart and its reasoning · the vpos 86 verdict log with R at each verdict · ADX-on-forming-candle
recorded next to the volume forming-candle fix · the volume-ceiling replication with confounds
stated · depth-at-6th-percentile as an open question.

**Infra fix found while publishing:** 57 root-owned files and git objects in the botuser
`kola-reports` clone were blocking publication — the exact landmine recorded on 17.07. Fixed with
`chown -R botuser` + `core.sharedRepository=group` + setgid. Publishing works again from botuser.

**Not touched:** entry logic, scoring, weights, the minority-zeroing rule, `EXIT_ADVISOR_DRYRUN`,
`WALL_TRAIL_LIVE_ENABLED`, the wall-rule zero weights, sizing, Mercury-SOL.

---

## THE THING I WOULD PUT IN FRONT OF YOU

The advisor has now called `close` three times running on a position sitting at −0.44R with its stop
0.56R away. It is blocked by DRYRUN by design, and the criterion that would let it act has just been
reset to 0 of ~10 — so on the current rules it needs ten more clean closes before it can ever act on
a call like this. **That is the rule working as written, not a malfunction.**

To be exact about their status, since it matters: **all three `close` calls were themselves fed a
corrupted book block** — they predate `625fedc` and are in the contamination ledger. What makes them
worth looking at anyway is that their stated reasoning does not rest on the book: all three cite the
**regime flip** (15m/5m turning bull, bullish I-CHOCH and OB created against the short), which is
measured on price and is unaffected by the percentile defect. That is an argument for reading them,
not for counting them. **They remain uncounted, and the first verdict — the `hold` at −0.01R — is
what §2.4 would measure for this position if it were counted at all.**

---

## THE FULL PATCH AS SHIPPED — `12b4df2..957f980`

```diff
diff --git a/titan-bot/claude_advisor.py b/titan-bot/claude_advisor.py
index f78467d..7668797 100755
--- a/titan-bot/claude_advisor.py
+++ b/titan-bot/claude_advisor.py
@@ -528,6 +528,62 @@ def consult_for_close_rich(ctx):
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
@@ -536,16 +592,7 @@ def consult_for_close_rich(ctx):
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
diff --git a/titan-bot/indicators.py b/titan-bot/indicators.py
index 2e3ce98..2db82a8 100755
--- a/titan-bot/indicators.py
+++ b/titan-bot/indicators.py
@@ -437,13 +437,31 @@ def _fmt(x, spec='.2f', dash='n/a'):
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
@@ -453,9 +471,15 @@ def telegram_block(snap: Dict[str, Optional[float]], primary_tf: str = '5m') ->
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
diff --git a/titan-bot/main.py b/titan-bot/main.py
index 8275698..49bf9cf 100644
--- a/titan-bot/main.py
+++ b/titan-bot/main.py
@@ -2234,12 +2234,56 @@ def _handle_5m_trigger(parsed, symbol, direction, signal_name):
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
@@ -2290,10 +2334,16 @@ def _entry_book_pct(walls):
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
@@ -2301,7 +2351,8 @@ def _entry_book_pct(walls):
             ).fetchone()
         if row:
             out['depth_btc'] = row[1]
-            out['depth_pct'], _ = _exit_pct('total_depth_btc', row[1])
+            out['depth_pct'], _ = _exit_pct(
+                'total_depth_btc', row[1], BOOK_SRC_OKX_4000)
             try:
                 out['depth_age_s'] = int((
                     datetime.now(timezone.utc) - datetime.fromisoformat(row[0])
@@ -2426,28 +2477,109 @@ def _build_exit_context(vpos, symbol, side, exit_signal_name, trigger):
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
@@ -2467,7 +2599,14 @@ def _build_exit_context(vpos, symbol, side, exit_signal_name, trigger):
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
diff --git a/titan-bot/microstructure.py b/titan-bot/microstructure.py
index 4f0a328..9024ae6 100755
--- a/titan-bot/microstructure.py
+++ b/titan-bot/microstructure.py
@@ -353,16 +353,15 @@ def capture_and_persist_sync(exchange, symbol, db_path, trade_row_id):
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
@@ -377,7 +376,28 @@ def format_telegram_block(book_summary, tape_summary, saved_status):
 
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
diff --git a/titan-bot/signal_matrix.py b/titan-bot/signal_matrix.py
index 04169a4..a871c9e 100755
--- a/titan-bot/signal_matrix.py
+++ b/titan-bot/signal_matrix.py
@@ -135,6 +135,32 @@ SIGNAL_DICTIONARY = {
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
 
@@ -537,7 +563,9 @@ def format_for_telegram(res):
         else:
             tag = (f"{b['net_direction']} +{b['contribution']:.2f}"
                    if b['contribution'] > 0 else "—")
-        parts.append(f"  • {cat}: {tag}  ({b['signal_count']} sig)")
+        # Display label only — `cat` stays the internal key everywhere else.
+        parts.append(f"  • {CATEGORY_DISPLAY_LABEL.get(cat, cat)}: {tag}  "
+                     f"({b['signal_count']} sig)")
     return "\n".join(parts)
 
 
diff --git a/titan-bot/virtual_trader.py b/titan-bot/virtual_trader.py
index 44edc6d..20cae5b 100755
--- a/titan-bot/virtual_trader.py
+++ b/titan-bot/virtual_trader.py
@@ -1622,6 +1622,72 @@ def _run_recheck_tier(exchange, row, last, tier, send_tg):
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
+        # "Did it change?" is asked AT EXCHANGE PRECISION, with no epsilon at all.
+        # The first version of this used `abs(new_sl - current_sl) <= entry_price *
+        # 1e-7`. That is safe at every price this bot has ever traded — 15x below a
+        # tick at 63k, 5x at 200k — but it scales the tolerance with PRICE while the
+        # BTC tick is FIXED at 0.1, so the margin shrinks as price rises and reaches
+        # exactly one tick at BTC $1M, where a genuine one-tick tighten would be
+        # misread as a no-op. A silent assumption about tick size, in the one branch
+        # whose entire job is to decide whether the stop moved.
+        #
+        # Quantising BOTH sides through the exchange's own precision removes the
+        # assumption instead of tuning it: new_sl is already the product of
+        # price_to_precision, so comparing it against current_sl put through the
+        # SAME function compares two numbers on the exchange's own grid. Equality is
+        # then exact rather than approximate — two identical decimal strings parse to
+        # identical floats — and it is correct for any symbol and any tick size,
+        # including ones this bot does not trade yet.
+        _cur_q = float(exchange.price_to_precision(symbol, current_sl))
+        if new_sl == _cur_q:
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
@@ -2102,6 +2168,22 @@ def _process_position(exchange, row, last, send_tg):
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
```
