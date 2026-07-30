# titan-row247-carries-adx_window-200-NOTE-GONE-not-a-regression

_2026-07-30 15:10 UTC_

---

# TITAN — 🔴 **ROW 247 CARRIES `adx_window = 200`. THE NOTE IS GONE. NOT A REGRESSION.** · §1 all green, nothing lost

_HEAD `1161802` · 🔴 LIVE, REAL MONEY · $30 × 5 = $150 notional · vpos 87 LONG **still open**, −0.14R_

---

## DECISION LINE

**The one time-gated observation has resolved, and it resolved the good way.** Row **247** landed at
**15:05:42.84** carrying **`adx_window = 200`** — the first row in the table's history to carry a
window at all. The exit consult six seconds later (**19761**, `hourly`, verdict **`hold`** @ 0.62)
rendered `regime_now` **without the 🔴 NOTE**, because both ADX figures finally sit on the same
window. §1 is green on every item: nothing was lost.

**And the fix's value is now on the record in the advisor's own words rather than as an argument.** At
13:05, pre-fix, it held a live LONG citing *"1h ADX rising (22.3) shows strengthening trend"* — a rise
that never happened. At 15:05, post-fix, on comparable numbers, it said *"1h still bull but
weakening."*

⚠️ **One correction to my own earlier arithmetic:** the 14:19 report predicted row 247's magnitudes as
`≈15 / ≈45 / ≈33`; the actual is `18.58 / 38.74 / 20.58`. **All three missed**, the 5m badly. They were
extrapolations from an hour-old market, they were never the test, and they are scored in §2a rather
than dropped.

**Nothing needed fixing. No code was changed in this session. No flag was touched.**

---
# titan-nothing-lost-1161802-intact-plus-the-fabricated-rise-quoted-verbatim

_2026-07-30 15:__ UTC_

---

# TITAN — §1 GREEN, NOTHING LOST · the time-gated row __ · the advisor's own words now on record

_HEAD `1161802` · 🔴 LIVE, REAL MONEY · $30 × 5 = $150 notional · vpos 87 LONG open_

---

## 1 · NOTHING WAS LOST — every item on the list, checked

**Nothing is off. Proceeding to §2.**

### Git and runtime identity

| check | result |
|---|---|
| `git status --porcelain` | **empty — clean** |
| HEAD | **`11618025ebb902b624ebef71bc6c545c149a891b`** · `2026-07-30 14:10:47 +0000` · *"fix(titan): one ADX, one window — and the guard that makes a foreign window unusable"* |
| `HEAD` vs `origin/main` | **identical hash — in sync** |

🔴 **Runtime = commit BY HASH, not by mtime.** Every runtime file on disk hashes identically to its
blob at HEAD — so what the worker imported is what the commit contains:

| file | disk sha256[:12] | `git show HEAD:` sha256[:12] | |
|---|---|---|---|
| `main.py` | `fb4337c3ccc0` | `fb4337c3ccc0` | ✅ |
| `virtual_trader.py` | `efc10b0a4fe8` | `efc10b0a4fe8` | ✅ |
| `indicators.py` | `53e2913b8100` | `53e2913b8100` | ✅ |
| `sensor_events.py` | `3827ddd5e2c1` | `3827ddd5e2c1` | ✅ |
| `config.py` | `0e1d3e9167c5` | `0e1d3e9167c5` | ✅ |
| `order_adapter.py` | `93dfcf32b6f8` | `93dfcf32b6f8` | ✅ |
| `claude_advisor.py` | `85d26cc0518b` | `85d26cc0518b` | ✅ |
| `breakeven_worker.py` | `87e39b3a2157` | `87e39b3a2157` | ✅ |

**And nothing was edited under the running worker:** worker pid `319878` started **14:11:12**; `.py`
files with mtime **after** that instant: **0**. Newest sources are `sensor_events.py` 14:09:52 and the
other three at 14:08:21 — all **before** the worker started.

### Service

