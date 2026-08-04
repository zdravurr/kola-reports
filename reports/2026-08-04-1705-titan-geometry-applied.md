# THE GEOMETRY MOVES — SL 2.5→2.25, TRAIL 1.00R→0.75R. AND THE WICK STORY WAS WRONG TOO.

**2026-08-04 17:05 UTC · Titan LIVE, real money · applied 17:01:29 from FLAT · commit `be53e63`**
**`SL_ATR_MULT = 2.25` · `TRAIL_MULT_ATR = 1.6875` (0.75R) · sampler 60 s → 10 s · `py_compile` clean**

🔴 **1R CHANGED. The §0 boundary is recorded in the same commit: R-multiples do not pool across
2026-08-04 17:01:29 UTC.** Split predicate `opened_at >= '2026-08-04T17:01:29'`. Applied from flat, so
**no position spans it**.

Canon: **§2.53** plus the **§0 boundary block**. Snapshot: `reports/2026-08-04-1705-open-items.md`.

---

## PART 1 — THE SAMPLER, APPLIED

`EXCURSION_SAMPLE_SEC 60 → 10` · `EXCURSION_DENSE_UNTIL_SEC 900 → 172800` (48 h).

**10 s and not 5 s:** the poll loop that *drives* the sampler runs at 5 s, so 10 s guarantees it can
never outpace its own driver — and it is the cadence Mercury-SOL's 2026-08-01 fix validated
(305 s → 10 s, peak replay error 0.298R → ~0.05R).

**Storage, measured from `dbstat` at 130 bytes/row — not estimated:**

| | rows | size |
|---|---|---|
| median position (6.2 h) | 2,249 | **286 KB** |
| p90 (38.6 h) | 13,895 | 1.77 MB |
| max observed (74.3 h) | 26,759 | 3.4 MB |
| **at 0.47 entries/day** | | **0.13 MB/day** |

**The three properties, by construction rather than by assertion:**
1. **It gates nothing** — the only writer is `_record_excursion_sample`, called once per poll tick
   inside a `try/except` (`virtual_trader.py:2432`); a failure prints and returns.
2. **No exit logic reads the table** — `grep` finds **no reader anywhere** in the codebase except
   that function's own `MAX(elapsed_s)` throttle query. Not the exit path, SL, trail, breakeven,
   advisor or optimizer.
3. **It cannot slow or block trading** — it writes only to its own table, never to `trades` or
   `virtual_positions`, and the call is already inside the poll tick that was happening anyway.

## PART 2 — BUILDING THE HONEST INSTRUMENT

### 🔴 Your design needed one repair, and I am flagging it rather than quietly working around it

> *"ARMING comes from the ENGINE'S OWN RECORD, never inferred. It is exact on all 59."*

**It is exact at SL 2.5 — and only there.** At a tighter SL, 1R shrinks, so the +1R arming level moves
**closer to entry**: a position that never armed at 2.5 may arm at 2.0, and one that armed may be
stopped out earlier. **The record cannot be carried into counterfactual cells.**

**I tried to calibrate around it and it failed, which is worth reporting as a negative result:** fit a
threshold θ so "armed iff the path exceeds +1R by ≥ θ·1R" reproduces the record. The two populations
overlap almost exactly — **truly-armed median penetration 0.0734R, falsely-armed median 0.0743R** —
and the best θ reaches **76.3 %**, no better than the raw proxy it was meant to replace.

### 🔴 And that failure exposed the real defect: it was never wicks

Of the 15 candle-armed / engine-not-armed positions, **8 exited `external`, `ai_exit` or
`post_entry_critical`**. **The replay outlived the real position** — the advisor closed it before
+1R, and the replay kept running and found +1R afterwards. Test:

| | untruncated | **truncated at the real close** |
|---|---|---|
| candle wicks | 75 % | **96.7 %** |
| candle closes | 76 % | **98.3 %** |

**That is a timeline error, and it supersedes the wick explanation I gave in §2.51 and §2.52.** My
"over-arming on wicks the poller never saw" was the wrong mechanism for most of the disagreement.

### The instrument that results

