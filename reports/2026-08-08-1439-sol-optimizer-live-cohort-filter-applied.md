# sol-optimizer-live-cohort-filter-applied

_2026-08-08 14:39 UTC_

---

# Mercury-SOL — the optimizer's live-mode cohort now has a live-only filter

**Applied and proved by executing the real `optimizer` code against an isolated copy.
On today's book the live cohort is 0 (was 21 — twenty-one PAPER pairs the old live branch
would have handed to `find_worst_segment`). With one closed live position injected, the new
cohort is exactly 1 and the 20 paper pairs are excluded. Zero production leaks. The weight
path is untouched. Titan was not touched.**

Prior: [measurement 14:17](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1417-sol-paper-weights-measured-not-in-the-gate.md)

---

## 1. THE PREDICATE — `virtual_positions.COALESCE(is_paper,1)=0`, and NOT the other two

You were right that one of them lies. Here is which, and why the third candidate is a trap.

### ❌ `trades.is_virtual` — lies in the DANGEROUS direction

Declared `INTEGER DEFAULT 0` (`main.py:759`). So **`0` means "this was live" OR "nobody stamped
it"** — two different claims sharing one value. 16,718 of 16,775 rows sit at 0.

That hole has already been paid for once. `main.py:4593` records six PAPER armed-exit closes
(rows 2148/3318/3507/4220/10309/13716) that took the default and were **stored labelled REAL**,
which advanced a LIVE-mode gate off paper trades. Using `is_virtual == 0` as a positive live
marker re-opens exactly that: an unstamped paper row silently joins the **live** cohort.

### ❌ Titan's `stop_order_id IS NOT NULL` — structurally unavailable here

Titan's `live_entry_row_ids()` splits on `virtual_positions.stop_order_id IS NOT NULL` ("paper rows
leave it NULL because the poller owns the stop there; a live row carries the exchange STOP_MARKET
id"). **SOL's `virtual_positions` has no such column** — verified against the live schema, the only
paper/live column is `is_paper` — and it cannot meaningfully get one: after B1, SOL's stop is a
**position-level `trading_stop` attribute** (`tpslMode='Full'`), not a conditional order, so a live
SOL position has no stop-order id to record. Porting Titan's line would have classified **every**
SOL live row as paper — a filter that looks right and inverts the answer.

### ✅ `virtual_positions.COALESCE(is_paper,1)=0` — fails SAFE, and is already this codebase's answer

- Declared `DEFAULT 1`, so an **unstamped row is PAPER and is EXCLUDED**. The failure direction is
  the conservative one.
- It is the predicate this codebase already settled on: the daily-loss brake was moved onto
  `virtual_positions` filtered by `COALESCE(is_paper,1)=?` on 2026-08-05, and **M7** (`main.py:1610`)
  names the loss-streak gate's failure to follow it as *the* defect. Same book, same filter, one
  answer to "was this real money".
- Join key `trades_entry_row_id` is populated on **22 of 22** closed rows.

```python
def live_entry_row_ids():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            return {r[0] for r in conn.execute(
                "SELECT trades_entry_row_id FROM virtual_positions "
                "WHERE status='closed' AND COALESCE(is_paper,1)=0 "
                "AND trades_entry_row_id IS NOT NULL")}
    except Exception:
        # Fail CLOSED: an unreadable ledger yields an EMPTY live set ...
        return set()
```

The cohort:

```python
     else:
-        cohort = [(o, c) for (o, c) in paired
-                  if (_safe_get(o, 'id') or 0) > cycle_start_id]
+        _live_ids = live_entry_row_ids()
+        cohort = [(o, c) for (o, c) in paired
+                  if (_safe_get(o, 'id') or 0) > cycle_start_id
+                  and (_safe_get(o, 'id') or 0) in _live_ids]
```

---

## 2. THE EXPIRED COMMENT AT :101 — CORRECTED IN THE SAME EDIT

It claimed coverage resting on *"SOL runs in OBSERVATION_MODE"*. Replaced with what the coverage
**actually is**, and with the distinction that made the old text read as protection it never gave:

- the seven venue-exit labels are gated by `virtual_trader._is_paper` (`virtual_trader.py:2182`) —
  a real gate, **independent of OBSERVATION_MODE** — but it decides which **label** a close gets,
  **not which rows are learned from**. It never covered a cohort.
- the **cohort** is filtered separately, in `main()`, by `live_entry_row_ids()`. Before today the
  live branch had **no such filter at all**.

---

## 3. AT n=0 IT DOES NOT GO QUIET — CONFIRMED, PLUS A LABEL FIX

**Confirmed: it already reported rather than falling silent.** The `accum_n < target` branch is
n=0-safe by construction (`wr = (wins/n*100) if n else 0.0`, and the W/L and money lines sit behind
`if n:`). No division by zero, no paper numbers presented as the cohort's.

What was wrong was the **label**: in live mode it printed *"Optimizer: Observation M."* — a mode
SOL left at 22:25 yesterday — above a paper-trained weight block, which invites reading those
weights as this cohort's evidence. Executed output of the new path at n=0:

```
⏳ Optimizer: insufficient LIVE data
Closed LIVE trades: 0/30
No closed live position has been booked yet — nothing to analyse. No proposal can be made from paper rows.
Accumulating data — no analysis yet.
```

and when a weight block is attached, it now carries `⚠️ The weight block below is trained on the
FULL all-time paired set (paper-dominated), NOT on the live cohort counted above.` The
`optimizer_runs` row records `mode='live_accum'`, `notes='insufficient live data'`.

---

## 4. 🔴 THE APPLY-GUARD DOES NOT EXIST IN SOL

