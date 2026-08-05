# TITAN — THE UNRANKABLE BOOK STOPS PASSING IN SILENCE. AND THE MFE TRACKER IS COSTED, NOT DEFERRED: ITS BLOCKER IS NOT THE LIFT-OUT.

**2026-08-05 20:55 UTC · ITEM 1 APPLIED FROM FLAT · HEAD `ece910d` → `7472729` · restarted 20:54:27 UTC**
**ITEM 2: DIFF SHOWN, NOT APPLIED — awaiting approval, as instructed.**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
**0 open positions and 0 `exit_pending`** at application, re-checked before the restart.
**Mercury-SOL never opened.**

Parent: `2026-08-05-2035-titan-refusals-made-countable-and-one-instruction-refused.md`.

---

## 1. ✅ APPLIED — THE UNRANKABLE-BOOK WARNING, AND THE HARD RULE MADE SAFE IN THAT STATE

### (a) 🔴 COUNTED FIRST — AND THE ANSWER IS **LATENT**, NOT LIVE

| era, by DEPLOY not by date | entry prompts | with an Order book block | 🔴 **book but NO percentile scale** |
|---|---|---|---|
| before the scale shipped | 2,623 | 2,623 | 🔴 **2,623 = 100 %** |
| **after** (from row 19464, 2026-07-29 13:45:21) | **101** | 101 | 🔴 **0** |
| total | 2,724 | 2,724 | 2,623 = 96.3 % |

⚠️ **A calendar split would have reported this wrong, and did on my first pass.** Splitting on
2026-07-29 put **two** prompts (19330, 19333) in the "post" bucket. They are not post-deploy: both
render *"**Massive** bid walls (>4x avg vol)"* — the pre-`8b15ecc` wording — so they precede that
day's deploy rather than follow it. **Ordered by deploy instead of by date, the count after the scale
shipped is exactly zero.**

**So it is latent today**, and the reason is structural: `baseline_n` is read from
`orderbook_density`, which is **append-only and holds 33k+ OKX rows**, so `_exit_pct` always returns a
count. **The branch remains reachable through one path only — `_entry_book_pct`'s `{}` fallback, which
it returns on ANY exception inside the percentile computation.** Rare, not impossible, and silent when
it happens. **A latent defect still gets the warning; you asked which it was, and it is this one.**

### (b) WORDED FROM THE EXIT BLOCK, SO THERE IS ONE DIALECT

### (c) 🔴 AND THE HARD RULE NO LONGER DANGLES — I AGREE WITH YOUR READING, AND HERE IS THE ARGUMENT

The rule says to judge thickness *"off the wall's OWN percentile, printed beside it."* With no
percentile it is **unsatisfiable** — the identical defect fixed at 19:08, recurring one layer down
through the degraded path. **Your reading is right, and it does not require new policy to justify:
the rule's own stated premise is that "EVERY book state contains a wall above 4x, so a large ×-figure
on its own says nothing." A wall with no percentile therefore cannot satisfy the rule, by the rule's
own reasoning.** Saying so applies the existing justification to the case where its input is missing.
The alternative is what shipped for 2,623 prompts: an unsatisfiable instruction sitting over
suggestive raw numbers, which is precisely the inference the rule exists to prevent.

### (d) VERIFIED BY EXECUTION ON THE DEGRADED PATH

Forced unrankable state (`bp={}`), rendered through the real function:

```
Order book (pre-trade, 8000 levels):
  Mid: $64,449.95  |  Imbalance ±1%: 0.34 (ask-heavy)
  Bid walls (>4x avg bucket vol): $64,317.50 (×4.1), $64,292.50 (×4.3)
  Ask walls (>4x avg bucket vol): $64,502.50 (×4.4), $64,677.50 (×9.3)
Order-book PERCENTILE scale: NOT AVAILABLE for this entry.
  The figures above are RAW multiples that could not be ranked against
  this book's own history. Do NOT infer 'extreme' or 'ordinary' from a
  bare multiple — every book state contains a wall above 4x.
  🔴 The HARD RULE on opposing walls therefore does NOT apply to any
  wall here: with no percentile there is no basis to call one thick.
  Decide on the signal tiers, regime and volatility blocks instead.
```

