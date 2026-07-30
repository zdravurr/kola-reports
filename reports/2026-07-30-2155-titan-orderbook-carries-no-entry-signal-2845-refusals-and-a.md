# titan-orderbook-carries-no-entry-signal-2845-refusals-and-a-veto-that-inverted

_2026-07-30 21:55 UTC_

---

# TITAN — DOES THE ORDER BOOK CARRY ENTRY INFORMATION? MEASURED THROUGH 2,845 REFUSALS.

**2026-07-30 22:10 UTC · READ-ONLY · HEAD `dee6cee`, LIVE, vpos 87 LONG open · nothing changed, nothing proposed**

---

## VERDICT FIRST

**No book measure passes all three tests. The question closes negative.**

| test | result |
|---|---|
| (a) carries information | ⚠️ **marginal — indistinguishable from chance.** 2 of 25 tests survive temporal clustering; ~1.3 false positives are *expected* at 5%. Neither survivor has a coherent term structure. |
| (b) locatable threshold | ❌ **no.** The percentile ladder is non-monotone and wanders in sign. Only the **bottom decile** of depth shows anything, and only at 12h/24h. |
| (c) not volatility or the clock in a costume | ❌ **fails.** **76% of the thin decile falls in the 18:00–24:00 UTC block**, where it is 27.6% of skips against 1.1–3.8% everywhere else. |

🔴 **To say it in the words you asked for: for total depth, the book is largely a proxy for the clock.** Not entirely — the effect does not vanish inside the evening block — but "thin book" and "late UTC" are so nearly the same event in this data that the depth measure cannot be given an independent entry vote.

**And the one thing that does survive lives at the wrong horizon.** The bottom-decile depth effect appears only at **12h and 24h**. Median holding time across 54 closed positions is **6.6 hours**; 67% close inside 12h. A signal that only resolves after the trade is typically over is not an entry filter.

🔴 **A finding you did not ask for, which bears directly on the premise.** The wall veto that motivated this method **has inverted out of sample.** In its original era it is negative as claimed; in the 17 days covered by the book data it has flipped sign. Details in §7b — this is the most consequential number in the report.

---

## 0. STATE AND METHOD

`git status` clean · HEAD **`dee6cee`** · `titan.service` **active** · vpos 87 **open**, stop order `2082799690256592896`. Read-only session: no file was written to `/root/titan-bot`, nothing restarted.

**Provenance guard (§2.19) honoured:** every book query filters `source = 'okx_books_full_4000'` **explicitly and in the `WHERE`**. That is the only source present (25,179 rows), but the filter is written anyway so a second source can never be silently mixed in.

**Sign convention (§0):** drift is **positive = the skipped signal would have won** (refusing was wrong); **negative = refusing was right**.

**De-confounding.** Every drift figure is **adjusted**: the unconditional forward drift over the same span is subtracted, signed to the direction (a LONG skip drifts positive for free, a SHORT negative). Computed from 5,445 real 5m BingX candles:

| horizon | unconditional drift (baseline for a LONG) | rolling windows |
|---|---:|---:|
| 15m | +0.0013% | 5,123 |
| 1h | +0.0064% | 5,114 |
| 4h | +0.0304% | 5,078 |
| 12h | +0.0926% | 4,982 |
| 24h | **+0.1860%** | 4,838 |

---

## 1. THE JOIN

**Book series:** 25,179 rows, `2026-07-13T02:34:56` → `2026-07-30T21:43:04`. Cadence **61 s median**, p95 61 s, **largest gap 7.9 min**, zero gaps over 10 min.

**Bound:** nearest snapshot within **±180 s**.

| | |
|---|---|
| skip rows in window | 2,943 |
| **matched** | **2,943 / 2,943 — 100%** |
| unmatched | 0 |

**Age of the attached snapshot** — staleness is not a problem here:

| | min | p25 | median | p75 | p95 | max |
|---|---:|---:|---:|---:|---:|---:|
| age (s) | 0 | 8 | **16** | 23 | 29 | **101** |

**98.6% are within 30 s; 100% within 61 s.**

### n per status, honestly

