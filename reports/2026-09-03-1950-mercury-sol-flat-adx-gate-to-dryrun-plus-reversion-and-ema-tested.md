# mercury-sol-flat-adx-gate-to-dryrun-plus-reversion-and-ema-tested

_2026-09-03 19:50 UTC_

---

# FLAT-ADX GATE → DRYRUN, AND THE TWO QUESTIONS ITS 372 REFUSALS COULD STILL ANSWER

**Titan pre-flight `tools/openitems_guard.py` → exit 0.** Titan otherwise untouched.
Acts on §6 of my own `2026-09-03-1910` report, which named DRYRUN as the only state that makes this
decidable.

**Part 1 APPLIED. Parts 2 and 3 are read-only and propose nothing.**

---

# 🔴 THE VERDICT, FIRST

**1. APPLIED, one line, from flat.** `FLAT_ADX_GATE_DRYRUN = False → True` at 19:43 UTC; service
restarted 19:45:36 on a venue the bot's own boot line asserts FLAT. `FLAT_ADX_GATE_ENABLED` stays
True, so the gate still computes and prints its verdict. AST: **139 module constants parsed before
and after, exactly one changed.** Every guarded constant identical. No other file touched.

**2. 🔴 THE DRYRUN PATH DOES RECORD — but not the way the brief assumed, and the difference matters.**
There is **no** `would-refuse` status marker on the row: everything that writes one sits inside
`if not FLAT_ADX_GATE_DRYRUN:`. What survives is **the number**: `trades.srv_adx_1h` is written on
the advisor path (`main.py:5172`) and `skip_attribution.srv_adx_1h` on both the `book_blocked`
(`main.py:5041`) and `ai_skipped` (`main.py:5299`) paths. **"Would have been refused" is therefore
exactly reconstructible as `srv_adx_1h < 20.0` — the same value, from the same `_adv_snap`, that the
gate itself reads.** The paired within-session comparison is available. This pass buys what it was
meant to buy.

**3. 🔴 WAS IT MANIPULATION? NO — and the operator's own case is the clearest evidence against it.**
At a 1-hour horizon only **2.1 % of LONG refusals and 6.7 % of SHORT refusals** spike-and-revert.
Even at 24 hours it is 49.5 % / 37.2 %, i.e. a coin. **On 2026-09-03, 12 of the 14 refusals HELD at
every horizon out to 24 h.** The move the operator watched did not revert: it ran 101.17 → 105.62
and stood at **105.18 at 18:55**. **The gate was refusing a real trend that day, not a fakeout.**

**4. 🔴 EMA: THE OPERATOR IS RIGHT ABOUT 09-03 AND THE POPULATION STILL REFUSES TO CONFIRM IT.**
On every one of the 14 refusals that day the 1h **EMA9 was above EMA21**, the cross was 5–12 bars
old, and the EMA9 slope was **positive and accelerating** (+0.1358 → +0.1015 → +0.1496 %/bar) while
ADX read **14.81–19.04**. The EMA saw a trend beginning that ADX could not. That is the concrete case
for his hypothesis and it is real.
**And the one declared candidate — `EMA9_SLOPE_AGREES` — clears Bonferroni on LONG at p = 0.00003
(+0.492R vs −0.045R) and then FAILS the controls harder than anything in the previous study:
2 windows correct, 3 windows WRONG, 7 unusable. It is the first candidate in this project to get the
sign actively backwards in a majority of the windows that could be evaluated at all.** On SHORT it
runs negative (−0.207R in the FLAT leg) and it admits 55.7 % of longs against 31.7 % of shorts —
**the side-ban shape this codebase already condemned once.**

**Nothing from Parts 2 or 3 is proposed. The dryrun is the experiment; it starts now.**

---

# 1. THE APPLY

## 1b. 🔴 What the dryrun path actually records — checked BEFORE applying

