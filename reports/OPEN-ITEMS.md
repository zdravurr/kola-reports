# TITAN — OPEN ITEMS

**Read this before touching Titan.** Written to be actionable by a session with **no memory** of
2026-07-26/27. Every entry states what is known, what is **not** known, and what would close it.

# 🔴🔴 TITAN IS **LIVE**. REAL MONEY. 🔴🔴

**Both mode flags are UP and orders ARE sent to BingX.** `LIVE_TRADING_ENABLED = True` **and**
`ORDER_ADAPTER_LIVE = True`, verified at runtime 2026-07-30 03:15 UTC. HEAD **`957f980`**.

🔴 **THE LIVE WINDOW IS NOT CONTINUOUS FROM 19:14 — do not state it as one line.** There was a
27-minute revert to paper in between, and a session with no memory must not miss it:

| # | UTC | commit | event |
|---|---|---|---|
| 1 | 2026-07-29 **19:13:33** | `cb3a8bb` | first flip to LIVE |
| 2 | 2026-07-29 **21:26:52** | `11055e2` | **REVERT TO PAPER** — naked-position defect in the shared entry path |
| 3 | 2026-07-29 **21:54:16** | `4ce8664` | **LIVE again, both flags True** — continuously live since this moment |

```
LIVE_FIXED_MARGIN_USDT = 30.0  x  LEVERAGE 5  =  $150 notional  (~0.0023 BTC)
```

🔴 **THE P&L BOUNDARY. This matters for EVERY future analysis, so do not blur it:**

| period | mode | where the numbers come from |
|---|---|---|
| everything up to **2026-07-29 19:13:33** | **PAPER** | simulated fills, `$10,000` notional (`PAPER_FIXED_MARGIN_USDT = 2000 x 5`) |
| **19:13:33 → 21:26:52** | REAL MONEY (first window) | see the naked-short caveat below |
| **21:26:52 → 21:54:16** | PAPER (revert) | flags down while the entry-path defect was fixed |
| from **2026-07-29 21:54:16** onward | **REAL MONEY** | real fills, real fees read back from BingX, `$150` notional |

Both live in the SAME `virtual_positions` table — the engine owns the position in both modes
(one engine, two adapters). **They are NOT poolable.** Pooling them would mix a $10,000 book with a
$150 one.

**USE `stop_order_id IS NOT NULL` AS THE SPLIT, NOT `opened_at`.** Live rows carry a real exchange
stop id; paper rows never do. It is exact, it needs no timestamp arithmetic, and — unlike a time
cut — it is not confused by the paper interlude above. As of 2026-07-30 03:15 UTC it yields exactly
one live row:

```
vpos 80-85  stop_order_id NULL  -> PAPER   (last paper close: vpos 85 LONG -137.32, 16:42:36)
vpos 86     stop_order_id 2082629881359347712  -> LIVE, OPEN, the FIRST real-money position
```

🔴 **CAVEAT — real P&L is NOT fully captured by `virtual_positions`.** During the first live window
a **naked short was opened with no DB row at all** (the 2026-07-29 defect) and was closed manually
at **−$0.26**. That is real money and it has **no `virtual_positions` row**, so summing the table
understates realised live P&L by that amount. Any live-P&L total must add it back by hand.

The trail is deliberately still owned by the poller in live — see the ⚡ section below.

