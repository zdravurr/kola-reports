# sol-prompt-truthfulness-landed-item3-held

_2026-08-01 16:52 UTC_

---

# MERCURY-SOL — PART 1 STATE CHECK: THE PROMPT FIX **DID** LAND (3 of 4), ITEM 3 HELD

**Read-only establishment pass. No SOL trading code was changed in this session.** One
documentation-only correction was made (a stale `OPEN-ITEMS-SOL.md` footer, §8). Titan was not
touched and none of its parameters were read.

**PART 2 WAS NOT EXECUTED.** Part 2 was conditional on "Part 1 shows the prompt fix did not
land." It landed. Re-applying it would have double-applied a live change.

---

# THE ANSWER FIRST

The prompt-truthfulness change **was applied at 16:15:42 and went live at the 16:17:51 restart**,
by a session that finished the work but never published a report. State:

| item | requested | status |
|---|---|---|
| **1** — replace the false closing sentence | yes | ✅ **APPLIED, LIVE** |
| **2** — explicit trade-direction field | yes | ✅ **APPLIED, LIVE** |
| **3** — 1H tier identity | *"check for a recorded rationale first; if deliberate, report BEFORE applying and let me decide"* | 🔴 **NOT APPLIED — HELD, AWAITING YOUR DECISION** (correct per your own instruction) |
| **4** — 15m tier age | yes | ✅ **APPLIED, LIVE** |

**This is not a half-applied change.** Item 3 is the one branch you explicitly asked to stop at,
and it was stopped at for the stated reason: `AI_ADVISOR_HIDE_1H` has a recorded rationale in
three independent places. §5 lays out the decision.

**Two things were genuinely left open**, and both are closed or flagged by this report:

- **The work was never reported.** The last dated file was the 16:07 audit. An applied, live
  change sat with no dated record for 45 minutes. This file is that record.
- **The new prompt has never actually rendered in production.** **Zero consultations** have
  occurred since the 16:17:51 restart — the cascade has been blocking every candidate at
  `HTF_NEUTRAL_15M_WOULD_BLOCK`. The newest stored prompt (row 14973, 16:00:01) is still the
  **old** format. §6 shows the new format rendered by the live code, and is explicit that this is
  a render, not a production consultation.

---

# §1 — SERVICE AND PROCESS

```
mercury-sol.service   active (running) since Sat 2026-08-01 16:17:51 UTC
Main PID  1112089   gunicorn: master [mercury-sol]     forked 16:17:51
Worker    1112227   gunicorn: worker [mercury-sol]     forked 16:18:13
Memory 332.0M (min 600.0M, peak 332.2M)     Tasks 8
```

No tracebacks in the journal since the restart. Clean boot:

```
[SMART-CLEANUP] No open positions for SOL/USDT:USDT — proceeding with orphan cleanup
[AP] No active positions in DB — clean boot.
[MONITOR] thread started in pid 1112227
[VIRTUAL] poller started in pid 1112227 (interval=10s)
[VPOS-RECONCILE] no open paper positions at boot — clean.
[SIGNAL-AUDIT] worker started in pid 1112227
```

One recurring **non-fatal** external error, pre-existing and unrelated: `CryptoPanic HTTP 404`
(the news feed, already known-absent on 100% of prompts per the 16:07 audit §5).

Also running, untouched: `optimizer_listener.py` (pid 939, up 19 days).

---

# §2 — WHAT CHANGED SINCE 15:38, AND WHAT DID NOT

`.bak_*` snapshots are made with mtime preserved from the **source**, so a snapshot's mtime is
the *pre-edit* mtime of the file it copied — not when the snapshot was taken. Read them that way.

| file | mtime | vs worker fork (16:18:13) | verdict |
|---|---|---|---|
| `claude_advisor.py` | **2026-08-01 16:15:42** | before fork | 🔴 **CHANGED after the 16:07 audit** |
| `config.py` | 2026-08-01 15:31:35 | before fork | unchanged since the 15:38 pass |
| `main.py` | 2026-08-01 15:31:54 | before fork | unchanged since the 15:38 pass |
| `virtual_trader.py` | 2026-08-01 15:34:21 | before fork | unchanged since the 15:38 pass |
| `OPEN-ITEMS-SOL.md` | 2026-08-01 16:17:41 | — | pre-registration written before restart |

