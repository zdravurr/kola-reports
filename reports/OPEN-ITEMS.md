# TITAN — OPEN ITEMS

**Read this before touching Titan.** Written to be actionable by a session with **no memory** of
2026-07-26/27. Every entry states what is known, what is **not** known, and what would close it.

Titan is a **BTC swing paper-trading bot**. `LIVE_TRADING_ENABLED = False`. All P&L below is paper
P&L from the `virtual_positions` table.

_Last updated: **2026-07-29 12:45 UTC** — §2.3 closed (`8b15ecc`), §2.11 closed (`4fc89ea`),
§2.8/§2.9/§2.10 added (`7285c5d`), §1 CORRECTED and §2.12–§2.15 opened after the full loose-ends
sweep. HEAD **`4fc89ea`**._

---

## 0. HOW TO READ THE DATA WITHOUT FOOLING YOURSELF

Four filters. Most of the wrong conclusions killed in §4 came from skipping one of them.
**Apply all four before quoting any statistic about entries or exits.**

| Filter | Why | Predicate |
|---|---|---|
| Forming-candle fix | `srv_vol_ratio_5m` before this read the **forming** candle and is not comparable | `t.timestamp >= '2026-07-04 11:58'` (commit `55d9c7f`) |
| Wall-trail window | Outcome decided by a **moved stop**, not by the entry | `NOT (opened_at < '2026-07-13T01:55' AND closed_at > '2026-07-02T23:28')` |
| Recheck TIGHTEN | Same — stop was moved after entry | `COALESCE(recheck_status,'') <> 'tightened'` |
| Excursion truth | `max_adverse_price` **stops updating at the close**, so it understates what price did | use real OHLCV candles, not stored extrema |

⚠️ The wall-trail filter must test **lifetime overlap**, not entry time. Using entry time alone
silently drops vpos 62. This exact bug produced a wrong answer once already.

**Sign convention:** skip-drift `_compute_drift_pct` is **positive = the skipped signal would have
won**. Reading it backwards inverts every veto conclusion. This caused a real inverted finding.

---

## 1. 🔴 LIVE-PATH PARITY GAP — BLOCKING before `LIVE_TRADING_ENABLED = True`

🔴 **CORRECTED 2026-07-29: this list said THREE. There are at least SEVEN, and one entry was
recorded BACKWARDS.** Measured by presence in `virtual_trader.py` vs `main.py`:

| Mechanism | virtual_trader | main (live) | was it listed? |
|---|---|---|---|
| LONG partial realisation (1/3 at +1R, `f7df202`) | 7 refs | **0** | yes |
| Recheck TIGHTEN + original-SL floor (`93c20c3`) | 52 refs | 1 | yes |
| `original_sl_price` / the 1R reference itself | 17 refs | 1 | **no** |
| **WALL_ANCHOR** | 7 refs | **0** | **no** |
| **adaptive_trail** | 5 refs | 0 (3 in `breakeven_worker`) | **no** |
| **EXCURSION_LOGGING** | 2 refs | **0** | **no** |
| **SMART_EXIT_DRYRUN** | 9 refs | **0** | **no** |
| `breakeven_jobs` | own +1R poller | **table is LIVE-only, 0 rows ever** | **recorded backwards** |

**`breakeven_jobs` does NOT live in `virtual_trader.py`.** The table is written only by
`breakeven_worker.py`, whose `enqueue()` is called from the LIVE entry path (`main.py:1411`,
`main.py:4348`). It has **zero rows in its entire life** because live trading has never run. The
paper path has a *separate* +1R implementation inside `virtual_trader`. The divergence is real; the
direction was written down wrong, and the direction is what matters when planning the rewrite.

Enabling live trading today would run a **materially different strategy** from the one being
measured.

**OPERATOR'S DECISION (2026-07-26), do not deviate:** rewrite the engine as **ONE code path with
two adapters** — orders either go to the exchange or are simulated — **NOT** piecemeal porting of
each mechanism into a second live path. Piecemeal porting is how the divergence happened.
**Do this well before live is enabled**, not as part of enabling it.

---

## 2. STILL OPEN — carry forward

