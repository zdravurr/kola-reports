# titan-agreement-line-states-the-gate-count-news-flip-dies-advisor-earns-its-place

_2026-09-26 17:01 UTC_

---

# Titan — **the entry prompt no longer tells the advisor "all agree" when the gate counted fewer. APPLIED FROM FLAT, `991b333`.** Measured what code already knows: the **news-flip rule DOES NOT SURVIVE** (it is the score, and a clock). The advisor **misread tier agreement on 61 % of claim-making executes**, all in the direction the lying line pushed. The entry advisor **earns its place**: its refusals, replayed under the live contract, lose **−13.37R**, and advisor-on beats advisor-off by **+20.7R**. Most of that saving comes from not trading; its per-trade selection edge is **not** significant.

**2026-09-26 · titan-bot HEAD `f53d048` → `991b333` · Titan LIVE REAL MONEY · Mercury-SOL NOT TOUCHED · `openitems_guard` EXIT=0 before and after**

---

## THE VERDICT FIRST

| § | result |
|---|---|
| **§1 Agreement line** | ✅ **APPLIED FROM FLAT.** Restarted 2026-09-26 16:57:26 UTC. `signal_tiers.render` only. RED on `f53d048` (8 failing) → GREEN 27/27, root and botuser, live `trades.db` opened **0** times. The four SYSTEM prompts are sha256-identical. |
| **§1c population** | Current prompt form: **119 of 341 consultations (34.9 %)** printed agreement the gate had not counted, including **19 of 28 executes (67.9 %)**, which cover 18 of the 27 live positions. Before 07-29 a fixed sentence did the same on **2,453 of 2,767 (88.7 %)**. In **16 of the 19** current-form misleading executes, the reason cites that agreement. |
| **§2 news-flip** | 🔴 **THE RULE DOES NOT SURVIVE. No gate diff.** On live, news-flipped = count-1 = raw < 3.0: the same 6 positions. It is **candidate 30's variable (the score)**. It fails Bonferroni (best p 0.027 against α 0.0083), the chronological halves (the sign reverses), and the regime split (FLAT leg empty). It **vanishes on day-matching, exactly like SOL's clock**. It would refuse **vpos 94 (+0.865R, trail)** live and **vpos 81 (+0.770R, trail)** on paper. |
| **§3a misread** | Current form: **18 of 51 claim-making reasons (35.3 %)** misread tier agreement (17 half-reads, 1 false). On executes it is **14 of 23 (60.9 %)**. All 17 half-reads were `execute` votes; 17 of 17 claim-making skips read it correctly. |
| **§3b does a misread predict a loss?** | **No.** Live: misread n 13, **+3.24R**; correct n 9, −3.35R. The two books point opposite ways. It is a text defect, not a money signal. |
| **§3c does the entry advisor earn its place?** | ✅ **YES, mostly by abstaining.** Its refusals replayed under the live contract: **173 resolved, ΣR −13.37** (live era 45, **−9.02**). **Advisor ON −0.81R on 74 vs OFF −21.50R on 197, worth +20.7R** (live era +7.9R). Per-trade selection edge: +0.039 vs −0.147R, day-clustered 95 % CI **[−0.14, +0.48]**, which crosses zero. Same direction as SOL on 2026-09-11 (refusals saved 7.11R). |

**Nothing from one trade. No new filter.**

---

# 1. THE Agreement LINE — FIXED, APPLIED FROM FLAT

## 1a. How it was built (`signal_tiers.py` @ `f53d048`)

- `build()` line **188**: `out['agreement'] = _agreement(out['tiers'], proposed_direction)`
- `_agreement()` lines **221–262** read exactly these inputs, per tier: `t['present']` and `t['direction']`, the **SLOT** direction from `state_machine`, plus `proposed_direction`. It groups the tiers whose slot says LONG/SHORT, then prints `"… all point X; vs the proposed X: A+B+C agree"`, plus NEUTRAL (reset) and ABSENT tails.
- 🔴 **It never reads `counted_by_gate`, `gate_direction` or `not_counted`.** `build()` computes all three at lines 132–186 of the same function, one call earlier.
- `render()` line **419**: `lines.append(f"  Agreement: {facts.get('agreement')}")`
- The same string is persisted in `entry_tiers_json` and printed by the EXIT advisor as `Agreement at entry:` (`entry_thesis_lines`, line 452).

