# titan grades corrected, learning text marked, combo-weight mechanism inert at live size

_2026-08-03 14:01 UTC_

---

# TITAN — §2.3 RUN AND VERIFIED · THE `learning_*` TEXT MARKED · AND THE COMBO-WEIGHT MECHANISM IS **INERT AT LIVE SIZE**

_2026-08-03 14:00 UTC · HEAD `ca90c2f` · LIVE, real money, flat · §2.4 explicitly NOT run_

---

## DECISION LINE

**§2.3 is done and verified against the backup.** Three grades corrected in one transaction with the
class-assert enforced; `weight`, `wins`, `losses`, `evaluations` untouched on both stores; a
full-table diff proves exactly 3 trades rows, 3 combo rows and 3 subtype rows changed, and
`total_pnl` is the only field that differs on any of them.

🔴 **And item 3 is worse than "inert going forward" — it has already been inert for the whole live
era, and the frozen table is still being shown to the advisor as current fact.**

Your reading was right on every count and the numbers are now on the record:

- the thresholds are **absolute USDT**, compared raw, with **no notional/size/R term anywhere near
  either comparison** — declared twice, in two files;
- live-era grades that crossed either threshold: **0 of 6**, needing **8.0R–15.1R** (mean 11.2R);
- **the loss side is unreachable BY CONSTRUCTION** — the stop caps a live loss at ~1R, so −15 USDT
  requires **6.0R at best, i.e. the stop must fail first**. The table can only ever move **up**, and
  in practice not at all;
- **the last grade capable of moving a weight was `audit_at 2026-07-20 02:24:17` — in the PAPER era,
  nine days before the live flip.** Since the flip: 6 grades, 0 threshold-crossing;
- expressed in R, +20/−15 meant **+0.1608R / −0.1206R** at paper size. The same meaning in live
  dollars is **+0.2985 / −0.2238**. The constants in force are **67× too high and 67× too deep**;
- **(d) yes.** The frozen table is rendered into every entry prompt. **Trade 19713 — a live,
  real-money entry — was shown `Combo weight: 0.90 (1.0 baseline; <1 = historical loser, >1 =
  winner)`, and that 0.90 came from a single PAPER evaluation of ≈−78.70 at 68× the notional.**

**§2.4 not run, and §2.40 is exactly why it got heavier:** with the update mechanism inert, whatever
that re-grade writes is the value the combo carries **permanently**, straight into the prompt.

**One thing changed while this ran: vpos 91's held branch terminated.** Stop 63224.6 touched at
13:52, cleared unambiguously by 63.1 pts at 13:55. Advisor **+0.8272 (+0.625R)**. **§2.4 tally goes
4 → 5**, net **advisor +3.3729**, improved 4 / worsened 1. Five more closes needed; the bar does not
move.

---

# 1. §2.3 — RUN

## 1.1 Backup first

Not `cp` — a byte copy of a live SQLite file can catch a partial write. Used the engine's own atomic
snapshot API:

```
sqlite3.Connection.backup()  ->  /root/titan-bot/trades.db.bak_gradefix_20260803   65,249,280 bytes
PRAGMA integrity_check       ->  ok
backup sees the pre-correction values: [-1.2829, -0.3467, 0.5015]     trades rowcount 20,056
```

Preconditions checked before touching anything: **no open position** (vpos 91 had closed at
13:41:09), and **0 rows** in the audit worker's queue, so no concurrent writer.

## 1.2 The transaction — asserts enforced, not assumed

`BEGIN IMMEDIATE`, all asserts evaluated **before** any write, `ROLLBACK` wired to any failure:

```python
assert old is not None                 # nothing to correct
assert new is not None                 # pnl NULL => position not closed => REFUSE
assert klass(old) == 'neutral'         # a weight moved on the old grade -> ABORT
assert klass(new) == 'neutral'         # a weight would have to move    -> ABORT
...
assert c1.rowcount == 1 and c2.rowcount == 1 and c3.rowcount == 1
```

The class-assert is the guard you asked for: **if neutral-to-neutral ever stops being true, the whole
transaction aborts**, because a class change means a weight must move and that is a different
operation than this one.

