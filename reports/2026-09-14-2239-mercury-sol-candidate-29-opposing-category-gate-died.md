# mercury-sol-candidate-29-opposing-category-gate-died

_2026-09-14 22:39 UTC_

---

# Mercury-SOL — candidate 29: make the opposing category a gate. It died. No diff.

**2026-09-14 · READ-ONLY on both bots · nothing proposed, nothing applied, nothing restarted, NO DIFF WRITTEN** · `openitems_guard` EXIT 0 at 22:36 and 22:37

**Basis:** `2026-09-14-1904` (§1b, §1c), `2026-09-14-2119` (block replay), `2026-09-14-2224` (re-wording).

> 🔴 **THE OPERATOR'S EXPECTATION, STATED BEFORE ANY NUMBER:** this would die the way the last candidates died. Live opposed n = 4 at ΣR −2.770, paper opposed n = 8 at **+2.151**, the sign inverting between books, p = 0.058 on the only rankable cell.
>
> **CONTROLS, DECLARED IN THE HEADER**
> * **Bonferroni over every threshold × side × book:** 4 thresholds (1.25 / 1.75 / 2.25 / 2.50) × 3 sides (ALL / LONG / SHORT) × 2 books = **24 cells, α = 0.05/24 = 0.00208**.
> * A cell is ranked only if both legs have n ≥ 8.
> * **Survival** requires all four: p < α; the same sign in both chronological halves of each book; the same sign in TREND and FLAT with both legs populated; and **the same sign on paper and live**.
> * **Paper and live are never pooled.** Book positions: 39 (live 17: vpos 29–45; paper 22: vpos 7–28). R = `net_pnl / initial_risk_usdt`.

---

## VERDICT

☠️ **IT DIES, AT EVERY THRESHOLD. The expectation was right. No diff is written, and the line closes for good.**

1. 🔴 **IT REFUSES WINNERS, at every threshold.**
   - **Paper:** it refuses vpos **7 (+2.089R), 13 (+1.337R), 19 (+0.463R), 21 (+0.285R)** at every T, and **11 (+1.133R)** too at T = 1.25.
   - **Live:** it refuses exactly vpos 32, 35, 36, 45, four SHORTs, all losers (ΣR −2.770).
   - That is the same way filter 21 died on SOL and Titan's clause B was disarmed.
2. 🔴 **THE SIGN INVERTS BETWEEN THE BOOKS, and it is stable inside each book.**
   - Refused minus admitted mean R is **negative on live** in both halves and in both TREND and FLAT.
   - It is **positive on paper** in both halves and in both TREND and FLAT.
   - The independent sample says the opposite of the live book, and no threshold rescues it: the book positions refused are identical at T = 1.75, 2.25 and 2.50.
3. **The only rankable cell** is paper ALL at T = 1.25 (refused 8 vs admitted 14): **p = 0.058 ≥ α 0.00208**. Every live cell is n < 8.
4. 🔴 **IT BREACHES THE BOOK GATE'S OWN ALARM SHAPE at every threshold, in both books.**
   - It would refuse **7.4–20.4 % of score-gate passes per side**, above the 5 % wire.
   - The side ratio is 1.01–1.39×, below the 2× wire. So it is **not a side ban at signal level**. It is a wide refusal that happens to hit only shorts in the live book.
5. **It does not fix the live short side.** The four live shorts it admits are still 0 wins in 4 (ΣR −4.062).

**What happens now:**
- Recorded in `OPEN-ITEMS-SOL.md §CANDIDATE-29-OPPOSING-CATEGORY-GATE-2026-09-14`.
- 🔴 **The opposing-category line stays what it is:** a fact in the entry prompt that the model reads and discounts, with **no mechanical consumer**.
- 🔴 **What no version of this addresses:** the model will keep discounting the opposition in its narration ("minority-zeroed", then "ignored per gate rules"). **A gate removes the trade, not the sentence.**

---

## 1. THE GATE, DEFINED BEFORE ANY NUMBER

### 1a. Predicate and placement

> **Refuse the entry when any scored category (TREND, MOMENTUM, LIQUIDITY, EXECUTION) has `net_direction` opposite to the proposed side with raw points `max(long_points, short_points)` ≥ T.**

**Placement:** in `main._handle_5m_trigger`, **after the score gate** and inside the `_entry_gate` lock, **before `consult_for_entry`**, beside the flat-ADX and book gates. That is exactly the book gate's position.
- At that point the HTF cascade has already refused every opposing TREND, MOMENTUM and EXECUTION (1904 §1b). **In practice the predicate reads LIQUIDITY.**

