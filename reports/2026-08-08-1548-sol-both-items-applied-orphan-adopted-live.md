# sol-both-items-applied-orphan-adopted-live

_2026-08-08 15:48 UTC_

---

# Mercury-SOL — BOTH ITEMS APPLIED. The orphan is adopted and managed. Both acts confirmed BY THE VENUE.

**Item 2 live at 15:37:06. Item 3 live at 15:40:22. The orphan is `vpos=29`, `is_paper=0`.
The stop moved 73.89 → 74.95 and 0.4 SOL sold @ 76.35 — both confirmed by reading Bybit, not by
reading our log. Neither act failed. Titan untouched.**

**One thing did not go as the code claimed, and it is the fee finding you told me to record:
the partial's booked PnL is overstated by 0.01774 USDT because the close fee was MODELLED at the
configured 0.055% while the venue charged 0.100%.** Recorded as its own open item, not fixed.

Prior: [diffs approved 15:30](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1530-sol-0850-reasoning-judged-apply-guard-and-adoption-diffs.md)

---

## 0. BACKUPS FIRST — md5-verified before a single byte changed

```
main.py.bak_adoptguard_20260808_153524              ea4f9e23b4881029e8a38cd70b1b5a61
optimizer.py.bak_adoptguard_20260808_153524         4b04775c3c46ce1dbedc84dd0550e061
optimizer_listener.py.bak_adoptguard_20260808_153524 b99087feccc4f51e532641b6c988a6d8
virtual_trader.py.bak_adoptguard_20260808_153524    5d12e5a757336642d9df31f538025713
```

All four md5-compared against the live file at backup time — `OK` on each. `cp -p`, so each
backup carries its source's original mtime.

---

## 1. ITEM 2 APPLIED FIRST, AS ORDERED — and it cannot touch the venue

Installed 15:36:57. Diff against the backup: **`optimizer.py` +51/−0, `optimizer_listener.py`
+60/−0** — exactly the approved diffstat, to the line.

**AST surface, prod vs backup:**

```
optimizer.py          : functions added=['_stamp_live_evidence']  changed=['main']       removed=[]
optimizer_listener.py : functions added=['_live_evidence_ok']     changed=['apply_proposal'] removed=[]
```

Nothing else in either file moved.

**The listener needed a restart** — it is a long-running service, so its in-memory copy was stale
and the guard would have been on disk only. This is the deployment-gap discipline from 2026-08-06.
It places no orders; the venue cannot be reached from it.

```
optimizer_listener.py mtime   2026-08-08 15:36:57
listener process started      2026-08-08 15:37:06   pid 3521920   (9s after the write)
mercury-sol at that moment    pid 3484279, unchanged — the trading bot was NOT restarted here
```

**Behavioural check against the INSTALLED production module:**

```
MIN_LIVE_PAIRS = 8 | optimizer.MIN_PATTERN_SAMPLE = 8 | equal: True
no evidence block                    -> REFUSED
majority-live by rows, paper dollars -> REFUSED
live-dominated on both               -> ALLOWED
optimizer._stamp_live_evidence present: True
```

Item 2 is live and proven in production, not in the lab.

---

## 2. ITEM 3 — RE-DERIVED AGAINST THE VENUE **BEFORE** THE RESTART, AS ORDERED

Installed 15:38:58. **`virtual_trader.py` +268/−15, `main.py` +65/−4** — the approved diffstat.

```
virtual_trader.py : added=['_adopt_card','_adopt_derive','_num','adopt_orphan_position']
                    changed=['book_live_position']            removed=[]
main.py           : added=['_orphan_trades_row_id']
                    changed=['_assert_exchange_matches_db_at_boot']  removed=[]
```

(`_num` is the nested field validator inside `_adopt_derive`.)

### The re-read at 15:39:21, and the derivation run on it