```
  assert OK  trade 19589: -1.2829 (neutral) -> -2.541574 (neutral)  delta -1.258674
  assert OK  trade 19713: -0.3467 (neutral) -> -0.819051 (neutral)  delta -0.472351
  assert OK  trade 20920: +0.5015 (neutral) -> -0.641000 (neutral)  delta -1.142500

  all asserts passed — applying inside the open transaction

  trade 19589: combo total_pnl -1.258674 | subtype HW_SIGNAL_SHORT total_pnl -1.258674 | audit_score -> -2.541574
  trade 19713: combo total_pnl -0.472351 | subtype HW_SIGNAL_LONG  total_pnl -0.472351 | audit_score -> -0.819051
  trade 20920: combo total_pnl -1.142500 | subtype HW_OS_LONG      total_pnl -1.142500 | audit_score -> -0.641000

✅ COMMITTED — one transaction, 9 statements, 3 rows each store
```

## 1.3 Verified against the backup — four checks

| # | check | result |
|---|---|---|
| 1 | `audit_score` now equals realised `pnl` on all three | −2.541574 / −0.819051 / −0.641000, all exact, `audit_at 2026-08-03 13:52:38` |
| 2 | per-row field diff | **`total_pnl` is the ONLY field that differs** on all six store rows. `weight` 1.0→1.0, 0.9→0.9, 1.0→1.0, 0.85→0.85, 0.75→0.75, 1.0→1.0 · `wins` 0→0 · `losses` unchanged · `evaluations` 3→3, 2→2, 1→1, 23→23, 18→18, 1→1 |
| 3 | **full-table** diff, both stores | `signal_weights`: **3** rows differ · `hyperwave_weights`: **3** rows differ. Nothing else in either table |
| 4 | full `trades` diff on graded rows | rows differing: **`[19589, 19713, 20920]`** and nothing else |

Resulting `total_pnl`:

| store | key | was | now |
|---|---|---:|---:|
| combo | `…Smart Trail Bearish\|HyperWave Signal Down\|Within Bearish OB` | +0.409604 | **−0.849070** |
| combo | `…Bullish Confirmation+\|HyperWave Signal Up\|Within Bullish OB` | −79.045825 | **−79.518176** |
| combo | `…Bearish Confirmation\|HyperWave OS Signal Up\|Bearish OB Created` | +0.501500 | **−0.641000** |
| subtype | `HW_SIGNAL_SHORT` | −343.603107 | **−344.861781** |
| subtype | `HW_SIGNAL_LONG` | −340.558645 | **−341.030996** |
| subtype | `HW_OS_LONG` | +0.501500 | **−0.641000** |

**One judgement call, stated so it is not discovered later:** `updated_at` was **left alone** on both
stores. It records when the evaluation happened, which is still true; bumping it would read as a new
evaluation. The audit trail for the correction is the `trades.audit_at` stamp, the backup, and
OPEN-ITEMS §2.39a.

---

# 2. THE `learning_*` TEXT — LEFT AND MARKED (option b)

Not cleared, not re-run. Recorded in **OPEN-ITEMS §2.39b**.

`_attempt_learning` receives `row_for_learning['pnl'] = outcome_pnl` — **the same number the weights
took**. So every attribution written before `ca90c2f` was reasoned against whatever
`_evaluate_trade_pnl` invented: an unrealized mark, or a fabricated `0.0`.

**The demonstrable case, trade 20920** (`learning_at 2026-08-03 08:48:53`), verbatim:

> *"Large ask wall (68.32 BTC at 62650.5) above entry created resistance, **enabling profitable short
> exit as price rejected upward pressure**."*

The position had not exited. It closed five hours later at **−0.6410**. **A wrong story, not a wrong
number** — which is exactly why arithmetic cannot repair it and why clearing it would destroy the
evidence that the defect existed.

**Cost is archival, not behavioural.** `learning_liquidity_factor`, `learning_aggression_factor`,
`learning_influence`, `learning_confidence`, `learning_reason`, `learning_raw` are written only by
`signal_weights._attempt_learning` and **read by nothing** — grep finds no reader anywhere. Nothing
trades on them.

**The marking rule, now in OPEN-ITEMS:** treat every row with `learning_at < 2026-08-03 13:42` as
attributed to an unresolved outcome. From `ca90c2f` forward the attribution sees a realised pnl.

---

# 3. 🔴 THE FINDING — THE MECHANISM CANNOT FUNCTION AT LIVE SIZE

Recorded as **OPEN-ITEMS §2.40**.

## 3a. The thresholds are absolute USDT, and nothing scales them

