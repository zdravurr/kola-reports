# SOL — M6 AND M7 APPLIED · M4: TWO TRAILING MECHANISMS, DECISION REQUIRED

**2026-08-06 13:45 UTC · Mercury-SOL (PAPER, stays PAPER)**

One file changed: `main.py`. Backup `main.py.bak_M6M7_partial_lossstreak_20260806`.
Service restarted **13:39:51**, master 2702530, **0 tracebacks**.
Titan (`/root/titan-bot`, LIVE REAL MONEY): **untouched** — clean, `897850b`, workers 2538048/2538082
running continuously since 01:53.

**M4 is investigated and NOT applied — it needs your decision. M6 and M7 are applied and proven.**

---

# 1. 🔴 M4 — TWO TRAILING MECHANISMS. THE FACTS, THEN THE RECOMMENDATION.

## a) Is the native trailing stop actually set on every entry? **YES — on every live entry.**

One call site, `main.py:2398`, inside `_execute_single_entry`, unconditional once the stop succeeds:

```python
tp_id = _place_trail_with_retry(symbol, market_id, pos_idx, trail_cb, active_price)
```

and the call it makes (`main.py:1842-1851`):

```python
POST /v5/position/trading-stop
  {'category':     'linear',
   'symbol':       market_id,          # 'SOLUSDT'
   'positionIdx':  str(pos_idx),       # 1 LONG / 2 SHORT
   'trailingStop': str(trail_cb),      # ← the distance
   'activePrice':  str(active_price)}  # ← where it arms
```

| what | value | from |
|---|---|---|
| `trail_cb` | `round(TRAIL_MULT_ATR * atr, 2)` = **2.5 × ATR(1h)**, in **price units** | `TRAIL_MULT_ATR = 2.5`, `ATR_TF = '1h'` |
| `active_price` | `fill ± activation_distance(fill, atr)` | `TRAIL_ARM_FIX_ENABLED=True` ⇒ `SL_BUFFER_ATR × atr` = 2.5×ATR = **+1R** |

Retried 3×; on total failure it only warns — deliberately, since the stop is the protection and the
trail is the improvement.

**So the native trail arms at exactly the same price as the engine's trail (+1R), at exactly the same
distance (2.5×ATR).** They are not two different policies. They are the same policy, twice.

## b) Who moves the level, and who wins?

**Nothing ever clears the native trail.** The engine's only stop mechanism is `_move_stop_to`
(`main.py:1768`), and it sends **`stopLoss` and `slTriggerBy` only** — never `trailingStop`. The two
are independent fields on the same position, so setting one leaves the other live.
`_cancel_stop_orders` cannot reach it either: that is `cancel-all` with `orderFilter=StopOrder`,
which targets **conditional orders**, and the native trail is a position **attribute** — the same
reasoning `_smart_boot_cleanup`'s docstring already records for the position-level SL.

**The engine cannot even see it.** `trailingStop` appears **once in the entire codebase**
(`main.py:1851`) and **zero times in `virtual_trader.py`**. The engine's own STOP-VERIFY block
(`virtual_trader.py:1353`) reads `info['stopLoss']` and nothing else — so the mechanism it is
competing with is invisible to the check designed to catch exactly this.

**The codebase already knows both can close the position.** `_BYBIT_STOPTYPE_TO_REASON`
(`main.py:2781`) maps **`'StopLoss' → 'sl'` AND `'TrailingStop' → 'trail'`**, and that table was
added on 2026-08-05 *because a native trailing-stop exit was being booked as a stop-out*. The venue
closing by its own trail is not hypothetical here — it is already anticipated in the accounting.

**Who wins:** whichever triggers first, and the asymmetry favours the venue.

| | native (Bybit) | engine (software) |
|---|---|---|
| high-water mark | the venue's own, **continuous, every tick** | `water_mark`, sampled by the **10s poller** |
| trigger | `water_mark − 2.5×ATR` (absolute distance) | `water_mark × (1 − trail_pct/100)`, `trail_pct` = % **of entry** |
| action | closes the position venue-side | `_exec_close(row, 'trail', …)` — a market close |
| survives process death | **yes** | no |

