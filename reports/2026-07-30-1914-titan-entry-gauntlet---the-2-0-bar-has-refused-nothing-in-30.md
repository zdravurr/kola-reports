# titan entry gauntlet - the 2.0 bar has refused nothing in 30 days

_2026-07-30 19:14 UTC_

---

# titan-entry-gauntlet-the-2.0-bar-has-refused-nothing-in-30-days

_2026-07-30 19:10 UTC_

---

# TITAN — 🔴 **THE 2.0 BAR HAS NEVER REFUSED A SINGLE SIGNAL. THE FLAT FLOOR DOES 76% OF THE WORK.**

_HEAD `1161802` · clean · 🔴 LIVE, REAL MONEY · $30 × 5 = $150 notional · vpos 87 LONG **open**, stop 64028.8 · service active_

**READ-ONLY. Nothing was changed, nothing is proposed.** Seven questions, answered with the numbers
attached and n stated in every cell.

---

## DECISION LINE

**The premise you handed me is right in mechanism and wrong in magnitude, and the correction makes the
picture worse, not better.**

`CONFLUENCE_SCORE_THRESHOLD = 2.0` is not merely a low bar — **it is unreachable.** The minimum raw
`direction_score` observed in a TREND regime over 1,533 scored events in 30 days is **2.25**. A TREND
signal has *never* scored below 2.0, so the constant has refused **zero** signals on its own merit in
the entire 30-day window. The 27 TREND refusals that do exist were caused **entirely** by
`macro_filter`'s −1.0 news penalty dragging a 2.25/2.5 under the bar. Remove the news penalty and the
score gate's TREND refusal count is **0 of 940**.

**What actually refuses on score is `CONFLUENCE_FLAT_THRESHOLD = 5.0` — 450 of 593 refusals (75.9%).**
The constant you filed as "binds only when `market_regime == 'FLAT'`" is doing three-quarters of the
gate's work, on a variable that is signal *presence* rather than a measurement.

**And a fourth signal that cannot stop a trade joins your list of four:** `dxy_halt` is behind
`DXY_HALT_DRYRUN = True`. It printed **16 would-blocks** in the ~2.7 days of journal that survive
retention and blocked nothing. A fifth: `FILTER_ENFORCEMENT_DRYRUN = True` mutes the enforcement-
extension filters the same way.

**The curve you asked for has a shape and it is monotone up to 5.0, then flat.** On the 11 clean closed
trades, net R goes **−2.88 → −1.69 → +0.31 → +0.36 → +0.12** at bars 2.0/3.0/4.0/5.0/7.0, while n
kept falls **11 → 10 → 5 → 3 → 1**. The whole gain is bought by refusing six trades at the 4.0 step.
**I am not recommending a level. n=5 is not a mandate.**

**§6 returned a genuinely new measurement and it killed its own hypothesis in a way I did not expect.**
There is no "late entry" cohort to compare against, because **every entry in the history is late by
this measure.** 23 of 23 sit in the adverse half of the prior 24h range; 22 of 23 above 0.75. The
variable has no variance. It is not a re-open of §4.3 (r = −0.26 against prior-move), and it is not a
finding either — it is a **description of what the strategy is**.

**One correction to the 13:09 narrative, from its own data.** On the clean cohort the intra-conflict
subgroup where the silenced side *opposed* the trade is **n=3, −0.43R**. The subgroup where the
silenced side *agreed* is **n=4, −2.87R**. The damage is not where the vpos-87 story put it.

---

## 1 · WHAT ACTUALLY GATES AN ENTRY, END TO END

Traced on `main.py:3672–4030`, the JSON state-machine 5m path — the one vpos 86 and vpos 87 took.
Two mirrors exist (`:1879` plain-text 5m, `:4196` direct P3 webhook); every score/HTF/risk gate below
is duplicated verbatim in both. Counts are `trades.status` over the last 30 days.

| # | gate | what it tests | value vs constant | can REFUSE? | refusals, 30d |
|---:|---|---|---|:---:|---:|
| 0 | `/webhook` parse + classify | signal text → category/direction | `signal_matrix.classify` | routing only | `context_recorded` **1650**, `trend_set` 122, `trend_reset` 12 |
| 1 | `confluence_check` *(plain-text path only)* | persistent 1H/15m slots agree | `state_machine` slots | ✅ | **0** |
| 2 | 🔴 **`_htf_cascade_gate`** | 1H TREND · 15m MOMENTUM · 5m tier vs trigger direction | `HTF_CASCADE_ENABLED=True`, `HTF_TOLERATE_NEUTRAL=True`, `HTF_NEUTRAL_REQUIRE_15M_AGREE=True` | ✅ | 🔴 **4077** |
| 3 | 🔴 **score gate** | `direction_score + total_gate_adj` | `< 5.0` if regime FLAT else `< 2.0` | ✅ | **593** |
| 4 | `_filter_match` | operator kill-list patterns | `original_only=True`; extension muted by `FILTER_ENFORCEMENT_DRYRUN=True` | ✅ / muted | **0** (0 dry-run would-blocks in journal) |
| 5 | `insert_signal` | DB row written before any order | `row_id is None` → HTTP 500 | ✅ (fail-closed) | 0 |
| 6a | `macro_event_halt` | now within ±30 min of a high-impact calendar event | `MACRO_BLACKOUT_MINUTES=30`, 20 events | ✅ | **3** |
| 6b | `dxy_halt` | DXY STRONG_UPTREND vs LONG / DOWNTREND vs SHORT | 🔴 `DXY_HALT_DRYRUN=True` | ❌ **muted** | **0** — 16 would-blocks logged since 07-27 22:50 |
| 6c | `daily_loss_halt` | today's realised PnL / equity | `≤ −DAILY_LOSS_PCT_LIMIT` = −5% | ✅ | **0** |
| 6d | `concurrent_position_halt` | exchange positions on the requested side | `≥ MAX_POSITIONS_PER_SIDE = 1` | ✅ | **36** |
| 6e | `loss_streak_halt` | last 3 closes all losers within 4h | `LOSS_STREAK_THRESHOLD=3`, cooldown 4h | ✅ | **0** |
| 7 | 🔴 **`claude_advisor.consult_for_entry`** | LLM verdict on the full prompt | `decide == 'skip'` | ✅ | 🔴 **831** |
| 7a | Claude unavailable, low score | `direction_score < 7.5` | `FALLBACK_SCORE_THRESHOLD = 7.5` | ✅ | **1** |
| 7b | Claude unavailable, flat market | `srv_adx_1h < 20` **and** regime FLAT | `ADX_FLAT_FLOOR = 20.0` | ✅ | **0** |
| 8 | `virtual_trader.open_position` cap | open rows on this side | `≥ MAX_POSITIONS_PER_SIDE = 1` | ✅ | **39** (`virt_cap_blocked`) |
| 8a | `_UNSAFE_STATE` breaker | in-process unsafe-state trip | boolean | ✅ | 0 |
| 9 | order placement | exchange min notional / exception | `create_market_order` raises | ✅ | **2** (`failed`) |
| 10 | 🔴 stop placement | 3× retry, then emergency close, **no row written** | `[SL-FAILSAFE]` | ✅ | 0 |

