# titan-adx-window-fix-APPLIED-1161802-live-plus-a-defect-in-my-own-patch

_2026-07-30 14:19 UTC_

---

# TITAN — ADX window fix **APPLIED AND LIVE** `1161802` · §2.4 window OPEN · one defect caught in my own patch

_2026-07-30 15:10 UTC · HEAD `1161802` · 🔴 LIVE, REAL MONEY · vpos 87 LONG open_

---

## DECISION LINE

**Applied, committed `1161802`, pushed, restarted deliberately at 14:10:59. The §2.4 window is now
OPEN and the exit prompt's inputs are FROZEN.** Every confirmation you listed is green.

🔴 **AND THE PRE-RESTART AUDIT FOUND A DEFECT IN MY OWN PATCH — fixed in the same commit, which is
why the diff is +441 and not the +404 you reviewed.** `sensor_events.init_db()` **has no caller
anywhere in the codebase.** My `recheck_events.adx_window` `ALTER` lived inside it, so it would never
have run; the first `log_recheck` would have raised `no such column`; and that module's own two-layer
try/except would have **swallowed it — losing every recheck evidence row, silently**, while the
journal printed a perfectly normal `RECHECK` line. **Same shape as §2.6: code that reads as armed and
is not.** Found by auditing the migration path before restarting rather than after.

**Your two additions are done:** the import-migrates-schema landmine is **§2.33** (documented, not
defused — your call recorded as yours); the open-position reachability proof is **§2.26c**, and it
required **correcting your framing on one point** — see below. Freeze scope is confirmed verbatim in
**§2.4-OP**. And the self-validating replay is now standing methodology in **§0**, not just a note
about this patch.

---

## 🔴 ONE CORRECTION TO YOUR ADDITION 2 — it is NOT only the NOTE

You asked me to confirm "the only live-path change reaching the open position is the additive NOTE in
the exit prompt." **That is not right, and the difference matters.** **Two** things reach vpos 87:

1. **The NOTE** — immediately, because its latest sampler row predates the fix (`adx_window` NULL).
2. 🔴 **The ADX FIGURES THEMSELVES**, from the first post-fix sampler row onward. `_tf_metrics_safe`
   is reached by the hourly smart-exit sampler for **any** open position, so `Now: ADX1h=…` becomes
   the converged reading and **the NOTE then disappears**, because the two sides finally match.

**That is the fix working, not a side effect** — but it means the patch changes an input the advisor
reads on a running position. And since `EXIT_ADVISOR_DRYRUN = False`, a different verdict on vpos 87 is
possible, and a `close` verdict closes it. **Direction of the change is toward LESS spurious
confidence in holding:** the advisor was being shown a fabricated ADX *rise* (13.5 → 22.3) and read it
as *"regime strengthened"* — a reason to hold a LONG. With the truth that support is gone. I would
rather say this out loud than let "only the NOTE" stand.

### What the patch genuinely CANNOT reach — traced, not asserted

| patch site | reaches open vpos 87? | why |
|---|---|---|
| `indicators.py` | **NO effect on any existing reader** | two hunks: the `typing` import, and a **pure insertion (+163/−0)**. `compute_tf_metrics`, `_fetch_ohlcv_cached`, `fetch_snapshot` are **byte-identical** — entry snapshot, optimizer and entry advisor see exactly what they saw |
| `execute_entry` (entry-ADX + INSERT) | **NO** | runs once, at entry |
| `_recheck_fetch_1h_metrics` · `_health_score` · `_run_recheck_tier` | 🔴 **NO — UNREACHABLE FOR LIFE** | `virtual_trader.py:2271-2273` skips the whole recheck block when `recheck_status IN ('done','tightened','closed_critical')`. vpos 87 is **`done`** (all three tiers ran: 12:05:30 / 12:06:24 / 12:10:28). **The corrected floor cannot fire retroactively**, and no diff hunk lands within ~200 lines of that guard |
| `sensor_events.log_recheck` | **NO** | only caller is `_run_recheck_tier`, unreachable above |
| stop price · breakeven · trail · LONG partial · emergency close | **NOT TOUCHED AT ALL** | no hunk in any of those paths |

⚠️ **Worth knowing about `_tier_from_status`, because it surprised me and I checked instead of
assuming:** `_tier_from_status('done')` returns **−1**, so `_recheck_tier_due(1e6, 'done')` returns
**300** — i.e. `done` is **not** terminal at the tier-arithmetic level. The terminality lives entirely
in the `if` at `virtual_trader.py:2271`. Executed proof:

```
status=done             tier_from_status= -1   due@10s=10    due@1e6s=300
status=t+300_ok         tier_from_status=300   due@10s=None  due@1e6s=None
```

**So the reachability claim rests on line 2271, not on the tier function** — and the patch does not
touch it. Had I leaned on `_recheck_tier_due` I would have had the right answer for the wrong reason.

**Nothing else in vpos 87's contract moves.** Same stop, same 1R, same breakeven level, same trail,
same partial.

---

## THE DEFECT IN MY OWN PATCH — §2.34

```
$ grep -rn "sensor_events" *.py | grep -v "^sensor_events.py"
breakeven_worker.py:41:import sensor_events
virtual_trader.py:35:import sensor_events
...
$ grep -n "init_db" sensor_events.py
94:def init_db():          <-- and that is the ONLY occurrence, anywhere
```

`recheck_events` and `adaptive_trail_events` exist because something created them once, long ago — so
the `CREATE TABLE IF NOT EXISTS` statements have never been needed since, and **nobody noticed the
migration door was shut.** Harmless while the schema never changed. Fatal, and silently so, the moment
that module gained an additive `ALTER`.

**Fixed in the same commit** with a one-shot `_ensure_schema()` at the top of **both** writers — the
pattern `post_exit_observatory._ensure_db()` already uses. Idempotent, once per process, cannot raise
into the caller. **Verified end-to-end against a COPY of `trades.db`:**

```
before: 0 adx_window column(s)
  -> log_recheck(...) called with AdxReading(13.83, 200, '1h') and a stored entry window of NULL
after : 1 adx_window column(s)
row written: {... 'adx_1h': 13.83, 'adx_window': 200, 'adx_delta': None, 'verdict': 'TIGHTEN',
              'health_score': -5, 'reasons_json': '[{"rule":"adx_below_floor","value":13.83,
              "points":-5,"window":200}]' ...}
```

`adx_1h = 13.83` is the **converged** value · `adx_window = 200` is **persisted** · `adx_delta = None`
is the guard **correctly refusing** a cross-window subtraction. **This also closes a hazard that
predates the ALTER:** if `trades.db` were ever recreated without those tables, every sensor write
would have failed the same silent way.

⚠️ **A consequence to expect, so it is not read as a fault:** the migration is now **lazy**, so
`recheck_events.adx_window` **does not exist on the live DB yet.** It is created the first time
`log_recheck` runs — and vpos 87 can never trigger a recheck (`recheck_status='done'`). **The column
appears on the NEXT position's T+10s recheck.** A query for it before then correctly errors with
`no such column`; that is the design.

---

## YOUR ADDITION 1 — THE LANDMINE, RECORDED AS §2.33

`virtual_trader.py` calls **`init_db()` at module scope (line 2641)** against
**`DB_PATH = '/root/titan-bot/trades.db'`, hardcoded.** So *merely importing the module* — no function
called, no intent to write — executes every `CREATE TABLE IF NOT EXISTS` and every additive
`ALTER TABLE` in it, against production.

**It fired today.** A scratch copy was imported to run a *guard truth table* — pure logic — and the
import added two columns to the live DB hours before the patch introducing them was approved. No harm
(additive nullable; every INSERT names its columns; nothing reads those tables positionally; service
active, `NRestarts=0`, zero errors; the open position read normally), and the approved patch then
adopted the columns, so nothing had to be undone.

