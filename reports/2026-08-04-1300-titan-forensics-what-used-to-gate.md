# TITAN FORENSICS — WHAT USED TO GATE, AND WHAT NEVER DID

**2026-08-04 12:54 UTC · Titan HEAD `6d9281d` · LIVE, REAL MONEY, $30 × 5 = $150 notional**
**Read-only pass. Nothing changed, nothing built, no plan proposed.**

Runtime verified by import, not copied forward: `LIVE_TRADING_ENABLED=True` · TREND bar **3.0** ·
FLAT floor **5.0** · `HTF_CASCADE_ENABLED=True` · `HTF_TOLERATE_NEUTRAL=True` ·
`HTF_NEUTRAL_REQUIRE_15M_AGREE=True, DRYRUN=False`.

**Cohort:** engine-owned entries = **66** (§2.45 counted 65 on 2026-08-03 16:10; vpos **92** opened
20:25 that evening). **59** carry a computable R (`net_pnl / initial_risk_usdt`); 7 pre-date
`initial_risk_usdt`. §0-clean cohort (wall-trail lifetime overlap + recheck TIGHTEN removed) = **40**
(§2.45's 39 plus vpos 92). Live era = **7** (`stop_order_id IS NOT NULL`).

---

## 🔴 THE HEADLINE, BEFORE ANY DETAIL

**The operator's premise does not survive the code.** Titan is not bare on the range-entry axis, and
Mercury-SOL is not the reference — on this specific question **SOL is the weaker bot.**

1. Titan's FLAT floor **binds, hard**: **518 signals refused** since 2026-07-06 that would have
   cleared the TREND bar in force. Established fact #1 ("it removed the LABEL, not the trades") is
   **wrong**, and §2 below shows exactly why the earlier reading missed it.
2. Titan has a **second** live gate on the same path — the Variant-B 1H-NEUTRAL/15m-agreement
   sub-gate — which **blocked 109 of 215** tolerate-NEUTRAL passes in the last 48 hours alone.
3. Consequence: **zero of the 25 entries since 2026-07-06 had a NEUTRAL 1H tier.** All 25 had a live,
   agreeing 1H TREND tier. The 1H-NEUTRAL cohort that lost −5.98R is **already closed off.**
4. SOL's FLAT threshold of 6.5 **is not wired to any gate on either bot**. **1,894 FLAT-regime SOL
   rows passed the gate with a raw score below 6.5.** SOL has one flat 2.0 bar and no FLAT floor.
5. SOL's `market_regime` is **byte-for-byte the same signal-presence label as Titan's**. There is
   nothing to port. SOL's own config says so in writing.

**So the decision is neither RESTORE nor PORT. Everything the operator asked about is either already
working, or was never built anywhere.** The only genuinely new candidate is the EMA envelope (Part 4d),
and it is a candidate, not a result.

---

# PART 1 — THE TOLERATE-NEUTRAL RULE

## 1a. The rule, in code, and what it replaced

`titan-bot/main.py:1733–1811` (`_htf_cascade_gate`), flag at `titan-bot/config.py:443`.

```
_tier_dirs   = (trend_direction, momentum_direction, execution_direction)   # 1H, 15m, 5m
_has_opposite = any(t != 'NEUTRAL' and t != direction for t in _tier_dirs)
if not _has_opposite and HTF_TOLERATE_NEUTRAL:  ->  PASS
```

**Before:** `signal_matrix.htf_alignment()` (`signal_matrix.py:470–507`) — docstring verbatim:
*"TREND (1H), MOMENTUM (15m), and EXECUTION (5m) must all agree with proposed_direction. NEUTRAL on
any tier is treated as disagreement — sparse context means no permission to trade."*

**YES — the cascade once required the 1H tier to AGREE.** That function is unchanged to this day; the
tolerate branch was added in `main.py` *around* it and re-decides from the same dict.

| commit | date (UTC) | what |
|---|---|---|
| `bd053dd` | 2026-05-20 14:41 | tolerate-NEUTRAL branch added, `HTF_TOLERATE_NEUTRAL=False` (log-only) |
| `f911d51` | 2026-05-20 19:36 | **flipped to True — the AGREE requirement stops binding** |
| `d9eba50` | 2026-05-25 05:51 | Variant-B 1H-NEUTRAL → require 15m agreement (DRYRUN observe-only) |
| `14f0d6f` | 2026-05-25 05:59 | **Variant-B DRYRUN→False — it actually blocks** |

`bd053dd`'s own message states the size of the change: *"~615/882 blocks would pass … ~267 stay
blocked."* This was a deliberate, evidence-cited widening, not an accident — but it lasted **5 days
and 5 hours** before Variant-B narrowed it again, and 47 days before the FLAT floor narrowed it a
second time.

## 1b. Outcomes by 1H tier state — all 66 entries

The 1H tier is `matrix_breakdown_json.TREND.net_direction`, reconstructed per §0's rule (never from
`confluence_score`).

| 1H tier at entry | n (R-computable) | win | sum R | median R | mean R |
|---|---|---|---|---|---|
| **agrees** | 50 | 46.0% | **+2.68** | −0.151 | **+0.054** |
| — LONG | 22 | 31.8% | −6.44 | −0.344 | −0.293 |
| — SHORT | 28 | 57.1% | +9.12 | +0.066 | +0.326 |
| **NEUTRAL / expired** | 9 | **11.1%** | **−5.98** | −0.560 | **−0.665** |
| — LONG | 4 | 25.0% | −1.51 | −0.285 | −0.377 |
| — SHORT | 5 | **0.0%** | −4.48 | −1.076 | −0.895 |
| **OPPOSES** | **0** | — | — | — | — |

Counts including the 3 without R: 12 of 66 entries carried a NEUTRAL 1H tier; 54 agreed; **none ever
opposed.** The OPPOSITE arm of the cascade has never been the discriminator among executions — by
construction, it blocks upstream.

**Δmean = 0.72R between agreeing and NEUTRAL 1H.** This is the single largest separation found
anywhere in this pass, and it is larger than any of §2.45's ten dead branches.

