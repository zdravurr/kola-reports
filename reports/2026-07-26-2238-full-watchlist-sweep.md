# full-watchlist-sweep

_2026-07-26 22:38 UTC_

---

# TITAN — full watch-list sweep

**2026-07-26 22:40 UTC · READ-ONLY. Nothing changed.** Tree clean at `ef7fa10`.

**Lead with the one thing that is not a sensor question: a secret is sitting in a world-readable
log.** See §5.

---

## Every sensor, with its N *now*

| sensor | schedule | threshold | **N now** | ever fired | status |
|---|---|---|---|---|---|
| `titan_bull_regime_watch.sh` | 08:17 daily | 30 / 3d | **66** | yes, daily since 07-23 | **ACTED** — drift-cut run 07-26 |
| `titan_volfloor_data_watch.sh` | 08:35 daily | 6 / side | **SHORT 7 · LONG 11** | yes, since 07-23 | **READY, with a caveat** |
| `titan_chop_short_flat_gap_watch.sh` | 08:29 daily | 5 new | **1** | never | **STARVED** → redefine |
| `titan_toln_short_cohort_watch.sh` | 08:41 daily | 6 | **1–2** | never | **CAN NEVER FIRE** |
| `titan_regime_flat_high_adx_watch.sh` | 08:53 daily | 12 / 3d | **0** | never | **CAN NEVER FIRE** (window bug) |
| `titan_counter_short_filter_review.sh` | Wed 10:23 | 1 fill / 8 skips | n/a | never (no sentinel) | **DEAD** — filter retired today |
| `titan_prior_move_logger.py` | every 6h | accumulate | 56 records | n/a | **DEAD hypothesis, live cost** |
| `daily_trend_cohort_sensor.py` | Mon 08:11 | — | tracks cohort counts | n/a | cheap, keep |
| smart-exit dryrun (in-bot) | hourly | 5 chop closes | **3 chop pos · 0 armed** | never | **STARVED + superseded** |
| ob-density collector (in-bot) | 60s | — | **19,559** snapshots | n/a | **promote to data source** |
| excursion sampler (in-bot) | per tick | — | 2,258 rows / 22 pos | n/a | keep — feeds R-analysis |
| recheck_events / adaptive_trail | in-bot | — | 25 / 3 | n/a | keep, cheap |
| post-exit observatory | in-bot | — | 36 + 175 samples | n/a | **UNREAD — see §3** |

### The two the earlier reports skipped

**`regime_flat_high_adx` — N=0, and the reason is a window bug, not the FLAT gate.**
The cohort is long *skips* in FLAT + ADX-1h ≥ 25 + 4h bull. The FLAT gate does not suppress skips —
FLAT `ai_skipped` rows since the gate: **123**. Over all history the cohort has **52** members
(June 32, July 20, last on 07-22). But the sensor counts them in a **rolling 3-day window** against
a threshold of **12**. At ~20/month the 3-day expectation is **≈2**. **It is arithmetically
incapable of reaching 12 in 3 days** and never has been. Fix is the window, not the market.

**`TOLN short cohort` — N=1–2 of 6, and the machinery forbids more.**
The cohort is SHORT with 1H NEUTRAL + 15m/5m bear. Of 28 closed shorts, `trend_1h` was
**bear 25 · neutral 2 · bull 1**. The HTF cascade hard-vetoes a direction the 1H tier does not
agree with, so a 1H-neutral short reaching a fill is close to a machine impossibility — the two that
exist predate or slipped the current cascade. **CAN NEVER FIRE while the cascade stands.**

---

## 1. Starved by our own fixes

FLAT-regime entries since the gate (`db71454`, 07-06 13:54): **executed = 0**. Only `ai_skipped`
(123), `virt_cap_blocked` (1), `claude_unavailable` (1).

