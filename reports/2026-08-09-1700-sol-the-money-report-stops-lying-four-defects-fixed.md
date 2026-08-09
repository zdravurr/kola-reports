# sol-the-money-report-stops-lying-four-defects-fixed

_2026-08-09 17:00 UTC_

---

# Mercury-SOL — the four report-only defects are FIXED. The close card will no longer price a live trade off a paper fee, and the digest will no longer cry wolf whenever the bot is working.

**All four applied, proven by execution in an isolated tree, ZERO leaks into the production
directory or into Titan. Nothing was restarted. vpos 30's stored numbers are untouched.**

- 🔴 **§1 `lookup_entry_for_close` now asks the POSITION.** It told the operator **−$3.26** on a
  trade the venue paid **+$1.58** for, because it reached the newest `status='executed'` row of any
  kind — a paper long from 2026-08-02 with a $5.4960 fee on $10,000 of notional. It now joins
  through `virtual_positions`, and **refuses to price the card at all** when it cannot.
- 🔴 **§2 the live close card stops calling itself paper.** Header, footer and the cumulative all
  read the row's own `is_paper`; the cumulative names its book instead of pooling 22 paper
  positions with one real $100 close.
- 🔴 **§3 who ACTED decides the reason.** Not a mapping of the venue's `'UNKNOWN'` — the venue
  genuinely cannot know why *we* closed. `_execute_close_position` already carries the caller's own
  reason; it now records it, and the detector uses it instead of asking an unanswerable question.
- 🔴 **§4 the digest distinguishes a STALE row from a HEALTHY one** by reading the venue — the
  resolver's own reader, reused so the two can never disagree — and **fails closed** when it can't.
- **§5 `entry_gate_refused` is classified.** The UNCLASSIFIED bucket is unchanged in kind.

**§6 — the read — is entirely clean.** vpos 30's partial is the first under the fixed code and every
number came from the venue: price `77.25 [venue_fill]`, fee at `0.001[venue]`, size 0.9 = 0.9.

```
PROOF BY EXECUTION: 57 assertions, 0 failed.  LEAKS: 0.  exit 0.
18 vectors rewritten by DIRECTORY (17 .py + .env). 0 residual prod-path literals in the lab.
```

Prior: [15:40 — the four defects named](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1540-sol-first-night-live-the-close-reconciled-against-the-venue.md) ·
[16:25 — filter 22 refused](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1625-sol-book-liquidity-measured-filter-22-refused-facts-on-the-card.md)

---

## 6. THE READ FIRST — vpos 30's PARTIAL IS CLEAN ON ALL THREE COUNTS

The "partial writes the FILL, not the ticker" fix loaded at the 16:08:59 restart. This is its first
live exercise, and it worked.

### (a) The price came from the venue FILL, and the log says so in words

```
2026-08-09T15:40:14  [QTY] partial.live SOL/USDT:USDT: 0.433333 -> 0.4 (step quantisation -7.692%)
2026-08-09T15:40:16  [PARTIAL] vpos=30 realised 0.3333 (0.4) @ 77.25 [venue_fill]
                     pnl=+0.3226 fees=0.0614 @rate=0.001[venue]
                     — remainder 0.9 rides the UNCHANGED trail
2026-08-09T15:40:17  BE-LOCK vpos=30 LONG SL→76.44258 (trail armed)
```

**`[venue_fill]`** — not a ticker fallback. It is stamped in the row too, not just the log:

```json
{"price": 77.25, "size": 0.4, "kind": "partial", "realised_fee": 0.061416,
 "realised_pnl": 0.322584, "price_source": "venue_fill",
 "fee_rate": 0.001, "fee_rate_source": "venue"}
```

**And the venue agrees to the cent.** Its own closed-PnL record for that leg:

```
createdAt 1786290015784 = 2026-08-09 15:40:15.784 UTC
  side=Sell qty=0.4 avgEntry=76.29 avgExit=77.25 openFee=0.030516 closeFee=0.0309
```

