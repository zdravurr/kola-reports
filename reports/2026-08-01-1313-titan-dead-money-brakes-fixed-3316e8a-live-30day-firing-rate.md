# titan-dead-money-brakes-fixed-3316e8a-live-30day-firing-rates

_2026-08-01 13:13 UTC_

---

# TITAN — BOTH PORTFOLIO MONEY-BRAKES WERE INERT SINCE MAY. FIXED, LIVE (`3316e8a`)

_2026-08-01 13:15 UTC · `54dc734` → **`3316e8a`** · LIVE, real money · restarted 13:08:26_

## DECISION LINE

**Shipped and live.** Both brakes now read realised P&L from
`virtual_positions(status='closed').net_pnl`, coverage proven against the live DB rather than assumed.
Nothing was retuned; no re-entry cooldown was added.

🔴 **ONE THING NEEDS YOUR DECISION, and it is a calibration question, not a defect.** Over the last
30 days the two brakes behave completely differently, and the difference is **position size**:

- **Loss-streak halt — FIRES OFTEN AND FIRES NOW.** It is count-based and size-blind: 13 windows,
  52 halted hours, **7.2% of the last 30 days**. In the live-size era it fired **twice in two days**
  and would have blocked **2 of the 5 live entries** — including **vpos 89, the only winner in the
  §2.4 sample (+2.30)**.
- **Daily-loss halt — WOULD HAVE FIRED ON 12 OF 18 TRADING DAYS, but every one of those days was at
  68× the current size.** At today's $146 notional it needs **~13 full-stop losses in one UTC day** to
  trip. Fixing the query made it *capable*; at current size it is effectively dormant.

I did not change `LOSS_STREAK_THRESHOLD=3`, `LOSS_STREAK_COOLDOWN_HOURS=4` or
`DAILY_LOSS_PCT_LIMIT=0.05`. **A brake that would have blocked the sample's only winner is your call
to calibrate, not mine to quietly soften.**

---

## 1. THE DEFECT, AND THE SOURCE THAT REPLACES IT

### What was wrong

Both brakes read `trades` rows whose `signal_type` was in a hardcoded tuple:

```python
_CLOSE_SIGNAL_TYPES = ('5m_group_b', 'close_long', 'close_short', 'exit_long', 'exit_short')
```

That tuple encodes an assumption that stopped being true: **that a close writes its own row.** It does
not. Every close route propagates P&L back onto the **ENTRY** row, whose `signal_type` is
`open_long` / `open_short`.

🔴 **The entire database contains ONE row matching that tuple — id 186, `close_long`,
2026-05-11 21:18:16.** So for two and a half months:

| function | what it returned, every call | consequence |
|---|---|---|
| `loss_streak_halt()` | `(False, '1/3 closes recorded')` | `len(rows) < 3` → never evaluated the streak |
| `daily_realized_pnl()` | `0.0` | `daily_loss_halt()` took the `pnl >= 0` branch forever |

**The tell was in the code's own comment**, and it is worth quoting because it shows this was a seam,
not carelessness:

> *"we filter on these ... because the AI close path **also** propagates pnl back to the entry row,
> and we don't want to double-count."*

The author knew the entry row carries the P&L and excluded it — **correctly, if a close row also
existed.** When close rows stopped being written, the exclusion became the whole set.

### The source that replaces it, and why it is right

`virtual_positions(status='closed').net_pnl`, with the predicate
`status='closed' AND closed_at IS NOT NULL AND net_pnl IS NOT NULL`.

**It is the position ledger for both paper and live** — it carries the real exchange `stop_order_id` —
and it is the only place where **one close is one row**. Each of the following was checked against the
live DB, not reasoned about:

| question you asked | answer | evidence |
|---|---|---|
| **Does it cover every close route?** | Yes, and **by construction** — the predicate names **no route** | present today: `sl`(28) `trail`(15) `external`(10) `ai_exit`(4) `post_entry_critical`(1) |
| **What about `breakeven`?** | It is a **fifth defined route** (`virtual_trader.py`, passive-fill reconciliation, `_reason = 'breakeven' if breakeven_applied else 'sl'`) that has produced **0 rows so far** — and it needs **no code change** to be counted | route-agnostic predicate |
| **What about `sl` / `trail` / `signal` / `external`?** | All present above. `external` (10 rows) is the reconciled/manual route | — |
| **Are partial exits double-counted?** | **No — `net_pnl` already CONTAINS the partial** | vpos 82, the only position that ever took one: gross 42.4633600 + partial 18.9070939 − fees 6.6849138 − funding 0.8929330 = **53.7926072 = `net_pnl` exactly** |
| **Any other double-count risk?** | Yes, and reading ONE table is what avoids it | six `15m_armed_exit` rows in `trades` carry pnl **byte-identical** to a `virtual_positions` row (vpos 54/60/64/75/76/84). The old tuple would have needed a seventh member and still been wrong |
| **Anything excluded that shouldn't be?** | `status='archived_pre_geometry_fix'` (6 rows) is correctly invisible; legacy `trades` id 186 (2026-05-11) predates the ledger entirely (first vpos close 2026-05-22) | — |

🔴 **ENUMERATING ROUTES IS THE DEFECT BEING FIXED.** The new predicate deliberately lists none, so a
future close route is counted the day it ships rather than the day someone remembers to add it.

**Ordering is by `closed_at`, not `id`** — `id` is *entry* order, and a LONG opened earlier can close
after a SHORT opened later. `closed_at` is ISO-8601 `+00:00` on **58 of 58** rows, so lexical order is
chronological; verified rather than assumed.

---

## 2. WHAT EACH WOULD HAVE DONE OVER THE LAST 30 DAYS

Window 2026-07-02 12:25 → 2026-08-01 12:25 UTC. **29 closes, 29 entries.**

🔴 **READ THIS FIRST — THE WINDOW SPANS A 68× SIZE CHANGE.** vpos 62–85 ran at **~$10,000 notional**
(paper); vpos 86–90 run at **~$146** (live, from 2026-07-30 00:50). Historical firing rates for the
*percentage* brake are therefore **not** predictive of its future rate. Splitting is not optional here.

### 2a. Loss-streak halt — count-based, size-blind, FIRES

**13 trigger events · 13 distinct halt windows · 52.0 halted hours = 7.22% of the 30 days.**

| halt window (UTC) | triggered by vpos | their P&L |
|---|---|---|
| 07-03 02:30 → 06:30 | 60, 61, 62 | −62.03 / −169.02 / −72.79 |
| 07-03 09:01 → 13:01 | 61, 62, 63 | −169.02 / −72.79 / −45.57 |
| 07-06 00:24 → 04:24 | 65, 66, 67 | −41.35 / −59.11 / −32.73 |
| 07-06 14:25 → 18:25 | 66, 67, 68 | −59.11 / −32.73 / −4.52 |
| 07-06 21:15 → 01:15 | 67, 68, 69 | −32.73 / −4.52 / −50.64 |
| 07-09 23:16 → 03:16 | 68, 69, 70 | −4.52 / −50.64 / −44.42 |
| 07-10 20:26 → 00:26 | 69, 70, 71 | −50.64 / −44.42 / −30.78 |
| 07-11 15:37 → 19:37 | 70, 71, 72 | −44.42 / −30.78 / −74.61 |
| 07-11 22:49 → 02:49 | 71, 72, 73 | −30.78 / −74.61 / −43.54 |
| 07-13 08:46 → 12:46 | 72, 73, 74 | −74.61 / −43.54 / −73.09 |
| 07-15 02:00 → 06:00 | 73, 74, 75 | −43.54 / −73.09 / −14.52 |
| **07-31 02:06 → 06:06** | **85, 86, 87** | −137.32 / −2.54 / −0.82 |
| **07-31 10:35 → 14:35** | **86, 87, 88** | −2.54 / −0.82 / −0.53 |

**Real entries that would have been BLOCKED: 5** — vpos 63 (07-03 05:50), 71 (07-10 01:50),
73 (07-11 17:35), **89 (07-31 12:20)**, **90 (07-31 14:25)**.