| sensor | needs | can it ever get it | recommendation |
|---|---|---|---|
| chop-short gap=Flat | 5 new SHORT closes with `gap1h='Flat'` **or** `regime='FLAT'` | the `regime='FLAT'` half is gone forever | **REDEFINE** |
| smart-exit chop giveback | 5 chop closes that ARM | chop entries are gone; 0 of 3 ever armed | **RETIRE** (superseded — §2) |
| regime-FLAT high-ADX | 12 skips in 3 days | not starved — the window is wrong | **REDEFINE the window** |

**REDEFINE for chop-short:** drop the `regime='FLAT'` clause and count
**`ema_gap_dir_1h='Flat'` under `market_regime='TREND'`** — the FLAT gate does not see it, so it
still fires. Historical members: vpos 53 (-106.86) and 60 (-62.03), plus vpos 33 (+0.78) and 40
(-103.86) whose regime pre-dates labelling — **4 of the 6 original losers, -271.97**. Current count
on the strict TREND-only definition: **2**.

**REDEFINE for regime-FLAT high-ADX:** the 3-day window against threshold 12 is the defect. At the
observed rate the cohort needs ~18 days to accumulate 12.

---

## 2. Superseded by today's changes

**smart-exit dryrun — REDUNDANT for its own question, still useful as a data source.**
It asks "would a fixed giveback rule have beaten the real exit on chop entries". It has 3 chop
positions and **zero arms**, so it has never answered. Meanwhile the exit advisor now consults
hourly on the same rows and reasons about giveback directly — and does it better, because it weighs
giveback *against* regime, book and thesis instead of a fixed threshold. **The one thing it still
does that the advisor does not: it writes the 48-field hourly snapshot the advisor's prompt reads
from.** Retire the *verdict* (`would_exit`, `ref_arm_pct`, `ref_gb_pct`); keep the *sampler*.

**ob-density baseline — no longer a sensor, now a dependency.** 19,559 snapshots, wired into the
exit prompt as percentiles (`ef7fa10`). It never had a firing threshold. Reclassify from "sensor" to
"data source"; it must keep running or the percentile scale goes blind.

**prior-move logger — the hypothesis is dead, the cost is not.** Continuous features fully overlap
at n=49; the bucket collapsed under decomposition (mid n=8→1 after decontamination, SHORT has
**zero** mid/late observations). Each run rebuilds a **35,987-point price oracle** from a 54 MB DB,
four times a day, for a question already answered no. **Retire, or drop to weekly.**

---

## 3. Unread data — collected, never queried

| what | volume | what it would answer |
|---|---|---|
| **post_exit_observatory + drift samples** | **36 rows + 175 samples, 175/175 populated** | the shadow "what if we had not exited" comparison — built 06-03, **never analysed once** |
| `mc_oi`, `mc_funding_rate` | **17,820 / 17,822 rows** | open-interest and funding at every signal. Never queried in any study |
| `weight_used`, `context_weight_score` | 2,777 each | the learning-loop weights actually applied. Never audited |
| `liquidity_swept_before_entry` | 2,777 | whether a sweep preceded the entry — the 5m LIQUIDITY tier's whole thesis |
| `macro_gate_penalty`, `news_score`, `dxy_trend` | 3,531 / 2,341 / 2,696 | what the macro gate has actually cost or saved. Never cut |
| `orderbook_json`, `tape_json` | 61 each | **full book + tape snapshots at every entry**, unparsed |
| `learning_*` (4 cols) | 55–56 | the learning loop's own reasoning, never read back |
| `mfe_tracking` | **0 rows** | dead table, feature disabled |
| `breakeven_jobs`, `liquidity_sweep_state` | **0 rows** | dead tables |

**The biggest single omission is the post-exit observatory.** It has been running since 2026-06-03,
its drift samples are 100% populated, and no report has ever opened it — including mine. It is the
only thing that measures what happened *after* we exited, which is exactly the question the exit
advisor is now being built to answer.

---

## 4. Duplication

