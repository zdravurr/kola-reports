# SOL MONEY-PATH AUDIT — THE TITAN CHECKLIST, RUN BACKWARDS

**2026-08-06 13:00 UTC · Mercury-SOL (PAPER) · READ-ONLY. Nothing changed.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`. No file modified; the only SOL files with
today's mtime are `claude_advisor.py` / `main.py` from the 12:45 dedup change, which predates this
audit. Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched, not read for state, not run** —
`git status` clean at `897850b`, workers 2538048/2538082 undisturbed.

**Why now:** the Bybit key expires **2026-08-13**, and SOL's live order path has never executed
against a real exchange.

---

## THE ANSWER FIRST

**SOL passes three of the four Titan F-class defects outright — and one of those (F3) it fixed on
2026-08-01, before Titan found it.** The exchange genuinely runs both ways.

**But seven money-misplacing defects remain, and five of them fire on the first live trade.**

The most severe is not on Titan's list. It is SOL's own recorded "OPEN, NOT BLOCKING" item, and the
rating is wrong: the justification says *"at $100 notional the alert naming the state is
sufficient."* **The venue is on CROSS margin (`tradeMode 0`, on record in OPEN-ITEMS §P3). The
exposure is not $100 — it is the account balance.**

---

## 1. THE FOUR TITAN F-CLASS DEFECTS, CHECKED HERE BY CODE

### ✅ F1 — "flat" vs "read failed": **CLOSED ON SOL. Genuinely.**

`_fetch_position_state` (main.py:1638) returns `POS_OPEN / POS_FLAT / POS_UNKNOWN`, and the ambiguous
helper was **deleted rather than kept**, so a future caller cannot reach for the shorter name. All
six consumers enumerated, with what each does on each outcome:

| # | caller | OPEN | FLAT | **UNKNOWN** |
|---|---|---|---|---|
| 1 | `_execute_close_position` (2175) | close | `return None` | **raises before unregister/cancel** |
| 2 | `_exec_partial_live` (2262) | reduce | no-op | **raises** |
| 3 | EQH/EQL Smart TP (2450) | close | log only | **`status='position_unknown'` + TG, no action** |
| 4 | 5m Group B (3593) | consult | cancel orphan stops | **one unknown side short-circuits ALL of it** |
| 5 | exit-arm lookup (3732) | arm | no arm | **no arm, and now says so** |
| 6 | `_monitor_positions` (4259) | manage | book close | **nothing, retry next tick** — and this loop is **RETIRED to a no-op** (4450) |

`_smart_boot_cleanup` (1704) — the analogue of Titan's every-boot `_reconcile_side` — is correct and
was correct first: `except → "DOING NOTHING to be safe"`. It is the pattern the rest was generalised
from.

🔶 **Residual, not a defect today:** `POS_FLAT` is also returned when `fetch_positions` *succeeds*
but returns an empty/stale list. Consumer 4 cancels stops on that. This is a venue-truthfulness
assumption, and Bybit has never been exercised live.

### 🔴 F2 — idempotency key: **PRESENT. The exchange CHECK is ABSENT.**

Better than Titan's pre-fix state, and the load-bearing half is still missing.

**What is right.** All three order writes route through `with_socks_retry_write` with a stable key:
entry `sol-e-{row_id}`, close `sol-c-{side}-{epoch}`, partial `sol-p-{vpos_id}`. Reads keep the blind
retry. **And the key genuinely reaches the venue** — verified in the installed ccxt 4.5.52:
`create_order_request` reads `clientOrderId` from params and sets `request['orderLinkId']`
(bybit.py:4049-4054); retCode `110072` "OrderLinkedID is duplicate" is mapped (bybit.py:751). This is
*not* the `reduce_only`-vs-`reduceOnly` class — this one is wired.

**Also structurally right:** SOL's stop is a **position-level `/v5/position/trading-stop`**, a SET,
not an appended order. Titan's F2 — two `closePosition` stops from one call — **cannot happen here by
construction.** `_place_sl_with_retry` retries an idempotent set.

🔴 **What is missing.** `with_socks_retry_write` (tor_retry.py:108) never queries the exchange before
retrying. There is no `fetch_open_orders` / `fetch_order` check. The entire protection rests on Bybit
returning 110072 — exactly the venue-uniqueness assumption the operator flagged, unproven on Bybit as
it was on BingX. If Bybit accepts the duplicate key instead of rejecting it, a 403-after-success
places a **second market order**: double-size entry.

### ✅ F3 — the book shrinks by what was SOLD. **ABSENT. SOL got here first.**

`_apply_partial_at_arm` (virtual_trader.py:840): the live adapter's **filled** size overrides the
intended fraction (`qty = float(_filled_override)`), `rem = size - qty`, and the fee split uses
`_frac = qty / size` — the *realised* fraction. The code says so in a 🔴 comment dated 2026-08-01.

**Checked on the real book first, as instructed — vpos 25:**

| | |
|---|---|
| remainder `size` | 91.93333 |
| `partial_size` | 45.96667 |
| **sum** | **137.9 — exactly the original size** |
| `net_pnl` | 126.523, which **includes** `partial_pnl` +31.749 |

The book shrank by exactly what was booked. **Titan's vpos-82 defect has no counterpart here.**

### 🔴 F4 — truthiness fill reads: **ABSENT on the entry, PRESENT on the partial.**

`_read_entry_fill` (main.py:1853) is exemplary — *"NEVER guesses a size"*, returns `(None, None)`
when it cannot substantiate, and the caller refuses to book.

But `_exec_partial_live` (main.py:2296):

```python
except Exception as e:
    print("... fill read FAILED ... falling back to requested {want}; "
          "accounting may differ from reality")
    filled = want            # ← the REQUESTED size