🔴 **The hazard is general, and it is the shape of the work this project does constantly.** Every
forensic session imports `virtual_trader` (or `main`, which imports it) to read state or replay logic.
**Every one of those imports migrates the production schema, silently, before the analyst's first line
runs.**

**Mitigation for future scratch work, recorded in §2.33:** copy `trades.db` and repoint `DB_PATH`
**before** importing — or, simplest and what should have been done here, test pure logic against a
copy of the file rather than the module in place.

**NOT restructured, and §2.33 records that as your decision and your reasoning:** moving `init_db()`
out of module scope is a change to a live trading module for a non-trading reason, which is exactly
the class of change this project keeps paying for. **The landmine stays armed and documented.**

---

## STANDING METHODOLOGY — now in §0, not a footnote

> **VALIDATE THE REPLAY BEFORE YOU TRUST IT.** Before a replay is used to predict what a corrected
> rule *would* do, it must first reproduce what the rule **actually did**, from the stored inputs,
> exactly, row for row. Only then swap the corrected input in.

Here that was **38 of 38 `recheck_events` rows reproducing their stored `health_score`** before the
200-bar ADX was substituted. **§0 now also states why it is a rule rather than a nicety:** §4's items
3, 9 and 10 are three confident wrong numbers, and every one came from a re-derivation nobody checked
against the real thing first. A replay that cannot reproduce the past has no standing to predict the
future.

I also added a fifth entry to §0's filter table: **indicator WINDOW, not just algorithm** — the same
`compute_tf_metrics` on a different candle limit is not the same measurement.

---

## §2.4 — THE WINDOW IS OPEN, AND THE CLOCK IS RUNNING

Your freeze scope is recorded in **§2.4-OP** verbatim and marked settled:

> **FROZEN = everything the advisor READS.** **NOT frozen** = act/hold plumbing, logging, labels,
> close mechanics, and the entire entry side. *Fixing a close mechanic does not void the window;
> changing a number the advisor sees does.*

- **The window opened at `1161802`.** Applying the patch was the act that started it.
- From here, any change to a figure rendered into the close prompt requires **voiding and restating
  the window in OPEN-ITEMS, in the same commit as the prompt change.**
- A defect found during the window: **finish it and note the caveat. Never reset.**
- vpos 86 contributes **zero**. §2.4 stands at **0 of ~10**.

⚠️ **One honest wrinkle, flagged now rather than argued later: this very patch changed a number the
advisor reads** — the `Now: ADX1h` figure — on the same commit that opens the window. That is
coherent (the window opens *at* the fix, so the frozen state is the post-fix state, and vpos 87's
first post-fix consult will be the first reading under the frozen prompt), but it means **vpos 87
straddles the boundary**: its earlier consults were made on the fabricated ADX. If vpos 87 becomes a
§2.4 datapoint, that should be recorded against it.

---

## POST-RESTART VERIFICATION — EVERY ITEM YOU LISTED

**🔴 LIVE banner at $150 — verbatim:**
```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
[TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
```

**Four boot gates green:**
```
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 1 exchange position(s), 1 open row(s)
[RECONCILE] boot reconciliation starting
[RECONCILE] engine owns positions — NOT enqueueing a breakeven job for LONG (item 12a: single owner)
[RECONCILE] LONG open, SL present @ 64028.8 — kept.
[RECONCILE] done
```

**Runtime = commit by hash.** `git status` **clean**, HEAD **`1161802`**, origin in sync. Worker pid
319878 started **14:11:12.396**; **latest source mtime 14:09:52 — sources newer than worker start: 0.**

| file | sha256[:12] | vs the pre-restart run (11:39 report) |
|---|---|---|
| `main.py` | `fb4337c3ccc0` | **CHANGED** (was `903d90ffb312`) ✅ patched |
| `virtual_trader.py` | `efc10b0a4fe8` | **CHANGED** (was `1815c98dd2e9`) ✅ patched |
| `indicators.py` | `53e2913b8100` | new to the list ✅ patched |
| `sensor_events.py` | `3827ddd5e2c1` | new to the list ✅ patched |
| `config.py` | `0e1d3e9167c5` | **identical** ✅ untouched, as intended |
| `order_adapter.py` | `93dfcf32b6f8` | **identical** ✅ |
| `claude_advisor.py` | `85d26cc0518b` | **identical** ✅ |
| `breakeven_worker.py` | `87e39b3a2157` | **identical** ✅ |
| `close_report.py` | `d023a31ad8a5` | **identical** ✅ |
| `microstructure.py` | `5ebbf1a4578d` | **identical** ✅ |

**Exactly the four intended files moved; the six untouched ones are byte-identical to the run before
the restart** — including `config.py`, which matters because no flag changed.

**vpos 87 — SAME exchange stop order id across the restart, both probes:**

| | before restart | after restart (14:12) |
|---|---|---|
| position | LONG 0.0023 @ 64838.7, posId `2082799688088776706` | **identical** |
| stop order | `2082799690256592896` `STOP_MARKET stopPrice=64028.8 closePosition=true` | **identical, status NEW** |
| DB row | `87 open · stop_order_id 2082799690256592896 · recheck_status done` | **identical** |
| probes | unified `fetch_positions` + raw `swapV2PrivateGetUserPositions` | **both agree: 1 position, 1 order** |

**The stop was not cancelled and not re-placed.** Balance `free 479.87 · used 29.83 · total 509.70`.

**Errors / breaker / Mercury:**

| check | result |
|---|---|
| tracebacks · CRITICAL · `REFUSING TO START` · `no such column` · `OperationalError` since restart | **0** |
| `🚨` / `MANUAL ACTION REQUIRED` | **0** |
| circuit breaker | **untripped** (0 hits) |
| `NRestarts` | **0** |
| Mercury-SOL | **active, untouched** — up since 2026-07-21 06:39:33, `NRestarts=0` |

**Verification battery re-run on the LIVE tree after applying:**

| check | result |
|---|---|
| `py_compile` | **4/4 pass** |
| symtable FUNCTION-scope audit (the 29.07 guard) | **0 unresolved names across all 4 files** |
| applied tree vs the reviewed scratch tree | **md5 MATCH on all 4 files** — what shipped is what you read |
| patch applied by `patch -p2`, not by file copy | dry-run clean, then applied — the diff itself is what landed |
| `sensor_events` migration + `log_recheck` round-trip | verified on a **copy** of `trades.db` |

---

## 🔴 ONE CONFIRMATION IS TIME-GATED — `adx_window=200` HAS NOT LANDED YET

**This report is published now, with that item open, because the commit is pushed and a commit
without a delivered link is an unclosed task.** The remaining item is an observation, not a change.

**Neither of the two writers that stamp `adx_window` can fire on demand, and both just missed the
restart:**

| writer | why it cannot confirm sooner |
|---|---|
| `recheck_events` | 🔴 **can NEVER confirm on vpos 87.** `recheck_status='done'`, so the recheck block is unreachable for this position for life (§2.26c). And because the migration is now lazy, `recheck_events.adx_window` **does not yet exist as a column** — it is created the first time `log_recheck` runs. **This confirms on the NEXT position's T+10s recheck.** |
| `smart_exit_dryrun_samples` | hourly, and it fired at **14:05:30 — five minutes BEFORE the 14:10:59 restart**, so row 246 is still a pre-fix row (`adx_window` NULL, `adx_1h = 17.96` on the 42-bar window) |

