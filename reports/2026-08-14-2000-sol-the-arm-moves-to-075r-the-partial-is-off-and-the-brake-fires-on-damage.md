# Mercury-SOL — the arm moves to 0.75R, the partial is off, and the brake now fires on damage

**2026-08-14 20:00 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · APPLIED and RESTARTED from FLAT · worker pid 2195271**

Titan (`/root/titan-bot`): **HEAD `897850b`, working tree clean, MainPID 2538048 unchanged, NRestarts 0, uptime unbroken since 2026-08-06 01:53:19. Zero `.py` files under its directory modified.** Directory-scoped harness, §5.

Acts on [19:30 §3a, §3d and §4a](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-14-1930-sol-the-payoff-ratio-is-the-defect-and-the-moves-are-not-there.md).

---

## ⚡ WHAT LANDED

1. **The arm moves to +0.75R** — `TRAIL_ARM_R = 0.75`, a new constant. **1R did not move**: `SL_BUFFER_ATR` is still 2.5, the stop is still a full 1R away, and every R-multiple in every past and future report remains directly comparable. **No §0 boundary is needed.**
2. **🔴 The 0.50R sweep maximum was refused, and the refusal is written into the constant's own comment** with the four peak values that make it a fence — so a future session that reruns the sweep and finds 0.50R again reads *why* finding it is not evidence.
3. **The partial is off** behind its existing named flag (`PARTIAL_AT_ARM_ENABLED = False`). **Code not deleted** — `_apply_partial_at_arm`, its quantisation path, its fee accounting and the close-card fields are all untouched and re-armable by one flag.
4. **The loss-streak brake keeps its threshold and its 4-hour cooldown and gains two conditions**: a **45.1 h recency window** (p25 of every rolling-triple span in the book) and a **−2.05R money floor** (p10 of every rolling-triple ΣR). Both derived, neither round. **Replayed over the whole book it fires once instead of six times**, and today's 15:30 halt and the 2026-08-07 one both die.
5. **🔴 Three strings that would have become lies were fixed with them** — the exit-advisor prompt still said *"it arms only at +1R"*, the adoption card promised a partial market-sell that will never be sent, and the boot geometry line could not tell the old geometry from the new one.
6. **Two restarts, both reported.** The second existed only to load the boot-line change; it is named here rather than buried.
7. **Harness: 49 assertions, 49 PASS, 0 FAIL.** Three failed on the first run; **all three were harness bugs, corrected rather than removed**, and each is named in §5.

---

## 0. APPLY RECORD

| | |
|---|---|
| backups, md5-verified against the originals **before** any edit | `config.py.bak_geometry_20260814_1945` `d49974b4…` · `trail_arm.py…` `9c26653f…` · `main.py…` `89dd88e3…` · `virtual_trader.py…` `79aa49b4…` · `trades.db.bak_geometry_20260814_1945` (55,480,320 B) |
| files changed | **exactly four**, all inside `mercury-sol`: `config.py` (+121/−3), `trail_arm.py` (+15/−3), `main.py` (+67/−9), `virtual_trader.py` (+13/−5) |
| compile | `py_compile` clean on all four **plus `book_gate.py` and `claude_advisor.py`**, to a **TEMP** directory — no `.pyc` written into production by me |
| DB write | **NONE.** `trades` max id unchanged across both boots; no close row, no reconcile |
| restart #1 | 19:52:51 → active 19:52:53, from **FLAT on all three books** (registry 0, `virtual_positions` 0, **venue 0 — read live over Tor**) |
| restart #2 | 19:54:35 → active 19:54:37 — **the boot-line change only**, see §4 |
| boot | clean both times: `[AP] No active positions in DB — clean boot` · `[BOOT-ASSERT] venue FLAT` · `unregister=yes` · **0 tracebacks, 0 assertion errors** |
| harness | **49 / 49 PASS** |

---

# 1. THE ARM MOVES TO +0.75R

## 1a. Why 0.75R and not the 0.50R the sweep prefers