**🔴 But the interval matters more than the split.** Every one of the 12 NEUTRAL-1H entries is dated
**2026-05-21 → 2026-07-05**. There has not been one since the FLAT floor shipped on 2026-07-06.

| vpos | when | side | 1H | raw | bar then | R |
|---|---|---|---|---|---|---|
| 30 | 05-21 05:20 | SHORT | NEUTRAL | 2.50 | 2.0 | n/a |
| 31 | 05-21 09:35 | SHORT | NEUTRAL | 3.75 | 2.0 | n/a |
| 33 | 05-21 17:05 | SHORT | NEUTRAL | 3.75 | 2.0 | n/a |
| 34 | 05-23 12:20 | SHORT | NEUTRAL | 1.75 | 2.0 | −1.195 |
| 36 | 05-24 03:05 | SHORT | NEUTRAL | 5.00 | 2.0 | −0.513 |
| 37 | 05-25 20:45 | LONG | NEUTRAL | 4.25 | 2.0 | −1.108 |
| 39 | 05-26 09:05 | LONG | NEUTRAL | 3.75 | 2.0 | +0.168 |
| 40 | 05-26 10:15 | SHORT | NEUTRAL | 3.75 | 2.0 | −1.130 |
| 61 | 06-30 22:15 | SHORT | NEUTRAL | 4.25 | 2.0 | −1.076 |
| 63 | 07-03 05:50 | LONG | NEUTRAL | 3.50 | 2.0 | −0.293 |
| 66 | 07-05 09:45 | SHORT | NEUTRAL | 2.50 | 2.0 | −0.560 |
| 67 | 07-05 22:35 | LONG | NEUTRAL | 3.50 | 2.0 | −0.277 |

**Eleven of twelve are below 5.0.** Under today's rules the FLAT floor refuses eleven of them outright;
only vpos 36 (raw exactly 5.00) still clears. The four that arrived after Variant-B went live
(61/63/66/67) all had an **agreeing 15m tier** — they passed Variant-B legitimately, and were then
closed off by the floor a day later.

## 1c. Does SOL have the same rule?

**Yes, set the same way, and SOL is looser.**

| | Titan | Mercury-SOL |
|---|---|---|
| `HTF_TOLERATE_NEUTRAL` | `True` (`config.py:443`) | `True` (`config.py:314`) |
| 1H-NEUTRAL → require 15m agree | **`True`, DRYRUN `False`** (`config.py:461-462`) | flag exists (`HTF_NEUTRAL_REQUIRE_15M_AGREE`, `main.py:2398`) |
| Where re-decided | `main.py` around the untouched `htf_alignment` | `signal_matrix.py:403–431` (folded into the matrix) |

SOL does **not** require agreement either. There is no working counterpart to restore — Titan already
holds the stricter half of the pair, in the 15m sub-gate that measurably fires.

## 1d. 🔴 THE CONTRADICTION — RECONCILED, AND IT IS NOT A DEFECT

**Claim to be tested:** the card says *"1H NEUTRAL (no active TREND signal)"*, so `market_regime`
should read FLAT and the entry should have faced 5.0, not 3.0.

**Checked on all 66 entries. The label and the cascade agree on every single row.**

| TREND tier NEUTRAL? | stored `market_regime` | rows |
|---|---|---|
| no | `TREND` | 46 |
| yes | `FLAT` | **4** |
| no | NULL | 8 |
| yes | NULL | 8 |

The 16 NULLs are all dated **2026-05-21 → 2026-05-26**, before the `market_regime` column was
populated on entry rows. **Zero contradictions.** Both readings come from the same object —
`alignment['trend_direction']` and `market_regime` are both `breakdown[TREND].net_direction`, computed
once per request and passed by reference (`main.py:1907–1922`).

**So: an entry whose card says "1H NEUTRAL" DID carry FLAT and DID face 5.0.** The card is not lying
about the tier.

**What the card *is* guilty of** is announcing a PASS at a gate that is not the binding one. A
tolerate-NEUTRAL PASS telegram fires **before** the score gate; on today's settings the vast majority
of those signals are then refused seconds later by the 5.0 floor or by Variant-B, and no second card
is sent for the tolerate case. That is why the live card reads like an admitted range entry when it is
almost certainly a refused one. **Display defect, not a gate defect** — and it is what made the whole
premise of this pass look true.

---

# PART 2 — HOW SOL DECIDES 'FLAT'

## 2a. Both definitions, side by side — they are the same line

```
titan-bot/signal_matrix.py:436-448          mercury-sol/signal_matrix.py:345-355
trend_net_dir = breakdown[TREND]            trend_net_dir = breakdown[TREND]
                 .net_direction                              .net_direction
'market_regime': 'TREND' if                 'market_regime': 'TREND' if
   trend_net_dir != NEUTRAL else 'FLAT'        trend_net_dir != NEUTRAL else 'FLAT'
```

**Input on both: the presence of an unconflicted signal in the TREND category. Nothing else.** No ADX,
no EMA, no price, no volatility, no range width. Established fact #2 holds for Titan **and** for SOL.

## 2b. What SOL's actually tests — the measured quantity

**None.** It measures *"did a 1H-category webhook arrive in the last TTL and not conflict with
itself"*. SOL knows this. `mercury-sol/config.py:409-412`, verbatim:

> *"The side-agnostic V2 above keys its SOFT branch on **market_regime, which is a signal-PRESENCE
> label (signal_matrix.py:355)** — **provably stuck at FLAT during real ADX>=25 breakouts**, so V2's
> trend-branch never arms (backtest 2026-07-03: 16/16 skips AGREE, 0 flips during the live ADX-28.75
> move)."*

That is SOL's own file declaring the label broken, with a measurement.

**SOL does have one place where the tape is genuinely measured and it changes an outcome** —
`ADVISOR_WALL_ALIGNED_V2` (`config.py:417`), a deterministic Python predicate at the advisor call site:

```
direction == 'LONG' AND trend_1h == 'bull' AND srv_adx_1h >= 25 AND ema_gap_dir_1h == 'Expanding'
```

