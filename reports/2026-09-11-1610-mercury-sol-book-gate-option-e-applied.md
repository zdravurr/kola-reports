# Mercury-SOL book-gate option E applied

_2026-09-11 16:10 UTC_

---

**2026-09-11 16:10 UTC · the workspace only, OUTSIDE both bot trees · Mercury-SOL and Titan are both LIVE and were not touched · basis: report 2026-09-11-1550 §4, option E · the second and final re-registration of the wires' arming, the operator's call**

## The answer first

1. **Option E has been live since 15:55:26 UTC,** in workspace commit `513eb13`: one script, plus its contract.
   - **Side wires** are read at **two fixed looks only**: the review-point pass, and the first pass on 2026-10-11. They still trip "above 5 %" and still need n ≥ 100 per side.
   - **The ratio wire** is read **once, at the 2026-10-11 look.** It still trips "above 2×" and still needs both sides at n ≥ 50.
   - Unchanged: the query, the anchor, the pinned floors, the review point, fire-once, and the stale-registration and unreadable-DB alerts.
2. **Re-measured: the expected 16.5 % and 23.9 % are confirmed, not corrected.**

   | noise alone trips at least one wire… | 06:12 | 15:32 | **E, live** |
   |---|---|---|---|
   | by the review point (≈ 100 per side) | 84.7 % | 44.5 % | **16.5 %** (exact 16.51 %) |
   | by 2026-10-11 (≈ 540 per side) | 93.2 % | 60.2 % | **23.9 %** (exact 23.86 %) |
   | the ratio wire alone, at its reading | 48.4 % | 37.3 % | **8.9 %** |

   - The same-seed Monte C. gives **16.2 % and 23.6 %** (RNG variants: 16.2–16.6 % and 23.5–23.9 %).
   - This is the first arming with both figures below 40 %. A wire alert is still a prompt to look, and the alert still says so.
3. **Power at E's looks:**
   - a true 7 % side rate is caught 70.9 % of the time at the review point, and 96.4 % at 2026-10-11 (97.5 % at either look);
   - a true 2.5× split is caught **72.8 %** at 2026-10-11 (the 15:32 arming: 59.3 %);
   - the 08-14 breach (5.67×) is caught **98.1 %** (the 15:32 arming: 79.9 %).
4. **The accepted cost is written down,** in the canon and in every alert. A side breach between the two looks waits for the next look instead of ringing within 30 min. The ratio is no longer read at the first review.
5. **The collapse case (1c) is defined and pinned.** Suppose the review point fires on the DATE 2026-10-11, with fewer than 200 rows. Then both looks are ONE pass:
   - one alert goes out;
   - each wire is read once, at that pass's counts — a side only at n ≥ 100, and the ratio only with both sides at n ≥ 50;
   - both looks are recorded with the same time;
   - no wire is ever read again (§3).
6. 🔴 **Found and fixed on this path: an overflow that would have silenced the 2026-10-11 look.**
   - The alert's noise line computed `float(comb(n, k))`, which overflows at **n ≥ 1,030 per side**. From there on, every alert raised `OverflowError` and the cron pass died before sending.
   - This is proven on the previous script (`0c58364`): at 1,029 per side the alert formats, and at 1,030 it raises. The defect was present from the 06:12 build.
   - At today's pace, about 1,000 per side by 2026-10-11, that is exactly where the second look lands.
   - It is now computed in log space, and the contract sends an alert at 1,100 per side (§4).
7. **Contract: 117/117 as botuser.** All 87 earlier checks are accounted for (§5a): 76 unchanged, 8 re-pointed to the looks, and 3 inverted — those three are the behaviour change.
   - **The new silence is pinned:** a side above 5 % at n ≥ 100 on a non-look pass is silent, where it used to fire.
   - **The mutants turn it red:** side wires read every pass fails **7** checks, and the ratio read at the review fails **21**. A third mutant, which restores the overflowing formula, fails **1**.
8. **The canon records it.** `§BOOK-GATE-RECUT-2026-09-11` has the second dated re-registration: the operator's call after reading 1550 §4, the figures beside the old ones, the power, the accepted cost and the collapse. The 15:32 subsection is marked ⚰️ superseded and kept.
9. **Neither bot was touched.**
   - No bot file changed, and nothing was restarted.
   - `NRestarts` stayed 0 → 0, with the same PIDs, on all three services.
   - `crontab -l` is byte-identical.
   - `openitems_guard` returned EXIT=0 before and after.
   - `--selftest` passes under `env -i`, and the suite is 267/267 as botuser.
   - **The live counter is at n = 30/200 (LONG 0/14, SHORT 0/16),** per `--selftest` at 16:00:3x. Nothing has fired, and no look has been taken.
   - **The first cron pass under option E ran at 16:00:04.** It logged `n=29/200 … looks_done=[] new=[]`: silent, as it must be.

---

## 1. The change

| wire | 06:12 (first build) | 15:32 (superseded) | **15:55 — option E (live, `513eb13`)** |
|---|---|---|---|
| side wire | every pass, n ≥ 50 | every pass, n ≥ 100 | **the review-point pass and the first pass on 2026-10-11 only**, n ≥ 100 |
| ratio wire | every pass, both sides n ≥ 50 | once, at the review point | **once, at the 2026-10-11 look**, both sides n ≥ 50 |
| thresholds | above 5 % · above 2× | unchanged | **unchanged** |

**In the code:**
- **Two constants now say when each wire is read:** `SIDE_LOOKS = (LOOK_REVIEW, LOOK_DATE)` and `RATIO_LOOKS = (LOOK_DATE,)`. `due_conditions()` reads a wire only when the current pass is one of its looks. The contract recomputes the false-alarm figures from these same constants.
- **`open_looks()` returns the looks the current pass is:**
  - the **review look** is the pass in which `review_point` is due and not yet fired;
  - the **date look** is the first pass on or after 2026-10-11 not yet recorded in the new `looks` map of the state file.
- **A look is recorded only once its alert, if any, has left.** A failed send records nothing, so the retry re-reads the same look. A look is never skipped and never read twice.
- **The wire reason says where it was read:** "read at the review point", "read at the 2026-10-11 look", or "read at the review point, which falls on 2026-10-11 (both looks in one pass)".
- **The alert text:**
  - a new WHEN-THEY-ARE-READ line replaces the ARMING line, and names the accepted cost and the collapse;
  - the FALSE-ALARM RATE line carries the E figures, with the 15:32 and 06:12 figures named as old;
  - a new POWER line.
- **`_pmf` is now computed in log space** (§4).
- **The log line gains `looks_done=[…]`.**

**How it went live.** The candidate script and contract were written to a botuser-readable temp directory. There, the contract was run against the candidate and against three mutants. Only once it was green and every mutant red were both files installed with `install` + `mv` (atomic), at 15:55:26 UTC. The installed sha256 values equal the tested candidates: script `b192c4627998dab0…`, contract `771dfd3e2556b910…`.

**Three alerts generated by the installed script** — synthetic counts, nothing sent:

**A — the review look, the 200th row: LONG 6/100 is read here, in the review-point alert; the 4× ratio is not**

```
[Mercury-SOL] BOOK-GATE REVIEW — ALERT
REVIEW POINT REACHED: 200 evaluations (>= 200)
WIRE TRIPPED: LONG 6/100 = 6.00 % is above 5 % at n 100 >= 100, read at the review point
Counted since the 09-11 re-cut, 2026-09-11 05:40:08 UTC · now 2026-09-14 04:30 UTC · 200/200 evaluations
LONG 6/100 refused = 6.00 % · registered 3.33 %
SHORT 2/100 refused = 2.00 % · registered 2.70 %
Side ratio: 3.00× (LONG higher) · registered 1.23×
Wires (pre-registered 09-11, thresholds unchanged): above 5 % on a side, or a side ratio above 2× → re-cut the ruler per side and say so. Never loosen quietly.
WHEN THEY ARE READ (re-registered 09-11 by the operator, after report 1550 §4, option E): the side wires at two fixed looks only, the review point and 2026-10-11, each side at n >= 100; the ratio once, at 2026-10-11, both sides at n >= 50. Between the looks nothing is read: a side breach there waits for the next look (cost accepted). If the review point itself falls on 2026-10-11, the two looks are one pass.
FALSE-ALARM LINE (0550 §5a): if the registered rates are true, the chance of a false alarm at the first review, about 100 per side, is LONG 11.7 %, SHORT 5.4 %. A LONG reading between 5 % and 6 % at the first review is within noise. Nobody re-cuts on that without reading this line.
FALSE-ALARM RATE OF THESE WIRES (registered rates true): at the review point, about 100 per side, noise alone trips at least one wire 16.5 % of the time, and by 2026-10-11, about 540 per side, 23.9 % — the ratio wire alone 8.9 %. Earlier armings, named as old: 44.5 % / 60.2 % (15:32 — the ratio at the review, the sides every pass) and 85 % / 93 % (06:12 — n >= 50, every pass). A wire alert is a prompt to look, not a finding.
POWER AT THESE LOOKS: a true 7 % side rate is caught 70.9 % at the review point and 96.4 % at 2026-10-11; a true 2.5× split 72.8 % and the 08-14 breach (5.67×) 98.1 % at 2026-10-11.
Noise at this n, registered rates assumed true: LONG above 5 % 11.73 % · SHORT above 5 % 5.42 % · ratio above 2× 37.33 %.
Canon: mercury-sol/OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11. Alert, not a report: each condition fires once (state .kola_state/sol_book_gate_review.json).
```

**B — the 2026-10-11 look, review already fired: the ratio is read once, here (2.50×)**

```
[Mercury-SOL] BOOK-GATE REVIEW — ALERT
WIRE TRIPPED: side ratio 2.50× (LONG higher) is above 2×, read at the 2026-10-11 look, both sides at n >= 50
Counted since the 09-11 re-cut, 2026-09-11 05:40:08 UTC · now 2026-10-11 00:00 UTC · 1080/200 evaluations
LONG 20/540 refused = 3.70 % · registered 3.33 %
SHORT 8/540 refused = 1.48 % · registered 2.70 %
Side ratio: 2.50× (LONG higher) · registered 1.23×
Wires (pre-registered 09-11, thresholds unchanged): above 5 % on a side, or a side ratio above 2× → re-cut the ruler per side and say so. Never loosen quietly.
WHEN THEY ARE READ (re-registered 09-11 by the operator, after report 1550 §4, option E): the side wires at two fixed looks only, the review point and 2026-10-11, each side at n >= 100; the ratio once, at 2026-10-11, both sides at n >= 50. Between the looks nothing is read: a side breach there waits for the next look (cost accepted). If the review point itself falls on 2026-10-11, the two looks are one pass.
FALSE-ALARM LINE (0550 §5a): if the registered rates are true, the chance of a false alarm at the first review, about 100 per side, is LONG 11.7 %, SHORT 5.4 %. A LONG reading between 5 % and 6 % at the first review is within noise. Nobody re-cuts on that without reading this line.
FALSE-ALARM RATE OF THESE WIRES (registered rates true): at the review point, about 100 per side, noise alone trips at least one wire 16.5 % of the time, and by 2026-10-11, about 540 per side, 23.9 % — the ratio wire alone 8.9 %. Earlier armings, named as old: 44.5 % / 60.2 % (15:32 — the ratio at the review, the sides every pass) and 85 % / 93 % (06:12 — n >= 50, every pass). A wire alert is a prompt to look, not a finding.
POWER AT THESE LOOKS: a true 7 % side rate is caught 70.9 % at the review point and 96.4 % at 2026-10-11; a true 2.5× split 72.8 % and the 08-14 breach (5.67×) 98.1 % at 2026-10-11.
Noise at this n, registered rates assumed true: LONG above 5 % 1.55 % · SHORT above 5 % 0.10 % · ratio above 2× 8.94 %.
Canon: mercury-sol/OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11. Alert, not a report: each condition fires once (state .kola_state/sol_book_gate_review.json).
```

