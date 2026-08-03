# titan book sources applied on okx-4000 plus the non-advisor entry path finding

_2026-08-03 14:37 UTC_

---

# TITAN — BOOK SOURCES APPLIED, LIVE, `34dbdbf` · AND A FINDING ON THE NON-ADVISOR ENTRY PATH

_2026-08-03 14:35 UTC · HEAD `34dbdbf` (was `a85733f`) · LIVE, real money, **flat** · 4 files, +177/−15_

---

## DECISION LINE

**Applied, restarted deliberately, every confirmation green.** The book that decides is now the book
that is stored, learned from and rechecked. `trades.advisor_book_json` holds the OKX-4000 dict the
advisor was handed — the **same object**, threaded down, never re-fetched. The learning loop reads
it. The recheck's baseline and refresh moved to OKX-4000 **together**, with **no substitute venue**
on failure.

**Both prompts verified byte-identical by md5**, before and after. The §2.4 window is not reset.

🔴 **And the `webhook()` question is a finding, not a footnote — but the reassuring half is
measurable and the worrying half is structural.**

- **(a) Zero.** Of the 65 positions in the book, **0** came through the non-advisor path — all 65
  carry `ai_decision='execute'` (59 paper, 6 live). Widening to every executed row ever: **exactly
  one entry** in Titan's history executed with no advisor verdict — **trade 181, 2026-05-11 21:13**,
  and it **predates `virtual_positions` entirely** (earliest position row: 2026-05-17). The other 7
  advisor-less executed rows are `15m_armed_exit` close legs, not entries.
- **(b) It bypasses the advisor, but it is not ungoverned — and yes, entries CAN execute without
  it.** `webhook()` never calls `consult_for_entry`, but it *delegates* to `_handle_state_machine`,
  which does. The legacy block is reached only by falling past **12 early returns**. What survives
  there: the **confluence score gate**, the **risk halt**, and **skip attribution**. What does not:
  the **entry advisor**, and any **OKX book fetch**.
- **(c) Not reachable by anything TradingView actually sends.** Every `task` value in the retained
  journal — `price_action` (1067), `confirmation` (107), `exit` (2), `trend_catch` (1), `signal` (1)
  — maps to a handler that returns first. It is legacy, **but it is not dead code**: a payload with
  an unrecognised `task` and an `action` outside `ACTION_TO_SLOT` still lands there.

**Reported, not changed, as instructed.**

---

# 1. APPLIED

## 1.1 Snapshot first

```
DB   trades.db.bak_booksrc_20260803   65,286,144 bytes   PRAGMA integrity_check: ok
     (SQLite .backup() — atomic; cp on a live DB can catch a partial write)
     pre-patch: entry_okx_wall_baseline_mult present? False | advisor_book_json present? False
     65 virtual_positions rows · 20,070 trades rows

FILES main.py / virtual_trader.py / signal_weights.py / sensor_events.py
      -> *.bak_booksrc_20260803  (cp -p, mtimes preserved)
```

Pre-flight: **flat** — no open position, so the restart was unconditionally safe.

## 1.2 Apply · compile · restart

```
git apply /tmp/titan-book-sources.patch      ->  ✅ applied
git diff --numstat                           ->  main.py 63/3 · virtual_trader.py 79/10
                                                 signal_weights.py 23/1 · sensor_events.py 12/1
                                                 = 4 files, +177 / -15   ✅ exactly as stated
python3 -m py_compile   x4                   ->  OK, OK, OK, OK
import smoke test       x4                   ->  OK (sensor_events, signal_weights,
                                                 virtual_trader, claude_advisor)
commit 34dbdbf
systemctl restart titan.service              ->  14:31:57 UTC, deliberate, from flat
```

**Four boot gates green:**

```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY   LIVE_TRADING_ENABLED = True · ORDER_ADAPTER_LIVE = True
[TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree: 0 exchange position(s), 0 open row(s)
[STOP-CLEANUP] no orphaned orders for LONG · no orphaned orders for SHORT
[RECONCILE] done
[TITAN][OB-DENSITY] ctVal=0.01 BTC/contract read from OKX instrument spec   <- from the SPEC
```

Zero errors, zero tracebacks since the restart.

