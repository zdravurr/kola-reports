# Mercury-SOL — book-gate lean floors re-cut per side and applied from flat: SHORT 0.3489 → 0.3975, LONG 0.4238 → 0.4214, side ratio 5.67× → 1.23× on replay; the breach was SHORT clause B silent, not LONG over-firing; the wall ruler was re-cut but not applied; the missed 08-20 review is recorded as a named failure

_2026-09-11 05:50 UTC_

---

**2026-09-11 05:50 UTC · APPLIED FROM FLAT, restarted 05:40:05 · Mercury-SOL (LIVE, `is_paper=0`) · basis: report 2026-09-11-0526 §3b and §4b**

## The answer first

1. **The pre-registered alarm had tripped, and the re-cut it requires is applied.** Since the 08-14 re-cut the gate refused **LONG 17 of 481 (3.53 %) against SHORT 3 of 481 (0.62 %) — 5.67×, exact two-sided p = 0.0026.** The review point, "200 further evaluations or 2026-09-14", came on **2026-08-20 23:30:02** with LONG 9/117 = 7.69 %, SHORT 3/83 = 3.61 %, 2.13×. Both wires had tripped then, and nobody checked. That is now in the canon as a named failure (§5c).
2. **What carried the breach is SHORT clause B, silent at 0 of 481** — not LONG over-firing. LONG sat on its registered rates: B 11/481 = 2.29 % against 2.01 %, and A 6/481 = 1.25 % against ~1.2 %. The SHORT floor of 0.3489 was the 2nd percentile of a population whose bottom tail was the 08-11 → 08-14 armed-window refusals. **Re-cutting the LONG floor alone would leave the ratio at 5.33×; it is not the fix.**
3. **Applied: both lean floors, re-cut by the unchanged rule.** The rule is the p2 of each side's own lean over the rows the gate evaluates in the current era (n = 481 / 481). **LONG 0.4238 → 0.4214, SHORT 0.3489 → 0.3975.** Replayed on the same 962 rows: **LONG 3.33 %, SHORT 2.70 %, ratio 1.23×.** Only `BOOK_GATE_LEAN_FLOOR` changed; the AST confirms it. The worker loaded it.
4. 🔴 **The clause-A ruler (`_NEAR_MULT_BREAKS`) was re-cut from the same rows, as ordered, and is shown beside the live one — but it was NOT applied.** This departs from the brief's apply step, for three measured reasons:
   - In-sample it takes SHORT to **4.57 %**. That gives a **31 % chance of reading above the 5 % wire at N = 200 from noise alone**, so it would breach its own re-registration by chance.
   - Cut on the first half of the era, it refuses **0 clause-A rows on the second half**. The ruler is not stable at this n.
   - It lowers the SHORT p90 from ×23.7 to ×21.5 using a population with no bear daily in it. That is exactly the direction in which a bear market grows SHORT clause A (0526 §3c). On the 1,313 stored bear-daily books it raises SHORT clause-A refusals from 13 to 19.

   The brief's own §2b asks for the clause-specific fix when one clause carries the breach. Floors alone restore the ratio. **Applying the ruler as well is one constant in `book_gate.py`; that is the operator's call, and the numbers are in §1d.**
5. 🔴 **One trade changes fate in the admitting direction, and it would have lost.** #18565, a LONG refused on 2026-08-15 07:05 at lean 0.4216, clears the new 0.4214 floor by 0.0002. Replayed on candles it would have made **−1.20R (−$1.20)**, had the advisor passed it; the advisor passes about 1 % of setups. **No executed trade changes fate.** The eight executed positions of the era are all admitted under the new floors. The new floors refuse **no winner**: vpos 38 +4.03R, 39 +1.60R, 40 +2.55R, 41 +1.63R and 43 +1.72R all read "book clear".
6. **The discipline basis is unchanged, and the comment in `config.py` says so.** The gate exists because a bot that buys into a wall does something a trader would not. It does not exist because the data promises money.

---

## 1. Cut on the right population

### 1a. Population, n per side first