**C — the collapse: 190 rows by 2026-10-11, the review point falls on the date — one pass, both looks**

```
[Mercury-SOL] BOOK-GATE REVIEW — ALERT
REVIEW POINT REACHED: the date is 2026-10-11 (190 evaluations, below 200)
WIRE TRIPPED: LONG 7/110 = 6.36 % is above 5 % at n 110 >= 100, read at the review point, which falls on 2026-10-11 (both looks in one pass)
WIRE TRIPPED: side ratio 5.09× (LONG higher) is above 2×, read at the review point, which falls on 2026-10-11 (both looks in one pass), both sides at n >= 50
Counted since the 09-11 re-cut, 2026-09-11 05:40:08 UTC · now 2026-10-11 00:00 UTC · 190/200 evaluations
LONG 7/110 refused = 6.36 % · registered 3.33 %
SHORT 1/80 refused = 1.25 % · registered 2.70 %
Side ratio: 5.09× (LONG higher) · registered 1.23×
Wires (pre-registered 09-11, thresholds unchanged): above 5 % on a side, or a side ratio above 2× → re-cut the ruler per side and say so. Never loosen quietly.
WHEN THEY ARE READ (re-registered 09-11 by the operator, after report 1550 §4, option E): the side wires at two fixed looks only, the review point and 2026-10-11, each side at n >= 100; the ratio once, at 2026-10-11, both sides at n >= 50. Between the looks nothing is read: a side breach there waits for the next look (cost accepted). If the review point itself falls on 2026-10-11, the two looks are one pass.
FALSE-ALARM LINE (0550 §5a): if the registered rates are true, the chance of a false alarm at the first review, about 100 per side, is LONG 11.7 %, SHORT 5.4 %. A LONG reading between 5 % and 6 % at the first review is within noise. Nobody re-cuts on that without reading this line.
FALSE-ALARM RATE OF THESE WIRES (registered rates true): at the review point, about 100 per side, noise alone trips at least one wire 16.5 % of the time, and by 2026-10-11, about 540 per side, 23.9 % — the ratio wire alone 8.9 %. Earlier armings, named as old: 44.5 % / 60.2 % (15:32 — the ratio at the review, the sides every pass) and 85 % / 93 % (06:12 — n >= 50, every pass). A wire alert is a prompt to look, not a finding.
POWER AT THESE LOOKS: a true 7 % side rate is caught 70.9 % at the review point and 96.4 % at 2026-10-11; a true 2.5× split 72.8 % and the 08-14 breach (5.67×) 98.1 % at 2026-10-11.
Noise at this n, registered rates assumed true: LONG above 5 % 16.14 % · SHORT above 5 % 6.56 % · ratio above 2× 49.39 %.
Canon: mercury-sol/OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11. Alert, not a report: each condition fires once (state .kola_state/sol_book_gate_review.json).
```

**And on a non-look pass — LONG 6/100 with 110 rows, mid-window — `due_conditions()` returns `{}`: no alert.** Under 15:32 this rang at once.

## 2. The re-measurement

**Exact, and the same-seed Monte C.** — the method of 1550 §2a: 40,000 paths, seed 20260911, registered rates true, n equal per side. The review look is at 100 per side, and the date look at 540 per side (the 0635 pace):

| | by the review point | by 2026-10-11 | LONG at 100 | SHORT at 100 | LONG at 540 | SHORT at 540 | ratio at 540 |
|---|---|---|---|---|---|---|---|
| **exact** | **16.51 %** | **23.86 %** | 11.73 % | 5.42 % | 1.55 % | 0.10 % | 8.94 % |
| MC `rng_random` | 16.21 % | 23.59 % | 11.53 % | 5.32 % | 1.61 % | 0.09 % | 8.88 % |
| MC, all 4 variants | 16.21–16.60 % | 23.54–23.94 % | 11.46–11.90 % | 5.30–5.56 % | 1.55–1.62 % | 0.07–0.11 % | 8.85–9.11 % |

- **The exact figure is computed three independent ways:**
  - the 1550 joint DP (`dp2.py`): 16.51 % and 23.86 %;
  - the two-look enumeration (`exact_e.py`, Appendix B): 16.51 % and 23.86 %;
  - the contract's own pure-Python recomputation from the script's constants: 16.51 % and 23.86 %.

  **16.5 % and 23.9 % are confirmed.**
- **The pace matters:**
  - The first ten hours of this era ran at about 34 per side per day. At that pace 2026-10-11 is about 1,080 per side.
  - There, the date-look figure is **18.70 %**, and the ratio alone is 2.74 %.
  - The review-point figure does not depend on the pace: 16.51 %.

**Power:** what E catches at its looks if the truth is NOT the registration (one look each, binomial):

| truth | the review look (100 per side) | the 2026-10-11 look (540 per side) | either look | the 15:32 arming |
|---|---|---|---|---|
| a side at 7 % | 70.86 % | 96.36 % | 97.54 % | 70.9 % at 100, and every pass after |
| a side at 10 % | 94.24 % | ≈ 100 % | 100.00 % | — |
| a 2.5× split (5.0 % / 2.0 %) | not read | **72.82 %** | — | 59.34 % (at the review) |
| the 08-14 breach, 5.67× (3.53 % / 0.62 %) | not read | **98.10 %** | — | 79.87 % (at the review) |

**The operator's argument, checked:** the ratio read later is better on both axes, with less noise (37.3 % → 8.9 %) and more power (79.9 % → 98.1 % on the 08-14 breach, 59.3 % → 72.8 % on 2.5×).

## 3. The collapse case (1c) — exactly what happens

**The review point fires on the date 2026-10-11 only if** fewer than 200 evaluations have arrived by then. That means below 3.4 per side per day, against the 18–34 seen so far.

**The first pass on or after 2026-10-11 00:00 UTC is then both looks at once:**
- **One alert.** It carries the review point (reason: "the date is 2026-10-11"), plus every wire that trips. Each wire reason reads "read at the review point, which falls on 2026-10-11 (both looks in one pass)".
- **Each side wire is read once,** at that pass's counts, and only for a side at n ≥ 100. With fewer than 200 rows, at most one side can be at 100 or more.
- **The ratio is read once,** if both sides are at n ≥ 50.
- **Both looks are recorded** in `looks` with the same time. There is no second side look: at the collapse, the two looks are one reading.
- **After it, no wire is ever read again.**
- **At such low n the ratio carries its binomial noise:** 48.4 % at 50 per side, 42.2 % at 75 and 37.5 % at 99. The alert prints it in "Noise at this n".

**Pinned by the contract (§5b):**
- **190 rows by 2026-10-11** (LONG 7/110, SHORT 1/80): ONE alert, with the review point, the LONG side wire and the ratio (5.09×). "Both looks in one pass" is in the text, and both looks are in the state with ONE timestamp.
- **The next pass,** with SHORT at 8/110 = 7.27 %: silent.
- **At the collapse, SHORT at 5/80 = 6.25 % is not read** (n < 100), while LONG at 7/110 is.
- **Sides at 40:** the ratio is not read. **Sides at 60 with ∞:** the ratio is in the same alert.

## 4. 🔴 Found and fixed: the alert text overflowed at n ≥ 1,030 per side

**What was wrong.** `_pmf()` computed `comb(n, k) * p**k * …`, and Python cannot convert `comb(n, k)` to a float beyond about 10³⁰⁸. The noise line ("Noise at this n") calls `_pmf(n, …)` on every alert. So at n ≥ 1,030 per side, `format_alert()` raised, `run()` raised with it, and the cron pass died before sending. The only traces were a traceback in a log nobody reads, and an alert that never left.

**Proven on the script that was live until 15:55** (`0c58364`), with synthetic counts and nothing sent:
```
n=1000/side: alert formats
n=1029/side: alert formats
n=1030/side: OverflowError: int too large to convert to float
n=1100/side: OverflowError: int too large to convert to float
```

**Why it mattered now.** Under every earlier arming, the defect could only bite a wire at very large n. Under E, the second look is **by construction** read at the largest n of the window. At today's pace (about 34 per side per day), 2026-10-11 is about 1,000–1,080 per side — right at the edge.

**The fix.** `_pmf()` now computes the binomial in log space (`lgamma`, `log1p`, `exp`). The §5a figures are unchanged, and the contract still reads 11.7 %, 5.4 %, 7.3 % and 2.1 %. The contract now runs the 2026-10-11 look at **1,100 per side** and requires the alert to leave. With the old formula restored, that check is red: mutant m3, §5b.

## 5. The contract — `tests/test_sol_book_gate_review_fires.py`, 117/117

### 5a. All 87 earlier checks are accounted for

The comparison is by check name, between the `0c58364` contract's output (87 ✅) and the new one (117 ✅):

- **76 keep their names and assertions.** Some are now staged at a look, because the old mid-window staging is silent by design:
  - "SHORT 6/100 = 6 % — тревога wire_rate_SHORT", "в тексте причина, доля и взвод", "строка ложной тревоги §5a есть и в тревоге провода", "и текущая доля ложных тревог проводов" and "старой строки «≈ 85 %» нет и здесь" are now proven on the review-look alert;
  - "LONG 5/100 = ровно 5 %" and "LONG 6/120 = ровно 5 %" are now proven at the review look;
  - "уже сработало — тишина" is now proven at the date look, after firing at the review;
  - "отношение стоит рядом с долями сторон" and "и ∞ названо в тексте" are now proven on the date-look ratio alert;
  - "в тексте тревоги: взвод стороны / взвод отношения" now check the WHEN-THEY-ARE-READ wording.
- **3 are INVERTED — this is the behaviour change.** They pinned 15:32 behaviour that option E removes:

  | 15:32 check (it passed) | now (it passes) |
  |---|---|
  | 🔴 LONG 6/100 = 6 % при n=100 — тревога СРАЗУ, посреди окна (110 оценок) | 🔴 LONG 6/100 … 110 оценок — НЕ взгляд — **ТИШИНА** (the same for SHORT), and it fires at the review look |
  | 🔴 200-я строка, 4.00× — ОДНА тревога, и провод отношения В НЕЙ | 🔴 200-я строка, 4.00× — **только review_point**: на ревью отношение больше НЕ читается |
  | ∞ в точке ревью — провод отношения | ∞ в точке ревью — **тоже только review_point**, and at the date look — провод отношения |

- **8 are RE-POINTED.** The property is the same, now proven where E reads it, or with E's recomputed figure:
  - the three "в тексте «X %» … = точный пересчёт" checks now read 16.5 %, 23.9 % and 8.9 % (they were 44.5 %, 60.2 % and 37.3 %), still recomputed from the script's constants;
  - "в тексте и точка ревью, и отношение" is now "в тексте отношение и где прочитано: на взгляде 2026-10-11";
  - "ровно 2× в точке ревью" is now "ровно 2× на взгляде 2026-10-11 — тишина";
  - "отправка в проходе ревью упала" and "повтор — всё ещё проход ревью: и точка, и отношение" now each exist twice: for the date look (the ratio) and for the review look (a side wire);
  - "точка ревью при 1.50× — только review_point" is covered by §2's "сработало условие review_point (1.50× …)" and asserted in every `reviewed()` setup.