```python
        _flat_adx = _adv_snap.get('srv_adx_1h')
        if FLAT_ADX_GATE_ENABLED and isinstance(_flat_adx, (int, float)) \
                and _flat_adx < ADX_BELOW_FLOOR:
            _fa_line = (f"[FLAT-ADX-GATE] "
                        f"{'DRYRUN would-refuse' if FLAT_ADX_GATE_DRYRUN else 'REFUSE'} "
                        f"{direction} row={row_id} ADX(1h,200)={_flat_adx:.2f} < "
                        f"{ADX_BELOW_FLOOR:.1f}")
            print(f"{LOG_PREFIX}{_fa_line}", flush=True)
            if not FLAT_ADX_GATE_DRYRUN:
                ...update_trade(status='flat_adx_blocked', srv_adx_1h=_flat_adx, ...)
                ..._record_skip_attribution(...)
                ...send_tg(...)
```
— `main.py:4922-4968`.

| what | in dryrun? | where |
|---|---|---|
| stdout line `DRYRUN would-refuse … row=N ADX(1h,200)=X < 20.0` | **YES** | `main.py:4925-4929`, printed before the branch |
| `trades.status = 'flat_adx_blocked'` marker | **NO** | inside `if not FLAT_ADX_GATE_DRYRUN` |
| `skip_attribution` row from THIS gate | **NO** | same block |
| Telegram refusal card | **NO** | same block |
| **`trades.srv_adx_1h` — the ADX it read** | **YES**, on the advisor path | `main.py:5172` |
| **`skip_attribution.srv_adx_1h`** | **YES**, on `book_blocked` and `ai_skipped` | `main.py:5041`, `main.py:5299` |

**Assessment, stated before applying:** there is no explicit marker, but the **number** is persisted
on every proposal that now flows past the gate, and the gate's own predicate is a pure comparison of
that number against a constant. `srv_adx_1h < 20.0` reproduces the verdict exactly. The paired
comparison — refused-and-admitted proposals coexisting in one session — is available in the DB.

🔴 **One caveat recorded rather than glossed:** the printed line lives in journald, and this box's
journal currently retains only back to **2026-08-31** (309 MB, rotating ≈ 3.5 days). It is **not** a
durable store for a 14-day experiment. It is also not needed, because `srv_adx_1h` is in SQLite.

## 1c. The change, and the AST verification

`.bak` → `config.py.bak_flatadx_dryrun_20260903_1930`. Diff against it:

```diff
-FLAT_ADX_GATE_DRYRUN  = False   # 🔴 ARMED. This gate REFUSES ENTRIES.
+FLAT_ADX_GATE_DRYRUN  = True    # 🔴 DRYRUN since 2026-09-03 19:30 — LOGS, DOES NOT REFUSE.
```

🔴 **The comment on that same line was corrected in the same edit and I am naming it rather than
letting it pass as "one line".** Leaving `# 🔴 ARMED. This gate REFUSES ENTRIES.` beside a value of
`True` would have created exactly the lying-label defect this codebase has closed four times. It is
still one line, and the line below it (`True = log + card only, never blocks.`) is a legend that
stays correct.

AST parse of both files (**parsed, never imported**):

```
module-level constants parsed: before=139 after=139
CHANGED: {'FLAT_ADX_GATE_DRYRUN': (False, True)}
🔴 EXACTLY ONE CONSTANT CHANGED, False -> True: True
```

| guarded constant | before | after | |
|---|---|---|---|
| `SL_BUFFER_ATR` | 2.5 | 2.5 | OK |
| `TRAIL_MULT_ATR` | 1.875 | 1.875 | OK |
| `TRAIL_ARM_R` | 0.75 | 0.75 | OK |
| `CONFLUENCE_SCORE_THRESHOLD` | 2.0 | 2.0 | OK |
| `ADX_BELOW_FLOOR` | 20.0 | 20.0 | OK |
| `EXIT_ADVISOR_DRYRUN` | True | True | OK |
| `PARTIAL_AT_ARM_ENABLED` | False | False | OK |
| `MAX_POSITIONS_PER_SIDE` | 1 | 1 | OK |
| `LIVE_FIXED_MARGIN` | 20 | 20 | OK |
| `LEVERAGE` | 5 | 5 | OK |
| `PAPER_FIXED_MARGIN` | 2000 | 2000 | OK |
| `FLAT_ADX_GATE_ENABLED` | True | True | OK |
| `BOOK_GATE_ENABLED / DRYRUN / WALL_PCTL / WALL_DIST_PCT / LEAN_FLOOR / MIN_SUPPORTING` | True / False / 90.0 / 0.2 / {LONG 0.4238, SHORT 0.3489} / 1 | identical | OK |

