# sol-vpos26-long-forensics

_2026-08-02 16:55 UTC_

---

# MERCURY-SOL — FORENSICS OF vpos 26 (LONG, 2026-08-02 05:00:19 UTC)

**Read-only forensics. Nothing was changed, nothing proposed. Written 2026-08-02 ~17:0x UTC.**
Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol` — **PAPER**. Titan (`/root/titan-bot`,
LIVE) was not touched and not read for parameters.

---

## 0. THE ONE THING

**The advisor refused this trade, and a deterministic override took it anyway.**

The V1 entry advisor returned `skip`, naming the exact object the operator says was missing:

> `v1_reason='Massive ask wall ×20.3 at $73.75 (0.31% above entry) blocks upside momentum. 1d BEAR opposes despite lower-TF bullish confluence. Risk/reward unfavorable.'`

`ADVISOR_WALL_ALIGNED_V2` (LIVE since 2026-07-02) then re-asked the same user prompt under a
system prompt that *instructs* the model that an overhead ask wall is a SOFT caution and
"do NOT reply 'skip' solely because of an overhead ask wall". That second call returned
`execute` (conf 0.78) and **replaced** the verdict. Journal, verbatim:

```
Aug 02 05:00:16 [MERCURY-SOL][WALL-V2-DRYRUN] AGREE skip LONG regime=TREND v2_decide='skip'
Aug 02 05:00:18 [MERCURY-SOL][WALL-ALIGNED-V2][LIVE] FLIP skip→execute LONG adx1h=29.3 v2_conf=0.78 ...
```

Three Claude calls were made on this signal. **Two of the three said skip.** The third, the one
that was told not to weigh the wall, said execute.

**And the wall held.** Price never traded through $73.75. Max high after entry: **$73.63**
(OKX 5m, 141 candles to 16:40 UTC). The position is 11.7h old, −0.36R, and has been within
**$0.08** of its stop.

The operator's read is right about *late* and *into a range* and **wrong about "no liquidity"**
— the liquidity was there, it was thick, the nearest of it was **opposing**, and it is the
reason the first advisor refused.

---

## 1. THE TRADE

### 1.1 Position record

| field | value |
|---|---|
| `virtual_positions.id` | **26** |
| `trades.id` (entry row) | **15093** |
| symbol / side | SOL/USDT:USDT · **LONG** (`side='buy'`) |
| entry time | **2026-08-02T05:00:19.711378+00:00** (signal 05:00:00.826, webhook `Bullish OB Created` tf=5m) |
| entry price | **73.53** |
| size | **135.9** SOL (margin 2000 × lev 5 = $10,000 notional) |
| ATR (5m, entry) | 0.374473291386036 |
| stop | **72.59** = −1.278%; `original_sl_price` identical, never moved |
| SL route | `route=fallback_atr sl=72.59 dist=1.278% wall=None (anchor_flag=OFF)` |
| initial risk | **$127.746** = (73.53 − 72.59) × 135.9 |
| trail_pct | 1.278 |
| entry fee | 5.4960 |
| `is_paper` | 1 — **no order was sent to any exchange** |
| status | **open** |
| water_mark | 73.65 (bot) · max high on OKX 5m 73.63 |
| `max_adverse_price` | **72.67** — 8 cents above the stop |
| partial at +1R | **not armed** (+1R = 74.47; never approached) |
| `mgmt_state_json` | `{"breakeven_applied": false}` |
| current (16:5x UTC) | last 73.19 → **−0.462%, −$46.21, −0.36R** |
| recheck | T+10s / T+60s / T+300s all `verdict=OK score=0`, `recheck_status='done'` |

### 1.2 The three signals

`combo_key = 1H:Smart Trail Switch Bullish|15M:HyperWave Signal Up|5M:Bullish OB Created`

| tier | signal | direction | set at (UTC) | age at consult | weight |
|---|---|---|---|---|---|
| **1H** (TREND) | Smart Trail Switch Bullish | LONG | **03:00:07** | **2.0h** | cat contribution 2.50 (4 signals) |
| **15m** (MOMENTUM) | HyperWave Signal Up | LONG | **04:15:02** | **45m** | `hw_15m_weight` 0.95 → contribution 1.75 |
| **5m** (EXECUTION) | Bullish OB Created | LONG | **05:00:00** | just fired | contribution 1.25 |
| LIQUIDITY | — | NEUTRAL | — | — | 0.00 |

TTLs in force: TREND 360m, MOMENTUM 90m, LIQUIDITY 30m, EXECUTION 5m. All three tiers were
**inside** their TTL. No tier was stale, no tier was tolerated-NEUTRAL.

### 1.3 The score arithmetic

From `matrix_breakdown_json` and the journal line at 05:00:11:

```
[MERCURY-SOL] weighted_adj: dir=LONG raw=5.50 adj=+0.3778 final=5.88
  breakdown={'ema_cross_15m': 0.04, 'ema_cross_1h': 0.04, 'ema_slope_15m': 0.0578,
             'ema_slope_1h': 0.02, 'dxy': 0.3, 'mtf': 0.02, 'funding': -0.1}
