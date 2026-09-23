# mercury-sol-size-is-now-a-one-line-change

_2026-09-23 15:50 UTC_

---

# SIZE IS NOW A ONE-LINE CHANGE — **APPLIED FROM FLAT, LOADED. SIZE UNCHANGED: $100 BOTH SIDES**

**2026-09-23 15:50 UTC · Mercury-SOL · APPLIED · Titan untouched · COHORT BOUNDARY 2026-09-23 15:42:32 UTC**

`openitems_guard` → **exit 0** before and **exit 0** after (titan-bot HEAD `f53d048`).

---

## 🔴 RESULT

**Raising size is now one config edit plus one restart. The size itself has not moved:** LONG and SHORT are both
`$20 × 5 = $100` notional. Every change below is **proven behaviour-identical at that size**.

| what | today at $100 | proof |
|---|---|---|
| per-side margin `LIVE_FIXED_MARGIN_LONG/SHORT = 20` | same qty | **74,002 of 74,002** price×side points give an identical qty through the real `quantise_amount`. Fail-safe: **39 of 39** bad values fall back to `LIVE_FIXED_MARGIN` |
| daily $ floor, now size-aware | same decisions | all **47** live-era days replayed: the floor **is** 5% on **11 of 11** loss days, **0** decision differences |
| naked-position alert | now true | the size is read from the venue. **9 of 9** contract cases pass, including $100, $10,000 and "size unknown — read failed" |
| open card | margin text byte-identical | the only addition is `· $<qty × fill> notional` |
| balance pre-check | never fires | lowest live-era balance $117.34 vs largest need $20.01. **17 of 17** cases pass; an unreadable balance ADMITS |
| restart | 1, from flat | issued 15:42:30.008, up 15:42:32, PID 214356 → **218734** (worker **218787**) |
| orders placed / cancelled | **0 / 0** | venue position `updatedTime` identical before and after |
| Titan | **UNTOUCHED** | PID 4007821, `NRestarts=0`, same before and after |

**What the operator now decides:** the numbers. §8 has the procedure and the cost per stop-out at each size step.

**Three things this pass found that the brief did not know:**
1. **Equity was not $4,118 for most of the live era.** The venue's own USDT cash-balance history reads:
   * **$811.80** at the flip (2026-08-08)
   * **$400–$630** from 2026-08-23 to 09-22
   * **$117.34** at the low on 2026-09-22 18:49, after about $500 of USDT went into spot FIL
   * **$4,117** only after a $4,000 transfer-in at 19:03 that day

   The 09-22 report's $4,118 is correct for **today**. The 5% floor was **$20–$40** for most of the era, not $206.
2. **Unequal sizes let one side's R cancel the other side's losses.** Both R brakes sum R, so a +5R win on a $100
   SHORT cancels 5R of a $10,000 LONG's losses. With median stops, the R brake then fires at the **8th** LONG
   stop-out instead of the 3rd. The new $ floor catches it at the **6th**. That is the backstop working, and it is
   named here (§6), not fixed.
3. **The brief's advisor-prompt count.** The brief says 7 this time, and 7 is correct. All 7 are sha256-identical.

---

## 1. PER-SIDE MARGIN

**a)** `config.py` gains `LIVE_FIXED_MARGIN_LONG = 20` and `LIVE_FIXED_MARGIN_SHORT = 20`.
`LIVE_FIXED_MARGIN = 20` stays as the fallback. The resolver is `live_fixed_margin(position_side)`, and
`live_fixed_margin_max()` returns the larger side.

**b)** The sizing site in `_execute_single_entry` changes from `notional_usdt = LIVE_FIXED_MARGIN * LEVERAGE` to
`notional_usdt = live_fixed_margin(position_side) * LEVERAGE`. A valid per-side value is returned **as the same
object**, so at 20 `notional_usdt` is the same `int` 100.

**c) Fail-safe direction, by execution: 39 of 39 fall back to exactly `LIVE_FIXED_MARGIN`.** Each of these was
tested per side:
* missing, `None`, `'2000'` (quoted), `'abc'`, `True`, `False`
* `0`, `0.0`, `-20`, `-1e9`, `nan`, `inf`, `-inf`
* list, dict, complex, `Decimal('NaN')`

Unknown sides also fall back: `None`, `'long'`, `'BOTH'`, `''`, `123`.
A valid raise works and stays on its own side: LONG=2000 → LONG 2000, SHORT 20, max 2000.
⚠️ **A quoted number (`'2000'`) silently stays at $20.** That is the safe direction, and it is why §8 step 5
verifies the loaded value after every raise.

**d) Stored `margin_usdt`.** `virtual_trader.book_live_position` (the INSERT) and `_adopt_derive` (the
adoption-fields dict) now use `live_fixed_margin(position_side)`, the ACTUAL side's margin.
**The adoption path gets its side from the venue.** At boot, `state_by_side` is keyed by the side of the venue
position being adopted. That key is passed as `position_side` into `adopt_orphan_position(...)`, which books through
`book_live_position(..., position_side, ...)`, so both stored values carry the adopted side's margin.

**e)** `LEVERAGE = 5`, one value; `set_leverage(LEVERAGE, symbol)` is untouched. **f)** `PAPER_FIXED_MARGIN`
(2000) is untouched, and the paper sizing in `virtual_trader.py:228` is untouched.

**7c) The next LONG and the next SHORT size to exactly $100.** Old and new sizing were both run through the real
`stop_loss.quantise_amount`, with Bybit's live SOLUSDT market spec (public `load_markets`: lot 0.1, min 0.1,
minNotional 5). Every cent from $30.00 to $400.00, both sides: **74,002 of 74,002 identical.**
Samples: @73.63 → 1.3 SOL both; @117.82 → **0.8 SOL** both, which is #50's actual fill size; @120.00 → 0.8 both.

---

## 2. BLOCKER 1 — THE DAILY $ FLOOR, NOW SIZE-AWARE AND BEHIND THE R BRAKE

**a) The derivation (not a pick).** Clause 1 halts when the day's **ΣR ≤ −3.0**. Take a day with only losing
trades. While clause 1 is still silent (ΣR > −3), the day's $ loss is

> Σ |R_i| · risk_i < 3.0 × max(risk_i)

So a $ floor of **`DAILY_LOSS_R_LIMIT × 1R_ref`**, with `1R_ref ≥ max(risk_i)`, **cannot fire before the R brake
on such a day**. The multiplier *is* `DAILY_LOSS_R_LIMIT`: it is the smallest value that guarantees this ordering.
The two are tied in code, so moving one moves the other.