| check | result |
|---|---|
| `titan.service` | **active (running)** since **2026-07-30 14:10:59 UTC** |
| uptime at check | ~41 min |
| `NRestarts` | **0** |
| master / worker pid | `319804` (14:10:59) / `319878` (14:11:12) |
| tracebacks · `CRITICAL` · `REFUSING TO START` · `OperationalError` · `no such column` · 🚨 · `MANUAL ACTION REQUIRED` since 14:10:59 | 🔴 **0 — zero matches across all 79 journal lines** |
| circuit breaker | **untripped** — `_UNSAFE_STATE` is in-process and reset by the restart; its trip print `"breaker is tripped"` has **0** occurrences since 14:10:59 |
| Mercury-SOL | **active**, up since **2026-07-21 06:39:33**, `NRestarts=0` — **untouched** |

⚠️ **One thing that looks like an error and is not, stated so it is not mis-read later:** `trades` rows
carry `ai_decision='risk_halt'` every few minutes since the restart. The reason string is
**`"position-cap halt: 1 LONG already open (cap=1)"`** — that is the position cap refusing a *second*
LONG while vpos 87 is open. Expected, benign, and the same behaviour seen while vpos 86 was open.

### Four boot gates — verbatim

```
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 1 exchange position(s), 1 open row(s)
[RECONCILE] boot reconciliation starting
[RECONCILE] engine owns positions — NOT enqueueing a breakeven job for LONG (item 12a: single owner)
[RECONCILE] LONG open, SL present @ 64028.8 — kept.
[RECONCILE] done
```

### 🔴 LIVE banner — verbatim

```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
[TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
```

### Flags at runtime — read from `config` as the process imports it

| flag | value |
|---|---|
| `LIVE_TRADING_ENABLED` | **True** |
| `ORDER_ADAPTER_LIVE` | **True** |
| `EXIT_ADVISOR_DRYRUN` | 🔴 **False** — *a `close` verdict CLOSES* |
| `SMART_EXIT_DRYRUN_SAMPLE_SEC` | 3600 |
| `ADX_BELOW_FLOOR` | 20.0 |
| `LEVERAGE` | 5 |
| `indicators.ADX_CANDLE_LIMIT` | **200** (= `indicators.CANDLE_LIMIT` 200) ✅ the fix's constant is live |

*(Read by importing `config` and `indicators` only. `virtual_trader` was **deliberately not imported** —
§2.33: its module-scope `init_db()` migrates the production schema on import.)*

### Exchange — BOTH probes, and they agree

```
=== PROBE 1 — unified fetch_positions ===
  side=long contracts=0.0023 entry=64838.7 uPnL=-0.2612 posId=2082799688088776706
  count=1

=== PROBE 2 — raw swapV2PrivateGetUserPositions ===
  positionId=2082799688088776706 side=LONG amt=0.0023 avg=64838.7 uPnL=-0.2612
  count=1

=== OPEN ORDERS ===
  id=2082799690256592896 type=STOP_MARKET stopPrice=64028.8 closePosition=true status=NEW side=SELL
  count=1

=== BALANCE === free=479.8998 used=29.8258 total=509.7256
```

**One position on both probes, one order, no orphans.**

### vpos 87 — DB row vs exchange, same `stop_order_id`

| field | DB row 87 | exchange |
|---|---|---|
| status | `open` | LONG present, both probes |
| entry / size | `initial_fill_price` **64838.7** · `step_size` **0.0023** · lev 5.0 | avg **64838.7** · amt **0.0023** |
| 🔴 `stop_order_id` | **`2082799690256592896`** | **`2082799690256592896`** — `STOP_MARKET stopPrice=64028.8 closePosition=true status=NEW` |
| stop price | `sl_price` **64028.8** = `original_sl_price` **64028.8** (never moved) | stopPrice **64028.8** |
| `recheck_status` | `done` | — |
| `initial_risk_usdt` | 1.86282508162303 | — |
| water_mark / max_adverse | 65121.0 / 64598.0 | — |
| opened_at | 2026-07-30T12:05:17.499868+00:00 | — |
| close_price / close_reason / net_pnl / closed_at | **all NULL — not closed** | — |
| `entry_adx_1h` / `entry_adx_1h_window` | 13.516319594647 / **NULL** | — |

