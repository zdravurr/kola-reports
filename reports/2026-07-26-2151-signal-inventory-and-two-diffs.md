# signal-inventory-and-two-diffs

_2026-07-26 21:51 UTC_

---

# TITAN — signal inventory · entry-advisor audit · two diffs (Parts 4-5 NOT applied)

**2026-07-26 · Parts 1-3 read-only · Parts 4-5 diffs prepared, NOTHING WRITTEN · Part 6 recorded.**
Tree clean at `f7df202`. Stopping for approval as instructed.

**Three findings worth leading with, one of which corrects me again:**

1. **The 15m entry stream was never ignored — only unrecorded.** `signal_matrix.record_signal` runs
   before the branch, so HyperWave / Reversal / Divergence have always carried their MOMENTUM weight
   (0.7-1.0) in the decision. What is missing is the DB row. My earlier phrasing ("discarded") was
   wrong: the loss is analytical, not decisional.
2. **The entry advisor already names two of the three tiers** — "15m: HyperWave Signal Up",
   "5m trigger: Bullish OB Created" — but **never the 1H signal**, by design
   (`AI_ADVISOR_HIDE_1H = True`). It sees "1h: BULL, ADX 16.9", never "Trend C. Up".
3. **10 of the 32 5m entry signals never trigger an entry** — they are LIQUIDITY-category and land
   as `5m_liquidity_ctx`. They still carry matrix weight; they just cannot open a trade.

---

## PART 1 — Signal inventory

Sources: `trades` (65 days) **and** the app journal via syslog (2026-06-28 .. 07-26, 6,027
`WEBHOOK_IN` events) — the 15m entry stream is absent from the DB, so journal-only for that tier.

### ENTRY 1H — 15 configured (2 Contrarian deliberately off, not counted)
All 15 arrive. Every one is `TREND` category and sets the 1H trend slot + matrix TREND points.
```
signal                     cat    dir    weight   journal   DB   classified as
Trend C. Up/Down      TREND  L/S      1.0      10/9   32/31  1h_trend_set
Bullish/Bearish C.+   TREND  L/S      1.0       7/8   21/21  1h_trend_set
Smart T. Bullish/Bear   TREND  L/S      0.9       5/4   12/11  1h_trend_set
Neo C. Bullish/Bearish  TREND  L/S      0.9       1/1     2/2  1h_trend_set
Trend T. Up/Down       TREND  L/S      0.9       3/3     6/7  1h_trend_set
Bullish/Bearish C.    TREND  L/S      0.7       8/6   23/21  1h_trend_set
Any B./Bear C. TREND  L/S      0.7     15/14   44/41  1h_trend_set
Exit S.                EXIT   NEUTRAL  0.0        19      61  60m_exit / 60m_exit_armed
```

### ENTRY 15m — 10 configured, `task="confirmation"`
**All 10 arrive. All carry MOMENTUM weight. NONE has ever been written to the database.**
```
signal                     weight   journal   DB
HyperWave Signal Up/Down     0.7     161/153   0/0
HyperWave OS Up / OB Down    1.0       30/37   0/0
Reversal Up / Down           0.7       31/38   0/0
Reversal Up + / Down +       1.0       10/18   0/0
Bullish / Bearish D. 0.8       15/20   0/0
```

### ENTRY 5m — 32 configured, `task="price_action"`. All 32 arrive.
**22 are EXECUTION → can trigger an entry.** Top by volume: Within B./Bullish OB (0.7,
4391/3636 rows), OB Entered (0.8, 988/890), OB Created (0.5, 486/431), OB Mitigated (0.5, 370/349),
Breaker (0.7, 370/352), I-BOS (0.7, 306/233), I-CHOCH (0.7), I-CHOCH+ (0.9), S-BOS (0.9),
S-CHOCH (0.8), S-CHOCH+ (1.0).

**10 are LIQUIDITY → `5m_liquidity_ctx`, weight but no trigger:**
Bullish/Bearish L. Grab (1.0), Equal H./Lows (0.9), New I. (0.7),
Imbalance M. (0.5), Broken Up/Downtrendline (0.7).

### The four answers
**(a) Arrive but IGNORED by the logic:** *none.* Every listed signal reaches
`signal_matrix.record_signal` and contributes points. The closest thing to "ignored" is the
10 LIQUIDITY 5m signals, which weigh but cannot trigger — that is by design.

**(b) Arrive and carry WEIGHT:** all of them, per the tables above (TREND 0.7-1.0,
MOMENTUM 0.7-1.0, EXECUTION 0.5-1.0, LIQUIDITY 0.5-1.0).

