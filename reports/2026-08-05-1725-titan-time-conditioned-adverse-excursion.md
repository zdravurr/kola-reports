# TITAN — TIME-CONDITIONED ADVERSE EXCURSION: DOES THE ADVISOR REACT, AND IS A CLOCK-TIER WORTH BUILDING?

**2026-08-05 17:25 UTC · READ-ONLY · nothing changed, NOTHING PROPOSED, NO DIFF · HEAD `b9081ad`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
Mercury-SOL never opened. `git status` on `titan-bot` clean before and after; `trades.db` opened
read-only (`file:…?mode=ro`) throughout. **0 open positions** for the whole pass.

Parent: `2026-08-05-1515-titan-does-the-exit-advisor-know-it-is-in-a-failed-breakout.md`.
Grandparent: `2026-08-05-1455-titan-what-discriminates-a-real-breakout-from-a-failed-one.md`.

---

## 🔴 BONFERRONI HEADER — READ BEFORE ANY NUMBER BELOW

**The budget was set at 54. The 14:55 report took the book to cell 115. This pass spends 77 more —
23 in §1, 12 in §2, 40 in §2e, 2 in the head-to-head — taking the book to cell ≈192.**

- Bonferroni α at the stated budget = 0.05 / 54 = **0.000926**.
- **§2 and §2e are a 52-cell grid on n=40 clean closed positions, of which only 16–31 are even
  alive at the horizon being tested. Every §2/§2e figure below is NOMINAL and nothing else.**
- 🔴 **It does not matter here, and that is the cleanest thing about this pass: no §2 or §2e cell
  reaches the operator's own gate, so there is no hit to correct.** The two §1 results that *do*
  clear 0.000926 (p < 0.0001, twice) are **not** a search — they are the single pre-named question
  §1 asked, answered on n=118.

---

## ANSWER IN ONE LINE

**§3's third branch fires: NEITHER SURVIVES, and both die for a stated reason rather than for want
of nerve.**

1. 🔴 **§1 — THE ADVISOR IS NOT BLIND TO DRAWDOWN. It is one of the strongest relationships in
   this entire book.** Across all 118 stored exit consultations the `close` rate runs **95 % at
   `upnl_r` < −0.5R against 25–27 % around flat** (point-biserial **r = −0.398**, perm-p < 0.0001;
   on the §2.18-clean subset **r = −0.504**). `giveback_r` is stronger still (**r = +0.533**,
   15 % → 94 % across its range). **The advisor reads the drawdown it is handed and acts on it.**
2. 🔴 **§1d — THE PROMPT ALREADY CARRIES POSITION AGE, and has since the exit advisor's first
   commit.** `claude_advisor.py:686`, verbatim: `f"  Elapsed: {g('elapsed_h','.1f')}h\n"`.
   It is present on **118 of 118** stored prompts. The advisor **quotes it back** — *"6h elapsed"*,
   *"Position down 0.53R after 26h"*, *"−0.09R after 4h"* — in **25 of 118** reasons.
   **The brief's structural premise is wrong on this point, and the correction is load-bearing:
   §3's second branch is asking for a fact that shipped on 2026-07-26.**
3. 🔴 **§2 / §2e — THE MECHANICAL TIER IS WORSE THAN DOING NOTHING IN 51 OF 52 CELLS.** The single
   positive cell is **+0.154R on the whole 40-position book** — it **loses on the LONG side**
   (ΔLONG −0.913R), its bootstrap CI is **[−8.10, +7.01]R**, and it closes **11 eventually-profitable
   positions worth +8.892R** to do it. **The operator's own §2c objection is not merely a risk here;
   it is the entire result.**
4. 🔴 **§2e — THE FIBONACCI LEVELS ARE INDISTINGUISHABLE FROM THEIR PLAIN NEIGHBOURS IN 15 OF 16
   CELLS** — identical position sets, identical n, identical R to the decimal. 0.618 and 0.60 are
   the same rule on this book. **And the move-normalised form LOSES to the ATR form** by +2.567R at
   each one's own best cell, so the second normalisation adds nothing.

**No diff is attached, for either branch. Both of §3's diff conditions were tested and neither is
met.**

---

## §0 — WHAT WAS MEASURED, AND THE VALIDATION THAT CAME FIRST

