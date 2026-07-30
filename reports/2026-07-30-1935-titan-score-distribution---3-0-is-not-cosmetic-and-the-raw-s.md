# titan score distribution - 3.0 is not cosmetic and the raw scale has a forbidden zone

_2026-07-30 19:35 UTC_

---

# titan-score-distribution-3.0-is-not-cosmetic-and-the-raw-scale-has-a-forbidden-zone

_2026-07-30 19:40 UTC_

---

# TITAN — 🔴 **3.0 IS NOT COSMETIC: 15.7% vs 4.5%. AND ON THE RAW SCALE, 2.75 / 3.00 / 3.25 / 3.50 ARE THE SAME BAR.**

_HEAD `1161802` · clean · 🔴 LIVE, REAL MONEY · vpos 87 LONG open · **READ-ONLY, no outcomes, no recommendation, no code**_

---

## THE ONE NUMBER

**At bar 3.0, the score gate would refuse 94 of 598 TREND signals — 15.7%. Today it refuses 27 —
4.5%. That is a 3.5× increase in refusal volume. It is not cosmetic.**

But the more useful number is the one you did not ask for and would have hit next:

🔴 **The raw score distribution has a hole. No TREND signal in 30 days has ever scored between 2.50
and 3.50.** The 630 TREND events occupy only **22 distinct values**, and the interval (2.50, 3.50] is
empty. On the raw scale, **bars 2.75, 3.00, 3.25 and 3.50 refuse an identical set of 144 events** —
they are the same bar wearing four numbers. Choosing "3.0" over "3.5" on the raw score is a choice
without a difference.

**On the gated scale — which is what the gate actually compares — that degeneracy is broken**
(27 → 33 → 94 → 133 across 2.0/2.5/3.0/3.5), because the ±1.0 macro adjustment shifts a third of the
population off its lattice position. **So the bar you would be setting behaves differently from the
score you would be reading.**

**And the capacity caveat resolves cleanly in your favour below 4.5:** of the 75 capacity refusals in
30 days, the number sitting behind a position that the bar would itself have refused is **3 at bar
2.0–2.5, 8 at 3.0, 21 at 3.5, 24 at 4.0 — then it jumps to 56 at 4.5.** Below 4.0 the replay's
assumption costs little. At 4.5 it swallows three quarters of the series.

---

## 0 · POPULATION, AND THE VALIDATION YOU ASKED ME TO STATE

**Population = every scored event that actually REACHED the score gate**, last 30 days.

`htf_blocked` is excluded for two independent reasons, both of which had to hold: (i) the HTF cascade
runs at `main.py:3676`, **before** the score gate at `:3691`, so those signals never reached it; and
(ii) their stored breakdown is `−HTF_PENALTY`-adjusted and would corrupt the distribution.

```
scored events reaching the score gate, 30d : 1533
  TREND  630      FLAT  903
  by status: ai_skipped 831 · below_threshold 594 · virt_cap_blocked 39 · risk_halt 39
             executed 27 · failed 2 · claude_unavailable 1
  rows with no usable proposed direction, dropped: 0
```

Regime is reconstructed exactly as §2b did — `TREND` iff the stored breakdown's `TREND` category has
`net_direction != NEUTRAL`, which is the same expression `signal_matrix.compute_score` uses to set
`market_regime`. `direction_score` is re-summed from the post-resolution `contribution` fields;
`gated = direction_score + macro_gate_penalty`.

### 🔴 The validation — and it initially FAILED, so here is the full diagnosis rather than a clean number

The previous report validated in **one direction only**: every `below_threshold` row satisfies
`gated < eff_thr` — **0 of 593 contradictions**. That statement was true and is still true. It was
also **not the whole test.** Running the reverse direction — every *passing* row must satisfy
`gated >= eff_thr` — produced **143 violations.** All 143 are diagnosed; none is a rule violation.

