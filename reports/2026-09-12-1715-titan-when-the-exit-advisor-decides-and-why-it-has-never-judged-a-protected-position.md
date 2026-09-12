# Titan — WHEN the exit advisor decides: **4 of 14 closes are TRIGGERED, and every one of them reversed a HOLD taken 13–45 minutes earlier**. And it has judged a position with trailing protection **7 times in 191 consultations — never once in the population the ledger counts**.

**2026-09-12 17:15 UTC · commit `f16c271` · Titan LIVE REAL MONEY · READ-ONLY PASS · Mercury-SOL NOT TOUCHED**

---

## 🔴 n FIRST, BEFORE ANY RESULT — READ THIS BEFORE THE NUMBERS

The question is whether the **trigger type** separates the advisor's outcome. Here is the n it has to work with:

| population | RESOLVED closes | TRIGGERED | PERIODIC |
|---|---|---|---|
| **canon (vpos ≥ 101), the ledger's own population** | **3** | **2** | **1** |
| pre-2026-08-30 (vpos 87–98) — a different prompt, **NOT pooled** | 10 | **1** | 9 |
| under the CURRENT prompt (after the 2026-09-12 14:58:32 boundary) | **0** | **0** | **0** |

🔴 **TWO TRIGGERED AND ONE PERIODIC CANNOT RANK ANYTHING, AND NEITHER CAN ONE AND NINE.** With group
sizes 2 and 1 the **smallest two-sided p-value any rank test can return is 0.667**; with 1 and 9 it is
**0.200**. Both are above 0.05 *before* a Bonferroni correction and *regardless of the data* — that is
arithmetic about the group sizes, not a result. **Nothing below is a finding. Everything below is a
description.** §4 states what n would be needed and how long that is.

---

## WHAT YOU ASKED, ANSWERED FIRST

1. **Four trigger types exist in code; three have ever fired.** `hourly` (periodic, the 3600 s sampler
   cadence), `15m_exit_confirm`, `armed_exit`, and `5m_group_b` — which has produced **0 consultations and
   0 rows in the bot's entire history**. `armed_exit` is **record-only and can never close**: the armed
   mechanism closes regardless of the verdict.
2. 🔴 **Of the 14 live `ai_exit` closes ever: 10 PERIODIC, 4 TRIGGERED.** All four triggered ones are
   `15m_exit_confirm`. Named with vpos, time and R in §1c.
3. 🔴 **Every one of the 4 triggered closes reversed a HOLD taken minutes earlier** — 13.4, 14.9, 44.5 and
   44.6 minutes. **But so did 9 of the 10 periodic closes**, at 60.1 minutes, because that is the cadence.
   **Reversing a hold is not what distinguishes a trigger. The LATENCY is** — triggered median 28.6 min vs
   periodic median 60.1 min.
4. 🔴 **A correction to the brief and to my own 14:30 report: vpos 106 had TWELVE consecutive hourly holds,
   not thirteen** (22:00:36 → 09:01:46), and the **thirteenth** consultation closed it, not the fourteenth.
   The 13-minute gap and everything else about that close stand.
5. 🔴 **CONFIRMED, and sharper than the 15:20 report said.** **4** consultations rendered the trail as
   **ARMED**. Three more (vpos 82, 2026-07-26) were taken on a position that *was* armed but whose prompt
   carried **no protection block at all** — so **7 of 191** consultations judged a protected position and
   **184 judged an unprotected one**. In era C: **0 of 33**. In the canon population: **0 of 32**.
6. 🔴 **WHY: not construction — data.** No gate anywhere excludes an armed position from the advisor.
   The reason is that positions do not get there: across the canon population's 32 consultations the
   **highest MFE ever seen at a decision was +0.72R**, median **+0.06R**. Not one was within reach of the
   +1R arm. §3b proves it from the code and from the prompt's own stored MFE line.
7. 🔴 **NOTHING SEPARATES ON TRIGGER TYPE, and the record leans the OPPOSITE way to the instinct.**
   In the canon population the two TRIGGERED closes are **+1.5238R** together and the one PERIODIC close is
   **−0.7805R**. In the pre-2026-08-30 window the single triggered close is **+0.7418R** and the nine
   periodic ones are **−0.8541R**. **That is 2-vs-1 and 1-vs-9. It ranks nothing in either direction**, and
   I am not going to let it read as support for the opposite claim either.
8. 🔴 **The honest result: 3 resolved closes cannot tell a bad mechanism from variance.** Your instinct
   about a sub-population is **not yet supported by the record**, and the record does not refute it either.
   That is a legitimate outcome and it is not being softened into a hint.
9. **The one thing that DOES track the outcome is not *when* the decision was taken but *whether the
   position was going to arm*.** 12 of the 13 resolved closes obey it: if the counterfactual armed, the
   advisor lost; if it never armed, the advisor won. The single exception is the only already-armed
   position it ever judged. §3d — stated as a description, near-tautological, **not a finding**.
10. **The outstanding `.pyc` item is STILL OPEN.** No entry consultation has occurred; the `signal_tiers`
    bytecode is still the 2026-08-04 build. §5, plainly, with no dressing.

`openitems_guard` **EXIT=0** at the start of this session and **EXIT=0** at the end. Nothing was written,
applied, restarted or proposed.

---

## 0. THE GUARD

