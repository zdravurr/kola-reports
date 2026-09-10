# Mercury-SOL — the entry prompt no longer calls an empty LuxAlgo slot "FLAT regime": one rendered line renamed, measurements put beside it, nothing computed changed

**2026-09-10 23:10 UTC · applied FROM FLAT and restarted · Mercury-SOL (LIVE, `is_paper=0`) · basis: report 2026-09-10-2250 §2c**

## What was done, in one paragraph

`market_regime` is computed in `signal_matrix.py:355` as `'TREND' if trend_net_dir != NEUTRAL else 'FLAT'` — it says FLAT whenever the matrix TREND category carries no net points (no 1H LuxAlgo trend signal has arrived, or the slot is tied). It is a signal-presence flag wearing a market-state name. The entry prompt rendered it as `Market regime: FLAT`, and after the daily regime flipped on 09-09 20:10, 19 of 32 SHORT refusals cited "FLAT regime" while the same prompt read 1h ADX 39–47 and OHLCV 1h BEAR. **The fix is prompt text only:** the line is now rendered as `LuxAlgo 1H trend slot: EMPTY or CONFLICTED (no net 1H trend signal in the matrix)` / `OCCUPIED (net 1H trend signal present in the matrix)`, followed by `Measured beside it: 1h ADX 46.4 | OHLCV trend 1h NEUTRAL / 4h BEAR`. The value, its computation, its storage and every gate that reads it are byte-identical. No instruction, threshold or constant was added. The exit prompts never rendered it, so only the entry builder changed.

**What this cannot do (§4c):** it removes one false word. It cannot stop the model reaching a wrong conclusion from correct facts, and the whole-record measurement below says the refusals it was misleading were, on the serial cut, **net losing anyway** (−10.05R over 112). Whether the advisor now takes any of those shorts is unknown until it runs; the pre-registered baseline for that is in §4d.

---

## 1. The change

### 1a. Nothing computed changed — proven by hash and AST

| file | sha256 before | after |
|---|---|---|
| `signal_matrix.py` | `a075ce05…bcfbe88f3` | **identical** |
| `config.py` | `530fb30f…512922ff` | **identical** |
| `main.py` | `a11a7cb3…c91a303` | **identical** |
| `claude_advisor.py` | `9728e26b…1fc5aeb3c` | `54e71f02…f42a63ac` |

AST of `claude_advisor.py`, before vs after: 23 functions before, 23 after, none added or removed; **exactly one function's AST differs: `consult_for_entry`**; every module-level statement (the seven system-prompt constants, the wall-rule substitutions, the client, the state-verdict cache) is AST-identical. `market_regime` is still passed in untouched (`'TREND'|'FLAT'` from `matrix_result`), still persisted to `trades.market_regime`, still read by `virtual_trader.py:1085` for `is_chop`, still read by `main.py:5219` for the advisor-unavailable flat guard — none of those files moved.

### 1b/1c. The rendered line, before and after

Before (`claude_advisor.py`, old lines 717–718):
```
  Market regime: {market_regime or 'n/a'} | MTF alignment score: {n}
```
After (new lines 733–737, plus `_slot_label` built at line 696):
```
  LuxAlgo 1H trend slot: {OCCUPIED (net 1H trend signal present in the matrix) | EMPTY or CONFLICTED (no net 1H trend signal in the matrix) | n/a} | MTF alignment score: {n}
  Measured beside it: 1h ADX {srv_adx_1h} | OHLCV trend 1h {trend_1h} / 4h {trend_4h}
```
Both measurements already existed in the prompt (the ADX row four lines above and the Higher-Timeframes block below); they are now adjacent to the label, the way the trend rows were paired on Titan 2026-08-31. The words "FLAT" and "regime" do not both appear on that line (or on any line of the user prompt — checked on both renders below). `EMPTY or CONFLICTED` is the honest reading of the code: `net_direction` is NEUTRAL both when the category has zero points and when long and short points tie (`signal_matrix.py:299–306`).

### 1d. Which builders render it

