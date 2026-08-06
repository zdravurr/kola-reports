# SOL — THE NAKED-POSITION CLASS CLOSED: PROTECT BEFORE DESCRIBE

**2026-08-06 13:30 UTC · Mercury-SOL (PAPER, stays PAPER) · M1 / M2 / M3 APPLIED and PROVEN BY EXECUTION**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`, one file changed: `main.py`.
Backup `main.py.bak_nakedposition_M1M2M3_20260806`. Service restarted **13:20:27**, worker **2697396**.
Titan (`/root/titan-bot`, LIVE REAL MONEY): **untouched** — `git status` clean at `897850b`, workers
2538048 / 2538082 running continuously since 01:53, never restarted, never read for state.

---

## §0 — WHAT WAS APPLIED WHEN I ARRIVED: **NOTHING. The tree was clean.**

The dropped session landed no code. Proven by mtime, not by assumption.

**Every file in the SOL tree with an mtime after 12:20:55** — the whole tree, `find -newermt`:

| file | mtime | what it is |
|---|---|---|
| `trades.db` | 12:56:31 | runtime — the bot writing signals |
| `optimizer/tg_offset.txt` | 12:58:04 | runtime — the optimizer's Telegram cursor |

**No `.py` file. No new `.bak_*`.** The most recent source mtimes were exactly the confirmed dedup:
`main.py` **12:10:12**, `claude_advisor.py` **12:15:12**, `config.py` 2026-08-05 00:19:54.

**b) Was `main.py` modified beyond the 12:10 dedup edit? NO — not in whole and not in part.**
Verified at the two named regions before any edit of mine:

- **~1958-2065** — the order was `create_market_order` (1958) → `_read_entry_fill` (1976) →
  `raise` (2005) → … → `_place_sl_with_retry` (**2059**). The stop still sat 54 lines *after* the
  raise. **M1 had not landed in any form.**
- **2061-2070** — still `print(...)` on the emergency-close failure, no Telegram, and `return None`.
  **M2 had not landed.**
- **~2154-2210** — still `_cancel_open_orders_for_side` (2191) → `fetch_ticker` (2193) →
  `create_market_order` (2206). **M3 had not landed.**

Nothing was half-applied, so I did not stop.

**c) Service** — `active (running)` since 12:20:39, worker **2680679**, `NRestarts=0`,
**0 tracebacks / errors / exceptions** in the journal since 12:20:55.

**d) Runtime invariants, read by IMPORTING config (with `.env` loaded):**

| | |
|---|---|
| `MERCURY_OBSERVATION_MODE` → `OBSERVATION_MODE` | **True (PAPER)** |
| `ADVISOR_WALL_ALIGNED_V2_MULT_CEILING` | 20.0 |
| `NEWS_OBSERVATION_PINNED` | True |
| `MAX_POSITIONS_PER_SIDE` | 1 |
| `SL_BUFFER_ATR` / `TRAIL_MULT_ATR` | **2.5 / 2.5** (G1b still live — untouched, out of scope) |
| `ATR_TF` | `'1h'` |

⚠️ **A correction worth recording, because it is a trap.** `MERCURY_OBSERVATION_MODE` is an *env
var*, not a config attribute — the attribute is `config.OBSERVATION_MODE`. My first read imported
`config` **without** `load_dotenv`, which returned `False` (the `os.getenv` default) — the opposite
of the truth. Worse, my first `import main` in that same bare shell ran main's **import-time boot**,
which executed `_smart_boot_cleanup` against Bybit. I checked what it did: the venue holds **no
positions and no open orders**, so `cancel-all StopOrder` cleared nothing. No harm, but it was an
unintended live call and it is on the record. **Import `main` only with a faked exchange.**

**e) Positions: all zero.** open `virtual_positions` = 0, `active_positions` = 0, `exit_pending` = 0
(`exit_pending` is its own table in `state_machine.py`, not a `virtual_positions` column).

Venue read back directly: **no positions, no open orders, USDT balance 811.90**.
That balance is the M-class exposure number — see below.

**f) Titan untouched** — clean, `897850b`, workers 2538048/2538082 with unbroken uptime.

---

## THE PREMISE ALL THREE SHARE

`tradeMode 0` — **CROSS margin**. An unstopped position is not bounded by its $20 margin; it draws on
the wallet. **The venue balance is $811.90, not $100.** Every "at $100 notional an alert is
sufficient" judgement in this file was reasoning about an isolated-margin position that does not
exist. That is why these three block the flip.

---

## 1. M1 — THE STOP NO LONGER DEPENDS ON READING THE FILL

### a) The reordering

**Before** — protect *after* describe, so a failure to describe meant a failure to protect:

```
create_market_order  →  _read_entry_fill  →  raise  ✗ (stop never reached, 54 lines below)
```

**After** — protect *before* describe:

```
create_market_order  →  compute_initial_sl(current_price)  →  _place_sl_with_retry  ← STOP IS ON
                     →  _read_entry_fill  →  raise if unreadable   (position already protected)
                     →  compute_initial_sl(fill_price)  →  _move_stop_to   (exact level)
