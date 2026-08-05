# TITAN — THREE FALSE STATEMENTS REMOVED FROM THE PROMPTS. AND ONE OF THEM WAS NOT PURELY COSMETIC.

**2026-08-05 19:40 UTC · 🔴 APPLIED FROM FLAT · HEAD `1ec2477` → `de1d0f2` · restarted 19:38:30 UTC**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
**0 open positions and 0 `exit_pending`** at application, re-checked immediately before the restart.
**Mercury-SOL never opened.**

Parent: `2026-08-05-1925-titan-audit-every-prompt-rule-for-the-unsatisfiable-defect.md`.

**All three edits REMOVE a falsehood.** No new policy, no new threshold, no invented number.
`main.py` untouched. `config.py` changed by **exactly one non-comment line.**

---

## 🔴 READ THIS FIRST — ONE OF THE THREE IS NOT THE PURE TRUTHFULNESS FIX IT WAS BILLED AS

The brief said of the `AI_ADVISOR_HIDE_1H` flip: *"This is a TRUTHFULNESS fix, not an information
change — the direction is already reaching the model 100 % of the time. Confirm that."*

**Confirmed for the direction. Not confirmed for everything else.** Rendered through the real
`signal_tiers.render()`, before and after:

```
BEFORE (HIDE_1H=True)
  1H:  Smart Trail Bullish  (direction withheld (AI_ADVISOR_HIDE_1H), weight 0.9)
  15m: HyperWave Signal Down  (SHORT, weight 0.7)
  5m:  Within Bearish OB  (SHORT, weight 0.7)
  Agreement: 15m and 5m both point SHORT; vs the proposed SHORT: 15m+5m agree.

AFTER (HIDE_1H=False)
  1H:  Smart Trail Bullish  (LONG, weight 0.9)
  15m: HyperWave Signal Down  (SHORT, weight 0.7)
  5m:  Within Bearish OB  (SHORT, weight 0.7)
  Agreement: 1H points LONG; 15m+5m point SHORT; vs the proposed SHORT: 15m+5m agree, 1H OPPOSE.
```

🔴 **The direction is not new — "Bullish" was in the name all along. THE AGREEMENT LINE IS.** It now
states the 1H's stance *against the proposed direction* — "**1H OPPOSE**" — a derived comparison that
was computed without the 1H before and is present on every prompt where a 1H tier exists (**81/81**
current-era).

Two further fields also stop being suppressed, though they print only in their rarer disagreement
cases: `gate_direction` (renders *"slot and matrix disagree"* when it differs from the tier
direction) and `counted_by_gate is False` (renders a not-counted phrase).

**So this is a truthfulness fix that also restores information.** It is factual, carries no verdict,
and breaks no standing line — but **it can change behaviour, and calling it cosmetic would have been
wrong.** It is flagged here rather than discovered later in a drift number.

---

## 1. 🔴 THE EXIT SYSTEM PROMPT'S TRAIL CLAIM — REMOVED

### (a) REMOVED, NOT REPLACED

```
BEFORE  You are an automated trading exit module. Decide whether to CLOSE the open
        position now or HOLD it. The stop-loss and trailing stop remain active if you hold.

AFTER   You are an automated trading exit module. Decide whether to CLOSE the open
        position now or HOLD it.
```

**Verified on the BUILT string, not the source:** `'trailing stop remain active'` absent ·
the word `trail` absent entirely · `stop-loss` absent entirely.

### (b) THE COMMENT LEFT IN ITS PLACE — THE LESSON, NOT THE CHANGE

The transferable finding is not "a sentence was wrong". It is **how a fixed defect kept shipping**:

> *"This is the exact claim `c307bb7` deleted on 2026-07-29. That commit measured it (**"FALSE on 56
> of the first 59"**), named it, and fixed it — **IN THE USER PROMPT ONLY**. The identical sentence
> went on shipping in the system prompt of the same call for another 58 consultations, because the
> fix was verified by re-reading the user-prompt builder rather than the prompt that is actually
> sent. **A defect can be known, measured, written up and still live, if it lived in two places and
> only one was searched.**"*

### (c) 🔴 NO STATEMENT ABOUT THE STOP EITHER — AND THE REASON IS NOT PEDANTRY

The brief asked whether a truthful statement about the stop alone is worth keeping. **My answer is
no, on two independent grounds:**

1. `_protection_block()` already prints the live stop price, its distance in R, whether the trail has
   armed and the exact price at which it would — **per consultation, from the position's own state.**
   Any system-level restatement is strictly more generic than what the user prompt already carries,
   and it was exactly that genericity that made the original claim wrong.
