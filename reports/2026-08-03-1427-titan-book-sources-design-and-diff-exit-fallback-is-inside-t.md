# titan book sources design and diff, exit fallback is inside the freeze, nothing applied

_2026-08-03 14:27 UTC_

---

# TITAN — BOOK SOURCES: DESIGN + DIFF. **NOTHING APPLIED.**

_2026-08-03 · HEAD `a85733f` · LIVE, real money, **flat** · patch validated with `git apply --check`, working tree clean_

---

## DECISION LINE

**Design and diff below. Nothing was applied. `git status` is clean and HEAD is unchanged.**

The patch is **4 files, +177 / −15**, validated by `git apply --check` against the real tree — it
applies cleanly and was not applied.

**Freeze check — one of your four items is INSIDE, and I stopped on it:**

| item | verdict |
|---|---|
| **a** · store the OKX book on the row | **OUTSIDE** ✅ — in the patch |
| **b** · point the learning loop at it | **OUTSIDE** ✅ — in the patch |
| **c** · recheck baseline + refresh | **OUTSIDE** ✅ — in the patch, **proven by execution**, not argued |
| **d** · the exit advisor's OKX-down fallback | 🛑 **INSIDE. STOPPED.** Your suspicion is correct |

**(d) in one line:** the fallback renders `vpos.entry_sup_wall_mult` and `vpos.entry_ob_imbalance`
directly into the close prompt. Changing what those columns *contain* changes what the close prompt
*renders*, and §2.4-OP freezes *"any figure rendered into the close prompt."* **So the patch keeps
the BingX depth-100 fetch alive for the sole purpose of feeding those two columns unchanged**, and
adds the OKX baseline as a **new** column beside them. That is the one place the shallow book
survives, and it survives because the freeze says so — not because it is defensible.

**One consequence I am flagging rather than hiding:** after this patch
`virtual_positions.entry_wall_baseline_mult` is **written but read by nothing**. I kept the writer
deliberately (the BingX dict is fetched anyway for the frozen columns, so the extra scalar is free
and keeps that series continuous) — but a write-only column is exactly the kind of thing this
project flags, so it is flagged.

---

# 1. FREEZE CHECK — ARGUED, AND ONE STOP

§2.4-OP, the bullet marked *"SETTLED, do not re-open the definition"*: frozen = **everything the
advisor READS**; not frozen = *"act/hold plumbing, logging, labels, close mechanics, and the entire
entry side."* The enumerating bullet names only close-prompt inputs.

**The complete list of `virtual_positions` fields `_build_exit_context` reads** — extracted
mechanically from `main.py:2493-2790`, not from memory:

```
vpos['id']                      vpos.get('opened_at')            vpos.get('trades_entry_row_id')
vpos['initial_fill_price']      vpos.get('original_sl_price')    vpos.get('water_mark')
vpos['sl_price']                vpos.get('pending_dca_limits')
vpos.get('entry_sup_wall_mult')     <- BingX depth-100, FALLBACK branch only
vpos.get('entry_ob_imbalance')      <- BingX depth-100, FALLBACK branch only
```

🔴 **`entry_wall_baseline_mult` is NOT in that list.** The recheck's baseline column is not read by
the close prompt at all. That single fact is what separates (c) from (d).

### (a) Storing the OKX book — **OUTSIDE**

A new column `trades.advisor_book_json` plus two new `virtual_positions` columns. **Nothing in
`_build_exit_context` or the close template reads any of them** — they do not exist yet, and the
patch adds no reader on the close side. Pure addition; no existing column changes meaning or value.

### (b) The learning loop — **OUTSIDE**

`_attempt_learning` writes `trades.learning_*`. Grep confirms `signal_weights` is the **only writer
and there is no reader anywhere** — established in §2.39b. The close prompt reads none of it.

### (c) The recheck baseline + refresh — **OUTSIDE, and proven rather than asserted**

Two independent checks:

1. **Structural.** `grep recheck` over `main.py:2490-2800` and over all of `claude_advisor.py`
   returns nothing. `recheck_status` is not read by the exit context. `recheck_events` is not read
   by anything close-side.
2. **Behavioural — the one that could have bitten.** The recheck *can* move `sl_price`, and
   `sl_price` **is** read by the close prompt (`Current stop: X -> +N.NNR away`). So the question is
   whether changing the wall SOURCE can change the verdict. **Measured, not assumed** —
   `_health_score` run over seven wall combinations including both `None` cases:

```
   entry_wall=  20.0  cur_wall=  17.8  ->  score  -5   TIGHTEN
   entry_wall=  4.66  cur_wall=   4.7  ->  score  -5   TIGHTEN
   entry_wall=  20.0  cur_wall= 100.0  ->  score  -5   TIGHTEN     <- a 5x wall explosion
   entry_wall=  4.66  cur_wall=   0.1  ->  score  -5   TIGHTEN     <- a 46x collapse
   entry_wall=  None  cur_wall=   4.7  ->  score  -5   TIGHTEN
   entry_wall=  20.0  cur_wall=  None  ->  score  -5   TIGHTEN     <- the OKX-failure path
   entry_wall=  None  cur_wall=  None  ->  score  -5   TIGHTEN
   distinct scores across every combination: {-5}
```

`WALL_GROWTH_CRITICAL_SCORE = 0` and `WALL_GROWTH_WARNING_SCORE = 0` (neutralised 2026-07-13), so
**no wall value can move the score, hence not the verdict, hence not `sl_price`.** The close
prompt's `Current stop` field is untouchable by this change. **OUTSIDE.**

### (d) The exit advisor's OKX-down fallback — 🛑 **INSIDE. NOT TOUCHED.**

`main.py:2600-2618`, the branch taken when `liquidity_zones` returns nothing (**5.1% of AI-path
consults** by the skip-attribution NULL rate):

```python
_bx = microstructure.fetch_pre_trade_walls(exchange, symbol)      # BingX depth-100, live
ctx.update(sup_now=..., opp_now=..., imb_now=_bx.get('imbalance'),
           sup_entry=vpos.get('entry_sup_wall_mult'),             # <- the stored column
           imb_entry=vpos.get('entry_ob_imbalance'),              # <- the stored column
           book_src='BingX depth-100 — RAW, NOT the percentile baseline')
if ctx.get('sup_entry'):
    ctx['sup_trend'] = 'THINNED' if ctx['sup_now'] < ctx['sup_entry'] else 'grew'
...
    ctx['imb_trend'] = 'FLIPPED' if (ctx['imb_entry'] - .5) * (ctx['imb_now'] - .5) < 0 else 'same side'
```

**Repointing those two columns to OKX values would change three rendered fields** — `sup_entry`,
`imb_entry`, and the derived `THINNED/grew` and `FLIPPED/same side` labels — and it would do worse
than change them: it would pair an **OKX entry reference** with a **BingX "now"**, which is the
cross-source comparison `625fedc` removed from the primary branch. The branch is currently
**self-consistent BingX-vs-BingX**, and the comment at `main.py:2540` already says so.

**Both the freeze and correctness point the same way: this waits.** The patch therefore keeps
`microstructure.fetch_pre_trade_walls` in `_execute_entry` **solely** to keep those columns
populated with the same BingX values they have always held.

**What it needs when the window closes:** repoint `entry_sup_wall_mult` / `entry_ob_imbalance` to
OKX **and** change the fallback so that when OKX is down it renders **no entry reference at all**
rather than a BingX one — "could not measure" is the correct output there, exactly as in §2c.

---

# 2. THE CHANGE — 4 files, +177 / −15

`git apply --check`: **applies cleanly.** Patch at `/tmp/titan-book-sources.patch`.

```
 titan-bot/main.py            63 +   3 -
 titan-bot/virtual_trader.py  79 +  10 -
 titan-bot/signal_weights.py  23 +   1 -
 titan-bot/sensor_events.py   12 +   1 -
```

## 2a. Persist the advisor's OKX-4000 book — SOL's shape, deliberately

**`trades.advisor_book_json TEXT`** — the OKX dict handed to `consult_for_entry`, serialised
verbatim, written **once**, on the advisor path, **before any branch** so it lands on execute, skip
and unavailable alike. Nothing overwrites it. `orderbook_json` keeps its meaning and every existing
writer, so **no current reader changes behaviour**.

This is `mercury-sol`'s `advisor_book_json` (2026-08-02) copied on purpose — same defect class, same
remedy, so the two books stay comparable.

🔴 **The stored dict is the SAME OBJECT the advisor was handed, not a re-fetch.** A second fetch
would be a second book, which is the defect itself. That is why `okx_walls` is threaded down through
`_execute_entry` rather than re-read at fill time.

Position identity comes through `virtual_positions.trades_entry_row_id → trades.id`, and the two
scalars the recheck needs at 10 s cadence are denormalised onto the position row so the poller never
parses JSON:

- **`entry_okx_wall_baseline_mult REAL`**
- **`entry_book_src TEXT`** — `'okx_books_full_4000'`, or NULL when no advisor book reached the entry

