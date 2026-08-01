# sol-phase3-preflip-applied

_2026-08-01 21:00 UTC_

---

# MERCURY-SOL — PHASE 3 APPLIED. THE PRE-FLIP LIST IS CLOSED.

All seven items applied in risk order, plus the §5a backfill. Restarted **19:52:34** (worker pid
1166793), **zero tracebacks**. SOL stays **PAPER**. The entry prompt and its inputs are untouched,
**the window was not reset (4 of 200)**, vpos 25 open and byte-identical. Titan untouched.

---

# WHAT SHIPPED

| order | item | change |
|---|---|---|
| 1 | **§1 partial fill on entry** | `_read_entry_fill` — the position is booked from the **venue's** filled size and average price |
| 2 | **§4 stop never re-verified** | every tick, for live rows, off the position object already held — **no network call** |
| 3 | **§5b risk gate** | reads `virtual_positions.net_pnl`, not `trades.pnl` |
| 4 | **§3 trail return** | checked; alerts; **does not** emergency-close |
| 5 | **§2 fee fallback** | modelled + labelled via `_resolve_fee`; new `fee_verified` column |
| 6 | **§5a duplicate row** | write fixed **and** six historical rows backfilled |
| 7 | **§6 arm on failed close** | survives `POS_UNKNOWN`, consumed on success or positive FLAT |
| — | **§7 news gate** | **decision recorded: Option A** — no code |

Files: `main.py`, `virtual_trader.py`. Snapshots `*.bak_phase3_preflip_20260801` (md5-verified),
DB backup `trades.db.bak_pre_5a_backfill_20260801`. `py_compile` clean on all five modules.

---

# §1 — THE ENTRY BOOKS REALITY (rank 1)

`_read_entry_fill(order, symbol, want=…, fallback_px=…)` returns `(filled, average)` from the
venue, or `(None, None)` when it cannot be substantiated. The common path costs **no extra call** —
a Bybit market order returns `filled`/`average` on the order dict; only when they are missing is
the order re-read once.

Three outcomes, all explicit:

| outcome | behaviour |
|---|---|
| **full fill** | as before |
| **partial fill** | `amount` and `fill_price` are replaced by the **filled** values, logged and Telegrammed. Everything downstream — `initial_risk_usdt`, the breakeven level, the partial's ⅓ leg, the close size — now derives from what the account actually holds |
| **unreadable** | 🔴 **refuses to book.** Raises → the existing call-site handler records `status='failed'` and alerts. The alert says plainly *"a position may be OPEN and UNSTOPPED"* |

**Recovery is real, not notional.** An unbooked-but-filled entry is picked up by
`_load_active_positions_from_db`'s adoption path, which reads the exchange at boot and imports a
position that exists with no DB record. **That is the path Phase 2 deliberately kept alive** — it
declines only when the engine already owns the row, which here it does not.

A size can never be guessed. A missing *average price* falls back to the pre-trade ticker — bounded,
and what the code already did — but it is now **logged as a labelled estimate** rather than silent.

---

# §4 — THE STOP IS RE-VERIFIED, AND IT COSTS NOTHING (rank 2)

**Confirmed: no network call added.** The live branch already calls `_live_pos_state()` for the
FLAT check and receives the **position object**; the stop is a *field on it* (B1). The verification
reads `info.stopLoss` off data already in hand.

| exchange state | action |
|---|---|
| **stop present, matches `sl_price`** | nothing |
| **stop present, differs** | re-set via `_move_stop_to`; on failure, alert naming both levels and stating that the wider side is safe, the engine enforces the intended level while running, and a restart reverts protection to the exchange level |
| 🔴 **stop ABSENT** | **restore it.** If the restore fails → **close the position** rather than run naked — the same discipline as the entry fail-safe |

**Interaction A honoured:** §1 landed first, so the `sl_price` this verifies against derives from
the real fill. Verifying a stop against a level computed from a fabricated fill would have been
*confidently wrong*.

---

# §5b — THE BRAKE READS THE LEDGER (rank 3), AND THE CORRECTION IT RESTS ON

```diff
-                "SELECT COALESCE(SUM(pnl), 0) FROM trades "
-                "WHERE pnl IS NOT NULL AND DATE(timestamp) = DATE('now') AND exchange='bybit'"
+                "SELECT COALESCE(SUM(net_pnl), 0) FROM virtual_positions "
+                "WHERE status='closed' AND DATE(closed_at) = DATE('now')"
```

**The correction, on the record.** Both of us said at 18:05 that the double-count's direction was
safe — "a doubled loss halts earlier". **That is false in general**, and 2026-07-16 is the
counterexample: the duplicated armed exit was a **WIN (+$89.00)**, so the brake read **−$56.04
against a true −$145.04** — a *smaller* loss than reality, the direction that **delays** a halt.

