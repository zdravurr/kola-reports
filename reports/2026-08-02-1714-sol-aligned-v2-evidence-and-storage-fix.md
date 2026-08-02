# sol-aligned-v2-evidence-and-storage-fix

_2026-08-02 17:14 UTC_

---

# MERCURY-SOL — DOES THE ALIGNED-V2 OVERRIDE'S EVIDENCE COVER vpos 26? + TWO STORAGE FIXES

**2026-08-02 ~17:25 UTC.** Part 1 is READ-ONLY. Parts 2–3 are storage/documentation, **outside the
entry-prompt freeze** — verified, not assumed (§2.4). `ADVISOR_WALL_ALIGNED_V2` was **not touched**.
Follows `reports/2026-08-02-1655-sol-vpos26-long-forensics.md`. Titan untouched throughout.

---

## 0. ANSWERS, UP FRONT

**1. Was vpos 26 inside the override's evidence base?**
**At the thresholds you named — yes, comfortably. At its actual wall multiple — effectively no.**

The study reproduces **exactly** (n=102, +1.16%/24h, 67% favourable — byte-match to the recorded
figure), so it can be stratified with confidence. Walls of the shape *near AND large*
(<0.35%, >15×) are **37 of 160 rows — 23% of the study — and they drift +0.79%/24h, 68% favourable,
statistically indistinguishable from the cohort as a whole.** The instruction is **not** being
applied outside a population it never contained.

But vpos 26's wall was **×20.3**, the **95th percentile** of the study. Narrow the tail to
`mult ≥ 20 AND dist < 0.35%` and the evidence base collapses to **n=3 rows in the entire 30-day
study — and all three drifted AGAINST the trade, mean −3.20%/24h, 0 of 3 favourable.**

So the honest finding is a *gradient*, not a boundary: the override is well-evidenced at ×5–19 and
runs out of data entirely at ×20+, where the three observations it does have point the other way.
A headline computed over a distribution whose **q3 is 16.8×** was applied to a case at ×20.3.

**And two corrections to the premise itself:**