### The refusal ledger, ranked

```
htf_blocked       4077   ← 72.7% of all refusals
ai_skipped         831   ← the LLM is the second-largest gate
below_threshold    593   ← of which 450 are the FLAT floor, 27 the macro penalty, 116 both
virt_cap_blocked    39
risk_halt           39   ← 36 position-cap, 3 macro-calendar
claude_unavailable   1
failed               2
─────────────────────
filtered             0    no_confluence 0    bypass_flat_skipped 0    dxy_halt 0 (muted)
```

🔴 **Two structural readings of that ledger.**

1. **The two gates that do 93% of the refusing are the two that are not the score gate.** The HTF
   cascade and the LLM. The score is a rounding error in refusal volume.
2. **Four of the sixteen gates have never refused anything, and two of those are switched off by a
   dry-run flag rather than by a threshold.** `dxy_halt` and the filter extension are not "quiet" —
   they are muted. That is the same class of defect as your four: a signal that exists, is computed,
   and cannot stop a trade.

### 🔴 The score gate's arithmetic, restated exactly (`main.py:3679–3691`)

```python
direction_score = signal_matrix.score_for_direction(matrix_result, direction)
_macro_gate_adj = macro_filter.build_macro_context(direction)['total_gate_adj']
_gated_score    = round(direction_score + _macro_gate_adj, 2)
_eff_thr        = (CONFLUENCE_FLAT_THRESHOLD              # 5.0, only if regime == 'FLAT'
                   if matrix_result.get('market_regime') == 'FLAT'
                   else CONFLUENCE_SCORE_THRESHOLD)       # 2.0
if _gated_score < _eff_thr:  ...refuse
```

**`thr = 4.0` on the card is `LIQUIDITY_HEATMAP_TREND_THRESHOLD`.** Its only consumers are
`signal_matrix.format_for_telegram:551` and the `trade_signal_matrix` snapshot row. Confirmed again
here: it is compared to nothing.

### 🔴 THE LOAD-BEARING NUMBER OF THIS WHOLE REPORT

**The 2.0 bar is not low. It is out of reach.** Over 1,533 scored events in 30 days that had a
proposed direction (htf_blocked rows excluded, because their stored breakdown is *penalised* and would
corrupt the distribution):

```
minimum raw direction_score, regime TREND :  2.25   <-- never once below 2.0
minimum raw direction_score, regime FLAT  :  1.75   <-- and FLAT is judged at 5.0, not 2.0
raw direction_score < 2.0                 :  137 events, ALL of them FLAT
```

The floor of the score distribution is **2.25**, because a single category contributes up to 2.5 and
the trigger that fires the webhook is itself a scoring signal. **`CONFLUENCE_SCORE_THRESHOLD` cannot
bind in the regime where it is the active constant.**

### History of the constant, from the commits

| date | commit | value |
|---|---|---|
| 2026-05-11 | `adc44bc` *add Global Confluence Dictionary — score-based entry gate* | **7.0** |
| 2026-05-12 | `cf6fed8` *cross-link virtual_positions↔trades; lower threshold; exit bypass* | 7.0 → **5.0** |
| 2026-05-20 | `645a211` *feat(titan): lower confluence score gate 5.0→2.0 (virtual experiment)* | 5.0 → 🔴 **2.0** |
| 2026-07-06 | `db71454` *fix(titan): enforce FLAT-regime score floor (5.0); TREND stays 2.0* | FLAT floor added |

Your account is exact: the 7.0 → 5.0 step is buried inside a three-subject commit, the 5.0 → 2.0 step
is labelled a virtual experiment, and neither was reverted.

---

## 2 · THE SCORE BAR — WHAT EACH LEVEL WOULD COST

**Cohort.** All five §0 filters applied: `t.timestamp >= '2026-07-04 11:58'` (forming-candle),
lifetime-overlap wall-trail exclusion, `recheck_status <> 'tightened'`, R used throughout (which
normalises the $10,000 paper book against the $150 live one), and real candles rather than stored
extrema wherever price paths are involved. **Clean closed cohort n = 11** — the same 11 as the 13:09
report, and it has not grown: vpos 86 is `tightened` and excluded, vpos 87 is still open.

The replay recomputes `direction_score` from each row's stored `matrix_breakdown_json` and adds the
stored `macro_gate_penalty`. **Reconstruction verified: 23 of 23 executed entries reproduce their
stored `confluence_score` to the cent, 0 mismatches.**

### a) What each level would have refused — clean closed cohort, n = 11

| bar | refused n | refused wins | refused totR | kept n | kept wins | **kept totR** | Δ vs 2.0 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| **2.0** (today) | 0 | 0 | +0.000 | **11** | 5 | 🔴 **−2.882** | — |
| 3.0 | 1 | 0 | −1.197 | 10 | 5 | −1.685 | **+1.197** |
| 4.0 | 6 | 2 | −3.190 | **5** | 3 | 🔴 **+0.309** | **+3.190** |
| 5.0 | 8 | 3 | −3.241 | 3 | 2 | **+0.359** | +3.241 |
| 7.0 | 10 | 4 | −3.004 | **1** | 1 | +0.122 | +3.004 |

**Per side.** LONG n=6, SHORT n=5.

| bar | LONG refused | LONG kept totR | SHORT refused | SHORT kept totR |
|---:|---|---:|---|---:|
| 2.0 | 0 | −0.726 | 0 | −2.156 |
| 3.0 | 1 (0 wins, −1.197) | +0.471 | 0 | −2.156 |
| 4.0 | 3 (1 win, −1.781) | **+1.055** | 3 (1 win, −1.410) | −0.747 |
| 5.0 | 4 (2 wins, −0.742) | +0.016 | 4 (1 win, −2.499) | **+0.343** |
| 7.0 | 5 (2 wins, −0.848) | +0.122 | **5 (2 wins, −2.156)** | **+0.000 — no SHORT survives** |

Exactly which trades each bar removes:

```
bar 3.0  vpos78(L g2.50 R-1.20)
bar 4.0  + vpos77(S 3.25 -1.09)  vpos79(L 3.25 +0.50)  vpos80(S 3.00 -1.09)
           vpos81(S 3.50 +0.77)  vpos85(L 3.25 -1.09)
bar 5.0  + vpos82(L 4.00 +1.04)  vpos83(S 4.25 -1.09)
bar 7.0  + vpos75(L 5.00 -0.11)  vpos76(S 6.00 +0.34)
```

### b) How many currently-refused signals would each level ADMIT?

