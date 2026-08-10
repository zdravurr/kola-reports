# sol-the-book-gate-is-armed

_2026-08-10 19:00 UTC_

---

# APPLIED AND **ARMED**. The order book refuses entries on Mercury-SOL as of **18:25:21 UTC**. The restart cost vpos 32 nothing — **39 of 39 fields identical, the venue stop's `updatedTime` unchanged.**

```
BOOK_GATE_ENABLED = True    BOOK_GATE_DRYRUN = False    🔴 IT REFUSES
HARNESS: 49 assertions ✅  0 ❌  LEAKS 0   (21 of them armed-path-only)
RESTART: 18:25:01 → 18:25:21   vpos 32: 39/39 identical, 0 changed
         venue stop 986c263d… updatedTime 1786375294067 UNCHANGED — nothing written
🔴 AND THE RESTART SURFACED A DEFECT I DID NOT GO LOOKING FOR — §8. It booked a
   DUPLICATE close row for vpos 31. No money moved. Reported, not fixed.
```

Design (approved as built): [18:30 — the book enters the entry decision](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-10-1830-sol-the-book-enters-the-entry-decision.md)

---

## 1. APPLIED — four files

```
book_gate.py          NEW  +202  −0     9db28ddae0b5c27c80f0bece93f39439
config.py                  +88   −2     409f5dfe764fdcf00ec760d2f4423e65
main.py                    +100  −0     cac58ade071e481244755a63d45ca4ef
skip_attribution.py        +6    −1     6594c8b4ab334bd6b1c875124978f829
OPEN-ITEMS-SOL.md          +64   −0     (pre-registration, §5)
```

**Backups taken BEFORE the first edit and md5-verified identical to the originals:**
`*.bak_bookgate_20260810_1900` — `config.py a6e15f41…`, `main.py d98b55d1…`,
`skip_attribution.py 54d11eea…`, `OPEN-ITEMS-SOL.md 30e0570a…`.

**All three deleted lines, listed individually** — there are only three in the whole pass:

```
[config.py]
< WALL_AVOIDANCE_THRESHOLD_PCT = 0.35  # (advisory only — see WALL_AVOIDANCE_ENABLED)
< WALL_AVOIDANCE_ENABLED = False       # A2 2026-06-08: Titan parity — walls advisory-only…
        (both re-declared with IDENTICAL VALUES 0.35 / False plus the SUPERSEDED banner — §3)
[skip_attribution.py]
< TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked', 'risk_halt')
[main.py]
  (none)
```

🔶 **The 17:42 lesson was applied:** the syntax check compiled to a **temp directory**, not into
production `__pycache__`. The `.pyc` files now dated 18:25 were written **by the booting worker
itself**, which is normal and is exactly the deployment-gap evidence we want — they record what the
process actually loaded.

---

## 2. THE TWO SWITCHES DO DIFFERENT THINGS — both stated in the comment

```python
#   BOOK_GATE_ENABLED = False
#       STOPS IT COMPUTING. evaluate() returns immediately, no book is read, the
#       six book_gate_* columns are written EMPTY on every row, no card, no log.
#       This is the KILL SWITCH… Cost: the telemetry stops too, so you go blind
#       at the same moment.
#
#   BOOK_GATE_DRYRUN = True
#       STOPS IT BLOCKING, KEEPS EVERYTHING ELSE. The book is still read, the six
#       columns are still written on EVERY scored row (they are written BEFORE the
#       dryrun branch, deliberately), the would-refuse is still logged.
#       This is the OBSERVE switch: use it to keep measuring while not acting.
```

**Asserted at runtime, not just written:** `✅ both kill switches are documented with their
DIFFERENT effects`.

---

## 3. ⚰️ THE OLD DEAD GATE — MARKED SUPERSEDED AT ITS DECLARATION

You were right that leaving it silent is the "reads as armed, is not" class. It is now impossible
to read it as live without reading why it isn't:

```python
WALL_AVOIDANCE_THRESHOLD_PCT = 0.35  # ⚰️ SUPERSEDED 2026-08-10 — see below
WALL_AVOIDANCE_ENABLED = False       # ⚰️ SUPERSEDED 2026-08-10 by BOOK_GATE_* — DO NOT SET True
# ── ⚰️ SUPERSEDED 2026-08-10 BY THE BOOK GATE BELOW. DO NOT TURN THIS ON. ──────
# 🔴 MARKED AT ITS DECLARATION RATHER THAN LEFT LOOKING LIVE. The block it drives
# (main.py, "OKX wall avoidance filter") is named for OKX and READS THE WRONG
# VENUE: its `_near_ask` / `_near_bid` come from liquidity_zones.fetch_clusters,
# which is the BYBIT depth book — not the OKX books-full depth-4000 snapshot…
# It has been False since A2 on 2026-06-08 … and `status='wall_blocked'` has
# fired ZERO times in this bot's entire history.
# 🔴 TURNING THIS True WHILE BOOK_GATE_ENABLED IS True WOULD PUT TWO WALL GATES ON
# ONE FACT, on two different venues' books, with no defined precedence. Do not.
```

