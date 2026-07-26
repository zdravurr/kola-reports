# security-purge-sensor-cleanup-postexit

_2026-07-26 22:52 UTC_

---

# TITAN — security purge · sensor cleanup · the post-exit observatory finally read

**2026-07-26 23:00 UTC · Parts 1-2 APPLIED · Part 3 read-only.**

---

# PART 1 — SECURITY

## What was exposed, and since when

**One secret: the `ANTHROPIC_API_KEY`** (`sk-ant-api03-…`, shared by both bots per
`project_shared_anthropic_key`). Values are not reproduced anywhere in this report.

| file | lines | perms | dates |
|---|---|---|---|
| `/var/log/titan_counter_short_filter_review.log` | 3 | **644 world-readable** | 07-08, 07-15, 07-22 |
| `/var/log/mercury_sol_30trade_reminder.log` | 2 | **644 world-readable** | **07-06**, 07-20 |

**Exposure window: 2026-07-06 → 2026-07-26, twenty days, five occurrences, world-readable the whole
time. Rotate the key.** Both bots share it, so rotation touches both.

**Separately — two Telegram bot tokens** (`8468351860:AA…`, `8936585316:AA…`) in
`/var/log/syslog.2.gz` and `syslog.4.gz`, 13 lines. Different cause: the mercury-sol optimizer
listener prints a `requests` exception whose message embeds the full API URL including the token.
Those files are `640 syslog:adm` — not world-readable, so lower severity, but still logged.

**Not a leak:** `/home/botuser/.openclaw/workspace/.kola_state/secrets/dirigent_bot.json` — a
secrets file by design, correctly `600 botuser:botuser`.

## Root cause

`.env` line 6 was `ANTHROPIC_API_KEY= sk-ant-…` — **a leading space, no quotes.** Under
`set -a; . "$ENV_FILE"` bash reads `VAR=` as an empty assignment prefix and the remainder as a
**command**, then reports `command not found` — echoing the key to stderr, i.e. into the cron log.
python-dotenv strips whitespace, so the bots always worked and nothing looked broken.

Two scripts used that pattern, one per bot:
`/root/titan_counter_short_filter_review.sh` and `/root/mercury_sol_30trade_reminder.sh`.

## What was done

1. **Backup** of the affected logs, `.env` and crontab to `/root/.secleak_backup_20260726` (700).
2. **Purged** — `sk-ant-api` lines deleted: titan 3→0, sol 2→0. syslog archives rewritten with the
   tokens redacted: 13→0.
3. **Permissions** — every sensor log on both bots is now **600 root:root** (11 files). `.env` → 600.
4. **`.env` repaired** — every unquoted value is now quoted and whitespace-stripped (6 lines,
   including the two other unquoted ones: `WEBHOOK_PASSPHRASE`, `GEMINI_API_KEY`).
   **Verified value-safe:** SHA-256 of all 12 keys compared before/after — **0 differences.**
5. **Root cause fixed on both bots** — `set -a; . <env>` replaced with a `_env_get()` sed parser
   that reads only the variables it needs, strips quotes/whitespace, and **executes nothing**.
   Live-tested: both scripts run clean, **no secret in their output**, logs stay clean.

*(Noted, not fixed: `mercury_sol_30trade_reminder.sh` logs `db-read-failed (got 'ERR')` — present
since 2026-07-13, pre-dating this change. SOL is out of scope.)*

---

# PART 2 — SENSOR CLEANUP (applied)

**Retired** (removed from crontab, scripts moved to `/root/titan-bot/retired_sensors/`):
`titan_counter_short_filter_review.sh` (its filter was retired today in `b878535`, and it was the
leak source) · `titan_toln_short_cohort_watch.sh` (cascade makes the cohort unreachable) ·
`titan_prior_move_logger.py` (dead hypothesis; rebuilt a 36k-point oracle 4×/day).

**Redefined:**
* `chop_short_flat_gap` → `gap1h='Flat' AND regime='TREND'`. The `regime='FLAT'` half can never
  grow again (0 FLAT entries since the gate). The new predicate covers 4 of the 6 original losers
  (vpos 33, 40, 53, 60 = **-271.97**); the 2 it drops are exactly the ones the FLAT gate now blocks.
  Live: `N=0 < 5` — correct, the marker counts only NEW closes.
* `regime_flat_high_adx` → window **3d → 21d**. It was never starved by the FLAT gate (it counts
  *skips*, and FLAT `ai_skipped` rose to 123 after the gate); 12-in-3-days at ~20/month has an
  expectation of ~2 and was arithmetically impossible. Live: **N=5 < 12** — it now measures something.

