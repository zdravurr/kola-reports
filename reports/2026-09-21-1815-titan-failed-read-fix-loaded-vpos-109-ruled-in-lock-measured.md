# titan-failed-read-fix-loaded-vpos-109-ruled-in-lock-measured

_2026-09-21 18:15 UTC_

---

# Titan: the false "POSITION GONE" alarm is FIXED and LOADED. vpos 109 is ruled into the exit-advisor ledger: 6 of 10, Σ +0.8798R, the rule does not fire. The database lock is measured: writers commit fast; the long holders are full-table scans on the webhook scoring path.

**2026-09-21 · titan-bot HEAD `7798f51` (was `f16c271`) · canon `053f5ff` · Titan LIVE, real money · Mercury-SOL not touched**
*(File dated 18:15 so its path matches the one the canon pre-registered; written and published at ~18:05 UTC.)*

`openitems_guard` at the start: **EXIT=0**. At the end, against the new HEAD and updated canon: **EXIT=0**.

---

## 0. Summary

| item | result |
|---|---|
| §1 fix | **Applied from flat and loaded** by the 17:39:09 UTC restart. The contract is **RED 7 of 19 on the old code, GREEN 19 of 19 on the patch, as root and as botuser**. AST: only `_reconcile_passive_fill` changed. Every guarded value and all four advisor prompts are identical in the loaded bytecode. Boot `RECONCILE-XDB ✅ 0 / 0`. |
| §1f other callers | Listed, **not migrated**. 🔴 **Two sit in emergency paths and would declare a possibly unprotected position safe on a failed read** (§1f). |
| §2 vpos 109 | **Ruled in.** The canon now defines the population as every live close from vpos 101 on where the advisor returned `close=True`. This **adds a negative row (−0.1699R)**. Ledger: **6 of 10, Σ +0.8798R / +$1.43**. The rule does not fire. The scan found **no other** such close in the population. |
| §3 lock | Every writer commits promptly (0 of 59 write blocks hold a lock across I/O). The long holders are **readers**: full-table scans on the webhook scoring path, **2.2–3.1 s each when the cache is cold**. Root cause: those scans combined with `journal_mode=delete` and a 5 s timeout. **WAL is named as a candidate, not switched.** |
| §3e | The −$0.1931 failsafe round trip is now in the canon (`§0.VENUE-VS-DB`), with positionId **2101906879672446978**. |
| incident | **My first contract draft opened the live `trades.db`** through two import-time `init_db()` calls. They were schema-only no-ops, and I proved the schema unchanged. The contract is now fail-closed: a kernel trace shows **0 opens** (§1a). |

---

## 1. The false-alarm fix

### 1a. Contract first: `tests/test_vpos_fill_failed_read_is_not_flat.py`

It runs the **real** code:
- `_fetch_position_state`, `_fetch_open_position` and `POS_*` are lifted out of `main.py` by AST.
- The double probe is the real `order_adapter._probe_positions`.
- `virtual_trader` is loaded from source.

Only the exchange, the fill lookup, `_do_close` and `sleep` are fakes. There are 19 checks:

| # | case | expected |
|---|---|---|
| 1 / 1b / 1c | **both probes fail**, on every attempt | NO alarm, no fill lookup, no close, row untouched. Re-probed once (2 attempts, one 2.0 s gap). One `UNKNOWN` log line. |
| 2 | unified fails, raw answers flat | UNKNOWN, no alarm |
| 3 | unified fails, raw **sees** the position | OPEN, nothing |
| 4 / 4b / 4c / 4d | **true flat on both probes** | the alarm fires once. **Telegram text and journal line are byte-identical to the `.bak`.** It still reaches `read_filled_protective_order` with the same arguments. |
| 5 | true open | nothing (new and `.bak`) |
| 6 / 6b | true flat + our stop filled | finalised through `_do_close` with the same arguments as the `.bak` |
| 7a / 7b | fail, then the re-probe says flat / open | alarm / nothing |
| 8a / 8b | paper; no stop id | returns before any probe |
| 9 | **sensitivity** | the `.bak` DOES raise the false alarm on a failed read |
| 10 | AST | only `_reconcile_passive_fill` may differ |
| 11 | the live DB | never opened |

