# titan-score-distribution-trend-flat-histograms-and-the-capacity-number

_2026-07-30 21:12 UTC_

---

# TITAN — THE SCORE DISTRIBUTION BEHIND THE 2.0 BAR

**2026-07-30 21:30 UTC · READ-ONLY · nothing changed, nothing recommended · HEAD `1161802`**

Answers the five questions asked of §1 of the 19:14 gauntlet report, which gave the distribution
only as a minimum (2.25). Volume only. No outcome is used to argue for or against any bar.

---

## DECISION LINE

**3.0 is neither cosmetic nor drastic — it is the smallest bar that does anything at all, and it
does a specific, bounded thing: it refuses 15.7% of TREND signals reaching the gate instead of
today's 4.5%, and it removes 3 of the 23 TREND trades actually taken in 30 days.** The drastic
step is 3.5, not 3.0: 3.5 removes 10 of 23. Between them sits the densest cluster in the whole
distribution — five entries at a gated score of exactly 3.25.

**Two structural facts the histogram exposes that the minimum could not:**

1. 🔴 **On the RAW scale there is a hole from 2.75 to 3.50 with zero events in it.** Every bar in
   `(2.75, 3.50]` refuses exactly the same 144 events. On raw score, **3.0 and 3.5 are the same
   bar.** Only `total_gate_adj` separates them — which means choosing between 3.0 and 3.5 is not
   a choice about signal quality, it is a choice about how much macro adjustment you let move a
   signal across the line.
2. 🔴 **Today's 2.0 bar refuses 27 TREND events — and 0 of them on raw merit.** The raw minimum
   is 2.25, so all 27 were pushed under 2.0 by `total_gate_adj`. §1 said the constant cannot bind;
   the distribution says something sharper: **the 27 refusals attributed to the score gate are
   actually refusals by the macro adjustment, wearing the score gate's name.**

**And the caveat §2 asked me to quantify is empirically null in the range under discussion:**
of the 36 `concurrent_position_halt` refusals, **0 were blocked by an incumbent that a bar of
2.5, 3.0, 3.5 or 4.0 would have refused.** It only turns on at 4.5, and then only because of one
position. Details and the honest limits of that number in §4 — it is a weaker sample than "36"
suggests.

---

## STATE AT PUBLICATION — read from runtime at 20:50–21:05 UTC, not copied forward

| check | result |
|---|---|
| `git status` | **clean** (0 modified) — single repo at `/root/.git` covering `titan-bot/` and `mercury-bot/` |
| HEAD | **`11618025ebb902b624ebef71bc6c545c149a891b`** *fix(titan): one ADX, one window…* (2026-07-30 14:10:47) |
| **runtime = commit by hash** | ✅ **proven.** Working tree clean ⇒ disk == HEAD. Process start **14:10:59.910 UTC**; latest of 38 `.py` mtimes is **14:09:52** (`sensor_events.py`); **0 files modified after process start.** |
| `titan.service` | **active**, MainPID **319804**, `NRestarts=0`, cwd `/root/titan-bot` |
| journal since boot | **0** tracebacks / CRITICAL / `REFUSING TO START` |
| **Mercury-SOL untouched** | ✅ lives at `/mnt/volume_nyc1_1780480650620/mercury-sol` (not `/root/mercury-bot`). Service **active/running** since **2026-07-21 06:39:33**, `NRestarts=0`. Latest `.py` mtime **2026-07-05 23:13** — **no file touched since before the service started.** |

**FOUR BOOT GATES — all green in the live journal for this process (14:11:05–14:11:11):**
```
[ORDER-MODE]    🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[ORDER-MODE]      LIVE_TRADING_ENABLED = True   ORDER_ADAPTER_LIVE = True
[ORDER-MODE]      sizing: margin $30 x 5 = $150 notional per entry
[RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 1 exchange position(s), 1 open row(s)
[RECONCILE]     LONG open, SL present @ 64028.8 — kept.
[RECONCILE]     engine owns positions — NOT enqueueing a breakeven job (item 12a: single owner)
```

**vpos 87 — OPEN.**

| | |
|---|---|
| side / size | **LONG 0.0023 BTC @ 64838.7** · $149.13 notional · 5x · margin $30 |
| opened | 2026-07-30 12:05:17 UTC · `status = open`, `closed_at = NULL` |
| stop | **64028.8**, `original_sl_price` identical — **never moved** |
| `recheck_status` | **`done`** (not `tightened` — unlike vpos 86) |
| water mark | 65121.0 · `entry_adx_1h` 13.516 · `entry_adx_1h_window` **NULL** (row predates the `1161802` window stamp; consistent with the 15:10 note) |

