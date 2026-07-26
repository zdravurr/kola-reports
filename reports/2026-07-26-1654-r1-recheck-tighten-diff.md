# r1-recheck-tighten-diff

_2026-07-26 16:54 UTC_

---

# TITAN R1 — post-entry recheck TIGHTEN: fix + validation

**2026-07-26 · DIFF ONLY, NOT APPLIED.** Working tree clean, HEAD `6c35b9d`.
Paper mode (`LIVE_TRADING_ENABLED = False`). Patch is inline in §4 — one document, no separate file.

---

## 1. Decision required: A / B / A+B

| | **Variant A** — zero the ADX weight | **Variant B** — floor the SL at the original distance |
|---|---|---|
| Hunks | 1, 2, 3 | 4, 5 |
| Scope | ONLY the `adx_below_floor` rule | the TIGHTEN **action**, all rules |
| Matches "touches only adx_below_floor" | **YES** | **NO** — see §3 |
| Saves vpos 74 | yes (proven) | yes (proven) |
| Saves the 5 tightenings whose reason was lost | no | yes |
| Side effect | weakens EMERGENCY_CLOSE reach (§5 TEST 4) | none found |
| Precedent | identical to `c845941` (wall rule, 2026-07-13) | new |

**Recommendation: Variant B alone.**

---

## 2. What is broken, and what it has cost

`_tighten_sl()` moves the stop to `midpoint(entry, current_sl)`. It has two clamps — never loosen,
never cross entry — and **no bound on how far the midpoint travels**. One tier firing halves the
stop distance.

`adx_below_floor` is worth `-5`. `HEALTH_SCORE_TIGHTEN` is `-5`. Since the wall weights went to `0`
on 2026-07-13 it is **the only rule that reaches TIGHTEN on its own** — every other rule is `-3` or
`-1` and needs a partner. Same silhouette as the wall rule killed on 07-13.

A low *absolute* ADX is a regime statement, fully knowable at entry time — it belongs in the entry
gate, not in a post-fill stop move. The ADX **drop** rule (delta vs the entry baseline) is the real
post-entry signal and stays untouched at `-3`.

### Which past trades this would have saved

Every position ever marked `recheck_status='tightened'`, with `max_adverse_price` vs
`original_sl_price`:

| vpos | side | pnl | exit | orig SL (dist) | final SL | max adverse | would survive orig SL? |
|---|---|---|---|---|---|---|---|
| 46 | SHORT | +241.37 | trail | 74048.1 (1.07%) | 73117.37 | 73298.0 | yes (winner, trail exit) |
| 47 | SHORT | **-127.44** | sl | 67938.8 (2.32%) | 67170.0 | 67181.2 | **YES** |
| 53 | SHORT | **-106.86** | sl | 62135.4 (1.86%) | 61567.2 | 61589.7 | **YES** |
| 55 | LONG | **-78.70** | sl | 64897.2 (1.35%) | 65340.4 | 65331.3 | **YES** |
| 57 | SHORT | +170.01 | trail | 64826.4 (1.39%) | 63806.83 | 63952.9 | yes (winner, trail exit) |
| 67 | LONG | **-32.73** | sl | 62828.0 (1.18%) | 63448.8 | 63436.0 | **YES** |
| 68 | SHORT | **-4.52** | sl | 63040.3 (1.26%) | 62129.49 | 62307.7 | **YES** |
| 71 | LONG | **-30.78** | sl | 62789.8 (1.57%) | 63660.1 | 63653.8 | **YES** |
| 72 | LONG | **-74.61** | sl | 63842.3 (0.75%) | 64084.1 | 63909.9 | **YES** |
| 74 | SHORT | **-73.09** | sl | 63489.3 (1.23%) | 63103.6 | 63119.8 | **YES** |

**10 positions tightened; 8 are losers whose price never reached the original stop. -528.73.**
(The audit called this "n=1, vpos 74, -73". That understated it — correction stands here.)

Attribution at the confidence the evidence supports:

