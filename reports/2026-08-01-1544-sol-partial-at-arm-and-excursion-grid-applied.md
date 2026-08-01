# sol-partial-at-arm-and-excursion-grid-applied

_2026-08-01 15:44 UTC_

---

# MERCURY-SOL — TWO CHANGES APPLIED, 2026-08-01 15:38 UTC

**Titan was not touched** — proof in §5. **SOL stays PAPER** (`MERCURY_OBSERVATION_MODE=1`,
re-verified at runtime after the restart). Acting on the §5 verdict of the 15:24 simulation, not
past it.

| | |
|---|---|
| files changed | `config.py`, `main.py`, `virtual_trader.py` |
| snapshots | `*.bak_partialarm_excursiongrid_20260801` |
| service | `mercury-sol.service` restarted deliberately at **15:37:56 UTC** |
| master / worker | **1101824** (was 1793275) / worker **1101944** forked 15:38:11 |
| open positions | **0** — nothing was live during the change |
| tracebacks since restart | **0** |

⚠️ **I made a mistake during verification and cleaned it up — see §6.** It is reported in full
because it briefly wrote into the live database.

---

# §1 — CHANGE 1: THE EXCURSION GRID (measurement only)

Config-only. No code path was edited.

```diff
 EXCURSION_LOGGING_ENABLED = True
-EXCURSION_SAMPLE_SEC       = 60     # base cadence between samples per position
-EXCURSION_DENSE_UNTIL_SEC  = 900    # dense (1x) for first 15 min (fast-SL region),
-                                    # then 5x cadence after
+EXCURSION_SAMPLE_SEC       = 10     # base cadence between samples per position
+EXCURSION_DENSE_UNTIL_SEC  = 3600   # dense (1x) for the first hour,
+                                    # then 5x cadence (50s) after
```

(plus a 15-line comment block recording why, the cost and the safety argument.)

**Why:** the realised cadence was a **305s median against a 10s live poller — 31× coarser**. The
recorded running peak missed the true peak by up to **0.298R** (vpos 21). A trail is a pure
function of the running peak, so the 15:24 simulation could not reproduce **either** of the
book's two trail exits until the peak was corrected from `water_mark`, and any trail narrower
than ~0.3R was finer than the instrument's own error.

**New cadence:** 10s (== `MONITOR_POLL_SECONDS`, i.e. every poller tick) for the first hour, then
5× = 50s. Expected peak error ~0.05R — roughly 6× better, enough to resolve a 0.3R trail.

## Storage cost, measured not guessed

`dbstat` over `position_excursion_samples`: 2,613 rows occupying 339,968 bytes =
**130.1 bytes/row**.

| position length | rows at new cadence | storage |
|---|---|---|
| 6h | 360 + 360 = 720 | 94 KB |
| 24h | 360 + 1,656 = 2,016 | **262 KB** |
| 57.5h (longest in the book) | 360 + 4,068 = 4,428 | **576 KB** |

At the current entry rate (0.33/day, ~13h median hold) that is **≈8 MB/year**, against **16 GB
free** on the volume and a 42 MB database. The old cadence produced 689 rows for that 57.5h
position; the new one produces ~6.4× more.

## It cannot slow the poller or block the trading path

Three independent reasons, each checked in the source:

1. **Nothing reads this table.** `position_excursion_samples` is written by
   `_record_excursion_sample` and read by no exit, SL, trail or breakeven logic — the module
   docstring states it and I confirmed it by grep. **Zero trading behaviour changes.**
2. **The call site is already wrapped.** `_process_position` section 1d is
   `try: _record_excursion_sample(...) except Exception as e: print(...)`. It is structurally
   incapable of raising into the exit checks below it.
3. **The work is sub-millisecond and mostly already happening.** One local SQLite
   `SELECT MAX(elapsed_s)` plus at most one `INSERT`, once per tick per open position, with at
   most one position open by `MAX_POSITIONS_PER_SIDE=1`. The `SELECT` already ran on *every*
   tick before this change — the only delta is that the `INSERT` now fires on most ticks instead
   of one in thirty.

**Nothing is backfilled.** The 18 closed positions keep their coarse sampling; from here every
position is worth more than the eighteen behind it.