**Values are byte-identical — `0.35` and `False`.** Only the comment changed.

🔴 **Why the dead block was NOT deleted in this pass, said plainly rather than left as an
omission:** deleting live-path code is a behaviour change, and this pass already restarted a live
process with an open position. **One risk at a time.** The deletion is a separate, smaller pass and
is recorded as such in the canon.

---

## 4. RUNTIME CONFIRMATION — all four, and the one that matters most

### (a) It is reached BEFORE the advisor, and it reads the SAME object

Proved from the applied file's own line numbers, not from reading:

```
✅ 🔴 ORDER: fetch_pre_trade_walls :4610  <  book_gate.evaluate :4644  <  consult_for_entry :4718
✅ 🔴 SAME OBJECT: the gate is passed `_pre_walls`, and so is the advisor
```

### (b) The six columns exist and are written on ADMITTED rows too

```
sqlite> PRAGMA table_info(trades) | grep book_gate
  book_gate_clause  book_gate_opp_mult  book_gate_opp_pctl
  book_gate_opp_dist_pct  book_gate_lean  book_gate_n_supporting     ← all six, created at boot

✅ the six columns are written at :4659, BEFORE the refuse branch at :4665
   -> they accrue on ADMITTED rows too
```

### (c) 🔴 THE HOOK IS REGISTERED **AND ACTUALLY CALLED** — the half-fix you named

```
✅ 'book_blocked' in TRACKED_STATUSES
   ('ai_skipped', 'below_threshold', 'htf_blocked', 'risk_halt', 'book_blocked')   ← at runtime

✅ 🔴 _record_skip_attribution(..., 'book_blocked', ...) is ACTUALLY CALLED — 1 call site
      (found by walking the AST for a Call node whose args contain the literal
       'book_blocked' — not by grepping for the string, which the TRACKED_STATUSES
       tuple would also have matched)
✅ the hook sits inside `if not BOOK_GATE_DRYRUN` (:4670 < :4677)
✅ exactly one place writes status='book_blocked'
✅ exactly one Telegram refusal card
```

**That second assertion is the one that would have caught Titan's 518 vanished FLAT refusals.**
Registering the status and never calling the hook passes a grep and fails reality; this checks the
call graph.

### (d) 🔶 NOT YET EXERCISED BY A LIVE SIGNAL — stated, not glossed

```
rows since the restart : 17341 (no_trend)  — nothing has reached the entry path yet
[BOOK-GATE] journal lines : 0
tracebacks                : 0
```

**The gate is LOADED — `import book_gate` is module-level in `main.py`, so a clean boot is proof it
imported** — and every assertion above is against the applied files and the live DB. But **no
scored signal has reached it in the 6 minutes since the restart**, so the *executed* path is
asserted, not yet observed. At the historical rate (~55 signals/day reach the book) the first
`[BOOK-GATE]` line is expected within hours. **I am not calling that "live-proven" until a line
exists.**

---

## 5. 🔴 PRE-REGISTERED — written into the canon BEFORE the first refusal

| quantity | expected | source |
|---|---|---|
| refusal rate LONG | **2.20 %** | real `evaluate()` over 1,545 stored LONG books |
| refusal rate SHORT | **2.67 %** | real `evaluate()` over 1,909 stored SHORT books |
| side ratio | **1.21×** | |
| clause A | **~0.5 %** (0.26 L / 0.73 S) | |
| clause B | **~1.85 %** (1.88 L / 1.83 S) | |
| first refusal | **~29 days** | at the live-era rate of 1.44 positions/day |

🔴 **Above 5 % on either side, or a side ratio above 2×, is a finding about the calibration and
grounds to revisit — NOT a reason to loosen the threshold quietly.** The correct response to a
divergence is to re-cut the ruler from the current nearest-opposing-wall distribution *and say so*,
not to raise `BOOK_GATE_WALL_PCTL` until the refusals stop.

---

## 6. THE RESTART — the 2026-08-09 17:42 procedure, and where today differed

### Before, at 18:24:50 — snapshot taken, not remembered

```
vpos 32   SHORT 1.3 @ 76.18 · sl 77.32 · original_sl 77.32 · water_mark 75.6
          max_adverse 76.25 · initial_risk $1.482 · is_paper 0
          mgmt_state {"breakeven_applied": false, "exit_advisor_last_ts": 1786385763.910438}
venue     POSITION Sell 1.3 avg 76.18 stopLoss 77.32 idx=2 lev 5 tradeMode 0
          CONDITIONAL 986c263d-0cf5-4aaf-ac1f-84834aa7c94c Untriggered StopLoss
                      trigger 77.32 qty 1.3 reduceOnly
                      createdTime 1786374932610   updatedTime 1786375294067  ← the fingerprint
```

