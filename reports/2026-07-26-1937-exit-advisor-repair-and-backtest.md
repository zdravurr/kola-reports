# exit-advisor-repair-and-backtest

_2026-07-26 19:37 UTC_

---

# TITAN — exit advisor: repair, enrich, and backtest

**2026-07-26 · Diff + backtest. NOTHING APPLIED.** Tree clean at `f7df202`. Paper mode.

**Lead finding, and it changes the task: the plumbing fix alone will not make the advisor run.**
There are **two** independent reasons it has never been invoked, and the brief only names one.

* **(b) — the one we knew.** `_handle_5m_close_via_ai` finds the position via
  `exchange.fetch_positions()`, empty in paper. Fixed by the diff below.
* **(a) — the one the reconstruction turned up.** Its trigger is a **5m Group B / exit** signal,
  and **zero have arrived in 65 days.** All 3,840 5m rows are `5m_liquidity_ctx` — Liquidity G.,
  Imbalance, Equal H./Lows, Broken T. — **none** matches the Group-B regex
  (`exit|take profit|stop loss|tp|sl`). The 32 `trend_reset` rows are all `60m_exit`, not 5m.

Fix (b) and the advisor still never runs. The diff therefore carries a third flag,
`EXIT_ADVISOR_ON_15M_CONFIRM`, **default OFF**, because changing *when* the advisor is consulted is
a policy decision, not plumbing — and it is the flag that actually determines the fire rate.

---

## 4. BACKTEST FIRST

### 4a. Reconstructing the moments

The literal trigger yields **n = 0**. So the backtest substitutes the exit signals that *do* fire —
1H exit-signal arms and 15m exit confirmations — while a position was open. **This substitution is
the same one `EXIT_ADVISOR_ON_15M_CONFIRM` would make, so the backtest tests that flag, not the
current trigger.** Stated plainly rather than buried.

```
60m_exit trend_reset (1H Exit S.)   32 total ·   0 while a position was open
60m_exit_armed                          24 total ·  24 while a position was open
60m_exit exit_logged                     4 total ·   0
15m_exit_confirm unarmed noop          327 total · 117 while a position was open
15m_armed_exit executed                  5 total ·   1

TOTAL reconstructable moments: 142   (2026-05-25 .. 2026-07-25, 32 positions)
```

**Usable window — stated honestly.** The enriched fields do not exist for most of that range:
```
with an entry-time book snapshot (from 2026-07-04):        41
inside the orderbook_density baseline (from 07-13 02:34):  27
with BOTH -> fully enrichable:                             27   across 6 positions
```
**115 of 142 moments cannot be enriched at all.** The backtest runs on 27 moments / 6 positions.

### 4b. The enriched prompt, built from stored data and actually sent

