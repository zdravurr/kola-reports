# live-check-long-partial

_2026-07-26 22:26 UTC_

---

# TITAN — live check: LONG partial, 15m persistence, hourly consultations

**2026-07-26 22:26 UTC · READ-ONLY.** Tree clean at `ef7fa10`. Paper mode.

---

## 1. LONG partial — **FIRED. First live test of `f7df202` passed.**

```
2026-07-26T22:02:34  [VIRTUAL] LONG PARTIAL vpos=82 33% @ 65212.40 (+1.00R)
                     realised=+18.91  remainder rides unchanged
```
```sql
id | partial_taken | realized_partial_usdt | water_mark | initial_fill | original_sl | sl_price
82 |       1       |        18.907         |  65218.5   |   64779.8    |   64444.1   | 64909.36
```

**Arithmetic checks out, and the level is measured off `original_sl_price` as intended:**
```
entry 64779.8 · ORIGINAL sl 64444.1  ->  1R = 335.7
+1R level = 64779.8 + 335.7 = 65115.5
price traded through it; peak (water_mark) 65218.5 = +1.31R
partial taken at 65212.40 — the first poller tick past the level
```

**The remainder is riding the unchanged contract:**
```
leg size 0.154300 -> 0.102867 BTC        exactly 2/3 kept, 1/3 realised
original_sl_price 64444.1                UNCHANGED
breakeven_applied = True
sl_price 64909.36                        above entry -> breakeven armed, trail leading, +0.39R
```
+18.91 banked, two thirds protected at breakeven. Exactly the construction the change was for.

**No conclusion drawn: n=1.** Whether the old contract would have done better on this position is
unknowable until it closes. The mechanism works as designed; that is all this shows.

*(The 22:06 exit-advisor consultation read +1.17R — that was the remainder, four minutes after the
partial. Both figures are correct: peak +1.31R, partial taken at +1.00R, position at +1.17R when
the advisor looked.)*

---

## 2. n/a — the partial fired, so this question does not arise.

---

## 3. First `15m_confirm` row — **NOT YET. Zero rows.**

```sql
SELECT id, timestamp, tv_action, status FROM trades WHERE signal_type='15m_confirm';
-- (empty)
```

**Cause is timing, not the code:**
```
last 15m alert of any kind :  21:45:04   (a 15m EXIT-stream alert, task=price_action)
last 15m ENTRY alert       :  21:30      (hyperwave signal up, task=confirmation)
restart carrying the fix   :  22:07
now                        :  22:26
```
**No 15m alert of any kind has arrived since the restart.** Today's spacing between 15m entry
alerts is 45-75 min, so the next is due roughly 22:30-22:50. The write is in place and dry-run
verified; the event simply has not happened. Reported as **not yet observed**, not as working.

A background watcher is waiting on the first row.

---

## 4. Hourly consultations — **one so far, and it is not yet due again.**

```sql
id    | timestamp            | ai_decision | ai_confidence
18773 | 2026-07-26 22:06:11  | hold        | 0.72
```
Cadence is `EXIT_ADVISOR_HOURLY_SEC = 3600` measured from the last consultation, so the next one on
vpos 82 is due at **~23:06**. One consultation 20 minutes in is exactly on schedule — nothing is
missing.

---

## Summary

| check | result |
|---|---|
| LONG partial fired | **YES** — 33% @ 65212.40, +18.91 banked, remainder intact |
| +1R measured off `original_sl_price` | **YES** — 65115.5, price traded to 65218.5 |
| first `15m_confirm` row | **not yet** — no 15m alert since the 22:07 restart |
| hourly consultations on schedule | **yes** — 1 at 22:06, next due ~23:06 |

Nothing changed. Tree clean at `ef7fa10`, `titan.service` healthy, Mercury-SOL untouched.