**b) Size-aware: I chose "a multiple of the largest configured 1R, with a hard ceiling".**
```
floor_pct = min( max(DAILY_LOSS_PCT_LIMIT, DAILY_LOSS_R_LIMIT × 1R_ref / equity), DAILY_LOSS_PCT_CEILING )
1R_ref    = max( live_fixed_margin_max() × LEVERAGE × DAILY_LOSS_STOP_PCT_REF ,  largest initial_risk_usdt closed today )
```
* **Why this form.** It follows the per-side config automatically, so nobody edits it on a raise.
* **Why the second term.** It keeps the proof true in an ATR regime wider than the reference, because the day's
  actual largest 1R always counts.
* **`DAILY_LOSS_STOP_PCT_REF = 0.033`** is the widest live stop distance on record: #40, 3.296% of entry.
* **Ceiling: `DAILY_LOSS_PCT_CEILING = 0.25`.** No day may lose more than a quarter of equity, whatever the R
  arithmetic says. 3R at the widest stop for $10,000 per side is **24.0%** of $4,115, so the ceiling does not
  bind at any size named so far. It binds once per-side notional exceeds **2.53 × equity (≈ $10,391 today)**, and
  from there the floor may fire before the R brake. That is deliberate: above that size, protecting the account
  from ruin outranks keeping the brakes in order.
* **Failure direction:** any error inside `_daily_loss_floor_pct` returns `DAILY_LOSS_PCT_LIMIT`, the old and
  stricter floor. It never raises.

**c) Fail-closed on unknown equity: unchanged.** The equity read, `equity <= 0 → return True,
'equity_unknown (fail-closed)'` and the outer `except → halt` are the same statements as before.

**d) 🔴 DORMANT AT $100 — every live-era day replayed.** Each day's closed live positions were summed with the
breaker's own SQL. Equity is the **lowest USDT cash balance on that day** from Bybit's
`/v5/account/transaction-log` (120 rows, 0 read errors, isolated circuits).

| day | $ PnL | ΣR | max 1R | lowest equity | new floor | old fires | new fires |
|---|---|---|---|---|---|---|---|
| 08-10 | −1.722 | −1.335 | 1.482 | 811.78 | **0.05 (is base)** | no | no |
| 08-12 | −0.068 | −0.049 | 1.391 | 811.67 | 0.05 (is base) | no | no |
| 08-13 | −0.911 | −0.643 | 1.417 | 810.80 | 0.05 (is base) | no | no |
| 08-14 | −0.729 | −0.701 | 1.040 | 810.07 | 0.05 (is base) | no | no |
| 08-16 | −0.728 | −0.757 | 0.962 | 796.76 | 0.05 (is base) | no | no |
| 08-17 | −1.116 | −1.226 | 0.910 | 795.74 | 0.05 (is base) | no | no |
| 09-03 | −2.838 | −1.083 | 2.620 | 403.87 | 0.05 (is base) | no | no |
| 09-11 | −2.131 | −1.110 | 1.920 | 403.91 | 0.05 (is base) | no | no |
| 09-14 | −1.881 | −1.133 | 1.660 | 601.14 | 0.05 (is base) | no | no |
| 09-17 | −3.239 | −1.069 | 3.030 | 577.46 | 0.05 (is base) | no | no |
| 09-23 | −2.647 | −1.092 | 2.424 | 4114.79 | 0.05 (is base) | no | no |

* **47 live-era days, 11 reach clause 2.** On 11 of 11 the floor **is** the `DAILY_LOSS_PCT_LIMIT` object, so
  the comparison is literally the old one. **0 decision differences.**
* Identity holds whenever equity ≥ **$198** (3 × $3.30 / 5%). The lowest equity on any loss day was **$403.87**.
  On 09-22, the one day equity dipped below $198, there was no closed loss, so clause 2 was never reached.
* Honest limit: below $198 of equity at $100 size, the new floor ($9.90) would be looser than 5% of equity. The R
  brake still stands at −3R.
* Log and DB: the old clause 2 **never fired** in the live era (0 rows, 0 log lines).

**e) At hypothetical sizes.** Equity is $4,115. Each case runs consecutive full stop-outs on the $10k side at each
of the 22 live stop widths. A loss is 1R plus 0.2% in fees.

*A: LONG $2,000 × 5, SHORT $20 × 5 · and · B: both $2,000 × 5.* The loss-only results are the same in both cases:

| live stop widths | old 5% floor ($205.74) fires at | R brake fires at | **new floor ($990, 24.1%) fires at** |
|---|---|---|---|
| 3 / 22 (widest) | stop-out **#1** | #3 | #3 (the same stop-out; clause 1 is checked first) |
| 3 / 22 | #1 | #3 | #4 |
| 3 / 22 | #1 | #3 | #5 |
| 1 / 22 | #2 | #3 | #5 |
| 2 / 22 | #2 | #3 | #6 |
| 6 / 22 | #2 | #3 | #7 |
| 4 / 22 (narrowest) | #2 | #3 | #8–#9 |

**In 22 of 22 cases the R brake fires first or on the same stop-out.** The old floor fired on the **1st or 2nd**
stop-out and halted **both** sides for the day.
Per stop-out at $10k: narrowest $114, median **$178**, widest **$350**.

**Mixed days (the gap the backstop exists for).** Median stop, the other side wins first:

| other side's win | A (other side $100): R brake / new floor / old | B (other side $10k): R brake / new floor / old |
|---|---|---|
| +1R | #4 / #6 / #2 | #4 / #7 / #3 |
| +2R | #5 / #6 / #2 | #5 / #8 / #3 |
| **+5R** | **#8 / #6** / #2 | #8 / #10 / #6 |

In case A, a +5R win worth $7.91 on the $100 SHORT cancels five LONG stop-outs' worth of R, about $890. The R brake
is blind until the 8th stop-out, and **the $ floor catches it at the 6th**. In case B the win is real dollars, so
the $ floor stays behind.

---

## 3. BLOCKER 2 — THE NAKED-POSITION ALERT

**a)** The line `🔴 … the exposure is the wallet balance, not the $100 notional.` is **gone from the alert's
bytecode**; `_sl_failsafe`'s code object holds no `$100`. At alert time, `_fetch_position_state(symbol, side)`
reads the venue. It is read-only and never raises. `_naked_exposure_text(state, pos, side)` renders the size from
`contracts`, and the notional from the venue's `notional` field, falling back to `contracts × markPrice`.
**b)** Any failed read renders **"Position size unknown — read failed."** No number is ever printed that was not
read.
**c) Contract, 9 of 9:**
```
$100 position    → … not just this position (0.8 SOL, $94.26 notional, read from the venue).
$10,000 position → … not just this position (84.9 SOL, $10,002.92 notional, read from the venue).
no notional field→ … (84.9 SOL, $10,002.92 notional …)   [contracts × markPrice]
size, no price   → … (0.8 SOL, read from the venue; notional unknown — price read failed).
read FAILED / unparseable / NaN / not-a-dict → … Position size unknown — read failed.
venue FLAT       → … A venue read at alert time showed no open LONG position — verify by hand; do not assume.
```
Cost: one extra read-only position fetch before this alert goes out (bounded by the ccxt timeout). It happens
only on the path where the stop could not be set **and** the emergency close failed.

