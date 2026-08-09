# sol-exit-advisor-live-in-dryrun-first-verdict-reads-its-prompt

_2026-08-09 19:00 UTC_

---

# APPLIED and RESTARTED. **The first exit verdict in Mercury-SOL's history: HOLD, 0.72, and 6 of 6 checkable claims TRUE.** The entry advisor's first four were 4 of 4 false.

**Position survived intact: 38 of 39 fields identical, the single change being the throttle stamp
the port is supposed to write.** The venue's protective stop was never written to — same orderId,
same `updatedTime`.

```
🔴 THE FIRST CONSULT, 4 SECONDS AFTER THE POLLER STARTED:

[EXIT-ADVISOR-DRYRUN] trigger=hourly SOL/USDT:USDT LONG close=False conf=0.72
  upnl=+0.94R giveback=0.43R took=1.55s
  | Position +0.94R with breakeven lock, trailing stop armed at 0.38% below current
    price. Peak +1.37R shows strength; 0.43R giveback acceptable. Hold for further
    upside, stops protect downside.
```

**Every number in that sentence is in its prompt, and every one is right.** 6 of 6.

**And the residual I named at 18:45 is now a measurement, not a caveat: `took=1.55s`**, and the tick
it ran on was **17 s against a 12–14 s neighbour baseline**.

```
PROOF BY EXECUTION (pre-apply): 37 assertions, 0 failed. LEAKS: 0. 18 vectors by DIRECTORY.
APPLIED: config.py +26−0 · claude_advisor.py +70−0 · main.py +140−0 · virtual_trader.py +36−0
🔴 ZERO DELETED LINES. Only ONE existing function changed: _process_position.
RESTART: 18:42:10 → 18:42:12.  Four boot gates clean.  0 tracebacks.
```

Prior: [18:45 — the approved diff](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1845-sol-hourly-exit-advisor-dryrun-diff-awaiting-approval.md)

---

## 0. ONE ADDITION BEYOND THE APPROVED DIFF, DECLARED

§(j) asked for the call duration to be logged on **every** consult. That was not in the diff you
approved, so it is an addition and I am naming it rather than folding it in quietly:

```python
        _t0 = time.monotonic()
        advice = claude_advisor.consult_for_close_state(ctx)
        _took = time.monotonic() - _t0
```

`monotonic()`, not wall clock — it cannot go backwards on an NTP step, and the figure is a duration,
never a timestamp. It adds `took=1.55s` to the log line. **main.py is +140 rather than +132 because
of it**, and the full 37-assertion proof was re-run on the amended source before applying.

---

## BEFORE

### (a) The snapshot, at 18:40:48

```
vpos 30  size 0.9 · entry 76.29 · sl_price 76.44258 · original_sl 75.41 · trail_pct 0.865
         water_mark 77.5 · max_adverse 75.73 · initial_risk 1.1440000000000126
         partial 0.4 @ 77.25 (pnl 0.322584, fees 0.061416, at 15:40:16)
         status open · is_paper 0 · recheck done · funding_paid/source NULL
         mgmt_state_json  {"breakeven_applied": true, "partial_done": true}
         fills_json       entry 0.9 @ 76.29 fee 0.068661
                          partial 0.4 @ 77.25 price_source=venue_fill fee_rate=0.001 [venue]

venue    LONG 0.9 @ 76.29 · stopLoss 76.44 · mark 77.10 · uPnL +0.729 · tradeMode 0 (cross)
         order 46968bbe-3bef-4ae6-a52d-6a0b11882f9d  Untriggered
               qty 0.9 · trigger 76.44 · created 1786223419195 · updated 1786290015787
```

Written to `before2_vpos30.json` for machine comparison, not held in memory.

### (b) Nothing was mid-flight

```
exit_pending           EMPTY          -> no armed exit about to fire
open rows              exactly ONE (vpos 30)
partial                partial_at set, partial_done=true -> settled at 15:40, not pending
entry / close in flight  none — last trades row 17081 @ 18:20 is context_recorded
journal                only the known STOP-VERIFY→34040 resync loop and the heartbeat
```

---

