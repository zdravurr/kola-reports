# Titan — the matrix tier names are APPLIED and LOADED, and the exit-advisor ledger is 3 RESOLVED of 10: **+0.74R in the advisor's favour, on one trade**

**2026-09-12 14:30 UTC · commit `7b17e11` · Titan LIVE REAL MONEY · Mercury-SOL NOT TOUCHED**

---

## WHAT YOU ASKED, ANSWERED FIRST

1. **The patch is applied and loaded.** Book proved flat on both BingX probes with an empty error list before
   the copy *and* again before the restart. AST proof PASS on the applied file; contract **8 of 8 green as root
   and as botuser**; the four advisor SYSTEM prompts sha256-identical after the apply. Restarted 14:18:13 UTC.
2. 🔴 **vpos 105 RESOLVED, and the advisor lost money on it.** It closed at **−0.01R**; holding resolved on the
   **trail at 77 393.9 on 09-10 14:56** for **+0.77R**. **Δ = −0.7805R / −$1.53.**
3. 🔴 **vpos 106 is STILL RUNNING and stays UNRESOLVED.** The original stop was never touched. Marked to this
   minute, **holding would have been WORSE by 0.0391R = $0.10** — but that counts for nothing until it resolves.
4. 🔴 **THE LEDGER IS POSITIVE: 3 RESOLVED of 10, Σ = +0.7433R / +$0.47.** **It is not grounds to flip.**
   But the sign is carried entirely by **one** trade: without vpos 104 the other two are **−0.936R / −$1.83**.
5. **7 resolved closes remain**, ≈ **23–25 days** at Titan's measured rate — **the first week of October 2026**.
   `EXIT_ADVISOR_DRYRUN` **stays False**. Not flipped, as instructed.

`openitems_guard` **EXIT=0** at the start of this session, after the restart, and after both canon writes.
One intermediate **EXIT=1** is reported in §1g — the guard caught my own stale header, which is its job.

---

## 0. THE GUARD, AND THE FLAT PROOF THAT LICENSED EVERYTHING ELSE

```
openitems_guard — canon: .../reports/OPEN-ITEMS.md
  titan-bot HEAD : cd0f175   <- the SUBJECT
  watched values : 14
✅ header and current-state table agree with runtime.          EXIT=0
```

🔴 **FLAT, on the DB and on the venue, both probes, empty error list** (14:14:25 UTC, and re-proved at
14:17:50 immediately before the restart — both readings identical):

```
open virtual_positions (status='open')   0      (6 rows are 'archived_pre_geometry_fix', historical)
exit_pending                             0 rows
breakeven_jobs                           0 rows

=== BingX PROBE (doubled: unified fetch_positions + raw swapV2PrivateGetUserPositions, UNION) ===
positions dict : {}          position errors: []      <- EMPTY, not "unknown"
open orders    : {}          order errors   : []
ALL-symbol non-zero positions: []
```

The doubled probe is `order_adapter._probe_positions` / `_probe_stop_orders` — Titan's own boot-reconcile
code, not a probe written for this report. An empty dict **with a non-empty error list** would have meant
*we do not know*; the error list is empty, so it means *flat*.

**vpos 106 closed 2026-09-12 09:15:10 UTC** at 77 329.8 on `ai_exit` (the operator said 09:14; the row says
09:15:10 and its consultation 09:15:09).

---

## 1. THE PATCH — APPLIED, PROVED ON THE APPLIED FILE, LOADED

### 1a. Backup, copy, and one discrepancy I have to report

```
signal_tiers.py                                  ac32ba122728557662473f1b7b4ccbe637fff91d629b439a512614e4adb11fa7  (before)
scratchpad/sbx/signal_tiers_BEFORE.py            ac32ba12...  <- IDENTICAL to the live file. The sandbox
                                                                 baseline WAS the running code.
signal_tiers.py.bak_matrixnames_20260912T141553Z ac32ba12...  <- the backup is the exact pre-change file
signal_tiers.py                                  4af4fdba57cfaf840416e260cd4cea2eb1b38a46caea6913bea887fe95ca6a6a  (after)
  == scratchpad/sbx/signal_tiers.py, byte for byte
```