| | n | cause |
|---|---:|---|
| **140** | pre-`db71454` | 🔴 **The FLAT floor did not exist yet.** `CONFLUENCE_FLAT_THRESHOLD` was created by **`db71454`, 2026-07-06 13:54:42**. Before that instant `_eff_thr` was unconditionally 2.0, so a FLAT event at 4.25 **correctly** passed. **21.1% of the 30-day window (324 of 1533 rows) predates the floor.** |
| **3** | ids 19614 / 19615 / 19622, 2026-07-30 04:30–05:05 | 🔴 **`macro_gate_penalty` is not persisted on the `risk_halt` branch.** `main.py:3785` writes `confluence_score`, `matrix_direction` and `matrix_breakdown_json` but **not** `macro_gate_penalty` and **not** `market_regime`. All three rows are FLAT with raw 4.25; their immediate neighbours (19616 / 19619 / 19620, same 35-minute window, same SHORT direction) all carry `macro_gate_penalty = +1.0`. With +1.0 the gated score is **5.25 ≥ 5.0** and the pass is correct. The reconstruction read the missing column as 0.0 and undercounted. |

**Post-diagnosis validation, era-aware:**

| regime | era | n | refused-rows violating the rule | passing-rows violating the rule |
|---|---|---:|---:|---:|
| TREND | pre-floor | 121 | **0** | **0** |
| TREND | post-floor | 509 | **0** | **0** |
| **TREND** | **ALL 30d** | **630** | 🔴 **0** | 🔴 **0** |
| FLAT | pre-floor | 203 | **0** | **0** |
| FLAT | post-floor | 700 | **0** | 3 *(the unpersisted-`macro_gate_penalty` rows above)* |

🔴 **The TREND analysis is unaffected by the era boundary and needs no split.** `db71454` only added
the FLAT branch; the TREND bar was 2.0 both before and after it. **All 630 TREND events sit on one
rule, and the reconstruction is exact in both directions on all of them.** The FLAT analysis (§5) is
era-split because it must be.

**Two data defects recorded in passing, since they limit what can ever be audited here:**
`macro_gate_penalty` and `market_regime` are absent on all 39 `risk_halt` rows, so those rows'
gate arithmetic is only recoverable by inference from neighbours. And `confluence_score` means three
different things depending on `status`: `_gated_score` on `below_threshold`, **`adj_score`** (the
weight-engine number) on `ai_skipped` / `virt_cap_blocked` / `risk_halt`, and the **raw** score on
`executed` (overwritten by `signal_matrix.snapshot()`). **137 of the 143 anomaly rows have a stored
`confluence_score` that does not equal their own raw direction score** — that is the `adj_score`
write, visible in the data. Nothing here reads that column; everything is recomputed from the
breakdown.

---

## 1 · TREND · RAW `direction_score` — the histogram

**n = 630 · min 2.25 · median 4.25 · max 9.00 · 0.25 buckets · all 30 days, one rule**

| score | n | share | cum n | **cum share** | |
|---:|---:|---:|---:|---:|---|
| **2.25** | 23 | 3.7% | 23 | **3.7%** | ██ |
| **2.50** | **121** | **19.2%** | 144 | **22.9%** | ██████████ |
| 2.75 | 🔴 **0** | — | 144 | 22.9% | |
| 3.00 | 🔴 **0** | — | 144 | 22.9% | |
| 3.25 | 🔴 **0** | — | 144 | 22.9% | |
| 3.50 | 4 | 0.6% | 148 | 23.5% | █ |
| 3.75 | 18 | 2.9% | 166 | 26.3% | █ |
| 4.00 | 48 | 7.6% | 214 | 34.0% | ████ |
| **4.25** | **116** | **18.4%** | 330 | **52.4%** | █████████ |
| 4.50 | 22 | 3.5% | 352 | 55.9% | ██ |
| 4.75 | 18 | 2.9% | 370 | 58.7% | █ |
| 5.00 | 52 | 8.3% | 422 | 67.0% | ████ |
| 5.25 | 3 | 0.5% | 425 | 67.5% | █ |
| 5.50 | 17 | 2.7% | 442 | 70.2% | █ |
| 5.75 | 7 | 1.1% | 449 | 71.3% | █ |
| **6.00** | 59 | 9.4% | 508 | 80.6% | █████ |
| 6.25 | 18 | 2.9% | 526 | 83.5% | █ |
| 6.50 | 15 | 2.4% | 541 | 85.9% | █ |
| **6.75** | 52 | 8.3% | 593 | 94.1% | ████ |
| 7.00 | 7 | 1.1% | 600 | 95.2% | █ |
| 7.25 | 6 | 1.0% | 606 | 96.2% | █ |
| 7.50 | 14 | 2.2% | 620 | 98.4% | █ |
| 7.75 | 4 | 0.6% | 624 | 99.0% | █ |
| 8.50 | 4 | 0.6% | 628 | 99.7% | █ |
| 9.00 | 2 | 0.3% | 630 | 100.0% | █ |