## 1b. The fix: states what the GATE counted

`render()` now calls `_gate_agreement(facts)`. It is built only from the `counted_by_gate`, `gate_direction` and `not_counted` fields that `build()` already captured. Nothing is recomputed. The output is facts only, with no instruction, no "therefore" and no lean.

It is **render-only**. `facts['agreement']` is unchanged, so:
- the persisted `entry_tiers_json` is untouched;
- the **EXIT advisor's `Agreement at entry:` line still prints the slot sentence.** That prompt is under `§0.EXIT-ADVISOR-RULE`, and moving it creates its own cohort boundary. It is **recorded in canon as found and not changed. Your call.**

**Degrades to today's sentence byte-identical** when any tier lacks a boolean `counted_by_gate`, or a counted tier lacks a LONG/SHORT `gate_direction`. That covers no breakdown, malformed input, and `AI_ADVISOR_HIDE_1H`: that flag strips the 1H gate direction so it cannot leak, and it still cannot.

**Census over every stored tier record (341), read-only:**
- **237** render the new line.
- **104** fall back to today's sentence. All 104 are dated 07-29 → 08-05, the `AI_ADVISOR_HIDE_1H` era.
- **341 of 341** differ from the old block in the Agreement line only.
- 0 exceptions. 0 instruction words.

## 1d. vpos 112 — before / after, on its stored prompt (trades 34546)

```
BEFORE:  Agreement: 15m and 1H and 5m all point LONG; vs the proposed LONG: 15m+1H+5m agree.
AFTER:   Agreement: Counted by the gate: 1 of 3 tiers (1H LONG); vs the proposed LONG: 1H agrees. 15m and 5m point LONG on their slots but net NEUTRAL inside their categories and were not counted.
```

**Whole-prompt diff** (the stored `ai_user_prompt` with the old render replaced by the new; the old render is found verbatim in the stored prompt):
```
--- stored 34546
+++ patched 34546
@@ -7 +7 @@
-  Agreement: 15m and 1H and 5m all point LONG; vs the proposed LONG: 15m+1H+5m agree.
+  Agreement: Counted by the gate: 1 of 3 tiers (1H LONG); vs the proposed LONG: 1H agrees. 15m and 5m point LONG on their slots but net NEUTRAL inside their categories and were not counted.
```

**Other shapes (exact, pinned in the contract):**
- `Counted by the gate: 3 of 3 tiers (1H LONG, 15m LONG, 5m LONG); vs the proposed LONG: 1H+15m+5m agree.`
- `Counted by the gate: 3 of 3 tiers (1H SHORT, 15m LONG, 5m LONG); vs the proposed LONG: 15m+5m agree, 1H OPPOSES.`
- `… 15m points SHORT on its slot but the matrix had expired it on its category TTL and it was not counted. 5m points LONG on its slot but nets NEUTRAL inside its category and was not counted.`
- `… 15m was counted from a signal its slot no longer holds (slot ABSENT).`
- `Counted by the gate: 0 of 3 tiers; vs the proposed SHORT: no tier counted. 1H and 15m are ABSENT and were not counted. …`
- `… 1H is NEUTRAL on its slot (reset) and was not counted.`

## 1d (cont.). Contract — `tests/test_agreement_line_states_gate_count.py`

**27 checks.** The vpos 112 fixture is **embedded** (copied read-only from trades 34546), so the contract never touches the DB.

