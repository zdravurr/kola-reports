# which-exit-mechanism-works-the-map

_2026-08-09 18:15 UTC_

---

# Which exit mechanism actually works — the map. **The mechanisms cannot be ranked, because mechanism is confounded with ERA.** But two things came out clean, and one of them corrects the premise of the question.

**READ-ONLY on both bots. Nothing changed, nothing restarted, no writes and no git operations on
Titan beyond reading its database.**

🔴 **TWO CORRECTIONS TO THE PREMISE, BOTH FOUND BY CHECKING:**

1. **The +3.3729R figure does not reproduce anywhere in Titan's data.** Correctly signed — and the
   sign is fixed by the schema comment, not by my inference — the exit advisor's measured edge is
   **+0.4178R across 7 positions, beating the alternative 5 of 7.** Real, positive, and an order of
   magnitude smaller than the number the task was built on.
2. **Mercury-SOL's exit advisor has NEVER RUN. Not once.** It is wired, unconditional and reachable
   only through a 5m Group-B webhook arriving while a live exchange position is open — and SOL has
   recorded **zero `5m_group_b` rows in its entire history**. So SOL has three mechanisms, not four.

🔴 **THE CENTRAL FINDING — WHY NO RANKING IS POSSIBLE.** On Titan the exit advisor has only ever
operated in the LIVE era and the trail has only ever operated in the PAPER era. **They have never
once coexisted.** Comparing their R compares two eras, two notionals (median |net| $73 vs $0.73) and
two code versions — not two mechanisms.

**What IS answerable, and it is consistent across both books and both eras: the STOP is where the
money is lost, and it is the mechanism the alternative beats most often.** Titan: the shadow beat
the stop in **18 of 22**. SOL: **10 of 11**.

**And the first genuinely positive result in this project's audit history:** the EXIT advisor's
verdict is strongly coupled to measurable state — `giveback_r` ρ=+0.523, `upnl_r` ρ=−0.448, both
p<0.0001 — and **3 of 211 checkable numeric claims are false (1.4%)**, against the ENTRY advisor's
**4 of 4**. The same model writes both. One of them reads its prompt.

Prior: [16:25 — filter 22 refused](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1625-sol-book-liquidity-measured-filter-22-refused-facts-on-the-card.md) ·
[17:45 — the restart](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1745-sol-restarted-with-vpos-30-open-position-survived-intact.md)

---

## 0. 🔴 THE SIGN CONVENTION, SETTLED BEFORE ANY NUMBER

Everything in §2 depends on it, and it is easy to get backwards. From
`post_exit_observatory.py:155` — the **schema comment**, not a guess:

```
"exit_advantage_pct REAL, "     # shadow_pnl_pct - real_pnl_pct
```

**`advantage = shadow − real`. A POSITIVE stored `exit_advantage_r` means the SHADOW would have done
BETTER — i.e. the mechanism that actually fired was WORSE.**

Everything below is reported as **(real − shadow)**, flipped, so that **POSITIVE always means the
mechanism that fired BEAT the alternative.** Stated once here so no table needs re-reading.

### The +3.3729R claim, checked against every candidate

```
ai_exit cohort (n=7)          exit_advantage_r   sum -0.4178   pos 2  neg 5
                              exit_advantage_pct sum -0.6888   pos 2  neg 5
                              shadow_pnl_r       sum -1.4206
                              real_pnl_r         sum -1.0028
                              max_favorable_post_exit_pct  sum +4.3634   <- closest positive
first FIVE ai_exit only (n=5) exit_advantage_r   sum -0.1766   pos 1  neg 4
whole book (n=47)             exit_advantage_r   sum +1.5887   pos 30 neg 17
```

**Nothing reaches +3.3729R, and no cell shows "improved 4, worsened 1".** Flipped to the (real −
shadow) convention, the advisor's actual record is **+0.4178R over 7, beating the shadow 5 of 7.**
That is a real positive result. It is not the one the task was premised on, and the difference
matters because +3.37R over 5 would be decision-grade and +0.42R over 7 is not.

🔶 Note also that the book-wide `+1.5887` reads, under the correct sign, as **the shadow beating our
real exits by 1.59R across 47 positions** — the opposite of how a positive number there invites you
to read it.

---

## 1. WHO ACTUALLY CLOSES POSITIONS

