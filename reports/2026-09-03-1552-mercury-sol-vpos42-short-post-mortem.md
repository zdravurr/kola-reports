# mercury-sol-vpos42-short-post-mortem

_2026-09-03 15:52 UTC_

---

# POST-MORTEM — LIVE SHORT vpos 42, SOL/USDT:USDT, entry 99.24 → stop 101.87, net −$2.8381

**READ-ONLY session.** Mercury-SOL was not touched: DB opened `file:…?mode=ro` with SELECTs
only, `config.py` read as text (never imported), no venue private call, no order, no restart.
Controls at the foot of this file. Titan pre-flight `openitems_guard.py` → **exit 0, clean**.

---

## 0. IDENTIFICATION — the vpos id was read from the ledger, not assumed

`virtual_positions.id = 42`, `is_paper = 0` (LIVE). Identified by matching the card's net
to the ledger to 7 decimals, not by recency.

| field | value |
|---|---|
| vpos id | **42** |
| entry trades row | 23053 |
| venue order id | `85ca0a10-89c6-4693-a946-7124fb81361e` |
| symbol / side | SOL/USDT:USDT · SHORT · sell |
| size / margin / leverage | 1.0 · 20.0 USDT · 5× |
| opened | 2026-09-01T21:40:18.343321+00:00 |
| closed | 2026-09-03T13:42:12.484258+00:00 |
| hold | **40 h 01 m 54 s** |
| entry fill | 99.24 |
| close | 101.87 · `close_reason = 'sl'` |
| ATR(1h) at entry | 1.04651359001191 |
| original_sl / sl at close | 101.86 / 101.86 — **never moved** |
| 1R (`initial_risk_usdt`) | **2.6200** |
| gross / fees / funding / net | −2.6300 / 0.20111 / 0.00701167 / **−2.83812167** |
| net in R | **−1.0833 R** |
| water_mark (best price seen) | **97.34** |
| max_adverse_price | 101.82 |
| `entry_adx_1h` / window | 29.416956796965152 / 200 |
| `entry_wall_baseline_mult` | 8.8 |
| `mgmt_state_json` | `{"breakeven_applied": false, "exit_advisor_last_ts": 1788439534.901061}` |

Card and ledger agree exactly (gross −2.6300, fees −0.2011, funding −0.007012, net −2.8381,
cumulative LIVE book 14 closed +$15.5574 — all reproduced below).

---

# 1. WHY DID IT ENTER?

## 1a. Tiers, weights, score arithmetic, cascade verdict

**The cascade tiers** (`combo_key = '1H:15m-rearm: Reversal Up|15M:HyperWave Signal Down|5M:Bearish New Imbalance'`):

| slot | signal | direction | age at entry | note |
|---|---|---|---|---|
| 1H | `15m-rearm: Reversal Up` | **LONG** | 1.7 h | **OPPOSES the short** |
| 15m | `HyperWave Signal Down` | SHORT | 25 m | `hw_15m_weight = 1.05`, subtype `HW_SIGNAL_SHORT` |
| 5m trigger | `Bearish New Imbalance` | SHORT | 0 m | the trigger |

**The matrix signals** — a *different* set from the cascade tiers, and this is worth naming:
the score is not computed from the three slots above.

| category | canonical id | signal | dir | age (min) | intensity weight | points |
|---|---|---|---|---|---|---|
| TREND | `neo_cloud_switch_bear` | Neo Cloud Switch Bearish | SHORT | 159.96 | 0.9 | **2.25** |
| MOMENTUM | `hw_signal_down` | HyperWave Signal Down | SHORT | 25.00 | 0.7 | **1.75** |
| LIQUIDITY | `imb_new_bear` | Bearish New Imbalance | SHORT | 0.0004 | 0.7 | **1.75** |
| EXECUTION | — | — | NEUTRAL | — | — | 0.00 |

No intra- or inter-category conflict on any of the four.

**Score arithmetic**

```
raw matrix score          5.75  SHORT     (2.25 + 1.75 + 1.75 + 0.00)
matrix direction threshold 4.00            -> PASSED  (trade_signal_matrix.threshold)

macro_gate_penalty        0.00             (macro_news_category NEUTRAL, macro_confidence 0.72,
                                            dxy_trend UPTREND, news MIXED score +0.15 impact low)
weighted_adj             +0.3708           (weight_engine, storage-only, clipped ±1.5)
gated confluence_score    6.12   = 5.75 + 0.3708
CONFLUENCE_SCORE_THRESHOLD 2.00            (config.py:670)  -> PASSED
```

Two thresholds, both cleared with room: 5.75 vs 4.00, and 6.12 vs 2.00. `config.py:670` is
explicit that at 2.0 *"the AI consult is the real entry filter"* — the score gate is not
where this trade was decided.

**Cascade verdict.** 3-way confluence fired (1H / 15m / 5m slots all filled), cascade passed,
score gate passed, risk gate passed. The prompt states this plainly and correctly warns that
it is *not* a statement that the tiers agree with each other — they did not: 2 agree, 1 opposes.

## 1b. 🔴 `trend_1d` and `trend_4h` at entry — THIS IS NOT AN OVERRIDE

```
trend_1d = 'neutral'   ADX(1d) 49.543   EMA-gap 7.193 % (Contracting)   ema_status_1d = Bullish
trend_4h = 'bear'      ADX(4h) 18.770   EMA-gap 0.885 % (Expanding)     ema_status_4h = Bearish
trend_1h = 'bear'      ADX(1h) 29.417   EMA-gap 0.974 % (Expanding)
trend_15m= 'bear'      ADX(15m)53.218   EMA-gap 0.439 % (Expanding)
mtf_alignment_score = 4
```

**Stated plainly: the daily regime did NOT oppose this short.** It was NEUTRAL, and the 4h
AGREED with the short. The standing order established on 2026-09-01 — lean toward `skip` when
1d/4h clearly oppose — never engaged, because nothing opposed.

**This is not the seventh override.** The 2026-09-01 figures reproduce exactly when cut at the
moment of this entry (`timestamp < '2026-09-01 21:40:00'`), with "opposed" = the 1d **or** the
4h pointing against the proposed direction:

```
opposed population   n = 2,127      execute = 6      skip = 2,121      obeyed 99.72 %
```

Under the stricter definition (1d alone opposing): n = 1,321, execute = 6, skip = 1,315. The
override count is **6 under either ruler** — it is a robust number. This trade is in neither
population.

The six overrides, for the record:

| trades id | date | dir | trend_1d | trend_4h | ADX(1d) | outcome |
|---|---|---|---|---|---|---|
| 4259 | 2026-06-24 | LONG | bear | bear | 26.49 | — |
| 11180 | 2026-07-19 | LONG | bear | neutral | 14.72 | — |
| 11181 | 2026-07-19 | LONG | bear | neutral | 14.72 | — |
| 15093 | 2026-08-02 | LONG | bear | neutral | 13.46 | — |
| **17289** | 2026-08-10 | **SHORT** | **bull** | neutral | 12.59 | **vpos 32, −0.180 R** |
| **18111** | 2026-08-13 | **SHORT** | **bull** | bear | 10.94 | **vpos 34, −0.643 R** |

Both live SHORT overrides lost, as the operator stated. vpos 42 is not among them.

**One nuance worth naming, and it is a labelling question, not an override.** `ema_status_1d`
was **Bullish** with ADX(1d) **49.5** — by the EMA/ADX reading the daily was in a strong
uptrend. The label the prompt rendered was `NEUTRAL` because the 1d EMA-gap was *Contracting*.
So the standing order keys on a label that said neutral while the underlying daily reading was
the most trend-y number on the whole board. That is worth knowing; it is not an override, and
this report proposes nothing about it.

## 1c. 🔴 THE ADVISOR'S VERBATIM PROMPT AND REASON

Model: `claude-haiku-4-5-20251001`. Decision `execute`, confidence 0.78.

### SYSTEM PROMPT (verbatim, untruncated)

