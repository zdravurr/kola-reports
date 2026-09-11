# Mercury-SOL book-gate wires re-armed

_2026-09-11 15:50 UTC_

---

**2026-09-11 15:50 UTC · the workspace only, OUTSIDE both bot trees · Mercury-SOL and Titan are both LIVE and were not touched · basis: report 2026-09-11-0635 §6 · a re-registration the operator ordered after reading §6**

## The answer first

1. **Done. The wires' arming moved; their thresholds did not.** One script changed, `scripts/sol_book_gate_review.py`, together with its contract, in workspace commit `0c58364`.
   - **Side wires** now arm at **n ≥ 100 per side** (it was 50). They still trip "above 5 %", and they are still checked on every 30-min pass.
   - **The ratio wire** is now **tested once, in the review-point pass** (it was checked on every pass). It still trips "above 2×", and it still needs both sides at n ≥ 50.
   - Unchanged: the query, the anchor, the pinned floors, the review point (200 or 2026-10-11), fire-once, and the stale-registration and unreadable-DB alerts.
2. 🔴 **NOT FIXED. The new false-alarm rate is still above 40 %.** With the registered rates TRUE:

   | noise alone trips at least one wire… | before | now |
   |---|---|---|
   | strictly before the review point | 84.5 % | **0 %** |
   | by the review point (≈ 100 per side) | 84.7 % | **44.5 %** (the ratio wire alone 37.3 %) |
   | by 2026-10-11 | 93.2 % | **60.2 %** |

   - These figures are exact, by dynamic programming.
   - The 0635 Monte C., re-run for the new arming with the same seed and method, gives **44.3 % and 60.3 %**.
   - The side wires moved just as your §6 figures said: LONG 23.2 % → 11.7 %, SHORT 15.2 % → 5.4 %.
3. **What still carries the noise, and what else would be needed** (§4). Measured, not built:
   - **The ratio.** Read at about 100 per side, it is noisy by its nature: **37.3 %**. At about 540 per side it would be 8.9 %.
   - **The side wires.** They are re-checked every pass once armed, so sequential looks pile up again. By 2026-10-11, LONG goes from 11.7 % to 30.9 % and SHORT from 5.4 % to 14.6 %.
   - **Option E** would give **16.5 % by the review and 23.9 % by 2026-10-11**. It tests the side wires at two fixed looks, the review point and 2026-10-11, and the ratio once, at 2026-10-11.
     - It still catches a true 7 % side rate 70.9 % of the time at n = 100, and 96.4 % at n = 540.
     - It would be a further re-registration, so it is your call.
4. **The alert carries its own current false-alarm rate.**
   - The ≈ 85 % line is gone. The new line states 44.5 %, 37.3 % and 60.2 %, and names 85 % and 93 % as the first arming's figures.
   - The contract recomputes these figures exactly from the script's constants, so the alert text cannot drift from the code.
5. **Contract: 87/87 as botuser (it was 59).**
   - It pins the behaviour change: silence at n = 50–99 above 5 % on both sides; the ratio silent mid-window (at 2.40×, at ∞, and at 3.96× with 199 rows) and present at the review point.
   - Each mutant turns it red: the one that arms the side wires at 50 fails 16 checks, and the one that evaluates the ratio every pass fails 7 (§3).
6. **Neither bot was touched.**
   - No bot file changed.
   - `NRestarts` stayed 0 → 0, with the same PIDs, on all three services.
   - The crontab is byte-identical: 76 lines, same sha256.
   - `openitems_guard` returned EXIT=0 before and after.
   - The workspace suite is 267/267 as botuser, and `--selftest` passes under `env -i`.
   - **The live counter is at n = 28/200 (LONG 0/14, SHORT 0/14). Nothing has fired.**
7. **The canon records the re-registration.** `OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11` has a new subsection, "RE-REGISTERED 2026-09-11 15:32 — THE WIRES' ARMING MOVED; THEIR THRESHOLDS DID NOT".
   - It says that you made this call after reading §6.
   - It says that the ratio wire is now a review-point test, not a continuous one.
   - It carries the new figures beside the old.

---

## 1. The change

| wire | as first built (0550 §5b verbatim, installed 06:12) | re-registered 15:32 (`0c58364`) |
|---|---|---|
| side wire | armed at n ≥ 50 on that side, checked every 30-min pass | armed at **n ≥ 100** on that side, still checked every 30-min pass |
| ratio wire | both sides n ≥ 50, checked **every 30-min pass** | **tested once, in the review-point pass**, both sides n ≥ 50 |
| thresholds | above 5 % · above 2× · integer comparisons | **unchanged** |

**In the code:**
- **Two constants instead of one.** `WIRE_MIN_N = 50` used to serve both wires. It is now `SIDE_WIRE_MIN_N = 100` for the side wires and `RATIO_MIN_N = 50` for the ratio, whose value is unchanged.
- **`due_conditions(counts, now, fired=())` evaluates the ratio only in the review-point pass.** That is the pass where `review_point` is due and not yet in `fired`.
  - A failed send marks nothing. The retry pass is therefore still the review-point pass, and it tests the ratio again; the contract pins this.
  - Once the review point has fired, the ratio is never read again. The ratio line stays in every alert as a reading, beside the side rates, as before.
- **The alert text changed in three places:**
  - the "Wires" line now says "thresholds unchanged";
  - a new ARMING line states when each wire may be read;
  - the SEQUENTIAL LOOKS ≈ 85 % line is replaced by a FALSE-ALARM RATE line (§2c).

**How it went live without a half-edited pass.**
- The new script and contract were written to a botuser-readable temp directory. The contract was run there, against the new script and against both mutants.
- Only then were both files installed with `install` + `mv` (atomic), at 15:31:22 UTC. That falls between the 15:30 and 16:00 cron passes.
- The 15:30 pass still ran the old script and logged `n=28/200 … new=[]`.
- The sha256 of the installed file equals the tested candidate (`6be299655d3d201e…`).

**Two alerts generated by the installed script** — synthetic counts, nothing sent:

**A — the review point at the 200th row, LONG 4/100 against SHORT 1/100: the ratio wire is read here, in the same alert**

```
[Mercury-SOL] BOOK-GATE REVIEW — ALERT
REVIEW POINT REACHED: 200 evaluations (>= 200)
WIRE TRIPPED: side ratio 4.00× (LONG higher) is above 2× at the review point, both sides at n >= 50
Counted since the 09-11 re-cut, 2026-09-11 05:40:08 UTC · now 2026-09-14 04:30 UTC · 200/200 evaluations
LONG 4/100 refused = 4.00 % · registered 3.33 %
SHORT 1/100 refused = 1.00 % · registered 2.70 %
Side ratio: 4.00× (LONG higher) · registered 1.23×
Wires (pre-registered 09-11, thresholds unchanged): above 5 % on a side, or a side ratio above 2× → re-cut the ruler per side and say so. Never loosen quietly.
ARMING (re-registered 09-11 by the operator after report 0635 §6): a side wire arms at n >= 100 on that side and is checked every 30 min; the ratio wire is tested once, at the review point, not continuously.
FALSE-ALARM LINE (0550 §5a): if the registered rates are true, the chance of a false alarm at the first review, about 100 per side, is LONG 11.7 %, SHORT 5.4 %. A LONG reading between 5 % and 6 % at the first review is within noise. Nobody re-cuts on that without reading this line.
FALSE-ALARM RATE OF THESE WIRES (registered rates true): below n = 100 on a side nothing fires from that side, and the ratio is not read before the review point; at the review point, about 100 per side, noise alone trips at least one wire 44.5 % of the time — the ratio wire alone 37.3 % — and by 2026-10-11 60.2 %. Under the first arming (n >= 50, every pass) it was 85 % by the first review and 93 % by 2026-10-11. A wire alert is a prompt to look, not a finding.
Noise at this n, registered rates assumed true: LONG above 5 % 11.73 % · SHORT above 5 % 5.42 % · ratio above 2× 37.33 %.
Canon: mercury-sol/OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11. Alert, not a report: each condition fires once (state .kola_state/sol_book_gate_review.json).
```

**B — a side wire mid-window, LONG 6/100 at 190 evaluations: it fires at once; the 2.70× ratio is shown as a reading, and NOT tested**

```
[Mercury-SOL] BOOK-GATE REVIEW — ALERT
WIRE TRIPPED: LONG 6/100 = 6.00 % is above 5 % at n 100 >= 100
Counted since the 09-11 re-cut, 2026-09-11 05:40:08 UTC · now 2026-09-13 22:00 UTC · 190/200 evaluations
LONG 6/100 refused = 6.00 % · registered 3.33 %
SHORT 2/90 refused = 2.22 % · registered 2.70 %
Side ratio: 2.70× (LONG higher) · registered 1.23×
Wires (pre-registered 09-11, thresholds unchanged): above 5 % on a side, or a side ratio above 2× → re-cut the ruler per side and say so. Never loosen quietly.
ARMING (re-registered 09-11 by the operator after report 0635 §6): a side wire arms at n >= 100 on that side and is checked every 30 min; the ratio wire is tested once, at the review point, not continuously.
FALSE-ALARM LINE (0550 §5a): if the registered rates are true, the chance of a false alarm at the first review, about 100 per side, is LONG 11.7 %, SHORT 5.4 %. A LONG reading between 5 % and 6 % at the first review is within noise. Nobody re-cuts on that without reading this line.
FALSE-ALARM RATE OF THESE WIRES (registered rates true): below n = 100 on a side nothing fires from that side, and the ratio is not read before the review point; at the review point, about 100 per side, noise alone trips at least one wire 44.5 % of the time — the ratio wire alone 37.3 % — and by 2026-10-11 60.2 %. Under the first arming (n >= 50, every pass) it was 85 % by the first review and 93 % by 2026-10-11. A wire alert is a prompt to look, not a finding.
Noise at this n, registered rates assumed true: LONG above 5 % 11.73 % · SHORT above 5 % 9.69 % · ratio above 2× 46.15 %.
Canon: mercury-sol/OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11. Alert, not a report: each condition fires once (state .kola_state/sol_book_gate_review.json).
```

