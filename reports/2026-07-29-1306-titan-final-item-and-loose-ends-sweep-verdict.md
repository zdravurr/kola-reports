# titan-final-item-and-loose-ends-sweep-verdict

_2026-07-29 13:06 UTC_

---

**VERDICT UP FRONT.** Part 1 is applied (`4fc89ea`). The sweep found **six things we had not
listed**, two of which matter:

1. 🔴 **The exit prompt tells the advisor "The stop and trail remain active if you HOLD" on 56 of 59
   consultations where no trail existed.** The trail arms at +1R; 94.9% of consults happened below
   +1R. Same class as "The 3 timeframes are aligned", higher frequency, and it biases the advisor
   toward HOLD by promising protection that is not there.
2. 🔴 **The live-parity list in §1 is incomplete and one entry is backwards.** It records three
   paper-only mechanisms; there are **at least seven**, and `breakeven_jobs` is a **live**-path table
   with **zero rows ever**, not a paper-path mechanism.

Plus: `Long/Short ratio` has **no producer at all** (0 non-null in 18,505 rows, 100% of prompts),
two sensors are supply-starved to the point of being undecidable, and the ADX "~<20-23 = weak" label
is still a hard-coded constant sold to the advisor as a measurement — the surviving instance of the
"Massive" class.

**Titan is not finished.** Details and the honest recommendation are in §15.

---

# PART 1 — EXIT-SIDE DEPTH, CLOSED (`4fc89ea`)

`_build_exit_context` never set `depth_pct`, so `Total depth = {depth_pct}th pct` rendered **`n/a` on
100% of the 59 exit consultations ever made** — the field was in the template and never in the
context. The entry side has carried depth with its percentile since `8b15ecc`.

Fixed identically: depth is read from the latest `orderbook_density` row (the live walls dict has no
depth *volume* — its `depth` field is a level count), percentiled through the **same `_exit_pct()`
against the same baseline**, with the sample age printed so a stale row is visible.

Applied 12:31 UTC, service restarted (12:31:27), **0 errors since**. Snapshot:
`pre-exit-depth-20260729T123009Z` + `*.bak_depth_20260729T123009Z`.

**REAL STORED CONSULT — depth line populated:**

Row **19459**, **2026-07-29 13:02:07 UTC**, trigger `hourly review`, verdict **close** (confidence 0.72) — the first hourly consultation after the restart:

```
Order-book PERCENTILE scale (baseline: 23246 snapshots)
  Supporting wall = 88th pct   Opposing wall = 39th pct
  Total depth = 3044 BTC = 54th pct (sampled 58s ago)   Imbalance = 0th pct
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile: ~50th is ORDINARY.
```

**Before this commit that line read `Total depth = n/a th pct`** — on every one of the 59
consultations that preceded it. Note also `Imbalance = 0th pct`: the exit advisor is now seeing an
extreme it could previously only read as a bare number.

---

# PART 2 — LOOSE-ENDS SWEEP

## 2.1 Prompt fields rendering n/a / none / unknown

**ENTRY advisor**, last 400 consults:

| field | share |
|---|---|
| 🔴 **`Long/Short ratio`** | **100.0%** (400/400) |
| `Massive bid walls … none` | 9.2% — pre-`8b15ecc` prompts in the sample; label since deleted |
| `Massive ask walls … none` | 6.2% — same |
| `15m` | 5.5% — closed by `7285c5d` (now `ABSENT`) |

**EXIT advisor**, all 59 consults:

| field | share |
|---|---|
| `Total depth` | **100%** — **closed today by `4fc89ea`** |
| `15m confirmed by` | 93.2% — closed by `7285c5d` |

### 🔴 NEW: `Long/Short ratio` has no producer at all

`mc_ls_ratio` is **NULL on all 18,505 trades rows** — not "rarely written", **never written**.
`grep` finds three references in the whole codebase: the column declaration (`main.py:220`), the
parameter default (`claude_advisor.py:241`) and the render (`claude_advisor.py:363`). **There is no
fetcher.** The BingX global long/short account ratio was designed in and never implemented.

