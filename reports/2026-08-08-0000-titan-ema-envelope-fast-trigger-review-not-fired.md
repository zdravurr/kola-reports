# TITAN — EMA ENVELOPE GATE, FAST-TRIGGER REVIEW AT n=111. **THE TRIGGER HAS NOT FIRED.** The gate refuses correctly and stays.

**2026-08-08 00:00 UTC** · Titan 🔴 LIVE (BingX, BTC) · **READ-ONLY — nothing changed, nothing proposed.**
The review pre-registered in `OPEN-ITEMS §2.47/§2.53` on 2026-08-04, executed at the row count that
triggered it. Surfaced by `reports/2026-08-07-2340-both-bots-closing-sweep…` §4b.

---

## §6 — VERDICT AGAINST THE PRE-REGISTERED TRIGGER, PLAINLY

**FAST TRIGGER: NOT FIRED.**

| the trigger, as written | required | **observed** |
|---|---|---|
| n ≥ 100 refusal rows | 100 | **111** ✅ reached |
| mean 4h drift | **≥ +0.25 %** | **−0.2177 %** (naive) · **−0.2359 %** (clustered) |
| 95 % CI excluding zero | required | naive `[−0.2869, −0.1484]` excludes zero **on the wrong side** |

**The sign is opposite.** The observed 4h mean sits **≈0.47 percentage points below** the threshold.
This is not a marginal miss — the gate's refused signals moved **against** the direction they wanted,
which is the definition of a refuser doing its job.

**The gate stays. The next review point is the SLOW TRIGGER at n ≥ 700** (currently 111 — roughly
another 24 days at the measured ~15–25 refusals/day). The 20-entries-per-side review point remains
joined, not replaced.

**Nothing is proposed in this pass, as instructed.**

---

## §1 — FORWARD DRIFT ON ALL 111 REFUSALS

Sign convention per canon §0: **positive = the refused signal would have won.**
Direction is taken from `signal_type` — the side that would actually have been placed.

| horizon | n | mean | median | % positive | naive t | 95 % CI | censored |
|---|---|---|---|---|---|---|---|
| 1 h | 111 | **−0.0854 %** | −0.0566 % | 37.8 % | −4.06 | [−0.1267, −0.0442] | 0 |
| **4 h** | 109 | **−0.2177 %** | −0.1996 % | **29.4 %** | −6.16 | [−0.2869, −0.1484] | 2 |
| 12 h | 107 | **−0.1186 %** | −0.0826 % | 28.0 % | −3.19 | [−0.1915, −0.0457] | 4 |
| 24 h | 92 | +0.0427 % | +0.0230 % | 52.2 % | +0.63 | [−0.0907, +0.1761] | **19** |

**Only 28–38 % of refusals moved the refused signal's way** at 1h/4h/12h. The mild positive at 24h is
a day/clock artifact — it inverts to **−0.0231 %** under the day control (§4 below) — and it is the
most censored row in the table.

🔴 **Right-censoring is real and stated:** the last refusal landed 2026-08-07 22:00:05 and the price
series ends 23:50, so 19 of 111 rows have no 24h forward window and **2026-08-07 drops out of the 24h
clustered statistic entirely** (n_days falls to 3). The 4h horizon — the one the trigger is written
on — is essentially complete at 109/111.

---

## §2 — AGAINST THE THREE COMPARATORS AND THE UNCONDITIONAL BASELINE

Same window (2026-08-04 23:10 → 2026-08-07 22:01), same computation, same direction convention.

### At 4h — the horizon the trigger is written on

| cohort | n | mean 4h drift | t |
|---|---|---|---|
| **EMA envelope** | 109 | **−0.2177 %** | −6.16 |
| `ai_skipped` | 4 | −0.2837 % | −1.68 |
| `below_threshold` | 11 | −0.1456 % | −0.83 |
| **`htf_blocked` ← THE ALARM LINE** | 359 | **+0.0849 %** | +3.76 |
| unconditional baseline (every 5m bar, LONG) | 825 | +0.0654 % | +4.50 |

**Canon's all-time comparators**, for reference: `ai_skipped` −0.059 %, `below_threshold` −0.073 %,
`htf_blocked` **+0.020 %**.

🔴 **The alarm was "the envelope sitting materially ABOVE `htf_blocked`'s +0.020 %."** The envelope
sits **0.24 pp below** the canon figure and **0.30 pp below** `htf_blocked` measured in this same
window. It is also below the unconditional baseline and below zero on every horizon but the censored
24h. **A healthy refuser sits at or below zero — this one does, comfortably.**

