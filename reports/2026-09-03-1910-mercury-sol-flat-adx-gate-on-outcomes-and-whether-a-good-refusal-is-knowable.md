# mercury-sol-flat-adx-gate-on-outcomes-and-whether-a-good-refusal-is-knowable

_2026-09-03 19:10 UTC_

---

# THE FLAT-ADX GATE, JUDGED ON OUTCOMES — AND WHETHER A GOOD REFUSAL CAN BE TOLD FROM A BAD ONE

**Titan pre-flight `tools/openitems_guard.py` → exit 0.** Titan otherwise untouched.
**Mercury-SOL: nothing changed.** `mode=ro`, config read as text, GET-only venue reads, service
untouched, `NRestarts=0`. Full confirmation in §7.

Basis: my own `2026-09-03-1840` report, §3b.

---

# 🔴 THE VERDICT, FIRST

**MIXED — and I say so plainly rather than pick a side.**

**On the serial cut, the one that decides: the gate COSTS money on LONGS and SAVES money on SHORTS,
and the net sign FLIPS between R and dollars.**

| serial cut | n | ΣR of the refused trades | Σ$ | what that means for the gate |
|---|---|---|---|---|
| **LONG** | **8** | **+0.42R** | **+$3.23** | 🔴 **the gate COST $3.23** |
| **SHORT** | **6** | **−1.48R** | **−$2.47** | the gate SAVED $2.47 — **but n=6 is below the n≥8 floor and I refuse to rank it** |
| **net** | 14 | −1.07R | +$0.76 | **the gate SAVED 1.07R and COST $0.76 — the signs disagree** |

The same per-side split holds on the independent cut, at much larger n and with far less meaning:
LONG refusals **+48.80R / +$155.70** (the gate cost that), SHORT refusals **−98.30R / −$193.58**
(the gate saved that). **Both cuts agree on the shape: positive on shorts, negative on longs.**
Neither cut says the gate saves on both sides, and neither says it costs on both sides.

**Part 2's answer: NOTHING SEPARATES that survives the controls.** Two candidates cleared Bonferroni
on nominal p — the confluence score on SHORT and the volume percentile on both sides — and **all
three of those cells failed the 12-window sign-stability control at 1/12**, because 11 of 12 windows
have a leg with n<8. The regime control could not populate its second leg either. **The
paper-versus-live control could not be run at all: every one of the 372 refusals is on the live
book, so the paper cell is n=0.**

**🔴 And the operator's own leading candidate — ADX slope — is not merely unproven, it is INVERTED.**
On the LONG side, refusals where ADX was *rising* into the floor returned **+0.090R** and refusals
where it was *flat or falling* returned **+0.374R**. The breakout-beginning intuition that 09-03
suggested runs the wrong way across the whole population. It fails Bonferroni on all six of its
tests.

**🔴 THE FINDING THAT MATTERS MORE THAN EITHER: THE GATE IS NOT A PER-TRADE FILTER. IT IS A DAY
SWITCH.** On 10 of the 18 days it was live it refused 0.0–5.9 % of proposals; on the other 8 it
refused 61.7–100 %. ADX(1h) barely moves within a day, so the gate is on or off for a whole session.
**372 refusals carry roughly ten days of information, not 372 trades' worth** — which is exactly why
no window control can be satisfied, and it caps what any measurement on this population can prove.

**🔴 By the gate's OWN pre-registered removal criteria (`config.py:378-396`), criterion (a) is met.**
It pre-registered a 33–45 % refusal band before it had refused anything. **Realised: 48.2 %**
(LONG 50.4 %, SHORT 46.2 %). The config's own instruction for that case is *"A REALISED RATE
MATERIALLY ABOVE THAT BAND IS A FINDING ABOUT THE READING… Go and find out which ADX is being read
before touching 20."* — and there is a reading defect: **129 of 372 refusals (34.7 %) were decided on
a stale cached ADX.**

**The staleness defect, quantified separately as ordered: exactly 1 of the 372 would have cleared
the floor on a fresh reading. It was a SHORT and it would have lost −1.07R / −$3.12. The stale cache
SAVED $3.12 over this population. That is luck, not design, and it is stated as such — but it is not
a cost and I will not report it as one.**

**On the operator's own framing: I cannot say "you were wrong to apply it" and I will not say "you
were right".** The gate was applied on discipline over a refuted n=6 cohort; the measurement now
available refutes it on longs, supports it on shorts, and cannot separate good refusals from bad.
The choice is binary and it is the operator's, on the Part 1 numbers above.

**No change is proposed. Nothing was applied.**
---

# 1. THE GATE ON OUTCOMES

## 1a. The population

**372 refusals, 2026-08-17 14:55:04 → 2026-09-03 14:55:03 — 192 LONG, 180 SHORT.**
Every one carries `trades.is_virtual = 0`: the whole population is on the **live** book.
Every one has a `skip_attribution` row, so every one has a recorded price at refusal.
One row (19315, the gate's first-ever refusal) has `srv_adx_1h` NULL — the documented
first-refusal defect at `main.py:4938-4946`; its ADX (13.62) was parsed out of the stored
`error` string.

**Every one of the 372 is listed in Appendix A** with timestamp, side, price at refusal, the ADX the
gate read, a fresh recompute of that ADX, distance below the floor, confluence score, matrix
direction, volume percentile, ADX 1-bar slope, whether it survived the serial cut, and its replayed
exit, R and dollars.

They are **not** spread evenly. They fall on ten calendar days:

| day | LONG | SHORT | | day | LONG | SHORT |
|---|---|---|---|---|---|---|
| 08-17 | 8 | 29 | | 08-30 | 18 | 43 |
| 08-18 | 14 | 34 | | 08-31 | 1 | 0 |
| 08-22 | 1 | 1 | | 09-01 | 39 | 27 |
| 08-23 | 31 | 7 | | 09-03 | 14 | 0 |
| 08-24 | 49 | 19 | | | | |
| 08-29 | 17 | 20 | | | | |

## 1b. The replay contract

Read from the code **as text**, never imported:

| element | value | source |
|---|---|---|
| stop | entry ∓ **2.5 × ATR(1h)** | `config.py:62` `SL_BUFFER_ATR = 2.5` |
| arm | entry ± **0.75 × 2.5 × ATR(1h)** | `trail_arm.activation_distance`, `config.py:231` `TRAIL_ARM_R = 0.75` |
| breakeven lock | entry × (1 ± **0.0020**) | `trail_arm._BE_TARGET_FRAC_ON` |
| trail | `water_mark × (1 ∓ trail_pct/100)`, `trail_pct = round(round(1.875 × ATR, 2)/entry × 100, 3)`, **armed only after the lock** | `config.py:104`, `virtual_trader.py:2649`, management tick |
| fees | **0.100 % taker, BOTH legs** | venue rate, boot line `2026-09-03 17:46:17` |
| size | **$100 notional** (LEVERAGE 5 × $20) | `config.py:50` |
| bar order | **adverse extreme first**, then favourable | as instructed |

Tape: real Bybit `linear SOLUSDT` 5m candles, 2026-08-15 00:00 → 2026-09-03 18:55 (5,700 bars),
GET-only. 1h: 1,339 bars from 2026-07-10 for ATR/ADX warm-up.

### 🔴 The engine, validated against real closed positions

Every live position the 5m tape can reach, replayed with its own stored fill and ATR:

| vpos | side | entry | REAL exit | REAL why | REPLAY exit | REPLAY why | replay R |
|---|---|---|---|---|---|---|---|
| 36 | SHORT | 75.20 | 75.62 | `exchange_market` (externally closed — no comparison possible) | 74.52 | trail | +0.71 |
| **37** | SHORT | 74.38 | **75.09** | **sl** | **75.08** | **sl** | −1.21 |
| 38 | LONG | 77.06 | 81.22 | trail | 79.97 | trail | +2.77 |
| 39 | LONG | 87.82 | 91.45 | trail | 91.69 | trail | +1.72 |
| 40 | LONG | 92.23 | 100.18 | trail | 100.20 | trail | +2.56 |
| 41 | LONG | 101.04 | 106.69 | trail | 103.18 | trail | +0.58 |
| **42** | SHORT | 99.24 | **101.87** | **sl** | **101.86** | **sl** | −1.08 |

**Both stop-outs reproduce to the cent.** Two of the four trail exits reproduce to within 2 cents
(39, 40); two exit materially early (38, 41). The cause is mechanical and known: the live engine
polls the ticker every 10 s, while this replay applies the adverse extreme of a whole 5m bar first,
which trips a trail stop that a tick-by-tick path would have survived.
**Across the six comparable positions the replay totals +$14.15 against the real +$17.24 — it is
conservative by ~18 %.** Every error therefore makes the refused trades look **worse** than they
were, which flatters the gate. Any "the gate cost money" number below is a **floor**, not a ceiling.

*(`ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True`, `config.py:614` — the adaptive trail recompute is in
dryrun and places the frozen `trail_pct`, so it is not a source of divergence.)*

## 1c. 🔴 BOTH CUTS

### Every signal independently (upper bound — it overcounts)

| | n | ΣR | Σ$ | mean | win rate | still open |
|---|---|---|---|---|---|---|
| ALL | 372 | **−49.51** | **−$37.89** | −0.133R | 45.4 % | 4 |
| **LONG** | 192 | **+48.80** | **+$155.70** | +0.254R | 58.3 % | 4 |
| **SHORT** | 180 | **−98.30** | **−$193.58** | −0.546R | 31.7 % | 0 |

Exit census: `sl` 169 (−187.29R) · `trail` 150 (+135.20R) · `be` 49 (**+0.00R** — the breakeven lock
is a fee wash at the real 0.100 % taker, exactly as `trail_arm.py` documents, and this is a second
independent check that the engine implements the contract) · marked-open 4 (+2.58R).

### 🔴 Honouring `MAX_POSITIONS_PER_SIDE = 1` — the cut that decides

Chronological, per side; a taken refusal blocks that side until its own replayed exit.

| | n | ΣR | Σ$ | mean | win rate |
|---|---|---|---|---|---|
| ALL | **14** | **−1.07** | **+$0.76** | −0.076R | 7/14 |
| **LONG** | **8** | **+0.42** | **+$3.23** | +0.052R | 4/8 |
| **SHORT** | **6** | **−1.48** | **−$2.47** | −0.247R | 3/6 |

**372 refusals collapse to 14 trades.** That is the whole point of the cut, and it is what makes the
independent column above an illusion of evidence rather than evidence.

The 14, in order:

| UTC | side | row | fill | ADX read | score | exit | R | $ |
|---|---|---|---|---|---|---|---|---|
| 08-17 14:55 | LONG | 19315 | 75.88 | 13.62 | 5.00 | trail @76.69 08-19 01:25 | +0.70 | +0.86 |
| 08-17 15:35 | SHORT | 19333 | 75.84 | 13.71 | 3.50 | be @75.69 08-18 04:25 | +0.00 | +0.00 |
| 08-18 05:15 | SHORT | 19501 | 75.88 | 11.05 | 3.75 | sl @76.76 08-18 14:25 | −1.17 | −1.36 |
| 08-18 16:05 | SHORT | 19632 | 77.20 | 17.52 | 4.50 | sl @78.23 08-19 12:45 | −1.15 | −1.54 |
| 08-22 21:00 | SHORT | 20494 | 94.37 | 19.04 | 3.50 | sl @98.27 08-24 22:30 | −1.05 | −4.33 |
| 08-22 23:55 | LONG | 20518 | 93.97 | 18.38 | 4.75 | be @94.16 08-23 02:10 | −0.00 | −0.00 |
| 08-23 03:25 | LONG | 20544 | 94.34 | 16.10 | 2.50 | trail @99.78 08-25 07:50 | +1.25 | +5.56 |
| 08-29 01:55 | SHORT | 21923 | 104.15 | 19.77 | 2.00 | trail @102.70 08-31 05:20 | +0.36 | +1.19 |
| 08-29 06:15 | LONG | 21960 | 103.41 | 18.42 | 2.50 | trail @105.24 08-30 17:20 | +0.57 | +1.57 |
| 08-30 17:20 | LONG | 22396 | 106.22 | 16.76 | **8.50** | sl @104.14 08-30 21:00 | −1.10 | −2.16 |
| 08-31 23:05 | LONG | 22784 | 102.94 | 17.87 | 5.00 | sl @100.36 09-01 17:50 | −1.08 | −2.71 |
| 09-01 03:35 | SHORT | 22817 | 103.91 | 14.50 | 4.50 | trail @99.99 09-01 19:20 | +1.53 | +3.57 |
| 09-01 17:50 | LONG | 23013 | 100.82 | 18.96 | 4.00 | sl @98.37 09-01 18:35 | −1.08 | −2.62 |
| 09-03 07:30 | LONG | 23517 | 100.77 | 19.04 | 2.50 | trail @103.73 09-03 15:45 | +1.15 | +2.74 |

🔴 **Note the last row, and what it does to the 09-03 story.** On the serial cut the +4.40 % impulse
does not cost seven refused longs — it costs **one**: the 07:30 refusal at 100.77, which trails out
at 103.73 for **+1.15R / +$2.74**. The four refusals inside the impulse would have been blocked by
that position under the very cap the operator asked me to honour.

### Refinement: the serial cut that ALSO blocks on the positions the bot really held

The bot held five real live positions during the gate's life (LONG 08-18→08-19, 08-20→08-21,
08-21→08-22, 08-27; SHORT 09-01→09-03). Blocking on those as well **changes nothing**: the same 14
trades, **−1.07R / +$0.76**. No refusal in the serial cut begins while the real book already owned
its side.

## 1d. Per side × per era × per book — n stated per cell

**🔴 PAPER CELL n = 0, on both sides.** The gate armed 2026-08-17; the last paper position opened
2026-08-06. Every refusal is live-book. **Paper and live are therefore not pooled here because there
is nothing to pool.**

Era = calendar halves of the gate's own life (midpoint 2026-08-26 02:55 UTC). **This is a TIME split
of one book. It is NOT the paper-vs-live independent sample and is not offered as a substitute.**

| cut | side | era | n | ΣR | Σ$ | mean | win |
|---|---|---|---|---|---|---|---|
| indep | LONG | 08-17→08-26 | 103 | +67.63 | +$204.12 | +0.657R | 73.8 % |
| indep | LONG | 08-26→09-03 | 89 | −18.83 | −$48.42 | −0.212R | 40.4 % |
| indep | SHORT | 08-17→08-26 | 90 | −76.07 | −$157.97 | −0.845R | 24.4 % |
| indep | SHORT | 08-26→09-03 | 90 | −22.23 | −$35.62 | −0.247R | 38.9 % |
| serial | LONG | 08-17→08-26 | **3** | +1.96 | +$6.42 | — | 🔴 n<8, NOT RANKED |
| serial | LONG | 08-26→09-03 | **5** | −1.54 | −$3.18 | — | 🔴 n<8, NOT RANKED |
| serial | SHORT | 08-17→08-26 | **4** | −3.37 | −$7.24 | — | 🔴 n<8, NOT RANKED |
| serial | SHORT | 08-26→09-03 | **2** | +1.89 | +$4.77 | — | 🔴 n<8, NOT RANKED |

**Every serial era cell is below the n≥8 floor. None is ranked.** The independent LONG cells flip
sign between eras (+0.657R → −0.212R); that is one more reason not to read the independent column as
evidence.

## 1e. 🔴 THE HEADLINE — one number per side, on the serial cut

| side | ΣR of the refused trades | Σ$ | **the gate…** |
|---|---|---|---|
| **LONG (n=8)** | **+0.42R** | **+$3.23** | **COST $3.23** |
| **SHORT (n=6)** | **−1.48R** | **−$2.47** | SAVED $2.47 — **n=6 is below the n≥8 floor; not ranked** |
| net (n=14) | −1.07R | +$0.76 | **SAVED 1.07R, COST $0.76 — the two units disagree in sign** |

The sign disagreement is not a rounding artefact. R normalises by the ATR-based stop distance at
entry; dollars do not. The losing shorts happened at low ATR (large R per dollar) and the winning
longs at high ATR (small R per dollar), so the same fourteen trades read −1.07R and +$0.76.
**Given the money is denominated in dollars, the dollar column is the one that pays: on the serial
cut the gate cost $0.76 net, on a book that trades $100 notional.**

---

# 2. 🔴 CAN A GOOD REFUSAL BE TOLD FROM A BAD ONE?

## 2a. The outcome split (independent replay)