---

# §2 — CHANGE 2: PARTIAL REALISATION AT +1R, ONE THIRD, TRAIL UNCHANGED

## 2.1 `config.py` — the flags and the recorded basis

```diff
 BREAKEVEN_LOCK_MARGIN_PCT  = 0.0005  # BE target = ... 0.0020 (0.20%); clean BE = small win.
 
+# ── Partial realisation at the +1R arm (2026-08-01, SOL-only, PAPER) ──────────────
+# Realise PARTIAL_AT_ARM_FRACTION of the position at the moment the breakeven lock
+# arms (+1R). The REMAINDER rides the IDENTICAL contract — same TRAIL_MULT_ATR, same
+# BE stop, same water_mark — so this can shave a runner's tail but can NEVER truncate
+# it. That bounded worst case is the whole reason this lever was chosen.
+#   [... basis: 2.5 == SL_BUFFER_ATR so callback is exactly 1.00R; §3 substitution
+#    result 50%/39%; runners untestable at n=3; 1/3 as the milder intervention ...]
+# ⚠️ THE PARAMETERS ARE PLACEHOLDERS CHOSEN FOR MILDNESS, NOT FINDINGS. Do not retune
+# them on the current three positions. Retune only at ~15 armed positions WITH path
+# data at the new excursion cadence. If TRAIL_MULT_ATR is ever narrowed, this fraction
+# MUST be re-tuned in the SAME pass — never added on top (the substitution result).
+PARTIAL_AT_ARM_ENABLED  = True
+PARTIAL_AT_ARM_FRACTION = 1.0 / 3.0   # fraction of size realised at the +1R arm
```

## 2.2 `main.py` — five additive columns, same idempotent idiom already in use

```diff
             ('recheck_status',           'TEXT'),
+            # Partial-at-arm (2026-08-01). One realisation of PARTIAL_AT_ARM_FRACTION
+            # at the +1R breakeven arm; the remainder keeps the identical contract.
+            # partial_at is the idempotency key (the UPDATE guards on it being NULL),
+            # so at most ONE partial can ever be booked per position. Legacy rows stay
+            # NULL and behave exactly as before — nothing is backfilled.
+            ('partial_size',             'REAL'),
+            ('partial_price',            'REAL'),
+            ('partial_pnl',              'REAL'),
+            ('partial_fees',             'REAL'),
+            ('partial_at',               'TEXT'),
         ):
             if col not in vp_cols:
                 conn.execute(f"ALTER TABLE virtual_positions ADD COLUMN {col} {ddl}")
```

## 2.3 `virtual_trader.py` — the engine

**a) import**

```diff
     MAX_POSITIONS_PER_SIDE, ENABLE_BREAKEVEN_LOCK,
+    PARTIAL_AT_ARM_ENABLED, PARTIAL_AT_ARM_FRACTION,   # 2026-08-01: 1/3 realised at +1R
```

**b) new `_apply_partial_at_arm()`** — books the leg, reduces `size`, rewrites the entry fill's
fee down to its remaining share, appends an audit fill with `fee=0.0`, and stamps the five
columns under `WHERE ... AND partial_at IS NULL`:

```python
    size = float(row['size'])
    qty  = size * PARTIAL_AT_ARM_FRACTION
    rem  = size - qty
    if qty <= 0 or rem <= 0: ... return None
    entry_fee_total = sum(f.get('fee', 0.0) for f in fills if f.get('kind') == 'entry')
    entry_fee_share = entry_fee_total * PARTIAL_AT_ARM_FRACTION
    close_fee = price * qty * BYBIT_TAKER_FEE_RATE
    pnl       = (price - entry) * qty * d - entry_fee_share - close_fee
    for f in fills:
        if f.get('kind') == 'entry':
            f['fee']  = f.get('fee', 0.0) * (1.0 - PARTIAL_AT_ARM_FRACTION)
            f['size'] = rem
    fills.append({... 'fee': 0.0, 'kind': 'partial', 'realised_fee': ..., 'realised_pnl': pnl})
    ... "UPDATE virtual_positions SET size=?, fills_json=?, mgmt_state_json=?, partial_size=?,
         partial_price=?, partial_pnl=?, partial_fees=?, partial_at=?
         WHERE id=? AND status='open' AND partial_at IS NULL"
```

