# titan-entry-advisor-percentiles-and-two-entry-forensics

_2026-07-29 10:11 UTC_

---

**TL;DR** — Part 1 is applied, committed (`8b15ecc`) and live: the entry advisor now reads the same
order-book percentile scale the exit advisor has had since `ef7fa10`, and the hard-coded word
"Massive" is gone. Part 2's headline is not about either advisor: **`market_regime` does not measure
the market.** It is `TREND` whenever a 1H LuxAlgo signal is live and `FLAT` when none is — over the
last 14 days ADX(1h) is **26.66 under FLAT vs 25.52 under TREND**, i.e. the label is very slightly
*anti*-correlated with trend strength. That label chooses the score threshold (2.0 vs 5.0). The
SHORT scored **4.25** — it cleared the 2.0 TREND bar and would have been **rejected by the 5.0 FLAT
floor**. The label was outcome-determining for it.

---

# PART 1 — §2.3 CLOSED: the entry advisor has the percentile scale

**Commit `8b15ecc`** on top of `f0a8d30`. `titan.service` restarted 09:56:06 UTC, worker 4017679
booted 09:56:15 from files written 09:54 — the fix is *in memory*, not only on disk.

## What was wrong

`claude_advisor._format_pre_trade_walls()` printed the literal word **"Massive"** for every wall
above `4.0x`. Against the `orderbook_density` baseline (23,054 snapshots, 2026-07-13 → now):

| column | p5 | p25 | **p50** | p75 | p95 | max |
|---|---|---|---|---|---|---|
| `max_wall_mult_bid` | 0.00 | 4.55 | **5.44** | 6.98 | 11.67 | 22.21 |
| `max_wall_mult_ask` | 0.00 | 4.74 | **5.97** | 7.99 | 14.78 | 27.86 |
| `imbalance` | 0.418 | 0.457 | **0.485** | 0.520 | 0.569 | 0.663 |
| `total_depth_btc` | 2449 | 2789 | **3013** | 3214 | 3549 | 4196 |

The threshold that fired the alarm — 4.0x — sits **below the 25th percentile**. The median book
carries a 5.44x bid wall. "Massive" was a constant, and the advisor quoted it back as evidence: the
SHORT that died at its stop was entered with the reason *"Massive ask walls above entry absorb
resistance"* over an ask wall at the **80th** percentile.

## What was applied

- `main._entry_book_pct(walls)` — new, calls the **same `_exit_pct()`** against the **same
  `orderbook_density`** baseline the exit advisor reads.
- `claude_advisor._format_pre_trade_walls(walls, book_pct)` — every wall figure, the imbalance and
  the depth now carry their percentile, in the exit side's format, including the
  *"~50th percentile is ORDINARY, not significant"* note. The word "Massive" is deleted.
- The system prompt's opposing-wall **HARD RULE** said *"a massive limit wall (volume marked with a
  multiplier, e.g. x8.3)"* — the same defect in the rule that **consumes** the label. It now says to
  judge thickness by the printed percentile and never by the raw multiple. **The rule's consequence
  is unchanged; only the measure of "thick" is.** Flagging this explicitly: §2.3 asked for the label,
  and I extended the fix to the rule that reads it. Trivial to revert if that is not wanted.
- Both `consult_for_entry` call sites (plain-text 5m path L1945, state-machine path L3471) wired.

**Apples-to-apples by construction.** The entry block is built from
`liquidity_zones.fetch_pre_trade_walls()` — the OKX books-full depth-4000 snapshot — and
`orderbook_collector` samples **that same book** every 60s with the same $bucket and the same
`mult = bucket_vol / mean_bucket_vol` rule. Verified live at 09:47 UTC: entry path x8.8 / x4.3,
imbalance 0.487; the collector row 60s later x9.23 / x4.67, imbalance 0.478. (The entry path buckets
USDT and the collector buckets BTC; across the ~0.7% of mid that 4000 levels span, price is
near-constant, so the ratio is the same number to a fraction of a percent.)

Depth comes from the **latest collector row**, not the walls dict, whose `depth` field is a *level
count* (8000) and not a volume; the row's age is rendered so a stale sample is visible, never silent.