### 1b. The threshold: derived, not swept

The distribution is 1904 §1c's population, the opposed rows at the score bar (zeroed ∪ kept), recomputed now on 8,244 bar rows (2 more rows since 1904, neither opposed):

| opposing points (largest opposing category per row) | 1.25 | 1.75 | 2.25 | **2.50** | n |
|---|---|---|---|---|---|
| rows | 243 | 456 | 95 | **902** (53.2 %) | **1,696** |

- **Rule, stated before looking at outcomes:** T = the **median** opposing weight of that distribution, which is **2.50**. That is also the category cap, the weight TREND can carry for the proposed side, and the "full-weight opposing category" of the vpos 45 defect.
- **All four observed levels are reported side by side** so the choice hides nothing.
- On the book it makes **no difference**: T = 1.75, 2.25 and 2.50 refuse identical positions, and T = 1.25 adds vpos 11 and 14.

### 1c. Zeroed and kept: treated the same

Yes. The predicate reads **raw** category points, not the post-minority-rule `contribution`.
- 1904 §1b established that the score gate nets neither a zeroed nor a kept opposing category.
- A rule that distinguished them would be judging the card's bookkeeping, not the market.

### 1d. No future information

It reads only `matrix_result['breakdown']`: `net_direction`, `long_points`, `short_points`.
- `signal_matrix.compute_score` builds that at `main.py:4370`, **before** the cascade and the score gate, from signals already inside their windows.
- It is the same dict passed to the advisor since 2026-09-11. Nothing later is read.

---

## 2. REPLAYED OVER EVERYTHING

### 2a. Signals refused

**Population:** rows that **passed the score gate**, i.e. would reach the gate's position. That is 4,813 of 8,244 bar rows with a stored breakdown. Book = era (live from 2026-08-07 22:25:18).

| T | book | LONG passes | LONG refused | SHORT passes | SHORT refused | side ratio | book-gate alarm shape (> 5 % on a side, or > 2×) |
|---|---|---|---|---|---|---|---|
| 1.25 | paper | 1,538 | 226 (**14.69 %**) | 1,853 | 378 (**20.40 %**) | 1.39× | 🔴 **BREACHED** (5 % wire) |
| 1.25 | live | 701 | 116 (**16.55 %**) | 721 | 118 (**16.37 %**) | 1.01× | 🔴 **BREACHED** |
| 1.75 | paper | 1,538 | 193 (12.55 %) | 1,853 | 299 (16.14 %) | 1.29× | 🔴 **BREACHED** |
| 1.75 | live | 701 | 105 (14.98 %) | 721 | 105 (14.56 %) | 1.03× | 🔴 **BREACHED** |
| 2.25 | paper | 1,538 | 150 (9.75 %) | 1,853 | 211 (11.39 %) | 1.17× | 🔴 **BREACHED** |
| 2.25 | live | 701 | 66 (9.42 %) | 721 | 72 (9.99 %) | 1.06× | 🔴 **BREACHED** |
| **2.50** | paper | 1,538 | 124 (8.06 %) | 1,853 | 199 (10.74 %) | 1.33× | 🔴 **BREACHED** |
| **2.50** | live | 701 | 63 (8.99 %) | 721 | 56 (7.77 %) | 1.16× | 🔴 **BREACHED** |

- **Last 30 days, as the book gate's review reads it:** T = 2.50 gives LONG 53/575 (9.22 %) and SHORT 43/580 (7.41 %). T = 1.25 gives LONG 92/575 (16.00 %) and SHORT 88/580 (15.17 %).
- **Across all 8,244 bar rows**, including those that failed the score gate, opposed ≥ T: 1.25 → 1,696 · 1.75 → 1,453 · 2.25 → 997 · 2.50 → 902.
- **Per month** (score-gate passes; refused at T = 2.50 / at T = 1.25 / n). June and July are paper, August is mixed (paper until 08-07), September is live:

| month | LONG | SHORT |
|---|---|---|
| 2026-06 | 37 / 75 / 428 | 51 / 100 / 415 |
| 2026-07 | 65 / 113 / 919 | 125 / 233 / 1,156 |
| 2026-08 | 46 / 93 / 515 | 48 / 100 / 655 |
| 2026-09 | 39 / 61 / 377 | 31 / 63 / 348 |

