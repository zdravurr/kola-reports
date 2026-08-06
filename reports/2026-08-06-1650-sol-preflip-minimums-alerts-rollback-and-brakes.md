# SOL — FOUR THINGS BEFORE THE FLIP: BYBIT'S REAL MINIMUMS, THE HANDS-REQUIRED ALERTS, THE ROLLBACK STACK, AND THE BRAKES AT $100

**2026-08-06 16:50 UTC · Mercury-SOL · READ-ONLY. NOTHING WAS CHANGED. NO ORDER PLACED.**

Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched.**

---

## THE HEADLINES

> **1. $100 IS VIABLE. The 16:25 §6 item 3 worry is dead — Bybit's `minNotionalValue` is $5, not $100.**
> Entry **1.3 SOL ($95.19)** and partial **0.4 SOL ($29.29)** are both VALID orders. **No budget change
> is needed.** The floor for full behaviour is **$30 notional**.
>
> **2. The real first-trade exposure is 3 consecutive losses ≈ $3.93** before any brake fires.
>
> **3. 🔴 A correction to my own 16:25 report: I wrote that the daily-loss brake is "skipped entirely
> in paper". That was wrong — only CLAUSE 2 is. Clause 1 is R-based and runs in BOTH modes**, which
> makes the brake far less dormant than I implied. Detail in §4.
>
> **4. There are 18 backups from today, not "about ten", and `mtime` is the wrong key to order them by.**

---

# 1. 🔴 BYBIT'S ACTUAL MINIMUMS — READ FROM THE VENUE

## a) Read live, `load_markets(True)` forced reload, public endpoints only, over the bot's own Tor proxy

```
SOL/USDT:USDT — from Bybit, 2026-08-06 16:4x UTC
  minOrderQty       : 0.1
  qtyStep           : 0.1
  maxOrderQty       : 96000.0
  minNotionalValue  : 5          ← 🔴 FIVE DOLLARS, not one hundred
  tickSize          : 0.010
  ccxt precision    : {'amount': 0.1, 'price': 0.01}
  mark price        : 73.226   (last 73.22)
```

## b) What `quantise_amount` actually produces — run against those numbers, not reasoned about

```
budget: LIVE_FIXED_MARGIN 20 × LEVERAGE 5 = $100 notional, mark $73.22

ENTRY    100 / 73.22 = 1.3657 SOL  ─quantise DOWN(0.1)→  1.3 SOL   ($95.19)
         minQty 0.1 ✅   minNotional $5 ✅   on step ✅   →  **VALID**
         [QTY] entry SOL/USDT:USDT: 1.365747 -> 1.3 (step quantisation -4.814%)

PARTIAL  1.3 × 1/3 = 0.4333 SOL   ─quantise DOWN(0.1)→  0.4 SOL   ($29.29)
         minQty 0.1 ✅   minNotional $5 ✅   on step ✅   →  **VALID**
```

**Both are valid orders at the venue.** The three numbers the operator already expected — $20 margin,
1.3 SOL entry, 0.4 SOL partial — are confirmed against Bybit's own filters, not against config comments.

## c) The floor, measured by sweep

| notional | entry | partial | verdict |
|---|---|---|---|
| $5 | — | — | 🔴 **ENTRY RAISES** `InvalidOrder` (raw 0.068 < 0.1 precision) |
| $8 | 0.1 ($7.32) | — | entry OK, **partial skipped** |
| $15 | 0.2 ($14.64) | — | entry OK, **partial skipped** |
| $20 | 0.2 ($14.64) | — | entry OK, **partial skipped** |
| $25 | 0.3 ($21.97) | — | entry OK, **partial skipped** |
| **$30** | **0.4 ($29.29)** | **0.1 ($7.32)** | ✅ **BOTH VALID — the floor for full behaviour** |
| $50 | 0.6 ($43.93) | 0.1 ($7.32) | ✅ both valid |
| **$100** | **1.3 ($95.19)** | **0.4 ($29.29)** | ✅ **both valid — the configured budget** |