**That is the only EMA-envelope condition that gates anything on either bot** — and it *relaxes* a
wall veto (turns a `skip` into an `execute`). It never refuses.

## 2c. Does SOL's 6.5 floor refuse anything?

**🔴 No. It refuses nothing, because it is not connected to a gate.**

- SOL's only score gate: `main.py:2879-2881` — `_thr = CONFLUENCE_SCORE_THRESHOLD` = **2.0**, one bar,
  no regime branch anywhere.
- `LIQUIDITY_HEATMAP_TREND_THRESHOLD=4.0` / `FLAT_THRESHOLD=6.5` reach only
  `signal_matrix.compute_score()['threshold']`, whose sole consumers are
  `signal_matrix.py:489` and `:514` — **card rendering.**

**Refusals attributable to the 6.5 floor: 0.** Proof: **1,894 FLAT-regime SOL rows passed the score
gate with a raw score below 6.5** (of 1,932 FLAT rows that passed; 3,145 rows passed in total). All
1,611 SOL `below_threshold` rows were refused by the single 2.0 bar.

**The identical dead wiring exists on Titan** (`config.py:329-330`, values 4.0/6.5; only consumer
`main.py:1846` and the card). Titan's real gate is `CONFLUENCE_SCORE_THRESHOLD`/`CONFLUENCE_FLAT_THRESHOLD`
in `main.py`. See Part 6b.

## 2d. Apply SOL's regime test to Titan's entries

**Zero flip. The test is the same test.** Running SOL's predicate over Titan's 66 entries reproduces
Titan's own labels exactly, because it is the same expression on the same input. There is no
alternative measurement in SOL to import.

## 2e. Is SOL's a real measurement of the tape?

**No.** It is signal presence, identical to Titan's, and SOL's own config documents it as broken and
routes around it. **This is not a PORT candidate. Building a real flatness measure would be NEW WORK
on both bots.**

## 2f. 🔴 CORRECTION TO ESTABLISHED FACT #1 — the FLAT floor DOES bind

`db71454`, 2026-07-06 13:54, `main.py:1921-1923` + `:3787-3789` + `:4341-4343`:

```
_eff_thr = CONFLUENCE_FLAT_THRESHOLD if matrix_result['market_regime']=='FLAT'
           else CONFLUENCE_SCORE_THRESHOLD
if _gated_score < _eff_thr:  ->  below_threshold
```

Since it shipped, of the **659** FLAT-labelled `below_threshold` rows, **518 scored at or above the
TREND bar in force at the time** (2.0 before `dee6cee` 2026-07-30 21:26, 3.0 after) and **below 5.0**.

> **518 signals were refused by the FLAT floor and by nothing else.**

Entries carrying the FLAT label: **12 of 43 before · 0 of 25 after.** Those 12 are precisely the 12
1H-NEUTRAL entries from Part 1b, and they lost **−5.98R over the 9 that have an R**.

**Why the earlier reading called it inert.** Two measurement traps:

1. **`market_regime` is NULL on every refused row.** It is written only on rows that *passed* the score
   gate (`ai_skipped`, `executed`, `virt_cap_blocked`, `risk_halt`, `claude_unavailable`). A
   `SELECT ... WHERE market_regime='FLAT'` over `below_threshold` returns **0 rows** and looks like
   "the floor never fired". The regime of a refused row must be reconstructed from
   `matrix_breakdown_json.TREND.net_direction` — the same rule §0 already mandates for scores.
2. **Flat entry rate is the wrong test.** 0.86/day → 0.82/day only says the *replacement* supply was
   sufficient. Post-floor gate-reaching supply is 601 TREND-passed vs 184 FLAT-passed — the TREND
   channel is wide enough to keep the rate flat while the FLAT channel is closed. **Constant volume is
   not evidence of an inert gate when the refused cohort is substitutable.**

---

# PART 3 — THE EMA ADJUSTMENT: WAS IT EVER LIVE?

## 3a. Never. There is no removal commit to quote.

`weight_engine.py:191-193`, verbatim: *"`total_adj` is clipped to [−1.5, +1.5] and added to
`direction_score` before storing as `confluence_score`. **Never applied to the gate check.**"* — that
line was written in `b62f623` (2026-05-17 12:23), the commit that created the engine.

Its predecessor `indicators.ema_score_adj()` arrived **the same day** in `6c0a78b` (2026-05-17 11:40).
In that commit's own `main.py`: the gate is at **line 1185** (`if direction_score < CONFLUENCE_SCORE_THRESHOLD`),
and `_ema_adj` is first computed at **line 1364** — **179 lines after the gate, on the far side of the
return.** It was post-gate on the day it was born.

**There was never a commit that removed it from a gate, because it was never on one.** The operator is
remembering a different mechanism — see 3b.

## 3b. Was there ever a SEPARATE EMA gate or veto?

Three candidates found; **not one was ever a gate on Titan.**

