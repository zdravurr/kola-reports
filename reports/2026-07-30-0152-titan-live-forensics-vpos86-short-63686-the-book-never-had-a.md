# TITAN LIVE FORENSICS vpos86 SHORT 63686 — the book never had a vote

_2026-07-30 01:52 UTC_

---

**VERDICT FIRST.** The premise of the question is wrong, and the way it is wrong is the finding.
**The order book never had a vote to lose.** The category the card calls `LIQUIDITY` contains no
order-book data at all — it holds ten TradingView 5m price-action signals. What was zeroed was a
**"Bullish Liquidity Grab" candlestick signal from 15 minutes earlier**, not the book.

The real book was seen by exactly one component (the entry advisor), which read it as **mildly
bid-heavy, 69th percentile** — a weak dissent, not the extreme the card implies — and executed
anyway at 0.82 confidence. Meanwhile **three separate defects** were found, two of them live and
one of them feeding a fabricated "0th percentile" alarm into the exit advisor right now.

Position is **open, LIVE, real money**, currently **−0.51R**, stop intact, trail not armed.
**No changes were made. Read-only throughout.**

---

## THE POSITION (live, as of 2026-07-30 01:48 UTC)

| | |
|---|---|
| vpos | 86 · entry row `trades.id=19589` · order `VIRT-86` |
| Side / size | SHORT 0.0023 BTC @ **63686.0** · $147.28 notional · 5x cross · margin $29.30 |
| Opened | 2026-07-30 00:50:14 UTC (held 58 min) |
| Mark | 64242.5 · uPnL **−$1.28** |
| 1R | 1081.1 pts (entry → original stop 64767.1) |
| Unrealised | **−0.515 R** |
| Distance to stop | 524.6 pts = **0.485 R** (0.82% of price) |
| MFE / MAE | +0.099R / **−0.515R** (water_mark 63578.5) |
| Trail | **NOT ARMED.** Arms at +1R = price 62604.9. trail_pct 1.698% |
| Breakeven | not applied |

**Orders on the exchange — exactly one:**

```
orderId   2082629881359347712   STOP_MARKET  BUY  0.0023  BTC-USDT
positionSide SHORT   stopPrice 64767.1   workingType MARK_PRICE
reduceOnly true   closePosition true   status NEW
```

Matches `virtual_positions.stop_order_id`. No TP, no trail order, no orphans. Exchange position
`positionId 2082629807737368578`, avgPrice 63686.0, positionAmt 0.0023, SHORT — reconciles with DB.

---

## 1. THE BOOK'S VOTE WAS DELETED — was that right?

### 1a) The code, and what it actually zeroes

`signal_matrix.py:342-362`:

```python
    # Inter-category resolution.
    long_cats  = sum(1 for b in breakdown.values() if b['net_direction'] == LONG)
    short_cats = sum(1 for b in breakdown.values() if b['net_direction'] == SHORT)
    ...
    for cat, b in breakdown.items():
        nd = b['net_direction']
        if nd == NEUTRAL:            continue
        if majority != NEUTRAL and nd != majority:
            b['inter_conflict'] = True          # <-- minority category
            b['contribution']  = 0.0            # <-- its entire 2.5pt budget deleted
            continue
```

Stated reason, verbatim from the same file (`:311-315` and the module docstring `:16-17`):

> `2) Inter-category: count categories by net direction. The MINORITY direction zeroes out — e.g.,
> "3-LONG-1-SHORT" loses the SHORT category's 2.5pt budget.`
> `Direction conflict between TREND and MOMENTUM zeros the conflicting categories' contributions`
> `(clean 0-10 semantics).`

**The stated justification is scoring hygiene — "clean 0-10 semantics." Not evidence. No study, no
win-rate, no PnL is cited anywhere for the rule.** It has been in the file since it was created;
the 2026-05-16 isolation refactor (`b9a2935`) squashed the pre-history, so no earlier commit
message survives.

### 🔴 1a-CRITICAL — what `LIQUIDITY` contains

`signal_matrix.py:125-135`, the complete membership of `CAT_LIQUIDITY`:

```python
    # ===== 5m LIQUIDITY context (task=price_action, 10 signals) =====
    'Bullish Liquidity Grab':       (CAT_LIQUIDITY, LONG,  'liq_grab_bull', 1.0),
    'Bearish Liquidity Grab':       (CAT_LIQUIDITY, SHORT, 'liq_grab_bear', 1.0),
    'Equal L.' / 'Equal H.'  ·  'Broken Up/Downtrendline'
    'Bullish/Bearish New Imbalance'  ·  'Bullish/Bearish Imbalance Mitigated'
```

Ten LuxAlgo candlestick signals off the 5m chart. **Zero order-book inputs.** The order book is
never scored, never weighted, and never enters `confluence_score` on any path.

The actual signal that was zeroed on this trade (`trade_signal_matrix.active_signals_json`):

```json
{"canonical_id": "liq_grab_bull", "category": "LIQUIDITY", "direction": "LONG",
 "signal_name": "Bullish Liquidity Grab", "intensity_weight": 1.0, "age_minutes": 14.99}
```

So the card line **`LIQUIDITY: 🚫 minority-LONG zeroed (would've been 2.5)`** means: *a Bullish
Liquidity Grab printed 15 minutes ago and was outvoted 3-to-1.* It does **not** mean the order book
lost an argument. This is a fourth instance of the "the label lies" class — the word **LIQUIDITY**
reads to the operator as *order book*, and it is not.

Score arithmetic, confirmed: TREND 2.25 + MOMENTUM 1.75 + EXECUTION 1.75 = **5.75**, threshold 4.0
(TREND regime). Had the Liquidity Grab counted, LONG would have had 2.50 vs SHORT 5.75 — the trade
fires either way. **Zeroing it changed nothing about whether this trade happened.**

### 1b) How often it fires, and on which category

**Full signal population** (13,811 rows carrying `matrix_breakdown_json`, includes skips):

| Category | times directional | times zeroed as minority | rate |
|---|---:|---:|---:|
| TREND | 5,699 | 916 | 16.1% |
| MOMENTUM | 7,282 | 1,035 | 14.2% |
| **LIQUIDITY** | 6,119 | **703** | **11.5%** |
| EXECUTION | 10,056 | 886 | 8.8% |

3,540 / 13,811 = **25.6%** of all scoring events contain at least one zeroed category. LIQUIDITY is
the *least*-zeroed of the four.

**Now the same question restricted to trades that actually EXECUTED** (`trade_signal_matrix`, 73 rows):

| Category | rows zeroed |
|---|---:|
| **LIQUIDITY** | **22** |
| TREND | 0 |
| MOMENTUM | 0 |
| EXECUTION | 0 |

**22 of 73 executed trades (30.1%) had a category zeroed, and it was LIQUIDITY every single time.**
Mean points deleted: 2.16.

This is not coincidence, it is structural. Zero TREND/MOMENTUM/EXECUTION and the survivors sum to
≈4.0 or less and usually miss the threshold. Zero LIQUIDITY and the other three still sum to ~5.75,
which clears 4.0 comfortably. **LIQUIDITY is the only category whose silencing still permits a
trade to fire.** So the rule is written as a symmetric tie-breaker and behaves in production as a
one-way LIQUIDITY silencer — a selection effect nobody designed.

### 1c) Outcomes on clean closed trades

Clean = `virtual_positions.status='closed'` (excludes 6 `archived_pre_geometry_fix`). n=53, joined
to their entry rows.

Note first: **when LIQUIDITY is zeroed as minority it disagrees with the trade direction by
construction** — minority ≠ majority, and the trade takes the majority. The conjunction in the
question is not a filter; the two conditions are the same condition. All 15 qualify.

| cohort | n | wins | net $ | sum R | mean R | **median R** |
|---|---:|---:|---:|---:|---:|---:|
| **LIQUIDITY zeroed** | **15** | 6 (40%) | **+507.17** | +2.23 | +0.159 | **−0.278** |
| no category zeroed | 38 | 18 (47%) | +21.57 | −3.65 | −0.096 | −0.116 |

R-multiples of the 15, in order:
`na +0.17 −0.55 +2.00 +1.97 −0.58 +2.39 −1.06 −0.28 −0.28 −0.31 −0.11 −1.09 +1.04 −1.09`

**Read it honestly, both ways:**

- **By hit rate the silenced signal was vindicated: 9 of 15 (60%) of these trades LOST.** The
  minority vote pointed at the winning direction more often than not.
