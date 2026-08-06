# SOL — THREE FINAL CHECKS BEFORE THE KEY: THE DEDUP MEASURED, THE LEDGER AUDITED, AND WHY IT HAS NOT TRADED

**2026-08-06 17:20 UTC · Mercury-SOL · READ-ONLY. NOTHING WAS CHANGED.**

Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched** — clean at `897850b`.

---

## THE THREE ANSWERS

> **1. The dedup is INTACT — measured, not reasoned. 1 model call, 2 reuses**, exactly as at 12:45.
>
> **2. The ledger does NOT silently drop a status** — the `pending` defect has not recurred. But
> **~22 writable statuses sit outside its ladder**, and it **never reads `naked_position_alerts` at
> all**, so every hands-required alert state is invisible to the daily digest.
>
> **3. 🔴 MARKET, not mechanical. The question closes.** SOL has been in a **2.78%-wide box for three
> days, net −0.20%**, and **this book has produced a LONGER zero-run before** — 390 prompts over six
> days in July — which resolved on its own.

---

# 1. THE DEDUP — MEASURED

You were right to ask for a run rather than accept reasoning. Here it is: the 11:25 shape — three
distinct 5m triggers on one market state — through the **current** advisor, with the new wall
percentiles and dual tally in the prompt.

## a) 1 call, 2 reuses

```
Bullish OB Created     reused=False  decide='skip'
Bullish I-CHOCH+       reused=True   decide='skip'  age=0.0s
Within Bullish OB      reused=True   decide='skip'  age=0.001s
🔴 MODEL CALLS: 1   REUSES: 2   ✅
[STATE-CACHE] HIT/cache — reusing the verdict for this market state, no model call.
              this_5m='Bullish I-CHOCH+' decided_on_5m='Bullish OB Created'
```

**Identical to the 2026-08-06 12:45 result.** The new prompt text changed nothing about it.

## b) Provenance survives the longer prompt

```
deciding prompt : 2834 chars · has PERCENTILE: True · has dual tally: True
Bullish I-CHOCH+   own render 2830 chars · has PERCENTILE True · differs from deciding: True
                   names deciding 5m: 'Bullish OB Created'
Within Bullish OB  own render 2832 chars · has PERCENTILE True · differs from deciding: True
                   names deciding 5m: 'Bullish OB Created'
```

Each reused row carries **its own render** — a different length, because its own 5m trigger is named in
it — while `verdict_reused_from.trigger_5m` still names **the prompt that actually produced the
verdict**. That is the 2026-08-01 provenance rule holding under text that is now longer and contains
percentiles: *"`user_prompt` keeps naming the prompt that ACTUALLY produced this verdict; THIS row's
rendering rides alongside it, never over it."*

## c) The key: PRICE busts, MULTIPLE does not

```
×11.7 → ×11.8  (same wall, re-measured)  reused=True   calls stay 1   ✅ multiple NOT in key
$73.75 → $73.90 (wall MOVED)             reused=False  calls → 2      ✅ price IS in key
   and the busting call rendered:  Ask walls (>4x avg vol): $73.90 (p70, x11.7), $74.25 (p20, x4.8)
```

**This is the check that mattered most**, because the multiple is now rendered as a *secondary* figure
beside a percentile — a plausible place for it to have leaked into the key. It did not. The key is
`(symbol, direction, 1H identity, 15m identity, nearest-opposing-wall PRICE)`, and the last line above
shows the percentile rendering riding on a busted key without being part of it.

*Isolated tree, 13-file rewrite, residual 0, leak assert `production-book opens: 0`, isolated `.env`.*

> 🔶 **One honest note on the harness, because it nearly produced a false alarm.** My first run reported
> `1 call → 3 calls, 0 reuses`. The cause was mine, not the bot's: I returned `{'decision': …}` where
> the contract is `{'decide': …}`, so every verdict parsed as `unavailable` — and **`'unavailable'` is
> never cached, by design.** The bot was refusing to pin an API failure for 60 s, which is correct.
> Fixed the harness, not the code. Recorded because "the dedup broke" would have been the wrong
> conclusion from a real-looking number.

---

# 2. THE SILENCE LEDGER

## a) What it recognises vs what the bot can write

The digest's ladder covers **19** statuses (6 bookkeeping, 6 gates, 3 advisor, 4 exit) plus `executed`.
The tree can write **~41**. The difference:

**🔴 Money-path statuses outside the ladder** — these are the ones that matter:
`naked_position_unprotected` · `sl_failed_position_closed` · `sl_failed_no_position` · `failed` ·
`closed_unrecorded_pnl`

**Gate-like statuses outside the ladder** (they *are* entry refusals, so the funnel understates):
`wall_blocked` · `spread_blocked` · `fee_gate_rejected` · `filter_blocked` · `bypass_flat_skipped` ·
`ai_hold` · `neutral1h_armed` · `neutral1h_unconfirmed` · `shadow_armed_pending_close` · `pending` ·
`stalled` · `tightened` · `sweep_recorded`

**✅ F1's seven close labels are NOT affected.** They are `signal_type` values, not statuses; their rows
carry `status='executed'` and land in `close_exec` (`executed` AND not `open_%`). The ledger counts
them correctly.

**🔴 And the gap I did not expect:** `grep -c naked_position_alerts silence_digest_sol.py` → **0**.
The digest **never reads that table**. So all five hands-required stages — `boot_orphan`,
`entry_fill_unreadable`, `partial_fill_unreadable`, `sl_failsafe_close_failed`, and today's
`exchange_close_unsubstantiated` — are **invisible to the daily silence digest.** The digest reports
why the bot was quiet; it cannot report that the bot was quiet *because a side is blocked*.

## b) The recurrence check — **the `pending` defect has NOT recurred**

```python
other = {s: c for s, c in by_status.items() if s not in known}
...
A('<b>⚠️ UNCLASSIFIED STATUSES</b> (not in the ledger\'s ladder — shown so nothing is silently dropped)')
```

An unrecognised status **lands in the UNCLASSIFIED bucket and is printed**. It does **not** vanish from
the render. That is the fix from the `pending` incident, and it still holds.

**But it is excluded from the funnel arithmetic** (`attempts = gate_n + adv_n`). So a gate-like status
is *visible* yet *uncounted* — the totals understate refusals rather than lose them. **Visible-but-
uncounted is a weaker failure than silently-dropped, and it is the one that remains.**

## c) Run now, 168 h window

```
🔇 MERCURY-SOL — SILENCE LEDGER          window: last 168h → 2026-08-06 17:14 UTC
mode: PAPER (OBSERVATION_MODE=1) · open positions: 0

  webhooks logged   2156 rows → 1269 market events (×1.70)
  ├─ bookkeeping     280
  └─ entry attempts 1834 rows → 1169 events
       ├─ 1H trend not set        126
       ├─ HTF cascade vetoed      761
       ├─ score below threshold   396
       ├─ risk gate halted         26
       └─ reached the advisor     525
             ├─ ADVISOR DECLINED          521  (99% of those)
             ├─ approved, not sent (paper)  1
             └─ EXECUTED                    3
  advisor declines: 521 rows → 409 events (×1.27; book-wide norm ×1.26)

WHAT THE ADVISOR CITED (of 521 declines)
  opposing order-book wall  469 (90%) · weak ADX 415 (80%) · FLAT/ranging 399 (77%) · tier disagreement 383 (74%)

VERDICT: not silent — 3 entry(ies) executed.
```

**No UNCLASSIFIED block appeared** — in the last 168 h the bot wrote no status outside the ladder. The
gap above is a *capability* gap, not an active one. **Not fixed in this pass, as instructed.**

---

# 3. 🔴 WHY HAS SOL NOT TRADED SINCE 2026-08-03?

## a) The funnel per day — nothing upstream stopped

| date | rows | book | no_trend | HTF veto | below thr | risk | reached advisor | declined | **entries** |
|---|---|---|---|---|---|---|---|---|---|
| 07-29 | 84 | 5 | 0 | 41 | 9 | 0 | 26 | 26 | **1** |
| 07-30 | 355 | 49 | 25 | 135 | 64 | 36 | 39 | 39 | 0 |
| 07-31 | 348 | 42 | 7 | 178 | 29 | 0 | 86 | 86 | 0 |
| 08-01 | 340 | 33 | 53 | 61 | 138 | 0 | 49 | 49 | **1** |
| 08-02 | 295 | 51 | 3 | 115 | 24 | 2 | 92 | 92 | **1** |
| 08-03 | 227 | 41 | 0 | 117 | 14 | 0 | 45 | 44 | **1** |
| 08-04 | 281 | 36 | 4 | 68 | 69 | 0 | 97 | 97 | 0 |
| 08-05 | 306 | 37 | 0 | 116 | 73 | 0 | 76 | 76 | 0 |
| 08-06 | 237 | 29 | 34 | 68 | 25 | 0 | 77 | 77 | 0 |