```
openitems_guard — canon: /mnt/volume_nyc1_1780480650620/kola-reports/reports/OPEN-ITEMS.md
  titan-bot HEAD : f16c271   <- the SUBJECT, this is what is compared
  repo HEAD      : f16c271   (context only, NOT compared)
  watched values : 14

✅ header and current-state table agree with runtime.                        EXIT=0
```

Run first, as instructed, and **non-zero would have stopped this pass**. It did not.

---

## 1. WHAT TRIGGERS AN EXIT CONSULTATION

### 1a. 🔴 EVERY CALL SITE, QUOTED, WITH LINE NUMBERS

There is exactly **ONE** call to `consult_for_close_rich` in the whole bot:

```
claude_advisor.py:746   def consult_for_close_rich(ctx):
main.py:3602                advice = claude_advisor.consult_for_close_rich(ctx)   <- THE ONLY ONE
```

It is wrapped by `consult_exit_advisor`, and the trigger is an explicit argument:

```
main.py:3570   def consult_exit_advisor(vpos_row, symbol, side, exit_signal_name, trigger):
```

**Four call sites pass a trigger. Three have ever fired.**

**(1) PERIODIC — `hourly`** · `virtual_trader.py:2572-2579`, inside `_process_position`:
```python
2572    if EXIT_ADVISOR_HOURLY:
2573        try:
2574            _st = mgmt_state.get('exit_advisor_last_ts')
2575            _now_ts = datetime.now(timezone.utc).timestamp()
2576            if _st is None or (_now_ts - float(_st)) >= EXIT_ADVISOR_HOURLY_SEC:
2577                import main as _m
2578                _adv = _m.consult_exit_advisor(row, row['symbol'], position_side,
2579                                               'hourly review', 'hourly')
```
`EXIT_ADVISOR_HOURLY_SEC = 3600`. This path **can close**: `_advisor_close(..., 'hourly')` at
`virtual_trader.py:2592`.

**(2) TRIGGERED — `15m_exit_confirm`** · `main.py:4393-4401`, inside the 15m webhook route, on the branch
where a directional 15m BOS/CHOCH/Liquidity-Grab arrives and **nothing is armed on the exit state machine**:
```python
4393        if EXIT_ADVISOR_ON_15M_CONFIRM:
4394            for _s in ('LONG', 'SHORT'):
4395                _vp = virtual_trader._open_position(symbol, _s)
4396                if _vp:
4397                    try:
4398                        _adv = consult_exit_advisor(_vp, symbol, _s,
4399                                                    signal_name,
4400                                                    '15m_exit_confirm')
4401                        if (not EXIT_ADVISOR_DRYRUN
```
This path **can close**: `virtual_trader._advisor_close(..., '15m_exit_confirm')` immediately below.

**(3) TRIGGERED, RECORD-ONLY — `armed_exit`** · `main.py:3951-3956`, inside `_execute_armed_exit`:
```python
3951    try:
3952        _vp_armed = virtual_trader._open_position(symbol, side)
3953        if _vp_armed is not None:
3954            consult_exit_advisor(_vp_armed, symbol, side, confirm_signal, 'armed_exit')
3955    except Exception as _e:
3956        print(f"[EXIT-ADVISOR] armed-exit consult failed (close unaffected): {_e}",
```
🔴 **The verdict is discarded.** The close below runs regardless, is not gated on it, and the result is
recorded with `close_reason='external'`, never `ai_exit`. **This trigger can never produce a ledger row** —
and the record confirms it: 3 consultations, 1 `close` verdict (`trades 26626`, vpos 95), and vpos 95 closed
`external` two seconds later.

**(4) TRIGGERED — `5m_group_b`** · `main.py:3717`, the 5m Group-B handler:
```python
3714    if _vpos is None:
3715        _vpos = virtual_trader._open_position(symbol, open_side)
3716    if _vpos is not None:
3717        advice = consult_exit_advisor(_vpos, symbol, open_side, signal_name, '5m_group_b')
3718    else:
3719        advice = claude_advisor.consult_for_close(          # the LEGACY 6-field prompt,
3720            symbol, open_side, entry_price, upnl, age_minutes,   # NOT consult_for_close_rich
3721            snapshot, signal_name,
```
🔴 **This has NEVER fired.** `signal_type='5m_group_b'` → **0 rows of any status, all time**;
`status='ambiguous_side'` → 0. Its `else` branch is the one path in the bot that would reach
`consult_for_close` (the legacy, non-rich prompt) — and it has never been reached either.

**Anything else:** none. `consult_for_close_rich` has no other caller; `grep` over the tree returns the
definition, the one call, and a line in the contract that lifts its source by `inspect.getsource`.

**Recovering the trigger from the record is not inference:** `claude_advisor.py:1089` renders
`Consultation trigger: {g('trigger')}` into the user prompt, and **all 191 stored exit prompts carry that
line** — 0 missing.

### 1b. 🔴 EVERY EXIT CONSULTATION, SPLIT BY TRIGGER — **n = 191**, whole record 2026-07-26 → 2026-09-12

```
trigger                  n   hold  close   close-rate
hourly                 164    110     54      32.9%
15m_exit_confirm        24     11     13      54.2%
armed_exit               3      2      1      33.3%
5m_group_b               0      -      -          -
TOTAL                  191    123     68      35.6%
```
**There is no `unavailable` verdict in this population** — 123 hold + 68 close = 191. One row (`trades 25159`)
is a `claude timeout` recorded as `hold` with confidence 0.0; it is counted as a hold above and named again
in §3a.