- **By money it was not.** Three trail winners (+2.39R, +2.00R, +1.97R = vpos 58/48/49) carry the
  entire cohort. Strip them and the rest is −2.1R across 11 trades. The median is **−0.278R**, worse
  than the no-zero cohort's −0.116R.
- Excluding `external` (operator/manual) closes: LIQz n=14, 43% win, +$521.69, median R −0.279;
  no-zero n=29, 38% win, **−$114.79**, median R −0.382.
- 14 of the 15 are from the $2000-margin era, so the dollar figures are comparable within the
  cohort but not across eras. R-multiples are the fair comparison and they are the ones that look
  worst.

**Conclusion on 1c: NO CONCLUSION IS AVAILABLE AT n=15.** A 60% "book was right" hit rate against a
positive-outlier PnL tail is exactly the shape that flips on the next three trades. What *is* solid
at this n is the structural finding in 1b — the rule only ever fires against LIQUIDITY on trades
that execute — and that deserves a proper study, not a patch.

---

## 2. THE IMBALANCE LABEL — is it lying like "Massive" was?

### 🔴 The bigger problem first: THREE different books, three different numbers, one word

At the same instant, `2026-07-30 00:50:1x`, the machine recorded three different "Imbalance" values
for BTC and showed them in three different places without ever saying they were different books:

| shown as | value | source | levels | volume unit |
|---|---:|---|---|---|
| Advisor prompt: `Imbalance ±1%: 0.51 (bid-heavy) — 71th pct` | **0.51** | OKX `books-full` via `liquidity_zones.fetch_pre_trade_walls` | 4000/side | USDT |
| Operator card: `• Imbalance: 0.31 (Balanced)` | **0.31** | BingX via `microstructure.fetch_snapshot` | **top 20** | contracts |
| DB `virtual_positions.entry_ob_imbalance` | **0.2914** | BingX via `microstructure.fetch_pre_trade_walls` | **100** | contracts |

Same label. Same minute. Three books. Nothing on the card names its source.

### 2a) Where "Balanced" comes from — hardcoded, `microstructure.py:356-365`

```python
def _imbalance_label(imbalance) -> str:
    """Ask-Heavy / Balanced / Bid-Heavy classification matching the same
    bands the analyzer uses for tape pressure (<.30 / .30-.70 / >.70)."""
    if imbalance is None:  return 'N/A'
    if imbalance < 0.30:   return 'Ask-Heavy'
    if imbalance > 0.70:   return 'Bid-Heavy'
    return 'Balanced'
```

Hardcoded three-band, no percentile, no baseline, no source attribution. **Same defect class as the
4.0x "Massive" wall label fixed in `8b15ecc`** — a constant threshold read as a judgement.

The advisor's own label is *also* hardcoded (`claude_advisor.py:166`,
`'bid-heavy' if imb > 0.5 else 'ask-heavy'`) — **but the advisor prints the percentile immediately
next to it**, so the calibration is present where it matters. The operator card carries the band and
nothing else. **The asymmetry closed for walls in `8b15ecc` was never closed for imbalance, and
never closed for the card at all.**

### 2b) Recomputed percentiles against the CURRENT baseline

`orderbook_density`, **n=24,001**, 2026-07-13 → 2026-07-30 01:47, source `okx_books_full_4000`,
recomputed just now (not the July figures):

```
p0 = 0.3101   p1 = 0.3959   p5 = 0.4187   p25 = 0.4575
p50 = 0.4856  p75 = 0.5209  p95 = 0.5691  p99 = 0.6123  p100 = 0.6632
mean 0.4898   sd 0.0463
```

| figure | percentile on this baseline |
|---|---:|
| advisor's 0.51 (OKX — *same measurement as the baseline*) | **68.5th** ✅ valid |
| card's 0.31 (BingX top-20) | 0.0th ❌ **invalid comparison** |
| DB's 0.2914 (BingX depth-100) | 0.0th ❌ **invalid comparison** |

**Two corrections to the brief, both material:**

1. **Direction.** `imbalance = bid_volume / (bid + ask)`. A value *below* the median means the
   **bid** side is thin — that is **ask-heavy**, not bid-heavy. A genuinely low imbalance would have
   been an argument **for** the short, not against it.