### (b) The boundaries — what I pooled and what I refused to pool

| boundary | decision |
|---|---|
| **Titan PAPER vs LIVE** (`stop_order_id`, first set at vpos 86, 2026-07-30) | 🔴 **REFUSED to pool.** Median \|net_pnl\| **$73.09 paper vs $0.73 live** — a ~100× notional change. R normalises risk so R *is* comparable; **net_pnl is not**, and every dollar figure is reported per era only. |
| **Titan 1R boundary 2026-08-04 17:01:29** | 🔴 **REFUSED to pool** — and it costs nothing to refuse, because **only ONE position (vpos 93) closed after it.** The post-boundary R cohort is n=1 and no conclusion rests on it. |
| **SOL paper vs live** (`is_paper`) | 🔴 **REFUSED to pool.** Live era is **n=1**. |
| **SOL taker-fee boundary vpos 29/30** | Not reached — only vpos 29 has closed live, and it sits on the pre-fix side. |
| **SOL ADX-window boundary vpos 28/29** | Not load-bearing here; no entry-side quantity is used in this analysis. |
| **SOL funding boundary (opened today)** | Recorded: every closed row has `funding_source` NULL, so **no closed position in either book has funding in its net_pnl**. Both books' R is therefore uniformly funding-blind, which makes them internally comparable and slightly optimistic in absolute terms. |

### (a)/(c) The census, per bot, per era

🔴 **TITAN — mechanism is almost perfectly confounded with era:**

```
close_reason            PAPER   LIVE          realised R
                                        PAPER                            LIVE
sl                        27      1     n=27 sumR=-18.732 mean-0.694   n=1  -1.022
trail                     15      0     n=14 sumR=+16.290 mean+1.164   —
external                  10      0     n=10 sumR= +1.011 mean+0.101   —
post_entry_critical        1      0     n=1  sumR= +0.015              —
ai_exit                    0      7     —                              n=7 sumR=-1.003 mean-0.143
```

**The trail has zero live closes. The advisor has zero paper closes.** That single fact governs the
whole question.

**SOL:**

```
close_reason            PAPER   LIVE          realised R
sl                        11      0     n=11 sumR=-10.345 mean-0.940 med-1.064
exit_signal                7      0     n=7  sumR= +1.952 mean+0.279 med-0.153
trail                      4      0     n=4  sumR= +3.019 mean+0.755 med+0.771
exchange_UNKNOWN           0      1     n=1  sumR= +1.355          <- vpos 29
```

**SOL's single live close is mislabelled and I am not going to let the label stand in a census.**
`exchange_UNKNOWN` was a 15m **exit signal** — the bot closed itself with a reduce-only market
order and its own detector then asked the venue why. Counted as what it was, SOL's exit-signal
cohort is 8, not 7.

### (d) 🔴 ARE TITAN'S LABELS TRUSTWORTHY? Yes — and here is the test rather than the assumption

The worry was Titan carrying SOL's defect: a trail pooled into `sl`, or an unmapped reason.

**It does not, and the data proves it rather than the code claiming it.** `trail` exists as its own
label on 15 rows with **mean R +1.164**, while `sl` sits at **−0.694** on 27. Had the two been
pooled, that separation could not appear — a pooled cohort cannot show both signs. The five labels
are distinct and each has a coherent R signature.

🔶 **One label does need naming: `external` (10 rows, all paper).** It is Titan's equivalent of
SOL's `exchange_*` bucket — "the position went away and we did not initiate it". Its mean R of
+0.101 sits between the trail and the stop, which is what a *mixture* looks like. **I would not
build anything on the `external` cohort**; it is a bucket, not a mechanism.

---

## 2. THE COUNTERFACTUAL — every mechanism against the shadow

The observatory already runs the head-to-head this section asks for: each closed position carries a
**shadow exit** — what a 15m-signal / 1h-reversal / stop alternative would have produced — priced on
the real path. Shadow reasons used: Titan `15m_signal` 34, `1h_reversal` 10, `sl_hit` 3; SOL
`15m_signal` 19, `1h_reversal` 4. **§2(c) is therefore answered by construction: the exit-signal
counterfactual is the shadow, and it is the dominant one.**

### (e) The ranking, per bot per era — **(real − shadow), positive = the mechanism WON**

