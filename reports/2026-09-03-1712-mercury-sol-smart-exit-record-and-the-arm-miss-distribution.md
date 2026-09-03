# mercury-sol-smart-exit-record-and-the-arm-miss-distribution

_2026-09-03 17:12 UTC_

---

# THE SMART-EXIT DRYRUN RECORD, AND THE ARM-MISS DISTRIBUTION — both books, read-only

**MULTIPLE-COMPARISON DECLARATION (up front, before any number).**
This pass evaluates **two candidate mechanisms** across **four book×era cells** (SOL paper, SOL
live, Titan paper, Titan live). The comparison family as actually executed:

```
smart-exit ΣR vs actual   3 cells with data × {all, LONG, SHORT}        =  9
arm-miss thresholds       4 cells × {<0.05R, <0.10R}                    =  8
regime split (chop/trend) 3 cells                                       =  3
                                                                  FAMILY = 20
Bonferroni α = 0.05 / 20 = 0.0025
```

🔴 **NO SIGNIFICANCE TEST IS RUN IN THIS REPORT, AND NONE COULD PASS.** The largest cell has
**n = 5**. The pre-declared refusal threshold is n = 8. Every cell is below it. What follows is
**descriptive**, plus **two results that are arithmetic identities and therefore valid at n = 1**
— they are marked ⚖️ where they appear. Sign-stability (leave-one-out), a regime split, and an
independent-sample check are reported for each cell **as robustness description, not as
evidence of significance**.

**READ-ONLY.** Mercury-SOL DB opened `file:…?mode=ro`, SELECT only. `config.py`, `trail_arm.py`,
`virtual_trader.py` read **as text** with line citations — never imported. Titan touched only by
the mandated guard and by a `mode=ro` read of its DB and config text. No venue call was needed
this pass. Controls at the foot.

Titan pre-flight `tools/openitems_guard.py` → **exit 0, clean** (11 watched values agree, HEAD
f5d3542).

**Basis:** my own `2026-09-03-1637` vpos 42 post-mortem, §3f (the counterfactual table) and §4a
(the five mechanisms). This report tests whether §3f's two central numbers — BE lock −$0.0068,
trail −$0.1769 — generalise, and whether the smart-exit rule that §4a scored at +0.113R is a
candidate.

---

# PART 1 — THE SMART-EXIT DRYRUN RECORD

## 1a. The rule, verbatim, with its constants

**The constants** (`/mnt/volume_nyc1_1780480650620/mercury-sol/config.py`):

```
config.py:925   SMART_EXIT_DRYRUN_ENABLED    = True
config.py:926   SMART_EXIT_DRYRUN_SAMPLE_SEC = 3600    # hourly re-evaluation cadence per position
config.py:927   SMART_EXIT_DRYRUN_ARM_PCT    = 1.2     # ref: arm giveback only after MFE >= this %
config.py:928   SMART_EXIT_DRYRUN_GB_PCT     = 0.8     # ref: would-exit on giveback >= this % from peak
```

Titan carries the identical four (`/root/titan-bot/config.py:716-719`) — same values, same names.

**The comparison, verbatim** (`virtual_trader.py:1097-1104`):

```python
    fill = float(row['initial_fill_price'])
    fav_now_pct = ((fill - last) / fill if side == 'SHORT'
                   else (last - fill) / fill) * 100.0
    mfe_pct = (abs(water_mark - fill) / fill) * 100.0
    giveback_pct = mfe_pct - fav_now_pct
    armed = 1 if mfe_pct >= SMART_EXIT_DRYRUN_ARM_PCT else 0
    would_exit = 1 if (armed and giveback_pct >= SMART_EXIT_DRYRUN_GB_PCT) else 0
```

