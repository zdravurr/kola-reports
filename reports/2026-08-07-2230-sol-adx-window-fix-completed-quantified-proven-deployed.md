# SOL — ADX WINDOW FIX **COMPLETED**: quantified, proven both directions, deployed. And the flat gate it enables is **REFUTED by SOL's own book**.

**2026-08-07 22:30 UTC** · Mercury-SOL · **PAPER** (`OBSERVATION_MODE=True`, verified at boot)
Parent: `2026-08-07-2050-…-entry-exit-routing.md` · State check: `2026-08-07-2155-…-session-dropped.md`
Titan (`/root/titan-bot`): **untouched** — clean, HEAD `897850b`, workers never restarted.

---

## HEADLINE

**§1 is closed and live.** Worker **pid 3134680**, booted **2026-08-07 22:11:26 UTC**, from flat.
The half-applied state that any OOM restart could have shipped silently no longer exists.

**And the measurement §2 asked for kills the idea it was supposed to enable.** On the corrected ADX,
the pre-registered flat gate **refuses the book's winners**: it keeps 15 trades worth **−7.704R** and
refuses 7 worth **+2.329R**. It would have made a losing book **worse by 2.33R**. This is the same
failure mode as the EMA envelope, and per the brief I am saying so immediately. **Nothing was
applied.** Filter number twenty dies with the other nineteen.

---

# §1c — QUANTIFIED, BEFORE THE RESTART

`adx_quantify.py` ran. The earlier session's silence was a SIGPIPE from a `head` in the pipeline, not
a code fault — but it left no artifact, so it counted as not done.

### The replay is trustworthy — validated before anything was concluded from it

Recomputing the **shipped** 42-bar ADX at each entry instant and comparing against the value the bot
actually stored: **22 of 22 reproduce within 1.0 point**, mean |Δ| **0.038**, max **0.235**.
The forming 1h candle was rebuilt from 5m bars, because ccxt returns it and `compute_tf_metrics`
takes `.iloc[-1]`.

### The bias

**17 of 22 entries read HIGH** (5 read low). Worst: **vpos 21 — 60.76 stored vs 29.00 converged,
+31.76 points**; vpos 28 — 34.15 vs **14.14**; vpos 16 — 47.93 vs 27.03; vpos 19 — 36.94 vs 22.00.

> An earlier note said "16 of 22". **17 of 22** is the correct count, measured here against a
> recomputed 200-bar ADX on the same candles. I have corrected the canon.

### a) How many verdicts flip

Replayed over **all 66** tier evaluations (22 positions × T+10/60/300s):

| | |
|---|---|
| **OK → TIGHTEN** | **9 of 66** — vpos **11, 17, 28**, all three tiers each, all SHORT |
| **TIGHTEN → OK** (c) | **0** — no stop that *was* tightened would have been left alone |
| could reach EMERGENCY | **0** |

The EMERGENCY bound is structural, not assumed: `_health_score` is monotone (`score = 0` then only
`-=`, verified), and `recheck_status='done'` means every tier scored > −5. An extra −5 therefore lands
in **[−9, −5]** — TIGHTEN, never ≤ −10. The wall rule needs a historical OKX book that does not
exist; it did not need replaying, because the observed outcome bounds it.

### b) 🔴 WOULD ANY HAVE MOVED A STOP? — **YES. This is where SOL differs from Titan.**

Titan's nine were no-ops under an existing bound. **SOL's are not.** I verified the branch rather than
trusting the claim: `_tighten_sl` returns midpoint(entry, SL) with tighten-only and never-cross-entry
clamps, `_exec_move_stop` fires, and `UPDATE virtual_positions SET sl_price` commits — in paper too,
because the engine's own comparison is the backstop.

**All three stops move. One changes the outcome:**

| vpos | side | entry | SL | tightens to | max adverse | outcome |
|---|---|---|---|---|---|---|
| 11 | SHORT | 71.43 | 73.33 | 72.38 | 71.99 | never reached — **unchanged**, +1.133R survives |
| 17 | SHORT | 75.91 | 77.41 | **76.66** | **76.83** | 🔴 **STOPPED OUT** — +0.004R → ≈ **−0.5R** |
| 28 | SHORT | 72.77 | 73.75 | 73.26 | 72.95 | never reached — **unchanged**, −0.153R |

Cost on the closed book: **≈ 0.5R, on the one near-flat trade**, and the +1.133R winner is untouched.
The tightened stop is exactly half the original distance, hence ≈ −0.5R.

**This is a correctness fix. Whether "tighten on a flat tape" is a good rule is a separate question —
and §2 below answers it, badly.**

---

# §2 — THE EXECUTION PROOF, BOTH DIRECTIONS

`test_adx_guard_v2.py`, on **isolated copies** of the pre- and post-edit trees.

**POST: exit 0, every check passes. PRE: exit 1.**

### Isolation — and a trap the brief did not know about

All **13** files carrying the live `trades.db` literal were rewritten. The 13th is the one a
`^DB_PATH =` grep misses: **`market_context.py:277` uses `_DB_PATH`** (leading underscore).

