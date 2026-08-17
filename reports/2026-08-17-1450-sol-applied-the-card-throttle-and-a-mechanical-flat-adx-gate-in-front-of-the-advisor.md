# Mercury-SOL — APPLIED: the card throttle, and the flat judgement taken out of the model and put in code

**2026-08-17 14:50 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · book FLAT throughout · TWO CHANGES APPLIED, service RESTARTED, boot clean.**

Titan (`/root/titan-bot`): **not touched, not read for state, no numbers imported.** HEAD `897850b`, clean.

Basis: [14:35 §3c — the card throttle](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-17-1435-sol-the-ten-cards-are-ten-real-calls-and-my-14aug-answer-measured-a-tautology.md) · [14:25 §3b — the ADX cohort, refused as candidate #27](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-17-1425-sol-the-recheck-tighten-is-a-hidden-adx-entry-filter-and-it-saved-money-on-two-of-three.md)

---

## ⚡ WHAT CHANGED

| | |
|---|---|
| **`AI_SKIP_CARD_THROTTLE_S = 1800`** | one AI SKIP card per (direction, combo, verdict) per 30 min. **Rows untouched.** |
| **`FLAT_ADX_GATE_ENABLED = True`, `FLAT_ADX_GATE_DRYRUN = False`** | 1h ADX(200) < `ADX_BELOW_FLOOR` (20.0) → **REFUSE**, status `flat_adx_blocked`, **before the advisor is consulted** |
| `skip_attribution.TRACKED_STATUSES` | `+ 'flat_adx_blocked'` — registered **and the hook called at the refusal site** |
| **NOT touched** | `_STATE_VERDICT_TTL_S` (60 s), `SL_BUFFER_ATR` (2.5), `TRAIL_ARM_R` (0.75), `TRAIL_MULT_ATR` (1.875), `POST_ENTRY_RECHECK_ENABLED` (True) |

**Files:** `config.py`, `main.py`, `skip_attribution.py` — each backed up to `*.bak_cardthrottle_flatadx_20260817` **before** the first edit.

**Isolation harness: 25 checks, ALL PASSED**, run against a full copy of the tree with a lock on the live path. **One finding it produced that no reading would have caught — §5.**

---

# 1. THE CARD THROTTLE

## 1a. Applied as designed

```python
# main.py — process-local, like claude_advisor's verdict cache, and sufficient for
# the same reason: gunicorn_mercury.conf.py is workers=1 threads=4.
_skip_card_lock = threading.Lock()
_skip_card_last = {}          # key -> [monotonic_at_first_sent, suppressed_count]

def _skip_card_due(direction, combo, verdict):
    if not AI_SKIP_CARD_THROTTLE_S:
        return True, 0
    key = (direction, combo, verdict)
    now = time.monotonic()
    with _skip_card_lock:
        prev = _skip_card_last.get(key)
        if prev is None or now - prev[0] >= AI_SKIP_CARD_THROTTLE_S:
            n = prev[1] if prev else 0
            _skip_card_last[key] = [now, 0]
            return True, n
        prev[1] += 1
        return False, prev[1]
```

At the send site the card now reads, when it has swallowed anything:

> `(+12 identical skip(s) in the previous 30 min — all rows in the DB)`

## 1b. 🔴 EVERY DB ROW IS STILL WRITTEN — proved by execution, not by reading

The harness parses `main.py` and compares **line positions inside the branch**, so this is a property of the shipped file rather than of my recollection of it:

```
PASS  the ai_skipped ROW is written BEFORE the throttle runs  — update_trade L5264 < throttle L5281
PASS  skip_attribution is recorded BEFORE the throttle runs   — attribution L5270 < throttle L5281
```

`update_trade(row_id, status='ai_skipped', …)` and `_record_skip_attribution(…, 'ai_skipped', …)` both execute **seventeen and eleven lines earlier** than the throttle. By the time `_skip_card_due` runs, the row exists, the attribution row exists, and the advisor call has already happened. **The throttle decides one thing only: whether the phone buzzes.** The suppression branch says so out loud in the journal:

```
[SKIP-CARD] throttled — row=<id> WRITTEN, card suppressed (<n> in this window) <dir> <combo>
```

## 1c. 🔴 AN `execute` CANNOT BE THROTTLED — on any path

Three independent proofs, all from the parse tree:

```
PASS  _skip_card_due has exactly ONE call site in main.py                 — 1 call site
PASS  that call site passes the LITERAL 'skip', never a variable
PASS  a DIFFERENT VERDICT ('execute') is never throttled                  — real helper, executed
```

The single call site sits inside `elif ai_decide == 'skip':`, in the non-DRYRUN arm. An `execute` verdict never enters that branch at all — it falls through to `_execute_single_entry`. And the third argument is the string constant `'skip'`, not `ai_decide`, so even a future edit that moved the helper could not carry an execute into it silently. **No `send_tg` on any entry, fill, exit, alert or gate path passes through this helper.**

## 1d. Replayed against the real burst

The helper — extracted from the shipped `main.py` **by AST, not retyped** — replaying 2026-08-16 12:00–13:00:

```
PASS  a 13-card burst emits exactly ONE card              — sent=1
PASS  12 suppressions counted                             — 12
PASS  an EXPIRED window sends again
PASS  and it carries the swallowed count                  — swallowed=12
PASS  a DIFFERENT DIRECTION is never throttled
PASS  a DIFFERENT COMBO is never throttled
PASS  5m trigger name is NOT in the key (same combo still collapses)
PASS  AI_SKIP_CARD_THROTTLE_S=0 disables the throttle entirely
```

The last-but-one is the one that matters for this defect: the real burst contained eleven `Within Bullish OB` and one `Bullish Breaker` under **one** combo_key, and the throttle collapses them because the 5m trigger name is not in the key.

## 1e. `_STATE_VERDICT_TTL_S` is untouched — deliberately

Still **60.0**. Raising it means applying a 12:00 verdict at 12:20 on a book that has moved, and the same burst already shows the wall level changing twice inside the hour. That is a risk trade needing its own measurement, and it is not this pass.

---

# 2. THE FLAT-ADX GATE

## 2a. Where it sits — exactly

```
webhook → state machine → HTF cascade → score gate → entry lock → risk gate
        → wall-avoidance filter → _pre_walls fetch (OKX-4000)
        → 🔴 FLAT-ADX GATE          ← L4911
        → BOOK GATE                  ← L4979
        → consult_for_entry          ← L5053
        → _execute_single_entry
```

```
PASS  the gate is BEFORE consult_for_entry              — gate L4911 < consult L5053
PASS  the gate is BEFORE the book gate                  — book  L4979
PASS  the gate is AFTER the _pre_walls fetch            — walls L4863
```

**Four ordering decisions, each with a reason:**

1. **Before `consult_for_entry`** — the same reason the book gate is. A judgement the model applies inconsistently must not be left to the model. It also saves the ~5 s Claude call on every refusal.
2. **Before the book gate** — "there is no trend" does not depend on the order book at all, so it is the more fundamental refusal and takes precedence when both would fire. This keeps `flat_adx_blocked` from ever being masked by `book_blocked`, so the two refusal counts stay attributable.
3. **After the `_pre_walls` fetch** — so `_record_skip_attribution` still gets its wall anchor and the refusal is drift-measurable later. One OKX read on a refused entry is the price of the refusal being measurable at all.
4. **Inside the `_entry_gate` lock** — a refusal returns through the same `finally` release as every other refusal in the block.

## 2b. 🔴 THE NUMBER IT READS IS THE NUMBER THE ROW PERSISTS

The gate reads `_adv_snap['srv_adx_1h']`:

```
indicators.fetch_snapshot(exchange, symbol, tfs=HTF_TFS, limit=CANDLE_LIMIT=200)
  -> _fetch_ohlcv_cached(symbol, '1h', 200) -> compute_tf_metrics -> ta.adx(length=14)
```

`virtual_positions.entry_adx_1h` — the value the recheck later reads — comes from:

```
indicators.adx_reading(exchange, symbol, '1h')
  -> _fetch_ohlcv_cached(symbol, '1h', ADX_CANDLE_LIMIT=200) -> compute_tf_metrics -> ta.adx(14)
```

**Same cache slot, same 200 bars, same function.** Not argued — measured on the book:

| vpos | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 |
|---|---|---|---|---|---|---|---|---|
| `trades.srv_adx_1h` | 53.200 | 30.928 | 23.419 | 26.350 | 12.780 | 18.953 | 21.125 | 24.668 |
| `virtual_positions.entry_adx_1h` | 53.200 | 30.928 | 23.419 | 26.350 | 12.780 | 18.953 | 21.125 | 24.668 |
| **delta** | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** |

**Eight of eight, exact** — every row written since the 2026-08-07 window fix, i.e. every row whose window is recorded as 200. On the 22 rows **before** that fix the same two columns diverge by up to **31.84 points** (vpos 21: 28.918 vs 60.759), which is the defect the window fix closed and the reason the gate reads the 200-bar side. **A refusal is therefore reproducible from the stored row.**

## 2c. One threshold, one definition

`ADX_BELOW_FLOOR = 20.0` is reused directly — the bot's own constant, load-bearing in `_health_score` since A16, with a 9-of-9 prediction record in the post-fix era. **No new constant was created**, and the harness enforces that structurally (§5).

## 2d. The refusal is countable from day one

```python
update_trade(row_id, status='flat_adx_blocked', combo_key=combo,
             confluence_score=direction_score,
             matrix_direction=matrix_result['direction'], error=_fa_reason)
_record_skip_attribution(row_id, symbol, direction, 'flat_adx_blocked',
                         matrix_result=matrix_result, confluence_score=direction_score,
                         pre_trade_walls=_pre_walls, ai_reason=_fa_reason,
                         srv_adx_1h=_flat_adx)
send_tg(f"📉 <b>FLAT REFUSED ENTRY</b> (ADX {_flat_adx:.2f} &lt; {ADX_BELOW_FLOOR:.0f}) …")
```

```
PASS  the branch writes status='flat_adx_blocked'
PASS  the branch CALLS _record_skip_attribution (not merely registers the status)
PASS  the branch sends a card naming the ADX value
PASS  the branch returns (nothing downstream can run)
PASS  the gate honours FLAT_ADX_GATE_DRYRUN
PASS  'flat_adx_blocked' registered in TRACKED_STATUSES
```

**Registering the status is half of it; calling the hook is the half that was missing on Titan when the FLAT floor's 518 refusals went uncounted for a month.** Both halves shipped in this pass.

## 2e. It fails open

```
PASS  every NULL ADX ADMITS (fail-open)  — 106 NULL rows, none refused
PASS  FLAT_ADX_GATE_ENABLED=False admits everything
```

A missing or unreadable ADX admits. An indicator outage must never become a trading halt.

## 2f. 🔴 THE PRE-REGISTERED REFUSAL RATE — and the shipped predicate reproduces it

The harness lifts the **actual `if` test out of the shipped `main.py` by AST** and evaluates it against all 3,803 historical consultations:

```
PASS  predicate reproduces the PRE-REGISTERED 1,264 refusals of 3,803  — 1264 of 3803
      LONG : 577/1702 = 33.9 %
      SHORT: 668/1968 = 33.9 %
PASS  the rate is SYMMETRIC by side (<2pp apart)
```

| | rate |
|---|---|
| **of consultations, whole history** | **33.2 %** (1,264 of 3,803) |
| LONG / SHORT | **33.9 % / 33.9 %** — symmetric |
| last 30 days | **41.6 %** — the tape has been flat |
| **of entries that became positions** | **19.4 %** (6 of 31: vpos 11, 17, 27, 28, 34, 35) |

🔴 **PRE-REGISTERED: expect the realised rate in the 33–45 % band.** A realised rate materially above that band is **a finding about the reading** — a different window, a different cache, a different timeframe — **and it is not a reason to lower the threshold.** Find out which ADX is being read before anyone touches 20.

*(The entry-level cohort is all SHORT, 6 of 6. That is n=6 against a consultation-level split that is symmetric to 0.0 pp, so it is read as small-sample noise and recorded rather than acted on.)*

## 2g. 🔴 WHAT IT DOES TO THE RECHECK TIGHTEN — a falsifiable prediction

The three tightens ever fired on entries at **ADX 15.95 (vpos 27), 12.78 (vpos 34), 18.95 (vpos 35)** — all below 20. **This gate would have refused all three before they opened.**

And on the observed book the ADX floor is the **only** route that has ever reached the threshold: `HEALTH_SCORE_TIGHTEN = −5`, the ADX floor alone scores −5, and the 28 rows marked `'done'` mean every tier scored **> −5** for them. So:

> 🔴 **PRE-REGISTERED: the recheck tighten's firing rate should now fall toward ZERO.** Its historical rate is 3 in 31 positions (9.7 %). The residual routes — wall growth (−5/−10), ADX drop (−3), ATR contraction (−3), adverse price (−1/−3) — have never in 31 positions summed to −5 without the ADX floor.
>
> **IF IT KEEPS FIRING AT ANYTHING LIKE 9.7 %, THE GATE IS NOT READING WHAT THE RECHECK READS.** That is the diagnosis to run first, not a reason to touch either constant.

**The tighten STAYS ENABLED.** It saved 0.964R on the closed book and it is the backstop for the case where the gate is killed by its own switch, or where a position's ADX collapses *after* entry — which the gate cannot see and the recheck can.

**One consequence, stated because it is a real change to a live path:** the non-AI flat-market guard at `main.py:5194` (`1h ADX < ADX_FLAT_FLOOR AND regime FLAT`, on the `claude_unavailable` auto-execute fallback) is now **downstream of a gate that refuses on the ADX clause alone**. Its ADX condition becomes unreachable while `FLAT_ADX_GATE_ENABLED` is True. It is left in place deliberately — it is Titan-parity code and it is exactly what the kill switch falls back to.

## 2h. 🔴 THE BASIS, WRITTEN INTO THE FILE — discipline, not a measured edge

The full text is in `config.py`. Its load-bearing paragraphs:

> **WHY IT IS IN CODE AND NOT LEFT TO THE MODEL — THE JUDGEMENT IS SOUND, THE APPLICATION IS NOT.** The advisor already refuses flat markets and already cites this exact number … Across the whole book it skipped **1,242 of the 1,263 sub-20 consultations it saw — 98.3 %**. And then it said EXECUTE on the other 21, four of which became the chop shorts vpos 27, 28, 34 and 35 at ADX 15.95 / 14.14 / 12.78 / 18.95.
>
> **THAT IS THE SAME SHAPE AS THE ORDER BOOK, AND IT TAKES THE SAME REMEDY.** There, four of four checkable book claims the advisor made were FALSE and the fix was to put the book in front of it. Here the claims are not false — they are RIGHT 98.3 % of the time and abandoned the rest. **A judgement that is correct and inconsistently applied is not a model problem to be prompted away; it is a decision that belongs in code, where it cannot lapse.**
>
> **THIS IS DISCIPLINE, NOT A MEASURED EDGE. SAY IT PLAINLY, BECAUSE IT WAS MEASURED AND IT DID NOT PASS.** [14:25] §3b measured the sub-20 cohort as an ENTRY candidate and REFUSED it as candidate #27: n = 6 positions, **TWO of them winners**, cohort mean −0.142 R/trade against −0.092 R for the other 23 … It is applied ANYWAY, for two reasons that are not statistical: (1) a bot that trades a market with no trend is doing something a discretionary trader would not do — the absence of a measurable edge in 6 trades is not evidence that trading chop is fine, it is evidence that 6 trades cannot tell; (2) **this bot already acts on this exact threshold, twice, and only after the money is committed.**
>
> **IF A LATER PASS MEASURES THIS AND FINDS NO EDGE, THAT IS THE EXPECTED RESULT AND IT IS NOT GROUNDS TO REMOVE THE GATE.** It was already measured, and it already found no edge. Do not re-run the same cohort test and read it as new. **THE GROUNDS FOR REMOVAL ARE THESE THREE, AND ONLY THESE:** (a) it fires too often — materially above the pre-registered rate; (b) it fires asymmetrically by side — a side ban is not a rule; (c) it refuses trades a trader would take — inspect the refused rows, not the R.

---

# 3. THE PRE-REGISTERED COUNT — CONFIRMED, IT STANDS

🔴 **Neither change moves 1R, so the count survives and vpos 36–37 stay in it.**

```
1R = SL_BUFFER_ATR x ATR x size
```

- The **card throttle** touches one `send_tg`. It cannot reach a price, a size or a stop.
- The **flat-ADX gate** refuses an entry *before it opens*. It changes **which trades happen**, never the unit in which any trade is measured. `SL_BUFFER_ATR` is untouched at 2.5 — confirmed in the live boot line below.

| | moves 1R? | count survives? |
|---|---|---|
| `AI_SKIP_CARD_THROTTLE_S` | no — a Telegram call | ✅ |
| `FLAT_ADX_GATE_*` | no — an admission decision | ✅ |
| `SL_BUFFER_ATR` *(untouched)* | would — re-denominates every R | n/a |

**THE COUNT STANDS AT 2 OF 20** — vpos 36 (−0.757R) and vpos 37 (−1.226R), Σ −1.983R, both losers, both in.

🔴 **And the remaining 18 closes now judge a contract that INCLUDES this gate.** That is stated on the count's own record rather than discovered at close 20: closes 1–2 were taken under a contract with no flat gate; closes 3–20 are taken under one with it. The unit is identical, the population is not.

**One practical consequence, so the date is not a surprise:** the live entry rate is **1.05/day** (9 live entries, 08.08 → 16.08). The gate refuses 19.4 % of entries on the historical rate, so 18 more closes takes roughly **22 days rather than 18** — the ~03.09 estimate moves to approximately **08–09.09**. The rule is unchanged; only its arrival date moves.

---

# 4. THE ISOLATION HARNESS

Built to the standing rule — isolation is **structural, not intentional** — and searched **by DIRECTORY**, which is the part that matters:

```
grep -l "/mnt/volume_nyc1_1780480650620/mercury-sol" *.py   ->  17 files
grep -l "mercury-sol/trades.db"                  *.py   ->  14 files   <- the WEAK search
```

🔴 **Three files hide from the DB-name search** — the census has grown to **17 `.py` + `.env` = 18 vectors**, up from the 16 + 1 recorded on 2026-08-08. Searching by database filename would have left three live writers reachable, one of which (`weight_engine.py`) owns the production `dynamic_weights.json`.

Four layers, all enforced:

1. the tree under test is a **COPY**; the live path never enters `sys.path`
2. `sys.dont_write_bytecode = True`
3. the live **DIRECTORY** literal rewritten in every `.py` **and** in `.env` — 18 of 34 copied files contained it
4. a **LOCK** on `sqlite3.connect` **and** on `open()` in any write mode, raising `AssertionError` on the live path

```
PASS  zero connections or writes to the LIVE tree  — []
PASS  no .pyc written into the LIVE tree           — []
```

**25 checks, all passed.** Full transcript: constants (6), throttle behaviour (9), the shipped predicate against 3,803 rows (5), wiring from the parse tree (7), lock integrity (2).

---

# 5. 🔴 WHAT THE HARNESS FOUND THAT NO READING WOULD HAVE

The check "this pass introduces no new ADX threshold constant" is written as a **diff against the backup's parse tree**, not as a substring search. It returned:

```
before = ['ADX_BELOW_FLOOR', 'ADX_DROP_THRESHOLD', 'ADX_FLAT_FLOOR']
after  = ['ADX_BELOW_FLOOR', 'ADX_DROP_THRESHOLD', 'ADX_FLAT_FLOOR']
      ADX_BELOW_FLOOR = 20.0        ADX_FLAT_FLOOR = 20.0
```

🔴 **A SECOND CONSTANT WITH THE SAME VALUE ALREADY EXISTED, AND I DID NOT KNOW IT WHEN I WROTE THE GATE.** `ADX_FLAT_FLOOR = 20.0` (`config.py:1092`) feeds the non-AI flat-market guard on the `claude_unavailable` fallback path. `ADX_BELOW_FLOOR = 20.0` feeds `_health_score`. **Two names, one fact, one value — the one-fact-many-judges shape this codebase keeps closing, sitting in the file the whole time.**

**Nothing was changed about it, on purpose.** The `ADX_FLAT_FLOOR` block is marked *"copied byte-for-byte from titan-bot"*, so binding it to a SOL-only constant would break a stated parity invariant, and it was not in scope. **It is reported, not fixed.** The risk it carries is latent, not active: both are 20.0 today, so nothing diverges — but a future edit to one of them silently splits the bot's definition of "flat" in two. That is a candidate for its own pass, with the parity question answered first.

**Two smaller things the harness caught in itself rather than in the code**, recorded because the first version of a test being wrong is normal and hiding it is not: the substring check for `FLAT_ADX_THRESHOLD` flagged the comment that *names the constant it refuses to create*, and the AST rewrite had to use the pre-lock `open` because the guard wrapper intercepts its own reads. Both were test defects; neither touched the shipped code.

---

# 6. LIVE STATE AFTER THE RESTART

```
Aug 17 14:31:20  [AP] No active positions in DB — clean boot.
Aug 17 14:31:21  [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
Aug 17 14:31:21  Listening at: http://127.0.0.1:5002 (3630271)
Aug 17 14:31:21  Booting worker with pid: 3630429
Aug 17 14:31:21  [BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R)
                 ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 3630429]
Aug 17 14:31:21  [VIRTUAL] poller started in pid 3630429 (interval=10s)
Aug 17 14:31:21  [VPOS-RECONCILE] no open positions at boot — clean.
```

🔴 **The boot geometry line is the deployment-gap proof** (`config.boot_geometry_line`, which reads this process's own globals, never the file): **`SL_BUFFER_ATR=2.5` unchanged**, arm 0.75R, partial OFF. The R the count is denominated in is the R the running worker holds.

**Zero tracebacks. `NRestarts=0`. `ActiveState=active`. Book FLAT.** Heartbeats healthy at the 10 s cadence:

```
Aug 17 14:41:41  [VIRTUAL] [HEARTBEAT] alive ticks=53 (+26 in 308s) last_tick=11.9s
                 max_tick=12.4s cadence=10s open=0 mode=LIVE pid=3630429
```

## 6b. 🔴 WHAT IS **NOT** YET PROVEN — LIVE FIRING IS PENDING

**Stated plainly rather than left to be assumed.** In the 13 minutes since the restart the bot has received **ZERO webhooks** — `grep -c WEBHOOK_IN` over the post-restart journal returns 0 — so **neither mechanism has fired in production yet.** The journal was watched continuously for the first firing and it has not come; inbound alerts are sporadic, and at the observed ~40 consultations/day they cluster rather than arrive on a clock.

| claim | status |
|---|---|
| the code is on disk, compiled, and loaded by the running worker | ✅ **proven** (boot geometry line from this process's own globals) |
| the throttle collapses a 13-card burst to one card + a counter | ✅ **proven by execution** — the real helper, AST-extracted from the shipped file |
| the shipped gate predicate refuses 1,264 of 3,803 historical rows | ✅ **proven by execution** against the real book |
| the gate runs before the advisor / before the book gate / after the walls | ✅ **proven from the parse tree** |
| the row is written before the throttle runs | ✅ **proven from the parse tree** |
| **a real `flat_adx_blocked` row and its card in production** | ⏳ **PENDING the next qualifying webhook** |
| **a real `[SKIP-CARD] throttled` line with its row intact** | ⏳ **PENDING a repeated skip inside 30 min** |

**The first thing to check on the next pass** is one query and one grep:

```sql
select id, timestamp, matrix_direction, round(srv_adx_1h,2), error
  from trades where status='flat_adx_blocked' order by id;
select count(*) from skip_attribution where status='flat_adx_blocked';
```
```
journalctl -u mercury-sol | grep -E "FLAT-ADX-GATE|SKIP-CARD throttled"
```

**The rate to check them against is §2f (33–45 % of consultations), and the tighten count to check is §2g (should fall toward zero).** Until those rows exist this is applied-and-harnessed, not live-proven, and it is recorded that way.

---

## STATE

```
mercury-sol   active - MainPID 3630271 / worker 3630429 - since 2026-08-17 14:31:00 UTC
              NRestarts=0 - restarted BY THIS PASS on a FLAT book - boot clean, 0 tracebacks
APPLIED       AI_SKIP_CARD_THROTTLE_S = 1800          (notification only)
              FLAT_ADX_GATE_ENABLED   = True
              FLAT_ADX_GATE_DRYRUN    = False          🔴 ARMED — this gate refuses entries
              skip_attribution.TRACKED_STATUSES += 'flat_adx_blocked'
UNCHANGED     SL_BUFFER_ATR 2.5 - TRAIL_ARM_R 0.75 - TRAIL_MULT_ATR 1.875 - PARTIAL off
              _STATE_VERDICT_TTL_S 60.0 - POST_ENTRY_RECHECK_ENABLED True
              ADX_BELOW_FLOOR 20.0 (reused, not re-defined) - ADX_FLAT_FLOOR 20.0 (reported, §5)
BACKUPS       config.py / main.py / skip_attribution.py -> *.bak_cardthrottle_flatadx_20260817
HARNESS       25 checks, ALL PASSED, isolated tree + live-path lock, 0 leaks, 0 .pyc
BOOK          31 closed - SumR -7.967 - FLAT, zero open
              stopping rule: 2 of 20 live closes (vpos 36, 37) - THE COUNT STANDS
PRE-REGISTERED  flat-ADX refusals: 33-45 % of consultations, ~19 % of entries
                recheck tighten firings: should fall toward ZERO from 9.7 %
titan         /root/titan-bot - NOT touched, NOT read for state, NO numbers imported.
              HEAD 897850b - working tree clean
```

**Provenance: every line number, constant and code block quoted from the files as they now stand on disk; the 8-of-8 ADX identity read from `trades` joined to `virtual_positions` under `mode=ro`; the refusal rate produced by evaluating the SHIPPED `if` test lifted from `main.py` by AST against all 3,803 historical rows; the boot lines quoted from `journalctl -u mercury-sol`. Titan was not read.**
