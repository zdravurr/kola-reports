# SOL — F1 CLOSED: EVERY EXIT IS NOW BOOKABLE. AND THE BOOT GEOMETRY LINE IS LIVE.

**2026-08-06 15:30 UTC · Mercury-SOL (PAPER) · APPLIED AND PROVEN BY EXECUTION.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`.
Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched in this pass** — clean at `897850b`,
workers 2538048/2538082 up since 01:53:18. §3a below answers your Titan question **from what I already
knew, without reading Titan.**

---

## 🔴 FIRST — A CORRECTION TO MY OWN 15:10 REPORT

**F1 is real, but I described its failure mode wrongly, and the truth is worse.**

I wrote that the six unmapped reasons would raise a `KeyError` inside `close_position`. They would not.
`close_position` already opened with a guard that predates all of my edits — I verified it in
`virtual_trader.py.bak_P1_G2c_20260806`, line 421:

```python
if reason not in _CLOSE_LABEL:
    print(f"{LOG_PREFIX}CLOSE rejected: unknown reason {reason!r}", flush=True)
    return None
```

So the lookup could never reach a `KeyError`. **The close was REFUSED instead** — and that is the worse
outcome, because a crash is loud and a refusal is not:

* no close row, no Telegram card, no PEO record;
* the `virtual_positions` row **left `'open'`** for a position the venue had already closed;
* `_poller_close` returns `None`, the live FLAT branch retries on the **next poll tick**, reads FLAT
  again, and is refused again — **a permanent rejection loop**, one log line per tick, while the engine
  goes on managing a position that no longer exists.

A `KeyError` would at least have produced a traceback someone greps for. This produced a line that looks
like routine chatter. **I am stating this plainly because the fix I shipped is the same either way, but
the severity I reported was wrong in the direction that understates it.**

The execution proof below shows the refusal directly — and it showed up in an unplanned way: the very
first pre-fix case left its row open and **the second case could not even be seeded**, because
`ux_vpos_one_open_per_side` is a partial unique index on `(symbol, position_side) WHERE status='open'`.
The defect blocked my own test harness. That is what it would do to the next real position on that side.

---

# 1. F1 — `close_position` CAN NO LONGER RAISE *OR* REFUSE

## a) All six venue reasons mapped, each to its OWN label

```python
'tp':                  'tp_{s}',                    # venue TakeProfit / PartialTakeProfit
'liquidation':         'liquidation_{s}',           # execType BustTrade — NEVER a stop-out
'adl':                 'adl_{s}',                   # execType AdlTrade — auto-deleveraged
'settlement':          'settlement_{s}',            # execType Settle
'exchange_market':     'exchange_market_{s}',       # plain fill: manual close / external reduce-only
'exchange_unreported': 'exchange_unreported_{s}',   # adapter returned no reason key
```

**None pooled into `sl_triggered_{s}`, none pooled into a shared `exchange_{s}` bucket.** This is the same
rule `_classify_exchange_exit` already applies on the reason side: an unrecognised value is information,
a wrong one is corruption. A liquidation filed as a stop-out would hide the single most important event
this book can record — and hide it inside the cohort that looks most ordinary. A take-profit filed as a
stop-out inverts the sign of the lesson. One frozenset entry each is the entire cost.

## b) 🔴 The fallback — and why it is a FIXED label, not a derived one

Mapping six known values still leaves the seventh unknown one failing in the same place.
`_classify_exchange_exit` **synthesises** `exchange_<sanitised>` for any venue type it has never seen, so
the set of reasons this function can receive is **open, not closed**. Enumeration is necessary but not
sufficient.

**What I chose:** an unmapped reason books as the single fixed label **`unmapped_close_{side}`**, plus a
loud line naming the literal reason and telling the reader exactly where to add it.

**Why not `f'{reason}_{side}'`,** which was the obvious alternative: a derived label would be a *new
unregistered string every time a new venue type appeared*, and `pair_trades` infers side from **set
membership** — an unregistered label is not an error, it is **silently dropped from learning**. A derived
label would therefore have reintroduced the P4 defect for exactly the cases nobody anticipated, which is
the population this fallback exists to protect. **A single fixed label can be registered in advance**, so
an unknown reason stays visible, stays paired, and stays non-fatal. Nothing is lost: the literal reason is
written verbatim to `virtual_positions.close_reason` on the same row.

The refusal guard is **gone**. Booking is always right here: the caller only reaches this function once it
has established the position is gone, and the reason is *descriptive*, never the decision.
**Refusing to describe an exit is not a reason to refuse to record it.**

## c) All seven labels registered with the optimizer in the same edit

```python
_CLOSE_LONG_TYPES  += tp_long,  liquidation_long,  adl_long,  settlement_long,
                      exchange_market_long,  exchange_unreported_long,  unmapped_close_long