```

**The entry refuses to guess; the partial guesses.** On a fill-read exception the book is written
down by what was *asked*, which is Titan's F3 shape arriving through the back door. It is logged
loudly, which is why it ranks below the others — but the log is not the book.

*(The `float(x or 0) or None` pattern here is safe in the 0.0 case: a genuine zero fill becomes
`None` → "nothing reduced", which is correct.)*

### 🔴 F7 — cancel-before-close: **PRESENT, and live-reachable.**

`_execute_close_position` (main.py:2154), live branch — paper returns at the top, so the guard is
mode-only, exactly as on Titan:

```
2191  _cancel_open_orders_for_side(...)   ← the protective stop goes
2193  fetch_ticker(...)                   ← a Tor round-trip, retried on 403
2206  create_market_order(...)            ← the close
```

**Between 2191 and 2206 the position is naked**, across a network read that is measurably slow
(285 SOCKS retries / 26 CloudFront 403s in two days, per OPEN-ITEMS). If the close then fails, the
position is left open **with its stop cancelled**.

The ticker fetch at 2193 is used only for `current_price`, a *fallback* for the fill price — it is
not needed to send a market close.

---

## 2. SOL's OWN "OPEN, NOT BLOCKING" ITEM — RE-RATED

**Traced to the finish. The entry order is SENT (main.py:1958). Then:**

1. `_read_entry_fill` cannot substantiate → `(None, None)`.
2. Telegram fires, and it is honest — it says recovery is MANUAL and lists three steps.
3. `raise RuntimeError` → caller records `status='failed'`.
4. 🔴 **The stop is never placed.** `_place_sl_with_retry` is at line 2058; the raise is at ~2005.
5. No `virtual_positions` row → the engine, "the single position manager in BOTH modes", has nothing.
6. No `active_positions` row → `_reconcile_active_positions` returns early on an empty table.
7. No boot reconciler reads the exchange — both read the DB.

**End state: a funded, UNSTOPPED, UNMANAGED live position that no restart will ever adopt.**

### Why the "NOT BLOCKING" rating is wrong

**a) The exposure is not $100.** `LIVE_FIXED_MARGIN 20 × LEVERAGE 5 = $100` notional, but the venue
reads **`tradeMode 0` — CROSS** (OPEN-ITEMS §P3, read back from Bybit by hand). Under cross margin an
unstopped position is not bounded by its $20 margin; it draws on the whole wallet balance. The
recorded justification — *"at $100 notional the alert naming the state is sufficient"* — is reasoning
about an isolated-margin position that does not exist.

**b) The trigger is not exotic.** `_read_entry_fill` reaches `(None, None)` when `fetch_order` raises.
`tor_retry` retries **403s only** — its docstring states *"Timeouts / connection errors are NOT
retried."* So a single Tor **timeout** on one `fetch_order`, against a venue reached over Tor with a
measured 403 rate, lands here directly. This is a routine network condition, not a tail event.

**c) It is unbounded in time.** Nothing adopts it on any restart, so the position sits until a human
reads Telegram and acts. The alert is the entire control.

**Re-rated: 🔴 BLOCKING. It is the single highest-cost path in this audit and it can fire on trade
one.**

---

## 3. GEOMETRY

### 🔴 G1 — the trail's giveback drifts with MFE. Confirmed, with the predicted sign.

`trail_pct` is computed off the **entry** (`trail_cb / fill_price * 100`, virtual_trader.py:224) and
applied to the **water mark** (`water_mark * (1 ± trail_pct/100)`, :1546-1549). The structural drift
is therefore exactly `water_mark / entry`.

Measured on every trailed exit in the book:

| vpos | side | `wm/entry` | giveback at trigger | nominal (entry-based) | drift |
|---|---|---|---|---|---|
| 21 | **LONG** | **1.01709** | 0.9151 | 0.8997 | **+1.7% WIDER** |
| 13 | SHORT | 0.94230 | 1.5831 | 1.6801 | **−5.8% tighter** |
| 15 | SHORT | 0.97072 | 1.8928 | 1.9499 | −2.9% tighter |
| 25 | SHORT | 0.97475 | 0.7113 | 0.7298 | −2.5% tighter |

**Wider on longs, tighter on shorts — Titan's G1 exactly.** The drift is largest on the *biggest
winner* (vpos 13, +$327, MFE 5.8%): the mechanism cuts the runner's room precisely when it has run.
Poll granularity adds 0.009–0.057 in price on top, always in the giveback direction.

### 🔴 G1b — `TRAIL_MULT_ATR == SL_BUFFER_ATR` — the ~1.00R giveback. **STILL LIVE ON SOL.**

`SL_BUFFER_ATR = 2.5` (config.py:61) and `TRAIL_MULT_ATR = 2.5` (config.py:62). The SL distance and
the trail callback are the *same number times the same ATR*, so the trail gives back **exactly 1R by
construction**. Titan fixed its equivalent on 2026-08-04. SOL still carries it.

Confirmed on SOL's own book — `sl_dist` vs `2.5 × atr` vs the trail's nominal:

| vpos | `atr` | `2.5×atr` | `sl_dist` | realised giveback |
|---|---|---|---|---|
| 21 | 0.3619 | 0.9046 | 0.90 | **1.0667 R** |
| 13 | 0.6736 | 1.6841 | 1.68 | **0.9762 R** |
| 15 | 0.7789 | 1.9472 | 1.95 | **0.9949 R** |
| 25 | 0.2920 | 0.7301 | 0.73 | **0.9866 R** *(of the post-partial size)* |

`initial_risk_usdt` equals `sl_dist × full size` to the cent in all four, so these are true R.

**The money:**

| vpos | given back | booked net | had it exited at MFE |
|---|---|---|---|
| 13 | $238.95 | $327.21 | $566.16 |
| 15 | $246.77 | $34.83 | $281.59 |
| 21 | $126.14 | $33.66 | $159.80 |
| 25 | $66.19 | $126.52 | $192.71 |
| **total** | **$678.05** | **$522.22** | — |

**The trail gave back $678.05 — 1.30× everything it booked.** Against a whole-book net of
**−$1,107.84** (sl −$2,185.12 ×11, trail +$522.22 ×4, exit_signal +$555.06 ×6), the trail's giveback
alone is **61% of the entire book's loss.**

### ✅ G3 — boot re-attach ATR timeframe: **ABSENT.**

There is one constant, `ATR_TF = '1h'`, used by `adaptive_trail.py`, `stop_loss.py` and the entry
path alike; no hardcoded `'5m'` anywhere in the geometry. And the boot path
(`_reconcile_open_virtual_positions`, main.py:4459) **recomputes no geometry at all** — it reads
`virtual_positions` and logs. Titan's G3 has no counterpart.

🔶 The flip side: nothing re-asserts the stop **on the venue** at boot, nor verifies the venue stop
matches the DB. A Bybit position-level stop persists venue-side, so this is a gap in verification,
not in protection.

### 🔴 G2 — the partial's PnL reaches the report, but the report no longer adds up. **ALREADY FIRED.**

`close_position` folds the partial back in — but only into **two of the card's three lines**:

```python
gross_pnl  = (close_price - entry_price) * size * direction_mult   # ← REMAINDER only
total_fees = entry_fee + close_fee
net_pnl    = gross_pnl - entry_fee - close_fee
net_pnl    += partial_pnl        # ← whole position
total_fees += partial_fees       # ← whole position
```

`gross_pnl` is never reconstituted. The card prints Gross, Fees and Net — and on vpos 25 it printed:

| card line | value |
|---|---|
| 💵 Gross P&L | **+$102.046** (remainder only) |
| 💸 Total Fees | −$10.9174 (whole position) |
| 💰 Net P&L | **+$126.523** (whole position) |

**Gross − Fees = $91.13. Net says $126.52. The card contradicts itself by $35.39** — the partial's
gross. This went to Telegram on 2026-08-01 and is the one operator-facing number in this audit that
has *already* been wrong.

### 📏 G2b — the close ROW mixes bases

The `trades` close row writes `amount = size` (the **remainder**, 91.933) alongside
`pnl = net_pnl` (the **whole** position, 126.52) — vpos 25 is row 15004. Any reader deriving
per-unit economics, R, or slippage from `pnl/amount` on that row is wrong by the partial.

### 📏 G2c — paper and live now disagree on what a trail exit is called

`_CLOSE_LABEL` maps `'trail' → 'sl_triggered_{s}'` in `trades` (virtual_trader.py:396). The
justification comment says *"live records trail-fired closes as sl_triggered too — the monitor can't
distinguish."* **That justification went stale on 2026-08-05**, when `_BYBIT_STOPTYPE_TO_REASON` made
the live path book `TrailingStop → 'trail'` properly.

So after the flip: **live books `trail`, paper books `sl_triggered`.** The paper-vs-live comparison
SOL is being run in paper to establish is the exact thing this breaks. `virtual_positions.close_reason`
keeps the truth (this audit used it), so the damage is confined to `trades`.

---

## 4. TWO FINDINGS THE CHECKLIST DID NOT ASK FOR

### 🔴 N1 — a naked live position can be filed as `observed_skipped`

`_execute_single_entry`, SL-failure branch (main.py:2061):

```python
if sl_id is None:
    send_tg("🚨 SL FAILED 3× — emergency close ...")
    try:    _execute_close_position(symbol, position_side)
    except Exception as ec:
        print(...)          # ← print only. NO Telegram.
    return None             # ← same return as "no order was placed"
