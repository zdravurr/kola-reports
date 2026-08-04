# MERCURY-SOL — PRE-FLIP ACCOUNT CHECK: **DO NOT FLIP YET**

**2026-08-05 01:20 UTC** · **READ-ONLY — nothing was changed, nothing flipped.**
Only GET endpoints were used against Bybit. **Titan untouched.**

> ## 🔴 THREE BLOCKERS. The flip as specified would not do what it says.
> 1. **In LIVE, no `virtual_positions` row is ever created** — so the position manager has nothing
>    to manage. No +1R partial, no breakeven, no close accounting, and **the daily-loss brake can
>    never see a live loss.** `is_paper=0` is unreachable code.
> 2. **One shared `MARGIN_USDT`** sizes both books. Setting it to 20 changes the **paper** size too,
>    which the standing instruction forbids.
> 3. **Venue leverage is 10, not 5** — the Titan finding, reproduced exactly. Plus: **the API key
>    expires in 8 days (2026-08-13).**

---

# §1 — ACCOUNT STATE (read-only)

| check | result |
|---|---|
| USDT free / total | **811.90 / 811.90** — $20 margin covered **~40×**. Comfortable. |
| account | UNIFIED (`uta=1`), totalEquity **1311.53**, totalAvailableBalance **1273.44** |
| open position SOLUSDT | **NONE** — `size=0` on positionIdx 1 (LONG) and 2 (SHORT) |
| leftover orders | **0 regular · 0 stop/conditional · 0 tpsl** — clean, no orphans |
| stopLoss / takeProfit / trailingStop fields | all empty / `0` on both sides |
| **leverage** | 🔴 **10** on both sides — **must be 5** |
| margin mode | `tradeMode=0` = **CROSS** (riskId 281, autoAddMargin 0) |

## 🔴 The leverage finding — the same one Titan had

The bot **does** call `set_leverage(LEVERAGE, symbol)` at `main.py:1919` before each entry, so on the
happy path it self-corrects to 5. **But it is wrapped and non-fatal:**

```python
try:
    tor_retry.with_socks_retry(exchange, lambda ex: ex.set_leverage(LEVERAGE, symbol), ...)
except Exception as e:
    print(f"{LOG_PREFIX}set_leverage warn: {e}", flush=True)   # ← warn only, order proceeds
```

A 403 on that one call at that one moment and the entry places **at 10×**.

**Honest magnitude:** the bot sends an explicit `amount`, so the **notional stays $96 either way**.
Leverage changes the margin consumed ($9.6 vs $19.2) and the liquidation distance — and at $96
notional against $811 free, liquidation is unreachable in both cases. So this is **not** a
blow-up risk. It is a *stated configuration that is not true at the venue*, and it should be set to 5
by hand so the first live order does not depend on a Tor-fragile call succeeding.

## 🔴 The API key expires 2026-08-13T18:32:09Z — in **8 days**

Going live on a credential with an 8-day life means the bot stops being able to trade — or manage an
open position — mid-flight, next week. That is exactly a "first live order fails for a stupid reason"
item, one week deferred.

---

# §2 — INSTRUMENT LIMITS AND THE EXACT LOT SIZES

Read from the venue (`/v5/market/instruments-info`), not from memory:

| field | value |
|---|---|
| `minOrderQty` | **0.1** |
| `qtyStep` | **0.1** |
| `minNotionalValue` | **5** |
| `tickSize` | **0.010** |
| `maxOrderQty` | 96000 · leverage 1–100, step 0.01 · status `Trading` |

**At the live price 73.84**, computed through the bot's own `quantise_amount`:

| | LIVE ($100 notional) | PAPER ($10,000) |
|---|---|---|
| raw size | 1.354280 | 135.427952 |
| **quantised entry** | **1.3 SOL** = **$95.99** | 135.4 SOL = $9,997.94 |
| step error | **−4.008 %** | −0.021 % |
| raw ⅓ leg | 0.433333 | 45.133333 |
| **quantised partial** | **0.4 SOL** = **$29.54** | 45.1 SOL = $3,330.18 |
| **realised fraction** | **0.307692** (not ⅓) | 0.333087 |
| remainder | 0.9 SOL = $66.46 | 90.3 SOL = $6,667.75 |
| min-notional $5 | entry ✅ partial ✅ remainder ✅ | ✅ ✅ ✅ |

**The Phase-1 quantisation handles it correctly.** It rounds **down** (`amount_to_precision`), refuses
outright if the leg falls under `minOrderQty` or `minNotionalValue` — in which case the caller must
not send an order — and the partial's accounting follows the **realised** fraction
(`_frac = qty / size`), not the intended third, so `net_pnl` still reconstitutes the whole position.

