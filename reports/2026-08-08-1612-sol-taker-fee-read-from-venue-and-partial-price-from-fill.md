# sol-taker-fee-read-from-venue-and-partial-price-from-fill

_2026-08-08 16:12 UTC_

---

# Mercury-SOL — the fee is now READ from Bybit and the partial books the FILL. Both applied and live.

**The venue reports `takerFeeRate: 0.001` — the rate is readable, so it is read and cached, not
replaced with a second hardcoded guess. The partial now books the execution price, not the poller's
ticker. Together they close the 0.01774 USDT overstatement measured on row 29's leg.
Row 29 was NOT touched. Titan untouched.**

🔴 **One thing stopped me before I wrote a line, and it is the most important paragraph here:
changing `BYBIT_TAKER_FEE_RATE` in place would have prevented the bot from booting.** It is not
only a fee rate — it is also a geometry input. Details in §1.

Prior: [both items applied 15:48](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1548-sol-both-items-applied-orphan-adopted-live.md)

---

## 1. 🔴 WHY THE OBVIOUS FIX WOULD HAVE BROKEN THE BOT

`config.py` does this:

```python
BYBIT_TAKER_FEE_RATE    = 0.00055
MIN_PROFIT_DISTANCE_PCT = 2 * (BYBIT_TAKER_FEE_RATE + SLIPPAGE_BUFFER_PCT)   # 0.0015
```

So the constant has **two jobs**: what a fill COSTS (accounting) and how far price must move to be
worth trading (policy/geometry). `MIN_PROFIT_DISTANCE_PCT` feeds:

- `trail_arm._BE_TARGET_FRAC_ON` — the **breakeven-lock target price**;
- `stop_loss._select_stop_wall` and the SL fallback floor;
- the EQH/EQL distance gate at `main.py:3890`.

Setting the constant to the true `0.001`:

```
BYBIT_TAKER_FEE_RATE=0.001 -> MIN_PROFIT_DISTANCE_PCT=0.0024 -> BE target frac 0.0029
  trail_arm import assert: TRAIL_MIN_ACTIVATION_PCT(0.0025) > 0.0029 ?  FALSE
  breakeven target on a 74.80 entry: 74.9496 -> 75.0169
```

That assert is **at module import**, so the service would have failed to start — and it would also
have moved the breakeven target and the stop-wall filter, which is exactly the geometry you
forbade. You asked me to fix what a fee costs, not what the bot decides.

**So the two roles are split.** Accounting now asks a new `fee_rates` module that reads the venue.
`BYBIT_TAKER_FEE_RATE` keeps its value and its geometry job, with the reason written at its
declaration so nobody re-conflates them. Verified after install:

```
BYBIT_TAKER_FEE_RATE    = 0.00055   unchanged
MIN_PROFIT_DISTANCE_PCT = 0.0015    unchanged
breakeven_target(74.80) = 74.9496   unchanged
activation_distance     = 0.9100    unchanged
compute_initial_sl LONG = 73.89 route=fallback_atr   unchanged
```

**Whether `MIN_PROFIT_DISTANCE_PCT` should itself be recalibrated on the true 0.1% is a real
question and it is now OPEN, not answered.** It would raise the round-trip viability bar from 0.15%
to 0.24% and change entries — a decision, not a bug fix.

---

## 2. (1a) THE RATE IS READ FROM THE VENUE

```
GET /v5/account/fee-rate?category=linear&symbol=SOLUSDT
-> retCode 0  {"symbol":"SOLUSDT","takerFeeRate":"0.001","makerFeeRate":"0.00036"}
```

0.100%, matching both of today's measurements exactly. New module `fee_rates.py`:

