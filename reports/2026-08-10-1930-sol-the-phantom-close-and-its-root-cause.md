# sol-the-phantom-close-and-its-root-cause

_2026-08-10 19:30 UTC_

---

# §1 APPLIED — the phantom row is labelled, not deleted, and `SUM(pnl)` is exactly $1.455432 lighter. **§2 IS ON DISK AND NOT LOADED: it needs a restart, and vpos 32 is open with an armed exit, so I have STOPPED.**

```
§1  row 17340   pnl=NULL, status='closed_unrecorded_pnl'   ✅ LIVE, no restart needed
    SUM(pnl)    −21.058101  →  −19.602669   = +1.455432 EXACTLY
    pair_trades 24 pairs before  →  24 pairs after  → 🔴 BYTE-IDENTICAL
§2  root cause  main.py +69 −0 · virtual_trader.py +71 −4   🔴 ON DISK, NOT LOADED
§3  RESTART REQUIRED — NOT TAKEN. Your call.
§4  the gate has NOT fired. Nothing has reached the entry path. Plainly stated in §4.
HARNESS: 25 ✅  0 ❌  LEAKS 0
```

Prior: [19:00 — the book gate is armed](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-10-1900-sol-the-book-gate-is-armed.md) (§8 is what this discharges)

---

## 1. THE PHANTOM ROW — APPLIED

```
BEFORE  17340  2026-08-10 18:25:19  close_long  75.9  1.2  pnl −1.455432  status executed
AFTER   17340  2026-08-10 18:25:19  close_long  75.9  1.2  pnl NULL       status closed_unrecorded_pnl
```

`status='closed_unrecorded_pnl'` is the state `main.py:399` already writes on the reconciler's own
can't-substantiate branch — **no new vocabulary**. The `error` column now carries the full account
of what the row is, so the next audit reads the explanation off the row itself rather than
reconstructing it.

### (a) 🔴 NOT DELETED

```
SELECT COUNT(*) FROM trades WHERE id=17340   ->   1
```

The row is still there, labelled. A deleted row is invisible to the next audit; a labelled one says
what happened. The standing rule against unrequested deletion holds.

### (b) Both consequences confirmed

```
SUM(pnl) over rows since 2026-08-07:
    BEFORE   −21.058101
    AFTER    −19.602669
    delta    +1.455432        🔴 EXACTLY the double-count, to six decimals
```

**And `optimizer.pair_trades` is byte-identical** — run against the pre-change backup and the live
DB, both through the real function:

```
pairs BEFORE the row fix: 24
pairs AFTER  the row fix: 24
🔴 PAIRING IDENTICAL: True        differences: NONE

vpos 31 still pairs:  open=17201  ->  close=17296 (sl_triggered_long, −1.4554319999999856)
17340 appears as a close in any pair:  False   (before AND after)
```

🔶 **And it is now protected by two mechanisms where it had one.** Before, 17340 was excluded only
because `pair_trades` pops the open on the *first* close row and the second finds nothing. Now the
`and r['pnl'] is not None` guard on the close branch excludes it outright. **The ordering
protection was doing real work and is no longer the only thing standing between us and a
double-paired trade.**

### (c) `virtual_positions` untouched

```
26 rows before, 26 rows after — IDENTICAL (full-table comparison, not spot checks)
vpos 31  net_pnl −1.45543199999999  close_reason sl  status closed
```

It was always right. Nothing in this pass wrote to it.

**Backup:** `trades.db.bak_phantomrow_20260810_1845` (52,015,104 bytes), taken before the update.

---

## 2. THE ROOT CAUSE — BUILT, PROVEN, NOT LOADED

### (a) Every close route, and which cleared the registry