**Signals arrive at the same rate (227–355/day, no collapse). The advisor is consulted MORE than
before, not less — 45 on 08-03, then 97 / 76 / 77.** Nothing upstream stopped. The entries stop at the
advisor's verdict and nowhere else.

## b) The advisor since 08-03

| era | prompts | executes | rate |
|---|---|---|---|
| before 08-04 | 2264 | 44 | **1.94%** |
| **since 08-04** | **250** | **0** | **0.00%** |

The shape you measured — many prompts, no executes — still holds, and the cited reasons have not
shifted: opposing wall 90%, weak ADX 80%, FLAT/ranging 77%.

## c) 🔴 MARKET or MECHANICAL — decided on the tape, not the bot's labels

**SOL/USDT daily, read live from Bybit:**

| | days | band | net move | avg daily range |
|---|---|---|---|---|
| **before 08-04** (bot traded) | 13 | 70.53 – 78.85 = **11.80% wide** | **−5.84%** | **3.40%** |
| **since 08-04** (0 entries) | 3 | 72.79 – 74.81 = **2.78% wide** | **−0.20%** | **2.09%** |

```
2026-08-04   73.53  74.44  73.01  73.72   range 1.96%  chg +0.26%
2026-08-05   73.72  74.81  73.20  73.99   range 2.20%  chg +0.37%
2026-08-06   73.99  74.32  72.79  73.38   range 2.10%  chg −0.82%
```

**The tape shows a textbook compression, established independently of the bot:** the three-day band is
**2.78%** against **11.80%** before, the net move over three days is **−0.20%** — flat to two decimal
places — and daily range fell **39%**. A trend-following bot with a FLAT-regime guard and an ADX floor
is *supposed* to be silent in this tape. The bot's own cited reasons (FLAT/ranging, weak ADX) agree
with the tape, but the tape did not need them.

**And the statistical objection, answered rather than avoided.** 0 executes in 250 prompts against a
1.94% base rate has probability ≈ 0.98^250 ≈ **0.75%** — unlikely enough to be worth checking. So I
checked whether this book has done it before:

```
2026-07-22 → 07-27:   390 prompts, 0 executes, SIX days
2026-07-30 → 07-31:   125 prompts, 0 executes
2026-08-04 → 08-06:   250 prompts, 0 executes  ← the current run
```

> 🔴 **The current drought is SHORTER than the July one — 250 prompts against 390, three days against
> six — and that one ended on its own with a normal resumption.** The current silence is not
> unprecedented; it is within this book's demonstrated behaviour.

**And my own changes are not implicated.** The drought began **08-04**; the prompt changes shipped
**08-06 16:05**. Of today's 77 prompts, **73 ran on the old prompt and 4 on the new — both 0 executes.**
Four prompts cannot explain a three-day drought that predates them.

## d) VERDICT

> ### **MARKET. The question closes.**
>
> The pipeline is fully alive — signals, gates, advisor, all at or above their normal rates. SOL has
> been in a 2.78% box for three days with a net move of −0.20%, and this book has previously gone six
> days and 390 prompts without an execute in a comparable regime. **Nothing mechanical stopped.**

**What this means for the flip, stated plainly and not softened:** the key will not produce a live
trade on day one merely because it is turned. At a 1.94% execute rate and ~80 prompts/day, the expected
wait for the first live entry is **on the order of a day or two of normal market**, and longer if the
range persists. **That is not a reason to delay the flip** — the bot is correctly quiet, and the flip
costs nothing while it is quiet — **but the operator should not read silence after the flip as a
failed flip.** The boot line and the funnel are how to tell them apart:

* the boot line says `OBSERVATION_MODE=False` → the flip took;
* the daily digest shows entry attempts reaching the advisor → the pipeline is alive;
* zero entries with both of those true → the market, not the bot.

---

```
READ-ONLY — no file written to the SOL tree, no service restarted, no order placed.
Public market data only (load_markets / fetch_ohlcv, keyless client).
SOL   worker 2756553 · flat 0/0/0 · OBSERVATION_MODE=True (still paper)
TITAN git clean · HEAD 897850b · NOT TOUCHED
```

*Generated 2026-08-06 17:20 UTC.*