**On §2.50's own cohort the timeline problem does not arise** (mechanical exits only — the contract
produced the exit), and there the closes basis is **exact**:

| check | result |
|---|---|
| **arming vs the engine's record**, §0-clean mechanical 24 | **24 of 24 = 100 %** |
| **outcomes** within ±0.15R, same cohort | **21 of 24** (mean \|Δ\| 0.077R) — vs 18 of 24 for wicks |

**Exact where the record exists, inferred only on the post-arm path, on the cohort whose timeline is
real.** That is what none of a/b/c was.

## THE GRID RE-RUN — §2.50's own cohort, §2.50's own rules

R_ref in **today's fixed 1R**, fees at each cell's own 1R (0.081 / 0.090 / 0.101), same 3×3×2 grid,
same four conjuncts. **mech-24 / clean-40:**

| SL \ trail (partial ON) | 0.75R | 1.0R | 1.25R |
|---|---|---|---|
| **2.0** | +6.62 / +6.65 | +4.92 / +3.81 | +2.77 / +2.75 |
| **2.25** | 🟢 **+5.20 / +6.13 — APPLIED** | +2.83 / +4.07 | +0.64 / +1.21 |
| **2.5 (was)** | +3.55 / +6.26 | **+0.84 / +3.82** ← was | −1.22 / +0.77 |

🔴 **The SL axis is MONOTONE on the honest instrument** — +3.55 → +5.20 → +6.62 at trail 0.75R —
where on wicks it turned at 2.25. **The turn that rejected all six cells in §2.50 was an artifact of
the lying instrument. Conjunct (c) was doing its job on a lying instrument, exactly as you said.**

**Three cells passed all four conjuncts** (2.25/0.75/on · 2.0/0.75/on · 2.25/0.75/off); the
tie-break took the **closest to today**. Both sides improve on both cohorts:

| | LONG | SHORT |
|---|---|---|
| mech-24 | −3.14 → **−2.02** | +3.98 → **+7.22** |
| clean-40 | −2.09 → **−0.74** | +5.91 → **+6.87** |

## PRE-REGISTERED BEFORE APPLYING

- **Of the last 25 entries, 24 change outcome, net +5.01 R_ref.** Best: vpos 75 (+1.47), vpos 89 and
  81 (+0.32 each). The six worst are −1.1R stop-outs each improving **+0.10** — because 1R is smaller,
  not because the trade got better.
- **Live era (n=7): −3.01 → −2.17 R_ref (Δ+0.84).**
- **Refusal effect: NONE.** This geometry gates no entry; entry count and the EMA gate's refusal rate
  are untouched. It changes only how an admitted position is managed.
- **Review point: 20 armed positions per side ≈ 279 days** at 0.14 armings/day. 🔴 **Part 1 does NOT
  shorten this**, and I want to correct the expectation in your brief: the sampler does not change how
  often positions arm. What it changes is that **28 % → 100 % of armed positions get a usable path**
  (5 of 18 today). Coverage, not frequency.
- **Risk per trade fell ~10 %** at unchanged $150 notional — a typical 1R goes **$1.796 → $1.617**.

## 🔴 THE RESIDUAL ASSUMPTION, AND WHAT SETTLES IT

**Arming fidelity is validated at SL 2.5 only.** At 2.25 the +1R level moves and no record exists to
check against. That is the one inference left in the chain, and it is now **cheap to close**: the
first ~10 post-boundary positions carry `breakeven_applied` flags that can be scored against this
instrument's prediction **at the new geometry, at 10 s resolution**. **That check is owed**, and it is
the successor to this pass rather than a promise to remember.

## SCOPE

Untouched: the EMA envelope gate, the HTF cascade, the FLAT floor, Variant-B, the score bars, the
risk gates, both advisor prompts, and the exit advisor's inputs. **One file changed (`config.py`),
three constants.** Backup `config.py.bak_sampler_20260804`. Applied with **0 open positions**;
restart **17:01:29**, re-synced at **17:02:04** after correcting the boundary timestamp in the
comments so that disk and process are byte-identical. LIVE banner clean.