⚠️ `entry_adx_1h_window` is **NULL on vpos 87 and that is correct, not a miss**: vpos 87 was entered at
**12:05:17**, hours before the fix. The column only gets a value from the *next* entry.

**Position now:** last **64724.2** → gross **−0.2633 USDT** = **−0.1414R**; **+0.859R above the stop**.
Exchange uPnL **−0.2612** on both probes (the small delta is mark-vs-last, not a disagreement).

**§1 verdict: nothing was lost. Everything on the list is green.**

---
## 2 · THE TIME-GATED CHECK — **ROW 247 CARRIES `adx_window = 200`. NOT A REGRESSION.**

### a) The sampler row — the query verbatim, and its output

```sql
SELECT id, ts, adx_1h, adx_15m, adx_5m, adx_window
FROM smart_exit_dryrun_samples WHERE vpos_id=87 ORDER BY id DESC LIMIT 3;
```

```
id   ts                                adx_1h  adx_15m  adx_5m  adx_window
---  --------------------------------  ------  -------  ------  ----------
247  2026-07-30T15:05:42.835959+00:00  18.58   38.74    20.58   200
246  2026-07-30T14:05:31.968691+00:00  17.96   46.18    32.3
245  2026-07-30T13:05:31.028782+00:00  22.3    49.56    48.66
```

🔴 **Row 247 landed at 15:05:42.84 — observed live at 15:05:43 — and it carries `adx_window = 200`.**
**The regression I committed to in advance did NOT occur.** The patched `virtual_trader` is loaded in
the running worker and the sampler path is writing provenance. Row 247 is the **first row in the
table's history** to carry a window; the 246 before it are all NULL.

**Predicted vs actual, so the forecast is scored rather than quietly dropped.** The 14:19 report
predicted `≈15 / ≈45 / ≈33`:

| | predicted | **actual** | |
|---|---:|---:|---|
| `adx_1h` | ≈15 | **18.58** | +3.6 off |
| `adx_15m` | ≈45 | **38.74** | −6.3 off |
| `adx_5m` | ≈33 | **20.58** | −12.4 off |
| `adx_window` | **200** | 🔴 **200** | ✅ **the only part that was a claim about the patch** |

The three magnitudes were extrapolations from an hour-old market and they missed — **stated plainly
rather than skipped.** They were never the test. The test was the window, and the window is **200**.

**Why this is a real confirmation and not a coincidence — the path was traced statically BEFORE the row
landed**, so a NULL could not later have been explained away as a sampler quirk:

| link | verified |
|---|---|
| `_tf_metrics_safe` (`virtual_trader.py:1949`) | `m['adx_window'] = adx.window`, where `adx = indicators.adx_reading(exchange, symbol, tf)` |
| `adx_reading` | returns `AdxReading(v, ADX_CANDLE_LIMIT, tf)`; `ADX_CANDLE_LIMIT` read live from the process = **200** |
| the sampler INSERT (`:2164`) | column list ends `…wall_sl_breached, adx_window`; value tuple ends `m1h.get('adx_window')` |
| arity | **49 columns = 49 placeholders — MATCH** (checked because a mismatch would mean *no row at all*, a different symptom from a NULL) |

### b) The exit consult after it — `regime_now` VERBATIM

**Consult `19761`, `2026-07-30 15:05:46`, trigger `hourly`.** Straight from `trades.ai_user_prompt`:

```
Regime at ENTRY vs NOW
  At entry: regime=TREND 1d=neutral 4h=bull 1h=bull ADX1h=13.5
  Now:      15m=neutral 5m=neutral ADX1h=18.6 ADX15m=38.7
  Volume:   vol_1h=1.89 vol_15m=0.86 ATR change vs entry=+4.9%
```

🔴 **THE NOTE IS GONE.** Checked as a string test on the stored prompt, not by eye:

```
NOTE present in prompt 19761 ?  False
"DIFFERENT candle windows" ?    False
```

Both figures now sit on 200 candles, `_comparable` is True, and the block prints plainly — exactly the
behaviour committed to in advance.

**And here is what that actually bought, which is the point of the whole fix.** The last consult before
the restart, `19740` at 14:05:36, rendered — on the old code, on the 42-candle sample:

```
  At entry: regime=TREND 1d=neutral 4h=bull 1h=bull ADX1h=13.5
  Now:      15m=neutral 5m=neutral ADX1h=18.0 ADX15m=46.2
```

no NOTE (the old code had none) and no way for the advisor to know the two numbers were not the same
measurement. 🔴 **The advisor duly acted on it. Its own words, from the journal, real money, verbatim:**

```
Jul 30 13:05:34 [EXIT-ADVISOR-LIVE] trigger=hourly BTC/USDT:USDT LONG close=False conf=0.72
  | Entry thesis intact: 15m hyperwave and 5m bullish OB still active;
    1h ADX rising (22.3) shows strengthening trend.
```

**"1h ADX rising (22.3) shows strengthening trend"** — cited as a reason to HOLD a live LONG. The 22.3
was a 42-candle warm-up artefact; the entry 13.5 was 200-candle. **That rise never happened.** Compare
today's post-fix reason for the same position, which no longer leans on the 1h ADX at all:

```
Jul 30 15:05:47 [EXIT-ADVISOR-LIVE] trigger=hourly BTC/USDT:USDT LONG close=False conf=0.62
  | Entry thesis (4/4 MTF bull alignment, 15m/5m agreement on LONG, strong book depth) remains
    partially intact despite -0.14R drawdown. 15m HyperWave and 5m bullish OB still active.
    However, regime has shifted: ADX15m spiked to 38.7 (volatile), imbalance flipped to 70th pct
    (bearish lean), supporting wall collapsed from 5.0x to 0.0x. 1h still bull but weakening.
```

⚠️ **An honest note on the 13.5 → 18.6 that now appears:** *this* one is a genuine, comparable rise —
both sides are 200-candle. **The fix does not suppress the 1h ADX rise; it makes it real.** The advisor
read it correctly this time and called 1h *"still bull but weakening"* rather than *"strengthening"* —
the 15m collapse (46.2 → 38.7) and the supporting wall going to 0.0x now dominate its reasoning, as
they should.

### c) Every exit consult since 14:10:59

```sql
SELECT id, timestamp, signal_type, ai_decision, ai_confidence
FROM trades WHERE signal_type='exit_ai_dryrun' AND timestamp >= '2026-07-30 14:10:59' ORDER BY id;
```

| id | UTC | trigger | verdict | confidence | position R |
|---|---|---|---|---|---:|
| **19761** | **15:05:46** | `hourly` | 🔴 **`hold`** (`close=False`) | **0.62** | **−0.14R** |

**Exactly ONE, and it is the row 247 consult.** Nothing else — the restart was 14:10:59 and the
previous consult had fired at 14:05:36, five minutes earlier, so 15:05 was the next hourly turn.

🔴 **`EXIT_ADVISOR_DRYRUN` is `False` and the label proves the path knew it** — the journal line reads
`[EXIT-ADVISOR-**LIVE**]`, not `DRYRUN` (the 81875c9 label fix). **A `close` here would have closed a
real position. The verdict was `hold`, so there is no close sequence to show — nothing fired, no fill,
no fee.** Emitted by pid **319878**, the post-restart worker.

*(Not exit consults, listed so the journal is not mis-read: `trades` also carries `risk_halt` rows every
few minutes with reason `"position-cap halt: 1 LONG already open (cap=1)"`. That is the position cap
refusing a second LONG. Expected.)*

### d) Has vpos 87 closed by any route? — **NO**

