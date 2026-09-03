# mercury-sol-vpos42-second-pass

_2026-09-03 16:37 UTC_

---

# POST-MORTEM (SECOND PASS) — LIVE SHORT vpos 42, SOL/USDT:USDT · 99.24 → 101.87 · net −$2.8381

**Mercury-SOL READ-ONLY.** DB opened `file:…?mode=ro` (SELECT only), `config.py` /
`trail_arm.py` / `main.py` / `virtual_trader.py` / `indicators.py` read **as text** with
`sed`/`grep` and cited by line — never imported. Venue touched with **GET only**. No order,
no cancel, no restart, no config edit. Controls at the foot.

Titan pre-flight `tools/openitems_guard.py` → **exit 0, clean** (11 watched values agree,
titan-bot HEAD f5d3542). Titan untouched thereafter.

**This is a SECOND PASS.** A first post-mortem on this same trade exists —
`2026-09-03-1552-mercury-sol-vpos42-short-post-mortem.md`. Its conclusions are confirmed here
on independent evidence. This pass adds three things that file could not have: **the venue's
own private order history**, **the true traded low from exchange candles**, and **the sibling
consultation 25 minutes before the entry**. It corrects two of its numbers. Both are marked 🆕
and ✏️ below.

---

## 0. IDENTIFICATION — read from the ledger, not assumed

`virtual_positions.id = 42`, `is_paper = 0`. Matched to the card by net PnL to 8 decimals.

| field | value |
|---|---|
| **vpos id** | **42** |
| entry trades row | 23053 · venue order `85ca0a10-89c6-4693-a946-7124fb81361e` |
| opened / closed | 2026-09-01T21:40:18.343Z → 2026-09-03T13:42:12.484Z |
| **hold** | **40 h 01 m 54 s** |
| size / margin / leverage | 1.0 SOL · 20.0 USDT · 5× |
| entry fill / close | 99.24 → 101.87 · `close_reason = 'sl'` |
| ATR(1h) at entry | 1.04651359001191 |
| `original_sl` / `sl_price` at close | 101.86 / **101.86 — identical, never moved** |
| **1R** (`initial_risk_usdt`) | **$2.6200** |
| gross / fees / funding / net | −2.6300 / 0.20111 / 0.00701167 / **−2.83812167** |
| **net in R** | **−1.0833 R** |
| `water_mark` (best price the poller saw) | **97.34** |
| `mgmt_state_json` | `{"breakeven_applied": false, "exit_advisor_last_ts": …}` — **no `trail_armed` key exists** |
| `entry_adx_1h` / window | 29.416956796965152 / 200 |

🆕 **Venue corroboration (private GET `/v5/position/closed-pnl`, read-only):**
`avgEntryPrice 99.24 · avgExitPrice 101.87 · closedPnl −2.83812167 · openFee 0.09924 ·
closeFee 0.10187`. The ledger and the exchange agree to the eighth decimal.

---

# 1. WHY DID IT ENTER?

## 1a. Tiers, weights, score arithmetic, cascade verdict

**The cascade slots** (`combo_key`):

| slot | signal | direction | age at entry | vs SHORT |
|---|---|---|---|---|
| 1H | `15m-rearm: Reversal Up` | **LONG** | 1.7 h (102 m) | **OPPOSES** |
| 15m | `HyperWave Signal Down` | SHORT | 25 m | agrees (`hw_15m_weight` 1.05) |
| 5m trigger | `Bearish New Imbalance` | SHORT | 0 m | agrees |

**The matrix signals that actually produced the score — a different set:**

| category | canonical id | dir | age (min) | intensity | points |
|---|---|---|---|---|---|
| TREND | `neo_cloud_switch_bear` | SHORT | 159.96 | 0.9 | **2.25** |
| MOMENTUM | `hw_signal_down` | SHORT | 25.00 | 0.7 | **1.75** |
| LIQUIDITY | `imb_new_bear` | SHORT | 0.0004 | 0.7 | **1.75** |
| EXECUTION | — | NEUTRAL | — | — | 0.00 |

`contribution = intensity_weight × CATEGORY_MAX_POINTS(2.5)` (signal_matrix.py:45,289). No
intra- or inter-category conflict on any of the four.

**Score arithmetic** (journal line, 21:40:11):

```
raw matrix score            5.75  SHORT   (2.25 + 1.75 + 1.75 + 0.00)
macro adjustment           +0.00           macro_gate_penalty = 0.0; MACRO_GATE_DRYRUN=False
                                           (config.py:767) so the GATED quantity is raw+macro
GATED value at the gate     5.75
CONFLUENCE_SCORE_THRESHOLD  2.00           (config.py:670)              -> PASSED, 2.9×
weighted_adj               +0.3708         (storage/telemetry, not the gate)
displayed confluence_score  6.12  = 5.75 + 0.3708
matrix threshold recorded   4.00           = LIQUIDITY_HEATMAP_TREND_THRESHOLD (config.py:672)
```

`weighted_adj` breakdown: `ema_cross_15m +0.04, ema_cross_1h +0.04, ema_slope_15m +0.02,
ema_slope_1h +0.02, dxy +0.20, news 0.00, mtf +0.3008, funding −0.25`.

config.py:670 states in its own comment that at 2.0 *"the AI consult is the real entry
filter"*. **The score gate is not where this trade was decided.**

### ✏️ Cascade verdict — corrected

The 15:52 file records "cascade passed … the tiers did not agree: 2 agree, 1 opposes". The
first half is right, the second conflates two different objects. The gate at
`main.py:4091` evaluates `signal_matrix.htf_alignment(matrix_result, direction)` — **the
matrix categories, not the cascade slots.** The journal at 21:40:00 shows what it saw:

```
HTF_WOULD_PASS (tolerate-NEUTRAL) SHORT 1H=SHORT 15m=SHORT 5m=NEUTRAL
                                  was='5m NEUTRAL (no active EXECUTION signal)'
```

Its "1H tier" was `neo_cloud_switch_bear` (**SHORT, agreeing**). It passed under
`neutral_tolerated` because the 5m EXECUTION slot had gone NEUTRAL (EXECUTION TTL is 5 min,
config.py:682 — the 21:15 `ibos_bear`/`ob_created_bear` had expired).

🔴 **So the opposing LONG 1H tier was never in front of the cascade at all.** The cascade
saw a 1H that agreed; the advisor saw a 1H that opposed. **Two judges, one instant, two
different 1H facts** — the "one-fact-many-judges" defect config.py:404 names by that phrase.

## 1b. 🔴 `trend_1d` and `trend_4h` AT ENTRY — THIS IS **NOT** AN OVERRIDE

```
trend_1d = 'neutral'   ADX(1d) 49.5   EMA-gap 7.193% Contracting   ema_status_1d 'Bullish'
trend_4h = 'bear'      ADX(4h) 18.8   EMA-gap 0.885% Expanding
trend_1h = 'bear'      trend_15m = 'bear'      trend_5m = 'bear'
MTF alignment vs SHORT: 4/4 (4H/1H/15m/5m; excludes 1d)
```

**Stated plainly: the daily regime did NOT oppose this short.** It was NEUTRAL, and the 4h —
the other half of the standing order's "dominant regime" — actively **agreed** with the
short. The standing order never engaged. It was not overridden; it was silent.

**The population reproduces exactly.** The ruler is "1d **or** 4h opposes the proposed side",
cut at the moment of this consult:

```
n = 2,127   obeyed (skip) = 2,121   overridden (execute) = 6   -> 99.72 % obeyed
```

— the operator's figures to the unit. Under the stricter "1d alone opposes" ruler the
population is n = 1,321 with the **same 6** overrides. The count is robust to the ruler.
**vpos 42 is in neither population. It is not the seventh override.**

*One labelling nuance, not an override.* `ema_status_1d` was **Bullish** and ADX(1d) 49.5 was
the strongest number on the board, yet the label read NEUTRAL. `indicators.py:322-329`
requires `close > ema9 > ema21 AND slope > flat` for BULL; the 1d EMA-gap was **Contracting**,
so the daily uptrend was decaying and the classifier withheld the label. Defensible — and
worth knowing that "neutral" here meant "a bull trend losing its slope", not "no trend".

## 1c. 🔴 THE ADVISOR'S PROMPT AND REASON, VERBATIM

**SYSTEM PROMPT (untruncated):**

```
You are an automated trading decision module for a SOL/USDT perpetual swing bot. You receive multi-timeframe LuxAlgo signal context (1H trend, 15m confirmation, 5m trigger) at the moment 3-way confluence has just fired and the bot is about to place a single market entry. You also receive real-time market context: a Volatility/regime block (ADX on 1h/15m, ATR% of price, EMA-gap compression, market_regime, MTF alignment) plus volume ratio, and pre-trade order-book walls.

You also receive a 'Higher Timeframes Trend' block: an OHLCV-derived (EMA/ADX) trend label, ADX, and EMA-gap for 1d/4h/1h/15m/5m, independent of the LuxAlgo signals. Treat the 1d and 4h trends as the dominant regime: when they clearly oppose the proposed entry direction, lean toward 'skip' unless the lower-TF confluence is exceptionally strong; when 1d/4h agree with the entry, that is supportive context.

Your job is to gate that entry: vote 'execute' when the context looks coherent, 'skip' when it looks like a chop/false break or contradicts the higher-timeframe regime.

HARD RULE — opposing walls: if a massive limit wall (volume marked with a multiplier, e.g. ×8.3) sits directly above a LONG entry or directly below a SHORT entry, you MUST reply 'skip'. A thick wall in the opposing direction represents strong resting liquidity that will absorb the move before it can develop.

SOFT RULE — FLAT-MARKET GUARD: read the multi-TF Volatility/regime block. Treat the market as flat/squeezed when 1h ADX is low (~<20-23) AND ATR% is low on 1h/15m AND the EMA-gap is Contracting/Flat (and/or market_regime is FLAT with weak MTF alignment). In a flat market, prefer 'skip' UNLESS the LuxAlgo confluence is exceptionally strong (clear multi-TF agreement). Conversely, do NOT skip a genuine trend (rising/high ADX, Expanding EMA-gap, market_regime=TREND) merely because absolute ATR looks small in a low-volatility era. Weigh these factors together — this is soft, multi-factor judgment, not a hard numeric gate; strong confluence can override.

Respond with ONLY a single JSON object, no markdown, no prose. Fields: decide ("execute"|"skip"), confidence (float 0.0-1.0), reason (string, max 80 chars).
```

**USER PROMPT (untruncated):**

```
PROPOSED ENTRY: SHORT
Symbol: SOL/USDT:USDT
1H: 15m-rearm: Reversal Up (direction: LONG, set 1.7h ago)
15m: HyperWave Signal Down (direction: SHORT, set 25m ago)
5m trigger: Bearish New Imbalance (direction: SHORT)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.3050  |  Volume ratio 5m: 0.99x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 29.4 | 15m 53.2  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 1.059% | 15m 0.605% | 5m 0.307%
  EMA-gap: 1h 0.974% (Expanding) | 15m 0.439% (Expanding)  (Contracting/Flat = compression)
  Market regime: TREND | MTF alignment score: 4
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: NEUTRAL, ADX 49.5, EMA-gap 7.193% (Contracting)
  4h: BEAR, ADX 18.8, EMA-gap 0.885% (Expanding)
  1h: BEAR, ADX 29.4, EMA-gap 0.974% (Expanding)
  15m: BEAR, ADX 53.2, EMA-gap 0.439% (Expanding)
  5m: BEAR, ADX 27.1, EMA-gap 0.187% (Expanding)
  MTF alignment vs SHORT: 4/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $99.25  |  Imbalance ±1%: 0.53 (bid-heavy)
  Bid walls (>4x avg vol): $99.25 (p55, x8.8), $98.75 (p31, x5.7), $98.25 (p29, x5.5), $96.25 (p42, x6.9), $95.25 (p15, x4.6)
  Ask walls (>4x avg vol): $99.25 (p39, x6.5), $99.75 (p31, x5.7), $106.25 (p39, x6.5), $107.25 (p18, x4.7), $107.75 (p5, x4.2)
  Wall figures: pN = this wall's PERCENTILE among all walls this prompt has rendered (n=23,080; the primary figure), xN = the raw volume multiple (secondary). Every wall listed already passed the >4x filter, so the multiple alone does not distinguish an ordinary wall from a thick one — the percentile does. CALIBRATION: ~p50 is an ORDINARY wall, p90+ is genuinely thick. Judge thickness by the percentile, not by the word "massive" or by the multiple.

Tier agreement vs SHORT (computed for this consultation):
  1H: 15m-rearm: Reversal Up -> LONG = OPPOSES
  15m: HyperWave Signal Down -> SHORT = AGREES
  5m trigger: Bearish New Imbalance -> SHORT = AGREES
  Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 2 agree, 1 oppose, 0 neutral, 0 absent.
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.
```

**RAW RESPONSE (untruncated), `ai_model = claude-haiku-4-5-20251001`:**

```json
{
  "decide": "execute",
  "confidence": 0.78,
  "reason": "4/4 MTF bear alignment (4h-5m), 15m/5m SHORT agree, strong ADX+trend. 1h rearm stale."
}
```

### Every checkable claim in the reason, against the prompt it was given

| # | claim | verdict |
|---|---|---|
| 1 | "4/4 MTF bear alignment (4h-5m)" | ✅ prompt: *"MTF alignment vs SHORT: 4/4 (4H/1H/15m/5m; excludes 1d)"* — exact, and it correctly named the excluded 1d by writing the range as 4h–5m. |
| 2 | "15m/5m SHORT agree" | ✅ prompt tier table: both AGREES. |
| 3 | "strong ADX+trend" | ✅ ADX 1h 29.4, 15m 53.2, `Market regime: TREND`, both EMA-gaps Expanding. |
| 4 | **"1h rearm stale"** | ❌ **NOT SUPPORTED BY THE PROMPT.** The prompt gives an **age** ("set 1.7h ago") and no staleness verdict. `claude_advisor.py:605,619-621` appends the literal marker *", STALE — past the 6h window the gate itself uses for this tier"* only when the tier exceeds `CATEGORY_TTL_MINUTES['TREND'] = 360 min`. The tier was **102 minutes old — 28 % of that window**, so the marker was correctly withheld. The prompt's own counting rule says the opposite of the model's conclusion: **"AS COUNTED (stale tiers vote in full): 2 agree, 1 oppose"**. The model invented a disqualification for the only tier that opposed the trade. |