**Exchange — BOTH probes, agreeing, no orphans:**

| probe | result |
|---|---|
| unified `fetch_positions` | 1 position — LONG 0.0023 @ 64838.7, `id 2082799688088776706`, uPnL **−$0.1638** |
| raw `swapV2/user/positions` | 1 row — `positionId 2082799688088776706`, `positionAmt 0.0023`, `avgPrice 64838.7`, LONG |
| unified `fetch_open_orders` | 1 order — `2082799690256592896` |
| raw `swapV2/trade/openOrders` | 1 order — **same id**, `STOP_MARKET SELL posSide=LONG stopPrice=64028.8 workingType=MARK_PRICE closePosition=true status=NEW` |
| **DB ↔ exchange** | `virtual_positions.stop_order_id = 2082799690256592896` — **identical**. 1 position ↔ 1 open row ↔ 1 stop. |

**Balance:** `USDT free 480.01 · used 29.83 · total 509.84`. Mark ~64766.8.
**Closed today:** 1 (vpos 86, −$2.54, `reason=sl`).

**Flags read from `config` with runtime==commit proven:**

| flag | value | | flag | value |
|---|---|---|---|---|
| 🔴 `LIVE_TRADING_ENABLED` | **True** | | `CONFLUENCE_SCORE_THRESHOLD` | **2.0** |
| 🔴 `ORDER_ADAPTER_LIVE` | **True** | | `CONFLUENCE_FLAT_THRESHOLD` | **5.0** |
| `LEVERAGE` / `LIVE_FIXED_MARGIN_USDT` | 5 / **30.0** | | `MAX_POSITIONS_PER_SIDE` | **1** |
| `PAPER_FIXED_MARGIN_USDT` | 2000.0 | | `ADX_FLAT_FLOOR` | 20.0 |
| 🔴 `EXIT_ADVISOR_DRYRUN` | **False** — changed by `81875c9`; the 03:30 snapshot still says True | | `MACRO_BLACKOUT_MINUTES` | 30 |
| `WALL_TRAIL_LIVE_ENABLED` | False | | `DAILY_LOSS_PCT_LIMIT` | 0.05 |
| `HTF_CASCADE_ENABLED` / `HTF_TOLERATE_NEUTRAL` | True / True | | `DXY_HALT_DRYRUN` / `FILTER_ENFORCEMENT_DRYRUN` | True / True |

---

## 0. METHOD — AND A RECONSTRUCTION DEFECT THAT HAD TO BE FIXED FIRST

**Cohort.** Every row in the last 30 days (`2026-06-30 21:15` → `2026-07-30 19:00`) that **reached
the score gate**: it carries a `matrix_breakdown_json` and a proposed direction, and it is not
`htf_blocked` (whose stored breakdown is penalised by −10 and would corrupt the distribution).

```
below_threshold      594      executed             27
ai_skipped           829      failed                2
risk_halt             39      claude_unavailable     1
virt_cap_blocked      39     ─────────────────────────
                             TOTAL               1531     (TREND 630 · FLAT 901)
```

`context_recorded` (1651), `trend_set/reset`, `confirm_recorded` and every `exit_*` status carry no
breakdown and never reach the gate — correctly excluded.

**Regime reconstruction**, per §2b: `market_regime = 'TREND'` iff the stored breakdown's `TREND`
category has `net_direction != NEUTRAL` (`signal_matrix.py:404–417`, verbatim).

### 🔴 THE VALIDATION COUNT, AND WHY THE FIRST ONE FAILED

My first pass validated the reconstruction the way §2 describes it — recompute the score from the
breakdown, add the stored `macro_gate_penalty`, compare to `confluence_score`. **It matched
645 of 1531 rows. 886 mismatches.** That is not a distribution I would publish, so I stopped and
found out why.

**`confluence_score` is not one quantity. Three different writers put three different numbers in
that one column, depending on which branch the row exits on:**

| path | what lands in `confluence_score` | code |
|---|---|---|
| `below_threshold` | `_gated_score` = **raw + `total_gate_adj`** — what the gate actually compared | `main.py:3695,3700` |
| `risk_halt` | `direction_score` = **raw**, and `macro_gate_penalty` is left **NULL** | `main.py:3797` |
| everything downstream (`ai_skipped`, `virt_cap_blocked`, `executed`, `failed`) | `adj_score` = **raw + weight-engine adjustment**, clipped to ±1.5 | `main.py:3883` |

