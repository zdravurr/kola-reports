# MERCURY-SOL — LIVE BOOKING GAP CLOSED + MARGIN SPLIT: **DIFF FOR REVIEW, NOT APPLIED**

**2026-08-05 02:10 UTC** · **NOTHING WAS APPLIED.** No file in `/mnt/.../mercury-sol` was edited, no
service restarted, nothing flipped. The change was built and proven in an **isolated sandbox copy**.
**Titan untouched.**

> **Verdict up front:** the change works, paper mode is **byte-identical by execution**, and the live
> book is now managed. Three things surfaced while building it that you should read before approving:
> a **false promise in an existing alert** (which corrects my own 01:20 report), a **close-reason
> mislabel** that would poison live exit analysis from trade one, and a **flag that keeps the trail
> recompute inert in live too**.

---

# HOW THIS WAS PROVEN WITHOUT TOUCHING THE TREE

13 modules each hold their own **absolute** `DB_PATH`, so patching one module does not isolate a test —
that is the 2026-08-01 lesson that wrote three `TEST/USDT` rows into the production DB. So:

1. copied the whole package **twice** — `sb_base` (untouched) and `sb_patched`;
2. rewrote the DB path in **all 13** files in both copies to a sandbox DB;
3. verified **zero** files still point at the live DB before running anything;
4. ran the **real** `execute_entry` in both trees with identical stubs and identical DB state.

Live DB re-checked afterwards: **21 rows, 21 paper, 0 live, max id 27** — no sandbox row leaked in.

---

# 🔴 THE REGRESSION THAT MATTERS: PAPER IS BYTE-IDENTICAL

Both trees, same pristine DB, same frozen clock, same stubbed exchange, real `execute_entry`:

```
diff -u R_base.txt R_patched.txt   →   (no output)
✅✅ every field and every id matches
```

The paper entry that ran in both:

| | value |
|---|---|
| size | **135.4 SOL** |
| notional | **$10,000** |
| SL | **71.34** (`route=fallback_atr`, dist 3.386%) |
| **1R** | **$338.50** |
| trail_pct | **3.386** |
| `margin_usdt` stored | **2000.0** |
| `is_paper` | **1** |

Nothing moved. The paper book keeps its $10,000 notional and stays comparable with its 21-position
history.

---

# THE DIFF

Three files, **+134 / −16** lines. Presented against the current tree.

