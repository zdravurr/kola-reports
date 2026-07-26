# long-exit-contract-sim-and-diff

_2026-07-26 18:46 UTC_

---

# TITAN — LONG exit contract: simulation, choice, and prepared diff

**2026-07-26 · Steps A + B + diff. NOT APPLIED.** Tree clean at `b878535`. Paper mode.

**Choice: STRUCTURE = partial realisation, LONG-only. Parameters 1/3 @ 1.0R, config-driven.**
On the clean sample: **-343.10 → -248.28, +94.83, zero winners cut.** The larger gains
(target 1.0R, +284.48) are rejected — not because they simulate worse, but because n=10 cannot
choose a parameter and a fixed target has the harshest failure mode if a long runner ever appears.

---

## Step A — simulation

### A.0 Simulator and its validation

Model: `net = notional × exit% / 100 − fees − funding`, with `notional` reconstructed per position
from its own arithmetic (verified: `gross − fees − funding = net` on every row carrying `gross_pnl`).
The contract is reproduced exactly as coded: no trail before +1R; at +1R the SL moves to breakeven
and the trail arms at `water_mark × (1 − trail_pct/100)`; the exit is whichever of breakeven / trail
price is met first. Signal ("external") exits that occurred before any retracement are kept as-is.

Baseline vs actual:
```
LONG  clean n=10   actual -344.68   simulated -343.10   error +1.57  (0.46%)
SHORT clean n=21   actual +1555.52  simulated +1623.18  error +67.67 (4.35%)
```
The short-side +4.35% is the simulator being slightly optimistic where the real fill slipped past
the trail trigger between polls (vpos 56, 44, 43 account for most of it). **All variant deltas below
are measured against the SIMULATED baseline**, so that bias cancels.

### A.1 LONG — clean n=10, baseline **-343.10**, win 5/10

| variant | net | Δ | win | winners cut | losers improved |
|---|---|---|---|---|---|
| A. baseline (current rule) | -343.10 | — | 5/10 | — | — |
| B. partial 1/3 @ 0.75R | -220.16 | **+122.94** | 5/10 | 1 | 1 |
| B. partial 1/2 @ 0.75R | -158.69 | **+184.42** | 5/10 | 1 | 1 |
| **B. partial 1/3 @ 1.0R** | **-248.28** | **+94.83** | 5/10 | **0** | 0 |
| B. partial 1/2 @ 1.0R | -200.87 | +142.24 | 5/10 | **0** | 0 |
| D. target 1.0R | **-58.63** | **+284.48** | 5/10 | 0 | 0 |
| D. target 1.25R | -144.11 | +199.00 | 5/10 | 0 | 0 |
| C. trail 0.5R *[upper bound]* | -178.35 | +164.76 | 5/10 | 1 | 0 |
| C. trail 0.6R *[upper bound]* | -233.54 | +109.57 | 5/10 | 1 | 0 |
| C. trail 0.75R *[upper bound]* | -316.32 | +26.79 | 5/10 | 1 | 0 |

Only **4 of 10** clean longs ever armed the trail (MFE ≥ 1R): vpos 79 (1.59R), 39 (1.29R),
54 (1.16R), 45 (1.06R). Every variant's gain comes from those four plus, at the 0.75R level,
vpos 41 (peaked 0.91R, ended -1.05R). **No single position drives the result** — all four
contribute, which is the one encouraging robustness signal in a sample this small.

### A.2 SHORT — clean n=21, baseline **+1623.18**, win 14/21 (control)

| variant | net | Δ | winners cut |
|---|---|---|---|
| A. baseline | +1623.18 | — | — |
| B. partial 1/3 @ 0.75R | +1431.90 | **-191.28** | 8 |
| B. partial 1/2 @ 0.75R | +1336.26 | **-286.92** | 8 |
| B. partial 1/3 @ 1.0R | +1446.39 | **-176.80** | 5 |
| B. partial 1/2 @ 1.0R | +1357.99 | **-265.20** | 5 |
| D. target 1.0R | +1092.79 | **-530.40** | 6 |
| D. target 1.25R | +1318.80 | **-304.38** | 6 |
| C. trail 0.5R *[upper bound]* | +2387.36 | +764.18 | 0 |
| C. trail 0.6R *[upper bound]* | +2218.63 | +595.45 | 0 |

