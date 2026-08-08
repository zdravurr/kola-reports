# sol-be-target-separated-assert-fixed-zero-behaviour

_2026-08-08 17:00 UTC_

---

# Mercury-SOL — three zero-behaviour fixes APPLIED. The value stayed at 0.0015. Every traded number is identical.

**`MIN_PROFIT_DISTANCE_PCT` re-documented at its declaration (name kept — see §1).
`_BE_TARGET_FRAC_ON` cut loose from the fee arithmetic and pinned explicitly at today's 0.0020.
The import assert now tests the arm the bot actually uses, at a measured ATR floor.**

**Proven by execution: `breakeven_target(74.80)` = 74.9496, `activation_distance` = 0.9100,
`compute_initial_sl` = 73.89 route=fallback_atr, the import assert passes — and it STILL FAILS on a
value that breaks the real invariant. vpos 29 untouched. Titan untouched.**

🔴 **I did not restart, deliberately.** Reasoning in the deployment section — it is a choice, not an
oversight.

Prior: [the measurement 17:06](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1706-sol-min-profit-distance-is-exit-geometry-not-a-viability-gate.md)

---

## 1. RENAME? — NO. I KEPT THE NAME AND DOCUMENTED IT. (your call, stated)

```
MIN_PROFIT_DISTANCE_PCT references: 25, across 6 files
  config.py 7 · main.py 5 · trail_arm.py 5 · stop_loss.py 4 · fee_rates.py 2 · virtual_trader.py 2
```

A rename touches all 25 and turns a naming fix into a six-file diff. Per your instruction I **kept
the symbol and put the truth at the declaration** instead, naming `BE_TARGET_BASE_FRAC` as what it
should have been called so a future reader finds the intent without a churn commit.

**What the declaration now says** — the four things you asked for:

- **it refuses nothing** and is not a viability gate; its one live effect is the breakeven target;
- **three of four consumers are unreachable**, each named with its flag and the line it dies at:
  `_select_stop_wall` (:40/:44) and the SL floor (:80) behind `SL_WALL_ANCHOR_ENABLED=False` via
  the early return on line 68; the EQH/EQL gate (`main.py:3903`) behind `FEE_GATE_ENABLED=False`;
- **the fee derivation is historical** — real taker rate 0.001, read from the venue by `fee_rates`;
- **why the value stays**: 8.7 cents per BE exit, −0.133R on vpos 21, with the report path.

And the block header, which described a filter that does not run:

```
- # ── Spread / commission gate ──────────────────────────────────────────────────
+ # ── Spread / commission gate — 🔴 DISABLED; THIS HEADER DESCRIBES NOTHING LIVE ─
+ # 2026-08-08: the gate below is OFF and has been since 2026-06-08, so the
+ # "hard pre-entry filter" this block describes DOES NOT RUN. Measured that day:
+ # nothing anywhere in the bot refuses an entry on move size. There is no viability
+ # gate — not a broken one, none.
```

---

## 2. THE BE TARGET IS NOW ITS OWN CONSTANT — VALUE UNCHANGED

```diff
- # Breakeven-lock target as a fraction of entry when the fix is ON (+0.20%).
- _BE_TARGET_FRAC_ON = MIN_PROFIT_DISTANCE_PCT + BREAKEVEN_LOCK_MARGIN_PCT
+ # It used to read `MIN_PROFIT_DISTANCE_PCT + BREAKEVEN_LOCK_MARGIN_PCT`. That made
+ # a LIVE STOP PRICE a function of the configured fee rate, so correcting the fee
+ # constant would have silently moved the breakeven stop on every open position.
+ # ... THE VALUE IS UNCHANGED at 0.0020 — this was a separation, not a re-tune.
+ _BE_TARGET_FRAC_ON = 0.0020
```

Recorded beside it, exactly as you asked:

- at the real 0.100% taker rate, 0.0020 yields **gross +0.2000% − fees 0.2002% = NET −0.0002%** —
  a fee wash, not the "small net WIN" the docstring promised against an assumed 0.055%;
- **0.0029 would restore the win** (+0.0897% net) **and is not free**: it tightens the lock in both
  directions, and on vpos 21 — the only measurable case in 22 closed positions — it would have
  breakeven-stopped at 76.2705 instead of trailing out at 76.39, **+0.152R instead of +0.285R,
  i.e. −0.133R**;