### 2.1 LONG partial parameters are placeholders
`LONG_PARTIAL_LEVEL_R = 1.0`, `LONG_PARTIAL_FRACTION = 1/3` were chosen as **round numbers that
survived simulation**, not as optima. Retune at **~30 clean longs reaching above 0.5R**.
**Current: 7 clean** (was 6; vpos 82 added tonight).

**First live firing — 2026-07-27 00:07, vpos 82:** partial took **+18.91 USDT** at 1R, remainder
rode the unchanged contract to a trail exit, **total +53.79**. One datapoint. It proves the
mechanism executes and folds into `net_pnl`; it proves **nothing** about the parameters.

### 2.2 Variant C (narrower LONG trail) — UNEVALUATED, not rejected
Was not tested because the excursion data needed to judge it (full price path between entry and
exit, per position) was not assembled. **It is not a rejected idea — it is an unasked question.**
Closing it needs excursion-path coverage on real candles, the same method §4.10 settled on.

### 2.3 ✅ CLOSED 2026-07-29 (`8b15ecc`) — entry advisor now has the percentile scale
The entry advisor received the **hard-coded word "Massive"** for every wall above `4.0x` with no
percentile scale, while 100% of observed book states contain such a wall — a constant read as an
alarm. `main._entry_book_pct()` now calls the **same `_exit_pct()`** against the **same
`orderbook_density`** baseline the exit side has used since `ef7fa10`, and the label is deleted.
The system prompt's opposing-wall HARD RULE now judges thickness by the printed percentile too.
Evidence: `reports/2026-07-29-1011-titan-entry-advisor-percentiles-and-two-entry-forensics.md`

### 2.11 ✅ CLOSED 2026-07-29 (`4fc89ea`) — exit prompt's "Total depth" line
It rendered **`n/a` on 100% of the 59 exit consultations ever made**: the field was in the template
and `_build_exit_context` never set `depth_pct`. Now read from the latest `orderbook_density` row,
percentiled through the same `_exit_pct()` baseline, with the sample age printed so a stale row is
visible. Both advisors now describe depth in the same language.

### 2.4 Exit-advisor activation criterion — RECORDED BEFORE ANY DATA EXISTED
Written down **deliberately in advance** so the bar cannot be moved after seeing results.

> It goes live only if, over the first **~10 closed positions**, its **FIRST** `"close"` verdict
> beats the actual exit **both in total USDT and in positions improved**.
> **No partial credit. No re-cutting the sample. First verdict only** — not its best verdict.

**Progress: 2 of ~10 closed** (vpos 82, vpos 83). **59 consults** recorded. vpos 82: no `close`
verdict ever issued (actual +53.79 kept). vpos 83: first `close` at 2026-07-28 04:00:51 would have
been **+23.61 gross vs the actual −135.80** — an improvement of ~159 USDT. Running tally: **improved
1, worsened 0, neutral 1.** Eight more closes needed; the bar does not move.
Currently `EXIT_ADVISOR_DRYRUN = True`: it can never close a position.

### 2.5 Volume ceiling — NOT BUILT, and has an EXPIRY
Clean n is **5 SHORT / 4 LONG** (2026-07-29). SHORT **p = 0.333**; LONG **contradicts** the thesis (p = 1.000).

The earlier, exciting **p = 0.048 came from three contaminated rows** (vpos 66, 68, 74). The
sensor that reported it has since been fixed to count clean rows only.

Re-cut at **~10 clean corrected SHORT closes**. **EXPIRES 2026-09-30** if n is not reached —
**delete it then.** Rationale: the counter-short caution shipped on a statistic that quietly
stopped being true and nobody re-checked for months (§4.5). An expiry date is how that is
prevented, so **do not extend it silently**.

### 2.6 🔴 EQH/EQL SMART TP — READS AS ARMED, IS UNREACHABLE. DO NOT "FIX" IT.
`EQH_EQL_SMART_TP_ENABLED = True` in config **READS AS ARMED AND IS NOT.** The flag is only ever
read inside `_handle_liquidity_sweep()` (`main.py:2746`), and that function is **never entered**.

