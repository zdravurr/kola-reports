# TITAN — THE MFE TRACKER IS LIFTED OUT OF DEAD CODE, AND IT CAN NO LONGER MISTAKE A NETWORK GAP FOR A WATERMARK

**2026-08-05 21:50 UTC · 🔴 BOTH HUNKS APPLIED FROM FLAT · HEAD `7472729` → `7a4169b` · restarted 21:50:38 UTC**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
**0 open positions and 0 `exit_pending`** at application, re-checked before the restart.
**Mercury-SOL never opened.**

Parent: `2026-08-05-2055-titan-unrankable-book-warning-applied-mfe-tracker-costed.md`.

**Approved together, and that mattered:** the lift-out alone would have installed a measurement that
cannot distinguish a real watermark from a network gap, on a question whose entire point is a fine
comparison between two exit shapes.

⚠️ **AND THE RECORD SAYS SO PLAINLY: THIS IS NOT URGENT.** ~4 rows a month at the current close rate,
**0 closed positions exist on the current geometry**, and it will not answer anything this quarter. It
is built because the rows cannot start accumulating until it exists — the same reasoning as the
attribution rows an hour earlier, and approved on that basis and no other.

---

## HUNK A — REGISTERED WHERE EVERY CLOSE ARRIVES

The tracker's only caller was `main.py:3643`, inside **`_handle_liquidity_sweep()`** — a handler that
has never executed: **0 of 20,721 signals ever carried an EQH/EQL type.** So `mfe_tracking` was empty
and the four `mfe_*` columns on `trades` were NULL on every row. **It was never a broken measurement.
It was an unreachable one, for a reason that had nothing to do with it.**

`enqueue()` now fires from **`virtual_trader._do_close()`** — the single convergence point for every
close route. The exit route and whether the partial had already fired are recorded as the label,
because **that is the cut the question is actually about.**

## HUNK B — THE COVERAGE CONTRACT `skip_drift_samples` ALREADY HAD

Before: a failed ticker fetch left `new_mfe = prev_mfe` and moved on, so a window blind for most of
its hour finalised as `completed`, indistinguishable from a fully-sampled one.

Now `polls_ok` / `polls_missed` are counted per tick and a thin window finalises `degraded=1`. **The
watermark still carries forward on a miss — an MFE is a running maximum, so that IS the correct
behaviour — but the miss is on the record.** A parity fix, not an invention.

### `MFE_MIN_POLLS_FOR_CLEAN` — NAMED, AND EXPRESSED FROM WHAT IT DEPENDS ON

```python
MFE_MIN_POLLS_FOR_CLEAN = (MFE_WINDOW_MINUTES * 60 // MFE_TICK_SECS) * 2 // 3
```

**= 80 of 120 possible polls** (60-minute window ÷ 30-second tick). 🔴 **It is derived, not
hard-coded, so changing the window or the cadence cannot silently invalidate the floor** — the defect
class where a threshold outlives the thing it was calibrated against. **Two thirds is deliberately
permissive:** an MFE is a running maximum and tolerates gaps far better than a point sample, so the
goal is to catch a window that was **mostly blind** (a Tor stall, a long API outage), not one that
blinked. **A row below the floor is KEPT with its numbers — it is marked, not discarded.**

---

## 🔴 PROVEN BY EXECUTION — ISOLATED DB COPY, EVERY MODULE'S `DB_PATH` PATCHED

Per the 2026-08-04 isolation lesson, that patching one module's path is not enough.

### 1. MIGRATION RAN ON A TABLE THAT ALREADY EXISTED

Columns added by **`ALTER`**, not only in the `CREATE` — `CREATE TABLE IF NOT EXISTS` would have
skipped them forever on the existing (empty) production table. **That is the migration-never-runs
shape recorded for `sensor_events`, avoided deliberately.**

```
1) MIGRATION — coverage columns present: True
   MFE_MIN_POLLS_FOR_CLEAN = 80 (= 60*60//30 * 2//3)
```

✅ **And confirmed on the LIVE database after restart:** `['polls_ok', 'polls_missed', 'degraded']`.

### 2. EVERY CLOSE ROUTE WRITES A ROW

```
external             row=WRITTEN  label=vclose:external:partial        status=active
sl                   row=WRITTEN  label=vclose:sl                      status=active
trail                row=WRITTEN  label=vclose:trail:partial           status=active
ai_exit              row=WRITTEN  label=vclose:ai_exit                 status=active
recheck_emergency    row=WRITTEN  label=vclose:recheck_emergency:partial status=active
passive_fill         row=WRITTEN  label=vclose:passive_fill            status=active
```

**All six routes named in the approval — external, poller SL, trail, ai_exit, recheck emergency,
passive exchange fill — reach the enqueue, each carrying its own route label.**

### 3. A FAILED FETCH IS COUNTED, NOT ASSUMED AWAY

```
MFE ticker fetch BTC/USDT:USDT failed: simulated Tor stall
   before: ok=0 missed=0 mfe=None
   after : ok=0 missed=1 mfe=None
   -> polls_missed incremented: True
   -> polls_ok NOT incremented: True
a SUCCESSFUL fetch increments polls_ok:
   after : ok=1 missed=1 mfe=64500.0  -> ok incremented: True
```

### 4. A THIN WINDOW IS DISTINGUISHABLE FROM A CLEAN ONE

```
MFE_COMPLETED trade_id=21690 … polls_ok=4  polls_missed=1 degraded=1 (below floor 80)
MFE_COMPLETED trade_id=21691 … polls_ok=86 polls_missed=1 degraded=0

   THIN  (polls_ok=4)    status=completed  degraded=1
   CLEAN (polls_ok=86)   status=completed  degraded=0
   -> distinguishable: True
```

### 5. NO NETWORK ON THE TRADING PATH