- **choosing it is a geometry decision needing its own evidence and approval.**

The stale docstring claim was corrected in the same edit rather than left contradicting the constant
two lines above it.

**Separation proved arithmetically, not asserted:**

```
MIN_PROFIT_DISTANCE_PCT + BREAKEVEN_LOCK_MARGIN_PCT = 0.002
_BE_TARGET_FRAC_ON (now explicit)                   = 0.002
identical: True   -> separation, not a re-tune
```

---

## 3. THE ASSERT NOW TESTS THE REAL ARM

```diff
- if TRAIL_ARM_FIX_ENABLED:
-     assert TRAIL_MIN_ACTIVATION_PCT > _BE_TARGET_FRAC_ON, (...)
+ ASSERT_MIN_ATR_PCT = 0.0035      # 0.35% — under min 0.3630% and p1 0.3873%
+
+ if TRAIL_ARM_FIX_ENABLED:
+     _MIN_ARM_FRAC = SL_BUFFER_ATR * ASSERT_MIN_ATR_PCT
+     assert _MIN_ARM_FRAC > _BE_TARGET_FRAC_ON, (...)
```

**The floor is measured, not guessed — and I used the scale-free form.** Absolute ATR is not
comparable across price levels, so the invariant is evaluated on **ATR(1h)/price**:

```
ATR(1h)/mid over 3,369 rendered books (2026-06-08 → 2026-08-08):
  min 0.3630%   p1 0.3873%   median 0.7336%   max 1.8431%
the invariant fails below 0.0800%; rows ever observed below it: 0
```

(Your absolute figure — p1 of ATR = 0.2896 — is the same population; at a ~72.5 mid it is ~0.40%,
consistent with the p1 above.)

**I set the floor at 0.0035, BELOW both the observed minimum and p1, on purpose:** a lower assumed
ATR means a smaller assumed arm, which makes the guard **stricter**. A safety invariant should err
strict.

**The margin the assert now guarantees:**

```
assumed arm at the floor = 2.5 × 0.0035 = 0.875% of entry
BE target                = 0.20%
GUARANTEED MARGIN        = 4.38x
  real margin at the observed MIN (0.3630%) = 4.54x
  real margin at p1        (0.3873%)        = 4.84x
  real margin at median    (0.7336%)        = 9.17x
```

**Superseded constants marked, not deleted**, with A6 named as what replaced them — at their
`config.py` declarations and again at the `trail_arm` imports, which now say plainly that they are
imported for the record and read by no live expression:

```
# 🔴 SUPERSEDED BY A6 (2026-06-08) — the next two constants NO LONGER SET THE ARM.
# ... They are KEPT, not deleted: TRAIL_MIN_ACTIVATION_PCT was the quantity the
# import-time invariant used to test, and that mismatch is how the whole
# MIN_PROFIT_DISTANCE_PCT problem became findable on 2026-08-08.
TRAIL_ACTIVATION_ATR_FIXED = 5.0     # SUPERSEDED by A6.
TRAIL_MIN_ACTIVATION_PCT   = 0.0025  # SUPERSEDED by A6.
```

---

## 4. PROOF BY EXECUTION

### (a) Zero behaviour — every traded value identical

```
PASS  breakeven_target(74.80, LONG)      = 74.9496   (expected 74.9496)
PASS  breakeven_target(74.80, SHORT)     = 74.6504
PASS  activation_distance(74.80, 0.364)  = 0.91      (expected 0.9100)
PASS  compute_initial_sl LONG            = (73.89, 'fallback_atr')
PASS  compute_initial_sl SHORT           = (75.71, 'fallback_atr')
PASS  MIN_PROFIT_DISTANCE_PCT            = 0.0015
PASS  BYBIT_TAKER_FEE_RATE               = 0.00055
PASS  BREAKEVEN_LOCK_MARGIN_PCT          = 0.0005
PASS  TRAIL_MIN_ACTIVATION_PCT           = 0.0025
PASS  TRAIL_ACTIVATION_ATR_FIXED         = 5.0
PASS  _BE_TARGET_FRAC_ON                 = 0.0020
PASS  import assert passed
```

Re-run against the **installed production modules** after the copy, not just in the lab — same
results.

