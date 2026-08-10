# sol-three-lying-comments-corrected-and-five-things-recorded

_2026-08-10 18:00 UTC_

---

# APPLIED. Three comments that said the opposite of the code are corrected, each carrying the 63-day lag as the lesson. **No behaviour changed, and it is proved rather than asserted.**

```
AST:      25 assertions ✅  0 ❌   — config.py and main.py module ASTs BYTE-IDENTICAL;
                                    macro_filter.py identical with docstrings stripped
HARNESS:  19 assertions ✅  0 ❌   LEAKS: 0   — 20 vectors rewritten BY DIRECTORY
DELETED:  9 lines, all 9 listed individually below — they ARE the three false blocks
🔴 NOT RESTARTED — vpos 32 SHORT is OPEN on real money since 15:15:33
```

Prior: [17:30 — the news adjustment is in the gate and it is a clock](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-10-1730-sol-the-news-adjustment-is-in-the-gate-and-it-is-a-clock.md)
(§1e and §6 point 8 are what this pass discharges)

---

## 🔴 THE MACRO ADJUSTMENT STAYS IN THE GATE — recorded before anything else

Nothing in this pass touches it, and the canon now says why in the file a future session will read:

> Removal admits the **274** signals it currently refuses, whose outcomes **do not exist and cannot
> be computed at any sample size**; against that, the term has built **exactly one position** in
> this bot's history (vpos 25, paper, +1.257R). The measurable half of the diff is −1.257R of paper.
> **That is not a case for either side.**

---

## 1. THE THREE LYING COMMENTS — corrected, with the lag recorded at each site

**Every one of the 9 deleted lines, listed individually — they are the three false blocks and
nothing else:**

```
[config.py] 3 deleted
< # MACRO_GATE_DRYRUN: Mercury-SOL ships this gate in DRYRUN — build_macro_context
< # is computed, logged, and persisted to trades.db, but the would-be adjustment
< # is NOT applied at the score gate. Flip to False to apply it (Titan behaviour).

[main.py] 2 deleted
<     # fetches are TTL-cached; every branch fails open. weighted_adj remains
<     # STORAGE-ONLY — the score gate still uses raw direction_score (gate UNCHANGED).

[macro_filter.py] 4 deleted
< Mercury-SOL wiring: the gate adjustment is computed and logged behind
< MACRO_GATE_DRYRUN (config). In DRYRUN it does NOT modify the entry gate — the
< would-be adjustment is logged + persisted only. Flip MACRO_GATE_DRYRUN=False to
< apply it at the score gate (matching Titan).
```

### (a) `config.py`, above `MACRO_GATE_DRYRUN` — **+22 / −3**

```diff
-# MACRO_GATE_DRYRUN: Mercury-SOL ships this gate in DRYRUN — build_macro_context
-# is computed, logged, and persisted to trades.db, but the would-be adjustment
-# is NOT applied at the score gate. Flip to False to apply it (Titan behaviour).
+# 🔴 MACRO_GATE_DRYRUN IS False: THE ADJUSTMENT IS APPLIED AT THE ENTRY GATE.
+# `main.py`'s score gate (symbol `_gate_score`; :4395 as of 2026-08-10 — anchor on
+# the SYMBOL, line numbers rot) reads
+#     _gate_score = direction_score if MACRO_GATE_DRYRUN else _macro_gated_score
+# so with DRYRUN False the quantity compared against CONFLUENCE_SCORE_THRESHOLD is
+# `_macro_gated_score` = direction_score + macro_filter total_gate_adj. A crypto-news
+# category of ±1.0 is 50 % of the 2.0 threshold and it flips real verdicts: measured
+# 2026-08-10, 487 of 5,355 scored signals (9.1 %) land on opposite sides of the bar on
+# the raw vs the adjusted score.
+#
+# 🔴 THE COMMENT THAT USED TO STAND HERE SAID THE OPPOSITE, FOR 63 DAYS.
+# It read "Mercury-SOL ships this gate in DRYRUN … the would-be adjustment is NOT
+# applied at the score gate". That was true until A7 flipped the flag on 2026-06-08;
+# the flag moved and the three comments describing it (here, main.py's "Pre-gate
+# enrichment" block, `macro_filter.py`'s module docstring) did not. Corrected
+# 2026-08-10 — 63 days late.
+# THE LAG IS THE LESSON, NOT THE WORDING: on 2026-08-08 a live-money conclusion was
+# asserted from reading one assignment line without reading the comparison line, and
+# the prose at each of these three sites would have confirmed the wrong answer. A
+# comment is not evidence about behaviour. Verify a gate against the comparison
+# expression and against the stored verdicts, never against the prose beside it.
+# Report: reports/2026-08-10-1730-sol-the-news-adjustment-is-in-the-gate-and-it-is-a-clock.md
 MACRO_GATE_DRYRUN           = False   # A7 2026-06-08: apply macro penalty at gate (Titan parity)
```

