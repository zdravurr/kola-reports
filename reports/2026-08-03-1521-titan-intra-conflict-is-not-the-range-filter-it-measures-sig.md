# titan intra-conflict is not the range filter, it measures signal agreement

_2026-08-03 15:21 UTC_

---

# TITAN — DOES INTRA-CONFLICT CATCH THE RANGE ENTRIES? **NO.** READ-ONLY.

_2026-08-03 15:35 UTC · HEAD `489e0ac` · LIVE, flat · **nothing changed, nothing proposed**_

---

## DECISION LINE

**The hypothesis is not supported, and it fails on its own terms twice.**

1. **§2 — conflict is NOT associated with a ranging tape.** Across four independent cuts (efficiency
   ratio at 4h and 12h, each split at the sample median and at a fixed 0.5), **the association is
   never significant, and the SIGN FLIPS between windows**: at 4h conflict is more common in ranges
   (65.6% vs 54.5%), at 12h it is more common in **trends** (66.7% vs 53.1%). Largest χ²(1df) =
   **1.24** against a 3.84 threshold. **Conflict is spread evenly across both tape states.**
2. **§1 — it misses the most range-like of the three flagged trades.** **vpos 86 has ZERO
   intra-conflicts.** The rule would **not** have blocked it — and vpos 86 is the one with
   ADX(1h) **11.12**, the lowest of the three by a wide margin. The rule catches vpos 87 and 91 and
   misses 86.

**So: it catches something else that correlates with losing.** And this pass can say what that
something is, more precisely than "not range":

> **It measures agreement among the bot's own signals — a property of the SIGNAL SET, not of the
> market.** It is not a signal-count proxy either: it separates *within* both signal-count buckets
> (few signals: **+0.545 vs −0.654**; many signals: **+0.513 vs −0.163**), and the two no-conflict
> cells land at nearly the same place regardless of how many signals fired.

🔴 **And the cost is much larger than my last report implied. The operator's correction was right and
my figure was wrong.** The bot enters **0.83 per calendar day / 1.67 per active day**, with **5 in a
single day** at peak and **18 days carrying 2+**. My "one entry per 2.6 days" came from a 3-day
window and should not have been stated. Under "refuse if any category is intra-conflicted":
**60% of all entries refused**, **67%** over the last 30 days, **83%** in the live era.

**§5 is the sharpest number here: all 5 live-era clean trades were conflicted.** The rule blocks
every one, including the only live winner (**vpos 89, +1.386R**), to avoid a set whose total is
**−0.138R**.

---

## §1 — THE THREE FLAGGED ENTRIES, PER TRADE

### vpos 86 — SHORT @ 63,686.0 · 2026-07-30 00:50 · **−1.022R**

| category | L | S | sig | state |
|---|---|---|---|---|
| TREND | 0.0 | 2.25 | 1 | SHORT +2.25 |
| MOMENTUM | 0.0 | 1.75 | 1 | SHORT +1.75 |
| LIQUIDITY | 2.5 | 0.0 | 1 | 🚫 **inter**-zeroed (minority direction) |
| EXECUTION | 0.0 | 1.75 | 1 | SHORT +1.75 |

raw **5.75** · macro 0.0 · gated **5.75** · regime TREND · bar 3.0 · **ADX(1h) 11.12**

🔴 **intra-conflicted categories: NONE. The rule would have TAKEN this trade.**

Every category held exactly **one** signal, so none *could* conflict. The one dissent — LIQUIDITY
pointing LONG against a SHORT — was silenced by the **inter**-category minority rule, a different
mechanism the proposed filter does not touch. This entry scored **5.75**, one of the highest in the
book, from three agreeing categories, at the lowest ADX of the three. It lost 1.02R.

### vpos 87 — LONG @ 64,838.7 · 2026-07-30 12:05 · **−0.440R**

| category | L | S | sig | state |
|---|---|---|---|---|
| TREND | 2.5 | 0.0 | 2 | LONG +2.5 |
| MOMENTUM | 1.75 | 2.5 | 2 | ⚠️ **INTRA-CONFLICT** |
| LIQUIDITY | 2.5 | 1.25 | 3 | ⚠️ **INTRA-CONFLICT** |
| EXECUTION | 1.75 | 0.0 | 1 | LONG +1.75 |

raw 4.25 · gated 4.25 · regime TREND · bar 3.0 · ADX(1h) 13.52 · **2 conflicted → BLOCKED**

### vpos 91 — SHORT @ 62,649.2 · 2026-08-03 06:40 · **−0.484R**