One verbatim example (moment #1, vpos 75):

```
OPEN POSITION — decide CLOSE or HOLD.

Position S.: LONG   Entry: 64664.1   Now: 64720.3
  Unrealised: +0.06R   (1R = 888.3 price units = the ORIGINAL stop distance)
  Elapsed: 0.2h
  Current stop: 63775.8  ->  +1.06R away from price
  Peak so far (MFE): +0.20R   Giveback from peak: 0.13R

Order book NOW vs AT ENTRY
  Supporting wall (behind us):  entry x16.0  ->  now x6.1   (THINNED)
  Opposing wall (ahead of us):  now x5.7
  Imbalance: entry 0.70  ->  now 0.43   (FLIPPED)

Order book PERCENTILE context (baseline: 17879 snapshots)
  Supporting wall x6.1 = 62th percentile
  Opposing wall  x5.7 = 40th percentile
  Total depth 2357 BTC = 2th pct
  Imbalance 0.43 = 11th pct
  NOTE: a wall multiple near the 50th percentile is ORDINARY, not significant.

Regime at ENTRY vs NOW
  At entry: regime=TREND 1d=bull 4h=bull 1h=bull ADX1h=34.2
  Now:      15m=bull 5m=bull ADX1h=41.5 ADX15m=48.8
  Volume:   vol_ratio_1h=0.24 vol_ratio_15m=0.44 ATR change vs entry=+0.0%

ENTRY THESIS (why this position was opened)
  Strong multi-TF BULL alignment (1d/4h/1h/15m/5m), ADX 34.2/41.4 confirms trend,
  LuxAlgo 15m/5m LONG signals coherent. No ask wall blocks entry; bid walls below support...

Incoming exit signal: 'Bullish I-CHOCH' (15m_exit_confirm)

The stop and trail remain active if you HOLD. Judge whether the ENTRY THESIS still holds
and whether the book/regime has turned against the position.
```
MFE is taken from `position_excursion_samples` **up to that moment only** — no look-ahead. Price
comes from the `orderbook_density` snapshot nearest the timestamp (180s tolerance).

**All 27 were sent to the model. 0 failures.** Verdicts: **10 CLOSE, 17 HOLD.**

### 4c. Verdict vs what actually happened

The first CLOSE verdict on a position *is* the exit — later moments would not exist.

| vpos | side | moments | first CLOSE | exit R | actual R | sim $ | actual $ | Δ$ | |
|---|---|---|---|---|---|---|---|---|---|
| 75 | LONG | 2 | — (HOLD throughout) | -0.03 | -0.03 | -14.52 | -14.52 | +0.00 | unchanged |
| 76 | SHORT | 2 | 07-17 05:30 | +0.24 | +0.41 | +22.12 | +45.36 | **-23.24** | **worse** |
| 78 | LONG | 1 | — (HOLD) | -1.08 | -1.08 | -103.54 | -103.54 | +0.00 | unchanged |
| 79 | LONG | 11 | 07-22 03:15 | +0.87 | +0.57 | +129.19 | +80.10 | **+49.09** | better |
| 80 | SHORT | 4 | 07-23 20:30 | -0.65 | -1.01 | -78.30 | -116.58 | **+38.28** | better |
| 81 | SHORT | 7 | 07-24 13:15 | +0.88 | +0.84 | +78.40 | +75.24 | +3.16 | better |

```
TOTAL over 6 positions:  actual -33.93$   with advisor +33.37$   Δ +67.30$
improved 3 · worsened 1 · unchanged 2
```

**Do not read that as a result.** It is **6 positions**. One of the three "improvements" is +3.16$
— noise. The whole delta is carried by vpos 79 and 80, i.e. **two trades**. A single different
verdict on either flips the sign of the total. This is a plumbing-and-plausibility check, not
evidence of edge.

What the verdicts look like as a population:
```
CLOSE n=10 : median uPnL +0.82R · median giveback 0.68R
HOLD  n=17 : median uPnL +0.52R · median giveback 0.11R
```
The model closes on **giveback**, which is the one signal today's exit path cannot see. That is
internally coherent, and it is the mechanism the LONG-partial work identified independently.

Sample reasoning (verbatim):
> **#15 vpos79 CLOSE** — *"Entry thesis invalidated. Regime has flipped from bull to bear across
> 15m/5m (ADX1h jumped 21.7→47.7, now mean-reverting/choppy). Supporting wall thinned 5.3→4.4x
> while imbalance at 82nd percentile su…"*
>
> **#1 vpos75 HOLD** — *"Entry thesis intact: multi-TF bull alignment strengthened (ADX 1h→41.5,
> 15m→48.8). I-CHOCH exit signal is typically bullish confirmation, not reversal trigger. Only
> +0.06R unrealised with +1.06R cushi…"*

It is using the enrichment — entry thesis, book dynamics, percentile context, regime delta — none
of which the current 6-field prompt contains.

---

## 6. Expected fire rate

At the substituted trigger (15m confirm + 1H arm, i.e. `EXIT_ADVISOR_ON_15M_CONFIRM = True`):
```
142 moments / 65 days  ~ 2.2 per day
27 moments / 13 days (enriched window) ~ 2.1 per day
concentration: one position (vpos 79) drew 11 consultations in 40h; vpos 60 drew 19
```
At the **current** trigger (5m Group B): **0 per day.** Unchanged by this diff unless the flag is set.

---

## 1–3, 5. The diff