**Where the model is simpler than reality.** The noise figures assume n equal on the two sides. In reality one side can reach 100 before the total reaches 200 (say, 110 against 85), and its side wire is then armed before the review point. The alert says it precisely: "below n = 100 on a side nothing fires from that side".

## 2. The re-measurement

### 2a. The 0635 Monte C., rebuilt — and checked against an exact computation

**The 0635 code was run inline and never saved.** So "same seed, same method" meant rebuilding it from its documented method:
- 40,000 paths, seed 20260911;
- registered rates true (LONG 3.33 %, SHORT 2.70 %);
- n equal per side, every armed wire checked at every evaluation;
- integer comparisons exactly as in the script.

Four RNG variants were run with that seed. None reproduces the 0635 table bit-for-bit, so the draw order differed. Both the rebuilt runs and the 0635 run were then checked against an **exact** computation: dynamic programming over the joint refusal counts, with no sampling error.

**The first arming (n ≥ 50, every pass):**

| by n per side | wire | 0635 MC | rebuilt MC (4 variants) | **exact** |
|---|---|---|---|---|
| 100 | LONG | 38.7 % | 38.4–38.8 % | 38.71 % |
| 100 | SHORT | 26.0 % | 25.8–26.4 % | 26.16 % |
| 100 | ratio | 70.5 % | 70.0–70.3 % | 70.23 % |
| 100 | **any** | **84.8 %** | 84.5–84.9 % | **84.68 %** |
| 200 | any | 91.2 % | 90.9–91.3 % | 91.06 % |
| 540 | LONG | 46.0 % | 45.6–45.9 % | 45.90 % |
| 540 | SHORT | 28.7 % | 29.0–29.6 % | 29.27 % |
| 540 | ratio | 82.5 % | 82.4–82.6 % | 82.53 % |
| 540 | **any** | **93.3 %** | 93.1–93.4 % | **93.23 %** |

- **The 0635 headline figures stand:** ≈ 85 % and ≈ 93 % are correct to within their sampling error.
- **One 0635 cell was off:** SHORT by 540 read 28.7 %, against an exact 29.27 %. That is about 2.6 standard errors at 40,000 paths. It changes nothing that was decided, but it is recorded here.

### 2b. The new arming — the figure you asked for

With the registered rates true, the chance that noise trips a wire:

| by n per side | LONG | SHORT | ratio | **ANY — exact** | ANY — MC, seed 20260911 |
|---|---|---|---|---|---|
| ≤ 99 (strictly before the review point) | 0 | 0 | 0 | **0.00 %** | 0.0 % |
| **100 (the review point)** | 11.73 % | 5.42 % | 37.33 % | **44.52 %** | 44.3 % (variants 44.3–44.6) |
| 200 | 27.33 % | 13.63 % | 37.33 % | 57.57 % | 57.6 % (57.5–58.1) |
| **540 (≈ 2026-10-11)** | 30.87 % | 14.59 % | 37.33 % | **60.18 %** | 60.3 % (60.1–60.6) |
| 1080 | 31.17 % | 14.61 % | 37.33 % | 60.36 % | — |

- **Answer to 2a: 0 % strictly before the first review, 44.5 % at it, and 60.2 % by 2026-10-11.**
- **The pace assumption.** "2026-10-11 ≈ 540 per side" is the 0635 assumption: 18 per side per day, the rate of the 08-14 era.
  - The first ten hours of this era ran faster, with 14 per side by 15:30.
  - At that pace the review point comes in about 3 days, and 2026-10-11 is about 1,000 per side.
  - The 1080 row shows that the figure barely moves: 60.4 %.

### 2c. The alert now carries it

This line replaces the ≈ 85 % line in every alert:

> FALSE-ALARM RATE OF THESE WIRES (registered rates true): below n = 100 on a side nothing fires from that side, and the ratio is not read before the review point; at the review point, about 100 per side, noise alone trips at least one wire 44.5 % of the time — the ratio wire alone 37.3 % — and by 2026-10-11 60.2 %. Under the first arming (n >= 50, every pass) it was 85 % by the first review and 93 % by 2026-10-11. A wire alert is a prompt to look, not a finding.

- **The contract recomputes 44.5, 37.3 and 60.2 exactly,** with its own pure-Python code, independent of the script, from the script's `SIDE_WIRE_MIN_N`, `RATIO_MIN_N` and `REVIEW_N`.
- **If someone changes the arming without the text, the contract goes red.** The side-wires-at-50 mutant shows this: the recomputation reads 68.5 % and 73.4 %, and two checks fail.
- **Unchanged:** the §5a line (11.7 % / 5.4 %) and the per-n binomial "Noise at this n" line.

## 3. The contract — `tests/test_sol_book_gate_review_fires.py`

**What changed:**
- **§4, side wire.** 🔴 It is now **SILENT at n = 50, 60, 80 and 99** at 6.00 %, 6.67 %, 6.25 % and 6.06 %, **on both sides** — all cases that fired before.
  - At n = 100, 6 % fires immediately, mid-window, with 110 evaluations.
  - Exactly 5 % stays silent, at both 5/100 and 6/120.
- **§5, ratio wire.** 🔴 It is **silent on mid-window passes**:
  - at 2.40×, with 110 evaluations;
  - at ∞, with SHORT 0/50;
  - at 3.96×, with 199 evaluations.

  It is **present at the review point**, in the same alert as the review, beside the side rates (4.00×, and ∞). It also proves:
  - exactly 2× at the review is silent;
  - after the review pass, 5.00× is silent — the ratio is read once;
  - a date-triggered review with the sides at 40 does not read the ratio, because its n ≥ 50 arming is unchanged;
  - a date-triggered review with the sides at 60 does read it;
  - a failed send in the review pass retries both the review point and the ratio.
- **§2 and §4, alert text.** Both now check the new ARMING and FALSE-ALARM lines, and check that the old ≈ 85 % line is **absent**.
- **§8, noise.** It pins the arming (100 / 50) and the unchanged thresholds (5 % / 2×). It proves that nothing can fire before the review point (0 %), and checks the three figures in the text against the exact recomputation.
- **Everything already proven stays proven:** the synthetic 200th row, the date, fire-once, exactly-5 % and exactly-2× silence, `mode=ro`, the stale-registration alert and the unreadable-DB alert.
- **Mutation hook.** `SOL_BGR_SCRIPT=<copy>` points the contract at a mutant copy.
  - The live script was never swapped for a mutant, because cron runs it every 30 min.
  - The suite never sets the variable, and the contract prints `script under test:` on its first line.

**Mutation check — each copy has one replacement, made on the installed script, and runs under the installed contract:**

```
installed contract aa67568c8113641f · mutants cut from the installed script 6be299655d3d201e (byte-identical to the candidate), one replacement each

== m1_side_arm_50: EXIT=1 · red checks: 16
  ❌ 🔴 LONG 3/50 = 6.00 % при n=50 — ТИШИНА (с 50 раньше звонило)
  ❌ 🔴 LONG 4/60 = 6.67 % при n=60 — ТИШИНА (с 50 раньше звонило)
  ❌ 🔴 LONG 5/80 = 6.25 % при n=80 — ТИШИНА (с 50 раньше звонило)
  ❌ 🔴 LONG 6/99 = 6.06 % при n=99 — ТИШИНА (с 50 раньше звонило)
  ❌ 🔴 SHORT 3/50 = 6.00 % при n=50 — ТИШИНА (с 50 раньше звонило)
  ❌ 🔴 SHORT 4/60 = 6.67 % при n=60 — ТИШИНА (с 50 раньше звонило)
  ❌ 🔴 SHORT 5/80 = 6.25 % при n=80 — ТИШИНА (с 50 раньше звонило)
  ❌ 🔴 SHORT 6/99 = 6.06 % при n=99 — ТИШИНА (с 50 раньше звонило)
  ❌ LONG 5/100 = ровно 5 % при n=100 — тишина (порог «выше»)
  ❌ LONG 6/120 = ровно 5 % при n=120 — тишина
  ❌ в тексте причина, доля и взвод
  ❌ уже сработало — тишина
  ❌ 🔴 взвод: сторона n >= 100, отношение при обеих n >= 50 (перерегистрация 09-11)
  ❌ 🔴 до точки ревью ни один провод не может сработать от шума (0 %)
  ❌ 🔴 в тексте «68.5 %» в точке ревью = точный пересчёт
  ❌ в тексте «73.4 %» к 2026-10-11 = точный пересчёт

== m2_ratio_every_pass: EXIT=1 · red checks: 7
  ❌ 🔴 2.40× посреди окна (110 оценок, обе n >= 50) — ТИШИНА (раньше звонило)
  ❌ 🔴 ∞ посреди окна (SHORT 0 отказов при n=50) — ТИШИНА
  ❌ 🔴 3.96× при 199 оценках — ТИШИНА: за строку до ревью отношение не читается
  ❌ и в состоянии ничего не помечено
  ❌ 🔴 200-я строка, 4 % против 1 % = 4.00× — ОДНА тревога, и провод отношения В НЕЙ
  ❌ в тексте и точка ревью, и отношение
  ❌ 🔴 после прохода ревью 5.00× — ТИШИНА: отношение читается ОДИН раз
```

**Full output, installed contract, as botuser, no override:**