| category | L | S | sig | state |
|---|---|---|---|---|
| TREND | 0.0 | 2.5 | 2 | SHORT +2.5 |
| MOMENTUM | 2.5 | 1.75 | 3 | ⚠️ **INTRA-CONFLICT** |
| LIQUIDITY | 2.5 | 2.5 | 3 | ⚠️ **INTRA-CONFLICT** |
| EXECUTION | 2.5 | 2.5 | 4 | ⚠️ **INTRA-CONFLICT** |

raw 2.5 · macro +1.0 · gated 3.5 · regime TREND · bar 3.0 · ADX(1h) 18.58 · **3 conflicted → BLOCKED**

**Score: the rule blocks 2 of the 3 the operator flagged, and the one it misses is the one that looks
most like a range by the conventional measure.**

---

## §2 — THE CROSS-TABULATION. THE HYPOTHESIS FAILS HERE.

**Definition, and why this one:** efficiency ratio **ER = |net move| ÷ (high−low range)** over the
prior N hours. ER→1.0 means price travelled in a straight line (**directional**); ER→0 means it
ended where it started having covered the range (**oscillating = range**). It is scale-free, needs no
calibration, and is the standard Kaufman construction. Reported at **4h and 12h**, each split at the
**sample median** and at a **fixed 0.5**, so the answer cannot rest on one arbitrary cut.

**n = 65.** Outcomes are not involved in an association test, so the §0 outcome filters do not apply
and the **full entry book** is used — deliberately, for the extra n.

| cut | | tape RANGING | tape TRENDING | conflict rate | χ²(1df) |
|---|---|---:|---:|---|---:|
| **4h, median 0.517** | conflicted | 21 | 18 | **65.6% vs 54.5%** | **0.831** |
| | no conflict | 11 | 15 | | |
| **4h, fixed 0.5** | conflicted | 20 | 19 | 66.7% vs 54.3% | 1.032 |
| | no conflict | 10 | 16 | | |
| **12h, median 0.565** | conflicted | 17 | 22 | **53.1% vs 66.7%** 🔴 *reversed* | 1.241 |
| | no conflict | 15 | 11 | | |
| **12h, fixed 0.5** | conflicted | 13 | 26 | 54.2% vs 63.4% 🔴 *reversed* | 0.539 |
| | no conflict | 11 | 15 | | |

Second axis — 24h range **width** in ATR(1h) units (median 5.22 ATR): conflict rate **narrow 53.1%**
(n=32) vs **wide 66.7%** (n=33). If anything conflict is slightly *more* common when the range is
wide, which is the opposite of "quiet chop".

🔴 **Not one cut reaches significance, and the direction reverses between the 4h and 12h windows.**
Per the operator's own framing: *"If conflict is spread evenly across both, it separates outcomes for
some OTHER reason and calling it a range filter would be a story we told ourselves."* **It is spread
evenly. It would be a story.**

---

## §3 — WHAT IT WOULD ACTUALLY COST IN ENTRY RATE

🔴 **My "one per 2.6 days" in the 14:37 report was wrong.** It was taken from a 3-day window and I
should not have generalised from it. The measured rate:

| window | span | entries | per calendar-day | per active-day | max in a day | days with 2+ |
|---|---|---:|---:|---:|---:|---:|
| **whole book** | 2026-05-17 → 08-03, 78 days (39 with an entry) | **65** | **0.83** | **1.67** | **5** | 18 |
| **last 30 days** | 2026-07-04 → 08-03, 31 days (18 with an entry) | 27 | 0.87 | 1.50 | 3 | 8 |
| **live era** | 2026-07-30 → 08-03, 4 days (3 with an entry) | 6 | 1.50 | 2.00 | 3 | 2 |

**The operator is right: the bot enters most days, sometimes several times.**

### Under "refuse if ANY category is intra-conflicted"

| window | entries kept | per calendar-day | **refused** |
|---|---:|---:|---:|
| whole book | **26 of 65** | 0.83 → **0.33** | **60%** |
| last 30 days | **9 of 27** | 0.87 → **0.29** | **67%** |
| live era | **1 of 6** | 1.50 → **0.25** | **83%** |

*"/calendar-day" counts every day in the window including downtime; "/active-day" counts only days
that had an entry.*

---

## §4 — WHICH CATEGORY CARRIES IT? **NONE OF THEM. THE COUNT DOES.**

Clean cohort n=39. No conflict anywhere: **n=14, 85.7% win, +0.536R**.

| conflicted category (cells overlap) | n | win | mean R | med R |
|---|---:|---:|---:|---:|
| MOMENTUM (with or without others) | 13 | 38.5% | −0.250 | −0.304 |
| LIQUIDITY | 11 | 36.4% | −0.179 | −0.440 |
| EXECUTION | 17 | 41.2% | −0.107 | −0.296 |