Every source file predates the worker fork, so the worker loaded all of them.

**Snapshots relevant to today** (the only `.bak_*` entries with a 2026-08-01 tag; every other
snapshot in the directory is 2026-06/07 and belongs to earlier passes):

| snapshot | preserved pre-edit mtime | covers |
|---|---|---|
| `claude_advisor.py.bak_prompt_truthful_agreement_20260801` | 2026-07-04 22:11:00 | **the prompt-truthfulness change** |
| `config.py.bak_partialarm_excursiongrid_20260801` | 2026-07-04 22:09:18 | the 15:38 pass |
| `main.py.bak_partialarm_excursiongrid_20260801` | 2026-07-02 21:36:17 | the 15:38 pass |
| `virtual_trader.py.bak_partialarm_excursiongrid_20260801` | 2026-07-02 21:37:21 | the 15:38 pass |
| `trades.db.bak_pre_testcleanup_20260801` | 2026-08-01 15:39:32 | DB, 42.5 MB |

Rollback for the prompt change is a single file copy; nothing else moved.

`python3 -m py_compile` on `claude_advisor.py`, `config.py`, `main.py`, `virtual_trader.py`:
**OK**.

---

# §3 — ARE THE 15:38 CHANGES STILL LIVE IN THE RUNNING PROCESS

**`OBSERVATION_MODE=True` — proven from the live process, not the file.** `start_virtual_poller`
has two mutually exclusive branches: it prints `[VIRTUAL] poller not started (live mode)` and
returns when `OBSERVATION_MODE` is false, and only reaches `start_worker` when true. The journal
for pid 1112227 carries **`[VIRTUAL] poller started in pid 1112227 (interval=10s)`** and **not**
the live-mode line. **SOL is in PAPER in the running worker.** The flag is set in `.env`
(`MERCURY_OBSERVATION_MODE=1`, loaded by `main.py:42` via `load_dotenv(..., override=True)`
before `config` is read), not in the unit file.

**On reading the other constants from memory — stating the limit honestly.** `/proc/<pid>/environ`
is unusable here: gunicorn's proc-title rewrite clobbers that region (367 bytes, all NULs, on
both master and worker), which is also why `optimizer.py:24` records that
`MERCURY_OBSERVATION_MODE` "lives only in `.env`, not the process env". Neither `gdb` nor `py-spy`
is installed, so there is **no ptrace path to read module globals out of memory**, and I am not
going to claim I did. What is proven instead is the **import chain**, which is the same guarantee
by a different route:

| constant | value in loaded source | evidence it is what the worker loaded |
|---|---|---|
| `EXCURSION_SAMPLE_SEC` | **10** | `config.py` mtime 15:31:35 |
| `EXCURSION_DENSE_UNTIL_SEC` | **3600** | `__pycache__/config.cpython-312.pyc` compiled **15:36:24** — newer than the source, so not stale |
| `PARTIAL_AT_ARM_ENABLED` | **True** | worker forked **16:18:13**, after both |
| `PARTIAL_AT_ARM_FRACTION` | **1.0/3.0 ≈ 0.3333** | CPython invalidates a `.pyc` on source mtime+size, so a stale bytecode load is excluded |
| `OBSERVATION_MODE` | **True** | ✅ additionally proven live (above) |

`claude_advisor.cpython-312.pyc` was recompiled at **16:17:48** from the 16:15:42 source — i.e.
the restarting process itself compiled the new advisor, 25 s before the worker forked.

All four constants are genuinely wired, not dead names:
`virtual_trader.py:47` imports the excursion pair and `:780-781` computes
`cadence = EXCURSION_SAMPLE_SEC if elapsed <= EXCURSION_DENSE_UNTIL_SEC else 5 * EXCURSION_SAMPLE_SEC`;
`:42` imports the partial pair, `:1313` gates on `PARTIAL_AT_ARM_ENABLED and not
mgmt_state.get('partial_done')`, `:839` sizes `qty = size * PARTIAL_AT_ARM_FRACTION`.

