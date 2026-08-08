# sol-min-profit-distance-is-exit-geometry-not-a-viability-gate

_2026-08-08 17:06 UTC_

---

# Mercury-SOL — `MIN_PROFIT_DISTANCE_PCT` refuses NOTHING. The framing is wrong, the defect is real but tiny, and I recommend NOT changing the number.

**Settled either way, as you asked: the bot does NOT enter unviable trades on this constant.
Nothing anywhere refuses an entry on it. Its only live consumer is the breakeven-lock target.
It is exit geometry wearing a viability name.**

**The real defect, with the number: at the true fee rate the breakeven lock books a
FEE WASH (−0.0002% of notional) where its own docstring promises "a small net WIN".
That is −$0.0002 per BE exit at live size. Correcting it would have cost −0.133R on the one
position in 22 where it measurably changes anything.**

🔴 **Recommendation: do NOT raise the constant. Fix the name, the separation, and the assert —
all of which are zero-behaviour changes.** No diff applied; nothing was written.

Prior: [§1 of the 16:12 report](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1612-sol-taker-fee-read-from-venue-and-partial-price-from-fill.md)

---

## 1. EVERY CONSUMER, AND WHETHER IT IS EVEN REACHABLE

`MIN_PROFIT_DISTANCE_PCT = 2 × (BYBIT_TAKER_FEE_RATE + SLIPPAGE_BUFFER_PCT)` = **0.0015** today,
**0.0024** at the honest 0.001 taker rate.

| # | consumer | what it computes | reachable? |
|---|---|---|---|
| a | `trail_arm._BE_TARGET_FRAC_ON` | the breakeven-lock target price | ✅ **LIVE — the only one** |
| b1 | `stop_loss._select_stop_wall` (:40/:44) | break-even filter on candidate stop walls | ❌ **DEAD** |
| b2 | `stop_loss` SL fallback floor (:80) | `max(3.0×atr, MPD×entry)` | ❌ **DEAD** |
| c | EQH/EQL distance gate (`main.py:3903`) | refuses an entry whose pool is nearer than the fee floor | ❌ **DEAD** |
| d | `trail_arm` import-time assert (:38) | invariant guard | ✅ runs at import |

### (a) The breakeven target — the ONLY live consumer

```
_BE_TARGET_FRAC_ON = MIN_PROFIT_DISTANCE_PCT + BREAKEVEN_LOCK_MARGIN_PCT
                   = 0.0015 + 0.0005 = 0.0020    ->  honest: 0.0024 + 0.0005 = 0.0029
```

**On vpos 29's entry of 74.80:** `74.9496` today → **`75.0169`** at 0.0024. A move of **+0.0673**,
which is 0.09% of entry. (vpos 29's stop is currently sitting at the 74.9496 figure on the venue —
untouched by this pass.)

### (b) Both `stop_loss` consumers are unreachable

`compute_initial_sl` returns on line 68:

```python
if not SL_WALL_ANCHOR_ENABLED:
    return round_price(entry + sign * SL_BUFFER_ATR * atr), 'fallback_atr'
```

`SL_WALL_ANCHOR_ENABLED = False`, so execution never reaches `_select_stop_wall` (which uses
`MIN_PROFIT_DISTANCE_PCT` at :40/:44) **or** the fallback floor at :80. Both are dead code with
respect to this constant. Confirmed by execution earlier today: `compute_initial_sl('LONG', 74.80,
0.364, None)` → `73.89, route=fallback_atr`, the line-68 branch.

### (c) The EQH/EQL gate — the ONLY entry-facing consumer — is dead

```python
# main.py:3903
if FEE_GATE_ENABLED:
    target_sweep = 'EQH' if direction == 'LONG' else 'EQL'
    ...
    if 0 < dist_pct < MIN_PROFIT_DISTANCE_PCT:
```

```
config.py:732   FEE_GATE_ENABLED = False   # A3 2026-06-08: Titan parity — Titan has no fee gate.
```

**The whole block is behind a False flag.** This is the answer to your §2b and it is unambiguous.

### (d) 🔴 THE ASSERT — it encodes a real invariant, but tests the WRONG QUANTITY

```python
assert TRAIL_MIN_ACTIVATION_PCT > _BE_TARGET_FRAC_ON
```

**It breaks at `MIN_PROFIT_DISTANCE_PCT >= 0.0020`:**

```
0.0015 -> BE frac 0.0020 -> PASSES
0.0019 -> BE frac 0.0024 -> PASSES
0.0020 -> BE frac 0.0025 -> FAILS  -> ImportError, the bot does not boot
0.0024 -> BE frac 0.0029 -> FAILS
```

