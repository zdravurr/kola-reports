# Mercury-SOL — the duplicate is a ROW, not a CALL; the range still does not separate; and two things nobody asked about are broken

**2026-08-14 17:50 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · READ-ONLY THROUGHOUT — no file written, no restart, no order, no DB write.**

Titan (`/root/titan-bot`) was **not touched, not read for state, and none of its numbers imported.**

---

## ⚡ THE SHORT VERSION

1. **The duplicate is a DISPLAY ARTIFACT.** Over the last 7 days: **231 consultation ROWS = 222 model CALLS + 9 REUSES**. Calls per market state = **1.000 every single day since 2026-08-07**. It has not drifted back toward 2.20; it has not drifted at all.
2. **Every same-minute pair the operator can be seeing is one call.** 12 same-side pairs inside 120 s in the window; **11 of 12 carry a populated `ai_verdict_reuse_json`**. Rows-per-call is **1.041** now (it was 1.26 when measured) — because multi-alert states have become *rarer*, not because the cache stopped working.
3. **The one genuine second call is correct.** `#17969`/`#17972`, 2026-08-12 23:45:20, same second, same side, same wall, same 1H tier — and the **15m tier changed between them** (`Reversal Up` set 76 m ago → `HyperWave Signal Up` **set just now**; the 15m confirm is row `#17970`, written 59 ms after the first consultation started). A refreshed tier is a new market state by design.
4. **The wall MULTIPLE and the PERCENTILE did NOT leak into the key.** Verified in source: the key is a 5-tuple and neither is in it; `_wall_pctl` is called at exactly one site — the prompt renderer. The wall **price** moved in **0 of 9** same-tier pairs, exactly as in the 0-of-353 measurement that chose it.
5. **The relaxations' flip count is much larger than 3.** Canonically (system-prompt provenance): **42 flip-stamped rows = 41 distinct model flips ever** (17 aligned-LONG, 24 aligned-SHORT; one is a reuse of a flip). **12 became positions, ΣR −4.403, 4 winners of 12.** The four most recent — vpos 26, 27, 28, 32 — are **0 for 4, ΣR −2.078**.
6. **🔴 The range problem is still NOT filterable.** Both refused candidates re-run on the 29-position book: the EMA envelope separates at **p = 0.90**, the ADX+range pair at **p = 0.98**. Nothing in fifteen declared hypotheses clears **Bonferroni α = 0.00333**. The strongest thing in the pass **reverses sign between the paper era and the live era**.
7. **The composition question has an answer, and it points the other way.** Chop entries *do* share a thinner composition (raw score 3.25 vs 4.38, p = 0.044) — but a thin composition does **not** predict a loss (p = 0.69). The composition quantity that *does* track outcomes says **richer is worse** (≥3 categories contributing: n = 5, mean **−1.087R** vs −0.023R, p = 0.0158, survives day/hour/side/halves — and still fails Bonferroni).
8. **🔴 UNASKED, AND MATERIAL: the 2026-08-10 registry fix reports success when it fails.** Twice — vpos 34 and vpos 35 — the DELETE hit `database is locked`, the exception was swallowed one level below, and the caller printed **"cleared active_positions"** anyway. **The stale row is in the table right now.** The loud "🔴 FAILED to clear" Telegram alert is unreachable through this path.
9. **🔴 UNASKED, AND MATERIAL: the book gate has breached its own pre-registered red line.** Pre-registered LONG 2.20 % / SHORT 2.67 %, ratio 1.21×. Realised: **LONG 6.82 %, SHORT 23.17 %, ratio 3.40×.** The OPEN-ITEMS file names *"above 5 % on either side, or a side ratio above 2×"* as grounds to revisit. Both wires are tripped.
10. **A correction to the brief: vpos 32 is not open.** It closed 2026-08-10 19:45:18 (`exit_signal`, −0.180R). The book is **flat** as of 15:30:13 today; vpos 35 was stopped out.

---

## 0. WHAT I MEASURED ON, AND WHAT I DID NOT USE

| item | source |
|---|---|
| consultations, positions, book gate | `/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db`, opened `file:…?mode=ro` |
| candles | Bybit SOLUSDT perp via Tor (`socks5h://127.0.0.1:9050`), fetched 2026-08-14: **2,922 × 1h · 11,686 × 15m · 35,057 × 5m** from 2026-04-15 |
| live behaviour | `journalctl -u mercury-sol` (retained back to 2026-08-12 16:35 only) |
| code facts | `claude_advisor.py`, `main.py`, `virtual_trader.py`, `config.py` read on disk |
| **`market_regime`** | **NOT USED ANYWHERE.** It is signal presence, not a measurement, exactly as the brief says |
| **Titan** | **not read, not touched, no numbers imported** |
| **files modified in `mercury-sol`** | **NONE.** No restart. No order. No DB write. |

**Measurement pipeline validated before anything was concluded from it.** My independent ADX/ER/ATR/range code reproduces the published 2026-08-07 figures for the three reference entries:

```
              published (2026-08-07)          mine (today, fresh candles)
vpos 26  ADX 29.9  ER4h 0.451  ER12h 0.192    29.9   0.451   0.192   range 4.07% (4.07)
vpos 27  ADX 15.5  ER4h 0.223  ER12h 0.271    15.5   0.223   0.271   range 2.33% (2.32)
vpos 28  ADX 13.2  ER4h 0.217  ER12h 0.257    13.2   0.217   0.257   range 2.64% (2.64)
book median ADX 25.7                          25.65      vpos 26 = 73rd pct → 76th
```

The one number that does not reproduce is `pos in 24h range` for vpos 27 (published 0.15, mine **−0.05** — the entry is *below* the 24 h low on my candles). Both readings say the same thing ("shorting at the bottom of the range"); the definition is stated in §2.1 so the difference is inspectable rather than hidden.

---

# PART 1 — THE DUPLICATE ADVISOR CALLS

## 1a. Calls per market state, BY DAY. It is 1.00, and it has been since 2026-08-07

The state key is reconstructed from stored columns exactly as the live code builds it — `(symbol, direction, 1H slot identity, 15m slot identity, nearest opposing wall PRICE)` — with the live 60 s TTL and a tier-refresh split.

| day | consultation ROWS | market STATES | model CALLS | REUSES | **calls/state** | rows/call |
|---|---|---|---|---|---|---|
| 2026-08-03 | 46 | 36 | 46 | 0 | **1.278** | 1.000 |
| 2026-08-04 | 97 | 71 | 97 | 0 | **1.366** | 1.000 |
| 2026-08-05 | 76 | 56 | 76 | 0 | **1.357** | 1.000 |
| 2026-08-06 *(dedup applied 12:20)* | 87 | 73 | 83 | 4 | **1.137** | 1.048 |
| 2026-08-07 | 24 | 22 | 22 | 2 | **1.000** | 1.091 |
| **2026-08-08** | 37 | 28 | 28 | 9 | **1.000** | 1.321 |
| **2026-08-09** | 34 | 34 | 34 | 0 | **1.000** | 1.000 |
| **2026-08-10** | 15 | 15 | 15 | 0 | **1.000** | 1.000 |
| **2026-08-11** | 61 | 61 | 61 | 0 | **1.000** | 1.000 |
| **2026-08-12** | 18 | 18 | 18 | 0 | **1.000** | 1.000 |
| **2026-08-13** | 41 | 41 | 41 | 0 | **1.000** | 1.000 |
| **2026-08-14** | 25 | 25 | 25 | 0 | **1.000** | 1.000 |

