# SOL — P2 IS NOW ACTUALLY RUNNING, P1 AND G2c ARE APPLIED, AND THE DEPLOYMENT GAP IS NAMED

**2026-08-06 15:10 UTC · Mercury-SOL (PAPER) · APPLIED AND PROVEN BY EXECUTION.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`.
Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched, not read for state, not restarted** — clean at
`897850b`, workers 2538048/2538082 up since 01:53:18, undisturbed for 13 h.

---

## THE ANSWER FIRST

All three steps are done. **Four code lines changed across two files**, plus the trail constant that was
already on disk and is now actually loaded.

| step | state |
|---|---|
| 1 · restart from flat, `TRAIL_MULT_ATR=1.875` in the RUNNING worker | ✅ **proven from the worker's own bytecode** |
| 2a · **P1** close-card Gross | ✅ applied, proven both directions |
| 2b · **G2c** paper trail label | ✅ applied, proven both directions |
| 3 · pre-registration + the deployment gap as a canon finding | ✅ below, published before the first trade |

**Nothing was reverted, and the book never left flat.** Last close is still vpos 27 on 2026-08-03; the
restarts happened with zero open positions, so `SL_BUFFER_ATR`, 1R and the arming price are all
exactly where they were and the before/after cohorts remain directly comparable.

---

# 1. THE RESTART — AND HOW I ESTABLISHED IT FROM THE WORKER

Restart issued **14:55:23**. Master `2722203` at 14:55:25, worker `2722353` forked at **14:55:55**.
Second restart at **15:05:23** to load P1/G2c: master `2725324`, worker **`2725363` at 15:05:40**.
Flat confirmed immediately before each (`open`/`active`/`exit_pending` = 0/0/0), and after.

**Fresh import with `load_dotenv` first** (the documented trap — see §4):

```
OBSERVATION_MODE = True     SL_BUFFER_ATR = 2.5     TRAIL_MULT_ATR = 1.875
ATR_TF = '1h'               MAX_POSITIONS_PER_SIDE = 1
ADVISOR_WALL_ALIGNED_V2_MULT_CEILING = 20.0         NEWS_OBSERVATION_PINNED = True
trail/SL ratio = 0.75
```

## 🔴 But a fresh import proves nothing about the worker — that was the whole finding. Here is what I actually did.

**I want to be exact about what this establishes, because "I checked" is the claim that failed last time.**
There is no way to read a running CPython process's module globals without injecting code into it, and I
was not willing to inject into the process whose correctness I was trying to prove. So instead of
asserting the worker's memory, I proved it from **an artifact the worker itself produced and validated**:

CPython caches each module as a `.pyc` whose header stores the **source mtime and size** it was compiled
from. On import the interpreter compares that header against the source on disk; a mismatch forces a
recompile. So whichever branch the worker took, the bytecode it executed encodes the current source.

```
config.py        mtime 14:30:43   size 55384
config...pyc     header: source mtime 14:30:43, size 55384   →  MATCHES     (flags=0, timestamp-validated)
  config bytecode:  TRAIL_MULT_ATR <- 1.875
  config bytecode:  SL_BUFFER_ATR  <- 2.5
virtual_trader   pyc validates against current source: True  (src 15:00:54, pyc hdr 15:00:54)
optimizer        pyc validates against current source: True  (src 15:01:32, pyc hdr 15:01:32)
```

Every one of those sources is **older than the worker's fork** (15:05:40), and the `.pyc` headers match
them exactly. Combined with two facts I verified separately —

* **zero `importlib` occurrences anywhere in the tree**, so no reload path exists and a process's value is
  fixed at its first `import config`; and
* **no `os.environ`/`getenv` override for `TRAIL_MULT_ATR` or `SL_BUFFER_ATR`** in `config.py` (they are
  plain literals at lines 104 and 60),

— the conclusion is forced: **the worker holds 1.875.** And `/health`, which is served *by the worker*,
answers `{"bot":"MERCURY-SOL","status":"ok"}`, so the process being reasoned about is the one serving.

**Stated honestly: this is a proof from artifacts and process facts, not a direct read of live memory.**
It is much stronger than "the file says 1.875" — which is precisely the claim that was false at 14:45 —
but it is not the one-glance certainty a startup log would give. That is exactly the gap §4 proposes to
close, and it is why I am proposing it.

**Tracebacks since each restart: 0.** No `NRestarts`. Only the pre-existing `CryptoPanic HTTP 404` noise.

---

# 2. P1 AND G2c — APPLIED, AND PROVEN BOTH DIRECTIONS

## The change, in full — code-only diff, comments and blanks stripped

```
virtual_trader.py
  255c255
  <     'trail':       'sl_triggered_{s}',
  >     'trail':       'trail_{s}',
  294a295
  >     gross_pnl  += partial_pnl + partial_fees