🔴 **Zero. At every level tested. The question has an empty answer and the reason is structural.**

Raising `CONFLUENCE_SCORE_THRESHOLD` can only add refusals; it can never admit. And the FLAT branch is
untouched by the constant, so of the 593 refusals in 30 days:

| refused by | n | affected by raising the TREND bar? |
|---|---:|---|
| **FLAT floor 5.0** (regime FLAT, gated ≥ 2.0) | **450** | no — judged against `CONFLUENCE_FLAT_THRESHOLD` |
| FLAT **and** gated < 2.0 (both would refuse) | 116 | no |
| TREND bar 2.0 | **27** | already refused; stays refused |

Regime was reconstructed from each refused row's stored breakdown (`TREND` category
`net_direction != NEUTRAL`), because `market_regime` is **not written on the below_threshold branch** —
only `_shared_update_kwargs` on the executed path carries it. **Validation: 0 of 593 rows contradict
the reconstructed rule.**

🔴 **A structural inversion that becomes live at any bar above 5.0.** At 7.0 the FLAT floor stops being
a floor and becomes a **discount**: a FLAT-regime signal at 5.5 would pass while a TREND-regime signal
at 5.5 would be refused. Observed rows that would flip: **0** — the highest score in the refused
population is 4.75. It is a construction defect waiting rather than an active one.

**What the refused population is worth, via skip-drift.** Sign convention per §0: **positive = the
skipped signal would have won.** Baseline: the unconditional 24h forward drift over the same span is
**+0.125%** (2,524 rolling 15m windows) — a LONG skip drifts positive by that much for free, so the
raw column is de-confounded in the second one.

| refusal | 15m | 1h | 4h | 12h | 24h | 24h LONG (adj) | 24h SHORT (adj) |
|---|---:|---:|---:|---:|---:|---:|---:|
| below_threshold (n=593) | +0.007% | +0.024% | −0.063% | +0.071% | +0.164% | **+0.209%** (n=257) | +0.156% (n=330) |
| ai_skipped (n=831) | −0.008% | −0.012% | −0.023% | +0.246% | +0.230% | 🔴 **+0.715%** (n=358) | −0.110% (n=469) |
| htf_blocked (n=4076) | +0.000% | +0.002% | +0.024% | −0.018% | −0.057% | +0.238% (n=1838) | 🔴 **−0.291%** (n=2143) |

By score band, 24h horizon, below_threshold only:

| band | n | 24h mean drift |
|---|---:|---:|
| < 2.0 | 142 | +0.100% |
| 2.0–3.0 | 93 | 🔴 **−0.324%** — these refusals were RIGHT |
| 3.0–4.0 | 188 | 🔴 **+0.463%** — these refusals were WRONG |
| 4.0–5.0 | 164 | +0.151% |

**Read that carefully before it is used as an argument for raising the bar: the band the FLAT floor
refuses most (3.0–4.0, n=188) is the band whose refusals look most costly.** Raising the TREND bar
does not touch those rows — but any thought of raising the FLAT floor runs straight into this number.

### c) Net R at each level versus today — the shape, not a proposal

```
kept net R, clean closed cohort (n falls 11 → 10 → 5 → 3 → 1)

 +0.5 |                    ●4.0      ●5.0
      |                   +0.31     +0.36
  0.0 |------------------------------------●7.0-------
      |                                    +0.12
 -1.0 |          ●3.0
      |         -1.69
 -2.0 |
      | ●2.0
 -3.0 | -2.88
      +----+-------+--------+--------+--------+
         2.0     3.0      4.0      5.0      7.0
   n:    11      10        5        3        1
```

**The shape: monotone improvement to 4.0, essentially flat 4.0 → 5.0, decaying at 7.0.** Every point
right of 3.0 rests on n ≤ 5. The contaminated 22-trade cut (moved stops included, reported labelled
rather than laundered) has the same shape and never crosses zero: −7.20 → −5.77 → −2.19 → −1.55 → −0.77.

🔴 **Three caveats that limit every cell above, stated so the curve is not over-read.**

1. **n is 11.** At bar 4.0 the entire positive result is five trades, and **one of them — vpos 82 at
   +1.04R — is more than three times the whole +0.31R kept total.** Drop that single trade and bar 4.0
   returns −0.73R over n=4.
2. 🔴 **Refusing a trade is not a no-op — it frees the position cap.** `MAX_POSITIONS_PER_SIDE = 1`,
   and the cap refused **36** entries in 30 days. Every replay above assumes the refused trade simply
   vanishes. In reality some of those 36 would have become trades, with unknown outcomes. **The replay
   is an upper bound on the benefit, not an estimate of it.**
3. **The bar never bound.** These are counterfactuals over a population selected by *other* gates
   (HTF, LLM). A score bar that had actually been in force would have changed which signals reached
   the LLM at all.

---

## 3 · INTRA-CONFLICT — IS ZEROING THE DISSENT RIGHT OR WRONG?

**The mechanism, verbatim (`signal_matrix.py:346–352`):**

```python
intra_conflict = lp > 0 and sp > 0
if intra_conflict:
    net_dir     = NEUTRAL
    contribution = 0.0
```

🔴 **Zeroing has a second-order effect nobody has written down.** Setting `net_direction = NEUTRAL`
also removes the category from the **inter-category majority vote** at `:368–376`. A silenced category
does not merely lose its 2.5 points — it loses its **vote on which side is the minority**, and the
minority side is then zeroed as well. One rule, two amputations.

### a) How often does a category get zeroed?

Two cuts, because `htf_blocked` rows store a **`−HTF_PENALTY`-adjusted** breakdown, which can
manufacture or destroy conflicts. The un-penalised cut is the honest one.

**Un-penalised (1,532 scored rows, htf_blocked excluded) — 905 of 1,532 (59.1%) carry ≥1 conflict:**

| category | present | zeroed | rate | dominant AGREES with trade | dominant **OPPOSES** | exact tie |
|---|---:|---:|---:|---:|---:|---:|
| TREND | 689 | 59 | 8.6% | 11 | 24 | 24 |
| MOMENTUM | 1391 | 303 | 21.8% | 14 | **84** | 205 |
| **LIQUIDITY** | 1139 | **430** | 🔴 **37.8%** | 127 | **170** | 133 |
| EXECUTION | 1532 | 474 | 30.9% | 155 | 93 | 226 |

**All 5,610 scored rows (htf_blocked breakdowns are penalised — for reference only):** 3,601 of 5,610
(64.2%) carry ≥1 conflict; MOMENTUM 1808 zeroed (36.4%), LIQUIDITY 1545 (38.2%), EXECUTION 1624
(28.9%), TREND 246 (9.4%).

**Answers.** **LIQUIDITY is zeroed most by rate (37.8%)**; MOMENTUM is zeroed most in absolute count on
the full cut. **Across all four categories the dominant side of a silenced category opposes the trade
more often than it agrees** — 371 opposed vs 307 agreed on the un-penalised cut. The rule
preferentially deletes dissent, but not overwhelmingly, and 588 of the 1,266 conflicts are exact ties
where "the zeroed side" is not a meaningful object.

