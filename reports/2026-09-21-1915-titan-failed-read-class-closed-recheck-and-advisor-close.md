# titan-failed-read-class-closed-recheck-and-advisor-close

_2026-09-21 19:15 UTC_

---

# Titan: the failed-read class is CLOSED. No live caller now drops an action or claims a fact on a failed position read. The post-entry critical close and the advisor close were the last two.

**2026-09-21 · titan-bot HEAD `f53d048` (was `07f9025`) · canon `fa233f3` · Titan LIVE, real money · Mercury-SOL not touched**
*(File dated 19:15 so its path matches the one pre-registered in the canon; written and published at ~19:08 UTC.)*

`openitems_guard`: **EXIT=0** at the start. **EXIT=0** at the end, against `f53d048` and the updated canon. The session-cost hook did not fire during this pass.

---

## 0. The answer, first

**Is there now ANY live caller whose None branch drops an action or claims a fact? None.**

| live caller | on a FAILED position read | fixed in |
|---|---|---|
| `virtual_trader._reconcile_passive_fill` | UNKNOWN → one log line, nothing done, re-checked next tick | `7798f51` |
| `virtual_trader._entry_failsafe_close` | re-read three-state; UNKNOWN → retried, then **breaker TRIPPED** + "READ FAILED, EXPOSURE UNKNOWN" | `d070a5f` |
| `breakeven_worker._emergency_close` | verified after every close; OPEN / UNKNOWN → "DID NOT FLATTEN" / "OUTCOME UNKNOWN" + **breaker TRIPPED** | `d070a5f`, `40aad46` |
| `main._handle_5m_close_via_ai` (side read) | "position read FAILED", no consultation; the next signal or the hourly review re-consults | `40aad46` |
| `main._handle_liquidity_sweep` | "read FAILED — sweep close NOT evaluated" | `40aad46` |
| `main._execute_armed_exit` | `exit_pending` **kept ARMED**, "close NOT confirmed"; OPEN retried | `07f9025` |
| `main._handle_5m_close_via_ai` (advisor close) | row `close_unconfirmed`, "AI CLOSE NOT confirmed"; OPEN retried | `07f9025` |
| **`virtual_trader._run_recheck_tier`** (critical close) | **NOT marked, tier re-fires, breaker TRIPPED, one hands-required alert**; OPEN retried | **`f53d048`** |
| **`virtual_trader._advisor_close`** (`ai_exit`) | **"close NOT confirmed" alert, next verdict decides (no breaker)**; OPEN retried | **`f53d048`** |
| `virtual_trader._process_position` stop / trail / breakeven closes | **a deferral by design:** the row stays OPEN, the trigger persists, it is retried next tick, and the exchange stop stays in place. No drop, no claim. | — |
| `breakeven_worker.move_stop_with_race_guard` | after a failed cancel returns `'closed'`; the caller persists nothing, the OLD stop is held, retried next tick | — (benign) |

**Not live:**
- `main.py:3926` and `4340` shim reads, and the legacy SL-failsafe in `main._execute_entry`: `engine_owns_position()` is True.
- The trend-reversal close: `TREND_REVERSAL_EXIT_DRYRUN = True`.
- The Smart-TP sweep close: `EQH_EQL_SMART_TP_ENABLED = False`.
- The `breakeven_jobs` path (`breakeven_worker.py:734/788/807`): 0 rows ever.

This table is canon `§0.FAILED-READ-CALLERS` verbatim.

---

## 1. `_run_recheck_tier`: the post-entry critical close

### 1a. The order, line by line

**Before (`07f9025`):**
```
1  sensor_events.log_recheck(...)
2  _set_recheck_status(vpos_id, 'closed_critical')        # 🔴 marked BEFORE anything happened
3  fresh = _open_position(...)
4  if fresh is this vpos:
5      send_tg("🛑 Post-entry T+Ns — EMERGENCY CLOSE …")   # 🔴 announced BEFORE anything happened
6      _do_close(... 'post_entry_critical' ...)           # 🔴 return value IGNORED
7      return 'closed'                                    # tier done; never re-fires
8  return None
```