🔴 **A NEW column, not a repurposing of `entry_wall_baseline_mult`.** That column holds BingX
depth-100 on every row ever written, and silently changing what an existing column *means*
mid-history is the `confluence_score` defect (§0: one column, three quantities). NULL on legacy rows
and **not backfilled**.

**One path deliberately gets nothing:** `webhook()` (`main.py:4157`) calls `_execute_entry` but never
consults the entry advisor and never fetches an OKX book — verified by AST: it never binds
`pre_trade_walls`. It keeps `okx_walls=None`, the columns stay NULL, and the recheck refuses. The
omission is written into the code as a comment so it is visible rather than mysterious.

## 2b. Point the learning loop at it

```python
book_raw = row_dict.get('advisor_book_json') or row_dict.get('orderbook_json')
_book_src = ('okx_books_full_4000' if row_dict.get('advisor_book_json')
             else ('bingx_depth20' if row_dict.get('orderbook_json') else None))
...
if compact_book is not None and _book_src:
    compact_book = dict(compact_book, source=_book_src)
```

Prefer the advisor's book; fall back to `orderbook_json` for rows that predate the column; **and say
which in the prompt**, so a mixed-provenance training set is never silently averaged.

**Shape fit verified by execution against the live OKX book:**

```
OKX dict keys      : depth, imbalance, mid, wall_threshold_mult, walls_ask, walls_bid
BingX-20 dict keys : ask_vol_band, bid_vol_band, imbalance, imbalance_band_pct, mid,
                     spread, top_asks, top_bids, walls_ask, walls_bid
OKX wall entry     : {'price': 63467.5, 'vol': 1024163199.0, 'mult': 8.1}     <- carries `mult`
BingX-20 wall entry: {'price': 62650.5, 'vol': 68.3216}                       <- no `mult`
compact_for_llm(OKX): {"imbalance":0.4034,"spread":null,"walls_bid_count":3,
                       "walls_ask_count":4,"top_wall_bid":{...,"mult":5.5},
                       "top_wall_ask":{...,"mult":8.1}}
```

⚠️ **One field degrades and I am naming it: `spread` is `null`** — `liquidity_zones` does not compute
it. It renders as null exactly as a missing field already does; no other field is affected. In
exchange the OKX walls carry `mult`, which the BingX-20 walls do not — **strictly richer**.

**This is the fix for vpos 91's attribution**: *"Large ask wall (68.32 BTC at 62650.5) … enabling
profitable short exit"* — the advisor's OKX book had **no wall at 62650.5**; its ask walls were ×4.7
at 62,712.50 and ×4.0 at 62,867.50.

## 2c. The recheck — baseline and refresh move **together**, no substitute venue

```python
cur_walls = liquidity_zones.fetch_pre_trade_walls(symbol)     # was microstructure (BingX-100)
_book_ok  = cur_walls is not None
entry_wall_mult = row['entry_okx_wall_baseline_mult']          # OKX only; NO BingX fallback
```

**Both move in the same hunk.** Moving only the refresh would have left an OKX "now" against a BingX
baseline — the mixed comparison just removed from SOL.

🔴 **On OKX failure there is NO substitute.** `liquidity_zones` returns `None`, `cur_wall_mult` stays
`None`, and the wall rule **contributes no signal**. And a failed read is now **distinguishable from
a pass**, which it was not:

```python
if cur_wall_mult is None:
    details.append({'rule': 'wall_growth', 'value': None,
                    'skipped': 'book_unavailable', 'points': 0})
elif entry_wall_mult is None:
    details.append({'rule': 'wall_growth', 'value': None,
                    'skipped': 'no_okx_baseline_on_this_row', 'points': 0})
```

Plus the log line: `wall=None/None (BOOK UNAVAILABLE — rule skipped)`, and a new
`recheck_events.book_src` column so provenance travels with the figure rather than living in the
code.

**As you asked me to say plainly: the wall rule's score weight is already 0, so this changes no
verdict and moves no stop. It is analytic hygiene, not a behaviour change** — and the code comment
says exactly that rather than dressing it up.

**Legacy rows:** `entry_okx_wall_baseline_mult` is NULL on all 65 existing rows, so the wall rule
refuses on them rather than falling back to the BingX column. Refusing is the point.

## 2d. The BingX-20 capture — kept, with SOL's justification and SOL's lapse condition

**Titan's has the same justification, and one more.**

1. **The tape half has no OKX equivalent.** `microstructure.capture_and_persist_sync` writes
   `orderbook_json` **and** `tape_json` from one call. The tape is L3 — whale detection, aggressor
   pressure, `buy_share_window` — and `liquidity_zones` fetches books only. Killing the capture
   would kill the tape.
