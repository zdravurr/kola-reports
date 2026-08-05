# TITAN — THE CASCADE FROM THE INSIDE: **A THREE-TIER GATE WHOSE THIRD TIER CANNOT VETO, AND A TOLERATE PATH THAT LOST −5.7R**

**2026-08-05 22:35 UTC · READ-ONLY · nothing changed, NOTHING PROPOSED, NO DIFF · HEAD `2ed2cef`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
`git status` clean · `trades.db` read-only, absolute path pinned · **0 open positions** ·
**Mercury-SOL never opened.**

⚠️ **The brief says HEAD `7a4169b`; actual HEAD is `2ed2cef`** — the `openitems_guard` commit landed
after the 21:50 report. No trading code differs between them.

**Cohort: 11,129 `htf_blocked` rows, 100 % of them carrying a stored `matrix_breakdown_json`** — so
every clause below is **replayed from what the gate actually saw**, not inferred. 4,226 in the last
30 days.

🔴 **BONFERRONI:** the book is past cell ≈338; this pass spends ~44 more (≈382). At the standing budget
α = 0.05/54 = **0.000926**. **The one statistical result below is p = 0.0189 — NOMINAL, and labelled so
wherever it appears.** Everything else here is a census, not a test.

---

## ANSWER IN ONE LINE

**The cascade is NOT clean, and the two largest findings are structural rather than statistical.**

1. 🔴 **IT IS A TWO-TIER GATE WITH A THREE-TIER NAME.** The 5m EXECUTION tier **net-opposed the
   trigger 0 times in 11,129 rows** — it cannot, because the trigger contributes points on its own
   side (verified: 11,129/11,129 rows have execution points FOR the proposed direction). **Clauses E
   and F of `htf_alignment` are unreachable as block reasons**, and its docstring's *"TREND, MOMENTUM
   and EXECUTION must all agree"* describes a gate that does not exist.
2. 🔴 **THE TOLERATE-NEUTRAL PATH IS THE WORST-PERFORMING ADMISSION ROUTE IN THE BOOK.** Under §0
   filters, entries admitted with the 1H tier **NEUTRAL** returned **−5.708R over 8** (win **12.5 %**)
   against **+3.755R over 40** (win 52.5 %) for genuine agreement — **Δ +0.807R, perm-p 0.0189
   (NOMINAL)**, and it holds on **both sides and in both size cohorts**.
3. 🔴 **`htf_alignment`'s docstring is contradicted by its only caller.** It says *"NEUTRAL on any tier
   is treated as disagreement — sparse context means no permission to trade."* The caller reverses
   that with `HTF_TOLERATE_NEUTRAL = True`.
4. 🔴 **THE TWO TTL REGISTRIES STILL DISAGREE — the exact pair the brief named.** 15m slot **4 h** vs
   matrix MOMENTUM **90 min**; and worse, the 1H slot **never expires** vs matrix TREND **6 h**.
5. 🔴 **`NEUTRAL` conflates two different states and the reason string names the wrong one.** 15m
   NEUTRAL is **74.6 % signals-in-conflict**, not absence — yet the gate prints *"15m NEUTRAL (no
   active MOMENTUM signal)"*.

**And one thing came back clean:** the cascade and `market_regime` **do not disagree** — 0 conflicts on
the 67 rows where both exist.

---

## §1 — EVERY CLAUSE, AND HOW OFTEN IT FIRES (last 30 days, n = 4,226)

`signal_matrix.htf_alignment` is an ordered if/elif chain. Replayed from stored breakdowns:

| clause | fires | share |
|---|---|---|
| **A.** `1H NEUTRAL (no active TREND signal)` | **2,476** | **58.6 %** |
| **B.** `1H {dir} != proposed` | **1,422** | 33.6 % |
| **C.** `15m NEUTRAL (no active MOMENTUM signal)` | 🔴 **0** | 0.0 % |
| **D.** `15m {dir} != proposed` | 328 | 7.8 % |
| **E.** `5m NEUTRAL (no active EXECUTION signal)` | 🔴 **0** | 0.0 % |
| **F.** `5m {dir} != proposed` | 🔴 **0** | 0.0 % |
| **G.** aligned | 0 | — (correct: aligned rows are not blocked) |

### 🔴 WHY THREE CLAUSES NEVER FIRE — AND ONLY ONE OF THE THREE REASONS IS BENIGN