### (b) `main.py`, the "Pre-gate enrichment" block — **+24 / −2**

The old clause was **right about `weighted_adj` and wrong about the gate, in one sentence** — which
is why it survived: the half a reader could check was true.

```diff
-    # fetches are TTL-cached; every branch fails open. weighted_adj remains
-    # STORAGE-ONLY — the score gate still uses raw direction_score (gate UNCHANGED).
+    # fetches are TTL-cached; every branch fails open.
+    #
+    # 🔴 TWO ADJUSTMENTS ARE BUILT BELOW AND ONLY ONE OF THEM GATES. Do not read
+    # them as one number — the entry card prints both, adjacent, and they have
+    # been confused for each other:
+    #   weighted_adj (`_w_adj`)  — STORAGE-ONLY. Clipped ±1.5, stored as
+    #       confluence_score, shown on the card as "adj ±X.XX⚖️". It appears in
+    #       NEITHER branch of the gate expression. Measured 2026-08-08.
+    #   macro total_gate_adj (`_macro_gate_adj`) — 🔴 THIS ONE GATES.
+    #       MACRO_GATE_DRYRUN is False (config.py), so the gate compares
+    #       `_macro_gated_score` = direction_score + _macro_gate_adj.
+    # Anchors are the SYMBOL NAMES, not line numbers — this very edit moved the
+    # gate expression from 4373 to 4395, and a stale line cite rots exactly the
+    # way the stale prose below did. As of 2026-08-10: _macro_gate_adj :4255,
+    # _w_adj :4286, the gate `if _gate_score < _thr` :4395-4396.
+    #
+    # 🔴 THIS COMMENT USED TO END "the score gate still uses raw direction_score
+    # (gate UNCHANGED)". That clause was FALSE from 2026-06-08, when A7 flipped
+    # MACRO_GATE_DRYRUN to False, until it was corrected on 2026-08-10 — 63 days.
+    # It was right about weighted_adj and wrong about the gate, and it read as one
+    # claim. THE LAG IS THE LESSON: three comments in three files all described the
+    # pre-flip behaviour, so "is macro in the gate?" answered by reading prose
+    # returned NO three times while the code had been answering YES for two months.
+    # Report: reports/2026-08-10-1730-sol-the-news-adjustment-is-in-the-gate-and-it-is-a-clock.md
```

### (c) `macro_filter.py`, the module docstring — **+17 / −4**