**(c) NEVER arrive:** only `Any B. Contrarian` — and `Any B. Contrarian` has 2 legacy
rows and nothing recent. Both are **deliberately disabled**, so this is not a defect.

**(d) Arriving but on NO list:** one legacy `close_long` row. Nothing else.

---

## PART 2 — Which signals produced which entries

All 49 closed positions, traced to their three tiers (1H from the last preceding `1h_trend_set`,
15m recovered from the entry advisor's stored prompt, 5m from `tv_action`).

**By 1H signal** — `n/a` means no 15m confirmation was recorded in the prompt.
```
Bearish C.+     n= 4  net +1062.90  win 3     Trend C. Down    n= 3  net  -56.72  win 1
Trend T. Down         n= 6  net  +561.31  win 4     Trend C. Up      n= 6  net  -68.11  win 2
Any B. Confirmation  n= 5  net  +132.86  win 2     Bearish C.  n= 5  net  -81.45  win 3
Neo C. Bullish         n= 1  net    +3.32  win 1     Trend T. Up       n= 3  net -132.88  win 0
Smart T. Bullish       n= 2  net    +0.02  win 1     Bullish C.+ n= 2  net -218.21  win 0
Smart T. Bearish       n= 6  net   -39.62  win 4     Any B. Confirm.  n= 6  net -424.03  win 1
```
**By 15m confirmation**
```
n/a (none recorded)      n=12  net +784.37  win 6      Reversal Up            n= 1  net -104.59  win 0
HyperWave Signal D.    n=15  net +624.66  win10      HyperWave OB Sig D.  n= 2  net -301.76  win 0
Reversal D.            n= 3  net +232.50  win 1      HyperWave Signal Up    n=16  net -495.78  win 5
```
**By 5m trigger**
```
Bearish OB Created  n=6 +786.00 w4   Within B. OB  n=11  -72.81 w5
Bearish I-BOS       n=5 +579.83 w3   Bearish OB Entered n= 3  -94.74 w2
Bearish I-CHOCH+    n=1 +435.32 w1   Bullish S-BOS      n= 2 -105.39 w0
Bullish S-CHOCH     n=1  +80.10 w1   Within B. OB  n= 7 -179.88 w2
Bearish OB Mitigated n=1 +21.39 w1   Bullish OB Created n= 7 -598.00 w0
Bullish OB Entered  n=1  +15.53 w1   Bearish S-CHOCH+   n= 1  -59.11 w0
Bullish I-CHOCH+    n=2   +3.94 w2   Bullish OB Mitigated n=1  -72.79 w0
```
**Table only, no conclusions.** Almost every cell is n<=6; the largest is `Within B. OB` at
n=11. The bearish/bullish split visible here is the same LONG-vs-SHORT asymmetry already documented,
re-expressed by signal name — it is not independent evidence about any signal.

---

## PART 3 — What the entry advisor sees

Verbatim, most recent executed entry:
```
Symbol: BTC/USDT:USDT
15m: HyperWave Signal Up (direction: LONG)
5m trigger: Bullish OB Created (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 49.4388  |  Volume ratio 5m: 1.37x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 16.9 | 15m 36.7   ATR% 1h 0.219% | 15m 0.133% | 5m 0.076%
  EMA-gap: 1h 0.150% (Expanding) | 15m 0.118% (Expanding)
  Market regime: TREND | MTF alignment score: 3
Higher T. Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: NEUTRAL ... 4h: NEUTRAL ... 1h: BULL ... 15m: BULL ... 5m: BULL
Long/Short ratio: n/a
Order book (pre-trade, 8000 levels):
  Mid: $64,783.15  |  Imbalance +/-1%: 0.41 (ask-heavy)
  Massive bid walls (>4x avg vol): $64,657.50 (x4.2), $64,477.50 (x9.0)
  Massive ask walls (>4x avg vol): $64,807.50 (x11.7), $65,102.50 (x8.9)
```
Name check: **HyperWave YES · Reversal/Divergence — absent because that entry was HyperWave ·
Trend C. NO · Smart T. NO · Confirmation NO · I-BOS/I-CHOCH/OB — only the one that
triggered.**

**The gap: the 1H tier has no identity.** `AI_ADVISOR_HIDE_1H = True` (config:320) removes it
deliberately. The advisor is told the OHLCV-derived 1h state but never which LuxAlgo alert set the
trend — so it cannot distinguish `Trend C. Up` (weight 1.0, n=6, net -68) from
`Bearish C.+` (weight 1.0, n=4, net +1063).

**What adding three-tier identity would look like** — described, not applied: one line above the
existing 15m line, `1H trend set by: <signal> (weight w, set Nh ago)`, sourced from the same
`1h_trend_set` lookup already written for the exit advisor (`_entry_signals_for`). It would make the
prompt read *"1H Trend C. Up + 15m HyperWave Signal Up + 5m Bullish I-BOS"* instead of
*"aligned bullish"*. **Not proposed for this session** — it changes the entry advisor's input, which
is the entry path, and the scope excludes it.

---

## PARTS 4 + 5 — the diff (NOT applied)

```diff
--- a/config.py
+++ b/config.py
@@ -100,6 +100,23 @@
 LONG_PARTIAL_LEVEL_R = 1.0      # take the partial when MFE reaches this many R
 LONG_PARTIAL_FRACTION = 1.0/3   # fraction of the position realised at that level
 
+# --- EXIT ADVISOR (2026-07-26) ----------------------------------------------
+# consult_for_close has been wired since Phase-2 and NEVER invoked. Two reasons,
+# both measured: (a) its trigger is a 5m Group-B alert and zero have ever arrived
+# — the operator has decided NOT to create a 5m exit alert, so this stays true;
+# (b) _handle_5m_close_via_ai looks the position up via exchange.fetch_positions(),
+# empty in paper. PAPER_ENABLED fixes (b); ON_15M_CONFIRM supplies a trigger that
+# actually fires (~2.2/day); HOURLY adds a full trajectory per position, reusing
+# the smart-exit sampler which already collects the 48 fields the prompt needs.
+# DRYRUN short-circuits before every close mechanic: the advisor cannot close
+# anything regardless of verdict. SL / trail / armed-exit remain sole authority.
+EXIT_ADVISOR_PAPER_ENABLED  = True   # paper mode: find the position in virtual_positions
+EXIT_ADVISOR_DRYRUN         = True   # record the verdict; the exit proceeds EXACTLY as today
+EXIT_ADVISOR_ON_15M_CONFIRM = True   # also consult on the 15m exit-confirm / 1H-arm triggers
+EXIT_ADVISOR_HOURLY         = True   # consult once per hour per open position (sampler cadence)
+EXIT_ADVISOR_HOURLY_SEC     = 3600   # cadence; mirrors SMART_EXIT_DRYRUN_SAMPLE_SEC
+EXIT_ADVISOR_5M_CONTEXT_MIN = 90     # look-back for the 5m structure context field
+
 # Adaptive L.-1 trail (adaptive_trail.compute_fresh_trail_pct): recompute the
 # trail_pct from a FRESH TRAIL_ATR_TF ATR at +1R arming instead of the
 # entry-frozen value, then place the SAME single server-side TRAILING_STOP_MARKET.
--- a/claude_advisor.py
+++ b/claude_advisor.py
@@ -335,6 +335,77 @@
     return result
 
 
+_CLOSE_SYSTEM_RICH = (
+    "You are an automated trading exit module. Decide whether to CLOSE the open "
+    "position now or HOLD it. The stop-loss and trailing stop remain active if you "
+    "hold.\n\nRespond with ONLY a single JSON object, no markdown, no prose. Fields: "
+    "close (true|false), confidence (float 0.0-1.0), reason (string, max 400 chars)."
+)
+
+
+def consult_for_close_rich(ctx):
+    """Enriched close consultation. `ctx` is assembled by the caller from data that
+    ALREADY EXISTS and is ALREADY SAMPLED — nothing new is fetched here. Missing
+    fields render 'n/a' rather than being dropped, so absent is distinguishable
+    from zero.
+
+    Versus consult_for_close (6 fields, dollars, 80-char answer) this carries:
+    unrealised and stop distance in R, MFE and giveback from peak, order-book
+    dynamics entry-vs-now, PERCENTILE context from the orderbook_density baseline
+    (the prompt's hard-coded word "Massive" fires on every wall above 4.0x, and
+    100% of book states contain one — the percentile is what tells x5.9 from
+    ordinary), regime at entry vs now, volume trend, recent 5m structure as
+    CONTEXT ONLY, and the entry thesis INCLUDING the three signals that opened
+    the position."""
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
+        f"  Current stop: {g('sl','.1f')}  ->  {g('dist_sl_r','+.2f')}R away\n"
+        f"  Peak so far (MFE): {g('mfe_r','+.2f')}R   Giveback from peak: {g('giveback_r','.2f')}R\n\n"
+        "Order book NOW vs AT ENTRY\n"
+        f"  Supporting wall: entry x{g('sup_entry','.1f')} -> now x{g('sup_now','.1f')} ({g('sup_trend')})\n"
+        f"  Opposing wall:   now x{g('opp_now','.1f')}\n"
+        f"  Imbalance:       entry {g('imb_entry','.2f')} -> now {g('imb_now','.2f')} ({g('imb_trend')})\n\n"
+        f"Order-book PERCENTILE scale (baseline: {g('baseline_n')} snapshots)\n"
+        f"  Supporting wall = {g('sup_pct','.0f')}th pct   Opposing wall = {g('opp_pct','.0f')}th pct\n"
+        f"  Total depth = {g('depth_pct','.0f')}th pct     Imbalance = {g('imb_pct','.0f')}th pct\n"
+        "  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means\n"
+        "  nothing on its own. Judge by the percentile: ~50th is ORDINARY.\n\n"
+        "Regime at ENTRY vs NOW\n"
+        f"  At entry: {g('regime_entry')}\n"
+        f"  Now:      {g('regime_now')}\n"
+        f"  Volume:   {g('volume_now')}\n\n"
+        "Recent 5m structure (CONTEXT ONLY — never a trigger)\n"
+        f"  {g('structure_5m')}\n\n"
+        "ENTRY THESIS — the signals that opened this position\n"
+        f"  1H trend set by:   {g('sig_1h')}\n"
+        f"  15m confirmed by:  {g('sig_15m')}\n"
+        f"  5m triggered by:   {g('sig_5m')}\n"
+        f"  Advisor's reason at entry: {g('entry_thesis')}\n\n"
+        f"Consultation trigger: {g('trigger')}\n\n"
+        "The stop and trail remain active if you HOLD. Judge whether THAT specific "
+        "entry thesis is still alive and whether book/regime have turned against it."
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
@@ -2169,6 +2170,191 @@
                     "combo": combo, "weight": weight_used}), 200
 
 
+def _exit_pct(col, value):
+    """Percentile of `value` within the orderbook_density baseline. Read-only."""
+    try:
+        with sqlite3.connect(DB_PATH) as conn:
+            r = conn.execute(f"SELECT SUM({col} < ?), COUNT(*) FROM orderbook_density "
+                             f"WHERE {col} IS NOT NULL", (value,)).fetchone()
+        return (100.0 * r[0] / r[1], r[1]) if r and r[1] else (None, 0)
+    except Exception:
+        return None, 0
+
+
+def _entry_signals_for(vpos):
+    """The THREE signals that opened this position: the 1H alert that set the
+    trend, the 15m confirmation and the 5m trigger. All read from stored rows —
+    the 15m name is recovered from the entry advisor's own prompt, which records
+    it verbatim."""
+    out = {'sig_1h': None, 'sig_15m': None, 'sig_5m': None, 'entry_thesis': None}
+    try:
+        eid = vpos.get('trades_entry_row_id')
+        if not eid:
+            return out
+        with sqlite3.connect(DB_PATH) as conn:
+            conn.row_factory = sqlite3.Row
+            e = conn.execute("SELECT timestamp,tv_action,ai_reason,ai_user_prompt "
+                             "FROM trades WHERE id=?", (eid,)).fetchone()
+            if not e:
+                return out
+            out['sig_5m'] = e['tv_action']
+            out['entry_thesis'] = e['ai_reason']
+            m = re.search(r'^15m: (.+?) \(direction', e['ai_user_prompt'] or '', re.M)
+            if m:
+                out['sig_15m'] = m.group(1)
+            h = conn.execute("SELECT tv_action FROM trades WHERE signal_type='1h_trend_set' "
+                             "AND timestamp<=? ORDER BY id DESC LIMIT 1",
+                             (e['timestamp'],)).fetchone()
+            if h:
+                out['sig_1h'] = h['tv_action']
+    except Exception as _e:
+        print(f"[EXIT-ADVISOR] entry-signal lookup partial: {_e}", flush=True)
+    return out
+
+
+def _recent_5m_structure(side, minutes):
+    """Recent 5m Price Action events rendered relative to the open side.
+    CONTEXT ONLY — this never triggers anything and gates nothing."""
+    try:
+        with sqlite3.connect(DB_PATH) as conn:
+            conn.row_factory = sqlite3.Row
+            rows = conn.execute(
+                "SELECT timestamp,tv_action FROM trades WHERE tv_tf='5m' "
+                "AND tv_action IS NOT NULL AND timestamp >= datetime('now',?) "
+                "ORDER BY id DESC LIMIT 6", (f'-{int(minutes)} minutes',)).fetchall()
+        if not rows:
+            return f'no 5m structure in the last {minutes} min'
+        now = datetime.now(timezone.utc)
+        parts = []
+        for r in rows:
+            try:
+                age = (now - datetime.fromisoformat(
+                    r['timestamp'].replace(' ', 'T')).replace(tzinfo=timezone.utc)
+                ).total_seconds() / 60
+            except Exception:
+                age = -1
+            nm = r['tv_action']
+            agree = ('bullish' in nm.lower()) == (side == 'LONG')
+            parts.append(f"{nm} {age:.0f}m ago ({'with' if agree else 'AGAINST'} the {side})")
+        return ' · '.join(parts)
+    except Exception:
+        return 'n/a'
+
+
+def _build_exit_context(vpos, symbol, side, exit_signal_name, trigger):
+    """Assemble the enriched close context from data that ALREADY EXISTS:
+    virtual_positions (entry, stop, water mark, entry-time book snapshot), the
+    live book, orderbook_density (percentile scale), the latest smart-exit
+    dryrun sample (live regime + volume), recent 5m structure, and the three
+    entry signals. Best-effort: a missing piece becomes None and renders 'n/a'."""
+    ctx = {'side': side, 'exit_signal': exit_signal_name, 'trigger': trigger}
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
+            if vpos.get('water_mark'):
+                ctx['mfe_r'] = (vpos['water_mark'] - fill) * sgn / r_dist
+                ctx['giveback_r'] = max(0.0, ctx['mfe_r'] - ctx['upnl_r'])
+        if vpos.get('opened_at'):
+            ctx['elapsed_h'] = (datetime.now(timezone.utc) - datetime.fromisoformat(
+                vpos['opened_at'])).total_seconds() / 3600.0
+        walls = microstructure.fetch_pre_trade_walls(exchange, symbol)
+        if walls:
+            b = [w.get('mult') for w in (walls.get('walls_bid') or []) if w.get('mult')]
+            a = [w.get('mult') for w in (walls.get('walls_ask') or []) if w.get('mult')]
+            sup = max(b or [0]) if side == 'LONG' else max(a or [0])
+            opp = max(a or [0]) if side == 'LONG' else max(b or [0])
+            ctx.update(sup_now=sup, opp_now=opp, imb_now=walls.get('imbalance'),
+                       sup_entry=vpos.get('entry_sup_wall_mult'),
+                       imb_entry=vpos.get('entry_ob_imbalance'))
+            if ctx['sup_entry']:
+                ctx['sup_trend'] = 'THINNED' if sup < ctx['sup_entry'] else 'grew'
+            if ctx['imb_entry'] is not None and ctx['imb_now'] is not None:
+                ctx['imb_trend'] = ('FLIPPED'
+                                    if (ctx['imb_entry'] - .5) * (ctx['imb_now'] - .5) < 0
+                                    else 'same side')
+            sc = 'max_wall_mult_bid' if side == 'LONG' else 'max_wall_mult_ask'
+            oc = 'max_wall_mult_ask' if side == 'LONG' else 'max_wall_mult_bid'
+            ctx['sup_pct'], n = _exit_pct(sc, sup)
+            ctx['opp_pct'], _ = _exit_pct(oc, opp)
+            if ctx['imb_now'] is not None:
+                ctx['imb_pct'], _ = _exit_pct('imbalance', ctx['imb_now'])
+            ctx['baseline_n'] = n
+        ctx.update(_entry_signals_for(vpos))
+        ctx['structure_5m'] = _recent_5m_structure(side, EXIT_ADVISOR_5M_CONTEXT_MIN)
+        with sqlite3.connect(DB_PATH) as conn:
+            conn.row_factory = sqlite3.Row
+            eid = vpos.get('trades_entry_row_id')
+            if eid:
+                e = conn.execute("SELECT market_regime,trend_1d,trend_4h,trend_1h,srv_adx_1h "
+                                 "FROM trades WHERE id=?", (eid,)).fetchone()
+                if e:
+                    ctx['regime_entry'] = (f"regime={e['market_regime']} 1d={e['trend_1d']} "
+                                           f"4h={e['trend_4h']} 1h={e['trend_1h']} "
+                                           f"ADX1h={e['srv_adx_1h'] or 0:.1f}")
+            se = conn.execute("SELECT trend_15m_live,trend_5m_live,adx_1h,adx_15m,"
+                              "vol_ratio_1h,vol_ratio_15m,atr_change_pct "
+                              "FROM smart_exit_dryrun_samples WHERE vpos_id=? "
+                              "ORDER BY id DESC LIMIT 1", (vpos['id'],)).fetchone()
+            if se:
+                ctx['regime_now'] = (f"15m={se['trend_15m_live']} 5m={se['trend_5m_live']} "
+                                     f"ADX1h={se['adx_1h'] or 0:.1f} "
+                                     f"ADX15m={se['adx_15m'] or 0:.1f}")
+                ctx['volume_now'] = (f"vol_1h={se['vol_ratio_1h'] or 0:.2f} "
+                                     f"vol_15m={se['vol_ratio_15m'] or 0:.2f} "
+                                     f"ATR change vs entry={se['atr_change_pct'] or 0:+.1f}%")
+    except Exception as e:
+        print(f"[EXIT-ADVISOR] context build partial: {e}", flush=True)
+    return ctx
+
+
+def consult_exit_advisor(vpos_row, symbol, side, exit_signal_name, trigger):
+    """Run the enriched close consultation and PERSIST the verdict exactly as the
+    entry side does (system prompt, user prompt, reason, confidence).
+
+    This function has no access to any close mechanic and can never close a
+    position. Whether an exit happens is decided by the callers, and while
+    EXIT_ADVISOR_DRYRUN is True every caller returns before its close path."""
+    ctx = _build_exit_context(dict(vpos_row), symbol, side, exit_signal_name, trigger)
+    advice = claude_advisor.consult_for_close_rich(ctx)
+    try:
+        row_id = insert_signal(parse_alert({'action': exit_signal_name}), symbol, 'na',
+                               'exit_ai_dryrun', status='exit_ai_dryrun')
+        if row_id:
+            update_signal_execution(
+                row_id, status='exit_ai_dryrun',
+                **_ai_fields_from_advice(advice,
+                                         'close' if advice.get('close') else 'hold'))
+    except Exception as e:
+        print(f"[EXIT-ADVISOR] persist failed: {e}", flush=True)
+    print(f"[EXIT-ADVISOR-DRYRUN] trigger={trigger} {symbol} {side} "
+          f"close={advice.get('close')} conf={advice.get('confidence')} "
+          f"| {(advice.get('reason') or '')[:200]}", flush=True)
+    return advice
+
+
+def _paper_position_as_exchange_dict(symbol, position_side):
+    """Paper stand-in for _fetch_open_position: read the open virtual_positions row
+    and shape it like the exchange dict the caller expects. Read-only — opens no
+    order and moves no stop. Returns N. when nothing is open."""
+    try:
+        row = virtual_trader._open_position(symbol, position_side)
+    except Exception as e:
+        print(f"paper position lookup failed: {e}", flush=True)
+        return None
+    if not row:
+        return None
+    return {'side': position_side, 'contracts': 1,
+            'entryPrice': row['initial_fill_price'], 'unrealizedPnl': None,
+            'timestamp': None, '_vpos': dict(row)}
+
+
 def _handle_5m_close_via_ai(parsed, symbol, signal_name, had_trend):
     """5m Group B handler: query BingX for an open position, ask Claude
     whether to close, run the close mechanics if Claude says yes. The 1H
@@ -2185,7 +2371,13 @@
     open_pos = None
     open_side = None
     for s in sides_to_check:
+        # PAPER FALLBACK (2026-07-26). _fetch_open_position asks the LIVE exchange,
+        # empty whenever LIVE_TRADING_ENABLED is False — that alone is why the close
+        # advisor was never consulted in 65 days of paper. The exchange is still
+        # asked FIRST; the fallback engages only in paper mode. Live path untouched.
         p = _fetch_open_position(symbol, s)
+        if p is None and EXIT_ADVISOR_PAPER_ENABLED and not LIVE_TRADING_ENABLED:
+            p = _paper_position_as_exchange_dict(symbol, s)
         if p:
             if open_pos is not None:
                 # Both sides open and signal didn't disambiguate — log + bail.
@@ -2224,11 +2416,23 @@
         except (TypeError, ValueError):
             pass
 
-    advice = claude_advisor.consult_for_close(
-        symbol, open_side, entry_price, upnl, age_minutes,
-        snapshot, signal_name,
-    )
+    _vpos = (open_pos or {}).get('_vpos')
+    if _vpos is not None:
+        advice = consult_exit_advisor(_vpos, symbol, open_side, signal_name, '5m_group_b')
+    else:
+        advice = claude_advisor.consult_for_close(
+            symbol, open_side, entry_price, upnl, age_minutes,
+            snapshot, signal_name,
+        )
     decide = advice.get('decide')
+
+    # DRYRUN (default ON). The verdict is already recorded by consult_exit_advisor.
+    # This early return sits BEFORE every close mechanic below — no branch past this
+    # point can execute while the flag is set. SL / trail / armed-exit remain the
+    # sole authority on exits.
+    if EXIT_ADVISOR_DRYRUN:
+        return jsonify({"status": "exit_ai_dryrun", "close": advice.get('close'),
+                        "reason": (advice.get('reason') or '')[:400]}), 200
     ai_close = advice.get('close')
     ai_conf = float(advice.get('confidence') or 0.0)
     ai_reason = (advice.get('reason') or '')[:200]
@@ -2864,6 +3068,19 @@
                         armed.get('source_signal'),
                     )
                 # Nothing armed → exit-only signal, dropped entirely.
+                # EXIT_ADVISOR_ON_15M_CONFIRM (2026-07-26): the 15m exit stream is the
+                # operator's dedicated exit alert set and fires ~2.2x/day with a
+                # position open. Consulted here in DRYRUN only — the noop below is
+                # unchanged and remains the sole outcome.
+                if EXIT_ADVISOR_ON_15M_CONFIRM and EXIT_ADVISOR_DRYRUN:
+                    for _s in ('LONG', 'SHORT'):
+                        _vp = virtual_trader._open_position(symbol, _s)
+                        if _vp:
+                            try:
+                                consult_exit_advisor(_vp, symbol, _s, signal_name,
+                                                     '15m_exit_confirm')
+                            except Exception as _e:
+                                print(f"[EXIT-ADVISOR] 15m consult failed: {_e}", flush=True)
                 insert_signal(parsed, symbol, 'na', '15m_exit_confirm',
                               status='exit_unarmed_noop')
                 print(f"EXIT_CONFIRM_15M_UNARMED cid={_m_cid} dir={_m_dir} "
@@ -2877,6 +3094,18 @@
                                 "direction": _m_dir, "signal": signal_name}), 200
         state_machine.update_slot('15m_confirm', direction or 'NEUTRAL',
                                   signal_name)
+        # PART 4 (2026-07-26) — THE MISSING WRITE. This branch updated the slot,
+        # sent the card and returned 200 without persisting anything: ~26 alerts/day,
+        # 374 per 15 days, and NOT ONE 15m_confirm row in the whole database. The
+        # signals were never ignored — signal_matrix.record_signal above already
+        # gave them their MOMENTUM weight — they were simply unauditable, which is
+        # why every DB-only inventory reported the operator's 15m entry set as
+        # "never arrives". Mercury-SOL persists these (997 rows, main.py:3463);
+        # Titan did not. Mirrored field-for-field, status name included, so the two
+        # books stay comparable. Purely additive: no routing, slot, matrix or
+        # decision change.
+        insert_signal(parsed, symbol, 'na', '15m_confirm',
+                      status='confirm_recorded')
         hw_subtype, hw_weight = engine_15m.evaluate(signal_name)
         send_tg(
             f"🌊 <b>15m slot updated</b>: {direction or '?'}\n"
--- a/virtual_trader.py
+++ b/virtual_trader.py
@@ -90,6 +90,7 @@
     PRICE_AGAINST_CRITICAL_PCT, PRICE_AGAINST_WARNING_PCT,
     HEALTH_SCORE_EMERGENCY, HEALTH_SCORE_TIGHTEN,
     LONG_PARTIAL_ENABLED, LONG_PARTIAL_LEVEL_R, LONG_PARTIAL_FRACTION,
+    EXIT_ADVISOR_HOURLY, EXIT_ADVISOR_DRYRUN, EXIT_ADVISOR_HOURLY_SEC,
 )
 
 # Serializes the final count-and-insert in execute_entry so two same-bar
@@ -1608,6 +1609,29 @@
         except Exception as e:
             print(f"[VIRTUAL] smart-exit dryrun failed vid={row['id']}: {e}", flush=True)
 
+    # 1e) EXIT-ADVISOR hourly consultation (2026-07-26), DRYRUN only. Reuses the
+    #     smart-exit sampler cadence — that sampler already collects the 48 fields
+    #     the enriched prompt needs. Signal triggers alone give ~2.2 consultations
+    #     a day; hourly gives a full trajectory per position. Records a verdict and
+    #     NOTHING ELSE: this block has no close mechanic and cannot move a stop.
+    #     main is imported lazily to avoid the circular import at module load.
+    if EXIT_ADVISOR_HOURLY and EXIT_ADVISOR_DRYRUN:
+        try:
+            _st = mgmt_state.get('exit_advisor_last_ts')
+            _now_ts = datetime.now(timezone.utc).timestamp()
+            if _st is None or (_now_ts - float(_st)) >= EXIT_ADVISOR_HOURLY_SEC:
+                import main as _m
+                _m.consult_exit_advisor(row, row['symbol'], position_side,
+                                        'hourly review', 'hourly')
+                mgmt_state['exit_advisor_last_ts'] = _now_ts
+                with sqlite3.connect(DB_PATH) as _c:
+                    _c.execute("UPDATE virtual_positions SET pending_dca_limits=? "
+                               "WHERE id=? AND status='open'",
+                               (json.dumps(mgmt_state), row['id']))
+                changed = True
+        except Exception as _e:
+            print(f"[EXIT-ADVISOR] hourly consult failed vpos={row['id']}: {_e}", flush=True)
+
     # 1c) Post-entry multi-tier recheck (T+10/60/300s). PRE-BREAKEVEN ONLY — once
     #     +1R/trail arms (section 2), the trail owns the position. Each tier fires
     #     once; tighten/critical-close are terminal. A new tier fires when its mark
```

### Part 4 — the missing write
One `insert_signal(parsed, symbol, 'na', '15m_confirm', status='confirm_recorded')`, mirroring
Mercury-SOL `main.py:3463` field-for-field including the status name. Titan's own plain-text 15m
path already uses that exact call — the JSON path simply never got it. Purely additive.

### Part 5 — exit advisor
* **Plumbing** — `_paper_position_as_exchange_dict`; the exchange is asked FIRST, the fallback only
  engages in paper. Live path untouched.
* **Enriched prompt** — R-denominated PnL and stop distance, MFE/giveback, book dynamics
  entry-vs-now, **percentile scale** with an explicit note that every book state contains a >4x wall
  so the multiple alone means nothing, regime entry-vs-now, volume, **recent 5m structure as context
  only**, and the **three entry signals** plus the entry advisor's own reason.
* **Hourly** (`EXIT_ADVISOR_HOURLY`) — in `virtual_trader`, reusing the sampler cadence; `main` is
  imported lazily to avoid the circular import. Records a verdict and nothing else.
* **15m trigger** (`EXIT_ADVISOR_ON_15M_CONFIRM = True`) — consulted where the `exit_unarmed_noop`
  is written; that noop is unchanged and remains the only outcome.
* **400-char reasoning**, payload+reason persisted via `_ai_fields_from_advice` exactly as on entry.

### DRYRUN proof
```
DRYRUN early return .................. main.py line 2433
_execute_close_position calls ........ main.py line 2471
every close mechanic AFTER the return .. True   (AST-verified on the patched copy)
```
`consult_exit_advisor` has no close mechanic in scope at all. The hourly hook lives in
`_process_position` before section 1c and returns nothing that any exit reads.

### Validation
`py_compile` OK on config / claude_advisor / virtual_trader · `main.py` AST-validated ·
`patch -p1 --dry-run` CLEAN on all four files · working tree still clean at `f7df202`.

### Snapshot / apply / rollback (for when approved)
```bash
git tag pre-signal-inventory-20260726
cd /root/titan-bot && for f in config.py claude_advisor.py main.py virtual_trader.py; do
  cp $f $f.bak_s6_20260726; done
patch -p1 < S6.patch && python3 -m py_compile config.py claude_advisor.py virtual_trader.py
sudo systemctl restart titan.service
# rollback: git checkout pre-signal-inventory-20260726 -- titan-bot/*.py
#      or:  EXIT_ADVISOR_DRYRUN stays True and EXIT_ADVISOR_HOURLY/_ON_15M_CONFIRM = False
```

### Scope — untouched
Entry gate · FLAT floor · HTF cascade · confluence matrix · **LONG partial `f7df202`** ·
**recheck bound `93c20c3`** · SL / trail / breakeven · the router and `_TF_TO_ACTION` ·
every sensor · **Mercury-SOL**. No 5m exit alert is created and the 5m router is not touched —
5m structure enters the exit advisor as a prompt field only.

---

## PART 6 — activation criterion, recorded (commit `900901e`)

Written into `reports/OPEN-ITEMS.md` **before any verdict exists**, so it cannot be adjusted to fit
the result: the exit advisor goes live only if, over the first ~10 closed positions, its FIRST
"close" verdict beats the actual exit **both** in total USDT **and** in positions improved.
No partial credit, no re-cutting the sample.

---

**Nothing applied. Stopped for approval.** Tree clean at `f7df202`; `titan.service` healthy;
Mercury-SOL untouched.