> 🔴 **CALIBRATION, NOT JUDGEMENT.** No statistic, win rate, PnL or historical performance is
> attached to any book figure — the same line `f0a8d30` drew for the 1H signal identity. The advisor
> learns whether a wall is ordinary or extreme *for this book*. It is told nothing about what that
> implies. Read-only and all-or-nothing: any failure returns `{}` and the block renders as before.

## Rendered entry prompt, BEFORE and AFTER, on two real decisions

Baseline truncated to snapshots at or before each entry, so these are the percentiles the advisor
would genuinely have seen at that moment.

### vpos 83 SHORT — `trades.id=19021`, 2026-07-28 01:00:17 UTC

```
--- BEFORE (exactly what was sent, f0a8d30) ---
Order book (pre-trade, 8000 levels):
  Mid: $63,423.05  |  Imbalance +/-1%: 0.56 (bid-heavy)
  Massive bid walls (>4x avg vol): $63,402.50 (x5.9), $63,387.50 (x4.2)
  Massive ask walls (>4x avg vol): $63,567.50 (x4.1), $63,577.50 (x4.7), $63,637.50 (x9.6)

--- AFTER (8b15ecc) ---
Order book (pre-trade, 8000 levels):
  Mid: $63,423.05  |  Imbalance +/-1%: 0.56 (bid-heavy)  - 92th pct
  Bid walls (>4x avg bucket vol): $63,402.50 (x5.9), $63,387.50 (x4.2)  - largest x5.9 = 61th pct
  Ask walls (>4x avg bucket vol): $63,567.50 (x4.1), $63,577.50 (x4.7), $63,637.50 (x9.6)  - largest x9.6 = 80th pct
  Book depth: 3,097 BTC - 61th pct, sampled 0s ago
Order-book PERCENTILE scale (baseline: 21120 snapshots of this same OKX depth-4000 book)
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile: ~50th percentile is ORDINARY,
  not significant.
```

### vpos 84 LONG — `trades.id=19214`, 2026-07-28 17:00:12 UTC

```
--- BEFORE (exactly what was sent, f0a8d30) ---
Order book (pre-trade, 8000 levels):
  Mid: $63,998.95  |  Imbalance +/-1%: 0.45 (ask-heavy)
  Massive bid walls (>4x avg vol): $63,862.50 (x4.3)
  Massive ask walls (>4x avg vol): none

--- AFTER (8b15ecc) ---
Order book (pre-trade, 8000 levels):
  Mid: $63,998.95  |  Imbalance +/-1%: 0.45 (ask-heavy)  - 20th pct
  Bid walls (>4x avg bucket vol): $63,862.50 (x4.3)  - largest x4.3 = 18th pct
  Ask walls (>4x avg bucket vol): none  - largest x0.0 = 0th pct
  Book depth: 2,743 BTC - 20th pct, sampled 0s ago
Order-book PERCENTILE scale (baseline: 22064 snapshots of this same OKX depth-4000 book)
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile: ~50th percentile is ORDINARY,
  not significant.
```

And live through the **real** running path at 09:52 UTC (`liquidity_zones` → `main._entry_book_pct`
→ `claude_advisor`), proving the wiring, not just the renderer:

```
Order book (pre-trade, 8000 levels):
  Mid: $64,646.85  |  Imbalance +/-1%: 0.46 (ask-heavy)  - 26th pct
  Bid walls (>4x avg bucket vol): $64,447.50 (x5.5), $64,252.50 (x9.8)  - largest x9.8 = 91th pct
  Ask walls (>4x avg bucket vol): $65,002.50 (x6.9)  - largest x6.9 = 65th pct
  Book depth: 3,345 BTC - 87th pct, sampled 40s ago
Order-book PERCENTILE scale (baseline: 23062 snapshots of this same OKX depth-4000 book)
```

**One gap found while doing this, NOT fixed:** the *exit* prompt has a `Total depth = {depth_pct}`
line that has **always rendered `n/a`** — `_build_exit_context` never sets `depth_pct`. Two lines to
fix the same way the entry side now does it. Left alone because it is the exit path and outside
what was asked; recorded here so it is not lost.

---

# PART 2 — WHY DID THESE TWO ENTRIES HAPPEN (read-only)

## 2.1 The two trades

