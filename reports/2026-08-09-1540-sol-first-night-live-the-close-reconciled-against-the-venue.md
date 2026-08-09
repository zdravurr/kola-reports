# sol-first-night-live-the-close-reconciled-against-the-venue

_2026-08-09 15:40 UTC_

---

# Mercury-SOL — the first full night live. Fix 1 and fix 3 are PROVEN in production. The close card the Boss received said **−$3.26** on a trade that made **+$1.58**.

**Read-only pass. Nothing changed, nothing restarted, nothing placed.** Every venue call was a read;
the DB was opened `mode=ro` throughout.

**The good news is real and it is load-bearing:**
- 🟢 **FIX 1 IS PROVEN.** `_read_entry_fill` returned a REAL venue fill on the 21:10 entry —
  1.3 @ 76.29, fee $0.099177 read from the order, verified against the venue's own execution
  record. Neither fallback branch fired. This is the fix that broke every entry yesterday morning.
- 🟢 **FIX 3'S REFUSAL BRANCH IS PROVEN.** Two same-side webhooks in the same second, ONE order
  placed, ONE position. The loser was **refused, not queued**, and it is countable on its own row.
  It has now fired **eleven times** in production, with zero duplicates across all eleven.
- 🟢 The stop was on the venue **before** the fill was read. Protect-before-describe held.
- 🟢 Zero tracebacks, zero naked-position alerts, zero hands-required. Heartbeat steady.

**And three defects the night exposed, all in the MONEY REPORT, none in the trading path:**
- 🔴 **The Armed-Exit close card priced the live close against a PAPER trade from 2026-08-02.**
  The Boss's phone said `−$3.2605`. The venue paid `+$1.5779`.
- 🔴 **The book's net for vpos 29 is overstated by $0.0246 (+1.56%)** — the partial's fee was booked
  at the old understated rate and the funding charge was never booked at all.
- 🔴 **The advisor's book claim is FALSE for the fourth time in four.** "No opposing walls above
  entry" — four ask walls sat above it, in its own prompt.

Prior: [baseline 18:04](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1804-sol-verification-of-the-last-pass-resolver-cron-proven.md) ·
[alerts 17:52](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1752-sol-naked-alerts-resolved-on-evidence-be-decided-reason-is-narration.md) ·
[reasoning judged 15:30](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1530-sol-0850-reasoning-judged-apply-guard-and-adoption-diffs.md)

---

## 0. 🔴 TWO CORRECTIONS TO THE PREMISE OF THE QUESTION — both found by checking, not recalling

**(1) vpos 29 did NOT close overnight. It closed at 18:45:05 on 2026-08-08** — before the new long,
not after it. The order of the night was: close 18:45 → new long 21:10 → quiet night.

**(2) NO duplicate-entry refusal fired at 02:25.** I went through the journal minute by minute.
The complete list of `[ENTRY-GATE]` refusals since the flip:

```
2026-08-08 20:10:13  LONG
2026-08-08 21:10:12  LONG   <- the one that guarded the entry that became vpos 30
2026-08-09 05:35:10  SHORT
2026-08-09 05:55:13  SHORT
2026-08-09 06:10:14  SHORT
2026-08-09 06:20:11  SHORT
2026-08-09 06:25:14  SHORT
2026-08-09 06:30:17  SHORT
2026-08-09 15:00:12  LONG
2026-08-09 15:00:12  LONG
2026-08-09 15:45:01  LONG
```

02:00–03:00 UTC held four webhooks (02:15, 02:30, 02:40, 02:55) and **no entry attempt reached the
gate at all**. If the card you read was timestamped 02:25 on the phone, it is a phone-local
rendering of one of the rows above — most plausibly the 05:35 SHORT (UTC−3) or the 21:10 LONG.
**I am not going to guess which; I am telling you what the machine recorded.** Everything asked of
"the 02:25 refusal" in §4 below is answered against **21:10:12**, the one that guarded the entry.

---

## 1. THE NEW LONG — vpos 30. Fix 1's live proof.

### (a) The full record

| | |
|---|---|
| **vpos** | **30** |
| side | **LONG** (buy) |
| entry price | **76.29** |
| size | **1.3 SOL** ($99.18 notional, margin $20 × 5x) |
| stop | **75.41** (= fill − 2.5×ATR₁ₕ = 76.29 − 0.883975 = 75.4060 → tick 75.41) |
| opened_at | **2026-08-08T21:10:20.117232+00:00** |
| **fee CHARGED** | **$0.099177** — `fee_verified=1` |
| 1R | $1.144 (1.3 × 0.88) · stop distance 1.153% |
| trades row | 16857 · order_id `989c90cf-e700-4195-89b4-9d291a051fe2` |
| `is_paper` | **0** |

**The fee is the venue's own number, not a model.** The venue execution record:

```
execTime 1786223418857 = 2026-08-08 21:10:18.857 UTC
  side=Buy qty=1.3 price=76.29 fee=0.099177 feeRate=0.001 execType=Trade
  orderId=989c90cf-e700-4195-89b4-9d291a051fe2   <- identical to trades.order_id
```

`feeRate=0.001` — the real Bybit taker rate, the one the 16:08 fix taught the bot to read.
The 1.82× understatement is gone from the live path.

### (b) 🔴 `_read_entry_fill` RETURNED A REAL FILL. Nothing fell back.

**This is proven by SILENCE, and the silence is load-bearing — so here is why it is admissible.**
`_read_entry_fill` (`main.py:2055-2095`) has exactly three exits, and **two of the three print**:

```python
except Exception as e:
    print(f"...[ENTRY] fill read FAILED ({e}) — NOT booking a fabricated position")
    return None, None                                   # <- prints
if avg is None or avg <= 0:
    print(f"...[ENTRY] filled {filled} but NO average price — using "
          f"pre-trade ticker {fallback_px} as a LABELLED estimate")   # <- prints
return filled, avg                                      # <- the happy path, SILENT by design
```

**Neither string appears anywhere in the journal since the flip.** The happy path is silent because
a Bybit market order is normally filled on return — `filled` and `average` are already on the order
dict and it costs no extra call.

And the silence is corroborated three ways, so it does not stand alone:

1. **`fee_verified=1` on the row.** `_resolve_fee` returns `True` **only** when `order_fee is not
   None` — i.e. only when the order dict carried a populated `fee.cost`. A stub order response
   cannot produce this.
2. **The booked fee equals the venue execution to the last digit** — `0.099177` in both.
3. **The venue's position `avgPrice` is 76.29**, read live today.