```diff
--- mercury-sol/config.py (current)
+++ mercury-sol/config.py (proposed)
@@ -29,8 +29,25 @@
 PARAM_TUNING_ENABLED = False
 
 # ── Position sizing ──────────────────────────────────────────────────────────
-MARGIN_USDT = 2000        # Per-trade margin (USDT). PAPER/virtual sizing while OBSERVATION_MODE=1 → $10,000 notional per trade. NOTE: this SAME constant sizes REAL orders once un-paused (OBSERVATION_MODE=0).
-LEVERAGE    = 5           # Isolated leverage → $10,000 notional per trade.
+# ── PER-TRADE MARGIN — SPLIT BY BOOK (2026-08-05) ────────────────────────────
+# There was ONE constant here sizing BOTH books, and its own comment admitted it:
+# "this SAME constant sizes REAL orders once un-paused". Flipping it to the live
+# figure would have resized the PAPER book from $10,000 notional to $100 and
+# destroyed comparability with its own 21-position history. Two names now,
+# resolved by mode — neither book can move the other.
+PAPER_FIXED_MARGIN = 2000   # paper: 2000 × LEVERAGE 5 = $10,000 notional. 🔴 DO NOT CHANGE — the paper book's history depends on it
+LIVE_FIXED_MARGIN  = 20     # live:    20 × LEVERAGE 5 = $100 notional (entry 1.3 SOL, partial 0.4 at the 0.1 step)
+
+
+def active_fixed_margin():
+    """The margin actually in force for THIS process, resolved on the runtime mode.
+    DISPLAY and STORAGE use this. The two execution paths deliberately use their own
+    constant explicitly instead, because each runs in exactly one mode — so a future
+    reader cannot mistake either path for being mode-dependent."""
+    return PAPER_FIXED_MARGIN if OBSERVATION_MODE else LIVE_FIXED_MARGIN
+
+
+LEVERAGE    = 5           # Applies to BOTH books: paper 2000×5 = $10,000 notional, live 20×5 = $100.
 
 # ── Execution model — strict single-entry, NO DCA grid ──────────────────────
 # Mercury fires ONE market order per signal. There is no averaging-down grid.

--- mercury-sol/virtual_trader.py (current)
+++ mercury-sol/virtual_trader.py (proposed)
@@ -38,7 +38,8 @@
 from config import (
     MONITOR_POLL_FALLBACK_SECONDS,   # PHASE 2: adaptive cadence absorbed from the retired monitor
     OBSERVATION_MODE,                # PHASE 2: stamps is_paper provenance on new rows
-    MARGIN_USDT, LEVERAGE, ATR_LEN, ATR_TF, SL_WALL_ANCHOR_ENABLED,
+    PAPER_FIXED_MARGIN, LIVE_FIXED_MARGIN,   # 2026-08-05: split by book
+    LEVERAGE, ATR_LEN, ATR_TF, SL_WALL_ANCHOR_ENABLED,
     TRAIL_MULT_ATR, BYBIT_TAKER_FEE_RATE,
     MAX_POSITIONS_PER_SIDE, ENABLE_BREAKEVEN_LOCK,
     PARTIAL_AT_ARM_ENABLED, PARTIAL_AT_ARM_FRACTION,   # 2026-08-01: 1/3 realised at +1R
@@ -187,7 +188,9 @@
     atr = _true_atr(ohlcv)
 
     # Sizing — IDENTICAL to main._execute_single_entry:1140-1143.
-    notional_usdt = MARGIN_USDT * LEVERAGE
+    # 2026-08-05: the PAPER constant explicitly — this function only ever runs
+    # in paper (its sole caller is behind `if OBSERVATION_MODE`). Value unchanged.
+    notional_usdt = PAPER_FIXED_MARGIN * LEVERAGE
     # Phase 1 (3): same venue lot-size policy as the live path. `price` is the
     # ticker already fetched above — no extra network call. At paper size this
     # produces the SAME number amount_to_precision already gave (137.9); what it
@@ -326,7 +329,7 @@
                     # even if the mode is flipped underneath it.
                     " is_paper) "
                     "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,'open',?,?,?,?,?,?,?,?,?)",
-                    (symbol, position_side, side, MARGIN_USDT, amount, LEVERAGE,
+                    (symbol, position_side, side, PAPER_FIXED_MARGIN, amount, LEVERAGE,
                      fill_price, atr, sl_price, trail_pct, json.dumps(mgmt_state),
                      json.dumps(fills), fill_price, opened_at, trades_row_id,
                      # max_adverse_price seeds to the entry fill price (adverse mirror
@@ -1472,9 +1475,17 @@
                                                  mgmt_state, _filled_override=_filled)
                     if _rem is not None and send_tg:
                         try:
-                            send_tg(f"🔻 <b>VIRTUAL partial</b> {symbol} {position_side} — "
-                                    f"{PARTIAL_AT_ARM_FRACTION*100:.0f}% off at +1R @ {last:.2f} "
-                                    f"(paper); remainder on the UNCHANGED trail")
+                            # 2026-08-05: the label was hardcoded "(paper)" and would
+                            # have announced a REAL, money-moving partial as paper the
+                            # first time this fired in live. Say which book it was.
+                            _paper = _is_paper(row)
+                            _book  = "paper" if _paper else "🔴 LIVE"
+                            _size  = float(row['size'])
+                            _lot   = _size - float(_rem)     # the QUANTISED leg actually realised
+                            send_tg(f"🔻 <b>{'VIRTUAL' if _paper else 'LIVE'} partial</b> "
+                                    f"{symbol} {position_side} — {_lot:g} of {_size:g} "
+                                    f"off at +1R @ {last:.2f} ({_book}); "
+                                    f"remainder on the UNCHANGED trail")
                         except Exception as e:
                             print(f"{LOG_PREFIX}[PARTIAL] tg failed: {e}", flush=True)
                 except Exception as _pe:
@@ -1641,6 +1652,104 @@
 _live_close = _live_partial = _live_move_stop = _live_pos_state = _live_book_close = None
 
 
+def book_live_position(exchange, symbol, side, position_side, *,
+                       fill_price, amount, atr, sl_price, trail_pct,
+                       entry_fee=None, trades_row_id=None, send_tg=None):
+    """Create the virtual_positions row for a LIVE entry that is ALREADY on the venue.
+
+    🔴 WHY THIS EXISTS (2026-08-05). The only INSERT INTO virtual_positions lived in
+    execute_entry, whose only caller sits behind `if OBSERVATION_MODE`. So
+    `1 if OBSERVATION_MODE else 0` was ALWAYS 1: `is_paper=0` was unreachable and no
+    live position was ever booked. The Phase-2 engine manages this table, so in live
+    it managed nothing — no +1R partial, no breakeven, no trail recompute, no
+    excursion sampling, no recheck tiers, no close accounting — and the daily-loss
+    brake summed an empty set and read $0 forever ON REAL MONEY.
+
+    🔴 THIS FUNCTION NEVER REFUSES AND NEVER RAISES. The order is already filled and
+    the money is already committed; the position EXISTS. Declining to book it — for a
+    stacking count, an integrity error, anything — would recreate the exact gap this
+    closes, only now with a live position nobody manages. Every failure path here
+    alerts loudly and returns None; none of them swallows.
+
+    Deliberately NOT gated on MAX_POSITIONS_PER_SIDE: that check belongs BEFORE an
+    order is sent (it runs upstream), never after the venue has filled one.
+
+    Values come from the REAL fill. The caller has already overwritten `amount` and
+    `fill_price` with what _read_entry_fill read back from the venue, and `entry_fee`
+    with what _resolve_fee resolved — this function invents nothing.
+
+    Recheck baselines are measured with the SAME helpers the paper path and the
+    recheck itself use (_walls_okx + _max_opposing_wall_mult, _recheck_fetch_1h_metrics),
+    so live and paper baselines stay apples-to-apples. Both degrade to None rather
+    than raising, and a missing baseline simply skips that recheck rule for the
+    position's life — the honest outcome of an unmeasured baseline.
+    """
+    def _shout(msg):
+        print(f"{LOG_PREFIX}{msg}", flush=True)
+        if send_tg:
+            try:
+                send_tg(msg)
+            except Exception:
+                pass
+
+    try:
+        opened_at = _utc_now_iso()
+        initial_risk_usdt = amount * abs(fill_price - sl_price)
+        if entry_fee is None:
+            # Should not happen — the live path resolves the fee before calling —
+            # but a None here would poison the partial's fee split, so model it and
+            # say so rather than storing a silent zero.
+            entry_fee = fill_price * amount * BYBIT_TAKER_FEE_RATE
+            _shout(f"[LIVE-BOOK] entry fee missing — modelled at the taker rate "
+                   f"({entry_fee:.4f}) rather than stored as zero")
+        fills = [{'price': fill_price, 'size': amount, 'fee': entry_fee,
+                  'ts': opened_at, 'kind': 'entry'}]
+        mgmt_state = {'breakeven_applied': False}
+
+        _entry_wall_mult = _max_opposing_wall_mult(_walls_okx(symbol), position_side)
+        _entry_adx_1h, _entry_atr_pct_1h = _recheck_fetch_1h_metrics(
+            exchange, symbol, fill_price)
+        if _entry_atr_pct_1h is None and fill_price:
+            _entry_atr_pct_1h = atr / fill_price * 100.0
+
+        with sqlite3.connect(DB_PATH) as conn:
+            cur = conn.execute(
+                "INSERT INTO virtual_positions "
+                "(symbol, position_side, side, margin_usdt, size, leverage, "
+                " initial_fill_price, atr, sl_price, trail_pct, mgmt_state_json, "
+                " fills_json, water_mark, status, opened_at, trades_entry_row_id, "
+                " initial_risk_usdt, original_sl_price, max_adverse_price, "
+                " entry_wall_baseline_mult, entry_adx_1h, entry_atr_pct_1h, "
+                " is_paper) "
+                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,'open',?,?,?,?,?,?,?,?,0)",
+                (symbol, position_side, side, LIVE_FIXED_MARGIN, amount, LEVERAGE,
+                 fill_price, atr, sl_price, trail_pct, json.dumps(mgmt_state),
+                 json.dumps(fills), fill_price, opened_at, trades_row_id,
+                 initial_risk_usdt, sl_price, fill_price,
+                 _entry_wall_mult, _entry_adx_1h, _entry_atr_pct_1h),
+            )
+            vpos_id = cur.lastrowid
+        print(f"{LOG_PREFIX}[LIVE-BOOK] vpos={vpos_id} BOOKED is_paper=0 "
+              f"{position_side} size={amount} @ {fill_price} sl={sl_price} "
+              f"1R=${initial_risk_usdt:.2f} — engine now manages it", flush=True)
+        return vpos_id
+
+    except sqlite3.IntegrityError as e:
+        # ux_vpos_one_open_per_side rejected it: an open row for this side already
+        # exists. The live position is REAL and now unmanaged — this must be loud.
+        _shout(f"🚨 <b>LIVE POSITION NOT BOOKED</b> ({symbol} {position_side})\n"
+               f"A real filled position could NOT be recorded because an open row "
+               f"for this side already exists ({type(e).__name__}). The position is "
+               f"on Bybit with its stop, but the engine will NOT manage it: no +1R "
+               f"partial, no breakeven, no close accounting. <b>Reconcile by hand.</b>")
+        return None
+    except Exception as e:
+        _shout(f"🚨 <b>LIVE POSITION NOT BOOKED</b> ({symbol} {position_side})\n"
+               f"{type(e).__name__}: {e}\nThe position is on Bybit with its stop, but "
+               f"the engine will NOT manage it. <b>Reconcile by hand.</b>")
+        return None
+
+
 def set_live_adapter(*, close_fn, partial_fn, move_stop_fn, pos_state_fn, book_close_fn):
     """main injects the LIVE executors before start_worker. Keeps virtual_trader free
     of any import of main — the same idiom as set_followthrough_hook below (main

--- mercury-sol/main.py (current)
+++ mercury-sol/main.py (proposed)
@@ -829,7 +829,8 @@
     DAILY_LOSS_R_LIMIT,     # PHASE-D: R-based tail brake (both modes)
     BYBIT_TAKER_FEE_RATE,   # PHASE 3 (2): modelled-fee fallback when the venue fee is unreadable
     OBSERVATION_MODE,
-    MARGIN_USDT,
+    LIVE_FIXED_MARGIN,        # 2026-08-05: split by book — live path only
+    active_fixed_margin,      # 2026-08-05: mode-resolved, for DISPLAY/storage
     LEVERAGE,
     ATR_LEN,
     ATR_TF,
@@ -1375,13 +1376,30 @@
         # halt decision changes — all four losing days breach the 5% limit either way.)
         # virtual_positions is the position ledger: exactly one row per position,
         # net_pnl already whole (partial leg folded back), duplicates impossible.
+        # 🔴 2026-08-05 — THE BRAKE MUST MEASURE THE BOOK IT PROTECTS.
+        # Until today only paper rows could exist, so no filter was needed. Now that
+        # is_paper=0 rows are created, an unfiltered SUM would MIX the two books, and
+        # it breaks in BOTH directions:
+        #   • a paper LOSS at $10,000 notional (1R ≈ $128) would trip a brake
+        #     protecting a $100 live book — a spurious halt;
+        #   • worse, a paper WIN would MASK a live loss and SUPPRESS a halt that
+        #     should fire. +5R of paper against -3R of live nets +2R and the live
+        #     book takes three full stop-outs with the brake silent.
+        # The window is real even with a flat flip: DATE('now') spans the whole
+        # calendar day, so a paper position closed hours BEFORE the flip would be
+        # counted against the live book for the rest of that day.
+        # COALESCE(is_paper,1): a legacy row with a NULL stamp counts as PAPER, which
+        # is what it was. (Checked: 21 of 21 existing rows are 1, none NULL — so in
+        # paper mode this filter changes nothing today, by construction.)
+        _brake_book = 1 if OBSERVATION_MODE else 0
         with sqlite3.connect(DB_PATH) as conn:
             row = conn.execute(
                 "SELECT COALESCE(SUM(net_pnl), 0), "
                 "       COALESCE(SUM(CASE WHEN initial_risk_usdt > 0 "
                 "                         THEN net_pnl / initial_risk_usdt ELSE 0 END), 0) "
                 "FROM virtual_positions "
-                "WHERE status='closed' AND DATE(closed_at) = DATE('now')"
+                "WHERE status='closed' AND DATE(closed_at) = DATE('now') "
+                "  AND COALESCE(is_paper, 1) = ?", (_brake_book,)
             ).fetchone()
         daily_pnl = float(row[0] or 0.0)
         daily_R   = float(row[1] or 0.0)
@@ -1904,7 +1922,10 @@
     ohlcv = tor_retry.with_socks_retry(exchange, lambda ex: ex.fetch_ohlcv(symbol, ATR_TF, limit=ATR_LEN * 3), label='ohlcv.atr')
     atr   = true_atr(ohlcv)
 
-    notional_usdt = MARGIN_USDT * LEVERAGE
+    # 2026-08-05: the LIVE constant explicitly — everything below this point in
+    # this function runs only when OBSERVATION_MODE is False (the paper branch
+    # returned above). The paper book keeps PAPER_FIXED_MARGIN and is untouched.
+    notional_usdt = LIVE_FIXED_MARGIN * LEVERAGE
     # Phase 1 (3): round DOWN to the venue lot step and validate min qty/notional.
     # `price` is the ticker we already hold — no extra network call.
     amount, _qerr = quantise_amount(exchange, symbol, notional_usdt / current_price,
@@ -2041,6 +2062,29 @@
                 f"the position exits on its stop, the breakeven move, or an exit "
                 f"signal. <b>No action is required for safety.</b>")
 
+    # ── 2026-08-05 (P1) — BOOK THE LIVE POSITION ────────────────────────────
+    # Until today this return went straight to the caller, which stamped the
+    # `trades` row 'executed' and stopped. NOTHING created a virtual_positions
+    # row, so the Phase-2 engine — "the single position manager in BOTH modes" —
+    # had nothing to manage in live: no +1R partial, no breakeven, no trail
+    # recompute, no excursion sampling, no recheck tiers, no close accounting,
+    # and the daily-loss brake summed an empty set and read $0 on real money.
+    #
+    # Placed HERE, after the stop is confirmed: the SL-failure branch above
+    # emergency-closes and returns None, so a booked row always corresponds to a
+    # position that is both open AND stopped.
+    #
+    # Booked from the REAL fill — `amount` and `fill_price` were overwritten above
+    # by _read_entry_fill (venue truth, not intent) and `fee_cost` by _resolve_fee.
+    # book_live_position never raises: a failure there must not turn a filled entry
+    # into an exception path, it alerts and returns None.
+    _vpos_id = virtual_trader.book_live_position(
+        exchange, symbol, side, position_side,
+        fill_price=fill_price, amount=amount, atr=atr,
+        sl_price=sl_price, trail_pct=trail_pct,
+        entry_fee=fee_cost, trades_row_id=row_id, send_tg=send_tg,
+    )
+
     return {
         'order':        order,
         'fill_price':   fill_price,
@@ -2053,6 +2097,7 @@
         'tp_id':        tp_id,
         'fee_cost':   fee_cost,
         'fee_verified': fee_verified,      # PHASE 3 (2)
+        'vpos_id':      _vpos_id,          # 2026-08-05: None ⇒ booking failed, alert already sent
     }
 
 
@@ -3393,7 +3438,7 @@
         f"{_open_hdr}\n"
         f"💎 {symbol}  @ {entry['fill_price']}\n"
         f"{_macro_blk}"
-        f"📦 {entry['amount']}  ⚙️ x{LEVERAGE}  💵 ${MARGIN_USDT} margin\n"
+        f"📦 {entry['amount']}  ⚙️ x{LEVERAGE}  💵 ${active_fixed_margin()} margin\n"
         f"📈 ATR({ATR_LEN},{ATR_TF}): {entry['atr']:.4f}\n"
         f"🛡 SL {sl_tag} {entry['sl_price']}   🎯 TRAIL {tp_tag} {entry['trail_pct']}%  (arms @ {entry['active_price']})\n"
         f"{indicators.ema_trend_line(_snap)}\n"
```