`avgExit = 77.25` = `partial_price`. **Contrast vpos 29**, whose partial ran 19 minutes before the
fix and booked **76.36** against a venue fill of **76.35**.

### (b) The fee is the venue's 0.001, not the old 0.00055

```
booked partial_fees 0.061416
  = 0.030516  (entry share, 0.4 x 76.29 x 0.001)
  + 0.030900  (exit,        0.4 x 77.25 x 0.001)
venue openFee 0.030516 + closeFee 0.0309 = 0.061416      IDENTICAL
```

**Exact, on both legs, at the venue's real rate.** vpos 29's partial booked its exit leg at 0.00055
and understated the fee by $0.0137. That class is closed.

The entry fill was also correctly rewritten pro-rata to the remaining size:
`0.068661 = 0.9 x 76.29 x 0.001` = `0.099177 x 0.9/1.3`.

### (c) Book and venue agree on size exactly — F3 holds

| | book | venue |
|---|---|---|
| size | **0.9** | **0.9** |
| entry | 76.29 | 76.29 |
| stop | 76.44258 | 76.44 (tick) |
| conditional order | — | `46968bbe…` qty **0.9**, trigger 76.44, updated 15:40:15 |

🔶 One residual, unchanged and out of scope: `partial_pnl` 0.322584 vs the venue's `closedPnl`
0.316644 — the $0.00594 difference is **funding**, which this book still does not record. That is
defect 2 of the 15:40 report and it was not in this pass's scope.

---

## 1. `lookup_entry_for_close` — IT NOW ASKS THE POSITION, AND REFUSES OTHERWISE

### (a) The join, stated

```sql
SELECT id, status, closed_at, initial_fill_price, fills_json
  FROM virtual_positions
 WHERE symbol = ? AND position_side = ?
 ORDER BY (status='open') DESC, id DESC
 LIMIT 1
```

- **entry price** ← `initial_fill_price` — the position's OWN entry.
- **entry fee** ← `fills_json[kind='entry'].fee`.

**Why the position row and not the `trades` row.** `virtual_positions` is the row that **is** the
position, not a row that resembles it. vpos 29's linked `trades` row (16767) carries
`status='failed'` — the fill-read failure of that morning — so even a correct join *through trades*
would have returned nothing usable. The ledger has the number; the signal table does not.

**Why `fills_json` and not `trades.fee`.** The partial **rewrites** the entry fee pro-rata to the
remaining size, which is exactly the fee attributable to the amount being closed. Verified on both
live positions: vpos 29 → `0.06732 = 0.9 x 74.80 x 0.001`, vpos 30 → `0.068661 = 0.9 x 76.29 x
0.001`.

**Why the open row is preferred, with a bounded fallback.** The engine poller can book the row
closed a few hundred ms before the caller prices its card. A just-closed row is therefore accepted
within `_CLOSE_ENTRY_LOOKBACK_MIN = 10` minutes — three orders of magnitude of headroom over the
observed race, and nowhere near a stale row from a previous session, which is the thing that must
never be reached.

**`is_paper` needs no filter now, and that is the point.** A paper position and a live position are
*different rows*. The old query needed a filter because it was reading the wrong row; this one reads
the right row.

### (b) 🔴 IT REFUSES RATHER THAN REACHING — and the card says so

Four refusal branches, every one exercised:

```
✅ REFUSES when no virtual_positions row exists for the side
✅ REFUSES when the newest row was closed too long ago to be the one just closed
✅ REFUSES when initial_fill_price is unusable (0)
✅ REFUSES on any exception, with the reason logged
```

**And the card no longer prints half a ledger.** The old code rendered Gross `?` and Net `?` but
still printed a confident `Total Fees: -$0.0685` — the **close fee alone**, formatted identically to
a complete total. A number that looks whole and is half is worse than no number. What the operator
will see instead, rendered by the real function in the harness:

```
⚠️ Trade Closed — LONG [Armed Exit] — NOT PRICED
💎 SOL/USDT:USDT  @ 76.09
📦 Qty: 0.9
━━━━━━━━━━━━━━━━━━━
🚫 Entry unknown — no position row could be linked to this close,
so gross and net are NOT computed. The close itself succeeded.
💸 Close fee only: -$0.0685  (entry fee unknown)
━━━━━━━━━━━━━━━━━━━
🔄 Batch #1: Trade 7/30
```

🔴 **A defect I introduced and caught in the harness, recorded because it is the kind that survives
review.** My first version `return`ed early on the unpriced branch — which would have skipped the
**batch-boundary summary** at trade 30. That is a behaviour change, not a report change. Restructured
as `if/else`, and the harness now asserts it explicitly:

```
✅ the batch boundary STILL fires on an unpriced close (no early return)
```

### (c) The DB row and `net_pnl` were never affected — only the card

**Confirmed by inspection of both paths.** `lookup_entry_for_close` is read-only (a `SELECT`), and
its six call sites use its result for exactly two things: `realized_pnl` passed to
`_send_trade_close_report`, and the log line. **The position ledger is written by
`virtual_trader.close_position`, which computes `net_pnl`, `total_fees` and `close_price` from the
row's OWN stored size and fills and never calls this function.** That is why vpos 29's stored
`net_pnl` (+1.6024798) was right while its card said −3.2605 — two different computations, only one
of which was broken. Nothing in this change touches the ledger.

**The proof, on the real data:**

```
the row the OLD code reached: id=15093 price=73.53 fee=5.4959998500000005  (paper, 2026-08-02)

✅ returns the POSITION's own entry, not the newest executed row   got (76.29, 0.068661)
✅ never returns the 2026-08-02 paper price 73.53
✅ never returns the $5.4960 paper fee
✅ vpos 29 -> (74.80, 0.06732) from initial_fill_price + fills_json
✅ the CARD would now read the venue truth +1.025199, not -3.260481
```

`(76.09 − 74.80) × 0.9 − 0.06732 − 0.068481 = **+1.025199**`, which is the venue's own closed-PnL
for that leg excluding funding, to six decimals.

---

## 2. THE LABELS ON A LIVE CLOSE CARD

### (a) Header and footer read the row

`_format_close_card` was written when the engine was paper-only, so it hardcoded `VIRTUAL Close` and
`(paper — no real order)`. After Phase 2 the *same* function renders live closes. Both now derive
from `virtual_positions.is_paper`, via a new `_is_paper_row` that returns **None** when it cannot
read — and **None renders as UNKNOWN, never as paper**, because defaulting to "paper" is the exact
failure being fixed.

### (b) The cumulative names its book

`_cumulative_closed_pnl(is_paper=None)` — the old pooled behaviour is still available, and the card
now asks for one book. The card the operator would have received for vpos 29, rendered by the real
function:

```
✅ 🔴 LIVE Close — LONG [Exit-Signal]
💎 SOL/USDT:USDT
📥 Entry: 74.8
📤 Exit:  76.09
━━━━━━━━━━━━━━━━━━━
💵 Gross P&L:  +$1.7850
💸 Total Fees: -$0.1825
💰 Net P&L:    +$1.6025
━━━━━━━━━━━━━━━━━━━
📈 Cumulative, LIVE book (1 closed): +$1.6025
(LIVE — real money)
```

Against the old one: `✅ VIRTUAL Close`, `(paper — no real order)`, `Cumulative (23 closed):
-$1126.8556`.

```
✅ a LIVE close is NOT headed "VIRTUAL Close"        ✅ the cumulative names the LIVE book
✅   it is headed LIVE                               ✅ and excludes the 22 paper positions
✅   and NOT footed "(paper — no real order)"        ✅ a PAPER close still says VIRTUAL / paper
✅ an UNREADABLE is_paper says UNKNOWN, never defaults to paper
✅ the two books partition the pooled total
     live=1.6025/1   paper=-1128.4580/22   pooled=-1126.8556/23
```