🔴 **The distribution is not continuous — it is a lattice with holes.** 630 events occupy **22 of the
28 possible 0.25 buckets** between 2.25 and 9.00, and the gaps are not in the tail:

```
occupied: 2.25 2.50 | ─── HOLE ─── | 3.50 3.75 4.00 4.25 4.50 4.75 5.00 5.25 5.50 5.75
          6.00 6.25 6.50 6.75 7.00 7.25 7.50 7.75 | HOLE | 8.50 | HOLE | 9.00
empty in the decision range: 2.75  3.00  3.25
```

**Why: the score is a sum of at most four category contributions, each capped at 2.50 and quantised by
the signal intensity table.** Two live categories at full weight give 5.00; one full plus one partial
gives 4.25; and the single-category-plus-trigger floor is 2.25–2.50. **The values between 2.50 and
3.50 are not rare — they are unreachable by the arithmetic.**

**Consequence, stated before any level is chosen:**

| refuse count | share | bars that produce it | |
|---:|---:|---|---|
| 0 | 0.0% | **2.00, 2.25** | indistinguishable |
| 23 | 3.7% | 2.50 | |
| **144** | **22.9%** | 🔴 **2.75, 3.00, 3.25, 3.50** | **indistinguishable — four numbers, one bar** |
| 148 | 23.5% | 3.75 | |
| 166 | 26.3% | 4.00 | |

---

## 2 · TREND · GATED score (`raw + total_gate_adj`) — what the gate actually compares

**n = 598** of 630 — the 32 excluded are `risk_halt` rows where `macro_gate_penalty` is not written
(§0). **min 1.25 · median 4.75 · max 8.75.**

| score | n | share | cum n | **cum share** | |
|---:|---:|---:|---:|---:|---|
| 1.25 | 6 | 1.0% | 6 | 1.0% | █ |
| 1.50 | 21 | 3.5% | 27 | **4.5%** | ██ |
| 2.00 | 1 | 0.2% | 28 | 4.7% | █ |
| 2.25 | 5 | 0.8% | 33 | 5.5% | █ |
| **2.50** | 58 | 9.7% | 91 | 15.2% | █████ |
| 2.75 | 3 | 0.5% | 94 | **15.7%** | █ |
| 3.00 | 11 | 1.8% | 105 | 17.6% | █ |
| 3.25 | 28 | 4.7% | 133 | 22.2% | ██ |
| **3.50** | 48 | 8.0% | 181 | 30.3% | ████ |
| 3.75 | 14 | 2.3% | 195 | 32.6% | █ |
| 4.00 | 20 | 3.3% | 215 | 36.0% | ██ |
| **4.25** | **71** | **11.9%** | 286 | 47.8% | ██████ |
| 4.50 | 9 | 1.5% | 295 | 49.3% | █ |
| 4.75 | 14 | 2.3% | 309 | **51.7%** | █ |
| **5.00** | **69** | **11.5%** | 378 | 63.2% | ██████ |
| 5.25 | 24 | 4.0% | 402 | 67.2% | ██ |
| 5.50 | 21 | 3.5% | 423 | 70.7% | ██ |
| 5.75 | 14 | 2.3% | 437 | 73.1% | █ |
| 6.00 | 35 | 5.9% | 472 | 78.9% | ███ |
| 6.25 | 15 | 2.5% | 487 | 81.4% | █ |
| 6.50 | 13 | 2.2% | 500 | 83.6% | █ |
| 6.75 | 27 | 4.5% | 527 | 88.1% | ██ |
| 7.00 | 23 | 3.8% | 550 | 92.0% | ██ |
| 7.25 | 10 | 1.7% | 560 | 93.6% | █ |
| 7.50 | 11 | 1.8% | 571 | 95.5% | █ |
| 7.75 | 14 | 2.3% | 585 | 97.8% | █ |
| 8.00 | 5 | 0.8% | 590 | 98.7% | █ |
| 8.50 | 7 | 1.2% | 597 | 99.8% | █ |
| 8.75 | 1 | 0.2% | 598 | 100.0% | █ |