**Both advisor prompts: untouched.** They live in `claude_advisor.py`; a filesystem scan of the whole
directory shows **`config.py` is the only `*.py` modified** in this session.

## 1d. Applied from flat — five checks

| # | check | result |
|---|---|---|
| 1 | `virtual_positions` where `status='open'` | **0** |
| 2 | `active_positions` rows | **0** |
| 3 | `exit_pending` rows | **0** (and 0 `pending`/`failed` trades since 09-01) |
| 4 | **Bybit position index `positionIdx=1` (LONG)** | **contracts 0.0** |
| 4 | **Bybit position index `positionIdx=2` (SHORT)** | **contracts 0.0** |
| 5 | open orders / stop orders | **0 / 0** |

Re-checked immediately before the restart: still flat. The bot's own boot line agrees:
`[BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible`, and
`[VPOS-RECONCILE] no open positions at boot — clean.`

Restart 19:45:36 UTC, `ExecMainPID=3442516`, `ActiveState=active`, `SubState=running`,
**`NRestarts=0`**. Geometry re-asserted at boot:
`SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h`.

*(Unrelated, observed not caused: `systemctl` reports `NeedDaemonReload=yes`. The unit file is dated
**2026-06-03** and was not touched here. I did not run `daemon-reload` — outside this brief's scope,
and the service is running correctly.)*

## 1e. 🔴 PRE-REGISTRATION — recorded now, before it runs

### The live baseline, stated exactly so it cannot be reconstructed later

**Live book (`is_paper = 0`), all closed positions, as of 2026-09-03 19:45 UTC:**

| | |
|---|---|
| **n** | **14** |
| **ΣR** | **+6.141R** |
| **Σ$** | **+$15.56** |
| **win rate** | **6/14 = 42.9 %** |
| **mean** | **+0.439R** |
| entry rate | **14 entries / 26.4 days = 0.53 entries/day** |

vpos 29 +1.355R · 30 +0.762R · 31 −1.155R · 32 −0.180R · 33 −0.049R · 34 −0.643R · 35 −0.701R ·
36 −0.757R · 37 −1.226R · 38 +4.031R · 39 +1.604R · 40 +2.549R · 41 +1.633R · 42 −1.083R.

### Expected entry rate under dryrun

The gate refused **48.2 %** of proposals reaching it, so a naive multiple is 1/(1−0.482) = **1.93×**.
🔴 **I do not expect 1.93×, and here is why, stated in advance.** The newly-admitted proposals go
straight to the book gate and then the advisor, and the advisor already refuses flat markets on its
own: `config.py:345-348` records that it skipped **1,242 of 1,263 sub-20 consultations — 98.3 %**.
Applying that 1.7 % execution rate to ~21 additional consultations/day gives roughly **+0.3
entries/day**.

> **PREDICTION: 0.8 – 1.1 entries/day, i.e. a multiple of 1.5 – 2.0× with a central estimate of
> ≈ 1.7×, not 1.93×. If the realised rate lands at or above 1.9× that is a finding about the advisor,
> not about the gate.**

### 🔴 STOPPING RULE, RECORDED NOW

> **Return `FLAT_ADX_GATE_DRYRUN` to `False` at −3R on the live book measured from the +6.141R
> baseline above (i.e. at a live ΣR of +3.141R), OR at 2026-09-17 19:45 UTC (14 days), WHICHEVER
> COMES FIRST.**

## 1f. Size

Unchanged. `LIVE_FIXED_MARGIN = 20` × `LEVERAGE = 5` = **$100 notional**, both verified identical in
the AST table above.

## Current state

ADX(1h) on the last closed bars is **22.33 → 25.03 → 27.54 → 29.91** — well above the floor, so the
gate has had nothing to log since the restart (**0** `FLAT-ADX-GATE` lines). **The experiment
produces its first data on the next flat session**, which on the day-switch structure means the next
flat day, not the next hour.

---

# 2. 🔴 WAS IT MANIPULATION? TESTED ON ALL 372

## 2b. The definition, fixed before computing

ATR(1h)/price across the 372 refusals: **p10 = 0.47 % · median = 0.91 % · p90 = 1.52 %.**