The third is the one that produced the noise. `weight_engine.py:191–193`, verbatim:

> *"`total_adj` is clipped to [−1.5, +1.5] and added to `direction_score` before storing as
> `confluence_score`. **Never applied to the gate check.**"*

That is why the mismatch vocabulary had a spike at exactly ±1.5 and a long fractional tail
(0.31, 0.34, −0.19, 1.16 …) that no gate adjustment could produce. **A column named
`confluence_score` holds the confluence score the gate used on one branch, the unadjusted score on
another, and a number explicitly documented as never reaching the gate on the third.** This is the
same class as your four labels that do not say what they mean — the fifth instance.

**It does not corrupt the distribution, because the distribution never needed that column.**
`matrix_breakdown_json` is assigned **once**, at `main.py:3678`, before the gate, and the identical
string is written on every branch. The raw score is reconstructed from it directly.

### Validation, stated as counts

| test | result |
|---|---|
| `below_threshold`: reconstructed **raw + `total_gate_adj` == `confluence_score`** | **594 / 594 exact** |
| `risk_halt`: reconstructed **raw == `confluence_score`** | **39 / 39 exact** |
| `executed`: reconstructed **raw == `confluence_score`** | **27 / 27 exact** |
| **TOTAL across the three paths whose column holds a gate quantity** | 🔴 **660 / 660 exact · 0 mismatches** |
| **Regime**: reconstructed vs stored `market_regime` | 🔴 **898 / 898 exact · 0 mismatches** |
| rows storing no regime (reconstruction is the only source) | 633 — all `below_threshold` + `risk_halt` |
| rows storing no `total_gate_adj` (gated not computable) | 39 — all `risk_halt` |

The remaining 871 rows store the weight-engine number and therefore **cannot** validate the
reconstruction. Two independent cross-checks cover them instead:

**Cross-check A — the §1 refusal ledger reproduces.** Splitting the 594 `below_threshold` rows by
reconstructed regime gives **451 FLAT-only · 116 both · 27 TREND**. §1 reported **450 · 116 · 27**
over 593 rows at 19:14. The population grew by exactly one row in the intervening two hours.

**Cross-check B — the reconstruction finds a code boundary it was never told about.** 138 FLAT
events with a gated score below 5.0 passed the gate instead of being refused. Every one of them is
dated **on or before 2026-07-06 09:15**. Commit `db71454` *"enforce FLAT-regime score floor (5.0)"*
landed **2026-07-06 13:54:42**. **After that commit: zero.** The reconstruction locates the
enforcement change to the correct side of the correct commit without being given the date.

**Sign convention.** `total_gate_adj` is signed and directional: **positive helps the proposed
direction**, negative opposes it. Vocabulary on the below_threshold path is discrete —
`{−1.5, −1.0, 0.0, +1.0}`.

---

## 1. TREND — RAW `direction_score`, 0.25 buckets from 2.25

**n = 630 · min 2.25 · max 9.00 · mean 4.619 · median 4.25**

| bucket | n | share | cum n | cum share | |
|---|---:|---:|---:|---:|---|
| [2.25, 2.50) | 23 | 3.65% | 23 | 3.65% | ██ |
| [2.50, 2.75) | **121** | **19.21%** | 144 | 22.86% | ██████████ |
| [2.75, 3.00) | 0 | 0.00% | 144 | 22.86% | 🔴 |
| [3.00, 3.25) | 0 | 0.00% | 144 | 22.86% | 🔴 **THE HOLE** |
| [3.25, 3.50) | 0 | 0.00% | 144 | 22.86% | 🔴 |
| [3.50, 3.75) | 4 | 0.63% | 148 | 23.49% | |
| [3.75, 4.00) | 18 | 2.86% | 166 | 26.35% | █ |
| [4.00, 4.25) | 48 | 7.62% | 214 | 33.97% | ████ |
| [4.25, 4.50) | **116** | **18.41%** | 330 | 52.38% | █████████ |
| [4.50, 4.75) | 22 | 3.49% | 352 | 55.87% | ██ |
| [4.75, 5.00) | 18 | 2.86% | 370 | 58.73% | █ |
| [5.00, 5.25) | 52 | 8.25% | 422 | 66.98% | ████ |
| [5.25, 5.50) | 3 | 0.48% | 425 | 67.46% | |
| [5.50, 5.75) | 17 | 2.70% | 442 | 70.16% | █ |
| [5.75, 6.00) | 7 | 1.11% | 449 | 71.27% | █ |
| [6.00, 6.25) | 59 | 9.37% | 508 | 80.63% | █████ |
| [6.25, 6.50) | 18 | 2.86% | 526 | 83.49% | █ |
| [6.50, 6.75) | 15 | 2.38% | 541 | 85.87% | █ |
| [6.75, 7.00) | 52 | 8.25% | 593 | 94.13% | ████ |
| [7.00, 7.25) | 7 | 1.11% | 600 | 95.24% | █ |
| [7.25, 7.50) | 6 | 0.95% | 606 | 96.19% | |
| [7.50, 7.75) | 14 | 2.22% | 620 | 98.41% | █ |
| [7.75, 8.00) | 4 | 0.63% | 624 | 99.05% | |
| [8.00, 8.50) | 0 | 0.00% | 624 | 99.05% | |
| [8.50, 8.75) | 4 | 0.63% | 628 | 99.68% | |
| [9.00, 9.25) | 2 | 0.32% | 630 | 100.00% | |