🔴 **In the live-size era it fired twice in two days and would have blocked 2 of 5 live entries — and
one of those, vpos 89, is the only winner in the entire §2.4 sample (+2.30).** Stated plainly because
it is the strongest argument against switching this on unchanged, and it is not mine to suppress.

*Note the streak is size-blind by design: the 07-31 windows were triggered by a −137.32 loss at the
old size sitting next to −2.54 and −0.82 at the new one. Three losses is three losses to this brake,
whether they cost $210 or $3.89.*

### 2b. Daily-loss halt — percentage-based, and the percentage moved

Threshold: **−5% of equity = −$25.52** on the current $510.41 balance (historical equity is not
recorded; today's balance is used and that is an assumption, stated).

| date | n | day total | intraday trough | | date | n | day total | intraday trough |
|---|--:|--:|--:|---|---|--:|--:|--:|
| 07-03 | 2 | −118.36 | −23.19% 🔴 | | 07-17 | 2 | −87.39 | −17.12% 🔴 |
| 07-04 | 2 | −38.03 | −7.45% 🔴 | | 07-20 | 1 | −103.54 | −20.28% 🔴 |
| 07-05 | 1 | −59.11 | −11.58% 🔴 | | 07-22 | 1 | +80.10 | +0.00% |
| 07-06 | 3 | −87.89 | −17.22% 🔴 | | 07-24 | 1 | −116.58 | −22.84% 🔴 |
| 07-09 | 1 | −44.42 | −8.70% 🔴 | | 07-25 | 1 | +75.24 | +0.00% |
| 07-10 | 1 | −30.78 | −6.03% 🔴 | | 07-27 | 1 | +53.79 | +0.00% |
| 07-11 | 2 | −118.15 | −23.15% 🔴 | | **07-29** | 3 | **−264.44** | **−51.81%** 🔴 |
| 07-13 | 1 | −73.09 | −14.32% 🔴 | | **07-30** | 1 | −2.54 | −0.50% |
| 07-15 | 1 | −14.52 | −2.84% | | **07-31** | 4 | **+0.34** | −0.26% |

**12 of 18 trading days would have halted.** Worst: **2026-07-29, −264.44 = −51.81% of equity in one
day** — ten times the limit, with the brake watching and unable to see.

🔴 **But all 12 are old-size days.** In the live-size era (07-30, 07-31) the troughs are **−0.50%** and
**−0.26%** — nowhere near. At the live 1R (mean **$1.96** across vpos 86–90), tripping −$25.52 in one
UTC day needs **~13 full-stop losses**. **Fixing the query made this brake capable; at current size it
is effectively dormant.**

### 2c. So — are we switching on a brake that fires constantly?

**The daily-loss brake: no, not at current size.** It is now armed for the day size goes back up,
which is exactly what it is for.
**The loss-streak brake: yes, meaningfully.** 7.2% of wall-clock over 30 days, 2 of 5 live entries
blocked in its first live-size test, one of them the sample's only winner. **That number is yours to
accept or retune.** I changed no threshold.

---

## 3. DOES THIS TOUCH ANYTHING THE EXIT ADVISOR READS?

**No. Proven three ways, not asserted:**

1. **Call sites** — `risk_manager` is referenced from `main.py:518` (the import) and exactly three
   call sites, all `check_risk` on the **entry** path: `main.py:1982`, `:3794`, `:4284`. The two other
   greps that mention the module (`virtual_trader.py:6`, `:700`) are **comments**.
2. **The advisor's context builder** — `grep` for `risk_manager|loss_streak|daily_realized` inside
   `_build_exit_context` … `consult_exit_advisor`: **0 matches**. Nothing this module computes is
   rendered into the close prompt.
3. **Writes** — `INSERT|UPDATE|DELETE|COMMIT` in `risk_manager.py`: **0**. It is read-only against the
   DB, so it cannot change a figure the advisor reads even indirectly.

**§2.4-OP's freeze is not engaged.** Its scope is settled and explicit: *"frozen = everything the
advisor READS. NOT frozen = act/hold plumbing, logging, labels, close mechanics, and **the entire
entry side**."* This is an entry-side portfolio brake. **The window stands, the count stays 4 of ~10,
nothing is voided.**

⚠️ **One interaction worth your eye, stated rather than buried:** a brake that blocks entries changes
which positions exist, and therefore which positions the advisor gets to close. It does **not** void
the window (entry side is explicitly not frozen), but if the loss-streak brake runs unchanged it will
shape the remaining ~6 datapoints. That is a reason to decide the calibration question now rather than
after the window closes.

---

## 4. THE GUARD — §2.19's SHAPE, 6th PLACE

**The failure was not just a wrong query. It was a mechanism silently reading a set that could never
populate, and reporting the miss in the same voice as a real pass.** `'1/3 closes recorded'` reads
exactly like a threshold that was evaluated. It was not evaluated — it *could not be*.

```python
class PnlWindow:
    __slots__ = ('rows', 'source', 'required')

    def __init__(self, rows, source, required):   # NO DEFAULTS
        ...

    @property
    def blind(self):
        """True iff the ledger returned FEWER rows than this brake needs to
        make any decision at all. Never conflate with 'evaluated and passed'."""
        return len(self.rows) < self.required
```

- **The required-positional half** — a window cannot be constructed without stating its **source**,
  what it **asked for**, and what it **got**. There is no way to build one that does not know.
- **The WHERE-clause half** — `blind` is a property of the **data**, not a check a caller may forget
  to perform.
- **Three states now exist where there were two:** `halted` · `evaluated-and-passed` ·
  **`could-not-see`**.

A blind brake is loud and greppable:

```
[TITAN][RISK-BLIND] 🔴 INSUFFICIENT DATA — loss-streak halt CANNOT FIRE: 0 of 3 required
closes visible in virtual_positions(status='closed').net_pnl. This is NOT "evaluated and passed".
```

**And every reason string on every branch now names the source and the row count** — `'daily PnL
$+0.00 on $510.41 (0 closes today from virtual_positions(status=closed).net_pnl)'`. `$0.00 on 0
closes` and `$0.00 on 4 closes` are different facts and used to print identically.

**Verified live, both paths:**

| | before (`54dc734`) | after (`3316e8a`) |
|---|---|---|
| `loss_streak_halt()` | `(False, '1/3 closes recorded')` — could not decide | `(False, "streak broken by a winner (last 3 closes from virtual_positions(status='closed').net_pnl)")` — **decided** |
| `daily_realized_pnl()` | `0.0` — blind | `(0.0, 0)` — evaluated, 0 closes today |
| rows visible | **1**, from 2026-05-11 | **58** |
| forced-blind path | did not exist | prints `[TITAN][RISK-BLIND]`, returns the loud reason |

*Design note: `daily_realized_pnl` is called with `required=0` on purpose — summing today's closes is
meaningful at any row count, and zero closes today genuinely means zero realised P&L today. That is an
evaluated answer, not blindness. The brake that can go blind is the streak one, which needs a minimum
count before it can decide anything.*

---

## 5. NO RE-ENTRY COOLDOWN WAS ADDED — recorded as OPEN-ITEMS §2.36

Per your ruling, and I agree with the reasoning. Recorded as a **live structural question** with the
mechanism named:

> The exit advisor closes on a **15m/5m tier flip against the position** (4 of 4 closes cite it,
> 5 of 23 holds). The entry cascade opens on **the same 15m/5m tiers**. Neither knows the other
> exists — an `ai_exit` close writes `close_reason` and nothing else.

**Why nothing was built:** n = 1, and the direction is not established — **vpos 89 was the winner
(+2.30) and vpos 90 was a loser (−0.61)**. Building a cooldown now would suppress the very signal
§2.4 exists to measure, before the measurement finishes. And counted properly it has happened **once
in four closes**: 0/4 within 5 min, 1/4 within 15 min, 1/4 within 60 min; the other gaps were 104.7
and 448.5 minutes, and after vpos 90 the entry path produced nothing for 20 hours. **The 10-minute
case is not a rate.**

## 5a. §2.4 CAVEATS RECORDED — as caveats, not resets (§2.4-OP·3)

Written into OPEN-ITEMS §2.4 while the window is **open**, so none can be introduced later to explain
away a result. **The bar does not move and the count does not restart.**

1. **Fees exceed the sample's realised P&L** — 0.5849 paid vs +0.3423 realised; ~0.08R per decision.
2. **No closing threshold is readable** — the deepest adverse reading ever shown is **−0.36R**;
   25 of 27 consults land within ±0.4R of flat. A distribution with no tail cannot yield a threshold.
3. **vpos 90's held branch is unresolved** — marked to market, not terminated; its sign can change.
4. **The held branches are mutually exclusive** — `MAX_POSITIONS_PER_SIDE = 1`; holding 88 means 89
   and 90 never exist. Per-position arithmetic is not a portfolio result.

---

## 6. APPLY AND VERIFY

**Snapshot:** `risk_manager.py.bak_deadbrakes_20260801T130135Z` + a full `trades.db` copy, both in
`/root/backups/titan-brakes-20260801/`.

| check | result |
|---|---|
| `py_compile risk_manager.py` | ✅ OK |
| symtable free-global audit (FUNCTION scopes) | ✅ **CLEAN** — no name resolved to a global that is never assigned |
| commit | **`3316e8a`**, pushed `54dc734..3316e8a` |
| restart | **deliberate**, 13:08:26 UTC · `NRestarts=0` · `SubState=running` |
| errors since restart (traceback / CRITICAL / REFUSING TO START / no such column / OperationalError) | **0** |

**🔴 LIVE banner at $150 — verbatim:**

```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
[TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
```

**Four boot gates — verbatim, all green:**

```
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
[RECONCILE] boot reconciliation starting
[STOP-CLEANUP] no orphaned orders for LONG BTC/USDT:USDT
[STOP-CLEANUP] no orphaned orders for SHORT BTC/USDT:USDT
[RECONCILE] done
```

*This is the no-position form of the block. With a position open, gates 3–4 read `engine owns
positions — NOT enqueueing a breakeven job` and `<SIDE> open, SL present @ <px> — kept` instead of the
two `STOP-CLEANUP` lines. Same block, different branch — not a missing gate.*

**Runtime = commit, by hash:**

| file | disk sha256[:12] | `git show HEAD:` sha256[:12] | |
|---|---|---|---|
| `risk_manager.py` | `0e43773939a2` | `0e43773939a2` | ✅ |
| `config.py` | `e9f8b8365f92` | `e9f8b8365f92` | ✅ |
| `main.py` | `274867014973` | `274867014973` | ✅ |
| `virtual_trader.py` | `efc10b0a4fe8` | `efc10b0a4fe8` | ✅ |

Worker 1064336 started **13:08:36**; **sources newer than worker start: 0**. The pre-restart master
**PID 481805 is GONE** — this is a new process tree, so no module could have been carried across
(the `project_fix_on_disk_not_loaded` hazard applies to a daemon that was *not* restarted; this one
was).

**`CONFLUENCE_SCORE_THRESHOLD` = 3.0** — `config.py:386`, runtime import confirms `3.0`.

**Open position:** 🔴 **there is none, so "same exchange stop order id" could not be checked and is
not claimed.** Verified by **both probes** before and after the restart: ccxt `fetch_positions` → 0,
**raw `swapV2` `positionAmt != 0` → 0**, open orders → 0, and the boot reconciler independently agrees
(`0 exchange position(s), 0 open row(s)`). Last position closed 2026-07-31 16:25:42.

**Mercury-SOL: untouched.** `active`, up since **2026-07-21 06:39:33 UTC** — identical before and
after the restart. Not read, not written, not restarted.

## WHAT I DID NOT DO

- **Did not retune any threshold.** `LOSS_STREAK_THRESHOLD=3`, `LOSS_STREAK_COOLDOWN_HOURS=4`,
  `DAILY_LOSS_PCT_LIMIT=0.05` are byte-identical.
- **Did not add a re-entry cooldown** — recorded as OPEN-ITEMS §2.36 instead.
- **Did not touch the exit advisor, its prompt, or any figure it reads.** No file but
  `risk_manager.py` changed.
- **Did not void or restart the §2.4 window.** Still 4 of ~10.
- **Did not backfill or modify any DB row.** The fix is read-side only.
