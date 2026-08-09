# sol-book-liquidity-measured-filter-22-refused-facts-on-the-card

_2026-08-09 16:25 UTC_

---

# Mercury-SOL — the three untested book quantities, measured. **Nothing separates. Filter 22 is REFUSED.** The book facts now print beside the model's reason.

**The operator's question was the right one and it had never been asked: not "is there a wall
against us" but "is there liquidity at all, and which way is it leaning". It has now been asked
properly, on 415 refusals across 8 days, with the family declared before any result.**

**The answer is no.** One cell out of 27 survived Bonferroni and both de-confounding controls —
imbalance leaning WITH a LONG, at 4h. It then **failed the out-of-sample split**: strong in
2026-08-02→04 (ρ=+0.42, p=0.0012), gone in 2026-08-05→08 (ρ=+0.10, p=0.38). At 24h it does not
merely fade, it **reverses** — +0.51 in the first half, **−0.36 in the second, both "significant"**.
And the SHORT side carries the opposite sign at every horizon. That is a 7-day sample generating
patterns, not a market fact.

🔴 **I also have to correct my own method mid-pass.** My first de-confound compared a within-day
permutation null against the RAW correlation. That is invalid — within-day shuffling preserves the
between-day component in both variables, so the null is not centred at zero and a pure day effect
can show an arbitrarily small p. Redone as a proper within-day partial correlation. **Two of the
four "survivors" from the first pass were artefacts of my own test.**

**APPLIED (§4 only): the book FACTS now render directly under the advisor's reason on the entry
card** — imbalance, nearest opposing wall, nearest supporting wall, each with the percentile from
**the same function that produced the prompt's numbers**. No verdict, no contradiction flag, no
gate. It is on disk and **NOT loaded** — vpos 30 is open.

Prior: [15:40 — the fourth false claim](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1540-sol-first-night-live-the-close-reconciled-against-the-venue.md) ·
[2026-08-08 Fisher p=1.0000](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1752-sol-naked-alerts-resolved-on-evidence-be-decided-reason-is-narration.md)

---

## 0. WHAT WAS MEASURED, AND HOW THE NUMBERS ARE DEFINED

Everything comes from `advisor_book_json` — the **OKX `books-full`, 4000 levels per side**, keyless
public REST, the exact dict handed to `consult_for_entry`. 434 snapshots exist, 2026-08-02 17:10 →
2026-08-09 14:00.

| quantity | definition | source |
|---|---|---|
| **(a) imbalance** | Σ(price×size) of bids within −1% of mid ÷ Σ both sides within ±1%. >0.5 = bid-heavy | `liquidity_zones.py:210-216`, stored |
| **(b) depth** | 🔴 **the stored field is a CONSTANT** — see below | reconstructed |
| **(c) supporting structure** | nearest wall BEHIND the entry (bid for LONG, ask for SHORT): percentile, multiple, distance | `skip_attribution._wall_shape` |

**Orientation, applied throughout:** every quantity is expressed as *leaning WITH the proposed
side*. For a SHORT, `lean = 1 − imbalance`. So "higher" always means "the book favours the trade we
were about to take".

**Sign convention (canon, `skip_attribution.py:317`):** `drift_pct > 0` = price moved the refused
signal's way = **we missed a move by refusing.**

### 🔴 (b) — THE STORED DEPTH FIELD IS NOT A DEPTH. It has ZERO variance.

```
depth values across all 434 snapshots : {8000: 434}
```

`liquidity_zones.py:250` sets `'depth': len(bids) + len(asks)` — the **number of price levels
returned**, which is 4000+4000 for every successful fetch. It is a fetch-size constant, not a
liquidity measure. **§1(b) as literally specified cannot be computed from what is stored, and
saying so is the honest answer.**

**So I reconstructed a real one.** `_walls` stores `vol` and `mult = vol / mean_vol`, therefore
`mean_vol` is recoverable per side:

```
mean_bucket_usdt = Σ vol / Σ mult          (mult-weighted: minimises the 1-dp rounding error)

verified on the 2026-08-09 14:00 snapshot:
  bids: 7198763/15.9=452752 · 3162572/7.0=451796 · 1990717/4.4=452436 · 2020881/4.5=449085
  asks: 7555374/14.9=507072 · 3200967/6.3=508090 · 2115109/4.2=503597 · ...  -> ~507k
```

That is **USDT of resting size per $0.50 price bucket** — a genuine density, comparable across
snapshots (same bucket size, same 4000 levels). It is used as the depth quantity everywhere below,
and it is a **reconstruction, not a stored fact** — stated so it is never quoted as one.

### A note on percentiles, so two numbers are never confused

§1 and §2 rank walls against the **empirical population of stored snapshots** (n=3,529 multiples).
The advisor's prompt — and the new card in §4 — use `claude_advisor._wall_pctl`, a fixed
breakpoint table cut from **23,080** multiples. They differ slightly (vpos 30's supporting wall:
p73 empirical, **p64 canonical**). **§4 deliberately uses the canonical one**, because the card
must speak the same number as the prompt.

---

## 1. THE THREE QUANTITIES ON CLOSED POSITIONS — 🔴 n = 3. NOT MEASURABLE.

**Stated before any result, as instructed.**

```
closed positions in the whole book            : 23
of those, carrying an OKX-4000 book           :  3     <- vpos 27, 28, 29
open positions carrying a book                :  1     <- vpos 30
```

The other 20 predate the 2026-08-02 wiring of `advisor_book_json` and carry no book at all.

**A small correction to the brief: it is 3, not 2.** vpos 29 is easy to miss because its entry row
16767 is `status='failed'` — yesterday morning's fill-read failure — but the advisor consult ran and
the book *was* captured before the failure, so the snapshot exists.

| vpos | side | mode | (a) lean WITH | (b) density | (c) nearest SUPPORTING | nearest OPPOSING | outcome |
|---|---|---|---|---|---|---|---|
| 27 | SHORT | paper | **0.4933** against | 967 724 | $72.75 p97 ×21.3 0.34% | $72.25 p100 ×30.6 0.34% | **−0.660R** |
| 28 | SHORT | paper | **0.4252** against | 929 236 | $72.75 p69 ×9.5 0.04% | $72.75 p94 ×19.1 0.04% | **−0.153R** |
| 29 | LONG | **LIVE** | **0.4847** against | 951 613 | $74.75 p84 ×14.4 0.04% | $74.75 p71 ×10.1 0.04% | **+1.355R** |
| 30 | LONG | **LIVE** | 0.5008 with | 901 053 | $76.25 p73 ×10.4 0.07% | $76.25 p55 ×6.5 0.07% | open |

🔴 **THE ANSWER IS "NOT MEASURABLE", AND I AM GOING NO FURTHER WITH IT.** Three closed positions.
All three had books leaning **AGAINST** them, inside a 0.06-wide band. Two lost, one won — and the
one that won is the one whose book leaned against it most among the losers' range. A quartile split
of n=3 is not a statistic, and the density spread (929k–968k) is a third of one standard deviation
of the refusal cohort. **There is no discriminating power here whatsoever. §1(d) is not computed,
because computing it would be reading a tail.** On to §2, which is where the sample is.

---

## 2. THE REFUSAL COHORT — 415 refusals, 8 days

```
refusals carrying full book structure + imbalance : 415   (all ai_skipped)
distinct DAYS                                     :   8   2026-08-02 .. 2026-08-09
LONG / SHORT                                      : 153 / 262
forward drift present  4h / 12h / 24h             : 413 / 390 / 378
wall population for empirical percentiles         : 3391 multiples

per day: 08-02  32 | 08-03  44 | 08-04  97 | 08-05  76
         08-06  82 | 08-07  23 | 08-08  31 | 08-09  30
```