**After (`f53d048`):**
```
1  sensor_events.log_recheck(...)                          # unchanged
2  fresh = _open_position(...)
3  if fresh is not this vpos: mark 'closed_critical'; return None     # unchanged outcome
4  _res = _do_close(... 'post_entry_critical' ...)         # the close FIRST
5  if _res is None:
6      state = _fetch_position_state(double_probe=True, attempts=2)
7      if state == OPEN: _res = _do_close(...)             # one retry
8      if _res is None and state != FLAT:                  # NOT confirmed
9          _UNSAFE_STATE tripped (detail names the vpos and why)
10         ONE hands-required alert per vpos ("critical close NOT confirmed … MANUAL ACTION REQUIRED")
11         return None                                     # NOT marked → the tier re-fires next tick
12 _set_recheck_status(vpos_id, 'closed_critical')         # ✅ only now: outcome KNOWN
13 send_tg("🛑 Post-entry T+Ns — EMERGENCY CLOSE …")       # ✅ same text as today
14 return 'closed'
```

### 1b. Every state

| state after the first close attempt | before | after |
|---|---|---|
| close succeeded | marked, message, `'closed'` | **same content** (R4). The mark and the message now come **after** the close, as the contract's event order proves. |
| None + **POS_FLAT** | marked, message, `'closed'` | **byte-identical** (R2) |
| None + **POS_OPEN** | 🔴 marked, "EMERGENCY CLOSE" sent, close silently not done, never re-fires | **retried**. On success: marked + message (R3). Still open: **not marked, breaker TRIPPED**, "still OPEN" alert (R5). |
| None + **POS_UNKNOWN** | 🔴 same silent drop under a message saying it happened | **not marked** (the tier re-fires every tick), **breaker TRIPPED**, one alert: "🚨 Post-entry T+Ns — critical close NOT confirmed … the position read FAILED on both probes … MANUAL ACTION REQUIRED … All further entries are REFUSED until the service is restarted" (R1) |

**No alert spam.** A re-fire while the breaker is already tripped *for this vpos* only logs to the journal; no second Telegram message (R1b). Without this, a failing read would alert every 10 s.

**Wording.** My first draft of the alert said "EMERGENCY CLOSE NOT confirmed". The contract caught that it contains the very phrase that must never read as "done". It now says "**critical close** NOT confirmed".

### 1c. Should an unconfirmed critical close trip the breaker? Applied as ruled (YES). The counter-argument, stated as you asked:

- **The position is not naked.** The close path is close-first, cancel-after, so a close that aborts on a failed read leaves the exchange stop in place. The per-side cap already blocks a second entry on the **same** side while the row is open.
- **The breaker adds two things:** it also blocks the **opposite** side, and it **stays tripped until a manual restart**, even if the next tick's re-fire closes the position cleanly.

That is a real cost (trading halted, possibly overnight), but it errs on the safe side, and your ruling is YES. **Applied.**

**If you'd rather it only alert:** the trip is one line in the patched function, and reverting it is a one-line change.

**How the breaker is cleared:** only by a service restart. It is the same `virtual_trader._UNSAFE_STATE` as the entry failsafe and the BE emergency close.

---

## 2. `_advisor_close`: the `ai_exit` path

### 2a. The change, the same shape as `07f9025`'s 5m fix

| state after a None close | before | after |
|---|---|---|
| POS_FLAT | "no live position to close — left for passive-fill reconciliation, NOT retried", `False` | **byte-identical** (V2) |
| POS_OPEN | 🔴 the same false line; the advisor's close dropped | **retried** → "🤖 EXIT ADVISOR CLOSED", `True` (V3) |
| POS_UNKNOWN / still open | 🔴 the same false line; the advisor's close dropped | "⚠️ EXIT-ADVISOR close NOT confirmed … Position left OPEN and the exchange stop is STILL the backstop. The next verdict decides." `False`. **Never "no live position"** (V1). |
| clean close | "EXIT ADVISOR CLOSED" | **byte-identical** (V4) |