2. 🔴 **"The stop is always active" is itself not guaranteed.** On **2026-07-29 this bot produced a
   NAKED position** when stop placement failed after a fill. The stop's existence is a fact to be
   read off the position — which the user prompt does — **not a promise to be made in advance.**
   Re-asserting it at system level would have re-created the same defect one layer down.

### ⚠️ WHAT TO WATCH — THIS IS THE ONLY MEASURED POSITIVE IN THE SYSTEM (+3.3729R over 5 closed)

| measure | baseline, from the 118 stored consultations |
|---|---|
| **close-verdict rate** | **58 close / 60 hold = 49.2 %** overall; on the §2.18-clean 58 post-`c307bb7`: watch this most closely |
| **reasons mentioning a trail** | **12 / 118 = 10.2 %** — of which pre-fix **2** relied on an unarmed trail, post-fix **0** |
| the specific failure that must not return | a HOLD justified by trail protection below +1R (*"Hold; let trail manage downside"*, +0.00R, row 19216) |
| the specific behaviour that should persist | correct conditional usage (*"Hold for trailing-stop arm at +1R"*, row 19460) |

**Prediction, stated so it can be wrong:** the close rate should **not** move materially — the user
prompt already carried the truth and was already winning (0 of 58 post-fix misinferences). **If the
close rate moves by more than a few points over the next ~30 consultations, the system prompt was
doing more work than the audit showed and that is worth knowing.** Reasons mentioning a trail should
stay at or below 10.2 %; they can legitimately fall, since the system prompt no longer raises the
topic unprompted.

**Revert:** `EXIT_ADVISOR_DRYRUN = True` (`config.py:278`) is unchanged and remains a **one-line**
revert — a `close` verdict then stops closing. **The branch it gates
(`virtual_trader.py:2479`, `main.py:3210`) is not touched by this commit**, verified by diff.

---

## 2. 🔴 `AI_ADVISOR_HIDE_1H` → `False`

**It never worked.** It replaced the direction *field* and left the signal *name*, which states the
direction: `Smart Trail **Bullish**`, `**Bullish** Confirmation+`, `**Bearish** Confirmation+`,
`Trend Tracer **Up**`. Measured: **101 of 101** withheld entry lines and **57 of 57** withheld exit
lines — **100 %, both prompts, every era since the flag shipped.**

**Why not the other repair:** stripping the direction out of the NAME would mangle a LuxAlgo
identifier into something that no longer matches the source feed, breaking every join, tally and
report keyed on the signal name. **Truthfulness is cheaper on this side.**

**(a) Is any figure now present that was absent before?** 🔴 **Yes — see the section at the top.**
The direction is not new; **the Agreement line's treatment of the 1H is.**

**(b) Parity recorded in the comment:** Mercury-SOL set the same flag `False` on **2026-08-01**, for
a related reason — the objection did not survive its own premise, since 15m and 5m are cascade gates
too and are shown in full.

**(c) Why, recorded in the comment** so a future parity sweep does not revert it, together with what
does **not** change: the hard `_htf_cascade_gate` still uses 1H independently, the signal matrix is
unchanged, `1h_context` stays in the snapshot for every other consumer, and the OHLCV-derived 1H row
in the Higher-Timeframes block was never governed by this flag.

---

## 3. 🔴 THE COMBO-WEIGHT DOLLAR THRESHOLDS

```
BEFORE  Combo weight: 1.00  (1.00 = untouched; -0.10 per evaluation that lost more than $15,
        +0.10 per one that gained more than $20)

AFTER   Combo weight: 1.00  (1.00 = untouched. The store moves it by -0.10 per evaluation that
        lost more than $15 and +0.10 per one that gained more than $20. Those thresholds were set
        when this bot traded at ~68x its current size; at the current size they are 8-15R, beyond
        anything a single position here has produced, so this number does not currently move.)
```

**WHICH REPAIR I CHOSE, AND WHY:** the brief offered *express the thresholds in R* or *state plainly
that it cannot fire*. **I chose the plain statement.** 1R moves with ATR, so rendering the thresholds
in R would print a freshly-computed pair of numbers on **every** prompt in order to describe a
mechanism that is inert either way — more machinery than the truth needs, and a new number where the
honest content is a plain fact.