> **X := the MEDIAN of that distribution = 0.91 %. Derived from the ATR distribution, not picked.**
> **REVERTED(h)** — from the refusal price P, price first moves ≥ 0.91 % **in the signal's favour**,
> then trades back **through P**, both within h hours.
> **HELD(h)** — reached the excursion and never came back through P within h.
> **NEVER(h)** — never reached the excursion within h.

## 2a. The counts, per side

| side | h | REVERTED | HELD | NEVER |
|---|---|---|---|---|
| LONG | 1h | **4 (2.1 %)** | 20 (10.4 %) | 168 (87.5 %) |
| LONG | 4h | 27 (14.1 %) | 47 (24.5 %) | 118 (61.5 %) |
| LONG | 12h | 66 (34.4 %) | 68 (35.4 %) | 58 (30.2 %) |
| LONG | 24h | 95 (49.5 %) | 62 (32.3 %) | 35 (18.2 %) |
| SHORT | 1h | **12 (6.7 %)** | 15 (8.3 %) | 153 (85.0 %) |
| SHORT | 4h | 25 (13.9 %) | 28 (15.6 %) | 127 (70.6 %) |
| SHORT | 12h | 49 (27.2 %) | 46 (25.6 %) | 85 (47.2 %) |
| SHORT | 24h | 67 (37.2 %) | 54 (30.0 %) | 59 (32.8 %) |

Conditional on the move actually getting going (reached the excursion), the share that then reverted:

| side | 1h | 4h | 12h | 24h |
|---|---|---|---|---|
| LONG | 4/24 = **16.7 %** | 27/74 = 36.5 % | 66/134 = 49.3 % | 95/157 = **60.5 %** |
| SHORT | 12/27 = **44.4 %** | 25/53 = 47.2 % | 49/95 = 51.6 % | 67/121 = **55.4 %** |

## 2d. 🔴 The answer, as a count and not an impression

**The manipulation signature is a fast spike that snaps back. At 1 hour it appears in 2.1 % of LONG
refusals and 6.7 % of SHORT refusals.** At 24 hours the reversion rate rises to a coin (49.5 % /
37.2 % of all refusals; 60.5 % / 55.4 % of those that moved at all) — but that horizon no longer
describes a fakeout, it describes normal two-day mean reversion that the trail and the breakeven lock
already price. The independent replay bears this out: the LONG refusals still totalled **+48.80R**
across exactly this population.

**The gate is NOT sitting on a population of one-hour fakeouts. It is refusing ordinary moves, about
half of which eventually come back and about half of which do not.**

## 2c. 🔴 The 2026-09-03 case specifically

14 refusals, all LONG. Last tape print **09-03 18:55 = 105.18**.

| time | P | 1h | 4h | 12h | 24h |
|---|---|---|---|---|---|
| 07:30 | 100.77 | NEVER | NEVER | **HELD** | **HELD** |
| 07:40 | 100.88 | NEVER | NEVER | **HELD** | **HELD** |
| 11:00 | 100.32 | NEVER | **HELD** | **HELD** | **HELD** |
| 11:40 | 100.78 | NEVER | **HELD** | **HELD** | **HELD** |
| 11:45 | 100.87 | NEVER | **HELD** | **HELD** | **HELD** |
| 11:50 | 100.80 | NEVER | **HELD** | **HELD** | **HELD** |
| 12:15 | 100.90 | NEVER | **HELD** | **HELD** | **HELD** |
| 12:20 | 100.68 | **HELD** | **HELD** | **HELD** | **HELD** |
| 12:35 | 101.09 | NEVER | **HELD** | **HELD** | **HELD** |
| 13:00 | 101.44 | NEVER | **HELD** | **HELD** | **HELD** |
| 14:35 | 102.65 | **HELD** | **HELD** | **HELD** | **HELD** |
| 14:45 | 102.78 | **HELD** | **HELD** | **HELD** | **HELD** |
| 14:50 | 103.88 | REVERTED | REVERTED | REVERTED | REVERTED |
| 14:55 | 103.78 | REVERTED | REVERTED | REVERTED | REVERTED |

