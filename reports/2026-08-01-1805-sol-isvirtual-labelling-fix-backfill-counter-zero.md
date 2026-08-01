# sol-isvirtual-labelling-fix-backfill-counter-zero

_2026-08-01 18:05 UTC_

---

# MERCURY-SOL — `is_virtual` LABELLING FIX APPLIED, SIX ROWS BACKFILLED, COUNTER 6 → 0

**Applied and live.** The write is fixed, the six mislabelled rows are corrected under an audited
predicate, and the live-mode news gate can no longer be advanced by paper activity. **The
200-consultation window was NOT reset** — a labelling fix is not a prompt change. SOL stays PAPER.
Titan untouched.

---

# THE ANSWER FIRST

| | |
|---|---|
| Write fixed in | **`main.py::_execute_armed_exit`** — now stamps `is_virtual=1 if OBSERVATION_MODE else 0` |
| Rows backfilled | **6** — 2148, 3318, 3507, 4220, 10309, 13716, all `0 → 1` |
| Non-virtual executed counter | **6 → 0** |
| News gate | still `True` → **news still withheld; the entry prompt is byte-identical** |
| Freeze | **not touched** — and the fix is actively freeze-*preserving* (§4) |
| 200-window | **NOT reset — still 1/200 from 17:13:02** |
| vpos 25 | **open and reconciled** — and its **partial-at-arm ⅓ leg fired at 17:34:57**, the first time ever |

**One thing I found before applying that the brief did not anticipate, and checked out fully
before touching anything:** each armed exit wrote **two** rows carrying the *identical*
`order_id`, price, amount and PnL. Relabelling therefore puts six paper closes twice inside the
`is_virtual=1` population. I verified no reader double-counts as a result before proceeding —
§6.

---

# §1 — THE WRITE FIX

**Changed function: `_execute_armed_exit` (`main.py:3127-3145`).** One call, one added kwarg:

```python
    update_trade(row_id, status='executed', price=result['fill_price'],
                 amount=result['amount'], pnl=realized_pnl, fee=result['fee_cost'],
                 order_id=(result['order'] or {}).get('id'),
                 is_virtual=1 if OBSERVATION_MODE else 0)
```

`update_trade` builds its `SET` clause from `**kwargs`, so no signature change was needed. The
value is **mode-dependent, not hard-coded to 1** — in live these rows must remain `0`, and the
counter must then be movable only by real fills.

**Labelling only.** No price, size, PnL, fee, routing, gate or threshold was changed.

## Every other close route audited — all already correct, none changed

| route | writer | `is_virtual` | verdict |
|---|---|---|---|
| paper SL / trail / timeout / exit-signal | `virtual_trader.close_position` | literal `1` in the INSERT (`virtual_trader.py:455-456`) | ✅ already correct |
| paper entry | `virtual_trader.execute_entry` | explicit `is_virtual=1` UPDATE (`virtual_trader.py:290`) | ✅ already correct |
| **armed exit** | `_execute_armed_exit` | schema default `0` | 🔴 **was wrong → FIXED** |
| `_handle_5m_close` | `insert_signal` + `update_trade` | would default to `0` | ⚠️ **unreachable in paper** — gated behind `_fetch_open_position`, which is always empty in observation mode. It **cannot** mislabel a paper row. Deliberately **not** changed: it is in the wake-on-flip set (17:46 study §3) and out of this scope. |
| `_handle_liquidity_sweep` | same | same | ⚠️ same, and dead a second time by the `('EQH','EQL')` vs `"Equal Highs"` router mismatch. **Not** changed. |
| live SL-detect / timeout close | `insert_signal` | `0` | ✅ correct — these are live-only paths |

So exactly one route could produce a mislabelled paper row, and that is the one that was fixed.

---

# §2 — THE BACKFILL

**Backups taken first:**

| artefact | detail |
|---|---|
| `trades.db.bak_pre_isvirtual_backfill_20260801` | 42,618,880 bytes, 2026-08-01 17:59:28 |
| `main.py.bak_isvirtual_armedexit_20260801` | md5 verified identical to pre-edit `main.py` (`c6146ae5…`) |