_CLOSE_SHORT_TYPES += tp_short, liquidation_short, adl_short, settlement_short,
                      exchange_market_short, exchange_unreported_short, unmapped_close_short
```

Emitting six new labels without registering them would have introduced the P4 defect **six times over**.
And the fallback in particular must be registered *ahead of time* or it protects nothing.

## d) Paper behaviour — byte-identical, proven not asserted

All seven are **LIVE-only**: the emitting branch is gated on `not _is_paper(row)` and SOL runs in
`OBSERVATION_MODE`, so no paper row can produce any of them. The harness ran all six paper reasons through
both trees and compared the results programmatically:

```
PAPER rows pre-fix == post-fix : True
  all 6 paper reasons: same outcome, same label, same close_reason
```

| paper reason | outcome | label | close_reason |
|---|---|---|---|
| `sl` | BOOKED | `sl_triggered_short` | sl |
| `trail` | BOOKED | `trail_short` | trail |
| `timeout` | BOOKED | `timeout_close_short` | timeout |
| `exit_signal` | BOOKED | `exit_short` | exit_signal |
| `post_entry_critical` | BOOKED | `sl_triggered_short` | post_entry_critical |
| `trend_reversal` | BOOKED | `exit_short` | trend_reversal |

**Identical in both trees.** This is coverage placed ahead of the live flip, not a change to what the bot
currently does.

## EXECUTION PROOF — both directions

Isolated tree, **13-file DB_PATH rewrite**, residual grep 0, `sqlite3.connect` wrapped to raise on the
production book, and the **isolated `.env`** loaded before `import config` (never production — `config.py`
does not call `load_dotenv` itself and the flag is `MERCURY_OBSERVATION_MODE`, so a bare import silently
inverts the mode). **`production-book opens: 0` in every run.**

### BEFORE

```
tp                     -> REFUSED (returned None)   label=None   row=open
liquidation            -> REFUSED (returned None)   label=None   row=open
adl                    -> REFUSED (returned None)   label=None   row=open
settlement             -> REFUSED (returned None)   label=None   row=open
exchange_market        -> REFUSED (returned None)   label=None   row=open
exchange_unreported    -> REFUSED (returned None)   label=None   row=open
exchange_SomeNewBybitType -> REFUSED (returned None) label=None  row=open
```

**Every one refused; every row left open.**

### AFTER

```
tp                     -> BOOKED  label=tp_short                    row=closed  optimizer_pairs=True
liquidation            -> BOOKED  label=liquidation_short           row=closed  optimizer_pairs=True
adl                    -> BOOKED  label=adl_short                   row=closed  optimizer_pairs=True
settlement             -> BOOKED  label=settlement_short            row=closed  optimizer_pairs=True
exchange_market        -> BOOKED  label=exchange_market_short       row=closed  optimizer_pairs=True
exchange_unreported    -> BOOKED  label=exchange_unreported_short   row=closed  optimizer_pairs=True
exchange_SomeNewBybitType -> BOOKED  label=unmapped_close_short     row=closed  optimizer_pairs=True
    🔴 UNMAPPED close reason 'exchange_SomeNewBybitType' — booking as 'unmapped_close_short'
       (NOT as a stop-out). The literal reason is preserved in virtual_positions.close_reason.
       Add it to _CLOSE_LABEL and to optimizer._CLOSE_*_TYPES.