🆕 **And it is worse than an invention — it is a reversal of the same model's own reasoning
25 minutes earlier.**

`trades` row **23052**, 2026-09-01 21:15, the same setup, same model, **`skip`, confidence
0.78** — verbatim:

> *"1H tier opposes SHORT (Reversal Up/LONG set 75m ago). Despite 15m/5m confluence and strong
> lower-TF trend alignment (4H/1H/15m/5m all BEAR, 15m ADX 52.7), the active 1H reversal signal
> creates directi…"* (stored reason is itself truncated at 200 chars by the column write)

Its prompt was near-identical: same 1d NEUTRAL / 4h BEAR block, same 4/4 MTF, same tier table
reading `1H … LONG = OPPOSES`, same "2 agree, 1 oppose". The **only** material deltas in 25
minutes:

| | 21:15 (row 23052, SKIP) | 21:40 (row 23053, EXECUTE) |
|---|---|---|
| 1H tier | Reversal Up / **LONG**, 75 m old | the **same** tier, **102 m** old |
| 5m trigger | Bearish I-BOS | Bearish New Imbalance |
| 5m ADX / vol ratio | 24.9 / 2.63× | 27.1 / **0.99×** |
| raw score | 4.75 | 5.75 |
| verdict | **skip** @ 0.78 | **execute** @ 0.78 |

🔴 **The opposing tier did not resolve, did not flip, and did not expire. It only got older —
and the model that had just called it disqualifying called it "stale" and traded through it.**
Volume ratio, meanwhile, fell from 2.63× to 0.99×, i.e. the *worse* of the two tapes was the
one that got the order.

## 1d. The order book as rendered

```
Mid $99.25 · depth 8,000 levels · imbalance ±1%: 0.53 — BID-HEAVY, i.e. against the short
wall threshold 4.0× · percentile base n = 23,080 rendered walls

SUPPORTING (ask walls, above a SHORT):   $99.25 p39 ×6.5 · $99.75 p31 ×5.7 ·
                                         $106.25 p39 ×6.5 · $107.25 p18 ×4.7 · $107.75 p5 ×4.2
OPPOSING   (bid walls, below a SHORT):   $99.25 p55 ×8.8 · $98.75 p31 ×5.7 · $98.25 p29 ×5.5 ·
                                         $96.25 p42 ×6.9 · $95.25 p15 ×4.6
(advisor_book_json also carries a 6th ask wall at $120.25 p— ×6.9, outside the rendered five)
```

**Book gate columns:** `book_gate_clause = ''` (empty — no clause fired),
`opp_mult 5.7 · opp_pctl 5.0 · opp_dist_pct 0.5038 · lean 0.4667 · n_supporting 5`. The gate's
nominated opposing wall was **$98.75** (0.50 % below), not the ×8.8 at the mid.
`BOOK_GATE_DRYRUN = False` (config.py:475) — the gate was **armed** and it **admitted**.

**Did the reason cite the book? No — not one word.** The reason names MTF, tiers and ADX only.

That silence is defensible under the prompt's own calibration and **not** defensible on the
whole picture:
- The thickest opposing wall, ×8.8 at $99.25, sat at **p55** — the prompt says "~p50 is an
  ORDINARY wall, p90+ is genuinely thick". By the rule the model was given, the HARD RULE did
  not trigger. ✅
- But the ±1 % imbalance was **0.53 bid-heavy** — resting liquidity leaning *against* the
  short — and the tape block behind it (`tape_json`) showed `buy_share 0.1781`, `pressure
  sell`. The model was handed a book that leaned against it and a tape that leaned with it,
  and weighed neither out loud. **Not an error; an unexamined contradiction.**

## 1e. The flat/ADX gate

```
FLAT_ADX_GATE_ENABLED = True                     (config.py:406)
FLAT_ADX_GATE_DRYRUN  = False   # 🔴 ARMED. This gate REFUSES ENTRIES.   (config.py:407)
threshold = ADX_BELOW_FLOOR = 20.0 — deliberately no private constant (config.py:409-411)
```

**ADX(1h) at entry = 29.416956796965152**, window 200 (`entry_adx_1h_window`). It cleared the
20.0 floor by **+47 %**. It did not squeak through and it was not bypassed: the gate refuses
below 20 and this read 29.4. Corroborated three ways — the same value appears in the advisor
prompt ("1h 29.4"), in `trades.srv_adx_1h`, and in the T+10s recheck journal line
(`adx=ADX1h=29.4 (entry ADX1h=29.4) … verdict=OK`). The regime label was `TREND`, both EMA
gaps Expanding, MTF alignment 4.

**The flat gate is not part of this failure.** This was a genuinely trending tape.

---

# 2. 🔴 WAS IT RIGHT TO ENTER? — judged on what was knowable BEFORE the move

## 2a. Was it in the population the daily-regime instruction would refuse?

**No.** `trend_1d = neutral`, `trend_4h = bear` (agreeing). Neither of the two timeframes the
system prompt names as "the dominant regime" opposed the short. The instruction was silent,
not overridden.

**It is not the seventh override.** The record stands unchanged:

| # | row | date | side | 1d | outcome |
|---|---|---|---|---|---|
| 1 | 4259 | 06-24 | LONG | bear | — |
| 2 | 11181 | 07-19 | LONG | bear | — |
| 3 | 15093 | 08-02 | LONG | bear | — |
| 4 | 17289 | 08-10 | **SHORT** | bull | vpos 32, **−0.180 R** |
| 5 | 18111 | 08-13 | **SHORT** | bull | vpos 34, **−0.643 R** |
| (6) | 11180 | 07-19 | LONG | bear | `observed_skipped` shadow of #2 |

6 overrides, 2,121 obeyed of 2,127, **both live SHORT overrides lost** — all as the operator
stated, and **all unchanged by this trade**.

## 2b. 🔴 SOL's live SHORT book — it is now SIX, and the running total

| vpos | entry → exit | reason | net $ | R |
|---|---|---|---|---|
| 32 | 76.18 → 76.24 | exit_signal | −0.2663 | **−0.180** |
| 34 | 75.21 → 75.76 | sl | −0.9113 | **−0.643** |
| 35 | 75.16 → 75.57 | sl | −0.7289 | **−0.701** |
| 36 | 75.20 → 75.62 | exchange_market | −0.7278 | **−0.757** |
| 37 | 74.38 → 75.09 | sl | −1.1156 | **−1.226** |
| **42** | **99.24 → 101.87** | **sl** | **−2.8381** | **−1.083** |

```
SHORT  n = 6   ΣR = −4.589   net = −$6.5880   winners = 0
LONG   n = 8   ΣR = +10.730  net = +$22.1455  winners = 6
BOOK   n = 14  ΣR = +6.141   net = +$15.5574   <- matches the card exactly
```

🔴 **Stated plainly: the live short side has NEVER produced a winner. Six positions, six
losses, zero winners, ΣR −4.589.** Every dollar of the live book's +$15.5574 was made by the
long side; the short side has given back $6.59 of it.

**This is also exactly where n cannot rank.** Six same-signed outcomes cannot separate "the
short side has no edge" from "six draws from a −0.09 R/trade book that happened to land on one
side". A fair coin gives six of one side 1.6 % of the time — unlikely, not absurd, and the
book's per-trade mean is not zero to begin with. The honest statement is the descriptive one:
**there is no live evidence that the short side works, and there is not yet enough to prove it
does not.**