The reasoning is not in this report only — it is in the constant's comment, verbatim, because that is the file a future session actually opens:

```python
# 🔴 WHY 0.75R AND NOT 0.50R, WHICH IS WORTH MORE. THIS IS THE POINT OF THE COMMENT
# AND NO FUTURE SESSION MAY "IMPROVE" IT BACK BY RERUNNING THE SWEEP.
# The sweep's best cell IS 0.50R, at +4.420R against +2.328R here. It was REFUSED on
# purpose. Four of the six positions carrying that cell have peaks between 0.510R and
# 0.568R (vpos 28 0.510, vpos 32 0.553, vpos 12 0.561, vpos 23 0.568): an arm at 0.50R
# sits just underneath that cluster and an arm at 0.60R sits just above it, so the cell
# is a fence built around four trades. Its neighbours at 0.40R and 0.60R are 2.27R and
# 2.00R worse. That is a FITTED MAXIMUM, and it is the same shape that killed the ADX
# grid, the +4h exit sweep and twenty-six earlier candidates.
#
# WHAT IS TAKEN IS THE DIRECTION, WHICH THE SAME SWEEP ESTABLISHES WITHOUT OVERLAP:
#   all SIX arm cells below 0.90R  ->  ΣR in [−4.697, −1.510]
#   all FOUR cells at or above 1.0R ->  ΣR in [−6.203, −5.818]
# no cell in the first group is worse than any cell in the second. 0.75R is the cell
# NEAREST the current setting that is still inside that established region — the most
# conservative step into it. The 2.09R difference from the maximum is GIVEN UP
# DELIBERATELY, and re-running the sweep will find that maximum again; finding it is
# not evidence, it is the same four trades.
```

The harness asserts that text is present (§5, item 4), so a future edit that removes the reasoning fails a check rather than passing silently.

## 1b. 🔴 THE CONSTANT, AND THE PROOF THAT 1R DID NOT MOVE

**The governing constant is `trail_arm.activation_distance()`**, the single shared arm policy imported by `main.py` (live entry, exit-advisor prompt) and `virtual_trader.py` (poller, adoption). It was:

```python
return SL_BUFFER_ATR * atr                      # = the SL distance = 1R
```

and is now:

```python
return TRAIL_ARM_R * SL_BUFFER_ATR * atr        # = 0.75 × 1R
```

**`SL_BUFFER_ATR` is untouched at 2.5.** The stop is placed at `fill ∓ SL_BUFFER_ATR × atr`, so 1R — the denominator of every R-multiple this project has ever quoted — is exactly what it was. Verified at runtime in the booted configuration:

```
SL_BUFFER_ATR             2.5      <- UNCHANGED
TRAIL_ARM_R               0.75
at atr = 0.32 :  1R (stop distance) = 0.8000
                 arm distance       = 0.6000  = 0.7500 R
BE target LONG (+0.20%)             = +0.1500  <  arm +0.6000   -> no instant stop-out
```

🔴 **R before and after this change are directly comparable. No §0 boundary is required, and none is declared.** This constant is a *fraction of R*, not a redefinition of it. That distinction is why this change could be made at all — the 19:30 sweep held 1R fixed for exactly this reason.

**The import-time invariant moved with it.** `trail_arm.py` asserts that the arm sits strictly above the breakeven target at a measured ATR floor; left alone it would have gone on testing a 1.0R arm the code no longer uses — the precise failure its own comment block describes. It now reads `TRAIL_ARM_R * SL_BUFFER_ATR * ASSERT_MIN_ATR_PCT`: at the floor, **0.75 × 2.5 × 0.35 % = 0.656 % of entry against a 0.20 % BE target — still 3.3× clear.** The live process imported it without raising.

## 1c. What the arm triggers now, and in what order

At `active_price = fill ± 0.75R`, on the poller tick that crosses it:

```
1.  the BREAKEVEN LOCK fires   — mgmt_state.breakeven_applied = True
                                 the resting venue stop is MOVED to entry ± 0.20%
2.  the PARTIAL                — 🔴 NO LONGER FIRES (item 2). Nothing is sent.
3.  the TRAIL ARMS             — one-shot fresh-ATR trail_pct recompute, then the
                                 trail rides 0.75R behind the high-water mark
```

**Two things happen at the arm instead of three, and the position now carries its FULL size onto the trail.** That interaction is why the two changes were made together and why the shipped pair is worth more than either alone (§4).

## 1d. 🔴 THE CAVEAT THAT IS MOST LIKELY TO MAKE THIS UNDERDELIVER

Carried forward from 19:30 §4a and recorded **beside the constant**, not only here:

```python
# 🔴 THE MOST LIKELY WAY THIS UNDERDELIVERS, recorded here rather than discovered later.
# The replay that measured it walks 5m candles and checks the ADVERSE extreme against
# the OLD stop BEFORE arming, so within one bar it can both "not be stopped" and "arm".
# A live 10-second poller can arm and then be stopped at breakeven INSIDE the same bar.
# The replay is therefore mildly OPTIMISTIC exactly where this change gains — the eight
# green-then-red losers. If the realised effect is smaller than +2.328R, this is the
# first thing to suspect, and it is not a reason to lower the arm further.
```

---

# 2. THE PARTIAL IS OFF

## 2a–2b. The one monotone axis, and why an earlier arm makes removing it more urgent

```
partial   none      1/4      1/3 (was live)     1/2      full
ΣR      −5.393   −5.796        −5.930        −6.199   −7.005
Δ       +0.538   +0.134          0.000       −0.269   −1.075
```

**Monotone decreasing in the fraction taken — the only monotone axis of the four swept.** Monotone means there is no cell to tune to: the direction holds at every step, so this is applied where the arm-level *maximum* is not.

**And it had barely run: 3 fires in 29 positions** (vpos 25, 29, 30), because it fires at the arm and 69 % of the book never reached +1R. 🔴 **Moving the arm to 0.75R would have made it fire on 13 of 29 instead of 9 — and the sweep says more partial is worse, not better.** Leaving it on while moving the arm down would have amplified the one thing measured to hurt.

## 2c. Disabled behind a named flag; the code is intact

`PARTIAL_AT_ARM_ENABLED = False`. The flag already existed, so nothing new was introduced and nothing was deleted. Asserted by harness: `_apply_partial_at_arm` still defined, its quantisation line `_raw_qty = size * PARTIAL_AT_ARM_FRACTION` still present, the call site still gated on the flag, `PARTIAL_AT_ARM_FRACTION` preserved at ⅓ and inert. **Setting the flag True restores the prior behaviour byte-for-byte.** Same rule as the aligned relaxations at 18:28.

## 2d. The three paths checked for a world with no partial

| path | behaviour with no partial | evidence |
|---|---|---|
| **quantisation** | never entered — `_apply_partial_at_arm` is the only caller of the lot-step rounding | call site gated on the flag |
| **fee accounting** | `close_position` reads `float(row['partial_pnl'] or 0.0)` and `float(row['partial_fees'] or 0.0)`, so NULL → 0.0 and the identity `gross − fees == net` holds unchanged | source, asserted by harness |
| **close card** | the partial block is printed only `if partial_pnl or partial_fees`, so it is simply absent | source, asserted by harness |
| **exit-advisor prompt** | its Partial section reads `psize = row['partial_size']` and prints nothing when NULL | already conditional |
| 🔴 **adoption card** | **was broken and is fixed** — see below | |

🔴 **The adoption card announced a real order that will never be sent.** It printed, unconditionally: *"the engine will (1) MOVE THE VENUE STOP … and (2) MARKET-SELL ~X as the +1R partial. Both are REAL orders on REAL money."* With the partial off, no reduce order is sent. A card that promises a live order which does not happen is worse than no card, so it now states what the tick will actually do and names the flag when the partial is off.

