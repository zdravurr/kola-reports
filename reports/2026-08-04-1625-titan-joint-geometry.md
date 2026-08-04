# JOINT GEOMETRY — NOTHING APPLIED, AND THE UNIT IS WHAT DECIDED IT

**2026-08-04 16:25 UTC · Titan LIVE, real money, flat · HEAD `14319a5`, UNCHANGED — no code shipped**

Pre-registered 3×3×2 grid, all four conjuncts required. **Zero cells passed.** `SL_ATR_MULT` stays
**2.5**, `TRAIL_MULT_ATR` stays **2.5**, the LONG partial stays **on**.

⚠️ **No level changed, so every R-multiple in this book remains comparable — no §0 boundary is
created.** The boundary machinery you specified was prepared and is not needed.

Canon: **§2.50** added in the same commit (and §2.49 corrected — see §5). Snapshot:
`reports/2026-08-04-1625-open-items.md`.

---

## 🔴 0. THE HEADLINE IS METHODOLOGICAL: MEASURING GEOMETRY IN R MEASURES PARTLY THE UNIT

`1R = SL_ATR_MULT × ATR × size`. **Tighten the stop and 1R shrinks — so every trade whose path is
unchanged reports a bigger R without one dollar changing.** A grid that ranks cells by "total R" is
therefore partly ranking its own denominator.

| metric | comparable across cells? | what it concluded |
|---|---|---|
| **R per cell** (the naive choice) | ❌ the unit moves with the axis under test | SL axis looks **monotone** (+4.94 → +8.64 → +8.96); **8 cells qualify**; tie-break selects 2.25/1.0R |
| **USDT** | ✅ across cells · ❌ dominated by paper trades at **68×** the live notional | only **2** cells pass (a)+(b) |
| 🔴 **R_ref — net ÷ TODAY's 1R** | ✅ **both**: unit fixed, position size normalised | SL axis is **NON-monotone** (+4.94 → **+7.78** → +7.17); **0 cells pass all four** |

**The naive metric would have shipped a change this morning. The invariant unit refuses it.** I ran
all three; the third is load-bearing. Anyone repeating this must denominate in a **fixed** 1R.

---

## 1. THE GRID (R_ref, partial ON) — mechanical-24 / clean-40

| SL \ trail-in-R | 0.75 | 1.0 | 1.25 |
|---|---|---|---|
| **2.0** | +7.17 / +9.10 | +4.74 / +7.07 | +2.86 / +6.13 |
| **2.25** | **+7.78 / +7.36** | +5.27 / +5.13 | +3.28 / +3.99 |
| **2.5 (today)** | +4.94 / +5.40 | **+2.25 / +2.92** ← today | +0.10 / +0.02 |

*(partial OFF is uniformly at or below partial ON on the clean-40 — it is never the better choice at
any geometry, which settles the third axis by itself.)*

**Fee share of 1R, charged inside each cell at that cell's own 1R — not annotated afterwards:**
**0.081R at 2.5 · 0.090R at 2.25 · 0.101R at 2.0.** Fees do not scale with the stop, so tightening
raises their share by a quarter at 2.0. This is modelled, per your instruction, not disclosed.

## 2. THE DECISION — six cells beat today, and every one fails conjunct (c)

**Passing (a) both cohorts and (b) both sides on both cohorts — six cells:**

| distance from today | cell | mech-24 | clean-40 | trades changed |
|---|---|---|---|---|
| 1 | 2.25 / 1.0R / on | +5.27 | +5.13 | 35 |
| 2 | **2.25 / 0.75R / on** | **+7.78** | +7.36 | 38 |
| 2 | 2.0 / 1.0R / on | +4.74 | +7.07 | 37 |
| 3 | 2.25 / 0.75R / off | +7.53 | +6.57 | 38 |
| 3 | 2.0 / 0.75R / on | +7.17 | **+9.10** | 39 |
| 4 | 2.0 / 0.75R / off | +7.17 | +8.53 | 39 |

🔴 **Conjunct (c) rejects all six. The SL axis turns at 2.25 — at every trail width and both partial
settings:**

```
trail 1.0R , partial on : 2.5 +2.25 -> 2.25 +5.27 -> 2.0 +4.74     turns
trail 0.75R, partial on : 2.5 +4.94 -> 2.25 +7.78 -> 2.0 +7.17     turns
trail 0.75R, partial off: 2.5 +4.68 -> 2.25 +7.53 -> 2.0 +7.17     turns
```