Same class as `depth_pct`, but worse: `depth_pct` had a source and no wiring; this has neither.
Two sibling columns are equally empty: `mc_recent_liq_long_usd`, `mc_recent_liq_short_usd`.

## 2.2 Flags that read as enabled — traced to consumers

All 26 boolean flags have a consumer file. Grep is not proof of reachability, so each was tested
against **observable evidence in the data**:

| flag | observable effect | rows | verdict |
|---|---|---|---|
| `EQH_EQL_SMART_TP_ENABLED` | `signal_type_ctx` written by the handler | **0** | 🔴 **unreachable — known, §2.6** |
| `MICROSTRUCTURE_ENABLED` | `orderbook_json` / `tape_json` | 63 / 63 | alive |
| `LEARNING_ENABLED` | `learning_at` | 58 | alive |
| `EXCURSION_LOGGING_ENABLED` | `position_excursion_samples` | 2 875 | alive |
| `POST_ENTRY_RECHECK_ENABLED` | `recheck_events` | 31 | alive |
| `SMART_EXIT_DRYRUN_ENABLED` | `smart_exit_dryrun_samples` | 228 | alive |
| `ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN` | `adaptive_trail_events` | **3** | ⚠️ barely exercised |
| `LONG_PARTIAL_ENABLED` | positions with a partial | **1** | ⚠️ one firing ever |
| `HTF_TOLERATE_NEUTRAL` | journal `HTF_WOULD_PASS` | 125 in 7d | alive, load-bearing |
| `HTF_NEUTRAL_REQUIRE_15M_AGREE` | journal `HTF_NEUTRAL` | 83 in 7d | alive |
| `WALL_ANCHOR_DRYRUN_ENABLED` | journal `WALL_ANCHOR` | **0 in 7d** | ✅ condition-gated, cleared |
| `TREND_REVERSAL_EXIT_DRYRUN` | journal `TREND_REVERSAL` | **0 in 7d** | ✅ condition-gated, cleared |
| `DXY_HALT_DRYRUN` | journal `DXY_HALT` | **0 in 7d** | ✅ condition-gated, cleared |
| `FILTER_ENFORCEMENT_DRYRUN` | journal `FILTER…DRYRUN` | **0 in 7d** | ✅ condition-gated, cleared |

Those last four looked exactly like the EQH/EQL signature, so I traced each to its consumer rather
than leaving them flagged. **All four are reachable code inside condition-gated branches:**
`WALL_ANCHOR` prints only when `wall_route == 'wall'` (`virtual_trader.py:1424`); the reversal exit
needs a signal in `CONFIRMED_REVERSAL_IDS` (`main.py:3142`); the DXY halt fires only when DXY would
block (`risk_manager.py:228`); the filter one fires only on a match. **Silence means the condition
has not occurred, not that the code is dead** — the opposite of §2.6, where the gate condition is
*structurally* False on every fire. Cleared, and recorded so the next sweep does not re-raise them.

## 2.3 Hard-coded thresholds sold to the advisor as measurements

🔴 **The "Massive" class has one live survivor**, in two places:

```
claude_advisor.py:334   f"(higher = stronger trend; ~<20-23 = weak/ranging)\n"
_ENTRY_SYSTEM           "Treat the market as flat/squeezed when 1h ADX is low (~<20-23) …"
```

A textbook ADX cut-off, asserted to the model as fact, never validated on this book — **and the
2026-07-29 market_regime study measured the opposite**: on skipped signals, ADX 25–30 drifts
**−0.34%/24h** while ADX < 20 drifts **+0.46%** (t=+2.94). High ADX marks the skips that were
*right*. The prompt tells the advisor high ADX means trend strength; the only measurement we have
says that reading is at best unsupported on Titan's own data.

Unlike "Massive" this one sits inside a **SOFT RULE the model is told to apply**, not just a label.
Not fixed here — it is a judgement change, not a plumbing fix, and it needs its own decision.

