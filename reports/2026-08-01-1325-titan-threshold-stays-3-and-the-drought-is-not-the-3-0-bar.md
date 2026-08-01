# titan-threshold-stays-3-and-the-drought-is-not-the-3-0-bar

_2026-08-01 13:25 UTC_

---

# TITAN — THRESHOLD STAYS AT 3, RECORDED WITH ITS REASONING · AND THE DROUGHT IS **NOT** THE 3.0 BAR

_2026-08-01 13:40 UTC · HEAD `3316e8a` · LIVE, real money · **no code change in this pass**_

## DECISION LINE

**`LOSS_STREAK_THRESHOLD` stays at 3.** Recorded in OPEN-ITEMS **§2.37** with the full reasoning, so it
cannot be reopened later as a rationalisation. Nothing was touched.

**And the answer to the drought question is a clean no.** The 3.0 confluence bar has refused
**2 TREND signals in its entire 38.9-hour life**, and **both scored 1.5 — below the OLD 2.0 bar as
well.** 🔴 **The 2.0 → 3.0 raise has cost EXACTLY ZERO entries.** Predicted ≈2.2 additional
refusals/day; observed **0.00/day, zero total.**

The drought has two other causes, and both are measured below: the **HTF cascade tightened** from ~73%
to **82.7%** of all entry signals, and the **regime composition collapsed toward FLAT** — **88.2%** of
gate-reaching signals in the last 24h, where the governing bar is the deliberately-unchanged **5.0**.
**Only 4 TREND signals reached the score gate in 24 hours, against a 30-day average of ~21/day.**

Per the pre-registration's own instruction: **this is a finding about the distribution and not a
reason to move any bar.**

---

## 1. THE DECISION, AND WHY — OPEN-ITEMS §2.37

`LOSS_STREAK_THRESHOLD = 3` · `LOSS_STREAK_COOLDOWN_HOURS = 4` · **unchanged, byte-identical.**

Recorded before any result exists, in your terms:

1. **Softening a brake because it blocked one winner is outcome-fitting on n=1** — the exact failure
   mode that has killed eleven hypotheses in §4. The whole case for "3 is too tight" is a single trade
   that happened to work.
2. **It is not a money mechanism.** Three consecutive losses mean *something is systematically off*,
   and that is equally true whether they cost **$4 or $400**. Size-blindness is the feature.
3. **The 7.2% figure is contaminated and we do not know the live rate.** The 30-day window spans a
   **68× notional change** ($10,000 → $146); the two 07-31 windows mix a **−137.32** loss with
   **−2.54** and **−0.82**. A rate measured across that discontinuity predicts nothing.
4. **A safety mechanism found dead after 2.5 months must not have "make it fire less" as its first
   treatment.** Restore, measure at one size, then discuss calibration.

**What would reopen it:** a measured live-size firing rate — not a single blocked winner. And it is
**not provisional on the §2.4 result**: a positive advisor window would be no evidence about this
brake.

## 1a. Recorded alongside it

| § | what it says |
|---|---|
| **2.37a — §2.4 CONFOUND** | The brake now **shapes the remaining ~6 datapoints**: entries following a losing streak are removed, so they come from a differently-filtered population than the first four. Had it been live it would have blocked **vpos 89 (+2.30) and vpos 90 (−0.61)** — the sample's best and one of its worst — leaving n=2 with a different net. **Does not void the window** (§2.4-OP: entire entry side not frozen); count stays **4 of ~10**; the result must carry this on its face. Also added as caveat **5** inside §2.4 itself. |
| **2.37b — MEASUREMENT DUTY** | The 30-day rate is **not predictive**. The live-size rate must be measured over the §2.4 window and reported **alongside** the window's result, not separately: halts fired · hours halted (and % of wall-clock) · entries blocked · what those entries would have been (side, tier set, recoverable outcome). **Until that table exists, no claim about this brake's cost or benefit is supportable in either direction.** |
| **2.37c — SIZE PRECONDITION** | `daily_loss_halt()` works but **cannot bite at $146**: −5% of $510.41 = **−$25.52**, and at the live 1R (mean **$1.96**) that is **~13 full-stop losses in one UTC day**. Live-era troughs: **−0.50%**, **−0.26%**. Added to the size-increase checklist **alongside §1b (margin mode CROSSED)**: before any notional increase, **re-derive `DAILY_LOSS_PCT_LIMIT` against the new 1R and state how many stop-outs it then represents.** A limit meaning "13 stops" at one size and "1.5 stops" at another is not the same limit, and finding that out afterwards is the wrong order. |