| behaviour | result |
|---|---|
| venue read | `rate=0.001 source=venue` |
| second call | `source=cache`, **no re-read** (6h TTL, off the 10s poller's hot path) |
| no exchange handle, warm | `source=cache` |
| venue read raises | `rate=0.001 source=measured` |
| no exchange handle, cold | `rate=0.001 source=measured` |
| reply says 90% | **refused** → `measured` |
| reply empty | **refused** → `measured` |
| `retCode != 0` | **refused** → `measured` |

🔴 **The fallback is 0.001 — the MEASURED rate — and is deliberately NOT
`config.BYBIT_TAKER_FEE_RATE`.** Falling back to the number the module exists to correct would let
a Tor outage silently restore the bug. Asserted in the test.

Every call site reports its source, so a modelled rate is never indistinguishable from a read one —
the rule `_resolve_fee` already applies to the fee itself.

**Primed at boot**, above the orphan assert, because `close_position()` has no exchange handle and
the assert's adoption path books an entry fee. Live boot line:

```
16:09:16 [BOOT] taker fee: 0.001 (0.1000%) source=venue | geometry constant
                BYBIT_TAKER_FEE_RATE=0.00055 is unchanged and separate
```

Five accounting sites moved onto it: the paper entry fee, `close_position`'s close fee, the
partial's close fee, `book_live_position`'s modelled fallback, and `main._resolve_fee`. The
constant is no longer imported by `main.py` or `virtual_trader.py` at all, so it cannot be reached
for by accident.

---

## 3. (2) THE PARTIAL BOOKS THE FILL

`_execute_partial_close` now returns **`(filled_qty, fill_price)`** — `average` is on the same order
object `filled` already came from, so it costs nothing to read. All three exits return 2-tuples
(AST-verified), and the single caller unpacks.

Replaying the **real 15:40:49 leg** — ticker 76.36, venue fill 76.35, qty 0.4:

```
[PARTIAL] vpos=900 realised 0.3333 (0.4) @ 76.35 [venue_fill] pnl=+0.5595
          fees=0.0605 @rate=0.001[venue] — remainder 0.9

booked partial_price = 76.35        <- the FILL, not the ticker
booked partial_pnl   = +0.55954
independent truth    = +0.55954     <- gross 0.4x1.55 - entry share - 0.1% close fee
what the OLD code booked           : +0.57728
the 0.01774 overstatement          : GONE (0.01774 recovered)
```

Provenance is stamped on the fill itself: `price_source='venue_fill'`, `fee_rate=0.001`,
`fee_rate_source='venue'`.

**The ticker survives only as a labelled estimate**, mirroring `main.py:2889`:

```
[PARTIAL] fill price unreadable — using ticker 76.36 as a LABELLED estimate
[PARTIAL] ... @ 76.36 [ticker_estimate] ...
```

with `price_source='ticker_estimate'` on the fill. The size fallback (derived from the position
size) proves a QUANTITY and never a price, so it correctly yields `None` and triggers the label.

---

## 4. (1b) WHAT THIS DID TO THE PAPER BOOK — THE BOUNDARY, NOT A REWRITE

**History is NOT rewritten.** The boundary is recorded so no study pools across it, the way the ADX
window boundary is recorded.

```
🔴 FEE BOUNDARY — Mercury-SOL
   vpos id <= 29  : fees modelled at 0.00055 (0.055%) — UNDERSTATED 1.82x
   vpos id >= 30  : fees at the VENUE rate (0.001 read live, or 0.001 measured fallback)
   Row 29 straddles it: its entry fee is the VENUE's 0.09724, its partial fee is
   MODELLED at 0.055%. It is the only mixed row and it is left as booked.
```

Effect on the 22 closed paper positions, if their fees had been right:

```
total understated cost      : 197.7638 USDT across 22 rows (~$9.00 per round trip
                              at a ~$9,994 paper notional)
win rate                    : 8/22 = 36.4%  ->  7/22 = 31.8%
positions whose SIGN flips  : ONE — vpos 17, +0.8624 -> -8.1298
```

---

## 5. (1c) 🔴 DID IT CHANGE DECISIONS ALREADY TAKEN? — MEASURED, NOT ASSERTED

I re-ran the real `weight_engine.compute_weight_updates` twice from today's actual weight file:
once on the book as booked, once with every closed pair's fee corrected by 1.82×.

**Weights: 7 of 18 segments move, and all of them barely.**

```
mtf_alignment_score:mtf_4            1.5433 -> 1.5202  (-0.0231)   <- largest
ema9_slope_state_15m:Inclined_Down   0.5350 -> 0.5286  (-0.0064)
ema9_slope_state_1h:Inclined_Down    0.5350 -> 0.5286  (-0.0064)
ema_status_15m:Bearish               0.5350 -> 0.5286  (-0.0064)
mc_funding_rate:funding_negative     2.1372 -> 2.1325  (-0.0047)
dxy_trend:DOWNTREND                  0.7445 -> 0.7424  (-0.0021)
macro_news_category:NEUTRAL          0.5077 -> 0.5061  (-0.0016)

max |delta| 0.0231, against LEARNING_RATE 0.10 (one full gradient step) on a table
spanning 0.20-2.10.
```

**So: inside the noise, on the weights.** The largest change is under a quarter of one gradient step
and ~1.1% of that weight's own value. The reason is the one measured on 2026-08-08 14:17 — at paper
magnitudes the `tanh(avg_pnl/20)` term is **already saturated** (−0.97 to −0.999), so a $9 fee
correction is absorbed. The win-rate half moves more (`mtf_4` 36.4%→27.3%, `funding_low` 50%→37.5%,
`news_overall:POS` 40%→30%), but at 0.6 weighting inside a 0.10 learning rate it still lands small.

**🔴 But there IS one decision-relevant consequence, and it is not in the weights.**

```
mtf_alignment_score:mtf_4   n=11   avg_pnl  +3.86  ->  -5.15      SIGN FLIP
                                   total   +42.5   ->  -56.6
```

`find_worst_segment` only proposes a filter when `total < 0`. Booked, that segment reads
**+$42.5 and is not a candidate**; corrected, it reads **−$56.6 and is**. **The understated fee hid
a losing segment from the filter proposer.** Direction of the whole error, stated plainly: fees too
low → net_pnl too high → segments look better than they are → **the optimizer has been too LENIENT,
never too harsh.** Nothing was wrongly filtered; something was wrongly spared.

And a forward-looking note that inverts the intuition: the correction matters **more** for live
trades than paper ones. At paper magnitudes tanh is saturated and absorbs it; at live magnitudes
(1R = $1.18) it sits in the linear region, where a $9-equivalent error would swing the PnL half of
the gradient five-fold. Fixing this before the live cohort fills up was the right order.

---

## 6. (3) ROW 29 NOT TOUCHED — and (4) nothing else changed

Row 29 after the restart, byte-compared against before:

```
id 29 | size 0.9 | sl_price 74.9496 | status open | trail_pct 0.909
partial_size 0.4 | partial_price 76.36 | partial_pnl 0.5772808 | partial_fees 0.0467192
mgmt_state {"breakeven_applied": true, "partial_done": true}
partial_price still 76.36 (NOT retroactively edited): True
partial_pnl   still 0.57728 (NOT retroactively edited): True
```

It keeps the numbers it was booked with. A retroactive edit to a live position is a different act,
as you said.

**(4) Nothing else changed.** No cascade, no thresholds, no prompts, no geometry, no
breakeven/partial/trail formulas, no risk gates — verified by execution in §1 and by the diff's
shape: every removed line is an arithmetic expression that swapped its rate source, a signature, or
a docstring. The only formula that changed is `fee = price × qty × rate`, and only in `rate`.

---

## PROOF BY EXECUTION — 17 VECTORS, SEARCHED BY DIRECTORY

```
by DB filename : 13     by DIRECTORY : 16     (+ .env = 17 VECTORS)
missed by the filename grep: healthcheck.py, mercury_sol_prior_move_logger.py,
                             weight_engine.py  <- holds WEIGHTS_PATH to prod weights
fee_rates.py is NEW and contains 0 prod-path literals, so the census is still 17.
```

Lab: full copied tree, all 17 rewritten (**0 prod-path literals remaining**),
`sys.dont_write_bytecode=True`, lock on `sqlite3.connect` **and** write-mode `open()` asserting
against **both** the prod directory and `/root/titan-bot`. **Leaks: 0. All assertions passed.**

One incidental proof of correct behaviour: the fixture INSERT initially hit
`UNIQUE constraint failed` from `ux_vpos_one_open_per_side`, because the lab DB carries the real
open vpos 29 — the index doing its job. The fixture was moved to its own symbol.

### Diffstat

```
config.py          +15   -1     (documentation only — the VALUE is unchanged)
virtual_trader.py  +52  -15
main.py            +40   -8
fee_rates.py       NEW, 129 lines
```

All 24 removed lines accounted for: 5 fee-arithmetic lines that swapped their rate source, 3 import
lines, 2 function signatures, 3 return statements changed to 2-tuples, and 11 docstring/log lines
replaced by ones that carry provenance.

---

## DEPLOYMENT

Backups `*.bak_feerate_20260808_160744`, md5-verified against the live files before the write.
Restarted **16:08:56**, worker pid **3533987**.

```
16:09:16 [BOOT] taker fee: 0.001 (0.1000%) source=venue | geometry constant unchanged
16:09:17 [BOOT-ASSERT] LONG open on venue and booked in the DB — consistent   <- no re-adoption
16:09:17 [BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) OBSERVATION_MODE=False
16:09:17 [VPOS-RECONCILE] OPEN vpos=29 LONG entry=74.8 sl=74.9496 age=7.3h — poller continues
16:09:23 [HEARTBEAT] open=1 mode=LIVE
0 tracebacks · 0 executions on the venue since the restart
```

🔶 **A bonus, and worth naming: one of this morning's three fixes just proved itself in flight.**

```
16:09:18 [STOP-MOVE] resync LONG ALREADY AT 74.9496 — venue returned 34040 not-modified;
         the stop is in the requested state, counting as SET (no change was needed)
```

That is the **34040 "not modified"** fix, which the 14:05 report recorded as *"unit-proven, neither
has fired in production"*. It has now fired in production three times, on a real stop, and correctly
counted the venue's idempotent reply as success. In the morning that same reply drove two emergency
closes.

---

## STATE

```
mercury-sol   active   pid 3533821 / worker 3533987   since 16:08:56   0 tracebacks
venue         LONG 0.9 @ 74.80 · stopLoss 74.95 · openTime 1786179014459 (unchanged)
              markPrice 76.37 · uPnL +1.413 · curRealisedPnl +0.4853476
              one Untriggered conditional 74.95 qty 0.9 — same orderId since 08:50
              executions since the restart: 0
book          vpos=29 is_paper=0 OPEN, managed, numbers exactly as booked at 15:40
titan         active · HEAD 897850b · git clean · master pid 2538048 from Aug 6 — NOT TOUCHED
```

A small honesty note on one number: `curRealisedPnl` moved 0.49222 → 0.4853476 since the 15:48
report. That is **−0.0068724 of funding**, charged by Bybit on the open position. It is not one of
our acts and not a discrepancy.

**Open, recorded, not answered:** whether `MIN_PROFIT_DISTANCE_PCT` (and therefore the breakeven
target, the stop-wall filter and the EQH/EQL gate) should be recalibrated on the true 0.100% taker
rate. That changes entries and exits, so it needs its own decision.
