# titan combo weight now carries its provenance, freeze checked, thresholds and regrade coupled

_2026-08-03 14:15 UTC_

---

# TITAN — THE COMBO WEIGHT NOW TRAVELS WITH WHAT IT IS BASED ON · APPLIED, LIVE, `a85733f`

_2026-08-03 14:15 UTC · HEAD `a85733f` (was `ca90c2f`) · LIVE, real money, flat · three files, +204/−4_

---

## DECISION LINE

**Applied and running.** The entry prompt no longer tells the model that a one-trade paper judgement
is established history. **The number is kept exactly as it is** — no suppression, no minimum-n rule,
no staleness cut-off. What changed is that it now arrives with the three facts needed to weigh it.

Was:

```
Combo weight: 0.90 (1.0 baseline; <1 = historical loser, >1 = winner)
```

Now:

```
Combo weight: 0.90  (1.00 = untouched; -0.10 per evaluation that lost more than $15,
  +0.10 per one that gained more than $20)
  Based on: 1 evaluation, most recent 2026-06-03, taken at ~67x the current position size.
```

**Freeze check passed and argued, not assumed:** §2.4-OP freezes *"everything the advisor READS"* on
the **close** prompt and states in the same bullet that **the entire entry side is NOT frozen**. The
combo weight appears **exactly once** in `claude_advisor.py` — inside `consult_for_entry` — and
neither `_build_exit_context` nor the close template touches `signal_weights`. **No diff line in this
change touches any close-side symbol.** The window is not voided and does not need restating.

**Nothing else changed.** `get_weight` is byte-identical (**0** diff lines in its body), the gate is
`direction_score + macro_gate_adj` with no weight term, and sizing is `FIXED_NOTIONAL_MODE` with
`scaled_step_margin` still having no callers.

**Recorded, not fixed:** the ±20/−15 thresholds — and **§2.40f now records why they and §2.41 are one
decision with two levers**, not two decisions in sequence.

---

## 1. FREEZE CHECK — ARGUED

§2.4-OP, verbatim, the bullet the operator marked *"SETTLED, do not re-open the definition"*:

> **Freeze scope — ✅ EXPLICITLY CONFIRMED BY THE OPERATOR 2026-07-30 14:0x, SETTLED:** frozen =
> **everything the advisor READS**. **NOT** frozen = act/hold plumbing, logging, labels, close
> mechanics, and **the entire entry side**.

And the enumerating bullet immediately above it lists only close-prompt inputs: *"`_build_exit_context`,
`claude_advisor`'s close template, the book block, the regime block, the tier block, the trail block,
or any figure rendered into the close prompt."*

**Traced rather than trusted:**

| check | result |
|---|---|
| where does the combo weight appear in `claude_advisor.py`? | **exactly one site**, line 342, inside `consult_for_entry` |
| does `_build_exit_context` (`main.py:2493-2740`) read `signal_weights`? | **no** — grep over the whole function range returns nothing |
| does the close template read a weight? | **no** — `consult_for_close_rich` / `_CLOSE_SYSTEM` contain no weight term |
| does this change's diff touch any close-side symbol? | **no** — `git diff \| grep -E "consult_for_close\|_CLOSE_SYSTEM\|close_rich\|_build_exit_context"` is empty |
| precedent | §2.37a and §2.38 are both recorded as *"entry-side change, so §2.4-OP does not forbid it mid-window"* |

⚠️ **One second-order effect, stated rather than hidden.** Future *entry* `ai_reason` text may read
differently, and the exit prompt renders `Advisor's reason at entry: <ai_reason>`. That is the **same
field reading the same column** — not a change to a close-prompt input — and it is the property
**every** entry-side change has, including the two already accepted mid-window. It is noted here so
it is on the record rather than discovered later.

**Conclusion: the entry prompt is not inside any freeze. Proceeding was correct.**

---

## 2. WHAT IS RENDERED, AND WHY IT IS FACTS

Three facts, and the third is the one that matters:

| fact | source | why |
|---|---|---|
| **evaluation count** | `signal_weights.evaluations` — the counter the weight was actually built from | 5 of the 7 non-baseline combos rest on **one** |
| **date of the most recent** | `MAX(audit_at)` over the audited trades carrying that combo | the newest non-baseline judgement is **2026-07-20**; the oldest **2026-05-26** |
| 🔴 **the position SIZE they were taken at** | `AVG/MIN/MAX(price × amount)` of those trades ÷ `order_adapter.active_fixed_margin() × LEVERAGE` | this is what the model had no way to know: the judgement was formed at **~67×** the size it is now being applied to |

**The size ratio is derived per combo from real trade rows, not hard-coded at 68.** A combo whose
evaluations are live-era renders `~0.97x` — comparable — and says so. That is the point: the line
distinguishes a well-founded weight from a paper relic, and it does it with data rather than a rule.

### The mechanism sentence replaced the verdict sentence

`(1.00 = untouched; -0.10 per evaluation that lost more than $15, +0.10 per one that gained more
than $20)` states **what moves the number**. The direction information the old line carried is
preserved; the character judgement (*"historical loser"*) is gone. It also, incidentally, lets the
model see the thresholds — which is a fact about the mechanism, not a hint about the combo.

### All four shapes, rendered on real data

```
── NEVER EVALUATED (the COMMON case — no store row at all)
   Combo weight: 1.00  (1.00 = untouched; -0.10 per evaluation that lost more than $15, +0.10 per one that gained more than $20)
     Based on: no evaluations yet — this is the untouched baseline.

── ONE PAPER EVALUATION (the case that motivated this)
   Combo weight: 0.90  (…)
     Based on: 1 evaluation, most recent 2026-06-03, taken at ~67x the current position size.

── LIVE-ERA EVALUATIONS (comparable size — and it says so)
   Combo weight: 1.00  (…)
     Based on: 3 evaluations, most recent 2026-08-03, taken at ~0.97x the current position size.

── MIXED ERAS (an honest range, not a mean that hides the mix)
   Combo weight: 0.90  (…)
     Based on: 2 evaluations, most recent 2026-08-03, taken at ~0.99x-67x the current position size (mixed sizes).

── REAL LOOKUP FAILURE (the ONLY thing that renders this)
   Combo weight: 0.90  (…)
     Based on: not available for this combo.
```

**One correction I made to my own first cut, because it mattered on the common path.** The first
version returned `None` when a combo had no `signal_weights` row, which rendered *"not available"*.
But a missing row **is the common case and it is a fact, not a failure** — the row is only created by
the first `record_outcome`, so any combo that has never been audited has none, and it carries the
untouched baseline. It now renders *"no evaluations yet — this is the untouched baseline."* `None`
is reserved for a genuine exception, and the exception path was tested by pointing `DB_PATH` at a
nonexistent file: it returns `None`, never a wrong number.

### Kept out, deliberately