| group | pins |
|---|---|
| A1–A3 | The baseline renders the stored block verbatim. The new line is exact. The whole prompt differs in ONE line. |
| C1–C6 | Six tier shapes, exact strings; every other line byte-identical. |
| D | No instruction vocabulary (`therefore / should / skip / execute / lean / consider / avoid / caution / risk / favour / recommend / suggest`). |
| E | `facts['agreement']` and `entry_thesis_lines` byte-identical, so the exit side is untouched. The four SYSTEM prompts are sha256-pinned. |
| B1–B4 | No breakdown, partial breakdown, 8 malformed inputs (exceptions included), and `AI_ADVISOR_HIDE_1H`: all byte-identical to the baseline, and no hidden-1H leak. |

| run | root | botuser |
|---|---|---|
| **RED**, subject = `f53d048` file | **8 failing**: A2, A3, C1–C6. Every identity pin passes. | **8 failing**, same |
| **GREEN**, subject = patch | **27/27** | **27/27** |
| all 8 Titan contracts | **8/8 GREEN**, `trades.db` opens **0** | **8/8 GREEN**, `trades.db` opens **0** |

**How the botuser pass was run, stated plainly.** `/root` is `drwx------`. botuser used sha256-pinned byte copies in `/tmp/titan-contract-agreement`: `.py` sources, baselines and `tests/`, with **no `.env`, no DB, no logs**.
- The sandbox copy of `tests/_dict_local.py` hardcodes `/root/titan-bot/signal_matrix.py`, which botuser cannot read. It was pointed at the sandbox's sha-identical copy (`0e4128911c283b2f`) **in the sandbox only**. Without that, even the unchanged 09-12 contract fails as botuser.
- **Harness fixes during the pass, disclosed:**
  1. My first contract run opened `trades.db` once as root. The real `signal_matrix` was imported through `signal_tiers._weight_of`. I added the `tests/` shim to `sys.path`, as the 09-12 contract does. Re-traced: 0 opens.
  2. **The 2026-09-12 contract `test_entry_tiers_matrix_names_ages.py` pinned the Agreement line UNCHANGED** ([4]), and three of its block comparisons ([1], [3], [6]) included that line. It was updated deliberately: those comparisons now exclude the Agreement line only, and [4] now pins the new gate-count line. `.bak_agreementline_20260926` kept. 9/9 GREEN.
  3. A dry-run command copied a temp file into `titan-bot/tests/` and deleted it in the same command. Verified gone.

## 1e. System prompts, sha256, read out of the loaded bytecode after the restart

`_ENTRY_SYSTEM 30c979595a4831aa` · `_LEARNING_SYSTEM 191cf5d71ebf3865` · `_CLOSE_SYSTEM 7d7707cfa2d336f7` · `_CLOSE_SYSTEM_RICH 3d709571e17ff405`. **Identical** to the 2026-09-21 pins. `claude_advisor.py` itself is unchanged (`e88d7fe634973e90`).

## 1c. How often the old line misled (all 3,108 stored entry consultations)

"Misleading" = a tier the prompt calls agreeing with the proposed direction was **not** counted that way by the gate.

| era | consultations | misleading | share | printed ALL THREE | … gate counted < 3 |
|---|---|---|---|---|---|
| **current `Agreement:` form** (07-29 → now) | 341 | **119** | **34.9 %** | 61 | **53 (86.9 %)** |
| older form ("The 3 timeframes are aligned", every prompt) | 2,767 | **2,453** | **88.7 %** | 2,767 | 2,453 |

**Current-form breakdown:**
- By status: ai_skipped 91, executed 19, virt_cap_blocked 6, failed 3.
- Tiers claimed but not counted: 5m ×65, 15m ×38, 1H ×30.
- **Executed and misleading: 19 of 28 (67.9 %)**: vpos 85, 87, 88, 89, 90, 91, 93, 94, 96, 98, 99, 101, 104, 105, 106, 107, 108, 111, 112. That is 18 of the 27 live positions (vpos 85 is paper).
- **Reasons citing the agreement** (hand-read, all 65 misleading executes across both eras): **36 cite it**, 16 of 19 current-form and 20 of 46 older.
  - The brief's broad regex hits 59, but its precision is only 61 %; its false hits are OHLCV "MTF 4/4 alignment" sentences, not tier claims.

