# sol-alignedv2-prereg-and-wall-shape-capture

_2026-08-02 17:28 UTC_

---

# MERCURY-SOL — ALIGNED-V2 RESTRICTION **PRE-REGISTERED** + WALL SHAPE NOW CAPTURED

**2026-08-02 ~17:40 UTC.** Neither item touches the frozen surface, and both checks were
**verified rather than assumed**. `ADVISOR_WALL_ALIGNED_V2` is **unchanged and still `True`**.
Follows `reports/2026-08-02-1714-sol-aligned-v2-evidence-and-storage-fix.md`. Titan untouched.

| | |
|---|---|
| service | active, worker pid **1499572**, booted 17:22:25 |
| `claude_advisor.py` / `config.py` | **not modified** — mtimes still 08-01 20:54 / 08-02 13:34 |
| `ADVISOR_WALL_ALIGNED_V2` | **`True`**, `config.py:426`, untouched |
| entry prompt | byte-identical; **window NOT reset** — 86 of 200 as of 17:40 |
| vpos 26 | open through both restarts, entry 73.53, SL 72.59 |
| errors since restart | none |

---

# PART 1 — THE PRE-REGISTERED DECISION

Written into `OPEN-ITEMS-SOL.md` today, dated, above both applied-change sections, marked
**OPERATOR DECISION, MADE AND RECORDED IN ADVANCE**. Reproduced here verbatim in substance.

## 1.1 The decision

> **When the 200-consultation window closes, `ADVISOR_WALL_ALIGNED_V2` will be RESTRICTED — not
> removed — unless new evidence contradicts what is already established.**
>
> **The restriction: the override may not fire when the overhead wall's multiple is at or above
> 20×.** Below ×20 it keeps firing exactly as today. This narrows the gate; it does not delete it,
> and it does not touch the SHORT companion (`ADVISOR_WALL_ALIGNED_SHORT_V2`).

**Nothing was changed today.** The flag is inside the entry-prompt freeze and the window has
**~114 consultations left** (86 of 200 recorded at 17:40 — up from 74 at the time of the 16:55
forensics; the file's "~147 left" was written against the earlier count and the arithmetic moves
with the window, which is the point of counting it rather than quoting it).

## 1.2 The rationale — all of it on the record now

1. **At `mult ≥ 20` AND `dist < 0.35%` the justifying study contains THREE rows, all negative** —
   mean **−3.20%/24h, 0 of 3 favourable** (2 of the 3 sit in the bull arm, at −3.56%). That is
   **not evidence against the override; it is the absence of evidence**, and what little exists
   points the other way.
2. **×20.3 is the 95th percentile of a distribution whose q3 is 16.8×.** The instruction was
   calibrated on the middle of its population and applied at the tail. Rows at `mult ≥ 20.3` are
   8 of 160 (5.0%); the bull arm's own maximum is 21.4×.
3. **The justifying metric is structurally blind to the failure mode the override creates.**
   `skip_drift_samples.drift_pct` is point-in-time price at the horizon versus the anchor — **no
   stop, no trail, no fees** — while every entry this override makes is **stop-sensitive by
   construction**, because it enters beneath a nearby opposing wall. On the four closed LONG flips
   the metric would have graded exactly **one** favourable: **vpos 18, at +0.85% drift, and the
   book's largest loser at −$234.04**.
4. **Realised, not modelled: 8 closed flips, net −$616.15.** LONG arm alone: **4 closed, net
   −$598.50, one win and three stop-outs.**

## 1.3 🔴 What would REVERSE it — pre-registered to the same standard as the decision

The restriction is **cancelled, and the override left untouched at all multiples**, if **either**
is observed before the window closes:

- **(R1) A flip at `mult ≥ 20` that closes profitably.** One is enough. It would be the first
  positive observation anywhere in that tail — currently **0 of 3** in the study and **0 of 1**
  realised. **vpos 26 itself qualifies: if it closes green, R1 is met and the restriction does not
  happen.**
- **(R2) The window's own data showing the verdicts are sound at that size** — aligned-LONG flips
  at `mult ≥ 20` whose outcomes are not worse than the sub-×20 flips. Judged on **realised close
  PnL, not drift**, for the reason in rationale 3.

**A partial or ambiguous result is NOT a reversal.** The default on ambiguity is to apply the
restriction, because the tail's evidence base is empty and the burden sits on keeping the wider
gate, not on narrowing it. That asymmetry is stated now, in advance, precisely so it cannot be
argued either way later.

