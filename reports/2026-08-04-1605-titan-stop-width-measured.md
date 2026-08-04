# IS THE STOP TOO TIGHT? NO — AND THE DATA LEANS THE OTHER WAY

**2026-08-04 16:05 UTC · Titan LIVE, real money, flat · HEAD `14319a5`, UNCHANGED — no code shipped**

Pre-registered **branch 3** fired: no level in the tested set beats 2.5, so **the stop is not the
leak**. `SL_ATR_MULT` stays **2.5**.

⚠️ **Because the level did not change, every R-multiple in this book stays comparable — no new
boundary is created.** Had it moved, R before and after would have been different units and §0 would
have needed a cut like the paper/live one.

Canon: **§2.49** added in the same commit; snapshot `reports/2026-08-04-1605-open-items.md`.
Basis: OPEN-ITEMS §2.2 (Variant C), §2.16, the post-exit observatory tables.

**Naming, corrected in passing:** the constant is **`SL_ATR_MULT`** (with `SL_ATR_TF = '1h'`), not
`SL_BUFFER_ATR` — there is no `SL_BUFFER_ATR` in this codebase. Your description of what it does is
exactly right: it is a round number, never derived, and it sets 1R.

---

## 🔴 THE ANSWER, AND THE MECHANISM

```
SL_ATR_MULT      clean-40 total R     validated mech-24     LONG      SHORT
2.0  (control)        +7.66                +3.57            +1.36     +6.30
2.25 (control)        +6.18                +4.92            +1.30     +4.88
2.5  TODAY            +2.92                +2.26            -0.47     +3.39
3.0                   -1.95                -1.38            -5.19     +3.24
3.5                   -4.26                -3.62            -5.19     +0.93
4.0                   -5.39                -2.49            -7.03     +1.64
```

**Widening is worse at every level, on both cohorts, on both sides.** The mechanism is the one your
brief anticipated and it is stronger than expected: **widening moves 1R, and the breakeven arm, the
LONG partial and the trail-arming threshold are ALL keyed to +1R.** A wider stop pushes the finish
line away faster than it buys survival. At 3.0 it **rescues 1** stop-out, **flips 5 winners into
losses**, and **shrinks 22 winners by 9.38R**.

---

## 1. §1c — VALIDATION FIRST, AND ITS LIMIT IS PART OF THE RESULT

The contract was replicated exactly from stored inputs — 1R = |entry − original_sl|, ATR1h recovered
as 1R/2.5 (exact), **size fixed** by `FIXED_NOTIONAL_MODE`, LONG partial 1/3 at +1R, breakeven at +1R,
trail armed only after breakeven, never-loosen, intrabar **adverse-first** — over **23,233 real 5m
BingX candles**.

| check | result |
|---|---|
| **stop-exits reproduced** | 🟢 **11 of 11 within 0.09R** — residual is fees, exactly as §2.2 found at width 1.0 |
| mechanical exits overall (`sl`/`breakeven`/`trail`) | **18 of 24 within ±0.15R** |
| the 6 misses | breakeven-vs-stop **ordering inside one bar**: the live stop triggers on **MARK**, the candles are **LAST** |
| 🔴 **positions the contract never owned** | **16 of the 40** clean positions exited `external` (9), `ai_exit` (6), `post_entry_critical` (1) |

🔴 **That last row is the honest limit, and I am not burying it:** for those 16 the replay
**substitutes** a mechanical outcome for what actually happened. That is a modelling assumption, not a
measurement. **So the curve is reported on BOTH cohorts — the validated mechanical 24 and the full
clean 40 — and they agree at every level.** The agreement is what gives the conclusion standing; the
replay alone would not.

*(A second limit, stated rather than left implicit: widening the stop changes the price path the exit
advisor would have seen, and the advisor has been live since 07-30. No replay can model what it would
have decided. This biases nothing in a known direction — it is simply unmodellable.)*

## 2. §1a — AFTER A STOP, PRICE DOES COME BACK. IT COMES BACK SLOWLY.

Favourable travel after the stop fill, §0-clean stop-exits (n=12), in R — distribution, not just the
mean:

| horizon | median | p25 | p75 | max | share reaching +1R |
|---|---|---|---|---|---|
| 1h | +0.26R | +0.09 | +0.41 | +1.06 | 8 % |
| 4h | +0.45R | +0.13 | +1.03 | +1.10 | 25 % |
| 12h | +0.85R | +0.27 | +2.14 | +2.44 | 42 % |
| **24h** | **+1.29R** | +0.27 | +2.41 | +3.08 | **50 %** |

**Per side:** LONG (n=6) recovers faster early — median +0.32R at 1h, +0.73R at 4h, 33 % reaching
+1R by 4h. SHORT (n=6) is flat early (+0.16R at 1h, 0 % reaching +1R) and catches up by 24h. Both hit
50 % at 24h.

**The observatory's "~65 % continue in favour" is confirmed in direction.** But the recovery is a
**12–24 hour** phenomenon, and that is exactly why the wider stop cannot harvest it: the position
would have to survive a deeper excursion *and then* travel to a **farther** breakeven arm before the
contract banks anything.

## 3. §2 — THE COST OF WIDENING, WHICH IS WHAT DECIDES IT

Full-contract replay, winners and losers, not just the rescued stop-outs:

| level | clean-40 total R | win % | mean R | median R | LONG | SHORT |
|---|---|---|---|---|---|---|
| **2.5 (today)** | **+2.92** | 60.0 % | +0.073 | +0.140 | −0.47 | +3.39 |
| 3.0 | −1.95 | 50.0 % | −0.049 | +0.077 | −5.19 | +3.24 |
| 3.5 | −4.26 | 47.5 % | −0.107 | −1.025 | −5.19 | +0.93 |
| 4.0 | −5.39 | 47.5 % | −0.135 | −1.022 | −7.03 | +1.64 |

**§2b — who changes:**

| level | stop-outs rescued | winners flipped to losses | winners shrunk | by how much |
|---|---|---|---|---|
| 3.0 | 1 | **5** | 22 | **−9.38R** |
| 3.5 | 2 | **7** | 22 | **−13.74R** |
| 4.0 | 3 | **8** | 22 | **−16.64R** |

**§2c — the shape: monotone downward** as the stop widens on the pooled book and on LONG. SHORT
wobbles (+3.39 → +3.24 → +0.93 → +1.64); the rise at 4.0 after the dip at 3.5 is non-monotone, i.e.
noise, and it never approaches the 2.5 baseline.

**Of the last 25 entries, 12 change outcome at 3.0 for a net −4.33R** — worst: vpos 75 (+0.36 →
−1.06), vpos 74 (+0.12 → −1.07), vpos 76 (+0.08 → −1.06). Best improvement across all 25: **+0.02R**.
**Live era (n=7): −3.04R → −3.20R.**

## 4. §3 — THE INTERACTIONS, WHICH ARE NOT ADDITIVE

**§3a — 🔴 THE TRAIL DOES NOT FOLLOW 1R.** `trail_pct = TRAIL_MULT_ATR × ATR / entry` is keyed to
**ATR**, not to 1R. Today `SL_ATR_MULT` and `TRAIL_MULT_ATR` are both 2.5, so **the trail width is
exactly 1.00R** — verified on every recent position (`trail_pct / 1R% = 1.000` on vpos 87–92). Widen
the stop and the trail stays 2.5 × ATR:

```
m = 2.5  ->  trail = 1.00R      m = 3.5  ->  trail = 0.71R
m = 3.0  ->  trail = 0.83R      m = 4.0  ->  trail = 0.62R
```

**A wider stop silently narrows the trail in R terms** — and §2.2 disqualified 0.5R for shorts
outright. **Anyone who changes `SL_ATR_MULT` must decide `TRAIL_MULT_ATR` in the same commit**, or
the contract changes shape without anyone choosing it.

**§3b — widening makes the LONG partial nearly irrelevant, but never harmful in this range:**

| level | LONG without partial | LONG with partial | partial's contribution |
|---|---|---|---|
| **2.5** | −1.14 | −0.47 | **+0.666** |
| 3.0 | −5.31 | −5.19 | +0.121 |
| 3.5 | −5.38 | −5.19 | +0.189 |
| 4.0 | −7.19 | −7.03 | +0.161 |

+1R moves away, fewer longs reach it, the partial stops mattering. It does **not** go negative here —
unlike §2.2's trail-narrowing at 0.5R. **Same family of lever, same diminishing return: §2.2's
substitutes finding, confirmed from the other direction.**

## 5. THE DECISION — pre-registered branch 3

| your branch | verdict |
|---|---|
| a level materially better on **both** sides, monotone up to it, ≥8 trades affected → apply | **FAILS.** No tested level beats 2.5 on either cohort or either side |
| better on one side only → record and stop | not reached |
| **non-monotone / gain inside noise / <8 affected → APPLY NOTHING, the stop is not the leak** | 🔴 **FIRED** |

**Applied: nothing.** No constant changed, no restart. `git status` clean at `14319a5`, the binary
running since 15:36:11, `virtual_positions` holds 0 open rows. All measurement was **read-only**.

### 🔴 THE TIGHTER SIDE — MEASURED, NOT APPLIED

The control extension shows **2.0 and 2.25 beat 2.5 on both cohorts and both sides** (+7.66R and
+6.18R vs +2.92R on the clean 40; LONG turns positive at both). **I am not applying it**, for one
reason that is not negotiable: **it was not in the pre-registered branch set.** You registered
2.5/3.0/3.5/4.0 and three outcomes. Acting on a level discovered *after* seeing the numbers is exactly
what pre-registration prevents — §4's items 3, 9 and 10 were all born that way, and I have refused
this same temptation twice today already.

**Pre-registered NOW, for a pass that has not been run:** a tightening to 2.25 or 2.0 applies only if
(a) it beats 2.5 on total R on **both** cohorts **and both sides**, (b) the curve is **monotone**
through it, (c) **≥8** trades change outcome, and (d) the **fee share of 1R is stated at the new
level** — fees are ~0.08R of 1R at today's $150 notional and **grow as 1R shrinks**, which is the
specific way a tight stop looks free and is not. **And the replay's two known biases run in favour of
tight stops** — adverse-first intrabar resolution, and MARK-vs-LAST (the source of all 6 validation
misses) — **so the tighter side is flattered by exactly the machinery that would be used to justify
it.** That must be stated in that pass, not discovered after it.

## 6. SCOPE

Nothing was touched: the EMA envelope gate, the HTF cascade, the FLAT floor, Variant-B, the score
bars, the risk gates, both advisor prompts, and the exit advisor's inputs are all unchanged — **there
is no diff.** No snapshot, no `py_compile`, no restart, because there is nothing to apply. Measurement
ran read-only against `trades.db` and 23,233 BingX 5m candles cached in scratch; **no table was
written**.