---

# 2. WHAT CODE ALREADY KNOWS: NEWS-FLIPPED ENTRIES (read-only)

**Bonferroni, declared first.** 2 samples (live actual; paper as the independent sample) × 3 outcomes (mean R, median MFE, share never +0.25R) = **6 tests, α = 0.0083**. **No test clears it. The best p is 0.027.** Cells with n < 8 are described, not ranked.

**Population:** 79 closed entries, LIVE 27 (vpos 86–112) and PAPER 52 (vpos 34–85). Excluded: vpos 33 (no risk value) and 27–32 (archived pre-geometry).

**Raw score:** Σ category `contribution` whose `net_direction` equals the traded side, rebuilt from `matrix_breakdown_json`. It reproduces vpos 112 at 2.5.
**Adjustment:** `macro_gate_penalty`, non-NULL on all 79.
**Bar history** from config commits:
- 5.0 until 05-20;
- 2.0 from `645a211` (05-20 21:05);
- FLAT 5.0 enforced from `db71454` (07-06);
- TREND 3.0 from `dee6cee` (07-30 21:26);
- FLAT 3.0 from `a7e7b46` to `6fa5d45` (08-21 → 09-09).

**Validation: 79 of 79 entries sit at or above their reconstructed bar.**

**"News-flipped"** = raw < bar ≤ raw + adj. A −1.0 adjustment hit 10 entries (paper 45, 59, 68, 72, 79, 80, 82; live 101, 104, 109); all still cleared the bar.

## 2a. Outcomes

| book | cell | n | ΣR | win | median MFE (R) | never +0.25R |
|---|---|---|---|---|---|---|
| **LIVE** | **news-flipped** | **6** | **−1.138** | 1/6 | 0.489 | 2/6 (33 %) |
| LIVE | rest | 21 | −0.717 | 7/21 | 0.427 | 10/21 (48 %) |
| PAPER | news-flipped, actual (2.0 bar era) | 1 (vpos 34) | −1.196 | 0/1 | 0.048 | 1/1 |
| PAPER | rest | 51 | −0.221 | 23/51 | 0.782 | 14/51 |
| PAPER | *counterfactual at today's 3.0 bar*: news-dependent | 9 | −5.841 | 1/9 | 0.214 | 5/9 |
| PAPER | *counterfactual*: raw ≥ 3.0 | 39 | +4.736 | 20/39 | 0.801 | 9/39 |

| live flip | side | date | raw | adj | news class | R |
|---|---|---|---|---|---|---|
| 88 | SHORT | 07-31 | 2.5 | +1 | CRITICAL_NEGATIVE | −0.296 |
| 90 | SHORT | 07-31 | 2.25 | +1 | CRITICAL_NEGATIVE | −0.304 |
| 91 | SHORT | 08-03 | 2.5 | +1 | CRITICAL_NEGATIVE | −0.484 |
| **94** | LONG | 08-17 | 2.25 | +1 | STRONG_POSITIVE | **+0.865 (trail)** |
| 96 | LONG | 08-24 | 2.5 | +1 | STRONG_POSITIVE | −0.546 |
| 112 | LONG | 09-22 | 2.5 | +1 | STRONG_POSITIVE | −0.373 |

**Tests:**
- **Live** flipped vs rest: mean R p **0.751**, MFE p 0.829, never-+0.25R p 0.662.
  - The flipped entries were if anything **greener**: median MFE 0.489 vs 0.427.
- **Paper counterfactual:** p 0.027 / 0.081 / 0.099. None clears α.

## 2b. Counted-tier count — 🔴 candidate 30 already died on this

**Candidate 30 (2026-09-16 17:30) died because the count IS the score (ρ = +0.92).** Here ρ(count, raw) = **+0.79 live, +0.85 paper**.