🔴 **The distribution is not smooth — it is a comb.** The score is a sum of category contributions
capped at 2.5 each, so it lands on a lattice, and three consecutive quarter-point buckets in the
region under discussion are **empty**. 22.86% of TREND signals sit in `[2.25, 2.75)`, then nothing
until 3.50.

**Consequence, stated plainly: on the raw scale every bar in `(2.75, 3.50]` refuses exactly the
same 144 events.** Raw refusals: `2.5 → 23` · `3.0 → 144` · `3.5 → 144` · `4.0 → 166`.

---

## 2. TREND — GATED score (`raw + total_gate_adj`), the number the gate compares

**n = 598** (excludes the 39 `risk_halt` rows that store no `total_gate_adj`, of which 32 are TREND)
**· min 1.25 · max 8.75 · mean 4.697 · median 4.75**

| bucket | n | share | cum n | cum share | |
|---|---:|---:|---:|---:|---|
| below 2.25 | **28** | 4.68% | 28 | 4.68% | 🔴 does not exist on the raw scale |
| [2.25, 2.50) | 5 | 0.84% | 33 | 5.52% | |
| [2.50, 2.75) | 58 | 9.70% | 91 | 15.22% | █████ |
| [2.75, 3.00) | 3 | 0.50% | 94 | **15.72%** | ← **bar 3.0 cuts here** |
| [3.00, 3.25) | 11 | 1.84% | 105 | 17.56% | █ |
| [3.25, 3.50) | 28 | 4.68% | 133 | **22.24%** | ← **bar 3.5 cuts here** |
| [3.50, 3.75) | 48 | 8.03% | 181 | 30.27% | ████ |
| [3.75, 4.00) | 14 | 2.34% | 195 | **32.61%** | ← **bar 4.0 cuts here** |
| [4.00, 4.25) | 20 | 3.34% | 215 | 35.95% | ██ |
| [4.25, 4.50) | 71 | 11.87% | 286 | **47.83%** | ← **bar 4.5 cuts here** |
| [4.50, 4.75) | 9 | 1.51% | 295 | 49.33% | █ |
| [4.75, 5.00) | 14 | 2.34% | 309 | **51.67%** | ← **bar 5.0 cuts here** |
| [5.00, 5.25) | 69 | 11.54% | 378 | 63.21% | ██████ |
| [5.25, 5.50) | 24 | 4.01% | 402 | 67.22% | ██ |
| [5.50, 5.75) | 21 | 3.51% | 423 | 70.74% | ██ |
| [5.75, 6.00) | 14 | 2.34% | 437 | 73.08% | █ |
| [6.00, 6.25) | 35 | 5.85% | 472 | 78.93% | ███ |
| [6.25, 6.50) | 15 | 2.51% | 487 | 81.44% | █ |
| [6.50, 6.75) | 13 | 2.17% | 500 | 83.61% | █ |
| [6.75, 7.00) | 27 | 4.52% | 527 | 88.13% | ██ |
| [7.00, 7.25) | 23 | 3.85% | 550 | 91.97% | ██ |
| [7.25, 7.50) | 10 | 1.67% | 560 | 93.65% | █ |
| [7.50, 7.75) | 11 | 1.84% | 571 | 95.48% | █ |
| [7.75, 8.00) | 14 | 2.34% | 585 | 97.83% | █ |
| [8.00, 8.25) | 5 | 0.84% | 590 | 98.66% | |
| [8.50, 8.75) | 7 | 1.17% | 597 | 99.83% | █ |
| [8.75, 9.00) | 1 | 0.17% | 598 | 100.00% | |

