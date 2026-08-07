# SOL — POLLER HEARTBEAT APPLIED. The gap named in the 22:50 report is closed: detection latency **24h → ~10 min**.

**2026-08-07 23:10 UTC** · Mercury-SOL · 🔴 **LIVE REAL MONEY**
Closes §6 of `2026-08-07-2250-sol-first-live-state-check-quiet-not-broken.md`.
Titan (`/root/titan-bot`): **untouched** — 0 changes, HEAD `897850b`, workers never restarted.

---

## WHAT SHIPPED

**One file, `virtual_trader.py`, three hunks.** Backup `virtual_trader.py.bak_heartbeat_20260807`.
Worker **pid 3147213**, booted **2026-08-07 22:59:24 UTC**, restart taken **from flat**.

**Three beats observed in production**, spanning two full intervals:

```
22:59:43  [HEARTBEAT] alive ticks=1  (+1 in 3s)    last_tick=3.2s  max_tick=3.2s  cadence=10s open=0 mode=LIVE pid=3147213
23:04:51  [HEARTBEAT] alive ticks=28 (+27 in 308s) last_tick=11.3s max_tick=11.7s cadence=10s open=0 mode=LIVE pid=3147213
23:10:02  [HEARTBEAT] alive ticks=55 (+27 in 312s) last_tick=12.9s max_tick=12.9s cadence=10s open=0 mode=LIVE pid=3147213
```

Cadence holds at 308 s and 312 s — slightly over 300 s because the gate is evaluated *after* a tick
completes, so a beat lands on the first tick past the threshold. Intended, and it is why "two missed
beats" (~10 min) is the right dead-thread rule rather than a tight 300 s alarm.

### 🔴 It has already shown something nobody could see before

**The loop's real period is ~11.4 s, not the nominal 10 s** — 27 ticks per ~310 s window, and
`last_tick` reading 11.3 s and 12.9 s against `cadence=10s`. The extra ~1.4 s is the work the
iteration does on top of its sleep (the poll plus the PEO, skip-attribution and follow-through
sub-ticks). A ~15 % drift between nominal and actual cadence was **invisible until this line existed**.
Nothing is wrong — `time.sleep(poll_secs)` is a floor, not a period — but it is exactly the class of
fact the heartbeat was added to surface, and it arrived within ten minutes of shipping.

---

## 1a. 🔴 THE CADENCE, AND WHY

**300 s.** Chosen against two failure modes, not by taste:

| cadence | lines/day | verdict |
|---|---|---|
| per tick (10 s) | **8,640** | would bury the 201 webhooks, the advisor verdicts and the entry blocks that actually matter — the thing the log is *for* |
| **300 s** | **288** | a dead thread is certain after two missed beats (**~10 min**) |
| 1 h | 24 | too slow to be worth having when the bot is live |

288 lines/day against a current volume of a few thousand is a rounding error. **Detection latency
goes from up to 24 h (the 08:20 daily digest) to ~10 minutes — a 144× improvement.**

**One beat is forced on the first COMPLETED tick** (`hb_first`), not after the first 300 s. That is
deliberate: `poller started in pid N` is printed *before* the loop, so "the thread started" and "the
loop is actually iterating" are different claims, and only the second was missing. The boot beat
proves the second one immediately.

## 1b. THE STATE IT CARRIES

`alive ticks=1 (+1 in 3s) last_tick=3.2s max_tick=3.2s cadence=10s open=0 mode=LIVE pid=3147213`

| field | what it lets a reader do |
|---|---|
| `ticks` | total iterations since boot — a monotonically rising number; frozen = wedged |
| `(+N in Ms)` | iterations **in this window**. `+0` with the line still arriving = a loop spinning without doing work — the case a bare "alive" cannot distinguish |
| `last_tick` | seconds between the last two iterations — catches a slow loop before it is a dead one |
| `max_tick` | worst gap **in this window**, reset each beat — one stall does not hide behind an average |
| `cadence` | 10 s normally, **20 s** when the adaptive back-off has engaged → an ongoing Tor/venue problem, visible without reading error lines |
| `open` | open positions on the last poll — **0** here; a live position with a silent poller is the nightmare case, and this makes it legible |
| `mode` | `LIVE` / `PAPER` — so a log line can never be misread across a flip |
| `pid` | ties the beat to the worker that emitted it |

## 1c. 🔴 IT IS INERT — confirmed, and proven by execution

- **No network call.** Proven, not asserted: the test drives the real `_worker_loop` with an
  exchange stub that **raises on any attribute access**. It never fired. The 08-01 lesson holds —
  a measurement that can skip on a Tor hiccup is worse than the gap it fills; this one has nothing
  to skip on.
- **No DB query.** The open count is recorded inside `_poll_once`, which **already** runs that query,
  stored before its early return so a flat book still reports its zero. Zero added reads.
- **Cannot change a decision.** It runs at the **end** of the iteration, after every verdict, stop and
  order decision, and writes only to stdout. It reads counters and constants already in hand.
