# TITAN — THE CASCADE STOPS MISDESCRIBING ITSELF. ZERO DECISIONS CHANGED, PROVEN ROW BY ROW.

**2026-08-05 22:50 UTC · 🔴 APPLIED FROM FLAT · HEAD `2ed2cef` → `22a085e` · restarted 22:48:36 UTC**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
**0 open positions and 0 `exit_pending`** at application, re-checked before the restart.
**Mercury-SOL never opened.**

Parent: `2026-08-05-2235-titan-cascade-audited-from-the-inside.md`.

**Items 1 and 2 applied — labels and documentation only. Items 3 and 4 recorded in the canon with a
pre-registered trigger, not acted on.** `config.py` is **comment-only**.

---

## 🔴 THE PROOF THAT MATTERS FIRST: NO DECISION CHANGED

The old and new `htf_alignment` were **replayed over all 11,129 stored `matrix_breakdown_json`
blobs** — every block the cascade has ever made:

| | |
|---|---|
| rows where `aligned` differs | 🔴 **0** |
| rows where any tier **direction** differs | 🔴 **0** |
| rows where **only the reason string** differs | **6,709** — 6,147 now say ABSENT, 562 say CANCELLED |
| rows whose reason is **byte-identical** | 4,420 (the `X != proposed Y` cases, untouched) |

**Same blocks, same counts, same tier readings. Only the strings differ** — asserted nowhere, replayed
everywhere.

⚠️ **And §1c was checked BEFORE the string was touched, because it gates whether it may be:** the
reason is **not persisted** — 0 of 11,129 `htf_blocked` rows store it in `trades.ai_reason`, 0 in
`skip_attribution` — and nothing parses it. Its only consumers are a journal `print`, the Telegram
card (`<i>was: …</i>`) and the HTTP response body. The optimizer never reads it.

---

## 1. ✅ THE REASON STRING NO LONGER ASSERTS ABSENCE WHERE SIGNALS FOUGHT

The gate emitted `'15m NEUTRAL (no active MOMENTUM signal)'` — a claim of **absence**. Over 11,129
stored breakdowns, `NEUTRAL` is two different market states:

| tier | NEUTRAL | **ABSENT** (`signal_count=0`) | 🔴 **CANCELLED** (signals fought) |
|---|---|---|---|
| 1H | 6,563 | 93.7 % | 6.3 % |
| 🔴 **15m** | 5,966 | 25.4 % | 🔴 **74.6 %** |
| 🔴 **5m** | 2,917 | 0.0 % | 🔴 **100.0 %** |

**False three times in four on the 15m tier, and every single time on the 5m.** The distinction was
already in the same dict the function reads — `signal_count`, `long_points`, `short_points` — and the
gate simply never consulted it when writing its own reason.

```
OLD: 15m NEUTRAL (no active MOMENTUM signal)
NEW: 15m NEUTRAL (this category's own signals disagree — LONG 1.75 / SHORT 1.75
     across 2 signals — so it nets NEUTRAL)

OLD: 1H NEUTRAL (no active TREND signal)
NEW: 1H NEUTRAL (no signal in this category)
```

**Worded to match `signal_tiers._not_counted_phrase`** so the gate's reason and the advisor's tier
block speak one dialect. **This is the 2026-08-03 defect class — fixed then in the PROMPT, still live
in the GATE until now.**

### (b) 🔴 SHOULD THE GATE DISTINGUISH THEM IN ITS *LOGIC*? — I AGREE WITH YOU, AND HERE IS WHY

**No, not in this pass — and my reasoning is not deference.** "Signals arrived and cancelled each
other" and "no signal exists" genuinely are different market states, and you are right that the gate
treats them as one. But acting on that would change **what the cascade blocks**, and:

1. **The two states are not symmetric in a way I can yet argue.** A cancelled 15m means the market
   produced conflicting evidence — arguably *worse* than silence, not better. Which way a rule should
   cut is exactly what the data has not been asked.
2. **Variant-B currently blocks both identically and does 35.4 % of all blocking.** Splitting them
   would re-open the largest single clause in the gate on a prior, not a measurement.