🔴 **The 2026-09-12-0020 report's §2f quotes the patched sha as `d7d6f33bc29cfb96` with `+142 / −2` lines. The
file actually sitting in that scratchpad is `4af4fdba57cfaf84`, `+145 / −2`.** The proof in §2f was printed at
00:12; the file was saved again at 00:15, during the contract iteration §2e describes. **I applied what is in
the scratchpad, as instructed, and re-proved it — the AST proof and all 8 contract cases pass on the file that
is actually there, with the same node counts §2f predicted.** I am not going to quietly let a published sha
stand for a different file.

**`tests/` created** (Titan had none). Installed: the contract, plus two support files.

🔴 **The contract needed exactly two adaptations to become a contract on the LIVE file instead of on a sandbox
copy, and they are the reason it is worth having:**
* it now loads `signal_tiers.py` from `/root/titan-bot/` and its baseline from
  `signal_tiers.py.bak_matrixnames_20260912T141553Z` — the applied file and the file it replaced, not two
  scratchpad copies. (That also needed an explicit `SourceFileLoader`: `spec_from_file_location` cannot infer a
  loader for a `.bak_…` extension.)
* `tests/signal_matrix.py` shadows the real module for that directory only, exposing **only** `classify()`,
  AST-read from the real `/root/titan-bot/signal_matrix.py`. **The real module runs `init_db()` at import**,
  which writes to the LIVE `trades.db`. A contract must not write to the live database to run.

### 1b. AST proof, re-run ON THE APPLIED FILE against the backup

```
signal_tiers.py  sha256 ac32ba1227285576 -> 4af4fdba57cfaf84
  top-level named nodes ADDED   : ['_gate_holds_phrase', '_sides_in_window', '_sides_phrase']
  top-level named nodes REMOVED : []
  text diff: +145 lines, -2 lines
  removed lines: ['                f"({pts}{cnt}), so it nets NEUTRAL")',
                  '                         f"state machine at this moment")']

  after stripping ONLY the change: AST identical to the file on disk = True
  removed counts: {'helper': 3, 'stmt': 1, 'assign': 2, 'call': 2}  (expected helper=3 assign=2 stmt=1 call=2)
AST PROOF PASS
```

### 1c. The 8-case contract — green as root AND as botuser

```
### AS ROOT
  [0] absent/malformed matrix_result: byte-identical to the pre-change builder and raises in exactly the same places: True
  [1] matrix_result WITH a breakdown but no active_signals == pre-change builder, byte for byte: True  (715 chars)
  [2] rendered phrase exact: True
  [3] block minus the one phrase == the no-names block: True
  [4] Agreement sentence untouched (still counts the slots): True
  [5] reverse case rendered: True
  [5b] reverse still names the gate direction without active_signals, and the names/ages clause is absent: True
  [6] malformed active_signals: no exception, no clause, byte-identical: True
  [7] the EXIT advisor's entry-thesis block carries it too: True
OK   EXIT=0

### AS BOTUSER  (whoami: botuser)   — same 9 lines, all True, EXIT=0
```

🔴 **HOW THE BOTUSER PASS WAS RUN, STATED PLAINLY BECAUSE IT IS NOT THE APPLIED PATH.** `/root` is `drwx------`,
so **botuser cannot read `/root/titan-bot/signal_tiers.py` at all** — which is also why titan's unit is
`User=root`. The botuser run therefore used **sha256-pinned byte copies** in a traversable directory:

```
4af4fdba57cfaf84…  /root/titan-bot/signal_tiers.py                    <- applied
4af4fdba57cfaf84…  <botuser dir>/signal_tiers.py                      <- identical
ac32ba122728…      /root/titan-bot/signal_tiers.py.bak_matrixnames_…  <- baseline
ac32ba122728…      <botuser dir>/signal_tiers.py.bak_matrixnames_…    <- identical
28053eb5f5d3…      /root/titan-bot/tests/test_…_names_ages.py         <- installed contract
28053eb5f5d3…      <botuser dir>/tests/test_…_names_ages.py           <- identical
```
The 2026-08-27 botuser rule exists because two other contracts read the invoking user's crontab. **This one
reads no crontab**, and it is a pure function test — which is why byte-identical copies are a sound stand for
it. The temporary directory was removed afterwards.