**Before this change, that same state rendered the first four lines and nothing else.**

| check | result |
|---|---|
| normal path vs before | ✅ **BYTE-IDENTICAL** (compared against the snapshot module) |
| `_ENTRY_SYSTEM` md5 | **`d7b8f3ed…` unchanged** |
| `_CLOSE_SYSTEM_RICH` md5 | **`f0ae3958…` unchanged** |
| `_CLOSE_SYSTEM` md5 | **`86fbc2e0…` unchanged** |
| exit block's own warning | ✅ **untouched** (0 diff hunks) |
| files changed | **1** (`claude_advisor.py`, +35) |
| gate / geometry / sizing lines | **none** outside comments |

---

## 2. 🔴 THE MFE TRACKER — DECIDED, AND THE BLOCKER IS NOT WHERE THE BRIEF EXPECTED

**Diff below is NOT applied.**

### (a) WHERE `enqueue()` WOULD GO — ONE SITE, NOT SEVERAL

Every close route converges on **`virtual_trader._do_close()`** (def@1220): external closes,
poller-triggered SL, trail, the advisor's `ai_exit`, the recheck emergency close, and the passive
exchange fill (`_exit_fill`) all pass through it — it is the function that writes `status='closed'`,
`close_price`, `close_reason` and `net_pnl`. `close_position()` (line 1101) delegates to it, and
`main._execute_close_position` delegates to `close_position`.

**Everything `enqueue()` needs is already in scope there** — no new query:
`row['symbol']`, `row['position_side']`, `close_price`, `row['step_size']`,
`row['trades_entry_row_id']`, plus `reason` and `row['partial_taken']`.

```diff
--- a/virtual_trader.py
+++ b/virtual_trader.py
@@ (inside _do_close, immediately after the close row is committed and
@@  report.combo_key is set — i.e. after the `with sqlite3.connect(DB_PATH)` block)

+    # 🔴 MFE TRACKING — REGISTERED HERE BECAUSE THIS IS WHERE EVERY CLOSE ARRIVES.
+    # The only existing enqueue site is main.py:3643, inside
+    # `_handle_liquidity_sweep()`, which has never executed: 0 of 20,721 signals
+    # ever carried an EQH/EQL type. The tracker was therefore never a broken
+    # measurement — it was an unreachable one, and `mfe_tracking` is empty with
+    # its four `trades` columns NULL on every row.
+    #
+    # `_do_close` is the single convergence point for external closes, poller SL,
+    # trail, the advisor's ai_exit, the recheck emergency close and the passive
+    # exchange fill. Registering here makes the measurement independent of exit
+    # route, which is the property the optimizer question needs.
+    #
+    # ONE LOCAL INSERT ON THE TRADING PATH, no network: `mfe_tracker.enqueue` is a
+    # single INSERT, and `_poll_once` returns before any `fetch_ticker` when the
+    # queue is empty. Wrapped so a measurement can never affect a close.
+    try:
+        import mfe_tracker
+        mfe_tracker.enqueue(
+            trade_id=row['trades_entry_row_id'],
+            symbol=row['symbol'],
+            position_side=row['position_side'],
+            close_price=close_price,
+            amount=row['step_size'],
+            signal_type=f"vclose:{reason}"
+            + (":partial" if row['partial_taken'] else ""),
+        )
+    except Exception as _mfe_err:
+        print(f"[MFE] enqueue failed (continuing): {_mfe_err}", flush=True)
```

*(`signal_type` is reused as the route/partial label — it is a free-text column the tracker only
stores, and it is what makes the 100 %-close-versus-partial cut possible at all.)*

### (b) 🔴 WORK ON THE TRADING PATH: NONE. BUT THE 08-01 LESSON BITES ELSEWHERE — AND THIS IS THE FINDING