## 2c. 🔴 Judge the REASONING, not the outcome

**Sound in three of four parts, and the fourth is the one that mattered.**

Sound: the tape was genuinely trending (ADX 1h 29.4, 15m 53.2, both gaps expanding, regime
TREND) — the flat guard rightly stayed quiet. The dominant regime did not oppose the trade;
4h/1h/15m/5m all read BEAR, 4/4. The hard wall rule was correctly *not* triggered: the ×8.8
was p55, an ordinary wall by the prompt's own calibration. The score cleared its gate 2.9×.
A trader shown that board would take the short.

Unsound, and decisive: **the single opposing fact was disposed of with a claim the prompt does
not support.** The 1H tier was LONG, 102 minutes old, inside a 360-minute window, and the
prompt had told the model in as many words that stale tiers *vote in full*. The model wrote
"1h rearm stale" and moved on. **Twenty-five minutes earlier the same model, at the same
confidence, had refused this trade citing that exact tier.** Nothing about the tier changed
except its age, and age made it *closer* to stale-by-the-rule, not further from it.

**Verdict: this was a bad decision, not merely a losing trade** — but the badness is narrow
and precise. It is not "it shorted into a bull daily" (it did not). It is not "it traded chop"
(it did not). It is: **the one veto in the prompt was dismissed by an unsupported assertion,
and the record shows the same model applying the opposite judgment to the same fact minutes
before.** That is a reasoning defect, and it is reproducible in the ledger, not inferred from
the loss.

**Second, structural, and independent of the model:** the cascade and the advisor were shown
**different 1H tiers at the same instant** (§1a). The gate that could have blocked never saw
the opposing signal; the judge that saw it talked itself out of it. No single component was
given the whole fact.

---

# 3. 🔴 WHY DID IT SIT SO LONG WHILE IN PROFIT?

## 3a. The price path, MFE, and the hold

Hourly extremes from the position's own 2,940 excursion samples (median gap 51 s), cross-checked
against **482 real 5m Bybit candles** pulled fresh over the bot's own Tor route:

```
elapsed   window                          low     high    running MFE
  0-3 h   09-01 21:40 → 00:40            99.20  100.16    0.04 %     drifts against
  4   h   09-02 01:40 → 02:40            98.49   99.70    0.76 %     first dip
  5-11 h  09-02 02:40 → 08:40            98.55  100.62    0.76 %     seven hours of nothing
 12   h   09-02 09:40 → 10:40            97.89   98.73    1.36 %
 13   h   09-02 10:40 → 11:40            97.38   98.21    1.91 %  <- THE PEAK
 14-15 h  09-02 11:40 → 13:40            97.60   98.37    1.91 %
 16   h   09-02 13:40 → 14:40            98.23   99.58    1.91 %     the turn
 17-27 h  09-02 14:40 → 09-03 00:40      98.16  100.44    1.91 %     grinds back through entry
 28-39 h  09-03 00:40 → 12:40            99.30  101.72    1.91 %     grinds to the stop
 40   h   09-03 13:40 → 13:42            101.63 101.69    1.91 %     stopped
```

🆕 **The true traded low, from the exchange's own candles: `97.29`, on the 09-02 11:20 5m
candle (O 97.83 H 97.84 **L 97.29** C 97.47).** The engine's 10-second poller recorded
`water_mark = 97.34` — it missed the true extreme by 5 cents, as a 10 s sampler will.

| MFE | price | in % | in R (gross) |
|---|---|---|---|
| as the engine saw it (`water_mark`) | 97.34 | **1.9146 %** | **+0.7252 R** |
| 🆕 as the venue actually traded | **97.29** | **1.9649 %** | **+0.7443 R** |

**When:** 13 h 40 m into a 40 h 02 m hold — at **34 %** of the way through. The position spent
its remaining **26 hours 22 minutes** giving the peak back and then losing 1R.

## 3b. 🔴 DID THE TRAIL EVER ARM? — **NO. It missed by 1.2 cents.**

```
config.py:249   TRAIL_ARM_R    = 0.75
config.py:104   TRAIL_MULT_ATR = 1.875      (the callback, decoupled from the stop)
trail_arm.py:activation_distance()  ->  TRAIL_ARM_R × SL_BUFFER_ATR × atr
                                     =  0.75 × 2.5 × 1.04651359001191  =  1.9622130

ARM PRICE (SHORT) = 99.24 − 1.9622130 = 97.2777870
```

✏️ *The 15:52 file states this arm as `97.27500`, writing "99.24 − 1.96221 = 97.27500". The
subtraction is 97.27779. The 97.2750 figure is real but it is a **different** number — it is
what the exit-advisor prompt prints, derived from the rounded `1R = 2.62` (99.24 − 0.75×2.62).
Both are quoted below; neither was reached, so nothing downstream changes.*

| | value |
|---|---|
| arm price the **engine compares against** (`virtual_trader.py:2122`) | **97.2777870** |
| arm price the **exit-advisor prompt displays** | 97.2750 |
| best price the poller saw (`water_mark`) | 97.34 — **6.2 ¢ short** (0.0237 R) |
| 🆕 **best price the venue actually traded** | **97.29 — 1.2 ¢ short of 97.27779** (0.0047 R) |
| tick samples at or below the arm | **0 of 2,940** |
| 5m candle lows at or below the arm | **0 of 482** |
| `mgmt_state_json` | `"breakeven_applied": false` — no arm key ever written |

🔴 **MFE reached +0.7443 R against an arm of 0.75 R. It fell short by 0.0057 R — one and a
fifth US cents on a $99 instrument.** This is not a sampling artefact: the poller's 97.34 and
the venue's true 97.29 both sit above the arm, so the answer is the same whichever number you
use.

**The trail therefore never existed for this position.** Had it armed at the true low, the
callback (`virtual_trader.py:2226`, `water_mark × (1 + trail_pct/100)`, `trail_pct = 1.975`)
would have parked at 97.29 × 1.01975 = **99.2115** — 3 cents *below* the entry — and price
first touched that at 09-02 13:40, sixteen hours in. See §3f for what that pays.

## 3c. 🔴 DID THE BREAKEVEN LOCK APPLY? — **NO, and it is NOT a mechanical defect**

The operator's framing was: *if the lock applied and it still stopped out at 101.87, that is a
mechanical defect outranking everything.* **It did not apply, so it is not.** Three independent
sources, none of them intent:

**(1) The ledger.** `mgmt_state_json = {"breakeven_applied": false, …}`. `sl_price` (101.86) ==
`original_sl_price` (101.86). No divergence, ever.

**(2) 🆕 The venue's own order history** (private GET `/v5/order/history`, read-only — this is
the evidence the first pass could not obtain):

```
created 09-01 21:40:16  ->  updated 09-03 13:42:02
Market Buy qty=1  triggerPrice=101.86  stopOrderType=StopLoss  reduceOnly=True
orderStatus=Filled  avgPrice=101.87
--- and one entry order, Market Sell qty=1, filled 09-01 21:40:15 @ 99.24 ---
```

🔴 **Exactly ONE stop order exists on the venue for the whole 40-hour life of this position.
Its trigger was 101.86 from 21:40:16 until it filled. It was never amended.** No breakeven
modification was ever sent, because none was ever attempted.