* **vpos 74 — proven `adx_below_floor`, -73.09.** The only persisted TIGHTEN:
  `reasons_json = [{"rule":"adx_below_floor","value":15.562,"threshold":20.0,"points":-5}]`.
  The only one **both** variants are proven to prevent.
* **vpos 71, 72 — proven wall rule, -105.39. ALREADY FIXED** by `c845941` (07-13). Cannot recur;
  neither variant gets credit.
* **vpos 47, 53, 55, 67, 68 — reason UNKNOWN, -350.25.** Pre-dates `recheck_events`; the journal
  rotated. **Variant B prevents these regardless of cause. Variant A only if they were ADX-driven,
  which cannot be established.**
* Overlap: 67, 68, 71, 72 sit inside the wall-trail window (07-02 23:28 – 07-13 01:55), so part of
  their damage is already counted in the -424 attributed to wall-trail.
  **Clean, non-overlapping recheck damage = vpos 47, 53, 55, 74 = -386.09.**

---

## 3. Scope confirmation — what it touches, and the one place I diverge from the brief

**You asked me to confirm the change touches ONLY the `adx_below_floor` recheck rule.**

* **Variant A (hunks 1-3): CONFIRMED.** It changes one score weight and nothing else.
* **Variant B (hunks 4-5): NOT TRUE, and I am recommending it anyway.** It bounds the TIGHTEN
  *action* for every rule, not just ADX. Stating it plainly rather than burying it: for 5 of the 8
  losers the firing rule is unknowable, so a fix scoped to the one rule we happen to have evidence
  for leaves the failure class alive. That is the whole argument for B over A.

**What NEITHER variant touches — verified by grep, not by assertion:**

`_tighten_sl` has exactly ONE call site — the TIGHTEN branch:
```
973:def _tighten_sl(position_side, entry_price, current_sl):
1097:            symbol, _tighten_sl(position_side, entry_price, current_sl)))
```

`ADX_BELOW_FLOOR` is referenced in exactly two files — its definition and the one rule:
```
config.py:505            ADX_BELOW_FLOOR = 20.0
virtual_trader.py:89     (import)
virtual_trader.py:934    if cur_adx < ADX_BELOW_FLOOR:
virtual_trader.py:936    parts.append(...)
virtual_trader.py:938    details.append(...)
```

All three writers of `sl_price` in `virtual_trader.py` — only the first is in the diff:
```
1100  recheck TIGHTEN            <-- THIS PATCH
1361  wall-trail ratchet         <-- NOT touched (WALL_TRAIL_LIVE_ENABLED = False since 07-13)
1597  breakeven / adaptive trail <-- NOT touched
```

* **wall-trail — NOT touched.** Separate branch at 1358-1361, still disabled. Not referenced.
* **main SL / trail / breakeven — NOT touched.** The 1597 UPDATE, `_breakeven_reached` and
  `_one_r_distance` are not in the diff. `_one_r_distance` already reads `original_sl_price`, so 1R
  is unaffected either way.
* **entry logic — NOT touched.** `grep -c` over `main.py` and `breakeven_worker.py` for
  `ADX_BELOW_FLOOR`, `ADX_BELOW_FLOOR_SCORE`, `_tighten_sl` returns **0 and 0**. No live path has
  its own recheck.
* **EMERGENCY_CLOSE — NOT touched by Variant B.** Variant A does reduce its reach; see §5 TEST 4.

**Load-bearing fact:** the recheck runs pre-breakeven only (poller guard `not be_applied`), so
`current_sl` **is** the original stop on every reachable path. Confirmed on the real row:
`recheck_events.sl_before (63489.3) == virtual_positions.original_sl_price (63489.3)` → `True`.
Consequence: under Variant B a TIGHTEN verdict becomes a **logged advisory that moves no stop** —
which is why "make it advisory" and "floor it at the original distance" collapse to the same
behaviour here.

---

## 4. The diff (inline — copy from here, no separate .patch file)

