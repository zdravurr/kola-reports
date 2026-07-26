# long-partial-applied-confirmed

_2026-07-26 18:56 UTC_

---

# TITAN — LONG partial realisation APPLIED, live, confirmed

**2026-07-26 18:51 UTC · APPLIED.** Commit `f7df202`, tree clean, `titan.service` healthy.
Structure = partial realisation · LONG-only · 1/3 @ 1.0R · `LONG_PARTIAL_ENABLED = True`.
Paper mode (`LIVE_TRADING_ENABLED = False`).

Running open-items list seeded: **reports/OPEN-ITEMS.md** (same repo).

---

## 1. What shipped

```
config.py         + LONG_PARTIAL_ENABLED / _LEVEL_R / _FRACTION  (3 constants, 24 lines of evidence comment)
virtual_trader.py + _take_long_partial()  + hook 1d  + 2 columns  + net_pnl fold
                    1 file changed: 81 insertions(+), 1 deletion(-)
```
Snapshot taken first: tag `pre-long-partial-20260726` (at `b878535`) +
`config.py.bak_longpartial_20260726` (md5 `1a4746e0…`) +
`virtual_trader.py.bak_longpartial_20260726` (md5 `cfb7f130…`).

---

## 2. The applied diff

```diff
--- a/config.py
+++ b/config.py
@@ -73,6 +73,33 @@
 TRAIL_ATR_TF = '1h'
 TRAIL_MULT_ATR = 2.5  # ~1.19% trail, matches SL width (2.5×ATR_1h)
 
+# --- LONG-side partial realisation (2026-07-26) -----------------------------
+# WHY. trail_pct is set equal to the stop distance on 47/49 positions, so the
+# trail hands back exactly 1R on BOTH sides. That is survivable for shorts
+# (median winner peak 1.84R -> 49% surrendered) and ruinous for longs (median
+# winner peak 1.16R -> 64% surrendered; every long above 0.5R gives back 72% of
+# its peak). Clean-sample medians are 0.93R LONG vs 0.97R SHORT — longs do NOT
+# move less, they simply have no right tail (0/10 reach 2R vs 29% of shorts)
+# and stall after ~2h having reached 91% of their peak.
+#
+# STRUCTURE, NOT PARAMETER. n=10 clean longs (6 above 0.5R, 5 winners) supports
+# choosing the SHAPE of the contract, not its numbers. A partial was chosen over
+# a fixed target because its worst case is bounded: if a long runner finally
+# appears, a partial surrenders only FRACTION of the excess, while a 1.0R target
+# would cap the whole trade. Simulated on the clean sample (baseline -343.10):
+#   partial 1/3 @1.0R  -248.28 (+94.83)   0 winners cut, 0 losers improved
+#   partial 1/2 @1.0R  -200.87 (+142.24)  0 winners cut
+#   partial 1/2 @0.75R -158.69 (+184.42)  1 winner cut, 1 loser improved
+#   target 1.0R         -58.63 (+284.48)  best observed, WORST tail risk
+# The same rules applied to SHORTS make them worse by -177..-530, which is why
+# this is LONG-ONLY: the short side's contract is already correct for its shape.
+# 1/3 @ 1.0R is the conservative corner: it never cut a winner in simulation and
+# it reuses the +1R point the breakeven/trail already arms at, so no new concept
+# enters the exit path. RETUNE only when ~30 clean longs have closed.
+LONG_PARTIAL_ENABLED = True     # kill switch — False restores the current rule exactly
+LONG_PARTIAL_LEVEL_R = 1.0      # take the partial when MFE reaches this many R
+LONG_PARTIAL_FRACTION = 1.0/3   # fraction of the position realised at that level
+
 # Adaptive L.-1 trail (adaptive_trail.compute_fresh_trail_pct): recompute the
 # trail_pct from a FRESH TRAIL_ATR_TF ATR at +1R arming instead of the
 # entry-frozen value, then place the SAME single server-side TRAILING_STOP_MARKET.
--- a/virtual_trader.py
+++ b/virtual_trader.py
@@ -89,6 +89,7 @@
     ADX_DROP_THRESHOLD, ADX_BELOW_FLOOR, ATR_DROP_PCT,
     PRICE_AGAINST_CRITICAL_PCT, PRICE_AGAINST_WARNING_PCT,
     HEALTH_SCORE_EMERGENCY, HEALTH_SCORE_TIGHTEN,
+    LONG_PARTIAL_ENABLED, LONG_PARTIAL_LEVEL_R, LONG_PARTIAL_FRACTION,
 )
 
 # Serializes the final count-and-insert in execute_entry so two same-bar
@@ -170,7 +171,12 @@
                         "entry_ob_imbalance REAL",
                         "entry_n_walls_bid INTEGER",
                         "entry_n_walls_ask INTEGER",
-                        "recheck_status TEXT"):
+                        "recheck_status TEXT",
+                        # LONG-side partial realisation (2026-07-26). Both NULL on
+                        # legacy rows -> treated as "no partial taken", so every
+                        # existing position keeps the old contract exactly.
+                        "partial_taken INTEGER",
+                        "realized_partial_usdt REAL"):
             try:
                 conn.execute(f"ALTER TABLE virtual_positions ADD COLUMN {_coldef}")
             except sqlite3.OperationalError:
@@ -741,6 +747,13 @@
     )
     net_pnl = report.net_pnl
 
+    # LONG partial: PnL already banked on the first tranche is added to the
+    # remainder's result so net_pnl stays the whole-position figure. Zero when no
+    # partial was taken, so the arithmetic is unchanged for every other position.
+    _rp = (row['realized_partial_usdt'] if 'realized_partial_usdt' in _rk else None) or 0.0
+    if _rp:
+        net_pnl += _rp
+
     entry_row_id = row['trades_entry_row_id'] if 'trades_entry_row_id' in row.keys() else None
     with sqlite3.connect(DB_PATH) as conn:
         conn.execute(
@@ -1011,6 +1024,56 @@
     return new_sl
 
 
+def _take_long_partial(row, last, send_tg):
+    """Realise LONG_PARTIAL_FRACTION of a LONG at LONG_PARTIAL_LEVEL_R.
+
+    Banks the tranche's PnL into realized_partial_usdt and shrinks every DCA leg
+    by the same fraction, so the position continues under the UNCHANGED contract
+    (same original SL, same breakeven arming, same trail width) on the remainder.
+    LONG only — the short side keeps the current rule untouched. Best-effort: any
+    failure leaves the position exactly as it was."""
+    try:
+        legs = json.loads(row['filled_legs'])
+        avg_entry, total_size = _avg_entry_and_size(legs)
+        if not avg_entry or total_size <= 0:
+            return False
+        frac = float(LONG_PARTIAL_FRACTION)
+        if not (0.0 < frac < 1.0):
+            return False
+        cut_size = total_size * frac
+        gross = (last - avg_entry) * cut_size
+        fee = last * cut_size * VIRTUAL_FEE_RATE
+        # Entry fee already paid on this tranche, charged pro-rata so the
+        # remainder is not billed twice for it at final close.
+        entry_fee_share = sum(leg.get('fee', 0.0) for leg in legs) * frac
+        realised = gross - fee - entry_fee_share
+        for leg in legs:
+            leg['size'] = leg['size'] * (1.0 - frac)
+            leg['fee'] = leg.get('fee', 0.0) * (1.0 - frac)
+        with sqlite3.connect(DB_PATH) as conn:
+            conn.execute(
+                "UPDATE virtual_positions SET filled_legs=?, partial_taken=1, "
+                "realized_partial_usdt=COALESCE(realized_partial_usdt,0)+? "
+                "WHERE id=? AND status='open'",
+                (json.dumps(legs), realised, row['id']),
+            )
+        print(f"[VIRTUAL] LONG PARTIAL vpos={row['id']} {frac*100:.0f}% @ {last:.2f} "
+              f"(+{LONG_PARTIAL_LEVEL_R:.2f}R) realised={realised:+.2f} "
+              f"remainder rides unchanged", flush=True)
+        if send_tg:
+            try:
+                send_tg(f"🟩 <b>LONG partial taken</b> {row['symbol']}\n"
+                        f"{frac*100:.0f}% @ {last:.2f} (+{LONG_PARTIAL_LEVEL_R:.2f}R) "
+                        f"= {realised:+.2f} USDT banked\n"
+                        f"Remainder continues on the unchanged SL/trail.")
+            except Exception as e:
+                print(f"long partial telegram failed: {e}", flush=True)
+        return True
+    except Exception as e:
+        print(f"[VIRTUAL] long partial failed vpos={row['id']}: {e}", flush=True)
+        return False
+
+
 def _one_r_distance(fill, original_sl):
     """1R = |entry - ORIGINAL stop|. Always reads the original SL so a post-entry
     SL tighten cannot shrink 1R and arm breakeven prematurely."""
@@ -1570,6 +1633,22 @@
                 _set_recheck_status(row['id'], 'done')
                 changed = True
 
+    # 1d) LONG partial realisation. Fires ONCE, before breakeven/trail, and only
+    #     for LONGs. The remainder keeps the original SL, the same +1R breakeven
+    #     arming and the same trail width — nothing else in the contract moves.
+    #     SHORTS are deliberately untouched: their 1.84R median winner peak makes
+    #     the current 1R giveback survivable, and every simulated variant made
+    #     them worse (-177 to -530 on the clean sample).
+    if (LONG_PARTIAL_ENABLED and position_side == 'LONG'
+            and not (row['partial_taken'] if 'partial_taken' in row.keys() else 0)):
+        _orig_sl_p = (row['original_sl_price'] if 'original_sl_price' in row.keys()
+                      and row['original_sl_price'] is not None else row['sl_price'])
+        _fill_p = float(row['initial_fill_price'])
+        _lvl = _fill_p + _one_r_distance(_fill_p, _orig_sl_p) * float(LONG_PARTIAL_LEVEL_R)
+        if last >= _lvl and _take_long_partial(row, last, send_tg):
+            row = _open_position(row['symbol'], position_side) or row
+            changed = True
+
     # 2) Breakeven transition — once price reaches +1R, move the SL to
     #    breakeven and arm the trail (same formula as live breakeven_worker).
     if not be_applied:
```