```
script under test: /home/botuser/.openclaw/workspace/scripts/sol_book_gate_review.py
── 1. ЗАПРОС — ДОСЛОВНО §5b, И ОН ИДЁТ НА ЖИВОЙ СХЕМЕ ─────────────────
  ✅ QUERY дословно совпадает с SQL-блоком §5b отчёта 0550
  ✅ якорь в запросе = ANCHOR
  ✅ запрос исполняется на живой trades.db (mode=ro)

── 2. 🔴 199 — ТИШИНА; 200-я — ОДНА ТРЕВОГА С ЦИФРАМИ; ПОТОМ ТИШИНА ─────
2026-09-11T15:31:22Z [sol_book_gate_review] n=199/200 LONG 3/100 SHORT 2/99 ratio=1.48× fired_ever=[] new=[]
  ✅ 199 оценок (3.00 % / 2.02 %, 1.49×) — ни одной отправки
  ✅ и в состоянии ничего не помечено
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] new=['review_point']
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
  ✅ в тексте тревоги: текущая доля ложных тревог проводов
  ✅ 🔴 старой строки «≈ 85 % до ревью» в тексте БОЛЬШЕ НЕТ
2026-09-11T15:31:22Z [sol_book_gate_review] n=205/200 LONG 3/103 SHORT 2/102 ratio=1.49× fired_ever=['review_point'] new=[]
  ✅ 🔴 уже сработало — 205 оценок, повторного звонка нет

── 3. ДАТА 2026-10-11 ПРИ n < 200 ───────────────────────────────────
2026-09-11T15:31:22Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=[] new=[]
  ✅ 2026-10-10 23:59:59 — тишина
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=['review_point'] new=['review_point']
  ✅ 2026-10-11 00:00:00 — одна тревога review_point
  ✅ причина названа датой
2026-09-11T15:31:22Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=['review_point'] new=[]
  ✅ на следующий день — тишина

── 4. 🔴 ПРОВОД СТОРОНЫ — ВЗВОД С n >= 100 (перерегистрация 09-11), ВЫШЕ 5 % ─────
2026-09-11T15:31:22Z [sol_book_gate_review] n=60/200 LONG 3/50 SHORT 0/10 ratio=∞ fired_ever=[] new=[]
  ✅ 🔴 LONG 3/50 = 6.00 % при n=50 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:31:22Z [sol_book_gate_review] n=70/200 LONG 4/60 SHORT 0/10 ratio=∞ fired_ever=[] new=[]
  ✅ 🔴 LONG 4/60 = 6.67 % при n=60 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:31:22Z [sol_book_gate_review] n=90/200 LONG 5/80 SHORT 0/10 ratio=∞ fired_ever=[] new=[]
  ✅ 🔴 LONG 5/80 = 6.25 % при n=80 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:31:22Z [sol_book_gate_review] n=109/200 LONG 6/99 SHORT 0/10 ratio=∞ fired_ever=[] new=[]
  ✅ 🔴 LONG 6/99 = 6.06 % при n=99 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:31:22Z [sol_book_gate_review] n=60/200 LONG 0/10 SHORT 3/50 ratio=∞ fired_ever=[] new=[]
  ✅ 🔴 SHORT 3/50 = 6.00 % при n=50 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:31:22Z [sol_book_gate_review] n=70/200 LONG 0/10 SHORT 4/60 ratio=∞ fired_ever=[] new=[]
  ✅ 🔴 SHORT 4/60 = 6.67 % при n=60 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:31:22Z [sol_book_gate_review] n=90/200 LONG 0/10 SHORT 5/80 ratio=∞ fired_ever=[] new=[]
  ✅ 🔴 SHORT 5/80 = 6.25 % при n=80 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:31:22Z [sol_book_gate_review] n=109/200 LONG 0/10 SHORT 6/99 ratio=∞ fired_ever=[] new=[]
  ✅ 🔴 SHORT 6/99 = 6.06 % при n=99 — ТИШИНА (с 50 раньше звонило)
2026-09-11T15:31:22Z [sol_book_gate_review] n=110/200 LONG 5/100 SHORT 0/10 ratio=∞ fired_ever=[] new=[]
  ✅ LONG 5/100 = ровно 5 % при n=100 — тишина (порог «выше»)
2026-09-11T15:31:22Z [sol_book_gate_review] n=130/200 LONG 6/120 SHORT 0/10 ratio=∞ fired_ever=[] new=[]
  ✅ LONG 6/120 = ровно 5 % при n=120 — тишина
2026-09-11T15:31:22Z [sol_book_gate_review] due=['wire_rate_LONG'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=110/200 LONG 6/100 SHORT 0/10 ratio=∞ fired_ever=['wire_rate_LONG'] new=['wire_rate_LONG']
  ✅ 🔴 LONG 6/100 = 6 % при n=100 — тревога СРАЗУ, посреди окна (110 оценок)
  ✅ в тексте причина, доля и взвод
  ✅ строка ложной тревоги §5a есть и в тревоге провода
  ✅ 🔴 и текущая доля ложных тревог проводов
  ✅ старой строки «≈ 85 %» нет и здесь
2026-09-11T15:31:22Z [sol_book_gate_review] n=122/200 LONG 7/110 SHORT 0/12 ratio=∞ fired_ever=['wire_rate_LONG'] new=[]
  ✅ уже сработало — тишина
2026-09-11T15:31:22Z [sol_book_gate_review] due=['wire_rate_SHORT'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=120/200 LONG 0/20 SHORT 6/100 ratio=∞ fired_ever=['wire_rate_SHORT'] new=['wire_rate_SHORT']
  ✅ SHORT 6/100 = 6 % — тревога wire_rate_SHORT

── 5. 🔴 ПРОВОД ОТНОШЕНИЯ — ТОЛЬКО В ТОЧКЕ РЕВЬЮ, НЕ НА КАЖДОМ ПРОХОДЕ ─────
2026-09-11T15:31:22Z [sol_book_gate_review] n=110/200 LONG 2/50 SHORT 1/60 ratio=2.40× fired_ever=[] new=[]
  ✅ 🔴 2.40× посреди окна (110 оценок, обе n >= 50) — ТИШИНА (раньше звонило)
2026-09-11T15:31:22Z [sol_book_gate_review] n=100/200 LONG 1/50 SHORT 0/50 ratio=∞ fired_ever=[] new=[]
  ✅ 🔴 ∞ посреди окна (SHORT 0 отказов при n=50) — ТИШИНА
2026-09-11T15:31:22Z [sol_book_gate_review] n=199/200 LONG 4/100 SHORT 1/99 ratio=3.96× fired_ever=[] new=[]
  ✅ 🔴 3.96× при 199 оценках — ТИШИНА: за строку до ревью отношение не читается
  ✅ и в состоянии ничего не помечено
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point', 'wire_ratio'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=200/200 LONG 4/100 SHORT 1/100 ratio=4.00× fired_ever=['review_point', 'wire_ratio'] new=['review_point', 'wire_ratio']
  ✅ 🔴 200-я строка, 4 % против 1 % = 4.00× — ОДНА тревога, и провод отношения В НЕЙ
  ✅ в тексте и точка ревью, и отношение
  ✅ отношение стоит рядом с долями сторон
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] new=['review_point']
  ✅ точка ревью при 1.50× — только review_point
2026-09-11T15:31:22Z [sol_book_gate_review] n=240/200 LONG 5/120 SHORT 1/120 ratio=5.00× fired_ever=['review_point'] new=[]
  ✅ 🔴 после прохода ревью 5.00× — ТИШИНА: отношение читается ОДИН раз
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=200/200 LONG 4/100 SHORT 2/100 ratio=2.00× fired_ever=['review_point'] new=['review_point']
  ✅ ровно 2× в точке ревью (4 % против 2 %) — только review_point
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point', 'wire_ratio'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=200/200 LONG 2/100 SHORT 0/100 ratio=∞ fired_ever=['review_point', 'wire_ratio'] new=['review_point', 'wire_ratio']
  ✅ ∞ в точке ревью — провод отношения
  ✅ и ∞ названо в тексте
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=80/200 LONG 2/40 SHORT 0/40 ratio=∞ fired_ever=['review_point'] new=['review_point']
  ✅ ревью по дате, стороны по 40 (< 50) — отношение не читается (взвод 50 не тронут)
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point', 'wire_ratio'] DELIVERED=True
2026-09-11T15:31:22Z [sol_book_gate_review] n=120/200 LONG 3/60 SHORT 0/60 ratio=∞ fired_ever=['review_point', 'wire_ratio'] new=['review_point', 'wire_ratio']
  ✅ ревью по дате, стороны по 60 и ∞ — провод отношения в той же тревоге
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point', 'wire_ratio'] DELIVERED=False
2026-09-11T15:31:22Z [sol_book_gate_review] n=200/200 LONG 4/100 SHORT 1/100 ratio=4.00× fired_ever=[] new=[]
  ✅ отправка в проходе ревью упала — ничего не помечено
2026-09-11T15:31:22Z [sol_book_gate_review] due=['review_point', 'wire_ratio'] DELIVERED=True
2026-09-11T15:31:23Z [sol_book_gate_review] n=200/200 LONG 4/100 SHORT 1/100 ratio=4.00× fired_ever=['review_point', 'wire_ratio'] new=['review_point', 'wire_ratio']
  ✅ повтор — всё ещё проход ревью: и точка, и отношение

── 6. ОТПРАВКА УПАЛА — НЕ ПОМЕЧЕНО, СЛЕДУЮЩИЙ ПРОХОД ПОВТОРЯЕТ ─────────
2026-09-11T15:31:23Z [sol_book_gate_review] due=['review_point'] DELIVERED=False
2026-09-11T15:31:23Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=[] new=[]
  ✅ отправка вернула False — код 1, ничего не помечено
2026-09-11T15:31:23Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:31:23Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] new=['review_point']
  ✅ следующий проход — тревога ушла

── 7. mode=ro — ЗАПИСЬ НЕВОЗМОЖНА, ФАЙЛ НЕ ТРОНУТ ─────────────────────
2026-09-11T15:31:23Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:31:23Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] new=['review_point']
2026-09-11T15:31:23Z [sol_book_gate_review] due=['review_point'] DELIVERED=True
2026-09-11T15:31:23Z [sol_book_gate_review] n=200/200 LONG 3/100 SHORT 2/100 ratio=1.50× fired_ever=['review_point'] new=['review_point']
  ✅ sha256 БД после двух проходов тот же
  ✅ соединение скрипта отвергает INSERT (readonly)

── 8. ШУМ В ТЕКСТЕ = §5a; ДОЛЯ ЛОЖНЫХ ТРЕВОГ = ТОЧНЫЙ ПЕРЕСЧЁТ ───────────
  ✅ P(LONG>5 %) при n=100 = 11.7 %
  ✅ P(SHORT>5 %) при n=100 = 5.4 %
  ✅ P(LONG>5 %) при n=200 = 7.3 %
  ✅ P(SHORT>5 %) при n=200 = 2.1 %
  ✅ 🔴 взвод: сторона n >= 100, отношение при обеих n >= 50 (перерегистрация 09-11)
  ✅ пороги не сдвинуты: 5 % и 2×
     точно: до ревью 0.00 % · в точке ревью 44.52 % (отношение 37.33 %) · к 2026-10-11 60.18 %
  ✅ 🔴 до точки ревью ни один провод не может сработать от шума (0 %)
  ✅ 🔴 в тексте «44.5 %» в точке ревью = точный пересчёт
  ✅ в тексте «37.3 %» для одного отношения = точный пересчёт
  ✅ в тексте «60.2 %» к 2026-10-11 = точный пересчёт
  ✅ старые цифры названы как старые (85 % / 93 %)

── 9. РЕГИСТРАЦИЯ СДВИНУЛАСЬ — СЧЁТЧИК ГОВОРИТ, ЧТО УСТАРЕЛ ────────────
2026-09-11T15:31:23Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=[] new=[]
  ✅ полы совпадают с 09-11 — тишина
2026-09-11T15:31:23Z [sol_book_gate_review] config floors {'LONG': 0.43, 'SHORT': 0.4} != pinned {'LONG': 0.4214, 'SHORT': 0.3975}; alert DELIVERED=True
2026-09-11T15:31:23Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=['registration_moved:{"LONG": 0.43, "SHORT": 0.4}'] new=['registration_moved:{"LONG": 0.43, "SHORT": 0.4}']
  ✅ полы в config.py другие — одна тревога «устарел»
2026-09-11T15:31:23Z [sol_book_gate_review] n=20/200 LONG 0/10 SHORT 0/10 ratio=n/a fired_ever=['registration_moved:{"LONG": 0.43, "SHORT": 0.4}'] new=[]
  ✅ повторно — тишина
  ✅ 🔴 ЖИВОЙ SOL config.py сейчас = приколотая регистрация 09-11 (красный здесь = перерез был, а счётчик не перенацелен)

── 10. БД НЕ ЧИТАЕТСЯ — ПЕРЕПРОС, ОДНА ТРЕВОГА НА ПОЛОМКУ ───────────────
2026-09-11T15:31:23Z [sol_book_gate_review] read failed (unable to open database file); re-asking in 90s before calling anyone
2026-09-11T15:31:23Z [sol_book_gate_review] read failed twice (unable to open database file); alert DELIVERED=True
  ✅ перед звонком перепросили через 90 с
  ✅ одна тревога «не может прочитать»
2026-09-11T15:31:23Z [sol_book_gate_review] read failed (unable to open database file); re-asking in 0s before calling anyone
2026-09-11T15:31:23Z [sol_book_gate_review] read still failing (unable to open database file); already alerted this outage
  ✅ та же поломка — второй тревоги нет
2026-09-11T15:31:23Z [sol_book_gate_review] n=5/200 LONG 0/5 SHORT 0/0 ratio=n/a fired_ever=[] new=[]
  ✅ после хорошего чтения поломка снята
2026-09-11T15:31:23Z [sol_book_gate_review] read failed (unable to open database file); re-asking in 0s before calling anyone
2026-09-11T15:31:23Z [sol_book_gate_review] read failed twice (unable to open database file); alert DELIVERED=True
  ✅ новая поломка — снова тревога

── 11. БОЕВОЙ ПУТЬ ПОМЕЧЕН КАК АЛЕРТ; КОНТРАКТ В СЕТЬ НЕ ХОДИТ ──────────
  ✅ вызов send_full_report(text, require_link=False) на месте
  ✅ run() не имеет отправителя по умолчанию (тест не может дойти до Telegram)
  ✅ импорт отправителя без записи байткода в дерево Титана

✅ ВСЕ ПРОВЕРКИ ЗЕЛЁНЫЕ
```

