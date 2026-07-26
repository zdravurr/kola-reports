# r1-variantB-applied-confirmed

_2026-07-26 17:08 UTC_

---

# TITAN R1 — Variant B APPLIED, LIVE, CONFIRMED

**2026-07-26 17:05 UTC · APPLIED and running.** Commit `93c20c3`, tree clean.
Variant A **declined and not applied** — `config.py` is byte-identical to before.
Paper mode (`LIVE_TRADING_ENABLED = False`).

---

## 1. What shipped

The `_tighten_sl` original-SL floor — hunks 4 and 5 only, **one file, `virtual_trader.py`**.
`config.py` was not opened. The `adx_below_floor` weight stays at `-5`; the TIGHTEN verdict is
still produced and still logged, so the labels remain available for future analysis.

**What it prevents:** of 10 positions ever marked `recheck_status='tightened'`, 8 are losers whose
`max_adverse_price` never reached their ORIGINAL stop — the recheck's own move closed them.
-528.73 realised; -386.09 once the already-reverted wall-trail window is excluded. Only 3 of the 8
have an attributable rule (vpos 71, 72 = wall growth, fixed 07-13; vpos 74 = `adx_below_floor`);
for the other 5 the reason rotated out of the journal before `recheck_events` existed. Bounding the
**action** rather than one rule's weight is what makes the class unreachable regardless of cause.

Replay of vpos 74 on the deployed code:
```
entry=62717.9  sl_before=63489.3  origSL=63489.3  maxAdverse=63119.8
SNAPSHOT -> 63103.6000 (dist 0.615%)   <- what actually happened; killed it for -73.09
LIVE     -> 63489.3000 (dist 1.230%)   <- original stop, UNMOVED
under LIVE the stop is NOT hit: True
```

---

## 2. Snapshot taken before applying

```
git tag pre-recheck-adx-fix-20260726          -> 6c35b9d
config.py.bak_recheckadx_20260726             md5 1a4746e072c74248a0efeefe4b206fdc
virtual_trader.py.bak_recheckadx_20260726     md5 f0db4259cde6958a47d942e8508154f7
```

---

## 3. The applied diff

```diff
--- a/virtual_trader.py
+++ b/virtual_trader.py
@@ -970,18 +970,43 @@
     return 'OK'
 
 
-def _tighten_sl(position_side, entry_price, current_sl):
+def _tighten_sl(position_side, entry_price, current_sl, original_sl=None):
     """Defensive SL move toward entry: midpoint(entry, current_sl), clamped so it
-    (a) only ever tightens, never loosens, and (b) NEVER crosses entry (instant
-    self-stop). The never-cross-entry clamp is applied LAST so it wins even on a
-    pathological current_sl already past entry."""
+    (a) only ever tightens, never loosens, (b) NEVER crosses entry (instant
+    self-stop), and (c) 2026-07-26 — NEVER ends up tighter than the ORIGINAL stop
+    distance. The never-cross-entry clamp is applied LAST so it wins even on a
+    pathological current_sl already past entry.
+
+    Clamp (c) is the fix. Clamps (a)+(b) bounded the DIRECTION of the move but never
+    HOW FAR the midpoint could travel, so a single tier firing halved the stop.
+    Forensics: of 10 positions ever marked recheck_status='tightened', EIGHT are
+    losers whose max_adverse_price never reached their ORIGINAL stop — the recheck's
+    own move is what stopped them out (-528.73 realised; -386.09 once the wall-trail
+    window is excluded). Only three of those eight have an attributable rule (vpos 71,
+    72 = wall growth, neutralised 2026-07-13; vpos 74 = adx_below_floor); for the other
+    five the reason rotated out of the journal before recheck_events existed. That is
+    the whole argument for fixing the ACTION rather than any one rule's weight: it
+    makes the failure class unreachable no matter which rule fires, including rules
+    not yet written. The scoring is deliberately left untouched — adx_below_floor is
+    still -5 and a TIGHTEN verdict is still produced and still logged, so the labels
+    stay available for future analysis.
+
+    Because the recheck only runs PRE-BREAKEVEN (see the poller: `not be_applied`),
+    current_sl IS the original stop on every reachable path, so in practice this makes
+    a TIGHTEN verdict a LOGGED ADVISORY that moves no stop. EMERGENCY_CLOSE is a
+    separate branch and is NOT affected. Pass original_sl=None for the old unbounded
+    behaviour (used by nothing; kept so the helper stays testable)."""
     eps = entry_price * 0.0001
     new_sl = (entry_price + current_sl) / 2.0
     if position_side == 'LONG':
         new_sl = max(new_sl, current_sl)         # tighten up only
+        if original_sl is not None:
+            new_sl = min(new_sl, float(original_sl))   # never tighter than ORIGINAL
         new_sl = min(new_sl, entry_price - eps)  # never at/above entry (wins)
     else:
         new_sl = min(new_sl, current_sl)         # tighten down only
+        if original_sl is not None:
+            new_sl = max(new_sl, float(original_sl))   # never tighter than ORIGINAL
         new_sl = max(new_sl, entry_price + eps)  # never at/below entry (wins)
     return new_sl
 
@@ -1094,7 +1119,8 @@
         _orig_sl = (row['original_sl_price'] if 'original_sl_price' in _rk
                     and row['original_sl_price'] is not None else current_sl)
         new_sl = float(exchange.price_to_precision(
-            symbol, _tighten_sl(position_side, entry_price, current_sl)))
+            symbol, _tighten_sl(position_side, entry_price, current_sl,
+                                original_sl=_orig_sl)))
         with sqlite3.connect(DB_PATH) as conn:
             conn.execute(
                 "UPDATE virtual_positions SET sl_price=?, recheck_status='tightened' "
```