**C and E are benign-but-dead.** Both are reached only when every earlier tier *agrees*, which means
no tier opposes — and the caller's tolerate path returns before any block row is written. So they are
**real conditions that can never be a block REASON.** Not a defect; worth knowing.

🔴 **F IS DIFFERENT: IT IS IMPOSSIBLE, AND THAT MAKES THE THIRD TIER DECORATIVE.**

| the 5m EXECUTION tier, over 11,129 rows | |
|---|---|
| net-opposes the proposed direction | 🔴 **0** |
| rows with execution points **FOR** the proposed direction | 🔴 **11,129 / 11,129 = 100 %** |
| agrees (last 30 d) | 3,026 = 71.6 % |
| NEUTRAL (last 30 d) | 1,200 = 28.4 % |
| **opposes (last 30 d)** | 🔴 **0 = 0.0 %** |

**The 5m trigger that fires the webhook is itself an EXECUTION-category signal in the proposed
direction.** It therefore always contributes points on its own side, so the tier can be *agreeing* or
*cancelled to NEUTRAL* — **never net-opposite.** The gate's own inline comment knows this
(*"the 5m side is established by the trigger itself"*), but `htf_alignment`'s docstring still promises
a three-tier hierarchy and still carries two clauses for a tier that cannot veto.

**Effective structure: 1H and 15m gate; 5m is a pass-through that can only abstain.**

---

## §2a — 🔴 THE TOLERATE PATH, MEASURED: ADMISSION ON ABSENCE COSTS MONEY

**Under §0 filters** (recheck TIGHTEN removed −11, NULL `initial_risk_usdt` removed −1 → **n = 48**),
1H state read from the same stored breakdown the gate used:

| era | 1H state | n | win % | sum R | mean R |
|---|---|---|---|---|---|
| **pre-boundary** | **1H AGREES** | **40** | **52.5 %** | **+3.755** | +0.094 |
| **pre-boundary** | 🔴 **1H NEUTRAL** | **8** | 🔴 **12.5 %** | 🔴 **−5.708** | 🔴 **−0.714** |
| **POST-boundary** | — | 🔴 **0** | — | — | — |

**Δ (AGREES − NEUTRAL) = +0.807R · perm-p 0.0189, 20 k two-sided — NOMINAL, does not clear 0.000926.**

**It holds where the book's results usually stop holding:**

| cut | 1H AGREES | 1H NEUTRAL |
|---|---|---|
| **LONG** | n=19 · −4.664R · mean −0.245 | n=3 · −1.233R · mean **−0.411** |
| **SHORT** | n=21 · **+8.419R** · mean +0.401 | n=5 · **−4.475R** · win **0.0 %** · mean **−0.895** |
| **paper** (1R ≥ $10) | n=33 · +4.110R | n=6 · **−3.999R** |
| 🔴 **live-sized** (1R < $10) | n=7 · −0.355R | n=2 · **−1.709R** · mean −0.854 |

**Both sides negative. Both size cohorts negative. Zero wins on the SHORT side.** This is the first
predicate in this book to be negative on every cut simultaneously — and it is not a predictor someone
proposed, it is **a route the gate already takes.**

⚠️ **THE LIMITS, STATED BEFORE THE CONCLUSION IS DRAWN.** **n = 8.** p = 0.0189 is nominal against a
budget of 0.000926. **Zero positions exist on the post-17:01:29 geometry**, so every figure describes
a machine that was retired. 6 of the 8 are paper at ~68× the live notional. **This is not a result
that licenses a change; it is the strongest reason yet to look at this route with live rows.**

---

## §2b — VARIANT-B DOES **35 %** OF ALL BLOCKING, AND NOT WHAT ITS NAME SAYS

Every `htf_blocked` row decomposes into exactly two causes:

| who blocked | all time (11,129) | last 30 d (4,226) |
|---|---|---|
| an **opposing tier** | 6,909 = 62.1 % | 2,731 = 64.6 % |
| 🔴 **Variant-B** (1H NEUTRAL + 15m not agreeing) | **4,029 = 36.2 %** | 🔴 **1,495 = 35.4 %** |
| unexplained | 191 (all pre-Variant-B deploy) | **0** |

🔴 **AND ITS 1,495 BLOCKS HAVE 15m = NEUTRAL IN 1,495 OF 1,495:**

| 15m | 5m | n |
|---|---|---|
| NEUTRAL | SHORT | 610 |
| NEUTRAL | NEUTRAL | 446 |
| NEUTRAL | LONG | 439 |
| **any non-NEUTRAL 15m** | — | 🔴 **0** |