## 4. 🔴 Still above 40 % — what carries it, and what else would be needed

**It is not fixed. At the review point, 44.5 % of registered-rate paths still trip a wire from noise.** Two things carry it.

**1. The ratio, read at about 100 per side: 37.3 %, noisy by its nature.** About 3 refusals are expected per side, and at that n no rule separates noise from a real split. The chance each rule fires, at 100 per side:

| rule | from noise (registered 1.23×) | truth 2.5× (5.0 % / 2.0 %) | truth 5.67× (3.53 % / 0.62 %, the 08-14 breach) |
|---|---|---|---|
| "above 2×" (the registered wire) | 37.3 % | 59.3 % | 79.9 % |
| exact conditional test, α 5 % | 1.2 % | 5.0 % | 3.8 % |
| "above 2×" read at 540 per side | **8.9 %** | 72.8 % | 98.1 % |

The exact test is quiet only because it is blind. What makes the ratio a test is **n**, not a different rule.

**2. The side wires re-accumulate after they arm.** Checked every pass from n = 100, LONG goes from 11.7 % (one look, at 100) to 30.9 % by 540, and SHORT from 5.4 % to 14.6 %.

**Options, all measured exactly, none built.** Each would be a further re-registration and the operator's call:

| option | by the review point | by 2026-10-11 |
|---|---|---|
| **built now:** sides n ≥ 100 every pass, ratio once at the review | 44.5 % | 60.2 % |
| D — as built, but the ratio read once at 2026-10-11 | 16.5 % | 44.8 % |
| **E — sides at two fixed looks (the review point, 2026-10-11), ratio once at 2026-10-11** | **16.5 %** | **23.9 %** |
| F — sides at the review only, ratio once at 2026-10-11 | 16.5 % | 23.4 % |
| A2 — sides at two fixed looks, ratio at the review | 44.5 % | 45.1 % |

**What E would still catch, at its looks:**
- a true 7 % side rate: 70.9 % of the time at n = 100, and 96.4 % at n = 540;
- a true 10 % side rate: 94.2 % at n = 100;
- a true 2.5× split: 72.8 % at 540;
- a true 5.67× split: 98.1 % at 540.

**What E would cost:**
- a side breach that appears between the two looks is seen at the next look, not within 30 min;
- the ratio would no longer be read at the first review at all — only at 2026-10-11.

## 5. The canon — `OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11`

- **It is a documentation file.** In the SOL tree, `grep` finds it mentioned only in `config.py`, and only in comments. Nothing opens it.
- **Backup,** outside both trees: `/root/backups/OPEN-ITEMS-SOL.md.bak_rearm_20260911T1532Z`.
- **Ownership** is unchanged: `root:root 644`.
- **Three edits:**
  - the new subsection, "RE-REGISTERED 2026-09-11 15:32";
  - the REVIEW-REMINDER bullet that described the first arming now carries the re-registration;
  - that section's 85 % warning is marked ⚰️ superseded, and kept as the reason.