### 1d. The four advisor SYSTEM prompts — sha256 re-verified AFTER the apply

```
  _ENTRY_SYSTEM         1871 chars  30c979595a4831aa751db8bd64d7bcb47e9af63088ae665489b4fe3bd5f573f2   == baseline: True
  _LEARNING_SYSTEM       730 chars  191cf5d71ebf3865535f8e0bfb09106a7d6c758bca8566e70e5fc4309f7138c2   == baseline: True
  _CLOSE_SYSTEM          452 chars  7d7707cfa2d336f75f690eba53114fedb56b790222ecf681ec467211a901b545   == baseline: True
  _CLOSE_SYSTEM_RICH     252 chars  3d709571e17ff4051362c5a50496c74c0223b29a062eb2c94b2a5de09655670b   == baseline: True
  claude_advisor.py whole file      ca14e959a5c6104c8438ddc493750d4193a0a32bfab49312b30eff2eb1a8c6c6   == baseline: True
```
The patch never opened `claude_advisor.py`. This confirms it rather than assuming it.

### 1e. Restart from flat — the boot line

```
MainPID  961100 -> 1563560     NRestarts 0     ActiveEnterTimestamp Sat 2026-09-12 14:18:13 UTC

14:18:19  [TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
14:18:19  [TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
14:18:19  [TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
14:18:19  [TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
🔴 14:18:23  [TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
14:18:23  [RECONCILE] boot reconciliation starting
14:18:25  [STOP-CLEANUP] no orphaned orders for LONG BTC/USDT:USDT
14:18:25  [STOP-CLEANUP] no orphaned orders for SHORT BTC/USDT:USDT
14:18:25  [RECONCILE] done
```
Zero errors, zero tracebacks in the boot journal.

### 1f. 🔴 THE LOADED-BYTECODE CHECK — WHAT I CAN PROVE NOW, AND WHAT I CANNOT YET

**I cannot yet quote a regenerated `.pyc` for `signal_tiers`, and I will not pretend otherwise.** The reason is
mechanical: `signal_tiers` is a **lazy** import — `claude_advisor.py:567` and `main.py:2999` import it *inside*
the function, so it is first imported at the first **entry consultation**, and none has occurred since the
restart (every signal since 14:18 was stopped at the HTF or EMA-envelope gate, before the advisor). Its
`__pycache__` entry is therefore still the one from 2026-08-04.

**What that stale cache proves, run with bytecode writing OFF so the on-disk pyc was not disturbed:**
```
CACHED pyc  header: mtime 1785855983  size 15924    (2026-08-04 15:07:11)
APPLIED src       : mtime 1789222553  size 23584    (2026-09-12 14:15:53)
cache VALID for this source?  False      -> the cache is DISCARDED, the module recompiles FROM SOURCE

module loaded from : /root/titan-bot/signal_tiers.py
has the three NEW helpers: True
source sha256 of the loaded file: 4af4fdba57cfaf840416e260cd4cea2eb1b38a46caea6913bea887fe95ca6a6a
pyc on disk UNCHANGED by this proof: True
```
**The old bytecode is not loadable.** Python validates the cache against the source's mtime and size; both
differ, so the worker's first `import signal_tiers` must compile the applied file. The other five modules
**were** re-read at boot and their headers do match their sources:
```
  claude_advisor  pyc 2026-08-31 15:10:04  header==source: True  sha ca14e959a5c6104c
  config          pyc 2026-09-10 14:34:54  header==source: True  sha 1dc387744a976d54
  main            pyc 2026-09-09 20:46:02  header==source: True  sha 00c8be297a8de922
  signal_matrix   pyc 2026-08-05 22:47:31  header==source: True  sha 0e4128911c283b2f
  state_machine   pyc 2026-08-21 19:44:21  header==source: True  sha 7f5a21ea88662453
```
A watcher is running against that `.pyc`; the in-process confirmation goes in the next report, at the first
consultation. **Every other claim here is measured, not inferred — this one is the exception and it is flagged.**

