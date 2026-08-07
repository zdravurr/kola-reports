# SOL — STATE CHECK: the ADX-window fix is HALF-APPLIED. A session dropped at 21:22. STOPPED as ordered.

**2026-08-07 21:55 UTC** · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · **PAPER**
Parent: `2026-08-07-2050-sol-loss-streak-brake-ema-envelope-gate-not-applied-entry-exit-routing.md`

---

## VERDICT

**The tree is NOT untouched.** The brief expected `main.py` to still date from 2026-08-06 15:46:27.
It does not. **Three source files were rewritten TODAY between 21:09 and 21:20 UTC** by a session that
then died at ~21:22 — 28 minutes before this session started.

The stop rule fired. **I applied nothing and measured nothing. §1 and §2 were not started.**

The half-applied work is the §1 ADX-window fix itself — the same task in this brief. It is
**complete and internally coherent ON DISK**, but **unproven, undeployed, un-migrated and unrecorded.**

**Nothing is at risk right now**, for three independent reasons, all verified below: the book is
flat, the running process still holds the pre-edit code, and a restart self-heals the schema before
anything can write. A full `cp -p` rollback set exists.

---

## a) FILES CHANGED SINCE 2026-08-06 15:50

Everything below 21:00 is ordinary runtime churn (`trades.db`, `oi_cache.json`, `dynamic_weights.json`
from the 14:00 optimizer timer, `.env` 00:15, `prior_move_samples.jsonl` 00:19) plus the two edits
already on record from the 06.08 session (`claude_advisor.py` 16:05, `silence_digest_sol.py` 17:26).

**The three that should not be there:**

| file | mtime (UTC) | diffstat vs its `.bak` |
|---|---|---|
| `indicators.py` | **2026-08-07 21:09:11** | 1 removed / **170 added** |
| `virtual_trader.py` | **2026-08-07 21:19:02** | 33 removed / **139 added** |
| `main.py` | **2026-08-07 21:20:12** | 1 removed / **24 added** |

`__pycache__/indicators` and `__pycache__/virtual_trader` were regenerated at **21:21:47 / 21:21:49**
— i.e. the dropped session **imported the live tree**, not only an isolated copy. That import was
read-only with respect to the book (the DB is unmigrated and the book is unchanged, both shown below),
but it is worth naming: the isolated-copy discipline was not fully held.

### `.bak` set — rollback IS available

A complete `cp -p` backup set tagged `_adxwindow_20260807` exists. Because `cp -p` preserves mtimes,
each `.bak` mtime **is the pre-edit mtime** — which is how the pre-edit state is provable:

| backup | size | preserved mtime = pre-edit mtime |
|---|---|---|
| `main.py.bak_adxwindow_20260807` | 289 574 | 2026-08-06 15:46:27 ← **matches the brief exactly** |
| `virtual_trader.py.bak_adxwindow_20260807` | 112 164 | 2026-08-06 16:56:47 |
| `indicators.py.bak_adxwindow_20260807` | 14 316 | 2026-07-04 20:37:15 |
| `OPEN-ITEMS-SOL.md.bak_adxwindow_20260807` | 94 764 | 2026-08-06 16:59:24 |

Plus a 49.6 MB `trades.db.bak_adxwindow_20260807` in the dead session's scratchpad (21:06).

**`OPEN-ITEMS-SOL.md` is byte-identical to its own backup** (both 94 764 bytes, both mtime 16:59:24)
— the canon was never touched. That is finding **§1e = NOT DONE**, below.

---

## b) SERVICE

```
mercury-sol.service   active (running) since 2026-08-07 00:25:33 UTC  (21h)
  master 2854332 · worker 2854383 (started 00:25:50)
  NRestarts = 0
  tracebacks / OperationalError / "no such column" since boot:  0 matches
mercury-sol-optimizer-listener   active, NRestarts = 0, up since 2026-07-13
```

Healthy. Last log activity 21:00:06 (a 15m HyperWave webhook), 20:30 advisor SKIP on a SHORT.

---

## c) RUNTIME INVARIANTS — imported WITH `load_dotenv` FIRST

```
OBSERVATION_MODE        = True          ← PAPER. Untouched.
SL_BUFFER_ATR           = 2.5
TRAIL_MULT_ATR          = 1.875
ATR_TF                  = '1h'
MAX_POSITIONS_PER_SIDE  = 1
ADX_BELOW_FLOOR         = 20.0    ADX_DROP_THRESHOLD = 5.0    ATR_LEN = 14
indicators.ADX_CANDLE_LIMIT = 200       (the old recheck window was ATR_LEN*3 = 42)
```

All nominal. Nothing in the dropped work moved a geometry or mode constant.

---

## d) BOOK — STILL FLAT

```
virtual_positions:  22 rows, ALL status='closed', 0 open
active_positions:   0
exit_pending:       0
highest id = 28, closed 2026-08-07T06:00:10.519128+00:00
```

The book closed flat at 06:00:10Z and **nothing has opened since** — max id is still 28, so no row 29
was ever created. Confirmed.

**This is why the half-applied state is harmless right now:** the new INSERT paths cannot have fired,
because no position opened.

---

## e) TITAN — UNTOUCHED

```
git status  : clean (no output)
HEAD        : 897850b16586d69e01dff44bf6426da94704a333
gunicorn master 2538048 · worker 2538082   up since 2026-08-06 01:53:18  (1d 19h 56m)
optimizer_listener 2538053                 up since 2026-08-06 01:53:18
gemini_bridge 3647921                      up since 2026-07-28
```

