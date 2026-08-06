# SOL — M4: THE NATIVE TRAILING STOP IS DELETED. ONE MANAGER, ACROSS THE WIRE.

**2026-08-06 13:55 UTC · Mercury-SOL (PAPER, stays PAPER)**

One file changed: `main.py`. Backup `main.py.bak_M4_native_trail_deleted_20260806`.
Service restarted **13:55:22**, master 2706601, **0 tracebacks**.
Titan (`/root/titan-bot`, LIVE REAL MONEY): **untouched** — clean, `897850b`, workers 2538048/2538082
running continuously since 01:53.

**M4 was the last item that fired on the first live trade. It is closed.**

---

## 1. THE DELETION

The call at `main.py:2398` is gone, and so is everything that existed only to serve it.

### a) 🔴 `_place_trail_with_retry` became unreferenced — **so it is DELETED, not left uncalled**

This was the deliberate decision, and it is the same rule the audit exists to enforce: **a dead
function that reads as armed is the defect.** Three mechanisms with zero runs were found on Titan on
2026-08-05 for exactly this reason. A reader finding `_place_trail_with_retry` in this file would
reasonably conclude SOL arms a venue trail — it does not. The function's 22 lines are removed and
replaced by a tombstone comment that records **why it went, what it cost, and what the follow-up is**,
so the next reader finds the decision rather than the corpse.

Two locals went with it, for the same reason — a dangling local whose comment says *"required by
trading-stop API"* is a small version of the same lie:

| removed | why |
|---|---|
| `_place_trail_with_retry` (the whole function) | unreferenced after the call site went |
| `market_id = exchange.market(symbol)['id']` | computed **only** for that call |
| the whole `if not tp_id:` branch + its Telegram alert | there is no venue trail left to fail; the alert would describe a mechanism that no longer exists |

**Kept, deliberately:** `trail_cb` — it still feeds `trail_pct` (`round(trail_cb / fill_price * 100, 3)`),
which is written to the DB, shown on the card, and **is the number the engine trails on**. And
`active_price`, which is still the engine's arming price and still feeds `_register_active_position`
and the card's *"arms @"*. The geometry is untouched.

### 🔴 What now goes in `tp_id`

`tp_id` held the native call's result and the caller renders it as the card's `🎯 TRAIL ✓/✗` tag
(`main.py:3940`). Leaving it `None` would print **✗ on every live entry while paper printed ✓**
(`virtual_trader.py:379` returns `'VIRT-TRAIL-{vpos_id}'`) — **a new paper-versus-live divergence in
the operator's card, introduced by a change whose entire purpose was to remove one.** That would have
been a quiet own-goal.

So the field keeps its shape and its meaning is made true:

```python
tp_id = f'ENGINE-TRAIL-{_vpos_id}' if _vpos_id else None
```

assigned after `book_live_position`. **The trail is the engine's in both modes, and the engine can
only trail a position it has a ROW for.** `_vpos_id` is `None` exactly when `book_live_position`
failed — in which case there genuinely is no trail, and ✗ is the honest tag.

**The tag stops reporting "a venue call returned OK" and starts reporting something that matters: is
the engine managing this position's trail?** Worth noting what it held before: the pre-fix run shows
`tp_id = True` — a bare boolean in a field named `_id`, which had been meaningless as an identifier
since the B1 change.

### b) `trailingStop` — measured before and after

**Before: 1 occurrence** (`main.py:1851`). **After: `grep -c "'trailingStop'" *.py` → 0.**
Nothing in the codebase sets a native trailing stop any more. Confirmed by grep **and** by execution
(S12b inspects the source with comment lines stripped, so the tombstone's own mention cannot mask a
real one).

### c) 🔴 The engine's trail is now the ONLY trailing mechanism — and STOP-VERIFY is now *correct*

Every writer of `/v5/position/trading-stop` in the tree:

| line | writer | sends | live? |
|---|---|---|---|
| `main.py:1790` | `_move_stop_to` | `stopLoss` + `slTriggerBy` **only** | **yes — the only one** |
| `main.py:4831` | inside `_monitor_positions` | `stopLoss` | **no** — `start_monitor` is retired; it prints `[MONITOR] RETIRED` and never spawns the thread (confirmed in today's boot log) |

Every trailing decision in the tree: `virtual_trader.py:1551-1552`, `if trail_hit: _exec_close(row,
'trail', last, send_tg)`. One mechanism.

**And the point you asked me to state explicitly.** `virtual_trader.py:1353` reads
`info['stopLoss']` and nothing else. Until today that was **accidental blindness**: the venue also
held a `trailingStop` the check never looked at, so the one guard designed to catch a stop
disagreeing with the book was blind to the mechanism it was competing with. **After this change it
has nothing to be blind to.** The venue holds exactly one protective field, `stopLoss`, written by
exactly one function, `_move_stop_to`. Reading `stopLoss` alone is now a **complete** read of the
venue's protection, not a partial one. The check did not change; the world it inspects did, and it is
correct rather than lucky.

### d) Nothing to clean up on the venue — **confirmed by reading it**

SOL has never traded live, so no position carries a native trail. Verified three ways just now:

| | |
|---|---|
| Bybit open positions (read back over Tor) | **0** |
| Bybit open orders | **0** |
| `virtual_positions` with `is_paper=0` (ever) | **0** |
| `virtual_positions` open | **0** |

The single call site sat below `if OBSERVATION_MODE: return …`, so across 21 closed positions it
never executed once. **There is no residue to clear.**

---

## 2. 🔴 THE COST, RECORDED IN THE CANON

Written into `main.py` at the deletion site so it is found by anyone reading the mechanism, not only
by anyone reading this report:

> **Open profit ABOVE BREAKEVEN is no longer ratcheted if the process dies.** The position is **NOT
> unprotected** — the venue holds the position-level stop, which the engine pushes to breakeven at
> +1R — but gains above breakeven are defended only by a **running process**. Worst case, named: **a
> runner at +4R gives back to breakeven.** That is a loss of **unrealised gain, not of capital**, and
> it is the price of this decision.

The distinction is the whole of it: what survives a process death is the *protection*; what does not
survive is the *ratchet*.

---

## 3. 🔶 THE FOLLOW-UP — RECORDED AS **NOT DONE**

Have the engine **push its trail level to the venue stop as it ratchets**, through `_move_stop_to`,
which it already owns. Today it does not: `_process_position` section 4 only tests `trail_hit` and
**closes** — the only stop moves the engine makes are the breakeven lock and the recheck tighten.
That change would make the trail **adaptive AND venue-backed**, so process death would cost only
*future* ratcheting and never locked gains — it removes the cost recorded in §2 entirely.

**Why it is not being done now, recorded with the same weight as the idea:**

1. **Every ratchet step becomes a Tor round-trip**, on a link that produced **285 SOCKS retries and
   26 CloudFront 403s in two days**. A 10s poller pushing a stop on every new water mark would
   multiply the write load on the least reliable part of this system. It needs a **rate limit or a
   materiality threshold** (only push when the level moved by more than X) before it is safe — that
   is design work with its own failure modes, not a small edit.
2. **Two behaviour changes in the exit path immediately before a flip cannot be attributed.** If the
   live book's exits then look different from paper's, there would be no way to tell whether the
   cause was removing the native trail or adding venue-backed ratcheting. One change, then measure.

---

## 4. PROOF BY EXECUTION — 7/7 AFTER, **4/7 BEFORE**

Isolated tree, scripted fake Bybit, no network. The fake records the **payload** of every
trading-stop call, not merely that one happened, so a `stopLoss` write and a `trailingStop` write are
distinguishable.

**BEFORE** — one full live entry:

```
call order : ['fetch_ticker','set_leverage','entry_order','trading_stop[stopLoss]',
              'fetch_order','trading_stop[trailingStop,activePrice]']
payloads   : {'stopLoss': '95.0', 'slTriggerBy': 'MarkPrice'}
             {'trailingStop': '5.0', 'activePrice': '105.0'}    ← 2.5×ATR at +1R
tp_id      : True
```

**AFTER** — the same entry:

```
payloads   : {'stopLoss': '95.0', 'slTriggerBy': 'MarkPrice'}    ← and nothing else
native trail set : None
tp_id      : 'ENGINE-TRAIL-1'
```

| scenario | BEFORE | AFTER |
|---|---|---|
| **S11** a live entry sends **no** trailing-stop call | 🔴 **1 sent**, `trailingStop='5.0'`, `activePrice='105.0'` | ✅ **0 sent** |
| **S11b** the STOP is still set | ✅ 95.0 | ✅ 95.0 — **protection untouched** |
| **S11c** `trail_pct` still reaches the DB/card | ✅ 5.0 | ✅ 5.0 — **geometry untouched** |
| **S11d** `tp_id` reports engine ownership *(after-only assertion)* | `True` (a bare boolean) | `'ENGINE-TRAIL-1'` |
| **S12** the function is **deleted**, not merely uncalled | 🔴 `def` present | ✅ absent |
| **S12b** `'trailingStop'` appears **zero** times in code | 🔴 present | ✅ absent |
| leak assert | clean | clean |

S11b and S11c passing in **both** directions is deliberate — they are the invariants this change must
not move, and it does not: the stop still goes on, and the trail geometry is identical.

**Isolation** — both traps from earlier today reused: `dotenv` stubbed (because `main.py:42` does
`load_dotenv(<absolute production .env>, override=True)`, which sets `DB_PATH`), and the production
path rewritten in the **copied source of 13 files** before import (because `signal_matrix.py` calls
`init_db()` **at import**). Plus a `sqlite3.connect` guard that raises on the production path.
**0 violations, production `trades.db` SHA-256 unchanged.**

---

## 5. LIVE VERIFICATION

```
Active: active (running) since 2026-08-06 13:55:22 UTC · master 2706601
[MERCURY-SOL] [AP] No active positions in DB — clean boot.
[MERCURY-SOL] [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
[MERCURY-SOL] [MONITOR] RETIRED — the paper engine is the single position manager in BOTH modes
```

**0 tracebacks.** `OBSERVATION_MODE=True` — **SOL stays PAPER**. Positions 0/0/0.

**Scope held.** One file changed. `config.py` (08-05 00:19:54), `claude_advisor.py` (12:15:12),
`virtual_trader.py` (08-05 00:20:58) and `trail_arm.py` (06-08) all carry pre-session mtimes —
**the geometry constants, the cascade, score bars, both prompts, the dedup, M1/M2/M3 and M6/M7 are
untouched.** The complete list of removed code is the function, two locals, and the failure branch
that served it.

---

## 6. WHERE THE FLIP STANDS

| | finding | status |
|---|---|---|
| M1 | unstopped position on an unreadable fill | ✅ closed 13:30 |
| M2 | worst outcome filed as `observed_skipped` | ✅ closed 13:30 |
| M3 | cancel-before-close | ✅ applied 13:30 (re-rated: not a naked window) |
| M6 | partial books the requested size | ✅ closed 13:45 |
| M7 | loss-streak gate reads the wrong book | ✅ closed 13:45 |
| **M4** | **two trailing mechanisms** | ✅ **closed now** |
| M5 | idempotency key with no exchange check | 🔴 open — **needs a 403 on a write** |
| P1 | close card's Gross excludes the partial (**off by $35.39, already sent**) | 🔴 open |
| P2 | `TRAIL_MULT_ATR == SL_BUFFER_ATR` ⇒ ~1.00R giveback — **$678.05 given back vs $522.22 booked** | 🔴 open — separate decision |

**🔴 Nothing on the audit's "fires on the first live trade" list remains open.** M5 needs a second
condition; P1 and P2 corrupt measurement rather than misplace money — and P2 is a geometry decision,
deliberately not taken here.

**One consequence worth stating before the flip is considered:** removing the native trail also
removed the *fourth* paper/live divergence. The remaining known one is G2c — paper books a trail exit
as `sl_triggered` in `trades` while live books `trail` — which is now the thing standing between the
book and a clean paper-versus-live comparison.

---

## THE LESSON, NAMED

**A second manager does not stop being a second manager because it lives on the other side of the
wire.** `_monitor_positions` was retired on 2026-08-01 with the correct diagnosis — *"two managers on
one position disagree about breakeven state and either can close it"* — and the retirement was
thorough on this side of the socket and did not look across it. The native trailing stop had the same
distance, the same arming price and the same job as the engine's trail, and it would have won every
race, silently, because it was continuous and the engine polls.

**The tell was that the code could not see it.** `trailingStop` appeared once in the whole
repository, in the line that set it, and zero times anywhere that reads, verifies or reasons about
position state. **A mechanism that nothing in the system can observe is not a mechanism the system
manages — it is one the system is subject to.** That is the strongest single argument for the
deletion, and it is worth keeping as a test to apply elsewhere: *what does this system set that it
never reads back?*