### 1g. The counters, and the guard catching me

```
BOOK_GATE_ENABLED            True
🔴 BOOK_GATE_DRYRUN          False
BOOK_GATE_CLAUSE_A_ENABLED   True
🔴 BOOK_GATE_CLAUSE_B_ENABLED False
🔴 EXIT_ADVISOR_DRYRUN       False
LIVE_TRADING_ENABLED         True     ORDER_ADAPTER_LIVE   True
SL_ATR_MULT 2.25   TRAIL_MULT_ATR 1.6875   MAX_POSITIONS_PER_SIDE 1   AI_ADVISOR_HIDE_1H False
CATEGORY_TTL_MINUTES  TREND 360 · MOMENTUM 90 · LIQUIDITY 30 · EXECUTION 5
```

**Book-gate review counter — 22 of 200, UNDISTURBED, 0 refusals all time.**

| era | rows | LONG | SHORT | window |
|---|---|---|---|---|
| DRYRUN, before the 2026-09-10 14:36:20 boundary | **15** | 13 | 2 | 09-08 04:15:15 → 09-10 13:55:09 |
| LIVE, after it | **7** | 5 | 2 | 09-11 11:10:08 → 09-11 22:00:11 |
| | **22 of 200** | 18 | 4 | |

`status='book_blocked'`, all time: **0**. Latest gate row: trades 31760, 09-11 22:00:11. Identical to the last
read — nothing in this pass reads, writes or can reach the gate.

🔴 **THE GUARD CAUGHT MY OWN STALE HEADER, AND THAT IS THE POINT OF IT.** After the commit:
```
🔴 1 MISMATCH(ES) — the canon asserts something runtime denies:
  HEAD    doc='cd0f175'    runtime='7b17e11'    header commit is stale vs the last titan-bot/ commit
REFUSING to bless this canon.                                                    EXIT=1
```
Header updated to `7b17e11` with its own stanza → **EXIT=0**. The guard ran **four** times this session:
clean before, clean after the restart, **EXIT=1** on the stale header, clean after the fix.

### 1h. §0.MATRIX-TIER-NAMES written into the canon, as applied

Inserted beside `§0.PROMPT-PAIRING`, rewritten from "PROPOSED / NOT APPLIED" to **APPLIED 2026-09-12 14:18:13
UTC, FROM FLAT**, carrying the shas, the AST result, the 8/8 contract, the boot line, the honest scope limit
(the names/ages clause vanishes without `active_signals`; the reverse clause does not), and the pre-existing
`build()` "never raises" defect **flagged and deliberately not fixed**.
**Nothing was lost in either canon write:** +4 725 bytes for the entry, 0 lines whose count decreased, verified
line-multiset against the backup `OPEN-ITEMS.md.bak_matrixnames_20260912`.

---

## 2. 🔴 THE EXIT-ADVISOR LEDGER

### 2a. The stand, and why you can trust this run

The replay is the canon's own method (`§0.EXIT-ADVISOR-RULE`), implemented from Titan's own exit code, not
reinvented: 1R = |entry − `original_sl_price`| (`virtual_trader._one_r_distance`); arm at +1R
(`_breakeven_reached`, identical to `breakeven_worker:754-759`); on arming the stop moves to
entry × (1 ∓ (2 × 0.0005 + 0.001)); after arming the trail is `water_mark × (1 ± trail_pct/100)` and is
**inactive before arming**, mirroring the live `TRAILING_STOP_MARKET`; `water_mark` carries over from the row's
value at the advisor's close; order at each price point is water_mark → arm → stop → trail; taker 0.0005 both
legs. Intrabar order **`bardir`**: rising bar O→L→H→C, falling bar O→H→L→C.

