# Titan — the unarmed-trail fact now LEADS WITH THE OPTION. The inversion was **3 of 4**, not 2 of 4 — vpos 101 did it too.

**2026-09-12 15:20 UTC · commit `f16c271` · Titan LIVE REAL MONEY · Mercury-SOL NOT TOUCHED**

---

## WHAT YOU ASKED, ANSWERED FIRST

1. 🔴 **The defect is worse than the brief said. It is 3 of the 4 positions closed under this wording, not 2.**
   **vpos 101 inverted it too** — *"Holding exposes the position to deteriorating thesis with no trailing stop
   yet armed."* (`trades 29123`). vpos 101 is also a ledger loss, **−0.1553R**.
2. 🔴 **The split is total. All 3 verdicts that used the trail's absence as a reason TO CLOSE are CLOSES. All
   16 that read it as something FORGONE are HOLDS.** 19 of 33 consultations mention it at all.
3. 🔴 **Only 1 verdict of 33 ever quoted the arm PRICE.** You were right: a fact nobody quotes is a fact nobody
   used. The arm price now appears **twice** in the sentence and the gap is given in price as well as R.
4. **The mirror is clean and the population is not larger.** The ARMED branch shows **no inversion in any of its
   4 rows ever**. And the entry prompt **does not contain the fact at all** — **0 of 3,075** entry
   consultations — so the **2,841 skip verdicts cannot invert it**.
5. 🔴 **I found a SECOND legibility defect in the same sentence** and fixed it by label only, changing no value:
   `0.94R` was measured from the **peak**, not from the current price. From the current price vpos 106 needed
   **1.25R**. The sentence read as "from here" and **understated the required move by 0.31R**.
6. **Applied from a proven-flat book, restarted 14:58:32 UTC, and LOADED — confirmed from the regenerated
   bytecode**, `claude_advisor.cpython-312.pyc` at 14:58:34, header == source, sha `e88d7fe634973e90`.
7. 🔴 **The ledger is untouched: 4 observed / 3 RESOLVED of 10, Σ +0.7433R.** This creates a **cohort boundary
   at 2026-09-12 14:58:32 UTC** and the 7 remaining closes must be read against it.

`openitems_guard` **EXIT=0** at the start of this session, and **EXIT=0** after the restart and after the canon
writes.

---

## 0. THE GUARD, AND THE FLAT PROOF

```
openitems_guard — titan-bot HEAD : 7b17e11   <- the SUBJECT
  watched values : 14
✅ header and current-state table agree with runtime.          EXIT=0
```

🔴 **FLAT, on the DB and on the venue, both probes, empty error list** — proved at 14:56:50 before the copy and
**re-proved at 14:58:20 immediately before the restart**, identical both times:

```
open virtual_positions (status='open')   0     (6 rows are 'archived_pre_geometry_fix', historical)
exit_pending                             0 rows
breakeven_jobs                           0 rows

=== BingX PROBE (doubled: unified fetch_positions + raw swapV2PrivateGetUserPositions, UNION) ===
positions dict : {}          position errors: []      <- EMPTY, not "unknown"
open orders    : {}          order errors   : []
ALL-symbol non-zero positions: []
```

---

## 1. THE MEASUREMENT

### 1a. The two branches, verbatim, with line numbers

`claude_advisor.py`, inside `consult_for_close_rich._protection_block` (defined at **:766**):

**The UNARMED branch — `:786-799`, the subject of this pass:**
```python
786         else:
787             arm = c.get('arm_level')
788             arm_s = (f" It would arm if price reaches {arm:.1f} (+1R)."
789                      if isinstance(arm, (int, float)) else "")
790             # 🔴 2026-08-30 — how far the arm still is, in R. Four of the nine
791             # unarmed live positions the advisor closed WOULD have armed later:
792             # it exited before the runner existed. Stated as distance, not advice.
793             ad = c.get('arm_dist_r')
794             if isinstance(ad, (int, float)):
795                 arm_s += (f" A further {ad:.2f}R of favourable movement would arm it; "
796                           f"closing now gives that up.")
797             head = ("If you HOLD: the stop-loss is in place. The trailing stop is "
798                     "NOT ARMED — it arms only at +1R, which this position has not "
799                     "reached, so the stop is the only protection." + arm_s)
```

