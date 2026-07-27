# counterfactual-settled-on-candles

_2026-07-27 00:00 UTC_

---

# TITAN — counterfactual settled on real candles: 17 of 18 resolved

**2026-07-27 00:10 UTC · READ-ONLY.** Tree clean at `d12e276`, origin in sync.

**This supersedes both earlier attempts.** With 13,536 real 5m candles instead of internal samples,
**17 of 18 candidates resolve to a genuine terminal condition** — against 5 last time. Both earlier
conclusions were sampling artefacts and both are corrected below.

---

## Method

* **Data:** OKX 5m OHLCV, 2026-05-31 → 2026-07-16, **13,536 candles, zero gaps** in the series.
* **Replay:** walk candles from entry to actual-close + 72h. Per candle, in order: original SL hit
  (using the candle's adverse extreme) → +1R reached (favourable extreme) → breakeven armed + trail
  follows the water mark → trail trigger. Stop **never** moved below the original.
* **Conservative on ambiguity:** when one candle touches both the stop and the target, the **stop is
  taken first**. This biases the result *against* the fix.
* Same management logic and the same notional/fee reconstruction as the LONG-partial simulator, so
  the numbers are comparable.

---

## A. Stop never moved below the original — per position

| vpos | side | actual | replayed | Δ | at | terminal condition |
|---|---|---|---|---|---|---|
| 46 | SHORT | +241.37 | +243.07 | +1.70 | 10.8h | breakeven/trail |
| **47** | SHORT | -127.44 | **+537.93** | **+665.37** | 22.9h | breakeven/trail |
| 53 | SHORT | -106.86 | -196.30 | -89.44 | 2.0h | original SL |
| 55 | LONG | -78.70 | +80.34 | +159.04 | 19.0h | breakeven/trail |
| 57 | SHORT | +170.01 | +176.36 | +6.35 | 9.8h | breakeven/trail |
| 62 | LONG | -72.79 | — | — | — | **UNRESOLVED — still open at +72h** |
| 63 | LONG | -45.57 | +112.07 | +157.64 | 51.8h | breakeven/trail |
| 64 | LONG | +3.32 | +29.87 | +26.54 | 30.1h | breakeven/trail |
| 65 | LONG | -41.35 | -109.86 | -68.50 | 8.7h | original SL |
| 66 | SHORT | -59.11 | -115.49 | -56.38 | 12.2h | original SL |
| 67 | LONG | -32.73 | -128.31 | -95.58 | 10.0h | original SL |
| 68 | SHORT | -4.52 | +21.54 | +26.06 | 2.4h | breakeven/trail |
| 69 | LONG | -50.64 | -191.16 | -140.53 | 5.7h | original SL |
| 70 | LONG | -44.42 | +53.46 | +97.89 | 21.7h | breakeven/trail |
| 71 | LONG | -30.78 | -166.17 | -135.39 | 73.4h | original SL |
| 72 | LONG | -74.61 | -85.12 | -10.51 | 9.0h | original SL |
| 73 | LONG | -43.54 | -101.42 | -57.88 | 6.4h | original SL |
| 74 | SHORT | -73.09 | +16.04 | +89.13 | 19.8h | breakeven/trail |

```
resolved 17 / 18        terminal: breakeven/trail 9   ·   original SL 8
LONG   n=10   actual -439.01  ->  -506.28    Δ  -67.28
SHORT  n= 7   actual  +40.36  ->  +683.16    Δ +642.80
TOTAL  n=17   actual -398.65  ->  +176.87    Δ +575.52
unresolved: vpos 62 (actual -72.79) — still open at +72h, excluded, not marked to market
```

## The result is one trade

```
Δ total +575.52  ·  median per position +1.70  ·  positive on 9 of 17
without vpos 47 (+665.37):  Δ = -89.86
SHORT without vpos 47:      Δ = -22.58   (from +642.80)
LONG without its best:      Δ = -226.32  (from -67.28)
```
**vpos 47 alone is larger than the entire effect.** Remove it and the fix is mildly negative. The
median position gains +1.70 — i.e. nothing. Nine of seventeen improve, eight worsen: a coin flip
with one enormous tail.

## C. With the LONG partial applied in the same replay

```
LONG   n=10   -439.01  ->  -424.08    Δ  +14.93   (was -67.28)
SHORT  n= 7    +40.36  ->  +683.16    Δ +642.80   (unchanged — LONG-only by design)
TOTAL  n=17   -398.65  ->  +259.08    Δ +657.72
```
The partial fires on 4 of the 10 longs (55, 63, 64, 70) and turns the long side from −67.28 to
+14.93. Combined, not summed — each partial is taken inside the same walk that had already saved the
position from a moved stop.

---

## 5. Verdict

**On the full candidate set, the moved stops CAUSED losses rather than cutting them — but the
finding rests on a single trade and should not be treated as an estimate of anything.**

Two things must be said plainly, and both correct earlier claims of mine from today:

* **"11 of 11 would have survived at their original SL" was wrong.** On real candles **8 of 17 hit
  the original stop**, most of them losing more than they actually did. That claim came from
  `max_adverse_price`, which stops being recorded at the close.
* **Last session's "-335.84, the fix would have lost money" was also wrong** — and wrong because of
  sampling. Only 5 positions resolved on internal data, and those 5 were precisely the ones that
  resolved *fastest*, i.e. the ones that ran into the stop early. The slow resolvers, which mostly
  reached breakeven and trailed out, were invisible. That is survivorship bias in the resolution
  criterion, and real candles remove it.

**Coverage:** 17 of 18 candidates, representing **-398.65** of actual PnL. Against the full book
(49 closed, +739.40 net) this candidate set is the contaminated slice — about a third of positions
and, before the fix, a large part of the drawdown.

**What I will not claim:** that removing the wall-trail and bounding the recheck is worth ~+575, or
~+658 with the partial. One trade carries it, the median is +1.70, and the direction flips on any
single exclusion. The honest statement is: **the moved stops were not systematically protective, and
on this evidence they were mildly harmful with one very large individual cost.**

## 6. Not a case for restoring anything

Neither mechanism is proposed for return, and this result does not argue for it. Both fired on
evidence that did not exist — a wall multiple that oscillated **17 → 8 → 11 within five minutes**,
and a **single ADX reading** below a fixed floor. A rule that cuts a loss without knowing why is not
an edge; it is a coin flip with a story attached. That is exactly what the numbers above show: nine
better, eight worse, median nothing.

The value here is knowing the true cost, which is what was asked for.

---

Nothing applied. Tree clean at `d12e276`; `titan.service`, `nginx`, `mercury-sol.service` healthy.
