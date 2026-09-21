# titan-failed-read-work-finished-breaker-last-callers-armed-exit

_2026-09-21 18:45 UTC_

---

# Titan: the failed-read work is finished for every caller that acts, bar one shared primitive. The BE emergency close now trips the entry breaker. 3663 and 4068 are migrated. Armed exits are labelled `armed_exit`. 🔴 And a correction: vpos 109 was a MECHANICAL armed exit, not an advisor decision.

**2026-09-21 · titan-bot HEAD `40aad46` (was `d070a5f`) · canon `82fd176` · Titan LIVE, real money · Mercury-SOL not touched**
*(File dated 18:45 so its path matches the one pre-registered in the canon; written and published at ~18:35 UTC.)*

`openitems_guard`: **EXIT=0** at the start. **EXIT=0** at the end, against `40aad46` and the updated canon.

---

## 0. First, the correction you need to decide on

**The vpos 109 ruling rests on a false fact, and the fact was mine.**

My 2026-09-21 17:20 report said vpos 109 was "closed by the advisor: `[EXIT-ADVISOR-LIVE] trigger=armed_exit … close=True`, then `ARMED_EXIT_CLOSE`". Reading the armed-exit path for §3 of this pass shows otherwise:

- **The armed exit is mechanical.** A 60m "Exit Signal" arms `exit_pending`. When an opposite confirm print arrives (for vpos 109, `Bearish I-CHOCH+`), both call sites run `_execute_armed_exit`, which **closes unconditionally**.
- **The advisor is consulted on that path, and its answer is thrown away:**
  - `consult_exit_advisor(_vp_armed, symbol, side, confirm_signal, 'armed_exit')` is called and its return value is **discarded**.
  - Its own docstring says it "can never close a position".
  - No armed-exit call site reads the verdict.
- **So for vpos 109 the advisor merely agreed** (`close=True` 0.72). Had it said hold, the position would have closed anyway.

**Your IN ruling was "the rule measures advisor DECISIONS". vpos 109 was not one.**

**What I did and did not do:**
- I did **not** change the ledger. That is your ruling to revisit.
- I recorded the correction in the canon (`§0.EXIT-ADVISOR-RULE`).
- **Without row 6:** 5 of 10, Σ **+1.0497R / +$1.72**. **With it (as ruled):** 6 of 10, Σ **+0.8798R / +$1.43**. The rule does not fire either way.

This is also why the new label in §3 is **`armed_exit`**, and not an advisor label.

---

## 1. The BE emergency close trips the entry breaker (your decision: yes)

**Change** (in `breakeven_worker._emergency_close` only):
- **Trigger:** the verification read says **POS_OPEN** or **POS_UNKNOWN**.
- **Action:** set `virtual_trader._UNSAFE_STATE['tripped'] = True`, with a detail that names the state and the contracts:
  - `… breakeven stop recreate failed and the emergency close left the position OPEN (0.0018 contracts)`
  - `… left the position UNKNOWN (position read FAILED — contracts unknown)`
- **Alert text:** unchanged.
- **POS_FLAT:** unchanged; the breaker is **not** tripped.
- **Safety wrapping:** the trip sits in its own `try`, so a failure to import `virtual_trader` cannot suppress the alert that follows.

| state | before (`d070a5f`) | after (`40aad46`) |
|---|---|---|
| POS_FLAT | ✅ "Emergency close executed" | **unchanged**, breaker NOT tripped (M1, M3) |
| POS_OPEN | "DID NOT FLATTEN" alert only; **entries continue** | same alert + **breaker TRIPPED**, all further entries refused (M4) |
| POS_UNKNOWN | "OUTCOME UNKNOWN" alert only; **entries continue** | same alert + **breaker TRIPPED** (M2, M6) |
| close order raised | "❌ CRITICAL" | **unchanged** (M5) |

**How the breaker is cleared: only by restarting the service.**
- `_UNSAFE_STATE` is an in-process dict, initialised `{'tripped': False, 'detail': None}` at import (`virtual_trader.py:133`).
- Nothing in the code resets it. The only read is `execute_entry`'s refusal (`virtual_trader.py:753`, `VIRTUAL ENTRY REFUSED … breaker is tripped — <detail>`).
- **This is the same breaker, and the same clearing path, as the entry failsafe.** A human checks the exchange, then restarts.