| item | provenance |
|---|---|
| **118 exit consultations** | `trades WHERE status='exit_ai_dryrun'`, 2026-07-26 22:06 → 2026-08-04 00:26. `upnl_r` / `mfe_r` / `giveback_r` / `dist_sl_r` / `elapsed_h` parsed **from the stored `ai_user_prompt`** — the literal text the model saw, not a reconstruction. **118/118 parse on every field.** |
| **40 clean closed positions** | `virtual_positions` under §0's filters: recheck TIGHTEN removed (11), wall-trail **lifetime overlap** removed (8), `archived_pre_geometry_fix` removed (6), one row with NULL `initial_risk_usdt` (vpos 33) removed. **= §2.45a's n=40 exactly.** |
| **candles** | BingX public REST 5m, **22,095 bars**, 2026-05-21 00:00 → 2026-08-05 17:10, **zero gaps** — the bot's own indicator source (`main.py:555` `ccxt.bingx`). Per §0's *excursion truth* rule, excursions come from real OHLCV, never from `max_adverse_price`. |
| **105 squeeze episodes** | reused from the 12:10 report **only** to re-measure the overlap in §2b. **No episode statistic is transferred into §2.** |

### 🔴 THE ERA SPLIT IS DEGENERATE, AND THAT IS A LIMIT ON EVERYTHING IN §2

| era | clean closed positions |
|---|---|
| **before** the 1R boundary 2026-08-04 17:01:29 | **40** |
| **from** the boundary onward | 🔴 **0** |

**There is nothing to pool and nothing to split — the entire clean book is on the OLD side.**
The brief asked for the correct side of the boundary or a per-era report; the honest answer is that
**the correct side is empty.** Every §2/§2e figure is therefore in the **old 1R unit** and, more
importantly, describes the **old geometry** — SL 2.5 ATR, trail 1.00R. The bot now runs SL 2.25 /
trail 0.75R (§2.53). A rule fitted here would be fitted to a machine that no longer exists.

**Actual book, stated before any counterfactual:** sum **+0.7329R** over 40 — **LONG −3.7712R (n=15)**,
**SHORT +4.5041R (n=25)**. Median lifetime **7.0 h** (min 0.02 h, max 74.3 h).

### 🔴 §0'S STANDING RULE — THE REPLAY REPRODUCES THE BOOK BEFORE IT PREDICTS ANYTHING

| check | result |
|---|---|
| entry fill **and** exit price both inside their own 5m candle range | **40 / 40** |
| `close_reason='sl'` rows whose candle path actually reached the stop **in force at close** | **12 / 12** |

⚠️ **One check I got wrong first, recorded rather than quietly fixed.** The first version tested
against `original_sl_price` and reported **11/12**, flagging vpos 45. vpos 45 is not a replay
failure: its stop had been **trailed** from 72,275.6 to 73,397.0 and fired there (`close_price`
73,387.6, R **+0.040**). The candle path does contain 73,397. **A "stop loss" that closes a position
in profit is a moved stop, and a validation keyed to the original stop will mislabel every one of
them.** Re-run against the stop in force: **12/12**.

---

## §1 — DOES THE EXIT ADVISOR ACTUALLY REACT TO DRAWDOWN? **YES, STRONGLY.**

**n = 118 consultations across 11 positions (vpos 82–92)**; 58 `close`, 60 `hold`; 0 unlinked.
Triggers: `hourly` 103 · `15m_exit_confirm` 14 · `armed_exit` 1.

⚠️ **§2.18 carry:** 60 of the 118 predate `c307bb7` (2026-07-29 13:21) and carried the false
*"the stop and trail remain active"* promise, whose bias is toward HOLD. **Both cohorts are reported
side by side and the clean one governs.** It makes the finding stronger, not weaker.

### 1a. 🔴 `close` RATE vs `upnl_r` — MONOTONE, AND STEEP

| `upnl_r` at consult | all 118 · n | close | **post-`c307bb7` · n** | **close** |
|---|---|---|---|---|
| < −0.50R | 20 | **95.0 %** | 10 | **90.0 %** |
| −0.50 … −0.25R | 21 | **81.0 %** | 10 | **70.0 %** |
| −0.25 … 0.00R | 24 | 25.0 % | 15 | 20.0 % |
| 0.00 … +0.25R | 33 | 27.3 % | 19 | **0.0 %** |
| +0.25 … +0.50R | 9 | 33.3 % | 2 | 0.0 % |
| +0.50 … +1.00R | 7 | 42.9 % | 1 | 0.0 % |
| ≥ +1.00R | 4 | 25.0 % | 1 | 100.0 % |

**point-biserial r = −0.398** (mean `upnl_r` | close −0.233 vs | hold +0.125, **perm-p < 0.0001**,
20 k shuffles). **On the §2.18-clean 58: r = −0.504, perm-p < 0.0001.**