**The ARMED branch beside it — `:783-785`, untouched by this pass:**
```python
783         elif armed:
784             head = ("If you HOLD: the stop-loss is in place AND the trailing stop is "
785                     "ARMED (it armed at +1R and now follows the high-water mark).")
```
🔴 **Read them side by side and the defect is visible without any data.** The armed branch leads with the thing
that exists. The unarmed branch leads with `NOT ARMED` and closes its first clause with *"the stop is the only
protection"* — and the option, the arm price and the distance all arrive **afterwards, in a subordinate
sentence**. `"no asymmetric upside protection exists"` is the natural completion of that opening.

### 1b. Every stored exit consultation, by prompt era

Classified by what the stored prompt actually contains, not by date:

| era | what fact (c) said | rows | window |
|---|---|---|---|
| 0 | no protection block at all | 61 | 2026-07-26 22:06 → 2026-08-30 16:30 |
| A | armed state only | 4 | 2026-07-31 14:15 → 2026-08-30 17:05 |
| B | + the arm price | 93 | 2026-07-29 13:30 → 2026-08-30 15:05 |
| 🔴 **C** | **+ the distance and "closing now gives that up"** | **33** | **2026-08-30 16:05:43 → 2026-09-12 09:15:09** |

**Era C is the population this pass is about: 33 consultations, ALL LIVE, and ALL unarmed by construction** —
the clause only renders in the unarmed branch. 28 `hold`, 5 `close`.

### 1c. 🔴 THE COUNT

| | count |
|---|---|
| era-C consultations | **33** |
| verdicts that mention the trail | **19** |
| 🔴 …that use its **ABSENCE** as a reason **TO CLOSE** | **3 — and all three are CLOSES** |
| …that read it as something **FORGONE** | **16 — and all sixteen are HOLDS** |
| verdicts that never mention it | 14 |
| 🔴 verdicts that quoted the arm **PRICE** | **1 of 33** |
| verdicts that quoted the gap in R | 13 of 33 |

**THE THREE INVERSIONS, QUOTED VERBATIM AND IN FULL CONTEXT:**

* 🔴 **`trades 29123` · 2026-09-01 18:00:17 · vpos 101 · CLOSE · conf 0.72** — *the one the 14:30 report missed*
  > "…The core confluence that justified entry—agreement across 15m/1H/5m—is now fractured: 1H signal dead, 15m
  > aging, 5m structure inverted by recent bullish OB/BOS/breaker. **Holding exposes the position to
  > deteriorating thesis with no trailing stop yet armed.** The 15m_exit_confirm trigger reinforces this timing.
  > Close to preserve the gain before thesis decay erodes it further."

  *(Prompt said: arm 76 641.6, a further 0.57R. Ledger Δ **−0.1553R / −$0.30** — the counterfactual trail armed
  **39 minutes later** and paid +0.45R.)*

* 🔴 **`trades 31259` · 2026-09-09 23:46:01 · vpos 105 · CLOSE · conf 0.72**
  > "…closing cost of 0.076R (114% of current unrealised +0.07R) is material but justified: the thesis is no
  > longer valid, **trailing stop won't arm (needs +1R)**, and holding into a reversed regime on lower TFs risks
  > holding through the actual reversal into loss."

  *(Prompt said: arm 77 231.3, a further 0.50R. Ledger Δ **−0.7805R / −$1.53 — the largest loss on the ledger.**
  The counterfactual armed 12.8h later and the trail paid +0.77R.)*