A continuously-tracked mark cannot be beaten by a 10s-sampled one. The audit already measured the
poll-granularity cost at 0.009–0.057 in price, always in the giveback direction — that is precisely
the margin by which the venue fires first. **In practice the native trail should win nearly every
time, which means the engine's trail — including the fresh-ATR `trail_pct` recompute at +1R, the one
piece of genuinely adaptive exit logic SOL has — would be pre-empted and never observed to act.**

🔶 **The limit of this evidence, stated plainly:** the trigger race itself cannot be proven without a
live position, and there has never been one. What **is** proven from the code: both are set on every
live entry, neither clears the other, the engine reads only one of them, and the accounting already
has a case for the venue's trail firing.

**One more interaction:** the engine's software trail does **not** ratchet the venue stop. Section 4
of `_process_position` (`virtual_trader.py:1545-1552`) only tests `trail_hit` and **closes**. The
only stop moves the engine makes are the breakeven lock and the recheck tighten. That matters for the
recommendation below.

## c) 🔴 RECOMMENDATION — KEEP THE ENGINE'S TRAIL, REMOVE THE NATIVE ONE

### The case for keeping the NATIVE trail
- **It survives process death, OOM, a deploy, or a Tor outage.** This is the same argument that put
  the stop on the exchange in the B1 change, and it is a good argument.
- **Continuous tick tracking** — a truer high-water mark, no poll-granularity giveback.
- **Zero network cost.** No per-tick call, on a link that produced 285 SOCKS retries in two days.

### The case for keeping the ENGINE's trail — **and why I would keep this one**
- **It is the stated architecture.** `start_monitor` was RETIRED on 2026-08-01 with this docstring:
  *"`_monitor_positions` was the SECOND position manager… this thread must never start again: two
  managers on one position disagree about breakeven state and either can close it."*
  **The native trailing stop is the surviving second manager.** It was simply on the other side of
  the wire, so the retirement missed it. The principle is already decided in this codebase; M4 is the
  same defect with a venue-side actor.
- **It carries all the adaptive logic** — the fresh-ATR recompute at +1R, coordination with the
  breakeven lock, with the partial-at-arm leg, and with the recheck tiers. The native trail is a
  fixed distance set once at entry and cannot participate in any of it.
- **🔴 It is the only one paper has ever run** (see (d)). SOL is in paper *for the paper-vs-live
  comparison*. Keeping a live-only exit mechanism means the live book's exits would be produced by
  machinery the paper book has never exercised — the comparison would be measuring the wrong thing
  from the first trade.
- It books `close_reason='trail'` through the engine's own accounting, which is the axis every exit
  cohort in this book is cut on.

### What is LOST by removing the native trail — and it is real
**Open profit above breakeven becomes unratcheted if the process dies.** The position is *not*
unprotected: the venue still holds the position-level stop, which the engine pushed to breakeven at
+1R. But the gains above breakeven are only defended by a process that is no longer running. Worst
case: a runner that was +4R gives back to breakeven instead of trailing out.

### 🔶 The third option, which removes that cost — flagging it, not choosing it
Have the engine **push its trail level to the venue stop as it ratchets**, via the `_move_stop_to`
mechanism it already owns. Today it does not — it only watches and closes. That would make the
trail **adaptive AND venue-backed**: the venue always holds the latest trailed level, so process
death loses only *future* ratcheting, never locked gains. It is more work than deleting one call and
it changes the stop's movement pattern, so it is a separate decision. I am not applying it.

**My recommendation: keep the engine's trail, delete the `_place_trail_with_retry` call at
`main.py:2398`.** But the process-death gap is a genuine cost and the third option is how it closes.
**Your call.**

## d) Has the paper book ever exercised this? **NO — and it cannot have.**

