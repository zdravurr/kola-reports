# TITAN — G2 AND G3 FIXED: ONE CLOSE NUMBER, AND A STOP ON THE RIGHT TIMEFRAME

**2026-08-06 01:15 UTC · APPLIED · `999572a` · from `7c2feac`**

Acts on the 00:50 geometry audit. **G1 is recorded as BLOCKED ON THE OPTIMIZER AUDIT** with the
specific question it poses; G4, G5, G7, G8, G9 are recorded untouched.

**§0 before touching anything:** `openitems_guard.py` **exit 0** (runtime HEAD `7c2feac`, 11 watched
values) · tree clean · service `active`, `NRestarts=0` · double probe `{}` errors `[]` · 0 open
orders · **0 open rows**, `MAX(id)=92`.

---

## §1 — 🔴 G3: THE BOOT RE-ATTACH NOW READS THE CONFIGURED TIMEFRAMES

### (a) Config, not a hardcoded string — because that is exactly how it got here

`main._reconcile_side`'s naked-position branch fetched `'5m'` while `SL_ATR_TF` **and**
`TRAIL_ATR_TF` are both `'1h'`.

```python
-        atr = true_atr(exchange.fetch_ohlcv(symbol, '5m', limit=ATR_LEN * 3))
+        _atr_by_tf = {}
+
+        def _atr_for_tf(tf):
+            if tf not in _atr_by_tf:
+                _atr_by_tf[tf] = true_atr(
+                    exchange.fetch_ohlcv(symbol, tf, limit=ATR_LEN * 3))
+            return _atr_by_tf[tf]
+
+        try:
+            atr = _atr_for_tf(SL_ATR_TF)             # the STOP's timeframe
+            atr_trail = _atr_for_tf(TRAIL_ATR_TF)    # the TRAIL's timeframe
…
         raw = (entry_price - SL_ATR_MULT * atr if side == 'LONG'
                else entry_price + SL_ATR_MULT * atr)
         sl_price = float(exchange.price_to_precision(symbol, raw))
-        trail_pct = round(TRAIL_MULT_ATR * atr / entry_price * 100, 3)
-        src = 'fallback-ATR'
+        trail_pct = round(TRAIL_MULT_ATR * atr_trail / entry_price * 100, 3)
+        src = f'fallback-ATR({SL_ATR_TF})'
```

**Fetched INDEPENDENTLY, not shared.** Sharing one fetch between the two would re-create the
identical defect the moment `SL_ATR_TF` and `TRAIL_ATR_TF` diverge — which is precisely what
happened when `SL_ATR_TF` moved to `'1h'` and this branch was left behind. The memo dict means that
today, with both `'1h'`, it is still a **single** network call: proven by execution, the timeframes
fetched are `['1h']`.

**The size of what was wrong**, measured rather than asserted:

| | distance | % of price | vs intended |
|---|---|---|---|
| intended `2.25 × ATR_1h` | **558.99** | 0.8646% | 1.000× |
| what this branch placed `2.25 × ATR_5m` | **106.95** | 0.1654% | **0.191×** |

A **0.165% stop on BTC** is inside ordinary minute-to-minute noise, and it was placed on a **live
position just found NAKED after a restart**. Proven forward on the fixed code: with entry 64,656.20
the stop now goes to **64,097.2** (the intended level); the pre-fix code would have placed
**64,549.3** — 0.191× the distance.

### (b) 🔴 If the ATR fetch fails: attach NOTHING, and say so

I agree with the brief and the code now says it in words. The previous behaviour was already
"alert and return", so this is a sharpening rather than a reversal — but the reasoning is now
written down where the next reader will find it:

```python
+            # 🔴 ATTACH NOTHING RATHER THAN ATTACH A WRONG LEVEL. This branch only
+            # runs when the position is ALREADY naked, so there is nothing to
+            # make worse by declining — but there is plenty to make worse by
+            # guessing a stop from whatever ATR happens to be reachable. A stop at
+            # the wrong distance is not partial protection: too tight it hands the
+            # position back to the market at a level nobody chose, too loose it
+            # misstates the risk every later R is measured against.
             send_tg(f"🚨 <b>NAKED {side} position</b> {symbol}; ATR fetch failed "
-                    f"(<code>{e}</code>) — cannot re-attach SL. MANUAL ACTION.")
+                    f"for {SL_ATR_TF}/{TRAIL_ATR_TF} (<code>{e}</code>) — "
+                    f"<b>NOTHING was attached</b>; a stop at a guessed distance "
+                    f"is worse than none. MANUAL ACTION.")
```