_Last updated: **2026-08-03 16:10 UTC** — HEAD **`6d9281d`**. §2.44 opened and CLOSED — the "matrix TTL expired" label was rendered 77 times and was WRONG on 70 (91%, they were intra-conflict); now four strings for four states, the reason CAPTURED into `entry_tiers_json`, close prompt byte-identical, gate arithmetic untouched. Includes a correction to the 16:05 report (the 7 are genuine TTL expiries, so 70 wrong / 7 right — not 77 / 0). **§2.45 opened as a CLOSED QUESTION: THE LOSING ENTRIES ARE NOT IDENTIFIABLE IN ADVANCE ON THIS DATA — ten branches named and all negative; only live-era observations would change it, ~30 live entries ≈ three weeks.**
Earlier the same day: HEAD **`489e0ac`**. §2.43 opened and CLOSED — the legacy fall-through now REFUSES to enter (alert + log + status stamp, no order); **the close half is untouched deliberately** (refusing a close could strand a position); proven **structurally** (`_execute_entry` has no call site left in `webhook()`), **not** behaviourally — a live probe was stopped earlier by the HTF cascade and state was not manipulated to force it. Prompts byte-identical, window untouched.
Earlier the same day: HEAD **`34dbdbf`**. §2.42 opened and CLOSED — the book sources moved to OKX-4000 for storage, learning and the recheck; new columns `advisor_book_json`, `entry_okx_wall_baseline_mult`, `entry_book_src`, `recheck_events.book_src`, NULL on all legacy rows, not backfilled; both prompts byte-identical (md5), **window NOT reset**. Includes the non-advisor entry-path finding (0 of 65 positions; one entry ever, 2026-05-11, predating the engine; unreachable by today's alerts but legacy-not-dead). **§2.42a opened — the POST-WINDOW LIST as one coupled block: ①§1d fallback both halves · ②§3 entry-reference drift · ③§2.40/§2.41 thresholds+re-grade · ④retire `entry_wall_baseline_mult` WITH ①.**
Earlier the same day: HEAD **`a85733f`**. §2.40e opened and CLOSED — the entry
prompt's combo weight now carries its **provenance** (evaluation count · date of the most recent ·
the POSITION SIZE they were taken at, as a ratio); the verdict wording *"<1 = historical loser"* is
gone, **the number is kept**, and no minimum-n or staleness rule was invented. Freeze checked and
argued: §2.4-OP freezes the CLOSE prompt and is explicit the entry side is not frozen; no diff line
touches a close-side symbol. §2.40f opened — 🔴 **the ±20/−15 thresholds and §2.41's re-grade are ONE
decision with two levers and must be taken TOGETHER**: an inert mechanism makes the re-grade
permanent, a live one makes it revisable. Both remain deferred.
Earlier the same day: HEAD **`ca90c2f`**. §2.39 opened and CLOSED (the learning
loop graded OPEN positions — 47 of 65; fixed, closure is now `pnl IS NOT NULL` in the WHERE clause).
§2.39a: the three wrong grades CORRECTED in one asserted transaction, backup
`trades.db.bak_gradefix_20260803`. §2.39b: every `learning_*` attribution before `ca90c2f` marked as
attributed-to-a-mark, left in place deliberately. **§2.40 opened — 🔴 the combo-weight mechanism is
INERT at live size: ±20/−15 USDT against a 1R of $1.32–2.49 needs 8–15R, the loss side is
unreachable while the stop holds, and the last weight to move did so 2026-07-20 in the PAPER era —
yet the frozen table is still rendered into every entry prompt.** §2.41 opened — the 44-row re-grade
DEFERRED, and §2.40 makes it weightier: an inert mechanism means any value written now is PERMANENT.
§2.4 tally **4 → 5** (vpos 91's held branch terminated 08-03 13:52); §2.4 caveat 3 RETIRED — vpos
90's held branch terminated 08-02 02:05, so no datapoint can still change sign.
Earlier: **2026-08-01 13:40 UTC** — §2.37/a/b/c and §2.38 added.
Earlier: **2026-07-30 03:15 UTC** — 🔴 header REBUILT after a regression (see §9): this file
had forked at 2026-07-29 13:54 and the canonical copy still described Titan as a paper-mode bot
while §2.19–§2.22 in the same file described real-money incidents with real BingX order IDs. Rebuilt from the 2026-07-29 20:30 snapshot, the
true latest base. Tonight: §2.19/§2.20/§2.22 CLOSED (`625fedc`, `838481f`, `957f980`), §2.21 opened,
§2.4 count RESTARTED at `957f980` (0 of ~10), §2.4a vpos 86 verdict log added, §2.5 replication
recorded, §0 gained the ADX forming-candle row, §7 re-verified at 03:15, §9 added. HEAD **`957f980`**.
Earlier: **2026-07-29 20:05 UTC** — 🔴 **TITAN WENT LIVE** (`cb3a8bb`, 19:14 UTC): header rewritten, §1 CLOSED, §1a blocker A now UNREACHABLE BY CONSTRUCTION, §7 flags re-verified at 19:30, ⚡ first-live-trade section added at the top. Earlier: **19:55 UTC** — §1b added (margin mode CROSSED; leverage corrected to 5/5 on the exchange). Earlier: **18:15 UTC** — §1a added (TWO LIVE BLOCKERS, `closePosition` class); item 11 landed in `5f054b7`. Earlier: **17:35 UTC** — §2.4 updated with the vpos 85 datapoint (count now
**2 of ~10**). Earlier today: §2.3 closed (`8b15ecc`), §2.11 closed (`4fc89ea`), §2.8/§2.9/§2.10
added (`7285c5d`), §1 CORRECTED and §2.12–§2.17 opened after the full loose-ends sweep.
§2.12/§2.13 CLOSED by `c307bb7`; §2.14/§2.15 CLOSED and §2.2 ANSWERED by `41c4a4d`.
HEAD **`cb3a8bb`** — items 11, 12, 13 applied; both live gates disarmed; both mode flags UP._

> 🗄 **HISTORICAL NOTE — 2026-07-29 17:29 UTC. SUPERSEDED BY THE 19:14 FLIP (`cb3a8bb`).**
> ⚠️ **This box describes the state as it was at 17:29, NOT current state.** At that moment both
> mode flags were still False. They are now BOTH TRUE — see the header. Items 11, 12 and 13 have
> since been implemented (`5f054b7`, `0833f42`, `d63cb8b`); **item 14 is still NOT implemented.**
> Kept because the mechanism it describes is still what runs.
>
> **2026-07-29 17:29 UTC — LIVE-ORDER ADAPTER APPLIED, COMMITTED (`96b83d4`) AND RUNNING.**
> What changed:
> `order_adapter.py` is now the single seam for fills; three exchange-write paths that were guarded
> only by circumstance (`main.py:4044/4058` P3 legacy close; `breakeven_worker.py:213/436`, reachable
> only because `breakeven_jobs` has always been empty) are now guarded by the flag. Paper arithmetic
> is byte-identical — verified against vpos 85's stored entry fee `4.99715034`.
> **Boot now HARD-REFUSES an unsafe configuration:** with both mode flags True while
> `ROUTING_MIGRATED_TO_ADAPTER` is False, the process `os._exit(3)`s instead of starting, because that
> combination would route to the legacy path at the PAPER size ($10,000 notional instead of $200).
> Verified by execution, exit code 3. *(At 17:29 design items 11–14 were all unimplemented; 11/12/13
> have since landed. The `PARTIAL_FILL_MAX_DIVERGENCE = 0.02` constant is recorded but **still**
> read by nothing — item 14 remains open.)*
> Full detail: `reports/2026-07-29-1740-titan-adapter-committed-and-restarted.md`._

---

## ⚡ FIRST LIVE TRADE — READ THIS BEFORE ANYTHING ELSE

🗄 **UPDATED 2026-07-30 03:15 — the first live trades HAVE now happened. This section stays because
the watch-order below is still exactly what to watch; only its premise has changed.**

The original premise — *"no live path in this bot has EVER executed against a real exchange"* — was
true when written at 20:05 on 2026-07-29 and is **no longer true**. What has executed since:

- **A naked short, 2026-07-29 first live window** — position opened on the exchange with **no DB row
  at all**, closed manually at **−$0.26**. Root cause `97a4fdb`; it is why the bot reverted to paper
  at 21:26:52 and came back live at 21:54:16.
- **vpos 86, 2026-07-30 00:50:14 — the first real-money position WITH a proper row.** Still open at
  the time of writing. See §7 for its full state and §2.4a for its advisor verdicts.

**The experiment returned a result, and the result was that real execution finds what mocks cannot:**
three defects came out of it — the naked position (`97a4fdb`), an alert that named the wrong number
(`12b4df2`), and a 356 ms window with no protective stop (§2.20). **Keep reading the watch-order
below on every live entry; it has not been retired.**

### Watch in this order

| # | stage | ✅ normal | 🔴 wrong |
|---|---|---|---|
| 0 | boot | `[ORDER-MODE] 🔴 LIVE ORDERS` · both flags `True` · `margin $30 x 5 = $150` | `🛑 REFUSING TO START` → read the CRITICAL line; service crash-loops every 5s |
| 1 | entry | `[ADAPTER] LIVE ENTRY ... @ <price> fee=<real>` then `VIRTUAL ENTRY vpos=N ... sl=<price>` | `ENTRY REFUSED ... below minimum` (harmless, no position) · traceback from `create_market_order` (harmless, no row) |
| 1b | fee | fee read back from the exchange | `[ADAPTER] fee not reported ... ESTIMATED` — book fee is approximate, not wrong |
| 1c | fill size | asked == filled | `🔴 PARTIAL FILL on entry ... asked X, filled Y` — item 14 NOT built, position is smaller than intended |
| 2 | **stop** | `[ADAPTER] LIVE STOP ... @ <price> id=<order id>`, and the row's `stop_order_id` is set | `BE-SL-RETRY` x3 → `🚨 STOP PLACEMENT FAILED` → `✅ Emergency close executed` → **no row written**. This is CORRECT behaviour |
| 3 | exchange | **exactly ONE `STOP_MARKET` with `closePosition=true`** and nothing else | anything else — see the assumption below |
| 4 | management | recheck tiers, +1R breakeven via cancel-then-create, LONG partial | cancel fails → `OLD STOP HELD, retrying next tick` (correct, not a fault) |
| 5 | exit | `[VPOS-FILL] passive fill vpos=N ... reason=sl` (or `reason=breakeven`) + close report, row `status='closed'` | **SILENCE** — position closed on the exchange but NO `[VPOS-FILL]` and NO close report. Check `select status from virtual_positions where id=N`; if still `open`, item 13 did not fire |

### 🖐 THE THREE THAT REQUIRE HANDS — nothing self-heals here

1. **`[SL-FAILSAFE] CRITICAL: emergency close itself failed`**
   A REAL position is open on the exchange with NO STOP. Close it manually, immediately.
2. **`🚨 ORPHAN STOP COULD NOT BE CANCELLED ... MANUAL ACTION REQUIRED`**
   A stop is live over ANOTHER position at a level computed for a fill that never happened.
   Cancel it by hand.
3. **`🚨 POSITION GONE, STOP DID NOT FILL ... MANUAL ACTION REQUIRED`**
   Something else closed the position — manual action, liquidation, an exchange action. The exit
   price is UNKNOWN and deliberately **not invented**. The row stays open, which also **blocks new
   entries on that side** until a human resolves it.

### 🔴 THE ONE THING ONLY A REAL TRADE CAN SETTLE

**PARTIALLY OBSERVED as of 2026-07-30 — and the part that matters is STILL UNOBSERVED.**

What vpos 86 has now demonstrated: a `closePosition='true'` `STOP_MARKET` can be **placed**, it
**persists** (open since 00:50:14), it **survives a service restart with an unchanged order id**, and
it can be **cancelled and re-placed** (§2.20). Exactly one such order exists on the symbol.

**What has NOT been observed: the stop actually FIRING.** Every claim that depends on the trigger is
still an assumption — that it closes the whole remainder after a LONG partial, that no second
position is created, that an order against a zero position is rejected. **Placement is not
triggering. Do not read the first as evidence of the second.**

**REVERT IMMEDIATELY — both flags back to `False` and restart — if either of these is true:**
- the exchange shows **more than one** `closePosition` order on the symbol, **or**
- after the stop fires the position is **non-zero** (or, worse, **reversed**).

Rollback is `LIVE_TRADING_ENABLED = False` + `ORDER_ADAPTER_LIVE = False` in `config.py`, then
`systemctl restart titan.service`. While flat it is instant and complete.

---

## 0. HOW TO READ THE DATA WITHOUT FOOLING YOURSELF

Four filters. Most of the wrong conclusions killed in §4 came from skipping one of them.
**Apply all four before quoting any statistic about entries or exits.**

| Filter | Why | Predicate |
|---|---|---|
| Forming-candle fix | `srv_vol_ratio_5m` before this read the **forming** candle and is not comparable | `t.timestamp >= '2026-07-04 11:58'` (commit `55d9c7f`) |
| **ADX/ATR/EMA still read the FORMING candle — BY DESIGN, on every TF** | Not a filter and **not a defect to fix** — recorded so it is not rediscovered as a bug | `indicators.py:210-223`, verbatim: *"ATR/ADX/EMA above keep `iloc[-1]` on purpose — they are calibrated on the live forming candle and are out of scope."* The July fix (`55d9c7f`) dropped the forming row for `vol_ratio` **only**. Measured effect at vpos 86's entry: **1h −0.59, 15m +0.31, 5m +1.07** (0.3–1.1 pts). Caching (`_CACHE_TTL_BY_TF`) adds a second staleness layer but is not the driver. |
| Wall-trail window | Outcome decided by a **moved stop**, not by the entry | `NOT (opened_at < '2026-07-13T01:55' AND closed_at > '2026-07-02T23:28')` |
| Recheck TIGHTEN | Same — stop was moved after entry | `COALESCE(recheck_status,'') <> 'tightened'` |
| Excursion truth | `max_adverse_price` **stops updating at the close**, so it understates what price did | use real OHLCV candles, not stored extrema |
| 🔴 **Indicator WINDOW, not just algorithm** | The same `compute_tf_metrics` on a different candle limit is **not the same measurement**. ADX(14) is doubly Wilder-smoothed and ran **+6.23 mean high** on 42 bars vs 200 (§2.26). ATR/trend/EMA-gap are window-stable; **ADX is not** | any ADX must carry its window — `adx_window = 200` / `entry_adx_1h_window = 200`. Never compare two ADX figures whose windows differ or are unrecorded |

### 🔴 STANDING METHODOLOGY — VALIDATE THE REPLAY BEFORE YOU TRUST IT (operator, 2026-07-30)
**Confirmed as the pattern for ANY future rule change, not just this one.** Before a replay is used to
predict what a corrected rule *would* do, it must first **reproduce what the rule ACTUALLY did** from
the stored inputs — exactly, row for row. Only then is the corrected input swapped in.

The §2.26a replay did this: re-scoring all 38 `recheck_events` rows from their own stored
`entry_adx` / `adx_1h` / `atr_pct` / prices reproduced the **stored** `health_score` on **38 of 38**
rows before the 200-bar ADX was substituted. That step is what separates "the replay says 9 verdicts
flip" from "my re-implementation of the rules disagrees with the bot and I cannot tell which".

**Why this is a standing rule and not a nicety:** §4's items 3, 9 and 10 are three confident wrong
numbers, and every one came from a re-derivation nobody checked against the real thing first. A replay
that cannot reproduce the past has no standing to predict the future.

⚠️ The wall-trail filter must test **lifetime overlap**, not entry time. Using entry time alone
silently drops vpos 62. This exact bug produced a wrong answer once already.

**Sign convention:** skip-drift `_compute_drift_pct` is **positive = the skipped signal would have
won**. Reading it backwards inverts every veto conclusion. This caused a real inverted finding.

### 🔴🔴 `trades.confluence_score` HOLDS THREE DIFFERENT QUANTITIES. NEVER COMPARE IT ACROSS STATUSES.

**Found 2026-07-30 21:00 while building the score distribution. Documented in code at all seven
write sites and at the schema declaration by commit `dee6cee`.** This is the **fifth** instance of "the label does not say what
it means", and unlike the other four it silently corrupts *analysis* rather than behaviour.

| exit branch | what lands in `confluence_score` | write site |
|---|---|---|
| `below_threshold` | `_gated_score` = **raw + `total_gate_adj`** — the number the gate actually compared | `main.py:3695,3700` (+ mirrors `:1903,1908`, `:4222,4227`) |
| `risk_halt` | `direction_score` = **raw**, and `macro_gate_penalty` is left **NULL** | `main.py:3797` |
| every downstream status (`ai_skipped`, `virt_cap_blocked`, `executed`, `failed`, `claude_unavailable`) | `adj_score` = **raw + weight-engine adjustment**, clipped to ±1.5 | `main.py:3883` (+ `:2210`, `:4461`) |

The third is the trap. `weight_engine.py:191–193`, verbatim:
> *"`total_adj` is clipped to [−1.5, +1.5] and added to `direction_score` before storing as
> `confluence_score`. **Never applied to the gate check.**"*

**Measured cost of not knowing this:** a first reconstruction that assumed one meaning
(`raw + macro_gate_penalty == confluence_score`) matched **645 of 1,531 rows — 886 mismatches**,
with a mismatch spike at exactly ±1.5 and a fractional tail (0.31, 0.34, −0.19, 1.16 …) no gate
adjustment can produce.

🔴 **THE RULE: reconstruct the score from `matrix_breakdown_json`, never from `confluence_score`.**
That column is assigned **once**, at `main.py:3678`, *before* the gate, and the identical string is
written on every branch. Reconstruction from it validates **660/660** exact (594 `below_threshold`
as raw+adj, 39 `risk_halt` as raw, 27 `executed` as raw) and **898/898** exact on regime.

**Also do not trust `macro_gate_penalty` to be present:** it is **NULL on every `risk_halt` row**,
so the gated score is not computable for those 39 rows. Say so rather than defaulting it to 0.

⚠️ **NOT FIXED, only documented — and here is why.** Splitting this into distinct columns needs a
schema migration plus edits to every reader (`optimizer._bucket_confluence`, `claude_advisor`'s
prompt builder, `skip_attribution`) while real money sits in an open position. That is a behaviour
change wearing a cleanup's clothes, and it would need its own verification cycle. **Proposed, not
done.** Until it is done, this box is the guard.

---

## 1. ✅ LIVE-PATH PARITY GAP — **CLOSED** by items 11/12/13 (`5f054b7`, `0833f42`, `d63cb8b`)

🔴 **CORRECTED 2026-07-29: this list said THREE. There are at least SEVEN, and one entry was
recorded BACKWARDS.** Measured by presence in `virtual_trader.py` vs `main.py`:

| Mechanism | virtual_trader | main (live) | was it listed? |
|---|---|---|---|
| LONG partial realisation (1/3 at +1R, `f7df202`) | 7 refs | **0** | yes |
| Recheck TIGHTEN + original-SL floor (`93c20c3`) | 52 refs | 1 | yes |
| `original_sl_price` / the 1R reference itself | 17 refs | 1 | **no** |
| **WALL_ANCHOR** | 7 refs | **0** | **no** |
| **adaptive_trail** | 5 refs | 0 (3 in `breakeven_worker`) | **no** |
| **EXCURSION_LOGGING** | 2 refs | **0** | **no** |
| **SMART_EXIT_DRYRUN** | 9 refs | **0** | **no** |
| `breakeven_jobs` | own +1R poller | **table is LIVE-only, 0 rows ever** | **recorded backwards** |

**`breakeven_jobs` does NOT live in `virtual_trader.py`.** The table is written only by
`breakeven_worker.py`, whose `enqueue()` is called from the LIVE entry path (`main.py:1411`,
`main.py:4348`). It has **zero rows in its entire life** — originally because live trading had never
run, and **since `0833f42` because it CANNOT gain rows**: both `enqueue()` doors are shut and the
worker stands down by flag (§1, §1a). The
paper path has a *separate* +1R implementation inside `virtual_trader`. The divergence is real; the
direction was written down wrong, and the direction is what matters when planning the rewrite.

**The table above is now HISTORY, not a gap.** It records what the divergence WAS and why the
rewrite was necessary — keep it, because it is the evidence for the decision below.

**OPERATOR'S DECISION (2026-07-26), and it was carried out exactly as written:** rewrite the engine
as **ONE code path with two adapters** — orders either go to the exchange or are simulated — **NOT**
piecemeal porting of each mechanism into a second live path. Piecemeal porting is how the divergence
happened in the first place. **This record is kept deliberately:** if anyone later proposes porting a
mechanism into `main.py` "just for live", that is the mistake this project already made once.

### ✅ HOW IT WAS CLOSED — the engine owns the position in BOTH modes

`virtual_trader.engine_owns_position()` returns True, so `main._execute_entry` and
`_execute_close_position` route EVERY position to the engine regardless of mode; `order_adapter`
decides only whether the fills underneath are simulated or sent. **The legacy live entry path is
unreachable** — the engine branch returns at `main.py:~1289`, above the legacy `FIXED_MARGIN_USDT`
sizing at `main.py:1319-1320`. That is also why the "$10,000 instead of $150" catastrophe is
**physically unreachable**, not merely unlikely.

**Every mechanism in the table above therefore now runs IN LIVE**, because it runs in the one engine:
LONG partial realisation (1/3 at +1R) · recheck TIGHTEN with the `93c20c3` original-SL floor ·
`original_sl_price` / the true 1R reference · WALL_ANCHOR · adaptive_trail · EXCURSION_LOGGING ·
SMART_EXIT_DRYRUN · the exit advisor (DRYRUN — records verdicts, cannot close).

`breakeven_jobs` stays at **0 rows forever**: both `enqueue()` doors are shut (legacy entry
unreachable; `_resume_job_if_needed` guarded), and `breakeven_worker._poll_once` stands down by flag.

**What is genuinely different in live, and is accepted:**
- the protective stop is a real exchange `STOP_MARKET closePosition='true'` (item 11), so it
  triggers on the WICK rather than on a polled `last` — measured at **+36.91 in the book's favour**
  over 101,739 candles, not against;
- the **trail is still owned by the poller** — deliberately, see §1a;
- a stop that fires on the exchange is reconciled back into the row from the REAL price and fee
  (item 13); a breakeven exit is stamped `reason='breakeven'`, not `'sl'`.

---

### 1a. ✅ THE "TWO `closePosition` STOPS ON ONE POSITION" CLASS — BOTH DOORS SHUT
**One defect class, reached through two different doors.** Status as of the live flip
(`cb3a8bb`, 2026-07-29 19:14 UTC): **A is unreachable by construction, B is handled with one
alerted residual case.** The class itself is what matters — see the closing note.

**BLOCKER A — ✅ UNREACHABLE BY CONSTRUCTION in the current configuration (not "pending").**

**Why it cannot happen now, traced rather than asserted:** a `TRAILING_STOP_MARKET` has exactly ONE
creation site in the entire codebase — `breakeven_worker._attempt_trail` (`breakeven_worker.py:532`).
It is reachable only from `_poll_once` handling a `breakeven_jobs` row, and:
1. `breakeven_worker._poll_once` **returns 0 immediately** while `engine_owns_position()` is True —
   verified by execution: no position read, no order created;
2. `breakeven_jobs` **cannot gain rows** — the legacy entry `enqueue()` is unreachable and
   `_resume_job_if_needed` is guarded;
3. the engine's trail is **not an order at all** — it is a poller close TRIGGER that sends a market
   order via `market_close`.

⇒ **Exactly ONE `closePosition` order exists at any moment**: the item-11 `STOP_MARKET` (at
breakeven it is cancelled and recreated, one at a time). Two cannot coexist.

🔴 **THE WARNING STANDS, DO NOT DELETE IT:** implementing the exchange trail brings this straight
back. `_attempt_trail` creates the `TRAILING_STOP_MARKET` and **never cancels the breakeven
`STOP_MARKET`** — while the neighbouring `_handle_watching` carries the comment *"never hold two
closePosition stops."* **Before any exchange-trail work, the unanswered question below must be
answered first.**

**The original finding, kept as the record — INHERITED, not introduced.**
`breakeven_worker._attempt_trail` (`:436-441`) creates a `TRAILING_STOP_MARKET` with
`closePosition='true'` and **never cancels the breakeven `STOP_MARKET`**. So once the trail arms,
live holds **two `closePosition='true'` orders on one position** — while the neighbouring
`_handle_watching` carries the comment *"never hold two closePosition stops."* The existing live
path has always done this; item 11 inherits it.

> **THE UNANSWERED QUESTION, STILL UNANSWERED: what does BingX actually do if BOTH trigger on one
> move?** We have no data. Plausible outcomes range from "the second is rejected because there is no
> position" to "the second opens a REVERSE position". **Nobody has tested it and nobody should guess.**
> **Closes when:** the behaviour is observed on a real position, or the trail change lands with an
> explicit cancel-then-create. **Live was enabled WITHOUT answering it — legitimately, because the
> current configuration creates no trailing order at all. It must be answered before the exchange
> trail is built, not before live.**

**BLOCKER B — the orphan stop hangs over ANOTHER position, not over nothing.**
Found by the operator, 2026-07-29, correcting this session's first draft. That draft called a
leftover stop "inert, because `closePosition` with no position does nothing". **Wrong, and the
reasoning inverted the precondition.** `order_adapter.place_stop` runs BEFORE the row insert (so a
position is never written unprotected). The entry then aborts in exactly two places, and **both
abort only when a position on that side ALREADY EXISTS**:
- the capacity check — `MAX_POSITIONS_PER_SIDE = 1`, so `n_open >= 1`;
- `ux_vpos_one_open_per_side`, which is `ON (symbol, position_side) WHERE status='open'`.

So the orphan is **live over the OTHER position, at a level computed for a fill that never
happened**, and `closePosition='true'` means it would close it. Same defect as Blocker A.

**HANDLED in `5f054b7`** — both abort paths now call `order_adapter.cancel_stop()`, which cancels
the stop it placed and, if the cancel itself fails, prints and Telegrams `MANUAL ACTION REQUIRED`
(that residual case is real and is why this stays on the blocker list rather than being closed).
Verified by execution: cancel-ok returns True; cancel-fail returns False and emits the alert.

**Why both are recorded together:** the lesson is the class, not the two instances. Any code that
places a `closePosition` order must answer "what else is already protecting this position?"
before it sends. That question was not asked in `_attempt_trail`, and it was answered wrongly in
the first draft of item 11.

---

### 1b. ⚠️ MARGIN MODE IS **CROSSED** — REVIEW BEFORE ANY SIZE INCREASE
Read off the exchange 2026-07-29, read-only: `fetch_margin_mode('BTC/USDT:USDT')` returns
`{"symbol":"BTC-USDT","marginType":"CROSSED"}`. `config.py` had claimed *"isolated, hedge mode"*
since it was written. **The comment was simply wrong**; it has been corrected rather than the mode
changed.

**What crossed means here:** a position is backed by the **WHOLE account balance**, not by its own
posted margin. With $512.88 free and $150 notional at 5x ($30 of margin), the distinction is
immaterial — the 2.5xATR stop (~1.26%) triggers far before any liquidation. **That is the only
reason it is acceptable.**

🔴 **IT DOES NOT STAY IMMATERIAL WITH SIZE.** Under crossed margin there is no per-position
firewall: as notional grows, one bad position can reach the entire balance. Isolated margin caps
the loss at the position's own margin; crossed does not.

**Rule, recorded now so it is not rediscovered later:** before ANY increase of
`LIVE_FIXED_MARGIN_USDT` above the first-run 30.0, the margin mode must be reviewed and a decision
recorded — either switch BTC-USDT to ISOLATED, or state explicitly why crossed is still acceptable
at the new size. **Operator decision 2026-07-29: leave CROSSED for the first live run, do not
change account state tonight.**

**Related and fixed the same evening:** exchange leverage was **10x LONG / 20x SHORT**, not the 5x
the code assumes. `set_leverage(5)` was called for both sides and read back as 5/5, so the startup
banner's "x5" now matches reality. Note that `order_adapter.market_entry` re-issues
`set_leverage(5)` on every entry but the call is **warn-only** — if it ever fails, the value on the
exchange applies, not `config.LEVERAGE`.

---

## 2. STILL OPEN — carry forward

### 2.0 🔴 PRE-REGISTERED: `CONFLUENCE_SCORE_THRESHOLD` 2.0 → 3.0 — WRITTEN BEFORE THE CHANGE SHIPPED

> **SHIPPED `dee6cee`, 2026-07-30 21:26:19 UTC. Service restarted 21:26:34, runtime==commit proven,
> constant reads 3.0 in the loaded bytecode. The block below was written at 21:20, BEFORE the edit.**
> Post-change verification is in the 2026-07-30 21:35 report.

**Written 2026-07-30 21:20 UTC, BEFORE the edit was applied, so the expected effect cannot be
restated after the fact.** Numbers come from the 21:12 distribution report, measured on the
30 days ending 2026-07-30 19:00 over **1,531 events that reached the score gate** (TREND 630,
FLAT 901). Reconstruction validated **660/660** exact on score, **898/898** exact on regime.

**THE PREDICTION — judge the change against these five numbers, not against a later retelling.**

| # | quantity | before | **predicted after** |
|---|---|---:|---:|
| 1 | refusal rate on TREND signals reaching the score gate | **4.52%** (27/598) | 🔴 **15.72%** (94/598) |
| 2 | additional refusals per 30 days | — | 🔴 **+67** (≈**2.2/day**) |
| 3 | TREND trades removed, last 23 executed | — | 🔴 **3 of 23 (−13%)** — **vpos 68, 71, 78** |
| 4 | cap refusals that would have become trades (capacity effect) | — | **5 of 75 (6.7%)** — small, not zero |
| 5 | `CONFLUENCE_FLAT_THRESHOLD` | 5.0 | **5.0 — DELIBERATELY UNCHANGED** |

**REVIEW POINT — after 15 executed entries under the new bar.** Compare the realised entry rate
against the **15.72%** prediction and outcomes against the pre-change book.
🔴 **If the entry rate diverges materially from the prediction, that is a finding about the
distribution — NOT a reason to move the bar again.** Written here so that instinct is pre-empted.

**THE BASIS, on the record (operator's, 2026-07-30 21:18):**

1. **2.5 removes 0 of 23 trades — it does nothing. 3.0 is the smallest bar that binds at all.**
2. **3.5 is the cliff:** 10 of 23 trades. And on the **RAW** scale, 3.0 and 3.5 refuse the
   *identical* 144 events — buckets `[2.75, 3.00)`, `[3.00, 3.25)`, `[3.25, 3.50)` are **empty**.
   So anything above 3.0 is **bought purely with `total_gate_adj`, not with signal quality.**
3. 🔴 **The load-bearing evidence is NOT the n=11 cohort.** It is the skip-drift band split from
   the 19:14 report: the **2.0–3.0** band drifted **−0.324%**/24h over n=93 (*refusing was right*),
   the **3.0–4.0** band drifted **+0.463%** over n=188 (*refusing was wrong*). **3.0 sits exactly on
   that boundary. 4.0 crosses it.** This is why the bar is 3.0 and not 4.0, despite §2 of the 19:14
   report showing +3.19R at 4.0 over n=5 — that cohort is not what this decision rests on.
4. **Structurally:** a raw score of 2.25–2.75 means **essentially only the trigger scored.**
   A *confluence* gate that admits signals with no confluence is not doing what its name says.

**WHY `CONFLUENCE_FLAT_THRESHOLD` WAS NOT TOUCHED — and must not be, without new evidence.**
The FLAT floor already refuses **78.86%** of what it judges (705/894), against the TREND bar's
4.52% — a 17× difference on the same scale. And the band it refuses most heavily, **3.0–4.0**, is
the band whose refusals measured **most costly** (+0.463%/24h, n=188). Tightening FLAT runs
straight into that number. Raising it is not a smaller version of this change; it is the opposite
change.

🔴 **A structural inversion that becomes live above 5.0, restated so it is not rediscovered:** at a
TREND bar above 5.0 the FLAT floor stops being a floor and becomes a **discount** — a FLAT signal
at 5.5 would pass while a TREND signal at 5.5 would be refused. At **3.0 this is not active** and
observed rows that would flip are **0**. It is a construction defect waiting, not one in force.

**What this change does NOT do.** It cannot admit anything — raising the bar only adds refusals.
It does not touch the FLAT branch, the HTF cascade (4,077 refusals, 72.7% of all refusing), or the
LLM (831). **The score gate remains a minority gate**; this makes it a real one, not a large one.

### 2.1 LONG partial parameters are placeholders
`LONG_PARTIAL_LEVEL_R = 1.0`, `LONG_PARTIAL_FRACTION = 1/3` were chosen as **round numbers that
survived simulation**, not as optima. Retune at **~30 clean longs reaching above 0.5R**.
**Current: 7 clean** (was 6; vpos 82 added tonight).

**First live firing — 2026-07-27 00:07, vpos 82:** partial took **+18.91 USDT** at 1R, remainder
rode the unchanged contract to a trail exit, **total +53.79**. One datapoint. It proves the
mechanism executes and folds into `net_pnl`; it proves **nothing** about the parameters.

### 2.2 Variant C (narrower LONG trail) — STUDIED 2026-07-29. STRUCTURE only; WIDTH undecidable.
Simulated on **real 5m candle paths** (18,900 bars), replicating the live contract exactly —
1R stop, breakeven + trail arming at +1R, never-loosen, intrabar resolved ADVERSELY. Validated at
width 1.0 against the 10 clean closed positions: all four stop-outs reproduce at −1.00R vs a real
−1.09…−1.20 (the difference is fees), trails reproduce within 0.11–0.13R.

🔴 **THE CRUX: the trail only arms at +1R, and almost nothing gets there.**
Of the 10 clean closed positions, **3 of 5 LONGs and 4 of 5 SHORTs NEVER ARMED IT.**
A position that never reaches +1R is **identical under every trail width**, so the width question
has an effective **n of 2 (LONG) and 1 (SHORT)**.

| width | LONG net R (n=5) | winners cut | losers improved |
|---|---|---|---|
| **1.0 (today)** | **+0.46** | — | — |
| 0.75 | +0.96 | 0 | 0 |
| 0.6 | +1.26 | 0 | 0 |
| 0.5 | +1.46 | 0 | 0 |

Monotone and entirely driven by **two positions** (vpos 79 and 82). The other three are byte-identical
across all four widths. "0 winners cut" is a two-observation coincidence, not a property.

🔴 **SHORT CONTROL — 0.5R IS DISQUALIFIED.** Re-simulated from entry on the 8 short runners
(43, 44, 46, 48, 49, 57, 58, 81; MFE 1.87R–3.40R):
| width | total R across the 8 runners |
|---|---|
| 1.0 | **+13.57** |
| 0.75 | +13.06 |
| 0.6 | +14.01 |
| **0.5** | **+8.67 — the tail is destroyed (−36%)** |
vpos 58 falls 2.41R → 1.07R, vpos 46 2.31R → 0.81R. The 0.6/0.75 differences are non-monotone,
i.e. noise. **Any narrowing must be LONG-ONLY, and 0.5R is out for shorts on this evidence.**

**Interaction with the LONG partial (`f7df202`) — they are SUBSTITUTES, not complements:**
| width | LONG net R, no partial | WITH the 1/3 @ +1R partial | partial's contribution |
|---|---|---|---|
| 1.0 | +0.46 | **+0.76** | **+0.30** ← today's live contract |
| 0.75 | +0.96 | +1.10 | +0.13 |
| 0.6 | +1.26 | +1.30 | +0.03 |
| 0.5 | +1.46 | +1.43 | **−0.03** |
Both solve the same problem — banking before giveback — so stacking them gives diminishing and then
NEGATIVE returns. **A narrower trail plus the partial is not the sum of the two.**

**VERDICT: enough to choose a STRUCTURE, nowhere near enough to choose a WIDTH.**
- Structure supported: *longs give back too much at 1.0R, and narrowing helps them without touching
  shorts*. Direction is consistent across both informative longs and both partial variants.
- Width NOT supported: n = 2 armed longs. Any width chosen today is fitted to vpos 79 and 82.
- **What the parameter needs:** ARMED longs, not merely closed ones. Historical arming rate is
  **22% for LONGs** (5 of 23) — a stricter bar than §2.1's ">0.5R". At 0.74 closed positions/day
  that is ~0.13 armed longs/day → **20 armed longs ≈ 5 months, 30 ≈ 7.5 months.**
- 🔴 **Do NOT apply a width on this evidence.** Not applied, by design.
Full study: `reports/2026-07-29-1400-titan-variant-c-and-final-cleanup.md`

### 2.3 ✅ CLOSED 2026-07-29 (`8b15ecc`) — entry advisor now has the percentile scale
The entry advisor received the **hard-coded word "Massive"** for every wall above `4.0x` with no
percentile scale, while 100% of observed book states contain such a wall — a constant read as an
alarm. `main._entry_book_pct()` now calls the **same `_exit_pct()`** against the **same
`orderbook_density`** baseline the exit side has used since `ef7fa10`, and the label is deleted.
The system prompt's opposing-wall HARD RULE now judges thickness by the printed percentile too.
Evidence: `reports/2026-07-29-1011-titan-entry-advisor-percentiles-and-two-entry-forensics.md`

### 2.11 ✅ CLOSED 2026-07-29 (`4fc89ea`) — exit prompt's "Total depth" line
It rendered **`n/a` on 100% of the 59 exit consultations ever made**: the field was in the template
and `_build_exit_context` never set `depth_pct`. Now read from the latest `orderbook_density` row,
percentiled through the same `_exit_pct()` baseline, with the sample age printed so a stale row is
visible. Both advisors now describe depth in the same language.

### 2.4-OP 🔴 OPERATOR RULING, 2026-07-30 13:40 — THE WINDOW, AND WHY IT CANNOT RESET AGAIN
**Recorded BEFORE the window opens, which is the whole point.** Three decisions, all the operator's,
written here verbatim in effect so no later session can soften them.

**1 · STRICT on vpos 86 — it contributes ZERO.** Its **first** `close` verdict (01:50:24) was
produced under the cross-source book defect. Nominating the 03:50:29 verdict as "the first" is
exactly the re-cut the criterion forbids. **§2.4 stays 0 of ~10.** The nine clean-book verdicts are
kept as an operational fact (§2.4b), not as a datapoint.

**2 · NO THIRD RESTART, EVER, AND THE REASON IS A FAILURE MODE OF ITS OWN.** The count has restarted
twice (`c307bb7`, `957f980`) and a **second, independent** contamination was then found in the same
sample (§2.26, the ADX window). Operator's ruling, and it is correct:

> **If every fix voids the accumulated sample, the criterion becomes unfalsifiable by attrition.**

So the rule is now:

- 🔴 **The criterion's window BEGINS at the commit that fixes the ADX window defect (§2.26).**
  Nothing before that commit counts. Nothing before it will ever be re-admitted.
- 🔴 **From that commit the exit prompt's INPUTS ARE FROZEN for the window's duration.** No change to
  `_build_exit_context`, `claude_advisor`'s close template, the book block, the regime block, the
  tier block, the trail block, or any figure rendered into the close prompt — **without explicitly
  VOIDING the window and RESTATING it in this file, in the same commit as the prompt change.**
  A silent prompt change during the window is the defect this rule exists to prevent.
- 🔴 **If a defect is found DURING the window: finish the window and record the caveat. Do not
  reset.** The result is then reported with the defect stated alongside it, and the operator decides
  what the caveat is worth. A noted caveat on a completed window beats a third empty restart.
- **Freeze scope — ✅ EXPLICITLY CONFIRMED BY THE OPERATOR 2026-07-30 14:0x, SETTLED, do not
  re-open the definition:** frozen = **everything the advisor READS**. **NOT** frozen = act/hold
  plumbing, logging, labels, close mechanics, and **the entire entry side**. *Fixing a close mechanic
  does not void the window; changing a number the advisor sees does.*
- 🔴 **THE WINDOW IS OPEN.** It opened with the ADX-window fix commit (§2.26a) — applying that patch
  is the act that started this clock. From that commit forward, any change to a figure rendered into
  the close prompt requires **voiding and restating the window in this file, in the same commit**.

**3 · Record the nine verdicts as an OPERATIONAL fact with their arithmetic — see §2.4b.** Not
admissible for §2.4, and it is still the strongest signal we have about the advisor; it must not
vanish because of a rule.

### 2.4b vpos 86 — NINE clean-book `close` verdicts, ALL of which beat the actual exit (operational)
**Not a §2.4 datapoint (see §2.4-OP·1). Recorded because a rule that discards evidence must not also
erase it.** All nine were issued after `625fedc` deployed at 02:51:11, i.e. on a corrected book
block. Counterfactual net computed at the nearest `position_excursion_samples` price, entry fee
0.073239 actual + exit fee at the 0.0005 taker rate; R against `initial_risk_usdt` 2.48655500.

| trades row | UTC | px (nearest sample) | net if closed | R | vs actual |
|---|---|---:|---:|---:|---:|
| **19607** | **03:50:29 (first)** | 64191.30 (03:52:45) | **−1.3092** | −0.527 | **+1.2324 / +0.495R** |
| 19617 | 04:50:34 | 64060.00 | −1.0071 | −0.405 | +1.5345 / +0.617R |
| 19624 | 05:50:43 | 64038.70 | −0.9581 | −0.385 | +1.5835 / +0.637R |
| **19628** | **06:50:53 (best)** | 63961.00 | **−0.7793** | **−0.313** | **+1.7623 / +0.709R** |
| 19633 | 07:50:54 | 63970.00 | −0.8000 | −0.322 | +1.7416 / +0.700R |
| 19646 | 08:45:12 | 64309.20 | −1.5806 | −0.636 | +0.9610 / +0.386R |
| 19649 | 08:51:02 | 64288.30 | −1.5325 | −0.616 | +1.0091 / +0.406R |
| 19660 | 09:51:11 | 64549.70 | −2.1340 | −0.858 | +0.4076 / +0.164R |
| 19678 | 10:51:14 | 64569.20 | −2.1789 | −0.876 | +0.3627 / +0.146R |
| — | **11:50:48 ACTUAL** | **64733.00** | **−2.541574** | **−1.02213** | — |

**9 of 9 beat the actual exit. Range +0.146R to +0.709R.** Add the three contaminated-book `close`
verdicts (01:50, 02:00, 02:50) and the advisor said `close` **twelve times over nine hours** on a
position that then ran to its stop.

🔴 **AND THE CAVEAT THAT MAKES THEM INADMISSIBLE TWICE OVER:** every one of these nine prompts also
carried a warm-up-biased ADX (§2.26). Row 19590's own words — *"bearish regime (ADX rising to
14.9)"* against a true entry ADX1h of 11.1 — are that artefact. So the nine are contaminated by the
ADX seam even though their book block was clean. **This is the concrete case that motivated §2.4-OP·2:
the sample was voided twice by two different seams, and a third reset would teach nothing.**

**Two timing facts, for the record:** `exit_advisor_last_ts` was 10:51:11, so the next consult was
due **11:51:11**; the stop filled at **11:50:47.926**, i.e. **23.1 s** earlier. The advisor was armed
at 11:32:45. **Arming was correct and bought zero datapoints.**

### 2.4 Exit-advisor criterion — **REPLACED 2026-07-30 11:10 UTC, MEASURED THE OTHER WAY ROUND**
The criterion is **not abandoned — it is mirrored.** Written into this file **BEFORE the advisor was
given hands and therefore before any position could close under it**, for exactly the reason the
original was written in advance: so the bar cannot be moved after seeing results.

#### 🔴 THE CRITERION IN FORCE (from the commit that sets `EXIT_ADVISOR_DRYRUN = False`)

> For every position the advisor CLOSES, replay from **real 5m candles** what the unchanged contract
> would have done had the position been held — **stop, breakeven, trail, LONG partial, and any
> intrabar ambiguity resolved ADVERSELY to the held branch's favour being overstated** — and record
> **advisor-close vs held-branch** in USDT.
> It stays live only if, over the first **~10 advisor-closed positions**, the advisor beats the
> held branch **both in total USDT and in positions improved**.
> **No partial credit. No re-cutting the sample. Every advisor close counts** — not its best ones.

**Same bar, same ~10, same no-re-cutting rule.** What changed is which branch is counterfactual.

**WHY THE MIRROR IS LEGITIMATE, stated as the operator put it and not softened:** the original
justification for DRYRUN was that both branches stay observable — the verdict *and* what actually
happened. **That justification was weaker than it was presented.** The held branch is
**recoverable from candles**, and this project has reconstructed exactly this kind of counterfactual
from OHLCV three times: **13,536 candles** for the stop counterfactual, **101,739** for the wick
study, **18,900 bars** for Variant C. Replaying "what if we had held" is a solved problem here, not
a lost observation. **So the real cost of DRYRUN was never preserved knowledge — it was forgone
action**, and on vpos 86 that cost is measurable (§2.4a).

**WHAT THE MIRROR CANNOT RECOVER, stated so it is not discovered later as a surprise:** funding
accrued on the held branch is estimated, not ledgered; and a held branch that would have been closed
by a *future advisor verdict* is not modelled — the replay holds to the mechanical contract only.
Both bias the comparison **toward the held branch**, i.e. against the advisor. That is the safe
direction and is deliberate.

#### The wording this replaced — kept verbatim as the record
> It goes live only if, over the first **~10 closed positions**, its **FIRST** `"close"` verdict
> beats the actual exit **both in total USDT and in positions improved**.
> **No partial credit. No re-cutting the sample. First verdict only** — not its best verdict.

It was measurable only while the advisor was blocked: it asks whether the advisor's first `close`
**would** have beaten an exit that something else produced. Once the advisor produces the exit, that
question has no held branch left to compare against — hence the mirror above, not a weakening.

🔴🔴 **Progress under the OLD criterion: 0 of ~10 — RESTARTED A SECOND TIME at `957f980`, 2026-07-30 02:51 UTC.**
**(Previous restart: `c307bb7`, 2026-07-29 13:21 — see §2.18. That restart is now itself void, and
the two datapoints it had collected, vpos 84 and vpos 85, are discarded with it.)**

**WHY IT RESTARTS AGAIN — and the partition question, answered with data.** Every exit consult
before `625fedc` was handed at least one **inverted** book percentile (§2.19). On vpos 86 the prompt
said `Imbalance = 0th pct` for a book at the 62nd–69th and `Opposing wall = 93th pct` for one at
~50th, **and the advisor quoted the phantom 93rd-percentile wall as a reason to HOLD.**

The operator proposed the right partition: reset consults whose reason **cites a book figure**, keep
those that do not, since the corruption is confined to the book block. **Agreed in principle — and
the data collapses it into a full restart, because the second bucket is EMPTY:**

| cohort | n | closes | holds |
|---|---:|---:|---:|
| reason **CITES** a book figure | **68** | 43 | 25 |
| reason does **not** cite the book | **0** | — | — |

**68 of 68 exit consults ever recorded cite a book figure** (64/68 say "wall" alone; the rest cite
imbalance or book). Confirmed against verbatim samples, not just a pattern match:
*"Supporting wall thinned (5.0→4.3x, 14th pct)"* · *"Order-book imbalance flipped from 0.21 to 0.52
(76th pct—ask-heavy resistance)"*. **So there is no clean cohort to preserve and no judgement call.**

**Caveat recorded so the reasoning stays auditable:** "the reason does not mention the book" would
**not** have proven non-contamination anyway — the prompt is read whole, and a fabricated
"0th percentile" is an extreme claim capable of moving a verdict it is never quoted in. The empty
bucket removes a judgement we would otherwise have had to defend. **The bar itself does not move.**

**Contamination ledger, cumulative:** vpos 82, 83 (pre-`c307bb7`) · vpos 84, 85 (pre-`957f980`) ·
vpos 86, all four consults (pre-`957f980`). None are counted.

**Datapoint 1 — vpos 84**, closed 13:30:08 at **+16.54**. Its only verdict under the corrected prompt
was `hold` (row 19460, 13:30:08); **no `close` verdict was ever issued**, so it is NEUTRAL for the
criterion — the advisor neither improved nor worsened the exit. Same shape as the discarded vpos 82.

**Datapoint 2 — vpos 85**, LONG, closed **2026-07-29 16:42:36 UTC at the stop**, `reason=sl`,
**net −137.31685**. This one produced a `close` verdict, so it counts as a real test.

| | value |
|---|---|
| entry | 64604.4 (2026-07-29 13:50:18), size 0.1547, 1R = 816.9 px = 1.2645% |
| original SL | 63787.5 — never moved; `breakeven_applied=false`, no partial taken |
| verdict 13:50:30 | `hold` (conf 0.72) |
| **FIRST `close` verdict** | **14:50:38, conf 0.72** — cited a broken entry thesis and a regime flip (15m HyperWave SHORT against the position; ADX1h 49.1; 15m/5m bear) |
| position R at that verdict | between **−0.646R** (14:45:54 sample) and **−0.561R** (14:50:58 sample) |
| actual exit | 63787.1 at 16:42:36 → **−1.000R** |

Arithmetic, first verdict vs actual, at the nearest excursion sample to the verdict (64146.3):

```
gross if closed on first verdict : (64146.3 − 64604.4) × 0.1547   =  −70.8681
gross actual                     :                                  −126.43631
improvement, gross               :                                  +55.5682

net if closed (entry fee 4.99715034 + exit fee 4.96172)           =  −80.8269
net actual (fees 9.931083, funding 0.949459)                      =  −137.31685
improvement, net (excl. funding accrued after 14:50)              :  +56.4899
```

**Counts as IMPROVED.** The advisor's first `close` verdict beat the actual exit by **+55.57 gross /
≈+56.49 net**, and the position went from −0.6R to the stop after the verdict was issued.

*Caveat stated for the record, not as an adjustment:* the −0.61R figure in the advisor's own text is
the **1h price move**, not the position's P&L; the position's own R at that moment is the bracket
given above. The net figure excludes funding accrued between 14:50 and 16:42, which is a fraction of
the 0.949459 total and is not separately recorded per-sample.

**Running tally since the restart: improved 1, worsened 0, neutral 1. Eight more closes needed; the
bar does not move.**

The pre-fix count was 2 of ~10 (vpos 82, vpos 83); both are contaminated and are no longer counted.

Historical record of the discarded pair: **59 consults** recorded. vpos 82: no `close`
verdict ever issued (actual +53.79 kept). vpos 83: first `close` at 2026-07-28 04:00:51 would have
been **+23.61 gross vs the actual −135.80** — an improvement of ~159 USDT. Running tally: **improved
1, worsened 0, neutral 1.** Eight more closes needed; the bar does not move.
Currently `EXIT_ADVISOR_DRYRUN = True`: it can never close a position.

#### 🔴 TALLY — **n = 5 of ~10** as of 2026-08-03 14:00 UTC. FIVE MORE CLOSES NEEDED; THE BAR DOES NOT MOVE.

Held branches replayed on real 5m BingX candles, **intrabar ambiguity resolved ADVERSELY to the held
branch**, each seeded from the position's real state at the advisor's close.

| vpos | side | held-branch outcome | advisor net | held net | **advisor − held** |
|---|---|---|---:|---:|---:|
| 87 | LONG | `sl` @ 64028.8, bar 07-31 07:05 | −0.8191 | −2.0110 | **+1.1919** |
| 88 | SHORT | breakeven → `trail` @ 63192.2, bar 07-31 17:50 | −0.5311 | +0.8914 | **−1.4225** |
| 89 | SHORT | `trail` @ 63171.3, bar 07-31 17:50 | +2.3024 | +1.0703 | **+1.2321** |
| 90 | SHORT | `sl` @ 63491.9, bar 08-02 02:05 *(resolved 08-03)* | −0.6099 | −2.1541 | **+1.5442** |
| **91** | SHORT | **`sl` @ 63224.6, bar 08-03 13:52** *(new)* | **−0.6410** | **−1.4682** | **+0.8272** |

```
NET n=5 : advisor -0.2987  vs  held -3.6716   ->  advisor +3.3729 USDT.  Improved 4, worsened 1.
(n=4 was +2.5457 after vpos 90 resolved; +1.5852 when vpos 90 was still a mark)
```

**Datapoint 5 — vpos 91**, SHORT 0.0023 @ 62649.2, closed by the advisor **2026-08-03 13:41:09** at
62871.4, `reason=ai_exit`, net **−0.6410**. Verdict verbatim: *"Entry thesis collapse: 15m was
opposing at entry (HyperWave OS LONG vs SHORT trade); now 15m=bull, 5m=neutral with bullish
structure… Regime shifted."* Held-branch seed: `sl 63224.6` (never moved), `breakeven_applied=false`,
water mark 62268.6 = **+0.661R**, so the +1R arm at 62073.8 was never reached — no breakeven, no
trail, the original stop stands. Held gross **−1.32342**, fees 0.144756 (entry 0.072047 + exit
0.072709 @ 5.0 bps) → **held net −1.46818**, funding not ledgered (**biases toward the held branch**).

⚠️ **Margin disclosed, because it was thin at first touch and thick eleven minutes later.** The 13:52
1m bar cleared the stop by **+0.4 pts** (H 63225.0 vs 63224.6) on a **last-price** candle, while the
real stop triggers on **MARK**. The rule resolves that — ambiguity goes against the held branch — but
the datapoint does **not rest on it**: the 13:55 bar printed **H 63287.7**, clearing the stop by
**63.1 pts**, and 13:56 by 8.8. **Unambiguous either way.**

#### 🔴 CAVEATS RECORDED 2026-08-01 AT n=4 — CAVEATS, **NOT** REASONS TO RESET (§2.4-OP·3)
Recorded while the window is OPEN and before it completes, so none of them can be introduced later to
explain away a result. **The bar does not move and the count does not restart.**

1. **FEES EXCEED THE SAMPLE'S REALISED P&L.** Four advisor round trips paid **0.5849 USDT** in fees
   against a total realised **+0.3423**. Mean **0.1462 per round trip** on ~$146 notional = **~0.08R
   burned per decision** before the advisor's judgement is worth anything. The counterfactual in §2.4
   is computed net of fees on both branches, so this does not bias it — but any reading of "the
   advisor is roughly break-even" must state that it is break-even **after** paying 1.7× its own
   P&L in fees.
2. **NO CLOSING THRESHOLD CAN BE READ FROM THIS DISTRIBUTION.** The closes cluster at unrealised
   −0.36 / −0.22 / +1.50 / −0.26 R, which looks like a threshold near −0.3R. It is not readable as
   one: **the deepest adverse reading ever shown to the advisor across all 27 consults is −0.36R**,
   and 25 of 27 land within ±0.4R of flat. There is **no consult at −0.5R, −0.7R or −0.9R that it
   held through**, so "it closes at about −0.3R" cannot be separated from "−0.3R is the worst it has
   ever been asked about." A distribution with no tail cannot yield a threshold.
3. ~~**ONE HELD BRANCH IS UNRESOLVED.** vpos 90's counterfactual never terminated — it is marked to
   market at 2026-08-01 12:25 (+0.291R for the advisor), not resolved by stop or trail. **One of the
   four datapoints can still change sign.**~~
   ✅ **RETIRED 2026-08-03 — it terminated.** vpos 90's held branch hit its stop **63491.9 on the
   5m bar of 2026-08-02 02:05 UTC** (O 62939.0 H **63500.0** L 62937.6 C 63365.9). Its +1R
   breakeven arm at 61744.9 was never reached (window low 62245.0), so the stop stood untouched the
   whole time and no trail could arm. Held net **−2.1541** vs the advisor's **−0.6099** →
   **advisor +1.5442 (+0.769R)**, up from the +0.5837 mark. **All held branches are now terminated
   and no datapoint can still change sign.** 828 real 5m BingX candles, 07-31 16:25 → 08-03 13:20.
5. 🔴 **FROM `3316e8a` THE SAMPLE IS FILTERED — see §2.37a.** The loss-streak brake is live and
   blocks entries after three consecutive losses, so the remaining ~6 datapoints are drawn from a
   differently-selected population than the first four. Had it been live already it would have
   blocked **vpos 89 (+2.30) and vpos 90 (−0.61)**. This does **not** void the window (§2.4-OP: the
   entire entry side is not frozen) but the final result must carry it on its face.

4. **THE HELD BRANCHES ARE MUTUALLY EXCLUSIVE** (`MAX_POSITIONS_PER_SIDE = 1`). Holding vpos 88 to its
   trail exit at 07-31 17:50 means **vpos 89 and 90 could never have opened**. The per-position
   arithmetic §2.4 asks for is correct as stated; it is **not** a portfolio result and must not be
   read as one.

### 2.4a vpos 86 — exit-advisor verdicts logged AS THEY HAPPEN (live, DRYRUN-blocked)
Recorded now rather than reconstructed later, so the datapoints exist whichever way the trade goes.
SHORT 0.0023 BTC @ 63686.0, opened 2026-07-30 00:50:14, 1R = 1081.1 pts, stop 64767.1 on the
exchange. **`EXIT_ADVISOR_DRYRUN = True`, so every one of these was blocked by design.**

| # | time (UTC) | trigger | verdict | conf | position R | book block |
|---|---|---|---|---:|---:|---|
| 19590 | 00:50:20 | hourly (first, `_st is None`) | `hold` | 0.72 | **−0.01R** | 🔴 corrupted — cited the phantom 93rd-pct wall |
| 19601 | 01:50:24 | hourly | **`close`** | 0.72 | **−0.47R** | 🔴 corrupted |
| 19602 | 02:00:09 | `15m_exit_confirm` | **`close`** | 0.72 | **−0.55R** | 🔴 corrupted |
| 19604 | 02:50:25 | hourly | **`close`** | 0.72 | **−0.51R** | 🔴 corrupted — fired 46s before the fix deployed at 02:51:11 |

**Three consecutive `close` verdicts, all "entry thesis broken/compromised"** — 15m flipped bull, 5m
bull/neutral, bullish I-CHOCH and OB created against the short. All four carried at least one
inverted percentile, so **none count toward §2.4**. Logged as an operational record only.

**Worth reading even so:** their stated reasoning rests on the **regime flip**, which is measured on
price and is unaffected by the percentile defect. That is an argument for reading them, not for
counting them. **The first verdict is what §2.4 measures, and for vpos 86 that was `hold` at −0.01R**
— recorded before the outcome is known, so the bar cannot be moved afterwards.

#### 🔴 THE NINE CLEAN VERDICTS — first admissible ones, recorded 11:10 UTC WHILE THE TRADE IS STILL OPEN
Every consult since the `957f980` fix at 02:51:11. **All nine say `close`, all at confidence 0.72.**
Position R is computed from `position_excursion_samples` (nearest sample at or before the verdict),
**not** from the advisor's own text — the two agree to within ~0.05R everywhere they overlap.

| row | time (UTC) | trigger | verdict | conf | px | position R | to stop |
|---|---|---|---|---:|---:|---:|---:|
| 19607 | 03:50:29 | hourly | **`close`** | 0.72 | 64162.8 | **−0.441R** | 0.559R |
| 19617 | 04:50:34 | hourly | **`close`** | 0.72 | 64060.0 | **−0.346R** | 0.654R |
| 19624 | 05:50:43 | hourly | **`close`** | 0.72 | 64038.7 | **−0.326R** | 0.674R |
| 19628 | 06:50:53 | hourly | **`close`** | 0.72 | 63961.0 | **−0.254R** | 0.746R |
| 19633 | 07:50:54 | hourly | **`close`** | 0.72 | 63982.0 | **−0.274R** | 0.726R |
| 19646 | 08:45:12 | `15m_exit_confirm` | **`close`** | 0.72 | 64252.0 | **−0.524R** | 0.476R |
| 19649 | 08:51:02 | hourly | **`close`** | 0.72 | 64309.2 | **−0.576R** | 0.424R |
| 19660 | 09:51:11 | hourly | **`close`** | 0.72 | 64608.0 | **−0.853R** | 0.147R |
| 19678 | 10:51:14 | hourly | **`close`** | 0.72 | 64569.2 | **−0.817R** | 0.183R |

**The book block is now provably the right scale.** Every one of the nine carries the header
`source: OKX books-full depth-4000 (the percentile baseline)` and an internally consistent reading —
e.g. 19678: `Supporting wall x7.4 = 70th pct · Opposing wall x4.5 = 23th pct · Imbalance 0.38 = 0th
pct · Total depth 3155 BTC = 70th pct`. **The phantom "93rd-percentile wall" that talked the advisor
into holding at 00:50 does not recur in any of the nine.** `625fedc` is proven on live data.

**Their common thesis, unchanged across seven hours:** the entry was 4/4 lower-TF BEAR; 15m and 5m
went NEUTRAL, then BULL. Verbatim from 19678 (10:51): *"At entry: 4/4 lower-TF alignment
(4h/1h/15m/5m all BEAR). Now: 15m=BULL, 5m=neutral. Regime flipped bullish on lower timeframes.
ADX15m surged to 32.1. Imbalance collapsed from 0.51→0.38 (entry edge gone, now at 0th percentile —
weakest reading)."*

**Recorded before the trade resolves, so the datapoint exists whichever way it goes.** The advisor's
best available exit was **−0.254R at 06:50**; by 09:51 the position was **−0.853R with 0.147R of
stop cushion left**. It has since printed a new MAE of **64613.7 (−0.858R)** against an MFE that
never exceeded **+0.099R**.

🔴 **NONE OF THESE NINE CAN BE ACTED ON**, and not because of the DRYRUN flag — because of the
call-site defect in §2.23. They were produced by the `hourly` and `15m_exit_confirm` triggers, and
**neither of those paths contains a close mechanic at all.**

### 2.5 Volume ceiling — NOT BUILT, and has an EXPIRY
Clean n is **5 SHORT / 4 LONG** (2026-07-29). SHORT **p = 0.333**; LONG **contradicts** the thesis (p = 1.000).

The earlier, exciting **p = 0.048 came from three contaminated rows** (vpos 66, 68, 74). The
sensor that reported it has since been fixed to count clean rows only.

🔴 **2026-07-30 — IT REPLICATES AT A LARGER CLEAN n. The study was killed on a sample size that no
longer applies.** On the clean closed cohort (n=53):

| cohort | n | wins | net $ |
|---|---:|---:|---:|
| entries at `vol_ratio_5m` **≥ 2.42** | **15** | **2 (13%)** | **−$708.72** |
| entries in the **1.30–1.60** band | 9 | 6 (67%) | **+$241.07** |

Median `vol_ratio_5m`: winners **0.95**, losers **1.57**. vpos 86 entered at **4.92 = 92nd
percentile**, inside the bad band near its top. The original split was killed at n=4; this is
n=15 vs n=9.

**CONFOUNDS, STATED — this is NOT a validated ceiling:** 11 of the 15 high-volume entries are
**LONGs**, so direction is entangled with volume; the sample spans **two sizing eras**, so dollar
figures are not comparable across it. **This is an ENTRY filter and needs its own study — DO NOT
BUILD IT FROM THIS TABLE.** The point of the record is only that the kill rested on n=4 and that
basis is gone.

Re-cut at **~10 clean corrected SHORT closes**. **EXPIRES 2026-09-30** if n is not reached —
**delete it then.** Rationale: the counter-short caution shipped on a statistic that quietly
stopped being true and nobody re-checked for months (§4.5). An expiry date is how that is
prevented, so **do not extend it silently**.

### 2.6 🔴 EQH/EQL SMART TP — READS AS ARMED, IS UNREACHABLE. DO NOT "FIX" IT.
`EQH_EQL_SMART_TP_ENABLED = True` in config **READS AS ARMED AND IS NOT.** The flag is only ever
read inside `_handle_liquidity_sweep()` (`main.py:2746`), and that function is **never entered**.

**Mechanism (verified, not inferred):** the dispatch gate at `main.py:2977` requires
`action_field == 'context_update' AND raw_signal_type in ('EQH','EQL')`, where `raw_signal_type`
comes from the **payload's own** `signal_type` field. The live alerts never carry that value, so
the condition is False on every fire and sweeps fall through to the generic context path.
**PROOF:** all **304** EQH/EQL rows land with `signal_type='5m_liquidity_ctx'`, and
`signal_type_ctx` — a column written **only** at `main.py:2766`, inside the handler — is NULL on
**304 of 304**. The handler has not run once since the alerts went live in May.

Restoring reachability is a **one-line change** (`classify()` already maps `Equal Highs →
LIQUIDITY/SHORT/eqh/0.9`), which is exactly why it is dangerous: anyone "repairing" dead-looking
dispatch code would **silently arm a rule that loses −971 on the clean sample** and destroys the
short side by closing winning shorts early on an EQL (vpos 58 −435, vpos 50 −403).

**STANDING DECISION: leave BOTH the flag and the routing EXACTLY as they are.** Do not set the
flag to `False` either — it changes no behaviour and would make a future reader think the rule was
evaluated and merely switched off, destroying the knowledge this entry exists to preserve.
The unreachable branch has been protecting the book **by luck, not design**.
Evidence: `reports/2026-07-27-0038-eqh-eql-sweeps-tested-and-killed.md`

### 2.7 Anthropic API key — exposed 20 days, rotation DECLINED
Leaked in plaintext to a world-readable sensor log for ~20 days. **Operator declined rotation** —
the server is single-user with no other access.
**Done:** root cause fixed on both bots (`set -a; . <env>` replaced with a scoped `_env_get()`
parser), logs purged, all sensor logs `chmod 600`, nginx `noquery` log format stops the webhook
passphrase reaching the access log.
**Revisit only if a second user or external access ever exists.** Not an open task today.

### 2.8 🔴 BEHAVIOURAL CHANGE — WATCH ENTRY FREQUENCY (opened 2026-07-29, `7285c5d`)
**WATCH, do not act.** The entry advisor now sees `ABSENT` tiers and an honest agreement line where
it was previously told *"The 3 timeframes are aligned (confluence has already passed)"* — a sentence
that was **false** on 14 of 59 executed entries, printed directly above `15m: n/a`.

**It may skip entries it would previously have approved.** That is the expected consequence of
removing a false statement, **not a regression** — but it must be **measured, not assumed.**

**The measurement, over ~2 weeks from 2026-07-29 11:36 UTC** (restart time; compare against the
equal-length window before it):
- the advisor's **skip rate** — `ai_skipped / (ai_skipped + executed)` on rows that cleared the score gate
- the **executed-entry count**

Baseline for the prior period, already computed: over 2026-07-06 → 07-29, **610** signals cleared
the score gate and **17** became trades = **2.79%**. 14 of 59 executed entries ever (24%) carried
the false alignment claim.

**Do not "fix" a drop by reverting.** A lower entry count with the same or better P&L is the
intended outcome. Only a drop **to near zero**, or a drop with **no change in the quality** of what
survives, is evidence of a defect.

### 2.9 TWO REGISTRIES HOLD THE SAME FACT AND DISAGREE — BY DESIGN. NOT PROPOSED.
`state_machine`'s 15m slot and `signal_matrix`'s MOMENTUM category both record "the 15m tier", and
they **diverge in both directions**:

| | `state_machine` 15m slot | `signal_matrix` MOMENTUM |
|---|---|---|
| TTL | **4 h** | **90 min** (cut 240→90 on 2026-05-20) |
| wiped by 1H flip / Group-B Exit | **YES** (`_clear_lower_tfs_locked`) | **NO** |
| read by | the **prompt** | the **score gate** and the HTF cascade |

Measured on the last 20 executed entries: **2** had an empty slot while the matrix held **3 live**
MOMENTUM signals; **6** had a live slot the matrix had already expired.

**`7285c5d` reports BOTH rather than picking one** — a tier the gate did not count says so, and a
tier whose slot and matrix directions disagree says so. **Reconciling the two registries is a
cascade-state change and is NOT proposed.** Anyone tempted should first read §2.8: the divergence is
also what makes the honest `ABSENT` rendering necessary.

### 2.10 AGE IS THE AGE OF LAST SET, NOT OF FIRING
`reset_1h_trend()` sets `direction = NEUTRAL` and **overwrites the slot `timestamp` with the reset
time while keeping the signal name.** So a reset tier's age is the age of the **reset**, not of the
signal. Live example — entry 19021: the prompt read *"1H trend set by: Trend Catcher Down, weight
1.0, set 1.0h ago"* when *Trend Catcher Down* had actually fired **2.0h** earlier (23:00:16) and an
Exit Signal had neutralised the tier at 00:00:29.

**`7285c5d` labels it `last set` rather than lying**, and now also prints the direction, so a reset
tier shows as `NEUTRAL` instead of reading as live. **A proper fix needs a separate `set_at` field
in `state_machine`, written only when a NEW signal arrives and preserved across resets — a
cascade-state change, out of scope, deliberately not done.** Recorded here so it is not rediscovered.

### 2.12 ✅ CLOSED 2026-07-29 (`c307bb7`) — the exit prompt's false trail promise
The close prompt ends with *"The stop and trail remain active if you HOLD."* **The trail arms at
+1R.** Of the 59 exit consultations ever made, **56 (94.9%) happened with MFE below 1.0R**, i.e. no
trail existed at all. The sentence asserts a protection that is not there, **in the direction that
makes holding look safer than it is.**

Replaced with a block computed **per consultation** from the position's own management state
(`breakeven_applied`, read not inferred): ARMED / NOT ARMED / unreadable, the live stop and its
distance in R, and — when not armed — the exact price that would arm it. Facts only.

Live proof, row 19460, 2026-07-29 13:30:08, trigger `armed_exit`:
> *If you HOLD: the stop-loss is in place. The trailing stop is NOT ARMED — it arms only at +1R,
> which this position has not reached, so the stop is the only protection. It would arm if price
> reaches 64864.7 (+1R). Current stop: 63129.9 (+1.19R away).*

The dormant legacy `_CLOSE_SYSTEM` carried the same falsehood and was corrected to a true statement
in the same commit. **See §2.18 for the contamination this created in the §2.4 sample.**

### 2.13 ✅ CLOSED 2026-07-29 (`c307bb7`) — the ADX "~<20-23" claim and the rule built on it
It appears twice: as a label in the volatility block (`claude_advisor.py:334`) and **inside the
FLAT-MARKET GUARD soft rule** in `_ENTRY_SYSTEM`. A textbook ADX cut-off, asserted to the model as
fact, never validated on this book — and **contradicted by our own measurement**: the 2026-07-29
regime study found that on skipped signals ADX 25–30 drifts **−0.34%/24h** while ADX < 20 drifts
**+0.46%** (t = +2.94). High ADX marks the skips that were RIGHT.

Same class as "Massive" (§2.3) and the same failure mode that forced the counter-short caution's
retirement (§4.5): a number nobody re-checked — except this one was never checked at all.

**RETIRED.** The label and the entire FLAT-MARKET GUARD soft rule are removed.
🔴 **DELIBERATELY NOT REPLACED WITH ANOTHER NUMBER** — we have no validated one, and a second
unvalidated threshold would repeat the defect with a new value. The advisor still sees every ADX,
ATR% and EMA-gap figure, raw, on every timeframe; it is no longer told what they mean.
`ADX_BELOW_FLOOR`, the post-entry recheck, the score gate and the cascade are untouched — this was
prompt text only. **Do not reintroduce a threshold without a study and a review date.**

### 2.14 ✅ CLOSED 2026-07-29 (`41c4a4d`) — `Long/Short ratio` line DELETED
`mc_ls_ratio` is NULL on **all 18,505** `trades` rows. Three references exist in the entire
codebase: the column declaration (`main.py:220`), the parameter default (`claude_advisor.py:241`)
and the render (`claude_advisor.py:363`). **There is no fetcher.** Siblings `mc_recent_liq_long_usd`
and `mc_recent_liq_short_usd` are equally empty.
**DELETED rather than implemented**, by operator decision: a field that has never had a producer is
not a feature we are missing. `_ENTRY_SYSTEM` no longer claims the model receives it; the `ls_ratio`
parameter stays in the signature and is ignored so both `main.py` call sites remain valid.
Verified on the first real entry after the change (vpos 85, trades row 19468): the string `n/a` now
appears **nowhere** in the entry prompt.
The siblings render nowhere — `market_context.py` already records that BingX removed the REST
liquidation endpoint on 2026-05-15. Nothing to delete there.

### 2.15 ✅ CLOSED 2026-07-29 (`41c4a4d`) — two sensors EXPIRED, one EDGE-TRIGGERED
- `regime-FLAT high-ADX` — **5 / 12 and the arrival rate is ZERO**: 0 in the last 7 days, all 5 rows
  sit in the 14–21 day band of a rolling 21-day window and **age out this week, so N goes DOWN**.
  Its predicate needs `trend_4h='bull'`, which fell from 34.9% to **7.9%** of rows. **A rolling
  window with a fixed threshold can never fire when arrivals < expiries.**
- `chop-short` — **0 / 5**; the cohort has produced 2 rows in two months and **0 since the FLAT
  floor**. At 0.7 closed positions/day this is a multi-month wait.
- `titan_bull_regime_watch` — **fires EVERY day** (157, 54, 56, 56). Its question is answered; it is
  now a daily Telegram generator, and noise is how a real alert gets missed.

**DONE 2026-07-29 (`41c4a4d`):**
- 🔴 **Both starved sensors now carry `EXPIRES 2026-09-30`** with the delete-if-not-reached rule
  **enforced by the script itself**: after that date each stops measuring, sends one
  *"DELETE the script and its cron line — do not extend the date"* Telegram, and exits. Verified by
  dry-running both at a simulated 2026-10-01. **The date is deliberately the SAME as the volume
  ceiling (§2.5): one expiry review to remember, not three.**
- **`titan_bull_regime_watch` is now EDGE-TRIGGERED** — it fires once on the TRANSITION into the
  bull regime and logs the transition out, instead of firing on the standing condition every day.
  State in `.state_bull_regime_watch` (delete the file to re-arm). Verified: first run fired, second
  run stayed quiet. Redefined rather than retired because the question it watches — the LONG regime
  drill, which needs a real daily uptrend — is still genuinely open.

### 2.16 THINGS ACCUMULATING WITH NO ANALYSIS PLAN
| table | rows | plan |
|---|---|---|
| `position_excursion_samples` | 2,885 | ✅ **§2.2 Variant C RUN 2026-07-29.** In the end the study used real 5m candles rather than these samples (§0 filter 4: never stored extrema for a path question); the table confirmed coverage. |
| `smart_exit_dryrun_samples` | 245 | the chop-exit re-cut (`config.py:293`) has **never been done** — 🔴 **AND ITS `adx_1h`/`adx_15m`/`adx_5m` COLUMNS ARE BIASED ON EVERY ROW WRITTEN BEFORE THE §2.26 FIX.** See the contamination ledger in §2.26. Re-cut on `adx_window = 200` only, or exclude ADX from the cut entirely |
| `skip_drift_samples` / `skip_attribution` | 38,480 / 7,696 | used ad hoc; no standing plan |
| `post_exit_drift_samples` / `post_exit_observatory` | 185 / 38 | **no plan recorded at all** |

### 2.20 🔴 NEW — THE FIVE CRON SENSORS ARE NOT UNDER VERSION CONTROL
Found while committing `41c4a4d`. `.gitignore` is deny-all-then-whitelist and only admits
`titan-bot/**/*.py`, so **every `*.sh` sensor is untracked**:
`titan_bull_regime_watch.sh` · `titan_regime_flat_high_adx_watch.sh` ·
`titan_chop_short_flat_gap_watch.sh` · `titan_volfloor_data_watch.sh` (+ the Mercury-SOL ones).

Consequences, all real:
- **No history.** `d12e276` records "retire 3 sensors, redefine 2" in its message, but the actual
  predicate changes are in **no diff anywhere**. The only record of what a sensor used to measure is
  prose.
- **No rollback.** Today's three sensor edits (edge-trigger + two expiries) exist **only on disk**.
  They are verified working — each was executed before and after — but they are not in `41c4a4d`,
  which contains `claude_advisor.py` alone.
- ⚠️ **Disclosure:** I made `.bak_20260729` copies before editing and then deleted them in the same
  step that staged the commit. Since the files are untracked, **the pre-edit versions of those three
  scripts no longer exist.** The edits are additive and verified; nothing is broken. But the undo is
  gone, and I should not have removed backups of files git was not holding.

**Recommendation (NOT applied — changing `.gitignore` is a repo-policy decision):** whitelist
`!titan-bot/**/*.sh` so the watch-list machinery is versioned like everything else. Until then,
treat the sensor scripts as production code with no safety net.

### 2.19 ✅ `entry_tiers_json` WRITE PATH — VERIFIED LIVE 2026-07-29
The gap flagged in the `7285c5d` and `4fc89ea` reports is closed. **vpos 85 (trades row 19468,
2026-07-29 13:50) is the first entry executed since the tier work**, and `entry_tiers_json` is
present and correct: all three tiers with name, direction, weight, age and the agreement line,
JSON round-tripped. The rendering was already verified; the persistence now is too.

⚠️ **One observation from that same entry, recorded as a FACT, not a finding (n=1):** the prompt
stated *"Agreement: 5m points LONG; 15m points SHORT; vs the proposed LONG: 5m agree, 15m OPPOSE"*,
and the advisor's reason came back *"1h/15m/5m agree on upside"* — it asserted an agreement the
prompt had explicitly denied. The tier block did its job; the advisor contradicted it. **One entry
proves nothing about advisor quality — but this is exactly the disagreement that was INVISIBLE
before `7285c5d` and is now auditable on every entry.** Worth watching alongside §2.8.

### 2.17 ✅ FOUR SILENT DRYRUN FLAGS — TRACED AND CLEARED (not a defect)
`WALL_ANCHOR_DRYRUN_ENABLED`, `TREND_REVERSAL_EXIT_DRYRUN`, `DXY_HALT_DRYRUN` and
`FILTER_ENFORCEMENT_DRYRUN` are all `True` and produced **zero journal output in seven days**, which
looks exactly like the EQH/EQL signature (§2.6). **They are not the same thing.** Each was traced to
its consumer and each is REACHABLE code inside a **condition-gated** branch:

| flag | consumer | why it is silent |
|---|---|---|
| `WALL_ANCHOR_DRYRUN_ENABLED` | `virtual_trader.py:1424` | prints only when `wall_route == 'wall'` — i.e. only when a qualifying wall would actually anchor the stop |
| `TREND_REVERSAL_EXIT_DRYRUN` | `main.py:3142` | inside the reversal-exit branch; needs a signal in `CONFIRMED_REVERSAL_IDS` |
| `DXY_HALT_DRYRUN` | `risk_manager.py:228` | inside the DXY-halt branch; fires only when DXY would block |
| `FILTER_ENFORCEMENT_DRYRUN` | `main.py` | fires only on a filter match |

**Silence here means the condition has not occurred, not that the code is dead.** Recorded so the
next sweep does not re-raise it. Contrast §2.6, where the gate condition is *structurally* False on
every fire.

Two empty tables are likewise **explained and not defects**:

`breakeven_jobs` and `mfe_tracking` are **live-path only** (§1). `liquidity_sweep_state` being empty
is a **second independent proof of §2.6** — its only writer sits inside the handler that never runs.


### 2.18 🔴 THE PRE-`c307bb7` EXIT VERDICTS ARE CONTAMINATED — §2.4's COUNT RESTARTS
**All 59 exit consultations recorded before `c307bb7` were produced under a false statement**, and
**56 of them (94.9%) carried it in the form that mattered**: the prompt asserted *"The stop and trail
remain active if you HOLD"* while the trail was not armed, i.e. it promised a protection that did not
exist. The bias has a **known direction — toward HOLD.**

**DECISION: the §2.4 activation criterion restarts its count from `c307bb7` (2026-07-29 13:21 UTC).
Progress resets from 2 of ~10 to 0 of ~10.** Reasoning, and the honest caveat:

- The criterion was written down **in advance specifically so the bar could not be moved after seeing
  results**. A sample generated under a known, directional bias is exactly what that discipline
  exists to exclude. Keeping it would mean the first thing we ever did with an un-gameable criterion
  was to accept evidence we know was skewed.
- Both closed datapoints are affected. vpos 82 received **no** `close` verdict at all — precisely the
  outcome a hold-bias produces. vpos 83's first `close` came at 04:00:51 while the position was
  below +1R, i.e. under the false promise throughout.
- **The caveat, stated because it cuts against the decision:** discarding vpos 83 throws away the
  datapoint that FAVOURED the advisor (+23.61 vs the actual −135.80, ~+159 USDT). Restarting is
  therefore **conservative against the advisor**, not for it. It also means a truthful prompt might
  plausibly have produced an EARLIER close on vpos 83 — better still — so the bias may have been
  costing the advisor credit rather than lending it. That is speculation; the direction of the bias
  is knowable, its effect on any single verdict is not, and a criterion this deliberate should not
  rest on a guess either way.

**I agree with the operator's view. Restart the count.** The 59 pre-fix consults keep their value as
a record of what the advisor said and why — they are simply not admissible evidence for the
go-live decision.

**Do not re-cut this sample later to reach ~10 sooner.** That is the same move the criterion forbids.


---

### 2.19 ✅ EXIT-SIDE PERCENTILE CROSS-SOURCE — FIXED `625fedc` (2026-07-30) + the guard that keeps it fixed
`_build_exit_context` fetched walls from `microstructure.fetch_pre_trade_walls` (**BingX, depth 100,
contracts**) and ranked them with `_exit_pct` against `orderbook_density` (**OKX books-full 4000,
USDT**). OKX imbalance sd **0.046** vs BingX depth-100 sd **0.238** — five times wider — so a foreign
value pins to 0 or 100. Live proof on vpos 86 at 00:50:20: `Imbalance = 0th pct` (truth **62nd–69th**),
`Opposing wall = 93th pct` (truth **~50th**); the advisor cited the phantom wall to justify HOLDing.
Depth (`6th pct`) was the one correct figure — always read straight from `orderbook_density`.

**The entry path never had this bug** (`_entry_book_pct`); that pattern was **copied**, not
re-invented. The exit side now reads the same `liquidity_zones.fetch_pre_trade_walls` OKX snapshot.

🔴 **The trap in the obvious fix, recorded because it nearly shipped:** `entry_sup_wall_mult` /
`entry_ob_imbalance` are **BingX** values written at fill. Pairing them with an OKX "now" would have
re-created the defect one line lower — vpos 86's stored **0.2914** against a live OKX **0.5008**
renders as a dramatic **FLIPPED that never happened**. The entry reference is therefore taken from
the `orderbook_density` row nearest the fill (**21 s** for vpos 86), bounded ±10 min, age printed.
**Fixing one seam must not open the next one.**

**STRUCTURAL GUARD — `_exit_pct(col, value, source)`:** `source` is a **required positional argument**
*and* is **ANDed into the SQL WHERE clause**. Required-positional means a caller that has not thought
about provenance cannot write a working call (`TypeError` at the call site). In the predicate means
even a **wrong** source string cannot borrow another book's distribution — it gets that book's rows
or none. `bingx_depth100` matches **zero** baseline rows, so a BingX percentile is **unobtainable**,
not merely omitted. A figure that cannot be ranked is rendered **RAW, with its source named and no
percentile**, and the prompt says so in words.

### 2.20 ✅ NO-OP TIGHTEN — FIXED `838481f` (2026-07-30). Two consequences, one unasked question.
The `93c20c3` bound makes `new_sl == current_sl` on every pre-breakeven path, and the recheck only
runs pre-breakeven — so **a zero-point TIGHTEN is the NORMAL outcome, not an edge case.** vpos 86 was
the first position to reach that branch since the bound landed, and hit both unfollowed consequences:

1. it wrote `recheck_status='tightened'`, which the poller treats as **terminal**, so **T+60s and
   T+300s never ran — including `EMERGENCY_CLOSE`, the only recheck path with teeth**;
2. it still called `move_stop()`, which **cancels the live exchange stop and re-places it at the
   identical price**. Verified against BingX: order `2082629809867436032` CANCELLED at
   **00:50:31.409**, `2082629881359347712` created at **00:50:31.765** — **356 ms with no protective
   stop on a real $147 short, bought for a stop move of exactly zero points.**

Fixed by asking what the old code never asked: **did the number actually change?** If not, touch
neither the exchange nor the tier ledger; record the advisory and write `t+{tier}_ok` so later tiers
stay due. Compared **at exchange precision** (`price_to_precision` both sides), no epsilon: the first
draft used `entry_price * 1e-7`, safe at every price we trade but scaling with price while BTC's tick
is fixed at 0.1 — **it equals one tick at BTC $1M**, where a real one-tick tighten would read as a
no-op. **If an epsilon needs defending, remove it rather than calibrate it.**

`'tightened'` **stays terminal for a real move.** The defect was never that it is terminal; it was
that **a no-op was recorded as one**. **NOT retroactive:** vpos 86 keeps `'tightened'` and no tier
fires late — its T+60s/T+300s windows elapsed ~00:51 and ~00:55, and an `EMERGENCY_CLOSE` on an
hour-old health read is not what that tier is for. Elapsed windows stay skipped **by construction**.

### 2.21 🔴 OPEN QUESTION — book DEPTH is the most extreme reading nobody weights
At vpos 86's entry, depth was **2,440 BTC = 6th percentile** of 24,001 snapshots — **the single most
extreme book figure of the trade**, and the one percentile computed **correctly** even before
`625fedc`. Shown accurately to **both** advisors: the entry advisor (*"Book depth: 2,440 BTC — 6th
pct"*) executed at 0.82; the exit advisor saw it and held.

**No gate reads depth on any path.** Collected every 60s, rendered into two prompts, stored in two
tables — weighted by nothing. Either it should carry weight somewhere, or we should stop rendering it
as though it does. **A question, not a plan** — it needs its own study.

### 2.22 ✅ THREE CARD LABELS — FIXED `957f980` (2026-07-30), display only
Fourth, fifth and sixth instances of *"check not only what the gate DECIDES, but what it SAYS"*.
- **`LIQUIDITY` → `5M-STRUCTURE`.** The category holds **ten LuxAlgo 5m candlestick signals and ZERO
  order-book inputs**; the book never enters `confluence_score`. The line appeared on **22 of 73
  executed trades** and reads as "the order book was outvoted" — on vpos 86 it sent a live-money
  investigation hunting a book veto that never existed. Renamed via `CATEGORY_DISPLAY_LABEL`; the
  **internal key is untouched** (it is in `matrix_breakdown_json`, read by the optimizer, quoted in
  every past report). **Membership, weights and the minority-zeroing rule deliberately unchanged** —
  whether that rule should fire at all is still open (it silences LIQUIDITY and effectively only
  LIQUIDITY on trades that execute).
- **`Imbalance: 0.31 (Balanced)`** — hardcoded bands, no baseline, no source. At 00:50:1x the machine
  held **three different "Imbalance" values in one minute** under one word: 0.31 (BingX top-20, card),
  0.51 (OKX-4000, advisor), 0.2914 (BingX-100, DB). `_imbalance_label` **deleted**, not deprecated.
  No percentile shown, deliberately: this book has no queryable baseline of its own, and ranking it
  against the OKX one is exactly the §2.19 inversion.
- **`Trend Strength (ADX): 25.87`** — no timeframe, and it was the **5m** value, the one TF no gate
  reads. The 1h then was **11.1, below the FLAT floor of 20**; the recheck scored that same value −5
  eleven seconds later. Now prints `ADX 5m: 25.87 | 1h: 11.12 ← the gates read this`.

### 2.23 ✅ THE ADVISOR'S OFF-SWITCH ALSO SILENCED IT — FIXED `81875c9` (2026-07-30 11:32, LIVE)
**Found 2026-07-30 11:05 while preparing exactly the one-line flip this item forbade.**
**Approved and shipped 11:32 — the advisor is now ARMED. `EXIT_ADVISOR_DRYRUN = False`.**
`EXIT_ADVISOR_DRYRUN` reads as "record the verdict, do not act on it". It is **two switches wearing
one name**, and the second one is wired backwards.

Both live consult sites gate on the flag being **True**:

```
virtual_trader.py:2149   if EXIT_ADVISOR_HOURLY and EXIT_ADVISOR_DRYRUN:          # 8 of 9 verdicts
main.py:3444             if EXIT_ADVISOR_ON_15M_CONFIRM and EXIT_ADVISOR_DRYRUN:  # 1 of 9 verdicts
```

**Setting `EXIT_ADVISOR_DRYRUN = False` deletes both consults.** No prompt, no verdict, no row, no
close. The advisor would have gone **silent**, and the silence would have looked like activation.

The **only** site where the flag behaves as its name promises is `main.py:2787`, the early return
inside `_handle_5m_close_via_ai` — the one path with a close mechanic past it. That path is reached
**only** by a 5m Group-B webhook, and:

| | |
|---|---|
| `5m_group_b` rows in `trades`, all time | **0** |
| `5m_group_b` rows since vpos 86 opened | **0** |
| exit-advisor consults recorded, all time | 77 — **none** from this trigger |

**The codebase already knew.** `config.py:232` says so, eight lines above the flag:
*"its trigger is a 5m Group-B alert and **zero have ever arrived** — the operator has decided NOT to
create a 5m exit alert, so this stays true."* That sentence was written to explain why the advisor
never got consulted; nobody re-read it as a statement about where the advisor could **act**.

**Net effect of the one-line flip, had it been applied:** the advisor stops speaking on the two
triggers that work, and gains permission to close on a trigger that has never fired in the bot's
history. **Strictly worse than DRYRUN — it forfeits the observation and buys no action.**

**A second defect on the same path, found with it:** in LIVE mode `_handle_5m_close_via_ai` finds the
position via `_fetch_open_position` (the exchange), so `_vpos` is `None` and it calls
`claude_advisor.consult_for_close(...)` — **the old, unenriched consult with no book block at all**,
not `consult_exit_advisor`. So the one close-capable path would also have been judging on a
different, poorer prompt than the 77 verdicts §2.4 was built on.

**THE CLASS, and it is the FOURTH instance in four days:** *the label does not say what the thing
does.* §2.19 (percentile ranked on another book's scale), §2.20 (a no-op TIGHTEN recorded as
terminal), §2.22 (three card labels), and now a flag whose name describes one of its two effects.
**The `957f980` lesson was "check not only what the gate DECIDES but what it SAYS." This is the
inverse and it is worse: the flag says the right thing and DOES a second, unnamed thing.**

**Guard shipped with the fix:** the two consult gates now read `EXIT_ADVISOR_HOURLY` /
`EXIT_ADVISOR_ON_15M_CONFIRM` alone — the flags they are named for — and `EXIT_ADVISOR_DRYRUN` is
read **only** where a verdict is acted on. The log prefix `[EXIT-ADVISOR-DRYRUN]` becomes
`[EXIT-ADVISOR-LIVE]` when it can act, so the journal cannot claim DRYRUN next to a real close.

**LABEL DEBT — A DELIBERATE CHOICE, NOT AN OVERSIGHT. Operator-approved 2026-07-30 11:28.**
The verdict row's `trades.status` stays **`exit_ai_dryrun`** even when the advisor acts, and the
string is now inaccurate on purpose. **The reason: renaming it forks the 77-row audit trail that
§2.4 is cut from** — every historical verdict carries that status, and a rename would split the
criterion's own sample across two labels for a cosmetic gain.

**Read it as the name of the CHANNEL, not as a claim about what happened.** It means *"a row on the
exit-advisor verdict channel"*. Whether that verdict was ACTED on is a different fact, recorded in a
different place: **`virtual_positions.close_reason='ai_exit'`**, which is the separable field and the
one every future cut should use.

🔴 **The next reader must not treat this as a lie, and must not "fix" it casually.** If a second
consumer is ever written that reads `exit_ai_dryrun` as *"the advisor did not act"*, that consumer
is wrong and this note is the reason why — fix the consumer, or migrate all 77 rows at once and
update §2.4's query in the same commit. **Do not rename it for one new query.**

### 2.24 ✅ THE THREE THINGS CONFIRMED IN THE SAME APPLY (operator's conditions, `81875c9`)
1. **`_emergency_close` is NOT collateral.** It calls
   `main._execute_close_position(symbol, position_side, _from_adapter=True)` — untouched by the
   reorder, which moved a block *inside* that function. It still reaches the RAW mechanics via
   `_from_adapter=True` (mandatory: it fires before the `virtual_positions` row exists, so
   engine-routing would find no row and return `None`, leaving a real position open with no stop).
   **Under the new ordering its behaviour is identical**: it fires precisely when the stop FAILED to
   place, so the cancel loop has nothing to cancel and is a no-op under *either* ordering. In the
   sub-case where a stale order does exist, the new ordering is strictly better — the close now
   happens before any cancel.
2. **The fetch guard is still FIRST.** Proven by position in the shipped function:
   `_fetch_open_position` line 39 → `return None` line 41 → `create_market_order` line 63 →
   `fetch_order_fee` line 69 → cancel loop line 78/87 → `_cancel_stop_orders` line 95. **A position
   that closed between ticks is returned as `None` and never traded against.**
3. **5m Group B was REPOINTED, not disabled** — operator's choice of the two offered. It now asks
   the engine for its own row (`virtual_trader._open_position`) and calls `consult_exit_advisor`,
   the same enriched prompt as the hourly and 15m triggers. The unenriched `consult_for_close`
   survives only for the case it was always right for: **no engine row exists at all.** Its close
   also now stamps **`ai_exit`** instead of `external` — `_execute_close_position` gained an explicit
   `reason` parameter defaulting to `'external'`, so **no existing caller changes stamp.**
   *Rationale for repointing over disabling:* a dormant path is not a dead one, and the failure mode
   of leaving it was a close-capable trigger judging on a weaker prompt than the sample the
   criterion is built from — which is precisely how this session's defects were seeded.

### 2.25 ✅ THE STOP FIRED — §7 UNCERTAINTY 1 CLOSED, no revert condition met (2026-07-30 11:50:47.9)
vpos 86's `closePosition='true'` `STOP_MARKET` triggered for the FIRST time in this bot's history.
Verified from the venue on both probes: **SHORT exactly ZERO** (no residual, no reversal), **exactly
ONE `closePosition` order on the symbol**, **zero orphans** of any type, and the stop filled the
**WHOLE 0.0023** in one child order (`avgPrice 64733.0`, `commission 0.074443`, `profit −2.4081`).
Row finalised by the **PASSIVE** path (item 13, first real firing, ~1.1 s detect-to-reconcile) from
the REAL order — price and fee **read back**, not estimated (`[BE-FILL] … ESTIMATED` absent). §1a's
revert conditions stay on the page and were NOT triggered. `reason='sl'` decided from the row's own
`breakeven_applied=false`. §7 uncertainty 3 → **n=4, 0 failures** (a rate still cannot be estimated).

🔴 **Three residuals, stated rather than closed with the item:**
1. **`fetch_order(<trigger id>)` returns a DIFFERENT order id** — the child execution, with
   `triggerOrderId` back-pointing. Reconciliation depends on BingX resolving trigger→child. If it ever
   returned the trigger object instead (no `avgPrice`), `read_filled_protective_order` falls through
   to `fetch_ticker(...)['last']` and books an **invented** exit price. No guard exists.
2. **The passive path runs NO orphan sweep** — `_reconcile_passive_fill → _do_close` never reaches
   `_execute_close_position`, so neither the cancel loop nor `_cancel_stop_orders` runs. Harmless in
   *this* configuration (the stop was the only order); a TP or DCA limit would be left behind.
3. **The 34-point favourable gap is NOT systematic.** Trigger 64767.1 on MARK, fill 64733.0 on BingX's
   book. Measured basis over **1,000 paired 1m mark/last candles**: mean +0.41, **median 0.00**, sd
   3.02, and max **+6.1** on the 20 high-volatility minutes. The 34 pts is a transient inside a
   **+175 pt / 60 s, 198 BTC** spike; **the sign is not guaranteed** (a BingX-led move triggers LATE
   and fills WORSE). **Do not conflate with §1's "+36.91 over 101,739 candles"** — different
   mechanism. BingX's finest kline is 1m and the event lasted 926 ms, so which side led is
   unobservable after the fact. **Cheap fix, NOT built:** log
   `(trigger_price, fill_price, mark_at_fill, last_at_fill)` on every stop fire.

### 2.26 🔴🔴 ONE ADX, TWO WINDOWS — AND THE DIFFERENCE IS RENDERED AS A CHANGE (§2.19's class, 4th place)
**The entry path computes ADX on 200 candles; the post-entry recheck and the exit-advisor sampler
compute it on `ATR_LEN * 3 = 42`.** ADX(14) is DOUBLY Wilder-smoothed, so 42 bars has not warmed up.

| path | fetch | value, same instant |
|---|---|---|
| entry snapshot | `indicators._fetch_ohlcv_cached(..., CANDLE_LIMIT=200)` | **13.83** (converged; 300 bars = 13.834) |
| **recheck** `virtual_trader.py:1541` | `fetch_ohlcv('1h', limit=ATR_LEN*3)` = 42 | **25.64** |
| **exit sampler** `virtual_trader.py:1805` `_tf_metrics_safe` | same 42 | same |

**Live tell — vpos 87, 13 seconds apart:** `virtual_positions.entry_adx_1h = 13.5163` vs
`recheck_events` id 37 `adx_1h = 25.3505`.

**Scope is TIGHT and was checked, not assumed — it is ADX and ONLY ADX.** Same two windows: ATR 1h
314.4 vs 317.4 (−0.9%), `trend` identical, `ema_gap` 0.3551 vs 0.3548. ADX 1h **+44%**, ADX 15m
**+4.3 pts**. The comment at `virtual_trader.py:683` — *"Wilder is window-sensitive, so faithful
alignment needs the same limit"* — is right, was written for ATR, and is **violated for ADX**.

**Magnitude, 800 paired readings over 1,000 real 1h candles:**
```
ADX42 − ADX200 : mean +6.23  median +5.38  sd 10.04  min −22.29  max +52.16
  |diff|>5 : 484 (60.5%)   |diff|>10 : 285 (35.6%)   ADX42 > ADX200 in 593/800 (74.1%)
ADX_BELOW_FLOOR = 20 :  truly <20 (200-bar) 221 of 800
  MISSED (true<20, 42-bar>=20) : 117  ->  52.9% of every true-below-floor state
  FALSE  (true>=20, 42-bar<20) :  56          agreement rate 78.4%
```
🔴 **`ADX_BELOW_FLOOR` misses more than half the states it exists to catch** — and it is worth −5 with
`HEALTH_SCORE_TIGHTEN = −5`, so that rule ALONE decides TIGHTEN. Its companion `adx_drop` computes
`entry_adx (200-bar) − cur_adx (42-bar)`, so a systematically-high `cur_adx` makes the difference
systematically negative: **both ADX rules in the recheck are biased toward "healthy".**

🔴 **It reaches the exit advisor as a fabricated trend.** vpos 87's stored exit prompt, verbatim:
```
Regime at ENTRY vs NOW
  At entry: regime=TREND 1d=neutral 4h=bull 1h=bull ADX1h=13.5     <- 200-bar
  Now:      15m=bull 5m=bull ADX1h=25.4 ADX15m=46.8                <- 42-bar
```
The prompt asserts an **11.9-point rise across 25 seconds that did not occur**, under a heading saying
the two are comparable — and the advisor read it that way: *"Regime strengthened."* vpos 86's row
19590 (*"bearish regime (ADX rising to 14.9)"* against an entry of 11.1) is the same artefact.

**Why §2.19's guard could not catch it:** `_exit_pct(col, value, source)` makes **book** provenance
mandatory. Nothing makes **indicator-window** provenance mandatory. All **228+**
`smart_exit_dryrun_samples` rows carry 42-bar ADX, so §2.16's chop-exit re-cut would run on biased data.

**Shape of the fix, NOT applied (read-only session, awaiting the operator):** one window per
indicator — route both paths through `_fetch_ohlcv_cached(..., CANDLE_LIMIT)` — plus a provenance
guard of the §2.19 shape so a window cannot be borrowed silently. **Consequence for the live
position:** vpos 87's true ADX1h is 13.5, under the floor; on the entry window all three recheck tiers
would have scored **−5 → TIGHTEN**. The three `Health 0 / verdict OK` readings are artefacts — **and
that is also why §2.20's no-op-TIGHTEN fix is still UNEXERCISED in live** (11 of 14 positions with
recheck rows already ran all three tiers; only vpos 74 and 86 ever stopped at T+10, both on a TIGHTEN).

#### 2.26a ✅ **APPLIED, COMMITTED `1161802`, LIVE 2026-07-30 14:11:12 UTC** (approved by the operator)
Snapshot `/root/backups/pre-adx-window-fix-20260730-140811/` (4 sources + `config.py` + `trades.db`).
**4 files, +441 / −40** — the extra 37 lines over the reviewed +404 are the `sensor_events` migration
fix found during the pre-restart audit (§2.34), applied in the same commit. Two halves:

**A · ONE WINDOW FOR ONE INDICATOR.** New `indicators.ADX_CANDLE_LIMIT = CANDLE_LIMIT` (by *identity*,
so the entry reference and every later reading are one measurement rather than two literals kept in
step by hand) and `indicators.adx_reading(exchange, symbol, tf)` — the only sanctioned way to read an
ADX. It routes through `_fetch_ohlcv_cached`, so at T+10s it re-reads the bytes the entry snapshot
cached ~13 s earlier: same value, **no extra request**.
🔴 **ATR IS UNTOUCHED, and that was the trap.** `entry_atr_pct_1h` is derived from `execute_entry`'s own
`ATR_LEN*3` 1h fetch, so moving ATR to 200 would have broken `atr_contraction` by changing ONE side of
its comparison. Both `_recheck_fetch_1h_metrics` and `_tf_metrics_safe` now make **two** fetches on
purpose — ADX on the converged window, ATR/vol_ratio/trend/ema_gap on the calibrated 42-bar one.
Verified live on all three TFs: ATR% **byte-identical**, `trend` identical, only `adx` moves
(1h 21.92→15.09, 15m 45.68→45.13, 5m 33.63→32.54).

**B · THE PROVENANCE GUARD, §2.19's SHAPE.** `indicators.AdxReading(value, window, tf)` — a NamedTuple
with **no defaults**, so a reading cannot be built without stating all three (the required-positional
half). `adx_delta()` **refuses** across windows or timeframes and returns `None`, so the rule SKIPS;
`usable_for_threshold()` demands the sanctioned window, so an unconverged value **cannot be tested
against `ADX_BELOW_FLOOR` at all** (the WHERE-clause half: unobtainable, not merely unlabelled). A
bare float reaches neither. Skips are written into `reasons_json` so a silent skip cannot read as a
passed check. Three new columns persist the window: `virtual_positions.entry_adx_1h_window`,
`recheck_events.adx_window`, `smart_exit_dryrun_samples.adx_window`.
The exit prompt now **refuses to imply a change it cannot support**: when the sample's window is not
the sanctioned one it prints the figure raw and states in words that no rise or fall may be inferred —
§2.19's precedent applied verbatim.

**🔴 THE BEHAVIOUR CHANGE, QUANTIFIED BEFORE IT SHIPS.** Replayed all **38** `recheck_events` rows with
the 200-bar ADX recomputed at each row's own timestamp from real 1h candles (854 candles, 2026-06-25
onward; the forming-candle `iloc[-1]` call reproduced exactly). **Reconstruction of the STORED score
from the STORED inputs: 38/38 exact**, so the replay is validated before it is trusted.

