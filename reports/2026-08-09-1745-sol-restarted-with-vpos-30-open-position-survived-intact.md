# sol-restarted-with-vpos-30-open-position-survived-intact

_2026-08-09 17:45 UTC_

---

# Mercury-SOL RESTARTED with vpos 30 OPEN. **The position survived intact — 37 of 37 fields identical, 0 changed.** All ten pending files are loaded.

**The restart ran at 17:42:35 → 17:42:52. Nothing was lost, nothing was touched on the venue, and
every check asked for passed.**

- 🔴 **THE POSITION IS UNCHANGED — field by field.** 37 fields compared against the pre-restart
  snapshot: **37 identical, 0 changed**, plus the two new funding columns. `water_mark` is still
  **77.50**, `mgmt_state_json` still `{"breakeven_applied": true, "partial_done": true}`. **The
  trail did NOT re-arm from scratch and breakeven was NOT lost.**
- 🔴 **The venue stop was never touched.** Same orderId `46968bbe…`, same trigger 76.44, same qty
  0.9, and — the decisive field — **the same `updatedTime` 1786290015787**, which still points at
  the 15:40 partial. The restart wrote nothing to it.
- **Boot adopted it as MANAGED, not as an orphan:** `[BOOT-ASSERT] LONG open on venue and booked in
  the DB — consistent`. No naked-position alert was written; still 5 rows, all resolved.
- **The migration ran:** `funding_paid` and `funding_source` exist, both NULL on vpos 30 — correct,
  since funding is booked at close.
- **`recvWindow` reads 20000 on BOTH clients**, `acknowledged` survived on the ISO client, and the
  funding reader returns **$0.02352016** for vpos 30 against the live venue.
- **Zero tracebacks. Four boot gates. Titan untouched.**

**The rule override was sound and the record now shows why:** the boot took the *managed* branch at
every one of the four gates, and the one that could have destroyed the stop —
`[SMART-CLEANUP] Skipping stop cancel — position still open on exchange` — refused by design.

Prior: [17:30 — the ten pending files](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1730-sol-blind-ticks-closed-and-funding-booked-from-the-venue.md)

---

## BEFORE — the snapshot, taken at 17:40:48

### (a) The exact state, recorded so it could be compared rather than remembered

**vpos 30, all 37 fields** (written to `before_vpos30.json` for machine comparison, not eyeballed):

```
size                0.9              partial_size        0.4
initial_fill_price  76.29            partial_price       77.25
sl_price            76.44258         partial_pnl         0.32258399999999754
original_sl_price   75.41            partial_fees        0.061416000000000005
atr                 0.35359018…      partial_at          2026-08-09T15:40:16.775532+00:00
trail_pct           0.865            recheck_status      done
water_mark          77.5             entry_adx_1h        53.19980888141308
max_adverse_price   75.73            entry_adx_1h_window 200
initial_risk_usdt   1.1440000000000126                   entry_wall_baseline_mult 6.5
opened_at           2026-08-08T21:10:20.117232+00:00     is_paper 0   status open

mgmt_state_json  {"breakeven_applied": true, "partial_done": true}
fills_json       [{"price":76.29,"size":0.9,"fee":0.068661,"kind":"entry",…},
                  {"price":77.25,"size":0.4,"kind":"partial","realised_fee":0.061416,
                   "realised_pnl":0.322584,"price_source":"venue_fill",
                   "fee_rate":0.001,"fee_rate_source":"venue"}]
```

**The venue:**

```
POSITION idx=1 Buy size=0.9 avg=76.29 stopLoss=76.44 mark=77.262 uPnL=+0.8748
               curRealisedPnl=0.23040284 leverage=5 tradeMode=0 (cross)

CONDITIONAL ORDER
  id 46968bbe-3bef-4ae6-a52d-6a0b11882f9d  Untriggered
  type=Market  stopOrderType=StopLoss  trigger=76.44  qty=0.9  reduceOnly=True  idx=1
  createdTime 1786223419195   updatedTime 1786290015787
```

### (b) The stop is POSITION-LEVEL and survives the process

**orderId `46968bbe-3bef-4ae6-a52d-6a0b11882f9d`.**

It is the venue's materialisation of the **position-level `stopLoss` attribute** (`tpslMode='Full'`,
set through `set_trading_stop`), which is why it appears both as `sl=76.44` on the position object
and as an untriggered conditional order. It lives on Bybit's side, not in our process — killing the
worker cannot cancel it.

**Two independent guarantees, both verified in the code before I touched anything:**