---

## 4. BLOCKER 3 — THE OPEN CARD

The margin comes from the per-side value that sized **this** entry; paper keeps `active_fixed_margin()`. The
notional comes from `qty × fill` actually executed. A failed multiply drops the notional; it never invents one.
```
BEFORE  '📦 0.8  ⚙️ x5  💵 $20 margin\n'
AFTER   '📦 0.8  ⚙️ x5  💵 $20 margin · $94.26 notional\n'        (#50's values)
SHORT   '📦 0.8  ⚙️ x5  💵 $20 margin · $96.00 notional\n'        (@120.00)
PAPER   '📦 136.0  ⚙️ x5  💵 $2000 margin · $10,000.08 notional\n'
bad fill '📦 0.8  ⚙️ x5  💵 $20 margin\n'                          (identical to before)
```
**The margin text is byte-identical in every case.** The only change is the appended notional, which the brief
asked for. At $2,000 the card will say `$2000 margin · $10,00x notional`, not `$20`.

---

## 5. BALANCE PRE-CHECK

**a)** In `_execute_single_entry`, after the qty is quantised and **before** `set_leverage` or any order:
`need = qty×price/LEVERAGE (initial margin) + qty×price×taker`. The taker term is the open fee, which is the
stated buffer; the rate is the venue's, via `fee_rates`, and 0 if unreadable.
It **refuses only if** `totalAvailableBalance < need × (1 − 0.02)`.
**Why that can only refuse where the venue would:** Bybit's order cost is IM + open fee **+ close fee**, so `need`
is already below what the venue demands. The 2% slack also absorbs a ticker-to-fill move of up to ~2%.

**b)** A refusal raises `EntryBalanceRefused`. The handler then records `status='balance_refused'` and **calls**
`_record_skip_attribution(..., 'balance_refused', ...)`. The status is registered in `TRACKED_STATUSES`, and the
**AST walker is 10 of 10, 0 failures.** The card:
```
💸 BALANCE TOO LOW — LONG REFUSED
💎 SOL/USDT:USDT
required $2,010.59 (margin $2,000.58 + open fee $10.00)
available $1,500.00
No order was sent. The venue would have rejected it.
```
**c) Unreadable → ADMIT, 17 of 17.** These cases all ADMIT:
* read raises, field missing, `''`, NaN, inf, `info=None`
* amount None, taker read fails, kill switch off
* the exact boundary

It refuses **only** at available $1,500 vs need $2,010.59 (a $10k raise without the balance) and at $5 vs $18.95.
**d) It never fires at today's size.** The largest live-era need is **$20.01** (the $99.56 max notional). The
lowest USDT cash balance of the whole live era was **$117.34**. Today available is **$4,114.38** against a need of
$18.95.
Cost: one balance read per live entry (≈ 0.33/day), bounded by the ccxt timeout. A failed read admits.

---

## 6. NAMED, NOT FIXED — the $-denominated learning and ranking loops (§4e #7–#11)

| # | loop | **raised EQUALLY** (both sides ×N) | **raised UNEQUALLY** (one side big) |
|---|---|---|---|
| 7 | combo weights `signal_weights.py` (win ≥ +$20 / loss ≤ −$15 → ±0.05, feeds the advisor prompt) | at $100 almost every trade is "neutral". Above ~$2k notional per side both sides' trades classify again, so it **re-activates symmetrically** | only the big side's trades ever cross ±$20/−$15. **It learns combos from one side only**, and combos shared across sides get the big side's verdict |
| 8 | 15m subtype weights `engine_15m.py` (same thresholds) | re-activates symmetrically | learns from the big side only |
| 9 | feature weights `weight_engine.py` `tanh(avg_pnl/$20)` | saturates at ±1 on both sides at $10k. Informational only; nothing gates on it | the big side saturates, the small side reads ≈0. Harmless, because nothing gates on it |
| 10 | optimizer worst-segment `optimizer.py` (Σ$) | ranks both sides again | **the small side can never be the "worst segment"**; every proposal targets the big side |
| 11 | listener `MIN_LIVE_SHARE = 0.50` of \|$ PnL\| | live dollars swamp the paper book's $10k history once live reaches $10k; the guard becomes easy to satisfy | the same, driven by the big side alone |

**Also named:** the R-netting gap (§2e mixed days), which applies to both the −3.0R brake and the loss-streak
brake. And the breaker's equity fallback path `balance['info']['list']` is **dead**: the real path is
`info.result.list`. It only matters if `USDT.total` is missing, and then it fails closed. Untouched.

---

## 7. APPLIED FROM FLAT

**a) Flat, read twice.** First at 15:33:12, then again inside the restart script (venue 15:40:01, DB one second
before the restart):

| leg | result |
|---|---|
| `virtual_positions` not closed / `active_positions` / `exit_pending` | **0 / 0 / 0** |
| Bybit position idx 1 / idx 2 | **0 / 0**, both reported |
| Bybit open orders / conditional orders | **0 / 0** |
| venue error list | **EMPTY**, every read succeeded on attempt 1 on its own random-SOCKS circuit |

**b) Backups and the AST proof.**
`config.py`, `main.py`, `virtual_trader.py`, `skip_attribution.py` and `OPEN-ITEMS-SOL.md` were each copied to
`*.bak_sizeready_20260923` first. Each `.bak`'s sha256 equals the pre-patch file's.

| file | pre sha256 | post sha256 | AST |
|---|---|---|---|
| `config.py` | `75394428…df44e2` | `ccf11e8d…9c4389` | constants 143 → 149, **ADDED 6**, CHANGED 0, REMOVED 0. Defs ADDED `live_fixed_margin`, `live_fixed_margin_max`. **0 lines deleted** |
| `main.py` | `58f14eac…fd02dc` | `5586d104…c4b494` | ADDED `EntryBalanceRefused`, `_balance_precheck`, `_daily_loss_floor_pct`, `_naked_exposure_text`. CHANGED `_check_daily_loss_breaker`, `_execute_single_entry`, `_handle_5m_trigger`, `_sl_failsafe`. REMOVED none. `from config import` +6 names. **7 lines deleted, each one an intended replacement** (diff §9) |
| `virtual_trader.py` | `eeeff98a…55cdfaa` | `7fea781c…618e1c78` | CHANGED `book_live_position`, `_adopt_derive` (1 line each). Import +`live_fixed_margin` |
| `skip_attribution.py` | `58b59687…c768e1` | `3fda23c6…18d380` | only `TRACKED_STATUSES` (+`balance_refused`) |
| `claude_advisor.py` | `52feade7…ec6c36` | **unchanged** | never opened for writing |

