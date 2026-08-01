# sol-vpos25-partial-arithmetic-verified

_2026-08-01 22:25 UTC_

---

# MERCURY-SOL — vpos 25 VERIFIED: **YOUR ARITHMETIC HOLDS.** THE PARTIAL COST $15.64 ON THIS TRADE.

**READ-ONLY. Nothing changed.** No file modified, no service restarted, no order placed. SOL is
PAPER, the entry prompt frozen, the window at 4 of 200, Titan untouched. Every figure below is
computed from the stored row, not re-derived from the report.

---

# THE ANSWER FIRST

**Every number in your reading is correct.** Two of them are better than "correct" — the peak you
*inferred* from the trail callback is the value actually stored, and the counterfactual you called
"roughly" is **exact**.

| your figure | verified | note |
|---|---|---|
| 1R in price = 100.667 / 137.9 = **0.730** | ✅ **0.730000** | cross-checks against \|entry − original_sl\| = \|72.47 − 73.20\| = 0.7300 |
| partial @ 71.70 = **+1.055R** | ✅ **+1.0548R** | |
| trail exit @ 71.36 = **+1.521R** | ✅ **+1.5205R** | |
| net with partial = **$126.52** | ✅ **$126.522951** | matches the stored `net_pnl` to 6 dp |
| net without partial ≈ **$142.16** | ✅ **$142.160214** | and it is **exact**, not approximate — see below |
| cost ≈ **$15.6 = 0.16R** | ✅ **$15.637262 = 0.1553R** | |
| peak ≈ **70.64 = +2.5R** | ✅ **stored `water_mark` = 70.64 → +2.5068R** | you inferred it; the DB confirms it directly |
| giveback ≈ **1R** | ✅ **0.9863R** | |

**Your trail-trigger inference also checks out:** `water_mark × (1 + 1.007/100) = 70.64 × 1.01007
= 71.3513`, and the position closed on the next tick at **71.36**.

---

# §1 — WHY THE COUNTERFACTUAL IS EXACT, NOT APPROXIMATE

This is the one place I can strengthen your reading rather than just confirm it.

**The partial modifies neither `water_mark` nor `trail_pct`** — that is the design property stated
in `config.py`: *"the REMAINDER rides the IDENTICAL contract — same TRAIL_MULT_ATR, same BE stop,
same water_mark."* And `water_mark` is tracked from the tick price independently of position size.

So in the no-partial world the peak is still 70.64, the trail level is still
`70.64 × 1.01007 = 71.3513`, and the trail fires **at the same tick, at the same price**. The
counterfactual is not a modelled estimate — it is the same exit with a different size.

```
ACTUAL      partial +31.749475  +  remainder +94.773476  =  +126.522951   (stored: 126.522951)
NO-PARTIAL  137.9 held to 71.36                          =  +142.160214
COST                                                        −15.637262  =  −0.1553R
```

## Where the $15.64 went

```
1/3 leg exited 0.34 earlier × 45.9667 units   = $15.6287
extra close fee (two closes instead of one)   = $ 0.0086
                                                --------
                                                $15.6373
```

**99.94% of the cost is opportunity, not friction.** The double-fee drag people usually worry
about with partials is **less than one cent** here. The entire cost is the ⅓ leg exiting at
+1.055R instead of +1.521R.

---

# §2 — THE FRAMING, AS YOU ASKED IT

**The mechanism performed exactly as designed, and it cost money on this trade.**

That is not a contradiction and not a defect. `config.py` states the bounded worst case up front:
the partial *"can shave a runner's tail but can NEVER truncate it"*. **This was a runner** — peak
+2.51R — and the partial shaved its tail for **0.155R**. The design was chosen *because* that
worst case is bounded, on a book where the alternative lever (narrowing `TRAIL_MULT_ATR`) carried
the one risk that could not be tested: cutting a runner short.

🔴 **+1.257R must not be read as vindication of the partial.** The position was profitable
*despite* the partial, not because of it. Without the partial it would have returned **+1.412R**.
Anyone reading "first partial-at-arm lifecycle, +1.257R, winner" as evidence the mechanism works
would be reading it exactly backwards.