**Recorded caveat, deliberately not argued away:** every number above rests on small n — 3 study
rows in the tail, 4 closed LONG flips. n=3 refutes nothing. This is explicitly **a judgement made
under absence of evidence**, not a claim that the override has been falsified, and it is recorded
that way so a future reader does not mistake it for a proven result.

---

# PART 2 — WALL SHAPE IS NOW CAPTURED

**Applied and LIVE 2026-08-02 17:22:25.** Backups: `skip_attribution.py.bak_wallshape_20260802`,
`trades.db.bak_pre_wallshape_20260802`.

## 2.1 What was missing

`skip_attribution` stored exactly three wall facts, because `_nearest_opposing_wall` returns
`walls[0]` and nothing else:

```python
wall_price, wall_strength = _nearest_opposing_wall(norm_dir, pre_trade_walls)   # walls[0] only
wall_dist_pct = abs(wall_price - anchor) / anchor * 100.0
```

So **"was that wall DOMINANT, or merely large?"** and **"was the opposing wall nearer than the
support?"** could not be asked of any stored row — and both became load-bearing on vpos 26, whose
opposing wall was ×20.3, **2.4× the next ask wall** and **nearer than either bid wall**. None of
that was ever a variable in the study that justified relaxing the wall veto.

## 2.2 The seven new columns

Computed by a new `_wall_shape()` from the `pre_trade_walls` dict **already in hand** at
`on_skip` — one pass over two short lists, no I/O, no new fetch.

| column | meaning | vpos 26 would have recorded |
|---|---|---|
| `opp_wall_next_mult` | mult of the **second** wall on the opposing side | 8.3 |
| `opp_wall_dominance` | nearest opposing mult ÷ next opposing mult | **2.446** |
| `sup_wall_price` | nearest **supporting** wall (bid for LONG, ask for SHORT) | 73.25 |
| `sup_wall_strength` | its mult | 27.4 |
| `sup_wall_distance_pct` | \|sup − anchor\| / anchor × 100 | 0.367% |
| `n_walls_opposing` | walls above the ×-threshold, opposing side | 3 |
| `n_walls_supporting` | same, supporting side | 2 |

"Is the opposing wall nearer than the support?" is then
`wall_distance_pct < sup_wall_distance_pct` — for vpos 26, **0.313% < 0.367% → true**.

**Conventions mirror the existing columns exactly**, so old and new rows stay comparable: distance
is **absolute** (as `wall_distance_pct` already is), "nearest" is index 0 (liquidity_zones sorts
nearest-to-mid on both sides), and the $0.50 **bucket-centre** caveat carries over unchanged — a
bucket straddling the mid can render up to $0.25 on the far side of it, which is *why* both
distances are absolute.

## 2.3 The patch