| | **vpos 83** | **vpos 84** |
|---|---|---|
| Side | **SHORT** | **LONG** |
| Entry | 2026-07-28 01:00:17 @ **63,449.7** | 2026-07-28 17:00:12 @ **63,997.3** |
| Exit | 2026-07-29 06:28:00 @ 64,311.4 — **stop** | **OPEN** (29th 09:55 @ 64,656.7) |
| PnL | gross **-135.80**, fees 10.07, funding -2.20, **net -143.67** | unrealised **+0.760R** |
| 1R | 836.7 (SL 64,286.4) | 867.4 (SL 63,129.9) |
| Confluence score | **4.25** vs threshold **2.0** | **7.50** vs threshold **2.0** |
| `market_regime` | **TREND** | **TREND** |
| trend 1d/4h/1h/15m/5m | neutral / **bear / bear / bear / bear** | neutral / **neutral / neutral** / bull / bull |
| MTF alignment | **4 / 4** | **2 / 4** |
| ADX 1h / 4h (/15m) | 26.34 / 18.90 (39.80) | 30.71 / 24.55 (20.74) |
| 1H signal | **Trend Catcher Down** (w 1.0, 1.0h old) | **Bullish Confirmation** (w 0.7, 1.0h old) |
| 15m signal | **`None`** — see §2.8 | **`None`** — see §2.8 |
| 5m trigger | **Within Bearish OB** | **Bullish OB Mitigated** |
| Advisor | `execute`, conf **0.78** | `execute`, conf **0.72** |

**Advisor reason, VERBATIM — vpos 83:**

> Strong multi-TF SHORT confluence: 1H/15m/5m all BEAR with high ADX (26.3→39.8→62.9). 4H confirms
> BEAR. Massive ask walls above entry absorb resistance; bid-heavy book supports entry. Volume ratio
> soft but acceptable. Execute.

**Advisor reason, VERBATIM — vpos 84:**

> 1H/15m/5m bullish confluence + 1H ADX 30.7 (strong trend) + 15m/5m expanding EMA. No opposing ask
> wall blocks long. 1D/4H neutral but lower-TF alignment (2/4) sufficient for DCA grid entry with
> hedge risk management.

## 2.2 WAS IT ACTUALLY RANGING? — the tape, independent of the bot

Measured on real OKX 1H candles. `|net|/range` near 1.0 = a clean directional leg; near 0 = chop.

| | prior 12h | prior 24h | ATR(14) 1h vs 14-day median |
|---|---|---|---|
| **vpos 83** (28th 01:00) | range 2,388.9 (3.78%), net **-3.06%**, **\|net\|/range 0.84** | range 2,729.0 (4.32%), net -3.05%, 0.73 | 371.6 vs 308.5 = **1.20x** |
| **vpos 84** (28th 17:00) | range 1,377.8 (2.16%), net **+0.39%**, **\|net\|/range 0.18** | range 2,355.9 (3.70%), net -2.05%, 0.56 | 387.6 vs 307.0 = **1.26x** |

**Verdict — the operator's read is right for one of the two, and right about the environment both
died/live in.**

- **The SHORT did NOT enter a ranging tape.** The prior 12h was a genuine 3% down-leg,
  `|net|/range` 0.84, ADX(1h) 26.3, 4/4 MTF. The problem is **where in the leg**: the prior-12h low
  was 63,011 and the entry filled at 63,449.7 — **within 0.7% of the leg's low**. It sold the
  exhaustion end of a completed move. What followed was chop: over the position's 30h life
  `|net|/Σ|bar move|` = **0.19** — near-pure noise, and the noise drifted up into the stop.
- **The LONG did enter a range, near its top.** Prior 12h `|net|/range` **0.18**, and the entry at
  63,997.3 sat against a 12h high of 64,077.9. Its own OHLCV plane said `trend_4h = neutral`,
  `trend_1h = neutral`, MTF **2/4**. It is currently **+0.76R** — the range has since resolved
  upward, so this is a bad-looking entry with a good-looking outcome so far, not a vindication.

### 🔴 The finding that outranks everything else here

**`market_regime` is not a measure of the market.** `signal_matrix.compute_score` (L391):

```python
'market_regime': 'TREND' if trend_net_dir != NEUTRAL else 'FLAT',
```

`trend_net_dir` is the net direction of the **TREND matrix category — the 1H LuxAlgo signals**.
No ADX, no ATR, no EMA-gap, no price path enters it. `TREND` means *"a 1H signal is live right
now"*. `FLAT` means *"none is"*.