**30 checks are new.** Among them:
- the non-look silence, both before the review and between the looks (2026-09-20, and one second before 2026-10-11);
- the side wire at each look, and where it was read;
- n = 99 not read at a look;
- exactly 5 % at the date look;
- the ratio at the date look, with exactly 2× silent and ∞ firing;
- the date look recorded once, whether a wire trips or not;
- silence the next pass and the next day;
- a failed send at either look, and its retry;
- the collapse (§3);
- the 1,100-per-side send (§4);
- the look constants pinned;
- the new figures and the power, recomputed.

### 5b. Mutation check

Each mutant is the installed script with ONE replacement, run under the installed contract through `SOL_BGR_SCRIPT`. The live file was never swapped, and the suite never sets the variable.
- **m1** — side wires read on every pass: `if any(lk in now_looks for lk in SIDE_LOOKS):` → `if True:`.
- **m2** — the ratio read at the review point: `RATIO_LOOKS = (LOOK_DATE,)` → `(LOOK_REVIEW,)`.
- **m3** — the overflowing `_pmf` restored.

```
candidate script b192c4627998dab0 · candidate contract 771dfd3e2556b910 · each mutant = the candidate with ONE replacement

== m1_side_every_pass: EXIT=1 · red checks: 7
  ❌ 🔴 LONG 6/100 = 6 % при n=100, 110 оценок — НЕ взгляд — ТИШИНА (в 15:32 звонило сразу)
  ❌ 🔴 SHORT 6/100 = 6 % при n=100, 110 оценок — НЕ взгляд — ТИШИНА (в 15:32 звонило сразу)
  ❌ 🔴 между взглядами (ревью было, 2026-09-20) LONG 9/130 = 6.92 % — ТИШИНА
  ❌ и за секунду до 2026-10-11 при 8.33 % — ТИШИНА
  ❌ 🔴 следующий проход того же дня, 6.00× — ТИШИНА: взгляд записан
  ❌ 🔴 2026-10-12, 6.00× и LONG 5.36 % — ТИШИНА: после взгляда провода не читаются никогда
  ❌ 🔴 следующий проход — SHORT 8/110 = 7.27 % — ТИШИНА: второго взгляда при слиянии нет

== m2_ratio_at_review: EXIT=1 · red checks: 21
  ❌ LONG 5/100 = ровно 5 % при n=100 — тишина (порог «выше»)
  ❌ LONG 6/120 = ровно 5 % при n=120 — тишина
  ❌ 🔴 LONG 6/100 = 6 % на взгляде ревью (200-я строка) — ОДНА тревога, провод стороны в ней
  ❌ взгляд ревью, LONG 8/99 = 8.08 % при n=99 — не читается (взвод 100 не тронут)
  ❌ 🔴 200-я строка, 4.00× — только review_point: на ревью отношение больше НЕ читается (в 15:32 читалось)
  ❌ но отношение стоит в тексте ревью как показание, рядом с долями сторон
  ❌ ∞ в точке ревью — тоже только review_point
  ❌ 🔴 взгляд 2026-10-11: 3.70 % против 1.48 % = 2.50× — тревога wire_ratio
  ❌ в тексте отношение и где прочитано: на взгляде 2026-10-11, без точки ревью
  ❌ отношение стоит рядом с долями сторон
  ❌ 🔴 следующий проход того же дня, 6.00× — ТИШИНА: взгляд записан
  ❌ ∞ на взгляде 2026-10-11 — провод отношения
  ❌ и ∞ названо в тексте
  ❌ отправка на взгляде 2026-10-11 упала — ничего не помечено, взгляд не записан
  ❌ повтор — всё ещё взгляд 2026-10-11: отношение, и взгляд записан
  ❌ 🔴 взгляд 2026-10-11 при n = 1100 на сторону (темп сегодня): тревога УХОДИТ — строка шума не падает на переполнении (до исправления — OverflowError, проход умирал молча)
  ❌ повтор — всё ещё взгляд ревью: и точка, и провод стороны
  ❌ 🔴 взгляды (вариант E): стороны — ревью и 2026-10-11, отношение — только 2026-10-11
  ❌ 🔴 в тексте «44.5 %» к точке ревью = точный пересчёт
  ❌ в тексте «45.1 %» к 2026-10-11 = точный пересчёт
  ❌ в тексте «37.3 %» для одного отношения = точный пересчёт

== m3_pmf_overflow: EXIT=1 · red checks: 1
  ❌ 🔴 взгляд 2026-10-11 при n = 1100 на сторону (темп сегодня): тревога УХОДИТ — строка шума не падает на переполнении (до исправления — OverflowError, проход умирал молча)

ALL_MUTANTS_RED=1
```

### 5c. Full output — the installed contract, as botuser, no override