🔴 **The macro adjustment fills the hole.** The raw scale has 22 occupied values; the gated scale has
**29**, and **every 0.25 step from 2.00 to 5.00 is populated.** The ±1.0 news adjustment maps the
2.50 cluster onto 1.50 and 3.50, and the 4.25 cluster onto 3.25 and 5.25. **The forbidden zone in the
raw score is an artefact of the category arithmetic; the gated score does not have it.**

**This matters directly for how a bar behaves:** on the raw scale a bar at 3.0 and a bar at 3.5 are
identical; on the gated scale they differ by **39 signals (6.5 points of refusal share)**. The
constant is compared to the gated number, so **the gated column is the one that governs**, and the raw
column is what you would see on the card.

**Also visible here and worth one line:** the gated distribution has a shoulder below 2.0 —
**27 events at 1.25/1.50, all of them TREND**. Those are the 27 refusals the 2.0 bar produces, and
§4 of the previous report established every one of them is the macro penalty dragging a 2.25/2.50
under. The raw column confirms it from the other side: **min raw TREND = 2.25, so nothing arrives
below 2.0 on its own.**

---

## 3 · THE OPERATIONAL NUMBER — SHARE OF TREND SIGNALS REFUSED AT EACH BAR

Volume only. No outcomes.

| bar | refused (**gated**, n=598) | **share** | admitted | step cost | refused (raw, n=630) | share |
|---:|---:|---:|---:|---:|---:|---:|
| **2.0** *(today)* | **27** | 🔴 **4.5%** | 571 | — | 0 | 0.0% |
| 2.5 | 33 | 5.5% | 565 | +6 | 23 | 3.7% |
| **3.0** | **94** | 🔴 **15.7%** | 504 | **+61** | 144 | 22.9% |
| 3.5 | 133 | 22.2% | 465 | +39 | 144 | 22.9% |
| **4.0** | **195** | **32.6%** | 403 | **+62** | 166 | 26.3% |
| 4.5 | 286 | 47.8% | 312 | 🔴 **+91** | 330 | 52.4% |
| 5.0 | 309 | 51.7% | 289 | +23 | 370 | 58.7% |

### Is 3.0 cosmetic or drastic? — **Neither. It is a real but middle step, and its position is unstable.**

- **Against today: 3.5× the refusal volume** — 94 signals instead of 27, 15.7% instead of 4.5%.
  **Not cosmetic.**
- **Against the ceiling: it refuses less than a sixth.** 84.3% of TREND signals still pass. Compare
  4.5, which refuses nearly half. **Not drastic either.**
- 🔴 **It is unstable in a way a single number hides.** The step from 2.5 to 3.0 costs **+61 signals**,
  almost all of them the single gated bucket at **2.50 (n=58, 9.7%)**. A bar at 3.0 is, to a first
  approximation, *one decision*: whether to keep or drop the 2.50 cluster. Move to 2.75 and you get
  91 of those 94 refusals; move to 3.25 and you get 133. **The bar is not measuring a gradient — it is
  picking a side of one mode.**

**The full 0.25-granularity view, so no plateau is hidden:**

```
bar   raw refused        gated refused
2.00      0   0.0%          27   4.5%
2.25      0   0.0%  ← same  28   4.7%
2.50     23   3.7%          33   5.5%
2.75    144  22.9%          91  15.2%
3.00    144  22.9%  ← same  94  15.7%
3.25    144  22.9%  ← same 105  17.6%
3.50    144  22.9%  ← same 133  22.2%
3.75    148  23.5%         181  30.3%
4.00    166  26.3%         195  32.6%
4.25    214  34.0%         215  36.0%
4.50    330  52.4%         286  47.8%
4.75    352  55.9%         295  49.3%
5.00    370  58.7%         309  51.7%
```

🔴 **The single largest step anywhere in the range is 4.25 → 4.50 on the gated scale: +71 signals in
one 0.25 move** (215 → 286), because the 4.25 bucket alone holds 71 events (11.9%). **The second is
2.50 → 2.75, +58.** Everything between those two modes is comparatively flat. **If a level is chosen,
the thing that determines its cost is which of the two big clusters — 2.50 and 4.25 — falls on which
side of it.**

---

## 4 · THE CAPACITY THE REPLAY ASSUMED AWAY — QUANTIFIED

