# sol-why-the-exit-advisor-never-ran

_2026-08-09 18:30 UTC_

---

# Why Mercury-SOL's exit advisor has never run: **it is neither a missing alert nor a routing defect. Titan's 5m Group-B door has never opened either.** Titan has four OTHER doors. SOL has none of them.

**READ-ONLY on both bots. Nothing changed, nothing restarted, no writes and no git operations on
Titan.**

🔴 **THE ANSWER, AND IT INVALIDATES MY OWN 18:15 FRAMING.** I wrote that SOL's advisor never runs
because it needs a 5m Group-B webhook that TradingView never sends. The first half is true. The
second half implied Titan gets one. **It does not.**

```
signals matching _GROUP_B_RE on tf='5m', in each bot's ENTIRE history:
   SOL   : 0
   TITAN : 0
```

**Titan's exit advisor has fired 119 times without that door ever opening once.**

🔴 **104 of the 119 came from `tv_action = "hourly review"` — an internal timer, not a webhook.**
Titan runs `consult_exit_advisor` from **five** call sites; the dominant one is an hourly loop inside
its poller (`virtual_trader.py:2567`, `EXIT_ADVISOR_HOURLY = True`, added 2026-07-26). **SOL has
exactly one call site, and it is the one door that has never opened on either bot.**

```
grep -rn "EXIT_ADVISOR_HOURLY|consult_exit_advisor|exit_advisor_last_ts" on SOL  ->  (empty)
```

**The Group-B regex is BYTE-IDENTICAL on both bots. The routing condition is byte-identical. The
difference is not classification and not TradingView — it is four missing call sites.**

**And the hook Titan uses already exists on SOL and already fires**: SOL's hourly smart-exit sampler
has written **292 samples across 16 positions**, including **22 on vpos 30**, the most recent at
18:12 today.

Prior: [18:15 — the exit map that named this question](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1815-which-exit-mechanism-works-the-map.md)

---

## 1. WHAT EXACTLY WAKES IT — the path, quoted

SOL's advisor sits behind exactly one gate. The routing condition, verbatim from `main.py:5361`:

```python
    # ── Group B ──────────────────────────────────────────────────────────────
    if group == 'B':
        had_trend = state_machine.reset_1h_trend(signal_name)
        if tf == '5m':
            return _handle_5m_close(symbol, signal_name, tf)
```

`group` comes from `state_machine.classify_group(signal_name)` (`main.py:5253`), which is:

```python
_GROUP_B_RE = re.compile(
    r'(\bexit\b|\btake[\s-]?profit\b|\bstop[\s-]?loss\b|\btp\b|\bsl\b)',
    re.I,
)
```

**So the requirement is precisely:**

| | required |
|---|---|
| **tf** | `5m` — from the `?tf=` query arg or the JSON `tf` field |
| **task** | any task that maps to the 5m slot; the **plain-text path** (`?tf=5m` + bare body) also reaches it |
| **signal text** | must contain one of `exit`, `take profit`, `take-profit`, `stop loss`, `stop-loss`, `tp`, `sl` as a **whole word** |
| **and then** | `_handle_5m_close` requires a **live position on the venue**, else it bails at `no_position` |

**The exact alert that would satisfy it:** a 5m alert whose body is, or contains, the word
"Exit" — e.g. `{"action": "Exit Signal", "task": "price_action", "tf": "5m"}`.

**SOL has received zero such alerts.** And so has Titan.

---

## 2. WHAT TITAN RECEIVES THAT SOL DOES NOT — nothing, on this path

Side by side, from each bot's own `trades` table:

```
                                   SOL                         TITAN
distinct (tv_action, tv_tf) pairs   79                          80
total signal rows                   17,022                      21,902
tv_tf distribution                  5m 14,887                   5m 20,637
                                    15m 1,796                    15m   750
                                    1h    339                    60m   324 · None 191
rows matching _GROUP_B_RE           54  ("Exit Signal", tf=1h)   70  ("Exit Signal", tf=None)
  ...of those, on tf='5m'           0                           0
```

**Both bots receive an "Exit Signal", both on an hourly timeframe, neither on 5m.** The webhook
feeds are near-identical in shape. TradingView is not the difference.

### 🔴 Then where did Titan's 119 consults come from?

```
tv_action           signal_type       n
hourly review       exit_ai_dryrun   104     <- an internal timer, not a webhook
Bullish I-BOS       exit_ai_dryrun     6
Bearish I-CHOCH     exit_ai_dryrun     3
Bearish I-BOS       exit_ai_dryrun     2
Bullish I-CHOCH     exit_ai_dryrun     2
Bearish S-CHOCH     exit_ai_dryrun     1
Bullish I-CHOCH+    exit_ai_dryrun     1
```

`"hourly review"` parses as `direction=NEUTRAL, group=None` — it would be classified as *nothing* by
the router. It never goes near the router. It comes from `virtual_trader.py:2567`:

