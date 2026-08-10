# sol-the-book-enters-the-entry-decision

_2026-08-10 18:30 UTC_

---

# DESIGN + DIFF. NOTHING APPLIED. **The book has never taken any part in the entry decision — and the one gate that would have used it is dead, has never fired once, and reads the wrong venue.**

```
📕 book_gate.py           NEW, 202 lines      🔴 NOT IN PRODUCTION
   config.py              +54  −0
   main.py                +100 −0             (runs BEFORE the advisor)
   skip_attribution.py    +6   −1             ONE deleted line in the whole design
HARNESS: 28 assertions ✅  0 ❌  LEAKS 0  — 20 vectors rewritten BY DIRECTORY,
         the REAL evaluate() replayed over all 3,454 stored OKX-4000 books
🔴 vpos 32 SHORT is OPEN — the rule WOULD REFUSE IT. Stated, not acted on.
```

Prior: [18:00 — three lying comments corrected](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-10-1800-sol-three-lying-comments-corrected-and-five-things-recorded.md)

---

## 0. 🔴 THE CORRECTION, RECORDED FIRST SO IT IS NOT MADE A FOURTH TIME

You asked for the book in the entry decision. **Three times I answered a different
question — "does the book yield a statistical edge?" — and refused the rule on the answer.**
Filter 21, filter 22, and the wall band at Fisher p=1.0000 on n=396 are all answers to a
question you did not ask.

**The question is why the book takes no part in the decision at all.** *Do not buy into a wall*
and *do not enter where there is nothing to enter into* are discipline, like *do not buy against
the higher timeframe*. **The bar is calibration, not significance** — and calibration is
answerable from 24,182 rendered walls even where edge is not.

**Everything below is built to that bar.** No outcome is consulted anywhere in §1 or §2. Outcomes
appear only in §3, and only to check that the rule does not refuse winners.

### And the premise checks out — the book really is absent

```
main.py  "OKX wall avoidance filter"        <- reads BYBIT liquidity_zones clusters,
config.py  WALL_AVOIDANCE_ENABLED = False      NOT the OKX-4000 book the advisor gets
           A2 2026-06-08: "Titan parity — walls advisory-only, NO hard block"

SELECT COUNT(*) FROM trades WHERE status='wall_blocked'   ->   0
                                                        ^^^ never, in 63 days
```

**The one wall gate in the entry path is switched off, has fired zero times in this bot's entire
history, and was pointed at a different venue's book than the one the advisor reads.** The
OKX-4000 snapshot is fetched, rendered into the prompt, stored — and read by no branch.

---

## 1. CALIBRATION

### 🔴 (0) THE SHAPE GUARD — and my own first pass being wrong

`trades.orderbook_json` **holds two different objects**:

```
refused rows   {mid, imbalance, walls_bid, walls_ask, depth, wall_threshold_mult}  ← OKX-4000
EXECUTED rows  {top_bids, top_asks, spread, bid_vol_band, imbalance_band_pct, …}   ← Bybit depth-20
               OVERWRITTEN AT FILL by microstructure.capture_and_persist_sync
```

**My first calibration read the column by name and reported "24 of 26 positions refused".** That
number was an artefact of asking a depth-20 Bybit snapshot for OKX walls it never contained. Every
row below is accepted only if it carries `wall_threshold_mult` **and** `depth`.

```
rows offering a book column : 3,482
ACCEPTED as OKX-4000        : 3,454      LONG 1,545 / SHORT 1,909
REJECTED by the shape guard :    28      all of them status='executed'
🔴 WALLS RENDERED           : 24,182     window 2026-06-08 .. 2026-08-10
```

### (a) The nearest OPPOSING wall at decision time — per side

