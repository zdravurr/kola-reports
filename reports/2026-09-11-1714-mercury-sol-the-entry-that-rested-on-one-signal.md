# mercury-sol-the-entry-that-rested-on-one-signal

_2026-09-11 17:14 UTC_

---

# Mercury-SOL — the entry that rested on one signal

**2026-09-11 · READ-ONLY audit · nothing proposed, nothing applied** · marker `REPORT-ID sol-single-signal-20260911-1715`

The trade: **vpos 44**, LIVE, SHORT 99.30 → 101.23, stop, **−$2.1305 = −1.110R**. Entry row `trades.id 25731`, 2026-09-11 11:50:07 (fill 11:50:24).

> **CONTROLS, DECLARED BEFORE ANY RESULT WAS READ.**
> * **Book cells** (the 38 closed `virtual_positions`: 16 live, 22 paper) are described, never tested. Paper and live are **never pooled**. **No cell below n = 8 is ranked.**
> * **SHAPE family** (substitute population, §5): 7 contrasts × 2 sides × 3 horizons = **42 cells, Bonferroni α = 0.05/42 = 0.00119**. S7 was added to the script *before its first run*, and the family size includes it.
> * **NEWS family** (replication of 2026-08-10): 2 contrasts × 3 sides × 3 statuses × 3 horizons = **54 cells, α = 0.000926**.
> * A shape **survives** only if all four hold: the raw p clears α; the **day-matched** p clears α; **≥ 10 of 12** equal-time windows show the full-sample sign, counting only windows where both legs have n ≥ 8; and the sign holds in **both** the paper era and the live era.

---

## VERDICT

🔴 **Nothing separates. No shape the operator named is measurably worse on any population this bot has.**

- **The book cannot rank the shape.** Entries with three of four categories zeroed: **live n = 2** (vpos 33 −0.049R, vpos 44 −1.110R), **paper n = 0**.
  - Single-contributor entries: **live n = 6, ΣR −0.710; paper n = 5, ΣR +5.156.** The sign **inverts** between the books.
  - A lone EXECUTION entry: **live n = 2, paper n = 0.**
  - Scraping the bar by exactly 0.00: **n = 1 in the whole book.** It is this trade.
- **The larger substitute population cannot rank it either.** That population is 4,494 signals that cleared the score gate and were then refused by the advisor, with forward drift measured.
  - **0 of 42 shape cells survive.** Six clear raw Bonferroni, and **four of those six point the wrong way**: the operator's shape drifted *better*.
  - All six die on day-matching.
  - The nearest miss, S7 SHORT 4h, fails day-matching, fails the 12-window test at 8/12, and **flips sign between the paper and live eras**.
- **The news term is still a clock:** 26/54 cells clear raw, **0/54 survive day-matching**.
- **Every candidate is knowable at entry.** None needs look-ahead, and none survives. This is the twenty-ninth set of entry candidates to die on these books, and it gets no sympathy.

**Three facts that do NOT need n. They come from the code and the record:**

1. **The 2.00 bar is a lookup table, not a judgement, for any signal with one contributing category** (§2c). Across 7,808 signals that reached it:
   - with **no news**, it passed **100%** of lone signals worth ≥ 2.00 and **0%** of those below;
   - with **news +1.0**, it passed **542 of 542** lone signals, down to a 0.5-weight trigger at 1.25;
   - with **news −1.0**, it passed **0 of 931**.
   - It has **never refused a signal with two or more contributing categories**, except 9 of 672 at news −1.0.
   - Arithmetic floor: **one unopposed 5m trigger scores 1.25 to 2.50.** Seven of the sixteen 5m triggers per side clear 2.00 alone, and with news +1.0 all sixteen do.
2. **The gate compared 3.00** (`main.py:4675-4676`, `MACRO_GATE_DRYRUN = False` at `config.py:813`). The weight term's +0.24 is **stored, not gated**, so the 2026-08-10 finding still holds. **But the news term did NOT flip this entry.** Raw 2.00 is not below 2.00, so the bar would have admitted it with no headline at all.
3. **The rule written for exactly this shape logged a block and did not refuse.** The HTF cascade's `neutral_15m` clause ("1H NEUTRAL and 15m not confirming → BLOCK") fired on this entry:
   `11:50:07 HTF_NEUTRAL_15M_WOULD_BLOCK SOL/USDT:USDT SHORT 1H=NEUTRAL 15m=NEUTRAL 5m=SHORT reason=1H_neutral_15m_not_confirming dryrun=True`
   - Cause: `HTF_NEUTRAL_REQUIRE_15M_DRYRUN = True` (`config.py:908`, "Lever A-2 2026-06-29").
   - This is a statement of how the entry got through, not a proposal. S7 measures the shape that clause describes, and **it dies** (§5).

---

## 0. THE TRADE, RE-READ FROM THE RECORD

```
trades.id 25731   2026-09-11 11:50:07   SHORT   tv_action 'Bearish OB Entered' (5m)   is_virtual 0 (LIVE)
matrix (trade_signal_matrix + trades.matrix_breakdown_json — identical)
  TREND      L 2.50 / S 2.50   intra_conflict  → 0     signals: Trend Catcher Up   (age 349.8 of 360 min TTL)
                                                                Trend Catcher Down (age  49.9 min)
  MOMENTUM   L 1.75 / S 1.75   intra_conflict  → 0     signals: HyperWave Signal Up   (age 80.0 of 90 min TTL)
                                                                HyperWave Signal Down (age 49.8 min)
  LIQUIDITY  L 1.75 / S 1.25   intra_conflict  → 0     signals: Bullish New Imbalance (0.0 min), Bearish Imbalance Mitigated (0.0 min)
  EXECUTION  S 2.00            contributes 2.00        signal : Bearish OB Entered, w 0.8 × 2.5 = 2.00
raw direction score    2.00        (journal 11:50:16: "weighted_adj: dir=SHORT raw=2.00 adj=+0.2400 final=2.24")
weighted_adj           +0.24       → stored confluence_score 2.24   (NOT in the gate)
macro_gate_penalty     +1.0        CRITICAL_NEGATIVE (conf 0.85) "Blockstream refuses ransom demand … Liquid exploit" [The B.]
GATE compared          2.00 + 1.0 = 3.00  ≥ 2.0
HTF cascade            1H NEUTRAL, 15m NEUTRAL, 5m SHORT → neutral_15m WOULD BLOCK, dryrun=True → passed
market_regime          FLAT (TREND zeroed)       srv_adx_1h 44.5
book gate              admitted (lean 0.5286; ask-heavy imbalance 0.4714 on the advisor book)   — not re-litigated
advisor                execute 0.72 — reason text: "3-tier SHORT confluence (1H/15m/5m all bearish)"
```

🔶 **The matrix and the advisor saw two different pictures, both from the same signals.**
- Both TREND and MOMENTUM zeroed because a **fresh** SHORT signal sat beside an **old** LONG signal that had not yet expired. Trend Catcher Up was **10 minutes from its 360-minute TTL**, and HyperWave Up was **10 minutes from its 90-minute TTL**.
- The matrix counts every signal inside its TTL. The slot state machine that feeds the advisor prompt keeps only the latest one per slot. So the advisor was told "1H Trend Catcher Down, 15m HyperWave Down", read that as three-tier alignment, and the matrix scored it as one signal.
- This is knowable at entry. It is **not** in the declared family and was **not** measured. It is recorded as how this entry was built, not as a candidate.

---

## 1. THE SHAPE, COUNTED ACROSS THE WHOLE BOOK

Definitions, for each signal on the side it proposes:
- **contributing** = the category's net direction is that side and its contribution is above 0;
- **ZEROED** = `intra_conflict` is true;
- inter-conflicted and opposite-side categories are counted apart and are neither.

The raw score is recomputed from the breakdown. It agrees with `skip_attribution.confluence_score` on **7,709 of 7,709** rows. It agrees with `trade_signal_matrix.score` on 87 of 93 rows; the 6 disagreements are explained in §3b and are a provenance trap.

### 1a. Every scored signal in the record (17,361 rows with a matrix breakdown)