**Checked rather than asserted: no historical decision changes.** Equity **$811.90**, 5% =
**$40.60**; all four losing days breach it under both readings. The hazard was real and simply did
not straddle the threshold.

**After the backfill the two sources agree exactly** — the daily-difference query now returns
**zero rows**.

---

# §3 — THE TRAIL RETURN (rank 4)

Checked, and **deliberately not an emergency close**: the stop is the protection, the trail is the
improvement, and closing a correctly-stopped position because an improvement failed is the wrong
trade. The alert says what to do and, more importantly, what *not* to worry about:

> *"The position IS protected — its stop-loss is on the exchange at {sl_price}. What is missing is
> the trail… **No action is required for safety.**"*

The DB still records `trail_pct` as computed, deliberately: in live the engine's own trail
comparison is the backstop, and zeroing it would stop that running too.

---

# §2 — FEES ARE MODELLED AND LABELLED, NEVER SILENTLY ZERO (rank 5)

`_resolve_fee()` returns `(fee, verified)`. Real fee when readable; otherwise the **modelled**
`BYBIT_TAKER_FEE_RATE` fee with a loud log line and `verified=False`. New column
**`fee_verified INTEGER DEFAULT 1`** on `trades` — confirmed present at index 129.

Your reasoning decided it and is recorded in the code: §5b makes `net_pnl` a **risk-gate input**, so
a NULL there is a hole in a safety calculation, while a modelled fee is approximately right *and*
uses the same rate the paper book charges — restoring exactly the comparability the silent zero
destroyed.

---

# §5a — ONE CLOSE, ONE ROW (rank 6), WRITE **AND** BACKFILL

**Write fix:** the armed-exit row is downgraded to a **signal record** — it keeps
`price`/`amount`/`order_id`/provenance and no longer writes `pnl`/`fee`. Leaving `pnl` NULL removes
it from every `SUM(pnl)` reader *and* from `optimizer.pair_trades` (which requires a non-NULL pnl
on a close row), so the sibling VIRT-CLOSE row is the one that pairs — the row the ledger agrees
with.

**Backfill executed** on the fresh backup, guarded by `order_id LIKE 'VIRT-CLOSE-%'` so a genuine
live armed exit could never be caught. **`changes() = 6`.** Prior values, re-recorded here and in
`OPEN-ITEMS-SOL.md` so the change is exactly reversible:

| id | order_id | prior pnl | prior fee |
|---|---|---|---|
| 2148 | VIRT-CLOSE-7 | +494.200607999999 | 5.7747008 |
| 3318 | VIRT-CLOSE-8 | −177.3411265 | 5.40479225 |
| 3507 | VIRT-CLOSE-9 | −58.7116749999992 | 5.472709 |
| 4220 | VIRT-CLOSE-11 | +301.156224650001 | 5.324594 |
| 10309 | VIRT-CLOSE-19 | +89.0011991000013 | 5.4449153 |
| 13716 | VIRT-CLOSE-23 | −93.2432959999992 | 5.544253 |

**Verified after:** rows with `signal_type='15m_armed_exit' AND pnl IS NOT NULL` → **0**; the
trades-vs-ledger daily difference query → **empty**; `optimizer.pair_trades` → **18 positions**,
unchanged; `PRAGMA quick_check` → **ok**. The six ids still exist and still carry their
timestamps, prices and provenance, so the three published reports that cite them remain valid.

---

# §6 — THE ARM SURVIVES A NETWORK FAILURE (rank 7)

The three outcomes were already distinct after Phase 1 (`POS_UNKNOWN` raises, `POS_FLAT` returns
`None`, success returns a dict) — only the arm handling collapsed them. Now:

| outcome | arm |
|---|---|
| close **completed** | consumed |
| positive **FLAT** (nothing to close) | consumed — the arm has no target |
| 🔴 **UNKNOWN** | **preserved**, `status='position_unknown'`, deferred-alert sent |

**No new constant, as you approved.** `arm_exit_pending` already stamps
`expires_at = now + EXIT_PENDING_TTL_MINUTES` and **`EXIT_PENDING_TTL_MINUTES = 360`** (6 h)
already exists, so a preserved arm dies on exactly the same clock as an unfired one. The narrow
change: an arm now survives a Tor hiccup instead of being discarded for a network reason.

---

# TWO BUGS CAUGHT IN MY OWN EDITS