**Contract** (`tests/test_failed_read_never_reports_safety.py`, extended):
- M2, M4 and M6 now also assert the breaker is TRIPPED and its detail names the state; M4's also names 0.0018 contracts.
- M1 and M3 assert it is NOT tripped.
- **RED on `d070a5f`: M2 M4 M6 fail** (the breaker was never tripped). **GREEN: 15/15.** Both results hold as root and as botuser.

---

## 2. The last two callers: migrated

Both now read the side three-state with `_fetch_position_state(double_probe=True, attempts=2)`.

**`main._handle_5m_close_via_ai` (was `main.py:3663`)**

| state | before | after |
|---|---|---|
| POS_FLAT | "📋 5m Group B logged … no open position", row `group_b_logged` / `trend_reset` | **byte-identical** (V2) |
| POS_OPEN | consults, using the exchange's full position dict | **same.** It fetches the same full dict (upnl, timestamp) for the prompt, and falls back to the probe's dict only if that second read fails, which is still OPEN (V3). If unified fails but raw sees the position, it is now OPEN; the old code called it flat (V4). |
| POS_UNKNOWN | 🔴 treated as **"no open position"**, consultation silently skipped | "⚠️ 5m Group B — **position read FAILED** … the exit advisor was NOT consulted … the next exit signal or the hourly review consults again", row `position_read_failed`, journal line (V1) |

- **Paper mode:** its fallback is untouched.
- **If any checked side is UNKNOWN,** nothing is consulted: a side we cannot see could be the open one, or the second of two.

**`main._handle_liquidity_sweep` (was `main.py:4068`)**

| state | before | after |
|---|---|---|
| POS_FLAT | "💧 EQH sweep logged … No open LONG — nothing to close" | **byte-identical** (W2) |
| POS_OPEN | proceeds to the Smart-TP logic | **same** (W3). Only `pos is None` is read in the whole function (verified), so the probe's dict is enough. |
| POS_UNKNOWN | 🔴 "**No open LONG — nothing to close**" | "⚠️ … Position read FAILED for LONG — the sweep close was **NOT evaluated** (the book is not known, not flat)", status `sweep_read_failed` (W1) |

**Contract** (`tests/test_last_callers_and_armed_exit_label.py`, new):
- **What runs for real:** both handlers, the armed exit, `_execute_close_position`, the position reads, `POS_*` and `_SWEEP_TO_SIDE`, all lifted from `main.py` by AST. The new file and the `.bak` run side by side.
- **Fakes:** the exchange and the handlers' collaborators, as recorders only.
- **How "OPEN keeps the same dict" is proven:** a tracked dict records every key downstream code reads. The probe's own reduced dict can't produce that sequence.
- **Results:** **RED with the `.bak` as "new": V1 V4 W1 L1 L2 fail. GREEN: 13/13.** Both results hold as root and as botuser.

### 2d. Is there any remaining live caller of `_fetch_open_position` whose None branch acts?

**Yes, one: the shared primitive `main.py:1357` `_execute_close_position`.** Stated plainly:

- **What it does on a failed read:** it returns None, so the close is aborted.
- **Mostly harmless:** `virtual_trader._do_close` then keeps the row **OPEN** and the poller retries next tick, with the exchange stop still in place. **No safety is claimed.**
- **One place where it isn't:** the armed exit reports that None as "**Armed exit fired but no live position**", and it has **already cleared `exit_pending`**. On a failed read, an armed exit is therefore dropped, with a false message.
- **Why it's not in this pass:** migrating the primitive changes all 8 of its callers.

| caller | status |
|---|---|
| `virtual_trader._reconcile_passive_fill` | 🟢 `7798f51` |
| entry failsafe (`virtual_trader.py:207`), BE emergency close (`breakeven_worker.py:475`) | 🟢 `d070a5f` (+ breaker in `40aad46`) |
| `_handle_5m_close_via_ai`, `_handle_liquidity_sweep` | 🟢 `40aad46` |
| `main.py:3669` | `40aad46`'s own call, reached only after the double probe says OPEN; its None falls back to OPEN |
| `main.py:1357` `_execute_close_position` | 🟡 **the one remaining live actor.** Close aborted and retried; the armed exit's message and disarm are the visible defect. |
| `main.py:3926` `_handle_exit_signal`, `main.py:4340` trend reversal | ⚪ dead in live (`engine_owns_position()` is True) |
| `breakeven_worker.py:734`, `788`, `807` | ⚪ dormant (`breakeven_jobs` has had 0 rows ever) |
| `breakeven_worker.py:425` `move_stop_with_race_guard` | 🟢 benign (old stop held, retried) |

