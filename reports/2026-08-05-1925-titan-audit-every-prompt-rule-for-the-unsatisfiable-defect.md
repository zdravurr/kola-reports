# TITAN — AUDITING EVERY PROMPT RULE FOR THE DEFECT WE JUST FIXED: **IT IS NOT SINGULAR. THE WORST INSTANCE IS IN THE EXIT PROMPT.**

**2026-08-05 19:25 UTC · READ-ONLY · nothing changed, NOTHING PROPOSED, NO DIFF · HEAD `1ec2477`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
`git status` clean before and after · `trades.db` opened read-only, **absolute path pinned** ·
**0 open positions** throughout · **Mercury-SOL never opened.**

Parents: `2026-08-05-1915-titan-wall-veto-percentile-applied-live.md`,
`2026-08-05-1855-titan-make-the-wall-veto-do-what-it-says.md`.

**Corpus: 2,724 stored entry prompts and 118 stored exit prompts**, counted the way the wall audit
was counted. **Era-split throughout**, because the prompt's shape changed repeatedly and an
all-time percentage would misrank a fixed defect as a live one.

---

## ANSWER IN ONE LINE

🔴 **THE WALL RULE WAS NOT SINGULAR — THE CLASS HAS FOUR MORE MEMBERS, AND THE MOST SEVERE IS IN THE
EXIT PROMPT, THE ONLY MEASURED POSITIVE IN THIS SYSTEM.**

1. 🔴 **The exit system prompt asserts "The stop-loss and trailing stop remain active if you hold" on
   118 of 118 consultations. It was FALSE on 114 of them (96.6 %).** This is the *exact* claim
   `c307bb7` was written to delete on 2026-07-29 — **the fix was applied to the user prompt and the
   system prompt was left asserting it**, so the two halves of the same request now contradict each
   other on 57 consults.
2. 🔴 **`AI_ADVISOR_HIDE_1H` does not hide the 1H direction.** It suppresses the direction *field*
   while the signal **name** states it — *"Smart Trail **Bullish** (direction withheld)"* — on
   **101 of 101** withheld entry lines and **57 of 57** withheld exit lines. **100 %, both prompts,
   every era.** Meanwhile the system prompt still promises the model a "1H trend".
3. 🔴 **The combo-weight block states a mechanism in dollars that cannot fire at live size.**
   *"−0.10 per evaluation that lost more than $15"* is **9.3R** at the live 1R of $1.61, and
   **12.4R** for the $20 side. **0 of 10 live-sized closed rows have ever come near it.** On paper
   rows the same constants are ~**0.1R** — the identical sentence is two different rules depending
   on sizing, and the prompt states it as a fact.
4. **"EVERY book state contains a wall above 4x"** — true on 99.4 % either-side, but **86.0 %** as
   the model must read it (both sides). The word is "EVERY".
5. **Four decisive terms in the entry prompt are adjectives with no number anywhere** — the wall
   rule's original defect, still present in the surrounding rules.

**And what is CLEAN is worth as much as what is not:** the exit prompt's percentiles rank
max-against-max — **apples-to-apples, no baseline defect**, unlike the entry side I had to fix at
18:55. The exit *user* prompt's protection block is computed per consultation and is correct. The
ADX interpretation was already retired. **The class is not everywhere.**

**No fixes proposed. This is the map, as asked.**

---

# PART ONE — THE ENTRY PROMPT

## §1 — EVERY INSTRUCTION THAT NAMES A QUANTITY

The entry system prompt is **1,871 characters**. Every instruction in it is enumerated below; none
is omitted.

### 1.1 🔴 "You receive multi-timeframe LuxAlgo signal context (**1H trend**, 15m confirmation, 5m trigger)"

**(a) verbatim** — opening sentence of `_ENTRY_SYSTEM`.

**(b) is the figure rendered for the object the rule names?** 🔴 **NO.** The 1H tier line renders as:

```
  1H:  Smart Trail Bullish  (direction withheld (AI_ADVISOR_HIDE_1H), weight 0.9, last set 5.8h ago)
```

**(c) how often:**