| book | counted | n | ΣR | win |
|---|---|---|---|---|
| LIVE | 1 | 6 | −1.138 | 1/6 |
| LIVE | 2 | 19 | +0.838 | 7/19 |
| LIVE | 3 | 2 | −1.555 | 0/2 |
| PAPER | 1 | 14 | −7.260 | 3/14 |
| PAPER | 2 | 29 | +2.933 | 13/29 |
| PAPER | 3 | 9 | +2.910 | 7/9 |

🔴 **On the live book the news-flipped set IS the count-1 set IS the raw < 3.0 set: {88, 90, 91, 94, 96, 112}, 6 = 6 = 6.**
- Under a 3.0 bar and ±1.0 news steps, one counted tier gives at most 2.5 and can pass only with news.
- Two counted tiers never need news.

**So the "new question" is not new on live: it is candidate 30's variable.** The only comparison that holds the score fixed is paper raw < 3.0, news vs no news: 9 against 4, Δ −0.57R, p 0.18. **Unrankable.**

## 2c. The five controls

1. **Bonferroni (6 tests, α 0.0083): FAILS.** Best p 0.027.
2. **Chronological halves: FAILS on live, and the sign REVERSES.**
   - H1 (07-30 → 08-27): flipped −0.765R over 5 vs rest −2.530R over 8, so flipped did *better*.
   - H2: flipped −0.374 over 1 vs rest +1.813 over 13.
3. **Regime split: FAILS, the FLAT leg is EMPTY.** All 6 live flips are TREND.
4. **Paper as the independent sample:** only **1** actual paper flip, because the old 2.0 bar made flips rare. The 3.0-bar counterfactual (n 9, 1/9 wins) points the same way, but all 9 are count-1 with raw 2.25–2.5. It is the score again.
5. **Confound, era and side: BOTH.**
   - **Side is fixed by the news sign by construction:** CRITICAL_NEGATIVE only lifts SHORTs, STRONG_POSITIVE only LONGs. The 3 live SHORT flips are all 07-31 → 08-03, one headline cluster in the 4 days after the 07-30 bar raise. The 3 LONG flips are 08-17 → 09-22.
   - 🔴 **Clock test, SOL-analog.** All 670 candidates that reached the score gate since 07-30 (deduped per side per 5 min) were compared on forward BingX 1h drift in the trade direction, news-admitted vs raw-admitted:
     - raw: **+0.285 % / +0.308 % / +0.323 %** at 4h / 12h / 24h;
     - **day-matched: +0.025 (p 0.79) / −0.100 (p 0.51) / −0.023 (p 0.89)**.
   - The non-zero-news rate runs **7 % → 100 % by UTC hour**. It is 0 % on 11 days and 100 % on 10.
   - **Titan's news term behaves exactly like SOL's on 2026-08-10: a CLOCK, not a per-signal fact.**

## 2d. Every winner a "no news-flip over the bar" rule would refuse

- **LIVE: vpos 94, LONG, +0.865R, 2026-08-17, trail.** One of only 3 live trail wins; the 5th-best live close of 27.
- **PAPER (3.0-bar counterfactual): vpos 81, SHORT, +0.770R, 2026-07-24, trail.** (The one actual paper flip, vpos 34, lost.)

> ### 🔴 §2 VERDICT: THE RULE DOES NOT SURVIVE. NO GATE DIFF.
> It fails Bonferroni, the halves (the sign reverses), the regime split (empty leg) and the clock test. On live it is the score. It refuses a material winner on each book. **The one thing the data says, weakly, is that raw 2.25–2.5 entries lose on paper (1/9). That is a SCORE statement, and the 07-30 bar raise already acted on the score.**

---

# 3. HOW OFTEN DOES THE ENTRY ADVISOR MISREAD? (read-only)

## 3a. Tier-agreement claims checked against each row's own prompt

**Rules** (deterministic; full rule text in the working file):
- A claim clause contains `agree|align|confluen` and names a tier or "3TF/all three". OHLCV-alignment and disagreement clauses are excluded.
- Each asserted tier is checked against the prompt's own tier line:
  - counted in the proposed direction → **CORRECT**;
  - "NOT counted" with the slot agreeing → **HALF-READ** (the vpos 112 shape);
  - opposite / absent / withheld → **FALSE**.