**A candidate sitting on a peak is a non-monotone winner** — the exact shape conjunct (c) exists to
reject, and the same shape as SHORT's 3.5→4.0 wobble in §2.49. **The trail axis is monotone
everywhere** (narrower is better at every SL level, both cohorts), but one clean axis does not carry
a joint change when the other turns under the candidate.

**Applied: nothing.** Per your rule: *if none qualifies, apply nothing and say the geometry is not the
leak.* `git status` clean at `14319a5`, process up since 15:36:11, 0 open positions, no restart.

## 3. THE THREE BIASES — MODELLED. TWO ARE NON-BINDING.

**① Fees at each cell's own 1R** — charged inside the replay, table above. At 2.0 a full round trip
costs **0.101R** versus 0.081R today: a quarter more of the unit, on every trade, win or lose.

**② Adverse- vs favourable-first intrabar — IDENTICAL results:**

| resolution | best cell (2.25/0.75R) | today | margin |
|---|---|---|---|
| adverse-first (default) | +7.78 / +7.36 | +2.25 / +2.92 | **+5.52 / +4.45** |
| favourable-first | +7.78 / +7.36 | +2.25 / +2.92 | **+5.52 / +4.45** |

**The ordering bias is non-binding on this cohort**, which the next item explains.

**③ MARK-vs-LAST — 0 ambiguous bars at every level.** Bars where the stop *and* the +1R level are
touched in the same candle: **zero**, at 2.5 / 2.25 / 2.0 crossed with 1.0R / 0.75R. So the ambiguity
I asked you to size does not exist in this sample, and the winner's margin is not exposed to it.

## 4. 🔴 A CORRECTION TO MY OWN 16:05 REPORT

§2.49 attributed the 6 validation misses to *"breakeven-vs-stop ordering inside one bar (the live stop
triggers on MARK, the candles are LAST)"*. **That mechanism is wrong.** Same-bar ambiguity is
literally zero. Checked on vpos 61 (SHORT, entry 58699.6, stop 59622.0, +1R 57777.2):

```
candle path : +1R first touched 07-01 01:10   ·   stop first touched 07-01 14:10
actual close: 07-01 14:10, reason = sl, -1.076R
```

**Thirteen hours apart — the divergence is ACROSS bars, not inside one.** The replay arms breakeven
on a wick the live engine's 5-second polling never saw, then rides a protected position the real one
never had. **This flatters the replay's protective features — breakeven, partial, trail — on every
cell**, so it largely cancels in cell-versus-cell comparison, but it means **the absolute R levels in
§2.49 and here are optimistic**, and that correction now stands in the canon rather than in my head.

## 5. LIVE ERA AND THE LAST 25 — the one signal that points consistently

**Live era (n=7, R_ref):** today **−3.04** · 2.25/1.0R **−2.44** · 2.25/0.75R **−2.00** · 2.0/1.0R
**−1.84** · 2.0/0.75R **−1.45**. **Monotone in the tightening direction.**
**Last 25 entries** under the best-scoring cell: **24 change, net +3.94 R_ref.**

**Neither is a basis for action** — n=7, and the pre-registered filter is what governs; that is the
whole point of writing it before the numbers. It is recorded so the next pass does not rediscover it
as new.

## 6. WHAT WOULD SETTLE IT — pre-registered now

The open question is narrow and stateable: **does the SL axis really turn at 2.25, or is the turn
sampling noise?** It rests on a handful of paths inside a mechanical cohort of **24**.

**Re-run when the mechanical cohort reaches ≥40 exits** (`sl`/`breakeven`/`trail`), with:
(a) the identical 3×3×2 grid, (b) denominated in a **fixed** 1R — never the cell's own, (c) the same
four conjuncts, (d) fees charged at each cell's own 1R, and (e) the across-bar wick bias stated as a
known optimism in the absolute levels. At ~0.47 entries/day with roughly half exiting mechanically,
that is **~2.5 months**.

## 7. SCOPE

Nothing was touched: the EMA envelope gate, the HTF cascade, the FLAT floor, Variant-B, the score
bars, the risk gates, both advisor prompts and the exit advisor's inputs. **There is no diff** — no
snapshot, no `py_compile`, no restart, because there is nothing to apply. Measurement ran read-only
against `trades.db` and the 23,233 cached BingX 5m candles; **no table was written**.