Everything else in that class is now percentile-backed (`8b15ecc`, `4fc89ea`) or definitional.

## 2.4 Tables and columns with zero / near-zero writers

**21 `trades` columns are NULL on all 18,505 rows:**

| group | columns | classification |
|---|---|---|
| TradingView payload | `signal_time, tv_pair, tv_market_position, tv_contracts, tv_order_price, volume, ema_9, ema_21, lux_strength, lux_volatility, lux_intensity, lux_sensitivity` | **dead schema** — the current alert format never sends them |
| EQH/EQL handler | `signal_type_ctx` | **never triggered** — the §2.6 proof |
| MFE tracker | `mfe_window_minutes, mfe_max_price, mfe_pnl_missed, mfe_completed_at` | 🔴 **live-path only** — `mfe_tracker.enqueue` sits in the live close handler; paper closes go through `virtual_trader`'s own SL/trail poller and never reach it |
| market context | `mc_ls_ratio, mc_recent_liq_long_usd, mc_recent_liq_short_usd` | 🔴 **no producer, ever** (§2.1) |
| new today | `entry_tiers_json` | expected — no entry has executed since `7285c5d` |

**Empty tables:**

| table | rows | classification |
|---|---|---|
| `breakeven_jobs` | **0** | **live-path only.** `enqueue` is called from `_execute_dca_entry` (`main.py:1411`) and `_resume_job_if_needed` (4348) — both live. The paper path reimplements +1R management inside `virtual_trader`. See §14: **OPEN-ITEMS §1 has this backwards.** |
| `mfe_tracking` | **0** | live-path only, as above |
| `liquidity_sweep_state` | **0** | 🔴 **second independent proof of §2.6** — its only writer is `liquidity_sweep.record_sweep()`, called from `_handle_liquidity_sweep()`, the function that is never entered. Two tables, same silence, same cause. |

## 2.5 Sensors whose threshold cannot be reached

| sensor | N vs threshold | verdict |
|---|---|---|
| `titan_regime_flat_high_adx_watch` | **5 / 12** | 🔴 **arrival rate is ZERO.** Rolling 21-day window; arrivals in the last 7 days: **0**. All 5 rows sit in the 14–21 day band and **age out this week — N will go to 0, not up.** Its predicate needs `trend_4h='bull'`, which has fallen from 34.9% to **7.9%** of rows in the last 7 days. Reachable only if BTC returns to a 4h uptrend. **A rolling window plus a fixed threshold can never fire when arrivals < expiries.** |
| `titan_chop_short_flat_gap_watch` | **0 / 5** | 🔴 **effectively unreachable.** Its cohort — closed SHORTs with `ema_gap_dir_1h='Flat'` and `regime='TREND'` — has produced **2 rows in two months and 0 since the FLAT floor**. At 0.7 closed positions/day, 5 is a multi-month wait. |
| `titan_volfloor_data_watch` | SHORT 5, LONG 5 / 6 | reachable; **note it FIRED on 07-26 at SHORT=7/LONG=10 and then fell to 4/4** — the count moved *backwards* when the sensor was corrected to count clean rows only. The 07-26 firing was a false positive. Known (§2.5) and confirmed here. |
| `titan_bull_regime_watch` | N=56 / 30 | ⚠️ **fires EVERY day** since at least 07-26 (157, 54, 56, 56). Its question is answered; it is now a daily Telegram generator. Not a defect, but it is noise, and noise is how a real alert gets missed. |
| `daily_trend_cohort_sensor` | weekly | "No new threshold crossings" — alive, quiet |

## 2.6 Statements in the prompts that can be false when printed

### 🔴 [A] EXIT: *"The stop and trail remain active if you HOLD."* — **FALSE on 94.9%**

