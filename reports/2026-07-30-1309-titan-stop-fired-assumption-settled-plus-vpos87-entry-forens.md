# titan-stop-fired-assumption-settled-plus-vpos87-entry-forensics-adx-window-defect

_2026-07-30 13:09 UTC_

---

# TITAN — the stop FIRED (assumption settled) + full entry forensics on the new LONG

_2026-07-30 13:10 UTC · HEAD `81875c9` · 🔴 LIVE, REAL MONEY · vpos 87 LONG open_

---

## DECISION LINE

**PART 1 — no revert condition is met. The `closePosition='true'` assumption held on its first real
firing.** The SHORT is **exactly zero** on both probes, **no** residual and **no** reversal, the stop
filled the **whole** 0.0023 in one child order, **zero** orphan orders, and the row was finalised by
the **passive-fill** path from the **REAL** order — price and fee **read back**, not estimated.
§7 uncertainty 1 can be closed. §1a's revert conditions stay on the page but were **not** triggered.

**PART 2 — you have item 8 exactly right, and the forensics turned up something bigger than the
question asked.** 🔴 **The bot computes 1h ADX on TWO DIFFERENT WINDOWS and renders the difference as
a CHANGE.** The entry path uses 200 candles (converged); the post-entry recheck and the exit-advisor
sampler use `ATR_LEN*3 = 42` candles, where Wilder's double smoothing has not warmed up. Measured on
**800 paired readings**: the 42-bar figure runs **+6.23 mean / +5.38 median** high, and
**`ADX_BELOW_FLOOR = 20` misses 52.9% of genuinely-below-floor states.**

Live consequence on vpos 87, 25 seconds apart, same bot, same timeframe:

```
entry snapshot   ADX1h = 13.5   (200 candles — converged)
recheck T+10s    ADX1h = 25.4   ( 42 candles — warm-up artefact)
exit prompt      "At entry: ADX1h=13.5   Now: ADX1h=25.4"
advisor read it  "Regime strengthened: ADX15m=46.8 (strong trend)"
```

**The +11.9-point ADX rise did not happen.** It is the same defect class as §2.19 — the entry
reference and the live reading come from different measurements and the difference is presented as
movement — and the §2.19 guard did not catch it because that guard covers *book* provenance only.

**Nothing was changed. This is a read-only report.**

---

# PART 1 — THE STOP FIRED. THE ASSUMPTION IS SETTLED.

Everything below is read off BingX at 12:40–13:05 UTC through both probes, plus the journal.

## 1 · Position: the SHORT is exactly ZERO. No residual, no reversal.

**Unified `fetch_positions(['BTC/USDT:USDT'])`** — one entry, and it is the NEW long:

```
symbol BTC/USDT:USDT  side long  contracts 0.0023  entryPrice 64838.7  notional 149.17
```

**Raw `swapV2PrivateGetUserPositions({'symbol':'BTC-USDT'})`** — verbatim, one element:

```json
{"positionId":"2082799688088776706","symbol":"BTC-USDT","positionAmt":"0.0023",
 "availableAmt":"0.0023","positionSide":"LONG","avgPrice":"64838.7","isolated":false,
 "initialMargin":"29.8258","unrealizedProfit":"0.0366","realisedProfit":"-0.0746",
 "leverage":"5","liquidationPrice":"0","markPrice":"64854.6"}
```

**There is no `positionSide: "SHORT"` element at all** — not a zero-size one, not a reversed one.
vpos 86's `positionId 2082629807737368578` is gone from both probes. **Neither revert condition in
§1a is met.**

## 2 · Open orders: ZERO on the short side, one on the long side, no orphans of any type.

Both probes return **exactly one** order, and it is the new LONG's protective stop:

```
id 2082799690256592896  type STOP_MARKET  side SELL  positionSide LONG  origQty 0.0023
stopPrice 64028.8  workingType MARK_PRICE  closePosition "true"  reduceOnly true  status NEW
positionID 2082799688088776706        <-- bound to the live LONG, not to a ghost
```

No `STOP_MARKET` on the SHORT side. No `TAKE_PROFIT_MARKET`. No `TRAILING_STOP_MARKET`. No unfilled
`LIMIT`. **Exactly one `closePosition` order exists on the symbol** — the §1a invariant holds through
a stop firing, which is the one transition it had never been tested across.

⚠️ **One honest gap in the evidence.** I can prove the book is clean **now**. The passive-fill path
does **not** run an orphan sweep — `_reconcile_passive_fill` hands the fill straight to `_do_close`
and never reaches `_execute_close_position`, so neither the cancel loop nor `_cancel_stop_orders`
ran, and **no journal line asserts the book was clean between 11:50:48 and 12:05:17.** Here it
cannot matter (the stop was the only order and it filled), but that is a property of *this
configuration*, not of the code. If a TP or a DCA limit ever coexists, a passive fill will leave it.

⚠️ **A caveat on that `reduceOnly: true`.** Both the filled child and the live LONG stop carry
`reduceOnly: true`, set by **BingX**, not by us. Our own code must still never send `reduceOnly` —
hedge mode rejects it with `109400` (2026-07-29). The venue setting it on its own trigger children is
not permission for us to set it.

## 3 · The stop order's final state — and a BingX behaviour worth writing down

`fetch_order('2082629881359347712')` **does not return the order you asked for.** It returns the
**child execution order**, with a back-pointer:

```json
{"orderId":"2082796043553173508","triggerOrderId":"2082629881359347712",
 "symbol":"BTC-USDT","side":"BUY","positionSide":"SHORT","type":"STOP_MARKET",
 "origQty":"0.0023","executedQty":"0.0023","avgPrice":"64733.0","cumQuote":"149",
 "stopPrice":"64767.1","profit":"-2.4081","commission":"-0.074443","status":"FILLED",
 "workingType":"MARK_PRICE","reduceOnly":true,"closePosition":"false",
 "positionID":"2082629807737368578","time":"1785412247000","updateTime":"1785412247926"}
```

| | |
|---|---|
| status | **FILLED** |
| filled qty | **0.0023 of 0.0023 — the WHOLE size, not partial** |
| average price | **64733.0** |
| fee | **0.074443 USDT** (`commission: -0.074443`) |
| trigger → fill | `time` 11:50:47.000 → `updateTime` **11:50:47.926** — **926 ms** |
| booked P&L | `profit: -2.4081` = `(63686.0 − 64733.0) × 0.0023` ✓ |
| bound to | `positionID 2082629807737368578` = vpos 86's exchange position ✓ |

🔴 **The behaviour to record: our `stop_order_id` is the TRIGGER id, and the order that fills is a
DIFFERENT id.** Reconciliation works only because BingX resolves a trigger id to its child. That is
an **undocumented convenience we now depend on**. If BingX ever returned the trigger object instead
(status `TRIGGERED`, no `avgPrice`), `read_filled_protective_order` would fall through to
`fetch_ticker(...)['last']` and book an **invented** exit price on a real trade. Worth a guard; not
built, not proposed here.

## 4 · WHICH PATH closed the row — passive-fill reconciliation. Journal, verbatim:

```
11:50:48  [VPOS-FILL] passive fill vpos=86 BTC/USDT:USDT SHORT: stop-loss filled @ 64733.0 fee=0.074443 reason=sl
11:50:54  VIRTUAL CLOSE vpos=86 SHORT avg_entry=63686.0000 exit=64733.0 net_pnl=-2.5416 reason=sl cycles=31/30
```

