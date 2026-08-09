# sol-the-boot-card-stops-lying-and-the-whole-class-is-swept

_2026-08-09 19:20 UTC_

---

# APPLIED. The boot card reads the row. **And the sweep you asked for found a FOURTH instance that had already fired on real money — vpos 30's REAL stop move was announced as "🔒 VIRTUAL Breakeven … (paper)" at 15:40:17 today.**

**The sweep was cheaper than a fourth catch, and it paid for itself immediately.** 47 sites
classified: **11 fixed, 16 already correct and verified, 20 deliberately left with a reason each.**

```
PROOF BY EXECUTION: 55 assertions ✅  0 ❌  LEAKS: 0.  Plus 14 AST assertions ✅ 0 ❌.
19 vectors rewritten by DIRECTORY (17 .py + .env + the cron .sh). 0 residual prod-path literals.
🔴 NOT RESTARTED — §4 found NOTHING on a live decision path. vpos 30 untouched.
```

Prior: [19:00 — the exit advisor's first verdict](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1900-sol-exit-advisor-live-in-dryrun-first-verdict-reads-its-prompt.md) ·
[17:00 — the same class on the close path](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1700-sol-the-money-report-stops-lying-four-defects-fixed.md)

---

## 🔴 THE FINDING YOU DID NOT ASK FOR, AND THE REASON THE SWEEP WAS WORTH IT

You named three instances: the close card, the pooled cumulative, the boot card. **There was a
fourth, on the same position, and unlike the boot card it is not hypothetical — it fired four hours
ago.**

```
WHAT vpos 30 ACTUALLY RECEIVED AT 15:40:17 TODAY:

  🔒 <b>VIRTUAL Breakeven</b> SOL/USDT:USDT LONG — SL → 76.44, trail 0.865% armed (paper)

The stop it is describing is conditional order 46968bbe-3bef-4ae6-a52d-6a0b11882f9d,
resting on Bybit, protecting $100 of real money. Nothing about it is paper.
```

`virtual_trader.py:2066`. It sits **six lines below** the partial card that was fixed for exactly
this on 2026-08-05, in the same `if crossed:` block, with the same `row` in scope. The partial card
was fixed because someone imagined it firing live; the breakeven card beside it was not, and then it
fired live.

```
NOW:
  🔒 <b>🔴 LIVE Breakeven</b> SOL/USDT:USDT LONG — SL → 76.44, trail 0.865% armed (🔴 LIVE — real money)
```

**The class is not "cards written before Phase 2". It is "every label that was true when only one
book existed".** That set is not enumerable by memory, which is why §4 was the right instruction.

---

## 1–3. THE BOOT CARD

### (a) What vpos 30 gets at the next boot, rendered by the real function

```
BEFORE
  🔄 <b>Paper positions still open at boot</b>
    • vpos=30 LONG @ 76.29 · SL 76.44258 · age 22.1h
  <i>poller resumes management — no auto-close</i>

AFTER
  🔴 <b>LIVE positions still open at boot</b>
    • vpos=30 LONG · 🔴 LIVE @ 76.29 · SL 76.44258 · age 22.1h
  <i>poller resumes management — no auto-close</i>
```

**§3 — the body is byte-identical.** `poller resumes management — no auto-close` is the sentence
that told you the 18:42 restart had adopted the position correctly, and it is still there, asserted
as such.

The log line gained the same fact, so the journal and the card cannot disagree:

```
[VPOS-RECONCILE] OPEN vpos=30 LONG book=LIVE entry=76.29 sl=76.44258 age=22.1h
                 — poller continues managing it (no auto-close)
```

### (b) 🔴 THE MIXED CASE — how it is handled, since you asked

**A mixed set is never rendered under either book's header. It is headed MIXED and COUNTED**, and
— the part that matters more than the header — **every line carries its own book**, so the header
is *checkable against the lines* rather than something to be believed:

```
🔴 <b>MIXED books still open at boot — 1 LIVE, 1 paper</b>
  • vpos=30 LONG · 🔴 LIVE @ 76.29 · SL 76.44258 · age 22.1h
  • vpos=31 SHORT · paper @ 74.8 · SL 75.9 · age 1.3h
<i>poller resumes management — no auto-close</i>
```

**Per-line books are the actual fix; the header is a summary of them.** A summary can only ever be
right about a homogeneous set, so the design makes the summary say *how many of each* and puts the
truth on the rows. The header is derived from the books present, never from a mode, a constant, or
the first row.

🔴 **Anything that is not purely paper leads with 🔴** — real money and an unreadable book are both
things to look at, and a boot card is read in three seconds on a phone.

### (c) 🔴 UNREADABLE IS UNKNOWN, NEVER PAPER

```
⚠️ <b>Positions still open at boot — book UNKNOWN (is_paper unreadable)</b>
  • vpos=32 LONG · book UNKNOWN @ 70.0 · SL 69.0 · age 1.3h
<i>poller resumes management — no auto-close</i>
```

And paper + unknown does **not** collapse to the paper header, because the unknown one might be
live:

```
🔴 <b>MIXED books still open at boot — 1 paper, 1 book-UNKNOWN</b>
```

**The column makes this reachable, not theoretical:** `is_paper INTEGER DEFAULT 1`, **no NOT NULL**.

### (d) 🔴 THE TWO DEFAULTS ARE OPPOSITE, AND THAT IS THE DESIGN

This is the sentence I would most want held against me later, so it is in the source as well as
here:

| | on an unreadable `is_paper` | why |
|---|---|---|
| **`_is_paper(row)`** — the **DECIDER** | falls back to **paper** | a paper close cannot spend money. Fail-safe. **UNCHANGED, and asserted unchanged.** |
| **`_row_book(row)`** — the **DESCRIBER** (new) | returns **None → UNKNOWN** | paper is the *dangerous* answer here: it is what hides real money. |

Same column, opposite safe direction, because one of them acts and the other only speaks. The
harness asserts both, so a future edit that "unifies" them fails loudly:

```
✅ 🔴 _is_paper (the DECIDER) STILL fails safe to paper on unreadable — UNCHANGED
✅ 🔴   and still fails safe when the column is missing — UNCHANGED
✅ 🔴 _is_paper still says paper when NO live adapter is registered — UNCHANGED
✅ _row_book is three-state and never guesses
```

### (e) The empty case said "paper" about zero rows

`no open paper positions at boot — clean.` → `no open positions at boot — clean.` There is no book
in an empty set to name.

---

## 4. 🔴 THE SWEEP — ALL 47 SITES

**Method, and why it is not a grep.** A plain grep over the tree returns 510 lines, nearly all
comments and identifiers (`virtual_positions`, `is_paper`, `virtual_trader`). Two AST passes instead:

1. **call-site pass** — string literals in argument position to `print`/`send_tg`/`send_full_report`/
   logging → **20 sites**;
2. **superset pass** — *every* non-docstring string literal carrying `paper|virtual|simulated|no real
   order`, minus identifier-only matches and SQL → **45 sites**.

🔴 **Pass 1 alone would have missed the entry card and the breakeven card**, because both build
their text into a variable first (`_open_hdr = …`) or sit inside a nested `try:`. The superset pass
is what caught the fourth instance. Plus 2 sites in the cron shell script, which no Python sweep
reaches at all → **47**.

### (a) FIXED — 11

| site | kind | why it can lie on the live path |
|---|---|---|
| `main.py:5923` | 🔴 TG boot card | **the header you named** — printed "Paper" for LIVE vpos 30 |
| `main.py:5900` | log | "no open **paper** positions at boot" — names a book for an empty set |
| `virtual_trader.py:2066` | 🔴 TG card | **"🔒 VIRTUAL Breakeven" — ALREADY FIRED on vpos 30, 15:40:17** |
| `virtual_trader.py:2067` | 🔴 TG card | "… armed **(paper)**" — same card, same real stop |
| `virtual_trader.py:2050` | log | `[ADAPT-TRAIL-PAPER]` — the BE block runs for LIVE rows too |
| `virtual_trader.py:2060` | log | same tag, failure branch |
| `silence_digest_sol.py:96` | 🔴 TG digest | `observed_skipped` = "approved, not sent **(paper)**" — **LIVE writes this status too** |
| `silence_digest_sol.py:452` | 🔴 TG digest | 2-state book read: **a NULL `is_paper` rendered as "LIVE"** |
| `silence_digest_sol.py:482` | 🔴 TG digest | same, on the HEALTHY line |
| `30trade_reminder.sh:86` | 🔴 TG | **"${CLOSED} closed paper trades" — POOLED both books since the flip** |
| `30trade_reminder.sh:7,71` | comment | documented the pooled count as paper |

**Two of these are findings in their own right, not just relabelling:**

🔴 **`observed_skipped` is not a paper status.** In LIVE mode `entry is None` writes it too — and
the boot-orphan refusal (`main.py:2591`, "the venue holds a position no database row describes") is
exactly that path. So the digest would have filed the single loudest live refusal this bot can
produce under a label reading *"(paper)"*. Now: `approved, no order was placed` — what is actually
known.

🔴 **The weekly reminder pooled the books and called the total paper.** `SELECT COUNT(*) FROM
virtual_positions WHERE status='closed'` with no filter — the pooled-cumulative defect again, in a
file outside the bot directory that no previous pass had reason to open. It has not fired yet (23
closed, threshold 30), so this is the rare one caught *before* the operator saw it.

```
BEFORE  [Mercury-SOL] ⏰ REMINDER: 30 closed paper trades (>=30).
AFTER   [Mercury-SOL] ⏰ REMINDER: 30 closed trades (>=30) — 22 paper, 7 🔴 LIVE, 1 book-unknown.

✅ paper + LIVE + unknown == the total — the split is exact, nothing invented or lost
```

**The THRESHOLD still counts both books, deliberately.** The re-check it triggers is a strategy
question (is there a negative-EV counter-trend cohort?), not a money question — filtering the
trigger to live rows would silently move the goalposts from 30 to a date years away. The *message*
now states the split instead of naming a book the number does not have.

### (b) ALREADY CORRECT — 16, verified rather than assumed

`virtual_trader.py:1387,1395` (close card + cumulative, the 17:00 fix) · `2026,2029` (partial card,
fixed 2026-08-05) · `optimizer.py:400,402,405,518,536` (all computed from `cohort_is_live`) ·
`optimizer_listener.py:89,93,94,102,104` (all read the evidence block).

🔴 **And one that looked exactly like the boot card and is not:** `main.py:4939`, the ENTRY card
`👁 VIRTUAL LONG OPENED (paper — no real order)`. It is gated on `entry.get('_virtual')`, and
`_virtual: True` is set in **exactly two places** — `virtual_trader.execute_entry:428` and `:806`,
both paper. The live path (`main.py:2900 book_live_position`) builds its dict at `:2934` and never
sets the key, so a live entry heads `🚀 LONG OPENED`. **Traced to both assignment sites rather than
inferred from the variable's name**, because "it reads a flag" is the same sentence that would have
been written about the boot card.

### (c) DELIBERATELY LEFT — 20, and the one real judgement call

**Paper-only by construction** (10): `virtual_trader.py:210,233,235` — `execute_entry`'s sole caller
is behind `if OBSERVATION_MODE` (`main.py:2575`); `main.py:2576,2577,2584` — that same branch;
`main.py:2953,2954,2957,2958` — `_virtual_close_for_side`, reached only via `if OBSERVATION_MODE`
(`main.py:2978`).

**Process-mode statements that are true as process-mode statements** (5): the poller heartbeat
`mode=PAPER/LIVE` (`virtual_trader.py:2217`), the digest's mode line (`silence_digest_sol.py:334`),
`main.py:5940,5941` — which says PAPER/LIVE *"adapter for NEW positions"*, and that scoping is
exactly right, and `main.py:5861` ("the paper engine is the single manager in **BOTH modes**").

**Identifiers, not operator text** (4): the `virtual-poller` thread name, `CYCLE_START_KEY =
'virtual_cycle_start_id'`, and the two places that name that key.

🔴 **The one I am leaving that I could argue either way — `virtual_trader.py:113`:**

```python
LOG_PREFIX = f"[{os.getenv('BOT_NAME', 'MERCURY-SOL')}][VIRTUAL] "
```

**This prefixes EVERY line the engine emits, including live ones** — `[VIRTUAL] CLOSE vpos=29` was
stamped on the first real $100 close. By the letter of §4 it hardcodes "VIRTUAL" and renders on the
live path.

**I left it, and this is the reasoning rather than a dismissal.** It names the *module*
(`virtual_trader`), not the position's book, and every line's *content* now carries the book.
Renaming it to `[ENGINE]` would rewrite the shape of every engine log line in the journal, break
every grep in every report written so far — including the ones I used to prove today's three
changes — and split the log history at an arbitrary point for a gain that is purely cosmetic once
the per-line labels are right.

**That is a trade-off, not a proof, and it is yours to overrule.** If you want it renamed, say so
and it is a one-line change with a stated log-history boundary.

**Files swept with ZERO hits (27):** `adaptive_trail` `claude_advisor` `config` `engine_15m`
`fee_rates` `filter_enforcement` `full_report` `gunicorn_mercury.conf` `healthcheck` `indicators`
`liquidity_sweep` `liquidity_zones` `macro_filter` `market_context` `mercury_sol_prior_move_logger`
`microstructure` `naked_alert_resolver` `news_sentiment` `post_exit_observatory` `signal_matrix`
`signal_weights` `skip_attribution` `state_machine` `stop_loss` `tor_retry` `trail_arm`
`weight_engine`.

---

## 5. 🔴 IT CHANGES NOTHING THE BOT DECIDES

### (a) Module AST, against the md5-verified pre-edit backups

```
main.py                 added=[]                        removed=[]  changed=['_reconcile_open_virtual_positions']
virtual_trader.py       added=['_book_label','_row_book'] removed=[]  changed=['_process_position']
silence_digest_sol.py   added=[]                        removed=[]  changed=['build']
```

### (b) 🔴 ONE FUNCTION IS NOT A CARD RENDERER, AND I AM NAMING IT RATHER THAN GLOSSING IT

Your §5 said *no function outside the card renderers may change*. **`_process_position` is not a card
renderer — it is the position-management tick** — and the breakeven card is written inline inside
it. There is no way to fix that card without its AST changing. So instead of claiming the rule held,
here is a stronger proof than the rule asked for:

```
🔴 _process_position, with EVERY print(...) / send_tg(...) statement deleted from BOTH
   versions, is AST-IDENTICAL before and after.                                    ✅

⇒ no branch, no comparison, no assignment, no order, no stop, no trail, no partial and
  no close changed. The only difference is what it SAYS.
```

Every other function on the money path is proved untouched by direct AST equality:

```
✅ main.py:start_virtual_poller        ✅ virtual_trader.py:_format_close_card
✅ virtual_trader.py:_exec_close       ✅ virtual_trader.py:_is_paper_row
✅ virtual_trader.py:_is_paper
✅ none of the other 29 production .py files was modified in this session
✅ 🔴 /root/titan-bot is git-CLEAN (HEAD 897850b) — NOT TOUCHED
```

### (c) The boot card still writes nothing

```
✅ 🔴 the boot card still WRITES NOTHING — no auto-close, row identical before/after render
```

### (d) Every deleted line accounted for

**18 deleted lines across four files, and all 18 are the mislabelling strings themselves or the
lines they wrap onto** — listed individually in the terminal record, not sampled. `main.py +70 −7` ·
`virtual_trader.py +55 −5` · `silence_digest_sol.py +26 −3` · `30trade_reminder.sh +15 −3`.

---

## PROOF BY EXECUTION — 19 VECTORS, SEARCHED BY DIRECTORY

```
LAB: full tree copy; every production-directory literal rewritten to the lab.
  residual "/mnt/volume_nyc1_1780480650620/mercury-sol" literals : 0
  residual "/root/titan-bot" literals                            : 0
  17 .py + .env + mercury_sol_30trade_reminder.sh  => 19 VECTORS

LOCK (installed BEFORE any import, never lifted):
  sqlite3.connect     -> raises on any path under PROD or /root/titan-bot
  open(mode=w/x/a/+)  -> same
  sys.dont_write_bytecode = True
  the Telegram sender replaced by a collector; the real one never reachable

RESULT: 55 assertions ✅  0 ❌  LEAKS: 0     +  14 AST assertions ✅  0 ❌
```

🔴 **By DIRECTORY, and the two methods disagree again — third time, third confirmation:**

```
found ONLY by the DIRECTORY grep (real vectors the filename grep MISSES):
    healthcheck.py        weight_engine.py   <- holds WEIGHTS_PATH to the prod weights
found ONLY by the FILENAME grep (FALSE POSITIVES — both are comments):
    config.py:320    macro_filter.py:34
```

**And this pass added a vector no version of either grep would have found:**
`/root/mercury_sol_30trade_reminder.sh` lives **outside the bot directory**, is not Python, and
holds the production DB path. It was found by asking "what else sends Telegram about this book",
not by searching the tree.

🔶 **Four harness assertions failed on the first run, and all four were my bugs, not the code's.**
Three tested `'paper' not in card` against a card containing the words *`is_paper` unreadable* — the
column name contains the word. The fourth asserted the old digest expression was gone from the file
while my own fix quotes it verbatim in a docstring as the record of what was fixed. Both are the
same mistake: **testing a substring where the claim is what matters.** The assertions now normalise
the column name and strip docstrings by AST. Recorded because a test that fails for the wrong reason
is one edit away from being "fixed" by weakening it.

---

## 🔴 WHAT IS LOADED AND WHAT IS NOT

**NOT RESTARTED. §4 found nothing on a live decision path — every one of the 11 fixes is a string.**

```
LIVE AT THE NEXT CRON FIRE — no restart needed, these are standalone scripts re-read per run:
  silence_digest_sol.py            08:20 tomorrow  <- the digest fixes ARE live tomorrow
  mercury_sol_30trade_reminder.sh  Mon 09:00       <- and it has not fired yet (23 closed / 30)

ON DISK, NOT LOADED — held in memory by the worker since 18:42:12:
  main.py            19:08   the boot card
  virtual_trader.py  19:10   the breakeven card + the ADAPT-TRAIL tag
```

**Stated plainly so it is not a surprise:** the boot card by its nature only renders at a boot, so it
is correct exactly when it next matters. **The breakeven card is different — it has already fired
for vpos 30 and will not fire again for this position** (`breakeven_applied: true`), so for vpos 30
the fix is retrospective only. The next position to reach +1R gets the true card.

These join `main.py` / `virtual_trader.py` / `optimizer.py` already pending from 17:00. **vpos 30 is
open, so nothing was restarted** — same rule as this morning.

---

## STATE

```
mercury-sol   active · master 4059454 / worker 4059524 · since 18:42:12 · NRestarts=0 · NOT restarted
vpos 30       OPEN · 0.9 @ 76.29 · sl 76.44258 · wm 77.50 · is_paper=0 · partial 0.4 @ 77.25
              mgmt_state {"breakeven_applied": true, "partial_done": true,
                          "exit_advisor_last_ts": 1786300951.587846}   — UNCHANGED BY THIS PASS
venue         LONG 0.9 · stop 76.44 · order 46968bbe · SHORT flat · stop NOT touched
advisor       DRYRUN · HOURLY · 1 verdict (HOLD 0.72) · next due ~19:42
tracebacks    0 since 18:42:12
db            opened read-only for every production query; every mutating test ran in the LAB
backups       *.bak_bootcard_20260809_1915 (4 files), md5-verified against the originals
              BEFORE the first edit
titan         active · pid 2538048 · NRestarts=0 · HEAD 897850b · git clean · NOT TOUCHED
```

🔶 **One process note against myself:** I first stamped the backups `_2015` and set the "nothing else
was modified" cutoff at 20:00 — both an hour ahead of the real 19:08–19:13 edits. The cutoff being in
the *future* meant that assertion passed vacuously and proved nothing. Backups renamed to `_1915`,
cutoff moved to 19:05, proof re-run. **A green check from a check that cannot fail is worse than a
red one.**

**One question left open for you, and only one:** whether `LOG_PREFIX`'s `[VIRTUAL]` tag should
become `[ENGINE]`. Everything else in the class is either fixed or has a reason recorded above.