1. **`NEAR_TERM_VETO` (A17)** — a real EMA veto (1m AND 5m oppose → block). **SOL/ETH-ancestor only.**
   `mercury-sol/config.py:435-441` verbatim: *"Both were SOL-only / ETH-ancestor vetoes that **Titan
   NEVER had**, already neutralized to `*_ENABLED=False` (dead)."* Deleted 2026-06-08. `git log -S
   "NEAR_TERM_VETO"` over Titan's history returns **nothing** — it never existed on Titan.
2. **Counter-trend EMA-1h caution** — Titan-only, real, and **removed**: introduced 2026-06-27, gated
   on `trend_1d != bull` by `596fbdf` (2026-07-26), **retired by `b878535` (2026-07-26 17:40)**. Its
   predicate — *SHORT + `ema_status_1h`=='Bullish' + `srv_adx_1h` < 22* — is an EMA condition **with a
   threshold**, which is almost certainly what "EMA gave its weight and there was a threshold" refers
   to. **But it was a sentence injected into the advisor prompt, explicitly `ADVISORY ONLY (not a
   veto)`.** It was retired because its founding statistic inverted on re-derivation
   (ADX<15: n=48, +1.055%/12h, 85% positive, p<1e-4 — *skipping those cost money*).
3. **The matrix `threshold` field (4.0/6.5)** — display-only on both bots. Part 6b.

## 3c. Every term in Titan's adjustment, and whether any is applied

`weight_engine.weighted_adj()` returns nine terms:
`ema_cross_15m` · `ema_cross_1h` · `ema_slope_15m` · `ema_slope_1h` · `dxy` · `news` · `mtf` ·
`funding` · `macro_category`.

**The whole vector is discarded together. Not one term is applied to any decision.** And it is worse
than "not applied to the gate":

> ### 🔴 NEW — THE ADJUSTMENT IS NOT EVEN RECORDED. IT IS OVERWRITTEN 154 LINES LATER.
>
> `main.py:4008` writes `confluence_score = adj_score` (raw + adjustment), with a comment saying so.
> Then `main.py:4162` calls `signal_matrix.snapshot(row_id, symbol, matrix_result)`, and
> `signal_matrix.py:565-569` does:
> ```
> UPDATE trades SET confluence_score=?, matrix_direction=?, matrix_breakdown_json=? WHERE id=?
>                   ^ res['score'] — the RAW matrix score
> ```
> **Measured: `confluence_score == raw` exactly on 66 of 66 entries.** The adjustment survives for
> about two seconds in one log line and then ceases to exist.
>
> **Fresh proof, vpos 92 (2026-08-03 20:25, live money):** journal at 20:25:14 —
> `weighted_adj P2: dir=LONG raw=4.25 adj=+0.7795 final=5.03`. Stored `confluence_score` on trades row
> **21106: 4.25.**
>
> **SOL does the identical `UPDATE` (`signal_matrix.py:493-497`) but calls `snapshot` at `main.py:3291`
> and re-writes `confluence_score=adj_score` at `:3298` and `:3319` — after. SOL keeps the value, and
> also has a dedicated `trades.weighted_adj` column. Titan has neither.**
>
> **Consequence for §0 of OPEN-ITEMS:** its decode table says `executed` rows hold `raw + weight-engine
> adjustment`. They hold **raw**. (§0's own validation line already says *"27 `executed` as raw"* — the
> table and the validation contradict each other; the mechanism above is why the validation is right.)
>
> **Consequence for this pass:** Titan's historical adjustment is unrecoverable. Per §0's standing
> methodology a replay must first reproduce what actually happened — **for Titan that is impossible,
> and Part 4a is labelled accordingly.**

> ### 🔴 NEW — THE WEIGHT TABLE HAS RAILED
>
> `optimizer/dynamic_weights.json` (refreshed 2026-08-04 12:00): **22 of 26 segments sit exactly on a
> clip bound** — 12 at `MAX_WEIGHT=2.500`, 10 at `MIN_WEIGHT=0.200`. And the split is systematic:
> every bearish/down/negative feature is at 2.500 (`ema_status_1h:Bearish`, `ema9_slope_state_1h:Inclined_Down`,
> `news_overall:NEG`, `macro_news_category:CRITICAL_NEGATIVE`, `dxy_trend:STRONG_UPTREND`); every
> bullish/up/positive feature is at 0.200. A weight pinned to its rail is not a learned weight.
>
> ### 🔴 NEW — ONE TERM SATURATES THE CLIP AND ERASES THE OTHER EIGHT
>
> `_MACRO_CAT_BASES` reaches **±3.5**, against `_EMA_CROSS_BASE = 0.20` — **17.5×**. With the railed
> weight that term alone computes to **−8.75 or +5.00**, so whenever a macro category is present the
> total pins to the ±1.5 clip and **every EMA term is arithmetically irrelevant.** Observed in the
> live journal, 2026-08-03 02:15:
> ```
> adj=-1.5000 breakdown={'ema_cross_15m': -0.5, 'ema_cross_1h': 0.04, 'ema_slope_15m': 0.0,
>                        'ema_slope_1h': 0.0, 'dxy': 0.2797, 'news': -0.5, 'funding': -0.25,
>                        'macro_category': -8.75}
> ```

## 3d. Every other EMA consumer, and which can change an outcome

| consumer | can it change an outcome? |
|---|---|
| `weight_engine.weighted_adj` → `confluence_score` | **No** — never gated, and now shown never even stored |
| **`claude_advisor` entry prompt** (`claude_advisor.py:443-459`): `EMA-gap: 1h X% (Expanding) \| 15m …` + per-TF block, labelled *"(Contracting/Flat = compression)"* | **YES — this is the only live EMA channel to a decision on Titan.** It is text to a model, not a gate: unmeasurable in effect, unreproducible, and not auditable |
| Counter-trend EMA-1h caution | **retired** `b878535` 2026-07-26 |
| HTF cascade | **No EMA input at all** — tiers are signal-matrix categories |
| `optimizer.py:217-219` buckets | analysis only |
| `virtual_trader.py:398`, `SMART_EXIT_DRYRUN` cohort selector (`ema_gap_dir_1h='Flat'`) | sensor selector, drives no exit |
| SOL `ADVISOR_WALL_ALIGNED_V2` (`ema_gap_dir_1h=='Expanding'`) | **YES, on SOL only** — and it admits, never refuses |

---

# PART 4 — THE EMA COUNTERFACTUAL

## 4a. TITAN — adjustment applied to the entry gate

**⚠️ NOT VALIDATABLE per §0's standing methodology.** The historical adjustment was destroyed by the
overwrite in 3c. Two replays are given, each an explicit assumption; neither is a reproduction.

Threshold per row is the one actually in force: TREND 5.0 → 2.0 (`645a211` 2026-05-20 21:05) → 3.0
(`dee6cee` 2026-07-30 21:26); FLAT floor 5.0 from `db71454` 2026-07-06 13:54.
Counterfactual gate: `raw + macro_gate_penalty + adj` vs that bar.

**Baseline actually traded:** n=59, win 40.7%, sum **−3.30R**, median −0.279, mean −0.056
(LONG n=26 win 30.8% −7.95R · SHORT n=33 win 48.5% +4.64R · live-era n=7 win 14.3% −1.89R).

**Replay A — today's (railed) weights**

| | n | win | sum R | median R | mean R |
|---|---|---|---|---|---|
| ADMITTED | 55 | 40.0% | −2.26 | −0.279 | −0.041 |
| REFUSED | **4** | 50.0% | −1.04 | −0.245 | −0.261 |
| ADMITTED LONG | 22 | 27.3% | −6.90 | −0.300 | −0.314 |
| REFUSED LONG | 4 | 50.0% | −1.04 | −0.245 | −0.261 |
| ADMITTED SHORT | 33 | 48.5% | +4.64 | −0.036 | +0.141 |
| REFUSED SHORT | **0** | — | — | — | — |

**Replay B — all weights = 1.0 (pre-learning bases)**

| | n | win | sum R | median R | mean R |
|---|---|---|---|---|---|
| ADMITTED | 55 | 41.8% | −1.71 | −0.279 | −0.031 |
| REFUSED | 4 | 25.0% | −1.59 | −0.514 | −0.397 |
| ADMITTED LONG | 23 | 30.4% | −6.39 | −0.293 | −0.278 |
| REFUSED LONG | 3 | 33.3% | −1.55 | −0.993 | −0.518 |
| ADMITTED SHORT | 32 | 50.0% | +4.68 | −0.097 | +0.146 |
| REFUSED SHORT | 1 | 0.0% | −0.04 | −0.036 | −0.036 |

**Volume cost:** whole book **4/59 = 6.8%** (both replays); last 30 days **2/27 = 7.4%** (A) /
**3/27 = 11.1%** (B). Sum-R improvement: **+1.04R** (A) / **+1.59R** (B) over 79 days — inside the
noise of a book whose total is −3.30R.

## 4b. MERCURY-SOL — same replay, NOT POOLED

**This one IS validatable.** SOL stores `trades.weighted_adj`; `raw + weighted_adj == confluence_score`
on **21 of 21** rows, exact. Gate = the single 2.0 bar.

**Baseline:** n=21, win 38.1%, sum **−5.22R**, median −0.660, mean −0.249
(LONG n=9 win 22.2% −4.05R · SHORT n=12 win 50.0% −1.17R).

| | n | win | sum R | median R | mean R |
|---|---|---|---|---|---|
| ADMITTED | 20 | 35.0% | −5.23 | −0.699 | −0.261 |
| REFUSED | **1** | 100.0% | +0.00 | +0.004 | +0.004 |
| REFUSED (side) | 1 SHORT, 0 LONG | | | | |

**Volume cost 1/21 = 4.8%.** The one trade it would have refused was a scratch (+0.004R). **On SOL the
mechanism is measurable, applied to the gate, and does nothing.** It does not point the opposite way —
it points nowhere.

## 4c. 🔴 PER-TERM — NO EMA TERM REFUSES A SINGLE ENTRY

Each term replayed **alone** (`raw + macro + term` vs the bar in force), Titan, both weightings:

| term | non-zero on | refused (railed weights) | refused (weights=1.0) |
|---|---|---|---|
| `ema_cross_15m` | 66/66 | **0** | **0** |
| `ema_cross_1h` | 66/66 | **0** | **0** |
| `ema_slope_15m` | 63/66 | **0** | **0** |
| `ema_slope_1h` | 58/66 | **0** | **0** |
| `mtf` | 60/66 | **0** | **0** |
| `funding` | 34/66 | **0** | **0** |
| `dxy` | 58/66 | 3 (mean R −0.286) | 2 (mean R +0.103) |
| `news` | 31/66 | 1 (mean R +0.511) | 0 |
| `macro_category` | 40/66 | **5** (mean R −0.095) | **7** (mean R −0.229) |

**The four EMA terms are non-zero on nearly every entry and move nothing across any bar, under either
weighting.** Their maximum reach is ±0.5 with a railed weight, ±0.2 at base; entry scores sit in
0.25-point steps well clear of their bars.

> **The blended 4a result is entirely `dxy` + `macro_category`. Applying the adjustment to the gate
> would not create an EMA gate — it would create a macro-news gate wearing an EMA label.** This is the
> exact failure mode Part 4c was written to catch.

## 4d. 🔴 THE ENVELOPE — the one flatness measure never tested

`ema_gap_pct_{tf}` = `|EMA9 − EMA21| / EMA21 × 100`; `ema_gap_dir_{tf}` ∈ Expanding / Contracting /
Flat over `SLOPE_LOOKBACK` bars (`indicators.py:258-296`). **Both are already stored on every entry
row, on all five timeframes** — nothing needed collecting.

⚠️ §0 caveat carried: **EMA reads the FORMING candle by design, on every TF.** These are live-bar
values, not closed-bar values. Not a defect; a property of the number.

### §0-CLEAN COHORT (n=40) — direction

| TF | Expanding | Contracting/Flat | Δmean | perm-p |
|---|---|---|---|---|
| 1d | n=12 win 41.7% +0.78R mean +0.065 | n=16 win 56.2% +1.74R mean +0.109 | −0.044 | 0.913 |
| 4h | n=16 win 50.0% −0.23R mean −0.014 | n=24 win 54.2% +0.96R mean +0.040 | −0.054 | 0.865 |
| **1h** | **n=24 win 62.5% +5.89R mean +0.245** | **n=16 win 37.5% −5.15R mean −0.322** | **+0.567** | **0.072** |
| 15m | n=21 win 61.9% +3.97R mean +0.189 | n=19 win 42.1% −3.24R mean −0.170 | +0.359 | 0.250 |
| 5m | n=30 win 53.3% +3.99R mean +0.133 | n=10 win 50.0% −3.26R mean −0.326 | +0.459 | 0.206 |

**Per side, 1h:** LONG Exp n=8 mean +0.070 vs C/F n=7 mean **−0.619**; SHORT Exp n=16 mean +0.333 vs
C/F n=9 mean −0.091. **Both sides point the same way** — the first predicate in this book that does.

### The strongest form: 1h AND 15m both Expanding (clean cohort)

| | n | win | sum R | median R | mean R |
|---|---|---|---|---|---|
| both Expanding | 14 | **71.4%** | **+6.62** | +0.423 | **+0.473** |
| otherwise | 26 | 42.3% | **−5.89** | −0.347 | **−0.226** |
| — LONG both / other | 5 / 10 | 60.0% / 40.0% | +0.61 / −4.38 | | +0.122 / −0.438 |
| — SHORT both / other | 9 / 16 | 77.8% / 43.8% | +6.01 / −1.50 | | +0.668 / −0.094 |

**Δmean = +0.699R, permutation p = 0.029 (20,000 shuffles).**

### Width quartiles (clean cohort) — weaker and non-monotone

1h: Q1 −0.210 · Q2 −0.176 · Q3 +0.016 · Q4 **+0.516** (widest best, but Q1 median is *positive*).
15m: Q1 −0.237 · Q2 **+0.395** · Q3 −0.225 · Q4 +0.182 — no order at all.
**Width is not the signal. Direction is.**

### 🔴 REPORTING ITS SHAPE HONESTLY — three reasons it is not yet a result

1. **It fails the standing significance bar.** ~12 cells were tested here; §2.45 set Bonferroni as the
   standard. p=0.029 against α≈0.004 does not clear it. The headline predicate is also the *best of*
   those twelve, which is exactly how §4's items 3, 9 and 10 were produced.
2. **🔴 It has zero discriminating power on the live era.** All **7** live entries were **1h Expanding**
   — the predicate admits 7 of 7 — and they returned **win 14.3%, −1.89R, mean −0.270.** The one
   cohort that matters is the one cohort where it separates nothing.
3. **34 of the 40 are paper trades at 68× the live notional**, the same objection §2.45 raised against
   every positive cell it found.

**It does not join the dead list — it is the only untested flatness measure that produced a
side-consistent, monotone ordering across the three timeframes the cascade actually uses (1h/15m/5m),
and it did so on data that was already sitting in the table. But on today's evidence it is a
HYPOTHESIS WITH A POSITIVE PRIOR, not a finding, and §2.45's ruling applies to it unchanged: only
live-era observations (~30 entries ≈ three weeks) can promote it.**

### SOL, same measure (n=21, no filters — book too small to slice)

1h: Expanding n=14 mean −0.099 · Contracting n=3 mean −0.897 · Flat n=4 mean −0.284.
4h: Expanding n=10 mean −0.284 · Contracting n=6 mean −0.237 · Flat n=3 mean +0.273.
1d: Expanding n=7 mean **−0.602** · Contracting n=11 mean −0.051 — **inverted vs Titan.**
**SOL's 1h ordering agrees with Titan's (Expanding least bad); its 1d contradicts it. n=21. Not
poolable, and not evidence either way.**

---

# PART 5 — THE HIGHER TIMEFRAMES

## 5a. Titan — trend_1d and trend_4h are computed and gate NOTHING

Both are computed (`indicators.py`, `SNAPSHOT_TFS`) and stored (`main.py:176`, `:211`). Every consumer:

| consumer | role |
|---|---|
| `daily_trend_cohort_sensor.py:55-70` | observational sensor, prints a 6-cell table |
| `titan_bull_regime_drift_cut.py:41-44` | offline analysis script |
| `main.py:2779-2783` | builds `ctx['regime_entry']`, a **string** for the exit-advisor prompt |
| `claude_advisor.py:499,514` | **comment text** in the retired-caution block |

**No `if`, no veto, no threshold, on any entry or exit path.**

**🔴 Your understanding is incorrect on both halves.** `trend_1d` **was never a hard veto** — the only
time it ever appeared in a conditional was as one clause inside the *advisory* counter-trend caution
(`596fbdf`, 2026-07-26), and that whole block was deleted **four hours later** by `b878535`.
`trend_4h` **is not in the cascade**: the cascade's three tiers are the signal-matrix categories
TREND/MOMENTUM/EXECUTION, rendered as 1H/15m/5m (`signal_matrix.py:483-485`). **4h has never been a
cascade tier.**

## 5b. SOL — same, plus one extra sink

Written to `trades` (`main.py:720-721`), to `skip_attribution` (`skip_attribution.py:150-151`), and
into the advisor snapshot (`main.py:3126-3127`). **No gate.** The two bots handle higher timeframes
identically: **record, show to the model, gate nothing.**

## 5c. If Titan's daily veto exists, how many refusals?

**It does not exist, so the question is unanswerable as posed — and that is the finding.** There is no
code path, no config flag, and no DB status for a daily veto on either bot. It belongs on the "NEVER
EXISTED" list in Part 9, not the dismantled list. **Building it is NEW WORK.**

---

# PART 6 — THE THRESHOLDS

## 6a. When each was set

**Titan (git, exact):**

| value | commit | date (UTC) |
|---|---|---|
| TREND 5.0 (initial) | `b9a2935` | 2026-05-16 19:32 |
| TREND 5.0 → **2.0** | `645a211` | 2026-05-20 21:05 |
| TREND 2.0 → **3.0** | `dee6cee` | 2026-07-30 21:26 |
| FLAT floor **5.0** created and enforced | `db71454` | 2026-07-06 13:54 |
| dead display TREND 4.0 / FLAT 6.5 | `config.py:329-330` | — |

**Was Titan's ever higher? Yes — 5.0 for the first four days**, then 2.0 for 71 days, now 3.0.

**Mercury-SOL: 🔴 SOL IS NOT UNDER VERSION CONTROL.** `git rev-parse` fails; there is no repository
anywhere on the box. Dating comes only from `.bak_*` filenames and in-code notes. On that evidence
`CONFLUENCE_SCORE_THRESHOLD = 2.0` and `4.0/6.5` are **unchanged since at least 2026-06-07**
(`config.py.bak.preB_20260607_080122`). **No commit can be quoted for SOL. I am not inventing one.**

## 6b. 🔴 THE CARD THAT MISLED YOU — decoded, and the diagnosis is worse than a display bug

**There are two numbers called "threshold" and they are not the same number.**

| | real gate | dead display value |
|---|---|---|
| **Titan** | `CONFLUENCE_SCORE_THRESHOLD` **3.0** / `CONFLUENCE_FLAT_THRESHOLD` **5.0** (`main.py:1921`, `:3787`, `:4341`) | `LIQUIDITY_HEATMAP_*` **4.0 / 6.5** → `matrix_result['threshold']` → card only |
| **SOL** | `CONFLUENCE_SCORE_THRESHOLD` **2.0**, one bar, no FLAT branch (`main.py:2879`) | same **4.0 / 6.5**, card only |

**Card A (`score=1.75 · thr=6.5 · FLAT`):** 6.5 is the dead number. The real refusal was **1.75 < 2.0**.
**Card B (`score=2.25 < thr=2.0`, breakdown `thr=4.0 · TREND`):** 2.0 is the real gate; 4.0 is dead.

**Is there a second gate at 2.0? Yes — 2.0 IS SOL's only gate.** There is no gate at 4.0 or 6.5 anywhere.

**Why "2.25 < 2.0" prints as an inequality that is false.** `mercury-sol/main.py:2879-2900`:

```
_thr        = 2.0
_gate_score = direction_score if MACRO_GATE_DRYRUN else _macro_gated_score   # DRYRUN = False
if _gate_score < _thr:
    send_tg(f"score={direction_score:.2f} < thr={_thr:.1f}")   #  <-- prints direction_score