**(3) The code path.** `virtual_trader.py:2119-2126`: the lock fires only inside
`if ENABLE_BREAKEVEN_LOCK and not be_applied:` on `crossed = last <= active_price`, where
`active_price` **is the same 97.2778 arm**. The lock's *park price* — 99.04152, i.e.
entry − 0.20 % (`trail_arm.py:_BE_TARGET_FRAC_ON = 0.0020`) — is where the stop would have
gone; it is not a trigger. And `virtual_trader.py:2224` gates the trail on `if be_applied`:
**the lock and the trail are one gate, and the gate is the 0.75 R arm.** It never evaluated
true, so the stop stayed at 101.86 and the position kept the full 1R of downside for 40 hours.

**Nothing here is broken. This is the mechanism working exactly as written, on a peak that
fell one cent short of switching it on.**

## 3d. Every exit-advisor consultation during the hold

`EXIT_ADVISOR_HOURLY = True`, `EXIT_ADVISOR_HOURLY_SEC = 3600` (config.py:918,923).
🔴 **`EXIT_ADVISOR_DRYRUN = True` (config.py:917) — "OBSERVE ONLY. No verdict reaches any close
path."** All 40 consultations below were structurally incapable of closing the position.

| # | timestamp (UTC) | upnl_r | verdict | reason (verbatim) |
|---|---|---|---|---|
| 1 | 09-01 21:40:29 | −0.00 | hold | Position at entry with no realized loss. Stop +1.00R away provides adequate protection. Trailing stop arms at +0.75R. Hold for signal or trend development. |
| 2 | 09-01 22:40:37 | −0.07 | hold | SHORT at -0.07R with +0.93R cushion to stop. Early stage (1h), peak barely tested (-0.00R MFE). Hold for trailing stop arm trigger at +0.75R. |
| 3 | 09-01 23:40:41 | −0.31 | hold | SHORT only -0.31R unrealized loss after 2h. Stop 0.69R away provides adequate protection. Trailing stop will arm at +0.75R. No signal to close; hold with discipline. |
| 4 | 09-02 00:40:52 | −0.13 | hold | SHORT only -0.13R unrealised, stop 0.87R away provides cushion. Peak was near-breakeven (MFE -0.00R), no established trend yet. Trailing stop armature at +0.75R still active objective. Hold. |
| 5 | 09-02 01:41:37 | +0.04 | hold | Position +0.04R with 1.04R downside buffer. Trailing stop not yet armed at +0.75R threshold. Early stage (4h); holds structure. HOLD. |
| 6 | 09-02 02:41:42 | −0.15 | hold | SHORT -0.15R underwater but peaked +0.29R. Trail unarmed at +0.75R threshold. Stop at +0.85R provides adequate protection. Hold for potential mean-revert or trail activation. |
| 7 | 09-02 03:41:47 | −0.41 | **close** | Position down 0.41R with 0.69R giveback from +0.29R peak. Trailing stop not armed yet. Stop 0.59R away offers insufficient margin for mean reversion in weak short setup. |
| 8 | 09-02 04:41:49 | −0.31 | hold | Short is -0.31R unrealised but peaked +0.29R; only 0.59R giveback from MFE. Stop at +0.69R provides adequate protection. Trail arms at +0.75R—close to current MFE. Hold for mean reversion. |
| 9 | 09-02 05:41:49 | −0.37 | hold | SHORT -0.37R unrealised loss; peaked +0.29R but gave back 0.65R. Stop at +0.63R provides buffer. Trail arms at +0.75R—position still has room to recover toward that threshold. Hold. |
| 10 | 09-02 06:41:56 | −0.32 | hold | SHORT at -0.32R with +0.68R cushion to stop. Peak +0.29R shows upside tested but not decisively broken. 9h elapsed, no signal. Hold for trail arm at +0.75R. |
| 11 | 09-02 07:41:57 | −0.30 | **close** | Short underwater -0.30R after 10h with 0.59R giveback from +0.29R peak. No trailing stop protection yet (arms at +0.75R). Risk/reward unfavorable; hold only if strong directional conviction remains. |
| 12 | 09-02 08:42:08 | **+0.08** | hold | SHORT +0.08R with +1.08R stop buffer. Peak +0.29R shows strength; 20bps giveback is minor. Trail arms at +0.75R. Hold for target; stops protect downside. |
| 13 | 09-02 09:42:19 | **+0.26** | hold | SHORT +0.26R, only 0.03R giveback from +0.29R peak. Trail arms at +0.75R; stop 1.26R away. Hold for target. |
| 14 | 09-02 10:42:24 | **+0.50** | hold | Position +0.50R with +1.50R stop buffer. Minimal 0.03R giveback from 0.53R peak shows strong trend control. Trailing stop arms at +0.75R—only 0.25R away. Hold for target. |
| 15 | 09-02 11:42:33 | **+0.46** | hold | Short +0.46R with +1.46R stop buffer. Peak +0.73R only 0.27R giveback suggests healthy momentum. Trail arms at +0.75R—very close. Hold for trail activation. |
| 16 | 09-02 12:42:34 | — | hold | `anthropic error: OverloadedError: 529 overloaded_error` — **the consult at the hour the peak was still fresh failed and defaulted to hold** |
| 17 | 09-02 13:42:53 | **+0.19** | hold | Position at +0.19R with peak +0.73R; 0.53R giveback acceptable given 16h horizon. Trailing stop arms at +0.75R—close to peak. Hold for mean reversion upside. |
| 18 | 09-02 14:42:54 | **+0.02** | **close** | Short at +0.02R with 0.70R giveback from +0.73R peak. 17h elapsed, trailing stop not armed. Risk-reward poor; high drawdown from MFE suggests momentum shift. Close to lock edge. |
| 19 | 09-02 15:43:01 | −0.05 | hold | SHORT is -0.05R unrealized but peaked +0.73R; only 0.77R giveback with 0.95R cushion to stop. Trail arms at +0.75R (0.02R away). Hold for trailing activation. |
| 20 | 09-02 16:43:12 | +0.10 | **close** | Position in drawdown from peak (+0.73R to +0.10R = 0.63R giveback, 86% retracement). Trailing stop not yet armed. Risk-reward unfavorable; hold exposes to further erosion without activated protection. |
| 21 | 09-02 17:43:16 | **+0.18** | hold | Short +0.18R, peaked +0.73R with 0.54R giveback. Trail arms at +0.75R—very close. Hold for trail activation; stop 1.18R away provides cushion. |
| 22 | 09-02 18:43:26 | 0.00 | **close** | Position at breakeven after 21h, peak +0.73R now fully given back. Trailing stop not armed; only static stop +1.0R away. Risk/reward unfavorable; hold offers diminishing edge. |
| 23 | 09-02 19:43:35 | −0.02 | hold | Short underwater only -0.02R after 22h. Peaked +0.73R, now 0.74R giveaway—normal pullback. Stop 0.98R away provides adequate protection. Hold for recovery. |
| 24 | 09-02 20:43:36 | −0.09 | hold | SHORT still -0.09R unrealised after 23h. Peaked +0.73R but gave back 0.82R—normal mean reversion. Stop at +0.91R provides cushion. Trailing stop arms soon at +0.75R. Hold for recovery or trail trigger |
| 25 | 09-02 21:43:37 | −0.18 | **close** | Short underwater -0.18R after 24h. Peak was +0.73R but gave back 0.90R, suggesting weakness. No trailing stop yet armed. Risk/reward unfavorable; close to lock learning. |
| 26 | 09-02 22:43:49 | −0.17 | **close** | Position underwater -0.17R after 25h with deteriorating setup. Peak MFE +0.73R now down 0.90R giveback indicates momentum reversed. Trail not armed; naked to gap risk. Risk/reward unfavorable. |
| 27 | 09-02 23:44:00 | −0.22 | **close** | Position is -0.22R underwater after 26h with deteriorating technicals. Peak MFE of +0.73R now down 0.94R giveback suggests momentum has reversed. Risk/reward unfavorable; trailing stop won't arm. |
| 28 | 09-03 00:44:02 | −0.17 | **close** | Position underwater -0.17R after 27h with -0.89R giveback from +0.73R peak. Trailing stop not yet armed; risk/reward deteriorating as price moves against short. |
| 29 | 09-03 01:44:13 | −0.37 | **close** | Short -0.37R underwater after 28h; peaked +0.73R then gave back 1.10R (150% of gain). Stop too far (+0.63R). Risk/reward unfavorable. |
| 30 | 09-03 02:44:28 | −0.55 | **close** | SHORT down 0.55R with 1.27R giveback from +0.73R peak. 29h elapsed, trailing stop still unarmed. Risk/reward deteriorating; hold only if conviction remains strong. |
| 31 | 09-03 03:44:31 | −0.42 | **close** | Short underwater -0.42R after 30h. Peaked at +0.73R but given back 1.14R (156% of gain). Trail not armed yet. Holding adds risk without fresh conviction. |
| 32 | 09-03 04:44:39 | −0.30 | **close** | Position at -0.30R with 1.03R giveback from +0.73R peak. Trailing stop not yet armed; 31h elapsed with deteriorating structure suggests holding for marginal +0.75R trail arm is unfavorable risk/reward |
| 33 | 09-03 05:44:48 | −0.42 | **close** | Short underwater -0.42R after 32h; peaked +0.73R but given back 1.15R (157% of peak gain). Stop 0.58R away leaves poor risk/reward. No trailing protection yet. |
| 34 | 09-03 06:44:49 | −0.65 | **close** | Short at -0.65R with 1.37R giveback from +0.73R peak. 33h elapsed, no trail armed yet. Risk/reward deteriorated; holding exposes full 1R stop for marginal upside potential. |
| 35 | 09-03 07:44:58 | −0.58 | **close** | Short underwater -0.58R after 34h. Peaked +0.73R but surrendered 1.30R (178% of gain). Risk/reward deteriorating; stop only +0.42R away. Hold exposes to shrinking buffer. |
| 36 | 09-03 08:44:59 | −0.54 | **close** | Short at -0.54R unrealised loss with 1.26R giveback from +0.73R peak. Position deteriorating after 35h. Risk/reward unfavourable; hold risks further drift without trailing stop protection. |
| 37 | 09-03 09:45:06 | −0.40 | **close** | Position underwater -0.40R after 36h. Peak of +0.73R gave back 1.13R; risk/reward deteriorating. Trailing stop won't arm; only static stop at +0.60R protects. Close to cut losses. |
| 38 | 09-03 10:45:18 | −0.25 | **close** | Short underwater -0.25R after 37h with 0.98R giveback from +0.73R peak. Risk/reward unfavorable; trailing stop not yet armed leaves only fixed protection. Exit to preserve capital. |
| 39 | 09-03 11:45:23 | −0.63 | **close** | Short underwater -0.63R after 38h with 1.35R giveback from +0.73R peak. Risk/reward unfavorable; trailing stop not armed yet. Cut loss. |
| 40 | 09-03 12:45:36 | −0.66 | **close** | Short underwater -0.66R after 39h with 1.39R giveback from +0.73R peak. Risk/reward unfavorable; trailing stop won't arm. Close to cut losses. |

