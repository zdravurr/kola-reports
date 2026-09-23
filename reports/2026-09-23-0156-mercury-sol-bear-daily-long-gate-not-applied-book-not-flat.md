# BEAR-DAILY LONG GATE — **NOT APPLIED. THE BOOK IS NOT FLAT. STOPPED.**

**2026-09-23 01:56 UTC · Mercury-SOL · NOTHING WRITTEN · Titan untouched**

`openitems_guard` → **exit 0** (titan-bot HEAD `f53d048`), run first.

---

## 🔴 RESULT: STOPPED AT STEP 3a. POSITION #50 (LONG) IS STILL OPEN.

The brief says: *"Position #50 (LONG) was open at 23:30 — if it still is, say so and STOP."* It still is.

| check | result |
|---|---|
| `virtual_positions` open | **1** — **#50**, LONG (`buy`), opened 2026-09-22 18:00:43 UTC, fill **117.82**, stop **114.79**, size 0.8, `is_paper=0` (live) |
| `active_positions` | **1** — SOL/USDT:USDT LONG, entry 117.82, entry 2026-09-22 18:00:46 |
| `exit_pending` | 0 |
| bot heartbeat 01:53:15 UTC | `open=1 mode=LIVE pid=3077058` |
| venue read | **not done**. The DB and the bot both show the position open, so reading Bybit could not make the book flat. |

The last closed position was #49 (LONG, trail exit, 2026-09-21 16:38).

---

## WHAT WAS DONE AND WHAT WAS NOT

**Done (read-only):**
* `openitems_guard` → EXIT=0.
* Read the 2026-09-22-2316 report, §1–§3: the mirror measured at 0 of 5 controls, n=3 paper (#12 −1.049R, #21 **+0.285R winner**, #26 −1.085R), live bear-long cell empty.
* Read the twin: canon `§BULL-DAILY-SHORT-GATE-2026-09-17` (`OPEN-ITEMS-SOL.md:2142`) and its 2026-09-17-1659 apply report. The shape to mirror is confirmed: `main.py:5374` site, `_bull_daily_short_halt`, `bull_daily_blocked` status, `BULL_DAILY_SHORT_BLOCK_ENABLED/DRYRUN`, 20-path fail-open proof, AST walker over `TRACKED_STATUSES`.

**Not done: every write in §1 and §3, plus the replay and rate in §2:**
* no `.bak`, no edit to `config.py` / `main.py` / `skip_attribution.py` / `OPEN-ITEMS-SOL.md`
* no restart (`mercury-sol.service` active since 2026-09-17 16:55:13, not restarted)
* no canon entry and no cohort boundary, because nothing changed
* the §2 replay and refusal-rate count were **not rerun**. The 09-22 §3 figures stand as the last measurement: paper refuses #12, #21 (winner), #26; live none; 0 live-era bear rows since 2026-08-08.

---

## 🔴 WHAT THIS MEANS FOR THE 100× LONG QUESTION

**The gate is not live.** Until it is applied, a LONG into a BEAR daily is **still admitted**. Size has not changed, so today's exposure is unchanged. **Do not raise LONG size before this gate is applied.** The reason for the gate was to remove that population *before* any size increase.

## NEXT STEP

Re-run the same brief once #50 has closed and `virtual_positions` open = 0. The spec above is ready to apply as written.

---

## CONFIRMATION

| | |
|---|---|
| writes to Mercury-SOL | **0** |
| `.bak` taken | not needed: nothing written |
| orders placed / cancelled | **0** |
| restarts | **0** |
| Titan | **UNTOUCHED** (`titan.service` NRestarts=0) |
| files written | this report only |