**Not yet exercised:** no position has opened since the restart, so neither the 10 s excursion
cadence nor the partial-at-arm leg has fired in anger. Both remain unproven **in execution** —
unchanged from the 15:44 report's own caveat.

---

# §4 — DID THE PROMPT CHANGE LAND: THE ACTUAL DIFF

Diff of `claude_advisor.py` against `claude_advisor.py.bak_prompt_truthful_agreement_20260801`.
Four hunks, all inside `consult_for_entry`; nothing outside the prompt string was touched.

### Hunk 1 — import for the age computation

```python
+from datetime import datetime, timezone   # 2026-08-01: 15m tier age in the entry prompt
```

### Hunk 2 — item 4, the 15m age (and the 1H age if ever unhidden)

```python
+    def _slot_age(_slot):
+        ts = _slot.get('timestamp')
+        if not ts:
+            return 'age unknown'
+        try:
+            _t = datetime.fromisoformat(ts)
+            if _t.tzinfo is None:
+                _t = _t.replace(tzinfo=timezone.utc)
+            _mins = (datetime.now(timezone.utc) - _t).total_seconds() / 60.0
+        except (ValueError, TypeError):
+            return 'age unknown'
+        if _mins < 1:
+            return 'set just now'
+        if _mins < 90:
+            return f'set {_mins:.0f}m ago'
+        return f'set {_mins / 60.0:.1f}h ago'
     _lux_lines = ""
     if not AI_ADVISOR_HIDE_1H:
         _lux_lines += (f"1H: {_h1.get('signal_name') or 'n/a'} "
-                       f"(direction: {_h1.get('direction') or 'n/a'})\n")
+                       f"(direction: {_h1.get('direction') or 'n/a'}, "
+                       f"{_slot_age(_h1)})\n")
     _lux_lines += (
         f"15m: {_m15.get('signal_name') or 'n/a'} "
-        f"(direction: {_m15.get('direction') or 'n/a'})\n"
+        f"(direction: {_m15.get('direction') or 'n/a'}, {_slot_age(_m15)})\n"
```

Age is **rendered, never filtered on** — as specified. The 5m trigger deliberately carries no
age: it *is* the signal that just fired, so its age is ~0 by construction. Unparseable or missing
timestamps degrade to `age unknown` rather than throwing.

### Hunk 3 — item 2, the explicit direction field

```python
+        f"PROPOSED ENTRY: {(direction or 'n/a').upper()}\n"
         f"Symbol: {symbol}\n"
```

First line of the prompt. The in-code comment records that this **re-creates** an
`Intended entry:` line that D5c deliberately removed on 2026-06-08 for Titan input-set parity —
so it is now a tracked, operator-ordered, evidence-backed divergence from Titan, flagged so a
future parity sweep does not silently revert it. **Titan itself was not modified.**

### Hunk 4 — item 1, the truthful agreement block