**Passive, not active.** There is no `[EXIT-ADVISOR-ACT]` line, no `[STOP-CLEANUP]` line and no
`create_market_order` in the window — the active close path was never entered. Item 13
(`d63cb8b`) did the work, on its **first real firing**, and the exchange detected-to-reconciled
latency was **~1.1 s** (fill 11:50:47.926, reconciliation 11:50:48).

**Finalised from the REAL order, proven by identity rather than by claim.** `_reconcile_passive_fill`
passes `_exit_fill={'fill_price': …, 'fee_cost': …, 'simulated': False, 'order': …}` into `_do_close`,
which then *cannot* re-derive a price. Every stored number matches the venue:

| | DB (`virtual_positions` 86) | BingX |
|---|---|---|
| close_price | **64733.0** | avgPrice **64733.0** |
| exit fee | 0.074443 (in `total_fees`) | commission **0.074443** |
| gross_pnl | **−2.4081** | profit **−2.4081** |
| total_fees | 0.147682 | entry 0.073239 + exit 0.074443 = **0.147682** ✓ |
| funding_paid | **−0.014208** (credited to us) | — |
| net_pnl | **−2.541574** = −2.4081 − 0.147682 + 0.014208 ✓ | — |
| R | −2.541574 / 2.48655500 = **−1.02213R** | — |

🔴 **AND THE TIMING YOU SHOULD SEE.** `exit_advisor_last_ts` on the row is `1785408671.085` =
**10:51:11**, so the next hourly consult was due **11:51:11**. The stop filled at **11:50:47.926** —
**23.1 seconds earlier**. The 11:39 report predicted exactly this outcome in advance, and that is
what happened. But see item 7a: it does **not** mean vpos 86 produced no evidence.

## 5 · THE 34-POINT GAP — mechanism established, systematic-ness DENIED by measurement

Trigger **64767.1** on `workingType MARK_PRICE`; fill **64733.0** against BingX's own book. Favourable
by **34.1 points ≈ 0.053% ≈ 0.031R ≈ $0.078**.

**The mechanism is structural: the trigger reference and the execution reference are two different
prices.** The trigger watches the **mark** price; the market order that follows executes against
**BingX's own ask**. They only have to agree on average, not at the instant.

**What the venue shows happened.** The 1-minute candle that contains the fire is violent:

| 11:50 candle | O | H | L | C | vol |
|---|---|---|---|---|---|
| last price | 64645.0 | **64820.0** | 64645.0 | 64820.0 | **198.4 BTC** |
| mark price | 64645.1 | **64826.1** | 64645.1 | 64820.1 | — |

A **+175-point vertical move inside 60 seconds** on ~198 BTC — roughly 5× the neighbouring minutes.
The stop fired 47.9 s into it, mid-ascent, and filled 34 points below the level the mark had already
crossed. For ~1 second the mark led BingX's tradeable price by 34 points.

🔴 **Is it systematic? NO — and I measured that rather than assuming it.** Over **1,000 paired 1-minute
mark/last candles**:

| statistic | mark_high − last_high | mark_close − last_close |
|---|---|---|
| mean | **+0.41** | +1.25 |
| median | **0.00** | +0.30 |
| sd | 3.02 | 1.93 |
| p99 | +7.3 | +8.8 |
| \|diff\| > 20 pts | 4 of 1000 (0.4%) | 0 |

And on the **20 high-volatility minutes** (last-price range ≥ 100 pts) the extreme is **max +6.1**.

**So 34 points is NOT a standing basis — the standing basis is ~zero.** It is a transient,
sub-minute divergence manufactured by the spike itself. Three consequences, stated plainly:

1. **Do not budget +34 points per stop.** n = 1.
2. 🔴 **The sign is not guaranteed.** This divergence is favourable when the mark *leads* the venue.
   When BingX's own book leads the index instead, the mark reaches the trigger **late** and the fill
   is **worse** than the trigger. Nothing here makes one more likely than the other.
3. **Do not conflate this with §1's "+36.91 in the book's favour over 101,739 candles."** That figure
   is about wick-triggering versus a polled `last`. Different mechanism. The numerical coincidence is
   a coincidence.

**Why I cannot go further, said rather than papered over:** BingX's finest kline is **1 minute**
(`ex.timeframes` has no `1s`/`5s`) and there is no historical trade tape at 50 minutes old. The whole
event lasted 926 ms. **Which of mark or last led is therefore unobservable after the fact.**
**The cheap fix — not built, recommended:** log `(trigger_price, fill_price, mark_at_fill,
last_at_fill)` on every stop fire. One line, and in ten fires it becomes a distribution instead of an
anecdote.

## 6 · The fee: **READ BACK from BingX. Not estimated.**

`read_filled_protective_order` takes `order['fee']['cost']`, and only falls back to
`exit_price × amount × TAKER_FEE_RATE` when that is absent — printing `[BE-FILL] fee not reported …
ESTIMATED` when it does. **That line does not appear in the journal.** Proof by identity:
`0.074443` is BingX's own `commission` string, to six decimals. An estimate would have been
`64733.0 × 0.0023 × 0.0005 = 0.0744430` — numerically the same here, which is exactly why the
journal line, not the arithmetic, is the evidence. §7 uncertainty 3 goes to **n = 4, 0 failures**;
a failure *rate* still cannot be estimated.

## 7 · `reason='sl'` confirmed at the source, and both consumers recorded it

**`reason='sl'`, not `'breakeven'` — decided from the row, not guessed.** The passive path reads the
row's own management state:

```python
_mgmt = json.loads(row['pending_dca_limits'] or '{}')
_reason = 'breakeven' if bool(_mgmt.get('breakeven_applied', False)) else 'sl'
```

and vpos 86's stored state is `{"breakeven_applied": false, "exit_advisor_last_ts": 1785408671.085}`.
`close_reason` in the row is **`sl`**. Breakeven never applied (it arms at +1R = 62604.9; the position
never went better than `water_mark 63578.5`, i.e. +0.10R).

| consumer | recorded? | evidence |
|---|---|---|
| **batch counter** | ✅ | `trades` row 19589 now carries `batch_number = 2` and `pnl = -2.541574` — the `reason in ('sl','trail','post_entry_critical','ai_exit')` callback fired |
| **post-exit observatory** | ⚠️ **recorded, onto the WRONG ROW** — see 7b | `post_exit_observatory` id 79, `status='shadow_completed'`, `real_close_price 64733.0`, `real_close_reason sl`, `real_net_pnl −2.541574`, `real_pnl_r −1.02213`, `exit_advantage_r +0.42525` |

### 7a · 🔴 vpos 86 DID produce clean evidence — NINE clean `close` verdicts, all ignored

The 0330 OPEN-ITEMS lists four consults on vpos 86, all contaminated (pre-`625fedc`). **It has since
produced nine more, every one of them AFTER the 02:51:11 fix deploy**, and every one said `close`:

| trades row | UTC | verdict | price at nearest excursion sample | net if closed | R |
|---|---|---|---:|---:|---:|
| 19607 | **03:50:29** | `close` | 64191.30 (03:52:45) | **−1.3092** | −0.527 |
| 19617 | 04:50:34 | `close` | 64060.00 | −1.0071 | −0.405 |
| 19624 | 05:50:43 | `close` | 64038.70 | −0.9581 | −0.385 |
| 19628 | 06:50:53 | `close` | 63961.00 | **−0.7793** | **−0.313** |
| 19633 | 07:50:54 | `close` | 63970.00 | −0.8000 | −0.322 |
| 19646 | 08:45:12 | `close` | 64309.20 | −1.5806 | −0.636 |
| 19649 | 08:51:02 | `close` | 64288.30 | −1.5325 | −0.616 |
| 19660 | 09:51:11 | `close` | 64549.70 | −2.1340 | −0.858 |
| 19678 | 10:51:14 | `close` | 64569.20 | −2.1789 | −0.876 |
| — | **11:50:48** | **ACTUAL** | **64733.00** | **−2.541574** | **−1.02213** |

**All nine beat the actual exit.** The first of them (03:50:29) by **+$1.2324 = +0.495R**; the best
(06:50:53) by **+$1.762 = +0.709R**.

🔴 **I am NOT counting this toward §2.4, and the reason is the discipline, not the number.** The
criterion says *first `close` verdict, no re-cutting the sample*. vpos 86's **first** `close` verdict
was 01:50:24 — **contaminated**. Calling 03:50:29 "the first" is precisely the re-cut the criterion
forbids. **That is your call, not mine**; I have put both readings on the table with the arithmetic
done so it can be decided by rule:

- **STRICT** (position-level contamination): vpos 86 does not count. §2.4 stays **0 of ~10**.
- **LENIENT** (first *clean* verdict): vpos 86 counts as **IMPROVED, +$1.23 / +0.495R**. §2.4 → 1 of ~10.

🔴 **And there is a NEW reason to prefer STRICT that has nothing to do with the book: every one of
those nine "clean" prompts carried a warm-up-biased ADX** (Part 2, item 9a). Row 19590's own text —
*"bearish regime (ADX rising to 14.9)"* — is that artefact: entry ADX1h was 11.1 on 200 candles, and
"14.9" is a 42-candle reading of the same hour. **The §2.4 sample is contaminated a second time, by a
second seam.** I am not proposing a third restart — that is a decision, and it belongs to you.

**The operational fact, separate from the criterion:** the advisor said `close` **twelve times over
nine hours**, was mute for the first eleven by `DRYRUN`, was armed at 11:32:45, and the stop then beat
its next turn by 23 seconds. **The arming was correct and it still bought zero datapoints.**

### 7b · 🔴 THE OBSERVATORY STAMPED vpos 86'S CLOSE ONTO A GHOST ROW

`post_exit_observatory` id 79 says `vpos_id = 86`. Its entry data is **not vpos 86's**:

| field | observatory row 79 | `virtual_positions` 86 |
|---|---|---|
| entry_price | **63605.6** | **63686.0** |
| original_sl_price | **64724.6** | **64767.1** |
| opened_at | **2026-07-29T21:50:04** | **2026-07-30T00:50:14** |

**Three hours and 80.4 points apart — these are two different positions.** `on_entry` upserts with
`ON CONFLICT(vpos_id) DO NOTHING`, so when the real vpos 86 opened it wrote **nothing**; `on_real_close`
then stamped today's real outcome onto the stale row. The result is a record that **mixes two books**:

```
shadow leg  : entry 63605.6, orig SL 64724.6  -> risk 1119.0 -> shadow_pnl_r -0.5969   (GHOST)
real   leg  : exit 64733.0, net -2.541574     -> real_pnl_r  -1.02213                  (REAL)
headline    : exit_advantage_r = +0.42525                                              (MIXED)
```

Recomputed on vpos 86's **own** numbers (entry 63686.0, risk 1081.1, shadow exit 64273.5):
shadow R = **−0.5434**, advantage = **+0.4787R**, not +0.4253R. The sign survives here; the
mechanism can flip one elsewhere. **This is §2.19's class in a third place.**

**Two more facts from the same corner, offered without a theory of cause:**

- `post_exit_observatory` also holds **id 80, `vpos_id = 89`** — SHORT, entry **63595.5**, orig SL
  **64714.5**, opened **2026-07-29T21:50:11** — and `virtual_positions` has **no row 88 or 89**, with
  `sqlite_sequence` at **87**. `recheck_events`, `position_excursion_samples` and
  `smart_exit_dryrun_samples` know only 86 and 87. So two observatory rows describe positions that
  `virtual_positions` does not contain, both stamped **2026-07-29 21:50**, i.e. inside the
  naked-position window. The OPEN-ITEMS caveat *"the naked short has no `virtual_positions` row"*
  stays true — but **it does have a surviving record, with an entry price and a stop, and nobody knew.**
- Row 80 is **still live**: `updated_at 2026-07-30T02:00:14`. The 02:00 15m signal armed a shadow exit
  on it. **A phantom position is accumulating shadow data today.**

**I changed nothing.** Deleting or repointing observatory rows is a data decision, and
`feedback_no_delete_virtual_positions` is standing.

---

# PART 2 — THE NEW LONG. FULL ENTRY FORENSICS (READ-ONLY)

`vpos 87` · LONG 0.0023 BTC @ **64838.7** · opened **12:05:17.4998** · stop **64028.8**
(`original_sl_price` identical, 1R = 809.9 pts = 1.249%) · exchange stop `2082799690256592896` ·
entry fee **0.074565** read back · `initial_risk_usdt 1.86282508` · `trades` row **19713**.

## 8 · THE GATE ARITHMETIC — you have it exactly right, with one correction

**The comparison actually performed** (`main.py:3645–3651`, the plain-5m entry path this trade took):

```python
_macro_ctx     = macro_filter.build_macro_context(direction)   # DXY + crypto news + macro calendar
_macro_gate_adj = _macro_ctx['total_gate_adj']                  # ==  0.0  for this entry
_gated_score   = round(direction_score + _macro_gate_adj, 2)    # == 4.25 + 0.0  = 4.25
_eff_thr       = (CONFLUENCE_FLAT_THRESHOLD                     # 5.0, only if regime == 'FLAT'
                  if matrix_result.get('market_regime') == 'FLAT'
                  else CONFLUENCE_SCORE_THRESHOLD)              # == 2.0   <-- the effective bar
if _gated_score < _eff_thr:      # 4.25 < 2.0  -> False  -> ENTRY PROCEEDS
```

✅ **`CONFLUENCE_SCORE_THRESHOLD = 2.0` was the effective bar** — `market_regime` was `TREND`, so the
`FLAT` floor of 5.0 never applied.

✅ **`thr=4.0` is display-only.** It is `matrix_result['threshold']` =
`LIQUIDITY_HEATMAP_TREND_THRESHOLD`. Its only two consumers in the entire codebase are
`signal_matrix.format_for_telegram` (line 551, the card) and the `trade_signal_matrix` snapshot table.
**It is never compared to anything.**

🔴 **The correction — `3.63` is not what the gate saw, and it is worse than display-only.** The value
compared was **4.25**, not 3.63. The 3.63 comes from a **second, entirely separate** adjustment
computed **after** the gate has already passed (`main.py:3789`), from the journal verbatim:

```
weighted_adj P2: dir=LONG raw=4.25 adj=-0.6212 final=3.63
  breakdown={'ema_cross_15m': 0.04, 'ema_cross_1h': 0.04, 'ema_slope_15m': 0.0287,
             'ema_slope_1h': 0.02, 'dxy': 0.0, 'news': -0.5, 'funding': -0.25}
```