**TITAN, PAPER era (n=39):**

| mechanism | n | sum (real−shadow) | mean | beat the shadow |
|---|---|---|---|---|
| **trail** | 10 | **+4.827** | +0.483 | **6/10** |
| external | 6 | +0.811 | +0.135 | 2/6 |
| post_entry_critical | 1 | −0.030 | — | 0/1 |
| 🔴 **sl** | 22 | **−7.136** | −0.324 | **4/22** |
| **ALL** | 39 | −1.528 | −0.039 | 12/39 |

**TITAN, LIVE era (n=8):**

| mechanism | n | sum (real−shadow) | mean | beat the shadow |
|---|---|---|---|---|
| **ai_exit** | 7 | **+0.418** | +0.060 | **5/7** |
| sl | 1 | −0.479 | — | 0/1 |

**SOL, PAPER era (n=22):**

| mechanism | n | sum (real−shadow) | mean | beat the shadow |
|---|---|---|---|---|
| **trail** | 4 | **+2.109** | +0.527 | **4/4** |
| exit_signal | 7 | +1.870 | +0.267 | 3/7 |
| 🔴 **sl** | 11 | **−7.618** | −0.693 | **1/11** |
| **ALL** | 22 | −3.639 | −0.165 | 8/22 |

**SOL, LIVE era: n=1** (`exchange_UNKNOWN`, −0.074). 🔴 **One position. Not ranked, not discussed.**

### (a)/(b) The trail and stop replay, from the stored fields

Computed only on positions whose recorded water mark actually **armed** the trail (+1R from entry) —
replaying a trail that never armed would be inventing an exit:

```
TITAN PAPER  armed 17 of 53   TRAIL cf  +18.034 (mean +1.061)   STOP cf -17.000   ACTUAL +17.000
TITAN LIVE   armed  1 of  8   TRAIL cf   +0.716                 STOP cf  -1.000   ACTUAL  +1.386
SOL   PAPER  armed  7 of 22   TRAIL cf   +6.472 (mean +0.925)   STOP cf  -7.000   ACTUAL  +6.245
SOL   LIVE   armed  1 of  1   TRAIL cf   +1.060                 STOP cf  -1.000   ACTUAL  +1.355
```

**Two things fall out.** The trail counterfactual tracks the realised result closely in both books
(+18.03 vs +17.00; +6.47 vs +6.25) — unsurprising, since many of those positions *did* close on the
trail, and it confirms the replay is not producing nonsense. And **the stop counterfactual is −1R by
construction in every cell**: on any position that reached +1R, letting the stop take it instead
would have cost roughly 2R against the trail. That is the clearest single number in this report.

### (d) The HOLD branches — what holding actually produced

Titan, 11 positions where the advisor said HOLD at least once (60 hold verdicts in total):

```
eventually closed by       n    sumR      meanR
  trail                     1   +1.039    +1.039
  external                  1   +0.122    +0.122
  ai_exit                   6   -0.866    -0.144
  🔴 sl                     3   -3.198    -1.066
  ALL held positions       11   -2.903    -0.264
```

**Holding is not free, and the cost is concentrated in exactly one place: the three positions where
holding ran into the stop cost −1.066R each.** vpos 83 is the extreme — **14 HOLD verdicts and 34
CLOSE verdicts** on one position that ended at −1.090R. The advisor said close 34 times, was in
DRYRUN, and the stop took it anyway.

### (f) 🔴 n PER CELL, STATED BEFORE THE CONCLUSION

```
Titan LIVE  ai_exit  n=7        Titan LIVE  sl  n=1        Titan LIVE trail n=0
Titan PAPER trail    n=10-14    Titan PAPER sl  n=22-27    Titan PAPER external n=6-10
SOL   PAPER trail    n=4        SOL   PAPER sl  n=11       SOL PAPER exit_signal n=7
SOL   LIVE  anything n=1        Titan post-1R-boundary     n=1
SOL   exit advisor   n=0        SOL   5m_group_b webhooks  n=0 (ever)
```

**Six of those cells hold two positions or fewer. No ranking is built on any of them.**

---

## 3. WHAT THE EXIT ADVISOR READS — and here the answer is genuinely different

### (a) 🔴 THE EXIT ADVISOR IS NOT NARRATION. Its verdict tracks the position's own state.