`_place_trail_with_retry` has **exactly one call site**, and it sits in `_execute_single_entry` after
the `if OBSERVATION_MODE: return …` early return. **The native trailing stop is a live-only call that
has never once executed**, because SOL has never traded live: `virtual_positions` holds **0 closed
rows with `is_paper=0`**.

Three consequences worth naming:

1. **Two mechanisms moving one stop has never actually happened.** It is a latent defect that fires
   on the first live entry — not something the book can be examined for.
2. **The P2 measurement is about the software trail only.** The $678.05 given back across vpos
   13/15/21/25 is the *engine's* trail. The native one contributed nothing, because it never ran.
3. **This is a fourth paper/live divergence at the flip**, alongside the `trail` vs `sl_triggered`
   label split already recorded as G2c.

**And to answer the question as asked: two mechanisms moving one stop is not a configuration, it is a
defect.** They are not complementary — same distance, same arming price, same job. One of them is
redundant by construction, and the redundant one shadows the other's logic.

---

# 2. 🔴 M6 — THE PARTIAL NO LONGER GUESSES. **APPLIED.**

## a) It refuses, exactly as `_read_entry_fill` does

The removed line was the whole defect:

```python
except Exception as e:
    print("... fill read FAILED ... falling back to requested {want}; "
          "accounting may differ from reality")
    filled = want            # ← the REQUESTED size
```

`_apply_partial_at_arm` then derives `rem = size - qty`, the fee split `qty/size`, and every
downstream R from a number the venue never confirmed. **The entry refuses to guess a size; the
partial guessed one.** It does not any more.

## b) 🔴 THE END STATE — and the answer is neither of the two offered

The question was: *alert and leave the book unchanged, or retry the read?* **Retry — but not the same
read.** Before giving up, ask a **different and more authoritative question**: *how big is the
position now?*

`held` was read before the reduce order, so **`held − contracts_now` is the amount that actually
left** — **measured at the venue, not inferred from intent.** It is a different endpoint from the one
that just failed, so a `fetch_order` outage does not take it down with it. This is the M1 lesson in
its mirror: the number you need is often available from an observable you are not asking.

Four outcomes, all substantiated:

| venue state after the reduce | booked |
|---|---|
| `POS_OPEN`, size fell 1.2 → 0.8 | **0.4** — measured |
| `POS_OPEN`, size fell 1.2 → 1.1 (a *partial* partial) | **0.1** — measured. The old code booked 0.4 |
| `POS_FLAT` — the reduce closed it outright | **1.2** — everything held left |
| `POS_UNKNOWN` / read also failed | **nothing booked** → alert + durable row |

**The final branch, named precisely:** the book is left **UNCHANGED**, deliberately. A wrong number
corrupts `net_pnl`, the fee split and every R that follows; an unchanged book is merely **stale**, and
is corrected the moment a read succeeds.

**The position stays MANAGED — confirmed:** its `virtual_positions` row is untouched and still open,
the engine keeps polling it, its stop is still on the venue and the trail stays armed. **Nothing is
naked.** What is wrong is only the SIZE — and **the eventual close is safe regardless**, because
`_execute_close_position` sizes from `pos['contracts']`, the **venue's** number, never from the book.
The residual cost is that this position's reported P&L overstates by the partial until reconciled by
hand, which the alert says in those words.

## c) `float(x or 0) or None` — **kept, and now says why**

A genuine **zero** fill still becomes `None` = "nothing was reduced", which is correct. That is a
different thing from an *unreadable* fill, and the comment now records that the two must never
collapse into one value. **Proven by S8.**

---

# 3. 🔴 M7 — THE LOSS-STREAK GATE READS THE BOOK IT PROTECTS. **APPLIED.**

## a) Fixed the way the daily-loss brake was fixed on 2026-08-05

```sql
-- before: no paper filter, no live filter, over `trades`
SELECT pnl FROM trades WHERE status='executed' AND pnl IS NOT NULL
 ORDER BY id DESC LIMIT 3

-- after: the book it protects, chosen by mode
SELECT net_pnl FROM virtual_positions
 WHERE status='closed' AND net_pnl IS NOT NULL
   AND COALESCE(is_paper, 1) = ?          -- 1 in paper, 0 in live
 ORDER BY closed_at DESC LIMIT 3
```