```

The caller (main.py:3433) turns `None` into **`status='observed_skipped'`** — the status that
everywhere else in this codebase means *the advisor said execute but nothing was sent*. So the worst
live outcome available — a funded position with **no stop** whose emergency close **also failed** —
is recorded as a routine non-event, and the only signal that the recovery failed is a line in the
journal. Note the emergency close routes through `_execute_close_position`, which **raises** on
`POS_UNKNOWN`; a Tor blip at that moment is enough to reach this branch.

### 🔴 N2 — the loss-streak gate is the daily-loss brake's unfixed twin

The daily-loss brake was fixed on 2026-08-05 to read the book it protects
(`COALESCE(is_paper,1) = ?` over `virtual_positions`). **The loss-streak gate beside it was not**
(main.py:1577):

```sql
SELECT pnl FROM trades WHERE status='executed' AND pnl IS NOT NULL
 ORDER BY id DESC LIMIT 3
```

No `is_paper`, no `is_virtual`, no `exchange` filter — over `trades`, the table where **every armed
exit is stored twice** (OPEN-ITEMS records six such pairs), so one armed-exit loss can count as two
consecutive losses out of three.

What it reads **right now**, i.e. what would gate the first live entry:

| id | signal_type | pnl | is_virtual |
|---|---|---|---|
| 15473 | sl_triggered_short | −85.45 | **1 (paper)** |
| 15404 | sl_triggered_long | −138.67 | **1 (paper)** |
| 15004 | sl_triggered_short | +126.52 | **1 (paper)** |

**2 of 3 negative.** One more paper loss and the gate halts *live* trading for 4 hours on a streak
that is entirely paper. Direction is mostly safe (spurious halt), but it is a live risk gate reading
a book that is not the one it protects.

---

## 5. VERDICT — RANKED BY RUNS × COST

### 🔴 MISPLACES MONEY

| # | finding | runs | cost if it fires | first live trade? |
|---|---|---|---|---|
| **M1** | Unreadable entry fill → funded, unstopped, unmanaged position nothing ever adopts. **CROSS margin ⇒ bound is account equity, not $100.** Trigger is one un-retried Tor timeout | every entry | **unbounded** | 🔴 **YES** |
| **M2** | SL fails 3× **and** emergency close fails → naked position filed `observed_skipped`, no Telegram on the failure (N1) | every entry | unbounded, and **invisible** | 🔴 possible |
| **M3** | **F7** — live close cancels the stop, then does a Tor ticker read, then closes. Close fails ⇒ open and unprotected | every programmatic close | position-sized | 🔴 **YES** |
| **M4** | Two trailing mechanisms in live: Bybit's native trailing stop set at entry **and** the engine's software trail, both armed, never co-executed. Contradicts "single position manager in BOTH modes" | every position past +1R | exit at the wrong level; ambiguous attribution | 🔴 **YES** |
| **M5** | **F2** — idempotency key present and wired, but **no exchange check** before retry. Rests entirely on Bybit returning 110072 | every 403-on-write | **double-size entry** | only on a 403 |
| **M6** | **F4** — live partial falls back to the **requested** size when the fill read raises, while the entry refuses to guess | every partial | book ≠ venue | on the first live partial |
| **M7** | Loss-streak gate: no `is_paper` filter, reads the double-counted `trades` (N2) | every entry | spurious 4h halt on paper losses | 🔴 **YES** |

### 📏 CORRUPTS MEASUREMENT

| # | finding | status |
|---|---|---|
| **P1** | **G2** — close card's Gross excludes the partial while Fees and Net include it. vpos 25: $102.05 − $10.92 ≠ $126.52, **off by $35.39** | 🔴 **already fired, already sent to Telegram** |
| **P2** | **G1b** — trail == SL by construction (2.5 = 2.5) ⇒ **~1.00R giveback**, 4/4 trailed exits. **$678.05 given back vs $522.22 booked; 61% of the book's entire net loss** | 🔴 **already in the book** |
| **P3** | **G1** — giveback drifts with MFE: wider on longs (+1.7%), tighter on shorts (−2.5% to −5.8%), worst on the biggest winner | already in the book |
| **P4** | close row's `amount` is the remainder while its `pnl` is whole-position (row 15004) | already in the book |
| **P5** | paper books a trail exit as `sl_triggered`, live (since 08-05) books `trail` — the paper/live comparison diverges at the flip | fires at the flip |

### ✅ CLEAN — and worth saying, because the exchange runs both ways

- **F1** three-state read: closed, all six consumers correct, the ambiguous helper deleted.
- **F3** partial book-down: absent, and **SOL fixed this before Titan found it** — verified on vpos 25.
- **F4 on the entry path**: `_read_entry_fill` refuses to guess a size.
- **G3**: one `ATR_TF`, no boot geometry recompute.
- **Titan's F2 double-stop cannot occur**: SOL's stop is an idempotent position-level SET, not an order.

---

## 🔴 WHAT FIRES ON THE FIRST LIVE TRADE — THE LIST THAT DECIDES THE FLIP

1. **M1** — one un-retried Tor timeout on a single `fetch_order` leaves a funded, unstopped position
   under CROSS margin that nothing will ever adopt. **This alone blocks the flip.**
2. **M3** — the first programmatic close cancels the stop before sending the close.
3. **M4** — the first position past +1R is managed by two trailing mechanisms at once.
4. **M7** — the first entry is gated by a loss streak computed from paper rows (currently 2 of 3
   negative — one paper loss from halting live trading).
5. **P1 / P2 / P4** — the first trailed exit gives back ~1R by construction and reports a card whose
   Gross, Fees and Net do not reconcile.

**M2 and M5 need a second condition (SL failure; a 403 on a write) but are unbounded when they fire.**

The recorded rating of the boot-adoption gap — *"OPEN, NOT BLOCKING … at $100 notional the alert
naming the state is sufficient"* — should be read as **BLOCKING**: it was rated against an
isolated-margin position, and the venue is on CROSS.

**No fixes proposed. This is the map.**

---

## APPENDIX — unrelated open thread from the 12:45 change

The state-dedup applied at 12:20:55 has still produced **no live reuse**: 0 advisor consultations in
the 22 minutes since boot (the gates have been quiet), so the column is still empty and the log has
no `STATE-CACHE` line. Watchers remain armed. **Not yet proven live, and still not claimed.**