```python
-        "\nThe 3 timeframes are aligned (confluence has already passed). "
+    _dir_up = (direction or 'n/a').upper()
+
+    def _tier_verdict(_slot):
+        _nm = _slot.get('signal_name')
+        _d = _slot.get('direction')
+        if not _nm or not _d:
+            return 'ABSENT'
+        _d = str(_d).upper()
+        if _d == _dir_up:
+            return 'AGREES'
+        if _d in ('LONG', 'SHORT'):
+            return 'OPPOSES'
+        return 'NEUTRAL'
+
+    _shown = ([('1H', _h1)] if not AI_ADVISOR_HIDE_1H else []) + \
+             [('15m', _m15), ('5m trigger', _m5)]
+    _tally = {'AGREES': 0, 'OPPOSES': 0, 'NEUTRAL': 0, 'ABSENT': 0}
+    _agree_lines = []
+    for _lbl, _slot in _shown:
+        _v = _tier_verdict(_slot)
+        _tally[_v] += 1
+        _agree_lines.append(
+            f"  {_lbl}: {_slot.get('signal_name') or 'ABSENT'} "
+            f"-> {(_slot.get('direction') or 'none')} = {_v}")
+    _hidden_1h = ("  1H LuxAlgo tier: NOT SHOWN in this prompt — do NOT assume it "
+                  "agrees or opposes\n" if AI_ADVISOR_HIDE_1H else "")
     user += (
+        f"\nTier agreement vs {_dir_up} (computed for this consultation):\n"
+        + _hidden_1h
+        + "\n".join(_agree_lines) + "\n"
+        + f"  Of the {len(_shown)} tier(s) shown: {_tally['AGREES']} agree, "
+          f"{_tally['OPPOSES']} oppose, {_tally['NEUTRAL']} neutral, "
+          f"{_tally['ABSENT']} absent.\n"
+        "The cascade gate, the score gate and the risk gate have already passed. "
+        "That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement "
+        "that the tiers listed above agree with each other.\n"
         "Decide whether the bot should execute this entry now."
     )
```

Checked against each of your four constraints:

- **Absent renders `ABSENT`.** `_tier_verdict` returns `ABSENT` when either `signal_name` or
  `direction` is falsy — it cannot be read as agreement. This matters for the 5.0 % of prompts
  with a missing 15m name and the 5.1 % with a missing 15m direction (16:07 audit §2), including
  **3 of the 18 real entries**.
- **The tally names its own scope** — "Of the 2 tier(s) shown" — so it cannot be read as a claim
  about three timeframes.
- **`confluence has already passed` is kept and separated.** It survives as a statement about the
  cascade/score/risk gates, with an explicit sentence that this is *not* an alignment claim.
- **No statistics, no win rates, no historical performance** are attached to any signal name
  anywhere in the diff. Identity and direction only.

**Scope discipline held.** Nothing in §5.2 (news/funding/tape/OI/macro), the news observation
gate, the system-prompt storage defect (16:07 audit §4, still 31 rows), or the 5m tier's class
labelling was touched. This change is attributable on its own.

---

# §5 — 🔴 ITEM 3: THE DECISION I AM HOLDING FOR YOU

You asked me to check for a recorded rationale first and to report rather than apply if the flag
was deliberate. **It was deliberate**, in three independent places:

- **`config.py:444-449`** — *"Divergence C (Titan parity): suppress the 1H LuxAlgo signal-name
  line from the advisor prompt. Matches titan-bot config (default True) — **the 1H is the hard
  cascade gate's domain**, so the AI advisor sees only the 15m + 5m LuxAlgo signal names. Flip
  False to also show the 1H signal-name line. Prompt-text only; never touches the gate, the
  matrix, or the snapshot."*
- **`project_mercury_sol_deploy` (2026-06-07)** — the flag was *created* for this purpose: *"1H
  suppressed via new `config.AI_ADVISOR_HIDE_1H=True`, matching Titan HEAD."*
- **`project_mercury_sol_parity_inventory` D5b (2026-06-08)** — SOL's 1H macro-trend line was
  *removed* to match Titan.

**And Titan reached the same question independently and deferred it** — its 2026-07-26 report §7
notes the entry advisor cannot see the 1H signal identity, that `Bearish C.+` (n=4) and
`Trend C. Up` (n=6) both reach it as "1h BULL", and that the change was *"deliberately out of
scope — it modifies the entry path, and the per-signal n (largest cell 6) cannot calibrate it
yet."*

**The honest case for flipping it**, which your brief already anticipated: the OHLCV block
*already* shows the 1H market direction, so adding the LuxAlgo tier identity supplies **which
signal set the tier**, not a second vote. That is a real distinction and it is the strongest
argument for the change.

**The honest case against:** the recorded intent is that the advisor must not re-litigate the
cascade's own gate, and this would be SOL's **second** deliberate divergence from Titan in one
day (`PROPOSED ENTRY` is the first). Titan declined the same change for want of per-signal
sample size, and SOL's is smaller.

