# mercury-sol-bear-daily-long-gate-armed-and-loaded

_2026-09-23 15:20 UTC_

---

# BEAR-DAILY LONG GATE — **ARMED AND LOADED**, restarted from FLAT

**2026-09-23 15:20 UTC · Mercury-SOL · APPLIED · Titan untouched · COHORT BOUNDARY 2026-09-23 15:12:43 UTC**

`openitems_guard` → **exit 0** before and **exit 0** after (titan-bot HEAD `f53d048`).

---

## 🔴 RESULT

**A LONG is now refused when the daily trend is BEAR. NEUTRAL still passes on both sides.** The gate is the
mirror of the 2026-09-17 bull-daily short gate. It sits at the same site, has the same shape, and is shipped
ARMED (`BEAR_DAILY_LONG_BLOCK_ENABLED=True`, `_DRYRUN=False`).

| | |
|---|---|
| book at start | **FLAT.** #50 (the LONG that stopped the 01:56 pass) **closed 14:11:17 UTC on its stop**: fill 117.82 → 114.75, −$2.65, **−1.092R**, daily=bull |
| restart | issued **15:12:30.005 UTC** from flat, rc=0. Up **15:12:43**. PID 3077029 → **214356** (worker **214481**), `NRestarts=0` |
| loaded-bytecode check | new flags present, **every protected value identical**, all 7 advisor prompts sha256-identical |
| AST walker | **9 of 9 statuses registered AND called**, 0 failures |
| fail-open | **27 of 27 error paths ADMIT**. The gate refuses in 4 of 4 real-`bear` cases |
| orders placed / cancelled | **0 / 0** |
| Titan | **UNTOUCHED** (PID 4007821, `NRestarts=0`, up since 2026-09-21 19:03:51, same before and after) |

**🔴 The evidence is thin, and I am not dressing it up.** Measured as a candidate on 2026-09-22, this rule failed
**0 of 5 controls**:
* n=3 on paper
* Bonferroni p=0.857
* the ranking flips between the two chronological halves
* the live bear-long cell is **EMPTY**, so the independent sample cannot be run
* the daily label and the era are collinear

🔴 **IT REFUSES A WINNER: paper #21, +0.285R, trail exit.** It is applied as **discipline**, on the same footing as
the order-book gate (08-10), the flat-ADX gate (08-17) and its own twin (09-17).

**For the 100× LONG question:** the gate is now live. A LONG into a bear daily, the population the live book has
never traded, is now refused at any size. That was the stated precondition for raising LONG size. **It is the
only precondition this pass met.** The 09-22 report (§4e) found other issues at $10,000:
* the 5%-of-equity daily breaker trips on a single ordinary stop-out
* the "$100 notional" alert text would understate exposure 100×
* the open card would print $20 for a $2,000 position

Those are unchanged.

---

## ⚠️ ONE CORRECTION TO THE BRIEF

The brief says the rejected stricter form ("LONG only when bull") refuses *"four known winners (live #47 and #49 at
+2.117R combined, paper #7 at +2.089R, paper #21 at +0.285R)"*. **The DB disagrees:**

| # | book | daily at entry | R | refused by "LONG only when bull"? |
|---|---|---|---|---|
| 47 | live | neutral | **−1.069 (loser)** | yes, but it is not a winner |
| 49 | live | **bull** | +1.856 | **no** (bull passes) |
| **29** | live | neutral | **+1.355** | yes |
| **30** | live | neutral | **+0.762** | yes |
| **48** | live | neutral | **+5.431 (the live book's best trade)** | yes |
| 7 | paper | neutral | +2.089 | yes |
| 21 | paper | bear | +0.285 | yes |

The +2.117R combined figure is **#29 + #30**. The rejected form refuses **five** winners, including **#48 at +5.431R**.
That makes the rejection stronger, not weaker. The DB figures are what went into config and canon.

---

## 1. THE RULE, AS APPLIED

**a) Rule.** Refuse a LONG entry when `trend_1d == 'bear'` at decision time. Nothing else changes:
* `bull` and `neutral` pass
* SHORT is untouched
* 4h is untouched