---

# P1 — ANSWERS

## a) The live path now books from the REAL fill

`virtual_trader.book_live_position()` — a **new function, not a second copy** of the paper insert. It
reuses the same Phase-1 discipline and the *same* baseline helpers the paper path and the recheck
itself use (`_walls_okx` + `_max_opposing_wall_mult`, `_recheck_fetch_1h_metrics`), so live and paper
baselines stay apples-to-apples.

It is called from `_execute_single_entry` **after the stop is confirmed** — the SL-failure branch above
it emergency-closes and returns `None`, so **a booked row always corresponds to a position that is both
open AND stopped.**

Every value comes from the venue, not from intent: `amount` and `fill_price` were already overwritten
by `_read_entry_fill`, and `fee_cost` by `_resolve_fee`.

**Proven by execution in the sandbox:**

```
id                         29
is_paper                   0          ← the whole point
margin_usdt                20.0       ← LIVE_FIXED_MARGIN, not 2000
size                       1.3
initial_fill_price         73.84
sl_price                   71.34
initial_risk_usdt          3.25       ← 1.3 × |73.84 − 71.34|, from the real fill
entry_wall_baseline_mult   20.3       ← recheck baseline armed
entry_adx_1h               29.3
status                     open
recheck_status             None       ← first tier will arm it
```

