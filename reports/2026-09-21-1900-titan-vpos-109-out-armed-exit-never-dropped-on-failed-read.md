# titan-vpos-109-out-armed-exit-never-dropped-on-failed-read

_2026-09-21 19:00 UTC_

---

# Titan: vpos 109 is OUT of the exit-advisor ledger (5 of 10, Σ +1.0497R). The armed exit is never dropped on a failed read. 🔴 Two paths inside virtual_trader still drop a close on a failed read, so the answer is NOT "none".

**2026-09-21 · titan-bot HEAD `07f9025` (was `40aad46`) · canon `8423b5d` · Titan LIVE, real money · Mercury-SOL not touched**
*(File dated 19:00 so its path matches the one pre-registered in the canon; written and published at ~18:55 UTC.)*

`openitems_guard`: **EXIT=0** at the start. **EXIT=0** at the end, against `07f9025` and the updated canon.

---

## 0. Summary

| item | result |
|---|---|
| §1 vpos 109 | **OUT.** Ledger **5 of 10, Σ +1.0497R / +$1.72.** Row 6 is kept below the table, struck out, with the reason. The population is restated as `close_reason='ai_exit'` (the verdict decided the close). **Both rulings are on record**, including that OUT moves the sum *in* the advisor's favour. vpos 95 is excluded under the same definition. |
| new evidence | **vpos 99: the advisor said `hold` (0.62) at 08:45:08, and the armed exit closed the position at 08:45:16 anyway.** That is live proof that the verdict is discarded on that path. |
| §2 armed exit | **Fixed** (`07f9025`). `exit_pending` is cleared only once the close outcome is known.<br>A failed read now keeps the arm and alerts. OPEN retries the close. A true flat is byte-identical to before. |
| §2a choice | Option (i), **plus the same fix in one more live caller.** (i) alone left `_handle_5m_close_via_ai` wrong: it dropped the advisor's close and said "Position vanished".<br>(ii) would change all 8 callers, and one concrete form of it bypasses `40aad46`'s breaker (§2a). |
| contracts | New: **RED on `40aad46` (A1 A3 A4 B1 B3 O), GREEN 12/12.** The three earlier contracts **stay GREEN (13/15/19)**. All four hold as root **and** as botuser, and a kernel trace shows **0 opens of the live DB**. |
| §2e | **Not "none".** Two live paths in `virtual_trader` still drop a close on a failed read: `_advisor_close` and the post-entry recheck's critical close (§2e). |
| apply | Flat (incl. 0 `exit_pending`), `.bak` first. AST: 2 functions only. One from-flat restart at **18:49:23 UTC**. Boot `RECONCILE-XDB ✅ 0/0`. Every guarded value is identical in the loaded bytecode. |

---

## 1. vpos 109: OUT

### 1a. The ledger, reverted

| # | vpos | side | closed | advisor R ($) | counterfactual | cf R ($) | Δ R | Δ $ |
|---|---|---|---|---|---|---|---|---|
| 1 | 101 | SHORT | 09-01 18:00 | +0.2956 (+0.57) | trail 77 124.0 | +0.4509 (+0.87) | −0.1553 | −0.30 |
| 2 | 104 | LONG | 09-09 08:30 | +0.5757 (+0.79) | sl 78 350.1 | −1.1033 (−1.51) | +1.6791 | +2.30 |
| 3 | 105 | SHORT | 09-09 23:46 | −0.0136 (−0.03) | trail 77 393.9 | +0.7669 (+1.50) | −0.7805 | −1.53 |
| 4 | 106 | SHORT | 09-12 09:15 | −0.2963 (−0.72) | sl 78 301.6 | −1.0603 (−2.59) | +0.7640 | +1.87 |
| 5 | 108 | LONG | 09-14 17:00 | +1.1371 (+1.54) | trail 79 024.4 | +1.5947 (+2.15) | −0.4576 | −0.62 |
| | | | | | | **Σ (5 of 10)** | **+1.0497** | **+$1.72** |

~~6 · vpos 109 · LONG · 09-18 23:45 · +2.0051 (+3.43) · trail 81 018.9 · +2.1750 (+3.72) · −0.1699 · −0.29~~
**Struck out.** A mechanical armed exit: the advisor's `close=True` was consulted and discarded, and was not the reason for the close. It was IN from the first ruling (canon `053f5ff`) until now; with it the sum was +0.8798R.

The rule does not fire. `EXIT_ADVISOR_DRYRUN` stays **False**. **Five more resolved closes are required.**