**This is not flat. The brief's "if flat, the advisor is NOT reading the drawdown — that is the
finding" resolves the other way, and decisively.**

### 1b. `mfe_r` AND `giveback_r`

| quantity | relationship | verdict |
|---|---|---|
| **`mfe_r`** | 50.0 / 34.5 / 62.2 / 25.0 % across four buckets · **r = +0.087 · perm-p 0.354** | 🔴 **non-monotone, nothing.** Peak-so-far on its own does not move the verdict |
| 🔴 **`giveback_r`** | **15.0 → 11.8 → 50.0 → 69.2 → 94.1 %** across five buckets · **r = +0.533 · perm-p < 0.0001** | **monotone and the single strongest field measured** |
| `dist_sl_r` | 100 / 94.4 / 48.9 / 30.2 / 37.5 % · **r = −0.442 · perm-p < 0.0001** | strong, but **collinear with `upnl_r` by construction** (`dist_sl_r = upnl_r + 1` whenever the stop has not moved) — not independent evidence |

**The pair is the story: giveback beats MFE, and drawdown beats both raw peak and raw profit.**
The advisor is not reacting to "am I up", it is reacting to **"how much of this has gone wrong"** —
which is exactly the quantity the 15:15 report identified as informative.

### 1c. 🔴 DOES THE VERBATIM REASON CITE DRAWDOWN? **CONSTANTLY — BUT NEVER AS THE HEADLINE.**

| category (regex over the stored `ai_reason`, all 118) | consults | share | of the 58 `close` |
|---|---|---|---|
| entry thesis / tiers | 118 | 100.0 % | **58 / 58** |
| order book / walls | 118 | 100.0 % | 58 / 58 |
| regime / trend / ADX | 116 | 98.3 % | 58 / 58 |
| **PnL / drawdown / R** | **106** | **89.8 %** | **48 / 58 = 82.8 %** |
| **explicitly ADVERSE PnL** (drawdown, underwater, giveback, −xR) | **64** | **54.2 %** | **34 / 58 = 58.6 %** |
| stop / trail geometry | 58 | 49.2 % | 13 / 58 |
| **duration / elapsed / "after Nh"** (timeframe tokens excluded) | **25** | **21.2 %** | 15 / 58 |
| volume / ATR | 23 | 19.5 % | 5 / 58 |

🔴 **THE STRUCTURE §2.4's TALLY SAW IS REAL AND IT IS A RHETORICAL ONE, NOT A CAUSAL ONE.**
Applying a mutually-exclusive priority order to the **first clause** of each `close` reason:
**entry thesis 58 / 58 = 100 %.** **Zero `close` verdicts lead with P&L.** But **48 of those same 58
cite P&L further in.** The advisor **always frames the decision as "the entry thesis is broken"**
and then **supplies the drawdown as the corroborating detail.**

Two verbatim examples, chosen because they show both halves in one string:

> *"Entry thesis deteriorated. ADX1h now 42.1 (overextended from 26.3), suggesting momentum
> exhaustion. **MFE +0.80R given back 1.10R — classic rejection.**"* (row 19285, 22.0 h, CLOSE)

> *"Entry thesis deteriorated. ADX1h spiked to 40.0 …—multi-TF confluence broken. **Position down
> 0.53R after 26h** with only …"* (row 19339, 26.0 h, CLOSE)

**Reading §2.4's tally as "the advisor decides on thesis, not on P&L" would have been a mistake, and
the correlation in §1a is why: the header is thesis; the discriminant is drawdown.**

### 🔴 1a-CONTROL — §2.54'S METHOD APPLIED, BECAUSE THE OBVIOUS CONFOUND IS OBVIOUS

Price moving against you *is* the thesis breaking. So the relationship in §1a could be regime
deterioration wearing drawdown's clothes. Stratifying by whether the **live 15m/5m regime printed in
the prompt has turned against the position** (parsed from the `Now:` line, 117/118):

| stratum | n | overall close rate | `upnl` < −0.50R | −0.50…−0.25 | −0.25…+0.25 | > +0.25R |
|---|---|---|---|---|---|---|
| 🔴 **regime NOT turned** | **90** | 36.7 % | **100.0 %** (n=2) | **80.0 %** (n=15) | **25.5 %** (n=55) | 27.8 % (n=18) |
| regime TURNED against | 28 | 89.3 % | 94.4 % (n=18) | 83.3 % (n=6) | 50.0 % (n=2) | 100 % (n=2) |

