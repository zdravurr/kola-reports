# titan-emergency-paths-no-longer-report-safety-on-failed-read

_2026-09-21 18:30 UTC_

---

# Titan: the two emergency paths no longer report SAFETY on a failed read. Fixed, loaded from flat, contract RED→GREEN. The unit-file warning is a global systemd flag; titan.service is unchanged. Rows 34281/34282 are relabelled.

**2026-09-21 · titan-bot HEAD `d070a5f` (was `7798f51`) · canon `53b7be8` · Titan LIVE, real money · Mercury-SOL not touched**
*(File dated 18:30 so its path matches the one pre-registered in the canon; written and published at ~18:20 UTC.)*

`openitems_guard`: **EXIT=0** at the start. **EXIT=0** at the end, against the new HEAD and the updated canon.

---

## 0. Summary

| item | result |
|---|---|
| §1 the two callers | **Migrated, applied from flat, LOADED** (restart 2026-09-21 18:16:14 UTC).<br>The contract is **RED on the old code: 5 of 15 fail**, exactly the five safety claims. It is **GREEN on the patch: 15 of 15, as root and as botuser**, and a kernel trace shows **0 opens of the live DB**.<br>AST: only the two functions changed. All guarded values and prompts are identical in the loaded bytecode. |
| §1d | Every state (OPEN / FLAT / UNKNOWN) is written out, before and after, for both callers. **No branch infers safety from a failed read** (§1d). |
| §2 unit file | **titan.service did NOT change.** On disk and loaded, it is identical in every property that matters.<br>The warning is a global systemd flag: **every unit on the box** shows `NeedDaemonReload=yes`. It was raised by an ordinary root SSH login at 17:00:51, whose session scope logind writes into `/run/systemd/transient`.<br>No daemon-reload, no edit. **The next restart loads nothing new.** |
| §3 rows | `.bak` first. The approved UPDATE ran: **2 rows affected**. Row 15604 untouched; nothing reconstructed. |
| §4 | Flat confirmed. Restarted once, from flat. Canon `§0.FAILED-READ-CALLERS` updated. |
| next pass | `main.py:3663` `_handle_5m_close_via_ai` and `main.py:4068` `_handle_liquidity_sweep`. Both take actions on a failed read but declare no safety. |

---

## 1. The two callers

### 1a. The defect, in one line each

- `main._execute_close_position` returns **None** in exactly one place (`main.py:1359`, `if pos is None: return None`). It reads through the `_fetch_open_position` shim, which returns None for a flat book **and** for a failed read.
- **`virtual_trader._entry_failsafe_close`** treated that None as "**nothing is exposed**": it sent an alert and returned, and `_UNSAFE_STATE` was **not** tripped.
- **`breakeven_worker._emergency_close`** sent "**✅ Emergency close executed**" regardless of the result. That includes the case where the stop was cancelled and its recreate failed.

**The remedy stays inside the two callers.** `_execute_close_position` is shared by 8 callers and was **not** changed. Each caller now asks `main._fetch_position_state(double_probe=True, attempts=2)`, the same three-state read that `7798f51` introduced. That is both probes (unified + raw swapV2), with one re-probe after 2 s.

### 1b. Contract first: `tests/test_failed_read_never_reports_safety.py`

**What is real and what is faked:**
- **Real code:** `_execute_close_position`, `fetch_order_fee`, `_cancel_stop_orders`, `_fetch_position_state`, `_fetch_open_position` and `POS_*` are lifted out of `main.py` by AST. `order_adapter._probe_positions` is the real double probe. Both modules are loaded from source.
- **Faked:** the exchange, `sleep` and the Telegram sender only.
- **The live DB is never opened**, by three layers:
  - `TITAN_PEO_AUTO_INIT=0`.
  - Any connect to a file named `trades.db` is redirected to a scratch DB. There were 5 import-time `init_db()` connects (virtual_trader, post_exit_observatory, and `breakeven_worker.py:1009`, which runs its own at import).
  - A kernel `openat` trace of the test process shows **0 opens of `/root/titan-bot/trades.db`**, on both the RED and the GREEN run.

**The checks. "`.bak`" means compared byte-for-byte against the pre-change file, in the same process:**