| | |
|---|---|
| OK verdicts today | **36** of 38 |
| **become TIGHTEN on the corrected window** | **9 of 36 = 25%** |
| become EMERGENCY_CLOSE | **0** — min score −6, the emergency floor is −10 |
| TIGHTEN → OK (a rule turned OFF) | **0** |
| difference made by re-enabling `adx_drop` | **NONE** — 9 either way |

**The 9 are three positions, all LONG, all with a true ADX1h under the floor: vpos 82 (16.88, ×3
tiers), vpos 85 (16.81, ×3), vpos 87 (13.83, ×3).** So it is **not** a rule that fires constantly —
**25% of tier runs, 3 of 14 positions** — and the answer to "are we turning on something that fires
all the time" is **no**.

🔴 **AND WHAT A TIGHTEN ACTUALLY DOES HERE MATTERS MORE THAN THE COUNT: nothing, on the exchange.**
The recheck only runs pre-breakeven, where the `93c20c3` bound forces `new_sl == current_sl` — so all
9 become **no-op TIGHTENs**: `t+{tier}_ok` written, later tiers stay due, **exchange stop untouched**,
one advisory Telegram line per tier. In practice this converts 9 silent `OK`s into 9 honest advisories
and **moves no money**. It also, finally, **exercises the §2.20 branch that has never run** — which is
the point the operator predicted, and it is why the ADX fix and §2.20 are one story.

