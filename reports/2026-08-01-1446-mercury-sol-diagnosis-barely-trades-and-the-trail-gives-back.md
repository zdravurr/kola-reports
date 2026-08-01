# mercury-sol-diagnosis-barely-trades-and-the-trail-gives-back-1r

_2026-08-01 14:46 UTC_

---

# MERCURY-SOL — READ-ONLY DIAGNOSIS, 2026-08-01

**Scope:** SOL/USDT swing bot only. Titan was not touched, not read for comparison, and
nothing here is imported from it. Nothing was changed, proposed or fixed.

**Where it lives:** `/mnt/volume_nyc1_1780480650620/mercury-sol` (NOT `/root/mercury-bot` —
that is the retired ETH Mercury, last written 2026-06-03). Services: `mercury-sol.service`
(gunicorn, `main:app`), `mercury-sol-optimizer.timer` (14:00 UTC daily),
`mercury-sol-optimizer-listener.service`.

**Mode:** paper. `MERCURY_OBSERVATION_MODE=1` in `.env`. No order has ever been sent to Bybit
by this bot. Bybit is reached read-only through Tor; the OKX book is fetched direct, keyless.

---

# §0 — CONTAMINATION FILTERS, DERIVED FOR SOL

I used only the *method* from the Titan open-items §0 (state the eras, mechanism changes and
measurement defects that make a naive whole-book query misleading, **before** quoting any
aggregate; prefer an exact structural split over timestamp arithmetic). Titan's specific dates
and its `stop_order_id IS NOT NULL` split do **not** apply here — SOL has never been live, so
that column does not exist and there is no paper/live boundary to cut on.

## 0.1 Eras

There is no git history for this bot (`fatal: not a git repository`). The only change record is
file mtimes plus ~90 `.bak_*` snapshots. Everything below is dated from those plus the
behavioural break visible in the data.

| # | boundary | what changed | visible in the data? |
|---|---|---|---|
| E-0 | 2026-06-03 → 06-07 | commissioning; 56 signal rows, no gate stack | n/a |
| E-1 | **2026-06-08** | the A/D/P-series parity rewrite. ~60 `.bak` files carry this single date. ATR basis moved 5m → 1h, SL/trail/arm constants all re-set, three vetoes deleted outright, the score threshold moved to 2.0 | yes — the gate stack only starts producing rows here |
| E-2 | 2026-06-24 | state_machine stacking-race fix | no |
| E-3 | **2026-06-29** | Lever A-2 (`HTF_NEUTRAL_REQUIRE_15M_DRYRUN` False→True) **and** Lever B (re-arm the 1h trend from a directional 15m confirm after a 60-min cooldown) | **yes, large** — see 0.1a |
| E-4 | 2026-06-30 → 07-02 | NEUTRAL-1h long relax, excursion logging, skip-attr HTF capture. `main.py` and `virtual_trader.py` last written **2026-07-02 21:36/21:37** | partly |
| E-5 | **2026-07-04 22:09–22:11** | the wall relaxations went LIVE: `ADVISOR_WALL_ALIGNED_V2` (LONG, gate widened same day) and `ADVISOR_WALL_ALIGNED_SHORT_V2` (new). `config.py` 22:09, `claude_advisor.py` 22:11 | yes — first entry after a 12.6-day drought lands 2026-07-08 |
| E-6 | 2026-07-04 22:11 → today | **no live code file has been modified in 28 days.** `.env` was touched 07-05 23:13 (full-report keys only) | — |

**0.1a — the 07-05 cut the operator named is real, but it is the *second* of two boundaries,
and the smaller one.** The mechanism change landed 2026-07-04 22:11; 07-05 is a safe cut for
it. But the funnel had already been opened a week earlier on **06-29** by Lever B, and that is
the larger break:

```
                        06-08 → 07-05      07-05 → now
  no_trend (1h blind)     43.2/day           15.1/day     ← Lever B, 06-29
  htf_blocked share       65.7%              47.9%        ← Lever A-2 + B, 06-29
  below_threshold share   17.0%              38.5%
  advisor kill rate       97.5%              97.8%        ← unchanged
```

Any before/after on 07-05 alone attributes Lever B's effect to the wall relax. Both are stated
separately below.

## 0.2 Measurement defects — these must be known before reading any aggregate

1. **`trades.confluence_score` is three different quantities depending on which gate wrote the
   row.** `htf_blocked` stores the HTF-*penalised* score; `below_threshold` / `risk_halt` /
   `observed_skipped` / `executed` store `adj_score` (raw + `weighted_adj`); `ai_skipped` /
   `claude_unavailable` / `wall_blocked` store the raw `direction_score`. A `GROUP BY status`
   over this column compares three different numbers. Everything I quote as a score below is
   labelled with which one it is.

2. **`trades.signal_type` mis-labels exits.** Every poller close is written
   `sl_triggered_<side>` regardless of whether it was the stop, the trail or the timeout.
   3 of the 9 `sl_triggered_*` rows are in fact trail exits. **The exit taxonomy exists only in
   `virtual_positions.close_reason`.** All exit counts below come from there.

3. **`virtual_positions.trades_close_row_id` is never written.** It is declared in the schema
   and it is *read* by the batch-summary join (`main.py:1228`,
   `ON (t.id=vp.trades_entry_row_id OR t.id=vp.trades_close_row_id)`), but no code path
   assigns it. All 18 rows are NULL. Entry↔close pairing by that key silently returns entries
   only.

4. **`trades.ai_system_prompt` always stores the V1 base prompt.** `claude_advisor.py` sets
   `result['system_prompt'] = _ENTRY_SYSTEM` unconditionally at the end of
   `consult_for_entry`, *after* a V2/aligned prompt may have overwritten the verdict. Any
   replay of a relaxed decision from the DB replays the wrong prompt.

5. **vpos 1–6 do not exist.** `virtual_positions` starts at id 7. The 2026-06-16 backup DB
   already starts at 7, so the deletion predates it. Three of the six survive in
   `post_exit_observatory`: vpos 1 (LONG, `post_entry_critical`, −0.72), vpos 4 (LONG, `sl`,
   −48.30), vpos 5 (LONG, never closed). vpos 2, 3, 6 are gone everywhere.
   **⇒ "since inception" in this report means since vpos 7, 2026-06-14 23:50 UTC — not since
   the bot started trading on 2026-06-08.**

6. **Excursion path data exists only from vpos 15 onward** (`EXCURSION_LOGGING_ENABLED` added
   07-01). The MFE/MAE *scalars* (`water_mark`, `max_adverse_price`) exist for all 18; the
   *timeline* does not. Same for `smart_exit_dryrun_samples` (vpos 15+).