**15 624 1m BingX candles, 2026-09-01 18:00 → 2026-09-12 14:23, 0 GAPS** (verified by expected-bar count).

🔴 **TWO INDEPENDENT CALIBRATIONS, BOTH EXACT.** The same stand re-derived rows 1 and 2 from scratch and
reproduced their already-published numbers **to the digit** — vpos 101 counterfactual **+0.4509R**, vpos 104
**−1.1033R**. And the canon, written 2026-09-09, *predicted* that vpos 105 would arm at 12:38 and trail at
**77 393.9 for +0.7669R**; this replay independently produced **armed 09-10 12:38, trail 77 393.9, +0.7669R**.
That is what licenses row 3.

### 2b. 🔴 vpos 105 — RESOLVED. The advisor cost $1.53 on this one.

```
vpos 105 SHORT · entry 78 263.2 · original stop 79 295.1 · 1R = 1 031.9 pts · trail 0.989% · size 0.0019
  +1R ARM PRICE = 77 231.3    breakeven-on-arm = 78 106.7
  state carried from the close: water_mark 77 750.2 · breakeven_applied False (NOT armed at the close)
  replay 2026-09-09 23:47 -> 2026-09-12 14:21 UTC, 3 755 bars, 0 gaps

  -> ARMED  2026-09-10 12:38 UTC   (low reached 77 231.3; stop moved to breakeven 78 106.7)
  -> TRAIL  fired at 77 393.9      2026-09-10 14:56 UTC     lowest print (MFE) 76 636.0
     gross +$1.6516   fees $0.1479   NET +$1.5037   = +0.7669 R
```
**ADVISOR: −0.0136R (−$0.0267). HOLDING: +0.7669R (+$1.5037). Δ = −0.7805R = −$1.53.**
It resolved **16 minutes after** the 14:40 snapshot the canon last took. It could no longer have ended on the
original stop — the stop had moved to breakeven at 12:38.

### 2c. 🔴 vpos 106 — STILL RUNNING. Left UNRESOLVED, as instructed.

```
vpos 106 SHORT · entry 77 014.2 · original stop 78 301.6 · 1R = 1 287.4 pts · trail 1.254% · size 0.0019
  +1R ARM PRICE = 75 726.8    water_mark over the whole 11.2h life = 76 936.5   -> 🔴 NEVER REACHED, 1 209.7 pts
                                                                                   short = 0.94R. THE TRAIL NEVER ARMED.
  replay 2026-09-12 09:16 -> 14:23 UTC, 308 bars, 0 gaps
  post-close HIGH 77 375.1 at 14:22  -> the original stop 78 301.6 was NOT touched
  post-close LOW  77 224.8 at 13:26  -> the arm is no nearer

  -> STILL OPEN at 77 368.8     net −$0.8204  = −0.3354 R    (mark-to-market only)
```

**PLAINLY: holding would have been WORSE, by 0.0391R = $0.10.** The advisor realised −0.2963R (−$0.72); the hold
stands at −0.3354R (−$0.82) as of 14:23. You are right that the stop was not hit — price was 77 337.9 shortly
after the close and 77 368.8 now. **The hold resolves nowhere yet: it is open, and it counts for nothing in the
ledger until it hits the stop, or arms and trails.** At the current price it needs 933 points *down* to arm and
932 points *up* to stop out.

*(Basis note: the advisor's realised R is `net_pnl / initial_risk_usdt` as everywhere in this canon, and that
includes −$0.02142 of funding; the counterfactual is gross − fees, because future funding is unknowable. The
asymmetry is worth ≤ $0.03 here and does not change any sign.)*

### 2d. vpos 106's closing verdict, IN FULL, untruncated

🔴 **Trigger: `15m_exit_confirm` on a `Bullish I-BOS` — NOT the hourly.** Thirteen consecutive hourly reviews
from 22:00:36 to 09:01:46 all said **hold** (conf 0.72, one 0.62). The fourteenth consultation, 13 minutes after
the last hold and fired by an adverse 5m structure print, closed it. *(The row carries
`status='exit_ai_dryrun'` — that is a label on the consultation row, not a mode: `EXIT_ADVISOR_DRYRUN` is
**False** and the position really closed, `close_reason='ai_exit'`.)*

