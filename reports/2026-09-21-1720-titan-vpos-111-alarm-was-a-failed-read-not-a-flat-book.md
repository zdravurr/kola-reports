# titan-vpos-111-alarm-was-a-failed-read-not-a-flat-book

_2026-09-21 17:20 UTC_

---

# Titan: the vpos 111 "POSITION GONE" alarm was a failed exchange read, not a flat book. The LONG side is not blocked. vpos 111 closed on its own trail at +2.82R. The two LONG losses are vpos 110 (stop hit) and a 7-second failsafe round trip caused by a database lock.

**2026-09-21 17:20 UTC · titan-bot HEAD `f16c271` · Titan LIVE, real money · forensic pass · 0 DB writes · 0 orders placed or cancelled · Mercury-SOL not touched**

`openitems_guard` was run first: **EXIT=0** (header and state table agree with runtime).

---

## 0. Summary, and the one decision that is yours

| question | answer |
|---|---|
| Is LONG blocked right now? | **NO.** 0 open LONG rows in the DB. BingX is flat on both probes with an empty error list, and has 0 open orders. The live cap check returns `(False, '0 LONG open of 1 cap')`. |
| Was the alarm true? | **NO.** Both alarms (06:20:16 and 08:15:36 UTC) fired one line after `[POS-UNKNOWN] … bingx {"code":109500,"msg":"The current system is busy"}`. The position stayed open at BingX until 10:28:59. |
| How did vpos 111 close? | **Titan's own trail.** Reduce-only MARKET SELL `2101982012063838208`, 0.0018 @ **84 392.8**, 10:28:59 UTC, fee 0.075954, realised +4.7941, net **+4.6367 = +2.816R**. The bot wrote the row itself at 10:29:00, and it matches BingX to the cent. |
| Orphan stop? | **None.** All three stops from this morning are `CANCELLED` with executedQty 0. Both probes show 0 open orders. |
| Row write needed? | **None.** The row was already closed correctly with the venue fill, so no `.bak` was needed and no UPDATE was run. |
| The "two LONG losses" | **vpos 110** (stop, −1.123R, −$1.62) and an **unrecorded failsafe round trip at 05:30** (−$0.19, 7 s, `database is locked`). vpos 111 was a **winner**. |
| Stop too tight? | For vpos 110, price went **0.30R (239.8 pts) past the stop**, bottomed 5 min after the fill, and was back at entry by 08:02. This does **not** match the ≥1.49R shape of earlier stop deaths. It is one trade (§4c). |
| `Bullish OB Created` | Did not fire vpos 110 or 111. For the failsafe fill, I **can't prove which of three names fired it**, and it isn't a market outcome anyway. The count stays at **4 live**. |
| Exit-advisor ledger | **Unchanged: 5 of 10 resolved, Σ +1.0497R.** Neither loss is an `ai_exit`. vpos 109 raises a population question (§5a). |
| Book gate | **42/200**: 15 dryrun + 27 armed (16 L / 11 S). **0 refusals.** |

> ### 🔴 YOUR DECISION: a proposed 6-line fix for the false alarm (§6). **Not applied.**
> `_reconcile_passive_fill` reads the position through a helper that treats a **failed read as flat**. That helper's own docstring says not to use it where "None" leads to an action. Since the 2026-09-12 restart there have been 2 failed reads during an open position, and **both** became a false "MANUAL ACTION REQUIRED". The fix only takes effect after a restart. Your brief says a required restart means "say so and STOP", so I stopped. Titan is flat right now, so a from-flat restart is possible whenever you choose.

---

## 1. Is the LONG side blocked right now?

### 1a. The `virtual_positions` row for vpos 111

| field | value |
|---|---|
| status | **closed** (written by Titan at 2026-09-21 10:29:00.146 UTC) |
| entry | 81 729.4, size 0.0018, lev 5, margin $30 |
| opened_at | 2026-09-21 05:35:16.753 UTC |
| original_sl_price | 80 814.6 (1R = 914.8 pts = $1.6466) |
| sl_price at close | 81 892.8588 (breakeven, armed 08:33:12) |
| stop_order_id (stored) | `2101952874489163776`, the breakeven stop. The alarm named `2101908097274064896`, the ATR stop it replaced at 08:33:12. |
| close_price / reason | **84 392.8 / trail** |
| total_fees / gross / net | 0.14951 / +4.79412 / **+4.636669** (funding 0.007941) |
| water_mark / max_adverse_price | 85 143.3 / 81 373.8 |