**Mechanism (verified, not inferred):** the dispatch gate at `main.py:2977` requires
`action_field == 'context_update' AND raw_signal_type in ('EQH','EQL')`, where `raw_signal_type`
comes from the **payload's own** `signal_type` field. The live alerts never carry that value, so
the condition is False on every fire and sweeps fall through to the generic context path.
**PROOF:** all **304** EQH/EQL rows land with `signal_type='5m_liquidity_ctx'`, and
`signal_type_ctx` — a column written **only** at `main.py:2766`, inside the handler — is NULL on
**304 of 304**. The handler has not run once since the alerts went live in May.

Restoring reachability is a **one-line change** (`classify()` already maps `Equal Highs →
LIQUIDITY/SHORT/eqh/0.9`), which is exactly why it is dangerous: anyone "repairing" dead-looking
dispatch code would **silently arm a rule that loses −971 on the clean sample** and destroys the
short side by closing winning shorts early on an EQL (vpos 58 −435, vpos 50 −403).

**STANDING DECISION: leave BOTH the flag and the routing EXACTLY as they are.** Do not set the
flag to `False` either — it changes no behaviour and would make a future reader think the rule was
evaluated and merely switched off, destroying the knowledge this entry exists to preserve.
The unreachable branch has been protecting the book **by luck, not design**.
Evidence: `reports/2026-07-27-0038-eqh-eql-sweeps-tested-and-killed.md`

### 2.7 Anthropic API key — exposed 20 days, rotation DECLINED
Leaked in plaintext to a world-readable sensor log for ~20 days. **Operator declined rotation** —
the server is single-user with no other access.
**Done:** root cause fixed on both bots (`set -a; . <env>` replaced with a scoped `_env_get()`
parser), logs purged, all sensor logs `chmod 600`, nginx `noquery` log format stops the webhook
passphrase reaching the access log.
**Revisit only if a second user or external access ever exists.** Not an open task today.

### 2.8 🔴 BEHAVIOURAL CHANGE — WATCH ENTRY FREQUENCY (opened 2026-07-29, `7285c5d`)
**WATCH, do not act.** The entry advisor now sees `ABSENT` tiers and an honest agreement line where
it was previously told *"The 3 timeframes are aligned (confluence has already passed)"* — a sentence
that was **false** on 14 of 59 executed entries, printed directly above `15m: n/a`.

**It may skip entries it would previously have approved.** That is the expected consequence of
removing a false statement, **not a regression** — but it must be **measured, not assumed.**

**The measurement, over ~2 weeks from 2026-07-29 11:36 UTC** (restart time; compare against the
equal-length window before it):
- the advisor's **skip rate** — `ai_skipped / (ai_skipped + executed)` on rows that cleared the score gate
- the **executed-entry count**

Baseline for the prior period, already computed: over 2026-07-06 → 07-29, **610** signals cleared
the score gate and **17** became trades = **2.79%**. 14 of 59 executed entries ever (24%) carried
the false alignment claim.

**Do not "fix" a drop by reverting.** A lower entry count with the same or better P&L is the
intended outcome. Only a drop **to near zero**, or a drop with **no change in the quality** of what
survives, is evidence of a defect.

### 2.9 TWO REGISTRIES HOLD THE SAME FACT AND DISAGREE — BY DESIGN. NOT PROPOSED.
`state_machine`'s 15m slot and `signal_matrix`'s MOMENTUM category both record "the 15m tier", and
they **diverge in both directions**:

| | `state_machine` 15m slot | `signal_matrix` MOMENTUM |
|---|---|---|
| TTL | **4 h** | **90 min** (cut 240→90 on 2026-05-20) |
| wiped by 1H flip / Group-B Exit | **YES** (`_clear_lower_tfs_locked`) | **NO** |
| read by | the **prompt** | the **score gate** and the HTF cascade |

Measured on the last 20 executed entries: **2** had an empty slot while the matrix held **3 live**
MOMENTUM signals; **6** had a live slot the matrix had already expired.

**`7285c5d` reports BOTH rather than picking one** — a tier the gate did not count says so, and a
tier whose slot and matrix directions disagree says so. **Reconciling the two registries is a
cascade-state change and is NOT proposed.** Anyone tempted should first read §2.8: the divergence is
also what makes the honest `ABSENT` rendering necessary.