**b) Site.** In `main.py`, **immediately after the twin's block** and immediately before `# Execute single-entry
order`. That is the last gate before the order goes out, after the advisor verdict falls through.
`_bear_daily_long_halt(requested_side, snap)` mirrors `_bull_daily_short_halt` line for line:
* the kill switch is checked first
* the side scope is LONG only
* `snap.get` is guarded in a `try`
* a non-string label is ADMITTED
* the label is compared as `strip().lower()` against the literal `'bear'`
* the DRYRUN branch logs and admits
* it returns `(halted, reason, label)`

The refusal block copies the twin's shape:
* `update_trade(status='bear_daily_blocked', error=reason)`
* `_record_skip_attribution(..., 'bear_daily_blocked', trend_4h=…, trend_1d=label)`
* a Telegram card
* a log line
* a JSON 200 return

**c) Fail-open, proven by execution.** The function was extracted from the patched source by AST and executed
over 27 cases. **All 27 ADMIT:**
* missing key, `None`, `''`, `'   '`
* `'bearish'`, `'bear market'`, `'b ear'`
* int 0, int −1, NaN, list, dict, bytes, datetime
* `snap=None`, a snap with no `.get`, a `.get()` that raises RuntimeError, a `.get()` that raises KeyError, a str snap
* `'neutral'`, `'bull'`
* SHORT+bear, SHORT+bull, side `None`, side `'long'` (lowercase)
* kill switch off, DRYRUN on

**4 of 4 refuse** with side `LONG` and label `'bear'`, `'BEAR'`, `' Bear '` or `'bear\n'`.
**The one path the type checks cannot see is a stale label, and it cannot reach the gate.** The daily candles come
from a cache (`indicators._fetch_ohlcv_cached`, TTL 3600 s) that is either fresh or refetched. A failed refetch is
caught in `fetch_snapshot`, which leaves `trend_1d=None`, and that ADMITS. Fewer than 30 candles also yields
`None`. No label older than the 1 h TTL can reach the gate. That matches the twin.

**d) Flags.**
* `BEAR_DAILY_LONG_BLOCK_ENABLED = True`: kill switch.
* `BEAR_DAILY_LONG_BLOCK_DRYRUN = False`: ARMED.

Both sit directly below the twin's flags in `config.py`. It ships armed because a dryrun at this firing rate would
produce its first observation in months, and a bug in the gate can only admit, never refuse.

**e) Status and attribution, verified by AST walk, not grep.** Every literal status passed to
`_record_skip_attribution` in `main.py` was checked against `TRACKED_STATUSES`:
```
✅ ai_skipped (5381)        ✅ below_threshold (4768)   ✅ htf_blocked (4243)
✅ risk_halt (4846)         ✅ book_blocked (5119)      ✅ flat_adx_blocked (5035)
✅ bull_daily_blocked (5430) ✅ entry_gate_refused (4823) ✅ bear_daily_blocked (5466)
update_trade(status='bear_daily_blocked') at 5458 · WALKER failures: 0
```

**f) Card on refusal:**
```
📉 BEAR DAILY REFUSED LONG
💎 SOL/USDT:USDT @ <price>
daily trend = BEAR — a long here is against the daily
<tf line>
<combo>
```

**g) Config comment.** It is in `config.py` verbatim, in the dictated shape. It is followed by the pre-registration,
the rejection record and the site note. Full text is in the diff (§6).

---

## 2. WHAT IT WOULD HAVE DONE — both books, never pooled

Source: `virtual_positions` joined to `trades` on `trades_entry_row_id`, reading the stored `trend_1d` at entry.
The DB was read-only (`mode=ro`, `query_only=1` asserted).

**PAPER: refuses 3 of 9 longs.** These are exactly the expected three.

| # | opened | fill | exit | R | daily |
|---|---|---|---|---|---|
| 12 | 2026-06-24 02:25 | 69.55 | sl | −1.049 | bear |
| **21** | 2026-07-19 06:50 | 76.05 | **trail** | **+0.285 🔴 WINNER** | bear |
| 26 | 2026-08-02 05:00 | 73.53 | sl | −1.085 | bear |

Paper LONG ΣR goes from −4.046 (n=9) to −2.197 (n=6).

**LIVE: refuses 0 of 12 longs.** Daily at entry: 9 bull, 3 neutral, 0 bear. Live LONG ΣR is **+18.648** on 12
closed trades (9 wins), unchanged. This now includes #50 at −1.092R.

**SHORTs: 0 of 23 touched** (paper 13, live 10).

**🔴 Restated, not buried: this gate refuses paper #21, a winner (+0.285R, trail exit, MFE +1.44R).**

**c) Live-era LONG consultations carrying `trend_1d == 'bear'`: ZERO.** This matches the 09-22 finding, so nothing
outranks the rest.
* `trades`, live era (≥ 2026-08-08): buy/bull 473, buy/neutral 355, buy/unlabelled 3,864, **buy/bear 0**.
* `skip_attribution`, live era: LONG/bull 1,525, LONG/neutral 664, LONG/unlabelled 2,188, **LONG/bear 0**.
* The last bear row anywhere is `trades` 2026-08-07 05:55 and `skip_attribution` 2026-08-07 19:05. Both are
  paper-era; the first live position opened 2026-08-08 08:50. Every row since 2026-09-22 is bull or unlabelled.

**d) Pre-registration.** It mirrors the twin's >50%-of-executable-shorts alarm.
* **Marginal rate: ~33% of EXECUTABLE longs while a bear-daily era lasts** (paper 3 of 9). Live: 0 of 12.
* **ALARM: >50% of EXECUTABLE longs.**
* **Condition rate: ~36%** (500 of 1,374 labelled paper-era long consultations carried a bear daily). That is
  **EXPECTED and is NOT the alarm**.
* 🔴 **No bear daily has closed since 2026-08-06. This gate may not fire for MONTHS.** Silence is expected and is
  not a fault.
* **Review at 10 `bear_daily_blocked` rows**, not at N days.

---

## 3. APPLIED FROM FLAT

**a) Flat, on all four legs, read twice.** First at 15:04, then again inside the restart script (venue 15:08:35,
DB one second before the restart):

| leg | result |
|---|---|
| `virtual_positions` not closed | **0** (44 closed) |
| `active_positions` | **0** |
| `exit_pending` | **0** |
| Bybit `/v5/position/list` SOLUSDT | idx 1 size **0**, idx 2 size **0**, both indices reported |
| Bybit open orders / conditional (stop) orders | **0 / 0** |
| **venue error list** | **EMPTY** (`[]`), and every read succeeded on attempt 1 |

Every venue read was a **GET on its own isolated Tor circuit**, using a random SOCKS username per attempt (for
example `2b6e34a4…`, `81f2634c…`, `b55fac8c…`). The restart script was built to **abort** unless all of this held.
It held.

**b) Backups first, then an AST proof of exactly what changed.**
`config.py`, `main.py`, `skip_attribution.py` and `OPEN-ITEMS-SOL.md` were each copied to
`*.bak_beardaily_20260923` before any edit. The `.bak` sha256 equals the pre-patch sha256.

| file | pre sha256 | post sha256 | AST change |
|---|---|---|---|
| `config.py` | `0585a82c…bee730` | `75394428…df44e2` | constants 141 → 143. **ADDED 2** (the two flags), **CHANGED 0, REMOVED 0** |
| `main.py` | `f355fdea…57e413` | `58f14eac…fd02dc` | defs 96 → 97, **ADDED `_bear_daily_long_halt`, REMOVED 0**. Changed: `_handle_5m_trigger` only. Stripping the inserted block leaves it **AST-identical to the .bak**. Module level: only the `from config import` gained the 2 names. **0 lines deleted.** |
| `skip_attribution.py` | `c5a669f5…1596b5` | `58b59687…68e1` | functions unchanged. Only `TRACKED_STATUSES` changed (+`bear_daily_blocked`) |
| `claude_advisor.py` | `52feade7…ec6c36` | **unchanged** | never opened for writing |

**Untouched at runtime, read from the LOADED bytecode.** The `.pyc` files are in `__pycache__`, compiled
15:07:19. Their header mtime and size match the source, and they predate the 15:12:43 process start.

| | | | |
|---|---|---|---|
| ✅ `SL_BUFFER_ATR` 2.5 | ✅ `TRAIL_MULT_ATR` 1.875 | ✅ `TRAIL_ARM_R` 0.75 | ✅ `CONFLUENCE_SCORE_THRESHOLD` 2.0 |
| ✅ `FLAT_ADX_GATE_DRYRUN` **True** | ✅ `BOOK_GATE_ENABLED` **True** | ✅ `BOOK_GATE_DRYRUN` **False** | ✅ `BULL_DAILY_SHORT_BLOCK_ENABLED` **True** |
| ✅ `BULL_DAILY_SHORT_BLOCK_DRYRUN` **False** | ✅ `EXIT_ADVISOR_DRYRUN` True | ✅ `MAX_POSITIONS_PER_SIDE` 1 | ✅ `LIVE_FIXED_MARGIN` **20** |
| ✅ `LEVERAGE` **5** | ✅ `PAPER_FIXED_MARGIN` 2000 | 🆕 `BEAR_DAILY_LONG_BLOCK_ENABLED` True | 🆕 `BEAR_DAILY_LONG_BLOCK_DRYRUN` False |

**Advisor system prompts: byte-identical by sha256, from the executed `claude_advisor` bytecode.** The brief says
six, but the module holds **seven** `_*SYSTEM*` strings. All seven were hashed:

| prompt | sha256 (before = after) |
|---|---|
| `_ENTRY_SYSTEM` | `cc70ed45…` ✅ |
| `_ENTRY_SYSTEM_V2` | `894a6c20…` ✅ |
| `_ENTRY_SYSTEM_V2_ALIGNED` | `f221365f…` ✅ |
| `_ENTRY_SYSTEM_V2_ALIGNED_SHORT` | `e1487999…` ✅ |
| `_CLOSE_SYSTEM` | `37bcdce4…` ✅ |
| `_CLOSE_STATE_SYSTEM` | `3be10726…` ✅ |
| `_LEARNING_SYSTEM` | `aa35142e…` ✅ |

**c) Restart from flat, and the loaded state.** The restart was timed mid-window, at minute 2:30 of a 5-minute
slot. Webhooks land at the boundary plus 0–15 s, so no consultation was cut. Boot:
```
15:12:30 systemd: Stopping mercury-sol.service …
15:12:43 systemd: Started mercury-sol.service
15:12:59 [SMART-CLEANUP] No open positions for SOL/USDT:USDT — proceeding with orphan cleanup
15:13:01 [AP] No active positions in DB — clean boot.
15:13:01 [BOOT] taker fee: 0.001 (0.1000%) source=venue
15:13:02 [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
15:13:02 [BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 214481]
15:13:06 [HEARTBEAT] alive ticks=1 cadence=10s open=0 mode=LIVE pid=214481
```
The orphan cleanup had nothing to cancel: open and conditional orders were 0 before and 0 after, and no cancel line
was logged.

Venue after (15:13:33): sizes 0/0, orders 0/0, errors `[]`. Position `updatedTime` is identical before and after on
both indices (`1790172670939`, `1789629064955`). `openitems_guard` after: **EXIT=0**.

**d) Canon.** `§BEAR-DAILY-LONG-GATE-2026-09-23` was written into `OPEN-ITEMS-SOL.md` directly after its twin. It
is a pure insertion (2211 → 2277 lines, 0 removed) and records:
* the discipline reasoning, verbatim
* the pre-registered rate and alarm, with the condition rate marked as expected
* the review point at **10 `bear_daily_blocked` rows**
* **COHORT BOUNDARY 2026-09-23 15:12:43 UTC**
* the replay
* the symmetry statement and the rejection record

---

## 4. WHAT IS NOW SYMMETRIC — AND WHAT IS NOT

* **Symmetric:** each side now refuses trading **against** the daily.
  * A SHORT is refused under a **bull** daily (since 2026-09-17).
  * A LONG is refused under a **bear** daily (since 2026-09-23).
* **Both sides still trade NEUTRAL.** This is by the operator's explicit decision.
* **Still NOT covered:** neither gate requires the daily to **agree**. A LONG under a neutral daily is admitted, and
  so is a SHORT under a neutral daily.
* 🔴 **Rejected, and recorded in config and canon so no later pass rediscovers it as a new idea:**
  * **"LONG only when bull"** was considered and rejected because it refuses known winners. Per the DB there are
    **five**: live #29 +1.355R, #30 +0.762R and #48 +5.431R, plus paper #7 +2.089R and #21 +0.285R.
  * The short-side analogue, **candidate 33 "SHORT only when bear"**, was measured on 2026-09-17 and died 0 of 5.
    It would have refused 10 of 10 live shorts.

---

## 5. CONFIRMATION

| | |
|---|---|
| every write stated before it ran | ✅ `.bak` ×4 → config → main (3 edits) → skip_attribution → restart → canon → this report |
| `.bak` taken | ✅ `*.bak_beardaily_20260923` ×4, sha256 = pre-patch |
| orders placed / cancelled | **0 / 0**. Venue access was GET only (`position/list`, `order/realtime`). Open orders were 0 before and after. |
| restarts | **exactly 1**, from flat, at 15:12:30.005 UTC |
| Titan | **UNTOUCHED**. Only `tools/openitems_guard.py` (read-only) was run: EXIT 0 before, EXIT 0 after |
| Mercury-SOL is not a git repo | recorded by sha256 + `.bak` + the diff below |

---

## 6. THE PATCH (unified diff against `*.bak_beardaily_20260923`)

```diff
--- a/config.py
+++ b/config.py
@@ -1386,3 +1386,36 @@
 # from _adv_snap, built at main.py:4529.
 BULL_DAILY_SHORT_BLOCK_ENABLED = True    # kill switch — False restores the pre-2026-09-17 path
 BULL_DAILY_SHORT_BLOCK_DRYRUN  = False   # 🔴 ARMED. This gate REFUSES ENTRIES.
+
+# ── 🔴 DO NOT LONG AGAINST A BEAR DAILY (2026-09-23) — the twin's mirror ──────
+#
+# this is DISCIPLINE, not a measured edge. Measured as a candidate on 2026-09-22
+# it failed 0 of 5 controls — n=3 on paper (1 win, ΣR −1.850), Bonferroni
+# p=0.857, the ranking flips between halves, the live bear-long cell is EMPTY so
+# the independent sample cannot be run, and it REFUSES A WINNER (paper #21,
+# +0.285R). It exists because a bot that longs into a falling daily trend is
+# doing something a trader would not do, and because the live book has never
+# traded that population at all. If a later pass measures it and finds no edge,
+# that is the EXPECTED result and NOT grounds to remove it. Grounds to remove it
+# are three and only three: it fires too often, it fires asymmetrically in a way
+# the rule does not explain, or it refuses trades a trader would take.
+#
+# PRE-REGISTERED MARGINAL RATE: ~33% of EXECUTABLE longs WHILE a bear daily era
+# lasts (3 of 9 on the paper book); 0% of the live book (0 of 12 — no live long
+# ever carried a bear daily). ALARM: >50% of EXECUTABLE longs. The ~36% CONDITION
+# rate (500 of 1,374 labelled paper-era long consultations carried a bear daily)
+# is EXPECTED and is NOT the alarm. 🔴 No bear daily has closed since 2026-08-06,
+# so this gate may not fire for MONTHS — silence is expected, not a fault.
+# REVIEW AT 10 `bear_daily_blocked` ROWS, not at N days.
+#
+# NEUTRAL passes on BOTH sides, by the operator's explicit decision. The stricter
+# form "LONG only when bull" was considered and REJECTED for refusing known
+# winners. Per the DB it refuses FIVE: live #29 +1.355R and #30 +0.762R (+2.117R
+# combined), live #48 +5.431R (NEUTRAL daily, the live book's best trade), paper
+# #7 +2.089R and paper #21 +0.285R. (The 2026-09-23 brief named them "#47 and #49"
+# and "four"; #47 is a −1.069R loser and #49 was BULL. The DB is right.)
+#
+# SITS beside its twin at main.py's post-advisor gate, NOT in the risk chain, for
+# the same reason: `trend_1d` does not exist at _risk_check time.
+BEAR_DAILY_LONG_BLOCK_ENABLED = True     # kill switch — False restores the pre-2026-09-23 path
+BEAR_DAILY_LONG_BLOCK_DRYRUN  = False    # 🔴 ARMED. This gate REFUSES ENTRIES.
--- a/main.py
+++ b/main.py
@@ -1188,6 +1188,8 @@
     ADX_BELOW_FLOOR,          # 🔴 THE threshold, shared with _health_score. ONE number.
     BULL_DAILY_SHORT_BLOCK_ENABLED,   # kill switch for the bull-daily short gate
     BULL_DAILY_SHORT_BLOCK_DRYRUN,    # False = ARMED, refuses entries
+    BEAR_DAILY_LONG_BLOCK_ENABLED,    # kill switch for the bear-daily long gate (twin's mirror)
+    BEAR_DAILY_LONG_BLOCK_DRYRUN,     # False = ARMED, refuses entries
     AI_SKIP_CARD_THROTTLE_S,  # 🔴 card throttle (2026-08-17) — notification only
     MAX_POSITION_DURATION_MINS,
     SPREAD_GATE_ENABLED,
@@ -2068,6 +2070,47 @@
               f"— ALLOWING through", flush=True)
         return False, 'DRYRUN would block — daily=bull', label
     return True, 'SHORT refused — daily trend is BULL', label