```
signal_weights.py:42   WIN_THRESHOLD_USDT  =  20.0        engine_15m.py:56   WIN_THRESHOLD_USDT  =  20.0
signal_weights.py:43   LOSS_THRESHOLD_USDT = -15.0        engine_15m.py:57   LOSS_THRESHOLD_USDT = -15.0

signal_weights.py:132      if pnl >= WIN_THRESHOLD_USDT:
signal_weights.py:134      elif pnl <= LOSS_THRESHOLD_USDT:
```

**Declared twice, in two files, compared raw.** Four call sites total, all four are the two
comparisons above. **No notional, margin, size, leverage, R or ATR term appears anywhere near
either.** Nothing reads the position's size before classifying it.

Their own surviving comment names the calibration they were written for:

> *"At \$2000 margin × 5x = \$10,000 notional, +\$500 = +25% ROI on margin; -\$300 ≈ -15% ROI on
> margin. These are the live-mode targets. TEMPORARY (set 2026-05-12, scaled 2026-05-15): lowered for
> the 30-cycle virtual observation window."*

They were lowered **for the paper window** and never raised again — and then the notional went the
other way by 68×.

## 3b. Live-era grades that could have crossed: **ZERO of 6**

| vpos | 1R (USDT) | realised | R | **R to reach +20** | **R to reach −15** | best MFE | worst MAE |
|---|---:|---:|---:|---:|---:|---:|---:|
| 86 | 2.4866 | −2.5416 | −1.022 | **8.04R** | 6.03R | +0.099R | −0.920R |
| 87 | 1.8628 | −0.8191 | −0.440 | **10.74R** | 8.05R | +0.615R | −0.486R |
| 88 | 1.7918 | −0.5311 | −0.296 | **11.16R** | 8.37R | +0.076R | −0.232R |
| 89 | 1.6610 | +2.3024 | +1.386 | **12.04R** | 9.03R | +1.697R | −0.143R |
| 90 | 2.0091 | −0.6099 | −0.304 | **9.95R** | 7.47R | +0.175R | −0.333R |
| 91 | 1.3234 | −0.6410 | −0.484 | **15.11R** | 11.33R | +0.661R | −0.557R |

**Mean 11.2R to register a win. Mean 8.4R to register a loss. Best case across all six: 8.04R.**

The best MFE ever achieved live is **+1.697R** (vpos 89) — less than a quarter of the way to the
easiest win threshold in the sample.

🔴 **The loss side is unreachable BY CONSTRUCTION.** The protective stop caps a live loss at ~1R.
Largest live loss ever: **−2.5416**. Deepest adverse excursion ever observed live: **−0.920R**.
Reaching −15 USDT needs **6.0R at best** — **the stop must fail first**. So at live size the table
is not merely hard to move; it is **one-sided by construction**, and the side it could theoretically
move on needs an 8R runner.

**When did a weight last actually move?** (`updated_at` is bumped on neutral grades too, so it does
not answer this — the last threshold-crossing grade does):

```
audit_at 2026-07-20 02:24:17   score  -103.535   trade 17092    <- the last one, PAPER era
audit_at 2026-07-11 16:35:00   score   -74.610   trade 14999
audit_at 2026-07-06 23:12:25   score   -50.639   trade 13739

live flip: 2026-07-29 19:13:33   ->   grades since: 6   threshold-crossing: 0
```

**No weight has moved at any point in the live era, and none can.**

## 3c. The size of the mismatch in R — RECORDED, NOT PROPOSED

```
PAPER 1R  mean 124.3608 USDT  (n=24, median 126.3231)     [$10,000 notional]
LIVE  1R  mean   1.8558 USDT  (n=6,  median   1.8273)     [$150 notional]
ratio 67.0x   (notional ratio 10,000/146 = 68.5x — the 1R ratio tracks it)

what +20 / -15 MEANT at paper size  :   +0.1608 R   /   -0.1206 R
the same meaning in LIVE dollars    :   +0.2985 USDT /  -0.2238 USDT
the constants actually in force     :   +20.0        /  -15.0
                                        => 67x too high  /  67x too deep
```

**Sanity check that this is the right reading:** at paper size **20 of 24 closes (83%) crossed a
threshold** — a bar of ~0.16R is cleared by almost any real outcome. At live size, **0 of 6**. The
mechanism did not get stricter; the yardstick stopped being a yardstick.