### 1b. BingX, both probes, read-only (no order endpoint was called)

First probe at **17:08:54 UTC**. It was repeated at **17:17:54 UTC** just before publishing, with the same result.

| probe | answered via | error list | result |
|---|---|---|---|
| `fetch_positions` (unified) | direct | **[]** | `[]`, no BTC position |
| raw `swapV2PrivateGetUserPositions` | direct | **[]** | `{"code":"0","data":[]}` |
| `fetch_open_orders` (unified) | direct | **[]** | `[]` |
| raw `swapV2PrivateGetTradeOpenOrders` | direct | **[]** | `{"orders":[]}` |

Every stop order from today, looked up by id (`swapV2PrivateGetTradeOrder`):

| order id | what | status | stop | created → updated (UTC) | executedQty |
|---|---|---|---|---|---|
| `2101906881789931520` | stop of the 05:30 failsafe entry | **CANCELLED** | 80 686.0 | 05:30:26.8 → 05:30:32.8 | 0 |
| `2101908097274064896` | vpos 111 ATR stop (the id in the alarm) | **CANCELLED** | 80 814.6 | 05:35:16.6 → **08:33:11.9** (breakeven move) | 0 |
| `2101952874489163776` | vpos 111 breakeven stop (stored id) | **CANCELLED** | 81 892.9 | 08:33:12.3 → **10:28:59.3** (cancelled before the trail close) | 0 |
| `2101845177601208320` (stored for vpos 110) | vpos 110 ATR stop | BingX returns it as `2101851680308162562`, **FILLED** | 81 069.8 | triggered 01:51:05 | 0.0018 @ 81 053.0 |

**No orphan stop and no conditional order exists on the symbol.** Nothing to cancel, so nothing was cancelled.

### 1c. LONG proposals refused by the position cap since the alarm

- **06:20:16 → 10:28:59** (row open AND position really open at BingX): **3 refusals**. `RISK HALT: position-cap halt: 1 LONG already open (cap=1)` at 08:25:15, 09:30:14, 09:30:14. **All three were correct**, because a real LONG was open. `VIRTUAL ENTRY BLOCKED: LONG` (the DB-side cap): **0**.
- **Since 10:28:59**: **0** cap refusals. The LONG proposals since then (14:40:04 / 14:40:05) were stopped by the HTF gate (`HTF_NEUTRAL_15M_WOULD_BLOCK … 1H_neutral_15m_not_confirming`), not by the cap.
- **Both cap inputs, evaluated live and read-only at 17:1x UTC:**
  - `risk_manager.concurrent_position_halt(exchange, 'BTC/USDT:USDT', 'LONG')` returned `(False, '0 LONG open of 1 cap')`.
  - `virtual_trader`'s cap reads `SELECT COUNT(*) … position_side='LONG' AND status='open'` and got **0**.
- **The next LONG proposal will not be refused by the cap.**

### 1d. Tor fallback

It was **not needed**. Every venue read, including 4 order lookups, all-orders, fills, position history and two income queries, answered on the direct path with an **empty error list**. The probe script had an isolated-circuit fallback (random SOCKS username per attempt on 127.0.0.1:9050, which was listening). It was never triggered. **No reading in this report was derived from an exception.**

---

## 2. How did the position actually close?

### 2a. BingX's own records (order history, fills, position history, income)

**All BTC-USDT orders since 2026-09-21 00:00 UTC**, as `swapV2PrivateGetTradeAllOrders` returned them:

| time (UTC) | order id | type | side | status | price | qty | realised | fee | reduceOnly |
|---|---|---|---|---|---|---|---|---|---|
| 01:25:14 | 2101845175261425664 | MARKET | BUY LONG | FILLED | 81 870.0 | 0.0018 | 0 | −0.073683 | no |
| 01:51:05 | 2101851680308162562 | STOP_MARKET | SELL LONG | FILLED | 81 053.0 (stop 81 069.8) | 0.0018 | −1.4706 | −0.072948 | yes |
| 05:30:26 | 2101906879651475456 | MARKET | BUY LONG | FILLED | 81 577.8 | 0.0018 | 0 | −0.073420 | no |
| 05:30:27 | 2101906881789931520 | STOP_MARKET | SELL LONG | CANCELLED | (stop 80 686.0) | 0 | 0 | 0 | yes |
| 05:30:32 | 2101906906608267264 | MARKET | SELL LONG | FILLED | 81 552.1 | 0.0018 | −0.0462 | −0.073397 | yes |
| 05:35:15 | 2101908094686818304 | MARKET | BUY LONG | FILLED | 81 729.4 | 0.0018 | 0 | −0.073556 | no |
| 05:35:17 | 2101908097274064896 | STOP_MARKET | SELL LONG | CANCELLED 08:33:12 | (stop 80 814.6) | 0 | 0 | 0 | yes |
| 08:33:12 | 2101952874489163776 | STOP_MARKET | SELL LONG | CANCELLED 10:28:59 | (stop 81 892.9) | 0 | 0 | 0 | yes |
| **10:28:59** | **2101982012063838208** | **MARKET** | **SELL LONG** | **FILLED** | **84 392.8** | **0.0018** | **+4.7941** | **−0.075954** | **yes** |