1. **`BYBIT_TAKER_FEE_RATE` was not imported into `main.py`** — `_resolve_fee` would have
   `NameError`d at call time. Found by checking the symbol resolves, not by reading the code.
2. The **name-resolution audit** was re-run across all changed functions after every edit and came
   back **clean** (the earlier `_new_sl` class of bug did not recur).

Both belong to the standing lesson: a name that resolves at *call* time, inside a statement the
compiler accepts.

---

# CONFIRMATION SET

| check | result |
|---|---|
| Service / worker | **active**; master 1166728, worker **1166793 forked 19:52:34** |
| Tracebacks since restart | **0** |
| `py_compile` | ✅ `main.py`, `virtual_trader.py`, `tor_retry.py`, `stop_loss.py`, `config.py` |
| **`fee_verified` column** | ✅ present, `INTEGER DEFAULT 1` |
| **§5a duplicates gone** | ✅ `15m_armed_exit` rows with non-NULL pnl → **0** |
| **trades vs ledger daily diff** | ✅ **empty** — the two sources now agree exactly |
| **optimizer pairing** | ✅ **18** positions, unchanged |
| **brake reads the ledger** | ✅ today's ledger sum = 0 (no closes today) |
| **DB integrity** | ✅ `quick_check` ok |
| **vpos 25 byte-identical** | ✅ `size 91.9333333333333`, `partial_size 45.9666666666667`, `partial_price 71.7`, `partial_pnl 31.7494754499998`, `partial_fees 3.64485788333333`, `partial_at 2026-08-01T17:34:57.241446+00:00`, `sl_price 72.32506`, `initial_risk_usdt 100.667000000001`, `is_paper 1`; reconciled at boot |
| **window not reset** | ✅ **4 of 200**, before and after |
| **entry prompt frozen** | ✅ `AI_ADVISOR_HIDE_1H = False`; `claude_advisor.py` 16:15:42, `config.py` 17:12:14 — untouched by Phase 3 |
| **`OBSERVATION_MODE` proven live in the new pid** | ✅ `[VIRTUAL] poller started in pid 1166793` |
| **engine still single manager** | ✅ `[MONITOR] RETIRED` · `live adapter registered` |
| **Tor → Bybit** | ✅ `{"retCode":0,"retMsg":"OK","timeSecond":"1785614000"}` |
| **OKX book** | ✅ live, mid ≈ **$71.235** |
| **Titan untouched** | ✅ clean · `HEAD 3316e8a` · active · **no `.py` modified** |

---

# §7 — SEQUENCING DECISION RECORDED: **OPTION A**

**The flip waits for the 200-consultation window.** Written into `OPEN-ITEMS-SOL.md` with the
reasoning, so it is not revisited:

- **C** re-creates by choice the exact defect eliminated this afternoon — the window was restarted
  at 17:13 specifically to stop it straddling two prompt forms, and letting that happen *by itself*
  is worse, not better.
- **B** disarms a designed safety behind a constant someone must remember to unpin — and **three
  "flag on, condition unreachable" defects were found in this codebase in two days.**
- **A** costs only time, and the window is days rather than weeks.

If the window turns out to be weeks, I will raise it rather than let it drift.

---

# 🔶 RECORDED, NOT CHANGED: THE BRAKE IS MIS-CALIBRATED IN BOTH DIRECTIONS

Computed from the 19 real positions rather than estimated:

| | notional | avg 1R | stop-outs before the day halts |
|---|---|---|---|
| **PAPER (now)** | $10,000 | **$213.86** | 🔴 **0.19** |
| **LIVE (intended)** | $100 | **$2.14** | 🔴 **19.0** |

Equity **$811.90**, limit **$40.60**. Average `initial_risk_usdt` **$213.86** (min $100.67, max
$393.21) = **2.139% of notional**. **289 `risk_halt` rows** in the book.

**Paper is worse than we thought: at 0.19, the brake halts the day before a single losing trade
completes.** Your ~13 for live was the right order of magnitude; the measured figure on the actual
1R distribution is **19**. Either way the conclusion holds — one constant, ~100× too tight in
paper and far too loose in live, in opposite directions.

**Not changed. Recorded as the next item after Phase 3, to be decided before the flip.**

---

# WHERE THIS LEAVES THE FLIP

The pre-flip list from the 20:00 Phase 2 report **§6 is now empty** except the two things that were
never code: the **sequencing decision** (settled — Option A) and the **brake calibration**
(recorded, awaiting your decision).

**SOL is still PAPER and still cannot place an order.** Phase 1 fixed the semantics, Phase 2
unified the manager, Phase 3 closed the protections that were believed-in but absent. What remains
before a flip is a decision about the brake and the completion of a 200-consultation window — not
code.