| | n | ΣR | Σ$ |
|---|---|---|---|
| LONG **would have WON** | 112 | +98.66 | +$275.34 |
| LONG **would have LOST** | 80 | −49.87 | −$119.64 |
| SHORT **would have WON** | 57 | +39.12 | +$87.46 |
| SHORT **would have LOST** | 123 | −137.42 | −$281.05 |
| BOTH won | 169 | +137.78 | +$362.80 |
| BOTH lost | 203 | −187.29 | −$400.69 |

**The gate is refusing a 45 % win rate.** It is not refusing garbage; it is refusing a coin.

## 2b/2c. The four named candidates — no-look-ahead stated BEFORE testing, and only these four

| # | candidate | computable at the refusal instant? |
|---|---|---|
| 1 | **ADX slope** (Δ over 1, 2, 3 closed 1h bars) | **YES** — from closed bars strictly before the refusal hour, already inside the same 200-bar array the gate fetched |
| 2 | **Distance below the 20.0 floor** | **YES** — it is `20.0 −` the gate's own input |
| 3 | **Confluence score at refusal** | **YES** — computed upstream and already persisted on the refused row |
| 4 | **Volume percentile** of the last **closed** 1h bar vs the trailing 200 | **YES** — same fetched array. The **forming** bar is deliberately excluded: its partial volume is not knowable in full, and `indicators.py:394-400` documents that exact trap |

**No grid was searched. These four, and nothing else, were tested.**

## 2d. Results — n / ΣR / mean / win rate, per side, nothing below n=8 ranked

### 🔴 Candidate 1 — ADX SLOPE. REFUTED, AND INVERTED.

| horizon | side | rising (Δ>0) | flat/falling (Δ≤0) | spread | nominal p |
|---|---|---|---|---|---|
| d1 | LONG | n=81 **+0.090R** win 51.9 % | n=111 **+0.374R** win 63.1 % | flat beats rising by +0.283R | 0.0378 |
| d1 | SHORT | n=79 −0.383R win 38.0 % | n=101 −0.674R win 26.7 % | rising beats flat by +0.292R | 0.0399 |
| d2 | LONG | n=85 +0.107R | n=107 +0.371R | flat by +0.264R | 0.0522 |
| d2 | SHORT | n=71 −0.463R | n=109 −0.600R | rising by +0.137R | 0.3589 |
| d3 | LONG | n=80 +0.103R | n=112 +0.362R | flat by +0.259R | 0.0643 |
| d3 | SHORT | n=52 −0.763R | n=128 −0.458R | **flat by +0.305R** | 0.0318 |

**All six fail Bonferroni (α = 0.00167).** And the direction is the opposite of the hypothesis on the
LONG side at every horizon: **ADX rising into the floor produced the WORSE longs, not the better
ones.** The two sides do not even agree with each other on d1/d2 versus d3. The 09-03 sequence
15.43 → 16.68 → 19.43 is a real observation; it is not a rule.

### Candidate 2 — DISTANCE BELOW THE FLOOR. Also inverted, also fails.

| side | near (gap<2) | mid (2–5) | deep (gap≥5) | spread | p |
|---|---|---|---|---|---|
| LONG | n=34 **−0.093R** | n=68 +0.264R | n=90 **+0.378R** | deep beats near +0.471R | 0.0051 |
| SHORT | n=21 −0.729R | n=30 −0.143R | n=129 −0.610R | mid beats near +0.586R | 0.0275 |

Fails Bonferroni on both sides. On LONG the direction is again backwards: refusals at ADX **far**
below the floor did better than refusals just under it. On SHORT it is non-monotone (mid best, near
and deep worse), which is the shape of noise, not of a threshold.

### Candidate 3 — CONFLUENCE SCORE.

| side | low (<2.5) | mid (2.5–4.0) | high (≥4.0) | spread | p |
|---|---|---|---|---|---|
| LONG | n=49 +0.306R | n=75 +0.314R | n=68 +0.151R | mid − high +0.163R | 0.2615 — fails |
| SHORT | n=20 −0.858R | n=70 −0.738R | n=90 **−0.327R** | high − low **+0.531R** | **0.00074 — PASSES** |

Passes Bonferroni on SHORT only — and note what it separates: **every SHORT bucket is negative.**
It tells "bad" from "less bad". It changes no refusal's fate from loser to winner.

### Candidate 4 — VOLUME PERCENTILE. Passes on both sides, coherently.

| side | low (<50) | mid (50–80) | high (≥80) | spread | p |
|---|---|---|---|---|---|
| LONG | n=81 +0.088R win 59.3 % | n=75 +0.092R win 46.7 % | n=36 **+0.967R win 80.6 %** | high − low **+0.879R** | **<0.00001 — PASSES** |
| SHORT | n=99 **−0.451R** win 31.3 % | n=49 −0.496R | n=32 **−0.919R** win 15.6 % | low − high **+0.469R** | **0.00035 — PASSES** |

High hourly volume at the moment of refusal ⇒ the refused **LONG** would have won and the refused
**SHORT** would have lost. That is symmetric and it is the strongest thing in this study.
**It is also exactly what a direction detector looks like**: high volume in this sample coincided
with up-moves. §3c tests that, and it is where it dies.

## 2e. What a gate carrying the survivor would do — 🔴 VOID

Printed only so the scale is visible. **Both survivors failed §3b and §3c; no rule is described and
none is recommended.**

- Of the 192 LONG refusals, **36** have `vol_pctl ≥ 80` and would change fate (be admitted); their
  replayed total is **+34.82R / +$108.42**.
- Of the **399** proposals the gate admits today, a `require vol_pctl ≥ 80` clause would **newly
  refuse 303 (75.9 %)** — it would be a far bigger gate than the one it modifies.

---

# 3. THE CONTROLS

## 3a. Multiplicity, declared before any result

4 candidates → 6 bucket schemes (d1, d2, d3, gap, score, vol_pctl) → **15 buckets × 2 sides = 30
tests**. **Bonferroni α = 0.05 / 30 = 0.00167.** No bucket below **n = 8** is ranked. No grid search.

## 3b. 🔴 12-WINDOW SIGN STABILITY — ALL THREE SURVIVORS FAIL AT 1/12

Twelve equal-time windows over 2026-08-17 14:55 → 2026-09-03 14:55.

| survivor | correct sign | wrong sign | unusable (a leg has n<8) | strict result |
|---|---|---|---|---|
| score, SHORT (high beats low) | 1/12 | 0/12 | **11/12** | 🔴 **FAILS** (needs ≥10/12) |
| vol_pctl, LONG (high beats low) | 1/12 | 0/12 | **11/12** | 🔴 **FAILS** |
| vol_pctl, SHORT (low beats high) | 1/12 | 0/12 | **11/12** | 🔴 **FAILS** |

**No window disagreed — but only one window in twelve could be evaluated at all.** Six windows are
entirely empty of refusals and five have one bucket empty. This is the day-switch finding showing up
as a measurement limit: the gate's refusals are not distributed in time, so the strongest available
stability control has almost nothing to act on. **A candidate that cannot be tested is not a
candidate that passed.**

## 3c. 🔴 REGIME TEST — THE SECOND LEG IS NEVER POPULATED

`skip_attribution.market_regime` on the 372: **FLAT 322 / TREND 50.**

| survivor | FLAT leg | TREND leg |
|---|---|---|
| score, SHORT | n(high)=75 −0.445R vs n(low)=18 −0.837R → spread +0.392R | n(high)=15, n(low)=**2** → 🔴 NOT POPULATED |
| vol_pctl, LONG | n(high)=36 +0.967R vs n(low)=65 +0.125R → spread +0.842R | n(high)=**0**, n(low)=16 → 🔴 NOT POPULATED |
| vol_pctl, SHORT | n(low)=93 −0.510R vs n(high)=32 −0.919R → spread +0.409R | n(low)=6, n(high)=**0** → 🔴 NOT POPULATED |

**Every effect exists only in the FLAT leg, and the TREND leg cannot be populated — for
`vol_pctl` it is literally empty (n=0 in the high bucket on LONG).** By the standing rule, a
discriminator that only exists in one regime is a regime detector. **This one cannot even be shown
to exist in one regime versus another, because the gate by construction only fires in the flat one.**

*(`skip_attribution.trend_1d` is NULL on all 372: the HTF-regime capture at `main.py:4150-4157` runs
on the `htf_blocked` path only, not on the flat-ADX path. A second regime axis was therefore
unavailable. Reported, not worked around.)*

## 3d. 🔴 PAPER ERA vs LIVE ERA — CANNOT BE RUN

All 372 refusals carry `is_virtual = 0`. The gate armed 2026-08-17; the last paper position opened
2026-08-06. **Paper n = 0 on both sides.** The strongest control available — the one that reversed
the smart-exit rule on 2026-09-03 — **does not exist for this gate**, and nothing here is offered as
equivalent to it. The era halves in §1d are a time split of a single book and are labelled as such.

## 3e. 🔴 THE STALENESS DEFECT, CARRIED IN AND COSTED SEPARATELY

`_CACHE_TTL_BY_TF['1h'] = 300.0` (`indicators.py:62`) — the 1h OHLCV array is served from cache for
up to 5 minutes, and on 2026-09-03 it served ADX 18.4166 across a 15-minute span.

Comparing the reading the gate used against a fresh recompute at the same instant:

| | |
|---|---|
| refusals decided on a reading that differs from fresh (>0.005) | **129 of 372 — 34.7 %** |
| \|delta\| median / p90 / max | 0.145 / 0.551 / **1.477** |
| read BELOW fresh (refused on a stale-low number) | 85 |
| read ABOVE fresh | 44 |
| **refusals that would have CLEARED the 20.0 floor on a fresh reading** | **1** |

The one: **2026-08-30 23:45:14, SHORT, row 22495, read 19.6825, fresh 20.0092.** Replayed, it
returns **−1.07R / −$3.12**.

**🔴 So the staleness defect SAVED $3.12 over this population, it did not cost anything.** It is a
real defect — a third of all readings are stale and the worst is off by 1.48 ADX points — and on a
different tape it would cut the other way. **But the honest number is a saving, and I report it as
a saving.** It is quantified here entirely separately from the gate's own merit, as ordered.

---

# 4. 🔴 THE GATE'S OWN PRE-REGISTERED CRITERIA

`config.py:378-396` pre-registered a refusal rate **before the gate had refused anything**, and named
the **only three** grounds for removal. Those are the criteria that bind, so they are tested.

> *"PRE-REGISTERED REFUSAL RATE, stated BEFORE the gate has refused anything: 33.2 % of
> consultations … LONG 33.9 % SHORT 33.9 % … 41.6 % over the last 30 days … expect the realised rate
> in the 33-45 % band, not at 33.2 % exactly."*

Denominator = every proposal that reached the gate (it sits immediately before `consult_for_entry`,
`main.py:4880`): refusals + everything downstream of it.

| side | refused | admitted | reached | **realised rate** |
|---|---|---|---|---|
| LONG | 192 | 189 | 381 | **50.4 %** |
| SHORT | 180 | 210 | 390 | **46.2 %** |
| **BOTH** | **372** | **399** | **771** | **48.2 %** |

**(a) IT FIRES TOO OFTEN — 🔴 MET.** 48.2 % against a pre-registered 33–45 % band. Both sides are
above the band on their own. The config's own instruction for this case is *"A REALISED RATE
MATERIALLY ABOVE THAT BAND IS A FINDING ABOUT THE READING — a different window, a different cache, a
different TF — AND IT IS NOT A REASON TO LOWER THE THRESHOLD. Go and find out which ADX is being read
before touching 20."* **A cache defect is exactly what §3e found: 34.7 % of readings are stale.**
It is not large enough to explain a 3-to-15-point overshoot on its own — only 1 refusal flips — so
the rate finding stands on its own and is not disposed of by the cache.

**(b) IT FIRES ASYMMETRICALLY BY SIDE — not met, on firing.** 50.4 % vs 46.2 % is a 4.2 pp gap
against a pre-registered 33.9/33.9. That is mild and I will not call it a side ban.
🔴 **But it behaves asymmetrically in OUTCOME, and that is the real asymmetry:** on both cuts the
gate is positive on shorts and negative on longs. Independent: LONG +48.80R (cost) vs SHORT −98.30R
(saved). Serial: LONG +0.42R (cost) vs SHORT −1.48R (saved). **The gate fires nearly symmetrically
and pays asymmetrically.**

**(c) IT REFUSES TRADES A TRADER WOULD TAKE — the config says inspect the rows, not the R.**
The ten highest-scoring refusals:

| UTC | side | ADX | score | combo |
|---|---|---|---|---|
| 08-30 17:20:00 | LONG | 16.76 | **8.50** | `1H:15m-rearm: HyperWave Signal Up \| 15M:HyperWave Signal Up \| 5M:Bullish OB Entered` |
| 08-18 16:20:11 | SHORT | 17.63 | 7.50 | `1H:15m-rearm: Reversal Up \| 15M:Reversal Down + \| 5M:Bearish OB Mitigated` |
| 08-18 16:25:04 | SHORT | 17.63 | 7.50 | same combo |
| 09-01 05:35:03 | SHORT | 14.83 | 7.25 | `1H:Trend Catcher Up \| 15M:HyperWave Signal Down \| 5M:Within Bearish OB` |
| 09-01 01:00:09 | LONG | 16.24 | 7.00 | `1H:Trend Catcher Up \| 15M:HyperWave Signal Up \| 5M:Bullish OB Entered` |
| 08-17 15:45:16 | SHORT | 13.71 | 6.75 | `1H:Smart Trail Switch Bullish \| 15M:Reversal Down \| 5M:Bearish Liquidity Grab` |
| 08-18 16:15:12 | SHORT | 17.63 | 6.75 | `1H:15m-rearm: Reversal Up \| 15M:Reversal Down + \| 5M:Within Bearish OB` |
| 08-23 02:20:00 | SHORT | 17.17 | 6.75 | `1H:Bearish Confirmation \| 15M:HyperWave OB Signal Down \| 5M:Bearish New Imbalance` |
| 08-23 19:10:01 | LONG | 9.14 | 6.75 | `1H:Trend Catcher Up \| 15M:HyperWave Signal Up \| 5M:Bullish Liquidity Grab` |
| 08-24 13:20:07 | SHORT | 12.41 | 6.75 | `1H:Trend Catcher Up \| 15M:Bearish Divergence \| 5M:Within Bearish OB` |

**Three of the ten are fully aligned across all three tiers in one direction** (08-30 LONG at score
8.50; 09-01 01:00 LONG; 08-23 19:10 LONG) — a discretionary trader would take those. **Seven are
not**: the 1H tier disagrees with the trade (`Reversal Up` on a short, `Trend Catcher Up` on a short,
`Smart Trail Switch Bullish` on a short). **Criterion (c) is met for a minority of the refusals and
not for most of them.** And the single best-looking one, 08-30 17:20 at score 8.50, is in the serial
cut — it **stopped out at −1.10R**.

## 4d. 🔴 THE GATE IS A DAY SWITCH, NOT A FILTER

Refusal rate by calendar day over the gate's life:

| day | rate | | day | rate | | day | rate |
|---|---|---|---|---|---|---|---|
| 08-17 | **97.4 %** | | 08-23 | **100 %** | | 08-29 | **61.7 %** |
| 08-18 | **88.9 %** | | 08-24 | **100 %** | | 08-30 | **100 %** |
| 08-19 | 0.0 % | | 08-25 | 0.0 % | | 08-31 | 2.4 % |
| 08-20 | 0.0 % | | 08-26 | 0.0 % | | 09-01 | **89.2 %** |
| 08-21 | 0.0 % | | 08-27 | 0.0 % | | 09-02 | 0.0 % |
| 08-22 | 5.9 % | | 08-28 | 0.0 % | | 09-03 | **63.6 %** |

**Ten days at 0.0–5.9 %. Eight days at 61.7–100 %. Nothing in between.** ADX(1h) is doubly
Wilder-smoothed and moves on a scale of many hours, so the gate is effectively on or off for a whole
session. **This is the single most important structural fact in this study.** It means:

- the 372 refusals carry about ten days of independent information;
- no time-window control can be satisfied on this population (§3b);
- and the serial cut collapsing 372 → 14 is not an artefact of the cut, it is the truth about how
  many decisions the gate actually made.

---

# 5. VERDICT, AGAINST THE OPERATOR'S OWN TREE

**Branch taken: "🔴 Mixed, or nothing separates → say that plainly, and then the choice is binary and
I will make it on Part 1's number alone."**

1. **The gate does NOT save money on both sides.** Serial: LONG +0.42R/+$3.23 refused (cost),
   SHORT −1.48R/−$2.47 refused (saved). Independent: the same signs at larger n.