```
You are an automated trading decision module for a SOL/USDT perpetual swing bot. You receive multi-timeframe LuxAlgo signal context (1H trend, 15m confirmation, 5m trigger) at the moment 3-way confluence has just fired and the bot is about to place a single market entry. You also receive real-time market context: a Volatility/regime block (ADX on 1h/15m, ATR% of price, EMA-gap compression, market_regime, MTF alignment) plus volume ratio, and pre-trade order-book walls.

You also receive a 'Higher Timeframes Trend' block: an OHLCV-derived (EMA/ADX) trend label, ADX, and EMA-gap for 1d/4h/1h/15m/5m, independent of the LuxAlgo signals. Treat the 1d and 4h trends as the dominant regime: when they clearly oppose the proposed entry direction, lean toward 'skip' unless the lower-TF confluence is exceptionally strong; when 1d/4h agree with the entry, that is supportive context.

Your job is to gate that entry: vote 'execute' when the context looks coherent, 'skip' when it looks like a chop/false break or contradicts the higher-timeframe regime.

HARD RULE — opposing walls: if a massive limit wall (volume marked with a multiplier, e.g. ×8.3) sits directly above a LONG entry or directly below a SHORT entry, you MUST reply 'skip'. A thick wall in the opposing direction represents strong resting liquidity that will absorb the move before it can develop.

SOFT RULE — FLAT-MARKET GUARD: read the multi-TF Volatility/regime block. Treat the market as flat/squeezed when 1h ADX is low (~<20-23) AND ATR% is low on 1h/15m AND the EMA-gap is Contracting/Flat (and/or market_regime is FLAT with weak MTF alignment). In a flat market, prefer 'skip' UNLESS the LuxAlgo confluence is exceptionally strong (clear multi-TF agreement). Conversely, do NOT skip a genuine trend (rising/high ADX, Expanding EMA-gap, market_regime=TREND) merely because absolute ATR looks small in a low-volatility era. Weigh these factors together — this is soft, multi-factor judgment, not a hard numeric gate; strong confluence can override.

Respond with ONLY a single JSON object, no markdown, no prose. Fields: decide ("execute"|"skip"), confidence (float 0.0-1.0), reason (string, max 80 chars).
```

### USER PROMPT (verbatim, untruncated)

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

### RAW RESPONSE (verbatim)

```json
{
  "decide": "execute",
  "confidence": 0.78,
  "reason": "4/4 MTF bear alignment (4h-5m), 15m/5m SHORT agree, strong ADX+trend. 1h rearm stale."
}
```

### Every checkable numeric claim, checked against the prompt it was given

| # | claim | verdict |
|---|---|---|
| 1 | "4/4 MTF bear alignment (4h-5m)" | ✅ **TRUE** — prompt: *"MTF alignment vs SHORT: 4/4 (4H/1H/15m/5m; excludes 1d)"*. Correct, including the parenthetical range. |
| 2 | "15m/5m SHORT agree" | ✅ **TRUE** — the tier-agreement block says exactly that: 15m AGREES, 5m AGREES. |
| 3 | "strong ADX+trend" | ✅ **TRUE but incomplete** — 1h 29.4 and 15m 53.2 are strong, `market_regime: TREND` is stated, both EMA-gaps Expanding. However the 4h leg of the "4/4 alignment" it leans on carries **ADX 18.8**, inside the system prompt's own *"~<20-23 = weak/ranging"* band. The one weak leg is one of the four it counted. Not a false claim; an omission. |
| 4 | **"1h rearm stale"** | ❌ **NOT SUPPORTED BY THE PROMPT.** The word *stale* appears nowhere as a verdict about this tier. The prompt gives an age — *"set 1.7h ago"* — and a counting rule that says the opposite of what the model concluded: **"AS COUNTED (stale tiers vote in full): 2 agree, 1 oppose"**. The model invented a disqualification for the **only tier that opposed the trade**. This is the single defect in the reason. |
| 5 | the order book | **not mentioned at all** — see 1d. |

## 1d. The order book as rendered

Two books were captured at entry. They are different books and both matter.

**(i) The book the advisor saw** (`advisor_book_json`, OKX depth 8000, wall threshold >4× avg vol,
mid 99.25, imbalance ±1 % = **0.5333** bid share):

| side | price | mult | percentile (all-walls ruler, n=23,080) | role vs a SHORT |
|---|---|---|---|---|
| bid | **99.25** | **×8.8** | **p55** | opposing (at mid) |
| bid | 98.75 | ×5.7 | p31 | opposing, 0.504 % below |
| bid | 98.25 | ×5.5 | p29 | opposing, 1.007 % below |
| bid | 96.25 | ×6.9 | p42 | opposing, 3.02 % below |
| bid | 95.25 | ×4.6 | p15 | opposing, 4.03 % below |
| ask | 99.25 | ×6.5 | p39 | supporting |
| ask | 99.75 | ×5.7 | p31 | supporting |
| ask | 106.25 | ×6.5 | p39 | supporting |
| ask | 107.25 | ×4.7 | p18 | supporting |
| ask | 107.75 | ×4.2 | p5 | supporting |
| ask | 120.25 | ×6.9 | p42 | in the JSON, **not rendered** into the prompt (5 shown) |

**(ii) The book it actually traded on** (`orderbook_json`, Bybit L2): mid 99.30, spread 0.01,
imbalance 0.4563, **one** bid wall at 99.18 (4,013.7), **zero** ask walls. Tape over the prior
60 s: 100 trades, buy $8,138.63 vs sell $37,546.69, `buy_share_window = 0.1781`, pressure
**sell**, no whales. The tape was strongly on the short's side at the moment of entry.

**The book gate** (`BOOK_GATE_ENABLED = True`, `BOOK_GATE_DRYRUN = False` — armed, refuses
entries) evaluated and **CLEARED** it. Stored facts: `book_gate_clause = ''` (empty = no clause
fired), `opp_mult = 5.7`, `opp_pctl = 5.0`, `opp_dist_pct = 0.5037783`, `lean = 0.4667`,
`n_supporting = 5`.

- **Clause A** (do not trade into a wall) needs `opp_pctl ≥ 90` **and** `opp_dist_pct ≤ 0.20`.
  Nearest opposing wall strictly below mid = 98.75 ×5.7 → on the SHORT-side nearest-opposing
  ruler that is **p5.0**, and it is **0.504 %** away. Both conditions fail. Clause A false.
- **Clause B** needs `n_supporting < 1` or `lean < 0.3489` (the SHORT floor). 5 supporting walls,
  lean 0.4667. Clause B false.

Two things about the gate's arithmetic that a reader should not trip over:

1. **Two different percentile rulers are in play, deliberately.** The prompt's `pN` is cut from
   *every rendered wall, both sides, all distances* (n = 23,080). The gate's `opp_pctl` is cut
   from *nearest-opposing walls on this side only* (3,454 signals, 2026-06-08 → 2026-08-10).
   The same ×5.7 wall reads **p31** on the prompt's ruler and **p5** on the gate's. `book_gate.py`
   explains why the second is the right one for a refusal rule and the first is not.
2. **The ×8.8 bid wall at 99.25 sits exactly AT mid**, and the gate's opposing test for a SHORT is
   `price < mid` — strictly below. So the thickest wall on the board was excluded from the gate's
   opposing set. It was not ignored elsewhere: it is stored as `entry_wall_baseline_mult = 8.8`
   and the post-entry rechecks tracked it at T+10 s / T+60 s / T+300 s (8.8 → 9.6 → 10.7, all
   `verdict=OK, no negative deltas`).

**Did the reason cite the book, and correctly?** **It did not cite the book at all.** Not one
word, despite a system prompt that carries a HARD RULE about opposing walls and a full
calibration paragraph telling it to judge by percentile. So nothing incorrect was said about the
book — because nothing was said. This is the documented behaviour: `book_gate.py`'s own docstring
records that the advisor cites the calibrated percentile in **6.6 %** of its reasons while its
prompt calls that figure primary, and that four of four checkable book claims it has made were
false, all in the same direction. That is precisely why the book rule lives in code, not in the
prompt — and here the code did the work.

## 1e. The flat/ADX gate

```
FLAT_ADX_GATE_ENABLED = True        (config.py:406)
FLAT_ADX_GATE_DRYRUN  = False       (config.py:407)  🔴 ARMED — this gate REFUSES ENTRIES
threshold             = ADX_BELOW_FLOOR = 20.0       (config.py:634; reused deliberately,
                                                      config.py:399-410 — one number, one definition)
```

**ADX(1h) at entry = 29.416956796965152**, window 200, `entry_atr_pct_1h = 1.0545 %`.

**29.42 > 20.0.** The gate did not have to be cleared by exception, a fallback, or a fail-open
path — it read **9.4 points above the floor** and admitted. There is no anomaly here to explain.
The same gate refused **10** other signals inside this very 40-hour window (`status =
'flat_adx_blocked'` × 10), so it was live and biting throughout.