🔶 **What to accept going in:** at $100 the lot step is $7.38 — **7.7 % of the position**. So the
entry is 4.0 % smaller than intended and the "third" is really **30.8 %**. The geometry survives but
becomes grainy; 0.4 and 0.5 are the only choices and neither is a third. This is a property of the
size, not a defect.

---

# §3 — 🔴 THE SIZE SPLIT DOES NOT EXIST

**SOL has ONE shared constant.** `config.py:32` — and its own comment already says so:

```python
MARGIN_USDT = 2000   # PAPER/virtual sizing while OBSERVATION_MODE=1 → $10,000 notional per trade.
                     # NOTE: this SAME constant sizes REAL orders once un-paused (OBSERVATION_MODE=0).
```

Both paths read it: `main.py:1907` (live) and `virtual_trader.py:190` (paper).

**Consequence: setting `MARGIN_USDT = 20` for the live flip also resizes the paper book to $100** —
destroying comparability with its own 21-position history at $10,000 notional, which the standing
instruction forbids. **The split is a prerequisite of this flip, not an optional tidy-up.**

**What it would take** (the paths are cleanly separated by mode, so this is small and safe):

| # | file / line | change |
|---|---|---|
| 1 | `config.py:32` | `PAPER_FIXED_MARGIN = 2000` · `LIVE_FIXED_MARGIN = 20` + `active_fixed_margin()` resolving on `OBSERVATION_MODE` |
| 2 | `main.py:1907` | `notional_usdt = LIVE_FIXED_MARGIN * LEVERAGE` (live path only) |
| 3 | `virtual_trader.py:190` | `notional_usdt = PAPER_FIXED_MARGIN * LEVERAGE` (paper path only) |
| 4 | `virtual_trader.py:329` | the `margin_usdt` column must store the margin **actually used** |
| 5 | `main.py:3396` | the entry card prints `${MARGIN_USDT}` — must print the active one |
| 6 | `main.py:832` | import list |

The separation is clean: `_execute_single_entry` branches `if OBSERVATION_MODE: → virtual_trader.execute_entry`
and otherwise falls through to the live order path, so each sizing line serves exactly one mode.

---

# §4 — 🔴 THE BLOCKER: A LIVE POSITION IS NEVER BOOKED

**Determined by exhaustive search, not inference:**

1. There is exactly **one** `INSERT INTO virtual_positions` in the whole tree — `virtual_trader.py:318`,
   inside `execute_entry`.
2. `execute_entry` has exactly **one** caller — `main.py:1891`, inside `if OBSERVATION_MODE:`.
3. Therefore the provenance stamp `1 if OBSERVATION_MODE else 0` (`virtual_trader.py:337`) **always
   evaluates to 1**. 🔴 **`is_paper=0` is unreachable code.**
4. Empirically: **21 of 21** rows in `virtual_positions` are `is_paper=1`. Zero live rows exist, and
   none can be created.
5. The live path (`main.py:1870-2056`) places the order, places the stop, places the trail, returns a
   dict — and its caller updates the **`trades`** row to `status='executed'`. **No position row.**
6. The Phase-2 engine — "the single position manager in BOTH modes" — iterates
   `SELECT * FROM virtual_positions WHERE status='open'` (`virtual_trader.py:558`).

**So on the first live trade the engine has nothing to manage.** What the position *would* still have:
the **on-exchange stop-loss** and the **Bybit-native trailing stop**, both placed at entry. What it
would silently **not** have:

- ❌ the +1R **partial** (the ⅓ leg computed above never fires)
- ❌ the **breakeven arm**
- ❌ engine-side trail recompute, excursion sampling, the recheck tiers
- ❌ **close accounting** — no `net_pnl` row is ever written for a live trade
- ❌ 🔴 **the daily-loss brake.** It sums `virtual_positions.net_pnl` for closed rows today
  (`main.py:1383`). With no live rows it reads **$0 forever and never halts**, on real money.

The live branch that exists for exactly this (`virtual_trader.py:1322`, `if not _is_paper(row)` →
external-close detection, POS_UNKNOWN discipline, `_book_exchange_close`) is **unreachable** until a
live row can be created.

**This is the item that must be closed before the flip.** It does not make the entry *fail* — it makes
the management *absent*, which is worse, because it looks like success.

---

# §5 — API KEY