| | |
|---|---|
| `status` | **`open`** |
| `close_price` · `close_reason` · `net_pnl` · `total_fees` · `closed_at` | **all NULL** |
| stop | `sl_price` **64028.8**, unchanged, `stop_order_id` **`2082799690256592896`** |
| exchange, unified | `long 0.0023 @ 64838.7 uPnL −0.2422 posId 2082799688088776706` |
| exchange, raw `swapV2` | `LONG 0.0023 @ 64838.7 uPnL −0.2424 posId 2082799688088776706` |
| open orders | **1** — `2082799690256592896 STOP_MARKET 64028.8 NEW` |
| last | 64737.7 |

**Not closed by the advisor, not by the stop, not by any other route. Both probes agree; one position,
one order, no orphans.** So (d) has no close to finalise — the question is answered by its absence,
which is checked here rather than assumed from (c).

**Post-check health, re-run after the consult:** `titan.service` **active**, `NRestarts=0`,
tracebacks / `CRITICAL` / `OperationalError` / `no such column` / 🚨 since 14:10:59 → **0**.

---
## 3 · WHAT IS OPEN — in the order you set it

### 1️⃣ FIRST — the observatory `on_entry` identity guard (§2.28a) · **code, unwritten**

**The defect, restated from §2.28a:** `post_exit_observatory.on_entry` treats `vpos_id` as a **stable
identity**. It is not — `virtual_positions.id` is unique only among rows that **still exist**. When ids
are deleted and re-issued, `on_entry`'s `ON CONFLICT(vpos_id) DO NOTHING` **silently adopts a stale
ghost row** instead of arming a fresh one. That is exactly how today's real vpos 86 inherited ghost
row 79.

**The §2.19-shaped fix (agreed shape, NOT written and NOT yet proposed):** make the conflict **speak**
— if the existing row's `opened_at` differs from the incoming one, that is a **different position**, so
`on_entry` must **refuse and shout**, not adopt.

🔴 **This is genuinely first.** §2.28a: *"Neither [row] should be touched before the `on_entry` guard
exists, or the next id re-use recreates exactly the same row."* Repairing data before the guard is
building on the same sand.

⏱️ **And it is not urgent in the trading sense but it IS time-boxed by the book:** observatory row **85
is vpos 87**, `status='shadow_armed_pending_close'`. The guard does not affect it. But the *next* entry
after vpos 87 closes will call `on_entry` again — and `sqlite_sequence` is the mechanism that made this
happen once already.

### 2️⃣ THEN — observatory data decision A: **row 80 terminal status** · **yours, one column**

| | |
|---|---|
| current | `id=80` · `vpos_id=**89**` · `status='shadow_pre_close'` · entry 63595.5 · orig SL 64714.5 · opened `2026-07-29T21:50:11` · `shadow_exit_at` **set** (02:00:05) · `shadow_pnl_r` −0.6059 · `exit_advantage_r` **NULL** |
| the problem | `virtual_positions` has **no row 89** and never will. Row 80 is **inert but immortal**: `on_15m_exit_signal` can never match it again (`shadow_exit_at` is set), and its drift slots can only be seeded by `on_real_close`, which needs a `virtual_positions` row that will never exist — **0 drift rows, confirmed just now**. `tick()` re-reads it every 5 s, forever, and it can never complete. |
| ✅ verified live | `post_exit_drift_samples WHERE observatory_id=80` → **0 rows** |
| the proposed fix | set `status` to the **existing terminal sentinel `'failed'`** — that removes it from `tick()`'s working set. **One column, on a row describing a position that never existed.** |
| why it is **your** call | `feedback_no_delete_virtual_positions` is standing; this is a data write to the book |
| no real money | §2.28a CORRECTION 1: rows 79/80 are stamped **21:50** on 07-29, inside the **paper interlude** (21:26:52 → 21:54:16), proven by the 21:53:11 boot banner `🧪 PAPER — simulated fills only`. **Neither row implicates real money.** |

### 3️⃣ THEN — observatory data decision B: **row 79, repair or retire** · **yours, harder**

