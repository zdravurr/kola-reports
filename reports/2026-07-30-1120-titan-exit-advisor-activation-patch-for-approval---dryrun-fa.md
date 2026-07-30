# TITAN exit-advisor activation PATCH FOR APPROVAL - DRYRUN=False would have SILENCED it

_2026-07-30 11:20 UTC_

---

### and the reason it could not be the one-line flip you asked for

**2026-07-30 11:15 UTC · HEAD `957f980` · position vpos 86 STILL OPEN and 0.155R from its stop**

---

## DECISION LINE

**You asked for `EXIT_ADVISOR_DRYRUN = False` and "nothing else changes". That exact change would
have made the advisor MUTE, not active.**

Both live consult sites gate on the flag being **True**:

```
virtual_trader.py:2149   if EXIT_ADVISOR_HOURLY and EXIT_ADVISOR_DRYRUN:          # 8 of 9 verdicts
main.py:3444             if EXIT_ADVISOR_ON_15M_CONFIRM and EXIT_ADVISOR_DRYRUN:  # 1 of 9 verdicts
```

Flipping it to `False` **deletes both consults**. No prompt, no verdict, no row, no close. The one
site where the flag means what its name says — `main.py:2787` — sits in `_handle_5m_close_via_ai`,
reachable only by a 5m Group-B webhook. **Zero such webhooks have arrived in this bot's entire
history** (0 rows in `trades`, all time; 77 exit consults recorded, none from that trigger).

So the one-line flip forfeits the observation **and** buys no action. Strictly worse than DRYRUN.

**Your argument for acting is untouched by this and I accept it in full.** The held branch is
recoverable from candles — this project has done it three times (13,536 / 101,739 / 18,900 bars) —
so DRYRUN's real cost is forgone action, not lost knowledge. Nine `close` verdicts on vpos 86 since
the 02:51 fix, the best exit available at **−0.254R**, the position now at **−0.845R**. That is the
wrong trade at $150 notional and the flag is why. **The disagreement is about the mechanism, not
the decision.**

**NOTHING HAS BEEN APPLIED. The service has not been restarted. The live tree is clean at `957f980`.**

---

## PART 0 — VERIFICATION, READ-ONLY. ALL GREEN.

| check | result |
|---|---|
| `git status` | **clean** |
| HEAD | **`957f980`** · origin in sync (`main...origin/main`) |
| runtime **= commit by hash** | **8/8 MATCH** — `main` `config` `virtual_trader` `order_adapter` `claude_advisor` `breakeven_worker` `close_report` `microstructure`; **no `.py` newer than proc start** (PID 116494, started 02:51:11) |
| `titan.service` | **active**, `NRestarts=0`, up since 02:51:11 |
| journal since restart | **0 errors · 0 tracebacks · 0 CRITICAL · 0 `REFUSING TO START`** |
| circuit breaker | **never tripped** (the 2 journal hits are TradingView *"Bearish Breaker"* price-action alerts, not the breaker) |
| Mercury-SOL | **untouched, active** |

**Four boot gates, verbatim from the live journal:**
```
[ORDER-MODE]   🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
[RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 1 exchange position(s), 1 open row(s)
[RECONCILE]     SHORT open, SL present @ 64767.1 — kept.
```

**The live position — BOTH probes, run at 11:10 UTC:**

```
unified fetch_positions : side=short contracts=0.0023 entry=63686.0 uPnL=-2.1022
                          posId=2082629807737368578 mark=64600.0
raw swapV2 UserPositions: {"positionId":"2082629807737368578","positionSide":"SHORT",
                          "positionAmt":"0.0023","avgPrice":"63686.0",
                          "unrealizedProfit":"-2.1022","markPrice":"64600.0","leverage":"5"}
open orders             : id=2082629881359347712 STOP_MARKET BUY posSide=SHORT qty=0.0023
                          stopPrice=64767.1 closePosition=true workingType=MARK_PRICE status=NEW
balance                 : USDT free 481.30 · used 29.30 · total 510.60
```

**They agree exactly.** One position, one order, no orphans. **The stop order id is still the one
placed at entry** — unchanged across the 02:51 restart and every hour since.

**vpos 86 row vs exchange — reconciles field for field:**

| | DB row | exchange |
|---|---|---|
| side / size | SHORT 0.0023 | SHORT 0.0023 |
| entry | 63686.0 | avgPrice 63686.0 |
| stop | `sl_price` = `original_sl_price` = 64767.1 · `stop_order_id` 2082629881359347712 | stopPrice 64767.1, order 2082629881359347712 |
| status | `open` | 1 position |

**Position state at 11:10:** 1R = 1081.1 pts · mark 64600.0 → **−0.845R** · **167.1 pts (0.155R)
from the stop** · uPnL **−$2.10**. `water_mark` 63578.5 → **MFE never exceeded +0.099R**;
`max_adverse_price` 64613.7 → **MAE −0.858R**. **Trail NOT armed** (arms at +1R = 62604.9);
`breakeven_applied=false`; `partial_taken` NULL; `recheck_status='tightened'` (terminal by design,
§2.20).