| # | case | pass condition |
|---|---|---|
| E1 | entry failsafe, **true flat** | "nothing open" alert byte-identical to `.bak`; breaker NOT tripped |
| E2 | entry failsafe, **every read fails** | breaker **TRIPPED**; alert says the **READ FAILED**; never "nothing is exposed" |
| E3 | entry failsafe, close-path read fails but a re-read shows OPEN | retried, and the retry **CLOSES** it |
| E4 | entry failsafe, normal close | "CLOSE EXECUTED" byte-identical to `.bak` |
| E5 | entry failsafe, close order raises 3× | existing CRITICAL alert and breaker detail byte-identical to `.bak` |
| E6 | entry failsafe, first read UNKNOWN, then a **confirmed** flat | "nothing open"; breaker NOT tripped |
| M1 | emergency close, fill, re-read flat | "✅ Emergency close executed" byte-identical to `.bak` |
| M2 | emergency close, **every read fails** | "OUTCOME UNKNOWN", hands required; **never ✅** |
| M3 | emergency close, already flat, reads fine | ✅ (as today) |
| M4 | emergency close, order sent but position **still open** | "DID NOT FLATTEN", hands required; **never ✅** |
| M5 | emergency close, order raises | existing CRITICAL message byte-identical to `.bak` |
| M6 | emergency close, fill, but the **verification read fails** | "OUTCOME UNKNOWN"; **never ✅** |
| S | sensitivity | the `.bak` **does** claim safety on E2, E3, M2, M4, M6 |
| A | AST | only `_entry_failsafe_close` / `_emergency_close` may differ |
| D | the live DB | never opened |

| run | root | botuser (sha256-pinned copies, `/tmp/titan-contract-safetyread`) |
|---|---|---|
| **RED**, unpatched (`vt 4184eb8ff1f59095`, `bw f76bede58d51b55b`) | **EXIT=1, FAIL: E2 E3 M2 M4 M6**, 10 OK | **EXIT=1, same 5 FAIL** |
| **GREEN**, patched (`vt 3f6f0dc0396b7107`, `bw 7bd67a06baadd054`) | **EXIT=0, 15 / 15** | **EXIT=0, 15 / 15** |
| `7798f51` contract (`test_vpos_fill_failed_read_is_not_flat.py`) | **EXIT=0, 19 / 19** | **EXIT=0, 19 / 19** |

**Change to `7798f51`'s contract.** Its AST scope pin compared against *its own* `.bak` and now also saw `_entry_failsafe_close`. That is the only check that failed. I widened the pin to the known set `{_reconcile_passive_fill, _entry_failsafe_close}`, with a comment. A third differing function still fails it.

### 1c. The diffs, as applied

```diff
--- virtual_trader.py.bak_safetyread_20260921T181249Z
+++ virtual_trader.py        (_entry_failsafe_close only)
     _last_err = None
+    _last_read_unknown = False
     for _attempt in range(FAILSAFE_CLOSE_ATTEMPTS):
+        _last_read_unknown = False
         try:
             import main as _m
             _res = _m._execute_close_position(symbol, position_side,
                                               _from_adapter=True)
             if _res is None:
+                # 🔴 F1 (2026-09-21). None means the close path's position read
+                # returned nothing — and that read returns nothing BOTH for a flat
+                # book AND for a FAILED read. Ask again, three-state, before
+                # believing it: only a CONFIRMED flat is "nothing exposed".
+                _state, _pos = _m._fetch_position_state(
+                    symbol, position_side, double_probe=True, attempts=2)
+                if _state == _m.POS_OPEN:
+                    # It IS there and was NOT closed. A failed attempt: retry;
+                    # exhausting the attempts trips the breaker below.
+                    raise RuntimeError(
+                        f"close path saw no position, but a re-read shows it OPEN "
+                        f"({(_pos or {}).get('contracts')} contracts) — not closed")
+                if _state == _m.POS_UNKNOWN:
+                    _last_read_unknown = True
+                    raise RuntimeError("position read FAILED on both probes — "
+                                       "exposure UNKNOWN, not flat")
                 # No live position found. Either the order never filled or it is
                 # already flat. Nothing is exposed.
                 _failsafe_alert(          ... unchanged "nothing open" text ...
@@ after the attempt loop
     # Every attempt failed. We may be holding a real, unprotected position.
     _UNSAFE_STATE['tripped'] = True
+    if _last_read_unknown:
+        # The close path found nothing, but the exchange could not be READ: the
+        # book is NOT known to be flat. Say that — never "nothing is exposed".
+        _UNSAFE_STATE['detail'] = (
+            f"{symbol} {position_side}: entry raised after the fill and the "
+            f"failsafe could not READ the position ({FAILSAFE_CLOSE_ATTEMPTS}x) — "
+            f"exposure UNKNOWN (last error: {_last_err})")
+        _failsafe_alert(
+            f"🚨🚨 <b>CRITICAL — POSITION READ FAILED, EXPOSURE UNKNOWN</b> 🚨🚨\n"
+            f"{symbol} {position_side} amount <code>{_amt}</code>\n"
+            f"The entry raised after a REAL fill. The failsafe close found no "
+            f"position, but the exchange READ FAILED on both probes "
+            f"{FAILSAFE_CLOSE_ATTEMPTS} times — the book is NOT known to be flat.\n"
+            f"Entry error: <code>{type(exc).__name__}: {exc}</code>\n"
+            f"<b>MANUAL ACTION REQUIRED — check the exchange NOW.</b>\n"
+            f"All further entries are REFUSED until the service is restarted.")
+        return
     _UNSAFE_STATE['detail'] = (   ... unchanged CRITICAL path ...
```