**On the trading path:** one local `INSERT`, no network. `_poll_once` does
`if not active: return 0` **before** any `fetch_ticker`, so an empty queue costs nothing. The tracker
already has a running worker (started from `gunicorn.conf.py:137` and `main.py`), and — unlike
`breakeven_worker` — **nothing else rides its loop**, verified: `mfe_tracker` imports only
`sqlite3/threading/time/datetime`, and has no reference to `liquidity_sweep`.

🔴 **BUT THE MEASUREMENT ITSELF CAN SILENTLY DEGRADE, AND THAT IS EXACTLY WHAT 2026-08-01 WARNED
ABOUT.** In `_poll_once`:

```python
        try:
            t = exchange.fetch_ticker(sym)
            prices[sym] = float(t['last'])
        except Exception as e:
            print(f"MFE ticker fetch {sym} failed: {e}", flush=True)
        …
        current_price = prices.get(symbol)
        new_mfe = prev_mfe          # ← fetch failed: silently keeps the stale watermark
```

| | |
|---|---|
| `mfe_tracking` columns | `id, trade_id, symbol, position_side, close_price, amount, signal_type, close_time, tracking_until, mfe_price, mfe_pnl, last_polled_at, status, completed_at, created_at` |
| 🔴 **a `degraded` column** | **ABSENT** |
| 🔴 **a poll-coverage count** | **ABSENT** |
| `skip_drift_samples`, for contrast | **HAS `degraded`**, plus `DRIFT_DEGRADED_GRACE_S` |

**A job that missed most of its 60-minute window finalizes as `status='completed'` and is
indistinguishable from a fully-sampled one.** The sister observatory solved this a month ago and this
module never got the fix — **the same "fixed in one place only" shape, across modules instead of
across prompts.**

🔴 **So the blocker is not the lift-out. The lift-out is the ten lines above. The blocker is that
`mfe_tracking` cannot currently tell a real MFE from a gap**, and shipping it as-is installs a
measurement that lies quietly — *worse than the gap it fills*, in the 08-01 wording. **A second hunk
is required, and I am naming it rather than hiding it inside "recoverable":**

```diff
--- a/mfe_tracker.py
+++ b/mfe_tracker.py
@@ (schema migration, alongside the existing ALTER-based column adds)
+    ('polls_ok',      'INTEGER DEFAULT 0'),   # ticks where a price was obtained
+    ('polls_missed',  'INTEGER DEFAULT 0'),   # ticks where the fetch failed
+    ('degraded',      'INTEGER DEFAULT 0'),   # set when coverage is insufficient
@@ (in _poll_once, per job)
-        new_mfe = prev_mfe
-        if current_price is not None and _is_more_favorable(…):
+        if current_price is None:
+            _bump(job_id, 'polls_missed')     # a gap is COUNTED, never assumed away
+        else:
+            _bump(job_id, 'polls_ok')
+        new_mfe = prev_mfe
+        if current_price is not None and _is_more_favorable(…):
@@ (at finalize)
+        # A window with thin coverage finalizes DEGRADED, not clean. The number is
+        # kept — the caller decides — but it can no longer be mistaken for a full
+        # sample. Same contract as skip_drift_samples.degraded.
+        degraded = 1 if polls_ok < MFE_MIN_POLLS_FOR_CLEAN else 0
```

### (c) 🔴 IS IT WORTH IT AT THIS TRADE RATE? — YES, AND THE REASON IS THE ONE YOU NAMED

Measured now: **0 closed positions on the current geometry** (nothing opened since the 17:01:29
boundary), **10 closes in the last 7 days** across the paper/live mix.

**Honest arithmetic:** at ~1 close a week on the live instrument, this tracker produces **~4 rows a
month**, and the 100 %-close-versus-partial question needs both arms populated. **It will not answer
anything this quarter.**