§2's caveat 2 said: refusing a trade is not a no-op, because it frees the position slot. Here is the
number instead of the caveat.

### The series is bigger than 36 — it is 75, and the other 39 are the paper-era half

`concurrent_position_halt` (`risk_halt`) queries the **live exchange**, so during paper mode it saw
nothing and never fired. The paper-era equivalent is `virtual_trader.open_position`'s own cap check,
which queries the **DB** and produces `virt_cap_blocked`. **They are the same phenomenon on two
adapters and both belong in the answer.**

```
capacity refusals, 30d : 75
   virt_cap_blocked      39   spread over 17 days, 2026-07-02 → 2026-07-28   (paper era)
   position-cap risk_halt 36   2026-07-29 20:10 → 2026-07-30 18:55           (live era)
resolvable to a scored blocking position : 66 of 75  (9 unresolvable: 8 virt_cap + 1 risk_halt with no
                                                     matching open row — the 2026-07-29 20:10 halt,
                                                     which falls in the naked-position window)
```

🔴 **Every one of the 36 position-cap halts comes from just two positions**, both opened in the last
42 hours — **vpos 87 blocked 26 signals, vpos 86 blocked 9.** There were zero before 2026-07-29.
**That series is a going-live artefact, not a 30-day rate.** The `virt_cap_blocked` series is the
one with history: 39 blocks behind **12 distinct positions** over 26 days.

### The number

**"Of the capacity refusals, how many sat behind a position that bar X would itself have refused?"** —
i.e. the slot the replay silently assumed would be free anyway. Counterfactual applied under **today's**
rule-set (FLAT floor 5.0 active for all rows).

| bar | blocked behind a would-be-refused position | of all 75 | of the 66 resolvable | TREND-owner only |
|---:|---:|---:|---:|---:|
| **2.0** | **3** | 4.0% | 4.5% | 0 |
| 2.5 | 3 | 4.0% | 4.5% | 0 |
| **3.0** | **8** | 10.7% | 12.1% | 5 |
| 3.5 | 21 | 28.0% | 31.8% | 18 |
| **4.0** | **24** | **32.0%** | 36.4% | 21 |
| **4.5** | 🔴 **56** | 🔴 **74.7%** | 84.8% | 53 |
| 5.0 | 56 | 74.7% | 84.8% | 53 |

The 3 at bar 2.0–2.5 are all one position — **vpos 63, the only FLAT-regime blocker in the set**
(gated 3.5, opened 2026-07-03, i.e. **pre-floor**, so historically it was not refused; under today's
5.0 floor it would be). **The TREND-owner column excludes it and every other FLAT case, and is the
cleaner read of the same question: 0 / 0 / 5 / 18 / 21 / 53 / 53.**

Every blocking position, ranked:

```
vpos 87 LONG  TREND gated 4.25  blocked 26   opened 2026-07-30 12:05   ← still open
vpos 86 SHORT TREND gated 5.75  blocked  9   opened 2026-07-30 00:50
vpos 79 LONG  TREND gated 3.25  blocked  6   opened 2026-07-20 15:45
vpos 68 SHORT TREND gated 2.75  blocked  4   opened 2026-07-06 12:00
vpos 80 SHORT TREND gated 3.00  blocked  4   opened 2026-07-23 18:00
vpos 63 LONG  FLAT  gated 3.50  blocked  3   opened 2026-07-03 05:50
vpos 64 LONG  TREND gated 4.00  blocked  3   opened 2026-07-03 20:10
vpos 81 SHORT TREND gated 3.50  blocked  3   opened 2026-07-24 11:00
vpos 83 SHORT TREND gated 4.25  blocked  3   opened 2026-07-28 01:00
vpos 62 LONG  TREND gated 3.25  blocked  1   opened 2026-07-02 13:20
vpos 65 LONG  TREND gated 7.75  blocked  1   opened 2026-07-04 18:00
vpos 74 SHORT TREND gated 3.25  blocked  1   opened 2026-07-13 05:05
vpos 77 SHORT TREND gated 3.25  blocked  1   opened 2026-07-17 13:10
vpos 78 LONG  TREND gated 2.50  blocked  1   opened 2026-07-20 00:15
```

### What this does to §2's caveat

🔴 **Below 4.0 the caveat is small: at bar 3.0 only 8 of 75 capacity refusals (5 with a TREND owner)
sat behind a position the bar would have removed.** The replay's assumption is close to harmless
there.