### 2b. No breaker here, deliberately

The exchange stop is in place, and the next verdict (at most 1 h, the hourly review) retries. Contract V1 asserts the breaker is **NOT** tripped.

### 2c. Was any ledger close affected? **No.**

- The journal only reaches back to 2026-09-18 13:25, after every ledger close. It has **0** "no live position to close" lines.
- **The DB answers the question directly.** A close dropped by this defect would show as an advisor `close` verdict with **no close following it**. Every advisor `close` verdict since 2026-09-01 (7) was followed by an actual close within **2 s**:

| consult row | verdict at (UTC) | closed |
|---|---|---|
| 29123 | 09-01 18:00:17 | vpos **101** (`ai_exit`) +2 s |
| 31113 / 31115 | 09-09 08:30:19 / :23 (the double) | vpos **104** (`ai_exit`) +2 s |
| 31259 | 09-09 23:46:01 | vpos **105** (`ai_exit`) +2 s |
| 31884 | 09-12 09:15:09 | vpos **106** (`ai_exit`) +1 s |
| 32630 | 09-14 17:00:23 | vpos **108** (`ai_exit`) +2 s |
| 33670 | 09-18 23:45:10 | vpos 109 (`external`, the armed exit, out of the population) +2 s |

**The ledger is unchanged: 5 of 10, Σ +1.0497R.**

---

## 3. Contracts

**New: `tests/test_recheck_and_advisor_close_failed_read.py`.**
- **What is real:** the `virtual_trader` module, loaded from source with `TITAN_PEO_AUTO_INIT=0` and every `trades.db` connect redirected to scratch; and `main`'s `_execute_close_position`, `fetch_order_fee`, `_cancel_stop_orders`, position reads and `POS_*`, lifted by AST.
- **How the close chain runs:** `_do_close` is faked as the live chain does it, straight into the **real** primitive with `_from_adapter=True`.
- **Faked:** the exchange, sleep, Telegram, the recheck's market-data inputs (walls, 1h metrics, a forced `EMERGENCY_CLOSE` verdict), the sensor logger, and the status writer.
- **Pins:** R1, R1b, R2, R3, R4 (byte-identical, and the order proven by an event log), R5, V1–V4, sensitivity, AST scope, live DB.

| contract | root | botuser (sha256-pinned copies, `/tmp/titan-contract-lasttwo`) |
|---|---|---|
| **new**, RED on `07f9025` | **FAIL R1 R1b R3 R4 R5 V1 V3** | **same 7 FAIL** |
| **new**, GREEN | **13 / 13** | **13 / 13** |
| `test_close_not_dropped_on_failed_read` | 12 / 12 | 12 / 12 |
| `test_last_callers_and_armed_exit_label` | 13 / 13 | 13 / 13 |
| `test_failed_read_never_reports_safety` | 15 / 15 | 15 / 15 |
| `test_vpos_fill_failed_read_is_not_flat` | 19 / 19 | 19 / 19 |

**Live `trades.db` opened 0 times on every root run** (kernel `strace -e openat`).

**What changed in the earlier contracts:** the AST scope pins in `test_failed_read_never_reports_safety` and `test_vpos_fill_failed_read_is_not_flat` were widened to include this pass's two functions, as for `07f9025`. Any other differing function still fails them.

**Stated so nothing looks cleaner than it was:**
- **The harness broke once.** Its first RED run crashed because a fake returned a bare float where the code calls `.label()`. The patch script refused to apply on a harness error, and nothing was patched until the harness was fixed (to the real `indicators.AdxReading`).
- **My inline-comment edit broke one pin**, a syntax error in the test file. I fixed it and re-ran.

---

## 4. Apply

