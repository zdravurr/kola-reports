# TITAN — OPEN ITEMS

Diagnosed but **not applied**. This file exists so nothing is lost between sessions.
Every entry states what is known, what is NOT known, and what would close it.

_Last updated: 2026-07-26 (session: recheck bound · counter-short caution retired · LONG partial shipped)_

---

## 1. 🔴 LIVE-PATH PARITY GAP — LONG partial exists in paper only

`virtual_trader.py` now takes a 1/3 partial at +1R on LONGs (`f7df202`).
**`breakeven_worker.py` — the live path — has no equivalent.**

* Harmless today: `LIVE_TRADING_ENABLED = False`, so every position is paper.
* **If live is ever enabled, longs would behave differently in live vs paper** — the paper book
  would bank a tranche at +1R and the live book would not, and the two would diverge silently.
* **MUST be closed before `LIVE_TRADING_ENABLED` is set True.** This is a blocking item, not a
  nice-to-have.
* Same class of gap to check at that time: the R1 recheck bound (`93c20c3`) and the FLAT score
  floor also live in the paper/entry path — verify parity for each before going live.

## 2. LONG partial parameters are PLACEHOLDERS, not findings

`LONG_PARTIAL_LEVEL_R = 1.0`, `LONG_PARTIAL_FRACTION = 1/3`.

* Chosen as the conservative corner of the tested grid (the only partial variant that cut zero
  winners in simulation), **not** because the data selected them.
* n = 10 clean longs, of which **6 ever exceeded 0.5R and 5 were winners**. One trade decides the
  ranking: 0.75R beats 1.0R entirely because it catches vpos 41 (peaked 0.91R, ended −1.05R).
* **Retune when ~30 clean long closes with MFE above 0.5R exist.** Current: 6.
* Kill switch: `LONG_PARTIAL_ENABLED = False` restores the previous contract exactly, no code edit.

## 3. Variant C (narrower LONG trail) is UNEVALUATED — not rejected

A narrower trail exits at the first retracement of its own width from the **running** peak, so it
can exit before the global peak is reached.

* Simulating it from endpoints (MFE, exit) assumes the global peak came first — an **optimistic
  upper bound**, not an estimate. Under that bound it looked good: LONG +164.76 at 0.5R width.
* Real excursion paths exist only for `position_excursion_samples` (vpos 61+), and among clean,
  **armed** positions that is **one long (vp79) and one short (vp81)**. Path and bound agreed on
  both — on n=1 per side, and only because those two paths rose near-monotonically.
* **Revisit when path coverage extends.** The excursion logger now runs on every position, so this
  resolves itself with time and needs no new work.

## 4. Entry-advisor order-book calibration — one confirmed miscalibration, scale unmeasured

`trades.id = 18631` (2026-07-26 10:55, SHORT, `ai_skipped`), advisor reason verbatim:

> *"1h BULL + 1h ADX 13.5 (weak) opposes SHORT. **Massive ask wall ×5.9 above entry blocks upside.**
> MTF alignment 0/4. Statistical headwind -0.49%/12h. Skip."*

An ask wall **above** entry is overhead supply — it blocks upside, which is a **tailwind for a
SHORT**, not a reason to skip one. The advisor read a supporting feature as an opposing one.

* **What is known:** one instance, verbatim, in the stored payload/reason pair.
* **What is NOT known:** whether this is systematic, how often it flips a verdict, or whether the
  same confusion runs the other way on LONGs. No frequency, no direction, no cost estimate.
* **To close:** classify wall-side references across all stored `ai_reason` texts by trade side and
  wall side, and measure how often the sign is wrong. `ai_user_prompt` + `ai_reason` are both
  persisted for 2,685 decisions, so this is a read-only study needing no new instrumentation.

## 5. Exit advisor — existence and capability not yet established

`claude_advisor.consult_for_close()` exists in the code. **Nothing is known about whether it is
wired in, how often it fires, or whether its verdicts are any good.**

* The book shows 9 `external` closes across 49 positions, but they have not been traced to a
  caller, and no equivalent of `ai_user_prompt` / `ai_reason` has been checked for the close path.
* **To close:** trace the call sites, count invocations, and — if it fires — apply the same
  evidence discipline used on the entry-side caution (does the payload reach it, does the reasoning
  reference it, does it change a decision).

---

## Watch-list items still accumulating (not defects — just waiting for n)

| item | current n | needed | note |
|---|---|---|---|
| Prior-move bucket (R2) | SHORT mid/late = **0** | SHORT observations in mid/late | logger running; months away |
| Chop-short gap=Flat | 1 of 5 new | 5 | FLAT gate now starves this cohort — may never fill |
| Smart-exit chop giveback | **0 armed** chop samples | ~5 chop closes that arm | same starvation risk |
| Order-book percentile veto | 9 entries with book data | ~15–20 | baseline is healthy (19k+ snapshots) |
| TOLN short cohort | 1–2 | 6 | |
| regime-FLAT high-ADX | 0 | 12 | |
| vol_ratio_5m ceiling (R4) | 7 SHORT (2 winners) | more winners | **build with the deterministic `row_id % 2` A/B arm from the start** |

---

## Closed this session (for context, not action)

* `93c20c3` — post-entry recheck TIGHTEN bounded at the original stop distance.
* `b878535` — counter-trend EMA-1h soft caution retired (founding statistic did not reproduce;
  cohort sign inverted on post-06-27 data).
* `f7df202` — LONG partial realisation, 1/3 @ +1R, LONG-only.
* Earlier: wall-trail disabled (`5f1b073`), phantom-wall recheck trigger zeroed (`c845941`),
  FLAT-regime score floor enforced (`db71454`).