**What was done instead — the absence is now explicit rather than silent.** The prompt states
`1H LuxAlgo tier: NOT SHOWN in this prompt — do NOT assume it agrees or opposes`. That removes
the specific mechanism by which the old text let a hidden tier be read as a third agreeing one,
without deciding the flag. If you flip `AI_ADVISOR_HIDE_1H = False`, the 1H falls into the
agreement tally automatically — the code already branches on it — and it gains an age line too.
**One-line config change, no code edit needed. Your call.**

---

# §6 — WHAT IS ACTUALLY BEING SENT RIGHT NOW

## 6.1 The newest stored prompt is still the OLD format

**Zero consultations since the 16:17:51 restart.** The newest stored consultation is **row 14973,
16:00:01** — 18 minutes before the new code went live. Verbatim tail, with the tier lines:

```
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Down (direction: SHORT)
5m trigger: Within Bullish OB (direction: LONG)
...
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
...
The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

This is a textbook instance of the defect: **trade LONG, 15m tier SHORT, 5m trigger LONG, 1H
absent — and the prompt closes by asserting all three timeframes are aligned.** No
`PROPOSED ENTRY` line, no age, no agreement block.

The reason no consultation has occurred is visible in the journal — the cascade is rejecting
candidates before the advisor is ever called:

```
HTF_WOULD_PASS (tolerate-NEUTRAL) LONG 1H=NEUTRAL 15m=NEUTRAL 5m=LONG
HTF_NEUTRAL_15M_WOULD_BLOCK SOL/USDT:USDT LONG 1H=NEUTRAL 15m=NEUTRAL 5m=LONG
    reason=1H_neutral_15m_not_confirming dryrun=True
```

So the first production render is pending market conditions, not pending a defect.

## 6.2 The new format, rendered by the live code — **labelled for what it is**

Because no production consultation exists yet, I rendered one **through the live
`claude_advisor.py`** with `_call` stubbed so **no API request was made**, feeding the tier values
verbatim from real row 14973 — the disagreeing case you asked to see. **This is a render, not a
production consultation.** The `n/a` fields below are artifacts of the synthetic `vol_snap` I
supplied (I passed ATR/ADX keys but not the `trend_*`/EMA-gap ones); they are **not** defects in
the change, and the real prompt at 16:00 populated them correctly.

```
PROPOSED ENTRY: LONG
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Down (direction: SHORT, set 79m ago)
5m trigger: Within Bullish OB (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0520  |  Volume ratio 5m: 0.82x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 22.4 | 15m 21.2  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.363% | 15m 0.125% | 5m 0.071%
  EMA-gap: 1h n/a% (n/a) | 15m n/a% (n/a)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: N/A, ADX n/a, EMA-gap n/a% (n/a)
  ...
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, ? levels):
  Mid: $72.77  |  Imbalance ±1%: n/a
  Massive bid walls (>4x avg vol): none
  Massive ask walls (>4x avg vol): none

Tier agreement vs LONG (computed for this consultation):
  1H LuxAlgo tier: NOT SHOWN in this prompt — do NOT assume it agrees or opposes
  15m: HyperWave Signal Down -> SHORT = OPPOSES
  5m trigger: Within Bullish OB -> LONG = AGREES
  Of the 2 tier(s) shown: 1 agree, 1 oppose, 0 neutral, 0 absent.
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.
```

Same market state, same tiers, no false alignment claim: the 15m now reads **OPPOSES**, the
direction is stated once at the top as a field, the 15m carries **`set 79m ago`**, and the hidden
1H is named as hidden.

---

# §7 — POSITIONS, CONNECTIVITY, TITAN

**Positions — matches the expected book exactly:**

```
virtual_positions:  closed 18   |   open 0   |   MAX(id) 24
```

Confirmed by the journal at boot (`[VPOS-RECONCILE] no open paper positions at boot — clean.`).

**Connectivity — both reachable, tested live:**

| path | result |
|---|---|
| **Tor → Bybit** (`socks5h://127.0.0.1:9050`, per `tor_retry.py:42`) | ✅ `{"retCode":0,"retMsg":"OK","timeSecond":"1785602732"}` |
| **OKX book** (`SOL-USDT-SWAP`) | ✅ live depth, mid ≈ **$72.795** (asks from 72.80, bids from 72.79) |