**The effect survives on the larger stratum.** On the **90 consults where the regime has NOT turned**
— i.e. where the advisor has no regime story to tell — the close rate still runs **80–100 % under
drawdown against 25.5 % around flat.** Where the regime *has* turned, it closes at ~89 % more or
less regardless, and drawdown adds little.

**Unlike §2.54's pockets and §2.46's location rule, this one does not flip, thin or vanish under its
control.** That is the third time this book has run this control and the first time something has
come through it intact.

### 1d. 🔴 IS POSITION AGE IN THE PROMPT? **YES. VERBATIM, AND ON EVERY CONSULT.**

`main.py:2762-2764` computes it:

```python
if vpos.get('opened_at'):
    ctx['elapsed_h'] = (datetime.now(timezone.utc) - datetime.fromisoformat(
        vpos['opened_at'])).total_seconds() / 3600.0
```

`claude_advisor.py:686` renders it, and this is the line as it stands in the file:

```python
f"  Elapsed: {g('elapsed_h','.1f')}h\n"
```

It sits in the **Position** block, third line, directly beneath `Unrealised: …R`. As it reaches the
model (row **21149**, the most recent consult, 2026-08-04 00:26:02):

```
Position
  Side: LONG   Entry: 63920.2   Now: 63416.3
  Unrealised: -0.65R   (1R = the ORIGINAL stop distance)
  Elapsed: 4.0h
  Current stop: 63139.3  ->  +0.35R away
  Peak so far (MFE): +0.00R   Giveback from peak: 0.65R
```

`git log -S` puts it in **`ef7fa10`, 2026-07-26 22:09:27 UTC** — *"wire the exit advisor in DRYRUN"*,
**the commit that created the exit advisor.** It has never not been there, which is why the field
parses on **118 of 118** prompts.

**And it is used, not merely present:** 25 reasons cite duration explicitly, including
*"1H bullish confirmation now stale (6h elapsed)"* (row 19284) and *"Position −0.09R after 4h;
stop +0.91R away provides adequate buffer"* (row 19257, a HOLD).

