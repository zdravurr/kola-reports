# titan every order-book figure traced, three SOL shapes checked, live short end-to-end

_2026-08-03 13:30 UTC_

---

# TITAN — EVERY ORDER-BOOK FIGURE TRACED · THE THREE SOL SHAPES CHECKED BY CODE · THE LIVE SHORT END-TO-END

_2026-08-03 · HEAD `3316e8a` · LIVE, real money, `LIVE_TRADING_ENABLED = True` + `ORDER_ADAPTER_LIVE = True` · $30 × 5 = $150 notional · **READ-ONLY pass, nothing changed, nothing proposed**_

---

## DECISION LINE

**Titan reads BingX's book in three places, and it contradicts OKX on almost every position.**

The entry advisor is shown the OKX depth-4000 book, as the standing decision requires. **What is
written on the position row is a different book** — a second, shallower BingX depth-100 capture
taken ~9 seconds later inside `_execute_entry`. Across the 18 positions since the OKX collector
went live, the stored imbalance sits on the **opposite side of 0.5** from the OKX reading at the
same instant in **16 of 18 — 88.9%**.

On the live short opened this morning the two readings are **0.0939 (row) vs 0.5584 (advisor)** —
the row says the book is 91% ask-weighted, the advisor was correctly told it was bid-heavy at the
89th percentile, and it cited that as a reason to enter. Same symbol, same second, opposite answer.

**This is not SOL's `walls_ask: []`, and it is not an overwrite.** No `UPDATE` ever touches the
`entry_*` book columns. The mechanism is different — **the advisor's book is simply never persisted
with position identity at all** — but the consequence is the same one SOL had: the number that
survives the trade is not the number the decision was made on.

**Three separate findings sit underneath, all measured, none previously recorded:**

1. **The exit advisor's "at entry" book reference silently changes between consults on the same
   position.** vpos 91's first consult was told `entry x4.8 / imbalance 0.55`; every consult since
   has been told `entry x4.1 / imbalance 0.56`. Cause traced and reproduced.
2. **The learning loop grades positions that are still open**, from unrealized P&L, once,
   permanently. **The live short was graded a WIN at +0.5015 on 2026-08-03 08:48:51 and is
   currently −0.534.** The combo-weight row already carries that number, and the combo weight is
   read by the entry gate.
3. **6,640 of 8,631 tracked skips carry no book at all** — the book is fetched *after* the gate, so
   `below_threshold` (843) and `htf_blocked` (5,797) rows have a NULL wall anchor 100% of the time,
   while the module's own docstring says the wall comes from "the OKX-4000 pre_trade_walls already
   computed."

**What is NOT broken, checked rather than assumed:** the cross-source *ranking* defect (§2b) is
genuinely dead. `_exit_pct()` takes `source` as a required positional argument and ANDs it into the
WHERE clause. Every one of the 7 consults on the live position carries
`source: OKX books-full depth-4000 (the percentile baseline)` and an internally consistent set of
percentiles. `625fedc` holds on live data.

**Nothing was touched. A live position is open.**

---

## 0. FILTERS APPLIED (OPEN-ITEMS §0)