```python
    if EXIT_ADVISOR_HOURLY:
        try:
            _st = mgmt_state.get('exit_advisor_last_ts')
            _now_ts = datetime.now(timezone.utc).timestamp()
            if _st is None or (_now_ts - float(_st)) >= EXIT_ADVISOR_HOURLY_SEC:
                import main as _m
                _adv = _m.consult_exit_advisor(row, row['symbol'], position_side,
                                               'hourly review', 'hourly')
```

with the comment that states the design intent outright:

> *"Signal triggers alone give ~2.2 consultations a day; hourly gives a full trajectory per
> position."*

**Titan's own author already knew the signal door was thin, and built a timer to replace it.**

### The five doors vs the one

```
TITAN — consult_exit_advisor call sites
  virtual_trader.py:2567   HOURLY loop per open position        -> 104 consults
  main.py:3995             15m-confirm path                     -> part of the 15
  main.py:3551             armed_exit path                      -> part of the 15
  main.py:3314             5m Group-B (_handle_5m_close_via_ai) -> 0, the door never opened
  config EXIT_ADVISOR_ON_15M_CONFIRM / EXIT_ADVISOR_HOURLY = True, DRYRUN = False (ACTING)

SOL — consult_for_close call sites
  main.py:4926             5m Group-B (_handle_5m_close)        -> 0, the door never opened
```

**The difference is in the CODE, and specifically in the porting: SOL received the door that has
never opened on either bot, and none of the four that work.**

---

## 3. MISSING ALERT, OR ROUTING DEFECT? 🔴 **NEITHER.**

### (a) Not an alert-configuration gap

An alert-configuration answer would require Titan to be receiving something SOL is not. **It is
not.** Both receive the same `Exit Signal` on an hourly timeframe and neither has ever received a
Group-B 5m alert. **Creating a new 5m "Exit" alert on TradingView would open a door that Titan has
never used** — it would be building SOL a fifth mechanism from scratch rather than porting the one
that demonstrably works. **So no TradingView change is specified here, because none is indicated.**

### (b) Not a routing defect

Everything on the path is identical between the two bots:

```
_GROUP_B_RE                     BYTE-IDENTICAL (state_machine.py:68-71 on both)
classify_group()                identical logic, Group B checked before A
the routing condition           if group == 'B': if tf == '5m': -> close handler
```

**Nothing is discarded and nothing is mis-routed.** There is no line to name, because there is no
defect on this path. The defect is an **absence**: four call sites that exist on Titan and were
never written on SOL.

### (c) 🔴 DID SOL RECEIVE IT UNDER A DIFFERENT NAME OR TASK? **YES — and it is NOT falling through.**

This is the shape the project keeps finding, so I checked it directly. SOL **does** receive an exit
alert, 54 times:

```
WEBHOOK_IN tf='60m' body='{"action": "Exit Signal", "task": "exit", "tf": "60m"}'
```

`task == 'exit'` is intercepted **before** the group router, at `main.py:5882`:

```python
    if task_field == 'exit':
        return _handle_exit_signal(data)
```

It goes to the **arming** mechanism, not the advisor — and that mechanism works:

```
Exit Signal rows      : 54     -> trend_reset 38 · exit_armed 16
15m_exit_confirm      : 309
15m_armed_exit        : 9  (executed)   <- one of these closed vpos 29 on 2026-08-08
```

**So the alert is not silently swallowed. It drives SOL's exit-signal mechanism, which is a
different and functioning mechanism.** The renamed-alert-falling-through failure mode was the right
thing to look for and it is **not** what happened here.

---

## 4. SHOULD SOL HAVE THIS MECHANISM AT ALL?

### (a) The two bots run genuinely different exit stacks

```
                 TRAIL          EXIT SIGNAL      EXIT ADVISOR     STOP
SOL   (live)     ✅ armed,      ✅ closed        ❌ never ran     ✅ backstop
                 never fired    vpos 29
SOL   (paper)    4 closes       7 closes         —                11 closes
TITAN (live)     ❌ 0 closes    —                ✅ 7 closes      1 close
TITAN (paper)    15 closes      —                ❌ 0 consults    27 closes
```

🔴 **SOL is the ONLY place in this project where the trail runs on live money.** Titan's trail has
never fired live — not once. That makes SOL's exit stack not merely "different" but **the sole
remaining measurement of the trail as a live mechanism.**

### (b) The case FOR porting it

- **SOL's largest measured loss source is the stop.** 11 of 22 paper closes, mean **−0.940R**, and
  the shadow beat the stop on **10 of those 11**. SOL has no mechanism that cuts a loser early —
  the trail only arms at +1R, so by construction it can never help a position that never gets there.
- **The advisor is the only mechanism in this project whose reasoning survives inspection**:
  ρ=+0.523 on giveback, ρ=−0.448 on unrealised R, both p<0.0001; 98.6% of its checkable claims true
  against the entry advisor's 0%.