3. **The measurement is now possible for the first time.** With the reason string distinguishing them,
   the `htf_blocked` population becomes cuttable by cancelled-versus-absent from here on — which is
   the precondition for asking the question properly.

**So: a strategy question, deliberately left open, and now instrumented.** If you want it measured, the
cut exists in `matrix_breakdown_json` retroactively for all 11,129 rows.

---

## 2. ✅ THE DOCSTRINGS NOW DESCRIBE THE GATE THAT EXISTS

**(a) It is a two-tier gate.** The docstring promised *"TREND, MOMENTUM and EXECUTION must all
agree"*. The 5m tier **net-opposed 0 times in 11,129 rows**, and **11,129 of 11,129** carry EXECUTION
points **on** the proposed side — because the 5m trigger that fires the webhook *is* an
EXECUTION-category signal in that direction. It can agree or cancel to NEUTRAL; it cannot oppose.

🔴 **The clauses are KEPT, not deleted** — they are correct if the trigger ever stops contributing —
with an explicit note **not to re-add the "all three must agree" claim on the strength of the code
being there.** That note is the point: the next reader's evidence for the old description would have
been the clauses themselves.

**(b) The "NEUTRAL is disagreement" promise is reversed by the only caller.** The docstring said
*"sparse context means no permission to trade"*; `HTF_TOLERATE_NEUTRAL = True` tolerates it. The
docstring now states what `aligned` actually means — *"1H and 15m both actively agree"* — and that
`aligned=False` is **not a veto** but the caller's cue to choose between opposition (block) and
silence (tolerate, subject to the 1H-NEUTRAL sub-rule).

**(c) Variant-B is described by what it does.** Named for 15m *agreement*, it has never adjudicated a
disagreeing 15m: **all 1,495 blocks in 30 days had 15m = NEUTRAL**, because an opposing 15m is always
caught first by the earlier opposing-tier path. The config comment now reads *"refuse when BOTH higher
tiers are silent"* and records that it is **35.4 % of all cascade blocking**.
🔴 **The flag names are unchanged** — `main.py` imports both by name and a rename buys nothing.

---

## ⚠️ A CORRECTION TO MY OWN 22:35 REPORT

It reported clauses **C, E and F as "never taken"**, on a **30-day** window. All-time is more precise
and one of the three is different:

| clause | all time | last 30 d | first … last |
|---|---|---|---|
| A. 1H NEUTRAL | 6,563 | 2,476 | 2026-05-16 … 08-05 |
| B. 1H opposes | 3,600 | 1,422 | 2026-05-15 … 08-05 |
| 🔴 **C. 15m NEUTRAL** | **146** | **0** | **2026-05-15 … 2026-05-20 only** |
| D. 15m opposes | 820 | 328 | 2026-05-15 … 08-05 |
| **E. 5m NEUTRAL** | 🔴 **0** | 0 | **never, in the bot's entire history** |
| **F. 5m opposes** | 🔴 **0** | 0 | **never** |

**C is not unreachable in principle — it fired 146 times in a five-day window in May and stopped when
the tolerate path shipped.** E and F have never fired at all. Saying "never taken" of C was true of
the window I measured and wrong as a general claim.

---

## 3. 📋 RECORDED, NOT ACTED ON — §2.60 IN THE CANON

The tolerate-NEUTRAL route, with the trigger fixed in advance:

| | 1H AGREES | 1H NEUTRAL |
|---|---|---|
| n · win · sum R | **40** · 52.5 % · **+3.755R** | **8** · **12.5 %** · **−5.708R** |
| LONG | −4.664R (mean −0.245) | −1.233R (mean **−0.411**) |
| SHORT | **+8.419R** (mean +0.401) | **−4.475R** · 🔴 **win 0.0 %** |
| paper / live-sized | +4.110R / −0.355R | **−3.999R / −1.709R** |

**Δ +0.807R, perm-p 0.0189 — NOMINAL against 0.000926.** Negative on **both sides and both size
cohorts** — the first predicate in this book to be negative on every cut at once.

