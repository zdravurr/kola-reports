# titan-two-prompt-fixes-applied-and-criterion-restart

_2026-07-29 13:35 UTC_

---

**Both applied — `c307bb7`, pushed, restarted 13:21:47 UTC, 0 errors.** Snapshot:
`pre-prompt-truth-20260729T131319Z` + `*.bak_prompts_20260729T131319Z`.

---

# 1. THE FALSE TRAIL PROMISE — REMOVED

The close prompt ended with *"The stop and trail remain active if you HOLD."* The trail arms at +1R
(`virtual_trader.py:1678-1691`, `_breakeven_reached` measured off the **original** stop), and 56 of
the first 59 consultations happened below +1R. **No trail existed on 94.9% of them.**

Replaced with a block computed **per consultation** from the position's own management state —
`breakeven_applied` in the JSON `virtual_trader` keeps in the repurposed `pending_dca_limits`
column. **Read, not inferred**, and it says so if it cannot be read:

- **ARMED / NOT ARMED / unreadable**
- the **live stop level and its distance in R**
- when not armed, the **exact price that would arm it**

## REAL STORED CONSULT

Row **19460**, **2026-07-29 13:30:08 UTC**, trigger `Bearish I-CHOCH`, verdict **hold** (confidence 0.62):

```
Consultation trigger: armed_exit

If you HOLD: the stop-loss is in place. The trailing stop is NOT ARMED — it arms only at +1R, which this position has not reached, so the stop is the only protection. It would arm if price reaches 64864.7 (+1R).
  Current stop: 63129.9 (+1.19R away).

Judge whether THAT specific entry thesis is still alive and whether book/regime have turned against it.
```

That is the corrected line as actually sent. The position (vpos 84) has an MFE of 0.806R — it has
never reached +1R, so the old prompt's claim was false at that very moment and the new one is not.

**Also corrected in the same commit:** the dormant legacy `_CLOSE_SYSTEM` carried the identical
falsehood (*"the bot's on-exchange SL/trail will still protect downside"*). It has no
per-consultation context to compute from — `consult_for_close()` is reached only by the 5m Group-B
trigger, which OPEN-ITEMS §5 records as never having arrived — so the claim was made **true** rather
than computed: the stop always protects, the trail only once armed at +1R. Flagged here because it
is one line beyond what you asked for; trivial to revert.

---

# 2. THE ADX RULE — RETIRED, NOT REPLACED

Removed from `claude_advisor.py:334`:

```
-  f"(higher = stronger trend; ~<20-23 = weak/ranging)\n"
```