🔴 **The one thing that would have made this ambiguous — and does not:** the pre-trade ticker was
*also* 76.29, so the number alone proves nothing. What proves it is that the fallback branch that
would have used the ticker **announces itself**, and it did not speak. The trace:

```
21:10:19  [SL] PROVISIONAL stop set from pre-trade ticker 76.29 → 75.41 (route=fallback_atr)
                BEFORE reading the fill — position is protected
21:10:20  [SL] exact level equals the provisional 75.41 — no re-set needed
```

"Exact level equals the provisional" is the code stating that the stop recomputed **from the real
fill** landed on the same tick as the one computed from the ticker. It read the fill, it compared,
it found no change needed.

**Fix 1 has now completed a live entry. It is closed.**

### (c) The engine is MANAGING it — and no alert was raised

```
21:10:20  [LIVE-BOOK] vpos=30 BOOKED is_paper=0 LONG size=1.3 @ 76.29 sl=75.41 1R=$1.14
                      — engine now manages it
21:10:36  RECHECK vpos=30 LONG T+10s  score=0 verdict=OK wall=6.5/6.5 adx=53.2 | no negative deltas
21:11:27  RECHECK vpos=30 LONG T+60s  score=0 verdict=OK wall=6.2/6.5 adx=53.2 | no negative deltas
21:15:33  RECHECK vpos=30 LONG T+300s score=0 verdict=OK wall=7.2/6.5 adx=53.2 | no negative deltas
```

All three recheck tiers ran and passed. `recheck_status='done'`. **Contrast with vpos 29**, whose
adoption left `entry_wall_baseline_mult` / `entry_adx_1h` / `entry_atr_pct_1h` NULL and closed the
recheck by fiat — vpos 30 has all three populated (6.5 / 53.20 / 0.4635) because it came through the
front door.

**Breakeven, partial and trail — evaluated every tick, correctly NOT yet armed:**

```
arm distance = SL_BUFFER_ATR × ATR₁ₕ = 2.5 × 0.35359018 = 0.883975
arm price    = 76.29 + 0.883975 = 77.1740        <- the +1R trigger
water_mark   = 77.03                              <- highest seen; gap to arm 0.1440 (0.19%)
max_adverse  = 75.73                              <- lowest seen; stop 75.41 never approached
mgmt_state   = {"breakeven_applied": false}       <- correct, the arm has not been reached
```

`water_mark` moved from the 76.29 seed to 77.03 and `max_adverse_price` to 75.73 — **the engine has
been tracking both extremes**, which is the positive evidence that the tick is live rather than
merely logging a heartbeat. On arming, the BE lock parks the stop at 76.29 × 1.0020 = **76.4426**
and the partial realises 1.3/3 = 0.4333 → **0.4** after the 0.1 step. Neither has happened because
the high is $0.144 short of the trigger.

🔴 **NO naked-position alert was raised for vpos 30.** The table still holds exactly the five rows
from 2026-08-08, all resolved, the newest stamped `15:40:43`. Nothing was appended overnight.

### (d) The stop was set BEFORE the fill was read — timestamps in order

| # | time (UTC) | event | source |
|---|---|---|---|
| 1 | 21:10:17 | `[QTY] entry.live 1.310788 → 1.3` (step quantisation) | journal |
| 2 | **21:10:18.857** | **order FILLED on the venue** — 1.3 @ 76.29 | venue execution |
| 3 | **21:10:19.195** | **stop order created on the venue** — trigger 75.41, qty 1.3, reduceOnly | venue order record |
| 4 | 21:10:19 | `[SL] PROVISIONAL stop set … BEFORE reading the fill — position is protected` | journal |
| 5 | 21:10:20 | `[SL] exact level equals the provisional` — the fill had been read | journal |
| 6 | 21:10:20.117 | row written, `is_paper=0` | `virtual_positions.opened_at` |

**The ordering holds: protection at :19.195, description at :20.117.** The position was unstopped
for **338 ms** between fill and stop — the irreducible window of a market order followed by a
position-level SL, not a defect.

---

## 2. 🔴 HOW IT DECIDED TO ENTER — judged, not assumed

### (a) The tiers, the arithmetic, the cascade

**The three tiers as the advisor was shown them:**

| slot | signal | direction | age | vs LONG |
|---|---|---|---|---|
| 1H | `15m-rearm: HyperWave OB Signal Down` | **SHORT** | **5.4h** | **OPPOSES** |
| 15m | `HyperWave Signal Up` | LONG | 70m | AGREES |
| 5m trigger | `Bullish I-BOS` | LONG | — | AGREES |

Combo weight **1.00** — the baseline. This combo has no history; it is neither a historical winner
nor a loser. `weight_used=1.0`.

**The score, in full:**

```
matrix raw            TREND      0.00  (0 signals)
                      MOMENTUM   1.75  (1 signal)
                      LIQUIDITY  0.00  (0 signals)
                      EXECUTION  2.50  (2 signals)
                                 ────
                      raw        4.25

macro/context adj    ema_cross_15m +0.0400   ema_cross_1h +0.0400
                     ema_slope_15m +0.0222   ema_slope_1h +0.0200
                     dxy           +0.2343   mtf          +0.3088
                     news           0.0000   funding       0.0000
                                             ────────
                     adj          +0.6653

final                4.25 + 0.6653 = 4.9153  ->  stored confluence_score 4.92
macro_gate_penalty    0.00
```

**The threshold it faced: `CONFLUENCE_SCORE_THRESHOLD = 2.0`**, with `MACRO_GATE_DRYRUN = False`, so
the gate compares the macro-gated score — and with a zero macro penalty both candidate readings
(raw 4.25 and adjusted 4.92) clear 2.0 by more than 2×. **The score gate is not a filter at this
setting; it was never in question.** Its own comment says so: *"at 2.0 the AI consult is the real
entry filter."* Separately, `AI_ADVISOR_FALLBACK_SCORE_THRESHOLD = 7.5` — at 4.92 the advisor was
**mandatory**, not bypassable.

**The cascade's verdict:**

```
HTF_WOULD_PASS (tolerate-NEUTRAL) LONG 1H=NEUTRAL 15m=LONG 5m=LONG
                                  was='1H NEUTRAL (no active TREND signal)'
```

**PASSED, under tolerate-NEUTRAL.** 🔴 **And here is a seam worth naming.** The cascade saw the 1H
slot as **NEUTRAL — "no active TREND signal"** — and passed on that basis. The advisor's prompt, for
the same instant, rendered the 1H slot as **an active SHORT signal 5.4 hours old** and duly counted
it `OPPOSES`. Two subsystems, one fact, two different readings of it: the cascade let the entry
through *because the 1H was empty*, and the advisor approved it *despite the 1H opposing*. Neither
is wrong on its own terms — the 15m-rearm surrogate is not a TREND-slot signal — but nothing in the
record reconciles them, and the entry passed both by being read two different ways. This is the
"ONE FACT, MANY JUDGES" class, in the entry path.