```

**P1/G2c regression re-run on the F1 tree:** Gross +137.4403, `Net−(Gross−Fees) = +0.000000`,
label `trail_short`, control unchanged. Nothing regressed.

---

# 2. THE BOOT GEOMETRY LINE — SHIPPED, AND IT IS THE WORKER SPEAKING

```
Aug 06 15:25:47 mercury-sol[2730881]: [2026-08-06 15:25:47] [2730881] [INFO] Booting worker with pid: 2730881
Aug 06 15:25:47 mercury-sol[2730881]: [MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h OBSERVATION_MODE=True [pid 2730881]
```

## a) It reports the WORKER's memory — and the placement had to change to achieve that

🔴 **`preload_app = True`.** That single setting invalidated the obvious implementation. With preload,
`main` — and therefore `config` — is imported in the **master**, and workers inherit it across `fork()`.
A module-level print at import time would have run in the **master**, reported the master's memory, and
carried the master's pid: the wrong process to make a claim about.

`post_fork` is the only hook that runs **inside the worker**, so that is where the call went, reading
through the imported `config` module object — its own in-memory globals, never re-read from disk. The
**pid in the line is the proof**: `[pid 2730881]` matches gunicorn's own "Booting worker with pid: 2730881"
on the line immediately above. This follows the file's existing precedent — `start_monitor`,
`start_virtual_poller` and `start_signal_audit` are all worker-only for the same preload reason, and
`[SIGNAL-AUDIT]` already logs its pid.

**Scope stated honestly:** production boots via systemd → gunicorn → `post_fork`, so the line always
appears. The dev-only path (`python main.py` directly) does not run `post_fork` and does not emit it.
That path is not used in production, and I left `main.py` byte-identical rather than widen the diff
during the n=8 window.

## b) 🔴 It is INERT — confirmed

`boot_geometry_line()` formats a string from module globals and returns it; `post_fork` prints it.
**No branch, no threshold, no order, no DB write.** A print cannot change a decision. That is why it
ships in the middle of the n=8 re-measurement window **without contaminating it** — and why it was safe
to ship in the same pass as F1.

## c) The derived ratio is in the line, not left to the reader

`1.875` means nothing without `2.5` beside it. The number a reader actually needs is the giveback in R,
so it is computed in the emitter and printed as **`(0.750R)`**. If either constant ever moves, the ratio
moves with it in the same glance.

## d) Recorded in the canon

The reasoning is written at the function itself, not only in this report: that this closes the gap **at
the point it opens** — the worker's own module state — and that the 25-minute divergence of 2026-08-06
(config edited 14:30:43, worker importing at 13:55:22) **cost nothing only because the book happened to be
flat since 2026-08-03.** A signal at 14:35 would have opened a position at 1.0R while every artifact on
disk claimed 0.75R, contaminating the n=8 cohort from its first observation with a member nothing would
have flagged. There is no reload path — zero `importlib` uses tree-wide — so a process's constants are
frozen at its first `import config`.

---

# 3. RECORDED, NOT ACTED ON

## a) 🔴 Titan — the question APPLIES, and it may be bigger than the label

**I did not read Titan. This is stated from what I already established, and it is a question, not a finding.**

Two things I know from SOL's own source, read earlier today:

1. **SOL's `optimizer.py` says the close-type sets are byte-identical to Titan's** — verbatim: *"Titan got
   the identical fix — the two sets stay byte-identical."* Those sets contained `sl_triggered_*` and **no
   `trail_*`**. So Titan's optimizer recognises no trail label, which means Titan's `trades` almost
   certainly does not emit one.
2. **SOL's `virtual_trader.py` cross-references `Titan vt:447`** for the entry-row back-fill convention, so
   Titan has a `virtual_trader.py` with a close path of the same shape. SOL's paper engine is a port of it.

**On your actual question — yes, the `trades`-vs-`virtual_positions` divergence I corrected here very
likely exists on Titan too**, for the same structural reason: a shared `_CLOSE_LABEL` pooling `trail` into
`sl_triggered_{s}` while `close_reason` keeps the literal. One grep settles it:
`grep -n "_CLOSE_LABEL" -A 12 /root/titan-bot/virtual_trader.py`.

> 🔴 **But the more urgent question is F1, not G2c.** If Titan's `close_position` carries the same
> `if reason not in _CLOSE_LABEL: return None` guard *and* has a live path feeding it venue-derived
> reasons, then **on Titan that refusal loop would run on real money** — a real liquidation or ADL could
> go unbooked while the engine kept managing a position the venue had already closed. On SOL this is
> latent because SOL is paper. On Titan it would not be.
>
> **I do not know whether Titan's live path feeds venue reasons at all.** SOL's did only after
> `_BYBIT_STOPTYPE_TO_REASON` landed on 2026-08-05, and Titan is a different venue with different exit
> semantics — it may never produce these strings. **That is precisely why this is a question for you and
> not an action by me.** Titan was not touched, read for state, or restarted.

## b) F2 — the retired monitor

`main.py:4793` still writes `sl_triggered_{side}` directly. Its own comment marks it as the **retired**
`_monitor_positions`, absorbed into the Phase-2 engine. Left alone deliberately, recorded so G2c is not
mistaken for total coverage of the `trades` label surface.

---

# 4. THE CHANGE, AND WHAT WAS NOT TOUCHED

**Code-only diffs (comments and blanks stripped):**

```
virtual_trader.py   +6 label mappings, +_UNMAPPED_CLOSE_LABEL, +_close_label_for(),
                    −3 (the refusal guard),  1 line changed (the lookup → helper)
optimizer.py        +4 lines (14 new labels across both sets)
config.py           +1 pure addition: boot_geometry_line()
gunicorn_mercury.conf.py  +3 lines in post_fork
```

**Untouched, mtimes unchanged:** `main.py` **13:51:21**, `claude_advisor.py` **12:15:12**,
`state_machine.py`, `signal_weights.py`. **The cascade, the score bars, both prompts, the state dedup and
M1–M7 all live in `main.py` and `claude_advisor.py` and were not opened.**

**Backups:** `virtual_trader.py.bak_F1_unmapped_reasons_20260806`, `optimizer.py.bak_F1_labels_20260806`,
`config.py.bak_bootgeometry_20260806`, `gunicorn_mercury.conf.py.bak_bootgeometry_20260806`.

---

# 5. FINAL STATE

```
mercury-sol.service  active (running)  master 2730795  worker 2730881 (15:25:46)  NRestarts=0
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h
                    OBSERVATION_MODE=True [pid 2730881]
tracebacks since restart : 0
open vpos / active_positions / exit_pending : 0 / 0 / 0     (flat since 2026-08-03)

OBSERVATION_MODE = True     SL_BUFFER_ATR = 2.5     TRAIL_MULT_ATR = 1.875 (0.750R)
ATR_TF = '1h'   MAX_POSITIONS_PER_SIDE = 1   WALL_V2_CEILING = 20.0   NEWS_PINNED = True

virtual_positions.close_reason : trail 4 · sl 11 · exit_signal 6   (untouched)

TITAN: git clean · HEAD 897850b · workers 2538048/2538082 up since 01:53:18 · NOT TOUCHED
```

**The n=8 trail re-measurement is unaffected — nothing in this pass changes a trading decision.
The next trailed exit is still observation 1 of 8.**

---

*Generated 2026-08-06 15:30 UTC.*