| | n | D1 | Q1 | MED | Q3 | D9 | P95 | P99 | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **LONG** mult | 1,545 | 10.30 | 12.30 | **14.60** | 17.10 | 19.10 | 20.40 | 23.50 | 26.10 |
| **LONG** distance % | 1,545 | 0.08 | 0.20 | **0.36** | 0.51 | 0.61 | 0.65 | 0.73 | 0.79 |
| **LONG** distance ATR(1h) | 1,524 | 0.11 | 0.25 | **0.45** | 0.67 | 0.92 | 1.05 | 1.42 | 1.82 |
| **SHORT** mult | 1,909 | 11.60 | 14.00 | **16.80** | 20.00 | 23.70 | 25.80 | 29.40 | 33.30 |
| **SHORT** distance % | 1,909 | 0.08 | 0.19 | **0.35** | 0.52 | 0.61 | 0.65 | 0.70 | 0.75 |
| **SHORT** distance ATR(1h) | 1,882 | 0.10 | 0.24 | **0.47** | 0.70 | 0.98 | 1.13 | 1.42 | 1.66 |

**100.0 % of signals have an opposing wall.** There is always something in the way; the only
question is how big and how close.

### (b) Liquidity leaning toward the proposed side — and the honest answer to "nothing to enter into"

| | n | min | p1 | p2 | D1 | MED | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| **LONG** lean | 1,545 | 0.3668 | 0.4251 | **0.4323** | 0.4628 | 0.5104 | 0.69 |
| **SHORT** lean | 1,909 | 0.3431 | 0.3986 | **0.4129** | 0.4460 | 0.4939 | 0.61 |

```
supporting-wall COUNT:   LONG min 1, D1 2, MED 3      SHORT min 1, D1 2, MED 3
🔴 n_supporting == 0 :   0 of 1,545 LONG    0 of 1,909 SHORT    — NEVER, not once
```

🔴 **"There is nothing to enter into" NEVER HAPPENS on this instrument at OKX-4000 depth.** The
literal form of your clause (b) is a **no-op**, and I am telling you that rather than inventing a
threshold to make it fire. What *does* vary is the **lean**, and SOL's book is persistently
bid-heavy — LONG median lean 0.510 against SHORT 0.494 — which is why a single fixed floor would
be a short-ban. The clause is therefore cut **per side, at each side's own 2nd percentile.**

### (c) 🔴 THE RATE — and the ruler that would have made this a side ban

The advisor's percentile scale (`claude_advisor._WALL_MULT_PCTL_BREAKS`) is cut from **every wall
it has ever rendered**. The rule tests **one** wall — the nearest opposing one — a strictly
stronger subpopulation:

```
LONG   median nearest-opposing wall  x14.6  ->  the advisor's ruler calls it p80
SHORT  median nearest-opposing wall  x16.8  ->  the advisor's ruler calls it p87
```

🔴 **"Above p85" is not "unusually big". On a SHORT it is BELOW TYPICAL.** The refusal rates
prove it:

| ruler | threshold | LONG refused | SHORT refused | ratio |
|---|---|---:|---:|---:|
| **advisor's** (all rendered walls) | p≥85, D≤0.20 % | 3.6 % | **12.1 %** | **3.4×** |
| **self-calibrated** (nearest-opposing, this side) | p≥90, D≤0.20 % | 0.3 % | 0.7 % | 2.2× |

