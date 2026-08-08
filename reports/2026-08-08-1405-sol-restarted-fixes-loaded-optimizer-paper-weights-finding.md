# sol-restarted-fixes-loaded-optimizer-paper-weights-finding

_2026-08-08 14:05 UTC_

---

# Mercury-SOL — RESTARTED with the fixes loaded. Boot touched nothing. One finding you need.

**The service is up on the fixed code, the boot path detected the orphan and adopted nothing, the
venue position is byte-identical to before the restart, and the LONG side is blocked. Titan was not
touched. One thing I found while answering §2 that you did not ask about and should see: the
optimizer timer is LIVE, it ran six minutes after the restart, and it wrote weights derived from a
100% PAPER cohort into the LIVE bot's entry scoring.**

Prior: [forensics 13:21](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1321-sol-live-forensics-three-entries-one-open.md)
· [diffs 13:40](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1340-sol-service-stopped-three-fixes-for-approval.md)
· [AST verification 13:54](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1354-sol-three-fixes-applied-ast-verified-not-restarted.md)

---

## 1. RESTART — ALL FIVE CONFIRMATIONS

`systemctl enable` → symlink recreated. `systemctl start` at **13:57:57 UTC**. Worker pid **3484439**.

### (a) BOOT GEOMETRY — exact match

```
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h OBSERVATION_MODE=False [pid 3484439]
```

Character for character what you specified.

### (b) THE WORKER IS RUNNING THE EDITED CODE

```
tor_retry.py   13:49:02        main.py   13:50:55
tor_retry.pyc  13:51:00        main.pyc  13:51:00      ← both .pyc POST-DATE both sources
worker started 13:58:18                               ← after the .pyc
```

Stronger than mtimes — the `.pyc` **header** records the source mtime Python saw at compile time:

```
main.pyc      records source mtime 2026-08-08 13:50:55Z | actual main.py      13:50:55Z | MATCH=True
tor_retry.pyc records source mtime 2026-08-08 13:49:02Z | actual tor_retry.py 13:49:02Z | MATCH=True
```

Both match, so Python considered the cache current and did **not** recompile — the worker loaded
exactly the bytecode I verified. And `grep -rn importlib *.py` returns **zero** reload paths (the
single hit is a comment in `config.py` stating there are none), so nothing can have swapped the
module out afterwards. This is the deployment-gap check from 2026-08-06 done both ways.

### (c) 🔴 THE BOOT PATH DID NOT TOUCH THE POSITION

Every boot line that could have:

```
13:58:17 [SMART-CLEANUP] Skipping stop cancel — position still open on exchange for SOL/USDT:USDT
13:58:18 [AP] No active positions in DB — clean boot.
13:58:18 [BOOT-ASSERT] 🔴 ORPHAN: LONG open on venue with NO database row — contracts=1.3 entry=74.8 stopLoss=73.89
13:58:19 [VPOS-RECONCILE] no open paper positions at boot — clean.
```

`_smart_boot_cleanup` saw the open position and **skipped the stop cancel** — which is the branch
that exists for exactly this. `BOOT-ASSERT` **named the orphan and did not adopt it**. No
`STOP-MOVE`, no `create_market_order`, no cancel anywhere in the boot log.

Venue re-read after boot:

| field | before restart | after restart |
|---|---|---|
| size | 1.3 | **1.3** |
| avgPrice | 74.80 | **74.80** |
| stopLoss | 73.89 | **73.89** |
| **openTime** | 1786179014459 | **1786179014459 — unchanged** |
| conditional | Untriggered qty 1.3 @ 73.89 | **Untriggered qty 1.3 @ 73.89** |
| positionIdx 2 | size 0 | size 0 |

`openTime` unchanged is the proof that this is the *same* position object, not a re-opened one. Only
`unrealisedPnl` moved (+0.83 → +0.91), with the mark.

### (d) HEARTBEAT TICKING