**AST comparison against the backups:** `config.py` and `trail_arm.py` — **zero** functions added,
removed or changed. `virtual_trader.py` — one changed, `_adopt_card`, which is the display string.
Everything else in the diff is module-level comments and the two rewritten definitions.

### (b) 🔴 The guard can still fail — a guard that cannot fail is not a guard

Re-imported `trail_arm` in a separate interpreter with the BE target replaced:

```
PASS  BE target 0.0100 (5x the arm at the ATR floor) -> RAISED
PASS  BE target 0.00875 (exactly equal to the arm)   -> RAISED   (strict >, boundary correct)
PASS  BE target 0.0086 (a hair under the arm)        -> passes
PASS  BE target 0.0029 (the honest-fee value)        -> passes
PASS  BE target 0.0020 (shipped)                     -> passes
```

The raised message names the real quantities:

```
trail_arm invariant violated: at the measured ATR floor (0.3500% of price) the REAL
arm is SL_BUFFER_ATR×atr = 0.8750% of entry, which must be > the breakeven target …
```

### (c) The old guard would have misfired where the new one does not

```
BE target 0.0020 : OLD -> PASS                      NEW -> PASS
BE target 0.0025 : OLD -> FAIL (bot would not boot) NEW -> PASS
BE target 0.0029 : OLD -> FAIL (bot would not boot) NEW -> PASS
```

**The 0.0029 row is the whole point.** The old guard refused a value the real arm clears with 3.0×
margin at the worst ATR ever recorded. A future BE-target decision is now judged on the real
invariant instead of a superseded constant — which is what made this defect findable in the first
place.

### Isolation

17 vectors, searched by **directory** (13 by DB filename; the three the filename grep misses are
`healthcheck.py`, `mercury_sol_prior_move_logger.py` and `weight_engine.py`, which holds
`WEIGHTS_PATH`), all rewritten, **0 prod-path literals remaining**, `sys.dont_write_bytecode=True`,
lock on `sqlite3.connect` and write-mode `open()` against **both** the prod directory and
`/root/titan-bot`. **Leaks: 0.**

### Diffstat

```
config.py          +51   -8
trail_arm.py       +75  -25
virtual_trader.py   +8   -2
```

All 35 removed lines accounted for: 26 comment/docstring lines replaced by accurate ones, 6 import
lines re-annotated, the derived `_BE_TARGET_FRAC_ON` line, the old assert body, and the adoption
card's formula string.

---

## DEPLOYMENT — 🔴 APPLIED, NOT RESTARTED, AND WHY

Backups `*.bak_beseparation_20260808_165135`, md5-verified against the live files before the write.
Files installed 16:51:55.

**I did not restart, and that is a deliberate choice:**

1. **The change is provably zero-behaviour.** Every traded value is byte-identical, verified against
   the installed modules. A restarted process would compute exactly the same numbers as the running
   one.
2. **The new assert protects the NEXT boot either way.** It is an import-time guard; not restarting
   now removes none of its protection, because it runs whenever the process next starts.
3. **vpos 29 is open, managed and live.** A restart is a non-zero-risk operation on real money, and
   here it buys nothing functional.

**The one difference between disk and memory, named so it is not a surprise:** if an orphan
adoption were to happen before the next restart, the running process would print the OLD formula
string on its card (`fill*(1+0.0015+0.0005)`) while computing the same 0.0020 target. Display only,
on a path that requires a brand-new orphan. Everything else is identical.

This is the one place I have deviated from the standing "disk ≠ memory" discipline, and I am naming
it rather than letting it pass silently. Say the word and I will restart at a moment you choose.

## STATE

```
mercury-sol   active   pid 3533821 / worker 3533987   since 16:08:59   NRestarts=0   0 tracebacks
              NOT restarted this pass — see above
vpos 29       size 0.9 · sl 74.9496 · open · trail_pct 0.909 · partial 0.4 @ 76.36 · wm 76.46
              IDENTICAL to before this pass
venue         LONG 0.9 @ 74.80 · stop 74.95 · untouched
titan         active · HEAD 897850b · git clean · master pid 2538048 · NOT TOUCHED
```

**Open, unchanged, and still yours to decide:** whether `_BE_TARGET_FRAC_ON` should become 0.0029.
It is now a single explicit constant with its evidence written beside it, and the assert will no
longer refuse it on a false premise.