### 🔴 ONE THING WAS DIFFERENT FROM 08-09, AND I CHECKED IT RATHER THAN ASSUMING PARITY

```
2026-08-09 17:42 :  exit_pending EMPTY
2026-08-10 18:24 :  exit_pending HAS A ROW
                    side=SHORT  armed_at 18:00:15  expires_at 2026-08-11 00:00:15
                    source_signal 'Exit Signal'
```

**An armed exit was live on the open position.** Verified before restarting:

- **It is TABLE-persisted, not in-process** — `state_machine.is_exit_pending` reads
  `SELECT … FROM exit_pending`, so a restart cannot lose it.
- **No boot path clears it.** All three `clear_exit_pending` call sites (`main.py` 3774 / 5134 /
  5571) sit *after* an actual close, none on boot.
- **It self-expires** at 2026-08-11 00:00:15.
- ✅ **Confirmed present, byte-identical, after the restart.**

🔶 **The residual risk, stated rather than hidden:** a 5m opposite-direction webhook landing inside
the ~20 s restart window would have been lost. None arrived — the restart ran at :24:58, and the
next row is 18:30:19. This is the ordinary cost of any restart, and it is the reason the restart
was issued at :58 rather than on a 5-minute boundary.

### After — field by field, machine-compared

```
fields compared : 39
IDENTICAL       : 39
CHANGED         :  0
```

`size 1.3` · `sl_price 77.32` · `water_mark 75.6` · `mgmt_state_json` unchanged (**`breakeven_applied`
still false, `exit_advisor_last_ts` intact**) · `fills_json` unchanged · `status open` · `is_paper 0`.

### 🔴 The venue stop was never written to

```
orderId       986c263d-0cf5-4aaf-ac1f-84834aa7c94c  ->  same
orderStatus   Untriggered  ->  Untriggered
triggerPrice  77.32        ->  77.32
qty           1.3          ->  1.3
createdTime   1786374932610 -> 1786374932610
updatedTime   1786375294067 -> 1786375294067      🔴 UNCHANGED
stop-order fields changed: NONE
```

The only difference anywhere on the venue is `unrealisedPnl 0.325 → 0.2249` — the mark moved.
`curRealisedPnl` is identical.

**Boot took the managed branch at every gate:**

```
[SMART-CLEANUP] Skipping stop cancel — position still open on exchange
[BOOT-ASSERT] SHORT open on venue and booked in the DB — consistent
[VPOS-RECONCILE] OPEN vpos=32 SHORT book=LIVE entry=76.18 sl=77.32 age=3.2h
                 — poller continues managing it (no auto-close)
```

🔶 That `book=LIVE` is the 2026-08-09 boot-card fix rendering **for the first time**. It would have
said "paper".

---

## 7. 🔴 vpos 32 STAYS OPEN

**The rule would have refused its entry.** Clause B: the book leaned **0.343** against the short —
**the minimum of all 1,909 SHORT signals ever scored, percentile 0.00.** The bot sold into the
heaviest bid support in 63 days.

**It does not refuse an existing position.** The gate governs **entries**. Closing a position
retroactively on a rule that was not live when it opened is not something this gate does, and
nothing in this pass touched the position, its stop, or its armed exit. It is managed exactly as it
was at 18:24, by the same poller, against the same venue stop at 77.32.

---

## 8. 🔴 THE DEFECT THE RESTART SURFACED — I CAUSED IT, IT COST NO MONEY, AND IT IS NOT FIXED

**Booting wrote a duplicate close row for vpos 31**, which had already closed at 15:21:44:

```
[AP] RECONCILED: LONG SOL/USDT:USDT closed on exchange while bot was down
     — recovering realized PnL (dryrun=False)
[CLOSE-ENTRY] newest LONG row is vpos 31, closed at '…15:21:44' — too old to be the
     position just closed. REFUSING to price the close card.
[AP] Recorded reconcile close row 17340: close_long pnl=-1.455432
```

```
row 17296  15:21:44  sl_triggered_long  75.9  1.2  pnl −1.45543199999999  fee 0.09108   ← the real close
row 17340  18:25:19  close_long         75.9  1.2  pnl −1.455432          fee NULL      ← 🔴 PHANTOM
```

**Root cause.** `_register_active_position` writes the LONG into the `active_positions` table at
entry; **the engine's own close does not remove it.** vpos 31 was closed by the engine at 15:21:44,
the stale registration survived, and the boot reconciler read it, found the venue flat for LONG, and
booked a second close — *"closed while the bot was down"* for a position that closed three hours
before the bot went down.