**MINIMUM VIABLE NOTIONAL = $30.** Below that the entry still works down to ~$8 but the ⅓ partial
quantises below `minOrderQty` and is skipped — the position then rides the full trail, which is a
degradation, not a failure (the code says so: *"leg not tradable at this venue — SKIPPED; position
rides the FULL trail, contract unchanged"*).

🔶 **One rough edge found while sweeping, worth recording:** below 0.1 SOL raw, `quantise_amount` does
**not** return `(None, err)` — `ccxt.amount_to_precision` **raises `InvalidOrder`** and the helper does
not catch it. Unreachable at $100 (raw 1.3657) and contained on the partial path (which is wrapped in
`try/except … "non-fatal, position untouched"`), so **not a flip blocker** — but if the budget is ever
cut below ~$30, the partial path would book an exception rather than a clean skip.

## d) Read-only

`load_markets` and `fetch_ticker` only, on a keyless public client. **No order was placed, no private
endpoint touched, the running bot was not disturbed.**

---

# 2. 🔴 THE ALERTS THAT REQUIRE HANDS — ALL OF THEM, IN ONE PLACE

**The blocking mechanism, stated once:** `ux_vpos_one_open_per_side` is a PARTIAL unique index on
`(symbol, position_side) WHERE status='open'`. **Any alert that leaves a row open, or leaves a venue
position the boot assert can see, blocks that side until a human clears it.** `MAX_POSITIONS_PER_SIDE=1`
does the same for a registered position. Alerts are also persisted to `naked_position_alerts` — *"A
Telegram message is not state"* — so they survive the restart the alert itself asks for.

## 🔴 GROUP A — BLOCKS THE SIDE. The bot waits for a human.

### A1 · `NAKED POSITION — EMERGENCY CLOSE FAILED` — **the worst state this bot can reach**
```
🔴🔴🔴 NAKED POSITION — EMERGENCY CLOSE FAILED
{symbol} {position_side}
The stop could NOT be set (3 attempts) and the emergency close …
```
**DO:** open Bybit immediately; the position is live with **no stop**. Close it by hand or set a stop by
hand. **Recovers alone: NO.** Persisted as `stage='sl_failsafe_close_failed'`. **BLOCKS the side.**

### A2 · `ENTRY FILL UNREADABLE`
```
🚨 ENTRY FILL UNREADABLE ({symbol} {position_side})
The order was sent but its fill could NOT be read, so the position was NOT booked from a guess.
✅ It IS protected — a stop is on the exchange at {sl_price}, set before this read for exactly this case.
🔴 But the bot will NOT manage it: with no row it gets no breakeven move, no partial, no trail
recompute and no close. The next restart will SEE it and block new {position_side} entries, but it
will not adopt it. Recovery is MANUAL.
Do now: 1) open Bybit and check the {position_side} position on {symbol}; 2) confirm its stop reads
{sl_price}; 3) close it by hand, or leave it to stop out.
```
**This is M1 working.** The position is protected but unmanaged. **Recovers alone: NO.**
**BLOCKS the side** (at the next restart, via the boot assert). `stage='entry_fill_unreadable'`.

### A3 · `LIVE POSITION NOT BOOKED`
```
🚨 LIVE POSITION NOT BOOKED ({symbol} {position_side})
A real filled position could NOT be recorded because an open row for this side already exists
({error}). The position is on Bybit with its stop, but the engine will NOT manage it: no +1R partial,
no breakeven, no close accounting. Reconcile by hand.
```
**DO:** reconcile the DB row against Bybit. **Recovers alone: NO. BLOCKS the side** (the pre-existing
open row is what caused it).

### A4 · `ENTRY DUPLICATE SUPPRESSED` — M5/idempotency
```
🚨 ENTRY DUPLICATE SUPPRESSED ({symbol} {position_side})
The first order reached the venue but the fill was never seen. NO second order was placed.
Check the position and its stop manually (idem sol-e-{row_id}).
```
**The first order is PROVEN to have landed.** **DO:** check Bybit for a position and whether it has a
stop. **Recovers alone: NO** — the entry raised before the stop was placed. **BLOCKS the side** once
the boot assert sees the venue position.

### A5 · `ENTRY NOT CONFIRMED — NO SECOND ORDER` — M5, new today
```
🚨 ENTRY NOT CONFIRMED — NO SECOND ORDER ({symbol} {position_side})
The first order failed at the transport and the venue could NOT be queried, so whether it landed is
UNKNOWN. Nothing else was sent. Check the position and its stop manually (idem sol-e-{row_id}).
```
**Distinct from A4 on purpose: there the order is proven landed, here it is UNKNOWN.** Same action.
**Recovers alone: NO.** **BLOCKS the side** if a position did in fact land.

### A6 · SOL's `POSITION GONE` equivalent — the substantiation refusal
SOL has no verbatim "POSITION GONE" message (that is Titan's). Its analogue is **silent-but-blocking**:
`_book_exchange_close` *"refuses to book a close it cannot substantiate"*, so a vanished position with
no readable fill leaves the row `status='open'` **forever, blocking the side**, logging
`[ENGINE] … NOT booking. Retrying next tick.` — **with no Telegram alert.**

> 🔴 **This is the one gap in the alert surface.** Every other blocking state shouts; this one only
> logs. **If entries stop on one side and no alert has fired, this is the first thing to check** —
> `SELECT id, symbol, position_side, opened_at FROM virtual_positions WHERE status='open'`.
> *(Titan alerts loudly here; SOL does not. Recorded, not fixed — read-only pass.)*

## GROUP B — LOUD, BUT THE BOT RECOVERS ALONE

| alert | verbatim | recovers |
|---|---|---|
| **`SL FAILED 3×`** | `🚨 SL FAILED 3× — emergency close of {side} {symbol}\nThe stop could not be set at {sl}. Closing the position now.` | **YES** — closes itself. Only escalates to A1 if the close *also* fails. Does **not** block. |
| **`NAKED POSITION`** (engine, stop-verify) | `🚨 NAKED POSITION {symbol} {side}\nNo stop on the exchange and it could NOT be restored. Closing now rather than running unprotected.` | **YES** — closes the position. Does **not** block. |
| **`DAILY LOSS BREAKER (R)`** | `🚨 DAILY LOSS BREAKER (R)\n{reason}` | **YES** — clears at the next calendar day. Blocks **entries**, not a side. |
| **`DAILY LOSS BREAKER TRIGGERED`** (equity, live-only) | `🚨 DAILY LOSS BREAKER TRIGGERED\n{reason}` | **YES** — same. |
| **loss-streak cooldown** | *(no Telegram — refusal reason only)* | **YES** — expires after `LOSS_STREAK_COOLDOWN_HOURS=4`. |
| **`EXIT ARMED`** | `🚨 EXIT ARMED\n{signal}\nTTL {n} min · expires {ts}` | informational — uses 🚨 but is **not** a hands-required alert. |

## The one-glance rule when entries stop

1. `[BOOT] geometry:` line — is `OBSERVATION_MODE` what you expect?
2. `SELECT * FROM virtual_positions WHERE status='open'` — **a row here blocks its side** (covers A2–A6).
3. `SELECT * FROM naked_position_alerts WHERE resolved=0` — survives restarts (covers A1, A2).
4. Journal for `daily_loss` / `loss streak` / `fail-closed` — time-based, self-clearing.

---

# 3. 🔴 THE ROLLBACK STACK — SOL IS NOT UNDER VERSION CONTROL

## a) Every backup from today, **in creation order** — 18, not ten

🔴 **Order them by `ctime` (when the backup was made), never by `mtime`.** The backups were made with
`cp -p`, so `mtime` is the *content's* date — `config.py.bak_P2_trail_decouple_20260806` carries an
**Aug 5** mtime. Sorting by mtime scrambles the stack.

| # | made (ctime) | file | precedes |
|---|---|---|---|
| 1 | 12:08:54 | `claude_advisor.py.bak_statededup` · `main.py.bak_statededup` · `trades.db.bak_pre_statededup` | state dedup |
| 2 | 13:03:15 | `main.py.bak_nakedposition_M1M2M3` | M1/M2/M3 protect-before-describe |
| 3 | 13:34:08 | `main.py.bak_M6M7_partial_lossstreak` | M6/M7 |
| 4 | 13:48:46 | `main.py.bak_M4_native_trail_deleted` | M4 native-trail deletion |
| 5 | 14:29:38 | `config.py.bak_P2_trail_decouple` · `virtual_trader.py.bak_P1_gross` | P2 trail 2.5→1.875 *(made by the session that then dropped; its P1 was never applied)* |
| 6 | 14:59:11 | `virtual_trader.py.bak_P1_G2c` · `optimizer.py.bak_G2c_trail_label` | P1 + G2c |
| 7 | 15:16:42 | `virtual_trader.py.bak_F1_unmapped_reasons` · `optimizer.py.bak_F1_labels` · `gunicorn_mercury.conf.py.bak_bootgeometry` · `config.py.bak_bootgeometry` | F1 + the boot geometry line |
| 8 | 15:43:46 | `tor_retry.py.bak_M5_exchange_check` · `main.py.bak_M5_exchange_check` | M5 venue check |
| 9 | 15:50:04 | `OPEN-ITEMS-SOL.md.bak_M5` | the canon correction |
| 10 | 16:00:29 | `claude_advisor.py.bak_wallpctl_dualtally` | wall percentiles + dual tally |

## b) The three rollbacks

**Revert ONE change** — restore that step's backup(s) **together** (see (c)), `py_compile`, restart,
confirm the boot line. Only steps 8, 7, 6 and 10 are independently revertible; the `main.py` backups
(2,3,4,8) are a **stack**, not a set — restoring #2 discards M4, M6/M7 and M5 as well.

**Revert the WHOLE day** — restore the *earliest* backup of each file:
`main.py` ← #1 (`bak_statededup`), `claude_advisor.py` ← #1, `config.py` ← #5 (`bak_P2_trail_decouple`,
pre-P2), `virtual_trader.py` ← #5 (`bak_P1_gross`), `optimizer.py` ← #6, `tor_retry.py` ← #8,
`gunicorn_mercury.conf.py` ← #7, `OPEN-ITEMS-SOL.md` ← #9. `trades.db` ← #1 **only if the DB itself is
corrupt** — it holds 21 closed positions and reverting it discards real history.

**Revert to paper** — **do not roll code back at all.** Set `MERCURY_OBSERVATION_MODE=1` and restart.
The code is mode-aware throughout; reverting code to "get back to paper" would discard today's fixes
for no benefit.

## c) 🔴 FILES THAT MUST MOVE TOGETHER — and what breaks if they are split

| pair | if split | severity |
|---|---|---|
| **`tor_retry.py` + `main.py` (M5, #8)** | Revert `tor_retry` alone → `main.py` still passes `find_existing=` to a function without that parameter → **`TypeError` on EVERY order** → **no entries at all, and the failure is at the first live order.** | 🔴 **FATAL** |
| **`config.py` + `gunicorn_mercury.conf.py` (boot line, #7)** | Revert `config` alone → `post_fork` still calls `_cfg.boot_geometry_line()` which no longer exists → **`AttributeError` in post_fork → the WORKER FAILS TO START.** | 🔴 **FATAL** |
| **`virtual_trader.py` + `optimizer.py` (F1/G2c, #6-7)** | **Direction matters.** Reverting `optimizer` alone while `virtual_trader` still emits `trail_*`/`tp_*`/`liquidation_*` → `pair_trades` **silently DROPS every such close from learning** — the P4 defect, invisible. Reverting `virtual_trader` alone is harmless (the extra optimizer labels simply never match). | 🔴 **SILENT** one way, benign the other |
| `config.py` P2 vs boot line | `config.py.bak_bootgeometry` (#7) **already contains P2** (mtime 14:30:43). To undo P2 you need #5, which also lacks `boot_geometry_line` → **must revert `gunicorn_mercury.conf.py` with it.** | 🔴 **FATAL if split** |

## d) 🔴 A LIVE POSITION IS OPEN AND BEHAVING WRONGLY — THE FASTEST SAFE ACTION

> **Flipping `MERCURY_OBSERVATION_MODE` back to 1 does NOT close the position, does not cancel its stop,
> and does not even take effect until a restart.** It only stops *new* paper-vs-live routing. Treating
> it as an emergency stop would be the most dangerous possible misunderstanding of it.

**In order:**

**Step 1 — `systemctl stop mercury-sol`.** Removes the *manager*, not the *exposure*. **What it leaves
behind:** the position stays on Bybit **with its stop**, because the stop is a **position-level
attribute (B1)**, not a bot-held order — it survives the process dying. No breakeven moves, no partial,
no trail from this moment on. Do this first if the *bot* is the thing misbehaving.

**Step 2 — close the position by hand in the Bybit app/web.** **This is the only step that removes
exposure.** **What it leaves behind:** the `virtual_positions` row stays `status='open'`, which
**blocks new entries on that side** — which is what you want while investigating.

**Step 3 — (optional) cancel any leftover conditional orders** in the app. The position-level stop
disappears with the position; stray conditional orders would not.

**Step 4 — restart when ready.** 🔴 **And here today's F1 work pays off directly:** a manual close in
the Bybit app is now **bookable** — `_classify_exchange_exit` returns `exchange_market`, which F1 maps
to `exchange_market_{side}` and the optimizer recognises. **Before today that reason was unmapped and
the close was REFUSED in a permanent retry loop, leaving the row open forever.** The row will now
reconcile itself and unblock the side.

**If you cannot reach Bybit at all:** leave the bot **stopped**. The venue stop is still in place and is
the protection of last resort. **Never restart a bot you believe is mismanaging a live position "to see
if it fixes itself".**

---

# 4. THE RISK GATES AT $100 — RECOMPUTED

## 🔴 First, the correction to my 16:25 report

I wrote that the daily-loss brake *"is skipped entirely in paper"*. **That is wrong, and it understated
the protection.** The brake has **two clauses**:

```python
# CLAUSE 1 — R-BASED TAIL BRAKE. BOTH MODES.       DAILY_LOSS_R_LIMIT = 3.0
if daily_R <= -DAILY_LOSS_R_LIMIT: → HALT
# CLAUSE 2 — EQUITY FLOOR. LIVE ONLY.              DAILY_LOSS_PCT_LIMIT = 0.05
if OBSERVATION_MODE: return False, None
balance = fetch_balance(...)
```

**Clause 1 runs in both modes and is size-independent by construction** — the code says so:
*"survives $10,000 → $100 without re-calibration — the exact failure of the constant it replaces."*
Only **clause 2** is live-only. My §4 #9 was right that a never-executed path exists; it is narrower
than I said.

## a) Clause 2 at $811.90 — **dormant, and knowingly so**

```
5% of $811.90            = $40.60
1R at $100 notional      = 2.5 × ATR(1h) 0.4032 × 1.3 SOL = $1.31
$40.60 / $1.31           = 31.0 stop-outs in ONE calendar day
```

> **Clause 2 needs 31 full stop-outs in a single day to fire. Clause 1 fires at 3. Clause 2 can never
> fire first — it is dormant, exactly as Titan's was (~13 at $150).**

**Said plainly, as asked: as a standalone brake at this size, clause 2 cannot fire and is not a brake.**
But — unlike Titan's — **it is not the only clause**, and the code states the reason it is kept:
*"dormant at $100 notional, which is not a reason to discard it — it matters the moment size grows."*
That is a defensible position, not an oversight. **The operative brake at $100 is clause 1.**

## b) 🔴 The balance path's first live execution — **fail-closed, and narrower than I implied**

```python
except Exception as e:
    # D1 FAIL-CLOSED — a risk-query error must BLOCK the entry, never allow it through unmeasured.
    return True, f'daily-loss check_error (fail-closed): {e}'
```

**A failed `fetch_balance` on Tor HALTS trading — it blocks the entry. It does not permit, and it does
not raise out of the gate.** `fetch_balance` is wrapped in `with_socks_retry`, so 403s retry; a timeout
propagates and is caught here.

**And the window is much narrower than "every entry":**

```python
if daily_pnl >= 0 and daily_R >= 0:
    return False, None          # ← profitable or FLAT day: returns BEFORE clause 2
```

> **On day one the live book is empty, so `daily_pnl = 0` and `daily_R = 0` → the gate returns
> immediately and `fetch_balance` is NEVER CALLED.** It first executes only after a live LOSS earlier
> the same calendar day. So its first-ever run will be on a losing day — and if Tor is flaky at that
> moment, entries halt with `daily-loss check_error (fail-closed)`. **Safe, but it will look like the
> bot has stopped for no reason. That string is the thing to grep.**

## c) The loss-streak gate arms itself — confirmed, no human action

```sql
SELECT net_pnl FROM virtual_positions
 WHERE status='closed' AND net_pnl IS NOT NULL AND COALESCE(is_paper,1) = 0
 ORDER BY closed_at DESC LIMIT 3
```
```python
if streak >= LOSS_STREAK_THRESHOLD and len(rows) >= LOSS_STREAK_THRESHOLD:
```

The `len(rows) >= 3` guard means an empty live book simply yields no streak — **no error, no
misfire.** After **three live closes** the gate reads them normally; if all three are losses it imposes
a **4-hour cooldown** from the most recent loss. **It arms itself with no human action, and it too is
fail-closed** on a query error or an unparseable timestamp.

## d) 🔴 THE HONEST NUMBER

> ### **3 consecutive live losses ≈ $3.93 before ANY brake fires.**

| brake | threshold | at $100 notional |
|---|---|---|
| loss-streak cooldown | 3 consecutive losses | 3 × $1.31 = **$3.93** → 4 h pause |
| daily-loss clause 1 (R) | −3.0R in one calendar day | 3 × $1.31 = **$3.93** → halt for the day |
| daily-loss clause 2 (equity) | −5% of $811.90 = $40.60 | **31 stop-outs** — unreachable |

**Both operative brakes need exactly three losses**, so the answer is the same either way: **three.**
If those three fall in one calendar day, both fire together. If spread across days, the daily brake
resets each midnight and **the loss-streak gate is the only one still counting** — so across a losing
week the streak gate is what actually protects, and its memory is only the **last 3 closes**: one win
resets it completely.

**Worst realistic first-day exposure: 3 stop-outs = $3.93, ≈ 0.48% of the $811.90 balance.**
With `MAX_POSITIONS_PER_SIDE=1` there is no way to stack beyond that inside the same window.

---

# 5. SUMMARY FOR THE FLIP

| # | question | answer |
|---|---|---|
| 1 | Is $100 viable? | ✅ **Yes.** Entry 1.3 SOL, partial 0.4 SOL, both valid. `minNotionalValue` is **$5**. Floor for full behaviour **$30**. |
| 2 | Hands-required alerts | **6 blocking (A1–A6)**, 6 self-recovering. 🔴 **A6 blocks WITHOUT alerting** — check `status='open'` first when entries stop. |
| 3 | Rollback | **18 backups, order by `ctime` not `mtime`.** Three fatal split-pairs: M5(`tor_retry`+`main`), boot-line(`config`+`gunicorn`), and F1(`optimizer` must never revert alone). **`OBSERVATION_MODE=1` is NOT an emergency stop.** |
| 4 | Brakes | Both fire at **3 losses ≈ $3.93**. Clause 2 needs 31 stop-outs — dormant. `fetch_balance` is **fail-closed** and is not called at all on a flat/profitable day. |

```
READ-ONLY — no file written to the SOL tree, no service restarted, no order placed.
SOL   worker 2742565 · flat 0/0/0 · OBSERVATION_MODE=True (still paper)
TITAN git clean · HEAD 897850b · NOT TOUCHED
```

*Generated 2026-08-06 16:50 UTC.*