| run | root | botuser (sha256-pinned copies in `/tmp/titan-contract-failedread`) |
|---|---|---|
| **RED**, unpatched file (sha `3b0b49d9c5d4e092`) | **EXIT=1, 7 FAIL / 12 OK**: [1] [1b] [1c] [2] [3] [7a] [7b] | **EXIT=1**, identical 7 FAIL |
| **GREEN**, patched file (sha `4184eb8ff1f59095`) | **EXIT=0, 19 / 19** | **EXIT=0, 19 / 19**, output identical to root |

**Pins, root vs botuser copy:** `virtual_trader.py` `4184eb8ff1f59095` = `4184eb8ff1f59095`; `.bak` `3b0b49d9c5d4e092` = `3b0b49d9c5d4e092`; `main.py` `00c8be297a8de922` = `00c8be297a8de922`; test `aeac207ba7882f52` = `aeac207ba7882f52`.

🔴 **What went wrong in the first draft.**
- **What happened:** `virtual_trader.py:2848` and `post_exit_observatory.py:828` both run `init_db()` **at import**, against the hard-coded live `/root/titan-bot/trades.db`. My module grep missed them. My first two root RED runs therefore opened the live DB, 6 import-time `init_db()` executions in total.
- **What those calls execute:** only `CREATE TABLE/INDEX IF NOT EXISTS` and `ALTER TABLE ADD COLUMN` inside `try/except`.
- **Proof that nothing was written:**
  - Both files predate the running process's 09-12 boot, which had already run the identical `init_db()`.
  - **All 54 ALTER-listed columns already existed** (0 missing), so every ALTER failed as a duplicate.
  - `virtual_positions` still has 44 columns, the same count read in the first session; `schema_version` 244; 45 schema objects.
- **Hardening:**
  - The contract sets `TITAN_PEO_AUTO_INIT=0`, and redirects **any** connect to a file named `trades.db` into a scratch DB.
  - Check [11] reports 2 such redirects.
  - A kernel `openat` trace of the test process shows **0 opens of `/root/titan-bot/trades.db`** on both the RED and GREEN runs.
- **Scope note:** the two existing contracts in `tests/` were not re-run; they don't load `virtual_trader`.

### 1b. The diff, as applied (your approved §6, verbatim)

```diff
--- virtual_trader.py.bak_failedread_20260921T173345Z
+++ virtual_trader.py
@@ -1154,13 +1154,21 @@
     # Is the position still on the exchange?
     try:
         import main as _m
-        pos = _m._fetch_open_position(row['symbol'], row['position_side'])
+        # F1 (2026-08-05): a FAILED read is not FLAT. The shim conflates them;
+        # 2026-09-21 it turned two BingX 109500 "system busy" replies into two
+        # false "POSITION GONE … MANUAL ACTION REQUIRED" alarms on a live vpos.
+        _state, pos = _m._fetch_position_state(
+            row['symbol'], row['position_side'], double_probe=True, attempts=2)
     except Exception as e:
         # Cannot tell -> do NOT guess. Leaving the row open is recoverable;
         # inventing a close is not.
         print(f"[VPOS-FILL] position check failed vpos={row['id']}: {e}", flush=True)
         return False
-    if pos is not None:
+    if _state == _m.POS_UNKNOWN:
+        print(f"[VPOS-FILL] vpos={row['id']}: position read UNKNOWN — not "
+              f"treated as flat, nothing done, re-checked next tick", flush=True)
+        return False
+    if _state == _m.POS_OPEN:
         return False                       # still open, nothing to reconcile
```