The cooldown timestamp query moved with it. **`ORDER BY closed_at`, not `id`** — vpos ids are
assigned when a position *opens*, so a position opened earlier but closed later would order wrong.
A streak is about the order things **closed** in.

## b) 🔶 THE DOUBLE-COUNT: REAL IN THE TABLE, **UNREACHABLE BY THIS QUERY**

The audit said one armed exit is stored twice and could count as two consecutive losses.
**Measured — it cannot.** Both rows do exist (21 entry + 21 close, for 21 positions), but:

| | |
|---|---|
| entry rows (`status='executed'`, `open_*`) | **21** |
| …of those carrying a `pnl` | **0** ← what the gate could double-count |
| close rows the gate actually reads | **21** |
| closed `virtual_positions` | **21** — exactly 1:1 |
| duplicated-pnl groups in `trades` | **0** |
| pnl-bearing rows within 5s of each other | **0** |

`pnl IS NOT NULL` already excludes every entry row. Over the last 30 days both books produce an
**identical** streak history — one halt moment, at the same instant (2026-07-30 12:03:30).

**`trades` is still the wrong book, for two reasons that do survive:**
1. **No paper/live separation at all** — that is the live-blocking defect, and it is (c);
2. **its labels have already diverged from the engine's.** Row 15004 is `sl_triggered_short` in
   `trades` and `close_reason='trail'` in `virtual_positions`. The gate was reading a book that
   already disagrees with the one the bot manages.
3. And the exclusion that saves the query today is an **accident** of how entry rows happen to be
   written — not a declared invariant. Depending on it is depending on something nobody promised.

## c) What it reads after the fix, and what it would have read

**Right now:**

| book | last 3 | negatives |
|---|---|---|
| `trades` (what it read before) | −85.45, −138.67, **+126.52** | **2 of 3** |
| `virtual_positions` paper (paper mode, now) | −85.45, −138.67, **+126.52** | 2 of 3 |
| `virtual_positions` **live** (at the flip, now) | **empty** | **0 — the gate cannot halt** |

**In paper mode the fix changes nothing today, by construction** — the identical property the
daily-brake fix recorded on 2026-08-05.

**Over the last 30 days:** 13 closes in each book, **one** moment with 3 consecutive losses, at the
same timestamp, in both. Had the gate been correct all along, its paper-mode behaviour would have
been **identical**.

**🔴 The entire value is at the flip.** Before: the first live entry would have been gated by a
streak computed from paper rows — 2 of 3 negative, **one paper loss away from halting real-money
trading for 4 hours** before it had placed a single trade. After: live mode reads the live book,
which has zero closed rows, so `len(rows) >= 3` is false and the gate cannot fire on paper history.
**Proven by S10.**

---

# 4. PROOF BY EXECUTION — 8/8 AFTER, **3/8 BEFORE**

Isolated tree, scripted fake Bybit, no network. Run in **both directions**; the five scenarios that
matter fail on `main.py.bak_M6M7_partial_lossstreak_20260806`.