---

## 3. The seven confirmations

### (1) Only `config.py` and `virtual_trader.py` changed · `claude_advisor.py` untouched
```
git status --porcelain  ->  M titan-bot/config.py
                            M titan-bot/virtual_trader.py
git diff --stat HEAD    ->  2 files changed, 107 insertions(+), 1 deletion(-)
claude_advisor.py md5   ->  0ea462ce0f54f238f9346bc77daeb820   IDENTICAL to before
```
`config.py` code lines changed — the entire rest of the diff is comment:
```
+LONG_PARTIAL_ENABLED = True
+LONG_PARTIAL_LEVEL_R = 1.0
+LONG_PARTIAL_FRACTION = 1.0/3
```

### (2) SHORT path byte-identical — the hook is gated on `position_side == 'LONG'`
Condition extracted **by AST from the deployed file**:
```
LONG_PARTIAL_ENABLED
 and position_side == 'LONG'
 and (not (row['partial_taken'] if 'partial_taken' in row.keys() else 0))
```
```
occurrences of _take_long_partial : 2   (1 definition + 1 call, both inside the LONG branch)
lines mentioning both 'partial' and 'SHORT' outside comments : 0
```
A SHORT never enters the branch, so its exit path executes exactly the instructions it did before.

### (3) R1 recheck fix (`93c20c3`) intact
```
 986: def _tighten_sl(position_side, entry_price, current_sl, original_sl=None):
1186:     original_sl=_orig_sl)))
"never tighter than ORIGINAL" clamps present : 2   (LONG branch + SHORT branch)
```
Signature and call site unchanged; both clamps in place.