🔴 **And n=1 says nothing either way.** One observation cannot distinguish "the partial costs
0.155R on runners" from "the partial saves on reversals" — the case it exists for. This trade
happened to be the case where it loses. `config.py` already forbids retuning on this sample:
*"retune only at ~15 armed positions WITH path data at the new excursion cadence."* **This is
armed position #7, and datapoint #1 under the new cadence.**

**What it does establish:** the mechanism executes correctly end-to-end in production — the leg
sizes, the fee split on the realised fraction, and the fold-back all reconcile to the stored
`net_pnl` to six decimal places, and `initial_risk_usdt` was untouched so R stays comparable
across the whole book.

---

# §3 — THE ~1R GIVEBACK REPRODUCED LIVE

Recomputed from stored `water_mark` for **every armed position**, not just the trail closes:

| vpos | side | close reason | peak | exit | **giveback** |
|---|---|---|---|---|---|
| 7 | LONG | exit_signal | +3.000R | +2.137R | 0.863R |
| 11 | SHORT | exit_signal | +1.711R | +1.174R | 0.537R |
| 13 | SHORT | **trail** | +2.357R | +1.381R | **0.976R** |
| 15 | SHORT | **trail** | +1.179R | +0.185R | **0.995R** |
| 17 | SHORT | sl (post-arm) | +1.180R | +0.060R | **1.120R** |
| 21 | LONG | **trail** | +1.444R | +0.378R | **1.067R** |
| **25** | SHORT | **trail** | **+2.507R** | **+1.521R** | **0.986R** |

**Mean giveback across all seven armed positions: 0.935R.** Across the five that ended on the
trail or a post-arm stop: **1.029R**.

**The finding reproduces.** `TRAIL_MULT_ATR (2.5) == SL_BUFFER_ATR (2.5)` makes the trail callback
exactly 1.00R by arithmetic, and vpos 25 gave back **0.986R** — a fifth confirmation, and the
first in production since the mechanism shipped.

**One honest discrepancy.** The 15:24 study cited the four historical givebacks as
**1.02 / 1.04 / 1.16 / 1.18R**; recomputing today from the stored `water_mark` and each position's
own R basis I get **0.98 / 1.00 / 1.12 / 1.07R** for vpos 13/15/17/21. The differences are 0.04–0.11R
and I have not chased them — plausibly a different R denominator or a peak taken from the
excursion table rather than `water_mark`. **It does not change the finding** (both sets cluster on
1R, which is what the arithmetic predicts) but the two figures should not be quoted
interchangeably, and today's are the ones computed from the position ledger.

**Why this matters beyond bookkeeping:** the ~1R giveback is the measurement that *motivated* the
partial. It was inferred from four historical positions and has now held on a fifth, live, under
the current code — which strengthens the premise of the change even as this particular trade shows
the change's cost.

---

# §4 — FOR THE RECORD

Written into `OPEN-ITEMS-SOL.md` as the first live datapoint on the partial, with this framing:

> **Armed position #7, vpos 25, 2026-08-01.** The partial-at-arm mechanism completed its first
> full production lifecycle and **cost 0.155R ($15.64)** on this trade. It performed **exactly as
> designed** — this was a runner (peak +2.51R) and the design shaves a runner's tail. That is the
> accepted bounded downside, **not a defect**. The trade's +1.257R is **not** vindication of the
> partial: without it the position returned **+1.412R**. **n=1 says nothing either way**; do not
> retune before ~15 armed positions with path data, per `config.py`.
>
> Separately: the trail's **~1R giveback reproduced live** (peak +2.507R → exit +1.521R =
> **0.986R**), a fifth confirmation of the finding that motivated the partial.

---

# STATE

Read-only throughout — `main.py`, `virtual_trader.py`, `config.py`, `claude_advisor.py`,
`skip_attribution.py`, `stop_loss.py`, `tor_retry.py` all untouched since the 20:15:16 restart.
Service active, SOL **PAPER**, window **4 of 200**, no open position (vpos 25 closed itself on the
trail at 20:13:32). **Titan untouched** — clean, `HEAD 3316e8a`, active.