**A guard that would have silently stopped matching, caught in the same pass.** `src` now carries
its timeframe (`fallback-ATR(1h)`), so the downstream test had to change with it:

```python
-    if src == 'fallback-ATR':
+    if src.startswith('fallback-ATR'):
```

Left as `==`, the one alert that tells the operator *"this level was reconstructed, not recovered —
verify it"* would have stopped firing, and nothing would have said so. That is the same class this
codebase keeps finding, and it was introduced by my own edit two lines earlier.

### (c) The trail is fixed by the same factor, and the enqueue gate is untouched

`trail_pct` now uses `atr_trail` off `TRAIL_ATR_TF`. The enqueue path is unchanged:
`_resume_job_if_needed` still returns at its first line under `engine_owns_position()` — **verified
True by execution** — and `breakeven_jobs` is still **0 rows**. `breakeven_jobs` is empty by design
and stays so.

---

## §2 — 🔴 G2: THE PARTIAL'S BANKED PnL REACHES EVERY CONSUMER

### (a) The correction moved into the unifier, not onto the object

The defect was that `_do_close` corrected a **local**:

```python
-    report = close_report.build_close_report(…)
-    net_pnl = report.net_pnl
-    _rp = row['realized_partial_usdt'] or 0.0
-    if _rp:
-        net_pnl += _rp          # ← the row gets this; `report` keeps the remainder-only figures
+    _rp = (row['realized_partial_usdt'] if 'realized_partial_usdt' in _rk else None) or 0.0
+    report = close_report.build_close_report(…, realized_partial_usdt=_rp)
+    net_pnl = report.net_pnl
```

and in `close_report.build_close_report`:

```python
+    realized_partial_usdt = float(realized_partial_usdt or 0.0)
     gross_pnl = (exit_price - entry_price) * size * direction
-    net_pnl = gross_pnl - entry_fee - exit_fee - funding_paid
+    net_pnl = (gross_pnl - entry_fee - exit_fee - funding_paid
+               + realized_partial_usdt)
```

**Fields set: `net_pnl` and, through it, `r_multiple`; plus the new `realized_partial_usdt` field
carried on `ClosedTrade` for the renderer.**

🔴 **`r_multiple` is recomputed from the corrected `net_pnl` against the SAME stored
`initial_risk_usdt` — it is not re-derived and not rescaled by the partial.** That is deliberate:
`initial_risk_usdt` is the position's 1R **at entry**, so leaving it alone is what keeps R
comparable to this position's own entry and to every other row in the book. Proven:
`r_multiple == net_pnl / initial_risk_usdt` exactly.

**`gross_pnl` is deliberately NOT inflated.** The banked figure is already net of that tranche's exit
fee and its pro-rata share of the entry fee, and `_take_long_partial` shrank the remaining legs'
`fee` by the same fraction — so the `entry_fee` passed in is the remainder's share only, and adding
the banked amount to gross would double-count. `gross_pnl` stays the remainder's price move, and the
renderer shows the banked tranche on its own line so `Net` cannot silently exceed `Gross − fees` and
look wrong:

```
🟩 Partial banked: +18.9071  (already realised on an earlier tranche; included in Net)
```

**Why the unifier and not the caller:** `build_close_report` is the one place every close passes
through, so a caller cannot forget the correction and no consumer can disagree. The new argument
defaults to `0.0`, so **all six call sites are unchanged** and a close with no partial is
byte-identical — verified.

### (b) 🔴 No historical row is rewritten — vpos 82 checked bit-for-bit

```
LIVE vpos 82: net_pnl=53.7926071500006  gross=42.4633600000003  banked=18.907093923333633
✅ net_pnl still the ORIGINAL whole-position figure, bit-for-bit
✅ realized_partial_usdt untouched     ✅ gross_pnl untouched
✅ live MAX(id) still 92 — no test row escaped the isolated copy
```

`build_close_report` only runs **forward**, on a close. The row was already correct; only the report
was wrong, and that report was sent months ago. Nothing re-sends it and nothing back-fills it.

### (c) G6 — the docstring now describes the code