```diff
--- /root/backups/OPEN-ITEMS-SOL.md.bak_rearm_20260911T1532Z	2026-09-11 06:20:43.946029848 +0000
+++ /mnt/volume_nyc1_1780480650620/mercury-sol/OPEN-ITEMS-SOL.md	2026-09-11 15:34:59.348214912 +0000
@@ -51,6 +51,47 @@
 
 **Above 5 % on either side, or a side ratio above 2× → a finding about the calibration, and grounds to revisit: re-cut the ruler per side and say so. Never loosen quietly.**
 
+### 🔴 RE-REGISTERED 2026-09-11 15:32 — THE WIRES' ARMING MOVED; THEIR THRESHOLDS DID NOT
+
+**This is a re-registration, and it is recorded as one.** **The operator made this call after reading report 2026-09-11-0635 §6.** Built in workspace commit `0c58364` (`scripts/sol_book_gate_review.py` and its contract); no bot file changed and nothing restarted. Record: `kola-reports/reports/2026-09-11-1550-mercury-sol-book-gate-wires-re-armed.md`.
+
+- **The thresholds are unchanged.** A side wire trips above 5 %, and the ratio wire above 2×. Both are "above", compared in integers, so exactly 5 % or exactly 2× does not fire. The wording in bold above stands as written.
+- **What moved is WHEN the thresholds may be read:**
+
+| wire | as first built (05:50 spec, installed 06:12) | re-registered 15:32 |
+|---|---|---|
+| side wire | armed at n ≥ 50 on that side, checked every 30-min pass | armed at **n ≥ 100** on that side, still checked every 30-min pass |
+| ratio wire | both sides n ≥ 50, checked **every 30-min pass** (continuous) | **tested once, at the review point** (200 evaluations or 2026-10-11), with both sides still at n ≥ 50. 🔴 **The ratio wire is now a review-point test, not a continuous one.** |
+
+- **Why — the measured false-alarm rate, with the registered rates true** (LONG 3.33 %, SHORT 2.70 %):
+  - at n = 50 per side, the ratio wire fires from noise **48.4 %** of the time (binomial);
+  - over the path, at least one wire tripped before the first review with **≈ 85 %** probability, and by 2026-10-11 with **≈ 93 %**; the ratio wire alone carried 70 % → 82 %.
+  - A wire that rings from noise in half of all cases is not a detector. An alert that is wrong 85 % of the time trains its reader to ignore it, which is the very failure §BOOK-GATE-REVIEW-MISSED records. **This is not a quiet loosening.** The thresholds stand; the moment they may be read moved, and it is written down here with the old figures beside the new.
+
+| false alarm from noise, registered rates true | before (armed at 50, every pass) | after (re-registered 15:32) |
+|---|---|---|
+| LONG side wire, at its arming n | 23.2 % (n = 50) | **11.7 %** (n = 100) |
+| SHORT side wire, at its arming n | 15.2 % (n = 50) | **5.4 %** (n = 100) |
+| ratio wire, at its only or first reading | 48.4 % (n = 50, then every pass) | **37.3 %** (n = 100, once) |
+| any wire, strictly before the review point | 84.5 % | **0 %** |
+| any wire, by the review point (≈ 100 per side) | **84.7 %** (0635 MC: 84.8 %) | **44.5 %** |
+| any wire, by 2026-10-11 (≈ 540 per side) | **93.2 %** (0635 MC: 93.3 %) | **60.2 %** |
+
+  - The figures are exact, by dynamic programming. The 0635 Monte C., re-run for the new arming with the same seed and method (40,000 paths, seed 20260911), gives 44.3 % and 60.3 %.
+  - The model: n equal per side, and every armed wire checked at every evaluation.
+- 🔴 **NOT FIXED: at the review point it is still above 40 %.** Two things carry what is left:
+  1. **Read at about 100 per side, the ratio is noisy by its nature: 37.3 %.** About 3 refusals are expected per side, and at that n no rule separates noise from a real split.
+     - "Above 2×" fires from noise 37.3 % of the time, and catches a true split like the 08-14 one (5.67×) 79.9 % of the time.
+     - An exact conditional test at α 5 % fires from noise 1.2 % of the time, but catches that same split only 3.8 % of the time.
+     - At about 540 per side (2026-10-11), the same 2× rule fires from noise 8.9 % of the time and catches 5.67× 98.1 % of the time.
+  2. **After arming, the side wires are re-checked every pass, so sequential looks pile up again.** LONG goes from 11.7 % at n = 100 to 30.9 % by 540; SHORT from 5.4 % to 14.6 %.
+- **What else would be needed.** Each option is measured, **not built**, and each would be a further re-registration and the operator's call:
+  - **D.** Read the ratio once, at 2026-10-11, instead of at the review → 16.5 % by the review, 44.8 % by 2026-10-11.
+  - **E.** Test the side wires at two fixed looks, the review point and 2026-10-11, and the ratio once, at 2026-10-11 → **16.5 % by the review, 23.9 % by 2026-10-11.**
+    - At its looks, E still catches a true 7 % side rate 70.9 % of the time at n = 100 and 96.4 % at n = 540, and a true 2.5× split 72.8 % of the time at n = 540.
+  - **F.** Test the side wires at the review point only, and the ratio at 2026-10-11 → 16.5 % and 23.4 %.
+- **The alert carries its own current false-alarm rate.** The line "FALSE-ALARM RATE OF THESE WIRES … 44.5 % … 37.3 % … 60.2 %" replaces the ≈ 85 % line. The contract recomputes these figures exactly from the script's constants, so the text cannot drift from the code.
+
 ### 🔴 §BOOK-GATE-REVIEW-MISSED — NAMED FAILURE, 2026-08-20 23:30:02 UTC
 
 The 08-14 re-registration set a review point of "200 further gate evaluations, or 2026-09-14". **The 200th evaluation came on 2026-08-20 23:30:02. At that moment LONG was 9/117 = 7.69 % (above 5 %), SHORT 3/83 = 3.61 %, and the side ratio 2.13× (above 2×). Both wires had tripped. Nobody checked for three weeks.** The 2026-09-01 report's "1.03×" pooled refusals from before and after the re-cut against pre-gate denominators; it was not a test of the live floors. The breach was found only on 2026-09-11 (report 0526), at 962 evaluations and 5.67×. **The operator recorded it as their own failure. The mechanism that should have caught it did not exist: the review depended on someone remembering.**
@@ -65,7 +106,11 @@
 - **Script:** `workspace/scripts/sol_book_gate_review.py`, workspace commits `91d1668` and `68a0298`.
   - It runs the §5b query verbatim, with `mode=ro` and SELECTs only.
   - The review point fires once, at n ≥ 200 or 2026-10-11, whichever comes first.
-  - The wires fire immediately: a side at n ≥ 50 and above 5 %, or both sides at n ≥ 50 and a ratio above 2×. The comparisons are integer, so exactly 5 % or exactly 2× does not fire.
+  - ~~The wires fire immediately: a side at n ≥ 50 and above 5 %, or both sides at n ≥ 50 and a ratio above 2×.~~ **Re-registered 15:32, commit `0c58364` (see the section above):**
+    - a side wire fires immediately at **n ≥ 100** on that side and above 5 %;
+    - the ratio wire is tested **once, in the review-point pass**, with both sides at n ≥ 50 and a ratio above 2×.
+
+    The comparisons are integer, so exactly 5 % or exactly 2× does not fire.
   - Each alert carries n and refusals per side, the rates, the ratio, the registered 3.33 % / 2.70 % / 1.23×, and the §5a false-alarm line. It goes out through `send_full_report(text, require_link=False)`.
 - **Beyond §5b, two one-shot alerts:**
   - It alerts if SOL `config.py` `BOOK_GATE_LEAN_FLOOR` stops matching the pinned 09-11 floors. A counter that measures a registration no longer running is this same failure, only quieter.
@@ -74,7 +119,8 @@
   - It fires on a synthetic 200th row, on a side breach and on a ratio breach.
   - It stays silent at 199, at n = 49, at exactly 5 % and exactly 2×, and after firing.
   - Mutation-checked. It also goes red when the live floors move: 🔴 **the next re-cut must re-point `ANCHOR`, `EXPECTED` and `PINNED_FLOORS` in the script.**
-- 🔴 **Read this before acting on a ratio alert.** If the registered rates are true, the ratio wire as specified fires by noise alone **48 % of the time at n = 50 per side**, 37 % at 100 and 25 % at 200 (binomial). **Over the whole path** — armed from n = 50 and re-checked every 30 min — noise alone trips at least one wire before the first review with **≈ 85 %** probability, and by 2026-10-11 with **≈ 93 %** (Monte C., registered rates true; the alert says so, commit `68a0298`). At small n, a ratio alert is a prompt to look, not a finding. The thresholds were built verbatim; this is recorded, not changed.
+- ⚰️ **SUPERSEDED 15:32 — these are the FIRST arming's figures, kept as the reason for the re-registration above.** Current figures: 0 % before the review point, 44.5 % at it, 60.2 % by 2026-10-11.
+- 🔴 **Read this before acting on a ratio alert (first arming, 06:12–15:32).** If the registered rates are true, the ratio wire as specified fires by noise alone **48 % of the time at n = 50 per side**, 37 % at 100 and 25 % at 200 (binomial). **Over the whole path** — armed from n = 50 and re-checked every 30 min — noise alone trips at least one wire before the first review with **≈ 85 %** probability, and by 2026-10-11 with **≈ 93 %** (Monte C., registered rates true; the alert says so, commit `68a0298`). At small n, a ratio alert is a prompt to look, not a finding. The thresholds were built verbatim; this is recorded, not changed.
 - **Live at install:** n = 2/200 (LONG 0/0, SHORT 0/2), nothing due.
 
 *The original specification follows, as written on 2026-09-11 05:50.*
```

## 6. Neither bot touched — and the usual

**Both trees, sha256 of every file,** from the baseline at 15:12:13 (before any change) to 15:35:15.

**SOL tree:** 351 files at baseline, 351 now; 2 differ.
- `OPEN-ITEMS-SOL.md` — the canon, the one intended change (§5).
- `trades.db` — the live bot's rows. It is held open by PIDs 1181897 and 1181966, the mercury-sol master and worker.

**Titan tree:** 208 files at baseline, 208 now; 3 differ.
- `trades.db` — held open by PIDs 961100 and 961118, `titan.service`.
- `oi_cache.json` — Titan's 5-min OI cache, mtime 15:20:04.
- `healthcheck_state.json` — written by `healthcheck.timer`, last fired 15:34:20, mtime 15:34:25.

🔴 **UNEXPECTED changes: none.** Titan `git status --short -- titan-bot`: **0 lines**.
- Titan's sender bytecode was not rewritten: `__pycache__/full_report.cpython-312.pyc` still has mtime 2026-08-04 19:39:21.
- SOL `trades.db` was opened only with `mode=ro`, by the contract's live-schema check and by `--selftest`.
- Titan's DB was never opened.

**Services — the same PIDs, NRestarts 0 → 0, nothing restarted:**
```
before (15:12)  service · MainPID · NRestarts · active since
1181897 0 Fri 2026-09-11 05:40:08 UTC  mercury-sol
961100 0 Thu 2026-09-10 14:36:20 UTC  titan
3521920 0 Sat 2026-08-08 15:37:06 UTC  mercury-sol-optimizer-listener
after (15:35)
1181897 0 Fri 2026-09-11 05:40:08 UTC  mercury-sol
961100 0 Thu 2026-09-10 14:36:20 UTC  titan
3521920 0 Sat 2026-08-08 15:37:06 UTC  mercury-sol-optimizer-listener
```