optimizer.py
  38a39  >     'trail_long',
  41a43  >     'trail_short',
```

**Four lines.** `main.py` (13:51:21), `claude_advisor.py` (12:15:12), `config.py` (14:30:43),
`state_machine.py`, `signal_weights.py` — all untouched, mtimes unchanged. **The cascade, the score bars,
both prompts, the state dedup and M1–M7 all live in `main.py` and `claude_advisor.py` and were not
opened.** Backups: `virtual_trader.py.bak_P1_G2c_20260806`, `optimizer.py.bak_G2c_trail_label_20260806`.

## a) P1 — why the addend is `partial_pnl + partial_fees`, not `partial_pnl`

`partial_pnl` is already **net** of `partial_fees`, so the partial's *gross* contribution is its net plus
the fees taken out of it. Adding only `partial_pnl` would have left the card short by exactly
`partial_fees`. With the full addend the identity **Gross − Fees == Net** holds for every close:

```
gross + p_pnl + p_fees − (entry_fee + close_fee + p_fees)
  = gross − entry_fee − close_fee + p_pnl   ==  net_pnl   ✔
```

Fixed in `close_position()` — **the one place every close passes through, paper and live alike** (the
live exchange-close route reaches the same function via `_poller_close`). Fixing `_format_close_card`
instead would have left every future caller free to forget. Same shape as Titan's G2 fix in the unifier.

**Reporting-only, and provably so:** `gross_pnl` is never written to the DB — the `UPDATE` stores
`net_pnl`/`total_fees`, the `INSERT` stores `net_pnl`/`close_fee`. It reaches the close card and the
CLOSE log line and nothing a trading decision reads.

## b) G2c — and a correction to the audit's framing that makes the fix BROADER

`_CLOSE_LABEL['trail']` now maps to `trail_{s}`, and **the false justification at lines 390-393 was
deleted in the same edit**, as instructed — a dead rationale beside a corrected mapping is the next
reader's trap. It claimed *"live records trail-fired closes as sl_triggered too — the monitor can't
distinguish"*; that stopped being true on 2026-08-05 when `_BYBIT_STOPTYPE_TO_REASON` (main.py:2813)
taught the engine to read the venue's own `stopOrderType` and book `TrailingStop → 'trail'`. I also
fixed a second stale cross-reference at the `post_entry_critical` entry, which cited `'trail'` as the
*precedent* for pooling into `sl_triggered`.

> 🔶 **The 13:00 audit called this a paper-vs-live split. The code does not split that way, and saying so
> makes the fix bigger, not smaller.** The live exchange-close route reaches this **same** `_CLOSE_LABEL`
> through `_poller_close` (virtual_trader.py:1401-1413), so **both** paths were writing `sl_triggered_{s}`
> into `trades` while **both** wrote the literal `'trail'` into `virtual_positions.close_reason`. The real
> divergence was never paper-vs-live — it was **`trades` vs `virtual_positions`, on both sides at once.**
> One line fixes both paths, and no new paper/live asymmetry is created.

### 🔴 The optimizer was taught the new label in the same pass — this was not optional

`pair_trades` infers side from **set membership**, so an unregistered close label is not an error: it is
**silently dropped from learning**. That is the exact P4 defect already documented in `optimizer.py:74-79`,
where a stale `'5m_armed_exit'` quietly removed every armed-exit close from both bots' optimizers.
Emitting `trail_{side}` without registering it would have introduced that bug fresh.

Because the label was recognised before (as `sl_triggered_*`) and is recognised now (as `trail_*`), **the
paired set is unchanged** — which is what keeps G2c reporting-only. Historical rows keep their
`sl_triggered_*` labels and were **not** rewritten.

> ⚠️ **A divergence I am flagging rather than burying:** `optimizer.py` carried a note that its close-type
> sets stay *byte-identical to Titan's*. They no longer are. **Titan is LIVE and was deliberately not
> touched.** Titan does not *emit* `trail_{side}` either, so nothing of Titan's is dropped — this is a
> divergence in coverage, not behaviour. **Porting G2c to Titan is your call, not mine.**

## c) EXECUTION PROOF — isolated tree, 13-file rewrite, leak assert, both directions

The harness rebuilds **vpos 25** — the real position whose card went to Telegram on 2026-08-01 — as an
open position from its actual stored values, and closes it through the real `close_position()`.

**Isolation, both traps handled:**
* **13-file source rewrite.** Exactly 13 modules hardcode the production DB path; `main.py` alone reads
  `os.getenv('DB_PATH', …)`. Rewriting one is not enough — that is the recorded trap. All 13 rewritten,
  then a residual grep proved **0** production paths survived in the copy.
* **Leak assert.** `sqlite3.connect` was wrapped to **raise** on any attempt to open the production book.
  Stronger than checksumming the live file afterwards, because the live bot writes to it continuously.
  Result both runs: **`production-book opens: 0`**.
* **The `load_dotenv` trap, caught in flight.** My first isolated run reported `OBSERVATION_MODE: False`.
  Cause: the flag is `MERCURY_OBSERVATION_MODE`, not `OBSERVATION_MODE`, and **`config.py` never calls
  `load_dotenv` itself** — a bare import silently yields the *opposite* of production. The harness now
  loads the **isolated copy** of `.env` (never the production file) before importing config, and reports
  `OBSERVATION_MODE: True`. I am recording this because it is the same trap in a new costume and it
  would have quietly invalidated the run.

### BEFORE — the defect reproduces exactly

```
── CASE A: trail close WITH a partial (vpos 25 reconstructed) ──
  Gross P&L       : +102.0460
  Total Fees      :   10.9174
  Net P&L         : +126.5230
  Net-(Gross-Fees): +35.394333
  trades.signal_type            : sl_triggered_short
  virtual_positions.close_reason: trail