**The `adx_drop` rule and legacy rows — a decision, with its cost measured rather than assumed.**
Legacy `virtual_positions` rows have `entry_adx_1h_window = NULL`, so `adx_drop` **refuses** for
them (including the open vpos 87) instead of comparing across a possibly-mismatched window. Those
values genuinely *were* 200-bar (`fetch_snapshot` is their only producer and `CANDLE_LIMIT` has been
200 in the entire git history of `indicators.py` — one `+CANDLE_LIMIT = 200`, never changed), so a
backfill would be **correct**. It is **NOT done anyway**: asserting provenance from a code invariant
is the habit that produced this defect, and the measured cost of refusing is **zero verdicts across
all 38 rows**. Legacy rows lose a rule that has never once fired.

#### 2.26c ✅ THE OPEN POSITION — what the patch can and CANNOT reach (traced, not asserted)
Asked by the operator before approval. **The patch cannot alter any MECHANICAL management of a
position that is already running.** Proven by reachability rather than by claim:

| patch site | reachable for the OPEN vpos 87? | why |
|---|---|---|
| `indicators.py` | **NO effect on any existing reader** | two hunks only: the `typing` import, and a **pure insertion** (+163/−0). `compute_tf_metrics`, `_fetch_ohlcv_cached` and `fetch_snapshot` are **byte-identical**, so the entry snapshot, the optimizer and the entry advisor see exactly what they saw before |
| `execute_entry` (entry-ADX normalisation + INSERT) | **NO** | runs once, at entry. vpos 87 is already open |
| schema ALTERs (3 columns) | additive, nullable | no row modified |
| `_recheck_fetch_1h_metrics` · `_health_score` · `_run_recheck_tier` | 🔴 **NO — UNREACHABLE FOR LIFE** | `virtual_trader.py:2271-2273` skips the whole recheck block when `recheck_status IN ('done','tightened','closed_critical')`. vpos 87 is **`done`** (all three tiers ran, 12:05:30 / 12:06:24 / 12:10:28). The corrected floor **cannot fire retroactively**, and the patch does not touch that guard — no diff hunk lands within ~200 lines of it |
| `sensor_events.log_recheck` | **NO** | its only caller is `_run_recheck_tier`, unreachable above |
| stop price · breakeven · trail · LONG partial · emergency close | **NOT TOUCHED AT ALL** | no hunk in any of those paths |