```diff
-Mercury-SOL wiring: the gate adjustment is computed and logged behind
-MACRO_GATE_DRYRUN (config). In DRYRUN it does NOT modify the entry gate — the
-would-be adjustment is logged + persisted only. Flip MACRO_GATE_DRYRUN=False to
-apply it at the score gate (matching Titan).
+🔴 Mercury-SOL wiring: THE GATE ADJUSTMENT IS LIVE AT THE ENTRY GATE.
+MACRO_GATE_DRYRUN is False (config.py), so main.py's score gate — the `_gate_score`
+comparison, :4395 as of 2026-08-10, but anchor on the SYMBOL, line numbers rot — compares
+direction_score + total_gate_adj against CONFLUENCE_SCORE_THRESHOLD. total_gate_adj
+is crypto_gate_adj + macro_gate_adj — note that DXY is NOT a term in it: dxy_value
+and dxy_trend are fetched, stored and displayed, and never summed into the gate.
+
+🔴 THIS PARAGRAPH SAID THE OPPOSITE FOR 63 DAYS. It read "In DRYRUN it does NOT
+modify the entry gate", which stopped being true on 2026-06-08 when A7 flipped the
+flag; the paragraph was corrected on 2026-08-10. Two sibling comments (config.py
+above MACRO_GATE_DRYRUN, main.py's "Pre-gate enrichment" block) lagged the same flip
+by the same 63 days.
+THE LAG IS THE LESSON, NOT THE WORDING — a reader answering "is macro in the gate?"
+from prose got NO from all three sources while the code had been answering YES since
+June. Establish gate behaviour from the comparison expression and from the stored
+verdicts, never from the prose beside it.
+Report: reports/2026-08-10-1730-sol-the-news-adjustment-is-in-the-gate-and-it-is-a-clock.md
```

### 🔴 (d) THE PASS CAUGHT ITSELF CREATING THE NEXT LAG, AND THAT IS RECORDED IN THE CODE

The first version of these comments cited `main.py:4373`. **Adding 18 comment lines above the gate
moved it to 4391; fixing the citation to 4391 added 4 more and moved it to 4395.** A line cite
inside the file it cites is a self-referential fixed point, and it rots for exactly the reason the
prose rotted.

```
iteration 1:  gate at 4373  ->  comments cite 4373        (correct at write time)
iteration 2:  comments added, gate now 4391, cite STALE   <- caught
iteration 3:  cite fixed to 4391, 4 lines added, gate 4395, cite STALE AGAIN  <- caught
iteration 4:  cite fixed to 4395, no lines added          -> FIXED POINT ✅

verified: _macro_gate_adj :4255 ✔   _w_adj :4286 ✔   if _gate_score < _thr :4395-4396 ✔
residual stale cites in the three files: 0
   (the only "4373" left is the sentence "this very edit moved the gate expression
    from 4373 to 4395", which is correct history)
```

**So the comments now anchor on SYMBOL NAMES and say so, with the line numbers marked "as of
2026-08-10".** Two of the three historical cross-references were changed from `main.py:4200` to
"main.py's Pre-gate enrichment block" for the same reason.

---

## 2. RECORDED IN THE CANON — `OPEN-ITEMS-SOL.md`, +130 lines, a new top-level section

Placed **immediately after the LIVE-MONEY header**, above "WHAT WAS KNOWINGLY ACCEPTED AT THE
FLIP", so it is read before anything is touched. All five items are records; **none is a proposal.**