**No change is proposed and none was made.** The numbers are here so the size of the mismatch is on
the record, and because adopting them interacts directly with §4 below.

## 3d. Yes — the frozen table is still shown to the advisor

```
main.py:2001 / 3776    weight_used = signal_weights.get_weight(combo)
main.py:2022 / 3850    consult_for_entry(symbol, snapshot, weight_used, ...)
claude_advisor.py:342  f"Combo weight: {weight:.2f} (1.0 baseline; <1 = historical loser, >1 = winner)\n"
```

**Not hypothetical.** Verbatim from the stored entry prompt of **trade 19713 — a LIVE, real-money
entry on 2026-07-30**:

```
Combo weight: 0.90 (1.0 baseline; <1 = historical loser, >1 = winner)
```

That **0.90** came from a **single paper evaluation of ≈ −78.70** at 68× the notional, and the prompt
presents it to the model as *"historical loser"*.

**7 of 52 combos currently carry a weight ≠ 1.00.** Their judgements date from **2026-05-26 to
2026-07-20** — the newest is 14 days old, and none can ever be revised at the current size:

| weight | evals | total_pnl | last | combo |
|---:|---:|---:|---|---|
| 0.80 | 4 | −154.17 | 2026-07-20 | `…Any Bullish Confirmation\|HyperWave Signal Up\|Bullish…` |
| 0.90 | 2 | −103.86 | 2026-05-26 | `…Bearish Confirmation\|HyperWave Signal Down\|Bearish…` |
| 0.90 | 1 | −127.44 | 2026-06-03 | `…Trend Catcher Down\|HyperWave Signal Down\|Bearish I…` |
| 0.90 | 1 | −106.86 | 2026-06-10 | `…Bearish Confirmation+\|HyperWave Signal Down\|Within…` |
| 0.90 | 2 | −79.52 | 2026-07-30 | `…Bullish Confirmation+\|HyperWave Signal Up\|Within B…` |
| 0.90 | 1 | −32.73 | 2026-07-06 | `…Any Bearish Confirmation\|HyperWave Signal Up\|Withi…` |
| 0.90 | 1 | −74.61 | 2026-07-11 | `…Trend Catcher Up\|HyperWave Signal Up\|Bullish S-BOS` |

**So the answer to (d) is: the mechanism cannot update, but its output is still presented to the model
as current fact, in a sentence that tells the model how to interpret it.** That is a live influence
channel regardless of whether it can ever change.

**One boundary worth having:** the **subtype** store is *not* exposed this way. `claude_advisor`
never imports `engine_15m`, and `hw_weight` reaches only Telegram lines. **This channel is
combo-weights only.**

---

# 4. §2.4 — NOT RUN, AND RECORDED AS HEAVIER

Recorded as **OPEN-ITEMS §2.41**.

```
COMBO   weights : 29 of 53 would move   (26 by +/-0.10, one 0.80 -> 0.60)
SUBTYPE weights :  4 of 16
     HW_SIGNAL_SHORT  0.85 -> 1.00      HW_SIGNAL_LONG  0.75 -> 0.85
     HW_OB_SHORT      1.00 -> 0.90      REVERSAL_LONG   1.00 -> 0.95
```

**Both of the two most-used subtypes would stop being marked as losers.**

🔴 **§3 makes this weightier, not lighter, and that is the framing now on the record.** If a weight
can never move again at live size, then **whatever value this re-grade writes is the value that combo
carries permanently** — and §3d shows it is carried into the advisor's prompt on every future entry,
labelled *"historical loser / winner"*. It would not be a repair that later evidence corrects. **It
would be a final, unrevisable judgement, derived from a paper era at 68× the notional.**

**Deferred. Not housekeeping. It requires a decision that also answers §2.40 — because writing
permanent weights while the update mechanism is inert *is* the decision, whichever way it goes.**

---

# 5. vpos 91's HELD BRANCH — IT TERMINATED. TALLY 4 → 5.

Computed the way vpos 90's was: real 5m/1m BingX candles, **intrabar ambiguity resolved AGAINST the
held branch**, **seeded from the position's real state at the advisor's close**.

**The seed, read off the row rather than assumed:**

```
closed 2026-08-03T13:41:09.328Z  reason=ai_exit  exit 62871.4  net -0.6410
sl 63224.6 == original_sl_price   (never moved)
breakeven_applied = False
water_mark 62268.6 = +0.661R   ->  the +1R arm at 62073.8 was NEVER reached
partial_taken = None            ->  no breakeven, no trail; the original stop stands the whole time
```

