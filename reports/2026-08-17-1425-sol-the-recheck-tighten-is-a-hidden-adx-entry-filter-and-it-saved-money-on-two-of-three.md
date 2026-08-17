# Mercury-SOL — the recheck tighten is not a health check. It is a hidden ADX entry filter executed 10 seconds late by halving the stop — and on this book it SAVED money on two of the three.

**2026-08-17 14:25 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · READ-ONLY THROUGHOUT — no `.py` written, no restart, no order, no DB write. Nothing proposed before §4, and nothing applied at all.**

Titan (`/root/titan-bot`): **not touched, not read for state, no numbers imported.** HEAD `897850b`, working tree clean.

Premise: [13:50 §1a](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-17-1350-sol-the-stop-is-not-too-tight-widening-shrinks-the-payoff-faster-than-it-saves-the-stop-outs.md) · the flag that was raised and never followed: [07.08 live flip §b](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-07-2245-sol-live-flip-executed.md) · the change that armed it: [07.08 ADX window fix](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-07-2230-sol-adx-window-fix-completed-quantified-proven-deployed.md)

---

## ⚡ THE SHORT VERSION

1. **🔴 THE TIGHTEN IS NOT MEASURING POST-ENTRY HEALTH. IT CANNOT.** At the T+10s tier the ADX it reads is **literally the entry snapshot's own cached bytes** — `_CACHE_TTL_BY_TF['1h'] = 300 s`, and `indicators.adx_reading`'s own docstring says so: *"the T+10s recheck runs seconds after the entry snapshot populated the 1h slot, so it reads the exact bytes the entry read."* The rule that fires is `ADX_BELOW_FLOOR` — an **absolute level**, not a delta — inside a score whose own header calls it *"delta-based … (NOT absolute levels)"*.
2. **🔴 ONE RULE REACHES THE THRESHOLD ON ITS OWN.** The ADX floor scores **−5**. `HEALTH_SCORE_TIGHTEN = −5`. The verdict is `score <= HEALTH_SCORE_TIGHTEN`. **So `ADX(1h) < 20` at entry ⇒ TIGHTEN at T+10 s, deterministically, with no other rule and no market movement required.** Verified: at T+10s the adverse-move rule contributed **0** in all three cases.
3. **🔴 THE PREDICTION IS EXACT IN THE POST-FIX ERA.** Reconstructed converged ADX(1h, 200) at every entry: **every post-2026-08-07 position with ADX < 20 was tightened (2 of 2); every one with ADX ≥ 20 was not (7 of 7). Nine for nine.** Before the fix the 42-bar ADX ran high and masked the same tapes — which is exactly why the 07.08 report predicted vpos **11, 17, 28** would flip OK→TIGHTEN. My independent reconstruction returns **the same three**.
4. **So it is an ENTRY FILTER wearing a stop's clothes.** It declines nothing, it takes the trade and then halves the risk ten seconds later, on information it already had before the fill.
5. **🔴 AND ON THIS BOOK IT MADE MONEY. Disabling it is WORSE by 0.964R.** vpos 27 **saved 0.502R**, vpos 34 **saved 0.500R** — both would have run on to breach the full 1R stop. vpos 35 **cost 0.037R** and is the only manufactured loss. Book with the tighten −2.961R; without it **−3.926R**.
6. **The operator's complaint is answered, and the answer is not the one the complaint expected.** The stop *was* halved, on three trades, two of which were already dead — the halving cut the loss, it did not cause it. **The chop shorts lost because they were chop shorts.**
7. **The one-way ratchet is real and it is confirmed.** `_tighten_sl` has explicit tighten-only clamps; the tier is terminal; **it has never loosened, never fired twice on one position, and never fired on a position that went on to win — 3 fires, 3 stop deaths.** But 2 of those 3 deaths were *smaller* than they would have been.
8. **🔴 THE REAL DEFECT IS THAT NOTHING IS WRITTEN DOWN.** The score and its reasons go to one stdout line and one Telegram message. **Neither survives** — journald retention on this unit starts **2026-08-15 11:15**, and all three tightens predate it. The DB stores the string `'tightened'` and nothing else. **The health score has never been validated against outcomes and, as built, it cannot be** — the evidence is deleted by design.
9. **A lying comment, still in the file.** `config.py:534-535`: *"here it only ever acts on PAPER positions (OBSERVATION_MODE), so zero real-money exposure."* **False since 2026-08-07.** vpos 34 and 35 are LIVE, and `_exec_move_stop` moved the resting stop on Bybit for both.
10. **NOTHING IS PROPOSED. `POST_ENTRY_RECHECK_ENABLED` stays `True`.** §4 carries the flag diff the brief asked to see, marked **NOT RECOMMENDED**, and confirms the operator's reading: **the 20-trade count SURVIVES** — the tighten moves a stop *within* R and never touches `SL_BUFFER_ATR`.