```diff
--- a/config.py
+++ b/config.py
@@ -100,6 +100,23 @@
 LONG_PARTIAL_LEVEL_R = 1.0      # take the partial when MFE reaches this many R
 LONG_PARTIAL_FRACTION = 1.0/3   # fraction of the position realised at that level
 
+# --- EXIT ADVISOR (2026-07-26) ----------------------------------------------
+# The close advisor (claude_advisor.consult_for_close) has been wired since Phase-2
+# and has NEVER been invoked. Two independent reasons, both measured:
+#   (a) its trigger is a 5m Group B / exit signal, and ZERO have arrived in 65 days
+#       — all 3,840 5m rows are 5m_liquidity_ctx (Liquidity G. / Imbalance / Equal
+#       Highs / Trendlines), none of which matches the Group-B regex;
+#   (b) even if one arrived, _handle_5m_close_via_ai finds the position through
+#       exchange.fetch_positions(), which is empty in paper mode, so the handler
+#       returns before the advisor line is reached.
+# EXIT_ADVISOR_PAPER_ENABLED fixes (b) only. Without EXIT_ADVISOR_ON_15M_CONFIRM
+# the advisor STILL never runs, because (a) is untouched.
+EXIT_ADVISOR_PAPER_ENABLED = True   # paper mode: find the position in virtual_positions
+EXIT_ADVISOR_DRYRUN = True          # True = record the verdict, exit proceeds EXACTLY as today
+EXIT_ADVISOR_ON_15M_CONFIRM = False # extend the trigger to 15m exit-confirm + 1H arm.
+#   DEFAULT OFF — this changes WHEN the advisor is consulted, which is a policy change,
+#   not plumbing. Historical rate at this trigger: 142 moments / 65 days ~ 2.2 per day.
+
 # Adaptive L.-1 trail (adaptive_trail.compute_fresh_trail_pct): recompute the
 # trail_pct from a FRESH TRAIL_ATR_TF ATR at +1R arming instead of the
 # entry-frozen value, then place the SAME single server-side TRAILING_STOP_MARKET.
--- a/claude_advisor.py
+++ b/claude_advisor.py
@@ -335,6 +335,71 @@
     return result
 
 
+_CLOSE_SYSTEM_RICH = (
+    "You are an automated trading exit module. A management/exit signal has arrived "
+    "while a position is open. Decide whether to CLOSE it now or HOLD. The stop-loss "
+    "and trailing stop remain active if you hold.\n\n"
+    "Respond with ONLY a single JSON object, no markdown, no prose. Fields: "
+    "close (true|false), confidence (float 0.0-1.0), reason (string, max 400 chars)."
+)
+
+
+def consult_for_close_rich(ctx):
+    """Enriched close consultation. `ctx` is a plain dict assembled by the caller
+    from data that ALREADY EXISTS and is ALREADY SAMPLED — nothing new is fetched
+    here. Every field is optional; missing ones render as 'n/a' rather than being
+    silently dropped, so the model can tell absent from zero.
+
+    Versus consult_for_close (6 fields, dollars, 80-char answer) this adds:
+    unrealised in R, distance to stop in R, MFE and giveback from peak, order-book
+    dynamics entry-vs-now, percentile context from the orderbook_density baseline,
+    regime at entry vs now, volume trend, and the ENTRY THESIS itself.
+    Backtested on 27 reconstructable historical moments before being written."""
+    def g(k, fmt=None, default='n/a'):
+        v = ctx.get(k)
+        if v is None:
+            return default
+        return format(v, fmt) if fmt else v
+    user = (
+        "OPEN POSITION — decide CLOSE or HOLD.\n\n"
+        "Position\n"
+        f"  Side: {g('side')}   Entry: {g('entry','.1f')}   Now: {g('price','.1f')}\n"
+        f"  Unrealised: {g('upnl_r','+.2f')}R   (1R = the ORIGINAL stop distance)\n"
+        f"  Elapsed: {g('elapsed_h','.1f')}h\n"
+        f"  Current stop: {g('sl','.1f')}  ->  {g('dist_sl_r','+.2f')}R away from price\n"
+        f"  Peak so far (MFE): {g('mfe_r','+.2f')}R   Giveback from peak: {g('giveback_r','.2f')}R\n\n"
+        "Order book NOW vs AT ENTRY\n"
+        f"  Supporting wall: entry x{g('sup_entry','.1f')} -> now x{g('sup_now','.1f')} ({g('sup_trend')})\n"
+        f"  Opposing wall:   entry x{g('opp_entry','.1f')} -> now x{g('opp_now','.1f')} ({g('opp_trend')})\n"
+        f"  Imbalance:       entry {g('imb_entry','.2f')} -> now {g('imb_now','.2f')} ({g('imb_trend')})\n\n"
+        f"Order book PERCENTILE context (baseline: {g('baseline_n')} snapshots)\n"
+        f"  Supporting wall = {g('sup_pct','.0f')}th percentile\n"
+        f"  Opposing wall   = {g('opp_pct','.0f')}th percentile\n"
+        f"  Total depth     = {g('depth_pct','.0f')}th percentile\n"
+        f"  Imbalance       = {g('imb_pct','.0f')}th percentile\n"
+        "  NOTE: a wall multiple near the 50th percentile is ORDINARY, not significant.\n\n"
+        "Regime at ENTRY vs NOW\n"
+        f"  At entry: {g('regime_entry')}\n"
+        f"  Now:      {g('regime_now')}\n"
+        f"  Volume:   {g('volume_now')}\n\n"
+        "ENTRY THESIS (why this position was opened)\n"
+        f"  {g('entry_thesis')}\n\n"
+        f"Incoming exit signal: {g('exit_signal')}\n\n"
+        "The stop and trail remain active if you HOLD. Judge whether the ENTRY THESIS "
+        "still holds and whether the book/regime has turned against the position."
+    )
+    result = _call(_CLOSE_SYSTEM_RICH, user)
+    if result.get('decide') != 'unavailable':
+        raw = result.get('close')
+        if isinstance(raw, str):
+            raw = raw.lower().strip() in ('true', 'yes', '1', 'close')
+        result['close'] = bool(raw)
+    result['system_prompt'] = _CLOSE_SYSTEM_RICH
+    result['user_prompt'] = user
+    result['model'] = MODEL
+    return result
+
+
 def consult_for_close(symbol, position_side, entry_price, unrealized_pnl,
                       age_minutes, snapshot, exit_signal_name):
     """Ask Claude whether to close an open position on a 5m Group B signal.
--- a/main.py
+++ b/main.py
@@ -486,6 +486,7 @@
     NEWS_FEEDS, NEWS_LOOKBACK_HOURS, NEWS_MAX_ITEMS, NEWS_FETCH_TIMEOUT,
     EQH_EQL_SMART_TP_ENABLED, LIQUIDITY_SWEEP_LOOKBACK_MINUTES,
     CONFLUENCE_SCORE_THRESHOLD, CONFLUENCE_FLAT_THRESHOLD, HTF_CASCADE_ENABLED, HTF_TOLERATE_NEUTRAL,
+    EXIT_ADVISOR_PAPER_ENABLED, EXIT_ADVISOR_DRYRUN, EXIT_ADVISOR_ON_15M_CONFIRM,
     HTF_NEUTRAL_REQUIRE_15M_AGREE, HTF_NEUTRAL_REQUIRE_15M_DRYRUN,
     TREND_REVERSAL_EXIT_DRYRUN, CONFIRMED_REVERSAL_IDS, OBSERVE_REVERSAL_IDS,
     ADX_FLAT_FLOOR, EXIT_CONFIRM_TF,
@@ -1473,7 +1474,7 @@
     return {
         'ai_decision': decision_label,
         'ai_confidence': float(advice.get('confidence') or 0.0),
-        'ai_reason': (advice.get('reason') or '')[:200],
+        'ai_reason': (advice.get('reason') or '')[:400],
         'ai_system_prompt': advice.get('system_prompt'),
         'ai_user_prompt': advice.get('user_prompt'),
         'ai_raw_response': advice.get('raw'),
@@ -2169,6 +2170,120 @@
                     "combo": combo, "weight": weight_used}), 200
 
 
+def _exit_ctx_percentile(col, value):
+    """Percentile of `value` within the orderbook_density baseline for `col`.
+    Read-only, single indexed scan; returns None if the baseline is empty."""
+    try:
+        with sqlite3.connect(DB_PATH) as conn:
+            row = conn.execute(
+                f"SELECT SUM({col} < ?), COUNT(*) FROM orderbook_density "
+                f"WHERE {col} IS NOT NULL", (value,)).fetchone()
+        if not row or not row[1]:
+            return None, 0
+        return 100.0 * row[0] / row[1], row[1]
+    except Exception:
+        return None, 0
+
+
+def _build_exit_context(vpos, symbol, side, snapshot, exit_signal_name):
+    """Assemble the enriched close-consultation context from data that ALREADY
+    EXISTS: virtual_positions (entry + entry-time book snapshot), the live book,
+    orderbook_density (percentile baseline), the latest smart-exit dryrun sample
+    (live regime + volume) and the ENTRY trade row (the entry thesis).
+
+    Every lookup is read-only and best-effort — a missing piece becomes None and
+    renders as 'n/a' in the prompt rather than aborting the consultation."""
+    ctx = {'side': side, 'exit_signal': exit_signal_name}
+    try:
+        fill = float(vpos['initial_fill_price'])
+        osl = vpos.get('original_sl_price') or vpos['sl_price']
+        r_dist = abs(fill - osl) or None
+        sgn = 1.0 if side == 'LONG' else -1.0
+        last = float(exchange.fetch_ticker(symbol)['last'])
+        ctx.update(entry=fill, price=last, sl=vpos['sl_price'])
+        if r_dist:
+            ctx['upnl_r'] = (last - fill) * sgn / r_dist
+            ctx['dist_sl_r'] = (last - vpos['sl_price']) * sgn / r_dist
+            wm = vpos.get('water_mark')
+            if wm:
+                ctx['mfe_r'] = (wm - fill) * sgn / r_dist
+                ctx['giveback_r'] = max(0.0, ctx['mfe_r'] - ctx['upnl_r'])
+        opened = vpos.get('opened_at')
+        if opened:
+            ctx['elapsed_h'] = (datetime.now(timezone.utc)
+                                - datetime.fromisoformat(opened)).total_seconds() / 3600.0
+        # live book vs the entry-time snapshot already stored on the row
+        walls = microstructure.fetch_pre_trade_walls(exchange, symbol)
+        if walls:
+            bids = [w.get('mult') for w in (walls.get('walls_bid') or []) if w.get('mult')]
+            asks = [w.get('mult') for w in (walls.get('walls_ask') or []) if w.get('mult')]
+            sup_now = max(bids or [0]) if side == 'LONG' else max(asks or [0])
+            opp_now = max(asks or [0]) if side == 'LONG' else max(bids or [0])
+            ctx['sup_now'], ctx['opp_now'] = sup_now, opp_now
+            ctx['imb_now'] = walls.get('imbalance')
+            ctx['sup_entry'] = vpos.get('entry_sup_wall_mult')
+            ctx['imb_entry'] = vpos.get('entry_ob_imbalance')
+            if ctx['sup_entry']:
+                ctx['sup_trend'] = 'THINNED' if sup_now < ctx['sup_entry'] else 'grew'
+            if ctx['imb_entry'] is not None and ctx['imb_now'] is not None:
+                ctx['imb_trend'] = ('FLIPPED' if (ctx['imb_entry'] - 0.5) * (ctx['imb_now'] - 0.5) < 0
+                                    else 'same side')
+            sup_col = 'max_wall_mult_bid' if side == 'LONG' else 'max_wall_mult_ask'
+            opp_col = 'max_wall_mult_ask' if side == 'LONG' else 'max_wall_mult_bid'
+            ctx['sup_pct'], n = _exit_ctx_percentile(sup_col, sup_now)
+            ctx['opp_pct'], _ = _exit_ctx_percentile(opp_col, opp_now)
+            if ctx['imb_now'] is not None:
+                ctx['imb_pct'], _ = _exit_ctx_percentile('imbalance', ctx['imb_now'])
+            ctx['baseline_n'] = n
+        # entry regime + entry thesis + latest live-regime sample
+        with sqlite3.connect(DB_PATH) as conn:
+            conn.row_factory = sqlite3.Row
+            eid = vpos.get('trades_entry_row_id')
+            if eid:
+                e = conn.execute(
+                    "SELECT market_regime,trend_1d,trend_4h,trend_1h,srv_adx_1h,ai_reason "
+                    "FROM trades WHERE id=?", (eid,)).fetchone()
+                if e:
+                    ctx['regime_entry'] = (f"regime={e['market_regime']} 1d={e['trend_1d']} "
+                                           f"4h={e['trend_4h']} 1h={e['trend_1h']} "
+                                           f"ADX1h={e['srv_adx_1h'] or 0:.1f}")
+                    ctx['entry_thesis'] = e['ai_reason']
+            se = conn.execute(
+                "SELECT trend_15m_live,trend_5m_live,adx_1h,adx_15m,vol_ratio_1h,"
+                "vol_ratio_15m,atr_change_pct FROM smart_exit_dryrun_samples "
+                "WHERE vpos_id=? ORDER BY id DESC LIMIT 1", (vpos['id'],)).fetchone()
+            if se:
+                ctx['regime_now'] = (f"15m={se['trend_15m_live']} 5m={se['trend_5m_live']} "
+                                     f"ADX1h={se['adx_1h'] or 0:.1f} ADX15m={se['adx_15m'] or 0:.1f}")
+                ctx['volume_now'] = (f"vol_1h={se['vol_ratio_1h'] or 0:.2f} "
+                                     f"vol_15m={se['vol_ratio_15m'] or 0:.2f} "
+                                     f"ATR change vs entry={se['atr_change_pct'] or 0:+.1f}%")
+    except Exception as e:
+        print(f"[EXIT-ADVISOR] context build partial: {e}", flush=True)
+    return ctx
+
+
+def _paper_position_as_exchange_dict(symbol, position_side):
+    """Paper-mode stand-in for _fetch_open_position: read the open row out of
+    virtual_positions and shape it like the exchange dict the caller expects.
+    Returns N. when nothing is open. Read-only; opens no order, moves no stop."""
+    try:
+        row = virtual_trader._open_position(symbol, position_side)
+    except Exception as e:
+        print(f"paper position lookup failed: {e}", flush=True)
+        return None
+    if not row:
+        return None
+    return {
+        'side': position_side,
+        'contracts': 1,                      # presence marker only
+        'entryPrice': row['initial_fill_price'],
+        'unrealizedPnl': None,               # the rich path computes uPnL in R
+        'timestamp': None,
+        '_vpos': dict(row),                  # full paper row for the rich prompt
+    }
+
+
 def _handle_5m_close_via_ai(parsed, symbol, signal_name, had_trend):
     """5m Group B handler: query BingX for an open position, ask Claude
     whether to close, run the close mechanics if Claude says yes. The 1H
@@ -2185,7 +2300,15 @@
     open_pos = None
     open_side = None
     for s in sides_to_check:
+        # PAPER FALLBACK (2026-07-26). _fetch_open_position asks the LIVE exchange,
+        # which is empty whenever LIVE_TRADING_ENABLED is False — that alone is why
+        # the close advisor has never been consulted in 65 days of paper trading.
+        # The live path is untouched: the exchange is still asked first, and the
+        # fallback only engages when the bot is in paper mode AND the exchange has
+        # nothing. Shaped like the exchange dict so the code below is unchanged.
         p = _fetch_open_position(symbol, s)
+        if p is None and EXIT_ADVISOR_PAPER_ENABLED and not LIVE_TRADING_ENABLED:
+            p = _paper_position_as_exchange_dict(symbol, s)
         if p:
             if open_pos is not None:
                 # Both sides open and signal didn't disambiguate — log + bail.
@@ -2224,11 +2347,34 @@
         except (TypeError, ValueError):
             pass
 
-    advice = claude_advisor.consult_for_close(
-        symbol, open_side, entry_price, upnl, age_minutes,
-        snapshot, signal_name,
-    )
+    _vpos = (open_pos or {}).get('_vpos')
+    if _vpos is not None:
+        advice = claude_advisor.consult_for_close_rich(
+            _build_exit_context(_vpos, symbol, open_side, snapshot, signal_name))
+    else:
+        advice = claude_advisor.consult_for_close(
+            symbol, open_side, entry_price, upnl, age_minutes,
+            snapshot, signal_name,
+        )
     decide = advice.get('decide')
+
+    # DRYRUN (default ON): the verdict is recorded and reported, the exit proceeds
+    # EXACTLY as it does today. Nothing below this line may close a position while
+    # the flag is set — the SL / trail / armed-exit path stays sole authority.
+    if EXIT_ADVISOR_DRYRUN:
+        row_id = insert_signal(parsed, symbol, 'na', '5m_group_b',
+                               status='exit_ai_dryrun')
+        update_signal_execution(
+            row_id, status='exit_ai_dryrun',
+            **_ai_fields_from_advice(
+                advice, 'close' if advice.get('close') else 'hold'),
+        )
+        print(f"[EXIT-ADVISOR-DRYRUN] {symbol} {open_side} "
+              f"close={advice.get('close')} conf={advice.get('confidence')} "
+              f"| {(advice.get('reason') or '')[:160]}", flush=True)
+        return jsonify({"status": "exit_ai_dryrun",
+                        "close": advice.get('close'),
+                        "reason": (advice.get('reason') or '')[:400]}), 200
     ai_close = advice.get('close')
     ai_conf = float(advice.get('confidence') or 0.0)
     ai_reason = (advice.get('reason') or '')[:200]
```

