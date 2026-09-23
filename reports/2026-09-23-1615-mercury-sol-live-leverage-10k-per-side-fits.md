# mercury-sol-live-leverage-10k-per-side-fits

_2026-09-23 16:15 UTC_

---

# $10,000 PER SIDE NOW FITS — **LIVE-ONLY LEVERAGE PREPARED, APPLIED FROM FLAT, LOADED. SIZE UNCHANGED: $100 BOTH SIDES, 5×**

**2026-09-23 16:15 UTC · Mercury-SOL · APPLIED · Titan untouched · COHORT BOUNDARY 2026-09-23 16:07:32 UTC**

`openitems_guard` → **exit 0** before and **exit 0** after (titan-bot HEAD `f53d048`).

---

## 🔴 RESULT

**The target now fits.** Both sides at **$1,000 × 10 = $10,000** lock **$1,998** of margin and leave **$2,096
free**, which is **6.2 widest stop-outs**. At $2,000 × 5 the same notional left **$97.94**. The sequence that
broke 5× now passes: after one widest stop-out the next entry clears the pre-check with **$2,756** available against a
$989 need, and after two in a row, with **$2,407**.

**Nothing moved today:** `LIVE_LEVERAGE = 5`, margins 20/20. Everything below is proven behaviour-identical at that
setting.

| proof at 5× / $20 / $20 | result |
|---|---|
| qty, every cent $30–$400 × both sides, real Bybit market spec | **74,002 of 74,002 identical** |
| `set_leverage` call | identical: `set_leverage(5, 'SOL/USDT:USDT')`, same int. Warn line **byte-identical** on today's normal 110043 answer |
| balance pre-check initial margin, need and decision | **21,144 of 21,144 identical** |
| daily $ floor, all 47 live-era days | floor **is** 5% on 11 of 11 loss days, **0** decision differences |
| open card | **byte-identical** (`⚙️ x5  💵 $20 margin · $94.26 notional`) |
| resolver bad cases | **23 of 23** fall back to `LEVERAGE` |
| `set_leverage` confirm outcomes | **9 of 9** |
| AST walker | **11 of 11** statuses registered AND called |
| orders placed / cancelled | **0 / 0** |
| restarts | **1**, from flat, 16:07:30.010 |

🔴 **THE HONEST LINE.** Leverage does **not** change the loss on a stop that **fills**. That loss is notional ×
stop distance plus fees: **$178 median, $350 widest at $10,000, at 5× or at 10× alike.** What leverage changes is
only how much margin is locked. **The risk it does not remove is a stop that does NOT fill.** The account is on
**cross margin**, so an unfilled stop exposes the **whole balance**, at any leverage. At 10× the account balance,
not the $1,000 margin, is what stands behind each position.

**Two things the brief did not have:**
1. **At the target, the worst day before a brake stops new entries is 4 full stop-outs, not 3.** Two losses leave
   every brake silent (≈ −2.1R, ≤ $699, below the $990 floor, not yet a 3-loss streak). Both sides can then open
   and both can stop. At the widest stop that is **$1,398 = 34.0% of equity**; at the median, $713 = 17.3%. The
   brakes gate **entries**, not open positions, so the 25% ceiling does not cap this.
2. **Every live entry already "fails" `set_leverage`.** The venue answers **110043 "leverage not modified"**
   because 5× is already set, and today's code logs a warning and sends the order regardless. It would also have
   sent the order after *any* failure, at whatever leverage the venue held. That is fixed below, and at today's
   size the 110043 path is identical.

---

## 1. THE LIVE-ONLY LEVERAGE

**a)** `config.py` gains `LIVE_LEVERAGE = 5`, `LIVE_LEVERAGE_CAP = 11` and `live_leverage()`, shaped like
`live_fixed_margin()`. A valid value comes back **as the same object**, so at 5 every expression downstream is the
same int. **Every bad case falls back to `LEVERAGE` (5), proven by execution, 23 of 23:**
* `LIVE_LEVERAGE`: missing, None, `'10'` (quoted), `'abc'`, True, False, 0, −5, 0.5 (below 1), NaN, inf,
  **12 (above the cap)**, **101 (above the venue max)**, 1e6, list, dict, complex, `Decimal(10)`
* `LIVE_LEVERAGE_CAP`: None, `'11'`, NaN, 0, True (with `LIVE_LEVERAGE = 10`)

Valid values: 10 → 10, 11 → 11, 1 → 1, 7.5 → 7.5 (the venue step is 0.01). With cap 200 and `LIVE_LEVERAGE = 150`
the result is 5: the venue maximum of 100 still binds.

**b) The cap, derived.** Isolated liquidation for a LONG sits at ≈ entry × (1 − 1/L + MMR), with MMR 0.5% on
tier 281. So the distance is **1/L − 0.5%**. Require that distance ≥ **2.5 × the widest live stop** (3.30%, #40):

> 1/L ≥ 2.5 × 0.033 + 0.005 = 0.0875 → L ≤ 11.43 → **`LIVE_LEVERAGE_CAP = 11`**

**Why 2.5×:** live stop widths already span 3.5× (0.94% → 3.30%). With a 2.5× buffer, ATR would have to widen to
2.5× the widest stop ever set before an isolated liquidation could come before the stop.

| leverage | liquidation distance | vs the widest stop 3.30% |
|---|---|---|
| 5× | 19.5% | 5.91× |
| **10×** | **9.5%** | **2.88× — fits** |
| 11× (cap) | 8.59% | 2.60× |

**c) Every live-path consumer, switched.** This list comes from a grep of `LEVERAGE` over all `.py` files in the
bot plus the SOL scripts; no external script reads it.