- **The hook point already exists and already fires on SOL.** `SMART_EXIT_DRYRUN_ENABLED = True`,
  `SMART_EXIT_DRYRUN_SAMPLE_SEC = 3600` — the identical cadence Titan's loop piggybacks on, with
  **292 samples across 16 positions**, 22 of them on vpos 30, latest 18:12 today. This is a small
  port onto a live hook, not new machinery.

### (c) The case AGAINST

- 🔴 **The evidence for the advisor is n=7.** Its edge over the shadow is +0.4178R across seven live
  closes and its **realised** mean R is **−0.143**. Adopting a mechanism on n=7 because its
  reasoning looks sound is *precisely* the pattern that produced twenty-two dead entry filters:
  plausibility mistaken for evidence.
- 🔴 **It would contaminate the only live trail measurement that exists.** An *acting* advisor on
  SOL closes positions the trail would otherwise have taken. SOL's live trail cohort — currently
  n=1 — would stop accumulating at the moment it started.
- **SOL has not measured its own current stack.** One live close. Changing the exit stack before
  the first stack has produced any live evidence means never learning what either does.
- The +3.3729R figure that motivated interest in this mechanism **does not reproduce** (18:15 §0).

### 🔴 MY RECOMMENDATION: PORT IT, BUT IN DRYRUN — OBSERVE-ONLY, ACTING DISABLED.

**This is not a compromise; it is what Titan itself did.** `EXIT_ADVISOR_DRYRUN` was **True** from
2026-07-26 to 2026-07-30 — Titan collected verdicts for four days before a single one was allowed to
close anything, and `EXIT_ADVISOR_DRYRUN = False` only came later, after the config comment records
that 8 of 9 clean `close` verdicts on vpos 86 had already been observed.

**What it costs in measurement terms:**

| choice | trail measurement | advisor measurement | R at risk |
|---|---|---|---|
| do nothing | preserved | never starts | SOL keeps riding to the stop |
| port ACTING | 🔴 **destroyed** — advisor pre-empts the trail | starts, but confounded from day one | real |
| **port DRYRUN** | ✅ **fully preserved** | ✅ starts immediately, uncontaminated | **zero** |

**DRYRUN is the only option that buys the measurement without spending anything**, and it directly
answers the closing recommendation of the 18:15 report — *"run the trail and the advisor in the same
era so n accumulates on a comparison"* — because in dryrun **both** run in the same era on the same
positions: the trail acts, the advisor records what it would have done, and every closed position
yields a paired observation instead of one arm of a split.

**How long each takes to answer, at the measured rates:**

```
CLOSE-level evidence (which mechanism earns more)
  0.50R separation needs 51 per arm (18:15 §4, from Titan's SD 0.900)
  Titan  0.79 closes/day -> ~65 days per arm
  SOL    22 paper closes over ~60 days = 0.36/day; 1 live close in 2 days
         -> ~140 days per arm.  🔴 Not reachable this quarter either way.

VERDICT-level evidence (does SOL's advisor read its prompt, like Titan's does)
  hourly cadence, per open position
  Titan reached n=119 consults in 12 days
  SOL's sampler already fires hourly: vpos 30 produced 22 ticks in 21 hours
         -> n~120 verdicts in ~2 weeks of normal position time
```

🔴 **That asymmetry is the whole argument.** Close-level evidence is months away on either bot and
DRYRUN does not delay it by a single day. Verdict-level evidence — the §3-style check of whether
SOL's advisor is coupled to state and whether its claims hold — is **two weeks away and available
for free**. It is also the check that would catch the failure mode that matters most: SOL's exit
prompt has **never been rendered once**, so nobody knows whether it carries the same class of
falsehood the entry prompt does. **A dryrun port is the only way to find that out before a verdict
is ever allowed to spend money.**

**What I am NOT recommending:** creating a TradingView 5m exit alert (§3a — it would build a fifth
mechanism Titan has never used), enabling acting mode, or touching SOL's trail, stop or geometry.

**And the honest caveat on my own recommendation:** a dryrun port is still a code change to a live
bot holding an open position, it adds an hourly LLM call per open position with its cost and its
failure modes, and everything above rests on Titan's n=7. **If the answer is "not now, the book is
too young", that is a defensible reading of the same numbers** — the case for dryrun is that it is
cheap and reversible, not that the advisor is proven.

---

## STATE — nothing was touched

```
Every query on both books used mode=ro. No writes, no restart, no git operation on Titan.
mercury-sol   active · worker 4037550 · vpos 30 OPEN, untouched · sampler still writing (18:12)
titan         active · pid 2538048 · NRestarts=0 · HEAD 897850b · NOT TOUCHED
```

**Corrected in this pass:** my 18:15 report said SOL's advisor never runs because TradingView never
sends the alert. **That was wrong about the cause.** TradingView sends Titan no such alert either;
the cause is four missing call sites, chief among them an hourly timer.