```diff
--- breakeven_worker.py.bak_safetyread_20260921T181249Z
+++ breakeven_worker.py      (_emergency_close only)
         print(f"[BE-FAILSAFE] emergency close result: {result}", flush=True)
+        # 🔴 F1 (2026-09-21). "Executed" is a claim about the BOOK, so it needs a
+        # read of the book: _execute_close_position returns None both when the
+        # position was already gone AND when its read FAILED, and a fill alone
+        # does not prove nothing is left. Only a CONFIRMED flat says done.
+        _state, _pos = main._fetch_position_state(
+            symbol, position_side, double_probe=True, attempts=2)
+        if _state == main.POS_FLAT:
+            _out = f"✅ Emergency close executed for {symbol} {position_side}."
+        elif _state == main.POS_OPEN:
+            _out = (f"🚨 <b>EMERGENCY CLOSE DID NOT FLATTEN</b> 🚨\n"
+                    f"{symbol} {position_side} is STILL OPEN on the exchange "
+                    f"(<code>{(_pos or {}).get('contracts')}</code> contracts) and "
+                    f"its breakeven stop could not be recreated.\n"
+                    f"<b>MANUAL ACTION REQUIRED — check the exchange NOW.</b>")
+        else:
+            _out = (f"🚨 <b>EMERGENCY CLOSE OUTCOME UNKNOWN</b> 🚨\n"
+                    f"{symbol} {position_side}: the position read FAILED on both "
+                    f"probes after the close attempt — the book is NOT known to be "
+                    f"flat, and the breakeven stop could not be recreated.\n"
+                    f"<b>MANUAL ACTION REQUIRED — check the exchange NOW.</b>")
+        if _state != main.POS_FLAT:
+            print(f"[BE-FAILSAFE] 🚨 emergency close NOT verified flat: {_state}",
+                  flush=True)
         if send_tg:
             try:
-                send_tg(f"✅ Emergency close executed for {symbol} {position_side}.")
+                send_tg(_out)
             except Exception:
                 pass
```

### 1d. Every state, before and after, for both callers

**Entry failsafe (`virtual_trader._entry_failsafe_close`).** It runs after a real fill, when the entry raised before its row was written. The state is what the exchange read returns once `_execute_close_position` has come back None.

