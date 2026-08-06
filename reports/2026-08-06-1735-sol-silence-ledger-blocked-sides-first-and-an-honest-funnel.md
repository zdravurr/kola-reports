# SOL — THE LEDGER CAN NOW REPORT A BLOCKED SIDE, AND ITS FUNNEL COUNTS WHAT IT DESCRIBES

**2026-08-06 17:35 UTC · Mercury-SOL (PAPER) · APPLIED AND PROVEN BY EXECUTION.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`. **One file changed: `silence_digest_sol.py`.**
Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched.**

**This was the last item.**

---

## THE ANSWER FIRST

With three unresolved alerts and two open rows seeded, the digest previously rendered **nothing** about
any of them — the only hint was `open positions: 2` in the header, which names neither the side nor the
block. It now opens with:

```
🔴 NEEDS HANDS — READ THIS BEFORE THE FUNNEL
  🚫 BLOCKS LONG · sl_failsafe_close_failed
      stop unset AND emergency close failed · SOL/USDT:USDT LONG · fired 2026-08-06T09:30:00+00:00
  ⚠️ non-blocking · partial_fill_unreadable
      partial leg fill unreadable · SOL/USDT:USDT SHORT · vpos=901 · fired 2026-08-06T11:00:00+00:00
  🚫 BLOCKS SHORT · exchange_close_unsubstantiated
      venue FLAT, closing fill unreadable · SOL/USDT:USDT SHORT · vpos=901 · fired 2026-08-06T12:00:00+00:00
  ⚠️ position with NO stop               1 row(s) in window  [naked_position_unprotected]
  ⚠️ stop failed, no position found      1 row(s) in window  [sl_failed_no_position]
  ⚠️ entry failed                        1 row(s) in window  [failed]
  🚫 OPEN ROW vpos 901 · SOL/USDT:USDT SHORT · LIVE · opened 2026-08-06T08:00:00+00:00
  🚫 OPEN ROW vpos 902 · ETH/USDT:USDT LONG · paper · opened 2026-08-01T08:00:00+00:00  ← 🔴 NO ALERT ROW for this open position
  ⚠️ ALERT with NO open row · SOL/USDT:USDT LONG — the row was settled but the alert is still
     unresolved; clear it or it will suppress the next one
```

And the funnel's `entry attempts` went **1832 → 1843** on the same data: it now counts the eleven
refusals it was already describing.

---

# 1. BLOCKED SIDES

## a) At the TOP, before the funnel

Placed first, deliberately, with the reason written at the code: **a blocked side changes how every
number below it must be read. Refusals on a blocked side are not the gates working — they are the
block.** Under the funnel it would invite exactly the wrong reading.

Each entry gives stage, symbol, side, vpos id (parsed out of `detail`), when it fired, and the
operative fact — **whether it BLOCKS that side**:

| stage | blocks? | why |
|---|---|---|
| `sl_failsafe_close_failed` | 🚫 **yes** | position live and unstopped |
| `entry_fill_unreadable` | 🚫 **yes** | venue position, no row; boot assert refuses to trade over it |
| `exchange_close_unsubstantiated` | 🚫 **yes** | row left open (today's A6) |
| `boot_orphan` | 🚫 **yes** | orphan found at boot |
| `partial_fill_unreadable` | ⚠️ **no** | the position is live and **managed** — only the partial leg failed; it occupies its side the way any open position does, which is not a stale block |

An unknown future stage defaults to **blocking** — the safe direction for something we have not
classified.

## b) Never an omitted section

```
✅ NOTHING NEEDS HANDS — no unresolved alerts, no open rows, no money-path statuses
   in the window. No side is blocked.