| status | matched | completed drift | **has 24h drift** | LONG | SHORT |
|---|---:|---:|---:|---:|---:|
| `htf_blocked` | 2,179 | 2,090 | **2,090** | 1,098 | 1,081 |
| `ai_skipped` | 408 | 406 | **406** | 186 | 222 |
| `below_threshold` | 356 | 349 | **349** | 164 | 192 |
| **TOTAL** | **2,943** | **2,845** | **2,845** | | |

**Analysis sample = 2,845.**

🔴 **Two limits on scope, stated rather than glossed.**

1. **`skip_attribution` tracks only three statuses.** `risk_halt`, `virt_cap_blocked`, `executed`, `failed` and `claude_unavailable` have **no drift rows at all** — the machinery never anchored them. So "all statuses that reached the score gate" is not available; what is available is `below_threshold` + `ai_skipped` (755 rows) plus `htf_blocked` (2,090).
2. **The sample is 73% `htf_blocked`.** Any pooled result is dominated by cascade refusals, not score refusals.

**Coverage against the `trades` table** — `skip_attribution` is near-complete, not sampled:

| status | trades | skip_attribution | coverage |
|---|---:|---:|---:|
| `htf_blocked` | 2,199 | 2,179 | 99.1% |
| `ai_skipped` | 411 | 408 | 99.3% |
| `below_threshold` | 375 | 356 | 94.9% |

---

## 2. IS DISAGREEMENT INFORMATIVE?

### a) What the naive comparison says — and why it cannot be believed

Splitting each measure and comparing de-confounded drift produces several |t| > 2 results: opposing wall mult negative at 1h/4h/12h (t = −2.31, −2.76, −2.04), supporting wall mult positive at 4h/12h/24h (t = +2.67, +2.70, +3.40), depth at 1h (t = −2.57).

🔴 **Those t-statistics are wrong, and the reason is the whole point of this report.**

```
median gap between consecutive skips : 299 s
share of consecutive skips <5 min apart : 57%
distinct days spanned : 17   (2026-07-13 .. 2026-07-29)
```

**A 24h forward window is shared by essentially every skip on the same day.** The 2,845 observations are not 2,845 independent draws — for the long horizons there are **17 independent blocks, not 2,845.** Treating them as independent inflates every t-statistic by roughly √(observations per day) ≈ **√167 ≈ 13×**.

**This is the same error, in a new costume, as the n=11 closed-trade split.** Eleven trades sliced two ways was arithmetic on noise; 2,845 overlapping windows sliced two ways is arithmetic on the *same* noise, wearing a bigger n.

### b) The honest test — day-block bootstrap

Resample the 17 days with replacement, 4,000 draws. A 95% CI excluding zero means the effect survives temporal clustering.

| measure (split) | horizon | observed diff | 95% CI | excl. 0 | p |
|---|---:|---:|---|:---:|---:|
| **imbalance**, signed to direction (0) | 15m | +0.0119% | [−0.0025, +0.0268] | no | 0.106 |
| | 1h | +0.0181% | [−0.0447, +0.0812] | no | 0.550 |
| | 4h | −0.0094% | [−0.1654, +0.1403] | no | 0.917 |
| | 12h | −0.1147% | [−0.5513, +0.2812] | no | 0.635 |
| | 24h | −0.1383% | [−0.6908, +0.4006] | no | 0.630 |
| **support − opposing wall** (0) | 15m | +0.0078% | [−0.0110, +0.0256] | no | 0.415 |
| | 1h | +0.0055% | [−0.0373, +0.0427] | no | 0.778 |
| | 4h | +0.0903% | [−0.0333, +0.2295] | no | 0.166 |
| | 12h | +0.0576% | [−0.2493, +0.3940] | no | 0.711 |
| | 24h | +0.1384% | [−0.2788, +0.5608] | no | 0.518 |
| **supporting wall mult** (5.69) | 4h | +0.0625% | [−0.0419, +0.1759] | no | 0.269 |
| | 24h | +0.1902% | [−0.1918, +0.6074] | no | 0.358 |
| **opposing wall mult** (5.58) | 15m | −0.0075% | [−0.0158, +0.0008] | no | 0.068 |
| | **1h** | **−0.0282%** | **[−0.0549, −0.0015]** | 🔴 **yes** | **0.037** |
| | 4h | −0.0646% | [−0.1746, +0.0259] | no | 0.192 |
| | 12h | −0.0825% | [−0.3002, +0.1153] | no | 0.417 |
| **total_depth_btc** (2,992) | 15m | −0.0096% | [−0.0224, +0.0030] | no | 0.137 |
| | **1h** | **−0.0314%** | **[−0.0639, −0.0043]** | 🔴 **yes** | **0.020** |
| | 4h | +0.0222% | [−0.0586, +0.1078] | no | 0.616 |
| | 24h | +0.1295% | [−0.0655, +0.3287] | no | 0.203 |