**⚠️ TWO things DO reach it, and "only the additive NOTE" would be wrong — correcting the framing:**

1. **The NOTE in the exit prompt** — immediately, because vpos 87's latest sampler row (245, 13:05:31)
   predates the fix and so has `adx_window` NULL. The prompt will refuse the entry-vs-now ADX
   comparison in words until the next hourly sample.
2. 🔴 **The ADX FIGURES THEMSELVES change**, from the first post-fix sampler row onward:
   `_tf_metrics_safe` is reached by the hourly smart-exit sampler for **any** open position, so
   `Now: ADX1h=… ADX15m=…` becomes the converged reading (~15.1 instead of ~22.3 on 1h) and the NOTE
   then disappears because the two sides finally match. **That is the fix working, not a side effect** —
   but it means the patch does change an input the advisor reads on a running position.

**AND THE HONEST CONSEQUENCE OF THAT, since `EXIT_ADVISOR_DRYRUN = False`:** a different verdict on
vpos 87 is possible, and a `close` verdict closes it. **Direction of the change is toward LESS spurious
confidence in holding:** the advisor was being shown a fabricated ADX *rise* (13.5 → 22.3) and read it
as *"regime strengthened"* — a reason to hold a LONG. With the truth (13.5 → ~15.1) that support is
gone. The sampler itself drives no exit: `armed` / `would_exit` are computed from price only, and the
table is read by no exit logic.

**Nothing else in the position's contract moves.** Same stop, same 1R, same breakeven level, same
trail, same partial.

#### 2.26b 🔴 CONTAMINATION LEDGER — every ADX these tables hold before the fix is SUSPECT
**Mark, do not re-run.** Nothing is re-analysed here; this exists so no future cut is done in
ignorance.

| table · column | rows affected | what is wrong | how to cut it safely |
|---|---:|---|---|
| `smart_exit_dryrun_samples.adx_1h` / `.adx_15m` / `.adx_5m` | **all 245 existing rows** | computed on `ATR_LEN*3 = 42`; biased **+6.23 mean / +5.38 median** on 1h, +4.3 pts on 15m | `WHERE adx_window = 200`. Post-fix rows carry it; the 245 legacy rows are NULL |
| `recheck_events.adx_1h` | **all 38 existing rows** | same 42-bar window | `WHERE adx_window = 200` |
| `recheck_events.adx_delta` | **all 38 existing rows** | 🔴 **worse than biased — it is a CROSS-WINDOW subtraction**: `entry_adx` (200-bar) − `adx_1h` (42-bar). It is not a measurement of anything | do not use any legacy `adx_delta`. Post-fix rows are refused-or-valid, never mixed |
| `recheck_events.health_score` / `.verdict` / `.reasons_json` | **38 rows** | both ADX rules were biased toward "healthy": the floor missed 52.9% of true sub-floor states, and `adx_drop` was silenced by a systematically-high `cur_adx` | treat every historical `OK` as **"OK, or an unfired ADX rule"**. The corrected replay is in §2.26a: 9 of 36 flip |
| `trades.srv_adx_*` (entry side) | ✅ **clean, all rows** | `fetch_snapshot(limit=CANDLE_LIMIT)` is its sole producer and that literal never changed | usable as-is. **This is why the entry advisor's ADX figures were never wrong** |
| §2.16 chop-exit re-cut | **not yet done** | would have run on the 245 biased rows | do it on `adx_window = 200` only, or drop ADX from the cut |

**Any past analysis quoting a recheck ADX, a recheck `adx_delta`, or a sampler `adx_*` is suspect and
should be re-derived, not trusted.** Known instances in this file and in reports: §2.22's *"the
recheck scored that same value −5 eleven seconds later"* (that one is **correct** — vpos 86's 42-bar
11.271 and its true 11.117 barely differ, which is exactly why the defect hid: at genuinely low ADX
the bias collapses), and every *"ADX rising to X"* / *"regime strengthened"* line quoted from an exit
verdict, all of which are artefacts.

### 2.27 🔴 §2.4 IS CONTAMINATED A SECOND TIME — and vpos 86 produced NINE clean-book `close` verdicts
Contrary to the 11:39 prediction that vpos 86 would contribute zero, it produced **nine `close`
verdicts after the `625fedc` deploy at 02:51:11**, every one on a corrected book block, and **every
one beat the actual exit**:

| row | UTC | px at nearest sample | net if closed | R |
|---|---|---:|---:|---:|
| **19607** | **03:50:29** | 64191.30 | **−1.3092** | **−0.527** |
| 19628 | 06:50:53 | 63961.00 | −0.7793 | −0.313 (best) |
| 19678 | 10:51:14 | 64569.20 | −2.1789 | −0.876 (worst) |
| — | **11:50:48 ACTUAL** | **64733.00** | **−2.541574** | **−1.02213** |

(the other six: 19617 −0.405 · 19624 −0.385 · 19633 −0.322 · 19646 −0.636 · 19649 −0.616 · 19660 −0.858)

🔴 **NOT counted, and the reason is the discipline, not the number.** The criterion says *first*
`close` verdict, *no re-cutting*. vpos 86's first was **01:50:24 — contaminated**. Calling 03:50:29
"the first" is the exact re-cut the criterion forbids. **Both readings, arithmetic done, operator
decides by rule:** STRICT → vpos 86 does not count, §2.4 stays **0 of ~10**. LENIENT → **IMPROVED
+$1.2324 = +0.495R**, §2.4 → 1 of ~10.
**And a new reason to prefer STRICT that has nothing to do with the book: all nine prompts carried
42-bar ADX (§2.26).** A third restart is a decision, not proposed here.
**The operational fact, separate from the criterion:** the advisor said `close` **twelve times over
nine hours**, was mute for eleven of them by `DRYRUN`, was armed at 11:32:45 — and the stop beat its
next turn (`exit_advisor_last_ts` 10:51:11 + 3600 = **11:51:11**) by **23.1 seconds**. Arming was
correct and still bought zero datapoints.

### 2.28 🔴 THE POST-EXIT OBSERVATORY HOLDS GHOST ROWS, and stamped a live outcome onto one
`post_exit_observatory` id **79** says `vpos_id = 86`, but its entry data is **not** vpos 86's:

| field | observatory 79 | `virtual_positions` 86 |
|---|---|---|
| entry_price | **63605.6** | **63686.0** |
| original_sl_price | **64724.6** | **64767.1** |
| opened_at | **2026-07-29T21:50:04** | **2026-07-30T00:50:14** |

Three hours and 80.4 points apart — **two different positions.** `on_entry` upserts with
`ON CONFLICT(vpos_id) DO NOTHING`, so the real vpos 86 wrote **nothing**; `on_real_close` then stamped
today's outcome onto the stale row. The published `exit_advantage_r = +0.42525` therefore mixes a
shadow leg priced off entry 63605.6 with a real leg from a position that entered at 63686.0. On vpos
86's OWN numbers the advantage is **+0.4787R**. Sign survives here; the mechanism can flip one.

Also: id **80** carries `vpos_id = 89` (SHORT, entry 63595.5, orig SL 64714.5, opened
2026-07-29T21:50:11) while `virtual_positions` has **no row 88 or 89** and `sqlite_sequence` is at
**87**; `recheck_events` / `position_excursion_samples` / `smart_exit_dryrun_samples` know only 86 and
87. Both ghosts are stamped **2026-07-29 21:50**.

> 🔴 **CORRECTED 2026-07-30 22:35 — "no row 88 or 89" is true TODAY and false TOMORROW.** This
> paragraph reads as if 89 were permanently vacant; §2.28a made that explicit with *"has no row 89 and
> **never will**"*. **Wrong.** `sqlite_sequence` at **87** is exactly the reason ids **88 and 89 are
> the next two AUTOINCREMENT values to be issued** — the sequence is the high-water mark, not a
> ceiling. Row 80 was therefore two positions away from blocking a real vpos 89.
> **Row 80 has since been re-keyed to `vpos_id = -80` — see §2.28b.**

#### 2.28a ✅ DIAGNOSED 2026-07-30 13:40 — test-harness residue, and **TWO CORRECTIONS to the 13:09 report**
**Read-only. Nothing touched.** The 13:09 report guessed two things about these rows and got both
wrong; the backups and the journal settle it.

🔴 **CORRECTION 1 — row 80 is NOT the naked short's surviving record. It is not the naked short at
all.** The naked short happened in the **FIRST** live window, before the 21:26:52 revert
(`11055e2`). Rows 79/80 are stamped **21:50:04** and **21:50:11**, which is **inside the PAPER
interlude** (21:26:52 → 21:54:16) — proven independently by the 21:53:11 boot banner in the journal:
`🧪 PAPER — simulated fills only ... LIVE_TRADING_ENABLED=False ... margin $2000 x 5`. **So no real
money is implicated by either row**, and the §7 caveat is unchanged and complete: the naked short's
−$0.26 is still recorded only in prose, nowhere in the DB.

🔴 **CORRECTION 2 — row 80 is NOT accumulating; row 79 IS.** Row 80 stopped being writable at
**02:00:14** on 07-30: `on_15m_exit_signal` updates only
`WHERE shadow_exit_at IS NULL AND status IN ('shadow_armed_pending_close','shadow_armed_post_close')`,
and row 80 now has `shadow_exit_at` set with `status='shadow_pre_close'`, so it can never match again;
its drift slots can only be seeded by `on_real_close`, which needs a `virtual_positions` row that will
never exist (**0 drift rows**). It is **inert** — a permanently non-terminal row, re-read by `tick()`
every 5 s forever and never able to complete.
**Row 79 is the active one.** `on_real_close` seeded it 5 drift slots off today's real close: 15m and
1h are sampled (12:06 → 64831.3, 12:51 → 64867.1); ~~**4h (15:50),**~~ **12h (23:50) and 24h (tomorrow
11:50) are still due.** Its *drift* leg is sound — it measures from the real 64733.0 exit. Its
*shadow* leg and `exit_advantage_r` remain the cross-position figures above.

> 🔴 **CORRECTED 2026-07-30 22:35 — the 4h slot is NOT pending. It sampled at 15:51:22
> (price 64705.9, pct +0.04186), about two hours after this paragraph was written.** Three of five
> slots are banked. Only 12h and 24h remain due. **Row 79 has since been REPAIRED — see §2.28b.**

**HOW THEY GOT THERE — reconstructed from two DB backups and the journal, not guessed:**

| evidence | what it shows |
|---|---|
| `/root/backups/pre-adapter-20260729-164638/trades.db` (07-29 **16:46**) | `virtual_positions` max **85**, `sqlite_sequence` **85**, observatory max id **77**. **No 79/80.** |
| `/root/backups/pre-exit-advisor-act-20260730-113107/trades.db` (07-30 **11:31**) | observatory **79 and 80 present** with the 21:50 stamps; `virtual_positions` max **86**, `sqlite_sequence` **86** |
| journal, 07-29 19:00 → 07-30 01:00 | **exactly ONE** `VIRTUAL ENTRY vpos=` line — vpos 86 at **00:50:15**. **Nothing at 21:50.** |
| `on_entry` re-SELECTs `virtual_positions WHERE id=?` and arms only if the row exists | rows **86 and 89** must have EXISTED at 21:50 — so 86, 87, 88, 89 were all allocated |
| `sqlite_sequence` is **86**, and AUTOINCREMENT never lowers itself | the sequence was **explicitly reset** (or its row deleted) after those ids were consumed |
| the two rows are **7.6 s apart on the SAME side**, which `MAX_POSITIONS_PER_SIDE = 1` + `ux_vpos_one_open_per_side` forbid concurrently | create → delete → create, i.e. a **test loop**, not normal operation |
| BTC 1h candle 07-29 21:00 ranged **63231.6–63829.7** | the ghost entries 63605.6 / 63595.5 are real market prices of that minute |

**CONCLUSION: rows 79/80 are residue from an ad-hoc script — run OUTSIDE the service, during the
21:26–21:54 paper interlude, to exercise the naked-position fix (`97a4fdb`).** It created
`virtual_positions` rows 86–89, which armed the observatory; the rows were then deleted and the
sequence reset to leave a clean book before going live at 21:54:16 — and `post_exit_observatory`,
being a separate table nobody was thinking about, kept its two rows. Today's real vpos 86 then
re-used id 86, and `on_entry`'s `ON CONFLICT(vpos_id) DO NOTHING` silently preserved the ghost.

**THE CODE DEFECT, separable from the data mess:** `on_entry` treats `vpos_id` as a stable identity.
It is not — `virtual_positions.id` is unique only among rows that still EXIST. The §2.19-shaped fix is
to make the conflict **speak**: if an existing row's `opened_at` differs from the incoming one, that
is a different position and `on_entry` must **refuse and shout**, not adopt. **NOT written and NOT
proposed here** — the operator sequenced the observatory after the ADX fix.

**What would stop each, stated and NOT acted on** (`feedback_no_delete_virtual_positions` is standing
and both are data decisions):
- **Row 80:** set `status` to the existing terminal sentinel `'failed'` — that removes it from
  `tick()`'s working set. One column, on a row describing a position that never existed.
- **Row 79:** a status change cannot repair it. `entry_price` / `original_sl_price` / `opened_at`
  would have to be corrected to vpos 86's real values **and** `shadow_pnl_r` / `exit_advantage_r`
  recomputed. Until then, **do not quote row 79's `exit_advantage_r`.**
- 🔴 **Neither should be touched before the `on_entry` guard exists**, or the next id re-use recreates
  exactly the same row.

#### 2.28b ✅ CLOSED 2026-07-30 22:40 — guard shipped, row 79 REPAIRED, row 80 RE-KEYED

**Guard: `45e20e7` + `54dc734`. Data repair: no code, no restart.** The guard was shipped first, so
neither row could be recreated by the next id re-use. Order was not optional.

##### 🔴 THE AUDIT TRAIL — row 79's BEFORE values, verbatim, so the corruption survives its repair

These are the values the row carried while it was cross-position. **Any figure quoted from row 79
before 2026-07-30 22:36 UTC is one of these, and is a cross-position number.**

| field | **BEFORE (ghost identity)** | AFTER (real vpos 86) |
|---|---:|---:|
| `entry_price` | `63605.6` | `63686.0` |
| `original_sl_price` | `64724.6` | `64767.1` |
| `opened_at` | `'2026-07-29T21:50:04.012998+00:00'` | `'2026-07-30T00:50:14.893642+00:00'` |
| `shadow_pnl_pct` | `-1.0500647741708224` | `-0.9224947398172256` |
| `shadow_pnl_r` | `-0.5968722073279727` | `-0.5434279900101755` |
| `exit_advantage_pct` | `0.5939386174694139` | `0.7215086518230107` |
| `exit_advantage_r` | 🔴 `0.4252543887272212` | `0.47869860604501846` |

**The published `exit_advantage_r = +0.42525` is now formally superseded by `+0.47870`.** The 1R basis
changed with the identity: ghost `|63605.6 − 64724.6|` = 1119.0 pts → real `|63686.0 − 64767.1|` =
1081.1 pts. Sign survived; §2.28's warning that the mechanism *can* flip one still stands.

