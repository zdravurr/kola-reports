# SOL — STATE DEDUP **APPLIED**. AND THE REVIEWED DIFF WOULD HAVE SAVED NOTHING.

**2026-08-06 12:45 UTC · Mercury-SOL (PAPER) · APPLIED, LIVE, worker pid 2680679, restart taken FROM FLAT**

Approved for application: the 12:15 report
(`2026-08-06-1215-sol-one-market-state-many-model-calls-dedup-safe.md`).
Titan (`/root/titan-bot`, LIVE REAL MONEY) **not touched** — `git status` clean at `897850b`,
its worker pid 2538048/2538082 never restarted.

---

## 🔴 THE HEADLINE IS NOT THE DEDUP. IT IS WHAT THE DIFF WAS MISSING.

The diff you approved was correct in every property it claimed — and it would have hit
**approximately never** in production. My own test T9 caught it, before restart, and the fix shipped
in the same change.

**The reviewed cache was consulted before the model call and written after it.** That is only
sufficient if the calls in one state are *sequential*. They are not. Measured on SOL's own book
before shipping:

| | |
|---|---|
| time from row insert to the post-verdict write | **min 6.11 s**, mean **16.14 s** (n=2,040) |
| same-side consultation pairs arriving **0 s** apart | **414** of ~528 |
| …within 5 s | **96%** |
| gunicorn | `workers=1, threads=4, worker_class=gthread` |

**The second alert is always already running while the first is still inside its Claude call.**
Both threads look in an empty cache, both call, both write. Zero saving, plus a cache.

Test T9, on the reviewed diff, against the real production shape:

```
4 concurrent alerts, one market state, 4 s model call
  model calls = 4    reused = 0        <-- the reviewed diff
  model calls = 1    reused = 3        <-- after in-flight coalescing
  wall-clock 4.0 s (four serial calls would be 16 s)
```

**What was added: in-flight coalescing.** The first thread into a state claims it with an Event; a
later thread for the same state waits on that Event instead of firing its own call, then reuses the
leader's verdict. Bounded, and degrading only ever toward "ask again":

- a follower **never waits longer than the leader's own call could take** — the wait is
  `TIMEOUT_SECONDS` (10 s), the advisor's own bound, so gunicorn's 30 s worker timeout is never
  approached;
- on timeout, or if the leader produced `unavailable`, the follower **makes its own call** — the
  pre-2026-08-06 behaviour. An outage is never inherited;
- the leader publishes and releases in **one critical section** and wakes its followers whether or
  not there was anything to publish, so an `unavailable` leader releases immediately rather than
  stranding anyone for the full 10 s (proven: T10 elapsed 2.0 s, not 10 s);
- a leaked marker (a leader that died between claiming and storing) is swept after 2× the wait and
  its waiters released — no thread can be stranded by a crash.

This is the same class as the finding the 12:15 report was about: **a mechanism that does not do what
it says.** It would have shipped as "20% saved", produced ~0%, and the next audit would have had to
find out why.

---

## WHAT IS LIVE

### 1. `claude_advisor.py` — the state cache (+143 lines)

- `_STATE_VERDICT_TTL_S = 60.0`, `_STATE_INFLIGHT_WAIT_S = TIMEOUT_SECONDS` (10.0),
  `_state_verdict_cache`, `_state_inflight`, one `threading.Lock`, `state_verdict_cache_clear()`.
  Process-local; dies with the worker.
- Key: `(symbol, direction, 1H slot identity, 15m slot identity, nearest opposing wall PRICE)`,
  where slot identity is `(signal_name, direction, slot timestamp)`.
  - **The 5m trigger is deliberately NOT in the key** — it is the only thing that differs.
  - **Slot timestamps, not rendered ages** — a refreshed tier self-invalidates.
  - **Wall price yes, wall multiple no** — the price never moved inside a state (0 of 353); the
    multiple wobbles in the first decimal (16.4%) and is the same wall re-measured.
- Store happens **after** the `system_prompt` / `user_prompt` / `model` stamps, so a reused copy
  carries the system prompt that actually produced it — including an aligned-V2 flip, which replaces
  both the verdict and `_verdict_system`.
- **`unavailable` is never cached.**
- A cache hit does not re-fire the aligned relaxation: the relaxation is part of the verdict, and at
  ≈12 extra calls per flip, re-asking it per 5m trigger is the same waste twice.

### 2. `main.py` — the companion column, shipped in the same change (+33 lines)

`ai_verdict_reuse_json TEXT`, added to `init_db()`'s additive column list and written on every
advisor consultation:

```json
{"reused": 1, "age_s": 0.012, "from_5m": "Within Bullish OB",
 "from_at": "2026-08-06T11:25:02+00:00", "rendered_user_prompt": "…"}
```