| route | clears `active_positions`? | |
|---|---|---|
| `main._execute_close_position` (:3008) | ✅ **always did** | main's own close path — exit signal, timeout, sl_failsafe, trend reversal, armed exit all funnel here |
| `_monitor_positions` SL/trail detect (:5851) | ✅ **always did** | 🔴 but the monitor is **RETIRED** — `[MONITOR] RETIRED — the paper engine is the single position manager in BOTH modes`. Dead code clearing a registry nothing else clears. |
| boot AP reconciler (`_remove_active_position`, :474) | ✅ did — **after fabricating the close** | it removes the row *as the last act of booking a phantom*. Cleaning up correctly after doing the wrong thing. |
| 🔴 **`virtual_trader.close_position`** | ❌ **NEVER** | **every close since Phase 2 goes through here** — sl, trail, partial-then-close, exit_signal, external/venue close via `_book_exchange_close`. This is the gap. |

**Now fixed at the seam that already exists.** `set_live_adapter` gains `unregister_fn` — keyword-only
with a default, the same idiom `funding_fn` used on 2026-08-09 — and `close_position` calls it:

```python
if not _is_paper(row) and _live_unregister is not None:
    try:
        _live_unregister(row['symbol'], position_side)
        print(f"{LOG_PREFIX}[REGISTRY] cleared active_positions for …")
    except Exception as _unreg_err:
        …
```

**It respects the invariant rather than breaking it.** `virtual_trader` still never imports main and
never touches `_active_positions`; main injects the cleaner, exactly as it injects the close,
partial, move-stop, position-state, book-close and funding executors.

**Placed after the double-close guard, deliberately:**

```
✅ 🔴 the clear sits AFTER the rowcount==1 guard (:741 < :788) — a lost race returns
     before it and cannot clear a registry row belonging to a position it did not close
✅ the clear fires only when `not _is_paper(row)` — a paper close never touches the registry
✅ it is wrapped in try/except — it can never raise into the poller
```

### (b) 🔴 WHAT HAPPENS IF THE CLEAR FAILS — and yes, it alerts

**The position is still closed.** The ledger UPDATE and the close row are already committed by the
enclosing transaction; this is bookkeeping, not money. So it must not raise back into the poller —
that would leave a correctly-closed position throwing an exception on the tick.

**But the consequence is not nothing: the stale row survives and the next boot repeats the
phantom.** So it logs loudly *and* sends an alert:

```
[REGISTRY] 🔴 FAILED to clear active_positions for LONG SOL/USDT:USDT (vpos=N): … —
the position IS closed and the ledger IS correct, but the stale registry row survives
and the NEXT BOOT COULD BOOK A PHANTOM CLOSE. main's reconciler cross-checks the
ledger, so this is a warning, not a corruption.

⚠️ Registry clear FAILED — LONG SOL/USDT:USDT vpos=N
   position closed correctly; stale active_positions row left behind. Boot reconcile
   is guarded, but clear it before the next restart.
```

**And the belt makes a failed clear survivable.** `_reconcile_closed_position` now asks the ledger
*before* inventing a close:

```
✅ 🔴 ORDER: ledger check :362  <  "[AP] RECONCILED" log :375  <  close-row insert :404
```

If `virtual_positions` already holds a **closed** row for that side that closed at or after the
registry row's `entry_time`, the position did not close during downtime — we merely never cleaned
up — and the reconciler drops the stale row **without writing a second close**.

🔴 **Replayed against a copy of the real database, on the real rows:**

```
✅ the belt FINDS vpos 31's close and would REFUSE the phantom:
     {'id': 31, 'closed_at': '2026-08-10T15:21:44.727354+00:00',
      'close_reason': 'sl', 'net_pnl': -1.4554319999999856}
✅ it does NOT fire for vpos 32 (still OPEN) — a REAL downtime close still reconciles
✅ it does NOT fire when the registration is NEWER than the close — no false suppression
✅ entry_time=None -> None — it never suppresses blindly
```

**It fails to the OLD behaviour on any error**, and that direction is argued rather than assumed:
failing to record a *real* downtime close is the more dangerous of the two failures, so a DB blip
returns `None` and the reconciler proceeds exactly as it did before 2026-08-10.

### (c) 🔴 WHY THE AP PATH WAS MISSED — the "fixed in one place of two" shape

`main.py:5395` names this class and fixed it — *"PHASE 3 (5a) — ONE CLOSE, ONE ROW"* — for the
**armed-exit** path, by leaving `pnl` NULL so the duplicate leaves every `SUM(pnl)` reader and
`optimizer.pair_trades`.