```
script under test: /home/botuser/.openclaw/workspace/scripts/sol_book_gate_review.py
── 1. ЗАПРОС — ДОСЛОВНО §5b, И ОН ИДЁТ НА ЖИВОЙ СХЕМЕ ─────────────────
  ✅ QUERY дословно совпадает с SQL-блоком §5b отчёта 0550
  ✅ якорь в запросе = ANCHOR
  ✅ запрос исполняется на живой trades.db (mode=ro)

── 2. 🔴 199 — ТИШИНА; 200-я — ОДНА ТРЕВОГА С ЦИФРАМИ; ПОТОМ ТИШИНА ─────
2026-09-11T15:55:26Z [sol_book_gate_review] n=199/200 LONG 3/100 SHORT 2/99 ratio=1.48× fired_ever=[] looks_done=[] new=[]
  ✅ 199 оценок (3.00 % / 2.02 %, 1.49×) — ни одной отправки
  ✅ и в состоянии ничего не помечено
2026-09-11T15:55:26Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:26Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
  ✅ 🔴 синтетическая 200-я строка — ровно ОДНА тревога
  ✅ сработало условие review_point (1.50× — провод отношения не сработал)
  ✅ в тексте тревоги: причина
  ✅ в тексте тревоги: n всего
  ✅ в тексте тревоги: LONG n и отказы и доля
  ✅ в тексте тревоги: SHORT n и отказы и доля
  ✅ в тексте тревоги: ожидание LONG
  ✅ в тексте тревоги: ожидание SHORT
  ✅ в тексте тревоги: отношение и ожидание
  ✅ в тексте тревоги: строка ложной тревоги §5a
  ✅ в тексте тревоги: строка §5a
  ✅ в тексте тревоги: провода
  ✅ в тексте тревоги: пороги не сдвинуты
  ✅ в тексте тревоги: взвод стороны
  ✅ в тексте тревоги: взвод отношения
  ✅ в тексте тревоги: принятая цена
  ✅ в тексте тревоги: слияние взглядов
  ✅ в тексте тревоги: текущая доля ложных тревог проводов
  ✅ в тексте тревоги: мощность взглядов
  ✅ 🔴 старой строки «≈ 85 % до ревью» в тексте БОЛЬШЕ НЕТ
2026-09-11T15:55:26Z [sol_book_gate_review] n=205/200 LONG 3/103 SHORT 2/102 ratio=1.49× fired_ever=['review_point'] looks_done=['review_point'] new=[]
  ✅ 🔴 уже сработало — 205 оценок, повторного звонка нет

── 3. ДАТА 2026-10-11 ПРИ n < 200 ───────────────────────────────────
2026-09-11T15:55:26Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=[] looks_done=[] new=[]
  ✅ 2026-10-10 23:59:59 — тишина
2026-09-11T15:55:26Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:26Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=['review_point'] looks_done=['2026-10-11', 'review_point'] new=['review_point']
  ✅ 2026-10-11 00:00:00 — одна тревога review_point
  ✅ причина названа датой
2026-09-11T15:55:26Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=['review_point'] looks_done=['2026-10-11', 'review_point'] new=[]
  ✅ на следующий день — тишина

── 4. 🔴 ПРОВОД СТОРОНЫ — ТОЛЬКО НА ДВУХ ВЗГЛЯДАХ, n >= 100, ВЫШЕ 5 % ─────
2026-09-11T15:55:26Z [sol_book_gate_review] n=60/200 LONG 3/50 SHORT 0/10 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 LONG 3/50 = 6.00 % при n=50 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:55:26Z [sol_book_gate_review] n=70/200 LONG 4/60 SHORT 0/10 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 LONG 4/60 = 6.67 % при n=60 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:55:26Z [sol_book_gate_review] n=90/200 LONG 5/80 SHORT 0/10 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 LONG 5/80 = 6.25 % при n=80 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:55:26Z [sol_book_gate_review] n=109/200 LONG 6/99 SHORT 0/10 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 LONG 6/99 = 6.06 % при n=99 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:55:26Z [sol_book_gate_review] n=60/200 LONG 0/10 SHORT 3/50 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 SHORT 3/50 = 6.00 % при n=50 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:55:26Z [sol_book_gate_review] n=70/200 LONG 0/10 SHORT 4/60 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 SHORT 4/60 = 6.67 % при n=60 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:55:26Z [sol_book_gate_review] n=90/200 LONG 0/10 SHORT 5/80 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 SHORT 5/80 = 6.25 % при n=80 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:55:26Z [sol_book_gate_review] n=109/200 LONG 0/10 SHORT 6/99 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 SHORT 6/99 = 6.06 % при n=99 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:55:26Z [sol_book_gate_review] n=110/200 LONG 6/100 SHORT 0/10 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 LONG 6/100 = 6 % при n=100, 110 оценок — НЕ взгляд — ТИШИНА (в 15:32 звонило сразу)
2026-09-11T15:55:26Z [sol_book_gate_review] n=110/200 LONG 0/10 SHORT 6/100 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 SHORT 6/100 = 6 % при n=100, 110 оценок — НЕ взгляд — ТИШИНА (в 15:32 звонило сразу)
2026-09-11T15:55:26Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:26Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:26Z [sol_book_gate_review] n=250/200 LONG 9/130 SHORT 2/120 ratio=4.15× fired_ever=['review_point'] looks_done=['review_point'] new=[]
  ✅ 🔴 между взглядами (ревью было, 2026-09-20) LONG 9/130 = 6.92 % — ТИШИНА
2026-09-11T15:55:26Z [sol_book_gate_review] n=600/200 LONG 25/300 SHORT 3/300 ratio=8.33× fired_ever=['review_point'] looks_done=['review_point'] new=[]
  ✅ и за секунду до 2026-10-11 при 8.33 % — ТИШИНА
2026-09-11T15:55:26Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:26Z [sol_book_gate_review] n=200/200 LONG 5/100 SHORT 2/100 ratio=2.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
  ✅ LONG 5/100 = ровно 5 % при n=100 — тишина (порог «выше»)
2026-09-11T15:55:26Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:26Z [sol_book_gate_review] n=200/200 LONG 6/120 SHORT 1/80 ratio=4.00× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
  ✅ LONG 6/120 = ровно 5 % при n=120 — тишина
2026-09-11T15:55:26Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:26Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:26Z [sol_book_gate_review] n=1080/200 LONG 27/540 SHORT 16/540 ratio=1.69× fired_ever=['review_point'] looks_done=['2026-10-11', 'review_point'] new=[]
  ✅ LONG 27/540 = ровно 5 % на взгляде 2026-10-11 — тишина
2026-09-11T15:55:26Z [sol_book_gate_review] due=['review_point', 'wire_rate_LONG'] DELIVERED=True
2026-09-11T15:55:26Z [sol_book_gate_review] n=200/200 LONG 6/100 SHORT 2/100 ratio=3.00× fired_ever=['review_point', 'wire_rate_LONG'] looks_done=['review_point'] new=['review_point', 'wire_rate_LONG']
  ✅ 🔴 LONG 6/100 = 6 % на взгляде ревью (200-я строка) — ОДНА тревога, провод стороны в ней
  ✅ в тексте причина, доля и взвод
  ✅ и где прочитан: на точке ревью
  ✅ строка ложной тревоги §5a есть и в тревоге провода
  ✅ 🔴 и текущая доля ложных тревог проводов
  ✅ старой строки «≈ 85 %» нет и здесь
2026-09-11T15:55:26Z [sol_book_gate_review] n=1080/200 LONG 40/540 SHORT 20/540 ratio=2.00× fired_ever=['review_point', 'wire_rate_LONG'] looks_done=['2026-10-11', 'review_point'] new=[]
  ✅ уже сработало — тишина
2026-09-11T15:55:26Z [sol_book_gate_review] due=['review_point', 'wire_rate_SHORT'] DELIVERED=True
2026-09-11T15:55:26Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 6/100 ratio=2.00× fired_ever=['review_point', 'wire_rate_SHORT'] looks_done=['review_point'] new=['review_point', 'wire_rate_SHORT']
  ✅ SHORT 6/100 = 6 % — тревога wire_rate_SHORT
2026-09-11T15:55:26Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:26Z [sol_book_gate_review] n=200/200 LONG 8/99 SHORT 1/101 ratio=8.16× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
  ✅ взгляд ревью, LONG 8/99 = 8.08 % при n=99 — не читается (взвод 100 не тронут)
2026-09-11T15:55:27Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:27Z [sol_book_gate_review] due=['wire_rate_LONG'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=1080/200 LONG 30/540 SHORT 16/540 ratio=1.87× fired_ever=['review_point', 'wire_rate_LONG'] looks_done=['2026-10-11', 'review_point'] new=['wire_rate_LONG']
  ✅ 🔴 взгляд 2026-10-11: LONG 30/540 = 5.56 % — тревога провода стороны
  ✅ и где прочитан: на взгляде 2026-10-11

── 5. 🔴 ПРОВОД ОТНОШЕНИЯ — ОДИН РАЗ, НА ВЗГЛЯДЕ 2026-10-11 ─────────────
2026-09-11T15:55:27Z [sol_book_gate_review] n=110/200 LONG 2/50 SHORT 1/60 ratio=2.40× fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 2.40× посреди окна (110 оценок, обе n >= 50) — ТИШИНА (раньше звонило)
2026-09-11T15:55:27Z [sol_book_gate_review] n=100/200 LONG 1/50 SHORT 0/50 ratio=∞ fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 ∞ посреди окна (SHORT 0 отказов при n=50) — ТИШИНА
2026-09-11T15:55:27Z [sol_book_gate_review] n=199/200 LONG 4/100 SHORT 1/99 ratio=3.96× fired_ever=[] looks_done=[] new=[]
  ✅ 🔴 3.96× при 199 оценках — ТИШИНА: за строку до ревью отношение не читается
  ✅ и в состоянии ничего не помечено
2026-09-11T15:55:27Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=200/200 LONG 4/100 SHORT 1/100 ratio=4.00× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
  ✅ 🔴 200-я строка, 4.00× — только review_point: на ревью отношение больше НЕ читается (в 15:32 читалось)
  ✅ но отношение стоит в тексте ревью как показание, рядом с долями сторон
2026-09-11T15:55:27Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=200/200 LONG 2/100 SHORT 0/100 ratio=∞ fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
  ✅ ∞ в точке ревью — тоже только review_point
2026-09-11T15:55:27Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:27Z [sol_book_gate_review] n=240/200 LONG 5/120 SHORT 1/120 ratio=5.00× fired_ever=['review_point'] looks_done=['review_point'] new=[]
  ✅ 🔴 после прохода ревью 5.00× — ТИШИНА: отношение читается ОДИН раз
2026-09-11T15:55:27Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:27Z [sol_book_gate_review] due=['wire_ratio'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=1080/200 LONG 20/540 SHORT 8/540 ratio=2.50× fired_ever=['review_point', 'wire_ratio'] looks_done=['2026-10-11', 'review_point'] new=['wire_ratio']
  ✅ 🔴 взгляд 2026-10-11: 3.70 % против 1.48 % = 2.50× — тревога wire_ratio
  ✅ в тексте отношение и где прочитано: на взгляде 2026-10-11, без точки ревью
  ✅ отношение стоит рядом с долями сторон
2026-09-11T15:55:27Z [sol_book_gate_review] n=1090/200 LONG 30/545 SHORT 5/545 ratio=6.00× fired_ever=['review_point', 'wire_ratio'] looks_done=['2026-10-11', 'review_point'] new=[]
  ✅ 🔴 следующий проход того же дня, 6.00× — ТИШИНА: взгляд записан
  ✅ в состоянии записан взгляд 2026-10-11
2026-09-11T15:55:27Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:27Z [sol_book_gate_review] n=1080/200 LONG 20/540 SHORT 10/540 ratio=2.00× fired_ever=['review_point'] looks_done=['2026-10-11', 'review_point'] new=[]
  ✅ ровно 2× на взгляде 2026-10-11 (20 против 10) — тишина
  ✅ и взгляд всё равно записан — второго чтения не будет
2026-09-11T15:55:27Z [sol_book_gate_review] n=1120/200 LONG 30/560 SHORT 5/560 ratio=6.00× fired_ever=['review_point'] looks_done=['2026-10-11', 'review_point'] new=[]
  ✅ 🔴 2026-10-12, 6.00× и LONG 5.36 % — ТИШИНА: после взгляда провода не читаются никогда
2026-09-11T15:55:27Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:27Z [sol_book_gate_review] due=['wire_ratio'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=1080/200 LONG 5/540 SHORT 0/540 ratio=∞ fired_ever=['review_point', 'wire_ratio'] looks_done=['2026-10-11', 'review_point'] new=['wire_ratio']
  ✅ ∞ на взгляде 2026-10-11 — провод отношения
  ✅ и ∞ названо в тексте
2026-09-11T15:55:27Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:27Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:28Z [sol_book_gate_review] due=['wire_ratio'] DELIVERED=False
2026-09-11T15:55:28Z [sol_book_gate_review] n=1080/200 LONG 20/540 SHORT 8/540 ratio=2.50× fired_ever=['review_point'] looks_done=['review_point'] new=[]
  ✅ отправка на взгляде 2026-10-11 упала — ничего не помечено, взгляд не записан
2026-09-11T15:55:28Z [sol_book_gate_review] due=['wire_ratio'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=1080/200 LONG 20/540 SHORT 8/540 ratio=2.50× fired_ever=['review_point', 'wire_ratio'] looks_done=['2026-10-11', 'review_point'] new=['wire_ratio']
  ✅ повтор — всё ещё взгляд 2026-10-11: отношение, и взгляд записан
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:28Z [sol_book_gate_review] due=['wire_ratio'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=2200/200 LONG 40/1100 SHORT 15/1100 ratio=2.67× fired_ever=['review_point', 'wire_ratio'] looks_done=['2026-10-11', 'review_point'] new=['wire_ratio']
  ✅ 🔴 взгляд 2026-10-11 при n = 1100 на сторону (темп сегодня): тревога УХОДИТ — строка шума не падает на переполнении (до исправления — OverflowError, проход умирал молча)

── 5b. 🔴 СЛИЯНИЕ — ТОЧКА РЕВЬЮ ПРИХОДИТ ДАТОЙ 2026-10-11: ОДИН ПРОХОД ─────
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point', 'wire_rate_LONG', 'wire_ratio'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=190/200 LONG 7/110 SHORT 1/80 ratio=5.09× fired_ever=['review_point', 'wire_rate_LONG', 'wire_ratio'] looks_done=['2026-10-11', 'review_point'] new=['review_point', 'wire_rate_LONG', 'wire_ratio']
  ✅ 🔴 190 оценок к 2026-10-11: ОДНА тревога — точка ревью, провод LONG и отношение
  ✅ в тексте: причина — дата, и оба взгляда в одном проходе
  ✅ в состоянии оба взгляда, с ОДНОЙ меткой времени
2026-09-11T15:55:28Z [sol_book_gate_review] n=225/200 LONG 9/115 SHORT 8/110 ratio=1.08× fired_ever=['review_point', 'wire_rate_LONG', 'wire_ratio'] looks_done=['2026-10-11', 'review_point'] new=[]
  ✅ 🔴 следующий проход — SHORT 8/110 = 7.27 % — ТИШИНА: второго взгляда при слиянии нет
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point', 'wire_rate_LONG'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=190/200 LONG 7/110 SHORT 5/80 ratio=1.02× fired_ever=['review_point', 'wire_rate_LONG'] looks_done=['2026-10-11', 'review_point'] new=['review_point', 'wire_rate_LONG']
  ✅ слияние: SHORT 5/80 = 6.25 % при n=80 не читается (взвод 100), LONG 7/110 читается
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=80/200 LONG 2/40 SHORT 0/40 ratio=∞ fired_ever=['review_point'] looks_done=['2026-10-11', 'review_point'] new=['review_point']
  ✅ ревью по дате, стороны по 40 (< 50) — отношение не читается (взвод 50 не тронут)
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point', 'wire_ratio'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=120/200 LONG 3/60 SHORT 0/60 ratio=∞ fired_ever=['review_point', 'wire_ratio'] looks_done=['2026-10-11', 'review_point'] new=['review_point', 'wire_ratio']
  ✅ ревью по дате, стороны по 60 и ∞ — провод отношения в той же тревоге

── 6. ОТПРАВКА УПАЛА — НЕ ПОМЕЧЕНО, СЛЕДУЮЩИЙ ПРОХОД ПОВТОРЯЕТ ─────────
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point'] DELIVERED=False
2026-09-11T15:55:28Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=[] looks_done=[] new=[]
  ✅ отправка вернула False — код 1, ничего не помечено
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
  ✅ следующий проход — тревога ушла
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point', 'wire_rate_LONG'] DELIVERED=False
2026-09-11T15:55:28Z [sol_book_gate_review] n=200/200 LONG 6/100 SHORT 2/100 ratio=3.00× fired_ever=[] looks_done=[] new=[]
  ✅ взгляд ревью с проводом LONG, отправка упала — взгляд не записан
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point', 'wire_rate_LONG'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=200/200 LONG 6/100 SHORT 2/100 ratio=3.00× fired_ever=['review_point', 'wire_rate_LONG'] looks_done=['review_point'] new=['review_point', 'wire_rate_LONG']
  ✅ повтор — всё ещё взгляд ревью: и точка, и провод стороны

── 7. mode=ro — ЗАПИСЬ НЕВОЗМОЖНА, ФАЙЛ НЕ ТРОНУТ ─────────────────────
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
2026-09-11T15:55:28Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:55:28Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] looks_done=['review_point'] new=['review_point']
  ✅ sha256 БД после двух проходов тот же
  ✅ соединение скрипта отвергает INSERT (readonly)

── 8. ШУМ В ТЕКСТЕ = §5a; ДОЛЯ ЛОЖНЫХ ТРЕВОГ И МОЩНОСТЬ = ТОЧНЫЙ ПЕРЕСЧЁТ ──
  ✅ P(LONG>5 %) при n=100 = 11.7 %
  ✅ P(SHORT>5 %) при n=100 = 5.4 %
  ✅ P(LONG>5 %) при n=200 = 7.3 %
  ✅ P(SHORT>5 %) при n=200 = 2.1 %
  ✅ 🔴 взвод: сторона n >= 100, отношение при обеих n >= 50 (перерегистрация 09-11)
  ✅ пороги не сдвинуты: 5 % и 2×
  ✅ 🔴 взгляды (вариант E): стороны — ревью и 2026-10-11, отношение — только 2026-10-11
     точно: к ревью 16.51 % · к 2026-10-11 23.86 % · отношение 8.94 % · мощность 7 % at the review 70.86 % · 7 % at 2026-10-11 96.36 % · 2.5× 72.82 % · 5.67× 98.10 %
  ✅ 🔴 до точки ревью ни один провод не может сработать от шума (0 %)
  ✅ 🔴 в тексте «16.5 %» к точке ревью = точный пересчёт
  ✅ в тексте «23.9 %» к 2026-10-11 = точный пересчёт
  ✅ в тексте «8.9 %» для одного отношения = точный пересчёт
  ✅ старые цифры названы как старые (85 % / 93 %)
  ✅ и прошлые цифры 15:32 названы как старые (44.5 % / 60.2 %)
  ✅ 🔴 мощность в тексте = пересчёт: 7 % → 70.9 % на ревью, 96.4 % на 2026-10-11
  ✅ мощность: 2.5× → 72.8 %, 5.67× → 98.1 % на 2026-10-11

── 9. РЕГИСТРАЦИЯ СДВИНУЛАСЬ — СЧЁТЧИК ГОВОРИТ, ЧТО УСТАРЕЛ ────────────
2026-09-11T15:55:29Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=[] looks_done=[] new=[]
  ✅ полы совпадают с 09-11 — тишина
2026-09-11T15:55:29Z [sol_book_gate_review] config floors {'LONG': 0.43, 'SHORT': 0.4} != pinned {'LONG': 0.4214, 'SHORT': 0.3975}; alert DELIVERED=True
2026-09-11T15:55:29Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=['registration_moved:{"LONG": 0.43, "SHORT": 0.4}'] looks_done=[] new=['registration_moved:{"LONG": 0.43, "SHORT": 0.4}']
  ✅ полы в config.py другие — одна тревога «устарел»
2026-09-11T15:55:29Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=['registration_moved:{"LONG": 0.43, "SHORT": 0.4}'] looks_done=[] new=[]
  ✅ повторно — тишина
  ✅ 🔴 ЖИВОЙ SOL config.py сейчас = приколотая регистрация 09-11 (красный здесь = перерез был, а счётчик не перенацелен)

── 10. БД НЕ ЧИТАЕТСЯ — ПЕРЕПРОС, ОДНА ТРЕВОГА НА ПОЛОМКУ ───────────────
2026-09-11T15:55:29Z [sol_book_gate_review] read failed (unable to open database file); re-asking in 90s before calling anyone
2026-09-11T15:55:29Z [sol_book_gate_review] read failed twice (unable to open database file); alert DELIVERED=True
  ✅ перед звонком перепросили через 90 с
  ✅ одна тревога «не может прочитать»
2026-09-11T15:55:29Z [sol_book_gate_review] read failed (unable to open database file); re-asking in 0s before calling anyone
2026-09-11T15:55:29Z [sol_book_gate_review] read still failing (unable to open database file); already alerted this outage
  ✅ та же поломка — второй тревоги нет
2026-09-11T15:55:29Z [sol_book_gate_review] n=5/200 LONG 0/5 SHORT 0/0 ratio=n/a fired_ever=[] looks_done=[] new=[]
  ✅ после хорошего чтения поломка снята
2026-09-11T15:55:29Z [sol_book_gate_review] read failed (unable to open database file); re-asking in 0s before calling anyone
2026-09-11T15:55:29Z [sol_book_gate_review] read failed twice (unable to open database file); alert DELIVERED=True
  ✅ новая поломка — снова тревога

── 11. БОЕВОЙ ПУТЬ ПОМЕЧЕН КАК АЛЕРТ; КОНТРАКТ В СЕТЬ НЕ ХОДИТ ──────────
  ✅ вызов send_full_report(text, require_link=False) на месте
  ✅ run() не имеет отправителя по умолчанию (тест не может дойти до Telegram)
  ✅ импорт отправителя без записи байткода в дерево Титана

✅ ВСЕ ПРОВЕРКИ ЗЕЛЁНЫЕ
```