```

One line when there is nothing, never silence. **An absent section is indistinguishable from a section
that failed to render, and this bot has been bitten by exactly that.** That is the line the production
run prints today.

## c) Cross-checked against `virtual_positions WHERE status='open'` — both directions

A stale open row blocks a side **even with no alert row** — true of A6 before today, and of any row
predating this ledger. So both sources are read and **every disagreement is named**:

* **open row, no alert** → `← 🔴 NO ALERT ROW for this open position` (vpos 902 above)
* **alert, no open row** → the row was settled but the alert was never resolved; and it says why that
  matters: *"clear it or it will suppress the next one"* — because A6's dedup keys on an unresolved row.

Open rows are also marked **`LIVE`** vs **`paper`**, which after the flip is the difference between
"the bot is holding real money" and "a paper row is stuck".

---

# 2. THE FUNNEL NOW COUNTS WHAT IT DESCRIBES

Six statuses joined the ladder as `GATES_EXTRA` — each verified from its emission site to be an
`update_trade()` on an **entry** row that stops that entry:

```
spread_blocked · filter_blocked · fee_gate_rejected · wall_blocked · bypass_flat_skipped · neutral1h_unconfirmed
```
plus **`ai_hold`** into `ADVISOR`, where it belongs — it is an advisor verdict (`ai_decision='hold'`),
not a gate.

Kept as a **separate ordered list** rather than merged into `GATES`, because `GATES`' order is the
verified runtime funnel and this group's is not: it is ordered by emission site (main.py 3371 → 4478),
which is a proxy, not a trace. **Saying so beats implying an order I have not established.**

## 🔴 What I did NOT add, and why

Adding a non-refusal would overstate the funnel — the same defect as understating it, pointed the other
way. So these stay out, and stay available to the bucket:

| status | why not |
|---|---|
| `neutral1h_armed` | an **arming**, not a refusal |
| `shadow_armed_pending_close` | a `virtual_positions` lifecycle state |
| **`pending`** | `insert_signal`'s **default** for a freshly written row (main.py:1139) — "not yet resolved", never a refusal. **This is the status whose mis-bucketing started all of this. It stays in UNCLASSIFIED.** |
| `stalled` / `active` / `open` / `closed` / `completed` | lifecycle, not entry outcomes |
| `tightened` | 🔶 **not a `trades.status` at all** — it is `recheck_status` on `virtual_positions` and can never reach `by_status`. It was on the candidate list; it does not belong on any list. |

## 🔴 The UNCLASSIFIED bucket is unchanged in kind — proven

Widening `known` narrows what the bucket surfaces, which is the one thing that must not happen. So the
proof seeded a status **neither of us classified**:

```
⚠️ UNCLASSIFIED STATUSES (not in the ledger's ladder — shown so nothing is silently dropped)
  some_future_status                1
```

**It still catches the unknown**, and now catches *only* the unknown — the classified ones moved to
their proper places instead of sitting in a bucket labelled "we do not know what this is".

---

# 3. THE MONEY-PATH STATUSES — FOLDED INTO THE TOP BLOCK

`naked_position_unprotected` · `sl_failed_position_closed` · `sl_failed_no_position` · `failed` ·
`closed_unrecorded_pnl`

**I chose to fold them into the §1 block rather than give them their own line.** They are not entry
refusals, so they must stay out of the funnel — but they *are* "stop and look" facts, and a reader
scanning one block for *is anything wrong* should not have to find a second one further down. They are
counted in `known`, so they never fall to UNCLASSIFIED either.

---

# 4. IT CHANGES NOTHING THE BOT DECIDES

```
$ grep -rn "silence_digest" --include=*.py .        → only its own usage line
```

**It is a standalone cron script, never imported by the bot** — so **no restart was needed and none was
performed.** The service is still `MainPID 2756504`, up since 16:59:32, from the A6 pass.

```
$ grep -n "execute(" silence_digest_sol.py | grep -iE "insert|update|delete|drop|create"
(empty — no write statement anywhere)
```

And the DB is opened `sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True)`. **SQLite enforces that
harder than any assert of mine could** — demonstrated:

```
$ INSERT INTO naked_position_alerts …  on a mode=ro handle
✅ write refused by SQLite: attempt to write a readonly database
```

## The production run, live path

```
🔇 MERCURY-SOL — SILENCE LEDGER
window: last 24h → 2026-08-06 17:28 UTC
mode: PAPER (OBSERVATION_MODE=1) · open positions: 0

✅ NOTHING NEEDS HANDS — no unresolved alerts, no open rows, no money-path statuses in the window.
   No side is blocked.

WHY IT WAS QUIET — per cause
  webhooks logged    344 rows → 218 market events (×1.58)
  …
```

---

# 5. ISOLATION — ONE FILE, NOT THIRTEEN, AND WHY THAT SUFFICES

**Stated plainly, as asked.** The 13-file rewrite exists because the **engine's** modules each hardcode
`DB_PATH` and each **write**; a test that rewrote one of them would have the other twelve writing into
the live book. `silence_digest_sol.py` is a different shape:

* it opens **exactly one** database, and opens it **`mode=ro`**;
* it contains **no** `INSERT`/`UPDATE`/`DELETE`/`CREATE` — verified by grep;
* it imports **nothing from the tree** except `config` (for the mode line).

So rewriting that single constant fully isolates it, and SQLite's own read-only enforcement is a
stronger guarantee than the external leak assert the engine tests need. Residual production DB paths in
the copy: **0**.

*(The isolated copy prints `mode: mode unknown` because `config.py` is not beside it — cosmetic to the
test and irrelevant to what is being measured. Production prints the real mode, shown above.)*

## Both directions, on the same seeded book

Seeded: **3 unresolved alerts** (2 blocking, 1 not; one with no matching row) · **2 open rows** (one
with an alert, one without) · **3 money-path statuses** · **11 gate-extra rows** · **1 status neither
of us classified**.

| | PRE-FIX | POST-FIX |
|---|---|---|
| blocked sides shown | **🔴 none** (only `open positions: 2` in the header) | ✅ **3 alerts + 2 open rows, sides named** |
| money-path statuses | in UNCLASSIFIED, uncounted | ✅ in the top block, counted as known |
| open-row / alert disagreements | not detected | ✅ **both directions flagged** |
| funnel `entry attempts` | **1832** (11 refusals uncounted) | ✅ **1843** |
| `wall_blocked` / `spread_blocked` | UNCLASSIFIED | ✅ funnel lines: 7 / 4 |
| unknown status | UNCLASSIFIED | ✅ **still** UNCLASSIFIED |

---

# 6. FINAL STATE

```
silence_digest_sol.py  — the only file changed; standalone cron script, no restart needed
backup                 — silence_digest_sol.py.bak_ledger_blindspot_20260806
mercury-sol.service    active · MainPID 2756504 · up since 16:59:32 (unchanged by this pass)
open / active / exit_pending : 0 / 0 / 0
TITAN: git clean · HEAD 897850b · NOT TOUCHED
```

**The digest can now report that the bot was quiet because a side is blocked — which was the one thing
it was built for and could not do.**

*Generated 2026-08-06 17:35 UTC.*
