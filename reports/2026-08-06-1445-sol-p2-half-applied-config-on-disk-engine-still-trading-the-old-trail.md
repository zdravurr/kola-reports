# SOL P2 IS HALF-APPLIED — THE CONSTANT IS ON DISK, THE ENGINE IS STILL TRADING THE OLD ONE

**2026-08-06 14:45 UTC · Mercury-SOL (PAPER) · §0 STATE RECONSTRUCTION ONLY. NOTHING WAS CHANGED BY ME.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`.
Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched, not read for state, not restarted** — clean at
`897850b`, working tree empty.

---

## THE ANSWER FIRST

**The gate fires. P2 is half-applied, and I stopped.**

The dropped session got exactly **one** thing done and then died before the two steps that make it real:

| | |
|---|---|
| `config.py` edited, `TRAIL_MULT_ATR` 2.5 → **1.875** | ✅ **DONE — 14:30:43** |
| The running engine loaded it | ❌ **NO — the process started 14:30:43 *minus* 35 minutes** |
| A report published for it | ❌ **NO — latest artefact is still 14:20** |
| P1 (close-card Gross) | ❌ **NOT STARTED** |
| G2c (paper trail label) | ❌ **NOT STARTED** |

> 🔴 **The disk says the trail gives back 0.75R. The engine in memory still gives back 1.0R.**
> `mercury-sol.service` has `NRestarts=0` and `ExecMainStartTimestamp = 13:55:22`. `config.py` was
> written at **14:30:43** — **35 min 21 s after** the process imported it. There is no
> `importlib.reload` anywhere in the tree (grepped: zero hits). Python imported `config` once, at
> boot, and cached it. **This is the "ФИКС НА ДИСКЕ ≠ ФИКС В РАБОТЕ" class, exactly.**

**The one piece of luck, and I want it on the record because it decides how cheap the recovery is:**
the book has been **flat since 2026-08-03 13:52:21** (vpos 27, the last close). **No position has been
opened since the config was edited.** So the stale value has not touched a single trade. There is no
contaminated cohort, no split epoch, nothing to unwind. A restart from flat is sufficient and total.

---

# §0 — WHAT IS APPLIED AND WHAT IS NOT

## a) Every SOL file with mtime after the M4 restart (13:55:22)

```
2026-08-06 14:00:02   optimizer/dynamic_weights.json   ← runtime artefact
2026-08-06 14:30:43   config.py                        ← 🔴 THE ONLY SOURCE FILE CHANGED
2026-08-06 14:40:07   optimizer/tg_offset.txt          ← runtime artefact
2026-08-06 14:40:10   oi_cache.json                    ← runtime artefact
2026-08-06 14:40:29   trades.db                        ← runtime artefact
```

**One source file. Nothing else.** `main.py` is still **13:51:21** and `virtual_trader.py` is still
**2026-08-05 00:20:58** — both *predate* the M4 restart, so neither P1 nor G2c was begun.

### Every `.bak_*` from 2026-08-06, with timestamps

```
12:08:45   trades.db.bak_pre_statededup_20260806
12:10:12   main.py.bak_nakedposition_M1M2M3_20260806
13:19:35   main.py.bak_M6M7_partial_lossstreak_20260806
13:35:16   main.py.bak_M4_native_trail_deleted_20260806      ← last CONFIRMED applied state
2026-08-05 00:19:54   config.py.bak_P2_trail_decouple_20260806   ← 🔴 THE P2 BACKUP EXISTS
```

The P2 backup carries an **Aug 5** mtime because it was made with `cp -p`, which preserves the source's
timestamp — it is a faithful byte-copy of `config.py` as it stood before the P2 edit, not a stale file.
**The rollback path is intact.**

## b) 🔴 `TRAIL_MULT_ATR` and `SL_BUFFER_ATR` — read from config

```
SL_BUFFER_ATR   = 2.5      ← UNCHANGED, as §1a demands
TRAIL_MULT_ATR  = 1.875    ← 🔴 NOT 2.5. PART OF P2 LANDED.
ratio           = 0.75
```

**Exactly what landed, stated precisely: instruction §1 landed on disk, in full and correctly.**
The code-only diff against the P2 backup — comments and blank lines stripped — is **one line**:

```
< TRAIL_MULT_ATR        = 2.5    # Trail callback = TRAIL_MULT_ATR × ATR(1h) / price × 100% (A5). Titan: 2.5.
> TRAIL_MULT_ATR        = 1.875  # = 0.75 × SL_BUFFER_ATR ⇒ trail gives back 0.75R.
```

Nothing else in `config.py` changed as code. Everything else in that edit is comment. And the comment
block satisfies §1a/§1b/§1c as written — it records the 1R identity, the ≥1R inertness (`trail=1.25R`
bit-identical to `trail=1.0R`), that 0.75R is **supported rather than optimised**, the explicit
Candidate-B rejection with the 82%/non-monotone-2.91-2.94-2.92 reasoning, the "no canon R-boundary is
required, and that is what makes this cheap" argument, and the pre-registered n=8 re-measurement
including "a null is a legitimate outcome, to be reported as a null and not re-cut."

> **So the edit is not wrong and not partial *in its own content*. It is correct, complete, and
> unloaded.** That distinction is the whole finding.

## c) P1 and G2c — neither landed, in whole or in part. Current code, quoted.

### P1 — the close card's Gross still excludes the partial

`virtual_trader.py` `close_position()`, the arithmetic that creates the contradiction:

```python
445:    gross_pnl  = (close_price - entry_price) * size * direction_mult   # ← REMAINDER ONLY
447:    total_fees = entry_fee + close_fee
448:    net_pnl    = gross_pnl - entry_fee - close_fee
...
457:    partial_pnl  = float(row['partial_pnl']  or 0.0) if 'partial_pnl'  in row.keys() else 0.0
458:    partial_fees = float(row['partial_fees'] or 0.0) if 'partial_fees' in row.keys() else 0.0
459:    net_pnl    += partial_pnl        # ← partial folded into NET
460:    total_fees += partial_fees       # ← partial folded into FEES
...
524:        'gross_pnl':   gross_pnl,    # ← 🔴 returned WITHOUT the partial
526:        'total_fees':  total_fees,
```

and the card that renders it, `_format_close_card()`:

```python
973:    gross   = res['gross_pnl']
974:    fees    = res['total_fees']
975:    net     = res['net_pnl']
...
991:        f"💵 Gross P&L:  {gross_str}\n"
992:        f"💸 Total Fees: -${fees:.4f}\n"
993:        f"💰 Net P&L:    <b>{net_str}</b>\n"
```

**Unchanged. The §1d mechanism is confirmed line-for-line:** `partial_pnl` is already net of
`partial_fees`, `net_pnl` and `total_fees` both absorb the partial at 459/460, and `gross_pnl` never
does. vpos 25 arithmetic reproduces the stated defect exactly:

```
Net − (Gross − Fees) = 126.523 − (102.046 − 10.9174) = +35.394   ← the $35.39 the card contradicts itself by
```

The self-consistent value is `gross_pnl + partial_pnl + partial_fees` (= Net + Fees = **137.44**), and
the one place every close passes through is `close_position()` before the return dict at line 524 —
the same shape as Titan's G2 fix in the unifier.

### G2c — paper still books a trail exit as `sl_triggered`

`virtual_trader.py:396-405`, unchanged:

```python
_CLOSE_LABEL = {
    'sl':          'sl_triggered_{s}',
    'trail':       'sl_triggered_{s}',      # ← 🔴 STILL sl_triggered
    'timeout':     'timeout_close_{s}',
    'exit_signal': 'exit_{s}',
```

and its justification comment, which is the part that went stale:

```python
390: #   'sl' / 'trail' -> sl_triggered_{side}   (live records trail-fired closes as
391: #                                            sl_triggered too — the monitor can't
392: #                                            distinguish; the literal reason is
393: #                                            kept in virtual_positions.close_reason)
```

That parenthetical stopped being true on 2026-08-05 when `_BYBIT_STOPTYPE_TO_REASON` made the live path
book `TrailingStop → 'trail'`. **The comment is now load-bearing and false — it argues for a mapping
whose premise is gone.**

**✅ Confirmed as instructed: `virtual_positions.close_reason` carries the truth on both sides.**

```
close_reason   count            trail closes: vpos 13, 15, 21, 25
------------   -----
exit_signal      6
sl              11
trail            4     ← the truth is recorded, so the damage is confined to `trades`
```

`main.py:1597` already documents the divergence in-tree: *"row 15004 is `sl_triggered_short` in
`trades` and close_reason=`trail` in virtual_positions."*

## d) Service

```
Active:                 active (running)
ExecMainStartTimestamp: Thu 2026-08-06 13:55:22 UTC   (the M4 restart)
MainPID:                2706601   gunicorn master, started 13:55:22
Worker:                 2706657   started 13:55:40
NRestarts:              0
Uptime at report:       ~48 min
Tracebacks since 13:55:22:  0
```

Clean run. The only journal noise is a recurring `CryptoPanic HTTP 404`, which predates all of this and
is not a traceback. **`NRestarts=0` with a 13:55:22 start is the proof of the half-application** — there
has been no opportunity for the 14:30:43 file to be read.

## e) Runtime invariants — imported **with `load_dotenv` first**

The bare-import trap is on record (`load_dotenv` override on a live `.env`), so the `.env` was loaded
before `import config`:

| constant | value | |
|---|---|---|
| `OBSERVATION_MODE` | `True` | ✅ paper |
| `SL_BUFFER_ATR` | `2.5` | ✅ **did not move** |
| `TRAIL_MULT_ATR` | `1.875` | 🔴 **P2 on disk only** |
| `ATR_TF` | `'1h'` | ✅ |
| `MAX_POSITIONS_PER_SIDE` | `1` | ✅ |
| `ADVISOR_WALL_ALIGNED_V2_MULT_CEILING` | `20.0` | ✅ |
| `NEWS_OBSERVATION_PINNED` | `True` | ✅ |

**Every invariant except the one P2 deliberately moves is where it should be.**

## f) Positions — flat, and flat for three days

```
virtual_positions status='open' :  0
active_positions                :  0
exit_pending                    :  0
virtual_positions total         :  21, ALL closed
```

Last activity **vpos 27, closed 2026-08-03 13:52:21**. **Nothing has opened since the config edit**, so
the stale in-memory 2.5 has not been applied to a single trade.

## g) Titan — untouched

```
git status --porcelain :  (empty)
HEAD                   :  897850b16586d69e01dff44bf6426da94704a333
```

`897850b` — *"the optimizer stops proposing live filters from paper dollars…"*. Not read for state,
not restarted, no worker touched.

---

# WHY I STOPPED, AND WHAT IT COSTS TO RESUME

The instruction was **"REPORT §0 AND STOP IF ANYTHING IS HALF-APPLIED."** It is half-applied, so I
stopped before doing any of §1–§3. I did not restart the service, and I did not begin P1 or G2c.

**I want to be precise about the *kind* of half-applied this is, because it changes the answer.** It is
not a torn edit or an inconsistent file — `config.py` is internally coherent, one code line changed,
the backup is intact, and the content satisfies §1 in full. It is half-applied in the *deployment*
sense only: **written but never loaded, and never reported.**

Resuming is therefore three steps and no unwinding:

1. **Restart from flat** to load `TRAIL_MULT_ATR = 1.875`. The book has been flat since 08-03, so this
   is free — no open position, no split epoch.
2. **Apply P1 and G2c** (both reporting-only; neither touches trading behaviour, so neither can
   contaminate the P2 measurement — that property still holds).
3. **Pre-register and publish** the P2 expectation that the dropped session never wrote down: the
   analytic estimate of **+1.280 R_ref (+$234.98), 6 of 7 improved, none harmed** (LONG +0.314 on 2 of 2,
   SHORT +0.966 on 4 of 5) — **stated in the same breath as its bias**, that it uses the FINAL water
   mark and therefore the LATEST possible trigger while the engine trails a RUNNING one, so a real
   earlier retrace fires sooner and it **may overstate**; plus the n=8 re-measurement at 10–50 s
   cadence, with a null pre-declared as a legitimate reportable outcome.

**Nothing needs to be reverted. Awaiting the word to proceed.**

---

*Generated 2026-08-06 14:45 UTC. Read-only session — no SOL file was modified, no service restarted.*