**trades.id 31884 · 2026-09-12 09:15:09 UTC · `close` · confidence 0.72 · `claude-haiku-4-5-20251001` · 881 of 1 200 chars:**

> Entry thesis deterioration outweighs holding cost. At entry, 15m+1h+5m aligned SHORT with ADX 31.0 (15m) and strong MTF confluence. Now: 15m and 5m both NEUTRAL (regime flip), ADX 15m collapsed to 14.1 (−54%), ADX 1h to 11.1 (−49%). The bearish I-CHOCH+ at entry (weight 0.9) is contradicted by Bullish I-CHOCH 25m ago—price has not confirmed further downside. Supporting wall thinned x9.0→x7.0; opposing wall thick at 90th pct. Imbalance fell 0.60→0.54. Position has given back 0.31R from +0.06R MFE with no fresh lower low; 11.2h elapsed suggests trapped liquidity. Unrealised loss −0.25R with 0.75R buffer to stop; holding risks full 1.0R stop-loss for a thesis no longer supported by momentum or trend alignment. Closing cost 0.060R (24% of unrealised) is acceptable vs thesis death and deteriorating technicals. Trailing stop not armed; no asymmetric upside protection exists.

**WHICH OF THE FIVE FACTS IT CITED: ALL FIVE — the first verdict in this population to do so.**

| fact | rendered in the prompt | cited? |
|---|---|---|
| **(a) cost of closing** | "Closing now costs 0.060R in fees … That is 24% of the −0.25R currently unrealised." | ✅ *"Closing cost 0.060R (24% of unrealised) is acceptable"* |
| **(b) the stop is already there + the −1.00R floor** | "Current stop: 78301.6 (+0.75R away) … a STOP_MARKET order resting ON THE EXCHANGE … closes at −1.00R … that is the floor on holding" | ✅ *"−0.25R with 0.75R buffer to stop; holding risks full 1.0R stop-loss"* — 🔴 **this is the fact vpos 105's verdict did NOT cite. 106 did.** |
| **(c) what an early close surrenders** | "The trailing stop is NOT ARMED … It would arm if price reaches 75726.8 (+1R). A further 0.94R of favourable movement would arm it; **closing now gives that up**." | ⚠️ cited **but inverted** — *"Trailing stop not armed; no asymmetric upside protection exists"* is used as a **reason to close**. Neither 75 726.8 nor the 0.94R appears. **vpos 105 inverted the same fact the same way.** |
| **(d) direction of travel since last consult** | "Unrealised: −0.24R → −0.25R (−0.01R) · Peak (MFE): +0.06R → +0.06R (−0.00R)" | ✅ *"given back 0.31R from +0.06R MFE with **no fresh lower low**"* |
| **(e) the entry thesis, named tier by tier** | "1H: Any Bearish Confirmation (0.7) · 15m: HyperWave Signal Down (0.7) · 5m: Bearish I-CHOCH+ (0.9) — NOT counted by the gate …" | ✅ *"At entry, 15m+1h+5m aligned SHORT with ADX 31.0 … The bearish I-CHOCH+ at entry (weight 0.9) is contradicted by Bullish I-CHOCH 25m ago"* |

🔴 **EVERY NUMBER IT QUOTES IS CORRECT**, checked line by line against the stored 4 161-char prompt: ADX15m
31.0 → 14.1 (it said −54 %, the values give −54.5 %), ADX1h 21.9 → 11.1 (−49 % vs −49.3 %), supporting wall
×9.0 → ×7.0, opposing wall 90th pct, imbalance 0.60 → 0.54, giveback 0.31R from +0.06R MFE, 11.2h elapsed,
−0.25R unrealised, +0.75R to stop, −1.00R floor, closing cost 0.060R = 24 %.
**No misreading of the vpos 104 / 105 class was found.** It honoured the 🔴 UNPAIRED warning — it asserted no
1d/4h/1h *trend* change and used only ADX1h, which the prompt does render on both lines — and it stated the
90th-percentile opposing wall as a **NOW** value, never as a change, which is exactly what that block demands.
*(Its one non-prompt assertion is "11.2h elapsed suggests trapped liquidity" — an inference, not a misquote.)*

