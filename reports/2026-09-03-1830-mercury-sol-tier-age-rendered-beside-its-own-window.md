# mercury-sol-tier-age-rendered-beside-its-own-window

_2026-09-03 18:30 UTC_

---

# TIER AGE MADE COMPARABLE TO ITS OWN WINDOW — one prompt fact, designed, proved, applied from flat

**Titan pre-flight `tools/openitems_guard.py` → exit 0 before, exit 0 after. Titan otherwise untouched.**

**What changed:** the entry advisor's prompt now prints each aged tier's **age beside the window it
is judged against**. Nothing else. No gate, no threshold, no constant, no advice. The system
prompt is byte-identical (sha256 proved on the string actually passed to `_call`), and 21 of 22
functions in the file are AST-identical.

**Applied from flat** (§3c is OPEN — no consultation has fired since the restart; see §3c), on a bot with zero open positions in the DB, zero rows in
`active_positions`, zero pending exits, and **zero size on both Bybit position indices**, verified
before the restart and re-asserted by the bot's own boot line.

---

# 1. THE CHANGE

## 1a/1c. What is rendered, and on which tiers

**Before → after, on vpos 42's own stored inputs:**

```
- 1H: 15m-rearm: Reversal Up (direction: LONG, set 1.7h ago)
+ 1H: 15m-rearm: Reversal Up (direction: LONG, set 1.7h ago — 102 of 360 min, 28% of its window, NOT stale)
- 15m: HyperWave Signal Down (direction: SHORT, set 25m ago)
+ 15m: HyperWave Signal Down (direction: SHORT, set 25m ago — 25 of 90 min, 28% of its window)
  5m trigger: Bearish New Imbalance (direction: SHORT)        <- unchanged
```

**Every tier that carries an age now carries its window beside it — and that is exactly two of the
three.**

| tier | carries an age today? | window rendered | source |
|---|---|---|---|
| **1H** | yes (`set 1.7h ago`) | **360 min** | `CATEGORY_TTL_MINUTES['TREND']` |
| **15m** | yes (`set 25m ago`) | **90 min** | `CATEGORY_TTL_MINUTES['MOMENTUM']` |
| **5m trigger** | 🔴 **no — it renders no age at all** | none | — |

🔴 **The 5m trigger is not skipped by choice; it has no age to make comparable.** The existing
code states why (`claude_advisor.py:556-558`, and again at 601-604): *"The 5m trigger deliberately
carries no age: it IS the signal that just fired, so its age is ~0 by construction"* —
`set_trigger_and_snapshot` writes the slot with `now_iso` and returns the snapshot **under the same
lock**, so the age is bounded by one request, and `5m trigger: n/a` occurs in 0 of 3,199 stored
consults. **Inventing an age line for it in order to be symmetric would have added a fact that is
not measured. It was not added.** The brief's instruction — do it for every tier that carries an
age — is satisfied at 2 of 2.

## 1b. 🔴 The window number comes from the code

```python
# claude_advisor.py, inside consult_for_entry
_TIER_WINDOW_MIN = {
    '1H':  float(CATEGORY_TTL_MINUTES.get('TREND', 360)),
    '15m': float(CATEGORY_TTL_MINUTES.get('MOMENTUM', 90)),
}
```

`CATEGORY_TTL_MINUTES` is imported at `claude_advisor.py:52` from `config.py:677-682`. Runtime
value, loaded and printed, not copied:

```
CATEGORY_TTL_MINUTES = {'TREND': 360, 'MOMENTUM': 90, 'LIQUIDITY': 30, 'EXECUTION': 5}
```

**It is the same dict the STALE marker already keys off** — `_TIER_STALE_TTL_MIN` at
`claude_advisor.py:605` reads `CATEGORY_TTL_MINUTES.get('TREND', 360)` — so the rendered number
cannot drift away from the number that decides. A future edit to the TTL moves both together or
neither.

🔴 **The 1H window DOES differ between the state machine and the matrix, and the report states
which is rendered.** The state-machine slot `1h_context` carries `ttl_hours: None`
(`state_machine.py:40` — *"Persistent — no expiry; changes only on new 1H signal"*), so by the
state machine the tier never expires at all. The matrix drops it at 360 min. **The MATRIX window
is the one rendered**, because it is the one the STALE marker keys off, so the two lines cannot
disagree with each other.

**The same divergence exists on 15m and is resolved the same way**: slot `15m_confirm` carries
`ttl_hours: 4` (240 min, `state_machine.py:47`) while the matrix MOMENTUM window is 90 min. The
matrix window is rendered, for the same reason.

## 1d. What was deliberately NOT added