## 6. The canon — `OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11`

- **It is a documentation file,** and nothing opens it. In the SOL tree, only `config.py` mentions it, and only in comments.
- **Backup,** outside both trees: `/root/backups/OPEN-ITEMS-SOL.md.bak_optionE_20260911T1555Z`.
- **Ownership** is unchanged: `root:root 644`.
- **Four edits:**
  - the 15:32 heading is marked **⚰️ SUPERSEDED 15:55 BY OPTION E**, with a line saying it is kept as written, as the 06:12 one is;
  - the new subsection **"RE-REGISTERED 2026-09-11 15:55 — OPTION E …"** — the operator's call after reading 1550 §4, the thresholds unchanged, when each wire is read, the false-alarm and power tables beside the old figures, the accepted cost, the collapse and the overflow;
  - the REVIEW-REMINDER bullet now carries option E;
  - the "current figures" line now reads 16.5 % and 23.9 %.

```diff
--- /root/backups/OPEN-ITEMS-SOL.md.bak_optionE_20260911T1555Z	2026-09-11 15:34:59.348214912 +0000
+++ /mnt/volume_nyc1_1780480650620/mercury-sol/OPEN-ITEMS-SOL.md	2026-09-11 15:58:24.343063686 +0000
@@ -51,7 +51,9 @@
 
 **Above 5 % on either side, or a side ratio above 2× → a finding about the calibration, and grounds to revisit: re-cut the ruler per side and say so. Never loosen quietly.**
 
-### 🔴 RE-REGISTERED 2026-09-11 15:32 — THE WIRES' ARMING MOVED; THEIR THRESHOLDS DID NOT
+### ⚰️ SUPERSEDED 15:55 BY OPTION E (next subsection) — RE-REGISTERED 2026-09-11 15:32 — THE WIRES' ARMING MOVED; THEIR THRESHOLDS DID NOT
+
+*Kept as written, as the 06:12 one is. Its arming — the side wires on every pass from n ≥ 100, and the ratio at the review point — is no longer live. Its measurements are the reason for the re-registration below.*
 
 **This is a re-registration, and it is recorded as one.** **The operator made this call after reading report 2026-09-11-0635 §6.** Built in workspace commit `0c58364` (`scripts/sol_book_gate_review.py` and its contract); no bot file changed and nothing restarted. Record: `kola-reports/reports/2026-09-11-1550-mercury-sol-book-gate-wires-re-armed.md`.
 
@@ -92,6 +94,80 @@
   - **F.** Test the side wires at the review point only, and the ratio at 2026-10-11 → 16.5 % and 23.4 %.
 - **The alert carries its own current false-alarm rate.** The line "FALSE-ALARM RATE OF THESE WIRES … 44.5 % … 37.3 % … 60.2 %" replaces the ≈ 85 % line. The contract recomputes these figures exactly from the script's constants, so the text cannot drift from the code.
 
+### 🔴 RE-REGISTERED 2026-09-11 15:55 — OPTION E: THE WIRES ARE READ AT TWO FIXED LOOKS. THE SECOND AND FINAL RE-REGISTRATION OF THEIR ARMING. THE THRESHOLDS DID NOT MOVE.
+
+**This is a re-registration, not a loosening.** **The operator made this call after reading report 2026-09-11-1550 §4, on its measured numbers, not on taste.**
+- **Live** since 15:55:26 UTC, in workspace commit `513eb13` (`scripts/sol_book_gate_review.py` and its contract).
+- **No bot file changed, and nothing was restarted.**
+- **Record:** `kola-reports/reports/2026-09-11-1610-mercury-sol-book-gate-option-e-applied.md`.
+
+**The thresholds are unchanged.** A side wire trips above 5 %, and the ratio wire above 2×. Both are compared in integers, so exactly 5 % or exactly 2× does not fire. The arming n's are unchanged too: a side wire needs n ≥ 100 on that side, and the ratio needs both sides at n ≥ 50.
+
+**Only WHEN they may be read moved:**
+
+| wire | 06:12 (first build) | 15:32 (superseded above) | **15:55 — option E (live)** |
+|---|---|---|---|
+| side wire | every pass, n ≥ 50 | every pass, n ≥ 100 | **two fixed looks only: the review-point pass and the first pass on 2026-10-11**, n ≥ 100 |
+| ratio wire | every pass, both sides n ≥ 50 | once, at the review point | **once, at the 2026-10-11 look**, both sides n ≥ 50 |
+
+**Why — the operator's reasoning, on the numbers in 1550 §4:**
+- Read at about 100 per side, the ratio fires from noise 37.3 % of the time and catches the 08-14 breach (5.67×) 79.9 % of the time.
+- Read at about 540 per side, it fires from noise 8.9 % of the time and catches that breach 98.1 % of the time.
+- **Reading it later is strictly better on both axes:** fewer false alarms and more true ones.
+- Once armed, the side wires re-accumulated (LONG went from 11.7 % to 30.9 % by 540). Two fixed looks remove that.
+
+| false alarm from noise, registered rates true | 06:12 | 15:32 | **E (live)** |
+|---|---|---|---|
+| any wire, by the review point (≈ 100 per side) | 84.7 % | 44.5 % | **16.5 %** |
+| any wire, by 2026-10-11 (≈ 540 per side) | 93.2 % | 60.2 % | **23.9 %** |
+| the ratio wire alone, at its reading | 48.4 % (n = 50, then every pass) | 37.3 % (n = 100) | **8.9 %** (n = 540) |
+| between the looks | — | — | **nothing is read** |
+
+- **The E figures are exact,** by enumeration over the two looks. The 1550 joint dynamic programming gives the same 16.51 % and 23.86 %.
+- **The 0635 Monte C., with the same seed and method** (40,000 paths, seed 20260911), gives 16.2 % and 23.6 %. The four RNG variants range from 16.2 % to 16.6 %, and from 23.5 % to 23.9 %.
+- **At today's faster pace** — about 1,080 per side by 2026-10-11 — the figure by 2026-10-11 is 18.7 %.
+
+**Power at E's looks** — one look each, binomial. This is what E catches if the truth is NOT the registration:
+
+| the truth | at the review point (100 per side) | at 2026-10-11 (540 per side) | the 15:32 arming, for comparison |
+|---|---|---|---|
+| a side at 7 % | 70.9 % | 96.4 % (97.5 % at either look) | — |
+| a side at 10 % | 94.2 % | ≈ 100 % | — |
+| a 2.5× split (5.0 % / 2.0 %) | not read | **72.8 %** | 59.3 %, at the review |
+| the 08-14 breach, 5.67× (3.53 % / 0.62 %) | not read | **98.1 %** | 79.9 %, at the review |
+
+🔴 **THE COST, ACCEPTED BY THE OPERATOR AND WRITTEN DOWN HERE:**
+- A side breach that appears between the two looks waits for the next look, instead of ringing within 30 minutes.
+- The ratio is no longer read at the first review at all — only on 2026-10-11.
+- The review point remains the registered test. This whole mechanism exists because nobody read it.
+
+**If the review point itself falls on 2026-10-11, the two looks collapse into ONE pass.** That happens with fewer than 200 evaluations by then, which means below 3.4 per side per day. In that pass:
+- one alert goes out, and the review point fires by the date;
+- each side wire is read once, at that pass's counts, and only for a side at n ≥ 100;
+- the ratio is read once, if both sides are at n ≥ 50;
+- both looks are recorded with the same time;
+- after it, no wire is ever read again.
+
+At such low n the ratio carries its binomial noise: 48.4 % at 50 per side, 42.2 % at 75 and 37.5 % at 99. The alert prints it as "Noise at this n". The contract pins this case.
+
+**How each look happens exactly once:**
+- The review look is the pass in which `review_point` fires.
+- The date look is recorded in the state file's `looks` map.
+- A failed send records no look, so the next pass re-reads it. A look is never skipped and never read twice.
+
+**Found and fixed on this path — an overflow in the alert's noise line.**
+- The line computed binomials with `float(comb(n, k))`, which overflows at n ≥ 1,030 per side.
+- From that n on, every alert raised `OverflowError`, and the cron pass died before sending. The defect was present from the 06:12 build.
+- At today's pace, the 2026-10-11 look lands near that n.
+- It is now computed in log space, and the contract sends an alert at 1,100 per side.
+
+**The alert carries all of it:**
+- a WHEN-THEY-ARE-READ line, with the accepted cost and the collapse;
+- the FALSE-ALARM RATE line — 16.5 %, 23.9 % and 8.9 %, with 44.5 % / 60.2 % and 85 % / 93 % named as old;
+- a POWER line.
+
+The contract recomputes every one of these figures from the script's constants.
+
 ### 🔴 §BOOK-GATE-REVIEW-MISSED — NAMED FAILURE, 2026-08-20 23:30:02 UTC
 
 The 08-14 re-registration set a review point of "200 further gate evaluations, or 2026-09-14". **The 200th evaluation came on 2026-08-20 23:30:02. At that moment LONG was 9/117 = 7.69 % (above 5 %), SHORT 3/83 = 3.61 %, and the side ratio 2.13× (above 2×). Both wires had tripped. Nobody checked for three weeks.** The 2026-09-01 report's "1.03×" pooled refusals from before and after the re-cut against pre-gate denominators; it was not a test of the live floors. The breach was found only on 2026-09-11 (report 0526), at 962 evaluations and 5.67×. **The operator recorded it as their own failure. The mechanism that should have caught it did not exist: the review depended on someone remembering.**
@@ -107,8 +183,12 @@
   - It runs the §5b query verbatim, with `mode=ro` and SELECTs only.
   - The review point fires once, at n ≥ 200 or 2026-10-11, whichever comes first.
   - ~~The wires fire immediately: a side at n ≥ 50 and above 5 %, or both sides at n ≥ 50 and a ratio above 2×.~~ **Re-registered 15:32, commit `0c58364` (see the section above):**
-    - a side wire fires immediately at **n ≥ 100** on that side and above 5 %;
-    - the ratio wire is tested **once, in the review-point pass**, with both sides at n ≥ 50 and a ratio above 2×.
+    - ~~a side wire fires immediately at **n ≥ 100** on that side and above 5 %;~~
+    - ~~the ratio wire is tested **once, in the review-point pass**, with both sides at n ≥ 50 and a ratio above 2×.~~
+    - **Re-registered again at 15:55 — option E, commit `513eb13`:**
+      - the side wires are read at **two fixed looks**, the review-point pass and the first pass on 2026-10-11, at n ≥ 100 and above 5 %;
+      - the ratio is read **once, at the 2026-10-11 look**, with both sides at n ≥ 50 and above 2×;
+      - nothing is read between the looks.
 
     The comparisons are integer, so exactly 5 % or exactly 2× does not fire.
   - Each alert carries n and refusals per side, the rates, the ratio, the registered 3.33 % / 2.70 % / 1.23×, and the §5a false-alarm line. It goes out through `send_full_report(text, require_link=False)`.
@@ -119,7 +199,7 @@
   - It fires on a synthetic 200th row, on a side breach and on a ratio breach.
   - It stays silent at 199, at n = 49, at exactly 5 % and exactly 2×, and after firing.
   - Mutation-checked. It also goes red when the live floors move: 🔴 **the next re-cut must re-point `ANCHOR`, `EXPECTED` and `PINNED_FLOORS` in the script.**
-- ⚰️ **SUPERSEDED 15:32 — these are the FIRST arming's figures, kept as the reason for the re-registration above.** Current figures: 0 % before the review point, 44.5 % at it, 60.2 % by 2026-10-11.
+- ⚰️ **SUPERSEDED 15:32 — these are the FIRST arming's figures, kept as the reason for the re-registration above.** Current figures, option E (15:55): 16.5 % by the review point and 23.9 % by 2026-10-11. The 15:32 figures (44.5 % and 60.2 %) are superseded too.
 - 🔴 **Read this before acting on a ratio alert (first arming, 06:12–15:32).** If the registered rates are true, the ratio wire as specified fires by noise alone **48 % of the time at n = 50 per side**, 37 % at 100 and 25 % at 200 (binomial). **Over the whole path** — armed from n = 50 and re-checked every 30 min — noise alone trips at least one wire before the first review with **≈ 85 %** probability, and by 2026-10-11 with **≈ 93 %** (Monte C., registered rates true; the alert says so, commit `68a0298`). At small n, a ratio alert is a prompt to look, not a finding. The thresholds were built verbatim; this is recorded, not changed.
 - **Live at install:** n = 2/200 (LONG 0/0, SHORT 0/2), nothing due.
 
```