```diff
--- a/config.py
+++ b/config.py
@@ -502,7 +502,25 @@
 WALL_GROWTH_CRITICAL_SCORE = 0       # score delta when ratio > WALL_GROWTH_CRITICAL
 WALL_GROWTH_WARNING_SCORE = 0        # score delta when ratio > WALL_GROWTH_WARNING
 ADX_DROP_THRESHOLD = 5.0             # 1h ADX dropped > 5 points vs entry  -> -3
-ADX_BELOW_FLOOR = 20.0               # 1h ADX now below 20                 -> -5
+ADX_BELOW_FLOOR = 20.0               # 1h ADX now below 20                 -> ADX_BELOW_FLOOR_SCORE
+# ADX-below-floor SCORE contribution — NEUTRALISED 2026-07-26, exactly mirroring the
+# 2026-07-13 wall-growth neutralisation above (same defect, different sensor).
+# After the wall weights went to 0 this became the ONLY rule that reaches
+# HEALTH_SCORE_TIGHTEN ON ITS OWN (-5 <= -5) — every other rule is -3 or -1 and needs a
+# partner. So one 1h-ADX reading below 20 could still halve the stop via _tighten_sl's
+# midpoint, which has NO distance ceiling. Proven on vpos 74 (2026-07-13 05:05, the first
+# and only TIGHTEN since evidence became persistent): score -5 from this rule ALONE
+# ("no negative deltas" elsewhere), SL 63489.3 -> 63103.6 (0.615% tighter), price then
+# reached 63119.8 and stopped it out for -73.09 — INSIDE the original stop, which was
+# never touched. A low absolute ADX is a REGIME statement, not evidence that this entry
+# is failing: it is fully knowable at entry time and belongs in the entry gate, not in a
+# post-fill stop move. The ADX-DROP rule (delta vs the entry baseline) is the genuine
+# post-entry signal and is UNTOUCHED at -3.
+# The floor is STILL evaluated and STILL logged (parts/details/recheck_events) — only its
+# score weight is zero. adx_drop / atr_contraction / price_against are untouched and can
+# still sum to TIGHTEN (-3 + -3 = -6) or to EMERGENCY.
+# Rollback = restore -5 here + restart. See project_post_entry_recheck.
+ADX_BELOW_FLOOR_SCORE = 0            # score delta when cur_adx < ADX_BELOW_FLOOR (was -5)
 ATR_DROP_PCT = 0.30                  # 1h ATR% shrank > 30% vs entry       -> -3
 PRICE_AGAINST_CRITICAL_PCT = 0.5     # unrealized adverse move > 0.5%      -> -3
 PRICE_AGAINST_WARNING_PCT = 0.3      # unrealized adverse move > 0.3%      -> -1
--- a/virtual_trader.py
+++ b/virtual_trader.py
@@ -86,7 +86,7 @@
     WALL_TRAIL_LIVE_ENABLED,
     WALL_GROWTH_CRITICAL, WALL_GROWTH_WARNING,
     WALL_GROWTH_CRITICAL_SCORE, WALL_GROWTH_WARNING_SCORE,
-    ADX_DROP_THRESHOLD, ADX_BELOW_FLOOR, ATR_DROP_PCT,
+    ADX_DROP_THRESHOLD, ADX_BELOW_FLOOR, ADX_BELOW_FLOOR_SCORE, ATR_DROP_PCT,
     PRICE_AGAINST_CRITICAL_PCT, PRICE_AGAINST_WARNING_PCT,
     HEALTH_SCORE_EMERGENCY, HEALTH_SCORE_TIGHTEN,
 )
@@ -931,11 +931,16 @@
             parts.append(f"ADX -{entry_adx - cur_adx:.1f} (-3)")
             details.append({'rule': 'adx_drop', 'value': round(entry_adx - cur_adx, 3),
                             'threshold': ADX_DROP_THRESHOLD, 'points': -3})
+        # Weight lives in config (ADX_BELOW_FLOOR_SCORE) and is 0 as of 2026-07-26:
+        # the floor is still measured and still reported (evidence keeps flowing into
+        # the RECHECK line and recheck_events) but no longer moves the score. See config.py.
         if cur_adx < ADX_BELOW_FLOOR:
-            score -= 5
-            parts.append(f"ADX {cur_adx:.1f}<{ADX_BELOW_FLOOR:.0f} (-5)")
+            score -= ADX_BELOW_FLOOR_SCORE
+            parts.append(f"ADX {cur_adx:.1f}<{ADX_BELOW_FLOOR:.0f} "
+                         f"({-ADX_BELOW_FLOOR_SCORE:+d})")
             details.append({'rule': 'adx_below_floor', 'value': round(cur_adx, 3),
-                            'threshold': ADX_BELOW_FLOOR, 'points': -5})
+                            'threshold': ADX_BELOW_FLOOR,
+                            'points': -ADX_BELOW_FLOOR_SCORE})
     if entry_atr_pct and entry_atr_pct > 0 and cur_atr_pct is not None:
         if (entry_atr_pct - cur_atr_pct) / entry_atr_pct > ATR_DROP_PCT:
             score -= 3
@@ -970,18 +975,40 @@
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
+    Clamp (c) is the structural guard, added because clamps (a)+(b) never bounded
+    HOW FAR the midpoint could travel. Forensics: of 10 positions ever marked
+    recheck_status='tightened', EIGHT are losers whose max_adverse_price never
+    reached their ORIGINAL stop — the recheck's own move is what stopped them out
+    (-528.73 realised). Two of the eight (vpos 71, 72) were the wall rule, killed
+    2026-07-13; one (vpos 74) was adx_below_floor, killed by the config weight above;
+    for the other five the reason rotated out of the journal before recheck_events
+    existed. That is exactly why this clamp is worth having independently of any
+    single rule's weight: it makes the FAILURE CLASS unreachable no matter which
+    rule fires, including rules not yet written.
+
+    Because the recheck only runs PRE-BREAKEVEN (see the poller: `not be_applied`),
+    current_sl IS the original stop on every reachable path, so in practice this
+    makes a TIGHTEN verdict a LOGGED ADVISORY that moves no stop. EMERGENCY_CLOSE is
+    a separate branch and is NOT affected. Pass original_sl=None to get the old
+    unbounded behaviour (used by nothing; kept so the helper stays testable)."""
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
 
@@ -1094,7 +1121,8 @@
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

## 5. Validation B. versions' pure functions (`_health_score`, `_recheck_verdict`, `_tighten_sl`) were extracted
by AST from the *patched copies* and executed side by side. Nothing imported from the running bot;
no DB writes.

```
=== TEST 1 — replay vpos 74, the one TIGHTEN with persisted reasons ===
  OLD: score= -5 verdict=TIGHTEN  parts=['ADX 15.6<20 (-5)']
        -> SL 63489.3 -> 63103.600000000006
  NEW: score=  0 verdict=OK       parts=['ADX 15.6<20 (+0)']
  DB recorded: score=-5 verdict=TIGHTEN sl 63489.3->63103.6   (OLD reproduces the DB exactly)
  vpos74 maxAdverse=63119.8 vs origSL=63489.3 -> NEVER touched the original stop; realised -73.09