2. **The gate does NOT cost money on both sides either.** So the sentence *"I applied it on
   discipline over a refuted cohort and the measurement says it loses"* is **not** what the
   measurement says, and I will not write it to be agreeable. What it says is narrower and worse:
   **the gate is a coin-flip filter that pays on one side and charges on the other, and the
   population is too clustered to tell you which will repeat.**
3. **Nothing separates.** Two candidates cleared Bonferroni and all three surviving cells died at
   1/12 on sign stability and could not populate a second regime leg. The paper-vs-live control does
   not exist here. **No discriminator is described, because none survived.**
4. **The operator's leading candidate, ADX slope, is refuted and inverted** on the LONG side at all
   three horizons. That is the clearest negative in this study and it is stated first among the
   candidates for that reason.
5. **By the gate's own pre-registered criteria, (a) is met** — 48.2 % against a 33–45 % band — and
   the config's own remedy for that case points at the reading, where a real cache defect exists
   (34.7 % stale) that is nonetheless **too small to explain the overshoot**.

**Part 1's number, for the binary choice: on the serial cut the gate cost $0.76 net (LONG −$3.23,
SHORT +$2.47) across 14 trades and 18 days, and the replay engine is conservative by ~18 %, so the
true cost is somewhat larger than $0.76, not smaller.**

**No change proposed. Nothing applied. No tail read.**

---

# 6. WHAT WOULD MAKE THIS DECIDABLE (stated, not acted on)

Not a proposal — a statement of what this study could not do, so the next one is not run blind:
the population is 10 days, one book, one regime leg, and 14 serial decisions. **No amount of
re-analysis on these 372 rows will produce a discriminator that survives the four controls.** Only
more days at the gate — or the gate in DRYRUN so that admitted-and-refused become comparable within
the same session — would change that. Which of those to run is the operator's call.

---

# 7. 🔴 READ-ONLY CONFIRMATION

| claim | evidence |
|---|---|
| **DB read-only** | every connection `file:/…/trades.db?mode=ro`, `uri=True`; SELECTs only |
| **cwd outside SOL's tree** | all work in `/tmp/claude-0/…/scratchpad`; `pwd` verified |
| **config not imported** | `config.py`, `main.py`, `virtual_trader.py`, `trail_arm.py`, `indicators.py`, `state_machine.py` read with `sed`/`grep`, cited by line. The replay engine re-declares the constants literally with the citation beside each |
| **no writes** | 34 of 34 `*.py` + `.env` md5 identical before and after |
| **no orders placed or cancelled** | no venue write call issued; only `GET /v5/market/kline` |
| **service untouched** | `ActiveState=active`, `SubState=running`, `ExecMainPID=3422117`, start `2026-09-03 17:45:58 UTC` — unchanged |
| **`NRestarts` unchanged** | `NRestarts=0` before, `NRestarts=0` after |
| **Titan** | `openitems_guard.py` exit 0; not touched otherwise |

---

# APPENDIX A — ALL 372 REFUSALS

`gap` = 20.0 − the ADX the gate read. `d1` = ADX(1h) change over the last closed 1h bar.
`volPctl` = volume percentile of the last closed 1h bar against the trailing 200.
`serial?` = survived the `MAX_POSITIONS_PER_SIDE = 1` cut. `R` and `$` are the full-contract replay.