**Why repair rather than retire.** The shadow leg was proven valid for vpos 86, not assumed: the real
window `00:50:14 → 02:00:05` is a strict **subset** of the ghost window `21:50:04 → 02:00:05`; the
exit reason `15m_signal` (Bullish I-CHOCH) is a **market event** at a **market price**, independent of
entry; and the ghost's SL **64724.6 is TIGHTER than the real 64767.1 for a SHORT** (by 42.5 pts) and
was not hit before the signal, so the wider real SL cannot have been hit either. Only the
entry-relative arithmetic needed recomputing, and both inputs survived. Live-money observatory records
will be scarce for months — discarding one to preserve a corrupted identity was the wrong trade.

**Method:** guarded predicate matching exactly 1 row, and the derived four recomputed by the module's
**own** functions (`_compute_shadow_pnl`, `_maybe_compute_advantage`), never by fresh arithmetic.
**All 15 real-leg / shadow-exit / drift / max-favourable fields verified byte-identical afterwards**;
`virtual_positions[86].net_pnl = -2.541574` still equals row 79's `real_net_pnl`.

##### Row 80: `status='failed'` (22:21) **and** `vpos_id = -80` (22:37)

🔴 **THE NEW GENERAL FACT, which is what made the guard's first remedy text wrong:
`status='failed'` does NOT free a `UNIQUE` `vpos_id`.** Status controls only whether `tick()` picks
the row up (`_active_rows()` filters `status NOT IN ('completed','failed')`). The `UNIQUE(vpos_id)`
constraint — and the identity guard, which keys on `vpos_id` regardless of status — keep matching a
retired row forever. **Retiring an observatory row therefore takes TWO columns, always:**

```sql
UPDATE post_exit_observatory
   SET status='failed', vpos_id = -<id>, updated_at = datetime('now')
 WHERE id = <id>;
```

A negative key cannot collide with any AUTOINCREMENT id, and the row keeps its full history —
row 80's shadow leg, `shadow_signal_details` and timestamps are all intact; only `vpos_id` and
`updated_at` changed. **Nothing was deleted anywhere.** `54dc734` corrected the guard's shout to name
both statements, *before* either row was touched.

##### Verified state after the pass
Full replay of all 42 observatory rows against `virtual_positions`: **41 match, 0 would be refused**
(was 1), 1 retired under a negative key and unreachable by any real id. `_identity_conflict()` run
live against the DB returns `None` for a future **vpos 88** and **vpos 89**, and for **vpos 86** now
that row 79's identity agrees. `virtual_positions` still **61 rows**; observatory still **42**.

### 2.29 🔴 `weighted_adj`'s OWN DOCSTRING IS HALF FALSE — the adjusted score is not stored either
`weight_engine.py`: *"Gate policy: `weighted_adj()` is NEVER applied to the raw `direction_score` that
gates entry. **Only the stored `confluence_score` uses it.**"* The first half is true. The second is
not: `adj_score` reaches a `print`, the Telegram card, and a `confluence_score=` update kwarg — and
then **`signal_matrix.snapshot()` at `main.py:3996` overwrites the column with `res['score']`**, the
RAW matrix score. Proof: vpos 87's journal reads `raw=4.25 adj=-0.6212 final=3.63` while
`trades.19713.confluence_score = 4.25`.
**So `_w_adj` gates nothing AND is persisted nowhere.** The only score adjustment that reaches the
gate is `macro_filter`'s `total_gate_adj` (0.0 on this entry). Two numbers are called "the adjusted
score"; one is documented as stored and is in fact discarded. **Fifth instance of *check what the
label SAYS, not only what the gate DECIDES*.** Display-only, no money at risk — recorded so the next
reader does not cut a cohort on `confluence_score` believing it is the adjusted figure.

### 2.30 🔴 TAPE PRESSURE — shown, weighted by nothing (§2.21's shape, 2nd place) + it mislabels its window
`trades.tape_json` has exactly three consumers: `format_telegram_block` (the card),
`_persist` (storage), and `compact_for_llm` → the **post-trade** attribution prompt. **It does not
appear in the entry prompt at all**, and `capture_and_persist_sync` runs at `main.py:3997`, *after*
the entry executed. `microstructure.py`'s docstring says it plainly: *"never gates a trade."*
So vpos 87's card showed **Tape Pressure Sell 0.09** — an extreme reading — next to **book depth 82nd
pct**, and **neither carries weight anywhere.**
**And the number is weaker than it looks:** `window_seconds: 60` but `span_ms: 15168` — `_analyze_tape`
filters `now_ms − ts <= window_ms` over whatever `fetch_trades` returned and never guarantees the
window it names; and **one 11.3-BTC print is 733,715 of the 831,707 USDT sell side (88%)**, so
`buy_share_window = 0.0949` is n=1 dressed as a ratio.
Not entangled with book imbalance by construction (L3 aggression vs L2 resting depth) but not
independent either — same snapshot, and on this entry they pointed **opposite** ways
(`orderbook_json` band **bid**-heavy 0.6994 vs tape 91% **sell**).

### 2.31 THE §4.4 MIRROR CASE DOES NOT EXIST AT USABLE n — and its sign is backwards where it does
§4.4: 289 skips citing an ask wall above while SHORT drifted −0.270%/4h (t=−4.6) — the best vetoes in
the book. The mirror — **LONGs taken THROUGH a notable ask wall** — parsed from every stored entry
prompt (both formats) and percentiled against the same 24,658-snapshot `max_wall_mult_ask` baseline:

| cohort | §0-CLEAN n | totR | ALL-closed n (⚠ breaks §0 filters 3+4) | totR |
|---|---:|---:|---:|---:|
| LONG · ask wall ≥ 77th pct | **1** | +1.04 | 5 | +0.27 |
| LONG · ask wall ≥ 70th pct | **1** | +1.04 | 6 | **−0.01** |
| LONG · ask wall < 50th pct | 4 | −2.27 | **14** | **−6.61** |

**Clean n = 1** (vpos 82, ×11.7 = 85.9th pct, +1.04R on the trail). The widened cut shows **no harm at
all** and, if anything, the inversion — thin ask walls did worse — which is contaminated by moved
stops and two sizing eras and is **NOT offered as a finding.**
**What IS solid is the structural asymmetry: 289 vetoes versus 6 contaminated entries. The advisor
almost never takes a LONG into a notable ask wall**, so §4.4 and this table are a filter and its
leakage, not two arms of an experiment. **Nothing here contradicts §4.4; nothing supports re-opening it.**
Independent check that the entry-side percentile machinery is CORRECT: the baseline's 77th percentile
of `max_wall_mult_ask` is **×8.38** and vpos 87's prompt rendered **×8.4 = 77th pct**. ✅
⚠️ Still open from §2.22: **three divergent "imbalance" values under one word** at vpos 87's entry —
0.42 (OKX-4000, prompt, **ask**-heavy, 5th pct) · 0.6994 (BingX ±1% band, `orderbook_json`, **bid**-heavy)
· 0.5748 (BingX-100, `entry_ob_imbalance`). The misleading label was deleted; the divergence remains,
and here two of them point in **opposite directions**.

### 2.32 WATCH — the ADX1h base rate at entry, and the 5th-pct imbalance the advisor did not mention
On executed entries since the forming-candle fix (23 rows, all with `srv_adx_1h`): **6 of 23 = 26.1%**
entered with **ADX1h < 20**; median at entry **24.00**; only **2** entries ever had
`market_regime='FLAT'`, the sole state where `CONFLUENCE_FLAT_THRESHOLD` binds. The last four
executed entries read **30.7, 16.7, 11.1, 13.5** — **the two lowest readings in the whole history are
the two most recent trades**, and 3 of the last 4 are sub-floor. Two-in-a-row is ~6.8% under
independence, i.e. unremarkable; **the tail is the watch item, with n=2. Not a finding, do not act.**
Outcome cut is under-powered both ways (ADX1h<20: n=2, −0.05R · ≥20: n=14, −4.87R).
Separately, on vpos 87 the entry advisor cited depth (82nd pct) and the ask wall (77th pct) and was
**silent on `Imbalance 0.42 ask-heavy — 5th pct`, the most extreme figure in the block and against the
LONG.** A selective read of a correct prompt. Worth watching alongside §2.8 and §2.19's n=1 note.

### 2.33 🔴 LANDMINE — `virtual_trader`'s IMPORT MIGRATES THE PRODUCTION SCHEMA
**Opened 2026-07-30 because it FIRED THAT DAY, on read-only work.** Recorded so the next person does
not have to discover it the way this session did.

`virtual_trader.py` calls **`init_db()` at module scope (line 2641)**. So *merely importing the
module* — with no function called, no position touched, no intent to write anything — executes every
`CREATE TABLE IF NOT EXISTS` and every additive `ALTER TABLE` in it, against
**`DB_PATH = '/root/titan-bot/trades.db'`, the live production database, hardcoded.**

**What happened:** a scratch copy of the module was imported to run a *guard truth table* — pure
logic, no exchange, no DB intent. The import added two columns to the LIVE database hours before the
patch that introduces them was approved:

```
virtual_positions.entry_adx_1h_window   INTEGER   (col 41)
smart_exit_dryrun_samples.adx_window    INTEGER   (col 49)
```

**Assessed at the time, no harm:** additive nullable columns are a metadata-only change in SQLite; no
row was modified; every INSERT into both tables names its columns explicitly
(`virtual_trader.py:895`, `:2027`); no code reads either table positionally; the service stayed
active with `NRestarts=0` and zero errors; the open live position read normally. **The columns were
then adopted by the approved patch, so nothing had to be undone.** Dropping a SQLite column needs a
table rebuild, which would have been a far larger intervention than the accident.

🔴 **THE HAZARD IS GENERAL, AND THIS PROJECT DOES THIS KIND OF WORK CONSTANTLY.** Every forensic
session imports `virtual_trader` (and `main`, which imports it) to read state, replay logic, or test a
guard. **Every one of those imports migrates the production schema.** It is silent, it is not logged,
and it happens before the first line of the analyst's own code runs.

**MITIGATION FOR ANY FUTURE SCRATCH WORK — do this, it is cheap:**
1. Copy `trades.db` to scratch and **repoint `DB_PATH` before importing**, or
2. import into a process whose `DB_PATH` you have already patched via `sys.modules` shimming, or
3. simplest and what should have been done here: **test pure logic against a copy of the file, not
   against the module in place.**

🔴 **NOT RESTRUCTURED, and that is the operator's decision, recorded as such:** moving `init_db()`
out of module scope is a change to a **live trading module for a non-trading reason**. The class of
defect this project keeps paying for is exactly that — touching working trading code to serve a
convenience. **So the landmine stays armed and documented rather than defused.** If it is ever
defused, it should be in a commit whose only purpose is that, with the boot path re-verified.

### 2.34 ✅ FOUND IN THE PRE-RESTART AUDIT AND FIXED IN THE SAME COMMIT (`1161802`) — `sensor_events.init_db()` HAD NO CALLER
**The second migration door, and this one was shut.** Grepped across every module: `init_db()` in
`sensor_events.py` appears **only as its own `def`**. Nothing calls it — not `main`, not
`virtual_trader`, not `breakeven_worker`. `recheck_events` and `adaptive_trail_events` exist because
something created them once, long ago, so the `CREATE TABLE IF NOT EXISTS` statements have never been
needed since — **and nobody noticed that the migration door was closed.**

**Harmless while the schema never changed. NOT harmless the moment this module gained an additive
`ALTER`:** the new `recheck_events.adx_window` column would never have been created, the first
`log_recheck` INSERT would have raised `no such column`, and the module's own **two-layer
try/except would have SWALLOWED it** — losing **every recheck evidence row, silently**, while the
journal printed a perfectly normal `RECHECK` line. **Same shape as §2.6: code that READS as armed and
is not.** Caught by auditing the migration path before the restart, not after.

**FIXED in `1161802`:** a one-shot `_ensure_schema()` at the top of **both** public writers — the
pattern `post_exit_observatory._ensure_db()` already uses. Idempotent (`CREATE IF NOT EXISTS` +
guarded `ALTER`), once per process, and it cannot raise into the caller. Verified end-to-end on a copy
of `trades.db`: column absent → `log_recheck` called → **column created and the row written**, with
`adx_1h = 13.83` (converged), `adx_window = 200`, and `adx_delta = None` (correctly REFUSED, because
the entry-side window was unrecorded).

**This also closes a hazard that PREDATES the ALTER:** if `trades.db` were ever recreated or restored
from a copy without those tables, every sensor write would have failed the same silent way.

⚠️ **CONSEQUENCE TO EXPECT, stated so it is not read as a failure:** because the migration is now
**lazy**, `recheck_events.adx_window` **does not exist on the live DB yet** — it is created the first
time `log_recheck` runs, and the open vpos 87 can never trigger a recheck (`recheck_status='done'`, see
§2.26c). **The column will appear on the NEXT position's T+10s recheck.** A query for it before then
correctly errors with `no such column`; that is the design, not a fault.

### 2.35 ✅ BOTH PORTFOLIO MONEY-BRAKES WERE INERT FOR 2.5 MONTHS — FIXED (2026-08-01)
**`risk_manager.loss_streak_halt()` and `daily_loss_halt()` could not halt anything, and had not been
able to since 2026-05-11.** Not a threshold that was never reached — a query that could never return
rows.

Both read `trades` rows whose `signal_type` was in a hardcoded tuple
`('5m_group_b','close_long','close_short','exit_long','exit_short')`. That tuple encodes an
assumption that stopped being true: **that a close writes its own row.** It does not. Every close
route propagates P&L back onto the **ENTRY** row, whose `signal_type` is `open_long` / `open_short`.

🔴 **The entire database contains ONE row matching that tuple: id 186, `close_long`,
2026-05-11 21:18:16.** So `loss_streak_halt()` hit `len(rows) < LOSS_STREAK_THRESHOLD` (1 < 3) and
returned `'1/3 closes recorded'` on **every call for 2.5 months**, and `daily_realized_pnl()` returned
**0.0** on every call, sending `daily_loss_halt()` down its `pnl >= 0` branch forever.

**The tell that was there all along, in the code's own comment:** *"we filter on these ... because the
AI close path **also** propagates pnl back to the entry row, and we don't want to double-count."* The
author knew the entry row carries the P&L and excluded it — correctly, **if** a close row also
existed. When close rows stopped being written, the exclusion became the whole set.

**FIXED — the source is now `virtual_positions(status='closed').net_pnl`**, with the coverage proven
rather than assumed:
- **Route-agnostic by construction.** The predicate is `status='closed' AND closed_at IS NOT NULL AND
  net_pnl IS NOT NULL` and names **no route**. Present today: `sl`(28) `trail`(15) `external`(10)
  `ai_exit`(4) `post_entry_critical`(1). **`breakeven` is a fifth defined route with 0 rows so far and
  needs no code change to be counted.** Enumerating routes is the defect; the fix must not repeat it.
- **Partials are not double-counted.** `net_pnl` already CONTAINS any realised partial. Proven on
  vpos 82, the only position that ever took one: gross 42.4633600 + partial 18.9070939 − fees
  6.6849138 − funding 0.8929330 = **53.7926072 = net_pnl exactly**.
- **Duplicate `trades` rows avoided.** Six `15m_armed_exit` rows carry pnl byte-identical to a
  `virtual_positions` row (vpos 54/60/64/75/76/84). Reading ONE table is what avoids counting that
  money twice — the old tuple would have needed a seventh member and still been wrong.
- **Ordering is by `closed_at`, not `id`** (id is ENTRY order; a LONG opened earlier can close after a
  SHORT opened later). ISO-8601 `+00:00` on 58 of 58 rows, so lexical order is chronological —
  verified, not assumed.

🔴 **THE GUARD, §2.19's shape (this is the 6th place).** The failure was a mechanism silently reading a
set that could never populate **and reporting the miss in the same voice as a real pass** —
`'1/3 closes recorded'` reads exactly like an evaluated threshold. `PnlWindow` now carries its own
provenance with **no constructor defaults** (the required-positional half), and `blind` is a property
of the DATA rather than a check a caller may forget (the WHERE-clause half). A blind brake prints
`[TITAN][RISK-BLIND] 🔴 INSUFFICIENT DATA — <brake> CANNOT FIRE: n of N required closes visible in
<source>. This is NOT "evaluated and passed".` **Three states now exist where there were two:
halted · evaluated-and-passed · could-not-see.** Every reason string on every branch names the source
and the row count.

⚠️ **WHAT THE FIX DOES NOT DO: it does not retune anything.** `LOSS_STREAK_THRESHOLD=3`,
`LOSS_STREAK_COOLDOWN_HOURS=4`, `DAILY_LOSS_PCT_LIMIT=0.05` are untouched. Calibration is a separate
operator decision and is stated in the 2026-08-01 report with the 30-day firing rates.

### 2.36 🔴 LIVE STRUCTURAL QUESTION — AN ADVISOR CLOSE DOES NOT REACH THE ENTRY PATH
**Recorded as an open question, NOT acted on. No re-entry cooldown has been added, deliberately.**

**The mechanism, named:** the exit advisor closes on a **15m/5m tier flip against the position**
(4 of 4 closes cite it; 5 of 23 holds do). The entry cascade opens on **the same 15m/5m tiers**.
Neither knows the other exists — an `ai_exit` close writes `close_reason` on the position row and
nothing else. No cooldown, lockout, flag or signal suppression is keyed on it. So the same live tier
set that the advisor just declared broken can re-admit immediately, and once it did:

> vpos 89 closed **14:15:13** — *"15m/5m SHORT agreement dissolved—both now neutral"*.
> vpos 90 opened **14:25:19**, **10.1 minutes later**, same side, on an **IDENTICAL tier set**
> (1H Smart Trail Bearish 0.9 · 15m HyperWave Signal Down 0.7 · 5m Within Bearish OB 0.7), with the
> **same 1H tier instance still live** (age 3.3 h → 5.4 h, matching the 2.1 h between entries).

🔴 **WHY NOTHING WAS BUILT — operator's ruling, 2026-08-01, and it is the correct reading of the
evidence:** *n = 1, and the direction is not even established.* **vpos 89 was the WINNER of the
sample (+2.30) and vpos 90 was a loser (−0.61).** One observation cannot show that re-entry is
costly; it is equally consistent with the entry path being right and the advisor's close being
premature. Building a cooldown now would be **suppressing the very signal the §2.4 window exists to
measure**, and it would do so before the measurement finishes.

**What would close this:** the remaining ~6 §2.4 closes, with the post-close re-entry gap and the
outcome of each re-entry recorded. If same-side re-entries inside ~15 min are systematically worse
than the position they replaced, the mechanism above is the thing to change — and it is an
**entry-side** change, so §2.4-OP does not forbid it mid-window.

⚠️ **Counted correctly, this has happened ONCE in four closes.** Same-side re-entry after an advisor
close: **0 of 4 within 5 min · 1 of 4 within 15 min · 1 of 4 within 60 min.** The other gaps were
104.7 min and 448.5 min, and after vpos 90 the entry path produced **nothing for 20 hours**. Do not
quote the 10-minute case as a rate.

### 2.37 🔴 DECISION — `LOSS_STREAK_THRESHOLD` STAYS AT **3**. Recorded WITH the reasoning (operator, 2026-08-01)
**Written down so it cannot be revisited later as a rationalisation.** The brake was found dead
(§2.35), its 30-day backtest showed it would have blocked **2 of 5 live entries including vpos 89, the
only winner in the §2.4 sample (+2.30)**, and the threshold was **left alone anyway.** The reasons, in
the operator's terms:

1. **Softening a brake because it blocked one winner is OUTCOME-FITTING ON n=1** — the exact failure
   mode that has killed eleven hypotheses in §4. The evidence for "3 is too tight" is a single trade
   that happened to work.
2. **It is not a money mechanism.** Three consecutive losses mean *something is systematically off*,
   and that is equally true whether they cost **$4 or $400**. A count-based brake is supposed to be
   size-blind; that is the feature, not the bug.
3. **The 7.2% figure is CONTAMINATED and we do not actually know the live rate.** The 30-day window
   spans a **68× notional change** ($10,000 → $146), and the two 07-31 windows mix a **−137.32** loss
   with **−2.54** and **−0.82**. A rate measured across that discontinuity predicts nothing.
4. **A safety mechanism found dead after 2.5 months must not have "make it fire less" as its first
   treatment.** Restore it, measure it at one size, *then* discuss calibration.

**What would reopen this:** a measured live-size firing rate (duty below), not a single blocked
winner. **Nothing about this decision is provisional pending the §2.4 result** — if the advisor's
window comes back positive, that is not evidence about the streak brake.

### 2.37a 🔴 §2.4 CONFOUND — THE LOSS-STREAK BRAKE NOW SHAPES THE REMAINING ~6 DATAPOINTS
**Stated NOW, before any result exists, so it cannot be discovered afterwards.** From `3316e8a` the
brake is live and blocks entries after three consecutive losses. **The positions the advisor gets to
close from here are therefore a SELECTED SET** — specifically, entries that would have followed a
losing streak are removed from the sample.

**Had it been live over the four closes already recorded, it would have blocked vpos 89 (+2.30) and
vpos 90 (−0.61)** — i.e. it would have removed the sample's best and one of its worst, and §2.4 would
today read n=2 with a different net.

🔴 **This does NOT void the window.** §2.4-OP is explicit that the **entire entry side is NOT frozen**;
only what the advisor READS is. The count stays **4 of ~10** and the bar does not move. But the
remaining datapoints are drawn from a differently-filtered population than the first four, and **the
result must be reported with that stated on its face.**

### 2.37b 🔴 MEASUREMENT DUTY — THE BRAKE'S *LIVE* FIRING RATE, REPORTED WITH THE §2.4 RESULT
The 30-day rate (13 windows · 52.0 h · 7.22% of wall-clock · 5 entries blocked) is **NOT predictive**:
it spans the 68× size change (§2.37·3). **The number that matters does not exist yet.**

**To be measured over the §2.4 window, at live size only, and reported ALONGSIDE the window's result —
not separately, and not on request:**

| quantity | how |
|---|---|
| halts fired | count of distinct loss-streak halt windows since `3316e8a` |
| hours halted | summed window duration, and as a % of the §2.4 window's wall-clock |
| entries blocked | signals that reached `check_risk` and were refused with `loss-streak halt` |
| what those entries would have been | side, tier set, and — where recoverable — the outcome of the position that did *not* open |

**Until that table exists, no statement about this brake's cost or benefit is supportable in either
direction.**

### 2.37c 🔴 PRECONDITION TO ANY SIZE INCREASE — the daily-loss brake is ARMED BUT DORMANT at $146
`daily_loss_halt()` works again (§2.35) but **cannot bite at the current size**: −5% of the $510.41
balance is **−$25.52**, and at the live 1R (mean **$1.96** over vpos 86–90) that needs **~13 full-stop
losses inside one UTC day**. Observed live-era troughs: **−0.50%** and **−0.26%**.

**It becomes a real constraint the moment size increases** — and the same increase is what makes it
necessary. In the old-size book it would have fired on **12 of 18 trading days**, worst
**2026-07-29 at −51.81% of equity in a single day**, ten times its own limit, while blind.

🔴 **THEREFORE, ADDED TO THE SIZE-INCREASE CHECKLIST alongside §1b (margin mode CROSSED):** before any
notional increase, **re-derive `DAILY_LOSS_PCT_LIMIT` against the NEW 1R** and state how many
stop-outs it then represents. A limit that means "13 stops" at one size and "1.5 stops" at another is
not the same limit, and discovering that after the increase is the wrong order.

### 2.38 👁 WATCH, NO ACTION — THE 20-HOUR DROUGHT IS **NOT** THE 3.0 BAR. Measured 2026-08-01
**The bar is exonerated on its own pre-registered terms, and the drought has two other causes.**
Reconstruction validated first per §0: rebuilding the gate number from `matrix_breakdown_json`
reproduced the stored `confluence_score` on **40 of 40** `below_threshold` rows since the bar went
live, **0 mismatches**, before anything below was computed.

| | predicted (§2.0 pre-registration) | **observed, whole life of the bar (~38.9 h)** |
|---|---:|---:|
| refusal rate on TREND signals reaching the score gate | 15.72% | **11.76% — 2 of 17** |
| additional refusals per day from the 2.0 → 3.0 raise | ≈2.2/day | 🔴 **0.00/day — ZERO, total** |

🔴 **THE RAISE HAS COST EXACTLY ZERO ENTRIES.** Both TREND signals the bar refused scored **1.5**
(raw 2.5, macro −1.0) — **below the OLD 2.0 bar as well.** Not one signal has landed in the
2.0–3.0 band that the raise created.

**What is actually causing the drought — two things, neither of them the bar:**

| period | entry rows | HTF-blocked | reached gate | TREND | FLAT | %FLAT | executed |
|---|--:|--:|--:|--:|--:|--:|--:|
| 30d before the bar | 5609 | 4084 (72.8%) | 1524 | 630 | 894 | 58.7% | 26 |
| 7d before the bar | 1221 | 902 (73.9%) | 319 | 169 | 150 | 47.0% | 7 |
| **last 24h** | 196 | **162 (82.7%)** | 34 | **4** | 30 | **88.2%** | 1 |

1. **The HTF cascade, not the score gate, is where the funnel closes** — and it tightened from
   ~73% to **82.7%**. It runs **in front of** the score gate (`main.py:3679`), so 162 of 196 signals
   never reached the bar at all.
