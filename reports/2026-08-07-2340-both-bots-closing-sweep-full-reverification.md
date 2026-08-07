# CLOSING SWEEP — BOTH BOTS LIVE. Both clean. Two corrections, and one review trigger that has already fired.

**2026-08-07 23:40 UTC** · READ-ONLY. Nothing changed, nothing fixed, nothing restarted.
Titan `/root/titan-bot` — 🔴 LIVE (BingX, BTC) · Mercury-SOL — 🔴 LIVE (Bybit via Tor, SOL) since 22:25:18.

---

## VERDICT FIRST (§7)

**Nothing is half-applied. Nothing is silently stale. Both bots are clean.**

Three things you should know anyway, none of them a defect:

1. 🔴 **Titan's `ema_envelope_blocked` has reached 111 rows — the pre-registered review trigger was
   100. It is CROSSED and nobody has looked.** That is a commitment coming due, not a fault.
2. 🔴 **The brief's premise is out of date: Titan's EMA envelope gate and the 2026-08-04 geometry
   HAVE seen a closed position** — vpos 93, today, a complete live round trip. Details below.
3. **A correction to my own method:** my first `.pyc` probe reported `claude_advisor` STALE on both
   bots. That was **my script's bug**, not a real staleness — each tree holds a junk
   `claude_advisor.py.cpython-312.pyc` from June, and my `split('.')[0]` aliased it onto the real
   module, overwriting the correct result. Re-probed with exact filename matching:
   **Titan 37/37 match, SOL 28/28 match** for every module in either bot's import graph.

---

# §1 — IS WHAT WE THINK IS RUNNING ACTUALLY RUNNING?

## a) Services

| | **TITAN** | **MERCURY-SOL** |
|---|---|---|
| state | active | active |
| since | 2026-08-06 01:53:19 (**1d 21h**) | 2026-08-07 22:59:24 |
| master / worker | 2538048 / 2538082 | 3147176 / 3147213 |
| NRestarts | **0** | **0** |
| tracebacks since boot | **0** (of 1,772 log lines) | **0** |

Titan also runs `optimizer_listener` (2538053, same boot) and `gemini_bridge` (3647921, since Jul 28).

## b) 🔴 LOADED CODE — proven by `.pyc` embedded source mtime

**Titan: 37 modules checked, ZERO mismatches.** And the concern that HEAD (`897850b`, committed
01:55:45) postdates the worker boot (01:53:27) is **resolved**: no `.py` in the tree is newer than
the boot — the newest is `config.py` at 01:53:01. The commit merely *recorded* files already written.
**Titan is running HEAD.**

**SOL: 28 modules checked. Every module in the bot's import graph matches**, including the three
edited today:

| module | pyc src mtime | py mtime | match |
|---|---|---|---|
| `indicators` | 2026-08-07 21:09:11 | 21:09:11 | ✅ |
| `virtual_trader` | 2026-08-07 22:55:55 | 22:55:55 | ✅ |
| `main` | 2026-08-07 21:20:12 | 21:20:12 | ✅ |

Two SOL `.pyc` files do *not* match, and **neither is in the bot process** — verified: no module
imports either.

- `silence_digest_sol` — pyc 08-06 17:26 vs py 08-07 23:18. It is the **cron script**, and the
  mismatch is positive evidence: it confirms the digest **has not run since today's edit**. Next run
  08:20 UTC.
- `healthcheck` — both June 3, a standalone CLI script, untouched by anything today.

## c) Runtime flags, read the load-bearing way

**SOL** — `os.environ['MERCURY_OBSERVATION_MODE'] = '0'`, `config.OBSERVATION_MODE = False`, and the
running process's own line:

```
[BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h OBSERVATION_MODE=False [pid 3147213]
[VIRTUAL] engine poller starting — LIVE adapter for NEW positions
```