```python
-    """Canonical result of a close. net_pnl is authoritative for DB + Telegram."""
+    """Canonical result of a close.
+
+    🔴 `net_pnl` IS THE WHOLE-POSITION FIGURE AND IS AUTHORITATIVE FOR THE DB,
+    TELEGRAM, THE BATCH BLOCK AND THE OBSERVATORY — all four read THIS object,
+    and since 2026-08-06 they all read the same number from it.
+
+    That sentence used to say "authoritative for DB + Telegram" and was false for
+    both at once (G2): … Measured on vpos 82: +1.0386R in the row against
+    +0.6736R in the report, a gap of 0.3651R and $18.91. …
+    """
```

### (d) Proven by execution — isolated DB, all 19 `DB_PATH` attrs patched, hard leak assert

A close **with** a partial, driven through the real `_do_close`:

```
ROW         net_pnl = 55.808900
REPORT      net_pnl = 55.808900    r_multiple = +1.077558
OBSERVATORY net     = 55.80890014999984   r = 1.077558377425406
TELEGRAM render contains the banked line: True

✅ ROW net_pnl == REPORT net_pnl
✅ OBSERVATORY net == REPORT net          ✅ OBSERVATORY r == REPORT r
✅ r_multiple is net / initial_risk_usdt (same denominator, not re-derived)
✅ the banked tranche IS in net           ✅ gross_pnl NOT inflated (remainder's price move only)

PRE-FIX  remainder-only net = 36.9018   R = +0.7125
CORRECTED           net = 55.8089   R = +1.0776
GAP CLOSED              = +18.9071 USDT / +0.3651R
```

**+0.3651R — the exact gap measured on vpos 82 in the 00:50 audit, closed.**

A close with **no** partial:

```
✅ net_pnl unchanged      ✅ r_multiple unchanged      ✅ no banked line rendered
```

---

## §3 — RECORDED, NOT FIXED

### 🔴 G1 — BLOCKED ON THE OPTIMIZER AUDIT

`trail_pct` is a fraction **of the ENTRY price**, applied **to the WATER MARK**. The giveback drifts
with MFE, in **opposite directions on the two sides**. Measured on the 14 positions that actually
closed on the trail, mechanism isolated from gap/slippage:

| side | n | mechanism giveback | nominal (`pct × entry`) | skew |
|---|---|---|---|---|
| **LONG** | 3 | **1.0160R** | 0.9997R | **+0.0163R (+1.63%)** |
| **SHORT** | 11 | **0.9591R** | 1.0000R | **−0.0409R (−4.09%)** |

Forward at the new geometry: **MFE 1.0R → 0.7560R · 2.0R → 0.7625R · 3.0R → 0.7690R.** The
documented 0.7500R is exact only at `water_mark == entry`, which never happens — the trail arms at
+1R.

🔴 **THE QUESTION, and it decides whether this is a documentation defect or a calibration error:**

> **Did the 2026-08-04 grid compute giveback as `pct × entry` or as `pct × water_mark`?**

- **`pct × water_mark`** → the grid measured the real mechanism, and **1.6875 is calibrated against a
  quantity the engine produces**. G1 collapses to a wrong label.
- **`pct × entry`** → **1.6875 was chosen against a number the engine does not produce**, the R-axis
  of §2.53's re-run is offset, and the offset is side-dependent in the **same direction** as the
  LONG-vs-SHORT gap the partial exists to fix.

**Not fixable before that answer**, because the fix is not obviously "use the entry base" — if the
grid measured the water-mark base, changing the engine would invalidate the calibration instead of
repairing it. **Until answered: do not quote "trail = 0.75R" as a fact and do not re-tune
`TRAIL_MULT_ATR` on it.** Recorded in the canon as **§0.1**. **0 positions have closed on the new
geometry**, so nothing has yet contradicted the label out loud.

### The rest, untouched

- **G4** — `initial_risk_usdt` is computed from the **requested** size before the fill and never
  recomputed. Only wrong on a **partial entry fill**, and item 14 is not implemented. All 7 live rows
  agree to four decimals because every fill so far was full.
- **G5** — the stored `atr` column is the **5m** ATR while the stop is built on **1h** (5.35× on
  vpos 86). `config.py:192` already warns *"NOT the 5m atr shown in entry logs"* — the warning was
  written and the column left misleading. **Note it is now MORE isolated, not less:** G3 removed the
  only place where a 5m ATR reached a *placed* stop; what remains reads it into a reported level and
  a Telegram line.
- **G7** — breakeven *"can no longer lose"* excludes funding, which is tracked and subtracted at
  close.