- **Cannot break the poller it observes.** It carries **its own `try/except`**, matching every other
  sub-tick in that loop (`_peo_tick`, `_skip_tick`, the follow-through hook). A failed `print` logs
  `[HEARTBEAT] emit failed (ignored)` and the loop continues.

## 1d. 🔴 HOW A READER TELLS **DEAD** FROM **QUIET**

| observation | verdict |
|---|---|
| beat arrives, `ticks` rising, `+N` > 0 | **HEALTHY** — quiet market, working loop |
| beat arrives, **`+0` ticks** in the window | **SPINNING** — loop alive, doing no work |
| beat arrives, `last_tick`/`max_tick` ≫ `cadence` | **STALLING** — degrading before it dies |
| beat arrives, `cadence=20s` | back-off engaged — venue/Tor trouble, still alive |
| **no beat for > 10 min** (two missed) | 🔴 **THREAD DEAD** — process may still be up and the socket still listening. **Act.** |
| `open=` non-zero **and** beats stop | 🔴 **WORST CASE** — a live position with no manager. Act immediately. |

**Detection latency: ~10 minutes**, versus up to 24 h before. And the distinction the 22:50 report
could not make — process alive vs *thread* alive — is now direct: the counters are **local to the
loop's own stack frame**, so the line cannot be produced by anything except that loop completing an
iteration. The CPU-delta check was process-level; this is not.

---

## 2. PROPOSAL ONLY — the daily digest should surface heartbeat age

**Not built in this pass, as instructed.** `silence_digest_sol.py` (08:20 UTC, read-only, separate
process) currently explains *why* the bot was quiet — no signals, gate refusal, advisor skip. It
cannot yet say the poller was *alive* while being quiet.

**Proposed:** one line — last heartbeat timestamp, its age, and the final `ticks` count. The digest
already parses the journal, so this is a grep for the last `[HEARTBEAT]` line and a subtraction; no
new state, no new file, no coupling to the trading path. It would turn "no signals arrived" into
"the poller ticked 8,640 times and no signals arrived", which are very different messages.

**Why it is worth doing separately:** the digest is a different process on a different schedule, and
folding it in here would widen a live-money change from one file to two for no gain in the thing that
was urgent.

---

## PROVEN BY EXECUTION, BOTH DIRECTIONS

Isolated tree copies, the **14-vector isolation** established earlier today: all **13** files
carrying the live `trades.db` literal rewritten **including `market_context._DB_PATH`** (underscore —
invisible to a `^DB_PATH =` grep), **plus the copied tree's `.env`**, because `main.py` does
`load_dotenv(override=True)`, which beats both the rewritten literal and `os.environ`. Plus a
`sqlite3.connect` leak assert.

**POST — exit 0:**

| | |
|---|---|
| heartbeats emitted | **4** |
| first beat on the first completed tick | ✅ `ticks=1` |
| **rate limit** | **31 ticks → only 4 beats** (per-tick would be 31) |
| carries every field | `ticks/last_tick/max_tick/cadence/open/mode/pid` ✅ |
| **no exchange call attempted** | ✅ exploding stub never fired |
| loop still alive after emitting | ✅ |
| leak assert | ✅ 0 live connects |

**PRE — exit 0:** the pre-edit tree emits **zero** heartbeats. The change is what produces them.

### 🔴 The leak assert caught MY OWN harness error — again

On the first PRE run it failed loudly:

```
FAIL DB_PATH rewritten to the copy      (DB_PATH = /mnt/…/mercury-sol/trades.db)
FAIL LEAK ASSERT: live DB never opened
```

I had copied the `.bak` over the rewritten file **after** the `sed`, restoring the live literal. The
child ran `SELECT`s against the **live** database before I caught it. **Verified unharmed:** 22 rows,
max id 28, 0 open, `is_paper` all 1, 0 `TEST` symbols — `_all_open_positions` only reads, and with a
flat book `_poll_once` returns early. Harness fixed, PRE re-run clean.

**That is twice in two sessions the leak assert has caught a real isolation break that review did
not.** It stays.

---

## DEPLOY VERIFICATION

Restart from flat (0 open / 0 `active_positions` / 0 `exit_pending`, max id 28).

| check | result |
|---|---|
| boot geometry | `SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h **OBSERVATION_MODE=False**` |
| live adapter registers | ✅ `live adapter registered (close/partial/move_stop/pos_state/book_close)` |
| venue boot assert | ✅ `venue FLAT for SOL/USDT:USDT — no orphan possible` |
| **first heartbeat** | ✅ 22:59:43, `ticks=1 … open=0 mode=LIVE` |
| **cadence held over 2 intervals** | ✅ 3 beats: 308 s, 312 s apart |
| tracebacks (11 min live) | **0** |
| loaded code | `.pyc` embedded source mtime matches `.py` for `virtual_trader` and `main` |
| book | still flat, max id 28, no live row yet |

Nothing else changed: no geometry, no brake, no cascade, no score bar, no prompt, no
`MERCURY_OBSERVATION_MODE`.

## Rollback

`cp -p virtual_trader.py.bak_heartbeat_20260807 virtual_trader.py` + restart from flat. The change is
additive and observational — reverting it removes log lines and nothing else.