Never restarted, not read for state, no numbers imported. Untouched.

---

## WHAT THE DROPPED SESSION ACTUALLY DID

It is worth being precise, because the code is *good* — the gap is proof and deployment, not quality.

### ✅ APPLIED AND COMPLETE ON DISK

**§1a — the recheck path now uses the sanctioned window.** `_recheck_fetch_1h_metrics` returns an
`AdxReading` from `indicators.adx_reading()`, pinned to `ADX_CANDLE_LIMIT`. `ADX_CANDLE_LIMIT` is bound
to `CANDLE_LIMIT` **by identity, not by a second literal that happens to agree** — so the entry
reference and every later reading are one measurement by construction.

**§1b — ATR was NOT moved blindly, and the coupling was checked.** SOL has the same trap Titan had, and
the code says so in the docstring: `entry_atr_pct_1h` is the baseline side of the `atr_contraction`
rule and has **two** producers on the 42-bar window — this function at entry, and a fallback in
`execute_entry` to `atr / fill_price` off `main.py`'s own `ATR_LEN*3` geometry fetch. Widening ATR here
would have left that fallback at 42 and changed **one side of a comparison** — the very defect being
fixed. So **two fetches were made deliberately**: ADX at 200, ATR kept at 42. Named, not silent.

**§1d — the provenance guard is real, and it is a guard, not a label.** `indicators.AdxReading` is a
`NamedTuple(value, window, tf)` with no defaults, so a reading cannot be built without stating all
three. `comparable_to()` refuses across windows *and* timeframes; `usable_for_threshold()` demands the
sanctioned window before any test against the calibrated `ADX_BELOW_FLOOR`; `adx_delta()` returns
`None` across windows so a legacy 42-bar baseline **cannot** be subtracted from a converged reading and
called a change. Refusals are **appended as visible reasons**, so a skip can never read as a passed
check. A bare float reaches none of it. Both entry write-sites (lines 262 and 2056), the recheck
rehydration, `_health_score`, `_tf_metrics_safe` and every log label were converted.

Schema: `virtual_positions.entry_adx_1h_window INTEGER` and
`smart_exit_dryrun_samples.adx_window INTEGER` added, with legacy rows left **NULL on purpose** —
"unrecorded", rather than backfilling 42 from a code invariant, which would be the same habit that
produced the defect.

**Verified by me:** all six ADX API symbols exist in `indicators.py`; all `indicators.*` call sites in
`virtual_trader.py` resolve; **all three files parse** (`ast.parse` clean); no bare-float ADX path
survives.

### ❌ NOT DONE — this is why I stopped rather than continued

| # | item | state |
|---|---|---|
| **§1c** | **QUANTIFY BEFORE APPLYING** — how many recheck verdicts flip OK→TIGHTEN, and would any have MOVED a stop | **UNPROVEN.** `adx_quantify.py` was written (21:02) and is read-only and well-formed, but **no output artifact exists**. The code was applied without a recorded answer. Under "never fabricate evidence", this counts as not done. |
| **proof** | execution both directions on an isolated copy, 13-file `DB_PATH` rewrite + leak assert | **NOT RUN.** `test_adx_guard.py` was written at **21:22** — the session died at that moment. `schema_test.db` (21:20) and `guard_test.db` (21:22) were staged; no result. |
| **§1e** | record in the canon that `entry_adx_1h` was biased high before this commit | **NOT DONE.** `OPEN-ITEMS-SOL.md` is byte-identical to its backup. |
| **deploy** | — | **NOT DEPLOYED.** Classic deployment gap: worker booted 00:25:50 against `main.cpython-312.pyc` dated **2026-08-06 15:50:47**. The running process holds **pre-edit** code. |
| **DB** | — | **NOT MIGRATED.** Live `virtual_positions` has 36 cols, **no** `entry_adx_1h_window`; `smart_exit_dryrun_samples` has 42 cols, **no** `adx_window`. |
| **report** | — | Nothing published, nothing sent. |

---

## RISK ASSESSMENT — why this is safe to leave frozen, and where the edge is

The on-disk code writes two columns the on-disk DB does not have. That disagreement is real, and it is
reconciled **only** by a restart. Three things keep it harmless:

1. **The book is flat** (0 open, max id 28). The new INSERT paths cannot fire until a position opens.
2. **The running worker holds pre-edit code** and `NRestarts = 0`. If a position opens *now*, the old
   code writes the old schema — consistent, no error.
3. **A restart self-heals.** `init_db()` is called at `main.py:814`, module level — it runs at import,
   before gunicorn serves any request, so both columns are added before any INSERT can reach them.

The residual edge: an `oom-armor.conf` drop-in exists on the unit. **An unattended OOM restart would
silently deploy this untested, unquantified change.** It would very likely work — but it would ship
without §1c, without the execution proof, and without the canon entry. That is the one thing worth
deciding quickly.

---

## WHAT I RECOMMEND

The work is good and the backups are complete. I recommend **completing it properly, not rolling it
back** — run §1c and record the number, run the guard test both directions on an isolated copy with the
13-file `DB_PATH` rewrite and the leak assert, write §1e into the canon, then restart to deploy, then
proceed to §2's measurement on the corrected ADX.

The alternative — `cp -p` the four `.bak_adxwindow_20260807` files back and redo from a clean tree — is
available and costs nothing but the redo.

**Awaiting your call. I have changed nothing.**

---

*Titan: untouched, HEAD 897850b, workers up 1d19h56m, never restarted.*
*SOL: PAPER (`OBSERVATION_MODE=True`), book flat, service healthy, 0 tracebacks.*
