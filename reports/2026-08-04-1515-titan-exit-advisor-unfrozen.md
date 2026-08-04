# THE EXIT ADVISOR IS UNFROZEN, AND IT NO LONGER REASONS FROM A REFERENCE THAT MOVED AFTER THE FILL

**2026-08-04 15:15 UTC · Titan LIVE, real money, flat (0 open positions) · commit `a637071`**
**Applied from flat, restart 15:08:30, `py_compile` clean on all four files.**

§2.4's ten-position window is **CLOSED at five by operator decision**, recorded as his. The four
post-window items land in one commit, in the order §2.42a required. Canon updated in the same commit:
**§2.4 replaced**, **§2.4-EXIT** added, **§2.42a** marked applied. Snapshot:
`reports/2026-08-04-1515-open-items.md`.

---

## 🔴 THE ONE MEASUREMENT THAT JUSTIFIES THE WHOLE PASS

The drifting entry reference was not an edge case. **Replayed against real stored rows, the old rule
picked a POST-fill measurement on 4 of the 4 most recent positions** — and across **every stored exit
consult that carries a book block (n = 146), the THINNED/grew arrow the advisor reasons from FLIPS on
15 of them (10.3 %)**:

| vpos | old rule (nearest ±10 min) | new rule (latest ≤ fill) | consults whose arrow flips |
|---|---|---|---|
| 91 | **+8.7 s** → x4.08 / imb 0.5584 | −52.3 s → **x4.85** / 0.5517 | 4 |
| 92 | **+10.0 s** → x4.03 / 0.4479 | −51.0 s → **x5.45** / 0.4589 | 0 |
| 90 | **+23.2 s** → x4.59 / 0.5549 | −37.8 s → **x4.39** / 0.5662 | 1 |
| 89 | **+23.2 s** → x5.58 / 0.5690 | −37.8 s → **x5.28** / 0.5484 | 0 |
| 87 | (same shape) | | **7** |

**vpos 87's printed reference moved `x6.4 → x5.0` mid-life** — the drift is visible in the stored
prompts themselves, not inferred. Seven of its consults would have read **THINNED** where they read
**grew**.

---

## 1. THE OPERATOR'S DECISION, RECORDED AS HIS

> §2.4's ten-position bar is **RETIRED at five**. It existed to decide whether the advisor should be
> allowed to close. It has closed five positions, all five held-branches resolved, improved 4 and
> worsened 1, **net +3.37R**. The question it was asked has been answered by the advisor's own work.
> Holding the remaining inputs behind it costs money on every position and buys nothing — and the
> cost doubled at 14:41, when the EMA envelope gate cut the entry rate from 0.90 to 0.47/day, so five
> more closes is **roughly three months, not six weeks**.
> **A measurement window that outlives the thing it measures is not discipline.**

```
FINAL TALLY, n = 5      advisor  -0.2987 USDT
                        held     -3.6716 USDT
                        Δ        +3.3729 USDT     improved 4 · worsened 1 · all 5 branches terminated
```

**What this is and is not — written at the operator's instruction, before any result can be claimed:**

- **It is a decision made on FIVE OBSERVATIONS.** The advisor **could still turn out to be
  net-negative over twenty**, and if that happens it is not a hidden surprise — it is written here in
  advance.
- **The evidence is a direction with a consistent sign, not a proof.** The one that worsened
  (vpos 88, **−1.4225**) is a real loss, not noise to be explained away.
- **The kill switch is `EXIT_ADVISOR_DRYRUN = True`** — one flag and the advisor can never close
  again. It does not need this file's permission to be used.
- **The bar was not moved to fit a result — it was retired, in the open, with the tally attached.**
  That distinction is the whole difference, and it is the operator's to make.

**The freeze is lifted.** Future exit-prompt changes need no window — they need the same discipline
as everything else: measure first, state the effect on real stored data, apply, verify against a live
artefact. **No standing exemption is created.**

## 2. ITEM ① — THE DRIFTING REFERENCE, FIXED