* **Three sensors point at the FLAT label**: the FLAT score floor (shipped), chop-short gap=Flat,
  regime-FLAT high-ADX. They cut it differently — floor by score, chop-short by outcome, high-ADX by
  mislabelling — but acting on all three would penalise one tape condition three times.
* **Three things now measure giveback**: smart-exit dryrun (`giveback_pct`), the exit advisor
  (reasons about it explicitly), the LONG partial (banks at +1R to avoid it). Only the partial acts.
* **Two things measure the entry book**: volfloor (`entry_*` columns) and ob-density (percentiles).
  Same book, different reference frame — complementary, not duplicate, **provided the volfloor
  threshold is ever expressed as a percentile rather than a raw multiple.**

---

## 5. Cost — and one thing that is not about cost

### 🔴 A live API key is sitting in a world-readable log
```
/var/log/titan_counter_short_filter_review.log   -rw-r--r--  root root
3 lines containing a full ANTHROPIC_API_KEY in plaintext
```
Cause: the review script does `set -a; . "$ENV_FILE"`, and a `.env` line whose value is unquoted is
executed by the shell, which echoes the failure — key and all — into the log. The file is
**world-readable**. The key value is deliberately not reproduced here.

This is not a sensor finding and it does not wait for a watch-list decision. Reported as-is; no fix
applied, per the read-only scope.

### Cadence cost
* `prior_move_logger` — 4×/day, rebuilds a 35,987-point oracle each run, for a dead hypothesis.
* `counter_short_filter_review` — weekly cron for a filter **retired today** (`b878535`). It now
  measures something that does not exist, and it is the script leaking the key.
* Everything else is trivial: sensor logs are 4–8 KB each, `prior_move_samples.jsonl` is 28 KB.
  The exit advisor adds ~24 Haiku calls/day — the only new recurring API cost, and it is the one
  thing on this list with an activation criterion attached.

---

## The prioritised list

**RETIRE (4)**
1. `titan_counter_short_filter_review.sh` — its filter was retired today; it also leaks the key.
2. `titan_toln_short_cohort_watch.sh` — the HTF cascade makes its cohort unreachable.
3. smart-exit dryrun **verdict fields** — superseded by the exit advisor. Keep the sampler.
4. `titan_prior_move_logger.py` — dead hypothesis, real recurring cost.

**REDEFINE (2)**
5. `chop_short_flat_gap` → `gap1h='Flat'` under `regime='TREND'`; covers 4 of 6 original losers
   (-271.97), and the FLAT gate does not blind it. Current N=2.
6. `regime_flat_high_adx` → widen the 3-day window to ~21 days, or drop the threshold to ~3.
   At the observed rate 12-in-3-days is arithmetically impossible.

**FOLD INTO THE ADVISOR (2)**
7. ob-density → already folded (`ef7fa10`); reclassify as a data source, not a sensor.
8. smart-exit sampler → already the advisor's data source; relabel it as such.

**GENUINELY STILL NEEDS n (3)**
9. **volfloor SHORT** — 7 of 6, fired, but only 2 winners and 9 of 18 rows sit in the wall-trail
   window. Needs **2–3 more clean SHORT winners**; at ~1 short close per 4 days, **4–8 weeks**.
10. **LONG partial parameters** — 6 clean longs above 0.5R, need ~30. **Months.**
11. **Exit advisor** — needs its first ~10 closed positions against the criterion already recorded
    in `OPEN-ITEMS.md §6`. At the current close rate, **5–7 weeks**.

**READ WHAT WE ALREADY HAVE (1, and it is free)**
12. The **post-exit observatory** — 36 positions, 175 fully-populated drift samples, sitting unread
    since June. No new data needed. It is the highest-value item on this list precisely because it
    costs nothing to answer.

---

Nothing changed. Tree clean at `ef7fa10`, `titan.service` healthy, Mercury-SOL untouched.
