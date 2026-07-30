# TITAN §2.21 — DOES ENTRY BOOK DEPTH PREDICT OUTCOME? Measured. It does not, and n could not have shown it if it did.

_2026-07-30 03:55 UTC · HEAD `957f980` · READ-ONLY · nothing proposed, nothing changed_

---

## ANSWER FIRST

**No relationship is detectable, and the honest reason is that n=11.** Spearman
rho(entry depth percentile, realised R) = **+0.209, permutation p = 0.541**. The point estimate
is the **opposite sign to the hypothesis** and is indistinguishable from zero.

**The decisive evidence is not the p-value — it is that the sign of the effect flips depending on
where the bucket line is drawn.** Cut into halves, thin looks *better*. Cut into thirds, thick looks
better. Both cuts, same 11 trades. That is the signature of noise, and it is exactly the shape the
brief warned about.

**To confirm a correlation of the size observed would need n ≈ 177.** To detect even a strong
rho = 0.4 needs n ≈ 47. We have **11**. At the current accrual rate (~0.71 positions/day) n=47 is
about **7 weeks** away.

**Two things I found while measuring that matter more than the answer:**

1. 🔴 **The brief's premise is wrong: depth was NOT "shown correctly to both advisors" for this
   cohort.** The exit advisor rendered `Total depth = n/a` on **59 of its 68 consults**, and only
   **16 entry prompts in history** ever carried a depth line. For **10 of the 11** positions measured
   here, **neither advisor saw depth at all.** It was not ignored — it was absent.
2. 🔴 **Depth is heavily confounded with volatility, and with time of day at a magnitude equal to
   its entire IQR.** Any future depth finding will have to be disentangled from ATR first.

---

## 1. MATCHING — how many of the 53 clean closes can be measured at all

**11.** The binding constraint is not the §0 filters — it is baseline coverage.

| step | n |
|---|---:|
| clean closed positions (`status='closed'`, excludes 6 `archived_pre_geometry_fix`) | 53 |
| …opened after `orderbook_density` begins (2026-07-13T02:34:56) | **12** |
| …after §0 filter *Recheck TIGHTEN* (`recheck_status <> 'tightened'` — drops vpos 74) | **11** |
| …after §0 filter *wall-trail lifetime overlap* | 11 *(binds nothing: all 11 opened after the window closed at 07-13T01:55)* |
| …after §0 filter *forming-candle* (`>= 2026-07-04 11:58`) | 11 *(binds nothing: all are later)* |

**42 of the 53 clean closes are unmeasurable for this question** — they closed before the collector
existed. No amount of care recovers them.

Matching used the **same bounded-nearest-row method as the `625fedc` entry-reference fix** (±600 s,
age carried and printed). Match quality was excellent — the collector's 60 s cadence means worst
case ~30 s:

```
vpos side  entry_depth  pct  age_s | exit_depth  pct  age_s |      R      net  reason
  75 LONG       2401.1    4     19 |     2972.0   46     11 |  -0.03   -14.52  external
  76 SHORT      2933.9   41      2 |     3098.2   62     13 |  +0.41   +45.36  external
  77 SHORT      3227.2   77     29 |     2774.7   25      1 |  -1.01  -132.75  sl
  78 LONG       2898.1   37     24 |     2850.9   32      3 |  -1.08  -103.54  sl
  79 LONG       2915.7   39     11 |     3185.1   73      3 |  +0.57   +80.10  trail
  80 SHORT      3121.6   65      1 |     2860.2   33      2 |  -1.01  -116.58  sl
  81 SHORT      3128.3   66      6 |     3022.4   53     17 |  +0.84   +75.24  trail
  82 LONG       3668.6   98      8 |     3172.3   71     25 |  +1.23   +53.79  trail
  83 SHORT      3097.4   62     11 |     3230.6   77     23 |  -1.03  -143.67  sl
  84 LONG       2743.5   23     14 |     3027.8   53      1 |  +0.21   +16.54  external
  85 LONG       3113.6   64     21 |     2442.1    6     15 |  -1.00  -137.32  sl

MATCHED 11/11 at entry and 11/11 at exit. Worst age 29 s. Baseline n=24,106, range 1510-4196 BTC.
```