**It was scoped to a duplicate the author could see.** The armed-exit duplicate is *synchronous and
same-session*: two rows appear seconds apart, in one journal, on one screen. **The AP duplicate is
separated by a process boundary and by hours** — the first row is written by the engine at 15:21,
the second by a different process at 18:25 after a restart the author was not performing. It is the
same defect with a latency, and latency is what hid it.

**Is any OTHER path exposed?** Enumerated above: the four close routes are now either clearing the
registry or protected by the ledger belt. The reconciler's *other* branch (`fetch` failed) already
writes `pnl=NULL` and was never able to double-count. **The remaining asymmetry worth naming: the
retired monitor at :5851 still clears a registry nothing else fills.** It is dead code and this pass
does not touch it — same reasoning as the superseded wall gate, one risk at a time.

### (d) Are there other stale rows right now? **No.**

```
active_positions          |  virtual_positions (open)
SOL/USDT:USDT SHORT       |  vpos 32 SHORT open 1.3 @ 76.18
entry_time 15:15:45.749   |  opened_at  15:15:33.975
────────────────────────────────────────────────────────
1 row, 1 open position, they match. ZERO stale registrations.
```

The LONG row that caused the phantom was consumed by the boot reconcile at 18:25:19 — it did the
wrong thing and then cleaned itself up, which is why the table is clean now and why the defect
would have stayed invisible until the *next* restart after the *next* engine close.

---

## 3. 🔴 THE DEPLOY QUESTION — A RESTART IS REQUIRED. I HAVE STOPPED.

**§1 landed with no restart** — it is a DB row, and every reader queries the table live. Confirmed
against the running process: the update is visible now.

**§2 cannot land without one.** Both halves are module-level code held in memory by the worker
since 18:25:21:

- `virtual_trader.close_position` — the clear only exists in the function object the poller is
  already executing;
- `main.set_live_adapter(...)` — the adapter is wired **once at boot**, so `unregister_fn` cannot
  reach `virtual_trader` without a boot;
- `_ledger_close_after` — the reconciler only runs at boot anyway.

```
ON DISK, NOT LOADED:
  main.py           +69  −0     (the belt + the adapter wiring)
  virtual_trader.py +71  −4     (the adapter contract + the clear)
  🔴 exactly 4 deleted lines in the whole change, all four the set_live_adapter
     signature/docstring/globals/print lines being extended in place
```

**vpos 32 is open with an armed exit** (SHORT, armed 18:00:15, expires 2026-08-11 00:00:15). **I am
not restarting. It is your call, and it can wait** — the defect needs an engine close *and then* a
restart to bite, and the belt means even that costs a dropped stale row instead of a phantom once
loaded.

🔶 **Stated so it is not a surprise:** until §2 loads, a close of vpos 32 will again leave a stale
SHORT registration, and the restart after that would book a phantom short close. **That is the exact
sequence to avoid** — either load §2 before vpos 32 closes, or check `active_positions` before the
next restart.

---

## 4. HAS THE GATE FIRED? **NO — AND NOTHING HAS REACHED IT.**

### (a) Zero, on both instruments

```
[BOOK-GATE] journal lines since 18:25:21 : 0
rows with a non-empty book_gate_clause   : 0
```

### (c) 🔴 THE PLAIN REASON: the market has produced no signal that reaches the entry path

Every row since arming, in full — there are only seven:

```
17341  18:30:19  no_trend
17342  18:35:09  entry_suppressed_armed     🔴 see below
17343  18:40:07  no_trend
17344  18:40:07  no_trend
17345  18:40:07  no_trend
17346  18:45:04  no_trend
17347  18:50:07  no_trend
```

**Six died at the state machine's trend gate**, hundreds of lines before the score gate, the risk
gate, the book fetch or the advisor. **One died at `entry_suppressed_armed`** — a 5m counter-entry
refused because *vpos 32's exit is armed*, so the bot will not open a hedge against a position it is
preparing to exit.