| scenario | **BEFORE** | **AFTER** |
|---|---|---|
| **S5** fill read raises, position readable | `filled = want` → **0.4**, a guess. Calls stop at `fetch_order` | **0.4 measured** from 1.2 → 0.8; an extra `fetch_positions` appears in the call log |
| **S5b** venue moved only 0.1, read raises | **0.4 — booked the REQUEST.** 🔴 the F3 shape | **0.1** — measured |
| **S6** order read *and* position read fail | **0.4 booked**, no Telegram, no row | **None** booked; TG sent; row `partial_fill_unreadable` |
| **S7** the reduce closed the whole position | **0.4** booked when **1.2** left | **1.2** |
| **S8** genuine zero fill | None ✅ | None ✅ *(must not change — it doesn't)* |
| **S9** paper mode, 3 paper losses | halts ✅ | halts ✅ *(must not change — it doesn't)* |
| **S10** **live mode, 3 PAPER losses, 0 live closes** | 🔴 **`allowed=False` — "loss streak 3/3 — cooldown until 16:00Z"**. Live halted on paper | ✅ **`allowed=True`, reason `'ok'`** |
| leak assert | clean | clean |

**S8 and S9 passing in both directions is the point of including them** — they are the invariants the
change must not move, and it does not.

**Isolation** — the two traps already paid for on 2026-08-06, reused: `dotenv` stubbed (because
`main.py:42` does `load_dotenv(<absolute production .env>, override=True)`, which sets `DB_PATH`),
and the production path rewritten in the **copied source of 13 files** before import (because
`signal_matrix.py` calls `init_db()` **at import**). Plus a `sqlite3.connect` guard that raises on the
production path. **0 violations, production `trades.db` SHA-256 unchanged.**

---

# 5. LIVE VERIFICATION

```
Active: active (running) since 2026-08-06 13:39:51 UTC · master 2702530
[MERCURY-SOL] [AP] No active positions in DB — clean boot.
[MERCURY-SOL] [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
```

**0 tracebacks.** `OBSERVATION_MODE=True` — **SOL stays PAPER**. Positions 0/0/0.
Geometry untouched: `SL_BUFFER_ATR` 2.5, `TRAIL_MULT_ATR` 2.5, `ATR_TF` `'1h'`, `LOSS_STREAK` 3/4h.

**Scope held.** One file changed. `config.py` (08-05 00:19:54), `claude_advisor.py` (12:15:12) and
`virtual_trader.py` (08-05 00:20:58) all carry pre-session mtimes. The complete list of **removed**
lines is four: the two `trades` queries and the two lines of `filled = want`. Nothing touched in the
geometry constants, the cascade, score bars, either prompt, the dedup, or the M1/M2/M3 work.

---

# 6. WHERE THE FLIP STANDS

| | finding | status |
|---|---|---|
| M1 | unstopped position on an unreadable fill | ✅ closed 13:30 |
| M2 | worst outcome filed as `observed_skipped` | ✅ closed 13:30 |
| M3 | cancel-before-close | ✅ applied 13:30 — **and re-rated: not a naked window** |
| **M4** | **two trailing mechanisms** | 🔴 **INVESTIGATED — awaiting your decision** |
| **M6** | **partial books the requested size** | ✅ **closed now** |
| **M7** | **loss-streak gate reads the wrong book** | ✅ **closed now** |
| M5 | idempotency key with no exchange check | 🔴 open — fires only on a 403 on a write |
| P1 | close card's Gross excludes the partial (**off by $35.39, already sent**) | 🔴 open |
| P2 | `TRAIL_MULT_ATR == SL_BUFFER_ATR` ⇒ ~1.00R giveback — **$678.05 given back vs $522.22 booked** | 🔴 open, separate decision |

**M4 is now the only remaining item that fires on the first live trade.** M5 needs a 403; P1 and P2
corrupt measurement rather than misplace money.

---

## THE LESSON, NAMED

**M6 is M1 in a mirror.** M1 was *protect before you describe*. M6 is its reflection: **when you
cannot describe something, ask a different question before you invent an answer.** The partial's size
was never unknowable — it was sitting in the position's own size, one endpoint away from the one that
failed. The old code did not reach for it because "the fill" and "the order's fill field" had become
the same idea.

**M7 is the older lesson repeating: a gate must read the book it protects.** The daily-loss brake
learned this on 2026-08-05. The gate beside it, doing the same job on the same table, did not — and
the reason it looked harmless is that in paper mode it produces identical output. **A defect that is
invisible in the mode you are running is still a defect in the mode you are about to switch to.**

And once more, the audit-archaeology lesson from 13:30 held: **the stated mechanism was wrong and the
stated consequence was right.** The double-count cannot reach the gate; the paper-halts-live risk is
exactly as described. Both had to be measured to tell them apart.
