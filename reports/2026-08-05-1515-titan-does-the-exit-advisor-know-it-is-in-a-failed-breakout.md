# TITAN — DOES THE EXIT ADVISOR KNOW IT IS IN A FAILED BREAKOUT?

**2026-08-05 15:15 UTC · READ-ONLY · nothing changed, NOTHING PROPOSED, NO DIFF · HEAD `b9081ad`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
Mercury-SOL never opened. `git status` on `titan-bot` clean before and after.

Parent: `2026-08-05-1455-titan-what-discriminates-a-real-breakout-from-a-failed-one.md`.
Its closure stands and is not disturbed: **nothing predicts a failed breakout in advance.**
This asked a different question — an observable *after* entry — and it is a fair question.

---

## ANSWER IN ONE LINE

**§1 is FEASIBLE — the box can be known in flight, and cheaply. But §3's gate, the one you
wrote into the brief yourself, FIRES: the field cannot distinguish the box event from ordinary
retracement, because it IS ordinary retracement.**

🔴 **"Price is back inside the box" is not merely correlated with "price has retraced past the
breakout level" — it is the SAME EVENT, identically, by construction.** The box's near edge
*is* the breakout level. Being inside the box is exactly "adverse excursion from that level > 0".
Measured at every horizon, the two produce **the same episodes, the same cell sizes, the same
failure rates, to the decimal.**

**And a plain ATR retracement — which needs no box, no Bollinger, no 2,160-candle fetch and no
new stored field — does the same job BETTER at every horizon.**

**So there is no diff.** Per §4 I stop here. If you want the diff regardless, say so and I will
write it — that call is yours, not mine, and I am not narrowing your scope on my own authority.

🔴 **One correction to the brief's premise, and it is load-bearing.** The brief says *"price
returns INSIDE the box it broke out of. That is the 45 % definition itself."* **It is not.** The
45 % definition is a **full traverse** — price crosses the entire box and exits the FAR side.
Returning inside the box is a far weaker and far more common event: **76 % of all breakouts,
including three quarters of the SUCCESSFUL ones.** The two were conflated, and the whole idea
rests on that conflation.

---

## §1 — CAN THE BOX BE KNOWN IN FLIGHT?

### 1a. 🔴 DOES THE LIVE BOT COMPUTE ANY SQUEEZE MEASURE? **NO. NOT ANYWHERE.**

```
$ grep -rniE "bollinger|bbands|bbw|squeeze|keltner|band_width|stddev" --include=*.py .
claude_advisor.py:67:  # It read: "Treat the market as flat/squeezed when 1h ADX is low (~<20-23)
```

**One hit, and it is a comment describing a RETIRED rule** — the FLAT-MARKET GUARD removed
2026-07-29 (§2.13 killed the ADX ~<20-23 claim it rested on). There is **no Bollinger band, no
bandwidth, no percentile baseline, no box** in the live bot. `indicators.compute_tf_metrics`
computes ATR, ADX, EMA9/21 slopes, `vol_ratio`, `trend` and the EMA-gap fields — and nothing else.

**Every squeeze figure in the 12:10, 14:55 and this report is REPLAY. The bot has never known
a squeeze existed.** Confirmed, as asked, rather than assumed.

### 1b. WHAT WOULD IT TAKE TO KNOW — COSTED

The work splits cleanly in two, and only the first half is expensive:

| half | what it needs | cost |
|---|---|---|
| **(i) at ENTRY — is this a squeeze breakout, and what are the box bounds?** | BBW over 20 bars is trivial. **The classification is not**: "squeezed" = BBW < p20 of the **trailing 90 days = 2,160 1h bars**. | 🔴 **BingX caps `fetch_ohlcv` at 1,000 candles — measured, not assumed** (`limit=1440` returns 1,000). So **3 network calls** at entry, or a rolling stored baseline seeded by a one-time 3-call backfill and appended hourly — the `orderbook_density` pattern. |
| **(ii) IN FLIGHT — where is price relative to the box?** | the stored bounds and the current price, both already in hand | 🔴 **ZERO network calls, zero computation.** Two float comparisons. |

### 1c. 🔴 IS IT CHEAP ENOUGH ON THE ADVISOR'S CADENCE WITHOUT A NETWORK CALL? **YES — AND THE 08-01 LESSON IS SATISFIED**

The concern was a field that costs a fetch on every consult, where a Tor hiccup silently skips
it. **That failure mode does not arise here**, because the expensive half happens **once, at
entry**, and the in-flight half is a comparison against a stored number.