- `consult_for_entry` — **rendered it; changed.**
- `consult_for_close` (5m exit-signal consult) — never rendered it; untouched.
- `consult_for_close_state` (hourly exit advisor, called by `main.consult_exit_advisor`) — renders only the position's own ledger (side, entry, now, R, stop, MFE, giveback, trail); never rendered it; untouched.
- `consult_for_learning` — untouched.

### 1e. No instruction

The two rendered lines carry a label and three measurements. No "therefore", no threshold, no verb addressed to the model. The contract in §2d greps the rendered lines for `therefore` / `you must` / `should skip` / `should execute` and fails on any.

### 1f. Before/after on two stored consultations (verbatim)

**Row 25610 · 2026-09-10 22:20:14 · slot EMPTY at ADX 46.4** (the refusal that read `FLAT-MARKET GUARD triggered: 1h ADX 46.4 strong, but … market_regime FLAT`):

BEFORE — the stored `ai_user_prompt`:
```
Volatility / regime (multi-TF):
  ADX(14): 1h 46.4 | 15m 17.0  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.838% | 15m 0.351% | 5m 0.154%
  EMA-gap: 1h 0.552% (Contracting) | 15m 0.024% (Contracting)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 1
```
AFTER — the new builder on the same stored inputs (`_call` stubbed; no model call):
```
Volatility / regime (multi-TF):
  ADX(14): 1h 46.4 | 15m 17.0  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h n/a | 15m n/a | 5m n/a
  EMA-gap: 1h 0.552% (Contracting) | 15m 0.024% (Contracting)  (Contracting/Flat = compression)
  LuxAlgo 1H trend slot: EMPTY or CONFLICTED (no net 1H trend signal in the matrix) | MTF alignment score: 1
  Measured beside it: 1h ADX 46.4 | OHLCV trend 1h NEUTRAL / 4h BEAR
```
(ATR% reads n/a in the offline render only because its denominator is the pre-trade book mid, which the offline call does not supply; the live prompt carries it as before.)

**Row 25566 · 2026-09-10 15:25:08 · slot OCCUPIED at ADX 46.0:**

BEFORE:
```
Volatility / regime (multi-TF):
  ADX(14): 1h 46.0 | 15m 34.6  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.965% | 15m 0.564% | 5m 0.308%
  EMA-gap: 1h 0.787% (Expanding) | 15m 0.299% (Contracting)  (Contracting/Flat = compression)
  Market regime: TREND | MTF alignment score: 3
```
AFTER:
```
Volatility / regime (multi-TF):
  ADX(14): 1h 46.0 | 15m 34.6  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h n/a | 15m n/a | 5m n/a
  EMA-gap: 1h 0.787% (Expanding) | 15m 0.299% (Contracting)  (Contracting/Flat = compression)
  LuxAlgo 1H trend slot: OCCUPIED (net 1H trend signal present in the matrix) | MTF alignment score: 3
  Measured beside it: 1h ADX 46.0 | OHLCV trend 1h BEAR / 4h BEAR
```

**Known residual, stated so it is not discovered later:** the SYSTEM prompt still says `market_regime is FLAT with weak MTF alignment` and `market_regime=TREND` in its soft flat-market guard (lines 163–167, 198–199). It is byte-identical by order (§2b), so the model is still told a field by that name exists while the user prompt no longer renders one under that name. That is the accepted cost of "system prompts byte-identical"; it is recorded here, not fixed.

---

## 2. What did not change

### 2a. Constants at runtime (config.py hash identical; quoted from text after the restart)

`LIVE_FIXED_MARGIN = 20` · `LEVERAGE = 5` · `SL_BUFFER_ATR = 2.5` · `TRAIL_MULT_ATR = 1.875` · `TRAIL_ARM_R = 0.75` · `CONFLUENCE_SCORE_THRESHOLD = 2.0` · `FLAT_ADX_GATE_ENABLED = True` · **`FLAT_ADX_GATE_DRYRUN = True`** · `ADX_BELOW_FLOOR = 20.0` · `BOOK_GATE_ENABLED = True` · `BOOK_GATE_DRYRUN = False` · `BOOK_GATE_WALL_PCTL = 90.0` · `BOOK_GATE_WALL_DIST_PCT = 0.20` · `BOOK_GATE_MIN_SUPPORTING = 1` · `EXIT_ADVISOR_DRYRUN = True` · `MAX_POSITIONS_PER_SIDE = 1`. The boot line after restart prints the same geometry (§3b).