2. **The regime composition collapsed toward FLAT** — **88.2%** of gate-reaching signals in the last
   24 h, against 58.7% over the prior 30 days. **Only 4 TREND signals reached the gate in 24 hours,
   against a 30-day average of ~21/day.** In FLAT the governing bar is `CONFLUENCE_FLAT_THRESHOLD`
   = **5.0**, deliberately unchanged on 2026-07-30, and it refused **26 of 30** FLAT signals (86.7%).

**So the 3.0 bar barely got to vote.** Reported early, per the pre-registration's own instruction —
and per its other instruction, **this is a finding about the distribution and NOT a reason to move any
bar.** The 15-entry review still stands and its denominator is still 15 executed entries.

⚠️ **METHOD NOTE, §0's trap avoided:** `confluence_score` holds THREE different quantities by status.
The validation above is on `below_threshold` rows only, which is the one cohort where it equals the
gated score. `risk_halt` row 20103 is **excluded from every gated-score figure**: its
`macro_gate_penalty` is **NULL**, so its gate number is **not computable** — it is counted as having
reached and passed the gate, and no score is asserted for it.

### 2.39 ✅ FIXED (`ca90c2f`) — THE LEARNING LOOP GRADED **OPEN** POSITIONS. 47 of 65.

`signal_weights.audit_pending` selected on **age alone** and never required the position to be
closed; `_evaluate_trade_pnl` then invented an outcome **two different ways**:

- `exchange.fetch_positions()` → the exchange's **UNREALIZED** pnl. Trade **20920** was stamped
  **+0.5015 — a WIN — at 08:48:51 while its live short was open.** It closed at **−0.6410**.
- no matching exchange position → `return 0.0, 'closed_unknown'`. **In PAPER mode there is never an
  exchange position to find**, so this branch fired on **44 of the 65 engine-owned entries** and
  graded every one **0.0**. **32 of those 44** had a realised outcome the store's own ±20/−15
  thresholds call a win or a loss (19021: 0.0 vs **−143.67**; 10369: 0.0 vs **+370.45**).

**Net: 47 of 65 (72%) graded mid-flight. The weight store learned from 18 trades — only those that
closed inside the 2 h grace, a sample selected for FAST closers.**

**The fix:** closure is `trades.pnl IS NOT NULL`, **in the WHERE clause**, plus a resolver that
returns `None` so the caller skips. `_do_close` is the codebase's only `status='closed'` writer and
writes `trades.pnl` in the same transaction for **both** modes — one predicate, no join, no mode
branch. `AUDIT_MAX_AGE_HOURS` **24 → 96** because the window is entry-anchored and 24 h would have
permanently discarded the **14 of 58 (24%)** positions held longer than a day (longest 74.33 h). **A
position still open at 96 h is LEFT UNGRADED, PERMANENTLY** — never graded on a mark.

🔴 **`audit_score` IS PERMANENT ONCE SET.** The queue predicate is `audit_score IS NULL`, so a row
graded wrongly is **never re-picked**, even after its position closes and `pnl` appears. The fix
prevents the next one; it repairs nothing.

### 2.39a ✅ THE THREE WRONG GRADES — CORRECTED 2026-08-03 13:52 UTC

Backup `trades.db.bak_gradefix_20260803` (SQLite `.backup()`, `integrity_check: ok`) taken first.
One transaction, per-row assert `class(old) == class(new) == 'neutral'` **enforced, not assumed**
(it aborts the whole transaction if a class ever changes, because that would mean a weight must
move — a different operation). Rowcount asserted 1/1/1 per statement.

| trade | vpos | was | now (realised) | Δ`total_pnl` | class |
|---|---|---:|---:|---:|---|
| 19589 | 86 | −1.2829 | **−2.541574** | −1.258674 | neutral → neutral |
| 19713 | 87 | −0.3467 | **−0.819051** | −0.472351 | neutral → neutral |
| 20920 | **91** | **+0.5015** | **−0.641000** | −1.142500 | neutral → neutral |

Applied to `signal_weights.total_pnl` **and** `hyperwave_weights.total_pnl`. **`weight`, `wins`,
`losses`, `evaluations` and `updated_at` untouched on both stores** — verified by full-table diff
against the backup: exactly **3 trades rows, 3 combo rows, 3 subtype rows**, and `total_pnl` is the
**only** field that differs on any of them. `updated_at` was deliberately left alone: it records
when the evaluation happened, which is still true; bumping it would read as a new evaluation.

### 2.39b 🔴 EVERY `learning_*` ATTRIBUTION WRITTEN BEFORE `ca90c2f` WAS PRODUCED AGAINST A MARK

**Left in place and MARKED, deliberately — operator's decision, 2026-08-03.** Not cleared (that
destroys the evidence the defect existed) and not re-run (a fresh LLM call produces a *different*
verdict, not a *corrected* one).

`_attempt_learning` receives `row_for_learning['pnl'] = outcome_pnl` — the same number the weights
took — so **every attribution written before `ca90c2f` was reasoned against whatever
`_evaluate_trade_pnl` invented**: an unrealized mark, or a fabricated `0.0`.

**The demonstrable case, trade 20920** (`learning_at 2026-08-03 08:48:53`), verbatim:

> *"Large ask wall (68.32 BTC at 62650.5) above entry created resistance, **enabling profitable short
> exit as price rejected upward pressure**."*

The position **had not exited**. It closed five hours later at **−0.6410**. This is not a wrong
number — it is a wrong **story**, stored as text.

**Cost is archival, not behavioural:** `learning_liquidity_factor`, `learning_aggression_factor`,
`learning_influence`, `learning_confidence`, `learning_reason`, `learning_raw` are written only by
`signal_weights._attempt_learning` and **read by nothing** — grep confirms no reader anywhere in the
codebase. Nothing trades on them.

**Treat every `learning_at < 2026-08-03 13:42` row as attributed to an unresolved outcome.** From
`ca90c2f` forward the attribution sees a realised pnl.

### 2.40 🔴🔴 THE COMBO-WEIGHT MECHANISM **CANNOT FUNCTION AT LIVE SIZE.** IT IS INERT, NOT MERELY BIASED.

Measured 2026-08-03. **This is not a bias going forward — the table is frozen and every future live
trade is a no-op on it.**

**(a) The thresholds are absolute USDT and nothing scales them.** `WIN_THRESHOLD_USDT = 20.0` /
`LOSS_THRESHOLD_USDT = −15.0`, declared twice (`signal_weights.py:42-43`, `engine_15m.py:56-57`) and
compared raw: `if pnl >= WIN_THRESHOLD_USDT`. **No notional, margin, size, leverage or R term appears
anywhere near either comparison.** Their own comment still describes the calibration they were
written for: *"At $2000 margin × 5x = $10,000 notional, +$500 = +25% ROI on margin"*.

**(b) Live-era grades that crossed either threshold: ZERO of 6.** What it would take:

| vpos | 1R (USDT) | realised | R to reach **+20** | R to reach **−15** |
|---|---:|---:|---:|---:|
| 86 | 2.4866 | −2.5416 | **8.04R** | 6.03R |
| 87 | 1.8628 | −0.8191 | **10.74R** | 8.05R |
| 88 | 1.7918 | −0.5311 | **11.16R** | 8.37R |
| 89 | 1.6610 | +2.3024 | **12.04R** | 9.03R |
| 90 | 2.0091 | −0.6099 | **9.95R** | 7.47R |
| 91 | 1.3234 | −0.6410 | **15.11R** | 11.33R |

Mean **11.2R** to register a win, **8.4R** to register a loss.

🔴 **The loss side is unreachable BY CONSTRUCTION, not merely unlikely** — the protective stop caps a
live loss at ~1R. Largest live loss ever: **−2.5416**. Reaching −15 needs **6.0R at best**, i.e. the
stop must **fail first**. Deepest adverse excursion ever observed live: **−0.920R**. So at live size
the table can only ever move **up**, and in practice not at all.

**The last grade capable of moving any weight was `audit_at 2026-07-20 02:24:17` — in the PAPER era,
14 days ago and nine days before the live flip. Since the flip: 6 grades recorded, 0 threshold-crossing.**

**(c) The size of the mismatch, expressed in R. RECORDED, NOT PROPOSED — no change is being made.**

```
PAPER 1R  mean 124.3608 USDT (n=24)   |   LIVE 1R  mean 1.8558 USDT (n=6)   |   ratio 67.0x
   (notional ratio 10,000 / 146 = 68.5x — the 1R ratio tracks it)

what +20 / -15 MEANT at paper size :  +0.1608 R  /  -0.1206 R
the same meaning in LIVE dollars   :  +0.2985 USDT  /  -0.2238 USDT
the constants actually in force    :  +20.0    /  -15.0
                                      => 67x too high / 67x too deep
```

Sanity check that this is the right reading: at paper size **20 of 24 closes (83%) crossed a
threshold** — the bar was ~0.16R, i.e. almost any real outcome cleared it. At live size **0 of 6**.

**(d) YES — the frozen table is still SHOWN to the advisor, and that is a live influence channel.**
`main.py:2001/3776` `weight_used = signal_weights.get_weight(combo)` → `consult_for_entry` →
`claude_advisor.py:342` renders it verbatim into every entry prompt:

```
Combo weight: 0.90 (1.0 baseline; <1 = historical loser, >1 = winner)
```

**That is not hypothetical. Trade 19713 — a LIVE, real-money entry on 2026-07-30 — was shown
`Combo weight: 0.90`, and that 0.90 came from a single PAPER evaluation of ≈−78.70 at 68× the
notional.** 7 of 52 combos currently carry a weight ≠ 1.00; the newest of those judgements is from
2026-07-20, the oldest from 2026-05-26.

So: **the mechanism cannot update, but its output is still presented to the model as current fact,
labelled "historical loser / winner".** The subtype store is *not* exposed this way — `claude_advisor`
never imports `engine_15m` and `hw_weight` reaches only Telegram — so this channel is combo-weights
only.

**NOT FIXED, ONLY MEASURED.** Re-scaling the thresholds is a strategy change, and it interacts
directly with §2.41. **Nothing here proposes adopting the R-equivalents above.**

### 2.40e ✅ THE INFLUENCE CHANNEL IS CLOSED (`a85733f`) — THE WEIGHT NOW CARRIES ITS PROVENANCE

**The mechanism is still inert (§2.40 stands, unchanged). What is fixed is that the model is no
longer told a one-trade paper judgement is established history.** Was:

```
Combo weight: 0.90 (1.0 baseline; <1 = historical loser, >1 = winner)
```

Now:

```
Combo weight: 0.90  (1.00 = untouched; -0.10 per evaluation that lost more than $15,
  +0.10 per one that gained more than $20)
  Based on: 1 evaluation, most recent 2026-06-03, taken at ~67x the current position size.
```

🔴 **THE NUMBER IS KEPT.** No suppression, **no minimum-n rule, no staleness cut-off** — deciding
for the model that a 1-evaluation weight should be ignored is the same mistake in the other
direction. **Facts, not judgements**, the same line drawn on the book block (*"CALIBRATION ONLY"*)
and on the 1H tier identity (`f0a8d30`). The direction sentence is kept but stated **mechanically**
— what moves the number — instead of as a character judgement about the combo.

Four render shapes, all verified on real data: **never evaluated** (the common case — no store row —
renders *"no evaluations yet — this is the untouched baseline"*); **single paper evaluation**
(*"~67x"*); **live-era** (*"~0.97x"*); **mixed eras** (*"~0.99x-67x the current position size (mixed
sizes)"* — an honest range, not a mean that hides the mix). A real lookup failure renders *"not
available"* and is the **only** thing that does.

Size ratio comes from `order_adapter.active_fixed_margin() × LEVERAGE`, **not** `FIXED_MARGIN_USDT`
— that alias resolves to the PAPER size and would understate the ratio by ~67x in live.

**FREEZE CHECK (§2.4-OP), argued not assumed:** §2.4-OP freezes *"everything the advisor READS"* on
the **close** prompt and is explicit that **the entire entry side is NOT frozen**. The combo weight
reaches `consult_for_entry` only; it appears **exactly once** in `claude_advisor.py`, and neither
`_build_exit_context` nor the close template touches `signal_weights`. Verified: **no diff line
touches any close-side symbol.** ⚠️ Second-order effect stated rather than hidden: future *entry*
`ai_reason` text may read differently, and the exit prompt renders `Advisor's reason at entry` — but
that is the same field reading the same column, not a change to a close-prompt input, and it is the
property every entry-side change has (cf. §2.37a, §2.38).

**Nothing else changed:** `get_weight` is byte-identical (**0** diff lines in its body), the gate is
`direction_score + macro_gate_adj` with **no weight term**, and sizing is `FIXED_NOTIONAL_MODE` with
`scaled_step_margin` still having **no callers**.

### 2.40f 🔴 THE THRESHOLDS AND §2.41 ARE ONE DECISION — DO NOT TAKE THEM IN SEQUENCE BY ACCIDENT

**Operator's ruling, 2026-08-03. Recorded so neither can be taken alone by a later session.**

Adopting the R-equivalent constants from §2.40c would make the mechanism **live again** — and that
**changes what §2.41's re-grade MEANS**:

| | if the thresholds STAY at ±20/−15 | if they are re-scaled to the R-equivalents |
|---|---|---|
| the mechanism | **inert** — no weight can ever move at live size | **live** — weights move again |
| what §2.41 would write | a **PERMANENT, unrevisable** value, carried into every future entry prompt | a **revisable** value that live evidence then corrects |
| so §2.41 is | a final judgement derived from a paper era at 68× notional | an initialisation that the next few trades can overwrite |

**The same re-grade is a different act depending on which threshold decision is in force.** Taking
them in sequence — re-grade first, re-scale later, or the reverse — means the first decision is made
under an assumption the second one invalidates.

🔴 **BOTH REMAIN DEFERRED, AND THEY ARE TO BE DECIDED TOGETHER.** §2.41 stays deferred; §2.40's
thresholds stay **recorded, not fixed**. Neither is housekeeping and neither is a prerequisite for
the other — they are one decision with two levers.

### 2.41 🔴 DEFERRED, EXPLICITLY NOT HOUSEKEEPING — THE 44-ROW RE-GRADE WOULD SET A **PERMANENT** WEIGHT

Correcting the 44 paper rows that `_evaluate_trade_pnl` graded `0.0` (§2.39) would, replaying
`record_outcome` in audit order over all 66 audited trades, move:

```
COMBO   weights : 29 of 53  (26 by +/-0.10, one 0.80 -> 0.60)
SUBTYPE weights :  4 of 16
     HW_SIGNAL_SHORT  0.85 -> 1.00      HW_SIGNAL_LONG  0.75 -> 0.85
     HW_OB_SHORT      1.00 -> 0.90      REVERSAL_LONG   1.00 -> 0.95
```

**Both of the two most-used subtypes would stop being marked as losers.**

🔴 **§2.40 makes this WEIGHTIER, not lighter, and that is the whole reason it is deferred.** If a
weight can never move again at live size, then **whatever value this re-grade writes is the value
that combo carries permanently** — and it is carried straight into the advisor's prompt on every
future entry (§2.40d). It would not be a data repair that later evidence can correct; **it would be
a final, unrevisable judgement, derived from a paper era at 68× the notional.**

**Deferred by the operator, 2026-08-03. Not a cleanup. Requires an explicit decision that also
answers §2.40 — because writing permanent weights while the update mechanism is inert is the
decision, whichever way it goes.**

### 2.42 ✅ BOOK SOURCES MOVED TO OKX-4000 (`34dbdbf`) — AND THE POST-WINDOW LIST, AS ONE BLOCK

**Applied 2026-08-03 14:31 UTC, LIVE, flat.** `trades.advisor_book_json` holds the OKX-4000 dict the
entry advisor was handed — **the same object, threaded down, never re-fetched**. The learning loop
reads it. The recheck's baseline (`entry_okx_wall_baseline_mult`, a **NEW** column — repurposing
`entry_wall_baseline_mult` would have been the `confluence_score` defect) and its refresh moved to
OKX **together**, with **NO substitute venue** on failure and an explicit `book_unavailable` marker
so a failed read is no longer indistinguishable from a pass. Wall-rule weight is 0, so **no verdict
and no stop moved** — analytic hygiene, verified over 7 wall combinations all scoring −5.

**Both prompts byte-identical (md5) before and after; the §2.4 window is NOT reset.** The structural
reason: `entry_wall_baseline_mult` is **not** in the close prompt's read list, while
`entry_sup_wall_mult` / `entry_ob_imbalance` **are** — and those are untouched.

🔴 **FINDING, reported not changed — the non-advisor entry path.** `webhook()` delegates to
`_handle_state_machine` (which consults the advisor) but also carries a legacy block reached by
falling past **12 early returns**, where `_execute_entry` runs with **no advisor and no OKX book**.
It keeps the confluence gate, the risk halt, the position cap and skip attribution; it loses the
advisor. **Entries came through it: 0 of 65 positions** (all 65 are `ai_decision='execute'`; 59
paper / 6 live). Across every executed row ever, **exactly one entry** — trade **181, 2026-05-11**,
which **predates `virtual_positions`** (earliest position row 2026-05-17); the other 7 advisor-less
rows are `15m_armed_exit` close legs. **Not reachable by anything TradingView sends today** — every
observed `task` (`price_action` 1067, `confirmation` 107, `exit` 2, `trend_catch` 1, `signal` 1)
routes to a handler that returns first — but it is **legacy, not dead**: an unrecognised `task` plus
an `action` outside `ACTION_TO_SLOT` still lands there.

### 2.42a 🔴 THE POST-WINDOW LIST — FOUR ITEMS, COUPLED. DO NOT TAKE THEM SINGLY.

**① §1d — the exit advisor's OKX-down fallback. BOTH HALVES IN ONE COMMIT.** Repoint
`entry_sup_wall_mult` / `entry_ob_imbalance` to OKX-4000 **AND** change the fallback to render **NO
entry reference** when OKX is down rather than a BingX one. **Repointing alone pairs an OKX entry
reference against a BingX "now"** — the exact cross-source comparison `625fedc` removed. The
fallback fires on ~**5.1%** of AI-path consults. *Inside the close prompt.*

**② §3 — the drifting "at entry" reference.** `main.py:2553-2573` takes the `orderbook_density` row
nearest the fill (±10 min), so once a post-fill row exists it becomes nearer and the entry number
changes **silently, once**. vpos 91: the −52.3 s row gave ×4.85 / 0.5517, the +8.7 s row ×4.08 /
0.5584 — first consult `entry x4.8 → THINNED`, every later one `entry x4.1 → grew`, and that is the
**denominator of the arrow**. **Fix: bound the search to rows at or BEFORE the fill** — stable and
causally honest. *Inside the close prompt.*

**③ §2.40 / §2.41 — the thresholds and the re-grade, one decision with two levers.** An inert
mechanism makes a re-grade **permanent**; a live one makes it **revisable**.

**④ RETIRE `entry_wall_baseline_mult` — WITH ①, not before.** After `34dbdbf` it is **written and
read by nothing**. Its writer is kept only because ① still needs the BingX fetch alive for the
frozen columns. **Once ① lands, that fetch's last consumer is gone and the column has no purpose** —
drop the writer; keep the data, recorded as historical BingX depth-100.

**Ordering constraint:** ④ cannot precede ①; ① cannot precede the window closing. ② shares ①'s gate
but is otherwise independent. ③ is independent of both.

### 2.43 ✅ THE LEGACY FALL-THROUGH REFUSES TO ENTER (`489e0ac`) — AND WHAT IS **NOT** PROVEN

**Applied 2026-08-03 14:48 UTC, LIVE, flat.** `webhook()`'s legacy entry branch no longer calls
`_execute_entry`. It logs `[P3-ENTRY-REFUSED]`, Telegrams the operator with `task`/`action`/`tf`
**verbatim** plus what to do (misconfigured alert **or** missing handler), stamps
`status='unrecognised_payload_refused'`, and returns 200 without trading. It deliberately does **NOT**
route the payload to the advisor — an unrecognised payload is exactly what we do not understand well
enough to trade on.

🔴 **THE CLOSE HALF IS UNTOUCHED, DELIBERATELY.** Same fall-through, but it already carries its own
`orders_are_real()` guard, it has run once (trade 186, 2026-05-11), and **refusing a close could
strand an open position — strictly less safe.** All 13 names the shared tail reads are
pre-initialised above the `is_close` split, so the close path is byte-for-byte unchanged (AST-verified;
`create_market_order` still reachable at 4476/4490).

🔴 **PROVEN STRUCTURALLY, NOT BEHAVIOURALLY — SAID PLAINLY.** A live probe
(`task='__guard_test__'`) **never reached the guard**: the **HTF cascade blocked it first**
(`htf_blocked`, *"1H NEUTRAL (no active TREND signal)"*, row 21032, still flat, vpos count 65).
Reaching the branch would have required setting a 1H TREND signal in a live bot's state machine —
**not done, and not to be done.** What IS proven: **`_execute_entry` has no remaining call site in
`webhook()`** (AST) — the route cannot place an order at all, which is stronger than one passing
probe. Plus: no dangling `entry` read, no unbound name in the refusal branch, both prompts
byte-identical (md5), four boot gates green.

**Incidental finding, recorded:** the **HTF cascade is a second layer in front of this branch**, but
it is conditional on **state-machine state**, not on the payload — with a 1H TREND signal live, the
same unrecognised payload would have walked straight to the entry. It is protection, **not** a
substitute for the guard.

The old branch body was **DELETED, not left unreachable under the return** — dead code still reading
`entry[...]` would NameError the moment anyone removed the return (the 2026-07-29 class).

### 2.44 ✅ THE "TTL EXPIRED" LABEL WAS WRONG 70 TIMES IN 77 — FIXED (`6d9281d`)

`signal_tiers.build` set `counted_by_gate = (net_direction not in (None,'NEUTRAL'))`. A category nets
NEUTRAL for **three structurally different reasons** — TTL expiry, **intra-conflict**, or no signal —
and `render()` printed ONE sentence for all of them: *"NOT counted by the gate — matrix TTL expired"*.

**Measured over the 87 stored `entry_tiers_json` records: rendered 77 times, WRONG on 70 (91%).**
Those 70 were intra-conflict with the signal live and inside its TTL; **7 (9%) were genuine TTL
expiry**.

🔴 **vpos 91 is the case, and the mislabel PROPAGATED.** Its 15m tier was shown as **"25m ago"** and
**"TTL expired"** in the same line under a **90-minute** MOMENTUM TTL — two facts that cannot both be
true. The entry advisor cited it; so did the operator's question that led to the fix.

**Fixed:** `build()` now captures the real reason into `not_counted` (+ `not_counted_detail` with the
L/S split and signal count), **persisted to `entry_tiers_json`** so it cannot be re-derived wrongly
later; `render()` looks it up and never re-derives. Four strings for four states; an unrecognised
value degrades to *"the category nets NEUTRAL"* — vaguer than the truth, **never a false reason**.
TTL minutes are read from `config.CATEGORY_TTL_MINUTES` so the printed number cannot drift.

**FACTS, NOT JUDGEMENT** — same line as `f0a8d30`, `8b15ecc`, `a85733f`. **Freeze:** entry side;
`entry_thesis_lines` (the only `signal_tiers` function the close prompt uses) has **0 references** to
`counted_by_gate`/`not_counted`; entry-thesis block and full close prompt **byte-identical by md5**.
**Gate arithmetic untouched** — `signal_matrix.py` not in the diff; `:322` still drops expired
signals before scoring.

⚠️ **CORRECTION TO THE 2026-08-03 16:05 REPORT, recorded not restated:** it said **0 of 77** were TTL
expiry and 7 were "no signal". Splitting on the slot's `present` flag shows those 7 are **genuine TTL
expiries** — the slot holds the signal, the matrix dropped it. **The honest split is 70 wrong / 7
right.**

### 2.45 🔴🔴 CLOSED QUESTION — **THE LOSING ENTRIES ARE NOT IDENTIFIABLE IN ADVANCE ON THIS DATA**

**Ten measured attempts. All documented. All negative.** Recorded so no future session re-runs a dead
branch.

| # | branch | result | n |
|---|---|---|---|
| 1–4 | **four `market_regime` redefinitions** | all four still took the losing trade | — |
| 5 | **ADX floor, 1st measurement** (2026-07-30) | sub-floor entries were the **BEST** cell (−0.02R vs −0.32R) | — |
| 6 | **ADX floor, 2nd measurement** (2026-08-03) | holds: ADX1h <20 **not** worst (n=7, −0.112R); **20–25 best** (n=14, +0.167R); **ADX4h <20 is the best 4h cell** (n=11, +0.250R) | 39 |
| 7 | **efficiency ratio at fixed 4h / 12h** | flat: +0.066 vs +0.010 (4h), −0.031 vs +0.102 (12h) | 39 |
| 8 | **ATR(1h) vs its own 14-day median** | flat: +0.002 vs +0.072 | 39 |
| 9 | **intra-conflict as a range proxy** | rejected 4 ways; **χ² ≤ 1.24** and the **sign REVERSES** between the 4h and 12h windows | 65 |
| 10a | **1H tier age** | non-monotone: `<1h` +0.293 · `1–3h` −0.036 · `3–6h` +0.370 · `≥6h` −0.584 | 39 |
| 10b | **5m tier age** | **zero variance** — it is the trigger, 0.00h on all 65 | 65 |
| 10c | **15m tier age** | **not reconstructible before 2026-07-26**; 7 of 65 covered | 7 |
| 10d | **ER over [signal fired → fill]** | **INVERTED**: predicted-worst cell is 2nd best (−0.028R); actual worst is "old **and** price moved cleanly" (−0.473R) | 27 |