* 🔴 **`trades 31884` · 2026-09-12 09:15:09 · vpos 106 · CLOSE · conf 0.72**
  > "…Closing cost 0.060R (24% of unrealised) is acceptable vs thesis death and deteriorating technicals.
  > **Trailing stop not armed; no asymmetric upside protection exists.**"

  *(Prompt said: arm 75 726.8, a further 0.94R. Ledger: **UNRESOLVED**.)*

**The fourth position, vpos 104, never mentioned the trail at all** — its two rows (`31113`, `31115`) are the
pre-`§0.CONSULT-LOCK` double consult. It is the ledger's **only positive** close, **+1.6791R**.

🔴 **n, PLAINLY: 3 of the 4 positions closed in era C. 3 of the 5 close ROWS. 3 of the 3 close verdicts that
mentioned the trail at all. 3 of 33 consultations.** The brief said *two of four*; the full sweep found
**vpos 101 as well**, and vpos 101 is also a negative-delta close. **Every inverting close is a ledger loss;
the one close that did not mention the fact is the ledger's only gain.** That is a correlation over four
positions with the reading and the decision produced by the same call — **stated, and explicitly not ranked.**

### 1d. The 16 correct readings — the same fact, read the right way round

Sixteen verdicts treated it as something forgone, and **every one of them held**. A sample, verbatim:
```
31235  "…forfeits the trailing-stop arming opportunity at +1R."
31239  "Trailing stop arms at +1R (need 0.72R further move), creating asymmetric upside."
31247  "…premature exit before +1R activation would lock small gains and forgo asymmetry."
31250  "…holding preserves upside to +1R trailing-stop arm at 77231.3."   <- 🔴 the ONLY verdict of 33
                                                                             that ever quoted the arm PRICE
31790  "Hold to preserve trailing-stop armament opportunity (+0.94R away)…"
31860  "The trailing stop remains disarmed; if price reverses hard into the 1h structure,
        the stop will catch it."
```

### 1e. 🔴 THE MIRROR — the ARMED branch is never inverted

**Four rows in the entire record.** `25159` is a `claude timeout` with no verdict. `20097` (CLOSE, 2026-07-31)
was truncated by the old reason cap before reaching the trail. The two that discuss it read it correctly:
```
25165  HOLD  "+1.13R gain with trailing stop 0.81R away provides solid risk/reward."
28531  HOLD  "With stop-market resting on exchange and trailing protection armed, downside is
              contained. Let trailing stop work…"
```
🔴 **When the sentence leads with ARMED, the reading is right. When it leads with NOT ARMED, three of three
closes read it backwards. That is the diagnosis, and it is about our wording, not the model's arithmetic** —
the 14:30 report §2d verified every number vpos 106 quoted against its stored prompt and all were correct.

### 1f. 🔴 THE SKIP VERDICTS — the population is NOT larger

| entry consultations with a stored prompt | **3 075** (2 841 `skip`, 208 `execute`, 26 `unavailable`) |
|---|---|
| containing `NOT ARMED` | **0** |
| containing `would arm` | **0** |
| containing `trailing stop` | **0** |
| containing `+1R` | **0** |

**The entry prompt does not carry this fact in any form.** The 2 841 skip verdicts cannot invert a fact they
were never shown. **The exposed population is the 33 exit consultations and nothing else.**

### 1g. 🔴 A SECOND DEFECT IN THE SAME SENTENCE, FOUND WHILE REWRITING IT

`arm_dist_r` is `max(0, 1 − mfe_r)` (`main.py:3447`) — **how far the PEAK is from the arm, not how far the
current price is.** On vpos 106:
```
arm 75726.8 · current price 77330.9 · gap in price = 1604.1
  that gap in R (1R = 1287.4)  = 1.25R   <- the move actually required FROM HERE
  the prompt stated              0.94R   <- = 1 - MFE(+0.06R), measured from the PEAK
```
*"A further 0.94R of favourable movement would arm it"* reads as *from here*, and **understated the required
move by 0.31R**. Both numbers are true statements of different things; only the label was wrong.
🔴 **I changed the LABEL, not the VALUE** — the same 0.94R now reads *"the peak reached so far came within
0.94R of it"* — and added the gap in **price** from the current price, which is unambiguous. **No computed
value anywhere is redefined.** Flagged here as a finding in its own right, as the `build()` "never raises"
defect was on 2026-09-12 00:20.