So the honest value is **4 basis points past the cliff**, not near it.

**Why the assert exists** — and it is a genuine invariant, quoted from its own message: *"the
arm-distance FLOOR must sit strictly ABOVE the breakeven-lock target, so that when the lock arms
(price ≥ entry+floor) the BE stop (entry+target) lands BELOW the live price and cannot
instant-trigger."* Violate it and you re-create the instant stop-out giveback bug. Real.

**But the arm it names is no longer the arm.** `TRAIL_MIN_ACTIVATION_PCT` appears in exactly one
place in the executable tree — **inside the assert itself**. A6 replaced the flag-ON arm with:

```python
return SL_BUFFER_ATR * atr        # trail_arm.activation_distance
```

So the assert guards a **superseded constant**. The invariant that actually matters is
`SL_BUFFER_ATR × ATR(1h) > BE target × entry`:

```
vpos 29: real arm = 2.5 × 0.364 = 0.9100 = 1.217% of entry
         BE target 0.20% today / 0.29% honest
         real margin at the HONEST value: 4.2x

the real invariant fails only if ATR(1h)/entry < 0.1160%, i.e. ATR < 0.0868 on SOL at 74.80
observed ATR(1h) across 3,372 rows: min 0.2639 · p1 0.2896 · median 0.5587 · max 1.3235
=> 3.0x margin at the WORST ATR ever recorded on this book
```

**So your instinct in the brief is half-right and half-wrong, and the distinction matters:** the
assert does encode a real invariant, so it cannot simply be deleted — but the honest fee rate does
**NOT** require moving `TRAIL_MIN_ACTIVATION_PCT`, because that constant no longer participates in
the arm. It requires the assert to test the quantity it claims to be testing. That is a
correctness fix to a guard, not a second geometry decision.

---

## 2. WHAT WOULD HAVE CHANGED ON THE BOOK

### (a) The breakeven target — all 22 move, 7 arm, ONE outcome changes

Every closed position's BE target shifts by **0.058–0.071 in price** (~0.09% of entry). But the BE
stop only exists after the lock arms:

```
positions closed              : 22
...where the BE lock FIRED    :  7   (vpos 7, 11, 13, 15, 17, 21, 25)
close_reason overall          : sl 11 · exit_signal 7 · trail 4
```

I replayed each of the 7 against 5-minute klines for its own lifetime, arming the BE stop only after
price first reached `entry ± 2.5×ATR`:

```
 vpos side   entry     arm   BE_now   BE_hon  BEnow hit    BEhon hit   actual close
    7 LONG  70.980  72.661  71.1220  71.1858      never        never   exit_signal@74.57
   11 SHORT 71.430  69.532  71.2871  71.2229      never        never   exit_signal@69.20
   13 SHORT 68.630  66.946  68.4927  68.4310      never        never   trail@66.31
   15 SHORT 78.560  76.613  78.4029  78.3322  07-09 01:05  07-09 01:05  trail@78.20
   17 SHORT 75.910  74.410  75.7582  75.6899  07-14 12:30  07-14 12:30  sl@75.82
   21 LONG  76.050  76.955  76.2021  76.2705      never    07-20 00:50  trail@76.39
   25 SHORT 72.470  71.740  72.3251  72.2598      never        never   trail@71.36
```

**Exactly ONE changes: vpos 21 — and it changes for the WORSE.**

```
vpos 21 LONG entry 76.05 size 131.4  1R = 118.26
  actual        : trailed out at 76.39   net +33.6592  = +0.285R
  at honest BE  : BE-stopped at 76.2705  net ~+17.96   = +0.152R
  COST of the honest value on this trade:            -0.133R
```

The honest value makes the BE lock **tighter in both directions** (the stop parks closer to entry in
profit terms, so a retrace hits it sooner). On this book that truncated one winner and helped
nobody. vpos 15 and 17 hit both levels **inside the same 5-minute bar**, so at this resolution the
difference is unresolvable — both are SHORTs where the lower level would fill marginally better, but
I will not claim a number I cannot see.

**Net measured effect across 22 positions: −0.133R.** In the wrong direction.

### (b) 🔴 DOES ANYTHING REFUSE AN ENTRY ON IT? — NO. SETTLED.

**No.** The EQH/EQL gate is the only entry-facing consumer and it is unreachable behind
`FEE_GATE_ENABLED = False`. `_risk_check` does not use it. The score gate does not use it. The
cascade does not use it. The advisor is not shown it.