The architecture is already sitting there:

- `_record_smart_exit_dryrun` (`virtual_trader.py:2091`) runs **hourly per open position** —
  `SMART_EXIT_DRYRUN_SAMPLE_SEC = 3600`, the same cadence as `EXIT_ADVISOR_HOURLY_SEC = 3600`.
- It is explicitly split into a **"CHEAP phase (DB only, no network)"** with the throttle, and a
  **HEAVY phase** that already fetches the OKX book and three timeframes of candles.
- The exit advisor **does not fetch these itself** — `_build_exit_context` (`main.py:2741`)
  **reads the latest `smart_exit_dryrun_samples` row from the DB** for its `regime_now` and
  `volume_now` lines.

So a box field would follow the identical, already-proven route: **written at entry, read from
SQLite at consult.** ⚠️ One correction to the brief's framing, recorded because it cuts the other
way: the exit context is **not** currently network-free — it calls
`liquidity_zones.fetch_pre_trade_walls` at `main.py:2782`. The box would add nothing to that.

### 1d. VERDICT ON §1

**It CAN be known in flight, and the cost is acceptable.** §1 does not kill the idea.

**What kills it is §3, and §3 was your own gate.**

---

## §2 — THE GATE IN §3 FIRES FIRST, SO THERE IS NO DIFF. HERE IS THE MEASUREMENT.

Your §3: *"The signal here is specifically 'back inside the box', which is the 45 % event — not
a retracement. If the field cannot distinguish those two, it is noise and should not be added."*

### 2a. 🔴 FIRST, THE PREMISE — "BACK INSIDE THE BOX" IS NOT THE 45 % EVENT

Measured on the same 105 episodes, over the 48 h after t0:

| event | episodes | rate | median first seen |
|---|---|---|---|
| **RETRACE** — adverse excursion > 1.0 × ATR | 84 / 105 | **80 %** | 2 h |
| **RE-ENTRY** — price closes back inside the box | 80 / 105 | **76 %** | 4 h |
| both | 77 / 105 | 73 % |  |
| 🔴 **FAILED** — full traverse to the FAR edge | **47 / 105** | **45 %** | 18 h |

**The box event is 4 percentage points rarer than the retracement event.** It is **not** the
45 % event; it is a 76 % event. It fires on **33 of the 58 successful breakouts.**

### 2b. 🔴 AND THE REASON IT CANNOT SEPARATE FROM RETRACEMENT: IT IS AN IDENTITY

For an UP break the box's near edge is `hi`, and "inside" means `close < hi`. The adverse
excursion from the breakout level is `hi − close`. **`close < hi` ⟺ `hi − close > 0`.** These are
the same predicate written twice. The same holds for a DOWN break with `lo`.

**That is not an empirical correlation to be de-confounded. It is an algebraic identity**, and
it shows up as such in the measurement — the two rows are not merely close, they are the same
episodes:

| h after t0 | BOX "inside" | ATR "adverse > 0.0" | identical? |
|---|---|---|---|
| **1 h** | n=21 · fail **71 %** vs 38 % · Δ+33.3 · p 0.0071 | n=21 · fail **71 %** vs 38 % · Δ+33.3 · p 0.0074 | 🔴 **yes** |
| **6 h** | n=40 · fail **60 %** vs 35 % · Δ+24.6 · p 0.0163 | n=40 · fail **60 %** vs 35 % · Δ+24.6 · p 0.0149 | 🔴 **yes** |
| **12 h** | n=37 · fail **73 %** vs 29 % · Δ+43.6 · p 0.0000 | n=37 · fail **73 %** vs 29 % · Δ+43.6 · p 0.0001 | 🔴 **yes** |

*(the two p-values differ only in the 20,000-shuffle permutation draw)*

**The stratified test §3 asks for cannot even be run** — and the reason is the identity, not a
thin sample. Within "adverse > 0.5 ATR", the cells are **31 / 0** and **32 / 0**: every episode
past a 0.5-ATR retracement is *necessarily* inside the box. There is no independent variation in
the box given the retracement, because there is no independent box.

### 2c. 🔴 AND THE BOX-FREE VERSION IS STRICTLY BETTER

A plain ATR-denominated retracement — **no box, no Bollinger, no 2,160-candle fetch, no new
stored field** — dominates the box binary at every horizon:

| h | BOX (inside / outside) | ATR > 0.5 | **ATR > 1.0** |
|---|---|---|---|
| 1 h | Δ+33.3 · p 0.0071 | Δ+38.9 · p 0.0212 | Δ+40.9 · p 0.0897 |
| 6 h | Δ+24.6 · p 0.0163 | Δ+32.6 · p 0.0019 | 🔴 **Δ+41.1 · p 0.0006** |
| 12 h | Δ+43.6 · p 0.0000 | Δ+39.0 · p 0.0002 | 🔴 **Δ+46.1 · p 0.0000** |

**The box is the zero-threshold special case of a family whose better members need no box at
all.** Building the squeeze machinery to obtain it would be paying three network calls and a new
stored field for the *worst* setting of a parameter the bot can already read.

⚠️ **And the advisor is already given this quantity.** `_build_exit_context` supplies `upnl_r`,
`mfe_r` and `giveback_r`, and R is ATR-denominated by construction — `1R = SL_ATR_MULT × ATR ×
size`. Adverse movement in ATR units is **already on the exit prompt**, measured from the fill.
The box would re-express it from a slightly different reference level.

### 2d. THE TWO THINGS THAT LOOKED STRONGEST, AND WHY NEITHER IS USABLE

**(i) "Never re-entered the box" is a perfect negative — and it is a tautology.**

| | FAILED | succeeded | |
|---|---|---|---|
| re-entered the box | 47 | 33 | P(fail) = **59 %** |
| **never re-entered** | **0** | **25** | P(fail) = **0 %** |

Sensitivity **100 %**. It looks like the strongest cell in this entire book — and it is
worthless, because **to traverse the box you must first re-enter it.** Re-entry is a logical
precondition of failure, so "all failures re-enter" is true by definition, exactly as
"wide boxes fail less" was true by definition in the 14:55 report. **Same trap, second sighting,
in eight hours.**

**(ii) The FAR-edge event is the real 45 % definition — and it arrives too late to act on.**
Median **18 h** from t0 to the far edge (p25 9 h, p75 37 h). By the time the field reads
"beyond the far edge", the position is already through the whole box. That is not a warning,
it is an obituary.

*(A third, depth of penetration in box widths — failed median 1.65 vs succeeded 0.34 — is
definitionally rigged the same way: failure REQUIRES depth ≥ 1.0. Recorded so it is not
mistaken for a finding later.)*

---

## §3 — THE HONEST RISK, AND THE COVERAGE PROBLEM THAT WOULD HAVE BITTEN ANYWAY

### 3a. 🔴 EVEN IF IT WORKED, IT WOULD ALMOST NEVER FIRE

Measured against Titan's **66 real positions** (2026-05-17 → 2026-08-03, 0 open now), under the
same episode definition:

| a squeeze t0 within the preceding… | entries | share | of which **same-direction** |
|---|---|---|---|
| 12 h | 5 / 66 | 7.6 % | **3** |
| 24 h | 8 / 66 | 12.1 % | **4** |
| 48 h | 17 / 66 | 25.8 % | **10** |

🔴 **Seven of the 17 matches are the WRONG DIRECTION** — the position was opened *against* the
break (vpos 30, 31, 32, 75, 79, 83, 91). A "you are in a failed breakout" field on those rows
would be describing someone else's trade.

**In the live era the coverage is 2 positions (vpos 91, 92), and one of those two is
counter-direction.** The field would be NULL on ~85 % of entries and meaningful on ~1 in 7 — the
same shape as the order book's n=5 in the 14:55 report, arrived at from the other end.

### 3b. WHAT I WOULD WATCH IF IT WERE ADDED (asked, and answered even though it is not)

The exit advisor is the only measured positive in this system: **+3.3729R over five closed
positions**, criterion closed at 5 of 10 on 2026-08-04 with the freeze lifted. **n=5 is a
direction, not a proof**, and a new prompt field could degrade it invisibly. I would watch:

1. **`close` verdict RATE before vs after**, split by whether the field is NULL — if the rate
   moves on rows where the field is NULL, the field changed the model's behaviour on trades it
   does not even describe, which is the clearest possible sign of contamination.
2. **The R-outcome of `close` verdicts**, kept strictly on the **post-17:01:29 side of §0's 1R
   boundary** — pre-boundary R is a 10 %-larger unit and must not pool.
3. **Advisor confidence distribution** — a field that shifts confidence without shifting verdicts
   is still changing the instrument.