```
VENUE, RE-READ 15:39:21 UTC          DERIVATION (prod virtual_trader._adopt_derive, pure)
  size            1.3                  refusals            NONE
  avgPrice        74.8                 atr                 0.364
  markPrice       76.34   <- MOVED     initial_risk_usdt   1.183
  stopLoss        73.89                trail_cb / trail_pct 0.68 / 0.909%
  openTime        1786179014459        arm_distance        0.910
  curRealisedPnl  -0.09724             ARM price           75.7100
  tpslMode        Full                 breakeven           74.9496
                                       partial raw         0.4333  -> quantised 0.4
                                       entry_fee           0.09724
                                       opened_at           2026-08-08T08:50:14.459+00:00
```

**Every derived number is identical to the 15:30 report** — and that is the point, not a
coincidence: all five inputs to the derivation (`avgPrice`, `stopLoss`, `size`, `openTime`,
`curRealisedPnl`) were unchanged. Only `markPrice` moved, 76.546 → 76.34, and the mark is an input
to *when* the engine acts, not to *what* the levels are. **Mark 76.34 ≥ arm 75.7100 → the acts were
going to fire.** Stated before the restart, not after.

Lot step confirmed from the venue: **0.1**, min 0.1 → the 0.4333 leg quantises to **0.4**,
remainder 0.9.

The trades-row link was checked for ambiguity before the restart: **exactly one** `buy` row within
±120 s of `openTime` → **16767**. Had there been two, the code stores NULL rather than guess.

---

## 3. 🔴 THE CARD vs THE ACTS — YOU ASKED ME TO SAY IT PLAINLY, SO: **NO, THERE IS NO REVIEW WINDOW**

**Ordering is guaranteed. A checkable window is not, and I will not imply one.**

Measured from the journal:

```
15:40:43   BOOT-ASSERT orphan detected
15:40:43   LIVE-BOOK vpos=29 booked   ->  ADOPTION CARD SENT HERE
15:40:43   poller started (interval=10s)
15:40:48   [QTY] partial.live 0.433333 -> 0.4
15:40:49   PARTIAL executed            <- FIRST ACT
15:40:50   BE-LOCK stop moved          <- SECOND ACT
```

**The gap between the card and the first act was ~6 seconds.** The card genuinely precedes both
acts — the send is synchronous inside the boot assert, before the worker's poller has ticked — so
the ordering you asked for holds. But six seconds is not a period in which anyone checks anything
against Bybit.

**A real window is not achievable in this design**, and it is not a tuning problem: adoption runs
inside boot, and the poller starts with the same boot. Getting an actual review window needs a
deliberate pause gate — adopt, alert, and *wait for a CONFIRM tap* before the engine is allowed to
manage the row. That is a different mechanism, you did not ask for it, and I did not add it. If you
want it for the next orphan, say so and it is a small diff.

What the card did buy you: it is in your Telegram, timestamped **before** the orders, with every
level and its formula, so the record of what was intended exists independently of what happened.
`send_tg` prints `TG send failed` on any exception — **0 such lines since the restart**, so the card
was delivered.

---

## 4. WHAT ACTUALLY HAPPENED — read from Bybit, not from our log

### (a) The partial — venue execution record

```
/v5/execution/list :  15:40:49.234   Sell   qty 0.4   @ 76.35   execFee 0.03054   closedSize 0.4
```

One execution. Exactly 0.4, exactly one leg, no partial-of-a-partial, no second order.

### (b) The stop move — venue position and order

```
/v5/position/list  :  stopLoss 73.89 -> 74.95      size 1.3 -> 0.9
/v5/order/realtime :  orderId 671eee37-1308-4efd-9fca-fd3586743e1e
                      Untriggered   triggerPrice 74.95   qty 0.9   positionIdx 1
```

🔴 **Note the orderId: it is the SAME `671eee37` that has been on this position since 08:50:14.**
The stop was **modified in place**, not cancelled and recreated. There is exactly one conditional
order, at the right price, for the right (reduced) size. No orphan stop, no duplicate — which is the
specific failure this bot produced twice this morning.