**It never refuses and never raises.** The money is already committed; declining to book would recreate
the exact gap this closes, only now with a live position nobody manages. Deliberately **not** gated on
`MAX_POSITIONS_PER_SIDE` — that check belongs *before* an order is sent, never after the venue filled
one. Tested: a second booking on the same side hits the unique index, **alerts loudly and returns
`None`; no exception escapes.**

## b) 🔴 UNREADABLE FILL — and a CORRECTION to my own 01:20 report

**What survives, confirmed:**
- ✅ **No row with invented numbers.** `_read_entry_fill` returning `None` raises `RuntimeError`
  ("refusing to book a fabricated position") *before* `book_live_position` is reached.
- ✅ **Not silent.** Two alerts fire — `🚨 ENTRY FILL UNREADABLE` ("a position may be OPEN and
  UNSTOPPED") and `⚠️ ORDER ERROR` — and the `trades` row is stamped **`status='failed'`** with the
  error text. That row is the recoverable state.

**🔴 The correction.** My 01:20 report (§8 row 3) repeated the code's own alert text — *"the next
restart reconciles from the exchange."* **That promise is false.** I traced both boot reconcilers:

- `_reconcile_open_virtual_positions` reads `SELECT … FROM virtual_positions` — **DB only, never the
  exchange**, and it never inserts.
- `_reconcile_active_positions` starts from the `active_positions` table and `return`s early when it is
  empty — and on this failure path `_register_active_position` (line 3462) is never reached, so it *is*
  empty.

So an unreadable fill leaves a **real position that no restart will ever adopt**. Recovery is
**manual**. The state is recoverable *because the alert names it*, not because anything reconciles it.
**I have not changed that alert text in this diff** — it is outside the brief and you should decide
whether to correct the wording or build the exchange-adoption path it promises. Flagging it, not
quietly fixing it.

## c) What the engine will now run — traced, one by one

All six live inside `_process_position`, which iterates every open row with **no mode gate**; the only
branches are the intended adapter dispatch (`_is_paper`).

| mechanism | runs in live? | how |
|---|---|---|
| **close accounting** | ✅ | `_exec_close` → live reduce-only, books at the REAL fill |
| **+1R partial** | ✅ | `_live_partial(...)`, accounting follows the **filled** lot (0.4 SOL at $100) |
| **breakeven** | ✅ | `_apply_breakeven` + `_exec_move_stop` — live also moves the resting exchange stop |
| **excursion sampling** | ✅ | `_record_excursion_sample`, ungated |
| **recheck tiers** | ✅ | `_run_recheck_tier`, baselines stamped at booking (above) |
| **trail recompute** | 🔶 **NO — and not because of this change** | `ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True`, so the one-shot fresh-ATR recompute at +1R **logs fresh-vs-frozen and keeps the frozen value — in BOTH modes.** It is shadow-only by flag today. Flipping it is a separate decision, and I have not touched it. |

## d) 🔴 THE DAILY-LOSS BRAKE — I agree with you, and the reason is stronger than stated

The brake was already better built than expected: **clause 1 is R-based and deliberately size-independent**
("survives $10,000 → $100 without re-calibration"), and **clause 2 (equity %) is already LIVE-only**.
What it lacked was an `is_paper` filter, so it would have summed **both books**.

**Your reading is right — live rows only — and the sharper argument is the other direction:** a paper
**loss** tripping a live brake is a spurious halt, which is merely annoying. A paper **WIN masking a
live loss** *suppresses a halt that should fire* — the live book takes three full stop-outs and the
brake stays silent. That is the dangerous direction, and unfiltered it is real.

The window is not hypothetical even with a flat flip: `DATE('now')` spans the whole calendar day, so a
paper position closed **hours before** the flip counts against the live book for the rest of that day.

**Demonstrated in the sandbox** — a paper −$300 at $10,000 notional alongside a live −$3.25:

```
PAPER book today   pnl $ -300.00    -2.34R
LIVE  book today   pnl $   -3.25    -1.00R   ← what the live brake must see
UNFILTERED (old)   pnl $ -303.25    -3.34R   ← mixes the two books
```

**−3.34R breaches `DAILY_LOSS_R_LIMIT = 3.0` → the unfiltered brake HALTS live trading** because of a
paper loss, while the live book is down one single stop-out. The filter fixes it.

Scoped as `COALESCE(is_paper, 1) = ?` with `1` in paper and `0` in live — a legacy NULL stamp counts as
paper, which is what it was. **In paper mode this changes nothing today by construction**, since 21 of
21 rows are already `is_paper=1` — which is exactly why the regression above came out identical.

## e) The newly-reachable live branch — safe, but it MISLABELS every exit

**Safety semantics: correct as written.** Verified line by line:
- `UNKNOWN` → returns `None`, does nothing (Phase 1 discipline) — nothing cancelled, nothing booked;
- `FLAT` → `_book_exchange_close`, which **refuses to book a close it cannot substantiate** (failed
  trade read, no matching fill, unparseable or non-positive values → `None`), leaving the row **OPEN**
  for the next tick rather than fabricating a close;
- `OPEN` → re-reads the **position-level** `stopLoss` field (never an order list, or a protected
  position reads as naked) off the object already held — no extra network call.

**🔴 But its close reason is hardcoded.** `_book_exchange_close`'s own docstring says *"resting stop **or
trail** fired"*, and the caller books every one of them as:

```python
return _poller_close(vpos_id, float(_booked['fill_price']), 'sl', symbol, position_side, send_tg)
```

So **every** live exchange-side exit — including a Bybit-native **trail** exit — will be recorded as
`close_reason='sl'`. SOL's entire exit analysis is cohorted by `close_reason` (the 08-01 diagnosis
"the trail gives back exactly 1R" *is* a `close_reason` cohort). From the first live trade, trail exits
would be misfiled as stop-outs and the live R-distribution would look like a book of pure −1R stops.