### b) Clean closed trades — zeroed-and-opposed vs no-conflict

Every clean closed trade, with its silenced categories:

```
vpos 75 LONG  R-0.106 g5.00  EXECUTION(L1.25/S1.75 → SHORT, opposes)
vpos 76 SHORT R+0.343 g6.00  — none —
vpos 77 SHORT R-1.087 g3.25  MOMENTUM(L1.75/S2.50 → SHORT, agrees); EXECUTION(1.75/1.75 tie)
vpos 78 LONG  R-1.197 g2.50  MOMENTUM(1.75/1.75 tie); EXECUTION(L2.50/S1.75 → LONG, agrees)
vpos 79 LONG  R+0.503 g3.25  EXECUTION(2.00/2.00 tie)
vpos 80 SHORT R-1.092 g3.00  MOMENTUM(L2.50/S1.75 → LONG, opposes)
vpos 81 SHORT R+0.770 g3.50  MOMENTUM(L2.50/S1.75 → LONG, opposes); EXECUTION(L1.75/S2.50 → SHORT, agrees)
vpos 82 LONG  R+1.039 g4.00  — none —
vpos 83 SHORT R-1.090 g4.25  — none —
vpos 84 LONG  R+0.122 g8.50  — none —
vpos 85 LONG  R-1.087 g3.25  LIQUIDITY(L1.75/S1.25 → LONG, agrees); EXECUTION(L2.50/S2.00 → LONG, agrees)
```

| cohort | n | wins | totR | meanR | medR |
|---|---:|---:|---:|---:|---:|
| zeroed **and the zeroed side OPPOSED** | **3** | 1 (33%) | **−0.428** | −0.143 | −0.106 |
| zeroed, but the zeroed side AGREED / tie | **4** | 1 (25%) | 🔴 **−2.868** | −0.717 | −1.087 |
| **ANY** category zeroed | 7 | 2 (29%) | −3.296 | −0.471 | −1.087 |
| **NO** category zeroed | **4** | 3 (75%) | **+0.414** | +0.104 | +0.233 |

Per side — LONG opposed n=1 (−0.106), LONG agreed/tie n=3 (−1.781), LONG clean n=2 (+1.161);
SHORT opposed n=2 (−0.322), SHORT agreed/tie n=1 (−1.087), SHORT clean n=2 (−0.747).

**The 13:09 MOMENTUM cut, re-run: it has not moved.** Conflict **n=4** (1 win, −2.606R) vs clean
**n=3** (2 wins, +0.740R) vs absent n=4 (2 wins, −1.015R). **Identical to 13:09, because no clean
closed trade has been added since** — vpos 86 is excluded as `tightened`, vpos 87 is open. The 4-vs-3
direction holds because it is literally the same four and three trades.

🔴 **And here is the correction the data forces on the vpos-87 narrative.** The 13:09 report framed the
harm as *"the rule removed the trade's only internal dissent."* On the clean cohort the **opposed**
subgroup is the *least* damaged of the three (−0.43R over 3), and the damage concentrates in
**agreed/tie** (−2.87R over 4). What survives is the cruder statement: **conflict of any kind, in any
direction, marks bad trades — 7 at −3.30R against 4 at +0.41R.** The directional refinement does not.

For the record, vpos 87's own two silenced categories, from `trades.19713.matrix_breakdown_json`:
**MOMENTUM** L1.75/S2.50 → dominant SHORT, **opposes** the LONG; **LIQUIDITY** L2.50/S1.25 → dominant
**LONG**, *agrees* with it. **One of the two, not both.** The 13:09 text said "both … leaned toward the
SHORT side" and then hedged the second as "mixed"; measured by dominant side, it agreed.

### c) What HALVING instead of zeroing would do

Modelled as: give the dominant side **50% of its own points** instead of 0, restore its
`net_direction`, then re-run the inter-category majority vote exactly as live.

| vpos | dir | R | live ds | live gated | half ds | half gated | Δ |
|---:|---|---:|---:|---:|---:|---:|---:|
| 75 | LONG | −0.106 | 4.00 | 5.00 | 4.00 | 5.00 | +0.00 |
| 76 | SHORT | +0.343 | 6.00 | 6.00 | 6.00 | 6.00 | +0.00 |
| 77 | SHORT | −1.087 | 2.25 | 3.25 | 3.50 | 4.50 | **+1.25** |
| 78 | LONG | −1.197 | 2.50 | 2.50 | 3.75 | 3.75 | **+1.25** |
| 79 | LONG | +0.503 | 4.25 | 3.25 | 4.25 | 3.25 | +0.00 |
| 80 | SHORT | −1.092 | 4.00 | 3.00 | 4.00 | 3.00 | +0.00 |
| 81 | SHORT | +0.770 | 2.50 | 3.50 | 3.75 | 4.75 | **+1.25** |
| 82 | LONG | +1.039 | 5.00 | 4.00 | 5.00 | 4.00 | +0.00 |
| 83 | SHORT | −1.090 | 4.25 | 4.25 | 4.25 | 4.25 | +0.00 |
| 84 | LONG | +0.122 | 7.50 | 8.50 | 7.50 | 8.50 | +0.00 |
| 85 | LONG | −1.087 | 2.25 | 3.25 | 4.38 | 5.38 | 🔴 **+2.13** |

🔴 **Halving is not a middle course. It is strictly a loosening — the score can only go up, never
down.** Four of eleven entries gain score; none lose any. **No entry would have failed a higher bar
under halving that passed under zeroing; the traffic is entirely the other way.**

| bar | refused (live) | refused (halved) | newly ADMITTED by halving | kept totR live | kept totR halved |
|---:|---|---|---|---:|---:|
| 3.0 | 78 | — | **78** (−1.20R) | −1.685 (n=10) | **−2.882** (n=11) |
| 4.0 | 77,78,79,80,81,85 | 78,79,80 | **77, 81, 85** (−1.40R) | +0.309 (n=5) | **−1.095** (n=8) |
| 5.0 | 77,78,79,80,81,82,83,85 | 77,78,79,80,81,82,83 | **85** (−1.09R) | +0.359 (n=3) | **−0.727** (n=4) |
| 7.0 | all but 84 | all but 84 | — | +0.122 (n=1) | +0.122 (n=1) |

**Halving makes the kept-set worse at every bar where it changes anything**, because the entries it
rescues (77 −1.09, 81 +0.77, 85 −1.09) are net −1.40R. **On n=11 that is a direction, not a verdict** —
but the *sign* of the mechanism is not an empirical question: halving can only ever admit.

---

## 4 · THE NEWS ADJUSTMENT — DEAD IN THE GATE, ALIVE IN THE CARD

