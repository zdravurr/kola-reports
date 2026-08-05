# TITAN — DOES THE FLAT GATE MAKE US LATE TO THE BREAKOUT?

**2026-08-05 12:10 UTC · READ-ONLY · nothing changed, NOTHING PROPOSED · HEAD `b9081ad`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY. Mercury-SOL not opened.
Companion to `2026-08-05-1055-titan-is-anything-cutting-more-than-it-should.md`, whose verdict
stands unchanged: nothing is cutting more than the evidence supports.

---

## ANSWER IN ONE LINE

**No. The gate is not late, and the premise it rests on does not apply to this label.**

Expansion *is* a lagging property — **of the gap WIDTH**. But `ema_gap_dir` is not a width. It is
a **3-bar RELATIVE rate of change with a ±5 % threshold** (`indicators.py:283-291`), and in a
squeeze the denominator is tiny, so it fires on the first real move. Measured over **105 squeeze
episodes**: the 1h leg already reads `Expanding` **at the breakout bar itself in 90 % of them**,
and the full gate (both legs) admits at a **median of 30 minutes** after the break — costing
**0 percentage points of the move at the 25th, 50th and 75th percentile.**

The worry is closed. What the measurement *did* find is a different and smaller thing, stated in
§2c: at the breakout instant the gate is **blind** to a real break versus a failed one (44 % vs
50 %). Its value is temporal, not predictive — it keeps the bot out of the box, then steps aside.

---

## §0 — SOURCES, AND THE REPLAY VALIDATED BEFORE IT WAS TRUSTED

### 🔴 ONE CORRECTION TO THE PREMISE, AND IT CHANGED NOTHING

The brief calls OKX "the canonical source". That is right for the **order book** (§2.42 /
`34dbdbf`) but **not for the candles behind `ema_gap_dir_*`**: the indicator snapshot is fetched
from **BingX** — `main.py:555` `exchange = ccxt.bingx(...)` → `main.py:917`
`indicators.fetch_snapshot(exchange, symbol)`. **Every headline number below is measured on
BingX**, the exchange the gate actually reads, with OKX kept as a cross-check. **The two agree**
(replay match 93.8 % BingX vs 94.3 % OKX), so the choice does not move the answer — recorded so
the next session does not rediscover it as a discrepancy.

| series | source | candles | span |
|---|---|---|---|
| 1h | **BingX** | 19,921 | 2024-04-27 → 2026-08-05 (~2.3 y) |
| 15m | **BingX** | 24,191 | 2025-11-26 → 2026-08-05 (~8.3 m) |
| 5m | **BingX** | 12,095 | 2026-06-24 → 2026-08-05 |
| 1h / 15m / 5m | OKX (cross-check) | 26,299 / 42,099 / 11,599 | to 3 y |

### THE LABEL IS NOT RE-IMPLEMENTED — THE BOT'S OWN FUNCTION IS CALLED

`replay_lib.py` imports **`/root/titan-bot/indicators.py`** and calls
**`indicators.compute_tf_metrics`** on a 200-bar window (`indicators.CANDLE_LIMIT`), the same
window the live snapshot uses. This removes the entire class of *"my re-derivation disagrees with
the bot and I cannot tell which is right"* that produced §4's items 3, 9 and 10.

**Validation against the bot's own stored labels** (evenly-spaced rows, so the check is not
concentrated in one episode):

| variant | 1h match | 15m match |
|---|---|---|
| last **CLOSED** bar | 90.1 % | 88.3 % |
| last bar **FORMING** (synthesised from 5m) | **93.8 %** | **90.8 %** |

**FORMING wins on both timeframes — confirming §0's standing note that ADX/ATR/EMA read the
forming candle by design.** Median |replayed − stored| gap_pct: **0.0066 points**.

🔴 **The residual is threshold noise, and that is what makes it harmless here.** The label is a
threshold on a continuous quantity, so a replay that is fractionally off in price can only
disagree *near the boundary* — and that is exactly what is observed:

| \|gap_change_pct\| | disagreement rate |
|---|---|
| 2.5 – 5.0 (**at the ±5.0 boundary**) | **45.5 %** |
| 5.0 – 10 | 19.4 % |
| 10 – 25 | 2.4 % |
| **> 25** | **1.9 %** |

**Where a breakout lives — a large, unambiguous gap change — the replay is ~98 % accurate.**
Its error costs at most ~1 bar of timing, and the whole answer below is denominated in bars.