```diff
-            # Bounded to ±10 min so a collector outage degrades to "no entry reference"
+            # Bounded to a 10-minute lookback so a collector outage degrades to "no
+            # entry reference" rather than silently quoting a stale one; the actual
+            # age is carried and printed so the operator sees how close the match was.
+            #
+            # 🔴 2026-08-04 — THE REFERENCE USED TO DRIFT, ONCE, SILENTLY. This search
+            # was ±10 MINUTES AROUND the fill and took the NEAREST row. The collector
+            # samples every 60s, so the moment a POST-fill row landed closer than the
+            # pre-fill one, the "at entry" number CHANGED underneath the position —
+            # and it is the DENOMINATOR of the THINNED/grew arrow the advisor reasons
+            # from. vpos 91: the −52.3 s row gave x4.85 / 0.5517 and the +8.7 s row
+            # x4.08 / 0.5584, so its FIRST consult said "entry x4.8 → THINNED" and
+            # every consult after it said "entry x4.1 → grew" — opposite arrows from
+            # the same position, with nothing in the prompt saying the baseline moved.
+            # FIX: rows at or BEFORE the fill only, newest first.
             try:
                 _t0 = datetime.fromisoformat(vpos['opened_at'])
                 _lo = (_t0 - timedelta(minutes=10)).isoformat()
-                _hi = (_t0 + timedelta(minutes=10)).isoformat()
                 with sqlite3.connect(DB_PATH) as conn:
-                    _rows = conn.execute(
+                    _best = conn.execute(
                         "SELECT ts, max_wall_mult_bid, max_wall_mult_ask, imbalance "
-                        "FROM orderbook_density WHERE source = ? AND ts BETWEEN ? AND ?",
-                        (BOOK_SRC_OKX_4000, _lo, _hi)).fetchall()
-                _best, _best_dt = None, None
-                for _r in _rows:            # ... nearest-by-absolute-distance loop ...
+                        "FROM orderbook_density WHERE source = ? "
+                        "AND ts BETWEEN ? AND ? ORDER BY ts DESC LIMIT 1",
+                        (BOOK_SRC_OKX_4000, _lo, _t0.isoformat())).fetchone()
                 if _best is not None:
                     ctx['sup_entry'] = _best[1] if side == 'LONG' else _best[2]
                     ctx['imb_entry'] = _best[3]
+                    ctx['book_entry_age_s'] = int((_t0 - datetime.fromisoformat(_best[0])).total_seconds())
+                else:
+                    ctx['entry_ref_missing'] = ('no OKX book sample in the 10 minutes BEFORE '
+                                                'the fill (collector gap) — comparison to '
+                                                'entry is not possible')
```

The rendered age line now says **"entry reference sampled N s BEFORE the fill"** — a lookback, never
a look-ahead, and **it cannot change for the life of the position.**

## 3. ITEM ② — THE OKX REPOINT, BOTH HALVES IN ONE CHANGE

**Half A — the writer** (`virtual_trader.execute_entry`): the at-entry book snapshot now comes from
the **OKX-4000 dict the entry advisor was handed** — the same object threaded down, not a re-fetch.

```diff
+        _entry_walls = entry_okx_walls or pre_trade_walls
+        _entry_book_src = ('okx_books_full_4000' if entry_okx_walls
+                           else ('bingx_depth_100' if pre_trade_walls else None))
...
-        _eb_mid = (pre_trade_walls or {}).get('mid') or fill_price
-        _entry_sup_mult, _entry_sup_dist = _nearest_wall(pre_trade_walls, ...)
-        _entry_ob_imb  = (pre_trade_walls or {}).get('imbalance') ...
+        # ALL SIX columns below come from THAT ONE dict — mult, distances and wall
+        # counts describe the same walls, so mixing sources across them would rebuild
+        # the defect being removed one field lower down.
+        _eb_mid = (_entry_walls or {}).get('mid') or fill_price
+        _entry_sup_mult, _entry_sup_dist = _nearest_wall(_entry_walls, ...)
+        _entry_ob_imb  = (_entry_walls or {}).get('imbalance') ...
```