The *soft* FLAT-MARKET GUARD in the advisor's system prompt had nothing to bite on either: EMA-gap
Expanding on both 1h and 15m, `market_regime = TREND`, MTF alignment 4. Every condition the guard
looks for pointed the other way.

---

# 2. 🔴 WAS IT RIGHT TO ENTER? — judged on what was knowable before the move

## 2a. Was this in the population the daily-regime instruction would refuse?

**No.** `trend_1d = neutral`, `trend_4h = bear` (agreeing). It is in neither the strict-1d
opposed population (n = 1,321) nor the 1d-or-4h one (n = 2,127 at the moment of entry, matching
the operator's figure exactly).

**It is NOT the seventh override.** The override count stands at **6**, with 1 winner and both
live SHORT overrides (vpos 32, vpos 34) losers. That record is unchanged by this trade, and the
headline the operator was braced for does not hold.

## 2b. 🔴 SOL's live short book — now six, and the running total

| vpos | opened | entry | close | reason | net $ | R |
|---|---|---|---|---|---|---|
| 32 | 2026-08-10 | 76.18 | 76.24 | exit_signal | −0.2663 | **−0.1797** |
| 34 | 2026-08-13 | 75.21 | 75.76 | sl | −0.9113 | **−0.6431** |
| 35 | 2026-08-14 | 75.16 | 75.57 | sl | −0.7289 | **−0.7009** |
| 36 | 2026-08-15 | 75.20 | 75.62 | exchange_market | −0.7278 | **−0.7566** |
| 37 | 2026-08-16 | 74.38 | 75.09 | sl | −1.1156 | **−1.2259** |
| **42** | 2026-09-01 | 99.24 | 101.87 | **sl** | **−2.8381** | **−1.0833** |
| | | | | **TOTAL** | **−$6.5880** | **−4.5894 R** |

**Stated plainly: SOL's live short side has NEVER produced a winner. Zero for six.** Not one
short has closed green — not by trail, not by exit signal, not by stop. Every single loss.

The contrast with the other side of the book is total:

```
LIVE LONGS   n = 8   winners 6   ΣR +10.7305   Σ$ +22.1454
LIVE SHORTS  n = 6   winners 0   ΣR  −4.5894   Σ$  −6.5880
LIVE BOOK    n = 14                             Σ$ +15.5574   ← matches the card exactly
```

Every dollar in the live book is long-side. The short side has been a straight −$6.59 tax on it.
All four winning **trail** exits in the book's history are longs (vpos 30, 38, 39, 40, 41).

## 2c. Judge the REASONING, not the outcome

**The entry was procedurally sound on everything checkable, with one real defect.**

Sound:
- 4/4 lower-timeframe bear alignment was genuinely present and correctly reported.
- ADX(1h) 29.4 in a `TREND` regime with expanding EMA-gaps on 1h/15m — this was not a
  flat-market entry, and both the hard gate (29.4 vs 20.0) and the soft guard agree.
- The order book was evaluated by the armed gate on the correct per-side ruler and was clear on
  both clauses. The gate was right not to refuse: p5 at 0.504 % is not a wall in the way.
- The tape at the moment of entry was 82.2 % sell-side by USDT.
- No standing order was violated: the daily regime did not oppose.

The defect:
- **The single opposing tier was disposed of with a word the prompt does not support.** The 1H
  slot held a LONG signal 1.7 h old. The prompt told the model "2 agree, 1 oppose" and told it
  explicitly that stale tiers *vote in full*. The model wrote "1h rearm stale" and moved on. It
  converted a 2-1 into a clean read by asserting a disqualification it was not given. The honest
  one-line summary of that board was: *the only higher-timeframe tier in the cascade points the
  other way.*

**That defect is not what lost the money.** The position went **0.725 R in its favour** before it
turned. A losing trade with mostly sound reasoning is a different problem from a bad decision,
and this is the former — with a small, specific, named reasoning fault attached that is worth
recording precisely because it is the kind that recurs invisibly.

**Where n cannot rank it.** At n = 6, all losers, SOL's live short side cannot be distinguished
from "the short side has no edge" and "six unlucky draws". −4.589 R over 6 positions is not
significant at any conventional level. But the descriptive statement stands and needs no
statistics: **six live shorts, six losses, no winner, and every entry mechanism in the bot passed
each of them.**

---

# 3. 🔴 WHY DID IT SIT SO LONG WHILE IN PROFIT?

## 3a. The full price path

> 🔴 **Source caveat, stated up front.** Bybit's public kline API returns **HTTP 403** to this
> host (both `api.bybit.com` and `api.bytick.com`), so the venue's own candles could not be
> pulled. The path below is reconstructed from two sources that *can* be read without touching
> the bot: **(i)** the bot's own **2,940 excursion samples** taken off Bybit ticks during the
> hold (`position_excursion_samples`, ~50 s cadence), and **(ii)** **488 OKX SOL-USDT-SWAP 5m
> candles** as an independent cross-check. They agree to 3 cents at the peak.

```
hold          2026-09-01 21:40:18Z  ->  2026-09-03 13:42:12Z   =  40 h 01 m 54 s
1R            2.6200 price units
entry         99.24        stop 101.86 (+1.000R)      arm 97.2750 (-0.750R)
```

**MFE — three independent measurements, all short of the arm:**

| source | best price | in R | in % of entry | when |
|---|---|---|---|---|
| Bybit `water_mark` (the ledger's own) | **97.34** | **+0.7252 R** | **1.9146 %** | 2026-09-02 ~11:2x |
| OKX 5m low | 97.31 | +0.7366 R | 1.9448 % | 2026-09-02 **11:20** |
| bot's excursion sampler minimum | 97.38 | +0.7099 R | 1.8742 % | 2026-09-02 11:26:57 |

**The peak occurred 13 h 46 m into a 40 h 02 m hold — at the 34 % mark.** The remaining
**26 h 16 m** were spent handing it back and then losing 1.08 R beyond.

**How much of the hold was actually spent in meaningful profit** (2,940 tick samples):

| threshold | price | samples | share of hold | window |
|---|---|---|---|---|
| ≥ +0.25 R | ≤ 98.5850 | 300 | 10.2 % | 09-02 01:50 → 17:32 |
| ≥ +0.50 R | ≤ 97.9300 | 91 | 3.1 % | 09-02 10:40 → 13:16 |
| ≥ +0.60 R | ≤ 97.6680 | 19 | 0.65 % | 09-02 10:49 → 12:59 |
| ≥ +0.70 R | ≤ 97.4060 | **1** | 0.03 % | 09-02 11:26:57 |
| **≥ +0.75 R (the arm)** | ≤ 97.2750 | **0** | **0 %** | **never** |

**Hourly path** (OKX 5m aggregated; `bestR` = best excursion that hour):

```
09-01 21:00  O 99.34 H 99.70 L 99.25 C 99.54  bestR -0.004
09-01 22:00  O 99.55 H 99.89 L 99.29 C 99.63  bestR -0.019
09-01 23:00  O 99.62 H100.19 L 99.55 C 99.91  bestR -0.118
09-02 00:00  O 99.92 H100.19 L 99.55 C 99.60  bestR -0.118
09-02 01:00  O 99.59 H 99.88 L 98.42 C 99.03  bestR +0.313
09-02 02:00  O 99.03 H 99.88 L 98.70 C 99.88  bestR +0.206
09-02 03:00  O 99.88 H100.65 L 99.78 C100.23  bestR -0.206
09-02 04:00  O100.24 H100.24 L 99.68 C100.04  bestR -0.168
09-02 05:00  O100.04 H100.37 L 99.70 C100.21  bestR -0.176
09-02 06:00  O100.22 H100.33 L 99.59 C100.01  bestR -0.134
09-02 07:00  O100.02 H100.38 L 99.74 C 99.78  bestR -0.191
09-02 08:00  O 99.77 H 99.97 L 98.71 C 98.95  bestR +0.202
09-02 09:00  O 98.95 H 99.27 L 98.09 C 98.58  bestR +0.439
09-02 10:00  O 98.57 H 98.62 L 97.37 C 98.18  bestR +0.714   <- 10:50 candle L 97.37
09-02 11:00  O 98.18 H 98.22 L 97.31 C 98.05  bestR +0.737   <- 🔴 11:20 candle L 97.31 = THE PEAK
09-02 12:00  O 98.05 H 98.43 L 97.53 C 97.63  bestR +0.653
09-02 13:00  O 97.64 H 99.61 L 97.63 C 99.15  bestR +0.615   <- the turn: +1.98 in one hour
09-02 14:00  O 99.15 H 99.75 L 98.82 C 98.87  bestR +0.160
09-02 15:00  O 98.87 H 99.46 L 98.37 C 99.26  bestR +0.332
09-02 16:00  O 99.25 H 99.76 L 98.70 C 98.73  bestR +0.206
09-02 17:00  O 98.74 H 99.27 L 98.14 C 99.25  bestR +0.420   <- last time it saw +0.42R
09-02 18:00  O 99.26 H 99.64 L 99.10 C 99.46  bestR +0.053
09-02 19:00  O 99.45 H 99.59 L 99.01 C 99.38  bestR +0.088
09-02 20:00  O 99.38 H 99.99 L 99.27 C 99.65  bestR -0.011
09-02 21:00  O 99.65 H 99.82 L 99.37 C 99.60  bestR -0.050
09-02 22:00  O 99.60 H 99.71 L 99.15 C 99.48  bestR +0.034
09-02 23:00  O 99.49 H100.48 L 99.37 C100.37  bestR -0.050
09-03 00:00  O100.38 H100.40 L 99.44 C 99.46  bestR -0.076
09-03 01:00  O 99.45 H100.57 L 99.09 C100.11  bestR +0.057   <- last time it was green at all
09-03 02:00  O100.10 H101.33 L 99.89 C101.07  bestR -0.248
09-03 03:00  O101.08 H101.14 L100.14 C100.47  bestR -0.344
09-03 04:00  O100.47 H100.96 L100.01 C100.93  bestR -0.294   <- EXIT ARMED 04:00:10
09-03 05:00  O100.94 H100.98 L 99.65 C100.81  bestR -0.156
09-03 06:00  O100.81 H100.93 L100.53 C100.84  bestR -0.492
09-03 07:00  O100.83 H101.33 L100.20 C100.35  bestR -0.366
09-03 08:00  O100.35 H101.09 L100.34 C100.58  bestR -0.420
09-03 09:00  O100.57 H100.75 L100.08 C100.12  bestR -0.321
09-03 10:00  O100.12 H100.44 L 99.87 C100.40  bestR -0.240   <- arm expired 10:00:10 unused
09-03 11:00  O100.39 H100.96 L100.27 C100.74  bestR -0.393
09-03 12:00  O100.73 H101.82 L100.57 C101.61  bestR -0.508
09-03 13:00  O101.61 H101.97 L101.01 C101.57  bestR -0.676   <- 13:40 candle H 101.97 takes the stop
```

The single 5m candle that made the peak: **09-02 11:20, O 97.83 H 97.84 L 97.31 C 97.49.** The
low held for one 5-minute bar and one adjacent bar (11:25, L 97.32). Everything after 12:00 on
09-02 is the give-back.

## 3b. 🔴 DID THE TRAIL EVER ARM? — NO

```
arm distance = TRAIL_ARM_R × SL_BUFFER_ATR × ATR(1h)          (trail_arm.activation_distance)
             = 0.75        × 2.5           × 1.04651359001191
             = 1.96221
arm price    = 99.24 − 1.96221 = 97.27500                     (config.py:231, config.py:62)
```

| quantity | value |
|---|---|
| **arm price** | **97.2750** |
| best price ever seen (Bybit `water_mark`) | **97.34** |
| **shortfall** | **0.0650 in price · 0.0248 R · 0.0655 % of entry** |
| shortfall on the OKX cross-check (97.31) | 0.0350 in price · 0.0134 R |
| tick samples at or below 97.2750 | **0 of 2,940** |
| 5m candles with a low at or below 97.2750 | **0 of 482** |
| `mgmt_state_json` arm/BE flag | `"breakeven_applied": false` — and no arm key at all |

**The trail never armed, and it therefore never sat anywhere.** It is gated behind the breakeven
flag in the poller (`virtual_trader.py:2224` — `if be_applied and trail_pct > 0:`), which was
never set. The stored `trail_pct = 1.975` was never read by a live comparison for 40 hours.

**And had it armed, at exactly the arm price, it would not have closed in profit either.** The
callback is `TRAIL_MULT_ATR × ATR(1h) = 1.875 × 1.04651 = 1.9622` in price — **0.749 R** given
back from the high-water mark. From a water mark of 97.2750 the trail sits at **99.2372**, three
cents *below* the entry. On a 0.725 R excursion the trail's own giveback is the entire excursion.

This is not a hidden flaw — it is arithmetic that follows directly from `TRAIL_MULT_ATR = 1.875`
against `SL_BUFFER_ATR = 2.5` (config.py:104, the P2 narrowing of 2026-08-06). It means that on
this trade **no armed trail existed that could have booked a profit**, only one that could have
booked approximately break-even.

## 3c. 🔴 DID THE BREAKEVEN LOCK APPLY? — NO, and it is NOT a mechanical defect

**The lock and the trail share ONE arming condition.** This is the crux and it needs saying
precisely, because the question as posed assumes two independent mechanisms:

```python
# virtual_trader.py:2122-2128
if ENABLE_BREAKEVEN_LOCK and not be_applied:
    crossed = ((position_side == 'LONG'  and last >= active_price) or
               (position_side == 'SHORT' and last <= active_price))
    if crossed:
        be_price = breakeven_target(fill, position_side)   # = 99.0415 here
        mgmt_state['breakeven_applied'] = True
        _exec_move_stop(row, be_price)
```

`active_price` is the **same 97.2750**. **99.0415 (= entry − 0.20 %) is where the lock PARKS the
stop once it fires — it is not the price at which it fires.** The lock arms at −0.75 R, not at
−0.20 %. Since 97.2750 was never touched, the lock never evaluated true, and the stop stayed at
101.86 for the whole hold.

**Established from three independent records, not from intent:**

1. **`mgmt_state_json`** — `{"breakeven_applied": false, "exit_advisor_last_ts": 1788439534.901061}`.
   Written by the poller itself; false for 40 hours.
2. **The ledger** — `sl_price` 101.86 **==** `original_sl_price` 101.86. The stop never moved.
3. **The venue's own stop history**, from `journalctl -u mercury-sol.service`:

```
Sep 01 21:40:16  [SL] position-level SL set on attempt 1: 101.87
Sep 01 21:40:16  [SL] PROVISIONAL stop set from pre-trade ticker 99.25 → 101.87
                      (route=fallback_atr) BEFORE reading the fill — position is protected
Sep 01 21:40:18  [SL] provisional 101.87 → EXACT 101.86 (fill 99.24)
Sep 01 21:40:18  [SL] route=fallback_atr sl=101.86 dist=2.640% wall=None (anchor_flag=OFF)
   … 40 hours. NO further [SL] line. No BE-LOCK line. No Breakeven card. No stop amend. …
Sep 03 13:42:12  [ENGINE] exchange close substantiated: 1.0 @ 101.87 fee=0.10187 reason=sl
                      — NOT closed by this process; classified from the venue
                        (stopOrderType='StopLoss')
```

**Verdict: the lock did not apply, and the exit at 101.87 is the ORIGINAL stop filling.** The
101.87-versus-101.86 gap is one cent of fill slippage on a market stop, not a stop parked in the
wrong place: the venue's resting stop was 101.86 from 21:40:18 onward, and 101.87 is where the
`StopLoss` order actually filled.

**So the mechanical defect the operator was watching for does not exist here.** Nothing moved a
stop to the wrong level; nothing armed and then failed; nothing lied about its state. What is at
issue is the *design* — one arming threshold gating everything — not its execution.

## 3d. 🔴 Every exit-advisor consultation during the hold

**40 consults**, hourly, one per open position. Model `claude-haiku-4-5-20251001`.

🔴 **`EXIT_ADVISOR_DRYRUN = True` (config.py:917) — "OBSERVE ONLY. No verdict reaches any close
path."** Every one of these 40 verdicts was computed, logged, persisted as a `trades` row with
`status='exit_ai_dryrun'`, and **discarded**. `consult_exit_advisor` is documented as having no
access to any close mechanic (main.py:3564-3571). This is deliberate: the config's own note says
an acting advisor would close positions the trail would otherwise have taken and would destroy
the sole live trail measurement that exists in this project.

**Verdict tally: 22 CLOSE · 17 HOLD · 1 error** (09-02 12:42, Anthropic 529 overloaded, recorded
as hold with confidence 0.0).

| # | timestamp (UTC) | upnl_r | giveback | verdict | verbatim reason |
|---|---|---|---|---|---|
| 1 | 09-01 21:40:29 | −0.00 R | 0.00 R | HOLD (0.95) | Position at entry with no realized loss. Stop +1.00R away provides adequate protection. Trailing stop arms at +0.75R. Hold for signal or trend development. |
| 2 | 09-01 22:40:37 | −0.07 R | 0.07 R | HOLD | SHORT at -0.07R with +0.93R cushion to stop. Early stage (1h), peak barely tested (-0.00R MFE). Hold for trailing stop arm trigger at +0.75R. |
| 3 | 09-01 23:40:41 | −0.31 R | 0.31 R | HOLD | SHORT only -0.31R unrealized loss after 2h. Stop 0.69R away provides adequate protection. Trailing stop will arm at +0.75R. No signal to close; hold with discipline. |
| 4 | 09-02 00:40:52 | −0.13 R | 0.13 R | HOLD | SHORT only -0.13R unrealised, stop 0.87R away provides cushion. Peak was near-breakeven (MFE -0.00R), no established trend yet. Trailing stop armature at +0.75R still active objective. Hold. |
| 5 | 09-02 01:41:37 | **+0.04 R** | 0.00 R | HOLD | Position +0.04R with 1.04R downside buffer. Trailing stop not yet armed at +0.75R threshold. Early stage (4h); holds structure. HOLD. |
| 6 | 09-02 02:41:43 | −0.15 R | 0.44 R | HOLD | SHORT -0.15R underwater but peaked +0.29R. Trail unarmed at +0.75R threshold. Stop at +0.85R provides adequate protection. Hold for potential mean-revert or trail activation. |
| 7 | 09-02 03:41:47 | −0.41 R | 0.69 R | **CLOSE** | Position down 0.41R with 0.69R giveback from +0.29R peak. Trailing stop not armed yet. Stop 0.59R away offers insufficient margin for mean reversion in weak short setup. |
| 8 | 09-02 04:41:49 | −0.31 R | 0.59 R | HOLD | Short is -0.31R unrealised but peaked +0.29R; only 0.59R giveback from MFE. Stop at +0.69R provides adequate protection. Trail arms at +0.75R—close to current MFE. Hold for mean reversion. |
| 9 | 09-02 05:41:49 | −0.37 R | 0.65 R | HOLD | SHORT -0.37R unrealised loss; peaked +0.29R but gave back 0.65R. Stop at +0.63R provides buffer. Trail arms at +0.75R—position still has room to recover toward that threshold. Hold. |
| 10 | 09-02 06:41:56 | −0.32 R | 0.61 R | HOLD | SHORT at -0.32R with +0.68R cushion to stop. Peak +0.29R shows upside tested but not decisively broken. 9h elapsed, no signal. Hold for trail arm at +0.75R. |
| 11 | 09-02 07:41:57 | −0.30 R | 0.59 R | **CLOSE** | Short underwater -0.30R after 10h with 0.59R giveback from +0.29R peak. No trailing stop protection yet (arms at +0.75R). Risk/reward unfavorable; hold only if strong directional conviction remains. |
| 12 | 09-02 08:42:08 | **+0.08 R** | 0.20 R | HOLD | SHORT +0.08R with +1.08R stop buffer. Peak +0.29R shows strength; 20bps giveback is minor. Trail arms at +0.75R. Hold for target; stops protect downside. |
| 13 | 09-02 09:42:19 | **+0.26 R** | 0.03 R | HOLD | SHORT +0.26R, only 0.03R giveback from +0.29R peak. Trail arms at +0.75R; stop 1.26R away. Hold for target. |
| 14 | 09-02 10:42:24 | **+0.50 R** | 0.03 R | HOLD | Position +0.50R with +1.50R stop buffer. Minimal 0.03R giveback from 0.53R peak shows strong trend control. Trailing stop arms at +0.75R—only 0.25R away. Hold for target. |
| 15 | 09-02 11:42:33 | **+0.46 R** | 0.27 R | HOLD | Short +0.46R with +1.46R stop buffer. Peak +0.73R only 0.27R giveback suggests healthy momentum. Trail arms at +0.75R—very close. Hold for trail activation. |
| 16 | 09-02 12:42:34 | — | — | (error) | anthropic error: OverloadedError: Error code: 529 … |
| 17 | 09-02 13:42:53 | **+0.19 R** | 0.53 R | HOLD | Position at +0.19R with peak +0.73R; 0.53R giveback acceptable given 16h horizon. Trailing stop arms at +0.75R—close to peak. Hold for mean reversion upside. |
| 18 | 09-02 14:42:54 | **+0.02 R** | 0.70 R | **CLOSE** | Short at +0.02R with 0.70R giveback from +0.73R peak. 17h elapsed, trailing stop not armed. Risk-reward poor; high drawdown from MFE suggests momentum shift. Close to lock edge. |
| 19 | 09-02 15:43:01 | −0.05 R | 0.77 R | HOLD | SHORT is -0.05R unrealized but peaked +0.73R; only 0.77R giveback with 0.95R cushion to stop. Trail arms at +0.75R (0.02R away). Hold for trailing activation. |
| 20 | 09-02 16:43:12 | **+0.10 R** | 0.63 R | **CLOSE** | Position in drawdown from peak (+0.73R to +0.10R = 0.63R giveback, 86% retracement). Trailing stop not yet armed. Risk-reward unfavorable; hold exposes to further erosion without activated protection. |
| 21 | 09-02 17:43:16 | **+0.18 R** | 0.54 R | HOLD | Short +0.18R, peaked +0.73R with 0.54R giveback. Trail arms at +0.75R—very close. Hold for trail activation; stop 1.18R away provides cushion. |
| 22 | 09-02 18:43:26 | −0.00 R | 0.73 R | **CLOSE** | Position at breakeven after 21h, peak +0.73R now fully given back. Trailing stop not armed; only static stop +1.0R away. Risk/reward unfavorable; hold offers diminishing edge. |
| 23 | 09-02 19:43:35 | −0.02 R | 0.74 R | HOLD | Short underwater only -0.02R after 22h. Peaked +0.73R, now 0.74R giveaway—normal pullback. Stop 0.98R away provides adequate protection. Hold for recovery. |
| 24 | 09-02 20:43:36 | −0.09 R | 0.82 R | HOLD | SHORT still -0.09R unrealised after 23h. Peaked +0.73R but gave back 0.82R—normal mean reversion. Stop at +0.91R provides cushion. Trailing stop arms soon at +0.75R. Hold for recovery or trail trigger |
| 25 | 09-02 21:43:37 | −0.18 R | 0.90 R | **CLOSE** | Short underwater -0.18R after 24h. Peak was +0.73R but gave back 0.90R, suggesting weakness. No trailing stop yet armed. Risk/reward unfavorable; close to lock learning. |
| 26 | 09-02 22:43:49 | −0.17 R | 0.90 R | **CLOSE** | Position underwater -0.17R after 25h with deteriorating setup. Peak MFE +0.73R now down 0.90R giveback indicates momentum reversed. Trail not armed; naked to gap risk. Risk/reward unfavorable. |
| 27 | 09-02 23:44:00 | −0.22 R | 0.94 R | **CLOSE** | Position is -0.22R underwater after 26h with deteriorating technicals. Peak MFE of +0.73R now down 0.94R giveback suggests momentum has reversed. Risk/reward unfavorable; trailing stop won't arm. |
| 28 | 09-03 00:44:02 | −0.17 R | 0.89 R | **CLOSE** | Position underwater -0.17R after 27h with -0.89R giveback from +0.73R peak. Trailing stop not yet armed; risk/reward deteriorating as price moves against short. |
| 29 | 09-03 01:44:13 | −0.37 R | 1.10 R | **CLOSE** | Short -0.37R underwater after 28h; peaked +0.73R then gave back 1.10R (150% of gain). Stop too far (+0.63R). Risk/reward unfavorable. |
| 30 | 09-03 02:44:28 | −0.55 R | 1.27 R | **CLOSE** | SHORT down 0.55R with 1.27R giveback from +0.73R peak. 29h elapsed, trailing stop still unarmed. Risk/reward deteriorating; hold only if conviction remains strong. |
| 31 | 09-03 03:44:31 | −0.42 R | 1.14 R | **CLOSE** | Short underwater -0.42R after 30h. Peaked at +0.73R but given back 1.14R (156% of gain). Trail not armed yet. Holding adds risk without fresh conviction. |
| 32 | 09-03 04:44:39 | −0.30 R | 1.03 R | **CLOSE** | Position at -0.30R with 1.03R giveback from +0.73R peak. Trailing stop not yet armed; 31h elapsed with deteriorating structure suggests holding for marginal +0.75R trail arm is unfavorable risk/reward |
| 33 | 09-03 05:44:48 | −0.42 R | 1.15 R | **CLOSE** | Short underwater -0.42R after 32h; peaked +0.73R but given back 1.15R (157% of peak gain). Stop 0.58R away leaves poor risk/reward. No trailing protection yet. |
| 34 | 09-03 06:44:49 | −0.65 R | 1.37 R | **CLOSE** | Short at -0.65R with 1.37R giveback from +0.73R peak. 33h elapsed, no trail armed yet. Risk/reward deteriorated; holding exposes full 1R stop for marginal upside potential. Close to lock remaining val |
| 35 | 09-03 07:44:58 | −0.58 R | 1.30 R | **CLOSE** | Short underwater -0.58R after 34h. Peaked +0.73R but surrendered 1.30R (178% of gain). Risk/reward deteriorating; stop only +0.42R away. Hold exposes to shrinking buffer. |
| 36 | 09-03 08:44:59 | −0.54 R | 1.26 R | **CLOSE** | Short at -0.54R unrealised loss with 1.26R giveback from +0.73R peak. Position deteriorating after 35h. Risk/reward unfavourable; hold risks further drift without trailing stop protection. |
| 37 | 09-03 09:45:06 | −0.40 R | 1.13 R | **CLOSE** | Position underwater -0.40R after 36h. Peak of +0.73R gave back 1.13R; risk/reward deteriorating. Trailing stop won't arm; only static stop at +0.60R protects. Close to cut losses. |
| 38 | 09-03 10:45:18 | −0.25 R | 0.98 R | **CLOSE** | Short underwater -0.25R after 37h with 0.98R giveback from +0.73R peak. Risk/reward unfavorable; trailing stop not yet armed leaves only fixed protection. Exit to preserve capital. |
| 39 | 09-03 11:45:23 | −0.63 R | 1.35 R | **CLOSE** | Short underwater -0.63R after 38h with 1.35R giveback from +0.73R peak. Risk/reward unfavorable; trailing stop not armed yet. Cut loss. |
| 40 | 09-03 12:45:36 | −0.66 R | 1.39 R | **CLOSE** | Short underwater -0.66R after 39h with 1.39R giveback from +0.73R peak. Risk/reward unfavorable; trailing stop won't arm. Close to cut losses. |

**It consulted nine times while in profit and said HOLD seven of them.** Two in-profit CLOSE
verdicts (+0.10 R at 16:43 and +0.02 R at 14:42) were produced and discarded by configuration.

### 🔴 Checking the in-profit HOLDs against the prompts they were given

**Consult #15 — 09-02 11:42:33, at +0.46 R, HOLD. The verbatim prompt:**

```
OPEN POSITION — decide CLOSE or HOLD.

Position
  Side: SHORT   Entry: 99.24   Now: 98.04
  Unrealised: +0.46R   (1R = the ORIGINAL stop distance, 2.6200)
  Elapsed: 14.0h
  Current stop: 101.86  ->  +1.46R away
  Peak so far (MFE): +0.73R   Giveback from peak: 0.27R

Trail
  The trailing stop is NOT ARMED — it arms only at +0.75R, which this
  position has not reached, so the stop above is the only protection.
  It would arm at 97.2750 (+0.75R).

Partial
  None taken; 1.0 open.

EVERY figure above is computed from this position's own ledger row; `Now` is the last traded price this poll tick.
Consultation trigger: hourly review (no signal fired).

Decide whether to close the remaining size now or hold it.
```

Claim by claim: "+0.46R" ✅ verbatim from the prompt. "+1.46R stop buffer" ✅ verbatim.
"Peak +0.73R only 0.27R giveback" ✅ both verbatim. "Trail arms at +0.75R" ✅ verbatim.
**Every numeric claim is exactly its prompt.** No fabrication.

**Consult #19 — 09-02 15:43:01, at −0.05 R, HOLD. The verbatim prompt:**

```
Position
  Side: SHORT   Entry: 99.24   Now: 99.37
  Unrealised: -0.05R   (1R = the ORIGINAL stop distance, 2.6200)
  Elapsed: 18.0h
  Current stop: 101.86  ->  +0.95R away
  Peak so far (MFE): +0.73R   Giveback from peak: 0.77R

Trail
  The trailing stop is NOT ARMED — it arms only at +0.75R, which this
  position has not reached, so the stop above is the only protection.
  It would arm at 97.2750 (+0.75R).
```

Its reason: *"Trail arms at +0.75R (0.02R away). Hold for trailing activation."*
**Both numbers are arithmetically correct against the prompt** — peak +0.73 R, arm +0.75 R,
difference 0.02 R.

🔴 **And this is the structural defect of the exit advisor, stated precisely.** The "0.02 R away"
is measured **from a high-water mark that is four hours in the past and cannot arm anything by
itself.** To reach the arm from 99.37 the price had to travel **2.10 in price — 0.80 R, 2.11 %**
— in the short's favour. The prompt hands the model a peak and an arm and gives it no way to see
that the gap between them is not the distance still to travel. Seventeen HOLD verdicts across the
hold lean on that phrasing — *"very close"*, *"only 0.25R away"*, *"0.02R away"*, *"arms soon"*.

**Note what the exit-advisor prompt does NOT contain: any market data at all.** No trend, no ADX,
no order book, no signal, no volume. Only the position's own ledger row. It is structurally
incapable of forming a view about the market; the single lever it has is proximity to the arm,
and it pulled that lever while the arm was receding. The arithmetic is honest; the prompt is what
is defective.

### Two further observation-only mechanisms fired during the hold

```
Sep 02 13:42:51  [SMART-EXIT-DRYRUN] would-exit SOL/USDT:USDT SHORT vpos=42 @~98.7400
                 chop=0 regime=TREND gap=Expanding peakMFE=1.91% giveback=1.41%
                 oppWall=8.7 imb=0.4279 adx15=63.198 flip15=0 (arm=1.2/gb=0.8)
                 — DRYRUN, position untouched
Sep 02 15:00:13  TREND-REVERSAL [OBSERVE]: Trend Catcher Up (trend_catcher_up)
                 would-close open SHORT vpos=42 — observe only, not acting
Sep 02 15:00:16  TREND-REVERSAL [CONFIRM]: Any Bullish Confirmation (confirmation_bull_any)
                 would close open SHORT vpos=42 dryrun=True
Sep 02 15:00:18  TREND-REVERSAL [CONFIRM]: Bullish Confirmation (confirmation_bull)
                 would close open SHORT vpos=42 dryrun=True
```

The SMART-EXIT sampler's would-exit at **98.74** is **+0.19 R** — a real, if modest, profit.

## 3e. 🔴 Was any exit signal received? — YES, one armed, and it expired unused

**How the mechanism actually works** (main.py:5648-5698, main.py:5944-5962,
state_machine.py:323-369): a **1h `Exit Signal`** *arms* the open side for
`EXIT_PENDING_TTL_MINUTES = 360` (**6 hours**). The close fires only when an **opposite-direction**
BOS / CHOCH / Liquidity-Grab arrives on `EXIT_CONFIRM_TF = '15m'`. For an armed **SHORT** that
means a **BULLISH** 15m structure signal. If the TTL elapses with no confirmation, the arm
expires silently.

**The complete timeline:**

| time (UTC) | event | status | note |
|---|---|---|---|
| 09-02 03:30:06 | 15m **Bullish** I-CHOCH | `exit_unarmed_noop` | would have qualified — nothing armed |
| 09-02 08:45:01 | 15m Bearish I-CHOCH+ | `exit_unarmed_noop` | wrong direction for a SHORT |
| 09-02 10:45:01 | 15m Bearish S-BOS | `exit_unarmed_noop` | wrong direction |
| 09-03 00:00:11 | 15m **Bullish** I-CHOCH+ | `exit_unarmed_noop` | would have qualified — nothing armed |
| 09-03 02:45:03 | 15m **Bullish** I-BOS | `exit_unarmed_noop` | would have qualified — nothing armed |
| 09-03 03:00:04 | 15m **Bullish** S-CHOCH | `exit_unarmed_noop` | would have qualified — nothing armed |
| **09-03 04:00:10** | **1h `Exit Signal`** | **`exit_armed`** | `EXIT_ARMED side=SHORT expires=2026-09-03T10:00:10.977608+00:00` · position was −0.30 R |
| 04:00:10 → 10:00:10 | **the entire 6-hour armed window** | — | 🔴 **ZERO 15m exit-confirmation signals of either direction arrived** |
| 09-03 10:00:10 | arm expires silently | — | never used |
| 09-03 10:15:00 | 15m Bearish I-CHOCH+ | `exit_unarmed_noop` | 15 min after expiry — and wrong direction anyway |
| **09-03 13:00:11** | **15m Bullish I-CHOCH** | `exit_unarmed_noop` | 🔴 **exactly the confirmation the armed SHORT needed — 3 h 00 m after the arm lapsed** |
| 09-03 13:00:12 | 1h `Smart Trail Switch Bullish` | `trend_set` | 1h context flipped LONG |
| 09-03 13:42:12 | stop filled | `sl_triggered_short` | 101.87 |

**The ordering was inverted at both ends.** Four qualifying bullish confirmations arrived during
the hold. Three of them came in the **four hours before** the arm (00:00, 02:45, 03:00) and one
came **three hours after it lapsed** (13:00). The six-hour window in between — the only window in
which the mechanism could act — contained nothing at all.

This is not a code fault. Every one of those eleven rows was handled exactly as
`main.py:5944-5962` specifies, and each produced its Telegram card. It is a **sequencing
mismatch** between a 6-hour arm and the rate at which 15m structure signals actually arrive.

Counterfactuals on this branch, for scale:

- close on the 13:00:11 bullish confirm at ≈101.61 → **−$2.578 = −0.984 R** (saves $0.26 / 0.10 R)
- close on the 04:00:10 arm itself at ≈100.47 → **−$1.437 = −0.548 R** (saves $1.40 / 0.53 R)

Neither is a profitable exit. By the time anything armed, the trade was already gone.

## 3f. 🔴 THE COUNTERFACTUAL

Modelled at the venue's **real 0.100 % taker** on both legs plus the actual funding
(0.00701167). Entry fee is the booked 0.09924.

| closed at | price | gross | **net $** | **net R** |
|---|---|---|---|---|
| **the trail level** | — | — | — | 🔴 **NEVER EXISTED — the trail never armed** |
| trail level *had it armed*, from the actual water mark (97.34 × 1.01975) | 99.2625 | −0.0225 | **−$0.2280** | **−0.087 R** |
| trail level *had it armed at the arm price* (97.2750 + 1.9622) | 99.2372 | +0.0028 | **−$0.2027** | **−0.077 R** |
| **the breakeven lock** (entry − 0.20 %) | 99.0415 | +0.1985 | **−$0.0068** | **−0.003 R** |
| **at MFE** — Bybit water mark | **97.3400** | **+1.9000** | **+$1.6964** | **+0.648 R** |
| at MFE — OKX 5m low | 97.3100 | +1.9300 | +$1.7264 | +0.659 R |
| the SMART-EXIT would-exit (09-02 13:42) | 98.7400 | +0.5000 | +$0.2950 | +0.113 R |
| the exit advisor's first in-profit CLOSE (09-02 14:42) | ≈99.1876 | +0.0524 | −$0.1530 | −0.058 R |
| **ACTUAL** | **101.87** | **−2.6300** | **−$2.8381** | **−1.083 R** |

🔴 **Read the two middle rows.** Even if the arm had been reached, the two mechanisms that would
then have come into existence were worth, at the prices this trade actually printed, **−$0.23**
and **−$0.01**. The breakeven lock is a **fee wash by construction** — `trail_arm.py`'s own
docstring says it outright: *"at the venue's real 0.100 % it is a fee WASH (net −0.0002 % of
notional)"*. The lock does not save money; it stops the bleeding.

**The only counterfactual worth real money is closing at or near the peak, and this bot has no
mechanism aimed at that.** The trail gives back 0.749 R from the high-water mark; on a 0.725 R
excursion that is the whole excursion and more. The gap between the best available outcome
(+$1.70) and the best *mechanised* outcome (−$0.01) is $1.70 — and nothing in the current design
reaches into it.

---

# 4. WHAT WOULD HAVE PREVENTED IT — descriptive only

## 4a. Every mechanism that COULD have closed this in profit, and why each did not fire

| # | mechanism | state | why it did not fire |
|---|---|---|---|
| 1 | **Trailing stop** | live | **Never armed.** Peak 0.7252 R vs arm 0.7500 R — short by **0.0248 R / 6.5 cents**. And had it armed, its 0.749 R callback would have parked it at 99.2372, three cents *below* entry — a break-even exit, not a profit. |
| 2 | **Breakeven lock** | live | **Never armed** — same single condition (`virtual_trader.py:2122`), same 97.2750. Had it fired it parks at 99.0415, worth **−$0.007**. |
| 3 | **Partial realisation at the arm** | **OFF** | `PARTIAL_AT_ARM_ENABLED = False` (config.py:312, off since 2026-08-14). Inert — and gated behind the same arm regardless. |
| 4 | **Hourly exit advisor** | **DRYRUN** | Consulted **40** times, said CLOSE **22** times, including **twice while in profit** (+0.10 R, +0.02 R). `EXIT_ADVISOR_DRYRUN = True` — no verdict reaches any close path. |
| 5 | **SMART-EXIT dryrun sampler** | **DRYRUN** | Logged a would-exit at 98.74 (**+0.19 R**) on 09-02 13:42. Observation only. |
| 6 | **Trend-reversal observers** | **DRYRUN** | Three lines on 09-02 15:00 declaring they would close vpos 42. `dryrun=True`. |
| 7 | **1h Exit Signal + 15m confirmation** | live | Armed once at 04:00:10 on 09-03, when the position was already −0.30 R. **Zero confirmations inside the 6 h TTL.** The qualifying bullish confirm arrived 3 h after expiry. |
| 8 | **Time stop** | **DISABLED** | `MAX_POSITION_DURATION_MINS = 0` (config.py:582, Titan parity: no time-close). Could not fire at any hold length, including 40 h. |
| 9 | **Entry rechecks T+10/60/300 s** | live | All three returned `verdict=OK, no negative deltas` (wall 8.8 → 9.6 → 10.7, ADX unchanged at 29.4). Window closed 5 minutes in; `recheck_status = 'done'`. Not an exit mechanism thereafter. |

**Summary of that table: of nine mechanisms, three are switched to observe-only, one is disabled,
one is inert, one armed too late into an empty window — and the two that were live and
arming-capable both hang off a single threshold the price missed by 0.0248 R.**

## 4b. 🔴 The peak never reached the arm — with the number

**Best price 97.34 against an arm at 97.2750. Short by 0.0650 in price, 0.0248 R, 0.0655 % of
entry.** Zero of 2,940 tick samples and zero of 482 five-minute candles printed a price at or
below the arm.

**So on this bot's own contract the position was never in *protected* profit.** It was in
unlatched, unprotected profit — ≥ +0.50 R for 3.1 % of the hold, ≥ +0.70 R for 0.03 % (one
sample) — and at no instant did it cross the line at which this bot does anything at all.

**Reconciling the card against the venue's unrealised history.** The card's figures are all
*realised-at-close* and they reconcile with the ledger exactly:

```
card:    Gross −2.6300 · Fees −0.2011 · Funding −0.007012 · Net −2.8381 · book +$15.5574
ledger:  gross −2.6300 · total_fees 0.20111 · funding_paid 0.00701167 (source: venue)
         net_pnl −2.83812167 · sum over 14 closed LIVE positions +15.55742
```

Agreement to seven decimals on the net and to the cent on the book. **The unrealised profit the
operator watched during the hold was real** — it peaked at **+$1.90 gross, +$1.70 net** of both
legs' fees. There is no discrepancy between what the operator saw and what the ledger holds; the
gap is between what the position *earned on paper* and what any mechanism was configured to
*capture*.

🔴 **What could NOT be verified, stated plainly:** the venue's own unrealised-PnL history and its
own OHLC could not be pulled. Bybit's public API returns **HTTP 403** to this host, and its
private endpoints are reachable only through the running bot's Tor-routed ccxt instance, which is
off-limits under the read-only instruction. Standing in for it: the bot's own **2,940 Bybit tick
samples** (which are the venue's prices, recorded by the bot) and **488 OKX 5m candles**. They
agree with each other to **3 cents at the peak** (97.34 vs 97.31), so the conclusion — the arm was
never reached — does not depend on which of them is used.

## 4c. What is broken, what is working as designed, what is unrankable at this n

### BROKEN — demonstrably not doing the job as written

1. **The exit advisor's user prompt.** It presents a high-water mark and an arm price side by side
   with no indication that the gap between them is not a distance the position can travel from
   where it now stands. The advisor reasoned correctly from that prompt **17 times** to "hold for
   trail activation" while the arm had become, in practice, unreachable. One defect, one prompt,
   seventeen consequences. It cost nothing this time only because nothing acted on any of them.
2. **The entry reason's "1h rearm stale".** Not in the prompt, not derivable from it, contradicted
   by the prompt's own counting note — and applied to the only tier that opposed the trade. Small,
   specific, and the kind that recurs without leaving a mark.

### WORKING AS DESIGNED — must not be read as failures

- **The stop.** Set provisionally at 101.87 from the pre-trade ticker *before* the fill was known
  (so the position was never naked), corrected to the exact 101.86 two seconds later, never moved
  again, filled at 101.87 with one cent of slippage. Exactly the documented behaviour, and the
  provisional-then-exact sequence is a deliberate safety design.
- **The BE lock and the trail not firing.** Their single shared arming condition was not met.
  There is no mechanical defect: the mechanism never got the chance to misbehave. **This
  specifically answers the question that would have outranked everything else in this report — it
  did not happen.**
- **The exit advisor being ignored.** `EXIT_ADVISOR_DRYRUN = True` is deliberate and documented:
  an acting advisor would close positions the trail would otherwise take, destroying the only live
  trail measurement in the project.
- **The book gate, the flat/ADX gate, the recheck tiers, the arm/confirm exit flow.** All
  evaluated, all behaved, all logged. In the same 40-hour window the surrounding gates refused
  156 signals as `htf_blocked`, 122 as `below_threshold`, 64 as `risk_halt`, 34 as `ai_skipped`,
  21 as `entry_gate_refused`, 10 as `flat_adx_blocked` and 4 as `book_blocked`. The funnel was
  working hard throughout.
- **`MAX_POSITION_DURATION_MINS = 0`.** A 40-hour hold is not a bug in a swing bot with no
  time-close by design.

### UNRANKABLE AT THIS n

- **Whether 0.75 R is the wrong arm.** This is the **first** position in the live book to peak
  between 0.70 R and 0.75 R. n = 1. The 2026-08-14 decision that set 0.75 R was cut on 29
  positions, explicitly **refused** the sweep's better cell (0.50 R) as a fitted maximum, and
  recorded in advance that four of the six positions carrying that cell peaked between 0.510 R and
  0.568 R — i.e. *the same shape one notch down*: a peak sitting just under whatever the arm is.
  The config's own note states that a smaller-than-expected realised effect *"is not a reason to
  lower the arm further."* One observation cannot rank this either way.
- **Whether SOL's short side has any edge.** Six live shorts, six losses, −4.589 R, zero winners.
  Striking, and not statistically separable from chance at n = 6. It can be **stated**; it cannot
  be **ranked**.
- **Whether an armed exit advisor would have helped.** On this trade, acting on its first
  in-profit CLOSE (09-02 14:42, +0.02 R) realises ≈ **−$0.15** instead of **−$2.84**. That is one
  observation, against 22 CLOSE verdicts of which 20 were underwater and several would have cut
  the position at −0.3 R only for it to return to green twice afterwards. n = 1 on the case that
  matters.

**No change is proposed. Per instruction, this report is descriptive.**

---

# CONTROLS

**🔴 SOL's live short book is now SIX positions — where n cannot rank, and the descriptive answer
anyway:**

| question | can n rank it? | the descriptive answer |
|---|---|---|
| Does SOL's short side have an edge? | **No** — n = 6 | Six live shorts, six losses, **zero winners**, −4.5894 R / −$6.5880. Every live dollar of profit is long-side. |
| Is 0.75 R the wrong arm? | **No** — n = 1 at this peak band | Peak 0.7252 R, arm 0.7500 R, missed by 0.0248 R. Had it armed, the trail books ≈ break-even and the lock books −$0.007 — so a lower arm buys a fee wash, not a profit, at these prices. |
| Would an armed exit advisor have helped? | **No** — n = 1 | It said CLOSE at +0.10 R and +0.02 R and 20 more times underwater. On this trade acting on the first in-profit CLOSE saves $2.69. |
| Is the 6 h exit-arm TTL too short? | **No** — n = 1 | Four qualifying bullish 15m confirms during the hold: three before the arm, one three hours after it lapsed, none inside it. |
| Is the daily-regime standing order being obeyed? | **Yes** — n = 2,127 | 2,121 obeyed / 6 overridden, unchanged. This trade is not in that population. |

**🔴 Read-only confirmation:**

- **DB read-only** — every connection opened as `sqlite3.connect("file:…/trades.db?mode=ro", uri=True)`, SELECT statements only. No INSERT / UPDATE / DELETE was issued or attempted.
- **cwd outside SOL's tree** — all work ran from `/root` and the session scratchpad. The shell never entered `/mnt/volume_nyc1_1780480650620/mercury-sol`.
- **Config not imported** — `config.py`, `trail_arm.py`, `book_gate.py`, `state_machine.py`, `main.py` and `virtual_trader.py` were read as **text** with `sed`/`grep`, with line citations. The only Python import of any config in this session was Titan's own `openitems_guard.py` reading **Titan's** config, as mandated.
- **No writes attempted** — no file under the SOL tree was opened for writing.
- **No orders placed or cancelled** — no private venue call of any kind was made. Public data was read from **OKX only** (keyless, direct); Bybit's public API returned 403 and no Bybit call succeeded or was retried through the bot.
- **Service untouched** — `mercury-sol.service`: `MainPID = 1196924`, `SubState = running`, `ActiveEnterTimestamp = Mon 2026-08-24 13:29:27 UTC` — all identical before and after.
- **`NRestarts` unchanged** — **0** at session start, **0** at session end.
- **File hashes identical before and after:**

```
ed7a14b0df440f2fc5040e87ea5b504b  mercury-sol/config.py
a02ce04e6a12864bfcc0c6118137ebd7  mercury-sol/claude_advisor.py
35b0201626303c730df6d1c2c3ec3f9e  mercury-sol/main.py
```

  A `find` over the whole SOL tree for anything modified after the session began returns
  **exactly one path — `trades.db`** — written by the running bot itself (size unchanged at
  70,356,992 bytes; mtime advanced by its own inserts, which continued throughout). No `.py`,
  `.json`, `.env` or `.md` file was touched.
- **Titan** — `tools/openitems_guard.py` run once (read-only by construction: reads git, one
  markdown file, and imports Titan's config), **exit 0, header and current-state table agree with
  runtime**, `titan-bot HEAD f5d3542`. Nothing else in `/root/titan-bot` was touched.

---

## THE THREE SENTENCES

1. **It was not an override.** The daily regime was NEUTRAL and the 4h AGREED with the short; the
   standing order never engaged, and the 6-override record stands unchanged at 2,121 obeyed of
   2,127.
2. **There is no mechanical defect at the stop.** The breakeven lock never applied because it arms
   at −0.75 R — the same threshold as the trail, not at −0.20 % — and the price missed that
   threshold by **0.0248 R / 6.5 cents**. The stop was set once, corrected once two seconds later,
   and never moved again; 101.87 is the original 101.86 filling with a cent of slippage.
3. **The position was never in profit this bot was built to keep.** Peak +0.7252 R against an arm
   at 0.7500 R; and even had it armed, the trail was worth ≈ break-even and the lock −$0.007. Nine
   mechanisms could in principle have closed it green; three are observing, one is disabled, one is
   inert, one armed into an empty window, and the two that were live share the one threshold the
   price did not reach.