**This is not caused by the book gate** — the gate touches neither `_active_positions` nor the
reconciler — but **I triggered it by restarting, so it is mine to report.** It is the *same class*
`main.py:5395` already documents and fixed for the armed-exit path (*"ONE CLOSE, ONE ROW"*, which
leaves `pnl` NULL precisely to keep the duplicate out of every reader). **The AP reconcile path was
missed by that fix.**

**Blast radius, measured rather than guessed:**

| consumer | affected? | why |
|---|---|---|
| `virtual_positions` (the authoritative ledger) | **NO** | vpos 31 has one row, `net_pnl −1.45543199999999`, unchanged |
| `optimizer.pair_trades` | **NO** | it pops the open on the FIRST close row (17296, lower id); 17340 finds no open and is dropped — the mechanism `main.py:5395` describes |
| the venue | **NO** | no order was placed; the stop's `updatedTime` is unchanged |
| any `SUM(trades.pnl)` reader | **YES** | −$1.4554 would be counted twice |
| the 30-trade reminder | **NO** | it counts `virtual_positions`, not `trades` |

**NOT FIXED, and deliberately.** The approved scope was arming the gate; a DB write is a separate
decision and there is a standing rule against unrequested row deletion. **The proposal, for your
call:** set row 17340 to `pnl = NULL, status = 'closed_unrecorded_pnl'` — which is the state
`main.py:399` already writes on the reconciler's own can't-substantiate branch, so it needs no new
vocabulary — and make the engine's close path clear its `active_positions` row so the next restart
cannot repeat it. **Neither is applied.**

---

## PROOF BY EXECUTION — 49 ✅ / 0 ❌, SEARCHED BY DIRECTORY, RUN BEFORE APPLYING

```
LAB: full tree copy + the design; every PRODUCTION-DIRECTORY literal rewritten.
  20 VECTORS by DIRECTORY grep      residual prod-path literals: 0
LOCK before the first import: sqlite3.connect + open(w/x/a/+) raise on PROD or /root/titan-bot
🔴 and a hard assertion before copying: no LAB/scratchpad literal survives in any applied file
```

```
── ARMED PATH (21 assertions that only mean anything with DRYRUN False) ──
✅ 🔴 BOOK_GATE_DRYRUN = False — THE GATE IS ARMED
✅ ⚰️ WALL_AVOIDANCE_ENABLED still False; marked SUPERSEDED at its declaration
✅ 🔴 ORDER: fetch :4610 < gate :4644 < consult_for_entry :4718
✅ 🔴 SAME OBJECT: `_pre_walls` to both
✅ six columns registered; written at :4659 BEFORE the refuse branch at :4665
✅ 🔴 _record_skip_attribution(…,'book_blocked',…) ACTUALLY CALLED — 1 call site, inside not-DRYRUN
✅ ARMED: a big+close opposing wall produces a REAL refusal (clause A)
✅ 🔴 ARMED AND STILL FAILS OPEN: an unreadable book ADMITS

── THE RATE, from the REAL evaluate() over 3,454 production books ──
   LONG   n=1545  A 4 (0.26%)  B 29 (1.88%)  AB 1  REFUSE 2.20%
   SHORT  n=1909  A 14 (0.73%) B 35 (1.83%)  AB 2  REFUSE 2.67%
✅ both under the 5 % "rule not ban" ceiling      ✅ 🔴 SIDE SYMMETRY 1.21×
✅ the shape guard refused ZERO non-OKX books on real data
✅ FAIL-OPEN on None / empty dict / a string / mid=0
✅ 🔴 /root/titan-bot git-CLEAN at 897850b — NOT TOUCHED
```

---

## STATE

```
mercury-sol   active · master 319767 / worker 319915 · since 2026-08-10 18:25:01 · NRestarts=0
              RESTARTED DELIBERATELY at 18:24:58; boot clean; 0 tracebacks
🔴 BOOK GATE  ARMED — BOOK_GATE_ENABLED=True, BOOK_GATE_DRYRUN=False
              loaded (module-level import + clean boot); NOT yet exercised by a live signal
🔴 vpos 32    OPEN · SHORT 1.3 @ 76.18 · SL 77.32 · is_paper 0 · UNTOUCHED
              39/39 fields identical across the restart; venue stop updatedTime unchanged
              exit_pending SHORT (armed 18:00:15, expires 00:00:15) SURVIVED intact
🔶 row 17340  PHANTOM duplicate close for vpos 31 — §8. Reported, NOT fixed.
backups       *.bak_bookgate_20260810_1900 (4 files), md5-verified BEFORE the first edit
db            read-only for every query except the bot's own writes; busy_timeout 8000
titan         HEAD 897850b · git clean · NOT TOUCHED
```

**The book now takes part in the entry decision. It refuses on its own numbers, before the model
gets a vote, and it will say so out loud the first time it fires.**