| consumer | before | after |
|---|---|---|
| sizing, `_execute_single_entry` | `live_fixed_margin(side) * LEVERAGE` | `_lev = live_leverage()` **resolved once**, then `* _lev` |
| `set_leverage` | `ex.set_leverage(LEVERAGE, symbol)`, failure ignored | `_confirm_live_leverage(symbol, side, _lev)`, refuse if unconfirmed (1d) |
| balance pre-check initial margin | `notional / LEVERAGE` | `notional / leverage`, with the **same `_lev`** passed in |
| daily $ floor 1R_ref | `live_fixed_margin_max() * LEVERAGE * 0.033` | `… * live_leverage() * 0.033` |
| open card | `⚙️ x{LEVERAGE}` | `⚙️ x{_card_lev}`: `LEVERAGE` if virtual, else `live_leverage()` |
| stored `leverage`, `book_live_position` INSERT | `LEVERAGE` | `live_leverage()` |
| adoption dict, `_adopt_derive` | `LEVERAGE` | `live_leverage()` |
| **paper** `virtual_trader.py:230` sizing, `:381` stored | `LEVERAGE` | **unchanged** |

**d) `set_leverage` on Bybit hedge mode.** ccxt 4.5.52's `bybit.set_leverage(L, symbol)` sends
**`POST /v5/position/set-leverage`** with `{category: linear, symbol: SOLUSDT, buyLeverage: "L", sellLeverage:
"L"}`. The venue docs say that in hedge mode with **cross** margin "buyLeverage must be the same as sellLeverage".
**So one call sets one live leverage for both sides**, and the venue reads confirm it: idx 1 `leverage=5`, idx 2
`leverage=5`, `tradeMode 0` (cross).

**If `set_leverage` fails:**
* **retCode 0** → confirmed.
* **110043 "leverage not modified"** → confirmed: the venue is saying it already *is* L. This is **today's normal
  path**; the retained journal holds one such warn (2026-09-21, entry #49).
* **Any other error** → a GET of `/v5/position/list`. The entry is confirmed only if **this side's positionIdx**
  reads `leverage == L`.
* **Otherwise** → `EntryLeverageUnconfirmed`, raised **before the order**. It gets its own status
  `leverage_unconfirmed` (registered and called) and a ⚙️ card: "No order was sent: it would not have gone out at
  the Lx the balance check assumed."

**The order can no longer go out at a leverage different from the one the pre-check used.**
Execution, 9 of 9: set OK ✅; 110043 ✅; other error + venue 5 ✅; other error + venue 10 ❌ refused; read raises ❌;
read retCode≠0 ❌; no idx row ❌; unparseable ❌; SHORT reading idx 2 only ✅.
**The only behaviour difference at today's size:** a non-110043 failure **and** a failed confirming read now
refuses, where it used to proceed. There are 0 occurrences in the retained journal.

**e) Leverage change with a position open.** The B. API docs **do not state** the effect. What is on record:
* ccxt's own source warns that it "WILL INCREASE LIQUIDATION PRICE FOR OPEN ISOLATED LONG POSITIONS AND DECREASE …
  FOR OPEN ISOLATED SHORT"
* the venue's error list includes **110044 "Available margin is insufficient"**, **110012 "Insufficient available
  balance"** and **110013 "Cannot set leverage due to risk limit level"**, which are the refusals a change can
  meet when it would re-margin an open position

I did **not** test it: that would be a venue write. Leverage is **per symbol, and one value for both sides** in cross
hedge mode, so a change always touches both sides. **The canon procedure now forbids changing it with any position
open (step 1).**

---

## 2. PROVEN AT TODAY'S SIZE

**a)** Every row in the RESULT table was executed:
* **qty:** old `LIVE_FIXED_MARGIN*LEVERAGE` against new `live_fixed_margin(side)*live_leverage()`, both through
  `stop_loss.quantise_amount` with Bybit's live SOLUSDT spec (lot 0.1, min 0.1, minNotional 5) → **0 mismatches in
  74,002**. @117.82 both give **0.8 SOL**.
* **`set_leverage`:** the call recorded is `('set_leverage', 5, 'int', 'SOL/USDT:USDT')`, identical to the old call.
  The warn line on 110043 is byte-identical to the old one.
* **pre-check:** 21,144 amount × price points, with initial margin, need and decision equal to the old formula.
* **floor:** all 47 live-era days replayed against the venue's USDT cash-balance history → floor **is**
  `DAILY_LOSS_PCT_LIMIT` on 11 of 11, 0 differences.
* **card:** before == after, live and paper.

**b) AST: exactly what changed.**