**`crontab -l` — unchanged.** This pass edited the script, not the cron line.
```
$ crontab -l | wc -l                         →  76 before, 76 after
$ sha256 before / after                      →  9ccbbf26d503989e6b6bea05a047eaf9ea54c73f41e79c21d96f9e820775e3d6 (both) · cmp: BYTE-IDENTICAL
$ crontab -l | grep -c sol_book_gate_review.py   →  1
$ crontab -l | grep sol_book_gate_review.py
*/30 * * * * /usr/bin/timeout 300 /usr/bin/python3 /home/botuser/.openclaw/workspace/scripts/sol_book_gate_review.py >> /home/botuser/.openclaw/workspace/.kola_state/sol_book_gate_review.log 2>&1
```

**`--selftest` under an empty `env -i`, on the installed script** (15:32:22):
```
$ env -i /usr/bin/python3 /home/botuser/.openclaw/workspace/scripts/sol_book_gate_review.py --selftest
db: OK mode=ro · LONG 0/14 · SHORT 0/14 · due now: []
config floors: {'LONG': 0.4214, 'SHORT': 0.3975} · pinned {'LONG': 0.4214, 'SHORT': 0.3975} · match=True
state: /home/botuser/.openclaw/workspace/.kola_state/sol_book_gate_review.json · dir writable=True
sender: OK (full_report imported, token and chat id present; nothing sent)
SELFTEST OK
EXIT=0
```

**The live counter's n, now:**
- **n = 28/200:** LONG 0/14, SHORT 0/14.
- `fired = {}`: nothing has ever fired.
- The log's last lines are the cron passes:
```
2026-09-11T15:00:03Z [sol_book_gate_review] n=28/200 LONG 0/14 SHORT 0/14 ratio=n/a fired_ever=[] new=[]
2026-09-11T15:30:03Z [sol_book_gate_review] n=28/200 LONG 0/14 SHORT 0/14 ratio=n/a fired_ever=[] new=[]
```

**Workspace suite, as botuser** (`whoami` → botuser):
- `ИТОГО В НАБОРЕ: 266/267 зелёных за 44с (по 8 разом)`, then **267/267** — `✅ ВСЕ КОНТРАКТЫ ЗЕЛЁНЫЕ (из них 1 — только со второго захода в одиночку)`. The 0635 pass had 266.
- `test_sol_book_gate_review_fires.py` was ✅ in the parallel run.
- The one that needed the solo retry was `test_contracts_never_write_battle_parking.py`: `FileNotFoundError … tests/test_zzcanary_1301199_1.py`.
  - It globs `tests/` while another contract's temporary canary file disappears mid-read. That is a race between two unrelated contracts.
  - Run solo by the runner, and again by me: `✅ КОНТРАКТ ЦЕЛ`, EXIT=0.

**`openitems_guard` — EXIT=0 before (15:10) and after (15:35):**
```
openitems_guard — canon: /mnt/volume_nyc1_1780480650620/kola-reports/reports/OPEN-ITEMS.md
  titan-bot HEAD : cd0f175   <- the SUBJECT, this is what is compared
  repo HEAD      : cd0f175   (context only, NOT compared)
  watched values : 14

✅ header and current-state table agree with runtime.
EXIT=0
```

**The commit** went through the hook as neutral, with no token pass and no BLOCK. Neither file is under a protected path, and the added lines match nothing in `TRADING_REACH`; this was checked before committing. `commit_gate_pass.log` accordingly has no new line.
```
0c58364 feat(sol): the book-gate wires are RE-ARMED — side wires at n>=100, the ratio read only at the review point. Thresholds unchanged.
 scripts/sol_book_gate_review.py          |  63 ++++++----
 tests/test_sol_book_gate_review_fires.py | 203 +++++++++++++++++++++++++------
```

## 7. What stays open, named

- 🔴 **The false-alarm rate is still 44.5 % at the review point and 60.2 % by 2026-10-11.** Options D, E and F are in §4. Each would be a further re-registration, so the choice is yours. **Until then, a wire alert remains a prompt to look, not a finding, and the alert says so.**
- **Nothing watches the watcher.** This is unchanged from 0635: if the cron line goes, the counter falls silent without an alert.
- **The M. Carlo and the exact computation are now in this report** (Appendix B), so the next re-measurement need not rebuild them. That was the one gap in "same method" this time.
- **The suite's parallel-run race** between `test_contracts_never_write_battle_parking.py` and a canary-writing contract is noise, not a regression. It was not touched: it is outside this pass.

## Verification

- **Pre-flight:** `openitems_guard` returned EXIT=0 before anything else. The baseline (both trees, three services, crontab) was taken at 15:12, before any change.
- **Changed, in the workspace, outside both trees:**
  - `scripts/sol_book_gate_review.py` and `tests/test_sol_book_gate_review_fires.py`, in workspace commit `0c58364`;
  - installed atomically at 15:31:22 UTC, owner `botuser:botuser` and modes 755 / 644 kept.
- **Contract:** 87/87 green as botuser. Each mutant turns it red (16 and 7 checks). Suite 267/267 as botuser.
- **Re-measured:** exactly (DP), and by the rebuilt same-seed Monte C..
  - New arming: **0 % before the review, 44.5 % at it, 60.2 % by 2026-10-11** — still above 40 %, and stated as not fixed.
  - The old table was re-derived: 84.7 % and 93.2 %.
- **Canon:** `§BOOK-GATE-RECUT-2026-09-11` now has the dated re-registration, new figures beside old. The backup is outside both trees.
- **Bots:**
  - no bot file changed;
  - `NRestarts` 0 → 0, with the same PIDs, on all three services;
  - crontab byte-identical;
  - `openitems_guard` EXIT=0 after;
  - `--selftest` OK under `env -i`;
  - live n = 28/200.

## Appendix A — the script diff, `68a0298` → `0c58364`