7. **`skip_attribution` coverage differs by gate.** `ai_skipped` from 06-08, `below_threshold`
   from 06-09, but `htf_blocked` only from **06-22**. A drift-by-gate comparison over the full
   book under-samples the cascade by two weeks.

8. **The journal only reaches back to 2026-07-30 20:55** (~2 days). Every "has it ever fired"
   claim sourced from logs is a 2-day window and is marked as such; DB-sourced claims are
   full-history.

9. **Sizing has been constant** — all 18 rows are `margin_usdt` 2000 × `leverage` 5 =
   **$10,000 notional**. On that axis the book *is* poolable. There is no paper/live split to
   cut: `OBSERVATION_MODE` has been 1 throughout and no row carries an exchange order id.

---

# §1 — IS IT TRADING, AND WHAT IS THE BOOK

## 1a — Rate

**18 entries and 18 closes in the entire history.** Nothing is open.

| week | entries | closes |
|---|---|---|
| W23 (from 06-14) | 1 | — |
| W24 | 2 | 3 |
| W25 | 5 | 5 |
| W26 (06-29→07-05) | **0** | 0 |
| W27 | 2 | 2 |
| W28 | 5 | 4 |
| W29 | 1 | 2 |
| W30 (07-27→) | 2 | 2 |

Rate: **0.25 entries/day before 07-05, 0.36/day after** (+44%). Rising — but from almost
nothing to almost nothing. Two long droughts and a third in progress:

```
  06-25 14:00 → 07-08 05:05   12.63 days, 0 entries
  07-21 03:10 → 07-28 11:05    7.33 days, 0 entries
  07-29 20:05 → now            2.77 days, 0 entries  (flat 50.5h since the last close)
```

Time in market: **12.37 position-days over 45.5 calendar days = 27.2% exposure**, one side at
a time.

The 12.6-day drought is not a signal drought. In 2026-06-26 → 07-07 the bot processed 1,154
`htf_blocked` + 608 `ai_skipped` + 305 `below_threshold`. **The advisor returned zero
`execute` verdicts for thirteen consecutive days.**

## 1b — The closed book