The trail **arms at +1R**. Of the 59 exit consultations, **56 had MFE below 1.0R**, so no trail
existed at all. The sentence promises a protection that is not there, in the direction that makes
holding look safer than it is. This is precisely the class of *"The 3 timeframes are aligned"*, at a
higher rate, and it is **still live** — I did not change it, because rewording an exit-side
instruction changes advisor behaviour and that is your call.

### [B] ENTRY: *"NOTE: EVERY book state contains a wall above 4x"* — false ~9% of the time

Measured on 23,222 snapshots: **no bid wall ≥4x in 9.1%**, no ask wall in **7.8%**, neither side in
**0.8%**. The sentence's job is calibration and the percentile beside it still does that job — but
it is literally false about one snapshot in eleven per side. Low severity, recorded.

### [C] ENTRY: *"Combo weight (1.0 baseline; <1 = historical loser, >1 = winner)"*

Only **7 of 48** `signal_weights` rows differ from 1.0, and every recent entry showed exactly `1.00`.
The clause describes a scale the advisor has never seen a non-baseline value on. Harmless, but it is
a sentence carrying no information — the same disease "Massive" had.

## 2.7 Values recovered by parsing rendered text

**One remains, and it is deliberate:** `main.py:2308`, the regex that recovers the 15m name from a
stored prompt. After `7285c5d` this is the **legacy fallback for rows written before today**;
current rows read `entry_tiers_json`. Every other former instance is gone. Class closed.

## 2.8 Statistics embedded in prompts or rules with no review date