---

## 2. THE FIX

### 2a. The new wording

```
If you HOLD: the stop-loss is in place. The trailing stop ARMS AT 75726.8 (+1R): reaching
that price moves the stop to breakeven, and the trail then follows the high-water mark from
there. From the current price that is a move of 1604.1 in the position's favour. The peak
reached so far came within 0.94R of it. Until 75726.8 prints, the trail does not exist and
the stop is the only protection. Closing now ends that possibility.
```
* **The option leads.** `ARMS AT 75726.8` is the first thing said about the trail; the absence is now a
  temporal clause (`Until 75726.8 prints…`) that arrives after it.
* 🔴 **The arm price appears TWICE, so it is quotable**, and the gap is given in **price** (1604.1) as well as
  in R (0.94R). Pinned by contract case [4].
* **What arming does is stated**: it moves the stop to breakeven and the trail then follows the high-water
  mark — Titan's actual mechanism (`breakeven_worker:754-770`, `virtual_trader:2667-2755`).
* **FACTS ONLY.** No *therefore*, no *consider*, no *should*, no threshold, no lean — contract case [6] fails
  the build if any of twelve such words appears. The 2026-08-05 line holds: give the model the fact, let it
  weigh.
* `arm_level` and `price` were **already in the context**, so the gap is computed inside the builder and
  **`main.py` is not touched**.

### 2b. BEFORE / AFTER on vpos 105's and vpos 106's OWN stored prompts

The ctx values below are read back **out of the two stored prompts**, so these are the exact numbers those two
consultations were given.

**vpos 106 · trades 31884** — `arm_level 75726.8 · arm_dist_r 0.94 · price 77330.9 · sl 78301.6`
```
===== BEFORE (the builder on disk) =====
If you HOLD: the stop-loss is in place. The trailing stop is NOT ARMED — it arms only at +1R, which this position has not reached, so the stop is the only protection. It would arm if price reaches 75726.8 (+1R). A further 0.94R of favourable movement would arm it; closing now gives that up.
  Current stop: 78301.6 (+0.75R away).
  That stop is a STOP_MARKET order resting ON THE EXCHANGE, not a software check:
  it stands whether or not this process is running and needs no action from you.
  If it fills, the position closes at -1.00R from the entry — that is the floor
  on holding, before slippage and fees.

===== AFTER =====
If you HOLD: the stop-loss is in place. The trailing stop ARMS AT 75726.8 (+1R): reaching that price moves the stop to breakeven, and the trail then follows the high-water mark from there. From the current price that is a move of 1604.1 in the position's favour. The peak reached so far came within 0.94R of it. Until 75726.8 prints, the trail does not exist and the stop is the only protection. Closing now ends that possibility.
  Current stop: 78301.6 (+0.75R away).
  That stop is a STOP_MARKET order resting ON THE EXCHANGE, not a software check:
  it stands whether or not this process is running and needs no action from you.
  If it fills, the position closes at -1.00R from the entry — that is the floor
  on holding, before slippage and fees.

===== unified diff, whole block =====
--- before
+++ after
@@ -1,2 +1,2 @@
-If you HOLD: the stop-loss is in place. The trailing stop is NOT ARMED — it arms only at +1R, which this position has not reached, so the stop is the only protection. It would arm if price reaches 75726.8 (+1R). A further 0.94R of favourable movement would arm it; closing now gives that up.
+If you HOLD: the stop-loss is in place. The trailing stop ARMS AT 75726.8 (+1R): reaching that price moves the stop to breakeven, and the trail then follows the high-water mark from there. From the current price that is a move of 1604.1 in the position's favour. The peak reached so far came within 0.94R of it. Until 75726.8 prints, the trail does not exist and the stop is the only protection. Closing now ends that possibility.
   Current stop: 78301.6 (+0.75R away).

  [pin] with arm_level absent, AFTER == BEFORE byte for byte: True  (570 chars)
```