🔴 **`total_gate_adj` fills the hole and creates a floor below the floor.** The raw minimum is 2.25;
the gated minimum is **1.25**. **28 TREND events sit below 2.25 after the adjustment — a region the
matrix cannot produce.** The macro adjustment moves signals across the bar in both directions, and
it is the only thing that does.

---

## 3. 🔴 THE OPERATIONAL NUMBER

### a) Share of TREND signals reaching the score gate that each bar would refuse

| bar | refused (gated, n=598) | share | **incremental vs today** | refused (raw, n=630) | share |
|---:|---:|---:|---:|---:|---:|
| **2.0** *(today)* | 27 | **4.52%** | — | 0 | 0.00% |
| 2.5 | 33 | 5.52% | +6 (+1.00 pt) | 23 | 3.65% |
| **3.0** | **94** | **15.72%** | **+67 (+11.20 pt)** | 144 | 22.86% |
| 3.5 | 133 | 22.24% | +106 (+17.73 pt) | 144 | 22.86% |
| 4.0 | 195 | 32.61% | +168 (+28.09 pt) | 166 | 26.35% |
| 4.5 | 286 | 47.83% | +259 (+43.31 pt) | 330 | 52.38% |
| 5.0 | 309 | 51.67% | +282 (+47.16 pt) | 370 | 58.73% |

**Per side** (gated, share refused):

| side | n | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 | 4.5 | 5.0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| LONG | 288 | 6.2% | 8.0% | 15.6% | 22.2% | 27.1% | 44.4% | 48.3% |
| SHORT | 310 | 2.9% | 3.2% | 15.8% | 22.3% | 37.7% | **51.0%** | **54.8%** |

The sides track each other closely to 3.5 and diverge above it: at 4.0 the bar refuses 37.7% of
SHORT signals against 27.1% of LONG.

### b) 🔴 Today's bar, decomposed

Bar 2.0 refuses **27 of 598** TREND events (**4.52%**). Of those 27, the number refused on raw
merit — `raw < 2.0` — is **0**. **Every one of the 27 is carried under the bar by
`total_gate_adj`.** §1 established the constant cannot bind on the matrix's own output; this
establishes what the 27 refusals in the ledger actually are.

### c) 🔴 The same question in trades rather than events — 23 TREND entries executed in 30 days

TREND signals arrive at **21.0 per day**; 23 of the 630 became trades. This is the concrete answer
to "cosmetic or drastic":

| bar | refuses | keeps | which `vpos` it removes |
|---:|---:|---:|---|
| 2.5 | **0 / 23** | 23 | — *(minimum gated score among executed TREND entries is 2.50)* |
| **3.0** | **3 / 23 (13.0%)** | **20** | **68, 71, 78** |
| 3.5 | **10 / 23 (43.5%)** | 13 | 62, 68, 71, 72, 74, 77, 78, 79, 80, 85 |
| 4.0 | 11 / 23 (47.8%) | 12 | + 81 |
| 4.5 | 15 / 23 (65.2%) | 8 | + 64, 82, 83, **87** |
| 5.0 | 17 / 23 (73.9%) | 6 | + 69, 70 |

**Read the 3.0 → 3.5 step.** Seven additional trades disappear across a half-point, because five
executed entries sit at a gated score of exactly **3.25** (vpos 62, 72, 74, 77, 85) and two more at
3.00–3.25. That cluster is the single densest point in the executed population.

**Note for the live book:** a bar of **4.5 or above would have refused vpos 87** — the position open
with real money right now, gated 4.25.

### d) The answer

**3.0 is not cosmetic.** It triples the TREND refusal rate (4.52% → 15.72%), refuses 67 more
signals in 30 days (≈2.2/day), and removes 3 of the 23 trades actually taken.

**3.0 is also not drastic.** It keeps 84.3% of TREND flow and 20 of 23 trades. The drastic step is
**3.5** — 10 of 23 trades removed, more than four in ten signals refused — and it costs only half a
point more.

**And 3.0 is the smallest bar that does anything measurable:** 2.5 refuses 6 additional events out
of 598 and **0** additional trades.

---

## 4. 🔴 THE CAPACITY EFFECT — §2's caveat 2, quantified

> *"Refusing a trade is not a no-op — it frees the position cap. Every replay above assumes the
> refused trade simply vanishes."*