**None live.** Every statistic in `claude_advisor.py` (`n=143`, `p<1e-4`, `+1.055%` …) sits in the
**historical note documenting the RETIRED counter-trend caution** (`b878535`) — comments, not prompt
text. `config.py` carries two statistics in comments justifying structure (`n=10` clean longs for the
partial's shape, `n=28` for the chop-exit logger); both are labelled as the basis for a **shape**
decision, not a live numeric rule.

The two live rules that *are* numeric — the FLAT floor (5.0) and the ADX guard (~20-23) — carry **no
review date**. The FLAT floor at least has a study behind it (2026-07-29). **The ADX guard has
none.** That is §2.3's finding restated as a governance gap: the failure mode that killed the
counter-short caution was a statistic nobody re-checked, and the ADX guard is a number nobody ever
checked in the first place.

---

# PART 3 — STATE OF EVERYTHING

## 3.9 Commits `93c20c3` → HEAD (9)

| commit | date | what it changed | verified live |
|---|---|---|---|
| `596fbdf` | 07-26 | gated the counter-short caution on `trend_1d != 'bull'` | superseded hours later |
| `b878535` | 07-26 | **RETIRED** that caution — founding statistic does not reproduce, cohort sign inverted | ✅ code path removed |
| `f7df202` | 07-26 | LONG partial 1/3 at +1R | ⚠️ **one firing ever** (vpos 82, +18.91) |
| `ef7fa10` | 07-26 | persist the 15m confirm + wire the exit advisor in DRYRUN | ✅ 59 consults, 15m rows arriving |
| `d12e276` | 07-26 | retire 3 sensors, redefine 2 | ✅ but see §2.5 — both redefined sensors are now starved |
| `f0a8d30` | 07-27 | 1H signal identity in the entry prompt | ✅ superseded by `7285c5d` |
| `8b15ecc` | 07-29 | order-book percentile scale for the entry advisor | ✅ live prompts show percentiles |
| `7285c5d` | 07-29 | all three tiers, name/direction/weight/age + agreement | ✅ live exit consult 12:02:01; entry render verified; **no executed entry yet** |
| `4fc89ea` | 07-29 | exit-side depth percentile (this session) | ✅ see Part 1 |

**Not yet verified by a real executed entry:** `7285c5d`'s `entry_tiers_json` write path. It is
exercised only when an entry executes; none has since 11:36. The rendering is verified, the
persistence is not.

## 3.10 OPEN-ITEMS entry-by-entry

| entry | recorded state | reality |
|---|---|---|
| §1 live-parity gap | 3 mechanisms | 🔴 **INCOMPLETE — at least 7, and one is backwards.** See §14 |
| §2.1 LONG partial params | 7 clean longs | **7** — unchanged, correct |
| §2.2 Variant C unevaluated | needs excursion data | still open; **2,875 excursion samples now exist and nobody has run it** |
| §2.3 entry wall label | open | ✅ **CLOSED `8b15ecc`**, marked |
| §2.4 exit-advisor criterion | 1 of ~10 | **2 of ~10** closed since it went live; 59 consults |
| §2.5 volume ceiling | 4/4 clean | **5 SHORT / 4 LONG**; expiry 2026-09-30 stands |
| §2.6 EQH/EQL unreachable | leave alone | ✅ correct, and now **doubly proven** (`liquidity_sweep_state` also empty) |
| §2.7 API key | not an open task | unchanged |
| §2.8 entry-frequency watch | opened today | open, measurement window started 11:36 |
| §2.9 two registries | opened today | open |
| §2.10 age = last set | opened today | open |
| §3 watch-list | "genuinely accumulating" | 🔴 **two of the five are starved**, see §2.5 |

**Closed but not marked:** none found.
**Marked closed but not done:** none found.
**Marked as accumulating but actually stalled:** `regime-FLAT high-ADX` and `chop-short`.

## 3.11 Sensors and crons

| cron | watches | N / threshold | ever fired | decidable when |
|---|---|---|---|---|
| `17 8` bull-regime | bull-regime drift cut | 56 / 30 | **daily since ≤07-26** | already decided; now noise |
| `29 8` chop-short | chop-short cohort | **0 / 5** | no | not on this horizon |
| `35 8` volfloor | clean corrected closes | 5+5 / 6 | 07-26 (false) | ~2–4 weeks at 0.7/day |
| `53 8` regime-FLAT high-ADX | FLAT mislabel cohort | **5 / 12, arrivals 0** | no | only if 4h returns to bull |
| `11 8 * * 1` daily-trend-cohort | daily-trend cells | weekly | quiet | open-ended |

## 3.12 Flags at runtime vs OPEN-ITEMS §7

All ten flags §7 records **match runtime exactly**: `LIVE_TRADING_ENABLED=False`,
`LONG_PARTIAL_ENABLED=True` (1.0R, 1/3), `EXIT_ADVISOR_PAPER_ENABLED/DRYRUN/ON_15M_CONFIRM/HOURLY
=True` (3600s), `CONFLUENCE_FLAT_THRESHOLD=5.0`, `WALL_TRAIL_LIVE_ENABLED=False`,
`AI_ADVISOR_HIDE_1H=True`, `ADX_BELOW_FLOOR=20.0`, `EQH_EQL_SMART_TP_ENABLED=True` (unreachable).

⚠️ **§7 omits `HTF_TOLERATE_NEUTRAL=True`** — the flag that lets an absent tier pass the cascade, and
the direct cause of the `15m: n/a` symptom. A load-bearing flag missing from the record.

## 3.13 Accumulating with no analysis plan

| table | rows | plan |
|---|---|---|
| `skip_drift_samples` | 38 480 | used ad hoc; **no standing plan** |
| `skip_attribution` | 7 696 | same |
| 🔴 `position_excursion_samples` | **2 875** | **§2.2 Variant C needs exactly this and nobody has run it.** The data that was missing on 07-27 now exists. |
| `smart_exit_dryrun_samples` | 228 | the chop-exit re-cut (`config.py:293`) has **never been done** |
| `post_exit_drift_samples` / `post_exit_observatory` | 185 / 38 | **no plan recorded at all** |
| `orderbook_density` | 23 223 | ✅ consumed by both advisors |

## 3.14 🔴 LIVE-PARITY — the real list

OPEN-ITEMS §1 records **three**. Measured by presence in `virtual_trader.py` versus `main.py`:

| mechanism | virtual_trader | main (live) | in §1? |
|---|---|---|---|
| LONG partial realisation | 7 refs | **0** | yes |
| Post-entry recheck (+ the `93c20c3` floor) | 52 refs | 1 | yes |
| `original_sl_price` / 1R reference | 17 refs | 1 | no |
| **WALL_ANCHOR** | 7 refs | **0** | 🔴 **no** |
| **adaptive_trail** | 5 refs | 0 (3 in `breakeven_worker`) | 🔴 **no** |
| **EXCURSION_LOGGING** | 2 refs | **0** | 🔴 **no** |
| **SMART_EXIT_DRYRUN** | 9 refs | **0** | 🔴 **no** |
| `breakeven_jobs` | own +1R poller | **the table is LIVE-only, 0 rows** | 🔴 **recorded backwards** |

**§1 says `breakeven_jobs` "lives in `virtual_trader.py`". It does not.** The table is written only
by `breakeven_worker.py`, whose `enqueue` is called from the live entry path; it has **zero rows
ever** because live trading has never run. The paper path has a *separate* +1R implementation. The
divergence is real — it is just not the one written down, and the direction matters when someone
plans the one-code-path rewrite.

**The operator's standing decision (§1) — one code path with two adapters, not piecemeal porting —
is correct and is now better supported: there are at least seven divergences, not three.**

---

# 3.15 HONEST VERDICT

**No. Titan is not finished — but nothing found today blocks moving to Mercury-SOL.**

The distinction matters, so here it is precisely.

**Nothing found is dangerous right now.** `LIVE_TRADING_ENABLED=False`, the exit advisor is DRYRUN
and cannot close anything, and every defect in this sweep degrades *information quality*, not
*trade safety*. The bot will not do something harmful while unattended.

**Two things should be decided before Titan is called done, and both are yours, not mine:**

1. **The exit prompt's false trail promise** (§2.6[A]) — 56 of 59 consultations. It is the same
   defect we just spent a session removing from the entry side, it is larger in frequency, and it
   pushes the advisor toward HOLD. I did not touch it because rewording an instruction changes
   behaviour. **This is the single highest-value remaining fix.**
2. **The ADX "~<20-23 = weak/ranging" rule** (§2.3, §2.8) — a hard-coded constant inside a SOFT RULE,
   contradicted by our own measurement, with no review date. Same class as the caution that had to be
   retired. Either validate it or retire it; leaving it is how the last one happened.

**Three that are cheap and can wait:** `Long/Short ratio` should be removed from the prompt or
implemented (a line that always says `n/a` is noise); `titan_bull_regime_watch` should stop firing
daily; the two starved sensors should be given an expiry the way `volfloor` has one, or they will sit
in the watch-list forever looking like progress.

**One that is real work and is already correctly parked:** the live-parity rewrite (§14). Seven
divergences, not three — but `LIVE_TRADING_ENABLED=False` means it blocks nothing today.

**And one honest gap in what I delivered this week:** `7285c5d`'s `entry_tiers_json` persistence has
**not** been verified by a real executed entry — only the rendering has. The first entry after
2026-07-29 11:36 will confirm or refute it, with no further work from anyone. If it fails, the exit
advisor silently falls back to the legacy block; it cannot break a trade.

**Recommendation:** go to Mercury-SOL. Come back for items 1 and 2 above as a short, self-contained
session — they are two prompt decisions, not an engineering project.

---

## STATE AT CLOSE

`git status` clean · HEAD **`4fc89ea`** · pushed · `titan.service` **active** since 12:31:27 UTC,
**0 errors** · hourly exit consultation firing on cadence (12:02:01, 13:02:07) · **Mercury-SOL
untouched and active**

**Book: 1 open position** — vpos 84 LONG @ 63,997.3, stop 63,129.9 (original), partial not fired.

OPEN-ITEMS working copy updated and pushed; byte-identical dated snapshot at
`reports/2026-07-29-1245-open-items.md` (§8 — the dated path is the linkable one). §1 corrected,
§2.11 closed, §2.12–§2.17 opened, §6/§7 brought to `4fc89ea`.
