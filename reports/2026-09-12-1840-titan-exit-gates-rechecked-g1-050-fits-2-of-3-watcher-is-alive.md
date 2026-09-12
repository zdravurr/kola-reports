# Titan — three exit gates, replayed again from scratch: **no gate qualifies**. But the 18:10 report got the one that matters wrong: **G1@0.50 blocks 2 of 3 canon closes, both of them losses**. That makes it a rule fitted to two trades, and it is rejected. Also: **the 14:59:35 watcher is NOT dead**

**2026-09-12 18:40 UTC · commit `f16c271` · Titan LIVE REAL MONEY · READ-ONLY PASS · nothing proposed, nothing applied · Mercury-SOL NOT TOUCHED**

---

## 🔴 n FIRST, AND THE MULTIPLICITY CORRECTION, BEFORE ANY NUMBER

**Declared tests: 7 gate variants × 2 populations = 14 cells. Bonferroni α = 0.05 / 14 = 0.003571.**
(G1@0.25 and G1@0.35 block the same set everywhere, so 12 cells are distinct and α = 0.004167. That changes
nothing, because no cell reaches even the uncorrected 0.05.)

| population | resolved `ai_exit` closes | most any gate blocks | smallest two-sided sign-test p that size allows | reaches 0.05? | reaches 0.003571? |
|---|---|---|---|---|---|
| **canon (vpos ≥ 101)** | **3** | 3 | **0.250** | **no** | **no** |
| pre-2026-08-30 (vpos 87–98), **NOT POOLED** | 10 | 8 | 0.0078 | only in principle | **no** |
| **under the CURRENT prompt (after 2026-09-12 14:58:32)** | **0** | 0 | — | — | — |

🔴 **WITH 3 AND 10, NOTHING RANKS.** The floors above depend only on group size and were fixed before
the data was read. **The best p actually observed in all 14 cells is 0.500** (G1@0.50 on canon, 2 of 2
blocked closes were losses). Nothing below is a finding. It is a description of what a rule would have
done to 13 trades.

---

## WHAT YOU ASKED, ANSWERED FIRST

1. **`openitems_guard` EXIT=0**, run first. A non-zero exit would have stopped this pass.
2. 🔴 **This brief was already carried out once, at 18:10** (delivered 17:59:10, Telegram message 12461,
   8 985 chars). I redid the whole thing from the database and fresh bars, **reusing only the calibrated
   counterfactual stand**. **Five of that report's claims are materially wrong, three of them caused by one rounding error** (§0). The table below
   replaces its table.
3. 🔴 **THE HEADLINE, CORRECTED. G1@0.50 blocks vpos 101 AND vpos 105.** Both are canon losses. It does
   not block vpos 104. On canon, **it keeps the win, drops both losses and blocks nothing that was right:
   +0.9358 R / +$1.83**. The 18:10 report said it blocks 101 only (+0.1553 R). The error came from the
   prompt's rounding: vpos 105's MFE prints as `+0.50R`, but its true value is **+0.4971R**, which is below
   0.50. I confirmed that two ways: from the row's own `water_mark`, and from `position_excursion_samples`
   taken **before** the decision.
4. 🔴 **G1@0.50 IS EXACTLY THE CASE YOU TOLD ME TO REJECT. It looks good only because it blocks 2 of 3.**
   It changes **2 canon closes** (below your threshold of ≥ 4) and was **best of five** declared values. In
   the only other population it **blocks 3 of the 6 never-armed wins** (90, 93, 97), and its +1.4317 R
   there **goes to −0.2257 R if you drop one trade, vpos 96**. Its canon result also rests on assuming the
   advisor stays silent after the gate lifts: on vpos 105 the gate lifts at 09-10 11:47, and the
   counterfactual needs **4 more hourly holds** after that (§2g). **It is fitted, and it is rejected.**
5. 🔴 **G2 blocks 101, 104 and 105: all three canon closes, and no other close in the record.** It saves
   both losses and gives back **vpos 104, +1.6791 R**. Net **−0.7433 R / −$0.47**, which wipes out the
   whole canon ledger. **It is a rule fitted to 3 of 3.**
6. 🔴 **G3 = G2 plus vpos 89.** Over all 68 close verdicts the two differ by exactly one row (`trades
   20097`). **G3 blocks both known saves, vpos 104 (+1.6791 R) and vpos 89 (+0.7418 R).**
7. 🔴 **G1@0.75, G2 and G3 are identical on canon** (each blocks {101, 104, 105}). **G1@0.25 and G1@0.35
   are identical everywhere.** Across seven variants, the canon population can only express **three
   distinct blocked sets**: ∅, {101, 105} and {101, 104, 105}.
8. 🔴 **Which gate blocks the six closes the advisor WON?** **G1@0.75 blocks all six** (87, 90, 91, 93, 97,
   104). G1@0.25/0.35/0.50 block three (90, 93, 97). G1@0.06 blocks one (93). G2 and G3 block 104. **No
   gate keeps every win and drops every loss in either population.**
9. 🔴 **vpos 106 re-checked on bars through 18:19 UTC: still UNRESOLVED.** The stop at 78 301.6 was never
   touched (post-close high 77 473.4). The arm at 75 726.8 was never reached (post-close low 77 093.4).
   **It is in no sum.**
10. 🔴 **All 14 closes predate the 2026-09-12 14:58:32 cohort boundary. Under the wording running now,
    n = 0 for everything in this report.**
11. 🔴 **THE WATCHER ARMED AT 14:59:35 IS ALIVE.** PID **1572660**, parent 1, detached session leader,
    3 h 29 m old at 18:29, currently in `sleep 15`. **The brief, the 17:15 report and the 18:10 report all
    called it dead.** The watcher that actually died is the **14:19:40** one: its output file never got its
    closing line. The `.pyc` item is **still OPEN** (one `stat`, §5).