`weight_engine.py`'s own docstring is explicit: *"Gate policy: `weighted_adj()` is NEVER applied to
the raw `direction_score` that gates entry. Only the stored `confluence_score` uses it."*

**Half of that sentence is also false.** `adj_score` appears in exactly three places: a `print`, the
`confluence_score=adj_score` update kwarg, and the Telegram card. And then **`signal_matrix.snapshot()`
runs at `main.py:3996` and overwrites the column with the RAW score** —

```python
"UPDATE trades SET confluence_score=?, ... WHERE id=?", (res['score'], ...)
```

— which is why `trades.19713.confluence_score` reads **4.25**, not 3.63. **So `−0.6212` gates nothing
and is not persisted anywhere.** The only number in the pipeline that both moves the score *and*
reaches the gate is `macro_filter`'s `total_gate_adj`, and it was **0.0**.

**Two numbers named "the adjusted score", one of them documented as stored and in fact discarded.**
Fourth instance in this file of *check what the label SAYS, not only what the gate DECIDES.*

## 9 · ADX 1h = 13.52 — second consecutive sub-floor entry. Two draws, not yet a pattern.

**Your reading of the mechanism is correct and I have nothing to add to it:** `CONFLUENCE_FLAT_THRESHOLD`
binds only on `market_regime == 'FLAT'`, and `market_regime` is *signal presence*, not a measurement,
so 13.52 was never eligible to block anything (§2.13, and the 07-29 regime study which found high ADX
marks the skips that were RIGHT).

**Measured, on executed entries since the forming-candle fix (`t.timestamp >= '2026-07-04 11:58'`),
using `srv_adx_1h` — the 200-candle converged reading:**

| | |
|---|---|
| executed entries in window | **23** (all 23 have `srv_adx_1h`) |
| **ADX1h < 20 at entry** | **6 of 23 = 26.1%** |
| median ADX1h at entry | **24.00** |
| entries with `market_regime='FLAT'` | **2** — the only state where the floor could ever bind |
| decade distribution | 10s: **6** · 20s: 11 · 30s: 5 · 40s: 1 |

Last ten executed entries, `(row, ADX1h)`:

```
(17092, 25.1) (17241, 21.7) (17895, 30.4) (18108, 20.5) (18699, 16.9)
(19021, 26.3) (19214, 30.7) (19468, 16.7) (19589, 11.1) (19713, 13.5)
```

**Answer: two draws, not a pattern — but not a coincidence either.** 26.1% base rate over 23 entries
means two-in-a-row has a ~6.8% chance under independence, which is unremarkable. **What is
remarkable is the tail**: 3 of the last 4 are sub-floor and the two lowest ADX1h readings in the whole
23-entry history are the two most recent trades. **That is a watch item with n=2, not a finding.**
Outcome-wise the cohort says nothing yet: on the closed cohort, entry ADX1h < 20 is **n=2, totR
−0.05**, versus ADX1h ≥ 20 at **n=14, totR −4.87**. Both under-powered; do not act on either.

### 9a · 🔴🔴 THE REAL FINDING — ONE ADX, TWO WINDOWS, AND THE DIFFERENCE IS SOLD AS A CHANGE

**The tell.** vpos 87's own recheck row, 13 seconds after the entry snapshot:

```
recheck_events id 37   vpos 87  tier 10s   adx_1h = 25.3505   adx_delta = -11.834   verdict OK  health 0
virtual_positions 87                      entry_adx_1h = 13.5163
```

**Two 1-hour ADX readings of the same hour, 13 seconds apart, differing by 11.83 points (+88%).**

**Root cause, isolated to one argument.** Two code paths, two candle windows:

| path | fetch | ADX warm-up |
|---|---|---|
| entry snapshot | `indicators._fetch_ohlcv_cached(..., CANDLE_LIMIT=200)` | converged |
| **recheck** | `virtual_trader.py:1541` `fetch_ohlcv(symbol,'1h', limit=ATR_LEN * 3)` = **42** | **not warmed up** |
| **exit sampler** | `virtual_trader.py:1805` `_tf_metrics_safe(...)` `limit=ATR_LEN * 3` = **42** | **not warmed up** |

ADX(14) is **doubly** Wilder-smoothed (DX, then a second smoothing), so it needs far more than
`14 × 3` bars. Reproduced live, same instant, same symbol:

```
1h limit= 42  ADX14 = 25.640      <-- what the recheck and the exit sampler use
1h limit= 60  ADX14 = 15.063
1h limit=100  ADX14 = 13.961
1h limit=150  ADX14 = 13.838
1h limit=200  ADX14 = 13.834      <-- what the entry snapshot uses
1h limit=300  ADX14 = 13.834      <-- converged; 200 IS the right answer
```

**Scope is TIGHT, and I checked rather than assumed — it is ADX and ONLY ADX.** Same two windows,
same call:

| metric | 42 bars | 200 bars | verdict |
|---|---|---|---|
| ATR 1h | 314.434 | 317.352 | −0.9% — **negligible** |
| trend 1h | `bull` | `bull` | **identical** |
| ema_gap 1h | 0.3551 | 0.3548 | **negligible** |
| **ADX 1h** | **22.305** | **15.450** | 🔴 **+44%** |
| **ADX 15m** | **49.559** | **45.280** | 🔴 **+4.3 pts** |

The comment at `virtual_trader.py:683` — *"Wilder is window-sensitive, so faithful alignment needs
the same limit, not just the algo"* — **is right, was written for ATR, and is violated for ADX.**

**Magnitude, over 800 paired readings on 1,000 real 1h candles:**

```
ADX42 - ADX200 :  mean +6.23   median +5.38   sd 10.04   min -22.29   max +52.16
  |diff| > 5   :  484 of 800  (60.5%)
  |diff| > 10  :  285 of 800  (35.6%)
  ADX42 > ADX200 in 593 of 800 (74.1%)   <-- biased HIGH, not merely noisy
```

🔴 **What it does to the only ADX rule with teeth** — `ADX_BELOW_FLOOR = 20.0`, worth **−5**, and
`HEALTH_SCORE_TIGHTEN = −5`, so that rule **alone** decides TIGHTEN:

```
truly < 20 (200-bar)              : 221 of 800
MISSED  (true <20, 42-bar >=20)   : 117   ->  52.9% of all true-below-floor states
FALSE   (true >=20, 42-bar <20)   :  56
agreement rate                    :  78.4%
```

**The floor misses more than half of the states it exists to catch.** And the companion rule is
biased the same way: `adx_drop` computes `entry_adx (200-bar) − cur_adx (42-bar)`, so a
systematically-high `cur_adx` makes the difference systematically negative and the rule
systematically silent. **Both ADX rules in the recheck are biased toward "healthy".**

**Concretely, on the live position:** vpos 87's true entry ADX1h is 13.5, well under the floor. Had
the recheck read the same window, `_health_score` would have returned **−5 → TIGHTEN**, on all three
tiers. **The three "Health 0, verdict OK" readings you are looking at are artefacts of the fetch
limit.**

🔴 **And it reaches the exit advisor as a fabricated trend.** From vpos 87's stored exit prompt,
verbatim:

```
Regime at ENTRY vs NOW
  At entry: regime=TREND 1d=neutral 4h=bull 1h=bull ADX1h=13.5
  Now:      15m=bull 5m=bull ADX1h=25.4 ADX15m=46.8
```

`13.5` is the 200-bar entry column; `25.4` is the 42-bar live column. **The prompt asserts an
11.9-point ADX rise across 25 seconds that did not occur**, under a heading that says the two numbers
are comparable — and the advisor read it exactly as intended: *"Regime strengthened: ADX15m=46.8
(strong trend)"*. Row 19590's *"bearish regime (ADX rising to 14.9)"* on vpos 86 is the same artefact.

**This is §2.19 in a fourth place, and the §2.19 guard could not catch it** — `_exit_pct(col, value,
source)` makes *book* provenance mandatory. Nothing makes *indicator-window* provenance mandatory.
Every one of the **228+** `smart_exit_dryrun_samples` rows carries 42-bar ADX, so the chop-exit re-cut
in §2.16 would be run on biased data.

**Not fixed, not proposed as a patch here — this report is read-only. The shape of the fix, for when
you want it:** one window for one indicator (`_fetch_ohlcv_cached(..., CANDLE_LIMIT)` on both paths),
and a provenance guard of the §2.19 shape so a window cannot be borrowed silently. Awaiting your word.

## 10 · MOMENTUM intra-conflict — the category is ZEROED, outright

From `trades.19713.matrix_breakdown_json`, verbatim:

```json
"TREND":     {"long_points":2.5,  "short_points":0.0,  "intra_conflict":false, "contribution":2.50, "signal_count":2}
"MOMENTUM":  {"long_points":1.75, "short_points":2.5,  "intra_conflict":true,  "contribution":0.00, "signal_count":2}
"LIQUIDITY": {"long_points":2.5,  "short_points":1.25, "intra_conflict":true,  "contribution":0.00, "signal_count":3}
"EXECUTION": {"long_points":1.75, "short_points":0.0,  "intra_conflict":false, "contribution":1.75, "signal_count":1}
```

**Answer: zeroed. Not halved, and the majority side does NOT carry.** `contribution` is `0.0` for both
conflicted categories, and `2.50 + 0.00 + 0.00 + 1.75 = 4.25` — the score exactly.

🔴 **Note what that means here: the two categories that were silenced both leaned toward the SHORT
side of a LONG trade** (MOMENTUM S2.5 vs L1.75; 5M-STRUCTURE S1.25 vs L2.5 — mixed). **The
minority-zeroing rule removed the trade's only internal dissent.** The score the gate saw, 4.25, is
composed *entirely* of the two categories that agreed with the direction. §2.22 already flagged that
whether this rule should fire at all is open; this entry is what it looks like in live money.

**Outcome data, and it is under-powered — I am not going to dress it up.** Applying all four §0
filters gives the **strict clean closed cohort n = 11**, in R (which normalises the two sizing eras):

| cohort | n | wins | totR | meanR | medR |
|---|---:|---:|---:|---:|---:|
| MOMENTUM intra-conflict | **4** | 1 (25%) | **−2.61** | −0.652 | −1.090 |
| MOMENTUM clean (present) | **3** | 2 (67%) | **+0.74** | +0.247 | +0.343 |
| MOMENTUM absent | 4 | 2 (50%) | −1.02 | −0.254 | −0.482 |
| **ANY** category conflicted | **7** | 2 (29%) | **−3.30** | −0.471 | −1.087 |
| **NO** category conflicted | **4** | 3 (75%) | **+0.41** | +0.104 | +0.233 |

By side: LONG conflicted **n=1** (−1.20R) vs LONG clean **n=2** (+0.40R); SHORT conflicted **n=3**
(−1.41R) vs SHORT clean **n=1** (+0.34R).

Dropping the wall-trail filter to widen it (n=16) keeps the direction — conflicted 5 at −2.89R,
clean 6 at −0.71R, absent 5 at −1.32R; ANY-conflicted 10 at −4.61R vs NO-conflict 6 at −0.31R.

🔴 **Verdict: n = 4 versus 3. That is a direction, not a finding, and the direction is consistent
across both cuts and both sides.** It costs nothing to keep counting; it would cost real money to act
on it. A clean-vs-conflicted split needs the same order of n as §2.2's armed-longs problem, which at
0.74 closed positions/day is months away. **Do not build a conflict filter from this table.**

## 11 · The news adjustment — it has NO path into the gate at all

**The path, traced.** There are **two** news-derived adjustments and they are not the same object:

| | producer | reaches the gate? | value here |
|---|---|---|---|
| `total_gate_adj` | `macro_filter.build_macro_context(direction)` — DXY + crypto-news CATEGORY + macro calendar | ✅ **YES**, inside `_gated_score` | **0.0** (`macro_news_category = NEUTRAL`) |
| `_w_adj` | `weight_engine.weighted_adj(...)` — EMA crosses/slopes, DXY, `news_overall`, funding, MTF | ❌ **NO** — computed after the gate | **−0.6212**, of which `news −0.5`, `funding −0.25` |