**c) call site — inside the existing breakeven block, no new trigger:**

```diff
             _apply_breakeven(vpos_id, be_price, mgmt_state)
             sl_price   = be_price
             be_applied = True
+            # Fires ONCE, right after the BE stop is parked and BEFORE this tick's
+            # SL/trail checks — so if the stop or trail also triggers on this same
+            # tick, close_position re-reads the row and closes the already-REDUCED
+            # size. Double-wrapped: a failure here must never touch the position.
+            if PARTIAL_AT_ARM_ENABLED and not mgmt_state.get('partial_done'):
+                try:
+                    _rem = _apply_partial_at_arm(vpos_id, row, last, mgmt_state)
+                    if _rem is not None and send_tg: ... 🔻 VIRTUAL partial ...
+                except Exception as _pe:
+                    print(f"...[PARTIAL] failed vpos={vpos_id} (non-fatal, position untouched)...")
```

**d) `close_position` — the accounting fold-back:**

```diff
     total_fees = entry_fee + close_fee
     net_pnl    = gross_pnl - entry_fee - close_fee
+    # Fold back any partial-at-arm leg. The arithmetic above is on the REDUCED size
+    # carrying only the REMAINING entry-fee share, so adding the partial's realised
+    # pnl/fees here — and only here — reconstitutes the whole-position totals exactly
+    # once. Keeping net_pnl whole is what lets every existing reader (optimizer
+    # pairing, loss-streak and daily-loss gates, PEO, cumulative equity, R-multiples
+    # against the untouched initial_risk_usdt) stay correct without being changed.
+    partial_pnl  = float(row['partial_pnl']  or 0.0) if 'partial_pnl'  in row.keys() else 0.0
+    partial_fees = float(row['partial_fees'] or 0.0) if 'partial_fees' in row.keys() else 0.0
+    net_pnl    += partial_pnl
+    total_fees += partial_fees
```

## 2.4 Why the accounting is built this way

`virtual_positions.net_pnl` must keep meaning **"total realised PnL of this position"**. Every
downstream reader assumes it: the optimizer's open/close pairing, the loss-streak and daily-loss
risk gates, `_cumulative_closed_pnl`, the Post-Exit Observatory, and every R-multiple in these
reports. Splitting a position into two legs is exactly the kind of change that quietly turns one
column into two different quantities — the §0.2 defect class I catalogued this morning — so the
whole design is arranged to avoid creating a new one:

- the entry fee is charged **exactly once** across the two legs (rewritten down here, folded back
  there);
- `initial_risk_usdt` is **not touched**, so R stays comparable to all 18 prior positions;
- `partial_at IS NULL` in the `WHERE` makes the booking idempotent at the DB layer, independent
  of the in-memory `mgmt_state` guard.

## 2.5 Proved by execution, not by algebra

Run against a **throwaway copy** of the DB, exercising the real `_apply_partial_at_arm` and
`close_position`:

```
LONG:  arm@76.95 exit@76.39  remainder=87.6000 (expected 87.6000)
  row.net_pnl      = +58.17367080
  independent calc = +58.17367080   diff=-7.11e-15
  row.total_fees   = 11.03032920
  true total fees  = 11.03032920   diff=+0.00e+00   <- entry fee charged ONCE
  idempotency: second call -> None

SHORT: arm@75.15 exit@75.71  remainder=87.6000 (expected 87.6000)
  row.net_pnl      = +58.24979520
  independent calc = +58.24979520   diff=-7.11e-15
  row.total_fees   = 10.95420480   diff=+0.00e+00

CONTROL (never armed, no partial):
  net=-280.21411350 vs pre-change formula -280.21411350   diff=+0.00e+00
```

Both directions reconcile to float epsilon; the entry fee is charged once; the booking is
idempotent; and **a position that never arms is byte-identical to the old behaviour** — which is
the guarantee that matters for the 12-of-18 that never reach +1R.

## 2.6 Known limitation accepted at ship time