---

# 3. THE LOSS-STREAK BRAKE — RECENCY AND A MONEY FLOOR

## 3a–3b. Both thresholds derived, neither chosen

**What the bare count actually did** — every firing over all 29 closed positions:

| fires after | vpos | R of each | **span** | **ΣR** | |
|---|---|---|---|---|---|
| vpos 10 (06-22) | 8, 9, 10 | −0.739, −0.264, −1.066 | **35.93 h** | **−2.069** | a real streak |
| vpos 24 (07-30) | 22, 23, 24 | −1.064, −0.577, −1.050 | 167.38 h | −2.690 | **7 days apart** |
| vpos 28 (08-07) | 26, 27, 28 | −1.085, −0.660, −0.153 | 95.34 h | −1.898 | **3.97 days apart** |
| vpos 33 (08-12) | 31, 32, 33 | −1.155, −0.180, −0.049 | 45.64 h | −1.383 | |
| vpos 34 (08-13) | 32, 33, 34 | −0.180, −0.049, −0.643 | 69.45 h | **−0.871** | three scratches |
| vpos 35 (08-14) | 33, 34, 35 | −0.049, −0.643, −0.701 | 50.50 h | −1.393 | **halted 4 h today** |

### (a) The recency window — **45.1 h**

The span of **every** rolling triple of closes in the book: min 20.92 h, **p25 45.13 h**, median **69.45 h**, p75 131.17 h, max 351.02 h.

**At this bot's close rate, three positions take about three days to accumulate.** "Three consecutive losses" is therefore the *normal spacing of any three trades*, not evidence about now. The window is set at the **25th percentile** — only the tightest quarter of triples is tight enough to be called a streak at all. **24 h was rejected**: 0 of 27 historical triples are that tight, which makes the brake unreachable rather than selective.

### (b) The money floor — **−2.05R**

ΣR over every rolling triple: **p10 −2.050R**, p20 −1.866R, p25 −1.564R, median −0.871R.

The floor is the **10th percentile** — the brake fires only when the damage is in the worst decile the book has produced. The arithmetic that makes it sane: the mean loser is −0.804R, so **three average losers total −2.41R and DO clear this floor**, while three scratches averaging −0.29R do not. A streak of three scratches is not the same event as three full stop-outs, and the brake now knows the difference.

## 3c. 🔴 EXPECTED FREQUENCY — replayed at every close in the book

The exact new logic was replicated and run at all 29 close instants:

```
after vpos  closed_at            book    losses/rows  damage R   OLD    NEW
        10  2026-06-22T01:25:56  paper      3/3        −2.069   HALT   HALT
        24  2026-07-30T12:03:30  paper      2/2        −1.627   HALT     -
        28  2026-08-07T06:00:10  paper      1/1        −0.153   HALT     -
        33  2026-08-12T13:00:19  LIVE       2/2        −0.228   HALT     -
        34  2026-08-13T17:12:26  LIVE       2/2        −0.692   HALT     -
        35  2026-08-14T15:30:13  LIVE       2/2        −1.344   HALT     -

OLD rule: 6 firings.    NEW rule: 1 firing.
```

🔴 **One of the six survives — the 2026-06-22 event, three losses inside 35.93 h for −2.069R, which is exactly what a loss-streak brake exists for.** Today's 15:30 halt and the 2026-08-07 one both fail *both* conditions.

**Expected frequency: ~1 halt per 29 closed positions ≈ 1 per 28 days at 1.02 entries/day**, against the current ~1 per 5 positions.

**And evaluated against the live book at 19:50 today:** 2 closes inside the last 45.1 h, 2 losses, damage −1.344R → **no halt**. Under the old rule the bot was blocked until 19:30Z.

## 3d. The brake is NOT removed

`LOSS_STREAK_THRESHOLD` stays **3**. `LOSS_STREAK_COOLDOWN_HOURS` stays **4**. The two new conditions are ANDed on top of the count, so they can only make it fire **less** — never more, and never on an error. Three implementation properties worth naming:

- 🔴 **The window is applied in SQL, before the `LIMIT`.** Filtering after `ORDER BY closed_at DESC LIMIT 3` would take the last three closes and *then* test their age — a different question that would still count a stale pair. Filtering first asks the right one: *are there three losses in the last 45.1 h?*
- 🔴 **R is per position, from each row's own `initial_risk_usdt`** — never a pooled denominator. A row with a null or zero risk contributes **nothing** rather than raising, so a malformed row can only make the brake fire less and can never crash a live entry path.
- 🔴 **A count-met-but-damage-too-small case is LOGGED, not silent**: `[STREAK] 3/3 recent losses within 45.1h but damage +X.XXXR is above the floor −2.05R — NOT halting`. A brake that declines to fire should leave the same trace as one that fires. **Every fail-closed path is preserved.**

---

# 4. PRE-REGISTRATION — written before it runs

## 4a. What is expected, including where the brief's prediction and the replay disagree

Replay of the **exact shipped pair** (arm 0.75R **and** partial off) through the same engine that reproduced the booked book at mean Δ +0.002R:

```
current geometry replay ΣR  −5.930      shipped ΣR  −2.962      Δ  +2.968
  (the report's separate cells were +2.328R and +0.538R; they interact, because
   removing the partial lets the FULL size ride the earlier-armed trail)
positions changed: 11   [7, 11, 13, 15, 17, 18, 21, 25, 26, 29, 33]
  SHORT  −2.235 -> −2.073   Δ +0.162        LONG   −3.695 -> −0.889   Δ +2.806
  paper  −5.150 -> −2.407   Δ +2.743        live   −0.780 -> −0.555   Δ +0.225
```

| pre-registered quantity | expectation |
|---|---|
| positions reaching the arm | **31.0 % → 44.8 %** of the book (9 → 13 of 29 on this history; SHORT 5→6, LONG 4→7, **live 2→3**) |
| full-1R stop-outs (replay R ≤ −0.85) | **10 → 8** |
| breakeven-ish scratches (\|R\| < 0.25) | **3 → 6** |
| mean winner | **+0.934R → +0.771R** (smaller, as expected) |
| payoff ratio | 1.16 → **0.95** |
| ΣR | −5.930 → −2.962 |
| `[STREAK]` halts | ~1 per 28 days, from ~1 per 5 positions |
| `[PARTIAL]` lines and partial rows | **exactly 0**, until the flag moves |

🔴 **One prediction in the brief is contradicted by the replay and I am recording it rather than quietly agreeing.** The brief expects *"a LOWER win rate with a SMALLER average loss"*. The replay says the **win rate RISES, 34.5 % → 44.8 %**, and the mean loser is essentially unchanged (−0.804 → −0.811). The reason is definitional: the breakeven lock parks the stop at entry **+0.20 %**, which is above the round-trip taker, so a scratch closes *marginally positive* (vpos 18 +0.069R, vpos 26 +0.039R, vpos 33 +0.027R) and counts as a "win" by sign. **The substance of the prediction is right — fewer full stop-outs, more scratches, a smaller average winner — only the sign of the scratch is different.** If the live win rate rises while ΣR does not improve, that is this artefact and not an edge.

## 4b. 🔴 THE STOPPING RULE — recorded now so it cannot be renegotiated later

> **20 FURTHER LIVE CLOSED POSITIONS.**
>
> **If the live book is still negative after them, the finding is that this signal set does not produce a positive expectancy on SOL, and the correct action is to STOP TRADING IT — not to look for a twenty-seventh candidate.**
>
> At 1.02 entries/day that is roughly **20 days**, i.e. on or about **2026-09-03**.
> The count is **closed live positions, from vpos 36 onward**, not signals, not days, and not "20 more once the next change lands".

## 4c. The live baseline, stated exactly so it is never reconstructed