**So the −0.62 you saw was never overridden — it was never in the room.** `news_score −0.57`,
`news_impact high`, `news_overall NEG` fed `weight_engine`, which produced `news: -0.5`, which landed
in `adj_score = 3.63`, which reached a `print`, a card, and a DB column that
`signal_matrix.snapshot()` then overwrote. The macro *gate* penalty — the one that can actually block
— was `0.0`, because `macro_filter` classified the headline (*"Bitcoin ETFs on track for the smallest
monthly inflows ever"*, `macro_confidence 0.85`) as **NEUTRAL**, not `CRITICAL_NEGATIVE`.

🔴 **This is why "the machinery reduced the score and the trade cleared anyway" happened: nothing was
overridden, because nothing was enforced.** The sign flip is real and symmetric, which is the neatest
proof that it is inert — vpos 86, the SHORT, three hours earlier:

```
weighted_adj P2: dir=SHORT raw=5.75 adj=+1.5000 final=7.25   breakdown={... 'news': 0.5 ...}
```

**Same NEG news, opposite direction, `news` flips +0.5 / −0.5, and neither number touched a gate.**
(vpos 86's `+1.5000` is also the clip ceiling — the raw sum exceeded `[−1.5, +1.5]`, so even the
displayed figure was truncated.)

**Outcome data on the strict clean cohort — and it is n=1, so it settles nothing:**

| cohort | n | wins | totR | meanR |
|---|---:|---:|---:|---:|
| NEG + high impact | **1** | 1 (100%) | **+0.77** | +0.770 |
| NEG, any impact | 2 | 1 (50%) | −0.32 | −0.159 |
| POS, any impact | 3 | 0 (0%) | **−2.28** | −0.762 |
| NEU / none | 3 | 2 (67%) | +0.18 | +0.062 |

Widened to n=16: NEG-high **n=1** (+0.77R), NEG-any 4 (−1.35R), POS-any 3 (−2.28R), NEU 4 (−0.23R).
The single NEG-high datapoint is a **SHORT** — the aligned case — so **there is no prior at all for
the case in front of you: a NEG-high news read against a LONG. vpos 87 is the first.** The one
mildly interesting cell is that POS news is 0 for 3; also noise.

## 12 · THE BOOK — measured, because this one was consulted properly

**Verbatim order-book section of the stored entry prompt (`trades.19713.ai_user_prompt`), every
percentile and its source:**

```
Order book (pre-trade, 8000 levels):
  Mid: $64,844.75  |  Imbalance ±1%: 0.42 (ask-heavy)  — 5th pct
  Bid walls (>4x avg bucket vol): $64,632.50 (×4.5), $64,597.50 (×5.1)  — largest ×5.1 = 40th pct
  Ask walls (>4x avg bucket vol): $65,002.50 (×8.4), $65,222.50 (×5.2)  — largest ×8.4 = 77th pct
  Book depth: 3,276 BTC — 82th pct, sampled 44s ago
Order-book PERCENTILE scale (baseline: 24610 snapshots of this same OKX depth-4000 book)
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile: ~50th percentile is ORDINARY,
  not significant.
```

**Source: one book throughout — OKX `books-full` depth-4000, via
`liquidity_zones.fetch_pre_trade_walls`, ranked against `orderbook_density` where
`source = 'okx_books_full_4000'` (the only source present, 24,658 rows).** No cross-source figure.

✅ **I independently re-derived the percentile and it is correct**: the 77th percentile of
`max_wall_mult_ask` over the baseline is **×8.38**, and the prompt's wall is **×8.4**. The §2.3 /
§2.19 machinery is doing its job on the entry side.

**Was "notable but not blocking" a reasonable read?** **Yes, on the numbers that were in front of it,
and it named the distance implicitly:** the wall sits at **$65,002.50 = +163.8 pts = +0.253% above
the fill**, i.e. **+0.20R** away — inside the noise, so "not blocking" is about *where* it is at
least as much as *how thick*. Two things the advisor did not say, though, and they cut against it:

1. 🔴 **It quoted the 82nd-pct depth as support and never mentioned the 5th-pct imbalance.**
   `Imbalance ±1%: 0.42 (ask-heavy) — 5th pct` is the **most extreme figure in the block** and it is
   **against** the LONG. Its own reason cites depth (82nd) and the wall (77th) and is silent on the
   5th. That is a selective read of a correct prompt.
2. **Three different "imbalance" values existed at that instant, again** — 0.42 (OKX-4000, prompt,
   ask-heavy), **0.6994** (BingX ±1% band, `orderbook_json`, bid-heavy), **0.5748** (BingX-100,
   `virtual_positions.entry_ob_imbalance`). §2.22 deleted the misleading *label*; the **three
   divergent values under one word remain**, and here two of them point in **opposite directions**.

### The §4.4 mirror case: does it exist? Honestly — no, not at usable n.

§4.4 is 289 skips citing an ask wall above while SHORT, drifting −0.270%/4h (t = −4.6) — the best
vetoes in the book. The mirror is: **LONGs taken THROUGH a notable ask wall above.**

I parsed the largest ask-wall multiple out of every stored entry prompt (both formats: *"Massive ask
walls … (×N)"* pre-`8b15ecc`, and *"Ask walls … largest ×N = Mth pct"* after) and percentiled it
against the same 24,658-snapshot `max_wall_mult_ask` baseline the live code uses.

**Strict §0-clean closed cohort — the only cut that is methodologically sound:**

| cohort | n | wins | totR |
|---|---:|---:|---:|
| LONG · ask wall ≥ 77th pct (vpos 87's level) | **1** | 1 | +1.04 |
| LONG · ask wall 50–70th pct | 1 | 1 | +0.50 |
| LONG · ask wall < 50th pct | 4 | 1 | −2.27 |
| LONG · no ask wall at all | 2 | 1 | −1.07 |

**n = 1. The mirror case does not exist in the clean data.** Only one clean closed LONG ever entered
through a ≥77th-pct ask wall (vpos 82, ×11.7 = 85.9th pct, **+1.04R, exited on the trail**).

**Widening to all 53 closed positions — which BREAKS §0 filters 3 and 4 (moved stops) and I am
reporting it labelled, not laundered:**

| cohort | n | wins | totR | meanR |
|---|---:|---:|---:|---:|
| LONG · ask wall ≥ 77th pct | 5 | 2 (40%) | **+0.27** | +0.054 |
| LONG · ask wall ≥ 70th pct | 6 | 2 (33%) | **−0.01** | −0.001 |
| LONG · ask wall 50–70th | 4 | 2 (50%) | −0.16 | −0.040 |
| LONG · ask wall < 50th pct | **14** | 4 (29%) | **−6.61** | −0.472 |
| LONG · no ask wall at all | 2 | 1 (50%) | −1.07 | −0.537 |

Every closed LONG with a rendered ask-wall line, worst-to-best by percentile:

```
vpos 69  x25.2 = 99.8 pct  R -0.28 sl        vpos 59  x 5.8 = 46.6 pct  R -1.06 sl
vpos 35  x17.0 = 97.8 pct  R +0.51 external  vpos 72  x 5.8 = 46.6 pct  R -0.99 sl
vpos 65  x13.2 = 90.4 pct  R -0.41 sl        vpos 45  x 5.6 = 42.7 pct  R +0.04 sl
vpos 82  x11.7 = 85.9 pct  R +1.04 trail *   vpos 71  x 5.4 = 38.4 pct  R -0.20 sl
vpos 55  x10.8 = 83.7 pct  R -0.58 sl        vpos 63  x 5.2 = 34.1 pct  R -0.29 sl
vpos 67  x 7.6 = 71.5 pct  R -0.28 sl        vpos 85  x 5.2 = 34.1 pct  R -1.09 sl *
vpos 64  x 6.6 = 59.4 pct  R +0.03 external  vpos 54  x 4.9 = 27.8 pct  R +0.71 external
vpos 70  x 6.4 = 56.2 pct  R -0.31 sl        vpos 41  x 4.8 = 25.5 pct  R -1.13 sl
vpos 79  x 6.2 = 52.8 pct  R +0.50 trail *   vpos 75  x 4.5 = 18.3 pct  R -0.11 external *
vpos 62  x 6.1 = 51.1 pct  R -0.38 sl        vpos 39  x 4.4 = 16.0 pct  R +0.17 trail
                                             vpos 37  x 4.3 = 13.6 pct  R -1.11 sl
                                             vpos 78  x 0.0 =  0.0 pct  R -1.20 sl *
                                             vpos 84  x 0.0 =  0.0 pct  R +0.12 external *
                                                              (* = §0-clean)
```

🔴 **Conclusion, stated against my own expectation: the mirror case shows NO harm, and if anything
the sign is backwards.** LONGs through a ≥70th-pct ask wall are **totR −0.01 across n=6** — exactly
break-even — while LONGs with a **thin** ask wall (<50th pct) are **−6.61R across n=14**. That
inversion is contaminated (moved stops, two sizing eras), and I am not proposing it as a finding.

**What IS solid is the structural asymmetry, and it explains why the mirror is empty:** 289 skips
versus 6 contaminated entries. **The advisor almost never takes a LONG into a notable ask wall.**
§4.4's 289 vetoes and this table are not two arms of an experiment — they are a filter and the handful
of cases that leaked past it. **Nothing here contradicts §4.4, and nothing here supports re-opening it.**

One control worth a line, offered as an oddity and not a claim: closed SHORTs with a ≥70th-pct ask
wall — where that wall is **supporting** the position — are **n=5, −2.87R**, while SHORTs with a
thinner one are **n=23, +8.28R**. Same contamination applies. Direction is entangled with era.

## 13 · Tape P. Sell 0.09 — shown, weighted by NOTHING. §2.21 again, in a second place.

**Stored value (`trades.19713.tape_json`):**

```json
{"total_trades":100, "window_seconds":60, "buy_usdt_window":87246.94,
 "sell_usdt_window":831706.92, "buy_share_window":0.0949, "pressure":"sell",
 "whale_usdt_threshold":50000, "whale_count":3, "span_ms":15168,
 "whales":[{"side":"sell","price":64837.6,"usdt":733715.25},
           {"side":"sell","price":64837.2,"usdt":70737.39},
           {"side":"buy","price":64837.7,"usdt":62827.73}]}
```

**Where it enters the decision: NOWHERE.** Traced to every consumer:

| consumer | what it does | when |
|---|---|---|
| `microstructure.format_telegram_block` | renders `Pressure: Sell (0.09)` on the card | **display** |
| `microstructure._persist` | writes `trades.tape_json` | storage |
| `microstructure.compact_for_llm` → `claude_advisor.py:667` | post-trade W/L attribution prompt | **AFTER the trade** |

**It does not appear in the entry prompt at all** — the verbatim prompt in item 12 is the whole book
section, and there is no tape line anywhere in the 33-line prompt. `microstructure.py`'s own docstring
says it: *"this module never raises into the caller and **never gates a trade**."* And
`capture_and_persist_sync` is called at `main.py:3997` — **after** the entry has executed.

✅ **So: shown, and weighted by nothing. That is the §2.21 shape exactly** — book *depth* was the
first instance, tape pressure is the second. **Two extreme readings in one entry card, neither
carrying weight anywhere:** depth 82nd pct and tape Sell 0.09.

**Is it entangled with the book imbalance?** **Not by construction, but they are not independent
either.** Tape is L3 — realised taker aggression. Imbalance is L2 — resting depth. Different objects.
But both are cut from the same BingX depth-100 / recent-trades snapshot, and `orderbook_json` for the
same instant shows the band **bid**-heavy at 0.6994 while the tape was 91% **sell** — so on this
entry they point opposite ways. Reading either as confirmation of the other would be wrong.

⚠️ **And the tape number itself is weaker than it looks — two caveats:**
1. **`window_seconds: 60` but `span_ms: 15168`.** The label says a 60-second window; the 100 trades
   ccxt returned span **15.2 seconds**. `_analyze_tape` filters `now_ms - ts <= window_ms` over
   whatever `fetch_trades` supplied — it never guarantees the window it names. **The label overstates
   the sample.** Fifth instance of the naming class in this file.
2. **One print is 88% of the sell side.** `733,715 USDT` of `831,707` total sell volume is a single
   trade. `buy_share_window = 0.0949` is not "sustained selling"; it is one 11.3-BTC market sell
   inside 15 seconds. **n=1 dressed as a ratio.**

Outcome data for completeness, n=16, and it is noise: `buy_share < 0.30` → n=9, −0.12R;
0.30–0.70 → n=5, −2.62R; `> 0.70` → n=2, −2.18R.

## 14 · POST-ENTRY RECHECK — the tier ran; the §2.20 fix was NOT exercised

🔴 **Correcting the premise in your question, because it matters.** The T+300s tier is **no longer
due — it FIRED at 12:10:28** and `virtual_positions.87.recheck_status` is now **`done`**. All three
tiers ran:

```
id 37  12:05:30.274  tier  10  health 0  OK  wall 20.4/16.0  ratio 1.2750  adx_1h 25.3505  reasons []
id 38  12:06:24.723  tier  60  health 0  OK  wall 11.9/16.0  ratio 0.7438  adx_1h 25.3541  reasons []
id 39  12:10:28.111  tier 300  health 0  OK  wall 40.1/16.0  ratio 2.5063  adx_1h 25.4048  reasons [wall_growth_critical 2.5063>2.0, points 0]
```

**But this is NOT the §2.20 fix in live use, and I should not let it be read that way.** §2.20 fixed
what happens when a **no-op TIGHTEN** is recorded. vpos 87 never produced a TIGHTEN — all three
verdicts were `OK` — so the branch the fix changed **was never entered**. Tiers stayed due because
nothing consumed them, which was already true before `838481f`. Checking history: 11 of 14 positions
with recheck rows already ran all three tiers; **only vpos 74 and vpos 86 ever stopped at T+10, and
both stopped because of a TIGHTEN.** So:

✅ **The §2.20 fix remains UNEXERCISED in live.** It needs a position that reaches the TIGHTEN branch.

🔴 **And here is the link back to item 9a: the ADX window bug is WHY it was not exercised.** vpos 87's
true ADX1h is 13.5, under the floor of 20; on the entry-path window `adx_below_floor` fires,
`_health_score` returns **−5**, `HEALTH_SCORE_TIGHTEN = -5`, verdict **TIGHTEN** — and *that* would
have been the no-op TIGHTEN that exercises the fix. The 42-bar reading of 25.35 suppressed the rule,
the verdict, and the test.

**The wall metric halving 20.4 → 11.9 in 54 s: MEASUREMENT NOISE, not book movement. Measured, not
guessed.** `cur_wall_mult` is the largest opposing-wall multiple in the **BingX depth-100** book (via
`microstructure.fetch_pre_trade_walls` — same book as the `entry_wall_mult 16.0` reference, so this
metric at least is internally consistent). I sampled it 12 times over 110 seconds on a quiet book
just now:

```
9.40  11.50  14.20  11.60  15.10  15.30  12.50  11.00  9.40  8.90  10.10  9.20
min 8.90   max 15.30   median 11.25   sd 2.21   max/min = 1.72x
```

**The metric swings 1.72× in under two minutes with nothing happening.** Your 20.4 → 11.9 is a
1.71× move — **exactly the idle noise band**. A depth-100 book on BTC spans a very narrow price
range, so a single large resting order arriving or leaving moves the max multiple by half. It is not
reading the market; it is reading order churn.

And the T+300 reading of 40.1 (ratio **2.5063**) **crossed `WALL_GROWTH_CRITICAL = 2.0`** and scored
**+0** — because `WALL_GROWTH_CRITICAL_SCORE = 0` and `WALL_GROWTH_WARNING_SCORE = 0` since
2026-07-13. **Correctly zero**, on this evidence: a rule fed a metric with a 1.7× idle range should
not carry weight. Worth recording that the one named "critical" rule that tripped in live contributed
nothing, deliberately.

## 15 · vpos 86 vs vpos 87, field by field

| | **vpos 86 — SHORT (closed −1.02R)** | **vpos 87 — LONG (open)** |
|---|---|---|
| entry / time | 63686.0 · 00:50:14 | 64838.7 · 12:05:17 |
| stop · 1R | 64767.1 · 1081.1 pts (**1.698%**) | 64028.8 · 809.9 pts (**1.249%**) |
| risk | $2.4866 | **$1.8628** |
| ATR 5m | 81.33 | 65.21 |
| **raw score** | **5.75** | **4.25** |
| display `adj_score` | 7.25 (`+1.5000`, **clip ceiling**) | 3.63 (`−0.6212`) |
| gate compared | 5.75 ≥ 2.0 | 4.25 ≥ 2.0 |
| TREND | 2.25 (1 sig) | **2.50 (2 sigs)** |
| MOMENTUM | **1.75, clean** | **0.00 — intra-conflict L1.75/S2.5** |
| 5M-STRUCTURE | 0.00 — **inter**-conflict | 0.00 — **intra**-conflict L2.5/S1.25 |
| EXECUTION | 1.75 | 1.75 |
| 1H tier | Smart Trail Bearish · w **0.9** · 3.8h | Bullish Confirmation+ · w **1.0** · 2.1h |
| 15m tier | HyperWave Down · counted | HyperWave Up · **NOT counted — matrix TTL expired** |
| 5m tier | Within Bearish OB · 0m | Within Bullish OB · 0m |
| combo weight | **1.00** | **0.90** (historical loser) |
| MTF / regime | 4/4 BEAR · TREND | 4/4 BULL · TREND |
| **ADX1h (200-bar)** | **11.12** | **13.52** |
| ADX 15m / 5m | 12.99 / 25.87 | **38.22 / 40.99** |
| 1d | NEUTRAL, ADX 15.6 | NEUTRAL, ADX 15.6 |
| vol ratio 5m | **4.92× (92nd pct — §2.5's bad band)** | **1.80×** |
| book imbalance (OKX) | 0.51 **bid**-heavy — **71st pct** | 0.42 **ask**-heavy — **5th pct** |
| supporting wall | ×4.8 = 32nd pct, 0.155% away | ×5.1 = 40th pct, 0.145% away |
| opposing wall | ×5.7 = **46th pct** (ordinary) | ×8.4 = **77th pct**, +0.253% (+0.20R) |
| book depth | **2,440 BTC = 6th pct** | **3,276 BTC = 82nd pct** |
| walls bid / ask (BingX-100) | 13 / 3 | 5 / 6 |
| tape | **buy 0.68**, 0 whales | **buy 0.09**, 3 whales (1 = 88% of sells) |
| news | NEG, **medium**, −0.25 → `news +0.5` (aligned) | NEG, **high**, −0.57 → `news −0.5` (opposed) |
| macro gate penalty | 0.0 | 0.0 |
| recheck | **T+10 TIGHTEN (−5), tiers 60/300 EATEN** | T+10/60/300 all **OK**, `done` |
| entry advisor conf | 0.82 | **0.78** |
| exit advisor, 1st | `hold` at −0.01R | `hold` at +0.03R (row 19714) |

### What is actually different, and is any of it better

**Genuinely better on vpos 87 — four things:**
1. **Tighter geometry.** 1R is **1.249%** vs 1.698%, and risk $1.86 vs $2.49. Same $150 notional,
   **25% less at stake per unit of thesis.**
2. **The lower-TF engine is actually turning.** ADX 15m **38.2** and 5m **41.0**, versus vpos 86's
   **13.0 / 25.9**. vpos 86 was a 4/4-aligned short with **no measured momentum on any timeframe**.
3. **Book depth 82nd pct vs 6th.** vpos 86 entered on the thinnest book in 24,000 snapshots — §2.21's
   open question, and its most extreme figure. vpos 87 entered on a deep one.
4. **Volume 1.80× vs 4.92×.** vpos 86 sat at the 92nd percentile, inside §2.5's replicated bad band
   (≥2.42×: 2 wins in 15, −$708.72). vpos 87 sits in the **1.30–1.60 band's neighbourhood** — the
   cohort that was 6 wins in 9, +$241.07. Confounded (§2.5 says so), but it is the right side of it.

**Genuinely worse on vpos 87 — four things:**
1. **Lower score from fewer agreeing parts: 4.25 vs 5.75**, and **two of four categories silenced by
   conflict** rather than one. Its 15m tier was **not counted by the gate at all** (TTL expired) —
   so the score rests on the 1H trend plus a 5m trigger.
2. **Combo weight 0.90** — the optimizer marks this signal triple a historical loser. vpos 86's was
   1.00.
3. **Book imbalance at the 5th percentile, against the direction** — the most extreme figure of the
   entry, and the advisor did not mention it. vpos 86's imbalance (71st pct, bid-heavy) was *against*
   its short too, but far less extreme.
4. **The opposing wall is genuinely thicker: 77th vs 46th pct.** Ordinary versus notable.

**The shared weakness is identical and it is the one you spotted: a strong lower-TF alignment story
resting on a 1h ADX that says nothing is trending** (11.1 and 13.5, both under the retired floor).
Neither trade was blocked by that, correctly — §2.13 retired the threshold for want of evidence and
deliberately did not replace it.

**Straight answer: on balance, marginally better.** The improvement is in the parts that are
*measured* — geometry, momentum, depth, volume — and the deterioration is in the parts that are
*counted* — score, conflict, combo weight, one book percentile. Given that §2.13 retired the ADX
threshold, §2.22 renamed the category whose vote was silenced, and §2.5's volume band is the one
replicated statistic in the file, **I would rather hold vpos 87's hand than vpos 86's.** With n=1 per
side that is a preference, not a prediction.

---

## STATE AT PUBLICATION — verified from runtime, not copied forward

`git status` clean · HEAD **`81875c9`** · origin in sync · `titan.service` **active** since
**11:32:45**, `NRestarts=0` · **0 tracebacks · 0 CRITICAL · 0 `REFUSING TO START`** since the restart
· no `🚨` and no `MANUAL ACTION REQUIRED` line · circuit breaker untripped · Mercury-SOL **untouched**.

`LIVE_TRADING_ENABLED = True` · `ORDER_ADAPTER_LIVE = True` · `EXIT_ADVISOR_DRYRUN = False` ·
sizing `$30 × 5 = $150`. Balance **free 480.10 · used 29.83 · total 509.93**.

**Book: 1 open row (vpos 87) · 1 exchange position · 1 exchange order. They reconcile on both probes.**

**Live realised P&L so far, and it needs the by-hand addition §7's caveat demands:**
`vpos 86 −$2.541574` **+** the 2026-07-29 naked short **−$0.26** (no `virtual_positions` row; but see
item 7b — it *does* have an observatory row, id 80 / `vpos_id 89`) = **−$2.80 realised**, against
vpos 87 open at **+$0.04** unrealised.

## WHAT I DID NOT DO

**Nothing was written, patched, restarted or deleted.** Read-only throughout: exchange probes are
`fetch_*` only; the DB was opened read-only in queries; the ADX, mark/last and wall-noise measurements
run in a scratch process outside the service. **Three items are now waiting on your word:**

1. 🔴 **The ADX window defect (9a).** One indicator, two windows, the difference rendered as a change;
   `ADX_BELOW_FLOOR` missing 52.9% of the states it exists to catch; the exit prompt asserting a rise
   that did not happen. **This is the one I would fix next.**
2. **§2.4's second contamination (7a).** Nine clean-book `close` verdicts on vpos 86 that all beat the
   actual exit — and all nine carried biased ADX. Whether that is a third restart, or a
   `first-clean-verdict` datapoint of **+0.495R**, is a rule decision and it is yours.
3. **The observatory ghost rows (7b).** Two rows describing positions `virtual_positions` does not
   contain, one of them still accumulating shadow data today, and a live position's outcome stamped
   onto a stale entry price.

---

*Titan · 2026-07-30 13:10 UTC · HEAD `81875c9` · 🔴 LIVE · vpos 86 closed by stop −$2.5416 (−1.02R) ·
vpos 87 LONG open · read-only report*