**The arithmetic of the next fire, so the expected moment is checkable rather than vague:** the
throttle is `elapsed − MAX(elapsed_s) >= SMART_EXIT_DRYRUN_SAMPLE_SEC`, with
`MAX(elapsed_s) = 7212.7` and `opened_at = 12:05:17.4998`.

```
next fire  =  12:05:17.4998 + 7212.7 + 3600  =  15:05:30 UTC
```

**What will be appended:** that row's `adx_1h` / `adx_15m` / `adx_5m` with **`adx_window = 200`**, and
the same position's next exit consult (due `15:05:36`) showing the `Regime at ENTRY vs NOW` block with
**the NOTE gone** — because both sides will finally sit on the same window. The pre-fix contrast is
already on record for comparison:

| sampler row | UTC | ADX1h | ADX15m | ADX5m | `adx_window` |
|---|---|---:|---:|---:|---|
| 244 | 12:05:26 | 25.35 | 46.84 | 45.88 | NULL (pre-fix) |
| 245 | 13:05:31 | 22.30 | 49.56 | 48.66 | NULL (pre-fix) |
| 246 | 14:05:30 | 17.96 | 46.18 | 32.30 | NULL (pre-fix) |
| **247** | **15:05:30 (expected)** | **≈15** | **≈45** | **≈33** | **200** |

**Stated in advance so it cannot be presented later as anything other than what it is:** if the row
lands with `adx_window` NULL, the patch is not live on that path and it is a **regression to
investigate**, not a delay. A monitor is running against the live DB and will report either way.

---

## WHAT I DID NOT DO

- **Did not restructure `virtual_trader`'s module-scope `init_db()`** — your call, recorded as yours
  in §2.33. The landmine stays armed and documented.
- **Did not touch the observatory** — rows 79 and 80 are untouched, `on_entry`'s identity guard is
  unwritten, and both data decisions are still yours. Sequenced after the ADX fix, as you set it.
- **Did not backfill `entry_adx_1h_window`** on legacy rows. Their values genuinely were 200-bar, but
  asserting provenance from a code invariant is the habit that produced this defect, and the measured
  cost of refusing is **zero verdicts across all 38 rows**. vpos 87 therefore loses `adx_drop` — a
  rule that has never once fired.
- **Did not re-run any analysis** over the contaminated tables. §2.26b marks them; nothing was re-cut.
- **Did not change any flag.** `config.py` is byte-identical to the pre-restart run.

**Next, when you want it:** the observatory `on_entry` identity guard, then the two observatory data
decisions (row 80 → terminal status; row 79 → repair or retire). §2.28a says neither should be touched
before the guard exists, or the next id re-use recreates the same row.

---

## THE SHIPPED DIFF — `81875c9..1161802`, 4 files, **+441 / −40**