**Method.** For each cap refusal: find the position open on that side at that instant
(`virtual_positions`, lifetime overlap), reconstruct **its entry's** gated score, and ask whether
the candidate bar would have refused **the incumbent** — freeing the seat. Then ask the second
question: would the **blocked** signal itself have passed the same bar? Only when both hold does a
refusal convert into a trade that actually happens. TREND incumbents are judged at the candidate
bar; FLAT incumbents at the unchanged 5.0 floor, since raising the TREND bar does not touch them.

### a) 🔴 First, a finding about the sample that changes how "36" should be read

The 36 `concurrent_position_halt` refusals are **not** spread over 30 days. They are:

```
2026-07-29 : 1        2026-07-30 : 35
```

**All 36 occurred in the last 36 hours, and 35 of them were caused by exactly two positions**
— vpos 86 (9 blocks) and vpos 87 (26 blocks, still open). `risk_manager.check_risk` queries the
**exchange**; in the paper era there were no exchange positions, so this gate could not fire at all.
It began firing when the bot went live.

**The 1 unmatched refusal is informative.** Halt `19557`, 2026-07-29 20:10, SHORT: no
`virtual_positions` row was open on that side at that moment (vpos 83 closed 06:28, vpos 85 was
LONG). It was blocked by a SHORT the exchange reported and the DB had no row for — **the naked
position from 2026-07-29.** The cap gate saw it; the book did not.

The paper-era equivalent of this mechanism is **`virt_cap_blocked`** — the same cap enforced against
the DB book, 39 refusals spanning **2026-07-02 → 2026-07-28** across **12 distinct incumbents**.
The two are era-separated and do not overlap. Both are reported below; the paper population is the
one that actually covers the 30 days, and it is the one the n=11 replay cohort lived inside.

### b) LIVE era — `concurrent_position_halt`, n = 36 (35 with an identified incumbent)

Incumbent entry gated scores: **vpos 86 = 5.75** · **vpos 87 = 4.25**.

| bar | incumbent would be refused | share | …**and** the blocked signal itself passes |
|---:|---:|---:|---:|
| 2.5 | **0 / 36** | 0.0% | 0 (0.0%) |
| **3.0** | **0 / 36** | **0.0%** | **0 (0.0%)** |
| 3.5 | **0 / 36** | 0.0% | 0 (0.0%) |
| 4.0 | **0 / 36** | 0.0% | 0 (0.0%) |
| 4.5 | 26 / 36 | 72.2% | 18 (50.0%) |
| 5.0 | 26 / 36 | 72.2% | 17 (47.2%) |

🔴 **Zero, at every bar up to and including 4.0.** Both incumbents scored above 4.0, so no bar in
the range under discussion would have freed a single seat. The effect switches on abruptly at 4.5
**entirely because vpos 87 scored 4.25** — one position, 26 of the 36 blocks. That is an n=1
dependency, not a rate.

### c) PAPER era — `virt_cap_blocked`, n = 39 (31 with an identified incumbent, 12 incumbents)

Incumbent entry gated scores: 2.50, 2.75, 3.00, 3.25 ×3, 3.50 ×2, 4.00, 4.25, 7.75.

| bar | incumbent would be refused | share | …**and** the blocked signal itself passes |
|---:|---:|---:|---:|
| 2.5 | 3 / 39 | 7.7% | 0 (0.0%) |
| **3.0** | **8 / 39** | **20.5%** | **5 (12.8%)** |
| 3.5 | 21 / 39 | 53.8% | 15 (38.5%) |
| 4.0 | 24 / 39 | 61.5% | 15 (38.5%) |
| 4.5 | 30 / 39 | 76.9% | 18 (46.2%) |
| 5.0 | 30 / 39 | 76.9% | 17 (43.6%) |

### d) Combined, n = 75

| bar | incumbent refused | share | **seat freed AND blocked signal passes** | share |
|---:|---:|---:|---:|---:|
| 2.5 | 3 / 75 | 4.0% | **0** | 0.0% |
| **3.0** | **8 / 75** | **10.7%** | **5** | **6.7%** |
| 3.5 | 21 / 75 | 28.0% | 15 | 20.0% |
| 4.0 | 24 / 75 | 32.0% | 15 | 20.0% |
| 4.5 | 56 / 75 | 74.7% | 36 | 48.0% |
| 5.0 | 56 / 75 | 74.7% | 34 | 45.3% |

### e) What this does to the replay

**At bar 3.0 the caveat is small but real: 5 of 75 cap refusals (6.7%) would have become trades**
that the replay silently deleted. The replay remains an upper bound, but the gap it hides at 3.0 is
five signals, not an unbounded unknown.