🔴 **At 4.5 the caveat swallows the series: 56 of 75, 74.7%.** Because vpos 87 (gated 4.25) alone
accounts for 26 of them, and it crosses from "kept" to "refused" between 4.25 and 4.50 — the same
cluster boundary that dominates §3.

**Two limits on this number, stated rather than buried.** (i) It counts **opportunities freed, not
trades gained** — whether any of those 75 signals would have passed the LLM gate afterwards is
unknown and not modelled; 831 `ai_skipped` in the same window says most would not. (ii) **35 of the 75
are two days old and both live**, so the live half of the series has n=2 positions behind it.

---

## 5 · FLAT REGIME ON THE SAME SCALE — era-split, because it must be

**FLAT is 903 of the 1533 events (58.9%)** — the majority of everything reaching the score gate. It is
judged against `CONFLUENCE_FLAT_THRESHOLD = 5.0`, which has existed only since **2026-07-06 13:54:42**.

### 5a · POST-floor era — the rule that runs today · n = 700 (693 with a recorded macro adj)

**RAW `direction_score` · min 1.75 · median 3.75 · max 7.50**

| score | n | share | cum share | |
|---:|---:|---:|---:|---|
| **1.75** | **119** | **17.0%** | 17.0% | ████████ |
| 2.50 | 52 | 7.4% | 24.4% | ████ |
| 3.00 | 17 | 2.4% | 26.9% | █ |
| **3.50** | **142** | **20.3%** | 47.1% | ██████████ |
| 3.75 | 49 | 7.0% | 54.1% | ████ |
| 4.00 | 7 | 1.0% | 55.1% | █ |
| **4.25** | **157** | **22.4%** | **77.6%** | ███████████ |
| 4.50 | 20 | 2.9% | 80.4% | █ |
| 4.75 | 18 | 2.6% | **83.0%** | █ |
| 🔴 **5.00 — the floor** | 40 | 5.7% | 88.7% | ███ |
| 5.25 | 8 | 1.1% | 89.9% | █ |
| 5.50 | 5 | 0.7% | 90.6% | █ |
| 5.75 | 3 | 0.4% | 91.0% | █ |
| 6.00 | 29 | 4.1% | 95.1% | ██ |
| 6.25 | 8 | 1.1% | 96.3% | █ |
| 6.50 | 1 | 0.1% | 96.4% | █ |
| 6.75 | 21 | 3.0% | 99.4% | ██ |
| 7.00 | 3 | 0.4% | 99.9% | █ |
| 7.50 | 1 | 0.1% | 100.0% | █ |

**GATED · min 0.75 · median 3.50 · max 7.75 · n = 693**

| score | n | share | cum share | | score | n | share | cum share |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 0.75 | 11 | 1.6% | 1.6% | | 4.00 | 16 | 2.3% | 57.4% |
| 1.50 | 5 | 0.7% | 2.3% | | **4.25** | **90** | **13.0%** | 70.4% |
| **1.75** | **83** | **12.0%** | 14.3% | | 4.50 | 44 | 6.3% | 76.8% |
| 2.00 | 5 | 0.7% | 15.0% | | 4.75 | 18 | 2.6% | 🔴 **79.4%** |
| 2.50 | 49 | 7.1% | 22.1% | | **5.00** | 37 | 5.3% | 84.7% |
| 2.75 | 40 | 5.8% | 27.8% | | 5.25 | 42 | 6.1% | 90.8% |
| 3.00 | 8 | 1.2% | 29.0% | | 5.50 | 8 | 1.2% | 91.9% |
| 3.25 | 31 | 4.5% | 33.5% | | 5.75 | 6 | 0.9% | 92.8% |
| **3.50** | **118** | **17.0%** | 50.5% | | 6.00 | 19 | 2.7% | 95.5% |
| 3.75 | 32 | 4.6% | 55.1% | | 6.25–7.75 | 31 | 4.5% | 100.0% |

**Refusal share by bar, FLAT post-floor era (gated, n=693):**