## 7. Neither bot touched — and the usual

```
=== at 2026-09-11 16:00:33 UTC — baseline taken 15:44:36, before any change
--- sol tree: baseline 351 files, now 351
   changed: /mnt/volume_nyc1_1780480650620/mercury-sol/OPEN-ITEMS-SOL.md
   changed: /mnt/volume_nyc1_1780480650620/mercury-sol/oi_cache.json
   changed: /mnt/volume_nyc1_1780480650620/mercury-sol/trades.db
--- titan tree: baseline 208 files, now 208
   changed: /root/titan-bot/healthcheck_state.json
   changed: /root/titan-bot/oi_cache.json
   changed: /root/titan-bot/trades.db
--- writers of the changed runtime files
   /mnt/volume_nyc1_1780480650620/mercury-sol/trades.db held open by PIDs: 1181897 1181966 
   /root/titan-bot/trades.db held open by PIDs: 961100 961118 
   2026-09-11 16:00:18.643206714 +0000 /mnt/volume_nyc1_1780480650620/mercury-sol/oi_cache.json
   2026-09-11 16:00:29.925321911 +0000 /root/titan-bot/oi_cache.json
   2026-09-11 15:59:36.750782510 +0000 /root/titan-bot/healthcheck_state.json
   healthcheck.timer last: Fri 2026-09-11 15:59:32 UTC
   Titan git status --short -- titan-bot: 0 lines
   Titan sender bytecode: 2026-08-04 19:39:21.500503140 +0000 /root/titan-bot/__pycache__/full_report.cpython-312.pyc
--- canon: root:root 644 · code that mentions it (non-comment): 0

=== services (MainPID · NRestarts · active since)
before (15:44):
   1181897 0 Fri 2026-09-11 05:40:08 UTC  mercury-sol
   961100 0 Thu 2026-09-10 14:36:20 UTC  titan
   3521920 0 Sat 2026-08-08 15:37:06 UTC  mercury-sol-optimizer-listener
after:
   1181897 0 Fri 2026-09-11 05:40:08 UTC  mercury-sol
   961100 0 Thu 2026-09-10 14:36:20 UTC  titan
   3521920 0 Sat 2026-08-08 15:37:06 UTC  mercury-sol-optimizer-listener

=== crontab -l
   lines: 76 before, 76 after
   sha256 before: 9ccbbf26d503989e6b6bea05a047eaf9ea54c73f41e79c21d96f9e820775e3d6
   sha256 after:  9ccbbf26d503989e6b6bea05a047eaf9ea54c73f41e79c21d96f9e820775e3d6
   cmp: BYTE-IDENTICAL
   the line (grep -c → 1):
   */30 * * * * /usr/bin/timeout 300 /usr/bin/python3 /home/botuser/.openclaw/workspace/scripts/sol_book_gate_review.py >> /home/botuser/.openclaw/workspace/.kola_state/sol_book_gate_review.log 2>&1

=== --selftest under an empty env -i (installed script b192c4627998dab0)
   db: OK mode=ro · LONG 0/14 · SHORT 0/16 · due now: []
   config floors: {'LONG': 0.4214, 'SHORT': 0.3975} · pinned {'LONG': 0.4214, 'SHORT': 0.3975} · match=True
   state: /home/botuser/.openclaw/workspace/.kola_state/sol_book_gate_review.json · dir writable=True
   sender: OK (full_report imported, token and chat id present; nothing sent)
   SELFTEST OK
   EXIT=0

=== the live counter
   state: {"fired":{},"last_counts":{"LONG":[14,0],"SHORT":[15,0]},"last_run":"2026-09-1116:00:03","looks":{}}
   2026-09-11T15:00:03Z [sol_book_gate_review] n=28/200 LONG 0/14 SHORT 0/14 ratio=n/a fired_ever=[] new=[]
   2026-09-11T15:30:03Z [sol_book_gate_review] n=28/200 LONG 0/14 SHORT 0/14 ratio=n/a fired_ever=[] new=[]
   2026-09-11T16:00:04Z [sol_book_gate_review] n=29/200 LONG 0/14 SHORT 0/15 ratio=n/a fired_ever=[] looks_done=[] new=[]

=== workspace suite, as botuser (whoami → botuser)
   ✅ test_sol_book_gate_review_fires.py
   ИТОГО В НАБОРЕ: 267/267 зелёных за 45с (по 8 разом); медленные: test_act_performs_the_prescribed_remedy.py (12с), test_bo
   ✅ ВСЕ КОНТРАКТЫ ЗЕЛЁНЫЕ

=== commit (neutral: no protected path, 0 added lines match TRADING_REACH — no token, no BLOCK; commit_gate_pass.log has no new line)
   513eb13 feat(sol): OPTION E — the book-gate wires are read at two fixed looks; the ratio once, at 2026-10-11. Thresholds unchanged.
    scripts/sol_book_gate_review.py          | 158 ++++++++-----
    tests/test_sol_book_gate_review_fires.py | 369 +++++++++++++++++++++----------
    2 files changed, 357 insertions(+), 170 deletions(-)
   commit_gate_pass.log last line: 2026-09-11T06:12:02Z	AUTHORISED	scripts/sol_book_gate_review.py,tests/test_sol_book_gate_review_fires.py

=== openitems_guard, after
   openitems_guard — canon: /mnt/volume_nyc1_1780480650620/kola-reports/reports/OPEN-ITEMS.md
     titan-bot HEAD : cd0f175   <- the SUBJECT, this is what is compared
     repo HEAD      : cd0f175   (context only, NOT compared)
     watched values : 14
   
   ✅ header and current-state table agree with runtime.
   EXIT=0
```

## 8. What stays open, named