**THE ARM, ASKED FOR EXPLICITLY: arm price = 77 014.2 − 1 287.4 = 75 726.8. Water mark 76 936.5. NOT REACHED —
by 1 209.7 points, which is 0.94R.** The trail was never armed and the stop was still the original 78 301.6 at
the close. The prompt rendered the unarmed form and said so.

### 2e. 🔴 THE LEDGER, UPDATED

| # | vpos | side | closed | advisor R (net $) | counterfactual exit | counterfactual R (net $) | Δ R | Δ $ |
|---|---|---|---|---|---|---|---|---|
| 1 | 101 | SHORT | 09-01 18:00 | +0.2956 (+0.57) | **trail** 77 124.0 at 09-01 19:00 — armed 18:39 | +0.4509 (+0.87) | **−0.1553** | −0.30 |
| 2 | 104 | LONG | 09-09 08:30 | +0.5757 (+0.79) | **ORIGINAL STOP** 78 350.1 at 09-09 15:11 — +1R 79 874.7 never printed | −1.1033 (−1.51) | **+1.6791** | +2.30 |
| 3 | 105 | SHORT | 09-09 23:46 | −0.0136 (−0.03) | 🔴 **trail** 77 393.9 at 09-10 14:56 — armed 09-10 12:38 | +0.7669 (+1.50) | **−0.7805** | −1.53 |
| 4 | 106 | SHORT | 09-12 09:15 | −0.2963 (−0.72) | **UNRESOLVED** — stop never touched, arm never reached | pending (m-t-m −0.3354) | **pending** | pending |
| | | | | | | **Σ RESOLVED (3)** | **+0.7433** | **+$0.47** |

🔴 **NEW RUNNING TOTAL: 4 observed · 3 RESOLVED of 10 · Σ(advisor − counterfactual) = +0.7433R / +$0.47,
IN THE ADVISOR'S FAVOUR.**

### 2f. 🔴 HOW LONG UNTIL THE RULE DECIDES — **7 RESOLVED CLOSES REMAIN**

Titan's measured `ai_exit` rate in this era: **4 closes in 13.02 days = one per 3.26 days** (one per 3.55 days
on an interval basis), and `ai_exit` is **67 % of all live closes** (4 of 6 since vpos 101; the other two were
stops). Seven more is **≈ 23–25 days ≈ 3.5 weeks — the first week of October 2026**, plus each counterfactual's
own resolution lag (1h, 6.7h and 39h for the three so far). **That is three intervals of evidence, so treat it
as an order of magnitude, not a date.**

**`EXIT_ADVISOR_DRYRUN` is still `False`. I did not flip it and nothing here asks you to.**

---

## 3. THE OPERATOR'S QUESTION — ANSWERED WITH THE LEDGER

### 3a. Every live `ai_exit` close from vpos 101 onward

| vpos | side | closed (UTC) | R realised | $ realised | counterfactual R | counterfactual $ | **Δ R** | **Δ $** | state |
|---|---|---|---|---|---|---|---|---|---|
| 101 | SHORT | 09-01 18:00:19 | +0.2956 | +0.5725 | +0.4509 | +0.8732 | **−0.1553** | **−0.3007** | RESOLVED |
| 104 | LONG | 09-09 08:30:21 | +0.5757 | +0.7900 | −1.1033 | −1.5139 | **+1.6791** | **+2.3038** | RESOLVED |
| 105 | SHORT | 09-09 23:46:03 | −0.0136 | −0.0267 | +0.7669 | +1.5037 | **−0.7805** | **−1.5304** | RESOLVED |
| 106 | SHORT | 09-12 09:15:10 | −0.2963 | −0.7248 | −0.3354 (m-t-m) | −0.8204 | *(+0.0391)* | *(+0.0956)* | 🔴 **UNRESOLVED** |
| | | | | | **Σ over the 3 RESOLVED** | | **+0.7433** | **+$0.4727** | |
| | | | | | *(memo: incl. the open one)* | | *+0.7823* | *+$0.5683* | *not the rule's measure* |

