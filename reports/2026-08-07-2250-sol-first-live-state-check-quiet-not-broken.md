# SOL — first live-state check after the flip: **QUIET, not broken**. Nothing traded, and the silence started *before* the flip.

**2026-08-07 22:50 UTC** · Mercury-SOL · 🔴 **LIVE REAL MONEY** since 22:25:18 UTC (25 min ago)
READ-ONLY. **Nothing was changed, nothing was fixed, no trade was forced.**
Titan (`/root/titan-bot`): untouched — 0 changes, HEAD `897850b`, workers up 1d20h, never restarted.

---

## 1. HAS ANYTHING TRADED? — **NO. This is the expected state.**

| | |
|---|---|
| rows with `id ≥ 29` | **0** |
| rows with `is_paper=0` | **0** |
| open `virtual_positions` | **0** |
| max id | still **28** |
| `is_paper` tally | `[(1, 22)]` — all 22 historical rows still paper |
| `active_positions` / `exit_pending` | **0 / 0** |
| `trades` rows since the flip | **0** |
| venue positions / orders / conditional orders | **0 / 0 / 0** |

**No live position has ever existed.** The bot is flat and waiting for its own signal.

---

## 2. THE FUNNEL — and the decisive fact about the silence

**Zero webhooks have arrived since the flip.** That sounds alarming until you look at when the
silence began:

> **Last webhook: 21:55:04. The flip: 22:25:18.**
> **The silence started 30.2 minutes BEFORE the flip** and simply continued through it.
> Current gap **44.1 min**.

Calibrated against the preceding 24 hours (201 webhooks):

| | |
|---|---|
| median gap | **5.0 min** |
| p90 | 15.0 min |
| p95 | 30.1 min |
| **max observed** | **75.1 min** |
| gaps > 44 min in that window | **5** |

A 44-minute gap is the **95th–100th percentile of ordinary behaviour**, five comparable gaps occurred
in the last day alone, and it is well inside the observed maximum. Late-UTC-evening quiet.
**Nothing about this gap is attributable to the flip** — it predates it.

### Where candidates die — measured over the last 24h (same code path in both modes)

| stage | count |
|---|---|
| `WEBHOOK_IN` | **201** |
| context recorded | 196 |
| HTF would-pass | 66 |
| weighted adjustment | 69 |
| **reached the AI advisor** | **23** |
| `ENTRY BLOCKED` | 2 |
| `ENTRY SKIPPED` | 0 |
| risk_check / macro halt / DXY halt | **0** |

**Answer to the question asked: candidates DO reach the advisor — 23 of them in 24 hours. The cascade
is not eating everything.** The advisor is the terminal filter, and it returned **SKIP on all 23**
(0 approvals). So the pipeline is alive end-to-end and the bot's silence is an *advisor* verdict, not
a plumbing failure.

---

## 3. 🔴 IS THE LIVE PATH ACTUALLY EXERCISABLE? — **Yes, on all three counts**

**Engine live adapter** — the boot lines name the registered hooks individually, which is stronger
than a mode flag:

```
[VIRTUAL] engine poller starting — LIVE adapter for NEW positions
[VIRTUAL] live adapter registered (close/partial/move_stop/pos_state/book_close)
[VIRTUAL] poller started in pid 3138270 (interval=10s)
[BOOT] geometry: … OBSERVATION_MODE=False [pid 3138270]
```

**`_risk_check` now reads the LIVE book, and it is empty — no brake can fire.** Verified by running
the breaker's exact query read-only, both ways:

| book selected | rows today | daily_pnl | daily_R |
|---|---|---|---|
| **LIVE (`is_paper=0`) — what it reads now** | **0** | **0.0000** | **0.0000** |
| PAPER (`is_paper=1`) — what it read before | 1 | **−20.6217** | −0.1531 |

The selector is `_brake_book = 1 if OBSERVATION_MODE else 0`. **This is not theoretical today:**
vpos 28 closed at 06:00:10Z for **−20.62 / −0.153R** *this calendar day* and is `is_paper=1`. Before
the flip that loss counted; after it, it does not. That is precisely the contamination the code
comment warns about — a paper loss tripping, or a paper win masking, a brake protecting a $100 live
book — and the filter is demonstrably doing its job on real data, today. With the live book empty the
breaker returns at `daily_pnl >= 0 and daily_R >= 0` → **no halt, and no `fetch_balance` round-trip**.

**Position cap counts live rows** — there are two caps and they differ, which is worth stating
precisely:

- `main._risk_check` (line 1589) counts **venue** positions via `fetch_positions` — genuinely live,
  currently **0 on both indices**, so it cannot block.
- `virtual_trader._open_count` counts **DB** open rows for (symbol, side) and does **not** filter
  `is_paper`. Currently 0 open, so it has no effect. Naming it for completeness: if a paper row were
  ever left open across a flip it would block a live entry — the **fail-safe direction** (blocks
  rather than stacks), and it cannot arise here because the flip was taken from flat.

**Nothing in the live path is unreachable.** The one thing that has not happened is a signal.

