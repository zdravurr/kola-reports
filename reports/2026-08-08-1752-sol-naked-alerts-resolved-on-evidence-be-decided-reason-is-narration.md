# sol-naked-alerts-resolved-on-evidence-be-decided-reason-is-narration

_2026-08-08 17:52 UTC_

---

# Mercury-SOL — the phantom alerts are gone, resolved ON EVIDENCE. Tomorrow's 08:20 digest reads zero.

**All five rows resolved individually, each with the venue evidence that ends its own
condition. A resolver now runs from cron at 08:19, one minute before the digest —
so this is fixed for tomorrow WITHOUT restarting the bot. It fails closed, it never
resolves on age, and a genuinely naked position still survives it (proven).**

**Item 2 decided and recorded with a falsifiable reversal condition. Item 3 recorded as a
correction to the record only — AST shows zero function changes across all four edited files.**

vpos 29 untouched · service not restarted · Titan untouched.

Prior: [close-of-session 17:20](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1720-sol-open-items-close-of-session.md)

---

## 1. THE NAKED-POSITION ALERTS — RESOLVED ON EVIDENCE

### (a) The predicate, for every stage that can write one

Five stages exist. Each gets a predicate that requires a **positive reading of the venue**:

| stage | resolved when | writer |
|---|---|---|
| `entry_fill_unreadable` | side **FLAT**, or the venue position is **described by an OPEN `is_paper=0` row** | `main.py:2581` |
| `boot_orphan` | same | `main.py:2331` |
| `sl_failsafe_close_failed` | side **FLAT**, or **managed AND a stop actually resting on the venue** — booked alone is not enough, an unstopped position is the danger | `main.py:2177` |
| `partial_fill_unreadable` | the named `vpos` is **CLOSED** (the close sizes from the venue, settling the leg), or side FLAT | `main.py:3069` |
| `exchange_close_unsubstantiated` | the named `vpos` is **CLOSED with a `close_price` booked** | `virtual_trader.py:2043` |
| *anything else* | **never** — an unknown stage refuses to resolve blind | — |

Bybit nets one position per `positionIdx` and `MAX_POSITIONS_PER_SIDE` is 1, so "is anything naked
on this side" is answerable from one row per side. That is why the side-level predicate is sound.

### (b) 🔴 EVIDENCE, NEVER AGE — and it fails closed

```
age-based tokens in the resolver (timedelta / days= / hours= / older than / age >): NONE
```

There is no sweep and there must never be one: age is the one signal that would clear a genuinely
naked position while it is still true. Proven:

```
venue read raises  ->  exit code 2, unresolved before=5 after=5
                       "resolving NOTHING. Every open alert stays open and keeps shouting."
```

`main()` returns before it opens the database when `read_venue()` raises.

### (c) The backfill — five rows, five separate pieces of evidence, no bulk UPDATE

Each row was verified against the venue at run time, then updated on its own.

```
✅ id=1 [entry_fill_unreadable] ts=06:50:21  detail order_id=bcf63671…
     EVIDENCE: venue closed-PnL record 06:50:25 UTC: side=Sell qty=2.6 avgEntry=74.795
     avgExit=74.78 closedPnl=-0.427895 orderId=e7ec215a — the position this alert was
     raised for was FLATTENED

✅ id=2 [entry_fill_unreadable] ts=08:35:17  detail order_id=6e489d1f…
     EVIDENCE: venue closed-PnL record 08:35:20 UTC: side=Sell qty=2.6 avgEntry=74.85
     avgExit=74.84 closedPnl=-0.415194 orderId=1ed83d66 — FLATTENED

✅ id=3 [entry_fill_unreadable] ts=08:50:15  detail order_id=12ed23b7…
✅ id=4 [boot_orphan]           ts=13:58:18
✅ id=5 [boot_orphan]           ts=15:40:43
     EVIDENCE (each): superseded by the ADOPTION of vpos=29 at 15:40:43Z — the venue LONG
     (size=0.9 avg=74.8 sl=74.95 openTime=1786179014459) is described by an OPEN is_paper=0
     row (vpos=29 size=0.9 sl=74.9496) and is MANAGED — not naked
```

