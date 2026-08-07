# SOL — heartbeat age is now in the DAILY DIGEST. "No signals arrived" can no longer be confused with "the poller was dead".

**2026-08-07 23:25 UTC** · Mercury-SOL · digest is a **separate read-only process** — the trading path
was not touched and the bot was **not restarted**.
Builds the proposal from `2026-08-07-2310-sol-poller-heartbeat-applied-observational.md` §2.
Titan (`/root/titan-bot`): untouched — 0 changes, HEAD `897850b`.

---

## 🔴 FIRST, A CORRECTION TO MY OWN §2

I wrote that "the digest already parses the journal, so this is a grep and a subtraction."
**That was wrong.** `silence_digest_sol.py` reads **only** `trades.db` (read-only) plus `config`.
It had no journal access at all.

So this is a **new read**, not a reuse — which is precisely why it carries its own subprocess
timeout, its own swallow-everything guard, and its own try/except around the whole block. Had I
believed my own claim, none of that would have been obviously necessary.

---

## WHAT SHIPPED

**One file, `silence_digest_sol.py`.** Backup `silence_digest_sol.py.bak_hbage_20260807`.
No restart: the digest is a cron job at 08:20 UTC in its own process. Bot still on **pid 3147176**,
`NRestarts=0`, untouched.

### Live rendered output (`--dry`, nothing sent)

```
🔇 MERCURY-SOL — SILENCE LEDGER
window: last 24h → 2026-08-07 23:20 UTC
mode: 🔴 LIVE · open positions: 0

✅ POLLER ALIVE · last beat 12s ago (23:20:21 UTC) · ticks=109 · open=0 · mode=LIVE
  5 beat(s) in the window · the loop iterated, so the silence below is a real
  verdict, not a dead thread.

✅ NOTHING NEEDS HANDS — no unresolved alerts, no open rows, …

WHY IT WAS QUIET — per cause
  webhooks logged    208 rows → 125 market events …
```

---

## 2. 🔴 PLACEMENT — above everything it invalidates

It sits **immediately after the mode line, ahead of NEEDS HANDS and the funnel** — the same logic the
blocked-sides block already used: a stale heartbeat changes how every number below must be read.

**And one placement decision the brief did not ask for but the code demanded:** `build()` has an early
return —

```python
if not rows:
    A('NOTHING ARRIVED AT ALL.  No webhook in the window —')
    return '\n'.join(L)
```

A day with **no webhooks at all** is exactly when a dead poller matters most. Put below that return,
the heartbeat block would have vanished **on the very day it is needed**. It is deliberately above it.
Verified by test 7: the block's offset precedes both NEEDS HANDS and the funnel.

## 3. THE VERDICT IS IN THE LINE, not just the age

Four distinct verdicts, each stated, per §1d of the 23:10 report:

| condition | rendered |
|---|---|
| age < 10 min | `✅ POLLER ALIVE · last beat 12s ago · ticks=109 · open=0 · mode=LIVE` + "the silence below is a real verdict, not a dead thread" |
| age > 10 min, **service active** | `🔴 POLLER HEARTBEAT — STALE. THREAD LIKELY DEAD. ACT.` + age, ticks, open, mode + **every number below is unverified** |
| age > 10 min, **service NOT active** | `⚠️ STALE, and the service is NOT active … The bot is down, which explains the silence below. Restart from flat.` — a **different** problem, not a dead thread |
| `open` non-zero behind a stale beat | `🔴🔴🔴 2 OPEN POSITION(S) WITH A DEAD POLLER — NO MANAGER. HIGHEST PRIORITY.` |

That last line is the whole point of carrying `open=` and `mode=` through from the beat: the worst
state in the system is a live position with no manager, and the operator now sees it **without
decoding anything**.

The stale/active split matters — a stopped service and a dead thread inside a running service need
different actions, and an age number alone cannot tell them apart. `systemctl is-active` is read-only
(a query, not a state change).

## 4. NO HEARTBEAT FOUND → SAID EXPLICITLY, NEVER OMITTED

```
🔴 POLLER HEARTBEAT — NOT FOUND
  no [HEARTBEAT] line in the last 24h · service is active
  Cannot confirm the poller thread ticked. Either the heartbeat build is not
  deployed, or the thread never ran.
  🔴 EVERY NUMBER BELOW IS UNVERIFIED — refusals counted on a dead poller are
  not the gates working.
```

Two causes are named and **not guessed between** — the heartbeat only began existing at 22:59 today,
so a window reaching back before that legitimately has no line. An absent section is
indistinguishable from one that failed to render; that is the `pending`-bucket lesson and it is why
this path exists at all.

A journalctl failure renders separately: `journal unreadable (journalctl failed or timed out)`.

## 5. IT CANNOT CHANGE A DECISION, CANNOT WRITE, CANNOT SUPPRESS

- **Changes nothing the bot decides.** Different process, different schedule, started by cron. It
  never imports `main` or `virtual_trader`; the bot was not restarted and its pid is unchanged.
- **No DB write.** Its only DB access is `file:{DB_PATH}?mode=ro` — SQLite refuses writes at the
  driver level. Test 8 asserts **every** connection carried `mode=ro`.
- **Cannot suppress the rest of the digest.** Three nested guards: `_run` collapses *every* failure
  (missing binary, permissions, non-zero exit, **15 s timeout**) to `None`; `_heartbeat` returns a
  reason string instead of raising; `_heartbeat_block` wraps the lot in its own `try/except`.
  **Test 6 injects a raising `_run` and asserts the funnel still renders** — the failure is stated
  (`could not be determined`) and the digest survives it.

---

## PROVEN BY EXECUTION — 8 scenarios, exit 0

| # | scenario | result |
|---|---|---|
| 1 | fresh beat (3 min) | ALIVE, carries ticks/open/mode |
| 2 | stale 45 min + active + **open=2** | THREAD LIKELY DEAD **+ worst-case line** |
| 3 | stale 45 min + **inactive** | correctly does **not** cry dead thread |
| 4 | no `[HEARTBEAT]` line | block present, reason stated |
| 5 | journalctl fails (`None`) | "journal unreadable" |
| 6 | **`_run` raises** | **digest still renders**, failure stated |
| 7 | placement | heartbeat before NEEDS HANDS *and* before the funnel |
| 8 | writes | every connection `mode=ro`; leak assert clean |

In every one of scenarios 1–6 the funnel still rendered.

### Isolation used, and why it suffices — argued, then verified

**Not** the 13/14-vector rewrite, and here is the justification rather than an assumption:

- The digest is a **single file** and imports **no bot module that holds a DB path**. I checked the
  indented imports too, not just top-level: only `config` (whose two `trades.db` mentions are
  **comments**, confirmed) and, at send time, `full_report`. There is no second module with a
  writable path — which is the entire reason the 13-file rewrite exists.
- Its DB handle is opened `?mode=ro`, so writes are refused by the driver.
- The new reads — `journalctl`, `systemctl is-active` — are read-only.

So a copy of the one file with its one `DB_PATH` repointed, **plus the `sqlite3.connect` leak
assert**, closes every path to production. The leak assert was kept regardless: it has caught a real
isolation break twice in two sessions, both times something review had missed.

---

## Rollback

`cp -p silence_digest_sol.py.bak_hbage_20260807 silence_digest_sol.py`. No restart, no schema, no
state — the digest is stateless and read-only. Reverting removes lines from one daily message.