```

This is only possible because **SOL's stop is a position-level `/v5/position/trading-stop` — a SET,
not an order.** It needs no size and no side, so it does not need the fill. Titan's stop is an order
and cannot do this; SOL's can.

**What the stop price derives from when the fill is unknown: the pre-trade ticker `current_price`.**
Chosen over the venue's `avgPrice` and over a re-read, and the reason is the whole point —
**both of those are network reads, and the failure being fixed IS a network read that fails.** A stop
that needs a successful read in order to exist reintroduces the defect it is meant to close.
`compute_initial_sl` is pure and `clusters` is the 60s-cached snapshot, so the provisional level
costs **no additional call**. The error is one market order's slippage measured against a 2.5×ATR
stop, and it is replaced by the exact fill-derived level the moment the fill is readable.

**The level is unchanged.** Same `compute_initial_sl`, same `SL_BUFFER_ATR`, same wall anchoring.
What changed is *when* the first stop goes on, not *where* it goes.

### b) If the stop set ALSO fails

That branch is M2 and it is now the only exit from it: `_sl_failsafe` **always raises**, so the code
cannot fall through into booking a position it failed to protect. Three classified outcomes, below.

If instead the *exact re-set* fails (the stop is already on at the provisional level), there is
**deliberately no emergency close** — the position is protected, at a slippage's width from the
intended price. `sl_price` then keeps the **provisional** value, so the DB, the close card and the
engine all record what is genuinely on the venue rather than what was intended.

### c) The fill is read only after — and still refuses to invent a size

`_read_entry_fill`'s *"NEVER guesses a size"* discipline is untouched. The unreadable-fill branch
still raises and still books nothing. **Refusing to book no longer means refusing to protect** — that
was the defect, and it is the whole change. The Telegram text was corrected accordingly: it used to
say *"A position may be OPEN and UNSTOPPED"*, which is no longer the state, and an alert that
overstates is as bad as one that understates.

### d) The adopter — `_assert_exchange_matches_db_at_boot`

Both existing reconcilers read the **database**. Nothing read the **exchange**, so a Bybit position
with no DB row was invisible forever. Added, and wired at boot after both DB loaders:

- reads the venue; for each open side, looks for an open live `virtual_positions` row
  (`COALESCE(is_paper,1)=0`) or an `active_positions` row;
- an orphan → loud Telegram naming the side, its size, its entry **and whether it has a stop** →
  a durable row in a new `naked_position_alerts` table → the side is added to `_BOOT_ORPHAN_SIDES`;
- **`_execute_single_entry` refuses new entries on a blocked side.** Without this the alert is
  advisory and the bot stacks a second position onto a side it cannot account for — `MAX_POSITIONS_
  PER_SIDE=1` cannot stop it, because it counts DB rows and the orphan has none;
- **on a failed read it reports UNKNOWN, never clean.** Concluding "no orphans" from a read that
  failed is the F1 defect this codebase already fixed everywhere else.

**It does not fabricate a row.** Adopting means inventing an entry price, a 1R, a breakeven and a
partial leg from data we do not have — the same fabrication `_read_entry_fill` refuses. It makes the
position **visible** and **blocks the side**, which is the honest half.

---

## 2. M2 — THE WORST OUTCOME IS NO LONGER A NON-EVENT

**a)** The emergency-close failure now sends `🔴🔴🔴 NAKED POSITION — EMERGENCY CLOSE FAILED`, naming
the symbol, the side, the underlying error, that the account is on **CROSS margin**, and the three
manual steps. It also writes a **durable row** — a Telegram message is not state, and the operator is
being asked to restart the very process that holds the only record.

**b)** It no longer shares a return value with "no order was placed". `_sl_failsafe` **always raises**
`EntryFailSafeError`, carrying its own status:

| status | meaning | `naked` |
|---|---|---|
| `naked_position_unprotected` | close raised — we do NOT know the position is flat, and we DO know it has no stop | **True** |
| `sl_failed_position_closed` | close succeeded; contained, still not routine | False |
| `sl_failed_no_position` | venue FLAT — the entry never filled; nothing was ever naked | False |

The webhook caller catches `EntryFailSafeError` **before** the generic handler and stamps the row
with `e.status`. `observed_skipped` is now unreachable from this path. One query counts it:

```sql
SELECT status, COUNT(*) FROM trades
 WHERE status LIKE 'sl_failed%' OR status='naked_position_unprotected';