**The rule is named "1H NEUTRAL requires 15m AGREEMENT", and its condition is `mom_dir != direction` —
which includes NEUTRAL.** In practice the *opposing* case is always caught first by the opposing-tier
path, so **Variant-B never once adjudicated a disagreeing 15m. Its entire measured effect is refusing
entries where BOTH higher tiers are silent.** That is a defensible rule — it is simply not the rule the
name describes, and it is a third of all blocking.

**What it adds over the base rule:** without it, all 1,495 would have been *tolerated* and passed to
the score gate. Given §2a — 1H-NEUTRAL admissions run −0.714R — **Variant-B is plausibly the most
valuable clause in the cascade, and it is the one whose name least matches its behaviour.**

---

## §2c — ✅ THE CASCADE AND `market_regime` DO **NOT** DISAGREE

| 1H TREND tier | `market_regime` | n |
|---|---|---|
| SHORT | TREND | 26 |
| LONG | TREND | 20 |
| NEUTRAL | *None* | 8 |
| SHORT | *None* | 6 |
| NEUTRAL | FLAT | 4 |
| LONG | *None* | 3 |

🔴 **Rows where the cascade saw no 1H signal while `market_regime` read TREND: 0.** Where the 1H tier
is NEUTRAL, the regime is `None` or `FLAT` — **never TREND.** The hypothesis in the brief is **not
confirmed**, and that is worth as much as a finding.

⚠️ **BUT THE QUESTION CANNOT BE ASKED WHERE IT MATTERS MOST.** `market_regime` is **NULL on 11,129 of
11,129 refused rows (100 %)** — §0's recorded trap, still present. The clean bill above rests on **67
executed rows**, of which 17 also have a NULL regime. **The cascade and the regime agree on every row
where both are recorded; on 99.4 % of the cascade's decisions, only one of the two is recorded at all.**

---

## §3 — 🔴 THE TTLs: THE TWO REGISTRIES STILL DISAGREE

| tier | matrix `CATEGORY_TTL_MINUTES` — **what the CASCADE reads** | `state_machine.market_state` slot — **what the PROMPT reads** | verdict |
|---|---|---|---|
| **1H** TREND | **360 min** (6 h) | `1h_context.ttl_hours = None` — *"Persistent — no expiry"* | 🔴 **DISAGREE — the slot never expires** |
| **15m** MOMENTUM | **90 min** (cut 240→90 on 2026-05-20) | `15m_confirm.ttl_hours = 4` = **240 min** | 🔴 **DISAGREE — 240 vs 90, the exact pair the brief named** |
| **5m** EXECUTION | 5 min | `5m_trigger.ttl_hours = None` — *consumed each fire* | ✅ consistent by design |

**Answer to the brief: yes, still true, and unchanged.** Between **90 and 240 minutes** after a 15m
signal, the state machine holds it live while the matrix has expired it — and **the cascade reads the
matrix.** On the 1H tier the window is unbounded.

### ✅ AND THE 2026-08-03 FIX FOR THIS IS WORKING — MEASURED

The disagreement is now *surfaced* rather than mislabelled. Across all stored prompts:

| rendering | n |
|---|---|
| 🔴 the OLD single false label `"NOT counted by the gate — matrix TTL expired)"` | **70** (all pre-fix) |
| **NEW** `"…this category's own signals disagree (LONG x / SHORT y across n signals)"` | **9** |
| **NEW** `"…the matrix expired this signal on its category TTL (MOMENTUM TTL 90 min); the state-machine slot still holds it"` | **2** |

**Post-fix, 9 of 11 are intra-conflict and 2 are genuine TTL expiry** — the same 4:1 direction the fix's
own docstring measured (77 renders, wrong on 70). **The two TTL-expiry renders name the registry split
explicitly to the model.** The label is honest now; **the underlying 240-vs-90 split was never closed.**

---

## §4 — 🔴 THE ARITHMETIC: `NEUTRAL` IS TWO STATES, AND THE REASON STRING NAMES THE WRONG ONE

Nothing is double-counted or dropped — `apply_htf_penalty` copies rather than mutates, and the penalty
is applied once. **The defect is in what `NEUTRAL` means.**

| tier | NEUTRAL instances | **ABSENT** (`signal_count = 0`) | 🔴 **CANCELLED** (signals arrived and fought) |
|---|---|---|---|
| 1H TREND | 6,563 | 6,147 = 93.7 % | 416 = 6.3 % |
| 🔴 **15m MOMENTUM** | 5,966 | 1,517 = 25.4 % | 🔴 **4,449 = 74.6 %** |
| 🔴 **5m EXECUTION** | 2,917 | 0 = 0.0 % | 🔴 **2,917 = 100 %** |