**Guarded predicate**, run inside a single `BEGIN IMMEDIATE` transaction:

```sql
UPDATE trades SET is_virtual=1
 WHERE signal_type='15m_armed_exit'
   AND status='executed'
   AND (is_virtual IS NULL OR is_virtual=0)
   AND order_id LIKE 'VIRT-CLOSE-%';
```

The `order_id` clause is the real safety. Every paper close carries a `VIRT-CLOSE-<vpos>` order
id, minted by the paper engine; a genuinely **live** armed exit would carry a Bybit order id and
**could never be caught by this backfill**. The predicate is therefore safe to re-run and safe
against future live rows.

**`changes()` returned 6** — exactly the expected set, no more.

## The audited record — prior values and ids

| trades id | timestamp (UTC) | `order_id` | prior `is_virtual` | now |
|---|---|---|---|---|
| **2148** | 2026-06-15 21:45:05 | `VIRT-CLOSE-7` | **0** | 1 |
| **3318** | 2026-06-20 13:30:02 | `VIRT-CLOSE-8` | **0** | 1 |
| **3507** | 2026-06-21 08:45:01 | `VIRT-CLOSE-9` | **0** | 1 |
| **4220** | 2026-06-23 21:30:02 | `VIRT-CLOSE-11` | **0** | 1 |
| **10309** | 2026-07-16 13:45:10 | `VIRT-CLOSE-19` | **0** | 1 |
| **13716** | 2026-07-28 15:15:09 | `VIRT-CLOSE-23` | **0** | 1 |

`PRAGMA quick_check` → **ok**. The same table is written into `OPEN-ITEMS-SOL.md` so the
correction is auditable from the canonical file, not only from this report.

---

# §3 — THE COUNTER READS 0, AND WHAT THAT BUYS

```
SELECT COUNT(*) FROM trades WHERE status='executed' AND (is_virtual IS NULL OR is_virtual=0)
  → 0        (was 6)

market_context.is_in_funding_news_observation()  → True        (news still withheld)
```

Every executed row in the book is now `is_virtual=1`:

| signal_type | is_virtual | n |
|---|---|---|
| `15m_armed_exit` | **1** | 6 |
| `exit_long` / `exit_short` | 1 | 3 / 3 |
| `open_long` / `open_short` | 1 | 8 / 11 |
| `sl_triggered_long` / `sl_triggered_short` | 1 | 5 / 7 |

**What it buys, plainly: while SOL is in `OBSERVATION_MODE`, the news gate can no longer be
advanced by paper activity at all.** The book contributes nothing, and the write path now stamps
`1` in paper going forward — so the counter is pinned at **0/30** for as long as SOL is paper. It
can only ever be moved by a real fill.

Two consequences, both closed:

- **The column is now honest.** Any analysis splitting real from paper on `is_virtual` was
  previously wrong for six rows; it no longer is.
- **A live-mode gate is no longer being driven by paper trades.** It stood at 6/30 on the strength
  of six simulated closes.

---

# §4 — IS THIS INSIDE THE FREEZE? ARGUED, NOT ASSUMED

**Ruling: not freeze-touching. And declining it would have left the freeze *less* protected.**

The freeze covers *everything the advisor reads*, and `news_summary` is an explicitly named frozen
input — so the question is real and worth answering rather than waving through.

**1. It changes nothing the advisor reads today.** The gate feeds the prompt through one line
(`main.py:2239`):

```python
_claude_news = None if _obs_window else _news_summary
```

`_obs_window` was `True` at counter 6/30 and is **still `True`** at 0/30. Verified by evaluating
the function itself after the backfill, not by reasoning about it. **The prompt is byte-identical
before and after.** No frozen value moved.

**2. It changes *when* a frozen input could later appear — in the protective direction.** This is
the part worth being precise about, because it is the operator's own stated hesitation:

- **Unfixed**, paper armed-exit closes keep incrementing a live-mode counter. On reaching 30 the
  entry prompt gains a `Recent news (last 2h):` block — **with no commit, no restart and no
  report.** That is precisely the accidental mid-window prompt change the 17:13:02 window restart
  existed to prevent, arriving by itself.