```diff
diff --git a/titan-bot/indicators.py b/titan-bot/indicators.py
index 2db82a8..77852d9 100755
--- a/titan-bot/indicators.py
+++ b/titan-bot/indicators.py
@@ -14,7 +14,7 @@ key at ``None`` so the row still records what we did manage to compute.
 import logging
 import time
 from threading import Lock
-from typing import Optional, Dict, List, Tuple
+from typing import NamedTuple, Optional, Dict, List, Tuple
 
 import pandas as pd
 import pandas_ta as ta
@@ -52,6 +52,163 @@ _CACHE_TTL_BY_TF: Dict[str, float] = {
 _cache_lock = Lock()
 _ohlcv_cache: Dict[Tuple[str, str], Tuple[float, List]] = {}
 
+# ---------------------------------------------------------------------------
+# 🔴 ADX PROVENANCE — ONE WINDOW FOR ONE INDICATOR (2026-07-30)
+#
+# ADX(14) is DOUBLY Wilder-smoothed (DX, then a second smoothing), so it
+# converges FAR more slowly than ATR(14), which is smoothed once. Measured on
+# live BTC 1h at a single instant:
+#
+#     limit= 42 -> 25.640      limit=150 -> 13.838
+#     limit= 60 -> 15.063      limit=200 -> 13.834   <- CANDLE_LIMIT: converged
+#     limit=100 -> 13.961      limit=300 -> 13.834
+#
+# The bot used to read ADX on TWO windows and render the difference as a CHANGE:
+# the entry snapshot on CANDLE_LIMIT (converged) and BOTH the post-entry recheck
+# and the smart-exit sampler on ATR_LEN*3 = 42 (not warmed up). Over 800 paired
+# readings on 1,000 real 1h candles the 42-bar figure ran +6.23 mean / +5.38
+# median HIGH, was high in 74.1% of cases, and made ADX_BELOW_FLOOR=20 miss
+# 52.9% of the states it exists to catch. The exit prompt printed
+# "At entry ADX1h=13.5 / Now ADX1h=25.4" — an 11.9-point rise across 25 seconds
+# that never happened — and the advisor read it as "regime strengthened".
+#
+# THE SENSITIVITY IS ADX'S ALONE, and this was checked rather than assumed. Over
+# the SAME two windows: ATR 314.434 vs 317.352 (-0.9%), `trend` identical,
+# ema_gap 0.3551 vs 0.3548. So ATR keeps its calibrated ATR_LEN*3 window
+# EVERYWHERE — the comment at virtual_trader.py:683 was written for ATR, it is
+# correct for ATR, and nothing here changes ATR's behaviour. Only `adx` moves.
+#
+# ADX_CANDLE_LIMIT is the ONE window an ADX may be read on. It is CANDLE_LIMIT by
+# IDENTITY, not by coincidence: `fetch_snapshot` has always used CANDLE_LIMIT
+# (verified: a single `+CANDLE_LIMIT = 200` in this file's entire git history and
+# no later change), so pinning to the same name makes the entry reference and
+# every later reading the same measurement BY CONSTRUCTION rather than by two
+# literals that happen to agree. If CANDLE_LIMIT is ever changed, every ADX
+# window already persisted stops matching and every comparison REFUSES instead of
+# silently mixing — which is the intended behaviour, not a regression.
+ADX_CANDLE_LIMIT = CANDLE_LIMIT
+
+# Sentinel for a persisted ADX whose window was never recorded. It matches NO
+# sanctioned window, so it is refused everywhere rather than guessed. -1 rather
+# than None so `window` is always an int and comparisons never raise.
+ADX_WINDOW_UNKNOWN = -1
+
+
+class AdxReading(NamedTuple):
+    """An ADX value THAT CARRIES THE WINDOW IT WAS COMPUTED ON.
+
+    🔴 THE GUARD, and it is deliberately the §2.19 shape. There, `source` was made
+    a REQUIRED POSITIONAL argument *and* was ANDed into the SQL WHERE clause: a
+    caller who had not thought about provenance could not write a working call, and
+    a WRONG provenance could not borrow another book's distribution — it got that
+    book's rows or none. The equivalent here:
+
+      * `value`, `window` and `tf` have NO defaults, so a reading cannot be
+        constructed without stating all three — the call-site half of the guard;
+      * `comparable_to` REFUSES across windows and timeframes, and the callers
+        return None (the rule SKIPS) rather than a number — so a foreign-window
+        ADX is UNUSABLE for a rule, not merely unlabelled;
+      * `usable_for_threshold` demands the sanctioned window, so an unconverged
+        reading cannot be tested against a fixed constant at all.
+
+    A bare float has no window and therefore cannot reach any of it. That is the
+    point: the defect this closes was a bare float from a 42-candle fetch being
+    compared with a bare float from a 200-candle fetch, with nothing in the code,
+    the DB or the prompt able to notice.
+    """
+    value: Optional[float]
+    window: int
+    tf: str
+
+    def usable_for_threshold(self) -> bool:
+        """True ONLY for a value on the one sanctioned window. Required by every
+        rule that tests an ADX against a FIXED constant (config.ADX_BELOW_FLOOR):
+        a floor calibrated on converged values means nothing against an
+        unconverged one."""
+        return self.value is not None and self.window == ADX_CANDLE_LIMIT
+
+    def comparable_to(self, other) -> bool:
+        """True ONLY when both readings are the SAME measurement — same window AND
+        same timeframe. Two different windows are not two observations of one
+        quantity, and their difference is not a change in the market."""
+        return (isinstance(other, AdxReading)
+                and self.value is not None and other.value is not None
+                and self.window == other.window and self.tf == other.tf)
+
+    def label(self) -> str:
+        """Render for a log line or a prompt. States the window whenever it is NOT
+        the sanctioned one, so an unusable figure is visibly unusable (§2.19: a
+        figure that cannot be ranked is rendered RAW with its provenance named)."""
+        if self.value is None:
+            return f"ADX{self.tf}=na"
+        if self.window == ADX_CANDLE_LIMIT:
+            return f"ADX{self.tf}={self.value:.1f}"
+        w = 'unrecorded' if self.window == ADX_WINDOW_UNKNOWN else f"{self.window}-candle"
+        return f"ADX{self.tf}={self.value:.1f} [{w} window]"
+
+
+def adx_delta(entry: 'AdxReading', current: 'AdxReading') -> Optional[float]:
+    """`entry - current`, and ONLY when the two are the same measurement.
+
+    Returns None across windows or timeframes — the caller's rule then SKIPS.
+    This is the half of the guard that cannot be bypassed by a careless call: the
+    old code did this subtraction on two bare floats from different fetches, which
+    is how a +11.9-point warm-up artefact became "ADX fell/rose"."""
+    if not isinstance(entry, AdxReading) or not entry.comparable_to(current):
+        return None
+    return entry.value - current.value
+
+
+def adx_reading(exchange, symbol: str, tf: str) -> AdxReading:
+    """THE ONLY SANCTIONED WAY TO READ AN ADX.
+
+    Routes through the SAME cached fetch at the SAME CANDLE_LIMIT the entry
+    snapshot uses, so the entry reference and every later reading are one
+    measurement rather than two literals that must be kept in step by hand. It
+    also inherits the per-TF OHLCV cache (`_CACHE_TTL_BY_TF`), which is why this
+    is cheaper than raising the literal at each call site: the T+10s recheck runs
+    ~13 s after the entry snapshot populated the 1h cache, so it reads the exact
+    bytes the entry read — same value, no extra request.
+
+    A failed fetch or compute returns value=None with the window STILL stated:
+    every rule skips a None, and nothing downstream can mistake it for a number."""
+    try:
+        ohlcv = _fetch_ohlcv_cached(exchange, symbol, tf, ADX_CANDLE_LIMIT)
+        v = (compute_tf_metrics(ohlcv) or {}).get('adx')
+    except Exception as e:
+        log.warning("adx_reading %s %s failed: %s", symbol, tf, e)
+        v = None
+    return AdxReading(v, ADX_CANDLE_LIMIT, tf)
+
+
+def adx_reading_from_stored(value, window, tf: str) -> AdxReading:
+    """Rehydrate a PERSISTED reading.
+
+    `window` is whatever the row recorded. NULL on every row written before the
+    window was persisted, and a NULL window is honestly UNKNOWN — it becomes
+    ADX_WINDOW_UNKNOWN, which matches no sanctioned window, so every comparison
+    and every threshold test involving it REFUSES.
+
+    🔴 LEGACY ROWS ARE NOT BACKFILLED, DELIBERATELY. Their `entry_adx_1h` really
+    was computed on CANDLE_LIMIT (fetch_snapshot is its only producer and that
+    literal never changed), so a backfill would be *correct* — and it would still
+    be a provenance value asserted from a code invariant rather than recorded at
+    write time, which is the habit that produced this defect. The cost of refusing
+    instead was measured, not assumed: across all 38 recheck_events rows ever
+    written, enabling or skipping the adx_drop rule changes ZERO verdicts, because
+    once both sides sit on the same window the entry-vs-now gap is fractions of a
+    point. Legacy rows lose a rule that has never fired; they do not get a guessed
+    window."""
+    try:
+        v = float(value) if value is not None else None
+    except (TypeError, ValueError):
+        v = None
+    try:
+        w = int(window)
+    except (TypeError, ValueError):
+        w = ADX_WINDOW_UNKNOWN
+    return AdxReading(v, w, tf)
+
 
 def _to_df(ohlcv):
     df = pd.DataFrame(
diff --git a/titan-bot/main.py b/titan-bot/main.py
index 3ec601b..6294be0 100644
--- a/titan-bot/main.py
+++ b/titan-bot/main.py
@@ -1315,11 +1315,21 @@ def _execute_entry(symbol, side, position_side, signal_row_id=None):
         # a snapshot price here).
         _snap = _request_snapshot() or {}
         _walls = microstructure.fetch_pre_trade_walls(exchange, symbol)
+        # 🔴 THE ENTRY ADX NOW TRAVELS WITH ITS WINDOW (2026-07-30). srv_adx_1h
+        # comes from indicators.fetch_snapshot, whose `limit` defaults to
+        # CANDLE_LIMIT == indicators.ADX_CANDLE_LIMIT — so the window is stated
+        # here from the same constant the producer used, not from a literal that
+        # would have to be kept in step by hand. This is the baseline the recheck
+        # compares against for the life of the position; sending it as a bare
+        # float is precisely how a 200-candle number came to be subtracted from a
+        # 42-candle one.
+        _entry_adx = indicators.AdxReading(_snap.get('srv_adx_1h'),
+                                           indicators.ADX_CANDLE_LIMIT, '1h')
         return virtual_trader.execute_entry(
             exchange, symbol, side, position_side,
             trades_entry_row_id=signal_row_id,
             pre_trade_walls=_walls,
-            entry_adx_1h=_snap.get('srv_adx_1h'),
+            entry_adx_1h=_entry_adx,
             # THE ONLY call site of execute_entry in the codebase. It is passed
             # explicitly rather than imported inside virtual_trader because
             # every other function in that module receives it the same way —
@@ -2673,13 +2683,42 @@ def _build_exit_context(vpos, symbol, side, exit_signal_name, trigger):
                                            f"4h={e['trend_4h']} 1h={e['trend_1h']} "
                                            f"ADX1h={e['srv_adx_1h'] or 0:.1f}")
             se = conn.execute("SELECT trend_15m_live,trend_5m_live,adx_1h,adx_15m,"
-                              "vol_ratio_1h,vol_ratio_15m,atr_change_pct "
+                              "adx_window,vol_ratio_1h,vol_ratio_15m,atr_change_pct "
                               "FROM smart_exit_dryrun_samples WHERE vpos_id=? "
                               "ORDER BY id DESC LIMIT 1", (vpos['id'],)).fetchone()
             if se:
+                # 🔴 THE PROMPT MAY NO LONGER IMPLY A CHANGE IT CANNOT SUPPORT
+                # (2026-07-30). This block renders directly under `At entry: ...
+                # ADX1h=<x>` beneath a heading that reads "Regime at ENTRY vs NOW",
+                # i.e. it asserts the two figures are two observations of one
+                # quantity. They were not: the entry side is srv_adx_1h on
+                # CANDLE_LIMIT and the sample side used to be ATR_LEN*3 = 42. On
+                # vpos 87 that printed a +11.9-point rise across 25 SECONDS which
+                # never happened, and the advisor duly reported "regime
+                # strengthened". Corrected samples now carry adx_window, so:
+                #   window == ADX_CANDLE_LIMIT -> same measurement, print it plainly;
+                #   anything else (incl. NULL on the 245 legacy rows) -> print the
+                #   figure RAW with its window named and say in words that no
+                #   rise or fall may be inferred.
+                # This is §2.19's precedent applied verbatim: a figure that cannot
+                # be compared is rendered with its provenance, not silently dropped
+                # and not silently used.
+                _sw = se['adx_window'] if 'adx_window' in se.keys() else None
+                _comparable = (_sw is not None
+                               and int(_sw) == indicators.ADX_CANDLE_LIMIT)
                 ctx['regime_now'] = (f"15m={se['trend_15m_live']} 5m={se['trend_5m_live']} "
                                      f"ADX1h={se['adx_1h'] or 0:.1f} "
                                      f"ADX15m={se['adx_15m'] or 0:.1f}")