`LIVE_FIXED_MARGIN 20 × LEVERAGE 5 = $100` · `active_fixed_margin() = 20` · `PAPER_FIXED_MARGIN 2000`.

**Titan** — `tools/openitems_guard.py` **exit 0**: *"header and current-state table agree with
runtime"*, runtime HEAD `897850b`, 11 watched values. Geometry `SL_ATR_MULT=2.25`,
`TRAIL_MULT_ATR=1.6875`.

## d) Exchange vs ledger, and wallets

| | **TITAN (BingX)** | **SOL (Bybit)** |
|---|---|---|
| wallet USDT | **508.3156** (free 508.3156, **used 0.0**) | **811.90195236** |
| positions | none returned; `used=0.0` corroborates flat | idx1 size 0, idx2 size 0 |
| open orders | 0 | 0 |
| conditional/stop | — | **0** |
| ledger open | 0 (of 67 vpos) | 0 (of 22, max id 28) |
| `is_paper=0` rows | n/a | **0 — no live position has ever existed** |

**Venue agrees with the ledger on both bots.** Note the "both probes" phrasing is a Bybit concept
(positionIdx 1/2); BingX has no equivalent pair, and the flat state there is corroborated
independently by `used=0.0` margin.

---

# §2 — APPLIED, NEVER RUN ON LIVE DATA

## MERCURY-SOL — everything below is unexercised, because **no live position has ever opened**

| mechanism | first firing looks like | working vs failing |
|---|---|---|
| `book_live_position` | row **id 29** with `is_paper=0` + `[LIVE-BOOK] BOOKED` | a venue position with **no** `is_paper=0` row = the booking gap. It never refuses and never raises by design |
| live stop placement | position-level `stopLoss` set at the venue, `tpslMode='Full'`, **before** the row is booked | booked row with `stopLoss=NONE` at the venue = naked position → the `🚨 NAKED POSITION` alert |
| live `move_stop` | `SL TIGHTENED` message + venue stop moves | a failed move leaves the venue stop **STALE BUT WIDER, never absent** — logged loudly, deliberately not retried |
| live partial | partial leg fills, banked PnL folded into the row | `partial_fill_unreadable` — **non-blocking**: the position is still managed |
| live close | `VIRTUAL CLOSE … reason=…` with a venue fill | `exchange_close_unsubstantiated` = venue FLAT but fill unreadable — **blocking** |
| `pos_state` read | engine reads venue truth each tick | disagreement surfaces as an orphan/naked alert |
| **`unmapped_close`** | a close the engine cannot map to a known reason | **firing = WORKING.** It is a refusal to invent a reason |
| **`WriteUnconfirmed`** | a write refuses because its confirmation check failed | **firing = WORKING.** An unknown result never licenses a second order |
| **M5 venue-check-before-retry** | before any retry, the venue is queried by client id; an existing order is **ADOPTED** | this is the load-bearing guarantee. `orderLinkId` *enforcement* is **UNPROVEN** — only acceptance was verified — and the guarantee deliberately does not depend on it |

**Also unexercised on live data:**

- **The corrected ADX feeding the recheck TIGHTEN branch.** First firing: `recheck_status='tightened'`
  + an `SL TIGHTENED` message at T+10/60/300s. 🔴 **If an early live position closes by a recheck
  tighten rather than its original stop, that is this change** — measured cost on the closed book was
  ≈0.5R on vpos 17. Working vs failing: the reason string must name a **200-candle** ADX; if it says
  `SKIPPED … different windows`, the guard is refusing, which is also correct behaviour.
- **The digest heartbeat block** — has never run in production. First firing: the 08:20 UTC message
  carrying `✅ POLLER ALIVE … ticks=N`. Failure would look like the block missing entirely, which is
  precisely what its "NOT FOUND" path exists to prevent.
- **The poller heartbeat itself is the exception — it HAS run**, 5+ beats observed, and has already
  surfaced that the loop's real period is ~11.4 s against a nominal 10 s.