## AFTER — the same checks that made 17:42 trustworthy

### (c) 🔴 THE POSITION SURVIVED — 38 of 39 fields identical

```
identical fields : 38
CHANGED          : 1   ->  mgmt_state_json
  BEFORE  {"breakeven_applied": true, "partial_done": true}
  AFTER   {"breakeven_applied": true, "partial_done": true,
           "exit_advisor_last_ts": 1786300951.587846}
```

**That single change is the throttle stamp the port exists to write.** The three you named:

| | |
|---|---|
| **`water_mark`** | **77.5 — unchanged. The trail did NOT re-arm from scratch.** |
| **`mgmt_state_json`** | `breakeven_applied: true` **kept**, `partial_done: true` **kept** |
| **`fills_json`** | **byte-identical**, including `price_source: venue_fill` and `fee_rate_source: venue` |

**And the 17 protected fields — size, sl_price, water_mark, status, close_price, close_reason,
net_pnl, initial_fill_price, original_sl_price, trail_pct, the four partial columns,
max_adverse_price, is_paper, fills_json — CHANGED: NONE.**

### (d) The venue's conditional order was NOT touched

| | BEFORE (18:40) | AFTER (18:47) | |
|---|---|---|---|
| orderId | `46968bbe-3bef-4ae6-a52d-6a0b11882f9d` | identical | ✅ |
| qty / trigger / status | 0.9 / 76.44 / Untriggered | identical | ✅ |
| createdTime | 1786223419195 | identical | ✅ |
| **updatedTime** | **1786290015787** | **1786290015787** | ✅ **unchanged** |
| position size / avg / sl | 0.9 / 76.29 / 76.44 | identical | ✅ |

**`updatedTime` still points at the 15:40 partial.** Neither the restart nor the consult wrote to
the protective stop.

### (e) Boot read CONSISTENT, not ORPHAN

```
18:42:12  [SMART-CLEANUP] Skipping stop cancel — position still open on exchange   ✅
18:42:2x  [AP] Restored LONG SOL/USDT:USDT from DB (entry=2026-08-08T21:10:22)      ✅
18:42:2x  [BOOT] taker fee: 0.001 (0.1000%) source=venue
18:42:2x  [BOOT-ASSERT] LONG open on venue and booked in the DB — consistent        ✅
18:42:29  live adapter registered (close/partial/move_stop/pos_state/book_close/funding=yes)
18:42:29  [VPOS-RECONCILE] OPEN vpos=30 LONG entry=76.29 sl=76.44258 age=21.5h
                           — poller continues managing it (no auto-close)           ✅
```

**Downtime: 2 seconds of process (18:42:10 → 18:42:12), 19 seconds to a managing poller.**

### (f) Geometry and the three new flags, at runtime

```
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R)
                    ATR_TF=1h OBSERVATION_MODE=False [pid 4059524]

EXIT_ADVISOR_DRYRUN          = True     🔴 OBSERVE ONLY
EXIT_ADVISOR_HOURLY          = True
EXIT_ADVISOR_HOURLY_SEC      = 3600
SMART_EXIT_DRYRUN_SAMPLE_SEC = 3600     (same period — the shared hook)
```

All four source files are stamped **18:41:54**, before the worker's **18:42:29** start, so what is on
disk is what is loaded.

---

## (g) 🔴 THE FIRST EXIT VERDICT MERCURY-SOL HAS EVER PRODUCED

`trades` row **17082**, `2026-08-09 18:42:33`, `tv_action='hourly review'`, `tv_tf='hourly'`,
model `claude-haiku-4-5-20251001`.

**The user prompt, exactly as sent:**

```
OPEN POSITION — decide CLOSE or HOLD.

Position
  Side: LONG   Entry: 76.29   Now: 77.12
  Unrealised: +0.94R   (1R = the ORIGINAL stop distance, 0.8800)
  Elapsed: 21.5h
  Current stop: 76.44258  ->  +0.77R away   (breakeven lock APPLIED)
  Peak so far (MFE): +1.37R   Giveback from peak: 0.43R

Trail
  The trailing stop is ARMED (this position reached +1R).
  It exits at 76.8296 = the high-water mark 77.5 less 0.865% of it.
  That is 0.38% below the price now.

Partial
  0.4 already realised at 77.25; 0.9 remains open.

EVERY figure above is computed from this position's own ledger row; `Now` is the last traded
price this poll tick.
Consultation trigger: hourly review (no signal fired).

Decide whether to close the remaining size now or hold it.
```