1. `_smart_boot_cleanup` cancels stops **only when the exchange reports FLAT**, and returns early
   otherwise.
2. Even if it ran, it cancels with `orderFilter=StopOrder`, which targets **conditional orders** —
   and after B1 the engine's stop is a position attribute, so that call cannot clear it.

`createdTime` 2026-08-08 21:10:19.195 — the original, never cancelled and recreated.
`updatedTime` 2026-08-09 15:40:15.787 — the partial reducing qty 1.3→0.9 and the BE lock moving
75.41→76.44. **That timestamp is the fingerprint used in (f) below.**

### (c) 🔴 NOTHING WAS MID-FLIGHT — checked, not assumed

```
exit_pending table            EMPTY            -> no exit armed, nothing about to fire
partial                       partial_at set, mgmt partial_done=true
                                               -> fired at 15:40 and settled; not pending
entry in flight               no [QTY] entry.live, no [ENTRY-GATE], no order placement
                                 in the journal window
close in flight               no [CLOSE], no ARMED_EXIT_CLOSE, no _execute_close_position
open rows                     exactly ONE (vpos 30)
last trades row               17080 @ 17:35:02 — context_recorded, not an entry
```

The only thing the journal showed in the minutes before the restart was the known
`STOP-VERIFY → 34040` resync loop, every ~12 s. 🔶 **Considered and judged safe rather than
ignored:** if the restart landed during one of those calls, the in-flight request is a
`set_trading_stop` to a value the venue is *already at* — which returns `34040 not-modified`, is
idempotent, and has now done so 699+ times. It is a no-op write, not a state change. **That is the
only class of in-flight call this restart could have interrupted, and interrupting it changes
nothing.**

---

## THE RESTART

```
17:42:35  restart issued (rc=0)
17:42:35  [STOP-MOVE] resync … 34040 not-modified          <- last act of the old worker
17:42:35  Handling signal: term
17:42:35  Worker exiting (pid: 3533987)
17:42:37  Shutting down: Master
17:42:38  Deactivated successfully  (consumed 1h37m CPU, 401.9M peak)
17:42:38  Started mercury-sol.service
17:42:50  [SMART-CLEANUP] Skipping stop cancel — position still open on exchange   ✅
17:42:51  [AP] Restored LONG SOL/USDT:USDT from DB (entry=2026-08-08T21:10:22)     ✅
17:42:51  [BOOT] taker fee: 0.001 (0.1000%) source=venue
17:42:52  [BOOT-ASSERT] LONG open on venue and booked in the DB — consistent       ✅
17:42:52  [BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R)
                  ATR_TF=1h OBSERVATION_MODE=False [pid 4037550]                   ✅
17:42:52  live adapter registered (close/partial/move_stop/pos_state/book_close/funding=yes) ✅
17:42:52  [VPOS-RECONCILE] OPEN vpos=30 LONG entry=76.29 sl=76.44258 age=20.5h
                  — poller continues managing it (no auto-close)                   ✅
17:42:56  [HEARTBEAT] alive ticks=1 open=1 mode=LIVE pid=4037550
```

**Downtime: 3 seconds of process (17:42:35 → 17:42:38), 17 seconds to a managing poller.** The
position was stopped on the venue throughout — the stop never depended on the process.

### (d) The migration ran

```
funding_paid     exists=True    value=None
funding_source   exists=True    value=None
```

Both columns added additively. **NULL on vpos 30 is correct** — funding is read and booked at close,
and this position is open. It places vpos 30 on the pre-fix side of the boundary recorded at 17:30.

### (e) 🔴 THE POSITION SURVIVED — 37 of 37 FIELDS IDENTICAL, 0 CHANGED

Compared programmatically against the JSON snapshot, not by reading:

```
identical fields : 37
CHANGED          : 0
new columns      : ['funding_paid', 'funding_source']
```

The ones that would have mattered most, each verified individually:

| field | value after | |
|---|---|---|
| `size` | 0.9 | ✅ |
| `initial_fill_price` | 76.29 | ✅ |
| `sl_price` | **76.44258** | ✅ |
| **`water_mark`** | **77.50** | ✅ **NOT reset** |
| **`mgmt_state_json`** | `{"breakeven_applied": true, "partial_done": true}` | ✅ **both flags kept** |
| `fills_json` | entry + partial, incl. `price_source: venue_fill`, `fee_rate_source: venue` | ✅ byte-identical |
| `partial_size` / `_price` / `_pnl` / `_fees` / `_at` | 0.4 / 77.25 / 0.322584 / 0.061416 / 15:40:16 | ✅ |
| `max_adverse_price` | 75.73 | ✅ |
| `status` / `is_paper` | open / 0 | ✅ |