**Exactly what it compares.** `mfe_pct` is the peak favourable excursion as a **percentage of the
entry price** — *not* in R, and this matters: 1.2 % of price is a different fraction of 1R for
every position (SOL's 1R runs 2.5–2.8 % of price, so 1.2 % ≈ 0.43–0.48 R). `giveback_pct` is the
peak minus the current favourable move, in the same units. It arms once the peak has been ≥ 1.2 %
and fires the first time the position has handed back ≥ 0.8 percentage points of it.

**Three properties of the implementation that the record cannot be read without.**

1. 🔴 **It is a LOGGER, and config says so in its own words.** `config.py:898`: *"Rows land in
   `smart_exit_dryrun_samples`; ARM/GB below are only the **reference config** for the one-shot
   `[SMART-EXIT-DRYRUN]` journal line."* `config.py:889-891`: *"PURE OBSERVATION — read by NO
   exit/SL/trail/breakeven logic."* The `would_exit` column is arithmetic that a rule *could*
   act on; **no rule has ever been written around it.**
2. **The journal line prints only on the FIRST fire per position** (`virtual_trader.py:1170-1174`,
   `first_fire`), while the DB column is written on **every** hourly sample. The record below is
   taken from the DB, which is complete; the journal is not (see 1b).
3. 🔴 **The cadence is hourly.** The price it names is whatever the once-an-hour poll caught, not
   the price at which the giveback threshold was actually crossed. Every would-exit price below
   therefore carries up to 59 minutes of latency, and its sign is unknown — it may be better or
   worse than the true trigger price. **This is not a tradeable price; it is a sample.**

## 1b. Every would-exit ever logged

🔴 **The journal contains exactly ONE line.** `journalctl -u mercury-sol.service` retains back to
**2026-08-31 10:04** on this box; everything earlier has rotated out. The single surviving line is
vpos 42's, quoted in the 1637 report. **The journal is not the record — the DB is**, and the two
must not be confused:

```
Sep 02 13:42:51 [SMART-EXIT-DRYRUN] would-exit SOL/USDT:USDT SHORT vpos=42 @~98.7400 chop=0
  regime=TREND gap=Expanding peakMFE=1.91% giveback=1.41% oppWall=8.7 imb=0.4279
  adx15=63.19811640987791 flip15=0 (arm=1.2/gb=0.8) — DRYRUN, position untouched
```

**The complete record, from `smart_exit_dryrun_samples`:**

| book | samples | date range | armed rows | would_exit rows | **positions that ever fired** |
|---|---|---|---|---|---|
| **Mercury-SOL** | 440 over 28 positions | 2026-07-08 05:05 → 2026-09-03 12:45 | 136 | 83 | **9** |
| **Titan** | 315 over 40 positions | 2026-07-02 20:50 → 2026-09-01 17:15 | — | 15 | **3** |

**SOL — the nine first-fires** (the fire a rule would have acted on; repeat fires per position in
brackets):

| vpos | book | side | first fire (UTC) | held | price | peak MFE | giveback | fav at fire | entry regime | [repeats] |
|---|---|---|---|---|---|---|---|---|---|---|
| 15 | paper | SHORT | 2026-07-08 17:07 | 12.03 h | 77.26 | 2.93 % | 1.27 % | +1.655 % | TREND | [9] |
| 17 | paper | SHORT | 2026-07-14 00:12 | 21.04 h | 75.11 | 2.33 % | 1.28 % | +1.054 % | TREND | [12] |
| 18 | paper | LONG | 2026-07-15 07:47 | 16.03 h | 77.49 | 1.45 % | 1.42 % | **+0.026 %** | TREND | [25] |
| 19 | paper | SHORT | 2026-07-16 13:26 | 13.02 h | 76.35 | 1.87 % | 0.97 % | +0.896 % | TREND | [1] |
| 21 | paper | LONG | 2026-07-20 00:52 | 18.04 h | 76.37 | 1.35 % | 0.93 % | +0.421 % | TREND | [1] |
| 39 | **LIVE** | LONG | 2026-08-21 04:30 | 5.01 h | 88.87 | 2.58 % | 1.39 % | +1.196 % | FLAT | [3] |
| 40 | **LIVE** | LONG | 2026-08-22 00:15 | 3.01 h | 93.55 | 2.97 % | 1.54 % | +1.431 % | FLAT | [1] |
| 41 | **LIVE** | LONG | 2026-08-27 09:51 | 6.01 h | 104.61 | 4.60 % | 1.07 % | +3.533 % | TREND | [7] |
| 42 | **LIVE** | SHORT | 2026-09-02 13:42 | 16.04 h | 98.74 | 1.91 % | 1.41 % | +0.504 % | TREND | [24] |

**Titan — the three first-fires:**

| vpos | book | side | first fire (UTC) | held | price | peak MFE | giveback | fav at fire |
|---|---|---|---|---|---|---|---|---|
| 71 | paper | LONG | 2026-07-10 14:51 | 13.03 h | 63,995.7 | 1.37 % | 1.05 % | +0.325 % |
| 79 | paper | LONG | 2026-07-21 17:48 | 26.06 h | 66,214.9 | 2.54 % | 1.06 % | +1.472 % |
| 81 | paper | SHORT | 2026-07-24 19:01 | 8.01 h | 64,234.3 | 1.83 % | 0.80 % | +1.030 % |

🔴 **Titan's last would-exit was 2026-07-24. It has fired ZERO times on live money** — all three
of its fires are in its paper era (Titan's live book begins at vpos 86, 2026-07-30, the
`trades.is_virtual` 1→0 boundary). **Titan contributes no live evidence about this rule at all.**

**Four positions armed and never fired** (peak ≥ 1.2 % but giveback never reached 0.8 %):
SOL vpos 25, 29, 30, 38; Titan vpos 68. Three of those four SOL positions are winners
(+1.257 R, +1.355 R, +4.031 R).

## 1c. Would-exit vs actual, per position, at each position's own 1R

**Fee basis, stated because it is not uniform.** SOL's paper era booked fees at
`BYBIT_TAKER_FEE_RATE = 0.00055` (config.py:1197, whose own comment reads *"GEOMETRY ONLY …
Real venue rate: 0.001"*); the live era books the real **0.100 %**. Verified from the ledger:
implied rate is exactly 0.000550 on vpos 15–21 and exactly 0.001000 on vpos 39–42. Titan books
**0.05 %** (BingX, `config.py:207`), verified at exactly 0.000500 on its live rows.

**Both columns below are recomputed on the same basis for each era** — actual and would-exit
alike — so the two are comparable within a cell. Funding is charged in full on the actual and
pro-rated by elapsed time on the counterfactual; it is ≤ $0.02 on every live position and does
not move any figure.

**Mercury-SOL — PAPER era** (taker 0.055 % both legs):

| vpos | side | 1R $ | would-exit | | actual | | **Δ (rule − actual)** |
|---|---|---|---|---|---|---|---|
| | | | price | net $ / R | price | net $ / R | |
| 15 | SHORT | 248.04 | 77.26 | +145.54 / **+0.587 R** | 78.20 | +25.85 / +0.104 R | **+0.483 R** |
| 17 | SHORT | 197.55 | 75.11 | +85.47 / **+0.433 R** | 75.82 | −8.13 / −0.041 R | **+0.474 R** |
| 18 | LONG | 218.01 | 77.49 | −17.41 / **−0.080 R** | 75.74 | −242.93 / −1.114 R | **+1.034 R** |
| 19 | SHORT | 192.10 | 76.35 | +69.65 / **+0.363 R** | 76.27 | +80.05 / +0.417 R | **−0.054 R** |
| 21 | LONG | 118.26 | 76.37 | +22.02 / **+0.186 R** | 76.39 | +24.65 / +0.208 R | **−0.022 R** |

**Mercury-SOL — LIVE era** (taker 0.100 % both legs):

| vpos | side | 1R $ | would-exit | | actual | | **Δ (rule − actual)** |
|---|---|---|---|---|---|---|---|
| | | | price | net $ / R | price | net $ / R | |
| 39 | LONG | 2.354 | 88.87 | +0.9504 / **+0.404 R** | 91.45 | +3.7762 / +1.604 R | 🔴 **−1.200 R** |
| 40 | LONG | 3.040 | 93.55 | +1.1305 / **+0.372 R** | 100.18 | +7.7482 / +2.549 R | 🔴 **−2.177 R** |
| 41 | LONG | 2.988 | 104.61 | +3.0208 / **+1.011 R** | 106.69 | +4.8808 / +1.633 R | 🔴 **−0.623 R** |
| 42 | SHORT | 2.620 | 98.74 | +0.2992 / **+0.114 R** | 101.87 | −2.8381 / −1.083 R | **+1.197 R** |

**Titan — PAPER era** (taker 0.05 % both legs):

| vpos | side | 1R $ | would-exit | | actual | | **Δ** |
|---|---|---|---|---|---|---|---|
| 71 | LONG | 156.48 | 63,995.7 | +22.47 / **+0.144 R** | 63,653.8 | −31.08 / −0.199 R | **+0.342 R** |
| 79 | LONG | 159.36 | 66,214.9 | +137.08 / **+0.860 R** | 65,842.8 | +80.10 / +0.503 R | **+0.358 R** |
| 81 | SHORT | 97.71 | 64,234.3 | +92.99 / **+0.952 R** | 64,367.6 | +72.45 / +0.741 R | **+0.210 R** |

## 1d. 🔴 THE HEADLINE — ΣR and Σ$, per side, per era, never pooled

```
MERCURY-SOL  PAPER  n=5     rule +1.488 R / +$305.27      actual −0.426 R / −$120.52    Δ +1.914 R
   LONG   n=2               rule +0.106 R / +$4.61        actual −0.906 R / −$218.29    Δ +1.012 R
   SHORT  n=3               rule +1.382 R / +$300.66      actual +0.480 R / +$97.77     Δ +0.902 R

🔴 MERCURY-SOL  LIVE  n=4   rule +1.901 R / +$5.40        actual +4.703 R / +$13.57     Δ −2.802 R
   LONG   n=3               rule +1.787 R / +$5.10        actual +5.786 R / +$16.41     Δ −3.999 R
   SHORT  n=1               rule +0.114 R / +$0.30        actual −1.083 R / −$2.84      Δ +1.197 R

TITAN  PAPER  n=3           rule +1.955 R / +$252.54      actual +1.046 R / +$121.48    Δ +0.910 R
TITAN  LIVE   n=0           NO FIRES — no evidence exists
```

🔴 **On the only real money this rule has ever been measurable against, it destroys 2.802 R.**
In dollars: the four live positions it touched actually returned **+$13.57**; under the rule they
would have returned **+$5.40**. It would have removed **$8.17 from a live book that has made
$15.56 in total** — better than half of everything the book has earned.

Both paper cells favour the rule. **The two paper cells and the one live cell are independent
samples of the same rule, and their signs disagree.** That is the independent-sample control the
brief asked for, and the rule fails it: +1.914 R (SOL paper), +0.910 R (Titan paper),
**−2.802 R (SOL live)**. The only sample drawn from real money is the negative one.

**Sign stability under leave-one-out** (description, not a test — every cell is under n = 8):

| cell | Σ Δ | drop-one range | sign stable? |
|---|---|---|---|
| SOL LIVE (n=4) | **−2.802 R** | −0.625 R … −4.000 R | **YES — negative in all four** |
| SOL PAPER (n=5) | +1.914 R | +0.880 R … +1.969 R | yes — positive in all five |
| Titan PAPER (n=3) | +0.910 R | +0.552 R … +0.700 R | yes — positive in all three |

The live cell's sign survives dropping any single position, **including dropping vpos 42**, the
one position the rule would have rescued: without it the damage grows to −4.000 R.

## 1e. 🔴 HOW MANY WOULD IT HAVE CUT SHORT — and the answer disqualifies it

**Every position where the actual outcome BEAT the would-exit, individually:**

| book / era | vpos | side | actual | would-exit | **cost of the rule** | what it cut |
|---|---|---|---|---|---|---|
| 🔴 SOL LIVE | **39** | LONG | **+1.604 R** | +0.404 R | **−1.200 R** | a trail winner, at 5.0 h of a 9.6 h hold |
| 🔴 SOL LIVE | **40** | LONG | **+2.549 R** | +0.372 R | **−2.177 R** | a trail winner, at 3.0 h of a 7.5 h hold |
| 🔴 SOL LIVE | **41** | LONG | **+1.633 R** | +1.011 R | **−0.623 R** | a trail winner, at 6.0 h of a 14.5 h hold |
| SOL paper | 19 | SHORT | +0.417 R | +0.363 R | −0.054 R | an exit-signal winner |
| SOL paper | 21 | LONG | +0.208 R | +0.186 R | −0.022 R | a trail winner |

**Tally, per cell — and this is the disqualifying line:**

```
SOL LIVE   : CAPPED 3 winners,  SAVED 1 loser    -> 3 caps : 1 save
SOL PAPER  : capped 2 winners,  saved 3          -> 2 caps : 3 saves
TITAN PAPER: capped 0,          saved 3          -> 0 caps : 3 saves
```

🔴 **Stated immediately, as instructed: on live money the rule caps winners THREE TIMES for every
ONE loser it saves, and the three it capped are ALL THREE of the live trail winners in the
book.** Mercury-SOL has produced exactly four live trail exits (vpos 30, 38, 39, 40, 41 — five,
of which four are in the sampled era); the smart-exit rule fired on **three of them, every time
in the first half of the hold, every time before the run had finished.** That is not a tail
risk. That is the rule's central behaviour on this book, because the rule arms on a 1.2 % peak —
and on SOL a 1.2 % peak is the *beginning* of a move, not the end of one.

**The mechanism of the failure is structural, not statistical.** `SMART_EXIT_DRYRUN_ARM_PCT` is
1.2 % **of price**. SOL's 1R is 2.5–2.8 % of price, so the rule arms at roughly **0.45 R** — well
below the 0.75 R at which the position's own trail arms. The rule therefore takes control of
every position during the window in which the trail has not yet armed, and hands back its verdict
before the trail ever gets to act. **Every trail winner in this book must pass through the
rule's armed zone on its way up.**

Across all nine SOL fires it capped 5 and saved 4. On the live cell alone it capped 3 and saved 1.
**By the brief's own criterion — "if it caps winners more often than it saves losers, that is
disqualifying regardless of the total" — this candidate is disqualified.** The total agrees
anyway: −2.802 R.

**Regime split** (`is_chop_entry`, the control the brief asked for): the three live caps are
2 FLAT-entry and 1 TREND-entry; the one live save is TREND. The five paper fires are 5/5 TREND.
The eras are not regime-comparable — a further reason the paper cells cannot stand in for the
live one, on top of their fee basis.

## 1f. Does it ever fire on a position that was never in profit?

**No — it cannot, by construction.** `armed` requires `mfe_pct >= 1.2`, i.e. the position must
already have shown a **1.2 % gross favourable excursion**, which is 6× a live round-trip
(0.20 %) and 11× a paper one (0.11 %). Every one of the twelve fires across both books occurred
on a position that had been solidly in profit at some point.

**The split that does matter is the state at the moment of firing:**

```
fired while GROSS-positive                 12 of 12   (100 %)
fired while NET-positive after round-trip  11 of 12   ( 92 %)
fired while net-NEGATIVE                    1 of 12   — SOL vpos 18, fav_now +0.026 % vs 0.11 % round trip
```

So the rule never fires on a position that was never in profit, but it **does** fire on positions
that have already surrendered essentially all of it: vpos 18 fired at +0.026 % favourable — below
the cost of closing. On the live cell the four fires were at +1.196 %, +1.431 %, +3.533 % and
+0.504 % — all genuinely net-positive, and three of the four still ended up capping a winner.

---

# PART 2 — THE ARM-MISS DISTRIBUTION

## 2a. Every closed position: peak MFE, its own arm, the miss or the runway

🔴 **The arm is not one number across this book, and evaluating every position against 0.75 R
would be an anachronism.** Three geometry eras, established from the config and its dated backups:

| era | boundary | arm | trail callback | partial | evidence |
|---|---|---|---|---|---|
| **A** | up to 2026-08-06 | **1.00 R** | 1.00 R | 1/3 ON | `TRAIL_MULT_ATR` was 2.5 == `SL_BUFFER_ATR` (config.py:66-76) |
| **B** | 2026-08-06 → 08-14 | **1.00 R** | 0.75 R | 1/3 ON | P2: `TRAIL_MULT_ATR` 2.5→1.875 (config.py:104); no `TRAIL_ARM_R` yet |
| **C** | from 2026-08-14 ~18:30 | **0.75 R** | 0.75 R | **OFF** | `TRAIL_ARM_R = 0.75` (config.py:231); `PARTIAL_AT_ARM_ENABLED = False` (config.py:312) |

Era boundary verified against the dated backup `config.py.bak_threeitems_20260814_1830`, which
contains `TRAIL_MULT_ATR = 1.875` but **no `TRAIL_ARM_R` line at all** — i.e. it is the
pre-change snapshot. Titan's arm is **1.00 R** in all eras: `TRAIL_ARM_R` is absent from
`/root/titan-bot/config.py` and the +1R arm is hardcoded in both sites (config.py:212, 354, and
its own note at config.py:296-299).

**Mercury-SOL — all 36 closed positions, each against its OWN era's arm:**

| vpos | book | era | arm | peak MFE (R) | armed? | gap to arm | realised | close reason |
|---|---|---|---|---|---|---|---|---|
| 7 | paper | A | 1.00 | 3.0000 | **YES** | +2.0000 | +2.089 | exit_signal |
| 8 | paper | A | 1.00 | 0.0173 | no | −0.9827 | −0.739 | exit_signal |
| 9 | paper | A | 1.00 | 0.3067 | no | −0.6933 | −0.264 | exit_signal |
| 10 | paper | A | 1.00 | 0.0539 | no | −0.9461 | −1.066 | sl |
| 11 | paper | A | 1.00 | 1.7105 | **YES** | +0.7105 | +1.133 | exit_signal |
| 12 | paper | A | 1.00 | 0.4774 | no | −0.5226 | −1.049 | sl |
| 13 | paper | A | 1.00 | 2.3571 | **YES** | +1.3571 | +1.337 | trail |
| 14 | paper | A | 1.00 | 0.0902 | no | −0.9098 | −1.032 | sl |
| 15 | paper | A | 1.00 | 1.1795 | **YES** | +0.1795 | +0.140 | trail |
| 16 | paper | A | 1.00 | 0.1630 | no | −0.8370 | −1.146 | sl |
| 17 | paper | A | 1.00 | 1.1800 | **YES** | +0.1800 | +0.004 | sl |
| 18 | paper | A | 1.00 | 0.8935 | no | **−0.1065** | −1.074 | sl |
| **19** | paper | A | 1.00 | **0.9730** | no | 🔴 **−0.0270** | **+0.463** | exit_signal |
| 20 | paper | A | 1.00 | 0.1594 | no | −0.8406 | −1.124 | sl |
| 21 | paper | A | 1.00 | 1.4444 | **YES** | +0.4444 | +0.285 | trail |
| 22 | paper | A | 1.00 | 0.2867 | no | −0.7133 | −1.064 | sl |
| 23 | paper | A | 1.00 | 0.5254 | no | −0.4746 | −0.577 | exit_signal |
| 24 | paper | A | 1.00 | 0.2531 | no | −0.7469 | −1.050 | sl |
| 25 | paper | A | 1.00 | 1.6712 | **YES** | +0.6712 | +1.257 | trail |
| 26 | paper | A | 1.00 | 0.7234 | no | −0.2766 | −1.085 | sl |
| 27 | paper | A | 1.00 | 0.5851 | no | −0.4149 | −0.660 | sl |
| 28 | paper | B | 1.00 | 0.4898 | no | −0.5102 | −0.153 | exit_signal |
| 29 | **LIVE** | B | 1.00 | 1.2629 | **YES** | +0.2629 | +1.355 | exchange_UNKNOWN |
| 30 | **LIVE** | B | 1.00 | 1.1565 | **YES** | +0.1565 | +0.762 | trail |
| 31 | **LIVE** | B | 1.00 | 0.1333 | no | −0.8667 | −1.155 | sl |
| 32 | **LIVE** | B | 1.00 | 0.5088 | no | −0.4912 | −0.180 | exit_signal |
| 33 | **LIVE** | B | 1.00 | 0.6075 | no | −0.3925 | −0.049 | exit_signal |
| 34 | **LIVE** | B | 1.00 | 0.1193 | no | −0.8807 | −0.643 | sl |
| 35 | **LIVE** | B | 1.00 | 0.1750 | no | −0.8250 | −0.701 | sl |
| 36 | **LIVE** | C | 0.75 | 0.2838 | no | −0.4662 | −0.757 | exchange_market |
| 37 | **LIVE** | C | 0.75 | 0.2286 | no | −0.5214 | −1.226 | sl |
| 38 | **LIVE** | C | 0.75 | 4.9899 | **YES** | +4.2399 | +4.031 | trail |
| 39 | **LIVE** | C | 0.75 | 2.5421 | **YES** | +1.7921 | +1.604 | trail |
| 40 | **LIVE** | C | 0.75 | 3.4243 | **YES** | +2.6743 | +2.549 | trail |
| 41 | **LIVE** | C | 0.75 | 2.5663 | **YES** | +1.8163 | +1.633 | trail |
| **42** | **LIVE** | C | 0.75 | **0.7252** | no | 🔴 **−0.0248** | **−1.083** | sl |

```
SOL PAPER n=22   armed  8 (36 %)   missed 14
SOL LIVE  n=14   armed  6 (43 %)   missed  8
```

**Titan — all 68 closed positions with a usable water mark, arm 1.00 R:**

```
TITAN PAPER n=52  armed 17 (33 %)  missed 35
TITAN LIVE  n=16  armed  3 (19 %)  missed 13
```

## 2b. 🔴 THE QUESTION — how many died within a hair of their own protection?

| cell | n | misses | **miss < 0.05 R** | **miss < 0.10 R** |
|---|---|---|---|---|
| SOL paper | 22 | 14 | **1** — vpos 19 (−0.0270 R) | **1** |
| **SOL live** | 14 | 8 | **1** — vpos 42 (−0.0248 R) | **1** |
| Titan paper | 52 | 35 | **1** — vpos 61 (−0.0333 R) | **3** — +35 (−0.0563), +41 (−0.0921) |
| **Titan live** | 16 | 13 | **0** | **1** — vpos 98 (−0.0709 R) |
| **ALL FOUR CELLS** | **104** | **70** | **3 (2.9 % of all; 4.3 % of misses)** | **6 (5.8 % / 8.6 %)** |

🔴 **The answer is: vpos 42 is not unique, but it is close to it — and the share is small.**
Three positions in 104 across two books and four months died within 0.05 R of their own arm.
Six within 0.10 R. **That is not a structural pattern; it is the thin tail of a distribution
that is overwhelmingly nowhere near the arm.** The modal miss is enormous: of SOL's 22 misses
across both eras, **13 never got past 0.51 R** — half the arm distance — and eight never got past
0.30 R. Positions in this book do not die inches from safety; they die a long way from it.

🔴 **So vpos 42 must be named as what it is: bad luck, in a cell of n = 14 that contains exactly
one such case.** It is the only live SOL position ever to miss by under 0.10 R. One observation
cannot distinguish "the arm is 0.006 R too high" from "a position happened to stop one cent
short", and §2c below shows the distinction would not matter even if it could.

**One anachronism worth recording, because it nearly went into this report.** Measured against a
flat 0.75 R ruler — the current arm applied to the whole history — the near-miss set would have
read *vpos 42 (−0.0248 R) and vpos 26 (−0.0266 R)*. Measured against each position's **own** era
arm it reads *vpos 42 and vpos 19*. **The membership changes completely.** Any future pass that
re-runs this must carry the era table or it will find a different set of near-misses and believe
it has found something.

## 2c. 🔴 The near-misses: what would arming actually have bought?

For each near-miss, the hypothetical is: *the arm triggers exactly at this position's own peak;
what then?* Two exits become available — the breakeven lock at entry ± 0.20 %
(`trail_arm.py:_BE_TARGET_FRAC_ON = 0.0020`) and the trail at
`water_mark × (1 ∓ trail_pct/100)` (`virtual_trader.py:2226`).

| vpos | book | era | miss | actual realised | **BE lock would pay** | **trail would pay** | peak would pay |
|---|---|---|---|---|---|---|---|
| **42** | LIVE | C | −0.0248 R | **−1.083 R** | **+0.0001 R** (+$0.0002) | **−0.084 R** (−$0.221) | +0.650 R (+$1.703) |
| **19** | paper | A | −0.0270 R | **+0.463 R** | +0.047 R (+$9.01) | **−0.066 R** (−$12.59) | +0.916 R (+$176.02) |
| 18 | paper | A | −0.1065 R | −1.074 R | +0.041 R (+$8.98) | −0.176 R (−$38.40) | +0.843 R (+$183.69) |
| 33 | LIVE | B | −0.3925 R | −0.049 R | −0.0001 R (−$0.0002) | −0.290 R (−$0.403) | +0.464 R (+$0.645) |

🔴 **The line closes, exactly as the brief anticipated.**

- **vpos 42**: arming buys **+0.0001 R** on the lock and **−0.084 R** on the trail. It converts a
  −1.083 R loss into a zero and a slightly larger-than-zero cost respectively. The lock is worth
  **two hundredths of a cent**.
- **vpos 19 is the case that settles it.** It missed its arm by 0.027 R — a near-miss every bit as
  tight as vpos 42's — and it **realised +0.463 R anyway**, via the exit-signal path. Had it
  armed, the lock would have paid +0.047 R and the trail **−0.066 R**. 🔴 **Arming would have
  made vpos 19 worse by 0.42–0.53 R.** The near-miss did not cost it anything; it saved it.
- **vpos 33** missed by a wide 0.39 R and still lost only 0.049 R — the trail, had it armed,
  would have paid −0.290 R.

**In three of the four near-miss cases the trail is the worst of the three available exits, and
in the fourth it is second worst.** There is no near-miss in this book where arming would have
been worth more than a few hundredths of R.

## 2d. Both books, each against its own arm

| | Mercury-SOL | Titan |
|---|---|---|
| arm | **0.75 R** (era C; 1.00 R before 2026-08-14) | **1.00 R**, all eras, hardcoded in two sites |
| trail callback | 0.75 R (`TRAIL_MULT_ATR` 1.875 / `SL_BUFFER_ATR` 2.5) | 0.75 R (`TRAIL_MULT_ATR` 1.6875 / `SL_ATR_MULT` 2.25) |
| BE park | entry ± 0.20 % | entry ± 0.20 % (2×0.05 % fees + 0.10 % buffer, config.py:203-208) |
| real taker | **0.100 %** | **0.05 %** |
| ⚖️ **BE lock net value** | **0.20 % − 0.20 % = 0.00 %** | **0.20 % − 0.10 % = +0.10 %** |
| ⚖️ **trail value at the arm** | arm == callback → **≈ 0 gross** | arm 1.00 R − callback 0.75 R → **+0.25 R gross** |
| live armed / live closed | 6 of 14 (43 %) | 3 of 16 (19 %) |
| live miss < 0.05 R | 1 (vpos 42) | 0 |
| smart-exit live fires | 4 | **0** |

🔴 **The two books are not in the same situation and must not be described as if they were.**
Titan's arm sits a full 0.25 R above its callback, so a Titan position that arms at its peak
still has a quarter-R of gross runway; and its 0.05 % venue fee leaves its breakeven lock a real
+0.10 % of notional. **Mercury-SOL has neither margin.** Titan's own config records that it
*measured* SOL's 0.75 R arm on its own book and refused it: *"My own measurement refuted it:
−15.11R on the seventeen against an UPPER-BOUND benefit"* (`/root/titan-bot/config.py:298-300`).

---

# PART 3 — THE HONEST FRAME

## 3a. 🔴 Does vpos 42's counterfactual generalise? — YES, and further than it showed

The 1637 report found the breakeven lock paying −$0.0068 and the trail −$0.1769 on one position.
Recomputed for **every closed position in the SOL book** — "arm exactly at this position's own
peak, then exit at the lock, or at the trail, or at the peak":

**⚖️ THE BREAKEVEN LOCK, LIVE ERA — an identity, not a sample:**

```
vpos   29     30     31     32     33     34     35     36     37     38     39     40     41     42
BE_R  -0.000 -0.000 -0.000 +0.000 -0.000 +0.000 +0.000 +0.000 +0.000 -0.000 -0.000 -0.000 -0.000 +0.000
```

🔴 **Zero. On all fourteen. To three decimals of R, every time.** This is not fourteen
observations that happen to agree — it is one identity observed fourteen times. The lock parks at
entry ± 0.20 %; the round trip at the real 0.100 % taker costs 0.20 %; the difference is
**−0.0002 % of notional**, which `trail_arm.py` states in its own comment: *"gross +0.2000 % −
fees 0.2002 % = NET −0.0002 % of notional. That is a FEE WASH, not the 'small net WIN' this
module's docstring promised."* Valid at n = 1 because it is arithmetic.

**⚖️ AND THE PAPER ERA'S APPARENT VALUE IS A FEE ARTEFACT.** The same computation on the 22 paper
positions gives BE_R of **+0.023 to +0.076 R, median +0.0456 R** — every one positive. The reason
is entirely the fee basis: at the understated 0.055 % the round trip is 0.11 %, so 0.20 % − 0.11 %
= +0.09 % of notional. 🔴 **Every dollar the breakeven lock appears to earn in the paper book is
1.82× understated fees. At real fees it earns exactly nothing.** Any past study that scored the
BE lock on the paper book scored a fee error.

**THE TRAIL, LIVE ERA** — it pays, but only as a function of how far past the arm the peak ran:

| vpos | era | peak MFE | trail would pay | realised |
|---|---|---|---|---|
| 38 | C | 4.990 R | +4.024 R | +4.031 R |
| 40 | C | 3.424 R | +2.526 R | +2.549 R |
| 41 | C | 2.566 R | +1.691 R | +1.633 R |
| 39 | C | 2.542 R | +1.659 R | +1.604 R |
| 29 | B | 1.263 R | +0.620 R | +1.355 R |
| 30 | B | 1.156 R | +0.507 R | +0.762 R |
| 33 | B | 0.607 R | −0.290 R | −0.049 R |
| 32 | B | 0.509 R | −0.374 R | −0.180 R |
| **42** | **C** | **0.725 R** | **−0.084 R** | −1.083 R |
| 36 | C | 0.284 R | −0.675 R | −0.757 R |
| 37 | C | 0.229 R | −0.726 R | −1.226 R |
| 35 | B | 0.175 R | −0.762 R | −0.701 R |
| 31 | B | 0.133 R | −0.767 R | −1.155 R |
| 34 | B | 0.119 R | −0.770 R | −0.643 R |

⚖️ **The trail's payout is `peak − 0.83 R`, to within a few hundredths, on every live row.**
(0.75 R of callback plus ~0.08 R of round-trip fees.) **It crosses zero at a peak of ≈ 0.83 R —
which is ABOVE the 0.75 R arm.** So there is a dead band between 0.75 R and 0.83 R in which a
position arms, the trail takes control, and the trail still exits at a loss. vpos 42's peak of
0.725 R sat just under that band; had it armed it would merely have entered it.

🔴 **VERDICT ON 3a: it generalises, and the statement is stronger than vpos 42 alone allowed.
"The trail would have saved it" is FALSE for every position in this book whose peak is under
0.83 R — which is every position that missed its arm, by definition, plus a slice of those that
made it. The only column in the whole table with real money in it is the peak column.** For the
fourteen live positions the peak column sums to +14.9 R while the trail column sums to +5.6 R and
the lock column sums to 0.0 R.

## 3b. Is there any mechanism in either bot that closes near a peak?

🔴 **No. There is none, in either bot, and the nearest thing to one is switched OFF in both.**

Everything either bot can do to an open position, classified:

| mechanism | book | type | closes near a peak? |
|---|---|---|---|
| Trailing stop | both | **giveback** — 0.75 R behind the running water mark | no, by definition |
| Breakeven lock | both | **giveback** — all the way back to entry | no |
| Smart-exit dryrun | both | **giveback** — 0.8 % behind the peak, a *tighter* giveback | no — same class, smaller number |
| Hourly exit advisor | both | judgment, hourly cadence | not by construction; and it is the thing this pass was told not to consider |
| Armed 1h exit + 15m confirm | both | **event** — needs an opposing structure signal | no |
| Trend-reversal exit | SOL | **event**, `TREND_REVERSAL_EXIT_DRYRUN = True` | no |
| Post-entry recheck | both | first-300-s risk check | no |
| Partial at arm, 1/3 @ 0.75 R | SOL | **LEVEL** — the closest thing that exists | 🔴 **OFF** since 2026-08-14 (config.py:312) |
| LONG partial, 1/3 @ 1.0 R | Titan | **LEVEL** — same idea | 🔴 **OFF** since 2026-08-27 (config.py:308) |
| Fixed 1.0 R target | Titan | **LEVEL** | 🔴 never built — simulated at −58.63 (best of four) and **rejected for tail risk**, config.py:263-268 |

**Every live mechanism in both bots is either a giveback rule or an event rule.** The only
peak-adjacent designs ever considered are *level* rules — realise a fixed fraction at a fixed R —
and both were measured, both were switched off as improvements, and the fixed target was refused
outright: *"a partial surrenders only FRACTION of the excess, while a 1.0R target would cap the
whole trade"* (Titan config.py:262-264). Both switch-offs were **monotone** results — on SOL,
config.py:296 records the partial as *"the ONLY monotone axis"* of a four-axis sweep, better at
every step with less taken.

So the record contains a consistent finding pointing the other way from this report's own
arithmetic: **every measurement this project has made of taking money off near a level has said
take LESS**, while §3a says the only column with money in it is the peak. Those two are not
reconciled by anything in this data, and this report does not reconcile them.

## 3c. 🔴 n, stated honestly, everywhere

| claim | n | rank? |
|---|---|---|
| smart-exit rule beats actual — SOL paper | **5** | ❌ **REFUSED, n < 8** |
| smart-exit rule loses to actual — SOL live | **4** | ❌ **REFUSED, n < 8** |
| smart-exit rule beats actual — Titan paper | **3** | ❌ **REFUSED, n < 8** |
| smart-exit rule — Titan live | **0** | ❌ no data whatsoever |
| the rule caps winners more often than it saves losers (live) | **4** | ❌ refused as a *ranking*; reported as a *count*: 3 caps, 1 save |
| positions dying within 0.05 R of the arm | **3 of 104** | ❌ refused; reported as a share |
| ⚖️ BE lock pays 0.00 R at the real 0.100 % taker | identity | ✅ **valid at n = 1 — arithmetic, not statistics** |
| ⚖️ trail pays `peak − 0.83 R` on SOL era C | identity | ✅ **valid at n = 1** |
| ⚖️ arm == callback in SOL era C ⇒ arming buys ≈ 0 | identity | ✅ **valid at n = 1** |

🔴 **The smart-exit record is a handful of lines: nine fires on SOL across fourteen months of
samples, three on Titan, none of Titan's on live money.** Nothing in Part 1 is rankable. The
descriptive answer is given anyway and it is not close: **on the only real-money sample that
exists, the rule takes 2.802 R off the book and caps three of the book's four live trail winners.**
A candidate does not need n = 8 to be withdrawn when the mechanism of its failure is visible in
the arithmetic — it arms at ~0.45 R, below the 0.75 R at which the position's own trail arms, so
every runner must pass through its armed zone before the trail can act.

**What would make any of this rankable, stated so it is falsifiable rather than open-ended:**
eight live smart-exit fires in one book on one fee basis, with the arm/callback geometry unchanged
across all eight. SOL has four and the geometry last moved on 2026-08-14 — so the earliest this
could be revisited is at eight live fires under era C, i.e. four more than exist today. Paper
fires do not count toward the eight: their fee basis is understated 1.82×, and §3a shows that
error is exactly the size of the effect being measured.

---

# CONTROLS

| control | evidence |
|---|---|
| Titan pre-flight | `tools/openitems_guard.py` → **exit 0**, 11 watched values agree, HEAD f5d3542 |
| **DB read-only** | every connection `sqlite3.connect('file:…?mode=ro', uri=True)` — both `mercury-sol/trades.db` and `titan-bot/trades.db`; SELECT and PRAGMA table_info only; **zero** INSERT/UPDATE/DELETE |
| **cwd outside SOL's tree** | all work in `/tmp/claude-0/…/scratchpad`, `/root`, `/root/titan-bot`; no shell ever entered `/mnt/volume_nyc1_1780480650620/mercury-sol` |
| **config not imported** | `config.py`, `trail_arm.py`, `virtual_trader.py` (SOL) and `config.py` (Titan) read as **text** via `sed`/`grep`, cited by line, plus the dated backup `config.py.bak_threeitems_20260814_1830`. The only Python import of any config was Titan's own guard reading Titan's config, as mandated. |
| **no writes** | no file under either bot's tree opened for writing; no `sudo`, no `chmod`, no editor |
| **no orders** | **no venue call was made at all this pass** — every figure comes from the two ledgers, the two configs, and the journal |
| **service untouched** | `systemctl show` only. Mercury-SOL PID **1196924** (up since 2026-08-24 13:29:27); Titan `titan.service` PID **2610002** (up since 2026-08-31 15:31:49) |
| **NRestarts unchanged** | Mercury-SOL **0 → 0**; Titan **0 → 0** |
| **file hashes identical** | all **33** `*.py` in the SOL tree md5-identical before and after |
| ⚠️ **`trades.db` hashes change on both bots — and they must** | both services are running and writing their own ledgers throughout. An unchanged hash would mean a bot had **stopped**. Every handle this session held was `mode=ro`, which cannot write. |
| Bonferroni | declared in the header: family 20, α = 0.0025 — **no test run**, every cell under the n = 8 refusal threshold |
| sign stability | leave-one-out reported for all three cells with data (1d) — all three stable, and reported as description, not significance |
| regime test | `is_chop_entry` split reported (1e): live caps 2 FLAT / 1 TREND, live save TREND, paper 5/5 TREND — the cells are not regime-comparable |
| independent sample | the paper cells vs the live cell — **the rule's sign does not replicate** (+1.914 R, +0.910 R, **−2.802 R**) |

**Nothing is proposed. Nothing is applied. No flag was changed and no file was edited.**

---

**Bottom line.** The smart-exit giveback rule has fired nine times on Mercury-SOL and three on
Titan, none of Titan's on live money. On the four live SOL positions it touched it would have
turned **+4.703 R into +1.901 R** — it caps **three winners for every one loser it saves**, and
the three it capped are **all three live trail winners in the book**. That is disqualifying by
the brief's own criterion and by the total, and the reason is structural: it arms at ~0.45 R,
below the 0.75 R at which the position's own trail arms, so every runner passes through it first.
The arm-miss line closes too, twice over: only **3 positions in 104** across both books ever died
within 0.05 R of their arm — vpos 42 is the only live one, and it is bad luck, not a pattern —
and it would not have mattered anyway, because **at the real 0.100 % taker Mercury-SOL's
breakeven lock pays exactly 0.00 R on all fourteen live positions and its trail pays
`peak − 0.83 R`, so a position that arms at 0.75 R exits at a loss.** The paper book's apparently
positive lock is 1.82× understated fees and nothing else. **No mechanism in either bot closes near
a peak; the only two ever built that came close are level rules, and both were switched off as
measured improvements.**