**From the LOADED bytecode.** `.pyc` compiled 15:36:33; the header mtime and size match the source; the process
started 15:42:32.

| | | | |
|---|---|---|---|
| ✅ `LIVE_FIXED_MARGIN` **20** | 🆕 `LIVE_FIXED_MARGIN_LONG` **20** | 🆕 `LIVE_FIXED_MARGIN_SHORT` **20** | ✅ `LEVERAGE` **5** |
| `live_fixed_margin('LONG'/'SHORT'/None)` → **20 / 20 / 20** | ✅ `PAPER_FIXED_MARGIN` 2000 | ✅ `SL_BUFFER_ATR` 2.5 | ✅ `TRAIL_MULT_ATR` 1.875 |
| ✅ `TRAIL_ARM_R` 0.75 | ✅ `CONFLUENCE_SCORE_THRESHOLD` 2.0 | ✅ `FLAT_ADX_GATE_DRYRUN` **True** | ✅ `BOOK_GATE_ENABLED` **True** / `DRYRUN` **False** |
| ✅ `BULL_DAILY_SHORT_BLOCK` **True / False** | ✅ `BEAR_DAILY_LONG_BLOCK` **True / False** | ✅ `EXIT_ADVISOR_DRYRUN` True | ✅ `MAX_POSITIONS_PER_SIDE` 1 |
| ✅ `DAILY_LOSS_R_LIMIT` 3.0 | ✅ `DAILY_LOSS_PCT_LIMIT` 0.05 | 🆕 `DAILY_LOSS_STOP_PCT_REF` 0.033 / `CEILING` 0.25 | 🆕 `BALANCE_PRECHECK_ENABLED` True / `SLACK` 0.02 |

`TRACKED_STATUSES` (loaded) ends in `…, 'bear_daily_blocked', 'balance_refused')`.
**All seven advisor system prompts are sha256-identical**, read from the executed `claude_advisor` bytecode:

| prompt | sha256 |
|---|---|
| `_ENTRY_SYSTEM` | `cc70ed45…` ✅ |
| `_ENTRY_SYSTEM_V2` | `894a6c20…` ✅ |
| `_ENTRY_SYSTEM_V2_ALIGNED` | `f221365f…` ✅ |
| `_ENTRY_SYSTEM_V2_ALIGNED_SHORT` | `e1487999…` ✅ |
| `_CLOSE_SYSTEM` | `37bcdce4…` ✅ |
| `_CLOSE_STATE_SYSTEM` | `3be10726…` ✅ |
| `_LEARNING_SYSTEM` | `aa35142e…` ✅ |

**d) Restart and boot:**
```
15:42:30 systemd: Stopping mercury-sol.service …          (issued 15:42:30.008, mid 5-minute window)
15:42:32 systemd: Started mercury-sol.service
15:42:45 [SMART-CLEANUP] No open positions for SOL/USDT:USDT — proceeding with orphan cleanup
15:42:46 [AP] No active positions in DB — clean boot.
15:42:47 [BOOT] taker fee: 0.001 (0.1000%) source=venue
15:42:47 [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
15:42:47 [BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 218787]
15:42:53 [HEARTBEAT] alive ticks=1 cadence=10s open=0 mode=LIVE pid=218787
```
Venue after (15:43:07): sizes 0/0, orders 0/0, errors `[]`. Position `updatedTime` is unchanged on both indices.
There were no orders to cancel, and no cancel line was logged. `openitems_guard` after: **EXIT=0**.

**e) Canon.** `§SIZE-READY-2026-09-23` was written into `OPEN-ITEMS-SOL.md` after `§BEAR-DAILY-LONG-GATE`. It is
a pure insertion (2277 → 2382 lines, 0 removed) and carries the **COHORT BOUNDARY 2026-09-23 15:42:32 UTC**.

---

## 8. 🔴 THE ONE-LINE RAISE (also in canon, verbatim)

1. **Flat book:** 0 open `virtual_positions`, 0 `active_positions`, 0 `exit_pending`. Bybit idx 1 and idx 2 size
   0, with 0 open and 0 conditional orders, read over isolated Tor circuits with an **empty error list**.
2. **Balance:** `totalAvailableBalance` must exceed `(m_long + m_short) × 1.005`, with room for a full stop-out on
   each side (table). Otherwise the pre-check refuses the second side, cleanly.
3. **The change:** `LIVE_FIXED_MARGIN_LONG = <n>` and/or `LIVE_FIXED_MARGIN_SHORT = <n>` in `config.py`. Use a
   **plain number, no quotes.** Do not touch `LIVE_FIXED_MARGIN`, `LEVERAGE` or `PAPER_FIXED_MARGIN`. `.bak`
   first.
4. `python3 -m py_compile config.py`, then **one** `systemctl restart mercury-sol.service`, from flat, away from a
   5-minute boundary.
5. **Verify:**
   * boot `[BOOT-ASSERT] venue FLAT` and `HEARTBEAT … open=0 mode=LIVE`
   * from the **loaded bytecode**, `live_fixed_margin('LONG')` and `('SHORT')` return the new numbers
   * `openitems_guard` EXIT=0
   * on the first entry, the card shows the new margin and a notional ≈ 5× margin, and the venue size matches
6. Record a cohort boundary in canon.

**Cost of one full stop-out per side** (1R plus 0.1% taker on both legs; live stops: median 1.58%, p90 3.11%,
widest 3.30%). Equity is $4,115.

| margin/side | notional | stop-out: median / p90 / widest | daily $ floor | floor % | ceiling binds? | pre-check need |
|---|---|---|---|---|---|---|
| **$20 (today)** | $100 | $1.78 / $3.31 / $3.50 | $205.74 | 5.0% | no | $20.10 |
| $100 | $500 | $8.91 / $16.57 / $17.48 | $205.74 | 5.0% | no | $100.50 |
| $200 | $1,000 | $17.82 / $33.15 / $34.96 | $205.74 | 5.0% | no | $201.00 |
| $500 | $2,500 | $44.55 / $82.87 / $87.40 | $247.50 | 6.0% | no | $502.50 |
| $1,000 | $5,000 | $89.09 / $165.74 / $174.81 | $495.00 | 12.0% | no | $1,005.00 |
| **$2,000** | **$10,000** | **$178.19 / $331.47 / $349.61** | **$990.00** | **24.1%** | no | **$2,010.00** |
| $2,500 | $12,500 | $222.74 / $414.34 / $437.01 | $1,028.70 | 25.0% | **YES** | $2,512.50 |

At $2,000 on **both** sides, both positions open together need **$4,021** against **$4,114** available today, a
margin of $93. That is **less than one widest stop-out ($350)**.
* **While one side is open:** the other side still passes the pre-check only while the open side's unrealised
  loss stays under about **$134**.