12. 🔴 **The 18:10 report said the lesson was "RECORDED IN THE CANON". It was not.** `OPEN-ITEMS.md` had
    not been committed since 15:04 (`017d603`), and the `.pyc` item was not in it either. **Both are in
    the canon now** (§5c).
13. **VERDICT: no gate this record supports improves the decision point.** Both options, with their
    numbers, are in §4c. **`EXIT_ADVISOR_DRYRUN` is False and was not flipped. The rule stands at 3 of 10.**

---

## 0. THE GUARD, AND THE REPORT THIS ONE CORRECTS

```
openitems_guard — canon: /mnt/volume_nyc1_1780480650620/kola-reports/reports/OPEN-ITEMS.md
  titan-bot HEAD : f16c271   <- the SUBJECT, this is what is compared
  repo HEAD      : f16c271   (context only, NOT compared)
  watched values : 14
✅ header and current-state table agree with runtime.                        EXIT=0
```

### 0a. 🔴 CORRECTIONS TO `2026-09-12-1810-titan-three-exit-gates-replayed-every-one-blocks-a-close-that-was-right.md`

| # | 18:10 said | the record says | why it matters |
|---|---|---|---|
| **1** | G1@0.50 on canon blocks **{101}**, 1 of 3, **+0.1553 R** | blocks **{101, 105}**, **2 of 3**, **+0.9358 R / +$1.83** | This is the shape you asked for, fitted to two trades. 18:10 dismissed it for the wrong reason |
| **2** | G1@0.50 blocks 39 of 68 close verdicts, 8 of 14 closes | **40 of 68, 9 of 14** | same cause |
| **3** | G1@0.50 "total +1.5870 R"; drop vpos 96 → "−0.0705 R" | those figures **POOL canon and pre**, which is forbidden. Separately: **canon +0.9358 R (2 blocked), pre +1.4317 R (6 blocked)**; drop 96 from pre → **−0.2257 R** | the pooled total should not exist |
| **4** | the 14:59:35 watcher "is dead" | **alive, PID 1572660** (§5a) | a claim about a process made without checking the process |
| **5** | lesson "RECORDED IN THE CANON"; item "stays open in OPEN-ITEMS.md" | **neither was ever written** to `OPEN-ITEMS.md` | the same class the lesson describes |
| 6 | "No consultation has an MFE in [+0.25, +0.35)" | **7 consultations do, all holds.** No *close verdict* does, so the degeneracy still holds | wording |
| 7 | "no row sits exactly at +0.00R unrealised" | **7 rows print `+0.00`** (all holds) and **6 print `−0.00`** (5 holds + vpos 93's close) | no close changes |
| 8 | "the renderer emits the true sign" | **not for an exact zero on a SHORT.** `(0.0)·(−1.0)` is IEEE `−0.0` and prints `−0.00`. vpos 93's MFE **is exactly −0.0** (water_mark == fill). Its UR is truly negative: Now 64 193.0 vs entry 64 192.9, **−0.0002 R** | G3 misses blocking vpos 93, a +1.0004 R win, **by one 0.1 price tick** |
| 9 | "waiting to 10 means 10 closes of the new prompt, ≈ 33 days" | canon `§0.ARMLEAD`: **the rule is UNAFFECTED, 3 RESOLVED of 10, 7 to go ≈ 23–25 days** plus resolution lag | the waiting time was overstated by 8–10 days |
| 10 | flipping DRYRUN "costs nothing to reverse" | `EXIT_ADVISOR_DRYRUN` is loaded by `from config import (…)` (`main.py:543`, `virtual_trader.py:106`), so **it only takes effect on a restart, in both directions** | a flip is a live-money restart, not a toggle |
| 11 | "smallest blocked set with a uniform sign is size 0" | only if you pool. **On canon, G1@0.50's set {101, 105} is all losses** | same cause as #1 |
| 12 | on canon only G2 ≡ G3 | **G1@0.75 ≡ G2 ≡ G3 on canon** | three variants, one outcome |

**What 18:10 got right and this pass reproduces to the digit:** the calibration, every G1@0.06 / 0.25 /
0.35 / 0.75, G2 and G3 figure per population, the 68-verdict counts for every gate except G1@0.50, the
G2/G3 one-row difference, and vpos 106 unresolved.

---

## 1. THE THREE GATES — STATED BEFORE THE NUMBERS

A gate does one thing: it **forbids a `close` verdict**. It never forces a close and never touches a
`hold`. A blocked position stays open and runs to its trail or its stop.

### 1a. G1 — MINIMUM PROGRESS

> **G1(f): block the close iff `ctx['mfe_r'] < f`.** At `mfe_r == f` the close is allowed. The arm is at
> +1.00R, so `f` is the fraction of the arm the position must reach.

🔴 **THE CANDIDATE SET IS {0.06, 0.25, 0.35, 0.50, 0.75}, THE SAME SET THE 18:10 PASS DECLARED BEFORE ITS
NUMBERS, KEPT UNCHANGED.** It comes from §3b's own MFE distribution: its two medians (**0.06** canon,
**0.35** whole record) and the three interior bin edges of its table (**0.25, 0.50, 0.75**). I had already
seen 18:10's results when I sat down, so **choosing a different set now would be exactly the sweep you
forbade.** **I did not sweep for the best value.** With five values, one of them is best by construction.

### 1b. G2 — NO CLOSING A WINNER BEFORE THE ARM

> **G2: block the close iff `ctx['upnl_r'] > 0` AND `ctx['trail_armed'] is not True`.**