**vpos 105 · trades 31259** — `arm_level 77231.3 · arm_dist_r 0.50 · price 78194.6 · sl 79295.1`
```
===== BEFORE =====
If you HOLD: the stop-loss is in place. The trailing stop is NOT ARMED — it arms only at +1R, which this position has not reached, so the stop is the only protection. It would arm if price reaches 77231.3 (+1R). A further 0.50R of favourable movement would arm it; closing now gives that up.
  Current stop: 79295.1 (+1.07R away).
  … (the stop / exchange-side / -1.00R floor lines, unchanged)

===== AFTER =====
If you HOLD: the stop-loss is in place. The trailing stop ARMS AT 77231.3 (+1R): reaching that price moves the stop to breakeven, and the trail then follows the high-water mark from there. From the current price that is a move of 963.3 in the position's favour. The peak reached so far came within 0.50R of it. Until 77231.3 prints, the trail does not exist and the stop is the only protection. Closing now ends that possibility.
  Current stop: 79295.1 (+1.07R away).
  … (identical)

  [pin] with arm_level absent, AFTER == BEFORE byte for byte: True  (570 chars)
```
🔴 **The diff is one line long in both cases. Nothing below it moves.**

### 2c. The contract — 9 of 9 green as root AND as botuser

`tests/test_exit_prompt_arm_leads_with_the_option.py`, run against the **applied file** and the **`.bak` it
replaced**:
```
  [0] ARMED branch byte-identical to the pre-change builder: True
  [1] armed-state-UNREADABLE branch byte-identical: True
  [2] unarmed WITHOUT a usable arm price == pre-change builder, byte for byte, for all 60 input shapes: True
  [3] new wording exact on vpos 106: True
  [4] arm price and gap are quotable numbers, option first: True
  [5] every other fact (stop, exchange-side, -1.00R floor) byte-identical: True
  [6] no instruction / threshold / lean word in the new text: True
  [7] _CLOSE_SYSTEM / _CLOSE_SYSTEM_RICH / _ENTRY_SYSTEM / _LEARNING_SYSTEM sha256 unchanged: True
  [8] the ENTRY consultation builder source is unchanged: True
OK   EXIT=0        — identical output as root and as botuser
```
Case **[2]** is the strong one: **60 input shapes** (`arm_level` ∈ {absent, `'nonsense'`, `[]`, `{}`, an object}
× `arm_dist_r` ∈ {absent, 0.94, `'abc'`, `[1]`} × `price` ∈ {absent, 77330.9, `'x'`}) — every one renders
**byte-identical to the pre-change builder**, including its old distance clause, and **none raises**. Case
**[4]** is the one you asked for: the arm price present, present **twice**, the price gap present, the R figure
present, and `ARMS AT` positioned **before** the absence clause.

🔴 **The botuser run, stated plainly because it is not the applied path.** `/root` is `drwx------`, so botuser
cannot read `/root/titan-bot/claude_advisor.py` at all — which is also why titan's unit is `User=root`. The
botuser pass used **sha256-pinned byte copies** in a traversable directory, and the pins are printed:
```
e88d7fe634973e90…  /root/titan-bot/claude_advisor.py                  <- applied
e88d7fe634973e90…  <botuser dir>/claude_advisor.py                    <- identical
ca14e959a5c6104c…  /root/titan-bot/claude_advisor.py.bak_armlead_…    <- baseline
ca14e959a5c6104c…  <botuser dir>/claude_advisor.py.bak_armlead_…      <- identical
462889e6806f10b6…  /root/titan-bot/tests/test_exit_prompt_…py         <- installed contract
462889e6806f10b6…  <botuser dir>/tests/test_exit_prompt_…py           <- identical
1dc387744a976d54…  config.py, both sides                              <- identical
```
This contract reads no crontab, so the 2026-08-27 botuser rule does not bind it; it was run both ways anyway.
The temporary directory was removed afterwards.