| era | 1H line present | 🔴 **1H direction visible** |
|---|---|---|
| all time (n=2,724) | 8.8 % | **5.1 %** |
| since 2026-07-13 (n=511) | 19.8 % | 🔴 **0.0 %** |
| **current, since 2026-08-01 (n=81)** | **100 %** | 🔴 **0.0 %** |

**On the machine as it runs today the 1H line is always present and its direction is never visible.**
`config.AI_ADVISOR_HIDE_1H = True`.

**(d) 🔴 IS IT RENDERED FOR A DIFFERENT OBJECT? WORSE — IT IS RENDERED IN THE SAME BREATH AND DENIED.**

| the direction is stated **inside the signal name** on a "withheld" line | |
|---|---|
| ENTRY | **101 / 101 = 100 %** |
| EXIT | **57 / 57 = 100 %** |

Observed name forms, all self-describing: `Smart Trail **Bullish**` (21×), `**Bullish** Confirmation+`
(30×), `**Bearish** Confirmation+` (10×), `**Bullish** Confirmation` (9×), `Trend Tracer **Up**`.

🔴 **The suppression has never once worked.** It removes a parenthesis and leaves the adjective. Any
reader — and the model is a reader — recovers the direction from the name. **This is the wall defect
precisely: a stated mechanism whose stated effect does not occur, invisible until counted.**

⚠️ **What I am NOT claiming:** that hiding the 1H is right or wrong. That is a separate question
this audit does not touch. The finding is only that **the flag does not do what its name says.**

### 1.2 "Treat the 1d and 4h trends as the dominant regime"

**(b)** ✅ both **are** rendered, per timeframe, with ADX and EMA-gap.
**(c)** HTF block on **81/81** current-era prompts.
**(d)** ⚠️ **a milder instance of the class:** the summary the model is handed —
`MTF alignment vs SHORT: 0/4 (4H/1H/15m/5m; **excludes 1d**)` — **omits the timeframe the rule calls
dominant**, on **81/81** prompts. The raw 1d row is present, so this is not the wall case; but the
one *aggregated* figure disagrees with the rule about which timeframes matter.

### 1.3 "…plus 5m ATR and volume ratio… ADX on 1h/15m, ATR% of price, EMA-gap compression, market_regime, MTF alignment"

**(c)** All rendered on **81/81 (100 %)** current-era prompts. Historic gaps (93.2 % all-time) are
**pre-2026-07-13 format churn, not live defects** — stated so they are not misranked.

### 1.4 THE HARD RULE — **fixed at 19:08 today, verified, no longer in this class**

Now names its own line (~50th / 90th) and every wall carries its own percentile against the
nearest-wall baseline. Confirmed live at 19:07: five walls, five percentiles.

### 1.5 🔴 THE COMBO-WEIGHT BLOCK — A MECHANISM STATED IN DOLLARS

**(a)** *"Combo weight: 1.00 (1.00 = untouched; **−0.10 per evaluation that lost more than $15,
+0.10 per one that gained more than $20**)"*

**(b)/(c)** Present on **2,724/2,724 = 100 %** of entry prompts — **the highest-frequency block in
the audit.** Observed values: `1.00` × 2,681 (**98.4 %**), `0.90` × 41, `0.80` × 2.

**(d) 🔴 THE FIGURE IS REAL BUT THE THRESHOLD BELONGS TO A DIFFERENT MACHINE:**

| | live-sized closed rows | paper rows |
|---|---|---|
| n | **10** | 49 |
| mean 1R | **$1.61** | $145.76 |
| `$15` threshold in R | 🔴 **9.3R** | ~0.10R |
| `$20` threshold in R | 🔴 **12.4R** | ~0.14R |
| observed net PnL range | **−$2.54 … +$2.30** | −$201.83 … +$441.84 |
| 🔴 **rows ever crossing either threshold** | 🔴 **0 of 10** | 40 of 49 |

**The same sentence describes a rule that fires on four trades in five (paper) and a rule that cannot
fire at all (live).** The prompt states it flatly, in dollars, with no sizing attached. This is
§2.45's *"the weight mechanism is inert at live size — but its output is in the prompt anyway"*
(2026-08-03), now measured from the prompt side: **the model is told the mechanism every single time.**