🔴 **The effective n is 8 DAYS, not 415 signals**, and every conclusion below is governed by that.
415 refusals inside 8 days are not 415 independent draws — a day's regime is shared by every
refusal in it. This is the same rule that reduced the 2026-08-08 wall study from n=396 to 6.

### (a) 🔴 A METHOD CORRECTION TO MY OWN FIRST PASS

My first de-confound permuted drift **within day** and compared the resulting null against the
**raw** correlation. **That is wrong.** Within-day shuffling preserves the between-day component of
the association in *both* variables, so the null distribution is centred on the between-day
correlation rather than on zero — a pure day effect can therefore produce an arbitrarily small p.
It reported two survivors, one of which (`depth SHORT 12h`) had a day-blocked p **smaller** than its
uncorrected p, which is the tell.

**Corrected control — a within-day PARTIAL correlation:** rank both variables, subtract each day's
own mean rank from both, correlate the residuals. The day, and everything constant within it
(regime, session, volatility level), is projected out by construction, and within-day permutation
then gives a null that **is** centred at zero. A second control repeats it demeaned by
**(day, 6-hour block)** jointly.

**FAMILY DECLARED BEFORE ANY RESULT: 3 quantities × 3 horizons × 3 slices = 27 tests.
Bonferroni α = 0.05/27 = 0.001852. 20 000 permutations per test.**

### (b) THE HEADLINE TABLE — does the tape go anywhere different?

Binary, the operator's question in its plainest form:

| slice | horizon | book leans **WITH** | book leans **AGAINST** | gap |
|---|---|---|---|---|
| POOLED | 4h | n=232 +0.040% (win 51.7%) | n=181 −0.092% (win 42.0%) | +0.133 |
| POOLED | 12h | n=231 +0.076% (win 63.6%) | n=159 −0.007% (win 51.6%) | +0.084 |
| POOLED | 24h | n=229 +0.159% (win 52.8%) | n=149 +0.397% (win 63.1%) | **−0.239** |
| **LONG** | 4h | n=99 +0.040% (48.5%) | n=54 **−0.434%** (18.5%) | **+0.474** |
| **LONG** | 12h | n=99 +0.075% (50.5%) | n=54 −0.357% (35.2%) | +0.432 |
| **LONG** | 24h | n=97 +0.689% (82.5%) | n=54 +0.318% (77.8%) | +0.371 |
| SHORT | 4h | n=133 +0.040% (54.1%) | n=127 +0.053% (52.0%) | −0.013 |
| SHORT | 12h | n=132 +0.077% (73.5%) | n=105 +0.172% (60.0%) | −0.095 |
| SHORT | 24h | n=132 −0.231% (31.1%) | n=95 +0.442% (54.7%) | **−0.673** |

**The LONG column looks like a finding.** Consistent sign, consistent magnitude across three
horizons, and the AGAINST bucket is genuinely poor (18.5% win rate at 4h). **The SHORT column is
its mirror image with the opposite sign, and the pooled row flips at 24h.** A liquidity effect that
helps longs and hurts shorts by the same mechanism is not a liquidity effect — it is direction.

### (c) THE FULL 27 UNDER CONTROL

Ranked by the corrected within-day p (RAW = uncontrolled, +HOUR = day-and-hour demeaned, DAY = one
point per day):