- **The n=102 headline is the wrong arm for this trade.** n=102/+1.16%/67% is the **`trend_1h=neutral`**
  cohort. vpos 26 was **`trend_1h=bull`** — its arm is **n=58, +0.23%/24h, 64% fav**, a mean **5×
  smaller** (both figures reproduce exactly; the bull arm's n was never written down before).
- **🔴 The study never measured the three things that made this wall distinctive.**
  `skip_attribution` records exactly three wall facts: `nearest_wall_price`, `wall_strength`,
  `wall_distance_pct`. *Larger than the next ask wall by 2.4×*, *closer than either bid wall*,
  *dominant on its side* — **none of these was ever a variable.** Not excluded: never captured.
  The study is structurally incapable of saying whether wall dominance matters, in either
  direction. **That is the finding that stands independent of any outcome.**

**2. Storage overwrite — FIXED and LIVE.** New column `advisor_book_json` holds the OKX-4000 book
the advisor was shown; `orderbook_json` keeps its existing meaning and writers. The learning loop
now reads the advisor's book. Verified writing live at 17:10:07. Past executed rows are **not
recoverable** — your expectation is confirmed, and it is recorded below with what *is* still
readable.

**3. Both documentation corrections applied** to `OPEN-ITEMS-SOL.md`.

---

# PART 1 — THE OVERRIDE'S EVIDENCE, STRATIFIED

## 1.1 The study reproduces exactly — so the stratification is trustworthy

Before stratifying anything I re-derived the recorded headline from the raw tables. Cohort:
`skip_attribution.status='ai_skipped'` ∧ `direction='LONG'` ∧ `trades.trend_1h ∈ {bull,neutral}` ∧
`trades.srv_adx_1h ≥ 25` ∧ `ai_reason` mentions a wall ∧ 24h drift matured, window
**2026-06-04 → 2026-07-04**. Drift is `skip_drift_samples.horizon='24h'`, already
direction-normalised (`_compute_drift_pct`: **positive = the skip was wrong**).

| arm | recorded in `config.py` / memory | **reproduced here** |
|---|---|---|
| `trend_1h=neutral`, ADX≥25 | "+1.16%/24h 67% fav n=102" | **n=102, +1.16%, 67%** ✅ byte-match |
| `trend_1h=bull`, ADX≥25 | "+0.23% 64%" (n never recorded) | **n=58, +0.23%, 64%** ✅ byte-match |

Both figures land exactly. Every number below comes from the same reconstruction.

## 1.2 (a) DISTRIBUTION of the overhead wall in the population that justified the override

100% of the study population has a recorded nearest opposing (ask) wall — it is all wall-cited
skips by construction, so there is no missing-data problem here.

| | min | q1 | **median** | q3 | p90 | max |
|---|---|---|---|---|---|---|
| **NEUTRAL arm** (n=102) — multiple | 4.1 | 9.3 | **13.7** | 16.8 | 19.4 | 23.8 |
| **NEUTRAL arm** — distance % | 0.000 | 0.101 | **0.177** | 0.284 | 0.398 | 0.533 |
| **BULL arm** (n=58, vpos 26's arm) — multiple | 5.3 | 10.9 | **14.6** | 16.9 | **18.8** | **21.4** |
| **BULL arm** — distance % | 0.000 | 0.069 | **0.176** | 0.324 | 0.424 | 0.549 |
| **BOTH** (n=160) — multiple | 4.1 | 9.3 | **13.9** | 16.8 | 19.1 | 23.8 |
| **BOTH** — distance % | 0.000 | 0.087 | **0.177** | 0.294 | 0.413 | 0.549 |

**vpos 26: multiple ×20.3, distance 0.313%.** Its distance is utterly ordinary — 0.313% sits
between the median (0.177%) and q3 (0.294%), and the *typical* wall in this study is **nearer** than
vpos 26's was. Its **multiple is not**: ×20.3 is above the bull arm's **p90 (18.8)** and close to
that arm's **maximum (21.4)**.

**Count with `dist < 0.35%` AND `mult > 15×` — the sub-population you asked for:**

| arm | near+large | as % of arm |
|---|---|---|
| NEUTRAL | **20** of 102 | 20% |
| BULL | **17** of 58 | 29% |
| **BOTH** | **37** of 160 | **23%** |

## 1.3 (b) Drift restricted to that sub-population

| population | n | drift @24h mean | median | favourable |
|---|---|---|---|---|
| **NEUTRAL arm — all** | 102 | +1.16% | +1.73% | 68/102 = 67% |
| · near only (<0.35%) | 83 | +1.34% | +2.26% | 58/83 = 70% |
| · large only (>15×) | 39 | +0.66% | +0.73% | 22/39 = 56% |
| · **near AND large** | **20** | **+0.93%** | +1.14% | **12/20 = 60%** |
| **BULL arm — all** | 58 | +0.23% | +1.22% | 37/58 = 64% |
| · near only | 46 | −0.06% | +1.12% | 27/46 = 59% |
| · large only | 25 | +0.73% | +1.49% | 19/25 = 76% |
| · **near AND large** | **17** | **+0.62%** | +1.25% | **13/17 = 76%** |
| **BOTH — all** | 160 | +0.82% | +1.34% | 105/160 = 66% |
| · **near AND large** | **37** | **+0.79%** | +1.19% | **25/37 = 68%** |
| · everything else | 123 | +0.83% | +1.47% | 80/123 = 65% |

**Read this straight: at your thresholds, the answer is no, the override is not being applied
outside its evidence.** Near+large is 23% of the study and its drift (+0.79%, 68% fav) is
indistinguishable from the whole (+0.82%, 66% fav). In vpos 26's own **bull** arm, near+large is
actually the *strongest* slice in it (+0.62%, **76%** fav vs the arm's +0.23%, 64%).

**Now the tail, which is where it breaks.** vpos 26's multiple was ×20.3, not ×15:

| population | n | drift @24h mean | favourable |
|---|---|---|---|
| BULL arm, `mult ≥ 20` AND `dist < 0.35%` | **2** | **−3.56%** | **0 / 2** |
| BOTH arms, `mult ≥ 20` AND `dist < 0.35%` | **3** | **−3.20%** | **0 / 3** |

**Three rows in a 160-row study, and every one of them said skip-was-right, hard — a mean of
−3.20% against the trade at 24h.** Rows with `mult ≥ 20.3` at all are 8 of 160 (5.0%); vpos 26 sits
at the **95th percentile** of a distribution the override was calibrated on at its middle.

**The precise, defensible statement:** the override's evidence covers *near* walls thoroughly, and
*large* walls up to about ×19 adequately. Beyond ×20 it has **three observations, all negative**,
and that tail is invisible inside a headline of "+1.16%, 67% favourable". This is not a claim that
the override is wrong. It is a claim that **at vpos 26's wall size the override had essentially no
evidence, and what little it had pointed the other way** — and that is true regardless of how
vpos 26 itself resolves.

### 1.3.1 🔴 The finding that does not depend on any of the above

`skip_attribution` (`skip_attribution.py:273-277`) stores, for each skip, **one** wall:

```python
wall_price, wall_strength = _nearest_opposing_wall(norm_dir, pre_trade_walls)   # walls[0] only
wall_dist_pct = abs(wall_price - anchor) / anchor * 100.0
```

`_nearest_opposing_wall` returns `walls[0]` — nearest-to-mid, on the opposing side, **and nothing
else**. Not the second ask wall. Not any bid wall. Not the count. Not the ratio between them.

So the three attributes that made vpos 26's book distinctive —

- the wall was **2.4× larger than the next ask wall** (×20.3 vs ×8.3),
- it was **closer than either bid wall** (+0.30% vs −0.38% / −1.06%),
- it **dominated its own side** of the book,

— were **never variables in the study that justified the override.** The study cannot support or
refute them. A future measurement could capture them cheaply (the full `pre_trade_walls` dict is
already in hand at `on_skip`), but as it stands, **"is a dominant wall different from a merely
large one?" has never been asked of this data.** Recorded, not acted on.

### 1.3.2 Two further caveats, stated because they bound everything above

- **Drift is not PnL, and here they diverge sharply.** `_compute_drift_pct` is point-in-time price
  at the horizon versus the anchor — **no stop, no trail, no fees**. A skip scored "favourable"
  can be a trade that was stopped out hours earlier. Measured against the five realised flips
  (§1.4.2), the study's own metric would have graded **exactly one** of the four closed LONG flips
  favourable — **vpos 18, the one that lost the most money (−$234.04)**. Every entry this override
  creates is stop-sensitive *by construction*, because it enters under a nearby opposing wall; the
  metric that justified it is blind to precisely that.
- **n is small everywhere in the tail.** n=3 refutes nothing. What n=3 establishes is the *absence
  of evidence*, not evidence of absence. The 30-closed-trade tripwire
  (`project_mercury_sol_strategy_diagnosis`) still applies to every number in this document.

## 1.4 (c) FULL FIRING HISTORY since 2026-07-02

The journal only retains from **2026-07-30 20:55**, so the history was reconstructed from the DB
instead — possible because the 2026-08-01 provenance backfill stamped `ai_system_prompt` with the
prompt that actually produced each verdict. An aligned-LONG flip is exactly a row whose
`ai_system_prompt` contains `_WALL_RULE_V2_ALIGNED`.

**Independent check that the identification is complete:** the 9 flips that became positions have
8 closed, net **−$616.15** — byte-matching the figure independently derived in
`reports/2026-08-01-2340-sol-sysprompt-backfill-executed.md`.

### 1.4.1 Every aligned-LONG flip — 17 rows, 2026-07-10 → 2026-08-02

| trades id | when (UTC) | status | vpos | conf | trend_1h | ADX 1h | nearest ask wall | \|dist\| | mult | outcome | PnL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8446 | 07-10 08:30 | executed | **16** | 0.72 | bull | 27.0 | $79.25 | 0.113% | 5.9 | **sl** | **−194.70** |
| 8447 | 07-10 08:35 | observed_skipped | — | 0.72 | bull | 27.0 | $79.25 | 0.126% | 5.5 | — | — |
| 9842 | 07-14 15:45 | executed | **18** | 0.72 | bull | 27.5 | $77.75 | 0.387% | 15.0 | **sl** | **−234.04** |
| 9875 | 07-14 19:00 | observed_skipped | — | 0.78 | bull | 30.1 | $77.25 | 0.000% | 7.9 | — | — |
| 9876 | 07-14 19:05 | observed_skipped | — | 0.78 | bull | 30.1 | $77.25 | 0.078% | 7.6 | — | — |
| 9878 | 07-14 19:10 | observed_skipped | — | 0.78 | bull | 30.2 | $77.25 | 0.000% | 9.5 | — | — |
| 9880 | 07-14 19:20 | observed_skipped | — | 0.82 | bull | 30.2 | $77.25 | 0.129% | 4.8 | — | — |
| 9881 | 07-14 19:20 | observed_skipped | — | 0.78 | bull | 30.2 | $77.25 | 0.129% | 4.8 | — | — |
| 9882 | 07-14 19:20 | observed_skipped | — | 0.78 | bull | 30.2 | $77.25 | 0.129% | 4.8 | — | — |
| 10003 | 07-15 04:45 | observed_skipped | — | 0.72 | bull | 33.0 | $78.25 | 0.449% | 17.3 | — | — |
| 11180 | 07-19 06:50 | observed_skipped | — | 0.78 | bull | 28.9 | $76.25 | 0.250% | 19.2 | — | — |
| 11181 | 07-19 06:50 | executed | **21** | 0.78 | bull | 28.9 | $76.25 | 0.250% | 18.8 | **trail** | **+33.66** |
| 11679 | 07-21 03:10 | executed | **22** | 0.78 | bull | 25.8 | $78.25 | 0.166% | 5.1 | **sl** | **−203.42** |
| 11680 | 07-21 03:10 | observed_skipped | — | 0.78 | bull | 25.8 | $78.25 | 0.166% | 5.1 | — | — |
| 11698 | 07-21 05:30 | observed_skipped | — | 0.78 | bull | 26.4 | $78.25 | 0.166% | 4.4 | — | — |
| 11700 | 07-21 05:35 | observed_skipped | — | 0.78 | bull | 26.4 | $78.25 | 0.166% | 4.9 | — | — |
| **15093** | **08-02 05:00** | **executed** | **26** | 0.78 | bull | 29.3 | **$73.75** | **0.313%** | **20.3** | **OPEN** | **−46.21** |

Wall figures parsed from each row's own stored `ai_user_prompt`. `observed_skipped` = the override
returned `execute` but no position opened — the side already held one
(`ux_vpos_one_open_per_side`); several are duplicate webhook fires in the same minute.

Two structural notes: **every single aligned-LONG flip had `trend_1h=bull`** — the 2026-07-04
widening to `neutral` (the arm carrying the n=102 headline) has produced **zero** live flips in a
month. And the override sat **idle for 8 days** after going live 07-02; the first flip was 07-10.

### 1.4.2 The scoreboard

**Aligned-LONG (live 2026-07-02): 17 flips → 5 positions → 4 closed.**

| vpos | wall shape | outcome | PnL | drift @24h (study's own metric) | stop hit within 24h |
|---|---|---|---|---|---|
| 16 | ×5.9 @ 0.113% — near, small | sl | **−194.70** | −1.71% | **YES, at 5.8h** |
| 18 | ×15.0 @ 0.387% — neither | sl | **−234.04** | **+0.85%** ← metric says favourable | no (stopped later) |
| 21 | ×18.8 @ 0.250% — **NEAR+LARGE** | trail | **+33.66** | −0.53% | no |
| 22 | ×5.1 @ 0.166% — near, small | sl | **−203.42** | −0.65% | no (stopped later) |
| 26 | ×20.3 @ 0.313% — **NEAR+LARGE** | **OPEN** | −46.21 | n/a | no (within $0.08) |

**Net on the 4 closed: −$598.50. One win, three stop-outs.**

**Aligned-SHORT (live 2026-07-04): 16 flips → 4 positions, all closed.**

| vpos | outcome | PnL |
|---|---|---|
| 17 | sl | +0.86 |
| 19 | exit_signal | +89.00 |
| 24 | sl | −234.03 |
| 25 | trail | +126.52 |
| | **net** | **−$17.65** |

**Combined: 8 closed flips, net −$616.15** — the cross-check that the reconstruction is complete.

**Fire rate**, over the journal's full retention (2026-07-30 20:55 → 2026-08-02 17:2x):

| | FLIP | HELD |
|---|---|---|
| aligned-**LONG** | **1** | **42** |
| aligned-**SHORT** | **1** | **14** |

The override is rare: roughly **1 fire per 43** eligible aligned-LONG consultations. HELD counts
before 07-30 are gone with the journal and are not recoverable.

**Where the near+large shape lands in live results:** exactly two flips have ever had it —
**vpos 21 (×18.8), the only profitable LONG flip in the book, and vpos 26 (×20.3), currently
−0.36R.** One each way, n=2. That settles nothing and is reported only so it cannot later be
quoted selectively.

**`ADVISOR_WALL_ALIGNED_V2` and `ADVISOR_WALL_ALIGNED_SHORT_V2` remain `True`, untouched.**

---

# PART 2 — THE STORAGE OVERWRITE, FIXED

**Applied and LIVE 2026-08-02 17:08:41, worker pid 1496095.** Backups first:
`main.py.bak_advisorbook_20260802`, `signal_weights.py.bak_advisorbook_20260802`,
`trades.db.bak_pre_advisorbook_20260802` (43,732,992 bytes).

## 2.1 What was wrong

`trades.orderbook_json` had two writers. The advisor path stored the OKX `books-full` depth-4000
wall dict it actually showed Claude; the fill-time microstructure capture then **overwrote** it
with a Bybit depth-20 snapshot. On every **executed** row the advisor's input was destroyed —
15093 stores `"walls_ask": []` where the advisor was shown the **×20.3 wall at $73.75 that produced
the verdict** — and `signal_weights.py:211` read that wrong book for post-trade learning.
**Skip** rows were never affected.

## 2.2 The patch — 3 hunks, purely additive

```diff
--- a/main.py
+++ b/main.py
@@ (schema migration list, ~line 755)
             ('orderbook_json',           'TEXT'),
             ('tape_json',                'TEXT'),
+            # 2026-08-02 — THE ADVISOR'S OWN BOOK, PRESERVED. `orderbook_json` is
+            # written TWICE on an executed entry: the advisor path stores the OKX
+            # books-full depth-4000 wall dict it actually showed Claude, and then the
+            # fill-time microstructure capture (microstructure._persist) OVERWRITES it
+            # with a Bybit depth-20 snapshot. The advisor's input was therefore
+            # destroyed on every executed row — 15093 stores `walls_ask: []` where the
+            # advisor was shown a ×20.3 wall at $73.75 that produced the verdict.
+            # This column holds the OKX-4000 dict the advisor saw and is written ONCE,
+            # on the advisor path only. Nothing overwrites it. `orderbook_json` keeps
+            # its existing meaning and its existing writers unchanged (skip rows: the
+            # OKX book; executed rows: the fill-time Bybit snapshot) so no current
+            # reader changes behaviour. Storage only — outside the entry-prompt freeze;
+            # the advisor reads no column.
+            ('advisor_book_json',        'TEXT'),
@@ (advisor path update_trade, ~line 3159)
-                 orderbook_json=(json.dumps(_pre_walls) if _pre_walls else None))
+                 orderbook_json=(json.dumps(_pre_walls) if _pre_walls else None),
+                 # 2026-08-02: the SAME dict, in a column nothing overwrites. On an
+                 # executed row microstructure._persist replaces orderbook_json at
+                 # fill with the Bybit depth-20 snapshot; advisor_book_json is the
+                 # permanent record of what the entry advisor was actually shown.
+                 advisor_book_json=(json.dumps(_pre_walls) if _pre_walls else None))

--- a/signal_weights.py
+++ b/signal_weights.py
@@ _attempt_learning, ~line 211
-    book_raw = row_dict.get('orderbook_json')
+    # 2026-08-02 — READ THE BOOK THE ADVISOR ACTUALLY SAW.
+    # `orderbook_json` is overwritten at fill by the Bybit depth-20 microstructure
+    # capture, so on every executed row this loop was attributing the outcome to a
+    # book the entry decision never used — and one that reports `walls_ask: []`
+    # where the advisor was shown the wall that produced the verdict.
+    # `advisor_book_json` (main.py, same commit) is the OKX-4000 dict the advisor
+    # was shown, written once and never overwritten. Prefer it; fall back to
+    # `orderbook_json` for the historical rows that predate the column.
+    # It is also the strictly richer input: the OKX wall dicts carry `mult`
+    # (bucket volume / that side's mean bucket volume), which the Bybit depth-20
+    # walls do not — so compact_for_llm's top_wall_bid/top_wall_ask now reach the
+    # learning prompt with the wall's SIZE, not just its price.
+    # FREEZE-SAFE, verified: the learning_* columns this function writes are
+    # write-only — nothing SELECTs them. The combo weight the entry advisor sees
+    # comes from get_weight() -> signal_weights.weight, driven solely by
+    # record_outcome(combo_key, pnl). This changes no value on the entry path.
+    book_raw = row_dict.get('advisor_book_json') or row_dict.get('orderbook_json')
+    book_src = ('advisor_okx4000' if row_dict.get('advisor_book_json')
+                else ('microstructure_fill' if row_dict.get('orderbook_json') else None))
     tape_raw = row_dict.get('tape_json')
@@ after compact_for_llm, ~line 258
     compact_tape = compact.get('tape') if compact else None
+    # Provenance in the log, so a future audit never has to guess which book the
+    # learning verdict was formed against (the whole defect being fixed here).
+    log.info("learning trade=%s book_source=%s", trade_id, book_src)
```

## 2.3 Both books preserved, clearly named

| column | holds | written by | overwritten? |
|---|---|---|---|
| **`advisor_book_json`** *(new)* | the **OKX books-full depth-4000** wall dict the entry advisor was shown — `mid`, `imbalance`, `walls_bid/ask` each with `price`/`vol`/`mult`, `depth`, `wall_threshold_mult` | `main.py:3164`, advisor path, **once** | **never** |
| `orderbook_json` *(unchanged)* | skip rows: the same OKX dict · executed rows: the **fill-time Bybit depth-20** microstructure snapshot | `main.py:3159` then `microstructure.py:222` | yes, as before |

`orderbook_json`'s semantics, writers and values are **deliberately untouched** — no existing
reader changes behaviour, and the Titan-parity shape is preserved. It is not in the optimizer's
`CANDIDATE_FIELDS`; `signal_weights.py:211` was its only real consumer.

**The overwrite is now structurally impossible, not merely unlikely** — a full-codebase grep shows
`advisor_book_json` has exactly **one** writer:

```
main.py:3164        advisor_book_json=(json.dumps(_pre_walls) ...)     <- the only write
signal_weights.py:227/228                                              <- reads only
```

and the only `UPDATE ... SET orderbook_json` in the codebase (`microstructure.py:222`) does not
name the new column.

## 2.4 🔴 The freeze check — verified, not assumed

`_attempt_learning` is a Claude call, so "does changing its input touch the frozen surface?" had to
be answered before touching it. **It does not**, and here is the chain:

1. `_attempt_learning` writes only `trades.learning_*`.
2. `learning_*` is **write-only** — a codebase-wide grep finds no `SELECT` of
   `learning_influence` / `learning_confidence` / `learning_liquidity_factor` anywhere.
3. The one advisor-visible quantity that could plausibly depend on learning is the **combo weight**
   (`Combo weight: 1.00` in the entry prompt). It comes from
   `signal_weights.get_weight(combo)` → `SELECT weight FROM signal_weights WHERE combo_key=?`,
   and that table is written **only** by `record_outcome(combo_key, pnl)` — pure realised PnL.

**Nothing on the entry path can move.** The 200-consultation window is **not** reset.

## 2.5 Verified live

| check | result |
|---|---|
| `py_compile main.py signal_weights.py` | ✅ OK |
| service restarted, active | ✅ 17:08:41, pid **1496095** |
| `advisor_book_json` column exists | ✅ |
| **vpos 26 survived the restart** | ✅ open, entry 73.53, SL 72.59, water_mark 73.65 |
| errors / tracebacks since restart | ✅ none |
| **`claude_advisor.py` / `config.py` modified?** | ✅ **NO** — mtimes still 08-01 20:54 / 08-02 13:34 |
| new column populated on a live consultation | ✅ **row 15221, 17:10:07 — OKX-4000 dict present** |
| entry prompt byte-identical post-restart | ✅ row 15221 carries the 1H tier and `Of the 3 tier(s) shown` |

## 2.6 🔴 Past rows: NOT recoverable — your expectation is confirmed

**Every `trades.db.bak_*` snapshot already carries the Bybit-20 overwrite** for all three executed
entries. The overwrite lands seconds after the advisor write, so no backup ever caught the window:

```
trades.db.bak_pre_testcleanup_20260801     | 13973 | bybit-20
trades.db.bak_pre_isvirtual_backfill_...   | 13973, 14988 | bybit-20
trades.db.bak_pre_phase2_20260801          | 13973, 14988 | bybit-20
trades.db.bak_pre_5a_backfill_20260801     | 13973, 14988 | bybit-20
trades.db.bak_pre_sysprompt_backfill_...   | 13973, 14988 | bybit-20
```

**The dict is gone for 13973, 14988 and 15093, permanently. Recorded.**

What **is** still readable, for those three and every other row, is the **rendering** inside
`ai_user_prompt`: `mid`, `Imbalance ±1%`, the depth (`8000 levels`), the threshold (`>4x`), and up
to **five** walls per side with bucket-centre price and `mult`. **Permanently lost:** per-bucket
USDT `vol`, and any sixth-or-later wall on a side (`_wall_list` slices `[:5]`).

**Deliberately NOT backfilled.** Reconstructing the dict from its own rendering would put an
authoritative column name on lossy derived data — the precise failure class this project keeps
hitting (a canonical artefact that nobody can tell from a captured one). Anyone needing those three
books reads the prompt text and knows they are reading a rendering.

---

# PART 3 — THE TWO DOCUMENTATION CORRECTIONS

Both applied to `OPEN-ITEMS-SOL.md` (backup `OPEN-ITEMS-SOL.md.bak_20260802_1710`).

## 3a. STANDING FACTS — `ai_system_prompt` line corrected

Was: *"`trades.ai_system_prompt` always stores the V1 base prompt, even when a V2/aligned prompt
produced the verdict."* Now struck through and replaced, citing row 15093 as live proof: its stored
prompt is byte-identical to `_ENTRY_SYSTEM_V2_ALIGNED`, and that row *was* an aligned-LONG flip.

The correction keeps the part that is **still true and still unfixed**: for the **32 historical**
flips, `ai_raw_response` holds the **V1** response while `ai_reason`/`ai_confidence` hold the
V2-aligned one. The flip's own raw text is permanently unrecoverable pre-2026-08-01. Post-fix rows
carry the V2 raw — 15093 does, which is how §1.4.1's wall figures were parseable at all.

## 3b. The 1H-flip item — CLOSED

The `applied-but-unconfirmed` block is replaced with the confirmation, the evidence table, and a
pointer to the 16:55 forensics §4.2:

| check (all 74 window consultations, ≥ 2026-08-01 17:13:02) | count |
|---|---|
| carrying the 1H tier line **and** `Of the 3 tier(s) shown` | **74 / 74** |
| carrying `1H LuxAlgo tier: NOT SHOWN` | **0** |
| carrying the old false `The 3 timeframes are aligned` | **0** |

The original requirement is retained verbatim as a block quote so nobody re-derives it, plus one
addition that was **not** in the original: this is a property of the **running worker**, not a
permanent fact. It was verified against pid 1126633→1444690 and re-verified against pid 1496095
after today's restart (row 15221). **Any future restart on a changed config must be re-confirmed
the same way.**

---

## ROLLBACK

```bash
cd /mnt/volume_nyc1_1780480650620/mercury-sol
cp main.py.bak_advisorbook_20260802          main.py
cp signal_weights.py.bak_advisorbook_20260802 signal_weights.py
cp OPEN-ITEMS-SOL.md.bak_20260802_1710       OPEN-ITEMS-SOL.md
systemctl restart mercury-sol
# the advisor_book_json COLUMN can stay — it is additive and unread by the old code.
# DB rollback (only if ever needed): trades.db.bak_pre_advisorbook_20260802
```

## REPRODUCE PART 1

```bash
# the study, reproduced exactly (n=102 / +1.16% / 67%)
sqlite3 "file:/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db?mode=ro" "
select count(*), round(avg(d.drift_pct),2), sum(d.drift_pct>0)
from skip_attribution sa join trades t on t.id=sa.trades_row_id
join skip_drift_samples d on d.skip_attr_id=sa.id and d.horizon='24h'
where sa.status='ai_skipped' and sa.direction='LONG'
  and sa.skip_ts>='2026-06-04' and sa.skip_ts<'2026-07-04'
  and lower(t.trend_1h)='neutral' and t.srv_adx_1h>=25
  and lower(sa.ai_reason) like '%wall%' and d.drift_pct is not null;"

# the near+large tail: add   and sa.wall_strength>=20 and sa.wall_distance_pct<0.35
# the full flip history:
sqlite3 "file:.../trades.db?mode=ro" "select id,timestamp,status from trades
  where ai_system_prompt like '%WALL RULE — overhead ask wall on a trend-aligned LONG%';"
```

_2026-08-02. Mercury-SOL is PAPER. `ADVISOR_WALL_ALIGNED_V2` unchanged and inside the freeze;
the entry prompt is byte-identical and the 200-window is not reset. Titan untouched._