**Last 7 days: 231 rows, 222 calls, 9 reuses — 1.000 calls per state, every day.**

🔴 **The honest reading is not "the fix is holding brilliantly."** From 2026-08-09 onward, **states = rows**: almost no market state produces more than one consultation any more. The cache has had nothing to do since 2026-08-08. Whatever the operator is looking at, it is **not** a per-state duplication that reappeared — the per-state number never moved off 1.00 after 08-07.

## 1b. The actual duplicates — every same-side pair inside 120 s in the window

**12 pairs. 11 carry a reuse. 1 is two genuine calls.**

| pair | when | gap | side | what it is |
|---|---|---|---|---|
| #16664 → #16665 | 08-08 00:20:06 | 1 s | LONG | **REUSE** |
| #16685 → #16689 → #16690 | 08-08 03:20:00 | 1 s, 2 s | SHORT | **REUSE** (3 rows, 1 call) |
| #16694 → #16695 → #16696 | 08-08 03:35:00 | 0 s, 1 s | SHORT | **REUSE** (3 rows, 1 call) |
| #16697 → #16698 | 08-08 03:40:00 | 1 s | SHORT | **REUSE** |
| #16700 → #16701 | 08-08 03:50:00 | 1 s | SHORT | **REUSE** |
| #16748 → #16749 | 08-08 06:50:02 | 0 s | LONG | **REUSE** (both `execute`) |
| #16765 → #16766 | 08-08 08:35:01 | 0 s | LONG | **REUSE** (both `execute`) |
| **#17969 → #17972** | **08-12 23:45:20** | **0 s** | **LONG** | **TWO MODEL CALLS** |

Same-minute clustering by side, for completeness (the shape an operator sees on a card feed):

```
2026-08-08 03:20 SHORT  16685 REUSE | 16689 CALL | 16690 REUSE      3 rows, 1 call
2026-08-08 03:35 SHORT  16694 CALL  | 16695 REUSE| 16696 REUSE      3 rows, 1 call
2026-08-08 06:50 LONG   16748 CALL  | 16749 REUSE                   2 rows, 1 call
2026-08-08 08:35 LONG   16765 REUSE | 16766 CALL                    2 rows, 1 call
2026-08-12 23:45 LONG   17969 CALL  | 17972 CALL                    2 rows, 2 calls
```

## 1c. So: ROWS, not CALLS — and here is the ratio

**They are working exactly as designed, and the operator is seeing ROWS.**

```
rows per call, last 7 days   231 / 222 = 1.041      (it was 1.26 when measured)
rows per call, 08-08 alone    37 /  28 = 1.321
model calls saved by the cache, last 7 days:  9
```

The ratio **fell** from 1.26 to 1.041 — not because reuse stopped, but because SOL stopped producing multi-alert states after 08-08. On the one day in the window that *did* produce them (08-08), the ratio was **1.321**, i.e. the mechanism did *more* work than the 1.26 baseline.

## 1d. What busts the key — and it is not the multiple and not the percentile

**Checked in source, not inferred.** `claude_advisor.py:838`:

```python
_state_key = (symbol, _dir_key, _slot_identity(_h1), _slot_identity(_m15),
              _near_opposing)
```

Five fields. `_near_opposing` is `w['price']` and nothing else (`claude_advisor.py:824-833`). Searching the whole module:

```
grep -n "_wall_pctl" claude_advisor.py
  339:  def _wall_pctl(mult):          <- the definition
  404:      _p = _wall_pctl(w.get('mult'))   <- ONE call site, inside _format_pre_trade_walls
```

**The percentile exists only in the rendered prompt. The multiple exists only in the rendered prompt.** Neither has a path into the key. This is not an accident of the new fields — it is the 2026-08-06 decision holding: **the key is deliberately not on prompt text**, which is precisely why the per-wall percentile, the dual stale-tier tally, the changing `n=23,080` wall-population counter, the taker-fee change and the book gate could all be added without touching it.

**And the wall price — the one book-derived field that *is* in the key — is still stable:**

```
same-tier same-side consultation pairs within 60 s, live era: 9
wall price IDENTICAL in 9 of 9 (moved in 0)
```

Same result as the 0-of-353 measurement that chose price over multiple.

**The one genuine second call, in full:**

```
#17969  23:45:20.856  LONG  1H: Trend Catcher Down (SHORT, 8.8h, STALE)
                            15m: Reversal Up        (LONG,  set 76m ago)
                            5m:  Bullish OB Created
                            mid 75.52  nearest opposing ask wall $75.75
                            -> skip 0.xx  "FLAT market (1h ADX 14.8) + thick ask wall $75.75 (p99)"

#17970  23:45:20.916  15m_confirm recorded          <-- THE 15m TIER IS REWRITTEN HERE, 59 ms LATER

#17972  23:45:20.960  LONG  1H: Trend Catcher Down (SHORT, 8.8h, STALE)   <- same
                            15m: HyperWave Signal Up (LONG, set JUST NOW) <- CHANGED
                            5m:  Within Bullish OB
                            mid 75.52  nearest opposing ask wall $75.75   <- same
                            -> skip  "FLAT regime + 1h BEAR trend opposes entry"
```

🔴 **The key was busted by the 15m tier, and that is the key doing its job.** A tier that is refreshed inside the 60 s window *should* start a new state and *should* be asked again — test T2 of the 2026-08-06 pass exists for exactly this. The second call was made on a materially different market state that arrived 104 ms after the first consultation began. **There is no defect here.**

## 1e. The aligned relaxations — the flip count, updated

The canonical identification is the one the 2026-08-02 pass established: **a flip is a row whose `ai_system_prompt` is byte-identical to `_ENTRY_SYSTEM_V2_ALIGNED` / `_ENTRY_SYSTEM_V2_ALIGNED_SHORT`**, because `_verdict_system` is replaced *only* on a flip. Hashed against the live constants today:

```
_ENTRY_SYSTEM              156c7ac7   3,408 rows   (the base prompt)
_ENTRY_SYSTEM_V2_ALIGNED   17720bff      17 rows   ALL 'execute'  -> aligned-LONG flips
_ENTRY_SYSTEM_V2_ALIGNED_S cc6a1bd7      25 rows   ALL 'execute'  -> aligned-SHORT flips
379c67c9 (2,809 chars, 06-20→06-26, 153 rows, 127 skip + 26 execute)
        = a SUPERSEDED June prompt, NOT a flip stamp — counting it would inflate the flips 5×
```