```

**That is vpos 25's real Telegram card, reproduced to the cent:** `+$102.046 / −$10.9174 / +$126.523`,
self-contradiction **$35.39**. And `35.394333 = partial_pnl + partial_fees = 31.7494754 + 3.6448579`.

### AFTER — both defects gone

```
── CASE A: trail close WITH a partial ──
  Gross P&L       : +137.4403          ← = Net + Fees, the predicted 137.44
  Total Fees      :   10.9174
  Net P&L         : +126.5230
  Net-(Gross-Fees): +0.000000
  trades.signal_type            : trail_short
  virtual_positions.close_reason: trail
  'trail_short' recognised by pair_trades: True
```

### CONTROL — a close with no partial is untouched by P1

```
── CASE B: NO partial, reason='sl' ──
  BEFORE: Gross +102.0460  Fees 7.2725  Net +94.7735   Net-(Gross-Fees) = +0.000000   label sl_triggered_short
  AFTER : Gross +102.0460  Fees 7.2725  Net +94.7735   Net-(Gross-Fees) = +0.000000   label sl_triggered_short
```

**Identical.** P1 moves only partial-bearing closes; `sl` keeps its label.

## d) `virtual_positions.close_reason` still carries the truth — confirmed, and NOT rewritten

```
exit_signal   6        trail   4   (vpos 13, 15, 21, 25)        sl   11
```

Unchanged from the 14:45 measurement. **vpos 25's DB row was not touched** — the row was always correct;
only the card was wrong.

---

# 3. 🔴 PRE-REGISTRATION — WRITTEN DOWN BEFORE THE FIRST TRADE UNDER 0.75R

**The expected effect, on the 7 armed positions:**

| | R_ref | detail |
|---|---|---|
| **total** | **+1.280** (**+$234.98**) | **6 of 7 improved, none harmed** |
| LONG | +0.314 | 2 of 2 |
| SHORT | +0.966 | 4 of 5 |

## 🔴 AND ITS BIAS, IN THE SAME BREATH

This estimate uses the **FINAL water mark**, which gives the **LATEST possible trigger**, while the engine
trails a **RUNNING** one. A real earlier retrace fires sooner. **It is outside the validated replay and it
MAY OVERSTATE.** It establishes direction, not magnitude. It is not a forecast and must not be quoted as
one — if the realised result comes in below +1.280 R_ref, that is the expected behaviour of a biased
estimator, not a failure of the change.

## The re-measurement, fixed now so it cannot be re-cut later

* Re-run **the identical 14:20 grid** at **8 trailed exits** — ~7 weeks at the observed 0.57/week.
* All 8 recorded at the current **10–50 s** excursion cadence, **not** the 305 s that destroyed vpos 21.
* **If it does not confirm, revert.** One constant, no boundary, nothing else to unwind.
* 🔴 **A null at n=8 is a legitimate outcome, to be reported AS A NULL and not re-cut.** No new cohort
  splits, no post-hoc subgroup, no "it works if you exclude…". The grid is fixed as of 14:20.

**No canon R-boundary is required and none was created.** 1R = `SL_BUFFER_ATR × ATR × size` contains no
trail term, `SL_BUFFER_ATR` did not move, and the book was flat across both restarts — so R before and
after are directly comparable and must **not** be split into separate cohorts.

---

# 4. 🔴 THE DEPLOYMENT GAP — A FINDING FOR THE CANON, NOT JUST FOR THIS REPORT

> **A config edit is not applied until a restart loads it. This codebase has no reload path. And the only
> reason today's gap cost nothing is that the book happened to be flat.**

Between 14:30:43 and 14:55:55 — **25 minutes** — `config.py` said the trail gives back 0.75R and the
running worker gave back 1.0R. Nothing in the system could tell the difference:

* **There is no reload path.** Zero `importlib` occurrences tree-wide. A process's constants are frozen at
  its first `import config`; editing the file afterwards changes nothing until a restart.
* **Nothing logs the geometry.** No startup line, no health field, no periodic line reports the trail or
  stop multiplier. `/health` returns `{status, bot, exchange}` and nothing else.
* **The only path that would have surfaced it is a trade** — the entry card prints the trail % — and a
  trade is exactly the event that would have been recorded under the wrong geometry.

**So the failure was silent by construction, and the recovery was luck.** Had a signal fired at 14:35,
a position would have opened at 1.0R trail while every artifact on disk claimed 0.75R, and the n=8
cohort would have been contaminated from its first observation — by a mislabelled member that nothing
would have flagged. This belongs beside §0.0 "ТИШИНА — НЕ ПОЛОМКА": here, too, silence was not health.

### The proposal — and I am proposing it, not building it

**One line at worker startup that logs the geometry constants the WORKER actually holds**, e.g.

```
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5  TRAIL_MULT_ATR=1.875 (0.750R)  ATR_TF=1h  OBSERVATION_MODE=True
```

Why this and not something larger:

* **It closes the gap at the exact point it opens** — the worker's own import — and says what the process
  *has*, never what the file *says*. That distinction is the entire finding.
* **It makes the check one glance in the journal**, replacing the `.pyc`-header reasoning I had to do in
  §1. That reasoning is sound but nobody will repeat it under time pressure.
* **It is inert.** A print at boot cannot change a decision, so it can ship at any time without a
  measurement window — including during the n=8 window, without contaminating it.
* **It is auditable after the fact**: the journal retains it, so "what geometry was position N opened
  under?" becomes answerable from the log instead of inferred from file mtimes.

**Not built in this pass, as instructed.** It also plainly applies to Titan, which has the same import
model and real money on it — but Titan was not touched and that call is yours.

---

# 5. TWO THINGS I FOUND AND DID NOT FIX — recorded, not silently changed

### 🔴 F1 — `_CLOSE_LABEL[reason]` will `KeyError` on six real LIVE exit reasons

`close_position` looks the label up with a **bracket** (`virtual_trader.py:532`), but the live path feeds
it whatever `_classify_exchange_exit` returns from the venue. Six of those reasons have no mapping:

```
mapped   : sl, trail
UNMAPPED : adl, exchange_market, exchange_unreported, liquidation, settlement, tp
```

A liquidation, an ADL, a manual close in the Bybit app, or a take-profit would raise `KeyError` **inside
the close path** — the worst possible place, since `_book_exchange_close` has already substantiated that
the position is gone. **Unreachable today**: the branch is gated on `not _is_paper(row)`, and SOL is in
`OBSERVATION_MODE`, so every row is paper. But it is armed for the live flip, and the reasons most likely
to hit it are the ones you least want dropped. **Not fixed here** — it is a live-path behaviour change and
this pass was scoped to reporting.

### 🔶 F2 — the retired monitor's close label

`main.py:4793` still writes `sl_triggered_{side}` directly. Its own comment marks it as the **retired**
`_monitor_positions`, absorbed into the Phase-2 engine. Left alone deliberately; noting it so the G2c fix
is not later mistaken for total coverage of the `trades` label surface.

---

# 6. FINAL STATE

```
mercury-sol.service   active (running)   master 2725324   worker 2725363 (15:05:40)   NRestarts=0
tracebacks since restart : 0
open vpos / active_positions / exit_pending : 0 / 0 / 0        (flat since 2026-08-03)

OBSERVATION_MODE = True          SL_BUFFER_ATR = 2.5  ← did not move
TRAIL_MULT_ATR   = 1.875 (0.75R) ← loaded in the worker, proven from its bytecode
ATR_TF = '1h'   MAX_POSITIONS_PER_SIDE = 1   WALL_V2_CEILING = 20.0   NEWS_PINNED = True

_CLOSE_LABEL['trail'] = 'trail_{s}'      _CLOSE_LABEL['sl'] = 'sl_triggered_{s}'
optimizer close types  = [..., 'trail_long'] / [..., 'trail_short']
virtual_positions.close_reason : trail 4 · sl 11 · exit_signal 6   (untouched)

TITAN: git clean · HEAD 897850b · workers 2538048/2538082 up since 01:53:18 · NOT TOUCHED
```

**The next trailed exit is observation 1 of 8.**

---

*Generated 2026-08-06 15:10 UTC. Changes: 4 code lines in 2 files + the trail constant now loaded.
Backups: `config.py.bak_P2_trail_decouple_20260806`, `virtual_trader.py.bak_P1_G2c_20260806`,
`optimizer.py.bak_G2c_trail_label_20260806`.*