## TITAN — the brief's premise is **out of date**

> "the EMA envelope gate and the 2026-08-04 geometry, neither of which has seen a closed position"

**Both have.** **vpos 93**, today:

```
04:50:03  [EMA-ENV] PASS SHORT BTC/USDT:USDT 1h=Expanding 15m=Expanding
04:50:13  [ADAPTER] LIVE ENTRY BTC/USDT:USDT SHORT 0.0023 @ 64192.9 fee=0.073822
04:50:13  [VIRTUAL] SL_DRYRUN 1h=64662.06 (0.73%) | margin_1h=$55 cap=HIT | active=1h
04:50:13  [ADAPTER] LIVE STOP @ 64662.1 id=2085589304776175616
04:50:13  VIRTUAL ENTRY BLOCKED … 1/1 open under the lock — no order sent   ← anti-stacking worked
04:50:22  [EXIT-ADVISOR-ACT] vpos=93 conf=0.72 — CLOSING at market
          "Entry thesis compromised… 5m structure has inverted sharply"
04:50:25  VIRTUAL CLOSE vpos=93 exit=64193.0 net_pnl=-0.1479 reason=ai_exit
```

**A complete live round trip, 10.5 seconds, that cost only fees:** gross **−$0.00023**, fees
**$0.1476**, net **−$0.1479** ≈ **−0.137R**. Entry 64192.9 → exit 64193.0.

Everything behaved: envelope admitted, geometry sized the stop (1h leg, margin cap HIT), a **real
venue stop** was placed, the per-side lock refused a second entry, the exit advisor closed on a
stated thesis, stop cleanup found no orphans, MFE was enqueued. The row carries
`entry_adx_1h_window=200` — Titan's own ADX provenance, working.

**One thing worth your judgement, not a defect:** the bullish 5m context the exit advisor cited
(*Bullish Breaker, OB Entered, Within Bullish OB*) was **already present at entry** — the cascade
scored 5m as NEUTRAL because *"this category's own signals disagree — LONG 2.50 / SHORT 2.50"*. So
the entry went in on a genuinely conflicted 5m and the exit advisor judged that same conflict
disqualifying nine seconds later. Coherent, self-cancelling, and it cost 15 cents.

Still unexercised on Titan: everything that needs a position to *live* — trail arming, breakeven
lock, partial, the wall-trail (still `observe-only`, confirmed in the vpos 93 log).

---

# §3 — IS ANYTHING STALE FROM TODAY'S CHANGES?

## a) 🔴 Nothing pools across SOL's ADX boundary. This is the decisive check.

**Every downstream consumer reads `trades.srv_adx_1h` — the column that was NEVER affected**, because
`indicators.fetch_snapshot` always used `CANDLE_LIMIT=200`:

| consumer | reads |
|---|---|
| `optimizer._bucket_adx_1h` | `o['srv_adx_1h']` |
| `mercury_sol_prior_move_logger` | `t.srv_adx_1h`, `t.srv_adx_4h`, `t.srv_adx_15m` |
| `claude_advisor` prompt | `_vs.get('srv_adx_1h')` |

**The only reader of `entry_adx_1h` in the entire tree is `virtual_trader.py:1476`** — the recheck
rehydration, which now goes through `adx_reading_from_stored` and **refuses** a NULL window rather
than guessing 200. It cannot pool.

Boundary integrity, verified in the DB:

```
entry_adx_1h NOT NULL with window NULL (pre-boundary)  : 22
window = 200 (post-boundary)                            :  0   (no live position yet)
window = 42  (must be zero — never backfilled)          :  0 ✅
smart_exit_dryrun_samples: 266 rows, 0 with adx_window  — all pre-fix, correctly NULL
```

## b) Optimizer / observatory / samplers / cron