**At 4.0 it is 15 of 75 (20%), and at 4.5 it is 36 of 75 (48%)** — at which point "the refused trade
simply vanishes" is no longer an approximation worth making. §2's `+3.19R at bar 4.0 over n=5` sits
in a region where one refusal in five would have been replaced by a different trade with an unknown
outcome.

**Limits I will not paper over.** (i) The blocked signals' own `total_gate_adj` is **not stored** on
the `risk_halt` path — for those 36 I used the raw score as the pass/fail test, which slightly
overstates how many blocked signals clear a bar. The incumbent side is unaffected: entries do store
it. (ii) 9 of 75 refusals have no identifiable incumbent and are counted in the denominator but can
never satisfy the numerator — so every share above is a **floor**. (iii) The live sample is 2
positions in 36 hours; the paper sample is 12 positions in 26 days. Only the second generalises,
and it describes a book with $2,000 margin per step, not $30.

---

## 5. FLAT — the same scale, against the 5.0 floor

### a) RAW `direction_score` — n = 901 · min 1.75 · max 7.50 · mean 3.803 · median 3.75

| bucket | n | share | cum n | cum share | |
|---|---:|---:|---:|---:|---|
| [1.75, 2.00) | **137** | **15.21%** | 137 | 15.21% | ████████ |
| [2.00, 2.50) | 0 | 0.00% | 137 | 15.21% | |
| [2.50, 2.75) | 66 | 7.33% | 203 | 22.53% | ████ |
| [2.75, 3.00) | 0 | 0.00% | 203 | 22.53% | |
| [3.00, 3.25) | 21 | 2.33% | 224 | 24.86% | █ |
| [3.25, 3.50) | 0 | 0.00% | 224 | 24.86% | |
| [3.50, 3.75) | **192** | **21.31%** | 416 | 46.17% | ███████████ |
| [3.75, 4.00) | 62 | 6.88% | 478 | 53.05% | ███ |
| [4.00, 4.25) | 10 | 1.11% | 488 | 54.16% | █ |
| [4.25, 4.50) | **211** | **23.42%** | 699 | 77.58% | ████████████ |
| [4.50, 4.75) | 26 | 2.89% | 725 | 80.47% | █ |
| [4.75, 5.00) | 19 | 2.11% | **744** | **82.57%** | ← **the 5.0 floor cuts here** |
| [5.00, 5.25) | 48 | 5.33% | 792 | 87.90% | ███ |
| [5.25, 5.50) | 11 | 1.22% | 803 | 89.12% | █ |
| [5.50, 5.75) | 8 | 0.89% | 811 | 90.01% | |
| [5.75, 6.00) | 4 | 0.44% | 815 | 90.46% | |
| [6.00, 6.25) | 43 | 4.77% | 858 | 95.23% | ██ |
| [6.25, 6.50) | 8 | 0.89% | 866 | 96.12% | |
| [6.50, 6.75) | 1 | 0.11% | 867 | 96.23% | |
| [6.75, 7.00) | 29 | 3.22% | 896 | 99.45% | ██ |
| [7.00, 7.25) | 4 | 0.44% | 900 | 99.89% | |
| [7.50, 7.75) | 1 | 0.11% | 901 | 100.00% | |

**The FLAT raw minimum is 1.75** — this is the population §1 identified as the only place where
`raw < 2.0` occurs at all (137 events, 15.21%), and it is judged at 5.0, not 2.0.

### b) GATED score — n = 894 (excludes 7 `risk_halt` FLAT rows) · min 0.75 · max 7.75 · mean 3.798 · median 3.75