```
live closed positions      7   (vpos 29–35)
ΣR (re-costed at 0.001)    −0.780
win rate                   28.6 %   (2 of 7)
mean winner                +0.969R
mean loser                 −0.544R
payoff                     1.78
expectancy                 −0.111R per trade
```

**The comparison at the stopping point is: the next 20 live closes, on the same re-costed basis, against ΣR ≥ 0.**

## 4d. 🔴 THE COUNTERWEIGHT — from this project's own §4c, not softened

```
live n = 7   mean −0.111R   sd 0.826   standard error 0.312R
95 % interval on the live mean:  [−0.724, +0.501] R
```

**That interval contains zero and most of the plausible range on both sides. Seven trades cannot tell a losing edge from a winning one.** Twenty more will not be conclusive either — at this sd, 27 trades give a standard error near 0.16R, so a −0.1R/trade edge and a +0.2R/trade edge remain inside one interval.

🔴 **The 20-trade rule exists because the question has to end somewhere, not because 27 trades will settle it.** It is a decision rule, not a significance test, and it is written down in advance precisely so that a marginal result cannot be re-argued into another window. Kelly on this book is **−0.219** — the size-optimal bet is already zero — and the honest reading is that these three changes buy the signal set one bounded, pre-registered chance to show a different number.

---

# 5. THE ISOLATION HARNESS — BY DIRECTORY. 49 ASSERTIONS, 49 PASS, 0 FAIL

**Why by directory:** both bots have a `config.py`, a `main.py` and a `virtual_trader.py`. A grep for a filename proves nothing about which bot it found.

```
1. TITAN — DIRECTORY-SCOPED, MUST BE UNTOUCHED
  [PASS] zero .py SOURCE files modified anywhere under /root/titan-bot
  [PASS] every changed path under Titan is one of ITS OWN runtime artefacts
         (trades.db · healthcheck_state.json · optimizer/tg_offset.txt · oi_cache.json)
  [PASS] HEAD 897850b · working tree clean · MainPID 2538048 · uptime unbroken · NRestarts 0

2. MERCURY-SOL — exactly ['config.py','main.py','trail_arm.py','virtual_trader.py'] changed
  [PASS] a .bak exists for every changed file + the DB

3. THE DEPLOYMENT GAP
  [PASS] worker booted 19:54:37 AFTER the newest changed file 19:54:21
  [PASS] 🔴 the RUNNING process's own boot line names the new geometry:
         geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF
                   ATR_TF=1h OBSERVATION_MODE=False [pid 2195271]
  [PASS] SL_BUFFER_ATR=2.5 still on the line (1R unchanged) · OBSERVATION_MODE=False (LIVE)

4. ITEM 1 (10)  TRAIL_ARM_R 0.75 · SL_BUFFER_ATR still 2.5 · arm == 0.75×1R at runtime ·
                stop still 1R · BE +0.1500 strictly inside arm +0.6000 · invariant tests the
                REAL arm · the 0.50R refusal AND the 5m-optimism caveat are in the comment
5. ITEM 2 ( 9)  flag False · fraction preserved · _apply_partial_at_arm still defined ·
                quantisation intact · call site gated · NULL partial fields coalesce to 0.0 ·
                close card conditional · adopt card fixed · exit prompt states the REAL arm
6. ITEM 3 (10)  window 45.1h · floor −2.05R · threshold 3 and cooldown 4h UNCHANGED ·
                window applied in SQL before the LIMIT · both conditions required ·
                declined-halt logged · per-position R · null-risk row cannot raise ·
                fail-closed preserved · derivations written into config
7. THE BOOK ( 8) registry empty · no open vpos · 29 closed, max vpos 35 · NO close row across
                either boot (only #18423 htf_blocked) · no reconcile branch · zero tracebacks ·
                LIVE mode on · the 18:28 pass's changes still loaded

RESULT: ALL PASS (49/49)
```

🔴 **Three assertions FAILED on the first run. All three were harness bugs, corrected rather than deleted, and named here:**