⚠️ **Direction of the remaining bias, stated rather than buried:** the historical episode study
uses **closed** bars, while the live bot reads the **forming** bar. The bot therefore sees
expansion **at most one bar EARLIER** than measured here. **Every lag figure below is an upper
bound.**

---

## §1 — MEASURING THE LAG ON HISTORY

### THE SQUEEZE DEFINITION, FIXED BEFORE ANY RESULT WAS LOOKED AT

- **BBW** = `4 × sd20(close) / sma20(close) × 100` on **1h** closes.
- A bar is **SQUEEZED** when `BBW <` the **20th percentile of the trailing 90 days** (2160 bars).
  Strictly backward-looking — **no look-ahead anywhere**.
- An **EPISODE** = a maximal run of **≥ 12 consecutive** squeezed bars.
- The **BOX** = `[min low, max high]` over the run.
- **t0 (BREAKOUT)** = the first bar after the run whose **close** leaves the box.
- **MOVE** = maximum favourable excursion from the box edge, in the breakout direction, within
  **48 h** of t0.

**Episodes found: 105 with a resolved breakout** (2024-08-18 onward on 1h). **34 of them** fall
inside 15m coverage, which is the sample for anything involving the 15m leg.

### 🔴 1a. THE CONTROL FIRST — OTHERWISE "lag = 0" MEANS NOTHING

A flag that is true at most bars would show "lag 0" everywhere and prove nothing. That is the
degenerate-control trap §2.54 caught and fixed. So the base rate comes first:

| `ema_gap_dir_1h` | all 19,722 bars | squeezed bars only | **at the breakout bar t0** |
|---|---|---|---|
| **Expanding** | **42.7 %** | **39.2 %** | 🔴 **89.5 %** (94 of 105) |
| Contracting | 49.0 % | 53.6 % | 8.6 % |
| Flat | 8.3 % | 7.2 % | 1.9 % |

**Lift at the breakout bar: +46.8 points over base.** The label is not trivially on, and it is not
flickering noise either — **median `Expanding` run = 5 bars**, p90 = 10, and only **11 %** of runs
last a single bar.

### 1a/b. THE MOVE, AND THE LAG TO `Expanding`

**48h move from the box edge (n=105):** median **2.70 %**, p25 1.24 %, p75 4.06 %.

**Lag, in minutes after t0 — the distribution, not the mean:**

| leg | n | min | p25 | **median** | p75 | p90 | max | never |
|---|---|---|---|---|---|---|---|---|
| **1h leg** (full sample, bars) | 105 | 0 | 0 | **0** | 0 | 1 | **2** | 0 |
| 1h leg (15m-covered subset) | 34 | 0 | 0 | **0** | 0 | 60 | 120 | 0 |
| 15m leg | 34 | 0 | 0 | **0** | 30 | 30 | 45 | 0 |
| 🔴 **BOTH — the gate admits** | 34 | 0 | 0 | **30 min** | 30 | 60 | 915 | **0** |

On the full 105-episode sample the 1h leg is **already Expanding at t0 in 90 %** of episodes and
**within one bar in 95 %**; the worst case in 2.3 years is **2 bars**.

**Distribution of the JOINT lag:**

| | episodes | share |
|---|---|---|
| **0 min — admits at the breakout bar** | 16 | **47.1 %** |
| ≤ 60 min | 15 | 44.1 % |
| ≤ 12 h | 2 | 5.9 % |
| > 12 h (one episode, 915 min) | 1 | 2.9 % |
| **never within 48 h** | **0** | **0 %** |

**91.2 % of squeeze breakouts are admitted within one hour of the break.**

### 1c. HOW MUCH OF THE MOVE HAD ALREADY HAPPENED

% of the 48h move already travelled when the gate admits (n=34): median **22 %**, p25 13 %,
p75 66 %, max 100 %.

| share of move already gone | episodes |
|---|---|
| 0–9 % | 5 (14.7 %) |
| 10–24 % | 15 (44.1 %) |
| 25–49 % | 2 (5.9 %) |
| 50–74 % | 6 (17.6 %) |
| 75–100 % | 6 (17.6 %) |

🔴 **THAT NUMBER IS NOT THE GATE'S FAULT, AND §2 IS WHERE THAT IS PROVED.** A median of 22 % of a
48-hour move happens inside the first hour because **breakouts are fast at the start** — that is a
property of the tape, not of any filter. Attributing it to the gate is the arithmetic error this
section exists to prevent.

---

## §2 — WHAT THE GATE WOULD ACTUALLY HAVE COST