---

## 0. METHOD

Same engine and conventions as 13:50 §0c: Bybit SOLUSDT-perp **5m** candles over Tor (35,875 bars, fetched 13:37 UTC today), taker **0.001 every leg**, adverse extreme assumed touched first, **R_ref = 2.5 × ATR(1h)** fixed, today's live contract (arm 0.75R, BE lock, partial OFF, trail 0.75R). Counterfactuals use the **extension convention**: for a position booked as a stop-out, keep walking real candles up to +H hours past the booked close, H ∈ {4, 12, 24, 48}.

**One addition:** the ADX reconstruction. `compute_tf_metrics` runs `pandas_ta.adx(length=14)` on the raw ccxt frame **including the forming bar**, so the forming 1h bar is rebuilt from the 5m bars of that hour up to the entry instant, appended to 199 closed bars, and fed to the same `pandas_ta 0.4.71b0` the bot imports.

**Validated against the bot's own persisted values** on the eight rows that carry `entry_adx_1h_window = 200`:

| vpos | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 |
|---|---|---|---|---|---|---|---|---|
| stored | 53.20 | 30.93 | 23.42 | 26.35 | **12.78** | **18.95** | 21.13 | 24.67 |
| reconstructed | 53.24 | 30.93 | 23.63 | 26.62 | **12.93** | **19.21** | 21.13 | 24.67 |
| Δ | +0.04 | 0.00 | +0.21 | +0.27 | +0.15 | +0.26 | 0.00 | 0.00 |

Three exact, worst error **+0.27** points. Good enough to test a rule whose threshold is a hard 20.0, and every case below clears the threshold by more than the error.

---

# 1. WHAT THE MECHANISM IS, EXACTLY

## 1a. The rules, verbatim, with line numbers

**One owner.** `main.py` has no recheck path — it only creates the columns (`main.py:784-814`). The entire mechanism lives in `virtual_trader.py`, the paper poller, **which also moves live stops** (`_exec_move_stop`, `virtual_trader.py:2939`).

**Driver — `virtual_trader.py:2095-2117`:**

```python
_rstatus = row['recheck_status'] if 'recheck_status' in row.keys() else None
if (POST_ENTRY_RECHECK_ENABLED and not be_applied
        and _rstatus not in ('done', 'tightened', 'closed_critical')):
    ...
    _tier = _recheck_tier_due(_elapsed, _rstatus)
    if _tier is not None:
        _rres = _run_recheck_tier(exchange, row, last, _tier, send_tg)
```

Poll cadence `MONITOR_POLL_SECONDS = 10` (`config.py:524`), tiers `RECHECK_TIERS_SEC = [10, 60, 300]` (`config.py:537`). Pre-breakeven only.

**The score — `virtual_trader.py:1662-1727`**, five rules, all subtractive:

| rule | condition | penalty | constant |
|---|---|---|---|
| opposing wall growth | `cur/entry > 2.0` | **−10** | `WALL_GROWTH_CRITICAL` |
| opposing wall growth | `cur/entry > 1.5` | −5 | `WALL_GROWTH_WARNING` |
| **ADX drop** *(a delta)* | `entry − cur > 5.0` | −3 | `ADX_DROP_THRESHOLD` |
| 🔴 **ADX floor** *(a LEVEL)* | `cur_adx.value < 20.0` | **−5** | `ADX_BELOW_FLOOR` |
| ATR% contraction | `(entry−cur)/entry > 0.30` | −3 | `ATR_DROP_PCT` |
| adverse move | `> 0.5 %` / `> 0.3 %` | −3 / −1 | `PRICE_AGAINST_*` |

**The verdict — `virtual_trader.py:1729-1735`:**

```python
def _recheck_verdict(score):
    if score <= HEALTH_SCORE_EMERGENCY:   # -10
        return 'EMERGENCY_CLOSE'
    if score <= HEALTH_SCORE_TIGHTEN:     # -5
        return 'TIGHTEN'
    return 'OK'
```

**The action — `virtual_trader.py:1738-1751`. It is a FIXED MIDPOINT, not a computed level:**