Rows 1 and 2 were resolved by the **closed-PnL records that flattened their positions** — stronger
per-row evidence than the generic side predicate, and re-fetched live rather than quoted from an
earlier report. If a row's own evidence had not verified, that row would have been left alone.

### (d) `resolved_at` and `resolved_by` — a resolution must not look like a suppression

```sql
ALTER TABLE naked_position_alerts ADD COLUMN resolved_at TEXT;
ALTER TABLE naked_position_alerts ADD COLUMN resolved_by TEXT;
```

Additive, applied by the resolver itself (so a fresh DB self-migrates; `main.py`'s CREATE was left
alone, keeping this out of the pending-restart set). Every resolution records the resolver name and
the venue facts it read. The stored trail:

```
(1, 'entry_fill_unreadable', 1, '2026-08-08T17:49:22Z', 'backfill 2026-08-08: venue closed-PnL record 06:50:25 UTC: …')
(2, 'entry_fill_unreadable', 1, '2026-08-08T17:49:22Z', 'backfill 2026-08-08: venue closed-PnL record 08:35:20 UTC: …')
(3, 'entry_fill_unreadable', 1, '2026-08-08T17:49:22Z', 'backfill 2026-08-08: superseded by the ADOPTION of vpos=29 …')
(4, 'boot_orphan',           1, '2026-08-08T17:49:22Z', '…')
(5, 'boot_orphan',           1, '2026-08-08T17:49:22Z', '…')
```

### (e) The digest reads zero — and a REAL naked position still surfaces

Queried with the digest's own SQL and its own `BLOCKING_STAGES` map:

```
unresolved rows the digest would print : 0
of those, BLOCKING                     : 0
```

**And the guard still fires.** With the managed row removed so the venue LONG is genuinely
unmanaged, the resolver cleared **nothing**:

```
venue: LONG: size=1.3 sl=73.89 | SHORT: size=0.0
  ⏳ KEPT id=1..5 — "venue holds a position with NO managed row — STILL NAKED"
  resolved 0; still unresolved: 5
```

Thirteen predicate vectors were exercised; the five that must refuse all refused, including
"managed but NO venue stop → STILL DANGEROUS", "unknown vpos → refuses rather than guessing" and
"unknown stage → refuses to resolve blind".

### 🔴 WHY THIS WORKS TOMORROW WITHOUT A RESTART

The resolver is a **standalone script on cron**, the same outboard shape as the digest — not code
inside `main.py`, which would not load until the bot restarts and therefore could not clean
tomorrow's message.

```
19 8 * * *  naked_alert_resolver.py    <- NEW
20 8 * * *  silence_digest_sol.py      <- unchanged
```

Live run against production just now: `unresolved alerts: 0 · resolved 0 · exit 0` — idempotent, as
it must be to run daily.

---

## 2. `_BE_TARGET_FRAC_ON` STAYS AT 0.0020 — DECIDED, WITH A REVERSAL CONDITION

Recorded at the constant, so it no longer reads as undecided:

```
# ── 🔴 DECIDED 2026-08-08: IT STAYS AT 0.0020. NOT DEFERRED, DECIDED. ────────
# The gain is 8.7 cents per breakeven exit at live size, on a lock that armed 7
# times in 22 closed positions; the cost is -0.133R on the only case the book can
# measure. Do not re-open this on the strength of the arithmetic alone — the
# arithmetic was already known when it was decided.
#
# REVERSAL CONDITION, stated so this is falsifiable rather than permanent:
#   RE-OPEN when LIVE-era breakeven exits reach n >= 10 AND the fee wash is
#   measurable in REALISED R across them. Paper exits do not count toward the 10 —
#   the whole defect is a fee effect, and paper fees were understated 1.82x until
#   2026-08-08 (see the vpos 29/30 fee boundary in config).
# Until that n exists, this is settled.
```