### 3b / 3c. 🔴 THE SUM IS **POSITIVE**. And here is why that is not reassuring.

**Σ = +0.7433R / +$0.47 over 3 resolved closes. It is NOT negative, so it is NOT grounds to flip.**

🔴 **But the sign is carried entirely by ONE trade.** Remove vpos 104 and the remaining two are
**−0.9358R / −$1.83**. The expensive mistakes, named:

* 🔴 **vpos 105 — −0.7805R / −$1.53. The big one.** Closed at −0.01R on 09-09 23:46. Price then fell, armed the
  trail 12.8 hours later at 12:38, and the trail paid **+0.77R**. The verdict that closed it did **not** cite
  fact (b) at all and inverted fact (c).
* **vpos 101 — −0.1553R / −$0.30.** Closed at +0.30R on 09-01 18:00. The trail armed **39 minutes later** at
  18:39 and paid +0.45R.
* **The one save, vpos 104, +1.6791R / +$2.30** — a **LONG**, closed at +0.58R, whose hold ran straight into the
  **original stop** at 15:11 for −1.10R. It never came within 137 points of its +1R arm.

**THE SHAPE, STATED AND EXPLICITLY NOT RANKED:** both losses are **SHORTS closed in front of a move that armed
the trail after the advisor had already exited**. The one gain is a **LONG whose hold hit the original stop**.
The fourth observation, vpos 106, is another short — currently marginally *for* the advisor. **2 shorts
negative, 1 long positive, n = 3.** That is three numbers, not a finding, and the rule deliberately waits for
10 before anyone acts on it. **No later pass may cite this cell as an effect.**

### 3d. 🔴 NOT POOLED with the pre-2026-08-30 population

vpos 87–98 (−$5.85 under the two-sentence prompt) are a **different instrument**: a different prompt, without
the five facts, and before the 1 200-char reason cap. The population here begins at **vpos 101** by the canon's
own definition. **They are not added, not averaged, and not mentioned in any total above.**

---

## CONTROLS

| | |
|---|---|
| `openitems_guard` | **EXIT=0** at session start · **EXIT=0** after the restart · **EXIT=1** on my stale header (caught, fixed) · **EXIT=0** final |
| flat before the copy | 0/0/0 DB · BingX both probes empty · **error list empty** |
| flat before the restart | re-probed 14:17:50, identical |
| boot | `RECONCILE-XDB ✅ 0 exchange position(s), 0 open row(s)` · 0 errors |
| book-gate counter | **22 of 200**, 0 refusals — unchanged, unreachable from this pass |
| `BOOK_GATE_DRYRUN` / `CLAUSE_B` / `EXIT_ADVISOR_DRYRUN` | **False / False / False** — read from `config` at runtime |
| 🔴 **Mercury-SOL** | **NOT TOUCHED.** `active`, MainPID **1341949**, `NRestarts 0`, `ActiveEnterTimestamp Fri 2026-09-11 18:26:59 UTC` — unchanged. `find mercury-sol -newermt '2026-09-12 14:10'` → **EMPTY**, not one file of any kind. |
| commit | `7b17e11` — `signal_tiers.py` + `tests/` (4 files, +372 / −2) |
| rollback | `cp signal_tiers.py.bak_matrixnames_20260912T141553Z signal_tiers.py` + restart from flat. One file. |
| canon | `§0.MATRIX-TIER-NAMES` written as APPLIED · `§0.EXIT-ADVISOR-RULE` updated to 3 of 10 · header → `7b17e11` · 0 lines lost, verified against the backup |
| 🔴 open | the in-process `.pyc` confirmation for `signal_tiers` — lazy import, no consultation yet since 14:18. Watcher running; it goes in the next report. |