Bybit rounded the engine's 74.9496 to the 0.01 tick → **74.95**. The row keeps 74.9496; the venue
holds 74.95. That is a 0.0004 difference in the bot's favour and is the normal tick behaviour, not a
discrepancy.

### (c) Neither act failed

No `TG send failed`, no `STOP-MOVE ... FAILED`, no `34040`, no fail-safe, **0 tracebacks** since the
restart. Both acts are reflected on the venue. **There is no half-adopted state.**

### (d) The resulting row

```
id 29 | SOL/USDT:USDT LONG buy | is_paper=0  <- the FIRST is_paper=0 row this book has ever held
size 0.9 (was 1.3)          initial_fill_price 74.8      atr 0.364
sl_price 74.9496            original_sl_price 73.89      initial_risk_usdt 1.183
trail_pct 0.909             water_mark 76.36             max_adverse_price 74.8
opened_at 2026-08-08T08:50:14.459+00:00   <- the VENUE openTime, not the adoption time
trades_entry_row_id 16767   recheck_status 'done'
entry_wall_baseline_mult / entry_adx_1h / entry_adx_1h_window / entry_atr_pct_1h : all NULL
mgmt_state_json {"breakeven_applied": true, "partial_done": true}
partial_size 0.4  partial_price 76.36  partial_pnl 0.57728  partial_fees 0.04672
                  partial_at 2026-08-08T15:40:49.757166+00:00
fills: entry  74.8  size 0.9  fee 0.06732      <- the entry fee correctly reduced to the
                                                  remainder's share: 0.09724 × 0.9/1.3
       partial 76.36 size 0.4 realised_fee 0.04672 realised_pnl 0.57728
```

`recheck_status='done'` is on the row as designed — **the T+300 tier never fired.** Confirmed in the
log: no `RECHECK` line anywhere after the restart. The trap you asked about on instinct stayed shut.

`[VPOS-RECONCILE] OPEN vpos=29 LONG entry=74.8 sl=73.89 **age=6.8h** — poller continues managing it`
— the age proves `opened_at` was stamped from the venue and not from the boot.

Heartbeat now reads **`open=1`** (it was `open=0` all day, because it counts rows).

### (e) Venue state now (15:44:37)

```
size 0.9   avgPrice 74.8   markPrice 76.32   stopLoss 74.95
curRealisedPnl +0.49222    unrealisedPnl +1.368    openTime unchanged
positionIdx 2 size 0       one Untriggered conditional 74.95 qty 0.9
```

**Risk transformed exactly as you said it would:** before adoption the position risked
−$1.183 to its 73.89 stop; it now has **+$0.49222 realised** and a stop at 74.95 that locks a further
**+$0.135** on the remaining 0.9 (0.9 × (74.95 − 74.80)), against **+$1.368** currently unrealised.

---

## 5. 🔴 THE FEE FINDING, NOW PROVEN IN COMBAT — recorded as its own open item, NOT fixed

You told me to record this separately. **This pass produced live evidence for it, on a real fill.**

```
                  price        close fee              partial pnl
BOOKED (row 29)   76.36        0.016797  MODELLED     +0.57728
VENUE (truth)     76.35        0.03054   ACTUAL       +0.55954
                  ^ ticker     ^ 1.82x understated    OVERSTATED by +0.01774 USDT
```

Reconciles exactly against Bybit: `−0.09724 + 0.4 × (76.35 − 74.80) − 0.03054 = 0.49222`, which is
the venue's `curRealisedPnl` to five decimals.

**Two distinct defects in one row, both recorded, neither fixed:**