**No minimum-n rule. No staleness cut-off. No suppression. No re-weighting.** Deciding for the model
that a 1-evaluation weight should be ignored would be the same mistake in the other direction —
substituting our judgement for the facts. This is the same line already drawn on the book block
(*"CALIBRATION ONLY … no win rate, no PnL, no historical performance is attached to any book
figure"*) and on the 1H tier identity in `f0a8d30`.

---

## 3. THE CODE

Three files, **+204 / −4**. Shape mirrors `_entry_book_pct`: **`main.py` assembles, `claude_advisor`
renders** — the established pattern here, not a second one invented.

| file | change |
|---|---|
| `signal_weights.py` | **new** `get_weight_provenance(combo_key)` — read-only accessor, never raises. `get_weight` **untouched** |
| `main.py` | **new** `_combo_weight_provenance(combo)` — adds the size ratio, because `order_adapter` owns the answer to *"what size are we trading now"*. Wired into **both** `consult_for_entry` call sites |
| `claude_advisor.py` | **new** `_format_combo_weight(weight, prov)`; `consult_for_entry` gains an optional `weight_provenance=` kwarg; the one-line render replaced by a call |

```diff
-    user += (
-        f"Combo weight: {weight:.2f} (1.0 baseline; <1 = historical loser, >1 = winner)\n"
-    )
+    user += _format_combo_weight(weight, weight_provenance)
```

**The size basis is `order_adapter.active_fixed_margin() × LEVERAGE`, not `FIXED_MARGIN_USDT`** —
that name is the back-compat alias resolving to the **PAPER** size, and using it would have
understated every ratio by ~67× in live. Current basis: **\$150**.

---

## 4. PROOFS BY EXECUTION

| # | proof | result |
|---|---|---|
| 1 | syntax + import, all three files | ✅ |
| 2 | **AST proof that `combo` is bound before the call in both enclosing functions** — the 2026-07-29 NameError class, where a guard inside a function did not protect its own argument list | `_handle_5m_trigger()` def@1848: call@2021, bound@1858 ✅ · `_handle_state_machine()` def@3407: call@3901, bound@3699 ✅ |
| 3 | both call sites patched, and **exactly** two | `assert n == 2` in the patch script; grep confirms lines 2035 and 3915 |
| 4 | all four render shapes on **real** store + trade data | as printed above |
| 5 | exception path | `DB_PATH` → nonexistent file ⇒ returns **`None`**, renders *"not available"*, no wrong number |
| 6 | **end-to-end prompt build with the API stubbed** | `consult_for_entry` returns the stub verdict; the weight block appears in the assembled prompt between the tier block and the ATR line, no request made |
| 7 | `get_weight` byte-identical | **0** diff lines in its body |
| 8 | gate arithmetic | `_gated_score = round(direction_score + _macro_gate_adj, 2)` at three sites — **`weight_used` appears in 0 of them** |
| 9 | sizing | `FIXED_NOTIONAL_MODE`; `scaled_step_margin` — **no callers anywhere** |
| 10 | close path untouched | no diff line matches `consult_for_close` / `_CLOSE_SYSTEM` / `close_rich` / `_build_exit_context` |

**Deployed** `14:12:31 UTC`. All four boot gates green, `0 exchange position(s), 0 open row(s)`, no
orphan stops either side, zero errors. Bot was **flat** for the restart.

---

## 5. RECORDED, NOT FIXED — AND WHY THE TWO DECISIONS ARE ONE

**OPEN-ITEMS §2.40f, new.** Your framing, recorded so no later session can take either lever alone:

| | thresholds **stay** at ±20/−15 | thresholds **re-scaled** to the R-equivalents |
|---|---|---|
| the mechanism | **inert** — no weight can ever move at live size | **live** — weights move again |
| what §2.41's re-grade would write | a **PERMANENT, unrevisable** value, carried into every future entry prompt | a **revisable** value the next few trades correct |
| so §2.41 is | a final judgement from a paper era at 68× notional | an initialisation later evidence overwrites |

**The same re-grade is a different act depending on which threshold decision is in force.** Doing
them in sequence means the first is decided under an assumption the second invalidates.

🔴 **Both remain deferred and are to be decided together.** §2.41 stays deferred. §2.40's thresholds
stay recorded, not fixed. **§2.39b stays as marked** — untouched this pass.

**Note on scope:** §2.40e closes the *influence channel*. **§2.40 itself is not closed** — the
mechanism is still inert, and this change does not make it less so. It makes the inertness visible to
the reader of the prompt instead of invisible.

---

## WHAT CHANGED, AND WHAT DID NOT

| | |
|---|---|
| **Code** | `signal_weights.py`, `main.py`, `claude_advisor.py` — **+204 / −4**, commit `a85733f` |
| **The weight number itself** | **unchanged.** Not suppressed, not re-scaled, not gated by an n-rule |
| **`get_weight` / gate / sizing** | **byte-identical.** 0 diff lines in `get_weight`'s body; no weight term in the gate; `scaled_step_margin` still has no callers |
| **The EXIT prompt** | **untouched.** §2.4 window intact, not voided, no restatement needed |
| **DB** | **no writes.** No `UPDATE`, no migration, no new column |
| **§2.41 (the 44-row re-grade)** | **still deferred**, now with §2.40f's coupling recorded |
| **±20/−15 thresholds** | **recorded, not fixed** |
| **§2.39b (`learning_*`)** | **as marked**, untouched |
| **Book sources** | still untouched — the separate, attributable question |