Empirically, over the last 14 days across 387 gate-reaching rows:

| label | n | ADX(1h) mean | ADX(1h) median | ADX(4h) mean | mean \|EMA-gap 1h\| | `trend_1h = neutral` |
|---|---|---|---|---|---|---|
| **FLAT** | 91 | **26.66** | 26.65 | 24.64 | 0.226% | 37.4% |
| **TREND** | 296 | **25.52** | 26.06 | 23.44 | 0.234% | 40.2% |

The trend-strength measures are **identical, and FLAT is marginally the stronger of the two**.
**119 of the 296 `TREND`-labelled rows had `trend_1h = neutral`** on the bot's own OHLCV plane —
vpos 84 is one of them. This is exactly the case the operator flagged: a TREND label on a ranging
tape. It is not an occasional misfire; the label was never measuring the tape.

This matters because **that label picks the score threshold** (§2.3), and because
`AI_ADVISOR_HIDE_1H = True` means the advisor cannot see the 1H LuxAlgo direction that produced the
label — it is shown `Market regime: TREND` as a market fact.

*Not proposed as a change.* Redefining `market_regime` moves the FLAT floor under 438 signals'
worth of gating in the last four weeks alone; it needs its own study and its own decision.

## 2.3 HOW DID THEY CLEAR THE GATE? — the arithmetic

Gate chain: `direction_score` (matrix category contributions) → `+ macro/news gate adj` →
`_gated_score` vs `_eff_thr` → separately `+ weight_engine adj` → `adj_score`, which is what is
stored in `trades.confluence_score`.

**vpos 83 SHORT — `matrix_breakdown_json`:**

| category | long pts | short pts | net | contribution | note |
|---|---|---|---|---|---|
| TREND | 0.0 | 2.5 | SHORT | **2.50** | Trend Catcher Down |
| MOMENTUM | 0.0 | 0.0 | NEUTRAL | 0.00 | |
| LIQUIDITY | **2.5** | 0.0 | **LONG** | **0.00** | `inter_conflict: true` — minority side, zeroed |
| EXECUTION | 0.0 | 1.75 | SHORT | **1.75** | Within Bearish OB |

- base `direction_score` = 2.50 + 1.75 = **4.25**
- news / macro adj = **0.00** (`macro_news_category = NEUTRAL`, conf 0.85; `news_score` 0.25, impact low — informational only, it does not enter the gate)
- `_gated_score` = **4.25**
- weight-engine adj = 0.00 (`weight_used` 1.00) → stored `confluence_score` **4.25**
- threshold faced: `market_regime = TREND` → `CONFLUENCE_SCORE_THRESHOLD` = **2.0** → **PASS**
- 🔴 **under the FLAT floor of 5.0 this trade is REJECTED.** The regime label was outcome-determining.
- Note the LIQUIDITY category was **LONG** — a full 2.5 points pointing the other way, zeroed as the
  minority and therefore invisible in the final number.

**vpos 84 LONG:**

| category | long pts | short pts | net | contribution |
|---|---|---|---|---|
| TREND | 2.5 | 0.0 | LONG | **2.50** |
| MOMENTUM | 0.0 | 0.0 | NEUTRAL | 0.00 |
| LIQUIDITY | 2.5 | 0.0 | LONG | **2.50** |
| EXECUTION | 2.5 | 0.0 | LONG | **2.50** |

- base `direction_score` = **7.50** (no conflicts, all three categories aligned)
- news / macro adj = **+1.00** — `STRONG_POSITIVE`, confidence 0.92, headline *"BlackRock, Fidelity, other Wall Street giants back the Clarity Act"* (`macro_gate_penalty` stores the adj, sign positive = boost)
- `_gated_score` = **8.50**
- weight-engine adj = 0.00 → stored `confluence_score` **7.50**
- threshold faced: **2.0** → **PASS**, and it would also have cleared the FLAT 5.0 floor. The regime label was **not** decisive here.

**Was the FLAT floor applied at all? YES — heavily, just not to these two.** Reconstructing the
regime from `matrix_breakdown_json` for every `below_threshold` row since 2026-07-01 (the column
itself is not written on that path — worth fixing, it makes this question needlessly hard):