| | |
|---|---|
| `readOnly` | **0** → **read-write. Trading is permitted.** |
| permissions | `ContractTrade: [Order, Position]`, `Derivatives: [DerivativesTrade]`, `Spot`, `Options` |
| **determinable without an order?** | **Yes** — `/v5/user/query-api` answers directly. No order was placed. |
| note / userID | `AI Mercury` / 424848927 |
| 🔴 **expiredAt** | **2026-08-13T18:32:09Z — 8 days** |
| IP allowlist | 🔶 `['*']` — **none** |
| 🔶 Wallet perms | `AccountTransfer`, `SubMemberTransfer` — **this trading key can move funds** |

**Shared with Titan? NO — and the question dissolves:** Titan has **no Bybit key at all** (it trades
BingX); SOL has no BingX key. Compared by SHA-256 of the values, never printed. So the shared-key
exposure the 2026-06-07 rotation request worried about **does not exist between these two bots**.
What does exist is the 8-day expiry, and a trading key with **no IP restriction and transfer rights** —
worth rotating on both counts, but that is a separate decision from this flip.

---

# §6 — TOR

**Last 48 h: 1,360 SOCKS isolation retries (~28/h). Every single one resolved on attempt 1 → `ok`.
Zero exhaustions, zero give-ups.**

| label | retries |
|---|---|
| `ticker.observatory` | 1,345 |
| `ohlcv.signal_*` | 11 |
| `positions.riskcheck` | 2 |
| `ticker.spread` / `tape.trades` | 1 / 1 |

98.9 % of the churn is the read-only observatory poller. **No order-write has ever gone through Tor on
this bot** — it has never placed one.

**What a mid-order Tor failure does under the Phase-1 semantics:**

- **Order writes are idempotent.** `with_socks_retry_write` hands the **same** `clientOrderId` to every
  attempt (`sol-e-<row_id>` / `sol-sl-<row_id>`). Previously ccxt minted a fresh `orderLinkId` per
  retry, so Bybit's duplicate rejection never engaged and a 403 *after* the order reached the matching
  engine placed a **second** order — double size. That is closed.
- **A landed-but-unseen first attempt raises `DuplicateSuppressed`** → **no second order**, `status='failed'`,
  and a Telegram alert saying plainly that a position may be open and unstopped and needs a human look.
- **`POS_UNKNOWN` is never destructive.** `_fetch_position_state` returns UNKNOWN on a failed read, and
  the close path **raises rather than returning None** (`main.py:2106`) — because every caller reads
  `None` as "no position" and would record a successful no-op close. Nothing is cancelled, no order is
  sent, the position stays registered and stopped.
- The engine **does nothing** on UNKNOWN (`virtual_trader.py:1322`), and `_book_exchange_close` refuses
  to book a close it cannot substantiate, leaving the row open for the next tick.
- **Unreadable entry fill** → refuses to book a fabricated position, alerts, and leaves it to boot
  reconciliation.

Tor is healthy and the write semantics are sound. ⚠️ Note only that **all of it is untested against a
real order**, since SOL has never placed one.

---

# §7 — THE FLIP SEQUENCE I WOULD RUN (not run — for your reading)

**Prerequisites (must be done first, or the flip does not mean what it says):**

- **P1.** Close §4 — make the live path create a `virtual_positions` row with `is_paper=0`, so the
  engine manages the live position and the daily-loss brake can see it. *This is code, and it needs
  its own diff, review and a paper-mode regression check first.*
- **P2.** Split the margin constant per §3 (paper stays 2000).
- **P3.** Set SOLUSDT leverage to **5** on both position indices, by hand, and re-read it back.
- **P4.** Decide the API key: 8 days of life is not enough to go live on.

**Then, and only then:**

| # | step | detail |
|---|---|---|
| 1 | snapshot | `.bak` on every file touched (no VCS on SOL) |
| 2 | flat check | 0 open positions, 0 pending exits, 0 conditional orders |
| 3 | `.env` | `MERCURY_OBSERVATION_MODE=1` → **`0`** — the single line that flips the mode |
| 4 | **restart REQUIRED** | `OBSERVATION_MODE` is read at import (`config.py:12`), and the branch at `main.py:1885` is evaluated per entry from that import. A restart is the only way it takes effect — and it must be taken **from flat**, because a paper position open across the flip would keep being managed as paper (`is_paper` is per-position provenance, deliberately) |
| 5 | verify at runtime | `load_dotenv` **first**, then `config.OBSERVATION_MODE is False`; ×20 ceiling 20.0; `NEWS_OBSERVATION_PINNED` True; geometry unchanged; venue leverage reads 5 |
| 6 | first-trade watch | §8 below |