**No threshold. No advice. No lean. No "therefore it counts."** The clause is a ratio and a
percentage of two numbers already in the system. The rule was already stated by the sentence the
prompt has carried since 2026-08-05 and which is untouched:

> `Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 2 agree, 1 oppose, 0 neutral, 0 absent.`

**`NOT stale` is the one word that could be mistaken for a verdict, so its scope is fenced in
code:** it renders only on a tier that actually carries the STALE marker (1H), and only in the
branch where that marker was withheld. It is that marker's complement — the same fact, stated in
the branch where today the prompt says nothing at all. It is **not** rendered on 15m, which has no
marker; asserting "NOT stale" there would claim a verdict that does not exist for that tier.

**One judgment call, named rather than buried.** Rendering `25 of 90 min` on the 15m tier does
surface that a 15m tier can be past *its* window — something today's prompt hides. That is the
legibility this pass is for, and it adds no marker and no instruction: the 15m STALE marker stays
absent, exactly as `claude_advisor.py:597-600` requires (*"Enabling it is one entry ('15m': 90.0),
and that is a decision, not a cleanup"*). **That entry was not made.** `_TIER_STALE_TTL_MIN` still
contains `'1H'` and nothing else.

## 1e/1f. The STALE branch is byte-identical

On a stored consultation where the 1H tier genuinely IS past its window — **row 23419**, 1H set
11.9 h ago:

```
- 1H: Bullish Confirmation (direction: LONG, set 11.9h ago, STALE — past the 6h window the gate itself uses for this tier)
+ 1H: Bullish Confirmation (direction: LONG, set 11.9h ago — 714 of 360 min, 198% of its window, STALE — past the 6h window the gate itself uses for this tier)
```

**The marker string `, STALE — past the 6h window the gate itself uses for this tier` is
unchanged, character for character.** `_stale_note()` was not edited; the age clause is inserted
in front of its return value. Verified programmatically: the exact substring is present in the
after-prompt.

**508 stored prompts carry that marker.** All of them keep it.

---

# 2. WHAT DID NOT CHANGE

## 2a. The system prompt — sha256, on the string actually passed to `_call`

```
BEFORE  cc70ed4582988b09e44ffcdf5453cfe12486d5a4890eb699fd8dcd02903bb620
AFTER   cc70ed4582988b09e44ffcdf5453cfe12486d5a4890eb699fd8dcd02903bb620
IDENTICAL: True     (captured on BOTH test cases, from the stubbed _call)
```

And every system-prompt literal in the module, hashed by AST before and after:

```
_ENTRY_SYSTEM  _ENTRY_SYSTEM_V2  _ENTRY_SYSTEM_V2_ALIGNED  _ENTRY_SYSTEM_V2_ALIGNED_SHORT
_WALL_RULE_V1  _WALL_RULE_V2     _WALL_RULE_V2_ALIGNED     _WALL_RULE_V2_ALIGNED_SHORT
ALL IDENTICAL: True
```

## 2b. AST verification — every function changed, named

```
CHANGED: consult_for_entry          (the tier block, inside it)
CHANGED: _age_window_clause  (NEW)  (nested helper, pure string formatting)
unchanged functions: 21 of 22
```

**No gate, no threshold, no constant was touched.** `config.py` is byte-identical:
`sha256 952bc29a0fefddf78890ddfc0aca9f4a3977f9d2f36097beab823cd5352b1da9` before and after.
`_stale_note`, `_slot_age`, `_slot_age_minutes`, `_call`, `_wall_pctl`,
`_format_pre_trade_walls`, `consult_for_close`, `consult_for_close_state`,
`consult_for_learning` — all AST-identical.

Source diff: **54 changed lines**, of which 43 are the comment block explaining why. File 1,346 →
1,399 lines.

## 2c. Runtime constants — loaded, not hand-copied

```
SL_BUFFER_ATR              = 2.5          TRAIL_MULT_ATR         = 1.875
TRAIL_ARM_R                = 0.75         CONFLUENCE_SCORE_THRESHOLD = 2.0
FLAT_ADX_GATE_ENABLED      = True         FLAT_ADX_GATE_DRYRUN   = False      🔴 still ARMED
BOOK_GATE_DRYRUN           = False        BOOK_GATE_WALL_PCTL    = 90.0       🔴 still ARMED
EXIT_ADVISOR_DRYRUN        = True         PARTIAL_AT_ARM_ENABLED = False
MAX_POSITIONS_PER_SIDE     = 1            LIVE_FIXED_MARGIN      = 20
LEVERAGE                   = 5            AI_ADVISOR_HIDE_1H     = False
MERCURY_OBSERVATION_MODE   = 0  (env, .env — config exposes it as OBSERVATION_MODE, config.py:12)
```

All at their pre-change values, and the bot's own boot line agrees (§3b).

## 2d. The full prompt diff, real code, `_call` stubbed, zero API calls

Both modules loaded from source in one process — the `.bak` as `adv_old`, the live file as
`adv_new` — `_call` replaced with a capturing stub, `state_verdict_cache_clear()` between runs,
identical inputs reconstructed from the two stored rows. **No network call of any kind was made by
the harness.**

```
FRESH case (row 23053, vpos 42's own entry):  diff lines changed = 4  (2 removed, 2 added)
STALE case (row 23419, 1H 11.9h old)      :  diff lines changed = 4  (2 removed, 2 added)
```

The complete diffs are the two blocks quoted in §1a and §1e. **In both cases the only delta in the
entire user prompt is the age clause on the 1H and 15m lines.** The proposed-entry line, the
volatility block, the higher-timeframe block, the order-book block, the wall calibration
paragraph, the tier-agreement tally and the closing instruction are unchanged.

## 2e. `.bak` first, contract suite

```
/mnt/volume_nyc1_1780480650620/mercury-sol/claude_advisor.py.bak_tierage_window_20260903_1815
```
written before the first edit. The Mercury-SOL tree is **not** under git — the `.bak` is the
rollback, and restoring it plus a restart returns the byte-exact previous behaviour.

Contract suite: **209/209 green in 51 s**, run as `botuser` (running it as root gives two false
failures — `feedback_contracts_run_as_botuser_not_root`).

🔴 **Stated plainly so it is not oversold: none of the 209 contracts reference `mercury` or
`claude_advisor`.** That suite is the OpenClaw/Kolya workspace's, and Mercury-SOL has no test
directory of its own. Green there is a **regression check on the rest of the box, not a proof of
this change.** The proof of this change is §2a–§2d.

---

# 3. APPLY — FROM FLAT ONLY

## 3a. 🔴 FLAT CONFIRMED — five checks, all zero

```
open virtual_positions          : 0      (last closed: vpos 42, 2026-09-03T13:42:12, 'sl')
active_positions rows           : 0
exit_pending rows               : 0
unresolved naked_position_alerts: 0

BYBIT /v5/position/list (GET, read-only), category=linear SOLUSDT:
   positionIdx=1  side=''  size=0
   positionIdx=2  side=''  size=0        🔴 BOTH indices, non-zero positions: 0
BYBIT /v5/order/realtime (GET): open + conditional orders: 0
```

Nothing was open. The restart proceeded.

## 3b. Restart, and the loaded bytecode

```
before  MainPID=1196924  NRestarts=0  active since 2026-08-24 13:29:27
after   MainPID=3422117  NRestarts=0  active since 2026-09-03 17:45:58   ActiveState=active
```

**Proof from the compiled bytecode actually on disk for the running interpreter:**

```
source  mtime=1788457255  size=77906
pyc     mtime=1788457255  size=77906     🔴 BYTECODE MATCHES CURRENT SOURCE: True
b'% of its window' present in bytecode : True
b'NOT stale'       present in bytecode : True
old STALE marker   present in bytecode : True
```

**Boot lines, verbatim:**

```
Started mercury-sol.service - Mercury-SOL SOL/USDT swing bot (Bybit, paper/observation).
[MERCURY-SOL] [AP] No active positions in DB — clean boot.
[MERCURY-SOL] [BOOT] taker fee: 0.001 (0.1000%) source=venue | geometry constant BYBIT_TAKER_FEE_RATE=0.00055 is unchanged and separate
[MERCURY-SOL] [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 3422246]
```

The bot's own boot assert independently re-confirms the venue was flat, and its geometry line
independently re-confirms every exit constant is where it was.

**`openitems_guard.py` after the restart: exit 0.**

## 3c. A live prompt after the restart

🔴 **NOT YET AVAILABLE AT PUBLICATION, AND NOT FABRICATED.**

In the 40 minutes between the restart (17:45:58) and this report, **one** webhook arrived — a 1h
`Exit Signal` at 18:00:07, logged as `60m_exit / trend_reset`. That path does not consult the
advisor. It also **reset the 1h trend**, so the next entry consultation cannot happen until a new
1h trend arrives or a 15m re-arm fires. The bot is alive and idle: `[HEARTBEAT] alive … open=0
mode=LIVE pid=3422246`.

```
rows written since the restart : 1   -> (23638, '2026-09-03 18:00:07', '60m_exit', 'trend_reset')
rows carrying a rendered prompt: 0
```

**A consultation is an external event.** Forcing one would mean writing to the money path, which
this pass will not do. **The quote will therefore be missing from this report and I am saying so
rather than showing a prompt rendered by anything other than the running process.**

**What IS proved about the running process, in place of the quote:**

1. The bytecode the interpreter loaded matches the current source exactly — embedded
   `mtime=1788457255 size=77906` equals the source's — and contains `b'% of its window'` and
   `b'NOT stale'`.
2. The §2d harness rendered its prompts through **the live file itself**
   (`/mnt/volume_nyc1_1780480650620/mercury-sol/claude_advisor.py`, loaded as `adv_new`) — the same
   bytes the service imported at 17:45:58 — not through a copy or a reconstruction.

So the code path that will render the next live prompt is the one already diffed in §1a and §1e.

**One query settles it when the next consultation fires**, and it needs no further work:

```sql
SELECT id, timestamp, substr(ai_user_prompt, instr(ai_user_prompt,'1H:'), 160)
FROM trades WHERE ai_user_prompt LIKE '%of its window%' ORDER BY id LIMIT 1;
```

The first row it returns is the live confirmation. **Until that row exists this item is OPEN, and
it is recorded as open.**

---

# 4. WHAT THIS CANNOT FIX — measured read-only, same report

## 4a. 🔴 How often has the advisor asserted staleness about a tier that was not past its window?

Every stored `ai_reason` containing "stale", cross-checked against the 1H age printed in **that
same consultation's own prompt**:

```
reasons containing "stale"                          : 346 of 4,279 stored reasons (8.1 %)
  the prompt CARRIED the STALE marker (supported)   : 342   (98.8 %)
  🔴 the prompt did NOT carry it (claim invented)   :   4   (1.2 % of "stale" reasons,
                                                            0.093 % of all stored reasons)
  age unparseable                                   :   0
```

**All four, in full:**

| row | when | side | 1H age | % of window | verdict | outcome | reason (the staleness clause) |
|---|---|---|---|---|---|---|---|
| 16857 | 08-08 21:10 | LONG | 324 m | **90 %** | execute | **vpos 30, +0.762 R** | *"1H rearm SHORT is stale (5.4h)"* |
| 19078 | 08-16 20:40 | LONG | 102 m | 28 % | skip | no position | *"1H signal stale (1.7h)"* |
| 21488 | 08-27 05:55 | SHORT | 132 m | 37 % | skip | no position | *"1H signal stale (2.2h)"* |
| **23053** | **09-01 21:40** | **SHORT** | **102 m** | **28 %** | **execute** | 🔴 **vpos 42, −1.083 R** | *"1h rearm stale."* |

🔴 **The pattern across all four is the same, and it is precisely the thing this change addresses:
in every case the model stated the AGE CORRECTLY — "5.4h", "1.7h", "2.2h" — and then mislabelled
it.** It never got the number wrong. It got the *comparison* wrong, because the age was on the
line and the window was not. Row 16857 is the mildest: at 90 % of the window it was nearly right.
Rows 19078, 21488 and 23053 are at 28 %, 37 % and 28 % — not close to anything.

**Direction of the error:** 2 of the 4 inventions supported a **skip** (19078, 21488, where the
reason carried other sufficient grounds anyway) and 2 supported an **execute** (16857, 23053).
Of the two executes, one won +0.762 R and one lost −1.083 R.

## 4b. How often has it reversed itself on the same setup?

**Definition, fixed before counting:** two stored consultations with (i) the same `signal_type`
(same proposed direction), (ii) an identical **1H tier signal name**, (iii) an identical **15m tier
signal name**, (iv) **≤ 60 minutes apart**, and (v) **different `ai_decision`** (execute vs skip).

```
consultations with a parseable prompt and a verdict : 4,130
qualifying reversal PAIRS                           :    10
distinct reversing consultations                    :     8   (0.19 %)
```

The eight: rows **15093, 16445, 16447, 16455, 16495, 16497, 16857, 23053**. Two of them
(16445/16447 and 16495/16497) are the same underlying setup flipping twice within an hour on
2026-08-06 and 2026-08-07.

🔴 **The intersection of §4a and §4b is exactly two events — and both are reversals from SKIP to
EXECUTE in which the reversing verdict invoked staleness it could not support:**

```
16852 (skip, "1H signal opposes")  -> 16857 (execute, "1H rearm SHORT is stale (5.4h)")  60 min  -> vpos 30, +0.762 R
23052 (skip, "1H tier opposes SHORT (Reversal Up/LONG set 75m ago)")
                                   -> 23053 (execute, "1h rearm stale.")                 25 min  -> vpos 42, −1.083 R
```

Both times the model refused the trade, then took it 25–60 minutes later on the strength of a
staleness claim its own prompt did not support. **One won, one lost. n = 2 and it cannot be
ranked** — it is a count, and the count is two.

## 4c. 🔴 Is this a single incident?

**No — and the brief asked for the honest answer, so: it is four, not one.** But it is four in
4,279 stored reasons, which is **0.093 %**, and the four are spread over 24 days. It is not
twenty, and it is not a pattern that would justify anything larger than what was done. **It is a
rare failure with an expensive worst case: the one that dismissed the *sole* opposing fact and
produced a live position lost 1.083 R, and 98.8 % of the time the model's staleness claims are
correct.** The change is cheap insurance against a rare, expensive error — that is the accurate
description and no larger one is offered.

## 4d. 🔴 What this change CANNOT do

**It cannot stop a model inventing a claim.** Nothing in a prompt can. A model that will write
"stale" about a 102-minute tier against a 360-minute window can equally write it when the window
is printed two words away.

What it changes is narrower and it is the only thing being claimed: **the invention is now
checkable against the same line it appears on.** Before, the prompt gave an age and no window, so
"stale" was unfalsifiable from the prompt alone — a reader had to know `CATEGORY_TTL_MINUTES` to
catch it, and the model had to supply the window from somewhere. Now both terms are on the line,
and any future audit of a "stale" claim is a comparison, not an investigation.

**Three further things it explicitly does not do:**
- It does not change any gate. The cascade, the score gate, the flat/ADX gate and the book gate
  saw exactly what they saw before and decide exactly as they did before.
- It does not stop self-reversal (§4b). Six of the eight reversals invoked no staleness at all;
  they flipped on regime, walls and ADX. This touches none of that.
- It does not make the model weigh the tier correctly. *"Stale tiers vote in full"* was already in
  the prompt on 2026-09-01 and was ignored. **A fact that is already present and disregarded is
  not fixed by a second fact.** The measurable claim here is legibility for the audit, not
  obedience from the model — and the next occurrence, if there is one, will show which.

**No further change is proposed.**

---

# CONTROLS

| control | evidence |
|---|---|
| Titan guard | `openitems_guard.py` exit **0** before, exit **0** after; Titan otherwise not touched |
| flat before apply | 5 checks, all zero, incl. **both** Bybit position indices and 0 open/conditional orders |
| `.bak` first | `claude_advisor.py.bak_tierage_window_20260903_1815` (74,740 B) written before the first edit |
| system prompt | sha256 **identical**, captured from the stubbed `_call` on both test cases |
| `config.py` | sha256 **952bc29a…** identical before and after — not edited |
| AST | 21 of 22 functions identical; `consult_for_entry` + new nested `_age_window_clause` only |
| runtime constants | 14 named constants loaded and printed, all unchanged; the bot's boot line agrees |
| zero API calls | `_call` stubbed in the harness; no Anthropic request issued |
| venue calls | **GET only** (`/v5/position/list`, `/v5/order/realtime`) — no order placed, amended or cancelled |
| contracts | 209/209 green as `botuser` — **and none of them cover this file**, stated as such |
| service | restarted once, deliberately, from flat. `NRestarts=0`; PID 1196924 → 3422117 |
| Titan service | PID 2610002 unchanged, `NRestarts=0` |
| n honesty | §4a n=4, §4b n=8 events / n=2 in the intersection — **counts, not rankings** |

**Nothing else was proposed and nothing else was applied.**

---

**Bottom line.** The entry advisor's prompt now prints, on every tier that carries an age, that
age beside the window it is judged against — `set 1.7h ago — 102 of 360 min, 28% of its window,
NOT stale` — with the window read from the same `CATEGORY_TTL_MINUTES` the gate uses, so the two
cannot drift apart. The 5m trigger is untouched because it renders no age to compare. The STALE
branch is byte-identical and all 508 prompts that carry the marker keep it. The system prompt is
byte-identical by sha256; `config.py` is byte-identical; 21 of 22 functions are AST-identical; the
only delta in either test prompt is two lines. Applied from a confirmed-flat book — zero
positions on both venue indices — with the restart's loaded bytecode verified against the source.
And the thing it is insurance against is **four events in 4,279 stored reasons, not one**: in all
four the model quoted the age correctly and mislabelled it, twice reversing its own skip into an
execute on that basis. **It cannot stop a model inventing a claim; it can only put both terms of
the claim on the same line so the invention is checkable. That is the whole of what is claimed.**