**The caller is unaffected.** `_process_position` already received `False` on OPEN and on the old false alarm, so on UNKNOWN it carries on managing the position exactly as before. The only behaviour change is that no alarm is raised and no fill lookup runs.

**Cost:**
- With a position open, 2 REST reads per 10 s poller tick instead of 1.
- On a failed read, one extra 2 s pause in the poller thread.

### 1c. Flat, confirmed before the restart (17:38:32 UTC)

- **DB:** 0 open `virtual_positions`, 0 `exit_pending`, 0 live `breakeven_jobs`.
- **BingX:** unified `fetch_positions` `[]`, raw `swapV2PrivateGetUserPositions` `data: []`, unified `fetch_open_orders` `[]`, raw `swapV2PrivateGetTradeOpenOrders` `orders: []`. **All four answered directly with an empty error list.**
- **Journal, last 90 s:** no webhook or entry in flight.

### 1d. `.bak`, AST, runtime values

- **`.bak`:** `virtual_trader.py.bak_failedread_20260921T173345Z`, taken **before any write** and byte-identical to the original.
- **AST:** 76 vs 76 top-level nodes; the only differing node is `_reconcile_passive_fill`. This is contract check [10].
- **Values:** read from source before the restart, and **from the loaded `.pyc` after it**, by unmarshalling the bytecode (no import). Both headers match their source (`header==source: True`). All identical:

| name | value |
|---|---|
| `SL_ATR_MULT` / `TRAIL_MULT_ATR` | 2.25 / 1.6875 |
| `EXIT_ADVISOR_DRYRUN` | **False** |
| `BOOK_GATE_ENABLED` / `BOOK_GATE_DRYRUN` | True / **False** |
| `BOOK_GATE_CLAUSE_A_ENABLED` / `_B_` | **True / False** |
| `LIVE_TRADING_ENABLED` / `ORDER_ADAPTER_LIVE` | True / True |
| `CONFLUENCE_SCORE_THRESHOLD` / `_FLAT_` | 3.0 / 5.0 |
| position size | `LIVE_FIXED_MARGIN_USDT` 30.0 × `LEVERAGE` 5 = $150 (boot banner: `sizing: margin $30 x 5 = $150 notional per entry`); `MAX_POSITIONS_PER_SIDE` 1 |
| `_ENTRY_SYSTEM` | sha256 `30c979595a4831aa` |
| `_LEARNING_SYSTEM` | sha256 `191cf5d71ebf3865` |
| `_CLOSE_SYSTEM` | sha256 `7d7707cfa2d336f7` |
| `_CLOSE_SYSTEM_RICH` | sha256 `3d709571e17ff405` |

### 1e. The restart, from flat

**Restart and boot:**
- `systemctl restart titan.service` at **17:38:44 UTC**; active **17:39:09 UTC**.
- MainPID 1572470 → **3989951**; worker **3989975**.
- **NRestarts 0 → 0.** systemd does not count a manual restart; this was the only restart.
- Boot line: `[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)`. **0 errors** at boot.

**Proof the new process loaded the patch:**
- **The patch was compiled at boot:** `virtual_trader.cpython-312.pyc` was rewritten at **17:39:16.29**. Its header equals the patched source, and in its bytecode `_reconcile_passive_fill` names `_fetch_position_state` and `POS_UNKNOWN`, **not** `_fetch_open_position`. The new log string is in its constants.
- **The other modules were read by the new process:** I reset the `atime` of five `.pyc` files to 2026-01-01 before the restart (metadata only). The boot re-stamped `main` (17:39:09.95), `config` and `claude_advisor` (17:39:11) and `order_adapter` (17:39:14).

**Since the restart, up to 17:59 UTC:** 0 `[VPOS-FILL] 🚨`, 0 tracebacks, 0 `database is locked`.

**Two things I saw and did not act on:**
- `systemctl` warned **"The unit file … of titan.service changed on disk. Run 'systemctl daemon-reload'"**. I did **not** reload, so the restart used the unit definition systemd already had loaded. Someone changed the unit file after the last reload; worth a look.
- The old master exited at 17:38:45.4, but systemd reported the unit stopped only at 17:39:09.6, 24 s later.