### a) The trace, confirmed at the source

`_w_adj` reaches exactly **three** places on the state-machine path, and the gate is not one of them:

| # | site | what it does |
|---|---|---|
| 1 | `main.py:3829` | a `print` — `weighted_adj P2: dir=… raw=… adj=… final=…` |
| 2 | `main.py:3883` | `confluence_score=adj_score` inside `_shared_update_kwargs` |
| 3 | `main.py:4053` / `:4058` | `adj_tag` and `Score {adj_score:.2f}/10` on the Telegram card |

It is computed at **`main.py:3825`** — **136 lines after** the gate at `:3691`. The mirrors behave
identically: P1 at `:2183/2186/2210/2237` and P3 at `:4416/4419/4461/4505`.

**The overwrite, verbatim (`signal_matrix.py:535`), reached from `main.py:4030`:**

```python
signal_matrix.snapshot(row_id, symbol, scoring_result=matrix_result)   # main.py:4030 — AFTER the fill
    ...
    conn.execute(
        "UPDATE trades SET confluence_score=?, matrix_direction=?, "
        "matrix_breakdown_json=? WHERE id=?",
        (res['score'], res['direction'], json.dumps(res['breakdown']), trade_id),
    )
```

`res['score']` is the **raw** matrix score. Site 2 wrote `adj_score`; `snapshot()` runs afterwards and
replaces it. **The confirmation is empirical, not just textual: all 23 executed entries reproduce
their stored `confluence_score` exactly from the raw breakdown, and none reproduces `adj_score`.**

**`weight_engine.py`'s own docstring — *"Gate policy: `weighted_adj()` is NEVER applied to the raw
`direction_score` that gates entry. Only the stored `confluence_score` uses it."* — is half true and
half false.** The first sentence is correct. The second describes a write that is undone ~200 ms later
by a function in a different module. Confirmed.

### b) `macro_filter`'s `total_gate_adj` — the one adjustment that DOES reach the gate

`total_gate_adj = crypto_gate_adj + macro_gate_adj`, where `crypto_gate_adj` is ±`MACRO_NEWS_CRIT_ADJ`
/ ±`MACRO_NEWS_STRONG_ADJ` (**both 1.0**, direction-signed) and `macro_gate_adj` is `−2.5` during a
calendar blackout.

**Over 1,494 rows carrying a recorded `macro_gate_penalty` in 30 days:**

| value | n |
|---:|---:|
| 0.0 | 885 (59.2%) |
| **+1.0** | 347 |
| **−1.0** | 253 |
| −1.5 | 9 |

🔴 **Non-zero on 609 of 1,494 = 40.8%.** News category: NEUTRAL 885, CRITICAL_NEGATIVE 364,
STRONG_POSITIVE 245.

**Decision flips it caused — computed by comparing `ds < eff_thr` against `ds + mg < eff_thr` on every
row, with regime reconstructed from the stored breakdown:**

| | n | where |
|---|---:|---|
| 🔴 **BLOCKED** that the raw score alone would have admitted | **42** | 27 `below_threshold` TREND · 13 `below_threshold` FLAT · 2 `ai_skipped` FLAT |
| 🔴 **ADMITTED** that the raw score alone would have refused | **51** | 50 `ai_skipped` FLAT · **1 `executed`** (trow 12094, 2026-06-30 — pre-forming-fix, outside every cohort here) |

🔴 **The finding.** Those 27 blocked TREND rows are **the entire TREND refusal population of the score
gate**. Cross-checked both ways and the numbers are the same 27. **`CONFLUENCE_SCORE_THRESHOLD = 2.0`
has never once refused a signal on its own; every TREND refusal in 30 days is the news penalty pushing
a 2.25 or 2.5 below 2.0.**

And it cuts both ways: **the adjustment admits more often than it blocks (51 vs 42)**, almost entirely
by lifting FLAT-regime signals of 4.0–4.75 over the 5.0 floor with a `+1.0`. Of the 51, **50 were then
refused by the LLM anyway** — so on the executed book its net admitting effect is one trade, in June.

**A structural note on the sign, offered as an observation and not a claim:** `CRITICAL_NEGATIVE` gives
SHORT **+1.0**. Twelve of the 51 admits were SHORTs lifted over the FLAT floor by bad news. Whether
"bad news ⇒ easier to short" is a filter or a momentum-chasing amplifier is not answerable at this n.

### c) Does a NEG high-impact news read predict worse outcomes?

**n = 1. Unchanged from 13:09, and it is a winner.** Full clean cohort:

| vpos | dir | news_overall | impact | news_score | macro category | R |
|---:|---|---|---|---:|---|---:|
| 75 | LONG | POS | medium | +0.350 | STRONG_POSITIVE | −0.106 |
| 76 | SHORT | NEU | low | 0.000 | NEUTRAL | +0.343 |
| 77 | SHORT | NEG | medium | −0.350 | CRITICAL_NEGATIVE | −1.087 |
| 78 | LONG | *(null)* | *(null)* | — | NEUTRAL | −1.197 |
| 79 | LONG | MIXED | low | +0.150 | CRITICAL_NEGATIVE | +0.503 |
| 80 | SHORT | POS | medium | +0.420 | STRONG_POSITIVE | −1.092 |
| **81** | SHORT | 🔴 **NEG** | 🔴 **high** | −0.520 | CRITICAL_NEGATIVE | 🔴 **+0.770** |
| 82 | LONG | NEU | low | −0.250 | CRITICAL_NEGATIVE | +1.039 |
| 83 | SHORT | MIXED | low | +0.250 | NEUTRAL | −1.090 |
| 84 | LONG | MIXED | medium | −0.150 | STRONG_POSITIVE | +0.122 |
| 85 | LONG | POS | medium | +0.350 | STRONG_POSITIVE | −1.087 |

| cohort | n | wins | totR | meanR |
|---|---:|---:|---:|---:|
| NEG + high impact | **1** | 1 | **+0.770** | +0.770 |
| NEG, any impact | 2 | 1 | −0.317 | −0.159 |
| POS, any impact | **3** | **0** | 🔴 **−2.285** | −0.762 |
| NEU / MIXED / none | 6 | 4 | −0.280 | −0.047 |

**Both sides, as asked: LONG NEG n = 0. SHORT NEG n = 2 (−0.317R).** There is no LONG-with-negative-
news trade in the clean book at all, so the question cannot be answered on the LONG side.

**Widened to all 22 closed since the forming fix (contaminated by moved stops, labelled):** NEG any
n=6 (1 win, −2.970R), POS any n=4 (0 wins, −2.320R), NEU/other n=12 (4 wins, −2.746R).

🔴 **Verdict: the −0.62 you traced is dead in the gate and the outcome data cannot tell you whether it
should be alive.** n=1 at the exact cut you asked about, and the only signed pattern that shows at all
runs the *wrong* way — **POSITIVE news is 0 for 3 at −2.29R**, the worst cell in the table. That is
three trades. It is noise until it is not.