**Every partial and every target damages the short side.** That is the strongest confirmation that
the current contract is correct for shorts and that this must be a one-sided change.

### A.3 The short tail under each variant — the disqualification test

| vpos | MFE | baseline | D 1.0R | D 1.25R | B 1/2@1R | C 0.6R | C 0.75R |
|---|---|---|---|---|---|---|---|
| 33 | 7.38R | +0.78 | +0.09 | +0.13 | +0.43 | +1.08 | +1.05 |
| **58** | **3.40R** | **+371.29** | +146.74 | +185.42 | +259.01 | +425.01 | +401.80 |
| **48** | **2.98R** | **+442.46** | +211.71 | +266.84 | +327.09 | +516.15 | +483.08 |
| 49 | 2.98R | +442.46 | +211.71 | +266.83 | +327.08 | +516.15 | +483.08 |
| 43 | 2.31R | +176.78 | +129.96 | +164.18 | +153.37 | +227.20 | +206.67 |
| 44 | 2.31R | +176.76 | +129.96 | +164.18 | +153.36 | +227.17 | +206.64 |
| 81 | 1.87R | +79.79 | +90.55 | +114.98 | +85.17 | +117.13 | +102.47 |
| 50 | 1.80R | +294.39 | +341.74 | +429.31 | +318.06 | +412.38 | +359.84 |
| **Σ runners** | | **+1984.71** | **+1262.45** | +1591.86 | +1623.58 | +2442.28 | +2244.63 |

`D 1.0R` removes **36%** of the runner cohort. `B 1/2 @1R` removes 18%. **Both are disqualified for
shorts**, which is exactly why the diff is long-only. Note the 7.38R case (vpos 33) is a micro-size
position — its R-multiple is extreme but its dollars are not, so it carries no weight either way.

### A.4 Variant C is NOT decidable on this data — stated plainly

A narrower trail exits at the first retracement of its own width from the **running** peak, so it
can exit before the global peak. Simulating it from endpoints (MFE, exit) assumes the global peak
was reached first — an **optimistic upper bound**, not an estimate. Real paths exist only for
`position_excursion_samples` (vpos 61–82), and among clean, armed positions that is **one long and
one short**:
```
vp79 LONG   MFE 1.59R  base  +80.14 | 0.5R path +163.85 (bound +163.86) | 0.6R +147.92 | 0.75R +124.01
vp81 SHORT  MFE 1.87R  base  +79.79 | 0.5R path +126.90 (bound +126.90) | 0.6R +117.13 | 0.75R +102.47
```
Path and bound coincide on both — but on **n=1 per side**, and only because these two paths rose
almost monotonically. **Variant C is not eliminated; it is unevaluated.** Choosing it would mean
acting on an upper bound. It is the natural candidate to revisit once path coverage extends beyond
vpos 61+ — note that the excursion logger now runs on every position, so this resolves itself with
time and no new work.

---

## Step B — the choice

**Structure: partial realisation. Not a target, not a narrower trail.**

*Why not the target*, despite it simulating best (+284.48): a 1.0R target caps every long at 1R
forever. Its whole advantage rests on longs having no right tail — and that finding is **0/10 at 2R
with P = 0.035** under the shorts' rate. Marginally significant on ten positions. If the absence of
long runners is sampling rather than structure, a fixed target permanently forecloses the fix. The
short-side control shows precisely what that costs when a tail does exist: **-36% of the runner
cohort**.

*Why not the narrower trail*: §A.4 — not evaluable on n=1 paths.

*Why the partial*: its worst case is bounded and proportional. If a 3.4R long appears, a 1/3 partial
at 1R yields ≈2.6R against the trail's ≈2.4R and the target's 1.0R. It cannot cap a trade, only
shave it. It also needs **no new concept in the exit path** — it reuses the +1R point at which
breakeven and the trail already arm.

### Parameter or structure? **Structure only.**

n = 10 clean longs, of which **6 ever exceeded 0.5R and 5 were winners**. The spread between
candidate parameters is decided by one or two positions:
* 0.75R beats 1.0R (+184 vs +142 at ½) **entirely because it catches vpos 41**, a single loser that
  peaked at 0.91R. One trade.