Proven with an exchange stub whose `fetch_ticker` **raises `AssertionError` if called at all**:

```
_poll_once on empty queue returned: 0  (no exception => no fetch attempted)
```

**`enqueue` itself is one local `INSERT`.** The polling happens on `mfe_tracker`'s own worker thread,
which already existed and — unlike `breakeven_worker` — carries nothing else (verified: it imports
only `sqlite3`, `threading`, `time`, `datetime`).

### 6. A MEASUREMENT CAN NEVER TOUCH A CLOSE

The wrapped block was executed against a tracker whose `enqueue` raises:

```
[MFE] enqueue failed (close unaffected): simulated tracker failure
close path continued after tracker failure: True
exception escaped: False
```

---

## 🔴 EQH/EQL STAYS DEAD TWICE OVER, INDEPENDENTLY

| guarantee | state |
|---|---|
| 1. the flag | `EQH_EQL_SMART_TP_ENABLED = False` |
| 2. the trigger | **0** signals in 20,721 rows ever carried an `EQ` type; `status='liquidity_sweep'` = **0** rows |
| `mfe_tracker` imports `liquidity_sweep`? | **No** |
| does the diff touch the handler or the flag? | **No** — both names appear in **comments only**; verified by grepping the diff for non-comment lines (`none`) |

**Reviving the measurement did not revive the strategy. Either guarantee alone keeps the smart-TP
dead, and §2.6's −971 simulated stands as the reason revival is refused.**

---

## VERIFICATION LEDGER

| check | result |
|---|---|
| `ast.parse` + `py_compile`, both files | ✅ |
| enqueue on all six close routes | ✅ proven by execution |
| failed fetch → `polls_missed`, not a silent hold | ✅ |
| thin window → `degraded=1`, clean → `degraded=0` | ✅ |
| `MFE_MIN_POLLS_FOR_CLEAN` named + derived + reasoned in comment | ✅ 80 of 120 |
| close path unaffected when enqueue throws | ✅ proven by execution |
| no network call on the trading path | ✅ proven with a raising stub |
| live migration after restart | ✅ all three columns present |
| gates / geometry / prompts / sizing | **none touched** — grep of non-comment additions returns nothing |
| files changed | **2** (`virtual_trader.py` +48, `mfe_tracker.py` +76/−3) |
| restart | active **21:50:38 UTC**, boot reconciliation agrees (0 exchange, 0 open rows) |
| order mode | 🔴 **LIVE REAL MONEY**, $30 × 5 — unchanged |

**Untouched:** EMA envelope gate · HTF cascade · FLAT floor · Variant-B · score bars · risk thresholds
· geometry (SL 2.25 / trail 0.75R) · both prompts · `config.py`.
**Snapshot:** `/root/backups/mfe-lift-20260805-2105/` (all 38 `.py`). **Revert:** `git revert 7a4169b`.

---

## 🔴 WRITTEN INTO THE CANON — "SILENCE IS NOT A FAULT"

**New `§0.0` inserted at the top of `reports/OPEN-ITEMS.md`**, above the LIVE banner, so a session
reading *"Read this before touching Titan"* hits it before it can start diagnosing. 43 insertions, 0
deletions.

It records: the bot can be fully alive and consult the entry advisor **zero** times for hours; the
ingestion path stayed alive throughout (`confirm_recorded` 20:45:05, `context_recorded` 20:20:04, and
since then `htf_blocked` 21:50:02, `context_recorded` 21:30:03); and **what does not happen in that
state is a 5m trigger COMPLETING 3-WAY CONFLUENCE — the only event that consults the entry advisor.**

It also gives the three one-line queries that separate silence from breakage:

| question | benign answer |
|---|---|
| is ingestion alive? | recent `confirm_recorded` / `context_recorded` rows |
| are the observatories ticking? | `MAX(sampled_at)` current, or next `due_at` in the future |
| has the advisor been asked? | **may legitimately be hours old** |

**If the first two are current and only the third is stale, nothing is broken — and restarting does
not help. Four restarts on 2026-08-05 changed nothing and each reset the clock on every pending live
confirmation.**

⚠️ **AND THE §0.0 NOTE FLAGS THAT THE CANON IS STALE.** `OPEN-ITEMS.md`'s own header still reads HEAD
`44731be`; actual HEAD is **`7a4169b`**, seven commits later. The 30.07 fork is still open and the
dated `*-open-items.md` snapshots remain the live truth for everything except `§0.0`. **I did not
silently update the header — that would paper over the fork rather than record it.**

---

## 3. ⏳ THE ITEM OPEN SINCE 19:15 — SIXTH REPORT, AND NOW IT IS DOCUMENTED RATHER THAN JUST REPEATED

**Still no stored prompt with per-wall percentiles.** Last consultation of any kind
**16:40:10 UTC**; **0** across five restarts now (19:08, 19:38, 20:31, 20:54, 21:50). Ingestion
current as of 21:50:02.

**This is the last report in which it will read as an open anomaly.** The cause is named, the
distinguishing queries are in the canon, and the honest status of every prompt change made today —
the 18:55 wall percentile, the 19:38 prompt fixes, the 20:54 unrankable-book warning — is: **verified
by execution through the real code path, not yet witnessed in a stored prompt, and waiting on
confluence rather than on a fix.**

---

## LIVE STATE

| | |
|---|---|
| HEAD / `git status` | **`7a4169b`** / **clean** |
| open positions | **0** |
| `mfe_tracking` rows | **0** — the first will appear on the next close |
| service | active since **21:50:38 UTC** |
| `EQH_EQL_SMART_TP_ENABLED` / `AI_ADVISOR_HIDE_1H` / `EXIT_ADVISOR_DRYRUN` | `False` / `False` / `False` |