**`htf_alignment` reads only `net_direction`, so both states arrive as the same `NEUTRAL`** — the
distinction survives only in `signal_count` / `intra_conflict`, which the gate never consults. Variant-B
blocks both identically.

🔴 **AND THE PRINTED REASON ASSERTS THE WRONG ONE.** The gate emits
**`'15m NEUTRAL (no active MOMENTUM signal)'`** — a claim of **absence** — while **74.6 % of 15m
NEUTRALs are signals in conflict**, live and inside their TTL. On the 5m tier the same sentence would be
wrong **100 %** of the time. **This is the 2026-08-03 defect class (four states collapsed into one
label), fixed in the PROMPT and still live in the GATE's own reason string.** The four states the brief
named are, as stored: agreeing · opposing · absent · cancelled — and the gate distinguishes **three**,
merging the last two.

---

## §5 — VERDICT, RANKED BY HOW OFTEN THE CLAUSE RUNS

| # | finding | runs | severity |
|---|---|---|---|
| **1** | 🔴 **`NEUTRAL` conflates absent and cancelled; the reason string claims absence and is wrong on 74.6 % of 15m NEUTRALs** | **every block** — 4,226/30 d | 🔴 **HIGH.** Reason text used by humans and by the optimizer; the gate cannot see the distinction at all |
| **2** | 🔴 **Variant-B is 35.4 % of all blocking and never adjudicates a disagreeing 15m** — it is a both-tiers-silent blocker under an agreement name | **1,495/30 d** | 🔴 **HIGH by volume.** Probably the most valuable clause; least accurately named |
| **3** | 🔴 **The 15m TTL registries disagree (240 vs 90 min); the 1H slot never expires vs 6 h** | **every entry** | 🔴 **HIGH.** Prompt and gate can disagree about whether a tier exists; honestly labelled since 08-03, root never closed |
| **4** | 🔴 **The 5m tier cannot veto — 0 of 11,129; clauses E/F unreachable; docstring promises three tiers** | **every entry** | **MEDIUM.** Costs nothing today, but the gate's stated contract is wrong and a future author would trust it |
| **5** | 🔴 **`htf_alignment`'s docstring says NEUTRAL blocks; its only caller tolerates it** | **every entry** | **MEDIUM.** Read the helper alone and you get the opposite policy |
| **6** | 🔴 **The tolerate-NEUTRAL admission route ran −5.708R over 8 (win 12.5 %) vs +3.755R over 40** | **the admission side** | **MEASURED, NOMINAL (p 0.0189).** n=8, all pre-boundary, 6 of 8 paper — the strongest reason to watch this route, not to change it |
| **7** | ✅ cascade vs `market_regime` | 67 rows | **CLEAN** — 0 disagreements, with a 100 %-NULL blind spot on refused rows |

## 🔴 IS THE CASCADE CLEAN? **NO — BUT IT FAILS DIFFERENTLY FROM EVERYTHING ELSE TONIGHT**

The twelve defects found earlier were mechanisms that **did not run** or **claims that were false**.
The cascade **runs, and refuses correctly by every outcome measure available** — §2.54 found no pocket
of positive drift among its refusals, and §2a here finds its *tolerated* admissions are the losing
ones. **What is wrong is everything it SAYS about itself:** a third tier that cannot veto, a docstring
reversed by its caller, a sub-rule named for a case it never handles, a reason string asserting absence
where there was conflict, and two registries that still disagree about when a signal expires.

**A mechanism can be right and still be undocumentable — and this one is the largest in the bot at
72 % of all refusals.** Nothing here suggests relaxing it. §2a suggests the opposite, at n=8.

⚠️ **NOT AUDITED, still open from the 19:55 scope note:** geometry arithmetic, `order_adapter`'s
live-order semantics, the optimizer. **Nothing proposed. No diff.**

---

## LIVE STATE

| | |
|---|---|
| HEAD / `git status` | **`2ed2cef`** / **clean** |
| open positions | **0** |
| `htf_blocked` last 30 d | **4,226** (72 % of all refusals) |
| ⏳ stored prompt with per-wall percentiles | **still none** — last consultation 16:40:10 UTC; per §0.0 this is confluence not firing, not a fault |
| `mfe_tracking` rows | **0** — awaiting the first close |