```diff
diff --git a/scripts/sol_book_gate_review.py b/scripts/sol_book_gate_review.py
index 801b766..748d7a0 100755
--- a/scripts/sol_book_gate_review.py
+++ b/scripts/sol_book_gate_review.py
@@ -9,15 +9,25 @@ of 2.13× — BOTH pre-registered wires already tripped — and nobody checked f
 The mechanism that should have caught it did not exist: the review depended on someone
 remembering. This script is that mechanism.
 
-WHAT IT DOES — report 2026-09-11-0550 §5b, option 1, built verbatim:
+WHAT IT DOES — report 2026-09-11-0550 §5b, option 1, as re-registered 2026-09-11:
   * reads SOL trades.db with mode=ro and runs the §5b SELECT, nothing else;
   * alerts ONCE at the review point: n_LONG + n_SHORT >= 200, or the UTC date reaches
     2026-10-11 — whichever comes first;
-  * alerts IMMEDIATELY on a wire: a side with n >= 50 and a rate above 5 %, or both sides
-    with n >= 50 and a side ratio above 2×;
+  * alerts IMMEDIATELY on a side wire: a side with n >= 100 and a rate above 5 %;
+  * tests the RATIO wire ONCE, in the review-point pass: both sides with n >= 50 and a side
+    ratio above 2× — never on the passes in between;
   * each condition fires exactly once — state in .kola_state/sol_book_gate_review.json;
   * alerts go through send_full_report(text, require_link=False): alerts, not reports.
 
+🔴 RE-REGISTERED 2026-09-11 by the operator, after report 0635 §6 — the ARMING moved, the
+thresholds did not. As first built (§5b verbatim) the side wires armed at n >= 50 and the
+ratio wire was checked on every 30-min pass. With the registered rates TRUE, the ratio wire
+at n = 50 per side fires from noise 48.4 % of the time, and at least one wire tripped before
+the first review with ≈ 85 % probability. A bell that rings from noise that often is not a
+detector: it trains its reader to ignore it. Now: side wires arm at n >= 100 per side (5 %
+unchanged); the ratio (2× unchanged) is read at the review point only. Canon:
+OPEN-ITEMS-SOL.md §BOOK-GATE-RECUT-2026-09-11.
+
 RUNS AS ROOT, not botuser as §5b wrote it: /root is 0700, so botuser can read neither
 /root/titan-bot/full_report.py nor its .env — the very sender §5b names. Same reason
 turn_report_watchdog and report_due live in root's crontab.
@@ -54,7 +64,8 @@ SENDER_DIR = "/root/titan-bot"
 ANCHOR = "2026-09-11 05:40:08"
 REVIEW_N = 200
 REVIEW_DATE = "2026-10-11"
-WIRE_MIN_N = 50
+SIDE_WIRE_MIN_N = 100  # a side wire arms at n >= 100 on that side (re-registered 09-11; was 50)
+RATIO_MIN_N = 50       # the ratio, read at the review point, needs both sides at n >= 50
 WIRE_RATE_PCT = 5      # a side above 5 %
 WIRE_RATIO = 2         # a side ratio above 2×
 EXPECTED = {"LONG": 0.0333, "SHORT": 0.0270}
@@ -97,12 +108,12 @@ def read_counts(db):
 
 # ── exact comparisons: integers, no float edge at 5 % or 2× ──────────────────────────────
 def rate_breached(n, r):
-    return n >= WIRE_MIN_N and r * 100 > WIRE_RATE_PCT * n
+    return n >= SIDE_WIRE_MIN_N and r * 100 > WIRE_RATE_PCT * n
 
 
 def ratio_breached(counts):
     (nl, rl), (ns, rs) = counts["LONG"], counts["SHORT"]
-    if nl < WIRE_MIN_N or ns < WIRE_MIN_N:
+    if nl < RATIO_MIN_N or ns < RATIO_MIN_N:
         return False
     # rate_hi > 2 × rate_lo  ⇔  r_hi·n_lo > 2·r_lo·n_hi   (0 vs >0 is a breach; 0 vs 0 is not)
     return rl * ns > WIRE_RATIO * rs * nl or rs * nl > WIRE_RATIO * rl * ns
@@ -141,8 +152,12 @@ def p_ratio_above(nl, ns):
 
 
 # ── what is due ─────────────────────────────────────────────────────────────────────────
-def due_conditions(counts, now):
-    """{key: reason} of every condition true right now (fired-once filtering is the caller's)."""
+def due_conditions(counts, now, fired=()):
+    """{key: reason} of every condition true right now (fired-once filtering is the caller's).
+
+    The ratio wire is tested ONLY in the review-point pass — the pass in which review_point is
+    due and not yet in `fired` (re-registered 09-11). A failed send marks nothing, so the retry
+    is still the review-point pass and tests the ratio again."""
     out = {}
     total = counts["LONG"][0] + counts["SHORT"][0]
     if total >= REVIEW_N:
@@ -154,11 +169,11 @@ def due_conditions(counts, now):
         n, r = counts[s]
         if rate_breached(n, r):
             out[f"wire_rate_{s}"] = (f"WIRE TRIPPED: {s} {r}/{n} = {_pct(r / n)} is above "
-                                     f"{WIRE_RATE_PCT} % at n {n} >= {WIRE_MIN_N}")
-    if ratio_breached(counts):
+                                     f"{WIRE_RATE_PCT} % at n {n} >= {SIDE_WIRE_MIN_N}")
+    if "review_point" in out and "review_point" not in fired and ratio_breached(counts):
         x, side = ratio_value(counts)
         out["wire_ratio"] = (f"WIRE TRIPPED: side ratio {_x(x)} ({side} higher) is above "
-                             f"{WIRE_RATIO}× with both sides at n >= {WIRE_MIN_N}")
+                             f"{WIRE_RATIO}× at the review point, both sides at n >= {RATIO_MIN_N}")
     return out
 
 
@@ -220,19 +235,25 @@ def format_alert(reasons, counts, now):
         side_line("LONG", nl, rl),
         side_line("SHORT", ns, rs),
         ratio_line,
-        "Wires (pre-registered 09-11, unchanged): above 5 % on a side, or a side ratio above 2× "
-        "→ re-cut the ruler per side and say so. Never loosen quietly.",
+        "Wires (pre-registered 09-11, thresholds unchanged): above 5 % on a side, or a side ratio "
+        "above 2× → re-cut the ruler per side and say so. Never loosen quietly.",
+        "ARMING (re-registered 09-11 by the operator after report 0635 §6): a side wire arms at "
+        "n >= 100 on that side and is checked every 30 min; the ratio wire is tested once, at the "
+        "review point, not continuously.",
         "FALSE-ALARM LINE (0550 §5a): if the registered rates are true, the chance of a false "
         "alarm at the first review, about 100 per side, is LONG 11.7 %, SHORT 5.4 %. A LONG "
         "reading between 5 % and 6 % at the first review is within noise. Nobody re-cuts on "
         "that without reading this line.",
-        # Sequential looks (Monte C., 40 000 paths, seed 20260911, registered rates true,
-        # n equal per side, checked at every evaluation): P(any wire ever trips by noise)
-        # = 0.848 by 100/side (the first review), 0.933 by 540/side (≈ 2026-10-11).
-        "SEQUENTIAL LOOKS: the wires are armed from n = 50 and checked every 30 min, so noise "
-        "alone trips at least one of them before the first review with ≈ 85 % probability, and "
-        "by 2026-10-11 with ≈ 93 % (Monte C., registered rates true). A wire alert is a "
-        "prompt to look, not a finding.",
+        # False-alarm rate OF THIS ARMING — exact (dynamic programming), registered rates true,
+        # n equal per side, every armed wire checked at every evaluation, 2026-10-11 ≈ 540 per
+        # side. The 0635 §6 Monte C. re-run for this arming (40 000 paths, seed 20260911)
+        # gives 44.3 % / 60.3 %. The contract recomputes these from the constants above.
+        "FALSE-ALARM RATE OF THESE WIRES (registered rates true): below n = 100 on a side "
+        "nothing fires from that side, and the ratio is not read before the review point; at the "
+        "review point, about 100 per side, noise alone trips at least one wire 44.5 % of the "
+        "time — the ratio wire alone 37.3 % — and by 2026-10-11 60.2 %. Under the first "
+        "arming (n >= 50, every pass) it was 85 % by the first review and 93 % by 2026-10-11. "
+        "A wire alert is a prompt to look, not a finding.",
     ]
     if noise:
         lines.append(f"Noise at this n, registered rates assumed true: {' · '.join(noise)}.")
@@ -318,7 +339,7 @@ def run(db, state_path, send, now=None, config_path=SOL_CONFIG,
             return 1, (["reader_broken"] if ok else [])
     st.pop("reader_broken", None)
 
-    new = {k: v for k, v in due_conditions(counts, now).items() if k not in fired}
+    new = {k: v for k, v in due_conditions(counts, now, fired).items() if k not in fired}
     out, code = [], 0
     if new:
         text = format_alert(list(new.values()), counts, now)
```

## Appendix B — the Monte C. and the exact computation, as run

`mc.py` is the 0635 method, rebuilt: 40,000 paths, seed 20260911. Run it as `python3 mc.py rng_random old new`.

```python
"""Monte C. of the SOL book-gate review wires — 0635 §6 method, rebuilt.

40 000 paths, seed 20260911, registered rates TRUE (LONG 3.33 %, SHORT 2.70 %), n equal per
side, every wire checked at every evaluation. Integer comparisons exactly as the script:
side  r*100 > 5*n ; ratio  rl*ns > 2*rs*nl  or  rs*nl > 2*rl*ns  (n equal ⇒ rl > 2 rs or rs > 2 rl).

MODE old : side wires armed n>=50, ratio armed n>=50 both sides, checked every evaluation.
MODE new : side wires armed n>=100, ratio tested ONCE, at the review point (100/side = 200).
"""
import sys
import numpy as np

P, N, SEED = 40_000, 540, 20260911
PL, PS = 0.0333, 0.0270
LOOKS = (100, 200, 540)


def draw(variant):
    if variant == "rng_random":
        rng = np.random.default_rng(SEED)
        L = rng.random((P, N)) < PL
        S = rng.random((P, N)) < PS
    elif variant == "rng_binomial":
        rng = np.random.default_rng(SEED)
        L = rng.binomial(1, PL, (P, N)).astype(bool)
        S = rng.binomial(1, PS, (P, N)).astype(bool)
    elif variant == "legacy_rand":
        np.random.seed(SEED)
        L = np.random.rand(P, N) < PL
        S = np.random.rand(P, N) < PS
    elif variant == "rng_random_interleaved":
        rng = np.random.default_rng(SEED)
        U = rng.random((P, N, 2))
        L, S = U[..., 0] < PL, U[..., 1] < PS
    else:
        raise SystemExit(variant)
    return L, S


def wires(L, S):
    rl = np.cumsum(L, axis=1, dtype=np.int32)       # refusals after k evaluations, k = 1..N
    rs = np.cumsum(S, axis=1, dtype=np.int32)
    n = np.arange(1, N + 1, dtype=np.int32)[None, :]
    long_hit = rl * 100 > 5 * n
    short_hit = rs * 100 > 5 * n
    ratio_hit = (rl > 2 * rs) | (rs > 2 * rl)      # n equal on both sides
    return long_hit, short_hit, ratio_hit


def ever_by(hit, arm, look):
    """P(the wire trips at some evaluation k with arm <= k <= look)."""
    if look < arm:
        return np.zeros(hit.shape[0], bool)
    return hit[:, arm - 1:look].any(axis=1)


def table(L, S, mode):
    lh, sh, qh = wires(L, S)
    out = {}
    for look in LOOKS:
        if mode == "old":
            a = ever_by(lh, 50, look); b = ever_by(sh, 50, look); c = ever_by(qh, 50, look)
        else:
            a = ever_by(lh, 100, look); b = ever_by(sh, 100, look)
            c = qh[:, 99] if look >= 100 else np.zeros(P, bool)     # ONCE, at 100/side
        out[look] = (a.mean(), b.mean(), c.mean(), (a | b | c).mean())
    if mode == "new":
        # strictly BEFORE the review pass: k <= 99
        a = ever_by(lh, 100, 99); b = ever_by(sh, 100, 99)
        out["<100"] = (a.mean(), b.mean(), 0.0, (a | b).mean())
    return out


def show(title, t):
    print(title)
    print(f"  {'by n/side':>10} | {'LONG':>6} | {'SHORT':>6} | {'ratio':>6} | {'ANY':>6}")
    for k, (a, b, c, d) in t.items():
        print(f"  {str(k):>10} | {a*100:5.1f}% | {b*100:5.1f}% | {c*100:5.1f}% | {d*100:5.1f}%")


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "rng_random"
    modes = sys.argv[2:] or ["old", "new"]
    L, S = draw(variant)
    for m in modes:
        show(f"[{variant}] mode={m}", table(L, S, m))
```

`dp.py` is the exact computation for both armings. `dp2.py` holds the options and power figures of §4.