**Independent validation of the method:** vpos 85 is the only position whose entry prompt carries a
stored depth line (the feature landed in `8b15ecc` on 07-29). The prompt recorded
**`Book depth: 3,114 BTC — 63th pct`**; my reconstruction gives **3113.6 BTC, 64th pct**. The method
reproduces what the machine actually saw.

---

## 2. OUTCOMES BY ENTRY DEPTH PERCENTILE

Deciles are impossible at n=11. Even thirds give 3–4 per bucket.

| bucket | n | wins | win rate | net $ | **median R** | mean R |
|---|---:|---:|---:|---:|---:|---:|
| THIN — p4–p39 | 4 | 2 | 50% | −21.41 | **+0.09** | −0.08 |
| ORDINARY — p41–p64 | 4 | 1 | 25% | −352.21 | **−1.00** | −0.66 |
| THICK — p65–p98 | 3 | 2 | 67% | −3.72 | **+0.84** | +0.35 |

**By side — printed because it was asked for, not because 2–4 per cell decides anything:**

```
LONG  n=6:  p4→R−0.03 · p23→R+0.21 · p37→R−1.08 · p39→R+0.57 · p64→R−1.00 · p98→R+1.23
SHORT n=5:  p41→R+0.41 · p62→R−1.03 · p65→R−1.01 · p66→R+0.84 · p77→R−1.01
```

There is no monotone pattern in either side. The worst bucket is the **middle** one, which no
mechanism predicts and which is what noise looks like when it is cut into three.

---

## 3. THE HYPOTHESIS — stated so it could fail, and it failed

> *A thin book means price moves on little volume, so entries into a thin book should be noisier —
> more stop-outs, worse median R.*

**NOT SUPPORTED. The point estimate runs the other way, and neither direction is distinguishable
from zero.**

```
Spearman rho(entry depth pct, realised R) = +0.209    permutation p = 0.541  (200,000 shuffles)
stop-outs: 5/11 — their entry depth percentiles: 37, 62, 64, 65, 77
winners:  23, 39, 41, 66, 98        losers: 4, 37, 62, 64, 65, 77
```

Every stop-out sits in the **middle** of the depth range (p37–p77). The thinnest entry in the
cohort (p4) did **not** stop out; the thickest (p98) was the best trade. H1 predicts the reverse of
both.

### Is there a depth level below which outcomes deteriorate? No — and here is the proof it is noise

**The answer changes sign depending on where the line is drawn:**

| split | thin-side median R | thick-side median R | supports H1? |
|---|---:|---:|---|
| halves (5/6) | +0.21 | −1.00 | **CONTRADICTS** |
| halves (6/5) | +0.09 | −1.00 | **CONTRADICTS** |
| thirds (4/3) | +0.09 | +0.84 | supports |
| extremes (3/3) | −0.03 | +0.84 | supports |

By absolute BTC threshold, the same instability:

| threshold | n below | median R below | n above | median R above |
|---:|---:|---:|---:|---:|
| 2700 | 1 | −0.03 | 10 | −0.39 |
| 2800 | 2 | +0.09 | 9 | −1.00 |
| 2900 | 3 | −0.03 | 8 | −0.29 |
| 3000 | 5 | +0.21 | 6 | −1.00 |
| 3100 | 6 | +0.09 | 5 | −1.00 |
| 3200 | 9 | −0.03 | 2 | +0.11 |

**A real effect does not reverse when you move the cut by one trade. This one does, twice.**
No threshold exists in this data, and none should be inferred from it.

---

## 4. CONFOUNDS — checked, not assumed. Both matter.

### 4a. Time of day is a first-order confound — but NOT in the direction the brief assumed