- 577 `below_threshold` rows: **552 FLAT / 25 TREND**
- **438** of them scored in `[2.0, 5.0)` with a FLAT regime — i.e. **killed by the FLAT floor
  alone**, most recently 2026-07-29 02:40. The floor is live and load-bearing.

## 2.4 THE BOOK AT THOSE MOMENTS

Verbatim blocks and the computed percentiles are in **Part 1** above. Restated as a judgement:

| | bid wall | ask wall | imbalance | depth |
|---|---|---|---|---|
| **vpos 83 SHORT** | x5.9 = **61th** | x9.6 = **80th** | 0.56 bid-heavy = **92th** | **61th** |
| **vpos 84 LONG** | x4.3 = **18th** | none = **0th** | 0.45 ask-heavy = **20th** | **20th** |

**Was the book genuinely weak?** For the LONG, **yes and uniformly** — every figure sits between the
0th and 20th percentile. That is a thin, empty book, and the old prompt could not say so: it showed
one "Massive" wall and the word `none`. For the SHORT the book was **not** weak — it was moderately
full, with the notable figure being the **imbalance at the 92nd percentile bid-heavy**, i.e. the
most bid-leaning book in roughly nine of ten samples, **against** a SHORT.

**Would the Part 1 fix plausibly have changed either verdict?** Honest answer, and it is a
plausibility read, not a counterfactual test:

- **vpos 84 LONG — almost certainly not.** The advisor's reason ("No opposing ask wall blocks long")
  is *true* and stays true; the percentiles only confirm the book is empty in both directions.
- **vpos 83 SHORT — possibly, but not mechanically.** The bid wall sitting directly below the
  entry (63,402.5, 47 dollars away) is the HARD RULE's opposing wall for a SHORT, and at the **61st
  percentile it is ordinary** — so the new rule would *not* force a skip on it either. What changes
  is the sentence the advisor actually wrote: it called a **80th-pct** ask wall "Massive … absorbs
  resistance" and described a **92nd-pct bid-heavy** book as "supports entry". Under the new block
  both of those read very differently. That is a reason to expect a better-reasoned verdict; it is
  **not** evidence the verdict would have flipped.

> ⚠️ Discipline note: OPEN-ITEMS §4.4 kills the "wall-side misread" hypothesis on two bots by two
> methods. Nothing here re-opens it. The above quotes one trade's reasoning as a **fact about the
> prompt**, and draws no conclusion about a systematic wall-side edge. n=1.

## 2.5 THE SHORT'S DEATH — original stop, and which guard actually held

**Original stop. Never moved.** `sl_price` = `original_sl_price` = **64,286.4**, `recheck_status` =
`done`. All three `recheck_events` rows verdict **OK**, `health_score` 0, **`sl_after` NULL** on all
three — no tighten was ever proposed.

| tier | ts | price | health | verdict | wall ratio | note |
|---|---|---|---|---|---|---|
| 10s | 01:00:44 | 63,460.4 | 0 | OK | 0.77 | |
| **60s** | 01:01:26 | 63,425.1 | 0 | OK | **2.30** | `wall_growth_critical` fired, **points: 0** |
| 300s | 01:05:33 | 63,371.1 | 0 | OK | 0.68 | |

🔴 **Which guard held is not the one asked about.** At the 60s tier the wall ratio hit **2.30** and
`wall_growth_critical` **fired** — under the pre-`c845941` scoring that is **-5 points → TIGHTEN**,
and the stop would have been halved toward the midpoint. It contributed **0 points** because
**`c845941`** zeroed the phantom-wall trigger. So:

- **`c845941` is what prevented the tighten.**
- **`93c20c3` (new SL can never be tighter than the ORIGINAL stop) was never exercised** — there was
  no tighten for it to bound. It held **vacuously**. Verified, not inferred: `sl_after` NULL on all
  three rows and `sl_price == original_sl_price` at close. I am not reporting this as a test of
  `93c20c3`, because it wasn't one.

**The real candle path** (353 5m candles, entry → close):

- best excursion **62,700.1 = +0.896R in favour** — it never reached +1R
- worst **64,370.0 = -1.10R**; first candle touching the original stop **2026-07-29 06:25**, closed 06:28 @ 64,311.4
- the trail arms at +1R and therefore **never armed**; `close_reason` = `sl`, and `adaptive_trail_events` is empty for this position — consistent
- 30h alive, `|net|/Σ|bar|` **0.19** over that window: it died in chop, not in a reversal