| bar | refused | **share** | step cost |
|---:|---:|---:|---:|
| 2.0 | 99 | 14.3% | — |
| 2.5 | 104 | 15.0% | +5 |
| 3.0 | 193 | 27.8% | +89 |
| 3.5 | 232 | 33.5% | +39 |
| 4.0 | 382 | 55.1% | +150 |
| 4.5 | 488 | 70.4% | +106 |
| 🔴 **5.0 — THE LIVE FLOOR** | 🔴 **550** | 🔴 **79.4%** | +62 |
| 5.5 | 629 | 90.8% | +79 |
| 6.0 | 643 | 92.8% | +14 |
| 6.5 | 664 | 95.8% | +21 |

### 5b · PRE-floor era, for completeness · n = 203

RAW: min 1.75, median 4.00, max 7.00 — same two big modes (**3.50 at 24.6%, 4.25 at 27.1%**).
GATED refusal share: 2.0 → 8.4% · 3.0 → 20.7% · 4.0 → 52.2% · 5.0 → 77.3% · 6.0 → 89.7%.
**Shape is indistinguishable from the post-floor era; only the rule applied to it changed.**

### 🔴 Both gates on one scale — the comparison you asked for

| | TREND | FLAT (post-floor) |
|---|---:|---:|
| population reaching the score gate | 630 (41.1%) | **903 (58.9%)** |
| live bar | **2.0** | **5.0** |
| **share refused at the live bar** | 🔴 **4.5%** | 🔴 **79.4%** |
| median gated score | 4.75 | **3.50** |
| raw score at the 50th percentile | 4.25 | 3.75 |
| bar's percentile position in its own distribution | ~**4th** | ~**79th** |

🔴 **The two halves of one gate sit at opposite ends of their own distributions.** The TREND bar sits
below the 5th percentile of TREND scores; the FLAT floor sits near the 80th percentile of FLAT scores.
**A signal in FLAT faces a bar that rejects four out of five; the same signal in TREND faces one that
rejects one in twenty-two.** And the thing that decides which side it lands on is `market_regime` —
the *presence* of a 1h TREND-category signal, not a measurement (§2.13).

**One number that puts the asymmetry in a single line.** To refuse the same **79.4%** share in TREND
that the FLAT floor refuses today, the TREND bar would have to sit between **6.25** (refuses 78.9%)
and **6.50** (81.4%) — call it **≈6.3**, against the 2.0 it is at. Going the other way, to refuse only
the TREND share of **4.5%** in FLAT, the floor would have to drop between **1.75** (2.3%) and **2.00**
(14.3%) — **≈1.8**, against the 5.0 it is at. **The two constants are roughly 4.3 points apart in
strictness on a 10-point scale, and nothing in the code says that was intended.**

---

## WHAT THIS DOES AND DOES NOT ANSWER

- ✅ The distribution, both scales, both regimes, with the era boundary handled and the validation
  stated in **both** directions.
- ✅ The refusal volume at every bar from 2.0 to 5.0, at 0.25 granularity, with plateaus exposed.
- ✅ The capacity number, on the full 75-refusal series rather than the 36 the live era shows.
- ❌ **No outcomes.** Nothing here says whether a refused signal would have won or lost.
- ❌ **No recommendation.** No level is proposed, endorsed or implied.
- ❌ **What the LLM gate would have done to the freed capacity** is not modelled. 831 `ai_skipped` in
  the same window is the relevant order of magnitude, and it is not a substitute for the calculation.

## WHAT I DID NOT DO

- **Read-only throughout.** No code, config, flag or DB row was written. `virtual_trader` was not
  imported (its module-scope `init_db()` migrates the production schema on import — §2.33).
- **I did not quietly drop the 143 validation failures.** They are diagnosed above: 140 are the
  pre-`db71454` era, 3 are an unpersisted column on the `risk_halt` branch.
- **I did not restate the previous report's "0 of 593" as if it had been a full check.** It was
  one-directional, it was correct as written, and the reverse direction is run here for the first time.

---

*Titan · 2026-07-30 19:40 UTC · HEAD `1161802` clean · 🔴 LIVE · vpos 87 open · READ-ONLY ·
TREND n=630, validation 0/0 both directions · **bar 3.0 refuses 15.7% of TREND signals vs 4.5% today** ·
**no TREND signal has ever scored in (2.50, 3.50] — on the raw scale 2.75/3.00/3.25/3.50 are one bar** ·
capacity cost of the replay: **8 of 75 at bar 3.0, 56 of 75 at bar 4.5** · FLAT floor refuses **79.4%**
against TREND's **4.5%***