| # | row | UTC | side | price | ADX read | ADX fresh | gap | score | mdir | volPctl | d1 | serial? | replay exit | why | R | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 19315 | 2026-08-17 14:55:15 | LONG | 75.88 | 13.62 | 14.05 | 6.38 | 5.00 | LONG | 91 | -1.09 | YES | 76.69 08-19 01:25 | trail | +0.70 | +0.86 |
| 2 | 19333 | 2026-08-17 15:35:30 | SHORT | 75.84 | 13.71 | 13.71 | 6.29 | 3.50 | SHORT | 69 | -0.39 | YES | 75.69 08-18 04:25 | be | +0.00 | +0.00 |
| 3 | 19334 | 2026-08-17 15:40:30 | SHORT | 75.90 | 13.71 | 13.86 | 6.29 | 3.50 | SHORT | 69 | -0.39 |  | 75.75 08-18 04:30 | be | +0.00 | +0.00 |
| 4 | 19338 | 2026-08-17 15:45:19 | SHORT | 76.00 | 13.71 | 14.05 | 6.29 | 5.50 | SHORT | 69 | -0.39 |  | 75.85 08-18 05:05 | be | +0.00 | +0.00 |
| 5 | 19339 | 2026-08-17 15:45:26 | SHORT | 76.00 | 13.71 | 14.05 | 6.29 | 6.75 | SHORT | 69 | -0.39 |  | 75.85 08-18 05:05 | be | +0.00 | +0.00 |
| 6 | 19341 | 2026-08-17 15:50:16 | SHORT | 76.06 | 14.05 | 14.16 | 5.95 | 4.25 | SHORT | 69 | -0.39 |  | 75.85 08-18 05:05 | trail | +0.06 | +0.07 |
| 7 | 19345 | 2026-08-17 15:55:12 | SHORT | 76.09 | 14.05 | 14.16 | 5.95 | 4.25 | SHORT | 69 | -0.39 |  | 75.85 08-18 05:05 | trail | +0.09 | +0.11 |
| 8 | 19348 | 2026-08-17 16:00:33 | SHORT | 76.05 | 14.27 | 14.27 | 5.73 | 6.00 | SHORT | 88 | +0.11 |  | 75.82 08-18 05:05 | trail | +0.09 | +0.10 |
| 9 | 19351 | 2026-08-17 16:20:23 | SHORT | 75.94 | 14.27 | 14.27 | 5.73 | 5.25 | SHORT | 88 | +0.11 |  | 75.79 08-18 04:45 | be | +0.00 | +0.00 |
| 10 | 19353 | 2026-08-17 16:30:23 | SHORT | 75.94 | 14.27 | 14.27 | 5.73 | 6.00 | SHORT | 88 | +0.11 |  | 75.79 08-18 04:45 | be | +0.00 | +0.00 |
| 11 | 19354 | 2026-08-17 16:40:18 | SHORT | 76.07 | 14.27 | 14.27 | 5.73 | 6.25 | SHORT | 88 | +0.11 |  | 75.83 08-18 05:05 | trail | +0.09 | +0.11 |
| 12 | 19356 | 2026-08-17 17:00:23 | SHORT | 75.94 | 14.37 | 14.30 | 5.63 | 4.25 | SHORT | 43 | +0.11 |  | 75.79 08-18 04:45 | be | +0.00 | +0.00 |
| 13 | 19357 | 2026-08-17 17:05:13 | SHORT | 75.88 | 14.37 | 14.23 | 5.63 | 4.25 | SHORT | 43 | +0.11 |  | 75.73 08-18 04:30 | be | +0.00 | +0.00 |
| 14 | 19361 | 2026-08-17 17:10:25 | SHORT | 75.85 | 14.23 | 13.94 | 5.77 | 5.00 | SHORT | 43 | +0.11 |  | 75.70 08-18 04:30 | be | +0.00 | +0.00 |
| 15 | 19364 | 2026-08-17 17:15:25 | SHORT | 75.75 | 14.23 | 13.84 | 5.77 | 2.50 | NEUTRAL | 43 | +0.11 |  | 76.65 08-18 14:25 | sl | -1.17 | -1.38 |
| 16 | 19366 | 2026-08-17 17:20:18 | SHORT | 75.98 | 13.84 | 13.84 | 6.16 | 2.50 | NEUTRAL | 43 | +0.11 |  | 75.83 08-18 05:05 | be | +0.00 | +0.00 |
| 17 | 19367 | 2026-08-17 17:25:15 | SHORT | 75.91 | 13.84 | 13.84 | 6.16 | 4.50 | SHORT | 43 | +0.11 |  | 75.76 08-18 04:30 | be | +0.00 | +0.00 |
| 18 | 19370 | 2026-08-17 17:35:20 | SHORT | 75.75 | 13.84 | 13.60 | 6.16 | 2.50 | SHORT | 43 | +0.11 |  | 76.67 08-18 14:25 | sl | -1.17 | -1.42 |
| 19 | 19374 | 2026-08-17 17:40:22 | SHORT | 75.82 | 13.60 | 13.60 | 6.40 | 4.75 | SHORT | 43 | +0.11 |  | 76.74 08-18 14:25 | sl | -1.17 | -1.42 |
| 20 | 19376 | 2026-08-17 17:45:18 | SHORT | 75.84 | 13.60 | 13.60 | 6.40 | 4.75 | SHORT | 43 | +0.11 |  | 76.76 08-18 14:25 | sl | -1.17 | -1.42 |
| 21 | 19378 | 2026-08-17 18:10:15 | SHORT | 75.84 | 12.98 | 12.98 | 7.02 | 4.00 | SHORT | 56 | -0.67 |  | 75.69 08-18 04:25 | be | +0.00 | +0.00 |
| 22 | 19379 | 2026-08-17 18:20:17 | SHORT | 75.94 | 12.98 | 13.15 | 7.02 | 2.00 | SHORT | 56 | -0.67 |  | 75.79 08-18 04:45 | be | +0.00 | +0.00 |
| 23 | 19382 | 2026-08-17 18:25:18 | SHORT | 76.05 | 13.15 | 13.15 | 6.85 | 1.75 | SHORT | 56 | -0.67 |  | 75.84 08-18 05:05 | trail | +0.06 | +0.07 |
| 24 | 19384 | 2026-08-17 18:30:21 | SHORT | 75.97 | 13.15 | 13.15 | 6.85 | 1.75 | SHORT | 56 | -0.67 |  | 75.82 08-18 05:05 | be | +0.00 | +0.00 |
| 25 | 19388 | 2026-08-17 19:05:20 | LONG | 75.80 | 12.63 | 12.63 | 7.37 | 1.75 | LONG | 52 | -0.45 |  | 76.74 08-18 20:50 | trail | +0.90 | +1.03 |
| 26 | 19390 | 2026-08-17 19:10:21 | LONG | 75.82 | 12.63 | 12.53 | 7.37 | 1.75 | LONG | 52 | -0.45 |  | 76.74 08-18 20:50 | trail | +0.88 | +1.01 |
| 27 | 19391 | 2026-08-17 19:15:23 | LONG | 75.75 | 12.50 | 12.50 | 7.50 | 3.50 | LONG | 52 | -0.45 |  | 76.74 08-18 20:50 | trail | +0.95 | +1.10 |
| 28 | 19406 | 2026-08-17 19:50:23 | LONG | 75.77 | 12.44 | 12.44 | 7.56 | 1.75 | LONG | 52 | -0.45 |  | 76.73 08-18 20:50 | trail | +0.91 | +1.06 |
| 29 | 19408 | 2026-08-17 19:55:27 | LONG | 75.72 | 12.44 | 12.44 | 7.56 | 1.75 | LONG | 52 | -0.45 |  | 76.73 08-18 20:50 | trail | +0.96 | +1.13 |
| 30 | 19411 | 2026-08-17 20:00:26 | SHORT | 75.75 | 12.44 | 11.68 | 7.56 | 3.50 | SHORT | 20 | -0.71 |  | 76.59 08-18 14:20 | sl | -1.18 | -1.31 |
| 31 | 19413 | 2026-08-17 20:20:17 | SHORT | 75.65 | 11.73 | 11.73 | 8.27 | 4.75 | SHORT | 20 | -0.71 |  | 76.51 08-18 14:20 | sl | -1.18 | -1.33 |
| 32 | 19414 | 2026-08-17 20:40:16 | SHORT | 75.84 | 11.73 | 11.73 | 8.27 | 3.00 | SHORT | 20 | -0.71 |  | 75.69 08-18 04:25 | be | +0.00 | +0.00 |
| 33 | 19416 | 2026-08-17 20:45:19 | SHORT | 76.03 | 11.73 | 12.25 | 8.27 | 5.00 | SHORT | 20 | -0.71 |  | 75.83 08-18 05:05 | trail | +0.05 | +0.06 |
| 34 | 19428 | 2026-08-17 22:20:18 | SHORT | 75.78 | 11.68 | 11.64 | 8.32 | 3.00 | SHORT | 20 | -0.18 |  | 76.64 08-18 14:25 | sl | -1.18 | -1.33 |
| 35 | 19429 | 2026-08-17 22:20:24 | SHORT | 75.78 | 11.68 | 11.64 | 8.32 | 4.25 | SHORT | 20 | -0.18 |  | 76.64 08-18 14:25 | sl | -1.18 | -1.33 |
| 36 | 19430 | 2026-08-17 23:15:18 | LONG | 75.80 | 10.58 | 10.58 | 9.42 | 1.75 | LONG | 8 | -0.77 |  | 76.76 08-18 20:50 | trail | +0.95 | +1.06 |
| 37 | 19435 | 2026-08-17 23:35:12 | LONG | 76.00 | 10.58 | 10.94 | 9.42 | 3.50 | LONG | 8 | -0.77 |  | 76.72 08-18 20:50 | trail | +0.64 | +0.74 |
| 38 | 19489 | 2026-08-18 03:35:15 | LONG | 75.31 | 12.13 | 12.13 | 7.87 | 4.50 | LONG | 81 | +0.87 |  | 76.71 08-18 20:50 | trail | +1.39 | +1.66 |
| 39 | 19490 | 2026-08-18 03:45:17 | LONG | 75.47 | 12.13 | 12.13 | 7.87 | 4.25 | LONG | 81 | +0.87 |  | 76.71 08-18 20:50 | trail | +1.21 | +1.44 |
| 40 | 19493 | 2026-08-18 03:50:21 | LONG | 75.44 | 12.13 | 12.13 | 7.87 | 4.25 | LONG | 81 | +0.87 |  | 76.71 08-18 20:50 | trail | +1.25 | +1.49 |
| 41 | 19494 | 2026-08-18 04:00:25 | LONG | 75.45 | 12.88 | 12.88 | 7.12 | 4.25 | LONG | 58 | +0.81 |  | 76.74 08-18 20:50 | trail | +1.34 | +1.51 |
| 42 | 19495 | 2026-08-18 04:10:14 | LONG | 75.59 | 12.51 | 12.32 | 7.49 | 4.25 | LONG | 58 | +0.81 |  | 76.72 08-18 20:50 | trail | +1.11 | +1.30 |
| 43 | 19496 | 2026-08-18 04:15:12 | LONG | 75.62 | 12.51 | 12.32 | 7.49 | 5.00 | LONG | 58 | +0.81 |  | 76.72 08-18 20:50 | trail | +1.08 | +1.26 |
| 44 | 19497 | 2026-08-18 04:35:16 | LONG | 75.72 | 11.86 | 11.86 | 8.14 | 6.00 | LONG | 58 | +0.81 |  | 76.70 08-18 20:50 | trail | +0.92 | +1.10 |
| 45 | 19499 | 2026-08-18 04:40:14 | LONG | 75.73 | 11.86 | 11.86 | 8.14 | 5.50 | LONG | 58 | +0.81 |  | 76.70 08-18 20:50 | trail | +0.91 | +1.09 |
| 46 | 19501 | 2026-08-18 05:15:18 | SHORT | 75.88 | 11.05 | 11.05 | 8.95 | 3.75 | SHORT | 38 | -0.33 | YES | 76.76 08-18 14:25 | sl | -1.17 | -1.36 |
| 47 | 19504 | 2026-08-18 06:20:18 | SHORT | 75.80 | 10.36 | 10.36 | 9.64 | 2.50 | SHORT | 74 | -0.74 |  | 76.70 08-18 14:25 | sl | -1.17 | -1.39 |
| 48 | 19507 | 2026-08-18 06:30:19 | SHORT | 75.94 | 10.26 | 10.42 | 9.74 | 4.50 | SHORT | 74 | -0.74 |  | 76.86 08-18 14:25 | sl | -1.17 | -1.42 |
| 49 | 19509 | 2026-08-18 06:35:14 | SHORT | 75.91 | 10.26 | 10.42 | 9.74 | 4.25 | SHORT | 74 | -0.74 |  | 76.83 08-18 14:25 | sl | -1.17 | -1.42 |
| 50 | 19511 | 2026-08-18 06:45:20 | SHORT | 75.97 | 10.42 | 10.46 | 9.58 | 2.00 | SHORT | 74 | -0.74 |  | 76.90 08-18 14:25 | sl | -1.17 | -1.42 |
| 51 | 19513 | 2026-08-18 06:50:12 | SHORT | 75.90 | 10.42 | 10.46 | 9.58 | 2.50 | SHORT | 74 | -0.74 |  | 76.83 08-18 14:25 | sl | -1.16 | -1.42 |
| 52 | 19515 | 2026-08-18 07:00:24 | SHORT | 76.00 | 9.90 | 9.97 | 10.10 | 2.50 | SHORT | 48 | -0.60 |  | 76.88 08-18 14:25 | sl | -1.17 | -1.35 |
| 53 | 19516 | 2026-08-18 07:05:15 | SHORT | 75.97 | 9.90 | 9.97 | 10.10 | 2.50 | SHORT | 48 | -0.60 |  | 76.85 08-18 14:25 | sl | -1.17 | -1.35 |
| 54 | 19518 | 2026-08-18 07:10:16 | SHORT | 76.00 | 9.97 | 10.31 | 10.03 | 2.50 | SHORT | 48 | -0.60 |  | 76.90 08-18 14:25 | sl | -1.17 | -1.38 |
| 55 | 19528 | 2026-08-18 07:25:13 | LONG | 76.06 | 10.57 | 10.57 | 9.43 | 3.50 | LONG | 48 | -0.60 |  | 76.71 08-18 20:50 | trail | +0.54 | +0.65 |
| 56 | 19544 | 2026-08-18 08:10:24 | SHORT | 75.82 | 10.38 | 10.31 | 9.62 | 3.00 | SHORT | 76 | +0.11 |  | 76.73 08-18 14:25 | sl | -1.17 | -1.40 |
| 57 | 19556 | 2026-08-18 10:30:11 | SHORT | 75.78 | 9.59 | 9.51 | 10.41 | 2.50 | SHORT | 16 | -0.24 |  | 76.65 08-18 14:25 | sl | -1.17 | -1.35 |
| 58 | 19558 | 2026-08-18 11:10:18 | SHORT | 75.93 | 8.99 | 9.31 | 11.01 | 1.75 | SHORT | 14 | -0.56 |  | 76.79 08-18 14:25 | sl | -1.18 | -1.33 |
| 59 | 19560 | 2026-08-18 11:20:09 | LONG | 76.28 | 10.22 | 10.40 | 9.78 | 3.00 | LONG | 14 | -0.56 |  | 76.70 08-18 20:50 | trail | +0.29 | +0.35 |
| 60 | 19566 | 2026-08-18 11:25:10 | LONG | 76.34 | 10.40 | 10.40 | 9.60 | 3.50 | LONG | 14 | -0.56 |  | 76.70 08-18 20:50 | trail | +0.22 | +0.27 |
| 61 | 19578 | 2026-08-18 12:05:18 | SHORT | 76.43 | 11.34 | 11.37 | 8.66 | 4.25 | SHORT | 92 | +0.88 |  | 77.33 08-18 19:25 | sl | -1.17 | -1.37 |
| 62 | 19582 | 2026-08-18 12:10:13 | SHORT | 76.34 | 11.34 | 11.37 | 8.66 | 2.50 | SHORT | 92 | +0.88 |  | 77.24 08-18 14:30 | sl | -1.17 | -1.37 |
| 63 | 19583 | 2026-08-18 12:15:10 | SHORT | 76.34 | 11.37 | 11.37 | 8.63 | 2.50 | SHORT | 92 | +0.88 |  | 77.24 08-18 14:30 | sl | -1.17 | -1.38 |
| 64 | 19592 | 2026-08-18 12:50:16 | SHORT | 76.32 | 11.37 | 11.37 | 8.63 | 4.25 | SHORT | 92 | +0.88 |  | 77.23 08-18 14:30 | sl | -1.17 | -1.39 |
| 65 | 19593 | 2026-08-18 12:55:14 | SHORT | 76.30 | 11.37 | 11.37 | 8.63 | 5.00 | SHORT | 92 | +0.88 |  | 77.21 08-18 14:30 | sl | -1.17 | -1.39 |
| 66 | 19594 | 2026-08-18 13:00:16 | SHORT | 76.16 | 11.98 | 11.82 | 8.02 | 4.25 | SHORT | 66 | +0.97 |  | 77.03 08-18 14:25 | sl | -1.18 | -1.34 |
| 67 | 19595 | 2026-08-18 13:05:11 | SHORT | 76.18 | 11.98 | 11.82 | 8.02 | 5.00 | SHORT | 66 | +0.97 |  | 77.05 08-18 14:30 | sl | -1.18 | -1.34 |
| 68 | 19596 | 2026-08-18 13:10:17 | SHORT | 76.12 | 11.82 | 11.82 | 8.18 | 4.25 | SHORT | 66 | +0.97 |  | 76.99 08-18 14:25 | sl | -1.18 | -1.34 |
| 69 | 19597 | 2026-08-18 13:15:18 | SHORT | 76.12 | 11.82 | 11.74 | 8.18 | 4.25 | SHORT | 66 | +0.97 |  | 76.99 08-18 14:25 | sl | -1.18 | -1.34 |
| 70 | 19598 | 2026-08-18 13:20:12 | SHORT | 76.09 | 11.82 | 11.74 | 8.18 | 4.25 | SHORT | 66 | +0.97 |  | 76.96 08-18 14:25 | sl | -1.18 | -1.34 |
| 71 | 19599 | 2026-08-18 13:25:18 | SHORT | 76.12 | 11.74 | 11.63 | 8.26 | 4.25 | SHORT | 66 | +0.97 |  | 77.00 08-18 14:25 | sl | -1.17 | -1.35 |
| 72 | 19600 | 2026-08-18 13:30:20 | SHORT | 76.05 | 11.63 | 11.49 | 8.37 | 4.25 | SHORT | 66 | +0.97 |  | 76.93 08-18 14:25 | sl | -1.17 | -1.36 |
| 73 | 19601 | 2026-08-18 13:35:20 | SHORT | 76.05 | 11.49 | 11.49 | 8.51 | 4.25 | SHORT | 66 | +0.97 |  | 76.94 08-18 14:25 | sl | -1.17 | -1.37 |
| 74 | 19602 | 2026-08-18 13:40:27 | SHORT | 76.25 | 11.49 | 11.49 | 8.51 | 4.25 | SHORT | 66 | +0.97 |  | 77.14 08-18 14:30 | sl | -1.17 | -1.37 |
| 75 | 19603 | 2026-08-18 13:50:25 | SHORT | 76.12 | 11.49 | 11.49 | 8.51 | 4.25 | SHORT | 66 | +0.97 |  | 77.01 08-18 14:25 | sl | -1.17 | -1.37 |
| 76 | 19604 | 2026-08-18 13:55:22 | SHORT | 76.03 | 11.49 | 11.49 | 8.51 | 4.25 | SHORT | 66 | +0.97 |  | 76.92 08-18 14:25 | sl | -1.17 | -1.37 |
| 77 | 19605 | 2026-08-18 14:00:33 | SHORT | 76.16 | 11.60 | 11.80 | 8.40 | 4.25 | SHORT | 82 | +0.12 |  | 77.03 08-18 14:25 | sl | -1.18 | -1.35 |
| 78 | 19615 | 2026-08-18 14:30:10 | LONG | 77.03 | 13.28 | 13.65 | 6.72 | 1.75 | LONG | 82 | +0.12 |  | 79.94 08-19 14:50 | trail | +2.64 | +3.58 |
| 79 | 19617 | 2026-08-18 14:30:16 | LONG | 77.03 | 13.28 | 13.65 | 6.72 | 1.75 | LONG | 82 | +0.12 |  | 79.94 08-19 14:50 | trail | +2.64 | +3.58 |
| 80 | 19618 | 2026-08-18 14:30:20 | LONG | 77.03 | 13.28 | 13.65 | 6.72 | 1.75 | LONG | 82 | +0.12 |  | 79.94 08-19 14:50 | trail | +2.64 | +3.58 |
| 81 | 19632 | 2026-08-18 16:05:13 | SHORT | 77.20 | 17.52 | 17.63 | 2.48 | 4.50 | SHORT | 86 | +2.01 | YES | 78.23 08-19 12:45 | sl | -1.15 | -1.54 |
| 82 | 19634 | 2026-08-18 16:10:17 | SHORT | 77.03 | 17.63 | 17.63 | 2.37 | 5.00 | SHORT | 86 | +2.01 |  | 78.07 08-19 12:40 | sl | -1.15 | -1.55 |
| 83 | 19635 | 2026-08-18 16:15:23 | SHORT | 77.00 | 17.63 | 17.63 | 2.37 | 6.75 | SHORT | 86 | +2.01 |  | 78.06 08-19 12:40 | sl | -1.15 | -1.57 |
| 84 | 19637 | 2026-08-18 16:20:17 | SHORT | 76.97 | 17.63 | 17.63 | 2.37 | 7.50 | SHORT | 86 | +2.01 |  | 78.03 08-19 12:40 | sl | -1.15 | -1.58 |
| 85 | 19638 | 2026-08-18 16:25:25 | SHORT | 76.88 | 17.63 | 17.63 | 2.37 | 7.50 | SHORT | 86 | +2.01 |  | 77.95 08-19 12:40 | sl | -1.14 | -1.60 |
| 86 | 20494 | 2026-08-22 21:00:14 | SHORT | 94.37 | 19.04 | 19.03 | 0.96 | 3.50 | SHORT | 28 | -1.20 | YES | 98.27 08-24 22:30 | sl | -1.05 | -4.33 |
| 87 | 20518 | 2026-08-22 23:55:10 | LONG | 93.97 | 18.38 | 18.38 | 1.62 | 4.75 | LONG | 63 | -0.56 | YES | 94.16 08-23 02:10 | be | -0.00 | -0.00 |
| 88 | 20520 | 2026-08-23 00:15:14 | LONG | 93.78 | 17.86 | 17.86 | 2.14 | 2.00 | LONG | 26 | -0.52 |  | 93.97 08-23 02:10 | be | -0.00 | -0.00 |
| 89 | 20527 | 2026-08-23 00:40:09 | LONG | 96.72 | 18.27 | 18.27 | 1.73 | 2.25 | LONG | 26 | -0.52 |  | 92.54 08-23 04:45 | sl | -1.05 | -4.52 |
| 90 | 20532 | 2026-08-23 00:55:11 | LONG | 96.52 | 18.35 | 18.35 | 1.65 | 2.50 | LONG | 26 | -0.52 |  | 92.31 08-23 04:45 | sl | -1.04 | -4.56 |
| 91 | 20536 | 2026-08-23 02:15:10 | SHORT | 94.56 | 17.17 | 17.17 | 2.83 | 2.50 | SHORT | 82 | -0.02 |  | 98.86 08-24 23:55 | sl | -1.05 | -4.75 |
| 92 | 20538 | 2026-08-23 02:20:09 | SHORT | 94.69 | 17.17 | 17.17 | 2.83 | 6.75 | SHORT | 82 | -0.02 |  | 98.99 08-25 00:05 | sl | -1.05 | -4.74 |
| 93 | 20541 | 2026-08-23 02:55:11 | SHORT | 95.12 | 17.17 | 17.17 | 2.83 | 4.50 | SHORT | 82 | -0.02 |  | 94.67 08-23 11:35 | trail | +0.06 | +0.28 |
| 94 | 20544 | 2026-08-23 03:25:09 | LONG | 94.34 | 16.10 | 16.10 | 3.90 | 2.50 | LONG | 96 | -1.16 | YES | 99.78 08-25 07:50 | trail | +1.25 | +5.56 |
| 95 | 20547 | 2026-08-23 03:35:11 | SHORT | 93.84 | 16.10 | 16.10 | 3.90 | 2.50 | SHORT | 96 | -1.16 |  | 98.13 08-24 22:30 | sl | -1.04 | -4.78 |
| 96 | 20549 | 2026-08-23 03:45:08 | LONG | 93.63 | 16.13 | 16.13 | 3.87 | 2.00 | LONG | 96 | -1.16 |  | 99.64 08-25 07:50 | trail | +1.35 | +6.21 |
| 97 | 20552 | 2026-08-23 04:05:09 | LONG | 93.38 | 15.25 | 15.33 | 4.75 | 4.25 | LONG | 72 | -1.04 |  | 99.77 08-25 07:50 | trail | +1.49 | +6.64 |
| 98 | 20553 | 2026-08-23 04:10:07 | LONG | 93.38 | 15.25 | 15.33 | 4.75 | 3.50 | LONG | 72 | -1.04 |  | 99.74 08-25 07:50 | trail | +1.47 | +6.60 |
| 99 | 20554 | 2026-08-23 04:25:08 | LONG | 93.62 | 15.33 | 15.33 | 4.67 | 3.50 | LONG | 72 | -1.04 |  | 99.75 08-25 07:50 | trail | +1.42 | +6.34 |
| 100 | 20555 | 2026-08-23 04:30:12 | LONG | 93.62 | 15.33 | 15.38 | 4.67 | 3.50 | LONG | 72 | -1.04 |  | 99.74 08-25 07:50 | trail | +1.41 | +6.33 |
| 101 | 20556 | 2026-08-23 04:35:09 | LONG | 93.12 | 15.33 | 15.44 | 4.67 | 4.25 | LONG | 72 | -1.04 |  | 99.71 08-25 07:50 | trail | +1.52 | +6.87 |
| 102 | 20558 | 2026-08-23 04:45:09 | LONG | 93.00 | 15.52 | 15.85 | 4.48 | 3.75 | LONG | 72 | -1.04 |  | 99.59 08-25 07:50 | trail | +1.47 | +6.88 |
| 103 | 20560 | 2026-08-23 04:50:08 | LONG | 92.34 | 15.52 | 15.85 | 4.48 | 4.25 | LONG | 72 | -1.04 |  | 99.57 08-25 07:50 | trail | +1.62 | +7.62 |
| 104 | 20561 | 2026-08-23 04:55:10 | LONG | 92.90 | 15.85 | 15.85 | 4.15 | 3.50 | LONG | 72 | -1.04 |  | 99.59 08-25 07:50 | trail | +1.49 | +6.99 |
| 105 | 20562 | 2026-08-23 05:00:09 | LONG | 92.72 | 15.59 | 15.59 | 4.41 | 3.50 | LONG | 81 | -0.28 |  | 99.77 08-25 07:50 | trail | +1.66 | +7.40 |
| 106 | 20563 | 2026-08-23 05:05:11 | LONG | 92.90 | 15.59 | 15.65 | 4.41 | 3.50 | LONG | 81 | -0.28 |  | 99.72 08-25 07:50 | trail | +1.58 | +7.14 |
| 107 | 20564 | 2026-08-23 05:10:08 | LONG | 92.60 | 15.59 | 15.65 | 4.41 | 4.25 | LONG | 81 | -0.28 |  | 99.71 08-25 07:50 | trail | +1.65 | +7.47 |
| 108 | 20566 | 2026-08-23 05:20:20 | LONG | 92.80 | 15.93 | 15.93 | 4.07 | 3.75 | LONG | 81 | -0.28 |  | 99.60 08-25 07:50 | trail | +1.52 | +7.12 |
| 109 | 20567 | 2026-08-23 05:25:10 | LONG | 93.27 | 15.93 | 15.93 | 4.07 | 3.00 | LONG | 81 | -0.28 |  | 99.59 08-25 07:50 | trail | +1.41 | +6.57 |
| 110 | 20580 | 2026-08-23 07:20:10 | SHORT | 92.88 | 15.91 | 15.91 | 4.09 | 2.25 | SHORT | 70 | +0.07 |  | 96.95 08-24 15:20 | sl | -1.05 | -4.59 |
| 111 | 20585 | 2026-08-23 08:15:09 | SHORT | 92.81 | 15.81 | 15.81 | 4.19 | 2.25 | SHORT | 42 | -0.09 |  | 96.72 08-24 12:50 | sl | -1.05 | -4.42 |
| 112 | 20608 | 2026-08-23 13:10:12 | SHORT | 94.77 | 12.26 | 12.38 | 7.74 | 5.00 | SHORT | 48 | -0.58 |  | 98.13 08-24 22:30 | sl | -1.06 | -3.75 |
| 113 | 20618 | 2026-08-23 14:45:13 | LONG | 94.53 | 12.14 | 12.14 | 7.86 | 5.50 | LONG | 73 | +0.23 |  | 94.76 08-24 17:25 | trail | +0.01 | +0.04 |
| 114 | 20622 | 2026-08-23 14:45:16 | LONG | 94.53 | 12.14 | 12.14 | 7.86 | 2.50 | LONG | 73 | +0.23 |  | 94.76 08-24 17:25 | trail | +0.01 | +0.04 |
| 115 | 20624 | 2026-08-23 14:50:13 | LONG | 94.84 | 12.14 | 12.14 | 7.86 | 2.50 | LONG | 73 | +0.23 |  | 95.03 08-24 17:20 | be | -0.00 | -0.00 |
| 116 | 20644 | 2026-08-23 17:05:16 | LONG | 95.19 | 10.12 | 10.12 | 9.88 | 5.00 | LONG | 40 | -0.70 |  | 100.11 08-25 01:50 | trail | +1.39 | +4.97 |
| 117 | 20647 | 2026-08-23 18:20:15 | LONG | 95.16 | 9.61 | 9.61 | 10.39 | 5.00 | LONG | 53 | -0.55 |  | 95.35 08-24 17:00 | be | -0.00 | -0.00 |
| 118 | 20649 | 2026-08-23 19:10:13 | LONG | 95.05 | 9.14 | 9.22 | 10.86 | 6.75 | LONG | 36 | -0.51 |  | 95.24 08-24 17:00 | be | -0.00 | -0.00 |
| 119 | 20651 | 2026-08-23 19:15:18 | LONG | 94.95 | 9.22 | 9.22 | 10.78 | 5.00 | LONG | 36 | -0.51 |  | 95.23 08-24 17:00 | trail | +0.03 | +0.10 |
| 120 | 20661 | 2026-08-23 20:05:15 | LONG | 94.91 | 8.98 | 8.98 | 11.02 | 2.50 | LONG | 32 | -0.35 |  | 95.35 08-24 17:00 | trail | +0.08 | +0.26 |
| 121 | 20672 | 2026-08-23 21:10:28 | LONG | 95.55 | 8.41 | 8.38 | 11.59 | 4.75 | LONG | 22 | -0.28 |  | 98.63 08-25 00:05 | trail | +0.98 | +3.02 |
| 122 | 20678 | 2026-08-23 21:25:08 | LONG | 95.94 | 8.75 | 8.83 | 11.25 | 2.50 | LONG | 22 | -0.28 |  | 98.58 08-25 00:05 | trail | +0.81 | +2.55 |
| 123 | 20695 | 2026-08-23 23:10:11 | LONG | 95.47 | 8.09 | 8.09 | 11.91 | 2.00 | SHORT | 64 | -0.40 |  | 95.66 08-24 17:00 | be | -0.00 | -0.00 |
| 124 | 20697 | 2026-08-23 23:30:13 | LONG | 95.48 | 8.09 | 8.21 | 11.91 | 2.00 | LONG | 64 | -0.40 |  | 98.63 08-25 00:05 | trail | +1.01 | +3.10 |
| 125 | 20699 | 2026-08-23 23:45:11 | LONG | 95.18 | 8.21 | 8.21 | 11.79 | 2.00 | SHORT | 64 | -0.40 |  | 95.37 08-24 17:00 | be | -0.00 | -0.00 |
| 126 | 20700 | 2026-08-24 00:05:17 | LONG | 95.20 | 7.98 | 7.91 | 12.02 | 2.00 | LONG | 50 | -0.25 |  | 95.39 08-24 17:00 | be | -0.00 | -0.00 |
| 127 | 20701 | 2026-08-24 00:10:13 | LONG | 95.16 | 7.98 | 7.91 | 12.02 | 2.50 | LONG | 50 | -0.25 |  | 95.35 08-24 17:00 | be | -0.00 | -0.00 |
| 128 | 20702 | 2026-08-24 00:20:15 | LONG | 94.91 | 7.86 | 7.75 | 12.14 | 4.25 | LONG | 50 | -0.25 |  | 95.44 08-24 17:00 | trail | +0.12 | +0.36 |
| 129 | 20703 | 2026-08-24 00:25:15 | LONG | 94.84 | 7.86 | 8.58 | 12.14 | 5.00 | LONG | 50 | -0.25 |  | 95.27 08-24 17:00 | trail | +0.08 | +0.26 |
| 130 | 20718 | 2026-08-24 01:20:22 | LONG | 94.80 | 8.93 | 8.93 | 11.07 | 3.75 | LONG | 88 | +0.38 |  | 95.28 08-24 17:00 | trail | +0.10 | +0.31 |
| 131 | 20719 | 2026-08-24 01:30:13 | LONG | 94.44 | 8.93 | 8.93 | 11.07 | 3.50 | LONG | 88 | +0.38 |  | 94.63 08-24 13:40 | be | -0.00 | -0.00 |
| 132 | 20720 | 2026-08-24 01:35:10 | LONG | 94.59 | 8.93 | 8.93 | 11.07 | 3.50 | LONG | 88 | +0.38 |  | 95.24 08-24 17:00 | trail | +0.15 | +0.48 |
| 133 | 20721 | 2026-08-24 01:40:14 | LONG | 94.38 | 8.93 | 8.93 | 11.07 | 3.50 | LONG | 88 | +0.38 |  | 94.57 08-24 13:40 | be | -0.00 | -0.00 |
| 134 | 20722 | 2026-08-24 01:45:15 | LONG | 94.19 | 8.93 | 8.93 | 11.07 | 3.50 | LONG | 88 | +0.38 |  | 94.38 08-24 13:45 | be | -0.00 | -0.00 |
| 135 | 20726 | 2026-08-24 02:05:10 | LONG | 93.97 | 9.36 | 9.36 | 10.64 | 4.50 | LONG | 70 | +0.35 |  | 94.16 08-24 12:15 | be | -0.00 | -0.00 |
| 136 | 20727 | 2026-08-24 02:20:22 | LONG | 94.62 | 9.36 | 9.36 | 10.64 | 4.25 | LONG | 70 | +0.35 |  | 95.20 08-24 17:00 | trail | +0.13 | +0.42 |
| 137 | 20728 | 2026-08-24 02:25:39 | LONG | 94.72 | 9.36 | 9.36 | 10.64 | 4.25 | LONG | 70 | +0.35 |  | 95.20 08-24 17:00 | trail | +0.09 | +0.30 |
| 138 | 20730 | 2026-08-24 02:30:11 | LONG | 94.80 | 9.36 | 9.36 | 10.64 | 3.75 | LONG | 70 | +0.35 |  | 94.99 08-24 17:20 | be | -0.00 | -0.00 |
| 139 | 20732 | 2026-08-24 03:35:12 | LONG | 93.85 | 9.93 | 9.92 | 10.07 | 2.00 | LONG | 68 | +0.43 |  | 94.04 08-24 12:15 | be | -0.00 | -0.00 |
| 140 | 20738 | 2026-08-24 04:55:15 | LONG | 94.00 | 10.45 | 10.45 | 9.55 | 3.75 | LONG | 54 | +0.57 |  | 94.19 08-24 12:15 | be | -0.00 | -0.00 |
| 141 | 20742 | 2026-08-24 05:20:13 | LONG | 94.27 | 10.43 | 10.43 | 9.57 | 3.75 | LONG | 43 | +0.53 |  | 94.46 08-24 13:45 | be | -0.00 | -0.00 |
| 142 | 20745 | 2026-08-24 05:25:14 | LONG | 94.02 | 10.43 | 10.43 | 9.57 | 4.50 | LONG | 43 | +0.53 |  | 94.21 08-24 12:15 | be | -0.00 | -0.00 |
| 143 | 20746 | 2026-08-24 05:35:15 | LONG | 93.62 | 10.43 | 10.43 | 9.57 | 3.50 | LONG | 43 | +0.53 |  | 94.00 08-24 12:15 | trail | +0.06 | +0.21 |
| 144 | 20751 | 2026-08-24 05:40:10 | LONG | 93.91 | 10.43 | 10.43 | 9.57 | 4.25 | LONG | 43 | +0.53 |  | 94.10 08-24 12:15 | be | -0.00 | -0.00 |
| 145 | 20756 | 2026-08-24 06:40:15 | SHORT | 93.88 | 10.40 | 10.40 | 9.60 | 1.75 | SHORT | 70 | -0.03 |  | 96.87 08-24 15:20 | sl | -1.06 | -3.39 |
| 146 | 20772 | 2026-08-24 07:45:13 | LONG | 93.98 | 10.03 | 10.03 | 9.97 | 3.75 | LONG | 54 | -0.02 |  | 94.17 08-24 12:15 | be | -0.00 | -0.00 |
| 147 | 20773 | 2026-08-24 07:50:16 | LONG | 94.16 | 10.03 | 10.03 | 9.97 | 3.75 | LONG | 54 | -0.02 |  | 94.35 08-24 13:45 | be | -0.00 | -0.00 |
| 148 | 20774 | 2026-08-24 08:00:23 | LONG | 94.09 | 9.69 | 9.64 | 10.31 | 3.25 | LONG | 80 | -0.37 |  | 94.28 08-24 12:15 | be | -0.00 | -0.00 |
| 149 | 20775 | 2026-08-24 08:05:08 | LONG | 94.00 | 9.69 | 9.64 | 10.31 | 3.75 | LONG | 80 | -0.37 |  | 94.19 08-24 12:15 | be | -0.00 | -0.00 |
| 150 | 20776 | 2026-08-24 08:10:17 | LONG | 94.09 | 9.64 | 9.64 | 10.36 | 3.00 | LONG | 80 | -0.37 |  | 94.28 08-24 12:15 | be | -0.00 | -0.00 |
| 151 | 20786 | 2026-08-24 08:30:14 | LONG | 93.40 | 9.82 | 9.82 | 10.18 | 2.50 | LONG | 80 | -0.37 |  | 94.02 08-24 12:15 | trail | +0.14 | +0.46 |
| 152 | 20787 | 2026-08-24 08:35:10 | LONG | 93.52 | 9.82 | 9.82 | 10.18 | 2.50 | LONG | 80 | -0.37 |  | 94.02 08-24 12:15 | trail | +0.10 | +0.33 |
| 153 | 20790 | 2026-08-24 08:45:14 | LONG | 93.97 | 9.82 | 9.82 | 10.18 | 2.50 | LONG | 80 | -0.37 |  | 94.16 08-24 12:15 | be | -0.00 | -0.00 |
| 154 | 20801 | 2026-08-24 10:15:11 | LONG | 94.91 | 9.02 | 9.02 | 10.98 | 2.50 | NEUTRAL | 44 | -0.56 |  | 95.39 08-24 17:00 | trail | +0.10 | +0.30 |
| 155 | 20804 | 2026-08-24 10:25:14 | LONG | 94.82 | 9.02 | 9.02 | 10.98 | 1.75 | SHORT | 44 | -0.56 |  | 95.38 08-24 17:00 | trail | +0.13 | +0.39 |
| 156 | 20805 | 2026-08-24 10:30:19 | LONG | 94.85 | 9.02 | 9.02 | 10.98 | 1.75 | SHORT | 44 | -0.56 |  | 95.39 08-24 17:00 | trail | +0.12 | +0.36 |
| 157 | 20806 | 2026-08-24 10:35:08 | LONG | 94.91 | 9.02 | 9.02 | 10.98 | 1.75 | SHORT | 44 | -0.56 |  | 95.39 08-24 17:00 | trail | +0.10 | +0.30 |
| 158 | 20807 | 2026-08-24 10:40:21 | LONG | 94.77 | 9.02 | 9.02 | 10.98 | 1.75 | LONG | 44 | -0.56 |  | 95.38 08-24 17:00 | trail | +0.15 | +0.45 |
| 159 | 20817 | 2026-08-24 11:25:21 | SHORT | 94.88 | 8.40 | 8.40 | 11.60 | 2.50 | SHORT | 58 | -0.24 |  | 97.72 08-24 22:00 | sl | -1.07 | -3.19 |
| 160 | 20829 | 2026-08-24 11:45:18 | SHORT | 96.19 | 9.74 | 10.03 | 10.26 | 5.50 | SHORT | 58 | -0.24 |  | 99.29 08-25 00:05 | sl | -1.06 | -3.42 |
| 161 | 20831 | 2026-08-24 11:45:16 | SHORT | 96.19 | 9.74 | 10.03 | 10.26 | 3.75 | SHORT | 58 | -0.24 |  | 99.29 08-25 00:05 | sl | -1.06 | -3.42 |
| 162 | 20833 | 2026-08-24 11:55:19 | SHORT | 95.62 | 10.03 | 10.03 | 9.97 | 3.00 | SHORT | 58 | -0.24 |  | 98.72 08-24 22:35 | sl | -1.06 | -3.44 |
| 163 | 20834 | 2026-08-24 12:05:18 | SHORT | 95.38 | 10.97 | 10.97 | 9.03 | 3.00 | SHORT | 88 | +1.01 |  | 98.34 08-24 22:30 | sl | -1.07 | -3.30 |
| 164 | 20835 | 2026-08-24 12:10:11 | SHORT | 95.52 | 10.97 | 10.97 | 9.03 | 3.75 | SHORT | 88 | +1.01 |  | 98.50 08-24 22:35 | sl | -1.07 | -3.33 |
| 165 | 20843 | 2026-08-24 12:55:18 | SHORT | 96.31 | 11.27 | 11.27 | 8.73 | 4.25 | SHORT | 88 | +1.01 |  | 99.69 08-25 00:05 | sl | -1.06 | -3.71 |
| 166 | 20845 | 2026-08-24 13:00:17 | SHORT | 96.12 | 12.41 | 12.41 | 7.59 | 4.25 | SHORT | 92 | +1.24 |  | 99.34 08-25 00:05 | sl | -1.06 | -3.55 |
| 167 | 20846 | 2026-08-24 13:15:21 | SHORT | 96.23 | 12.41 | 12.41 | 7.59 | 4.25 | SHORT | 92 | +1.24 |  | 99.49 08-25 00:05 | sl | -1.06 | -3.59 |
| 168 | 20848 | 2026-08-24 13:20:18 | SHORT | 96.20 | 12.41 | 12.41 | 7.59 | 6.75 | SHORT | 92 | +1.24 |  | 99.46 08-25 00:05 | sl | -1.06 | -3.60 |
| 169 | 20849 | 2026-08-24 13:30:18 | SHORT | 95.88 | 12.41 | 12.41 | 7.59 | 4.25 | SHORT | 92 | +1.24 |  | 99.28 08-25 00:05 | sl | -1.06 | -3.75 |
| 170 | 20850 | 2026-08-24 13:35:28 | SHORT | 95.47 | 12.41 | 12.41 | 7.59 | 3.75 | SHORT | 92 | +1.24 |  | 98.87 08-24 23:55 | sl | -1.06 | -3.77 |
| 171 | 20852 | 2026-08-24 13:40:14 | SHORT | 95.22 | 12.41 | 12.41 | 7.59 | 6.75 | SHORT | 92 | +1.24 |  | 98.73 08-24 22:35 | sl | -1.06 | -3.89 |
| 172 | 20854 | 2026-08-24 13:45:20 | SHORT | 94.69 | 12.41 | 12.41 | 7.59 | 4.25 | SHORT | 92 | +1.24 |  | 98.24 08-24 22:30 | sl | -1.05 | -3.96 |
| 173 | 20855 | 2026-08-24 14:05:15 | SHORT | 95.00 | 13.48 | 13.48 | 6.52 | 3.50 | SHORT | 88 | +1.15 |  | 98.39 08-24 22:35 | sl | -1.06 | -3.77 |
| 174 | 20858 | 2026-08-24 14:35:13 | SHORT | 96.27 | 13.48 | 13.48 | 6.52 | 3.00 | SHORT | 88 | +1.15 |  | 99.88 08-25 00:05 | sl | -1.05 | -3.95 |
| 175 | 20860 | 2026-08-24 14:40:37 | SHORT | 96.44 | 13.48 | 13.60 | 6.52 | 3.75 | SHORT | 88 | +1.15 |  | 100.07 08-25 00:05 | sl | -1.05 | -3.97 |
| 176 | 20874 | 2026-08-24 15:45:23 | LONG | 96.25 | 15.41 | 15.41 | 4.59 | 3.75 | LONG | 87 | +1.19 |  | 100.26 08-25 07:50 | trail | +1.04 | +3.96 |
| 177 | 20877 | 2026-08-24 16:00:30 | LONG | 96.62 | 17.09 | 17.09 | 2.91 | 1.75 | LONG | 88 | +1.81 |  | 100.09 08-25 01:50 | trail | +0.94 | +3.39 |
| 178 | 20878 | 2026-08-24 16:25:19 | LONG | 97.16 | 17.09 | 17.09 | 2.91 | 1.75 | LONG | 88 | +1.81 |  | 100.34 08-25 07:50 | trail | +0.83 | +3.07 |
| 179 | 20880 | 2026-08-24 16:45:17 | LONG | 96.75 | 17.09 | 17.09 | 2.91 | 4.25 | LONG | 88 | +1.81 |  | 100.33 08-25 07:50 | trail | +0.94 | +3.50 |
| 180 | 20884 | 2026-08-24 16:55:22 | LONG | 95.97 | 16.62 | 16.62 | 3.38 | 4.25 | LONG | 88 | +1.81 |  | 100.19 08-25 07:50 | trail | +1.07 | +4.19 |
| 181 | 20888 | 2026-08-24 17:05:19 | LONG | 95.66 | 16.98 | 16.98 | 3.02 | 4.25 | LONG | 79 | +1.21 |  | 100.25 08-25 07:50 | trail | +1.21 | +4.60 |
| 182 | 20890 | 2026-08-24 17:10:18 | LONG | 96.00 | 16.98 | 16.98 | 3.02 | 4.25 | LONG | 79 | +1.21 |  | 100.26 08-25 07:50 | trail | +1.11 | +4.24 |
| 183 | 20895 | 2026-08-24 18:10:21 | LONG | 95.81 | 16.18 | 16.18 | 3.82 | 1.75 | LONG | 92 | -0.23 |  | 100.31 08-25 07:50 | trail | +1.20 | +4.49 |
| 184 | 20897 | 2026-08-24 18:15:24 | LONG | 95.98 | 16.18 | 16.39 | 3.82 | 3.50 | LONG | 92 | -0.23 |  | 100.26 08-25 07:50 | trail | +1.12 | +4.26 |
| 185 | 20898 | 2026-08-24 18:20:12 | LONG | 96.12 | 16.18 | 16.39 | 3.82 | 3.50 | LONG | 92 | -0.23 |  | 100.27 08-25 07:50 | trail | +1.08 | +4.11 |
| 186 | 20899 | 2026-08-24 18:25:31 | LONG | 96.09 | 16.39 | 16.39 | 3.61 | 3.50 | LONG | 92 | -0.23 |  | 100.27 08-25 07:50 | trail | +1.09 | +4.14 |
| 187 | 20900 | 2026-08-24 18:30:19 | LONG | 96.28 | 16.39 | 16.39 | 3.61 | 3.50 | LONG | 92 | -0.23 |  | 100.27 08-25 07:50 | trail | +1.04 | +3.94 |
| 188 | 20902 | 2026-08-24 18:35:36 | LONG | 96.09 | 16.39 | 16.39 | 3.61 | 4.75 | LONG | 92 | -0.23 |  | 100.27 08-25 07:50 | trail | +1.09 | +4.14 |
| 189 | 20910 | 2026-08-24 20:40:14 | SHORT | 96.50 | 16.89 | 16.89 | 3.11 | 2.50 | SHORT | 73 | +0.21 |  | 100.04 08-25 00:05 | sl | -1.06 | -3.88 |
| 190 | 20915 | 2026-08-24 21:10:17 | LONG | 96.72 | 17.30 | 17.43 | 2.70 | 4.25 | LONG | 48 | +0.29 |  | 100.17 08-25 01:50 | trail | +0.96 | +3.36 |
| 191 | 20920 | 2026-08-24 21:55:09 | LONG | 97.25 | 17.73 | 17.92 | 2.27 | 1.75 | LONG | 48 | +0.29 |  | 100.11 08-25 01:50 | trail | +0.76 | +2.74 |
| 192 | 20927 | 2026-08-24 22:35:13 | LONG | 98.16 | 19.44 | 19.70 | 0.56 | 2.25 | LONG | 43 | +1.03 |  | 100.10 08-25 01:50 | trail | +0.50 | +1.78 |
| 193 | 20929 | 2026-08-24 22:40:16 | LONG | 98.22 | 19.70 | 19.70 | 0.30 | 1.75 | LONG | 43 | +1.03 |  | 100.10 08-25 01:50 | trail | +0.48 | +1.72 |
| 194 | 21923 | 2026-08-29 01:55:09 | SHORT | 104.15 | 19.77 | 19.77 | 0.23 | 2.00 | SHORT | 13 | -0.89 | YES | 102.70 08-31 05:20 | trail | +0.36 | +1.19 |
| 195 | 21925 | 2026-08-29 02:05:08 | SHORT | 104.15 | 19.06 | 19.06 | 0.94 | 2.00 | SHORT | 11 | -0.77 |  | 107.40 08-30 13:50 | sl | -1.07 | -3.32 |
| 196 | 21928 | 2026-08-29 02:25:09 | SHORT | 103.84 | 19.06 | 19.14 | 0.94 | 2.50 | SHORT | 11 | -0.77 |  | 107.18 08-30 13:45 | sl | -1.06 | -3.42 |
| 197 | 21935 | 2026-08-29 03:00:17 | SHORT | 103.88 | 18.71 | 18.71 | 1.29 | 2.00 | SHORT | 14 | -0.55 |  | 107.01 08-30 13:35 | sl | -1.07 | -3.22 |
| 198 | 21939 | 2026-08-29 03:45:14 | SHORT | 104.06 | 18.71 | 18.71 | 1.29 | 2.00 | SHORT | 14 | -0.55 |  | 107.24 08-30 13:45 | sl | -1.07 | -3.26 |
| 199 | 21943 | 2026-08-29 04:10:14 | SHORT | 103.59 | 18.53 | 18.53 | 1.47 | 2.50 | SHORT | 9 | -0.51 |  | 106.62 08-30 13:30 | sl | -1.07 | -3.13 |
| 200 | 21946 | 2026-08-29 04:55:13 | SHORT | 103.94 | 18.58 | 18.58 | 1.42 | 2.00 | SHORT | 9 | -0.51 |  | 107.01 08-30 13:35 | sl | -1.07 | -3.15 |
| 201 | 21950 | 2026-08-29 05:15:12 | SHORT | 104.06 | 18.43 | 18.30 | 1.57 | 2.50 | SHORT | 12 | -0.13 |  | 106.97 08-30 13:35 | sl | -1.07 | -3.00 |
| 202 | 21951 | 2026-08-29 05:20:12 | SHORT | 104.12 | 18.29 | 18.29 | 1.71 | 2.50 | SHORT | 12 | -0.13 |  | 107.03 08-30 13:35 | sl | -1.07 | -3.00 |
| 203 | 21960 | 2026-08-29 06:15:13 | LONG | 103.41 | 18.42 | 18.42 | 1.58 | 2.50 | LONG | 2 | -0.29 | YES | 105.24 08-30 17:20 | trail | +0.57 | +1.57 |
| 204 | 21962 | 2026-08-29 06:25:12 | SHORT | 103.40 | 18.50 | 18.50 | 1.50 | 2.50 | NEUTRAL | 2 | -0.29 |  | 106.24 08-30 13:15 | sl | -1.07 | -2.95 |
| 205 | 21963 | 2026-08-29 06:25:12 | LONG | 103.40 | 18.50 | 18.50 | 1.50 | 2.50 | LONG | 2 | -0.29 |  | 105.22 08-30 17:20 | trail | +0.57 | +1.56 |
| 206 | 21968 | 2026-08-29 07:40:12 | SHORT | 103.81 | 18.70 | 18.70 | 1.30 | 2.00 | SHORT | 4 | +0.21 |  | 106.52 08-30 13:30 | sl | -1.08 | -2.81 |
| 207 | 21969 | 2026-08-29 07:55:11 | LONG | 103.60 | 18.70 | 18.70 | 1.30 | 2.50 | LONG | 4 | +0.21 |  | 105.33 08-30 17:20 | trail | +0.56 | +1.46 |
| 208 | 21973 | 2026-08-29 08:10:12 | LONG | 103.28 | 19.16 | 19.16 | 0.84 | 5.00 | LONG | 2 | +0.20 |  | 105.40 08-30 17:20 | trail | +0.74 | +1.85 |
| 209 | 21975 | 2026-08-29 08:35:13 | LONG | 103.30 | 19.19 | 19.19 | 0.81 | 3.25 | LONG | 2 | +0.20 |  | 105.40 08-30 17:20 | trail | +0.73 | +1.83 |
| 210 | 21977 | 2026-08-29 08:40:13 | LONG | 103.30 | 19.19 | 19.20 | 0.81 | 2.50 | LONG | 2 | +0.20 |  | 105.40 08-30 17:20 | trail | +0.73 | +1.83 |
| 211 | 21988 | 2026-08-29 09:40:14 | SHORT | 103.44 | 19.92 | 19.92 | 0.08 | 2.50 | SHORT | 6 | +0.63 |  | 105.94 08-30 12:55 | sl | -1.08 | -2.62 |
| 212 | 21990 | 2026-08-29 09:45:21 | LONG | 103.41 | 19.92 | 19.92 | 0.08 | 2.50 | NEUTRAL | 6 | +0.63 |  | 105.48 08-30 17:20 | trail | +0.74 | +1.80 |
| 213 | 21991 | 2026-08-29 09:50:11 | LONG | 103.41 | 19.92 | 19.92 | 0.08 | 2.00 | SHORT | 6 | +0.63 |  | 105.48 08-30 17:20 | trail | +0.74 | +1.80 |
| 214 | 21992 | 2026-08-29 09:55:12 | LONG | 103.40 | 19.92 | 19.92 | 0.08 | 2.00 | SHORT | 6 | +0.63 |  | 105.48 08-30 17:20 | trail | +0.75 | +1.81 |
| 215 | 22100 | 2026-08-29 15:00:32 | LONG | 105.30 | 19.62 | 19.62 | 0.38 | 4.25 | LONG | 76 | -0.79 |  | 105.51 08-30 17:20 | be | -0.00 | -0.00 |
| 216 | 22103 | 2026-08-29 15:05:25 | LONG | 105.05 | 19.62 | 19.62 | 0.38 | 4.25 | LONG | 76 | -0.79 |  | 105.26 08-30 17:20 | be | -0.00 | -0.00 |
| 217 | 22153 | 2026-08-29 18:55:15 | LONG | 105.16 | 16.66 | 16.66 | 3.34 | 4.25 | LONG | 10 | -1.30 |  | 105.37 08-30 17:20 | be | -0.00 | -0.00 |
| 218 | 22158 | 2026-08-29 19:10:23 | LONG | 105.18 | 15.83 | 16.14 | 4.17 | 6.00 | LONG | 28 | -0.97 |  | 105.39 08-30 17:20 | be | -0.00 | -0.00 |
| 219 | 22161 | 2026-08-29 19:15:27 | LONG | 105.45 | 16.14 | 16.49 | 3.86 | 4.25 | LONG | 28 | -0.97 |  | 105.66 08-30 17:20 | be | -0.00 | -0.00 |
| 220 | 22164 | 2026-08-29 19:20:21 | LONG | 105.63 | 16.14 | 16.49 | 3.86 | 6.00 | LONG | 28 | -0.97 |  | 105.84 08-30 17:20 | be | -0.00 | -0.00 |
| 221 | 22166 | 2026-08-29 19:25:24 | LONG | 105.59 | 16.49 | 16.49 | 3.51 | 6.75 | LONG | 28 | -0.97 |  | 105.80 08-30 17:20 | be | -0.00 | -0.00 |
| 222 | 22168 | 2026-08-29 19:30:17 | LONG | 105.69 | 16.49 | 16.49 | 3.51 | 5.50 | LONG | 28 | -0.97 |  | 105.90 08-30 15:15 | be | -0.00 | -0.00 |
| 223 | 22179 | 2026-08-29 21:05:18 | SHORT | 104.94 | 15.87 | 15.87 | 4.13 | 4.25 | SHORT | 7 | -0.25 |  | 106.95 08-30 13:35 | sl | -1.11 | -2.12 |
| 224 | 22180 | 2026-08-29 21:10:15 | SHORT | 105.12 | 15.87 | 15.87 | 4.13 | 4.25 | SHORT | 7 | -0.25 |  | 107.15 08-30 13:40 | sl | -1.10 | -2.14 |
| 225 | 22182 | 2026-08-29 21:15:15 | SHORT | 105.20 | 15.87 | 15.87 | 4.13 | 4.25 | SHORT | 7 | -0.25 |  | 107.23 08-30 13:45 | sl | -1.10 | -2.13 |
| 226 | 22184 | 2026-08-29 21:25:14 | SHORT | 105.02 | 15.87 | 15.87 | 4.13 | 4.25 | SHORT | 7 | -0.25 |  | 107.05 08-30 13:40 | sl | -1.10 | -2.14 |
| 227 | 22185 | 2026-08-29 21:30:13 | SHORT | 104.94 | 15.87 | 15.76 | 4.13 | 3.50 | SHORT | 7 | -0.25 |  | 106.99 08-30 13:35 | sl | -1.10 | -2.15 |
| 228 | 22187 | 2026-08-29 21:35:09 | SHORT | 104.90 | 15.87 | 15.76 | 4.13 | 3.50 | SHORT | 7 | -0.25 |  | 106.95 08-30 13:35 | sl | -1.10 | -2.15 |
| 229 | 22188 | 2026-08-29 21:40:25 | SHORT | 104.91 | 15.53 | 15.53 | 4.47 | 4.25 | SHORT | 7 | -0.25 |  | 106.98 08-30 13:35 | sl | -1.10 | -2.18 |
| 230 | 22193 | 2026-08-29 22:35:12 | SHORT | 105.12 | 14.87 | 14.87 | 5.13 | 2.00 | SHORT | 28 | -0.71 |  | 107.11 08-30 13:40 | sl | -1.11 | -2.10 |
| 231 | 22211 | 2026-08-30 00:15:08 | SHORT | 105.28 | 14.64 | 14.64 | 5.36 | 1.75 | SHORT | 10 | -0.05 |  | 107.20 08-30 13:45 | sl | -1.11 | -2.03 |
| 232 | 22212 | 2026-08-30 00:20:07 | SHORT | 105.52 | 14.64 | 14.64 | 5.36 | 4.25 | SHORT | 10 | -0.05 |  | 102.43 08-30 23:25 | trail | +1.50 | +2.73 |
| 233 | 22213 | 2026-08-30 00:30:16 | SHORT | 105.30 | 14.64 | 14.64 | 5.36 | 3.50 | SHORT | 10 | -0.05 |  | 107.22 08-30 13:45 | sl | -1.11 | -2.03 |
| 234 | 22214 | 2026-08-30 00:35:10 | SHORT | 105.27 | 14.64 | 14.64 | 5.36 | 6.00 | SHORT | 10 | -0.05 |  | 107.19 08-30 13:45 | sl | -1.11 | -2.03 |
| 235 | 22215 | 2026-08-30 00:40:11 | SHORT | 105.28 | 14.64 | 14.59 | 5.36 | 3.50 | SHORT | 10 | -0.05 |  | 107.21 08-30 13:45 | sl | -1.11 | -2.03 |
| 236 | 22218 | 2026-08-30 00:45:11 | SHORT | 105.22 | 14.64 | 14.59 | 5.36 | 3.50 | SHORT | 10 | -0.05 |  | 107.15 08-30 13:40 | sl | -1.11 | -2.03 |
| 237 | 22219 | 2026-08-30 00:50:14 | SHORT | 105.40 | 14.59 | 14.59 | 5.41 | 3.50 | SHORT | 10 | -0.05 |  | 107.33 08-30 13:45 | sl | -1.11 | -2.03 |
| 238 | 22220 | 2026-08-30 00:55:11 | SHORT | 105.32 | 14.59 | 14.59 | 5.41 | 3.50 | SHORT | 10 | -0.05 |  | 107.25 08-30 13:45 | sl | -1.11 | -2.03 |
| 239 | 22221 | 2026-08-30 01:00:18 | SHORT | 105.19 | 14.16 | 14.12 | 5.84 | 3.50 | SHORT | 17 | -0.46 |  | 107.01 08-30 13:35 | sl | -1.12 | -1.93 |
| 240 | 22222 | 2026-08-30 01:05:08 | SHORT | 105.25 | 14.16 | 14.10 | 5.84 | 3.50 | SHORT | 17 | -0.46 |  | 107.07 08-30 13:40 | sl | -1.12 | -1.93 |
| 241 | 22223 | 2026-08-30 01:10:16 | SHORT | 105.15 | 14.10 | 14.03 | 5.90 | 3.50 | SHORT | 17 | -0.46 |  | 106.98 08-30 13:35 | sl | -1.12 | -1.94 |
| 242 | 22226 | 2026-08-30 01:15:16 | SHORT | 105.15 | 14.03 | 13.99 | 5.97 | 4.25 | SHORT | 17 | -0.46 |  | 106.98 08-30 13:35 | sl | -1.12 | -1.95 |
| 243 | 22227 | 2026-08-30 01:20:10 | SHORT | 105.16 | 14.03 | 13.99 | 5.97 | 4.25 | SHORT | 17 | -0.46 |  | 107.00 08-30 13:35 | sl | -1.12 | -1.95 |
| 244 | 22228 | 2026-08-30 01:25:13 | SHORT | 105.23 | 13.99 | 13.99 | 6.01 | 3.50 | SHORT | 17 | -0.46 |  | 107.07 08-30 13:40 | sl | -1.12 | -1.95 |
| 245 | 22229 | 2026-08-30 01:30:16 | SHORT | 105.09 | 13.99 | 13.79 | 6.01 | 3.50 | SHORT | 17 | -0.46 |  | 106.95 08-30 13:35 | sl | -1.11 | -1.97 |
| 246 | 22230 | 2026-08-30 01:35:21 | SHORT | 105.06 | 13.79 | 13.79 | 6.21 | 4.25 | SHORT | 17 | -0.46 |  | 106.92 08-30 13:35 | sl | -1.11 | -1.97 |
| 247 | 22233 | 2026-08-30 02:10:12 | SHORT | 105.28 | 13.18 | 13.18 | 6.82 | 2.00 | SHORT | 4 | -0.80 |  | 107.05 08-30 13:40 | sl | -1.12 | -1.89 |
| 248 | 22239 | 2026-08-30 03:10:13 | LONG | 105.03 | 12.31 | 12.31 | 7.69 | 3.75 | LONG | 2 | -0.55 |  | 106.12 08-30 15:10 | trail | +0.52 | +0.84 |
| 249 | 22242 | 2026-08-30 04:10:12 | LONG | 104.91 | 11.45 | 11.45 | 8.55 | 2.00 | LONG | 1 | -0.93 |  | 106.17 08-30 15:10 | trail | +0.64 | +1.00 |
| 250 | 22245 | 2026-08-30 04:20:09 | LONG | 104.93 | 11.52 | 11.52 | 8.48 | 4.25 | LONG | 1 | -0.93 |  | 106.16 08-30 15:10 | trail | +0.62 | +0.97 |
| 251 | 22247 | 2026-08-30 04:25:07 | LONG | 104.93 | 11.52 | 11.52 | 8.48 | 4.25 | LONG | 1 | -0.93 |  | 106.16 08-30 15:10 | trail | +0.62 | +0.97 |
| 252 | 22248 | 2026-08-30 04:35:09 | LONG | 104.84 | 11.52 | 11.63 | 8.48 | 4.25 | LONG | 1 | -0.93 |  | 106.16 08-30 15:10 | trail | +0.67 | +1.06 |
| 253 | 22250 | 2026-08-30 04:40:11 | LONG | 104.78 | 11.63 | 11.63 | 8.37 | 2.50 | LONG | 1 | -0.93 |  | 106.16 08-30 15:10 | trail | +0.70 | +1.11 |
| 254 | 22253 | 2026-08-30 04:45:12 | LONG | 104.80 | 11.63 | 11.92 | 8.37 | 2.50 | LONG | 1 | -0.93 |  | 106.13 08-30 15:10 | trail | +0.66 | +1.07 |
| 255 | 22254 | 2026-08-30 04:50:11 | LONG | 104.66 | 11.63 | 11.92 | 8.37 | 2.50 | LONG | 1 | -0.93 |  | 106.13 08-30 15:10 | trail | +0.74 | +1.20 |
| 256 | 22257 | 2026-08-30 05:00:08 | LONG | 104.98 | 11.92 | 11.30 | 8.08 | 2.50 | LONG | 10 | -0.40 |  | 106.19 08-30 15:10 | trail | +0.62 | +0.95 |
| 257 | 22258 | 2026-08-30 05:05:09 | SHORT | 105.18 | 11.30 | 11.30 | 8.70 | 2.00 | SHORT | 10 | -0.40 |  | 106.79 08-30 13:30 | sl | -1.13 | -1.73 |
| 258 | 22260 | 2026-08-30 05:10:14 | SHORT | 105.07 | 11.30 | 11.30 | 8.70 | 2.50 | SHORT | 10 | -0.40 |  | 106.68 08-30 13:30 | sl | -1.13 | -1.74 |
| 259 | 22266 | 2026-08-30 07:00:12 | LONG | 105.34 | 9.94 | 9.96 | 10.06 | 3.50 | LONG | 2 | -0.71 |  | 106.26 08-30 15:10 | trail | +0.46 | +0.67 |
| 260 | 22269 | 2026-08-30 07:05:14 | LONG | 105.22 | 9.96 | 9.96 | 10.04 | 2.50 | LONG | 2 | -0.71 |  | 106.26 08-30 15:10 | trail | +0.54 | +0.78 |
| 261 | 22271 | 2026-08-30 07:05:14 | SHORT | 105.22 | 9.96 | 9.96 | 10.04 | 2.50 | NEUTRAL | 2 | -0.71 |  | 106.75 08-30 13:30 | sl | -1.14 | -1.66 |
| 262 | 22272 | 2026-08-30 07:10:10 | SHORT | 105.16 | 9.96 | 9.96 | 10.04 | 2.50 | NEUTRAL | 2 | -0.71 |  | 106.69 08-30 13:30 | sl | -1.14 | -1.66 |
| 263 | 22278 | 2026-08-30 07:35:10 | LONG | 105.00 | 9.96 | 9.96 | 10.04 | 4.50 | LONG | 2 | -0.71 |  | 106.22 08-30 15:10 | trail | +0.64 | +0.96 |
| 264 | 22283 | 2026-08-30 07:50:09 | SHORT | 104.75 | 10.15 | 10.15 | 9.85 | 3.50 | SHORT | 2 | -0.71 |  | 106.37 08-30 13:20 | sl | -1.13 | -1.75 |
| 265 | 22327 | 2026-08-30 10:30:14 | SHORT | 104.82 | 10.51 | 10.51 | 9.49 | 2.00 | SHORT | 8 | +0.14 |  | 106.40 08-30 13:30 | sl | -1.13 | -1.71 |
| 266 | 22331 | 2026-08-30 10:45:15 | LONG | 105.00 | 10.30 | 10.04 | 9.70 | 3.50 | LONG | 8 | +0.14 |  | 106.18 08-30 15:10 | trail | +0.60 | +0.92 |
| 267 | 22352 | 2026-08-30 12:05:14 | SHORT | 105.23 | 8.63 | 9.50 | 11.37 | 4.25 | SHORT | 2 | -0.70 |  | 106.84 08-30 13:30 | sl | -1.13 | -1.73 |
| 268 | 22353 | 2026-08-30 12:10:11 | SHORT | 105.72 | 8.63 | 9.58 | 11.37 | 4.25 | SHORT | 2 | -0.70 |  | 107.34 08-30 13:45 | sl | -1.13 | -1.73 |
| 269 | 22359 | 2026-08-30 12:15:14 | SHORT | 105.57 | 9.58 | 9.58 | 10.42 | 4.25 | SHORT | 2 | -0.70 |  | 107.19 08-30 13:45 | sl | -1.13 | -1.73 |
| 270 | 22364 | 2026-08-30 12:20:11 | SHORT | 105.34 | 9.58 | 9.58 | 10.42 | 2.50 | SHORT | 2 | -0.70 |  | 106.96 08-30 13:35 | sl | -1.13 | -1.74 |
| 271 | 22366 | 2026-08-30 12:25:16 | SHORT | 105.31 | 9.58 | 9.58 | 10.42 | 2.50 | SHORT | 2 | -0.70 |  | 106.93 08-30 13:35 | sl | -1.13 | -1.74 |
| 272 | 22367 | 2026-08-30 12:30:15 | SHORT | 105.32 | 9.58 | 9.58 | 10.42 | 2.50 | SHORT | 2 | -0.70 |  | 106.94 08-30 13:35 | sl | -1.13 | -1.74 |
| 273 | 22369 | 2026-08-30 12:35:26 | SHORT | 105.28 | 9.58 | 9.58 | 10.42 | 2.50 | SHORT | 2 | -0.70 |  | 106.90 08-30 13:35 | sl | -1.13 | -1.74 |
| 274 | 22370 | 2026-08-30 12:35:39 | SHORT | 105.28 | 9.58 | 9.58 | 10.42 | 2.50 | SHORT | 2 | -0.70 |  | 106.90 08-30 13:35 | sl | -1.13 | -1.74 |
| 275 | 22371 | 2026-08-30 12:40:21 | SHORT | 105.34 | 9.58 | 9.58 | 10.42 | 2.50 | SHORT | 2 | -0.70 |  | 106.96 08-30 13:35 | sl | -1.13 | -1.74 |
| 276 | 22372 | 2026-08-30 12:45:22 | SHORT | 105.50 | 9.58 | 9.58 | 10.42 | 2.00 | SHORT | 2 | -0.70 |  | 107.12 08-30 13:40 | sl | -1.13 | -1.74 |
| 277 | 22374 | 2026-08-30 13:00:15 | LONG | 106.03 | 11.05 | 11.05 | 8.95 | 3.50 | LONG | 61 | +0.92 |  | 106.24 08-30 15:10 | be | -0.00 | -0.00 |
| 278 | 22395 | 2026-08-30 17:10:17 | LONG | 106.59 | 16.76 | 16.75 | 3.24 | 6.50 | LONG | 55 | +0.91 |  | 104.73 08-30 20:40 | sl | -1.11 | -1.95 |
| 279 | 22396 | 2026-08-30 17:20:11 | LONG | 106.22 | 16.76 | 15.28 | 3.24 | 8.50 | LONG | 55 | +0.91 | YES | 104.14 08-30 21:00 | sl | -1.10 | -2.16 |
| 280 | 22399 | 2026-08-30 17:25:09 | LONG | 105.43 | 16.76 | 15.28 | 3.24 | 6.50 | LONG | 55 | +0.91 |  | 103.35 08-30 21:00 | sl | -1.10 | -2.17 |
| 281 | 22424 | 2026-08-30 20:30:14 | LONG | 105.35 | 13.35 | 14.04 | 6.65 | 4.50 | LONG | 29 | -0.72 |  | 103.11 08-30 23:15 | sl | -1.09 | -2.33 |
| 282 | 22445 | 2026-08-30 21:05:13 | SHORT | 103.85 | 15.84 | 15.84 | 4.16 | 2.50 | SHORT | 66 | +0.54 |  | 101.95 08-30 23:55 | trail | +0.71 | +1.63 |
| 283 | 22449 | 2026-08-30 21:10:09 | SHORT | 104.06 | 15.84 | 15.84 | 4.16 | 2.50 | SHORT | 66 | +0.54 |  | 101.94 08-30 23:55 | trail | +0.79 | +1.84 |
| 284 | 22475 | 2026-08-30 23:10:15 | SHORT | 103.44 | 18.41 | 18.41 | 1.59 | 4.25 | SHORT | 53 | +1.33 |  | 101.94 08-30 23:55 | trail | +0.54 | +1.25 |
| 285 | 22477 | 2026-08-30 23:15:16 | SHORT | 103.44 | 18.41 | 18.88 | 1.59 | 4.25 | SHORT | 53 | +1.33 |  | 102.05 08-31 00:15 | trail | +0.47 | +1.14 |
| 286 | 22480 | 2026-08-30 23:20:11 | SHORT | 103.35 | 18.41 | 19.10 | 1.59 | 2.50 | SHORT | 53 | +1.33 |  | 102.10 08-31 00:15 | trail | +0.40 | +1.01 |
| 287 | 22488 | 2026-08-30 23:25:11 | SHORT | 102.56 | 19.10 | 19.68 | 0.90 | 2.50 | SHORT | 53 | +1.33 |  | 102.26 08-31 00:20 | trail | +0.03 | +0.09 |
| 288 | 22492 | 2026-08-30 23:30:14 | SHORT | 101.47 | 19.68 | 19.68 | 0.32 | 4.25 | SHORT | 53 | +1.33 |  | 104.27 08-31 18:35 | sl | -1.07 | -2.97 |
| 289 | 22493 | 2026-08-30 23:35:12 | SHORT | 101.94 | 19.68 | 19.68 | 0.32 | 6.75 | SHORT | 53 | +1.33 |  | 104.74 08-31 18:40 | sl | -1.07 | -2.95 |
| 290 | 22494 | 2026-08-30 23:40:12 | SHORT | 101.30 | 19.68 | 19.68 | 0.32 | 6.00 | SHORT | 53 | +1.33 |  | 104.10 08-31 11:15 | sl | -1.07 | -2.97 |
| 291 | 22495 | 2026-08-30 23:45:14 | SHORT | 101.38 | 19.68 | 20.01 | 0.32 | 5.50 | SHORT | 53 | +1.33 |  | 104.33 08-31 18:35 | sl | -1.07 | -3.12 |
| 292 | 22784 | 2026-08-31 23:05:15 | LONG | 102.94 | 17.87 | 17.87 | 2.13 | 5.00 | LONG | 3 | -1.11 | YES | 100.36 09-01 17:50 | sl | -1.08 | -2.71 |
| 293 | 22790 | 2026-09-01 00:15:20 | LONG | 103.16 | 16.60 | 16.87 | 3.40 | 4.25 | LONG | 8 | -1.29 |  | 100.67 09-01 16:35 | sl | -1.08 | -2.61 |
| 294 | 22792 | 2026-09-01 00:20:13 | LONG | 103.34 | 16.60 | 16.95 | 3.40 | 5.50 | LONG | 8 | -1.29 |  | 100.84 09-01 16:35 | sl | -1.08 | -2.62 |
| 295 | 22795 | 2026-09-01 01:00:18 | LONG | 103.15 | 16.24 | 16.24 | 3.76 | 7.00 | LONG | 12 | -0.85 |  | 100.78 09-01 16:35 | sl | -1.09 | -2.50 |
| 296 | 22796 | 2026-09-01 01:15:25 | LONG | 102.91 | 16.24 | 16.24 | 3.76 | 4.50 | LONG | 12 | -0.85 |  | 100.47 09-01 17:15 | sl | -1.08 | -2.57 |
| 297 | 22802 | 2026-09-01 01:30:12 | LONG | 102.88 | 15.86 | 15.86 | 4.14 | 5.00 | LONG | 12 | -0.85 |  | 100.39 09-01 17:50 | sl | -1.08 | -2.61 |
| 298 | 22804 | 2026-09-01 01:35:09 | LONG | 103.03 | 15.86 | 15.86 | 4.14 | 2.50 | LONG | 12 | -0.85 |  | 100.54 09-01 16:35 | sl | -1.08 | -2.61 |
| 299 | 22808 | 2026-09-01 02:05:13 | LONG | 103.12 | 14.77 | 14.77 | 5.23 | 2.00 | SHORT | 18 | -1.17 |  | 100.77 09-01 16:35 | sl | -1.09 | -2.48 |
| 300 | 22810 | 2026-09-01 02:15:10 | LONG | 102.98 | 14.77 | 14.77 | 5.23 | 2.50 | NEUTRAL | 18 | -1.17 |  | 100.58 09-01 16:35 | sl | -1.08 | -2.53 |
| 301 | 22813 | 2026-09-01 02:40:13 | LONG | 103.03 | 14.77 | 14.77 | 5.23 | 2.00 | LONG | 18 | -1.17 |  | 100.62 09-01 16:35 | sl | -1.08 | -2.54 |
| 302 | 22817 | 2026-09-01 03:35:10 | SHORT | 103.91 | 14.50 | 14.79 | 5.50 | 4.50 | SHORT | 2 | -1.08 | YES | 99.99 09-01 19:20 | trail | +1.53 | +3.57 |
| 303 | 22823 | 2026-09-01 03:40:10 | SHORT | 103.95 | 14.79 | 14.79 | 5.21 | 2.50 | SHORT | 2 | -1.08 |  | 99.99 09-01 19:20 | trail | +1.55 | +3.61 |
| 304 | 22827 | 2026-09-01 03:55:16 | SHORT | 103.59 | 14.79 | 14.79 | 5.21 | 2.50 | SHORT | 2 | -1.08 |  | 100.00 09-01 19:20 | trail | +1.40 | +3.27 |
| 305 | 22833 | 2026-09-01 05:05:14 | SHORT | 103.94 | 14.83 | 14.83 | 5.17 | 4.50 | SHORT | 9 | +0.02 |  | 99.89 09-01 19:00 | trail | +1.69 | +3.70 |
| 306 | 22834 | 2026-09-01 05:10:13 | SHORT | 103.94 | 14.83 | 14.83 | 5.17 | 4.25 | SHORT | 9 | +0.02 |  | 99.89 09-01 19:00 | trail | +1.69 | +3.70 |
| 307 | 22836 | 2026-09-01 05:30:19 | SHORT | 103.90 | 14.83 | 14.99 | 5.17 | 6.75 | SHORT | 9 | +0.02 |  | 99.91 09-01 19:00 | trail | +1.64 | +3.65 |
| 308 | 22837 | 2026-09-01 05:35:10 | SHORT | 104.07 | 14.83 | 15.00 | 5.17 | 7.25 | SHORT | 9 | +0.02 |  | 99.90 09-01 19:00 | trail | +1.72 | +3.81 |
| 309 | 22841 | 2026-09-01 05:40:14 | SHORT | 104.00 | 15.00 | 15.09 | 5.00 | 5.00 | SHORT | 9 | +0.02 |  | 99.91 09-01 19:00 | trail | +1.67 | +3.73 |
| 310 | 22843 | 2026-09-01 05:45:19 | SHORT | 104.19 | 15.09 | 15.24 | 4.91 | 4.25 | SHORT | 9 | +0.02 |  | 99.93 09-01 19:00 | trail | +1.73 | +3.89 |
| 311 | 22844 | 2026-09-01 05:50:13 | SHORT | 104.25 | 15.09 | 15.24 | 4.91 | 4.25 | SHORT | 9 | +0.02 |  | 99.93 09-01 19:00 | trail | +1.76 | +3.95 |
| 312 | 22845 | 2026-09-01 05:55:08 | SHORT | 104.25 | 15.24 | 15.24 | 4.76 | 4.25 | SHORT | 9 | +0.02 |  | 99.93 09-01 19:00 | trail | +1.76 | +3.95 |
| 313 | 22846 | 2026-09-01 06:00:23 | SHORT | 104.22 | 15.63 | 15.63 | 4.37 | 4.25 | SHORT | 19 | +0.42 |  | 99.82 09-01 19:00 | trail | +1.91 | +4.03 |
| 314 | 22848 | 2026-09-01 06:05:08 | SHORT | 104.19 | 15.63 | 15.63 | 4.37 | 4.25 | SHORT | 19 | +0.42 |  | 99.85 09-01 19:00 | trail | +1.86 | +3.97 |
| 315 | 22855 | 2026-09-01 06:50:13 | LONG | 103.68 | 15.63 | 15.63 | 4.37 | 1.75 | LONG | 19 | +0.42 |  | 101.38 09-01 12:40 | sl | -1.09 | -2.42 |
| 316 | 22856 | 2026-09-01 06:50:14 | LONG | 103.68 | 15.63 | 15.63 | 4.37 | 2.50 | LONG | 19 | +0.42 |  | 101.38 09-01 12:40 | sl | -1.09 | -2.42 |
| 317 | 22857 | 2026-09-01 06:55:10 | LONG | 103.53 | 15.63 | 15.19 | 4.37 | 2.50 | LONG | 19 | +0.42 |  | 101.18 09-01 15:05 | sl | -1.09 | -2.46 |
| 318 | 22859 | 2026-09-01 07:00:15 | LONG | 103.34 | 15.09 | 15.09 | 4.91 | 3.00 | LONG | 14 | -0.05 |  | 101.12 09-01 15:05 | sl | -1.09 | -2.34 |
| 319 | 22862 | 2026-09-01 07:05:13 | SHORT | 103.41 | 15.09 | 15.09 | 4.91 | 2.50 | NEUTRAL | 14 | -0.05 |  | 99.86 09-01 19:00 | trail | +1.50 | +3.24 |
| 320 | 22863 | 2026-09-01 07:05:13 | LONG | 103.41 | 15.09 | 15.09 | 4.91 | 2.50 | LONG | 14 | -0.05 |  | 101.18 09-01 15:05 | sl | -1.09 | -2.35 |
| 321 | 22864 | 2026-09-01 07:10:18 | LONG | 103.43 | 15.09 | 15.03 | 4.91 | 4.25 | LONG | 14 | -0.05 |  | 101.20 09-01 15:05 | sl | -1.09 | -2.35 |
| 322 | 22870 | 2026-09-01 08:05:14 | LONG | 103.05 | 13.24 | 13.39 | 6.76 | 2.00 | LONG | 41 | -1.01 |  | 100.78 09-01 16:35 | sl | -1.09 | -2.40 |
| 323 | 22873 | 2026-09-01 08:10:14 | LONG | 102.62 | 13.39 | 13.46 | 6.61 | 2.50 | LONG | 41 | -1.01 |  | 100.34 09-01 18:05 | sl | -1.09 | -2.42 |
| 324 | 22882 | 2026-09-01 08:40:12 | LONG | 102.12 | 14.27 | 14.39 | 5.73 | 1.75 | NEUTRAL | 41 | -1.01 |  | 99.70 09-01 18:10 | sl | -1.08 | -2.56 |
| 325 | 22883 | 2026-09-01 08:45:13 | SHORT | 102.16 | 14.39 | 14.39 | 5.61 | 3.50 | SHORT | 41 | -1.01 |  | 100.01 09-01 19:20 | trail | +0.81 | +1.91 |
| 326 | 22884 | 2026-09-01 08:50:07 | SHORT | 101.97 | 14.39 | 14.39 | 5.61 | 3.50 | SHORT | 41 | -1.01 |  | 100.01 09-01 19:20 | trail | +0.73 | +1.72 |
| 327 | 22885 | 2026-09-01 08:55:15 | SHORT | 102.10 | 14.39 | 14.39 | 5.61 | 3.50 | SHORT | 41 | -1.01 |  | 100.01 09-01 19:20 | trail | +0.78 | +1.85 |
| 328 | 22886 | 2026-09-01 09:00:15 | SHORT | 102.09 | 14.60 | 14.60 | 5.40 | 3.50 | SHORT | 72 | +0.22 |  | 99.93 09-01 19:00 | trail | +0.86 | +1.92 |
| 329 | 22924 | 2026-09-01 11:30:16 | SHORT | 102.09 | 13.57 | 13.57 | 6.43 | 6.00 | SHORT | 46 | -0.53 |  | 99.86 09-01 19:00 | trail | +0.92 | +1.99 |
| 330 | 22932 | 2026-09-01 12:35:16 | SHORT | 101.91 | 13.12 | 13.87 | 6.88 | 4.25 | SHORT | 24 | -0.49 |  | 99.91 09-01 19:00 | trail | +0.80 | +1.77 |
| 331 | 22937 | 2026-09-01 12:40:12 | SHORT | 101.40 | 13.12 | 13.94 | 6.88 | 4.25 | SHORT | 24 | -0.49 |  | 99.92 09-01 19:00 | trail | +0.56 | +1.26 |
| 332 | 22941 | 2026-09-01 12:45:11 | SHORT | 101.90 | 13.94 | 13.94 | 6.06 | 4.25 | SHORT | 24 | -0.49 |  | 99.91 09-01 19:00 | trail | +0.79 | +1.76 |
| 333 | 22943 | 2026-09-01 12:50:16 | SHORT | 102.00 | 13.94 | 13.94 | 6.06 | 4.25 | SHORT | 24 | -0.49 |  | 99.91 09-01 19:00 | trail | +0.83 | +1.85 |
| 334 | 22952 | 2026-09-01 13:50:17 | SHORT | 102.19 | 14.42 | 14.42 | 5.58 | 4.25 | SHORT | 54 | +0.36 |  | 99.94 09-01 19:15 | trail | +0.88 | +2.00 |
| 335 | 22953 | 2026-09-01 13:55:10 | SHORT | 101.91 | 14.42 | 14.42 | 5.58 | 6.25 | SHORT | 54 | +0.36 |  | 99.95 09-01 19:15 | trail | +0.76 | +1.73 |
| 336 | 22979 | 2026-09-01 15:45:16 | SHORT | 102.15 | 15.95 | 15.95 | 4.05 | 6.25 | SHORT | 66 | +0.28 |  | 99.97 09-01 19:20 | trail | +0.84 | +1.93 |
| 337 | 22981 | 2026-09-01 15:50:11 | SHORT | 102.22 | 15.95 | 15.95 | 4.05 | 6.75 | SHORT | 66 | +0.28 |  | 99.98 09-01 19:20 | trail | +0.86 | +1.99 |
| 338 | 22983 | 2026-09-01 16:20:25 | LONG | 101.22 | 17.13 | 17.13 | 2.87 | 2.00 | LONG | 72 | +1.26 |  | 98.84 09-01 18:35 | sl | -1.08 | -2.55 |
| 339 | 22984 | 2026-09-01 16:25:15 | LONG | 101.09 | 17.13 | 17.13 | 2.87 | 2.00 | LONG | 72 | +1.26 |  | 98.71 09-01 18:35 | sl | -1.08 | -2.55 |
| 340 | 22985 | 2026-09-01 16:25:22 | LONG | 101.09 | 17.13 | 17.13 | 2.87 | 2.50 | LONG | 72 | +1.26 |  | 98.71 09-01 18:35 | sl | -1.08 | -2.55 |
| 341 | 22986 | 2026-09-01 16:30:29 | LONG | 101.23 | 17.13 | 17.13 | 2.87 | 1.75 | LONG | 72 | +1.26 |  | 98.85 09-01 18:35 | sl | -1.08 | -2.55 |
| 342 | 22988 | 2026-09-01 16:35:15 | LONG | 101.09 | 17.13 | 17.50 | 2.87 | 2.50 | LONG | 72 | +1.26 |  | 98.61 09-01 18:35 | sl | -1.08 | -2.65 |
| 343 | 22990 | 2026-09-01 16:40:14 | LONG | 101.06 | 17.50 | 17.50 | 2.50 | 5.00 | LONG | 72 | +1.26 |  | 98.58 09-01 18:35 | sl | -1.08 | -2.65 |
| 344 | 22992 | 2026-09-01 16:45:18 | LONG | 100.81 | 17.50 | 17.50 | 2.50 | 4.25 | LONG | 72 | +1.26 |  | 98.33 09-01 18:45 | sl | -1.08 | -2.65 |
| 345 | 22996 | 2026-09-01 16:50:12 | LONG | 101.00 | 17.50 | 17.50 | 2.50 | 2.50 | LONG | 72 | +1.26 |  | 98.52 09-01 18:35 | sl | -1.08 | -2.65 |
| 346 | 22997 | 2026-09-01 16:55:16 | LONG | 101.06 | 17.50 | 17.50 | 2.50 | 4.25 | LONG | 72 | +1.26 |  | 98.58 09-01 18:35 | sl | -1.08 | -2.65 |
| 347 | 22998 | 2026-09-01 17:00:19 | LONG | 100.97 | 18.94 | 18.94 | 1.06 | 4.25 | LONG | 73 | +1.55 |  | 98.63 09-01 18:35 | sl | -1.09 | -2.52 |
| 348 | 23000 | 2026-09-01 17:05:10 | LONG | 100.88 | 18.94 | 18.94 | 1.06 | 4.25 | LONG | 73 | +1.55 |  | 98.52 09-01 18:35 | sl | -1.08 | -2.53 |
| 349 | 23001 | 2026-09-01 17:10:18 | LONG | 100.75 | 18.94 | 18.94 | 1.06 | 1.75 | LONG | 73 | +1.55 |  | 98.39 09-01 18:35 | sl | -1.08 | -2.54 |
| 350 | 23003 | 2026-09-01 17:15:16 | LONG | 100.72 | 18.94 | 18.97 | 1.06 | 1.75 | LONG | 73 | +1.55 |  | 98.32 09-01 18:45 | sl | -1.08 | -2.58 |
| 351 | 23005 | 2026-09-01 17:20:20 | LONG | 101.02 | 18.96 | 18.97 | 1.04 | 1.75 | LONG | 73 | +1.55 |  | 98.60 09-01 18:35 | sl | -1.08 | -2.59 |
| 352 | 23006 | 2026-09-01 17:25:21 | LONG | 101.03 | 18.96 | 18.97 | 1.04 | 2.50 | LONG | 73 | +1.55 |  | 98.61 09-01 18:35 | sl | -1.08 | -2.59 |
| 353 | 23007 | 2026-09-01 17:30:19 | LONG | 100.95 | 18.96 | 18.97 | 1.04 | 1.75 | LONG | 73 | +1.55 |  | 98.52 09-01 18:35 | sl | -1.08 | -2.60 |
| 354 | 23008 | 2026-09-01 17:35:40 | LONG | 101.09 | 18.96 | 18.97 | 1.04 | 1.75 | LONG | 73 | +1.55 |  | 98.66 09-01 18:35 | sl | -1.08 | -2.60 |
| 355 | 23010 | 2026-09-01 17:40:10 | LONG | 101.06 | 18.96 | 18.97 | 1.04 | 3.50 | LONG | 73 | +1.55 |  | 98.63 09-01 18:35 | sl | -1.08 | -2.60 |
| 356 | 23012 | 2026-09-01 17:45:26 | LONG | 100.90 | 18.96 | 18.97 | 1.04 | 4.00 | LONG | 73 | +1.55 |  | 98.47 09-01 18:35 | sl | -1.08 | -2.60 |
| 357 | 23013 | 2026-09-01 17:50:29 | LONG | 100.82 | 18.96 | 19.06 | 1.04 | 4.00 | LONG | 73 | +1.55 | YES | 98.37 09-01 18:35 | sl | -1.08 | -2.62 |
| 358 | 23014 | 2026-09-01 17:55:21 | LONG | 100.47 | 18.96 | 19.06 | 1.04 | 4.25 | LONG | 73 | +1.55 |  | 98.02 09-02 10:30 | sl | -1.08 | -2.63 |
| 359 | 23517 | 2026-09-03 07:30:14 | LONG | 100.77 | 19.04 | 19.04 | 0.96 | 2.50 | LONG | 31 | -1.30 | YES | 103.73 09-03 15:45 | trail | +1.15 | +2.74 |
| 360 | 23521 | 2026-09-03 07:40:10 | LONG | 100.88 | 19.04 | 19.04 | 0.96 | 2.50 | LONG | 31 | -1.30 |  | 103.74 09-03 15:45 | trail | +1.10 | +2.63 |
| 361 | 23549 | 2026-09-03 11:00:32 | LONG | 100.32 | 15.36 | 15.18 | 4.64 | 1.75 | LONG | 41 | -0.79 |  | 103.88 09-03 15:45 | trail | +1.52 | +3.35 |
| 362 | 23556 | 2026-09-03 11:40:20 | LONG | 100.78 | 15.32 | 15.38 | 4.68 | 1.75 | SHORT | 41 | -0.79 |  | 103.83 09-03 15:45 | trail | +1.25 | +2.82 |
| 363 | 23557 | 2026-09-03 11:45:13 | LONG | 100.87 | 15.32 | 15.43 | 4.68 | 1.75 | SHORT | 41 | -0.79 |  | 103.83 09-03 15:45 | trail | +1.21 | +2.73 |
| 364 | 23561 | 2026-09-03 11:50:15 | LONG | 100.80 | 15.43 | 15.43 | 4.57 | 3.50 | LONG | 41 | -0.79 |  | 103.83 09-03 15:45 | trail | +1.24 | +2.80 |
| 365 | 23567 | 2026-09-03 12:15:13 | LONG | 100.90 | 14.81 | 14.86 | 5.19 | 1.75 | LONG | 52 | -0.67 |  | 103.90 09-03 15:45 | trail | +1.28 | +2.77 |
| 366 | 23571 | 2026-09-03 12:20:15 | LONG | 100.68 | 14.86 | 14.86 | 5.14 | 1.75 | LONG | 52 | -0.67 |  | 103.89 09-03 15:45 | trail | +1.37 | +2.98 |
| 367 | 23573 | 2026-09-03 12:35:12 | LONG | 101.09 | 15.55 | 15.55 | 4.45 | 3.50 | LONG | 52 | -0.67 |  | 103.83 09-03 15:45 | trail | +1.11 | +2.51 |
| 368 | 23591 | 2026-09-03 13:00:20 | LONG | 101.44 | 16.47 | 16.47 | 3.53 | 4.00 | LONG | 78 | +0.54 |  | 103.86 09-03 15:45 | trail | +0.99 | +2.18 |
| 369 | 23606 | 2026-09-03 14:35:14 | LONG | 102.65 | 18.42 | 18.42 | 1.58 | 2.25 | SHORT | 68 | +0.71 |  | 105.18 09-03 18:55 | open_marked | +0.92 | +2.26 |
| 370 | 23608 | 2026-09-03 14:45:20 | LONG | 102.78 | 18.42 | 18.92 | 1.58 | 4.00 | LONG | 68 | +0.71 |  | 105.18 09-03 18:55 | open_marked | +0.83 | +2.13 |
| 371 | 23610 | 2026-09-03 14:50:10 | LONG | 103.88 | 18.42 | 18.97 | 1.58 | 4.75 | LONG | 68 | +0.71 |  | 105.18 09-03 18:55 | open_marked | +0.41 | +1.05 |
| 372 | 23612 | 2026-09-03 14:55:13 | LONG | 103.78 | 18.97 | 19.43 | 1.03 | 2.25 | LONG | 68 | +0.71 |  | 105.18 09-03 18:55 | open_marked | +0.42 | +1.15 |