The population is every row the live gate evaluated after the 2026-08-14 18:28:16 re-cut: rows with the six `book_gate_*` facts written, or `status = 'book_blocked'`. It runs from 2026-08-14 22:50:02 to 2026-09-11 04:30:14. **n = 481 LONG / 481 SHORT.** Status: LONG 459 advisor-refused · 17 gate-refused · 5 executed; SHORT 475 · 3 · 3. Every row carries a lean and a nearest-opposing-wall multiple, with no nulls. The facts are the gate's own stored values, not a re-parse.

**Replay check:** the live constants applied to these stored facts reproduce the stored gate decision on **962 of 962** rows.

### 1b. 🔴 The regime of the tail — and yes, it has the same problem as 08-14

| | LONG | SHORT |
|---|---|---|
| population, daily regime | BULL 336 · NEUTRAL 142 · unlabelled 3 | BULL 399 · NEUTRAL 82 |
| **rows below the new floor (the tail that sets p2)** | 10: BULL 4 · NEUTRAL 3 · unlabelled 3 | **10: BULL 10** |
| tail by day | 09-02 ×4, 08-15 ×2, 08-26 ×2, 08-16, 09-07 | **08-29 ×5**, 09-06 ×2, 08-26, 09-04, 09-09 |
| rows at or above the re-cut p90 wall | 50: BULL 28 · NEUTRAL 21 · unlabelled 1 | 49: BULL 36 · NEUTRAL 13 |

**Plainly: this cut has the same problem.** The SHORT floor's tail is entirely bull-daily, and half of it comes from one day. Unlike 08-14, it cannot be avoided: **the current era contains not one bear-daily row.** The last BEAR daily anywhere was 2026-08-07 05:55. The rule, p2 over every evaluated row, was kept exactly as it was. Its sensitivity, so the reader knows how much is noise:

| | all rows | one row per side per hour | without 2026-08-29 | without 2026-09-02 |
|---|---|---|---|---|
| LONG p2 | **0.4214** (n 481) | 0.4199 (n 165) | 0.4214 | 0.4293 |
| SHORT p2 | **0.3975** (n 481) | 0.3967 (n 170) | **0.4116** | 0.3975 |

Split-half, floors only: cut on 08-14 → 09-01 (LONG 0.4214, SHORT 0.3949) and applied to 09-01 → 09-11, it refuses LONG 6/245 = 2.45 % and SHORT 3/236 = 1.27 %. Cut on the second half and applied to the first, LONG 0.4317 / SHORT 0.4018 refuse 6.36 % / 4.08 %. **The floor moves by ±0.01 between halves of the same month.** That is the resolution of this ruler at n ≈ 240, and it is why the review point matters.

### 1c. The cut — the rule stays, the ruler moves

- **Lean floor, per side, at p2** over the population above: **LONG 0.4214, SHORT 0.3975.** Neither the percentile (2) nor anything in clause B's logic changed.
- **Clause-A ruler** — the nearest-opposing-wall multiple at p5 … p95, per side, over the same rows. `BOOK_GATE_WALL_PCTL` (90) and the 0.20 % distance are untouched.

| percentile | LONG live | LONG re-cut | SHORT live | SHORT re-cut |
|---|---|---|---|---|
| p5 | ×9.20 | ×8.90 | ×10.00 | ×7.40 |
| p10 | ×10.30 | ×9.90 | ×11.60 | ×8.00 |
| p15 | ×10.90 | ×10.40 | ×12.70 | ×8.30 |
| p20 | ×11.70 | ×11.00 | ×13.40 | ×8.80 |
| p25 | ×12.30 | ×11.60 | ×14.00 | ×9.30 |
| p30 | ×12.90 | ×12.00 | ×14.70 | ×9.70 |
| p35 | ×13.20 | ×12.20 | ×15.20 | ×10.00 |
| p40 | ×13.80 | ×12.40 | ×15.80 | ×10.30 |
| p45 | ×14.20 | ×12.80 | ×16.30 | ×10.60 |
| p50 | ×14.60 | ×13.10 | ×16.80 | ×11.00 |
| p55 | ×15.20 | ×13.60 | ×17.30 | ×11.50 |
| p60 | ×15.50 | ×14.00 | ×18.00 | ×11.80 |
| p65 | ×16.00 | ×14.60 | ×18.50 | ×12.50 |
| p70 | ×16.60 | ×15.20 | ×19.40 | ×13.10 |
| p75 | ×17.10 | ×15.90 | ×20.00 | ×14.10 |
| p80 | ×17.70 | ×16.80 | ×20.90 | ×15.40 |
| p85 | ×18.40 | ×18.50 | ×22.00 | ×17.80 |
| p90 | ×19.10 | ×19.70 | ×23.70 | ×21.50 |
| p95 | ×20.40 | ×21.40 | ×25.80 | ×23.50 |