### 2d. 🔴 The two close SYSTEM prompts — sha256-identical, proved twice

Once by the contract (case [7], from the loaded module objects) and once by AST off the applied file:
```
  _ENTRY_SYSTEM         1871 chars  30c979595a4831aa751db8bd64d7bcb4…  unchanged: True
  _LEARNING_SYSTEM       730 chars  191cf5d71ebf3865535f8e0bfb09106a…  unchanged: True
  _CLOSE_SYSTEM          452 chars  7d7707cfa2d336f75f690eba53114fed…  unchanged: True
  _CLOSE_SYSTEM_RICH     252 chars  3d709571e17ff4051362c5a50496c74c…  unchanged: True
  ALL FOUR UNCHANGED: True
```
**The other four facts were not touched** — contract case [5] pins every line below the first byte-identical on
both real prompts.

---

## 3. THE APPLY

### 3a. Backup and shas
```
claude_advisor.py                                ca14e959a5c6104c8438ddc493750d4193a0a32bfab49312b30eff2eb1a8c6c6  (before)
claude_advisor.py.bak_armlead_20260912T145700Z   ca14e959a5c6104c…  <- byte-identical to the file it replaced
claude_advisor.py                                e88d7fe634973e903d7292cefd47a529e0efc8698797ea59b6e30d3f938af4ac  (after)
                                                 == the sandbox patched file, byte for byte
```

### 3b. AST proof — only the exit-prompt builder changed
```
claude_advisor.py  sha256 ca14e959a5c6104c -> e88d7fe634973e90
  top-level named nodes ADDED   : []
  top-level named nodes REMOVED : []
  text diff: +47 lines, -11 lines
  unarmed else-branches stripped: before=1 after=1 (expect 1 and 1)

  after stripping ONLY that branch: AST identical = True
  functions whose AST differs after the strip: NONE
  module-level constants that differ: NONE  (7 checked)
AST PROOF PASS
```
**Strip that one `else:` body out of both trees and the two files are `ast.dump`-identical.** No function
anywhere else in the file differs; no module-level constant differs; nothing added, nothing removed.
**`main.py`, `config.py`, `signal_tiers.py`, `virtual_trader.py` and `breakeven_worker.py` are zero bytes of
this change.**

### 3c. Untouched at runtime, read by importing `config`
| value | reading |
|---|---|
| `SL_ATR_MULT` / `TRAIL_MULT_ATR` | **2.25** / **1.6875** |
| EMA envelope gate | `ENABLED` **True** · `TFS` `('1h','15m')` · `REQUIRED_DIR` `Expanding` · `FAIL_OPEN` **True** |
| `LONG_PARTIAL_ENABLED` | **False** |
| `CONFLUENCE_SCORE_THRESHOLD` / `_FLAT_` | **3.0** / **5.0** |
| 🔴 `EXIT_ADVISOR_DRYRUN` | **False** — unchanged, not flipped |
| 🔴 `BOOK_GATE_ENABLED` / `_DRYRUN` / `_CLAUSE_A_` / `_CLAUSE_B_` | **True / False / True / False** |
| `LIVE_TRADING_ENABLED` / `ORDER_ADAPTER_LIVE` | **True** / **True** |
| size | `LEVERAGE` **5** · `LIVE_FIXED_MARGIN_USDT` **30.0** · `PAPER_FIXED_MARGIN_USDT` **2000.0** |
| `MAX_POSITIONS_PER_SIDE` / `AI_ADVISOR_HIDE_1H` | **1** / **False** |