🔴 **This is the answer to the question that mattered: the water mark did NOT reset and
`breakeven_applied` was NOT lost.** Had either gone, the trail would have re-armed from scratch —
it would have needed a fresh +1R from 76.29 (i.e. 77.174) before locking anything, and the
breakeven stop at 76.44258 would have been re-derived instead of kept. Neither happened. The
position picked up exactly where it was, because `virtual_positions` is the ledger and the poller
re-reads it rather than reconstructing state.

The trail's own arithmetic is unchanged and still live:

```
water_mark 77.50 · trail_pct 0.865%  ->  trail trigger 76.8296
BE stop (the resting venue stop)      ->  76.44258  (venue tick 76.44)
mark at the time of writing           ->  77.28
```

### (f) The venue's conditional order was NOT touched

| | BEFORE (17:40) | AFTER (17:47) | |
|---|---|---|---|
| orderId | `46968bbe-3bef-4ae6-a52d-6a0b11882f9d` | **identical** | ✅ |
| qty | 0.9 | 0.9 | ✅ |
| trigger | 76.44 | 76.44 | ✅ |
| status | Untriggered | Untriggered | ✅ |
| createdTime | 1786223419195 | 1786223419195 | ✅ |
| **updatedTime** | **1786290015787** | **1786290015787** | ✅ **unchanged** |
| position size / avg / sl | 0.9 / 76.29 / 76.44 | 0.9 / 76.29 / 76.44 | ✅ |

**`updatedTime` is the decisive one.** It still points at 2026-08-09 15:40:15.787 — the partial. If
the restart had rewritten the stop it would carry a 17:42 timestamp. It does not: **the restart made
no write to the protective order at all.**

### (g) Adopted as managed, no orphan, no alert

```
[BOOT-ASSERT] LONG open on venue and booked in the DB — consistent
```

Not `🔴 ORPHAN`, which is what the same assert printed on 2026-08-08 15:40:43 when the venue held a
position with no row. The predicate is
`SELECT position_side FROM virtual_positions WHERE symbol=? AND status='open' AND COALESCE(is_paper,1)=0`
— vpos 30 matches on all three, so the orphan branch was never entered. **This was the operator's
distinction and the boot log states it in its own words.**

```
naked_position_alerts: 5 rows, all resolved=1, newest still 2026-08-08T15:40:43
unresolved: 0        -> nothing was written by this restart
```

---

## AFTER

### (h) The boot geometry line, verbatim

```
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R)
                    ATR_TF=1h OBSERVATION_MODE=False [pid 4037550]
```

**`OBSERVATION_MODE=False`** — live, as it must be. All three geometry constants are the expected
values. Also on the boot path: `[BOOT] taker fee: 0.001 (0.1000%) source=venue | geometry constant
BYBIT_TAKER_FEE_RATE=0.00055 is unchanged and separate` — the fee is read from the venue and the
geometry constant is untouched, exactly as the 2026-08-08 fix specified.

### (i) `recvWindow` = 20000 on BOTH clients, `acknowledged` intact

Both files predate the process start (`main.py` 17:28:26, `tor_retry.py` 17:16:42, worker booted
17:42:52), so what is on disk **is** what was loaded.

```
ISO client — tor_retry.iso_exchange(), THE REAL FUNCTION the worker calls on every Tor retry:
   recvWindow                20000        ✅
   fetchOrder.acknowledged   True         ✅  survived, not clobbered
   adjustForTimeDifference   False        ✅  ccxt's own default; we never set it

PRIMARY client — constructed from the prod main.py source verbatim:
   recvWindow                20000        ✅
   fetchOrder.acknowledged   True         ✅
   adjustForTimeDifference   False        ✅
   ccxt default, for comparison           5000
```

**Since the restart: 0 × `10002`, 0 × `POS-UNKNOWN`.** That is not yet proof the fix works — the
same was true for the ninety minutes before it — but the window is now 4× wider than the 7,463 ms
worst case ever observed.

### (j) The engine is ticking and evaluating vpos 30

```
[HEARTBEAT] alive ticks=25 (+24 in 303s) last_tick=12.7s max_tick=13.2s
            cadence=10s open=1 mode=LIVE pid=4037550
```

**`open=1`, `mode=LIVE`, ~12.7 s cadence — steady.** And the position is genuinely being evaluated,
not merely counted: **26 `STOP-VERIFY vpos=30` cycles** since the restart, each one a real read of
the venue position followed by a stop comparison. That is the trail and breakeven path executing
against vpos 30 on every tick.

