# sol-failed-read-never-fired-and-bybit-capture-exception

_2026-08-02 17:53 UTC_

---

# MERCURY-SOL — THE OLD FAILED-READ DEFECT NEVER FIRED + BYBIT CAPTURE RECORDED AS AN EXCEPTION

**2026-08-02 ~18:00 UTC. Read-only audit plus two documentation entries. No code changed, no
restart.** Follows `reports/2026-08-02-1740-sol-recheck-okx4000-no-substitute-venue.md`.
Freeze untouched — `claude_advisor.py` / `config.py` mtimes still 08-01 20:54 / 08-02 13:34.
Window **86/200**, not reset. vpos 26 open, SL 72.59. Titan not touched.

---

## 1. 🟢 HOW OFTEN DID THE OLD DEFECT FIRE? **ZERO TIMES. The historical recheck record is trustworthy.**

The pre-fix defect: a failed order-book read silently skipped the wall rule, the surviving rules
scored 0, the verdict came out `OK`, and the tier was written **`t+N_ok`** with a healthy
Telegram. The question was whether that ever actually happened.

**It did not.** Four independent lines of evidence, three of them persistent and one of them
complete over the entire book's history.

### 1.1 The wall rule is skipped on two paths — both are measurable

```python
if entry_wall_mult and entry_wall_mult > 0 and cur_wall_mult is not None:
```

- **Path A — no baseline** (`entry_wall_baseline_mult` NULL or 0): the wall rule is skipped for
  **every tier of that position's whole recheck**. Persistent, per position.
- **Path B — failed refresh** (`cur_wall_mult is None`): skipped for that one tier.

### 1.2 Path A — complete, and clean

| | |
|---|---|
| positions in the book | **20** (vpos 7 → 26) |
| with a measured `entry_wall_baseline_mult` | **20 / 20** — range **8.9 – 15.5** |
| NULL baselines | **0** |
| 0.0 baselines | **0** |

**Path A never happened, for any position, ever.**

### 1.3 Path B — the completeness argument

The old `_walls_with_okx_fallback` returned `None` only when **Bybit-100 AND OKX-4000 both**
failed — Bybit was primary, OKX the fallback. So Path B is bounded above by OKX's own failure
rate, and that turns out to be measurable across the entire history.

**Every stored consultation records OKX-4000 availability**, because `main.py` renders either the
book block or the literal string `Order book (pre-trade): unavailable` into the prompt it stores:

| | |
|---|---|
| stored `ai_user_prompt`s | **3,033** — 2026-06-08 → 2026-08-02 |
| rendered `Order book (pre-trade, 8000 levels)` | **3,030** |
| rendered `Order book (pre-trade): unavailable` | **3** |
| **OKX-4000 failure rate** | **0.099 %** |

Corroborated by a second, independent persistent series — `smart_exit_dryrun_samples`, which calls
the same OKX source:

| | |
|---|---|
| samples | **234** — 2026-07-08 → 2026-08-02 |
| wall-fetch failures (`ob_imbalance IS NULL`) | **0** |
| `data_ok = 0` (any data gap at all) | **0** |

### 1.4 The three outages — and why none of them could have touched a recheck

| trades id | timestamp (UTC) | verdict |
|---|---|---|
| 5948 | 2026-06-30 18:20:01 | skip |
| 5949 | 2026-06-30 18:40:03 | skip |
| 5976 | 2026-06-30 20:25:02 | skip |

All three on **2026-06-30, inside a single 2-hour window** — and **the book was flat throughout**.

```
vpos 14  closed 2026-06-25 23:18
                        ← 13-day gap, no position open →
vpos 15  opened 2026-07-08 05:05
```

A join of every outage timestamp against every position's `[opened_at, opened_at + 300s]` recheck
window returns **no rows**. **No OKX outage in SOL's history has ever fallen inside a recheck
window** — and even if one had, Bybit-100 was the primary and would have served the refresh.

### 1.5 Direct observation, where the journal reaches

Journal retention is 2026-07-30 20:55 → now, covering vpos 25 and 26 — six tiers:

```
RECHECK vpos=25 SHORT T+10s  ... wall=10.2/10.2 ...
RECHECK vpos=25 SHORT T+60s  ... wall=8.8/10.2  ...
RECHECK vpos=25 SHORT T+300s ... wall=10.5/10.2 ...
RECHECK vpos=26 LONG  T+10s  ... wall=9.4/10.2  ...
RECHECK vpos=26 LONG  T+60s  ... wall=10.7/10.2 ...
RECHECK vpos=26 LONG  T+300s ... wall=9.3/10.2  ...
```

Every tier carries a real `cur/entry` pair. Occurrences of `wall=None/`: **0**. `[WALLS]`
fetch-failure lines: **0**.