2. **0.31 is not "below p5 of the baseline" in any meaningful sense** — it is a number from a
   different instrument. BingX depth-100 imbalance across the 22 positions that recorded it:
   mean 0.542, **sd 0.238**, range 0.073→0.892. The OKX depth-4000 baseline has sd 0.046 — **five
   times tighter**. Landing a wide-distribution number on a narrow-distribution scale pins it at 0
   or 100 almost every time. On its own distribution 0.2914 sits around the 20th percentile:
   somewhat ask-lean, unremarkable.

**So the card's "0.31 (Balanced)" is not a false alarm — it is a meaningless one.** It is a
hardcoded band, on an unnamed book, that no gate reads.

### 🔴 2b-CRITICAL — the same cross-source mistake IS live, and it fired on this position

`main.py:2429-2450`, `_build_exit_context()`, the prompt the **exit advisor** reads:

```python
walls = microstructure.fetch_pre_trade_walls(exchange, symbol)     # <-- BingX depth-100
...
ctx['sup_pct'], n = _exit_pct(sc, sup)                              # <-- OKX depth-4000 baseline
ctx['opp_pct'], _ = _exit_pct(oc, opp)
if ctx['imb_now'] is not None:
    ctx['imb_pct'], _ = _exit_pct('imbalance', ctx['imb_now'])      # <-- OKX depth-4000 baseline
```

`_exit_pct` ranks against `orderbook_density`, which is OKX depth-4000. The values handed to it are
BingX depth-100. **Verbatim from the prompt actually sent for THIS position at 00:50:20:**

```
Order book NOW vs AT ENTRY
  Supporting wall: entry x5.7 -> now x5.2 (THINNED)
  Opposing wall:   now x10.4
  Imbalance:       entry 0.29 -> now 0.29 (same side)

Order-book PERCENTILE scale (baseline: 23947 snapshots)
  Supporting wall = 35th pct   Opposing wall = 93th pct
  Total depth = 2440 BTC = 6th pct (sampled 42s ago)   Imbalance = 0th pct
```

**`Imbalance = 0th pct` is fabricated.** The OKX book at that same second measured **0.5141** —
69th percentile, mildly bid-heavy. The prompt told the model the book was the most ask-heavy state
ever seen in 23,947 snapshots. The exact opposite end of the scale.

**`Opposing wall = 93th pct` is fabricated the same way.** BingX said x10.4; the OKX book at that
second had a max bid wall of **x4.8 = 25.7th pct**. And the advisor *used* it — its verbatim reason:

> `Supporting wall thinned but opposing wall strong (93rd pct). Stop 0.99R away provides safety.`

A phantom 93rd-percentile bid wall became part of the argument to hold a short.

`Total depth = 2440 BTC = 6th pct` **is** correct — it is read straight from the latest
`orderbook_density` row, so it is OKX-vs-OKX. It is also the only genuinely extreme book reading of
the entry, and **neither advisor weighted it**: the book was among the thinnest 6% ever recorded.

The **entry** path does not have this bug. `_entry_book_pct()` (`main.py:2248`) feeds the OKX walls
dict to the OKX baseline, and its docstring documents the apples-to-apples check explicitly. The
defect is exit-side only, and it is running right now.

### 2c) What the advisor was actually told — verbatim

Order-book section of `trades.ai_user_prompt` for `id=19589`, exactly as stored:

```
Order book (pre-trade, 8000 levels):
  Mid: $63,715.05  |  Imbalance ±1%: 0.51 (bid-heavy)  — 71th pct
  Bid walls (>4x avg bucket vol): $63,587.50 (×4.8), $63,577.50 (×4.0), $63,447.50 (×4.4), $63,337.50 (×4.5)  — largest ×4.8 = 32th pct
  Ask walls (>4x avg bucket vol): $63,787.50 (×4.6), $63,877.50 (×4.1), $64,017.50 (×4.2), $64,122.50 (×5.7)  — largest ×5.7 = 46th pct
  Book depth: 2,440 BTC — 6th pct, sampled 35s ago
Order-book PERCENTILE scale (baseline: 23947 snapshots of this same OKX depth-4000 book)
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile: ~50th percentile is ORDINARY.
```

Every percentile here is **valid** (OKX vs OKX; my recompute puts 0.51 at 68.5th vs the 71st printed
— the baseline grew by ~54 rows since). So yes: **the advisor got the percentile, the card got a
hardcoded band, and they were reading two different books.**