**The exit advisor called it, and DRYRUN meant nothing happened.** 34 consults on this position,
**27 close / 7 hold**. First `close` at **2026-07-28 04:00:51** (row 19056), 5m close 63,299.9 =
**+0.179R**:

| | gross | net |
|---|---|---|
| **Advisor's first close verdict** | **+23.61** | ≈ +15.7 (taker fees ~7.9) |
| **What actually happened** | **-135.80** | **-143.67** |
| **Difference** | **+159.41** | **≈ +159** |

**§2.4 activation criterion — progress is now 2 of ~10 closed, and the bar does not move.**
vpos 82: no `close` verdict was ever issued (actual +53.79 kept, advisor neither helped nor hurt).
vpos 83: first `close` verdict beats the actual exit by ~159 USDT. Running: **positions improved
1, worsened 0, neutral 1.** Eight more closes are needed. `EXIT_ADVISOR_DRYRUN` stays `True`.

## 2.6 THE OPEN LONG — vpos 84

- **Unrealised +0.760R** (last 5m close 64,656.7 vs entry 63,997.3; 1R = 867.4)
- **MFE +0.792R** (high 64,684.0), MAE -0.621R (low 63,458.9). `water_mark` 64,664.1 = +0.769R
- **The partial has NOT fired.** `partial_taken` NULL. `LONG_PARTIAL_LEVEL_R = 1.0` needs
  **64,864.7**; the position has never traded there — it topped **200 dollars short of the trigger**.
  §2.1's clean-long counter therefore stays at **7**.
- Stop still the original **63,129.9**; trail arms at +1R, so it has not armed either.

**Full exit-advisor verdict history — 18 consults, 10 hold / 8 close, all hourly except one:**

| # | ts (UTC) | verdict | trigger |
|---|---|---|---|
| 1 | 07-28 17:00:32 | hold | hourly |
| 2 | 07-28 18:00:41 | **close** | hourly |
| 3 | 07-28 19:00:44 | **close** | hourly |
| 4 | 07-28 20:00:43 | hold | hourly |
| 5 | 07-28 21:00:49 | hold | hourly |
| 6 | 07-28 22:00:50 | hold | hourly |
| 7 | 07-28 23:00:51 | **close** | hourly |
| 8 | 07-29 00:00:53 | hold | hourly |
| 9 | 07-29 01:00:59 | **close** | hourly |
| 10 | 07-29 02:01:06 | **close** | hourly |
| 11 | 07-29 03:01:10 | hold | hourly |
| 12 | 07-29 04:01:19 | **close** | hourly |
| 13 | 07-29 05:01:28 | hold | hourly |
| 14 | 07-29 06:01:28 | **close** | hourly |
| 15 | 07-29 06:30:10 | **close** | Bullish I-BOS |
| 16 | 07-29 07:01:35 | hold | hourly |
| 17 | 07-29 08:01:38 | hold | hourly |
| 18 | 07-29 09:01:42 | hold | hourly |

