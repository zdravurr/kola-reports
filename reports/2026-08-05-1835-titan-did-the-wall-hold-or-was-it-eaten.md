# TITAN — DID THE WALL HOLD, OR WAS IT EATEN? **IT WAS EATEN. 95 % OF THE TIME.** AND THAT TURNS OUT NOT TO BE THE INTERESTING PART.

**2026-08-05 18:35 UTC · READ-ONLY · nothing changed, NOTHING PROPOSED, NO DIFF · HEAD `b9081ad`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
`git status` clean before and after · `trades.db` opened read-only (`file:…?mode=ro`) throughout ·
**0 open positions** for the whole pass · **Mercury-SOL never opened.**

---

## 🔴 BONFERRONI HEADER — READ BEFORE ANY NUMBER BELOW

**The budget was set at 54. The 17:25 report took the book to cell ≈192. This pass spends ~146 more,
taking the book to cell ≈338 — more than six times the budget.**

- Bonferroni α at the stated budget = 0.05 / 54 = **0.000926**, i.e. a cell needs **|t| > 3.31**.
- 🔴 **Every hit below is NOMINAL and is labelled as such.** Two cells reached |t| > 3.31 at one
  control specification; **both collapse when the next control is added**, which is §2.54's rule
  operating exactly as designed.
- ⚠️ **The unit of independence is the DAY, not the signal.** 277 refusals sit on **22 days**.
  Every headline below is reported per-signal *and* day-clustered, and **the two disagree
  systematically** — that disagreement is one of the two findings.

---

## ANSWER IN ONE LINE

**§4's first branch fires: NOTHING SURVIVES. Nineteenth closure.** But it closes on two facts that
are worth more than the null:

1. 🔴 **THE WALLS DO NOT HOLD.** Of 277 wall-citing refusals, price traded **through** the cited
   wall's own price level in **54 % within 1 h, 75 % within 4 h, 88 % within 12 h and 95 % within
   24 h.** The barrier the veto is built on is, as a matter of record, **not a barrier**.
2. 🔴 **AND IT DOES NOT MATTER, BECAUSE THE VETO WAS NEVER READING THE WALL.** The dial the advisor
   is told to judge by carries **no information about whether the wall survives, once distance is
   controlled** (perm-p 0.08–0.97 inside distance strata). The marginal appearance that thick walls
   hold is **distance wearing a costume**: r(percentile, distance) = **+0.361**, and mean distance
   rises monotonically across percentile buckets (0.174 → 0.242 → 0.267 → **0.427 %**).
3. 🔴 **THE INVERSION IN THE BRIEF IS EXPLAINED, AND IT IS NOISE.** The veto's own drift is
   **+0.048 % / +0.062 % / +0.174 % / +0.177 %** per-signal (t up to +2.79) — but **day-clustered it
   is +0.042 % / −0.031 % / +0.038 % / +0.014 %, t = +0.91 / −0.34 / +0.24 / +0.06.** With only 22
   days, two windows landing on opposite signs is exactly what zero looks like. **−0.093 % then
   +0.104 % was never an inversion of an effect; it was two draws from nothing.**

**No diff is attached. Nothing is proposed, per the brief's instruction to propose nothing until §4.**

---

## §1 — THE JOIN. **IT WAS POSSIBLE, AND NOT VIA THE REASON TEXT**