Tested on the **full baseline, n=24,111**, so this part is *not* underpowered.

| session (UTC) | n | median depth | p25 | p75 |
|---|---:|---:|---:|---:|
| Europe (08–12) | 5,016 | **3,131** | 2,970 | 3,307 |
| Asia (00–07) | 8,082 | 3,017 | 2,859 | 3,204 |
| US/overlap (13–20) | 8,002 | 2,957 | 2,675 | 3,183 |
| late US (21–23) | 3,011 | **2,697** | 2,436 | 2,964 |

**Session median spread = 434 BTC. Overall IQR = 437 BTC. Ratio 0.99** — the time-of-day swing is
as large as the entire interquartile range of the depth distribution. Hour 21 UTC has median
**2,413**; hour 09 has **3,177**. **A depth percentile is, to a first approximation, a clock.**

🔴 **Correction to the brief:** *"the Asian session is structurally thinner"* — **it is not.** Asia
(median 3,017) is **thicker** than both US windows. The thin session is **late US, 21–23 UTC**, and
hour 21 alone is the thinnest hour of the day by a wide margin. If "thin book" turns out to mean a
clock hour, it means **21:00 UTC**, not 3am.

Within the n=11 cohort the entry-hour correlation is weak (rho −0.118) only because the 11 entries
are scattered across all four sessions (hours 0,1,2,11,13,13,15,15,17,18,21) — too few per session
to register.

### 4b. Depth is strongly entangled with VOLATILITY — the more serious confound

Within the cohort (n=11, so directional only):

| pair | rho |
|---|---:|
| entry depth pct vs **ATR% 1h** | **−0.673** |
| entry depth pct vs **ADX 1h** | **−0.518** |
| entry depth pct vs ATR 5m | −0.464 |
| entry depth pct vs vol_ratio_5m | +0.300 |
| entry depth pct vs UTC hour | −0.118 |

**Thin book ≈ high volatility, strong trend.** This is mechanically sensible — volatility thins a
book — and it is why *any* future depth→outcome result must be disentangled from ATR before it can
be believed. A "thin book is bad" finding and an "ATR is high" finding would be the same finding
wearing different clothes. **At n=11 they cannot be separated at all.**

### 4c. Era — no confound within the cohort, and that is itself a limitation

**All 11 are PAPER positions at $2,000 margin / $10,000 notional.** vpos 86 is the only live row and
it is still open, so it contributes nothing. There is **zero live-money data** in this measurement.

### 4d. Baseline drift — mild

Daily median depth ranges **2,607 → 3,386** across the 18 days (low 07-30 and 07-20; high 07-25).
A percentile against the pooled baseline therefore mixes regimes somewhat, but the drift is small
relative to the session effect in 4a.

---

## 5. CAN n SUPPORT THE QUESTION? No, and here is the number

Fisher-z, α = 0.05 two-sided, power = 0.80:

| to detect | required n |
|---|---:|
| rho = 0.60 | 19 |
| rho = 0.50 | 29 |
| rho = 0.40 | 47 |
| rho = 0.30 | 85 |
| rho = 0.25 | 123 |
| **rho = 0.209 (what was observed)** | **177** |

**We have 11.** Accrual since the collector started: 12 positions in 17 days ≈ **0.71/day**.

| target | more positions needed | ~time |
|---|---:|---:|
| n = 29 | 18 | ~4 weeks |
| n = 47 | 36 | ~7 weeks |
| n = 85 | 74 | ~15 weeks |

**This question is not answerable today and will not be for about two months at the current rate.**
Reporting it as "no relationship found" would be as wrong as reporting a relationship: the correct
statement is that the measurement has **no power to distinguish the two**.

---

## 6. THE EXIT SIDE — no relationship either, and I had to fix my own metric first

**Judged from real candles after the close** (§0 filter 4 — stored extrema stop updating at close,
so they cannot answer this).

### The metric flaw I caught, stated because it nearly became a finding

