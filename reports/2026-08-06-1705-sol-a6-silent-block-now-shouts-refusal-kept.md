# SOL A6 — THE SILENT BLOCK NOW SHOUTS. THE REFUSAL IS UNCHANGED.

**2026-08-06 17:05 UTC · Mercury-SOL (PAPER) · APPLIED AND PROVEN BY EXECUTION.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`. **One source file changed: `virtual_trader.py`**
(plus a recorded-only canon entry). Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched.**

**This was the last item before the flip.**

---

## THE ANSWER FIRST

```
PRE-FIX   5 poll ticks, live row, unsubstantiable close
          refusal ran 5×  ·  row stayed 'open'  ·  🔴 ALERTS SENT: 0  ·  durable rows: 0

POST-FIX  same 5 ticks
          refusal ran 5×  ·  row stayed 'open'  ·  ✅ ALERTS SENT: 1  ·  durable rows: 1
```

**Nothing about the refusal changed.** `close_reason` and `close_price` are still `None`, the row is
still `open`, no close row was written, nothing was fabricated. The only difference is that it now
says so — **once**.

---

# 1. RATE LIMITING — ONCE PER POSITION, IN TWO LAYERS

A tick-rate alert would fire every 10 s for as long as the row stays open — the operator mutes it, and
a muted alert is worse than none. So the alert is bounded by **the position**, not by time, using two
layers of state:

| layer | state | scope | purpose |
|---|---|---|---|
| 1 | **`_unsub_alerted`** — an in-process `set` of vpos ids | this process | fast path; costs nothing on the 10 s tick |
| 2 | **`naked_position_alerts` row with `resolved=0`** | **durable, survives restarts** | the one that matters |

**Layer 2 is not redundant, and that is the point.** `main._record_naked_position` already states the
principle — *"A Telegram message is not state"*. Without the persisted row, the in-process set empties
on restart and the alert would fire again **on every boot for as long as the row stays open**, which
for this state can be days. The DB row is what makes "once per position" survive **the very restart the
alert asks the operator to make.**

**Keyed on the vpos id**, so a later position on the same side still gets its own alert — and since the
stale row blocks that side, a later position cannot exist until a human clears this one.

The bookkeeping is wrapped whole: **a failure to record cannot mask the state it is recording**, and it
cannot touch the refusal — the caller returns `None` either way.

---

# 2. THE MESSAGE — same register as A2, a designed refusal rather than a malfunction

```
🚨 EXIT UNSUBSTANTIATED — SHORT SIDE BLOCKED
SOL/USDT:USDT · vpos 28
The exchange reports this position GONE, but its closing fill could NOT be read, so the exit
price is UNKNOWN.
✅ Nothing was fabricated — no close row, no PnL, no invented price. That refusal is
deliberate: an exit we cannot price is one we must not record.
🔴 But the row stays OPEN, and an open row BLOCKS every new SHORT entry on SOL/USDT:USDT.
The engine will retry each tick and keep refusing while the fill stays unreadable. This alert
fires ONCE, not per tick.
Do now: 1) open Bybit and confirm the SHORT position on SOL/USDT:USDT really is closed;
2) find its closing fill and price; 3) settle the row by hand to unblock the side.
```

Every element you asked for is named and actionable: **symbol · side · vpos id · the row is open and
BLOCKING that side · the venue position appears gone · the exit price could not be substantiated so
nothing was fabricated · what to do.** It also says the alert fires once, so silence afterwards is not
read as the problem having gone away.

---

# 3. PERSISTED LIKE THE OTHERS

```sql
INSERT INTO naked_position_alerts (ts, symbol, position_side, stage, detail, resolved)
VALUES (?, ?, ?, 'exchange_close_unsubstantiated',
        'vpos={id}|venue reports FLAT, closing fill unreadable — row left OPEN and
         BLOCKING new {side} entries', 0)
```

Same table as A1/A2, with its own `stage`, so the pre-flip check
`SELECT * FROM naked_position_alerts WHERE resolved=0` now surfaces **this** state too. It previously
did not — which is exactly why A6 was the one blocking state invisible to that query.

---

# 4. 🔴 THE REFUSAL IS KEPT — proven, not asserted

The code-only diff is **purely additive**: one call line and one helper. **The `return None` does not
appear in the diff at all.**

```diff
             _booked = _live_book_close(symbol, position_side)
             if _booked is None:
+                _alert_unsubstantiated_close(vpos_id, symbol, position_side, send_tg)
                 return None          # unsubstantiated → leave OPEN, retry next tick
```

And the proof measures the refusal directly rather than trusting the diff: after **five** ticks the row
is still `status='open'` with `close_reason=None` and `close_price=None`, in **both** trees.

The 15:45 distinction stands and is restated at the code: **refusing to record an exit you cannot
PRICE is correct; refusing one you CAN price because a dict lacked a key was the F1 defect.** A6 was
never a wrong refusal — it was a right refusal made quietly.

---

# 5. IT CANNOT FIRE IN PAPER — proven

The branch sits inside `if not _is_paper(row) and _live_pos_state is not None:`. The harness ran a
**paper** row through the same five ticks:

```
── CASE 3: PAPER row (is_paper=1), 5 ticks ──
  _book_exchange_close called : 0   ← the branch is never entered
  alerts sent                 : 0
  naked_position_alerts rows  : 0
```

**Zero.** It adds nothing to the paper book, writes no row, sends no message, and therefore **cannot
contaminate the n=8 trail window.**

---

# 6. EXECUTION PROOF — both directions

Isolated tree, **13-file DB_PATH rewrite**, residual grep 0, sqlite leak assert
(**`production-book opens: 0`**), **isolated `.env`** loaded before `import config`. The harness injects
a live adapter whose `book_close_fn` always returns `None` — the unsubstantiated case — and drives the
**real** `_process_position`, not a stand-in.

| case | measure | PRE-FIX | POST-FIX |
|---|---|---|---|
| **1** · live row, 5 ticks | refusal ran | 5× | 5× |
| | row status | `open` | `open` |
| | `close_reason` / `close_price` | `None` / `None` | `None` / `None` |
| | **Telegram alerts** | **🔴 0** | **✅ 1** |
| | durable `naked_position_alerts` rows | 0 | **1** |
| **2** · restart simulated (in-process set cleared), 3 more ticks | alerts sent | 0 | **0** — the DB row suppresses |
| | durable rows | 0 | still **1** |
| **3** · **paper** row, 5 ticks | `_book_exchange_close` calls | 0 | **0** |
| | alerts / rows | 0 / 0 | **0 / 0** |

**Case 2 is the one that proves layer 2 does real work:** with only the in-process set, a restart would
re-alert; with the persisted row, it stays quiet and the operator is not re-pinged for a state they
already know about.

---

# 7. ALSO RECORDED, NOT FIXED — the `quantise_amount` sub-minimum raise

Added to `OPEN-ITEMS-SOL.md` beside the `quantise_amount` entry, as an open item:

> `quantise_amount` returns `(None, err_pct)` below `minOrderQty`/`minNotionalValue`, and every caller
> is written against that contract. But when the **raw** size is below the venue's amount *precision*,
> `ccxt.amount_to_precision` **raises `InvalidOrder` before the helper's own checks are reached** — so
> it raises instead of refusing.
> **Unreachable at the configured budget:** $100 / $73.22 = raw **1.3657 SOL**, far above the 0.1
> precision. On the partial path it is additionally **contained** by that path's `try/except`.
> 🔴 **It would matter below ~$30 notional**, where the ⅓ partial's raw size falls under 0.1 SOL: the
> partial would book an *exception* rather than the clean "leg not tradable — SKIPPED" the design
> intends. Measured floor: **$30 = both valid · $22–29 = entry valid, partial silently skipped ·
> below ~$8 = the entry itself raises.**

**Not fixed, as instructed.**

---

# 8. WHAT WAS NOT TOUCHED

**`virtual_trader.py` is the only source file changed**, and its diff is the two additions above.
Everything else carries an earlier pass's mtime — none was reopened:

```
main.py         15:46:27  (M5, M1–M7)        claude_advisor.py  16:05:22  (wall percentiles, dual tally, prompts, dedup)
tor_retry.py    15:45:18  (M5)               optimizer.py       15:18:55  (F1, G2c)
config.py       15:19:24  (P2 trail, boot geometry line)
```

Verified live in the running tree, not by mtime alone:

```
P2  TRAIL/SL            : 1.875 / 2.5 = 0.75          ✅
G2c _CLOSE_LABEL[trail] : trail_{s}                    ✅
F1  venue labels        : tp_{s}, liquidation_{s}, adl_{s} + fallback unmapped_close_{s}   ✅
F1  optimizer registered: True                         ✅
P1  gross folds partial : True                         ✅
walls  _wall_pctl(11.7) : 70                           ✅
dedup                   : intact                       ✅
A6  refusal              : intact                      ✅
```

```
mercury-sol.service  active   master 2756504   worker 2756553 (16:59:47)   NRestarts=0
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h
                    OBSERVATION_MODE=True [pid 2756553]
tracebacks since restart : 0        open / active / exit_pending : 0 / 0 / 0
TITAN: git clean · HEAD 897850b · NOT TOUCHED
```

**Backups:** `virtual_trader.py.bak_A6_unsubstantiated_alert_20260806`, `OPEN-ITEMS-SOL.md.bak_A6_20260806`.

---

**Every blocking state in this bot now alerts. The pre-flip check
`SELECT * FROM naked_position_alerts WHERE resolved=0` covers all of them.**

*Generated 2026-08-06 17:05 UTC.*