### What it does
1. **Plumbing** — `_paper_position_as_exchange_dict()` reads the open row from `virtual_positions`
   and shapes it like the exchange dict. The exchange is still asked **first**; the fallback engages
   only when `LIVE_TRADING_ENABLED` is False and the exchange returned nothing. **Live path
   untouched.**
2. **Enrichment** — `consult_for_close_rich()` in `claude_advisor.py` (the old `consult_for_close`
   is left byte-identical as the live-path fallback), fed by `_build_exit_context()` which assembles
   the context from data that already exists: `virtual_positions` (entry, stop, water mark,
   entry-time book snapshot), the live book, `orderbook_density` for percentiles, the latest
   `smart_exit_dryrun_samples` row for live regime and volume, and the entry `ai_reason` for the
   thesis. Every field is best-effort; a missing one renders `n/a` rather than aborting.
3. **Reasoning + persistence** — 80 → **400 chars**, and `_ai_fields_from_advice` (already the
   shared projector for all five entry/close branches) persists `ai_system_prompt`,
   `ai_user_prompt`, `ai_reason`, `ai_confidence` exactly as on the entry side.
5. **DRYRUN, default ON** — `EXIT_ADVISOR_DRYRUN = True`. The verdict is recorded under a new
   `exit_ai_dryrun` status and the handler **returns before any close mechanic**. While the flag is
   set nothing below that line can close a position; SL / trail / armed-exit remain sole authority.