* **The zero line: strictly greater than zero.** At `upnl_r == 0.0`, including IEEE `−0.0`, **G2 does NOT
  block**. A flat position may be closed.
* **Unreadable armed state (`None`) counts as not armed**, so a positive position stays blocked. One row in
  the record has that state (`28528`). It is a hold and also has no `upnl_r`, so it cannot matter.
* **`upnl_r` is before the closing fee.** vpos 105 realised **−0.0136 R** after a **0.076 R** fee, but the
  advisor was looking at **`Unrealised: +0.07R`**. G2 reads +0.07 and blocks. This is why the brief's
  "vpos 105 closed at −0.01R" still falls inside G2.

### 1c. G3 — LOSERS ONLY

> **G3: allow the close only iff `ctx['upnl_r'] < 0`**, i.e. block iff `upnl_r >= 0`.

* **At exactly 0.00R, G3 BLOCKS.** Zero is not under water. On this record that is one tick away from
  mattering: vpos 93 was at −0.0002 R (correction #8).

### 1d. 🔴 WHAT EACH GATE READS, WHERE IT LIVES, AND PROOF THAT IT NEEDS NO FUTURE INFORMATION

| gate | quantity | computed at | from | in the stored prompt as | needs the future? |
|---|---|---|---|---|---|
| G1 | `mfe_r` | `main.py:3109` | `(vpos['water_mark'] − fill)·sgn / r_dist`: the running peak **as stored now** | `Peak so far (MFE): ±X.XXR` (`claude_advisor.py:1075`) | **NO** |
| G2, G3 | `upnl_r` | `main.py:3106` | `(last − fill)·sgn / r_dist`, where `last` = `exchange.fetch_ticker()` **on this call** | `Unrealised: ±X.XXR` (`claude_advisor.py:1072`) | **NO** |
| G2 | `trail_armed` | `main.py:3394` | `pending_dca_limits.breakeven_applied`: the state **now** | the protection block (`ARMED` / `NOT ARMED` / unreadable) | **NO** |

All three values are built into `ctx` **before** `consult_for_close_rich(ctx)` is called (`main.py:3602`).
A gate would read the same dict one branch earlier. **None of the three gates needs the outcome.**

🔴 **Two honest limits on reconstructing the gates from the stored prompts:**
* **The prompt prints 2 decimals, but a gate reads the float.** Three close verdicts sit on a printed
  boundary, and **all three can be resolved exactly** from the position's own row: **vpos 105** MFE
  `+0.50` → **0.4971** (G1@0.50 **blocks**); **vpos 106** MFE `+0.06` → **0.0604** (G1@0.06 does **not**
  block; unresolved anyway); **vpos 93** UR `−0.00` → **−0.0002** (G3 does **not** block). For a close
  that happened 1–2 s after its verdict, the row's final `water_mark` equals the value at decision time,
  because a water mark only moves in the position's favour. vpos 105 is also confirmed independently by
  `position_excursion_samples`: peak **0.6555 %** at **22:09:29** = **0.4972 R**, **1 h 37 m before**
  the decision.
* **38 of the 68 close verdicts are from the earliest prompt, which has no protection block.** For those,
  G2's armed term is not in the stored prompt, so it is reconstructed as `MFE ≥ +1.00R`. On the 130
  consultations that *do* print the block, that proxy agrees **130 of 130**. **None of the 38 has
  MFE ≥ 1**, and **all 14 live closes print the block**, so the proxy never touches a close that has
  money attached.

**Parse coverage:** 191 of 191 consultations; 190 matched to exactly one position by side + entry price
+ open window; one unmatched (`28528`, the unreadable-state prompt with `n/a` everywhere, a **hold**).
Wordings: 126 `NOT ARMED`, 60 no block, 4 `ARMED`, 1 unreadable, the same as §3a of the 17:15 report.

---

## 2. THE REPLAY

### 2a. The stand, re-calibrated, on bars fetched **with no API key in the client**

```
canon window : 15 860 1m bars  2026-09-01 18:00 -> 2026-09-12 18:19 UTC   GAPS 0
pre   window : 63 741 1m bars  2026-07-30 12:00 -> 2026-09-12 18:20 UTC   GAPS 0
```

🔴 **CALIBRATION, EXACT:** vpos 101 **−0.1553**, 104 **+1.6791**, 105 **−0.7805**; **Σ canon +0.7433 R /
+$0.4727**; **Σ pre −0.1123 R / −$1.9322**. Every published row reproduces to the digit. The stand is the
17:15 `ledger2.py` (the 14:30 replay plus a read-only handle and a selectable bar file), byte-identical to the
copy the 18:10 pass ran (`diff` empty). Geometry, `bardir`,
fees and arming were not touched.

### 2b. 🔴 THE 14 CLOSING CONSULTATIONS, THE **EXACT** VALUES EACH GATE READS, AND WHAT IT DOES

| vpos | pop | trigger | `upnl_r` | `mfe_r` | armed | Δ R (adv − cf) | advisor | G1@.06 | G1@.25 | G1@.35 | G1@.50 | G1@.75 | G2 | G3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 87 | pre | hourly | −0.36 | +0.6146 | no | +0.6398 | **WON** | · | · | · | · | **B** | · | · |
| 88 | pre | hourly | −0.22 | +0.0761 | no | −0.7939 | lost | · | **B** | **B** | **B** | **B** | · | · |
| 89 | pre | 15m_exit_confirm | +1.50 | +1.6968 | **YES** | +0.7418 | **WON** | · | · | · | · | · | · | 🔴 **B** |
| 90 | pre | hourly | −0.26 | +0.1749 | no | +0.7686 | **WON** | · | **B** | **B** | **B** | **B** | · | · |
| 91 | pre | hourly | −0.40 | +0.6615 | no | +0.6250 | **WON** | · | · | · | · | **B** | · | · |
| 92 | pre | hourly | −0.65 | +0.0005 | no | −1.0025 | lost | **B** | **B** | **B** | **B** | **B** | · | · |
| 93 | pre | hourly | **−0.0002** | **−0.0 exactly** | no | +1.0004 | **WON** | **B** | **B** | **B** | **B** | **B** | · | · *(1 tick)* |
| 96 | pre | hourly | −0.48 | +0.4640 | no | −1.6575 | lost | · | · | · | **B** | **B** | · | · |
| 97 | pre | hourly | −0.74 | +0.1162 | no | +0.2531 | **WON** | · | **B** | **B** | **B** | **B** | · | · |
| 98 | pre | hourly | −0.18 | +0.9291 | no | −0.6873 | lost | · | · | · | · | · | · | · |
| **101** | **canon** | 15m_exit_confirm | **+0.40** | +0.4271 | no | −0.1553 | lost | · | · | · | **B** | **B** | **B** | **B** |
| **104** | **canon** | 15m_exit_confirm | **+0.67** | +0.7208 | no | **+1.6791** | **WON** | · | · | · | · | **B** | 🔴 **B** | 🔴 **B** |
| **105** | **canon** | hourly | **+0.07** | 🔴 **+0.4971** | no | −0.7805 | lost | · | · | · | 🔴 **B** | **B** | **B** | **B** |
| *106* | *canon* | *15m_exit_confirm* | *−0.25* | *+0.0604* | *no* | *UNRESOLVED* | — | · | *B* | *B* | *B* | *B* | · | · |

`B` = blocked. `upnl_r` is shown at the printed precision except where the boundary needed the exact value.
**Advisor WON (Δ > 0), 7:** 87, 89, 90, 91, 93, 97, 104. **Advisor LOST, 6:** 88, 92, 96, 98, 101, 105.
Six of the seven wins are the never-armed counterfactuals. The seventh is vpos 89, the only
already-armed position the advisor ever closed.

### 2c. 🔴 CANON (vpos ≥ 101): n = 3 RESOLVED. No-gate baseline **Σ +0.7433 R / +$0.4727**

**effect = −Σ(Δ R over the blocked closes)**: the change in realised P&L if the gate had been installed.
**Negative means the gate would have cost money.**

| gate | blocks | n changed | **effect R** | **effect $** | ledger after | wins destroyed | losses saved |
|---|---|---|---|---|---|---|---|
| G1@0.06 | — | **0 of 3** | 0.0000 | $0.00 | +0.7433 | — | — |
| G1@0.25 ≡ G1@0.35 | — | **0 of 3** | 0.0000 | $0.00 | +0.7433 | — | — |
| 🔴 **G1@0.50** | **101, 105** | 🔴 **2 of 3** | 🔴 **+0.9358** | 🔴 **+$1.83** | **+1.6791** | **none** | **101, 105** |
| G1@0.75 | 101, 104, 105 | 3 of 3 | −0.7433 | −$0.47 | 0.0000 | **104** | 101, 105 |
| **G2** | 101, 104, 105 | **3 of 3** | **−0.7433** | **−$0.47** | 0.0000 | 🔴 **104 (+1.6791)** | 101, 105 |
| **G3** | 101, 104, 105 | **3 of 3** | **−0.7433** | **−$0.47** | 0.0000 | 🔴 **104 (+1.6791)** | 101, 105 |

### 2d. PRE-2026-08-30 (vpos 87–98): n = 10 RESOLVED. **A DIFFERENT PROMPT. NOT POOLED.** Baseline **Σ −0.1123 R / −$1.9322**

| gate | blocks | n changed | **effect R** | **effect $** | wins destroyed | losses saved |
|---|---|---|---|---|---|---|
| G1@0.06 | 92, 93 | 2 of 10 | +0.0021 | +$0.72 | **93** | 92 |
| G1@0.25 ≡ G1@0.35 | 88, 90, 92, 93, 97 | 5 of 10 | −0.2257 | −$0.13 | **90, 93, 97** | 88, 92 |
| G1@0.50 | 88, 90, 92, 93, 96, 97 | 6 of 10 | +1.4317 | +$3.94 | 🔴 **90, 93, 97** | 88, 92, 96 |
| G1@0.75 | 87, 88, 90, 91, 92, 93, 96, 97 | 8 of 10 | +0.1669 | +$1.92 | 🔴 **87, 90, 91, 93, 97** | 88, 92, 96 |
| **G2** | — | **0 of 10** | 0.0000 | $0.00 | — | — |
| **G3** | **89** | 1 of 10 | **−0.7418** | **−$1.23** | 🔴 **89 (+0.7418)** | — |

R and $ can differ in sign (G1@0.06, G1@0.25) because `initial_risk_usdt` varies from position to
position. Both columns are shown, and neither is a result.

### 2e. 🔴 vpos 106: RE-CHECKED ON THE NEWEST BARS, STILL UNRESOLVED, IN NO SUM

```
closed by the advisor 2026-09-12 09:15:10 at 77 329.8          advisor realised  -0.2963 R
bars after the close   544, through 2026-09-12 18:19 UTC
original stop 78 301.6   post-close HIGH 77 473.4 (14:53)  -> UNTOUCHED, 828.2 away
+1R arm       75 726.8   post-close LOW  77 093.4 (18:17)  -> NOT REACHED, 1 366.6 away
counterfactual  STILL OPEN at 77 105.5  mark -0.1308 R net  (mark-to-market only)
```
**It never armed, the stop is intact, and it counts for nothing.** At the moment, holding would be
0.1656 R *better* than the advisor's close. G1@0.25/0.35/0.50/0.75 would have blocked the close;
G1@0.06 (by 0.0004 R), G2 and G3 would not.

### 2f. 🔴 THE COST SIDE, OVER ALL 191 CONSULTATIONS, STATED AS LOUDLY AS THE BENEFIT

191 consultations: **68 `close`**, 123 `hold`. **No gate touches a hold.** 52 close verdicts are from the
DRYRUN era (before `81875c9`, 2026-07-30 11:32:18) and **16 from the acting era**. Of those 16, **14
closed a position**; `31115` came 2 s after vpos 104 was already closed; `26626` (vpos 95) is an
`armed_exit` row, which records but cannot close.

| gate | **close verdicts blocked, of 68** | share | DRYRUN era (of 52) | acting era (of 16) | **of the 14 that CLOSED** | 🔴 **named saves it blocks** |
|---|---|---|---|---|---|---|
| G1@0.06 | 5 | 7.4 % | 3 | 2 | 2 | — |
| G1@0.25 ≡ G1@0.35 | 27 | 39.7 % | 21 | 6 | 6 | — |
| 🔴 G1@0.50 | **40** | **58.8 %** | 31 | 9 | **9** | — *(but 90, 93, 97)* |
| G1@0.75 | **46** | **67.6 %** | 32 | 14 | **12** | 🔴 **vpos 104 (+1.6791 R)** |
| **G2** | 19 | 27.9 % | 15 | 4 | 3 | 🔴 **vpos 104 (+1.6791 R)** |
| **G3** | 20 | 29.4 % | 15 | 5 | 4 | 🔴 **vpos 104 (+1.6791 R) AND vpos 89 (+0.7418 R)** |

🔴 **G1@0.50 would have forbidden 59 % of every close the advisor ever called, and 9 of the 14 it
actually made. G1@0.75 would have forbidden two thirds. Those are not adjustments. They are a different
bot.**

### 2g. 🔴 WHAT THE COUNTERFACTUAL ASSUMES, MEASURED RATHER THAN WAVED AT

The stand holds a blocked position to its trail or stop, **as if the advisor never spoke again**. In the
real bot the hourly consultation keeps running, and **the gate lifts as soon as its own condition stops
holding**. From then on the advisor can close, and this record cannot say what it would have said. I
counted the **hourly** marks between each blocked canon close and its counterfactual exit at which the
gate **would have allowed a close** (15m triggers would add more):

| gate | vpos | hourly marks before cf exit | marks where the gate would allow a close | first allowed |
|---|---|---|---|---|
| any | **101** | **0** (trail fired 60 min after the close) | 0 | — → **the 101 counterfactual needs no later verdict** |
| G1@0.50 | **105** | 15 | **4** | 09-10 11:47, MFE reached +0.56 R, before the 12:38 arm |
| G2 | **105** | 15 | **7** | 09-10 03:47, **under water at −0.13 R** |
| G3 | **105** | 15 | **4** | 09-10 03:47, −0.13 R |
| G2 / G3 | **104** | 6 | **2** | 09-09 10:31, **−0.04 R**, 4 h 40 m before the stop |
| G1@0.75 | **104** | 6 | 6 | 09-09 09:31, MFE +0.82 R |

🔴 **So G1@0.50's +0.7805 R on vpos 105 requires the advisor to hold at 4 more consultations after the
gate lifts. G2's −1.6791 R on vpos 104 requires it to hold twice while under water on the way to the
stop.** Both numbers are what the stand gives, as the brief asked, **but only vpos 101's is free of this
assumption.**

---

## 3. 🔴 THE HONEST ARITHMETIC, BEFORE ANY CONCLUSION

### 3a. HOW MANY CLOSES EACH GATE CHANGES, AND WHICH ARE FITTED

| gate | canon changed | pre changed | fitted? |
|---|---|---|---|
| G1@0.06 | **0 of 3** | 2 of 10 | never touches canon |
| G1@0.25 ≡ G1@0.35 | **0 of 3** | 5 of 10 | never touches canon |
| 🔴 **G1@0.50** | 🔴 **2 of 3** | 6 of 10 | 🔴 **A RULE FITTED TO TWO TRADES.** Canon effect +0.9358 R. Drop 105 → **+0.1553 R**; drop 101 → **+0.7805 R** |
| G1@0.75 | 3 of 3 | 8 of 10 | changes nearly everything; canon −0.7433 R |
| **G2** | 🔴 **3 of 3** | **0 of 10** | 🔴 **the three canon trades turned into a rule**, and the result is negative |
| **G3** | 🔴 **3 of 3** | 1 of 10 | 🔴 the same, plus it destroys vpos 89 |

**Leave-one-out, per population, never pooled:**

| gate | pop | effect | drop the most influential close | what is left |
|---|---|---|---|---|
| G1@0.50 | canon | **+0.9358** | vpos 105 (+0.7805) | **+0.1553** |
| G1@0.50 | pre | **+1.4317** | vpos 96 (+1.6575) | 🔴 **−0.2257** |
| G1@0.75 | canon | −0.7433 | vpos 104 (−1.6791) | +0.9358 |
| G1@0.75 | pre | +0.1669 | vpos 96 (+1.6575) | −1.4906 |
| G2 / G3 | canon | −0.7433 | vpos 104 (−1.6791) | +0.9358 |
| G3 | pre | −0.7418 | vpos 89 (−0.7418) | 0.0000 |
| G1@0.25 ≡ .35 | pre | −0.2257 | vpos 92 (+1.0025) | −1.2282 |
| G1@0.06 | pre | +0.0021 | vpos 92 (+1.0025) | −1.0004 |

🔴 **The threshold's position, stated plainly because 18:10 got it wrong.** On canon, **any `f` in
(0.4971, 0.7208] blocks exactly {101, 105}**. That is a range, not a knife-edge. **The declared 0.50 sits
0.0029 R (2.95 price points on vpos 105's R) above its lower end.** Over the same canon-identical range,
the **pre** effect moves from **+1.4317** (f ≤ 0.6146) to **+0.7919** (adds win 87) to **+0.1669**
(adds win 91). **The out-of-population evidence for "G1 around one half" shrinks toward zero across
values that are indistinguishable on canon.** I list this as sensitivity, **not** as a search for a
better f.

### 3b. 🔴 DEGENERACY: WHICH GATES ARE NOT INDEPENDENT

Pairwise |symmetric difference| of blocked sets over **all 68 close verdicts**:

| | G1@.06 | G1@.25 | G1@.35 | G1@.50 | G1@.75 | G2 | G3 |
|---|---|---|---|---|---|---|---|
| **G1@.06** | 0 | 22 | 22 | 35 | 41 | 24 | 25 |
| **G1@.25** | 22 | 0 | 🔴 **0** | 13 | 19 | 44 | 45 |
| **G1@.35** | 22 | 🔴 **0** | 0 | 13 | 19 | 44 | 45 |
| **G1@.50** | 35 | 13 | 13 | 0 | 6 | 37 | 38 |
| **G1@.75** | 41 | 19 | 19 | 6 | 0 | 37 | 38 |
| **G2** | 24 | 44 | 44 | 37 | 37 | 0 | 🔴 **1** |
| **G3** | 25 | 45 | 45 | 38 | 38 | 🔴 **1** | 0 |

* 🔴 **G1@0.25 ≡ G1@0.35 exactly**, on all 68 close verdicts. No close verdict has an MFE in [0.25, 0.35);
  7 holds do. **One gate, not two.**
* 🔴 **G2 and G3 differ by one row in the whole record, `trades 20097` (vpos 89).** They are not
  independent gates. **G3 is G2 plus one +0.7418 R save it throws away.**
* 🔴 **On canon, G1@0.75 ≡ G2 ≡ G3**, and G1@0.06 ≡ G1@0.25 ≡ G1@0.35 ≡ ∅. **Seven variants produce
  three canon outcomes.** On pre, six distinct sets (G2 = ∅).

### 3c. 🔴 THE COHORT BOUNDARY: n IS ZERO

**All 14 closes were taken before 2026-09-12 14:58:32 UTC.** The latest exit consultation of any kind in
the database is **2026-09-12 09:15:09**, and there are **0** after it (queried at 18:22). **Under the
prompt wording running now, every gate here has been replayed against zero observations of the current
bot.**

### 3d. 🔴 BONFERRONI, DECLARED IN THE HEADER, APPLIED HERE

α = 0.05 / 14 = **0.003571**. Sign test: among the blocked resolved closes, how many were advisor losses
(the gate helped) versus wins (the gate hurt), two-sided.

| gate | pop | blocked n | floor p | **observed p** | ≤ 0.05? | ≤ 0.003571? |
|---|---|---|---|---|---|---|
| G1@0.06 | canon | 0 | — | — | no | no |
| G1@0.06 | pre | 2 | 0.5000 | 1.0000 | no | no |
| G1@0.25 | canon | 0 | — | — | no | no |
| G1@0.25 | pre | 5 | 0.0625 | 1.0000 | no | no |
| G1@0.35 | canon | 0 | — | — | no | no |
| G1@0.35 | pre | 5 | 0.0625 | 1.0000 | no | no |
| 🔴 **G1@0.50** | **canon** | **2** | **0.5000** | 🔴 **0.5000** | **no** | **no** |
| G1@0.50 | pre | 6 | 0.0313 | 1.0000 | no | no |
| G1@0.75 | canon | 3 | 0.2500 | 1.0000 | no | no |
| G1@0.75 | pre | 8 | 0.0078 | 0.7266 | no | no |
| G2 | canon | 3 | 0.2500 | 1.0000 | no | no |
| G2 | pre | 0 | — | — | no | no |
| G3 | canon | 3 | 0.2500 | 1.0000 | no | no |
| G3 | pre | 1 | 1.0000 | 1.0000 | no | no |

🔴 **G1@0.50 on canon reaches the lowest p a sample of two can reach, 0.500, and that is still ten times
0.05 and 140 times the corrected α.** Two losses out of two blocked is the best result two trades can
produce, **and it means nothing.**

---

## 4. 🔴 VERDICT — DECISION-SHAPED

### 4a. Your first criterion: keeps the wins, drops the losses, blocks nothing right, changes ≥ 4 closes

**No gate meets it.** The closest is **G1@0.50 on canon**: it keeps the win, drops both losses and blocks
nothing that was right, **but it changes 2 closes, not ≥ 4**. In the only other population it **blocks
3 closes that were right** (90, 93, 97). Every other variant blocks a win in the canon population, or
changes nothing there.

### 4b. 🔴 Your second criterion: "looks good only because it blocks 2 of 3". **That is G1@0.50. It is fitted and it is rejected.**

* It changes **2 of 3** canon closes. That is a rule fitted to two trades, as you defined it.
* It is the **best of five** declared values, and one of five is best by construction.
* Its canon sign test gives **p = 0.500**, the best two trades can give.
* Out of population it **destroys 3 of 6 never-armed wins**, and its pre result **turns negative if you
  drop one trade** (vpos 96).
* Its canon saving on vpos 105 **needs the advisor to hold at 4 more consultations** after the gate lifts.
* The 18:10 pass rejected it for the wrong reason (one trade). **The right reason is two trades, and the
  conclusion is the same.**

**G2 and G3 are rejected too:** each changes 3 of 3 canon closes, gives back vpos 104, and ends at
**−0.7433 R / −$0.47**. G3 also discards vpos 89.

### 4c. 🔴 NOTHING WORKS. THE HONEST POSITION, BOTH SIDES, WITH NUMBERS

**No rule this record supports can improve the advisor's decision point.** The reason is the §3b fact
from 17:15: **184 of 191 consultations, and 32 of 32 in canon, judge an unprotected position (canon
median MFE +0.06R, maximum +0.72R).** Every gate built from what is known at that moment (progress, sign,
protection) cuts the same population, and **wins and losses land on both sides of every cut**. The one
cut that separated the canon trio did it with two trades, and its only out-of-sample test was a
different prompt, where it destroyed three wins.

| | **A. LEAVE IT RUNNING to 10 resolved closes** | **B. FLIP `EXIT_ADVISOR_DRYRUN` → True** |
|---|---|---|
| **what it is** | the rule you wrote (`§0.EXIT-ADVISOR-RULE`): at 10, flip if Σ Δ < 0; if not, review again at 20 | the gate that blocks **all** closes. The advisor keeps consulting and recording; nothing acts |
| **the case for it** | The ledger is **+0.7433 R / +$0.47 over canon (n=3)**. Nothing in this pass refutes the advisor. It refutes the **gates**. | Its **whole decision population is blind**: 32 of 32 canon consultations came before the one fact that decides the outcome (will it arm?) could be known. **12 of 13 resolved closes follow that fact.** No rule built from what it can see separates its wins from its losses. |
| **on this record** | advisor vs holding: canon **1 win / 2 losses, Σ +0.7433 R / +$0.47**, sign p = 1.000; pre **6 / 4, Σ −0.1123 R / −$1.93**, sign p = 0.754. **Two figures, never summed.** | the flip's effect is the negative of those: canon **−0.7433 R / −$0.47**; pre **+0.1123 R / +$1.93**. It gives up **every** save: 104 (+1.6791), 89 (+0.7418), and the five never-armed wins 87, 90, 91, 93, 97 |
| **size of the stake** | mean |Δ| per close: **0.8716 R canon (n=3)**, 0.8170 R pre (n=10). Risk per R across the 13 resolved closes is **$1.08–2.87** (canon $1.37–1.96), so one close moves the ledger by about **$1–2** | the same per-close stake, in the other direction |
| **time** | **7 resolved closes to go ≈ 23–25 days** at the canon's 1 close per 3.26 days, plus each counterfactual's resolution lag (1 h / 6.7 h / 39 h so far; vpos 106 is 9 h and still open) | immediate, **but a restart**: the flag is loaded at import (`main.py:543`, `virtual_trader.py:106`); every flip in either direction is an edit plus a restart, done from flat by standing practice |
| **what it buys** | the 7 closes all fall **after** the 14:58:32 wording boundary, so at 10 the rule will mix 3 old and 7 new, and **the canon already requires that split to be stated next to the sum** | verdicts keep accruing **with no money at risk** (DRYRUN gates *acting* only, `config.py:320`), and the counterfactual becomes the **realised** exit rather than a replay |
| **what the record CANNOT say** | 🔴 **n = 3. Nothing ranks. Smallest attainable p = 0.25.** | 🔴 **The same n.** That it decides **blind** is PROVEN. That this makes it **wrong** is NOT proven, and this pass did not bring that any closer |

🔴 **I am not choosing, and I have not touched anything. `EXIT_ADVISOR_DRYRUN` is `False`, read from
`config` at runtime. Not flipped, not proposed. The rule stands at 3 of 10.**

---

## 5. 🔴 THE WATCHER LESSON, CORRECTED BEFORE IT WAS CLOSED

### 5a. 🔴 THE 14:59:35 WATCHER IS **ALIVE**. THE 14:19:40 ONE IS THE ONE THAT DIED

```
$ pgrep -f 'watch\.sh'   ->  1572660
PID 1572660  PPID 1  ELAPSED 03:29:48  STAT Ss  STARTED Sat Sep 12 14:59:35 2026
  /bin/bash /tmp/claude-0/-root/8cc0273f-…/scratchpad/x/stwatch.sh
  /proc/1572660/exe -> /usr/bin/bash     State: S (sleeping)     child: `sleep 15` (7 s old)
  same PID namespace as this shell (pid:[4026531836] both)
```

* **The 15:20 session's watcher (`stwatch.sh`) is running.** It is a detached session leader (`Ss`)
  re-parented to PID 1, so it **outlived** the session that started it. Its loop is `4000 × sleep 15`, so
  it **will stop on its own at about 2026-09-13 07:40 UTC**, appending `NO IMPORT within the window` to
  a file in a dead session's `/tmp` scratchpad **that nobody is told to read**. It only runs `stat` and
  reads a 16-byte header, so it can change nothing. **Left untouched, as the read-only brief requires.**
* **The 14:30 session's watcher (`pycwatch.sh`, armed 14:19:40) is dead.** It is not in the process
  table, and its output file holds **only its start line**. Its window was `340 × sleep 10`, which ends by
  about 15:17 and would have appended `NO IMPORT within window`. That line is missing, so **it was killed
  before its window ended**, most likely when its session ended.
* 🔴 **The 17:15 report wrote "`ps` shows no watcher process", the 18:10 report repeated "is dead", and
  the brief took both on trust.** The process was there, so whatever `ps` query 17:15 ran did not find it.
  The report does not show the query, and I am not going to guess what it was. The other evidence both
  reports gave is a stale output file.
  **A stale output file means nothing has been written, not that the writer is dead.** This is the
  `mail_watch "DEAD 64 m"` class of 2026-08-31 (the daemon was alive for 3 days; the judge had read a
  file's mtime).

### 5b. THE ITEM'S STATUS, FROM ONE `stat`. NO WATCHER NEEDED. **STILL OPEN.**

```
$ stat -c '%n  mtime=%y  size=%s' signal_tiers.py __pycache__/signal_tiers.cpython-312.pyc
signal_tiers.py                            mtime=2026-09-12 14:15:53.435775912 +0000  size=23584
__pycache__/signal_tiers.cpython-312.pyc   mtime=2026-08-04 15:07:11.339529860 +0000  size=16950
```
**The `.pyc` is older than the source it would have to be compiled from, so it has not been regenerated
and `signal_tiers` has not been imported since the 14:18 apply. THE ITEM IS OPEN.** (For corroboration,
the 16-byte header was read with bytecode writing off: it records source mtime 2026-08-04 15:06:23, size
15 924; header == source **False**; source sha256 `4af4fdba57cfaf84…`.) **Why it has not closed:** no
entry consultation has happened. The last one was `trades 31760`, 2026-09-11 22:00:11. Since the 14:58:32
restart every signal has been stopped before the advisor: `htf_blocked` 24, `ema_envelope_blocked` 18,
`context_recorded` 6, `confirm_recorded` 1, `exit_unarmed_noop` 1. **0 open positions.**

### 5c. 🔴 RECORDED IN THE CANON, THIS TIME ACTUALLY

Committed to `reports/OPEN-ITEMS.md` in the same commit as this report, as **`§0.SESSION-PROMISES`**
(with the `.pyc` item as a tracked OPEN entry and the exact command that closes it) and
**`§0.EXIT-GATES`** (this replay's result, with the corrected G1@0.50 figure, so the 18:10 table does
not become the record). The lesson, as written there:

> **A promise whose keeper is a background process started by a session is not a mechanism.** It fails
> two ways, and **this item has one of each**. *It can die with its session* (14:19:40): the item stays
> open while the record says someone is watching. *It can outlive its session* (14:59:35): it keeps
> running, writes its answer where no future session will look, and expires on its own schedule.
> **Either way the promise is kept by nobody.** Worse, a process nobody owns gets described by guesswork:
> two reports called a live process dead based on a stale file.
>
> **This is the same class as the book-gate review that went unchecked for three weeks: reported as
> arranged, never arranged.** A mechanism outlives the session that set it up and delivers to someone who
> will actually be there: a cron entry that reports, a contract test, a guard the next session must run,
> **a line in this file**. **Where a persistent artefact can answer the question on demand (here, the
> `.pyc` mtime), write down which artefact to read and the one command that reads it. Arming a watcher is
> strictly worse:** it adds a way to fail and buys nothing. **Never state that a process is alive or
> dead without `pgrep` / `/proc`.**

A matching class entry was added to the session memory index, next to the `mail_watch` entry.

---

## CONTROLS — READ-ONLY, PROVEN RATHER THAN ASSERTED

| | |
|---|---|
| `openitems_guard` | **EXIT=0** first (18:18) · **EXIT=0** at 18:32 · **EXIT=0** after the canon write (18:38) |
| Titan DB | every handle `file:/root/titan-bot/trades.db?mode=ro` + `PRAGMA query_only=1`, **read back as 1**. **No `-wal`, `-shm` or `-journal` file exists** |
| writes / orders / restarts | **NONE** to Titan. Journal lines since session start (18:16) matching `EXIT-ADVISOR\|ORDER\|CLOSE\|RECONCILE\|BREAKEVEN\|TRAIL\|error\|Traceback`: ****0**** |
| `titan.service` | `active`, **MainPID 1572470**, **NRestarts 0**, start **2026-09-12 14:58:32 UTC**. At session start (18:21) **and** end (18:38): **identical**: MainPID 1572470, NRestarts 0 |
| open positions | **0** (74 `closed` + 6 `archived_pre_geometry_fix`); `exit_pending` 0, `breakeven_jobs` 0 |
| `EXIT_ADVISOR_DRYRUN` | **False**, read from `config` at runtime. **NOT FLIPPED** |
| **book-gate counter** | 🔴 **22 of 200, UNTOUCHED**: 22 rows with book-gate columns, latest `trades 31760` (2026-09-11 22:00:11), **0 refusals**, the same as the 14:30, 15:20, 17:15 and 18:10 readings |
| the live watcher | **PID 1572660 left running, not signalled.** It was already running before this session |
| BingX | **public 1m OHLCV only, from a ccxt client created with NO API key**, so nothing in this pass could authenticate to the account |
| git (Titan) | working tree **clean**, `titan-bot/` HEAD **`f16c271`**, no commit |
| git (kola-reports) | one commit: this report + `OPEN-ITEMS.md` (`§0.EXIT-GATES`, `§0.SESSION-PROMISES`); backup `OPEN-ITEMS.md.bak_exitgates_20260912` |
| 🔴 **Mercury-SOL** | 🔴 **NOT TOUCHED.** No file of it was opened, no DB queried, no process signalled, no venue called. **Disclosed in full:** two filesystem-wide `find / -name …` searches (for `openitems_guard.py` and the memory contract) walked every directory on the box, including Mercury-SOL's, reading directory entries only. Beyond that the only look was `systemctl show`: `mercury-sol.service` `active`, **MainPID 1341949, NRestarts 0**, start 2026-09-11 18:26:59 UTC; `mercury-sol-optimizer-listener.service` `active`, **MainPID 3521920, NRestarts 0**. At start (18:21) and end: **identical**: 1341949 / 0 and 3521920 / 0 |
| 🔴 open | the in-process `.pyc` confirmation for `signal_tiers` (§5b), now tracked in the canon as `§0.SESSION-PROMISES` |