**Twelve of fourteen HELD at every horizon out to 24 hours. It did not revert.** The two that
reverted are the two taken nearest the top, at 103.88 and 103.78, which briefly tagged 105.62 and
then traded back through their own entry — a retrace, not a fakeout.

🔴 **This is evidence AGAINST the manipulation reading on the one case the operator watched, and I
state it as such rather than leaving the hypothesis open.**

---

# 3. 🔴 EMA — THE PARAMETER THE GATE DOES NOT READ

The gate's predicate is `if FLAT_ADX_GATE_ENABLED and _flat_adx < ADX_BELOW_FLOOR` — **no EMA term
appears in it.**

## 3d. The ONE candidate, named before the numbers

> 🔴 **`EMA9_SLOPE_AGREES`** — the **1h EMA9 slope over the last 3 closed bars** points the SAME WAY
> as the proposed trade. Companion form: admit a sub-20-ADX entry only when this holds.
> One term. Directional, so it cannot become a side ban by construction. Uses the bot's own
> `SLOPE_LOOKBACK = 3` (`indicators.py:56`) rather than a fitted lookback. Instantaneous where ADX
> is a lag.
> **It is NOT the 2026-08-07 EMA-ENVELOPE gate ("both 1h and 15m gaps Expanding"), which was ported
> to SOL, admitted 0 of 9 LONGs and was refuted. That form is dead and is not re-run.**

Buckets declared before any outcome was looked at. |EMA9 slope(1h)| over the 372:
median **0.0803 %/bar** (p10 0.0118, p90 0.1942) — the shallow/steep split point is that median, a
derived number, not a chosen one. All quantities use **closed bars only**, so there is no look-ahead.

## 3a/3b. The descriptive splits (nothing below n=8 ranked)

### EMA9/21 cross recency — 1h

| side | ≤6 bars | 7–24 | >24 |
|---|---|---|---|
| LONG | n=64 **−0.036R** win 42.2 % | n=100 +0.230R win 64.0 % | n=28 **+1.003R** win 75.0 % |
| SHORT | n=64 −0.002R win 48.4 % | n=76 −0.750R win 30.3 % | n=40 **−1.029R** win 7.5 % |

### EMA9/21 cross recency — 15m

| side | ≤6 bars | 7–24 | >24 |
|---|---|---|---|
| LONG | n=67 **+0.604R** win 74.6 % | n=77 +0.201R | n=48 −0.149R |
| SHORT | n=49 −0.545R | n=101 −0.482R | n=30 −0.764R |

🔴 The two horizons point in **opposite directions on LONG**: a *stale* 1h cross (>24 bars) and a
*fresh* 15m cross (≤6 bars) both look good. That is not one mechanism; it is two slices of the same
handful of trending days.

### EMA9 slope (1h) — the tested candidate

| side | DISAGREES | AGREES shallow (<0.0803) | AGREES steep (≥0.0803) |
|---|---|---|---|
| LONG | n=85 −0.045R win 44.7 % | n=49 **+0.661R** win 79.6 % | n=58 +0.349R win 60.3 % |
| SHORT | n=123 −0.595R win 30.1 % | n=34 **−0.843R** win 11.8 % | n=23 +0.156R win 69.6 % |

### |price − EMA9(1h)| in ATR

| side | pinned <0.5 | 0.5–1.5 | stretched ≥1.5 |
|---|---|---|---|
| LONG | n=95 +0.253R | n=87 +0.201R | n=10 +0.731R |
| SHORT | n=85 **−0.877R** win 15.3 % | n=82 −0.254R | n=13 −0.225R |

### |price − EMA21(1h)| in ATR

| side | pinned <0.5 | 0.5–1.5 | stretched ≥1.5 |
|---|---|---|---|
| LONG | n=80 +0.111R | n=80 **+0.622R** win 72.5 % | n=32 −0.309R |
| SHORT | n=34 **−0.919R** win 8.8 % | n=123 −0.485R | n=23 −0.320R |

### The candidate, headline