### 2a. IT ADMITTED IN EVERY SINGLE EPISODE

**34 of 34 within 48 h. Zero misses.** The question was never *whether*, only *when*.

### 2b. 🔴 THE COST, ISOLATED FROM THE BREAKOUT'S OWN FIRST-BAR TRAVEL

The honest comparison the brief asked for — **the gate versus entering at the first signal after
the break, with no gate**. t0 is the earliest a bar-resolution entry could act, so:

**COST = (% of move gone when the GATE admits) − (% of move gone at t0, no gate)**

| | p25 | **median** | p75 | max |
|---|---|---|---|---|
| % of move gone at **t0 (NO GATE)** | 13 % | **22 %** | 66 % | 100 % |
| % of move gone when the **GATE admits** | 13 % | **22 %** | 66 % | 100 % |
| 🔴 **THE GATE'S OWN COST** | **0** | **0** | **0** | **28 pts** |

**Identical at every quantile.** The gate cost **exactly nothing in 32 of 34 episodes (94 %)**. It
cost more than 25 points of the move in **1 of 34 (3 %)** — the single 915-minute outlier.

**Sensitivity — the headline does not depend on my definition.** Nine variants of (percentile ×
minimum run):

| pctl | min run | episodes | 1h lag = 0 | median lag | median move | **failed** | move < 1.5 % |
|---|---|---|---|---|---|---|---|
| 10 | 6 | 101 | 87 % | **0 h** | 2.47 % | 55 % | 30 % |
| 10 | 12 | 61 | 92 % | **0 h** | 2.95 % | 54 % | 28 % |
| 10 | 24 | 27 | 93 % | **0 h** | 3.31 % | 52 % | 22 % |
| **20** | **12** | **105** | **90 %** | **0 h** | **2.70 %** | **45 %** | **31 %** |
| 20 | 6 | 178 | 87 % | **0 h** | 2.56 % | 45 % | 30 % |
| 20 | 24 | 51 | 90 % | **0 h** | 2.82 % | 45 % | 29 % |
| 30 | 6 | 225 | 88 % | **0 h** | 2.38 % | 40 % | 30 % |
| 30 | 12 | 145 | 93 % | **0 h** | 2.71 % | 37 % | 30 % |
| 30 | 24 | 82 | 96 % | **0 h** | 2.49 % | 37 % | 28 % |

**Median lag is 0 hours in all nine. `lag = 0` ranges 87–96 %.**

### 2c. 🔴 THE OTHER SIDE, STATED AS PLAINLY AS THE FIRST

**A lag measurement that ignores false starts is half an answer — so here is the other half.**

On the full n=105 sample:

| | count | share |
|---|---|---|
| 🔴 **FAILED** — price traversed the **entire box the other way** within 48 h | **47 / 105** | **45 %** |
| move < 1.5 % (not worth a trade after costs) | 33 / 105 | **31 %** |
| move < 1.0 % | 16 / 105 | 15 % |

**Nearly half of all squeeze breakouts fail outright.** That is the population the gate exists to
refuse, and it is large.

**And here is what the gate does about it — measured, not assumed:**

| where | joint condition (1h AND 15m Expanding) |
|---|---|
| **INSIDE the squeeze box** (4,016 × 15m steps) | admits 20.0 % → 🔴 **REFUSES 80.0 %** |
| **AT the breakout bar** | admits **47.1 %** |
| discrimination | **+27.1 points** |

The **80 % refusal inside the box independently reproduces §2.47's ~80 % pre-registration**, from
a completely different direction — squeeze episodes on 2.3 years of candles, rather than the
bot's own signal log.

🔴 **BUT THE GATE IS BLIND TO WHICH BREAKOUT IS REAL:**

| at t0 | n | gate admits |
|---|---|---|
| **successful** breakouts | 18 | 8 = **44 %** |
| **failed** breakouts | 16 | 8 = **50 %** |

**A 6-point difference in the wrong direction, on n=34 — i.e. nothing.** The gate's value is
**temporal, not predictive**: it keeps the bot out of the box (refusing 80 % of it), then steps
aside at the break without knowing whether the break is genuine. It does not, and was never shown
to, pick winners at the breakout instant.

---

## §3 — IS THERE A LEADING ALTERNATIVE INSIDE THE SAME FAMILY?

No new indicator family was considered — §2.45 killed ten and that ruling stands. This stays
strictly inside the EMA envelope.

### 3a. THE CONTINUOUS QUANTITY VS ITS OWN LABEL