### 3d. Restart from flat — the boot line
```
MainPID  1563560 -> 1572470    NRestarts 0    ActiveEnterTimestamp Sat 2026-09-12 14:58:32 UTC

14:58:36  [TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
14:58:36  [TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
14:58:36  [TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
14:58:36  [TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
🔴 14:58:41  [TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
14:58:41  [RECONCILE] boot reconciliation starting
14:58:43  [STOP-CLEANUP] no orphaned orders for LONG BTC/USDT:USDT
14:58:43  [STOP-CLEANUP] no orphaned orders for SHORT BTC/USDT:USDT
14:58:43  [RECONCILE] done
14:58:43  breakeven_worker started (interval=5s)
14:58:43  virtual_trader worker started (interval=10s, target_cycles=30, closed=51/30, entries=65)
```
Zero errors, zero tracebacks.

### 3e. 🔴 LOADED — confirmed from the bytecode
```
  claude_advisor     pyc 2026-09-12 14:58:34  header==source: True   src sha e88d7fe634973e90   <- 🔴 THIS CHANGE
  config             pyc 2026-09-10 14:34:54  header==source: True   src sha 1dc387744a976d54
  main               pyc 2026-09-09 20:46:02  header==source: True   src sha 00c8be297a8de922
  signal_matrix      pyc 2026-08-05 22:47:31  header==source: True   src sha 0e4128911c283b2f
  state_machine      pyc 2026-08-21 19:44:21  header==source: True   src sha 7f5a21ea88662453
  virtual_trader     pyc 2026-08-30 15:16:19  header==source: True   src sha 3b0b49d9c5d4e092
  breakeven_worker   pyc 2026-08-06 01:08:00  header==source: True   src sha f76bede58d51b55b
  signal_tiers       pyc 2026-08-04 15:07:11  header==source: False  src sha 4af4fdba57cfaf84   <- still lazy, see below
```
`claude_advisor` is imported at module level by `main.py`, so the boot re-read it: **the `.pyc` was regenerated
at 14:58:34, two seconds after the boot, and its header matches the applied source.** The bytes the running
worker executes are `e88d7fe634973e90`.

### 3f. 🔴 THE 14:30 OPEN ITEM — STILL OPEN, AND I AM NOT DRESSING IT UP

The in-process `.pyc` confirmation for **`signal_tiers`** is **not closed**. It is a **lazy** import
(`claude_advisor.py:567`, `main.py:2999`) that first runs at an **entry consultation**, and there has been
**none** — 0 consultations between 14:18 and the 14:58 restart, and 0 since. Its `.pyc` is still the 2026-08-04
build. What remains proved, unchanged from 14:30: the cached header (`mtime 1785855983, size 15924`) disagrees
with the applied source (`mtime 1789222553, size 23584`), so **Python cannot load the old bytecode** and the
first import must compile `4af4fdba57cfaf84`. A fresh watcher is armed on that file:
```
watch armed 2026-09-12T14:59:35Z  baseline pyc mtime=1785856031 (the 2026-08-04 build)
```
**It goes in the next report, as a quoted header or not at all.**

---

## 4. RECORD

### 4a. `§0.ARMLEAD` written into the canon
Inserted beside `§0.PROMPT-PAIRING` — the same defect class — carrying the full 33-row count, all three
inversions verbatim, the two negative checks (armed branch, skip verdicts), the before/after, the second
labelling defect, the proofs and the cohort boundary. Header updated to `f16c271` with its own stanza.
**Nothing lost in the canon write: +7 667 bytes, +99 lines, 0 lines whose count decreased**, verified by
line-multiset against `OPEN-ITEMS.md.bak_armlead_20260912`.

### 4b. 🔴 WHAT THIS CANNOT DO

**It removes an inverted reading. It cannot stop a model concluding wrongly from correct facts.**
The precedent is on this record: on **2026-08-31** the SOL zeroed-tier label was already present on **all nine**
live cases and the narration built on the tier anyway. A clearer sentence is a necessary condition for a better
reading, not a sufficient one.