What the advisor was told about the book, plainly stated:
- Imbalance **69th pct** — mildly bid-heavy. Not extreme. A weak dissent.
- Bid walls (the side that would stop a short) **32nd pct** — below ordinary.
- Ask walls **46th pct** — ordinary. The advisor's reason says exactly this: *"Ask walls at 46th pct
  (ordinary)... No blocking wall."*
- Depth **6th pct** — the one extreme figure, ignored by both.

The advisor's `"Book bid-heavy"` is technically true off the hardcoded `>0.5` and materially
overstated: 0.51 is one hundredth above the cutoff and sits at the 69th percentile.

---

## 3. ADX 25.87 AT ENTRY vs 11.3 TEN SECONDS LATER

**They are not two measurements of the same quantity. They are two different timeframes, and one of
them is printed on the card with no timeframe label.**

### 3a) What each one reads

| | card "Trend Strength (ADX): 25.87" | recheck "ADX 11.3<20" |
|---|---|---|
| Function | `indicators.telegram_block(snap)` `:445` | `virtual_trader._recheck_fetch_1h_metrics` → `_health_score` `:1361` |
| Timeframe | **5m** (`primary_tf` defaults to `'5m'`, `main.py:3810` passes no override) | **1h** |
| Field | `srv_adx_5m` = **25.8746** | `adx_1h` = **11.2711** |
| Period / lib | ADX(14), `pandas_ta`, `iloc[-1]` | ADX(14), `pandas_ta`, `iloc[-1]` |
| Candle | last row incl. the **forming** 5m bar | last row incl. the **forming** 1h bar |
| Read by | nobody — display only | the recheck health score, floor 20 |

Same library, same period, same forming-candle convention. **Different series.** The 1h value at
entry was `srv_adx_1h = 11.117`; ten seconds later the recheck's independent fetch gave 11.271. A
0.15 drift across ten seconds — entirely consistent, no anomaly. The 25.87 was never a 1h number.

The card line is `f"\n📊 Trend Strength (ADX): {_fmt(adx)}\n"` — **no timeframe in the string.**
The advisor prompt, by contrast, labels everything: `ADX(14): 1h 11.1 | 15m 13.0` and
`5m: BEAR, ADX 25.9`. So the operator card is the only surface that prints an unlabelled ADX, and
it prints the one timeframe no gate uses.

### 3b) Forming candle — yes, ADX has it, deliberately

`indicators.py:210-223`, the July volume fix, verbatim:

> `Volume ratio uses the last CLOSED candle only. ccxt fetch_ohlcv returns the currently-FORMING`
> `candle as the final row... Drop that row so both the SMA and the latest bar are completed`
> `candles.` **`ATR/ADX/EMA above keep iloc[-1] on purpose — they are calibrated on the live`**
> **`forming candle and are out of scope.`**

`git diff` against `indicators.py.bak_volforming_20260704` confirms the fix touched **only**
`vol_ratio`. **ADX is still computed on a partial candle on every timeframe, by explicit decision.**
Caching adds a second staleness layer (`_CACHE_TTL_BY_TF`, `indicators.py:49`) but is not the driver
here.

Measured effect at this entry (00:50 UTC, 50 minutes into the 1h bar, so nearly complete):

| TF | ADX(14) incl. that candle | ADX(14) fully-closed only | delta |
|---|---:|---:|---:|
| 1h | 11.382 | 11.969 | −0.59 |
| 15m | 13.371 | 13.060 | +0.31 |
| 5m | 26.463 | 25.394 | +1.07 |

Real but small. **It is not what produced the 25.87 / 11.3 gap.**

### 3c) Which number is right — computed from real BingX candles

Fetched fresh, sliced to the entry timestamp:

```
1h  : ADX(14) = 11.38  (11.97 on closed candles only)
15m : ADX(14) = 13.37  (13.06)
5m  : ADX(14) = 26.46  (25.39)

bot recorded: srv_adx_1h=11.117 · recheck adx_1h=11.271 · srv_adx_15m=12.988 · srv_adx_5m=25.875
```

**Both numbers are right; neither is stale.** 11.1/11.3 is the 1h ADX and matches 11.38±0.6.
25.87 is the 5m ADX and matches 26.46±1.1. **The 1h number is the one that matters** — it is what
the FLAT gate (`ADX_FLAT_FLOOR`) and the post-entry recheck floor both read, and at **11.1 it was
below the floor of 20 at the moment of entry.**