Canon `§0.FAILED-READ-CALLERS` now says exactly this.

---

## 3. The armed-exit label

- **Where it was written:** `main._execute_armed_exit` closed through `_execute_close_position(symbol, side)`. That routes to `virtual_trader.close_position`, whose default reason is `'external'`.
- **The change:** one argument, `_execute_close_position(symbol, side, reason='armed_exit')`.
- **Why `armed_exit`:** it names the mechanism that decides the close, which is `exit_pending` plus the confirm print.
  - It is **not** `ai_exit`, because the advisor's verdict is not used on this path (§0).
  - It is **not** `external`, because the close comes from inside the engine.
  - It matches the name the code already uses for this path: the consult trigger `'armed_exit'` and the journal tag `ARMED_EXIT_CLOSE`.
- **No historical rows rewritten.** vpos 95 and 109 keep `external`.

**Every consumer of `close_reason`, checked across `titan-bot/*.py`, `tools/`, the `.sh` watchers, `/root/*.py`, `/root/titan-bot/optimizer`, `retired_sensors`, and the botuser workspace:**

| consumer | effect of `armed_exit` |
|---|---|
| `virtual_trader._do_close` batch counter: counts only `('sl','trail','post_entry_critical','ai_exit')` | **unchanged behaviour.** `armed_exit` is not in the tuple, exactly as `external` wasn't, so the main.py armed-exit caller still counts the batch **once** (`main.py`, `_increment_batch_and_stamp` in `_execute_armed_exit`). **`ai_exit` would have double-counted.** Pinned by contract L3. |
| `close_report` card | prints the reason verbatim (`🏁 Close: armed_exit`) |
| `post_exit_observatory.real_close_reason` | stored verbatim (TEXT) |
| `risk_manager` (loss streak, daily loss) | filters on `status`/`net_pnl`, never on reason |
| `optimizer`, `silence_digest`, advisor prompts, `report.py`, cron watchers | **no reference to `close_reason`** |
| `§0.EXIT-ADVISOR-RULE` | canon text only; its clarified population keys on `close=True`, not on the label |

**Contract pins:**
- L1: the armed exit passes `reason='armed_exit'` (the `.bak` passes `external`).
- L2: all 6 other close calls in `main.py` are byte-identical to the `.bak`, and the default is still `external`.
- L3: `armed_exit` is not in the batch tuple.

---

## 4. Apply

**`.bak`s, taken before any change:** `main.py.bak_lastcallers_20260921T182539Z` (`00c8be297a8de922`) and `breakeven_worker.py.bak_lastcallers_20260921T182539Z` (`7bd67a06baadd054`), both byte-identical to the originals.

**AST:**
- `main.py`: 160 / 160 top-level nodes; differing: **`_handle_5m_close_via_ai`, `_execute_armed_exit`, `_handle_liquidity_sweep`**.
- `breakeven_worker.py`: 47 / 47; differing: **`_emergency_close`**.
- Nothing else.

**Flat at 18:30:56 UTC:**
- DB: 0 open `virtual_positions`, 0 `exit_pending`, 0 live `breakeven_jobs`.
- BingX, **both probes, empty error lists**: unified positions `[]`, raw `data: []`, unified open orders `[]`, raw `orders: []`.
- The only webhook in the previous 150 s was a 15m `HyperWave Signal Up` context print (18:30:08). It isn't an entry trigger, and nothing followed it.

**The restart, from flat:**
- `systemctl restart titan.service` at 18:31:10; active **18:31:13 UTC**.
- MainPID 3997369 → **4001002**; worker **4001096**.
- **NRestarts 0 → 0.** systemd does not count a manual restart; this was the only restart.
- **No daemon-reload.** The "changed on disk" warning is the global flag explained last pass.

**Boot line:**
```
2026-09-21T18:31:23.981 [TITAN] [TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
```
0 boot errors. Since the restart: 0 tracebacks, 0 `database is locked`, 0 failsafe lines, 0 `VPOS-FILL 🚨`.

**Proof the patches are loaded:**
- `main.cpython-312.pyc` recompiled at boot (18:31:13.56); `breakeven_worker.cpython-312.pyc` at 18:31:17.99. Both headers match the patched sources (`main` `d69fea17b4a93844`, `breakeven_worker` `5dd4b1fd0d9d9c0c`).
- Unmarshalled from the loaded `.pyc` files:
  - `_handle_5m_close_via_ai` names `_fetch_position_state` and `POS_UNKNOWN`, and carries `position_read_failed`.
  - `_handle_liquidity_sweep` carries `sweep_read_failed`.
  - `_emergency_close` names `_UNSAFE_STATE` and carries "OUTCOME UNKNOWN" and "DID NOT FLATTEN".