---

## 5 · ADX 1h BELOW THE FLOOR AT ENTRY

**Context first, because it changes what the column means.** Every `srv_adx_1h` below is the **200-candle
converged** reading from the entry snapshot. `ADX_BELOW_FLOOR = 20.0` lives in `_health_score` and is
consulted **only post-entry, in the recheck tiers** — it has never been a gate input, and until
`1161802` it was being fed a 42-candle warm-up artefact that ran **+6.23 high on average and missed
52.9% of true sub-floor states**. **The entry column was always clean; the rule that used it was not.**

The entry-side base rate is unchanged from 13:09: **6 of 23 executed entries (26.1%) below 20**, median
24.00, and the two lowest readings in the whole history are the two most recent trades (vpos 86 at
11.12, vpos 87 at 13.52).

### Outcome by entry-ADX1h band

**CLEAN closed, n = 11:**

| band | n | wins | totR | meanR | medR |
|---|---:|---:|---:|---:|---:|
| < 15 | **0** | — | — | — | — |
| 15–20 | 2 | 1 | −0.048 | −0.024 | −0.024 |
| **20–25** | 3 | 🔴 **3 (100%)** | 🔴 **+1.616** | +0.539 | +0.503 |
| 25–30 | 2 | 0 | −2.286 | −1.143 | −1.143 |
| ≥ 30 | 4 | 1 | −2.163 | −0.541 | −0.597 |
| **< 20 (below the floor)** | **2** | 1 | **−0.048** | −0.024 | — |
| **≥ 20** | **9** | 4 | **−2.834** | −0.315 | — |

Per side: LONG <20 n=2 (−0.048R), LONG ≥20 n=4 (−0.678R); **SHORT <20 n = 0** — there has never been a
clean closed sub-floor SHORT. SHORT ≥20 n=5 (−2.156R).

**ALL 22 closed since the forming fix (contaminated, labelled):** <15 n=1 (−1.022), 15–20 n=4 (−0.678),
20–25 n=7 (+0.277), 25–30 n=4 (−3.476), ≥30 n=6 (−3.138). Sub-floor n=5 (−1.700), ≥20 n=17 (−6.337).

The full clean cohort, sorted:

```
vpos 85 LONG  16.70  R -1.087 sl        vpos 83 SHORT 26.34  R -1.090 sl
vpos 82 LONG  16.88  R +1.039 trail     vpos 77 SHORT 30.29  R -1.087 sl
vpos 81 SHORT 20.51  R +0.770 trail     vpos 80 SHORT 30.38  R -1.092 sl
vpos 76 SHORT 21.35  R +0.343 external  vpos 84 LONG  30.71  R +0.122 external
vpos 79 LONG  21.75  R +0.503 trail     vpos 75 LONG  34.24  R -0.106 external
vpos 78 LONG  25.05  R -1.197 sl
```

🔴 **Answer: the tail is two draws, and the sign of the whole relationship is the opposite of the
worry.** Sub-floor entries are the *best*-performing cell in the clean book on a per-trade basis
(−0.024R mean against −0.315R for everything at or above 20). All three trail-exits — the only three
trades that ran — entered at **16.9 / 20.5 / 21.7**. **Of the six clean entries above 25, five lost;
the only positive is vpos 84 at +0.12R.**

**But n = 2 below the floor, and the 20–25 cell that carries the positive result is n = 3 and 3-for-3.**
Both are unusable. And §4.5 of OPEN-ITEMS already killed an ADX+score chop gate on exactly this shape
of evidence — *"the proposed separator fully overlaps winners and losers."* **This table is consistent
with that kill, not a challenge to it.** The honest statement is: **there is no evidence that entering
below the ADX floor is harmful, and weak, under-powered evidence that entering above 25 is.**

---

## 6 · WHERE IS THE ENTRY ACTUALLY LATE?

**Method, chosen to satisfy §4's own rule that price-path questions get real candles.** 2,620 BingX
15m candles fetched live, covering 2026-07-03 12:15 → 2026-07-30 19:00 UTC. For each entry:
`pos = (fill − low₂₄ₕ) / (high₂₄ₕ − low₂₄ₕ)` over the 96 bars **strictly before** the fill. Then
**adverse-extremity** = `pos` for a LONG, `1 − pos` for a SHORT — so 1.0 always means "entered at the
worst end of the range for this direction", regardless of side. No stored extrema were used.

### First: is this §4.3 wearing new clothes?

**No — and the check is quantitative, not rhetorical.** §4.3 killed the *prior-move bucket* (the
magnitude of the move leading into entry). Range position is a different object: it is a **level**
within a window, not a **displacement**. On the clean cohort:

```
Pearson r(adverse-extremity, directional prior-4h move) = -0.260   (n=11)
```

**The two measures are essentially unrelated, and the sign is even mildly negative.** So §6 is a
genuinely new measure. Recorded so nobody re-litigates it: **it is not a re-open of §4.3.**

### The measurement — all 23 entries in the history

| vpos | dir | fill | 24h low | 24h high | pos | prior-4h % | R | cohort |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 65 | LONG | 63244.9 | 62104.2 | 63403.0 | 0.878 | +0.98 | −0.414 | walltrail |
| 66 | SHORT | 62515.2 | 62413.9 | 63440.0 | 0.099 | −0.32 | −0.560 | walltrail |
| 67 | LONG | 63580.5 | 62413.9 | 63927.8 | 0.771 | +1.34 | −0.277 | excl |
| 68 | SHORT | 62254.0 | 61838.6 | 63969.0 | 0.195 | −1.23 | −0.036 | excl |
| 69 | LONG | 64542.5 | 61303.4 | 64692.7 | 0.956 | +1.13 | −0.279 | walltrail |
| 70 | LONG | 63335.2 | 61666.5 | 63469.3 | 0.926 | +1.05 | −0.307 | walltrail |
| 71 | LONG | 63788.4 | 61666.5 | 63925.0 | 0.940 | +0.85 | −0.197 | excl |
| 72 | LONG | 64325.9 | 63637.5 | 64431.3 | 0.867 | +0.26 | −0.993 | excl |
| 73 | LONG | 64352.6 | 63637.5 | 64481.3 | 0.847 | +0.21 | −0.476 | walltrail |
| 74 | SHORT | 62717.9 | 62453.6 | 64404.1 | 0.136 | −1.73 | −0.594 | tightened |
| **75** | LONG | 64664.1 | 61854.0 | 64939.4 | 0.911 | +0.27 | −0.106 | **CLEAN** |
| **76** | SHORT | 63384.5 | 63383.0 | 64973.1 | **0.001** | −1.04 | +0.343 | **CLEAN** |
| **77** | SHORT | 62834.1 | 62636.2 | 64872.8 | 0.088 | −0.16 | −1.087 | **CLEAN** |
| **78** | LONG | 65022.3 | 64256.3 | 65091.6 | 0.917 | +0.87 | −1.197 | **CLEAN** |
| **79** | LONG | 65254.4 | 63730.4 | 65654.1 | 0.792 | +0.44 | +0.503 | **CLEAN** |
| **80** | SHORT | 64683.2 | 64627.1 | 66280.9 | 0.034 | −0.53 | −1.092 | **CLEAN** |
| **81** | SHORT | 64902.7 | 64627.1 | 65779.6 | 0.239 | −1.27 | +0.770 | **CLEAN** |
| **82** | LONG | 64779.8 | 64089.7 | 64796.0 | **0.977** | +0.49 | +1.039 | **CLEAN** |
| **83** | SHORT | 63449.7 | 63020.9 | 65717.1 | 0.159 | −2.20 | −1.090 | **CLEAN** |
| **84** | LONG | 63997.3 | 62712.2 | 65063.6 | **0.547** | +0.83 | +0.122 | **CLEAN** |
| **85** | LONG | 64604.4 | 62935.4 | 64696.0 | 0.948 | −0.09 | −1.087 | **CLEAN** |
| 86 | SHORT | 63686.0 | 63231.6 | 64696.0 | 0.310 | +0.32 | −1.022 | tightened |
| **87** | LONG | **64838.7** | 63231.6 | **64990.0** | **0.914** | +1.34 | *open* | live |