My first measure was *max favourable excursion after exit, in R*. It returned **11/11 positive** —
every exit apparently left money on the table, which looks like a dramatic result about exit timing.

**It is an artifact.** The maximum of a random walk over a 4-hour window is positive almost surely,
whatever the exit did. The measure cannot return anything else. **Discarded.**

The unbiased version is the **endpoint** move at a fixed horizon:

```
vpos side  exit_pct realisedR  endpoint4h  endpoint12h  reason
  85 LONG         6     -1.00       -0.28        +0.43  sl
  77 SHORT       25     -1.01       -0.54        -0.41  sl
  78 LONG        32     -1.08       +0.17        +0.40  sl
  80 SHORT       33     -1.01       -0.07        +1.84  sl
  75 LONG        46     -0.03       +0.26        +0.62  external
  81 SHORT       53     +0.84       +0.02        -0.03  trail
  84 LONG        53     +0.21       -0.38        -0.27  external
  76 SHORT       62     +0.41       +0.36        -1.24  external
  82 LONG        71     +1.23       +0.19        +0.02  trail
  79 LONG        73     +0.57       +0.09        +0.00  trail
  83 SHORT       77     -1.03       -0.34        +0.28  sl
```

| measure | result |
|---|---|
| endpoint 4h | **6/11 positive**, median **+0.02** |
| endpoint 12h | **7/11 positive**, median **+0.02** |
| rho(exit depth pct, endpoint 4h) | **+0.236** |
| rho(exit depth pct, endpoint 12h) | **−0.282** |

A coin flip, and **the correlation flips sign between the two horizons** — the same instability as
the entry side. **Depth at exit carries no detectable information about whether the exit was good.**

---

## 7. THE PREMISE CORRECTION — depth was mostly not shown to anybody

§2.21 records depth as *"shown correctly to BOTH advisors and weighted by NEITHER."* That is true of
**vpos 85 and vpos 86 only.** For the rest of this cohort it was never rendered:

| surface | when depth became visible | coverage |
|---|---|---|
| ENTRY advisor | `8b15ecc`, 2026-07-29 09:56 | **16** prompts in the bot's entire history carry `Book depth:` |
| EXIT advisor | `4fc89ea`, 2026-07-29 12:31 | **59 of 68** consults rendered `Total depth = n/a`; only **9** ever carried a real figure |

**For 10 of the 11 positions measured here, neither advisor saw depth at all.** "Ignored" is the
wrong word; "absent" is the right one.

**This is methodologically fortunate and worth keeping.** Because nothing acted on depth during this
period, depth is a **clean observational variable** here — there is no feedback loop between the
measurement and the outcome. Whatever the eventual answer, this window is uncontaminated by the
advisors reacting to the number. That property will be **lost** for positions from 2026-07-29
onward, where both advisors do see it.

---

## WHAT THIS DOES AND DOES NOT ESTABLISH

**Established:**
- 11 of 53 clean closes are measurable; the other 42 predate the collector and are unrecoverable.
- The matching method reproduces the one stored depth figure exactly (3113.6/64th vs 3114/63rd).
- No detectable entry-depth→outcome relationship (rho +0.209, p 0.541), sign unstable across cuts.
- No detectable exit-depth→exit-quality relationship, sign unstable across horizons.
- Depth's time-of-day structure is real and large (spread ≈ IQR), and the thin session is **late US
  21–23 UTC**, not Asia.
- Depth is strongly anti-correlated with ATR and ADX — the confound that would have to be broken.
- Required n is ~47 for a strong effect, ~177 for the effect actually observed.

**NOT established, and not to be read into this:**
- That depth carries no information. **Absence of power is not absence of effect.**
- Any threshold, level, or direction. The data reverses itself under re-cutting.
- Anything about live-money behaviour — all 11 are paper.

**Nothing is proposed. No filter, no weight, no threshold.** §2.21 stays open, and the honest
status is: *not yet measurable, ask again at n≈47 (~7 weeks), and disentangle ATR when you do.*