🔴 **The verdict split only means something once DRYRUN is taken out.** `EXIT_ADVISOR_DRYRUN` went `False`
in `81875c9`, **2026-07-30 11:32:18**; before that a `close` verdict was a recorded opinion and nothing more.

```
### DRYRUN era — verdicts recorded, nothing acted on          (n=77)
   hourly            n=  68  hold= 24  close= 44   close-rate  64.7%
   15m_exit_confirm  n=   8  hold=  0  close=  8   close-rate 100.0%
   armed_exit        n=   1  hold=  1  close=  0   close-rate   0.0%

### ACTING era — a close verdict closes the position          (n=114)
   hourly            n=  96  hold= 86  close= 10   close-rate  10.4%
   15m_exit_confirm  n=  16  hold= 11  close=  5   close-rate  31.2%
   armed_exit        n=   2  hold=  1  close=  1   close-rate  50.0%
```
**In the acting era, every `close` verdict but one produced an `ai_exit` close.** The exception is the
`armed_exit` record-only row already named. 10 hourly close verdicts → 10 closes; 5 `15m_exit_confirm` close
verdicts → 4 closes (vpos 104 got two, four seconds apart — the pre-`§0.CONSULT-LOCK` double consult).

**By prompt era** (classified by what the stored prompt actually contains, reproducing the 15:20 table
exactly; the 15:20 report's "era 0 = 61" is 60 rows with no protection block plus the one
armed-state-UNREADABLE row, separated here):

| era | rows | hourly | 15m_exit_confirm | armed_exit | hold | close |
|---|---|---|---|---|---|---|
| 0 — no protection block | 60 | 54 | 6 | 0 | 22 | 38 |
| ARMED branch rendered | **4** | 3 | 1 | 0 | 3 | 1 |
| armed state UNREADABLE | 1 | 0 | 1 | 0 | 1 | 0 |
| B — + the arm price | 93 | 80 | 10 | 3 | 69 | 24 |
| **C — + the distance clause** | **33** | **27** | **6** | 0 | **28** | **5** |

🔴 **The era-C column is the one worth staring at: 27 hourly consultations produced ONE close (3.7 %);
6 triggered consultations produced FOUR (66.7 %).** Same in the canon population (vpos ≥ 101, n = 32):
hourly 26 → 1 close, `15m_exit_confirm` 6 → 4 closes. **That is a real and large difference in what the two
paths DO.** It says nothing yet about whether what they do is right — §2.

### 1c. 🔴 THE CLOSES SPECIFICALLY — **14 live `ai_exit` closes, 10 PERIODIC, 4 TRIGGERED**

**All 14 are LIVE.** Titan has been continuously live since 2026-07-29 21:54:16 (`§0.FIRSTLIVE`), the first
`ai_exit` is 2026-07-31 02:06:51, and **every one of the 14 rows carries a real BingX `stop_order_id`**
(e.g. vpos 106 → `2098532141951987712`) at margin $30 × 5. **There is no paper `ai_exit` close in the
record**, so the paper/live split §4a asks for is degenerate: 14 live, 0 paper.

| vpos | side | closed (UTC) | 🔴 TRIGGER | closing row | prev verdict | gap | hold-run | R realised |
|---|---|---|---|---|---|---|---|---|
| 87 | LONG | 2026-07-31 02:06:51 | **hourly** | `19928` | hold | 36.6m | 17 | −0.4397 |
| 88 | SHORT | 2026-07-31 10:35:35 | **hourly** | `20032` | hold | 60.1m | 1 | −0.2964 |
| **89** | SHORT | 2026-07-31 14:15:13 | 🔴 **15m_exit_confirm** | `20097` | hold | **14.9m** | 3 | +1.3862 |
| 90 | SHORT | 2026-07-31 16:25:42 | **hourly** | `20129` | hold | 60.1m | 2 | −0.3036 |
| 91 | SHORT | 2026-08-03 13:41:09 | **hourly** | `21007` | hold | 60.0m | 7 | −0.4844 |
| 92 | LONG | 2026-08-04 00:26:04 | **hourly** | `21149` | hold | 60.2m | 5 | −0.7279 |
| 93 | SHORT | 2026-08-07 04:50:23 | **hourly** | `22065` | — (first) | — | 0 | −0.1370 |
| 96 | LONG | 2026-08-24 13:45:36 | **hourly** | `26756` | hold | 60.0m | 1 | −0.5456 |
| 97 | LONG | 2026-08-24 17:30:52 | **hourly** | `26788` | hold | 60.1m | 2 | −0.7964 |
| 98 | LONG | 2026-08-27 13:16:13 | **hourly** | `27591` | hold | 60.1m | 5 | −0.2601 |
| **101** | SHORT | 2026-09-01 18:00:19 | 🔴 **15m_exit_confirm** | `29123` | hold | **44.6m** | 2 | +0.2956 |
| **104** | LONG | 2026-09-09 08:30:21 | 🔴 **15m_exit_confirm** | `31113` | hold | **44.5m** | 4 | +0.5757 |
| 105 | SHORT | 2026-09-09 23:46:03 | **hourly** | `31259` | hold | 60.2m | 6 | −0.0136 |
| **106** | SHORT | 2026-09-12 09:15:10 | 🔴 **15m_exit_confirm** | `31884` | hold | **13.4m** | 12 | −0.2963 |