```python
def _tighten_sl(position_side, entry_price, current_sl):
    eps = entry_price * 0.0001
    new_sl = (entry_price + current_sl) / 2.0
    if position_side == 'LONG':
        new_sl = max(new_sl, current_sl)         # tighten up only
        new_sl = min(new_sl, entry_price - eps)  # never at/above entry (wins)
    else:
        new_sl = min(new_sl, current_sl)         # tighten down only
        new_sl = max(new_sl, entry_price + eps)  # never at/below entry (wins)
    return new_sl
```

**Midpoint, halving the remaining distance.** Nothing in it reads volatility, the book, or the score's magnitude — a −5 and a −9 produce the identical stop. And it commits both sides (`virtual_trader.py:1890-1903`): `_exec_move_stop(row, new_sl)` moves the venue stop for a live row, then `UPDATE virtual_positions SET sl_price=?, recheck_status='tightened'`.

## 1b. 🔴 WHICH INPUTS ARE FRESH, AND WHICH ARE THE ENTRY SNAPSHOT

| input | source | fresh at the tier? |
|---|---|---|
| opposing wall mult | `_walls_okx` → OKX books-full depth-4000 | **fresh** (60 s cache in `liquidity_zones`) |
| **ADX(1h)** | `indicators.adx_reading` → `_fetch_ohlcv_cached(..., '1h')` | 🔴 **THE ENTRY SNAPSHOT'S OWN BYTES at T+10s and T+60s.** `_CACHE_TTL_BY_TF['1h'] = 300.0` (`indicators.py:62-64`) |
| ATR%(1h) | separate uncached `fetch_ohlcv(limit=42)` | fresh |
| adverse move | `last` from the poll tick | fresh |
| **the two baselines** | `entry_wall_baseline_mult`, `entry_adx_1h`, `entry_atr_pct_1h` | DB row, by definition entry-time |

The ADX row is not an inference — it is the design, stated in `indicators.adx_reading`'s own docstring (`indicators.py:198-201`):

> *"it inherits the per-TF cache (`_CACHE_TTL_BY_TF['1h'] = 300 s`), which is why this is cheaper than raising the literal at each call site: **the T+10s recheck runs seconds after the entry snapshot populated the 1h slot, so it reads the exact bytes the entry read — same value, no extra Tor request.**"*

🔴 **That is a correctness argument for the ADX *drop* rule — two readings of one measurement — and it is fatal for the ADX *floor* rule.** The drop rule then evaluates `entry − entry = 0` and never fires at T+10s. The floor rule evaluates **the entry value against a constant**, and fires or does not fire before the position has done anything at all.

**Verified on the three cases** — the adverse-move rule's contribution at each tier, from 5m bars:

| vpos | T+10s adverse | T+60s | T+300s | px-rule at T+10s | ADX floor | **score at T+10s** |
|---|---|---|---|---|---|---|
| 27 | +0.069 % | +0.069 % | +0.179 % | **0** | −5 | **−5 → TIGHTEN** |
| 34 | +0.173 % | +0.173 % | +0.452 % | **0** | −5 | **−5 → TIGHTEN** |
| 35 | +0.013 % | +0.013 % | +0.080 % | **0** | −5 | **−5 → TIGHTEN** |

**All three fired at T+10 s on the ADX floor alone**, ten seconds after the fill, on a market that had moved less than two tenths of one percent. `-5 <= HEALTH_SCORE_TIGHTEN` is a landing exactly on the boundary, not a margin.

## 1c. How often it has fired, and on what

Reconstructed converged ADX(1h, 200) at every entry, against what actually happened:

| era | positions with **ADX < 20** at entry | tightened | match |
|---|---|---|---|
| **pre-fix** (vpos 7–28, ADX read on 42 bars) | 11 (17.15), 17 (18.56), 27 (**15.95**), 28 (14.14) | **only 27** | the 42-bar figure read 27.03 / 20.92 / **17.67** / 34.15 — **only vpos 27's was under 20** |
| **post-fix** (vpos 29–37, ADX read on 200 bars) | 34 (**12.93**), 35 (**19.21**) | **34, 35** | 🔴 **2 of 2 fired; 7 of 7 with ADX ≥ 20 did not. 9 for 9.** |

🔴 **The pre-fix row is the causal proof, and it was written down in advance.** The 07.08 22:30 report replayed all 66 tier evaluations under the corrected ADX and found *"OK → TIGHTEN: 9 of 66 — vpos **11, 17, 28**, all three tiers each, all SHORT."* **My reconstruction, built today from candles with no knowledge of that table, returns exactly those three as the pre-fix sub-20 tapes.** Two independent methods, same three positions. The ADX window fix is what armed this rule, precisely as the flip report said it would.

**Counts:**