```
quantity slice  h    n     RAW      WITHIN-DAY  p        +HOUR      p        DAY     verdict
depth    SHORT  12h  237  -0.1366  -0.3290  p=0.0001   -0.0807  p=0.2651  -0.381  Bonf-pass
lean     LONG   4h   153  +0.2736  +0.2891  p=0.0002   +0.3380  p=0.0001  +0.429  Bonf-pass
depth    SHORT  24h  227  +0.0926  -0.2259  p=0.0007   +0.0886  p=0.2072  +0.107  Bonf-pass
sup_p    POOLED 12h  390  -0.1388  -0.1605  p=0.0015   -0.1253  p=0.0215  +0.357  Bonf-pass
lean     SHORT  24h  227  -0.2178  +0.1842  p=0.0070   +0.2072  p=0.0024  -0.286  dies
lean     LONG   12h  153  +0.0877  +0.2055  p=0.0094   +0.3790  p=0.0001  +0.429  dies
... 21 further tests, all p > 0.018 ...

SURVIVORS at Bonferroni 0.001852 : 4 of 27
survive at UNCORRECTED 0.05      : 8 of 27
```

**Three of the four collapse immediately:**

- 🔴 **`depth SHORT 12h` — DEPTH IS A CLOCK, AGAIN.** ρ goes from −0.329 (p=0.0001) to **−0.081
  (p=0.265) the moment the hour is controlled.** And the raw distribution says why:
  ```
  thinnest-quartile readings (n=104), by 6-hour block:
     00-06h   9   ( 8.7%)      12-18h  18  (17.3%)
     06-12h  23   (22.1%)      18-24h  54  (51.9%)   <- more than half
  by DAY:
     08-02  19 | 08-03   8 | 08-04  57  (54.8% of ALL thin readings)
     08-05  13 | 08-07   7 |    08-06, 08-08, 08-09: ZERO
  ```
  **One day supplies 54.8% of every "thin" reading and three of eight days supply none.** "Thin
  book" is not a market state on this sample — it is a label for the evening of 2026-08-04. This is
  the identical failure the brief warned about, reproduced exactly.
- **`depth SHORT 24h`** — sign flips three times: RAW **+**0.093, WITHIN **−**0.226, +HOUR
  **+**0.089. Incoherent. Dead.
- **`sup_p POOLED 12h`** — one horizon of three (4h and 24h are ~0), fails Bonferroni once the hour
  is controlled (p=0.0215), and the day-level view carries the **opposite** sign (+0.357 vs
  −0.161). Also note the sign is *backwards* from the hypothesis: a thicker wall behind us
  predicting **less** drift our way. Dead.

### (d) 🔴 THE ONE SURVIVOR, AND HOW IT DIED

`lean × LONG × 4h` — imbalance leaning WITH the long. It passes everything the first three failed:

```
RAW ρ=+0.2736 · WITHIN-DAY ρ=+0.2891 p=0.0002 · +HOUR ρ=+0.3380 p=0.0001 (STRENGTHENS)
DAY-LEVEL ρ=+0.429 (n=7, same sign)
LEAVE-ONE-DAY-OUT — survives all seven:
   drop 08-02 ρ=+0.285 p=0.0008    drop 08-06 ρ=+0.294 p=0.0018
   drop 08-03 ρ=+0.260 p=0.0028    drop 08-07 ρ=+0.300 p=0.0010
   drop 08-04 ρ=+0.207 p=0.0244    drop 08-08 ρ=+0.300 p=0.0002
   drop 08-05 ρ=+0.368 p=0.0002
```

**That is a serious-looking result, and it is why the holdout exists.**

```
🔴 TIME-SPLIT HOLDOUT
   4h   EARLY (08-02..08-04) n=70  ρ=+0.4207  p=0.0012
        LATE  (08-05..08-08) n=83  ρ=+0.0976  p=0.3829     <- gone
   12h  EARLY                n=70  ρ=+0.5777  p=0.0002
        LATE                 n=83  ρ=-0.1785  p=0.1290     <- sign flipped
   24h  EARLY                n=70  ρ=+0.5131  p=0.0002
        LATE                 n=81  ρ=-0.3580  p=0.0018     <- REVERSED, AND SIGNIFICANT
```

**At 24h the effect does not fade — it reverses, and both halves clear p<0.002 in opposite
directions.** Nothing that behaves like this is a market mechanism. Per-day correlations at 4h say
the same: **+0.62, +0.46, +0.37, +0.18, +0.13, −0.14, −0.18** — five days one way, two the other,
with the two largest coefficients on 08-04 and 08-08.