**Reclassified as data sources, still running:** ob-density collector (19.5k snapshots — feeds the
exit-advisor percentile scale) and the smart-exit sampler (48 fields — the advisor's prompt reads
from it). **Only the dryrun *verdict* fields are deprecated; the sampler code was deliberately not
touched**, because the exit advisor depends on it and a code edit there is risk without benefit.

**Nothing the exit advisor or any shipped fix depends on was removed.** Verified: 4 Titan cron lines
remain (bull-regime, flat-high-adx, chop-short, volfloor); the ob-density collector and smart-exit
sampler are in-bot and untouched; `LONG_PARTIAL_*`, the recheck bound and the FLAT floor are
unchanged.

---

# PART 3 — THE POST-EXIT OBSERVATORY, READ AT LAST

36 positions, 175 drift samples, running since 2026-06-03. **Never opened until now.**

## Where price went after we exited, in R
*(positive = price kept going our way = we exited early)*

| horizon | n | median | mean | share > 0 |
|---|---|---|---|---|
| 15m | 35 | +0.03R | +0.01R | 60% |
| 1h | 35 | +0.06R | +0.10R | 60% |
| 4h | 35 | +0.03R | +0.17R | 54% |
| 12h | 35 | +0.21R | +0.19R | 69% |
| **24h** | 35 | **+0.38R** | +0.20R | **66%** |

**On average we exit early, and the gap widens with time** — negligible in the first hour, +0.38R
median by 24h. Two thirds of exits were followed by further favourable movement.

## By exit reason (24h)

| exit reason | n | median | mean | share > 0 |
|---|---|---|---|---|
| **sl** | 20 | **+0.75R** | +0.32R | 65% |
| external (signal) | 5 | +0.38R | +0.44R | 100% |
| post_entry_critical | 1 | +0.08R | — | — |
| **trail** | 9 | **-0.01R** | -0.19R | 44% |

**The stop leaves the most on the table by a wide margin.** Median +0.75R of further favourable
movement within 24h of being stopped out — on a book where 1R is the entire risk budget. The trail,
by contrast, is close to optimal: median -0.01R means it exits almost exactly where the move ends.

n=5 for signal exits and n=1 for post-entry-critical — those two rows are indicative only.

## By side (24h)
```
LONG   n=16   median +0.58R   mean +0.48R   75% positive
SHORT  n=19   median +0.07R   mean -0.04R   58% positive
```
**Longs are exited far too early; shorts are about right.** This is the third independent route to
the same conclusion — the LONG-side diagnostic reached it from excursion shape, the exit-contract
study from giveback, and now the observatory from post-exit drift.

## The shadow exit — what the table was actually built for

Every position carries a shadow exit armed at entry (signal-based). Comparing it against what
really happened, in R:

| real exit reason | n | Σ advantage | median | shadow better |
|---|---|---|---|---|
| **sl** | 20 | **+5.72R** | +0.29R | **16/20** |
| post_entry_critical | 1 | +0.03R | — | 1/1 |
| external | 5 | -0.88R | +0.07R | 3/5 |
| **trail** | 9 | **-3.73R** | -0.14R | 4/9 |
| **TOTAL** | **35** | **+1.13R** | | |

```
real book, these 35 positions:  -0.87R
shadow book:                    +0.26R
by side:  LONG +2.76R   ·   SHORT -1.63R
```

**The signal-based shadow exit would have turned a losing book into a marginally positive one — and
the entire gain comes from replacing stop-outs.** It beats the real exit on 16 of 20 SL deaths
(+5.72R) and loses badly on trail exits (-3.73R, driven by vpos 58 at -2.59R and 48/49 at ~-1.07R
each: the trail caught runners a signal exit would have cut short).

**Read carefully — this is not "switch to signal exits".** It is two separate statements:
* on positions that ended at a stop, an earlier signal-based exit was better 80% of the time;
* on positions that ended on the trail, it was clearly worse.
The two cancel to +1.13R over 35 positions, which is not a mandate for anything. What it *is*, is
the first independent confirmation that **the stop is the expensive exit** — which is exactly what
the exit advisor was wired up to interrogate, and it now has a prior to be measured against.

---

## What changed, what did not

Applied: crontab (3 sensors removed), 2 sensor predicates redefined, `.env` quoting, 2 scripts'
env-loading, log permissions and purge. **No bot code, no config constant, no gate, no SL/trail, no
Mercury-SOL logic.** `titan.service` was not restarted — nothing it loads was touched.

**Decision needed from you: rotate the Anthropic key.** Exposed world-readable for 20 days.