```diff
--- a/skip_attribution.py
+++ b/skip_attribution.py
@@ Wall helpers — new function after _nearest_opposing_wall
+def _wall_shape(direction, pre_trade_walls, anchor):
+    """2026-08-02 — CAPTURE THE SHAPE OF THE BOOK, not just its nearest wall.
+    [full docstring in source: rationale, the seven fields, the conventions,
+     and the bucket-centre caveat]
+    PURE MEASUREMENT. Written once at on_skip, read by no gate.
+    """
+    out = {'opp_wall_next_mult': None, 'opp_wall_dominance': None,
+           'sup_wall_price': None, 'sup_wall_strength': None,
+           'sup_wall_distance_pct': None,
+           'n_walls_opposing': None, 'n_walls_supporting': None}
+    if not pre_trade_walls:
+        return out
+    opp_key = 'walls_ask' if direction == 'LONG' else 'walls_bid'
+    sup_key = 'walls_bid' if direction == 'LONG' else 'walls_ask'
+    opp = pre_trade_walls.get(opp_key) or []
+    sup = pre_trade_walls.get(sup_key) or []
+    out['n_walls_opposing'] = len(opp)
+    out['n_walls_supporting'] = len(sup)
+    if len(opp) >= 2:
+        first = _safe_float(opp[0].get('mult'))
+        nxt = _safe_float(opp[1].get('mult'))
+        out['opp_wall_next_mult'] = nxt
+        if first is not None and nxt:      # nxt falsy (0/None) -> no ratio
+            out['opp_wall_dominance'] = round(first / nxt, 3)
+    if sup:
+        sp = _safe_float(sup[0].get('price'))
+        out['sup_wall_price'] = sp
+        out['sup_wall_strength'] = _safe_float(sup[0].get('mult'))
+        if sp is not None and anchor:
+            out['sup_wall_distance_pct'] = abs(sp - anchor) / anchor * 100.0
+    return out

@@ init_db — same idempotent-ALTER idiom as the existing trend_4h/trend_1d adds
         for _c in ('trend_4h', 'trend_1d'):
             if _c not in _sa_cols:
                 conn.execute(f"ALTER TABLE skip_attribution ADD COLUMN {_c} TEXT")
+        # 2026-08-02 — WALL SHAPE (see _wall_shape). Pure measurement columns,
+        # written once at on_skip, read by NO gate and by no advisor.
+        # 🔴 NOT BACKFILLABLE — every pre-existing row stays NULL, permanently.
+        # Cohorts spanning this date must treat NULL as "not measured", never as
+        # "no second wall".
+        for _c, _t in (('opp_wall_next_mult',    'REAL'),
+                       ('opp_wall_dominance',    'REAL'),
+                       ('sup_wall_price',        'REAL'),
+                       ('sup_wall_strength',     'REAL'),
+                       ('sup_wall_distance_pct', 'REAL'),
+                       ('n_walls_opposing',      'INTEGER'),
+                       ('n_walls_supporting',    'INTEGER')):
+            if _c not in _sa_cols:
+                conn.execute(f"ALTER TABLE skip_attribution ADD COLUMN {_c} {_t}")

@@ on_skip — compute alongside the existing nearest-wall block, then persist
         if wall_price is not None and anchor:
             wall_dist_pct = abs(wall_price - anchor) / anchor * 100.0
+        # 2026-08-02: wall SHAPE alongside the nearest wall — dominance over the
+        # next wall on the same side, the nearest SUPPORTING wall, and the counts.
+        # Never raises: _wall_shape is total over a missing/empty dict.
+        shape = _wall_shape(norm_dir, pre_trade_walls, anchor)
@@ the INSERT — 7 columns and 7 placeholders added
                 "matrix_direction, trend_4h, trend_1d, "
+                "opp_wall_next_mult, opp_wall_dominance, sup_wall_price, "
+                "sup_wall_strength, sup_wall_distance_pct, "
+                "n_walls_opposing, n_walls_supporting, "
                 "tracking_status, created_at, updated_at) "
-                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, 'active', ?, ?) "
+                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, 'active', ?, ?) "
                 "ON CONFLICT(trades_row_id) DO NOTHING",
                 (... trend_4h, trend_1d,
+                 shape['opp_wall_next_mult'], shape['opp_wall_dominance'],
+                 shape['sup_wall_price'], shape['sup_wall_strength'],
+                 shape['sup_wall_distance_pct'],
+                 shape['n_walls_opposing'], shape['n_walls_supporting'],
                  skip_ts, skip_ts),
```

## 2.4 🔴 It changes no value on the entry path — verified, not asserted

**(a) The advisor cannot read `skip_attribution`.** A codebase-wide grep for the module name
returns imports in exactly **two** files:

```
main.py:813          import skip_attribution          <- the write hooks
virtual_trader.py:85 from skip_attribution import tick <- the drift sampler
```

**`claude_advisor.py` does not import it at all.** There is no path from this table to the entry
prompt.

**(b) No gate reads it either.** `_record_skip_attribution` is called *after* each refusal is
already decided (`htf_blocked` main.py:2464, `below_threshold` 2890, `risk_halt` 2930,
`ai_skipped` 3254) and returns nothing into the trade path. The seven new columns are **written
once and read by nothing** — not by a gate, not by the optimizer, not by the advisor.

**(c) The 200-window is not reset.** The entry prompt is byte-identical; 86 of 200 stands.

## 2.5 Verified — isolated test first, then live

**Isolated test on a scratch DB copy, using vpos 26's actual book.** Per the standing lesson that
overriding one module's `DB_PATH` is not enough, the whole call graph was checked first:
`skip_attribution` opens a DB in exactly one place (`_connect()` → module-level `DB_PATH`) and no
callee opens another, so overriding that one name **fully** isolates the test.