**The two flagged trades defeat all ten:** on age they sit at the **51st and 62nd percentile**; on
ER-since-signal they land on **opposite sides of the median** (30th / 67th); and **vpos 86 carries one
of the highest scores in the book (5.75) with ZERO intra-conflicts, three agreeing categories, at
ADX(1h) 11.12** — it passes every filter ever considered and lost 1.02R.

🔴 **WHAT WOULD CHANGE THIS — AND IT IS THE ONLY THING THAT WOULD: LIVE-ERA OBSERVATIONS.** The clean
cohort is **39, of which 34 are paper**; the live era holds **5–6**. Every positive cell that
motivates any rule rests on paper trades at **68× the notional**. At the measured rate of **1.5
entries per active day**, **30 live entries is roughly three weeks.**

**Until that sample exists, do not re-run these branches and do not fit a threshold to n=39.**

## 3. WATCH-LIST — CURRENT REALITY

**Retired** (deleted `d12e276` — they answered their question or their question died):
`prior-move logger` · `TOLN (tolerate-NEUTRAL)` · `counter-short review`

**Redefined** — the old predicates could never fill again:
| Sensor | New predicate | N |
|---|---|---|
| chop-short | `ema_gap_dir_1h='Flat' AND market_regime='TREND'` (old half included `regime='FLAT'`, which the FLAT score floor drove to zero) | **0 of 5** |
| regime-FLAT high-ADX | window widened `-3d → -21d` | **5 of 12** |

**Reclassified as DATA SOURCES — these are not watchers, they FEED the exit advisor. Keep them
running; switching them off silently degrades every exit consultation:**
`orderbook-density collector` (60s, builds the percentile baseline `_exit_pct()` reads) ·
`smart-exit dryrun sampler` (live regime + volume in the exit context)

🔴 **CORRECTED 2026-07-29 — two of these are NOT accumulating, see §2.15:**
`chop-short` **0 of 5, 0 arrivals since the FLAT floor** · `regime-FLAT high-ADX` **5 of 12 with a
ZERO arrival rate and a rolling window that will take it back DOWN**

**Genuinely accumulating toward a decision:**
`volfloor` **5 SHORT / 4 LONG clean** (threshold 6; expiry §2.5) ·
`exit advisor` **0 of ~10 closed positions — count RESTARTED A SECOND TIME at `957f980` (2026-07-30); all 68 prior consults contaminated by the cross-source percentile defect, tally reset to improved 0 / worsened 0 / neutral 0** (§2.4, §2.19)

---

## 4. HYPOTHESES TESTED AND KILLED — DO NOT RE-OPEN WITHOUT NEW EVIDENCE

Ten. Each cost real analysis time. **A hypothesis is re-openable only with data that did not
exist on 2026-07-27** — not with a fresh intuition.

1. **Prior-4h chase** — the idea that entries chase an already-extended 4h move. No relationship
   survived contamination filtering.
2. **Signal → entry slippage** — the delay between alert and fill was proposed as a P&L drain.
   Measured; it is not material.
3. **Entry-timing bucket (R2, prior-move)** — first reported at p=0.011/0.027, both **under-filtered**.
   Correctly filtered: **p = 0.1544**, and the mid bucket collapses from n=8 to **n=1**. An artefact.
4. **Wall-side misread — DEAD, twice, on two bots by two methods.** The claim was that the advisor
   confuses a wall above with a wall below and vetoes good trades. Reality: **289 skips citing an
   ask wall above drifted −0.270%/4h (t = −4.6)** vs −0.051% control, load-bearing subset
   **−1.509%/24h**. Positive drift = the skip would have won, so **these were the BEST vetoes in
   the book**. Mercury-SOL reached the same conclusion on 2026-06-30 by replaying 471 historical
   skips: only 6 flipped (1.3%) and **all six were losers**. 🔴 **Do not re-open.**
5. **ADX + score chop gate** — the proposed separator fully overlaps winners and losers; the
   highest-ADX trade (#47) is a **−$127 loser**. Only the 1h EMA-gap 'Flat' tell survived, and it
   is still only being watched (§3), never shipped.
6. **Stop-too-tight** — rejected on geometry: stops are a uniform **2.5×ATR**, so "too tight" is
   not a property the data can express. The stop being the expensive exit is a **horizon**
   artefact, not a distance one.
7. **Volume ceiling** — 2 vs 2, p = 0.333. Tested **twice**, failed twice. See §2.5 for the expiry.
8. **EQH/EQL liquidity sweeps** — no directional edge (EQH and EQL drift the **same** way; the
   thesis needs opposite signs). Smart-TP simulated at **−971** on the clean sample. Not a
   volatility proxy either: at sweep moments ADX 25.91 vs 25.08 baseline, ATR 351.4 vs 351.7. §2.6.
9. **"11 of 11 would have survived their original stop"** — **WRONG, an artefact.**
   `max_adverse_price` **stops updating at the close**, so it never sees the excursion that
   followed. On real candles, **8 of 17 hit the original stop.** Never quote stored extrema for a
   survival question.
10. **The 5-position counterfactual** — the follow-up figure (−335.84, "the fix would have lost
    money") was **also wrong**: **survivorship bias in the resolution criterion**, because only
    fast-resolving positions could resolve on internal data. Settled properly on **13,536 real
    OHLCV candles**. 🔴 **Regardless of the outcome, do not propose restoring wall-trail or
    recheck TIGHTEN** — operator's standing instruction.

**The pattern in 3, 9 and 10:** every one was a *stored-column shortcut* standing in for a real
price path, and every one produced a confident wrong number. When the question is "what would
price have done", **fetch candles**.

---

## 5. RESOLVED 2026-07-26/27 — closed, recorded so they are not re-investigated

- **Exit advisor existence.** It was **wired but NEVER invoked**: the 5m Group-B trigger has never
  arrived, and the paper-mode position lookup returned empty. It was not broken — it was
  unreachable, which reads identically from the outside. Now **live in DRYRUN** on three triggers:
  **hourly + on 15m confirm + on armed exit** (`ef7fa10`). **68 consults recorded as of 2026-07-30 03:15** — **ALL 68 contaminated** by the cross-source percentile defect (§2.19); the count is **0 of ~10**. *(This line read "3 consults" from the day it was written and went un-updated for weeks — the same staleness class as §9.)*
- **Entry-advisor 1H identity gap** — closed (`f0a8d30`). The advisor now sees which named signal
  set the 1H trend, its weight and its age. **`AI_ADVISOR_HIDE_1H` stays `True`**, and the identity
  is supplied as a **FACT ONLY — no statistic, win rate or historical performance attached**,
  deliberately. Renders as: `1H trend set by: Trend Catcher Up, weight 1.0, set 2.2h ago`.
- **Wall-side misread** — see §4.4. Moved out of open items entirely.

---

## 6. SHIPPED 2026-07-26 → 07-30 — **twenty-five commits, `93c20c3..81875c9`**

🔴 **`81875c9` (2026-07-30 11:32) — THE EXIT ADVISOR CAN ACT.** `EXIT_ADVISOR_DRYRUN=False`, both consult gates freed from the flag that also muted them (§2.23), `_advisor_close` added as the only advisor-driven close, `close_reason='ai_exit'`, **close-first/cancel-after in the shared close path** (removes a naked-position window latent on sl / trail / armed / emergency), 5m Group B repointed to the enriched prompt (§2.24). 186 insertions, 35 deletions, 3 files.

**2026-07-29 evening → 07-30 (post-`cb3a8bb`), six commits:** `11055e2` revert to paper ·
`97a4fdb` naked-position defect + its class + the race neither cap caught · `4ce8664` LIVE again ·
`1db2b4c` exchange→DB boot reconciliation · `12b4df2` size-mismatch alert named the wrong number ·
`625fedc` exit percentile cross-source + provenance guard (§2.19) · `838481f` no-op TIGHTEN
(§2.20) · `957f980` three card labels (§2.22).


*(the table also lists `93c20c3` itself as the starting anchor, so nineteen rows)*

| Commit | What it fixed |
|---|---|
| `93c20c3` | **Recheck TIGHTEN bound** — new SL can never be tighter than the **ORIGINAL** stop. (Variant B only; Variant A explicitly rejected.) |
| `596fbdf` | Gated the counter-short caution on `trend_1d != 'bull'` — **superseded hours later by `b878535`**, kept in history to show the stopgap preceded the retirement |
| `b878535` | **RETIRED the counter-trend EMA-1h soft caution** — its founding statistic does not reproduce and the cohort's sign is **inverted**. 17 lines removed, replaced by a 28-line historical note |
| `f7df202` | **LONG partial realisation** — 1/3 at +1R, remainder rides the unchanged contract; columns `partial_taken`, `realized_partial_usdt`, folded into `net_pnl` |
| `ef7fa10` | Persist the 15m entry confirmation + **wire the exit advisor in DRYRUN** (hourly / 15m confirm / armed exit) |
| `d12e276` | Retire 3 sensors, redefine 2 |
| `f0a8d30` | Give the entry advisor the **1H signal identity** (fact, not judgement) |

| `8b15ecc` | **2026-07-29** — order-book PERCENTILE scale for the ENTRY advisor; the word "Massive" deleted; the HARD RULE now judges thickness by percentile |
| `7285c5d` | **2026-07-29** — all THREE tiers to both advisors with name/direction/weight/age + an explicit agreement line; `ABSENT` replaces `n/a`; new `entry_tiers_json` column; the false "3 timeframes are aligned" sentence removed |
| `4fc89ea` | **2026-07-29** — EXIT prompt's "Total depth" line populated (had rendered `n/a` on 100% of consultations) |
| `c307bb7` | **2026-07-29** — two prompt claims replaced by facts: the false trail promise (§2.12) and the ADX "~<20-23" threshold plus the FLAT-MARKET GUARD rule built on it (§2.13) |
| `41c4a4d` | **2026-07-29** — cleanup: `Long/Short ratio` line deleted (§2.14); bull-regime watcher edge-triggered; the two starved sensors given an enforced 2026-09-30 expiry (§2.15) |
| `5285495` | **2026-07-29** — the `.sh` watchers were outside git: `.gitignore` admitted only `*.py`, so every shell sensor existed in ONE copy on disk, with no history and no backup. Six files brought under version control |
| `96b83d4` | **2026-07-29** — **the live-order adapter.** `order_adapter.py` becomes the ONE seam where a fill either happens or is simulated; two flags, both must be True. Closes three exchange-write paths that were guarded only by circumstance. Boot HARD-REFUSES an unsafe configuration (`os._exit(3)`). Paper arithmetic byte-identical (`4.99715034`) |
| `5f054b7` | **2026-07-29** — **item 11: the stop moves to the EXCHANGE.** Real `STOP_MARKET closePosition='true'`; the cancel/create race lifted into `move_stop_with_race_guard` and shared; the emergency-close invariant now lives in exactly two places. Orphan stops cancelled on both entry-abort paths — an orphan hangs over ANOTHER live position, not over nothing |
| `0833f42` | **2026-07-29** — **item 12: routing asks WHO OWNS THE POSITION.** `engine_owns_position()` replaces `is_active()` at seven sites; `_from_adapter` stops an unbounded close recursion AND a broken emergency close; the reconciliation door to double management shut at the root; `is_virtual` data-integrity fix. Sizing set to `$150`. Second live gate added |
| `d63cb8b` | **2026-07-29** — **item 13: passive-fill reconciliation.** A stop that fires on the exchange is reconciled back into the row from the REAL price and fee, via `read_filled_protective_order` extracted from `_report_passive_fill`. Position gone with our stop unfilled ⇒ shout and do NOT touch. Breakeven exits stamped `reason='breakeven'`, not `'sl'` |
| `984c96a` | **2026-07-29** — the margin-mode comment was lying: the account is **CROSSED**, not isolated. Comment-only change; the mode itself deliberately left alone (§1b) |
| `cb3a8bb` | 🔴 **2026-07-29 19:14 UTC — LIVE.** Both mode flags flipped to True. Two lines, nothing else. `$150` notional |

`596fbdf` and `b878535` are two commits on one decision that reversed itself within a session —
recorded that way on purpose.

✅ `7285c5d`'s `entry_tiers_json` WRITE path **is verified** — vpos 85 / trades row 19468,
2026-07-29 13:50. See **§2.19**. (This slot previously carried a "not yet verified" warning that
§2.19 had already superseded.)

---

## 7. VERIFIED STATE — 2026-07-30 03:15 UTC (LIVE, POSITION OPEN)

**Re-verified from runtime at 03:15, not copied forward from the 19:30 block.** See §9 for why that
sentence is now a rule.

🔴 **RE-VERIFIED AGAIN AT 2026-07-30 11:10 UTC, whole block, against runtime — nothing below is
copied forward.** Unchanged: `git status` clean · origin in sync · HEAD `957f980` · `titan.service`
active since 02:51:11, `NRestarts=0`, **0 errors / 0 tracebacks / 0 CRITICAL / 0 `REFUSING TO
START`**, breaker never tripped · runtime **= commit by HASH, 8/8 MATCH** (no `.py` newer than the
process start) · four boot gates green in the live journal · **Mercury-SOL untouched, active** ·
exchange **and** raw `swapV2` both report exactly 1 position and 1 order, ids unchanged, no orphans ·
balance `free 481.30 · used 29.30 · total 510.60`. Changed: the position's P&L only (row below).

`git status` **clean** · origin **in sync** (`main...origin/main`, 0 ahead 0 behind) ·
HEAD **`957f980`** · `titan.service` **active**, restarted **2026-07-30 02:51:11**, `NRestarts=0`,
**0 errors / 0 tracebacks / 0 CRITICAL**, **0 `REFUSING TO START`**, breaker never tripped ·
runtime **= commit by HASH, 8/8 MATCH** (latest source mtime 02:49:33 precedes proc start) ·
**Mercury-SOL untouched and active** since 2026-07-21 06:39, `NRestarts=0`.

**FOUR BOOT GATES, all green in the live journal:**
```
[ORDER-MODE]   🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
[RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 1 exchange position(s), 1 open row(s)
[RECONCILE]     SHORT open, SL present @ 64767.1 — kept.
[RECONCILE]     engine owns positions — NOT enqueueing a breakeven job (item 12a: single owner)
```
The `RECONCILE-XDB` line is the first time that gate has proven itself against a **live position**
rather than a flat book (previously `0 exchange position(s), 0 open row(s)`).

**THE OPEN POSITION — vpos 86, the first real-money position in this bot's history:**

| | |
|---|---|
| side / size | **SHORT 0.0023 BTC @ 63686.0** · $147.28 notional · 5x · margin $29.30 |
| opened | 2026-07-30 00:50:14 UTC |
| stop | **64767.1**, `original_sl_price` identical · 1R = 1081.1 pts |
| **exchange stop order** | **`2082629881359347712`** `STOP_MARKET BUY posSide=SHORT qty=0.0023 stopPrice=64767.1 closePosition=true workingType=MARK_PRICE status=NEW` |
| exchange position | `positionId 2082629807737368578`, avgPrice 63686.0, amt 0.0023, SHORT |
| both probes agree | unified `fetch_positions` **and** raw `swapV2` — 1 position, 1 order, no orphans |
| at 03:15 | mark ~64159 · uPnL ~**−$1.09** · **−0.44R** · stop **+0.56R away** |
| 🔴 **at 11:10** | mark **64600.0** · uPnL **−$2.10** · **−0.845R** · stop **+0.155R away (167 pts)** |
| trail | **NOT ARMED** (arms at +1R = 62604.9) · breakeven not applied · MFE never exceeded **+0.099R** |
| `recheck_status` | **`tightened`** — terminal, deliberately NOT resumed (§2.20) |

**The stop order id is UNCHANGED across the 02:51 restart** — not cancelled, not re-placed.

**Balance:** `USDT free 482.13 · used 29.30 · total 511.43` (used == the $30 margin).

**Flags — every value read from `config` at 03:15 with runtime==commit proven:**

| flag | value |
|---|---|
| 🔴 `LIVE_TRADING_ENABLED` | **True** |
| 🔴 `ORDER_ADAPTER_LIVE` | **True** |
| `ROUTING_MIGRATED_TO_ADAPTER` / `PASSIVE_FILL_RECONCILE_EXISTS` | True / True (both live gates disarmed) |
| `LEVERAGE` | 5 |
| `PAPER_FIXED_MARGIN_USDT` | 2000.0 ($10,000 notional — historical book) |
| `LIVE_FIXED_MARGIN_USDT` | **30.0** ($150 notional) |
| `FIXED_MARGIN_USDT` | 2000.0 — **dead in live**, reachable only from the unreachable legacy path |
| 🔴 `EXIT_ADVISOR_DRYRUN` | **False since `81875c9`, 2026-07-30 11:32 — THE ADVISOR CAN NOW CLOSE A POSITION.** It was never a one-line flip; see §2.23 / §2.24 |
| `EXIT_ADVISOR_HOURLY` | True |
| `WALL_TRAIL_LIVE_ENABLED` | False |
| `MAX_POSITIONS_PER_SIDE` | 1 |
| `POST_ENTRY_RECHECK_ENABLED` / `RECHECK_TIERS_SEC` | True / `[10, 60, 300]` |
| `SL_ATR_MULT` / `TRAIL_MULT_ATR` | 2.5 / 2.5 |
| `AI_ADVISOR_HIDE_1H` / `HTF_TOLERATE_NEUTRAL` | True / True |
| ⚠️ `EQH_EQL_SMART_TP_ENABLED` | True **(unreachable — see §2.6)** |

**Derived predicates:** `orders_are_real()=True` · `stop_lives_on_exchange()=True` ·
`active_fixed_margin()=30.0 → $150` · `engine_owns_position()=True`.

### 🔴 THE FOUR HONEST UNCERTAINTIES — partially resolved by the first live trade
Recorded at 19:30 before any live order existed. Status as of 2026-07-30:

1. **BingX behaviour on `closePosition='true'`** — **PARTIALLY resolved, and the important half is
   still open.** Placement, persistence, restart-survival (unchanged order id) and cancel/re-place
   are now observed on vpos 86. **The stop has never FIRED**, so the trigger behaviour — whole
   remainder closed, no second position, order against a zero position rejected — remains an
   assumption. The revert conditions in §1a stand unchanged.
2. **`_live_fill`: `filled == 0.0` is treated as a FULL fill** — **STILL OPEN.** Not exercised.
3. **Failure rate of `fetch_order_fee` unknown** — **STILL OPEN** (n=3 now, 0 failures; a rate still
   cannot be estimated).
4. ~~**No live path has ever executed against a real exchange.**~~ **RESOLVED for the ENTRY and STOP-
   PLACEMENT paths, and it found things** (the exit/stop-trigger path is still unexercised):
   the naked-position defect (`97a4fdb`), the size-mismatch alert naming the wrong number
   (`12b4df2`), and the 356 ms stop-churn window (§2.20) were all found by real execution, not by
   mocks — which is exactly what this uncertainty predicted.

**Titan crons — 4 daily + 1 weekly:**
`17 8` bull-regime · `29 8` chop-short · `35 8` volfloor · `53 8` regime-FLAT high-ADX ·
`11 8 * * 1` daily-trend-cohort (weekly)

**Book:** **1 open row** (`vpos 86`, LIVE) · 1 position on the exchange · they reconcile.
Last PAPER close: vpos 85 LONG **−137.32** (`reason=sl`, 2026-07-29 16:42:36).

---

## 8. 🔴 STANDING PUBLISHING RULE — never link a reused path

**A reused URL is served from CACHE.** `raw.githubusercontent.com` returns a stale copy when the
path has not changed. This is not theoretical: the operator's assistant received a **stale
mid-session version of this very file twice in one evening**, and this file's entire purpose is to
be read by a session with no memory — a stale copy shows closed items as open and open items as
closed.

**THE RULE, permanent:**
1. **Never send a link to a file whose path is reused.** Reports, diffs, patches, OPEN-ITEMS,
   registries — **anything** intended for the operator.
2. Every document is published as a **NEW dated file**: `reports/YYYY-MM-DD-HHMM-<name>.md`, and
   **that dated link is what gets sent**.
3. A canonical working file (like `OPEN-ITEMS.md`) **stays** as the working copy, but an
   **identical dated snapshot** is written alongside it and the **dated** one is sent.
4. **Patches always INLINE** in the `.md` as a fenced block, never a separate `.patch` file —
   **one link must be the complete document.**
5. Verification checks **200 AND a freshness marker in the body**. A cached response also returns
   200, so a status-code check alone would miss exactly this failure.

Gist raw URLs remain **blocked entirely** (robots-disallowed) — a gist link delivers an empty file.
Full reports go to the **`kola-reports` repo**; the secret/PII scan is **fail-closed before every
push** because the repo is public; Telegram gets a short decision summary **plus the single dated
raw link**, not the report body.

### 🔴 8a. EVERY CHECK GETS A DATED FILE AND A LINK — operator, 2026-07-30, SECOND OCCURRENCE
**A result that exists only in the terminal DID NOT HAPPEN.** §8 above already said this; it was read
as applying to *reports* rather than to *checks*, and that reading is now closed.

- **EVERY check gets a NEW dated file and a delivered raw link. However small. Including one-line
  answers. Including "nothing has changed yet" and "not due for another 40 minutes".**
- **§8 is NOT "when asked". The report IS the deliverable.**
- **If a check is too small to write up, write it up in THREE LINES — but write it up.**

**Both violations on the day it became a rule, recorded rather than smoothed over:** a query answering
*"did the post-fix sampler row land"* delivered in the terminal only, and a pending-item follow-up
held back for "when the monitor fires" instead of delivered on the check that had already run.
**Two occurrences is what makes it a rule instead of a lapse.**

Durable memory: `feedback_dated_snapshot_never_reused_urls`, `feedback_every_check_gets_a_link`.

---

## 9. 🔴 HOW THIS FILE REGRESSED, AND THE RULE THAT PREVENTS IT
**Seventh instance of the "label lies" class — in the one file whose entire job is to be true for a
session with no memory.** Recorded here rather than quietly fixed, because a regression in the safety
document is worse than the defects it records.

### What happened — the canonical file was the stale branch, not the snapshot generator
The 2026-07-30 03:00 snapshot carried the **2026-07-29 14:00** header — *"Titan is a BTC swing
paper-trading bot. `LIVE_TRADING_ENABLED = False`. All P&L below is paper P&L."*, HEAD `41c4a4d` —
while §2.19–§2.22 in the same file described **real-money incidents with real BingX order IDs**.

**Diagnosis, from git rather than memory:**

```
canonical reports/OPEN-ITEMS.md   last touched  c376879  2026-07-29 13:54:54   <-- FROZE HERE
Titan went live                            cb3a8bb  2026-07-29 19:13:33
six dated snapshots published after 14:00: 1735 · 1815 · 1955 · 2005 · 2030 · 2132
                                           ^ the LIVE header, §1 CLOSED and the
                                             first-live-trade section were written
                                             into THESE and never back into canonical
```

**So the canonical file forked from the truth at 13:54 on 2026-07-29 and the dated snapshots became
the real document.** The 03:00 snapshot was generated from the *current canonical file* — which is
the correct procedure — but the canonical file was the **stale branch**, 145 lines behind
`2026-07-29-2030-open-items.md` (739 vs 884 lines). Appending new sections to it published a
document that contradicted itself.

**The defect is not "generated from the wrong source". It is that there are TWO sources and nothing
reconciles them.** A canonical file that is not written back to is not canonical; it is a stale copy
with an authoritative name — which is the same shape as every other item in this file: *a label that
says something the thing does not do.*

### The rule, from now on
1. **The canonical `reports/OPEN-ITEMS.md` is the ONLY base.** Every dated snapshot is generated
   **from it**, and every edit is written **back into it in the same commit**. If a session ends with
   a dated snapshot newer than canonical, canonical is broken — treat it as an incident.
2. **Before publishing, the header is VERIFIED AGAINST RUNTIME, never copied forward.** The three
   header claims — mode flags, sizing, HEAD — are each checked against a live source: `config` import
   for the flags, `active_fixed_margin()` for the sizing, `git rev-parse HEAD` for the commit. This
   session's §7 was rebuilt that way; the 19:30 block was copied forward, and that is the difference.
3. **A mode claim and a P&L claim must never live in prose alone.** The split is stated as an
   executable predicate — `stop_order_id IS NOT NULL` — so a reader can re-derive it instead of
   trusting a sentence that may have gone stale. Prose describing state is exactly what rotted here.
4. **If the generation is manual, that IS the defect** — stated plainly, because it currently is.
   The reconciliation above is a discipline, not a mechanism, and disciplines are what failed twice
   in this file already (this section, and the "3 consults" line in §5 that went un-updated for
   weeks). **The durable fix is a publisher that refuses to emit a snapshot whose header disagrees
   with runtime flags, and refuses to emit one whose base is not canonical.** That is NOT built. It
   is recorded here as the open item it is, rather than closed with a promise to remember.