```
tier evaluations across the closed book : ~93  (31 positions x 3 tiers, terminal states aside)
TIGHTEN verdicts                        :   3  (vpos 27, 34, 35 — all SHORT)
EMERGENCY_CLOSE verdicts                :   0  (no row carries 'closed_critical')
positions marked 'done'                 :  28  (every tier scored > -5)
```

**Has it ever fired on a position that went on to WIN? No. 3 fires, 3 closes with `close_reason='sl'`.** All three were SHORT; all three had entry ADX under the floor.

## 1d. 🔴 Does it ever loosen? — No, and it is terminal

Three independent locks, all verified in source:

1. **`_tighten_sl` clamps direction** — `max(new_sl, current_sl)` for LONG, `min(...)` for SHORT. The stop can only move toward entry.
2. **The tier is terminal** — `_rstatus not in ('done', 'tightened', 'closed_critical')` (`virtual_trader.py:2104`). Once `'tightened'` is written the recheck block is never entered again for that position.
3. **Nothing else ever widens `sl_price`** — the only other writers are the breakeven lock (also toward entry) and the trail (also toward entry). `_exec_move_stop`'s own docstring: *"A failed live move leaves the exchange stop STALE BUT PRESENT — WIDER than intended, never tighter, never absent."*

**It is a one-way ratchet on the losing side, as the brief describes.** And there is a structural consequence nobody has stated:

🔴 **The tighten halves the stop and leaves the ARM where it was.** `activation_distance(fill, atr)` (`virtual_trader.py:2016`) is computed from the entry `atr` column and never reads `sl_price`. So after a tighten the position must travel **0.75 R_ref** to arm the breakeven lock while risking only **0.50 R_ref** — it needs **1.5× its remaining risk** in its favour to reach safety, against 0.75× before. **The tighten does not just cut the loss; it materially reduces the chance of the position ever being rescued.** That is the mechanism behind vpos 35 in §2.

*(Also noted in passing: the comment at `virtual_trader.py:2015` still describes the arm as `max(5×ATR, 0.25%)`, a formula superseded on 2026-06-08 and again on 2026-08-14. The code is right, the comment is three revisions stale.)*

---

# 2. WHAT IT COST — MEASURED, AND IT DID NOT COST

## 2a. The three cases

| | **vpos 27** | **vpos 34** | **vpos 35** |
|---|---|---|---|
| side / book | SHORT / paper | SHORT / **LIVE** | SHORT / **LIVE** |
| entry | 72.5300 | 75.2100 | 75.1600 |
| **original stop** (1.000 R_ref) | 73.4700 | 76.3000 | 75.9600 |
| **tightened to** (0.500 R_ref) | **73.0000** | **75.7550** | **75.5600** |
| booked exit | 73.0700 after 7.12 h | 75.7600 after **0.53 h** | 75.5700 after **1.16 h** |
| realised | **−0.660 R** | **−0.643 R** | **−0.701 R** |
| MFE / MAE in its booked life | +0.649 / −0.585 | −0.037 / −0.514 | +0.113 / −0.512 |

**What the tape did after each exit** — the question that decides everything:

| vpos | worst +4h | worst +12h | worst +24h | **would the FULL 1R stop have been hit?** | best after the exit |
|---|---|---|---|---|---|
| **27** | −1.394 | −1.862 | −1.862 | 🔴 **YES, within 4 h** | −0.202 (never green again) |
| **34** | −1.000 | −1.110 | −1.110 | 🔴 **YES, within 4 h** | +0.183 at 24 h |
| **35** | −0.738 | −0.738 | −0.738 | **NO — never reached −1R** | **+0.675 at 4 h** |

**Two of the three were already dead.** The tighten did not take them out of a trade that recovered; it took them out of a trade that went on to run past the full stop. **vpos 35 is the single case where the halved stop ended a position the untightened one would have survived** — and it is also the case that shows §1d's arm/stop asymmetry doing damage: it peaked at +0.675R after the exit, short of the 0.75R arm it would have needed.

## 2b. Replayed at the untightened stop, whole contract

| vpos | booked | **no-tighten +4h** | **+12h** | **+24h** | **+48h** | with the tighten (all horizons) |
|---|---|---|---|---|---|---|
| 27 | −0.660 | −1.158 `stop` | −1.158 `stop` | −1.158 `stop` | −1.158 `stop` | **−0.656 `stop`** |
| 34 | −0.643 | −1.137 `stop` | −1.137 `stop` | −1.137 `stop` | −1.137 `stop` | **−0.638 `stop`** |
| 35 | −0.701 | +0.175 `horizon` | −0.651 `horizon` | −0.551 `horizon` | −0.626 `horizon` | **−0.688 `stop`** |