**And the whole LONG gap lives in one small bucket that is itself concentrated in the early half:**

```
LONG "book leans AGAINST" bucket: n=54, mean 4h drift -0.434%
  by day: 08-02: 8 · 08-03: 14 · 08-04: 16 · 08-05: 3 · 08-06: 8 · 08-07: 4 · 08-08: 1
          -> 38 of 54 (70%) in the EARLY half
```

**The mechanism I believe is at work, stated as a hypothesis and not as a result:** SOL rose through
this window (73→77, +5%). In a rising tape, bid-heavy books and subsequent upward drift co-occur
because both are downstream of the same local momentum. That predicts exactly what is observed —
the effect on LONGs, its mirror image on SHORTs, and its disappearance when the second half of the
week traded differently. **It is not testable on 8 days and I am not going to pretend it is.**

---

## 3. VERDICT — 🔴 NOTHING SEPARATES. FILTER 22 IS REFUSED AND CLOSED.

**No hard gate is proposed. No X. No Y. Nothing is built.**

Stating the threshold the curve "indicates" would mean quoting a number from a correlation that
does not replicate across a four-day boundary inside its own sample. **That would be the exact
error the operator's own instruction forbids: reading a tail.**

```
FILTER 22 — "book liquidity as a hard entry gate (imbalance / depth / supporting structure)"
STATUS   : REFUSED 2026-08-09
COHORT   : 415 ai_skipped refusals, 8 days, forward drift 4h/12h/24h
FAMILY   : 27 tests, Bonferroni 0.001852, declared before any result
RESULT   : 4 of 27 pass Bonferroni under a within-day partial correlation.
           3 die under an hour control or on sign incoherence.
           The 4th (imbalance x LONG x 4h) dies on a time-split holdout,
           and REVERSES sign at 24h with both halves significant.
REVERSAL CONDITION, so this is falsifiable rather than permanent:
           RE-OPEN when the cohort spans >= 30 distinct DAYS covering at least
           one sustained down-trending week, and the imbalance effect holds the
           SAME SIGN in both halves of a time-split holdout on the LONG and the
           SHORT side. Signal count is NOT the criterion; days are.
```

🔴 **The honest conclusion, in full, because it is the useful half of this pass:**

**The book carries no tradeable signal on this instrument at this sample — and therefore the
advisor's false book claims have cost nothing in money.** Four entries were justified with a
statement about walls that was untrue, and because the walls do not separate outcomes, the untruth
did not change what the trades earned. That is now measured on three independent axes rather than
assumed: the wall band (2026-08-08, Fisher p=1.0000, n=396), the opposing wall as a veto (filter 21,
refused 2026-08-08), and now liquidity level and lean (filter 22, refused today).

**What it has cost is the operator's ability to trust the card**, and that is a real cost with a
cheap remedy — §4.

---

## 4. 🔴 APPLIED — THE BOOK FACTS NOW PRINT BESIDE THE REASON

### (a) Where, and what it renders

The card the operator actually reads the reason on is the **`🤖 AI ADVISOR — EXECUTE ✓`** card
(`main.py`, the `ai_decide == 'execute'` branch). The facts render **directly under the reason
line**, from `_pre_walls` — the same object passed to `consult_for_entry` a few lines above.

**Rendered against vpos 30's real stored snapshot — the fourth false claim:**