**Titan — untouched, verified four ways:**

| check | result |
|---|---|
| `git status --short` | **clean** (no output) |
| `HEAD` | **`3316e8a`** — *"fix(titan): both money brakes read a set that could never populate"* |
| `titan.service` | **active** |
| files modified today under `/root/titan-bot` | **runtime data only**: `trades.db` (16:43), `optimizer/tg_offset.txt` (16:43), `healthcheck_state.json` (16:42), `oi_cache.json` (16:40). Newest **source** file is `risk_manager.py` at **13:04**, which is committed (git clean) and predates this session. |

**No Titan file was read for parameters and no Titan file was written.**

---

# §8 — ONE DOCUMENTATION-ONLY CORRECTION MADE

`OPEN-ITEMS-SOL.md` had mtime **16:17:41** and carried the 16:18 pre-registration in its body,
while its footer still read *"Last updated: 2026-08-01 15:36 UTC"*. That is precisely the
documented failure class — a canonical header that is not written back is a stale copy wearing an
authoritative name. The footer now reflects 16:52, names item 3 as held, and points at this file.
**Documentation only; no code, no config, no parameter.**

---

# §9 — THE PRE-REGISTRATION IS ALREADY ON DISK

`OPEN-ITEMS-SOL.md:21-63`, written **16:17:41, before the restart that made the prompt live** —
i.e. genuinely pre-registered, not back-filled:

| population | wrong-side rate | n |
|---|---|---|
| book-wide | **3.53 %** | 104 / 2,944 |
| inside prompts whose two visible tiers **disagree** | **9.70 %** | 103 / 1,062 |
| inside prompts whose two visible tiers **agree** | **0.05 %** | 1 / 1,882 |

Re-measure the same three over the **next 200 consultations** under the new prompt, by the
identical method: wrong-side when `ai_reason` names the side opposite the trade, matched on
`opposes <OPP>` / `against <OPP>` / `<OPP> entry` / `for a <OPP>`; "disagree" = both visible tier
directions present and different (the looser n=1,062 definition, **not** the strict n=912).

🔴 **If the disagreeing-population rate does not fall, the prompt's self-contradiction was not the
cause. Record that as-is** — do not re-cut the population until it agrees, and do not add further
prompt fields hoping to move it.

**Progress toward the 200: 0.** No consultation has occurred since the restart. At the pre-restart
rate (roughly one per 5–10 min when the cascade passes) this is hours-to-days away, and the
cascade is currently blocking on `1H_neutral_15m_not_confirming`. **Do not read the first handful
as a trend.**

---

# §10 — WHAT I DID NOT DO

- **Did not execute Part 2** — its precondition ("the prompt fix did not land") was false.
- **Did not apply item 3** — held for your decision, per your instruction.
- **Did not restart the service.** It is already running the new code; a second restart would
  have destroyed the running state for nothing.
- **Did not touch** news/funding/tape/OI/macro, the news observation gate, the system-prompt
  storage defect, or the 5m tier's class labelling.
- **Did not touch Titan** in any way.

## The one thing I want to flag plainly

An applied, live change existed for 45 minutes with a full on-disk pre-registration and **no
dated report**. The pre-registration was done properly; the publication step was the one that
did not happen. On this evidence, the work is sound and the record was the gap.

---

# DECISION REQUIRED FROM YOU

**Item 3 — flip `AI_ADVISOR_HIDE_1H` to `False`?** One line in `config.py`, no code change; the
agreement tally and the age line pick the 1H up automatically. Arguments both ways are in §5. The
flag's recorded intent says no; the fact that the OHLCV block already shows the 1H *direction*
(so this adds only *which signal* set the tier) says the objection is weaker than it looks.

Everything else is applied, live, compiled, pre-registered, and awaiting market conditions to
produce its first production prompt.