### 2.10 AGE IS THE AGE OF LAST SET, NOT OF FIRING
`reset_1h_trend()` sets `direction = NEUTRAL` and **overwrites the slot `timestamp` with the reset
time while keeping the signal name.** So a reset tier's age is the age of the **reset**, not of the
signal. Live example — entry 19021: the prompt read *"1H trend set by: Trend Catcher Down, weight
1.0, set 1.0h ago"* when *Trend Catcher Down* had actually fired **2.0h** earlier (23:00:16) and an
Exit Signal had neutralised the tier at 00:00:29.

**`7285c5d` labels it `last set` rather than lying**, and now also prints the direction, so a reset
tier shows as `NEUTRAL` instead of reading as live. **A proper fix needs a separate `set_at` field
in `state_machine`, written only when a NEW signal arrives and preserved across resets — a
cascade-state change, out of scope, deliberately not done.** Recorded here so it is not rediscovered.

### 2.12 🔴 EXIT PROMPT PROMISES A TRAIL THAT DOES NOT EXIST — 56 of 59 consultations
The close prompt ends with *"The stop and trail remain active if you HOLD."* **The trail arms at
+1R.** Of the 59 exit consultations ever made, **56 (94.9%) happened with MFE below 1.0R**, i.e. no
trail existed at all. The sentence asserts a protection that is not there, **in the direction that
makes holding look safer than it is.**

Exactly the class of *"The 3 timeframes are aligned"* (closed by `7285c5d`), at a higher rate, and
**still live**. NOT fixed on 2026-07-29 because rewording an exit-side instruction changes advisor
behaviour and that is an operator decision, not a plumbing fix.
**This is the highest-value remaining item on Titan.**

### 2.13 🔴 THE ADX "~<20-23 = weak/ranging" LABEL IS A HARD-CODED CONSTANT WITH NO REVIEW DATE
It appears twice: as a label in the volatility block (`claude_advisor.py:334`) and **inside the
FLAT-MARKET GUARD soft rule** in `_ENTRY_SYSTEM`. A textbook ADX cut-off, asserted to the model as
fact, never validated on this book — and **contradicted by our own measurement**: the 2026-07-29
regime study found that on skipped signals ADX 25–30 drifts **−0.34%/24h** while ADX < 20 drifts
**+0.46%** (t = +2.94). High ADX marks the skips that were RIGHT.

Same class as "Massive" (§2.3) and the same failure mode that forced the counter-short caution's
retirement (§4.5): a number nobody re-checked — except this one was never checked at all.
**Either validate it or retire it. Leaving it is how the last one happened.**

### 2.14 `Long/Short ratio` has NO PRODUCER — 100% of entry prompts say `n/a`
`mc_ls_ratio` is NULL on **all 18,505** `trades` rows. Three references exist in the entire
codebase: the column declaration (`main.py:220`), the parameter default (`claude_advisor.py:241`)
and the render (`claude_advisor.py:363`). **There is no fetcher.** Siblings `mc_recent_liq_long_usd`
and `mc_recent_liq_short_usd` are equally empty.
Either implement it or delete the line — a prompt line that always says `n/a` is pure noise.

### 2.15 TWO SENSORS ARE STARVED; ONE FIRES EVERY DAY
- `regime-FLAT high-ADX` — **5 / 12 and the arrival rate is ZERO**: 0 in the last 7 days, all 5 rows
  sit in the 14–21 day band of a rolling 21-day window and **age out this week, so N goes DOWN**.
  Its predicate needs `trend_4h='bull'`, which fell from 34.9% to **7.9%** of rows. **A rolling
  window with a fixed threshold can never fire when arrivals < expiries.**
- `chop-short` — **0 / 5**; the cohort has produced 2 rows in two months and **0 since the FLAT
  floor**. At 0.7 closed positions/day this is a multi-month wait.
- `titan_bull_regime_watch` — **fires EVERY day** (157, 54, 56, 56). Its question is answered; it is
  now a daily Telegram generator, and noise is how a real alert gets missed.

**Give the two starved sensors an EXPIRY the way §2.5 has one, or they will sit in the watch-list
forever looking like progress.** Not done today — retiring a sensor is an operator call.