and the **entire FLAT-MARKET GUARD soft rule** from `_ENTRY_SYSTEM` — the instruction built on that
number, which also leaned on `market_regime` (shown by the same study to carry almost no information
about the tape, Cramér's V 0.04–0.07).

🔴 **Deliberately not replaced with a different number.** We have no validated one, and a second
unvalidated threshold would repeat the defect with a new value. The advisor still sees **every** ADX,
ATR% and EMA-gap figure, raw, on every timeframe — it is simply no longer told what they mean.

## RENDERED ENTRY PROMPT — no ADX claim

Built by the deployed code at `c307bb7` against live state. **Labelled honestly: a forced render, not
a stored decision — no entry consult has landed since the restart** (the signals since were
`htf_blocked` or exit-side, and those never reach the entry advisor).

```
Symbol: BTC/USDT:USDT
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  Smart Trail Bullish  (direction withheld (AI_ADVISOR_HIDE_1H), weight 0.9, last set 5.5h ago)
  15m: HyperWave Signal Down  (SHORT, weight 0.7, last set 2.5h ago, NOT counted by the gate — matrix TTL expired)
  5m:  Bullish Breaker  (LONG, weight 0.7, last set 66m ago, trigger-capable, NOT counted by the gate — matrix TTL expired)
  Agreement: 5m points LONG; 15m points SHORT; vs the proposed LONG: 5m agree, 15m OPPOSE.
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 71.1214  |  Volume ratio 5m: 0.48x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 16.1 | 15m 22.8
  ATR% of price: 1h 0.474% | 15m 0.195% | 5m 0.111%
  EMA-gap: 1h 0.238% (Contracting) | 15m 0.073% (Expanding)  (Contracting/Flat = compression)
  Market regime: TREND | MTF alignment score: 3
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: NEUTRAL, ADX 16.0, EMA-gap 0.266% (Contracting)
  4h: NEUTRAL, ADX 24.7, EMA-gap 0.185% (Contracting)
  1h: NEUTRAL, ADX 16.1, EMA-gap 0.238% (Contracting)
  15m: BEAR, ADX 22.8, EMA-gap 0.073% (Expanding)
  5m: BEAR, ADX 32.1, EMA-gap 0.100% (Expanding)
  MTF alignment vs LONG: 3/4 (4H/1H/15m/5m; excludes 1d)
```

`20-23` and `weak/ranging` now appear **zero** times in the user prompt and **zero** times in
`_ENTRY_SYSTEM` (checked programmatically, both False).

The `_ENTRY_SYSTEM` block that survives is the one still backed by a measurement — the opposing-wall
HARD RULE, which judges thickness by the **percentile** (`8b15ecc`), not by a raw multiple.

---

# 3. SCOPE

| target | result |
|---|---|
| files changed vs `4fc89ea` | **2** — `claude_advisor.py` (+95/−15), `main.py` (+23) |
| `config.py` | **not in the diff** |
| `state_machine.py`, `signal_matrix.py`, `virtual_trader.py`, `signal_tiers.py` | **zero changed lines** |
| score gate, both thresholds, HTF cascade, `confluence_check`, `market_regime` | untouched |
| SL / trail / breakeven **mechanics**, `ADX_BELOW_FLOOR`, post-entry recheck | untouched — prompt text only |
| LONG partial, signal tiers | untouched |
| Mercury-SOL | untouched, service active |

Flags unchanged: `LIVE_TRADING_ENABLED=False` · `LONG_PARTIAL_ENABLED=True` ·
`EXIT_ADVISOR_PAPER_ENABLED/DRYRUN/ON_15M_CONFIRM/HOURLY=True` · `CONFLUENCE_FLAT_THRESHOLD=5.0` ·
`CONFLUENCE_SCORE_THRESHOLD=2.0` · `WALL_TRAIL_LIVE_ENABLED=False` · `AI_ADVISOR_HIDE_1H=True` ·
`ADX_BELOW_FLOOR=20.0` · `HTF_CASCADE_ENABLED/HTF_TOLERATE_NEUTRAL=True` · `SL_ATR_MULT=2.5` ·
`TRAIL_MULT_ATR=2.5`.

---

# 4. CONTAMINATION — §2.4's COUNT RESTARTS. I AGREE.

Recorded as **OPEN-ITEMS §2.18**.

**All 59 exit consultations before `c307bb7` were produced under a false statement, and 56 (94.9%)
carried it in the form that mattered** — the prompt promised a trail that was not armed. The bias
has a **known direction: toward HOLD.**

**DECISION: the §2.4 activation criterion restarts from `c307bb7` (2026-07-29 13:21 UTC).
Progress goes from 2 of ~10 back to 0 of ~10. Your view is right and I agree with it.**

Why, and the caveat that cuts against it — stated because leaving it out would be the same sin:

- The criterion was written down **in advance so the bar could not be moved after seeing results**.
  A sample generated under a known directional bias is exactly what that discipline exists to
  exclude. Accepting it would mean the first thing we ever did with an un-gameable criterion was to
  admit evidence we know was skewed.
- Both closed datapoints are affected. vpos 82 received **no `close` verdict at all** — precisely
  what a hold-bias produces. vpos 83's first `close` came while the position was below +1R, i.e.
  under the false promise throughout.
- 🔴 **The caveat: restarting discards the datapoint that FAVOURED the advisor** — vpos 83's first
  close verdict beat the actual exit by ~159 USDT. So the restart is **conservative against the
  advisor**, not for it. A truthful prompt might plausibly have produced an *earlier* close there,
  which would have been better still — meaning the bias may have been costing the advisor credit
  rather than lending it. That is speculation. The direction of the bias is knowable; its effect on
  any single verdict is not, and a criterion this deliberate should not rest on a guess either way.

The 59 pre-fix consults keep their value as a record of what the advisor said and why. They are
simply **not admissible evidence for the go-live decision**. And the standing rule holds: **do not
re-cut this sample later to reach ~10 sooner** — that is the move the criterion forbids.

---

## STATE AT CLOSE

`git status` clean · HEAD **`c307bb7`** · pushed · `titan.service` **active** since 13:21:47 UTC,
**0 errors** · hourly + armed-exit consultations firing (13:30:08) · **Mercury-SOL untouched and
active**

**Book: 1 open position** — vpos 84 LONG @ 63,997.3, stop 63,129.9 (original), trail **not armed**
(MFE 0.806R, would arm at 64,864.7), partial not fired.

OPEN-ITEMS updated and pushed — §2.12 and §2.13 **closed**, §2.18 **opened**, §6/§7 at `c307bb7`.
Byte-identical dated snapshot: `reports/2026-07-29-1335-open-items.md`.

**Titan is done for now.** The two remaining known items are both parked deliberately and neither
blocks anything: the live-parity rewrite (§1, seven divergences, blocked by nothing while
`LIVE_TRADING_ENABLED=False`) and `Long/Short ratio` (§2.14, a prompt line with no producer — delete
or implement, your call). Mercury-SOL next.