The label is `Expanding ⇔ gap_change_pct > +5.0` over a 3-bar lookback. The natural leading form
is the same quantity with the threshold removed: **`gap_change_pct > 0`** — any widening at all.

| | result |
|---|---|
| bars by which `gap_change > 0` **precedes** the `Expanding` label (n=34) | median **0**, p75 **0**, **max 1** |
| episodes where it is **not one bar earlier** | **33 of 34 = 97 %** |
| 🔴 **its price**: `Expanding` true on all bars | 42.7 % |
| 🔴 **its price**: `gap_change > 0` true on all bars | **46.5 %** |
| net | **+3.8 pts more permissive — 1.09× — for 0 bars of lead** |

**Both numbers, as required, and they point the same way: there is no lead to buy.** In a squeeze
the gap denominator is so small that any genuine widening blows straight past +5 %, so the
threshold is not what delays the label — **the threshold is essentially free.** Dropping it would
purchase **zero bars** of earliness at the cost of admitting **9 % more of all bars**.

### 3b. DOES THE 15m LEG LEAD THE 1h LEG?

**No, not consistently.** `(1h lag − 15m lag)`, n=34: **median 0 minutes**, p25 −30, p75 0.

| 15m strictly earlier | same bar | **1h earlier** |
|---|---|---|
| 7 | 16 | **11** |

The 1h leg is earlier more often than the 15m leg is. **There is no stable lead/lag structure
between the two legs to exploit.**

### 3c. CONCLUSION

**A leading form exists in principle and is worthless in practice: 0 bars earlier, 9 % more
permissive.** Both numbers or neither — and with both in hand, the answer is neither.

---

## §4 — VERDICT ON THE CURRENT SQUEEZE

### WHERE WE ACTUALLY ARE

| | value |
|---|---|
| latest 1h bar | 2026-08-05 10:00 UTC |
| 1h BB width | **0.755 %** |
| p20 threshold (trailing 90 d) | 1.227 % |
| 🔴 **BBW percentile within trailing 90 days** | **5.0** — deep in the squeeze |
| consecutive squeezed hours ending now | **6** (an episode needs 12) |
| current 1h gap label | `Contracting` |
| `Expanding` over the last 24 bars | 12 of 24 — **exactly the 42.7 % base rate** |

This corroborates the 10:55 report from a third direction: BBW at the **5th percentile** of 90
days is as tight as this instrument gets. **The squeeze is real and is currently deepening** —
0.741 % and 0.755 % on the last two bars, against a 1.227 % threshold.

### THE PLAIN ANSWER

🔴 **The gate is NOT likely to be late to the resolution of this squeeze, and the expected
lateness is roughly zero.**

- On history the gate admits at the breakout bar itself **47 %** of the time and **within one
  hour 91 %** of the time; the 1h leg alone is ready at t0 in **90 %** of 105 episodes.
- Its **own** contribution to "the move already happened" is **0 points at p25, p50 and p75**.
- The realistic bad case is **one episode in thirty-four** (3 %) where it cost ~28 points of a
  48-hour move — and even that episode was eventually admitted, not missed.
- Since the live bot reads the **forming** candle, its true lag is **at most one bar earlier than
  these figures**, never later.
- Against that, **45 % of squeeze breakouts fail outright** and 31 % move less than 1.5 % — the
  population that makes a quiet gate worth having.

**The worry can be closed.** What should *not* be carried forward from it is the premise itself:
**expansion is lagging as a WIDTH, but `ema_gap_dir` is a rate of change, and a derivative leads a
level.** That distinction is the whole of this result, and it is the thing worth remembering.

### 🔴 NOTHING IS PROPOSED

Per the brief and per §2.45 / §2.54: **this is cell 56 of a Bonferroni budget set at 54.** No
change to the gate, no relaxation of the threshold, no leading variant, no new filter. The one
finding that could look actionable — the gate is blind to real-vs-failed breaks at t0 (44 % vs
50 %, n=34) — is **exactly the kind of thin-sample cell this book has killed a dozen times**, and
it is recorded as an observation with its n attached, not as an opening.

The pre-registered instruments from §2.47 are unchanged and remain the only things that may move
the gate: **n ≥ 100 refusal rows** for the fast trigger (currently **12**), and **20 executed
entries per side** for the review point.

---

*Read-only. Candles from BingX public REST (the bot's own indicator source) with OKX as a
cross-check; labels produced by importing and calling the bot's own `indicators.compute_tf_metrics`;
`titan-bot` unmodified; Mercury-SOL never opened.*