```

| quantity | value |
|---|---|
| base (TREND 2.50 + MOMENTUM 1.75 + EXECUTION 1.25 + LIQUIDITY 0.00) | **5.50** |
| weight adjustment | **+0.3778** |
| `trades.confluence_score` as stored | **5.88** |
| macro adjustment (`macro_gate_penalty`) | **0.00** (`macro_confidence` 0.00) |
| macro-gated score (`MACRO_GATE_DRYRUN=False`, so this is the gated value) | **5.50** |
| threshold actually compared | **`CONFLUENCE_SCORE_THRESHOLD` = 2.00** |
| margin | **+3.50** — passed by 2.75× |

⚠️ Note for anyone re-deriving this: `signal_matrix.compute_score` also returns a
`threshold` of **4.0** (TREND) / 6.5 (FLAT) from `LIQUIDITY_HEATMAP_*_THRESHOLD`. **That value
is display-only.** `main.py:2865` gates on `CONFLUENCE_SCORE_THRESHOLD` (2.0). The 5.88 in the
DB is *also* not what was gated — it is the informational `adj_score`. Three numbers, one
column, per the standing fact that `trades.confluence_score` is three different quantities.

### 1.4 The advisor's decision

| field | value |
|---|---|
| `ai_decision` | **execute** |
| `ai_confidence` | **0.78** |
| `ai_model` | `claude-haiku-4-5-20251001` |
| producing system prompt | **`_ENTRY_SYSTEM_V2_ALIGNED`** (verified byte-identical to the stored `ai_system_prompt`) |

**VERBATIM reason (full, from `ai_raw_response` — the `ai_reason` column truncates at 200 chars):**

> "3-way confluence LONG, 1h ADX 29.3 (trend), 15m ADX 50.0 (strong), 5m vol 5.69x. 1d BEAR is offset by 4h/1h/15m/5m BULL agreement (3/4 MTF). Ask walls overhead are soft caution in expanding trend; bid-heavy book supports entry. Execute with awareness of daily headwind."

**VERBATIM reason of the V1 call that was overridden** (exists only in the journal — `result['raw']`
was replaced by the V2-aligned response):

> "Massive ask wall ×20.3 at $73.75 (0.31% above entry) blocks upside momentum. 1d BEAR opposes despite lower-TF bullish confluence. Risk/reward unfavorable."

### 1.5 The stored `ai_user_prompt`, VERBATIM

```
PROPOSED ENTRY: LONG
Symbol: SOL/USDT:USDT
1H: Smart Trail Switch Bullish (direction: LONG, set 2.0h ago)
15m: HyperWave Signal Up (direction: LONG, set 45m ago)
5m trigger: Bullish OB Created (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0831  |  Volume ratio 5m: 5.69x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 29.3 | 15m 50.0  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.507% | 15m 0.246% | 5m 0.113%
  EMA-gap: 1h 0.270% (Expanding) | 15m 0.474% (Flat)  (Contracting/Flat = compression)
  Market regime: TREND | MTF alignment score: 3
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 13.5, EMA-gap 1.383% (Expanding)
  4h: NEUTRAL, ADX 25.2, EMA-gap 0.480% (Contracting)
  1h: BULL, ADX 29.3, EMA-gap 0.270% (Expanding)
  15m: BULL, ADX 50.0, EMA-gap 0.474% (Flat)
  5m: BULL, ADX 56.5, EMA-gap 0.152% (Expanding)
  MTF alignment vs LONG: 3/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $73.52  |  Imbalance ±1%: 0.55 (bid-heavy)
  Massive bid walls (>4x avg vol): $73.25 (×27.4), $72.75 (×7.3)
  Massive ask walls (>4x avg vol): $73.75 (×20.3), $74.25 (×8.3), $79.25 (×4.3)

Tier agreement vs LONG (computed for this consultation):
  1H: Smart Trail Switch Bullish -> LONG = AGREES
  15m: HyperWave Signal Up -> LONG = AGREES
  5m trigger: Bullish OB Created -> LONG = AGREES
  Of the 3 tier(s) shown: 3 agree, 0 oppose, 0 neutral, 0 absent.
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.
```

---

## 2. WAS IT A RANGE, AND WAS IT LATE — measured independently

**Method.** OKX `SOL-USDT-SWAP` 5m candles pulled fresh from public REST (`history-candles`,
keyless), 14,700 candles 2026-06-12 → 2026-08-02 16:40 UTC. Windows are strictly **prior** to
the entry candle (05:00). Nothing here uses `market_regime`, `trend_*` or any bot label.

### 2a. The tape

| window | high | low | range | range % | net (first open → last close) | **directionality \|net\|/range** |
|---|---|---|---|---|---|---|
| prior **4h** | 73.51 | 72.06 | 1.45 | 2.01% | **+1.42** | **0.979** |
| prior **12h** | 73.51 | 70.51 | 3.00 | 4.25% | +0.84 | **0.280** |
| prior **24h** | 73.51 | 70.51 | 3.00 | 4.25% | **+0.36** | **0.120** |

Read plainly: **over 24 hours SOL swung 4.25% and ended 0.5% from where it started.** That is a
range by measurement, not by opinion. Over the final **4 hours** it ran +1.42 of a 1.45 range —
a one-way leg that consumed 98% of its own window.

**Volatility.** 1h ATR(14) at entry = **0.3982** (0.542% of price) against a **median of
0.4827** over the prior 14 days of hourly readings → **0.82×**, between p10 (0.311) and p90
(0.612). Volatility was *below* its own median. The prompt's `ADX(14) 1h 29.3` and
`market_regime: TREND` were reading a 4-hour impulse inside a flat 24-hour tape.

### 2b. Where in the range it entered

Position within the prior high–low, 0 = low, 1 = high:

| window | prior low | prior high | entry | **position** |
|---|---|---|---|---|
| 12h | 70.51 | 73.51 | 73.53 | **1.007** |
| 24h | 70.51 | 73.51 | 73.53 | **1.007** |
| 4h | 72.06 | 73.51 | 73.53 | 1.014 |

**The LONG was filled 2 cents ABOVE the prior 24-hour high.** Not near the top of the range —
outside it. This is a breakout fill at the range extreme.

### 2c. How far the move had already gone

| window | move already made, in the trade's direction |
|---|---|
| prior 1h | **+0.506%** |
| prior 4h | **+2.026%** |
| from the 24h low (70.51) | **+4.28%** |

### 2d. 🔴 THE SAME QUESTION TITAN ASKED — SOL's distribution first

Titan's answer was "23 of 23 entries sit in the unfavourable half", which made the variable
useless. **SOL's answer is the same shape.** Over all 20 positions in the book (vpos 7–26),
scoring a LONG as favourable when it enters below 0.5 of the prior 24h range and a SHORT when
it enters above 0.5:

> **Favourable: 1 of 20. Unfavourable: 19 of 20.**

The split by side is nearly disjoint:

- **LONGs, 24h position** (n=9): 0.377, 0.762, 0.796, 0.914, 0.937, 0.961, 0.977, 0.988, **1.007**
- **SHORTs, 24h position** (n=11): 0.038, 0.043, 0.046, 0.074, 0.080, 0.085, 0.108, 0.133, 0.143, 0.148, 0.154

**SOL always enters here.** Buying the top of the range and selling the bottom is what this
system structurally does — it is a breakout system, and "it entered near the high" is not by
itself evidence of anything. **Report the distribution before drawing a conclusion, and this
variable does not discriminate.**

**Where vpos 26 is genuinely unusual — full ranking, n=20:**

| measure | vpos 26 | min | median | max | **rank** |
|---|---|---|---|---|---|
| 12h range position | **1.007** | 0.038 | 0.159 | 1.007 | **20/20 — highest** |
| 24h range position | **1.007** | 0.038 | 0.151 | 1.007 | **20/20 — highest** |
| 4h directionality | **0.979** | 0.155 | 0.744 | 0.979 | **20/20 — highest** |
| 24h directionality | **0.120** | 0.038 | 0.505 | 0.853 | **2/20 — 2nd lowest** |
| 12h directionality | **0.280** | 0.094 | 0.675 | 0.929 | 3/20 |
| move already made, 4h | 2.026% | −0.462% | 1.089% | 5.728% | 14/20 |
| move already made, 1h | 0.506% | −0.444% | 0.524% | 4.996% | 9/20 |
| 24h range % | 4.255% | 1.534% | 4.535% | 8.815% | 10/20 |

**What the ranking says, precisely:**

1. **"Into a range" — supported, and it is the strongest signal here.** 24h directionality 0.120
   is the second-lowest of twenty entries; 12h is third-lowest. By this measure SOL has almost
   never entered into a flatter multi-hour tape than this one.
2. **"At the extreme" — supported, and it is the single most extreme entry in the book.** The
   only one of twenty above 1.0. But see 2d above: 19/20 are already in the unfavourable half,
   so this is a difference of degree inside a structural pattern, not a new failure mode.
3. **"End of a move" — supported by shape, not by distance.** The distance travelled (2.03% in
   4h) ranks only 14/20 — five entries had already run further. What is extreme is the
   *straightness*: 0.979 directionality over 4h, the highest in the book. The entry landed at
   the terminal tick of a clean 4-hour one-way leg that itself sat inside a 24-hour range.
4. **"No liquidity" — not supported. See §3.**

The combination that is genuinely novel: **highest 4h directionality AND second-lowest 24h
directionality in the same entry.** No other entry in the book pairs a maximally-straight short
leg with a maximally-flat day. That is the measured signature of "impulse into the top of a
range", and vpos 26 is the book's only instance of it.

---

## 3. THE BOOK

### 3a. Verbatim, from the stored prompt

```
Order book (pre-trade, 8000 levels):
  Mid: $73.52  |  Imbalance ±1%: 0.55 (bid-heavy)
  Massive bid walls (>4x avg vol): $73.25 (×27.4), $72.75 (×7.3)
  Massive ask walls (>4x avg vol): $73.75 (×20.3), $74.25 (×8.3), $79.25 (×4.3)
```

**There are no percentiles in it.** SOL's entry book block quotes a mid, a ±1% imbalance ratio,
and per-bucket **multiples of the same side's own mean bucket volume**. No figure is ranked
against any historical distribution. Every number, with its source and its distance from entry:

| figure | value | source | ranked against | distance from 73.53 |
|---|---|---|---|---|
| Mid | $73.52 | OKX `books-full`, `sz=4000` | — | — |
| Imbalance ±1% | 0.55 (bid-heavy) | Σ price×size within ±1% of mid, **same OKX-4000 snapshot** | — | — |
| bid wall ×27.4 | $73.25 | OKX-4000, $0.50 bucket | mean bucket vol **of the bid side of that same snapshot** | **−0.38%** |
| bid wall ×7.3 | $72.75 | ″ | ″ | −1.06% |
| **ask wall ×20.3** | **$73.75** | ″ | mean bucket vol **of the ask side of that same snapshot** | **+0.30%** |
| ask wall ×8.3 | $74.25 | ″ | ″ | +0.98% |
| ask wall ×4.3 | $79.25 | ″ | ″ | +7.78% |
| "8000 levels" | `len(bids)+len(asks)` | 4000 per side | — | — |
| threshold ">4x" | `PRE_TRADE_WALL_MULTIPLIER = 4.0` | config | — | — |

### 3b. 🔴 DOES SOL HAVE TITAN'S CROSS-SOURCE DEFECT ON THE ENTRY PATH?

**No — and it cannot, because there is no percentile anywhere in SOL's code.**
`grep -rn "percentile\|pctile\|_pct_rank" *.py` over the whole project returns **zero hits**.
Titan's defect was a *ranking against a foreign distribution*; SOL never ranks.

The self-consistency check that matters here, run anyway:

- Every entry-path figure comes from **one HTTP response**: `liquidity_zones.fetch_pre_trade_walls`
  → `GET https://www.okx.com/api/v5/market/books-full?instId=SOL-USDT-SWAP&sz=4000`, keyless,
  direct (not via Tor).
- `mult = bucket_usdt_vol / mean_bucket_usdt_vol` where **both numerator and denominator are
  computed inside `_walls()` from the same `levels` list, for the same side, in the same call**
  (`liquidity_zones.py:218-243`). Venue, depth, timestamp and side all match by construction.
- `mid` and `imbalance` come from the same `bids`/`asks` arrays.

**Verdict: SOL's entry book figures are internally sound. This is not the Titan defect.**

Three related things found while checking, none of which invalidate §3a:

1. **The mean is taken over the entire 4000-level depth.** A bucket near the mid is measured
   against a mean that includes buckets 7–8% away — visible in the prompt as a "massive wall"
   at **$79.25**, +7.78% from spot, which is a wall in name only. The near-mid multiples
   (×27.4, ×20.3) are therefore inflated relative to a near-mid-only baseline. This is a
   *methodological* property, not a cross-source error, and it applies equally to both sides so
   the bid-vs-ask comparison the advisor makes is not skewed by it.

2. **🔴 The book the advisor saw is NOT the book stored on the trade row.** `main.py:3145` writes
   `orderbook_json = json.dumps(_pre_walls)` (the OKX-4000 walls), and then the synchronous
   microstructure capture at entry fill **overwrites** it (`microstructure.py:222`) with the
   Bybit depth-20 snapshot. Row 15093's stored `orderbook_json` is
   `{"mid": 73.56, "spread": 0.01, "imbalance": 0.5942, "walls_bid":[{"price":73.5,"vol":25530.5}], "walls_ask":[], "top_bids":[...20 levels...]}`
   — a different venue, a different depth, a different mid, an **empty** ask-wall list, and no
   `mult` field at all. Confirmed on **all three** executed entry rows (13973, 14988, 15093);
   **skip** rows keep the OKX book intact (15206–15210 all carry `mult`). Consequence: anyone
   auditing an executed SOL entry from `orderbook_json` — including `signal_weights.py:211`,
   the post-trade learning loop — is reading a book the advisor never saw, and one whose
   `walls_ask: []` says the exact opposite of the ×20.3 wall that drove the decision.
   **Storage-side only; the advisor's input was correct.** Storage is explicitly NOT frozen.

3. **The recheck's wall baseline is a third number.** `virtual_positions.entry_wall_baseline_mult
   = 10.2` for this trade, against the advisor's ×20.3 — because
   `_walls_with_okx_fallback` prefers **Bybit depth-100** and only falls back to OKX-4000.
   The comparison it feeds is same-source (baseline and refresh both Bybit), so the *ratio* is
   valid — the recheck logged `wall=9.4/10.2`, `10.7/10.2`, `9.3/10.2`, all healthy. But the
   docstring at `virtual_trader.py:1041-1051` explicitly accepts that a position opened
   pre-Tor-block and refreshed mid-block **will mix Bybit-100 and OKX-4000 into one ratio** —
   that *is* Titan's cross-source class, on SOL's post-entry recheck path, present but
   **documented and deliberately accepted**, not latent. It did not fire here.

### 3c. What the book actually indicated

**Liquidity was not absent. It was abundant, and the nearest of it was against the trade.**

- **Imbalance 0.55 bid-heavy** — mild, supportive.
- **Support below:** ×27.4 at 73.25 (−0.38%) and ×7.3 at 72.75 (−1.06%). Genuinely thick.
  Incidentally the stop at 72.59 sits *below* the 72.75 wall — good geometry, arrived at by
  accident (`route=fallback_atr`, `wall=None`, `anchor_flag=OFF`; the wall anchoring is off).
- **Resistance above:** **×20.3 at 73.75, +0.30% away** — closer to the entry than either bid
  wall, and 2.4× larger than the next ask wall. Then ×8.3 at 74.25 (+0.98%).

Geometry, stated plainly: the trade entered **0.30% below a wall 20× the average bucket** and
**0.38% above a wall 27× the average**. It was filled in a 0.68%-wide pocket between two walls,
at the top of a 24h range, long.

**What happened next settles it.** The ask wall at 73.75 was never traded through. Highest print
after entry: **73.63** — twelve cents short of the wall, +0.14% MFE. Price then reversed to
**72.64**, one cent below the ×7.3 bid wall at 72.75 and **eight cents above the stop**. Both
walls the book named did exactly what a wall does.

### 3d. Did the advisor weigh the book, or recite it?

Both — in two different calls, with opposite results.

- **V1 weighed it, decisively, and refused.** Its entire first clause is the wall, with the
  correct multiple and the correct distance computed to two decimals: *"Massive ask wall ×20.3
  at $73.75 (0.31% above entry) blocks upside momentum."* This is the strongest possible
  evidence that the book block is legible and load-bearing.
- **The V2-aligned call that produced the verdict mentions it and discounts it:** *"Ask walls
  overhead are soft caution in expanding trend; bid-heavy book supports entry."* That is not
  the model independently down-weighting the wall — **its system prompt told it to**:

  > "A massive ASK wall above the entry is overhead resistance in the PATH of the move — treat
  > it as a SOFT caution, NOT a hard skip. Trending price with rising ADX routinely absorbs
  > resting liquidity and breaks through; do NOT reply 'skip' solely because of an overhead ask
  > wall."

  The deciding call was handed the conclusion about the book before it read the book. Note also
  that it cited the *bid*-heavy imbalance as support while the nearest and largest wall was on
  the ask — it weighed the softer, more distant evidence over the nearer, larger, opposing
  evidence, exactly as instructed.

---

## 4. WHAT COULD HAVE STOPPED IT AND DIDN'T

Every gate in execution order, with the value each compared.

| # | gate | where | compared | result |
|---|---|---|---|---|
| 1 | **Slot arming / no_trend** | `main.py:4025` | 1H slot held `Smart Trail Switch Bullish` LONG, set 03:00:07, TTL 360m → 120m of 360m used | **pass** |
| 2 | **HTF cascade (1h→15m→5m)** | `main.py:2426` | TREND=LONG, MOMENTUM=LONG, EXECUTION=LONG vs proposed LONG; no NEUTRAL, no OPPOSITE | **pass, unanimously** |
| 3 | Spread gate | `main.py:2679` | `SPREAD_GATE_ENABLED=False` | **not evaluated (disabled, Titan parity)** |
| 4 | Filter enforcement | `main.py:2830` | no ORIGINAL_6 / extension pattern matched this combo | pass |
| 5 | **Score gate** | `main.py:2865` | gated score **5.50** (macro adj 0.00) vs `CONFLUENCE_SCORE_THRESHOLD` **2.00** | **pass by +3.50** |
| 6 | **Risk gate** | `main.py:2903` | see below | **pass** |
| 6a | · macro-event halt | | no high-impact calendar window at 05:00 UTC 2026-08-02 | pass |
| 6b | · DXY halt | | `DXY_HALT_DRYRUN=True` — observe-only, can never block | inert |
| 6c | · **daily loss brake** | | zero closes on 2026-08-02 before 05:00 → day loss 0.00R vs `DAILY_LOSS_R_LIMIT` 3.0 | pass, wide |
| 6d | · position cap | | 0 open LONG vs `MAX_POSITIONS_PER_SIDE` 1 | pass |
| 6e | · **loss streak** | | last 3 executed PnL rows: **+126.52, −234.03, −93.24** → streak **2 of 3** vs `LOSS_STREAK_THRESHOLD` **3** | **pass — one loss from a 4h cooldown** ⚠️ |
| 7 | Fee gate | `main.py:2929` | `FEE_GATE_ENABLED=False` | **not evaluated (disabled, Titan parity)** |
| 8 | **OKX wall-avoidance block** | `main.py:2975` | `WALL_AVOIDANCE_ENABLED=False` — **dead by design.** Had it been True it would have compared the nearest ask cluster ≥ spot against `WALL_AVOIDANCE_THRESHOLD_PCT = 0.35%`. The ×20.3 wall bucket sat at **+0.299%** | **⚠️ inside the threshold — this gate would have blocked the trade if it were enabled** |
| 9 | **Advisor V1** | `claude_advisor.py:493` | `_ENTRY_SYSTEM` | **🔴 SKIP** — "Massive ask wall ×20.3 … Risk/reward unfavorable." |
| 10 | Wall-rule V2 shadow | `claude_advisor.py:506` | `_ENTRY_SYSTEM_V2`, log-only | **skip** (`AGREE skip`) — was still enabled at 05:00; turned off ~14:5x the same day |
| 11 | **🔴 Aligned-LONG V2 override** | `claude_advisor.py:536-563` | direction LONG ✓ · `trend_1h='bull'` ∈ {bull, neutral} ✓ · `srv_adx_1h` **29.33 ≥ 25.0** ✓ · `ADVISOR_WALL_ALIGNED_V2=True` (LIVE) | **FIRED → verdict replaced with `execute` (0.78)** |
| 12 | Observation mode | `main.py:3283` | `MERCURY_OBSERVATION_MODE=1` | routed to paper engine, **no real order** |
| 13 | Post-entry recheck | `virtual_trader.py:1174` | T+10s / T+60s / T+300s, score 0 each | OK — no negative deltas |

### 4.1 The three that came close

1. **The advisor itself — it did not come close, it said no.** Two of three Claude calls
   returned `skip`. The gate that overrode them is deterministic and cannot be talked out of it.
2. **`WALL_AVOIDANCE_THRESHOLD_PCT = 0.35%` vs a wall at +0.299%.** Inside the threshold by
   5 basis points. The gate is disabled for Titan parity (`WALL_AVOIDANCE_ENABLED=False`,
   A2 2026-06-08 — "walls advisory-only, fed to Claude, NO hard block"). Caveat: that check
   reads `liquidity_zones.fetch_clusters` (top-3 by volume, $0.10 buckets), not
   `fetch_pre_trade_walls` ($0.50 buckets) — same book, different granularity — and the cluster
   list was not persisted for this row (`lz_near_ask_*` writes were removed in P2, Titan
   parity), so this is a same-book inference, not a replay.
3. **Loss streak 2 of 3.** One more losing close before 05:00 and a 4-hour cooldown would have
   been in force. Nothing to fix — recorded because it is the only *value* gate that was
   genuinely near its limit.

### 4.2 🔴 THE 1H TIER — did it change the shape of the reasoning?

**First: the flip is now CONFIRMED from rendered production prompts, which it was not before.**
`OPEN-ITEMS-SOL.md` requires this confirmation and lists the flip as applied-but-unconfirmed.
Across **all 74** consultations stored since the 17:13:02 restart (through 16:45:02 today):

| check | count |
|---|---|
| prompts carrying `Of the 3 tier(s) shown` | **74 / 74** |
| prompts carrying `1H LuxAlgo tier: NOT SHOWN` | **0** |
| prompts carrying the old false `The 3 timeframes are aligned` | **0** |

`AI_ADVISOR_HIDE_1H = False` is live and rendering. The `except ImportError` fallback at
`claude_advisor.py:29-32` has not silently re-hidden it. **This item can be closed.**

**Second: on this trade the 1H AGREED.** `1H: Smart Trail Switch Bullish -> LONG = AGREES`,
age 2.0h, in a `3 agree, 0 oppose, 0 neutral, 0 absent` tally.

**Third — and this is the part that matters for the experiment: this consultation is in the
AGREEING population, not the disagreeing one the window is built to measure.** Its 15m and 5m
tiers both point LONG, so under the pre-registered (deliberately unchanged) 15m-vs-5m definition
it belongs to the population whose baseline wrong-side rate is **0.05% (1 / 1,882)**. It is not
evidence about the treatment. Window composition so far:

| tally | n |
|---|---|
| 3 agree, 0 oppose | 37 |
| 2 agree, 1 oppose | 24 |
| 1 agree, 2 oppose | 13 |

**Fourth: did seeing three tiers change the reasoning?** The deciding reason opens *"3-way
confluence LONG"* — language about three tiers, which the prompt now genuinely supports. But
that phrasing is not new: `3-way`/`three-way` appears in **5 of 2,946** pre-flip reasons and
**1 of 74** in the window. The 1H is named in 50 of 74 window reasons vs 1,968 of 2,946
pre-flip. **Neither difference is measurable at this n.** No conclusion is available, and none
is offered.

What can be said without statistics: the deciding call cited *"4h/1h/15m/5m BULL agreement
(3/4 MTF)"* — which is the **OHLCV-derived** HTF block, a line that was present before the flip
too. It did not cite the LuxAlgo 1H tier identity. The newly-visible field appears not to have
been the thing it reasoned from.

### 4.3 One measurement defect found on the way

`virtual_positions.entry_adx_1h = 45.83` for this trade. The prompt shown to the advisor at the
same instant said **1h ADX 29.3**. Two numbers, same indicator, same timeframe, same moment.

**Cause — Titan's "one ADX, two windows", present on SOL:**

| consumer | fetch | candles | ADX(14) |
|---|---|---|---|
| entry snapshot (`indicators.fetch_snapshot`) | `CANDLE_LIMIT` | **200** | 29.3 (bot) |
| post-entry recheck (`_recheck_fetch_1h_metrics`) | `ATR_LEN * 3` | **42** | 45.8 (bot) |

Reproduced independently on OKX 1h candles at 2026-08-02 05:00 UTC:

```
1h ADX(14), last  42 candles -> 45.07     <- the recheck's window
1h ADX(14), last 100 candles -> 31.67
1h ADX(14), last 200 candles -> 31.73     <- the snapshot's window
```

42 candles gives Wilder's smoothing ~14 iterations after warm-up — not converged, and it
**over-reads by ~13 points**.

**This did not affect the trade.** The recheck compares its own 42-candle entry baseline against
its own 42-candle refresh, so the delta rule is same-window and sound; and the gate that
actually fired (`ADX >= 25.0` in the aligned-V2 block) read the **200-candle** 29.33, which
clears 25.0 by 4.33 either way. It is a **reporting** defect: the same DB row carries 45.8 and
29.3 as "the 1h ADX", and the recheck's Telegram/journal line prints the number the advisor was
never shown. Recorded, not acted on — the recheck is on the exit side, explicitly outside the
freeze.

### 4.4 A stale line in the canonical file

`OPEN-ITEMS-SOL.md` STANDING FACTS still says *"`trades.ai_system_prompt` always stores the V1
base prompt, even when a V2/aligned prompt produced the verdict."* **Row 15093 disproves it**:
the stored prompt is byte-identical to `_ENTRY_SYSTEM_V2_ALIGNED`, not to `_ENTRY_SYSTEM`. The
provenance fix landed 2026-08-01 (`claude_advisor.py:548-583`, `_verdict_system`) and works.
Exactly the failure mode the file warns about in its own header — the canonical copy went stale
while the dated reports moved on. Noted here so the next reader does not re-derive the old fact.

---

## 5. CONTEXT, NOT EVIDENCE

**Under the current (final, four-item) prompt form there have been 74 consultations and
exactly 2 entries.**

| | |
|---|---|
| window opened | 2026-08-01 17:13:02 UTC (worker pid 1126633) |
| consultations, window | **74 of 200** as of 2026-08-02 16:45:02 UTC |
| verdicts | 72 skip · **2 execute** |
| the two entries | **vpos 25** (SHORT, 2026-08-01 17:20, closed `trail` **+$126.52**) · **vpos 26** (this LONG, open, **−0.36R**) |
| orphan row 14981 | excluded from the count and from every pooled statistic, per the pre-registration |

**n = 2. Nothing about the prompt form, the 1H tier, the aligned-V2 override or SOL's entry
quality can be concluded from this trade.** One of the two entries under the new form is a
+$126 winner and one is currently −$46; that comparison is noise and should not be quoted as
anything else.

The freeze holds. Per the pre-registered rule, defects found inside the window are recorded as
caveats and **the counter is not reset** — the two items above (§3b.2 storage overwrite, §4.3
ADX window) are storage- and exit-side, both explicitly outside the frozen surface, and neither
changes a single value the entry advisor read.

**Nothing in this document is a recommendation.** The one finding that would justify a decision
if it survived more data — that the aligned-LONG V2 override took a trade the advisor refused,
on a wall that then held — is **one trade**, and the override's own evidence base (n=102, 30d
drift study) is larger than this counter-example. Since the window opened the override fired
**once**, against **18 HELD** cases where V1's skip stood.

---

## APPENDIX — how to reproduce

```bash
# the trade
sqlite3 "file:/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db?mode=ro" \
  "select * from virtual_positions where id=26;"
sqlite3 "file:.../trades.db?mode=ro" "select ai_user_prompt,ai_raw_response from trades where id=15093;"

# the override, verbatim
journalctl -u mercury-sol --since "2026-08-02 05:00" --until "2026-08-02 05:01" --no-pager

# the tape (independent of the bot)
curl -s "https://www.okx.com/api/v5/market/history-candles?instId=SOL-USDT-SWAP&bar=5m&limit=100&after=<ms>"

# no percentiles anywhere
cd /mnt/volume_nyc1_1780480650620/mercury-sol && grep -rn "percentile\|pctile\|_pct_rank" *.py   # -> 0 hits
```

_Generated 2026-08-02, read-only session. Mercury-SOL is PAPER; no order was placed by the bot
or by this analysis. Titan was not touched._
