# commit-d12e276-sensor-cleanup

_2026-07-26 23:35 UTC_

---

# TITAN — commit d12e276: sensor retirement and redefinition, committed

**2026-07-26 23:45 UTC.** Housekeeping commit for the cleanup applied earlier in the session.
It landed after the sweep report was published, so this is its own record. Tree clean.

## What the commit contains

**Retired** → `titan-bot/retired_sensors/`, removed from crontab:

| sensor | why |
|---|---|
| `titan_counter_short_filter_review.sh` | the filter it reviews was retired in `b878535`, and this script was the source of the `ANTHROPIC_API_KEY` leak into a world-readable log |
| `titan_toln_short_cohort_watch.sh` | the HTF cascade makes a 1h-neutral short essentially unreachable — 25 of 28 closed shorts had `trend_1h=bear`, 2 neutral, 1 bull |
| `titan_prior_move_logger.py` | hypothesis dead (continuous features overlap fully; the bucket collapsed under decomposition), and it rebuilt a 36k-point price oracle four times a day |

**Redefined:**

* `titan_chop_short_flat_gap_watch.sh` → `gap1h='Flat' AND regime='TREND'`. The FLAT score floor
  (`db714540`) drove `regime='FLAT'` entries to zero, so that half of the cohort could never grow
  again. The new predicate covers 4 of the 6 original losers (vpos 33, 40, 53, 60 = **-271.97**);
  the 2 it drops are exactly the ones the gate now blocks at entry.
* `titan_regime_flat_high_adx_watch.sh` → window **3d → 21d**. It was never starved by the FLAT gate
  (it counts *skips*, and FLAT `ai_skipped` rose to 123 after the gate). At ~20 members/month a
  3-day window against a threshold of 12 has an expectation of ~2 and was arithmetically incapable
  of firing. It now reads **N=5/12** instead of a permanent 0.

## Scope

No bot code, no config constant, no gate, no in-bot sensor, no Mercury-SOL logic. The ob-density
collector and the smart-exit sampler are untouched and still running — the exit advisor reads from
both.

## Session commits

```
93c20c3  recheck TIGHTEN bounded at the original stop distance
b878535  counter-trend EMA-1h soft caution retired
f7df202  LONG partial realisation, 1/3 @ +1R (fired live on vpos 82, +18.91 banked)
ef7fa10  15m entry confirmation persisted + exit advisor wired in DRYRUN
d12e276  this commit — sensor retirement and redefinition
```
Plus, outside git: the secret purge, log permissions, `.env` quoting, the safe env parser on both
bots, and the nginx `noquery` log format.

## Still waiting on you

1. **Rotate the Anthropic API key** — world-readable for 20 days (`OPEN-ITEMS §8`).
2. Webhook passphrase — redacted in logs and no longer written by nginx; rotation declined.
3. Exit advisor activation criterion — recorded before any data existed (`OPEN-ITEMS §6`).
4. Volume ceiling — not built, expires 2026-09-30 (`OPEN-ITEMS §11`).