**The raw response:**

```json
{
  "close": false,
  "confidence": 0.72,
  "reason": "Position +0.94R with breakeven lock, trailing stop armed at 0.38% below current price. Peak +1.37R shows strength; 0.43R giveback acceptable. Hold for further upside, stops protect downside."
}
```

**Verdict: HOLD. Confidence 0.72.**

---

## (h) 🔴 ITS CLAIMS, CHECKED THE WAY TITAN'S 211 WERE — 6 OF 6 TRUE

| # | claim in the reason | what the prompt says | |
|---|---|---|---|
| 1 | "Position **+0.94R**" | `Unrealised: +0.94R` | ✅ |
| 2 | "with **breakeven lock**" | `(breakeven lock APPLIED)` | ✅ |
| 3 | "**trailing stop armed**" | `The trailing stop is ARMED` | ✅ |
| 4 | "at **0.38% below current price**" | `That is 0.38% below the price now.` | ✅ |
| 5 | "Peak **+1.37R**" | `Peak so far (MFE): +1.37R` | ✅ |
| 6 | "**0.43R giveback**" | `Giveback from peak: 0.43R` | ✅ |

**Checkable claims: 6. False: 0.**

🔴 **The contrast is the entire point of this port.** The ENTRY advisor's first four checkable book
claims were **4 of 4 FALSE** — every one asserting "no opposing walls above entry" while ask walls
sat in its own prompt. The EXIT advisor's first six are **6 of 6 TRUE**, on the same model, on the
same day. Titan's exit advisor runs at 98.6% true across 211 claims; SOL's opens at 6/6.

**What this is NOT evidence of.** It is one verdict. It does not show the advisor is right to hold,
that it would beat the trail, or that its verdicts correlate with anything — those need the ~120
verdicts that two weeks of position-time will produce. **It shows the mechanism reads its input,
which is precisely the question that could not be asked before today because the prompt had never
been rendered.**

🔶 **One observation, offered as an observation and not a finding:** the reason paraphrases the
prompt closely — it restates six figures and adds a judgement ("shows strength", "acceptable"). That
is what a well-fed prompt should produce, and it is also what a model that is merely echoing would
produce. **Distinguishing the two needs the correlation test on n≈120, not a reading of one
sentence.** I am not going to claim more from this than it can carry.

---

## (i) The position after the consult — untouched

```
17 protected fields changed : NONE
mgmt_state added            : ['exit_advisor_last_ts']   removed: []
breakeven_applied           : True   (kept)
partial_done                : True   (kept)
water_mark                  : 77.5   (kept)
```

**A verdict was produced, recorded, and discarded.** The trail still owns the position.

---

## (j) 🔴 THE LATENCY, MEASURED

```
took = 1.55s        (the LLM call itself, monotonic)
```

**The tick it ran on, against its neighbours:**

```
18:42:29  poller started
18:42:30  STOP-VERIFY tick
18:42:33  [EXIT-ADVISOR-DRYRUN] ... took=1.55s        <- the consult tick
18:42:47  STOP-VERIFY tick        gap 17s   <- the consult tick
18:43:00  STOP-VERIFY tick        gap 13s
18:43:13  STOP-VERIFY tick        gap 13s
18:43:26  STOP-VERIFY tick        gap 13s
18:43:40  STOP-VERIFY tick        gap 14s
18:43:52  STOP-VERIFY tick        gap 12s
18:44:05  STOP-VERIFY tick        gap 13s
18:44:18  STOP-VERIFY tick        gap 13s
```

**The consult tick took 17 s against a 12–14 s baseline — roughly +3 to +4 s**, of which 1.55 s is
the model call and the rest is the one-off cost of the lazy `import main` plus the mgmt_state write.
**Subsequent consults should cost closer to the 1.55 s alone**, since the import is cached after the
first.