---

## 4. The five confirmations you asked for

### (1) `config.py` unchanged — `ADX_BELOW_FLOOR` still `-5`
```
md5 config.py = 1a4746e072c74248a0efeefe4b206fdc   (identical to the pre-apply baseline)
git diff HEAD -- titan-bot/config.py              -> 0 files
config.py:505  ADX_BELOW_FLOOR = 20.0    # 1h ADX now below 20   -> -5
grep -c ADX_BELOW_FLOOR_SCORE config.py virtual_trader.py -> 0 and 0   (Variant A absent)

_health_score ADX branch, live file, unchanged:
    if cur_adx < ADX_BELOW_FLOOR:
        score -= 5
        parts.append(f"ADX {cur_adx:.1f}<{ADX_BELOW_FLOOR:.0f} (-5)")
        details.append({'rule': 'adx_below_floor', 'value': round(cur_adx, 3),
                        'threshold': ADX_BELOW_FLOOR, 'points': -5})
```

### (2) `_tighten_sl` receives `original_sl` at the call site
```
 973:def _tighten_sl(position_side, entry_price, current_sl, original_sl=None):
1122:            symbol, _tighten_sl(position_side, entry_price, current_sl,

live call site:
        _orig_sl = (row['original_sl_price'] if 'original_sl_price' in _rk
                    and row['original_sl_price'] is not None else current_sl)
        new_sl = float(exchange.price_to_precision(
            symbol, _tighten_sl(position_side, entry_price, current_sl,
                                original_sl=_orig_sl)))
```
Exactly ONE call site. Clamp verified on the deployed file, both sides, incl. pathological inputs:
```
SHORT entry=62717.9 cur=63489.3 orig=63489.3 -> 63489.3000  never tighter than orig: True
LONG  entry=63788.4 cur=62789.8 orig=62789.8 -> 62789.8000  never tighter than orig: True
SHORT entry=62717.9 cur=63200.0 orig=63489.3 -> 63489.3000  never tighter than orig: True
LONG  entry=63788.4 cur=63000.0 orig=62789.8 -> 62789.8000  never tighter than orig: True
back-compat: original_sl=None reproduces the snapshot exactly -> True
```

### (3) Service healthy
```
systemctl is-active titan.service   -> active (running), MainPID 3158505, NRestarts 0
17:05:46  Started titan.service
17:05:52  gunicorn 26.0.0, listening 127.0.0.1:5000
17:05:58  [RECONCILE] boot reconciliation starting / STOP-CLEANUP no orphaned orders LONG+SHORT / done
17:05:59  breakeven_worker started (interval=5s)
17:05:59  virtual_trader worker started (interval=10s, closed=26/30, entries=61)
17:06:00  [OB-DENSITY] collector started, ctVal=0.01 read from OKX spec, heartbeat +1 rows / 0 failures
journal grep traceback|exception|error -> none
```
Open position survived the restart untouched:
`vpos 82 LONG open sl_price=64444.1 original_sl_price=64444.1 recheck_status='done'`
(already past the recheck window, so it was never exposed either way).

### (4) EMERGENCY_CLOSE reach unchanged
`_health_score` + `_recheck_verdict` were extracted by AST from the **deployed** file and from the
snapshot, then fuzzed side by side over **4000 randomised states** (both sides, every input
nullable, wall/ADX/ATR/price ranges spanning all thresholds):
```
divergences in score or verdict: 0
```
Named cases:
```
adx_below_floor ALONE (vpos-74 shape)  SNAPSHOT  -5/TIGHTEN          LIVE  -5/TIGHTEN
adx_drop + atr_contraction             SNAPSHOT  -6/TIGHTEN          LIVE  -6/TIGHTEN
all three -3 rules (emergency)         SNAPSHOT -14/EMERGENCY_CLOSE  LIVE -14/EMERGENCY_CLOSE
```
All three verdicts — OK / TIGHTEN / EMERGENCY_CLOSE — are byte-identical. Only the SIZE of the
stop move changed. This is the side effect Variant A would have introduced and B does not.

### (5) Wall-trail still disabled
```
config.py:284  WALL_TRAIL_LIVE_ENABLED = False
virtual_trader.py:1385  if (WALL_TRAIL_LIVE_ENABLED and _tighter and _dir_ok
```
All three writers of `sl_price`; only the first is in the diff:
```
1126  recheck TIGHTEN            <-- CHANGED (bounded)
1387  wall-trail ratchet         <-- untouched, still gated off
1623  breakeven / adaptive trail <-- untouched
```

---

## 5. Rollback

```bash
# 1. from the tag
git checkout pre-recheck-adx-fix-20260726 -- titan-bot/virtual_trader.py

# 2. from the .bak copy
cd /root/titan-bot && cp virtual_trader.py.bak_recheckadx_20260726 virtual_trader.py

# 3. revert the commit
cd /root && git revert 93c20c3

sudo systemctl restart titan.service
```

---

## 6. Status of the rest of the R1 audit list

* **Variant A — declined by you, not applied.** If ever revisited, note it carries the
  EMERGENCY_CLOSE regression (-14 -> -9) and would need `HEALTH_SCORE_EMERGENCY = -10 -> -9`
  alongside it.
* This closes the last live self-clipper. The wall-trail (07-13) and the phantom-wall recheck
  trigger (07-13) were the earlier two.
* Nothing else from the audit was touched: entry gate, FLAT floor, HTF cascade, advisor, the
  counter-short filter and every watch-list sensor are exactly as they were.