### 🔴 THE RESULT: THE VARIABLE HAS NO VARIANCE

Clean cohort, ranked by adverse-extremity:

```
vpos 76 SHORT 0.999  R +0.343      vpos 77 SHORT 0.912  R -1.087
vpos 82 LONG  0.977  R +1.039      vpos 75 LONG  0.911  R -0.106
vpos 80 SHORT 0.966  R -1.092      vpos 83 SHORT 0.841  R -1.090
vpos 85 LONG  0.948  R -1.087      vpos 79 LONG  0.792  R +0.503
vpos 78 LONG  0.917  R -1.197      vpos 81 SHORT 0.761  R +0.770
                                   vpos 84 LONG  0.547  R +0.122
```

| bucket | n | wins | totR | meanR |
|---|---:|---:|---:|---:|
| top quartile (≥0.75 — "chasing") | **10** | 4 | −3.004 | −0.300 |
| upper-mid (0.50–0.75) | **1** | 1 | +0.122 | +0.122 |
| lower-mid (0.25–0.50) | 🔴 **0** | — | — | — |
| bottom quartile (<0.25 — "fading") | 🔴 **0** | — | — | — |

🔴 **Across the entire 23-entry history — clean, contaminated, live, paper — the minimum
adverse-extremity is 0.547 and 22 of 23 are above 0.75.** There is no comparison group. The bot has
never once entered from the favourable half of its own recent range.

```
Spearman rho(adverse-extremity, R)             = -0.118   (n=11)
Spearman rho(directional prior-4h move, R)     = +0.000   (n=11)
```

**Both correlations are noise, and they have to be: you cannot measure the effect of a variable that
does not vary.**

**So the answer to "where is the entry actually late" is: always, and by construction.** The matrix is
assembled from HyperWave / CHoCH / order-block continuation signals, the HTF cascade demands 1H and
15m agreement with the trigger, and the 5m trigger fires on the break. A gate stack that requires
three timeframes to already agree **cannot produce a fade entry.** vpos 86 (0.310) and vpos 87 (0.914)
are not two unlucky draws — 87 is the ordinary case and 86 is the second-least-extreme SHORT ever
taken.

🔴 **Recorded as a NEW, live hypothesis, explicitly not a finding, and explicitly not §4.3:** *the
entry engine has no fade mode.* It is untestable on the current book because the population contains
no counterexamples. **It would become testable only by taking entries the current cascade forbids,
which is a strategy change, not a measurement.** I am not proposing that. I am recording that the
question **cannot** be answered by more of the same data — waiting for n to grow will not help here,
because every new entry lands in the same bucket.

---

## 7 · THE HONEST SUMMARY — RANKED, WITH THE NUMBERS AND WHAT BREAKS

Ranked by expected value per unit of risk. **Nothing below is a proposal.** Every row states what
would break if it were wrong.

### 🥇 1 — Say out loud that `CONFLUENCE_SCORE_THRESHOLD` is not a gate

| | |
|---|---|
| **evidence** | min raw `direction_score` in TREND = **2.25** over 1,533 scored events / 30 days. The bar is 2.0. **Zero refusals on its own merit.** All 27 TREND refusals are the macro news penalty. |
| **n** | 🔴 **1,533** — by far the largest n in this report, and it is a fact about the *distribution*, not about outcomes |
| **EV** | highest confidence, **zero risk**: this changes no behaviour. It removes a false belief that the entry has a score gate. |
| **what would break if wrong** | nothing — it is an observation. It would be wrong only if a TREND signal can score below 2.0, which would require the triggering signal to contribute nothing to its own category. |
| **the risk it creates** | that "raise it to 4.0" becomes the obvious move. §2's curve says +3.19R over n=5 — **and §2's three caveats say the position cap makes that an upper bound, not an estimate.** |

### 🥈 2 — The FLAT floor is the real gate, and it is judged on signal presence

| | |
|---|---|
| **evidence** | **450 of 593 (75.9%)** score refusals are `CONFLUENCE_FLAT_THRESHOLD = 5.0`; 27 are the 2.0 bar. `market_regime` is `'TREND' if TREND-category net_direction != NEUTRAL else 'FLAT'` — **presence of a 1h signal, not a measurement of trend** (§2.13). Regime reconstruction validated at **0 / 593** contradictions. |
| **n** | 593 refusals, 30 days |
| **EV** | **high, and it is where weight already lives.** Anything given back to "regime" lands here, not on the 2.0 bar. |
| **what would break if wrong** | 🔴 **the skip-drift says its most-refused band is its most costly one:** the 3.0–4.0 band is n=188 at **+0.463%/24h** — those refusals look wrong. Tightening the FLAT floor would deepen exactly that. |
| **also** | at any global bar above 5.0 the floor **inverts into a discount** — FLAT gets an easier bar than TREND. 0 rows affected today (max refused score 4.75). Structural, dormant. |

### 🥉 3 — Two more signals that cannot stop a trade, and both are dry-run flags

| | |
|---|---|
| **evidence** | `DXY_HALT_DRYRUN = True` → `dxy_halt` returns `False` after printing; **16 would-blocks** in the ~2.7 days of journal that survive retention, **0** blocks. `FILTER_ENFORCEMENT_DRYRUN = True` → the enforcement extension logs and does not block. |
| **n** | 16 observed would-blocks (journal-limited, not 30 days); 39,310 `skip_attribution` rows carry no dxy field to widen it |
| **EV** | **medium-high, cheap to establish**: unlike the score bar, these were *designed* to refuse and were parked. Your four become six. |
| **what would break if wrong** | DXY has never been validated against outcomes on this book. The muted rule is symmetric (STRONG_UPTREND blocks LONG, DOWNTREND blocks SHORT) and **untested** — un-muting it is not "giving weight back to something that worked", it is switching on something unmeasured. |