In a bull tape the SHORT walls, the bids below price, are much smaller: the median fell from ×16.8 to ×11.0. The LONG walls barely moved.

### 1d. 🔴 Both cuts side by side, replayed over the 962 evaluated rows

| variant | LONG A | LONG B | **LONG any** | SHORT A | SHORT B | **SHORT any** | **ratio** | P(realised > 5 % at N=200 by noise) L / S | bear-daily books (1,313, pre-gate) L / S |
|---|---|---|---|---|---|---|---|---|---|
| **live, as running** | 6 | 11 | **17 = 3.53 %** | 3 | 0 | **3 = 0.62 %** | **5.67×** | 0.099 / ~0 | 1.20 % / 2.00 % |
| **APPLIED: floors re-cut, live rulers** | 6 | 10 | **16 = 3.33 %** | 3 | 10 | **13 = 2.70 %** | **1.23×** | 0.073 / 0.021 | 1.20 % / 2.47 % |
| full re-cut (floors + rulers) | 3 | 10 | 13 = 2.70 % | 12 | 10 | 22 = 4.57 % | 1.69× | 0.021 / **0.308** | 1.20 % / **3.39 %** |
| rulers only (live floors) | 3 | 11 | 14 = 2.91 % | 12 | 0 | 12 = 2.49 % | 1.17× | — | 1.20 % / 2.93 % |
| LONG floor only | 6 | 10 | 16 = 3.33 % | 3 | 0 | 3 = 0.62 % | **5.33×** | — | 1.20 % / 2.00 % |

The in-sample rates of the applied variant are the new pre-registration (§5a). The full re-cut is inside the wire in-sample but sits at 91 % of it on SHORT. On the stored bear-daily books it moves SHORT the wrong way, from 2.00 % to 3.39 %. The 0526 era factor (×3.8 on clause A) makes that ≈ 11 % in a bear market, against ≈ 7.6 % with the live ruler. **That is a prediction, labelled as such**, and it is the third reason the ruler was not applied.

---

## 2. Which clause is over-firing, on which side

### 2a. The breakdown

| | clause A | clause B | total | registered (08-14) |
|---|---|---|---|---|
| LONG | 6 (1.25 %) | 11 (2.29 %) | 17 (3.53 %) | A ~1.2 %, B 2.01 % → **on registration** |
| SHORT | 3 (0.62 %) | **0 (0.00 %)** | 3 (0.62 %) | A ~1.2 %, B 2.14 % → **B silent** |

**What carries the breach: SHORT clause B, dead since the 08-14 re-cut.** It had 481 chances and fired none. LONG is not over-firing against its own registration, though its absolute 3.53 % is the larger number. The side ratio breached because one side went quiet, not because the other got loud.

### 2b. Is a LONG-floor re-cut the whole fix?

**No.** The re-cut LONG floor moves 0.4238 → 0.4214 and removes 1 LONG refusal, #18565. SHORT is untouched at 0.62 %, so the ratio stays at **5.33×**, still breached. The whole fix for the ratio is the SHORT floor. The LONG floor moves too because the rule is per side and both sides were re-cut together, as the pre-registration requires.

### 2c. All 20 refusals, by name