You asked me to confirm it still refuses. **It is not there.** `optimizer_listener.apply_proposal`
has no paper/live check of any kind — `grep -niE "paper|is_virtual|is_paper|dominat|refus"` over
`optimizer_listener.py` returns only two incidental comment hits. And `save_proposal` stamps **no
cohort provenance**, so the listener could not check even if it wanted to.

The 2026-08-06 guard you are remembering is **Titan's** (commit 897850b). Titan has
`_evidence_ok()` refusing unless a proposal carries a live/paper evidence block, refusing outright
when the block is **missing** (fail-closed), and testing **both** row share and dollar share —
because, in its own words, *"a segment can be majority-live by row count and still be 99% paper by
dollars"*. SOL has none of that.

**Its predicate does not depend on OBSERVATION_MODE** — it reads the evidence block on the proposal
— so the answer to that half is "no", but for SOL the question is moot until the guard exists.

What today's fix does instead is close the hole **at the source**: the cohort is now live-only by
construction, so any proposal SOL saves is derived from live pairs only and `paper_pairs` is 0 by
definition. That is the primary defence. Titan's listener guard is the **second** line, and SOL is
still missing it — flagging, not building, since you scoped this pass to the cohort.

---

## 5. WEIGHT PATH — UNTOUCHED, PROVEN

```
compute_weight_updates : bak=3 now=3  SAME
save_weights           : bak=1 now=1  SAME
load_weights           : bak=1 now=1  SAME
weight_engine          : bak=8 now=8  SAME
weight_engine.py                  md5 480fa431f1aa792b09c64fb74c2e1208  (not edited)
optimizer/dynamic_weights.json    md5 0e2b431eed073a1285714ab258e538cb  mtime 14:00 (untouched)
mercury-sol-optimizer.timer       active — left exactly as it was
```

---

## PROOF BY EXECUTION — 17 VECTORS, NOT 14

🔴 **The isolation census has grown.** `grep -l "mercury-sol/trades.db" *.py` finds **13** files.
The prod-*directory* literal appears in **16**, and the three the narrower grep misses are
`healthcheck.py`, `mercury_sol_prior_move_logger.py` and — the one that matters —
**`weight_engine.py`, which holds `WEIGHTS_PATH` to the production `dynamic_weights.json`.**
A test run of `optimizer.main()` isolated only by the `trades.db` grep would have **written
production weights** — the precise §5 violation this pass forbids. With `.env` that is **17
vectors**. Searching by DB filename is not enough; search by the directory.

Isolation built structurally, three layers plus a lock:

```
tree under test = COPY; prod path never in sys.path
all 16 .py + .env rewritten   -> remaining prod-path literals in the lab: 0
sys.dont_write_bytecode = True
LOCK on sqlite3.connect AND on open() in write modes -> AssertionError on any prod path
```

Executed result (real `optimizer.pair_trades`, `_get_cycle_start_id`, `live_entry_row_ids`,
`fmt_report`):

```
config.OBSERVATION_MODE = False   (live mode = True)
optimizer.DB_PATH          = <lab>/trades.db
weight_engine.WEIGHTS_PATH = <lab>/optimizer/dynamic_weights.json

A) TODAY'S REAL BOOK (0 closed live positions)
   all paired pairs      : 22        cycle_start_id: 2325
   live_entry_row_ids()  : EMPTY
   OLD live branch (no filter) -> cohort n = 21   <-- the defect
   NEW live branch (is_paper=0) -> cohort n = 0

B) SAME BOOK, ONE CLOSED **LIVE** POSITION  (lab-only flip of vpos id=28 -> is_paper=0)
   live_entry_row_ids()  : [16405]
   OLD live branch -> cohort n = 21   <-- 20 of them PAPER at ~103x notional
   NEW live branch -> cohort n = 1    <-- exactly the live pair, entry row 16405

C) FAIL-CLOSED: live_entry_row_ids() on an unreadable ledger -> set()

=== ISOLATION VERDICT: prod leaks = 0 (none) ===
ALL ASSERTIONS PASSED
```

**A is the whole point:** today, on the real book, the old live branch yields **21 paper pairs**.
Nine short of the 30 threshold. The next nine paper closes would have tripped a live filter
proposal built entirely from paper dollars.

`py_compile` clean; `.pyc` header records source mtime 14:32:04 = `optimizer.py` mtime — MATCH.
Backup `optimizer.py.bak_livecohort_20260808_142638`, md5-verified against the pre-edit file.
`diff` vs backup: 105 added, **11 removed** — all 11 accounted for (4 comment lines, the signature,
the message header, the cohort line, the `fmt_report` call, 2 `_record_optimizer_run` lines).

---

## DEPLOYMENT — NO RESTART NEEDED, AND WHY

The optimizer runs as a **oneshot service from a timer**, i.e. a fresh `python3 optimizer.py` each
firing, so the change is live at the next run: **2026-08-09 14:00:00 UTC**. `main.py` imports
`optimizer` lazily (`main.py:3631`) and uses **only** the `_bucket_*` helpers, none of which were
touched — so the running worker's in-memory copy being stale changes nothing. I did not restart.

## STATE

```
venue   LONG 1.3 @ 74.80  stopLoss 73.89  openTime 1786179014459 — UNCHANGED
        conditional Untriggered 73.89 qty 1.3.  An optimizer edit cannot reach it:
        nothing in optimizer.py or its call graph places, cancels or modifies an order.
mercury-sol               active     (not restarted)
mercury-sol-optimizer.timer active   (untouched; next 2026-08-09 14:00 UTC)
titan                     active / enabled — NOT TOUCHED, /root/titan-bot/optimizer.py mtime
                          still 2026-08-06T01:49 (read only, never written)
prod trades.db            16,775 rows, is_paper=0 rows: 0 — the lab flip never reached it
```