### (4) SL placement, `original_sl_price`, `_one_r_distance`, breakeven and trail all unchanged
The diff contains **no modification** to any line touching `sl_price`, `_breakeven_reached`,
`be_price`, `trail_pct`, `water_mark` or `_tighten_sl`. The only new references to stop data are
three **read-only** lines inside the new hook:
```python
_orig_sl_p = (row['original_sl_price'] if 'original_sl_price' in row.keys()
              and row['original_sl_price'] is not None else row['sl_price'])
_lvl = _fill_p + _one_r_distance(_fill_p, _orig_sl_p) * float(LONG_PARTIAL_LEVEL_R)
if last >= _lvl and _take_long_partial(row, last, send_tg):
```
1R is still measured off the **ORIGINAL** stop. The remainder keeps that same original SL, arms
breakeven at the same +1R, and trails at the same width — the contract on the remainder is
byte-identical to the one before this change.

### (5) New columns present and NULL on every legacy row · vpos 82 unaffected
```
38 | partial_taken          | INTEGER
39 | realized_partial_usdt  | REAL

rows=56   partial_taken NULL=56   realized_partial_usdt NULL=56      (100% NULL)

open position:
  vpos 82 LONG  entry 64779.8  original SL 64444.1  trail 0.518%
                partial_taken = NULL   realized_partial_usdt = NULL
                +1R level = 65115.5  -> the partial fires only if price reaches it
```
Every one of the 56 existing rows keeps the old contract exactly. The open long is untouched and
will only take a partial if it earns +1R from here.