| row | when (UTC) | side | clause | lean (floor then) | nearest opposing wall | daily |
|---|---|---|---|---|---|---|
| #18539 | 2026-08-15 05:40:02 | LONG | B | 0.4210 (0.4238) | ×12.1 · p23 · 0.638 % | bull |
| #18565 | 2026-08-15 07:05:02 | LONG | B | 0.4216 (0.4238) | ×12.9 · p30 · 0.544 % | neutral |
| #18800 | 2026-08-15 20:20:03 | LONG | B | 0.4141 (0.4238) | ×22.8 · p99 · 0.411 % | unlabelled |
| #18913 | 2026-08-16 09:10:14 | LONG | B | 0.4194 (0.4238) | ×20.9 · p99 · 0.464 % | neutral |
| #19221 | 2026-08-17 06:45:07 | LONG | A | 0.5089 (0.4238) | ×19.6 · p92 · 0.172 % | neutral |
| #19660 | 2026-08-18 19:50:08 | LONG | A | 0.4879 (0.4238) | ×19.6 · p92 · 0.169 % | bull |
| #19778 | 2026-08-19 06:25:03 | SHORT | A | 0.4450 (0.3489) | ×23.8 · p90 · 0.195 % | bull |
| #20016 | 2026-08-20 13:35:12 | LONG | A | 0.5687 (0.4238) | ×19.9 · p93 · 0.104 % | bull |
| #20022 | 2026-08-20 14:50:07 | SHORT | A | 0.4664 (0.3489) | ×25.6 · p94 · 0.174 % | bull |
| #20055 | 2026-08-20 18:20:06 | LONG | A | 0.5106 (0.4238) | ×19.2 · p90 · 0.080 % | bull |
| #20058 | 2026-08-20 18:40:04 | LONG | A | 0.5086 (0.4238) | ×19.7 · p92 · 0.104 % | bull |
| #20096 | 2026-08-20 23:15:04 | SHORT | A | 0.4898 (0.3489) | ×24.1 · p91 · 0.172 % | bull |
| #21252 | 2026-08-26 11:05:01 | LONG | B | 0.4135 (0.4238) | ×19.8 · p93 · 0.318 % | bull |
| #21254 | 2026-08-26 11:15:05 | LONG | B | 0.4210 (0.4238) | ×18.0 · p82 · 0.318 % | bull |
| #23096 | 2026-09-02 02:35:01 | LONG | B | 0.4211 (0.4238) | ×16.9 · p73 · 0.130 % | neutral |
| #23337 | 2026-09-02 22:10:01 | LONG | B | 0.3878 (0.4238) | ×18.4 · p85 · 0.060 % | neutral |
| #23370 | 2026-09-02 23:50:01 | LONG | B | 0.4000 (0.4238) | ×9.4 · p6 · 0.060 % | unlabelled |
| #23375 | 2026-09-02 23:55:01 | LONG | B | 0.3825 (0.4238) | ×12.7 · p28 · 0.449 % | unlabelled |
| #24547 | 2026-09-07 02:45:08 | LONG | B | 0.3820 (0.4238) | ×10.2 · p10 · 0.094 % | bull |
| #25482 | 2026-09-10 06:50:03 | LONG | A | 0.4639 (0.4238) | ×20.0 · p94 · 0.196 % | neutral |

**By day:** 08-20 × 5 · 09-02 × 4 · 08-15 × 3 · 08-26 × 2 · one each on 08-16, 08-17, 08-18, 08-19, 09-07, 09-10. **Three days hold 12 of the 20.** 08-20 is the clause-A day: five clause-A refusals, walls at p90–p94 within 0.20 %, between 13:35 and 23:15. 09-02 is a LONG clause-B day. It is less concentrated than 08-12, when one day held 16 of 25, but it is clustered. Five of the eleven LONG clause-B refusals sat within 0.003 of the floor: 0.4210, 0.4216, 0.4194, 0.4210 and 0.4211 against 0.4238. **They are noise-edge refusals.** At the new floor of 0.4214, #18565 is the only one that flips.

---

## 3. What the applied cut would have done — both directions

### 3a. Fate changes over the 962 evaluated rows