| filter | how it was honoured here |
|---|---|
| paper/live split | **`stop_order_id IS NOT NULL`**, never `opened_at`. Yields exactly 6 rows: vpos 86–91. The paper book (53 closed rows, +528.74 at $10,000 notional) is stated separately and **never pooled**. |
| `confluence_score` holds three quantities | The live position's gate number is rebuilt from `matrix_breakdown_json`, not read off the column. Stored 2.5 ≠ the gate's 3.5. |
| ADX window | Every ADX quoted below carries `window=200`; `recheck_events.adx_window` = 200 on all three tiers. No cross-window subtraction is made. |
| replay validated before trusted | The one replay in this report (§4d, vpos 90's held branch) is a stop-touch test on real 5m candles with the intrabar ambiguity resolved **against** the held branch, seeded from the position's real state at close (`breakeven_applied=false`, water mark 62465.6 = +0.175R, so no breakeven and no trail could have armed). Its inputs are stated so it can be re-run. |
| excursion truth | `max_adverse_price` is not used for any R figure; `position_excursion_samples` (92 rows for vpos 91) and real candles are. |

---

# 1. EVERY ORDER-BOOK FIGURE: PRODUCER → CONSUMER

## 1.1 The four producers

| # | producer | venue | depth | wall rule | cadence |
|---|---|---|---|---|---|
| **P1** | `liquidity_zones.fetch_pre_trade_walls()` | **OKX** `books-full` | **4000/side** (8000 levels) | $5 bucket (`PRE_TRADE_WALL_BUCKET`); bucket USDT vol > **4.0×** side mean bucket vol (`PRE_TRADE_WALL_MULTIPLIER`) | on demand, 60 s cache |
| **P2** | `liquidity_zones.fetch_raw_book()` → `orderbook_collector` | **OKX** `books-full` | **4000/side** | same $5/×4.0 rule; also persists the **mean bucket volume** each multiple is measured against | **every 60 s, always** |
| **P3** | `microstructure.fetch_pre_trade_walls(exchange, …)` | **BingX** (ccxt `fetch_order_book`) | **100/side** (`PRE_TRADE_BOOK_DEPTH`) | level BTC vol > **4.0× mean of those 100 levels** — same constant, **different denominator** | on demand |
| **P4** | `microstructure.fetch_snapshot()` / `capture_and_persist_sync()` | **BingX** | **20/side** (`MICROSTRUCTURE_BOOK_DEPTH`) | level vol > **3.0× mean of those 20 levels** (`MICROSTRUCTURE_WALL_MULTIPLIER`) | async at every trade row |

P2 is the only baseline. `orderbook_density`: **30,343 rows**, `2026-07-13T02:34:56` → now,
**one source value only** (`okx_books_full_4000`), **zero gaps > 300 s since 2026-08-01**.

Note P1 and P3 share the constant `PRE_TRADE_WALL_MULTIPLIER = 4.0` while measuring different
things — a $5 USDT bucket against the OKX side mean vs a single BTC price level against a 100-level
BingX mean. **The same number, meaning two different things, in two functions with the same name.**

## 1.2 The consumer table — asked for, in full

| # | consumer | producer it reads | venue/depth | threshold | what it feeds |
|---|---|---|---|---|---|
| **a** | **Entry advisor prompt** — `claude_advisor._format_pre_trade_walls`, fed at `main.py:2017` / `:3835` | **P1** | **OKX-4000** | ×4.0 / $5 bucket | Claude's execute/skip verdict. Percentiles via `_entry_book_pct` → `_exit_pct(..., BOOK_SRC_OKX_4000)` |
| **b** | **Exit advisor prompt** — `main._build_exit_context:2531` | **P1** | **OKX-4000** | ×4.0 | Claude's close/hold verdict. **`EXIT_ADVISOR_DRYRUN = False` — this verdict closes real positions** |
| b′ | Exit advisor **fallback** when OKX returns nothing — `main.py:2600` | **P3** | **BingX-100** | ×4.0 (100-level mean) | same prompt, labelled `BingX depth-100 — RAW, NOT the percentile baseline`, **no percentile shown** (structurally: `BOOK_SRC_BINGX_100` matches 0 baseline rows) |
| b″ | Exit advisor "**at entry**" reference | **P2** row nearest the fill, ±10 min | **OKX-4000** | — | the `entry → now` arrows. **Drifts between consults — see §2c** |
| b‴ | Exit advisor **depth** line | **P2** latest row | **OKX-4000** | — | `Total depth = N BTC = Xth pct` |
| **c1** | **Position row** `virtual_positions.entry_wall_baseline_mult`, `entry_sup_wall_mult`, `entry_sup/opp_wall_dist_pct`, `entry_ob_imbalance`, `entry_n_walls_bid/ask` — written from `main.py:1317` | **P3** | 🔴 **BingX-100** | ×4.0 (100-level mean) | the recheck baseline; the exit-advisor fallback's entry reference |
| **c2** | **Trade row** `trades.orderbook_json` — `kick_off_capture` / `capture_and_persist_sync` | **P4** | 🔴 **BingX-20** | ×3.0 (20-level mean) | the learning loop; the entry Telegram card |
| c3 | Entry Telegram "Microstructure" line | **P4** | BingX-20 | ×3.0 | operator display only — **already labelled** `BingX top-20, raw (no baseline · not the advisor's book · context only)` |
| **d** | **Post-entry recheck** — baseline `virtual_trader.py:1669`, refresh `virtual_trader.py:1665` | baseline **P3**, refresh **P3** | 🔴 **BingX-100 both** | ×4.0 | `wall_ratio` vs `WALL_GROWTH_CRITICAL 2.0` / `WARNING 1.5`. **Score weight = 0 since 2026-07-13**, so it moves no verdict; it is logged to `recheck_events` |
| **e1** | **Learning loop** `signal_weights._attempt_learning` → `claude_advisor.consult_for_learning` | **P4** via `trades.orderbook_json` | 🔴 **BingX-20** | ×3.0 | `trades.learning_*`. Those columns are **read by nothing** |
| **e2** | **Combo weights** `signal_weights.audit_pending` → `record_outcome` | **no book** | — | — | `signal_weights.weight` → `weight_used` at the gate. **See §2e — it is fed a mid-flight P&L** |
| e3 | **Optimizer** `optimizer.CANDIDATE_FIELDS` | **no book** — 24 fields, none is a book field | — | — | segment proposals |
| e4 | **Weight engine** `weight_engine` | **no book** | — | — | `confluence_score` adjustment |
| **f1** | **skip_attribution** `_nearest_opposing_wall` | **P1** — but **only on the `ai_skipped` path** | OKX-4000 | ×4.0, nearest-to-mid | `skip_attribution.nearest_wall_price / wall_strength / wall_distance_pct`. **NULL on 100% of `below_threshold` and `htf_blocked`** |
| f2 | Sensors: `daily_trend_cohort_sensor`, `titan_bull_regime_watch.sh`, `titan_chop_short_flat_gap_watch.sh`, `titan_regime_flat_high_adx_watch.sh`, `titan_volfloor_data_watch.sh` | **no book** | — | — | — |
| f3 | `post_exit_observatory` | **no book** | — | — | — |
| **g1** | **Real SL anchoring** — `virtual_trader.py:833-836` | **no book**. `sl_price = fill ∓ SL_ATR_MULT(2.5) × ATR(SL_ATR_TF='1h')` | — | — | the live exchange `STOP_MARKET` |
| **g2** | Wall-anchor **DRYRUN** `_would_wall_stop` | **P1** (the sampler's already-fetched dict) | OKX-4000 | wall must sit > 0.15% beyond entry; buffer 0.15%; cap 1.2% | `smart_exit_dryrun_samples.would_wall_sl / wall_route`. `WALL_TRAIL_LIVE_ENABLED = False` — **moves no stop** |
| **h1** | **Smart-exit sampler** `_record_smart_exit_dryrun` | **P1** | OKX-4000 | ×4.0 | `smart_exit_dryrun_samples.ob_imbalance / opp_wall_mult / sup_wall_mult / n_walls_*`, `data_ok` |
| **h2** | **Excursion logger** `_record_excursion_sample` | **no book** — price only | — | — | `position_excursion_samples` |

## 1.3 🔴 IS ANYTHING ON TITAN READING BingX's BOOK? — YES. THREE THINGS.

**(1) The position row's entire entry-book snapshot** (`main.py:1317`, BingX depth-100).
This is the live, engine-owning entry path — the one that *always* runs. It feeds the recheck
baseline for the life of the position, and the exit advisor's entry reference whenever OKX is down.

**(2) The recheck's refresh** (`virtual_trader.py:1665`, BingX depth-100). Internally consistent
with (1), so the *ratio* is apples-to-apples — but it is a ratio on a book no percentile scale
exists for, and it is the one the operator sees in `[VIRTUAL] RECHECK … wall=17.8/20.0`.

**(3) `trades.orderbook_json`** (BingX depth-20, ×3.0 threshold), which is what the learning
loop reads and attributes the outcome to.

### Has it ever contradicted the OKX figure the way SOL's did? — Yes, systematically.

Every position with a stored book since `orderbook_density` began, against the OKX row nearest the
fill (±10 min, `source='okx_books_full_4000'`):

| vpos | side | row imbalance (BingX-100) | OKX-4000 imbalance | side-of-0.5 | row opposing wall | OKX opposing wall |
|---|---|---:|---:|:---:|---:|---:|
| 74 | SHORT | 0.6233 | 0.4926 | **FLIP** | ×5.6 | ×6.58 |
| 75 | LONG | 0.6957 | 0.4648 | **FLIP** | ×11.9 | ×4.49 |
| 76 | SHORT | 0.1130 | 0.5726 | **FLIP** | ×30.1 | ×4.67 |
| 77 | SHORT | 0.3194 | 0.6084 | **FLIP** | ×9.7 | ×12.78 |
| 78 | LONG | 0.7389 | 0.4302 | **FLIP** | ×15.8 | ×4.29 |
| 79 | LONG | 0.8919 | 0.4469 | **FLIP** | ×17.5 | ×6.42 |
| 80 | SHORT | 0.6258 | 0.6204 | same | ×14.2 | ×4.47 |
| 81 | SHORT | 0.3314 | 0.5764 | **FLIP** | ×12.3 | ×5.59 |
| 82 | LONG | 0.8748 | 0.4062 | **FLIP** | ×13.2 | ×9.48 |
| 83 | SHORT | 0.2058 | 0.5743 | **FLIP** | ×13.9 | ×5.08 |
| 84 | LONG | 0.6220 | 0.4444 | **FLIP** | ×8.1 | ×4.89 |
| 85 | LONG | 0.7306 | 0.4616 | **FLIP** | ×10.5 | ×6.44 |
| **86** | SHORT | 0.2914 | 0.5086 | **FLIP** | ×9.1 | ×4.84 |
| **87** | LONG | 0.5748 | 0.4182 | **FLIP** | ×16.0 | ×8.23 |
| **88** | SHORT | 0.3173 | 0.6012 | **FLIP** | ×10.8 | ×5.71 |
| **89** | SHORT | 0.3132 | 0.5690 | **FLIP** | ×9.6 | ×7.57 |
| **90** | SHORT | 0.5458 | 0.5549 | same | ×6.5 | ×4.45 |
| **91 (LIVE NOW)** | SHORT | **0.0939** | **0.5584** | **FLIP** | **×20.0** | **×4.66** |

**16 of 18 = 88.9% disagree on which side of the book is heavier.** Bold rows are the live era.
The opposing-wall multiple is 2–6× larger on the shallow book in every single row — it is a
multiple of a 100-level mean, so it is measuring a much smaller "average" and inflating everything
against it. **This is the same class as SOL's Bybit-20 row against the OKX-4000 advisor figure. The
difference is only that Titan's shallow number is not empty — it is wrong in a way that reads as
data.**

**Where the code already knew.** `main.py:2540-2546` says it outright:

> *"virtual_positions.entry_sup_wall_mult and entry_ob_imbalance are BingX depth-100 (written by
> the microstructure path at fill time), so pairing them with an OKX 'now' would re-create the very
> defect being removed… vpos 86's stored 0.2914 against a live OKX 0.51 would have read as a
> dramatic FLIP that never happened."*

The exit side routed **around** the bad column. The column itself was never fixed, and nothing else
that reads it was told.

---

# 2. THE FOUR SOL SHAPES, CHECKED BY CODE

## 2a. STORAGE OVERWRITE — **not present as an overwrite. Present as an equivalent.**

**Checked:** every `UPDATE virtual_positions` in the codebase — 10 sites (`virtual_trader.py:1230,
1327, 1577, 1616, 1836, 2117, 2306, 2328, 2380, 2536`). **Not one touches an `entry_*` book
column.** `trades.ai_user_prompt` is written once by `update_signal_execution` and never rewritten.
**There is no fill-time overwrite on Titan. SOL's exact mechanism is absent.**

**But the effect SOL suffered is reproduced by a different route.** The entry path takes **two
book snapshots from two venues**:

```
06:40:0x  main.py:2017  liquidity_zones.fetch_pre_trade_walls()   OKX-4000  -> ADVISOR PROMPT (persisted in trades.ai_user_prompt)
06:40:17  main.py:1317  microstructure.fetch_pre_trade_walls()    BingX-100 -> THE POSITION ROW  (persisted in virtual_positions.entry_*)
06:40:19  virtual_trader:2067  liquidity_zones.fetch_pre_trade_walls()  OKX-4000 -> smart_exit_dryrun_samples (1.6 s after fill)
06:40:1x  microstructure.kick_off_capture()                        BingX-20  -> trades.orderbook_json
```

**Four book fetches, two venues, three depths, three wall thresholds, inside 20 seconds.** The
advisor's book is not overwritten — it is **never given position identity in the first place**.
Anything downstream asking "what did the book look like when this position opened" and reading the
position row gets the BingX-100 answer.

**Proof on the live position, from the bot's own two records 1.6 seconds apart:**

| field | `smart_exit_dryrun_samples` @ 06:40:19.9 (OKX-4000) | `virtual_positions` row 91 (BingX-100) |
|---|---:|---:|
| imbalance | **0.5539** | **0.0939** |
| supporting wall (ask, SHORT) | ×4.7 | ×4.8 |
| opposing wall (bid, SHORT) | ×4.7 | **×20.0** |
| n walls bid / ask | 2 / 2 | **5 / 2** |

## 2b. CROSS-SOURCE RANKING — **fixed, and the guard is structural. Verified live.**

`main._exit_pct(col, value, source)` — `source` is a **required positional argument** and is ANDed
into the WHERE clause, so a value can only be ranked against rows from its own instrument.
`BOOK_SRC_BINGX_100 = 'bingx_depth100'` matches **zero** rows in `orderbook_density` (confirmed:
the table has exactly one distinct source value across 30,343 rows), so a BingX figure is not
merely *not ranked* by convention — **it is unrankable**.

Both call paths verified: `_entry_book_pct` (3 calls) and `_build_exit_context` (4 calls) all pass
`BOOK_SRC_OKX_4000`, and all read `walls` from `liquidity_zones`.

**Live evidence, all 7 consults on vpos 91:** every prompt carries
`source: OKX books-full depth-4000 (the percentile baseline)` and internally coherent percentiles.
The inverted `93th pct` phantom wall that talked the advisor into holding vpos 86 does not recur.
**Not present today.**

## 2c. MIXED BASELINE AND REFRESH — **not in the recheck. Present, differently, in the exit advisor.**

**The recheck is clean.** Baseline `entry_wall_baseline_mult` (P3, BingX-100) vs refresh
`cur_walls` (P3, BingX-100) — **same function, same venue, same depth, same threshold**. The ratio
is apples-to-apples. It is on the wrong book, but it is not a mixed comparison, and
`WALL_GROWTH_*_SCORE = 0` means it moves no verdict either way.

🔴 **But the exit advisor's "at entry" reference is not stable across consults on the same
position.** `main.py:2553-2573` picks the `orderbook_density` row **nearest the fill** within
±10 min. At the first consult (seconds after the fill) only *pre-fill* rows exist; by the second
consult a *post-fill* row exists and is nearer. **The "at entry" number therefore changes once, and
silently.**

Reproduced exactly on vpos 91 (fill `06:40:17.483`):

| collector row | Δ to fill | imbalance | max ask wall |
|---|---:|---:|---:|
| 06:39:25.195 | **−52.3 s** | 0.5517 | ×4.85 |
| 06:40:26.228 | **+8.7 s** | 0.5584 | ×4.08 |

| consult | prompt says |
|---|---|
| 20921 @ 06:40:23 | `(entry reference sampled 52s from fill)` · `Supporting wall: entry x4.8 -> now x4.7 (THINNED)` · `Imbalance: entry 0.55` |
| 20985 @ 12:41:06 | `(entry reference sampled 8s from fill)` · `Supporting wall: entry x4.1 -> now x6.4 (grew)` · `Imbalance: entry 0.56` |

**Same position, same "entry", two different numbers — the wall reference moved −15%, and it is
the denominator of the THINNED/grew arrow the advisor reads.** The age *is* printed, which is why
this was catchable; nothing states that the reference changed. Both books are OKX-4000, so this is
not a cross-source defect — it is a **moving baseline**, the third shape's cousin.

## 2d. FAILED READ SCORED AS A PASS — **handled in four places, half-handled in one, unhandled in one.**

| site | failed read distinguishable? | evidence |
|---|---|---|
| **Smart-exit sampler** | ✅ **Yes, explicitly.** `data_ok = 0` on fetch failure, all book fields NULL. A *successful* read with no wall gives `data_ok = 1` + `opp_wall_mult = NULL` — and both states occur in vpos 91's own 7 samples (two have `opp_wall_mult NULL, n_walls_bid 0, data_ok 1`). | 272 samples lifetime, **0 with `data_ok = 0`** |
| **Entry advisor** | ✅ Yes. `main.py:410` renders `Order book (pre-trade): unavailable` when `pre_trade_walls` is falsy. No block, no percentile, no silence. | 102 of 1,991 `ai_skipped` rows have a NULL wall = **5.1% OKX failure rate on the AI path** |
| **Exit advisor** | ✅ Yes. OKX down → BingX fallback rendered with its source named and **no percentile**; both down → the whole book block is absent. | all 7 live consults used the OKX branch |
| **Percentile function** | ✅ Yes. `_exit_pct` returns `(None, 0)` on an empty baseline; every renderer degrades to "no percentile shown". | — |
| **Post-entry recheck** | ⚠️ **Half.** In the DB, `cur_wall_mult` is `NULL` on fetch failure vs `0.0` on "read fine, no opposing wall" — distinguishable. **In `reasons_json`, in the verdict, and in the Telegram line it is not**: `_health_score`'s wall rule appends nothing when its inputs are None, which is byte-identical to appending nothing when the ratio is small. Because `WALL_GROWTH_*_SCORE = 0`, **a failed read cannot change a verdict** — the exposure is analytic, not behavioural. | 50 `recheck_events` rows lifetime: **0 NULL, 0 zero** — it has never yet failed |
| **skip_attribution** | 🔴 **No.** `_nearest_opposing_wall` returns `(None, None)` both when the walls dict is missing (OKX failed) and when there simply is no wall on that side. Observational module; nothing trades on it. | 102 NULL rows on the AI path are indistinguishable between the two causes |

### 🔴 And a coverage hole underneath it: 6,640 of 8,631 tracked skips have no book at all

`skip_attribution.py:9` states the wall comes *"from the OKX-4000 pre_trade_walls **already
computed** on the AI path"* — true, and that is exactly the problem: the book is fetched **after**
the score gate, so the two pre-AI skip statuses never have one.

| status | rows tracked | rows with NULL wall anchor |
|---|---:|---:|
| `ai_skipped` | 1,991 | 102 (**5.1%** — real OKX failures) |
| `below_threshold` | 843 | **843 (100%)** |
| `htf_blocked` | 5,797 | **5,797 (100%)** |

The module's docstring also says `htf_blocked` is *"EXCLUDED by design"*, while
`TRACKED_STATUSES` includes it and 5,797 rows exist. The observatory's central question — *"is
there a wall-distance threshold that separates good skips from missed moves?"* — **is unanswerable
for 77% of its own sample**, and nothing says so.

## 2e. 🔴 NOT ONE OF THE FOUR, BUT IT IS THE LEARNING LOOP: OPEN POSITIONS ARE GRADED AS CLOSED

`signal_weights.audit_pending` selects on `status='executed' AND audit_score IS NULL` and an age
window of **2–24 h**. It does **not** require the position to be closed. `_evaluate_trade_pnl` then
falls back to the exchange's **unrealized** P&L, `audit_score` is stamped, and the row is never
audited again. The same number goes to `record_outcome` (combo weights, which the entry gate reads
as `weight_used`), to `engine_15m.record_outcome`, and to `consult_for_learning` as the outcome the
BingX-20 book is attributed to.

Live era, audit time vs close time:

| trade | vpos | audited at | audit_score used | realised net | verdict |
|---|---|---|---:|---:|---|
| 19589 | 86 | 07-30 02:51:22 | **−1.2829** | −2.5416 | graded while open, **half the eventual loss** |
| 19713 | 87 | 07-30 14:11:13 | **−0.3467** | −0.8191 | graded while open (closed 12 h later) |
| 20006 | 88 | 07-31 11:44:43 | −0.5311 | −0.5311 | closed first ✅ |
| 20054 | 89 | 07-31 14:24:45 | +2.3024 | +2.3024 | closed first ✅ |
| 20100 | 90 | 07-31 16:34:47 | −0.6099 | −0.6099 | closed first ✅ |
| **20920** | **91** | **08-03 08:48:51** | **+0.5015 — a WIN** | **still open, −0.534 now** | 🔴 **graded while open, wrong sign** |

**3 of 6 live-era entries were graded from a mid-flight mark. Two of those are materially wrong,
and one is the position that is open right now.** The weight table already carries it:

```
combo_key = '1H:Bearish Confirmation|15M:HyperWave OS Signal Up|5M:Bearish OB Created'
weight 1.0 · wins 0 · losses 0 · evaluations 1 · total_pnl +0.5015 · updated_at 2026-08-03 08:48:51
```

And the microstructure attribution written 2 seconds later, for a trade that has not exited:

> *"Large ask wall (68.32 BTC at 62650.5) above entry created resistance, **enabling profitable
> short exit as price rejected upward pressure**."* — `learning_reason`, row 20920

That ask wall is a **BingX depth-20** level at 62650.5, ×3.0 of a 20-level mean. The advisor's
OKX-4000 book that same second reported ask walls at **62712.50 (×4.7)** and **62867.50 (×4.0)** —
**and none at 62650.5.** Three books, three wall sets, and the learning loop is writing its lesson
from the shallowest one about an outcome that has not happened.

---

# 3. THE LIVE POSITION — vpos 91

## 3a. Full record

| | |
|---|---|
| **vpos** | **91** · BTC/USDT:USDT · **SHORT** · `status=open` |
| entry | **62,649.2** @ **2026-08-03 06:40:17.483 UTC** |
| size / margin | 0.0023 BTC · $30 × 5 = **$144.62 notional** |
| stop | **63,224.6** — `original_sl_price` identical, **never moved** |
| exchange stop id | `2084167453017485312` |
| **1R** | 575.4 pts = **1.32339 USDT** = 0.918% |
| entry fee | 0.072011 (taker 5.0 bps, read back from BingX) |
| MFE / MAE | water mark **62,268.6 = +0.661R** · max adverse **62,884.6 = −0.409R** |
| now (13:26 UTC) | 62,822.9 → **−0.302R**, uPnL **−0.534 USDT**, 0.64% of stop cushion left |
| breakeven / trail | `breakeven_applied = false` — **never armed** (needs 62,073.8 = +1R) |
| recheck | `done` — three tiers ran, all `TIGHTEN`, **all no-op** |
| entry ADX 1h | 18.5805, **window 200** |
| entry ATR% 1h | 0.36737 |

**The three tiers that opened it** (`trades.entry_tiers_json` — the structured record, not parsed
from text):

| tier | name | direction | weight | age at entry | counted by gate |
|---|---|---|---:|---|---|
| **1H** | Bearish Confirmation | *withheld* (`AI_ADVISOR_HIDE_1H = True`) | 0.7 | 2.7 h | **yes** |
| **15m** | HyperWave OS Signal Up | **LONG** | 1.0 | 25 m | no — matrix TTL expired |
| **5m** | Bearish OB Created | **SHORT** | 0.5 | 0 m, trigger-capable | no — matrix TTL expired |

> *Agreement: 15m points LONG; 5m points SHORT; vs the proposed SHORT: 5m agree, **15m OPPOSE**.*

**The score arithmetic**, rebuilt from `matrix_breakdown_json` per §0 (never from
`confluence_score`):

| category | long | short | net | contribution |
|---|---:|---:|---|---:|
| TREND | 0.0 | 2.5 | SHORT | **+2.5** |
| MOMENTUM | 2.5 | 1.75 | NEUTRAL (intra-conflict) | 0.0 |
| LIQUIDITY | 2.5 | 2.5 | NEUTRAL (intra-conflict) | 0.0 |
| EXECUTION | 2.5 | 2.5 | NEUTRAL (intra-conflict) | 0.0 |

```
raw                 = 2.5
macro_gate_penalty  = +1.0
gated               = 3.5   >=  CONFLUENCE_SCORE_THRESHOLD 3.0 (TREND bar)  -> PASS
weight_used         = 1.00  (combo baseline)
stored confluence_score = 2.5   <- raw + weight-engine adj, NOT the gate number
```

🔴 **The gate passed on 3.5 against a 3.0 bar with 2.5 of raw score, entirely from TREND, with
three of four categories self-cancelling and the 15m tier pointing the other way.** Every number
here is stated, none is a judgement.

**The entry advisor's verbatim reason** (`claude-haiku-4-5-20251001`, `execute`, conf 0.72):

> *1d/4h/1h/15m/5m all BEAR; 15m ADX 47.7 strong; 5m trigger fresh (0m); **bid-heavy imbalance
> (89th)**; ask walls ordinary (22nd pct). 15m opposes but expired TTL. Risk: low depth (52nd pct),
> 1.85x vol.*

## 3b. The book section of its stored entry prompt — verbatim

```
Order book (pre-trade, 8000 levels):
  Mid: $62,648.45  |  Imbalance ±1%: 0.55 (bid-heavy)  — 89th pct
  Bid walls (>4x avg bucket vol): $62,522.50 (×4.7), $62,487.50 (×4.0)  — largest ×4.7 = 28th pct
  Ask walls (>4x avg bucket vol): $62,712.50 (×4.7), $62,867.50 (×4.0)  — largest ×4.7 = 22th pct
  Book depth: 2,981 BTC — 52th pct, sampled 47s ago
Order-book PERCENTILE scale (baseline: 29952 snapshots of this same OKX depth-4000 book)
```

| figure | value | percentile | **source** |
|---|---:|---:|---|
| Mid | $62,648.45 | — | **OKX books-full depth-4000** (P1) |
| Imbalance ±1% | 0.55 bid-heavy | **89th** | OKX-4000 value, ranked in `orderbook_density` source `okx_books_full_4000` |
| Largest bid wall | ×4.7 @ $62,522.50 | **28th** | OKX-4000, $5 bucket, ×4.0 threshold |
| Largest ask wall | ×4.7 @ $62,712.50 | **22nd** | OKX-4000, $5 bucket, ×4.0 threshold |
| Book depth | 2,981 BTC | **52nd** | `orderbook_density` latest row (P2), 47 s old — **not** the walls dict, whose `depth` is a level count |

**All five figures are OKX-4000 ranked against OKX-4000.** The entry block is correct and says so.

## 3c. The prompt against the trade row and the position row, RIGHT NOW — **they are not the same book**

| figure | **advisor prompt** (OKX-4000) | **`virtual_positions` 91** (BingX-100) | **`trades.orderbook_json` 20920** (BingX-20) |
|---|---:|---:|---:|
| mid | 62,648.45 | 62,649.2 (fill fallback) | 62,648.25 |
| **imbalance ±1%** | **0.55 — bid-heavy, 89th pct** | **0.0939** | **0.338** |
| opposing wall (bid) | ×4.7 @ 62,522.50 | **×20.0** | 23.6085 BTC @ 62,646.0 |
| supporting wall (ask) | ×4.7 @ 62,712.50 | ×4.8 | 68.3216 BTC @ 62,650.5 |
| n walls bid / ask | 2 / 2 | **5 / 2** | 2 / 1 |
| wall rule | > ×4.0 of side mean **$5 bucket** | > ×4.0 of mean of **100 levels** | > ×3.0 of mean of **20 levels** |

**They differ, and the difference is not cosmetic.** The advisor entered partly *because* the book
was bid-heavy at the 89th percentile — a fact recorded verbatim in its reason. The row that
survives this trade says the book was 91% ask-weighted with a ×20 wall against it. **Whatever the
outcome, the row will teach the opposite lesson from the one the decision was made on.**

**Per the terms of §2a, this is the SOL defect on live money — reached by a different mechanism
(two captures, not one overwrite), with the same result.** The count is
`1 of 1` live positions currently affected, and `16 of 18` historically.

## 3d. What the exit advisor has said — all 7 consults, verbatim, with the book it was given

`EXIT_ADVISOR_DRYRUN = False` — **these verdicts can close the position.** Every one was `hold`.

| row | UTC | trigger | verdict | conf | R then | book block given (source: **OKX-4000** on all 7) |
|---|---|---|---|---:|---:|---|
| 20921 | 06:40:23 | hourly | hold | 0.62 | −0.00R | sup entry ×4.8 → now ×4.7 (THINNED, 22nd) · opp ×4.7 (28th) · imb 0.55→0.55 (89th) · depth 2981 BTC (52nd) |
| 20932 | 07:40:34 | hourly | hold | 0.62 | +0.08R | sup ×4.1 → ×4.8 (grew) · imb 95th · "opposing wall absent" |
| 20950 | 08:40:33 | hourly | hold | **0.68** | +0.47R | imb 94th (extreme bid-heavy) · sup ×4.1→×4.5 |
| 20960 | 09:40:40 | hourly | hold | 0.62 | +0.02R | imb **flipped to 54th (ordinary)** · sup grew but 13th pct |
| 20973 | 10:40:49 | hourly | hold | 0.62 | +0.02R | imb 89th → **53rd** · sup thinned ×4.1→×4.0 |
| 20980 | 11:40:57 | hourly | hold | 0.62 | −0.07R | imb 89th → **36th** · sup ×4.1→×6.1 · opp 37th |
| 20985 | 12:41:06 | hourly | hold | 0.62 | +0.05R | sup ×4.1→×6.4 (58th) · opp ×4.8 (31st) · imb 0.52 (70th) · depth 2861 BTC (37th) |

Verbatim, the most recent (20985):

> *Position +0.05R with active stop at +1.05R. Entry thesis partially intact: 1d/4h/1h remain bear,
> 5m trigger fresh. However, 15m has shifted to neutral (ADX 34.6 from 47.7), opposing the short.
> Recent bullish imbalance 16m ago and liquidity grab 41m ago work against thesis. Supporting wall
> grew 6.4x (58th pct, ordinary), but opposing wall weak (31st pct). Book imbalance 70th pct
> maintains conviction…*

And the first (20921):

> *Position is 0m old with no realized loss. Entry thesis partially compromised: 15m HyperWave OS
> (LONG, weight 1.0) opposes SHORT directionally, though 5m bearish trigger fresh. Regime confirms
> bear across all timeframes (ADX15m=47.7 strong), and **bid-heavy imbalance (89th pct) supports
> entry logic**…*

🔴 **Note the arithmetic the advisor is being handed and what it does with it.** Rows 20932 and
20950 cite `imbalance 95th` and `94th` as support while the *position's* own edge is 0.08R and
0.47R; by 20960 the same figure is 54th and the verdict does not change. **Six of seven consults
returned confidence 0.62 and the word "partially" — the book figures moved across the full
36th–95th percentile range without moving the verdict once.** That is an observation about the
sample, not a conclusion; §2.4 is the place it gets counted, and this position has not closed.

**Also note the entry-reference drift from §2c is visible in this very table** — `sup entry ×4.8`
at 06:40 becomes `sup entry ×4.1` from 07:40 onward. The `THINNED` on the first consult and the
`grew` on the second are computed against **different denominators**.

## 3e. The exchange, read-only — it reconciles

```
POSITION   BTC/USDT:USDT  short  0.0023  entry 62649.2  mark 62881.4
           uPnL -0.5341  leverage 5.0  marginMode CROSSED  initialMargin 28.8186  notional 144.62

OPEN ORDERS (exactly one)
  id 2084167453017485312   STOP_MARKET   closePosition='true'   positionSide SHORT
  stopPrice 63224.6   workingType MARK_PRICE   status NEW   placed 06:40:17.415Z

BALANCE  USDT  free 481.0035  used 28.8186  total 509.8221
```

| check | result |
|---|---|
| exchange size vs row `step_size` | 0.0023 = 0.0023 ✅ |
| exchange entry vs row `initial_fill_price` | 62,649.2 = 62,649.2 ✅ |
| order id vs row `stop_order_id` | `2084167453017485312` = `2084167453017485312` ✅ |
| stopPrice vs row `sl_price` | 63,224.6 = 63,224.6 ✅ |
| **exactly ONE `closePosition` order** | ✅ — the §1a invariant holds |
| orphan stops on either side | none — boot `[STOP-CLEANUP] no orphaned orders` for LONG **and** SHORT ✅ |
| **margin mode** | **CROSSED** — §1b, unchanged, immaterial at $150/5x but still on the size-increase checklist |
| stop trigger basis | `MARK_PRICE` (62,881.4), not last — mark is 0.7 above last right now |

**"Does it reconcile with the book?"** — the stop at 63,224.6 sits **0.64%** above the current
price. The OKX-4000 book right now shows the nearest supporting (ask) wall at ×6.4 and the wall-
anchor DRYRUN would place its stop at **63,096.47** — 0.76% away, *tighter* than the real ATR stop,
`wall_route='wall'`, `tighter=1`, `breached_now=0`. **`WALL_TRAIL_LIVE_ENABLED = False`, so this
moves nothing** — it is the observational series, and on this position it has logged
`wall_route='wall'` on 4 of 7 samples and `fallback_atr` on 3.

---

# 4. HOW TITAN HAS LIVED SINCE 2026-08-01

## 4a. Every position, LIVE era stated separately

**Split predicate: `stop_order_id IS NOT NULL`.** Not `opened_at` — §0.

### LIVE (real money, $150 notional)

| vpos | side | opened (UTC) | closed | reason | net USDT | 1R USDT | fees |
|---|---|---|---|---|---:|---:|---:|
| 86 | SHORT | 07-30 00:50:14 | 07-30 11:50:48 | `sl` | **−2.5416** | 2.487 | 0.1477 |
| 87 | LONG | 07-30 12:05:17 | 07-31 02:06:51 | `ai_exit` | **−0.8191** | 1.863 | 0.1488 |
| 88 | SHORT | 07-31 09:35:18 | 07-31 10:35:35 | `ai_exit` | **−0.5311** | 1.792 | 0.1466 |
| 89 | SHORT | 07-31 12:20:15 | 07-31 14:15:13 | `ai_exit` | **+2.3024** | 1.661 | 0.1453 |
| 90 | SHORT | 07-31 14:25:19 | 07-31 16:25:42 | `ai_exit` | **−0.6099** | 2.009 | 0.1443 |
| **91** | **SHORT** | **08-03 06:40:17** | **— OPEN —** | — | **−0.534 unreal.** | 1.323 | 0.0720 so far |

```
LIVE closed, 5 positions            : -2.1993 USDT
  + the 2026-07-29 naked short with no DB row, closed by hand :  -0.26
  = realised live P&L to date       : -2.4593 USDT
per side (closed) : SHORT n=4  -1.3802  (1 win)   |   LONG n=1  -0.8191  (0 wins)
exit reasons      : ai_exit 4 · sl 1
total fees paid   : 0.7327 USDT across 5 round trips  = 33% of the gross loss
```

**Since 2026-08-01 specifically: exactly ONE new position — vpos 91, opened 08-03 06:40, still
open.** Two and a half days, one entry. The drought §2.36/§2.37 recorded on 08-01 has continued.

### PAPER (simulated, $10,000 notional) — **stated separately, never pooled**

```
53 closed rows, sum +528.74 USDT.  A 68x notional difference. These two books are not comparable
and no figure above mixes them.
```

## 4b. The four hands-required alerts — **none fired**

Journal swept `2026-07-30 21:00` (earliest retained) → now:

| alert | fired? |
|---|---|
| `[SL-FAILSAFE] CRITICAL: emergency close itself failed` | **no** |
| `🚨 ORPHAN STOP COULD NOT BE CANCELLED … MANUAL ACTION REQUIRED` | **no** |
| `🚨 POSITION GONE, STOP DID NOT FILL … MANUAL ACTION REQUIRED` | **no** |
| circuit breaker / `daily_loss_halt` / loss-streak halt tripped | **no** |
| `🔴 PARTIAL FILL on entry` (item 14 still unbuilt) | **no** |
| `🛑 REFUSING TO START` | **no** |

`RISK HALT` appears 29 times — **all of them `position-cap halt: 1 SHORT/LONG already open
(cap=1)`**, which is `MAX_POSITIONS_PER_SIDE = 1` working as designed while a position is open, not
a fault.

**The stop still has not FIRED on a live position under item 11.** vpos 86 closed at `reason='sl'`
on 07-30, before the window; nothing since has reached its stop. The §1a caveat stands: **placement
is not triggering.**

## 4c. Service health

```
titan.service   active (running) since 2026-08-01 13:08:26 UTC   uptime 2d 0h
Main PID 1064304 (gunicorn master) + 1064336 (worker)
Memory 339.4M (peak 393.8M, swap 278.2M)   CPU 1h41m over 2 days
```

**Restarts since 08-01: exactly one** — the `3316e8a` deploy at 13:08:26. (Prior restarts 07-30
21:26, 22:16, 22:24 are outside the window.)

**All four boot gates green on that restart**, verbatim:

```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
[TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
[RECONCILE] boot reconciliation starting
[STOP-CLEANUP] no orphaned orders for LONG BTC/USDT:USDT
[STOP-CLEANUP] no orphaned orders for SHORT BTC/USDT:USDT
[RECONCILE] done
[TITAN][OB-DENSITY] ctVal=0.01 BTC/contract read from OKX instrument spec   <- from the SPEC, not the fallback
```

**Errors and tracebacks since 08-01: five lines, all one class** — `ConnectionResetError(104)` on
BingX `/quote/openInterest` (×4) and `/quote/premiumIndex` (×1). Market-context enrichment only;
no gate, no exit, no order path. **Zero tracebacks. Zero `[ERROR]`. Zero exceptions.**

Collector health: **30,343 rows, no gap > 300 s since 08-01**, heartbeat `+1 rows, 0 failures`.

## 4d. The exit-advisor criterion (§2.4) — **still 4 of ~10, and it did not move**

**Count: 4. Unchanged since 2026-08-01 12:25.** Zero new datapoints in 2.6 days, for a single
reason: **only one position has opened since, and it has not closed.** vpos 91's 7 consults are all
`hold`, so it has not yet produced a datapoint at all.

🔴 **What DID change: the one unresolved held branch has resolved, and it resolved in the
advisor's favour.**

Caveat 3 recorded on 08-01 said *"vpos 90's held branch never terminated — it is marked to market
at 08-01 12:25 (+0.291R for the advisor), not resolved by stop or trail. One of the four datapoints
can still change sign."* Measured today on 828 real 5m BingX candles, 07-31 16:25 → 08-03 13:20:

```
vpos 90 SHORT, entry 62618.4, stop 63491.9 (never moved), 1R = 2.00908 USDT
  +1R breakeven arm level 61744.9   -> min low over the window 62245.0   NEVER REACHED
  => breakeven never arms, trail never arms, stop stands at 63491.9 the whole time
  first 5m candle touching the stop: 2026-08-02 02:05 UTC   O 62939.0  H 63500.0  L 62937.6  C 63365.9
  held gross  (62618.4 - 63491.9) x 0.0023            = -2.0090
  held fees   entry 0.072011 + exit 63491.9x0.0023x5bps = 0.1450
  held net (excl. funding)                              = -2.1541
  advisor actual net                                     = -0.6099
  ADVISOR - HELD                                         = +1.5442 USDT  (+0.769R)
```

Updating only that one line of the 08-01 table, with the other three untouched:

| vpos | side | held branch outcome | advisor net | held net | advisor − held |
|---|---|---|---:|---:|---:|
| 87 | LONG | `sl` @ 64028.8, bar 07-31 07:05 | −0.8191 | −2.0110 | **+1.1919** |
| 88 | SHORT | breakeven → `trail` @ 63192.2, bar 07-31 17:50 | −0.5311 | +0.8914 | **−1.4225** |
| 89 | SHORT | `trail` @ 63171.3, bar 07-31 17:50 | +2.3024 | +1.0703 | **+1.2321** |
| **90** | SHORT | 🔴 **RESOLVED: `sl` @ 63491.9, bar 2026-08-02 02:05** *(was: marked to market)* | −0.6099 | **−2.1541** | **+1.5442** |

```
NET n=4 : advisor +0.3423  vs  held -2.2034   ->  advisor +2.5457 USDT.  Improved 3, worsened 1.
(was +1.5852 on 08-01, when vpos 90 was a mark rather than a resolution)
```

**Drift, stated and not concluded on:** the margin widened from +1.5852 to +2.5457 and **all four
held branches are now terminated**, which retires caveat 3 — the only caveat that could still have
flipped a datapoint's sign. Caveats 1, 2, 4 and 5 stand unchanged: fees are 1.7× the sample's
realised P&L; no closing threshold is readable from a distribution whose deepest adverse consult is
−0.36R; the held branches are mutually exclusive at `MAX_POSITIONS_PER_SIDE = 1`; and from `3316e8a`
the remaining ~6 datapoints come from a loss-streak-filtered population.

🔴 **The bar is 10 and it does not move. n = 4. Six more advisor closes are needed, and at the
current rate — one entry in 2.6 days — that is a long way off. Nothing here is a result.**

---

## APPENDIX — WHAT WAS CHECKED AND FOUND CLEAN

| claim | verdict |
|---|---|
| Cross-source percentile ranking (§2b) | **Dead.** `source` mandatory + in the WHERE clause; `BOOK_SRC_BINGX_100` matches 0 baseline rows. All 7 live consults verified OKX-vs-OKX |
| Storage overwrite of the entry book | **Absent.** All 10 `UPDATE virtual_positions` sites checked; none touch an `entry_*` book column |
| Recheck baseline/refresh mismatch | **Absent.** Both are `microstructure.fetch_pre_trade_walls` |
| Optimizer reads a book figure | **No.** 24 `CANDIDATE_FIELDS`, none is a book field |
| Weight engine reads a book figure | **No.** |
| Excursion logger reads a book figure | **No.** Price only |
| Post-exit observatory reads a book figure | **No.** |
| Sensors / watch scripts read a book figure | **No.** |
| Real SL anchored to a wall | **No.** `2.5 × ATR(1h)`. Wall anchoring is DRYRUN, `WALL_TRAIL_LIVE_ENABLED = False` |
| Smart-exit sampler venue | **OKX-4000**, correct, with `data_ok` |
| `trades.learning_*` feeds anything that trades | **No** — the columns are written and read by nothing |
| Exchange/DB reconciliation on the live position | **Exact on all four fields**, one `closePosition` order, no orphans |
| Boot gates on the one restart since 08-01 | **All four green** |

**Nothing in this pass was changed, and nothing is proposed. The position is untouched.**