The FLAT gate did not block it because that gate requires `adx_1h < 20` **AND** `market_regime ==
FLAT`, and the regime was TREND. So the entry was taken into a 1h trend strength of 11.1, and the
recheck flagged it as a −5 defect eleven seconds later. **The machine already knew.**

*(Side observation, same class: the T+1.9s dryrun sample logged `adx_5m = 43.89`, versus 25.87 from
the entry snapshot three seconds earlier. Two 5m ADX readings, 3 seconds apart, differing by 70%.
Different fetch path and cache state. Not investigated further — flagged for the record.)*

---

## 4. VOLUME 4.92x — for the record

`srv_vol_ratio_5m = 4.9223` at entry. **92nd percentile** of all 53 clean closed entries.

Restated on the current clean cohort (n=53), which is larger than the 4/4 that killed the study:

| cohort | n | wins | net $ | median vol_ratio_5m |
|---|---:|---:|---:|---:|
| winners | 24 | — | — | **0.95** |
| losers | 29 | — | — | **1.57** |
| entries at vol_ratio_5m **≥ 2.42** | **15** | **2 (13%)** | **−$708.72** | — |
| entries in the 1.30–1.60 band | 9 | 6 (67%) | **+$241.07** | — |

The ≥2.42 cohort in full — 13 of 15 stopped out:

```
vpos69 10.69 LONG  sl   -50.64     vpos73  3.28 LONG  sl   -43.54
vpos71  9.12 LONG  sl   -30.78     vpos85  3.22 LONG  sl  -137.32
vpos68  5.70 SHORT sl    -4.52     vpos79  3.18 LONG  trail +80.10
vpos78  5.01 LONG  sl  -103.54     vpos80  2.98 SHORT sl  -116.58
vpos72  4.79 LONG  sl   -74.61     vpos66  2.67 SHORT sl   -59.11
vpos67  4.74 LONG  sl   -32.73     vpos41  3.62 LONG  sl  -139.51
vpos46  3.58 SHORT trail +241.37   vpos37  3.31 LONG  sl  -104.59
vpos77  3.51 SHORT sl  -132.75
```

**This entry sits at 4.92 — inside that band, near its top.** The original 1.38–1.54 / 2.42–5.70
split replicates at n=15 vs n=9, not n=4.

**Confounds, stated honestly:** 11 of the 15 high-volume entries are LONGs, so direction and era are
entangled with volume, and the sample spans two sizing regimes. This is not a validated ceiling. It
is a signal that the killed study was killed on a sample size that no longer applies.
**Noted for the record; no action taken.**

---

## 5. HOW THE BOOK IS BEING READ RIGHT NOW, IN FLIGHT

### 5a) Exit advisor — ONE consult, at T+6 seconds. Nothing since.

`EXIT_ADVISOR_HOURLY = True`, `EXIT_ADVISOR_HOURLY_SEC = 3600`, `EXIT_ADVISOR_DRYRUN = True`.
`virtual_positions.pending_dca_limits` → `exit_advisor_last_ts = 1785372617.61` =
**2026-07-30 00:50:17.61 UTC**. Position opened 00:50:14. The first consult fired because
`_st is None`, three seconds after fill. Next due 01:50:17.

**Consult #1 of 1 — `trades.id=19590`, 00:50:20, verdict HOLD, confidence 0.72. Verbatim reason:**

> *Entry thesis intact: 15m+5m SHORT agreement, bearish regime (ADX rising to 14.9), recent bearish
> structure (OB, I-CHOCH). Position only -0.01R (negligible loss), just entered 0h ago. Supporting
> wall thinned but opposing wall strong (93rd pct). Stop 0.99R away provides safety. Volume
> adequate. No regime flip yet—hold for thesis to develop.*

Book percentiles it was given, and what they should have been:

| told | actual (OKX, same second) |
|---|---|
| Imbalance **0th pct** (0.29) | **68.7th pct** (0.5141) — ❌ inverted |
| Opposing wall **93th pct** (x10.4) | **25.7th pct** (x4.8) — ❌ inverted |
| Supporting wall **35th pct** (x5.2) | **41.3th pct** (x5.7) — ≈ |
| Depth **6th pct** (2440 BTC) | 5.7th pct — ✅ correct |