```
🤖 AI ADVISOR — EXECUTE ✓ (0.72) (LONG)
💎 SOL/USDT:USDT
🧠 claude-haiku-4-5-20251001
4H/1H/15m/5m all BULL, 1H ADX 53.2 (strong trend), 15m+5m LuxAlgo agree LONG. 1H rearm
SHORT is stale (5.4h). Market regime FLAT but confluence overcomes soft rule. No opposing
walls above entry. Execute.
📖 BOOK AT CONSULT — the same OKX snapshot the advisor was given
   mid $76.30 · imbalance ±1%: 0.50 (bid-heavy)
   🧱 OPPOSING (ask): 5 of 6 beyond mid — nearest $76.75 (p38, x6.3, +0.59%)
   🧱 SUPPORTING (bid): 7 of 7 beyond mid — nearest $76.25 (p64, x10.4, -0.07%)
```

**"No opposing walls above entry" now sits one line above "OPPOSING (ask): 5 of 6 beyond mid".**
The operator draws his own conclusion in about a second, and nothing in the code draws it for him.

**Every historical entry with a stored book, re-rendered — all four false claims become visible:**

| trades | reason's book claim | what the card would have shown |
|---|---|---|
| 16748/9 (06:50) | "No opposing wall at entry" | OPPOSING (ask) **2 of 3** beyond mid — nearest $75.25 **p69** ×11.5 +0.63% |
| 16765/6 (08:35) | "No opposing walls above entry" | OPPOSING (ask) **2 of 3** beyond mid — nearest $75.25 **p69** ×11.6 +0.55% |
| 16767 (08:50, vpos 29) | "No opposing walls above entry" | OPPOSING (ask) **3 of 4** beyond mid — nearest $75.25 **p64** ×10.6 +0.63% |
| 16857 (21:10, vpos 30) | "No opposing walls above entry" | OPPOSING (ask) **5 of 6** beyond mid — nearest $76.75 **p38** ×6.3 +0.59% |

The seven SHORT entries of 08-03…08-07 come out clean by contrast — each *named* its bid walls and
called them support, and the card agrees with them. **The failure is specific to the LONG "no
opposing walls" phrasing, in 4 of 4 cases.**

🔴 **A NEW FACT THIS PASS TURNED UP: the prompt truncates the wall list to FIVE per side.**
`claude_advisor._wall_list` does `wlist[:5]`. vpos 30's snapshot held **6 ask walls and 7 bid
walls**, so the model was **never shown** the $79.25 ask or the $73.75 / $73.25 bids. The card reads
the **full** snapshot, which is why it says "5 of 6" where my 15:40 report said four — four is
correct *as counted in the prompt*, five is correct *as counted in the book*. Both numbers are right
about different things, and the card is now the more complete of the two. Recorded, not changed:
altering the prompt is out of scope and the prompt has already been rewritten once for this.

### (b) 🔴 NO EDITORIALISING, NO AUTOMATIC CONTRADICTION FLAG — and why, in the code

Written into the function's own docstring so the next reader cannot undo it by accident:

```
🔴 FACTS ONLY — NO VERDICT, AND DELIBERATELY NO CONTRADICTION FLAG. An
automatic "the reason disagrees with the book" line would be a SECOND JUDGE ON
ONE FACT, which is the defect class this bot keeps closing (see
project_seam_class_one_fact_many_judges_27jul). The comparison is the
operator's; this function only renders what is in the snapshot.
```

Three design choices that follow from it:

1. **Percentiles come from `claude_advisor._wall_pctl`** — the *same* function that produced the
   prompt's `pN`. A second percentile scale would put two different numbers for one wall in front
   of the operator, which is the confusion this exists to end. Proven: the card renders vpos 30's
   supporting wall as **p64**, identical to its prompt.
2. **The anchor is the snapshot's own `mid`**, because that is the reference the prompt rendered
   and therefore what the model's "above entry" was about.
3. **Counts are printed as "N of M"**, never the beyond-count alone. A wall's price is its **$0.50
   bucket centre**, so a bucket straddling mid can sit up to $0.25 on the far side — the
   `M` makes any such exclusion visible instead of silent. (vpos 30's $76.25 ask is exactly this
   case: it is excluded from "beyond mid", and the "of 6" says so.)

**Degraded paths are visible, never omitted:**