| file | pre → post sha256 | AST |
|---|---|---|
| `config.py` | `ccf11e8d` → `87fcc0ab` | constants 149 → 151, **ADDED `LIVE_LEVERAGE`, `LIVE_LEVERAGE_CAP`**, CHANGED 0, REMOVED 0. Defs ADDED `live_leverage`. **0 lines deleted** |
| `main.py` | `5586d104` → `1b4d434c` | ADDED `EntryLeverageUnconfirmed`, `_confirm_live_leverage`. CHANGED `_balance_precheck`, `_daily_loss_floor_pct`, `_execute_single_entry`, `_handle_5m_trigger` (the `__init__` listing is a name collision between two classes; `EntryFailSafeError` and `EntryBalanceRefused` are unchanged). Import +`live_leverage`. **12 lines deleted, each an intended replacement** (diff below) |
| `virtual_trader.py` | `7fea781c` → `7b0f0bba` | CHANGED `book_live_position`, `_adopt_derive` (one token each). Import +`live_leverage` |
| `skip_attribution.py` | `3fda23c6` → `baad7354` | `TRACKED_STATUSES` +`leverage_unconfirmed` |
| `claude_advisor.py` | `52feade7` | **unchanged** |

**From the LOADED bytecode.** `.pyc` compiled 15:58:58; the headers match the source; the process started 16:07:32.
* **New:** `LIVE_LEVERAGE` 5, `LIVE_LEVERAGE_CAP` 11, `live_leverage()` → **5**.
* **Untouched:**
  * `LIVE_FIXED_MARGIN` 20; `_LONG` 20; `_SHORT` 20; `live_fixed_margin(LONG/SHORT/None)` → 20 / 20 / 20
  * `LEVERAGE` 5; `PAPER_FIXED_MARGIN` 2000
  * `SL_BUFFER_ATR` 2.5; `TRAIL_MULT_ATR` 1.875; `TRAIL_ARM_R` 0.75; `CONFLUENCE_SCORE_THRESHOLD` 2.0
  * `FLAT_ADX_GATE_DRYRUN` **True**; `BOOK_GATE_ENABLED/DRYRUN` **True/False**
  * `BULL_DAILY_SHORT_BLOCK` **True/False**; `BEAR_DAILY_LONG_BLOCK` **True/False**
  * `EXIT_ADVISOR_DRYRUN` True; `MAX_POSITIONS_PER_SIDE` 1
  * `DAILY_LOSS_R_LIMIT` 3.0; `DAILY_LOSS_PCT_LIMIT` 0.05; `DAILY_LOSS_STOP_PCT_REF` 0.033;
    `DAILY_LOSS_PCT_CEILING` 0.25
  * `BALANCE_PRECHECK_ENABLED` True; `BALANCE_PRECHECK_SLACK` 0.02; `LOSS_STREAK_THRESHOLD` 3

**All seven advisor system prompts are sha256-identical:** `_ENTRY_SYSTEM` `cc70ed45…`, `_ENTRY_SYSTEM_V2`
`894a6c20…`, `_ENTRY_SYSTEM_V2_ALIGNED` `f221365f…`, `_ENTRY_SYSTEM_V2_ALIGNED_SHORT` `e1487999…`, `_CLOSE_SYSTEM`
`37bcdce4…`, `_CLOSE_STATE_SYSTEM` `3be10726…`, `_LEARNING_SYSTEM` `aa35142e…`.

---

## 3. 🔴 THE TARGET, COMPUTED — both sides $1,000 × 10

**a) Balance, read now** over an isolated circuit (`79b97a28…`, attempt 1, 0 failed attempts; the first try hit a
CloudFront 403 on another exit and was retried on a fresh circuit): **`totalAvailableBalance` $4,114.38**.
Representative entry: #50's fill **117.82** → qty **84.8 SOL** (lot 0.1) = **$9,991.14** per side.

| | 5× ($2,000 × 5) | **10× ($1,000 × 10)** |
|---|---|---|
| initial margin per side | $1,998.23 | **$999.11** |
| open fee per side | $9.99 | $9.99 |
| **locked with both sides open** | $3,996.45 | **$1,998.23** |
| **free with both sides open** | **$97.94** | **$2,096.17** |
| free covers stop-outs: median / p90 / widest | 0.6 / 0.3 / 0.3 | **12.5 / 6.5 / 6.2** |
| pre-check refuses below | $1,968.05 | $988.92 |

**b) 🔴 The sequence that broke 5×.** Both sides are open, then one side stops at the **widest** distance (−$338.97
including the close fee), and the same side re-enters.

| step | 5×, other side unrealised 0 | **10×, other side unrealised 0** | **10×, other side at −1.0R unrealised (worst)** |
|---|---|---|---|
| both open | $97.94 | $2,096.17 | $2,096.17 |
| stop #1 → available | $1,757.20 → **next entry REFUSED** | **$2,756.31 → PASSES** | **$2,427.00 → PASSES** |
| re-enter | — | $1,747.21 | $1,417.90 |
| stop #2 → available | — | **$2,407.35 → PASSES** | **$2,078.04 → PASSES** |
| re-enter | — | $1,398.24 | $1,068.94 |

At 10×, each widest stop plus re-entry costs ≈ $349 of availability. The pre-check would first refuse after the
**7th** consecutive widest stop-out. The R brake stops new entries at the 3rd.