**Why it is not acted on, in the canon verbatim:** n=8 · all pre-17:01:29 · 6 of 8 paper at ~68×
notional · **Variant-B already refuses 1,495/30 d of this population, so the residual is only the
narrow 1H-NEUTRAL-with-15m-AGREEING case** · the claim is mechanical and narrow — *"a 15m agreement
does not substitute for a 1H agreement"* — not general discipline, so it needs evidence rather than a
prior.

🔴 **THE TRIGGER:** at **8 further 1H-NEUTRAL admissions on the current geometry**, re-measure. Still
negative on both sides → **close the tolerate path by requiring 1H to AGREE**. Not negative → **record
the reversal as a dead branch.**
**Cost if closed today: 8 of 48 entries = 17 % of the book** ≈ one entry every twelve days foregone.

## 4. 📋 RECORDED — §2.59, AND CLOSING IT IS NOT A LABEL FIX

| tier | matrix (**gate**) | slot (**prompt**) | window |
|---|---|---|---|
| 15m | 90 min | 240 min | 🔴 **90 → 240 min** |
| 1H | 360 min | never expires | 🔴 **unbounded** |
| 5m | 5 min | consumed each fire | ✅ by design |

✅ The 2026-08-03 fix **surfaces** it honestly — old false label **70×, all pre-fix**; new reasons
**11× (9 intra-conflict, 2 genuine expiry)**, and those 2 name the split to the model explicitly.

🔴 **The root stays open because closing it means PICKING a registry**, and either direction changes
behaviour: the slot expiring on the matrix TTL changes `combo_key`, tier ages and the advisor's
"last set Nm ago"; the matrix adopting the slot TTL changes **what the cascade blocks**. **A
cascade-STATE change needs its own pass and its own pre-registration.**

---

## VERIFICATION LEDGER

| check | result |
|---|---|
| `ast.parse` + `py_compile` (`signal_matrix`, `config`, `main`) | ✅ |
| 🔴 gate decisions across all 11,129 rows | ✅ **`aligned` 0 diffs · tier directions 0 diffs** |
| reason strings changed | 6,709 (6,147 ABSENT / 562 CANCELLED); 4,420 identical |
| nothing persists or parses the reason | ✅ 0 rows store it; consumers are a print, a card, an HTTP body |
| `config.py` | ✅ **comment-only** — 0 non-comment changes |
| flag names unchanged | ✅ `HTF_NEUTRAL_REQUIRE_15M_AGREE` / `_DRYRUN` untouched |
| both prompts | ✅ untouched (this pass changed the GATE's reason, not `_ENTRY_SYSTEM` / `_CLOSE_SYSTEM*`) |
| gates / geometry / score bars / risk thresholds | ✅ untouched |
| restart | active **22:48:36 UTC**, boot reconciliation agrees (0 exchange, 0 open rows) |
| 🔴 `openitems_guard` after the commit | **caught the stale HEAD (`2ed2cef` → `22a085e`) and refused** → canon refreshed → **re-run exit 0** |
| snapshot | `2026-08-05-2250-open-items.md`, generated **from** the canon **after** a passing guard, body **byte-identical** |

**Snapshot of code:** `/root/backups/cascade-labels-20260805-2245/` (all 38 `.py`).
**Revert:** `git revert 22a085e`.

---

## ⏳ THE OPEN ITEM, SEVENTH REPORT

**Still no stored prompt with per-wall percentiles.** Last consultation of any kind **16:40:10 UTC**;
0 `htf_blocked` rows since the 22:48 restart either — the bot has had no signal traffic to gate.
Per §0.0 this is confluence not firing, **not a fault**, and the queries that distinguish the two are
in the canon.

---

## LIVE STATE

| | |
|---|---|
| HEAD / `git status` | **`22a085e`** / **clean** |
| canon asserts HEAD | **`22a085e`** — machine-checked, guard exit 0 |
| open positions | **0** |
| service | active since **22:48:36 UTC**, 🔴 LIVE REAL MONEY $30 × 5 |