- **Fixed**, paper can never advance the counter, so **the 200-window is now guaranteed to run on
  a single prompt form.**

**3. Was it actually reachable inside this window?** Honestly: probably not — 24 more paper armed
exits would be needed, and six occurred over roughly six weeks, against a window that should close
in days. But *unlikely* is not *impossible*, and the fix removes the possibility rather than
betting on it.

**Storage and labels are explicitly in the NOT-FROZEN list.** This change is a column value in a
storage table. It is out of the frozen surface by the freeze's own wording, and its only effect on
the frozen surface is to make it more stable.

The same ruling is recorded inside the freeze section of `OPEN-ITEMS-SOL.md`, next to the scope it
interprets.

---

# §5 — WHAT I DID NOT TOUCH

Per instruction, and verified:

- **`FUNDING_NEWS_OBSERVATION_TRADES` — unchanged at 30** (`config.py:209`).
- **The news path — untouched.** `fetch_recent_headlines`, `build_news_context`,
  `is_in_funding_news_observation` itself: no edits.
- **All six management mechanisms from the 17:46 study §2 — untouched.** No change to
  partial-at-arm, the post-entry recheck, the SL tighten, excursion sampling, the smart-exit
  dryrun, or water_mark/MAE.
- **The entry prompt and everything feeding it — untouched.** `AI_ADVISOR_HIDE_1H` still `False`,
  `claude_advisor.py` unmodified since 16:15:42.

Diff surface for this change: **one file, one function, one added kwarg**, plus six UPDATEd column
values and documentation.

---

# §6 — THE COMPLICATION I CHECKED BEFORE APPLYING

The brief did not anticipate this, and it is the one thing that could have made the backfill
harmful. **Each armed exit wrote two rows for the same close:**

| id | signal_type | is_virtual (before) | order_id | price | amount | pnl |
|---|---|---|---|---|---|---|
| 2148 | `15m_armed_exit` | 0 | `VIRT-CLOSE-7` | 74.57 | 140.8 | +494.2006 |
| 2149 | `exit_long` | 1 | `VIRT-CLOSE-7` | 74.57 | 140.8 | +494.2006 |

…and identically for the other five. `_execute_armed_exit` writes its own row **and**
`_execute_close_position` → `_virtual_close_for_side` → `virtual_trader.close_position` writes the
VIRT-CLOSE row. Same close, recorded twice, ~$555 of PnL in the pair.

So relabelling puts six paper closes **twice** inside the `is_virtual=1` population. I checked
every reader before proceeding:

| reader | reads `is_virtual`? | affected? |
|---|---|---|
| `is_in_funding_news_observation` | yes, `=0` | ✅ **this is the intended target** — 6 → 0 |
| `mercury_sol_prior_move_logger:107` | yes, `=1` | ❌ no — it also filters `signal_type IN ('open_long','open_short')`, which armed-exit rows can never match |
| `optimizer.pair_trades` | **no** — `SELECT * FROM trades` | ❌ no. And it cannot double-count: `15m_armed_exit` is in `_AMBIGUOUS_CLOSE_TYPES` and arrives **first by id**, so it pops the open; the sibling `exit_*` row then finds `open_pos` empty and is dropped |
| `virtual_trader._cumulative_closed_pnl` | no — reads `virtual_positions.net_pnl` | ❌ no |
| `_check_daily_loss_breaker` | **no `is_virtual` filter at all** — sums `trades.pnl WHERE exchange='bybit'` | ❌ unaffected **either way** |

**Conclusion: the relabel introduces no double-counting anywhere**, because the only reader that
filters `is_virtual=1` excludes these rows by `signal_type`, and the two readers that would sum
their PnL ignore `is_virtual` entirely.

🔴 **But two pre-existing defects are now on the record, neither introduced nor fixed here:**

1. **The duplicate row itself.** Every armed exit is stored twice. It has been true since
   2026-06-15 and survives this change untouched.
2. **`_check_daily_loss_breaker` already double-counts those six days**, because it sums
   `trades.pnl` with no `is_virtual` filter and both sibling rows carry the full PnL. That is a
   **risk gate** reading inflated daily loss/profit on six historical days. It is out of scope
   here — but it is a risk gate, and it should not stay unexamined.