**c) Liquidation vs the stop**, on #50's entry 117.82 with stop 114.79 = 2.5 × ATR(1h) 1.2105, 2.57% below:

| margin mode | liquidation | distance | vs this stop (2.57%) | vs the widest stop (3.30%) |
|---|---|---|---|---|
| isolated 5× | 94.85 | 19.5% | 7.58× | 5.91× |
| **isolated 10×** | **106.63** | **9.5%** | **3.69×** | **2.88×** |
| isolated 11× (cap) | 107.70 | 8.59% | 3.34× | 2.60× |
| **cross, as the account actually is**, LONG $9,991 alone, equity $4,114 | ≈ 69.89 | 40.7% | **15.8×** | 12.3× |
| cross, **both sides open** (hedged, equal qty) | — | — | net price exposure ≈ 0: no price-driven liquidation while both are open | |

On cross, the liquidation price is set by account equity against maintenance margin (MMR 0.5% of notional), **not
by the leverage setting**. It is the same at 5× and 10×.

**d) Brakes at this size, both sides.** 1R_ref = $10,000 × 3.3% = $330, so the **$ floor is $990 (24.1%)**. The
R brake fires at ΣR ≤ −3.0.
* **Loss-only, one side at a time:** the R brake fires at stop-out **#3** on every live stop width. The $ floor
  fires at #3 (widest; clause 1 is checked first) to #9 (narrowest). This is the same as the 15:50 case B.
* **Worst day before any brake stops trading: 4 full stop-outs.** Two losses keep every brake silent: ≈ −2.1R,
  ≤ $699, below 3 losses. Both sides can then open and both stop.
  **Widest: $1,398 = 34.0% of equity. p90: $1,326 = 32.2%. Median: $713 = 17.3%.** The brakes gate entries only;
  they do not close positions, so this passes the 25% ceiling.

**e) 🔴 THE HONEST LINE.** Leverage **does not change the loss on a stop that fills**. At $10,000 it is $178 median
and $350 widest, at 5× or 10×. The risk leverage **does not remove** is a stop that **does not fill**: a gap, a
venue outage, an exchange-side cancel. **On cross margin the whole balance is then exposed, at any leverage.** 10×
only changes how much of that balance is formally locked, not how much can be lost.

---

## 4. APPLIED FROM FLAT

**a) Flat, read twice.** First at 15:57:41, then again inside the restart script (venue 16:03:40, DB one second
before the restart):
* 0 open `virtual_positions`, 0 `active_positions`, 0 `exit_pending`
* Bybit idx 1 / idx 2 size **0 / 0**; open and conditional orders **0 / 0**
* the error list **EMPTY**; each read ran on its own random-SOCKS circuit

**b)** `.bak` copies were taken first: `config.py`, `main.py`, `virtual_trader.py`, `skip_attribution.py` and
`OPEN-ITEMS-SOL.md` → `*.bak_liveleverage_20260923`, sha256 = pre-patch.
**One restart**, from flat, issued **16:07:30.010 UTC**, mid 5-minute window:
```
16:07:32 systemd: Started mercury-sol.service
16:07:49 [SMART-CLEANUP] No open positions for SOL/USDT:USDT — proceeding with orphan cleanup
16:07:50 [AP] No active positions in DB — clean boot.
16:07:50 [BOOT] taker fee: 0.001 (0.1000%) source=venue
16:07:51 [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
16:07:51 [BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 222243]
16:07:55 [HEARTBEAT] alive ticks=1 cadence=10s open=0 mode=LIVE pid=222243
```
PID 218734 → **222221** (worker **222243**), `NRestarts=0`.
Venue after (16:08:12): sizes 0/0, orders 0/0, errors `[]`, position `updatedTime` unchanged on both indices.
`openitems_guard` after: **EXIT=0**. **Canon:** new `§LIVE-LEVERAGE-2026-09-23`, **COHORT BOUNDARY 2026-09-23
16:07:32 UTC**.

---

## 5. 🔴 THE THREE-NUMBER RAISE (rewritten in canon §SIZE-READY; supersedes the 15:42 procedure)

**`LIVE_FIXED_MARGIN_LONG = 1000` · `LIVE_FIXED_MARGIN_SHORT = 1000` · `LIVE_LEVERAGE = 10`**, plain numbers, no
quotes.
1. **Flat check** (as in §4a). 🔴 **Never change leverage with a position open.**
2. **Balance ≥ $2,020** plus the stop-out room you want. Today that leaves $2,094 free, which is 6.0 widest
   stop-outs.
3. `.bak`, then edit `LIVE_LEVERAGE = 10` (cap 11), then `LIVE_FIXED_MARGIN_LONG = 1000`, then
   `LIVE_FIXED_MARGIN_SHORT = 1000`. Do not touch `LEVERAGE`, `LIVE_FIXED_MARGIN` or `PAPER_FIXED_MARGIN`.