| | recorded | the one sentence that matters |
|---|---|---|
| **(a)** | 🔴 **the instrument mismatch** | the classifier's own prompt says *"classify the broad crypto regime, not SOL-specific noise"* and files **altcoin-specific news → NEUTRAL**. SOL is an altcoin. 153 BTC headlines moved 1,029 signals; 10 SOL headlines moved 50, and all ten qualify on their BTC/TradFi half. **Not evaluable from this book — SOL-specific news has moved the gate twice.** Marked *do not "fix" the prompt on the strength of this note*. |
| **(b)** | **it is a clock** | the full 24-hour table is in the canon: **11.8 % non-zero at 23:00 UTC against 87.6 % at 13:00 — 7.4×**. Recorded consequence: *the effective entry threshold is lower in US/EU hours and higher overnight, for reasons unrelated to price.* |
| **(c)** | `crypto_confidence` **multiplies nothing** | `_CRYPTO_ADJ` is a sign table keyed on category alone; ±1.0 at 0.72 and ±1.0 at 0.95, with the full distribution. Recorded **as a fact, not as a case for weighting** — (d) says the effect is not there to weight. |
| **(d)** | 🔴 **the sign symmetry is the tell** | 21 of 54 cells clear Bonferroni raw → **0 of 54** day-matched, `t=7.96 → t=0.15`. And **`news+` and `news−` drift the SAME WAY** — recorded first, because *a future reader who checks the sign symmetry saves the whole de-confounding pass*. Effective n = **58 DAYS**. |
| **(e)** | 🔴 **the second door** | `macro_news_category` **and** `dxy_trend` are ORIGINAL_6 keys, and **ORIGINAL_6 hard-blocks regardless of `FILTER_ENFORCEMENT_DRYRUN`** — the flag gates only the extension class. `optimizer/filters.json` **does not exist**, so it is inert. Written **beside the apply-guard record** so the two are read together: *the guard that would stop this is the same guard already flagged as resting on an expired premise. Two records, one door.* |

### 🔴 3. AND MY OWN FRAMING IS CORRECTED IN THE CANON WITH THE SAME PROMINENCE AS THE ALARM

It is item **(0)** — *above* all five, under its own red heading, in the section a fresh session
reads first:

```
🔴 (0) MY OWN FRAMING WAS WRONG, AND IT IS RECORDED HERE WITH THE SAME WEIGHT AS THE ALARM

The alarm that opened this work said "one third of the deciding score came from
headlines". It was 18 %, and it did not decide.

    raw direction_score  4.50    ← price. Cleared the 2.0 bar by 2.50 UNAIDED.
    news (STRONG_POS)   +1.00    ← 18 % of the deciding 5.50
    DXY                  0.00    ← DXY IS NOT A TERM IN total_gate_adj AT ALL

… Two adjacent numbers on one card, one of which gates and one of which does not —
that is the trap, and it caught the operator and the assistant on the same day.
The position in question (vpos 31) closed at −1.155R on its own stop.
```

**Written as a property of the card, not as a mistake by a person** — the card puts `adj +1.50⚖️`
(the weight term, outside the gate) and `DXY=… | adj=+1.0pts` (the news term, inside it) within
four lines of each other, and the same misreading landed on both sides of this conversation.

---

## 4. AST — NO FUNCTION CHANGED IN ANY FILE

```
── config.py ──
✅ the file DID change (a no-op edit would be a false pass)
✅ no function/class ADDED or REMOVED (2 defs, added=[] removed=[])
✅ NO function/class BODY changed  changed=[]
✅ 🔴 module AST is BYTE-IDENTICAL — the edit is invisible to the parser
✅ MACRO_GATE_DRYRUN UNCHANGED (Constant(value=False))
✅ MACRO_NEWS_CRIT_ADJ / MACRO_NEWS_STRONG_ADJ UNCHANGED (1.0 / 1.0)
✅ CONFLUENCE_SCORE_THRESHOLD UNCHANGED (2.0)
✅ FILTER_ENFORCEMENT_ENABLED / _DRYRUN UNCHANGED (True / True)

── main.py ──
✅ no function/class ADDED or REMOVED (93 defs, added=[] removed=[])
✅ NO function/class BODY changed  changed=[]
✅ 🔴 module AST is BYTE-IDENTICAL — the edit is invisible to the parser

── macro_filter.py ──
✅ no function/class ADDED or REMOVED (9 defs, added=[] removed=[])
✅ NO function/class BODY changed  changed=[]
✅ module AST DIFFERS — 🔴 EXPECTED AND NAMED, NOT GLOSSED: the module docstring
   IS an AST node, so a docstring edit cannot leave the AST identical
✅ AST with ALL docstrings stripped is IDENTICAL
✅ everything ABOVE the wiring paragraph is byte-identical
✅ the false sentence is GONE; the docstring now states what the code does
✅ the docstring records the flip date AND the 63-day lag

✅ exactly the 3 intended .py files were modified — ['config.py','macro_filter.py','main.py']
✅ exactly ONE gate expression exists, at main.py:4395

AST ASSERTIONS: 25 ✅   0 ❌
```

