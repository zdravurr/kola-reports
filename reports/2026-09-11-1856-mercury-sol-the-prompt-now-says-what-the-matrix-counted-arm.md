# mercury-sol-the-prompt-now-says-what-the-matrix-counted-arm-miss-is-one-trade

_2026-09-11 18:56 UTC_

---

# Mercury-SOL — the prompt now says what the matrix counted; the arm miss is one trade

**2026-09-11 · 🔴 LIVE REAL MONEY · §1 and §3 READ-ONLY · §2 APPLIED and RESTARTED FROM FLAT (18:26:51 UTC) · Titan untouched** · marker `REPORT-ID sol-matrixline-armmiss-20260911`

Guard pre-flight: `titan-bot/tools/openitems_guard.py` **EXIT = 0** (14 watched values agree with runtime). This pass acts on two defects from my 2026-09-11 17:14 report, §0 and §4c.

---

## WHAT YOU MAY WANT TO DECIDE

1. **Nothing is waiting on you to keep running.** The prompt line has been live since 18:26:59; ✅ LIVE-PROVEN at 19:40:06 UTC: the first consultation after the restart (trades.id 25817, open_long, decision skip) carried the line, and it agreed with that row's own stored matrix on 3 of 3 tiers (published 18:56, before it arrived; ADDENDUM at the end). Rollback is two `.bak_matrixline_20260911` files plus a restart from flat.
2. 🔶 **I changed `main.py` by ONE keyword argument, which the brief did not foresee.**
   - You said the data is in `matrix_breakdown_json`. It holds points and flags only: no signal names and no ages.
   - Names and ages exist only in `matrix_result['active_signals']` at the call site. So the call now passes `matrix_result=matrix_result`.
   - The AST proof shows this is the only change in `main.py` (§2c). If you want it gone, the rollback above removes it.
3. **Defect B is one trade in 38.** It is worth **+1.110R / +$2.13 live, and 0 on paper**. §3e prices three remedies and proposes none; whether to build any is your call.

## VERDICT

- **Defect A is not rare: it is half the book.** Of **4,598** entry consultations, **2,265 (49.3%)** showed the advisor a directional tier whose matrix category had been **zeroed by intra-conflict**. It happened on **92 of 92 days**.
  - **1,453 (31.6%)** showed the zeroed tier **agreeing** with the proposed side, which inflates confluence.
  - **1,090 (23.7%)** showed it **opposing** the proposed side, which deflates it.
  - It is **not one-sided**. The 5m trigger inflates (904 agree vs 7 oppose). The 15m and 1H tiers mostly deflate (15m: 592 vs 1,001; 1H-trend: 18 vs 70).
  - The reverse, where the matrix scores a tier the prompt shows as neutral, happened **55** times.
- **It reached real money.** Of 16 live entries, **11** carried a zeroed tier shown agreeing. In **9 of those 11** the stored reason builds on LuxAlgo tier agreement (e.g. "3/3 tier agreement", "3-way LuxAlgo confluence"). 2 are ambiguous (manual read of every one, §1d).
- **It is not an outcome lever, and nothing here says it is.** Those 11 live entries made ΣR **+7.733**; the 5 without a zeroed tier made **−0.979**. That is n = 11 against n = 5, so it is **not ranked**. §2 was applied because the prompt promised something the numbers did not support, not because it pays.
- **§2 is applied.** One fact line now sits directly under the AS-COUNTED tally. It says, per tier, what the score gate did with that tier's category; when a category was zeroed, it names each side's signal with its age against the window.
  - There is no instruction, no threshold, and no change to anything computed.
  - AST-proven, system prompts byte-identical, contract 7/7, restarted from flat, loaded bytecode verified. ✅ LIVE-PROVEN at 19:40:06 UTC: the first consultation after the restart (trades.id 25817, open_long, decision skip) carried the line, and it agreed with that row's own stored matrix on 3 of 3 tiers (published 18:56, before it arrived; ADDENDUM at the end).
- **Defect B happened once.** Across **38** closed positions, reconstructed from Bybit 1m candles, the venue printed through the arm while the poller's water mark never reached it **exactly once: vpos 44**. Had it armed at that print, the lock would have closed the trade at breakeven: **−1.110R → +0.000R, +$2.1307**.
  - Paper: **0**. Near misses where no candle crossed: 3 (vpos 18, 19, 42).
  - The poller ticks every **12.5 s** (median; p95 13.7 s, max 243.5 s), not the configured 10 s.
- **Titan has the same structural gap** (it arms on sampled `last`, never on extremes) at a tighter **10.5 s** cadence and a wider **1R** arm. It is not quantified on its book, and it is untouched.

---

## 0. WHAT THE CUT-OFF SESSION LEFT BEHIND — established before any new work

The cut-off session was `9d1123f8`. It received this same brief at 17:28:42, made its first tool call at 17:30:16, and stopped at **17:40:17**: *"You've hit your session limit · resets 6pm (UTC)"*. Its transcript was read end to end: **31 tool calls, zero Edit, zero Write, zero `systemctl`**. Every write it made went to its own scratchpad.