+
+
+def _bear_daily_long_halt(requested_side, snap):
+    """(halted, reason, label) — refuse a LONG when the DAILY trend is BEAR.
+
+    The MIRROR of _bull_daily_short_halt, line for line. NEUTRAL passes, exactly
+    as it does for the twin: this refuses trading AGAINST the daily, it does NOT
+    require the daily to agree.
+
+    🔴 DISCIPLINE, NOT A MEASURED EDGE. The reasoning lives verbatim in config.py
+    beside the flags; it is not repeated here so there is exactly ONE copy to
+    keep true.
+
+    🔴 FAIL-OPEN BY CONSTRUCTION. Every unknown, missing, stale, malformed or
+    unreadable label ADMITS the entry. A bug in this gate must never be able to
+    invent a refusal: the ONLY path to True is side=='LONG' AND a normalised
+    literal 'bear'. Proven by execution before it shipped over the twin's paths
+    — missing key, None, '', '   ', 'bearish', int/list/dict, snap=None, snap
+    with no .get, and a snap whose .get() RAISES all return False.
+
+    Called after the advisor verdict and before the order, beside its twin, for
+    the same reason: `trend_1d` does not exist at _risk_check time.
+    """
+    if not BEAR_DAILY_LONG_BLOCK_ENABLED:
+        return False, 'gate disabled (kill switch)', None
+    if requested_side != 'LONG':
+        return False, f'side={requested_side} — gate is LONG-only', None
+    try:
+        raw = snap.get('trend_1d') if hasattr(snap, 'get') else None
+    except Exception as _bd_err:
+        return False, f'ADMIT — snapshot unreadable ({type(_bd_err).__name__})', None
+    if not isinstance(raw, str):
+        return False, f'ADMIT — daily label absent/not-a-string ({type(raw).__name__})', None
+    label = raw.strip().lower()
+    if label != 'bear':
+        return False, f'ADMIT — daily={label!r} (not bear)', label
+    if BEAR_DAILY_LONG_BLOCK_DRYRUN:
+        print(f"{LOG_PREFIX}[BEAR-DAILY][DRYRUN] would refuse LONG (daily=bear) "
+              f"— ALLOWING through", flush=True)
+        return False, 'DRYRUN would block — daily=bear', label
+    return True, 'LONG refused — daily trend is BEAR', label
 def _risk_check(symbol, position_side):
     """Returns (ok: bool, reason: str). Blocks entries on streak/loss limits.
     FAIL-CLOSED (D1, Titan risk_manager parity): any risk-query error (positions fetch,
@@ -5407,6 +5450,42 @@
                             'trend_1d':  _bd_label,
                             'combo':     combo}), 200
 
+        # ── 🔴 DO NOT LONG AGAINST A BEAR DAILY (2026-09-23) — the twin's mirror ─
+        # Same site, same shape as the bull-daily short gate above. NEUTRAL passes.
+        # Discipline, not a measured edge. See config.py for WHY, verbatim.
+        _br_halt, _br_reason, _br_label = _bear_daily_long_halt(position_side, _adv_snap)
+        if _br_halt:
+            update_trade(row_id, status='bear_daily_blocked', combo_key=combo,
+                         confluence_score=direction_score,
+                         matrix_direction=matrix_result['direction'],
+                         matrix_breakdown_json=matrix_bkdn_json,
+                         error=_br_reason)
+            # Drift-tracked from the FIRST refusal — registered in
+            # skip_attribution.TRACKED_STATUSES in the SAME pass that shipped the
+            # gate, and the hook is CALLED here, not merely registered.
+            _record_skip_attribution(row_id, symbol, direction, 'bear_daily_blocked',
+                                     matrix_result=matrix_result,
+                                     confluence_score=direction_score,
+                                     pre_trade_walls=_pre_walls,
+                                     ai_reason=_br_reason,
+                                     srv_adx_1h=_adv_snap.get('srv_adx_1h'),
+                                     trend_4h=_adv_snap.get('trend_4h'),
+                                     trend_1d=_br_label)
+            send_tg(
+                f"\U0001F4C9 <b>BEAR DAILY REFUSED LONG</b>\n"
+                f"\U0001F48E {symbol} @ {_current_price:.2f}\n"
+                f"<i>daily trend = BEAR — a long here is against the daily</i>\n"
+                f"{_tf_line}\n"
+                f"<code>{combo}</code>"
+            )
+            print(f"{LOG_PREFIX}[BEAR-DAILY] REFUSED LONG {symbol} @ {_current_price:.2f} "
+                  f"daily={_br_label!r} row={row_id}", flush=True)
+            return jsonify({'status':    'bear_daily_blocked',
+                            'direction': direction,
+                            'reason':    _br_reason,
+                            'trend_1d':  _br_label,
+                            'combo':     combo}), 200
+
         # Execute single-entry order
         try:
             entry = _execute_single_entry(symbol, side, position_side, row_id=row_id,
--- a/skip_attribution.py
+++ b/skip_attribution.py
@@ -72,9 +72,12 @@
 # (trades=608, skip_attribution=0). That is the Titan FLAT-floor half-fix in mirror
 # image — hook called, status unregistered — and it is why this tuple is now
 # AST-checked against the call sites rather than eyeballed.
+# 🔴 'bear_daily_blocked' added 2026-09-23 WITH the bear-daily long gate (the
+# bull-daily short gate's mirror), same pass, same reason — registered here AND
+# called at the refusal site, verified by AST walk.
 TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked', 'risk_halt',
                     'book_blocked', 'flat_adx_blocked', 'bull_daily_blocked',
-                    'entry_gate_refused')
+                    'entry_gate_refused', 'bear_daily_blocked')
 
 # Drift sample offsets from the skip (label -> seconds). Same horizons as PEO.
 DRIFT_SLOTS = [('15m', 900), ('1h', 3600), ('4h', 14400),
```