🔴 **AND THE R-FIGURE QUOTED IS THE PROJECT'S OWN.** "8-15R" is §2.40d's existing measurement
(`main._combo_weight_provenance`: *"Against a live 1R of $1.32-2.49 that needs 8.0R-15.1R… no weight
has moved, or can move, at the current size… The table is frozen."*). **I did not introduce my own
9.3R/12.4R** — one fact, one number, travelling with its original provenance.

**The constants are NOT touched.** §2.40/§2.41 remain a coupled, deferred decision. This changes what
the prompt **says**, not what the weight store **does**.

⚠️ **The evidence was already in the codebase, in two docstrings, since 2026-08-03 — and the prompt
went on contradicting them for 2,724 renders.** That is the same shape as finding 1: the knowledge
was written down in the place that explains the code, and the falsehood lived in the place that talks
to the model.

---

## VERIFICATION LEDGER

| check | result |
|---|---|
| `ast.parse` + `py_compile`, all three files | ✅ |
| trail claim absent from the **built** `_CLOSE_SYSTEM_RICH` | ✅ (`trail`, `stop-loss` both absent) |
| `AI_ADVISOR_HIDE_1H` as imported at runtime | ✅ **`False`** |
| combo-weight line renders truthfully, both provenance paths | ✅ |
| 🔴 `_ENTRY_SYSTEM` md5 | **`d7b8f3ed…` — UNCHANGED** |
| 🔴 `_CLOSE_SYSTEM` md5 (the non-rich close prompt) | **`86fbc2e0…` — UNCHANGED** |
| `config.py` non-comment changes | **exactly one line**, `True` → `False` |
| `main.py` | **untouched** |
| flat before application | **0 open / 0 `exit_pending`**, checked twice |
| restart | `active`, `19:38:30 UTC`, 🔴 `LIVE ORDERS — REAL MONEY` unchanged |
| boot reconciliation | ✅ *"exchange and DB agree: 0 exchange position(s), 0 open row(s)"* |
| `EXIT_ADVISOR_DRYRUN` revert path | ✅ `False` unchanged, branch untouched by this diff |
| gates/geometry identifiers in the diff | only inside **comments** — verified by grep |

**Untouched:** EMA envelope gate · HTF cascade · FLAT floor · Variant-B · score bars · risk gates ·
geometry (SL 2.25 / trail 0.75R) · the weight store's constants · every schema.

**Snapshots:** `/root/backups/prompt-truth-20260805-1930/` (all three files, md5-verified).
**Revert:** `git revert de1d0f2`.

---

## NOT IN SCOPE — RECORDED, AS INSTRUCTED

**Finding 4 — six decisive adjectives with no number** (*"clearly oppose"*, *"exceptionally strong"*,
*"coherent"*, *"chop/false break"*, *"dominant"*). 🔴 **Deliberately NOT fixed, and the operator's
reasoning is the right one:** the wall rule could be given a number only because the prompt **already
asserted** *"~50th is ORDINARY"*. No such number exists for these, and inventing one would be **new
policy dressed as a correctness fix**. This is now **the largest remaining instance of the class** —
it includes *"clearly oppose"*, the only other rule in the prompt that says *"lean toward skip"* —
and it needs **evidence, not an edit**.

**Findings 5, 6, 7 — measured, no action:** *"EVERY book state contains a wall above 4x"* is 86.0 %
as read (99.4 % loosely, n=33,534) · the MTF alignment summary excludes the 1d the rule calls
dominant (81/81) · *"IDENTITY ONLY: no past performance"* sits three lines above a combo-weight block
that encodes exactly past performance.

---

## ⏳ THE ITEM STILL OPEN FROM 19:15 — STATED AGAIN RATHER THAN LEFT TO LAPSE

**No stored real prompt with per-wall percentiles has landed yet.** The last consultation of any kind
was **16:40:10 UTC**; there have been **zero** since the 19:08 restart, and the 15-minute watcher
expired empty. **The 18:55 wall change is confirmed on a live book through the real code path but
still has no stored-prompt confirmation** — and today's restart resets that clock again. Both this
and the three changes above will be visible in the first consultation that fires.

---

## LIVE STATE

| | |
|---|---|
| HEAD / `git status` | **`de1d0f2`** / **clean** |
| open positions | **0** |
| service | `titan.service` **active**, restarted **19:38:30 UTC** |
| order mode | 🔴 **LIVE REAL MONEY**, $30 × 5 — unchanged |
| `AI_ADVISOR_HIDE_1H` | **`False`** |
| `EXIT_ADVISOR_DRYRUN` | `False` — the advisor is ACTING |
| consultations since restart | **0** |