* **After one median stop-out ($178):** the balance is about $3,936. That is enough for one $10k side at a time,
  but not for both at once.

The pre-check turns that into a clean `balance_refused` card, not a venue exception. The balance, not the code,
is what limits a both-sides $2,000 raise today.

---

## 9. CONFIRMATION

| | |
|---|---|
| every write stated before it ran | ✅ `.bak` ×5 → config (3 edits) → main (9 edits) → virtual_trader → skip_attribution → restart → canon → this report |
| `.bak` taken | ✅ `*.bak_sizeready_20260923` ×5, sha256 = pre-patch |
| orders placed / cancelled | **0 / 0**. All venue access was GET: `position/list`, `order/realtime`, `wallet-balance`, `transaction-log`, public `load_markets` |
| restarts | **exactly 1**, from flat, 15:42:30.008 UTC |
| size | **unchanged: $20 × 5 = $100 on both sides**, proven from the loaded bytecode and by 74,002 qty comparisons |
| Titan | **UNTOUCHED**. Only `tools/openitems_guard.py` (read-only) was run: EXIT 0 before, EXIT 0 after |
| Mercury-SOL is not a git repo | recorded by sha256, `.bak` and the diff below |

### The patch (unified diff against `*.bak_sizeready_20260923`)

```diff
--- a/config.py
+++ b/config.py
@@ -47,6 +47,43 @@
     return PAPER_FIXED_MARGIN if OBSERVATION_MODE else LIVE_FIXED_MARGIN
 
 
+# ── 🔴 PER-SIDE LIVE MARGIN (2026-09-23) — THE SIZE KNOB ─────────────────────
+# THESE TWO LINES ARE THE ONE-LINE RAISE. Everything that must follow size — the
+# order qty, the stored margin_usdt, the open card, the daily $ floor, the balance
+# pre-check — reads them through live_fixed_margin(). Procedure: canon
+# §SIZE-READY-2026-09-23. LEVERAGE stays ONE value for both sides.
+# Today both sides are EXACTLY LIVE_FIXED_MARGIN (20 × 5 = $100 notional).
+LIVE_FIXED_MARGIN_LONG  = 20
+LIVE_FIXED_MARGIN_SHORT = 20
+
+
+def live_fixed_margin(position_side):
+    """Live margin for ONE side. 🔴 FAIL-SAFE DIRECTION: a missing, None,
+    non-numeric (incl. bool and numeric strings), zero, negative or non-finite
+    per-side constant — or an unknown side — returns LIVE_FIXED_MARGIN, never a
+    larger number derived from anything else. A valid per-side value is returned
+    AS IS (same object, same type), so at 20 the arithmetic downstream is
+    byte-for-byte what it was with LIVE_FIXED_MARGIN."""
+    import math, numbers
+    name = {'LONG': 'LIVE_FIXED_MARGIN_LONG',
+            'SHORT': 'LIVE_FIXED_MARGIN_SHORT'}.get(position_side)
+    raw = globals().get(name) if name else None
+    if isinstance(raw, bool) or not isinstance(raw, numbers.Real):
+        return LIVE_FIXED_MARGIN
+    try:
+        if not (math.isfinite(raw) and raw > 0):
+            return LIVE_FIXED_MARGIN
+    except Exception:
+        return LIVE_FIXED_MARGIN
+    return raw
+
+
+def live_fixed_margin_max():
+    """The larger of the two resolved per-side margins — the LARGEST size the
+    config can hold, which is what the daily $ floor must sit behind."""
+    return max(live_fixed_margin('LONG'), live_fixed_margin('SHORT'))
+
+
 LEVERAGE    = 5           # Applies to BOTH books: paper 2000×5 = $10,000 notional, live 20×5 = $100.
 
 # ── Execution model — strict single-entry, NO DCA grid ──────────────────────
@@ -1306,6 +1343,41 @@
                                    # Kept because ruin risk IS denominated in percent
                                    # of balance. Dormant at $100 notional — that is not
                                    # a reason to discard it; it matters as size grows.
+# ── 🔴 2026-09-23 — THE $ FLOOR IS SIZE-AWARE AND SITS BEHIND THE R BRAKE ─────
+# The effective floor, as a fraction of USDT equity, is
+#     min( max(DAILY_LOSS_PCT_LIMIT, DAILY_LOSS_R_LIMIT × 1R_ref / equity),
+#          DAILY_LOSS_PCT_CEILING )
+#     1R_ref = max( live_fixed_margin_max() × LEVERAGE × DAILY_LOSS_STOP_PCT_REF,
+#                   largest initial_risk_usdt among TODAY's closed live positions )
+# DERIVED, not picked: on any day with only losing trades, the $ loss is
+# Σ|R_i|·risk_i < DAILY_LOSS_R_LIMIT × max(risk_i) ≤ DAILY_LOSS_R_LIMIT × 1R_ref
+# while the R brake is still silent — so a floor of R_LIMIT × 1R_ref can NEVER
+# fire before the R brake on such a day. The multiplier IS DAILY_LOSS_R_LIMIT;
+# move one and the other follows. The first term makes it size-aware from config;
+# the second keeps the proof true in an ATR regime wider than the reference.
+# Where it CAN fire first: a day whose R is netted by a win on the other side
+# (unequal sizes) — that is exactly the gap a $ backstop exists for.
+# At $100 per side, 3 × $3.30 = $9.90 < 5% of any equity ≥ $198, so the floor is
+# exactly DAILY_LOSS_PCT_LIMIT and the breaker is unchanged (live-era equity has
+# never been below $401 on a day with a closed loss).
+DAILY_LOSS_STOP_PCT_REF    = 0.033  # widest LIVE stop distance on record (#40, 3.296%), rounded up
+DAILY_LOSS_PCT_CEILING     = 0.25   # hard ceiling: a day may not lose more than 25% of
+                                    # equity whatever the R arithmetic says. Above
+                                    # 3R at the widest stop for $10,000 per side
+                                    # (24.0% of $4,118), so it does not bind at any
+                                    # size named so far; it binds (and the floor may
+                                    # then fire BEFORE the R brake) once per-side
+                                    # notional exceeds 2.53 × equity.
+# ── 🔴 BALANCE PRE-CHECK (2026-09-23) — a raise must never fail silently ─────
+# Before a LIVE entry: need = qty×price/LEVERAGE (initial margin) + qty×price×taker
+# (the OPEN fee — the stated fee buffer). Refuse only if Bybit's
+# totalAvailableBalance < need × (1 − BALANCE_PRECHECK_SLACK). Bybit's own order
+# cost is IM + open fee + CLOSE fee, so `need` is already BELOW what the venue
+# demands, and the 2% slack covers a ticker-to-fill move of up to ~2%. The check
+# can therefore only refuse where the venue would have refused. An UNREADABLE
+# balance ADMITS and lets the venue decide, exactly as before this existed.
+BALANCE_PRECHECK_ENABLED   = True
+BALANCE_PRECHECK_SLACK     = 0.02
 MAX_POSITIONS_PER_SIDE     = 1     # Max 1 open position per side at any time.
 LOSS_STREAK_THRESHOLD      = 3     # Consecutive losses before entering cooldown.
 # ── 🔴 2026-08-14 — THE BRAKE NOW FIRES ON DAMAGE, NOT ON A COUNTER ────────────
--- a/main.py
+++ b/main.py
@@ -1172,6 +1172,12 @@
     OBSERVATION_MODE,
     LIVE_FIXED_MARGIN,        # 2026-08-05: split by book — live path only
     active_fixed_margin,      # 2026-08-05: mode-resolved, for DISPLAY/storage
+    live_fixed_margin,        # 🔴 2026-09-23: per-side live margin (the size knob), fail-safe to LIVE_FIXED_MARGIN
+    live_fixed_margin_max,    # 🔴 2026-09-23: the larger side — what the daily $ floor sits behind
+    DAILY_LOSS_STOP_PCT_REF,  # 🔴 2026-09-23: size-aware $ floor — widest live stop on record
+    DAILY_LOSS_PCT_CEILING,   # 🔴 2026-09-23: size-aware $ floor — hard % ceiling
+    BALANCE_PRECHECK_ENABLED, # 🔴 2026-09-23: clean refusal instead of a venue exception
+    BALANCE_PRECHECK_SLACK,
     LEVERAGE,
     ATR_LEN,
     ATR_TF,
@@ -1871,6 +1877,37 @@
 _daily_loss_alerted = False   # suppress repeated TG alerts within same day
 
 
+def _daily_loss_floor_pct(equity, max_risk_today):
+    """Effective clause-2 floor as a fraction of equity. NEVER raises.
+
+    min( max(DAILY_LOSS_PCT_LIMIT, DAILY_LOSS_R_LIMIT × 1R_ref / equity), CEILING )
+    1R_ref = max(largest configured side × LEVERAGE × DAILY_LOSS_STOP_PCT_REF,
+                 largest initial_risk_usdt closed today).
+    Derivation and the proof that it sits behind the R brake: config.py, beside
+    DAILY_LOSS_STOP_PCT_REF. When the size term is at or below the base, this
+    returns DAILY_LOSS_PCT_LIMIT ITSELF, so the comparison is the pre-2026-09-23
+    one exactly. Any failure returns DAILY_LOSS_PCT_LIMIT — the old, stricter floor.
+    """
+    import math
+    base = DAILY_LOSS_PCT_LIMIT
+    try:
+        ref_1r = live_fixed_margin_max() * LEVERAGE * DAILY_LOSS_STOP_PCT_REF
+        try:
+            _today = float(max_risk_today)
+            if math.isfinite(_today) and _today > ref_1r:
+                ref_1r = _today
+        except (TypeError, ValueError):
+            pass
+        size_pct = DAILY_LOSS_R_LIMIT * ref_1r / float(equity)
+        if not math.isfinite(size_pct):
+            return base
+        floor = base if size_pct <= base else size_pct
+        ceiling = max(base, DAILY_LOSS_PCT_CEILING)
+        return floor if floor <= ceiling else ceiling
+    except Exception:
+        return base
+
+
 def _check_daily_loss_breaker():
     """Return (halted: bool, reason: str). Halts if today's loss >= DAILY_LOSS_PCT_LIMIT × equity.
     FAIL-CLOSED (D1, Titan parity): any risk-query error or unknown equity on a loss day
@@ -1906,7 +1943,8 @@
             row = conn.execute(
                 "SELECT COALESCE(SUM(net_pnl), 0), "
                 "       COALESCE(SUM(CASE WHEN initial_risk_usdt > 0 "
-                "                         THEN net_pnl / initial_risk_usdt ELSE 0 END), 0) "
+                "                         THEN net_pnl / initial_risk_usdt ELSE 0 END), 0), "
+                "       MAX(initial_risk_usdt) "
                 "FROM virtual_positions "
                 "WHERE status='closed' AND DATE(closed_at) = DATE('now') "
                 "  AND COALESCE(is_paper, 1) = ?", (_brake_book,)
@@ -1961,9 +1999,12 @@
             return True, 'equity_unknown (fail-closed)'
 
         loss_pct = -daily_pnl / equity
-        if loss_pct >= DAILY_LOSS_PCT_LIMIT:
+        # 🔴 2026-09-23: size-aware floor, behind the R brake. At $100 per side it
+        # returns DAILY_LOSS_PCT_LIMIT itself — see _daily_loss_floor_pct.
+        _floor_pct = _daily_loss_floor_pct(equity, row[2] if len(row) > 2 else None)
+        if loss_pct >= _floor_pct:
             reason = (f"daily_loss_equity_breaker (LIVE): {loss_pct*100:.2f}% >= "
-                      f"{DAILY_LOSS_PCT_LIMIT*100:.1f}% of equity")
+                      f"{_floor_pct*100:.1f}% of equity")
             if not _daily_loss_alerted:
                 _daily_loss_alerted = True
                 send_tg(f"🚨 <b>DAILY LOSS BREAKER TRIGGERED</b>\n<i>{reason}</i>")
@@ -2672,6 +2713,112 @@
         self.naked  = naked
 
 
+class EntryBalanceRefused(RuntimeError):
+    """🔴 2026-09-23. The balance pre-check found available balance below what the
+    order needs. Raised BEFORE set_leverage / the order — nothing was sent. The
+    handler records status='balance_refused', calls the skip-attribution hook and
+    sends a card naming required vs available."""
+
+    def __init__(self, message, *, detail):
+        super().__init__(message)
+        self.detail = detail
+
+
+def _balance_precheck(amount, price):
+    """(ok, detail). ok=False ONLY when a READ available balance is below the need.
+
+    need = qty×price/LEVERAGE + qty×price×taker (open fee). Refuse only if
+    available < need × (1 − BALANCE_PRECHECK_SLACK). Bybit's own order cost adds the
+    CLOSE fee on top, so this is strictly more lenient than the venue. 🔴 Every
+    failure — arithmetic, the balance read, a missing/unparseable/non-finite field,
+    the kill switch — returns ok=True: ADMIT and let the venue decide, as before.
+    NEVER raises."""
+    import math
+    detail = {'need': None, 'im': None, 'fee': None, 'available': None, 'why': None}
+    if not BALANCE_PRECHECK_ENABLED:
+        detail['why'] = 'disabled'
+        return True, detail
+    try:
+        notional = float(amount) * float(price)
+        im = notional / LEVERAGE
+        try:
+            taker = float(fee_rates.taker_rate(exchange, DEFAULT_SYMBOL))
+            if not (math.isfinite(taker) and taker >= 0):
+                taker = 0.0
+        except Exception:
+            taker = 0.0
+        fee = notional * taker
+        need = im + fee
+        if not (math.isfinite(need) and need > 0):
+            detail['why'] = 'ADMIT — need not computable'
+            return True, detail
+        detail.update(need=need, im=im, fee=fee)
+    except Exception as e:
+        detail['why'] = f'ADMIT — sizing arithmetic failed ({type(e).__name__})'
+        return True, detail
+    try:
+        bal = tor_retry.with_socks_retry(
+            exchange, lambda ex: ex.fetch_balance({'type': 'swap'}),
+            label='balance.precheck')
+        available = float(bal['info']['result']['list'][0]['totalAvailableBalance'])
+        if not math.isfinite(available):
+            raise ValueError(f'non-finite {available!r}')
+    except Exception as e:
+        detail['why'] = f'ADMIT — balance unreadable ({type(e).__name__})'
+        print(f"{LOG_PREFIX}[BALANCE-PRECHECK] balance unreadable ({e}) — ADMIT, "
+              f"the venue decides", flush=True)
+        return True, detail
+    detail['available'] = available
+    if available < need * (1.0 - BALANCE_PRECHECK_SLACK):
+        detail['why'] = 'REFUSE — available below need'
+        return False, detail
+    detail['why'] = 'ok'
+    return True, detail
+
+
+def _naked_exposure_text(state, pos, position_side):
+    """The exposure clause of the naked-position alert, from a VENUE read only.
+
+    🔴 2026-09-23: replaces the literal "not the $100 notional". Never prints a
+    number that was not read: an unreadable size says so. NEVER raises."""
+    import math
+    _unknown = ("🔴 The account is on <b>CROSS margin</b> — the exposure is the "
+                "wallet balance. <b>Position size unknown — read failed.</b>")
+    try:
+        if state == POS_FLAT:
+            return ("🔴 The account is on <b>CROSS margin</b>. A venue read at alert "
+                    f"time showed <b>no open {position_side} position</b> — verify "
+                    "by hand; do not assume.")
+        if state != POS_OPEN or not pos:
+            return _unknown
+        size = float(pos.get('contracts'))
+        if not (math.isfinite(size) and size > 0):
+            return _unknown
+        notional = None
+        try:
+            v = float(pos.get('notional'))
+            if math.isfinite(v) and v > 0:
+                notional = v
+        except (TypeError, ValueError):
+            pass
+        if notional is None:
+            try:
+                mp = float(pos.get('markPrice'))
+                if math.isfinite(mp) and mp > 0:
+                    notional = size * mp
+            except (TypeError, ValueError):
+                pass
+        if notional is None:
+            return ("🔴 The account is on <b>CROSS margin</b> — the exposure is the "
+                    f"wallet balance, not just this position (<b>{size:g} SOL</b>, "
+                    "read from the venue; notional unknown — price read failed).")
+        return ("🔴 The account is on <b>CROSS margin</b> — the exposure is the "
+                f"wallet balance, not just this position (<b>{size:g} SOL, "
+                f"${notional:,.2f} notional</b>, read from the venue).")
+    except Exception:
+        return _unknown
+
+
 def _record_naked_position(symbol, position_side, *, stage, detail):
     """Persist a naked/unknown-protection event to its OWN table.
 
@@ -2725,13 +2872,19 @@
         _record_naked_position(symbol, position_side, stage='sl_failsafe_close_failed',
                                detail=f'attempted_sl={attempted_sl} err={ec}')
         print(f"{LOG_PREFIX}[SL-FAIL-SAFE] 🔴 emergency close FAILED: {ec}", flush=True)
+        # 🔴 2026-09-23: the size in this alert is READ from the venue position it is
+        # about — never a config constant. _fetch_position_state never raises; a
+        # failed read renders "size unknown — read failed".
+        try:
+            _nk_state, _nk_pos = _fetch_position_state(symbol, position_side)
+        except Exception:
+            _nk_state, _nk_pos = POS_UNKNOWN, None
         send_tg(f"🔴🔴🔴 <b>NAKED POSITION — EMERGENCY CLOSE FAILED</b>\n"
                 f"{symbol} {position_side}\n"
                 f"The stop could NOT be set (3 attempts) and the emergency close "
                 f"then FAILED too: <code>{str(ec)[:200]}</code>\n"
                 f"<b>A funded position may be OPEN on Bybit with NO STOP.</b>\n"
-                f"🔴 The account is on <b>CROSS margin</b> — the exposure is the "
-                f"wallet balance, not the $100 notional.\n"
+                f"{_naked_exposure_text(_nk_state, _nk_pos, position_side)}\n"
                 f"🔴 <b>NOTHING WILL FIX THIS BY ITSELF.</b>\n"
                 f"<b>Do now:</b> 1) open Bybit, check for a {position_side} position "
                 f"on {symbol}; 2) if it exists, set a stop or close it BY HAND; "
@@ -2965,7 +3118,10 @@
     # 2026-08-05: the LIVE constant explicitly — everything below this point in
     # this function runs only when OBSERVATION_MODE is False (the paper branch
     # returned above). The paper book keeps PAPER_FIXED_MARGIN and is untouched.
-    notional_usdt = LIVE_FIXED_MARGIN * LEVERAGE
+    # 🔴 2026-09-23: per side. live_fixed_margin() falls back to LIVE_FIXED_MARGIN on
+    # any bad per-side value, never to a larger number. At 20/20 this is the same
+    # object as before, so notional_usdt is the same int (100).
+    notional_usdt = live_fixed_margin(position_side) * LEVERAGE
     # Phase 1 (3): round DOWN to the venue lot step and validate min qty/notional.
     # `price` is the ticker we already hold — no extra network call.
     amount, _qerr = quantise_amount(exchange, symbol, notional_usdt / current_price,
@@ -2976,6 +3132,16 @@
         send_tg(f"🚫 <b>Entry aborted</b> — size below venue minimum ({symbol})")
         return None
 
+    # 🔴 2026-09-23 — BALANCE PRE-CHECK. Raises EntryBalanceRefused (its own status,
+    # its own card) only when the venue would have refused anyway; an unreadable
+    # balance ADMITS. Before any order-side call, so nothing has been sent.
+    _bal_ok, _bal = _balance_precheck(amount, current_price)
+    if not _bal_ok:
+        raise EntryBalanceRefused(
+            f"balance pre-check: need ${_bal['need']:.2f} (IM ${_bal['im']:.2f} + "
+            f"open fee ${_bal['fee']:.2f}) > available ${_bal['available']:.2f}",
+            detail=_bal)
+
     try:
         tor_retry.with_socks_retry(exchange, lambda ex: ex.set_leverage(LEVERAGE, symbol), label='set_leverage')
     except Exception as e:
@@ -5507,6 +5673,37 @@
                   f"row={row_id}: {e}", flush=True)
             return jsonify({'status': e.status, 'naked': e.naked,
                             'message': str(e), 'combo': combo}), 500
+        except EntryBalanceRefused as e:
+            # 🔴 2026-09-23 — a clean refusal where the venue would have refused
+            # anyway. NOTHING was sent (raised before set_leverage / the order).
+            # Registered in skip_attribution.TRACKED_STATUSES in the same pass and
+            # the hook is CALLED here, not merely registered.
+            _bd = e.detail or {}
+            update_trade(row_id, status='balance_refused', error=str(e), combo_key=combo,
+                         confluence_score=direction_score,
+                         matrix_direction=matrix_result['direction'],
+                         matrix_breakdown_json=matrix_bkdn_json)
+            _record_skip_attribution(row_id, symbol, direction, 'balance_refused',
+                                     matrix_result=matrix_result,
+                                     confluence_score=direction_score,
+                                     pre_trade_walls=locals().get('_pre_walls'),
+                                     ai_reason=str(e),
+                                     srv_adx_1h=_adv_snap.get('srv_adx_1h'),
+                                     trend_4h=_adv_snap.get('trend_4h'),
+                                     trend_1d=_adv_snap.get('trend_1d'))
+            send_tg(
+                f"💸 <b>BALANCE TOO LOW — {position_side} REFUSED</b>\n"
+                f"💎 {symbol}\n"
+                f"required <b>${_bd.get('need', 0):,.2f}</b> (margin ${_bd.get('im', 0):,.2f} "
+                f"+ open fee ${_bd.get('fee', 0):,.2f})\n"
+                f"available <b>${_bd.get('available', 0):,.2f}</b>\n"
+                f"<i>No order was sent. The venue would have rejected it.</i>\n"
+                f"<code>{combo}</code>"
+            )
+            print(f"{LOG_PREFIX}[BALANCE-PRECHECK] REFUSED {position_side} row={row_id}: {e}",
+                  flush=True)
+            return jsonify({'status': 'balance_refused', 'direction': direction,
+                            'reason': str(e), 'combo': combo}), 200
         except Exception as e:
             err = str(e)
             update_trade(row_id, status='failed', error=err, combo_key=combo,
@@ -5606,11 +5803,20 @@
             _macro_blk = ""
         _news_block = (f"\n\n📰 <b>News (last 2h):</b>\n{_news_summary}"
                        if _news_summary else "")
+        # 🔴 2026-09-23: THIS entry's margin (the per-side value that sized it; paper
+        # keeps active_fixed_margin()) and its notional from qty × fill actually
+        # executed. A failed multiply drops the notional, never invents one.
+        _card_margin = (active_fixed_margin() if entry.get('_virtual')
+                        else live_fixed_margin(position_side))
+        try:
+            _card_notional = f" · ${float(entry['amount']) * float(entry['fill_price']):,.2f} notional"
+        except Exception:
+            _card_notional = ""
         send_tg(
             f"{_open_hdr}\n"
             f"💎 {symbol}  @ {entry['fill_price']}\n"
             f"{_macro_blk}"
-            f"📦 {entry['amount']}  ⚙️ x{LEVERAGE}  💵 ${active_fixed_margin()} margin\n"
+            f"📦 {entry['amount']}  ⚙️ x{LEVERAGE}  💵 ${_card_margin} margin{_card_notional}\n"
             f"📈 ATR({ATR_LEN},{ATR_TF}): {entry['atr']:.4f}\n"
             f"🛡 SL {sl_tag} {entry['sl_price']}   🎯 TRAIL {tp_tag} {entry['trail_pct']}%  (arms @ {entry['active_price']})\n"
             f"{indicators.ema_trend_line(_snap)}\n"
--- a/virtual_trader.py
+++ b/virtual_trader.py
@@ -40,6 +40,7 @@
     MONITOR_POLL_FALLBACK_SECONDS,   # PHASE 2: adaptive cadence absorbed from the retired monitor
     OBSERVATION_MODE,                # PHASE 2: stamps is_paper provenance on new rows
     PAPER_FIXED_MARGIN, LIVE_FIXED_MARGIN,   # 2026-08-05: split by book
+    live_fixed_margin,   # 🔴 2026-09-23: the stored margin_usdt is the ACTUAL side's margin
     LEVERAGE, ATR_LEN, ATR_TF, SL_WALL_ANCHOR_ENABLED,
     TRAIL_MULT_ATR,   # BYBIT_TAKER_FEE_RATE deliberately NOT imported: accounting
                       # asks fee_rates.taker_rate() (2026-08-08). The constant is
@@ -2572,7 +2573,7 @@
                 " entry_atr_pct_1h, recheck_status, "
                 " is_paper) "
                 "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,'open',?,?,?,?,?,?,?,?,?,?,0)",
-                (symbol, position_side, side, LIVE_FIXED_MARGIN, amount, LEVERAGE,
+                (symbol, position_side, side, live_fixed_margin(position_side), amount, LEVERAGE,
                  fill_price, atr, sl_price, trail_pct, json.dumps(mgmt_state),
                  json.dumps(fills), fill_price, opened_at, trades_row_id,
                  initial_risk_usdt, sl_price, fill_price,
@@ -2760,7 +2761,7 @@
         'breakeven_price': be_px,
         'partial_fraction': PARTIAL_AT_ARM_FRACTION,
         'partial_size_raw': size * PARTIAL_AT_ARM_FRACTION,
-        'margin_usdt': LIVE_FIXED_MARGIN, 'leverage': LEVERAGE,
+        'margin_usdt': live_fixed_margin(position_side), 'leverage': LEVERAGE,
         'water_mark': fill, 'max_adverse_price': fill,
         'mgmt_state': {'breakeven_applied': False},
         'recheck_status': 'done',
--- a/skip_attribution.py
+++ b/skip_attribution.py
@@ -77,7 +77,10 @@
 # called at the refusal site, verified by AST walk.
 TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked', 'risk_halt',
                     'book_blocked', 'flat_adx_blocked', 'bull_daily_blocked',
-                    'entry_gate_refused', 'bear_daily_blocked')
+                    'entry_gate_refused', 'bear_daily_blocked',
+                    'balance_refused')
+# 🔴 'balance_refused' added 2026-09-23 WITH the balance pre-check, same pass,
+# registered here AND called at the refusal site in main.py (AST walker).
 
 # Drift sample offsets from the skip (label -> seconds). Same horizons as PEO.
 DRIFT_SLOTS = [('15m', 900), ('1h', 3600), ('4h', 14400),
```