**Tally: 40 consultations · 21 HOLD · 19 CLOSE · 1 API failure (defaulted to hold).**
The last **sixteen consecutive** verdicts from 09-02 21:43 to 09-03 12:45 were **CLOSE**. Not
one of them could act.

### Checking a profit-time HOLD against its own prompt — #14, the closest call

Its prompt, verbatim:

```
OPEN POSITION — decide CLOSE or HOLD.

Position
  Side: SHORT   Entry: 99.24   Now: 97.93
  Unrealised: +0.50R   (1R = the ORIGINAL stop distance, 2.6200)
  Elapsed: 13.0h
  Current stop: 101.86  ->  +1.50R away
  Peak so far (MFE): +0.53R   Giveback from peak: 0.03R

Trail
  The trailing stop is NOT ARMED — it arms only at +0.75R, which this
  position has not reached, so the stop above is the only protection.
  It would arm at 97.2750 (+0.75R).

Partial
  None taken; 1.0 open.
```

Its answer: *"Position +0.50R with +1.50R stop buffer. Minimal 0.03R giveback from 0.53R peak
shows strong trend control. Trailing stop arms at +0.75R—only 0.25R away. Hold for target."*

**Every checkable claim is correct:** +0.50R ✅, +1.50R to stop ✅, 0.03R giveback ✅, 0.53R
peak ✅, arm at +0.75R with 0.25R to go ✅. Unlike the entry advisor, the exit advisor
**invented nothing.** Its arithmetic was faultless and its reasoning was reasonable — it held
a position 0.25R from arming its own protection, in a trend that had just made a new low.
**It was right on the facts and wrong on the outcome, and it could not have acted either way.**

Note what the prompt tells it and what it does *not*: it is told *"the bot's on-exchange stop
and its trailing stop still protect the downside if you hold"*, while the very next block says
the trail is NOT armed. The advisor is being told it has two protections and one protection in
the same prompt.

## 3e. Was any exit signal received during the hold?

**Yes — one, and it expired unused with the confirmation arriving on the wrong channel and
then three hours too late.** The mechanism (`main.py:5667-5736, 5911-5962`;
`state_machine.py:29`): a 1h `Exit Signal` **arms** the open side for
`EXIT_PENDING_TTL_MINUTES = 360`; the close then fires only when a directional
BOS/CHOCH/Liquidity-Grab in the **opposite** direction arrives on
`EXIT_CONFIRM_TF = '15m'` (config.py:665).

| time (UTC) | event | status | note |
|---|---|---|---|
| 09-02 03:30:06 | 15m `Bullish I-CHOCH` (LONG) | `exit_unarmed_noop` | would have closed the short — **24 h before anything armed** |
| 09-02 08:45 / 10:45 | 15m Bearish I-CHOCH+ / S-BOS | `exit_unarmed_noop` | wrong direction for a short exit |
| 09-03 00:00:11 | 15m `Bullish I-CHOCH+` (LONG) | `exit_unarmed_noop` | qualifying — 4 h **before** the arm |
| 09-03 02:45:04 | 15m `Bullish I-BOS` (LONG) | `exit_unarmed_noop` | qualifying — 75 min **before** the arm |
| 09-03 03:00:04 | 15m `Bullish S-CHOCH` (LONG) | `exit_unarmed_noop` | qualifying — 60 min **before** the arm |
| **09-03 04:00:10** | **1h `Exit Signal`** | **`exit_armed`** | `EXIT_ARMED side=SHORT expires=2026-09-03T10:00:10Z` · position was ≈ −0.30 R |
| 04:25 · 05:00 · 05:25 · 07:05 · 07:50 · 08:55 | **six 5m bullish confirmations** (liq-grab ×3, I-CHOCH, I-CHOCH+, I-CHOCH) | `entry_suppressed_armed` | 🔴 `GUARD_A_SKIP_ENTRY … armed_side=SHORT — exit runs on 15m, counter-entry suppressed` |
| **09-03 10:00:10** | **arm expires, unused** | — | zero qualifying 15m signals inside the 6-hour window |
| 09-03 10:15:00 | 15m Bearish I-CHOCH+ | `exit_unarmed_noop` | wrong direction |
| **09-03 13:00:11** | **15m `Bullish I-CHOCH` (LONG)** | `exit_unarmed_noop` | 🔴 **exactly the confirmation the armed short needed — 3 h 00 m after the arm lapsed** |
| 09-03 13:00:12 | 1h `Smart Trail Switch Bullish` | `trend_set` | the 1h context flipped LONG |
| 09-03 13:42:02 | stop filled 101.87 | — | 42 minutes later |