### (b) 🔴 THE ADVISOR'S VERBATIM PROMPT AND ITS VERBATIM REASON

**The system prompt's two operative rules, verbatim:**

```
HARD RULE — opposing walls: if a massive limit wall (volume marked with a multiplier, e.g. ×8.3)
sits directly above a LONG entry or directly below a SHORT entry, you MUST reply 'skip'. A thick
wall in the opposing direction represents strong resting liquidity that will absorb the move
before it can develop.

SOFT RULE — FLAT-MARKET GUARD: read the multi-TF Volatility/regime block. Treat the market as
flat/squeezed when 1h ADX is low (~<20-23) AND ATR% is low on 1h/15m AND the EMA-gap is
Contracting/Flat (and/or market_regime is FLAT with weak MTF alignment). In a flat market, prefer
'skip' UNLESS the LuxAlgo confluence is exceptionally strong (clear multi-TF agreement). …
```

**The user prompt, verbatim and complete** (2 390 chars):

```
PROPOSED ENTRY: LONG
Symbol: SOL/USDT:USDT
1H: 15m-rearm: HyperWave OB Signal Down (direction: SHORT, set 5.4h ago)
15m: HyperWave Signal Up (direction: LONG, set 70m ago)
5m trigger: Bullish I-BOS (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0626  |  Volume ratio 5m: 1.47x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 53.2 | 15m 34.3  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.460% | 15m 0.196% | 5m 0.082%
  EMA-gap: 1h 0.781% (Contracting) | 15m 0.080% (Expanding)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 4
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: NEUTRAL, ADX 12.9, EMA-gap 0.534% (Contracting)
  4h: BULL, ADX 21.5, EMA-gap 1.043% (Expanding)
  1h: BULL, ADX 53.2, EMA-gap 0.781% (Contracting)
  15m: BULL, ADX 34.3, EMA-gap 0.080% (Expanding)
  5m: BULL, ADX 20.8, EMA-gap 0.052% (Expanding)
  MTF alignment vs LONG: 4/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $76.30  |  Imbalance ±1%: 0.50 (bid-heavy)
  Bid walls (>4x avg vol): $76.25 (p64, x10.4), $75.75 (p45, x7.2), $75.25 (p5, x4.0), $74.75 (p18, x4.7), $74.25 (p5, x4.2)
  Ask walls (>4x avg vol): $76.25 (p39, x6.5), $76.75 (p38, x6.3), $77.25 (p10, x4.4), $78.25 (p36, x6.1), $78.75 (p15, x4.6)
  Wall figures: pN = this wall's PERCENTILE among all walls this prompt has rendered (n=23,080; the primary figure), xN = the raw volume multiple (secondary). Every wall listed already passed the >4x filter, so the multiple alone does not distinguish an ordinary wall from a thick one — the percentile does. CALIBRATION: ~p50 is an ORDINARY wall, p90+ is genuinely thick. Judge thickness by the percentile, not by the word "massive" or by the multiple.

Tier agreement vs LONG (computed for this consultation):
  1H: 15m-rearm: HyperWave OB Signal Down -> SHORT = OPPOSES
  15m: HyperWave Signal Up -> LONG = AGREES
  5m trigger: Bullish I-BOS -> LONG = AGREES
  Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 2 agree, 1 oppose, 0 neutral, 0 absent.
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.
```

**The raw response, verbatim** (`claude-haiku-4-5-20251001`):

```json
{
  "decide": "execute",
  "confidence": 0.72,
  "reason": "4H/1H/15m/5m all BULL, 1H ADX 53.2 (strong trend), 15m+5m LuxAlgo agree LONG. 1H rearm SHORT is stale (5.4h). Market regime FLAT but confluence overcomes soft rule. No opposing walls above entry. Execute."
}
```

### (c) 🔴 THE BOOK, AS RENDERED — and the claim checked against it

**The book arrived COMPLETE.** Every field the channel can carry was populated: depth (8 000
levels), mid ($76.30), imbalance (0.50, bid-heavy), five bid walls and five ask walls, **each with
its percentile and its multiple**, plus the calibration paragraph. **Nothing arrived empty** —
this answers §2(e) directly, and it matters, because it means the claim below cannot be excused as
the model reasoning from a blank field.

Entry **76.29**, mid **76.30**. Sorted by position relative to the entry:

| level | side | percentile | multiple | vs entry 76.29 |
|---|---|---|---|---|
| $78.75 | **ASK** | p15 | ×4.6 | **ABOVE — opposes a LONG** |
| $78.25 | **ASK** | p36 | ×6.1 | **ABOVE — opposes a LONG** |
| $77.25 | **ASK** | p10 | ×4.4 | **ABOVE — opposes a LONG** |
| $76.75 | **ASK** | p38 | ×6.3 | **ABOVE — opposes a LONG** |
| $76.25 | ASK | p39 | ×6.5 | below entry |
| $76.25 | BID | **p64** | **×10.4** | below entry — supports (thickest wall in the book) |
| $75.75 | BID | p45 | ×7.2 | below — supports |
| $75.25 | BID | p5 | ×4.0 | below — supports |
| $74.75 | BID | p18 | ×4.7 | below — supports |
| $74.25 | BID | p5 | ×4.2 | below — supports |

**Did the reason cite the book? Yes — one clause: "No opposing walls above entry."**

**Is it correct? NO. 🔴 FOUR ask walls sat above the entry**, every one of them already past the
>4× filter that qualifies a level as a wall at all, the nearest at $76.75 (p38, ×6.3) — **46 cents,
0.60%, above the fill.** The statement is false against the model's own prompt, in the same message
that rendered the walls to it.

**This is the fourth false book claim in four checkable claims.** On 2026-08-08 all three entries
claimed "no opposing walls above entry" with ask walls at **p64** in their own prompts. This one
claims it with ask walls at **p38/p36/p15/p10**. **The pattern is confirmed and it is directional:
every error so far erases opposing structure. Not one has ever invented it.**

### (d) 🔴 JUDGING THE REASONING ON WHAT IT SAID — n=1, and the profit does not buy the claim

The position is up **+$0.72 unrealised** as I write. **That is irrelevant to this section and I am
not going to let it be relevant.** One profitable entry cannot retro-justify a false statement of
fact; if it could, the book claim would be unfalsifiable by construction.