No sampler or cron reads a column whose meaning moved today. The optimizer's ADX bucket reads
`srv_adx_1h`. The digest reads `trades.status` and `virtual_positions`, neither touched. `oi_cache`,
`dynamic_weights` and the prior-move logger are unaffected.

## c) Titan against its own boundary — 2026-08-04 17:01:29

Titan carries **two** boundaries, and both are handled:

| boundary | before | after |
|---|---|---|
| ADX window (2026-07-30) | 61 rows `window=NULL` | **6 rows `window=200`** |
| geometry (2026-08-04 17:01:29) | 66 positions opened | **1** (vpos 93) |

The geometry change altered `SL_ATR_MULT`, so **1R means a different distance across it** — and only
**one** closed position exists on the new side. No study can say anything about the new geometry yet,
and that is a statement about n, not a defect.

**The optimizer does not create a units mismatch:** its cohort is `cycle_start_id`-bounded **and
LIVE-ROWS-ONLY** (the 2026-08-06 O1/O2 fix), and it ranks **raw dollars** at a constant $150 live
notional — not R. What changes across the boundary is the outcome distribution, not the unit.
`weight_engine` still learns from the full all-time paired set — **documented as deliberate (O3) and
flagged inert**, not an oversight.

---

# §4 — WHAT IS QUIET, AND IS IT MARKET OR MECHANICAL?

## a) SOL — the silence RESOLVED itself since the 22:50 check

| | |
|---|---|
| webhooks / 24h | **206** |
| last webhook | **23:30:03** — **3.5 min ago** |
| current gap percentile | **40th** (median 5.0 min, p95 30.1, max 75.1) |
| **webhooks since the flip** | **7** |
| advisor consultations since the flip | **0** |

The 44-minute gap reported at 22:50 was ordinary and it ended. **All 7 post-flip webhooks are
accounted for**, individually:

- 2 × `context_recorded` + 1 × `confirm_recorded` — bookkeeping, never entry attempts
- **4 × `htf_blocked` (`open_long`)** — genuine entry attempts, stopped by the HTF cascade, which
  sits **upstream of the advisor**. That is why the advisor was not consulted.

**MARKET, not mechanical — checked against the tape, not the bot's label:**

```
1h   last=73.61 ema20=73.51 ema50=73.45 ADX=21.9  -> BULL
15m  last=73.61 ema20=73.67 ema50=73.60 ADX=14.1  -> MIXED
5m   last=73.61 ema20=73.65 ema50=73.67 ADX=12.0  -> BEAR
24h range 2.62% · 24h change +1.36%
```

The lower timeframes genuinely oppose LONG and 15m/5m ADX are **14.1 / 12.0** — flat. Blocking LONG is
a defensible read of that tape. Mechanically the funnel is provably alive: 7 webhooks in, 7 rows
written, 4 classified as entry attempts and refused with a stated reason.

## b) 🔴 TITAN — the pre-registered trigger has been CROSSED

| | |
|---|---|
| **`ema_envelope_blocked` ROWS** | **111** — trigger was **100. CROSSED.** |
| distinct days | 4 |
| first / last | 2026-08-04 23:10:04 → **2026-08-07 22:00:05** |
| last 6h | 25 webhooks, 5 reached the gate: **4 BLOCK / 1 PASS** |
| hours since last consultation | **~18.7 h** (exit advisor 04:50:22) |
| hours since last position | **~18.7 h** (vpos 93 closed 04:50:23) |
| last webhook | 23:15:01 — 25 min ago |

**The review you pre-registered at 100 blocked rows is now due.** I am reporting it, not acting on it.

**MARKET, checked against the tape:**

```
BTC 1h   last=64863 ema20=64775 ema50=64609 ADX=20.3 -> BULL
BTC 15m  last=64863 ema20=64883 ema50=64847 ADX=13.3 -> MIXED
24h range 1.88% · 24h change +0.89%
```