| side | n | contributing 0 / 1 / 2 / 3 / 4 | intra-ZEROED 0 / 1 / 2 / 3 / 4 | **3 zeroed + 1 contributing (this trade's shape)** |
|---|---|---|---|---|
| LONG | 8,433 | 1,999 / 3,092 / 2,674 / 644 / 24 | 3,125 / 3,340 / 1,633 / **326** / 9 | **92** |
| SHORT | 8,928 | 2,051 / 3,451 / 2,745 / 652 / 29 | 3,370 / 3,536 / 1,700 / **314** / 8 | **70** |

Three of four categories zeroed is **3.9% of LONG and 3.5% of SHORT** signals. A single contributing category is **37% / 39%**, which makes it the commonest shape after two contributors.

**Of the 7,808 signals that actually reached the score gate:**

| side | reached, by # zeroed 0 / 1 / 2 / 3 / 4 | passed the bar | 3-zeroed pass rate |
|---|---|---|---|
| LONG | 944 / 1,539 / 984 / 215 / 8 | 815 / 940 / 337 / 25 / 0 | 25/215 = 11.6% |
| SHORT | 1,143 / 1,763 / 1,013 / 192 / 7 | 1,010 / 1,080 / 355 / 33 / 0 | 33/192 = 17.2% |

### 1b. ENTRIES by # categories zeroed — n per cell, per side, paper and live separately

| book | side | 0 zeroed | 1 zeroed | 2 zeroed | **3 zeroed** |
|---|---|---|---|---|---|
| **live** | LONG | 1 | 7 | 0 | **1** (vpos 33) |
| **live** | SHORT | 1 | 5 | 0 | **1** (vpos 44) |
| paper | LONG | 2 | 4 | 3 | 0 |
| paper | SHORT | 0 | 10 | 3 | 0 |

### 1c. Outcomes by that count (n stated first, below n = 8 not ranked)

| book | cell | n | ΣR | win | mean | median | |
|---|---|---|---|---|---|---|---|
| live | 0 zeroed | 2 | −0.321 | 1/2 | −0.160 | −0.160 | n<8 NOT RANKED |
| live | 1 zeroed | **12** | **+8.233** | 6/12 | +0.686 | +0.587 | rankable |
| live | **3 zeroed** | **2** | **−1.158** | 0/2 | −0.579 | −0.579 | **n<8 NOT RANKED** |
| paper | 0 zeroed | 2 | −2.159 | 0/2 | −1.080 | −1.080 | n<8 NOT RANKED |
| paper | 1 zeroed | **14** | **−3.341** | 6/14 | −0.239 | −0.365 | rankable |
| paper | 2 zeroed | 6 | +0.125 | 2/6 | +0.021 | −0.462 | n<8 NOT RANKED |
| paper | 3 zeroed | 0 | — | — | — | — | empty |

By **number of contributing categories** (the same question from the other end):

| book | 1 contributor | 2 contributors | 3 contributors |
|---|---|---|---|
| **live** | n=6 · ΣR **−0.710** · 1/6 · med −0.672 | n=7 · ΣR +8.051 · 5/7 | n=3 · ΣR −0.587 · 1/3 |
| **paper** | n=5 · ΣR **+5.156** · 4/5 · med +1.257 | n=12 · ΣR −5.096 · 4/12 · med −0.420 | n=5 · ΣR −5.435 · 0/5 |

🔴 **The live book cannot rank the operator's shape: the 3-zeroed cell is n = 2 live and n = 0 paper.** The only rankable cells are "1 zeroed" (live n=12, paper n=14), and they point opposite ways: +8.233 live, −3.341 paper.
- The single-contributor cell is n = 6 live, n = 5 paper, and inverts sign between the books: −0.710 live, +5.156 paper.
- **Paper figure, labelled as paper:** single-contributor paper entries returned **+5.156R, 4 of 5 winning.** On paper the lone-signal shape is the *best* cell, not the worst.

🔶 **A confound that dominates every live SHORT-heavy cell: the live SHORT side is 0 wins in 7 (ΣR −5.699), whatever its shape.** The live LONG side is 7 in 9 (ΣR +12.453). Four of the six live single-contributor entries are SHORT. A shape that happens to be SHORT on the live book will look bad for reasons that have nothing to do with the shape.

### 1d. The single contributing category — is a lone EXECUTION different from a lone TREND?

| book | lone category | n | ΣR | win | vpos |
|---|---|---|---|---|---|
| live | **EXECUTION** | **2** | **−1.866** | 0/2 | 36, 44 |
| live | MOMENTUM | 3 | +1.205 | 1/3 | 34, 35, 40 |
| live | TREND | 1 | −0.049 | 0/1 | 33 |
| live | (multi) | 10 | +7.464 | 6/10 | |
| paper | TREND | 3 | +2.563 | 2/3 | 7, 11, 27 |
| paper | MOMENTUM | 1 | +1.337 | 1/1 | 13 |
| paper | LIQUIDITY | 1 | +1.257 | 1/1 | 25 |
| paper | EXECUTION | 0 | — | — | — |
| paper | (multi) | 17 | −10.531 | 4/17 | |

🔴 **All cells are n < 8, and none is ranked.** A lone EXECUTION has happened twice, both live, both losses, both SHORT. On paper it never happened. **The book cannot say whether a lone EXECUTION differs from a lone TREND.** The substitute population's direct contrast (S5, lone EXECUTION vs lone LIQUIDITY) finds nothing on either side (§5).

Notice what the lone category usually is: in 5 of the 11 single-contributor entries it is **MOMENTUM, with the trigger's own EXECUTION category zeroed**. The bot entered on its 15m signal while the 5m trigger that fired the webhook cancelled itself out.

---

## 2. THE BAR, CLEARED BY ZERO

### 2a. Raw score at entry

| book | raw score at entry: value (n) |
|---|---|
| live | 1.75 (3) · **2.00 (1)** · 2.50 (2) · 3.50 (1) · 4.00 (1) · 4.25 (3) · 4.50 (2) · 5.75 (1) · 6.00 (1) · 6.75 (1) |
| paper | 1.75 (2) · 2.50 (3) · 3.00 (1) · 3.50 (1) · 3.75 (3) · 4.00 (2) · 4.25 (2) · 4.75 (2) · 5.00 (1) · 5.50 (1) · 5.75 (2) · 6.00 (1) · 6.25 (1) |

- **Cleared by exactly 0.00 on raw: 1 entry in the whole book, vpos 44.** Cleared by more than 0 and less than 0.25: **0**.
- **Below the bar on raw and carried over it by news: 5** (live 34, 35, 40; paper 13, 25). All five had raw 1.75.
- **On the quantity the gate actually compares** (raw + news), **no entry has ever cleared by less than 0.50.** The lowest gate score in the book is 2.50. vpos 44 cleared the gate by **1.00**.

### 2b. Outcomes by margin over the bar

| book | raw margin | n | ΣR | win |
|---|---|---|---|---|
| live | < 0 (news-carried) | 3 | +1.205 | 1/3 |
| live | **0.00** | **1** | **−1.110** | 0/1 |
| live | [0.25, 1.0) | 2 | −0.805 | 0/2 |
| live | ≥ 1.0 | **10** | +7.464 | 6/10 |
| paper | < 0 (news-carried) | 2 | +2.594 | 2/2 |
| paper | [0.25, 1.0) | 3 | +2.563 | 2/3 |
| paper | ≥ 1.0 | **17** | **−10.531** | 4/17 |

| book | gate margin (raw + news) | n | ΣR | win |
|---|---|---|---|---|
| live | [0.50, 1.0) | 4 | +0.448 | 1/4 |
| live | ≥ 1.0 | 12 | +6.306 | 6/12 |
| paper | [0.50, 1.0) | 5 | **+5.820** | **5/5** |
| paper | ≥ 1.0 | 17 | **−11.195** | 3/17 |

🔴 **Entries that scrape the bar do NOT lose systematically on either book.**
- Live: every "scrape" cell is n < 8.
- Paper, labelled as paper: the thin-margin entries won 5 of 5, and the ≥ 1.0 cell lost −11.195R on 17.
- On paper the relation runs **the other way**. The substitute population agrees in direction: S3 on LONG shows [2.00, 2.25) drifting better, and on SHORT worse at nominal p ≈ 0.01, with 8 of 12 windows unusable (§5). **This is not a fact about the bar.**

### 2c. 🔴 The arithmetic floor — stated from the code

`signal_matrix.py:289` `contribution = sig['intensity_weight'] * CATEGORY_MAX_POINTS` (2.5), capped at 2.5 per category (`:297-298`). A category with signals on both sides contributes **0** (`:299-301`). The direction score is the sum over that side's categories (`:333-336`). The gate is `raw + news ≥ 2.0` (`main.py:4675-4676`).

**So one unopposed signal scores `weight × 2.5`.** The 5m triggers (EXECUTION and LIQUIDITY, identical on both sides), read from `signal_matrix.py` as text:

| weight | score alone | 5m triggers (per side) | clears 2.00 with news 0 | with news +1.0 | with news −1.0 |
|---|---|---|---|---|---|
| 1.0 | 2.50 | S-CHOCH+, Liquidity Grab | ✅ | ✅ | ❌ |
| 0.9 | 2.25 | I-CHOCH+, S-BOS, Equal H./Lows | ✅ | ✅ | ❌ |
| **0.8** | **2.00** | S-CHOCH, **OB Entered** | ✅ **by exactly 0.00** | ✅ | ❌ |
| 0.7 | 1.75 | I-CHOCH, I-BOS, Within OB, Breaker, Broken trendline, New Imbalance | ❌ | ✅ | ❌ |
| 0.5 | **1.25 = the floor** | OB Created, OB Mitigated, Imbalance Mitigated | ❌ | ✅ | ❌ |

- **The floor is 1.25.** A single unopposed 5m signal yields 1.25 to 2.50.
- **Seven of the sixteen 5m triggers per side clear the 2.00 bar alone. With a +1.0 headline, all sixteen do.** A lone 1h TREND signal (weight 0.6–1.0) scores 1.50–2.50, and a lone 15m MOMENTUM (0.7–1.0) scores 1.75–2.50.

**And the record shows the bar behaving exactly as that table predicts, with no exceptions.** Signals that reached the gate with one contributing category:

| lone score | news 0 | news +1.0 | news −1.0 |
|---|---|---|---|
| 1.25 | 0 / 83 passed | **30 / 30** | 0 / 42 |
| 1.75 | 0 / 989 | **284 / 284** | 0 / 449 |
| 2.00 | **98 / 98** | 28 / 28 | 0 / 67 |
| 2.25 | 25 / 25 | 27 / 27 | 0 / 23 |
| 2.50 | 505 / 505 | 173 / 173 | 0 / 335 |

| # contributing categories | news 0 | news +1.0 | news −1.0 |
|---|---|---|---|
| 0 | 0 / 668 | 0 / 287 | 0 / 246 |
| **1** | 628 / 1,700 (36.9%) | **542 / 542 (100%)** | **0 / 931 (0%)** |
| 2 | 1,271 / 1,271 | 618 / 618 | 663 / 672 |
| 3 | 371 / 371 | 236 / 236 | 207 / 207 |
| 4 | 25 / 25 | 19 / 19 | 9 / 9 |

🔴 **So, stated plainly:**
- For a single-signal entry, the 2.00 bar is **a function of two inputs**: the weight of the one signal (≥ 0.8 or not) and the sign of the headline. It weighs nothing else.
- **Once a +1.0 headline is on the wire, the bar cannot refuse a single-signal entry at all.** At news 0 it refuses only the 0.5 and 0.7 triggers.
- Above one contributing category, the bar has refused **9 signals out of 3,631** in the bot's history, and all 9 had news −1.0.
- **Decorative, in the operator's word, for everything with two or more categories. For single-signal entries it is a weight lookup with a headline override.** That is a statement about the arithmetic, not a finding that the entries it admits lose. §1 and §5 show that they do not lose measurably.

---

## 3. THE NEWS TERM, ON THIS TRADE AND IN GENERAL

### 3a. Which quantity did the gate compare? — **3.00**

```
main.py:4536   _macro_gated_score = round(direction_score + _macro_gate_adj, 2)
main.py:4566   _w_adj, _w_breakdown = weight_engine.weighted_adj(
main.py:4570   adj_score = round(direction_score + _w_adj, 2)          # → stored as confluence_score (2.24)
main.py:4674   _thr = _get_live_param('CONFLUENCE_SCORE_THRESHOLD', CONFLUENCE_SCORE_THRESHOLD)
main.py:4675   _gate_score = direction_score if MACRO_GATE_DRYRUN else _macro_gated_score
main.py:4676   if _gate_score < _thr:
config.py:813  MACRO_GATE_DRYRUN           = False
config.py:716  CONFLUENCE_SCORE_THRESHOLD = 2.0
main.py:60-66  _get_live_param(key, default): … return default      # neutered — no live override
```

- **On this entry the gate compared `_macro_gated_score` = 2.00 + 1.0 = 3.00.** Not 2.00 and not 2.24. The +0.24 weight term appears in neither branch of `:4675`.
- `:4675-4676` is **the only score-gate site in `main.py`**; `CONFLUENCE_SCORE_THRESHOLD` has no other use.
- **The 2026-08-10 finding still holds, and it is proven again from data.** The verdict predicted from `raw + macro_gate_penalty` against 2.0 matches the stored status on **7,808 of 7,808** gate-reaching rows. `macro_gate_penalty` is NULL on none of them.
- 🔴 **Did the news term flip this one? — No.** Raw 2.00 against `if _gate_score < 2.0`: 2.00 is not less than 2.0, so the entry would have passed with no headline. The +1.0 moved it from "cleared by 0.00" to "cleared by 1.00", and that changed nothing about the verdict.

### 3b. How often does the news term move a signal across the bar?

| side | reached the gate | flipped IN (raw < 2 ≤ raw+news) | flipped OUT (raw ≥ 2 > raw+news) | unchanged |
|---|---|---|---|---|
| LONG | 3,690 | **116** (3.1%) | 244 (6.6%) | 3,330 |
| SHORT | 4,118 | **198** (4.8%) | 203 (4.9%) | 3,717 |

Of the 314 flipped in, the advisor refused **308**, 1 was observed-skipped, and **5 became positions**:

| vpos | book | side | raw | news | gate | R |
|---|---|---|---|---|---|---|
| 13 | paper | SHORT | 1.75 | +1.0 | 2.75 | +1.337 |
| 25 | paper | SHORT | 1.75 | +1.0 | 2.75 | +1.257 |
| 34 | live | SHORT | 1.75 | +1.0 | 2.75 | −0.643 |
| 35 | live | SHORT | 1.75 | +1.0 | 2.75 | −0.701 |
| 40 | live | LONG | 1.75 | +1.0 | 2.75 | +2.549 |

🔴 **Provenance trap found on the way. `trade_signal_matrix.score` is NOT the direction score.** It stores the matrix **winner's** score (`res['score']`). On **6 of 93** rows the winner was the opposite side, and **two of them are book entries**:
- **vpos 13** (paper) and **vpos 35** (live) were entered SHORT while the matrix's own winner was LONG, at 2.50.
- Their true SHORT score was **1.75**, which makes both **news-flipped**.
- The 2026-08-10 note "raw for `executed` → `trade_signal_matrix.score`" misclassifies both. The raw score must come from the breakdown on the traded side; that recompute agrees with `skip_attribution.confluence_score` on 7,709 of 7,709 rows.
- Separately, **entering against the matrix's own winning direction** has happened on 2 positions (1 live, 1 paper). It is recorded, not measured.

### 3c. Outcomes of news-flipped entries versus the rest

| book | cell | n | ΣR | win | mean |
|---|---|---|---|---|---|
| live | news-flipped | 3 | +1.205 | 1/3 | +0.402 |
| live | not flipped | 13 | +5.549 | 6/13 | +0.427 |
| paper | news-flipped | 2 | +2.594 | 2/2 | +1.297 |
| paper | not flipped | 20 | −7.968 | 6/20 | −0.398 |

**Unrankable. n = 3 live and n = 2 paper.** By news sign at entry: live `+1.0` n=6 ΣR −1.109; `0` n=8 ΣR +6.688; `−1.0` n=2 ΣR +1.175. All n < 8.

**Does "it is a clock" hold on the current book? — Yes, the de-confound result holds exactly.** I re-ran the 2026-08-10 design on the cohort as it stands today: 7,666 refusals from 06-08 to 09-11 with drift; 41 rows inside the blackout window were excluded.

| control | cells | clearing α = 0.000926 |
|---|---|---|
| raw | 54 | **26** (08-10: 21) |
| **day-matched** | 54 | **0** (08-10: 0) |

- The strongest raw cell, `SHORT BOTH news+ vs news0` at 12h (**t = 9.40, p = 1.8e-20**), becomes **t = 0.13 inside a day**.
- **Every one of the 26 dies.**
- 🔶 **One part of the 08-10 argument does NOT replicate, and I am saying so.** The "tell" was that news+ and news− drift the same way. On today's cohort that holds in only **8 of 27** paired cells. The raw pattern now looks directional: news+ better, news− worse.
- The conclusion rests on the day-matching, and that is still **0 of 54**. Whatever the raw pattern is, it lives between days, not between signals.

---

## 4. 🔴 THE CPI WINDOW — entered at −39.6 minutes

### 4a. SOL around CPI, −120m → +120m, 15-minute buckets

**Method, as in 2026-09-04 §4:**
- `range% = (high − low) / mid` of Bybit `SOLUSDT` linear 5m bars, pulled by public GET over the box's Tor SOCKS. There are 288,492 bars from 2023-12-15 to 2026-09-11, with no gaps.
- Each event's bucket is divided by the **median of the same clock bucket on baseline days**, and the table reports the median of those per-event ratios.
- **Baseline: weekdays within ±14 days, excluding every known release day.** The 09-04 report used all non-event days in its sample.

**The dates, and how far each tier can be trusted:**
- **Tier A+B, n = 10**, from 2025-12-18 to 2026-09-11. The dates agree between **two sources**: the BLS release schedule and archive pages, plus `config.py` `MACRO_EVENTS` for the five from May onward. 08:30 ET is converted to UTC via `America/New_York`.
- **Tier C, n = 22**, 2024–2025. These come from **one source only**, the BLS archive page. The raw page returns "Access D." to this box directly and over Tor, so the dates reached me only through a summarising fetch. **They are a sensitivity check, not the headline.**
- 🔶 One Tier C date, **2024-01-16, shows no disturbance at all**: its −5..+10 block is 0.60×, the only one of 32 releases below 1.29×. That is consistent with a mis-read date. It is kept as fetched, and it is flagged.

**CPI, Tier A+B (n = 10):**

| bucket | med range % | baseline % | ratio | events > 2× |
|---|---|---|---|---|
| −120..−105 | 0.441 | 0.313 | 1.14× | 2/10 |
| −105..−90 | 0.326 | 0.293 | 0.92× | 0/10 |
| −90..−75 | 0.457 | 0.354 | 1.29× | 1/10 |
| −75..−60 | 0.320 | 0.346 | 0.83× | 2/10 |
| −60..−45 | 0.342 | 0.306 | 1.04× | 0/10 |
| **−45..−30** ← this entry | 0.306 | 0.309 | **0.86×** | **0/10** |
| −30..−15 *(blackout)* | 0.448 | 0.375 | 1.15× | 1/10 |
| −15..+0 *(blackout)* | 0.539 | 0.365 | 1.49× | 1/10 |
| **+0..+15** *(blackout)* | **1.303** | 0.443 | **3.16×** | **8/10** |
| +15..+30 *(blackout)* | 0.549 | 0.377 | 1.41× | 3/10 |
| +30..+45 | 0.576 | 0.443 | 1.10× | 1/10 |
| +45..+60 | 0.677 | 0.431 | 1.43× | 2/10 |
| +60..+75 | 1.056 | 0.846 | 1.00× | 2/10 |
| +75..+90 | 0.963 | 0.719 | 1.27× | 1/10 |
| +90..+105 | 0.788 | 0.685 | 1.24× | 1/10 |
| +105..+120 | 0.697 | 0.704 | 1.06× | 1/10 |

At 5-minute resolution: **−5..+0 1.94× (5/10), +0..+5 3.75× (9/10), +5..+10 2.56× (7/10), +10..+15 1.76×.** Every bucket from −30 to −5 sits between 0.97× and 1.25×.

**Block view, three populations:**

| block | CPI A+B (n=10) | CPI C (n=22, sensitivity) | NFP (n=4, config dates) |
|---|---|---|---|
| **−120..−30** (the band the blackout leaves open) | **1.13×** | **0.85×** | 1.18× |
| −30..−5 (the blackout's left half) | **1.01×** | **0.93×** | **2.01×** (3 of 4 ≥ 1.98×) |
| **−5..+10** (the disturbance) | **3.07×** | **2.95×** | 3.49× |
| +10..+30 | 1.36× | **1.94×** | 1.40× |
| +30..+120 | 1.41× | 1.19× | 1.05× |

🔴 **CPI's shape, stated:**
- **Nothing happens before −5 minutes.** The −120..−30 band runs at 1.13× baseline on the corroborated ten and **0.85×** on the 2024–25 sample. Across 32 releases, the hour and a half before a CPI print is **quieter than or equal to** an ordinary weekday at the same clock.
- The disturbance is **−5 to +10**: 3.07× and 2.95×, and +0..+5 is elevated on 9/10 and 20/22.
- It has a **tail to +30** that is clear in the 2024–25 sample (1.94×) and weaker in the recent ten (1.36×).
- **The entry's own bucket, −45..−30, was 0.86× with no release above 2×.** At −39.6 minutes vpos 44 entered into ordinary air.

**CPI is not NFP in one respect, on thin evidence.** NFP's last half hour before the print ran at **2.01×**, with 3 of 4 releases ≥ 1.98×. CPI's ran at **1.01× / 0.93×**. **At n = 4 that difference is unrankable.** It is recorded as a description: the blackout's left half is empty for CPI on 32 releases, and may not be for NFP.

### 4b. Entries between −120m and −30m before a scheduled release

| book | side | n | ΣR | |
|---|---|---|---|---|
| **live** | SHORT | **1** | −1.110 | **vpos 44 itself** |
| live | LONG | 0 | — | |
| paper | both | 0 | — | |

🔴 **It is one trade. This band cannot be ranked. Nothing about the window's shape can be concluded from the book.**
- The substitute population (§5 S6) has 6 LONG and 14 SHORT gate-passed signals in this band, on **four calendar days per side**. Its 12-window test has **0 usable windows of 12**.

**What does touch the book is not the entry band but exposure through the print.** The blackout is entry-only (confirmed live on 2026-09-04: a stop filled 11 s after a CPI print). Positions held open across a scheduled release:

| book | n | ΣR | vpos |
|---|---|---|---|
| live | 2 | −1.158 | 33 (LONG, entered 870 min before CPI, −0.049R), **44** (SHORT, 40 min before, −1.110R) |
| paper | 1 | +0.004 | 17 |

n = 3 in total. Unrankable. This is also only partly knowable at entry: the calendar is known, the holding time is not.

### 4c. How this trade was lost — a trace, n = 1, exit-side, outside the five questions

Recorded because it decided the size of this loss, and it happened inside the CPI disturbance. **It is not a finding.**

```
fill 99.30 @ 11:50:24   SL 101.22 = 99.30 + 2.5 × ATR(1h) 0.76806
arm distance = TRAIL_ARM_R × SL_BUFFER_ATR × ATR = 0.75 × 2.5 × 0.76806 = 1.440   (trail_arm.py:135)
                → arm level for the SHORT = 97.86      BE lock = 99.30 × (1 − 0.0020) = 99.10
11:50 → 12:28   price 99.04 – 99.61 (ordinary; poller MFE 0.25 %)
12:29 (1m)      high 100.12  — the pre-print spike
12:30 (1m)      LOW 97.76    ← 0.10 BEYOND the arm level
                poller samples: 12:29:57 99.59 · 12:30:09 98.08 · 12:30:24 98.36   (cadence ≈ 12.3 s)
                water_mark stored = 98.08   mgmt_state breakeven_applied = false
12:37 (1m)      high 101.21  — one cent short of the stop
12:46 (1m)      high 101.23  → CLOSE vpos=44 exit=101.23 net −2.1305 reason=sl  @ 12:46:59
```

- **The venue printed through the arm level. The 12-second poller's best reading was 22 cents short of it.**
- Had the poller sampled the wick, the lock would have sat at 99.10 and the trade would have closed near break-even instead of −1.110R.
- That is one observation of a poll-cadence limit meeting a CPI wick. It says nothing about entries. It is not measured across the book here.

---

## 5. VERDICT — candidates, with n, ΣR and every control

**Substitute population.** 4,494 gate-passed signals that the advisor refused (`status = ai_skipped`), 2026-06-08 → 09-11, with forward drift at 4h/12h/24h.
- Drift is signed toward the would-be direction, `skip_attribution.py:11-13`: **positive = the price went the trade's way.**
- It is **drift, not R**, and its effective n is a count of **days**.
- For a shape to be "worse", A must drift lower than B.

| # | candidate shape (A vs B) | knowable at entry? | book LIVE n · ΣR | book PAPER n · ΣR | substitute: cells clearing raw α | day-matched | 12-window | paper/live era sign | **verdict** |
|---|---|---|---|---|---|---|---|---|---|
| S1 | single contributing category vs ≥ 2 | **yes** (breakdown) | 6 · −0.710 | 5 · **+5.156** | 0/6 (SHORT 4h p = 1.35e-3, just above α) | best p 1.8e-2 | SHORT 4h **10/12** | SHORT 4h holds (−0.127 / −0.196) | **dies** (raw, day) |
| S2 | ≥ 2 categories zeroed vs 0 | **yes** | 2 (3-zeroed) · −1.158 | 6 (2-zeroed) · +0.125 | 2/6 — **both LONG, both the WRONG way** (zeroed drifted **better**, +0.43 % / +0.63 %) | 0 | ≤ 9/12 | — | **dies** |
| S3 | raw in [2.00, 2.25) vs ≥ 2.25 | **yes** | 1 · −1.110 | 0 | 0/6 | 0 | ≤ 3/12 (8–9 unusable) | — | **dies** |
| S4 | news-flipped (raw < 2) vs raw ≥ 2 | **yes** | 3 · +1.205 | 2 · +2.594 | 2/6 — **both LONG, the WRONG way** (flipped drifted better) | 0 | ≤ 6/12 | — | **dies** |
| S5 | lone EXECUTION vs lone LIQUIDITY | **yes** | 2 · −1.866 | 0 | 0/6 | 0 | ≤ 4/12 | — | **dies** |
| S6 | −120..−30 m before a release vs rest | **yes** (static calendar) | 1 · −1.110 | 0 | 0/6 | 0 (3–4 days) | **0/12 usable** | n < 8 | **dies — unrankable** |
| S7 | 1H NEUTRAL and 15m not confirming (the `neutral_15m` clause, in DRYRUN) vs rest | **yes** | 2 · −1.866 (vpos 36, 44) | 1 · +1.257 (vpos 25) | 2/6 — SHORT 4h p = 6.8e-5, 12h p = 1.5e-4 | **0** (best 5.4e-3) | 8/12 | **flips**: paper −0.251 / live +0.069 | **dies** |
| N | news term (54-cell family) | **yes** | — | — | **26/54** | **0/54** | — | — | **dies — a clock** |

🔴 **Nothing separates.**
- **0 of 42 shape cells** and **0 of 54 news cells** survive.
- Of the 6 shape cells that clear raw Bonferroni, **4 point the wrong way**: the operator's shape drifts *better*. **All 6 die when the comparison is made inside a single day.**
- **No candidate needs the outcome.** Every one is computed from the matrix breakdown, the news term and the static calendar at decision time, so every one was a legal rule, and every one fails the same bar the twenty-eight before it failed.
- **The book cannot rank any of them.** The operator's exact shape (three categories zeroed, one 5m signal, raw 2.00) has happened **once**.

**What IS known, and none of it needed the population:**
1. For a single-signal entry, the **2.00 bar is a weight lookup with a headline override**: 100% pass with news +1.0, 0% with news −1.0 (§2c). It refused 9 of 3,631 signals with two or more categories in the bot's life.
2. The gate compared **3.00**; the weight term is stored and not gated; **the news term did not flip this entry** (§3a).
3. The entry passed the cascade because `neutral_15m` is in **DRYRUN** (§0). Measured as S7, that shape **dies**.
4. CPI's pre-print hour is **ordinary air** (1.13× / 0.85× on 10 and 22 releases). The disturbance is −5..+10 with a tail. The entry band holds **one** book trade.

**No change is proposed. Nothing was applied.**

---

## READ-ONLY CONFIRMATION

| check | result |
|---|---|
| guard pre-flight | `titan-bot/tools/openitems_guard.py` **EXIT = 0** (header and current-state table agree with runtime, 14 watched values), run with `PYTHONDONTWRITEBYTECODE=1` |
| DB | every connection `file:/…/mercury-sol/trades.db?mode=ro` (URI read-only), **SELECT only** |
| cwd | every command ran from `/tmp`, the session scratchpad, or `/root`, all **outside SOL's tree**. The one process with its cwd inside the tree is the service's own `optimizer_listener` |
| config | `config.py` and `signal_matrix.py` read **as text** (grep / regex). **No SOL module was imported** by any script in this session |
| writes | **none** in SOL's tree, SOL's DB or Titan. Scratch output only in the session scratchpad and this report file |
| orders | **none**. No authenticated venue call. Network: Bybit public `/v5/market/kline` GET over Tor SOCKS; BLS / ALFRED public GETs (BLS refused, ALFRED unreachable) |
| service | `mercury-sol.service` untouched — MainPID **1181897** before and after, ActiveEnter 2026-09-11 05:40:08 |
| **NRestarts** | **0 before, 0 after** |
| file hashes | **41 of 42 byte-identical.** The one that moved is `oi_cache.json`, the live bot's own open-interest cache, rewritten by the bot during the audit (the same file moved in the 09-04 audit). No `.py`, no config, no `.env` changed |
| **`FLAT_ADX_GATE_DRYRUN`** | **still `True`** (`config.py:407`) |
| **book-gate counter** | untouched by this session. `sol_book_gate_review.json` was rewritten at **17:00:04 by its own 30-minute cron**: `last_run` 16:30:03 → 17:00:03, LONG evaluations 14 → 15 (one new gate evaluation by the live bot), `fired` `{}` before and after. `BOOK_GATE_DRYRUN = False` unchanged |
| Titan | untouched beyond the guard: `git status -- titan-bot` clean, HEAD **cd0f175** |


---

## APPENDIX A — every book entry, as computed (raw from the breakdown on the traded side)

```
vpos  7 paper LONG  06-14 23:50 R=+2.089 exit_signal      raw=2.50 news=+0.0 gate=2.50 wadj=0.7 contrib=['TREND'] intra=['MOMENTUM', 'EXECUTION'] inter=[] opp=['LIQUIDITY'] trig='Bullish OB Created' regime=TREND next=FOMC in 3970m since_last=6440m
vpos  8 paper LONG  06-20 07:00 R=-0.739 exit_signal      raw=4.75 news=+0.0 gate=4.75 wadj=-0.3 contrib=['TREND', 'LIQUIDITY'] intra=['MOMENTUM'] inter=[] opp=[] trig='Bullish Imbalance Mitigated' regime=TREND next=NFP in 17610m since_last=3660m
vpos  9 paper LONG  06-21 02:50 R=-0.264 exit_signal      raw=4.00 news=+0.0 gate=4.00 wadj=0.3 contrib=['TREND', 'MOMENTUM'] intra=['LIQUIDITY', 'EXECUTION'] inter=[] opp=[] trig='Bullish OB Created' regime=TREND next=NFP in 16420m since_last=4850m
vpos 10 paper SHORT 06-22 00:00 R=-1.066 sl               raw=6.00 news=+0.0 gate=6.00 wadj=1.4 contrib=['TREND', 'MOMENTUM', 'EXECUTION'] intra=['LIQUIDITY'] inter=[] opp=[] trig='Within Bearish OB' regime=TREND next=NFP in 15149m since_last=6121m
vpos 11 paper SHORT 06-23 00:30 R=+1.133 exit_signal      raw=2.50 news=+0.0 gate=2.50 wadj=0.9 contrib=['TREND'] intra=['MOMENTUM', 'EXECUTION'] inter=[] opp=['LIQUIDITY'] trig='Bearish I-BOS' regime=TREND next=NFP in 13680m since_last=7590m
vpos 12 paper LONG  06-24 02:25 R=-1.049 sl               raw=3.75 news=+0.0 gate=3.75 wadj=-0.35 contrib=['TREND', 'LIQUIDITY'] intra=['MOMENTUM', 'EXECUTION'] inter=[] opp=[] trig='Bullish Breaker' regime=TREND next=NFP in 12125m since_last=9145m
vpos 13 paper SHORT 06-24 13:25 R=+1.337 trail            raw=1.75 news=+1.0 gate=2.75 wadj=1.5 contrib=['MOMENTUM'] intra=['EXECUTION'] inter=[] opp=['LIQUIDITY'] trig='Bearish OB Created' regime=FLAT next=NFP in 11465m since_last=9805m
vpos 14 paper SHORT 06-25 14:00 R=-1.032 sl               raw=3.75 news=+1.0 gate=4.75 wadj=1.5 contrib=['TREND', 'EXECUTION'] intra=['MOMENTUM'] inter=['LIQUIDITY'] opp=[] trig='Bearish OB Mitigated' regime=TREND next=NFP in 9990m since_last=11280m
vpos 15 paper SHORT 07-08 05:05 R=+0.140 trail            raw=4.25 news=+1.0 gate=5.25 wadj=1.5 contrib=['TREND', 'EXECUTION'] intra=['MOMENTUM'] inter=[] opp=[] trig='Within Bearish OB' regime=TREND next=CPI in 9085m since_last=8195m
vpos 16 paper LONG  07-10 08:30 R=-1.146 sl               raw=5.75 news=+0.0 gate=5.75 wadj=0.6 contrib=['TREND', 'MOMENTUM', 'EXECUTION'] intra=['LIQUIDITY'] inter=[] opp=[] trig='Within Bullish OB' regime=TREND next=CPI in 6000m since_last=11280m
vpos 17 paper SHORT 07-13 03:10 R=+0.004 sl               raw=3.75 news=-1.0 gate=2.75 wadj=-1.4136 contrib=['TREND', 'EXECUTION'] intra=['LIQUIDITY'] inter=[] opp=[] trig='Bearish OB Created' regime=TREND next=CPI in 2000m since_last=15280m
vpos 18 paper LONG  07-14 15:45 R=-1.074 sl               raw=6.25 news=+1.0 gate=7.25 wadj=1.5 contrib=['TREND', 'MOMENTUM', 'EXECUTION'] intra=[] inter=['LIQUIDITY'] opp=[] trig='Bullish OB Entered' regime=TREND next=FOMC in 21735m since_last=195m
vpos 19 paper SHORT 07-16 00:25 R=+0.463 exit_signal      raw=4.25 news=+0.0 gate=4.25 wadj=0.15 contrib=['TREND', 'MOMENTUM'] intra=['EXECUTION'] inter=['LIQUIDITY'] opp=[] trig='Bearish I-CHOCH+' regime=TREND next=FOMC in 19775m since_last=2155m
vpos 20 paper SHORT 07-17 13:40 R=-1.124 sl               raw=3.00 news=+1.0 gate=4.00 wadj=1.5 contrib=['MOMENTUM', 'EXECUTION'] intra=['TREND', 'LIQUIDITY'] inter=[] opp=[] trig='Bearish OB Mitigated' regime=FLAT next=FOMC in 17539m since_last=4391m
vpos 21 paper LONG  07-19 06:50 R=+0.285 trail            raw=4.75 news=+0.0 gate=4.75 wadj=0.9822 contrib=['TREND', 'EXECUTION'] intra=['MOMENTUM'] inter=['LIQUIDITY'] opp=[] trig='Bullish OB Created' regime=TREND next=FOMC in 15070m since_last=6860m
vpos 22 paper LONG  07-21 03:10 R=-1.064 sl               raw=5.75 news=-1.0 gate=4.75 wadj=-1.5 contrib=['TREND', 'MOMENTUM', 'EXECUTION'] intra=['LIQUIDITY'] inter=[] opp=[] trig='Bullish I-BOS' regime=TREND next=FOMC in 12410m since_last=9520m
vpos 23 paper SHORT 07-28 11:05 R=-0.577 exit_signal      raw=3.50 news=+1.0 gate=4.50 wadj=1.5 contrib=['MOMENTUM', 'LIQUIDITY'] intra=['EXECUTION'] inter=[] opp=[] trig='Bearish I-CHOCH+' regime=FLAT next=FOMC in 1855m since_last=20075m
vpos 24 paper SHORT 07-29 20:05 R=-1.050 sl               raw=5.00 news=+0.0 gate=5.00 wadj=0.6769 contrib=['TREND', 'MOMENTUM'] intra=['EXECUTION'] inter=['LIQUIDITY'] opp=[] trig='Bearish S-CHOCH' regime=TREND next=NFP in 12505m since_last=125m
vpos 25 paper SHORT 08-01 17:20 R=+1.257 trail            raw=1.75 news=+1.0 gate=2.75 wadj=1.5 contrib=['LIQUIDITY'] intra=['MOMENTUM'] inter=[] opp=[] trig='Bearish New Imbalance' regime=FLAT next=NFP in 8350m since_last=4280m
vpos 26 paper LONG  08-02 05:00 R=-1.085 sl               raw=5.50 news=+0.0 gate=5.50 wadj=0.3778 contrib=['TREND', 'MOMENTUM', 'EXECUTION'] intra=[] inter=[] opp=[] trig='Bullish OB Created' regime=TREND next=NFP in 7650m since_last=4980m
vpos 27 paper SHORT 08-03 06:45 R=-0.660 sl               raw=2.50 news=+1.0 gate=3.50 wadj=1.3265 contrib=['TREND'] intra=['MOMENTUM', 'LIQUIDITY'] inter=[] opp=[] trig='Bearish New Imbalance' regime=TREND next=NFP in 6105m since_last=6525m
vpos 28 paper SHORT 08-06 19:00 R=-0.153 exit_signal      raw=4.00 news=-1.0 gate=3.00 wadj=-1.5 contrib=['TREND', 'MOMENTUM'] intra=['LIQUIDITY'] inter=[] opp=[] trig='Bearish New Imbalance' regime=TREND next=NFP in 1049m since_last=11581m
vpos 29 live  LONG  08-08 08:50 R=+1.355 exchange_UNKNOWN raw=4.50 news=-1.0 gate=3.50 wadj=None contrib=['TREND', 'EXECUTION'] intra=['MOMENTUM'] inter=[] opp=[] trig='Bullish OB Entered' regime=TREND next=CPI in 5980m since_last=1220m
vpos 30 live  LONG  08-08 21:10 R=+0.762 trail            raw=4.25 news=+0.0 gate=4.25 wadj=0.6653 contrib=['MOMENTUM', 'EXECUTION'] intra=[] inter=[] opp=[] trig='Bullish I-BOS' regime=FLAT next=CPI in 5240m since_last=1960m
vpos 31 live  LONG  08-10 08:10 R=-1.155 sl               raw=4.50 news=+1.0 gate=5.50 wadj=1.5 contrib=['TREND', 'EXECUTION'] intra=['MOMENTUM'] inter=[] opp=[] trig='Bullish OB Entered' regime=TREND next=CPI in 3140m since_last=4060m
vpos 32 live  SHORT 08-10 15:15 R=-0.180 exit_signal      raw=4.25 news=-1.0 gate=3.25 wadj=-1.5 contrib=['TREND', 'EXECUTION'] intra=['MOMENTUM'] inter=['LIQUIDITY'] opp=[] trig='Within Bearish OB' regime=TREND next=CPI in 2714m since_last=4486m
vpos 33 live  LONG  08-11 22:00 R=-0.049 exit_signal      raw=2.50 news=+1.0 gate=3.50 wadj=1.5 contrib=['TREND'] intra=['MOMENTUM', 'LIQUIDITY', 'EXECUTION'] inter=[] opp=[] trig='Bullish I-BOS' regime=TREND next=CPI in 870m since_last=6330m
vpos 34 live  SHORT 08-13 16:40 R=-0.643 sl               raw=1.75 news=+1.0 gate=2.75 wadj=0.6732 contrib=['MOMENTUM'] intra=['EXECUTION'] inter=[] opp=[] trig='Bearish I-BOS' regime=FLAT next=NFP in 31430m since_last=1690m
vpos 35 live  SHORT 08-14 14:20 R=-0.701 sl               raw=1.75 news=+1.0 gate=2.75 wadj=0.4807 contrib=['MOMENTUM'] intra=['EXECUTION'] inter=[] opp=['LIQUIDITY'] trig='Bearish I-BOS' regime=FLAT next=NFP in 30130m since_last=2990m
vpos 36 live  SHORT 08-15 07:50 R=-0.757 exchange_market  raw=2.50 news=+0.0 gate=2.50 wadj=0.3106 contrib=['EXECUTION'] intra=['MOMENTUM'] inter=[] opp=['LIQUIDITY'] trig='Bearish OB Created' regime=FLAT next=NFP in 29080m since_last=4040m
vpos 37 live  SHORT 08-16 22:05 R=-1.226 sl               raw=6.00 news=+0.0 gate=6.00 wadj=0.2967 contrib=['TREND', 'MOMENTUM', 'EXECUTION'] intra=['LIQUIDITY'] inter=[] opp=[] trig='Within Bearish OB' regime=TREND next=NFP in 26785m since_last=6335m
vpos 38 live  LONG  08-18 22:20 R=+4.031 trail            raw=4.00 news=+0.0 gate=4.00 wadj=0.1998 contrib=['TREND', 'MOMENTUM'] intra=['LIQUIDITY'] inter=[] opp=[] trig='Bullish New Imbalance' regime=TREND next=NFP in 23890m since_last=9230m
vpos 39 live  LONG  08-20 23:30 R=+1.604 trail            raw=3.50 news=+0.0 gate=3.50 wadj=0.5032 contrib=['MOMENTUM', 'LIQUIDITY'] intra=['EXECUTION'] inter=[] opp=[] trig='Bullish OB Created' regime=FLAT next=NFP in 20940m since_last=12180m
vpos 40 live  LONG  08-21 21:15 R=+2.549 trail            raw=1.75 news=+1.0 gate=2.75 wadj=1.2474 contrib=['MOMENTUM'] intra=['EXECUTION'] inter=[] opp=[] trig='Bullish OB Created' regime=FLAT next=NFP in 19635m since_last=13485m
vpos 41 live  LONG  08-27 03:50 R=+1.633 trail            raw=4.25 news=+0.0 gate=4.25 wadj=0.14 contrib=['TREND', 'EXECUTION'] intra=['MOMENTUM'] inter=[] opp=[] trig='Within Bullish OB' regime=TREND next=NFP in 12040m since_last=21080m
vpos 42 live  SHORT 09-01 21:40 R=-1.083 sl               raw=5.75 news=+0.0 gate=5.75 wadj=0.3708 contrib=['TREND', 'MOMENTUM', 'LIQUIDITY'] intra=[] inter=[] opp=[] trig='Bearish New Imbalance' regime=TREND next=NFP in 3770m since_last=29350m
vpos 43 live  LONG  09-05 13:05 R=+1.723 trail            raw=6.75 news=+0.0 gate=6.75 wadj=0.7295 contrib=['TREND', 'MOMENTUM', 'EXECUTION'] intra=['LIQUIDITY'] inter=[] opp=[] trig='Within Bullish OB' regime=TREND next=CPI in 8605m since_last=1475m
vpos 44 live  SHORT 09-11 11:50 R=-1.110 sl               raw=2.00 news=+1.0 gate=3.00 wadj=0.24 contrib=['EXECUTION'] intra=['TREND', 'MOMENTUM', 'LIQUIDITY'] inter=[] opp=[] trig='Bearish OB Entered' regime=FLAT next=CPI in 40m since_last=10040m
```

## APPENDIX B — substitute population, SHAPE family (42 cells), raw output

Columns: nA (days carrying A) / nB · mean drift A / B (%, + = the trade's way) · Welch t, p (✱ = clears α 0.00119) · day-matched t, p · 12-window agree/wrong/unusable · paper-era and live-era nA/nB and diff · verdict.

```
cohort: 7707 refusals with drift; degraded samples flagged (kept): 19
span: 2026-06-08 00:40:13+00:00 -> 2026-09-11 16:00:23+00:00

SHAPE FAMILY — gate-passed (ai_skipped) n=4494; alpha = 0.05/36 = 0.00139
FAMILY SIZE = 7 contrasts x 2 sides x 3 horizons = 42 cells; alpha = 0.05/42 = 0.00119
 side LONG
  S1 lone contributor vs >=2 contributors       4h  nA=  497 (days  74) nB= 1579  mA=+0.056% mB=+0.046% diff=+0.010  t=+0.17 p=8.68e-01  | day-matched 73d t=-1.34 p=1.83e-01  | 12w 6/6/0u | paper:346/1165 -0.058 live:151/414 +0.161 | dies
  S1 lone contributor vs >=2 contributors      12h  nA=  496 (days  74) nB= 1558  mA=+0.294% mB=+0.129% diff=+0.164  t=+1.80 p=7.22e-02  | day-matched 73d t=-1.84 p=6.99e-02  | 12w 8/4/0u | paper:346/1157 +0.017 live:150/401 +0.503 | dies
  S1 lone contributor vs >=2 contributors      24h  nA=  495 (days  73) nB= 1554  mA=+0.650% mB=+0.277% diff=+0.372  t=+2.58 p=9.96e-03  | day-matched 72d t=-1.83 p=7.10e-02  | 12w 10/2/0u | paper:346/1157 +0.071 live:149/397 +1.052 | dies
  S2 >=2 cats intra-zeroed vs 0 zeroed          4h  nA=  354 (days  69) nB=  801  mA=+0.155% mB=-0.007% diff=+0.162  t=+1.77 p=7.80e-02  | day-matched 68d t=+0.84 p=4.04e-01  | 12w 7/5/0u | paper:263/581 +0.060 live:91/220 +0.459 | dies
  S2 >=2 cats intra-zeroed vs 0 zeroed         12h  nA=  350 (days  68) nB=  793  mA=+0.469% mB=+0.036% diff=+0.433  t=+3.59 p=3.54e-04✱ | day-matched 67d t=-0.53 p=5.96e-01  | 12w 9/3/0u | paper:263/573 +0.322 live:87/220 +0.772 | dies
  S2 >=2 cats intra-zeroed vs 0 zeroed         24h  nA=  350 (days  68) nB=  790  mA=+0.947% mB=+0.319% diff=+0.628  t=+3.30 p=1.01e-03✱ | day-matched 67d t=-1.18 p=2.42e-01  | 12w 9/3/0u | paper:263/573 +0.387 live:87/217 +1.372 | dies
  S3 raw in [2.00,2.25) vs raw >=2.25           4h  nA=   56 (days  31) nB= 1905  mA=+0.164% mB=+0.023% diff=+0.142  t=+1.42 p=1.60e-01  | day-matched 31d t=+0.66 p=5.15e-01  | 12w 2/1/9u | paper:38/1401 +0.181 live:18/504 +0.045 | dies
  S3 raw in [2.00,2.25) vs raw >=2.25          12h  nA=   56 (days  31) nB= 1883  mA=+0.485% mB=+0.111% diff=+0.374  t=+1.65 p=1.04e-01  | day-matched 31d t=+1.44 p=1.60e-01  | 12w 3/0/9u | paper:38/1393 +0.416 live:18/490 +0.280 | dies
  S3 raw in [2.00,2.25) vs raw >=2.25          24h  nA=   56 (days  31) nB= 1878  mA=+0.510% mB=+0.274% diff=+0.236  t=+0.66 p=5.09e-01  | day-matched 31d t=+0.62 p=5.41e-01  | 12w 2/1/9u | paper:38/1393 -0.236 live:18/485 +1.203 | dies
  S4 news-flipped (raw<2) vs raw>=2             4h  nA=  115 (days  39) nB= 1961  mA=+0.420% mB=+0.027% diff=+0.394  t=+2.56 p=1.17e-02  | day-matched 38d t=+0.09 p=9.30e-01  | 12w 5/2/5u | paper:72/1439 +0.287 live:43/522 +0.552 | dies
  S4 news-flipped (raw<2) vs raw>=2            12h  nA=  115 (days  39) nB= 1939  mA=+0.962% mB=+0.122% diff=+0.840  t=+3.70 p=3.23e-04✱ | day-matched 38d t=-0.30 p=7.68e-01  | 12w 6/1/5u | paper:72/1431 +0.365 live:43/508 +1.626 | dies
  S4 news-flipped (raw<2) vs raw>=2            24h  nA=  115 (days  39) nB= 1934  mA=+1.826% mB=+0.281% diff=+1.545  t=+4.14 p=6.44e-05✱ | day-matched 38d t=+0.20 p=8.45e-01  | 12w 6/1/5u | paper:72/1431 +0.667 live:43/503 +2.957 | dies
  S5 lone EXECUTION vs lone LIQUIDITY           4h  nA=  230 (days  50) nB=   91  mA=+0.214% mB=+0.072% diff=+0.142  t=+1.04 p=2.98e-01  | day-matched 33d t=+0.24 p=8.10e-01  | 12w 2/3/7u | paper:156/54 +0.099 live:74/37 +0.279 | dies
  S5 lone EXECUTION vs lone LIQUIDITY          12h  nA=  230 (days  50) nB=   91  mA=+0.439% mB=-0.025% diff=+0.464  t=+2.08 p=3.88e-02  | day-matched 33d t=+0.84 p=4.09e-01  | 12w 4/1/7u | paper:156/54 +0.414 live:74/37 +0.715 | dies
  S5 lone EXECUTION vs lone LIQUIDITY          24h  nA=  229 (days  49) nB=   91  mA=+0.855% mB=+0.255% diff=+0.600  t=+1.65 p=1.02e-01  | day-matched 33d t=+0.44 p=6.61e-01  | 12w 3/2/7u | paper:156/54 +0.484 live:73/37 +1.149 | dies
  S6 -120..-30m before event vs rest            4h  nA=    6 (days   4) nB= 2070  mA=+2.596% mB=+0.041% diff=+2.555  t=+5.07 p=3.80e-03  | day-matched 4d t=+1.58 p=2.12e-01  | 12w 0/0/12u | paper:5/1506 n<8 live:1/564 n<8 | dies
  S6 -120..-30m before event vs rest           12h  nA=    5 (days   3) nB= 2049  mA=+0.380% mB=+0.169% diff=+0.212  t=+0.24 p=8.21e-01  | day-matched 3d t=-0.07 p=9.53e-01  | 12w 0/0/12u | paper:5/1498 n<8 live:0/551 n<8 | dies
  S6 -120..-30m before event vs rest           24h  nA=    5 (days   3) nB= 2044  mA=+2.972% mB=+0.361% diff=+2.611  t=+5.41 p=5.19e-03  | day-matched 3d t=+0.48 p=6.81e-01  | 12w 0/0/12u | paper:5/1498 n<8 live:0/546 n<8 | dies
  S7 1H neutral AND 15m not confirming vs rest  4h  nA=  587 (days  61) nB= 1489  mA=+0.103% mB=+0.027% diff=+0.076  t=+1.37 p=1.70e-01  | day-matched 59d t=+1.35 p=1.83e-01  | 12w 4/6/2u | paper:389/1122 +0.076 live:198/367 +0.049 | dies
  S7 1H neutral AND 15m not confirming vs rest 12h  nA=  586 (days  61) nB= 1468  mA=+0.157% mB=+0.174% diff=-0.017  t=-0.20 p=8.43e-01  | day-matched 59d t=+1.11 p=2.71e-01  | 12w 3/7/2u | paper:389/1114 -0.118 live:197/354 +0.170 | dies
  S7 1H neutral AND 15m not confirming vs rest 24h  nA=  585 (days  60) nB= 1464  mA=+0.354% mB=+0.373% diff=-0.019  t=-0.14 p=8.89e-01  | day-matched 58d t=+0.70 p=4.90e-01  | 12w 5/5/2u | paper:389/1114 -0.233 live:196/350 +0.345 | dies
 side SHORT
  S1 lone contributor vs >=2 contributors       4h  nA=  641 (days  78) nB= 1762  mA=-0.056% mB=+0.097% diff=-0.153  t=-3.21 p=1.35e-03  | day-matched 77d t=-2.42 p=1.78e-02  | 12w 10/2/0u | paper:464/1334 -0.127 live:177/428 -0.196 | dies
  S1 lone contributor vs >=2 contributors      12h  nA=  640 (days  78) nB= 1761  mA=-0.174% mB=-0.050% diff=-0.124  t=-1.40 p=1.63e-01  | day-matched 77d t=-0.43 p=6.66e-01  | 12w 7/5/0u | paper:464/1334 -0.129 live:176/427 +0.003 | dies
  S1 lone contributor vs >=2 contributors      24h  nA=  636 (days  77) nB= 1747  mA=-0.314% mB=-0.348% diff=+0.034  t=+0.29 p=7.74e-01  | day-matched 76d t=+0.03 p=9.74e-01  | 12w 4/8/0u | paper:464/1334 -0.121 live:172/413 +0.654 | dies
  S2 >=2 cats intra-zeroed vs 0 zeroed          4h  nA=  368 (days  70) nB=  997  mA=+0.017% mB=+0.085% diff=-0.068  t=-1.18 p=2.38e-01  | day-matched 70d t=+0.07 p=9.48e-01  | 12w 6/6/0u | paper:274/757 -0.129 live:94/240 +0.126 | dies
  S2 >=2 cats intra-zeroed vs 0 zeroed         12h  nA=  367 (days  69) nB=  997  mA=+0.030% mB=-0.175% diff=+0.205  t=+1.75 p=8.04e-02  | day-matched 69d t=+0.70 p=4.85e-01  | 12w 6/6/0u | paper:274/757 +0.137 live:93/240 +0.458 | dies
  S2 >=2 cats intra-zeroed vs 0 zeroed         24h  nA=  366 (days  69) nB=  985  mA=-0.186% mB=-0.288% diff=+0.102  t=+0.64 p=5.24e-01  | day-matched 69d t=+0.62 p=5.35e-01  | 12w 4/8/0u | paper:274/757 +0.007 live:92/228 +0.505 | dies
  S3 raw in [2.00,2.25) vs raw >=2.25           4h  nA=   68 (days  36) nB= 2145  mA=-0.263% mB=+0.059% diff=-0.322  t=-2.53 p=1.36e-02  | day-matched 36d t=-0.87 p=3.91e-01  | 12w 3/1/8u | paper:45/1616 -0.356 live:23/529 -0.194 | dies
  S3 raw in [2.00,2.25) vs raw >=2.25          12h  nA=   68 (days  36) nB= 2143  mA=-0.712% mB=-0.098% diff=-0.615  t=-2.60 p=1.13e-02  | day-matched 36d t=-0.50 p=6.21e-01  | 12w 3/1/8u | paper:45/1616 -0.649 live:23/527 -0.287 | dies
  S3 raw in [2.00,2.25) vs raw >=2.25          24h  nA=   68 (days  36) nB= 2126  mA=-0.983% mB=-0.352% diff=-0.631  t=-2.01 p=4.84e-02  | day-matched 36d t=+0.48 p=6.32e-01  | 12w 3/1/8u | paper:45/1616 -0.810 live:23/510 +0.161 | dies
  S4 news-flipped (raw<2) vs raw>=2             4h  nA=  190 (days  46) nB= 2213  mA=+0.137% mB=+0.049% diff=+0.088  t=+0.96 p=3.37e-01  | day-matched 46d t=-0.86 p=3.94e-01  | 12w 3/4/5u | paper:137/1661 +0.136 live:53/552 -0.012 | dies
  S4 news-flipped (raw<2) vs raw>=2            12h  nA=  190 (days  46) nB= 2211  mA=+0.303% mB=-0.116% diff=+0.419  t=+2.90 p=4.14e-03  | day-matched 46d t=-0.19 p=8.54e-01  | 12w 5/2/5u | paper:137/1661 +0.381 live:53/550 +0.621 | dies
  S4 news-flipped (raw<2) vs raw>=2            24h  nA=  189 (days  46) nB= 2194  mA=+0.033% mB=-0.371% diff=+0.404  t=+2.13 p=3.38e-02  | day-matched 46d t=-0.15 p=8.81e-01  | 12w 4/3/5u | paper:137/1661 +0.114 live:52/533 +1.345 | dies
  S5 lone EXECUTION vs lone LIQUIDITY           4h  nA=  330 (days  55) nB=  104  mA=-0.145% mB=-0.120% diff=-0.025  t=-0.26 p=7.98e-01  | day-matched 37d t=-0.95 p=3.48e-01  | 12w 4/3/5u | paper:237/72 +0.028 live:93/32 -0.170 | dies
  S5 lone EXECUTION vs lone LIQUIDITY          12h  nA=  330 (days  55) nB=  104  mA=-0.316% mB=-0.413% diff=+0.097  t=+0.57 p=5.68e-01  | day-matched 37d t=-1.75 p=8.85e-02  | 12w 4/3/5u | paper:237/72 +0.156 live:93/32 -0.104 | dies
  S5 lone EXECUTION vs lone LIQUIDITY          24h  nA=  329 (days  55) nB=  101  mA=-0.493% mB=-0.453% diff=-0.041  t=-0.17 p=8.67e-01  | day-matched 37d t=-1.52 p=1.36e-01  | 12w 2/4/6u | paper:237/72 +0.198 live:92/29 -0.663 | dies
  S6 -120..-30m before event vs rest            4h  nA=   14 (days   4) nB= 2389  mA=+0.194% mB=+0.055% diff=+0.139  t=+0.26 p=8.02e-01  | day-matched 4d t=-0.35 p=7.52e-01  | 12w 0/0/12u | paper:11/1787 -0.599 live:3/602 n<8 | dies
  S6 -120..-30m before event vs rest           12h  nA=   14 (days   4) nB= 2387  mA=-0.038% mB=-0.083% diff=+0.046  t=+0.10 p=9.22e-01  | day-matched 4d t=-0.06 p=9.56e-01  | 12w 0/0/12u | paper:11/1787 -0.838 live:3/600 n<8 | dies
  S6 -120..-30m before event vs rest           24h  nA=   14 (days   4) nB= 2369  mA=-1.339% mB=-0.333% diff=-1.006  t=-1.95 p=7.25e-02  | day-matched 4d t=-0.23 p=8.30e-01  | 12w 0/0/12u | paper:11/1787 -2.257 live:3/582 n<8 | dies
  S7 1H neutral AND 15m not confirming vs rest  4h  nA=  682 (days  63) nB= 1721  mA=-0.072% mB=+0.107% diff=-0.179  t=-4.00 p=6.81e-05✱ | day-matched 62d t=-2.88 p=5.42e-03  | 12w 8/2/2u | paper:468/1330 -0.251 live:214/391 +0.069 | dies
  S7 1H neutral AND 15m not confirming vs rest 12h  nA=  682 (days  63) nB= 1719  mA=-0.314% mB=+0.008% diff=-0.322  t=-3.81 p=1.46e-04✱ | day-matched 62d t=-0.95 p=3.45e-01  | 12w 8/2/2u | paper:468/1330 -0.397 live:214/389 +0.144 | dies
  S7 1H neutral AND 15m not confirming vs rest 24h  nA=  673 (days  62) nB= 1710  mA=-0.435% mB=-0.301% diff=-0.134  t=-1.16 p=2.47e-01  | day-matched 61d t=-0.53 p=5.99e-01  | 12w 7/3/2u | paper:468/1330 -0.200 live:205/380 +0.448 | dies

context — gate-passed shape counts per side:
  LONG n_intra: {0: 803, 1: 921, 2: 330, 3: 24} n_contrib: {1: 497, 2: 1196, 3: 361, 4: 24} lone cat: {'TREND': 92, 'MOMENTUM': 84, 'LIQUIDITY': 91, 'EXECUTION': 230} pre-band: 6 pre-band days: 4
  SHORT n_intra: {0: 997, 1: 1045, 2: 343, 3: 31} n_contrib: {1: 648, 2: 1315, 3: 424, 4: 29} lone cat: {'TREND': 91, 'MOMENTUM': 116, 'LIQUIDITY': 106, 'EXECUTION': 335} pre-band: 14 pre-band days: 4

```

## APPENDIX C — NEWS family (54 cells), raw output

```
NEWS FAMILY — replication of 2026-08-10; alpha = 0.05/54 = 0.000926
classes: news+ = macro_gate_penalty +1.0, news- = -1.0, news0 = 0.0; blackout-window rows (-2.5/-1.5/-3.5) EXCLUDED
rows in news family: 7666 excluded (window/NULL): 41
  LONG  below_threshold news+ vs news0          4h  nA=  124 (days  42) nB=  845  mA=+0.153% mB=+0.230% diff=-0.076  t=-0.55 p=5.85e-01  | day-matched 40d t=+0.00 p=9.97e-01  | 12w 4/4/4u | paper:54/503 -0.132 live:70/342 -0.072 | dies
  LONG  below_threshold news- vs news0          4h  nA=  584 (days  69) nB=  845  mA=+0.038% mB=+0.230% diff=-0.192  t=-2.98 p=2.94e-03  | day-matched 59d t=+0.03 p=9.72e-01  | 12w 5/5/2u | paper:361/503 -0.150 live:223/342 -0.252 | dies
  LONG  ai_skipped      news+ vs news0          4h  nA=  551 (days  58) nB= 1050  mA=+0.154% mB=-0.017% diff=+0.171  t=+2.76 p=5.88e-03  | day-matched 52d t=+0.49 p=6.25e-01  | 12w 7/5/0u | paper:366/772 +0.141 live:185/278 +0.205 | dies
  LONG  ai_skipped      news- vs news0          4h  nA=  475 (days  59) nB= 1050  mA=+0.070% mB=-0.017% diff=+0.087  t=+1.25 p=2.13e-01  | day-matched 55d t=+0.98 p=3.33e-01  | 12w 7/4/1u | paper:373/772 +0.137 live:102/278 -0.070 | dies
  LONG  BOTH            news+ vs news0          4h  nA=  675 (days  65) nB= 1895  mA=+0.154% mB=+0.093% diff=+0.061  t=+1.09 p=2.77e-01  | day-matched 63d t=+0.56 p=5.80e-01  | 12w 7/5/0u | paper:420/1275 +0.048 live:255/620 +0.061 | dies
  LONG  BOTH            news- vs news0          4h  nA= 1059 (days  76) nB= 1895  mA=+0.052% mB=+0.093% diff=-0.041  t=-0.88 p=3.81e-01  | day-matched 73d t=+0.43 p=6.71e-01  | 12w 6/6/0u | paper:734/1275 +0.017 live:325/620 -0.161 | dies
  SHORT below_threshold news+ vs news0          4h  nA=  160 (days  38) nB=  895  mA=-0.107% mB=-0.148% diff=+0.042  t=+0.38 p=7.06e-01  | day-matched 35d t=+0.16 p=8.78e-01  | 12w 3/4/5u | paper:83/496 -0.073 live:77/399 +0.186 | dies
  SHORT below_threshold news- vs news0          4h  nA=  559 (days  62) nB=  895  mA=-0.141% mB=-0.148% diff=+0.007  t=+0.11 p=9.10e-01  | day-matched 53d t=+1.39 p=1.69e-01  | 12w 6/4/2u | paper:286/496 +0.112 live:273/399 -0.078 | dies
  SHORT ai_skipped      news+ vs news0          4h  nA=  810 (days  68) nB= 1205  mA=+0.177% mB=-0.081% diff=+0.258  t=+5.48 p=4.89e-08✱ | day-matched 64d t=-0.29 p=7.74e-01  | 12w 10/2/0u | paper:648/891 +0.231 live:162/314 +0.296 | dies
  SHORT ai_skipped      news- vs news0          4h  nA=  386 (days  54) nB= 1205  mA=+0.228% mB=-0.081% diff=+0.309  t=+5.03 p=6.59e-07✱ | day-matched 52d t=+2.28 p=2.69e-02  | 12w 9/3/0u | paper:257/891 +0.375 live:129/314 +0.228 | dies
  SHORT BOTH            news+ vs news0          4h  nA=  970 (days  74) nB= 2100  mA=+0.130% mB=-0.110% diff=+0.240  t=+5.62 p=2.18e-08✱ | day-matched 71d t=+0.07 p=9.48e-01  | 12w 10/2/0u | paper:731/1387 +0.196 live:239/713 +0.275 | dies
  SHORT BOTH            news- vs news0          4h  nA=  945 (days  70) nB= 2100  mA=+0.010% mB=-0.110% diff=+0.120  t=+2.68 p=7.54e-03  | day-matched 68d t=+1.53 p=1.30e-01  | 12w 8/4/0u | paper:543/1387 +0.237 live:402/713 +0.013 | dies
  BOTH  below_threshold news+ vs news0          4h  nA=  284 (days  60) nB= 1740  mA=+0.007% mB=+0.035% diff=-0.028  t=-0.33 p=7.45e-01  | day-matched 60d t=-0.53 p=5.95e-01  | 12w 4/6/2u | paper:137/999 -0.117 live:147/741 +0.072 | dies
  BOTH  below_threshold news- vs news0          4h  nA= 1143 (days  86) nB= 1740  mA=-0.050% mB=+0.035% diff=-0.085  t=-1.86 p=6.27e-02  | day-matched 77d t=-0.27 p=7.88e-01  | 12w 7/3/2u | paper:647/999 -0.023 live:496/741 -0.163 | dies
  BOTH  ai_skipped      news+ vs news0          4h  nA= 1361 (days  81) nB= 2255  mA=+0.168% mB=-0.051% diff=+0.219  t=+5.82 p=6.66e-09✱ | day-matched 79d t=+0.81 p=4.21e-01  | 12w 10/2/0u | paper:1014/1663 +0.201 live:347/592 +0.267 | dies
  BOTH  ai_skipped      news- vs news0          4h  nA=  861 (days  76) nB= 2255  mA=+0.141% mB=-0.051% diff=+0.192  t=+4.08 p=4.85e-05✱ | day-matched 75d t=+1.92 p=5.82e-02  | 12w 8/4/0u | paper:630/1663 +0.231 live:231/592 +0.088 | dies
  BOTH  BOTH            news+ vs news0          4h  nA= 1645 (days  85) nB= 3995  mA=+0.140% mB=-0.014% diff=+0.153  t=+4.50 p=7.16e-06✱ | day-matched 84d t=+0.31 p=7.56e-01  | 12w 9/3/0u | paper:1151/2662 +0.135 live:494/1333 +0.189 | dies
  BOTH  BOTH            news- vs news0          4h  nA= 2004 (days  91) nB= 3995  mA=+0.032% mB=-0.014% diff=+0.046  t=+1.42 p=1.57e-01  | day-matched 90d t=+0.87 p=3.88e-01  | 12w 6/6/0u | paper:1277/2662 +0.117 live:727/1333 -0.074 | dies
  LONG  below_threshold news+ vs news0         12h  nA=  124 (days  42) nB=  845  mA=+0.624% mB=+0.422% diff=+0.202  t=+0.84 p=4.02e-01  | day-matched 40d t=-0.84 p=4.06e-01  | 12w 3/5/4u | paper:54/503 -0.281 live:70/342 +0.366 | dies
  LONG  below_threshold news- vs news0         12h  nA=  577 (days  68) nB=  845  mA=-0.008% mB=+0.422% diff=-0.430  t=-4.52 p=6.81e-06✱ | day-matched 58d t=-1.56 p=1.24e-01  | 12w 7/3/2u | paper:361/503 -0.252 live:216/342 -0.670 | dies
  LONG  ai_skipped      news+ vs news0         12h  nA=  544 (days  57) nB= 1039  mA=+0.452% mB=+0.076% diff=+0.376  t=+4.00 p=6.95e-05✱ | day-matched 51d t=+0.42 p=6.77e-01  | 12w 4/8/0u | paper:366/764 +0.371 live:178/275 +0.358 | dies
  LONG  ai_skipped      news- vs news0         12h  nA=  471 (days  58) nB= 1039  mA=+0.047% mB=+0.076% diff=-0.029  t=-0.33 p=7.42e-01  | day-matched 53d t=-0.16 p=8.77e-01  | 12w 5/6/1u | paper:373/764 +0.028 live:98/275 -0.205 | dies
  LONG  BOTH            news+ vs news0         12h  nA=  668 (days  64) nB= 1884  mA=+0.484% mB=+0.231% diff=+0.253  t=+2.87 p=4.16e-03  | day-matched 62d t=-0.13 p=8.94e-01  | 12w 6/6/0u | paper:420/1267 +0.263 live:248/617 +0.177 | dies
  LONG  BOTH            news- vs news0         12h  nA= 1048 (days  75) nB= 1884  mA=+0.017% mB=+0.231% diff=-0.215  t=-3.33 p=8.83e-04✱ | day-matched 71d t=-1.59 p=1.16e-01  | 12w 7/5/0u | paper:734/1267 -0.101 live:314/617 -0.435 | dies
  SHORT below_threshold news+ vs news0         12h  nA=  157 (days  37) nB=  895  mA=+0.301% mB=-0.293% diff=+0.594  t=+3.87 p=1.43e-04✱ | day-matched 35d t=+0.20 p=8.45e-01  | 12w 5/2/5u | paper:83/496 +0.333 live:74/399 +0.924 | dies
  SHORT below_threshold news- vs news0         12h  nA=  559 (days  62) nB=  895  mA=-0.489% mB=-0.293% diff=-0.196  t=-1.46 p=1.44e-01  | day-matched 53d t=+1.86 p=6.86e-02  | 12w 2/8/2u | paper:286/496 +0.322 live:273/399 -0.679 | dies
  SHORT ai_skipped      news+ vs news0         12h  nA=  808 (days  67) nB= 1205  mA=+0.399% mB=-0.310% diff=+0.709  t=+8.33 p=1.80e-16✱ | day-matched 63d t=-0.21 p=8.35e-01  | 12w 8/4/0u | paper:648/891 +0.693 live:160/314 +0.577 | dies
  SHORT ai_skipped      news- vs news0         12h  nA=  386 (days  54) nB= 1205  mA=-0.387% mB=-0.310% diff=-0.078  t=-0.55 p=5.82e-01  | day-matched 52d t=+0.85 p=3.97e-01  | 12w 4/8/0u | paper:257/891 +0.321 live:129/314 -0.734 | dies
  SHORT BOTH            news+ vs news0         12h  nA=  965 (days  73) nB= 2100  mA=+0.383% mB=-0.303% diff=+0.686  t=+9.40 p=1.77e-20✱ | day-matched 70d t=+0.13 p=9.00e-01  | 12w 9/3/0u | paper:731/1387 +0.612 live:234/713 +0.663 | dies
  SHORT BOTH            news- vs news0         12h  nA=  945 (days  70) nB= 2100  mA=-0.448% mB=-0.303% diff=-0.145  t=-1.49 p=1.36e-01  | day-matched 68d t=+1.05 p=2.96e-01  | 12w 5/7/0u | paper:543/1387 +0.349 live:402/713 -0.685 | dies
  BOTH  below_threshold news+ vs news0         12h  nA=  281 (days  59) nB= 1740  mA=+0.444% mB=+0.055% diff=+0.389  t=+2.85 p=4.66e-03  | day-matched 59d t=-0.05 p=9.63e-01  | 12w 7/3/2u | paper:137/999 +0.079 live:144/741 +0.690 | dies
  BOTH  below_threshold news- vs news0         12h  nA= 1136 (days  85) nB= 1740  mA=-0.245% mB=+0.055% diff=-0.299  t=-3.63 p=2.93e-04✱ | day-matched 76d t=-1.06 p=2.93e-01  | 12w 5/5/2u | paper:647/999 +0.008 live:489/741 -0.705 | dies
  BOTH  ai_skipped      news+ vs news0         12h  nA= 1352 (days  80) nB= 2244  mA=+0.420% mB=-0.131% diff=+0.552  t=+8.73 p=4.45e-18✱ | day-matched 78d t=+1.79 p=7.79e-02  | 12w 9/3/0u | paper:1014/1655 +0.558 live:338/589 +0.519 | dies
  BOTH  ai_skipped      news- vs news0         12h  nA=  857 (days  75) nB= 2244  mA=-0.149% mB=-0.131% diff=-0.018  t=-0.22 p=8.28e-01  | day-matched 74d t=+0.26 p=7.99e-01  | 12w 7/5/0u | paper:630/1655 +0.171 live:227/589 -0.540 | dies
  BOTH  BOTH            news+ vs news0         12h  nA= 1633 (days  84) nB= 3984  mA=+0.424% mB=-0.050% diff=+0.474  t=+8.44 p=4.91e-17✱ | day-matched 83d t=+0.99 p=3.26e-01  | 12w 9/3/0u | paper:1151/2654 +0.467 live:482/1330 +0.478 | dies
  BOTH  BOTH            news- vs news0         12h  nA= 1993 (days  90) nB= 3984  mA=-0.203% mB=-0.050% diff=-0.153  t=-2.67 p=7.69e-03  | day-matched 89d t=-0.32 p=7.49e-01  | 12w 7/5/0u | paper:1277/2654 +0.106 live:716/1330 -0.608 | dies
  LONG  below_threshold news+ vs news0         24h  nA=  124 (days  42) nB=  844  mA=+1.566% mB=+0.511% diff=+1.055  t=+2.78 p=6.19e-03  | day-matched 40d t=-1.52 p=1.38e-01  | 12w 6/2/4u | paper:54/503 +0.014 live:70/341 +1.613 | dies
  LONG  below_threshold news- vs news0         24h  nA=  577 (days  68) nB=  844  mA=+0.148% mB=+0.511% diff=-0.362  t=-2.64 p=8.44e-03  | day-matched 58d t=-0.61 p=5.44e-01  | 12w 6/4/2u | paper:361/503 -0.285 live:216/341 -0.424 | dies
  LONG  ai_skipped      news+ vs news0         24h  nA=  544 (days  57) nB= 1034  mA=+0.860% mB=+0.309% diff=+0.551  t=+3.62 p=3.06e-04✱ | day-matched 51d t=+0.89 p=3.78e-01  | 12w 7/5/0u | paper:366/764 +0.328 live:178/270 +0.979 | dies
  LONG  ai_skipped      news- vs news0         24h  nA=  471 (days  58) nB= 1034  mA=-0.074% mB=+0.309% diff=-0.383  t=-2.84 p=4.56e-03  | day-matched 53d t=+0.71 p=4.83e-01  | 12w 5/6/1u | paper:373/764 -0.358 live:98/270 -0.440 | dies
  LONG  BOTH            news+ vs news0         24h  nA=  668 (days  64) nB= 1878  mA=+0.991% mB=+0.400% diff=+0.591  t=+4.23 p=2.51e-05✱ | day-matched 62d t=-0.72 p=4.74e-01  | 12w 6/6/0u | paper:420/1267 +0.317 live:248/611 +0.990 | dies
  LONG  BOTH            news- vs news0         24h  nA= 1048 (days  75) nB= 1878  mA=+0.048% mB=+0.400% diff=-0.351  t=-3.66 p=2.63e-04✱ | day-matched 71d t=-0.53 p=5.95e-01  | 12w 6/6/0u | paper:734/1267 -0.332 live:314/611 -0.350 | dies
  SHORT below_threshold news+ vs news0         24h  nA=  157 (days  37) nB=  895  mA=+0.250% mB=-0.452% diff=+0.702  t=+3.16 p=1.84e-03  | day-matched 35d t=+0.60 p=5.54e-01  | 12w 5/2/5u | paper:83/496 +0.320 live:74/399 +1.188 | dies
  SHORT below_threshold news- vs news0         24h  nA=  557 (days  62) nB=  895  mA=-1.145% mB=-0.452% diff=-0.694  t=-3.85 p=1.26e-04✱ | day-matched 53d t=+1.82 p=7.50e-02  | 12w 6/4/2u | paper:286/496 +0.292 live:271/399 -1.644 | dies
  SHORT ai_skipped      news+ vs news0         24h  nA=  797 (days  67) nB= 1201  mA=+0.072% mB=-0.543% diff=+0.614  t=+5.33 p=1.12e-07✱ | day-matched 63d t=-0.58 p=5.63e-01  | 12w 7/5/0u | paper:648/891 +0.445 live:149/310 +0.954 | dies
  SHORT ai_skipped      news- vs news0         24h  nA=  383 (days  54) nB= 1201  mA=-0.553% mB=-0.543% diff=-0.010  t=-0.05 p=9.60e-01  | day-matched 52d t=+1.09 p=2.82e-01  | 12w 3/9/0u | paper:257/891 +0.801 live:126/310 -1.439 | dies
  SHORT BOTH            news+ vs news0         24h  nA=  954 (days  73) nB= 2096  mA=+0.101% mB=-0.504% diff=+0.605  t=+6.13 p=1.07e-09✱ | day-matched 70d t=-0.20 p=8.42e-01  | 12w 8/4/0u | paper:731/1387 +0.357 live:223/709 +0.970 | dies
  SHORT BOTH            news- vs news0         24h  nA=  940 (days  70) nB= 2096  mA=-0.904% mB=-0.504% diff=-0.400  t=-2.98 p=2.89e-03  | day-matched 68d t=+1.54 p=1.29e-01  | 12w 5/7/0u | paper:543/1387 +0.584 live:397/709 -1.547 | dies
  BOTH  below_threshold news+ vs news0         24h  nA=  281 (days  59) nB= 1739  mA=+0.831% mB=+0.015% diff=+0.815  t=+3.85 p=1.44e-04✱ | day-matched 59d t=+0.16 p=8.76e-01  | 12w 9/1/2u | paper:137/999 +0.185 live:144/740 +1.447 | dies
  BOTH  below_threshold news- vs news0         24h  nA= 1134 (days  85) nB= 1739  mA=-0.487% mB=+0.015% diff=-0.502  t=-4.38 p=1.27e-05✱ | day-matched 76d t=-1.49 p=1.40e-01  | 12w 6/4/2u | paper:647/999 -0.022 live:487/740 -1.139 | dies
  BOTH  ai_skipped      news+ vs news0         24h  nA= 1341 (days  80) nB= 2235  mA=+0.391% mB=-0.149% diff=+0.540  t=+5.81 p=7.05e-09✱ | day-matched 78d t=+1.28 p=2.06e-01  | 12w 9/3/0u | paper:1014/1655 +0.348 live:327/580 +1.104 | dies
  BOTH  ai_skipped      news- vs news0         24h  nA=  854 (days  75) nB= 2235  mA=-0.289% mB=-0.149% diff=-0.140  t=-1.19 p=2.33e-01  | day-matched 74d t=+0.60 p=5.49e-01  | 12w 5/7/0u | paper:630/1655 +0.186 live:224/580 -1.051 | dies
  BOTH  BOTH            news+ vs news0         24h  nA= 1622 (days  84) nB= 3974  mA=+0.468% mB=-0.077% diff=+0.544  t=+6.59 p=5.22e-11✱ | day-matched 83d t=+0.33 p=7.43e-01  | 12w 9/3/0u | paper:1151/2654 +0.298 live:471/1320 +1.103 | dies
  BOTH  BOTH            news- vs news0         24h  nA= 1988 (days  90) nB= 3974  mA=-0.402% mB=-0.077% diff=-0.325  t=-3.96 p=7.54e-05✱ | day-matched 89d t=-0.44 p=6.59e-01  | 12w 6/6/0u | paper:1277/2654 +0.096 live:711/1320 -1.059 | dies
NEWS FAMILY: cells clearing Bonferroni RAW = 26/54 ; DAY-MATCHED = 0/54
news+ and news- drift the SAME way (vs news0) in 8/27 paired cells
```

## APPENDIX D — volatility profiles, raw output

```
CPI-tierAB: events with data 10/10: ['2025-12-18 13:30', '2026-01-13 13:30', '2026-02-13 13:30', '2026-03-11 12:30', '2026-04-10 12:30', '2026-05-12 12:30', '2026-06-10 12:30', '2026-07-14 12:30', '2026-08-12 12:30', '2026-09-11 12:30']

CPI-tierAB — 15-minute buckets, -120m → +120m
bucket         med range%  baseline%  ratio   events>2x
 -120.. -105      0.441      0.313    1.14x   2/10
 -105..  -90      0.326      0.293    0.92x   0/10
  -90..  -75      0.457      0.354    1.29x   1/10
  -75..  -60      0.320      0.346    0.83x   2/10
  -60..  -45      0.342      0.306    1.04x   0/10
  -45..  -30      0.306      0.309    0.86x   0/10
  -30..  -15      0.448      0.375    1.15x   1/10
  -15..   +0      0.539      0.365    1.49x   1/10
   +0..  +15      1.303      0.443    3.16x   8/10
  +15..  +30      0.549      0.377    1.41x   3/10
  +30..  +45      0.576      0.443    1.10x   1/10
  +45..  +60      0.677      0.431    1.43x   2/10
  +60..  +75      1.056      0.846    1.00x   2/10
  +75..  +90      0.963      0.719    1.27x   1/10
  +90.. +105      0.788      0.685    1.24x   1/10
 +105.. +120      0.697      0.704    1.06x   1/10

CPI-tierAB — 5-minute buckets, -30m → +60m
bucket         med range%  baseline%  ratio   events>2x
  -30..  -25      0.266      0.220    0.98x   2/10
  -25..  -20      0.265      0.206    1.11x   2/10
  -20..  -15      0.156      0.195    0.97x   1/10
  -15..  -10      0.226      0.219    1.12x   1/10
  -10..   -5      0.295      0.212    1.25x   1/10
   -5..   +0      0.349      0.183    1.94x   5/10
   +0..   +5      0.951      0.290    3.75x   9/10
   +5..  +10      0.592      0.246    2.56x   7/10
  +10..  +15      0.357      0.244    1.76x   4/10
  +15..  +20      0.361      0.265    1.41x   3/10
  +20..  +25      0.345      0.216    1.70x   3/10
  +25..  +30      0.293      0.186    1.37x   1/10
  +30..  +35      0.307      0.254    1.32x   1/10
  +35..  +40      0.249      0.255    1.08x   1/10
  +40..  +45      0.320      0.240    1.53x   4/10
  +45..  +50      0.335      0.278    1.24x   1/10
  +50..  +55      0.311      0.225    1.19x   2/10
  +55..  +60      0.311      0.248    1.26x   0/10

CPI-tierAB — block buckets
  -120.. -30  median ratio 1.13x  per-event [1.04, 1.21, 0.59, 1.34, 0.88, 1.27, 1.41, 1.27, 0.35, 1.05]
   -30..  -5  median ratio 1.01x  per-event [1.93, 0.73, 0.98, 1.25, 0.93, 0.99, 1.0, 1.18, 1.02, 1.23]
    -5.. +10  median ratio 3.07x  per-event [2.2, 3.1, 1.29, 1.97, 2.32, 4.08, 4.7, 3.63, 3.05, 6.18]
   +10.. +30  median ratio 1.36x  per-event [2.11, 1.55, 1.02, 1.05, 0.92, 1.37, 1.18, 3.33, 1.35, 1.73]
   +30..+120  median ratio 1.41x  per-event [1.48, 0.98, 1.82, 1.7, 1.42, 0.64, 1.39, 1.01, 1.03, 3.33]

CPI-tierC-archive-only: events with data 22/22: ['2024-01-16 13:30', '2024-02-13 13:30', '2024-03-12 12:30', '2024-04-10 12:30', '2024-05-15 12:30', '2024-06-12 12:30', '2024-07-11 12:30', '2024-08-14 12:30', '2024-09-11 12:30', '2024-10-10 12:30', '2024-11-13 13:30', '2024-12-11 13:30', '2025-01-15 13:30', '2025-02-12 13:30', '2025-03-12 12:30', '2025-04-10 12:30', '2025-05-13 12:30', '2025-06-11 12:30', '2025-07-15 12:30', '2025-08-12 12:30', '2025-09-11 12:30', '2025-10-24 12:30']

CPI-tierC-archive-only — 15-minute buckets, -120m → +120m
bucket         med range%  baseline%  ratio   events>2x
 -120.. -105      0.445      0.560    0.80x   0/22
 -105..  -90      0.403      0.491    0.82x   2/22
  -90..  -75      0.468      0.585    0.89x   0/22
  -75..  -60      0.456      0.570    0.80x   0/22
  -60..  -45      0.549      0.560    1.00x   0/22
  -45..  -30      0.489      0.477    0.95x   0/22
  -30..  -15      0.529      0.627    0.89x   2/22
  -15..   +0      0.694      0.658    1.17x   2/22
   +0..  +15      2.175      0.719    3.43x   18/22
  +15..  +30      1.009      0.648    1.50x   5/22
  +30..  +45      1.016      0.712    1.44x   5/22
  +45..  +60      0.825      0.689    1.28x   3/22
  +60..  +75      1.187      1.047    1.08x   2/22
  +75..  +90      1.026      0.895    1.21x   1/22
  +90.. +105      0.927      0.999    1.01x   2/22
 +105.. +120      0.946      0.968    0.97x   0/22

CPI-tierC-archive-only — 5-minute buckets, -30m → +60m
bucket         med range%  baseline%  ratio   events>2x
  -30..  -25      0.322      0.369    0.87x   0/22
  -25..  -20      0.318      0.383    0.94x   1/22
  -20..  -15      0.289      0.311    0.88x   1/22
  -15..  -10      0.307      0.373    0.93x   0/22
  -10..   -5      0.387      0.346    1.07x   3/22
   -5..   +0      0.417      0.310    1.38x   6/22
   +0..   +5      1.675      0.446    3.68x   20/22
   +5..  +10      0.695      0.391    2.22x   13/22
  +10..  +15      0.784      0.378    2.11x   12/22
  +15..  +20      0.707      0.406    1.66x   7/22
  +20..  +25      0.569      0.364    1.58x   4/22
  +25..  +30      0.464      0.303    1.52x   5/22
  +30..  +35      0.584      0.423    1.42x   7/22
  +35..  +40      0.595      0.398    1.42x   4/22
  +40..  +45      0.496      0.352    1.33x   6/22
  +45..  +50      0.606      0.396    1.38x   1/22
  +50..  +55      0.428      0.382    1.02x   2/22
  +55..  +60      0.410      0.341    1.23x   3/22

CPI-tierC-archive-only — block buckets
  -120.. -30  median ratio 0.85x  per-event [0.49, 0.63, 0.57, 0.99, 1.23, 0.82, 0.99, 1.41, 1.4, 0.98, 0.91, 0.74, 0.6, 0.59, 2.24, 0.87, 0.92, 0.81, 0.81, 0.91, 0.74, 0.62]
   -30..  -5  median ratio 0.93x  per-event [0.81, 0.59, 1.25, 2.37, 0.62, 1.04, 0.72, 0.85, 0.74, 0.75, 1.15, 0.7, 0.64, 1.39, 1.01, 1.75, 1.01, 1.19, 1.11, 0.58, 2.49, 0.53]
    -5.. +10  median ratio 2.95x  per-event [0.6, 3.91, 2.69, 4.36, 4.85, 7.52, 2.59, 2.2, 2.35, 2.77, 3.13, 1.6, 3.21, 5.97, 4.5, 2.41, 2.32, 3.36, 2.75, 2.34, 5.7, 3.6]
   +10.. +30  median ratio 1.94x  per-event [1.14, 2.0, 0.99, 3.1, 1.6, 1.72, 2.26, 2.96, 2.22, 1.57, 2.51, 1.04, 2.01, 2.33, 1.89, 2.84, 1.35, 2.31, 2.1, 1.15, 1.81, 0.85]
   +30..+120  median ratio 1.19x  per-event [0.98, 1.49, 1.02, 1.03, 1.61, 1.16, 1.09, 1.51, 1.64, 1.32, 1.28, 1.22, 0.85, 0.95, 1.34, 0.66, 1.22, 0.97, 0.81, 0.68, 1.34, 1.32]

NFP-config: events with data 4/4: ['2026-06-05 12:30', '2026-07-02 12:30', '2026-08-07 12:30', '2026-09-04 12:30']

NFP-config — 15-minute buckets, -120m → +120m
bucket         med range%  baseline%  ratio   events>2x
 -120.. -105      0.576      0.300    2.04x   2/4
 -105..  -90      0.462      0.330    1.37x   2/4
  -90..  -75      0.585      0.362    1.79x   2/4
  -75..  -60      0.681      0.368    1.99x   2/4
  -60..  -45      0.511      0.328    1.47x   2/4
  -45..  -30      0.458      0.405    1.02x   0/4
  -30..  -15      0.520      0.423    1.73x   2/4
  -15..   +0      0.733      0.427    1.59x   2/4
   +0..  +15      1.645      0.469    3.51x   4/4
  +15..  +30      0.552      0.434    1.46x   1/4
  +30..  +45      0.667      0.429    1.46x   1/4
  +45..  +60      0.793      0.451    1.72x   2/4
  +60..  +75      1.076      0.802    1.24x   1/4
  +75..  +90      0.834      0.676    1.01x   1/4
  +90.. +105      0.671      0.699    1.28x   1/4
 +105.. +120      0.973      0.785    1.46x   0/4

NFP-config — 5-minute buckets, -30m → +60m
bucket         med range%  baseline%  ratio   events>2x
  -30..  -25      0.258      0.258    1.11x   1/4
  -25..  -20      0.284      0.249    1.73x   2/4
  -20..  -15      0.328      0.225    1.75x   2/4
  -15..  -10      0.403      0.228    1.69x   2/4
  -10..   -5      0.185      0.261    0.83x   1/4
   -5..   +0      0.493      0.199    2.07x   2/4
   +0..   +5      1.474      0.286    5.16x   4/4
   +5..  +10      0.595      0.293    2.01x   2/4
  +10..  +15      0.517      0.242    2.13x   2/4
  +15..  +20      0.356      0.282    1.28x   1/4
  +20..  +25      0.390      0.248    1.75x   1/4
  +25..  +30      0.332      0.208    1.42x   1/4
  +30..  +35      0.377      0.275    1.26x   1/4
  +35..  +40      0.448      0.231    1.79x   1/4
  +40..  +45      0.401      0.211    1.70x   2/4
  +45..  +50      0.465      0.271    1.59x   0/4
  +50..  +55      0.322      0.240    1.53x   0/4
  +55..  +60      0.393      0.247    1.58x   1/4

NFP-config — block buckets
  -120.. -30  median ratio 1.18x  per-event [1.7, 3.51, 0.66, 0.54]
   -30..  -5  median ratio 2.01x  per-event [2.3, 1.98, 2.03, 0.47]
    -5.. +10  median ratio 3.49x  per-event [3.95, 2.99, 3.03, 6.15]
   +10.. +30  median ratio 1.40x  per-event [1.63, 1.02, 1.16, 2.12]
   +30..+120  median ratio 1.05x  per-event [2.56, 1.2, 0.9, 0.88]
```