### 2.16 THINGS ACCUMULATING WITH NO ANALYSIS PLAN
| table | rows | plan |
|---|---|---|
| `position_excursion_samples` | **2,875** | 🔴 **§2.2 Variant C needs exactly this and nobody has run it.** The data missing on 07-27 now exists. |
| `smart_exit_dryrun_samples` | 228 | the chop-exit re-cut (`config.py:293`) has **never been done** |
| `skip_drift_samples` / `skip_attribution` | 38,480 / 7,696 | used ad hoc; no standing plan |
| `post_exit_drift_samples` / `post_exit_observatory` | 185 / 38 | **no plan recorded at all** |

### 2.17 FLAGS WITH NO OBSERVABLE EFFECT IN 7 DAYS — unclassified
`WALL_ANCHOR_DRYRUN_ENABLED`, `TREND_REVERSAL_EXIT_DRYRUN`, `DXY_HALT_DRYRUN`,
`FILTER_ENFORCEMENT_DRYRUN` are all `True` and produce **zero journal output in seven days**. They
may be correctly dormant or they may be a second EQH/EQL (§2.6). **Not traced to a proof either
way** — a bounded follow-up, not a claim.

Two empty tables ARE now explained and are **not** defects:
`breakeven_jobs` and `mfe_tracking` are **live-path only** (§1). `liquidity_sweep_state` being empty
is a **second independent proof of §2.6** — its only writer sits inside the handler that never runs.


---

## 3. WATCH-LIST — CURRENT REALITY

**Retired** (deleted `d12e276` — they answered their question or their question died):
`prior-move logger` · `TOLN (tolerate-NEUTRAL)` · `counter-short review`

**Redefined** — the old predicates could never fill again:
| Sensor | New predicate | N |
|---|---|---|
| chop-short | `ema_gap_dir_1h='Flat' AND market_regime='TREND'` (old half included `regime='FLAT'`, which the FLAT score floor drove to zero) | **0 of 5** |
| regime-FLAT high-ADX | window widened `-3d → -21d` | **5 of 12** |

**Reclassified as DATA SOURCES — these are not watchers, they FEED the exit advisor. Keep them
running; switching them off silently degrades every exit consultation:**
`orderbook-density collector` (60s, builds the percentile baseline `_exit_pct()` reads) ·
`smart-exit dryrun sampler` (live regime + volume in the exit context)

🔴 **CORRECTED 2026-07-29 — two of these are NOT accumulating, see §2.15:**
`chop-short` **0 of 5, 0 arrivals since the FLAT floor** · `regime-FLAT high-ADX` **5 of 12 with a
ZERO arrival rate and a rolling window that will take it back DOWN**

**Genuinely accumulating toward a decision:**
`volfloor` **5 SHORT / 4 LONG clean** (threshold 6; expiry §2.5) ·
`exit advisor` **2 of ~10 closed positions** (§2.4)

---

## 4. HYPOTHESES TESTED AND KILLED — DO NOT RE-OPEN WITHOUT NEW EVIDENCE

Ten. Each cost real analysis time. **A hypothesis is re-openable only with data that did not
exist on 2026-07-27** — not with a fresh intuition.

1. **Prior-4h chase** — the idea that entries chase an already-extended 4h move. No relationship
   survived contamination filtering.
2. **Signal → entry slippage** — the delay between alert and fill was proposed as a P&L drain.
   Measured; it is not material.
3. **Entry-timing bucket (R2, prior-move)** — first reported at p=0.011/0.027, both **under-filtered**.
   Correctly filtered: **p = 0.1544**, and the mid bucket collapses from n=8 to **n=1**. An artefact.
4. **Wall-side misread — DEAD, twice, on two bots by two methods.** The claim was that the advisor
   confuses a wall above with a wall below and vetoes good trades. Reality: **289 skips citing an
   ask wall above drifted −0.270%/4h (t = −4.6)** vs −0.051% control, load-bearing subset
   **−1.509%/24h**. Positive drift = the skip would have won, so **these were the BEST vetoes in
   the book**. Mercury-SOL reached the same conclusion on 2026-06-30 by replaying 471 historical
   skips: only 6 flipped (1.3%) and **all six were losers**. 🔴 **Do not re-open.**