**And it should still be built, for exactly the reasoning that was correct for the attribution rows:
the rows cannot start accumulating until it exists.** Two things make it more pressing than it was
when the tracker was written:

1. **The ⅓ partial at +1R is now LIVE**, so the two arms of the comparison both actually occur — when
   the tracker was built there was only one arm.
2. **§2.2 established the partial and a narrower trail are SUBSTITUTES, not complements** — a
   question that has never had data, and this is the instrument that would produce it.

**What I would not claim:** that this is urgent, or that it will inform the next geometry decision. It
will not. It is a seed, and its value is that the seed is cheap.

### (d) ✅ CONFIRMED — LIFTING THE TRACKER OUT CANNOT RE-ENABLE THE SWEEP HANDLER

| check | result |
|---|---|
| does the diff touch `_handle_liquidity_sweep`? | **No** — it only ADDS a call in `virtual_trader._do_close` |
| does `mfe_tracker` import `liquidity_sweep`? | **No** — `sqlite3`, `threading`, `time`, `datetime` only |
| does the handler stay unreachable? | **Yes** — gated by `signal_type in ('EQH','EQL')`, which 20,721 rows have never satisfied |
| `EQH_EQL_SMART_TP_ENABLED` | **`False`** (set at 19:38, revival refused on §2.6's −971 simulated) |
| the old call at `main.py:3643` | **left in place** — it is inside dead code; removing it would delete the evidence of which path is legacy |

🔴 **Reviving the measurement is not reviving the strategy, and the diff keeps them separate: the
smart-TP stays dead by flag AND by unreachable trigger, independently.**

### 🔴 MY RECOMMENDATION, STATED SO YOU CAN OVERRULE IT

**Approve both hunks together, or neither.** The lift-out alone gives a measurement that cannot
distinguish a real watermark from a network gap, on a question whose whole point is a fine comparison
between two exit shapes. **Ten lines of lift-out plus a coverage marker is the honest price; ten lines
alone is the 08-01 defect installed deliberately.**

---

## 3. ⏳ THE ITEM OPEN SINCE 19:15 — FIFTH REPORT, STILL OPEN, AND NOW WITH A PRECISE CAUSE

**No stored prompt with per-wall percentiles has landed.** Confirmed directly: **0 rows** in `trades`
whose `ai_user_prompt` contains a per-wall percentile, anywhere in the table.

| | |
|---|---|
| last consultation of ANY kind | **2026-08-05 16:40:10 UTC** — over 4 hours ago |
| consultations since the 19:08 / 19:38 / 20:31 / 20:54 restarts | **0 / 0 / 0 / 0** |

🔴 **AND THE CAUSE IS NOW NAMEABLE, WHICH IT WAS NOT IN THE LAST FOUR REPORTS.** The bot is **not
idle** — webhooks are arriving normally (`confirm_recorded` at 20:45:05, `context_recorded` at
20:20:04, `confirm_recorded` at 20:15:06). What has not happened since 16:40 is a **5m trigger
completing 3-way confluence**, which is the only event that consults the entry advisor. **The
ingestion path is alive; the advisor simply has not been asked.** That is the explanation, it is
benign, and it is still not confirmation — the 18:55 wall change, the 19:38 prompt fixes and today's
item 1 all remain verified on live data through the real code path and unverified on a stored row.

---

## LIVE STATE

| | |
|---|---|
| HEAD / `git status` | **`7472729`** / **clean** |
| open positions | **0** |
| service | active since **20:54:27 UTC**, boot reconciliation agrees (0 exchange, 0 open rows) |
| order mode | 🔴 **LIVE REAL MONEY**, $30 × 5 — unchanged |
| snapshots | `/root/backups/entry-warning-20260805-2047/` (all 38 `.py`) |
| revert | `git revert 7472729` |

**Untouched:** EMA envelope gate · HTF cascade · FLAT floor · Variant-B · score bars · risk thresholds
· geometry (SL 2.25 / trail 0.75R) · the exit prompt · `config.py` · every schema.
