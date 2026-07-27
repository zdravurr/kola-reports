# three-zero-row-tables-traced

_2026-07-27 00:22 UTC_

---

# TITAN — the three zero-row tables, traced

**2026-07-27 00:30 UTC · READ-ONLY. No fixes.** Tree clean at `f0a8d30`.

**None of the three is the 15m class. Two share a single root cause, one is correct behaviour.**
And the `mfe_tracking` question has a clean answer: **`water_mark` is the right source, today's
excursion conclusions stand.**

---

## breakeven_jobs — **(b) LIVE-PATH ONLY**

```
breakeven_worker.enqueue()  <-  main.py:1407, inside _execute_entry (1226-1430)
```
It is called with `sl_order_id=sl_id` — a **real exchange stop-order id**. `_execute_entry` is the
live order path; in paper mode `virtual_trader` manages breakeven itself (`VIRTUAL BREAKEVEN
vpos=… SL→… (trail armed)`), never touching this queue.

**Zero rows is correct.** `LIVE_TRADING_ENABLED = False`, so the live entry path has never run.
The worker starts (`gunicorn.conf.py:109`) and polls an empty queue.

**→ Add to the live-parity list.** When live is enabled this becomes the mechanism that arms
breakeven, and it must be checked alongside the LONG partial and the recheck bound, which also live
only in the paper path.

---

## liquidity_sweep_state — **(d) NEVER TRIGGERED, and it cannot be with current alerts**

```python
# main.py:2976
if (action_field == 'context_update'
        and raw_signal_type in liquidity_sweep.SWEEP_TYPES):     # 'EQH' | 'EQL'
    return _handle_liquidity_sweep(...)
```
Both conditions must hold. Neither does:

* **`action_field == 'context_update'`** — Equal H. / Equal L. arrive on **`tf='5m'`**, and the
  router forces 5m to `execute_trade`. They can never present as a context update.
* **`raw_signal_type` must be `'EQH'`/`'EQL'`** — the payload is
  `{"action": "Equal H.", "task": "price_action", "tf": "5m"}`. **There is no `signal_type` field
  at all.**

The market event is not rare: **Equal H. 165 rows, Equal L. 139** — ~300 occurrences, all filed
as `5m_liquidity_ctx`. The handler is waiting for a payload shape TradingView is not configured to
send. **`EQH_EQL_SMART_TP_ENABLED = True` is irrelevant** — it is checked at main.py:2783, inside a
function that is never entered.

**Same silhouette as the 5m exit tier:** a live listener, a real market event, and a payload contract
neither side implements. Configuration, not code.

---

## mfe_tracking — **(d) NEVER TRIGGERED, downstream of the same root**

```
mfe_tracker.enqueue()  <-  main.py:2863, inside _handle_liquidity_sweep (2746-2912)
```
**Its only call site is inside the function above.** No sweep handled → no MFE job enqueued. It is
not independently broken; it is the second casualty of one unreachable branch.

Corroboration: `status='liquidity_sweep'` and `status='smart_tp_armed'` both appear in the code and
**never once in the database** — they were on the never-fired list in yesterday's sweep.

### Does this affect today's excursion work? **No — and the reason matters**

They measure **different things**:

| | measures | window |
|---|---|---|
| `virtual_positions.water_mark` | best favourable price **while the position is open** | entry → exit |
| `mfe_tracker` | best favourable price **after the close** — "missed PnL" if price kept running | exit → exit+60min |

`mfe_tracker.py`'s own docstring: *"Post-close MFE… starts a virtual tracker for
MFE_WINDOW_MINUTES."* It was built to judge **100% close vs partial-close + trail** — a post-exit
question.

**`water_mark` is the correct and only source for in-trade MFE**, and it is written on every poller
tick (`virtual_trader.py:1560-1564`) for every position. Nothing today read a substitute:
* the LONG-partial study, the exit-contract study and the giveback figures all used `water_mark`
  correctly;
* the *post-exit* question `mfe_tracker` was meant to answer has in fact been answered — by the
  post-exit observatory (36 positions, 175 drift samples), which is a strictly better instrument:
  five horizons out to 24h instead of one 60-minute window.

**mfe_tracker is redundant, not missing.** Had it been running it would have duplicated a worse
version of data we already hold.

---

## Summary

| table | class | root |
|---|---|---|
| `breakeven_jobs` | **(b) LIVE-PATH ONLY** | correct in paper; belongs on the live-parity list |
| `liquidity_sweep_state` | **(d) NEVER TRIGGERED** | handler requires `signal_type='EQH'/'EQL'` + `context_update`; alerts arrive as 5m `price_action` with no `signal_type`. ~300 real events discarded |
| `mfe_tracking` | **(d) NEVER TRIGGERED** | sole call site is inside the unreachable sweep handler |

**Nothing is class (c).** No writer that should be running has silently stopped. This is not another
15m-missing-write — that was a live path returning 200 without persisting; these are branches that
have never been entered.

**If you ever want the sweep path alive** — not proposed, and it touches the router, which is out of
scope — it needs the TradingView EQH/EQL alerts to carry an explicit `signal_type` and a task that
maps to `context_update`. That is an alert-configuration change on your side, not a code change on
mine, and it would revive both tables at once.

---

Nothing applied. Tree clean at `f0a8d30`; `titan.service`, `nginx`, `mercury-sol.service` healthy.