**Position history** (`swapV1PrivateGetTradePositionHistory`). Three LONG positions today, all fully closed:

| positionId | open → close (UTC) | avg open | avg close | realised | **net** | commission |
|---|---|---|---|---|---|---|
| 2101845175286591490 | 01:25:15 → 01:51:05 | 81 870.0 | 81 053.0 | −1.4706 | **−1.6172** | −0.14663 |
| 2101906879672446978 | 05:30:26 → 05:30:32 | 81 577.8 | 81 552.1 | −0.0463 | **−0.1931** | −0.14682 |
| 2101908094711984130 | 05:35:16 → 10:28:59 | 81 729.4 | 84 392.8 | +4.7941 | **+4.6367** | −0.14951 |

Income records agree: REALIZED_PNL +4.79412 / −0.04626 / −1.47060, and six TRADING_FEE lines matching the fees above. **No liquidation** (the `liquidatedPrice` field is empty on every fill).

**The vpos 111 closing fill:** order `2101982012063838208`, reduce-only MARKET SELL, **0.0018 @ 84 392.8, 2026-09-21 10:28:59 UTC, fee 0.075954 USDT**, realised +4.7941. The DB row has exactly these values: close 84 392.8, fees 0.14951 = 0.073556 + 0.075954, gross 4.79412, net 4.636669. BingX's own net figure is 4.6367.

### 2b. The mechanism

**Titan's own trail.** The `virtual_trader` poller saw price fall through the trail trigger (water mark 85 143.3 × (1 − 0.839 %) ≈ 84 429) and called `_do_close(reason='trail')`. That went through `order_adapter.market_close` → `main._execute_close_position`. It cancelled breakeven stop `…3776` (BingX updateTime 10:28:59.288), sent reduce-only MARKET SELL `…8208`, re-swept for orphans, and wrote the row.

- **Not** `ai_exit`: no exit consultation closed it. The only advisor event was the 08:30 `EXIT-ADVISOR-REFUSED` duplicate, which the consult lock refused.
- **Not** manual: no order in the history without a matching bot log line.
- **Not** a liquidation.
- **Not** BingX's stop filling under a different id: all three stops are CANCELLED with executedQty 0.

**The alarm's premise ("the position is gone") was false.** At 06:20:16 and 08:15:36 the position was open and stayed open for another 4h09m and 2h13m.

### 2c. The bot's own log at each alarm (journal, verbatim)

```
06:20:15.781 [TITAN] [POS-UNKNOWN] BTC/USDT:USDT LONG: position read FAILED (probe 1/1) — ExchangeError: bingx {"code":109500,"msg":"The current system is busy, please try again later","data":{}}
06:20:16.024 [TITAN] [VPOS-FILL] 🚨 vpos=111 BTC/USDT:USDT LONG: position GONE from the exchange but our stop 2101908097274064896 did NOT fill. NOT closing the row — exit price unknown. MANUAL ACTION REQUIRED.

08:15:36.128 [TITAN] [POS-UNKNOWN] BTC/USDT:USDT LONG: position read FAILED (probe 1/1) — ExchangeError: bingx {"code":109500,"msg":"The current system is busy, please try again later","data":{}}
08:15:36.385 [TITAN] [VPOS-FILL] 🚨 vpos=111 BTC/USDT:USDT LONG: position GONE from the exchange but our stop 2101908097274064896 did NOT fill. NOT closing the row — exit price unknown. MANUAL ACTION REQUIRED.
```

After each alarm the bot kept managing the position, which only makes sense if it was open:

```
08:30:07 [EXIT-ADVISOR-REFUSED] vpos=111 … an exit consultation is already in flight … REFUSED, not queued
08:33:12 VIRTUAL BREAKEVEN vpos=111 LONG SL→81892.86 (trail armed)
10:29:00 [STOP-CLEANUP] no orphaned orders for LONG BTC/USDT:USDT
10:29:01 VIRTUAL CLOSE vpos=111 LONG avg_entry=81729.4000 exit=84392.8 net_pnl=4.6367 reason=trail cycles=56/30
```

**What the bot sent and believed.** It sent nothing to the exchange at either alarm and changed nothing. It believed the position was gone because `_reconcile_passive_fill` (virtual_trader.py:1157) calls `main._fetch_open_position`. That helper (main.py:1276) maps `POS_UNKNOWN` to `None`, and its docstring says: *"THIS SHIM CONFLATES FLAT WITH READ-FAILED … DO NOT USE IT WHERE THE None BRANCH TAKES AN ACTION."* This caller's None branch sends a hands-required alert.

### 2d. Is this the 2026-09-09 race class? **No. It is the F1 class (2026-08-05).**

- **2026-09-09 (race):** the venue **really was flat** because the advisor's own close had filled. The fill poller read a **true** flat about a second before the close was written to the row.
- **2026-09-21 (this one):** the venue **was not flat.** The read **failed** (BingX 109500 "system busy"). The poller consumed the failure through the shim that turns "read failed" into "flat". This is F1, *"FLAT IS NOT THE SAME ANSWER AS THE READ FAILED"*, main.py:1190–1208, written 2026-08-05. The pattern is **a consumer that was never migrated**, not a race.
- **Frequency since the 2026-09-12 14:58 restart:** 2 `[POS-UNKNOWN]` reads, and **2 of 2** became a false `[VPOS-FILL] 🚨`. Every failed position read during an open position has produced a false hands-required alarm.
- **Why it matters beyond noise:** the alarm tells a human to take manual action on a position that is **live**. If you had "resolved" the row by hand, Titan would have stopped managing a live position, with no breakeven at 08:33 and no trail at 10:28.

**Same helper, other callers (class check, not fixed):** `breakeven_worker._fetch_open_position` has the same conflation.
- In `move_stop_with_race_guard` (breakeven_worker.py:425), a failed read after a failed cancel returns `'closed'`. That is benign in consequence: the caller persists nothing, **the old stop stays in place**, and it retries next tick.
- The job path at :765 is dormant (`breakeven_jobs` has 0 rows ever).
- main.py has 5 more read-only callers (1357, 3663, 3900, 4068, 4291). I did **not** audit them here.

---

## 3. Resolving the row

**3a/3b. No resolution needed.** The row was already closed, by Titan itself at 10:29:00.146 UTC, from the real venue fill:

| | DB row | BingX |
|---|---|---|
| exit price | 84 392.8 | 84 392.8 (order 2101982012063838208) |
| fees | 0.14951 | 0.073556 + 0.075954 = 0.14951 (position commission −0.14950998) |
| gross | +4.79412 | realised +4.7941 / income +4.79412 |
| net | +4.636669 | net +4.6367 |
| close_reason | `trail` | reduce-only MARKET at the trail trigger (§2b) |

**3c.** No write was made, so no `.bak` was taken and no UPDATE was run. I did not annotate the row. It is correct as it stands, and editing a correctly closed live-money row to record "evidence" would be a write with no purpose. The evidence is in this report. The LONG side is unblocked (§1c).

**3d.** No orphan stop. Open orders before: **0** (17:08:54). After: **0** (17:17:54). Nothing cancelled.

**What the alarm got right:** it did **not** invent an exit price and did not close the row. The fail-safe behaved correctly. Only its premise, "the position is gone", was wrong.

---

## 4. The two LONG losses

You reported "entered LONG twice and lost twice". BingX shows **three** LONG entries today:

- **vpos 110**: a real loss, stopped out.
- **The 05:30 entry**: a real-money round trip with **no `virtual_positions` row**, closed in 7 s by the entry failsafe after `database is locked`.
- **vpos 111**: a **winner**, +2.82R. The alarm was about this one.

So the two losses are **vpos 110** and **the failsafe round trip**.

### 4a. The table