4. `python3 -m py_compile config.py`.
5. **One** restart, from flat, mid-window.
6. **Verify:**
   * the boot line and heartbeat
   * **from the loaded bytecode:** `live_fixed_margin('LONG') == 1000`, `('SHORT') == 1000`,
     `live_leverage() == 10`
   * `openitems_guard` EXIT=0
   * after the **first entry**, GET `/v5/position/list` shows **`leverage "10"` on BOTH idx 1 and idx 2**
   * the first card reads **`⚙️ x10  💵 $1000 margin · $~10,000 notional`**
   * a `leverage_unconfirmed` ⚙️ card means nothing was sent
7. Record a cohort boundary.

| margin/side × leverage | notional/side | stop-out median / p90 / widest | margin locked, both sides | free after both open | widest stop-outs covered | daily $ floor |
|---|---|---|---|---|---|---|
| $20 × 5 (today) | $100 | $1.78 / $3.32 / $3.50 | $40 | $4,074.18 | 1,165 | $205.72 (5.0%) |
| $100 × 5 | $500 | $8.91 / $16.58 / $17.48 | $200 | $3,913.38 | 224 | $205.72 (5.0%) |
| $200 × 5 | $1,000 | $17.82 / $33.15 / $34.96 | $400 | $3,712.38 | 106 | $205.72 (5.0%) |
| $500 × 5 | $2,500 | $44.55 / $82.88 / $87.40 | $1,000 | $3,109.38 | 35.6 | $247.50 (6.0%) |
| $500 × 10 | $5,000 | $89.10 / $165.75 / $174.80 | $1,000 | $3,104.38 | 17.8 | $495.00 (12.0%) |
| $1,000 × 5 | $5,000 | $89.10 / $165.75 / $174.80 | $2,000 | $2,104.38 | 12.0 | $495.00 (12.0%) |
| **$1,000 × 10 ← TARGET** | **$10,000** | **$178.20 / $331.50 / $349.60** | **$2,000** | **$2,094.38** | **6.0** | **$990.00 (24.1%)** |
| $2,000 × 5 (does NOT fit) | $10,000 | $178.20 / $331.50 / $349.60 | $4,000 | $94.38 | 0.3 | $990.00 (24.1%) |

---

## 6. CONFIRMATION

| | |
|---|---|
| every write stated before it ran | ✅ `.bak` ×5 → config → main (13 edits) → virtual_trader (3) → skip_attribution (1) → restart → canon (procedure rewritten + new section) → this report |
| `.bak` taken | ✅ `*.bak_liveleverage_20260923` ×5 |
| orders placed / cancelled | **0 / 0**. **`set_leverage` was NOT called by me** (it is a venue write). All venue access was GET: `position/list`, `order/realtime`, `wallet-balance`, `market/risk-limit`, `market/instruments-info`, public `load_markets` |
| restarts | **exactly 1**, from flat, 16:07:30.010 UTC |
| size | **unchanged: $20 × 5 = $100 both sides.** The venue leverage is still 5 on both indices |
| Titan | **UNTOUCHED**. Only `tools/openitems_guard.py` (read-only) was run: EXIT 0 before, EXIT 0 after |

### The patch (unified diff against `*.bak_liveleverage_20260923`)