Titan, **n=119 consults** (60 HOLD / 59 CLOSE), every field parsed from the stored prompts.
Family of 5 quantities declared up front → Bonferroni α = 0.05/5 = 0.0100.

| quantity | ρ vs CLOSE | p | regime-blocked p | |
|---|---|---|---|---|
| **giveback_r** | **+0.5232** | <0.0001 | <0.0001 | ✅ **strongest** |
| **upnl_r** | **−0.4476** | <0.0001 | <0.0001 | ✅ |
| **stop_away_r** | −0.4339 | <0.0001 | 0.0001 | ✅ |
| **elapsed (h)** | +0.3160 | 0.0002 | 0.0006 | ✅ |
| mfe_r | +0.1633 | 0.0756 | 0.0774 | ✗ dies |

**Every sign is the one a competent exit rule would have**: closing more as unrealised R falls, as
giveback from the peak grows, as the stop gets nearer, and as the position ages. The brief's
r = −0.398 on upnl_r across 118 is now **−0.4476 across 119** — it held and strengthened.

🔴 **BUT THE REGIME CONTROL IS DEGENERATE AND MUST NOT BE CITED AS A SURVIVAL TEST.**

```
regime distribution across the 119 consults:  TREND 118,  None 1
```

**118 of 119 consults carry the same regime label.** Blocking on a variable with one value cannot
break any association — the "regime-blocked" p is arithmetically almost the same test as the
unblocked one. Saying this survived a regime control **overstates what was done**. The correlations
are real and strong; the control behind them is empty, and a genuine control needs a regime variable
that actually varies.

### (b) 🔴 3 OF 211 CHECKABLE CLAIMS FALSE — against the entry advisor's 4 OF 4

Every numeric claim in every exit reason (percentiles, ADX values), checked against that consult's
own prompt:

```
checkable numeric claims found : 211
NOT matching the prompt        :   3   (1.4%)

  row 19102  claimed ADX 39.8  ; prompt carried 26.3 / 29.8 / 33.9
  row 20073  claimed "93 pct"  ; prompt carried 20 / 34 / 80 / 82
  row 20097  claimed "93 pct"  ; prompt carried 24 / 30 / 48 / 79
```

**This is the single sharpest contrast in the whole audit series.** The same model
(`claude-haiku-4-5`) writes both prompts' reasons. On the **entry** side, 4 of 4 checkable book
claims were false and the verdict was statistically independent of the book (Fisher p=1.0000). On
the **exit** side, 98.6% of checkable claims are true and the verdict is strongly coupled to the
state it is shown.

🔶 **The difference is not the model — it is the prompt.** The exit prompt hands it *the position's
own numbers* (R, giveback, elapsed, stop distance) which are unambiguous and self-consistent. The
entry prompt hands it a ten-wall order book and asks for a judgement about "opposing walls", which
is where all four failures occurred. **That is a hypothesis this report does not test**, but it is
the obvious one and it is worth recording as such.

The two `"93 pct"` claims are worth a flag on their own: 93 is a plausible-sounding percentile that
appears in *some* prompts and was asserted in two where the book carried nothing near it.

### (c) The prompt DOES state duration, trail and stop — and the trail claim is now TRUE

```
Elapsed        119/119        MFE            119/119
Current stop   119/119        Giveback       119/119
trail clause    59/119        <- added 2026-07-29 13:30 (row 19460); silent on the earlier 60
```

**Of the 59 prompts that make a trail claim, 59 are consistent** with the position's own MFE
(armed ⟺ MFE ≥ +1R). And the arithmetic behind the claim holds too:

```
arm level is +1R in the TRADE'S OWN direction : 58/58 correct, 0 wrong
"+N R away" matches |stop − now| / 1R          : 58/58 match,  0 mismatched
```

🔶 **Honest limit on this check.** The brief records the trail claim as false on 96.6% of consults
until 2026-08-05. My test is of the **armed/not-armed** claim and of the **arm level and stop
distance** — all three now clean. I did **not** reproduce a 96.6% failure rate, and the clause does
not exist at all before 2026-07-29, so whatever that figure measured is either a different aspect of
the claim or a population I cannot reconstruct from the stored prompts. **I am reporting what I
tested, not confirming a number I could not find.**