- The boot re-stamped the reset `atime`s of `config` and `claude_advisor` (18:31:14.86–.88).

**From the loaded bytecode, identical to before the restart (all 21 lines):**

| name | value |
|---|---|
| `SL_ATR_MULT` / `TRAIL_MULT_ATR` | 2.25 / 1.6875 |
| `EXIT_ADVISOR_DRYRUN` | **False** |
| `BOOK_GATE_DRYRUN` | **False** (`BOOK_GATE_ENABLED` True) |
| `BOOK_GATE_CLAUSE_A_ENABLED` / `_B_` | **True / False** |
| `LIVE_TRADING_ENABLED` / `ORDER_ADAPTER_LIVE` | True / True |
| `CONFLUENCE_SCORE_THRESHOLD` / `_FLAT_` | 3.0 / 5.0 |
| size | `LIVE_FIXED_MARGIN_USDT` 30.0 × `LEVERAGE` 5 = $150 (boot banner); `MAX_POSITIONS_PER_SIDE` 1 |
| `_ENTRY_SYSTEM` / `_LEARNING_SYSTEM` | `30c979595a4831aa` / `191cf5d71ebf3865` |
| `_CLOSE_SYSTEM` / `_CLOSE_SYSTEM_RICH` | `7d7707cfa2d336f7` / `3d709571e17ff405` |

**All three contracts, root AND botuser** (sha256-pinned copies in `/tmp/titan-contract-lastcallers`), live `trades.db` opened **0 times** (kernel `openat` trace on every root run):

| contract | RED | GREEN |
|---|---|---|
| `test_failed_read_never_reports_safety` | on `d070a5f`: **M2 M4 M6** | **15/15** |
| `test_last_callers_and_armed_exit_label` | with the `.bak` as new: **V1 V4 W1 L1 L2** | **13/13** |
| `test_vpos_fill_failed_read_is_not_flat` | (unchanged) | **19/19** |

Two test-harness fixes during this pass, stated so nothing looks cleaner than it was:
- **The handlers return `(jsonify(...), 200)`.** I normalised the tuple in the harness.
- **V3's first form compared every key read**, including the new probe's own reads. I narrowed it to the reads made downstream of the check.

**Canon `82fd176`:**
- the new `40aad46` header paragraph;
- `§0.FAILED-READ-CALLERS` states the one remaining live actor (`_execute_close_position`) and lists the dead and dormant callers;
- `§0.EXIT-ADVISOR-RULE` records the label fix and **the vpos 109 correction**.

**WAL** stays named as a candidate. It is not in this pass.

---

## 5. Confirmations: every write, in order

| # | write |
|---|---|
| 1 | `.bak` of `main.py` and `breakeven_worker.py` (`…bak_lastcallers_20260921T182539Z`) |
| 2 | extend `tests/test_failed_read_never_reports_safety.py`; new `tests/test_last_callers_and_armed_exit_label.py`; sandbox copies for botuser |
| 3 | `breakeven_worker._emergency_close`: breaker trip |
| 4 | `main._handle_5m_close_via_ai`, `main._handle_liquidity_sweep`: three-state reads |
| 5 | `main._execute_armed_exit`: `reason='armed_exit'` |
| 6 | `touch -a` on 6 `__pycache__/*.pyc` (atime only) |
| 7 | `systemctl restart titan.service`, from flat, **the only restart** |
| 8 | `git commit 40aad46` in `/root` (not pushed) |
| 9 | canon `82fd176`, pushed as botuser |

**Not done:**
- **0 orders placed or cancelled.** Venue calls were read-only.
- **No daemon-reload.**
- No DB writes this pass.
- Historical `close_reason` rows untouched.
- The ledger not changed.
- **Mercury-SOL not touched.**

**Open for you:**
1. **vpos 109:** keep it IN, or take it OUT now that it's known to be a mechanical armed exit (§0)? 5/10 +1.0497R vs 6/10 +0.8798R.
2. The shared primitive `_execute_close_position`, and with it the armed exit's false "no live position" plus disarm on a failed read (§2d). That is its own pass.
3. WAL, still a candidate.