---

## §2 — INSTRUCTIONS WHOSE DECISIVE TERM IS AN ADJECTIVE

The wall rule's operative word was *"genuinely THICK"* with the only number forty lines away. Same
search across the rest:

| instruction (verbatim) | decisive adjective | is there a number? |
|---|---|---|
| "when they **clearly oppose** the proposed entry direction, lean toward 'skip'" | **clearly** | 🔴 **none anywhere** |
| "…unless the lower-TF confluence is **exceptionally strong**" | **exceptionally strong** | 🔴 **none anywhere** — no confluence scale is printed at all |
| "vote 'execute' when the context **looks coherent**" | **coherent** | 🔴 **none anywhere** |
| "'skip' when it **looks like a chop/false break**" | **chop/false break** | 🔴 none — and `market_regime`'s own FLAT label is printed but carries no threshold |
| "Treat the 1d and 4h trends as the **dominant** regime" | **dominant** | 🔴 none |
| "when 1d/4h agree with the entry, that is **supportive context**" | **supportive** | none (harmless — no action attached) |
| HARD RULE "**genuinely unusual**" | genuinely unusual | ✅ **~50th / 90th, in the rule itself** — *as of 19:08 today* |

🔴 **Six decisive terms, one number — and that number was added today.** The 1d/4h rule is the
second-most-consequential instruction in the prompt (it is the only other one that says "lean toward
skip") and **its trigger condition is the word "clearly".**

**`_CLOSE_SYSTEM_RICH` and `_CLOSE_SYSTEM` contain no such adjectives at all** — they are short and
make no judgement calls. Clean.

---

## §3 — MECHANISTIC ASSERTIONS vs WHAT THIS BOOK HAS MEASURED

| assertion | status |
|---|---|
| ~~"strong resting liquidity **will absorb the move before it can develop**"~~ | 🔴 **CONTRADICTED — 95 % of cited walls traded through within 24h. REMOVED at 19:08 today** |
| **"EVERY book state contains a wall above 4x"** | ⚠️ **99.4 %** either side; 🔴 **86.0 %** both sides, which is how the model must read it against a specific side. **33,534 snapshots.** The claim is load-bearing — it is the justification for "a large ×-figure on its own says nothing" — and it is 14 points short of "EVERY" |
| **"−0.10 per evaluation that lost more than $15"** | 🔴 **unreachable at live size (9.3R); ~0.10R on paper.** §1.5 |
| **"Treat the 1d and 4h trends as the dominant regime"** | ⚠️ **UNVALIDATED, not contradicted.** §2.55 found no predictor survives correction (the apparatus is *"unfalsified, not validated"*); §2.45 killed four `market_regime` redefinitions. Nothing in this book establishes 1d/4h dominance — but nothing refutes it either, so it is recorded as an assertion without evidence, not as a falsehood |
| ADX interpretation *("~<20-23 = weak/ranging")* | ✅ **already retired `c307bb7`** — and our data pointed the other way |
| "(Contracting/Flat = compression)" | ✅ definitional, not a claim about outcomes |
| SIGNAL TIERS *"IDENTITY ONLY: no win rate or past performance is implied"* | ⚠️ **in tension with the combo-weight block three lines below**, which encodes exactly past performance (*"per evaluation that lost…"*). Both are on 100 % of prompts |

---

# PART TWO — THE EXIT PROMPT *(reported separately, as instructed)*

The exit advisor is the only measured positive in this system (**+3.3729R over five closed
positions**, §2.4). It uses **`_CLOSE_SYSTEM_RICH`** — 310 characters.

## §4.1 🔴 THE WORST FINDING IN THIS AUDIT

**`_CLOSE_SYSTEM_RICH`, verbatim and complete on the point:**

> *"You are an automated trading exit module. Decide whether to CLOSE the open position now or HOLD
> it. **The stop-loss and trailing stop remain active if you hold.**"*

**The trailing stop arms at +1R. Below +1R it does not exist.**

| | |
|---|---|
| exit consultations with this system prompt | 🔴 **118 / 118 = 100 %** |
| of those, position was **below +1R** (trail cannot be armed) | 🔴 **114 / 118 = 96.6 %** |
| at or above +1R (claim true) | 4 / 118 = 3.4 % |
| user prompt explicitly says **"The trailing stop is NOT ARMED"** | 57 / 118 |
| 🔴 **system asserts it AND the user prompt denies it, same request** | 🔴 **57 / 118 = 48.3 %** |

### 🔴 AND THIS IS THE CLAIM `c307bb7` WAS WRITTEN TO DELETE

The comment sitting in `claude_advisor.py` today, beside the *user*-prompt fix:

```python
        # WHAT ACTUALLY PROTECTS THIS POSITION IF YOU HOLD (2026-07-29).
        # This replaced the flat assertion "The stop and trail remain active if you
        # HOLD", which was printed on every consultation and was FALSE on 56 of the
        # first 59: the trail arms at +1R and those consults were all below it.
```

**The identical sentence was left standing in the system prompt of the same call.** The defect was
found, named, measured and fixed — **in one of the two places it lived.** 60 consults carried it in
both halves; 58 have carried it in the system half alone since.

### DID IT CHANGE A DECISION? — MEASURED, AND THE ANSWER IS NUANCED

| | |
|---|---|
| advisor reasons mentioning a trail | 12 / 118 = 10.2 % |
| 🔴 **pre-`c307bb7`: HOLD justified by a trail that was not armed** | 🔴 **2 of 60** |
| **post-`c307bb7`: same** | ✅ **0 of 58** |

The two pre-fix cases, verbatim:

> *"…No regime reversal—15m/5m still bullish, ADX strengthening. **Hold; let trail manage
> downside.**"* — row 19216, **+0.00R**, decision **hold**

> *"…+0.58R with 1.58R cushion and only 0.06R giveback from peak—tight risk/reward. **Hold through
> trailing st[op]**"* — row 19413, **+0.58R**, decision **hold**

**Both held a position on the strength of a trailing stop that did not exist.**

🔴 **AND THE HONEST OTHER HALF: since the user-prompt fix, the model has not made that inference
once.** Post-fix reasons are careful — *"Hold for trailing-stop arm at +1R"* (19460), *"Hold for
trailing-stop trigger at +1R"* (19722), *"trailing stop not [armed]"* (19908). **The user prompt is
winning over the system prompt on every observed case.** The residual falsehood is therefore
**latent, not currently active** — but it is asserted 118 times out of 118 and is contradicted by
the same request 57 times, and it is the reason the pre-fix errors happened at all.

⚠️ **ONE CORRECTION TO MY OWN COUNTING, RECORDED RATHER THAN QUIETLY FIXED.** My first pass flagged
**4 post-fix failures**. Reading them individually, all four are *correct* usage — and one, row 19470
(*"1h smart trail (weight 0.9) remains active"*), is not about the trailing stop at all: **"Smart
Trail" is a LuxAlgo signal name.** The regex could not tell the LuxAlgo tier from the stop mechanism.
**The true post-fix count is 0.** A name collision between an indicator and a risk mechanism is worth
knowing about on its own.

## §4.2 THE EXIT PROMPT'S QUANTITIES — AND WHY THIS SIDE IS MOSTLY CLEAN

| instruction / figure | verdict |
|---|---|
| *"Judge by the percentile: ~50th is ORDINARY"* + `Supporting wall = 57th pct` / `Opposing wall = 65th pct` | ✅ **CLEAN, and notably so.** `sup`/`opp` are the **max** wall multiples and are ranked against **`max_wall_mult_bid/ask`** — max-against-max. **The entry side's baseline defect does not exist here** |
| which wall the percentile describes | ✅ **CLEAN** — the exit block names no individual price levels, so there is no wall-identity ambiguity to get wrong |
| the protection block (*"NOT ARMED … would arm at 64701.1"*) | ✅ **CLEAN** — computed per consultation from the position's own state |
| `Elapsed: 4.0h` | ✅ present on **118/118** (confirmed 17:25 today) |
| 🔴 the 1H tier line | 🔴 **direction withheld on 57/60, name leaks it on 57/57 = 100 %** — §1.1 applies identically here |
| *"Recent 5m structure (CONTEXT ONLY — never a trigger)"* | ✅ clean — an explicit non-instruction |
| adjectives with no number | ✅ **none** |
| mechanistic "X means Y" claims | ✅ **none besides the trail claim** |

---

# §5 — VERDICT, RANKED BY HOW OFTEN THE AFFECTED RULE FIRES

| # | finding | fires on | severity |
|---|---|---|---|
| **1** | 🔴 **EXIT system prompt asserts an active trailing stop** | **118/118 = 100 %** of exit consults; **false on 96.6 %**; contradicted by its own user prompt on 48.3 % | 🔴 **HIGHEST.** In the only measured positive. Demonstrably changed 2 HOLD decisions pre-fix. Latent since — the user-prompt fix is holding |
| **2** | 🔴 **`AI_ADVISOR_HIDE_1H` does not hide the direction** | **100 %** of current-era entry prompts (81/81) and **100 %** of withheld lines in both prompts (101/101, 57/57) | 🔴 **HIGH.** A named mechanism with zero effect, in both prompts, every era. The system prompt also promises a "1H trend" the render withholds |
| **3** | 🔴 **Combo weight stated in dollars, unreachable at live size** | **2,724/2,724 = 100 %** of entry prompts | 🔴 **HIGH by frequency.** 9.3R / 12.4R live; 0 of 10 live rows in range; ~0.1R on paper |
| **4** | **Six decisive terms are adjectives with no number** | **100 %** — includes the only other "lean toward skip" rule | **MEDIUM.** Exactly the wall rule's original shape, unfixed in its neighbours |
| **5** | **"EVERY book state contains a wall above 4x"** | **100 %** of prompts carrying the scale | **MEDIUM-LOW.** 86.0 % as read, 99.4 % loosely. Load-bearing but directionally right |
| **6** | **MTF alignment summary excludes the 1d the rule calls dominant** | **81/81 = 100 %** | **LOW.** The raw 1d row is present; only the aggregate disagrees |
| **7** | **"IDENTITY ONLY: no past performance" vs the combo-weight block** | 100 % | **LOW.** Internal tension, no measured consequence |

## 🔴 SO: WAS THE WALL RULE SINGULAR? **NO — AND THAT IS THE ANSWER THAT MATTERED**

The brief asked to be told if nothing else had this shape. **Four more instances do**, and the class
turns out to have three distinct forms worth naming separately:

1. **The figure is not rendered for the object the rule names** — the original wall defect.
2. **The mechanism has no effect** — `AI_ADVISOR_HIDE_1H`, defeated by the signal name 100 % of the time.
3. 🔴 **The fix landed in one of the two places the claim lived** — `c307bb7`. **This is the most
   dangerous form, because the defect is already known, already measured, already written up, and
   still shipping.** It would not be found by re-reading the report that fixed it; only by reading
   the prompt that is actually sent.

**And the reason all five survived is the same reason the wall rule did: the model complied with
something, and the output looked reasonable.** None of these produces an error message. Two of them
(the trail claim, the 1H hide) were introduced *by* a previous correctness fix.

⚠️ **Scope of this audit, stated so it is not over-read:** it covers `_ENTRY_SYSTEM`,
`_CLOSE_SYSTEM_RICH`, `_CLOSE_SYSTEM` and the user prompts as rendered. **`_LEARNING_SYSTEM`
(post-trade attribution) was read and is not in this class** — it asks for attribution and names no
threshold. Non-prompt mechanisms (gates, cascade, geometry) were not audited.

---

## LIVE STATE

| | |
|---|---|
| HEAD / `git status` | **`1ec2477`** / **clean** |
| open positions | **0** |
| consultations since the 19:08:39 restart | **0** — ⏳ the stored-prompt confirmation of the 19:15 change is **still pending**, as reported then and not yet closed |
| `config.AI_ADVISOR_HIDE_1H` | `True` |
| entry prompts audited | **2,724** · exit prompts **118** |

*Read-only throughout. Nothing proposed, no diff, `titan-bot` unmodified at `1ec2477`, 0 open
positions for the entire pass, `trades.db` opened read-only on its absolute path. Mercury-SOL never
opened.*