🔴 **The brief's stop-condition did not fire, and for a reason worth recording: the wall price is not
something that has to be scraped out of prose — it is a dedicated column.**
`skip_attribution.nearest_wall_price` (`skip_attribution.py:154`, commented *"nearest OPPOSING wall
price"*), alongside `wall_strength` and `wall_distance_pct`. The reason text *does* often carry it
too (*"Ask wall at 63977.50 is 22nd pct (weak)"*), but no parsing was needed.

### THE COHORT, STATED BEFORE ANY RESULT

| step | n |
|---|---|
| `skip_attribution` rows since 2026-07-13 | 4,177 |
| of which `status='ai_skipped'` (the advisor's own refusals) | 492 |
| + wall price present (`nearest_wall_price > 0`) | 453 |
| + the stored reason cites a wall | **328** |
| 🔴 **− duplicate records** (same minute, side, price and wall) | **−51** |
| 🔴 **DEDUPED COHORT** | **277** |
| **distinct DAYS carrying them** | 🔴 **22** |

⚠️ **The 51 duplicates are a 15.5 % inflation and they are not harmless.** Rows 5979/5980 are one
second apart with identical price, wall and distance — the same signal recorded twice. Counting them
would have made every n and every p look 15 % better than the evidence supports. **They are removed
everywhere below.**

### THE STORED WALL REALLY IS THE OPPOSING ONE — CHECKED, NOT ASSUMED

The advisor's HARD RULE (`claude_advisor.py:59-65`) defines opposing as *"directly above a LONG entry
or directly below a SHORT entry"*. The column agrees:

| side | wall ABOVE price | wall BELOW price |
|---|---|---|
| LONG (n=174 raw) | **174** | 0 |
| SHORT (n=154 raw) | 2 | **152** |

The two exceptions are the duplicate pair 5979/5980, at a distance of **0.0018 %** — the wall was
*at* the price. They fall out with the dedupe.

### THE ORDER-BOOK SNAPSHOT JOIN — BOUNDED, WITH ITS AGE DISTRIBUTION

`orderbook_density`: **33,486 snapshots, every one `okx_books_full_4000`**, starting 2026-07-13 —
the window matches the brief's exactly. Nearest snapshot to each refusal, **bounded at 300 s**:

| joined | min | p25 | median | p75 | p95 | max |
|---|---|---|---|---|---|---|
| **275 of 277** | 0.3 s | 7.5 s | **14.2 s** | 22.3 s | 29.2 s | **30.4 s** |

**No snapshot used is older than 31 seconds.** This is the one part of the exercise where the data is
genuinely luxurious, and it is why the question was worth asking: 33,486 book states against a closed
book of 40 trades.

### PRICE SIDE, AND §0's STANDING REPLAY RULE

**BingX 5m, 7,132 bars, 2026-07-12 → 2026-08-05 18:15, zero gaps** — the bot's own indicator source.

| validation | result |
|---|---|
| `price_at_skip` inside its own 5m candle range | **253 / 277** |
| worst deviation among the other 24 | **0.0090 %** |

⚠️ **Stated rather than buried:** the 24 misses are a **cross-venue basis** artefact — the refusal
price comes from the **OKX** book, the candles are **BingX**. A 0.009 % worst-case deviation is two
orders of magnitude below the smallest wall distance being tested and cannot flip an eaten/held call.
It is not a replay failure, but it is not nothing either, and it is why the eaten/held test uses the
**wall's own stored price** rather than a reconstructed one.

---

## §2a — WAS THE CITED WALL EATEN, OR DID IT HOLD?

**EATEN := price traded through the opposing wall's stored price level** (LONG: any high ≥ wall;
SHORT: any low ≤ wall) within the horizon. Path from real 5m OHLCV, never from a stored extremum.

| H | usable | truncated | **EATEN** | **HELD** |
|---|---|---|---|---|
| 1 h | 277 | 0 | **150 = 54.2 %** | 127 = 45.8 % |
| 4 h | 277 | 0 | **208 = 75.1 %** | 69 = 24.9 % |
| 12 h | 276 | 1 | **242 = 87.7 %** | 34 = 12.3 % |
| 24 h | 276 | 1 | 🔴 **262 = 94.9 %** | **14 = 5.1 %** |

| H | LONG | SHORT |
|---|---|---|
| 1 h | 72/147 = 49.0 % | 78/130 = 60.0 % |
| 4 h | 117/147 = 79.6 % | 91/130 = 70.0 % |
| 12 h | 138/147 = 93.9 % | 104/129 = 80.6 % |
| 24 h | 143/147 = 97.3 % | 119/129 = 92.2 % |

**Both sides, every horizon, monotone. There is no side on which these walls hold.**

### 🔴 AND THE NUMBER THAT REFRAMES ALL OF THE ABOVE

| the distance price had to cross | min | p25 | **median** | p75 | max |
|---|---|---|---|---|---|
| wall distance % | 0.002 % | 0.096 % | 🔴 **0.129 %** | 0.253 % | 0.792 % |

**The median cited wall sits 0.129 % away.** On BTC that is ordinary 5-minute noise. **A 95 % eaten
rate at 24 h is not a discovery about walls — it is arithmetic about a threshold set inside the
noise floor.** Every statement in §2a has to be read through that, and it is the first reason the
mechanical question turns out to be less interesting than it looked.

When eaten, price does not merely touch the level — median penetration **beyond** the wall is
**+0.190 % (1 h)**, **+0.419 % (4 h)**, **+0.819 % (12 h)**, **+1.229 % (24 h)**, i.e. several times
the wall's own distance. **These walls are not slowing anything down.**

---

## §2b — DOES THE REFUSAL'S CORRECTNESS TRACK THE WALL'S FATE?

**RIGHT := drift ≤ 0**, drift = signed % move in the **signal's** direction, entry → close at H
(§2.54's basis; positive = the refused signal would have won).

| H | | refusal RIGHT | refusal WRONG | P(right) | χ² (1 df) |
|---|---|---|---|---|---|
| **1 h** | wall EATEN | 36 | 114 | **24.0 %** | **62.90** |
| | wall HELD | 91 | 36 | **71.7 %** | |
| **4 h** | wall EATEN | 74 | 134 | 35.6 % | **40.56** |
| | wall HELD | 55 | 14 | 79.7 % | |
| **12 h** | wall EATEN | 98 | 144 | 40.5 % | **38.25** |
| | wall HELD | 33 | **1** | **97.1 %** | |
| **24 h** | wall EATEN | 93 | 169 | 35.5 % | **23.29** |
| | wall HELD | 14 | **0** | **100.0 %** | |

### 🔴 THIS ASSOCIATION IS REAL, ENORMOUS, AND VERY NEARLY A TAUTOLOGY — SAY SO

χ² of 62.9 on 1 df looks like the strongest result in the book. **It is not a result at all, and the
reason is mechanical.** The opposing wall sits **in the direction the signal points**. Eating it
*means* price moved ≥ dist % the signal's way. Drift > 0 *means* price ended up the signal's way.
**"Wall eaten" and "refusal wrong" are two descriptions of the same event, separated only by
path-versus-endpoint.** With a median distance of 0.129 %, the bar "eaten" sets is so low that it is
close to asking "did price move at all".

**So the brief's §2b test resolves — but not in the direction its wording anticipated.** The brief
said: *"If a wall being eaten does NOT mean the refusal was wrong, the wall was never the operative
reason."* Here a wall being eaten **does** track the refusal being wrong. **That is not evidence the
wall is operative; it is evidence the two variables are algebraically entangled.** Reading the χ² as
support for the veto would be the same error as the 15:15 report's box — a quantity restating another
quantity and being credited as a discovery.

### THE NON-TRIVIAL RESIDUE, WHICH IS THE PART WORTH HAVING

Given the wall **was** eaten, did the move **sustain** to the horizon close?

| H | eaten | sustained | **reversed back** |
|---|---|---|---|
| 1 h | 150 | 114 = 76.0 % | 36 = 24.0 % |
| 4 h | 208 | 134 = 64.4 % | **74 = 35.6 %** |
| 12 h | 242 | 144 = 59.5 % | **98 = 40.5 %** |
| 24 h | 262 | 169 = 64.5 % | 93 = 35.5 % |

**A third to two-fifths of eaten walls are eaten and then given back.** That is the only part of §2b
not fixed by construction — and it says the wall's breach carries **no reliable information about
continuation**, which is precisely what a veto would need it to carry.

### THE VETO'S OWN DRIFT — AND THE FIRST APPEARANCE OF THE DAY PROBLEM

| H | per-signal | day-clustered |
|---|---|---|
| 1 h | +0.0478 % **t=+2.44** (n=277) | +0.0423 % **t=+0.91** (22 days) |
| 4 h | +0.0616 % t=+1.57 | **−0.0309 %** t=−0.34 |
| 12 h | +0.1741 % **t=+2.79** | +0.0379 % **t=+0.24** |
| 24 h | +0.1769 % **t=+2.07** | +0.0135 % **t=+0.06** |

🔴 **t = +2.79 becomes t = +0.24.** 277 refusals are 22 days, and treating them as 277 independent
draws inflates every t by roughly √(277/22) ≈ 3.5. **This is the SOL depth lesson and §2.54's
`ai_skipped` cell in one table.**

---

## §2c — DOES ANYTHING AT THE MOMENT DISTINGUISH AN EATEN WALL FROM ONE THAT HOLDS?

### MARGINALLY, TWO THINGS DO

| H | feature | eaten | held | perm-p (20 k) |
|---|---|---|---|---|
| 1 h | **multiple** | 5.115 | 6.400 | **0.0000** nominal |
| 1 h | **distance %** | 0.121 | 0.309 | **0.0000** nominal |
| 1 h | total depth BTC | 2893 | 2950 | 0.1675 |
| 1 h | imbalance | 0.482 | 0.487 | 0.3837 |
| 1 h | supporting wall | 6.070 | 7.607 | 0.0005 nominal |
| 4 h | multiple | 5.375 | 6.697 | 0.0002 nominal |
| 4 h | distance % | 0.161 | 0.346 | **0.0000** nominal |
| 12 h | multiple | 5.620 | 6.353 | 0.1065 |
| 12 h | distance % | 0.188 | 0.343 | **0.0000** nominal |
| 24 h | multiple | 5.607 | 7.636 | 0.0074 nominal |
| 24 h | distance % | 0.201 | 0.326 | 0.0113 nominal |

**Total depth and imbalance are inert at every horizon** (p 0.15–0.93) — the two book-wide aggregates
carry nothing about the fate of a specific level.

### 🔴 AND THE CONTROL THAT DISSOLVES THE OTHER TWO

A wall further away is harder to reach **for purely mechanical reasons**. And thick walls *are*
further away:

| | r with distance |
|---|---|
| **wall multiple** | **+0.3695** |
| **wall percentile** | **+0.361** |
| supporting wall | +0.0795 |

| multiple bucket | n | mean distance |
|---|---|---|
| 4–5× | 165 | 0.167 % |
| 5–6× | 45 | 0.210 % |
| 6–8× | 33 | 0.245 % |
| 8×+ | 34 | **0.363 %** |

**Inside distance terciles, the multiple stops working:**

| H | NEAR (<0.105 %) | MID | FAR (>0.220 %) |
|---|---|---|---|
| 1 h | p **0.0889** | p 0.1590 | p 0.2685 |
| 4 h | p 0.5505 | p 0.3279 | p 0.0270 |
| 12 h | p 0.6441 | p 0.5590 | p 0.6047 |
| 24 h | p 0.6388 | n/a (held n=1) | p 0.0117 |

**Eleven testable strata; two nominal hits, both in the FAR stratum only, at non-adjacent horizons.**
At α = 0.05 you expect ~0.55 false positives from eleven tests; two is not a pattern, and neither is
within two orders of magnitude of 0.000926.

### 🔴 THE VETO'S *ACTUAL* DIAL IS THE PERCENTILE, NOT THE MULTIPLE — SO IT WAS TESTED TOO

The prompt is explicit (`claude_advisor.py:199-203`): *"EVERY book state contains a wall above 4x, so
'large multiple' means nothing on its own. Judge by the percentile: ~50th percentile is ORDINARY, not
significant."* Testing the raw multiple alone would have tested the wrong dial. Percentile
reconstructed for **272 of 277** by ranking each refusal's wall against the trailing 7 days of the
same OKX book (**median baseline 9,913 snapshots**).

#### 🔴 AND THE RECONSTRUCTION PRODUCES THE SHARPEST MECHANICAL FACT IN THIS REPORT

| percentile of the wall being vetoed on | n | share |
|---|---|---|
| 🔴 **below the 50th — "ORDINARY" in the prompt's own words** | **191** | 🔴 **70.2 %** |
| 50th–75th | 39 | 14.3 % |
| 75th–90th | 24 | 8.8 % |
| **90th+ (genuinely thick)** | **18** | **6.6 %** |

**Median percentile of a vetoed wall: 29th.** **Seven vetoes in ten fire on a wall the prompt would
call unremarkable, and fewer than one in fifteen fires on a wall above the 90th percentile.** The
HARD RULE asks for "genuinely THICK FOR THIS BOOK"; what it is being applied to is, most of the time,
a median wall.

Eaten-rate by percentile does show a gradient at short horizons — and dies under the same control:

| H | 0–50th | 50–75th | 75–90th | 90th+ |
|---|---|---|---|---|
| 1 h | 60 % | 62 % | 29 % | **17 %** |
| 4 h | 81 % | 79 % | 50 % | 44 % |
| 12 h | 91 % | 87 % | 71 % | 83 % |
| 24 h | 97 % | 95 % | 92 % | 83 % |

**Within distance strata:** 1 h → p 0.1256 / 0.6913 / **0.9668**; 4 h → 0.0783 / 0.1022 / 0.0155;
12 h → 0.8983 / 0.4171 / 0.2838; 24 h → 0.9028 / n/a / 0.1020. **Eleven strata, one nominal hit.**

🔴 **So the veto's own dial — in the form the advisor is actually told to read — does not predict
whether the wall survives.** By 24 h the gradient is 97/95/92/83 %: **even the 90th-percentile walls
are eaten five times in six.**

---

## §3 — DE-CONFOUNDING PER §2.54

### 3a. THE VETO'S OWN DRIFT — THE SENSITIVITY TABLE IS AGAIN THE FINDING

| control | 1 h | 4 h | 12 h | 24 h |
|---|---|---|---|---|
| none (per-signal) | +0.0478 % t=+2.44 | +0.0616 % t=+1.57 | +0.1741 % t=+2.79 | +0.1769 % t=+2.07 |
| + day | +0.0423 % t=+0.91 | 🔴 **−0.0309 %** t=−0.34 | +0.0379 % t=+0.24 | +0.0135 % t=+0.06 |
| + day+direction | +0.0597 % t=+1.63 | 🔴 **−0.0105 %** t=−0.13 | 🔴 **−0.0301 %** t=−0.20 | +0.0064 % t=+0.03 |
| + day+direction+hour | +0.0653 % t=+2.24 | +0.0505 % t=+0.87 | +0.1210 % t=+1.29 | +0.1659 % t=+1.27 |

**The sign flips at 4 h and at 12 h.** Nothing reaches |t| > 3.31 at any specification. **§2.54's
ruling applies verbatim: an effect whose sign depends on the control is not an effect.**

### 3b. THE ONE CELL THAT LOOKED LIKE IT SURVIVED — AND DID NOT

The sharpest available question is not "is the veto's drift positive" but **"is a wall-citing refusal
different from the advisor's other refusals?"** If not, the wall citation is decorative and the veto
rests on whatever else the advisor was reading. Deduped `ai_skipped`: **274 wall-citing vs 135 other.**

| control | 1 h | 4 h | 12 h | 24 h |
|---|---|---|---|---|
| none (raw) | −0.0349 % t=−1.06 | +0.0224 % t=+0.33 | −0.1425 % t=−1.34 | −0.3858 % t=−2.71 |
| + day | −0.0641 % t=−1.24 | −0.1831 % t=−1.88 | −0.3572 % t=−2.10 | −0.5403 % t=−2.34 |
| + day+direction | −0.1060 % t=−2.10 | −0.1166 % t=−1.00 | 🟡 **−0.2701 % t=−3.79** | 🟡 **−0.3200 % t=−3.50** |
| 🔴 **+ day+direction+HOUR** | −0.0277 % t=−1.11 | −0.0482 % t=−1.63 | 🔴 **−0.0331 % t=−1.82** | 🔴 **−0.0392 % t=−1.60** |

**Two cells cleared |t| > 3.31 — and both collapse when the hour is added: −3.79 → −1.82 and
−3.50 → −1.60, with the effect size falling by 88 %.** Day-clustered permutation (wall label shuffled
within day+direction, 20 k draws): **p = 0.0243 / 0.2080 / 0.0033 / 0.0021 — nominal only, none
clearing 0.000926.**

⚠️ **And this control is NOT degenerate — checked, because §2.54 was caught by exactly that.**
39 (day, direction) strata, **29 contain both a wall-cited and a non-wall refusal**, and
**253 of 273 wall-cited refusals (93 %) have a same-day-same-direction comparator.** §2.54's
equivalent coverage was **16 %**. 🔴 **This is the best-controlled refusal question this book has
run — and it still finds nothing.** That makes the null considerably more informative than §2.54's.

### 3c. THE ASSOCIATION THAT *DOES* SURVIVE CONTROL — AND WHY IT PROVES NOTHING

eaten-minus-held drift, paired within day+direction+hour: **+0.1490 % t=+3.74 (1 h)**,
+0.1780 % t=+2.72 (4 h), **+0.3115 % t=+3.36 (12 h)**, +0.4164 % t=+3.30 (24 h).

**These survive every control, and they are the tautology from §2b.** Price that broke through an
upside level and price that closed higher are the same price. **Recording it as a positive finding
would be the nineteenth branch dying with a false headline attached**, so it is recorded here as an
arithmetic check that the pipeline is wired correctly — which it is.

---

## §4 — VERDICT

### 🔴 NOTHING SURVIVES. NINETEENTH CLOSURE, ON EVIDENCE.

| §4 condition | fired? | why |
|---|---|---|
| something survives → show the shape with n and corrected p, and STOP | 🔴 **NO** | Two cells reached \|t\| > 3.31 at day+direction; **both collapsed to \|t\| < 1.9 when the hour was added**, clustered perm-p 0.0033 / 0.0021 — nominal. Nothing else came within two orders of magnitude of 0.000926 |
| nothing survives → say so; that is the closure and it prevents a filter | ✅ **THIS ONE** | Said here |

**No filter is proposed. No threshold. No diff. Nothing is applied.**

### 🔴 DOES THE WALL VETO ITSELF STILL EARN ITS PLACE? — THE OLDER QUESTION, ANSWERED PLAINLY

**It does not earn its place on its stated mechanism, and it does not demonstrably cost anything
either. Both halves have to be said, and the honest status is: UNFALSIFIED BUT UNSUPPORTED.**

**Against it — three findings, all new here:**
1. **The premise is false as stated.** The HARD RULE says thick resting liquidity *"will absorb the
   move before it can develop"*. **It absorbs nothing: 95 % of cited walls are eaten within 24 h,
   87.7 % within 12 h, and when eaten price travels a median +1.229 % beyond them.** Even
   90th-percentile walls are eaten **83 %** of the time by 24 h.
2. **The dial carries no information.** Neither multiple nor percentile predicts survival once
   distance is held fixed (22 strata tested across both, **two isolated nominal hits**). What looks
   like thickness is distance: r = +0.37 / +0.36, monotone across every bucket.
3. 🔴 **The veto is mostly not firing on thick walls at all. 70.2 % of vetoed walls sit below the
   50th percentile** — the exact region the prompt tells the model to treat as *"ORDINARY, not
   significant"*. **Median 29th percentile.** Whatever is driving these refusals, "a genuinely thick
   wall" describes fewer than one in fifteen of them.

**For it — and this is why the answer is not "retire it":**
4. **Its measured cost is zero.** Day-clustered drift **t = +0.91 / −0.34 / +0.24 / +0.06** — the
   refused signals were not systematically winners. The brief's inversion (−0.093 % → +0.104 %) is
   fully explained as sampling noise across 22 days.
5. **What signal there is points the safe way.** Wall-cited refusals drift *less* favourably than the
   advisor's other refusals at every horizon under day+direction (−0.11 % to −0.32 %). It does not
   survive the hour control — **but nothing in this book suggests the veto is refusing winners.**

🔴 **THE CONCLUSION, STATED SO IT CANNOT BE MISREAD:** the wall veto is **not doing what it says it
is doing** — but on 277 refusals across 22 days, **with the best-controlled comparator structure this
book has achieved (93 %), it cannot be shown to cost anything.** Relaxing it is a change with its own
risk class: §2.54 measured that cascade relaxation roughly **doubles** the entry rate, and the only
measured positive in this system remains the exit advisor at n=5. **A gate whose mechanism is wrong
but whose cost is zero is not an emergency; it is a candidate for retirement on a live sample, not on
this one.** The same ~30 live entries §2.45 and §2.47 are already waiting for would settle it.

### 🔴 NINETEENTH DEAD BRANCH, FOR §2.45's LIST

| # | branch | verdict |
|---|---|---|
| 19. | **the cited wall's own fate as a signal** (eaten vs held × refusal-correct, and multiple / percentile / depth / imbalance / supporting wall as discriminators of survival) | 🔴 **dead.** The eaten↔wrong association is **algebraic, not empirical**. No discriminator survives the distance control. The veto's drift is **zero under day clustering and flips sign at two horizons**. The one cell clearing \|t\|>3.31 collapsed on adding the hour |

---

## LIMITS — WHAT WOULD CHANGE THIS, AND WHAT WOULD NOT

1. 🔴 **22 days is the binding constraint, not 277 signals.** Every per-signal t in this report is
   inflated ~3.5×. More refusals from the same fortnight will not help; **more days will.**
2. **"Eaten" is a low bar by construction** — median distance 0.129 %. A study of walls at
   materially greater distance would be a different question, but the bot does not cite those:
   **p75 is 0.253 %** and the max in the entire cohort is 0.792 %.
3. **Drift is not PnL** (§2.54's standing warning, carried): no stop, no trail, no fees, no partial.
   A positive drift means a refused **move**, not a refused **winner**.
4. **The percentile is reconstructed, not the stored one.** It ranks each wall against the trailing
   7 days of the same OKX-4000 book; the live prompt's percentile uses the engine's own baseline.
   r(reconstructed percentile, raw multiple) = **+0.845**. The reconstruction is faithful enough to
   rank, and the 70.2 %-below-median finding is robust to any monotone rescaling — **but it is a
   reconstruction and is labelled as one.**
5. **This says nothing about the EXIT advisor's use of the book**, which is a different consumer with
   a different prompt and remains the only measured positive in the system.

---

## LIVE STATE, AS OF THIS REPORT

| | |
|---|---|
| open positions | **0** |
| `titan-bot` HEAD / `git status` | **`b9081ad`** / **clean** |
| wall-citing advisor refusals since 2026-07-13 (deduped) | **277** on **22 days** |
| OKX-4000 snapshots | **33,486** |
| 🔴 `ema_envelope_blocked` rows (§2.47's FAST TRIGGER needs n ≥ 100) | **19** |
| clean closed positions on the post-17:01:29 geometry | 🔴 **0** |

---

## APPENDIX — WHAT WAS RUN

| file | purpose | cells |
|---|---|---|
| `fetch_candles.py` | 7,132 BingX 5m bars, zero gaps | — |
| `engine.py` | cohort + dedupe + bounded snapshot join + age distribution; §2a eaten/held, per side, penetration | ~16 |
| `s2b.py` | §2b cross-tab, χ², the tautology decomposition, sustained-vs-reversed, drift by fate, day-clustered drift | ~16 |
| `s2c.py` | §2c marginal features, within-distance strata, multiple/distance dials; §3a sensitivity ladder; §3c eaten-drift under control | ~55 |
| `s3b.py` | the multiple↔distance confound; day-clustered §2c permutations | ~15 |
| `s4.py` | replay validation; wall-cited vs other-refusal population comparison | ~10 |
| `s5.py` | §3b full sensitivity ladder, degeneracy check, day+direction-clustered permutations | ~24 |
| `s6.py` | percentile reconstruction (272/277) and the whole §2c battery re-run on the veto's actual dial | ~19 |

**Total ≈ 146 cells.** Permutations are 20,000 draws, two-sided, seed 20260805; day-clustered
permutations shuffle the label **within** day (or day+direction), preserving the day structure.

⚠️ **ONE TRAP CAUGHT, RECORDED RATHER THAN QUIETLY FIXED.** A **0-byte `/root/trades.db`** exists
alongside the real 67 MB `/root/titan-bot/trades.db`. A relative open from the wrong working
directory hits the decoy — it has **no tables**, so it raises rather than silently returning zero
rows, which is the only reason it was caught immediately. **Every query in this report pins the
absolute path.** This is a sibling of the SQLite-affinity trap already in the book: the failure mode
that returns *nothing* is survivable; the one that returns *something wrong* is not.

*Read-only throughout. `titan-bot` unmodified at `b9081ad`, `git status` clean, 0 open positions for
the entire pass, `trades.db` opened read-only. Mercury-SOL never opened.*