🔴 **That second one is a concrete, nameable reason and not an idle market:** while an exit is armed
on the open SHORT, 5m counter-entries are suppressed upstream of everything. **The gate is not
unproven because of any doubt about the gate — it is unproven because 25 minutes of quiet market
plus one armed exit have sent nothing down the path it sits on.**

### (b) The telemetry path proven end to end — and labelled as a LAB proof, not a production row

You asked for a real row with the six columns populated. **There is no such production row yet, and
I will not manufacture one.** What I can prove is that the write works, using a **real production
book** (vpos 32's own entry, row 17289) through the **real `book_gate.evaluate()`**, written by the
**exact UPDATE `main.py` performs**, into a **copy** of the database:

```
evaluate() on the REAL book of row 17289:  refuse=True  clause=B
  opp_mult 13.1 · opp_pctl 17.9 · opp_dist_pct 0.53834 · lean 0.34310 · n_supporting 6

the six columns after the write (🔴 LAB COPY, NOT PRODUCTION):
  book_gate_clause          'B'
  book_gate_opp_mult        13.1
  book_gate_opp_pctl        17.9
  book_gate_opp_dist_pct    0.5383403361344493
  book_gate_lean            0.34309999999999996
  book_gate_n_supporting    6
```

**Every column accepts its value and the clause round-trips.** The first production row will appear
the moment a signal reaches the entry path; **I am not calling the telemetry live-proven until one
does.**

---

## PROOF BY EXECUTION — 25 ✅ / 0 ❌, SEARCHED BY DIRECTORY

```
LAB: full tree copy + §2; every PRODUCTION-DIRECTORY literal rewritten. residual: 0
LOCK before the first import: sqlite3.connect + open(w/x/a/+) raise on PROD or /root/titan-bot
```

```
✅ set_live_adapter gains unregister_fn (keyword-only, default None)
✅ registering the ORIGINAL five leaves it None — back-compatible
✅ the clear is guarded by `not _is_paper(row) and _live_unregister is not None`
✅ 🔴 it sits AFTER the rowcount==1 double-close guard
✅ wrapped in try/except — can never raise into the poller
✅ a failed clear ALERTS, and the log says exactly what it costs
✅ 🔴 ORDER: ledger check < RECONCILED log < close-row insert
✅ 🔴 the belt FINDS vpos 31's close and would REFUSE the phantom
✅ it does NOT fire for the open vpos 32, nor on a newer registration, nor on entry_time=None
✅ §1 re-verified against PRODUCTION: 17340 pnl NULL, status closed_unrecorded_pnl, ROW STILL EXISTS
✅ the real close row 17296 untouched · virtual_positions vpos 31 untouched
✅ main.py / virtual_trader.py: LAB differs from PRODUCTION — §2 NOT applied
✅ 🔴 /root/titan-bot git-CLEAN at 897850b — NOT TOUCHED       LEAKS: 0
```

---

## STATE

```
mercury-sol   active · master 319767 / worker 319915 · since 2026-08-10 18:25:01 · NRestarts=0
              🔴 NOT RESTARTED IN THIS PASS
🔴 vpos 32    OPEN · SHORT 1.3 @ 76.18 · SL 77.32 · UNTOUCHED
              exit_pending SHORT armed 18:00:15, expires 2026-08-11 00:00:15 — untouched
book gate     ARMED (ENABLED=True, DRYRUN=False) · 0 refusals · 0 signals reached it
APPLIED       trades row 17340 only — pnl NULL, status closed_unrecorded_pnl, error explains it
ON DISK       main.py +69/−0 · virtual_trader.py +71/−4 — 🔴 AWAITING YOUR RESTART
backups       trades.db.bak_phantomrow_20260810_1845 (pre-update, 52,015,104 b)
              config/main/skip_attribution .bak_bookgate_20260810_1900 (from the 19:00 pass)
active_pos    1 row (SHORT), matches the one open position — ZERO stale registrations
titan         HEAD 897850b · git clean · NOT TOUCHED
```

**The phantom is labelled and cannot be counted twice. The cause is built and waits on you.**