=== TEST 2 — _tighten_sl clamp (c), both sides, incl. pathological inputs ===
  SHORT entry=62717.9 cur_sl=63489.3 orig_sl=63489.3   [recheck runs pre-BE: current==original]
      OLD -> 63103.6000 (dist 0.615%)   NEW -> 63489.3000 (dist 1.230%)   never tighter: True
  LONG  entry=63788.4 cur_sl=62789.8 orig_sl=62789.8   [same, LONG]
      OLD -> 63289.1000 (dist 0.783%)   NEW -> 62789.8000 (dist 1.565%)   never tighter: True
  SHORT entry=62717.9 cur_sl=63200.0 orig_sl=63489.3   [hypothetical: current already tighter]
      OLD -> 62958.9500 (dist 0.384%)   NEW -> 63489.3000 (dist 1.230%)   never tighter: True
  LONG  entry=63788.4 cur_sl=63000.0 orig_sl=62789.8   [hypothetical: current already tighter]
      OLD -> 63394.2000 (dist 0.618%)   NEW -> 62789.8000 (dist 1.565%)   never tighter: True

=== TEST 3 — back-compat: original_sl=None reproduces OLD exactly ===
  identical for all cases: True

=== TEST 4 — do the other rules still reach TIGHTEN / EMERGENCY? ===
  adx_drop + atr_contraction                 OLD  -6/TIGHTEN         NEW  -6/TIGHTEN
  adx_drop + price_against_crit              OLD  -6/TIGHTEN         NEW  -6/TIGHTEN
  adx_below_floor ALONE (the vpos-74 shape)  OLD  -5/TIGHTEN         NEW   0/OK
  all three -3 rules (emergency reach)       OLD -14/EMERGENCY_CLOSE NEW  -9/TIGHTEN   <-- SIDE EFFECT