🔴 **The `macro_filter.py` AST is NOT identical, and saying so is the point.** The instruction was
"confirm by AST that no function changed" — a docstring is not a function, but it *is* an AST node,
so a bare `ast.dump` equality would have gone red for an honest reason. **Both facts are asserted
separately** rather than picking whichever comparison passes.

---

## PROOF BY EXECUTION — 20 VECTORS, SEARCHED BY DIRECTORY

```
LAB: full tree copy; every PRODUCTION-DIRECTORY literal rewritten to the lab.
  residual "/mnt/volume_nyc1_1780480650620/mercury-sol" + "/root/titan-bot" : 0

20 VECTORS found by DIRECTORY grep (not by filename):
  .env  engine_15m.py  healthcheck.py  liquidity_sweep.py  main.py  market_context.py
  mercury_sol_prior_move_logger.py  naked_alert_resolver.py  optimizer.py
  optimizer_listener.py  post_exit_observatory.py  signal_matrix.py  signal_weights.py
  silence_digest_sol.py  skip_attribution.py  sol_downtrend_regime_watch.sh
  sol_uptrend_regime_watch.sh  state_machine.py  virtual_trader.py  weight_engine.py

LOCK (installed BEFORE the first import, never lifted):
  sqlite3.connect      -> raises on any path under PROD or /root/titan-bot
  open(mode=w/x/a/+)   -> same
  sys.dont_write_bytecode = True

RESULT: 19 assertions ✅  0 ❌   LEAKS: 0
```

**What the harness actually exercised — the gate on both branches, not just the constants:**

```
✅ 🔴 total_gate_adj has NO DXY TERM — proved BY CONSTRUCTION, not by reading:
     the summed terms are exactly  ctx['crypto_gate_adj'] + ctx['macro_gate_adj']

✅ raw=4.50 pen=+1.0 DRYRUN=True  -> ADMIT   today's entry: clears on raw alone either way
✅ raw=4.50 pen=+1.0 DRYRUN=False -> ADMIT   today's entry, LIVE branch — still clears
✅ raw=2.50 pen=-1.0 DRYRUN=True  -> ADMIT   row 17299 under DRYRUN: would have been admitted
✅ raw=2.50 pen=-1.0 DRYRUN=False -> REFUSE  row 17299 LIVE: the headline decided this one
✅ raw=1.75 pen=+1.0 DRYRUN=True  -> REFUSE  vpos 25 under DRYRUN: would never have opened
✅ raw=1.75 pen=+1.0 DRYRUN=False -> ADMIT   vpos 25 LIVE: the one position it ever built
✅ with the SHIPPED flag, raw=2.50 pen=-1.0 is REFUSED — the adjustment reaches the threshold
✅ _CRYPTO_ADJ sign table, _MACRO_WIN_PENALTY −2.5, TTLs 900 s / 60 s — all unchanged
✅ 🔴 /root/titan-bot git-CLEAN at HEAD 897850b — NOT TOUCHED
```

**And the 2026-08-09 lesson was re-applied:** the sweep for production-path holders **outside** the
bot directory found **388 files**, headed by `/root/mercury_sol_30trade_reminder.sh` — the vector no
in-tree grep reaches. None of them is touched by this pass (it edits three files inside the bot
directory), but the check was run rather than assumed.

---

## 🔶 ONE THING I DID THAT I DID NOT INTEND, DISCLOSED

Running `python3 -m py_compile config.py main.py macro_filter.py` **inside the production
directory** as a syntax check **rewrote three `.pyc` files in `/…/mercury-sol/__pycache__/`** at
17:42.