`_execute_armed_exit` in `main.py` recomputes its own `realized_pnl` from the close result's
`amount`, which after a partial is the **remainder** size. On a 15m-armed-exit close, that path's
Telegram card and its own `trades` row therefore understate by the partial leg.
**`virtual_positions.net_pnl` and the `VIRT-CLOSE` trades row are whole and correct** — those are
what all analysis reads. Touching the 15m armed exit was explicitly out of scope, so this is
recorded rather than fixed.

---

# §3 — PRE-REGISTRATION, WRITTEN BEFORE THE FIRST FILL

SOL had no open-items file; one was created at
`/mnt/volume_nyc1_1780480650620/mercury-sol/OPEN-ITEMS-SOL.md`, carrying a header stating that it
is the *working* copy and that the dated report is the record — the stale-canon trap from
2026-07-30 applies here too.

Registered at **15:36 UTC**, with **no open position** and none since 2026-07-30 12:03:

- **Expected:** on the three simulated positions the partial adds **+0.852R** (+0.429R →
  +1.281R). Per position: vpos 15 +0.140→+0.426, vpos 17 +0.004→+0.333, vpos 21 +0.285→+0.522.
- **The parameters (⅓, +1R) are PLACEHOLDERS chosen for mildness, not findings.** Retune only at
  **~15 armed positions WITH path data at the new grid cadence** — not on the current three.
- **Review point:** after **10 armed positions** under the new contract, compare realised
  giveback-from-peak against the **1.00R** the old trail delivered, and re-rank partial vs
  narrower trail with the runner risk finally testable. At ~1 armed position per 9 days that is
  roughly 90 days out.
- **The substitution result stands:** if `TRAIL_MULT_ATR` is ever narrowed, this fraction **must
  be re-tuned in the same pass, never added on top**.

---

# §4 — SCOPE HELD

Verified unchanged at runtime after the restart:

| | value | |
|---|---|---|
| `TRAIL_MULT_ATR` | 2.5 | unchanged |
| `SL_BUFFER_ATR` | 2.5 | unchanged |
| `TRAIL_ARM_FIX_ENABLED` (arm point) | True → arm = `SL_BUFFER_ATR × atr` = +1R | unchanged |
| `ENABLE_BREAKEVEN_LOCK` | True | unchanged |
| `EXIT_CONFIRM_TF` (15m armed exit) | '15m' | unchanged |
| `HTF_CASCADE_ENABLED` | True | unchanged |
| `CONFLUENCE_SCORE_THRESHOLD` | 2.0 | unchanged |
| `AI_ADVISOR_DRYRUN` | False | unchanged |
| `OBSERVATION_MODE` | **True (PAPER)** | unchanged |

Diff sizes: `config.py` 47 changed lines (mostly the recorded basis), `main.py` **10**,
`virtual_trader.py` 103 (78 of them the new function and its docstring).

---

# §5 — VERIFICATION AFTER THE DELIBERATE RESTART

| check | result |
|---|---|
| service active | ✅ `active`, `NRestarts=0` since restart |
| worker forked after restart | ✅ master **1101824** @ 15:37:56, worker **1101944** @ 15:38:11 |
| runtime matches edited files | ✅ the **live DB now carries `partial_size/price/pnl/fees/at`** — only the edited `main.py` migration can have created them |
| flags live in-process | ✅ `EXCURSION 10/3600`, `PARTIAL True 0.333333`, `OBSERVATION_MODE True` |
| poller cadence | ✅ `poller started in pid 1101944 (interval=10s)` |
| tracebacks | ✅ **0** since restart |
| boot sequence clean | ✅ `[SMART-CLEANUP] No open positions`, `[AP] clean boot`, `[VPOS-RECONCILE] no open paper positions at boot — clean` |
| Tor → Bybit | ✅ HTTP **200** in 0.83s via `socks5h://127.0.0.1:9050`; `tor.service` active |
| OKX book direct | ✅ HTTP **200** in 1.08s |
| full pipeline alive post-restart | ✅ webhook → `Context recorded` → `HTF_WOULD_PASS` → `[ENRICH] vol_snapshot written row=14969` at 15:40 |
| open position | ✅ **none** (0 open, 18 total, max id 24 — unchanged) |