**Coverage limit:** 1,591 rows past the bar (`risk_halt`, `entry_gate_refused`, `flat_adx_blocked`, `book_blocked`) store no breakdown and are not in these counts (1904 §1c).

### 2b–2c. 🔴 Which book positions it refuses

**LIVE:** identical at every T.

| vpos | side | opposing | rule | R |
|---|---|---|---|---|
| 32 | SHORT | LIQUIDITY LONG 2.50 | zeroed | −0.180 |
| 35 | SHORT | LIQUIDITY LONG 2.50 | kept | −0.701 |
| 36 | SHORT | LIQUIDITY LONG 2.50 | kept | −0.757 |
| 45 | SHORT | LIQUIDITY LONG 2.50 | zeroed | −1.133 |

No live winner is refused. No live LONG is refused.

**PAPER:** 🔴 **WINNERS REFUSED.**

| vpos | side | opposing | refused at T = 1.25 | refused at T ≥ 1.75 | R |
|---|---|---|---|---|---|
| **7** | LONG | LIQUIDITY SHORT 2.50 | ✔ | ✔ | **+2.089 🔴 winner** |
| **11** | SHORT | LIQUIDITY LONG 1.25 | ✔ | — | **+1.133 🔴 winner** |
| **13** | SHORT | LIQUIDITY LONG 2.50 | ✔ | ✔ | **+1.337 🔴 winner** |
| 14 | SHORT | LIQUIDITY LONG 1.25 | ✔ | — | −1.032 |
| 18 | LONG | LIQUIDITY SHORT 2.50 | ✔ | ✔ | −1.074 |
| **19** | SHORT | LIQUIDITY LONG 2.50 | ✔ | ✔ | **+0.463 🔴 winner** |
| **21** | LONG | LIQUIDITY SHORT 2.50 | ✔ | ✔ | **+0.285 🔴 winner** |
| 24 | SHORT | LIQUIDITY LONG 2.50 | ✔ | ✔ | −1.050 |

**At T = 2.50, the derived threshold, it refuses four paper winners worth +4.174R, and 6 paper positions in all.**

### 2d. ΣR and Σ$ with and without, per side, per book (n first; n < 8 not ranked)

**T = 1.75 / 2.25 / 2.50 (identical book effect):**

| book | side | without gate | refused | with gate |
|---|---|---|---|---|
| live | ALL | n 17 · ΣR +5.621 · $+13.72 | **n 4 · ΣR −2.770** | n 13 · ΣR +8.391 · $+17.32 |
| live | LONG | n 9 · +12.453 · $+24.32 | n 0 | n 9 · +12.453 · $+24.32 |
| live | SHORT | n 8 · −6.832 · $−10.60 | n 4 · −2.770 · NOT RANKED | n 4 · −4.062 · $−7.00 |
| paper | ALL | n 22 · ΣR −5.374 · $−1,128.46 | **n 6 · ΣR +2.051** · NOT RANKED | n 16 · ΣR −7.425 · $−1,604.46 |
| paper | LONG | n 9 · −4.046 · $−712.63 | n 3 · +1.300 · NOT RANKED | n 6 · −5.347 · $−1,006.45 |
| paper | SHORT | n 13 · −1.328 · $−415.83 | n 3 · +0.750 · NOT RANKED | n 10 · −2.078 · $−598.01 |

**T = 1.25:**

| book | side | without gate | refused | with gate |
|---|---|---|---|---|
| live | all cells | identical to above | | |
| paper | ALL | n 22 · −5.374 | **n 8 · ΣR +2.151** | n 14 · −7.525 · $−1,499.64 |
| paper | LONG | n 9 · −4.046 | n 3 · +1.300 · NOT RANKED | n 6 · −5.347 |
| paper | SHORT | n 13 · −1.328 | n 5 · +0.851 · NOT RANKED | n 8 · −2.179 · $−493.19 |

Live Σ$ is the DB book, which is overstated by ≈ $1.16 against Bybit (`§LIVE-BOOK-VS-VENUE-GAP-2026-09-14`).

### 2e. Volume cost

**Book positions per day** (live era 38 days, paper era 54 days):

| book | side | today | with gate (T ≥ 1.75) | with gate (T = 1.25) |
|---|---|---|---|---|
| live | ALL | 0.447 | 0.342 | 0.342 |
| live | LONG | 0.237 | 0.237 | 0.237 |
| live | SHORT | 0.211 | **0.105 (−50 %)** | 0.105 |
| paper | ALL | 0.407 | 0.296 | 0.259 |
| paper | LONG | 0.167 | 0.111 | 0.111 |
| paper | SHORT | 0.241 | 0.185 | 0.148 |