**Nothing is off. Part 0 does not stop the work.** What stops it is a defect in Part 1 itself.

---

## 🔴 THE FINDING — §2.23, and it is the FOURTH "the label does not say what it does" in four days

`EXIT_ADVISOR_DRYRUN` is **two switches wearing one name**, and the second is wired backwards:

1. **"do not act on the verdict"** — the name. True at exactly one site, `main.py:2787`.
2. **"do consult"** — unnamed, undocumented, and it is the one that governs both working triggers.

**The codebase already knew and said so eight lines above the flag** (`config.py:232`):

> *"its trigger is a 5m Group-B alert and **zero have ever arrived** — the operator has decided NOT
> to create a 5m exit alert, so this stays true."*

That sentence was written to explain why the advisor was never **consulted**. Nobody re-read it as a
statement about where the advisor could **act**. It is both.

**A second defect on the same dead path:** in LIVE mode `_handle_5m_close_via_ai` locates the
position through `_fetch_open_position` (the exchange), so `_vpos` is `None` and it calls
`claude_advisor.consult_for_close(...)` — **the old, unenriched consult, no book block at all** —
not `consult_exit_advisor`. The only close-capable path would have judged on a poorer prompt than
the 77 verdicts §2.4 is built from.

**The class.** §2.19 percentile on another book's scale · §2.20 a no-op TIGHTEN recorded as terminal
· §2.22 three card labels · **§2.23 a flag whose name describes one of its two effects.** The
`957f980` lesson was *"check not only what the gate DECIDES but what it SAYS."* This one is the
inverse and worse: **the flag says the right thing and silently does a second, unnamed thing.**

---

## PART 1 — THE CHANGE, AND WHAT IT ACTUALLY HAD TO BE

**Four edits across three files, 280 diff lines. `git apply --check` passes against the live tree;
all three files compile; the symtable FUNCTION-scope audit (the 29.07 guard) parses clean.**

1. **`config.py`** — `EXIT_ADVISOR_DRYRUN = False`, and the comment rewritten to state that the flag
   now gates **acting only**.
2. **`virtual_trader.py:2149`** — gate reads `EXIT_ADVISOR_HOURLY` alone. On a `close` verdict with
   DRYRUN off it calls the new `_advisor_close(...)` and **returns immediately**, so nothing
   downstream (recheck tiers, breakeven, trail, LONG partial) operates on a closed row.
3. **`main.py:3444`** — gate reads `EXIT_ADVISOR_ON_15M_CONFIRM` alone, same act path.
4. **`virtual_trader._advisor_close(...)`** — new, and the **only** code in this bot that closes on
   an advisor's say-so.

Plus two supporting changes: `'ai_exit'` added to the batch-counter reason tuple (so advisor exits
are not invisible to the optimizer cohort, same reasoning that admits `post_entry_critical`), and the
`[EXIT-ADVISOR-DRYRUN]` log prefix becomes `[EXIT-ADVISOR-LIVE]` when it can act — **the journal must
not print DRYRUN next to a real close.**

---

## PART 1.2 — WHAT HAPPENS ON A `close` VERDICT, STEP BY STEP

**Trigger: hourly (8 of 9 verdicts came this way).** Poller tick, ~10s cadence.