### 4 — Intra-conflict, as a blunt marker only

| | |
|---|---|
| **evidence** | ANY conflict **n=7, −3.30R** vs NO conflict **n=4, +0.41R**. Holds on the widened n=16 cut (−4.61 vs −0.31). Conflicts are common: **59.1%** of 1,532 un-penalised scoring events. |
| **n** | 🔴 **7 vs 4.** Unchanged since 13:09 and it will stay unchanged until a clean trade closes. |
| **EV** | **medium.** The blunt version replicates across two cuts and both sides. |
| **what would break if wrong** | 🔴 **the directional refinement does NOT hold** — opposed n=3 at −0.43R is *better* than agreed/tie n=4 at −2.87R. Anything built on "the rule deletes dissent" is built on the wrong half of the split. And **halving is not the middle course it looks like**: it only ever raises the score, admits 3 more trades at 4.0 worth −1.40R, and turns +0.31R into −1.10R. |
| **cost of waiting** | at 0.74 closed positions/day, a properly powered clean-vs-conflicted split is months out (§2.2's standard). It costs nothing to keep counting. |

### 5 — The news adjustment: `_w_adj` reconnected to the gate

| | |
|---|---|
| **evidence** | trace confirmed at three call sites plus the overwrite; empirically confirmed by all 23 entries reproducing the raw score. `macro_filter`'s adjustment **does** reach the gate and flips **93 decisions** in 30 days (42 blocks, 51 admits). |
| **n** | 🔴 **1 for the outcome question.** NEG+high on the clean book is one trade, and it **won** (+0.770R). |
| **EV** | **low, and the sign is unsupported.** The only signed pattern in the news column runs backwards: **POSITIVE news is 0-for-3 at −2.29R**. |
| **what would break if wrong** | `_w_adj` on vpos 87 was **−0.62 with `news −0.5` and `funding −0.25`** — reconnecting it is not "adding the news back", it is adding **funding, EMA crosses, EMA slopes, DXY and MTF** to the gate simultaneously, all of them optimizer-learned weights that have never gated anything. **That is five untested inputs riding in on one label.** |
| **the cheap half** | the label defect is free to fix and independent of any gate change: `weight_engine`'s docstring claims `confluence_score` stores the adjusted value, and `signal_matrix.snapshot()` overwrites it ~200 ms later. Two numbers, one name, and the documented one is the discarded one. |

### 6 — Entry ADX 1h

| | |
|---|---|
| **evidence** | sub-floor cohort **n=2, −0.048R** vs at-or-above-20 **n=9, −2.834R**. The three trail-exits — the only three trades that ran — entered at 16.9 / 20.5 / 21.7. Of the six clean entries above 25, five lost. |
| **n** | 2 vs 9. The 20–25 cell carrying the positive result is n=3, 3-for-3. |
| **EV** | 🔴 **low, and the sign is opposite to the worry.** There is no evidence sub-floor entries hurt. |
| **what would break if wrong** | §4.5 already killed an ADX+score chop gate: *"the separator fully overlaps winners and losers."* This table agrees with that kill. Acting on the >25 tail would be re-opening a dead hypothesis on n=6. |
| **note** | `ADX_BELOW_FLOOR` was never a gate — post-entry only — and until `1161802` it read a warm-up artefact that missed **52.9%** of true sub-floor states. Any historical claim about it is claim about the artefact. |

### 7 — Entry lateness / range position

| | |
|---|---|
| **evidence** | **23 of 23** entries in the adverse half; **22 of 23** above 0.75; minimum 0.547. Spearman rho(extremity, R) = **−0.118**. |
| **n** | 11 clean, 23 total — **and zero in the comparison group** |
| **EV** | 🔴 **zero, as an actionable item.** Not because it is false but because it is **unmeasurable on this book.** |
| **what would break if wrong** | nothing can be built on it. **Its value is the opposite: it forecloses a plausible-sounding line of investigation before it costs analysis time.** "We enter late" is not a defect the data can see — it is the strategy's definition. |
| **honesty check** | it is **not** §4.3 re-opened (r = −0.26 against prior-move), and it is **not** a finding. Recorded as a closed question, not a live one. |

### What I am NOT ranking, and why

- **Raising the score bar to any specific level.** §2 gives the shape; the load-bearing cell (bar 4.0,
  +0.31R) is **n=5**, one trade supplies most of the swing, and the position cap makes every replay an
  upper bound. **That is your choice to make with the curve in front of you, not mine to recommend.**
- **A conflict filter.** 13:09's standing conclusion holds and this report strengthens it: *do not
  build a conflict filter from this table.*
- **Anything touching the exit path.** §2.4's frozen-input window is at **0 of ~10** and any change to
  what the advisor reads voids it.

---

## STATE AT PUBLICATION — read from runtime, not copied forward

| | |
|---|---|
| HEAD | `11618025ebb902b624ebef71bc6c545c149a891b`, working tree **clean** |
| `titan.service` | **active** |
| mode | 🔴 `LIVE_TRADING_ENABLED = True` · `ORDER_ADAPTER_LIVE = True` · $30 × 5 = $150 |
| vpos 87 | **open**, LONG, entry 64838.7, `sl_price` **64028.8** = `original_sl_price`, water_mark 65121.0, max_adverse 64576.4, `close_*` / `net_pnl` / `closed_at` all NULL |
| entries since vpos 87 | **0** |
| clean closed cohort | **n = 11**, unchanged since 13:09 |

## WHAT I DID NOT DO

- **No code was read into, changed, proposed or patched.** No config value touched. No flag flipped.
- **No level is recommended in §2.** The curve is given with n per cell, as asked.
- **`virtual_trader` was not imported** in any analysis process — its module-scope `init_db()` migrates
  the production schema on import (§2.33). Every number came from `sqlite3` reads and static parsing.
- **Two numbers I could not produce, said plainly rather than estimated:** (i) a 30-day `dxy_halt`
  would-block count — journald retention starts 2026-07-27 22:50, so 16 is a ~2.7-day figure;
  (ii) any outcome statistic for a LONG entered on negative news — **n = 0**, the cell is empty, not small.

---

*Titan · 2026-07-30 19:10 UTC · HEAD `1161802` clean · 🔴 LIVE · vpos 87 open −0.14R region, stop
64028.8 unchanged · READ-ONLY, nothing changed · clean closed cohort n=11 · the 2.0 bar has refused
**0** signals on its own merit in 30 days · the FLAT floor did **450 of 593** · 23 of 23 entries are
late by construction*