## Titan untouched

| | |
|---|---|
| `titan.service` | `active`, MainPID **1064304** (started 13:08, before this session), `NRestarts=0` |
| working tree | `git status --porcelain` **empty** — clean |
| HEAD | `3316e8a`, unchanged |
| `.py` files modified today | **one**: `risk_manager.py`, mtime **13:04:17** — committed at 13:07:10 as part of `3316e8a` by an **earlier session**, before this one began (~14:22) and long before the first SOL edit (15:31). `git diff HEAD` for it is empty. |
| other files touched today | `oi_cache.json`, `trades.db`, `healthcheck_state.json` — Titan's **own runtime artefacts**, written by the running bot itself |

Nothing under `/root/titan-bot` was read for parameters or written by this work.

---

# §6 — 🔴 A MISTAKE I MADE, AND THE CLEANUP

**What happened.** To prove the partial accounting I ran the real functions against a throwaway
copy of the database, redirecting `virtual_trader.DB_PATH` to `/tmp/sol_partial_test.db`. That
was not sufficient isolation. `close_position` calls the Post-Exit Observatory hook
`_peo_on_real_close`, and **`post_exit_observatory.py` holds its own module-level
`DB_PATH = '/mnt/.../trades.db'`** — it does not read the caller's. So three synthetic
`TEST/USDT` rows were written into the **live** `post_exit_observatory`, and after the restart
the PEO tick loop began trying to price a symbol that does not exist:

```
price fetch failed TEST/USDT after 3 tries (+OKX fallback): bybit does not have market symbol TEST/USDT
```

**How it was caught.** In the post-restart journal sweep, in the same output where I was checking
for tracebacks. It was not reported by anything.

**Cleanup, verified.** Backed the DB up to `trades.db.bak_pre_testcleanup_20260801` first, then:

```
peo_TEST_left=0
peo_total=21            <- all 21 real rows intact
drift_orphans=0         <- no orphaned child rows
real_vpos_rows_intact=21
```

Last `TEST/USDT` log line **15:39:23**; cleanup committed **15:39:32**; **0 occurrences in the
75 seconds after**, and 0 errors. The live `trades`, `virtual_positions`,
`position_excursion_samples` and `skip_attribution` tables were never touched by the test — only
`post_exit_observatory`, and only those three rows.

**The lesson, which is general:** redirecting one module's `DB_PATH` does not isolate a test when
a **hook it calls owns its own path**. Isolation has to be verified at every module the call
graph reaches, not just the one under test. This is the same shape as the defects catalogued in
the 14:46 §0.2 — a second writer nobody accounted for.

---

# §7 — WHAT HAPPENS NEXT, AND HOW IT WILL BE VISIBLE

Nothing is live to observe yet: **there is no open position**, and at 0.33 entries/day the next
one is not due for roughly three days. On the next entry that reaches +1R the journal will show:

```
[PARTIAL] vpos=N realised 0.3333 (<qty>) @ <price> pnl=<+/-> fees=<f> — remainder <rem> rides the UNCHANGED trail
```

followed at close by `CLOSE vpos=N ... [incl. partial pnl=... fees=...]`, and a
`🔻 VIRTUAL partial` card in Telegram. The excursion grid is verifiable at that same moment: the
first hour of that position should carry ~360 samples instead of ~15.

**Neither change can be confirmed by execution until then.** What is confirmed now is that the
flags are loaded in the running worker, the migration ran against the live database, the
accounting reconciles to float epsilon in both directions on a throwaway copy, a position that
never arms is byte-identical to the old behaviour, and the service is clean.

---

*Snapshots for rollback (SOL is not a git repo):
`config.py.bak_partialarm_excursiongrid_20260801`,
`main.py.bak_partialarm_excursiongrid_20260801`,
`virtual_trader.py.bak_partialarm_excursiongrid_20260801`, plus
`trades.db.bak_pre_testcleanup_20260801`. Rollback is `cp` the three files back and
`systemctl restart mercury-sol.service`; the five DB columns are additive and harmless if the
code is reverted. Basis:
`reports/2026-08-01-1524-sol-exit-contract-simulated-current-trail-provably-wrong-rep.md`.*