**2 survivors out of 25 tests. At 5% significance, 25 tests are expected to produce ~1.3 false positives by chance.** Both survivors sit at **1h only**, both are tiny (−0.03%), and both **fail at every adjacent horizon**. A real effect does not appear at 1h, vanish at 4h, and reverse at 24h.

### c) Which measures show nothing — stated because it is as useful as a positive

- **Imbalance: nothing.** Not one horizon survives, and the raw signs are incoherent (positive at 15m/1h, negative at 12h/24h). Whatever the naive t=−2.83 at 12h was, it was not information.
- **Supporting wall: nothing.** Its best naive result (t=+3.40 at 24h) collapses to p=0.358.
- **Support-minus-opposing wall: nothing.** Its best naive result (t=+3.86 at 4h) collapses to p=0.166.
- **Total depth: not directional in the first place.** Depth has no side, so the WITH/AGAINST framing does not apply to it; it was tested thick-vs-thin instead. **This is worth saying explicitly:** three of the four measures you named are directional and one is not, and the one that produced the only durable-looking result is the one that cannot disagree with a direction at all.

---

## 3. WHERE IS THE THRESHOLD? — it is not monotone, and it is not locatable

Percentile buckets against the full 25,179-row book baseline. De-confounded drift.

**`total_depth_btc`**

| pct bucket | n | 15m | 1h | 4h | 12h | 24h |
|---|---:|---:|---:|---:|---:|---:|
| **0–10** | 249 | +0.0001% | −0.0453% | −0.0992% | **−0.1955%** | **−0.2091%** |
| 10–25 | 411 | +0.0133% | +0.0633% | +0.0602% | −0.0695% | +0.0189% |
| 25–50 | 780 | +0.0063% | +0.0327% | −0.0282% | −0.0024% | +0.0711% |
| 50–75 | 713 | −0.0040% | +0.0037% | +0.0128% | +0.0832% | +0.2285% |
| 75–90 | 400 | −0.0008% | −0.0008% | +0.0377% | −0.0539% | +0.0787% |
| 90–100 | 292 | +0.0062% | −0.0290% | −0.0480% | −0.1235% | −0.0517% |

**`max_wall_mult_ask`**

| pct bucket | n | 15m | 1h | 4h | 12h | 24h |
|---|---:|---:|---:|---:|---:|---:|
| 0–10 | 282 | +0.0033% | +0.0144% | −0.0051% | −0.1062% | +0.0227% |
| 10–25 | 437 | +0.0056% | +0.0311% | +0.0015% | −0.0275% | +0.1372% |
| 25–50 | 800 | +0.0075% | +0.0192% | +0.0060% | +0.0211% | +0.0552% |
| 50–75 | 712 | +0.0080% | +0.0358% | +0.0158% | −0.0021% | −0.0154% |
| 75–90 | 422 | −0.0136% | −0.0542% | −0.0647% | −0.0943% | +0.1227% |
| 90–100 | 192 | −0.0014% | −0.0082% | +0.0017% | −0.0569% | +0.2035% |

🔴 **Neither ladder is monotone.** Depth goes negative in the bottom decile, positive in 10–75, negative again at the top. The ask-wall ladder wanders and its extreme decile is *positive* at 24h — the opposite of a veto.

**The one exception is a tail, not a threshold.** The bottom depth decile is the only bucket with a coherent shape — monotonically more negative as the horizon lengthens — so it was tested directly:

| comparison | horizon | diff | 95% CI (day-block) | excl. 0 | p |
|---|---:|---:|---|:---:|---:|
| depth <10th pct vs rest | 15m | −0.0034% | [−0.0364, +0.0326] | no | 0.891 |
| | 1h | −0.0627% | [−0.1591, +0.0251] | no | 0.188 |
| | 4h | −0.1042% | [−0.3257, +0.0562] | no | 0.291 |
| | **12h** | **−0.1844%** | **[−0.3775, −0.0065]** | 🔴 yes | 0.041 |
| | **24h** | **−0.3025%** | **[−0.5342, −0.0619]** | 🔴 yes | **0.013** |
| depth >90th pct vs rest | all five | — | all include 0 | no | 0.154–0.707 |

**So: not monotone, and it only bites in the thin tail — and only at 12h/24h.** §5 shows what that tail actually is.

---

## 4. 🔴 IS IT TEMPORARY? — NO. WAITING IS NOT A MECHANISM.

Starting from skip moments where the book leaned **against** the proposed direction, how often has it flipped to leaning **with** it, t minutes later?

| +min | imbalance lean (n=1,322) flipped | still against | support−opposing wall (n=1,425) flipped | still against |
|---:|---:|---:|---:|---:|
| 5 | 130 (**9.8%**) | 90.2% | 341 (23.9%) | 76.1% |
| 15 | 179 (13.5%) | 86.5% | 394 (27.6%) | 72.4% |
| 30 | 248 (18.8%) | 81.2% | 406 (28.5%) | 71.5% |
| 60 | 313 (**23.7%**) | **76.3%** | 439 (30.8%) | **69.2%** |

**Thin depth** (below the 25th pct of the full series = 2,765 BTC), n=660 starting thin:

| +min | still below p25 | recovered |
|---:|---:|---:|
| 5 | 552 (83.6%) | 16.4% |
| 15 | 524 (79.4%) | 20.6% |
| 30 | 489 (74.1%) | 25.9% |
| 60 | 449 (**68.1%**) | 31.9% |

**Autocorrelation over the full 25,179-row series** — no skip selection, the clean answer:

| measure | +5m | +15m | +30m | +60m | +120m | +240m |
|---|---:|---:|---:|---:|---:|---:|
| `total_depth_btc` | +0.921 | +0.849 | +0.771 | **+0.673** | +0.552 | +0.383 |
| `imbalance` | +0.903 | +0.809 | +0.700 | **+0.542** | +0.386 | +0.226 |
| `max_wall_mult_bid` | +0.649 | +0.538 | +0.435 | +0.325 | +0.219 | +0.067 |
| `max_wall_mult_ask` | +0.807 | +0.710 | +0.614 | +0.497 | +0.322 | +0.135 |

🔴 **The answer to your question is unambiguous: a thin or opposed book persists for hours, not minutes.** Depth still correlates **+0.67 with itself an hour later** and +0.55 after two hours. An opposed imbalance is still opposed **76% of the time an hour later**.

**Therefore a "wait for the book to turn" trigger is not worth building.** To get even a coin-flip chance of the lean reversing you would wait well over an hour, by which time the 5m trigger that fired the signal is long stale (`EXECUTION` category TTL is **5 minutes**). **If the book were ever to be used, only a veto makes sense — a deferred-entry mechanism is ruled out by this table**, independently of whether the book carries information at all.

---

## 5. CONFOUNDS — CHECKED, NOT ASSUMED

### a) Your stated correlations do not reproduce at the magnitude given

| relationship | you stated | **I measure** (n=2,845 joined skips) |
|---|---:|---:|
| depth × ATR(1h) | −0.67 | **−0.374** |
| depth × ADX(1h) | −0.52 | **+0.055** |

The ATR link is real but roughly half as strong as quoted; **the ADX link is absent — near zero and the wrong sign.** I am not claiming the earlier figures were wrong: they may come from a different population or a different depth field. But on the sample this report uses, ADX is not a confound for depth at all, and I will not carry it forward as one.

### b) The hour-of-day confound is real, and larger than you stated