`openitems_guard` after the commit and canon update: **EXIT=0**.

### 1f. The other callers: NOT migrated. What their None branch does

| caller | None branch | takes an action? |
|---|---|---|
| `main.py:1357` `_execute_close_position` | returns None, so the close is aborted and no order is sent | **yes, it aborts.** It feeds the three rows below. |
| ↳ `virtual_trader.py:207` **entry failsafe** | treats None as "**nothing is exposed**": alert and return. `_UNSAFE_STATE` is **not** tripped. | 🔴🔴 **yes.** A failed read declares a possibly naked position safe. |
| ↳ `breakeven_worker.py:475` **emergency close** | sends "✅ **Emergency close executed**" whatever the result | 🔴🔴 **yes.** False success after the stop was cancelled and its recreate failed. |
| ↳ `virtual_trader._do_close` (via `market_close`) | "VIRTUAL CLOSE ABORTED … row left OPEN", retried next tick | yes, a deferral. The exchange stop stays in place. |
| `main.py:3663` `_handle_5m_close_via_ai` | treats the side as not open, so the exit consultation is skipped | yes, it skips an advisor decision |
| `main.py:3900` `_handle_exit_signal` | only reached when `engine_owns_position()` is False | **dead in live** (`ROUTING_MIGRATED_TO_ADAPTER = True`) |
| `main.py:4068` `_handle_liquidity_sweep` | sends "No open LONG — nothing to close" and returns | yes: a false message and a skipped sweep close |
| `main.py:4291` trend reversal | only reached when `engine_owns_position()` is False | **dead in live** |
| `breakeven_worker.py:425` `move_stop_with_race_guard` | after a failed cancel returns `'closed'`; the caller persists nothing, the **old stop is held**, and it retries | benign |
| `breakeven_worker.py:765` (also :692, :746) | marks the job closed and reports a passive fill | **dormant**: `breakeven_jobs` has had 0 rows ever |

**For the next pass, I recommend doing the two 🔴🔴 rows first.** They are the only callers that report *safety* on a failed read.

---

## 2. vpos 109 is ruled into `§0.EXIT-ADVISOR-RULE`

### 2a. The canon now says (verbatim, `053f5ff`)