---

## 2. THE DROUGHT — WHICH GATE IS ACTUALLY REFUSING

### Method, and the §0 trap avoided

**Reconstruction validated before anything was concluded** (§0 standing methodology). Rebuilding the
gate number from `matrix_breakdown_json` — NEUTRAL categories contribute 0, each directional category
adds its contribution to its own side, `gated = raw + macro_gate_penalty` — reproduced the **stored**
`confluence_score` on **40 of 40** `below_threshold` rows since the bar went live. **0 mismatches.**

Two §0 traps were live here and both were avoided:

- 🔴 **`confluence_score` holds three different quantities by status.** The validation is on
  `below_threshold` rows only — the one cohort where it equals the gated score. Row 20196
  (`ai_skipped`) stores **6.29** while its gate number was **7.0**; that is the `raw + weight-engine
  adjustment` quantity, and reading it as the gate number would have been wrong.
- 🔴 **`macro_gate_penalty` is NULL on every `risk_halt` row.** Row 20103 is therefore counted as
  having **reached and passed** the gate, with **no score asserted for it** — its gate number is not
  computable and is not guessed.

**Regime is reconstructed, not read:** `market_regime = 'TREND' if breakdown['TREND'].net_direction !=
NEUTRAL else 'FLAT'` (`signal_matrix.py:448`) — the DB column is empty on `htf_blocked` and
`below_threshold` rows. The HTF cascade runs **in front of** the score gate (`main.py:3679-3683`), so
`htf_blocked` rows **never reached the bar** and are excluded from every denominator below.

### The answer, last 24 hours (2026-07-31 13:15 → 2026-08-01 13:15 UTC)