**A 3.4× side asymmetry produced by the RULER, not by the market — that is the EMA envelope's
failure mode exactly** (0 of 9 LONGs refused: a side ban wearing an indicator's name). The design
therefore carries its own side-conditional breakpoints and says so in the source.

**The full rate grid, self-calibrated ruler, no outcome consulted:**

```
              D<=0.10%  D<=0.15%  D<=0.20%  D<=0.25%  D<=0.30%
  LONG  p>=85    0.1%      0.5%      0.6%      2.4%      4.3%
  LONG  p>=90    0.0%      0.1%      0.3%      0.8%      2.2%
  SHORT p>=85    0.3%      0.6%      1.1%      3.2%      6.4%
  SHORT p>=90    0.1%      0.4%      0.7%      1.9%      4.3%
```

---

## 2. THE RULE — two clauses, flagged separately

```python
A  WALL-AVOIDANCE     side-conditional pctl of the nearest opposing wall >= 90
                      AND its distance <= 0.20 % of mid          (BOTH required)
B  LIQUIDITY-PRESENCE n_supporting < 1   OR   lean < p2 for THIS side
                      (LONG 0.4323, SHORT 0.4129)
```

**Both conditions are required in A on purpose.** A ×25 wall 0.6 % away is not in the way; a ×6
wall 0.05 % away is not a wall. Only *big AND close* is what a trader refuses.

**Measured on 3,454 signals — the numbers that decide whether this is discipline or a ban:**

| | n | clause A | clause B | BOTH | **EITHER** |
|---|---:|---:|---:|---:|---:|
| LONG | 1,545 | 4 (0.26 %) | 29 (1.88 %) | 1 | **34 = 2.20 %** |
| SHORT | 1,909 | 14 (0.73 %) | 35 (1.83 %) | 2 | **51 = 2.67 %** |

🔴 **Side ratio 1.21× — read the symmetry, not the level.** That is what "a rule, not a side ban"
looks like numerically, and it is the single number that would have killed this design if it had
come out at 3.4×.

**(c) They are separable and separately flagged.** They overlap on **3 signals out of 3,454**. The
card, the DB column and the JSON response all name `A`, `B` or `AB`, so one clause can be judged
without the other.

### (d) 🔴 WHERE IT SITS, AND WHY THERE

```
HTF cascade ─▶ score gate ─▶ entry lock ─▶ risk gate ─▶ fee gate ─▶ dead wall gate
                                                                          │
                                    _pre_walls = fetch_pre_trade_walls()  ◀── the book arrives
                                                                          │
                                       🔴 BOOK GATE  ◀── HERE (main.py, +85 lines)
                                                                          │
                                       claude_advisor.consult_for_entry() ◀── the advisor
                                                                          │
                                                                        order
```

- **It cannot be earlier** — there is no book before the fetch on the line above it.
- **It must be before the advisor.** Four of four checkable book claims the advisor has made were
  **false, all erasing opposing structure**; its verdict is independent of the wall band
  (p=1.0000, n=396); it cites the calibrated percentile in **6.6 %** of reasons while its own
  prompt calls that figure primary. **A model that cannot read a wall must never get the chance
  to trade through one.** After the advisor, the rule would be a second-guesser instead of a
  precondition.
- **It reads the SAME `_pre_walls` object the advisor is handed on the next line.** One fact, one
  snapshot — the gate and the prompt can never disagree about what the book was. That is the
  `one-fact-many-judges` defect class this bot keeps closing.
- **Cheapest-last, expensive-first**: everything above it has already passed, so it costs nothing
  on the common path and it **saves the ~5 s Claude call** on what it refuses.
- **Inside the `_entry_gate` lock**, so a refusal returns through the existing `finally` release.

---

## 3. WHAT WOULD IT HAVE DONE — both directions, honestly

### 🔴 (a) ONLY 6 OF 26 POSITIONS CAN BE JUDGED AT ALL

```
vpos  7 .. 26   (20 positions, 2026-06-14 .. 2026-08-02)   🔴 NO OKX BOOK STORED
vpos 27, 28, 29, 30, 31, 32                                 judgeable
```

`advisor_book_json` was added **2026-08-02**. Before it, the only book column on an executed row
was `orderbook_json` — **overwritten at fill by the depth-20 microstructure capture.** *The column
that would answer "what did the book look like when we entered?" is destroyed for exactly the rows
that became positions.* That is §4's first requirement, and it is why the design stores **columns,
not a blob**.

| vpos | date | book | side | R | oppMult | sp | dist % | nSup | lean | verdict |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 27 | 08-03 | paper | SHORT | −0.660 | 30.6 | 99 | 0.345 | 2 | 0.493 | ✅ admit |
| 28 | 08-06 | paper | SHORT | −0.153 | 19.1 | 68 | 0.041 | 3 | 0.425 | ✅ admit |
| 29 | 08-08 | 🔴LIVE | LONG | **+1.355** | 10.6 | 12 | 0.629 | 5 | 0.485 | ✅ admit |
| 30 | 08-08 | 🔴LIVE | LONG | **+0.762** | 6.3 | 1 | 0.590 | 7 | 0.501 | ✅ admit |
| 31 | 08-10 | 🔴LIVE | LONG | −1.155 | 14.4 | 47 | 0.390 | 5 | 0.524 | ✅ admit |
| 32 | 08-10 | 🔴LIVE | SHORT | **OPEN** | 13.1 | 17 | 0.538 | 6 | **0.343** | 🔴 **REFUSE (B)** |

**🔴 IT REFUSES NO WINNER.** Both live winners (+1.355R, +0.762R) are admitted, and admitted
*comfortably* — vpos 29's nearest opposing wall is at **p12** for its side and 0.629 % away; vpos
30's is at **p1**. Filter 21 died because it refused the winners; **this does the opposite, and
that check was run before anything else in §3.**

### 🔴 (b) vpos 31 IS ADMITTED AND STILL LOST — exactly as you predicted

You said: *"vpos 31's book was BID-HEAVY with a ×17.4 bid wall under the entry, so a wall rule
should ADMIT it and it still lost. Say that plainly if so."*

**Plainly: yes.** vpos 31's lean is **0.524 toward the LONG**, its nearest opposing wall sits at
**p47** for its side — dead median — and **0.390 % away, past every candidate distance threshold.**
The rule admits it without hesitation, and it stopped out at **−1.155R**. *This rule would not
have saved today's loss and does not claim to.*

### 🔴 (b2) AND IT WOULD REFUSE THE POSITION THAT IS OPEN RIGHT NOW

```
vpos 32  SHORT  1.3 @ 76.18  SL 77.32  — OPEN on real money since 15:15:33

  clause B: book leans 0.343 toward the short side  (< 0.4129 = p2 for SHORT)
  🔴 that lean is the MINIMUM of all 1,909 SHORT signals ever scored — percentile 0.00
```

The book is **65.7 % bid** and the bot sold into it. Whatever else is true, *selling into the
heaviest bid support seen in 63 days* is the case this rule exists for. **NOTHING WAS DONE ABOUT
IT** — the position is untouched, its stop is untouched, nothing was restarted. It is your call.

### (c) The volume cost

```
🔴 'executed' contains 33 rows with side='na' — those are CLOSE rows, not entries.
   The honest entry figures:

   positions opened   26 over 58 days  =  0.448/day     ← use this
   entries (executed) 25 over 58 days  =  0.431/day
   LIVE ERA            4 over 2.77 days = 1.44/day

   LONG   0.1897/day  −2.20 %  ->  0.1855/day
   SHORT  0.2414/day  −2.67 %  ->  0.2352/day
   TOTAL  0.4310/day          ->  0.4207/day   (−0.0104/day ≈ 1 refusal every 96 days)
```

🔶 **I could not reproduce your 0.79/day** and am not adopting it silently — my figures and their
provenance are above. **And the tension is stated rather than smoothed:** the signal-level rate
says one refusal every ~96 days, while the (tiny) position-level sample refuses **1 of 6**. n=6
cannot resolve that. At the live-era entry rate the first refusal would land in ~29 days.

### 🔴 (d) WHAT THIS RULE CANNOT CLAIM

**It cannot claim it improves outcomes.** The book has been measured against outcomes on this
instrument three times and does not separate them. This sentence is not in the report only — it is
in the config, in the module docstring, and worded so it cannot be read as a proven edge:

```python
# 🔴 THIS IS TRADING DISCIPLINE. IT IS NOT A MEASURED EDGE, AND THE DAY A FUTURE
# SESSION READS IT AS ONE IS THE DAY IT GETS TUNED INTO SOMETHING ELSE.
#     · filter 21 (wall band)      — REFUSED, it refused the winners
#     · filter 22 (book liquidity) — REFUSED
#     · advisor-vs-book independence — Fisher p = 1.0000 on n = 396
# This gate exists because a bot that sells into a bid wall is doing something a
# trader would not do. Its bar is CALIBRATION … NOT statistical significance.
# IF A LATER PASS MEASURES IT AND FINDS NO EDGE, THAT IS THE EXPECTED RESULT AND
# IS NOT A REASON TO REMOVE IT. The reasons to remove it are: it fires too often,
# it fires asymmetrically, or it refuses trades a trader would take.
```

---

## 4. OBSERVABILITY FROM DAY ONE

| | requirement | how |
|---|---|---|
| **(a)** | its own DB status | `status='book_blocked'` + **six columns on EVERY scored row, admitted or refused** — `book_gate_clause`, `_opp_mult`, `_opp_pctl`, `_opp_dist_pct`, `_lean`, `_n_supporting`. 🔴 **Columns, not a JSON blob** — a blob is what got overwritten at fill and cost us 20 of 26 judgeable positions. |
| **(b)** | a Telegram card on refusal | names the wall, its **side-conditional** percentile, its distance, **which clause fired**, the wall line, and the sentence *"discipline rule, not a measured edge"*. |
| **(c)** | registered with `skip_attribution` | `'book_blocked'` added to `TRACKED_STATUSES` **in the same pass as the gate** — the FLAT floor's 518 refusals were invisible for a month on Titan because the refusal path never called the hook. Drift accrues from refusal #1. |
| **(d)** | kill switch + the reasoning | `BOOK_GATE_ENABLED` (stops it computing) **and** `BOOK_GATE_DRYRUN=True` — it **ships unable to block**, logging + carding + filling columns only. §3d's paragraph is in the comment. |

---

## THE DIFF — 🔴 SHOWN, NOT APPLIED

```
book_gate.py          NEW  +202  −0     does not exist in production
config.py                  +54   −0
main.py                    +100  −0
skip_attribution.py        +6    −1
                          ────────
TOTAL                      +362  −1     🔴 exactly ONE deleted line in the entire design
```

**The one deletion, in full:**

```diff
-TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked', 'risk_halt')
+TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked', 'risk_halt',
+                    'book_blocked')
```

### `main.py` — the gate itself (abridged; full text in the harness record)

```diff
+        # ── 🔴 BOOK GATE — THE ORDER BOOK DECIDES, BEFORE THE ADVISOR DOES ────
+        try:
+            _book_verdict = book_gate.evaluate(_pre_walls, direction)
+        except Exception as _bg_err:
+            print(f"{LOG_PREFIX}[BOOK-GATE] evaluate failed (non-fatal, ADMITTING) "
+                  f"row={row_id}: {type(_bg_err).__name__}: {_bg_err}", flush=True)
+            _book_verdict = {'refuse': False, 'clause': None, ...}
+        _bf = _book_verdict.get('facts') or {}
+        update_trade(row_id,
+                     book_gate_clause=(_book_verdict.get('clause') or ''),
+                     book_gate_opp_mult=_bf.get('opp_mult'),
+                     book_gate_opp_pctl=_bf.get('opp_pctl'),
+                     book_gate_opp_dist_pct=_bf.get('opp_dist_pct'),
+                     book_gate_lean=_bf.get('lean'),
+                     book_gate_n_supporting=_bf.get('n_supporting'))
+        if _book_verdict.get('refuse'):
+            print(f"{LOG_PREFIX}[BOOK-GATE] {'DRYRUN would-refuse' if BOOK_GATE_DRYRUN else 'REFUSE'} …")
+            if not BOOK_GATE_DRYRUN:
+                update_trade(row_id, status='book_blocked', …)
+                _record_skip_attribution(row_id, symbol, direction, 'book_blocked', …)
+                send_tg(f"📕 <b>BOOK REFUSED ENTRY</b> (clause {_book_verdict['clause']})\n…")
+                return jsonify({'status': 'book_blocked', …}), 200
+
         _combo_weight = signal_weights.get_weight(combo)
```

**Note the shape of the refusal**: the columns are written **before** the DRYRUN branch, so the
gate's inputs accrue on every row from day one **even while it cannot block anything.**

---

## PROOF BY EXECUTION — 28 ✅ / 0 ❌, SEARCHED BY DIRECTORY

```
LAB: full tree copy + the design applied; every PRODUCTION-DIRECTORY literal rewritten.
  20 VECTORS rewritten by DIRECTORY grep    residual prod-path literals: 0
LOCK before the first import: sqlite3.connect + open(w/x/a/+) raise on PROD or /root/titan-bot
```

```
✅ 🔴 BOOK_GATE_DRYRUN = True — ships unable to block
✅ the OLD wall gate stays False — two wall gates are never both live

── THE SHAPE GUARD, on real and synthetic input ──
✅ read_book(Bybit depth-20 snapshot) -> None (refuses to guess)
✅ FAIL-OPEN on None / empty dict / a string / mid=0 — every one ADMITS
✅ 🔴 replayed over 3,454 real OKX books + 28 real Bybit books:
     it refused ZERO non-OKX books — the guard held on production data

── THE RULER ──
✅ median LONG x14.6 -> p50 NEW ruler   (advisor ruler says p80)
✅ median SHORT x16.8 -> p50 NEW ruler  (advisor ruler says p87)
✅ the same x18.0 ranks LONG p82 vs SHORT p60 — that IS the correction
✅ unrankable multiplier -> None, and None never refuses

── THE RATE, from the REAL evaluate() ──
   LONG   n=1545  A 4 (0.26%)  B 29 (1.88%)  AB 1  REFUSE 2.20%
   SHORT  n=1909  A 14 (0.73%) B 35 (1.83%)  AB 2  REFUSE 2.67%
✅ both sides under the 5 % "rule not ban" ceiling
✅ 🔴 SIDE SYMMETRY 1.21x  (the advisor's ruler gives 3.4x, which is a side ban)

── SEPARABILITY ──
✅ big+close wall -> clause A ONLY   ✅ hard lean -> clause B ONLY   ✅ clear book -> admits

── THE OPEN POSITION ──
✅ vpos 32 -> REFUSE, clause B: "book leans 0.343 against this side (< 0.413 = p2 for SHORT)"

── NOTHING APPLIED ──
✅ main.py / config.py / skip_attribution.py: LAB differs from PRODUCTION
✅ 🔴 book_gate.py does NOT exist in production
✅ 🔴 /root/titan-bot git-CLEAN at 897850b — NOT TOUCHED
✅ LEAKS: 0
```

---

## STATE

```
mercury-sol   active · master 4059454 / worker 4059524 · since 2026-08-09 18:42:12 · NRestarts=0
              NOT restarted · NOT edited · no order placed · no stop moved
🔴 vpos 32    OPEN · SHORT 1.3 @ 76.18 · SL 77.32 · is_paper=0 · UNTOUCHED
              (the rule would refuse it — SAID, NOT DONE)
production    book_gate.py absent · config.py / main.py / skip_attribution.py unchanged
              (md5 identical to this morning's post-comment state)
design        lives only in the scratchpad lab; +362 / −1 across 4 files
db            file:trades.db?mode=ro for every query
titan         HEAD 897850b · git clean · NOT TOUCHED
```

**The map is drawn and the diff is on the table. It lands when you say so.**