> 🔴 **POPULATION CLARIFIED 2026-09-21 (operator's ruling): every LIVE close, from vpos 101 onward, where the advisor returned `close=True` — whatever `close_reason` the row carries.** The rule measures advisor DECISIONS; the label is bookkeeping. The armed-exit path (`[EXIT-ADVISOR-LIVE] trigger=armed_exit … close=True` → `ARMED_EXIT_CLOSE`) writes `close_reason='external'`, so **vpos 109** … was outside the letter of the old wording. 🔴 **This clarification ADDS A NEGATIVE-DELTA ROW (−0.1699R): it moves the sum AGAINST the advisor — the conservative direction, not a selection in its favour.**

### 2b. The ledger: 6 of 10, Σ +0.8798R / +$1.43. The rule does not fire.

| # | vpos | side | closed | advisor R ($) | counterfactual | cf R ($) | Δ R | Δ $ |
|---|---|---|---|---|---|---|---|---|
| 1 | 101 | SHORT | 09-01 18:00 | +0.2956 (+0.57) | trail 77 124.0 | +0.4509 (+0.87) | −0.1553 | −0.30 |
| 2 | 104 | LONG | 09-09 08:30 | +0.5757 (+0.79) | sl 78 350.1 | −1.1033 (−1.51) | +1.6791 | +2.30 |
| 3 | 105 | SHORT | 09-09 23:46 | −0.0136 (−0.03) | trail 77 393.9 | +0.7669 (+1.50) | −0.7805 | −1.53 |
| 4 | 106 | SHORT | 09-12 09:15 | −0.2963 (−0.72) | sl 78 301.6 | −1.0603 (−2.59) | +0.7640 | +1.87 |
| 5 | 108 | LONG | 09-14 17:00 | +1.1371 (+1.54) | trail 79 024.4 | +1.5947 (+2.15) | −0.4576 | −0.62 |
| **6** | **109** | LONG | 09-18 23:45 | **+2.0051 (+3.43)** | **trail 81 018.9 @ 09-19 04:33** | **+2.1750 (+3.72)** | **−0.1699** | **−0.29** |
| | | | | | | **Σ (6 of 10)** | **+0.8798** | **+$1.43** |

- **The canon was stale before this pass:** its table still showed the 09-12 state (3 resolved). Rows 4–5 come from the 2026-09-16 15:20 report and never reached it. The old block is kept below the new table, marked superseded.
- **How row 6 was computed:** replayed on 3,974 BingX 1m candles, **0 gaps**. The same replay first reproduced the published vpos 108 counterfactual **to the digit (+1.5947R)**.
- `EXIT_ADVISOR_DRYRUN` stays **False**. **Four more resolved closes are needed.**

### 2c. Scan of the whole live book (vpos 86–111) for other mislabelled advisor closes

**Method:** for every live close whose reason is not `ai_exit`, look for an advisor `close` decision (`trades` consult rows, `ai_decision='close'`) in the 180 s before it.

| vpos | reason | advisor decision before the close | verdict |
|---|---|---|---|
| **109** | external | `close` 0.72 at 23:45:10, **2 s before** | **IN** (the ruling) |
| 95 | external | `close` 0.72 at 08-24 02:00:18, 2 s before | same shape, but **predates vpos 101**, so it stays in the OLD population |
| 99 | external | `hold` 2 s before | not the advisor |
| 102, 103, 107, 110 | sl | `hold` | not the advisor |
| 100, 111 | trail | `hold` | not the advisor |
| 86 | sl | last consult `close`, **59 min** before its stop fired; not closed on it | pre-population; noted, not investigated |
| 94 | trail | `hold` | not the advisor |

**Result: vpos 109 is the only mislabelled advisor close in the population.** The label defect itself is **not** fixed; that is a separate pass. The armed-exit path writes `external` for an advisor close.

---

## 3. The database lock (read-only)

### 3a. Everything that opens `trades.db`

**Inside Titan (one process; worker 3989975 now):**

| thread | period | DB work |
|---|---|---|
| 4 gthread request threads (webhooks) | per signal | `insert_signal`, `update_signal_execution`, skip-attribution inserts, and the **scoring reads**: `orderbook_density` percentiles, `market_context` count on `trades`, tiers/matrix. Also the entry path's cap reads and `virtual_positions` insert. |
| `virtual-trader` poller | 10 s | open positions, cycle counters; row updates and excursion samples when a position is open |
| `breakeven-worker` | 5 s | `breakeven_jobs` (0 rows ever) |
| `mfe-tracker` | tick | `mfe_tracking` select and update, `trades` MFE columns |
| `orderbook-density-collector` | 60 s | one INSERT into `orderbook_density` |
| `signal-audit` | 10 min | `SELECT * FROM trades …`, a full scan; audit updates |
| skip-attribution tracker | tick | `skip_attribution` / `skip_drift_samples` (indexed) |

**Outside Titan:**
- **Titan crons, all 08:05–08:53 UTC:** `silence_digest.py`, `daily_trend_cohort_sensor.py` (Mondays) and the four `titan_*_watch.sh`.
- **Manual tools:** `report.py`, `optimizer.py`.
- **Any root shell:** including Claude sessions.
- **botuser:** cannot open the file, because `/root` is 0700.

**Transaction scope, by AST scan of all 20 files:**
- 119 `with <connection>` blocks, of which 59 write.
- **0 hold a write open across a network or slow call.**
- Python's sqlite3 starts the transaction at the first write and commits when the `with` block exits, so every writer commits promptly by construction.
- Busy timeout is the default **5 s** at most sites (30 s in `post_exit_observatory` and `skip_attribution`).
- **`trades` has no secondary index:** 33,422 wide rows, ~110 MB with the stored prompts.

### 3b. Who holds the lock longest: measured

**On a copy of the live file.** The copy was taken with the backup API in 256-page steps; integrity ok. Each actor's real SQL, median of 3 runs warm, then cold (only the copy's pages evicted):

