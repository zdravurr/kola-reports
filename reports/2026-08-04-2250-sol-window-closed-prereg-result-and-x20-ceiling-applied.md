# MERCURY-SOL — THE WINDOW CLOSED, THE PRE-REGISTERED PREDICTION HELD, THE ×20 CEILING IS LIVE

**2026-08-04 22:50 UTC** · subject: **Mercury-SOL** (`/mnt/volume_nyc1_1780480650620/mercury-sol`), **PAPER**, not under version control — every edit below was `.bak`-snapshotted first.
**Titan was not touched and not read for parameters.**

---

## §1 — THE WINDOW

### 1a. It is CLOSED

| | |
|---|---|
| opened | **2026-08-01 17:13:02** UTC (worker restart, pid 1126633) |
| **200th consultation** | **row 15694, 2026-08-04 12:50:05 UTC** |
| elapsed | 2 d 19 h 37 m (~20.4 min/consult) |
| rows now ≥ open | **251** — the 51 past the close are **excluded** from every figure below |

**Orphan set: exactly 1 — row 14981**, 2026-08-01 17:00:01, SHORT, `skip` (conf 0.92), the only
production render the interim 3-of-4 form ever produced. Re-queried against the definitive interval
`(16:18:13, 17:13:02)`: **it is the only row there.** The pre-registration's count of 1 is confirmed,
not assumed. It is **OUT** of the 200 and out of every pooled statistic.