- **A wire alert is still a prompt to look, not a finding.** By 2026-10-11, one path in four (23.9 %) trips a wire from noise alone. That is far better than 93 %, and it is still not zero; the alert says so.
- **The accepted cost is live.** A side breach that appears between the review point and 2026-10-11 is not rung until 2026-10-11.
- **Nothing watches the watcher,** unchanged since 0635. If the cron line goes, the counter falls silent without an alert. Under E this matters more: the whole second look is **one pass** on 2026-10-11.
- **The pace assumption.** The figures use 540 per side on 2026-10-11, the 0635 method. At today's pace the date look lands near 1,080 per side, where the noise is lower (18.7 %) and the power higher. The overflow that would have killed it there is fixed (§4).

## Verification

- **Pre-flight:** `openitems_guard` returned EXIT=0 (15:44) before anything else. The baseline (both trees, three services, crontab) was taken before any change.
- **Changed, in the workspace, outside both trees:**
  - `scripts/sol_book_gate_review.py` and `tests/test_sol_book_gate_review_fires.py`, in commit `513eb13`;
  - installed atomically at 15:55:26 UTC, keeping `botuser:botuser` and modes 755 / 644.
- **Contract:** 117/117 green. All 87 earlier checks are accounted for. Each mutant turns it red: 7, 21 and 1 checks. Suite 267/267 as botuser.
- **Re-measured, exactly (three ways) and by the same-seed Monte C.:** 16.5 % and 23.9 % are confirmed. Power is stated, and the alert carries both.
- **The collapse** is defined and pinned. **The overflow** is proven on `0c58364` and fixed.
- **Canon:** the second dated re-registration is in place, and the 15:32 subsection is superseded and kept. The backup is outside both trees.
- **Bots:** see §7.

## Appendix A — the script diff, `0c58364` → `513eb13`

```diff
diff --git a/scripts/sol_book_gate_review.py b/scripts/sol_book_gate_review.py
index 748d7a0..2156ce5 100755
--- a/scripts/sol_book_gate_review.py
+++ b/scripts/sol_book_gate_review.py
@@ -9,24 +9,28 @@ of 2.13× — BOTH pre-registered wires already tripped — and nobody checked f
 The mechanism that should have caught it did not exist: the review depended on someone
 remembering. This script is that mechanism.
 
-WHAT IT DOES — report 2026-09-11-0550 §5b, option 1, as re-registered 2026-09-11:
+WHAT IT DOES — report 2026-09-11-0550 §5b, option 1, as re-registered 2026-09-11 (option E):
   * reads SOL trades.db with mode=ro and runs the §5b SELECT, nothing else;
   * alerts ONCE at the review point: n_LONG + n_SHORT >= 200, or the UTC date reaches
     2026-10-11 — whichever comes first;
-  * alerts IMMEDIATELY on a side wire: a side with n >= 100 and a rate above 5 %;
-  * tests the RATIO wire ONCE, in the review-point pass: both sides with n >= 50 and a side
-    ratio above 2× — never on the passes in between;
+  * reads the SIDE wires at TWO fixed looks only — the review-point pass and the first pass
+    on 2026-10-11 — a side with n >= 100 and a rate above 5 %;
+  * reads the RATIO wire ONCE, at the 2026-10-11 look: both sides with n >= 50 and a side
+    ratio above 2×;
+  * between the looks nothing is read: a side breach there waits for the next look;
+  * if the review point itself falls on 2026-10-11 (fewer than 200 evaluations by then), the
+    two looks are ONE pass: one alert, each wire read once, at that pass's counts;
   * each condition fires exactly once — state in .kola_state/sol_book_gate_review.json;
   * alerts go through send_full_report(text, require_link=False): alerts, not reports.
 
-🔴 RE-REGISTERED 2026-09-11 by the operator, after report 0635 §6 — the ARMING moved, the
-thresholds did not. As first built (§5b verbatim) the side wires armed at n >= 50 and the
-ratio wire was checked on every 30-min pass. With the registered rates TRUE, the ratio wire
-at n = 50 per side fires from noise 48.4 % of the time, and at least one wire tripped before
-the first review with ≈ 85 % probability. A bell that rings from noise that often is not a
-detector: it trains its reader to ignore it. Now: side wires arm at n >= 100 per side (5 %
-unchanged); the ratio (2× unchanged) is read at the review point only. Canon:
-OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11.
+🔴 RE-REGISTERED TWICE ON 2026-09-11 — the ARMING moved, the thresholds (5 %, 2×) never did.
+  06:12 as first built (§5b verbatim): side wires from n >= 50 and the ratio, every 30-min
+        pass. Noise alone tripped a wire by the first review ≈ 85 %, by 2026-10-11 ≈ 93 %.
+  15:32 (operator, after 0635 §6): side wires from n >= 100 every pass, the ratio once at the
+        review point. 44.5 % / 60.2 % — still above 40 %, recorded as not fixed.
+  now   (operator, after 1550 §4, option E): side wires at two fixed looks, the ratio once at
+        2026-10-11. 16.5 % by the review, 23.9 % by 2026-10-11 (exact).
+Canon: OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11.
 
 RUNS AS ROOT, not botuser as §5b wrote it: /root is 0700, so botuser can read neither
 /root/titan-bot/full_report.py nor its .env — the very sender §5b names. Same reason
@@ -52,7 +56,7 @@ import sys
 import time
 import urllib.parse
 from datetime import datetime, timezone
-from math import comb
+from math import exp, lgamma, log, log1p
 
 SOL_DIR = "/mnt/volume_nyc1_1780480650620/mercury-sol"
 DB = os.path.join(SOL_DIR, "trades.db")
@@ -64,10 +68,15 @@ SENDER_DIR = "/root/titan-bot"
 ANCHOR = "2026-09-11 05:40:08"
 REVIEW_N = 200
 REVIEW_DATE = "2026-10-11"
-SIDE_WIRE_MIN_N = 100  # a side wire arms at n >= 100 on that side (re-registered 09-11; was 50)
-RATIO_MIN_N = 50       # the ratio, read at the review point, needs both sides at n >= 50
+SIDE_WIRE_MIN_N = 100  # a side wire reads only a side with n >= 100 (re-registered 09-11 15:32)
+RATIO_MIN_N = 50       # the ratio needs both sides at n >= 50 (unchanged)
 WIRE_RATE_PCT = 5      # a side above 5 %
 WIRE_RATIO = 2         # a side ratio above 2×
+# WHEN the wires are read (re-registered 09-11, option E): two fixed looks, not every pass.
+LOOK_REVIEW = "review_point"   # the pass in which review_point fires
+LOOK_DATE = REVIEW_DATE        # the first pass on or after 2026-10-11
+SIDE_LOOKS = (LOOK_REVIEW, LOOK_DATE)
+RATIO_LOOKS = (LOOK_DATE,)
 EXPECTED = {"LONG": 0.0333, "SHORT": 0.0270}
 EXPECTED_RATIO = 1.23
 PINNED_FLOORS = {"LONG": 0.4214, "SHORT": 0.3975}
@@ -132,7 +141,10 @@ def ratio_value(counts):
 
 # ── noise, for the reader of the alert (binomial, registered rates assumed true) ──────────
 def _pmf(n, p):
-    return [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
+    """Binomial pmf, in log space: comb(n, k) as a float overflows beyond n ≈ 1030 per side, and
+    then no alert could be formatted — exactly where the 2026-10-11 look can land at this pace."""
+    lp, lq, top = log(p), log1p(-p), lgamma(n + 1)
+    return [exp(top - lgamma(k + 1) - lgamma(n - k + 1) + k * lp + (n - k) * lq) for k in range(n + 1)]
 
 
 def p_rate_above(n, p):
@@ -152,28 +164,56 @@ def p_ratio_above(nl, ns):
 
 
 # ── what is due ─────────────────────────────────────────────────────────────────────────
-def due_conditions(counts, now, fired=()):
-    """{key: reason} of every condition true right now (fired-once filtering is the caller's).
-
-    The ratio wire is tested ONLY in the review-point pass — the pass in which review_point is
-    due and not yet in `fired` (re-registered 09-11). A failed send marks nothing, so the retry
-    is still the review-point pass and tests the ratio again."""
-    out = {}
+def review_reason(counts, now):
+    """Why the review point is due right now, or None."""
     total = counts["LONG"][0] + counts["SHORT"][0]
     if total >= REVIEW_N:
-        out["review_point"] = f"REVIEW POINT REACHED: {total} evaluations (>= {REVIEW_N})"
-    elif now.strftime("%Y-%m-%d") >= REVIEW_DATE:
-        out["review_point"] = (f"REVIEW POINT REACHED: the date is {REVIEW_DATE} "
-                               f"({total} evaluations, below {REVIEW_N})")
-    for s in SIDES:
-        n, r = counts[s]
-        if rate_breached(n, r):
-            out[f"wire_rate_{s}"] = (f"WIRE TRIPPED: {s} {r}/{n} = {_pct(r / n)} is above "
-                                     f"{WIRE_RATE_PCT} % at n {n} >= {SIDE_WIRE_MIN_N}")
-    if "review_point" in out and "review_point" not in fired and ratio_breached(counts):
+        return f"REVIEW POINT REACHED: {total} evaluations (>= {REVIEW_N})"
+    if now.strftime("%Y-%m-%d") >= REVIEW_DATE:
+        return f"REVIEW POINT REACHED: the date is {REVIEW_DATE} ({total} evaluations, below {REVIEW_N})"
+    return None
+
+
+def open_looks(counts, now, fired=(), looks=()):
+    """The looks this pass IS (option E, re-registered 09-11).
+
+    The review look is the pass in which review_point is due and not yet in `fired`; the date
+    look is the first pass on or after 2026-10-11 not yet in `looks`. A failed send records
+    nothing, so the retry is still the same look. When the review point itself falls on
+    2026-10-11, both are open in the same pass: ONE pass, each wire read once."""
+    out = []
+    if review_reason(counts, now) and "review_point" not in fired:
+        out.append(LOOK_REVIEW)
+    if now.strftime("%Y-%m-%d") >= REVIEW_DATE and LOOK_DATE not in looks:
+        out.append(LOOK_DATE)
+    return out
+
+
+def _read_at(now_looks):
+    if len(now_looks) == 2:
+        return f"read at the review point, which falls on {REVIEW_DATE} (both looks in one pass)"
+    return "read at the review point" if now_looks == [LOOK_REVIEW] else f"read at the {REVIEW_DATE} look"
+
+
+def due_conditions(counts, now, fired=(), looks=()):
+    """{key: reason} of every condition true right now (fired-once filtering is the caller's).
+    The side wires are read only in a look listed in SIDE_LOOKS, the ratio only in RATIO_LOOKS."""
+    out = {}
+    reason = review_reason(counts, now)
+    if reason:
+        out["review_point"] = reason
+    now_looks = open_looks(counts, now, fired, looks)
+    at = _read_at(now_looks)
+    if any(lk in now_looks for lk in SIDE_LOOKS):
+        for s in SIDES:
+            n, r = counts[s]
+            if rate_breached(n, r):
+                out[f"wire_rate_{s}"] = (f"WIRE TRIPPED: {s} {r}/{n} = {_pct(r / n)} is above "
+                                         f"{WIRE_RATE_PCT} % at n {n} >= {SIDE_WIRE_MIN_N}, {at}")
+    if any(lk in now_looks for lk in RATIO_LOOKS) and ratio_breached(counts):
         x, side = ratio_value(counts)
         out["wire_ratio"] = (f"WIRE TRIPPED: side ratio {_x(x)} ({side} higher) is above "
-                             f"{WIRE_RATIO}× at the review point, both sides at n >= {RATIO_MIN_N}")
+                             f"{WIRE_RATIO}×, {at}, both sides at n >= {RATIO_MIN_N}")
     return out
 
 
@@ -237,23 +277,27 @@ def format_alert(reasons, counts, now):
         ratio_line,
         "Wires (pre-registered 09-11, thresholds unchanged): above 5 % on a side, or a side ratio "
         "above 2× → re-cut the ruler per side and say so. Never loosen quietly.",
-        "ARMING (re-registered 09-11 by the operator after report 0635 §6): a side wire arms at "
-        "n >= 100 on that side and is checked every 30 min; the ratio wire is tested once, at the "
-        "review point, not continuously.",
+        "WHEN THEY ARE READ (re-registered 09-11 by the operator, after report 1550 §4, option E): "
+        "the side wires at two fixed looks only, the review point and 2026-10-11, each side at "
+        "n >= 100; the ratio once, at 2026-10-11, both sides at n >= 50. Between the looks nothing "
+        "is read: a side breach there waits for the next look (cost accepted). If the review point "
+        "itself falls on 2026-10-11, the two looks are one pass.",
         "FALSE-ALARM LINE (0550 §5a): if the registered rates are true, the chance of a false "
         "alarm at the first review, about 100 per side, is LONG 11.7 %, SHORT 5.4 %. A LONG "
         "reading between 5 % and 6 % at the first review is within noise. Nobody re-cuts on "
         "that without reading this line.",
-        # False-alarm rate OF THIS ARMING — exact (dynamic programming), registered rates true,
-        # n equal per side, every armed wire checked at every evaluation, 2026-10-11 ≈ 540 per
-        # side. The 0635 §6 Monte C. re-run for this arming (40 000 paths, seed 20260911)
-        # gives 44.3 % / 60.3 %. The contract recomputes these from the constants above.
-        "FALSE-ALARM RATE OF THESE WIRES (registered rates true): below n = 100 on a side "
-        "nothing fires from that side, and the ratio is not read before the review point; at the "
-        "review point, about 100 per side, noise alone trips at least one wire 44.5 % of the "
-        "time — the ratio wire alone 37.3 % — and by 2026-10-11 60.2 %. Under the first "
-        "arming (n >= 50, every pass) it was 85 % by the first review and 93 % by 2026-10-11. "
-        "A wire alert is a prompt to look, not a finding.",
+        # False-alarm rate and power OF THIS ARMING — exact, registered rates true, n equal per
+        # side; the review look at 100 per side, the 2026-10-11 look at ≈ 540 per side (0635 §6
+        # pace). The 0635 Monte C. re-run for option E (40 000 paths, seed 20260911) agrees.
+        # The contract recomputes every figure here from the constants above.
+        "FALSE-ALARM RATE OF THESE WIRES (registered rates true): at the review point, about 100 "
+        "per side, noise alone trips at least one wire 16.5 % of the time, and by 2026-10-11, "
+        "about 540 per side, 23.9 % — the ratio wire alone 8.9 %. Earlier armings, named as old: "
+        "44.5 % / 60.2 % (15:32 — the ratio at the review, the sides every pass) and 85 % / 93 % "
+        "(06:12 — n >= 50, every pass). A wire alert is a prompt to look, not a finding.",
+        "POWER AT THESE LOOKS: a true 7 % side rate is caught 70.9 % at the review point and "
+        "96.4 % at 2026-10-11; a true 2.5× split 72.8 % and the 08-14 breach (5.67×) 98.1 % at "
+        "2026-10-11.",
     ]
     if noise:
         lines.append(f"Noise at this n, registered rates assumed true: {' · '.join(noise)}.")
@@ -299,6 +343,7 @@ def load_state(path):
             pass
         st = {}
     st.setdefault("fired", {})
+    st.setdefault("looks", {})
     return st
 
 
@@ -317,7 +362,7 @@ def run(db, state_path, send, now=None, config_path=SOL_CONFIG,
     Telegram by forgetting to pass one. Returns (exit_code, [keys fired this pass])."""
     now = now or datetime.now(timezone.utc)
     st = load_state(state_path)
-    fired = st["fired"]
+    fired, looks = st["fired"], st["looks"]
     stamp = now.strftime("%Y-%m-%d %H:%M:%S")
 
     try:
@@ -339,19 +384,23 @@ def run(db, state_path, send, now=None, config_path=SOL_CONFIG,
             return 1, (["reader_broken"] if ok else [])
     st.pop("reader_broken", None)
 
-    new = {k: v for k, v in due_conditions(counts, now, fired).items() if k not in fired}
-    out, code = [], 0
+    now_looks = open_looks(counts, now, fired, looks)
+    new = {k: v for k, v in due_conditions(counts, now, fired, looks).items() if k not in fired}
+    out, code, delivered = [], 0, True
     if new:
         text = format_alert(list(new.values()), counts, now)
-        ok = bool(send(text))
-        if ok:
+        delivered = bool(send(text))
+        if delivered:
             for k, v in new.items():
                 fired[k] = {"at": stamp, "reason": v,
                             "counts": {s: list(counts[s]) for s in SIDES}}
             out += list(new)
         else:
             code = 1   # not marked: the next pass retries
-        _log(f"due={list(new)} DELIVERED={ok}")
+        _log(f"due={list(new)} DELIVERED={delivered}")
+    if delivered:      # a look is done once its alert (if any) has left; else the retry re-reads it
+        for lk in now_looks:
+            looks.setdefault(lk, {"at": stamp, "counts": {s: list(counts[s]) for s in SIDES}})
 
     floors = floors_in_config(config_path)
     if floors is not None and floors != PINNED_FLOORS:
@@ -371,7 +420,8 @@ def run(db, state_path, send, now=None, config_path=SOL_CONFIG,
     st["last_counts"] = {s: list(counts[s]) for s in SIDES}
     save_state(state_path, st)
     _log(f"n={nl + ns}/{REVIEW_N} LONG {rl}/{nl} SHORT {rs}/{ns} "
-         f"ratio={'n/a' if x is None else _x(x)} fired_ever={sorted(fired)} new={out}")
+         f"ratio={'n/a' if x is None else _x(x)} fired_ever={sorted(fired)} "
+         f"looks_done={sorted(looks)} new={out}")
     return code, out
 
 
```