- A tier the reason itself calls neutral / expired / not counted → CORRECT.

**Validation:** vpos 112 classifies HALF-READ ✅.
**Hand audits:**
- 44/46 in-sample (46/46 on misread-vs-not);
- **39/40 out-of-sample (40/40 on misread-vs-not)**.
- The rules under-count claims (recall ≈ 75 %) and never flipped a misread verdict.

| era | group | rows | making a claim | CORRECT | HALF-READ | FALSE |
|---|---|---|---|---|---|---|
| **current (07-29 →)** | all | 341 | 51 | 33 | **17** | 1 |
| current | **executed** | 28 | 23 | 9 | **13** | 1 |
| current | ai_skipped | 298 | 17 | **17** | 0 | 0 |
| older (judged vs the GATE) | all | 2,767 | 63 | 19 | 34 | 10 |

> ### **MISREAD RATE: 18 of 51 = 35.3 % of claim-making consultations; 14 of 23 = 60.9 % of claim-making EXECUTES.**
> 🔴 **One-sided. All 17 half-reads are `execute` votes** (13 executed, 2 cap-blocked, 2 order-failed). **All 17 claim-making skips read it correctly.** The misread appears when the model argues FOR entry. It argues in the direction the old Agreement line handed it.
> The older era's 69.8 % "misread vs the gate" is **the prompt's error, not the model's**: that prompt said all three were aligned on every row.

Verbatim half-reads: 32533 *"1H+15m+5m agree LONG"* (15m not counted) · 34283 *"1h+15m+5m signals agree LONG"* · 22063 *"3TF SHORT agreement (1H/15m/5m)"* (5m not counted) · 34546 (vpos 112) *"15m+5m BULL confluence"*.
Correct readings exist: 33554 *"1H+5m LONG confluence, … 15m signal expired"* · 34280 *"15m neutral nets safely to 1H+5m agreement"*.

## 3b. Does a misread predict the outcome? (executes that became positions; R = net / initial risk)

| book | group | n | ΣR | mean R | win | rank? |
|---|---|---|---|---|---|---|
| LIVE | **misread** | 13 | **+3.237** | +0.249 | 5/13 | n ≥ 8 |
| LIVE | **correct** | 9 | **−3.347** | −0.372 | 2/9 | n ≥ 8 |
| LIVE | no claim | 5 | −1.745 | | 1/5 | **UNRANKABLE** |
| PAPER | misread | 11 | −3.222 | −0.293 | 4/11 | n ≥ 8 |
| PAPER | correct | 4 | +3.612 | | 4/4 | **UNRANKABLE** |
| PAPER | no claim | 37 | −1.807 | −0.049 | 15/37 | n ≥ 8 |

**A misread does NOT predict a loss.**
- On live it points the *opposite* way, carried by vpos 111 (+2.82R) and 89 (+1.39R); without them the misread group is −0.97R over 11.
- The two books disagree.

**This is a TEXT defect**: the reason overstated what the gate counted. It is not an outcome signal. That is why the fix is to stop the prompt lying, and **not** to move a decision into code on the strength of a misread.

## 3c. Does the entry advisor add value on Titan at all? Its refusals replayed

**Method: Titan's live contract on BingX 5m, validated before trusting.**
- **Contract:**
  - SL = 2.25 × the row's `srv_atr_1h`; this matches live 1R within a median 1.3 %.
  - Arm at +1R, then the stop goes to breakeven entry × (1 ± 0.002).
  - Trail 0.75R from the water mark, tightening only.
  - Taker 0.0005 on both legs.
  - bardir order within each bar.
  - One position per side.
  - Entry at the open of the signal's 5m bar; on executed positions this lands within a median 1.84 bps of the real fill.
- **Candles:**
  - BingX serves 5m history only back to 2026-08-12, so 5m bars were built from BingX 1m.
  - 192,531 bars, 0 gaps.
  - Where native 5m exists, 12,993 of 12,994 bars match exactly.