| | **vpos 110** | **05:30 failsafe (no row)** | *vpos 111 (for reference, winner)* |
|---|---|---|---|
| entry | 81 870.0 @ 01:25:15 | 81 577.8 @ 05:30:26 | 81 729.4 @ 05:35:16 |
| original stop / 1R | 81 069.8 / 800.2 pts = $1.4403 | 80 686.0 / 891.8 pts = $1.6052 | 80 814.6 / 914.8 pts = $1.6466 |
| exit | **81 053.0** (stop fill, 16.8 pts of slippage) | **81 552.1** (failsafe market close) | 84 392.8 (trail) |
| R (net) | **−1.1228R** (gross −1.0210R) | **−0.1203R** (gross −0.0288R) | **+2.8159R** |
| $ net | **−1.6172** | **−0.1931** | +4.6367 |
| hold | 25 m 50 s | **7 s** | 4 h 53 m 43 s |
| close reason | `sl` (passive fill, reconciled correctly) | ENTRY FAILSAFE: `OperationalError: database is locked` at virtual_trader.py:987, **after** the fill | `trail` |
| MFE (stored water_mark) | **+0.0614R** (81 919.1). 1m candle high in life: +0.077R | ±0.03R (05:30 bar H 81 606.3 / L 81 549.2), not meaningful in 7 s | +3.73R (85 143.3); candle +3.88R at 09:38 |
| MAE | stored −0.840R (81 198.2; the sampler missed the stop minute). **At the stop fill: −1.021R.** Deepest after the stop: −1.300R | ±0.03R | −0.389R stored; candle −0.404R at 06:45 |
| trigger (5m name) | **`Bullish I-BOS`** (trades 34255) | **Not provable**: one of `Within Bullish OB` (34280), `Bullish OB Created` (34281), `Bullish I-CHOCH+` (34282). See 4d. | `Bullish OB Mitigated` (34283) |
| tiers | 1H `Trend Catcher Up` (LONG, 25m) · 15m **absent** · 5m `Bullish I-BOS` (w 0.7) | 1H `Trend Catcher Up` (4.5h) · 15m `HyperWave Signal Up`, **not counted, intra-conflict** 1.75/1.75 vs `HyperWave Signal Down` · 5m trigger | same as failsafe; 5m `Bullish OB Mitigated` (w 0.5) |
| score | **4.25** | 3.91 (row 34280; raw 5.00, adj −1.09 DXY-dominated) | 5.0 |
| trend_1d | bull | bull | bull |
| entry advisor | execute 0.82 | execute 0.82 (all three rows) | execute 0.82 |

### 4b. Did either ever print +0.25R?

- **vpos 110: NO.** MFE was +0.061R. The +0.25R level (82 070.05) never printed in its life.
- **Failsafe: no**, but it lived 7 seconds. Had it lived, it would never have touched its stop (80 686.0 was not printed all day) and would have printed +1R (82 469.6) at 08:32. It was the right trade, killed by a database lock.

**Updated live-book figures** (the 2026-09-16 15:20 base of 23 positions, vpos 86–108, plus 109, 110 and 111; stored water_mark method):

- live losers **17 → 18**, ΣR −9.8564 → **−10.9792**
- losers that never printed +0.25R: **11 → 12**, ΣR −7.5805 → **−8.7033 = 79.3 % of all live losses** (was 76.9 %)
- live ΣR over 26 positions: **−1.4814R** (was −5.1796 over 23; 109 +2.005R and 111 +2.816R are both winners)
- the failsafe round trip has no row and is in none of these counts, by design ("No row was written")

### 4c. Is the stop too tight? The overshoot number.

**vpos 110: price went 239.8 pts = 0.30R BEYOND the stop, then turned.**

- stop 81 069.8, filled 81 053.0 at 01:51:05
- deepest low **80 830.0 at 01:56**, five minutes after the fill. That is the minimum over the next 1 h, the next 4 h, and the whole path back to entry.
- total run against the entry: **1.30R**
- back at the entry price (81 870) at **08:02**; the 01:51–05:30 high was 81 621.6 (−0.31R)
- after that: 85 277.7 at 09:38. vpos 111 entered only 140.6 pts below vpos 110's entry and made +2.82R on the same move.

**Compared with the 2026-08-30 finding** (every real ATR-stop death ran ≥1.49R against): **vpos 110 does not match that pattern.** It ran 1.30R against in total, 0.30R past the stop. That is not "a hair" (the stop fill slipped 16.8 pts, 0.02R), but it is well short of the ≥0.49R past the stop that the earlier deaths showed. **It is the first real ATR-stop death under the 1.49R floor.** A stop 1.31R wide would have held this trade.