| actor | query | warm ms | **cold ms** |
|---|---|---|---|
| webhook | `orderbook_density` percentile `_exit_pct` (17 call sites per scored signal) | 96.3 | **3 117.6** |
| webhook | `orderbook_density` `_rank_walls` (fetches 96,876 values) | 185.1 | **2 776.0** |
| webhook | `market_context` `COUNT(*)` on `trades` (full scan) | 62.3 | **2 670.3** |
| signal-audit | `SELECT * FROM trades WHERE …` (full scan, every 10 min) | 73.0 | **2 205.0** |
| webhook | `_recover_sl_from_trades` / `lookup_entry_for_close` (backward scans) | 1.3 / 1.4 | 79.5 / 60.1 |
| **virtual-trader poller** | open positions | 1.1 | **21.2** |
| **mfe-worker** | active MFE jobs | 0.9 | **12.9** |
| skip tracker | active attributions (indexed) | 2.8 | 21.5 |

**Live, and passive:** `/proc/locks` sampled every ~4.9 ms for 16 minutes (17:42:45–17:58:45), 196,390 samples, 616 held-lock intervals. **No other process touched the file** apart from this investigation.

| holder | lock | n | p50 | p99 | max |
|---|---|---|---|---|---|
| Titan worker | SHARED (reading) | 541 | 10.7 ms | 77.5 ms | 106.0 ms |
| Titan worker | EXCLUSIVE (commit) | 30 | 12.6 ms | 58.0 ms | 58.0 ms |
| Titan worker | RESERVED (write open) | 25 | 4.8 ms | 19.2 ms | 19.2 ms |
| **this investigation's backup copy** | SHARED | 1 | | | **1 914.7 ms** |
| this investigation's `sqlite3` query | SHARED | 1 | | | 151.6 ms |

**Answer to "which of the five holds a transaction longest":**
- **The webhook threads, and by a wide margin.**
- They are the only ones of the five that run multi-second full-table reads on the scoring path.
- The poller and `mfe_worker` stay under 22 ms even when cold.

**What the window could and couldn't show:**
- It was warm, and only 2 webhooks landed in it, so nothing came near 5 s.
- The longest hold in the window was **my own copy (1.9 s)**, still under the timeout. Titan logged **0** lock errors.
- The 05:30 event needed **cold pages plus three signals scored at once** (05:30:15). A window without a signal burst can't reproduce that.
- So **the exact 05:30 holder is bounded by measurement but not named by observation.**

### 3c. Is `journal_mode=delete` + 5 s the root cause?

It is **half** of it.

**The mechanism:** in rollback-journal mode, a writer that wants to commit takes PENDING and waits for readers to drain, and **while it waits, no new reader can start**. That is why plain SELECTs (`virtual_trader.py:731` and `:987`) failed at 05:30.

**The other half:** readers that hold SHARED for **seconds**. Measured, that means the webhook's scoring scans: 2.7–3.1 s each when cold, several per signal, three signals at once.

**Neither half alone reaches 5 s.** Together they can: with overlapping multi-second readers and any writer, new readers wait past the 5 s timeout.

**Candidate: `PRAGMA journal_mode=WAL`. Named, NOT switched.**
- **What it fixes:** readers never block a writer and a writer never blocks readers, so a SELECT can no longer fail "database is locked". Writers still serialise with each other, but they commit in ≤58 ms.
- **What it costs:**
  - It is persistent and file-level, so it affects every process that opens the file.
  - It adds `-wal`/`-shm` files next to the database, and needs periodic checkpoints.
  - It should be applied from flat in its own pass.