```

**c) The `POS_UNKNOWN` path is confirmed handled — by execution, not by reading.** Scenario **S2b**
below fires a Tor blip on `fetch_positions` at exactly the moment the fail-safe runs;
`_execute_close_position` raises *"refusing to close blind"*, and the new path catches it, alerts,
persists and raises `naked_position_unprotected`. The old code printed one line and returned `None`.

---

## 3. M3 — CLOSE FIRST, CANCEL AFTER — **AND A CORRECTION TO THE AUDIT**

**a)** Applied. The order is now `create_market_order(close)` → `_cancel_open_orders_for_side` →
`_cancel_stop_orders`. Both cancels still run; they run when there is nothing left to protect.

**b) The ticker: moved after the close AND made conditional** — strictly better than either alone.
It fed exactly one thing, the last fallback for `fill_price`. The common path (a market order that
returns its `average`) now makes **no ticker call at all**; the rare path pays for it only when it
has nothing better. If that read then fails, it falls back to the position snapshot rather than
raising — the close already happened, and failing to *price* it must not make the caller believe the
position is still open.

**c) Confirmed: the fix does not rely on the mode guard.** The paper branch returns at the top of
`_execute_close_position`, so everything below is the live path by construction. The reordering is
unconditional within it and adds no test of `OBSERVATION_MODE`. This code is what runs at the flip.

### 🔶 THE CORRECTION — M3 WAS **NOT** A NAKED WINDOW, AND I CAN SHOW IT

The 13:00 audit rated M3 as *"the protective stop goes at 2191"*. **Run against the pre-fix file,
the stop survives that cancel.** The reason is the B1 change: since SOL's stop became a
**position-level attribute** it is **not an order**, and `_cancel_open_orders_for_side` reaches only
orders — it calls `fetch_open_orders` with no params, which ccxt 4.5.52 sends as
`orderFilter='Order'`; conditional/stop orders are not even returned. That is the same fact
`_cancel_stop_orders`' own docstring records from the other side. **The audit's premise was inherited
from the pre-B1 era, when the SL genuinely was a conditional order.**

Pre-fix run, close failing: `['fetch_positions', 'fetch_open_orders', 'fetch_ticker', 'close_order']`
→ position **OPEN**, venue stop **still `97.50`**. Not naked.

**The reorder is still applied, for two real but smaller reasons:** it shrinks the gap between
`_fetch_position_state` (which established `close_amount`) and the close from up to three Tor
round-trips to none, so a stale `close_amount` is far less likely; and it stops the safety of this
path from resting on a fact that could silently change — if a stop ever becomes an order again, the
old sequence would become a genuine naked window with no code change to notice it.

**M3's rank drops from "misplaces money on the first live close" to hardening.** M1 and M2 do not
move: both were reproduced firing.

---

## 4. PROOF BY EXECUTION — 9/9, AND THE OLD CODE FAILS THE SAME TESTS

Isolated copy of the tree, a scripted fake Bybit, no network. **Both directions were run**: a test
that passes on fixed code proves nothing unless it fails on the broken code, so every scenario was
also run against `main.py.bak_nakedposition_M1M2M3_20260806` — byte-identical to what the service ran
until 13:20.

| scenario | **BEFORE** | **AFTER** |
|---|---|---|
| **S1** fill read raises | `['fetch_ticker','set_leverage','entry_order','fetch_order']` — **`trading_stop` NEVER CALLED**, position OPEN, stop `None` | `[…,'entry_order','trading_stop','fetch_order']` — **stop `95.0` set BEFORE the read**, position OPEN and protected, entry still refuses to book |
| **S2a** SL fails, close works | `return None` → `observed_skipped` | raises `sl_failed_position_closed`, position flat |
| **S2b** SL fails, close fails (Tor blip → `POS_UNKNOWN`) | `return None` → **`observed_skipped`**, **1** TG (the pre-close one), **no alert on the failure** | raises **`naked_position_unprotected`**, **2** TG incl. `🔴🔴🔴 NAKED POSITION`, durable row `sl_failsafe_close_failed` |
| **S2c** SL fails, venue FLAT | indistinguishable from the above | raises `sl_failed_no_position`, correctly benign |
| **S3** close fails | stop `97.50` survives (see correction), ticker ran before the close | stop `97.50` survives, **no cancel and no ticker before the close** |
| **S3b** close succeeds | — | close ran **before** both cancels; **ticker not called at all**; stop cleared after |
| **S4** venue position, no DB row | `_assert_exchange_matches_db_at_boot`: **absent**. `_BOOT_ORPHAN_SIDES`: **absent**. `EntryFailSafeError`: **absent** | orphan detected, TG sent, row persisted, `{'SHORT'}` blocked, **entry refused — no `entry_order` sent** |
| **S4b** boot read itself fails | — | reports **inconclusive**, does not claim a clean start |

### The leak assert — and the two leaks it actually caught

Not decoration. `sqlite3.connect` was wrapped to **raise** on any attempt to open the production DB,
and the production file was SHA-256'd before and after. **It fired twice on the first runs, both
genuine:**

1. `main.py:42` is `load_dotenv('/mnt/.../mercury-sol/.env', override=True)` — an **absolute path to
   the production `.env`, with `override=True`**, and that file sets `DB_PATH`. Exporting `DB_PATH`
   before the import is **not enough**; the import overwrites it with the production path.
2. `signal_matrix.py` hardcodes the path and calls `init_db()` **at import**, i.e. while
   `import main` is still running — so patching `module.DB_PATH` *after* import is **too late**.

Final isolation: the production path is rewritten in the **copied source** of all **13** files that
hardcode it, before a line is imported, and `dotenv` is neutralised.
Result: **0 blocked attempts, production `trades.db` SHA-256 unchanged.**

---

## 5. LIVE VERIFICATION AFTER RESTART

```
Active: active (running) since 2026-08-06 13:20:27 UTC · worker 2697396
[MERCURY-SOL] [SMART-CLEANUP] No open positions for SOL/USDT:USDT — proceeding with orphan cleanup
[MERCURY-SOL] [AP] No active positions in DB — clean boot.
[MERCURY-SOL] [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible   ← NEW, and it read the EXCHANGE
```

**0 tracebacks.** `OBSERVATION_MODE=True` — **SOL stays PAPER**. Positions still 0/0/0.
Geometry untouched: `SL_BUFFER_ATR` 2.5, `TRAIL_MULT_ATR` 2.5, `ATR_TF` `'1h'`.

**Scope held.** One file changed. `config.py` (2026-08-05 00:19:54) and `claude_advisor.py`
(12:15:12) have their pre-session mtimes. Nothing touched in geometry constants, the cascade, score
bars, either prompt, the 12:20 dedup, or `MERCURY_OBSERVATION_MODE`. The complete list of *removed*
lines is the old SL-placement block, the old inline fail-safe, the pre-close cancel, and the
unconditional ticker — nothing else.

---

## WHAT THIS DOES AND DOES NOT UNBLOCK

**Closed:** M1 (a funded position is now protected before it is described, and an orphan is visible
at boot and blocks its side) · M2 (the worst state is loud, durably recorded and countable, and can
no longer be filed as `observed_skipped`) · M3 (applied as hardening — **and re-rated: it was not the
naked window the audit described, and the evidence is in §3**).

**Still open from the 13:00 audit, untouched here and still blocking or costing:**
**M4** two trailing mechanisms armed at once · **M5** idempotency key with no exchange check ·
**M6** the live partial falls back to the *requested* size · **M7** the loss-streak gate reads paper
rows (currently 2 of 3 negative — one paper loss from halting live) · **P1** the close card's Gross
excludes the partial while Fees and Net include it (**already sent to Telegram, off by $35.39**) ·
**P2** `TRAIL_MULT_ATR == SL_BUFFER_ATR` ⇒ ~1.00R giveback, **$678.05 given back vs $522.22 booked**.

**The flip is not unblocked by this change alone.** M4, M6 and M7 fire on the first live trade.

---

## THE LESSON, NAMED

**PROTECT BEFORE DESCRIBE.** The defect was never in the stop, the level, or the fill reader — each
was individually correct, and `_read_entry_fill`'s refusal to guess is genuinely good code. The
defect was in the **order**: a bot that must *describe* a position before it may *protect* it will,
on the first network hiccup, own something it cannot see and has not stopped. The fix is not a new
mechanism. It is two existing mechanisms, swapped.

The second lesson is smaller and sharper: **an audit finding inherits the era it was written in.**
M3 was real when the stop was an order. B1 made it not-real, and nothing re-checked. That is why
these were run against the *pre-fix file* rather than reasoned about — and it is the only reason the
correction in §3 exists.