### 1b. The population, restated (canon, verbatim)

> every LIVE close from vpos 101 onward where the ADVISOR'S VERDICT DETERMINED THE CLOSE — i.e. `close_reason = 'ai_exit'` (written only by `virtual_trader._advisor_close` and the 5m advisor-close path, both of which close ON the verdict). **An advisor consultation whose verdict is discarded does not qualify.**

**The live proof, from the `trades` table:**
- **vpos 99:** consult row **28402 at 08:45:08, `hold` 0.62**, followed by **28403 `15m_armed_exit` `executed` at 08:45:16**. The position closed against the advisor's verdict.
- **vpos 109:** 33670 `close` 0.72, then 33671 `15m_armed_exit` `executed`.
- **vpos 95:** 26626 `close` 0.72, then 26628 `15m_armed_exit` `executed`.

There are 4 executed armed-exit rows since 2026-07-28.

### 1c. Both rulings, so the reversal is visible

- **First ruling (IN):** justified as adding a **negative** row, "the conservative direction".
- **Second ruling (OUT):** moves the sum **+0.1699R in the advisor's favour, the opposite direction.**
- **Why the second:** factual population membership. vpos 109 was not an advisor decision. It is not a selection on outcome: had its Δ been positive, it would leave just the same.

Both are recorded in canon `§0.EXIT-ADVISOR-RULE`.

### 1d. vpos 95

Under the same definition, vpos 95 is also a mechanical armed exit (`close_reason='external'`). **It is not an advisor decision, so it belongs to neither population.**

It was never in the OLD population either: that population is `ai_exit` closes before vpos 101, and vpos 95's reason is `external`. **Status: excluded, unchanged.**

---

## 2. The armed exit that dropped itself

### 2a. Where to fix it: option (i), plus the same fix in one more live caller

**Option (i) alone would leave another live caller wrong.** `main._handle_5m_close_via_ai` (the 5m advisor close) is reachable in live because `EXIT_ADVISOR_DRYRUN = False`. On a None it wrote row status `no_position` and sent "**📋 Position vanished before close**". On a failed read, that drops the advisor's close and states a false fact.

**Option (ii), migrating the primitive, costs:**
- All 8 callers of `_execute_close_position` change behaviour, including the poller's stop and trail closes, which run through every position.
- **A concrete regression in one form of it:** an exception-style primitive would send the BE emergency close into its `except` path. That path sends "❌ CRITICAL" but skips the `_UNSAFE_STATE` trip that `40aad46` just added. Contract M2 would fail.
- Every migrated caller's contract would need re-deriving.

**What I did:** applied the (i) pattern to **both** live `main.py` callers whose None branch cleared state or made a claim: `_execute_armed_exit` and `_handle_5m_close_via_ai`. That is a third option you didn't list. It is smaller than (ii), and it leaves no `main.py` caller wrong.

**What's left:** two paths inside `virtual_trader` that (i) cannot reach (§2e).

### 2b. The order, line by line

**Before (`40aad46`):**
```
1  consult_exit_advisor(... 'armed_exit')            # verdict discarded
2  try: close = _execute_close_position(..., reason='armed_exit')
3  except: … return 500                               # exit_pending NOT cleared (fine)
4  state_machine.clear_exit_pending(side)             # 🔴 cleared UNCONDITIONALLY — outcome unknown
5  if close is None: "Armed exit fired but no live position"; return   # 🔴 false on a failed read
6  … close report, batch count …
```

**After (`07f9025`):**
```
1  consult_exit_advisor(... 'armed_exit')            # unchanged
2  try: close = _execute_close_position(..., reason='armed_exit')
3  except: … return 500                               # unchanged, arm kept
4  if close is None:
5      state = _fetch_position_state(side, double_probe=True, attempts=2)
6      if state == OPEN: close = retry _execute_close_position(...)   # one retry
7      if close is None and state != FLAT:
8          "⚠️ ARMED EXIT — close NOT confirmed … exit_pending is kept ARMED" ; return 'close_unconfirmed'
9  state_machine.clear_exit_pending(side)             # ✅ only now — outcome KNOWN
10 if close is None: "Armed exit fired but no live position"; return   # reached only on a CONFIRMED flat
11 … close report, batch count …                      # unchanged
```

Contract check [O] proves it from the AST: **every `clear_exit_pending` in the function sits after the first `close is None`.**