---

# 2. THE CONFIRMATION SET

| # | confirmation | result |
|---|---|---|
| **1** | 4 files, +177/−15 | ✅ `main.py` 63/3 · `virtual_trader.py` 79/10 · `signal_weights.py` 23/1 · `sensor_events.py` 12/1 |
| **2** | the new columns exist | ✅ `virtual_positions.entry_okx_wall_baseline_mult`, `.entry_book_src`, `trades.advisor_book_json`, `recheck_events.book_src` |
| **3** | NULL on all legacy rows, not backfilled | ✅ `entry_okx_wall_baseline_mult` NULL on **65/65** · `entry_book_src` NULL on **65/65** · `recheck_events.book_src` NULL on **50/50** · `advisor_book_json` non-NULL on **0** (no advisor consult since the restart yet) |
| **4** | recheck refuses on legacy rows, no BingX fallback | ✅ see 2.1 below |
| **5** | failed OKX read → `book_unavailable`, distinguishable from a pass | ✅ see 2.2 below |
| **6** | `entry_sup_wall_mult` / `entry_ob_imbalance` still BingX, unchanged | ✅ **0 of 65** rows differ. vpos 91 still reads `sup 4.8, imb 0.0939, baseline 20.0` |
| **7** | entry prompt byte-identical | ✅ md5 `450de1a7…` before **and** after |
| **8** | close prompt byte-identical | ✅ md5 `98d7f191…` before **and** after |
| **9** | §2.4 window not reset | ✅ nothing the close prompt reads changed — see 2.3 |
| **10** | four boot gates green | ✅ above |
| **11** | flat / open position untouched | ✅ **flat** before, during and after |

**Bonus check nobody asked for but which the migration made necessary:** a full-table diff of
`virtual_positions`, `signal_weights`, `hyperwave_weights` and `recheck_events` against the
pre-patch snapshot, on every pre-existing column — **0 rows differ in any of the four tables**
(65 · 52 · 16 · 50 rows compared). The migration added columns and changed **no value**.

## 2.1 The recheck refuses on a legacy row — proven, not asserted

```
vpos 91  entry_okx_wall_baseline_mult = None      (legacy row)
vpos 91  entry_wall_baseline_mult     = 20.0      (BingX — present, and NOT used)

_health_score(...) -> score=-5  verdict=TIGHTEN
details: [{'rule': 'wall_growth', 'value': None,
           'skipped': 'no_okx_baseline_on_this_row', 'points': 0},
          {'rule': 'adx_below_floor', 'value': 18.5, 'threshold': 20.0, 'points': -5, 'window': 200}]
```

**The rule refused, and it SAID SO in the row.** The BingX value sat right there and was not
touched.

## 2.2 A failed read is distinguishable from a pass — and changes nothing

```
book read FAILED         -> score=-5  details=[{'rule':'wall_growth','value':None,
                                                'skipped':'book_unavailable','points':0}, …]
book read OK, ratio fine -> score=-5  details=[…]        (no wall_growth entry)
```

**Same score. Different record.** That is exactly the intent: the rule's weight is 0
(`WALL_GROWTH_*_SCORE`, neutralised 2026-07-13), so this is **analytic hygiene, not a behaviour
change** — and the code comment says so rather than dressing it up.

Verified end-to-end through the real `log_recheck` writer **on a copy of the DB, not production**:

```
tier= 10  cur=  4.7  ratio=1.0086  book_src=okx_books_full_4000
tier= 60  cur= None  ratio=  None  book_src=None
          reasons_json=[{"rule":"wall_growth","value":null,"skipped":"book_unavailable","points":0}, …]
```

⚠️ **One thing I found while confirming, worth stating.** `recheck_events.book_src` did **not**
exist immediately after the restart — `sensor_events._ensure_schema()` is **lazy by design** (the
§2.34 fix put the migration at the top of each public writer), so the column is created by the first
`log_recheck` call. No recheck had run because no position had opened. I did not assume it would
work: I invoked the bot's own `_ensure_schema()` — idempotent, touches only sensor_events' tables —
and confirmed the column appears, then proved the insert path end-to-end on a copy. **The column now
exists ahead of the first live recheck rather than being created during one.**