5. **ADX + score chop gate** — the proposed separator fully overlaps winners and losers; the
   highest-ADX trade (#47) is a **−$127 loser**. Only the 1h EMA-gap 'Flat' tell survived, and it
   is still only being watched (§3), never shipped.
6. **Stop-too-tight** — rejected on geometry: stops are a uniform **2.5×ATR**, so "too tight" is
   not a property the data can express. The stop being the expensive exit is a **horizon**
   artefact, not a distance one.
7. **Volume ceiling** — 2 vs 2, p = 0.333. Tested **twice**, failed twice. See §2.5 for the expiry.
8. **EQH/EQL liquidity sweeps** — no directional edge (EQH and EQL drift the **same** way; the
   thesis needs opposite signs). Smart-TP simulated at **−971** on the clean sample. Not a
   volatility proxy either: at sweep moments ADX 25.91 vs 25.08 baseline, ATR 351.4 vs 351.7. §2.6.
9. **"11 of 11 would have survived their original stop"** — **WRONG, an artefact.**
   `max_adverse_price` **stops updating at the close**, so it never sees the excursion that
   followed. On real candles, **8 of 17 hit the original stop.** Never quote stored extrema for a
   survival question.
10. **The 5-position counterfactual** — the follow-up figure (−335.84, "the fix would have lost
    money") was **also wrong**: **survivorship bias in the resolution criterion**, because only
    fast-resolving positions could resolve on internal data. Settled properly on **13,536 real
    OHLCV candles**. 🔴 **Regardless of the outcome, do not propose restoring wall-trail or
    recheck TIGHTEN** — operator's standing instruction.

**The pattern in 3, 9 and 10:** every one was a *stored-column shortcut* standing in for a real
price path, and every one produced a confident wrong number. When the question is "what would
price have done", **fetch candles**.

---

## 5. RESOLVED 2026-07-26/27 — closed, recorded so they are not re-investigated

- **Exit advisor existence.** It was **wired but NEVER invoked**: the 5m Group-B trigger has never
  arrived, and the paper-mode position lookup returned empty. It was not broken — it was
  unreachable, which reads identically from the outside. Now **live in DRYRUN** on three triggers:
  **hourly + on 15m confirm + on armed exit** (`ef7fa10`). 3 consults recorded.
- **Entry-advisor 1H identity gap** — closed (`f0a8d30`). The advisor now sees which named signal
  set the 1H trend, its weight and its age. **`AI_ADVISOR_HIDE_1H` stays `True`**, and the identity
  is supplied as a **FACT ONLY — no statistic, win rate or historical performance attached**,
  deliberately. Renders as: `1H trend set by: Trend Catcher Up, weight 1.0, set 2.2h ago`.
- **Wall-side misread** — see §4.4. Moved out of open items entirely.

---

## 6. SHIPPED 2026-07-26 → 07-29 — twelve commits, `6c35b9d..4fc89ea`

| Commit | What it fixed |
|---|---|
| `93c20c3` | **Recheck TIGHTEN bound** — new SL can never be tighter than the **ORIGINAL** stop. (Variant B only; Variant A explicitly rejected.) |
| `596fbdf` | Gated the counter-short caution on `trend_1d != 'bull'` — **superseded hours later by `b878535`**, kept in history to show the stopgap preceded the retirement |
| `b878535` | **RETIRED the counter-trend EMA-1h soft caution** — its founding statistic does not reproduce and the cohort's sign is **inverted**. 17 lines removed, replaced by a 28-line historical note |
| `f7df202` | **LONG partial realisation** — 1/3 at +1R, remainder rides the unchanged contract; columns `partial_taken`, `realized_partial_usdt`, folded into `net_pnl` |
| `ef7fa10` | Persist the 15m entry confirmation + **wire the exit advisor in DRYRUN** (hourly / 15m confirm / armed exit) |
| `d12e276` | Retire 3 sensors, redefine 2 |
| `f0a8d30` | Give the entry advisor the **1H signal identity** (fact, not judgement) |

| `8b15ecc` | **2026-07-29** — order-book PERCENTILE scale for the ENTRY advisor; the word "Massive" deleted; the HARD RULE now judges thickness by percentile |
| `7285c5d` | **2026-07-29** — all THREE tiers to both advisors with name/direction/weight/age + an explicit agreement line; `ABSENT` replaces `n/a`; new `entry_tiers_json` column; the false "3 timeframes are aligned" sentence removed |
| `4fc89ea` | **2026-07-29** — EXIT prompt's "Total depth" line populated (had rendered `n/a` on 100% of consultations) |

`596fbdf` and `b878535` are two commits on one decision that reversed itself within a session —
recorded that way on purpose.

⚠️ **Not yet verified by a real executed entry:** `7285c5d`'s `entry_tiers_json` WRITE path. The
rendering is verified live; the persistence is exercised only when an entry executes, and none has
since 2026-07-29 11:36. If it fails, the exit advisor falls back to the legacy block — it cannot
break a trade.

---

## 7. VERIFIED STATE AT CLOSE — 2026-07-29 12:45 UTC

`git status` **clean** · origin **in sync** · HEAD **`4fc89ea`** · `titan.service` **active**
(restarted 2026-07-29 12:31:27, 0 errors since) · `nginx -t` **successful**, `noquery` format live · **Mercury-SOL untouched
and active**

**Flags live:** `LONG_PARTIAL_ENABLED=True` (1.0R, 1/3) · `EXIT_ADVISOR_PAPER_ENABLED=True`
`DRYRUN=True` `ON_15M_CONFIRM=True` `HOURLY=True` (3600s) · `CONFLUENCE_FLAT_THRESHOLD=5.0` · `HTF_TOLERATE_NEUTRAL=True` (⚠️ omitted from this list until 2026-07-29 — it is why an ABSENT tier passes the cascade) ·
`WALL_TRAIL_LIVE_ENABLED=False` · `AI_ADVISOR_HIDE_1H=True` · `ADX_BELOW_FLOOR=20.0` ·
🔴 `LIVE_TRADING_ENABLED=False` · ⚠️ `EQH_EQL_SMART_TP_ENABLED=True` **(unreachable — see §2.6)**

**Titan crons — 4 daily + 1 weekly:**
`17 8` bull-regime · `29 8` chop-short · `35 8` volfloor · `53 8` regime-FLAT high-ADX ·
`11 8 * * 1` daily-trend-cohort (weekly)

**Book:** 1 open position — vpos 84 LONG @ 63,997.3, stop 63,129.9 (original), partial not fired.
Last close vpos 83 SHORT **−143.67** (stop).

---

## 8. 🔴 STANDING PUBLISHING RULE — never link a reused path

**A reused URL is served from CACHE.** `raw.githubusercontent.com` returns a stale copy when the
path has not changed. This is not theoretical: the operator's assistant received a **stale
mid-session version of this very file twice in one evening**, and this file's entire purpose is to
be read by a session with no memory — a stale copy shows closed items as open and open items as
closed.

**THE RULE, permanent:**
1. **Never send a link to a file whose path is reused.** Reports, diffs, patches, OPEN-ITEMS,
   registries — **anything** intended for the operator.
2. Every document is published as a **NEW dated file**: `reports/YYYY-MM-DD-HHMM-<name>.md`, and
   **that dated link is what gets sent**.
3. A canonical working file (like `OPEN-ITEMS.md`) **stays** as the working copy, but an
   **identical dated snapshot** is written alongside it and the **dated** one is sent.
4. **Patches always INLINE** in the `.md` as a fenced block, never a separate `.patch` file —
   **one link must be the complete document.**
5. Verification checks **200 AND a freshness marker in the body**. A cached response also returns
   200, so a status-code check alone would miss exactly this failure.

Gist raw URLs remain **blocked entirely** (robots-disallowed) — a gist link delivers an empty file.
Full reports go to the **`kola-reports` repo**; the secret/PII scan is **fail-closed before every
push** because the repo is public; Telegram gets a short decision summary **plus the single dated
raw link**, not the report body.

Durable memory: `feedback_dated_snapshot_never_reused_urls`.