15m ADX **13.3** and a 1.88% daily range is a compressed tape — exactly what an *envelope-expansion*
gate is built to refuse. 4 blocks of 5 is consistent with that, and the one PASS became a real live
trade. Titan's quiet is the market plus a gate doing its stated job.

**One cosmetic nit, not a fault:** `CryptoPanic HTTP 404` appears in Titan's log (1 in 6h). The news
source returns 404; `news` weight showed `0.0` in the vpos 93 breakdown. It degrades to neutral rather
than failing — worth knowing, not worth acting on tonight.

---

# §5 — HANDS-REQUIRED, BOTH BOTS, ONE PLACE

### 🔴 MERCURY-SOL — these BLOCK a side

| verbatim | what it means | operator does |
|---|---|---|
| `🔴🔴🔴 NAKED POSITION — EMERGENCY CLOSE FAILED` | position with no stop, and closing it failed | **close it at Bybit by hand, now** |
| `🚨 NAKED POSITION` | position exists with no stop | verify at venue; close or re-stop by hand |
| `🚨 ENTRY FILL UNREADABLE` | order sent, fill unreadable, **not booked** | check the venue for an unbooked position |
| `🔴 ORPHAN POSITION ON THE VENUE` | venue has a position the ledger does not | reconcile before restart |
| `⚠️ SL failed 3× — position CLOSED` / `🚨 SL FAILED 3× — emergency close` | stop could not be set; position force-closed | confirm flat at the venue |
| `🛑 Post-entry T+Ns — EMERGENCY CLOSE` | health score ≤ −10 | confirm the close landed |
| `🚨 DAILY LOSS BREAKER (R)` | ≥ 3.0R lost today on the **live** book | trading halts; decide whether to resume |