*(Incidentally: 14981's own reason — "15m HyperWave LONG opposes SHORT entry" — is **correct** usage,
not wrong-side. The interim form's single render did not misread the side.)*

### 1b. 🔴 THE PRE-REGISTERED RESULT

**First, the method was proven identical, not merely described as identical.** Re-running the matcher
over the baseline population reproduces the pre-registration **exactly**:

| population | pre-registered | my re-measurement | match |
|---|---|---|---|
| book-wide | 3.53 % (104 / 2,944) | **3.53 % (104 / 2,944)** | ✅ |
| visible tiers **disagree** | 9.70 % (103 / 1,062) | **9.70 % (103 / 1,062)** | ✅ |
| visible tiers **agree** | 0.05 % (1 / 1,882) | **0.05 % (1 / 1,882)** | ✅ |

*(The exact baseline cut is `timestamp < 2026-08-01 16:00:01`; the naïve `<= 16:07` cut yields 2,945/1,063 —
one extra disagreeing row, 14973. Same matcher, same definitions.)*

**The same three rates over the window's 200:**

| population | baseline | **window** | change |
|---|---|---|---|
| book-wide | 3.53 % (104/2,944) | **0.00 % (0 / 200)** | **−3.53 pp** |
| tiers **disagree** (15m vs 5m) | 9.70 % (103/1,062) | **0.00 % (0 / 53)** | **−9.70 pp** |
| tiers **agree** | 0.05 % (1/1,882) | **0.00 % (0 / 147)** | −0.05 pp |

**🔴 A parser correction is disclosed here, because it changes nothing in the definition and everything
in the number.** The post-17:13 prompt renders the 15m tier as `(direction: SHORT, set 35m ago)` — the
age was added inside the parens. The original regex anchored on the closing paren, so on the new form
it read every 15m tier as missing and reported **100 % disagreement**. The anchor was removed; the
**definition is untouched** (the direction label the prompt renders for the 15m tier vs the 5m
trigger), and the corrected parser **still reproduces the baseline exactly**, which is what proves the
change is neutral rather than convenient.

**Sanity checks on the zero, because a zero is the easiest number to produce by accident:**

- reasons are present and normal length — 0 empty, mean 127 chars (baseline 142)
- the matcher **still fires on this population**: 80 of 200 window rows contain its phrase family in
  **correct** usage (40.0 %, vs 1,077/2,944 = 36.6 % at baseline). The vocabulary did not shift out
  from under the matcher — the wrong-side matches are genuinely absent.
- exact binomial: at the baseline disagreeing rate, 53 rows predict **5.14** wrong-side.
  **P(0 | p=0.0970, n=53) = 0.0045.**
- conservative dedup (one row per timestamp, see caveats): **0 / 41** disagreeing, **p = 0.015**.

### 1c. 🔴 AGAINST THE PRE-REGISTRATION, VERBATIM

The pre-registration said: *"If the disagreeing-population rate does not fall, the prompt's
self-contradiction was NOT the cause. Record that outcome as-is."*

**The disagreeing rate FELL: 9.70 % → 0.00 %.** This is **not** a null. The clause did not need to be
invoked, no population was re-cut, and nothing was explained away. The pre-registered prediction is
**CONFIRMED** on its own stated terms.

**What this does and does not license:**

- The **disagreeing** arm carries the result: 0/53 where 5.14 were predicted, p=0.0045.
- The **agreeing** arm is **uninformative** and should not be quoted as support — its baseline was
  already 0.05 %, so 0/147 is exactly what the old prompt would also have produced.
- n=53 against a baseline of 1,062. The direction is established at conventional significance; the
  *magnitude* ("zero") is not — the honest reading is "fell sharply", not "eliminated".

### 1d. CAVEATS, ON THEIR FACE

1. **The 1H tier was added mid-setup, and the treatment is a BUNDLE.** Items 1–4 (direction field,
   1H tier, per-tier agreement block, removal of the false alignment sentence) shipped together.
   **Attribution among them is impossible by construction** — an operator decision recorded in
   advance, on the grounds that no one intends to keep one line and revert another.
2. **The aligned-V2 override fired inside the window.** **4 of the 200 verdicts were produced by a
   DIFFERENT system prompt** than the frozen base — 1 × `V2 ALIGNED (LONG SOFT)` (row 15093 = vpos 26)
   and 3 × `V2 ALIGNED SHORT (SOFT)`. These 4 are **exactly the 4 `execute` decisions**; the other 196
   are the frozen base. So 2 % of the measured population was not judged by the prompt under test.
   None are wrong-side, so the headline is unaffected — but the window is 98 % pure, not 100 %.
3. **Duplicate-timestamp rows.** 35 of the 200 share a timestamp with another row (17.5 %), against
   353/2,944 (12.0 %) at baseline — same phenomenon, somewhat denser. Prompts and reasons differ, so
   these are genuine separate consultations, but they are not independent trials. The dedup
   sensitivity above exists for this reason; the result survives it.
4. Decisions in the window: **196 skip, 4 execute.**

---

## §2 — vpos 26

| | |
|---|---|
| status | **CLOSED** |
| closed at | 2026-08-03 06:40:01 UTC |
| exit reason | **`sl`** (stop-out; `max_adverse_price` = `sl_price` = 72.59) |
| net P&L | **−$138.67** (fees $10.92) |
| **R** | **−1.085R** (initial risk $127.746) |
| entry | LONG @ 73.53, 2026-08-02 05:00:19; water mark 74.21 |
| the wall | ask **×20.3 at $73.75, +0.30 %** — confirmed from its own rendered entry prompt (row 15093) |

**REVERSAL CONDITION R1: NOT MET.** R1 required a `mult ≥ 20` flip that **closes profitably**. It
closed on its stop at −1.085R.

**R2 also not met**, and it is worth stating rather than passing over: the window produced **three**
positions (25, 26, 27). vpos 25 and 27 are SHORT — outside the restriction's scope. **vpos 26 is the
only aligned-LONG flip at `mult ≥ 20` the window contained**, and it is the negative observation.
There is no cohort to compare, so the "not worse than sub-×20" test has nothing to evaluate.

**The tail now stands 0 of 3 in the study, 0 of 1 realised.**

---

## §3 — THE OVERRIDE: RESTRICTION **APPLIED**

Per §2, the reversal condition did not fire, so the pre-registered restriction was applied as written.

**`ADVISOR_WALL_ALIGNED_V2_MULT_CEILING = 20.0`** (`config.py`) — the override may not fire when the
overhead wall is at or above ×20. Below ×20, **unchanged**. The SHORT companion is **untouched**.

**One ambiguity the pre-registration's one-line phrasing did not pin down**, resolved and recorded
rather than silently chosen: *which* overhead wall? I implemented the **nearest ask wall above mid** —
the wall V1's veto actually names, and the mechanism rationale 3 describes ("enters beneath a *nearby*
opposing wall"). The alternative reading (**any** overhead ask wall ≥ 20×) was **measured across all
486 stored LONG consults that reach this gate: it blocks the same 29 rows.** The two readings have
**never diverged on this book**, so the choice is empirically moot.

**Verified by executing the real code path** with the model call stubbed (no API spend):

| test | result |
|---|---|
| ×20.3 — vpos 26's exact wall | ✅ V1 skip **STANDS**, and the SOFT prompt is **not called** (no wasted spend) |
| ×20.0 — "at or above" boundary | ✅ blocked |
| ×19.9 — below the ceiling | ✅ flip still happens, SOFT verdict adopted, provenance stamp intact |
| unreadable/empty book | ✅ passes through — the ceiling is not a data-quality veto (book unavailability is 0.099 %) |
| aligned SHORT, bid wall ×27.4 | ✅ unaffected, as pre-registered |

Two deliberate design choices:
- **The `except ImportError` fallback defaults to 20.0 — it fails TOWARD the restriction**, unlike the
  `AI_ADVISOR_HIDE_1H` guard beside it that silently re-hides the 1H. A renamed config must not
  silently re-widen a gate whose tail holds no positive evidence.
- **A suppression is logged** (`[WALL-ALIGNED-V2][CEILING]`). A gate that narrows without leaving a
  trace is the one nobody grades.

🔴 **LIVE, not merely on disk.** Files written 22:42:26 / 22:47:22; `mercury-sol.service` restarted
**22:48:10**, worker pid **2190445** booted 22:48:27 — file mtimes precede the boot, so the running
process holds them. Restarted while **flat** (0 open positions, 0 pending exits; boot log: *"no open
paper positions at boot — clean"*).

**This remains a judgement made under absence of evidence** (n=3 study rows, 4 closed LONG flips) —
not a falsified override. Raising the ceiling is legitimate if that tail ever produces a winner, and
the config comment says so.

---

## §4 — THE TWO STALE COMMENTS: CORRECTED, AND THEY WERE WORSE THAN LABELLED

The freeze is over, so the mtime evidence it rested on is no longer needed — and it is preserved
anyway in `claude_advisor.py.bak_alignedv2_multceiling_20260804` (`cp -p`, Aug 1 20:54 mtime intact).

**Tracing the code instead of copying the label found the comments were wrong about the MODULE, not
just the venue.** They named `microstructure.fetch_pre_trade_walls()` — Bybit depth-100. The advisor's
book is `liquidity_zones.fetch_pre_trade_walls()` — **OKX books-full, 4000 levels per side**, keyless
public REST, since 2026-06-03. `microstructure.fetch_pre_trade_walls` **feeds no caller on any path**;
the only two live references to that name in the tree were these comments.

Also resolved: the prompt renders **"8000 levels"** for a 4000-level request because the dict's
`depth` is `len(bids) + len(asks)`. That looked like a third venue figure; it is one book, counted on
both sides.

**Three sites corrected** — the two named, plus `_format_pre_trade_walls`'s own docstring (line 259),
which carried the identical "depth-100" claim. Leaving it would have re-seeded the defect.

The remaining `Bybit` strings in the file (`_CLOSE_SYSTEM`, ~line 712) are **correct** — that is the
venue the bot trades on, and the fill-time Bybit capture is a recorded, deliberate exception.

---

## §5 — WHAT REMAINS WITHHELD (REPORT ONLY — NOTHING APPLIED)

Re-verified **empirically against the window's own 200 rendered prompts**, not carried forward from
the 16:07 audit:

| # | field | column | collected on the 200 | rendered | withheld by |
|---|---|---|---|---|---|
| 1 | funding rate | `mc_funding_rate` | 200/200 | **0/200** | never rendered |
| 2 | OI delta % | `mc_oi_delta_pct` | 200/200 | **0/200** | never rendered |
| 3 | DXY trend | `dxy_trend` | 200/200 | **0/200** | never rendered |
| 4 | macro news category | `macro_news_category` | 200/200 | **0/200** | never rendered |
| 5 | macro gate penalty | `macro_gate_penalty` | 200/200 | **0/200** | never rendered |
| 6 | confluence score | `confluence_score` | 200/200 | **0/200** | never rendered |
| 7 | HyperWave subtype | `hw_15m_subtype` | 200/200 | **0/200** | never rendered |
| 8 | HyperWave weight | `hw_15m_weight` | 200/200 | **0/200** | never rendered |
| 9 | tape buy ratio | `tape_buy_ratio` | **3**/200 | **0/200** | never rendered |
| 10 | tape aggression | `tape_aggression` | **3**/200 | **0/200** | never rendered |
| 11 | news sentiment | `news_score` | 188/200 | **0/200** | 🔴 **GATE** — `is_in_funding_news_observation()` |

**Ten of eleven are simply never rendered — no gate, no flag, no condition.** Only news is gated.
Correction worth carrying: **the two tape fields are NULL at source on 197 of 200 rows** — they are
withheld *and* largely uncollected, so adding them would buy almost nothing today.

**The news counter is structurally pinned, not merely at 0.** It counts
`status='executed' AND (is_virtual IS NULL OR is_virtual=0)` — real trades. SOL is paper, so every
trade is virtual: **the count is 0 of 30 and cannot advance while SOL stays paper.** This is not a
counter that is "nearly there"; it is one that will read 0/30 forever until SOL goes live.

### 🔴 The macro split — flagged, as instructed

Across the window's 200 rows: **`CRITICAL_NEGATIVE` on 104 (52 %)**, NEUTRAL 63, STRONG_POSITIVE 33.
Mean `macro_gate_penalty` on the CRITICAL_NEGATIVE rows: **0.442**. `MACRO_GATE_DRYRUN = False`, so
**that penalty was applied at the score gate — while the advisor saw none of it, on any of the 200.**

The majority of the window's consultations were judged by an advisor blind to a critical-negative
macro verdict the machinery had already acted on. It remains a **coherent split** (the gate owns
macro, the advisor owns the rest) and **not** the Titan defect where the adjustment reached nothing —
here it reached the score. **Recorded as the leading candidate for the post-window prompt decision.
Not acted on.**

---

## FILES TOUCHED

| file | change | snapshot |
|---|---|---|
| `config.py` | `ADVISOR_WALL_ALIGNED_V2_MULT_CEILING = 20.0` + rationale | `config.py.bak_alignedv2_multceiling_20260804` |
| `claude_advisor.py` | ceiling gate + suppression log + import guard; 3 venue comments corrected | `claude_advisor.py.bak_alignedv2_multceiling_20260804` |

Both snapshots taken **before** any edit and verified by md5 against the originals.

## WHAT I DID NOT DO

- Did not apply anything from §5 — reported only, as instructed.
- Did not touch the SHORT companion override.
- Did not touch Titan, or read it for parameters.
- Did not re-cut the window population at any point.
