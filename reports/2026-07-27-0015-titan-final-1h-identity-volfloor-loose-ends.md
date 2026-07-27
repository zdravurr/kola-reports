# titan-final-1h-identity-volfloor-loose-ends

_2026-07-27 00:15 UTC_

---

# TITAN — 1H signal identity, volfloor counting, and the remaining loose ends

**2026-07-27 00:20 UTC · items 1-2 APPLIED · item 3 read-only.** Commit `f0a8d30`, pushed.

---

## 1. AI_ADVISOR_HIDE_1H — there IS a documented rationale, and it does not block this

Asked for before applying, so here it is first.

```
a8a6989  2026-05-25  "hide 1H from entry AI advisor view (AI_ADVISOR_HIDE_1H=True) —
                      advisor judges on 15m/5m/orderbook/volume; hard HTF gate still
                      uses 1H upstream"
882cd7c  2026-05-29  "AI advisor sees full 5-TF OHLCV trend picture (1d/4h/1h/15m/5m,
                      hybrid — LuxAlgo 1H still gated separately)"
```
config.py:330-337 states it explicitly: *"This is NOT a gate — it ONLY controls whether the 1H line
is shown in the ENTRY advisor's prompt… The hard `_htf_cascade_gate` above STILL uses 1H
independently."*

**The rationale is double-counting avoidance:** the cascade already hard-vetoes on 1H, so showing
the 1H *direction* again would let one tier influence the decision twice.

**Why it does not block adding identity** — and this is the part that matters:
* The advisor has seen the **1h state in substance since 882cd7c** — the 5-TF block prints
  `1h: BULL, ADX 16.9` on every prompt regardless of this flag. The tier is not hidden; only the
  LuxAlgo alert's *name and direction line* is.
* **Identity is not direction.** The new line says which alert fired and what its matrix weight is.
  It adds no directional claim the prompt did not already carry.
* `AI_ADVISOR_HIDE_1H` is **left True and untouched**. The suppressed `1H: <name> (direction: …)`
  line stays suppressed.

Had the rationale been "the model over-weights the 1H tier when it can name it", I would have
stopped and reported rather than applied. It is not that — it is about direction double-counting,
which this does not reintroduce.

### The diff — one line, and what it deliberately omits
```python
_h1_name = h1.get('signal_name')
if _h1_name:
    _w   = f", weight {classify(_h1_name)[3]:.1f}"          # matrix category weight
    _age = f", set {(now - slot_timestamp).total_seconds()/3600:.1f}h ago"
    user += f"1H trend set by: {_h1_name}{_w}{_age}\n"
```
Live render, verified after restart:
```
1H trend set by: Trend C. Up, weight 1.0, set 2.2h ago
```
**No win rate. No PnL. No historical performance.** The largest per-signal cell in the book is n=6,
and several hypotheses died on exactly that sample size today. The model learns **which** signal
fired, never whether it is good. Attaching a statistic is a separate decision with its own
validation and its own n — recorded as such, not done here.

Untouched: the HTF cascade veto, the signal matrix, the score gate, the FLAT floor, the exit
advisor, SL/trail/breakeven, the LONG partial, the recheck bound, every sensor, Mercury-SOL.

---

## 2. Volfloor now counts CLEAN rows

Three conditions added: entry after the forming-candle fix (**2026-07-04 11:58**), outside the
wall-trail window (07-02 23:28 – 07-13 01:55), `recheck_status != 'tightened'`.

```
before:  SHORT=7  LONG=11   -> FIRED on 2026-07-23
after:   SHORT=4  LONG=4    -> "not ready yet", silent
```
The 07-23 firing announced a cohort that was really 4 clean rows; the inflated p=0.048 came from
vpos 66, 68 and 74 — all three contaminated. The sensor now stays quiet until there is something
real. *(The file is gitignored, so it is applied on disk and documented in the commit message
rather than committed.)*

---

## 3. Remaining loose ends — small, safe, and none on the trade path

| # | finding | class | assessment |
|---|---|---|---|
| 1 | **`mfe_tracking`, `breakeven_jobs`, `liquidity_sweep_state` — 0 rows each, but each HAS a writer** (`mfe_tracker.py`, `breakeven_worker.py`, `liquidity_sweep.py`) | same class as the 15m missing write | **The closest thing to a real remaining loose end.** A table with a writer and zero rows means either the writer never runs or its path is dead. Worth one hour of tracing — it is exactly how the 15m gap looked. Not urgent: nothing reads them either |
| 2 | **13 of 28 status strings in `main.py` have never once appeared in the DB** — `ai_hold`, `ai_pending`, `no_position`, `close_failed`, `ambiguous_side` (all the exit-advisor path, expected), plus `unparsed`, `no_trend`, `no_confluence`, `filtered`, `bypass_flat_skipped`, `smart_tp_armed`, `liquidity_sweep`, `closed` | dead branches | Mostly benign — the exit-advisor five are explained. The other eight are branches that have never executed in 77 days. Not a defect, but they are untested code |
| 3 | **12 config constants with no comment** — `LIQUIDITY_SWEEP_WEIGHT_BONUS`, `LOSS_STREAK_COOLDOWN_HOURS`, `MACRO_VOLATILITY_PENALTY`, `CONFIRMED_REVERSAL_IDS`, `OBSERVE_REVERSAL_IDS`, `HTF_NEUTRAL_REQUIRE_15M_DRYRUN`, and 6 more | undocumented rationale | The same class as `AI_ADVISOR_HIDE_1H`, which *did* have its reason written down and that is precisely why today's decision was answerable. These twelve are not |
| 4 | **34 `.bak*` files, 111 MB working directory** | housekeeping | Harmless but accumulating; several are today's own snapshots |
| 5 | `mercury_sol_30trade_reminder.sh` logs `db-read-failed (got 'ERR')` since 2026-07-13 | SOL, pre-existing | Out of Titan scope — flagged for tomorrow |

**Nothing here needs new data and nothing touches the trade path.** Item 1 is the only one I would
call a genuine loose end of the 15m class; items 2-4 are hygiene.

---

## State at close of Titan

```
HEAD f0a8d30, pushed, tree clean
titan.service active, restarted 00:14, 0 errors on boot
flags: LONG_PARTIAL True · EXIT_ADVISOR PAPER/DRYRUN/ON_15M/HOURLY True
       FLAT 5.0 · WALL_TRAIL False · AI_ADVISOR_HIDE_1H True · LIVE_TRADING False
crontab: 4 Titan sensors · nginx noquery active
```

**Still awaiting your decision, unchanged:** rotate the Anthropic key (world-readable for 20 days),
and the live-path parity gap before `LIVE_TRADING_ENABLED` is ever set True.