**vpos 27 and 34 hit the full 1R stop under every horizon.** vpos 35 is horizon-dependent and never resolves to a win — at +4h it marks out at +0.175R, at +12h at −0.651R, and it never arms.

## 2c. 🔴 THE WHOLE-BOOK COUNTERFACTUAL

Today's live contract, b = 2.5, tighten modelled ON (as it actually ran) vs OFF:

| extension | **ON** (as it ran) | **OFF** (disabled) | **Δ (OFF − ON)** | positions changed |
|---|---|---|---|---|
| +0 h | −2.961 | −3.053 | **−0.091** | 3 |
| +4 h | −2.961 | −3.100 | **−0.138** | 3 |
| **+12 h** | **−2.961** | **−3.926** | **−0.964** | 3 |
| +24 h | −2.961 | −3.826 | −0.864 | 3 |
| +48 h | −2.961 | −3.901 | −0.939 | 3 |

**n=31 (with vpos 36, 37): identical deltas** — −0.091 / −0.138 / **−0.964** / −0.864 / −0.939, because neither new position was tightened.

🔴 **Disabling the tighten is worse at every horizon, by up to 0.964R.** The three positions and their individual contributions at +12h:

```
vpos 27  the tighten SAVED  0.502 R
vpos 34  the tighten SAVED  0.500 R
vpos 35  the tighten COST   0.037 R    (0.137 R at the +24h horizon)
                            ------
                    net    +0.964 R in the book's favour
```

## 2d. Costs, charged

**The tighten adds no extra leg** — it moves a stop, it does not exit. Taker 0.001 is charged on the entry and on the one exit leg in **both** arms, on the **same** size, so the only difference between the arms is the exit **price** and the exit **time**:

| vpos | tighten | legs | taker (R_ref) | exit | hold |
|---|---|---|---|---|---|
| 27 | ON | 1 | 0.1548 | stop | 7.08 h |
| 27 | OFF | 1 | 0.1553 | stop | 7.66 h |
| 34 | ON | 1 | 0.1385 | stop | 0.49 h |
| 34 | OFF | 1 | 0.1390 | stop | 3.41 h |
| 35 | ON | 1 | 0.1884 | stop | 1.08 h |
| 35 | OFF | 1 | 0.1884 | horizon | 13.16 h |

The fee difference between the arms is **0.0005 R_ref**, i.e. nothing. Note the taker burden itself on these rows — **0.14 to 0.19 R_ref per position** — because live risk is $0.91–$1.42 against a $100 notional. That is a live-sizing fact, not a tighten fact, and it is stated so it is not read as one.

---

# 3. THE HEALTH SCORE ITSELF

## 3a. 🔴 It has never been validated against outcomes, and as built it cannot be

**Plainly, as the brief asked:** the score is a hand-assigned penalty table — −10/−5 for wall growth, −5 for an ADX level, −3 for an ADX drop, −3 for ATR contraction, −3/−1 for adverse price. **No number in it was fitted to, or checked against, what happened next.** There is no backtest of the score, no calibration of the thresholds against realised R, and no record of a verdict ever being scored for accuracy.

**And it cannot be checked retroactively, because the mechanism deletes its own evidence:**

| where the score goes | survives? |
|---|---|
| one stdout line, `virtual_trader.py:1870-1875` | ❌ **journald retention on this unit begins 2026-08-15 11:15** — all three tightens (03.08, 13.08, 14.08) predate it |
| one Telegram message, `virtual_trader.py:1906-1913` | ❌ not machine-readable, not archived |
| the DB | ❌ **`recheck_status` stores only the string `'tightened'`** — no score, no reasons, no tier, no ADX, no wall ratio |

🔴 **So the three most consequential decisions this mechanism has ever made left no record of why.** The score of −5, the tier, and which rules fired had to be **reconstructed from candles** for this report. A rule that moves a live stop and writes nothing but a five-character status is not auditable, and the fact that this pass could reconstruct it is luck — the ADX floor happens to be a deterministic function of a value the DB *does* persist. Had the wall rule been the trigger, the OKX depth-4000 book at 2026-08-13 16:40:34 does not exist anywhere and the decision would be permanently unexplainable.

**One more thing the record gets wrong** — `config.py:534-535`:

> *"LIVE action mode (no DRYRUN) — matches Titan's deliberate operator decision; **here it only ever acts on PAPER positions (OBSERVATION_MODE), so zero real-money exposure**."*