+                if not _comparable:
+                    _wtxt = ('an unrecorded' if _sw is None else f"a {int(_sw)}-candle")
+                    ctx['regime_now'] += (
+                        f"\n  🔴 NOTE: the two ADX figures above were computed on "
+                        f"DIFFERENT candle windows — the 'At entry' value on "
+                        f"{indicators.ADX_CANDLE_LIMIT} candles and the 'Now' value on "
+                        f"{_wtxt} window. ADX(14) is doubly smoothed and reads far "
+                        f"higher on a short window, so these are NOT two observations "
+                        f"of one quantity: NO rise or fall between them may be "
+                        f"inferred. Judge the 'Now' figure on its own, or ignore it.")
                 ctx['volume_now'] = (f"vol_1h={se['vol_ratio_1h'] or 0:.2f} "
                                      f"vol_15m={se['vol_ratio_15m'] or 0:.2f} "
                                      f"ATR change vs entry={se['atr_change_pct'] or 0:+.1f}%")
diff --git a/titan-bot/sensor_events.py b/titan-bot/sensor_events.py
index a4b6bb9..e804aff 100644
--- a/titan-bot/sensor_events.py
+++ b/titan-bot/sensor_events.py
@@ -54,6 +54,7 @@ _RECHECK_SCHEMA = """
         entry_wall_mult REAL,
         wall_ratio REAL,
         adx_1h REAL,
+        adx_window INTEGER,
         adx_delta REAL,
         atr_pct_1h REAL,
         atr_delta_pct REAL,
@@ -95,12 +96,55 @@ def init_db():
     with sqlite3.connect(DB_PATH) as conn:
         conn.execute(_RECHECK_SCHEMA)
         conn.execute(_TRAIL_SCHEMA)
+        # 🔴 Additive migration (2026-07-30): the window every adx_1h below was
+        # computed on. NULL on the 38 legacy rows, all of which were written on
+        # the unconverged ATR_LEN*3 window — so any past analysis quoting
+        # recheck adx_1h or adx_delta is suspect and now says so in the data.
+        try:
+            conn.execute("ALTER TABLE recheck_events ADD COLUMN adx_window INTEGER")
+        except sqlite3.OperationalError:
+            pass  # column already exists
         conn.execute("CREATE INDEX IF NOT EXISTS ix_recheck_events_vpos "
                      "ON recheck_events(vpos_id)")
         conn.execute("CREATE INDEX IF NOT EXISTS ix_trail_events_vpos "
                      "ON adaptive_trail_events(vpos_id)")
 
 
+# 🔴 init_db() HAS NO CALLER ANYWHERE IN THIS CODEBASE (verified 2026-07-30 by
+# grep across every module: only its own `def`). The two tables exist because
+# something created them once, by hand, months ago — so the CREATEs have simply
+# never been needed since, and NOBODY NOTICED that the migration door was shut.
+#
+# That was harmless while the schema never changed. It stopped being harmless the
+# moment this module gained an additive ALTER (adx_window): the column would never
+# have been created, the first log_recheck INSERT would have raised "no such column",
+# and the two-layer try/except below would have SWALLOWED it — losing every recheck
+# evidence row silently, while the journal showed a perfectly normal recheck. Same
+# shape as §2.6: code that READS as armed and is not.
+#
+# Fixed by putting the migration where it actually runs — a one-shot at the top of
+# each public writer, the pattern post_exit_observatory already uses (_ensure_db).
+# It is idempotent (CREATE IF NOT EXISTS + guarded ALTER), it runs once per process,
+# and it CANNOT raise into the caller: init_db is wrapped, and every writer is
+# already inside its own try/except. This also closes a latent hazard that predates
+# the ALTER — if trades.db were ever recreated, recheck_events would not exist at
+# all and every write would have failed the same silent way.
+_schema_ready = False
+
+
+def _ensure_schema():
+    """Idempotent, once per process, never raises."""
+    global _schema_ready
+    if _schema_ready:
+        return
+    try:
+        init_db()
+    except Exception as e:
+        print(f"[TITAN][SENSOR-EVT] schema ensure failed (observational, ignored): {e}",
+              flush=True)
+    _schema_ready = True
+
+
 def _insert(table, row):
     cols = list(row.keys())
     with sqlite3.connect(DB_PATH) as conn:
@@ -121,15 +165,31 @@ def log_recheck(vpos_id, side, tier_sec, score, verdict, details,
     sl_after is None for OK/EMERGENCY (no tighten happened); the caller passes the
     real post-write value for TIGHTEN. Layer 1 of the guard lives here: this
     function NEVER raises, so a logging fault cannot abort a recheck or a stop move.
+
+    🔴 `adx_1h` and `entry_adx` are indicators.AdxReading, NOT floats (2026-07-30).
+    `adx_delta` is derived through indicators.adx_delta(), which REFUSES across
+    windows — so the stored delta can no longer be a cross-window subtraction
+    presented as a market move, which is what the 38 legacy rows contain. The
+    window itself is stored in the new adx_window column, because a number whose
+    provenance lives only in the code is a number that goes stale silently.
     """
     if not SENSOR_EVENT_LOGGING_ENABLED:
         return
+    _ensure_schema()
     try:
         ratio = (cur_wall_mult / entry_wall_mult
                  if (entry_wall_mult and entry_wall_mult > 0
                      and cur_wall_mult is not None) else None)
-        adx_delta = ((entry_adx - adx_1h)
-                     if (entry_adx is not None and adx_1h is not None) else None)
+        # Imported here, not at module scope: sensor_events is imported by both
+        # bots' engines and must stay import-light and side-effect-free.
+        import indicators
+        _cur = (adx_1h if isinstance(adx_1h, indicators.AdxReading)
+                else indicators.AdxReading(adx_1h, indicators.ADX_WINDOW_UNKNOWN, '1h'))
+        _ent = (entry_adx if isinstance(entry_adx, indicators.AdxReading)
+                else indicators.AdxReading(entry_adx, indicators.ADX_WINDOW_UNKNOWN, '1h'))
+        adx_value = _cur.value
+        adx_window = _cur.window
+        adx_delta = indicators.adx_delta(_ent, _cur)
         atr_delta = (((entry_atr_pct - atr_pct_1h) / entry_atr_pct * 100.0)
                      if (entry_atr_pct and entry_atr_pct > 0
                          and atr_pct_1h is not None) else None)