```
walls = None      -> 📖 BOOK AT CONSULT: unavailable (OKX snapshot missing)
no mid            -> 📖 BOOK AT CONSULT: unavailable (no mid in snapshot)
no walls at all   -> 🧱 OPPOSING (ask): none in snapshot
unrankable mult   -> "pctl N/A"  (rendered exactly as the prompt does; never "ordinary")
```

### (c) IT CHANGES NOTHING THE BOT DECIDES — proven three ways

```
$ python3 -m py_compile main.py           SYNTAX OK

AST vs main.py.bak_bookfacts_card_20260809:
  added  : ['_book_facts_tg_block', '_line']      <- the new helper + its nested renderer
  removed: []
  changed: ['_handle_5m_trigger']

textual diff: 81 lines added, ZERO lines deleted
  inside _handle_5m_trigger, the ONLY change is:
    + 3 comment lines
    + f"{_book_facts_tg_block(_pre_walls, direction)}\n"    <- one line, inside a send_tg f-string
```

- **No gate, no score, no prompt.** The new function does no I/O, opens no DB, fetches nothing,
  raises nothing, and returns a string. It is called from exactly one place: inside a `send_tg(...)`
  argument.
- **`_pre_walls` cannot NameError there.** Its `try/except` assigns it on **both** branches at
  8-space indent (`main.py:4077-4082`), unconditionally, before the `if bypass_advisor:` split at
  4088 and before the card at 4116 — same straight-line block, same scope. Checked deliberately,
  because a NameError inside the entry card would break the entry path on a live-money bot.
- **`direction` is `'LONG'`/`'SHORT'`** at that point (`main.py:3592`: `position_side = direction`),
  which is the side mapping `_wall_shape` uses — so card, observatory and prompt all mean the same
  thing by "opposing".
- Backup `main.py.bak_bookfacts_card_20260809`, **md5-verified identical before the edit**
  (`357d539c…`).

### (d) 🔴 IT IS NOT LOADED. It renders from the next flat restart.

```
PENDING (loaded by the bot, disk newer than the 16:08:59 worker start) — now SIX
  config.py            2026-08-08 16:51:55
  virtual_trader.py    2026-08-08 16:51:55
  claude_advisor.py    2026-08-08 17:47:11
  skip_attribution.py  2026-08-08 17:47:11
  trail_arm.py         2026-08-08 17:47:11
  main.py              2026-08-09 16:19:32   <- NEW, this pass
```

**vpos 30 is open, so nothing was restarted.** The running worker is still the 16:08:59 process and
still renders the old card. Deployment gap named explicitly, per the standing rule: *a fix is not a
fix until a restart has loaded it.*

**What I did NOT touch, deliberately:** the SKIP card (`ai_decide == 'skip'`) carries a reason too,
and the same block would fit it. The brief specified the entry card and the 4-of-4 finding is about
entries; extending it is a separate decision and is left to you.

---

## STATE

```
mercury-sol   active · pid 3533821 / worker 3533987 · since 16:08:59 · NRestarts=0 · NOT restarted
vpos 30       🔴 IT ARMED WHILE THIS PASS RAN — size 1.3 -> 0.9 (0.4 partial realised),
              sl 75.41 -> 76.44258 (BE lock), water_mark 77.50, is_paper=0
              This is the exact level computed in the 15:40 report (76.29 x 1.0020 = 76.4426)
              and the exact arm price (76.29 + 2.5 x ATR = 77.1740, reached).
db            opened mode=ro for every query in §1-§3; zero writes
venue         NOT called in this pass at all
main.py       edited (card rendering only), py_compile OK, backup md5-verified, NOT loaded
titan         active · pid 2538048 · NRestarts=0 · HEAD 897850b · git clean · NOT TOUCHED
```

**Filter 22: refused, with a reversal condition stated in days rather than signals. The advisor's
book channel remains dead, its false claims remain free, and the operator can now see them.**