🔴 **The armed window was six hours long and contained not one qualifying 15m signal — while
containing six qualifying 5m ones, each of which the code explicitly discarded with the words
"exit runs on 15m".** Three qualifying 15m confirmations arrived in the four hours *before*
the arm; a fourth arrived three hours *after* it lapsed and forty-two minutes before the stop.
The exit machinery was armed for precisely the interval in which its trigger did not appear.

This is not a bug — every line behaved as written. It is a **channel-and-window mismatch**: the
arm is granted on the 1h clock, the confirmation is only accepted on the 15m clock, and the 5m
stream that was carrying the same information the whole time is defined out of the conversation.

**Two further would-close mechanisms fired, both in DRYRUN:**
- 09-02 13:42:51 — `[SMART-EXIT-DRYRUN] would-exit … @~98.7400 … peakMFE=1.91% giveback=1.41%
  (arm=1.2/gb=0.8) — DRYRUN, position untouched`. Its reference arm (1.2 % MFE) *had* been
  cleared; its giveback threshold (0.8 %) had been breached. **It would have closed in profit.**
- 09-02 15:00:13-18 — `TREND-REVERSAL [OBSERVE]: Trend Catcher Up … would-close open SHORT
  vpos=42 — observe only` and two `[CONFIRM] … would close … dryrun=True`
  (`TREND_REVERSAL_EXIT_DRYRUN = True`, config.py:1145). It would have closed at ≈ −0.13 R.

## 3f. 🔴 THE COUNTERFACTUALS

Taker 0.100 % both legs, funding −$0.007012 charged in full (it is immaterial at this size):

| close at | price | gross $ | gross R | fees $ | **net $** | **net R** | when reachable |
|---|---|---|---|---|---|---|---|
| 🆕 **MFE, true venue low** | **97.29** | +1.9500 | +0.744 | 0.1965 | **+$1.7465** | **+0.667 R** | 09-02 11:20 (13.7 h) |
| MFE, engine's water_mark | 97.34 | +1.9000 | +0.725 | 0.1966 | **+$1.6964** | **+0.647 R** | 09-02 11:26 |
| **the trail level** (had it armed, from the true low) | 99.2115 | +0.0285 | +0.011 | 0.1985 | **−$0.1769** | **−0.068 R** | 09-02 13:40 (16.0 h) |
| **the breakeven lock** (had it armed) | 99.0415 | +0.1985 | +0.076 | 0.1983 | **−$0.0068** | **−0.003 R** | 09-02 13:40 (16.0 h) |
| SMART-EXIT-DRYRUN would-exit | 98.74 | +0.5000 | +0.191 | 0.1980 | **+$0.2950** | **+0.113 R** | 09-02 13:42 |
| trend-reversal would-close | ≈99.37 | −0.1300 | −0.050 | 0.1986 | **−$0.3356** | −0.128 R | 09-02 15:00 |
| **ACTUAL — the stop** | **101.87** | −2.6300 | −1.004 | 0.2011 | **−$2.8381** | **−1.083 R** | 09-03 13:42 |

🔴 **Read the middle two rows carefully, because they are the answer to "why didn't the safety
net save it".** Even if the arm had triggered — even if the peak had gone one more cent — the
**breakeven lock would have banked −$0.0068 and the trail would have banked −$0.1769.** Both
are losses. `trail_arm.py` says so in its own comment: at the venue's real 0.100 % taker,
the 0.20 % BE target is *"a FEE WASH, not the small net WIN this module's docstring
promised"* (net −0.0002 % of notional).

**The only counterfactual that pays meaningfully is closing at or near the peak itself
(+$1.75), and no armed mechanism in this bot closes at a peak — every one of them is a
giveback mechanism that must first let the peak be surrendered.** The gap between +$1.75 and
−$2.84 is $4.59, and nothing in the current contract was ever going to capture more than a
fraction of it.

---

# 4. WHAT WOULD HAVE PREVENTED IT — descriptive only

## 4a. Every mechanism that could have closed this in profit, and why each did not fire

| # | mechanism | could it have closed in profit? | why it did not fire |
|---|---|---|---|
| 1 | **Trailing stop** | marginally — −0.068 R, a loss | **never armed.** MFE +0.7443 R vs arm 0.75 R — short by **0.0057 R / 1.2 ¢** |
| 2 | **Breakeven lock** | no — −0.003 R, a fee wash | same gate as #1 (`virtual_trader.py:2119`); `breakeven_applied: false`; venue shows one unamended stop |
| 3 | **Hourly exit advisor** | **YES** — CLOSE at #18 (+0.02 R) and #20 (+0.10 R) | `EXIT_ADVISOR_DRYRUN = True` (config.py:917) — **19 CLOSE verdicts, all structurally inert** |
| 4 | **Smart-exit giveback** | **YES** — +0.113 R at 98.74 | `SMART_EXIT_DRYRUN_ENABLED` is a *sampler*; the journal line ends *"DRYRUN, position untouched"* |
| 5 | **Trend-reversal exit** | no — ≈ −0.128 R | `TREND_REVERSAL_EXIT_DRYRUN = True` (config.py:1145) — logged `would-close`, observed only |
| 6 | **Armed 1h exit + 15m confirm** | no — armed at ≈ −0.30 R | armed 04:00:10, expired 10:00:10 with **zero** qualifying 15m signals inside; six qualifying **5m** ones suppressed inside it; the qualifying 15m arrived 13:00, 3 h late |
| 7 | **Partial at the arm** | n/a | `PARTIAL_AT_ARM_ENABLED` off since 2026-08-14 (monotone sweep, config.py:283-296) — and it hangs off the same unreached arm |
| 8 | **Post-entry recheck (T+10/60/300 s)** | no | all three tiers `verdict=OK … no negative deltas`; wall went 8.8 → 9.6 → 10.7 **in the short's favour**; `recheck_status = done` |

**Four of the five mechanisms that saw the position correctly were in DRYRUN. The one that was
live never armed, by one cent.**

## 4b. 🔴 The peak never reached the arm — and the card's figures reconciled

**Stated plainly: the peak reached 97.29, the arm was 97.2778. It fell short by $0.0122 — 0.0057 R.**

So: **it was never in the profit an armed mechanism could see.** But it *was* in profit the
operator could see, and the two must be reconciled rather than one dismissed:

- **Unrealised profit was real.** At the peak the position was **+$1.95 gross / +$1.75 net**,
  and the engine's own hourly consults recorded it — #14 at **+0.50 R**, #15 at **+0.46 R**,
  with a peak logged as +0.53 R and then +0.73 R (the advisor's peak field lags the true
  water_mark by one poll cycle; the true figure is **+0.7443 R**).
- **Nothing on the venue changed.** `/v5/order/history` shows one stop at 101.86 throughout;
  unrealised PnL never became realised anything until 13:42:02.
- **The card is correct and complete.** Gross −2.6300, fees −0.2011, funding −0.007012, net
  −2.8381, and the venue's `closedPnl` is **−2.83812167** — identical to the ledger's
  `net_pnl` to eight decimals.

There is **no discrepancy** between the card and the venue. The discrepancy the operator felt
is between **the profit that existed** (+$1.75 at its best) and **the profit the machinery was
built to notice** (it notices nothing below +0.75 R). Both statements are true at once:
*it was up $1.95 for three hours*, and *no mechanism in this bot was watching that.*

## 4c. What is broken, what is working as designed, what is unrankable at this n

**BROKEN — one thing, and it is not in the exit path.**
1. **The entry reason asserted a fact the prompt does not contain.** "1h rearm stale" — the
   tier was 102 min old against a 360-min window, the prompt's staleness marker was correctly
   withheld, and the prompt states in terms that stale tiers *vote in full*. 🆕 **And the same
   model, 25 minutes earlier at the same confidence, skipped this trade citing that exact
   tier** (row 23052). The only thing that changed was that the tier got older. That is not a
   different reading of new information; it is the opposite verdict on the same fact.

**BROKEN-ADJACENT — structural, and nobody's fault at runtime.**
2. **The cascade and the advisor were shown different 1H tiers at the same instant.** The gate
   read the matrix TREND category (`neo_cloud_switch_bear`, SHORT, agreeing); the advisor read
   the state-machine slot (`15m-rearm: Reversal Up`, LONG, opposing). Neither judge held the
   whole fact. ✏️ *This corrects the 15:52 file, which reported the cascade as having passed
   over disagreeing tiers.*
3. **The armed-exit channel mismatch.** A 6-hour arm granted on the 1h clock, a confirmation
   accepted only on the 15m clock, and six qualifying 5m confirmations discarded inside the
   window by design. The arm was live for exactly the interval that contained no trigger.

**WORKING AS DESIGNED — do not mistake any of these for faults.**
4. The **trail and breakeven lock**: the arm is 0.75 R, MFE was 0.7443 R, so neither ran. The
   code, the ledger and the venue's order history agree. **Not a mechanical defect.**
5. The **flat/ADX gate**: ADX(1h) 29.4 against a 20.0 floor, armed and correctly silent.
6. The **book gate**: armed (`BOOK_GATE_DRYRUN = False`), evaluated, admitted — the thickest
   opposing wall was p55, ordinary by the prompt's own calibration.
7. The **post-entry recheck**: all three tiers OK, deltas favourable.
8. **Every DRYRUN flag** (#3–#5 in §4a) is doing exactly what the operator set it to do.
   config.py:906 is explicit: *"DRYRUN IS True AND MUST STAY True UNTIL THE BOSS DECIDES
   OTHERWISE."* **That 19 CLOSE verdicts went unheard is a policy in force, not a malfunction.**
9. The **exit advisor's own arithmetic**: checked against its prompt at the closest call and
   found faultless. It invented nothing.

**UNRANKABLE AT THIS n — say the number, then stop.**
10. **The short side: 6 positions, 0 winners, ΣR −4.589.** Six same-signed outcomes cannot
    separate "no edge" from "a bad run in a book whose per-trade mean is already negative".
11. **The 0.75 R arm.** This position argues it is 0.006 R too high. That is one observation,
    and config.py:196-213 records that the sweep's better cell (0.50 R) was **refused on
    purpose** as a fence built around four trades. One more near-miss is not evidence against
    a threshold; it is exactly the observation a fitted threshold would generate.
12. **The exit advisor's CLOSE record.** 19 CLOSE verdicts on one position, of which two
    (#18 at +0.02 R, #20 at +0.10 R) would have banked a small profit and seventeen would have
    cut the loss. n = 1 position. It cannot be scored.
13. **The armed-exit window.** One arm, one expiry, one late confirmation. n = 1.

**No change is proposed in this report.**

---

# CONTROLS

| control | evidence |
|---|---|
| Titan pre-flight | `tools/openitems_guard.py` → **exit 0**, 11 watched values agree, HEAD f5d3542. Nothing else on Titan touched. |
| **DB read-only** | every connection `sqlite3.connect('file:…/trades.db?mode=ro', uri=True)`; SELECT only; **zero** INSERT/UPDATE/DELETE/PRAGMA issued |
| **cwd outside SOL's tree** | all work in `/tmp/claude-0/…/scratchpad` and `/root`; no shell ever `cd`-ed into `/mnt/volume_nyc1_1780480650620/mercury-sol` |
| **config not imported** | `config.py`, `trail_arm.py`, `virtual_trader.py`, `main.py`, `state_machine.py`, `signal_matrix.py`, `indicators.py` read as **text** via `sed`/`grep`, cited by line. The only Python import of a config in this session was Titan's own guard reading **Titan's** config, as mandated. |
| **no writes attempted** | no file under the SOL tree opened for writing; no `sudo`, no `chmod`, no editor |
| **no orders placed or cancelled** | venue calls were **GET only**: `/v5/market/kline` (public), `/v5/position/closed-pnl`, `/v5/order/history`. No POST to any endpoint. |
| **service untouched** | no `systemctl` verb other than `show`; PID **1196924** unchanged, up since 2026-08-24 13:29:27 UTC |
| **`NRestarts` unchanged** | **0** before, **0** after |
| **file hashes identical** | all **33** `*.py` in the SOL tree md5-identical before and after (`config.py ed7a14b0…`, `claude_advisor.py a02ce04e…`, `adaptive_trail.py 69fb9754…`) |
| ⚠️ **`trades.db` hash changed — and it must** | `66a4308c…` → `7c7528c0…`. **The live bot wrote it, not this session.** PID 1196924 has held `fd 4 -> trades.db` since 2026-08-24; rows **23628–23633** (`open_short / htf_blocked`) were written at 16:10–16:30 UTC while this session ran. A byte-identical live DB would have meant the bot had **stopped**. All of this session's handles were `mode=ro`, which cannot write. |
| open positions now | **0** |

---

**Bottom line.** It did not override the daily regime — the daily was neutral and the 4h agreed;
the standing order stands at 2,121 obeyed of 2,127 and this is not the seventh. It entered on a
genuinely trending board, and the one fact against it was dismissed with a claim its own prompt
contradicts — a claim the same model had rejected 25 minutes earlier. It then sat 40 hours
because its peak of **+0.7443 R fell 1.2 cents short of the 0.75 R arm**, so the trail and the
breakeven lock never came into existence — established from the ledger, the code, and the
venue's single unamended stop order. **No mechanical defect.** Meanwhile four separate exit
mechanisms saw it correctly and were all in DRYRUN by standing policy, and the one armed exit
path was live for exactly the six hours its trigger did not appear. The live short book is now
**six positions, zero winners, ΣR −4.589** — a fact worth stating and, at n = 6, not yet a
fact worth ranking.