| side | | n | ΣR | mean | win | Σ$ |
|---|---|---|---|---|---|---|
| LONG | **AGREES** | 107 | **+52.66** | **+0.492R** | **69.2 %** | +$163.15 |
| LONG | DISAGREES | 85 | −3.87 | −0.045R | 44.7 % | −$7.45 |
| | **spread** | | | **+0.538R** | | **nominal p = 0.00003 → PASSES Bonferroni (α = 0.00167)** |
| SHORT | AGREES | 57 | −25.08 | −0.440R | 35.1 % | −$52.45 |
| SHORT | DISAGREES | 123 | −73.23 | −0.595R | 30.1 % | −$141.13 |
| | spread | | | +0.155R | | nominal p = 0.298 → **fails** |

Note what it separates even where it "passes": **DISAGREES is −0.045R, not a loss.** The candidate
tells good from *neutral*, not good from bad.

## 3c. 🔴 WHERE THE EMA WAS ON 2026-09-03 — the operator's case, with the numbers

| time | P | ADX read | EMA9(1h) | EMA21(1h) | cross 1h | cross 15m | slope %/bar | agrees | \|P−EMA9\| ATR |
|---|---|---|---|---|---|---|---|---|---|
| 07:30 | 100.77 | 19.04 | 100.44 | 100.06 | 5 | 54 | **+0.1358** | **YES** | 0.34 |
| 07:40 | 100.88 | 19.04 | 100.44 | 100.06 | 5 | 54 | **+0.1358** | **YES** | 0.46 |
| 11:00 | 100.32 | 15.36 | 100.38 | 100.15 | 9 | 5 | −0.0130 | no | 0.07 |
| 11:40 | 100.78 | 15.32 | 100.38 | 100.15 | 9 | 7 | −0.0130 | no | 0.44 |
| 11:45 | 100.87 | 15.32 | 100.38 | 100.15 | 9 | 0 | −0.0130 | no | 0.54 |
| 11:50 | 100.80 | 15.43 | 100.38 | 100.15 | 9 | 0 | −0.0130 | no | 0.46 |
| 12:15 | 100.90 | 14.81 | 100.45 | 100.20 | 10 | 2 | +0.0015 | YES | 0.51 |
| 12:20 | 100.68 | 14.86 | 100.45 | 100.20 | 10 | 2 | +0.0015 | YES | 0.26 |
| 12:35 | 101.09 | 15.55 | 100.45 | 100.20 | 10 | 3 | +0.0015 | YES | 0.70 |
| 13:00 | 101.44 | 16.47 | 100.68 | 100.33 | 11 | 5 | **+0.1015** | **YES** | 0.84 |
| 14:35 | 102.65 | 18.42 | 100.83 | 100.43 | 12 | 11 | **+0.1496** | **YES** | 1.80 |
| 14:45 | 102.78 | 18.42 | 100.83 | 100.43 | 12 | 12 | **+0.1496** | **YES** | 1.84 |
| 14:50 | 103.88 | 18.42 | 100.83 | 100.43 | 12 | 12 | **+0.1496** | **YES** | 2.86 |
| 14:55 | 103.78 | 18.97 | 100.83 | 100.43 | 12 | 12 | **+0.1496** | **YES** | 2.60 |

🔴 **The EMA said "trend, and up" on all fourteen: EMA9 above EMA21 throughout, a bullish cross 5–12
bars old, the pair widening from 100.44/100.06 to 100.83/100.43, and the slope going
+0.1358 → +0.1015 → +0.1496 %/bar. ADX said 14.81–19.04 and refused every one.**
The operator's hypothesis is **correct on this day**, and the mechanism is exactly the one he named:
ADX is a doubly-smoothed level and the EMA pair is an already-completed event.

*(The 11:00–11:50 block is the honest exception: the 1h slope was fractionally negative there, so the
candidate would have refused those four too.)*

---

# 4. THE CONTROLS

**Bonferroni:** 15 buckets × 2 sides = **30 tests**, **α = 0.05/30 = 0.00167**, declared before results.

**🔴 Stated up front, as instructed:** the day-switch structure — 10 days at 0–5.9 % refusal, 8 days
at 61.7–100 % — will leave most 12-windows unusable, exactly as it did in `2026-09-03-1910`. The
count of **evaluable** windows is reported, not hidden behind a pass/fail.

## 12-window sign stability — `EMA9_SLOPE_AGREES`