- **Validation on live sl/trail closes:** **7 of 8 within 0.1R**, median error 0.024R.
  - It **reproduces every published canon counterfactual exactly** (vpos 101, 104, 105, 106, 108, 109, 112).
  - Paper-era closes do not reproduce (22 of 41), because paper ran under older exit mechanics. So every book below is replayed under ONE contract rather than compared to realised paper R.
- **Population:** 2,863 `ai_skipped` refusals.
  - **540 excluded**, because a real position on that side was open and the cap would have blocked them anyway.
  - **2,148 skipped** under one position per side.
  - **175 replayed: 173 resolved, 2 unresolved**. The unresolved two are live-era, marked to market at −0.148R and kept out of every total.

| book (all replayed by the same simulator) | n | ΣR | mean R |
|---|---|---|---|
| **REFUSED**, one per side | **173** | **−13.37** | −0.077 |
| … live era (since 07-29 20:05) | 45 | **−9.02** | −0.200 |
| … paper era | 128 | −4.35 | |
| … live LONG / live SHORT | 17 / 28 | +1.44 / −10.46 | |
| … paper LONG / paper SHORT | 59 / 69 | −11.18 / +6.83 | |
| … first half / second half | 86 / 87 | −8.94 / −4.43 | |
| executed, one per side | 67 | −6.13 | |
| executed, each on its own | 87 | +9.27 | |
| **ADVISOR ON** (its execute verdicts, serial) | **74** | **−0.81** | −0.011 |
| **ADVISOR OFF** (every consultation traded, serial) | **197** | **−21.50** | −0.109 |
| ON vs OFF, live era | 23 vs 60 | −1.20 vs −9.06 | |

> ### 🔴 §3c VERDICT: **ITS REFUSALS SAVED R. The entry advisor earns its place on Titan.**
> **ON vs OFF = +20.7R over the record, +7.9R in the live era.** That is the least path-sensitive statement of its value.
> 🔴 **But the value is mostly ABSTENTION, not selection.**
> - Per trade, executed averaged +0.039R against refused −0.147R, but the day-clustered 95 % CI of that gap is **[−0.14, +0.48]**, P(diff > 0) = 0.89. **It crosses zero.**
> - Refusals are clustered: 1,931 fall on 107 days, which is why the bootstrap is clustered by day.
> - Not every refused slice loses: live LONG refusals (+1.44R, n 17) and paper SHORT refusals (+6.83R, n 69) would have made money.
> **Serial books are order-dependent.** The same executed set is −6.13R one-per-side and +9.27R each alone. Read the on/off comparison, not the serial totals.
> Same direction as SOL on 2026-09-11 (refusals saved 7.11R on 62).

🟡 **One live-vs-replay deviation, recorded and not investigated here.** On **vpos 111** the replay's trail fires at 09-21 08:40 (+1.84R), where the 5m low wicked to 83 493 on last price. The **live trail did not fire and exited at 10:29 for +2.82R**. Changing the trail width does not move it. The likely cause is live-check granularity or mark vs last price. **Unconfirmed.** It cost nothing, and it moves no number above materially. It is the one validation miss out of 8.

---

# 4. VERDICT

- **§1 — applied from flat.** The prompt no longer states agreement the gate did not count. The exit-side twin (`Agreement at entry:`) is recorded and left for your decision, because it moves the exit-advisor cohort.
- **§2 — "no news-flip over the bar" does NOT survive.** On live it is the score (candidate 30), and at signal level it is a clock (it vanishes on day-matching, as on SOL). It refuses vpos 94 and vpos 81. **No gate diff, nothing proposed.**
- **§3 — misread rate: 35.3 % of claim-making consultations, 60.9 % of claim-making executes**, one-sided toward execute and toward the old line's claim. A misread does not predict the outcome. **The entry advisor earns its place on Titan.** Its refusals replay to −13.37R (live era −9.02R), and on vs off is worth +20.7R (+7.9R live era). That value is mostly abstention: its per-trade selection edge is not significant (95 % CI [−0.14, +0.48]).
- **Nothing is proposed from one trade.**