**That was true until 2026-08-07 22:25 and has been false ever since.** vpos 34 and 35 are live rows; `_exec_move_stop` (`virtual_trader.py:2939-2952`) calls `_live_move_stop` for them and moved the resting stop on Bybit. The sentence is now a false safety claim sitting directly above the constant it describes.

## 3b. 🔴 Cutting a loss early, or manufacturing one? — crossed with 13:50 §1c

The 13:50 report established that **11 of 14 stopped positions went a further 0.25R+ against within four hours of the exit** — the stop-outs were not noise takeouts, the moves continued. That finding decides this question, and it decides it in the tighten's favour:

| | verdict | evidence |
|---|---|---|
| **vpos 27** | **cutting a loss early — BENEFIT** | ran to −1.394R within 4h, −1.862R within 12h; never green again (best −0.202R) |
| **vpos 34** | **cutting a loss early — BENEFIT** | reached exactly −1.000R within 4h, −1.110R by 12h |
| **vpos 35** | **manufacturing a loss — COST** | never reached −0.738R; peaked +0.675R after the exit — but **below the 0.75R arm**, so it would not have been rescued either |

**Two of three, and the whole book agrees:** disabling the tighten costs 0.964R. **The mechanism fires on positions that were going to lose, and it is cutting the loss roughly in half when it does.**

**But note carefully WHY it is right, because the reason is not the one the code claims.** It is right because `ADX(1h) < 20` at entry has been a losing tape for this signal set — not because a health score detected deterioration. The six positions in the book that entered with converged ADX under 20:

```
vpos 11 +0.955   vpos 17 +0.396   vpos 27 -0.656
vpos 28 -0.220   vpos 34 -0.638   vpos 35 -0.688
                                  --------------
n = 6            sum -0.851 R     mean -0.142 R/trade
the other 23     sum -2.111 R     mean -0.092 R/trade
```

🔴 **And that is an ENTRY-SIDE candidate, so it is refused here rather than smuggled in through the exit.** The cohort is 6 positions, two of them winners, and its mean is 0.05R/trade worse than the rest of a book that is itself losing. **That is candidate #27 and it fails on sight** — no side split, no era split, no monotone threshold, and it would need the same de-confounding that killed the previous twenty-six. **It is reported as a measurement, not proposed as a filter.**

## 3c. The usable n, stated honestly

**Three cases is not a sample.** No p-value is quoted for anything in §2, no confidence interval is claimed on +0.964R, and the whole result would reverse if the next two firings behave like vpos 35 rather than 27 and 34.

**What IS a mechanical fact and does not need n:**

```
fires                                 : 3
fires that ended in a stop death      : 3  (3/3)
fires on a position that later won    : 0
times it has ever LOOSENED a stop     : 0  (structurally impossible - three clamps)
fires that reduced the realised loss  : 2  (vpos 27 -0.502R avoided, vpos 34 -0.500R avoided)
fires that increased it               : 1  (vpos 35, +0.037R at +12h)
post-fix positions with ADX < 20      : 2  -> tightened 2   (2/2)
post-fix positions with ADX >= 20     : 7  -> tightened 0   (7/7)
```

**"Fired three times and lost three times" is true and it is the wrong summary.** All three were losers before the tighten touched them; the question is whether they lost *more* or *less*, and the answer is less, twice out of three.

---

# 4. VERDICT

## 4a. 🔴 IT SAVES MONEY. It is the brief's SECOND bullet, and the operator's complaint is answered.

**The three deaths would substantially have happened anyway.** vpos 27 and 34 breached the full 1R stop within four hours of their tightened exit and kept going — the tighten cut 0.502R and 0.500R off losses that were already in flight. vpos 35 is the one manufactured loss and it is worth 0.037R at the +12h horizon. **Net, the mechanism is +0.964R in the book's favour, at every extension horizon tested.**

**So: yes, the stop was too short on those three trades — it was literally halved — and no, that is not why they lost.** They were sub-20-ADX shorts entered into a flat tape, and 13:50 §1c already established that this book's stop-outs keep running against after the exit rather than reverting. The tighten found two of them and got out for half price.

**`POST_ENTRY_RECHECK_ENABLED` stays `True`. Nothing is proposed and nothing is applied.**

## 4b. What IS wrong, named without proposing a change to it

Three things are true at once, and only the first is about money:

1. **The mechanism nets positive on this book.** Do not disable it on the strength of three trades in either direction.
2. **🔴 Its stated design and its actual behaviour do not match.** `_health_score`'s own header calls it *"delta-based … (NOT absolute levels)"*, and the rule that has fired every single time is an absolute level, evaluated at T+10s against **the entry snapshot's own cached bytes**. Whatever this mechanism is, it is not post-entry health monitoring — it is a `ADX(1h) < 20` entry filter that executes ten seconds late by halving the stop, and it leaves the arm at 0.75R so the tightened position needs 1.5× its remaining risk to reach safety.
3. **🔴 It writes nothing down.** The three decisions that moved a live stop persist as the five-character string `'tightened'`. Their scores exist nowhere. This report reconstructed them only because the trigger happened to be a function of a column the DB does keep.

**The honest consequence of (2) and (3), stated as a question for the operator rather than as a proposal:** if `ADX(1h) < 20` is genuinely a bad tape for this signal set, the mechanism that expresses it should be an entry gate that declines the trade — saving the whole loss — not a stop halving that saves half of it. **§3b measures that gate and it fails on sight (n=6, two winners, 0.05R/trade).** So the current arrangement is, by accident, the more conservative of the two available expressions of the same belief. **That is a reason to leave it alone, not a reason to promote it.**

## 4c. The flag diff — shown because the brief asked to see it, marked **NOT RECOMMENDED**

The brief's first bullet is not met (the tighten does not cost money, and there are two cases where it saved). This diff is therefore an artifact, not a proposal. It is **not applied**, and it should not be.

```diff
--- a/config.py
+++ b/config.py
@@ -527,15 +527,29 @@
 # ── Post-entry multi-tier recheck (paper poller, LIVE action mode) ───────────
 # A16 2026-06-08: Titan parity (titan-bot config.py:430-446 / virtual_trader.py
 # post-entry recheck). After a virtual fill the poller re-evaluates the position
 # at T+10/60/300s against its entry baselines (opposing-wall multiplier, 1h ADX,
 # 1h ATR%) plus the unrealized adverse move. A delta-based Health Score (NOT
 # absolute levels) drives a defensive response BEFORE breakeven arms; once
 # +1R/trail is active the trail owns the position and rechecks stop. LIVE action
-# mode (no DRYRUN) — matches Titan's deliberate operator decision; here it only
-# ever acts on PAPER positions (OBSERVATION_MODE), so zero real-money exposure.
+# mode (no DRYRUN) — matches Titan's deliberate operator decision.
+#
+# 🔴 2026-08-17 — THE SENTENCE THAT USED TO SIT HERE WAS FALSE SINCE THE LIVE FLIP.
+# It read "here it only ever acts on PAPER positions (OBSERVATION_MODE), so zero
+# real-money exposure". Since 2026-08-07 22:25 this poller drives LIVE stops via
+# _exec_move_stop -> _live_move_stop. vpos 34 and 35 are live rows whose resting
+# Bybit stop this mechanism moved. Measured: reports/2026-08-17-1425-*.md
 POST_ENTRY_RECHECK_ENABLED = True
+
+# ── 🔴 THE TIGHTEN BRANCH, BEHIND ITS OWN FLAG (2026-08-17) ───────────────────
+# False = the recheck still SCORES and still LOGS every tier, and EMERGENCY_CLOSE
+# still fires; only the defensive SL halving is suppressed and the tier is
+# recorded 't+{n}_ok' instead of 'tightened'. Code path intact, one constant.
+#
+# 🔴 IT IS True ON PURPOSE. The measured effect of setting it False on the closed
+# book is -0.964 R (book -2.961 -> -3.926 at the +12h extension). It fired three
+# times: vpos 27 SAVED 0.502R, vpos 34 SAVED 0.500R, vpos 35 COST 0.037R. Both
+# saves are positions that went on to breach the FULL 1R stop within four hours.
+# Do NOT flip this without n >= 8 firings and a fresh counterfactual.
+RECHECK_TIGHTEN_ENABLED = True
```

```diff
--- a/virtual_trader.py
+++ b/virtual_trader.py
@@ -1729,7 +1729,7 @@
 def _recheck_verdict(score):
     """EMERGENCY_CLOSE / TIGHTEN / OK from a health score."""
     if score <= HEALTH_SCORE_EMERGENCY:
         return 'EMERGENCY_CLOSE'
-    if score <= HEALTH_SCORE_TIGHTEN:
+    if score <= HEALTH_SCORE_TIGHTEN and RECHECK_TIGHTEN_ENABLED:
         return 'TIGHTEN'
     return 'OK'
```