| isolated — that one and no other | n | win | mean R |
|---|---:|---:|---:|
| MOMENTUM alone | 3 | 33.3% | −0.693 |
| LIQUIDITY alone | 2 | 0.0% | −1.103 |
| EXECUTION alone | 6 | 33.3% | −0.125 |

**A single-category rule captures far less than the "any" rule:**

```
refuse on MOMENTUM  -> keeps n=26  meanR +0.181  sumR +4.70 | blocks n=13 sumR -3.24
refuse on LIQUIDITY -> keeps n=28  meanR +0.122  sumR +3.43 | blocks n=11 sumR -1.97
refuse on EXECUTION -> keeps n=22  meanR +0.149  sumR +3.27 | blocks n=17 sumR -1.81
refuse on ANY       -> keeps n=14  meanR +0.536  sumR +7.50 | blocks n=25 sumR -6.04
```

🔴 **The three categories are interchangeable within noise (−0.11 to −0.25R).** No single one carries
the separation — **the strength comes from requiring ALL FOUR to be clean**, which is precisely why
it refuses 60% of entries. **The smaller intervention the question hoped for does not exist in this
data:** the best single-category rule keeps +0.181R against the "any" rule's +0.536R.

---

## §5 — THE LIVE-ERA TAIL. A TAIL, NOT EVIDENCE.

| vpos | side | opened | R | conflicts | rule |
|---|---|---|---:|---|---|
| 87 | LONG | 07-30 12:05 | −0.440 | MOMENTUM, LIQUIDITY | **BLOCK** |
| 88 | SHORT | 07-31 09:35 | −0.296 | EXECUTION | **BLOCK** |
| 89 | SHORT | 07-31 12:20 | **+1.386** | EXECUTION | **BLOCK** |
| 90 | SHORT | 07-31 14:25 | −0.304 | MOMENTUM, EXECUTION | **BLOCK** |
| 91 | SHORT | 08-03 06:40 | −0.484 | MOMENTUM, LIQUIDITY, EXECUTION | **BLOCK** |

🔴 **5 of 5 conflicted. The no-conflict cell is EMPTY in the live era.** The rule blocks the entire
live book — including the only winner — to avoid a set totalling **−0.138R**.

**Stated as a tail:** n=5 is not evidence of anything, and the +0.536R no-conflict cell that motivates
the whole idea has **zero live representation**. Every trade supporting the rule is a paper trade.

---

## §6 — HONEST VERDICT

**Intra-conflict does NOT catch what the operator sees as range entries.**

**What the data can settle:**

- **The range interpretation is rejected**, not merely unproven. §2 tested it four ways on n=65 and
  found no association, with the sign reversing between the 4h and 12h windows. §1 found it misses
  vpos 86 — the flagged trade with ADX 11.12, the most range-like of the three.
- **It is not a signal-count proxy either.** A category can only conflict if it holds ≥2 opposing
  signals, so "no conflict" might just mean "quiet tape". It does not: conflicted entries carry 7.18
  signals on average against 4.35, **but conflict still separates within both buckets** —

  ```
  few signals  : no conflict n=10 +0.545R (80% win) | conflicted n=4  -0.654R (0% win)
  many signals : no conflict n=4  +0.513R (100%)    | conflicted n=21 -0.163R (43%)
  ```

  The two no-conflict cells land at **+0.545 and +0.513** regardless of how many signals fired.
  Agreement matters; quantity does not.

**What it therefore is:** a measure of **whether the bot's own signal generators agree with each
other** — a property of the **signal set**, not of the market. That is why it does not track any
price-derived range measure: it is not measuring price. It may be reading the consistency of the
LuxAlgo feed rather than any market state at all.

**What the data CANNOT settle,** and I am saying so rather than filling it in: whether signal
disagreement is *causally* connected to the loss, or is a marker of some third condition that
produces both. Nothing here separates those. The book has 39 clean outcomes, 34 of them paper, and
the live cell that would test it is empty.

**The one framing I would push back on:** "the filter we already found is the range filter, and it
just has the wrong name" — it is not the wrong name, it is a **different quantity**. Naming it a range
filter would attach a market interpretation to a measurement that has now been tested against the
market four ways and failed to correlate. The measurement is real; the interpretation is not
supported.

**Nothing is proposed. Nothing was changed.** The trade-off the numbers put in front of the operator
is: a cell worth **+0.536R on n=14 (all paper)**, bought at the cost of **60% of all entries, 67% of
the last 30 days, and 83% of the live era including its only winner** — with the mechanism unexplained
and the range explanation ruled out.