Note the same-window `htf_blocked` (+0.0849 %) runs hotter than its all-time figure (+0.020 %). That
is a statement about these four days, not about the cascade, and it makes the envelope's margin
against the alarm line *wider*, not narrower.

⚠️ `ai_skipped` (n=4) and `below_threshold` (n=11) are far too thin in this window to be comparators.
They are shown for completeness; the canon's all-time figures are the ones with standing.

---

## §3 — 🔴 THE UNIT OF INDEPENDENCE IS THE DAY. n_effective ≈ 4.

111 rows land on **four calendar days** — 08-04: 8, 08-05: 25, **08-06: 59**, 08-07: 19. More than
half the rows come from one day. Overlapping forward windows on the same tape are not independent
observations, so the naive t is inflated. Measured here:

| horizon | day-mean | clustered t | clustered 95 % CI (t-dist, df=3) | naive t | **inflation** |
|---|---|---|---|---|---|
| 1 h | −0.1138 % | −1.81 | [−0.3136, +0.0859] | −4.06 | **×2.2** |
| **4 h** | **−0.2359 %** | **−2.26** | **[−0.5688, +0.0969]** | −6.16 | **×2.7** |
| 12 h | −0.2119 % | −1.95 | [−0.5572, +0.1333] | −3.19 | ×1.6 |
| 24 h | +0.1535 % | +0.51 | [−1.1443, +1.4512] | +0.63 | ×1.2 (n_days=3) |

Per-day 4h means: `08-04 −0.037 % (8) · 08-05 −0.236 % (25) · 08-06 −0.146 % (59) · 08-07 −0.525 % (17)`
— **all four days negative.**

**Inflation of ×2.2–2.7**, against the ×3.5 this book has seen before. **n_effective is 4 days, not
111 rows**, and the clustered 4h CI `[−0.5688, +0.0969]` **includes zero**.

**What that means, stated carefully:** at n_eff ≈ 4 this study cannot establish the *size* of the
gate's effect in either direction. But the trigger did not ask for a size — it asked for a **positive
mean with a CI excluding zero**, and the mean is **negative on every day**. A trigger requiring
positive evidence cannot fire on negative evidence, regardless of power. **The verdict is safe even
though the estimate is not precise.**

---

## §4 — DE-CONFOUNDING AGAINST HOUR AND DIRECTION (§2.54 method)

> Stated rather than dressed up: drift here is a **signed price return**, so the SHORT baseline is the
> exact negation of the LONG one. Controlling for `day` and for `day+direction` therefore **coincide**
> — the direction control is absorbed by construction. Printing them as two separate rungs would be
> false precision, so they are shown as one.

| horizon | raw | day (= day+dir) | **day+dir+hour** |
|---|---|---|---|
| 1 h | −0.0854 % (t=−4.06) | −0.0820 % (t=−4.06) | **+0.0067 % (t=+0.54)** |
| 4 h | −0.2177 % (t=−6.16) | −0.2103 % (t=−6.52) | **−0.0143 % (t=−1.31)** |
| 12 h | −0.1186 % (t=−3.19) | −0.0663 % (t=−1.97) | **+0.0003 % (t=+0.02)** |
| 24 h | +0.0427 % (t=+0.63) | −0.0231 % (t=−0.33) | **−0.0159 % (t=−1.19)** |

**The effect collapses to zero under the hour control** — the same shape §2.54 found in the
`htf_blocked` 1H-alone pocket, and the same shape SOL's depth turned out to have. **Drift is a clock.**

🔴 **And this cuts in the gate's favour, not against it.** The collapse says the refusals are neither
selecting winners nor selecting losers once you know the hour — the gate is **hour-neutral**, which is
exactly what a refuser should be. What it emphatically does *not* show is a positive pocket surviving
controls; **no cut in this review is positive after the hour control, and none flips sign into positive
territory.** Two pockets have died in §2.54 and one flipped sign; nothing here repeats that.

The 06–11 UTC cell is the strongest raw cell (−0.5578 %, t=−7.23, n=24) and is precisely the hour
effect the control removes. It is not a finding.

---

## §5 — WHICH LEG REFUSED