| | count |
|---|--:|
| entry-path rows | **196** |
| refused **before** the score gate (HTF cascade) | **162 (82.7%)** |
| **reached the score gate** | **34** |
|   · of which **TREND** (the 3.0 bar's jurisdiction) | 🔴 **4** |
|   · of which **FLAT** (the unchanged 5.0 bar) | **30** |
| 🔴 **refused BY THE 3.0 TREND BAR specifically** | **2 of 4** |
| refused by the 5.0 FLAT bar | 26 of 30 (86.7%) |
| passed the score gate, then skipped by the entry AI | 4 |
| executed | 1 (vpos 90, 14:25 — the last entry) |

**Every TREND signal that reached the gate in 24h, verbatim:**

| row | when (UTC) | dir | raw | macro | gated | bar | status |
|---|---|---|--:|--:|--:|--:|---|
| 20100 | 07-31 14:25 | SHORT | 2.25 | +1.0 | **3.25** | 3.0 | **executed** → vpos 90 |
| 20103 | 07-31 14:30 | SHORT | 2.25 | *NULL* | *not computable* | 3.0 | risk_halt (passed the bar) |
| 20113 | 07-31 15:25 | SHORT | 2.50 | −1.0 | **1.50** | 3.0 | below_threshold |
| 20116 | 07-31 15:30 | SHORT | 2.50 | −1.0 | **1.50** | 3.0 | below_threshold |

### Against the pre-registration — whole life of the bar (~38.9 h)

| # | quantity | predicted (§2.0, written 21:20 **before** the 21:26 commit) | **observed** |
|---|---|---:|---:|
| 1 | refusal rate on TREND signals reaching the score gate | **15.72%** | **11.76% — 2 of 17** |
| 2 | additional refusals per day from the raise | **≈2.2/day** | 🔴 **0.00/day** |

🔴 **THE RAISE HAS COST ZERO ENTRIES, TOTAL.** Both refused TREND signals scored **1.5** — below the
old **2.0** bar as well. **Not one signal has landed in the 2.0–3.0 band the raise created.** The
refusal rate is if anything *below* prediction, and on n=17 the interval is far too wide to call that
a divergence in either direction.

### What is actually causing the drought

| period | entry rows | HTF-blocked | reached gate | TREND | FLAT | %FLAT | executed |
|---|--:|--:|--:|--:|--:|--:|--:|
| 30d before the bar | 5609 | 4084 (72.8%) | 1524 | 630 | 894 | 58.7% | 26 |
| 7d before the bar | 1221 | 902 (73.9%) | 319 | 169 | 150 | 47.0% | 7 |
| bar live, first 24h | 230 | 195 (84.8%) | 35 | 17 | 18 | 51.4% | 3 |
| **last 24h** | 196 | **162 (82.7%)** | 34 | 🔴 **4** | 30 | 🔴 **88.2%** | 1 |
| bar live, whole life | 360 | 296 (82.2%) | 64 | 17 | 47 | 73.4% | 3 |

**1 · The HTF cascade is where the funnel closes, and it tightened.** ~73% before → **82.2%** since
the bar went live. It runs ahead of the score gate, so **162 of 196** signals in the last 24h never
reached any bar.

**2 · The regime composition collapsed toward FLAT.** **88.2%** of gate-reaching signals in the last
24h vs 58.7% over the prior 30 days. **TREND signals reaching the gate fell from ~21/day to 4/day —
a 5× collapse.** In FLAT the governing bar is `CONFLUENCE_FLAT_THRESHOLD = **5.0**`, deliberately left
alone on 2026-07-30, and it refused **26 of 30**.

**So the 3.0 bar barely got to vote.** If the drought needs explaining, the HTF cascade rate and the
FLAT-regime share are where to look — not the TREND bar.

### Stated as a limit, not smuggled past

n = **17** TREND signals over 38.9 hours. That is enough to say **the raise removed no entries**
(a direct observation: nothing landed in the 2.0–3.0 band), and **not** enough to compare 11.76%
against 15.72% as rates. Recorded as **§2.38 WATCH, no action.** The 15-entry review still stands, and
its denominator is still 15 **executed** entries — of which there have been **3**.

---

## 3. STATE

| | |
|---|---|
| HEAD | `3316e8a` — **unchanged this pass**, no code touched |
| titan.service | active, `NRestarts=0`, up since 13:08:26 UTC |
| open position | none — last close 2026-07-31 16:25:42 |
| §2.4 | **4 of ~10**, window intact, bar unmoved |
| `LOSS_STREAK_THRESHOLD` / `COOLDOWN_HOURS` / `DAILY_LOSS_PCT_LIMIT` | **3 / 4 / 0.05 — untouched** |
| `CONFLUENCE_SCORE_THRESHOLD` / `CONFLUENCE_FLAT_THRESHOLD` | **3.0 / 5.0 — untouched** |
| OPEN-ITEMS | `8859e98` — §2.37, §2.37a, §2.37b, §2.37c, §2.38, plus caveat 5 inside §2.4 |

## WHAT I DID NOT DO

- **No code change of any kind.** This pass is measurement and record only.
- **Did not move any bar** — not the streak threshold, not the confluence bars, despite the 3.0 bar
  measuring below its predicted refusal rate. The pre-registration forbids it and the n forbids it.
- **Did not treat 11.76% vs 15.72% as a divergence.** n=17.
- **Did not assert a gated score for `risk_halt` row 20103** — its `macro_gate_penalty` is NULL and
  the number is not recoverable.
- **Did not void or restart the §2.4 window**, and did not let the new confound become a reason to.
