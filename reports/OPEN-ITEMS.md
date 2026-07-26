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

---

## 6. ACTIVATION CRITERION — exit advisor (recorded 2026-07-26, BEFORE any data exists)

**The exit advisor goes live only if, over the first ~10 closed positions, its FIRST "close"
verdict beats the actual exit BOTH in total USDT AND in the number of positions improved.
Otherwise it stays in record mode.**

**No partial credit. No re-cutting the sample.** The window is the first ~10 closed positions after
the advisor starts recording — not the best ten, not ten chosen afterwards. "Beats" means both
conditions together: total USDT higher, and more positions improved than worsened. One condition
without the other is a failure.

Written before the first verdict exists, precisely so it cannot be adjusted to fit the result.

Cross-check when the window closes: the 27-moment backtest (2026-07-26 19:37 report) gave +67.30 USDT
across 6 positions, 3 improved / 1 worsened / 2 unchanged — with the whole delta carried by two
trades. That was a plausibility check, not evidence, and it does not count toward this criterion.

## 7. ENTRY advisor is blind to the 1H signal identity

`AI_ADVISOR_HIDE_1H = True` (config.py:337). The entry prompt names two of the three tiers —
`15m: HyperWave Signal Up`, `5m trigger: Bullish OB Created` — but never the 1H alert that set the
trend. It sees only the OHLCV-derived state, `1h: BULL, ADX 16.9`.

Consequence: it cannot distinguish signals with identical matrix weight and opposite records —
`Bearish Confirmation+` (weight 1.0, n=4, net **+1063**) and `Trend Catcher Up` (weight 1.0, n=6,
net **-68**) both reach it as "1h BULL".

Candidate change: one line above the existing 15m line —
`1H trend set by: <signal> (weight w, set Nh ago)` — sourced from the same `1h_trend_set` lookup
already written for the exit advisor (`_entry_signals_for`). The prompt would then read
*"1H Trend Catcher Up + 15m HyperWave Signal Up + 5m Bullish I-BOS"* instead of *"aligned bullish"*.

**Deliberately out of scope for the 2026-07-26 session: it modifies the ENTRY path.** The per-signal
n is also thin (largest cell n=6), so the advisor would be handed identity it cannot yet calibrate.

## 8. ROTATE THE ANTHROPIC API KEY (2026-07-26)

A live `ANTHROPIC_API_KEY` sat in plaintext in two **world-readable** cron logs for twenty days:
`/var/log/titan_counter_short_filter_review.log` (07-08, 07-15, 07-22) and
`/var/log/mercury_sol_30trade_reminder.log` (07-06, 07-20). Five occurrences, 644 perms.
Cause: `.env` had `ANTHROPIC_API_KEY= <value>` — leading space, no quotes — and
`set -a; . "$ENV_FILE"` made bash execute the value as a command and echo it to stderr.

Purged, permissions locked to 600, `.env` quoted, and the sourcing replaced on both bots with a
non-executing parser. **The key itself is unchanged and must be rotated — that is the Boss's call.**
Both bots share it (`project_shared_anthropic_key`), so rotation touches Titan and Mercury-SOL.

Lower severity, same class: two Telegram bot tokens appeared in `syslog.2.gz`/`syslog.4.gz`
(13 lines, `640 syslog:adm`) because the mercury-sol optimizer listener prints a `requests`
exception containing the full bot URL. Archives redacted; the listener still does it.

## 9. Sensor cleanup applied 2026-07-26
RETIRED -> `/root/titan-bot/retired_sensors/`: counter_short_filter_review, toln_short_cohort_watch,
prior_move_logger. REDEFINED: chop_short_flat_gap (gap1h='Flat' under regime='TREND'),
regime_flat_high_adx (window 3d -> 21d, now N=5/12 instead of a permanent 0).
RECLASSIFIED as data sources, still running: ob-density collector, smart-exit sampler — the exit
advisor reads both. Only the dryrun VERDICT fields are deprecated; the sampler code was not touched.
