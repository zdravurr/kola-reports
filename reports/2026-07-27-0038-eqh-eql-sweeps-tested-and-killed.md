# eqh-eql-sweeps-tested-and-killed

_2026-07-27 00:38 UTC_

---

# TITAN — do EQH/EQL sweeps predict anything? No. Leave the handler dead.

**2026-07-27 00:45 UTC · READ-ONLY.** Tree clean at `f0a8d30`.

**Verdict: the event has no directional edge, and the smart-TP rule it was built for would have cost
-971 on the clean sample, improving 5 of 14 positions.** Leave `_handle_liquidity_sweep` unreachable.
No code change described in §7, because it does not survive §6.

Data: 21,032 real 5m candles (OKX, 2026-05-15 → 2026-07-27, zero gaps) against 165 Equal H. and
139 Equal L..

---

## 1. The event itself — symmetric noise

Price move after the event, in %:

| event | horizon | n | median | mean | >0 | t |
|---|---|---|---|---|---|---|
| Equal H. | 15m | 165 | -0.023 | -0.012 | 47% | -0.9 |
| Equal H. | 1h | 165 | -0.017 | -0.036 | 46% | -1.4 |
| Equal H. | 4h | 165 | -0.045 | -0.145 | 45% | -2.3 |
| Equal H. | 12h | 164 | -0.078 | -0.327 | 46% | -3.3 |
| Equal L. | 15m | 139 | -0.021 | -0.019 | 43% | -1.2 |
| Equal L. | 1h | 139 | -0.016 | -0.019 | 47% | -0.5 |
| Equal L. | 4h | 139 | -0.034 | -0.045 | 49% | -0.8 |
| Equal L. | 12h | 138 | +0.214 | +0.067 | 56% | +0.7 |

**The thesis requires opposite signs** — EQH is resistance overhead (price should fall), EQL is
support beneath (price should rise). Instead both drift the *same* way at every horizon that matters:

```
EQL minus EQH, median:   15m +0.003%   ·   1h +0.001%   ·   4h +0.011%   ·   12h +0.292%
```
**Three thousandths of a percent at 15 minutes.** The two opposite-side events are indistinguishable.
EQH's t = -3.3 at 12h is not an edge — EQL drifts negative too at 15m/1h/4h; it is the sample
period's general downward drift showing through both. The only real spread appears at 12h, far
beyond the 5-8h median hold, and it is one horizon out of four.

## 2. As an exit signal — the smart-TP thesis, tested directly

102 sweeps landed while a position was open, across 27 positions. The rule (**EQH while LONG → close
LONG; EQL while SHORT → close SHORT**) would have fired on 51 of them, hitting 18 distinct positions
at their first occurrence.

```
 vp side      actual   smart-TP        Δ        vp side      actual   smart-TP        Δ
 33 SHORT     +0.78      -0.17     -0.94        59 LONG    -201.83     -30.42  +171.42
 35 LONG      +0.62      -0.04     -0.66        60 SHORT    -62.03     -39.87   +22.16
 43 SHORT   +168.54     +80.64    -87.90        62 LONG     -72.79     -24.39   +48.41
 45 LONG      +5.34     +30.70    +25.36        66 SHORT    -59.11     -69.04    -9.93
 50 SHORT   +292.60    -110.77   -403.37        71 LONG     -30.78      -0.25   +30.53
 54 LONG    +117.71     +29.37    -88.35        75 LONG     -14.52     -14.15    +0.37
 56 SHORT   +106.19     +32.84    -73.35        79 LONG     +80.10      +9.17   -70.93
 57 SHORT   +170.01    +168.10     -1.91        81 SHORT    +75.24    +114.34   +39.10
 58 SHORT   +370.45     -64.83   -435.28        82 LONG     +53.79     -15.15   -68.94
```
```
LONG   n=9   -62.36   ->   -15.15     Δ  +47.21
SHORT  n=9  +1062.67  ->  +111.26     Δ -951.41
TOTAL  n=18                           Δ -904.21    improved 7/18
```

**It destroys the short side.** vpos 58 (-435) and vpos 50 (-403) alone account for most of it: both
were large short winners that the rule would have closed early, on an EQL, while the move was still
running. That is the mechanism — EQL fires *into* a falling market, which is exactly when a short
should be held.

## 6. Decontaminated — it gets worse, not better

Excluding the wall-trail window and recheck-tightened positions leaves 14:
```
Δ -971.31    ·    improved 5 of 14
without the best trade:  -1142.73        without the worst: -536.03
without both:            -707.45
```
**Not outlier-driven in the direction that would rescue it.** Removing the single best case makes it
worse; removing the worst still leaves -536. Every subsetting keeps the sign.

## 3. As an entry filter — thin and confounded

```
sweep within 2h before entry:   n=18   net -155.94   win  6/18   median -36.06
no sweep within 2h:             n=32   net +949.13   win 17/32   median  +0.70
sweep within 30 min:            n= 2   net +173.34   win  2/2
```
Directionally it suggests entries shortly after a sweep do worse — but n=18 against 32, no
decontamination applied, and the 30-minute window has n=2. **This is not evidence, it is a cell
count.** Reported for completeness, not as a finding.

## 4. Confounding — the sweep is NOT "volatility was high"

| at the sweep moment | sweep (n=304) | all 5m signals (n≈17,160) |
|---|---|---|
| ADX-1h | 25.91 | 25.08 |
| vol_ratio_5m | 0.20 | 0.24 |
| ATR-1h | 351.44 | 351.70 |

**Indistinguishable from an ordinary 5m moment on every dimension.** Hour-of-day is spread (top
buckets 23, 19, 20, 02, 04 UTC — 17-21 occurrences each out of 304). So the event is not a proxy for
something already gated. It is simply not informative.

## 5. What the handler would have done

`_handle_liquidity_sweep` (main.py:2746-2912) records the sweep, then — with
`EQH_EQL_SMART_TP_ENABLED = True`, which it is — closes the matching open side and spawns a
60-minute MFE tracker on the closed trade. Simulated above on real candles: **-904 raw, -971 clean.**
The flag being already `True` means that, had the routing worked, this would have been live and
firing since May.

**The unreachable branch has been protecting the book.** That is luck, not design — but it is worth
stating plainly, because the instinct on finding a dead handler is to revive it.

---

## 7. No code change described

The brief asked for the minimal fix **if it survives**. It does not, so none is given. Name-based
recognition would be trivial — `classify()` already maps `Equal H. → (LIQUIDITY, SHORT, eqh, 0.9)`
— but making it reachable would switch on a rule that loses ~-971 on the clean sample.

**Recommendation: leave the handler dead.** The alerts are correct and are already doing useful work
as LIQUIDITY-category matrix weight (0.9 each). Their value is as one input among many, which is
what they are today — not as an exit trigger.

`EQH_EQL_SMART_TP_ENABLED = True` is worth noting in `OPEN-ITEMS`: the flag reads as armed and is
not, and anyone who fixes the routing without reading this report would arm a loss-making rule by
accident.

---

Nothing applied. Tree clean at `f0a8d30`; `titan.service`, `nginx`, `mercury-sol.service` healthy.