**Half B — the fallback** (`main.py`): when OKX is down, the close prompt now renders **no entry
reference at all.**

```diff
                 ctx.update(
                     sup_now=..., opp_now=..., imb_now=_bx.get('imbalance'),
-                    sup_entry=vpos.get('entry_sup_wall_mult'),
-                    imb_entry=vpos.get('entry_ob_imbalance'),
-                    book_src='BingX depth-100 — RAW, NOT the percentile baseline')
-                if ctx.get('sup_entry'):
-                    ctx['sup_trend'] = 'THINNED' if ctx['sup_now'] < ctx['sup_entry'] else 'grew'
+                    book_src='BingX depth-100 — RAW, NOT the percentile baseline',
+                    entry_ref_missing=('the OKX book (the baseline instrument) is '
+                                       'unavailable right now; the figures below are a '
+                                       'DIFFERENT book, so they cannot be compared to '
+                                       'the entry reading at all'))
```

**Why both halves had to move together:** repointing alone would pair an **OKX entry** against a
**BingX now** — the cross-source comparison `625fedc` removed, rebuilt on the fallback path. The two
books disagree on **which side is heavier in 16 of 18 positions**, so the arrow would not be slightly
wrong, it could point the **wrong way**.

**And the renderer no longer fakes a comparison it did not make** (`claude_advisor._book_block`):

```
BEFORE   Order book NOW vs AT ENTRY — source: BingX depth-100 …
           Supporting wall: entry xn/a -> now x4.1 (n/a)      ← reads like a blank comparison
           Imbalance:       entry n/a -> now 0.54 (n/a)

AFTER    Order book NOW — source: BingX depth-100 — RAW, NOT the percentile baseline
           Supporting wall: now x4.1
           Opposing wall:   now x6.8
           Imbalance:       now 0.54

           NO COMPARISON TO ENTRY IS AVAILABLE for this consultation:
           the OKX book (the baseline instrument) is unavailable right now; the figures
           above are a DIFFERENT book, so they cannot be compared to the entry reading.
           Do NOT infer that the book is unchanged, thinned or grown since entry —
           that question is simply unanswered here.
```

### 🔴 WHAT HAPPENS TO POSITIONS OPENED BEFORE THE REPOINT — your expectation, confirmed

**Confirmed, and by construction rather than by promise:** these columns are written **once, inside
the `INSERT` in `execute_entry`**, and **no code path anywhere rewrites them** (`grep` for each column
name: one writer, in the INSERT tuple). Therefore:

- a position opened before `a637071` **keeps the exact numbers it was opened with**, and its ratio
  keeps the meaning it had at entry;
- only positions opened from now on carry OKX values;
- **`entry_book_src` tells the two apart without guessing** — `okx_books_full_4000` vs
  `bingx_depth_100` vs NULL for legacy rows.

**No in-flight position could change meaning even in principle:** the change was applied with
**0 open positions**, so nothing was mid-life at the moment it landed.

## 4. ITEM ③ — DEPTH PERCENTILE CONFIRMED, AND THE FOUR-STATE REASON NOW REACHES THE EXIT PROMPT

**Depth: confirmed from a real stored consult, not from reading the code.** Trades row **21149**
(2026-08-04 00:26:02, vpos 92):

```
Order-book PERCENTILE scale (baseline: 31001 snapshots of this SAME book)
  Supporting wall = 57th pct
  Opposing wall = 65th pct
  Total depth = 2747 BTC = 26th pct (sampled 29s ago)      ← OKX-vs-OKX, working since ef7fa10
  Imbalance = 85th pct
```