**`.bak` before any change:** `virtual_trader.py.bak_lasttwo_20260921T185843Z` (`3f6f0dc0396b7107`, byte-identical to the original). `virtual_trader.py` is the only source file touched: → `0f355819a2f68777`.

**AST:** `virtual_trader.py` 76 / 76 top-level nodes; differing: **`_run_recheck_tier`, `_advisor_close`**. Nothing else.

**Flat, checked in the same command that restarted, gated (the restart ran only if every condition held), 19:03:46 UTC:**
- DB: open rows 0, `exit_pending` 0, live `breakeven_jobs` 0.
- BingX: unified positions, raw positions, unified open orders and raw open orders all **ok, empty, with empty error lists**.
- 0 entry lines in the previous 120 s.

**The restart:**
- `systemctl restart titan.service` at 19:03:48; active **19:03:51 UTC**.
- MainPID 4004539 → **4007821**; worker **4007905**.
- **NRestarts 0 → 0.** systemd does not count a manual restart; this was the only restart.
- **No daemon-reload.**

**Boot line:**
```
2026-09-21T19:04:00.464 [TITAN] [TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
```
0 boot errors.

**Proof the patch is loaded:**
- `virtual_trader.cpython-312.pyc` was recompiled at boot (19:03:55.66); header matches source.
- Unmarshalled from it: `_run_recheck_tier` names `_UNSAFE_STATE` and carries "critical close NOT"; `_advisor_close` carries "close NOT confirmed".
- `config` and `claude_advisor` `atime`s were re-stamped at boot (19:03:52.81–.82).

**From the loaded bytecode, identical to before the restart:**

| name | value |
|---|---|
| `SL_ATR_MULT` / `TRAIL_MULT_ATR` | 2.25 / 1.6875 |
| `EXIT_ADVISOR_DRYRUN` | **False** |
| `BOOK_GATE_DRYRUN` | **False** |
| `BOOK_GATE_CLAUSE_A_ENABLED` / `_B_` | **True / False** |
| `LIVE_TRADING_ENABLED` / `ORDER_ADAPTER_LIVE` | True / True |
| size | `LIVE_FIXED_MARGIN_USDT` 30.0 × `LEVERAGE` 5; `MAX_POSITIONS_PER_SIDE` 1 |
| advisor SYSTEM prompts (sha256) | `_ENTRY` `30c979595a4831aa`, `_LEARNING` `191cf5d71ebf3865`, `_CLOSE` `7d7707cfa2d336f7`, `_CLOSE_RICH` `3d709571e17ff405` |

**Canon `fa233f3`:** the new `f53d048` header paragraph, and `§0.FAILED-READ-CALLERS` answering **"none"** with the table in §0.

**WAL:** not in this pass. Still a candidate.

---

## 5. Confirmations: every write, in order

| # | write |
|---|---|
| 1 | `.bak` of `virtual_trader.py` (`…bak_lasttwo_20260921T185843Z`) |
| 2 | new `tests/test_recheck_and_advisor_close_failed_read.py` (one harness fix); scope pins in two earlier contracts; sandbox copies for botuser |
| 3 | patch `_run_recheck_tier` and `_advisor_close` (script-applied, anchor-checked; then one wording fix to the new alert) |
| 4 | `touch -a` on 6 `__pycache__/*.pyc` (atime only) |
| 5 | `systemctl restart titan.service`, gated on flat, **the only restart** |
| 6 | `git commit f53d048` in `/root` (not pushed) |
| 7 | canon `fa233f3`, pushed as botuser |

**Not done:**
- **0 orders placed or cancelled.** Venue calls were read-only.
- **No daemon-reload.**
- No DB writes.
- The ledger unchanged.
- **Mercury-SOL not touched.**

**Open for you:**
1. Keep the breaker trip on an unconfirmed critical close (§1c)? It is applied, per your ruling; reverting to alert-only is one line.
2. WAL, still a candidate.