| state after a None close | before | after |
|---|---|---|
| POS_FLAT (confirmed) | arm cleared, "no live position" | **byte-identical** (A2) |
| POS_OPEN | 🔴 arm cleared, "no live position": **exit dropped** | close **retried**. On success: arm cleared after it, normal close report (A3). Still not closed: **arm kept**, "NOT confirmed … still OPEN after a retry" (A4). |
| POS_UNKNOWN | 🔴 arm cleared, "no live position": **exit dropped** | **arm kept**, "⚠️ ARMED EXIT — close NOT confirmed … the position read FAILED … exit_pending is kept ARMED: the next confirm print retries" (A1) |
| close raised | error, arm kept | **unchanged** (A5) |

**The 5m advisor close gets the same shape:**
- **FLAT:** today's `no_position` row and "Position vanished" message, byte-identical (B2).
- **OPEN:** retried (B3).
- **UNKNOWN, or still not closed:** row `close_unconfirmed` and "⚠️ AI CLOSE NOT confirmed … the advisor's close did not execute; the exchange stop is still the backstop and the next verdict decides" (B1).

### 2c. Contract: `tests/test_close_not_dropped_on_failed_read.py`

**What is real and what is faked:**
- **Real code, lifted from `main.py` by AST (new and `.bak`):** both callers, the primitive `_execute_close_position` (with `fetch_order_fee` and `_cancel_stop_orders`), the position reads and `POS_*`.
- **The engine's `close_position` is faked the way the live chain works:** straight into the real primitive with `_from_adapter=True`.
- **Faked:** the exchange and sleep; recorders for Telegram, rows and the state machine.
- **The live DB:** `TITAN_PEO_AUTO_INIT=0`, every `trades.db` connect redirected, and the kernel `openat` trace shows **0 opens** on every run.

| run | root | botuser (pinned copies, `/tmp/titan-contract-closedrop`) |
|---|---|---|
| **RED**, `40aad46` as "new" | **FAIL A1 A3 A4 B1 B3 O**; A2 A5 B2 pass (the byte-identical pins) | **same 6 FAIL** |
| **GREEN**, `07f9025` | **12 / 12** | **12 / 12** |

### 2d. The three existing contracts: all still GREEN

| contract | root | botuser |
|---|---|---|
| `test_last_callers_and_armed_exit_label` | 13 / 13 | 13 / 13 |
| `test_failed_read_never_reports_safety` | 15 / 15 | 15 / 15 |
| `test_vpos_fill_failed_read_is_not_flat` | 19 / 19 | 19 / 19 |

**One pin changed in `test_last_callers_and_armed_exit_label`.** L2 compared the list of close calls exactly. The retries add a second, byte-identical call in each fixed function, so it now compares the **distinct call signatures**. Any changed or new call still fails it.

**Two harness fakes were added to the new contract** (`microstructure.kick_off_capture` and `virtual_trader.set_close_trade_row`). The success path calls them before the batch count.

### 2e. Is there ANY remaining live caller whose None branch drops an action or claims a fact?

**Yes, two. I can't prove "none", because it isn't true.**

**Fixed in `07f9025`:**
- the armed exit;
- the 5m advisor close.

**Remaining, both in `virtual_trader`,** both reached through `_do_close → order_adapter.market_close → _execute_close_position(_from_adapter=True)`:

1. **`_advisor_close`**, the hourly and 15m advisor exits, i.e. **the `ai_exit` population itself.**
   - **On None it logs:** "no live position to close — left for passive-fill reconciliation, NOT retried", to the journal only.
   - **On a failed read:** the advisor's close is **dropped until its next verdict (≤ 1 h)**, and the journal line states a false fact.
   - **Mitigations:** the row stays OPEN and the exchange stop stays in place.
2. **`_run_recheck_tier`, the post-entry critical close.** Verified this pass:
   - **Before the close:** it writes `recheck_status='closed_critical'` and sends "🛑 Post-entry T+Ns — EMERGENCY CLOSE", then calls `_do_close`.
   - **On a failed read:** the close aborts, and the tier never re-fires because it's already marked.
   - **Result:** a critical close is **dropped, under a message saying it happened.**

**Deferrals only, no drop and no claim:** the poller's stop, trail and breakeven closes. The trigger persists, so they retry next tick.

**Dead in live:**
- the trend-reversal close (`TREND_REVERSAL_EXIT_DRYRUN = True`);
- the Smart-TP sweep close (`EQH_EQL_SMART_TP_ENABLED = False`);
- the legacy SL-failsafe in `main._execute_entry`, which returns into the engine first. It sends "✅ Emergency close executed" unconditionally, the same defect `d070a5f` fixed elsewhere, but it cannot run while `engine_owns_position()` is True.