**Whether the advisor now holds where it used to close is UNKNOWN and UNMEASURABLE until it runs.** The
3-of-3 / 16-of-16 split is a **correlation over 19 verdicts and four positions**, in which the reading and the
decision were produced by the same model call — it cannot separate *"the wording caused the close"* from
*"a verdict that had decided to close reached for the nearest supporting clause"*. **No later pass may cite it
as an effect.** **This is LEGIBILITY, NOT A MEASURED EDGE.**

### 4c. 🔴 THE LEDGER IS UNAFFECTED — AND THIS IS A COHORT BOUNDARY

`§0.EXIT-ADVISOR-RULE` stands exactly where the 14:30 report left it:
**4 observed · 3 RESOLVED of 10 · Σ(advisor − counterfactual) = +0.7433R / +$0.47.**
Nothing in this pass resolves, re-scores or re-weights a single row. `EXIT_ADVISOR_DRYRUN` stays **False**.

🔴 **BOUNDARY: 2026-09-12 14:58:32 UTC.** Verdicts before and after that instant were shown **different wording
of the same fact**, so they are **not one population**. The **7 remaining closes** will all fall after it. When
the rule fires at 10, the sum must be reported **with the split stated** — 3 resolved under the old wording,
the rest under the new — or it will pool two instruments, exactly the error `§0.EXIT-ADVISOR-RULE` already
forbids against the pre-2026-08-30 book.

### 4d. Counters and the other bot

**Book-gate review counter — 22 of 200, UNDISTURBED, 0 refusals all time.**

| era | rows |
|---|---|
| DRYRUN, before the 2026-09-10 14:36:20 boundary | **15** |
| LIVE, after it | **7** |
| | **22 of 200** |

`status='book_blocked'`, all time: **0**. Latest gate row: `trades 31760`, 2026-09-11 22:00:11 — identical to
the 14:30 reading. Nothing in this pass reads, writes or can reach the gate.

🔴 **Mercury-SOL — NOT TOUCHED, proved not asserted.** `active`, **MainPID 1341949**, `NRestarts 0`,
`ActiveEnterTimestamp Fri 2026-09-11 18:26:59 UTC` — the process has been up since before this session and was
never signalled. `ps` confirms the master's start time is unchanged.
`find mercury-sol -name '*.py' -newermt '2026-09-12 14:40'` → **EMPTY**. The only files newer than this session
are the bot's **own** runtime writes — `oi_cache.json`, `trades.db`, `optimizer/tg_offset.txt` — which it wrote
itself while I did not touch it. No DB query, no restart, no venue call on its key.

---

## CONTROLS

| | |
|---|---|
| `openitems_guard` | **EXIT=0** at session start · **EXIT=0** after the restart · **EXIT=0** after the canon writes |
| flat before the copy | 0/0/0 DB · BingX both probes empty · **error list empty** (14:56:50) |
| flat before the restart | re-probed 14:58:20, identical |
| boot | `RECONCILE-XDB ✅ 0 exchange position(s), 0 open row(s)` · 0 errors |
| loaded | `claude_advisor.pyc` regenerated **14:58:34**, header == source, sha `e88d7fe634973e90` |
| AST | strip one `else` branch → identical; 0 functions, 0 of 7 constants, 0 top-level nodes differ |
| contracts | new: **9 of 9** as root and botuser · existing `test_entry_tiers_matrix_names_ages`: **EXIT=0** |
| SYSTEM prompts | all four sha256 **unchanged**, verified twice |
| `EXIT_ADVISOR_DRYRUN` | **False** — not flipped |
| book-gate counter | **22 of 200**, 0 refusals — unchanged |
| ledger | **4 observed / 3 RESOLVED of 10, Σ +0.7433R** — unchanged; cohort boundary 14:58:32 UTC |
| commit | `f16c271` — `claude_advisor.py` + the new contract |
| rollback | `cp claude_advisor.py.bak_armlead_20260912T145700Z claude_advisor.py` + restart from flat. One file. |
| 🔴 open | the in-process `.pyc` for **`signal_tiers`** — lazy import, still no consultation. Watcher armed 14:59:35. |