| state | BEFORE | AFTER |
|---|---|---|
| close succeeded (a fill returned) | "ENTRY FAILSAFE CLOSE EXECUTED", return | **unchanged** (E4, byte-identical) |
| close order raised, 3× | breaker TRIPPED, "POSITION MAY BE OPEN AND UNPROTECTED" | **unchanged** (E5, byte-identical) |
| **POS_FLAT** (confirmed on both probes) | "nothing open … nothing is exposed", return, breaker not tripped | **unchanged** (E1, byte-identical). Also reached after an earlier UNKNOWN attempt if a later read confirms flat (E6). |
| **POS_OPEN** (the close path's read failed, but a re-read sees it) | 🔴 "**nothing is exposed**", return; **a live position left open and declared safe** | counted as a failed attempt and **retried**; the retry closes it (E3). If every attempt fails, the breaker is TRIPPED via the existing CRITICAL path. |
| **POS_UNKNOWN** (both probes fail, including the re-probe) | 🔴 "**nothing is exposed**", return, **breaker NOT tripped**; entries continue | **retried**. If the attempts run out on a failed read: **`_UNSAFE_STATE` TRIPPED**, and a hands-required "**POSITION READ FAILED, EXPOSURE UNKNOWN** … the book is NOT known to be flat" alert. All further entries are refused until restart (E2). |

**BE emergency close (`breakeven_worker._emergency_close`).** It runs after the old stop was cancelled and the breakeven stop could not be recreated. The state is the verification read, which now happens **after every close attempt**.

| state | BEFORE | AFTER |
|---|---|---|
| close order raised | "❌ CRITICAL: BE emergency close failed" | **unchanged** (M5, byte-identical) |
| **POS_FLAT** (confirmed) | "✅ Emergency close executed" | **unchanged** (M1, M3) |
| **POS_OPEN** (order went through, position still there) | 🔴 "✅ **Emergency close executed**" | "🚨 **EMERGENCY CLOSE DID NOT FLATTEN** … STILL OPEN (n contracts) … MANUAL ACTION REQUIRED", plus a journal line (M4) |
| **POS_UNKNOWN** (the read fails, whether or not the close filled) | 🔴 "✅ **Emergency close executed**" | "🚨 **EMERGENCY CLOSE OUTCOME UNKNOWN** … the book is NOT known to be flat … MANUAL ACTION REQUIRED", plus a journal line (M2, M6) |

**No branch now infers safety from a failed read.** The only paths that say "nothing open" or "✅ executed" are the ones where both probes answered and neither saw the position.

**Costs:**
- The extra read runs only on the None path (entry failsafe) or once per emergency close.
- Each read is at most two REST calls plus one 2 s re-probe.
- The emergency close's retries are unchanged in count. The breakeven emergency path gains no breaker of its own: it now shouts instead of reassuring. Tripping `_UNSAFE_STATE` from it as well would be a separate decision.

### 1e. `.bak`, AST, runtime values

- **`.bak` before any change:** `virtual_trader.py.bak_safetyread_20260921T181249Z` (sha `4184eb8ff1f59095`) and `breakeven_worker.py.bak_safetyread_20260921T181249Z` (sha `f76bede58d51b55b`), both byte-identical to the files at the time.
- **AST:** `virtual_trader` 76 / 76 top-level nodes, the only one differing is `_entry_failsafe_close`. `breakeven_worker` 47 / 47, the only one differing is `_emergency_close`. This is contract check [A].
- **Values:** read from source before the restart, and **from the loaded `.pyc` after it**, by unmarshalling the bytecode. **All 21 lines are identical:**

| name | value |
|---|---|
| `SL_ATR_MULT` / `TRAIL_MULT_ATR` | 2.25 / 1.6875 |
| `EXIT_ADVISOR_DRYRUN` | **False** |
| `BOOK_GATE_ENABLED` / `BOOK_GATE_DRYRUN` | True / **False** |
| `BOOK_GATE_CLAUSE_A_ENABLED` / `_B_` | **True / False** |
| `LIVE_TRADING_ENABLED` / `ORDER_ADAPTER_LIVE` | True / True |
| `CONFLUENCE_SCORE_THRESHOLD` / `_FLAT_` | 3.0 / 5.0 |
| size | `LIVE_FIXED_MARGIN_USDT` 30.0 × `LEVERAGE` 5 (boot banner `$30 x 5 = $150 notional`); `MAX_POSITIONS_PER_SIDE` 1 |
| `_ENTRY_SYSTEM` | `30c979595a4831aa` |
| `_LEARNING_SYSTEM` | `191cf5d71ebf3865` |
| `_CLOSE_SYSTEM` | `7d7707cfa2d336f7` |
| `_CLOSE_SYSTEM_RICH` | `3d709571e17ff405` |

- **Proof the patches are loaded:**
  - `virtual_trader.cpython-312.pyc` was recompiled at boot (18:16:18.15); header matches source. `_entry_failsafe_close` names `_fetch_position_state` and `POS_UNKNOWN`, and its constants carry "EXPOSURE UNKNOWN".
  - `breakeven_worker.cpython-312.pyc` was recompiled at 18:16:16.92; header matches source. `_emergency_close` names `_fetch_position_state` and carries "OUTCOME UNKNOWN". It needs no `POS_UNKNOWN` name, because UNKNOWN is its `else` branch.
  - `7798f51`'s `_reconcile_passive_fill` is still loaded.
- **Other modules were read by the new process:** I reset the `atime` of their `.pyc` files to 2026-01-01 before the restart. The boot re-stamped `main` (18:16:14.41), `config` and `claude_advisor` (18:16:15.46–47).

### 1f. Not migrated: the next pass

These two take an **action** on a failed read, but neither declares safety:

| caller | on a failed read |
|---|---|
| `main.py:3663` `_handle_5m_close_via_ai` | treats the side as not open and **skips the advisor consultation** |
| `main.py:4068` `_handle_liquidity_sweep` | sends "No open LONG — nothing to close" and **skips the sweep close** |

The rest of the table is unchanged in canon `§0.FAILED-READ-CALLERS`:
- `3900` and `4291` are dead in live.
- `breakeven_worker:425` is benign.
- The job path (`:692`, `:746`, `:765`) is dormant.
- `_do_close`'s abort retries next tick.

---

## 2. The unit file: read-only. Nothing changed, nothing reloaded.

### 2a. On disk vs loaded

**On disk** (`systemctl cat titan.service`), verbatim apart from the drop-in's comment lines:
```
# /etc/systemd/system/titan.service
[Unit]
Description=Titan BTC/USDT trading bot
After=network-online.target
Wants=network-online.target
[Service]
Type=simple
User=root
WorkingDirectory=/root/titan-bot
ExecStart=/usr/local/bin/gunicorn -c /root/titan-bot/gunicorn.conf.py main:app
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=titan
[Install]
WantedBy=multi-user.target
# /etc/systemd/system/titan.service.d/oom-armor.conf
[Service]
OOMScoreAdjust=-900
MemoryMin=600M
```

**Loaded** (`systemctl show`):
```
Type=simple  Restart=always  RestartUSec=5s  User=root  Group=  Environment=  WorkingDirectory=/root/titan-bot
ExecStart={ path=/usr/local/bin/gunicorn ; argv[]=/usr/local/bin/gunicorn -c /root/titan-bot/gunicorn.conf.py main:app ; … }
OOMScoreAdjust=-900  MemoryMin=629145600  StandardOutput=journal  SyslogIdentifier=titan
Description=Titan BTC/USDT trading bot  Wants=network-online.target  After=… network-online.target
FragmentPath=/etc/systemd/system/titan.service  DropInPaths=/etc/systemd/system/titan.service.d/oom-armor.conf
```

### 2b. Who changed it, and when

**Nobody changed titan.service:**
- `titan.service` was last modified **2026-05-16 19:33:38**; `oom-armor.conf` and its directory **2026-07-13 21:21:43**.
- No other `titan.service.d` or global `service.d` drop-in exists in any systemd unit path.
- Shell history shows only `status`, `is-active`, `is-enabled` and `stop` commands against it, no edits.

**Why systemd still says "changed on disk":**
- `NeedDaemonReload=yes` is **not specific to titan**. `ssh`, `cron`, `systemd-journald` and every other unit I checked report it too.
- systemd sets it when **any** unit directory in its search path is newer than the last reload.
- The last reload was **snapd's**, at 08:08:36–37 (while mounting `snap-core24-2124.mount`).
- The newest directory since then is **`/run/systemd/transient`, 17:00:51**. That is where logind writes a login session's scope.
- **Root SSH session 807023** was opened at 17:00:51 (`sshd … session opened for user root`, `Started session-807023.scope`) and is still active.
- snapd also wrote two `.wants` symlinks at 08:08:37.27, a quarter-second after its own reload finished. That is the same global effect.

**Scope note:** I ran one read-only systemd property query (`NeedDaemonReload`) on the Mercury-SOL unit, among others, to show the flag is global. No Mercury-SOL file or process was touched.

### 2c. Does anything that matters differ?

**No.** ExecStart, Environment (empty on both), User, WorkingDirectory, Restart policy, RestartSec, OOMScoreAdjust and MemoryMin are identical. **A restart or a daemon-reload loads exactly what is already running.** So §4b's stop condition did not apply, and I went ahead with the from-flat restart.

### 2d. No action taken

**No `daemon-reload`, no edit.** The warning will recur after every new login session until something runs a reload. It is harmless for titan. Whether to reload is your call.

---

## 3. The relabel (approved)

**Step 1, backup:** `trades.db.bak_relabel_20260921T181534Z`, written with SQLite's online backup API in 256-page steps. It took 1.9 s, integrity `ok`, and holds 15604, 34281 and 34282 all still `pending`.

**Step 2, the exact statement:**
```sql
UPDATE trades SET status='failed', error='database is locked (status write lost)' WHERE id IN (34281,34282) AND status='pending'
```

**Rows affected: 2.** Committed. After:

| id | status | error | ai_decision / score |
|---|---|---|---|
| 15604 | **pending** (untouched, pre-live) | NULL | NULL |
| 34280 | failed | database is locked | execute / 3.91 (unchanged) |
| 34281 | **failed** | database is locked (status write lost) | NULL / NULL (not reconstructed) |
| 34282 | **failed** | database is locked (status write lost) | NULL / NULL (not reconstructed) |

---

## 4. Apply

**Flat before the restart (18:16:04 UTC):**
- DB: 0 open `virtual_positions`, 0 `exit_pending`, 0 live `breakeven_jobs`.
- BingX, **both probes, empty error lists**: unified positions `[]`, raw `data: []`, unified open orders `[]`, raw `orders: []`.
- 0 webhooks or entries in the previous 90 s.

**The restart:**
- `systemctl restart titan.service` at 18:16:12; active **18:16:14 UTC**. This time shutdown took 2 s, not 24 s.
- MainPID 3989951 → **3997369**; worker **3997377**.
- **NRestarts 0 → 0.** systemd does not count a manual restart; this was the only restart.

**Boot line:**
```
2026-09-21T18:16:22.302 [TITAN] [TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
```

**After the boot:**
- 0 boot errors. Since the restart: 0 `VPOS-FILL 🚨`, 0 tracebacks, 0 `database is locked`, 0 failsafe lines.
- `openitems_guard` **EXIT=0** against HEAD `d070a5f` and the updated canon.

**Canon updates:**
- `2e85565`:
  - a new `d070a5f` header paragraph;
  - `§0.FAILED-READ-CALLERS` marks the two safety-direction callers **migrated** and **3663 / 4068 pending**;
  - `§0.VENUE-VS-DB` and `§0.DB-LOCK` record the relabel.
- `53b7be8`: I had written the header's re-verification time as 18:25, which was in the future. Corrected to the real 18:17.

---

## 5. Confirmations: every write, in order

| # | write |
|---|---|
| 1 | `cp -p` `.bak` of `virtual_trader.py` and `breakeven_worker.py` (`…bak_safetyread_20260921T181249Z`) |
| 2 | new `tests/test_failed_read_never_reports_safety.py`; sandbox copies in `/tmp/titan-contract-safetyread` (botuser, 0700) |
| 3 | patch `virtual_trader._entry_failsafe_close` |
| 4 | patch `breakeven_worker._emergency_close` |
| 5 | widen the scope pin in `tests/test_vpos_fill_failed_read_is_not_flat.py` |
| 6 | `trades.db.bak_relabel_20260921T181534Z` (online backup) |
| 7 | the approved UPDATE (2 rows) |
| 8 | `touch -a` on 6 `__pycache__/*.pyc` (atime only) |
| 9 | `systemctl restart titan.service`, from flat, **the only restart** |
| 10 | `git commit d070a5f` in `/root` (not pushed) |
| 11 | canon `2e85565` + `53b7be8`, pushed as botuser |

**Not done:**
- **0 orders placed or cancelled.** Venue calls were read-only (positions and open orders on both probes).
- **No `daemon-reload`, no unit edit.**
- Row 15604 untouched; lost advisor fields not reconstructed.
- `3663` / `4068` not migrated.
- **Mercury-SOL not touched** (one read-only systemd property query, §2b).
- `EXIT_ADVISOR_DRYRUN` **False**, `BOOK_GATE_DRYRUN` **False**, both read from the loaded bytecode.

**Open for you:**
1. The next pass: `3663` / `4068`.
2. Whether the BE emergency close should also trip `_UNSAFE_STATE` on OPEN or UNKNOWN (today it alerts only).
3. Whether to run a `daemon-reload`. It is harmless (nothing differs) but not needed.
4. Carried from before: WAL; the armed-exit `external` label.