**What this does and does not say:**
- It is **one trade**. It does not overturn the book-level result you cited, that widening is monotonically worse (−19.49R).
- The same trade **also** never printed +0.25R, so it belongs in the entry-price class (§4b) as well.
- Both are true for vpos 110: the entry never went green, **and** the stop was taken 0.30R before a turn in the right direction.
- I am **not** recommending any stop change on one observation. It is logged as an exception to the ≥1.49R pattern, to be counted if more appear.

**The failsafe loss has nothing to do with the stop.** Its stop was never approached (±0.03R in 7 s). The cause was the database lock (§4e).

### 4d. `Bullish OB Created`

- **vpos 110 was fired by `Bullish I-BOS` and vpos 111 by `Bullish OB Mitigated`.** Neither was `Bullish OB Created`.
- **The failsafe fill cannot be attributed to a single name.** Three 5m signals (`Bullish I-CHOCH+` 05:30:09.82, `Bullish OB Created` 09.91, `Within Bullish OB` 09.96) each got `execute 0.82` from the entry advisor and entered `execute_entry` at the same time. One reached the fill; the other two raised `database is locked` at the pre-lock cap read (virtual_trader.py:731) and never placed an order.
  - Row 34280 (`Within Bullish OB`) is the only one whose failure write landed: status `failed`, error `database is locked`, advisor prompt stored.
  - Rows 34281 (`Bullish OB Created`) and 34282 (`Bullish I-CHOCH+`) lost their writes to the same lock and are still `pending`.
  - The failsafe path logs no row id, and stdout is block-buffered across threads, so log order does not prove which thread filled.
  - **I'm not claiming a name I can't prove.**
- **Watch count: stays at 4 live (0 winners), 13 across both books, 1 winner.** Even if `Bullish OB Created` owned the fill, a 7-second round trip closed by a database failsafe is not a market outcome of the entry. Had it lived, it would have been a winner (see 4b).

### 4e. What held the database lock at 05:30 (not identified)

- `trades.db` is in `journal_mode=delete` with Python's default 5 s busy timeout.
- **Lock errors since the 2026-09-12 restart:** 09-18 16:18–16:19 (2), 09-18 20:00–20:11 (5), **09-21 05:30 (13)**, 09-21 17:01 (1, before this session started).
- **Ruled out:**
  - no cron or timer touches `trades.db` or titan-bot at 05:30 (the titan crons run at 08:05–08:53 and Mondays at 08:11)
  - CPU was 84–90 % idle in the 05:30 and 05:40 sysstat samples on this 4-CPU box
- **Present at the time:** three concurrent webhook threads, the `virtual_trader` poller and `mfe_worker` were all writing (each logged `database is locked`), and ~30 unrelated cron jobs launched at 05:30:01.
- **The holder is not identified.** This is stated as open, not guessed.
- **The failsafe did exactly what it was built for:** it closed the position at market within 7 s, cancelled its stop, left no orphan, and wrote no invented row. Cost: −$0.19.

---

## 5. The ledgers

### 5a. `§0.EXIT-ADVISOR-RULE`: **unchanged, 5 of 10 resolved, Σ +1.0497R / +$1.72**

- Neither loss is an `ai_exit`: vpos 110 is `sl`, and the failsafe has no row. vpos 111 is `trail`.
- **No `ai_exit` close has happened since the 2026-09-16 15:20 ledger report.** The rule does not fire. `EXIT_ADVISOR_DRYRUN` stays **False**.

🔴 **A population question for you: vpos 109.**
- vpos 109 (LONG, closed 2026-09-18 23:45:13) was closed **by the advisor**: `[EXIT-ADVISOR-LIVE] trigger=armed_exit … close=True conf=0.72`, then `ARMED_EXIT_CLOSE`.
- But its row says `close_reason='external'`. By the rule's letter (`close_reason = 'ai_exit'`) it is **outside** the population, so I did not add it.
- Its counterfactual, computed by the canon method in case you rule it in:
  - BingX 1m candles, 3 974 in the live window, **0 gaps**, bardir order
  - the replay was first **validated against the published vpos 108 counterfactual and reproduced it to the digit (+1.5947R)**
  - result: counterfactual **trail 81 018.9 at 09-19 04:33, +2.1750R** vs advisor **+2.0051R**, so **Δ = −0.1699R (−$0.29)**