**⚠️ The verification in step 5 must load `.env` first.** A bare `import config` reads
`MERCURY_OBSERVATION_MODE` from the process environment, where it does not exist, and returns the
default `'0'` → `False`. It will tell you the bot is LIVE when it is not. I hit exactly this earlier
tonight.

**The banner should read** — and should be derived at runtime, never copied forward:

```
🔴 MERCURY-SOL IS LIVE — REAL MONEY ON BYBIT.
MERCURY_OBSERVATION_MODE=0 in .env, verified at runtime <UTC ts>.
LIVE_FIXED_MARGIN 20 × LEVERAGE 5 = $100 notional  (entry 1.3 SOL, partial 0.4 SOL at the 0.1 step)
PAPER_FIXED_MARGIN 2000 unchanged — the paper book stays at $10,000 notional and stays comparable.
Venue leverage verified 5 on positionIdx 1 and 2. Bybit reached read-write through Tor.
Positions opened before this line are is_paper=1 and stay managed as paper.
```

---

# §8 — WHAT TO WATCH ON THE FIRST LIVE TRADE, IN ORDER

| # | moment | healthy | failure, and what it looks like |
|---|---|---|---|
| 1 | **sizing** | `[QTY] entry.live … → 1.3` and a card reading `📦 1.3 ⚙️ x5 💵 $20 margin` | `[QTY] entry ABORTED — size not tradable` + `🚫 Entry aborted`. **Also check the card says x5 and $20** — if it says $2000 the split (§3) did not land |
| 2 | **leverage** | silent | `set_leverage warn: …` in the log — **the entry still proceeds, at whatever the venue holds.** Cross-check the position's `leverage` field after the fill |
| 3 | **entry order** | fill booked from the venue, not from intent | `🚨 ENTRY DUPLICATE SUPPRESSED` (first attempt landed; **no** second order — check the position by hand) · `🚨 ENTRY FILL UNREADABLE` (**a position may be open and unstopped**) · `⚠️ Partial entry fill` (booked at the filled size; 1R, breakeven and the partial all follow it) |
| 4 | **stop placement** | `sl_id` present, `sl_tag ✓` | 3 failed attempts → `🚨 SL FAILED 3×` → **emergency market close**. This is the one failure that closes the position on purpose |
| 5 | **trail** | `tp_tag ✓` | `⚠️ Trailing stop NOT set` — **deliberately not an emergency close.** The stop is the protection, the trail is the improvement; no action needed for safety |
| 6 | 🔴 **the position row** | a `virtual_positions` row appears with **`is_paper=0`** | **Until §4 is fixed, no row appears at all.** Symptom: the trade shows `status='executed'` in `trades`, the position is live on Bybit, and the engine logs nothing about it. Ever. |
| 7 | **+1R partial** | `[PARTIAL] … qty 0.4` and the remainder rides at 0.9 | `[PARTIAL] SKIPPED — leg … not tradable` (rides the full trail, contract unchanged) · `SKIPPED — live adapter reduced nothing`. **With §4 open this never fires at all — silence here is not success** |
| 8 | **stop fires** | engine sees FLAT, books the close from the real fill, `net_pnl` written | with §4 open: the stop fires on Bybit, money moves, **and nothing is booked** — the daily-loss brake still reads $0 |
| 9 | **Tor mid-position** | `[SOCKS_RETRY] retried … → ok` (~28/h is normal) | `[ENGINE] position state UNKNOWN — no action this tick` = correct and non-destructive. What must **never** appear: a close recorded while state was UNKNOWN |
| 10 | **daily brake** | halts after the configured daily loss | with §4 open it can never trigger on live money |

**The first live trade should be watched to its close before a second is allowed** — the partial and
the close-booking (rows 7 and 8) are the two that have never executed once on this bot.

---

# 📌 ONE LINE, AS ASKED — the stray files in `kola-reports`

The `fault-prom-promise-…` files come from the **OpenClaw workspace**, not from either bot:
`lib/fault_realert.py` escalates an unresolved promise via `notify.notify_boss(...)`, and
`notify.notify_boss` **auto-publishes every alert into `kola-reports/reports/`** (`report_publish.publish(text, topic=task)`)
purely to mint a raw link — committed by `kola-reports publisher <reports@kola.local>`; yes, it can be
routed out, either by giving `publish()` a subdirectory for operational alerts or by skipping
publication for `fault_*` topics, which are short alerts that do not need a raw file at all.
**Not fixed in this pass, as instructed.**

---

# WHAT I DID NOT DO

- **Did not flip.** Nothing was changed: no file edited, no order placed, no leverage set, no restart.
- Only GET endpoints were called against Bybit; API keys were compared by hash and never printed.
- Titan was not touched.