NULL on a real call, including the NEUTRAL-1H bypass path (which synthesises `advice` and never sets
these keys). **This was not optional and it is why:** a reused row stamps the prompt that *produced*
the verdict, so without this column it is indistinguishable from a fresh consultation and the next
audit mis-counts model calls exactly as the 2026-08-05 one nearly did — a measurement that cannot see
itself.

🔴 **A hazard found while wiring it:** `update_trade` (`main.py:1155`) builds its SQL straight from
kwargs and **swallows the exception**. A missing column would therefore have silently discarded the
*entire* advisor update — `ai_decision` included — not just the new field. `init_db()` runs at module
import (`main.py:791`), before the app serves, so the restart closes the window; the migration was
rehearsed on a DB copy first (16,271 rows, 0 back-filled) and confirmed present after boot.

### 3. Provenance — the rule holds, confirmed by execution

The 2026-08-01 defect was the inverse: 31 stored decisions named a prompt that did not produce them,
7 of which became positions carrying −$742.67. Driven against a DB copy with the real applied
advisor, three rows in one state:

| row | its own 5m trigger | `ai_decision` | `ai_user_prompt` names | `ai_verdict_reuse_json` |
|---|---|---|---|---|
| 16309 | `Within Bullish OB` | skip 0.92 | **Within Bullish OB** | NULL — a real call |
| 16310 | `Bullish I-CHOCH+` | skip 0.92 | **Within Bullish OB** ← the prompt that DECIDED | `from_5m: Within Bullish OB`, `.rendered_user_prompt` names **Bullish I-CHOCH+** |
| 16311 | `Bullish OB Created` | skip 0.92 | **Within Bullish OB** ← the prompt that DECIDED | `from_5m: Within Bullish OB`, `.rendered_user_prompt` names **Bullish OB Created** |

**1 model call for 3 rows.** Every row keeps its own verdict, its own `signal_type`, its own
`combo_key`. `ai_user_prompt` names the deciding prompt on all three; the row's own rendering rides
*beside* it, never over it.

### The tests — 13 + 4, all green against the applied files

| # | check | result |
|---|---|---|
| T1 | operator's 11:25 state, 3 triggers | **1 call, was 3** |
| T2 | refreshed 15m tier → new state | re-asks |
| T3 | opposing wall **price** moves → new state | re-asks |
| T4 | same wall re-measured ×11.7→×11.8 | reuses |
| T5 | opposite side never reuses | re-asks (+2 = V1 **and** the aligned-SHORT relaxation) |
| T6 | `unavailable` never cached | re-asks |
| T7 | TTL expiry | re-asks |
| T8/b/c | provenance: deciding prompt kept, own rendering beside it, reuse facts present | ✅ |
| **T9** | **4 concurrent alerts, one state, real production shape** | **1 call, 3 reused** (was 4 / 0) |
| **T10** | `unavailable` **leader** must not strand or infect followers | 3 own calls, elapsed **2.0 s**, not the 10 s wait |
| **T11** | in-flight marker released, not leaked | `_state_inflight == {}` |
| **T12** | a different state in flight is never coalesced in | 2 calls, 1 reused |

---

## PRE-REGISTRATION — WRITTEN BEFORE THE DATA ARRIVES

**Prediction: 69.6 → 54.8 calls/day at the 30-day rate; 89.1 → 68.6 at the current rate.
A 21.0% reduction. Measured after 200 consultations.**

The band is tight, not hedged. The live key is **stricter** than the key the 12:15 analysis grouped
on (slot timestamps vs a 10-minute bucket), which could in principle have cost hits — measured, it
costs none: **the rendered tier age changes between calls inside a state in 0 of 351 states**, so the
upper bound on redundant calls the stricter key could miss is **0 of 436**.

🔴 **If the realised saving is materially different, that is a finding about the state definition —
not a reason to widen the TTL.** Widening the TTL to chase a number would convert a measured claim
into a tuned one. The TTL is 60 s because 100% of redundant calls land inside it against a worst
observed gap of 32 s; that is a fact about the data, and it moves only if the data moves.

Recorded honestly: **the in-flight coalescing is new behaviour with no history**, so this prediction
is being made about a mechanism that has run for minutes, not weeks. The 21.0% figure is what the
*state grouping* implies; whether coalescing captures all of it in the field is exactly what the
200-consultation check is for.

---

## THE CAVEAT, ON THE RECORD RATHER THAN ARGUED AWAY

The two suppressed `execute` verdicts in the 59-day book were saved by `MAX_POSITIONS_PER_SIDE = 1`,
**not by the dedup**: on both dates a SHORT was already open (vpos 15 on 07-08, vpos 19 on 07-16), so
`virtual_trader.execute_entry` refused regardless of the verdict.

- measured rate of *"a reuse suppresses an execute verdict"*: **2 in 59 days**
- measured rate of *"a reuse costs a position"*: **0 in 59 days**