| leg | n | 4h mean | naive t | clustered 4h | 12h mean |
|---|---|---|---|---|---|
| **BOTH legs** non-Expanding | 46 | −0.2323 % | −5.01 | −0.1176 % (t=−1.45, 4 days) | −0.1791 % |
| **1h leg only** | 41 | −0.2523 % | −3.97 | −0.2628 % (t=−1.65, 4 days) | −0.1707 % |
| **15m leg only** | 24 | −0.1316 % | −1.60 | −0.3802 % (t=−1.44, 3 days) | +0.0764 % |

Composition: `1h Contracting/15m Expanding` 39 · `both Contracting` 32 · `1h Expanding/15m
Contracting` 18 · `1h Flat/15m Contracting` 10 · `1h Expanding/15m Flat` 6 · `1h Contracting/15m Flat`
3 · `1h Flat/15m Expanding` 2 · `both Flat` 1.

**No single leg carries the refusals and no leg carries a positive signal.** The load is spread
41 / 24 / 46 across 1h-only, 15m-only and both, and **all three are negative at 4h**. Every clustered
t is |t| < 1.7 — none individually significant at n_days ≈ 3–4, which is expected and is why the split
is reported as a *mechanism check*, not as three findings. The one mildly positive cell anywhere is
`15m leg only @ 12h` (+0.0764 %, t=+0.77, n=24) — well inside noise.

**Conclusion for §5:** the measured cohort is the mechanism the trigger was written about. There is no
single-leg artifact masquerading as a gate effect.

### By direction and session (4h)

| cut | n | mean | t |
|---|---|---|---|
| LONG | 48 | −0.1586 % | −3.34 |
| SHORT | 61 | −0.2642 % | −5.24 |
| 00–05 | 28 | −0.2114 % | −3.61 |
| 06–11 | 24 | −0.5578 % | −7.23 |
| 12–17 | 26 | −0.0501 % | −0.61 |
| 18–23 | 31 | −0.1005 % | −4.23 |

**Both directions negative. No sign flip anywhere.**

---

## §7 — vpos 93, RECORDED FOR WHAT IT IS: n = 1

The **one** entry this gate admitted that became a live position.

```
04:50:03  [EMA-ENV] PASS SHORT BTC/USDT:USDT 1h=Expanding 15m=Expanding
04:50:13  LIVE ENTRY SHORT 0.0023 @ 64192.9    ·  LIVE STOP @ 64662.1
04:50:22  [EXIT-ADVISOR-ACT] conf=0.72 — "Entry thesis compromised… 5m structure
          has inverted sharply" → CLOSING at market
04:50:23  CLOSE @ 64193.0 · net −$0.1479 · reason=ai_exit
```

**Closed by the exit advisor 9 seconds after entry, for fees.** Gross **−$0.00023**; fees **$0.1476**;
net **−$0.1479 ≈ −0.137R**.

🔴 **n = 1. It is evidence for nothing — not for the gate and not against it.** It is recorded here so
that a later session cannot pick it up as either. The admitted-entry question is the 20-per-side
review point's job, and that review is nowhere near its threshold.

---

## Method, and its stated limits

- Price series: 911 BingX 5m closes, 2026-08-04 20:00 → 2026-08-07 23:50 UTC, paginated; anchor is the
  close of the last 5m bar at or before the refusal instant.
- 111 of 111 refusals carry a directional claim. **Correction to a first pass of my own:** I initially
  keyed direction off `matrix_direction`, which disagrees with `signal_type` on **5 of 111** rows (2
  `open_short` scored matrix LONG, 3 scored NEUTRAL). The refused *signal* is the entry that would have
  been placed, so `signal_type` is the right anchor and every number above uses it. The same correction
  moved same-window `htf_blocked` at 4h from −0.1464 % to **+0.0849 %** — a large enough shift that
  using the wrong field would have misstated the comparator, though not the verdict.
- ⚠️ **What drift cannot answer, restated with the result rather than after it** (§2.47's own caveat):
  this measures whether **price moved the refused signal's way**, not whether the **trade** would have
  won. No stop, no trail, no fees, no partial. A negative drift is evidence the gate is refusing
  *moves* that went the wrong way; it is not proof it refused *losers*. It is the cheap early check.
  The 20-per-side review remains the expensive honest one.

**Read-only throughout:** the DB was opened `?mode=ro`, the exchange call was `fetch_ohlcv` (public,
keyless), no Titan file was read for state beyond `trades.db`, nothing was written, nothing restarted.
Titan remains clean at HEAD `897850b`, `NRestarts=0`.