### 2b. System prompts byte-identical — sha256 before = after, 7 of 7

`_ENTRY_SYSTEM cc70ed45…` · `_ENTRY_SYSTEM_V2 894a6c20…` · `_ENTRY_SYSTEM_V2_ALIGNED f221365f…` · `_ENTRY_SYSTEM_V2_ALIGNED_SHORT e1487999…` · `_CLOSE_SYSTEM 37bcdce4…` · `_CLOSE_STATE_SYSTEM 3be10726…` · `_LEARNING_SYSTEM aa35142e…` — hashed by importing the module before and after the patch; identical.

### 2c. AST — functions changed: `consult_for_entry` only. Nothing outside the prompt builders.

### 2d. Backup and contracts

- `.bak` first: `claude_advisor.py.bak_regimeline_20260910T2300Z` (77,906 bytes, the 09-03 17:40 file).
- New contract `mercury-sol/tests/test_entry_prompt_regime_line_is_legible.py`: renders FLAT / TREND / None through the real builder with `_call` stubbed, asserts no `Market regime` line, no line with both `FLAT` and `regime`, the exact measurement line beneath the slot line, no instruction words, and the six system-prompt hashes. **OK, exit 0.**
- Workspace contract suite (`/home/botuser/.openclaw/workspace`, run as `botuser`): **baseline before the patch 263/263 green in 62 s**; after the patch: **264/264 green in 61 s** (the suite grew by one file between the two runs; every contract green both times).

---

## 3. Applied from flat

### 3a. Flat, checked twice (before the patch and again immediately before the restart)