Canon `§0.FAILED-READ-CALLERS` states exactly this.

---

## 3. Apply

**`.bak` before any change:** `main.py.bak_closedrop_20260921T184709Z` (`d69fea17b4a93844`, byte-identical to the original). `main.py` is the only source file touched: `d69fea17b4a93844` → `7298f0d6daf12820`.

**AST:** `main.py` 160 / 160 top-level nodes; differing: **`_handle_5m_close_via_ai`, `_execute_armed_exit`**. Nothing else.

**Flat at 18:49:12 UTC:**
- DB: 0 open `virtual_positions`, **0 `exit_pending`**, 0 live `breakeven_jobs`.
- BingX, **both probes, empty error lists**: unified positions `[]`, raw `data: []`, unified open orders `[]`, raw `orders: []`.
- No webhook or entry in the preceding 2 minutes.

**The restart:**
- `systemctl restart titan.service` at 18:49:20; active **18:49:23 UTC**.
- MainPID 4001002 → **4004539**; worker **4004551**.
- **NRestarts 0 → 0.** systemd does not count a manual restart; this was the only restart.
- **No daemon-reload.**

**Boot line:**
```
2026-09-21T18:49:31.277 [TITAN] [TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
```
0 boot errors. Since the restart: 0 tracebacks, 0 lock errors, 0 failsafe lines, 0 `ARMED_EXIT_UNCONFIRMED`.

**Proof the patch is loaded:**
- `main.cpython-312.pyc` was recompiled at boot (18:49:23.76); header matches source.
- Unmarshalled from it: `_execute_armed_exit` names `_fetch_position_state` and carries `close_unconfirmed` / "kept ARMED". `_handle_5m_close_via_ai` carries `close_unconfirmed` / "AI CLOSE NOT confirmed".
- `config` and `claude_advisor` `atime`s were re-stamped at boot (18:49:24.81–.82).

**From the loaded bytecode, identical to before the restart (all 21 lines):**

| name | value |
|---|---|
| `SL_ATR_MULT` / `TRAIL_MULT_ATR` | 2.25 / 1.6875 |
| `EXIT_ADVISOR_DRYRUN` | **False** |
| `BOOK_GATE_DRYRUN` | **False** |
| `BOOK_GATE_CLAUSE_A_ENABLED` / `_B_` | **True / False** |
| `LIVE_TRADING_ENABLED` / `ORDER_ADAPTER_LIVE` | True / True |
| size | `LIVE_FIXED_MARGIN_USDT` 30.0 × `LEVERAGE` 5; `MAX_POSITIONS_PER_SIDE` 1 |
| advisor SYSTEM prompts (sha256) | `_ENTRY` `30c979595a4831aa`, `_LEARNING` `191cf5d71ebf3865`, `_CLOSE` `7d7707cfa2d336f7`, `_CLOSE_RICH` `3d709571e17ff405` |

**Canon `8423b5d`:**
- the new `07f9025` header paragraph;
- `§0.EXIT-ADVISOR-RULE`: second ruling, population restated, both rulings recorded, vpos 99 proof, vpos 95 status, ledger 5/10 with row 6 struck out;
- `§0.FAILED-READ-CALLERS`: the two remaining paths, plus the deferrals and dead callers.

**WAL:** not in this pass. Still named as a candidate.

---

## 4. Confirmations: every write, in order

| # | write |
|---|---|
| 1 | `.bak` of `main.py` (`…bak_closedrop_20260921T184709Z`) |
| 2 | new `tests/test_close_not_dropped_on_failed_read.py`; L2 pin in `tests/test_last_callers_and_armed_exit_label.py`; sandbox copies for botuser |
| 3 | `main._execute_armed_exit` and `main._handle_5m_close_via_ai` |
| 4 | `touch -a` on 6 `__pycache__/*.pyc` (atime only) |
| 5 | `systemctl restart titan.service`, from flat, **the only restart** |
| 6 | `git commit 07f9025` in `/root` (not pushed) |
| 7 | canon `8423b5d`, pushed as botuser |

**Not done:**
- **0 orders placed or cancelled.** Venue calls were read-only.
- **No daemon-reload.**
- No DB writes.
- **Mercury-SOL not touched.**

**Open for you:**
1. The two remaining `virtual_trader` paths (§2e). The recheck critical close is the more dangerous: it announces an emergency close that can silently not happen, and it never re-fires.
2. WAL, still a candidate.