| | value |
|---|---:|
| median depth, thinnest hour (21 UTC) | 2,411 BTC |
| median depth, thickest hour (09 UTC) | 3,166 BTC |
| **spread across hours** | **755 BTC** |
| full-series IQR | 434 BTC |
| **ratio** | **1.74×** |

Median depth by UTC hour:
```
00:2888 01:2915 02:2941 03:2938 04:3005 05:3036 06:3093 07:3115 08:3097 09:3166 10:3162 11:3085
12:3125 13:3133 14:3048 15:2935 16:2927 17:2909 18:2785 19:2828 20:2813 21:2411 22:2823 23:2812
```

**The hour-of-day spread is 1.74× the entire interquartile range of the distribution** — worse than "equal to" it.

### c) 🔴 The thin decile is very nearly just "evening UTC"

| UTC block | thin-decile skips / all skips in block | share |
|---|---:|---:|
| 00–06 | 28 / 729 | 3.8% |
| 06–12 | 8 / 731 | 1.1% |
| 12–18 | 24 / 700 | 3.4% |
| **18–24** | **189 / 685** | 🔴 **27.6%** |

**76% of the thin decile (189 of 249) sits in one six-hour block.**

### d) Does anything survive the controls?

**The 1h depth effect does survive** — it is not time-of-day and not ATR:

| control | 1h diff (thick − thin) |
|---|---:|
| uncontrolled | −0.0314% |
| mean of four within-6h-block diffs | **−0.0369%** |
| mean of three within-ATR-tercile diffs | **−0.0359%** |

**The 12h/24h thin-decile effect partially survives, but on one block's worth of data:**

| control | 12h | 24h |
|---|---:|---:|
| uncontrolled | −0.1844% | −0.3025% |
| within h00–06 (n 28) | −0.6780% | −0.6673% |
| within h06–12 (n 8) | *too small* | *too small* |
| within h12–18 (n 24) | −0.1290% | **+0.2685%** |
| within h18–24 (n 189) | −0.1306% | −0.3885% |
| within low ATR (n 26) | −0.1553% | **+0.1114%** |
| within mid ATR (n 85) | −0.2257% | −0.4028% |
| within high ATR (n 138) | −0.1151% | −0.2833% |

**Read the n column, not the percentages.** Three of the four hour blocks have 8–28 observations and one of them flips sign. The effect is carried by the single h18–24 block. **The honest statement: within the evening block thin depth still looks bad, but "thin depth" and "evening" are so nearly the same event here that the measure cannot be given an independent vote.**

**In the words you asked for: for total depth, the book is largely a proxy for the clock.**

---

## 6. THE TWO LIVE CASES — context only, n=2, nothing is built on this

| | **vpos 86** (SHORT, 07-30 00:50) | **vpos 87** (LONG, 07-30 12:05) |
|---|---|---|
| book row age | 22 s | 12 s |
| `total_depth_btc` | 2,460 → **6th pct** | 3,373 → **89th pct** |
| in the thin decile? | **YES** | no |
| imbalance | 0.5086 → leaned **AGAINST** (−0.0086) | 0.4182 → leaned **AGAINST** (−0.0818) |
| supporting / opposing wall mult | 5.73 / 4.84 → support > resistance | 4.99 / 8.23 → **resistance ≫ support** |
| hour | 00 UTC | 12 UTC |

**Where they sit against the findings.** vpos 86 is in the one bucket that showed anything (bottom decile) — but at 00 UTC, not in the evening block that carries the effect. vpos 87 sits at the 89th percentile, in the bucket where §3 found nothing, with the strongest opposing-wall reading of the two.

🔴 **The measure you would have to use to reject both is "imbalance leaned against" — and imbalance is the measure that showed nothing at any horizon (§2c).** Two losing trades that a dead measure would have caught is the exact shape of a spurious rule. **n=2. Nothing follows from it.**

---

## 7. HONEST VERDICT

### a) The three tests

**(a) Does a book measure carry information?** — **Marginal, and indistinguishable from chance.** 2 of 25 tests survive day-block bootstrap; ~1.3 are expected by chance. Both survivors are at 1h only, both ≈−0.03%, both fail at adjacent horizons. Imbalance, supporting wall, and support-minus-opposing wall show **nothing at any horizon**.