If the cap had been free, those two would have traded. That is the exposure, stated as a rate, not
dissolved.

---

## APPLY RECORD

| | |
|---|---|
| backups | `claude_advisor.py.bak_statededup_20260806`, `main.py.bak_statededup_20260806`, `trades.db.bak_pre_statededup_20260806` — all verified by md5 against the originals **before** any edit |
| diffs | `reports/2026-08-06-1245-sol-state-dedup-advisor.diff`, `…-main.diff` |
| compile | `py_compile` clean on both files |
| restart | `systemctl restart mercury-sol.service` at **12:20:55 UTC**, **from flat** — `open_vpos=0`, `active_positions=0`, `exit_pending=0` verified immediately before |
| boot | clean: *"No open positions … clean boot … no open paper positions at boot — clean"*, no traceback |
| worker | pid **2680679** (master 2680621), listening 127.0.0.1:5002 |
| migration | `ai_verdict_reuse_json` **PRESENT** after boot; 16,271 existing rows left NULL |

### Invariants, re-read at runtime after the restart

| | |
|---|---|
| `MERCURY_OBSERVATION_MODE` | **1** — still PAPER, no order has ever been sent |
| `ADVISOR_WALL_ALIGNED_V2_MULT_CEILING` | **20.0** |
| `NEWS_OBSERVATION_PINNED` | **True** |
| `MAX_POSITIONS_PER_SIDE` | **1** |
| geometry | `config.py` mtime **2026-08-05 00:19** — untouched. `SL_BUFFER_ATR 2.5`, `TRAIL_MULT_ATR 2.5`, `stop_loss.py`, `adaptive_trail.py`, `virtual_trader.py`, `signal_matrix.py`, `state_machine.py` all unmodified |
| files changed | **exactly two**: `claude_advisor.py` (12:15), `main.py` (12:10) |
| **Titan** | `git status` clean at **897850b**; worker 2538048/2538082 never restarted; nothing in `/root/titan-bot` read for state, modified or run |

---

## LIVE PROOF — **PENDING, AND SAID SO PLAINLY**

**What is proven:** the mechanism, by execution, against the applied files (17 checks, above); the
migration, on a DB copy and then confirmed present in the live DB after boot; the provenance rule,
by writing and reading back three rows in one state.

**What is NOT yet proven:** that the *running worker* has produced a reuse on real traffic. It
cannot be claimed yet, so it is not.

At 12:26 UTC, 5 minutes after the restart, the book shows **1 row since boot** (`no_trend`) and
**zero advisor consultations**. That is normal: the 08-04 silence ledger measured 274 rows → 155
distinct events, of which the gates stopped 135 *before* the advisor and only **93/day reached it**
— roughly 4 an hour. A multi-alert state is ~24% of states, so the first live reuse is expected
within one to two hours, not minutes. **Two watchers are armed** on the log (`STATE-CACHE`,
`AI-ADVISOR`, `Traceback`, `update_trade failed`) and on the column.

🔴 **Reading a quiet hour as success would be exactly the error this pass exists to stop.** Silence
is not proof — the whole finding above is that a mechanism can be correct in every stated property
and still never fire. The live confirmation is a **follow-up**, and it will name the row ids.

The query that settles it:

```sql
SELECT id, timestamp, side, ai_decision, signal_type,
       json_extract(ai_verdict_reuse_json,'$.from_5m')  AS decided_on,
       json_extract(ai_verdict_reuse_json,'$.age_s')    AS age_s
  FROM trades
 WHERE ai_verdict_reuse_json IS NOT NULL
 ORDER BY id;
```

Expected on the first multi-alert state: N rows sharing one `ai_user_prompt`, N−1 of them carrying a
`from_5m` naming the row that actually called, and **one** `[STATE-CACHE] HIT/inflight` per reuse in
the log. **If a multi-alert state passes and produces no reuse, that is a defect report, not a
footnote** — and it would mean the coalescing does not hold under the real request shape after all.

---

## STILL OPEN — unchanged by this change

1. **§3a — the stale 1H still casts a full vote.** 44.3% of current-form prompts read
   "2 agree, 1 oppose" where the lone opposing vote is a 13.4 h-median-old tier that the gate's own
   TTL would have dropped. The 2026-08-05 decision covered the *label*, not the *tally*.
2. **§3b — no per-wall percentile.** A ≥×4 wall exists in **100%** of book states; the ×11.7 wall
   behind the three 11:25 skips is the **69th percentile**. `skip_attribution` already stores the
   wall shape needed to compute it.
3. **The aligned relaxations at ≈12 extra model calls per flip** — now costed, still a live decision.
4. **P4 — the Bybit API key expires 2026-08-13T18:32:09Z.** Not flipped.