## Appendix B — the computations, as run

`mc_e.py` is option E under the 0635 method. It imports `mc.py`, which is printed in full in report 1550, Appendix B.

```python
"""Option E under the 0635 §6 method: 40 000 paths, seed 20260911, registered rates true,
n equal per side. Side wires read at 100/side (the review look) and 540/side (2026-10-11 look);
the ratio read once, at 540/side."""
import sys
import numpy as np
import mc
for v in ("rng_random", "rng_binomial", "legacy_rand", "rng_random_interleaved"):
    L, S = mc.draw(v)
    lh, sh, qh = mc.wires(L, S)
    r1 = lh[:, 99] | sh[:, 99]
    r2 = lh[:, 539] | sh[:, 539] | qh[:, 539]
    print(f"[{v}] E: by review {r1.mean()*100:.2f} % · by 2026-10-11 {(r1 | r2).mean()*100:.2f} %"
          f" · LONG@100 {lh[:,99].mean()*100:.2f} SHORT@100 {sh[:,99].mean()*100:.2f}"
          f" · LONG@540 {lh[:,539].mean()*100:.2f} SHORT@540 {sh[:,539].mean()*100:.2f} ratio@540 {qh[:,539].mean()*100:.2f}")
```

`exact_e.py` holds the exact figures for option E: the pace sensitivity, the collapse noise and the power.

```python
"""Exact figures for option E beyond the headline: pace sensitivity, collapse at low n, power."""
from math import comb, exp, lgamma, log, log1p
PL, PS = 0.0333, 0.0270
def pmf(n, p): return [exp(lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)+k*log(p)+(n-k)*log1p(-p)) for k in range(n+1)]
def ratio_hit(a, b): return a > 2*b or b > 2*a
def side_hit(a, n): return a*100 > 5*n
def e_exact(n1, n2, pl=PL, ps=PS, ratio_at_date=True):
    A1, B1 = pmf(n1, pl), pmf(n1, ps); TL, TS = pmf(n2-n1, pl), pmf(n2-n1, ps)
    cap = (5*n2)//100; q1 = q2 = 0.0
    for a1, pa in enumerate(A1):
        for b1, pb in enumerate(B1):
            if pa*pb < 1e-18 or side_hit(a1, n1) or side_hit(b1, n1): continue
            q1 += pa*pb; s = 0.0
            for a2 in range(a1, cap+1):
                for b2 in range(b1, cap+1):
                    if not (ratio_at_date and ratio_hit(a2, b2)): s += TL[a2-a1]*TS[b2-b1]
            q2 += pa*pb*s
    return 1-q1, 1-q2
def p_ratio(n, pl, ps):
    A, B = pmf(n, pl), pmf(n, ps)
    return sum(x*y for a, x in enumerate(A) if x > 1e-18 for b, y in enumerate(B) if y > 1e-18 and ratio_hit(a, b))
def p_side(n, p): return sum(v for k, v in enumerate(pmf(n, p)) if side_hit(k, n))
def side_two_looks(n1, n2, p):   # P(side trips at look 1 or look 2), one side alone
    A1, T = pmf(n1, p), pmf(n2-n1, p); cap = (5*n2)//100
    quiet = sum(pa * sum(T[a2-a1] for a2 in range(a1, cap+1)) for a1, pa in enumerate(A1) if not side_hit(a1, n1))
    return 1-quiet
r, d = e_exact(100, 540); print(f"E exact, date look at 540/side: by review {r*100:.2f} % · by 2026-10-11 {d*100:.2f} %")
r, d = e_exact(100, 1080); print(f"E exact, date look at 1080/side (today's pace): by review {r*100:.2f} % · by 2026-10-11 {d*100:.2f} %")
print(f"ratio alone at the date look: 540/side {p_ratio(540, PL, PS)*100:.2f} % · 1080/side {p_ratio(1080, PL, PS)*100:.2f} %")
print(f"side alone at the date look (one look): LONG@540 {p_side(540, PL)*100:.2f} % SHORT@540 {p_side(540, PS)*100:.2f} %")
print("collapse (review on the date at < 200 rows): the ratio, read once at low n, noise:")
for n in (50, 75, 99): print(f"   {n}/side: {p_ratio(n, PL, PS)*100:.2f} %")
print("POWER at E's looks:")
print(f"   side 7 %: review(100) {p_side(100, .07)*100:.2f} % · date(540) {p_side(540, .07)*100:.2f} % · either look {side_two_looks(100, 540, .07)*100:.2f} %")
print(f"   side 10 %: review(100) {p_side(100, .10)*100:.2f} % · either look {side_two_looks(100, 540, .10)*100:.2f} %")
print(f"   ratio 2.5x (5.0/2.0 %): at 540 {p_ratio(540, .05, .02)*100:.2f} %  (15:32 arming, at 100: {p_ratio(100, .05, .02)*100:.2f} %)")
print(f"   ratio 5.67x (3.53/0.62 %): at 540 {p_ratio(540, .0353, .0062)*100:.2f} %  (15:32 arming, at 100: {p_ratio(100, .0353, .0062)*100:.2f} %)")
```