---

## 4. TRACEBACKS, `10010`, HANDS-REQUIRED — **all zero**

| | |
|---|---|
| tracebacks since 22:25:18 | **0** |
| `10010` (IP-allowlist / key) | **0** |
| naked-position / hands-required alerts | **0** |
| `unmapped_close` / `WriteUnconfirmed` / EMERGENCY | **0** |

Two log lines matched an `orphan` grep; both are benign and are the cleanup **working**:
`[SMART-CLEANUP] No open positions for SOL/USDT:USDT — proceeding with orphan cleanup` and
`[BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible`. Total log volume since the flip is
20 lines, all boot.

---

## 5. CONNECTIVITY AND WALLET

| | |
|---|---|
| Tor → Bybit, **signed** | ✅ ok in 16.5 s, no `10010` |
| OKX direct, keyless | ✅ ok in 2.4 s (bid 73.58 / ask 73.59) |
| **wallet USDT** | **811.90195236** — **byte-identical to the flip-time reading** |
| webhook receiver | ✅ **LISTENING** on 127.0.0.1:5002 (master + worker fds) |

---

# 6. 🔴 WHAT WOULD TELL US THE LIVE PATH IS **BROKEN** RATHER THAN **QUIET**

Silence is only readable against a baseline. Here is the one, plus the honest gap in it.

### Positive liveness — confirmed right now, none of which requires a trade

1. **Receiver socket LISTENING** on 127.0.0.1:5002, held by both master and worker. If the receiver
   died, this disappears — a webhook could not even be accepted.
2. **CPU is accumulating**: +129 ticks (1.29 s) over a 30 s sample. The worker is doing periodic
   work, not parked. *(This proves the process ticks; it does not by itself isolate the poller
   thread — see the gap below.)*
3. **Signed venue call succeeds** through Tor — the live path's most fragile dependency answers.
4. **The gap distribution above** — 44 min sits inside ordinary behaviour (max observed 75.1 min).

### The distinguishing table — silence made readable

| observation | **QUIET** (healthy) | **BROKEN** (act) |
|---|---|---|
| no trade | webhooks arriving **and** `[AI-ADVISOR] SKIP` lines logged | webhooks arriving but **no `[AI-ADVISOR]` line across ~20+ signals** → the cascade is eating everything before the advisor |
| no webhook | gap **≤ ~75 min**, socket LISTENING | gap **> ~90 min** with socket still listening → upstream (TradingView) is dead, not the market. Socket **not** listening → the receiver is dead |
| entries never fire | explicit `ENTRY BLOCKED` / `ENTRY SKIPPED` with a reason | 🔴 **`_risk_check` FAIL-CLOSED on an exception.** Any risk-query error → block. From outside this is **indistinguishable from "no signal"**. Tell: a `macro halt` / `DXY halt` / `daily_loss` / `positions.riskcheck` failure line. **0 in 24h** |
| venue calls | signed calls return | **any `10010`** → key or IP-allowlist broken; the live path goes **blind while looking healthy** (this one has bitten before, and it blinds paper too) |
| a position opens | row 29 with `is_paper=0`, `[LIVE-BOOK] BOOKED` | a venue position exists with **no** `is_paper=0` row → the booking gap; **or** `unmapped_close` / `WriteUnconfirmed` firing, which is the mechanism **WORKING**, not breaking |
| a position closes early | closed at the original stop | **`recheck_status='tightened'` + an `SL TIGHTENED` message at T+10/60/300s** → that is the corrected-ADX change from §1c, **flag immediately** (accepted risk (b)) |

### 🔴 THE GAP I AM NAMING, because it is the one silence hides

**While the book is flat, the poller logs NOTHING.** It has ticked roughly 150 times since boot at
`interval=10s` and produced **zero** log lines beyond its three startup messages. **If the poller
thread died right now, nothing would say so** — the process would stay up, the socket would stay
listening, and the first evidence would be a signal arriving and no position opening.

The available mitigations, and their latency:

- **`silence_digest_sol.py`** — the read-only daily digest at **08:20 UTC** (cron), which exists
  precisely so Telegram shows *why* the bot was quiet: no signals, gate refusal, or advisor skip.
  **Latency: up to ~24 h.**
- The **CPU-delta check** above — immediate, but process-level rather than thread-level.
- The next arriving webhook — which, at a median 5-minute cadence, is the real answer and needs no
  new machinery.

**No change is proposed here** (this pass is read-only). But if you want the poller's liveness
observable without waiting for a signal, that is the one gap worth closing, and it is a heartbeat
line on the poller tick, not a new subsystem.

---

## VERDICT

**Quiet, not broken.** Nothing traded, which is the expected state 25 minutes in. The silence began
30 minutes before the flip, sits within the normal gap distribution, and the funnel that feeds it was
demonstrably alive over the preceding 24 hours with 23 candidates reaching the advisor. The live path
is exercisable on all three counts, the brake correctly reads an empty live book, connectivity and
wallet are unchanged, and there is not one traceback, `10010`, or hands-required alert.