The paper-exits exclusion matters: counting them would let the very fee error this is about
manufacture its own reversal.

---

## 3. THE ADVISOR'S BOOK CHANNEL — HALF-MEASURE, AS SPECIFIED

### (a) The prompt is untouched

`p = 1.0000` shows the wall **band** does not move the verdict. It does **not** show that depth and
imbalance contribute nothing, and removing information from a live prompt is a behaviour change
with no measured benefit. Nothing was changed. That reasoning is now written into the code so the
next reader does not "clean up" the prompt on the strength of the p-value.

### (b) The canon: `ai_reason` is narration, and the consumers are named

Placed on `consult_for_entry`'s return contract — where the string is produced:

```
── 🔴 CANON 2026-08-08 — `reason` IS NARRATION, NOT MECHANISM ──────────────
  • P(execute) 3.24% with a p80+ opposing wall vs 3.36% without — Fisher p = 1.0000
  • 81.6% of reasons discuss walls; 6.6% cite the percentile the prompt calls primary
  • of 3 checkable claims, 3 were FALSE against the model's own prompt
ANY ANALYSIS THAT READS A CITED REASON AS A CAUSE IS READING A STORY.
```

**The three places that currently do it, each given a pointer at the line where it happens:**

1. **`skip_attribution.py:371`** — persists `ai_reason` into the Skip-Attribution Observatory,
   whose stated purpose is "why did we skip".
2. **`silence_digest_sol.py:437`** — buckets `ai_reason` across `ai_skipped` rows and presents the
   tally as the explanation of a quiet day.
3. **`claude_advisor.consult_for_learning`** — the post-trade attribution consult.

### (c) Nothing the bot decides changes — proven

```
AST vs the backups:
  claude_advisor.py     added=[] removed=[] changed=[]
  trail_arm.py          added=[] removed=[] changed=[]
  skip_attribution.py   added=[] removed=[] changed=[]
  silence_digest_sol.py added=[] removed=[] changed=[]
```

**Zero functions added, removed or changed in any of the four.** Every line is a comment or a
docstring.

---

## PROOF BY EXECUTION — 17 VECTORS, BY DIRECTORY

```
by DB filename : 13     by DIRECTORY : 16     (+ .env = 17 VECTORS)
missed by the filename grep: healthcheck.py, mercury_sol_prior_move_logger.py,
                             weight_engine.py  <- holds WEIGHTS_PATH to prod weights
```

Lab: full copied tree, all 17 rewritten, **0 prod-path literals**, `sys.dont_write_bytecode=True`,
lock on `sqlite3.connect` and write-mode `open()` against **both** the prod directory and
`/root/titan-bot`. **Leaks: 0. All assertions passed.**

```
naked_alert_resolver.py   NEW, 236 lines
trail_arm.py              +13   -1
claude_advisor.py         +24   -0
skip_attribution.py        +3   -0
silence_digest_sol.py      +3   -0
```

Backups `*.bak_alertresolver_20260808_174710`, md5-verified before the write. Crontab backed up
before the edit.

---

## STATE

```
mercury-sol   active  pid 3533821 / worker 3533987  since 16:08:59  NRestarts=0  0 tracebacks
              NOT restarted — vpos 29 is open; the pending files stay pending
vpos 29       0.9 @ 74.80 · sl 74.9496 · open · partial 0.4 @ 76.36 · wm 76.46 — IDENTICAL
venue         LONG 0.9 · stop 74.95 · SHORT flat · untouched
alerts        5 of 5 resolved, each with its own evidence · 0 unresolved · digest reads zero
cron          19 8 resolver (new) · 20 8 digest (unchanged)
titan         active · HEAD 897850b · git clean · NOT TOUCHED
```

**Still open, unchanged:** the pending-restart trio (restart when flat), and the seven items from
the 17:20 register that were not in this pass — `apply_opt_proposal`'s dead second door, paper-mode
refusals, the vpos 29/30 fee boundary, filter #21's pre-registered test, the two morning fixes not
yet proven in a live entry, and tomorrow's 14:00 optimizer run.