4. **Verdict flips on the same position across consecutive hourly consults** — the box state
   changes hour to hour, so an unstable field would show up as advisor chatter first.

### 3c. THE KILL SWITCH — CONFIRMED, AND IT REVERTS CLEANLY

`EXIT_ADVISOR_DRYRUN = True` (`config.py:278`, currently `False` = acting). Traced:

- `virtual_trader.py:2479` — `if not EXIT_ADVISOR_DRYRUN and _advisor_says_close(_adv)` — the
  hourly path.
- `main.py:3813` — `if (not EXIT_ADVISOR_DRYRUN …` — the 15m-confirm / 1H-arm path.
- `_advisor_close` (`virtual_trader.py:2314`) is **the only code in the bot that closes on an
  advisor's say-so**, and both call sites are behind the flag.

**Setting it True leaves the consult running and the verdict persisted, and removes the hands.**
One flag, no code path left half-armed. ⚠️ Recorded from §2.4's history: this flag once **silenced
the consult instead of arming it** (the 07-30 finding, `virtual_trader.py:2456` comment). It no
longer does — the consult is outside the guard, only the action is inside — but that is the exact
line to re-read before touching it.

---

## §4 — VERDICT

### 🔴 §1 SAYS FEASIBLE. §3 SAYS DO NOT BUILD IT. §3 WINS, AND §3 WAS YOURS.

**The exit advisor does not know it is in a failed breakout. It also does not need the box to
find out** — the box's only content is a retracement past the breakout level, and adverse
movement in ATR is already on the exit prompt in R.

| the idea's three claims | verdict |
|---|---|
| a failed breakout has an observable post-entry signature | ✅ **true** — adverse excursion, and it is genuinely informative (71 % vs 38 % at h=1) |
| that signature is "price returns inside the box" | 🔴 **that is a 76 % event, not the 45 % event** |
| the box is distinguishable from ordinary retracement | 🔴 **NO — it is algebraically identical to it, at the worst threshold** |

**This is not a seventeenth dead prediction branch** — you were right that it is a different
class, and the class is sound. **It is something rarer: a proposed observable that turned out to
be an observable the system already has, wearing new structure.** That is worth a §2.45 entry of
its own, because the next person to have this idea will have it about some other box.

### THE SQUEEZE, AS OF THIS REPORT

| | value |
|---|---|
| latest closed 1h bar | 2026-08-05 **14:00 UTC** |
| 1h BB width | **0.769 %** (0.698 % at the 13:00 bar, 0.755 % at 10:00) |
| p20 threshold, trailing 90 d | 1.224 % |
| **BBW percentile within trailing 90 d** | **5.6** (was 3.4 an hour ago) |
| consecutive squeezed hours | **10** — an episode still needs 12 |

**The squeeze has ticked slightly wider in the last hour but has not resolved.** The bot holds
**0 open positions**, so nothing is exposed to its resolution at this moment.

### 🔴 NOTHING IS PROPOSED, AND NO DIFF IS ATTACHED

No field, no prompt change, no config, no schema. `titan-bot` unmodified at `b9081ad`,
`git status` clean. `trades.db` opened read-only throughout.

**If you want the §2 diff anyway** — the fields are well-defined and I have the placement — say
so and I will write it. I am not applying anything either way. My recommendation is that the
measurement above makes it a cost with no content, but the decision is yours.

---

## APPENDIX — WHAT WAS RUN

| file | purpose |
|---|---|
| *(grep/read only)* | §1a: the squeeze-measure search across the live tree; `_build_exit_context`, `_record_smart_exit_dryrun`, `_tf_metrics_safe`, `_fetch_ohlcv_cached` read for cadence and network structure |
| *(ccxt probe)* | §1b: BingX `fetch_ohlcv` cap measured at **1,000 candles** — `limit=1440` returns 1,000 |
| `c1_would_it_fire.py` | §3a coverage: 66 real positions vs the 105 episodes; re-entry vs retracement base rates |
| `c2_state.py` | the ever-version 2×2; the STATE version hour by hour; the far-edge timing; penetration depth |
| `c3_vs_retrace.py` | 🔴 the deciding test: BOX vs ATR-retracement at h=1/6/12, and BOX within an ATR stratum |

Permutation tests are 20,000 shuffles, two-sided, seed 20260805. Episodes **reused** from the
12:10 report, not re-derived. Candles from BingX public REST (the bot's own indicator source).

*Read-only. Nothing changed, nothing proposed, no diff. Mercury-SOL never opened.*