**(b) Is there a locatable threshold?** — **No.** Both percentile ladders are non-monotone and change sign more than once. The only coherent region is the **bottom decile of depth**, and only at 12h/24h.

**(c) Is it something other than volatility or the clock?** — **No, for the only measure that showed anything.** 76% of the thin decile is one six-hour UTC block. ATR is a genuine but weaker confound (−0.374, not −0.67); ADX is not a confound at all (+0.055).

**Answer: there is no book measure worth building an entry filter on.** That closes the question, which is the outcome you said is worth as much as a positive.

**Two supporting reasons not to revisit it soon:**

1. **The surviving signal is at the wrong horizon.** It appears only at 12h/24h. Median holding time across 54 closed positions is **6.6 h**; **67% close inside 12h, 74% inside 24h**. A signal that resolves after most trades are already closed cannot inform entry.
2. **Waiting is ruled out independently** (§4). Even if the book were informative, an opposed state persists for hours, so only a veto was ever architecturally available — and there is no veto worth having.

### b) 🔴 THE FINDING THAT MATTERS MOST — THE WALL VETO HAS INVERTED OUT OF SAMPLE

You cited the wall veto as the proof that this method works. **I could not reproduce its sign in the book-data window, so I checked the full history — and the result is worse than a failed reproduction: the effect reversed.**

`opposing wall` = the recorded nearest wall lies against the proposed direction (of 2,845 joined skips: 365 opposing, **2** supporting, 2,478 with no recorded wall — the advisor essentially only ever records the blocking wall). Raw 4h drift, no baseline subtraction, to match the original's form:

| era | opposing-wall skips | control | reading |
|---|---:|---:|---|
| **2026-06-07 → 07-13** (before book data) | **−0.0931%** (n=1,451) | +0.0412% (n=3,435) | ✅ negative — **the veto was right**, matching the cited claim's direction |
| **2026-07-13 → 07-30** (this window) | 🔴 **+0.1041%** (n=368) | −0.0228% (n=2,519) | 🔴 **sign flipped — the veto was wrong** |
| full history | −0.0532% (n=1,819) | +0.0141% (n=5,954) | negative, carried entirely by the earlier era |

The literal "ask wall" reading (wall above price, n=178 in window, 176 of them LONG) gives the same story: **+0.1269% at 4h against −0.0129% control**, versus the cited −0.27% vs −0.05%.

And under the day-block bootstrap on this window, opposing-wall skips are **+0.4146% at 12h with a CI of [+0.0753, +0.8232], p=0.013** — significantly *positive*. The veto is not merely absent; in the recent window it points the other way.

**What I am and am not claiming.** I am **not** claiming the original analysis was wrong: its era reproduces with the sign it reported (my magnitude is smaller, −0.09% vs −0.27%, which may be a definition or window difference — I could not see the original query). I **am** claiming that **the effect did not persist**, and that the landmark result underwriting "measure it through refusals" is itself unstable out of sample.

🔴 **The implication for method, not just for walls: if the strongest previous positive result flips sign in the next 17 days, then any book finding from this data — including the two marginal survivors in §2b — should be assumed unstable until it holds across a genuine out-of-sample window.** That is the strongest argument in this report for not building anything on the book.

---

## WHAT I DID NOT DO

- **Nothing was changed and nothing is proposed.** No file in `/root/titan-bot` was written; no restart; HEAD still `dee6cee`; vpos 87 untouched.
- **I did not extend the analysis to `risk_halt`, `virt_cap_blocked` or `executed`** — `skip_attribution` never anchored them, so no drift exists. §1 states this rather than quietly narrowing the population.
- **I did not use closed trades.** No result here rests on the n=11 cohort or on vpos 86/87; §6 is labelled context and nothing is derived from it.
- **I did not re-derive the wall-veto original.** I reproduced it from `skip_attribution` under two readings and reported both; I could not inspect the original query, so §7b states what I can and cannot conclude.
- **I did not correct for multiple comparisons beyond stating the expected false-positive count.** With 25 tests at 5%, ~1.3 survivors are expected; 2 were observed. A formal Bonferroni or FDR adjustment would remove both, and would not change the verdict.