**42 flip-stamped rows. One of them (#16444) is a REUSE of a flip, so distinct model flips = 41** (17 LONG-arm, 24 SHORT-arm). **Twelve became positions:**

| vpos | arm | R | | vpos | arm | R |
|---|---|---|---|---|---|---|
| 16 | LONG | −1.146 | | 24 | SHORT | −1.050 |
| 17 | SHORT | +0.004 | | 25 | SHORT | **+1.257** |
| 18 | LONG | −1.074 | | **26** | LONG | **−1.085** |
| 19 | SHORT | +0.463 | | **27** | SHORT | **−0.660** |
| 21 | LONG | +0.285 | | **28** | SHORT | **−0.153** |
| 22 | LONG | −1.064 | | **32** | SHORT | **−0.180** |

```
ALL 12 flip-positions            ΣR −4.403     4 winners / 12   (33.3%)
the FOUR most recent (26,27,28,32) ΣR −2.078   0 winners /  4   (0.0%)
whole book for comparison (29)   ΣR −5.985    10 winners / 29   (34.5%)
```

🔴 **The brief's "3 ever, both positions LOST" was the state of the ledger on 2026-08-03** (flips #15093, #15410, #15412 — two became vpos 26 and 27). **Since then: 7 more flips, 2 more positions, vpos 28 (−0.153R) and vpos 32 (−0.180R) — both also LOSSES.** The relaxation-position record is now **0 for 4** since the ×20 ceiling era began.

**What the relaxations cost in calls — reconstructed and then PROVEN against the live log.** The deterministic gate is recomputable from stored columns (`side`, `trend_1h`, `srv_adx_1h`, plus the overhead-wall ×20 ceiling from `advisor_book_json`). On 2026-08-14 my reconstruction predicts exactly four extra SHORT-arm calls:

```
predicted  18316 09:45 adx 13.41 | 18327 11:20 adx 15.45 | 18329 11:40 adx 15.45 | 18337 12:35 adx 16.46
journal    09:45:20 HELD adx1h=13.4 | 11:20:16 adx1h=15.5 | 11:40:20 adx1h=15.5 | 12:35:20 adx1h=16.5
                                         4 predicted, 4 logged, ADX matches to the decimal
```

On that footing:

```
last 7 days   222 base calls + 11 relaxation calls = 233 total   (+5.0%, 1.57 extra calls/day)
all time      3,606 base calls + 713 relaxation calls           (+19.8%)
              -> 713 extra calls have bought 41 flips, 12 positions, ΣR −4.403
the ×20 ceiling has SUPPRESSED an override exactly ONCE, ever (2026-08-11)
```

**A cache hit correctly does not re-fire the relaxation** — confirmed in code (`claude_advisor.py:1111`, the store happens after the aligned block, so a reuse carries the flipped verdict *and* its system prompt), and confirmed in data (#16444 is a reuse carrying an aligned stamp).

---

# PART 2 — IS IT ENTERING RANGES?

## 2.0 🔴 THE DECLARATIONS, IN THE HEADER, BEFORE ANY NUMBER

**Fifteen hypotheses were fixed before the outcomes were inspected. Bonferroni α = 0.05 / 15 = 0.00333.**

> H1 EMA envelope (both Expanding) · H2 ADX ≥ 20 AND 24h-width pctl ≥ 20 · H3 ADX(1h,200) ≥ 20 · H4 24h width ≥ median · H5 ER(4h) · H6 ER(12h) · H7 ATR/14d-median · H8 |pos-in-24h − 0.5| · H9 ≥3 categories contributing · H10 no intra-conflict · H11 MOMENTUM zeroed by intra-conflict · H12 15m tier absent · H13 top-category share · H14 raw direction score · H15 raw score ≤ 2.75

**Every test is a two-sided permutation test on the difference in mean R (200,000 shuffles).** Anything that separates is then re-tested **day-clustered** (labels permuted at the day level), **hour-residualised** (R centred within 6-hour buckets), **side-residualised**, and **split in half by time** — per §2.54. **Twenty-two filters have died on this book. Nothing here gets a lower bar.**

**One structural caveat, stated rather than buried:** `TRAIL_MULT_ATR` changed 2.5 → 1.875 (1.00R → 0.75R giveback) around 2026-08-06, so realised R for vpos ≥ 28 comes from a slightly different exit geometry than vpos 7–27. 1R itself (the original stop distance) did not change, so the R-multiples pool; the *upside tail* is clipped for the newer trades, which if anything biases the recent half **downward**.

## 2a. The tape at EVERY entry — measured independently of the bot's labels

**Definitions (so the numbers travel with their provenance).** ADX = Wilder ADX(14) over the **200 CLOSED 1h bars before the entry bar** (entry bar excluded). ER = Kaufman `|net| / Σ|Δ|`, 4h from 48 × 5m closes, 12h from 48 × 15m closes. ATR = Wilder ATR(14) on 1h at entry ÷ the median of the same series over the prior 336 bars. `pos24` = `(price − low₂₄ₕ)/(high₂₄ₕ − low₂₄ₕ)` over the 24 closed 1h bars. **`ADXpct` / `wpct` = that entry's percentile within the CONTEMPORANEOUS 30-day tape** (all closed 1h bars in the preceding 30 days) — the measure that answers "was this an unusual moment, or just Tuesday?"

| vpos | side | era | opened (UTC) | R | ADX | ADXpct | 24h w% | wpct | pos24 | |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 | LONG | paper | 06-14 23:50 | +2.089 | 29.5 | 58 | 5.37 | 66 | 1.07 | |
| 8 | LONG | paper | 06-20 07:00 | −0.739 | 27.9 | 56 | 6.43 | 70 | 0.90 | |
| 9 | LONG | paper | 06-21 02:50 | −0.264 | 39.3 | 78 | 6.59 | 72 | 0.80 | |
| 10 | SHORT | paper | 06-22 00:00 | −1.066 | 30.0 | 55 | 3.38 | 14 | 0.14 | |
| 11 | SHORT | paper | 06-23 00:30 | +1.133 | 15.8 | 10 | 5.35 | 55 | 0.08 | |
| 12 | LONG | paper | 06-24 02:25 | −1.049 | 39.5 | 76 | 5.69 | 60 | 0.38 | |
| 13 | SHORT | paper | 06-24 13:25 | +1.337 | 25.4 | 43 | 3.05 | 8 | 0.14 | |
| 14 | SHORT | paper | 06-25 14:00 | −1.032 | 19.3 | 18 | 8.74 | 87 | 0.16 | |
| 15 | SHORT | paper | 07-08 05:05 | +0.140 | 23.2 | 44 | 5.84 | 63 | 0.09 | |
| 16 | LONG | paper | 07-10 08:30 | −1.146 | 25.9 | 53 | 2.82 | 2 | 0.97 | |
| **17** | SHORT | paper | 07-13 03:10 | +0.004 | **18.8** | **24** | **3.15** | **9** | 0.05 | **RANGE** |
| 18 | LONG | paper | 07-14 15:45 | −1.074 | 26.3 | 55 | 4.83 | 49 | 0.92 | |
| 19 | SHORT | paper | 07-16 00:25 | +0.463 | 23.7 | 47 | 2.76 | 4 | 0.08 | |
| 20 | SHORT | paper | 07-17 13:40 | −1.124 | 32.5 | 79 | 3.68 | 31 | −0.21 | |
| 21 | LONG | paper | 07-19 06:50 | +0.285 | 27.4 | 61 | 2.77 | 7 | 0.75 | |
| 22 | LONG | paper | 07-21 03:10 | −1.064 | 25.4 | 55 | 3.70 | 40 | 1.02 | |
| 23 | SHORT | paper | 07-28 11:05 | −0.577 | 36.5 | 88 | 6.47 | 92 | 0.04 | |
| 24 | SHORT | paper | 07-29 20:05 | −1.050 | 21.7 | 34 | 2.52 | 17 | 0.00 | |
| 25 | SHORT | paper | 08-01 17:20 | +1.257 | 23.6 | 44 | 1.45 | 1 | 0.07 | |
| 26 | LONG | paper | 08-02 05:00 | −1.085 | 29.9 | 71 | 4.07 | 78 | 1.00 | |
| **27** | SHORT | paper | 08-03 06:45 | −0.660 | **15.5** | **11** | **2.33** | **14** | −0.05 | **RANGE** |
| **28** | SHORT | paper | 08-06 19:00 | −0.153 | **13.2** | **12** | **2.64** | **27** | 0.05 | **RANGE** |
| 29 | LONG | **live** | 08-08 08:50 | **+1.355** | 31.9 | 83 | 3.01 | 44 | 0.86 | |
| 30 | LONG | **live** | 08-08 21:10 | **+0.762** | 52.9 | 100 | 4.29 | 90 | 0.84 | |
| 31 | LONG | **live** | 08-10 08:10 | −1.155 | 31.4 | 75 | 2.27 | 20 | 0.50 | |
| 32 | SHORT | **live** | 08-10 15:15 | −0.180 | 23.6 | 49 | 2.30 | 22 | 0.06 | |
| 33 | LONG | **live** | 08-11 22:00 | −0.049 | 27.3 | 62 | 2.44 | 27 | 1.04 | |
| **34** | SHORT | **live** | 08-13 16:40 | −0.643 | **12.7** | **11** | **1.78** | **7** | −0.04 | **RANGE** |
| **35** | SHORT | **live** | 08-14 14:20 | −0.701 | **17.6** | **26** | **2.01** | **15** | 0.07 | **RANGE** |

**Book: n = 29, ΣR −5.985, win 34.5 %.** Paper 22 at −5.374; **live 7 at −0.611, win 28.6 %.**

### 🔴 IS IT SELECTING RANGES? Half yes, half no — and the halves matter

If entries were timed at random, these percentiles would be uniform on [0, 100].

| quantity | mean pctl (all 29) | median | bottom third | top third | vs uniform |
|---|---|---|---|---|---|
| **ADX(1h,200)** | **50.8** | 54.9 | 24.1 % | 27.6 % | **p = 0.877 — indistinguishable from random** |
| **24h range width** | **37.6** | 27.1 | **55.2 %** | 20.7 % | **p = 0.0204 — biased NARROW** |
| ADX, live 7 only | 57.9 | 61.5 | 28.6 % | 42.9 % | p = 0.478 |
| width, live 7 only | 32.2 | 21.9 | **71.4 %** | 14.3 % | p = 0.102 |

**The bot does NOT pick low-ADX moments** — its entries land uniformly across the ADX distribution of its own tape. **It DOES pick narrow-range moments**: 55 % of all entries and 71 % of live entries sit in the bottom third of the contemporaneous 24 h-width distribution. (Nominal at 0.05; it does **not** clear α = 0.00333, and it is a *selection* statement, not an outcome claim.)

**And the tape itself has compressed, which is the larger half of the answer:**

```
median 24h range width, unconditional, by ISO week
  W25  5.53%   W26  6.65%   W27  5.30%   W28  3.43%   W29  3.51%
  W30  2.71%   W31  3.14%   W32  2.65%   W33  2.46%     <- the live era
median ADX(1h,200)
  W25 30.8  W26 24.1  W27 23.0  W28 21.9  W29 26.2  W30 25.0  W31 24.3  W32 18.6  W33 20.9
```

🔴 **SOL is in a range right now. The bot is trading it. That is not the same as the bot preferring ranges** — on the measure that actually defines chop (ADX) its timing is random, and the narrowness it does select for is mostly the market's, not the bot's.

## 2b. Which entries were genuinely range entries, and what each realised

**Pre-stated rule: RANGE = ADX percentile < 33 AND 24h-width percentile < 33, both against the contemporaneous 30-day tape.** Five of 29.

| vpos | side | ADX (pctl) | width (pctl) | pos24 | **R** | how it died |
|---|---|---|---|---|---|---|
| 17 | SHORT | 18.8 (24) | 3.15 % (9) | 0.05 | **+0.004** | sl, after 33 h |
| 27 | SHORT | 15.5 (11) | 2.33 % (14) | −0.05 | **−0.660** | sl |
| 28 | SHORT | 13.2 (12) | 2.64 % (27) | 0.05 | **−0.153** | exit_signal, 11 h inside a 0.9 % band |
| **34** | SHORT | 12.7 (11) | 1.78 % (7) | −0.04 | **−0.643** | **sl, 32 minutes** |
| **35** | SHORT | 17.6 (26) | 2.01 % (15) | 0.07 | **−0.701** | **sl, 70 minutes** |

```
RANGE   n= 5   ΣR −2.152   mean −0.430   win 20.0%
OTHER   n=24   ΣR −3.832   mean −0.160   win 37.5%
        Δ = −0.271R   p = 0.574   (day-clustered p = 0.568)
```

🔴 **All five are SHORT. All five are shorts taken at the bottom of the range** (`pos24` between −0.05 and +0.07). Four of the five lost; the fifth was a scratch. **Two of the five are the two newest live positions**, taken yesterday and today, and they died in 32 and 70 minutes.

**The pattern is real to the eye and absent from the statistics.** −0.430R vs −0.160R on n = 5 is p = 0.574 — you would see a gap that size or larger **57 times in 100** by shuffling the labels.

## 2c. 🔴 RE-RUNNING THE TWO REFUSED CANDIDATES ON THE BOOK AS IT NOW STANDS

### Candidate 1 — the EMA envelope (both 1h and 15m `Expanding`)

**29-position book, live positions included.** vpos 8 still has a NULL `ema_gap_dir_15m` and cannot satisfy the rule, so the strict gate refuses it — it is counted in the refused column and named as unevaluable rather than dropped:

| cohort | n | win | ΣR | mean R | vpos |
|---|---|---|---|---|---|
| admitted | 12 | 33.3 % | **−2.791** | −0.233 | 11,14,17,19,20,25,27,28,**31,32,34,35** |
| refused | 17 | 35.3 % | **−3.194** | −0.188 | 7,8,9,10,12,13,15,16,18,21,22,23,24,26,**29,30,33** |
| | | | | **Δ = −0.045R, p = 0.902** | |

| per side | n | ΣR | win |
|---|---|---|---|
| **LONG admitted** | **1** (vpos 31) | **−1.155** | **0.0 %** |
| LONG refused | 12 | −1.978 | 33.3 % |
| SHORT admitted | 11 | −1.636 | 36.4 % |
| SHORT refused | 5 | −1.216 | 40.0 % |

**Three things changed, none of them in the gate's favour:**

1. **The LONG side-ban has technically broken — and it broke onto a loser.** It was **0 of 9** LONGs admitted; it is now **1 of 13** (7.7 %), and that one LONG is **vpos 31, −1.155R**. The 2026-08-07 verdict *"`if side == LONG: refuse` wearing an indicator's clothes"* still stands: one admission in 13 does not make a filter.
2. **The SHORT side flipped direction.** On 2026-08-07 admitted SHORTs were the better half (−0.11R vs −1.22R). With four more live SHORTs the admitted half is now **worse per trade** (−0.149 vs −0.243 mean, and the gate admits all four of the newest SHORTs: 32, 34, 35 and refuses none of them).
3. **It still admits every chop entry.** vpos **27, 28, 34, 35** — four of the five measured range entries — are all **ADMITTED**. It refuses vpos 17 only.

**p = 0.902. Effect size d = −0.05. Required sample for that effect to clear α = 0.00333 at 80 % power: ≈ 31,000 positions ≈ 69 years at the live rate. It does not separate. It has never separated. It is refuted again.**

### Candidate 2 — the ADX + range pair (`ADX(1h,200) ≥ 20 AND 24h-width percentile ≥ 20`)

**Reproduction fidelity, stated first.** The 2026-08-07 22:30 pass reported **7 refused at +2.329R / 15 kept at −7.704R** on the 22-position book. My reconstruction refuses **6–8** depending on the percentile base, at ΣR between **−0.04 and +0.55**. The divergence is two boundary entries: **vpos 14** (my ADX 19.3; theirs ≥ 20, inferable from their own quartile table) and **vpos 21/24** (whose relative 24 h-width ranking differs under my definition). I could not reproduce their exact refusal set, and I am not going to pretend I did.

**So I am not resting the answer on one threshold pair. Here is the whole surface — ΣR of the KEPT book, 29 positions, book = −5.985R:**

| | width pctl ≥ 0 | ≥ 10 | ≥ 20 | ≥ 30 | ≥ 40 |
|---|---|---|---|---|---|
| **ADX ≥ 0** | −5.985 | −5.898 | −3.903 | −2.652 | −2.254 |
| **ADX ≥ 16** | −5.662 | −6.218 | −4.883 | −3.785 | −3.387 |
| **ADX ≥ 18** | −4.961 | −6.218 | −4.883 | −3.785 | −3.387 |
| **ADX ≥ 20** | −3.933 | −5.190 | **−3.855** | −2.757 | −2.359 |
| **ADX ≥ 22** | −2.883 | −4.140 | −2.805 | −2.757 | −2.359 |
| **ADX ≥ 24** | −4.564 | −4.564 | −3.409 | −3.360 | −2.499 |

**The surface is non-monotone in both axes** — ADX ≥ 16 and ≥ 18 are *worse* than no filter at all, ADX ≥ 24 is worse than ADX ≥ 22. That is the signature of noise, not of a threshold.

**And at the pre-registered pair (ADX ≥ 20, width pctl ≥ 20):**

| | n | win | ΣR | **mean R** |
|---|---|---|---|---|
| kept | 19 | 36.8 % | −3.855 | **−0.203** |
| refused | 10 | 30.0 % | −2.130 | **−0.213** |
| whole book | 29 | 34.5 % | −5.985 | −0.206 |

🔴 **Read the mean column, not the ΣR column. −0.203 versus −0.213. p = 0.978.** The gate's entire apparent "improvement" (−5.985 → −3.855) is **volume**: it removes ten trades whose average outcome is identical to the ten it keeps. **It is not a filter. It is a 34 % reduction in trading, dressed as an edge.** Any rule that refused ten trades at random would show the same ΣR improvement in expectation.

**Per side, and the era split that would have been the temptation:**

| | n | ΣR | vpos |
|---|---|---|---|
| LONG kept | 12 | −1.978 | 7,8,9,12,16,18,21,22,26,29,30,33 |
| LONG refused | 1 | −1.155 | 31 |
| SHORT kept | 7 | −1.877 | 10,13,15,19,20,23,24 |
| SHORT refused | 9 | −0.975 | 11,14,17,25,27,28,32,34,35 |
| **LIVE ERA ONLY: kept** | **3** | **+2.068** | 29,30,33 |
| **LIVE ERA ONLY: refused** | **4** | **−2.679** | 31,32,34,35 |

🔴 **In the live era alone the pair looks magnificent: it keeps every winner and refuses every loser, ΣR +2.068 kept vs −2.679 refused.** On the paper era it is neutral-to-harmful. **That is a sign reversal between the halves of the same window on n = 7** — the exact failure mode the brief names, and the exact reason §2.54 exists. **I am recording it as evidence AGAINST the gate, not for it.** Three consecutive book findings have died here; this would be the fourth if it were promoted.

**Required sample for the observed effect (d = +0.011) to clear α at 80 % power: ≈ 742,000 positions.** In plain words: **the effect is zero.**

## 2d. 🔴 THE THIRD QUANTITY — COMPOSITION. It exists. It points the WRONG way.

The 2026-08-10 LONG is row **#17201 / vpos 31**, and the brief describes it exactly:

```
TREND      contribution 2.50   signal_count 1     <- half the score, from ONE 1H signal
MOMENTUM   contribution 0.00   signal_count 2     <- intra_conflict TRUE: HyperWave Up AND Down together
LIQUIDITY  contribution 0.00   signal_count 0     <- absent
EXECUTION  contribution 2.00   signal_count 1     <- one 5m signal
                    raw direction score = 4.50  against a 2.0 bar
prompt:  "15m: n/a (direction: n/a, age unknown)"  <- NO 15m TIER AT ALL
outcome: −1.155R, stopped out in 7h 12m
(the stored confluence_score of 6.00 is the MACRO-GATED figure; 4.50 is the price-only sum)
```

**Measured across all 29, for the first time:**

| vpos | side | R | raw | nz | intra | absent | top % | 15m tier | |
|---|---|---|---|---|---|---|---|---|---|
| 7 | LONG | +2.089 | 5.00 | 2 | 2 | 0 | 50 | HyperWave Signal Up | |
| 8 | LONG | −0.739 | 4.75 | 2 | 1 | 1 | 53 | HyperWave Signal Up | |
| 9 | LONG | −0.264 | 4.00 | 2 | 2 | 0 | 56 | HyperWave Signal Up | |
| 10 | SHORT | −1.066 | 6.00 | **3** | 1 | 0 | 42 | HyperWave Signal Down | |
| 11 | SHORT | +1.133 | 3.75 | 2 | 2 | 0 | 67 | HyperWave Signal Down | |
| 12 | LONG | −1.049 | 3.75 | 2 | 2 | 0 | 67 | Bearish Divergence | |
| 13 | SHORT | +1.337 | 4.25 | 2 | 1 | 1 | 59 | HyperWave Signal Down | |
| 14 | SHORT | −1.032 | 3.75 | 2 | 1 | 0 | 67 | **n/a** | |
| 15 | SHORT | +0.140 | 4.25 | 2 | 1 | 1 | 59 | HyperWave Signal Down | |
| 16 | LONG | −1.146 | 5.75 | **3** | 1 | 0 | 39 | HyperWave Signal Up | |
| 17 | SHORT | +0.004 | 3.75 | 2 | 1 | 1 | 67 | **n/a** | RANGE |
| 18 | LONG | −1.074 | 6.25 | **3** | 0 | 0 | 40 | HyperWave Signal Up | |
| 19 | SHORT | +0.463 | 4.25 | 2 | 1 | 0 | 59 | HyperWave Signal Down | |
| 20 | SHORT | −1.124 | 3.00 | 2 | 2 | 0 | 58 | **n/a** | |
| 21 | LONG | +0.285 | 4.75 | 2 | 1 | 0 | 53 | HyperWave Signal Up | |
| 22 | LONG | −1.064 | 5.75 | **3** | 1 | 0 | 39 | HyperWave Signal Up | |
| 23 | SHORT | −0.577 | 3.50 | 2 | 1 | 1 | 50 | HyperWave Signal Down | |
| 24 | SHORT | −1.050 | 5.00 | 2 | 1 | 0 | 50 | HyperWave Signal Down | |
| 25 | SHORT | **+1.257** | **1.75** | **1** | 1 | 2 | **100** | HyperWave Signal Down | |
| 26 | LONG | −1.085 | 5.50 | **3** | 0 | 1 | 45 | HyperWave Signal Up | |
| 27 | SHORT | −0.660 | 2.50 | **1** | 2 | 1 | **100** | HyperWave Signal Down | RANGE |
| 28 | SHORT | −0.153 | 4.00 | 2 | 1 | 1 | 56 | **n/a** | RANGE |
| 29 | LONG | +1.355 | 4.50 | 2 | 1 | 1 | 56 | HyperWave Signal Up | |
| 30 | LONG | +0.762 | 4.25 | 2 | 0 | 2 | 59 | HyperWave Signal Up | |
| **31** | LONG | −1.155 | 4.50 | 2 | 1 | 1 | 56 | **n/a** | |
| 32 | SHORT | −0.180 | 4.25 | 2 | 1 | 0 | 59 | HyperWave Signal Down | |
| 33 | LONG | −0.049 | 2.50 | **1** | **3** | 0 | **100** | HyperWave Signal Up | |
| 34 | SHORT | −0.643 | **1.75** | **1** | 1 | 2 | **100** | HyperWave Signal Down | RANGE |
| 35 | SHORT | −0.701 | 4.25 | 2 | 1 | 1 | 59 | HyperWave Signal Down | RANGE |

*nz = categories contributing non-zero · intra = categories zeroed by intra-conflict · absent = categories with zero signals · top % = share of the raw score from the single largest category*

**The distributions, never measured before:**

```
categories contributing non-zero :  1 -> 4 entries   2 -> 20 entries   3 -> 5 entries   4 -> 0 entries
categories zeroed by INTRA-conflict: 0 -> 3   1 -> 19   2 -> 6   3 -> 1
15m tier ABSENT from the prompt  :  5 of 29 (17.2%) — vpos 14, 17, 20, 28, 31
MOMENTUM zeroed by intra-conflict: 13 of 29 (44.8%)
MOMENTUM contributed nothing at all: 14 of 29 (48.3%)
```

🔴 **Not one entry in the book's history has ever had all four categories contribute.** The median entry scores on **two** of four, with **one** category silenced by its own signals disagreeing with each other.

**The outcome splits:**

| hypothesis | n (yes/no) | ΣR yes / no | mean yes / no | p |
|---|---|---|---|---|
| **H9 ≥3 categories contributed** | 5 / 24 | **−5.435** / −0.550 | **−1.087** / −0.023 | **0.0158** |
| H13b MOMENTUM contributed 0.0 | 14 / 15 | +1.400 / −7.385 | +0.100 / −0.492 | 0.0893 |
| H11 MOMENTUM zeroed by intra-conflict | 13 / 16 | +1.395 / −7.380 | +0.107 / −0.461 | 0.1051 |
| H13 top-category share ≥ 58 % | 15 / 14 | −0.341 / −5.644 | −0.023 / −0.403 | 0.2811 |
| H12 15m tier ABSENT | 5 / 24 | −3.461 / −2.524 | −0.692 / −0.105 | 0.2141 |
| H10 no intra-conflict at all | 3 / 26 | −1.397 / −4.588 | −0.466 / −0.176 | 0.6359 |
| H14 raw score ≥ median (4.25) | 17 / 12 | −2.828 / −3.157 | −0.166 / −0.263 | 0.7889 |
| H15 raw score ≤ 2.75 | 4 / 25 | −0.095 / −5.890 | −0.024 / −0.236 | 0.6908 |

**And the answer to the operator's actual question:**

> **The chop entries DO share a composition quantity — a thinner one.**
> RANGE entries raw score **3.25** vs others **4.38**, Δ = −1.125, **p = 0.044**.
>
> **But a thin composition does not predict a loss.** H15 (raw score ≤ 2.75): **p = 0.691.** The four thinnest entries in the book are vpos 25 (**+1.257R**), 27 (−0.660), 33 (−0.049), 34 (−0.643) — the best trade of the paper book sits at the very bottom of the composition scale, alone on a single category at 100 % top-share.
>
> **The composition quantity that DOES track outcomes says the opposite of the hypothesis.** Entries where **three** categories fired are the worst cohort in the book: **n = 5, ΣR −5.435, mean −1.087R, zero winners** (vpos 10, 16, 18, 22, 26). Richer confluence, worse result.

**§2.54 de-confounding of every nominal hit:**

| candidate | raw Δ, p | day-clustered p | hour-residual Δ, p | side-residual Δ, p | first half / second half |
|---|---|---|---|---|---|
| **≥3 categories** | −1.064, **0.0158** | **0.0104** | −0.933, 0.0294 | −1.037, 0.0190 | **−1.182 / −0.959** |
| MOMENTUM = 0.0 | +0.592, 0.0884 | 0.0932 | +0.648, 0.0525 | +0.599, 0.0858 | +0.489 / +0.686 |
| ATR/14d ≥ 0.93 | −0.545, 0.1194 | 0.1269 | −0.586, 0.0813 | −0.560, 0.1101 | −0.289 / −0.782 |
| RANGE entry | −0.271, 0.5739 | 0.5679 | −0.301, 0.5117 | −0.305, 0.5221 | +0.184 / **−0.403** |
| raw score ≤ 2.75 | +0.212, 0.6893 | 0.6975 | +0.146, 0.7715 | +0.198, 0.7132 | n/a / +0.300 |

🔴 **H9 is the only thing in this pass that survives every control with a stable sign — and it still fails Bonferroni by a factor of 4.7 (p = 0.0158 vs α = 0.00333).** It is also n = 5, **all five in the paper era**, and **four of five LONG**. It is a lead, not a finding, and it is recorded as one.

### The strongest raw correlation in the pass — and how it dies

```
Spearman(stored confluence_score, R) = −0.475   p = 0.0100      the bot's own score
                                                                RANKS ITS TRADES BACKWARDS
  hour-residualised  −0.427  p = 0.0225
  side-residualised  −0.458  p = 0.0125
  day-residualised   −0.439  p = 0.0173        survives every control...
  first half (n=14)  −0.719
  second half (n=15) −0.243
  🔴 paper only (n=22) −0.642      🔴 live only (n=7) +0.214     ...and REVERSES SIGN at the flip
```

**It clears no bar, it halves across its own window, and it changes sign between paper and live.** Filed exactly where the brief says three previous findings went. **n needed for ρ = −0.475 to clear α = 0.00333 at 80 % power: 56 positions — 27 more, ≈ 27 days at the live rate.** That is the one number in this report worth coming back for.

## 2e. NOTHING CLEARS. The full ledger.

**Fifteen declared hypotheses. Bonferroni α = 0.00333. Zero clear it. One (H9) clears the naive 0.05 and survives the controls; one (the score correlation) clears 0.05 and reverses sign.**

Live entry rate: **7 positions in 6.79 days = 1.03 entries/day.** Book R standard deviation: **0.938**.

| candidate | prevalence | Cohen's d | positions needed **in total** | more needed | **days at 1.03/day** |
|---|---|---|---|---|---|
| **RANGE entry split** | 17 % | −0.29 | **2,033** | 2,004 | **1,946 (5.3 years)** |
| ≥3 categories contributed | 17 % | −1.24 | 108 | 79 | **77** |
| MOMENTUM contributed 0.0 | 48 % | +0.65 | 138 | 109 | **106** |
| score-vs-R correlation (ρ=−0.475) | — | — | 56 | 27 | **27** |
| **EMA envelope** | 41 % | −0.05 | 31,458 | 31,429 | **30,514 (84 years)** |
| **ADX+width pair** | 34 % | +0.011 | ~742,000 | — | **~2,000 years** |

---

# PART 3 — THE VERDICT

## Observation 1 — the duplicate: **DISPLAY ARTIFACT. Not real.**

**The operator is seeing ROWS. The bot is making CALLS, and it is making exactly one per market state.**

- Calls per market state: **1.000 on every one of the last 7 days**, and on every day since 2026-08-07. It never drifted back toward 2.20.
- Rows per call: **1.041** over the window, **1.321** on the one day that produced multi-alert states. The 1.26 figure was measured on a busier tape.
- Of the 12 same-side pairs inside 120 s, **11 carry a populated `ai_verdict_reuse_json`** — one model call, N rows, each keeping its own verdict, its own `signal_type`, and the prompt that actually decided.
- The single genuine second call (#17969/#17972) was caused by the **15m tier being rewritten 59 ms into the first consultation**. That is the key working, not failing.
- **Neither the wall multiple nor the wall percentile leaked into the key** — verified at the source line, and the wall price moved in 0 of 9 opportunities.

**One thing did change and it is not the dedup: the relaxations' flip ledger.** Not 3 flips — **41 distinct model flips ever**, 12 of which became positions worth **−4.403R**, and the four most recent (vpos 26, 27, 28, 32) are **0 for 4 at −2.078R**. The relaxations cost **+5.0 % of calls in the last 7 days and +19.8 % all time**, and their live record since the ×20 ceiling is unbroken losses. **That is a decision for the operator, and it is a different decision from the duplicate question.**

## Observation 2 — the range: **STILL NOT FILTERABLE.**

**Is it entering ranges? Partly — and mostly because the market is one.**

- On **ADX**, entry timing is statistically **indistinguishable from random** (mean percentile 50.8, p = 0.877).
- On **24 h range width**, entries are **biased narrow** (mean percentile 37.6, p = 0.0204; 71 % of live entries in the bottom third) — but the tape's own median 24 h width has fallen from 5.5–6.6 % in late June to **2.46 % this week**.
- **Five of 29 entries are genuine range entries** (17, 27, 28, 34, 35), all SHORT, all near the bottom of the range, ΣR **−2.152**, win 20 %. **Two of them are the two newest live positions**, dead in 32 and 70 minutes.

**Has anything changed since the two filters were refused? Yes — and it changed against them.**

- The **EMA envelope** admits **four of the five range entries** (27, 28, 34, 35). Its LONG side-ban broke onto a single loser. Its SHORT half is now *worse* than the half it refuses. **p = 0.902.**
- The **ADX+range pair** produces identical mean outcomes on both sides of the cut (−0.203 vs −0.213, **p = 0.978**). Its ΣR "improvement" is a **34 % volume cut**, not an edge, and its threshold surface is non-monotone in both axes. **In the live era alone it looks perfect — and that is a sign reversal on n = 7, which is evidence against it, not for it.**
- The **composition** hypothesis has an answer for the first time: chop entries *are* thinner (p = 0.044), thinness does *not* predict loss (p = 0.691), and the composition measure that does track outcomes runs the **opposite** way (≥3 categories: mean −1.087R, p = 0.0158, still 4.7× short of Bonferroni).

**What n would be needed, and how long that is:**

> **For the range split as it actually presents itself (d = −0.29 at 17 % prevalence): ≈ 2,033 positions. At the live rate of 1.03 entries/day that is 2,004 more positions — 1,946 days, or 5.3 years.**
>
> **The range problem is not going to become filterable on this book. Not this year, not this decade at this entry rate.** Saying so is the finding. Twenty-two filters have died on this book; the twenty-third and twenty-fourth die here, and the honest reason is not that the mechanism is imaginary — vpos 34 and 35 are as clean a pair of chop shorts as the book contains — but that **SOL does not trade often enough for a 0.27R effect to ever be told apart from noise.**
>
> The only quantity within reach is the **score-vs-outcome correlation: 27 more positions, ≈ 27 days.** If the operator wants one thing watched, watch that — and expect it to die too, because it already reversed sign at the paper/live boundary.

---

# 🔴 PART 4 — TWO THINGS NOBODY ASKED ABOUT, FOUND WHILE MEASURING

## 4a. The 2026-08-10 registry fix REPORTS SUCCESS WHEN IT FAILS — and the stale row is in the table right now

```
2026-08-14T15:30:18   [MERCURY-SOL] [AP] _remove_active_position failed: database is locked
2026-08-14T15:30:18   [MERCURY-SOL][VIRTUAL] [REGISTRY] cleared active_positions for SHORT SOL/USDT:USDT (vpos=35)
                                              ^^^^^^^ IT DID NOT
2026-08-13T17:12:31   [MERCURY-SOL] [AP] _remove_active_position failed: database is locked
2026-08-13T17:12:31   [MERCURY-SOL][VIRTUAL] [REGISTRY] cleared active_positions for SHORT SOL/USDT:USDT (vpos=34)
```

**The table right now:**

```sql
SELECT * FROM active_positions;
  SOL/USDT:USDT  SHORT  entry_time 2026-08-14T14:20:27  entry_price 75.16  updated_at 14:20:27
SELECT id FROM virtual_positions WHERE status != 'closed';   ->  (none)
```

**The row has never been touched since the entry that created it, and its position closed at 15:30:13.**

**The mechanism, exactly.** `main._remove_active_position` (`main.py:234-243`) wraps its `DELETE` in `try/except Exception` and **prints and returns**. `_unregister_active_position` (`main.py:614-618`) pops the in-memory dict first, then calls it — and also returns normally. So in `virtual_trader.close_position` (`virtual_trader.py:785-806`) the call `_live_unregister(...)` **never raises**, the success line prints unconditionally, and the block's own carefully-written failure handler —

```python
except Exception as _unreg_err:
    print(... "🔴 FAILED to clear active_positions" ...)
    send_tg("⚠️ <b>Registry clear FAILED</b> ...")
```

— **is unreachable through this path.** The Telegram alert designed to catch precisely this has never fired and cannot.

**What it costs.** The in-memory registry *was* cleared, so the running process is not confused. The exposure is the **next boot**, which is exactly the sequence the 08-10 pass was written to close: a boot that reads a stale `active_positions` row, asks the venue, finds it flat, and books a phantom close. **The belt is loaded** (`_ledger_close_after` runs before the close-row insert, proven present at the 19:06 boot), so a phantom row should still be prevented — **but the primary defence silently failed on both of its first two real exercises, and the alarm on it is dead.** This is the "a mechanism that does not do what it says" class, in the fix written to close that class.

**Read-only. Nothing was changed. The row was not deleted by me.**

## 4b. 🔴 THE BOOK GATE HAS BREACHED ITS OWN PRE-REGISTERED RED LINE

The OPEN-ITEMS file states the trip wire in its own words:

> *"🔴 IF THE REALISED RATE IS MATERIALLY DIFFERENT — above 5 % on either side, or a side ratio above 2× — THAT IS A FINDING ABOUT THE CALIBRATION AND GROUNDS TO REVISIT. IT IS NOT A REASON TO LOOSEN THE THRESHOLD QUIETLY."*

**It has fired, and both wires are tripped:**

| | pre-registered 2026-08-10 18:30 | **realised** | |
|---|---|---|---|
| refusal rate LONG | 2.20 % | **6.82 %** (6 of 88) | **3.1× · above the 5 % wire** |
| refusal rate SHORT | 2.67 % | **23.17 %** (19 of 82) | **8.7× · far above the 5 % wire** |
| side ratio | 1.21× | **3.40×** | **above the 2× wire** |
| overall | ~2.4 % | **14.7 %** (25 of 170) | |
| first refusal expected | ~29 days (≈ 2026-09-08) | **2026-08-11 07:20:01 — day 1** | |

**By clause and side:** A (wall) — 2 LONG, 2 SHORT. **B (liquidity presence) — 4 LONG, 17 SHORT.** Clause B on the SHORT side is doing nearly all of the work, at roughly **10× its pre-registered 1.83 %**.

**Refusals by day: 08-11 → 5, 08-12 → 16, 08-13 → 3, 08-14 → 1.** The 08-12 cluster is 16 refusals in one day out of 34 evaluations — **47 %**.

The pre-registration also says what the correct response is, and it is not mine to take: **re-cut the ruler and say so**, do not raise `BOOK_GATE_WALL_PCTL` until the refusals stop. The `BOOK_GATE_LEAN_FLOOR` was cut from the 2nd percentile of each side's own lean distribution over 1,545/1,909 stored books; a realised SHORT rate of 23 % against a designed 1.83 % means **that distribution has moved**, which is consistent with everything in §2a — the tape compressed, and a lean floor cut on a wider tape now bites constantly.

🔴 **This is a declared, pre-registered finding that fired three days ago and has not been read until now. Read-only — no threshold was touched, no flag changed.**

---

## STATE AT THE END OF THIS PASS

```
mercury-sol   active · master 335081 / worker 335146 · since 2026-08-10 19:06:06 · NRestarts=0
              🔴 NOT RESTARTED BY ME. Same pid as the 08-10 pass left running.
BOOK          29 positions, ALL CLOSED. FLAT since 2026-08-14 15:30:13.
              🔴 CORRECTION TO THE BRIEF: vpos 32 is NOT open — closed 08-10 19:45:18,
                 exit_signal, −0.180R. Nothing was touched either way.
              paper 22 (vpos 7–28) ΣR −5.374 · live 7 (vpos 29–35) ΣR −0.611
              live era: 6.79 days, 1.03 entries/day, win 28.6%
LAST TRADE    vpos 35 SHORT 75.16 → 75.57, sl, −0.701R, closed 15:30:13 (70 minutes)
🔴 OPEN       active_positions holds ONE STALE ROW (SHORT, entry_time 14:20:27) for a
              position that closed at 15:30:13. Two silent clear-failures: vpos 34, vpos 35.
🔴 OPEN       book gate realised refusal rate 6.82% LONG / 23.17% SHORT vs pre-registered
              2.20% / 2.67%; side ratio 3.40× vs 1.21×. Both declared wires tripped.
FILES         mercury-sol: NONE modified. No restart, no order, no DB write, no .bak needed.
titan         /root/titan-bot — NOT touched, NOT read for state, NO numbers imported.
```

---

## APPENDIX — the fifteen hypotheses and their p-values, in one place

```
alpha = 0.05 / 15 = 0.00333          none clear it

H1  EMA envelope both-Expanding              n=12/17  Δ−0.045  p=0.9022
H2  ADX>=20 AND width-pctl>=20               n=19/10  Δ+0.010  p=0.9784
H3  ADX(1h,200) >= 20                        n=22/7   Δ+0.114  p=0.7853
H4  24h width >= median (3.15%)              n=15/14  Δ−0.255  p=0.4734
H5  ER(4h) >= median (0.198)                 n=15/14  Δ−0.135  p=0.7049
H6  ER(12h) >= median (0.207)                n=15/14  Δ+0.482  p=0.1720
H7  ATR/14d-median >= median (0.93)          n=15/14  Δ−0.545  p=0.119
H8  |pos24 − 0.5| >= median (0.43)           n=15/14  Δ−0.274  p=0.4430
H9  >=3 categories contributed               n= 5/24  Δ−1.064  p=0.0158  <- nominal only
H10 no category zeroed by intra-conflict     n= 3/26  Δ−0.289  p=0.6359
H11 MOMENTUM zeroed by intra-conflict        n=13/16  Δ+0.569  p=0.1051
H12 15m tier ABSENT from the prompt          n= 5/24  Δ−0.587  p=0.2141
H13 top-category share >= median (0.58)      n=15/14  Δ+0.380  p=0.2811
H14 raw direction score >= median (4.25)     n=17/12  Δ+0.097  p=0.7889
H15 raw score <= 2.75                        n= 4/25  Δ+0.212  p=0.6908

    RANGE-entry split (the composite of H3+H4)  n= 5/24  Δ−0.271  p=0.5739
    Spearman(confluence_score, R)            ρ=−0.475  p=0.0100  <- reverses sign paper→live
```

**Provenance of every figure above: SOL's own `trades.db` opened read-only, and Bybit SOLUSDT-perp candles fetched fresh through the bot's own venue over Tor. `market_regime` was not used. Titan was not read.**