**So the "bot enters unviable trades" framing is WRONG, and I am saying so plainly because you asked
me to settle it either way.** The bot has no viability gate on move size at all — not a broken one,
none. `MIN_PROFIT_DISTANCE_PCT` is an **exit-geometry number wearing a viability name**, and it has
been since `FEE_GATE_ENABLED` was set False for Titan parity on 2026-06-08.

### (c) N/A — no entries are gated, so nothing clears 0.15% and fails 0.24%.

---

## 3. 🔴 THE HONEST FRAME — WHICH PROBLEM IS IT?

**It is mostly a naming and separation problem, with one small, real, measurable money effect.
Both, but not in the proportions the framing implies.**

### The real money effect, with the number

`trail_arm.breakeven_target`'s docstring promises: *"above true round-trip break-even, so a clean
fill at the BE stop books a small net WIN instead of a fee wash."* At the real fee rate it does not:

| | BE target | gross | fees | **NET** |
|---|---|---|---|---|
| today 0.0015, fee **assumed** 0.055% | +0.20% | +0.2000% | 0.1101% | **+0.0899%** ← what the docstring describes |
| today 0.0015, fee **real** 0.100% | +0.20% | +0.2000% | 0.2002% | **−0.0002%** ← what actually happens |
| honest 0.0024, fee real 0.100% | +0.29% | +0.2900% | 0.2003% | **+0.0897%** |

Counting the slippage the constant claims to cover (0.02%/side): **today −0.0402%**, honest
**+0.0497%**.

**In money, per BE exit:**

```
LIVE   $97.24 notional : today -0.0002 USDT   honest +0.0872   difference +0.0874
PAPER  $9,994 notional : today -0.0200 USDT   honest +8.9656   difference +8.9856
```

**At live size the defect is worth 8.7 US cents per breakeven exit**, and only 7 of 22 positions
ever armed the lock. It is real, it is correctly described as "the breakeven lock does not break
even", and it is very small.

### The naming problem, which is the larger one

A constant named `MIN_PROFIT_DISTANCE_PCT`, derived from `2 × (fee + slippage)`, sitting in a block
headed *"Spread / commission gate"*, refuses nothing and gates nothing. Its entire live effect is to
set a breakeven-lock target. Three of its four consumers are dead code. That mismatch is what made
this question look like a money emergency when it is a sub-cent geometry detail — and it is exactly
the class this book already has a rule for: **a number must travel with its provenance, and its name
is part of its provenance.**

### 🔴 MY RECOMMENDATION: DO NOT CHANGE THE NUMBER

The evidence does not support raising it:

1. it refuses nothing, so no unviable entry is being admitted;
2. its only live effect is worth **8.7 cents per BE exit** at live size;
3. the one measurable case on the whole book says the change is **−0.133R**, i.e. worse;
4. it breaks the boot at ≥0.0020 and would need the assert fixed first regardless.

**What I would change instead — three zero-behaviour fixes, proposed only, not written:**

- **Re-document and rename at the declaration.** It is `BE_TARGET_BASE_FRAC`, not a minimum profit
  distance. Say that its fee derivation is now historical, that the real taker rate is 0.001, and
  that three of its four consumers are unreachable.
- **Cut the BE target loose from the fee arithmetic.** Make `_BE_TARGET_FRAC_ON` an explicit
  constant with its own justification, so "what should the breakeven lock lock in?" becomes a
  geometry decision with its own evidence — and so a future fee change cannot silently move a stop.
  Choosing **0.0029** would restore the promised small win; that is a decision for you, on its own
  merits, and it carries the −0.133R evidence above.
- **Fix the assert to test the real arm** — `SL_BUFFER_ATR × atr` against the BE target at the
  minimum plausible ATR — instead of `TRAIL_MIN_ACTIVATION_PCT`, which the arm has not used since
  A6. Mark `TRAIL_MIN_ACTIVATION_PCT` and `TRAIL_ACTIVATION_ATR_FIXED` as superseded; they exist
  only inside the assert and its docstring.

Say the word and I will bring those as a diff. None of them moves a price the bot trades on.

---

## WHAT I DID NOT TOUCH

Read-only throughout. No file written, no service restarted, **vpos 29 untouched** (its stop is
still the 74.9496/74.95 discussed above), no cascade, no thresholds, no prompts. DB access `mode=ro`;
the only network calls were public kline reads for the 7 replay windows.

```
mercury-sol   active   pid 3533821 / worker 3533987   open=1   0 tracebacks
venue         LONG 0.9 @ 74.80 · stop 74.95 · vpos 29 managed · unchanged by this pass
titan         active · HEAD 897850b · git clean · NOT TOUCHED
```