Its **first** `close` (#2, 07-28 18:00) came at roughly -0.33R — that one would have **cost** money
against the current +0.76R. This position is the counterweight to vpos 83 and it is the reason the
criterion is measured over ~10 closes and not over anecdotes. It counts only when it closes.

Selected verbatim, most recent (#18, 09:01:42, `hold`, conf 0.62):

> Entry thesis partially intact but deteriorating. ADX1h collapsed 30.7→11.4 (trend strength
> evaporated); 5m/15m now neutral. Order book imbalance flipped dramatically (0.62→0.39, 1st
> percentile—extreme reversal). Supporting wall thinned 8.5x→7.6x. However: +0.45R unrealised gain,
> current stop 1.45R away provides cushion, position still within bullish OB structure, vol_15m
> healthy at 1.79. Risk: reg[truncated]

And the one that names the baseline problem itself (#7 on vpos 83, 07-28 04:00:51):

> … Supporting wall percentile=100th is artificial given baseline contains persiste[truncated]

## 2.7 ENTRIES SINCE 2026-07-27 00:00, BY REGIME

**Executed entries in the window: exactly two — the two above. Both `TREND`.** n=2 supports no
distributional claim, so here is the population that actually reaches the gate:

| day | TREND | FLAT | TREND share | n |
|---|---|---|---|---|
| 07-22 | 24 | 20 | 54.5% | 44 |
| 07-23 | 41 | 0 | 100.0% | 41 |
| 07-24 | 14 | 3 | 82.4% | 17 |
| 07-25 | 9 | 1 | 90.0% | 10 |
| 07-26 | 56 | 8 | 87.5% | 64 |
| **07-27** | **14** | **5** | **73.7%** | 19 |
| **07-28** | **27** | **3** | **90.0%** | 30 |
| **07-29** (to 10:00) | **0** | **2** | 0.0% | 2 |

**Nothing has shifted.** The TREND share has swung between 5.6% (07-18) and 100% (07-23) all month;
73.7% and 90.0% on the two days in question are unremarkable inside that spread. Today's 0/2 is two
signals before lunch, not a regime change.

The stable fact underneath is the one from §2.2: **TREND dominates because it only reports whether a
1H signal is live**, and one usually is. Across the last 22 executed entries (since 2026-06-29),
**19 were `TREND` and 4 were `FLAT`** — and all four FLAT executions are from 06-30 … 07-05, i.e.
before the FLAT floor was enforced on 2026-07-06. **Since the floor went in, no FLAT-labelled signal
has ever been executed.** That is the floor working as designed, and it is also why "regime
distribution among entries" cannot detect anything: the answer is structurally always TREND.

## 2.8 NEW — not asked for, found on the way: both entries have NO 15m signal name

Both trades' `combo_key` reads `15M:None`, `hw_15m_signal_name` is NULL, and the advisor prompt
printed:

```
15m: n/a (direction: n/a)
```

…immediately above the closing line *"The 3 timeframes are aligned (confluence has already passed)"*.
`state_machine.confluence_check` **does** require a non-NEUTRAL 15m direction, so the slot genuinely
held a confirmation — but neither its **name** nor its **direction** reached the advisor. Real 15m
confirmations exist in the DB around both entries (`Reversal Up` 07-27 23:30; `Bullish Divergence`
and `HyperWave Signal Up` 07-28 14:30), so the alerts are arriving and `ef7fa10`'s write is working.

This is **5 of the last 12 executed entries** (19214, 19021, 17895, 15510 and 18108's mismatch), so
it is not new to these two and not a regression from anything shipped this week. Recording it as a
new open item rather than diagnosing it here — it needs its own session. It also degrades
`_entry_signals_for()`, which recovers the 15m name **from the entry prompt** and therefore returns
`n/a` for these positions, so the exit advisor is told "15m confirmed by: n/a" too.

---

## STATE AT CLOSE

`git status` clean · HEAD **`8b15ecc`** (was `f0a8d30`) · `titan.service` **active**, restarted
09:56:06 UTC, worker 4017679 running post-fix code · `orderbook_density` collector alive (+60
rows/h, 0 failures) · **Mercury-SOL untouched**

Flags unchanged: `LIVE_TRADING_ENABLED=False` · `EXIT_ADVISOR_DRYRUN=True` ·
`CONFLUENCE_FLAT_THRESHOLD=5.0` · `AI_ADVISOR_HIDE_1H=True` · `LONG_PARTIAL_ENABLED=True` (1.0R, 1/3)

**Book: 1 open position** — vpos 84 LONG @ 63,997.3, **+0.76R**, stop 63,129.9 (original), partial
not fired.

### Carry forward

1. **`market_regime` does not measure the market** (§2.2). It gates the 2.0/5.0 threshold and it was
   outcome-determining for vpos 83. Needs its own study before anything is changed — 438 signals in
   four weeks hang off the current definition.
2. **Exit advisor: 2 of ~10 closed** (§2.5). vpos 83 says +159; vpos 84's first close verdict is
   currently losing. The bar does not move.
3. **`depth_pct` on the EXIT prompt has always rendered `n/a`** (Part 1). Two lines.
4. **`market_regime` is not written on `below_threshold` rows** (§2.3) — the gating question has to
   be answered by reconstructing it from `matrix_breakdown_json`.
5. **15m signal name missing from the advisor prompt** (§2.8), 5 of the last 12 entries.