```diff
--- a/config.py
+++ b/config.py
@@ -78,6 +78,48 @@
     return raw
 
 
+# ── 🔴 LIVE-ONLY LEVERAGE (2026-09-23) — the third number of the raise ──────
+# LEVERAGE (below) stays the PAPER book's value and the fallback. The live path —
+# sizing, set_leverage, the balance pre-check, the daily $ floor, the card, the
+# stored leverage column, adoption — reads live_leverage(). Leverage does NOT
+# change the loss on a stop that fills (that is notional × stop distance); it only
+# changes how much margin a position locks.
+# CAP, DERIVED: isolated liquidation sits ≈ (1/L − MMR) from entry; MMR 0.5% on
+# SOLUSDT tier 281. Require that distance ≥ 2.5 × the WIDEST live stop (3.30%, #40):
+#   1/L ≥ 2.5 × 0.033 + 0.005 = 0.0875  →  L ≤ 11.43  →  CAP = 11.
+# 2.5× because live stop widths already span 3.5× (0.94% → 3.30%): ATR would have to
+# widen to 2.5× the widest stop ever set before an isolated liquidation could come
+# before the stop. At 10×: 9.5% vs 3.30% = 2.88×. At 11×: 8.59% = 2.60×. The
+# account is CROSS, whose liquidation is far wider (an account property); isolated
+# is the conservative reference. Venue maximum on this tier is 100×.
+LIVE_LEVERAGE     = 5
+LIVE_LEVERAGE_CAP = 11
+
+
+def live_leverage():
+    """Live leverage. 🔴 FAIL-SAFE DIRECTION, same shape as live_fixed_margin(): a
+    missing, None, non-numeric (incl. bool and quoted strings), zero, negative,
+    non-finite, below-1 or above-cap value returns LEVERAGE — never a larger number.
+    The cap is min(LIVE_LEVERAGE_CAP, venue maximum 100); a broken cap also falls
+    back. A valid value is returned AS IS (same object), so at 5 every downstream
+    expression is byte-for-byte what it was with LEVERAGE."""
+    import math, numbers
+    raw = globals().get('LIVE_LEVERAGE')
+    cap = globals().get('LIVE_LEVERAGE_CAP')
+    try:
+        if isinstance(cap, bool) or not isinstance(cap, numbers.Real) \
+                or not math.isfinite(cap) or cap < 1:
+            return LEVERAGE
+        cap = min(cap, 100)
+        if isinstance(raw, bool) or not isinstance(raw, numbers.Real):
+            return LEVERAGE
+        if not (math.isfinite(raw) and 1 <= raw <= cap):
+            return LEVERAGE
+    except Exception:
+        return LEVERAGE
+    return raw
+
+
 def live_fixed_margin_max():
     """The larger of the two resolved per-side margins — the LARGEST size the
     config can hold, which is what the daily $ floor must sit behind."""
--- a/main.py
+++ b/main.py
@@ -1174,6 +1174,7 @@
     active_fixed_margin,      # 2026-08-05: mode-resolved, for DISPLAY/storage
     live_fixed_margin,        # 🔴 2026-09-23: per-side live margin (the size knob), fail-safe to LIVE_FIXED_MARGIN
     live_fixed_margin_max,    # 🔴 2026-09-23: the larger side — what the daily $ floor sits behind
+    live_leverage,            # 🔴 2026-09-23: LIVE-only leverage (paper keeps LEVERAGE), fail-safe to LEVERAGE
     DAILY_LOSS_STOP_PCT_REF,  # 🔴 2026-09-23: size-aware $ floor — widest live stop on record
     DAILY_LOSS_PCT_CEILING,   # 🔴 2026-09-23: size-aware $ floor — hard % ceiling
     BALANCE_PRECHECK_ENABLED, # 🔴 2026-09-23: clean refusal instead of a venue exception
@@ -1881,7 +1882,7 @@
     """Effective clause-2 floor as a fraction of equity. NEVER raises.
 
     min( max(DAILY_LOSS_PCT_LIMIT, DAILY_LOSS_R_LIMIT × 1R_ref / equity), CEILING )
-    1R_ref = max(largest configured side × LEVERAGE × DAILY_LOSS_STOP_PCT_REF,
+    1R_ref = max(largest configured side × live_leverage() × DAILY_LOSS_STOP_PCT_REF,
                  largest initial_risk_usdt closed today).
     Derivation and the proof that it sits behind the R brake: config.py, beside
     DAILY_LOSS_STOP_PCT_REF. When the size term is at or below the base, this
@@ -1891,7 +1892,7 @@
     import math
     base = DAILY_LOSS_PCT_LIMIT
     try:
-        ref_1r = live_fixed_margin_max() * LEVERAGE * DAILY_LOSS_STOP_PCT_REF
+        ref_1r = live_fixed_margin_max() * live_leverage() * DAILY_LOSS_STOP_PCT_REF
         try:
             _today = float(max_risk_today)
             if math.isfinite(_today) and _today > ref_1r:
@@ -2724,10 +2725,65 @@
         self.detail = detail
 
 
-def _balance_precheck(amount, price):
+class EntryLeverageUnconfirmed(RuntimeError):
+    """🔴 2026-09-23. set_leverage could not be confirmed at the leverage the balance
+    pre-check assumed. Raised BEFORE the order — nothing was sent. The handler
+    records status='leverage_unconfirmed', calls the skip-attribution hook and
+    sends a card."""
+
+    def __init__(self, message, *, leverage):
+        super().__init__(message)
+        self.leverage = leverage
+
+
+def _confirm_live_leverage(symbol, position_side, lev):
+    """(confirmed, why). NEVER raises.
+
+    ccxt bybit.set_leverage sends POST /v5/position/set-leverage with
+    buyLeverage == sellLeverage == str(lev) (hedge mode on CROSS margin requires them
+    equal), so one call sets BOTH sides. Outcomes:
+      • retCode 0                          → confirmed
+      • retCode 110043 "not modified"      → confirmed: the venue says it already IS lev
+      • any other error                    → read /v5/position/list for THIS side's
+        positionIdx; confirmed only if its `leverage` equals lev. A failed read or a
+        different value → NOT confirmed, and the caller refuses the entry.
+    The warn line is printed exactly as before for every exception."""
+    try:
+        tor_retry.with_socks_retry(exchange, lambda ex: ex.set_leverage(lev, symbol),
+                                   label='set_leverage')
+        return True, 'set (retCode 0)'
+    except Exception as e:
+        print(f"{LOG_PREFIX}set_leverage warn: {e}", flush=True)
+        if '110043' in str(e):
+            return True, 'venue 110043: already at this leverage'
+        _set_err = f'{type(e).__name__}: {str(e)[:120]}'
+    try:
+        _mid = exchange.market(symbol)['id']
+        r = tor_retry.with_socks_retry(
+            exchange, lambda ex: ex.private_get_v5_position_list(
+                {'category': 'linear', 'symbol': _mid}),
+            label='positions.leverage_confirm')
+        if str(r.get('retCode')) != '0':
+            return False, f'set failed ({_set_err}); read retCode={r.get("retCode")}'
+        _idx = '1' if position_side == 'LONG' else '2'
+        row = next((p for p in (r.get('result') or {}).get('list') or []
+                    if str(p.get('positionIdx')) == _idx), None)
+        if row is None:
+            return False, f'set failed ({_set_err}); venue has no positionIdx {_idx} row'
+        venue_lev = float(row.get('leverage'))
+        if venue_lev == float(lev):
+            print(f"{LOG_PREFIX}[LEVERAGE] set failed but venue reads {venue_lev:g}x "
+                  f"== {lev}x on idx {_idx} — confirmed", flush=True)
+            return True, f'venue reads {venue_lev:g}x'
+        return False, f'set failed ({_set_err}); venue reads {venue_lev:g}x, need {lev}x'
+    except Exception as e2:
+        return False, f'set failed ({_set_err}); leverage read failed ({type(e2).__name__})'
+
+
+def _balance_precheck(amount, price, leverage=None):
     """(ok, detail). ok=False ONLY when a READ available balance is below the need.
 
-    need = qty×price/LEVERAGE + qty×price×taker (open fee). Refuse only if
+    need = qty×price/leverage + qty×price×taker (open fee). Refuse only if
     available < need × (1 − BALANCE_PRECHECK_SLACK). Bybit's own order cost adds the
     CLOSE fee on top, so this is strictly more lenient than the venue. 🔴 Every
     failure — arithmetic, the balance read, a missing/unparseable/non-finite field,
@@ -2740,7 +2796,9 @@
         return True, detail
     try:
         notional = float(amount) * float(price)
-        im = notional / LEVERAGE
+        # 🔴 the SAME leverage the order will be sent at (resolved once by the
+        # caller); None → the live resolver.
+        im = notional / (leverage if leverage is not None else live_leverage())
         try:
             taker = float(fee_rates.taker_rate(exchange, DEFAULT_SYMBOL))
             if not (math.isfinite(taker) and taker >= 0):
@@ -3121,7 +3179,10 @@
     # 🔴 2026-09-23: per side. live_fixed_margin() falls back to LIVE_FIXED_MARGIN on
     # any bad per-side value, never to a larger number. At 20/20 this is the same
     # object as before, so notional_usdt is the same int (100).
-    notional_usdt = live_fixed_margin(position_side) * LEVERAGE
+    # 🔴 2026-09-23: ONE live leverage, resolved ONCE per entry. The same value sizes
+    # the order, feeds the pre-check, and is what set_leverage must confirm.
+    _lev = live_leverage()
+    notional_usdt = live_fixed_margin(position_side) * _lev
     # Phase 1 (3): round DOWN to the venue lot step and validate min qty/notional.
     # `price` is the ticker we already hold — no extra network call.
     amount, _qerr = quantise_amount(exchange, symbol, notional_usdt / current_price,
@@ -3135,17 +3196,21 @@
     # 🔴 2026-09-23 — BALANCE PRE-CHECK. Raises EntryBalanceRefused (its own status,
     # its own card) only when the venue would have refused anyway; an unreadable
     # balance ADMITS. Before any order-side call, so nothing has been sent.
-    _bal_ok, _bal = _balance_precheck(amount, current_price)
+    _bal_ok, _bal = _balance_precheck(amount, current_price, _lev)
     if not _bal_ok:
         raise EntryBalanceRefused(
             f"balance pre-check: need ${_bal['need']:.2f} (IM ${_bal['im']:.2f} + "
             f"open fee ${_bal['fee']:.2f}) > available ${_bal['available']:.2f}",
             detail=_bal)
 
-    try:
-        tor_retry.with_socks_retry(exchange, lambda ex: ex.set_leverage(LEVERAGE, symbol), label='set_leverage')
-    except Exception as e:
-        print(f"{LOG_PREFIX}set_leverage warn: {e}", flush=True)
+    # 🔴 2026-09-23 — the order may NOT go out at a leverage other than the one the
+    # pre-check assumed. Confirmed = set OK, or venue 110043 "not modified" (already
+    # equal — the NORMAL answer at an unchanged leverage), or a venue read of this
+    # side's positionIdx showing it. Anything else refuses BEFORE the order.
+    _lev_ok, _lev_why = _confirm_live_leverage(symbol, position_side, _lev)
+    if not _lev_ok:
+        raise EntryLeverageUnconfirmed(
+            f"leverage {_lev}x not confirmed on the venue: {_lev_why}", leverage=_lev)
 
     pos_idx = 1 if position_side == 'LONG' else 2
     # Phase 1 (2): THE duplication risk. A blind 403-retry of this call places a
@@ -5673,6 +5738,32 @@
                   f"row={row_id}: {e}", flush=True)
             return jsonify({'status': e.status, 'naked': e.naked,
                             'message': str(e), 'combo': combo}), 500
+        except EntryLeverageUnconfirmed as e:
+            # 🔴 2026-09-23 — NOTHING was sent: raised before the order. Registered in
+            # skip_attribution.TRACKED_STATUSES and the hook is CALLED here.
+            update_trade(row_id, status='leverage_unconfirmed', error=str(e), combo_key=combo,
+                         confluence_score=direction_score,
+                         matrix_direction=matrix_result['direction'],
+                         matrix_breakdown_json=matrix_bkdn_json)
+            _record_skip_attribution(row_id, symbol, direction, 'leverage_unconfirmed',
+                                     matrix_result=matrix_result,
+                                     confluence_score=direction_score,
+                                     pre_trade_walls=locals().get('_pre_walls'),
+                                     ai_reason=str(e),
+                                     srv_adx_1h=_adv_snap.get('srv_adx_1h'),
+                                     trend_4h=_adv_snap.get('trend_4h'),
+                                     trend_1d=_adv_snap.get('trend_1d'))
+            send_tg(
+                f"⚙️ <b>LEVERAGE NOT CONFIRMED — {position_side} REFUSED</b>\n"
+                f"💎 {symbol}\n"
+                f"<i>{str(e)[:300]}</i>\n"
+                f"<i>No order was sent: it would not have gone out at the {e.leverage}x "
+                f"the balance check assumed.</i>\n"
+                f"<code>{combo}</code>"
+            )
+            print(f"{LOG_PREFIX}[LEVERAGE] REFUSED {position_side} row={row_id}: {e}", flush=True)
+            return jsonify({'status': 'leverage_unconfirmed', 'direction': direction,
+                            'reason': str(e), 'combo': combo}), 200
         except EntryBalanceRefused as e:
             # 🔴 2026-09-23 — a clean refusal where the venue would have refused
             # anyway. NOTHING was sent (raised before set_leverage / the order).
@@ -5808,6 +5899,7 @@
         # executed. A failed multiply drops the notional, never invents one.
         _card_margin = (active_fixed_margin() if entry.get('_virtual')
                         else live_fixed_margin(position_side))
+        _card_lev = LEVERAGE if entry.get('_virtual') else live_leverage()
         try:
             _card_notional = f" · ${float(entry['amount']) * float(entry['fill_price']):,.2f} notional"
         except Exception:
@@ -5816,7 +5908,7 @@
             f"{_open_hdr}\n"
             f"💎 {symbol}  @ {entry['fill_price']}\n"
             f"{_macro_blk}"
-            f"📦 {entry['amount']}  ⚙️ x{LEVERAGE}  💵 ${_card_margin} margin{_card_notional}\n"
+            f"📦 {entry['amount']}  ⚙️ x{_card_lev}  💵 ${_card_margin} margin{_card_notional}\n"
             f"📈 ATR({ATR_LEN},{ATR_TF}): {entry['atr']:.4f}\n"
             f"🛡 SL {sl_tag} {entry['sl_price']}   🎯 TRAIL {tp_tag} {entry['trail_pct']}%  (arms @ {entry['active_price']})\n"
             f"{indicators.ema_trend_line(_snap)}\n"
--- a/virtual_trader.py
+++ b/virtual_trader.py
@@ -41,6 +41,7 @@
     OBSERVATION_MODE,                # PHASE 2: stamps is_paper provenance on new rows
     PAPER_FIXED_MARGIN, LIVE_FIXED_MARGIN,   # 2026-08-05: split by book
     live_fixed_margin,   # 🔴 2026-09-23: the stored margin_usdt is the ACTUAL side's margin
+    live_leverage,       # 🔴 2026-09-23: the stored leverage is the LIVE leverage
     LEVERAGE, ATR_LEN, ATR_TF, SL_WALL_ANCHOR_ENABLED,
     TRAIL_MULT_ATR,   # BYBIT_TAKER_FEE_RATE deliberately NOT imported: accounting
                       # asks fee_rates.taker_rate() (2026-08-08). The constant is
@@ -2573,7 +2574,7 @@
                 " entry_atr_pct_1h, recheck_status, "
                 " is_paper) "
                 "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,'open',?,?,?,?,?,?,?,?,?,?,0)",
-                (symbol, position_side, side, live_fixed_margin(position_side), amount, LEVERAGE,
+                (symbol, position_side, side, live_fixed_margin(position_side), amount, live_leverage(),
                  fill_price, atr, sl_price, trail_pct, json.dumps(mgmt_state),
                  json.dumps(fills), fill_price, opened_at, trades_row_id,
                  initial_risk_usdt, sl_price, fill_price,
@@ -2761,7 +2762,7 @@
         'breakeven_price': be_px,
         'partial_fraction': PARTIAL_AT_ARM_FRACTION,
         'partial_size_raw': size * PARTIAL_AT_ARM_FRACTION,
-        'margin_usdt': live_fixed_margin(position_side), 'leverage': LEVERAGE,
+        'margin_usdt': live_fixed_margin(position_side), 'leverage': live_leverage(),
         'water_mark': fill, 'max_adverse_price': fill,
         'mgmt_state': {'breakeven_applied': False},
         'recheck_status': 'done',
--- a/skip_attribution.py
+++ b/skip_attribution.py
@@ -78,7 +78,9 @@
 TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked', 'risk_halt',
                     'book_blocked', 'flat_adx_blocked', 'bull_daily_blocked',
                     'entry_gate_refused', 'bear_daily_blocked',
-                    'balance_refused')
+                    'balance_refused', 'leverage_unconfirmed')
+# 🔴 'leverage_unconfirmed' added 2026-09-23 WITH the live-leverage confirm, same
+# pass, registered here AND called at the refusal site in main.py (AST walker).
 # 🔴 'balance_refused' added 2026-09-23 WITH the balance pre-check, same pass,
 # registered here AND called at the refusal site in main.py (AST walker).
 
```