### (6) Service healthy, no errors on boot
```
systemctl is-active -> active, MainPID 3181827, NRestarts 0
18:51:10 Started · 18:51:14 Listening 127.0.0.1:5000 · 18:51:19 [RECONCILE] done
18:51:20 breakeven_worker started (5s) · virtual_trader worker started (10s, closed=26/30)
18:51:21 [OB-DENSITY] ctVal=0.01 from OKX spec · heartbeat +1 rows / 0 failures
journal grep traceback|exception|error -> none
```

### (7) Entry gate, FLAT floor, cascade, sensors and Mercury-SOL untouched
```
CONFLUENCE_SCORE_THRESHOLD = 2.0     CONFLUENCE_FLAT_THRESHOLD = 5.0
HTF_CASCADE_ENABLED = True           WALL_TRAIL_LIVE_ENABLED = False
POST_ENTRY_RECHECK_ENABLED = True    ADX_BELOW_FLOOR = 20.0 (-5)
HEALTH_SCORE_EMERGENCY/-TIGHTEN = -10 / -5
SMART_EXIT_DRYRUN_ENABLED = True     ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True

Titan cron sensor lines: 7 (unchanged)
mercury-sol/virtual_trader.py mtime 2026-07-02 21:37 — untouched · mercury-sol.service active
```

---

## 4. Verification to run on the next LONG that reaches +1R

```sql
-- must show partial_taken=1 and a non-zero realised amount
SELECT id, position_side, partial_taken, realized_partial_usdt, water_mark, initial_fill_price
FROM virtual_positions WHERE partial_taken = 1;
```
```bash
journalctl -u titan.service | grep "LONG PARTIAL"     # expect one line per long, none for shorts
```
A SHORT reaching +1R must log **nothing** new.

---

## 5. Rollback
```bash
# no code edit at all — the kill switch
LONG_PARTIAL_ENABLED = False   in config.py   + sudo systemctl restart titan.service

# or full revert
git checkout pre-long-partial-20260726 -- titan-bot/config.py titan-bot/virtual_trader.py
# or: cp *.bak_longpartial_20260726 back over the originals
# or: git revert f7df202
sudo systemctl restart titan.service
```
The two added columns are harmless if the code is reverted — they simply stop being written.

---

## 6. OPEN-ITEMS.md seeded

`reports/OPEN-ITEMS.md` now carries the running list, headed by the blocking one:

1. **🔴 LIVE-PATH PARITY GAP** — `breakeven_worker.py` has no partial equivalent. Harmless while
   `LIVE_TRADING_ENABLED = False`, but longs would diverge live-vs-paper. **Must be closed before
   live is enabled.** Noted alongside it: the R1 recheck bound and the FLAT floor need the same
   parity check at that time.
2. LONG partial parameters are placeholders — retune at ~30 clean long closes (currently 6 above 0.5R).
3. Variant C (narrower trail) is **unevaluated, not rejected** — n=1 real path per side.
4. Entry-advisor order-book calibration — one confirmed miscalibration (trade 18631: an ask wall
   above entry, which is a tailwind for a SHORT, was cited as a reason to skip one). Systematic
   scale not measured; `ai_user_prompt` + `ai_reason` are persisted for 2,685 decisions, so closing
   it needs no new instrumentation.
5. Exit advisor — `consult_for_close()` exists; whether it is wired in, how often it fires and
   whether its verdicts are good is **not established**.

Plus the watch-list table (items waiting only for n) and a list of what closed this session.

---

Session commits: `93c20c3` (recheck bound) · `596fbdf` (superseded) · `b878535` (caution retired) ·
`f7df202` (LONG partial). Tree clean, service healthy, Mercury-SOL untouched throughout.