**The intra-conflict state did NOT reach the exit prompt — and now does.** §2.44's fix (`6d9281d`)
corrected the false *"matrix TTL expired"* label (wrong 70 times in 77) on the **entry** side only,
because the close prompt was inside this freeze. The exit side never printed the false string; it
printed **nothing at all**, so the advisor deciding whether to **close** could not see that a tier it
was reading had been **intra-conflicted at entry** rather than counted. Unit-rendered, new output:

```
  1H:  HyperWave OB  (SHORT, weight 1.0, set 12m ago at entry)
  15m: HyperWave OS  (LONG, weight 0.9, set 25m ago at entry)
        NOT counted by the gate — this category's own signals disagree
        (LONG 1.50 / SHORT 1.50 across 3 signals), so it nets NEUTRAL
  5m:  Bearish OB  (SHORT, weight 1.0, set 0m ago at entry)
        NOT counted by the gate — the matrix expired this signal on its category TTL;
        the state-machine slot still holds it
  Agreement at entry: 1H SHORT, 15m LONG, 5m SHORT
```

**Same persisted field, same helper, no re-derivation.** A row written before `6d9281d` carries no
`not_counted` and degrades to the vague-but-true *"the category nets NEUTRAL"* — verified by
unit-rendering a pre-fix fixture.

## 5. ITEM ④ — `entry_wall_baseline_mult` RETIRED

Writer removed (writes NULL); **column and history kept** as recorded historical BingX depth-100.
**The BingX fetch itself is kept deliberately** — it still supplies the labelled `bingx_depth_100`
fallback when OKX is down at fill, so an outage degrades to a *labelled* reading rather than a NULL
row. Deleting the fetch would have been a larger change than the list called for; that choice is
stated rather than assumed.

## 6. SCOPE — EXIT SIDE ONLY, VERIFIED BY GREPPING THE DIFF

| must not be touched | evidence |
|---|---|
| **EMA envelope gate** (applied 14:41) | `EMA_ENVELOPE_GATE_ENABLED=True` by runtime import; not in the diff |
| HTF cascade · Variant-B | `HTF_CASCADE_ENABLED`, `HTF_NEUTRAL_REQUIRE_15M_AGREE` still `True`; `_htf_cascade_gate` not in the diff |
| FLAT floor · score bars | `CONFLUENCE_SCORE_THRESHOLD 3.0` / `CONFLUENCE_FLAT_THRESHOLD 5.0` by import; `_eff_thr` not in the diff |
| risk gates | not in the diff |
| **entry prompt** | `signal_tiers.entry_thesis_lines` has exactly **one** caller — `main.py:2661`, the close-prompt builder. The entry prompt's `render()` is untouched |

Four files, all exit-side: `main.py`, `claude_advisor.py`, `signal_tiers.py`, `virtual_trader.py`.
Backups `*.bak_exitunfreeze_20260804` on each. Applied from flat; restart **15:08:30**; worker up
**15:08:40**; LIVE banner clean.

## 7. WHAT IS NOT PROVEN — and the one thing you asked for that I cannot yet show

🔴 **You asked for a REAL stored exit consult after the restart, with the corrected entry reference
and the OKX values. It does not exist yet, and I will not manufacture one.** An exit consult requires
an **open position**; Titan is flat, and the entry rate is now **0.47/day** behind the envelope gate
applied at 14:41. Nothing has opened since 15:08.

What is verified instead, and by what means:

| claim | how |
|---|---|
| the reference no longer drifts | **replay on real stored rows** — 4 of 4 recent positions changed reference; 15 of 146 consults flip their arrow |
| depth renders against the OKX baseline | **a real stored consult**, row 21149 |
| the four-state reason renders on the exit side | **unit-render**, including a pre-`6d9281d` fixture |
| the no-entry-reference block | **unit-render** of the new branch |
| in-flight positions cannot change meaning | **structural** — one writer, in the INSERT; and 0 open positions at apply time |

**A watcher is armed on `trades` for the first exit consult written after 15:08.** It will be reported
with its row id and the verbatim book block — and if the corrected reference or the OKX values do not
appear in it, that will be reported just as plainly.