- **Admitted that was refused (1):** #18565, LONG, 2026-08-15 07:05:02, lean 0.4216 against the new 0.4214. It was refused by clause B at 0.4238.
- **Refused that was admitted (10), all SHORT, all refused by the advisor anyway (`ai_skipped`), and all under a BULL daily:** #21218 (08-26, lean 0.356), #22026, #22027, #22049, #22053, #22061 (all 08-29, lean 0.359–0.396), #23728 (09-04, 0.381), #24320, #24324 (09-06, 0.381–0.396), #25256 (09-09, 0.394). **No money changes on these ten.** Each was a skip either way; only the refusing gate differs.
- **Executed trades: no change.** All eight executed positions of the era stay admitted: vpos 36 lean 0.532, 37 0.454, 38 0.524, 39 0.485, 40 0.484, 41 0.487, 42 0.467, 43 0.477.

### 3b. 🔴 Did it admit a loser or refuse a winner?

- **It would have admitted one loser, to the advisor:** **#18565 → −1.20R (−$1.20)**. The replay used candle ATR 0.3018 and entry at the candle close (the refused row stores no price), with SL at 2.5×ATR on the live geometry, stopped 2026-08-16 21:40. It would have reached the advisor, not the book directly. The advisor executed 1.0 % of consultations over the last 30 days.
- **It refuses no winner.** Every winner of the era (vpos 38, 39, 40, 41, 43: +4.03, +1.60, +2.55, +1.63, +1.72R) reads "book clear" under the new floors.

### 3c. Volume cost

Entries are unchanged in-sample. None of the eight executed trades is refused, so entries per day stay at **LONG 0.19, SHORT 0.11** (5 and 3 over 27 days). The one newly admitted LONG row adds at most about 0.01 expected entries per day, at the advisor's pass rate. **The re-cut costs no measured volume. It moves ten SHORT refusals from the advisor to the gate** — about 0.37 a day — and that is the point: the gate now does its share on both sides.

---

## 4. Applied — from flat

### 4a. Flat, confirmed twice

- **DB before the change:** `virtual_positions` not closed **0**, `active_positions` **0**, `exit_pending` **0**. The last position was vpos 43, closed 2026-09-06 03:58. The same check ran again inside the apply step, immediately before the file was replaced.
- **Venue, read-only, the bot's own key through Tor** (`/v5/position/list` and `/v5/order/realtime`, SOLUSDT linear): **positionIdx 1 size 0 · positionIdx 2 size 0 · open orders 0**. After the restart, the bot asserted the same by itself: `[BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible`.

### 4b. Backup first; the AST proves only the constants changed

- **Backup:** `config.py.bak_bookgate_recut_20260911T0540Z` (`cp -p`, sha256 `530fb30f…`, the pre-change file). The new `config.py` is `a308a130…`.
- **AST check:** **145 → 145 top-level nodes, exactly one differs, `BOOK_GATE_LEAN_FLOOR`**, now `{'LONG': 0.4214, 'SHORT': 0.3975}`. Everything else added is comment text, which carries no logic.
- **Untouched:** no gate logic, no clause structure and no rule. `book_gate.py` is byte-identical (`efdfd156…`), so `_NEAR_MULT_BREAKS`, `read_book`, `side_pctl` and `evaluate` are all unchanged.

### 4c. Confirmed untouched

- **At runtime, from the loaded bytecode:** the worker's `__pycache__/config.cpython-312.pyc` header matches the new source (mtime 05:40:05, 98,026 bytes). Its code constants contain **0.4214 and 0.3975, and neither 0.4238 nor 0.3489**.
- **Every guarded constant keeps its value; only its line number moved,** because of the new comment block:
  - `SL_BUFFER_ATR` 2.5 · `TRAIL_MULT_ATR` 1.875 · `TRAIL_ARM_R` 0.75 · `CONFLUENCE_SCORE_THRESHOLD` 2.0
  - **`FLAT_ADX_GATE_DRYRUN` True** · `EXIT_ADVISOR_DRYRUN` True · `MAX_POSITIONS_PER_SIDE` 1 · `LIVE_FIXED_MARGIN` 20 · `LEVERAGE` 5
  - `BOOK_GATE_ENABLED` True · `BOOK_GATE_DRYRUN` False · `BOOK_GATE_WALL_PCTL` 90.0 · `BOOK_GATE_WALL_DIST_PCT` 0.20 · `BOOK_GATE_MIN_SUPPORTING` 1