⚠️ **The rest of the brief's structural claim is correct and stands.** `RECHECK_TIERS_SEC = [10, 60,
300]` (`config.py:822`) — all three tiers really do fire inside the first five minutes; the stop and
trail really do watch price and not time. **But the exit advisor is a multi-hour clock, it runs at
`EXIT_ADVISOR_HOURLY_SEC = 3600`, and it is told the hour.** "There is nobody to ask" is not true.

**Age alone, incidentally, does not survive de-confounding the way drawdown does:** close rate rises
0 → 45 → 44 → 48 → 67 → 83 % with elapsed hours (r = +0.327, p 0.0002) on all 118 — **but on the
§2.18-clean 58 the same correlation collapses to r = +0.044, p 0.7475**, while `upnl_r`'s **strengthens**
to −0.504. **The advisor is tracking the drawdown, not the clock.** The cross-tab makes it plain:

| | `upnl_r` < −0.25R | `upnl_r` ≥ −0.25R |
|---|---|---|
| 0–3 h | **72.7 %** (n=11) | 9.1 % (n=22) |
| 3–6 h | **80.0 %** (n=5) | 30.8 % (n=13) |
| 6–12 h | **100.0 %** (n=8) | 30.4 % (n=23) |
| ≥ 12 h | **94.1 %** (n=17) | 47.4 % (n=19) |

**Drawdown moves the verdict at every age. Age barely moves it at either drawdown.**

---

## §2 — THE MECHANICAL BRANCH, COSTED PROPERLY

**The rule: at exactly H hours after entry, if the running adverse excursion exceeds X × ATR(entry),
close at the 5m close.** Positions already closed by H are untouched — the rule cannot fire on them.
Each counterfactual pays **the position's own actual round-trip fee** in R.

### 2b. 🔴 THE OVERLAP WITH THE 105 EPISODES, RE-MEASURED ON THIS COHORT, STATED BEFORE ANY RESULT

The 105 episodes are **squeeze breakouts on 2.3 years of candles**. This cohort is **the bot's own
40 clean trades**. They are different objects and are not pooled anywhere below.

| a squeeze t0 within … before the entry | of the clean 40 | same-direction |
|---|---|---|
| 12 h | **2 (5.0 %)** | 1 |
| 24 h | 3 (7.5 %) | 2 |
| 48 h | 10 (25.0 %) | 6 |

**Six of the forty.** The 15:15 report's cells — 71 % vs 38 % at h=1, 73 % vs 29 % at h=12, the
lowest p in this book — describe **breakout episodes**, and **six same-direction overlaps is not a
bridge between them and this grid.** Nothing from the episode study is used as evidence for a single
cell below. Everything in §2 is re-measured on the trades.

### 2d. 🔴 n PER CELL, BEFORE ANY RESULT IS QUOTED

**The rule can only fire on a position still open at H.** That ceiling is the real constraint:

| H | alive of 40 | LONG | SHORT |
|---|---|---|---|
| 3 h | **31** | 12 | 19 |
| 6 h | **26** | 9 | 17 |
| 9 h | **18** | 6 | 12 |
| 12 h | **16** | **6** | 10 |

**At H=12 the LONG side of every cell is six positions.** A 12-cell grid on that, before §2e adds
40 more, is the multiplicity problem stated at the top.

### 2a. THE GRID — ACTUAL BOOK **+0.733R**; 11 OF 12 CELLS ARE WORSE

| H | X (ATR) | fired | RULE sum R | **Δ vs actual** | ΔLONG | ΔSHORT | winners cut | their R |
|---|---|---|---|---|---|---|---|---|
| 3 | 0.5 | 25 | −7.183 | **−7.915** | −1.124 | −6.792 | 14 | +13.345 |
| 3 | 1.0 | 22 | −9.570 | **−10.303** | −1.124 | −9.179 | 14 | +13.345 |
| 3 | 1.5 | 20 | −6.172 | −6.905 | −1.124 | −5.781 | 12 | +9.367 |
| 6 | 0.5 | 25 | −4.261 | −4.994 | −2.488 | −2.506 | 16 | +14.308 |
| 6 | 1.0 | 25 | −4.261 | −4.994 | −2.488 | −2.506 | 16 | +14.308 |
| 6 | 1.5 | 22 | −4.153 | −4.886 | −2.488 | −2.397 | 13 | +10.273 |
| 9 | 0.5 | 18 | −3.131 | −3.864 | −1.338 | −2.526 | 12 | +8.949 |
| 9 | 1.0 | 18 | −3.131 | −3.864 | −1.338 | −2.526 | 12 | +8.949 |
| 9 | 1.5 | 17 | −3.228 | −3.961 | −1.338 | −2.623 | 11 | +8.892 |
| **12** | **0.5** | 16 | +0.887 | 🟡 **+0.154** | 🔴 **−0.913** | +1.067 | **11** | **+8.892** |
| **12** | **1.0** | 16 | +0.887 | 🟡 **+0.154** | 🔴 **−0.913** | +1.067 | 11 | +8.892 |
| **12** | **1.5** | 16 | +0.887 | 🟡 **+0.154** | 🔴 **−0.913** | +1.067 | 11 | +8.892 |

**One of twelve cells is positive at all, by +0.154R on a 40-position book — and it fails the
operator's own gate on the first clause: it loses on the LONG side.**

### 🔴 2a-MECHANISM — THE THRESHOLD IS NOT DOING ANY WORK. THIS IS A PURE TIME STOP.

Notice that at H=6, X=0.5 and X=1.0 give **identical** results; at H=12 all three do. That is not a
coincidence to be noted and moved past — it is the whole mechanism:

| H | alive | > 0.5 ATR | > 1.0 ATR | > 1.5 ATR | median adverse | p25 | p75 |
|---|---|---|---|---|---|---|---|
| 3 h | 31 | 25 (81 %) | 22 (71 %) | 20 (65 %) | **2.93 ATR** | 0.93 | 4.20 |
| 6 h | 26 | 25 (96 %) | 25 (96 %) | 22 (85 %) | **3.46 ATR** | 1.80 | 5.57 |
| 9 h | 18 | 18 (100 %) | 18 (100 %) | 17 (94 %) | **4.11 ATR** | 3.26 | 7.55 |
| **12 h** | 16 | **16 (100 %)** | **16 (100 %)** | **16 (100 %)** | **4.11 ATR** | 3.26 | 9.33 |

🔴 **By 12 hours EVERY surviving position has already travelled more than 1.5 ATR against itself.
The threshold selects nobody.** What the H=12 row measures is **the clock alone** — the excursion
condition is decorative. This is §2.45b's shape exactly: *a value that is computed, stored and
displayed but reaches no `if`*, except here the `if` exists and is always true.

**And that matters for the one positive cell: it is not "close the ones that are failing", it is
"close everything still open at 12 hours".** Which is a time stop, and the objection below is aimed
precisely at it.

### 2c. 🔴 THE OBJECTION THAT DECIDES IT — TESTED, AND IT IS THE RESULT

The operator's condition was not the failure rate but **how many eventually-profitable positions the
rule closes, and their total R.** At the only positive cell, H=12:

| | |
|---|---|
| positions the rule closes | **16** |
| 🔴 of which were **eventually profitable** | **11** |
| 🔴 their **actual** total | **+8.892R** |
| what the rule leaves of that | **+6.489R** |
| 🔴 **R handed back on winners alone** | **−2.403R** |
| positions improved by the rule | 9 |
| positions damaged by the rule | 7 |
| largest single improvement | **+1.040R** |
| largest single damage | **−2.871R** |
| **net** | **+0.154R** |

**Eleven of the sixteen positions this rule closes were winners.** It buys its +0.154R by cutting
+2.403R off them and recovering slightly more elsewhere. **Paired bootstrap over the 40 positions,
20 k draws: 95 % CI on Δ = [−8.104, +7.005]R, 45.8 % of draws below zero.** There is no effect here.

**Every other cell in the grid cuts more winners for a worse result** — 10 to 17 winners worth +5.7R
to +14.3R, for Δ between −2.4R and −10.3R.

**The time stop cuts winners that are merely slow. That was the stated risk. It is what happened.**

---

## §2e — THE SECOND NORMALISATION: RETRACEMENT AS A FRACTION OF THE MOVE

### 🔴 THE OBJECTION, IN THE HEADER, UNSOFTENED

**The levels are arbitrary. No mechanism makes 0.618 different from 0.60.** Seventeen branches have
died in this book and several looked more principled than this one — §2.45's ten, §2.45b's two
asserted mechanisms, the 14:55 report's six, and the 15:15 report's box, which turned out to be an
algebraic restatement of a quantity the bot already had. **This is measured because the operator
named it and because §2e(a) makes it cheap to falsify, not because it has a prior.**

⚠️ **And it adds 40 cells (16 Fibonacci + 24 even-grid) to an already-overspent budget. Every hit
below is NOMINAL.** There are no hits.

### 2e(c) — CAN IT EVEN FIRE? THE DENOMINATOR HAS TO EXIST FIRST

| H | alive | MFE == 0 → **rule INERT** | 0 < MFE < 0.10R → **denominator is noise** | MFE ≥ 0.25R → usable |
|---|---|---|---|---|
| 3 h | 31 | 0 | 6 | **23** |
| 6 h | 26 | 0 | 5 | **19** |
| 9 h | 18 | 0 | 2 | **14** |
| 12 h | 16 | 0 | 1 | **14** |

**This one passes.** Every surviving position has a non-zero MFE at every horizon, and 74–88 % have
a usable one. **The rule is not inert — it is simply wrong**, which is a cleaner death.

### 2e — THE TWO GRIDS, RUN IN THE SAME PASS

**Fibonacci levels:**

| H | 0.382 | 0.500 | 0.618 | 0.786 |
|---|---|---|---|---|
| 3 h | −8.141 (n=28) | −4.743 (n=26) | −6.678 (n=22) | −9.176 (n=17) |
| 6 h | −4.280 (n=17) | −4.280 (n=17) | −4.280 (n=17) | −4.287 (n=15) |
| 9 h | −2.632 (n=14) | −2.856 (n=13) | −2.525 (n=12) | −3.202 (n=9) |
| 12 h | −2.854 (n=11) | −3.718 (n=10) | −3.718 (n=10) | **−2.413** (n=7) |

**Even grid:**

| H | 0.30 | 0.40 | 0.50 | 0.60 | 0.70 | 0.80 |
|---|---|---|---|---|---|---|
| 3 h | −7.737 | −8.141 | −4.743 | −5.833 | −9.140 | −9.176 |
| 6 h | −4.513 | −4.280 | −4.280 | −4.280 | −4.280 | −4.287 |
| 9 h | −2.632 | −2.632 | −2.856 | −2.525 | −2.623 | −3.202 |
| 12 h | −2.505 | −2.854 | −3.718 | −3.718 | −2.972 | **−2.413** |

🔴 **ALL 40 CELLS ARE NEGATIVE.** The best of them, −2.413R, is worse than doing nothing by more
than three times the entire book's realised profit.

### 2e(a). 🔴 THE HONEST TEST: ARE THE FIBONACCI NUMBERS DISTINGUISHABLE FROM THEIR NEIGHBOURS?

| H | Fib | neighbour | Fib Δ | nbr Δ | Fib n | nbr n | |
|---|---|---|---|---|---|---|---|
| 3 | 0.382 | 0.400 | −8.141 | −8.141 | 28 | 28 | 🔴 **IDENTICAL** |
| 3 | 0.618 | 0.600 | −6.678 | −5.833 | 22 | 24 | differs |
| 3 | 0.786 | 0.800 | −9.176 | −9.176 | 17 | 17 | 🔴 **IDENTICAL** |
| 6 | 0.382 / 0.618 / 0.786 | 0.400 / 0.600 / 0.800 | — | — | — | — | 🔴 **IDENTICAL ×3** |
| 9 | 0.382 / 0.618 / 0.786 | 0.400 / 0.600 / 0.800 | — | — | — | — | 🔴 **IDENTICAL ×3** |
| 12 | 0.382 / 0.618 / 0.786 | 0.400 / 0.600 / 0.800 | — | — | — | — | 🔴 **IDENTICAL ×3** |

*(0.500 appears in both grids and is trivially identical at all four H — counted, not credited.)*

🔴 **15 of 16 Fibonacci levels select EXACTLY the same positions, the same n and the same R as the
plain decimal beside them.** The single exception (H=3, 0.618 vs 0.600) differs by two positions and
is **worse**. **The numbers themselves carry nothing.** They are not a level in this data; they are a
label on an interval that happens to contain no position boundaries.

**That is the answer to the operator's own question, and it cost one extra grid to get.**

### 2e(b). 🔴 THE COMPARISON THAT DECIDES: MOVE-NORMALISED vs ATR-NORMALISED, SIDE BY SIDE

| form | best cell | n fired | **Δ vs actual** | ΔLONG | ΔSHORT |
|---|---|---|---|---|---|
| **ATR-normalised** (adverse ÷ ATR) | H=12 h, X=0.5 | 16 | **+0.154R** | −0.913 | +1.067 |
| **move-normalised** (retracement ÷ MFE) | H=12 h, X=0.786 | 7 | **−2.413R** | −0.006 | −2.407 |

**The ATR form beats the move-normalised form by +2.567R at each one's own best cell.**

🔴 **THE SECOND NORMALISATION ADDS NOTHING, AND THE SIMPLER MEASURE WINS.** The premise was sound —
a 1-ATR pullback from a 1-ATR move and from a 5-ATR move genuinely are different events, and the
book really is blind to that. **The gap is real; filling it does not help.** That is a fair test of
a fair objection, and it comes back negative.

*(And the simpler measure is itself worthless — see §2c. "Wins the comparison" here means "is less
bad".)*

---

## §3 — VERDICT

### 🔴 NEITHER BRANCH SURVIVES. NO DIFF, AND THE REASON IS EVIDENCE, NOT FATIGUE.

Taking the operator's three conditions in the order they were written:

| §3 condition | fired? | why |
|---|---|---|
| **§2 or §2e beats the actual book on BOTH sides, ≥8 positions affected, surviving 2c** | 🔴 **NO** | **0 of 52 cells.** The only positive cell (+0.154R) loses on LONG (−0.913R), has a bootstrap CI of [−8.10, +7.01]R, and closes 11 winners worth +8.892R. Its threshold is inert — it is a time stop |
| **§1 shows the advisor blind to drawdown AND the prompt lacks age → add age as a FACT** | 🔴 **NO, TWICE** | The advisor is the **opposite** of blind (r = −0.398 / −0.504, p < 0.0001, survives the regime control on 90 consults). And the prompt **has carried age since `ef7fa10`, 2026-07-26** — `Elapsed: {h}h`, on 118 of 118 prompts, quoted back in 25 reasons |
| **Neither survives → say so plainly** | ✅ **THIS ONE** | Said plainly above |

### 🔴 WHAT THE 15:15 REPORT ACTUALLY GOT WRONG, NAMED PRECISELY

The 15:15 report wrote *"the advisor is already given this quantity"* and stopped. The operator was
right that **being given** and **acting on** are different, and right that neither had been measured.

**But the measurement does not reverse the 15:15 conclusion — it hardens it.** The advisor is given
adverse movement in R, and it **acts on it more strongly than on anything else in its prompt.** The
sentence the 15:15 report stopped at turns out to have been a sufficient reason to stop, arrived at
without the evidence that made it sufficient. **The error was the epistemics, not the call**, and
that distinction is worth keeping because next time the call may go the other way.

### 🔴 THE THING WORTH CARRYING FORWARD, AND IT IS NOT A RULE

**§2's failure and §1's success are the same fact seen twice.** A mechanical clock-tier fails because
at 12 hours *every* open position is deep in adverse excursion — the quantity has no variance left to
discriminate with. **The advisor succeeds on the same quantity because it reads it continuously, in R,
against the position's own stop, alongside the giveback and the regime — and closes at −0.5R rather
than waiting for hour twelve.** The bot already has the multi-hour drawdown reaction the brief went
looking for. **It is the exit advisor, and it is the only measured positive in this system**
(+3.3729R over five closed positions, §2.4 closed at 5 of 10 on 2026-08-04).

⚠️ **What would change this, and it is the same answer as §2.45 and §2.47: live-era closed positions
on the CURRENT geometry.** The clean book is **40, all of them pre-boundary, 34 of them paper at 68×
the live notional, and ZERO on the SL-2.25/trail-0.75R machine now running.** Any grid fitted here is
fitted to a bot that was retired on 2026-08-04 at 17:01:29.

### 🔴 EIGHTEENTH AND NINETEENTH DEAD BRANCHES, FOR §2.45's LIST

| # | branch | verdict |
|---|---|---|
| 17. | **time-conditioned adverse excursion as a recheck tier** (H × ATR) | 🔴 **dead.** 11 of 12 cells worse than doing nothing; the survivor loses on LONG, cuts 11 winners worth +8.892R, CI spans zero. **And its threshold is inert — it is a time stop, not an excursion rule** |
| 18. | **retracement ÷ MFE at Fibonacci levels** | 🔴 **dead, and dead twice over.** All 40 cells negative; **15 of 16 Fibonacci levels are numerically identical to their plain decimal neighbours**; and the normalisation **loses to the ATR form it was meant to improve** |

### 🔴 NOTHING IS PROPOSED, AND NO DIFF IS ATTACHED

No recheck tier, no prompt field, no config, no schema, no threshold. `titan-bot` unmodified at
`b9081ad`, `git status` clean, 0 open positions throughout, `trades.db` read-only.

**§3's second branch asked for a diff adding position age as a fact. That diff would be a no-op:
the fact is already on the prompt.** Writing it anyway would be adding a line the model already has,
to an instrument whose only measured positive is n=5 — the precise shape of change §3b of the 15:15
report warned about.

---

## LIVE STATE, AS OF THIS REPORT

| | |
|---|---|
| open positions | **0** |
| `EXIT_ADVISOR_DRYRUN` | `False` — **the advisor is ACTING** (`config.py:278`) |
| exit consults ever | **118** (last: 2026-08-04 00:26) |
| 🔴 `ema_envelope_blocked` rows (§2.47's FAST TRIGGER needs **n ≥ 100**) | **19** |
| clean closed positions on the post-17:01:29 geometry | 🔴 **0** |

*(The envelope count is carried because §2.47's rule is "count refusal rows, never days". 19 of 100
is the honest position; the gate is no longer at zero, and nothing here touches it.)*

---

## APPENDIX — WHAT WAS RUN

| file | purpose | cells |
|---|---|---|
| `s1_consults.py` | §1a/§1b: all 118 prompts parsed from `ai_user_prompt`; close rate vs `upnl_r`, `mfe_r`, `giveback_r`, `dist_sl_r`, `elapsed_h`, pooled and §2.18-clean; the age × drawdown cross-tab | 15 |
| `s1c_reasons.py` | §1c: category tally over the verbatim `ai_reason`; mutually-exclusive lead-clause analysis; the duration-citation count with timeframe tokens excluded | — |
| *(inline)* | §1a-control: §2.54's method — close rate vs drawdown stratified by the live 15m/5m regime parsed out of the prompt | 8 |
| `fetch_candles.py` | 22,095 BingX 5m bars, 2026-05-21 → 2026-08-05, **zero gaps** | — |
| `s2_engine.py` | §0 cohort + replay validation; §2b overlap; §2a ATR grid; §2e Fibonacci and even grids; §2e(c) MFE existence; §2c winner accounting | 52 |
| `s3_diag.py` | the adverse-excursion distribution that explains the inert threshold; §2e(a) Fibonacci-vs-neighbour; §2e(b) head-to-head; the paired bootstrap; the SL-validation mismatch | 2 |

**Total cells spent: 77.** Permutation tests are 20,000 shuffles, two-sided, seed 20260805;
the bootstrap is 20,000 paired resamples over positions, same seed.

*Read-only. `trades.db` opened read-only throughout; `titan-bot` unmodified at `b9081ad`;
0 open positions for the entire pass. Mercury-SOL never opened.*