Exactly one worker was booted and it is still the same one:

```
[4037550] Booting worker with pid: 4037550        (one occurrence)
poller started in pid 4037550 (interval=10s)      (one occurrence)
master 4037477 / worker 4037550 — both alive, uptime 396 s, NRestarts=0
```

### (k) 🔴 THE FUNDING PATH, PROVEN END TO END BEFORE IT MATTERS

Run against the **live venue**, from the same `main.py` the worker loaded:

```
[FUNDING] venue reports 3 funding record(s) since 1786223420117: total 0.02352016 (positive = paid)
RETURNED: 0.02352016
```

**$0.02352016 — the three stamps vpos 30 has crossed (00:00, 08:00 and 16:00 UTC), the last of them
charged on the reduced 0.9 size.** The read works, the query is bounded by the position's own
`opened_at`, and the number matches the venue's execution records.

**It is NOT booked yet, and that is correct** — `funding_paid` is written at close. `funding_source`
is NULL on vpos 30, which is exactly the boundary marker: this position opened before the fix and
will close with `funding_source` set only if it is still open at close time under the new code —
which it now is. **So vpos 30 will be the first position in this book to carry a funding figure.**

🔶 **Honest limit on this proof:** the function was executed from the same source file the worker
loaded, in a separate process — not inside the worker itself. The worker only calls it at close, so
triggering it in-process would mean closing the position. This is the strongest check available
without doing that.

### (l) Zero tracebacks, four boot gates, Titan untouched

```
tracebacks since the restart : 0
boot gates                   : SMART-CLEANUP ✅  AP-restore ✅  BOOT-ASSERT ✅  VPOS-RECONCILE ✅
unresolved alerts            : 0
cron entries (resolver 08:19, digest 08:20) : both present, untouched
```

```
titan   active · pid 2538048 · NRestarts=0 · up since 2026-08-06 01:53:19 (unchanged)
        HEAD 897850b · git clean (0 porcelain lines) · NOT TOUCHED
```

🔴 **A correction to my own reading, recorded because it nearly went into this report as a
finding.** A `pgrep` showed an unexpected worker pid and I began investigating a worker respawn —
it was **my own `pgrep` subshell matching its own command line**. The journal settles it: exactly
one `Booting worker`, one `poller started`, and `ps` shows master and worker with 393 s / 379 s
uptime. There was no respawn. Checked before reporting rather than after.

---

## THE PENDING SET IS EMPTY

```
$ find . -name "*.py" -newer <process start 17:42:52>
  (nothing)
```

**All ten files are loaded.** Every fix from today is now running:

| | |
|---|---|
| `main.py` 17:28 | close card linked to the position · `exchange_UNKNOWN` → who-acted reason · book facts on the entry card · **recvWindow** · **funding reader** · funding columns |
| `virtual_trader.py` 17:21 | LIVE/paper close-card labels · per-book cumulative · **funding booked into `net_pnl`** |
| `tor_retry.py` 17:16 | **recvWindow on the ISO retry client** |
| `optimizer.py` 16:48 | comment only |
| `config.py`, `claude_advisor.py`, `skip_attribution.py`, `trail_arm.py` (08-08) | the comment-only set that had waited since yesterday |
| `silence_digest_sol.py`, `naked_alert_resolver.py` | standalone cron — were already effective |

---

## STATE

```
mercury-sol   active · master 4037477 / worker 4037550 · since 2026-08-09 17:42:38 · NRestarts=0
vpos 30       OPEN · 0.9 @ 76.29 · sl 76.44258 · wm 77.50 · is_paper=0
              mgmt {"breakeven_applied": true, "partial_done": true}
              37/37 fields IDENTICAL to the pre-restart snapshot
              funding_paid NULL · funding_source NULL (booked at close; venue currently owes
              $0.02352016 against it)
venue         LONG 0.9 · stop 76.44 · order 46968bbe, updatedTime UNCHANGED · SHORT flat
alerts        5 of 5 resolved · 0 unresolved · none written by the restart
pending       EMPTY — every file loaded
titan         active · pid 2538048 · NRestarts=0 · HEAD 897850b · git clean · NOT TOUCHED
```

🔶 **One cosmetic defect still running, unchanged and out of today's scope:** the
`STOP-VERIFY → 34040` loop fires every ~12 s because the intended stop is 76.44258 and the venue
holds it at tick 76.44. It is harmless and idempotent, but it costs two venue calls per tick
forever. Named in the 15:40 report, still open, still not fixed.