**What the reason got RIGHT — and it is most of it:**

- "4H/1H/15m/5m all BULL" — **true**, verbatim from the HTF block, MTF 4/4.
- "1H ADX 53.2 (strong trend)" — **true**, and 53.2 is genuinely high.
- "15m+5m LuxAlgo agree LONG" — **true**, matches the computed tier tally 2-agree/1-oppose.
- "1H rearm SHORT is stale (5.4h)" — **true**, and *correctly discounted rather than ignored*.
  The prompt deliberately makes stale tiers vote in full; the model saw the opposition, named it,
  and gave a reason for setting it aside. That is the behaviour the prompt was rewritten to
  produce, and it produced it.
- "Market regime FLAT but confluence overcomes soft rule" — **a legitimate application of the SOFT
  RULE**, which explicitly permits exactly this override on exceptionally strong confluence, and
  which explicitly warns against skipping a genuine trend on low absolute ATR.

**What it got WRONG:**

- **"No opposing walls above entry" — FALSE.** Four of them, in its own prompt.

**The honest verdict, stated precisely:**

🔴 **The claim is false. The decision it accompanied was not obviously wrong.** Under the prompt's
own calibration — *"~p50 is an ORDINARY wall, p90+ is genuinely thick"* — the thickest opposing
wall was **p38, well below median**. The HARD RULE bites only on a *massive* wall, so **executing
did not violate the hard rule**. Had the model written *"no THICK opposing walls above entry —
nearest is p38, ordinary"*, the claim would have been true, the decision identical, and the
percentile calibration would have visibly done its job.

**It did not write that. It wrote the categorical form, for the fourth time running.** And the
categorical form is the dangerous one, because it is the form a human reading the card believes.

🔴 **The most useful thing in this book, the reason never mentioned:** the **single thickest wall in
the entire book (p64, ×10.4) is a BID wall at $76.25** — four cents under the fill, supporting the
long — and the imbalance was **0.50, bid-heavy**. The book was **mildly favourable** to this entry.
The reason cited a false absence instead of a true presence. **It is still narration, exactly as the
canon written into `consult_for_entry` on 2026-08-08 says. Four for four now says it louder.**

**What this does NOT license:** four claims is a pattern, not a measurement. The Fisher test of
2026-08-08 (p = 1.0000, n = 396, effective n = 6 days) already showed the wall band does not move
the verdict. **Nothing here justifies touching the prompt** — that argument was made and settled on
2026-08-08. What it justifies is that no downstream reader may treat `ai_reason` as a cause.

### (e) Was the wall structure present? YES — completely

Answered in full at the head of §(c): depth, imbalance, ten walls, every one with percentile **and**
multiple, plus the calibration text. **No field arrived empty.** The `advisor_book_json` column is
populated on row 16857. The failure here is not a rendering failure. **The model was shown the
walls and then said there were none.**

---

## 3. vpos 29'S CLOSE — the first live close in this bot's history

### (a) 🔴 THE CLOSE CARDS — VERBATIM. THERE WERE TWO, AND THEY DISAGREE BY $4.86.

**Card 1 — `_send_trade_close_report(…, 'Armed Exit')`, `main.py:1360`:**

```
❌ Trade Closed — LONG [Armed Exit]
💎 SOL/USDT:USDT  @ 76.09
📦 Qty: 0.9
━━━━━━━━━━━━━━━━━━━
💵 Gross P&L:  +$2.3040
💸 Total Fees: -$5.5645
💰 Net P&L:    -$3.2605
━━━━━━━━━━━━━━━━━━━
🔄 Batch #1: Trade 10/30
```

**Card 2 — `_format_close_card`, `virtual_trader.py:1235`, fired by the external-close detector:**

```
✅ VIRTUAL Close — LONG [exchange_UNKNOWN]
💎 SOL/USDT:USDT
📥 Entry: 74.8
📤 Exit:  76.09
━━━━━━━━━━━━━━━━━━━
💵 Gross P&L:  +$1.7850
💸 Total Fees: -$0.1825
💰 Net P&L:    +$1.6025
━━━━━━━━━━━━━━━━━━━
📈 Cumulative (23 closed): -$1126.8556
(paper — no real order)
```

The engine's own log line for the same event:

```
18:45:05  [VIRTUAL] CLOSE vpos=29 LONG entry=74.8 exit=76.09 size=0.9 gross=1.7850
          fees=0.1825 net=1.6025 reason=exchange_UNKNOWN
          [incl. partial pnl=+0.5773 fees=0.0467] (close_row=16837)
```

**Exit price 76.09 · duration 9h 54m 51s (08:50:14.459 → 18:45:05.527) · R as booked +1.355R
(1.6025 / 1R 1.183); R against the venue +1.334R.**

🔴 **CARD 1 IS GARBAGE, AND I HAVE THE MECHANISM.** `lookup_entry_for_close` (`main.py:1260`) is:

```sql
SELECT price, fee FROM trades
 WHERE symbol=? AND side=? AND status='executed'
 ORDER BY id DESC LIMIT 1
```