🔴 **Then the leak assert fired on the post tree — and it was right.** `init_db()` opened the **live
database** anyway:

```
AssertionError: 🔴 DB LEAK — test opened the LIVE database:
    /mnt/volume_nyc1_1780480650620/mercury-sol/trades.db
```

**Cause: `.env` line 2 sets `DB_PATH=` to the live database, and `main.py` does
`load_dotenv(..., override=True)` — which beats the rewritten literal *and* `os.environ`.**
**The 13-file rewrite is necessary but NOT sufficient. There is a 14th vector.** The copied tree's
`.env` must be rewritten too and `load_dotenv` repointed at it. Recorded in the canon. Without the
leak assert this test would have "passed" while reading production.

### b) The four things proven

| claim | proof |
|---|---|
| a 42-bar reading cannot be compared to a 200-bar one | `adx_delta(A(30,42), A(20,200))` → `None` |
| `adx_delta()` refuses across windows | also `None` across timeframes, and for a bare float |
| `usable_for_threshold()` refuses a non-sanctioned window | 200 ✔ · 42 ✘ · unknown ✘ · None ✘ |
| a refusal appends a **VISIBLE** reason | `ADX-floor SKIPPED: ADX1h=14.0 [42-candle window] — floor is calibrated on the 200-candle window` |

Also proven: `adx_reading_from_ohlcv` reports the **actual** bar count (60 bars in → window 60), so a
short cache slot cannot masquerade as 200; a NULL stored window becomes `ADX_WINDOW_UNKNOWN` and is
never guessed as 200.

### a) The pre-edit tree fails — and fails *behaviourally*, not just on a missing symbol

A missing attribute proves absence, not wrongness. So I ran the **same two scenarios through both
trees**, using vpos 28's real numbers (42-bar 34.15 / 200-bar 14.14):

| scenario | PRE-EDIT | POST-EDIT |
|---|---|---|
| 42-bar reading alone | score **0**, reasons **`[]`** — **silent** | score 0, reasons `['ADX-floor SKIPPED: …']` |
| **42-bar entry vs 200-bar current** | score **−8**, `['ADX -20.0 (-3)', 'ADX 14.1<20 (-5)']` | score **−5**, `['ADX-drop SKIPPED: … different windows, not a change', …]` |

The pre-edit code **invents a −20.0-point "change" out of two different measurements** and charges −3
for it. And in the silent case it returns a bare `0` that is **indistinguishable from a passed check**
— which is exactly how this survived 22 positions.

### c) Migration: idempotent, legacy rows NULL

Starts without both columns (matching live) → migration adds both → **all 22 legacy rows left NULL,
0 backfilled with 42** → second `init_db()` does not raise, columns still exactly once.
Backfilling 42 from a code invariant would be the same habit that produced the defect.

---

# §3 — THE CANON

`OPEN-ITEMS-SOL.md` now opens with a **DATA BOUNDARY** section (backup:
`.bak_adxwindow_applied_20260807`). The boundary is stated as an exact instant **and** as a durable DB
predicate, so a future study cannot pool across it by accident:

| | before | after |
|---|---|---|
| `virtual_positions.id` | **≤ 28** | **≥ 29** |
| `entry_adx_1h` window | **42** (`ATR_LEN*3`), not converged | **200** (`CANDLE_LIMIT`) |
| `entry_adx_1h_window` | **NULL** = unrecorded | **200** |
| `smart_exit_dryrun_samples.adx_*` | 42 | 200 |

**Boundary instant: 2026-08-07 22:11:26 UTC.** `trades.srv_adx_1h` is **not** affected — it always
used `CANDLE_LIMIT`. That is precisely why the defect was invisible: two different measurements sat in
columns named as if they were one.

---

# §4 — DEPLOYED

Restart taken **from flat** (0 open, `active_positions` 0, `exit_pending` 0, max id 28). Consistent DB
backup first: `trades.db.bak_pre_adxwindow_migration_20260807` (sqlite backup API, not `cp` — the
worker was writing).

| check | result |
|---|---|
| migration ran | `entry_adx_1h_window` ✔ · `adx_window` ✔ |
| legacy rows | **22 NULL, 0 backfilled** |
| `OBSERVATION_MODE` | **True** |
| boot geometry | `SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h OBSERVATION_MODE=True [pid 3134680]` |
| tracebacks since restart | **0** |
| book | still flat, max id 28 |

**Loaded code proven by `.pyc` header**, not inferred from mtimes — each `.pyc`'s embedded source
mtime matches its `.py` exactly (`main` 1786137612, `indicators` 1786136951, `virtual_trader`
1786137542), and `main.pyc` was rewritten at the 22:11:26 boot.

### 🔴 The discipline lapse, for the record

The dropped session regenerated `__pycache__` **in the live tree** at 21:21 — it imported the live
modules rather than only an isolated copy. Nothing was harmed (the DB was unmigrated, the book flat),
but the habit is the risk.