```
virtual_trader._process_position(exchange, row, last, send_tg)
│
├─ 0. _reconcile_passive_fill(...)          ← ALWAYS FIRST. If our exchange stop already
│                                              filled, the row is finalised from the REAL
│                                              filled order and we return before anything below.
├─ 1. water_mark / MAE / excursion / smart-exit sampler   (observational)
│
├─ 2. if EXIT_ADVISOR_HOURLY:                            ← no longer reads DRYRUN
│      └─ if ≥3600s since exit_advisor_last_ts:
│         ├─ a. main.consult_exit_advisor(row, ...)      → builds the 48-field prompt,
│         │                                                calls Claude, INSERTS the verdict row
│         │                                                (status='exit_ai_dryrun'), logs
│         │                                                [EXIT-ADVISOR-LIVE], returns `advice`
│         ├─ b. mgmt_state['exit_advisor_last_ts'] = now  🔴 STAMPED BEFORE THE CLOSE,
│         │    UPDATE virtual_positions ...                  UNCONDITIONALLY — this is what makes
│         │                                                  "one attempt per verdict" TRUE
│         └─ c. if not DRYRUN and _advisor_says_close(advice):
│                └─ _advisor_close(...) ──────────────┐
│                   and `return True` on success       │
└─ 3..N recheck tiers / breakeven / trail / partial ← NEVER REACHED after a close
                                                       │
_advisor_close(exchange, row, advice, last, send_tg, trigger)
│  logs [EXIT-ADVISOR-ACT] … CLOSING at market
└─ virtual_trader._do_close(exchange, row, last, reason='ai_exit', send_tg)
   │
   ├─ order_adapter.market_close(exchange, symbol, 'SHORT', 0.0023, last)
   │  └─ orders_are_real() → True   ⇒  _require_live('send a close order')
   │     └─ main._execute_close_position(symbol, 'SHORT', _from_adapter=True)
   │        │                          ^^^^^^^^^^^^^^^^^^ mandatory: without it this
   │        │                          re-enters the engine and recurses unbounded
   │        ├─ _fetch_open_position → None ⇒ return None (see FAILURE MODES)
   │        ├─ 🔴 fetch_ticker → create_market_order(BUY 0.0023, positionSide='SHORT')
   │        │     ▸ NO reduceOnly — BingX rejects it in hedge mode (109400, proven 29.07)
   │        │     ▸ THE STOP IS STILL LIVE ON THE EXCHANGE AT THIS MOMENT
   │        ├─ fill_price = order['average']  ← REAL fill
   │        ├─ fee_cost   = fetch_order_fee(order['id'])  ← REAL fee, read back from BingX
   │        ├─ ✅ ONLY NOW: cancel STOP_MARKET / TP / TRAILING / LIMIT for this side
   │        └─ _cancel_stop_orders(...)   ← second-pass orphan sweep
   │     └─ fee is None ⇒ ESTIMATED at SIM_FEE_RATE and SAID SO in the log
   │
   ├─ funding_paid = close_report.funding_for_close(...)   (estimated, tagged as such)
   ├─ report = close_report.build_close_report(... reason='ai_exit' ...)
   │            net = gross − entry_fee − exit_fee − funding   (fees never pre-summed)
   ├─ UPDATE virtual_positions SET status='closed', close_price=?, close_reason='ai_exit',
   │         net_pnl=?, total_fees=?, gross_pnl=?, funding_paid=?, closed_at=?
   │   WHERE id=? AND status='open'          ← idempotent by construction
   ├─ UPDATE trades SET pnl=? WHERE id=<entry row> AND pnl IS NULL
   ├─ _batch_fn(...)          ← 'ai_exit' now counted, like post_entry_critical
   ├─ send_tg(report.telegram())            ← the 🧪 close report
   └─ post_exit_observatory.on_real_close(row, close_price, 'ai_exit', report)
```

**Answering your four questions directly:**

| question | answer |
|---|---|
| **which function executes** | `virtual_trader._advisor_close` → `_do_close` → `order_adapter.market_close` → `main._execute_close_position(_from_adapter=True)` |
| **cancel the stop first or after** | 🔴 **AFTER — but only because this patch changes it.** Today it cancels FIRST. See G. 2. |
| **real fill price and real fee from BingX** | **Yes both.** `fill_price` = `order['average']`; `fee_cost` = `fetch_order_fee(order_id)` read back from the venue. If the fee is not reported it is estimated at `SIM_FEE_RATE` **and the log says `close fee not reported — ESTIMATED`** — it is never passed off as real. |
| **which path handles it** | **Active close.** Passive-fill reconciliation is the *other* branch and runs FIRST every tick — if the exchange stop already fired, `_reconcile_passive_fill` finalises the row from the real filled order (`reason='sl'` or `'breakeven'`) and the advisor never gets to act. |

**FAILURE MODES, each stated with what it leaves behind:**

| failure | result |
|---|---|
| `create_market_order` raises | **Stop still on the exchange, position still protected**, row still `open`. Loud log + Telegram. **Not retried this tick or any tick for the next hour.** |
| position already gone (stop fired concurrently) | `_execute_close_position` returns `None` → `market_close` logs `🔴 close requested but NO live position found` → `_do_close` returns `None` → row left `open` → **next tick's `_reconcile_passive_fill` finalises it from the real fill.** |
| Claude unavailable / malformed verdict | `_advisor_says_close` returns `False`. **An absent answer is never read as an instruction to trade.** |
| Telegram down | wrapped; never blocks or reverses a close. |

---

## PART 1.3 — YOUR FOUR GUARDS, ANSWERED. I DISAGREE WITH NOTHING; ONE COULD NOT BE MET WITHOUT A FIFTH EDIT.

**Guard 1 — CLOSE only. Never open, reverse, resize. ✅ Met by construction.**
`_advisor_close` has one mechanic: `_do_close` on an already-open row. There is no entry call, no
side flip, and **no size argument anywhere on the path** — `_do_close` closes the whole size recorded
in `filled_legs`. It cannot reverse because it never chooses a side, and cannot resize because it
never passes a quantity.

**Guard 2 — the STOP stays the backstop until the close CONFIRMS; never cancel-then-fail.
🔴 VIOLATED BY THE EXISTING CODE. This is the fifth edit, and it is why I am not treating your
"nothing else changes" as satisfiable.**

`_execute_close_position` today does, in order: **cancel every STOP_MARKET / TP / TRAILING / LIMIT
for the side → fetch ticker → send the market close.** If `create_market_order` raises — rate limit,
a 109400-class rejection, a network blip — **the stop is already gone and a real position is left
naked.** That is precisely the state this bot ate on 2026-07-29, and it is **latent on every close
path** — `sl`, `trail`, armed exit, emergency close — not just the advisor's.