```
shape(): {'opp_wall_next_mult': 8.3, 'opp_wall_dominance': 2.446,
          'sup_wall_price': 73.25, 'sup_wall_strength': 27.4,
          'sup_wall_distance_pct': 0.36724700761696955,
          'n_walls_opposing': 3, 'n_walls_supporting': 2}
empty  : all None                      <- degrades cleanly on a missing dict
1 wall : dominance None, counts 1/0    <- no second wall -> no ratio, not a crash

row written to the scratch DB:
  nearest_wall_price    = 73.75      opp_wall_next_mult    = 8.3
  wall_strength         = 20.3       opp_wall_dominance    = 2.446
  wall_distance_pct     = 0.31284    sup_wall_strength     = 27.4
  sup_wall_price        = 73.25      sup_wall_distance_pct = 0.36725
  n_walls_opposing      = 3          n_walls_supporting    = 2
  opposing nearer than support? True
  drift rows created: 5              <- the existing behaviour still intact

live DB rows matching the test id: 0  <- isolation held
```

Every value matches the figures independently derived in the 16:55 forensics — the 2.446 is the
"2.4× the next ask wall" from that report, now a stored number rather than a hand calculation.

**Live, after the 17:22:25 restart:**

| id | time | dir | opp mult | next | **dominance** | sup mult | n opp / n sup |
|---|---|---|---|---|---|---|---|
| 8781 | 17:25:18 | SHORT | 16.4 | 12.8 | **1.281** | 10.3 | 3 / 3 |
| 8782 | 17:25:19 | SHORT | 16.4 | 12.8 | **1.281** | 10.3 | 3 / 3 |
| 8783 | 17:25:19 | SHORT | 16.4 | 12.8 | **1.281** | 10.3 | 3 / 3 |

**The first live reading already discriminates:** dominance **1.281** — a large but *non*-dominant
wall — where vpos 26's was **2.446**. Same `wall_strength` bracket, entirely different shape. That
is precisely the distinction that was invisible before today.

⚠️ **A false alarm worth recording**, because it is the exact trap this project keeps hitting: the
first rows I inspected after the restart (8779/8780, skip_ts 17:20:18–19) had all seven columns
NULL. They were written **before** the 17:22:25 worker boot, by the old module — a stale-read, not
a defect. Checked the boot timestamp against the row timestamps rather than trusting the first
query. **Fix on disk ≠ fix in the running process**, and the boundary is the worker's boot time.

## 2.6 🔴 Historical rows cannot be backfilled — recorded

The input is the full `pre_trade_walls` dict as it stood at skip time. Only `walls[0]` was ever
persisted, and the OKX book is a live snapshot with no history — there is no source to reconstruct
from, in the DB or anywhere else.

**All 8,780 pre-existing `skip_attribution` rows stay NULL on these columns, permanently.**

**Any cohort spanning 2026-08-02 must treat NULL as "not measured", never as "no second wall".**
The two are indistinguishable in the old rows, and conflating them would silently make every
historical skip look like it faced a lone wall. That warning is in the source comment, in
`OPEN-ITEMS-SOL.md`, and here.

**Practical consequence:** the dominance question becomes answerable **from 2026-08-02 forward
only**. At the current rate (~86 consultations/day, most of them refusals that anchor a row) the
table will hold a few hundred shaped rows within a week — but the 30-day study that justified the
override **cannot be re-cut on it, ever**. A future dominance analysis is a new measurement on new
data, not a re-reading of the old one.

---

## ROLLBACK

```bash
cd /mnt/volume_nyc1_1780480650620/mercury-sol
cp skip_attribution.py.bak_wallshape_20260802 skip_attribution.py
cp OPEN-ITEMS-SOL.md.bak_20260802_1710        OPEN-ITEMS-SOL.md   # also reverts the pre-registration
systemctl restart mercury-sol
# the seven COLUMNS can stay — additive and unread by the old code.
# DB rollback (only if ever needed): trades.db.bak_pre_wallshape_20260802
```

## VERIFY

```bash
# the flag was NOT changed
grep -n '^ADVISOR_WALL_ALIGNED_V2 ' config.py          # -> True, LIVE 2026-07-02

# the advisor cannot see skip_attribution
grep -rn 'skip_attribution' claude_advisor.py          # -> 0 hits

# live wall shape
sqlite3 "file:trades.db?mode=ro" "select id,wall_strength,opp_wall_next_mult,
  opp_wall_dominance,sup_wall_strength,n_walls_opposing,n_walls_supporting
  from skip_attribution where opp_wall_dominance is not null order by id desc limit 5;"
```

_2026-08-02. Mercury-SOL is PAPER. `ADVISOR_WALL_ALIGNED_V2` unchanged and inside the freeze; the
entry prompt is byte-identical and the 200-window is not reset (86/200). Titan untouched._