- **G8** — `trail_pct` quantised to 3 dp (±0.08% of trail width).
- **G9** — the breakeven Telegram reads the stale pre-`UPDATE` row; a no-op only while
  `ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True`.

---

## §4 — WHAT CHANGED, AND WHAT PROVABLY DID NOT

```
main.py             CODE-CHANGED: _reconcile_side          ADDED: _atr_for_tf (nested)
close_report.py     CODE-CHANGED: build_close_report, telegram
virtual_trader.py   CODE-CHANGED: _do_close
breakeven_worker.py CODE-CHANGED: none
order_adapter.py    CODE-CHANGED: none
```

**4 functions changed, 1 added, nothing else.** Plus one dataclass field
(`ClosedTrade.realized_partial_usdt`, default `0.0`) — `ClosedTrade` is constructed in exactly one
place, inside `build_close_report`, so no other construction site exists to break.

**No DB schema change:** `realized_partial_usdt` was already a `virtual_positions` column (44
columns, present, unchanged). No `CREATE TABLE`, `ALTER TABLE` or `ADD COLUMN` in the diff.

**Untouched, checked by grepping the diff rather than asserted:** no added or removed line matches
`SL_ATR_MULT=`, `TRAIL_MULT_ATR=`, `SL_ATR_TF=`, `TRAIL_ATR_TF=`, `*_ENABLED=`, `*_THRESHOLD=`,
`CREATE TABLE`, `ALTER TABLE`, `ADD COLUMN`, `SYSTEM_PROMPT`, `PROMPT=`, `HARD RULE`, `SOFT RULE`.
Re-read by importing `config` after the restart: `SL_ATR_MULT = 2.25`, `TRAIL_MULT_ATR = 1.6875`,
`SL_ATR_TF = 1h`, `TRAIL_ATR_TF = 1h`, `CONFLUENCE_SCORE_THRESHOLD = 3.0`,
`CONFLUENCE_FLAT_THRESHOLD = 5.0`. **Gates, geometry constants, score bars, both prompts and every
schema untouched.**

`ast.parse` ✅ and `py_compile` ✅ on all five modules.

## §5 — RESTARTED DELIBERATELY, FROM FLAT

| | before | after |
|---|---|---|
| `virtual_positions` open rows | **0** | **0** |
| double probe (positions) | `{}`, errors `[]` | **`{}`, errors `[]`** |
| open orders | 0 | **0** |
| `MAX(id)` | 92 | **92** |

Restarted **01:12:11 UTC**. `ActiveState=active`, `NRestarts=0`, **0** errors. Four boot gates green;
no `[POS-UNKNOWN]`, no `[BE-SL-*]`. **`openitems_guard.py` exit 0**, canon header now `999572a`.

### A correction to my own 00:50 report

That report wrote *"NULL in 7 of 92 rows"* and *"the only position in 92"*. **`virtual_positions`
holds 66 rows, with ids running to 92** — the ids have gaps. The counts themselves were right (7
NULL `original_sl_price`, 1 `partial_taken`); the denominator was not. Nothing else in that report
depends on it.

*(Unrelated: `/root/trades.db` is an empty file dated 2026-05-27. It pre-dates this session — I did
not create it and did not remove it. The live database is `/root/titan-bot/trades.db`.)*

---

## §6 — THE THROUGH-LINE

The 00:50 audit named the shape: **two quantities that are equal at one instant, then used as if
they stayed equal.** Both fixes here are that shape, and they fail in opposite directions.

- **G3** — `'5m'` and the stop's timeframe were the same string until `SL_ATR_TF` moved to `'1h'`.
  Nothing broke loudly; the branch simply kept fetching a number that used to be right. The fix is
  not "change 5m to 1h" — it is **to stop naming the timeframe here at all**, so the next move
  carries this code with it.
- **G2** — `report.net_pnl` and the row's `net_pnl` were the same number until a partial existed.
  The author corrected one and left three consumers reading the other. The fix is not to patch the
  object — it is **to put the correction where the number is made**, so there is no second copy to
  forget.

**Both were one-line-shaped defects with several-consumer blast radii, and in both cases the
narrow fix would have left the trap armed for the next change.**

---

*Applied and committed as `999572a`. No order was sent. Isolation enforced with a hard assert across
19 `DB_PATH` attributes; live `MAX(id)` still 92 and vpos 82 bit-for-bit unchanged.*