* ½ beats ⅓ by construction on a sample with no runners; on a sample with one, the ordering reverses.

**So the numbers are not chosen — they are defaulted, conservatively, and exposed as config
constants.** `1/3 @ 1.0R` is the mildest corner of the grid: it is the only partial variant that cut
**zero** winners in simulation, and 1.0R reuses an arming point that already exists rather than
introducing a new level. Its simulated gain (+94.83) is the smallest of the credible options — that
is the price of not overfitting, and it is the right price to pay at n=10.

**What n the parameter needs:** to separate 0.75R from 1.0R, and ⅓ from ½, at the effect sizes seen
here requires roughly **8–10 clean longs in each comparison bucket**, i.e. on the order of **30+
clean long closes with MFE above 0.5R**. Current count: 6. At the rate of the last 65 days that is
a multi-month wait — the same horizon as R2. Until then the constants should be treated as
placeholders, not findings.

---

## Step C — the prepared diff (LONG-ONLY)

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

### What it does
1. Three config constants with the full evidence trail in the comment, including the rejected
   alternatives and their simulated numbers, so a future session cannot re-derive this blindly.
2. Two additive columns (`partial_taken`, `realized_partial_usdt`), NULL on every legacy row →
   every existing position keeps the old contract exactly.
3. `_take_long_partial()` — banks the tranche's PnL and shrinks each DCA leg by the same fraction.
   Entry fees are charged pro-rata so the remainder is not billed twice at final close.
   Wrapped in try/except: any failure leaves the position untouched.
4. One hook at section **1d**, before breakeven, gated on `position_side == 'LONG'` and firing once.
5. `_do_close` folds `realized_partial_usdt` into the final `net_pnl` so the recorded figure stays a
   whole-position number. Zero for every position that took no partial → arithmetic unchanged.

### Scope — what it does NOT touch
* **SHORTS** — gated out at the hook. Their contract is byte-identical.
* **SL placement itself** — the original stop, `original_sl_price` and `_one_r_distance` are read,
  never written. 1R is still measured off the ORIGINAL stop.
* **Recheck fix `93c20c3`** — `_tighten_sl` and its call site are not in the diff.
* **Entry gate, FLAT floor (`CONFLUENCE_FLAT_THRESHOLD`), HTF cascade, confluence matrix, advisor**
  (`claude_advisor.py` is not in the diff at all), wall-trail (still `False`), every sensor, and
  Mercury-SOL.
* **Breakeven and trail logic** — untouched; the remainder rides the identical rule.

Two limitations stated rather than buried:
* **Paper path only.** `breakeven_worker.py` (the live path) has no equivalent. `LIVE_TRADING_ENABLED`
  is `False`, so this is currently complete — but live parity is a separate change and must not be
  forgotten if live is ever re-enabled.
* `LONG_PARTIAL_ENABLED = True` in the diff. Setting it `False` restores the current rule exactly,
  with no other edit.

### Snapshot / apply / rollback
```bash
# snapshot
cd /root && git tag pre-long-partial-20260726
cd /root/titan-bot
cp config.py         config.py.bak_longpartial_20260726
cp virtual_trader.py virtual_trader.py.bak_longpartial_20260726

# apply
patch -p1 < LP.patch
python3 -m py_compile config.py virtual_trader.py
sudo systemctl restart titan.service

# rollback — any of the three
git checkout pre-long-partial-20260726 -- titan-bot/config.py titan-bot/virtual_trader.py
cp config.py.bak_longpartial_20260726 config.py && cp virtual_trader.py.bak_longpartial_20260726 virtual_trader.py
patch -R -p1 < LP.patch
# or, without touching code at all:  LONG_PARTIAL_ENABLED = False  + restart
```
Verification after apply: the next LONG reaching +1R must log `[VIRTUAL] LONG PARTIAL vpos=…` and
leave `partial_taken=1` with a non-zero `realized_partial_usdt`; the next SHORT reaching +1R must
log nothing new.

`py_compile` OK on both files · `patch -p1 --dry-run` CLEAN (2 files) · working tree clean at
`b878535`.

---

**Nothing applied.** Session commits: `93c20c3`, `596fbdf` (superseded), `b878535`.
`titan.service` healthy, Mercury-SOL untouched.