**Termination, at 1m resolution:**

```
13:52  O 63049.9  H 63225.0  L 63049.8  C 63102.1   <== first touch, +0.4 pts over the stop
13:55  O 63144.8  H 63287.7  L 63144.8  C 63208.9   <== clears by +63.1 pts
13:56  O 63208.9  H 63233.4  L 63208.8  C 63211.8   <== clears by +8.8 pts
```

⚠️ **The thin margin is disclosed, and the datapoint does not depend on it.** The first touch cleared
by **0.4 pts** on a **last-price** candle while the real stop triggers on **MARK** (`workingType =
MARK_PRICE`, which ran ~0.7 pts above last earlier today). The rule resolves that against the held
branch — but three minutes later the bar cleared it by **63.1 pts**, so the termination is
unambiguous on any reading.

**Arithmetic:**

```
held gross  (62649.2 - 63224.6) x 0.0023                    = -1.32342
fees        entry 0.072047 + exit 0.072709 (taker 5.0 bps)  =  0.144756
HELD net (funding NOT ledgered -> biases toward the held branch) = -1.46818
ADVISOR actual net                                              = -0.64100
ADVISOR - HELD = +0.82718 USDT = +0.625R      -> IMPROVED
```

**The tally, all five held branches now terminated:**

| vpos | side | held-branch outcome | advisor net | held net | advisor − held |
|---|---|---|---:|---:|---:|
| 87 | LONG | `sl` @ 64028.8, bar 07-31 07:05 | −0.8191 | −2.0110 | **+1.1919** |
| 88 | SHORT | breakeven → `trail` @ 63192.2, bar 07-31 17:50 | −0.5311 | +0.8914 | **−1.4225** |
| 89 | SHORT | `trail` @ 63171.3, bar 07-31 17:50 | +2.3024 | +1.0703 | **+1.2321** |
| 90 | SHORT | `sl` @ 63491.9, bar 08-02 02:05 | −0.6099 | −2.1541 | **+1.5442** |
| **91** | SHORT | **`sl` @ 63224.6, bar 08-03 13:52** | **−0.6410** | **−1.4682** | **+0.8272** |

```
NET n=5 : advisor -0.2987  vs  held -3.6716  ->  advisor +3.3729 USDT.  Improved 4, worsened 1.
          (+2.5457 at n=4 after vpos 90 resolved; +1.5852 when vpos 90 was still a mark)
```

**Also retired: §2.4's caveat 3.** vpos 90's held branch — the one that "could still change sign" —
terminated at its stop on 08-02 02:05. **All five held branches are now resolved. No datapoint can
still change sign.**

🔴 **n = 5 of ~10. Five more closes needed. The bar does not move, the sample is not re-cut, and
every advisor close counts.** Caveats 1, 2, 4 and 5 stand: fees still exceed the sample's realised
P&L; no closing threshold is readable from a distribution whose deepest adverse consult is −0.36R;
the held branches are **mutually exclusive** at `MAX_POSITIONS_PER_SIDE = 1` (holding 88 means 89, 90
and 91 could never have opened, so this is **per-position arithmetic and not a portfolio result**);
and from `3316e8a` the sample is loss-streak-filtered.

---

## WHAT WAS CHANGED, AND WHAT WAS NOT

| | |
|---|---|
| **DB writes** | exactly 3 `trades` rows, 3 `signal_weights` rows, 3 `hyperwave_weights` rows — `total_pnl` / `audit_score` / `audit_at` only. Verified by full-table diff |
| **Code** | **none.** No `.py` file was touched in this pass. HEAD is still `ca90c2f` |
| **§2.4 (the 44-row re-grade)** | **NOT RUN.** Recorded as OPEN-ITEMS §2.41 with its numbers and the permanence framing |
| **`learning_*` columns** | **NOT touched.** Left and marked, OPEN-ITEMS §2.39b |
| **Weights / thresholds / gates** | **unchanged.** Nothing in §3 was adopted — it is measurement only |
| **Book sources** | still untouched — the separate, attributable question |
| **Backup** | `/root/titan-bot/trades.db.bak_gradefix_20260803`, `integrity_check: ok` |
| **Live position** | **flat** — vpos 91 closed on the advisor's own verdict at 13:41:09, before any of this ran |