The patch moves the cancel loop to **after** the fill comes back. A failed close then changes
nothing: position open, stop live.

🔴 **The residual, stated rather than buried:** the stop can trigger during the ~1s close window. It
carries `closePosition=true`, so the venue applies it to the whole remaining size and has nothing to
open with once that is zero. **That rejection is EXPECTED but UNPROVEN** — §7 uncertainty 1, the
stop has never fired. I accept it because the alternative failure is a naked live position, which is
strictly worse and has actually happened here. **If you would rather not take an unproven behaviour
on a live position, the honest alternative is to hold this edit until the stop has fired once** —
but then Guard 2 is not met and the advisor should not be armed either.

**Guard 3 — one close attempt per verdict, no retry loop. ✅ Met, and mechanically not by promise.**
`exit_advisor_last_ts` is stamped **before** `_advisor_close` is called, and unconditionally. A
failed close therefore sees a fresh timestamp on this tick and every tick for the next 3600s. **A
retry can only come from a NEW verdict, on fresh numbers.** On the 15m path each signal is its own
verdict and `_advisor_close` contains no loop.

**Guard 4 — advisor exits stamped distinctly in `reason`. ✅ Met.**
`close_reason='ai_exit'`, new and unused. Current distribution: `sl` 30 · `trail` 18 · `external` 10
· `post_entry_critical` 1. **Separable in every future cut with a plain `WHERE close_reason='ai_exit'`.**

**Label debt I am recording rather than hiding:** the *verdict row* status stays `exit_ai_dryrun`
even when acting. Renaming it forks the 77-row audit trail §2.4 is cut from. Acted-on verdicts are
identified by `close_reason='ai_exit'` on the position; the status column is the verdict channel, not
a claim about acting. **Flagging it because "a label that no longer says what it means" is exactly
the class in §2.23 — I am choosing continuity over purity here, and you should overrule me if you
disagree.**

---

## PART 2 — THE CRITERION IS REPLACED, NOT ABANDONED. ALREADY WRITTEN INTO §2.4.

**Written to `reports/OPEN-ITEMS.md` §2.4 at 11:10 UTC — before the advisor has hands, and therefore
before any position can possibly close under it. It cannot be moved afterwards.** The old wording is
kept verbatim alongside as the record of what it replaced.

> **THE CRITERION IN FORCE** (from the commit that sets `EXIT_ADVISOR_DRYRUN = False`)
>
> For every position the advisor CLOSES, replay from **real 5m candles** what the unchanged contract
> would have done had the position been held — **stop, breakeven, trail, LONG partial, and any
> intrabar ambiguity resolved ADVERSELY** — and record **advisor-close vs held-branch** in USDT.
> It stays live only if, over the first **~10 advisor-closed positions**, the advisor beats the held
> branch **both in total USDT and in positions improved**.
> **No partial credit. No re-cutting the sample. Every advisor close counts** — not its best ones.

**Same bar, same ~10, same no-re-cutting rule. Only the counterfactual branch swaps sides.**

**Two things the mirror cannot recover, recorded now so they are not discovered later as a surprise:**
funding on the held branch is estimated, not ledgered; and a held branch that a *future advisor
verdict* would have closed is not modelled — the replay holds to the mechanical contract only.
**Both biases run toward the held branch, i.e. against the advisor.** That is the safe direction and
it is deliberate.

---

## PART 3 — vpos 86's NINE CLEAN VERDICTS. ALL SAY `close`.

Every consult since the `957f980` fix at 02:51:11. **Nine of nine `close`, every one at confidence
0.72.** Position R computed from `position_excursion_samples` — **not** from the advisor's own text
(they agree to within ~0.05R wherever they overlap).

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

**Recorded now, before the trade resolves, so the datapoint exists whichever way it goes.**

### The book block is now provably on the right scale — `625fedc` proven on live data

Every one of the nine carries the header
`source: OKX books-full depth-4000 (the percentile baseline)`, and the readings are internally
consistent. **The phantom "93rd-percentile wall" that talked the advisor into HOLDING at 00:50 does
not recur in any of the nine.**

Verbatim book block, row 19678 (10:51:14):
```
Order book NOW vs AT ENTRY — source: OKX books-full depth-4000 (the percentile baseline)
  Supporting wall: entry x5.7 -> now x7.4 (grew)
  Opposing wall:   now x4.5
  Imbalance:       entry 0.51 -> now 0.38 (FLIPPED)

Order-book PERCENTILE scale (baseline: 24537 snapshots of this SAME book)
  Supporting wall = 70th pct
  Opposing wall = 23th pct
  Total depth = 3155 BTC = 70th pct (sampled 32s ago)
  Imbalance = 0th pct
```
Compare row 19607 (03:50): `Supporting 75th · Opposing 82nd · Depth 17th · Imbalance 17th` —
**the opposing wall decays 82nd → 75th → 48th → 38th → 23rd across the nine as price runs up into
the stop.** That is a coherent trajectory on one scale, which is exactly what was impossible before.