⚠️ **That second hunk has a trap and it is named rather than shipped:** routing a suppressed TIGHTEN into `'OK'` makes it indistinguishable from a genuine pass, and on an unmeasured OKX book the `cur_walls is None and verdict == 'OK'` branch (`virtual_trader.py:1862-1868`) would then *decline to record the tier* — turning a suppressed tighten into an infinite retry until the 300s window expires. **A correct implementation must gate at the ACTION site (`if verdict == 'TIGHTEN'`, `virtual_trader.py:1890`) and record `t+{tier}_ok` explicitly, not at the verdict site.** This is exactly the class of defect the standing rules exist to catch, and it is written down here so that if this diff is ever wanted, the two-line version is not the one that gets applied.

## 4d. 🔴 THE PRE-REGISTERED 20-TRADE COUNT — the operator's reading is CORRECT

**Confirmed, and here is the arithmetic that makes it so.**

```
1R = SL_BUFFER_ATR x ATR x size          <- _tighten_sl appears NOWHERE in this
```

`_tighten_sl` writes `sl_price`. It never touches `SL_BUFFER_ATR`, never touches `atr`, never touches `size`, and never touches `original_sl_price` — the row keeps its original stop on record, which is exactly why every R in this report and in 13:50 could be computed for the tightened positions at all. **`initial_risk_usdt` is stamped at entry and is not rewritten.** So R before and after a tighten is the same unit, and a book containing tightened and untightened positions is a book in one denomination.

| | moves 1R? | count survives? |
|---|---|---|
| `SL_BUFFER_ATR` (13:50 §4c) | **YES** — re-denominates every R | ❌ count must reset to 0/20 |
| `TRAIL_ARM_R`, `TRAIL_MULT_ATR` | no — fractions OF R | ✅ |
| **`_tighten_sl` / disabling the tighten** | **NO** — moves a stop WITHIN R | ✅ **the count SURVIVES** |

**So disabling the tighten would be a mid-count change that does not void the count** — vpos 36 and 37 stay in it, and the ~03.09 date does not move.

**Two caveats, recorded because "the count survives" is not the same as "the change is free":**

1. **It would change what the remaining 18 closes measure.** The count judges *this signal set under this contract*; the tighten is part of that contract for the two already banked. Mixing 2 tightened-era closes with 18 untightened-era ones is a unit-clean but **policy-mixed** sample, and that must be stated on the count's own record rather than discovered at close 20.
2. **On the observed rate it would touch roughly one of the remaining 18.** The tighten has fired 3 times in 31 positions (9.7 %), all SHORT, all sub-20-ADX. **Eighteen closes at that rate is 1.7 expected firings.** Whatever is decided about this mechanism, **the 20-trade count is not the instrument that will settle it** — it will contain one or two cases, which is where this report already is.

**Neither of those is a reason to change anything now. Nothing is proposed.**

---

## STATE — nothing was changed by this pass

```
mercury-sol   active - MainPID 2195203 - since 2026-08-14 19:54:37 UTC - NRestarts=0
              NOT restarted by this pass. FLAT: zero open positions.
GEOMETRY      unchanged: SL_BUFFER_ATR 2.5 - TRAIL_ARM_R 0.75 - TRAIL_MULT_ATR 1.875
              PARTIAL_AT_ARM_ENABLED False - ATR_TF 1h
RECHECK       unchanged: POST_ENTRY_RECHECK_ENABLED True - RECHECK_TIERS_SEC [10,60,300]
              HEALTH_SCORE_TIGHTEN -5 - ADX_BELOW_FLOOR 20.0 - fired 3 times ever
BOOK          31 closed - booked SumR -7.967 - live sub-book (vpos 29-37) -2.593
              stopping rule: 2 of 20 live closes done (vpos 36, 37), both losers
FILES         mercury-sol: ZERO .py modified. No DB write. No order. No restart.
              Read-only URI (mode=ro) on trades.db throughout. The diffs in 4c are
              PRINTED IN THIS REPORT ONLY and exist in no file.
titan         /root/titan-bot - NOT touched, NOT read for state, NO numbers imported.
              HEAD 897850b - working tree clean
```

**Provenance: `virtual_trader.py`, `config.py`, `indicators.py`, `trail_arm.py` read from disk at their current revisions with line numbers quoted as found; SOL's own `trades.db` opened `mode=ro`; Bybit SOLUSDT-perp 5m and 1h candles over Tor (13:37 UTC today); the ADX reconstruction validated against the eight `entry_adx_1h_window = 200` rows the bot itself persisted, worst error +0.27 points, and independently corroborated by the 07.08 22:30 report's own OK→TIGHTEN list (vpos 11, 17, 28). `journalctl -u mercury-sol` retains nothing before 2026-08-15 11:15, which is why the three actual scores are reconstructed rather than quoted. Titan was not read.**