| bucket | n | share | cum n | cum share | |
|---|---:|---:|---:|---:|---|
| below 1.75 | 18 | 2.01% | 18 | 2.01% | |
| [1.75, 2.00) | 98 | 10.96% | 116 | 12.98% | █████ |
| [2.00, 2.25) | 5 | 0.56% | 121 | 13.53% | |
| [2.50, 2.75) | 69 | 7.72% | 190 | 21.25% | ████ |
| [2.75, 3.00) | 45 | 5.03% | 235 | 26.29% | ███ |
| [3.00, 3.25) | 12 | 1.34% | 247 | 27.63% | █ |
| [3.25, 3.50) | 42 | 4.70% | 289 | 32.33% | ██ |
| [3.50, 3.75) | **156** | **17.45%** | 445 | 49.78% | █████████ |
| [3.75, 4.00) | 43 | 4.81% | 488 | 54.59% | ██ |
| [4.00, 4.25) | 18 | 2.01% | 506 | 56.60% | █ |
| [4.25, 4.50) | **126** | **14.09%** | 632 | 70.69% | ███████ |
| [4.50, 4.75) | 54 | 6.04% | 686 | 76.73% | ███ |
| [4.75, 5.00) | 19 | 2.13% | **705** | **78.86%** | ← **the 5.0 floor cuts here** |
| [5.00, 5.25) | 49 | 5.48% | 754 | 84.34% | ███ |
| [5.25, 5.50) | 52 | 5.82% | 805 | 90.04% | ███ |
| [5.50, 5.75) | 11 | 1.23% | 816 | 91.28% | █ |
| [5.75, 6.00) | 7 | 0.78% | 823 | 92.06% | |
| [6.00, 6.25) | 32 | 3.58% | 855 | 95.64% | ██ |
| [6.25, 6.50) | 2 | 0.22% | 857 | 95.86% | |
| [6.75, 7.00) | 20 | 2.24% | 877 | 98.10% | █ |
| [7.00, 7.25) | 6 | 0.67% | 883 | 98.77% | |
| [7.25, 7.50) | 3 | 0.34% | 886 | 99.11% | |
| [7.50, 7.75) | 1 | 0.11% | 887 | 99.22% | |
| [7.75, 8.00) | 7 | 0.78% | 894 | 100.00% | |

### c) Both gates on one scale

| bar | FLAT refused (n=894) | share | TREND refused (n=598) | share |
|---:|---:|---:|---:|---:|
| 2.0 | 116 | 12.98% | **27** ← *TREND bar today* | **4.52%** |
| 2.5 | 121 | 13.53% | 33 | 5.52% |
| 3.0 | 235 | 26.29% | 94 | 15.72% |
| 3.5 | 289 | 32.33% | 133 | 22.24% |
| 4.0 | 488 | 54.59% | 195 | 32.61% |
| 4.5 | 632 | 70.69% | 286 | 47.83% |
| **5.0** | **705** ← *FLAT floor today* | **78.86%** | 309 | 51.67% |
| 5.5 | 805 | 90.04% | — | — |
| 6.0 | 823 | 92.06% | — | — |

🔴 **The two gates are not comparable in severity by a factor of seventeen.** The FLAT floor refuses
**78.86%** of the events it judges; the TREND bar refuses **4.52%**. Same column, same scale, same
30 days.

**And the FLAT population is genuinely lower-scoring**, not merely harshly judged: FLAT median 3.75
against TREND median 4.75, FLAT mean 3.80 against TREND 4.70. But the gap in refusal rate (74
percentage points) is far larger than the gap in the underlying distribution (one point of median).

**Era split at `db71454`** (FLAT floor enforced 2026-07-06 13:54:42) — the shape is stable, so the
30-day FLAT distribution is not an artefact of the rule change:

| window | n | mean | median | share below 5.0 |
|---|---:|---:|---:|---:|
| pre-floor (5.0 not in force) | 201 | 3.92 | 3.75 | 77.1% |
| post-floor (5.0 in force) | 693 | 3.76 | 3.50 | 79.4% |

**A note on where raising the FLAT floor would land**, carried over from §2b without re-arguing it:
the band the floor already refuses most heavily is 3.0–4.0, and §2b measured that band's skip-drift
at **+0.463%** over 24h — the band whose refusals looked most costly. Nothing in this report
changes that number; it is stated so the FLAT column above is not read in isolation.

---

## WHAT I DID NOT DO

- **Nothing was changed.** Read-only, as asked. No code, no config, no commit. `git status` clean at
  publication, HEAD unchanged at `1161802`, service not restarted.
- **No recommendation.** §3d says whether 3.0 is cosmetic or drastic, in volume. It does not say
  what the bar should be.
- **No outcomes.** PnL, R and win rate are excluded from §1–§3 and §5 by instruction. §4 uses
  outcomes nowhere — only scores and cap occupancy. The one outcome-derived number quoted (the
  +0.463% skip-drift in §5) is carried verbatim from the 19:14 report and is flagged as such.
- **I did not fix the `confluence_score` polysemy** found in §0. It is recorded, not patched.
- **The `total_gate_adj` of blocked signals on the `risk_halt` path is not stored** and I did not
  reconstruct it from the macro history — §4e states where that weakens the numbers.
- **`htf_blocked` (4,080 rows) is excluded throughout** because its stored breakdown carries the
  −10 cascade penalty. Those signals never reached the score gate, so no bar could have affected
  them.