2. **It records the venue we actually trade on**, which is a real thing to have.
3. **Titan-specific:** the same BingX fetch also populates `entry_sup_wall_mult` /
   `entry_ob_imbalance`, which the frozen exit fallback reads (§1d). It **cannot** be removed until
   the window closes even if we wanted to.

**KEPT, with the same lapse condition, stated as a rule and not a hope:** it is archival and
operator-display only. Its Telegram line is already labelled *"BingX top-20, raw (no baseline · not
the advisor's book · context only)"*. **After this patch its book half feeds no decision at all** —
the learning loop moves to the advisor's book. 🔴 **If it ever feeds a decision again, the rule
applies again and it must be re-argued, not inherited.**

## 2e. Two lying labels fixed in passing

`virtual_trader.py` carried two comments naming `microstructure.fetch_pre_trade_walls`: the module
header (describing the recheck — true until this patch) and the smart-exit sampler's column comment
(**never true** — that sampler has always used OKX; only the label was wrong). Both corrected. The
now-unused `import microstructure` is removed — verified zero references remain outside comments.

---

# 3. RECORD, DO NOT FIX — THE EXIT ADVISOR'S "AT ENTRY" REFERENCE DRIFTS

**Inside the close prompt. Waits for the window. Recorded with its numbers.**

`main.py:2553-2573` picks the `orderbook_density` row **nearest the fill**, ±10 min. At the first
consult (seconds after the fill) only *pre-fill* rows exist; by the second, a *post-fill* row exists
and is nearer. **The "at entry" number therefore changes exactly once, silently.**

| collector row | Δ to vpos 91's fill | imbalance | max ask wall |
|---|---:|---:|---:|
| 06:39:25.195 | **−52.3 s** | 0.5517 | ×4.85 |
| 06:40:26.228 | **+8.7 s** | 0.5584 | ×4.08 |

| consult | what the prompt said |
|---|---|
| 20921 @ 06:40:23 | `(entry reference sampled 52s from fill)` · `Supporting wall: entry x4.8 -> now x4.7 (THINNED)` · `Imbalance: entry 0.55` |
| 20985 @ 12:41:06 | `(entry reference sampled 8s from fill)` · `Supporting wall: entry x4.1 -> now x6.4 (grew)` · `Imbalance: entry 0.56` |

**Same position, same "entry", a −15% move in the wall reference — and that reference is the
denominator of the `THINNED`/`grew` arrow the advisor reads.** Both rows are OKX-4000, so this is
not a cross-source defect; it is a **moving baseline**.

**The fix when the window allows** (recorded now so it is not re-derived): resolve the entry
reference **once**, at first consult, and persist it — or bound the search to rows at or **before**
the fill so a later row cannot become "nearer". Either makes it stable; the second also makes it
causally honest. **Not in this patch.**

---

# 4. WHAT THE PATCH DOES NOT DO

| | |
|---|---|
| **Applied?** | **NO.** `git status` clean, HEAD `a85733f` unchanged, no DB write, no restart |
| exit advisor's fallback columns | **untouched** — §1d, inside the freeze |
| the §2.4 window | **not voided, not restated** — nothing it reads changes |
| `entry_wall_baseline_mult` | still written, now **read by nothing** — flagged above |
| the entry advisor's prompt | **untouched** — this is storage, learning and recheck only |
| gate / sizing / thresholds | untouched |
| `orderbook_json` / `tape_json` | meaning and writers unchanged |
| historical rows | **not backfilled.** The advisor's book for the 65 existing entries is unrecoverable — it was never stored. Same conclusion SOL reached, and it is stated rather than worked around |
| §2.41 re-grade · ±20/−15 thresholds · §2.39b | all still deferred / as marked |

## Verification done on the unapplied copies

| # | check | result |
|---|---|---|
| 1 | `ast.parse` on all four patched files | ✅ |
| 2 | `git apply --check` against the live tree | ✅ applies cleanly |
| 3 | working tree after generating the patch | ✅ clean, HEAD unchanged |
| 4 | `liquidity_zones` reachable from the recheck | ✅ module-level import (`virtual_trader.py:51`), no function-local shadow |
| 5 | `microstructure` truly unused after removal | ✅ zero references outside comments |
| 6 | wall input cannot change score/verdict | ✅ 7 combinations, all `{-5}` |
| 7 | OKX dict fits `compact_for_llm` | ✅ with `spread: null`, named above |
| 8 | INSERT placeholder count matches columns | ✅ 30 → 32, both edited in the same hunk |
| 9 | `_ensure_schema` runs the ALTER before the first insert | ✅ `log_recheck` calls it at the top |

**Awaiting your go-ahead. Nothing will be applied until you give it.**