@@ -158,7 +218,8 @@ def log_recheck(vpos_id, side, tier_sec, score, verdict, details,
             'cur_wall_mult': cur_wall_mult,
             'entry_wall_mult': entry_wall_mult,
             'wall_ratio': None if ratio is None else round(ratio, 4),
-            'adx_1h': adx_1h,
+            'adx_1h': adx_value,
+            'adx_window': adx_window,
             'adx_delta': None if adx_delta is None else round(adx_delta, 3),
             'atr_pct_1h': atr_pct_1h,
             'atr_delta_pct': None if atr_delta is None else round(atr_delta, 3),
@@ -186,6 +247,7 @@ def log_adaptive_trail(vpos_id, side, source, entry_price, current_price,
     """
     if not SENSOR_EVENT_LOGGING_ENABLED:
         return
+    _ensure_schema()
     try:
         atr = (fresh_pct * entry_price / (100.0 * trail_mult)
                if (fresh_pct is not None and entry_price and trail_mult) else None)
diff --git a/titan-bot/virtual_trader.py b/titan-bot/virtual_trader.py
index 49cfb51..9e0a423 100755
--- a/titan-bot/virtual_trader.py
+++ b/titan-bot/virtual_trader.py
@@ -34,9 +34,18 @@ from adaptive_trail import true_atr_wilder as _true_atr
 import adaptive_trail
 import sensor_events
 # Post-entry recheck reuses the SAME order-book wall analysis as the live entry
-# gate (microstructure.fetch_pre_trade_walls) and the SAME 1h ADX/ATR computation
-# as the entry snapshot (indicators.compute_tf_metrics) — one 1h OHLCV fetch per
-# tier yields both metrics, so baselines and rechecks are measured identically.
+# gate (microstructure.fetch_pre_trade_walls) and the SAME 1h ADX/ATR ALGORITHMS
+# as the entry snapshot (indicators.compute_tf_metrics).
+# 🔴 CORRECTED 2026-07-30: "one 1h OHLCV fetch per tier yields both metrics, so
+# baselines and rechecks are measured identically" — the first half was true and
+# the SECOND HALF WAS FALSE, which is exactly how this went unnoticed. The same
+# ALGORITHM on a DIFFERENT WINDOW is not the same measurement: ADX(14) is doubly
+# Wilder-smoothed and read +6.23 mean high on the ATR_LEN*3 window this fetch
+# uses. ADX now comes from indicators.adx_reading() on the entry's own
+# CANDLE_LIMIT window and arrives carrying it; ATR still comes off the
+# ATR_LEN*3 fetch, because that is the window ITS entry baseline was calibrated
+# on. TWO fetches, deliberately — one window per indicator, each matching its
+# own baseline.
 import microstructure
 import indicators
 import liquidity_zones
@@ -301,6 +310,13 @@ def init_db():
                         # 'done', or terminal 'tightened' / 'closed_critical'.
                         "entry_wall_baseline_mult REAL",
                         "entry_adx_1h REAL",
+                        # 🔴 THE WINDOW THE ADX ABOVE WAS COMPUTED ON (2026-07-30).
+                        # A stored ADX without its window is exactly what let a
+                        # 42-candle reading be compared with a 200-candle one for
+                        # weeks. NULL on every legacy row and NOT backfilled — see
+                        # indicators.adx_reading_from_stored for why, and for the
+                        # measured cost of refusing (zero verdicts change).
+                        "entry_adx_1h_window INTEGER",
                         "entry_atr_pct_1h REAL",
                         # At-entry side-aware book snapshot (2026-07-04, diff #2).
                         # Observational — read by NO gate/exit; accumulates
@@ -408,6 +424,12 @@ def init_db():
                 "lux_volatility_entry TEXT",
                 # momentum
                 "adx_1h REAL", "adx_15m REAL", "adx_5m REAL",
+                # 🔴 the candle window all three ADX values above were computed on
+                # (2026-07-30). NULL on the 245 legacy rows, which were all written
+                # on the unconverged ATR_LEN*3 window — the exit prompt refuses to
+                # compare an ADX carrying a NULL/foreign window against the entry
+                # figure, and says so in words instead of implying a change.
+                "adx_window INTEGER",
                 "trend_15m_live TEXT", "trend_5m_live TEXT",
                 "mom_flip_15m INTEGER", "mom_flip_5m INTEGER",
                 "ema_gap_dir_1h_live TEXT",
@@ -646,7 +668,28 @@ def execute_entry(exchange, symbol, side, position_side,
     "acts correctly, stays quiet" instead of raising — the failure mode of
     2026-07-29, where the NAME itself was absent from this scope and the
     NameError fired while evaluating an argument, is what that default prevents.
+
+    🔴 `entry_adx_1h` IS EXPECTED TO BE AN indicators.AdxReading (2026-07-30), so
+    the window it was measured on is persisted alongside the value and the recheck
+    never has to assume. It DEGRADES rather than raises on a bare float: the value
+    is still stored and the window is recorded as UNKNOWN, so the adx_drop rule
+    refuses for that position instead of silently comparing across windows. Chosen
+    over raising deliberately — a TypeError here would stop the bot trading, and
+    "lose one rule on one position" is the cheaper failure. The normalisation runs
+    BEFORE any exchange call for the 2026-07-29 reason: nothing that can go wrong
+    with an argument should be able to go wrong after a fill.
     """
+    if isinstance(entry_adx_1h, indicators.AdxReading):
+        _entry_adx_val = entry_adx_1h.value
+        _entry_adx_window = entry_adx_1h.window
+    else:
+        _entry_adx_val = entry_adx_1h
+        _entry_adx_window = None
+        if entry_adx_1h is not None:
+            print(f"[VIRTUAL] ⚠️ entry_adx_1h arrived as a bare "
+                  f"{type(entry_adx_1h).__name__}, not an AdxReading — window "
+                  f"recorded as UNKNOWN, so the recheck's adx_drop rule will "
+                  f"refuse for this position. Fix the caller.", flush=True)
     # 🔴 UNSAFE-STATE BREAKER. Tripped only when an entry failsafe close FAILED,
     # i.e. a real position may exist that we could not unwind. Refuse to trade
     # until a human has looked; a restart clears it.
@@ -845,6 +888,9 @@ def execute_entry(exchange, symbol, side, position_side,
         _entry_n_ask = len(pre_trade_walls.get('walls_ask') or []) if pre_trade_walls else None
         _entry_atr_pct = (entry_atr_pct_1h if entry_atr_pct_1h is not None
                           else (atr_1h / fill_price * 100.0 if fill_price else None))
+        # entry_adx_1h_window: recorded, never derived. See the docstring — a
+        # bare float leaves this NULL and the recheck refuses rather than guesses.
+        _entry_adx_win = _entry_adx_window
 
         # step_margin_usdt / step_size columns are NOT NULL — repurposed here to
         # store the single-entry margin and size. pending_dca_limits now holds the
@@ -898,11 +944,12 @@ def execute_entry(exchange, symbol, side, position_side,
                     "pending_dca_limits, filled_legs, water_mark, status, "
                     "opened_at, trades_entry_row_id, "
                     "initial_risk_usdt, original_sl_price, max_adverse_price, "
-                    "entry_wall_baseline_mult, entry_adx_1h, entry_atr_pct_1h, "
+                    "entry_wall_baseline_mult, entry_adx_1h, "
+                    "entry_adx_1h_window, entry_atr_pct_1h, "
                     "entry_sup_wall_mult, entry_sup_wall_dist_pct, "
                     "entry_opp_wall_dist_pct, entry_ob_imbalance, "
                     "entry_n_walls_bid, entry_n_walls_ask, stop_order_id) "
-                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
+                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (
                         symbol, position_side, side, margin_required, amount, LEVERAGE,
                         fill_price, atr, sl_price, trail_pct,
@@ -912,7 +959,8 @@ def execute_entry(exchange, symbol, side, position_side,
                         # ORIGINAL ATR stop (sl_price here is pre-breakeven).
                         # max_adverse_price = MAE seed at entry price (mirror water_mark).
                         realized_risk_usdt, sl_price, fill_price,
-                        _entry_wall_mult, entry_adx_1h, _entry_atr_pct,
+                        _entry_wall_mult, _entry_adx_val, _entry_adx_win,
+                        _entry_atr_pct,
                         _entry_sup_mult, _entry_sup_dist,
                         _entry_opp_dist, _entry_ob_imb,
                         _entry_n_bid, _entry_n_ask,
@@ -1338,6 +1386,11 @@ def _health_score(position_side, entry_price, last,
     """Delta-based health score (<= 0). Each rule subtracts; missing inputs
     (None) skip their rule. Returns (score, [reason strings], [detail dicts]).
 
+    🔴 `entry_adx` and `cur_adx` are indicators.AdxReading, NOT floats (2026-07-30).
+    A bare float has no window and is refused by both ADX rules below — which is
+    the whole guard: this function used to accept two floats and subtract them
+    without either being able to say what it was measured on.
+
     `details` is a STRUCTURED mirror of `parts` (rule name, measured value, points
     contributed) for recheck_events.reasons_json — purely additive, it is written to
     the DB and read by nothing. `score` and `parts` are byte-identical to before, so
@@ -1364,17 +1417,50 @@ def _health_score(position_side, entry_price, last,
             details.append({'rule': 'wall_growth_warning', 'value': round(ratio, 4),
                             'threshold': WALL_GROWTH_WARNING,
                             'points': -WALL_GROWTH_WARNING_SCORE})
-    if entry_adx is not None and cur_adx is not None:
-        if (entry_adx - cur_adx) > ADX_DROP_THRESHOLD:
-            score -= 3
-            parts.append(f"ADX -{entry_adx - cur_adx:.1f} (-3)")
-            details.append({'rule': 'adx_drop', 'value': round(entry_adx - cur_adx, 3),
-                            'threshold': ADX_DROP_THRESHOLD, 'points': -3})
-        if cur_adx < ADX_BELOW_FLOOR:
-            score -= 5
-            parts.append(f"ADX {cur_adx:.1f}<{ADX_BELOW_FLOOR:.0f} (-5)")
-            details.append({'rule': 'adx_below_floor', 'value': round(cur_adx, 3),
-                            'threshold': ADX_BELOW_FLOOR, 'points': -5})
+    # 🔴 BOTH ADX RULES NOW DEMAND PROVENANCE (2026-07-30). `entry_adx` and
+    # `cur_adx` are indicators.AdxReading, not floats, and each rule asks the
+    # guard for permission rather than trusting that two numbers are comparable:
+    #
+    #   adx_drop        -> indicators.adx_delta(), which returns None across
+    #                      windows or timeframes. The rule then SKIPS. This
+    #                      subtraction used to run on two bare floats from a
+    #                      200-candle fetch and a 42-candle fetch, so a +6-point
+    #                      warm-up artefact was read as "ADX fell by 6 less than
+    #                      it did" — biasing the rule toward silence.
+    #   adx_below_floor -> usable_for_threshold(), which demands the sanctioned
+    #                      window. A floor calibrated on converged values means
+    #                      nothing against an unconverged reading, and testing it
+    #                      anyway is what made this rule miss 52.9% of the states
+    #                      it exists to catch.
+    #
+    # A skipped rule is recorded in `details` so a silent skip cannot be mistaken
+    # for a passed check — the 29.07 lesson: check what the gate SAYS, not only
+    # what it decides.
+    _drop = indicators.adx_delta(entry_adx, cur_adx)
+    if _drop is not None and _drop > ADX_DROP_THRESHOLD:
+        score -= 3
+        parts.append(f"ADX -{_drop:.1f} (-3)")
+        details.append({'rule': 'adx_drop', 'value': round(_drop, 3),
+                        'threshold': ADX_DROP_THRESHOLD, 'points': -3})
+    elif _drop is None and isinstance(cur_adx, indicators.AdxReading):
+        details.append({'rule': 'adx_drop', 'value': None, 'points': 0,
+                        'skipped': 'not comparable',
+                        'entry_window': getattr(entry_adx, 'window', None),
+                        'cur_window': cur_adx.window})
+    if isinstance(cur_adx, indicators.AdxReading):
+        if cur_adx.usable_for_threshold():
+            if cur_adx.value < ADX_BELOW_FLOOR:
+                score -= 5
+                parts.append(f"ADX {cur_adx.value:.1f}<{ADX_BELOW_FLOOR:.0f} (-5)")
+                details.append({'rule': 'adx_below_floor',
+                                'value': round(cur_adx.value, 3),
+                                'threshold': ADX_BELOW_FLOOR, 'points': -5,
+                                'window': cur_adx.window})
+        elif cur_adx.value is not None:
+            details.append({'rule': 'adx_below_floor', 'value': round(cur_adx.value, 3),
+                            'threshold': ADX_BELOW_FLOOR, 'points': 0,
+                            'skipped': 'window not sanctioned',
+                            'window': cur_adx.window})
     if entry_atr_pct and entry_atr_pct > 0 and cur_atr_pct is not None:
         if (entry_atr_pct - cur_atr_pct) / entry_atr_pct > ATR_DROP_PCT:
             score -= 3
@@ -1534,18 +1620,36 @@ def _set_recheck_status(vpos_id, status):
 
 
 def _recheck_fetch_1h_metrics(exchange, symbol, last):
-    """One 1h-OHLCV fetch -> (adx, atr_pct), via the SAME indicators path as the
-    entry snapshot (ADX_14 / ATR_14). Any failure -> (None, None) so a fetch
-    hiccup merely skips the ADX/ATR rules, never blocks the recheck."""
+    """1h metrics for the recheck -> (AdxReading, atr_pct).
+
+    🔴 TWO WINDOWS ON PURPOSE, AND THAT IS THE FIX (2026-07-30). This used to take
+    BOTH numbers off one ATR_LEN*3 = 42-candle fetch. ATR(14) is fine on 42 bars
+    (single Wilder smoothing; 314.4 vs 317.4 at 200 bars = -0.9%) AND that window
+    is the one the entry reference was calibrated on — `entry_atr_pct_1h` is
+    derived from execute_entry's own ATR_LEN*3 1h fetch, so moving ATR here would
+    break the atr_contraction rule by changing one side of its comparison. ATR
+    therefore stays EXACTLY where it was.
+
+    ADX(14) is NOT fine on 42 bars — it is doubly smoothed and had not warmed up,
+    running +6.23 mean high and making ADX_BELOW_FLOOR miss 52.9% of the states it
+    exists to catch. It now comes from indicators.adx_reading(), the one sanctioned
+    accessor, on the same CANDLE_LIMIT window as the entry snapshot, and it arrives
+    as an AdxReading carrying that window rather than as a bare float.
+
+    Cost: at T+10s this is usually FREE — the entry snapshot populated the 1h
+    OHLCV cache ~13 s earlier and the 1h TTL is 300 s, so the recheck reads the
+    same bytes the entry read. Any failure -> value=None (rules skip) or
+    atr_pct=None; never blocks the recheck."""
+    adx = indicators.adx_reading(exchange, symbol, '1h')
     try:
         ohlcv_1h = exchange.fetch_ohlcv(symbol, '1h', limit=ATR_LEN * 3)
         m = indicators.compute_tf_metrics(ohlcv_1h) or {}
         atr = m.get('atr')
         atr_pct = (atr / last * 100.0) if (atr is not None and last) else None
-        return m.get('adx'), atr_pct
     except Exception as e:
-        print(f"[VIRTUAL] recheck 1h metrics fetch failed [{symbol}]: {e}", flush=True)
-        return None, None
+        print(f"[VIRTUAL] recheck 1h ATR fetch failed [{symbol}]: {e}", flush=True)
+        atr_pct = None
+    return adx, atr_pct
 
 
 def _run_recheck_tier(exchange, row, last, tier, send_tg):
@@ -1563,7 +1667,12 @@ def _run_recheck_tier(exchange, row, last, tier, send_tg):
     cur_adx, cur_atr_pct = _recheck_fetch_1h_metrics(exchange, symbol, last)
 
     entry_wall_mult = row['entry_wall_baseline_mult'] if 'entry_wall_baseline_mult' in _rk else None
-    entry_adx = row['entry_adx_1h'] if 'entry_adx_1h' in _rk else None
+    # The entry ADX is rehydrated WITH the window the row recorded (NULL ->
+    # UNKNOWN -> adx_drop refuses). It is never re-derived and never assumed.
+    entry_adx = indicators.adx_reading_from_stored(
+        row['entry_adx_1h'] if 'entry_adx_1h' in _rk else None,
+        row['entry_adx_1h_window'] if 'entry_adx_1h_window' in _rk else None,
+        '1h')
     entry_atr_pct = row['entry_atr_pct_1h'] if 'entry_atr_pct_1h' in _rk else None
 
     score, parts, details = _health_score(
@@ -1573,10 +1682,15 @@ def _run_recheck_tier(exchange, row, last, tier, send_tg):
     verdict = _recheck_verdict(score)
     reasons = ", ".join(parts) if parts else "no negative deltas"
 
+    # The log line now prints the ADX's WINDOW alongside its value (via
+    # AdxReading.label(), which names the window whenever it is not the sanctioned
+    # one). The old line printed a bare number, which is why an 11.8-point
+    # divergence from the entry figure sat in the journal unremarked.
     print(f"[VIRTUAL] RECHECK vpos={vpos_id} {position_side} T+{tier}s "
           f"score={score} verdict={verdict} "
-          f"wall={cur_wall_mult}/{entry_wall_mult} adx={cur_adx} atr%={cur_atr_pct} "
-          f"| {reasons}", flush=True)
+          f"wall={cur_wall_mult}/{entry_wall_mult} "
+          f"adx={cur_adx.label()} (entry {entry_adx.label()}) "
+          f"atr%={cur_atr_pct} | {reasons}", flush=True)
 
     # Evidence row for EVERY tier run (OK included). sl_before is captured HERE,
     # before any branch can move the stop — that separation is the whole point:
@@ -1589,6 +1703,9 @@ def _run_recheck_tier(exchange, row, last, tier, send_tg):
                 verdict=verdict, details=details, entry_price=entry_price,
                 current_price=last, sl_before=_sl_before,
                 cur_wall_mult=cur_wall_mult, entry_wall_mult=entry_wall_mult,
+                # Readings, not floats: log_recheck derives adx_delta through the
+                # same guard, so the stored delta can no longer be a cross-window
+                # subtraction, and adx_window is persisted for every future cut.
                 adx_1h=cur_adx, entry_adx=entry_adx,
                 atr_pct_1h=cur_atr_pct, entry_atr_pct=entry_atr_pct)
 
@@ -1798,19 +1915,39 @@ def _record_excursion_sample(row, last, water_mark, mae):
 
 
 def _tf_metrics_safe(exchange, symbol, tf, last):
-    """One OHLCV fetch -> compute_tf_metrics dict (adx / atr_pct / vol_ratio /
-    trend / ema_gap_dir). Any failure -> {} so a hiccup merely blanks that TF's
-    fields; never raises, never touches the position."""
+    """Per-TF metrics for the smart-exit sampler -> compute_tf_metrics dict
+    (atr_pct / vol_ratio / trend / ema_gap_dir) with `adx` REPLACED by the
+    sanctioned converged reading and `adx_reading` / `adx_window` added.
+
+    🔴 SAME SPLIT AS THE RECHECK, AND FOR THE SAME REASONS (2026-07-30). The
+    ATR_LEN*3 fetch stays: `atr_pct` here is compared against
+    `entry_atr_pct_1h`, which execute_entry derives from its OWN ATR_LEN*3 1h
+    fetch, and vol_ratio / trend / ema_gap_dir were measured to be window-stable
+    (trend identical, ema_gap 0.3551 vs 0.3548 across 42 vs 200 bars). Only `adx`
+    was window-sensitive, and only `adx` moves — these three ADX values are what
+    the EXIT PROMPT prints as "Now: ADX1h=... ADX15m=...", directly under the
+    entry figure, and on the old window that pairing asserted changes that had not
+    happened.
+
+    Any failure -> {} for the TF's fields, or an AdxReading with value=None; never
+    raises, never touches the position."""
+    adx = indicators.adx_reading(exchange, symbol, tf)
     try:
         ohlcv = exchange.fetch_ohlcv(symbol, tf, limit=ATR_LEN * 3)
         m = indicators.compute_tf_metrics(ohlcv) or {}
         atr = m.get('atr')
         m['atr_pct'] = (atr / last * 100.0) if (atr is not None and last) else None
-        return m
     except Exception as e:
         print(f"[VIRTUAL] smart-exit {tf} metrics fetch failed [{symbol}]: {e}",
               flush=True)
-        return {}
+        m = {}
+    # The unconverged value from the 42-bar frame above is OVERWRITTEN, not
+    # merged: there must be exactly one `adx` in this dict and it must be the
+    # sanctioned one, so no downstream reader can pick up the old number.
+    m['adx'] = adx.value
+    m['adx_reading'] = adx
+    m['adx_window'] = adx.window
+    return m
 
 
 def _nearest_wall(walls, side_key, mid):
@@ -2034,9 +2171,14 @@ def _record_smart_exit_dryrun(exchange, row, last, water_mark):
             "atr_change_pct, lux_volatility_entry, adx_1h, adx_15m, adx_5m, "
             "trend_15m_live, trend_5m_live, mom_flip_15m, mom_flip_5m, "
             "ema_gap_dir_1h_live, data_ok, would_wall_sl, wall_route, actual_sl, "
-            "wall_sl_dist_pct, actual_sl_dist_pct, wall_sl_tighter, wall_sl_breached"
+            "wall_sl_dist_pct, actual_sl_dist_pct, wall_sl_tighter, wall_sl_breached, "
+            # 🔴 the window the three adx_* values were computed on. Written on
+            # every new row so the exit prompt can REFUSE a cross-window
+            # comparison instead of implying one, and so any future cut of this
+            # table can tell the corrected rows from the 245 legacy ones.
+            "adx_window"
             ") VALUES ("
-            "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
+            "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
             (row['id'], entry_id, symbol, side, entry_regime, entry_gap,
              round(elapsed, 1), last, round(fav_now_pct, 4), round(mfe_pct, 4),
              round(giveback_pct, 4), armed, would_exit,
@@ -2052,7 +2194,8 @@ def _record_smart_exit_dryrun(exchange, row, last, water_mark):
              m1h.get('ema_gap_dir'), data_ok,
              _r(would_wall_sl, 2), wall_route, _r(actual_sl, 2),
              _r(wall_sl_dist_pct, 4), _r(actual_sl_dist_pct, 4),
-             wall_sl_tighter, wall_sl_breached))
+             wall_sl_tighter, wall_sl_breached,
+             m1h.get('adx_window')))
 
     if first_fire:
         print(f"[SMART-EXIT-DRYRUN] would-exit {symbol} {side} "
```

---

*Titan · 2026-07-30 15:10 UTC · HEAD `1161802` · 🔴 LIVE · vpos 87 LONG open, stop 64028.8 unchanged · §2.4 window OPEN, exit-prompt inputs FROZEN · one time-gated confirmation pending at 15:05:30*