| | |
|---|---|
| current | `id=79` · `vpos_id=**86**` · `status='shadow_completed'` · entry **63605.6** · orig SL **64724.6** · opened `2026-07-29T21:50:04` · `shadow_pnl_r` −0.5969 · `exit_advantage_r` **0.4253** |
| the problem | **its identity fields belong to a ghost, its drift leg belongs to the real vpos 86.** Real vpos 86 was a *different* position; row 79's `entry_price` / `original_sl_price` / `opened_at` are the ghost's. So `shadow_pnl_r` and `exit_advantage_r` are **cross-position figures**. |
| what IS sound | its **drift leg** — `on_real_close` seeded 5 slots off today's **real** 64733.0 exit. ✅ **verified live just now:** 5 slots exist; **15m sampled** (12:06:11 → 64831.3, −0.152%) and **1h sampled** (12:51:00 → 64867.1, −0.207%); **4h due 15:50:54, 12h due 23:50:54, 24h due tomorrow 11:50:54** — all three still pending. |
| repair | a status change **cannot** fix it. `entry_price`, `original_sl_price` and `opened_at` must be corrected to vpos 86's real values **and** `shadow_pnl_r` / `exit_advantage_r` recomputed. |
| retire | the alternative, if the shadow leg is not worth reconstructing — the drift leg would be lost with it, and it is still accumulating (3 of 5 slots due) |
| 🔴 standing until decided | **do not quote row 79's `exit_advantage_r`** |

### 4️⃣ AND — §2.4 as it stands

| | |
|---|---|
| 🔴 **count** | **0 of ~10.** Unchanged. |
| window opened | **`1161802`, 2026-07-30 14:10:47** — applying the ADX-window fix is the act that started the clock (§2.4-OP·3) |
| advisor consults inside the window | 🔴 **ZERO** — verified: `SELECT … WHERE signal_type='exit_ai_dryrun' AND timestamp >= '2026-07-30 14:10:47'` returns **no rows** |
| vpos 86 | contributes **ZERO** — §2.4-OP·1, strict, its first `close` verdict (01:50:24) was under the cross-source book defect |
| the nine clean-book `close` verdicts | kept as an **operational** fact in §2.4b, **not** as datapoints — and doubly inadmissible, because every one of those prompts also carried the warm-up-biased ADX (§2.26) |
| 🔴 no third restart, ever | §2.4-OP·2: *"If every fix voids the accumulated sample, the criterion becomes unfalsifiable by attrition."* A defect found **during** the window → finish it and record the caveat. **Never reset.** |
| inputs FROZEN | everything the advisor **reads**. NOT frozen: act/hold plumbing, logging, labels, close mechanics, the entire entry side. Any change to a figure rendered into the close prompt requires **voiding and restating the window in OPEN-ITEMS, in the same commit**. |
| ⚠️ the caveat already on the books | **vpos 87 straddles the boundary** — its 12:05 / 13:05 / 14:00 / 14:05 consults were made on the fabricated ADX; only consults from 15:05 onward are under the frozen prompt. If vpos 87 becomes a §2.4 datapoint, that must be recorded against it. |

---

## SUGGESTED ORDER, AND WHY

1. **`on_entry` identity guard** — code, small, §2.19-shaped, and it **gates** items 2 and 3.
2. **Row 80 → `'failed'`** — one column, zero ambiguity, stops a row being re-read every 5 s forever.
3. **Row 79 — repair or retire** — the real decision; needs your call on whether the shadow leg is
   worth reconstructing given its drift leg is sound and still filling.
4. **§2.4** needs no action — it needs **time**. It fills only when the advisor closes a position, and
   the window is 0 of ~10 with the first eligible consult only now arriving.

---

*Titan · 2026-07-30 15:10 UTC · HEAD `1161802`, clean, in sync · 🔴 LIVE · service active since
14:10:59, NRestarts=0, 0 errors · vpos 87 LONG **open** −0.14R, stop 64028.8 unchanged, order
`2082799690256592896` NEW, both probes agree · row 247 `adx_window=200` ✅ · consult 19761 `hold` 0.62,
🔴 NOTE **gone** · §2.4 = **0 of ~10** · next: observatory `on_entry` guard → row 80 → row 79*