```

`MACRO_GATE_DRYRUN = False` (`config.py:221`), so the gate compares `_macro_gated_score`
(= raw + macro penalty) while the card prints the **raw** `direction_score`. **The header shows a
number that did not decide, next to the bar that did.** Not a rounding artifact — a different
quantity. Same class as `confluence_score` holding three meanings (§0).

**Do Titan's cards do the same? No, and this is one place Titan is strictly better.**
`main.py:3812-3814` prints both quantities and the effective bar:
`Below threshold (4.25 | macro −0.5 → 3.75<5.00 for SHORT)`.
**But Titan's card still carries the dead number too**, because it appends
`signal_matrix.format_for_telegram()` (`signal_matrix.py:582`) — so a Titan refusal card can read
`→ 3.75<5.0` on one line and `score=4.25/10 (thr=6.5 · FLAT)` on the next. **Two thresholds, one card,
one of them connected to nothing.**

---

# PART 7 — THE EXIT CASCADE

## 7a/7b. Both bots are TWO tiers. The premise about SOL is wrong.

`EXIT_CONFIRM_TF = '15m'` on **both**: `titan-bot/config.py:282`, `mercury-sol/config.py:176`.
Flow on both: 1H arms (`60m_exit_armed`) → 15m confirms and closes (`_execute_armed_exit`).

**SOL has no 5m exit tier.** Its 5m branch (`main.py:3888-3891`) is a **counter-entry suppression**,
and its own comment says so verbatim: *"GUARD A (tf == '5m', opposite side armed): suppress the
counter-entry hedge — **the exit runs on 15m, not here**."*

**Titan has the byte-equivalent guard** (`main.py:3694-3716`), including the same
`if EXIT_CONFIRM_TF == '5m': return _execute_armed_exit(...)` switch. **Either bot becomes three-tier
by changing one config string.** There is no divergence and therefore nothing to git-date. The
2026-07-26 finding (Titan = two tiers, no 5m exit tier ever created) is **confirmed, and now extends
to SOL.**

## 7c. Does SOL's 5m tier fire?

**As an exit: 0 times, on both bots — the branch is unreachable while `EXIT_CONFIRM_TF == '15m'`.**
As a suppression it fires and is counted: SOL **37** `entry_suppressed_armed` rows. **Titan returns the
same JSON status but writes no row** (`main.py:3714`), so Titan's count is structurally 0 and its
suppressions are invisible to any query. Minor, but it is the same class: the event happens, the record
does not.

**§2.4 freeze respected — forensics only, nothing proposed on Titan's exit side.**

---

# PART 8 — WHAT ELSE READS AS ARMED AND IS NOT

Ranked by how much it misleads.

| # | mechanism | state | since | evidence |
|---|---|---|---|---|
| 1 | **`weighted_adj` overwritten in the DB** by `signal_matrix.snapshot` (`main.py:4162` → `signal_matrix.py:565`) | **computed, logged, then destroyed** | `b62f623` 2026-05-17 (order has always been this way) | `confluence_score == raw` on **66/66** entries; vpos 92 logged `adj=+0.7795` and stored 4.25 |
| 2 | **`matrix_result['threshold']` 4.0 / 6.5** | **display-only on BOTH bots** | `b9a2935` 2026-05-16 | only consumers are card renderers; **1,894 SOL rows passed below 6.5** |
| 3 | **SOL's FLAT floor** | **does not exist** | never | one 2.0 bar, no regime branch |
| 4 | **Weight table railed** | **22 of 26 segments pinned to a clip bound** | as of 2026-08-04 12:00 | 12 at 2.500, 10 at 0.200, systematically by direction |
| 5 | **`macro_category` saturates the ±1.5 clip** | base ±3.5 vs EMA base 0.20 (**17.5×**) | `b62f623` 2026-05-17 | live journal: `adj=-1.5000 … 'macro_category': -8.75` |
| 6 | **Combo-weight learning** | thresholds ±20/−15 **USDT** vs 1R = $1.32–2.49 → needs 8–15R | live-size switch 2026-07-29 | §2.40; last weight moved 2026-07-20, and its output still enters every prompt |
| 7 | **`trend_1d` / `trend_4h`** | observational on both bots; **refusals: 0, all-time** | never gated | Part 5 |
| 8 | **`DXY_HALT_DRYRUN = True`** | a veto that logs and never blocks | `config.py:545` | **0 fires** in the 2-day journal window |
| 9 | **`FILTER_ENFORCEMENT_DRYRUN = True`** | filters evaluated, never enforced | `config.py:556` | 0 fires in window |
| 10 | **`TREND_REVERSAL_EXIT_DRYRUN = True`** | would-close logged, never closes | `config.py:563` | 0 fires in window |
| 11 | **`ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True`** | fresh ATR computed, **frozen value placed** | `config.py:262` | 0 fires in window |
| 12 | **`WALL_TRAIL_LIVE_ENABLED = False`** | off (deliberate) | `config.py:512` | — |
| 13 | **Titan's 5m counter-entry suppression writes no DB row** | event invisible to queries | `main.py:3714` | SOL writes 37; Titan writes 0 |
| 14 | **`market_regime` NULL on every refused row** | makes a working gate look inert | `db71454` 2026-07-06 | the trap that produced established fact #1 |

⚠️ **Journal retention is 2 days (Aug 02 19:55 → Aug 04 12:45).** Rows 8–11 are "0 fires in a 2-day
window", **not** "0 fires ever". Stated as measured.

**Gates that DO refuse, for contrast:** HTF cascade **10,936** `htf_blocked` · FLAT floor **518** ·
Variant-B 15m-agree **109 of 215 in 48h** · risk gate **137** · virtual cap **118** ·
TREND bar 1,022 `below_threshold` all-time.

---

# PART 9 — THE VERDICT

## A. EXIST AND WORK — on Titan, today

| mechanism | evidence |
|---|---|
| **HTF cascade OPPOSITE veto** | 10,936 blocks; **no entry in the book ever had an opposing 1H tier** |
| **FLAT-regime score floor 5.0** | **518 refusals** since 2026-07-06; FLAT entries 12/43 → **0/25** |
| **Variant-B 1H-NEUTRAL → require 15m agreement** | **109 of 215** tolerate-passes blocked in 48h; enforcing since `14f0d6f` 2026-05-25 05:59 |
| **TREND bar 3.0** | `dee6cee` 2026-07-30 |
| risk gate · virtual cap · macro gate penalty | 137 · 118 · applied pre-gate at `main.py:1918` |

**On SOL:** the HTF cascade, the single 2.0 bar, and `ADVISOR_WALL_ALIGNED_V2` (the only live EMA-envelope
predicate on either box — and it admits, never refuses).

## B. EXISTED ON TITAN AND WERE DISABLED

| mechanism | commit | date | note |
|---|---|---|---|
| **Cascade requirement that 1H AGREE** | `bd053dd` → **`f911d51`** | 2026-05-20 14:41 → **19:36** | the one real dismantling. **Partly re-armed 5 days later** by Variant-B and again on 2026-07-06 by the FLAT floor |
| **Counter-trend EMA-1h caution** (advisory, never a veto) | `b878535` | 2026-07-26 17:40 | retired on evidence — founding statistic **inverted**; do not rebuild |
| TREND bar 5.0 → 2.0 | `645a211` | 2026-05-20 21:05 | partially reversed to 3.0, `dee6cee` |

## C. NEVER EXISTED — building any of these is NEW WORK, and must be labelled as such

| claimed mechanism | reality |
|---|---|
| **EMA adjustment applied to the entry gate** | post-gate on the day it was born (`6c0a78b`, gate line 1185, adj line 1364). **No removal commit exists.** |
| **A separate EMA veto on Titan** | `NEAR_TERM_VETO` was **SOL/ETH-only** and is deleted; `git log -S` over Titan returns nothing |
| **`trend_1d` hard veto** | never a conditional on any path |
| **`trend_4h` in the cascade** | cascade tiers are 1H/15m/5m matrix categories; 4h never a tier |
| **A regime label that measures the tape** | neither bot has one; SOL's is the same broken label and SOL's config says so |
| **SOL's 6.5 FLAT floor** | not wired to a gate; 1,894 rows passed beneath it |
| **A 5m exit tier** | neither bot; one config string away on both |

## D. RANKED BY EVIDENCE — what is worth restoring

**1. Nothing at the top of this list needs restoring. The two mechanisms with the best evidence are
already live.**

| rank | candidate | n behind it | evidence | status |
|---|---|---|---|---|
| **1** | **The 1H-tier-must-agree requirement** | **12 NEUTRAL entries (9 with R): win 11.1%, −5.98R, mean −0.665** vs 50 agreeing: win 46.0%, +2.68R, mean +0.054. **Δ0.72R — the largest separation in the book** | **ALREADY CLOSED** by Variant-B (2026-05-25) + FLAT floor (2026-07-06). **0 of 25 post-floor entries had a NEUTRAL 1H.** Restoring the strict cascade would add a third lock on a door with two |
| **2** | **The FLAT floor** | **518 refusals**; the refused cohort is the −5.98R cohort | **ALREADY LIVE.** Established fact #1 is withdrawn — see 2f |
| **3** | **EMA envelope direction (1h+15m Expanding)** | clean cohort **n=40**: 14 vs 26, **+0.473 vs −0.226 mean R**, Δ+0.699, perm-p **0.029**; side-consistent; monotone on 1h/15m/5m | **NEW WORK.** Fails Bonferroni (α≈0.004 for 12 tests), **admits 7 of 7 live entries which lost −1.89R**, 34 of 40 are paper at 68× notional. A hypothesis with a positive prior, nothing more |
| **4** | **The weight adjustment on the gate** | 4/59 refused (6.8%), +1.04R / +1.59R over 79 days; **every EMA term refuses 0** | **DO NOT.** It is a macro-news gate wearing an EMA label, computed from a table that is 85% railed, on top of a value that is not even stored |
| **5** | `trend_1d` veto · a real flatness measure · a 5m exit tier | 0 | **NEW WORK, no supporting measurement on either bot** | |

## E. TWO CORRECTIONS THAT OUTLIVE THIS PASS

1. **§0's decode table is wrong for `executed` rows.** They hold **raw**, not raw+adjustment —
   `signal_matrix.snapshot` overwrites it 154 lines after it is written. §0's own validation line
   already said *"27 executed as raw"*; the table contradicted it. **Mechanism now identified.**
2. **The regime of a REFUSED row cannot be read from `market_regime` — that column is NULL on every
   refused row.** It must be reconstructed from `matrix_breakdown_json.TREND.net_direction`. This one
   omission is what made a gate with **518 refusals** read as inert.

**No plan proposed. The second task is yours to define.**