## 2.3 Why the §2.4 window is intact

Both prompts rebuilt from **fixed inputs** with the API stubbed, before and after the patch:

```
entry prompt : 450de1a77a99deaf676f8a7347a35835   (before)  ==  450de1a77a99deaf676f8a7347a35835   (after)
close prompt : 98d7f1911bab03e0a14046481bd9f2d3   (before)  ==  98d7f1911bab03e0a14046481bd9f2d3   (after)
```

And the structural reason, which is the one that matters: `entry_wall_baseline_mult` is **not in the
close prompt's read list**, while `entry_sup_wall_mult` and `entry_ob_imbalance` **are** — and the
patch leaves those two untouched, keeping the BingX depth-100 fetch alive for the sole purpose of
feeding them. **The window is not voided and needs no restatement.**

---

# 3. 🔴 THE FINDING — THE NON-ADVISOR ENTRY PATH

## 3a. How many entries came through it — split by era

**Discriminator:** both advisor handlers stamp `ai_decision`; the legacy block never calls the
advisor, so an entry that went through it has `ai_decision IS NULL`.

| era | route | positions |
|---|---|---:|
| PAPER | `ai_decision = 'execute'` | **59** |
| LIVE | `ai_decision = 'execute'` | **6** |
| either | **no advisor** | **0** |

```
positions with an entry row      : 65     of which NO ADVISOR : 0
positions with NO entry row      : 0      (nothing unlinkable)
```

Widening past `virtual_positions` to **every executed trades row ever** — 73 rows, 65 with an
advisor verdict and 8 without:

| row | when | what it is |
|---|---|---|
| **181** | 2026-05-11 21:13:07 | 🔴 **a real ENTRY** — `open_long`, real exchange order `2053946534144471040`, no advisor verdict |
| 186 | 2026-05-11 21:18:16 | its close leg |
| 7726 · 11622 · 12961 · 15955 · 16373 · 19461 | 2026-06-13 → 2026-07-29 | `15m_armed_exit` **close legs** (`VIRT-CLOSE-*`) — not entries |

**So: exactly one entry in Titan's entire history executed without the advisor, and it predates the
engine.** The earliest `virtual_positions` row is **2026-05-17T06:40:10**; trade 181 is from
**2026-05-11**. **Zero since.** No live-era entry has ever taken that path.

## 3b. Does it bypass the advisor entirely, or reach it another way?

**Both, depending on the branch — and this is the part worth knowing independently of the book.**

```
webhook()  @4213
  ├─ plain text (?tf= and no JSON body)        -> _handle_plain_text_signal   RETURNS
  ├─ task in _DIRECT_TASKS ('exit')            -> _handle_exit_signal         RETURNS
  ├─ task mapped via _TASK_TO_ACTION           -> _handle_state_machine       RETURNS  ← consults the advisor
  ├─ action in state_machine.ACTION_TO_SLOT    -> _handle_state_machine       RETURNS  ← consults the advisor
  └─ …falls past 12 early returns…
       └─ legacy block @4421  if is_close: …  else: _execute_entry(...)  @4510   ← NO ADVISOR
```

`webhook()` **never calls `consult_for_entry` itself** (AST-verified), but it **delegates** to
`_handle_state_machine`, which does. So the advisor is reached on the normal routes and skipped only
on the fall-through.

🔴 **Entries can execute without the advisor ever being consulted. That is real.** What that path
still has, and what it does not:

| guard | on the legacy path |
|---|---|
| confluence score gate (`_gated_score` vs `_eff_thr`) | ✅ present |
| risk halt | ✅ present |
| skip attribution | ✅ present |
| position cap / one-open-per-side | ✅ present (inside `_execute_entry`) |
| **entry advisor** | 🔴 **absent** |
| **OKX book fetch** | 🔴 **absent** — which is why this patch leaves its columns NULL |
| **recheck wall baseline** (after this patch) | 🔴 **absent → the rule refuses.** Correct behaviour |

So it is **not ungoverned** — it is gated and risk-checked — but it is **unadvised**, and now
visibly **unbooked**.

## 3c. Is it live-reachable today?

**Not by anything TradingView actually sends.** Every `task` observed in the retained journal routes
to a handler that returns first:

| task | occurrences | routes to |
|---|---:|---|
| `price_action` | 1067 | `_handle_state_machine` (via `_TASK_TO_ACTION → execute_trade`) |
| `confirmation` | 107 | `_handle_state_machine` (`→ context_update`) |
| `exit` | 2 | `_handle_exit_signal` |
| `trend_catch` | 1 | `_handle_state_machine` (`→ context_update`) |
| `signal` | 1 | `_handle_state_machine` (`→ context_update`) |

**Legacy, but not dead.** It is reachable by a payload with an unrecognised `task` **and** an
`action` outside `ACTION_TO_SLOT` **and** no plain-text body. Nothing sends that shape today — but
the only thing standing between a malformed or newly-added alert and an unadvised live entry is the
shape of the incoming JSON. **Reported, not changed.**

---

# 4. THE POST-WINDOW LIST — ONE COUPLED BLOCK

Recorded in **OPEN-ITEMS §2.42** as a single block, because these are now three coupled items plus a
retirement, and doing any of them alone is wrong.

### ① §1d — the exit advisor's OKX-down fallback. **BOTH HALVES TOGETHER.**
Repoint `virtual_positions.entry_sup_wall_mult` and `entry_ob_imbalance` to OKX-4000, **and** change
`_build_exit_context`'s fallback so that when OKX is down it renders **no entry reference at all**
rather than a BingX one. 🔴 **Repointing alone would pair an OKX entry reference against a BingX
"now"** — the cross-source comparison `625fedc` removed from the primary branch. The fallback fires
on ~**5.1%** of AI-path consults, so it is not hypothetical. *Inside the close prompt: needs the
window closed, or an explicit void-and-restate in the same commit.*

### ② §3 — the drifting "at entry" reference.
`main.py:2553-2573` picks the `orderbook_density` row nearest the fill within ±10 min, so once a
post-fill row exists it becomes nearer and the entry number changes **silently and exactly once**.
vpos 91: `−52.3 s` row gave ×4.85 / 0.5517; `+8.7 s` row gave ×4.08 / 0.5584 — first consult said
`entry x4.8 → THINNED`, every later one `entry x4.1 → grew`, and that is the **denominator of the
arrow the advisor reads**. **Fix: bound the search to rows at or BEFORE the fill** — stable *and*
causally honest. *Inside the close prompt.*

### ③ §2.40 / §2.41 — the thresholds and the re-grade, already one decision with two levers.
An **inert** mechanism makes any re-grade **permanent**; a **live** one makes it **revisable**. The
same re-grade is a different act depending on which threshold decision is in force, so they are
taken together or not at all.

### ④ RETIRE `entry_wall_baseline_mult` — **at the same time as ①**.
After this patch it is **written and read by nothing**. Its writer is kept only so the BingX series
stays continuous while ① still depends on the BingX fetch. **Once ① lands, that fetch's last
consumer is gone and the column has no remaining purpose** — drop the writer, and record the column
as historical BingX depth-100 rather than deleting the data.

**Ordering constraint, stated so it is not rediscovered:** ④ cannot precede ①, and ① cannot precede
the window closing. ② is independent of ① but shares the same gate. ③ is independent of both.

---

## WHAT CHANGED, AND WHAT DID NOT

| | |
|---|---|
| **Code** | 4 files, **+177/−15**, commit `34dbdbf`, live since 14:31:57 UTC |
| **DB** | 4 columns added, **0 pre-existing values changed** (verified by full-table diff on 4 tables) |
| **Historical rows** | **not backfilled, not recoverable** — the advisor's book for the 65 existing entries was never stored. Same conclusion SOL reached |
| **Entry prompt / close prompt** | **byte-identical**, md5-verified |
| **§2.4 window** | **not reset, not voided** |
| **Frozen columns** | `entry_sup_wall_mult` / `entry_ob_imbalance` untouched; the BingX fetch kept alive solely to feed them |
| **`entry_wall_baseline_mult`** | still written, **read by nothing** — retirement queued as ④ |
| **The non-advisor path** | **reported, not changed** |
| **§2.41 · ±20/−15 thresholds · §2.39b** | still deferred / as marked |
| **Position** | **flat** throughout |