**What prevents recurrence:** the harness used here does it structurally, not by intention —
(1) the tree under test is a **copy**, never the live path on `sys.path`; (2) `sys.dont_write_bytecode
= True`, so no `.pyc` is produced anywhere; (3) the **`sqlite3.connect` leak assert raises** on any
live path, so a missed rewrite fails loudly instead of quietly reading production — as it did here,
catching the `.env` vector. A test that *can* touch production eventually will; this one cannot.

---

# §5 — THE MEASUREMENT. THE GATE IS REFUTED.

Read-only. **Nothing proposed, nothing applied.**
Pre-registered before any outcome was inspected: **ADX(1h,200) ≥ 20 AND 24h range-width percentile
≥ 20.** ADX 20 is *not* fitted — it is the bot's existing `config.ADX_BELOW_FLOOR`. Exactly one pair
tested; no grid search.

### 🔴 d) It refuses the book's winners — the envelope's failure mode, again

| | n | win | ΣR |
|---|---|---|---|
| **kept** by the pair | 15 | **20.0%** | **−7.704** |
| **refused** by the pair | 7 | **71.4%** | **+2.329** |
| whole book | 22 | 36.4% | −5.374 |

The gate turns **−5.374R into −7.704R**. Among the 7 it refuses are the two best SHORTs (**+1.257**,
**+1.133**) and 5 of the book's 8 profitable trades. It does refuse the two genuine chop cases
(vpos 27 −0.660, vpos 28 −0.153) — **the mechanism is not imaginary** — but ADX < 20 does not isolate
them: it also catches vpos 11 (+1.133) and vpos 17 (+0.004).

Volume: 0.417 → 0.284 entries/day (68% kept). **LONG 9 → 8, SHORT 13 → 7.**

### a) By ADX quartile — monotone in the WRONG direction

| quartile | ADX range | n | win | ΣR |
|---|---|---|---|---|
| Q1 lowest | < 21.5 | 5 | 40.0% | −0.708 |
| Q2 | 21.5–27.0 | 6 | **66.7%** | **+1.084** |
| Q3 | 27.0–30.3 | 5 | 20.0% | −4.086 |
| Q4 highest | ≥ 30.3 | 6 | 16.7% | −1.664 |

The *highest*-ADX bucket is the worst. `ADX ≥ 20` keeps −5.699R and refuses **+0.325R**.

🔴 **And on LONG the ADX leg is a structural no-op: every one of the 9 LONG entries had ADX ≥ 20**
(`ADX<20` → n=0). Exactly like the envelope, it is a one-sided instrument wearing a filter's clothes.

### b) By 24h range width — also backwards

Tightest quartile (wPct < 21): **win 60.0%, ΣR +1.192** — the best bucket. Q3 (58–78): −3.199.

### e) Bonferroni, and de-confounding

**9 tests → corrected α = 0.0056. Nothing survives.** Best p = **0.0534** (the pair) — and it points
the *wrong way*: it is weak evidence the gate **hurts**.

Refusals do not ride on a day or an hour: they spread across Mon 2/3, Thu 2/3, Tue 1/4, Sun 1/4,
Sat 1/2, Wed 0/4, Fri 0/2, and across hour buckets 3/9, 2/5, 1/5, 1/3. No day or session drives it.
There is no confound to de-confound — the effect simply is not there.

### f) Does n support a decision?

**No — and it is worse than "unprovable".** With 22 entries (9 LONG / 13 SHORT) and only 2 clean chop
cases, nothing approaches significance under correction. But this is not the "right in mechanism,
unprovable at this n" case: **the point estimate points the wrong way, decisively and on both legs
independently.** The honest statement is:

> The mechanism is real for vpos 27 and 28. **ADX(1h,200) < 20 does not select them** — it selects a
> set that is, on this book, *more* profitable than what it keeps. As a gate it is refuted; as a
> hypothesis about chop it is untested, because n = 2.

**No filter is proposed. Nothing was applied.** The corrected ADX now feeds the recheck rules, which
is a correctness change on its own merits — its measured cost on the closed book is the ≈0.5R on
vpos 17 quantified in §1c, and it was deployed knowing that.

---

## Scope honoured

Untouched: loss-streak brake, geometry, cascade, score bars, both prompts, `MERCURY_OBSERVATION_MODE`.
SOL remains **PAPER**. Titan never read, never restarted, never imported.

**Ordering note:** §3 was written immediately *after* the restart rather than before it. The canon's
own house style records "worker pid N, booted T, restart taken from flat" — an exact timestamp that
cannot exist before the restart. The brief's hard constraint, *do not deploy before §1c*, was
honoured: §1c and the full execution proof both completed before the service was touched.

## Rollback

`*.bak_adxwindow_20260807` (code, `cp -p`) · `OPEN-ITEMS-SOL.md.bak_adxwindow_applied_20260807` ·
`trades.db.bak_pre_adxwindow_migration_20260807`. The two new columns are additive and NULL for every
legacy row, so a code rollback needs no schema rollback.
