# titan-failed-read-class-handoff-to-fresh-session

_2026-09-21 18:55 UTC_

---

# Titan: the failed-read class is NOT closed yet. The last two paths were deliberately NOT started in the expensive session. Run the same brief in a FRESH session.

**2026-09-21 · titan-bot HEAD `07f9025` · canon `8423b5d` · Titan LIVE, real money · Mercury-SOL not touched · no code, DB or order touched by this note**

## Why nothing was done this turn

Your session-cost hook fired at ~363K context per turn, rising quadratically. It said to end the session at the nearest finished point and start a new one, *now*. Your brief itself begins "FRESH SESSION, no prior state".

This pass (two fixes, a new contract, re-running four contracts as two users, a flat restart, the canon, a report) is ~40 turns. A fresh session does the same work at a fraction of the cost. **So I stopped before touching anything.**

## State as last verified (2026-09-21 18:51 UTC, not re-checked for this note)

- Titan runs `07f9025`, loaded by the 18:49:23 UTC from-flat restart. Boot `RECONCILE-XDB ✅ 0/0`, 0 errors, NRestarts 0, MainPID 4004539.
- Flat: 0 open rows, 0 `exit_pending`; BingX 0 positions and 0 orders on both probes.
- Everything is committed (`07f9025` in `/root`) and pushed (canon `8423b5d`). Nothing is half-applied, and no `.bak` or test was started for this pass.

## What is still open: the two remaining failed-read paths (from the 19:00 report §2e)

1. **`virtual_trader._run_recheck_tier`**, the post-entry critical close. **The more dangerous one; do it first.**
   - **The defect is the order.** It writes `recheck_status='closed_critical'` and sends "🛑 Post-entry T+Ns — EMERGENCY CLOSE" *before* `_do_close(... 'post_entry_critical' ...)`, and it ignores that call's return.
   - **On a failed read:** the close aborts, and the tier never re-fires. An emergency close is announced and silently does not happen.
   - **Your ruling for the fix:** mark and announce only after the outcome is known.
     - FLAT: today's behaviour.
     - OPEN: retry.
     - UNKNOWN, or still open: do not mark, leave the tier able to re-fire, send a hands-required alert, and **trip `_UNSAFE_STATE`**.
2. **`virtual_trader._advisor_close`**, the `ai_exit` path.
   - **Today:** its `if res is None:` branch logs "no live position to close — left for passive-fill reconciliation, NOT retried". On a failed read, the advisor's close is dropped for up to an hour, and the log states a false fact.
   - **The fix:** the same shape as `07f9025`'s fix for the 5m advisor close, with **no breaker** (the exchange stop is in place, and the next verdict retries).
   - **Also check:** whether any ledger close (vpos 101, 104, 105, 106, 108) has a "no live position to close" line near it in the journal.

## Everything the fresh session needs

- **Basis:** `reports/2026-09-21-1900-titan-vpos-109-out-armed-exit-never-dropped-on-failed-read.md` §2e, and canon `§0.FAILED-READ-CALLERS`.
- **Contract pattern to copy:** `titan-bot/tests/test_close_not_dropped_on_failed_read.py`.
  - Real code is lifted from source by AST.
  - Only the exchange and sleep are faked.
  - `TITAN_PEO_AUTO_INIT=0` is set, and every `trades.db` connect is redirected to a scratch file.
  - It is proven with `strace -f -e trace=openat` (0 opens of the live DB).
  - The botuser leg runs on sha256-pinned copies in a `/tmp` sandbox, because `/root` is 0700.
- **The four existing contracts,** which must stay GREEN:
  - `test_vpos_fill_failed_read_is_not_flat` (19)
  - `test_failed_read_never_reports_safety` (15)
  - `test_last_callers_and_armed_exit_label` (13)
  - `test_close_not_dropped_on_failed_read` (12)
- **Helper scripts, still on disk:**
  - `/tmp/claude-0/-root/c37184bc-171f-49bf-87f9-e550e4c86636/scratchpad/venue_probe.py`: read-only BingX probes, both endpoints, Tor fallback.
  - `/tmp/claude-0/-root/c37184bc-171f-49bf-87f9-e550e4c86636/scratchpad/vals.py`: settings and advisor-prompt sha256 from source (`src`) and from the loaded `.pyc` (`pyc`).
- **Traps already hit:**
  - Importing `virtual_trader`, `post_exit_observatory` or `breakeven_worker` runs `init_db()` against the **live** `trades.db`.
  - `report_publish` truncates the file name to 60 characters, so compute the slug before pre-registering a path in the canon.
- **Memory:** `project_titan_vpos111_false_gone_alarm_failed_read_21sep.md` holds the whole chain.

**Still a candidate, not in any pass yet:** WAL for `trades.db`.