**HOW THE TRIGGER WAS RECOVERED, AND HOW IT WAS CHECKED.** The trigger is not stored in a column; it is in
the prompt (`Consultation trigger:`) and in the journal line `[EXIT-ADVISOR-ACT] … trigger=`. Matching each
close to its consultation is unambiguous: **exactly one candidate within ±10 minutes for every close**, at a
lag of 2–3 seconds, and `tv_action` independently agrees (`'hourly review'` vs the 15m signal's own name).
The only position with two candidates is vpos 104, whose second row fired **2 s after the close was already
done** — both are `15m_exit_confirm`, so the attribution is unaffected. **The journal, which only retains
back to 2026-09-09 22:10, independently confirms the two it covers:**
```
2026-09-09T23:46:01  [EXIT-ADVISOR-ACT] vpos=105 BTC/USDT:USDT SHORT trigger=hourly            conf=0.72 — CLOSING at market
2026-09-12T09:15:09  [EXIT-ADVISOR-ACT] vpos=106 BTC/USDT:USDT SHORT trigger=15m_exit_confirm  conf=0.72 — CLOSING at market
```

### 1d. 🔴 HOW STALE WAS THE HOLD THE TRIGGER OVERTURNED

**All four triggered closes reversed a HOLD**: 13.4 min (vpos 106), 14.9 (89), 44.5 (104), 44.6 (101).
Median **29.7 min**.

🔴 **And that is NOT what makes them different, because nine of the ten periodic closes reversed a hold too.**
Their gaps are **36.6, 60.0, 60.0, 60.0, 60.0, 60.0, 60.1, 60.1, 60.1, 60.2 minutes** — the cadence, by
construction (`EXIT_ADVISOR_HOURLY_SEC = 3600`). The tenth (vpos 93) had no previous consultation at all: it
was closed **10 seconds after the position opened**, on its very first look.

**The distribution over the whole record**, gap from the previous consultation on the same position:

| | n | median | mean | min | max |
|---|---|---|---|---|---|
| PERIODIC (`hourly`) | 139 | **60.1 m** | 56.0 m | 1.5 m | 60.2 m |
| TRIGGERED (`15m_exit_confirm` / `armed_exit`) | 27 | **28.6 m** | 30.9 m | 0.1 m | 58.6 m |

**Every `close` verdict that overturned a hold, all eras: 22 periodic (all but one at exactly 60 min) and
6 triggered (13.4 / 14.9 / 24.1 / 44.5 / 44.6 / 58.6 min).** 8 of the 27 triggered consultations came less
than 20 minutes after the previous one.

🔴 **So "a trigger reversed a hold minutes earlier" is the normal shape of the triggered path, not an
anomaly of vpos 106.** What vpos 106 has that the others do not is the **length of the hold run** it
overturned — 12, against 2, 3 and 4 for the other three.

🔴 **CORRECTION TO THE BRIEF AND TO MY 14:30 REPORT.** vpos 106's chain is **13 consultations, not 14**:
twelve hourly holds at 22:00:36, 23:00:42, 00:00:51, 01:00:56, 02:01:04, 03:01:15, 04:01:25, 05:01:28,
06:01:36, 07:01:37, 08:01:42, 09:01:46 — and the **thirteenth**, `trades 31884` at 09:15:09
(`15m_exit_confirm`, Bullish I-BOS), closed it. **Twelve holds, not thirteen.** The 13-minute gap, the
trigger, the verdict and every number in the 14:30 §2d are unchanged.

---

## 2. 🔴 DOES THE TRIGGER TYPE PREDICT THE OUTCOME?

### 2a. The stand — the SAME one, re-run, and it reproduces to the digit

The 14:30 session's replay code was recovered intact and re-run with **two changes and no others**: the DB
handle is read-only (`file:…?mode=ro`, `PRAGMA query_only=1`) and the bar file is selectable so the
pre-2026-08-30 window can be replayed too. **Nothing about 1R, arming, breakeven, the trail, `bardir` order
or fees was altered.** Geometry, verbatim from the stand's own docstring:

```
1R          = |entry - original_sl|                 virtual_trader._one_r_distance
arm at +1R  = entry -/+ 1R                          virtual_trader._breakeven_reached
breakeven   = entry * (1 -/+ (2*TAKER + BUFFER))    = entry * (1 -/+ 0.002)
trail       = water_mark * (1 +/- trail_pct/100)    ARMED ONLY AFTER breakeven
order       at each price point: water_mark -> arm -> SL -> trail
intrabar    `bardir`: rising bar O->L->H->C, falling bar O->H->L->C
fees        taker 0.0005 per leg, both legs
```

**Bars, both fetched fresh and gap-checked by expected-bar count:**
```
canon window : 15 785 1m bars  2026-09-01 18:00 -> 2026-09-12 17:04 UTC   GAPS 0
pre window   : 63 666 1m bars  2026-07-30 12:00 -> 2026-09-12 17:05 UTC   GAPS 0
```

🔴 **CALIBRATION — the three published rows come back EXACTLY:** vpos 101 counterfactual **+0.4509R**,
vpos 104 **−1.1033R**, vpos 105 trail at **77 393.9**, armed 09-10 12:38, **+0.7669R**; deltas
**−0.1553 / +1.6791 / −0.7805**; **Σ +0.7433R / +$0.4727**. Not one digit moved.

**vpos 106 is STILL UNRESOLVED at 17:04.** Re-checked on 7½ hours of bars the 14:30 report did not have:
the original stop **78 301.6 is still untouched**, the +1R arm **75 726.8 is still not reached** (water mark
76 936.5), and the hold marks to **−0.3169R** against the advisor's realised **−0.2963R** — Δ **+0.0206R /
+$0.05**, *mark-to-market only, and it counts for nothing until it resolves.*

### 2b. 🔴 THE DELTAS, SPLIT BY TRIGGER — n stated on every line

**CANON POPULATION (vpos ≥ 101) — the ledger's own population, 3 RESOLVED**

| # | vpos | side | 🔴 trigger | closed | advisor R | counterfactual | cf R | **Δ R** | **Δ $** |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 101 | SHORT | **15m_exit_confirm** | 09-01 18:00 | +0.2956 | **trail** 77 124.0, armed 18:39 | +0.4509 | **−0.1553** | −0.30 |
| 2 | 104 | LONG | **15m_exit_confirm** | 09-09 08:30 | +0.5757 | **ORIGINAL STOP** 78 350.1, never armed | −1.1033 | **+1.6791** | +2.30 |
| 3 | 105 | SHORT | **hourly** | 09-09 23:46 | −0.0136 | **trail** 77 393.9, armed 09-10 12:38 | +0.7669 | **−0.7805** | −1.53 |
| 4 | 106 | SHORT | **15m_exit_confirm** | 09-12 09:15 | −0.2963 | **STILL OPEN**, never armed | *(−0.3169)* | *pending* | *pending* |
| | | | | | | **Σ RESOLVED (3)** | | **+0.7433** | **+$0.47** |

```
TRIGGERED  n=2   Σ Δ +1.5238 R   +$2.0031     values [-0.1553, +1.6791]
PERIODIC   n=1   Σ Δ -0.7805 R   -$1.5304     values [-0.7805]
```

**PRE-2026-08-30 POPULATION (vpos 87–98) — 🔴 A DIFFERENT INSTRUMENT, NOT POOLED WITH THE ABOVE ANYWHERE**

| vpos | side | trigger | closed | advisor R | counterfactual | cf R | **Δ R** |
|---|---|---|---|---|---|---|---|
| 87 | LONG | hourly | 07-31 02:06 | −0.4397 | ORIGINAL STOP 64 028.8 | −1.0795 | **+0.6398** |
| 88 | SHORT | hourly | 07-31 10:35 | −0.2964 | trail 63 192.2, armed 14:06 | +0.4975 | **−0.7939** |
| **89** | SHORT | **15m_exit_confirm** | 07-31 14:15 | +1.3862 | trail 63 171.3, armed 14:16 | +0.6444 | **+0.7418** |
| 90 | SHORT | hourly | 07-31 16:25 | −0.3036 | ORIGINAL STOP 63 491.9 | −1.0722 | **+0.7686** |
| 91 | SHORT | hourly | 08-03 13:41 | −0.4844 | ORIGINAL STOP 63 224.6 | −1.1094 | **+0.6250** |
| 92 | LONG | hourly | 08-04 00:26 | −0.7279 | trail 64 198.7, armed 08-05 15:10 | +0.2746 | **−1.0025** |
| 93 | SHORT | hourly | 08-07 04:50 | −0.1370 | ORIGINAL STOP 64 662.1 | −1.1374 | **+1.0004** |
| 96 | LONG | hourly | 08-24 13:45 | −0.5456 | trail 80 263.5, armed 08-25 02:17 | +1.1119 | **−1.6575** |
| 97 | LONG | hourly | 08-24 17:30 | −0.7964 | ORIGINAL STOP 78 170.3 | −1.0495 | **+0.2531** |
| 98 | LONG | hourly | 08-27 13:16 | −0.2601 | trail 80 038.6, armed 15:12 | +0.4272 | **−0.6873** |
| | | | | | **Σ over 10 RESOLVED** | | **−0.1123** (−$1.93) |

```
TRIGGERED  n=1   Σ Δ +0.7418 R   +$1.2321     values [+0.7418]
PERIODIC   n=9   Σ Δ -0.8541 R   -$3.1643     values [+0.6398, -0.7939, +0.7686, +0.6250,
                                                      -1.0025, +1.0004, -1.6575, +0.2531, -0.6873]
```

### 2c. 🔴 WHAT THIS DOES AND DOES NOT SAY

**IT IS 2 VERSUS 1 IN ONE WINDOW AND 1 VERSUS 9 IN THE OTHER. IT RANKS NOTHING.** I said so at the top and
I am saying it again after the numbers.

Read descriptively and no further: **in both windows the triggered close is the one on the right side of
the sum, and the periodic group carries the negative.** That is the *opposite* direction to the instinct
that prompted this pass. **It is not evidence of that either** — one observation in one group and two in
the other is a coin, not a measurement. Both readings are unsupported by this record.

🔴 **And the sub-population the ledger's sign hangs on is not the triggered one.** Without vpos 104 the
other two resolved closes are −0.9358R; of those two, **one is triggered (101, −0.1553R) and one is
periodic (105, −0.7805R)**. The single gain, vpos 104, is **also triggered**. The trigger axis does not cut
the ledger where the instinct expected.

### 2d. COHORT DISCIPLINE, STATED FOR EVERY OBSERVATION

* **Pre-2026-08-30 (vpos 87–98, the two-sentence prompt): NOT POOLED.** Reported in its own table, its own
  sum, its own trigger split. It is never added to, averaged with, or ranked against the canon population.
  It is here because it is the only way to put more than four numbers in front of you, and it is fenced.
* **The 2026-09-12 14:58:32 cohort boundary:** **all 14 closes fall BEFORE it.** Zero fall after it.
  Verified directly — the latest exit consultation of any kind in the database is 2026-09-12 09:15:09.
  🔴 **So under the wording the bot is running right now, the n for every question in this report is 0.**

---

## 3. 🔴 THE ARMED-STATE QUESTION

### 3a. CONFIRMED — and the true count is 7, not 4

**4 consultations of 191 rendered the trail as ARMED.** Every one:

| trades | when | vpos | side | trigger | verdict | note |
|---|---|---|---|---|---|---|
| `20097` | 2026-07-31 14:15:11 | **89** | SHORT | 15m_exit_confirm | **close** | 🔴 the only armed CLOSE ever; reason **truncated at exactly 400 chars** by the old cap, mid-word — it never reached the trail |
| `25159` | 2026-08-17 15:41:04 | 94 | LONG | hourly | hold | `claude timeout`, conf 0.0, 14-char reason — **no verdict content at all** |
| `25165` | 2026-08-17 16:41:00 | 94 | LONG | hourly | hold | *"+1.13R gain with trailing stop 0.81R away provides solid risk/reward."* |
| `28531` | 2026-08-30 17:05:47 | 100 | LONG | hourly | hold | *"With stop-market resting on exchange and trailing protection armed, downside is contained. Let trailing stop work…"* |

**The 15:20 report's "four, of which one was a timeout and one was truncated" HOLDS, exactly.**

🔴 **And the population is slightly larger than four, in the direction that makes the point stronger.**
vpos 82 armed at **2026-07-26 22:02:35** and was then consulted **three times** — 22:06:11, 23:06:12,
00:06:15, all HOLD, MFE +1.29R / +2.07R / +2.24R — on a prompt that carried **no protection block at all**,
because the block did not exist yet. So:

```
consultations taken on a position whose trail WAS armed :   7 of 191
   ...with the fact RENDERED                            :   4
   ...with the prompt SILENT about it                   :   3   (vpos 82, 2026-07-26)
consultations taken on an UNPROTECTED position          : 184 of 191
```

**In era C: 0 of 33. In the canon population (vpos ≥ 101): 0 of 32. Your observation (2) is correct and
survives the full sweep.**

### 3b. 🔴 WHY — from the code, and from the data, not by inference

**FROM THE CODE: arming and consulting are NOT mutually exclusive. There is no gate.**
* The hourly consult is `if EXIT_ADVISOR_HOURLY:` (`virtual_trader.py:2572`) — **no `be_applied` term**, and
  it sits at step **1e** of `_process_position`, **before** the breakeven/arming block at step 2 and the
  trail at step 4. It runs on an armed position exactly as on an unarmed one.
* The `15m_exit_confirm` consult is `if EXIT_ADVISOR_ON_15M_CONFIRM:` (`main.py:4393`) with no armed term
  either; it takes whatever `_open_position` returns.
* The prompt itself is written to handle both: in the applied file `claude_advisor.py:783-785` is the ARMED
  branch and `:786` onward the unarmed one (the `f16c271` rewrite, `ARMS AT` at `:820`), with the
  unreadable-state branch at `:782`. The branch is selected on `ctx['trail_armed']`, which
  `main.py:3391-3398` reads from the authoritative `pending_dca_limits.breakeven_applied`.
* The only thing in the engine that *is* gated on `be_applied` is the **post-entry recheck**
  (`virtual_trader.py:2621`, "PRE-BREAKEVEN ONLY") — a different mechanism.

**FROM THE DATA: the positions simply never get there.** Every stored prompt carries
`Peak so far (MFE): ±X.XXR`. Across the 190 consultations that have the line:

| MFE at the moment of decision | n | share |
|---|---|---|
| ≥ +1.00R (armed, or arming) | **7** | 3.7 % |
| +0.75 … +1.00R | 28 | 14.7 % |
| +0.50 … +0.75R | 27 | 14.2 % |
| +0.25 … +0.50R | 41 | 21.6 % |
| 0 … +0.25R | 54 | 28.4 % |
| ≤ 0R — never once positive | 33 | 17.4 % |

median **+0.350R**, mean **+0.382R**.

🔴 **And in the canon population it is not close: n = 32, median MFE +0.06R, MAXIMUM +0.72R, and NOT ONE
consultation at or above +1R.** Era C is the same 33 numbers.

**The mechanism is airtight and checkable:** all 7 consultations with MFE ≥ +1R either rendered ARMED (4 of
4 that had a protection block) or predate the block entirely (3, vpos 82). **There is no case where a
position was at or past +1R and the prompt said "not armed".** The unarmed rendering is not a bug and it is
not a filter — it is an accurate report that the position had not got there.

### 3c. HOW MANY POSITIONS EVER ARMED, AND WHO CLOSED THEM

**24 of the 80 positions in the book have ever armed** (`breakeven_applied = True`). Who closed them:

| closed by | armed | never armed |
|---|---|---|
| **trail** | **17** | 3 |
| **sl** (the breakeven stop, post-arming) | 5 | 28 |
| **external** | 1 | 11 |
| `post_entry_critical` | 0 | 1 |
| 🔴 **`ai_exit` — the advisor** | 🔴 **1** | **13** |

🔴 **One armed position has ever been closed by the advisor: vpos 89, 2026-07-31, ten minutes after it
armed.** Every other armed position was taken by the trail, by the breakeven stop, or externally.

**Restricted to the 25 positions the advisor has ever been consulted on, the picture is starker: 4 armed.**

| vpos | armed at | armed → closed | closed by | consultations | of which ARMED-rendered |
|---|---|---|---|---|---|
| 82 | 2026-07-26 22:02:35 | 125 min | trail | 3 | 0 *(no block existed yet)* |
| **89** | 2026-07-31 14:05:07 | **10 min** | 🔴 **ai_exit** | 4 | **1** |
| 94 | 2026-08-17 15:38:07 | 117 min | trail | 7 | 2 |
| 100 | 2026-08-30 16:16:20 | 62 min | trail | 6 | 1 |

**That is the structural fact.** Arming does not remove a position from the advisor's reach by rule — it
removes it by *speed*. The armed window is 10–125 minutes wide; the periodic cadence is 60 minutes; the
trail usually gets there first. **In the 13 days of the canon population, no position armed at all.**

### 3d. 🔴 THE SHAPE OF THE LEDGER — described, not concluded

Your reading of the ledger is right on its own terms: both canon losses are **SHORTS closed in front of a
move that armed the trail afterwards** — vpos 101 armed **39 minutes** after the advisor left, vpos 105
**12.8 hours** after. The one gain, vpos 104, is a **LONG whose hold ran into the ORIGINAL STOP** and never
came within 137 points of its arm.

🔴 **Extended to all 13 resolved closes, that shape is almost the whole story — and it is not about the
trigger:**

```
counterfactual ARMED after the advisor left  : n=7    advisor LOST (ΔR<0) in 6 of 7
counterfactual NEVER armed                   : n=6    advisor WON  (ΔR>0) in 6 of 6
```

**12 of 13.** The single exception is **vpos 89 — the one position the advisor judged while it was already
armed**, where the advisor beat the hold by +0.7418R.

**Stated as a description and nothing more.** It is close to a tautology: if the hold would have armed, the
advisor forwent a runner; if it would not, the advisor forwent a stop-out. It carries no information about
*whether the advisor could have known*. What it does say plainly is:

🔴 **The advisor decides, essentially always, at the point where the single fact that determines the
outcome — will this position arm? — is not yet knowable. 184 of 191 consultations, and 32 of 32 in the
population the ledger counts, were taken on an unprotected position, at a median MFE of +0.06R.** That is a
description of *when* it acts. It is not a claim that acting there is wrong, and **no later pass may cite
this cell as an effect.**

---

## 4. 🔴 THE HONEST FRAME

### 4a. It does not separate on a usable n, and here is the arithmetic rather than an opinion

I am not reporting a Bonferroni-corrected p-value, a sign test or a paper/live split as *results*, because
the group sizes make them undefined-by-arithmetic before the data is even looked at:

| comparison | group sizes | **smallest two-sided p any rank test can return** | can reach 0.05? |
|---|---|---|---|
| canon population, resolved | 2 vs 1 | **0.667** | **no** |
| canon population, observed (incl. the open one) | 3 vs 1 | 0.500 | **no** |
| pre-2026-08-30 population | 1 vs 9 | **0.200** | **no** |
| *(the forbidden pooled 14)* | *4 vs 10* | *0.002* | *— pooling is not permitted* |

**Bonferroni over the two windows would demand α = 0.025, which neither window can reach even with a
perfect separation.** The **sign test** is worse: it would have one sign in the triggered group in each
window. The **paper/live split** is degenerate: **14 live, 0 paper** — the advisor has never closed a paper
position, so there is no contrast to draw.

### 4b. 🔴 WHAT n WOULD, AND HOW LONG THAT IS

**The bare floor — capability, not power.** A permutation test needs `C(n₁+n₂, n₁) ≥ 40` to be *able* to
return p ≤ 0.05. That is **4 vs 4 = 8 closes**, and only if **every** triggered delta is worse than **every**
periodic delta. At Titan's measured **one `ai_exit` per 3.26 days**, 8 closes ≈ **26 days**.

**Realistically — power, using the only legitimate variance estimate available.** The pre-2026-08-30 window
is a single population of 10 deltas: mean −0.011R, **SD 0.935R**. Against that spread, at α = 0.05 two-sided
and 80 % power:

| difference in mean Δ to detect | n per group | closes, balanced | at the observed 28.6 % triggered rate | elapsed at 3.26 d/close |
|---|---|---|---|---|
| 1.50 R *(implausibly large)* | 7 | 14 | 25 | **82 days** |
| **1.00 R** | 14 | 28 | **49** | **≈ 160 days ≈ 5.3 months** |
| 0.75 R | 25 | 50 | 88 | 287 days |
| **0.50 R** | 55 | 110 | **193** | **≈ 630 days ≈ 1.7 years** |

With the Bonferroni correction §4a asks for (α = 0.025), the 1.00R row becomes **34 balanced closes**.

🔴 **And all of that restarts from zero.** Every one of the 14 closes was taken under prompt wording that
the 14:58:32 patch replaced. **Under the current wording the count is 0.** The trigger question, asked of
the bot as it stands right now, has no observations at all.

### 4c. 🔴 THE RESULT, PLAINLY

**Nothing separates.** The record does **not** support the reading that the advisor is wrong on exits in the
triggered sub-population — and it does not support the opposite either. **Three resolved closes cannot tell
a bad mechanism from variance, and they cannot tell a good one from luck.** The ledger's positive sign is
carried by one trade; the two remaining losses are split one triggered, one periodic. **That is a
legitimate result. It is not a hint, and it should not be read as one.**

The one thing this pass does establish, and it is a fact about the mechanism rather than a measurement of
its quality: **the advisor's entire decision population is unprotected positions, at a median MFE of
+0.06R in the canon window, with a maximum of +0.72R.** It does not decide *whether to give up a runner* —
it decides *whether a position that has not yet earned protection is still worth holding*. Whether that is
the right place to decide is a question this record cannot answer yet.

### 4d. `EXIT_ADVISOR_DRYRUN`

**Still `False`, read from `config` at runtime. Not flipped, not proposed, not asked about. The rule decides
at 10 resolved closes and it stands — 3 of 10, 7 remaining.**

---

## 5. 🔴 THE OUTSTANDING ITEM — STILL OPEN. IT IS NOT CLOSED AND I AM NOT DRESSING IT UP.

**No entry consultation has occurred, so `signal_tiers` has still not been imported, and there is no
regenerated header to quote.**

```
last ENTRY consultation in the database : 2026-09-11 22:00:11   (trades 31760, BEFORE the 14:18 restart)
every trades row since the 14:58:32 restart:
    ema_envelope_blocked  17   (latest 2026-09-12 17:05:04)
    htf_blocked            3
    context_recorded       3
    confirm_recorded       1
  -> every signal since the restart was stopped at the EMA-envelope or HTF gate,
     BEFORE the advisor. Open positions right now: 0.
```

```
signal_tiers .pyc, read with bytecode writing OFF so nothing was disturbed:
  pyc file mtime   : 2026-08-04 15:07:11 UTC       <- UNCHANGED since the 15:20 report
  pyc header mtime : 2026-08-04 15:06:23  size 15924
  source    mtime  : 2026-09-12 14:15:53  size 23584
  header == source : False
  source sha256    : 4af4fdba57cfaf840416e260cd4cea2eb1b38a46caea6913bea887fe95ca6a6a
```

**What remains proved, unchanged:** the cached header disagrees with the applied source in both mtime and
size, so **Python cannot load that bytecode** — the first `import signal_tiers` must compile
`4af4fdba57cfaf84` from source. **What remains UNPROVED is the in-process confirmation, and it stays
unproved.**

🔴 **One more thing, because the mechanism failed and not just the wait: the watcher armed at
2026-09-12 14:59:35 is NO LONGER RUNNING.** It was bound to the session that started it; `ps` shows no
watcher process, and its output file still contains only its start line. **A promise that depends on a
session-scoped background process is not a mechanism.** It does not matter much here, because the check
needs no watcher — the `.pyc` header is a persistent record and one `stat` answers it at any time — but the
15:20 report's "a fresh watcher is armed" should be read as "nothing is watching".

**This item stays open.**

---

## CONTROLS — READ-ONLY, PROVED RATHER THAN ASSERTED

| | |
|---|---|
| `openitems_guard` | **EXIT=0** at session start (run first, as instructed) · **EXIT=0** at session end |
| Titan DB | every handle opened `file:/root/titan-bot/trades.db?mode=ro` with `PRAGMA query_only=1`. **No `-wal`, `-shm` or `-journal` side-file exists.** The counterfactual stand was re-pointed to a read-only handle before it was run |
| writes / orders / restarts | **none.** Journal since session start (16:55) contains **0** lines matching `EXIT-ADVISOR|ORDER|CLOSE|RECONCILE|BREAKEVEN|TRAIL|error|Traceback` |
| `titan.service` | `active`, **MainPID 1572470**, **NRestarts 0**, `ExecMainStartTimestamp 2026-09-12 14:58:32 UTC` — identical at the start and the end of this pass |
| open positions | **0** — the book is flat; nothing in this pass could reach a position if it tried |
| `EXIT_ADVISOR_DRYRUN` | **False** — read from `config` at runtime. **Not flipped** |
| other flags, read at runtime | `LIVE_TRADING_ENABLED` **True** · `ORDER_ADAPTER_LIVE` **True** · `BOOK_GATE_ENABLED` **True** · `BOOK_GATE_DRYRUN` **False** · `CLAUSE_A` **True** · `CLAUSE_B` **False** · `SL_ATR_MULT` **2.25** · `TRAIL_MULT_ATR` **1.6875** · `MAX_POSITIONS_PER_SIDE` **1** · `AI_ADVISOR_HIDE_1H` **False** |
| **book-gate counter** | **22 of 200, UNTOUCHED, 0 refusals all time.** 15 DRYRUN rows (13 LONG / 2 SHORT, 09-08 04:15:15 → 09-10 13:55:09) + 7 LIVE (5/2, 09-11 11:10:08 → 09-11 22:00:11). Latest gate row `trades 31760` — identical to the 14:30 and 15:20 readings |
| git | working tree **clean**, `titan-bot/` HEAD **`f16c271`**, no commit made |
| BingX | **public 1m OHLCV only**, the same `fetch_ohlcv` call the 14:30 report used. No order, no position query, no account mutation |
| 🔴 **Mercury-SOL** | **NOT TOUCHED.** `active`, **MainPID 1341949**, **NRestarts 0**, `ExecMainStartTimestamp 2026-09-11 18:26:59 UTC` — unchanged. `find mercury-sol -name '*.py' -newermt '2026-09-12 16:55'` → **EMPTY**. The only files newer than this session's start are its own runtime writes (`oi_cache.json`, `trades.db`, `optimizer/tg_offset.txt`), written by the bot itself. No DB query, no restart, no venue call on its key |
| 🔴 open | the in-process `.pyc` confirmation for `signal_tiers` — still open, §5, and the watcher that was meant to close it is dead |