```
config.cpython-312.pyc       10,573 b   17:42   (overwritten)
main.cpython-312.pyc        253,374 b   17:42   (overwritten)
macro_filter.cpython-312.pyc 27,641 b   17:42   (overwritten)
ownership root:root — unchanged, matching every other file in that directory
```

**Behaviourally harmless and stated as such:** a `.pyc` is a cache keyed to its source's mtime and
size, these were compiled from the current source, and the running worker imported its modules at
18:42:12 **yesterday** — it holds them in memory and never re-reads either file.

🔴 **The real cost is forensic, and it is the one worth naming.** The deployment-gap method used on
this bot reads the `.pyc` header's recorded source-mtime to prove what a running process loaded.
For these three modules that trail now records the **post-edit** mtime. **It is recoverable: the
backups were taken with `cp -p`, so the pre-edit source mtimes survive exactly** —

```
config.py.bak_macrocomments_20260810_1735       2026-08-09 18:41:54.355280860
main.py.bak_macrocomments_20260810_1735         2026-08-09 19:08:25.250787278
macro_filter.py.bak_macrocomments_20260810_1735 2026-06-23 09:54:34.198210356
```

— and `config.py`'s 18:41:54 still sits **before** the 18:42:12 service start, which is the proof
that the running process has `MACRO_GATE_DRYRUN=False` loaded. **The anchor is intact. The syntax
check should have run in the lab.**

---

## 🔴 WHAT IS LOADED AND WHAT IS NOT — NOT RESTARTED

```
🔴 vpos 32 SHORT is OPEN on real money since 2026-08-10 15:15:33
   is_paper=0 · size 1.3 @ 76.18 · SL 77.32 · entry row 17289
   (raw 4.25, pen −1.0 -> gated 3.25 — admitted either way, NOT a macro flip)

NOT RESTARTED, and there are now two reasons rather than one:
  1. this pass adds ONLY comments — nothing to load;
  2. a live position is open, same rule as every pass this week.

ON DISK, NOT LOADED — held in memory by the worker since 2026-08-09 18:42:12:
  config.py       18:00 today  (this pass)   + nothing pending before it
  macro_filter.py 18:00 today  (this pass)   + nothing pending before it
  main.py         18:00 today  (this pass)   + the 19:08 boot-card fix, still pending
```

**Stated plainly: the corrected comments are on disk and will be read by the next person to open
the file, which is the only audience a comment has.** They do not need to be loaded, and nothing in
this pass would change if they were.

---

## STATE

```
mercury-sol   active · master 4059454 / worker 4059524 · since 2026-08-09 18:42:12 · NRestarts=0
              NOT restarted · webhooks serving normally at 17:40 · heartbeat open=1
vpos 32       OPEN · SHORT 1.3 @ 76.18 · SL 77.32 · is_paper=0 · UNTOUCHED
vpos 31       CLOSED 15:21:44 · sl @ 75.90 · −$1.4554 · −1.155R  (the trigger position)
changed       config.py +22/−3 · main.py +24/−2 · macro_filter.py +17/−4 · OPEN-ITEMS-SOL.md +130/−0
              9 deleted lines total, all 9 listed above, all 9 the false comment blocks
backups       *.bak_macrocomments_20260810_1735 (4 files), md5-verified IDENTICAL to the
              originals BEFORE the first edit, mtimes preserved with cp -p
md5 after     config a6e15f41…  main d98b55d1…  macro_filter 597cee88…
db            opened read-only for every query (file:trades.db?mode=ro); one read retried
              on "database is locked" — the live worker holds it, which is correct
titan         active · HEAD 897850b · git clean · NOT TOUCHED, NOT READ FOR STATE
```

**No behaviour changed. No function changed. No constant changed. No restart. No order. The macro
adjustment is exactly where it was this morning, and now the source says so.**