It cited the fabricated 93rd-pct wall in its hold reasoning. It has not been asked again since. It
**cannot** close anything — `EXIT_ADVISOR_DRYRUN=True` returns before every close mechanic.

### 5b) `orderbook_density` — yes, unchanged cadence

57 rows since entry over 58 minutes = one per 60s. Prior 24h: 1,421 rows = same rate. Latest row
01:47:40, `okx_books_full_4000`, depth 2835.7 BTC, imbalance 0.4105. **Identical to paper cadence.**

*(Note: the OKX book has since drifted to 0.41 — genuinely ask-heavy, ~3rd percentile — i.e. the
real book has moved toward supporting the short at the same time price has moved against it.)*

### 5c) What actually CONSUMES book data during the hold — the answer is nothing

| consumer | reads book? | can act? |
|---|---|---|
| `orderbook_collector` (60s) | ✅ OKX | ❌ writes a table |
| `_record_smart_exit_dryrun` (hourly) | ✅ OKX | ❌ *"read by NO exit logic"* — its own docstring |
| Wall-anchor `would_wall_sl` | ✅ | ❌ `WALL_TRAIL_LIVE_ENABLED = False` |
| Exit advisor (hourly) | ✅ (with the corrupted percentiles) | ❌ `EXIT_ADVISOR_DRYRUN = True` |
| Post-entry recheck | ✅ BingX walls | ❌ **`WALL_GROWTH_CRITICAL_SCORE = 0`, `WALL_GROWTH_WARNING_SCORE = 0`** (neutralised 2026-07-13) |
| SL / trail / breakeven | ❌ | ✅ — **the only paths with authority, and they are price-and-ATR only** |

**Nothing in the live path consumes book data during the hold.** The exchange trail was deliberately
not implemented; the wall-trail is off; the recheck's wall rule carries zero points. The book is
collected on three independent sources, rendered into two prompts, logged into two tables — and
**read by nothing that can move a stop.**

Exactly **one** smart-exit dryrun sample exists for this position, at elapsed 1.9s. The next is due
at ~01:50. **In 58 minutes of live risk the book has been sampled for decision purposes once,
6 seconds after entry.**

### 🔴 5c-CRITICAL — a no-op advisory permanently retired the post-entry recheck

The recheck fired at T+10s: health **−5**, verdict **TIGHTEN**, sole reason
`[{"rule": "adx_below_floor", "value": 11.271, "threshold": 20.0, "points": -5}]`.

`sl_before = 64767.1`, `sl_after = 64767.1`, `sl_tightened_pct = 0.0`. **The stop did not move** —
correctly, and by design: `_tighten_sl()` was bounded on 2026-07-26 so it can never end tighter than
the original stop, and since the recheck only runs pre-breakeven, `current_sl` *is* the original
stop. The docstring says it plainly:

> `in practice this makes a TIGHTEN verdict a LOGGED ADVISORY that moves no stop.`

But the TIGHTEN branch still writes `recheck_status = 'tightened'`, and the poller
(`virtual_trader.py:2105`) treats `'tightened'` as **terminal**:

```python
    if (POST_ENTRY_RECHECK_ENABLED and not be_applied
            and row['recheck_status'] not in ('done', 'tightened', 'closed_critical')):
```

**So the T+60s and T+300s tiers will never run on this position — including the EMERGENCY_CLOSE
branch, the only recheck path that still has teeth.** A verdict that moves nothing consumed the
entire remaining post-entry budget.

Evidence across every position that has recheck rows:

```
vpos 74  tightened   tiers: 10           (1 of 3)
vpos 75-85  done     tiers: 10,60,300    (3 of 3, eleven positions)
vpos 86  tightened   tiers: 10           (1 of 3)   <-- THIS POSITION
```

**vpos 86 is the first position to reach `'tightened'` since the 2026-07-26 bounding fix.** The fix
made the action harmless and left the terminal status behind it. This is the same shape as the
class recorded on 29.07: *the failing thing was made safe, and a second consequence of it was not
followed through.*

### 5d) Current state — see the table at the top

Restated: **−0.515R**, stop **0.485R away** at 64767.1, trail **not armed** (needs 62604.9), one
STOP_MARKET order on the exchange, DB and exchange reconcile.

---

## 6. THE HONEST QUESTION