- **The boot line prints the same geometry** (4d).
- **Advisor prompts, byte-identical by sha256.** Computed from the AST literals before and after:
  - `_ENTRY_SYSTEM cc70ed45…`
  - `_CLOSE_SYSTEM 37bcdce4…`
  - `_CLOSE_STATE_SYSTEM 3be10726…`
  - `_LEARNING_SYSTEM aa35142e…`
- **Files, byte-identical:** `claude_advisor.py` `54e71f02…` · `main.py` `a11a7cb3…` · `signal_matrix.py` `a075ce05…` · `book_gate.py` `efdfd156…`.

### 4d. Restart and runtime proof

`systemctl restart mercury-sol.service` at **05:40:05 UTC**. Active since **05:40:08**; master **1181897**, worker **1181966**; `NRestarts = 0` before and after. Boot, verbatim:

```
[MERCURY-SOL] [BOOT] taker fee: 0.001 (0.1000%) source=venue | geometry constant BYBIT_TAKER_FEE_RATE=0.00055 is unchanged and separate
[MERCURY-SOL] [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 1181966]
```

- `/health` → `{"bot":"MERCURY-SOL","exchange":"bybit_live","status":"ok"}`.
- **Contracts,** workspace suite run as `botuser`: **265/265 green before, 265/265 green after** (61 s each).
- **`openitems_guard`:** EXIT=0 before and after. Titan was not touched.

### 4e. The discipline wording stays

The new comment block in `config.py` ends: *"THE BASIS DOES NOT CHANGE. This gate exists because a bot that buys into a wall does something a trader would not — NOT because the data promises money. A re-cut moves the ruler. It does not turn discipline into an edge."* The 08-10 and 08-14 wording above it is kept intact as history, as is `book_gate.py`'s docstring.

---

## 5. Re-registered — and the review made unmissable

### 5a. The new pre-registration, written in `config.py` and in `OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11`

| quantity | expected | source |
|---|---|---|
| refusal rate LONG | **3.33 %** (A 1.25 %, B 2.08 %) | replay over the 481 LONG evaluations |
| refusal rate SHORT | **2.70 %** (A 0.62 %, B 2.08 %) | replay over the 481 SHORT evaluations |
| side ratio | **1.23×** | "rule", not "ban" |
| review point | **200 further gate evaluations, or 2026-10-11 — whichever first**, counted from 2026-09-11 05:40:08 | ≈ 36 evaluations a day ⇒ about 6 days |
| alarm | **above 5 % on either side, or a side ratio above 2× — unchanged** | grounds to revisit: re-cut per side and say so |

Chance of a false alarm at the review point — 200 evaluations in total, about 100 per side — if these rates are true: **LONG 11.7 %, SHORT 5.4 %** (binomial). At 200 per side it would be 7.3 % / 2.1 %. The LONG figure is not small. **A LONG reading between 5 % and 6 % at the first review is within noise, and should be read against this line before anyone re-cuts again.**

### 5b. 🔴 The mechanical reminder — specified in the canon, NOT built

Written into `OPEN-ITEMS-SOL.md §BOOK-GATE-REVIEW-REMINDER`:

1. **A cron counter — no bot change, no restart.** Preferred.
   ```
   */30 * * * * botuser /usr/bin/python3 /home/botuser/.openclaw/workspace/scripts/sol_book_gate_review.py
   ```
   It reads `trades.db` with `mode=ro` and runs:
   ```sql
   SELECT CASE WHEN signal_type='open_long' THEN 'LONG' ELSE 'SHORT' END AS side,
          COUNT(*) AS n, SUM(status='book_blocked') AS refused
   FROM trades
   WHERE (book_gate_lean IS NOT NULL OR status='book_blocked')
     AND timestamp >= '2026-09-11 05:40:08'
   GROUP BY side;
   ```
   - It alerts **once** when n_LONG + n_SHORT ≥ 200, or at 2026-10-11.
   - It alerts **immediately** when a side has n ≥ 50 and a rate above 5 %, or both sides have n ≥ 50 and a ratio above 2×.
   - Alerts go out through `send_full_report(text, require_link=False)`, because they are alerts, not reports.
   - State is kept in a small JSON, so each condition fires once. It gets its own contract: fire on a synthetic 200th row.