```
13:58:22 [HEARTBEAT] alive ticks=1  (+1 in 3s)    open=0 mode=LIVE pid=3484439
14:03:22 [HEARTBEAT] alive ticks=27 (+26 in 301s) open=0 mode=LIVE pid=3484439
```

26 ticks in 301 s at a 10 s cadence — nominal. `open=0` is **correct**: there is no ROW, and the
heartbeat counts rows, not venue positions. `mode=LIVE`.

### (e) LONG BLOCKED, SHORT OPEN

Replayed the gate's own arithmetic against the live venue, read-only:

```
side=long  contracts=1.3  entry=74.8  mark=75.508  uPnL=0.9204  SL=73.89  idx=1
side=short contracts=0.0                                                  idx=2

GATE open_count[LONG]  = 1 -> BLOCKED: max 1 LONG position(s) already open
GATE open_count[SHORT] = 0 -> passes
```

---

## 2. 🔴 THE OPTIMIZER LISTENER — AND SOMETHING BIGGER BEHIND IT

### What the listener can change

`optimizer_listener.py` long-polls Telegram `getUpdates` and acts only on a CONFIRM tap. On confirm:

| function | writes |
|---|---|
| `apply_proposal(pid)` | appends a filter to `optimizer/filters.json` (the bot re-reads filters per webhook — no restart needed, so it takes effect on the **next signal**) |
| `apply_proposal` → cycle advance | `settings.virtual_cycle_start_id` in `trades.db` |
| `apply_opt_proposal(pid)` | rewrites `optimizer/params.json`, and may append a filter from `worst_segment` |
| batch counters | `settings.batch_trade_count`, `settings.batch_number` |

So yes — it can change what the live bot refuses to trade, and its tuning params.

### Is there a pending proposal a stray tap could apply? **No.**

```
MISSING: optimizer/proposals     ← the directory does not exist
MISSING: optimizer/filters.json
MISSING: optimizer/params.json
optimizer/ contains only: dynamic_weights.json, tg_offset.txt
```

And the optimizer's own run today reported `Accumulating data — no analysis yet` (21/30 closed
pairs), so no proposal was generated. A stray tap on any **old** Telegram message would hit
`apply_proposal`'s first line — `if not p_file.exists(): return False, f"Proposal {pid} not found."`
— and write nothing. `apply_opt_proposal` is guarded the same way. **A stray tap today is inert.**

### Does the 2026-08-06 paper-dominated-cohort guard cover it? **NO — and the premise it rests on is now false.**

The comment at `optimizer.py:101` says the coverage is *"gated on `not _is_paper(row)` and **SOL runs
in OBSERVATION_MODE**, so no paper row can produce any of them. This is coverage placed ahead of the
live flip."*

**SOL no longer runs in OBSERVATION_MODE** — the boot line I confirmed in §1(a) says
`OBSERVATION_MODE=False`. That comment describes the world before 2026-08-07 22:25. Also, that
`_is_paper` guard is not in the optimizer at all: it lives in `virtual_trader.py:2182` and governs
venue-exit *labels*, not cohort selection.

The only paper/live separation in the optimizer is the cohort filter:

```python
cycle_start_id = _get_cycle_start_id()
if config.OBSERVATION_MODE:
    cohort = [... if (_safe_get(o, 'is_virtual') or 0) and id > cycle_start_id]   # paper filter
else:
    cohort = [... if id > cycle_start_id]                                          # NO paper filter
```

Two holes:

1. **In live mode there is no paper filter at all.** Once live trades start closing, the cohort will
   mix paper and live rows in one pool. Right now that is invisible because 100% of closed rows are
   paper — but it is the same defect the Titan commit fixed, sitting unfired.
2. **The cohort does not govern the weight path anyway.** Its own comment: *"Dynamic weight update
   runs **regardless of observation mode** … train combo-weights on the FULL all-time `paired` set,
   NOT the current-cycle `cohort`."*

### 🔴 AND IT RAN SIX MINUTES AFTER THE RESTART

`mercury-sol-optimizer.timer` is **active and enabled**, `OnCalendar=*-*-* 14:00:00 UTC`,
`Persistent=true`. It fired at **14:00:01 today**, while I was writing §1:

```
14:00:04  Weight updates applied: 18 segments
14:00:04    ema9_slope_state_15m:Inclined_Up   0.274 → 0.222 (-0.0518) n=7  win=29%
14:00:04    news_overall:NEG                   0.704 → 0.654 (-0.0500) n=6  win=33%
14:00:04    macro_news_category:NEUTRAL        0.599 → 0.553 (-0.0454) n=11 win=36%
14:00:04  ⏳ Optimizer: Observation M.
14:00:04  Closed trades: 21/30
14:00:04  💰 Net: $-1622.6586
14:00:04  Accumulating data — no analysis yet.
```

`optimizer/dynamic_weights.json` mtime is now **2026-08-08 14:00** (was Aug 7 14:00). What that
cohort actually is:

```sql
SELECT COALESCE(is_paper,1), status, COUNT(*) FROM virtual_positions WHERE status='closed' GROUP BY 1,2;
  is_paper=1  closed  22          ← every single one
SELECT is_virtual, COUNT(*) FROM trades WHERE pnl IS NOT NULL GROUP BY 1;
  is_virtual=1  22                ← zero live closed rows
```

**All 22 closed rows are paper. The $-1622.66 is paper money.** And those weights are not
decoration — `weight_engine` reads `dynamic_weights.json`, and `main.py:3605` does
`adj_score = round(direction_score + _w_adj, 2)`, which is what the entry threshold gate compares.
Today's real entries show it in the log:

```
06:50:13 weighted_adj: dir=LONG raw=4.25 adj=+0.6215 final=4.87
08:35:11 weighted_adj: dir=LONG raw=3.75 adj=-0.4094 final=3.34
```

`raw → final` is the paper-trained adjustment moving a **live** entry score across the threshold.

**Stated plainly: paper dollars are steering live entry decisions right now, through the weight
path, and that path re-trained six minutes after this restart.** The filter path is safely gated at
21/30 and has no pending proposal; the weight path is not gated at all.

**I did not stop it, as instructed.** `mercury-sol-optimizer.timer`, `mercury-sol-optimizer.service`
and `mercury-sol-optimizer-listener.service` are all in the state you left them. Next firing:
2026-08-09 14:00:00 UTC.

---

## 3. RECORDED AS NOT CLOSED

**The fixed fill read has never run in the live entry path.** What is proven: it returns correct
`filled`/`average`/`fee` for three of today's real order ids, including the live position's own
(`filled=1.3 average=74.8 fee=0.09724`, matching the venue's `avgPrice` and `curRealisedPnl`); and
the exchange-level option reaches `fetch_order` with the call site unchanged, on **both** clients.
What is not proven: that an actual live entry books a row.

**The FIRST live entry after this restart is what closes it.** Until then: proven-in-principle, not
proven-in-flight. Same status for the 34040 fix (needs a real duplicate-stop set) and the entry gate
(needs a real double webhook) — both are unit-proven, neither has fired in production.

🔶 And note the ordering problem this creates: **the LONG side is blocked by the open position**, so
the next live entry can only be a SHORT. The LONG path — the one all three defects fired on today —
stays unexercised until the open position is resolved.

---

## 4. UNTOUCHED

- **The open position:** 1.3 SOL LONG @ 74.80, stop 73.89, unmanaged, no row. Nothing in this pass
  adopted, closed, moved or booked it. Every venue call I made this session was a read.
- **Titan:** `active / enabled`, `/root/titan-bot` file mtimes unchanged. Not touched at any point.
- **The optimizer units:** left running, as instructed.

## STATE

```
mercury-sol                        active / enabled   pid 3484439, up since 13:57:57 UTC
mercury-sol-optimizer.timer        active / enabled   next 2026-08-09 14:00 UTC
mercury-sol-optimizer-listener     active / enabled
titan                              active / enabled   UNTOUCHED
venue  LONG 1.3 @ 74.80  stop 73.89  openTime 1786179014459  uPnL +0.92
```