**And SOL: there is no exit prompt to check.** `consult_for_close` exists at
`claude_advisor.py:1135`, is called unconditionally at `main.py:4926`, and has produced **zero
consults ever**. Its only caller is `_handle_5m_close`, which needs a **5m Group-B webhook** while an
exchange position is open — and SOL has logged **0 `5m_group_b` rows in its entire history**. The
mechanism is present in the code, correct-looking, and has never once executed. **§3 for SOL is not
"unmeasured"; it is "has never happened".**

---

## 4. VERDICT — framed as a decision

### 🔴 THE MECHANISMS CANNOT BE RANKED ON THIS BOOK. That is the answer, and it is a real one.

**Not because the data is noisy — because of how it is structured.** Mechanism is confounded with
era to the point of near-perfect separation:

```
the TRAIL   has 15 paper closes and  0 live closes
the ADVISOR has  0 paper closes and  7 live closes
```

They have never coexisted. Any table putting the trail's +1.164 mean R beside the advisor's −0.143
is comparing 2026-05→07 paper at ~$10k notional against 2026-07→08 live at ~$100 — different
notional, different code, different market. **The number would look like a ranking and would be an
era comparison.** SOL cannot break the tie either: its live era is n=1 and its exit advisor has
never run.

### What IS established, and holds across both books and both eras

🔴 **THE STOP IS THE WORST OUTCOME, MEASURED THREE INDEPENDENT WAYS:**

```
realised R          Titan paper sl  n=27  mean -0.694      SOL paper sl  n=11  mean -0.940
vs the shadow       Titan       sl  n=22  BEATEN 18 of 22  SOL       sl  n=11  BEATEN 10 of 11
holding into it     Titan HOLD -> sl n=3  mean -1.066
```

This is the one conclusion with n on its side (33 stop closes across both books), consistent
direction, and agreement between the realised and counterfactual views. **The stop is doing its job
as a backstop — it is not a mechanism that competes, and any future work should treat "how often do
we reach the stop" as the thing to reduce, not "which exit is best".**

### The exit advisor: the first mechanism whose reasoning survives inspection — and still not proven

**What is proven:** its verdict is strongly coupled to `giveback_r`, `upnl_r`, `stop_away_r` and
`elapsed`, all at p<0.0001; 98.6% of its checkable claims are true; its prompt states the trail and
stop correctly. **After twenty-two dead entry filters and an entry advisor whose reasons are
narration, this is the first thing in the project that reads its inputs.**

**What is NOT proven:** that it makes money. Its edge over the shadow is **+0.4178R across 7
positions**, its realised R is **−0.143 mean across 7**, and its regime control is degenerate.
**n=7 is not a decision.**

### What n would be needed

Measured from Titan's own realised-R distribution (mean −0.057, **SD 0.900** across 60 closes), at
80% power and α=0.05:

| difference to detect | n per arm | total |
|---|---|---|
| 1.00 R | 13 | 25 |
| 0.75 R | 23 | 45 |
| **0.50 R** | **51** | **102** |
| 0.25 R | 203 | 407 |

**Titan closes 0.79 positions/day.** A clean 0.50R separation between two mechanisms needs ~102
closes in a single era — about **130 days** of Titan at current rate, and far longer on SOL, which
has **1 live close to date**. A 0.25R separation needs ~407 closes: **over 1.2 years.**

🔴 **So: "not answerable at this book size" is the honest verdict, and the shortest credible path is
not more data on four mechanisms — it is running the trail and the advisor IN THE SAME ERA so that
n accumulates on a comparison instead of on two disjoint histories.**

**No change is proposed. The map first, as with every audit this week.**

---

## STATE — nothing was touched

```
Every query on both books used mode=ro. No writes, no restart, no order, no git operation on Titan.
mercury-sol   active · master 4037477 / worker 4037550 · since 17:42:38 · vpos 30 OPEN, untouched
titan         active · pid 2538048 · NRestarts=0 · HEAD 897850b · NOT TOUCHED
```

**Open questions this pass deliberately did not answer:** why SOL has never received a 5m Group-B
webhook (a TradingView alert-configuration question, not a code one); whether the entry/exit
asymmetry in claim accuracy is caused by prompt shape, which would be testable by giving the entry
advisor an equally unambiguous input; and what the 96.6% trail-claim failure figure originally
measured, which I could not reconstruct.