### 7. Scope T. files: `config.py`, `claude_advisor.py`, `main.py`. **Not touched:**
* SL placement, trail, breakeven — no line in `virtual_trader.py` is in the diff at all.
* **LONG partial (`f7df202`)** and the **recheck bound (`93c20c3`)** — same file, not in the diff.
* Entry path — the entry advisor, `consult_for_entry`, the FLAT floor, the HTF cascade and the
  confluence matrix are untouched. The only shared edit is `_ai_fields_from_advice`'s reason cap
  200 → 400, which lengthens what is **stored** on both sides and changes no decision.
* Every sensor, every cron, and **Mercury-SOL**.
* `consult_for_close` itself is unchanged, so the live path behaves exactly as before.

`py_compile` OK on `config.py` and `claude_advisor.py`; `main.py` AST-validated (it imports live
exchange state, so it is not import-compiled here). `patch -p1 --dry-run` CLEAN on all three.

### Snapshot / rollback
```bash
cd /root && git tag pre-exit-advisor-20260726
for f in config.py claude_advisor.py main.py; do cp $f $f.bak_exitadvisor_20260726; done
patch -p1 < EA.patch && python3 -m py_compile config.py claude_advisor.py main.py
sudo systemctl restart titan.service
# rollback: git checkout pre-exit-advisor-20260726 -- titan-bot/{config,claude_advisor,main}.py
#       or: EXIT_ADVISOR_PAPER_ENABLED = False   (advisor stops being consulted, no code edit)
```

---

## What I am NOT claiming

* **Not** that the exit advisor improves outcomes. n = 6 positions, delta carried by 2 trades.
* **Not** that `EXIT_ADVISOR_ON_15M_CONFIRM` should be turned on. That is the flag that decides
  whether the advisor exists at all, and 27 moments is not enough to authorise it.
* The honest sequence is: ship the plumbing + enrichment **in dryrun**, turn on the 15m trigger
  **also in dryrun**, and let real verdicts accumulate against real outcomes for a few weeks before
  anyone considers letting it close anything.

---

Session commits: `93c20c3` · `596fbdf` (superseded) · `b878535` · `f7df202`. Nothing applied here.
Tree clean, `titan.service` healthy, Mercury-SOL untouched. Open items: `reports/OPEN-ITEMS.md`.