2. **A counter the bot prints itself** (a `main.py` change plus a restart): `[BOOK-GATE] review n=N/200 since 2026-09-11 05:40 · LONG r/n · SHORT r/n · ratio x`, logged where the six columns are written.
3. **A digest row.** The same four numbers in the daily SOL digest.

### 5c. 🔴 The missed review — recorded as a named failure

`OPEN-ITEMS-SOL.md §BOOK-GATE-REVIEW-MISSED — NAMED FAILURE, 2026-08-20 23:30:02 UTC` reads: the 200th evaluation after the 08-14 re-cut came on 2026-08-20 23:30:02. LONG was at **9/117 = 7.69 %** and SHORT at **3/83 = 3.61 %**, a ratio of **2.13×**. **Both wires had tripped, and nobody checked for three weeks.** The 2026-09-01 report's "1.03×" pooled refusals from before and after the re-cut, so it was not a test. The breach was found only on 2026-09-11, at 962 evaluations and 5.67×. The operator recorded it as their own failure. The review depended on someone remembering.

### 5d. 🔴 The bear-daily watch item — recorded verbatim

`OPEN-ITEMS-SOL.md §BOOK-GATE-BEAR-WATCH` quotes 0526 §4c word for word: *at the first `trend_1d = BEAR` row the gate evaluates, count the next N = 100 gate evaluations per side, spanning ≥ 5 distinct days; compare against the re-registration and the ≈ 7.6 % SHORT prediction; breach = above 5 % on a side or a side ratio above 2×*. It adds a dated note: compare against the **09-11** re-registration (3.33 % / 2.70 % / 1.23×). Refused rows store no `trend_1d`, so they must take the regime from the nearest row, or the count drops every refusal.

The canon file's stale line was also corrected. The rule box still read `(LONG 0.4323 · SHORT 0.4129)`, the 08-10 floors, a month after they stopped being true. Backup: `OPEN-ITEMS-SOL.md.bak_bookgate_recut_20260911`.

---

## Verification

- **Pre-flight:** `openitems_guard` EXIT=0 before anything else (titan-bot HEAD cd0f175). It returned EXIT=0 again after the restart, and again at the end. **Titan untouched:** its tree is clean in `git status`, its database was not opened, and none of its constants were read or used.
- **Flat before the change:** the DB showed 0 open, 0 active and 0 exit-pending, checked twice, the second time inside the apply step. The venue showed idx 1 = 0, idx 2 = 0 and 0 open orders, read-only through Tor. The bot's own boot assert confirmed venue FLAT after the restart.
- **Changed, by intent:**
  - `config.py`: `530fb30f…` → `a308a130…`; AST 145 → 145 nodes, 1 differs (`BOOK_GATE_LEAN_FLOOR`).
  - `OPEN-ITEMS-SOL.md`: four new sections plus one corrected stale line.
  - Backups: `config.py.bak_bookgate_recut_20260911T0540Z` and `OPEN-ITEMS-SOL.md.bak_bookgate_recut_20260911`.
- **Changed by the running services, not by this pass:** `trades.db` (live bot rows), `oi_cache.json` (`market_context.py`), `optimizer/tg_offset.txt` (the optimizer listener), and `__pycache__/config.cpython-312.pyc`, rewritten by the restart and verified in §4c. **33 of 36** baseline files are byte-identical. The other three are `config.py`, `trades.db` and `oi_cache.json`.
- **Service:** restarted once, by this pass, at 05:40:05. `NRestarts = 0` before and after; master 1181897 (worker 1181966) has run since 05:40:08. Health is ok. One gate evaluation has passed since, an `ai_skipped` row under the new floors.
- **`FLAT_ADX_GATE_DRYRUN = True`** at `config.py:407`, unchanged. `EXIT_ADVISOR_DRYRUN` True, unchanged.
- **Contracts:** 265/265 green before and after, run as `botuser`.
- **Analysis reads:** DB via `mode=ro` SELECTs; `config.py` and `book_gate.py` read as text. No SOL module was imported, except that the running service imported its own new config at restart.
- **Telegram sender:** imported from `/root/titan-bot` with bytecode writing disabled.