**Signal-level refusal:** 7.4–20.4 % of score-gate passes per side (§2a), which is more than the book gate's own registered ceiling.

---

## 3. THE FOUR CONTROLS

| control | result |
|---|---|
| **a. Bonferroni** (24 cells, α 0.00208) | **Only one cell is rankable** (paper ALL, T = 1.25, refused 8 vs admitted 14): **p = 0.0584 ≥ α.** Every other cell has n < 8 on the refused leg and is NOT RANKED |
| **b. Chronological halves** | Live: refused − admitted sign **− / −** at every T. Paper: **+ / +** at every T. Stable within each book, **opposite between books** |
| **c. Regime split**, both legs populated | Live: TREND − (refused 2 / admitted 8), FLAT − (2 / 5). Paper at T ≥ 1.75: TREND + (5 / 13), FLAT + (1 / 3). At T = 1.25: TREND + (7 / 11), FLAT + (1 / 3). Both legs populated everywhere, and **opposite between books** |
| **d. 🔴 Paper as the independent sample** | ☠️ **FAILS.** Live refused lost (ΣR −2.770); **paper refused WON** (ΣR +2.051 / +2.151, 4–5 winners). **The sign inverts, so the rule does not survive, and no threshold rescues it**: T = 1.75, 2.25 and 2.50 refuse identical positions, and T = 1.25 only adds a paper winner (vpos 11) and a paper loser (vpos 14) |
| **e. 🔴 Book-gate alarm shape** | ☠️ **BREACHED at every threshold, both books**: 7.4–20.4 % per side against the 5 % wire. The side ratio stays 1.01–1.39× (below 2×), so it is not a side ban at signal level. In the live book, though, every refused position is a SHORT |

---

## 4. DIFF: NONE

**§4b applies.** It did not survive, so **no module and no diff was written**. Nothing in either bot's code tree was touched.
- **Recorded in the canon:** `OPEN-ITEMS-SOL.md §CANDIDATE-29-OPPOSING-CATEGORY-GATE-2026-09-14`, inserted above §PROMPT-CATEGORY-WORDING. Backup `OPEN-ITEMS-SOL.md.bak_candidate29_20260914`; the `§BOOK-GATE-RECUT-2026-09-11` anchor is intact.
- **Numbering, stated honestly:** recorded as **candidate twenty-nine** per the operator's count. The 2026-09-11 17:14 report had already called its own set "the twenty-ninth", so the running count is approximate and nothing depends on it.
- 🔴 **The opposing-category line stays what it is:** a fact in the entry prompt (§PROMPT-CATEGORY-BLOCK, re-worded in §PROMPT-CATEGORY-WORDING) that the model reads and **discounts**, with **no mechanical consumer**. The score gate never nets it, the cascade does not read LIQUIDITY, and no gate refuses on it.

### 4c. What this does NOT address, either way

- **The narration.** The model will keep discounting the opposition in its reasons: "minority-zeroed" under the first wording, "ignored per gate rules" under the second.
- **A gate would have removed the trade, not the sentence.** The failed gate removes neither.
- **The live short side.** 0 wins in 8, and 0 in the 4 this gate would have admitted (ΣR −4.062). That is the regime question of 1904 §4 and 2013 §3, and the live book still has never seen a BEAR daily.
- **Outcomes of refused signals** beyond the 39 book positions. No substitute-population (skip-drift) test was run for this candidate. It was not asked, and the book already kills it on two independent controls.

---

## CONFIRMATION