**Blocking stages** (from the digest's own table): `sl_failsafe_close_failed`,
`entry_fill_unreadable`, `exchange_close_unsubstantiated`, `boot_orphan`.
**Non-blocking:** `partial_fill_unreadable` — the position is live and managed; only the partial leg
failed.

**Not alerts — mechanisms working:** `unmapped_close`, `WriteUnconfirmed`, `🚨 ENTRY DUPLICATE
SUPPRESSED`, `🚨 ENTRY NOT CONFIRMED — NO SECOND ORDER`.

### 🔴 TITAN — these need hands

| verbatim | operator does |
|---|---|
| `🛑 TITAN REFUSED TO START` | the boot guard refused — read the reason before forcing anything |
| `❌ CRITICAL: emergency close failed for …` / `… BE emergency close failed` | **close at BingX by hand** |
| `🚨 POSITION GONE, STOP DID NOT FILL` | ledger/venue disagree — reconcile before the next entry |
| `🚨 ORPHAN STOP COULD NOT BE CANCELLED` | a resting stop with no position — cancel by hand |
| `🚨 Could not re-attach SL for open …` | open position, stop not re-attached at boot — re-stop by hand |
| `🚨 NAKED {side} position … ATR fetch failed` | position with no stop | close or stop by hand |
| `🔴 STOP RETRY HALTED — CANNOT CONFIRM` | **this is the F2 guard WORKING** — it refused to risk a second stop. Verify the venue, then decide |
| `🔴 ZERO FILL on entry` | order returned no fill — confirm nothing is open |
| `🔴 EXIT-ADVISOR CLOSE FAILED` | the advisor wanted out and could not — close by hand |

**New tonight, SOL only:** the digest's `🔴 POLLER HEARTBEAT — STALE. THREAD LIKELY DEAD. ACT.` and
its worst-case escalation `🔴🔴🔴 N OPEN POSITION(S) WITH A DEAD POLLER — NO MANAGER.`

---

# §6 — ROLLBACK PATHS

## a) Titan — git

**There is nothing to revert for today: Titan received no commit and no file edit today.** HEAD is
`897850b` (2026-08-06 01:55:45) and the tree is clean.

If an earlier commit must come out, each bundles **two** fixes and must move whole:
`897850b` = optimizer live-only cohort **+** trail label · `999572a` = G3 boot re-attach **+** G2
partial PnL · `7c2feac` = F2 stop-retry **+** F9c degraded close.
🔴 `897850b` and `999572a` **must move together** if you revert either: 897850b's optimizer cohort
change assumes the live/paper split that 999572a's unifier work depends on.

## b) SOL — `.bak` only, **sorted by ctime** (mtime is the pre-edit source time on `cp -p` copies)

| ctime taken | file | belongs to |
|---|---|---|
| 21:06:56 | `indicators.py.bak_adxwindow_20260807` | ADX fix |
| 21:06:56 | `virtual_trader.py.bak_adxwindow_20260807` | ADX fix |
| 21:06:56 | `main.py.bak_adxwindow_20260807` | ADX fix |
| 21:06:56 | `OPEN-ITEMS-SOL.md.bak_adxwindow_20260807` | ADX fix |
| 22:11:19 | `trades.db.bak_pre_adxwindow_migration_20260807` | pre-migration DB |
| 22:13:43 | `OPEN-ITEMS-SOL.md.bak_adxwindow_applied_20260807` | canon |
| 22:25:10 | `.env.bak_preflip_live_20260807` | **the flip** |
| 22:29:11 | `OPEN-ITEMS-SOL.md.bak_preflip_live_20260807` | canon |
| 22:53:09 | `virtual_trader.py.bak_heartbeat_20260807` | heartbeat |
| 23:16:39 | `silence_digest_sol.py.bak_hbage_20260807` | digest block |

**Pairs that MUST move together:**

- 🔴 **`indicators.py` + `virtual_trader.py` + `main.py` (`_adxwindow_`) are ONE set.** Reverting
  `indicators.py` alone leaves `virtual_trader` calling `indicators.adx_reading()` → `AttributeError`
  → **the poller thread dies on the first tick.**
- 🔴 **`virtual_trader.py` has TWO backups and they are NOT interchangeable.**
  `.bak_heartbeat_20260807` (22:53) removes **only** the heartbeat and keeps the ADX fix.
  `.bak_adxwindow_20260807` (21:06) removes **both**, and then demands the other two files revert too.
  Picking the wrong one is the easiest mistake available tonight.
- The DB backup is **not** needed for a code revert: both new columns are additive and NULL on every
  existing row. Restoring it would discard everything written since 22:11 (currently nothing) — do
  not restore it reflexively.
- Every code revert needs a **restart from flat** to take effect.

## c) 🔴 FASTEST SAFE ACTION IF A LIVE POSITION MISBEHAVES

**Both bots place a REAL stop at the venue before the position is booked** — SOL sets a
position-level `stopLoss` (`tpslMode='Full'`) and calls `book_live_position` only *after the stop is
confirmed*; Titan's vpos 93 log shows `LIVE STOP … id=2085589304776175616`. **So the position is
protected by the exchange even if the bot is not running.**

- **SOL:** `systemctl stop mercury-sol` — the venue stop remains. Then close manually on Bybit if
  needed. 🔴 **Flipping `MERCURY_OBSERVATION_MODE` back to `1` does NOT close a position, does not
  stop the bot, and does not even change how that position is managed** — `is_paper` is stamped on the
  row at open, so a live row keeps being managed as live no matter what the mode says afterwards.
  Treat the mode flag as irrelevant in an emergency.
- **Titan:** `systemctl stop titan` — venue stop remains. Then close manually on BingX.
- **Fastest of all, either bot:** close the position **at the exchange**, then stop the service, then
  reconcile. Stopping the service first leaves a position nobody is trailing, but still stopped.

---

## What I did not do

No file was edited, no service restarted, no order placed, no DB written. Every DB read used
`?mode=ro`; every exchange call was a read (`fetch_balance`, `fetch_positions`, `fetch_open_orders`,
`fetch_ohlcv`, and a read-only stop-order query).