1. **`BYBIT_TAKER_FEE_RATE = 0.00055` against a venue rate of 0.100% — understated 1.82×.**
   Measured twice today on real money: the entry (0.09724 on 97.24 notional) and now this partial
   (0.03054 on 30.54). The same constant computes **every paper fee** (`virtual_trader.py:233`), so
   the whole paper book's fees are understated by the same factor and **every paper R is
   correspondingly flattered** — which feeds `weight_engine`'s `avg_pnl` and `find_worst_segment`'s
   dollar ranking.
2. **`partial_price` is written from the TICKER, not the fill.** 76.36 stored against a 76.35
   execution. The live fill is readable — the `acknowledged` fix on 2026-08-08 is what opened it —
   so this is now a fixable gap that was previously invisible.

Contribution to the 0.01774: **0.01374 from the fee rate, 0.00400 from the ticker-vs-fill price.**

Filed as its own open item with the measurement. **Not touched in this pass.**

---

## 6. YOUR TWO FLAGS — RECORDED AS INSTRUCTED

1. **`apply_opt_proposal` left unguarded, deliberately.** It is dead behind
   `PARAM_TUNING_ENABLED = False` (`config.py:29`), which forces an early return before any write,
   and **Titan does not guard it either** — guarding it here would be a divergence from parity, not
   an improvement. 🔴 **Recorded with the condition: flipping `PARAM_TUNING_ENABLED` to True
   re-opens the hole**, because that path can append a filter from `worst_segment` without passing
   `_live_evidence_ok`.
2. **Paper mode now refuses every proposal.** The cohort is paper by construction there, so
   `live_pairs = 0` and the `MIN_LIVE_PAIRS` floor refuses. Accepted as correct while real money is
   on the venue; recorded as a known consequence, so a future return to observation mode is a
   decision and not a surprise.

---

## PROOF BY EXECUTION — 17 VECTORS, SEARCHED BY DIRECTORY

Re-confirmed this pass against the current tree:

```
grep -l "mercury-sol/trades.db" *.py            -> 13   (the narrow, insufficient census)
grep -l "<prod directory>"      *.py            -> 16   (the real census)
missed by the filename grep: healthcheck.py, mercury_sol_prior_move_logger.py,
                             weight_engine.py   <- holds WEIGHTS_PATH to production weights
+ .env                                          =  17 VECTORS
```

Every pre-apply test ran in a copied tree with all 17 rewritten (**0 prod-path literals remaining**),
`sys.dont_write_bytecode = True`, and a lock on `sqlite3.connect` **and** write-mode `open()`
asserting against **both** the prod directory and `/root/titan-bot`. Leaks: **0**.

The production run then confirmed it live: `virtual_positions` went from max id 28 to max id 29,
`is_paper=0` rows from 0 to **1** — the lab's id-29 write never reached production, exactly as the
lock reported.

---

## STATE

```
mercury-sol            active   pid 3523302 / worker 3523426   since 15:40:22   NRestarts=0
                       0 tracebacks · HEARTBEAT open=1 mode=LIVE
listener               active   pid 3521920   since 15:37:06   (guard loaded)
optimizer timer        active   next 2026-08-09 14:00 UTC — first run under the new guard
venue                  LONG 0.9 @ 74.80 · stopLoss 74.95 · openTime 1786179014459 (unchanged)
                       curRealisedPnl +0.49222 · uPnL +1.368 · idx2 size 0
                       one Untriggered conditional 74.95 qty 0.9 — same orderId since 08:50
book                   vpos=29 is_paper=0 OPEN, managed, recheck closed, linked to trades 16767
titan                  active · HEAD 897850b · git clean · master pid 2538048 from Aug 6
                       NOT TOUCHED at any point
```

**Both items applied, both proven live, nothing half-done.** The position that spent 6h50m
unmanaged is now on the book, past its +1R, a third realised, and stopped above entry.

**Open, recorded, not fixed:** the 1.82× taker-fee understatement and the ticker-vs-fill
`partial_price` — awaiting your decision as a separate pass.