```python
"""EXACT (dynamic programming) false-alarm rates of the SOL book-gate review wires.

Same model as the Monte C. of 0635 §6 — registered rates TRUE (LONG 3.33 %, SHORT 2.70 %),
n equal per side, every armed wire checked at every evaluation — but computed exactly, with no
sampling error: P[rl, rs] = probability of the counts AND no wire tripped so far.
"""
import numpy as np
from math import comb

PL, PS = 0.0333, 0.0270


def joint(side_on, ratio_on, looks, n_max):
    """P(at least one wire tripped by k) for k in looks. side_on(k)/ratio_on(k): is it checked at k."""
    size = n_max + 2
    P = np.zeros((size, size)); P[0, 0] = 1.0
    r = np.arange(size)
    RL, RS = np.meshgrid(r, r, indexing="ij")
    ratio_m = (RL > 2 * RS) | (RS > 2 * RL)          # n equal per side
    out = {}
    for k in range(1, n_max + 1):
        Q = P * (1 - PL) * (1 - PS)
        Q[1:, :] += P[:-1, :] * PL * (1 - PS)
        Q[:, 1:] += P[:, :-1] * (1 - PL) * PS
        Q[1:, 1:] += P[:-1, :-1] * PL * PS
        P = Q
        m = np.zeros_like(P, dtype=bool)
        if side_on(k):
            m |= (RL * 100 > 5 * k) | (RS * 100 > 5 * k)
        if ratio_on(k):
            m |= ratio_m
        P[m] = 0.0
        if k in looks:
            out[k] = 1.0 - P.sum()
    return out


def single(p, on, looks, n_max):
    P = np.zeros(n_max + 2); P[0] = 1.0
    r = np.arange(n_max + 2)
    out = {}
    for k in range(1, n_max + 1):
        Q = P * (1 - p); Q[1:] += P[:-1] * p; P = Q
        if on(k):
            P[r * 100 > 5 * k] = 0.0
        if k in looks:
            out[k] = 1.0 - P.sum()
    return out


def ratio_only(on, looks, n_max):
    return joint(lambda k: False, on, looks, n_max)


NEVER = lambda k: False
LOOKS = (99, 100, 200, 540, 1080)
NMAX = 1080


def row(label, side_arm, ratio_on):
    side_on = (lambda k: k >= side_arm) if side_arm else NEVER
    L = single(PL, side_on, LOOKS, NMAX)
    S = single(PS, side_on, LOOKS, NMAX)
    Q = ratio_only(ratio_on, LOOKS, NMAX)
    A = joint(side_on, ratio_on, LOOKS, NMAX)
    print(label)
    print(f"  {'by n/side':>9} | {'LONG':>7} | {'SHORT':>7} | {'ratio':>7} | {'ANY':>7}")
    for k in LOOKS:
        print(f"  {k:>9} | {L[k]*100:6.2f}% | {S[k]*100:6.2f}% | {Q[k]*100:6.2f}% | {A[k]*100:6.2f}%")
    return A


print("== OLD arming (0550 §5b as built): sides n>=50 every pass; ratio both n>=50 every pass")
row("old", 50, lambda k: k >= 50)
print("\n== NEW arming (re-registered 09-11): sides n>=100 every pass; ratio ONCE at review (100/side)")
row("new", 100, lambda k: k == 100)

print("\n== ALTERNATIVES (what else would be needed) — not built")
print("-- A. everything tested ONCE, at the review point (sides and ratio at 100/side)")
row("A", None, NEVER)  # placeholder line to keep table format; real figure below
A = joint(lambda k: k == 100, lambda k: k == 100, (100,), 100)
print(f"   A: any wire at the review point, all at one look: {A[100]*100:.2f}%")
A2 = joint(lambda k: k in (100, 540), lambda k: k == 100, (100, 540), 540)
print(f"   A2: sides at review + at 2026-10-11 (two looks), ratio at review: by review {A2[100]*100:.2f}% · by 10-11 {A2[540]*100:.2f}%")


def pmf(n, p):
    return [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]


def p_ratio_fixed(n):
    A, B = pmf(n, PL), pmf(n, PS)
    return sum(pa * pb for a, pa in enumerate(A) for b, pb in enumerate(B) if a > 2 * b or b > 2 * a)


print("-- B. the 2x ratio read at a later n (binomial, one look):")
for n in (100, 200, 300, 400, 500, 540):
    print(f"   n={n}/side: {p_ratio_fixed(n)*100:.2f}%")


def exact_test_reject(a, b, alpha=0.05):
    """Conditional exact test of the side split, H0 = the registered rates (n equal):
    a | a+b ~ Bin(a+b, pi0), pi0 = PL/(PL+PS). Two-sided, alpha/2 per tail."""
    T = a + b
    if T == 0:
        return False
    pi0 = PL / (PL + PS)
    f = pmf(T, pi0)
    hi = sum(f[a:])
    lo = sum(f[:a + 1])
    return hi <= alpha / 2 or lo <= alpha / 2


def fixed_look(n, ratio_rule, sides=True, pl=PL, ps=PS):
    A, B = pmf(n, pl), pmf(n, ps)
    t = 0.0
    for a, pa in enumerate(A):
        for b, pb in enumerate(B):
            hit = ratio_rule(a, b) or (sides and (a * 100 > 5 * n or b * 100 > 5 * n))
            if hit:
                t += pa * pb
    return t


two_x = lambda a, b: a > 2 * b or b > 2 * a
print("-- C. ratio by an exact conditional test (alpha 5 %) instead of 'above 2x', at the review (100/side):")
print(f"   ratio alone: 2x rule {fixed_look(100, two_x, sides=False)*100:.2f}% · exact test {fixed_look(100, exact_test_reject, sides=False)*100:.2f}%")
print(f"   any wire at the review, sides at one look: 2x {fixed_look(100, two_x)*100:.2f}% · exact test {fixed_look(100, exact_test_reject)*100:.2f}%")
print("-- power, the 08-14 breach as truth (LONG 3.53 %, SHORT 0.62 %, 5.67x), ratio alone at 100/side:")
print(f"   2x rule {fixed_look(100, two_x, sides=False, pl=0.0353, ps=0.0062)*100:.2f}% · exact test {fixed_look(100, exact_test_reject, sides=False, pl=0.0353, ps=0.0062)*100:.2f}%")
print("-- power, a true 2.5x split (LONG 5.0 %, SHORT 2.0 %), ratio alone at 100/side:")
print(f"   2x rule {fixed_look(100, two_x, sides=False, pl=0.05, ps=0.02)*100:.2f}% · exact test {fixed_look(100, exact_test_reject, sides=False, pl=0.05, ps=0.02)*100:.2f}%")
```

```python
"""Exact figures for what ELSE would be needed — options NOT built, for the operator.
Same model as dp.py (registered rates true, n equal per side, checks at every evaluation)."""
import numpy as np
from math import comb

PL, PS = 0.0333, 0.0270


def joint(side_on, ratio_on, looks, n_max, pl=PL, ps=PS):
    size = n_max + 2
    P = np.zeros((size, size)); P[0, 0] = 1.0
    r = np.arange(size)
    RL, RS = np.meshgrid(r, r, indexing="ij")
    ratio_m = (RL > 2 * RS) | (RS > 2 * RL)
    out = {}
    for k in range(1, n_max + 1):
        Q = P * (1 - pl) * (1 - ps)
        Q[1:, :] += P[:-1, :] * pl * (1 - ps)
        Q[:, 1:] += P[:, :-1] * (1 - pl) * ps
        Q[1:, 1:] += P[:-1, :-1] * pl * ps
        P = Q
        m = np.zeros_like(P, dtype=bool)
        if side_on(k):
            m |= (RL * 100 > 5 * k) | (RS * 100 > 5 * k)
        if ratio_on(k):
            m |= ratio_m
        P[m] = 0.0
        if k in looks:
            out[k] = 1.0 - P.sum()
    return out


def pmf(n, p):
    return [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]


def p_side(n, p):
    return sum(v for k, v in enumerate(pmf(n, p)) if k * 100 > 5 * n)


def p_ratio(n, pl, ps):
    A, B = pmf(n, pl), pmf(n, ps)
    return sum(a_ * b_ for a, a_ in enumerate(A) for b, b_ in enumerate(B) if a > 2 * b or b > 2 * a)


L = (100, 540)
opts = {
    "NEW (built): sides >=100 every pass, ratio once at review":
        (lambda k: k >= 100, lambda k: k == 100),
    "D: sides >=100 every pass, ratio once at 2026-10-11 (540/side)":
        (lambda k: k >= 100, lambda k: k == 540),
    "E: sides at two looks (review, 10-11), ratio once at 10-11":
        (lambda k: k in (100, 540), lambda k: k == 540),
    "F: sides at review only, ratio once at 10-11":
        (lambda k: k == 100, lambda k: k == 540),
    "A2: sides at two looks (review, 10-11), ratio once at review":
        (lambda k: k in (100, 540), lambda k: k == 100),
}
for name, (s_on, q_on) in opts.items():
    r = joint(s_on, q_on, L, 540)
    print(f"{name}\n   noise, any wire: by review {r[100]*100:.2f} %  ·  by 2026-10-11 {r[540]*100:.2f} %")

print("\nPOWER (one look, binomial) — what each reading catches if the truth is NOT the registration:")
for n in (100, 540):
    print(f"  n={n}/side  side >5 % if the true rate is 7 %: {p_side(n, 0.07)*100:.1f} %  ·  10 %: {p_side(n, 0.10)*100:.1f} %")
for n in (100, 540):
    print(f"  n={n}/side  ratio >2x if the truth is 2.5x (5.0 %/2.0 %): {p_ratio(n, 0.05, 0.02)*100:.1f} %"
          f"  ·  5.67x (3.53 %/0.62 %, the 08-14 breach): {p_ratio(n, 0.0353, 0.0062)*100:.1f} %"
          f"  ·  noise (registered 1.23x): {p_ratio(n, PL, PS)*100:.1f} %")
```