| side | per-window spread | correct | wrong | unusable | **evaluable** | result |
|---|---|---|---|---|---|---|
| LONG | w1 −0.02 · w4 +0.81 · w5 +0.28 · w9 −0.32 · w11 −0.01 | **2/12** | **3/12** | 7/12 | **5/12** | 🔴 **FAILS** |
| SHORT | w9 +0.04 · w11 −0.55 | 1/12 | 1/12 | 10/12 | 2/12 | 🔴 **FAILS** |

🔴 **This is worse than the previous study's survivors.** Those never disagreed in an evaluable
window; this one **gets the sign backwards in 3 of the 5 windows that can be evaluated at all**. A
+0.538R aggregate spread that flips sign across most of its own timeline is not a discriminator.

## Regime test — both legs must be populated

Population: **FLAT 322 / TREND 50.**

| side | FLAT leg | TREND leg |
|---|---|---|
| LONG | n(agree)=81 **+0.632R** vs n(disagree)=82 −0.008R → spread **+0.639R** | n(agree)=26, n(disagree)=**3** → 🔴 NOT POPULATED |
| SHORT | n(agree)=36 **−0.802R** vs n(disagree)=123 −0.595R → spread **−0.207R** | n(agree)=21, n(disagree)=**0** → 🔴 NOT POPULATED |

**The TREND leg cannot be populated on either side — for SHORT the disagree bucket is literally
empty. And in the one leg that IS populated, the candidate runs BACKWARDS on shorts.**

## Paper vs live

🔴 **Does not exist for this gate. All 372 refusals are `is_virtual = 0` (live book); the last paper
position opened 2026-08-06 and the gate armed 2026-08-17. PAPER n = 0 on both sides.** Saying it
again rather than substituting a time split, as instructed.

## Shape check — would it be a side ban?

| side | admitted by the candidate | their ΣR |
|---|---|---|
| LONG | **107 of 192 = 55.7 %** | +52.66 |
| SHORT | **57 of 180 = 31.7 %** | **−25.08** |

It admits nearly twice the share of longs as shorts, and the shorts it admits **lose money**. As a
companion condition it would function as a long-only relaxation. `config.py`'s own standing rule —
*"a side ban is not a rule (the same test that condemned a nominal p85 wall percentile)"* — applies
to it directly.

---

# 5. WHAT THIS LEAVES

- **The gate is in DRYRUN and the experiment is running.** It is the only state in which a refused
  and an admitted proposal coexist in one session, which is the comparison every previous pass
  lacked. First data arrives on the next flat session.
- **Manipulation is not the explanation.** 2.1 % / 6.7 % one-hour reversion, and 12 of 14 HELD on
  09-03.
- **The EMA hypothesis is right about 09-03 and unproven across the population.** It produced the
  strongest single split measured on this data (+0.538R, p = 0.00003) and then failed the sign
  stability control more decisively than anything before it.
- **Nothing is proposed.** Parts 2 and 3 changed nothing and recommend nothing.

---

# 6. 🔴 CONFIRMATION

| claim | evidence |
|---|---|
| Titan | `openitems_guard.py` exit 0; not touched otherwise |
| the ONE applied change | `config.py:407` only, `FLAT_ADX_GATE_DRYRUN False → True`; AST 139/139 constants, exactly one differs |
| every guarded constant | identical before/after (table in §1c) — including `ADX_BELOW_FLOOR`, `MAX_POSITIONS_PER_SIDE`, `LEVERAGE`, `LIVE_FIXED_MARGIN`, all `BOOK_GATE_*` |
| both advisor prompts | untouched — they are in `claude_advisor.py`; `config.py` is the only `*.py` modified |
| applied from flat | five checks, all zero, **both Bybit position indices at contracts 0.0**; bot's own `BOOT-ASSERT venue FLAT` |
| no orders placed or cancelled | no venue write call issued; authenticated reads were `fetch_positions` / `fetch_open_orders` only |
| DB | all analysis connections `file:/…/trades.db?mode=ro`, SELECTs only |
| config not imported | `config.py` **parsed with `ast`** and read with `sed`/`grep`; never imported |
| service | restarted **once, deliberately**, to load the constant: 19:45:36 UTC, PID 3442516, active/running |
| `NRestarts` | **0** before, **0** after |
| size | $20 × 5 = **$100**, unchanged |
| backup | `config.py.bak_flatadx_dryrun_20260903_1930` |