**Other candidates, not applied:**
- Take the percentile scans off the hot path: cache the baseline, or index `orderbook_density(source)`.
- A longer busy timeout on the entry path.

### 3d. The two stuck `pending` rows (34281, 34282): not written

- **What it would take:** `UPDATE trades SET status='failed', error='database is locked (status write lost)' WHERE id IN (34281,34282) AND status='pending'`, with a `.bak` first.
- **Is it safe? Yes:**
  - No code reads `trades.status='pending'`; it is only `insert_signal`'s default.
  - `skip_attribution` already holds both rows as `failed` (17553, 17554).
  - The only visible effect is `silence_digest`'s daily status count.
- **What it can't do:** restore the advisor fields that the lock lost. Those stay NULL, and must not be reconstructed.
- **A third one exists:** row 15604 (2026-07-13, before live trading).
- **Your call.**

### 3e. The failsafe round trip is in the canon (`§0.VENUE-VS-DB`)

| field | value |
|---|---|
| BingX positionId | **2101906879672446978**, LONG 0.0018, 5×, cross |
| open | `2101906879651475456` MARKET BUY @ 81 577.8, 05:30:26 UTC, fee −0.073420 |
| stop | `2101906881789931520` STOP_MARKET 80 686.0, **CANCELLED**, executedQty 0 |
| close | `2101906906608267264` reduce-only MARKET SELL @ 81 552.1, 05:30:33 UTC, fee −0.073397 |
| net | realised −0.0463, commission −0.14682, **−$0.1931** |

**Reconciliation rule, written into the canon:** venue net P&L = Σ `virtual_positions.net_pnl` + Σ rows of this table (currently 1 row, −$0.1931).

---

## 4. Confirmations: every write, in order

| # | write | stated before, and why |
|---|---|---|
| 1 | `cp -p virtual_trader.py virtual_trader.py.bak_failedread_20260921T173345Z` | the `.bak`, before any change |
| 2 | new file `tests/test_vpos_fill_failed_read_is_not_flat.py` (plus two hardening edits) | the contract |
| 3 | sandbox `/tmp/titan-contract-failedread` (botuser 0700 copies) | the botuser run |
| 4 | Edit `virtual_trader.py`, `_reconcile_passive_fill` only | the approved §6 diff |
| 5 | `touch -a` on 5 `__pycache__/*.pyc` (atime only) | proof the new process read them |
| 6 | `systemctl restart titan.service`, from flat | the one restart |
| 7 | `git commit 7798f51` in `/root` (not pushed) | fix + contract |
| 8 | canon `OPEN-ITEMS.md` edited on a scratch copy, installed as botuser, `053f5ff` pushed to kola-reports | ledger, clarification, `§0.VENUE-VS-DB`, `§0.DB-LOCK`, `§0.FAILED-READ-CALLERS` |
| — | **unintended:** 6 import-time `init_db()` executions against the live `trades.db` by the first contract draft | schema-only no-ops, proven unchanged (§1a) |

**Not done, as instructed:**
- **0 orders placed or cancelled.**
- No DB rows written (the pending rows and WAL are deferred).
- Other callers not migrated.
- No `daemon-reload`.
- Nothing pushed from `/root`.
- **Mercury-SOL not touched:** not read, not probed, not restarted.
- **NRestarts:** 0 → 0 (the one manual restart; MainPID 1572470 → 3989951).
- `EXIT_ADVISOR_DRYRUN` **False**, `BOOK_GATE_DRYRUN` **False**, from the loaded bytecode.

**Open for you:**
1. Migrate the two 🔴🔴 emergency-path callers (§1f).
2. WAL, in its own from-flat pass (§3c).
3. Relabel rows 34281/34282 (§3d).
4. The armed-exit `external` label defect (§2c).
5. The unit file changed on disk without a `daemon-reload` (§1e).