**No `is_virtual` filter. No link to the position being closed.** vpos 29's real entry row — 16767 —
carries `status='failed'` (it is yesterday morning's fill-read failure), so it is **invisible to this
query**. The most recent matching row was **id 15093: a PAPER long from 2026-08-02, price 73.53,
fee $5.4960 on $10 000 of paper notional.** Reproduced exactly:

```
gross = (76.09 − 73.53) × 0.9              = +2.3040
fees  = 5.4959998500000005 + 0.068481      =  5.5644808
net   = 2.3040 − 5.5645                    = −3.2604808   <- the journal's pnl=-3.260480849999998
```

**The Boss's phone was told a live trade lost $3.26 because a paper trade from seven days earlier
paid a $5.50 paper fee.** The trading path was never touched — this is a report-only defect — but
it is a report about money, and it was wrong by **$4.86** in the direction that matters.

🔴 **Card 2 has its own two labelling defects:** a **live** $100 position closed under the header
**"VIRTUAL Close"** with the footer **"(paper — no real order)"**; and the cumulative line sums
`net_pnl` over **all 23 closed rows regardless of `is_paper`**, mixing 22 paper positions at ~$10 000
notional with the one real $100 close — hence **−$1 126.86** on a book whose live realised total is
**+$1.58**.

### (b) 🔴 THE THREE NUMBERS — the identity HOLDS; two of the three are WRONG

**First, plainly: `Gross − Fees = Net` is EXACT on card 2.**

```
1.7850000 − 0.1825202 = 1.6024798   ✅ to seven decimals
```

**And it is exact around numbers that do not match the venue. I am not softening this.**

The venue's own records for this position — entry, partial, funding, close:

```
08:50:14.456  Buy  1.3 @ 74.80   fee 0.09724   rate 0.001
15:40:49.234  Sell 0.4 @ 76.35   fee 0.03054   rate 0.001   closedPnl +0.55954
16:00:00.000  FUNDING 0.9 @ 76.36  fee 0.0068724  (execType=Funding)
18:45:02.500  Sell 0.9 @ 76.09   fee 0.068481  rate 0.001   closedPnl +1.0183266
```

| | **BOT'S CARD** | **VENUE** | **delta** |
|---|---|---|---|
| Gross | **1.7850** | **1.7810** | **+0.0040** |
| Fees | **0.1825** | **0.1963** | **−0.0138** |
| Funding | *(not booked)* | **0.0069** | **−0.0069** |
| **NET** | **+1.6025** | **+1.5779** | 🔴 **+0.0246 (+1.56%)** |

**Venue net = 0.55954 + 1.0183266 = $1.5778666.** Booked **$1.6024798**.

**Where each cent went — three distinct causes, none of them a rounding artefact:**

1. **+$0.0040 on gross — the partial's price.** The bot booked the partial at **76.36**; the venue
   filled it at **76.35**. × 0.4 = $0.004. The partial ran at 15:40:49, **19 minutes before the
   16:08:59 restart** that loaded the "partial writes the FILL" fix — so this leg is the *last*
   partial booked from a ticker instead of a fill. Not yet re-proven, because vpos 30 has not
   partialled.
2. **−$0.0138 on fees — the understated taker rate, one last time.** The partial's exit fee was
   booked at **0.00055** where Bybit charged **0.001**:
   ```
   booked partial fee 0.0467192 = 0.029920 (entry share, 0.4×74.80×0.001)
                                + 0.0167992 (exit,       0.4×76.35×0.00055)  <- the 1.82x error
   venue  partial fee 0.0604400 = 0.029920 + 0.030540   (0.4×76.35×0.001)
   ```
   Same cause as (1): pre-16:08 code. **The entry leg and the close leg are both at the correct
   0.001** — `0.9×76.09×0.001 = 0.068481`, booked exactly. **The fee fix works; this leg simply
   predates it.**
3. **−$0.0069 — funding was never booked at all.** Bybit charged one funding payment at 16:00 UTC
   while the position was open. `virtual_positions` has no funding column and no code path books
   one. **This is not a leftover from an old build — it will recur on every position held across a
   funding stamp, including vpos 30, which has already paid two ($0.00938 + $0.00992 = $0.0193).**

**The close leg alone, isolated, is PERFECT:** `1.161 − 0.135801 = 1.025199`, and the booked net
minus the partial's booked net is `1.6024798 − 0.5772808 = 1.025199`. **Identical.** The close path
and the venue fee read are sound. **The error is entirely in the pre-fix partial leg and in the
absent funding.**

### (c) 🔴 WHAT CLOSED IT — NOT the trail. Yesterday's projection was WRONG.

```
18:45:01  WEBHOOK_IN tf='15m' body='{"action": "Bearish I-CHOCH+", "task": "trend_signal", "tf": "15m"}'
18:45:03  [CLOSE] order carried no fill price — using ticker 76.09 as a LABELLED estimate
18:45:05  [STOP-CLEANUP] StopOrders cleared for SOLUSDT
18:45:05  ARMED_EXIT_CLOSE side=LONG amount=0.9 price=76.09 pnl=-3.260480849999998
          confirm=ichoch_bear_strong exit_src='Exit Signal'
```

**It was the EXIT SIGNAL** — a 15m `Bearish I-CHOCH+` — firing a pre-armed exit. Not the trail, not
the exit advisor, not the venue stop.

**Yesterday I projected the trail at 75.7650 as most likely. That was wrong**, and the reason is
worth recording: the trail was never approached. Price went **up** from 76.33 to 76.09-at-exit
having peaked at a 76.46 water mark; the trail trigger sat at 75.7650 and the BE stop at 74.9496,
and **neither was ever within 30 cents.** The exit advisor's channel — a bearish Group-B webhook —
was the branch I ranked second, and it is the one that fired, 43 minutes after I wrote the ranking.

🔶 **One thing the close DID expose:** `[CLOSE] order carried no fill price — using ticker 76.09 as a
LABELLED estimate`. The venue's execution says the true exit was **76.09** — so the estimate was
right to the tick, this time, by luck. **The close path still cannot read its own fill on Unified**
(the `fetchOrder` blindness), and it is labelled rather than silent, which is the fix working as
designed. But "labelled estimate" is what the money was booked from.

### (d) The two legs, and whether `close_reason` is a real reason

**The legs DO settle into one coherent net — arithmetically.** `net_pnl = 1.6024798` is the sum of
the close leg (1.025199) and the partial leg as booked (0.5772808); `fills_json` carries both
records; `total_fees = 0.1825202` is the sum of all three fee entries; `mgmt_state_json` reads
`{"breakeven_applied": true, "partial_done": true}`. **The unifier did its job — it just summed one
leg that was itself measured wrong** (§3b).

🔴 **`close_reason` is NOT a real reason. It is a defaulted one, and the bot said so out loud:**

```
18:45:05  [ENGINE] UNKNOWN venue exit type 'UNKNOWN' — booking as 'exchange_UNKNOWN'
          (NOT as 'sl'). Add it to _BYBIT_STOPTYPE_TO_REASON.
18:45:05  [ENGINE] exchange close substantiated: 0.9 @ 76.09 fee=0.068481
          reason=exchange_UNKNOWN (venue stopOrderType='UNKNOWN')
18:45:05  [VIRTUAL] 🔴 UNMAPPED close reason 'exchange_UNKNOWN' — booking as
          'unmapped_close_long' (NOT as a stop-out). The literal reason is preserved
          in virtual_positions.close_reason. Add it to _CLOSE_LABEL and to
          optimizer._CLOSE_*_TYPES.
```

**The mechanism and the label diverged, and the cause is a race the bot won safely.** The bot closed
the position itself with a reduce-only **Market** order (armed exit). Milliseconds later its own
external-close detector saw the venue FLAT, asked the venue *why*, and got `stopOrderType='UNKNOWN'`
— **because a plain market close has no stop-order type.** The detector then booked the close under
its own generic label, overwriting nothing but naming nothing either.

**So the book says `exchange_UNKNOWN` where the truth is `exit_signal`, and the reason lives only in
the journal.** Both guards did the right thing — `'sl'` was explicitly refused, the literal was
preserved, and both call sites printed the exact map they need adding to. **But `close_reason` is
the axis every exit cohort in this book is cut on**, and the first live close in this bot's history
is now filed under a label that means "we don't know". **The one-line remedy each log line names is
NOT applied — this is a read-only pass.**

---

## 4. THE DUPLICATE REFUSAL — fix 3's refusal branch, fired in production

Answered against **21:10:12**, the refusal that guarded this entry (see §0 on "02:25").

### (a) Two webhooks in the same second. ONE order. ONE position.

```
21:10:01  WEBHOOK_IN tf='5m' body='{"action": "Bullish OB Created", "task": "price_action", "tf": "5m"}'
21:10:01  Context recorded: Bullish OB Created (cat=EXECUTION dir=LONG cid=ob_created_bull)
21:10:01  HTF_WOULD_PASS (tolerate-NEUTRAL) LONG 1H=NEUTRAL 15m=LONG 5m=LONG
21:10:01  WEBHOOK_IN tf='5m' body='{"action": "Bullish I-BOS", "task": "price_action", "tf": "5m"}'
21:10:01  Context recorded: Bullish I-BOS (cat=EXECUTION dir=LONG cid=ibos_bull)
21:10:01  HTF_WOULD_PASS (tolerate-NEUTRAL) LONG 1H=NEUTRAL 15m=LONG 5m=LONG
21:10:02  [ENRICH] vol_snapshot written row=16856
21:10:03  [ENRICH] vol_snapshot written row=16857
21:10:12  weighted_adj: dir=LONG raw=4.25 adj=+0.6653 final=4.92     <- row 16857, WON
21:10:12  weighted_adj: dir=LONG raw=3.00 adj=+0.6653 final=3.67     <- row 16856, LOST
21:10:12  [ENTRY-GATE] concurrent LONG entry already in flight for SOL/USDT:USDT
                       — refused, not queued
21:10:17  [QTY] entry.live 1.310788 -> 1.3
21:10:22  OK: buy LONG 1.3 SOL/USDT:USDT @ 76.29
```

| | |
|---|---|
| webhooks in that second | **2** (`Bullish OB Created`, `Bullish I-BOS`) |
| entry rows created | **2** (16856, 16857) |
| **orders PLACED** | **1** — `989c90cf-e700-4195-89b4-9d291a051fe2` |
| **positions resulting** | **1** — vpos 30 |

**Only ONE `[QTY] entry.live` line appears.** That line is the race marker the 2026-08-08 finding
named: *"the marker of the race is `[QTY] entry.live` twice"*. **It appears once.** The venue's
execution list for that second confirms it — a single Buy 1.3, one orderId.

### (b) REFUSED, not queued — proven in the code AND on the row

```python
_gate = _entry_gate(symbol, position_side)
if not _gate.acquire(blocking=False):        # <- blocking=False IS the mechanism
```

`blocking=False` cannot queue: `acquire` returns `False` immediately and the thread takes the
refusal branch. Its own comment states the intent — *"A queued duplicate is the same defect with a
delay: it would wake seconds later, having missed nothing but the price, and place the second order
this exists to prevent."*

**And the losing thread left the record, not a silence:**

```
trades 16856 · status = 'entry_gate_refused'
             · order_id = NULL   · price = NULL   · amount = NULL
             · error = 'concurrent LONG entry already in flight for
                        SOL/USDT:USDT — refused, not queued'
```

`order_id` NULL is the second, independent proof that no order was placed on that thread. The row
also went to the Skip-Attribution Observatory. **There is no later retry of 16856 anywhere in the
journal — it was discarded, exactly as specified.**

🔴 **And the gate is taken BEFORE the position read, which is the whole point.** Its comment:
*"Not around the order: THE READ is the thing that goes stale. At 06:50 the cap was read at :02 and
the order left at :18, sixteen seconds later. Locking only the order would let both threads read
zero and then queue politely to place two."* Here the two threads were 9 seconds into their advisor
consults when the gate resolved them. **Locking the order alone would have placed two.**

### (c) 🔴 FIX 3 IS CLOSED.

**I state it plainly: fix 3 is proven in production.** The refusal branch — the one that could not be
scheduled, the one that needed two same-side webhooks in the same second, the exact race of 06:50
and 08:35 on 2026-08-08 — **has now fired eleven times since the flip**: 2 LONG on the 08-08
evening, 6 SHORT overnight, 3 LONG today (15:00 ×2, 15:45). **Zero duplicate orders and zero
duplicate positions across all eleven.** On the one occasion it guarded a real entry it produced
exactly one position with exactly one stop.

**All three morning fixes are now proven in production:** fix 1 (§1b, this entry), fix 2 (the `34040`
success mapping — **699 occurrences** in the journal since the 16:08:59 start, every one counted as
SET rather than as a failure, on vpos 29's stop resync), fix 3 (here).

🔶 **One residual, cosmetic but worth a line:** the digest's ladder does not know
`entry_gate_refused`, so every refusal lands in **"⚠️ UNCLASSIFIED STATUSES"** (8 of them in the
08:20 window). That bucket is
working exactly as designed — it exists to surface statuses neither of us thought of — but the
status is now understood, and it will keep reading as an anomaly until it is classified.

---

## 5. THE RESOLVER AND THE DIGEST

### (a) The resolver ran from cron at 08:19 — clean

`/var/log/mercury_sol_naked_alert_resolver.log`, complete contents after its first unattended run:

```
[2026-08-09T08:19:01.509450+00:00] naked_alert_resolver starting
  venue: LONG: size=1.3 sl=75.41 | SHORT: size=0.0 sl=NONE
  unresolved alerts: 0
  resolved 0; still unresolved: 0
```

**It fired at 08:19:01.5, 1.5 s after its cron minute. It read the venue over Tor successfully** —
`LONG: size=1.3 sl=75.41` is vpos 30, exactly right. **It wrote nothing, because there was nothing
to resolve.** Exit code is not in the log (the entry does not echo `$?`), but the "resolved N; still
unresolved: N" line is the **last** statement in `main()` and only prints on the success path — the
fail-closed branch returns before it with a different message. **It reached the end.** The 17:58
`env -i` rehearsal predicted this exactly.

`naked_position_alerts` today: **5 rows, all `resolved=1`, all stamped `2026-08-08T17:49:22`.**
No new row was written overnight and none was un-resolved. Idempotent as designed.

### (b) 🔴 ZERO unresolved alerts — but the NEEDS-HANDS block was NOT empty

**The alerts half: YES, zero.** No `naked_position_alerts` row reached the digest.

**But the block still fired, for two other reasons.** Reconstructed by running the digest's own
`build()` against a fixed 08:20 clock (rows are append-only, so the funnel is exact; the heartbeat
line reads the latest beat and cannot be rewound, so it is excluded from the quote):

```
🔴 NEEDS HANDS — READ THIS BEFORE THE FUNNEL
  ⚠️ stop failed → position closed       1 row(s) in window  [sl_failed_position_closed]
  ⚠️ entry failed                        2 row(s) in window  [failed]
  🚫 OPEN ROW vpos 30 · SOL/USDT:USDT LONG · LIVE · opened 2026-08-08T21:10:20.117232+00:00  ← 🔴 NO ALERT ROW for this open position
```

**Two findings here, and neither is an alert regression:**

1. **The two money-path lines are yesterday morning's incidents, correctly still inside a 24h
   window** ending 08:20 — the 06:50 and 08:35 failed entries and the failed stop. They age out on
   their own. **They are not new and nothing overnight caused them.**
2. 🔴 **The third line is a false alarm by construction.** A healthy, managed, correctly-stopped
   live position renders as a red `🚫 OPEN ROW … ← 🔴 NO ALERT ROW for this open position`. The
   cross-check at `silence_digest_sol.py:378` was written when an open row with no alert meant a
   **stale** row; it has no way to distinguish that from **the normal state of a bot holding a
   position**. Worse, `_open_rows` being non-empty also suppresses the `✅ NOTHING NEEDS HANDS`
   all-clear. **So for as long as the bot holds any position, the digest can never say "nothing
   needs hands", and will show a red 🚫 line saying the opposite.** Named, not fixed — read-only
   pass.

### (c) The funnel, verbatim, for the 08:20 window

🔴 **A correction to my own method before the numbers, because it changed them.** My first
reconstruction rewound the clock but not the query: `build()` selects `WHERE timestamp >= since`
with **no upper bound**, so a rewound "now" widened the window instead of moving it, and swept in
seven hours that the real 08:20 run could not have seen. Bounding the query at 08:20:01 — which is
what the real run's own `now` did for it — gives the faithful reproduction:

```
WHY IT WAS QUIET — per cause
  webhooks logged    210 rows → 137 market events (×1.53)
  ├─ bookkeeping      33  (slot writes, never an entry attempt)
  └─ entry attempts  158 rows → 115 events
       ├─ 1H trend not set         25
       ├─ HTF cascade vetoed       47
       ├─ score below threshold    44
       ├─ risk gate halted          9
       ├─ already in position       3
       └─ reached the advisor   30
             ├─ ADVISOR DECLINED           29  (97% of those)
             └─ EXECUTED                    1
  advisor declines: 29 rows → 29 events (×1.00; book-wide norm ×1.26)

EXIT SIDE
  exit armed                      2
  exit signal, nothing armed      4
  closes executed                 2

WHAT THE ADVISOR CITED (of 29 declines; one reason cites several)
  FLAT / ranging regime            29  (100%)
  tier disagreement                28  (97%)
  counter-trend vs HTF             24  (83%)
  EMA compression                  23  (79%)

⚠️ UNCLASSIFIED STATUSES (not in the ledger's ladder — shown so nothing is silently dropped)
  entry_gate_refused                8

VERDICT: not silent — 1 entry(ies) executed.
```

**Where every signal died: 115 entry-attempt events → 25 died with no 1H trend set, 47 at the HTF
cascade, 44 below the score threshold, 9 at the risk gate, 3 because a position was already open,
30 reached the advisor, and the advisor declined 29 of 30 (97%).** One executed — vpos 30. The two
closes are vpos 29's partial and its close.

🔴 **Read the advisor's own tally against §2: 100% of the 29 declines cited FLAT/ranging, and 97%
cited tier disagreement.** **The single entry that executed had BOTH conditions** — `market_regime =
FLAT` and a 1H tier that OPPOSES. It is the one that talked itself past both, in the very sentence
quoted in §2b: *"Market regime FLAT but confluence overcomes soft rule."* Whether that is judgement
or noise cannot be answered at n=1, and I am not going to pretend otherwise.

---

## 6. STATE AND HEALTH

### (a) Venue vs row, field by field — vpos 30

| field | **VENUE** | **ROW (vpos 30)** | |
|---|---|---|---|
| size | 1.3 | 1.3 | ✅ |
| entry | 76.29 | 76.29 | ✅ |
| stop | **75.41** | **75.41** | ✅ exact, no tick drift |
| positionIdx / side | 1 / Buy | LONG | ✅ |
| leverage | 5 | 5.0 | ✅ |
| tradeMode | 0 (**CROSS**) | — | ⚠️ unchanged, still cross margin |
| mark / uPnL | 76.841 / **+0.7163** | — | |
| curRealisedPnl | −0.11848343 | — | = entry fee 0.099177 + 2 funding (0.00938 + 0.00992) |
| **conditional order** | `46968bbe-3bef-4ae6-a52d-6a0b11882f9d` | 🔴 **NOT STORED** | see below |

**The stop order, in full:**

```
orderId 46968bbe-3bef-4ae6-a52d-6a0b11882f9d   Untriggered
  type=Market  stopOrderType=StopLoss  trigger=75.41  qty=1.3  reduceOnly=True  idx=1
  createdTime 1786223419195 = 2026-08-08 21:10:19.195 UTC
  updatedTime 1786223419195  <- NEVER MODIFIED since creation
```

**One stop, the original, untouched since 338 ms after the fill.** Exactly one conditional order
exists on the symbol. No orphan.

🔴 **And a gap worth naming: `active_positions` is a shell.** Its row for vpos 30 is:

```
symbol=SOL/USDT:USDT  position_side=LONG  entry_time=2026-08-08T21:10:22  entry_price=76.29
entry_row_id=NULL  amount=NULL  sl_price=NULL  sl_order_id=NULL
trail_active=0  breakeven_locked=0
```

**Four of the eleven columns are NULL, including `sl_order_id`.** So the venue's stop-order id lives
**nowhere on disk** — the only reason I can quote `46968bbe…` is that I asked the venue. The engine
does not need it (it drives the **position-level** SL field, per the B1 rule, never an order list),
so nothing is broken today. But `active_positions` reads like a live mirror and is not one, and the
next person to trust it will be misled. **`trail_active=0` / `breakeven_locked=0` happen to be
correct — the arm has not been reached — but they are correct by coincidence, not by update.**

### (b) Tracebacks, alerts, heartbeat

```
tracebacks since 2026-08-08 16:08:59  : 0   (grep -c "Traceback" = 0)
hands-required / naked alerts         : 0   (no new naked_position_alerts row; none since 15:40:43)
[ENTRY] fill read FAILED              : 0
[ENTRY] NO average price              : 0
[FEE] venue fee UNREADABLE            : 0
```

```
[HEARTBEAT] alive ticks=6708 (+25 in 312s) last_tick=12.2s max_tick=13.1s
            cadence=10s open=1 mode=LIVE pid=3533987     (15:22:26 UTC)
```

**Cadence steady at ~12.3 s against a 10 s target, max tick 13.1 s, open=1, mode=LIVE, uptime
23h 14m, NRestarts=0.** ~25 beats per 5 minutes, unbroken.

🔶 **ONE REAL HEALTH FINDING — 32 blind ticks, and the bot handled every one correctly.**

```
[ENGINE] vpos=30 position state UNKNOWN — no action this tick (Phase 1 semantics)

  2026-08-08 21h : 8      2026-08-09 10h : 8
  2026-08-08 22h : 3      2026-08-09 11h : 7
                          2026-08-09 12h : 1
                          2026-08-09 13h : 5      = 32 ticks
```

The cause is Bybit `retCode 10002` — the request's timestamp arrives outside the 5 000 ms
`recv_window`, because **the round trip through Tor exceeded five seconds**. The host clock is fine
(`System clock synchronized: yes`, NTP active); I reproduced the same failure from my own read
script and had to widen `recvWindow` to 60 s to get through. **The bot sets no `recvWindow` and no
`adjustForTimeDifference`, so it lives with the ccxt default of 5 s.**

**On every one of the 32 the bot did the right thing: `no action this tick`.** It never guessed, it
never closed, it never re-stopped. **But each is a tick where the trail, the breakeven arm and the
external-close detector could not evaluate** — 32 ticks ≈ 6.5 minutes of unmanaged time across 18
hours, in clusters of up to 8. **Named as a residual, not fixed. It is a one-line client option and
it is not a read-only change, so it waits for you.**

Also live and untouched: `EXIT_ARMED side=LONG` fired at **08:00:01** today and expired unfired at
**14:00:01** — vpos 30 came within one bearish 15m confirmation of being closed the same way vpos 29
was.

### (c) The pending-restart set — five files, disk-only, zero-behaviour. UNCHANGED.

```
PENDING (loaded by the bot, disk newer than the 16:08:59 start)
  config.py            2026-08-08 16:51:55
  virtual_trader.py    2026-08-08 16:51:55
  claude_advisor.py    2026-08-08 17:47:11
  skip_attribution.py  2026-08-08 17:47:11
  trail_arm.py         2026-08-08 17:47:11

NOT pending (standalone, cron re-reads each run)
  naked_alert_resolver.py  17:47:11    silence_digest_sol.py  17:47:11
```

**Still five. Every mtime identical to the 18:04 baseline — nothing has been edited since.** The
zero-behaviour claim stands on the same evidence as yesterday: AST-proven (`added=[] removed=[]
changed=[]`) for the three 17:47 files, and value-proven for `config.py` / `virtual_trader.py`
against the backups the running worker actually loaded. **The single known divergence is unchanged
and display-only** — `_adopt_card` would print the superseded formula string while computing the
same 0.0020 target.

🔴 **The restart is still blocked, and vpos 30 is why.** Restart only from flat.

### (d) Titan — untouched

```
HEAD            897850b  (unchanged)
git status      clean — zero modified, zero untracked
MainPID         2538048  ·  NRestarts=0
active since    2026-08-06 01:53:19 UTC   (79h, spanning this entire session and the last)
```

**Not read for state, not restarted, no worker touched. The only commands issued against
`/root/titan-bot` this session were `git log -1` and `git status --porcelain`, both reads.**

---

## WHAT I CHANGED: NOTHING

```
service       mercury-sol  active · pid 3533821 / worker 3533987 · since 16:08:59 · NRestarts=0
vpos 30       OPEN · LONG 1.3 @ 76.29 · sl 75.41 · wm 77.03 · uPnL +$0.72 · is_paper=0
venue         LONG 1.3 · stop 75.41 · order 46968bbe since 21:10:19 · SHORT flat
vpos 29       CLOSED 18:45:05 · booked +$1.6025 · VENUE PAID +$1.5779
alerts        5/5 resolved · 0 unresolved · nothing new overnight
cron          08:19 resolver ran clean · 08:20 digest delivered
pending       5 files, unchanged, awaiting a flat-book restart
titan         active · HEAD 897850b · git clean · NOT TOUCHED
```

Every venue call was a read. The DB was opened `mode=ro` for every query. The digest was run with
`--dry` (print-only; the script contains zero INSERT/UPDATE/DELETE/commit). No order was placed, no
file in `/mnt/volume_nyc1_1780480650620/mercury-sol` was written, no service was restarted.

---

## THE LEDGER — what closed, what opened

**CLOSED tonight:**
- ✅ **Fix 1** — `_read_entry_fill` completed a live entry, fill and fee verified against the venue.
- ✅ **Fix 3** — the refusal branch fired in production, ten times, zero duplicates.
- ✅ **All three morning fixes** are now proven live.
- ✅ The resolver survived its first unattended cron run; the digest reads zero alerts.

**OPENED tonight — four, in descending order of what they cost:**
1. 🔴 **`lookup_entry_for_close` prices a live close off the most recent `status='executed'` buy row
   with no `is_virtual` filter and no link to the position.** It told the Boss −$3.26 on a +$1.58
   trade. Report-only, and it will recur on every live close.
2. 🔴 **Funding is never booked.** −$0.0069 on vpos 29; vpos 30 has already paid $0.0193 unbooked.
   Recurs on every position held across a funding stamp.
3. 🔴 **`close_reason` on the first live close is `exchange_UNKNOWN`** — a self-closed market exit
   read back from the venue, which has no stop-order type for it. Both log lines name the exact
   one-line map to add.
4. 🔶 **32 blind ticks** from Tor latency exceeding the default 5 s `recv_window`. Fails safe every
   time; ~6.5 minutes unmanaged across 18 hours.

**Plus two cosmetic:** the "VIRTUAL Close / (paper — no real order)" label and the −$1 126.86
paper-mixed cumulative on live close cards; and the digest's permanent red 🚫 line for any open
position.

**And one finding that is neither closed nor new:** the advisor's book claim is **false for the
fourth time in four**. The canon written on 2026-08-08 — *`ai_reason` is narration, not mechanism* —
now has four for four behind it.
