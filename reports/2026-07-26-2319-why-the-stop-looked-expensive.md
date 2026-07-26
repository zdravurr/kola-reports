# why-the-stop-looked-expensive

_2026-07-26 23:19 UTC_

---

# TITAN — why the stop looked expensive, and the nginx query-string fix

**2026-07-26 23:20 UTC · nginx fix APPLIED · stop investigation READ-ONLY.**

**Headline: the stop is not the problem. Three quarters of the "expensive" stop-outs never reached
their stop at all — they died on a stop the wall-trail or the recheck had moved, and both of those
were removed today.** Of what remains, the geometry is uniform and the recovery is late. Detail below.

---

# The nginx fix

`log_format noquery` now logs `$request_method $uri $server_protocol` instead of `$request`, so the
query string — which is where both bots carry their credential — never reaches disk.

```
before:  "POST /webhook?key=<PASSPHRASE>&tf=5m HTTP/1.1" 200 328
after:   "POST /webhook HTTP/1.1" 200 268
         "POST /webhook/sol HTTP/1.1" 200 363
```

**(a) nginx healthy** — `nginx -t` passed, reloaded, `active`.
**(b) per-bot counts survive** — `/webhook` and `/webhook/sol` are distinct `$uri` values and still
group cleanly.
**(c) SOL unaffected** — `mercury-sol.service` active, last DB row 23:10, its requests logging
normally.
**(d) no passphrase in new lines** — 0 of the post-reload lines contain a query string.

Config backed up to `/root/.secleak_backup_20260726/nginx.conf.bak`. Passphrase **not** rotated, per
your decision.

**One cost, stated plainly:** `?tf=` is gone too, so nginx can no longer break requests down by
timeframe. That breakdown is still available from the app's own `WEBHOOK_IN` lines, which carry
`tf=` and `action=` — the ingress analysis earlier today used exactly that source.

---

# The stop investigation

## 1. Penetration depth — the decisive test, and it kills the premise

For each of the 20 SL deaths, how far past the **original** stop did price actually go?

```
median penetration:  -0.49R      LONG -0.66R (n=12)   SHORT -0.48R (n=8)
```
**Negative means price never reached the original stop.** Only **5 of 20** got there:

| group | n | wall-trail / recheck exposure |
|---|---|---|
| reached the ORIGINAL stop | **5** (vpos 59, 61, 77, 78, 80) | **0 / 5** |
| died on a MOVED stop | **15** (47, 53, 55, 62, 63, 65–74) | **15 / 15** |

The correlation is total. Every position that died short of its own stop was inside the wall-trail
window or carried a recheck TIGHTEN. **The +0.75R "left on the table" by stop-outs is three-quarters
a re-measurement of the self-clipping already removed today** (`5f1b073`, `c845941`, `93c20c3`).

This is the fourth independent route to that same damage — after the era split, the SL-death
decomposition, and the excursion truncation.

## 2 & 3. When the recovery happens — late, in both groups

| horizon | genuine stop (n=5) | moved stop (n=15) |
|---|---|---|
| 15m | +0.02R | +0.03R |
| 1h | +0.23R | +0.06R |
| 4h | +0.27R | +0.30R |
| 12h | +0.40R | +0.44R |
| **24h** | **+0.67R** | **+0.83R** |

**Almost nothing happens in the first hour.** The gap opens between 4h and 24h — and the book's
median hold is **5.2h for longs and 8.4h for shorts**. A recovery that arrives at hour 12–24 is
beyond the horizon this bot trades on. **H3 is supported directly.**

## 4. By side — the recovery is a LONG phenomenon

```
moved-stop group, 24h:    LONG  +0.98R (n=10)      SHORT  -0.46R (n=5)
genuine-stop group, 24h:  LONG  +0.34R (n=2)       SHORT  +0.67R (n=3)
```
In the group that matters most (moved stops), longs recover strongly and **shorts do not recover at
all — they keep going against**. n=2 and n=3 in the genuine group are too thin to read.

## 5. Stop geometry — uniform, and that kills H1

```
SL deaths          n=20   median 2.50 x ATR-1h   range 2.44 - 2.67
reached the trail  n=14   median 2.51 x ATR-1h   range 0.43 - 2.56
whole book         n=49   median 2.51 x ATR-1h   range 0.43 - 2.83
```
**Not one stopped-out trade carried a tighter-than-usual stop.** The range on SL deaths is *narrower*
than the book's. The stop distance is 2.5×ATR by construction and it was 2.5×ATR on every one of
them. **H1 — "the stop is too tight" — is dead on the geometry alone**, before any drift argument.

## 6. Entry quality — the one place H2 has something

| field | SL deaths (n=20) | reached trail (n=14) |
|---|---|---|
| confluence_score | 3.75 | 4.00 |
| MTF alignment | 4.00 | 4.00 |
| **ADX-1h** | **28.92** | **22.80** |
| **vol_ratio_5m** | **2.54** | **0.95** |

Score and MTF are effectively identical — these were **not worse setups by the machinery's own
measures**. But the stopped-out trades entered on **2.7× the 5m volume** and into a noticeably
higher ADX. That is the same signal the volume-floor work found independently on the short side
(winners 1.38–1.54, losers 2.42–5.70). **Partial support for H2, but not as "bad setups" — as a
different tape: entering into a volume spike.** n=20 vs 14, and this is one comparison among many,
so it is a pointer, not a finding.

## 7. What the exit advisor would have said — n is too small to run

Full enrichment needs the entry-book snapshot (from 07-04) **and** the ob-density baseline (from
07-13). SL deaths meeting both: **4** — vpos 74, 77, 78, 80. Three of those four are in the
moved-stop group or are shorts that kept falling.

**I did not run the retroactive queries.** Four reconstructable cases, of which the interesting
subset is one or two, cannot separate the hypotheses — and the live advisor is already recording
verdicts hourly on exactly this question. Running four rushed retro-queries would add noise, not
evidence. Stated as a skipped step rather than dressed up.

---

## 8. Verdict

**H1 — stop too tight: REJECTED.** Every SL death carried the standard 2.5×ATR stop; the range is
narrower than the book's. And 15 of 20 never even reached that stop.

**H3 — horizon artefact: SUPPORTED, and it is the main answer.** The recovery is ~+0.03R at 15
minutes and only reaches +0.67–0.83R by 24 hours, against a median hold of 5–8 hours. What the
observatory measured is largely mean-reversion the bot would never have been in the trade to
capture.

**H2 — early entries: PARTIAL, one side only.** Not by score or alignment, which are identical, but
by tape: stopped-out entries came on 2.7× the 5m volume. And the side split says it is a long-side
question — longs recover +0.98R at 24h, shorts −0.46R.

**Per side:**
* **SHORT — the stop is fine.** Shorts that were stopped kept going against us. There is nothing
  to recover and no case to answer.
* **LONG — the stop is fine too, but the tape around the entry is not.** The +0.98R recovery is
  real, and it arrives 12–24h after an exit on a position whose median hold is 5.2h.

**Plainly, as you asked for it: the stop is fine, and the 24h recovery is largely irrelevant to a
swing bot holding 5–8 hours.** The finding that looked like "the stop is expensive" was mostly the
two stop-moving mechanisms that were removed today, measured a fourth time from a new angle.

**No proposal follows.** Nothing here argues for widening the stop or letting anything override it —
the two mechanisms that did exactly that this year cost real money and are gone.

---

Applied: nginx `log_format` only. No bot code, config, gate or sensor touched. `nginx`,
`titan.service` and `mercury-sol.service` all healthy.