```

**TEST 4 row 4 is the one regression, and it belongs to Variant A only.** Dropping the ADX weight
to 0 removes 5 points from the *emergency* sum too, so a position that used to trip
EMERGENCY_CLOSE at -14 now lands on TIGHTEN at -9. EMERGENCY_CLOSE has fired exactly once in the
whole book (vpos 51, +2.74 — a winner, so not a demonstrated save). Mitigation if you want A
without the cost: a separate one-liner, `HEALTH_SCORE_EMERGENCY = -10 -> -9`.
**Variant B has no such side effect** — every score and verdict is byte-identical to today; only
the size of the stop move changes.

Mechanical checks:
```
py_compile b/config.py b/virtual_trader.py     -> OK (both files)
patch -p1 --dry-run < R1.patch                 -> CLEAN (2 files, 5 hunks)
git status --porcelain                         -> empty (working tree untouched)
md5sum config.py virtual_trader.py             -> identical to the pre-patch baseline
```

---

## 6. Snapshot / apply / rollback

**Snapshot first** (mirrors the `pre-flat-gate-fix-20260706` precedent):
```bash
cd /root
git tag pre-recheck-adx-fix-20260726
cd /root/titan-bot
cp config.py         config.py.bak_recheckadx_20260726
cp virtual_trader.py virtual_trader.py.bak_recheckadx_20260726
```

**Apply** — save §4 as `R1.patch`, then:
```bash
cd /root/titan-bot
patch -p1 < R1.patch          # full patch = A + B
# for B only: drop the config.py hunk and the two _health_score hunks first
python3 -m py_compile config.py virtual_trader.py
sudo systemctl restart titan.service
journalctl -u titan.service -n 40 --no-pager | grep -i recheck
```

**Rollback** — any of the three, all equivalent:
```bash
# 1. from the tag
git checkout pre-recheck-adx-fix-20260726 -- titan-bot/config.py titan-bot/virtual_trader.py

# 2. from the .bak copies
cp config.py.bak_recheckadx_20260726 config.py \
                   && cp virtual_trader.py.bak_recheckadx_20260726 virtual_trader.py

# 3. reverse the patch
cd /root/titan-bot && patch -R -p1 < R1.patch

sudo systemctl restart titan.service
```

**Config-only rollback of Variant A** — no code change: set `ADX_BELOW_FLOOR_SCORE = -5` in
`config.py` and restart. The rule is a config weight by design, exactly like `WALL_GROWTH_*_SCORE`.

---

## 7. What this does NOT do

* Does not touch the entry gate, the FLAT floor, the HTF cascade, or the advisor.
* Does not re-enable the wall-trail (`WALL_TRAIL_LIVE_ENABLED` stays `False`).
* Does not change 1R, breakeven, the trail, or `original_sl_price`.
* Does not change EMERGENCY_CLOSE under Variant B.
* Does not stop the recheck from *measuring* anything — every rule is still evaluated and still
  written to `recheck_events`. Only the stop move is bounded.
* **Nothing was applied.** Tree clean at `6c35b9d`; `titan.service` running unmodified.