---

# §7 — 🔶 THE PARTIAL-AT-ARM ⅓ LEG FIRED FOR THE FIRST TIME

Unrelated to this fix, but it happened during it and belongs in the record. **vpos 25 armed and
took its partial at 17:34:57** — the first execution of the mechanism applied at 15:38:

```
[PARTIAL] vpos=25 realised 0.3333 (45.96666666666667) @ 71.7 pnl=+31.7495 fees=3.6449
          — remainder 91.93333333333334 rides the UNCHANGED trail
[VIRTUAL] BE-LOCK vpos=25 SHORT SL→72.32506 (trail armed)
```

| field | value |
|---|---|
| size | 137.9 → **91.9333** (exactly ⅔) |
| `partial_size` / `partial_price` | 45.9667 @ **$71.70** |
| `partial_pnl` / `partial_fees` | **+$31.75** / $3.64 |
| `partial_at` | 2026-08-01T17:34:57 |
| SL | moved to breakeven **72.32506** |
| `mgmt_state_json` | `{"breakeven_applied": true, "partial_done": true}` |
| `water_mark` | 71.60 |

The contract held exactly as designed: ⅓ realised at the +1R arm, remainder on the **unchanged**
trail, `initial_risk_usdt` untouched so R stays comparable to the 18 prior positions. **The
mechanism is now proven in execution, not just in code** — the caveat carried in every report
since 15:44 is discharged.

**And note what §8 of the 17:46 study said about this leg going live:** at $100 notional the ⅓
would be **0.43333 SOL against a 0.1 lot step** — invalid. Here at paper size it is 45.9667, which
is equally step-invalid but harmless because no order is placed. This firing is a clean
demonstration of the paper/live divergence that study flagged.

---

# §8 — STATE VERIFICATION, POST-RESTART

Restarted deliberately at **18:01:55**; worker **pid 1138867**.

| check | result |
|---|---|
| Service / worker | **active**; master 1138809, worker **1138867 forked 18:01:55** |
| **`OBSERVATION_MODE`** | **True — proven live in the NEW pid**: `[VIRTUAL] poller started in pid 1138867`, whose alternative branch prints `poller not started (live mode)` and returns. **SOL is PAPER.** |
| Fixed code loaded | `main.py` mtime **18:00:08**, predating the 18:01:55 fork ✅ |
| Other sources unchanged | `config.py` 17:12:14, `claude_advisor.py` 16:15:42, `virtual_trader.py` 15:34:21 — all predate the fork, none edited |
| `py_compile` | **OK** on `main.py`, `config.py`, `claude_advisor.py`, `virtual_trader.py` |
| **200-window NOT reset** | **1 of 200**, measured before *and* after the restart. The window is defined by `timestamp >= 17:13:02`, so a restart cannot move it |
| Prompt form unchanged | `AI_ADVISOR_HIDE_1H = False` — same final form as 17:13:02. **This restart did not create a second orphan set**, because the prompt did not change |
| News counter | **0** |
| **vpos 25 intact** | ✅ reconciled at boot: `[VPOS-RECONCILE] OPEN vpos=25 SHORT entry=72.47 sl=72.32506 age=0.7h — poller continues managing it (no auto-close)` |
| DB integrity | `PRAGMA quick_check` → **ok** |
| **Tor → Bybit** | ✅ `{"retCode":0,"retMsg":"OK","timeSecond":"1785607344"}` |
| **OKX book** | ✅ live, mid ≈ **$71.725** |

**Titan — untouched:**

| check | result |
|---|---|
| `git status --short` | **clean** |
| `HEAD` | **`3316e8a`** |
| `titan.service` | **active** |
| `.py` modified since 16:00 under `/root/titan-bot` | **none** |

---

# WHAT IS NOW OPEN

1. **The duplicate armed-exit row** (§6) — every armed exit stored twice since 2026-06-15.
2. **`_check_daily_loss_breaker` double-counting those six days** (§6) — a *risk gate* reading
   inflated numbers. Out of scope today; flagged because of what it is.
3. **The window** — 1 of 200, prompt form final and stable, and now provably unable to change by
   itself.