Ledger: `virtual_positions` not-closed **0** · `active_positions` **0** · `exit_pending` **0** · last position vpos 43 closed 2026-09-06 03:58. Venue (Bybit, read-only `fetch_positions` on the bot's own key through Tor): `positionIdx 1 size 0` · `positionIdx 2 size 0` · open orders **0**.

### 3b. Restart and runtime proof

`systemctl restart mercury-sol.service` at **23:04:28 UTC**; service active since **23:04:47**, MainPID 1084680, worker 1084884, `NRestarts = 0`. Boot lines, verbatim:
```
[MERCURY-SOL] [BOOT] taker fee: 0.001 (0.1000%) source=venue | geometry constant BYBIT_TAKER_FEE_RATE=0.00055 is unchanged and separate
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 1084884]
```
`/health` → `{"bot":"MERCURY-SOL","exchange":"bybit_live","status":"ok"}`. Loaded bytecode: `__pycache__/claude_advisor.cpython-312.pyc` header (source mtime 23:02:19, size 79,177) matches the on-disk source exactly, so the worker's import accepted this bytecode; its string constants contain `LuxAlgo 1H trend slot:` and `Measured beside it: 1h ADX` and **do not** contain `Market regime:`. `openitems_guard` after: **EXIT=0**. No consultation had fired between the restart and this report (quiet minutes); the first live prompt will carry the new line by construction.

### 3c. The dryrun experiment is untouched

`FLAT_ADX_GATE_DRYRUN = True` at `config.py:407` after the restart (file hash unchanged). Its counter lives in syslog (`[FLAT-ADX-GATE] DRYRUN would-refuse …`, 136 unique rows since 09-03 19:30, 77 LONG / 59 SHORT) and survives a restart; 0 armed `REFUSE` lines since the flip. Stopping rule unchanged: revert at live ΣR ≤ +3.141R (−3R from the +6.141R baseline) OR 2026-09-17 19:45 UTC. Live book now: n 15, **+7.864R**, +$17.73 — neither condition met.

---

## 4. What this cannot fix — measured, read-only

### 4a. The misled population, whole record (2026-06-10 → 2026-09-10)

Refusals (`ai_skipped`) whose reason contains "flat"/"FLAT" **while `srv_adx_1h` > 25**:

| side | n | of which stored `market_regime` |
|---|---|---|
| SHORT | **613** | 1048 FLAT / 15 TREND across both sides |
| LONG | **450** | |
| total | **1,063** of 4,456 refusals (23.9 %) | |

By month: Jun 107 · Jul 550 · Aug 213 · Sep 193. Exposure is wider than citation: **1,323** refusals (549 LONG / 774 SHORT) carried `market_regime=FLAT` at ADX > 25 whether or not the reason mentioned it; 7 executions did too.

### 4b. Were they profitable? Serial cut, live geometry, real taker both legs, `MAX_POSITIONS_PER_SIDE=1`

Replayed on real Bybit 5m candles (27,349 bars) with ATR14(1h) from real 1h candles, SL 2.5×ATR, arm 0.75R, BE lock at ±0.20 %, trail 1.875×ATR after the lock, adverse extreme first, to its own exit.

| cut | n | ΣR | Σ$ | wins / losses | exits |
|---|---|---|---|---|---|
| **serial, cap 1 per side, both sides** | **112** | **−10.05R** | **−$17.75** | 59 / 53 | 58 trail · 49 SL · 4 BE · 1 open |
| serial SHORT only | 59 | **−13.97R** | −$29.25 | 29 / 30 | 29 SL · 28 trail |
| serial LONG only | 53 | +3.92R | +$11.50 | 30 / 23 | 30 trail · 20 SL |
| independent, all 1,063 (overlapping, shape only) | 1,063 | −172.4R | −$247.93 | 530 / 533 | 508 SL · 476 trail |

n = 112 clears the bar of 8, so this ranks: **the refusals the false word was decorating were, as a population, right to refuse — the serial short book of them loses 14R.** By month the serial shorts were −0.95R (Jun), +0.75R (Jul), **−11.86R (Aug)**, −1.92R (Sep). The 09-09/10 decline (§4 of the 2250 report, +1.08R serial) is a small positive inside a losing population.

### 4c. Plainly

This change removes one false word from one line of one prompt. It does not change what any gate computes, and it cannot stop the model reaching a wrong conclusion from correct facts — the same prompt already carried `ADX(14): 1h 46.4` four lines above the false word, and the model cited the word. Whether the advisor now takes any of those shorts is unknown and unmeasurable until it runs against live signals. The population it was misleading has a negative serial expectancy, so "taking them" is not obviously the desired outcome either. Do not read this patch as a P&L change; read it as a removed lie.

### 4d. Pre-registered baseline for the behaviour change

Advisor consultations by side, last 7 days (2026-09-03 23:01 → 2026-09-10 23:01 UTC, `open_short`/`open_long`, `ai_decision ∈ {execute, skip}`):

| side | execute | skip | **pass rate** |
|---|---|---|---|
| **SHORT** | **0** | **229** | **0.00 %** |
| LONG | 1 | 188 | 0.53 % |

Last 30 days for scale: SHORT 5 / 509 = 0.98 %, LONG 5 / 507 = 0.99 %. Within the 7-day window, 121 SHORT and 74 LONG consultations carried `market_regime=FLAT` at ADX > 25 — the sub-population the new line touches. A behaviour change is measured against **0 of 229** for SHORT, not reconstructed later.

---

## Verification block

- Titan guard: `openitems_guard` EXIT=0 before and after; Titan untouched (book gate armed 2026-09-10 14:36:20 left as is).
- Mercury-SOL: `signal_matrix.py`, `config.py`, `main.py` sha256 identical before/after; `claude_advisor.py` changed in exactly one function; 7 system prompts byte-identical; `.bak` taken first; new contract green; restart from a verified flat book and venue; boot line quoted; `NRestarts 0`; `FLAT_ADX_GATE_DRYRUN` still `True`; live book +7.864R, stop rule not fired.
- DB read-only throughout (`mode=ro`); venue GET only (`fetch_positions`, `fetch_open_orders`, kline, ticker) through the bot's Tor egress.