- **If armed-exit closes count, the ledger would be 6 of 10, Σ +0.8798R.** Still positive; the rule still does not fire. **Your ruling.**

### 5b. Book gate: **42 / 200**, 0 refusals

- **Method check:** it reproduces the canon's boundary count exactly (15 = 13 LONG / 2 SHORT before 2026-09-10 14:36:20).
- **Armed era:** 27 rows (16 LONG / 11 SHORT), **0 refusals**. No `book_gate_clause` values are set and there are 0 `[BOOK-GATE]` refuse lines.
- Today's rows: 34255 (vpos 110, pctl 59.1), 34280/34281/34282 (the 05:30 triplet, pctl 42.5; two stuck `pending`, see 4d), 34283 (vpos 111, pctl 15.0). All admitted.
- **Rate:** 2.43 rows/day in the armed era, so 158 remaining is about 65 days. **The 200-row review lands around late November 2026.**
- **The SHORT side's first armed-era rows arrived** (11), but none refused.

---

## 6. The proposed fix for the false alarm (NOT applied, needs a restart, your call)

This switches `_reconcile_passive_fill` from the shim to the three-state read that already exists in `main.py`. It uses the same double probe as the boot gate (unified + raw swapV2), re-reads once, and does nothing on UNKNOWN.

```diff
--- a/titan-bot/virtual_trader.py
+++ b/titan-bot/virtual_trader.py
@@ def _reconcile_passive_fill(exchange, row, send_tg):
     # Is the position still on the exchange?
     try:
         import main as _m
-        pos = _m._fetch_open_position(row['symbol'], row['position_side'])
+        # F1 (2026-08-05): a FAILED read is not FLAT. The shim conflates them;
+        # 2026-09-21 it turned two BingX 109500 "system busy" replies into two
+        # false "POSITION GONE … MANUAL ACTION REQUIRED" alarms on a live vpos.
+        _state, pos = _m._fetch_position_state(
+            row['symbol'], row['position_side'], double_probe=True, attempts=2)
     except Exception as e:
         # Cannot tell -> do NOT guess. Leaving the row open is recoverable;
         # inventing a close is not.
         print(f"[VPOS-FILL] position check failed vpos={row['id']}: {e}", flush=True)
         return False
-    if pos is not None:
+    if _state == _m.POS_UNKNOWN:
+        print(f"[VPOS-FILL] vpos={row['id']}: position read UNKNOWN — not "
+              f"treated as flat, nothing done, re-checked next tick", flush=True)
+        return False
+    if _state == _m.POS_OPEN:
         return False                       # still open, nothing to reconcile
```

- **Behaviour change:** only on a failed read. A true flat still reaches `read_filled_protective_order` and the alarm exactly as today.
- **Cost:** at most one extra 2 s re-probe, and only when a read fails.
- **To make it live:** it needs a contract test (a failing unified read + raw read must give no alarm; a true flat must still give one), then apply from flat and restart.
- **Titan is flat now.** Per your brief I stopped at "a restart is required".

---

## 7. Confirmations

| check | state |
|---|---|
| writes | **0 DB writes, 0 code edits, 0 config edits.** Nothing was written in `/root/titan-bot`; `git status` clean. |
| `.bak` | not needed: nothing was written |
| orders | **0 placed, 0 cancelled.** Venue calls were read-only: positions ×2, open orders ×2, order by id ×4, all orders, fills, position history, income ×2, public 1m candles |
| NRestarts | **0, unchanged.** MainPID 1572470, active since 2026-09-12 14:58:32 UTC |
| `EXIT_ADVISOR_DRYRUN` | **False** (runtime `import config`) |
| `BOOK_GATE_DRYRUN` | **False** (`CLAUSE_A` True, `CLAUSE_B` False) |
| `LIVE_TRADING_ENABLED` / `ORDER_ADAPTER_LIVE` | True / True |
| Mercury-SOL | **not touched**: not read, not probed, not restarted |
| `openitems_guard` | EXIT=0 at start |

**Open items this report leaves:**
1. The §6 fix: your decision, needs a restart.
2. The vpos 109 population question (§5a): your ruling.
3. The database-lock holder at 05:30 (§4e): not identified.
4. Rows 34281/34282 stuck `pending`: cosmetic, lost to the lock.
5. The failsafe round trip is invisible to every `virtual_positions` ledger (−$0.19): recorded here only.
