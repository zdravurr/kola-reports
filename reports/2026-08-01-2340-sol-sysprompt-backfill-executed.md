# sol-sysprompt-backfill-executed

_2026-08-01 23:40 UTC_

---

# MERCURY-SOL — BACKFILL EXECUTED. **32 ROWS, ONE COLUMN, VERIFIED.** SOL IS DONE FOR THE NIGHT.

`changes() = 32`, committed, `quick_check` **ok**. SOL stays **PAPER**, the entry prompt is
byte-identical, the window is **still 4 of 200**, no open position, Titan untouched.

---

# §1 — THE BACKFILL

## Dry run first — every precondition checked per row, nothing assumed

Before any write, all 32 rows were tested against **five** conditions, and each row additionally
had to **prove its own invertibility**:

| condition | result |
|---|---|
| `ai_system_prompt` not NULL | 32/32 |
| stored base **contains** `_WALL_RULE_V1` | 32/32 |
| the replace is **not** a no-op | 32/32 |
| V1 **absent** after the replace | 32/32 |
| the correct V2 block **present** after the replace | 32/32 |
| 🔴 **`soft.replace(V2, V1) == stored base`** — per-row invertibility | **32/32** |

**0 skipped.** Split **16 buy / 16 sell**, all dated 2026-07-10 → 2026-08-01 — consistently after
both aligned flags went live (LONG 07-02, SHORT 07-04), which is the independent sanity check that
the population is the right one.

The reconstruction matched the module exactly: `_ENTRY_SYSTEM_V2_ALIGNED[_SHORT] =
_ENTRY_SYSTEM.replace(_WALL_RULE_V1, _WALL_RULE_V2_ALIGNED[_SHORT])` — verified at
`claude_advisor.py:157` and `:178` — applied to **each row's own** stored base, so every row gets
the base of its era.

## Execution

Backup `trades.db.bak_pre_sysprompt_backfill_20260801` (42,688,512 bytes, 21:12:55) taken first.
Single `BEGIN IMMEDIATE`; the script aborts and rolls back unless `changes()` is exactly 32.

```
changes() = 32
COMMITTED
```

## Verification

| check | result |
|---|---|
| **`changes() == 32`** | ✅ |
| **`PRAGMA quick_check`** | ✅ **ok** |
| rows now containing the **correct** V2 wall block | ✅ **32/32** |
| rows **no longer** containing V1 | ✅ **32/32** |
| rows elsewhere in the book still on V1 (must be untouched) | ✅ **2,765** — unchanged |

**Nothing but `ai_system_prompt` altered — spot-checked on three rows, before and after:**

| id | `ai_decision` | `ai_confidence` | `ai_reason` | `ai_raw_response` | `pnl` | `ai_system_prompt` length |
|---|---|---|---|---|---|---|
| 8446 | execute → execute | 0.72 → 0.72 | unchanged | unchanged | unchanged | 2179 → **2410** |
| 10178 | execute → execute | 0.72 → 0.72 | unchanged | unchanged | unchanged | 2179 → **2326** |
| 14988 | execute → execute | 0.78 → 0.78 | unchanged | unchanged | unchanged | 2179 → **2326** |

The two different new lengths are the expected signature: 8446 is a **buy** (LONG rule, 2410) and
the other two are **sells** (SHORT rule, 2326). A single uniform length would have meant the
side-selection was wrong.

---

# §2 — vpos 25 WAS ITSELF ONE OF THE 32

You put this precisely: **the trade we spent the evening analysing was itself a flip.**

Row **14988** — vpos 25's entry — was a `WALL-ALIGNED-SHORT-V2` flip. V1 said *skip*; the SOFT
prompt said *execute*; the SOFT verdict was adopted. **So the position that produced the partial
mechanism's first live datapoint was decided by a system prompt that was never stored** until
21:13 tonight.

Both records now cross-reference each other in `OPEN-ITEMS-SOL.md`, because a future reader
needs both facts about the same trade:

- it is the **first full production lifecycle** of partial-at-arm, and the mechanism **cost 0.155R**
  on it (bounded downside, working as designed, **not** vindication — +1.412R without the partial);
- it is **one of the 32** whose decision provenance was mis-recorded — and, per the permanent
  limitation, **its V2 raw response is gone**, so that decision can be **replayed but never
  audited** against the model's own words.

The backfill fixes *which prompt asked*. It cannot recover *what the model answered*. For vpos 25
that gap is permanent.

---

# §3 — NET vs GROSS, BOTH RECORDED

| framing | figure | what it answers |
|---|---|---|
| **NET** (the audit's method) | **69.7%** — the 8 positions' net −$616.15 against the book's net −$883.72 | *"how much of what the book actually lost came from flipped decisions?"* — counts their winners |
| **GROSS** | **37.8%** — their losing legs −$866.20 against the book's gross losses −$2,291.16 | *"how much of the book's total damage did they contribute?"* — ignores their winners |

The audit's **74%** was the NET framing before vpos 25 closed. **Both are in OPEN-ITEMS with what
each answers, so neither can later be quoted as the other.**

---

# §4 — RECORDED, NOT ACTED ON

## 4.1 🔶 The macro split — a candidate, not a defect

Verified: **`MACRO_GATE_DRYRUN = False`** (`config.py:221`), so on the row checked the
`macro_gate_penalty = 1.0` for a `CRITICAL_NEGATIVE` category **was applied at the score gate**.

**The machinery acted on it; the advisor never saw it.** That is a **coherent split** — the gate
owns macro, the advisor owns the rest — and it is explicitly **not** Titan's defect, where the
adjustment reached nothing at all. Here it reached the score.

The consequence, stated so it is decided rather than inherited: **the advisor can approve an entry
the macro filter judged critically negative, without knowing that judgement was made.** The gate's
penalty may be sufficient on its own; what is certain is that the advisor reasons without a fact
the system already holds and already acted upon.

**Recorded as a candidate for the post-window decision. Not acted on.**

## 4.2 The headline of the withheld list

Now the first line of that section in OPEN-ITEMS:

> **TEN of eleven are simply NEVER RENDERED — no gate, no flag, no condition. Only news is gated.**
> Ten are a **prompt-content** decision for after the window; one is a **sequencing** decision
> already settled as **Option A**.

That distinction is the useful part: it separates "someone must decide what the advisor should
see" from "we already decided when news arrives", and stops the two being re-litigated together.

---

# §5 — CONFIRMATION SET

| check | result |
|---|---|
| `changes() == 32` | ✅ |
| `quick_check` | ✅ ok |
| every row contains the correct V2 block | ✅ 32/32 |
| no row still contains V1 | ✅ 32/32 |
| nothing but `ai_system_prompt` altered | ✅ spot-checked 8446 / 10178 / 14988 — decide, confidence, reason, raw, pnl all unchanged |
| other V1 rows untouched | ✅ 2,765 |
| **window still 4 of 200** | ✅ |
| **entry prompt byte-identical** | ✅ every `_call(system, user)` code line identical to the pre-fix file; `claude_advisor.py` unchanged since the 20:54 provenance edit |
| service / mode | ✅ active; `[VIRTUAL] poller started in pid 1184217` — **PAPER** proven live |
| open positions | ✅ 0 |
| **Titan untouched** | ✅ clean · `HEAD 3316e8a` · active · **no `.py` modified** |

---

# SOL IS DONE FOR THE NIGHT

**PAPER · single manager · entry prompt frozen · window accumulating at 4 of 200.**

What is waiting, and waiting deliberately:

- **the window** — 196 consultations to go, then the prompt-content decisions unfreeze;
- **ten never-rendered fields** — a post-window decision, with a ready list rather than a re-audit;
- **the macro split** — same, recorded precisely as a candidate;
- **the flip's V2 raw** — permanently unrecoverable for the historical 32, fixed going forward.

Nothing is left half-applied and nothing is left unrecorded.