| item | state |
|---|---|
| **`openitems_guard`** | EXIT **0** at 22:36 (first) and 22:37 (after) |
| **SOL DB** | opened only as `file:…?mode=ro` with `PRAGMA query_only=1` (verified `= 1`); **no write** |
| **SOL config** | **not imported**; no SOL module imported at all by this pass. The replay reads only the DB |
| **orders / venue** | **none**. No venue call and no model call in this pass |
| **restart** | **none**. `mercury-sol` NRestarts **0**, MainPID 2245907 unchanged · `titan` NRestarts **0**, MainPID 1572470 unchanged · `mercury-sol-optimizer-listener` 0, unchanged |
| **code hashes** | md5 of every SOL `*.py` (incl. `config.py`), `titan-bot/config.py` and every `titan-bot/*.py`: **identical** 22:36 → 22:37. The only changed hashed file is `OPEN-ITEMS-SOL.md` (the §4b canon record) |
| **`FLAT_ADX_GATE_DRYRUN`** | **True** (config.py:407) |
| **`BOOK_GATE_DRYRUN`** | **False** (config.py:475) |
| **book-gate review counter** | **untouched**. Only its own cron ran (22:30:03): LONG 0/137, SHORT 0/112, unchanged since 22:00 |
| **Titan** | **untouched**: no Titan file, DB or service touched; its only read was the guard itself. Newer files in Titan's tree (`healthcheck_state.json`, `optimizer/tg_offset.txt`) were written by Titan's own processes |
| **files written in SOL's tree** | `OPEN-ITEMS-SOL.md` (+1 section) and its `.bak_candidate29_20260914`. Also newer: `optimizer/tg_offset.txt`, written by the bot's own listener. **No code, no diff** |

---

## APPENDIX: raw replay output

The per-T blocks below were generated by the replay script over the DB (read-only).

```
bar rows with breakdown: 8244 | passed the score gate (reach the proposed gate position): 4813
opposing-points distribution at the bar (zeroed ∪ kept): [(1.25, 243), (1.75, 456), (2.25, 95), (2.5, 902)] n 1696 · median 2.5 · mean 2.105 · share at cap 0.532

=== T = 1.25 ===
  live REFUSED: [(32,SHORT,-0.18), (35,SHORT,-0.701), (36,SHORT,-0.757), (45,SHORT,-1.133)]  WINNERS REFUSED: []
    ALL   without n=17 ΣR +5.621 Σ$ +13.72 | refused n=4 ΣR -2.770 | with n=13 ΣR +8.391 Σ$ +17.32 | entries/day 0.447 → 0.342 | NOT RANKED
    LONG  without n=9 ΣR +12.453 | refused n=0 | with n=9 ΣR +12.453 | 0.237 → 0.237 | NOT RANKED
    SHORT without n=8 ΣR -6.832 Σ$ -10.60 | refused n=4 ΣR -2.770 | with n=4 ΣR -4.062 Σ$ -7.00 | 0.211 → 0.105 | NOT RANKED
    controls: full − · halves (−, −) · TREND − · FLAT − · legs TREND 2/8 FLAT 2/5
  paper REFUSED: [(7,LONG,2.089), (11,SHORT,1.133), (13,SHORT,1.337), (14,SHORT,-1.032), (18,LONG,-1.074), (19,SHORT,0.463), (21,LONG,0.285), (24,SHORT,-1.05)]
        WINNERS REFUSED: [(7,2.089), (11,1.133), (13,1.337), (19,0.463), (21,0.285)]
    ALL   without n=22 ΣR -5.374 Σ$ -1128.46 | refused n=8 ΣR +2.151 | with n=14 ΣR -7.525 Σ$ -1499.64 | 0.407 → 0.259 | p=0.0584
    LONG  without n=9 ΣR -4.046 | refused n=3 ΣR +1.300 | with n=6 ΣR -5.347 | 0.167 → 0.111 | NOT RANKED
    SHORT without n=13 ΣR -1.328 | refused n=5 ΣR +0.851 | with n=8 ΣR -2.179 | 0.241 → 0.148 | NOT RANKED
    controls: full + · halves (+, +) · TREND + · FLAT + · legs TREND 7/11 FLAT 1/3

=== T = 1.75 / 2.25 / 2.50 (identical book effect) ===
  live: identical to T = 1.25
  paper REFUSED: [(7,LONG,2.089), (13,SHORT,1.337), (18,LONG,-1.074), (19,SHORT,0.463), (21,LONG,0.285), (24,SHORT,-1.05)]
        WINNERS REFUSED: [(7,2.089), (13,1.337), (19,0.463), (21,0.285)]
    ALL   without n=22 ΣR -5.374 | refused n=6 ΣR +2.051 | with n=16 ΣR -7.425 Σ$ -1604.46 | 0.407 → 0.296 | NOT RANKED
    LONG  refused n=3 ΣR +1.300 | with n=6 ΣR -5.347 | NOT RANKED
    SHORT refused n=3 ΣR +0.750 | with n=10 ΣR -2.078 Σ$ -598.01 | 0.241 → 0.185 | NOT RANKED
    controls: full + · halves (+, +) · TREND + · FLAT + · legs TREND 5/13 FLAT 1/3
```