### Their thesis, unchanged across seven hours

Verbatim, row 19678:

> *"Entry thesis deteriorated. At entry: 4/4 lower-TF alignment (4h/1h/15m/5m all BEAR). Now:
> 15m=BULL, 5m=neutral. Regime flipped bullish on lower timeframes. ADX15m surged to 32.1 (strong
> directional move—upward). Imbalance collapsed from 0.51→0.38 (entry edge gone, now at 0th
> percentile—weakest reading). Supporting wall grew +7.4x but opposing wall intact at 4.5x.
> Position -0.80R with only +0.20R t…"*

Row 19649 (08:51): *"Regime has flipped decisively to bull (15m/5m both bullish, ADX rising). Order
book imbalance inverted from entry (0.51→0.36, now 0th percentile vs ordinary baseline)…
The 4/4 lower-TF bearish alignment at entry no longer exists."*

Row 19628 (06:50), **the cheapest exit it offered, −0.254R**: *"Entry thesis compromised… now
15m=neutral, 5m=neutral, ADX collapsed to 11.0 (no directional conviction)… supporting wall grew to
85th pct (strong bid support, unusual st…"*

**Note this cuts both ways and I am not going to shade it:** these nine are one position, one
direction, one thesis, restated hourly. **They are nine samples of a single opinion, not nine
independent judgements.** Under either §2.4 wording vpos 86 contributes **one** datapoint. What they
do establish is that the corrected book block produces a coherent, stable, non-contradictory read —
which is what `625fedc` was for.

---

## THE THING I WOULD PUT IN FRONT OF YOU

**The advisor has been right about this trade for seven hours and could not have acted for a reason
that has nothing to do with the flag you asked me to flip.** Even with `DRYRUN=False` applied on
2026-07-30 at 03:00, vpos 86 would have run to its stop untouched — because `hourly` and
`15m_exit_confirm` have no close mechanic, and the path that does has never once been triggered.

**DRYRUN was not the only thing standing between the verdict and the position. It was the one we
knew about.**

---

## WHAT IS APPLIED AND WHAT IS NOT

| | |
|---|---|
| Live tree | **UNCHANGED**, clean at `957f980` |
| Service | **NOT restarted**, up since 02:51:11 |
| `EXIT_ADVISOR_DRYRUN` | **still `True`** |
| Patch | **prepared, compiles, `git apply --check` passes — NOT applied** |
| `OPEN-ITEMS.md` | **updated**: §2.4 criterion replaced · §2.4a nine clean verdicts · **§2.23 new** · §7 re-verified at 11:10 |
| vpos 86 | **open, −0.845R, 0.155R from its stop** |

**Awaiting your approval on two things, not one:**
1. arming the advisor (the four edits), and
2. **the fifth edit — close-first/cancel-after in the shared close path**, which changes `sl`,
   `trail`, armed-exit and emergency closes too, and which trades a proven failure mode for an
   unproven one.

---

## THE FULL PATCH — `957f980` + these 280 lines

```diff
--- a/config.py	2026-07-29 21:53:46.205777145 +0000
+++ b/config.py	2026-07-30 11:07:22.045573129 +0000
@@ -235,10 +235,22 @@
 # empty in paper. PAPER_ENABLED fixes (b); ON_15M_CONFIRM supplies a trigger that
 # actually fires (~2.2/day); HOURLY adds a full trajectory per position, reusing
 # the smart-exit sampler which already collects the 48 fields the prompt needs.
-# DRYRUN short-circuits before every close mechanic: the advisor cannot close
-# anything regardless of verdict. SL / trail / armed-exit remain sole authority.
+# 🔴 DRYRUN NOW GATES **ACTING ONLY** — and that is itself the change (2026-07-30).
+# It used to gate CONSULTING as well, on the only two triggers that ever fire:
+#     virtual_trader.py  `if EXIT_ADVISOR_HOURLY and EXIT_ADVISOR_DRYRUN:`
+#     main.py            `if EXIT_ADVISOR_ON_15M_CONFIRM and EXIT_ADVISOR_DRYRUN:`
+# Setting this False on its own would therefore have SILENCED the advisor — no
+# consult, no verdict, no close — while arming the ONE close-capable path (5m
+# Group B) on a trigger that has never arrived in this bot's history (0 rows,
+# and the comment 8 lines above already said so). Those two gates now read their
+# own flags, which is what they were always named for.
+#
+# With DRYRUN=False a `close` verdict CLOSES: at market, through the adapter,
+# stamped reason='ai_exit'. It may only CLOSE — never open, never reverse, never
+# resize. The exchange STOP_MARKET stays the backstop and is cancelled only
+# AFTER the close confirms. ONE attempt per verdict; no retry loop.
 EXIT_ADVISOR_PAPER_ENABLED  = True   # paper mode: find the position in virtual_positions
-EXIT_ADVISOR_DRYRUN         = True   # record the verdict; the exit proceeds EXACTLY as today
+EXIT_ADVISOR_DRYRUN         = False  # 🔴 ACTING — a `close` verdict closes the position
 EXIT_ADVISOR_ON_15M_CONFIRM = True   # also consult on the 15m exit-confirm / 1H-arm triggers
 EXIT_ADVISOR_HOURLY         = True   # consult once per hour per open position (sampler cadence)
 EXIT_ADVISOR_HOURLY_SEC     = 3600   # cadence; mirrors SMART_EXIT_DRYRUN_SAMPLE_SEC
--- a/virtual_trader.py	2026-07-30 02:49:33.323605537 +0000
+++ b/virtual_trader.py	2026-07-30 11:07:22.052573212 +0000
@@ -1220,7 +1220,11 @@
     # intentionally unused: report.batch_line above is the richer block and is
     # set for ALL reasons. post_entry_critical IS a real outcome the optimizer
     # must see to learn poor entries, so it counts toward the cohort here.
-    if _batch_fn is not None and reason in ('sl', 'trail', 'post_entry_critical'):
+    # 'ai_exit' counts for the same reason post_entry_critical does: it is a REAL
+    # outcome on a REAL position, and an optimizer cohort that silently omitted
+    # every advisor exit would be scoring a strategy that no longer exists.
+    if _batch_fn is not None and reason in ('sl', 'trail', 'post_entry_critical',
+                                            'ai_exit'):
         try:
             _batch_fn(row_id=entry_row_id)
         except Exception as _bf_err:
@@ -2061,6 +2065,70 @@
               f"— DRYRUN, position untouched", flush=True)
 
 
+def _advisor_says_close(advice):
+    """True ONLY for an explicit close verdict. A missing, failed or
+    'unavailable' consult is NOT a close — an absent answer must never be read
+    as an instruction to trade."""
+    return (bool(advice) and bool(advice.get('close'))
+            and advice.get('decide') != 'unavailable')
+
+
+def _advisor_close(exchange, row, advice, last, send_tg, trigger):
+    """THE EXIT ADVISOR'S ONLY HANDS. Close the whole open position, once.
+
+    CLOSE ONLY. There is no entry call, no side flip and no size argument
+    anywhere below: _do_close closes the WHOLE size recorded on the row. This
+    function cannot open, reverse or resize a position, by construction rather
+    than by promise.
+
+    THE STOP IS NOT TOUCHED HERE. The exchange STOP_MARKET remains the backstop
+    for the entire attempt — it is cancelled inside _execute_close_position only
+    AFTER the market close has returned a fill. If anything below raises, the
+    stop is still live on the exchange and the position is still protected.
+
+    ONE ATTEMPT PER VERDICT. The caller stamps exit_advisor_last_ts BEFORE
+    calling this, so a failure is never retried by the next 10s poll tick. The
+    next attempt can only come from the next VERDICT, on fresh numbers.
+    """
+    _reason = (advice.get('reason') or '')[:200]
+    _conf = float(advice.get('confidence') or 0.0)
+    print(f"[EXIT-ADVISOR-ACT] vpos={row['id']} {row['symbol']} "
+          f"{row['position_side']} trigger={trigger} conf={_conf:.2f} — CLOSING "
+          f"at market | {_reason}", flush=True)
+    try:
+        res = _do_close(exchange, row, last, 'ai_exit', send_tg)
+    except Exception as e:
+        # The close FAILED. The stop was never cancelled, so the position is
+        # still protected by it. Shout, and do NOT retry.
+        print(f"[EXIT-ADVISOR-ACT] 🔴 close FAILED vpos={row['id']}: {e} — "
+              f"position left OPEN, exchange stop still in place, NOT retried",
+              flush=True)
+        if send_tg:
+            try:
+                send_tg(f"🔴 <b>EXIT-ADVISOR CLOSE FAILED</b>\n"
+                        f"{row['symbol']} {row['position_side']} · vpos "
+                        f"{row['id']}\n<code>{e}</code>\n"
+                        f"Position left OPEN and the exchange stop is STILL the "
+                        f"backstop. Not retried — the next verdict decides.")
+            except Exception:
+                pass
+        return False
+    if res is None:
+        # market_close found no live position (already flat / stop just filled).
+        # The row is left for _reconcile_passive_fill. Not an error, not retried.
+        print(f"[EXIT-ADVISOR-ACT] vpos={row['id']}: no live position to close "
+              f"— left for passive-fill reconciliation, NOT retried", flush=True)
+        return False
+    if send_tg:
+        try:
+            send_tg(f"🤖 <b>EXIT ADVISOR CLOSED</b> ({_conf:.2f}) · {trigger}\n"
+                    f"{row['symbol']} {row['position_side']} · vpos {row['id']}\n"
+                    f"<i>{_reason}</i>")
+        except Exception:
+            pass
+    return True
+
+
 def _process_position(exchange, row, last, send_tg):
     """One position, one tick. Returns T. iff state changed (so caller can
     short-circuit logging). Single-entry model, mirroring the live
@@ -2143,23 +2211,39 @@
     # 1e) EXIT-ADVISOR hourly consultation (2026-07-26), DRYRUN only. Reuses the
     #     smart-exit sampler cadence — that sampler already collects the 48 fields
     #     the enriched prompt needs. Signal triggers alone give ~2.2 consultations
-    #     a day; hourly gives a full trajectory per position. Records a verdict and
-    #     NOTHING ELSE: this block has no close mechanic and cannot move a stop.
+    #     a day; hourly gives a full trajectory per position.
     #     main is imported lazily to avoid the circular import at module load.
-    if EXIT_ADVISOR_HOURLY and EXIT_ADVISOR_DRYRUN:
+    #
+    #     🔴 THE GATE NO LONGER READS DRYRUN (2026-07-30). It used to, so
+    #     EXIT_ADVISOR_DRYRUN=False silenced the consult instead of arming it —
+    #     this block produced 8 of the 9 clean `close` verdicts on vpos 86 and
+    #     would have stopped producing any. DRYRUN is now read ONLY below, where
+    #     it decides whether the verdict is ACTED ON.
+    if EXIT_ADVISOR_HOURLY:
         try:
             _st = mgmt_state.get('exit_advisor_last_ts')
             _now_ts = datetime.now(timezone.utc).timestamp()
             if _st is None or (_now_ts - float(_st)) >= EXIT_ADVISOR_HOURLY_SEC:
                 import main as _m
-                _m.consult_exit_advisor(row, row['symbol'], position_side,
-                                        'hourly review', 'hourly')
+                _adv = _m.consult_exit_advisor(row, row['symbol'], position_side,
+                                               'hourly review', 'hourly')
+                # THE TIMESTAMP IS STAMPED BEFORE THE CLOSE IS ATTEMPTED, and
+                # unconditionally. That is what makes 'one attempt per verdict'
+                # true: if the close below fails, this poll tick and every tick
+                # for the next hour see a fresh exit_advisor_last_ts and do not
+                # re-enter. A retry can only come from a NEW verdict.
                 mgmt_state['exit_advisor_last_ts'] = _now_ts
                 with sqlite3.connect(DB_PATH) as _c:
                     _c.execute("UPDATE virtual_positions SET pending_dca_limits=? "
                                "WHERE id=? AND status='open'",
                                (json.dumps(mgmt_state), row['id']))
                 changed = True
+                if not EXIT_ADVISOR_DRYRUN and _advisor_says_close(_adv):
+                    if _advisor_close(exchange, row, _adv, last, send_tg, 'hourly'):
+                        # The row is CLOSED. Everything below this point — the
+                        # recheck tiers, breakeven, the trail, the LONG partial —
+                        # would be operating on a position that no longer exists.
+                        return True
         except Exception as _e:
             print(f"[EXIT-ADVISOR] hourly consult failed vpos={row['id']}: {_e}", flush=True)
 
--- a/main.py	2026-07-30 02:49:33.322605526 +0000
+++ b/main.py	2026-07-30 11:09:50.345352133 +0000
@@ -1218,10 +1218,38 @@
     close_amount = float(pos['contracts'])
     close_side = 'sell' if position_side == 'LONG' else 'buy'
 
-    # Cancel any pending triggers (SL / trail / TP) and unfilled DCA limits
-    # for this side. BingX does not auto-cancel TRAILING_STOP_MARKET when
-    # the position closes via opposing market order — leaving them creates
-    # an orphan against a flat position. (Memory: project_bingx_bot.md)
+    # 🔴 CLOSE FIRST, CANCEL AFTER (2026-07-30). The cancel loop below used to run
+    # BEFORE this market order. That ordering is cancel-then-fail: if
+    # create_market_order raises — rate limit, a 109400-class rejection, a network
+    # blip — the protective STOP_MARKET is ALREADY GONE and a REAL position is
+    # left naked. That is the exact state this bot ate on 2026-07-29, and it sat
+    # latent on EVERY close path (sl, trail, armed exit, emergency), not just this
+    # one. The close is now sent while the stop is still on the exchange, so a
+    # failed close changes nothing: the position stays open and stays protected.
+    #
+    # RESIDUAL, STATED RATHER THAN HIDDEN: the stop can trigger during the close
+    # window. It carries closePosition=true, so the venue applies it to the whole
+    # remaining size and has nothing to open with once that is zero. That
+    # rejection is EXPECTED but still UNPROVEN (§7 uncertainty 1 — the stop has
+    # never fired). It is accepted because the alternative failure mode is a naked
+    # live position, which is strictly worse and has actually happened here.
+    ticker = exchange.fetch_ticker(symbol)
+    current_price = float(ticker['last'])
+
+    order = exchange.create_market_order(
+        symbol, close_side, close_amount,
+        params={'positionSide': position_side},
+    )
+    fill_price = float((order or {}).get('average')
+                       or (order or {}).get('price') or current_price)
+    fee_cost = (fetch_order_fee((order or {}).get('id'), symbol)
+                if (order or {}).get('id') else None)
+
+    # The position is now flat. Cancel this side's pending triggers (SL / trail /
+    # TP) and unfilled DCA limits. BingX does not auto-cancel
+    # TRAILING_STOP_MARKET when the position closes via an opposing market
+    # order — leaving them creates an orphan against a flat position.
+    # (Memory: project_bingx_bot.md)
     try:
         for o in exchange.fetch_open_orders(symbol):
             info = o.get('info') or {}
@@ -1238,18 +1266,6 @@
     except Exception as e:
         print(f"order cleanup failed: {e}")
 
-    ticker = exchange.fetch_ticker(symbol)
-    current_price = float(ticker['last'])
-
-    order = exchange.create_market_order(
-        symbol, close_side, close_amount,
-        params={'positionSide': position_side},
-    )
-    fill_price = float((order or {}).get('average')
-                       or (order or {}).get('price') or current_price)
-    fee_cost = (fetch_order_fee((order or {}).get('id'), symbol)
-                if (order or {}).get('id') else None)
-
     # Post-close second-pass: wipe any stop/trigger orders that survived the
     # pre-close cancel loop (race conditions, BingX propagation delay, etc.).
     _cancel_stop_orders(symbol, position_side)
@@ -2673,8 +2689,10 @@
     entry side does (system prompt, user prompt, reason, confidence).
 
     This function has no access to any close mechanic and can never close a
-    position. Whether an exit happens is decided by the callers, and while
-    EXIT_ADVISOR_DRYRUN is True every caller returns before its close path."""
+    position. Whether an exit happens is decided by the callers: while
+    EXIT_ADVISOR_DRYRUN is True none of them acts on the verdict, and when it is
+    False they hand the verdict to virtual_trader._advisor_close, which is the
+    ONLY code in this bot that closes on an advisor's say-so."""
     ctx = _build_exit_context(dict(vpos_row), symbol, side, exit_signal_name, trigger)
     advice = claude_advisor.consult_for_close_rich(ctx)
     try:
@@ -2687,7 +2705,12 @@
                                          'close' if advice.get('close') else 'hold'))
     except Exception as e:
         print(f"[EXIT-ADVISOR] persist failed: {e}", flush=True)
-    print(f"[EXIT-ADVISOR-DRYRUN] trigger={trigger} {symbol} {side} "
+    # 🔴 THE LABEL MUST NOT LIE (2026-07-30). This line said DRYRUN unconditionally.
+    # Once the advisor can act, a log line claiming DRYRUN next to a verdict that
+    # is about to close a real position is the third instance of this bot's
+    # "the label does not say what it means" class. It now reports which it is.
+    print(f"[EXIT-ADVISOR-{'DRYRUN' if EXIT_ADVISOR_DRYRUN else 'LIVE'}] "
+          f"trigger={trigger} {symbol} {side} "
           f"close={advice.get('close')} conf={advice.get('confidence')} "
           f"| {(advice.get('reason') or '')[:200]}", flush=True)
     return advice
@@ -3441,13 +3464,26 @@
                 # operator's dedicated exit alert set and fires ~2.2x/day with a
                 # position open. Consulted here in DRYRUN only — the noop below is
                 # unchanged and remains the sole outcome.
-                if EXIT_ADVISOR_ON_15M_CONFIRM and EXIT_ADVISOR_DRYRUN:
+                # 🔴 THE GATE NO LONGER READS DRYRUN (2026-07-30) — same defect as
+                # the hourly gate: DRYRUN=False silenced the consult instead of
+                # arming it. DRYRUN is now read only where the verdict is ACTED on.
+                if EXIT_ADVISOR_ON_15M_CONFIRM:
                     for _s in ('LONG', 'SHORT'):
                         _vp = virtual_trader._open_position(symbol, _s)
                         if _vp:
                             try:
-                                consult_exit_advisor(_vp, symbol, _s, signal_name,
-                                                     '15m_exit_confirm')
+                                _adv = consult_exit_advisor(_vp, symbol, _s,
+                                                            signal_name,
+                                                            '15m_exit_confirm')
+                                if (not EXIT_ADVISOR_DRYRUN
+                                        and virtual_trader._advisor_says_close(_adv)):
+                                    # One attempt per verdict: each 15m signal is
+                                    # its own verdict, and _advisor_close never
+                                    # loops. A failure waits for the next signal.
+                                    _last = float(exchange.fetch_ticker(symbol)['last'])
+                                    virtual_trader._advisor_close(
+                                        exchange, _vp, _adv, _last, send_tg,
+                                        '15m_exit_confirm')
                             except Exception as _e:
                                 print(f"[EXIT-ADVISOR] 15m consult failed: {_e}", flush=True)
                 insert_signal(parsed, symbol, 'na', '15m_exit_confirm',
```

---

*Titan · 2026-07-30 11:15 UTC · HEAD `957f980` · nothing applied · vpos 86 live*