| | question | finding |
|---|---|---|
| a | Did any SOL file change since 17:14? | **No `.py`, no config, no `.env`.** Files newer than 17:14 in the tree: `trades.db` (the live bot's own writes), `oi_cache.json` (the bot's OI cache, 18:00:18), `optimizer/tg_offset.txt` (the listener's offset, 18:03:26). Its 42-file hash baseline taken at 17:30 was re-checked: **41 of 42 identical**, and the one that moved is `oi_cache.json`. **`claude_advisor.py` was NOT modified by that session.** Its mtime was 2026-09-10 23:02:19 (the regime-line pass) until this pass patched it at 18:24:18. No prompt builder was touched. |
| b | A `.bak` from that session? | **None.** No `.bak*` in the SOL tree has an mtime after 17:14. |
| c | `NRestarts` / MainPID | mercury-sol: MainPID **1181897** since 05:40:08, NRestarts **0**. titan: MainPID **961100** since 2026-09-10 14:36:20, NRestarts **0**. **Neither was restarted by that session.** |
| d | Partial report, scratch output, held gate patch? | **No report.** The last kola-reports commit before this pass is `9f3eefd`, my 17:14 report. **No held commit-gate patch.** The newest file in `.kola_state/commit_gate_held/` is `20260911T061118Z.patch.APPLIED_91d1668`, from 06:11; the last line of `commit_gate_pass.log` is 06:12:02. **Scratch output exists**, all under `/tmp/claude-0/-root/9d1123f8…/scratchpad/p2/`: `a1.py` + `a1_out.txt` (a §1 measurement), `za.json`, `cite_sample.json`, hash/service baselines, `windows.txt`, and **38 complete 1m kline files** `k1/v7…v44.csv` (every one `bars == expected` in `k1fetch.log`). |
| e | Runtime flags / Titan | `FLAT_ADX_GATE_DRYRUN = True` (config.py:407) and `BOOK_GATE_DRYRUN = False` (config.py:475), **confirmed as loaded** (method in CONTROLS: the running process's `config` bytecode was compiled from exactly these bytes). Titan `git status -- titan-bot` **clean**, HEAD **`cd0f175`**. |
| f | A prompt edit already on disk? | **No.** Nothing to verify or skip; §2 was applied fresh by this pass. |

**What the cut-off session HAD done:**
- measured §1 with a method this pass corrects: it mapped the 1H tier to TREND unconditionally;
- fetched the 1m candles §3 needs;
- timed Tor GETs;
- read Titan's breakeven worker.

**What it had NOT done:**
- the 1H re-arm correction;
- the §3 reconstruction and money;
- the citation read;
- any edit, restart, report or Telegram message.

Its §1 headline (2,260 / 4,595) and this pass's (2,265 / 4,598) differ by the corrected mapping and by three consultations that arrived after it stopped. The kline files were re-used only after an integrity check: **vpos 44's window re-fetched from Bybit at 18:19 UTC is byte-identical in OHLC** (67 bars).

---

## 1. DEFECT A — MEASURED (read-only)

### 1a. The two code paths, verbatim, and why they disagree

**The matrix: every signal inside its category window counts, per signal TYPE.**
```
signal_matrix.py:204-231  record_signal(): one row per (symbol, canonical_id) in live_context_state, last_seen bumped
signal_matrix.py:234-236
def _ttl_for(category):
    minutes = CATEGORY_TTL_MINUTES.get(category, 30)
    return timedelta(minutes=minutes)
signal_matrix.py:259-261   (inside get_active_signals)
        age = now - last
        if age > _ttl_for(cat):
            continue
signal_matrix.py:284-293   (compute_score)
    for sig in active:
        cat = sig['category']
        ...
        contribution = sig['intensity_weight'] * CATEGORY_MAX_POINTS
        if sig['direction'] == LONG:
            by_cat[cat]['long_points'] += contribution
        elif sig['direction'] == SHORT:
            by_cat[cat]['short_points'] += contribution
signal_matrix.py:297-301
        lp = min(data['long_points'],  CATEGORY_MAX_POINTS)
        sp = min(data['short_points'], CATEGORY_MAX_POINTS)
        intra_conflict = lp > 0 and sp > 0
        if intra_conflict:
            net_dir, contribution = NEUTRAL, 0.0
config.py:724-729   CATEGORY_TTL_MINUTES = {'TREND': 360, 'MOMENTUM': 90, 'LIQUIDITY': 30, 'EXECUTION': 5}
```

**The slot state machine: the LATEST write per slot, and that is what the advisor is shown.**
```
state_machine.py:217-233   update_slot(): overwrites direction / signal_name / timestamp — one value per slot
            market_state[slot]['direction'] = direction
            market_state[slot]['signal_name'] = signal_name
            market_state[slot]['timestamp'] = now_iso
state_machine.py:289-304   set_1h_trend(): overwrites the 1h_context; clears 15m/5m only on a direction FLIP
state_machine.py:35-55     1h_context ttl_hours=None (never expires) · 15m_confirm ttl_hours=4 · 5m_trigger consumed each fire
main.py:4364               combo, _sm_snap = state_machine.set_trigger_and_snapshot(...)
main.py:4370               matrix_result    = signal_matrix.compute_score(symbol)
claude_advisor.py:548-551  (pre-change numbering)
    _snap = sm_snapshot or {}
    _h1  = _snap.get('1h_context') or {}
    _m15 = _snap.get('15m_confirm') or {}
    _m5  = _snap.get('5m_trigger') or {}
claude_advisor.py:797-807  _tier_verdict(): AGREES iff the SLOT's direction == the proposed side
claude_advisor.py:815-822  the AS-COUNTED tally increments on that slot verdict
```

**Why they can disagree — four mechanisms, measured separately in 1b and 1e:**
1. **Multiplicity (the vpos 44 shape).** The matrix keeps every signal TYPE whose `last_seen` is inside the window. An older opposite-side type that has not expired zeroes the category, but the slot has been overwritten by the newer signal and cannot show it. On vpos 44, Trend Catcher Up (349.8 / 360 min) sat beside Trend Catcher Down (49.9), and HyperWave Up (80.0 / 90) beside HyperWave Down (49.8). The slots showed only the Downs.
2. **Different clocks.** The 1H slot never expires, while TREND expires at 360 min. The 15m slot lasts 4 h, while MOMENTUM lasts 90 min. So the slot can show a direction while the matrix holds nothing in that category. The 2026-08-05 STALE marker and the 2026-09-03 age-against-window clause already label this.
3. **Routing.** The 1H slot can be written by a re-armed 15m signal (`15m-rearm: HyperWave …`), a MOMENTUM signal. That was **452 of 1,652** stored 1H lines. This pass judges each tier by the category of the **signal it shows**, not by its timeframe label. This is the one method change from the cut-off session's script.
4. **Reverse.** A 1H flip or Exit reset clears the 15m slot to `n/a` (`_clear_lower_tfs_locked`, state_machine.py:236-246) while a MOMENTUM signal is still inside its window. The matrix counts a direction the prompt shows as absent.

### 1b. How often — every consultation in the record

**n = 4,598** entry consultations with a stored prompt, 2026-06-08 00:40 → 2026-09-11 18:10, **92 days**. All 4,598 carry `matrix_breakdown_json` from the same request. `trade_signal_matrix` agrees with it on **93 of 93** rows where both exist. `PROPOSED ENTRY` matches `signal_type` on all 4,598.

| class (per consultation) | n | share of 4,598 |
|---|---|---|
| ≥ 1 shown directional tier **ZEROED by intra-conflict** | **2,265** | **49.3%** |
| … of which a zeroed tier is shown **AGREEING** with the proposed side (inflates) | **1,453** | 31.6% |
| … of which a zeroed tier is shown **OPPOSING** the proposed side (deflates) | 1,090 | 23.7% |
| LONG consultations affected | 1,074 of 2,120 | 50.7% |
| SHORT consultations affected | 1,191 of 2,478 | 48.1% |
| era: 1H hidden (to 2026-08-01 17:20) | 1,428 of 2,946 | 48.5% |
| era: 1H shown | 574 of 1,185 | 48.4% |
| era: age-against-window clause (from 2026-09-03 18:15) | 263 of 467 | 56.3% |
| zeroed shown tiers per affected consultation | 1: 1,798 · 2: 436 · 3: 31 | |

**Per tier × side** (tier-instances; the denominator is consultations where that tier was shown):

| tier | side | zeroed & shown AGREEING | zeroed & shown OPPOSING | tier shown | zeroed share |
|---|---|---|---|---|---|
| 1H (TREND signal) | LONG | 5 | 28 | 563 | 5.9% |
| 1H (TREND signal) | SHORT | 13 | 42 | 637 | 8.6% |
| 1H (15m-rearm, MOMENTUM) | LONG | 29 | 47 | 189 | 40.2% |
| 1H (15m-rearm, MOMENTUM) | SHORT | 66 | 29 | 263 | 36.1% |
| 15m | LONG | 281 | 473 | 2,120 | 35.6% |
| 15m | SHORT | 311 | 528 | 2,478 | 33.9% |
| 5m trigger | LONG | 452 | 5 | 2,120 | 21.6% |
| 5m trigger | SHORT | 452 | 2 | 2,478 | 18.3% |

**What the AS-COUNTED tally told the model on the 1,453 inflating consultations**, as (tiers shown agreeing, of which the matrix actually counted):
(1, 0): 212 · (2, 0): 139 · (2, 1): 868 · (3, 0): 8 · (3, 1): 130 · (3, 2): 96.
- vpos 44 is one of the **130** that read "3 agree" where the matrix counted one.
- **8** read "3 agree" where it counted **none** of the three.

Descriptive only (consultations cluster in bursts; the effective n is days): P(execute) was **57 of 1,453 = 3.92%** on inflating consultations and **40 of 2,333 = 1.71%** where no shown tier was zeroed. This is not tested and not causal.

### 1c. How many became ENTRIES — live and paper never pooled

**n = 38** closed positions, every one with a stored consultation. **Below n = 8 nothing is ranked.**

| book | class | n | ΣR | wins | Σ$ |
|---|---|---|---|---|---|
| **LIVE** | zeroed tier shown AGREEING | **11** | **+7.733** | 5 | +17.9640 |
| LIVE | zeroed tier shown OPPOSING only | 0 | — | — | — |
| LIVE | no zeroed tier shown | 5 | −0.979 | 2 | −2.3665 |
| **PAPER** | zeroed tier shown AGREEING | **13** | **+3.262** | 7 | +737.1770 |
| PAPER | zeroed tier shown OPPOSING only | 1 | −1.049 | 0 | −233.6063 |
| PAPER | no zeroed tier shown | 8 | −7.587 | 1 | −1632.0288 |

**LIVE entries with a zeroed tier shown agreeing — every one, named:**

| vpos | side | R | zeroed tier(s) shown agreeing | opposing signal inside the window (age / window) | reason builds on the tier? |
|---|---|---|---|---|---|
| 29 | LONG | +1.355 | 15m HyperWave Signal Up | not recorded (no `trade_signal_matrix` signal list) | **yes** — "fresh 15m/5m agree LONG" |
| 32 | SHORT | −0.180 | 15m HyperWave Signal Down | HyperWave Signal Up 45.2 / 90 | **yes** — "3/3 tier agreement" |
| 33 | LONG | −0.049 | 15m HyperWave Signal Up · 5m Bullish I-BOS | Bearish Divergence 15.0, HW OB Signal Down 15.0, Reversal Down 60.0 / 90 · Bearish Breaker 0.0 / 5 | **yes** — "3-way LuxAlgo confluence" |
| 34 | SHORT | −0.643 | 5m Bearish I-BOS | Bullish Breaker, Bullish OB Entered, Within Bullish OB, all 0.0 / 5 | **yes** — "15m/5m strong SHORT agreement (HyperWave+I-BOS)" |
| 35 | SHORT | −0.701 | 5m Bearish I-BOS | Bullish OB Entered 0.0 / 5 | ambiguous — "15m/5m fresh & strong" |
| 36 | SHORT | −0.757 | 15m HyperWave Signal Down | HyperWave Signal Up 49.9 / 90 | **yes** — "15m+5m fresh SHORT confluence" |
| 38 | LONG | +4.031 | 5m Bullish New Imbalance | Bearish Liquidity Grab 5.0 / 30 | **yes** — "3-way confluence (1H/15m/5m all LONG)" |
| 39 | LONG | +1.604 | 5m Bullish OB Created | Bearish Breaker, Within Bearish OB 0.0 / 5 | **yes** — "15m/5m confluence fresh & aligned" |
| 40 | LONG | +2.549 | 5m Bullish OB Created | Within Bearish OB 0.0 / 5 | **yes** — "fresh 15m/5m LONG agreement" |
| 41 | LONG | +1.633 | 1H 15m-rearm HyperWave Up · 15m HyperWave Up | HyperWave Signal Down 65.0 / 90 | ambiguous — "1d/4h/1h BULL confluence" is the OHLCV block |
| **44** | SHORT | **−1.110** | 1H Trend Catcher Down · 15m HyperWave Signal Down | **Trend Catcher Up 349.8 / 360 · HyperWave Signal Up 80.0 / 90** | **yes** — "3-tier SHORT confluence (1H/15m/5m all bearish)" |

**PAPER entries with a zeroed tier shown agreeing (13):**
- vpos 7 +2.089, 8 −0.739, 9 −0.264, 11 +1.133, 13 +1.337, 15 +0.140, 19 +0.463;
- vpos 21 +0.285, 23 −0.577, 24 −1.050, 25 +1.257, 27 −0.660, 28 −0.153.
- The per-entry detail is in APPENDIX B.

**Effective n:** 11 live entries on 11 different days; 13 paper entries. Handfuls. The descriptive answer is the table above. None of these cells is compared with another as evidence of an effect, and the live contrast (11 vs 5) is below the ranking floor on one side.

### 1d. Does the stored reason build on the tier it was shown?

The rubric was applied to every tier-instance where a zeroed tier was shown agreeing. It checks, in order:
1. the reason names the shown signal;
2. it uses LuxAlgo / confluence / tier wording;
3. it names that timeframe with that direction **and** the prompt's OHLCV trend for that timeframe disagrees (so it can only mean the LuxAlgo tier);
4. otherwise the same timeframe + direction while OHLCV agrees counts as **ambiguous**.

| decision | n | shown signal named | LuxAlgo/tier wording | TF+dir, OHLCV disagrees | ambiguous | no mention |
|---|---|---|---|---|---|---|
| execute | 77 | 1 | 52 | 0 | 4 | 20 |
| skip | 1,532 | 3 | 555 | 76 | 15 | 883 |

**The rubric was checked by hand.**
- On **30 execute instances drawn at random** (seed 20260911), a manual read found **14 clearly build on tier agreement, 3 ambiguous, 13 do not**.
- The rubric flagged 19 of those 30, and 14 of the 19 are confirmed: **precision 74%**. The false positives are OHLCV phrases like "4H/1H/15m/5m all BEAR".
- The rubric's "no mention" had no false negatives in the sample.

**Every inflating ENTRY was read by hand (24):**
- **14 build their case on tier agreement, 6 ambiguous, 4 do not.**
- **Live: 9 of 11 yes, 2 ambiguous, 0 no.** Paper: 5 yes, 4 ambiguous, 4 no.

The live-era prompts carry the explicit "Tier agreement … AS COUNTED: 3 agree" block, and the model repeats it: "3/3 tier agreement", "3-way LuxAlgo confluence". Per the 2026-08-08 canon, `reason` is narration, not mechanism: this shows **what the model says it relied on**, not what moved the verdict.

### 1e. One-sided? Both directions

- **Zeroed tier shown directional — both signs occur.** Inflating 1,453 consultations, deflating 1,090. By tier the sign flips:
  - the **5m trigger inflates** (904 agree / 7 oppose), because it is the fresh signal that just fired and the opposing one is an older or simultaneous 5m print;
  - **15m** (592 / 1,001) and **1H-trend** (18 / 70) mostly **deflate**.
- **Reverse — the matrix scores a direction on a tier the slot shows as neutral / `n/a`:** **55** consultations, all on the 15m tier, `15m: n/a` while MOMENTUM had a net direction. That is 17 days and 2 entries. A further 34 show the 15m as neutral while MOMENTUM was itself intra-conflicted.
- **Other disagreement classes, for completeness** (the slot shows a direction, the matrix differs, but not by zeroing):
  - **EMPTY**, where the matrix has nothing in that category's window: 1H-trend 684, 1H-rearm 48, 15m 597, 5m 2. This is mechanism 2, already labelled by the STALE marker and the age clause.
  - **OPPOSITE**, where only the other side is in the window: 1H-rearm 77, 1H-trend 5, 15m 1.
  - The new line renders all of these as facts too.

### 1f. Effective n

2,265 consultations; **92 distinct days**; **893** distinct (tier, signal, day) episodes. Entries: **25** carried a zeroed tier (11 live, 14 paper), and **24** a zeroed tier shown agreeing (11 live, 13 paper). This is a mechanical defect measured on the whole population, not a sample-size question. The entry counts are handfuls and are given descriptively.

**§2f test:** the brief said do not apply if this happens about twice in the record. It happened on **every one of 92 days**, in **49.3%** of consultations. **Applied.**

---

## 2. THE FIX — ONE PROMPT LINE, APPLIED FROM FLAT

### 2a/2b. What the advisor now sees, directly under the AS-COUNTED tally

It is one line, facts only:
- For each tier shown: the category the gate judged it in, and whether that category was **counted** (with its points), **ZEROED** (with every signal on each side inside the window and its age against the window), zeroed as a minority, or **empty**.
- There is no instruction, no "therefore", no threshold, and no lean.
- The tally above it is unchanged: it still counts the slots. The new line re-counts nothing.
- Absent or malformed input renders **nothing**, so the prompt is then byte-identical to the old builder.

### 2d. vpos 44's own stored prompt, before and after — verbatim

```
===== BEFORE (trades.id 25731 ai_user_prompt, verbatim) — tier block =====
Tier agreement vs SHORT (computed for this consultation):
  1H: Trend Catcher Down -> SHORT = AGREES
  15m: HyperWave Signal Down -> SHORT = AGREES
  5m trigger: Bearish OB Entered -> SHORT = AGREES
  Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 3 agree, 0 oppose, 0 neutral, 0 absent.
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.

===== AFTER — tier block =====
Tier agreement vs SHORT (computed for this consultation):
  1H: Trend Catcher Down -> SHORT = AGREES
  15m: HyperWave Signal Down -> SHORT = AGREES
  5m trigger: Bearish OB Entered -> SHORT = AGREES
  Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 3 agree, 0 oppose, 0 neutral, 0 absent.
  Score matrix, as the score gate counted these tiers (it counts every signal still inside its category window, not only the latest per slot): 1H → TREND 0, ZEROED: LONG and SHORT both inside its 360-min window (LONG: Trend Catcher Up 350 of 360 min; SHORT: Trend Catcher Down 50 of 360 min) | 15m → MOMENTUM 0, ZEROED: LONG and SHORT both inside its 90-min window (LONG: HyperWave Signal Up 80 of 90 min; SHORT: HyperWave Signal Down 50 of 90 min) | 5m trigger → EXECUTION SHORT +2.00, counted
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.

===== unified diff, whole prompt =====
--- before
+++ after
@@ -31,2 +31,3 @@
   Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 3 agree, 0 oppose, 0 neutral, 0 absent.
+  Score matrix, as the score gate counted these tiers (it counts every signal still inside its category window, not only the latest per slot): 1H → TREND 0, ZEROED: LONG and SHORT both inside its 360-min window (LONG: Trend Catcher Up 350 of 360 min; SHORT: Trend Catcher Down 50 of 360 min) | 15m → MOMENTUM 0, ZEROED: LONG and SHORT both inside its 90-min window (LONG: HyperWave Signal Up 80 of 90 min; SHORT: HyperWave Signal Down 50 of 90 min) | 5m trigger → EXECUTION SHORT +2.00, counted
 The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
```

### 2c. Only the prompt builder changed — AST proof

The proof strips exactly the change from the new file's AST, and requires the result to be `ast.dump`-identical to the backup.
- `claude_advisor.py`: the change is the new `_render_matrix_tier_line`, the trailing `matrix_result=None` parameter, the `_matrix_line = …` assignment, and the `+ _matrix_line` term.
- `main.py`: the change is the one `matrix_result=` keyword on the one `claude_advisor.consult_for_entry(...)` call, inside `_handle_5m_trigger`.
- **`signal_matrix.py`, `state_machine.py`, `config.py` and every gate: not touched** (hashes in CONTROLS).

```
== claude_advisor.py: sha 54e71f0285921d19 -> bff44d00fd0e0aa0
   top-level named nodes that differ BEFORE stripping: ['_render_matrix_tier_line', 'consult_for_entry']
   text diff: +84 lines, -1 lines; removed lines: ['-                      combo_weight=None, sm_snapshot=None):']
   after stripping ONLY the change: AST identical to backup = True
== main.py: sha a11a7cb372a0bf94 -> 91dfa43f251c6245
   top-level named nodes that differ BEFORE stripping: ['_handle_5m_trigger']
   text diff: +4 lines, -0 lines; removed lines: []
   after stripping ONLY the change: AST identical to backup = True
removed counts: {'helper': 1, 'param': 1, 'assign': 1, 'term': 1, 'kw': 1} (expected helper=1 param=1 assign=1 term=1 kw=1)
   bak: system-prompt assignments found 6/6
   new: system-prompt assignments found 6/6
   system-prompt AST nodes identical bak vs new: True
AST PROOF PASS
```

**Contract** `tests/test_entry_prompt_matrix_line.py`: new, run with bytecode writing off, `_call` stubbed, no DB, no network.
```
  [1] matrix_result=None == pre-change builder, byte for byte (1774 chars)
  [2] rendered:   Score matrix, as the score gate counted these tiers (it counts every signal still inside its category window, not only the latest per slot): 1H → TREND 0, ZEROED: LONG and SHORT both inside its 360-min window (LONG: Trend Catcher Up 350 of 360 min; SHORT: Trend Catcher Down 50 of 360 min) | 15m → MOMENTUM 0, ZEROED: LONG and SHORT both inside its 90-min window (LONG: HyperWave Signal Up 80 of 90 min; SHORT: HyperWave Signal Down 50 of 90 min) | 5m trigger → EXECUTION SHORT +2.00, counted
  [3] prompt minus the one line == matrix_result=None prompt
  [5] 15m-rearm 1H slot judged in MOMENTUM
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): TypeError: 'in <string>' requires string as left operand, not NoneType
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): AttributeError: 'NoneType' object has no attribute 'get'
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): TypeError: 'int' object is not iterable
[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): AttributeError: 'str' object has no attribute 'get'
  [6] malformed matrix_result: no exception, no line
OK — the matrix line is one fact line under the tally; nothing else in the prompt moved; 6 system prompts byte-identical
```
**The existing contract** `tests/test_entry_prompt_regime_line_is_legible.py`, re-run as a regression check:
```
OK — entry prompt regime line is legible; 6 system prompts byte-identical
```
**The system prompts are byte-identical by sha256.** Both contracts pin all six `_ENTRY_SYSTEM*` / `_CLOSE*` constants to the 2026-09-10 snapshot, and the AST proof shows their assignment nodes identical, backup against new.

**One limit, stated and not changed.**
- The 60-second state-verdict cache key is still the slot identities plus the nearest opposing wall.
- Inside one minute, a reused verdict can therefore come from a prompt whose matrix line differed. For example, an opposing signal may expire inside that minute.
- Provenance is kept: `user_prompt` names the prompt that produced the verdict, and `rendered_user_prompt` is this row's.
- Widening the key would change how often the model is called. That is not a prompt line, so it was left alone.

**Not edited:** `OPEN-ITEMS-SOL.md`. The 2026-09-10 regime-line pass set no precedent there, so the write surface was kept to the two files and the new test.

### 2e. Applied from flat, confirmed from the loaded bytecode

```
18:24:18   atomic patch: both .bak copies written and sha-verified FIRST, every old string found exactly once,
           new source ast.parse()d before os.replace — pre-patch check: virtual_positions open = 0, active_positions = 0
             claude_advisor.py  54e71f0285921d19 -> bff44d00fd0e0aa0   backup claude_advisor.py.bak_matrixline_20260911
             main.py            a11a7cb372a0bf94 -> 91dfa43f251c6245   backup main.py.bak_matrixline_20260911
18:26:27   pre-restart: open vpos 0 · active_positions 0 · last trades row 18:10:05 · no webhook in the last 16 min
           next alert boundary 18:30:00 — the ~22 s boot fits inside the quiet window
18:26:51   systemctl restart mercury-sol   (MainPID 1181897 -> 1341949, worker 1342064)
18:26:59   active · NRestarts 0
18:27:24   [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
           [BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False
           [VIRTUAL] poller started in pid 1342064 (interval=10s) · [VPOS-RECONCILE] no open positions at boot — clean
18:27:27   [HEARTBEAT] alive ticks=1 ... open=0 mode=LIVE
LOADED     __pycache__/claude_advisor.cpython-312.pyc compiled 18:27:04 — header source mtime 1789151058 size 84462
             == claude_advisor.py (sha bff44d00fd0e0aa0)  -> the running worker imported the patched builder
           __pycache__/main.cpython-312.pyc compiled 18:27:00 — header == main.py (sha 91dfa43f251c6245)
           __pycache__/config.cpython-312.pyc header == config.py (sha a308a130e4dde9f6, unchanged since 05:40:05)
```

**Live proof: the first real consultation after the restart.**
```
NOT YET SEEN ON A LIVE PROMPT at publication (18:56 UTC).
Between the restart (18:26:59) and publication the bot wrote these rows, and NONE reached the advisor:
  25810 2026-09-11 18:30:07 exit_unarmed_noop
  25811 2026-09-11 18:50:06 htf_blocked
  25812 2026-09-11 18:55:02 htf_blocked
A read-only waiter is still running (4 h, trades.db ?mode=ro): it takes the first post-restart consultation,
checks that its stored ai_user_prompt carries the line, and checks every tier claim on it against that
row's own stored matrix_breakdown_json. Its result will be APPENDED to THIS file, at this same URL.
→ DONE 19:40:06 — see ADDENDUM at the end: trades.id 25817 carried the line, 3 of 3 tier claims agree with its stored matrix.
What IS proven now: the running worker imported the patched builder (bytecode header == patched source,
§2e), and the builder renders the line on vpos 44's own stored inputs (§2d) and in the contract (§2c).
```

**Rollback:** `cp claude_advisor.py.bak_matrixline_20260911 claude_advisor.py && cp main.py.bak_matrixline_20260911 main.py`, then restart **from flat**.

---

## 3. DEFECT B — THE POLLER MISSED THE ARM (read-only)

### 3a. The poller's actual cadence, from stored tick timestamps

**The source.** `position_excursion_samples` is written on every tick for the first hour of a position: `EXCURSION_SAMPLE_SEC = 10`, and ticks are ≥ 11.7 s apart. So in that phase each stored `ts` **is** a tick. After the first hour the sampler throttles to 50 s, so ticks there are **not** in the record.
- Journal heartbeats give a second, independent reading, but journal retention starts only at 2026-09-09 22:05.
- **Configured:** `MONITOR_POLL_SECONDS = 10` (config.py:663). **Actual:** 10 s of sleep, plus the Tor ticker GET, plus processing.

| source | n | median | p95 | p99 | max | > 20 s | > 30 s |
|---|---|---|---|---|---|---|---|
| **LIVE era**, first hour of 15 live positions (vpos 30-44) | **4,074 gaps** | **12.50 s** | **13.70 s** | 16.20 s | **243.5 s** (vpos 30) | 10 | 6 |
| journal heartbeats (5-min windows, 2026-09-09 22:05 → 09-11 18:10) | 520 windows | mean tick 11.85 s | 12.71 s | — | 16.32 s | — | — |
| same, longest single gap per window | 520 | 12.5 s | 16.7 s | — | 63.4 s | — | — |

- Live gaps over 30 s: vpos 30 (243.5, 116.5), vpos 32 (75.9), vpos 42 (107.8, 35.0, 35.9).
- The live per-position medians run 12.0 to 13.0 s.

**vpos 44 around the wick** (stored ticks):
- 12:29:32.9 → 99.63
- 12:29:45.2 → 100.11
- 12:29:57.5 → 99.59
- **12:30:10.0 → 98.08**
- 12:30:24.4 → 98.36
- 12:30:37.1 → 98.69

The gaps were 12.3, 12.3, 12.5, 14.4 and 12.7 s. The venue's 12:30 1m candle, re-fetched and byte-identical: **O 99.59 · H 99.85 · L 97.76 · C 98.60**.

### 3b. Every closed position — did the venue print through the arm while the water mark did not?

**The arm rule, reproduced from code:**
- `trail_arm.py:1336-1360`: arm distance = `TRAIL_ARM_R × SL_BUFFER_ATR × atr`.
- `virtual_trader.py:2015-2019, 2120-2131`: the arm fires on `last` crossing the arm level.
- `TRAIL_ARM_R` was 1.0 before the 2026-08-14 19:52:53 restart and **0.75** after it.

**The reconstruction agrees with the stored `breakeven_applied` flag on 38 of 38 positions**, meaning `water_mark` reached the reconstructed arm exactly where the lock armed. The 1m candles are Bybit public klines (last-trade OHLC), one file per position, covering open − 5 min → close + 6 min.

**n = 38 closed positions (16 live, 22 paper). Misses: 1.**

| vpos | book | side | arm | poller best (water mark) | candle through the arm | poller short by | realised |
|---|---|---|---|---|---|---|---|
| **44** | **LIVE** | SHORT | **97.860** | **98.080** | **97.76 @ 12:30 (interior minute)**, 0.100 through | **0.220 = 0.115R** | **−1.110R, −$2.1305 (sl)** |

**Near misses** (no candle printed through, so no counterfactual):
- vpos 18 (paper): the candle stopped 0.087R short;
- vpos 19 (paper): 0.006R short;
- vpos 42 (**LIVE**): the candle low 97.29 against an arm of 97.278, **0.005R short**.

The per-position table is in APPENDIX C.

### 3c. The money

The counterfactual arms the lock at the first 1m candle whose extreme crossed the arm.
- **The lock:** stop moved to BE = fill × (1 − 0.0020) = 99.1014, trail active at the position's own `trail_pct`.
- **Order:** stops are checked from the next candle onward, adverse extreme before favourable, and a gap through the stop exits at the open.
- **Fees:** the position's own realised rate, 0.1000%.
- **Robust to the unknown in-candle order:** if the 12:30 high of 99.85 came after the low, the BE stop is hit inside 12:30 at the same 99.10.

| book | n | realised ΣR | realised Σ$ | counterfactual ΣR | counterfactual Σ$ | **difference** |
|---|---|---|---|---|---|---|
| **LIVE** | **1** (vpos 44) | −1.110 | −2.1305 | **+0.000** | **+0.0002** | **+1.110R, +$2.1307** |
| PAPER | 0 | — | — | — | — | 0 |

- **It is one trade.** It is also the single largest money item on vpos 44, as the 17:14 report said, and it stays one trade across the whole book.
- The BE target is a fee wash at the venue's real 0.100% (`trail_arm.py` note), which is why the counterfactual lands at +$0.0002 rather than a win.
- **Caveat:** the venue stop triggers on **MarkPrice** (`slTriggerBy: 'MarkPrice'`, main.py:2381, 6246). The candles and the arm are last-price, so a CPI wick in last may not be the same wick in mark.

### 3d. Titan — the same exposure? (read-only; not changed)

- **Arm:** `_breakeven_reached()` (titan virtual_trader.py:1791-1796) arms at **+1R** off the ORIGINAL stop, on `last`.
- **Poll:** `_poll_once()` (2793-2802) takes `exchange.fetch_ticker(symbol)['last']` once per poll, `POLL_INTERVAL_SECS = 10` (line 263), and sleeps after processing. The engine owns every position (`ROUTING_MIGRATED_TO_ADAPTER = True`), so `breakeven_worker`'s 5 s loop stands down.
- **Cadence, from its own excursion samples** (dense for 48 h on Titan): positions opened since 2026-08-07 give **12 positions, 4,050 first-hour gaps, median 10.50 s, p95 10.70 s, p99 12.40 s, max 20.8 s**. Over the whole live era since 2026-07-29 21:54:16 (19 positions): median 10.50, p95 11.50. The ~300 s gaps in older rows are the sampler's throttle, not ticks.
- **Verdict: the same structural gap exists.** Titan arms on sampled last-trade prices and never on the venue's extremes. Its cadence is tighter (10.5 s against SOL's 12.5 s; BingX direct against Bybit over Tor) and its arm is wider (1R against 0.75R).
- **Not quantified on Titan's book:** that would need BTC 1m candles per position, which this pass did not fetch. Titan: not touched.

### 3e. Remedies — named and priced, not built, none proposed

**Measured cost of the current path:**
- one public `fetch_ticker` over Tor per tick, plus one private position read per tick while a live position is open, so about 4.9 of each per minute;
- Tor GET latency measured at ~18:22 UTC: ticker 0.77-1.72 s, and **2 of 6 returned CloudFront 403** and needed a fresh circuit; 1m kline 1.01-2.73 s;
- journal since 2026-09-09 22:05 (≈ 44 h): **18 × 403, 419 SOCKS-retry mentions, 0 "poll ticker fetch failed"**. Retries absorb it today.

| remedy | API calls | latency | new failure modes |
|---|---|---|---|
| **1. Sample the venue's 1m high/low.** Read `kline 1m limit=2` each tick: the in-progress candle carries the running high/low since the minute opened, and its close is the last trade. | **0 extra** if it *replaces* the ticker (same public endpoint class, same Tor path); +1 per tick (≈ +4.9/min) if added. | kline GET 1.0-2.7 s against ticker 0.8-1.7 s, so the tick is ≈ 0.3-1 s slower. | (i) the candle holding the fill carries pre-fill extremes, so extremes must be clipped to after the fill; (ii) it arms on prints the poller never saw, so the BE stop can be placed after mark is already back through BE, and Bybit rejects or instantly triggers a stop on the wrong side of mark, which needs an explicit close-or-skip path; (iii) the arm fires more often, a behaviour change (the 0.75R arm was calibrated on a 5m-candle replay, config.py:216-221, itself extreme-based); (iv) last-price extremes against MarkPrice stops. |
| **2. A faster poll** (5 s or 3 s). | ≈ 2× (5 s) or 4× (3 s) Tor GETs for the ticker **and** the private position read: ≈ 10-20/min each. | Each GET is already 0.8-2.7 s over Tor, so about 3 s is the floor. | More 403s and SOCKS retries (already 18 and 419 in 44 h at 12 s), and more private-endpoint load. **It still samples**: a wick shorter than the interval is still missed. The vpos 44 low printed somewhere in 12:30:00-12:31:00, between ticks at :10, :24 and :37, and the tape is not in the record, so which cadence would have caught it is **unknowable**. |
| **3. Arm from the closed candle.** Once per minute, read the just-closed 1m candle and arm if its extreme crossed. | +1 public GET/min (≈ +1.0/min against ≈ 4.9 ticker/min). | Arms **up to ~60 s + one GET** after the print. On vpos 44 that is ≈ 12:31:0x with price ≈ 98.6, so BE at 99.10 is still valid. | Late arming: in a fast reversal BE may already be on the wrong side of mark (rejection or immediate trigger), plus minute-boundary and clock-skew handling and a second endpoint dependency. |
| *(not asked)* 4. A public WebSocket trade/ticker stream | 1 persistent connection, no polling | continuous | A new long-lived component over Tor: reconnects, silent-stall detection. Named only. |

**None is proposed.** The whole book holds **one** trade this would have changed. Every remedy except the WebSocket still leaves a residual sampling or latency gap, and remedies 1 and 3 change how often the arm fires, which is a strategy change hiding inside an execution fix.

---

## CONTROLS AND CONFIRMATION

- **n is stated before every result.** Nothing below n = 8 is ranked, and nothing in this report is ranked, so no Bonferroni family was needed. Paper and live are never pooled, and the two bots are never pooled.

| check | result |
|---|---|
| guard pre-flight | `openitems_guard.py` **EXIT = 0** |
| SOL DB | every measurement connection `file:…/trades.db?mode=ro`, **SELECT only**. §2 wrote **no** DB row; the bot writes its own. |
| config | **not imported by any measurement script.** It was imported only inside the §2 contract-test and render processes (they import `claude_advisor`), with bytecode writing disabled, `_call` stubbed, no DB, no network. |
| writes in SOL's tree | `claude_advisor.py`, `main.py` (patched); their two `.bak_matrixline_20260911` copies; `tests/test_entry_prompt_matrix_line.py` (new). The service rewrote `__pycache__` for the two patched modules at boot. Final re-check against the cut-off session's 42-file baseline and the tree:

```
FINAL CHECK 2026-09-11 18:56:16 UTC
== SOL: cut-off baseline (42 files, 17:30) — entries that differ now:
/mnt/volume_nyc1_1780480650620/mercury-sol/claude_advisor.py: FAILED
/mnt/volume_nyc1_1780480650620/mercury-sol/main.py: FAILED
/mnt/volume_nyc1_1780480650620/mercury-sol/oi_cache.json: FAILED
== SOL: files newer than 17:14 (excluding trades.db*, __pycache__):
   2026-09-11 18:10:11  /mnt/volume_nyc1_1780480650620/mercury-sol/oi_cache.json
   2026-09-11 18:24:18  /mnt/volume_nyc1_1780480650620/mercury-sol/claude_advisor.py
   2026-09-11 18:24:18  /mnt/volume_nyc1_1780480650620/mercury-sol/main.py
   2026-09-11 18:25:28  /mnt/volume_nyc1_1780480650620/mercury-sol/tests/test_entry_prompt_matrix_line.py
   2026-09-11 18:56:12  /mnt/volume_nyc1_1780480650620/mercury-sol/optimizer/tg_offset.txt
== SOL: __pycache__ rewritten since 17:14:
   2026-09-11 18:27:00  main.cpython-312.pyc
   2026-09-11 18:27:04  claude_advisor.cpython-312.pyc
== SOL flags (text) + config sha:
407:FLAT_ADX_GATE_DRYRUN  = True    # 🔴 DRYRUN since 2026
475:BOOK_GATE_DRYRUN    = False   # 🔴 ARMED. This gate RE
a308a130e4dde9f6
== untouched modules sha:
   signal_matrix.py   a075ce05137f03b4
   state_machine.py   9a0d314091b2e078
   config.py          a308a130e4dde9f6
   book_gate.py       efdfd156ebc48733
   virtual_trader.py  eeeff98ae5018c95
   trail_arm.py       511b0516e242b284
== book-gate review counter:
   mtime 2026-09-11 18:30:03.6
0fbcc185e326bf80
{"fired":{},"last_counts":{"LONG":[18,0],"SHORT":[16,0]},"last_run":"2026-09-1118:30:02","looks":{}}
2026-09-11T17:30:02Z [sol_book_gate_review] n=31/200 LONG 0/15 SHORT 0/16 ratio=n/a fired_ever=[] looks_done=[] new=[]
2026-09-11T18:00:03Z [sol_book_gate_review] n=31/200 LONG 0/15 SHORT 0/16 ratio=n/a fired_ever=[] looks_done=[] new=[]
2026-09-11T18:30:03Z [sol_book_gate_review] n=34/200 LONG 0/18 SHORT 0/16 ratio=n/a fired_ever=[] looks_done=[] new=[]
== services:
MainPID=1341949 NRestarts=0 ActiveState=active ActiveEnterTimestamp=Fri 2026-09-11 18:26:59 UTC 
MainPID=961100 NRestarts=0 ActiveState=active ActiveEnterTimestamp=Thu 2026-09-10 14:36:20 UTC 
== SOL open positions:
0
== Titan:
   git status -- titan-bot lines: 0  HEAD cd0f175
   /root/titan-bot/healthcheck_state.json: FAILED
   /root/titan-bot/oi_cache.json: FAILED
``` |
| orders | **none.** No authenticated venue call by this session. Network: Bybit public `/v5/market/kline` and `/v5/market/tickers` GETs over Tor. |
| **NRestarts** | **mercury-sol 0 → 0** (one manual restart from flat at 18:26:51: MainPID 1181897 → 1341949; a manual restart does not count). **titan 0 → 0**, MainPID **961100 unchanged**. |
| **`FLAT_ADX_GATE_DRYRUN`** | **True** — config.py:407, loaded (config bytecode == config.py bytes, sha `a308a130…`) |
| **`BOOK_GATE_DRYRUN`** | **False** — config.py:475, loaded (same proof) |
| book-gate review counter | Never written by this session. It is rewritten only by its own 30-minute cron; the state at the final check follows (the cron also writes `fired` / `last_counts` from the bot's own evaluations): `   mtime 2026-09-11 18:30:03.6 · 0fbcc185e326bf80 · {"fired":{},"last_counts":{"LONG":[18,0],"SHORT":[16,0]},"last_run":"2026-09-1118:30:02","looks":{}} · 2026-09-11T17:30:02Z [sol_book_gate_review] n=31/200 LONG 0/15 SHORT 0/16 ratio=n/a fired_ever=[] looks_done=[] new=[] · 2026-09-11T18:00:03Z [sol_book_gate_review] n=31/200 LONG 0/15 SHORT 0/16 ratio=n/a fired_ever=[] looks_done=[] new=[] · 2026-09-11T18:30:03Z [sol_book_gate_review] n=34/200 LONG 0/18 SHORT 0/16 ratio=n/a fired_ever=[] looks_done=[] new=[]` |
| Titan | `git status -- titan-bot` **clean**, HEAD **`cd0f175`**, MainPID 961100, NRestarts 0. Of its 48 baseline files only `healthcheck_state.json` (rewritten by its own `healthcheck.py`, 18:23) and `oi_cache.json` (by its own `market_context.py`, 18:20) moved: runtime state, not code. |

---

## APPENDIX A — the patch, inline

```diff
--- a/claude_advisor.py
+++ b/claude_advisor.py
@@ -465,10 +465,88 @@
     )
 
 
+# ── 🔴 2026-09-11 — DEFECT A: THE MATRIX AND THE PROMPT READ THE SAME SIGNALS DIFFERENTLY ──
+# The tiers this prompt shows come from the state-machine SLOTS, which keep only the LATEST
+# signal per slot. The score gate counts EVERY signal still inside its category window
+# (signal_matrix.get_active_signals / CATEGORY_TTL_MINUTES) and ZEROES a category that holds
+# both a LONG and a SHORT signal (intra_conflict, signal_matrix.py:299-301).
+# On vpos 44 (LIVE, -1.110R) the tally below said "3 agree"; the matrix had zeroed TREND
+# (Trend Catcher Up 349.8 of 360 min beside Trend Catcher Down) and MOMENTUM (HyperWave Up
+# 80.0 of 90 beside HyperWave Down) and scored ONE category. The model wrote "3-tier SHORT
+# confluence (1H/15m/5m all bearish)". Measured 2026-09-11 over every stored consultation:
+# 2,265 of 4,598 (49.3%) showed a directional tier whose matrix category was zeroed, on all
+# 92 days; 1,453 (31.6%) showed it AGREEING with the proposed side.
+#
+# WHAT THIS ADDS: ONE line of FACTS — for each tier shown, what the matrix did with that
+# tier's category at scoring time; when zeroed, the signals on each side inside the window,
+# each with its age against the window. Same discipline as §0.PROMPT-PAIRING (2026-08-31)
+# and the regime line (2026-09-10).
+# 🔴 WHAT IT DELIBERATELY DOES NOT ADD, and no later pass may add it here: no threshold, no
+# "therefore", no advice, and NO change to the AS-COUNTED tally it sits under. Nothing
+# computed changes — the score, every gate, the slots and the tally are untouched.
+# `matrix_result` is the dict signal_matrix.compute_score returned for THIS request.
+# Returns '' when it is absent or malformed, so the prompt then renders BYTE-IDENTICALLY to
+# the pre-2026-09-11 builder (tests/test_entry_prompt_matrix_line.py pins that).
+# Ages are as of scoring, a few seconds before this render — the instant the gate used.
+def _render_matrix_tier_line(shown, matrix_result):
+    """FACT LINE: how the score matrix counted the tiers in `shown` [(label, slot), ...]."""
+    if not matrix_result:
+        return ''
+    try:
+        import signal_matrix as _sm      # classify() only — a pure dictionary lookup, no DB
+        _bk = matrix_result.get('breakdown') or {}
+        _act = matrix_result.get('active_signals') or []
+        _tier_default = {'1H': 'TREND', '15m': 'MOMENTUM'}
+        _parts = []
+        for _lbl, _slot in shown:
+            # The 1H slot can hold a re-armed 15m signal ("15m-rearm: HyperWave ...", 452 of
+            # 1,652 stored 1H lines): judge a tier by the category of the signal it SHOWS.
+            _base = re.sub(r'^15m-rearm:\s*', '',
+                           str((_slot or {}).get('signal_name') or '')).strip()
+            _cat = _sm.classify(_base)[0] if _base else None
+            if _cat not in _bk:
+                _cat = _tier_default.get(_lbl)
+            if _cat not in _bk:
+                continue
+            _b = _bk[_cat]
+            _win = float(CATEGORY_TTL_MINUTES.get(_cat, 0) or 0)
+
+            def _side(_d, _cat=_cat, _win=_win):
+                _xs = sorted((a for a in _act
+                              if a.get('category') == _cat and a.get('direction') == _d),
+                             key=lambda a: float(a.get('age_minutes') or 0.0))
+                _t = ', '.join(f"{a.get('signal_name')} "
+                               f"{float(a.get('age_minutes') or 0.0):.0f} of {_win:.0f} min"
+                               for a in _xs[:3])
+                return _t + (f", +{len(_xs) - 3} more" if len(_xs) > 3 else '')
+
+            if _b.get('intra_conflict'):
+                _parts.append(f"{_lbl} → {_cat} 0, ZEROED: LONG and SHORT both inside its "
+                              f"{_win:.0f}-min window (LONG: {_side('LONG')}; "
+                              f"SHORT: {_side('SHORT')})")
+            elif _b.get('inter_conflict'):
+                _parts.append(f"{_lbl} → {_cat} {_b.get('net_direction')} 0, ZEROED as the "
+                              f"minority direction across categories")
+            elif _b.get('net_direction') in ('LONG', 'SHORT'):
+                _parts.append(f"{_lbl} → {_cat} {_b['net_direction']} "
+                              f"+{float(_b.get('contribution') or 0.0):.2f}, counted")
+            else:
+                _parts.append(f"{_lbl} → {_cat} 0, no signal inside its {_win:.0f}-min window")
+        if not _parts:
+            return ''
+        return ("  Score matrix, as the score gate counted these tiers (it counts every signal "
+                "still inside its category window, not only the latest per slot): "
+                + " | ".join(_parts) + "\n")
+    except Exception as _e:   # a malformed matrix_result must never break the entry path
+        print(f"[MERCURY-SOL][MATRIX-LINE] render failed (non-fatal, line omitted): "
+              f"{type(_e).__name__}: {_e}", flush=True)
+        return ''
+
+
 def consult_for_entry(symbol, direction, vol_snap,
                       market_regime=None, news_summary=None,
                       mtf_alignment_score=None, pre_trade_walls=None,
-                      combo_weight=None, sm_snapshot=None):
+                      combo_weight=None, sm_snapshot=None, matrix_result=None):
     """Ask Claude whether to take the entry.
 
     direction       — 'LONG' | 'SHORT'
@@ -881,12 +959,17 @@
             f"Decide for yourself how much weight a tier that old deserves.\n")
     _hidden_1h = ("  1H LuxAlgo tier: NOT SHOWN in this prompt — do NOT assume it "
                   "agrees or opposes\n" if AI_ADVISOR_HIDE_1H else "")
+    # 🔴 2026-09-11 — the MATRIX's reading of the SAME tiers, as one fact line directly
+    # under the tally. The tally is UNCHANGED (it still counts the slots); this line
+    # re-counts nothing. '' when matrix_result is None. See _render_matrix_tier_line.
+    _matrix_line = _render_matrix_tier_line(_shown, matrix_result)
     user += (
         f"\nTier agreement vs {_dir_up} (computed for this consultation):\n"
         + _hidden_1h
         + "\n".join(_agree_lines) + "\n"
         + _stale_line
         + _tally_line
+        + _matrix_line
         + "The cascade gate, the score gate and the risk gate have already passed. "
         "That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement "
         "that the tiers listed above agree with each other.\n"
--- a/main.py
+++ b/main.py
@@ -5085,6 +5085,10 @@
                 # the state_machine snapshot captured above (line ~1841) — same fresh
                 # 5m_trigger the combo_key was built from; no new fetch.
                 sm_snapshot=_sm_snap,
+                # 2026-09-11 (Defect A): the SAME matrix_result the score gate used
+                # (compute_score above), rendered as ONE fact line under the tier tally
+                # and read by nothing else. See claude_advisor._render_matrix_tier_line.
+                matrix_result=matrix_result,
             )
         ai_decide = advice.get('decide')
         ai_conf   = float(advice.get('confidence') or 0.0)
```

## APPENDIX B — §1 raw output (this session's `s1.py`)

```
consultations with a prompt: 4598; with matrix breakdown: 4598; without: 0; PROPOSED-ENTRY/side mismatches: 0
span 2026-06-08 00:40:01 -> 2026-09-11 18:10:03 | distinct days 92
by era: {'A_1Hhidden': 2946, 'B_1Hshown': 1185, 'C_agewindow': 467}
tier shown: {'1H': 1652, '15m': 4598, '5m': 4598} | 1H split: {'1H-rearm': 452, '1H-trend': 1200}
unmapped tiers: []

== per tier (sub) x side x class ==
1H-trend  LONG  n=  563  {'COUNTED': 182, 'EMPTY': 343, 'OPPOSITE': 5, 'ZEROED_INTRA': 33}
1H-trend  SHORT n=  637  {'COUNTED': 241, 'EMPTY': 341, 'ZEROED_INTRA': 55}
1H-rearm  LONG  n=  189  {'COUNTED': 41, 'EMPTY': 22, 'OPPOSITE': 50, 'ZEROED_INTRA': 76}
1H-rearm  SHORT n=  263  {'COUNTED': 115, 'EMPTY': 26, 'OPPOSITE': 27, 'ZEROED_INTRA': 95}
15m       LONG  n= 2120  {'COUNTED': 970, 'EMPTY': 292, 'NEUTRAL_BOTH': 65, 'NEUTRAL_SHOWN_MATRIX_INTRA': 12, 'OPPOSITE': 1, 'REVERSE_COUNTED': 26, 'ZEROED_INTRA': 754}
15m       SHORT n= 2478  {'COUNTED': 1232, 'EMPTY': 305, 'NEUTRAL_BOTH': 51, 'NEUTRAL_SHOWN_MATRIX_INTRA': 22, 'REVERSE_COUNTED': 29, 'ZEROED_INTRA': 839}
5m        LONG  n= 2120  {'COUNTED': 1662, 'EMPTY': 1, 'ZEROED_INTRA': 457}
5m        SHORT n= 2478  {'COUNTED': 2023, 'EMPTY': 1, 'ZEROED_INTRA': 454}

== 1b DEFECT A: consults with >=1 shown directional tier ZEROED by intra-conflict: 2265/4598 = 49.3%  days=92/92
  LONG: 1074/2120 = 50.7%
  SHORT: 1191/2478 = 48.1%
  era A_1Hhidden: 1428/2946 = 48.5%
  era B_1Hshown: 574/1185 = 48.4%
  era C_agewindow: 263/467 = 56.3%
  consults where a zeroed tier is shown AGREEING with the proposed side (inflates): 1453 (31.6% of all)
  consults where a zeroed tier is shown OPPOSING the proposed side (deflates):      1090 (23.7% of all)
  per tier x side (tier-instances): zeroed & shown-agreeing / zeroed & shown-opposing / tier shown n
    1H-trend  LONG  agree=    5  oppose=   28  shown=  563   (5.9% of shown)
    1H-trend  SHORT agree=   13  oppose=   42  shown=  637   (8.6% of shown)
    1H-rearm  LONG  agree=   29  oppose=   47  shown=  189   (40.2% of shown)
    1H-rearm  SHORT agree=   66  oppose=   29  shown=  263   (36.1% of shown)
    15m       LONG  agree=  281  oppose=  473  shown= 2120   (35.6% of shown)
    15m       SHORT agree=  311  oppose=  528  shown= 2478   (33.9% of shown)
    5m        LONG  agree=  452  oppose=    5  shown= 2120   (21.6% of shown)
    5m        SHORT agree=  452  oppose=    2  shown= 2478   (18.3% of shown)
  decisions among inflating consults: {'skip': 1396, 'execute': 57}  statuses: {'ai_skipped': 1396, 'observed_skipped': 29, 'executed': 23, 'sl_failed_position_closed': 2, 'failed': 3}
  P(execute): inflating 57/1453 = 3.92% | no zeroed tier 40/2333 = 1.71%
  zeroed shown tiers per consult: {1: 1798, 2: 436, 3: 31}
  "shown-count" the AS-COUNTED tally gave vs matrix on inflating consults:
   (tiers shown agreeing, of those actually COUNTED by the matrix) -> consults: {(1, 0): 212, (2, 0): 139, (2, 1): 868, (3, 0): 8, (3, 1): 130, (3, 2): 96}

== 1c ENTRIES (closed virtual_positions), paper and live NEVER pooled ==
entries with a consult prompt: 38
  LIVE  inflating (zeroed tier shown AGREEING)                     n=11  ΣR=+7.733  wins=5  Σ$=+17.9640
  LIVE  deflating only (zeroed tier shown OPPOSING, none agreeing) n= 0  ΣR=+0.000  wins=0  Σ$=+0.0000
  LIVE  no zeroed tier shown                                       n= 5  ΣR=-0.979  wins=2  Σ$=-2.3665
  PAPER inflating (zeroed tier shown AGREEING)                     n=13  ΣR=+3.262  wins=7  Σ$=+737.1770
  PAPER deflating only (zeroed tier shown OPPOSING, none agreeing) n= 1  ΣR=-1.049  wins=0  Σ$=-233.6063
  PAPER no zeroed tier shown                                       n= 8  ΣR=-7.587  wins=1  Σ$=-1632.0288
  per entry:
   vpos  7 paper LONG  R=+2.089 $+494.2006 row 1920 2026-06-14 23:50 INFL ['15m:HyperWave Signal Up(LONG,MOMENTUM)', '5m:Bullish OB Created(LONG,EXECUTION)']
   vpos  8 paper LONG  R=-0.739 $-177.3411 row 3225 2026-06-20 07:00 INFL ['15m:HyperWave Signal Up(LONG,MOMENTUM)']
   vpos  9 paper LONG  R=-0.264 $-58.7117 row 3437 2026-06-21 02:50 INFL ['5m:Bullish OB Created(LONG,EXECUTION)']
   vpos 10 paper SHORT R=-1.066 $-245.2109 row 3685 2026-06-22 00:00 -    []
   vpos 11 paper SHORT R=+1.133 $+301.1562 row 4002 2026-06-23 00:30 INFL ['15m:HyperWave Signal Down(SHORT,MOMENTUM)', '5m:Bearish I-BOS(SHORT,EXECUTION)']
   vpos 12 paper LONG  R=-1.049 $-233.6063 row 4259 2026-06-24 02:25 DEFL ['15m:Bearish Divergence(SHORT,MOMENTUM)', '5m:Bearish I-CHOCH(SHORT,EXECUTION)']
   vpos 13 paper SHORT R=+1.337 $+327.2106 row 4370 2026-06-24 13:25 INFL ['5m:Bearish OB Created(SHORT,EXECUTION)']
   vpos 14 paper SHORT R=-1.032 $-405.9690 row 4652 2026-06-25 14:00 -    []
   vpos 15 paper SHORT R=+0.140 $+34.8251 row 7815 2026-07-08 05:05 INFL ['15m:HyperWave Signal Down(SHORT,MOMENTUM)']
   vpos 16 paper LONG  R=-1.146 $-194.7049 row 8446 2026-07-10 08:30 -    []
   vpos 17 paper SHORT R=+0.004 $+0.8624 row 9358 2026-07-13 03:10 -    []
   vpos 18 paper LONG  R=-1.074 $-234.0402 row 9842 2026-07-14 15:45 -    []
   vpos 19 paper SHORT R=+0.463 $+89.0012 row 10178 2026-07-16 00:25 INFL ['5m:Bearish I-CHOCH+(SHORT,EXECUTION)']
   vpos 20 paper SHORT R=-1.124 $-210.8823 row 10618 2026-07-17 13:40 -    []
   vpos 21 paper LONG  R=+0.285 $+33.6592 row 11181 2026-07-19 06:50 INFL ['15m:HyperWave Signal Up(LONG,MOMENTUM)']
   vpos 22 paper LONG  R=-1.064 $-203.4161 row 11679 2026-07-21 03:10 -    []
   vpos 23 paper SHORT R=-0.577 $-93.2433 row 13644 2026-07-28 11:05 INFL ['5m:Bearish I-CHOCH+(SHORT,EXECUTION)']
   vpos 24 paper SHORT R=-1.050 $-234.0339 row 13973 2026-07-29 20:05 INFL ['5m:Bearish S-CHOCH(SHORT,EXECUTION)']
   vpos 25 paper SHORT R=+1.257 $+126.5230 row 14988 2026-08-01 17:20 INFL ['1H:15m-rearm: HyperWave Signal Down(SHORT,MOMENTUM)', '15m:HyperWave Signal Down(SHORT,MOMENTUM)']
   vpos 26 paper LONG  R=-1.085 $-138.6677 row 15093 2026-08-02 05:00 -    []
   vpos 27 paper SHORT R=-0.660 $-85.4470 row 15410 2026-08-03 06:45 INFL ['15m:HyperWave Signal Down(SHORT,MOMENTUM)', '5m:Bearish New Imbalance(SHORT,LIQUIDITY)']
   vpos 28 paper SHORT R=-0.153 $-20.6217 row 16405 2026-08-06 19:00 INFL ['5m:Bearish New Imbalance(SHORT,LIQUIDITY)']
   vpos 29 LIVE  LONG  R=+1.355 $+1.6025 row 16767 2026-08-08 08:50 INFL ['15m:HyperWave Signal Up(LONG,MOMENTUM)']
   vpos 30 LIVE  LONG  R=+0.762 $+0.8720 row 16857 2026-08-08 21:10 -    []
   vpos 31 LIVE  LONG  R=-1.155 $-1.4554 row 17201 2026-08-10 08:10 -    []
   vpos 32 LIVE  SHORT R=-0.180 $-0.2663 row 17289 2026-08-10 15:15 INFL ['15m:HyperWave Signal Down(SHORT,MOMENTUM)']
   vpos 33 LIVE  LONG  R=-0.049 $-0.0677 row 17671 2026-08-11 22:00 INFL ['15m:HyperWave Signal Up(LONG,MOMENTUM)', '5m:Bullish I-BOS(LONG,EXECUTION)']
   vpos 34 LIVE  SHORT R=-0.643 $-0.9113 row 18111 2026-08-13 16:40 INFL ['5m:Bearish I-BOS(SHORT,EXECUTION)']
   vpos 35 LIVE  SHORT R=-0.701 $-0.7289 row 18345 2026-08-14 14:20 INFL ['5m:Bearish I-BOS(SHORT,EXECUTION)']
   vpos 36 LIVE  SHORT R=-0.757 $-0.7278 row 18578 2026-08-15 07:50 INFL ['15m:HyperWave Signal Down(SHORT,MOMENTUM)']
   vpos 37 LIVE  SHORT R=-1.226 $-1.1156 row 19108 2026-08-16 22:05 -    []
   vpos 38 LIVE  LONG  R=+4.031 $+4.7888 row 19689 2026-08-18 22:20 INFL ['5m:Bullish New Imbalance(LONG,LIQUIDITY)']
   vpos 39 LIVE  LONG  R=+1.604 $+3.7762 row 20103 2026-08-20 23:30 INFL ['5m:Bullish OB Created(LONG,EXECUTION)']
   vpos 40 LIVE  LONG  R=+2.549 $+7.7482 row 20271 2026-08-21 21:15 INFL ['5m:Bullish OB Created(LONG,EXECUTION)']
   vpos 41 LIVE  LONG  R=+1.633 $+4.8808 row 21453 2026-08-27 03:50 INFL ['1H:15m-rearm: HyperWave Signal Up(LONG,MOMENTUM)', '15m:HyperWave Signal Up(LONG,MOMENTUM)']
   vpos 42 LIVE  SHORT R=-1.083 $-2.8381 row 23053 2026-09-01 21:40 -    []
   vpos 43 LIVE  LONG  R=+1.723 $+2.1706 row 24167 2026-09-05 13:05 -    []
   vpos 44 LIVE  SHORT R=-1.110 $-2.1305 row 25731 2026-09-11 11:50 INFL ['1H:Trend Catcher Down(SHORT,TREND)', '15m:HyperWave Signal Down(SHORT,MOMENTUM)']

== 1e BOTH DIRECTIONS ==
  REVERSE (matrix scores a direction on a tier the slot shows NEUTRAL/n/a): 55/4598 consults; per tier: {'15m': 55} | shown names: {'n/a': 55} | days 17 | entries 2
  EMPTY                       {'15m': 597, '1H-rearm': 48, '1H-trend': 684, '5m': 2}
  OPPOSITE                    {'15m': 1, '1H-rearm': 77, '1H-trend': 5}
  ZEROED_INTER                {}
  NEUTRAL_SHOWN_MATRIX_INTRA  {'15m': 34}
  REVERSE_INTER               {}
  1H-trend EMPTY: total 684

== 1d reason vs the zeroed tier it was shown AGREEING (tier-instances) ==
  execute n=77 {'LuxAlgo/confluence/tier wording': 52, 'TF+direction, OHLCV agrees (ambiguous)': 4, None: 20, 'names the shown signal': 1}
  skip    n=1532 {'LuxAlgo/confluence/tier wording': 555, None: 883, 'TF+direction, OHLCV does NOT (must be the tier)': 76, 'names the shown signal': 3, 'TF+direction, OHLCV agrees (ambiguous)': 15}
  ENTRIES only: {'LuxAlgo/confluence/tier wording': 25, None: 5, 'TF+direction, OHLCV agrees (ambiguous)': 1} of 31

== opposing signal age vs TTL on zeroed tiers (trade_signal_matrix rows only) ==
   vpos  7 15m shown HyperWave Signal Up(LONG) | same-side in window: HyperWave Signal Up 50.0/90 | OPPOSING: HyperWave OB Signal Down 65.0/90
   vpos  7 5m  shown Bullish OB Created(LONG) | same-side in window: Bullish I-BOS 0.0/5, Bullish OB Created 0.0/5 | OPPOSING: Within Bearish OB 0.0/5
   vpos  8 15m shown HyperWave Signal Up(LONG) | same-side in window: HyperWave Signal Up 15.0/90 | OPPOSING: HyperWave OB Signal Down 60.0/90, Reversal Down + 75.0/90
   vpos  9 5m  shown Bullish OB Created(LONG) | same-side in window: Bullish OB Created 0.0/5 | OPPOSING: Within Bearish OB 0.0/5
   vpos 11 15m shown HyperWave Signal Down(SHORT) | same-side in window: HyperWave Signal Down 15.1/90 | OPPOSING: Bullish Divergence 75.2/90, HyperWave Signal Up 60.2/90, Reversal Up 75.2/90
   vpos 11 5m  shown Bearish I-BOS(SHORT) | same-side in window: Bearish I-BOS 0.0/5, Bearish OB Created 0.1/5 | OPPOSING: Bullish OB Entered 0.1/5
   vpos 12 15m shown Bearish Divergence(SHORT) | same-side in window: Bearish Divergence 10.0/90, HyperWave OB Signal Down 10.0/90, Reversal Down + 85.0/90 | OPPOSING: HyperWave Signal Up 24.9/90
   vpos 12 5m  shown Bearish I-CHOCH(SHORT) | same-side in window: Bearish I-CHOCH 0.0/5, Bearish OB Created 0.0/5 | OPPOSING: Bullish Breaker 0.0/5, Within Bullish OB 5.0/5
   vpos 13 5m  shown Bearish OB Created(SHORT) | same-side in window: Bearish I-CHOCH 0.1/5, Bearish OB Created 0.0/5 | OPPOSING: Bullish Breaker 0.1/5, Within Bullish OB 0.1/5
   vpos 15 15m shown HyperWave Signal Down(SHORT) | same-side in window: HyperWave Signal Down 4.8/90 | OPPOSING: HyperWave Signal Up 19.9/90
   vpos 19 5m  shown Bearish I-CHOCH+(SHORT) | same-side in window: Bearish I-CHOCH+ 0.0/5 | OPPOSING: Within Bullish OB 5.0/5
   vpos 21 15m shown HyperWave Signal Up(LONG) | same-side in window: HyperWave Signal Up 19.9/90 | OPPOSING: HyperWave Signal Down 49.9/90
   vpos 23 5m  shown Bearish I-CHOCH+(SHORT) | same-side in window: Bearish I-CHOCH+ 0.0/5, Bearish S-BOS 0.0/5 | OPPOSING: Bullish OB Entered 4.9/5, Within Bullish OB 5.0/5
   vpos 24 5m  shown Bearish S-CHOCH(SHORT) | same-side in window: Bearish S-CHOCH 0.0/5 | OPPOSING: Bullish Breaker 4.5/5
   vpos 25 1H  shown 15m-rearm: HyperWave Signal Down(SHORT) | same-side in window: HyperWave Signal Down 5.0/90 | OPPOSING: HyperWave Signal Up 35.0/90
   vpos 25 15m shown HyperWave Signal Down(SHORT) | same-side in window: HyperWave Signal Down 5.0/90 | OPPOSING: HyperWave Signal Up 35.0/90
   vpos 27 15m shown HyperWave Signal Down(SHORT) | same-side in window: HyperWave Signal Down 0.0/90 | OPPOSING: HyperWave Signal Up 30.0/90
   vpos 27 5m  shown Bearish New Imbalance(SHORT) | same-side in window: Bearish New Imbalance 0.0/30 | OPPOSING: Bullish Imbalance Mitigated 0.0/30, Bullish Liquidity Grab 10.0/30
   vpos 28 5m  shown Bearish New Imbalance(SHORT) | same-side in window: Bearish New Imbalance 0.0/30 | OPPOSING: Bullish Imbalance Mitigated 25.1/30
   vpos 32 15m shown HyperWave Signal Down(SHORT) | same-side in window: HyperWave Signal Down 0.2/90 | OPPOSING: HyperWave Signal Up 45.2/90
   vpos 33 15m shown HyperWave Signal Up(LONG) | same-side in window: HyperWave Signal Up 0.0/90 | OPPOSING: Bearish Divergence 15.0/90, HyperWave OB Signal Down 15.0/90, Reversal Down 60.0/90
   vpos 33 5m  shown Bullish I-BOS(LONG) | same-side in window: Bullish I-BOS 0.0/5 | OPPOSING: Bearish Breaker 0.0/5
   vpos 34 5m  shown Bearish I-BOS(SHORT) | same-side in window: Bearish I-BOS 0.0/5, Bearish OB Created 0.0/5 | OPPOSING: Bullish Breaker 0.0/5, Bullish OB Entered 0.0/5, Within Bullish OB 0.0/5
   vpos 35 5m  shown Bearish I-BOS(SHORT) | same-side in window: Bearish I-BOS 0.0/5, Bearish OB Created 0.0/5 | OPPOSING: Bullish OB Entered 0.0/5
   vpos 36 15m shown HyperWave Signal Down(SHORT) | same-side in window: HyperWave Signal Down 5.0/90 | OPPOSING: HyperWave Signal Up 49.9/90
   vpos 38 5m  shown Bullish New Imbalance(LONG) | same-side in window: Bullish New Imbalance 0.0/30, Broken D. 25.0/30 | OPPOSING: Bearish Liquidity Grab 5.0/30
   vpos 39 5m  shown Bullish OB Created(LONG) | same-side in window: Bullish I-CHOCH 0.0/5, Bullish OB Created 0.0/5 | OPPOSING: Bearish Breaker 0.0/5, Within Bearish OB 0.0/5
   vpos 40 5m  shown Bullish OB Created(LONG) | same-side in window: Bullish OB Created 0.0/5 | OPPOSING: Within Bearish OB 0.0/5
   vpos 41 1H  shown 15m-rearm: HyperWave Signal Up(LONG) | same-side in window: HyperWave Signal Up 4.9/90 | OPPOSING: HyperWave Signal Down 65.0/90
   vpos 41 15m shown HyperWave Signal Up(LONG) | same-side in window: HyperWave Signal Up 4.9/90 | OPPOSING: HyperWave Signal Down 65.0/90
   vpos 44 1H  shown Trend Catcher Down(SHORT) | same-side in window: Trend Catcher Down 49.9/360 | OPPOSING: Trend Catcher Up 349.8/360
   vpos 44 15m shown HyperWave Signal Down(SHORT) | same-side in window: HyperWave Signal Down 49.8/90 | OPPOSING: HyperWave Signal Up 80.0/90
  opposing-signal age as a fraction of its TTL: n=91 median=0.39 p25=0.01 p75=0.83  >=0.8: 23
  trade_signal_matrix breakdown identical to trades.matrix_breakdown_json on 93 of 93 consult rows

== effective n: 2265 consults; 92 days; 893 (tier, signal, day) episodes; entries 25 (live 11, paper 14)
vpos44: {'1H': ('Trend Catcher Down', 'SHORT', 'TREND', 'ZEROED_INTRA'), '15m': ('HyperWave Signal Down', 'SHORT', 'MOMENTUM', 'ZEROED_INTRA'), '5m': ('Bearish OB Entered', 'SHORT', 'EXECUTION', 'COUNTED')} | cite: ['LuxAlgo/confluence/tier wording', 'LuxAlgo/confluence/tier wording']
vpos44 reason: 3-tier SHORT confluence (1H/15m/5m all bearish); 1h/4h BEAR regime supportive; 1h ADX 44.5 strong trend; no opposing wall blocks short entry; 15m ADX weak but overridden by lower-TF trigger + higher-TF alignment
```

## APPENDIX C — §3 raw output (this session's `s3.py`, T_LOAD 2026-08-14 19:52:53, PARTIAL_ON 2026-08-01 15:44)

```
consistency: stored breakeven_applied vs "water_mark reached the reconstructed arm":
  agree on 38 of 38; disagree: []

per position (arm R | BE applied | candle crossed arm? first crossing | poller wm vs arm):
  vpos  7 paper LONG  armR=1.00 partial=0 BE=Y arm=72.661 wm=76.020 bestcandle=76.060 cross=559(558 int) first=('06-15 11:20', 'interior', 72.69) R=+2.089 exit_signal
  vpos  8 paper LONG  armR=1.00 partial=0 BE=n arm=73.778 wm=72.080 bestcandle=72.100 cross=0(0 int) first=- R=-0.739 exit_signal
  vpos  9 paper LONG  armR=1.00 partial=0 BE=n arm=74.933 wm=73.800 bestcandle=73.830 cross=0(0 int) first=- R=-0.264 exit_signal
  vpos 10 paper SHORT armR=1.00 partial=0 BE=n arm=70.902 wm=72.480 bestcandle=72.410 cross=0(0 int) first=- R=-1.066 sl
  vpos 11 paper SHORT armR=1.00 partial=0 BE=Y arm=69.532 wm=68.180 bestcandle=68.050 cross=798(797 int) first=('06-23 08:13', 'interior', 69.01) R=+1.133 exit_signal
  vpos 12 paper LONG  armR=1.00 partial=0 BE=n arm=71.103 wm=70.290 bestcandle=70.420 cross=0(0 int) first=- R=-1.049 sl
  vpos 13 paper SHORT armR=1.00 partial=0 BE=Y arm=66.946 wm=64.670 bestcandle=64.660 cross=100(99 int) first=('06-24 16:46', 'interior', 66.93) R=+1.337 trail
  vpos 14 paper SHORT armR=1.00 partial=0 BE=n arm=62.302 wm=64.620 bestcandle=64.180 cross=0(0 int) first=- R=-1.032 sl
  vpos 15 paper SHORT armR=1.00 partial=0 BE=Y arm=76.613 wm=76.260 bestcandle=76.240 cross=45(45 int) first=('07-08 13:25', 'interior', 76.58) R=+0.140 trail
  vpos 16 paper LONG  armR=1.00 partial=0 BE=n arm=80.724 wm=79.590 bestcandle=79.630 cross=0(0 int) first=- R=-1.146 sl
  vpos 17 paper SHORT armR=1.00 partial=0 BE=Y arm=74.410 wm=74.140 bestcandle=74.040 cross=43(43 int) first=('07-13 21:10', 'interior', 74.39) R=+0.004 sl
  vpos 18 paper LONG  armR=1.00 partial=0 BE=n arm=79.157 wm=78.980 bestcandle=79.010 cross=0(0 int) first=- R=-1.074 sl
  vpos 19 paper SHORT armR=1.00 partial=0 BE=n arm=75.561 wm=75.600 bestcandle=75.570 cross=0(0 int) first=- R=+0.463 exit_signal
  vpos 20 paper SHORT armR=1.00 partial=0 BE=n arm=72.201 wm=73.360 bestcandle=73.340 cross=0(0 int) first=- R=-1.124 sl
  vpos 21 paper LONG  armR=1.00 partial=0 BE=Y arm=76.955 wm=77.350 bestcandle=77.390 cross=25(25 int) first=('07-20 00:15', 'interior', 77.09) R=+0.285 trail
  vpos 22 paper LONG  armR=1.00 partial=0 BE=n arm=79.912 wm=78.840 bestcandle=78.860 cross=0(0 int) first=- R=-1.064 sl
  vpos 23 paper SHORT armR=1.00 partial=0 BE=n arm=71.800 wm=72.360 bestcandle=72.310 cross=0(0 int) first=- R=-0.577 exit_signal
  vpos 24 paper SHORT armR=1.00 partial=0 BE=n arm=71.048 wm=72.260 bestcandle=72.240 cross=0(0 int) first=- R=-1.050 sl
  vpos 25 paper SHORT armR=1.00 partial=1 BE=Y arm=71.740 wm=70.640 bestcandle=70.530 cross=134(133 int) first=('08-01 17:34', 'interior', 71.66) R=+1.257 trail
  vpos 26 paper LONG  armR=1.00 partial=1 BE=n arm=74.466 wm=74.210 bestcandle=74.310 cross=0(0 int) first=- R=-1.085 sl
  vpos 27 paper SHORT armR=1.00 partial=1 BE=n arm=71.587 wm=71.980 bestcandle=71.920 cross=0(0 int) first=- R=-0.660 sl
  vpos 28 paper SHORT armR=1.00 partial=1 BE=n arm=71.788 wm=72.290 bestcandle=72.270 cross=0(0 int) first=- R=-0.153 exit_signal
  vpos 29 LIVE  LONG  armR=1.00 partial=1 BE=Y arm=75.710 wm=76.460 bestcandle=76.800 cross=263(262 int) first=('08-08 14:04', 'interior', 75.74) R=+1.355 exchange_UNKNOWN
  vpos 30 LIVE  LONG  armR=1.00 partial=1 BE=Y arm=77.174 wm=77.760 bestcandle=77.830 cross=294(294 int) first=('08-09 15:37', 'interior', 77.18) R=+0.762 trail
  vpos 31 LIVE  LONG  armR=1.00 partial=1 BE=n arm=78.015 wm=77.100 bestcandle=77.110 cross=0(0 int) first=- R=-1.155 sl
  vpos 32 LIVE  SHORT armR=1.00 partial=1 BE=n arm=75.038 wm=75.600 bestcandle=75.550 cross=0(0 int) first=- R=-0.180 exit_signal
  vpos 33 LIVE  LONG  armR=1.00 partial=1 BE=n arm=77.566 wm=77.150 bestcandle=77.370 cross=0(0 int) first=- R=-0.049 exit_signal
  vpos 34 LIVE  SHORT armR=1.00 partial=1 BE=n arm=74.122 wm=75.080 bestcandle=75.050 cross=0(0 int) first=- R=-0.643 sl
  vpos 35 LIVE  SHORT armR=1.00 partial=1 BE=n arm=74.360 wm=75.020 bestcandle=75.010 cross=0(0 int) first=- R=-0.701 sl
  vpos 36 LIVE  SHORT armR=0.75 partial=0 BE=n arm=74.642 wm=74.990 bestcandle=74.990 cross=0(0 int) first=- R=-0.757 exchange_market
  vpos 37 LIVE  SHORT armR=0.75 partial=0 BE=n arm=73.859 wm=74.220 bestcandle=74.210 cross=0(0 int) first=- R=-1.226 sl
  vpos 38 LIVE  LONG  armR=0.75 partial=0 BE=Y arm=77.805 wm=82.000 bestcandle=82.070 cross=157(156 int) first=('08-19 12:41', 'interior', 77.89) R=+4.031 trail
  vpos 39 LIVE  LONG  armR=0.75 partial=0 BE=Y arm=89.427 wm=93.260 bestcandle=93.400 cross=283(282 int) first=('08-21 01:49', 'interior', 89.48) R=+1.604 trail
  vpos 40 LIVE  LONG  armR=0.75 partial=0 BE=Y arm=94.506 wm=102.640 bestcandle=102.740 cross=164(163 int) first=('08-21 22:42', 'interior', 94.52) R=+2.549 trail
  vpos 41 LIVE  LONG  armR=0.75 partial=0 BE=Y arm=103.532 wm=109.560 bestcandle=109.570 cross=603(602 int) first=('08-27 08:09', 'interior', 104.22) R=+1.633 trail
  vpos 42 LIVE  SHORT armR=0.75 partial=0 BE=n arm=97.278 wm=97.340 bestcandle=97.290 cross=0(0 int) first=- R=-1.083 sl
  vpos 43 LIVE  LONG  armR=0.75 partial=0 BE=Y arm=104.290 wm=106.970 bestcandle=107.100 cross=83(82 int) first=('09-05 17:33', 'interior', 104.29) R=+1.723 trail
  vpos 44 LIVE  SHORT armR=0.75 partial=0 BE=n arm=97.860 wm=98.080 bestcandle=97.760 cross=1(1 int) first=('09-11 12:30', 'interior', 97.76) R=-1.110 sl

== MISSES (venue printed through the arm, poller water mark never reached it, lock never armed): 1 of 38 ==
  vpos 44 LIVE  SHORT first print 2026-09-11 12:30 (interior) through by 0.100 | poller short by 0.220 = 0.115R | realised R=-1.110 $-2.1305 (sl) -> CF exit 99.101 via BE: R=+0.000 $+0.0002  delta +1.110R $+2.1307 (fee rate 0.1000%, act_chk -2.1305 vs net -2.1305)
  LIVE : n=1 realised ΣR=-1.110 Σ$=-2.1305 | CF ΣR=+0.000 Σ$=+0.0002 | delta ΣR=+1.110 Σ$=+2.1307
  PAPER: n=0 realised ΣR=+0.000 Σ$=+0.0000 | CF ΣR=+0.000 Σ$=+0.0000 | delta ΣR=+0.000 Σ$=+0.0000

near misses (lock never armed, best candle within 0.10R of the arm but did not cross):
  vpos 18 paper candle short of arm by 0.147 = 0.087R; poller short by 0.105R
  vpos 19 paper candle short of arm by 0.009 = 0.006R; poller short by 0.027R
  vpos 42 LIVE candle short of arm by 0.012 = 0.005R; poller short by 0.024R
```

---

## ADDENDUM (19:4x UTC) — the live proof, same file, same URL

The read-only waiter armed at 18:27 found the first entry consultation after the 18:26:59 restart. There were no consultations before it: 18:30-19:30 rows were exit_unarmed_noop, htf_blocked ×4, context_recorded, and 19:40:05 entry_gate_refused.
- **The stored `ai_user_prompt` carries the line, exactly once, directly under the AS-COUNTED tally.**
- **Each tier claim was checked against that row's own stored `matrix_breakdown_json`: 3 of 3 AGREE.**
- It also shows a mismatch class other than vpos 44's. The 15m slot said `HyperWave Signal Down -> SHORT = OPPOSES`, while MOMENTUM held **no signal inside its 90-min window**. The tally counted that tier as an opposing vote; the line now states that the matrix had nothing there (the EMPTY class, §1e).
- mercury-sol MainPID 1341949, NRestarts 0, unchanged since the restart.

```
FIRST POST-RESTART CONSULT: trades.id 25817 2026-09-11 19:40:06 status=ai_skipped open_long decision=skip reused=False
matrix line present: True
  Score matrix, as the score gate counted these tiers (it counts every signal still inside its category window, not only the latest per slot): 1H → TREND LONG +2.25, counted | 15m → MOMENTUM 0, no signal inside its 90-min window | 5m trigger → EXECUTION LONG +2.50, counted
  1H         TREND     line says ZEROED=False  stored breakdown intra_conflict=False  net=LONG contrib=2.25  -> AGREE
  15m        MOMENTUM  line says ZEROED=False  stored breakdown intra_conflict=False  net=NEUTRAL contrib=0.0  -> AGREE
  5m trigger EXECUTION line says ZEROED=False  stored breakdown intra_conflict=False  net=LONG contrib=2.5  -> AGREE
--- full stored prompt tier block ---
Tier agreement vs LONG (computed for this consultation):
  1H: Smart Trail Switch Bullish -> LONG = AGREES
  15m: HyperWave Signal Down -> SHORT = OPPOSES
  5m trigger: Bullish OB Created -> LONG = AGREES
  Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 2 agree, 1 oppose, 0 neutral, 0 absent.
  Score matrix, as the score gate counted these tiers (it counts every signal still inside its category window, not only the latest per slot): 1H → TREND LONG +2.25, counted | 15m → MOMENTUM 0, no signal inside its 90-min window | 5m trigger → EXECUTION LONG +2.50, counted
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.
```