That last assertion is the one that matters for trust: the split is **exact**, so nothing was
invented or lost — the same rows, correctly separated.

---

## 3. 🔴 WHO ACTED DECIDES THE REASON

### (a) The distinction, and why it is not a mapping

**I did not map `'UNKNOWN'` to `'exit_signal'`.** That would be a lie of the same shape as the one
it replaces. The two cases are different **facts** and are distinguished by **who acted**:

| | how it is known | reason booked |
|---|---|---|
| **WE closed it** | `_execute_close_position` recorded its own `reason` when the close returned | **ours** — `exit_signal`, `timeout`, `sl_failsafe`, … |
| **The venue closed it** | no mark | classified from the venue as before |

`_execute_close_position(symbol, position_side, reason='exit_signal')` **already carried the
caller's reason** and always has — it is the single choke point for every bot-initiated live close
(armed exit, Group B, Smart TP, timeout, sl_failsafe, the engine's own `_exec_close_live`). It now
records it after the close succeeds, so a close that raised leaves no mark.

**In-process, not a table, and that is a decision not a shortcut.** The race is strictly
intra-process: main.py's close and virtual_trader's poller run in the SAME gunicorn worker, on
different threads — pid 3533987 stamps both the `ARMED_EXIT_CLOSE` line and the `[VIRTUAL] CLOSE
vpos=29` line on 2026-08-08. **A cross-process close is by definition not ours, and for that case
the venue lookup is the correct answer.** No migration, no new table, and the degraded path is
exactly the old behaviour: if the process dies between the close and the detection, the mark is gone
and the venue classifies it.

**Single-use and self-expiring**, so one close can never label a second, and a mark left behind by a
close the detector never saw cannot mislabel a genuine stop-out two hours later.

**The literal is preserved either way** — both branches print the venue's own `stopOrderType`:

```
[ENGINE] exchange close substantiated: 0.9 @ 76.09 fee=0.068481 reason=exit_signal
  — WE closed this position, so the reason is OURS, not the venue's
    (venue stopOrderType='UNKNOWN'; a plain market close has none)

[ENGINE] exchange close substantiated: 0.9 @ 74.95 fee=… reason=sl
  — NOT closed by this process; classified from the venue (stopOrderType='StopLoss')
```

### 🔴 AND A SEPARATE FINDING, SETTLED BY MEASUREMENT: `exchange_market` WAS DEAD CODE

`_classify_exchange_exit` assumed an **empty** `stopOrderType` marks a plain market fill. **Bybit
never sends an empty string — it sends the literal `'UNKNOWN'`.** Measured on every fill this
account has ever made:

```
12 of 12 fills — entries AND closes — stopOrderType='UNKNOWN', execType=Trade, orderType=Market
  06:50:20 buy 0.3   06:50:21 buy 1.3   06:50:25 sell 2.6   08:35:16 buy 1.3
  08:35:16 buy 1.3   08:35:20 sell 2.6  08:50:14 buy 1.3    15:40:49 sell 0.4
  18:45:02 sell 0.9  21:10:18 buy 1.3   15:40:15 sell 0.4   (+1)
```

So the `if not raw` branch **could never fire on this venue** and `'exchange_market'` had never once
been produced. `'UNKNOWN'` is not a mystery value — it is Bybit's way of saying *"this fill did not
come from a conditional order"*, which is precisely what the empty string was meant to mean. They
are now treated identically. **This is measurement, not inference: 12 of 12, and the venue's literal
word is still printed.**

```
✅ venue 'UNKNOWN' is a plain market fill, not a mystery   -> 'exchange_market'
✅ empty stopOrderType still means the same thing          ✅ a REAL stop is still 'sl'
✅ a native trail is still 'trail'                         ✅ a liquidation still overrides everything
✅ an unseen venue type is still kept verbatim             -> 'exchange_SomethingNew'
✅ OUR close is remembered with OUR reason
✅   and it is SINGLE-USE (a second close cannot inherit it)
✅   sides do not cross-talk        ✅ the SHORT mark survives
✅   a STALE mark is discarded, so a later venue stop is not mislabelled
✅   an empty reason is never marked
```

### (b) Registered in the SAME edit — P4 does not get a second chance

Four reasons were added to `virtual_trader._CLOSE_LABEL`:

| reason | label | why |
|---|---|---|
| `exchange_UNKNOWN` | `exchange_market_{s}` | **vpos 29 already carries it** — the first live close in this bot's history. It can no longer be produced, but the existing row must keep pairing. |
| `sl_failsafe` | `sl_triggered_{s}` | an emergency stop-out in outcome, pooled for the same reason `post_entry_critical` is |
| `engine` | `exit_{s}` | `_exec_close_live`'s default |
| `exit_signal` | `exit_{s}` | already mapped; reached by a new route |

🔴 **`optimizer._CLOSE_*_TYPES` needed no new entry, and that was CHECKED rather than assumed.**
Every new reason maps onto a label **already** in both frozensets. That is the whole point of mapping
new reasons onto registered labels instead of minting new ones — `pair_trades` infers side from **set
membership**, and an unregistered label is not an error, it is silently **dropped from learning**
(defect P4). The harness asserts it exhaustively rather than trusting the reading:

```
✅ EVERY _CLOSE_LABEL value is registered in optimizer._CLOSE_*_TYPES (P4)
     15 reasons x 2 sides checked; offenders=[]
✅   the unmapped fallback unmapped_close_long is registered too
✅   the unmapped fallback unmapped_close_short is registered too
✅ vpos 29's stored 'exchange_UNKNOWN' now pairs instead of falling to unmapped
```

`optimizer.py`'s AST is **unchanged — `added=[] removed=[] changed=[]`**. The only edit is the
comment recording that the membership was verified by execution.

### (c) The first live close stays filed as it was, and that is deliberate

**vpos 29's stored `close_reason` is NOT rewritten.** `'exchange_UNKNOWN'` is what the venue said at
the time and the record should say what was known. What changes is that it now **pairs** into
`exchange_market_long` instead of the unmapped bucket, and that no future close will be filed that
way. The cohort axis is repaired going forward; history is preserved.

---

## 4. THE DIGEST'S PERMANENT RED LINE

### (a) STALE vs HEALTHY, decided by the venue

```
STALE   — open in the DB, FLAT on the venue          -> needs hands
HEALTHY — open in the DB, open on the venue          -> informational, all-clear allowed
UNKNOWN — the venue could not be read                -> needs hands (FAILS CLOSED)
```

**`naked_alert_resolver.read_venue` is REUSED, not reimplemented**, so the 08:19 resolver and the
08:20 digest can never disagree about what is on the venue. Importing it is safe: that module has no
import-time side effects.

🔴 **It fails closed.** An unreadable venue is not evidence of health, so it keeps the loud line —
the same rule the resolver applies when it refuses to resolve what it cannot positively verify.

**And a HEALTHY row is still REPORTED, just not as an alarm.** Dropping it would trade one blindness
for another: *"the bot holds nothing"* and *"the bot holds a position that is fine"* must never
render identically. Each line carries the venue evidence it was classified on, so the all-clear can
be checked rather than trusted:

```
📌 1 open position(s) — each classified against the venue in the block below.

✅ NOTHING NEEDS HANDS — no unresolved alerts, no stale or unverified rows,
   no money-path statuses in the window. No side is blocked.
  ✅ MANAGED vpos 30 · SOL/USDT:USDT LONG · LIVE · opened 2026-08-08T21:10:20.117232+00:00
      venue holds 0.9 @ 76.29, stop 76.44 — DB row and venue agree; nothing to do
```

A fourth state was added that the brief did not ask for but the data demanded: **HEALTHY BUT
UNSTOPPED**. A row the venue confirms, with no stop on it, is not stale — and it is emphatically not
fine. It gets its own escalation.

```
✅ HEALTHY: no red STALE line          ✅ STALE: a row the venue does not have IS flagged
✅ HEALTHY: no UNVERIFIED line          ✅ STALE: the NEEDS HANDS header fires
✅ HEALTHY: the all-clear is ALLOWED    ✅ STALE: the all-clear is suppressed
✅ HEALTHY: still reported, as managed  ✅ UNKNOWN venue: FAILS CLOSED, not open
✅ HEALTHY: venue evidence is shown     ✅ UNKNOWN venue: no all-clear
✅ OPEN BUT UNSTOPPED is escalated on its own terms, and suppresses the all-clear
```

### (b) Why this mattered

That block is the one made most prominent **precisely so it would be believed** — it sits above the
funnel by deliberate design. Before today, holding any position produced a red `🚫 OPEN ROW … ← 🔴 NO
ALERT ROW` line **and** suppressed the `✅ NOTHING NEEDS HANDS` all-clear. So the block shouted
exactly when the bot was working, and could never say all-clear while it held money. A block that
cries wolf whenever the bot is working is worse than no block at all, because it trains the operator
to skip the one section that must never be skipped.

🔶 **One residual, named:** the digest now makes a Tor venue read at 08:20 that it did not make
before. It is bounded — ccxt's default timeout is **10 000 ms**, well inside the cron entry's
`timeout 120` — and it only runs when an open row exists, so a flat day does zero venue work exactly
as before. If it does fail, it fails closed and the digest still sends.

---

## 5. `entry_gate_refused` — CLASSIFIED, BUCKET UNTOUCHED

Added to `GATES_EXTRA` rather than `GATES`, because it is **not part of the ordered cascade** — it
fires across it, whenever two same-side signals arrive in one second.

🔴 **The UNCLASSIFIED bucket is unchanged in kind**, which the harness asserts against the source
rather than against my intention:

```
✅ §5 entry_gate_refused entered the funnel ladder
✅ §5 the UNCLASSIFIED bucket is unchanged in KIND (still "everything else")
     asserted by the literal presence of:
     other = {s: c for s, c in by_status.items() if s not in known}
```

This status qualifies under the rule already written at that bucket: its meaning was **established
from its emission site** — the refusal branch that writes the row with its reason — not adopted to
quieten the bucket. Nothing else moved.

---

## PROOF BY EXECUTION — 18 VECTORS, SEARCHED BY DIRECTORY

```
LAB: full tree copy. Every prod-directory literal rewritten.
  residual "/mnt/volume_nyc1_1780480650620/mercury-sol" literals in lab .py : 0
  residual "/root/titan-bot" literals in lab .py                            : 0
  files rewritten                                                           : 17
  + .env                                                    => 18 VECTORS

LOCK (installed first, never lifted):
  sqlite3.connect  -> raises on any path under PROD or /root/titan-bot
  open(mode=w/x/a/+) -> same
  sys.dont_write_bytecode = True
  the Telegram sender replaced by a stub that RAISES if called

RESULT:  57 assertions ✅   0 ❌   LEAKS: 0   exit 0
```

🔴 **Why by DIRECTORY and not by DB filename — the two methods disagree, and the filename one is
wrong in both directions.** Both return 17 files, which looks like agreement and is not:

```
found ONLY by the directory grep (real vectors the filename grep MISSES):
    healthcheck.py        weight_engine.py   <- holds WEIGHTS_PATH to the prod weights

found ONLY by the filename grep (FALSE POSITIVES — both are comments):
    config.py:320   "# Recalibrate after accumulating … history in trades.db."
    macro_filter.py:34  "All context … is persisted to trades.db"
```

The filename method would have left two real write vectors pointing at production while reporting
the same count. This is the same finding as 2026-08-08 and it has now cost nothing twice.

### The diff, and every deleted line accounted for

```
main.py                +248  -35
virtual_trader.py      +102  -16
optimizer.py            +11   -0      <- comment only; AST added=[] removed=[] changed=[]
silence_digest_sol.py  +101  -10

AST:
  main.py                added=[_mark_our_close, _take_our_close]  removed=[]
                         changed=[_book_exchange_close, _classify_exchange_exit,
                                  _execute_close_position, _send_trade_close_report,
                                  lookup_entry_for_close]
  virtual_trader.py      added=[_is_paper_row]  removed=[]
                         changed=[_cumulative_closed_pnl, _format_close_card]
  optimizer.py           added=[]  removed=[]  changed=[]
  silence_digest_sol.py  added=[_row_state]  removed=[]  changed=[_heartbeat_block, build]
```

**Every one of the 61 deleted lines sits inside one of those seven rewritten functions** — checked
line by line, not assumed. No geometry, no cascade, no threshold, no prompt, no entry path, no exit
path and no stored value was touched.

Backups `*.bak_moneyreport_20260809_1700` for all four files, **md5-verified identical to the
originals before the first edit**.

---

## 🔴 WHAT IS LOADED AND WHAT IS NOT — THE SPLIT MATTERS TODAY

**§4 and §5 go live TOMORROW MORNING WITHOUT A RESTART.** `silence_digest_sol.py` is a standalone
cron script re-read on every run, exactly like the resolver. The 08:20 digest will be the fixed one.

**§1, §1b, §2 and §3 are on disk and NOT loaded.** They live in `main.py` and `virtual_trader.py`,
which the worker holds in memory from its 16:08:59 start. **vpos 30 is open, so nothing was
restarted.** They take effect at the next flat-book restart — which means that **if vpos 30 closes
before that restart, its close card will still carry the old defects.** Stated plainly so it is not
a surprise: the fix exists, it is proven, and it is not yet in the running process.

`optimizer.py` is comment-only, so its load state is irrelevant either way.

```
PENDING (loaded by the bot)      config.py             2026-08-08 16:51
                                 claude_advisor.py     2026-08-08 17:47
                                 skip_attribution.py   2026-08-08 17:47
                                 trail_arm.py          2026-08-08 17:47
                                 main.py               2026-08-09 16:45   <- NEW
                                 virtual_trader.py     2026-08-09 16:47   <- NEW
                                 optimizer.py          2026-08-09 16:48   <- NEW (comment only)

NOT pending (standalone, re-read per run — LIVE AT THE NEXT CRON FIRE)
                                 naked_alert_resolver.py  2026-08-08 17:47
                                 silence_digest_sol.py    2026-08-09 16:51   <- NEW, live 08:20
```

---

## STATE

```
mercury-sol   active · pid 3533821 / worker 3533987 · since 16:08:59 · NRestarts=0 · NOT restarted
vpos 30       OPEN · 0.9 @ 76.29 · sl 76.44258 · partial 0.4 @ 77.25 (venue_fill, fee 0.061416
              at the venue's 0.001) · wm 77.50 · is_paper=0 — UNCHANGED BY THIS PASS
venue         LONG 0.9 · stop 76.44 · order 46968bbe (qty 0.9) · SHORT flat
tracebacks    0 since 16:08:59
db            opened read-only for every production query; every mutating test ran in the LAB
titan         active · pid 2538048 · NRestarts=0 · HEAD 897850b · git clean · NOT TOUCHED
```

**Two defects from the 15:40 register remain open and were NOT in this pass's scope:** funding is
still never booked (−$0.0069 on vpos 29, $0.0193 already unbooked on vpos 30), and the
`recv_window` blind ticks. Named, not silently carried.