**So the residual is real, small, and bounded: once an hour, one tick runs ~25–30% long.** The stop
is resting on the venue and is independent of the process throughout, so a late tick delays the
*trail's* re-evaluation, never the *stop's* protection. Now it is a number that can be watched
rather than a caveat that has to be believed.

---

## PROOF BY EXECUTION — 18 VECTORS, SEARCHED BY DIRECTORY (pre-apply)

```
LAB: full tree copy from the PORTED source, every prod-directory literal rewritten.
  residual prod-directory literals : 0      residual /root/titan-bot literals : 0
  files rewritten : 17   + .env  => 18 VECTORS
LOCK: sqlite3.connect and open(w/x/a/+) raise on any path under PROD or /root/titan-bot;
      sys.dont_write_bytecode = True; the Telegram sender is a stub that RAISES if called.
RESULT: 37 assertions ✅  0 ❌  LEAKS: 0  exit 0   (re-run after the timing addition)

AST vs the pre-apply production files:
  config.py          added=[] removed=[] changed=[]
  claude_advisor.py  added=['consult_for_close_state'] removed=[] changed=[]
  main.py            added=['_build_exit_ctx_from_ledger','consult_exit_advisor']
                     removed=[] changed=[]
  virtual_trader.py  added=[] removed=[] changed=['_process_position']
```

**Zero deleted lines in all four files.** `consult_for_close` (the legacy 6-field prompt), the 5m
Group-B path, the trail, the breakeven lock, the partial, the stop and every geometry constant are
byte-identical. Backups `*.bak_exitadvisor_hourly_20260809_1845`, md5-verified against the live
files before the first edit.

🔶 **A small process note against myself:** my first apply command chained on `grep "^<"`, which
exits non-zero when it finds nothing — so the "no deleted lines" check *succeeded* and the chain
stopped before copying anything. It failed safe, I noticed, and I reran it unchained. Recording it
because a shell idiom that stops on success is worth not repeating.

---

## THE BOUNDARY IS NOW OPEN

```
🔴 THE FIRST SOL EXIT-ADVISOR CONSULT: trades row 17082, 2026-08-09 18:42:33 UTC.

BEFORE it: zero consults, ever. All 23 closed positions were decided by the trail, the exit
           signal or the stop with NO advisory verdict in existence for them.
AFTER  it: every open position carries hourly verdicts recorded beside the mechanism that acts.

NOTHING BEFORE ROW 17082 MAY BE POOLED WITH ANYTHING AFTER IT in any study of exit behaviour.
The bot's behaviour has not changed — in DRYRUN it cannot — but the POPULATION has: before, a
"held" position was unobserved; after, it is observed and held anyway.

Fourth boundary in SOL's book, and they must not be conflated with one another:
   taker fee      vpos <=29 / >=30
   ADX window     vpos <=28 / >=29
   funding        every closed row NULL; first booked at the next close
   exit advisor   trades row 17082 onward   <- THIS ONE
```

---

## STATE

```
mercury-sol   active · master 4059454 / worker 4059524 · since 2026-08-09 18:42:12 · NRestarts=0
vpos 30       OPEN · 0.9 @ 76.29 · sl 76.44258 · wm 77.50 · is_paper=0
              38/39 fields identical to the pre-restart snapshot; the one change is the
              throttle stamp. 17 protected fields untouched.
venue         LONG 0.9 · stop 76.44 · order 46968bbe · updatedTime UNCHANGED · SHORT flat
advisor       DRYRUN · HOURLY · 3600s · 1 verdict recorded (HOLD 0.72) · 1.55s
tracebacks    0 since the restart
titan         active · pid 2538048 · NRestarts=0 · HEAD 897850b · git clean · NOT TOUCHED
```

**The next consult is due at ~19:42 UTC.** From here the useful number is not any single verdict but
the correlation across ~120 of them — whether SOL's exit advisor tracks giveback and unrealised R
the way Titan's does (ρ=+0.523 and −0.448), or whether it narrates. **That question is now
answerable, and it was not this morning.**