1. **`/root/titan-bot/oi_cache.json` was not in the Titan allowlist.** Investigated rather than waved through: it is written by **Titan's own `market_context.py`**, mtime 19:50:08, while this pass was editing a different directory. Added to the allowlist as a fourth known runtime artefact.
2. **`trail_arm.py` did not appear as changed** — its mtime is **19:39:50** and the scan window started at 19:40. The constant was wrong by ten minutes, not the file. Window moved to 19:35.
3. **The peak-cluster assertion looked for `'0.510R and 0.568R'`** as one string; in the file that phrase wraps across a comment line break. The check now asserts the two values and the two key phrases separately.

**A harness bent to pass is worse than no harness, so each correction is stated with what it was.**

---

# 6. THE THREE STRINGS THAT WOULD HAVE BECOME LIES

Fixed in the same pass, because a geometry change that leaves the machine describing the old geometry is the defect class this project keeps finding:

| where | said | now |
|---|---|---|
| **exit-advisor prompt** (`main.py`) | *"it arms only at +1R … It would arm at X (+1R)"*, and the price was computed as `entry ± 1×risk_px` | renders `TRAIL_ARM_R` in both the sentence and the price. **The advisor is a live consumer of this text — leaving it would have told a model a level the engine no longer uses.** |
| **adoption card** (`virtual_trader.py`) | *"the engine will … MARKET-SELL ~X as the +1R partial. Both are REAL orders on REAL money."* | states the stop move, and names the flag when the partial is off: *"— and NOTHING ELSE: the arm partial is OFF"* |
| **boot geometry line** (`config.py`) | `SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h OBSERVATION_MODE=False` — **byte-identical before and after this change** | adds `ARM=0.75R PARTIAL=OFF`, so a boot can be **checked** rather than assumed |

🔴 **The boot line is why there were two restarts.** Restart #1 (19:52:51) loaded the three changes; its boot line could not distinguish the new geometry from the old, which is exactly the trap the 2026-08-10 registry pass hit when a missing `unregister=` field exposed a wasted restart. Restart #2 (19:54:35) loaded the boot-line change alone, from flat, with nothing open. **It is named rather than buried, and it is the operator's call whether it was worth a second restart of a live process.**

---

## STATE

```
mercury-sol   active · master 2195203 / worker 2195271 · since 2026-08-14 19:54:37 · NRestarts=0
              🔴 TWO restarts this pass: 19:52:51 (the three changes) and 19:54:35 (boot line)
BOOT LINE     geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF
                        ATR_TF=1h OBSERVATION_MODE=False [pid 2195271]
LOADED        TRAIL_ARM_R=0.75 · PARTIAL_AT_ARM_ENABLED=False
              LOSS_STREAK_WINDOW_HOURS=45.1 · LOSS_STREAK_MIN_DAMAGE_R=-2.05
              (threshold 3 and cooldown 4h UNCHANGED — the brake is not removed)
              still loaded from 18:28: ADVISOR_WALL_ALIGNED_RELAXATIONS=False ·
              BOOK_GATE_LEAN_FLOOR {'LONG':0.4238,'SHORT':0.3489} · gate ARMED
UNCHANGED     SL_BUFFER_ATR 2.5 — 1R IS THE SAME UNIT. No §0 boundary. R still pools.
BOOK          29 closed · ΣR −5.985 booked · FLAT · registry empty · max vpos 35
              live baseline for the stopping rule: 7 closed, ΣR −0.780, win 28.6 %
STOPPING RULE 20 further LIVE closed positions (vpos 36 → 55), ~2026-09-03.
              Still negative -> STOP TRADING THIS SIGNAL SET. Not a 27th candidate.
titan         /root/titan-bot — NOT touched. HEAD 897850b · clean · MainPID 2538048
```

**Rollback is one command per file:** `cp <file>.bak_geometry_20260814_1945 <file>` — all four md5-verified against the originals before any edit, and `trades.db.bak_geometry_20260814_1945` predates a pass that made no DB write at all.