### 1.6 Verdict, and its honest limits

> **No recheck tier in SOL's history was ever written `t+N_ok` on unmeasured wall data. Every
> stored `recheck_status` means what it says. Nothing to re-open — the 17:47 fix is forward-looking
> protection, not remediation.**

⚠️ **Coverage honesty.** The journal directly witnesses only vpos 25–26; the sampler starts
2026-07-08. For vpos 7–14 the evidence is the complete stored-prompt series (which shows OKX up on
every consultation outside 2026-06-30) plus the 20/20 measured baselines. That is strong but it is
inference, not a per-tier log. **It is not possible to do better**: per-tier history was never
persisted — `recheck_status` holds only the latest value, overwritten each tier. Recorded rather
than glossed.

**This is the good outcome, and it is worth stating plainly:** the past recheck record can be
trusted, which was the point of asking.

---

## 2. ✅ THE BYBIT CAPTURE IS NOW AN EXPLICIT, REASONED EXCEPTION

**Operator decision, recorded in `OPEN-ITEMS-SOL.md` so it is not re-litigated in a future venue
sweep.** `microstructure.kick_off_capture` — **Bybit depth-20** → `orderbook_json` + `tape_json`,
fired at `main.py:2365 / 3537 / 3707 / 4135` — **keeps its current source.** It is the only
remaining Bybit book reader on SOL, and it is an **exception, not an oversight**:

- **The standing OKX-4000 rule is about figures that FEED DECISIONS.** The shallow book is
  uninformative as an **input** — that is the rule's stated rationale. This capture is not an
  input to anything.
- **Its book half feeds nothing.** `orderbook_json` has been read by no one since the 17:08
  `advisor_book_json` fix repointed the learning loop.
- **Its tape half is executed-trade data** — aggressor pressure, whale counts — with **no OKX
  equivalent in the current code**. Repointing it would **delete the tape and the ladder**, not
  swap a source.
- **It has a purpose the rule does not cover:** it records what the venue we would actually trade
  on looked like at fill — **slippage evidence the moment SOL goes live.**

**Lapse condition recorded with the exception:** if it ever starts feeding a decision, the rule
applies again and the exception ends.

---

## 3. 📋 THE POST-WINDOW LIST — now a single block at the top of `OPEN-ITEMS-SOL.md`

Both items are deferred **only** because acting now would disturb the freeze or the evidence that
the freeze holds. Neither is optional.

| # | item | why deferred |
|---|---|---|
| **1** | **Restrict `ADVISOR_WALL_ALIGNED_V2` to `mult < 20`** — pre-registered 2026-08-02 with reversal conditions **R1** (a flip at `mult ≥ 20` that closes profitably — vpos 26 itself qualifies) and **R2** (window data showing the verdicts are sound at that size, judged on realised PnL) | the flag is **inside** the frozen surface |
| **2** | **Correct `claude_advisor.py:287` and `:420`** — they name the advisor's book as *"microstructure … depth-100 … Bybit for SOL"*; it has been **OKX-4000 since 2026-06-03** | both are comments and **neither reaches the model** (`_format_pre_trade_walls` never emits a venue name), but the file holds the frozen prompt and **its mtime is the evidence the freeze rests on** |

Item 2 is the **fourth** instance on this system of a label that does not say what the code does.

---

## VERIFY

```bash
cd /mnt/volume_nyc1_1780480650620/mercury-sol

# Path A — every baseline measured
sqlite3 "file:trades.db?mode=ro" "select count(*), sum(entry_wall_baseline_mult is null or
  entry_wall_baseline_mult=0) from virtual_positions;"                       # -> 20 | 0

# Path B — OKX availability over the complete history
sqlite3 "file:trades.db?mode=ro" "select
  sum(ai_user_prompt like '%Order book (pre-trade): unavailable%'),
  sum(ai_user_prompt like '%Order book (pre-trade, % levels)%')
  from trades where ai_user_prompt is not null;"                             # -> 3 | 3030

# no outage ever inside a 300s recheck window
sqlite3 "file:trades.db?mode=ro" "select t.id from trades t join virtual_positions vp
  on julianday(t.timestamp) between julianday(replace(substr(vp.opened_at,1,19),'T',' '))
  and julianday(replace(substr(vp.opened_at,1,19),'T',' '))+300.0/86400
  where t.ai_user_prompt like '%Order book (pre-trade): unavailable%';"      # -> no rows

journalctl -u mercury-sol | grep -c "wall=None/"                             # -> 0
```

_2026-08-02. Mercury-SOL is PAPER. No code changed in this report; the entry prompt is
byte-identical, the window stands at 86/200 and is not reset. **Titan was not read and not
modified.**_