**Was the entry sound on the evidence available?**

On the trend/momentum evidence, **yes, and it was not close.** 4/4 MTF alignment (4h/1h/15m/5m all
BEAR), EMA bearish on all five timeframes, EMA-gap expanding on 4h/1h/5m, three tiers agreeing
SHORT, score 5.75 against a threshold of 4.0. Any reasonable reading of that stack is short.

**Did the machinery override a book that was telling it not to?** **No. Twice over.**

1. **The book was never in the vote.** What got zeroed was a 5m Liquidity Grab candlestick pattern
   worth 2.5 points, and zeroing it changed nothing — SHORT wins 5.75 to 2.50 either way.
2. **The real book was a weak dissenter and was heard.** 69th-percentile imbalance, 32nd-percentile
   bid walls (the side that would stop a short), 46th-percentile ask walls. The advisor read all of
   it, said so — *"Ask walls at 46th pct (ordinary). Book bid-heavy. No blocking wall"* — and
   executed at 0.82. **Nothing was overridden. The book was mildly against and the advisor
   correctly judged it ordinary.**

**Was the book historically worth listening to when it dissents?** **On the only evidence that
exists: n=15, and it does not answer the question.** 60% of those trades lost — the silenced side
pointed the right way more often than not. But the money went the other way (+$507, mean +0.159R)
because three trail winners carried the cohort, and the median trade was −0.278R, *worse* than the
no-dissent cohort. Both statements are true; they point in opposite directions; **n=15 with a
three-outlier tail decides nothing.** Anyone who tells you otherwise is reading a tail.

**What the evidence does say, and this is the part that matters:**

- **The dissenter was never the book — but for 22 of 73 executed trades the operator was shown a
  line that reads as though it was.** The word LIQUIDITY on that card means candlesticks.
- **The one hard warning was raised, was correct, and did nothing.** 1h ADX 11.1 at entry, below the
  floor of 20. The FLAT gate missed it because regime was TREND. The recheck caught it eleven
  seconds later, scored it −5, and produced a stop move of exactly zero — then permanently disabled
  its own two remaining tiers, including the emergency-close path.
- **The one genuinely extreme book reading was depth at the 6th percentile,** shown correctly to
  both advisors, weighted by neither.
- **The one number that most predicted trouble was volume at 4.92x** — 92nd percentile, inside a
  band that is 2-for-15 with −$709 across the clean cohort. No gate reads it.
- **And the exit advisor, the only thing looking at this position, was handed an inverted book.**
  Imbalance 0th pct when it was 69th. Opposing wall 93rd pct when it was 26th. It quoted the phantom
  wall as a reason to hold.

**Plainly: this was a well-founded trend entry that the machinery took for good reasons, on a book
that mildly disagreed and was correctly judged ordinary. The failures here are not in the entry
decision. They are in four labels that do not say what they mean — LIQUIDITY that is not the book,
Imbalance that is three different books, ADX that does not say which timeframe, and a percentile
scale on the exit path that is computing rank against the wrong instrument.**

The 29.07 finding was *"check not only that the gate DECIDES, but what it SAYS."* Three more
instances found today, one of them actively feeding a corrupted number to the only advisor watching
live money right now.

---

## FILE / LINE INDEX

| finding | location |
|---|---|
| Minority zeroing | `signal_matrix.py:342-362` |
| LIQUIDITY = 10 candlestick signals, no book | `signal_matrix.py:125-135` |
| Hardcoded `Balanced` band, no percentile | `microstructure.py:356-365` |
| Hardcoded advisor label (percentile present) | `claude_advisor.py:166` |
| ✅ Entry percentiles, apples-to-apples | `main.py:2248-2316` |
| 🔴 **Exit percentiles, BingX values on OKX scale** | `main.py:2429-2450` |
| Card ADX unlabelled, defaults 5m | `indicators.py:445-460`; call `main.py:3810` |
| ADX on forming candle by design | `indicators.py:210-223` |
| TIGHTEN moves no stop (correct) | `virtual_trader.py:1408-1434` |
| 🔴 **`'tightened'` terminal → tiers 60/300 lost** | `virtual_trader.py:2105-2107` |
| Wall rule scores zero | `config.py:673-674` |
| Wall-trail off | `config.py:455` |

**Nothing was changed. No code, no config, no order, no stop. Read-only throughout.**