The data to tell them apart **is** available — the raw trade dict carries `stopOrderType` — but
`_book_exchange_close` returns only `{fill_price, amount, fee_cost}` and discards it. **Not fixed in
this diff** (outside the brief); the remedy is to return the trade's `stopOrderType` and pass a reason
through instead of the literal `'sl'`.

---

# P2 — THE MARGIN SPLIT

`PAPER_FIXED_MARGIN = 2000` · `LIVE_FIXED_MARGIN = 20` · `active_fixed_margin()` resolving on
`OBSERVATION_MODE`. **`MARGIN_USDT` is gone entirely** — a name that no longer decides anything is the
"label doesn't say what the thing is" defect we have been closing all week, so it was removed rather
than left as a trap. All six readers updated (both imports, both sizing sites, the stored column, the card).

- **live path** → `LIVE_FIXED_MARGIN` explicitly · **paper path** → `PAPER_FIXED_MARGIN` explicitly.
  Each function runs in exactly one mode, so an explicit constant is more honest than a resolver there.
- **`margin_usdt` column** stores the margin actually used — 2000 on the paper row, 20 on the live row
  (both proven above).
- **entry card** prints `active_fixed_margin()` — your §8 row 1 check. In live it will read
  `💵 $20 margin`; if it ever reads `$2000` the split did not land.
- `LEVERAGE`'s comment claimed "$10,000 notional per trade", true for only one book now — corrected.

**Bonus fix, flagged as beyond the brief so you can strike it:** the +1R partial's Telegram text
hardcoded **`(paper)`** and would have announced a real, money-moving partial as paper the first time
it fired live. It now names its book and prints the **quantised lot actually realised** (`0.4 of 1.3`)
instead of a nominal `33%`.

---

# WHAT I AM NOT DOING

| | |
|---|---|
| ❌ applied | nothing — this is a diff for review |
| ❌ restarted | no |
| ❌ flipped | no |
| 🔶 left open | the false "restart reconciles from the exchange" promise (b) |
| 🔶 left open | the hardcoded `'sl'` close reason (e) |
| 🔶 left open | `ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN=True` keeps trail recompute shadow-only (c) |
| 🔶 separate | P3 venue leverage 10→5, P4 the key expiring 2026-08-13 |

**To apply:** `.bak` all three files, copy them in, `py_compile`, restart **from flat**, then verify
`is_paper=0` appears on the first live entry. The paper regression above should be re-run after applying
to confirm the tree matches the sandbox.