---

# 5. APPLIED — FROM FLAT

| step | result |
|---|---|
| **flat, 16:54:09 and again 16:57:21 UTC** | DB 0 open rows, 0 `exit_pending`, 0 breakeven jobs. BingX unified and raw probes both 0 positions and 0 open orders; error list **empty**. |
| `.bak` | `signal_tiers.py.bak_agreementline_20260926` (`4af4fdba57cfaf84` = the `f53d048` file), `tests/test_entry_tiers_matrix_names_ages.py.bak_agreementline_20260926`, `OPEN-ITEMS.md.bak_agreementline_20260926` |
| AST | `signal_tiers.py` 15 → 17 top-level nodes: **`render` changed, `_join_labels` + `_gate_agreement` added, 0 removed, nothing else**. New sha256 `2870ccc423c9fc4c`. |
| commit | **`991b333`**: `signal_tiers.py` + the two contracts only |
| **restart** | `systemctl restart titan` at **16:57:26 UTC**. MainPID **4007821 → 912030**, worker **912101**, NRestarts 0. |
| boot line | `[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)` at 16:57:45. 0 tracebacks. |
| loaded bytecode (`config.pyc`, `claude_advisor.pyc`, headers match source) | SL_ATR_MULT **2.25** · TRAIL_MULT_ATR **1.6875** · EXIT_ADVISOR_DRYRUN **False** · BOOK_GATE_DRYRUN **False** · CLAUSE_A **True** / CLAUSE_B **False** · LIVE_TRADING_ENABLED **True** · ORDER_ADAPTER_LIVE **True** · LIVE_FIXED_MARGIN_USDT **30.0** · LEVERAGE **5** · CONFLUENCE bars 3.0 / 5.0 · AI_ADVISOR_HIDE_1H False. The four SYSTEM prompts are identical (see §1e). |
| ✅ **`signal_tiers` in-process: LIVE-PROVEN** | The module is imported **lazily** (`claude_advisor.py:567`, `main.py:2999`). At restart its `.pyc` was the old code with a header that did not match the new source. **The first post-restart entry consultation, trades 35682 at 17:00:09 UTC (`Within Bearish OB`, SHORT, advisor `skip` 0.78), rendered:** `Agreement: Counted by the gate: 2 of 3 tiers (15m SHORT, 5m SHORT); vs the proposed SHORT: 15m+5m agree. 1H points SHORT on its slot but the matrix had expired it on its category TTL and it was not counted.` The old line would have said all three agree. The `.pyc` was rewritten at **17:00:12**; its header matches the source and it contains `_gate_agreement`. |
| canon | header HEAD → `991b333`; the `991b333` entry; **`§0.AGREEMENT-LINE` with the COHORT BOUNDARY 2026-09-26 16:57:26 UTC** (never pool entry verdicts across it); the exit-side twin recorded. |
| `openitems_guard` | EXIT=0 before. EXIT=1 after the commit (stale header, as designed). **EXIT=0 after the canon update.** |

## Confirmations

- **Every write was stated before it ran:**
  - `.bak` ×3;
  - `signal_tiers.py`;
  - the new contract, with one harness line added after the first trace;
  - the updated 09-12 contract;
  - commit `991b333`;
  - the canon (as botuser);
  - the sandbox `/tmp/titan-contract-agreement` (no secrets, no DB);
  - one temp file in `tests/`, created and removed in the same command;
  - this report and one Telegram message.
- **`trades.db`:** only `mode=ro` + `query_only`, by me and by the three read-only forks. The contracts opened it **0** times.
- **Venue:** GET only. **0 orders placed, 0 cancelled.**
- **Exactly one restart:** titan, from flat. NRestarts 0.
- **Mercury-SOL untouched:** MainPID 222221, NRestarts 0, before and after. Not read, not opened.
- `EXIT_ADVISOR_DRYRUN` / `BOOK_GATE` flags untouched (read back from the loaded bytecode).
