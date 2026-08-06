# SOL — FINAL PRE-FLIP VERIFICATION. READ-ONLY STATE AUDIT BEFORE REAL MONEY.

**2026-08-06 16:25 UTC · Mercury-SOL · READ-ONLY. NOTHING WAS CHANGED.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`, worker **2742565**.
Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched.**

---

## THE VERDICT FIRST

> ### SOL is ready to flip. Everything reported closed is genuinely loaded in the running worker, and the four open items are all correctly rated as accept-or-latent.
>
> ### 🔴 But "ready" here means *the code is right*, not *the code has been exercised*. **Nine mechanisms on the live path have never executed a single time against Bybit.** §6 names them. The first live trade is a test, and it should be watched as one.

---

# 1. IS EVERYTHING ACTUALLY LOADED IN THE WORKER? — **YES**

## a) The boot line, from the current worker

```
Aug 06 16:05:58  mercury-sol[2742565]: [MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5
                 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h OBSERVATION_MODE=True [pid 2742565]
```

```
master 2742517  started 16:05:43        worker 2742565  forked 16:05:58        NRestarts=0
```

**`[pid 2742565]` in the line == the running worker's pid.** The line was built for exactly this
question and it answers it in one glance — no `.pyc` archaeology required, unlike at 15:10.

## b) Every file changed today — `.pyc` validated, source older than the fork

| module | src mtime | pyc header | validated | src < fork |
|---|---|---|---|---|
| `main.py` | 15:46:27 | 15:46:27 | ✅ | ✅ |
| `claude_advisor.py` | 16:05:22 | 16:05:22 | ✅ | ✅ |
| `virtual_trader.py` | 15:18:01 | 15:18:01 | ✅ | ✅ |
| `config.py` | 15:19:24 | 15:19:24 | ✅ | ✅ |
| `tor_retry.py` | 15:45:18 | 15:45:18 | ✅ | ✅ |
| `optimizer.py` | 15:18:55 | 15:18:55 | ✅ | ✅ |

`gunicorn_mercury.conf.py` is **exec'd by gunicorn, not imported**, so it has no `.pyc`; its mtime
**15:21:06** precedes the master's start **16:05:43**, so the `post_fork` hook running today is the
current one — which the boot line itself proves, since that hook is what emits it.

## c) Anything edited after the last restart

```
find . -newermt "2026-08-06 16:05:43"  →  (empty)
```

**Nothing.** The 25-minute disk-vs-worker divergence of 14:30 has no counterpart in the current state.

---

# 2. 🔴 THE FOUR RECORDED-BUT-NOT-CLOSED ITEMS — RE-RATED FOR THE FLIP

## a) F2 — the retired monitor's `sl_triggered_{side}` write · **UNREACHABLE, STRUCTURALLY. Closed.**

Not "retired by comment" — **dead by call graph**:

* the write is at **`main.py:4859`**, inside `_monitor_positions` (`4810` → next top-level def `4988`);
* **`_monitor_positions` has NO caller.** Every remaining reference in the tree is a comment;
* the one thing that used to start it, `start_monitor()`, is now a **no-op that only prints**:

> *"RETIRED 2026-08-01 (Phase 2) — ONE MANAGER, TWO ADAPTERS… Kept as a NO-OP rather than deleted:
> post_fork calls it, and a hard removal would let a future re-add silently resurrect a second manager."*

**RATING: not a flip risk.** It cannot emit a label because it cannot run. Keeping the no-op is the
right call — it is a tripwire against a second manager, not dead weight.

## b) M4 follow-up — the unratcheted trail, **in dollars at $100 notional**

Live sizing, computed from the loaded config:

```
LIVE_FIXED_MARGIN 20 × LEVERAGE 5 = $100 notional
at SOL ~$73:  1.3699 → quantised DOWN (0.1 step) = 1.3 SOL
1R = SL_BUFFER_ATR 2.5 × ATR(1h) 0.4032 × 1.3 SOL = $1.31
trail giveback 0.75R = $0.98
```
*(ATR(1h) 0.4032 = mean since 2026-08-01, n=438; range 0.2639–0.4929.)*

**The worst case is bounded below by breakeven, and it is small in dollars:**

| MFE reached | engine alive (exit ≈ MFE − 0.75R) | process dead (exit = breakeven) | **given up** |
|---|---|---|---|
| 1.0R | 0.25R = $0.33 | $0.00 | **$0.33** |
| 2.0R | 1.25R = $1.64 | $0.00 | **$1.64** |
| 3.0R | 2.25R = $2.95 | $0.00 | **$2.95** |

> **The position can never turn into a LOSS from this defect.** Once the trail arms, `ENABLE_BREAKEVEN_LOCK`
> has already moved the venue stop to entry + round-trip fees, and that stop is a **position-level
> attribute that survives the process dying**. What is lost is open profit above breakeven, nothing more.
>
> 🔴 **The one thing to be precise about: this protection begins only at +1R.** If the process dies
> *before* the trail arms, the venue stop is still the full ATR stop and the exposure is the full
> **1R = $1.31**. That is the designed risk, not a defect.

**RATING: correctly accepted. At $100 notional the worst realistic give-up is a few dollars.** Revisit
if notional grows — the number scales linearly, so at $10,000 notional the 3R case is ~$295.

## c) `_smart_boot_cleanup`'s POS_FLAT assumption · **DOWNGRADED — the blast radius is structurally bounded**

The concern was right in form: `has_open = any(contracts > 0)` treats a **successful-but-empty or stale**
`fetch_positions` as FLAT, and then calls `_cancel_stop_orders`. That assumption is still there and
Bybit still has not been exercised live.

**But what a false FLAT can actually reach is now near-nothing**, and for a reason recorded in the code:

```python
# _cancel_stop_orders → POST /v5/order/cancel-all with orderFilter='StopOrder'
```

That targets **conditional/trigger ORDERS**. Since B1, the engine's protection is a **position-level
`/v5/position/trading-stop` attribute — not an order.** A cancel-all of StopOrders **cannot clear it.**

**And the other POS_FLAT consumer is protected differently and independently:** the engine's
`_process_position` FLAT branch routes to `_book_exchange_close`, which **refuses to book a close it
cannot substantiate** — a false FLAT finds no matching fill, returns `None`, and leaves the row OPEN
rather than fabricating a close.

**RATING: latent, LOW, and no longer the same defect it was at 13:00.** Two independent structural
protections stand between a false FLAT and any destructive action. **Residual risk:** a false FLAT
while a position is genuinely open would cancel any *other* conditional orders on the symbol and would
skip the "position open, stops preserved" alert — a visibility loss, not a protection loss.
**Not a flip blocker. Worth one look at the first live boot** (the `[SMART-CLEANUP]` line is printed
either way, so the journal will say which branch ran).

## d) `ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN` · **STILL SHADOW. Does not matter at the flip — with one caveat.**

```python
ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True   # compute fresh ATR at +1R, LOG fresh-vs-frozen,
                                         # but PLACE the FROZEN trail_pct (zero behavioural change)
```

Still `True`, and the flag is **mode-independent** — it behaves identically in paper and live, so the
flip changes nothing about it. The trail the engine enforces stays the value frozen at entry. **No flip
surprise: this is exactly what paper has been doing.**

🔶 **The caveat worth stating:** even in shadow it makes a **live network call**
(`compute_fresh_trail_pct(exchange, …)`) at the moment of +1R arming — on the Tor link, on the money
path, purely to log a comparison. It is wrapped in `try/except` and a failure keeps the frozen value,
so it cannot break the arming. But it is a non-free call at the busiest moment in the position's life.
**Not a blocker; flag it if arming ever looks slow on the live link.**

---

# 3. WHAT NO SINGLE PASS COULD SEE — THE INTERACTIONS

## a) ONE COMPLETE LIVE ENTRY, end to end, through the CURRENT code

```
webhook /webhook/sol
  └─ … cascade gate → score gate → risk gates (loss-streak, daily-loss brake) → advisor
      └─ _execute_single_entry(symbol, side, position_side, row_id, clusters)
          │
          ├─ if OBSERVATION_MODE: → virtual_trader.execute_entry … RETURN   ← 🔴 THE FORK (main.py:2173)
          │                                                                   everything below is UNRUN
          ├─ stop_loss.quantise_amount(...)             → 1.3 SOL (rounds DOWN, refuses below min)
          ├─ _idem_entry = f'sol-e-{row_id}'
          ├─ tor_retry.with_socks_retry_write(          ← M5
          │     call        = ex.create_market_order(..., clientOrderId=k)
          │     find_existing = _entry_exists ──► tor_retry.find_order_by_client_id
          │                                        (fetch_open_orders + fetch_closed_orders)
          │  )   ├─ DuplicateSuppressed  → 🚨 alert, NO second order, raise
          │      └─ WriteUnconfirmed     → 🚨 alert, NO second order, raise      ← M5
          │
          ├─ 🔴 _place_sl_with_retry(...) → _move_stop_to → /v5/position/trading-stop   ← M1: PROTECT…
          ├─ _read_entry_fill(...)                                                      ← …BEFORE DESCRIBE
          ├─ _resolve_fee(...)
          └─ virtual_trader.book_live_position(..., is_paper=0)   ← "never refuses, never raises"
                └─ engine picks it up: _worker_loop → _process_position
                      ├─ _reconcile / _live_pos_state
                      ├─ water mark → +1R arm → breakeven lock (_move_stop_to)
                      ├─ adaptive_trail.compute_fresh_trail_pct  (shadow)
                      ├─ _apply_partial_at_arm → _execute_partial_close
                      └─ trail / SL / timeout / exit → _exec_close → _do…close_position
```

**Where two of today's changes MEET — the interaction sites:**

1. **M5 × M1.** The M5 probe can now **raise `WriteUnconfirmed` before the stop is placed.** This is
   safe and is the *correct* ordering: the raise happens when the order's fate is unknown, so there may
   be no position to protect, and M1's guarantee ("stop before fill read") is unaffected — it is
   downstream of a *successful* order. **No conflict; the alert explicitly tells the operator to check
   for a position and its stop manually, which is precisely the state M1 exists to prevent silently.**
2. **M5 × the entry idempotency key.** `_idem_entry` is derived from `row_id`, which is stable across
   retries of this entry — so the probe and the key name the same object. ✅
3. **F1 × M4.** M4 deleted the venue trail; F1 mapped `tp`/`liquidation`/etc. Neither touches the
   other's surface — F1 is a label map, M4 removed an order. ✅
4. **P2 × everything.** The trail constant is read only by the engine's trail trigger and
   `adaptive_trail`. It reaches no order path. ✅

## b) ONE COMPLETE LIVE CLOSE, and ONE PARTIAL AT +1R

```
CLOSE   _exec_close(row,…) ─ not _is_paper ─► _live_close → _execute_close_position
          ├─ _fetch_position_state              (POS_OPEN / POS_FLAT / POS_UNKNOWN)
          ├─ _idem = f'sol-c-{side}-{epoch}'
          ├─ with_socks_retry_write(create_market_order(reduceOnly=True, …),
          │                          find_existing=_close_exists)          ← M5
          ├─ _cancel_open_orders_for_side(...)                             ← M3
          └─ back into virtual_trader._do…close_position
                ├─ gross_pnl += partial_pnl + partial_fees                 ← P1
                ├─ label = _close_label_for(reason, side)                  ← F1 (never raises/refuses)
                │     'trail' → trail_{s}                                  ← G2c
                │     venue reasons → own labels; unknown → unmapped_close_{s}
                ├─ UPDATE virtual_positions … close_reason = <literal>
                └─ INSERT INTO trades … signal_type = <label>  → optimizer pairs it  ← F1(c)/G2c

PARTIAL _apply_partial_at_arm → _execute_partial_close
          ├─ stop_loss.quantise_amount → 0.4 SOL (of 1.3, rounds DOWN)
          ├─ _idem = f'sol-p-{vpos_id}'
          ├─ with_socks_retry_write(…reduceOnly=True…, find_existing=_partial_exists)  ← M5
          └─ filled read back off the order → the REALISED fraction drives the fee split ← F3
```

**Interaction sites here:**

5. **P1 × F3.** P1 folds `partial_pnl + partial_fees` into `gross_pnl`; F3 makes the partial's
   *realised* size authoritative. They compose: P1 consumes the stored `partial_pnl`/`partial_fees`,
   which F3 already wrote from the real fill. **Proven by execution on vpos 25 — `Gross − Fees == Net`
   to 0.000000.** ✅
6. **M5 × F3.** If the partial's write is **adopted** from the venue rather than re-placed, the caller
   still reads `filled` off the **adopted** order — so the realised size is the one that actually
   reduced. **The two changes reinforce each other rather than collide.** ✅
7. **F1 × G2c × the optimizer.** Every label the close path can now emit — `trail_*` plus the seven
   F1 labels — is registered in `optimizer._CLOSE_*_TYPES`. **Nothing the close path can emit is
   unpairable.** ✅

## c) Does any change assume a state another change removed?

| change | removed / added | does anything still assume the old state? |
|---|---|---|
| **M4** deleted the native venue trail | no venue trail object | **No.** `trail_pct` is consumed only by the engine's own trigger and `adaptive_trail`; nothing reads a venue trail back. This was the M4 finding itself — the deleted thing was *never read back*. |
| **F1/G2c** grew the label map | 7 new labels | **No.** All registered with the optimizer in the same edits; historical `sl_triggered_*` rows still pair. |
| **M5** made `find_existing` required | new required kwarg | **No** — see (d), enforced by the interpreter. |
| **F1** removed `close_position`'s refusal guard | unknown reasons now BOOK | **One behaviour genuinely changed, and it is the intended one:** a caller that previously got `None` for an unrecognised reason now gets a booked close. No caller depended on the refusal — `_poller_close` simply skips the card on `None`, and the live FLAT branch retried forever, which was the defect. **The reason is descriptive, never a decision, so booking is always right.** |

**No change assumes a state another change removed.**

## d) 🔴 `find_existing` — confirmed unbypassable, by execution

```
$ grep -rn "with_socks_retry_write" --include=*.py .
main.py:2249  · main.py:2643  · main.py:2758     ← the three write sites, all pass find_existing
tor_retry.py:170                                 ← the definition
$ grep -rn "retry_write\|getattr(tor_retry" …    ← no alias, no getattr, no functools.partial
```

```python
signature: (exchange, call, *, label, idem_key, find_existing)
find_existing kind: KEYWORD_ONLY | default: NONE (required)
omitting it raises: TypeError - missing 1 required keyword-only argument: 'find_existing'
```

**No indirect path exists, and if one were added it would fail loudly at the call, not silently at the
venue.** 3/3 confirmed, and the 4th case — a future path — is prevented by the interpreter.

---

# 4. THE PAPER/LIVE DIVERGENCE LIST — WHAT REMAINS

Closed today: the native trail (M4), the trail label (G2c), the close-card Gross (P1). **What remains
is what the first live trade will do that no paper trade ever has.**

## 🔴 The fork itself

**`main.py:2173` — `if OBSERVATION_MODE: … return`.** Every line of `_execute_single_entry` below that
point **has never executed.** That is the single largest divergence and it contains the entry order,
the stop placement, the fill read and the fee resolution.

## The behavioural divergences that remain

| # | where | paper | live |
|---|---|---|---|
| 1 | **size** (`config.py:38-50`) | margin **2000** × 5 = **$10,000** notional | margin **20** × 5 = **$100** notional |
| 2 | **entry** (`main.py:2173`) | `virtual_trader.execute_entry` — no order | real `create_market_order` + M5 probe + M1 stop |
| 3 | **the stop** | a number the poller evaluates | a real position-level `/v5/position/trading-stop` |
| 4 | **stop moves** (`vt:1960`) | row update only | `_live_move_stop` → venue; failure leaves stop **stale but WIDER**, alerts |
| 5 | **close** (`vt:1941`) | books at the decision price | real reduce-only order, books at the **REAL fill** |
| 6 | **passive exit** (`vt:1473`) | unreachable — no passive fill can exist | `_live_pos_state` + `_book_exchange_close`, venue-derived reasons |
| 7 | **partial size** (`vt:1626`) | intended fraction | **filled read back from the venue** (F3) |
| 8 | **F1's six venue reasons** | cannot occur | `tp`/`liquidation`/`adl`/`settlement`/`exchange_market`/`exchange_unreported` become reachable |
| 9 | **daily-loss balance check** (`main.py:1441`) | **`if OBSERVATION_MODE: return False, None` — SKIPPED** | **ACTIVE**, and makes a `fetch_balance` call |
| 10 | **risk-gate book** (`main.py:1402, 1605`) | reads `is_paper=1` | reads `is_paper=0` |

## 🔴 The consequence of #10 that the operator must know

```
virtual_positions by is_paper:   is_paper=1 → 21 rows      is_paper=0 → 0 rows
```

**The live book is EMPTY.** At the flip, `_brake_book` and `_streak_book` switch to `is_paper=0`, so:

> **The daily-loss brake and the loss-streak gate both start from ZERO history on trade one.**
> No paper loss carries over. This is correct by design — live risk must not be gated on paper P&L —
> but it means **neither brake can fire until live losses accumulate**, and the first live trades run
> with those two protections effectively at their most permissive.

And **#9 is a code path that has never executed once**: the balance-based daily-loss check is skipped
entirely in paper, so its first run will be on live money, including its first-ever `fetch_balance`.

---

# 5. THE FLIP SEQUENCE

## The line that changes

```
/mnt/volume_nyc1_1780480650620/mercury-sol/.env
    MERCURY_OBSERVATION_MODE=1     →     MERCURY_OBSERVATION_MODE=0
```

**That is the only line.** `BYBIT_API_KEY` / `BYBIT_API_SECRET` are already wired
(`main.py:76`, `tor_retry.py:44`) and are read from the environment — the new key goes in the same two
variables. There is **no testnet/sandbox flag**: this exchange object is mainnet-only.

## 🔴 A restart IS required

`config.py` reads `MERCURY_OBSERVATION_MODE` **once, at import**. There is **no reload path anywhere in
the tree** (zero `importlib` uses). Editing `.env` without restarting changes nothing — **this is
precisely the 25-minute defect of 14:30, and it would be far more expensive here**: the disk would say
LIVE while the worker kept paper-trading, and the operator would believe money was at risk when it was
not, or worse, the reverse on a later restart.

```
systemctl restart mercury-sol
```

## What the boot line must read afterwards

```
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h
                    OBSERVATION_MODE=False [pid <NEW WORKER PID>]
```

**`OBSERVATION_MODE=False` and a pid matching the new fork.** If it still says `True`, the flip did not
take and nothing else in this list matters. **Check this before anything else.**

## What to check on the first live trade

**The three already known:**

| # | check | expected |
|---|---|---|
| 1 | margin on the entry card | **$20** (not $2000) |
| 2 | `virtual_positions.is_paper` | **0** |
| 3 | the partial | **0.4** SOL of a **1.3** SOL entry (0.4333 quantised DOWN at the 0.1 step) |

**And these, which would each show a distinct defect on trade one:**

| # | check | why it matters |
|---|---|---|
| 4 | **the stop exists on the venue BEFORE the fill is read** | M1's whole purpose. Journal: `_place_sl_with_retry` must precede `_read_entry_fill`. A funded position with no stop is the one unrecoverable state. |
| 5 | `[SMART-CLEANUP]` line at boot | says which POS_FLAT branch ran (§2c) |
| 6 | `entry 1.3 SOL` accepted by Bybit | `quantise_amount` refuses below min qty/notional — if $100 is under Bybit's SOL minimum the entry will REFUSE, loudly, rather than send a bad order |
| 7 | the entry order's `orderLinkId` == `sol-e-{row_id}` | proves the M5 key reaches the venue on a real order, not just in ccxt source |
| 8 | no `[SOCKS_RETRY] … ADOPTED` unless a 403 occurred | an adoption on a clean path would mean the probe is matching something it should not |
| 9 | `close_reason` on the first exit is a literal (`sl`/`trail`/…), and `trades.signal_type` agrees | G2c + F1 on a real exit |
| 10 | the close card's **Gross − Fees == Net** | P1 on a real partial-bearing close |
| 11 | breakeven lock moves the venue stop at +1R | `_move_stop_to` on real money; a failure leaves it **wider**, and alerts |
| 12 | first `fetch_balance` succeeds | §4 #9 — never executed before |

---

# 6. VERDICT

## Is SOL ready? **Yes — with the distinction stated plainly.**

Everything reported closed today is **loaded in the running worker**, verified two independent ways.
The four open items are all correctly rated: **F2 is structurally dead, M4's worst case is a few
dollars at $100 notional, the POS_FLAT assumption has two independent structural guards, and the
adaptive-trail shadow is mode-independent.** No change made today assumes a state another removed, and
the one required-parameter contract is enforced by the interpreter.

## 🔴 What I would NOT be surprised to see go wrong on the first live trade

**Not hedging — this is a specific list. Nine mechanisms have been proven by mocks, isolated trees and
fake venues. None has executed once against Bybit.**

1. **`find_order_by_client_id` against a real Bybit response.** My fake venue returned exactly the
   shape I wrote. Real risks: `fetch_closed_orders(symbol, limit=50)` may not accept `limit` as I pass
   it, `clientOrderId` may be absent or empty on closed orders, or a filled market order may not appear
   in `fetch_closed_orders` at all. **If the probe throws, M5 does the safe thing — `WriteUnconfirmed`,
   refuse, alert — so the failure mode is a refused entry, not a double order.** That is the right way
   to fail, but expect it to be the first thing that fires.
2. **The M5 probe's cost on Tor.** Two extra calls per retry attempt, on a link that produced 285 SOCKS
   retries and 26 CloudFront 403s in two days. A probe that is itself 403-blocked returns
   `WriteUnconfirmed` — correct, but it means a Tor-flaky moment now refuses entries that previously
   retried through.
3. **`quantise_amount` at 1.3 SOL / $100 notional against Bybit's real minimums.** If SOL's min
   notional exceeds $100, **every entry will refuse**. That is a loud, safe failure — but it would mean
   zero live trades until the margin rises.
4. **The 0.4 SOL partial's `reduceOnly`.** Proven correct in ccxt source (`reduceOnly` camelCase, the
   2026-08-01 fix), never sent.
5. **`/v5/position/trading-stop` (B1) on a real position** — entry stop, breakeven move and recheck
   tighten all route through `_move_stop_to`, which has never set a real stop.
6. **`_classify_exchange_exit` on a real Bybit exit.** F1 mapped six venue reasons from the API docs
   and my reading of ccxt; the actual `stopOrderType`/`execType` strings Bybit returns have never been
   seen. **The `unmapped_close_{side}` fallback exists exactly for this** — expect it to fire at least
   once, loudly, and that is the mechanism working, not failing.
7. **The daily-loss `fetch_balance` path** (§4 #9) — skipped in paper, first execution on live money.
8. **`_smart_boot_cleanup`'s first real `fetch_positions`** (§2c).
9. **The risk gates starting from an empty live book** (§4 #10) — not a defect, but the first live
   trades run with the loss-streak and daily-loss brakes at their most permissive, and that is worth
   knowing on trade one rather than trade five.

**The common shape of 1, 3, 5, 6 is the same one this project has hit all week: a mechanism verified
against a model of the venue rather than the venue.** Today's work made every one of them *fail safely*
— refuse, alert, leave the row open, never double, never fabricate. **That is the property to trust on
trade one, not the assumption that they will all work first time.**

**Recommendation: flip, and watch the first trade end to end against the twelve checks in §5.**

---

```
READ-ONLY AUDIT — nothing changed, no service restarted, no file written to the SOL tree.
SOL   worker 2742565 · flat 0/0/0 · tracebacks 0 · OBSERVATION_MODE=True (still paper)
TITAN git clean · HEAD 897850b · NOT TOUCHED
```

*Generated 2026-08-06 16:25 UTC.*