Source: `virtual_positions`, all 18 rows, close reasons from `close_reason` (see §0.2 #2).

| | n | net USD | win rate | PF | avg win | avg loss | median R | mean R |
|---|---|---|---|---|---|---|---|---|
| **ALL** | 18 | **−1,010.24** | 7/18 = 39% | **0.559** | +182.99 | −208.29 | **−0.658** | −0.263 |
| LONG | 8 | −573.96 | 2/8 = 25% | 0.479 | +263.93 | −183.64 | −0.894 | −0.370 |
| SHORT | 10 | −436.28 | 5/10 = 50% | 0.633 | +150.61 | −237.87 | −0.286 | −0.177 |

Fees: 197.83 total (≈11.0 per round trip on $10,000 notional = 0.11%). Fees are 19.6% of the
gross loss but are not the story.

Break-even at this win/loss geometry needs a **~49.4%** hit rate; it is running 39%.

## 1c — The equity path

```
  2026-06-15  vpos  7 LONG  exit_signal   +494.20   cum   +494.20   ← the whole peak, trade #1
  2026-06-20  vpos  8 LONG  exit_signal   -177.34   cum   +316.86
  2026-06-21  vpos  9 LONG  exit_signal    -58.71   cum   +258.15
  2026-06-22  vpos 10 SHORT sl            -245.21   cum    +12.94
  2026-06-23  vpos 11 SHORT exit_signal   +301.16   cum   +314.09
  2026-06-24  vpos 12 LONG  sl            -233.61   cum    +80.49
  2026-06-24  vpos 13 SHORT trail         +327.21   cum   +407.70
  2026-06-25  vpos 14 SHORT sl            -405.97   cum     +1.73   ← end of era, dead flat
  ---------------------------- 12.6-day drought ----------------------------
  2026-07-09  vpos 15 SHORT trail          +34.83   cum    +36.55
  2026-07-10  vpos 16 LONG  sl            -194.70   cum   -158.15
  2026-07-14  vpos 17 SHORT sl (at BE)      +0.86   cum   -157.29
  2026-07-16  vpos 18 LONG  sl            -234.04   cum   -391.33
  2026-07-16  vpos 19 SHORT exit_signal    +89.00   cum   -302.33
  2026-07-17  vpos 20 SHORT sl            -210.88   cum   -513.21
  2026-07-20  vpos 21 LONG  trail          +33.66   cum   -479.55
  2026-07-23  vpos 22 LONG  sl            -203.42   cum   -682.97
  2026-07-28  vpos 23 SHORT exit_signal    -93.24   cum   -776.21
  2026-07-30  vpos 24 SHORT sl            -234.03   cum  -1010.24
```

**The damage is not concentrated — it is a metronome.** Eight of the eleven losers sit in a
−194…−246 band, i.e. a full −1R each. The largest single loss (−406, vpos 14) is large only
because its ATR was large; in R terms it is −1.03, indistinguishable from the rest.

Split by era:

| | n | net | win | PF | mean R |
|---|---|---|---|---|---|
| pre-07-05 | 8 | **+1.73** | 3/8 | 1.002 | +0.051 |
| post-07-05 | 10 | **−1,011.97** | 4/10 | **0.135** | −0.514 |

The pre-07-05 book was an exact wash (+1.73 on 8 trades). Every dollar of the drawdown was
made after the funnel was reopened. The win *rate* barely moved (38% → 40%); what collapsed is
the **size of the wins**: avg win fell +374.19 → **+39.59** while avg loss barely moved
(−224.17 → −195.05). Post-07-05 the bot still catches its winners — it just no longer keeps
any of them. See §4 for the mechanism.

## 1d — Currently open

**Nothing.** `virtual_positions` where status='open' → 0. `active_positions` → 0.
`exit_pending` → 0. Last close 2026-07-30 12:03:30 UTC; **flat for 50.5 hours**. No unrealised
PnL, no stop to be distant from.

---

# §2 — THE FUNNEL

## 2a — What arrives

TradingView posts plain-text alerts to `POST /webhook/sol?tf=<1h|15m|5m>`. Steady
~240–350 events/day, no dead days since 2026-06-08.

| tf | rows | role |
|---|---|---|
| 5m | 13,046 | execution / trigger tier |
| 15m | 1,547 | momentum confirm tier |
| 1h | 293 | trend tier + Exit Signal |

Top types — 5m: Within Bearish OB 3,315 · Within Bullish OB 2,993 · OB Entered 1,525 ·
Liquidity Grab 731 · OB Created 663 · Imbalance 1,258 · Breaker 564 · I-BOS 286 · I-CHOCH 203 ·
**Equal H. 107 / Equal L. 104**.
15m: HyperWave Up 407 / Down 398 · Reversal 176 · HyperWave OB/OS 160 · Divergence 72.
1h: **Exit Signal 47** · Trend Catcher 63 · Confirmation family 120 · Smart Trail 24 ·
Neo C. 6.

## 2b — Where they die, in execution order

Whole book from 2026-06-08, 5m directional signals only:

```
  5m rows                                    13,012   (238/day)
  context/unparsed/suppressed                   669
  no_trend  — 1h slot not set                 1,771   (32/day)
  ──> reached the gate stack                 10,556   (193/day)

     1. htf_blocked        5,811   kills 55.0%  of the 10,556 alive
     2. filter_blocked         0   (see §5c — filters.json does not exist)
     3. below_threshold    1,514   kills 31.9%  of the  4,745 alive
     4. risk_halt            289   kills  8.9%  of the  3,231 alive
     5. fee_gate_rejected      0   (gate disabled)
     6. wall_blocked           0   (gate disabled)
     7. ai_skipped         2,873   kills 97.7%  of the  2,942 alive
        claude_unavailable     1
     ──> passed EVERY gate      68   (1.25/day)
        paper per-side cap     50
        ENTERED                18   (0.33/day)
```

*(The spread gate sits between 1 and 3 and is disabled; the code order is
HTF → spread → filters → score → risk → fee → wall → advisor → execute.)*

**The single gate that closes the funnel hardest is the Claude entry advisor: it refuses
97.7% of everything that reaches it** — 2,873 of 2,942. The HTF cascade blocks far more in
absolute count (5,811) but lets 45% through. The advisor is `claude-haiku-4-5-20251001`,
`AI_ADVISOR_DRYRUN=False`, i.e. a live veto with no kill-switch (the `AI_ADVISOR_ENABLED` flag
was deliberately removed 06-08).

Its refusals are extremely stereotyped. Every advisor skip in the journal window cites the same
three things — FLAT regime, 1h ADX ≈ 20–23, and a "massive wall". Verbatim samples:

> `SKIP LONG conf=0.92 'BEAR regime (1d/4h) opposes LONG; flat market (ADX 1h 21.1, ATR% 0.454%); massive ask wall $73.25×15.6 blocks upside.'`
> `SKIP SHORT conf=0.92 'FLAT market (1h ADX 21.6, ATR% 0.516%, EMA contracting) + massive bid walls ($72.75 ×23.5) directly below SHORT entry absorb downside move.'`

Two of the skips I read state `"opposes LONG"` on a **SHORT** signal (02:50:33 and 02:55:15 on
08-01). That is model text, not a code path, but it means at least some verdicts are being
produced with the direction confused.

## 2c — What happens to the survivors

68 signals passed every gate. **50 of them (73.5%) were refused by the paper engine itself** —
`virtual_trader.execute_entry` returns None when `MAX_POSITIONS_PER_SIDE=1` is already met on
that side, and the webhook records it as `observed_skipped`. Confirmed exactly:
`ai_decision='execute'` → 18 `executed` + 50 `observed_skipped`, no other outcome.

This is not noise, because **the advisor's "yes" arrives in bursts**: 9 execute verdicts on
06-23, 9 on 06-24, 8 on 07-13, 8 on 07-14, 6 on 07-16 — of which exactly one each became a
position. The bot converts a cluster of agreement into a single trade, then spends hours or
days in that one trade while further agreement is discarded.

## 2d — Before / after 2026-07-05

| measure | 06-08 → 07-05 (31.4 d) | 07-05 → now (27.6 d) | |
|---|---|---|---|
| 5m rows | 189.9/day | 256.7/day | +35% |
| `no_trend` | 43.2/day | 15.1/day | **−65%** |
| reached gate stack | 135.2/day | 228.8/day | +69% |
| htf_blocked (share of alive) | 65.7% | **47.9%** | opened |
| below_threshold (share) | 17.0% | 38.5% | tightened (more weak signal arriving) |
| risk_halt (share) | 8.0% | 9.5% | — |
| **ai_skipped (share)** | **97.5%** | **97.8%** | **unchanged** |
| passed all gates | 0.89/day | 1.45/day | +63% |
| paper cap refusals | 20 | 30 | |
| **entries** | **0.25/day** | **0.36/day** | **+44%** |

**The shape changed upstream and did not change at the advisor.** Reopening the cascade
delivered 63% more fully-qualified candidates to the advisor's door; the advisor refused them
at precisely the same rate, and the paper cap ate three quarters of what got past it. The net
effect on entries was +0.11/day.

---

# §3 — HOW IT ENTERS

## 3a — One real entry, end to end: vpos 24 (the most recent), 2026-07-29 20:05 UTC

`trades` row **13973** → `virtual_positions` **24**.

**Signals that formed it** (combo key
`1H:Any Bearish Confirmation | 15M:HyperWave Signal Down | 5M:Bearish S-CHOCH`):

- 1h tier — "Any Bearish Confirmation" set `1h_context = SHORT` (persistent slot, no expiry).
- 15m tier — "HyperWave Signal Down" set `15m_confirm = SHORT`; HyperWave subtype
  `HW_SIGNAL_SHORT`, learnable weight 1.1.
- 5m trigger — "Bearish S-CHOCH" arrived, set `5m_trigger = SHORT`, and is the signal that ran
  the gate stack.

**Matrix score** (`signal_matrix.compute_score`, raw `direction_score = 5.00`):

| category | long pts | short pts | contribution | note |
|---|---|---|---|---|
| TREND | 0.0 | 2.5 | **+2.5** | 2 signals, no conflict |
| MOMENTUM | 0.0 | 2.5 | **+2.5** | 2 signals, no conflict |
| LIQUIDITY | 2.5 | 0.0 | 0.0 | *inter*-conflict → zeroed |
| EXECUTION | 1.75 | 2.0 | 0.0 | *intra*-conflict → zeroed |

**Every check it passed, in order:**

1. `_handle_plain_text` — group A, direction SHORT, `is_trend_set()` true (1h slot held SHORT),
   so no `no_trend` drop.
2. **HTF cascade gate** — 1h SHORT ✅ / 15m SHORT ✅ / 5m SHORT ✅, full alignment, no opposite
   tier. Pass with no NEUTRAL tolerance needed.
3. **Spread gate** — `SPREAD_GATE_ENABLED=False`, skipped entirely.
4. **Optimizer filter enforcement** — `optimizer/filters.json` absent → empty filter set → no
   match possible.
5. **Score gate** — `MACRO_GATE_DRYRUN=False`, so the compared value is
   `direction_score + macro_gate_adj = 5.00 + 0.00 = 5.00` vs `CONFLUENCE_SCORE_THRESHOLD=2.0`.
   Pass, and by a wide margin.
6. **Risk gate** — no macro-event window; DXY halt is observe-only; daily-loss breaker clear;
   per-side exchange count 0; loss streak under 3. Pass.
7. **Fee gate** — `FEE_GATE_ENABLED=False`, skipped.
8. **OKX wall avoidance** — `WALL_AVOIDANCE_ENABLED=False`, skipped.
9. **Claude entry advisor** — `execute`, confidence **0.82**, model
   `claude-haiku-4-5-20251001`:
   > *"Multi-TF bear alignment (4H/1H/5m), expanding EMA-gap, combo=1.0, strong 5m momentum
   > (ADX 30.9). Bid walls are support path; volume ratio 2.72x supports breakthrough."*

   Context it saw: trend 1d/4h/1h/15m/5m all **bear**; `srv_adx_1h` 21.52, `srv_adx_15m` 19.68,
   `srv_adx_5m` 30.93; `srv_atr_1h` 0.660; EMA 1h Bearish, gap **Expanding**, slope Strong;
   `mtf_alignment_score` 4/4; funding +7.36e-05; OI Δ −1.42%; DXY NEUTRAL; macro category
   NEUTRAL (confidence 0.85, penalty 0.00); news overall POS; combo weight 1.0; OKX pre-trade
   book mid 72.66, imbalance 0.538, **zero walls detected on either side** (nothing exceeded
   4× mean bucket volume). Tape buy-ratio 0.849, aggression "bullish" — against the trade,
   and not gated on.

   Note the wall relaxations were **not** involved: they only ever act on a V1 `skip`.
10. **Paper engine** — no open SHORT, so the per-side cap passed. Filled at the live ticker.

**Result:** SHORT 137.6 SOL @ 72.67, $2,000 margin × 5 = $10,000 notional. ATR(14, 1h) 0.6489.
Initial SL 74.29 = entry + 2.5×ATR (1R = $222.91). Trail callback 2.229% = 2.5×ATR. Breakeven
arm at entry − 1R = 71.05. Entry fee 5.4997.

**Outcome:** price never traded below 72.26 (best excursion 0.41 of a 1.62 stop distance =
0.25R). Breakeven never armed. Stop hit at 74.29 on 2026-07-30 12:03 after 15.97h.
Net **−234.03** (−1.05R). Recheck ran all three tiers and recorded `done` — no tighten, no
critical close.

## 3b — The constants that govern entry

Last-changed is from file mtime; there is no git, so day granularity is the best available.

| constant | value | in file since |
|---|---|---|
| `CONFLUENCE_SCORE_THRESHOLD` | **2.0** | 2026-06-08 (from 4.6) |
| `HTF_CASCADE_ENABLED` | True | 06-08 |
| `HTF_TOLERATE_NEUTRAL` | True | 06-08 |
| `HTF_NEUTRAL_REQUIRE_15M_AGREE` | True | 06-08 |
| `HTF_NEUTRAL_REQUIRE_15M_DRYRUN` | **True** (= relaxed) | **06-29** (Lever A-2) |
| `HTF_REARM_FROM_15M_ENABLED` | True | **06-29** (Lever B) |
| `HTF_REARM_COOLDOWN_MINUTES` | 60 | 06-29 |
| `HTF_REARM_DRYRUN` | False (= live) | 06-29 |
| `NEUTRAL_1H_LONG_FOLLOWTHROUGH_ENABLE` | True | 07-01 |
| `NEUTRAL_1H_LONG_FOLLOWTHROUGH_MIN` | 15 min | 07-01 |
| `AI_ADVISOR_DRYRUN` | **False** (live veto) | 06-08 |
| `AI_ADVISOR_FALLBACK_SCORE_THRESHOLD` | 7.5 | 06-08 |
| `ADX_FLAT_FLOOR` | 20.0 | 06-08 |
| `ADVISOR_WALL_ALIGNED_V2` | **True** (LIVE) | 07-02, gate widened **07-04** |
| `ADVISOR_WALL_ALIGNED_SHORT_V2` | **True** (LIVE) | **07-04** |
| `ADVISOR_WALL_RULE_V2` | False (shadow only) | 06-30 |
| `MACRO_GATE_DRYRUN` | **False** (penalty applied at the gate) | 06-08 |
| `MAX_POSITIONS_PER_SIDE` | **1** | 06-08 |
| `LOSS_STREAK_THRESHOLD` / `COOLDOWN_HOURS` | 3 / 4h | 06-08 |
| `DAILY_LOSS_PCT_LIMIT` | 5% | 06-08 |
| `MARGIN_USDT` × `LEVERAGE` | 2000 × 5 = $10,000 | 06-08 |
| `SL_BUFFER_ATR` / `ATR_LEN` / `ATR_TF` | 2.5 / 14 / **1h** | 06-08 (was 5m) |
| `TRAIL_MULT_ATR` | **2.5** | 06-08 |
| `SPREAD_GATE_ENABLED` / `FEE_GATE_ENABLED` / `WALL_AVOIDANCE_ENABLED` / `SL_WALL_ANCHOR_ENABLED` | all **False** | 06-08 |

## 3c — Winners vs losers on entry-time fields

**n = 18. Every cell below is thin. I draw no conclusion from any of them; they are recorded so
the next pass has a starting point.** `score_stored` is `adj_score` (see §0.2 #1).

| vpos | side | result | score_stored | regime | ADX 1h | trend 1h/4h/1d | mtf | session |
|---|---|---|---|---|---|---|---|---|
| 7 | LONG | **WIN** +494 | 3.20 | TREND | 31.2 | bull/bull/neutral | 4 | us-late |
| 8 | LONG | loss −177 | 4.45 | TREND | 30.3 | bull/–/– | 1 | europe |
| 9 | LONG | loss −59 | 4.30 | TREND | 40.1 | bull/bull/neutral | 4 | asia |
| 10 | SHORT | loss −245 | 7.40 | TREND | 29.5 | bear/neutral/neutral | 3 | asia |
| 11 | SHORT | **WIN** +301 | 3.40 | TREND | 17.2 | bear/neutral/neutral | 3 | asia |
| 12 | LONG | loss −234 | 3.40 | TREND | 37.2 | **neutral/bear/bear** | 0 | asia |
| 13 | SHORT | **WIN** +327 | 3.25 | FLAT | 24.7 | bear/bear/bear | 4 | us-overlap |
| 14 | SHORT | loss −406 | 5.25 | TREND | 21.1 | bear/–/bear | 3 | us-overlap |
| 15 | SHORT | **WIN** +35 | 5.75 | TREND | 25.1 | bear/bear/neutral | 3 | asia |
| 16 | LONG | loss −195 | 6.35 | TREND | 27.0 | bull/neutral/neutral | 3 | europe |
| 17 | SHORT | **WIN** +1 | 2.34 | TREND | 18.4 | bear/bear/neutral | 4 | asia |
| 18 | LONG | loss −234 | 7.75 | TREND | 27.5 | bull/neutral/neutral | 3 | us-overlap |
| 19 | SHORT | **WIN** +89 | 4.40 | TREND | 22.2 | bear/neutral/neutral | 3 | asia |
| 20 | SHORT | loss −211 | 4.50 | FLAT | 34.1 | bear/bear/neutral | 4 | us-overlap |
| 21 | LONG | **WIN** +34 | 5.73 | TREND | 28.9 | bull/neutral/bear | 3 | europe |
| 22 | LONG | loss −203 | 4.25 | TREND | 25.8 | bull/bull/bull | 4 | asia |
| 23 | SHORT | loss −93 | 5.00 | FLAT | 36.9 | bear/bear/bear | 4 | europe |
| 24 | SHORT | loss −234 | 5.68 | TREND | 21.5 | bear/bear/bear | 4 | us-late |

What is visible, with honest n:

- **Higher stored score is associated with *worse* outcomes.** Winners mean 4.01, losers mean
  5.26. The three highest-scoring entries in the book (7.75, 7.40, 6.35) are all losses; the
  three lowest (2.34, 3.20, 3.25) are all wins. **n=18, 7 wins.** This is the wrong sign for a
  gate that is supposed to be a quality filter, and it is far too thin to act on.
- **Higher 1h ADX at entry is associated with worse outcomes.** Winners mean 24.0, losers mean
  30.1. The four highest-ADX entries (40.1, 37.2, 36.9, 34.1) are all losses. **n=18.**
- **Direction:** LONG 2/8 (25%), SHORT 5/10 (50%). LONG carries 57% of the net loss on 44% of
  the trades.
- **Trend alignment is not a discriminator here because there is almost no variance** — 17 of
  18 entries were 1h-aligned (LONG in bull / SHORT in bear). The one counter-trend entry
  (vpos 12, LONG with 1h neutral and 4h+1d bear) lost. **n=1.**
- **`mtf_alignment_score`:** winners {4,3,4,3,4,3,3}, losers {1,4,3,0,3,3,3,4,3,4,4}. No
  separation.
- **`market_regime`:** FLAT 1W/2L (n=3), TREND 6W/9L (n=15). No separation.
- **Combo weight (`weight_used`)** was 1.0 on 16 of 18 and 0.9 on two. The self-learning
  weight has had essentially no variance to contribute.

---

# §4 — HOW IT EXITS

## 4a — Everything that can close a position, in priority order

Priority is the order inside `virtual_trader._process_position`, which runs every
**10 seconds** (`MONITOR_POLL_SECONDS`); signal-driven closes arrive out-of-band on the webhook
thread.

| # | closer | live? | times fired (this book, n=18) |
|---|---|---|---|
| 1 | **Post-entry recheck — emergency close** (`post_entry_critical`, health ≤ −10, tiers T+10/60/300s) | enabled | **0.** All 18 rows ended `recheck_status='done'`. It fired exactly once ever — on **vpos 1**, 2026-06-08, in the deleted pre-book |
| 2 | **Post-entry recheck — defensive SL tighten** (health ≤ −5) | enabled | **0** (no row ever reached `recheck_status='tightened'`) |
| 3 | **Breakeven lock** — at +1R, moves SL to entry ± 0.20% and arms the trail | enabled | **armed 6/18.** Not itself an exit |
| 4 | **Stop loss** (initial 2.5×ATR, or the BE stop after #3) | enabled | **9** |
| 5 | **Trailing stop** — watermark ∓ `trail_pct`, only after #3 arms | enabled | **3** |
| 6 | **Timeout** | `MAX_POSITION_DURATION_MINS = 0` → **disabled** | **0, cannot fire** |
| 7 | **15m armed exit** — a 1h `Exit Signal` arms the side, an opposite BOS/CHOCH/Liq-Grab on 15m fires it | enabled | **6** |
| 8 | **5m Group B close + exit-AI** (`consult_for_close`) | **structurally unreachable in paper** | **0** |
| 9 | **EQH/EQL Smart TP** | **structurally unreachable — two independent reasons** | **0** |
| 10 | **1h trend-reversal close** | `TREND_REVERSAL_EXIT_DRYRUN = True` → log-only | **0, inert by design** |
| 11 | **Smart-exit giveback rule** | `SMART_EXIT_DRYRUN_ENABLED` — observational sampler | **0 acts; 48 would-exits recorded** |

**On #8 and #9 — two exit paths are dead in a way the config does not show.** Both
`_handle_5m_close` and `_handle_liquidity_sweep` decide whether to act by calling
`_fetch_open_position(symbol, side)`, which queries the **Bybit exchange**. In
`OBSERVATION_MODE` the exchange never holds a position, so both always take the "no open
position" branch. Consequences:

- `claude_advisor.consult_for_close` — the **exit** advisor — has never been consulted, and
  cannot be while the bot is in paper. Only the *entry* advisor is exercised.
- Every 5m Group B signal instead calls `_cancel_stop_orders(symbol)`, a real Bybit write
  endpoint, on a symbol that has no orders.

**#9 is dead a second time over, before it ever reaches that check.** The 5m router matches
sweeps with `signal_name.upper() in liquidity_sweep.SWEEP_TYPES`, and `SWEEP_TYPES = ('EQH',
'EQL')` — but TradingView sends the strings **"Equal H."** and **"Equal L."**. `"EQUAL
HIGHS" in ('EQH','EQL')` is False, always. Verified by import. Downstream:
`liquidity_sweep_state` has **0 rows**, `trades.status='sweep_recorded'` has **0 rows**, and
all 18 entries carry `liquidity_swept_before_entry = 0` and `context_weight_score = 0.0` — so
the `LIQUIDITY_SWEEP_WEIGHT_BONUS` (0.25) has never once been applied. 211 Equal-Highs/Lows
alerts have arrived and all 211 were handled as ordinary matrix context.

## 4b — Exit distribution and PnL

| close_reason | n | net USD | win rate | avg win | avg loss | mean R | median R |
|---|---|---|---|---|---|---|---|
| **sl** | **9** | **−1,961.00** | 1/9 = 11% | +0.86 | −245.23 | **−0.956** | −1.064 |
| exit_signal | 6 | **+555.06** | 3/6 = 50% | +294.79 | −109.77 | +0.351 | +0.100 |
| trail | 3 | **+395.69** | 3/3 = 100% | +131.90 | — | +0.587 | +0.285 |

The one "winning" stop (vpos 17, +0.86 = +0.004R) is a breakeven-lock stop, not a real stop.
**So: the stop has 9 outcomes and 8 of them are a clean −1R.**

**The +1R breakeven arm splits the book almost perfectly:**

- 6 positions reached +1R and armed → **6 of 6 finished at or above zero** (+2.089R, +1.337R,
  +1.133R, +0.285R, +0.140R, +0.004R; mean **+0.831R**).
- 12 positions never reached +1R → **11 of 12 lost** (the sole exception is vpos 19, +0.463R on
  a 15m armed exit; mean of the 12 is **−0.810R**).

That yields exactly the observed expectancy: 0.333 × 0.831 + 0.667 × (−0.810) = **−0.263R**.

**And this is where the post-07-05 collapse lives.** `TRAIL_MULT_ATR = 2.5` is identical to
`SL_BUFFER_ATR = 2.5`, so the trail callback distance **equals the full initial 1R**. The trail
arms at exactly +1R, which places its first trigger level back at the entry price — so the BE
stop (entry ± 0.20%) is the tighter of the two at the moment of arming, and the trail only
takes over once the watermark has advanced past +2R. Measured giveback on the four armed
positions that were not closed by a signal:

| vpos | peak excursion | closed at | given back |
|---|---|---|---|
| 13 | +2.36R | +1.337R (trail) | 1.02R |
| 15 | +1.18R | +0.140R (trail) | 1.04R |
| 17 | +1.18R | +0.004R (BE stop) | 1.18R |
| 21 | +1.44R | +0.285R (trail) | 1.16R |

Every one gives back ≈1R — which is the callback width, exactly as configured. The two big
winners in the book (+2.089R and +1.133R) were **not** taken by the trail; both were taken by
the 15m armed exit, which is the only exit here that has ever booked a large gain.

The bot's own observational sampler agrees and has been saying so for a month:
`smart_exit_dryrun_samples` (arm at MFE ≥ 1.2%, exit on 0.8% giveback) recorded **48
would-exit events across vpos 15–21** — including 25 on vpos 18, which armed 26 times under
that reference rule and nevertheless finished at a full −1.07R under the live rule. It is
DRYRUN and has never acted.

## 4c — Where the stop lives

**In this bot's own poller, in Python, in the gunicorn worker process. Nothing rests on
Bybit.** In `OBSERVATION_MODE` `_execute_single_entry` returns before any exchange call, and
`virtual_trader.execute_entry` writes `sl_price` into `virtual_positions` and nothing else. The
poller re-reads it every 10s and compares against a `fetch_ticker` last price fetched through
Tor.

Direct consequences: (i) the stop is only as good as the 10-second poll and the Tor round-trip
— an adverse move between ticks fills at the *tick* price, not at the stop level (vpos 24
filled at exactly 74.29 = the stop, but vpos 13 "trailed" out 2.18 below its trail level);
(ii) a worker restart with an open position leaves it unprotected until
`_reconcile_open_virtual_positions` runs at boot; (iii) **the entire stop/trail mechanism is
paper-only code that has never been exercised against a real exchange.**

The trail **exists, arms and has fired** — 6 arms, 3 trail exits, all three profitable. It is
the only exit besides the stop that the poller has ever executed.

---

# §5 — WHAT IS RUNNING

## 5a — Service health

| | |
|---|---|
| `mercury-sol.service` | **active**, master PID 1793275, worker **1794078** |
| started | **2026-07-21 06:39:51 UTC — uptime 11d 07h** |
| restarts | 0 within the journal window (07-30 20:55 →). Why it restarted on 07-21 cannot be recovered — the journal is rotated past it |
| worker RSS | 356 MB |
| OOM armor | `OOMScoreAdjust=-900`, `MemoryMin=600M` drop-in present |
| `mercury-sol-optimizer.timer` | active, last run **2026-08-01 14:00**, exit 0 |
| `mercury-sol-optimizer-listener` | active, **up since 2026-07-13 16:08 (18d)** |
| tracebacks | **0** in the journal window |

**Tor → Bybit: working.** `tor.service` active, SOCKS on 127.0.0.1:9050, live exit IP
45.66.35.35, and a direct probe of the Bybit SOL/USDT ticker through the proxy returns
**HTTP 200 in 3.0 s**. 231 `SOCKS_RETRY` lines and 27 `403`s in the 2-day journal — the
circuit is being rotated regularly and recovering each time. One `OKX fallback (Bybit/Tor
fail…)` event.

**OKX book: working.** Direct, keyless, no Tor (`liquidity_zones.py` →
`https://www.okx.com/api/v5/market/books-full`, 4000 levels). Live probe **HTTP 200 in
0.75 s**. Recent advisor prompts quote real wall multipliers (×14–×23 at $72.75/$73.25), so it
is being fetched and parsed at decision time.

**One degraded input: CryptoPanic returns HTTP 404 — 164 times in 2 days.** The endpoint in
`macro_filter.py` is `https://cryptopanic.com/api/free/v1/posts/`. `macro_filter` fails soft
and still produces a category from the RSS side, so `macro_news_category` is never NULL — but
`MACRO_GATE_DRYRUN=False` means the macro penalty **is** applied at the score gate (82 of 86
advisor-reaching signals on 07-31 carried a non-zero penalty), and one of its two inputs has
been dead throughout. The four RSS feeds themselves are mostly fine, degrading today: 15 of 24
advisor-reaching rows on 08-01 had a NULL `news_summary`, vs 0 on 07-28/29/30.

## 5b — Every SOL background job

| job | schedule | what it watches | last run | has it produced anything? |
|---|---|---|---|---|
| `mercury-sol-optimizer` | daily 14:00 UTC | re-weights `optimizer/dynamic_weights.json` from the closed book | 2026-08-01 14:00 | yes — 60 runs. But see 5c: what it writes reaches no decision |
| `mercury-sol-optimizer-listener` | resident | Telegram CONFIRM callbacks → would write `optimizer/filters.json` | up 18d | **never produced a file** — `filters.json` does not exist |
| `mercury_sol_prior_move_logger.py` | every 6h | prior-move oracle | 2026-08-01 12:19 | yes — 42,329 oracle samples, 18 entries tracked |
| `sol_downtrend_regime_watch.sh` | daily 08:23 | bear-regime census | 2026-08-01 08:23 | yes — fired 8 of the last 12 days (N=210 today) |
| `sol_uptrend_regime_watch.sh` | daily 08:47 | uptrend-strength census | 2026-08-01 08:47 | yes, but **has not fired since 07-22** (N=2 vs threshold 30) |
| `mercury_sol_30trade_reminder.sh` | Mondays 09:00 | 30-closed-trade sentinel + Lever B digest | **2026-07-27 09:00** | yes, and it is the honest one: *"closed=16 threshold=30"*. **It did not run on 2026-08-03's predecessor — the last entry in the log is 07-27**, and it logged `db-read-failed (got 'ERR')` on 07-13 |
| Skip-Attribution O. (in-process) | continuous | tracks every skip for 15m/1h/4h/12h/24h drift | live | **the richest dataset the bot owns** — 8,555 skips × 5 horizons = 42,775 samples, 99.9% completed, 6 degraded |
| Post-Exit Observatory (in-process) | continuous | shadow-exit counterfactual per position | live | 21 rows, all `completed` except vpos 5 |
| Excursion logger (in-process) | 60s/dense 15m | MFE/MAE path | live | 2,613 samples — **vpos 15 onward only** |
| Smart-exit DRYRUN sampler (in-process) | hourly | giveback-rule counterfactual | live | 218 samples, **48 would-exit events**, never acts |
| Combo-weight audit (in-process) | continuous | scores combo keys after closes | live | 12 combos scored, weights 0.8–1.1 |
| **SOL healthcheck** | — | — | — | **NOT SCHEDULED.** `healthcheck.py` exists (dated 2026-06-03) but no timer or cron invokes it, and there is no `healthcheck_state.json` in the SOL directory. The system `healthcheck.timer` runs a different bot's script (`WorkingDirectory=/root/titan-bot`). **SOL has no health monitor of its own.** |

## 5c — Flags that are ON but have never had an effect

| flag | value | why it does nothing |
|---|---|---|
| `FILTER_ENFORCEMENT_ENABLED` | True | `optimizer/filters.json` **does not exist**; `load_filters_cached` returns an empty set on `OSError`. **0 `filter_blocked` rows ever.** Additionally `FILTER_ENFORCEMENT_DRYRUN=True` would neuter the extension class even if the file appeared |
| `NEUTRAL_1H_LONG_FOLLOWTHROUGH_ENABLE` | True | **0 `neutral1h_armed` rows and 0 rows in `neutral1h_followthrough`** in the 31 days since it shipped. It has never armed once |
| `EQH_EQL_SMART_TP_ENABLED` | True | unreachable — the sweep router can never match "Equal H."/"Equal L." (§4a), and even if it did, `_fetch_open_position` is exchange-backed and always empty in paper |
| `ADVISOR_WALL_ALIGNED_V2_DRYRUN` | True | **ignored.** The code reads `_shadow = DRYRUN and not MASTER`, and the master is True. The flag reads "shadow-only" and has no force whatsoever |
| `ADVISOR_WALL_ALIGNED_SHORT_V2_DRYRUN` | True | same — ignored, master is True |
| `TRAIL_ACTIVATION_ATR_FIXED` (5.0), `TRAIL_MIN_ACTIVATION_PCT` (0.0025) | set | **not used in the arm distance.** `trail_arm.activation_distance` returns `SL_BUFFER_ATR × atr`; these two are only read by the import-time assertion, which now guards an invariant about values that no longer drive anything. Verified against the book: arm distance == 1R on all 18 rows |
| `TRAIL_ACTIVATION_ATR` (0.5) | set | flag-OFF legacy path only; `TRAIL_ARM_FIX_ENABLED=True` |
| `ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN` | True | the fresh-ATR trail recompute at +1R is computed and logged, then discarded; the frozen value is used |
| `TREND_REVERSAL_EXIT_DRYRUN` | True | 1h trend-reversal close logs "would close", never closes |
| `DXY_HALT_DRYRUN` | True | observes and logs, never blocks |
| `SMART_EXIT_DRYRUN_ENABLED` | True | observational by design — 48 would-exits recorded, 0 acted on |
| `MAX_POSITION_DURATION_MINS` | 0 | timeout close disabled |
| `PARAM_TUNING_ENABLED` | False | off |
| `SPREAD_GATE_ENABLED`, `FEE_GATE_ENABLED`, `WALL_AVOIDANCE_ENABLED`, `SL_WALL_ANCHOR_ENABLED` | False | deliberately disabled. 0 rows for `spread_blocked` / `fee_gate_rejected` / `wall_blocked` |
| `LEARNING_ENABLED` | True | works, but thin — 15 rows carry `learning_at`, 12 combos scored, 16 of 18 entries saw weight exactly 1.0 |

**Two more that are ON, do something, and cost money for it:**

- **`ADVISOR_WALL_RULE_V2_DRYRUN = True` with the master False fires a *second* Claude call on
  every single advisor skip** — the guard is `if decide == 'skip' and DRYRUN and not MASTER`,
  with no direction or regime gate. 110 shadow calls in the 2-day journal window (≈55/day),
  of which 107 agreed with the skip and 3 logged a would-flip. Over the book that is on the
  order of 2,873 extra Haiku calls whose only output is a log line.
- **The two *live* aligned relaxations also each cost a second call, and in the observed window
  they flipped nothing.** 37 invocations (24 LONG, 13 SHORT), **0 FLIP, 37 HELD** — the SOFT
  prompt agreed with the hard veto every time. That is the 2-day window only; the DB cannot
  distinguish a flipped verdict from a normal one, because of §0.2 #4.

- **The optimizer's daily output reaches no decision.** It rewrites
  `optimizer/dynamic_weights.json` every day from cells of n=6, n=7, n=10 — drawn from an
  18-trade book — and `weight_engine.weighted_adj` is explicitly storage-only
  (*"Never applied to the gate check"*). It moves `confluence_score` in the DB and nothing
  else. It is not harmful; it is measuring noise and writing it down.

---

# §6 — THE HONEST SUMMARY

## Condition

The machine is **healthy and the strategy is not**. Every piece of infrastructure I checked is
doing its job: 11 days of uptime with no tracebacks, Tor routing Bybit correctly, the OKX book
live, 8,555 skips tracked to five horizons with 99.9% completion, an excursion logger, a
shadow-exit sampler, a post-exit observatory. This bot has better instrumentation than it has
trades. In 55 days of continuous operation it has opened **18 positions** and lost **$1,010 on
$10,000 notional**, all on paper.

## Ranked by what it appears to cost

**1. The trail callback equals the full initial risk — it gives back ~1R on every armed
winner.** `TRAIL_MULT_ATR = 2.5 = SL_BUFFER_ATR`. All four armed positions not rescued by a
signal exit gave back 1.02R, 1.04R, 1.16R, 1.18R. This is the single largest identifiable
leak: it converts +1.2R…+2.4R excursions into +0.00R…+0.29R. Post-07-05 the win *rate* held at
40% while the average win collapsed from +374 to **+40**. The bot's own DRYRUN sampler logged
48 would-exit events under a tighter giveback rule and was never allowed to act. **Estimated
cost: on the four affected trades alone, ~4.4R ≈ $900 — i.e. roughly the entire drawdown.**

**2. The advisor refuses 97.7% of everything that reaches it, and reopening the funnel did not
change that.** 2,873 of 2,942. It refused for 13 consecutive days in June/July. Its refusals
are near-identical text about FLAT regime, ADX ≈ 21 and walls — and at least two in the last
two days named the wrong direction. Meanwhile the thin evidence points the *other* way from
what the gates assume: the highest-scoring and highest-ADX entries in the book are the losers.
**Cost: it is the binding constraint on sample size, which is why nothing else can be
measured.**

**3. Three exit paths are structurally dead and the config does not show it.** The exit advisor
(`consult_for_close`) has never been consulted and cannot be in paper mode; the 5m Group B
close and the EQH/EQL Smart TP both gate on an exchange position that never exists. The Smart
TP is dead twice over — the router matches `'EQH'/'EQL'` against TradingView's *"Equal
Highs"/"Equal L."*, so 211 sweep alerts have been silently discarded and the
`LIQUIDITY_SWEEP_WEIGHT_BONUS` has never once applied. **Cost: unmeasurable, because it has
never run — but note that the 15m armed exit, the one signal exit that *does* work, produced
both of the book's large winners.**

**4. The per-side cap discards three quarters of all fully-qualified signals.** 68 passed every
gate; 50 were refused by `MAX_POSITIONS_PER_SIDE=1` because a position was already open on that
side, and the advisor's agreement arrives in bursts (9, 9, 8, 8 in a day). The cap is a correct
risk control; the point is that it, not the gates, sets the ceiling on trade count.

**5. Measurement rot.** `confluence_score` means three different things; `signal_type`
mis-labels 3 of 9 stop exits as stops when they were trails; `trades_close_row_id` is read by a
report and written by nothing; `ai_system_prompt` records the wrong prompt on every relaxed
verdict; vpos 1–6 are gone. **Cost: every past and future analysis of this book is one careless
query away from a wrong answer.**

**6. Flags that read as armed and are not** — `FILTER_ENFORCEMENT_ENABLED` with no filters
file, `NEUTRAL_1H_LONG_FOLLOWTHROUGH` never armed once in 31 days, two `*_DRYRUN` flags whose
value is ignored, an arm-distance constant superseded but still asserted on. **Cost: they make
the config an unreliable description of the bot.**

**7. No health monitor.** The system `healthcheck.timer` runs another bot's script. SOL's own
`healthcheck.py` has never been scheduled. The one sentinel that *is* SOL's — the Monday
30-trade reminder — last logged on **2026-07-27** and reported `closed=16 threshold=30`. Its
own honesty is the reason this bot went 11 days unexamined without anyone noticing.

**8. Degraded inputs.** CryptoPanic 404s (164× in 2 days) into a macro gate that **is** live
(`MACRO_GATE_DRYRUN=False`); RSS news is degrading today (15 of 24 rows NULL vs 0 three days
ago).

**9. The optimizer is fitting noise.** Daily weight updates from n=6/n=7/n=10 cells on an
18-trade book. It happens to be harmless because `weighted_adj` never touches the gate — but
that also means the self-evolution loop has never evolved anything.

## The question you asked

**It barely trades — and that is the first problem, but not because the answer is "loosen the
gates".**

The two readings need separating, because the data supports a specific one:

- **"It trades badly"** is not yet a claim anyone can make. n=18, of which 8 predate the last
  mechanism change. Every cell in §3c is under n=10. The book is a wash pre-07-05 (+1.73 on 8)
  and −1,012 post (on 10). You cannot distinguish a bad edge from an unlucky ten trades at
  this sample size, and the two eras are not the same bot.

- **"It barely trades"** is measurable and it is the binding constraint: 0.33 entries/day,
  27% time in market, three droughts of 12.6, 7.3 and 2.8 days. **Sample size is the resource
  this bot is starving for, and every question you would want to ask about entry quality is
  blocked on it.**

But the honest version of "it barely trades" is not "the gates are too tight". It is this:
**the funnel was already reopened on 06-29 and 07-04 and it barely moved the needle** —
+63% more fully-qualified candidates produced +0.11 entries/day, because the advisor's kill
rate did not budge (97.5% → 97.8%) and the per-side cap absorbed three quarters of the rest.
Loosening upstream again would repeat that result.

Meanwhile the *one* thing in this book that is measurable at n=18 is not an entry problem at
all. **The bot reaches +1R on a third of its trades and finishes six for six non-negative when
it does — and then hands back essentially the entire excursion, by exactly the amount its trail
is configured to hand back.** That is a single constant, its effect is arithmetic rather than
statistical, and the bot's own DRYRUN sampler has been recording the counterfactual for a
month.

**My read: the first problem is that it barely trades, and the reason it barely trades is a
single gate (the advisor) that upstream loosening cannot route around. The most defensible
thing visible in the data, however, is the exit, not the entry — because it is the only finding
here that does not depend on n=18.**

I have changed nothing. This pass was diagnosis only.

---

*Evidence: `/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db` (14,904 signal rows, 18
positions, 8,555 tracked skips, 42,775 drift samples), `main.py`, `config.py`,
`claude_advisor.py`, `virtual_trader.py`, `trail_arm.py`, `liquidity_sweep.py`,
`filter_enforcement.py`, `weight_engine.py`; `journalctl -u mercury-sol` (2026-07-30 20:55 →
2026-08-01 14:30); systemd units and root crontab; live probes of Tor→Bybit and OKX at
2026-08-01 14:35 UTC.*
