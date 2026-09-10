# Mercury-SOL — why no SHORT on the two-day decline: the 1H LuxAlgo tier stood LONG, then the advisor said "flat" at ADX 46

**2026-09-10 22:50 UTC · READ-ONLY post-mortem · Mercury-SOL (LIVE, `is_paper=0`) · window 2026-09-09 00:00 → 2026-09-10 22:40 UTC**

## VERDICT (one answer)

**Shorts WERE proposed — 178 of them — and a NAMED mechanism refused every one that mattered. Two mechanisms, in sequence, and neither is the daily regime any more:**

1. **The HTF cascade refused 76 of 178**, 58 of those because the **1H LuxAlgo tier itself stood LONG** for two of the three legs of the decline (`Smart Trail Switch Bullish` from 09-08 17:00 until 09-09 11:00; `HyperWave OS Signal Up` re-arm from 09-09 23:30 and `Bullish Confirmation` at 09-10 05:00 until 09-10 10:00). The bot's own trend tier pointed UP while price fell 105 → 101.
2. **Every SHORT that cleared the cascade and the score bar reached the advisor — 58 — and the advisor declined all 58.**
   - **Before 09-09 20:10 (26 refusals):** the daily-regime standing order. 25 of 26 cite `1d BULL`. **The label was CORRECT at those moments**: independent recomputation from Bybit daily candles matches the stored label at 56 of 58 refusal instants (the 2 misses are a ≤1 h cache lag at the margin, price 0.1 % under EMA9, not a classifier defect). The daily label left `bull` at **09-09 20:10**, the first evening print under EMA9, and it has been `neutral` since.
   - **After the flip (32 refusals, all of 09-10):** `1d BULL` is cited **0 times**. The advisor now cites **order-book walls (20 of 32)**, **15m/1H LuxAlgo opposition (20)**, and **"FLAT regime" (19)** — the last one while **1h ADX read 39–47 and the OHLCV 1h trend read BEAR**. That `market_regime=FLAT` is the LuxAlgo-slot label (`signal_matrix.py:355`: `'TREND' if trend_net_dir != NEUTRAL else 'FLAT'` — it says FLAT whenever the matrix TREND category carries no points), which the advisor's own source comments as "that label is broken" (`claude_advisor.py:213`). The advisor was told the market was flat by a label that reads the LuxAlgo slot, not the tape.

**What did NOT bind:** no position was open at any point in the window (cap never engaged) · book gate refused **0** shorts (1 long) · flat-ADX gate is DRYRUN and refused nothing; its 29 "would-refuse" shorts in the window were all 09-09 rows the advisor had already skipped · macro blackout 0 · risk halt 0 · counter-entry suppression 0. The 11 `entry_gate_refused` rows are same-second duplicate webhooks, not distinct opportunities.

**What the shorts would have made (serial, `MAX_POSITIONS_PER_SIDE=1`, live geometry, real 5m candles): n=5, ΣR +1.08R, Σ$ +2.55. Over the 58 advisor refusals alone: n=4, ΣR +0.72R, +$1.74. n < 8 — descriptive only.** An 8 % three-day slide yields about one R under this geometry because the first short (09-09 00:35 at 103.64) sits 16 hours in chop to a breakeven exit, and the 1.875×ATR trail gives back most of each leg.

---

## 1. The move, then the funnel

### 1a. The move (Bybit linear SOLUSDT, fetched read-only via the bot's Tor egress; api.bybit.com is CloudFront-blocked from this box's own IP)

| | |
|---|---|
| Window high | **107.05 @ 2026-09-07 02:00 UTC** |
| Low after the high | **98.30 @ 2026-09-10 12:00 UTC** |
| High → low | **−8.17 % = 8.50 × ATR(1h)** (ATR14 at the high = 1.029) |
| High → last (99.29 @ 22:00 close) | −7.25 % = 7.54 ATR |
| 09-09 daily | o 103.31 · h 105.15 · l 100.07 · c 101.50 · **−1.75 %** |
| 09-10 daily (in progress) | o 101.50 · h 102.15 · l 98.30 · c 99.31 · **−2.16 %** |
| 09-09 00:00 → now | 103.31 → 99.29 = **−3.89 %** |
| Ticker 22:41 UTC | last 99.31 · 24 h −1.96 % · 24 h range 98.30–102.15 (operator's 99.69 / −1.97 % matches) |
| ATR(1h) now | 0.865 = 0.87 % of price |
| Position in range | **11 % of the 7-day range** (98.30–107.32) · 15 % of 14-day (97.29–110.61) · 57.5 % of 30-day (83.95–110.61) |

Hourly closes: 09-09 held 103–104.8 until 18:00, broke to 100.7 at 22:00; 09-10 chopped 101–102 until 11:00, broke to 98.9 at 12:00, then 99.3–100.1 into the close. **Two legs down, each preceded by 10+ hours of a 1.5 % chop.**

### 1b. Every signal received (518 webhook rows since 09-09 00:00)

397 entry proposals: **219 LONG, 178 SHORT.** The remaining 121 rows are tier bookkeeping (47 `15m_confirm`, 28 `5m_liquidity_ctx`, 26 `no_trend`, 9 `1h_trend_set`, 2 `trend_reset`, 2 `trend_rearmed`, 8 `exit_unarmed_noop`). All 178 SHORT rows with tier composition, cause of death and replay outcome are in the appendix.

**The 1H tier was supplied the whole window. Its DIRECTION is the story:**

| 1H tier event (webhook) | UTC | tier direction |
|---|---|---|
| Smart Trail Switch Bullish | 09-08 17:00 | LONG |
| **Bearish Confirmation / Any Bearish Confirmation** | **09-09 11:00** | SHORT |
| Smart Trail Switch Bearish | 09-09 20:00 | SHORT |
| 60m Exit Signal (trend reset) | 09-09 22:00 | — |
| re-arm: HyperWave OS Signal Up | 09-09 23:30 | LONG |
| Bullish Confirmation / Any Bullish Confirmation | 09-10 05:00 | LONG |
| **Bearish Confirmation+ / Any Bearish Confirmation** | **09-10 10:00** | SHORT |
| Neo Cloud Switch Bearish · Trend Tracer Down | 09-10 13:00 · 14:00 | SHORT |
| 60m Exit Signal (trend reset) | 09-10 17:00 | — |
| re-arm: HyperWave Signal Down | 09-10 18:30 | SHORT |

Of the 178 SHORT proposals, **105 fired while the 1H tier stood LONG**, 73 while it stood SHORT.

### 1c. Where each SHORT died (178)

| Cause | n | verbatim / mechanism |
|---|---|---|
| **HTF cascade** (`htf_blocked`) | **76** | 58 × `SHORT blocked — 1H tier OPPOSES (needs SHORT)` · 14 × `15m tier OPPOSES` · 4 × `NEUTRAL-expired`. The block reason is not persisted as text (only the −10/−7.5 penalty and `combo_key`); attribution is reconstructed from the tier names in `combo_key`, and the retained journal (from 09-09 22:05) confirms the cascade path line-for-line. |
| **Advisor** (`ai_skipped`) | **58** | quoted in §2c and the appendix |
| **Score bar** (`below_threshold`) | **33** | `direction_score < CONFLUENCE_SCORE_THRESHOLD = 2.0` — scores −0.73 … 1.91; four rows at 2.21 fell under the live-param threshold at 12:40 09-10 |
| **Entry lock** (`entry_gate_refused`) | **11** | `concurrent SHORT entry already in flight for SOL/USDT:USDT — refused, not queued` — all within 0–2 s of a sibling row, i.e. duplicate webhooks of the same instant |
| Flat/ADX gate | **0** | DRYRUN: 29 SHORT `would-refuse` lines in the window, ALL on 09-09 (ADX 12.0–17.8); none on 09-10 (ADX 26.8–47.0) |
| Book gate | **0** | 1 LONG refused 09-10 06:50 (`opposing wall x20.0 at p94 (this side) only 0.196% away`) |
| Position cap | **0** | `active_positions` empty; no `virtual_positions` row open since vpos 43 closed 09-06 03:58 |
| Counter-entry suppression / macro blackout / risk halt | **0 / 0 / 0** | none in the window (last `risk_halt` 09-06 01:15) |

LONG side for symmetry: 219 → 124 cascade, 46 advisor, 34 score bar, 14 entry lock, 1 book gate. **Zero entries either side.**

### 1d. How many SHORT proposals existed at all — 178. The question is not "why no signal"; it is which mechanism refused them, answered above.

---

## 2. The daily regime — has it flipped, and is the standing order still binding?

### 2a/2b. Stored label vs independent recomputation (classifier = bot's own `_classify_trend`: `close > ema9 > ema21 and slope3 > 0.05 %` → bull; mirror → bear; else neutral; EMA via pandas_ta, same as the bot)

| day | daily candle (o → c, %) | stored `trend_1d` | stored `trend_4h` | recompute AS OF CLOSE | close vs EMA9 |
|---|---|---|---|---|---|
| 09-07 | 106.49 → 103.73 **−2.59 %** | bull (79 rows, all day) | neutral/bull alternating | **bull** — 103.73 > 102.81 > 97.87, slope +1.55 % | above |
| 09-08 | 103.73 → 103.31 **−0.40 %** | bull (64) with **neutral 06:25–14:15** (13 rows, intraday dip under EMA9) | bear from 06:40, neutral/bull later | **bull** — 103.31 > 102.91 > 98.37, slope +1.27 % | above |
| 09-09 | 103.31 → 101.50 **−1.75 %** | **bull until 19:15 → neutral from 20:10** | neutral / bull; **bear from 15:25** | **neutral** — 101.50 < EMA9 102.63; slope +0.049 % (< 0.05) | **below (1st close)** |
| 09-10 | 101.50 → 99.31 **−2.16 %** (in progress) | neutral (39 rows, all day) | bear all day | **neutral** — 99.31 < 101.96, but EMA9 101.96 > EMA21 98.71 ⇒ not bear; slope −0.83 % | **below (2nd, open)** |

**Match at the moment of every SHORT advisor refusal: 56 of 58.** The bot's label is computed on the live (in-progress) daily bar, so I recomputed each instant with the 5m price as the bar's close. The two misses are rows 25299 (09-09 15:10, price 102.78 vs EMA9 102.88) and 25310 (15:25, 102.60 vs 102.85): stored `bull`, recomputed `neutral`. The 1d OHLCV is cached 3600 s (`indicators._CACHE_TTL_BY_TF['1d']`), and one hour earlier price was 103.7, above EMA9. **A ≤1 h lag at 0.1 % from the line, not a defect. The label did not say `bull` for two closes under EMA9: it left `bull` at 20:10 on the first evening under EMA9, before the first such close printed.**

### 2c. SHORT refusals citing the daily regime

**25 of 58** cite `1d BULL` — **25 of the 26 before the flip, 0 of the 32 after.** Three verbatim:

- 25189 · 09-09 06:25 · `SHORT opposes dominant 1d/4h/1h/15m/5m BULL regime (0/4 MTF align). FLAT market (ADX 1h 15.2, ATR% 0.767%), stale 1h signal (13.4h old). Thick ask wall p86 x16.5 blocks upside but regime is bullish.`
- 25283 · 09-09 13:45 · `1d BULL (ADX 52.2) strongly opposes SHORT; 1h/4h NEUTRAL weak. Flat squeeze: 1h ADX 12.9, EMA Flat. Skip.`
- 25299 · 09-09 15:10 · `1d BULL (ADX 52.2) conflicts with SHORT; 1h ADX 12.4 + 1h EMA contracting = weak trend. Skip.`

And three from after the flip, which is what binds now:

- 25364 · 09-09 20:25 · `1d NEUTRAL w/ high ADX 52.2 + contracting EMA contradicts SHORT. 4h weak ADX 13.0. Flat-market risk.`
- 25566 · 09-10 15:25 · `15m HyperWave opposes SHORT; 15m EMA contracting + 5m volume weak (0.38x); bid wall at $99.75 (p54, x8.6) blocks SHORT momentum.` — at this instant the prompt's own OHLCV block read `1h: BEAR, ADX 46.0, Expanding · 4h: BEAR · 5m: BEAR · MTF 3/4 · market_regime TREND`, and the cascade had just logged `15m=NEUTRAL (no active MOMENTUM signal)` — the "opposing" 15m tier was TTL-expired.
- 25610 · 09-10 22:20 · `FLAT-MARKET GUARD triggered: 1h ADX 46.4 strong, but 15m ADX 17.0 weak + EMA-gap Contracting (1h 0.552%, 15m 0.024%) + market_regime FLAT + MTF alignment 1/4. Massive ask wall at $100.25 (p79, x14.3)` — `market_regime FLAT` here comes from an empty LuxAlgo TREND slot (`TREND: signal_count 0`), not from ADX.

### 2d. The lag

The label leaves `bull` on the **first live print** under EMA9 — zero closed bars required — and did so at 09-09 20:10. Two daily closes under EMA9 have printed (09-09 closed, 09-10 in progress). To reach `bear` it needs `close < EMA9 < EMA21`, i.e. an EMA9/EMA21 cross-down: holding 99.31 flat it **never** gets there within 39 days; at −1 %/day it needs **6 more closes** (≈93.5). `trend_1d = bear` will not exist for this move unless it turns into a crash. The standing order ("lean toward skip when 1d/4h clearly oppose") is therefore **not binding since 20:10 on 09-09** — 1d is `neutral`, 4h is `bear`, and the advisor stopped citing it.

---

## 3. The flat-ADX gate in DRYRUN

### 3a. Runtime state

- `config.py:407` reads `FLAT_ADX_GATE_DRYRUN = True` (as text). The running process (PID 3442516) started **2026-09-03 19:45:15 UTC**, after the flip; `NRestarts = 0` before and after this audit.
- syslog: the last armed line is `[FLAT-ADX-GATE] REFUSE LONG row=23612 ADX(1h,200)=18.97` at 09-03 14:55; **0 `REFUSE` lines after 19:30 on 09-03**; the first `DRYRUN would-refuse` line is 09-05 11:30 (row 24147). (The systemd journal only retains from 09-09 22:05; syslog/syslog.1 carry the full span.)
- **"Would have refused" rows since the flip: 136 unique (77 LONG / 59 SHORT).** In this window: 65 (36 LONG / 29 SHORT).
- **Entries taken since the flip: 1** — vpos 43 LONG, row 24167, 09-05 13:05, ADX(1h,200) 18.53, **on the would-refuse list** → closed by trail **+1.723R, +$2.17**. So the armed gate would have blocked 1 of 1 entries, and that one was a winner.

### 3b. The paired comparison during this decline

| leg | SHORTs that reached the advisor | ADX(1h) | armed gate would have | advisor did |
|---|---|---|---|---|
| 09-09 00:50–15:25 (1d still bull) | 26 | 12.0–17.8 | **refused all 26** | skipped all 26 |
| 09-09 20:10–20:30 (1d just flipped) | 3 | 16.6–16.8 | refused all 3 | skipped all 3 |
| **09-10 01:10–22:35** | **29** | **26.8–47.0** | **passed all 29** | **skipped all 29** |

The dryrun changes nothing here: on 09-09 both the gate and the advisor said no; on 09-10 the gate would have admitted every short and the advisor refused them anyway. **The ADX floor is not what binds; the advisor is.**

### 3c. Stopping rule

| | baseline 09-03 19:45 | now |
|---|---|---|
| n | 14 | **15** |
| ΣR | +6.141R | **+7.864R** (Δ **+1.723R**) |
| Σ$ | +$15.56 | **+$17.73** |

Rule: revert at ΣR ≤ +3.141R OR at 2026-09-17 19:45 UTC. **Neither has fired** (+4.72R of room; 7 days left).

---

## 4. What the shorts would have made

Replay on real Bybit 5m candles: market fill at the row's price (5m close where the row carries none), **SL = 2.5 × ATR14(1h)** of the last closed hour, **arm at 0.75R**, **breakeven lock at entry −0.20 %**, **trail 1.875 × ATR from the water mark, active only after the lock**, **taker 0.100 % both legs**, **$100 notional**, **adverse extreme first inside each bar**, to its own exit or the 22:40 print.

| cut | n | ΣR | Σ$ | exits |
|---|---|---|---|---|
| every SHORT independently (all 178) | 178 | +55.21R | +$116.00 | 128 trail · 25 BE · 25 still open — 178 overlapping positions, physically impossible, shown for the shape only |
| the 58 advisor refusals independently | 58 | +14.32R | +$30.17 | 36 trail · 7 BE · 15 open |
| **serial over all 178, cap 1 per side (THE DECIDING CUT)** | **5** | **+1.08R** | **+$2.55** | below |
| serial over the 58 advisor refusals | 4 | +0.72R | +$1.74 | below |

Serial over all 178:

| row | entry UTC | price | ATR | 1R | exit | R |
|---|---|---|---|---|---|---|
| 25107 (cascade) | 09-09 00:35 | 103.64 | 0.824 | $1.99 | BE 103.43 @ 09-09 16:30 | −0.00 |
| 25321 (cascade) | 09-09 16:35 | 103.32 | 0.932 | $2.26 | trail 101.82 @ 09-10 02:50 | **+0.56** |
| 25436 (advisor) | 09-10 02:50 | 101.83 | 0.993 | $2.44 | trail 100.16 @ 09-10 14:25 | **+0.59** |
| 25565 (entry lock) | 09-10 15:25 | 99.57 | 0.996 | $2.50 | open @ 99.31 | +0.02 |
| 25615 (score bar) | 09-10 22:40 | 99.31 | 0.869 | $2.19 | open @ 99.31 | −0.09 |

Serial over the 58 advisor refusals: 25111 09-09 00:50 → BE (+0.00) · 25363 09-09 20:10 → trail 101.76 (+0.11) · 25436 09-10 02:50 → trail 100.16 (+0.59) · 25566 09-10 15:25 → open (+0.02).

**n = 5 (or 4) — under 8; descriptive only.** The descriptive answer: the refused shorts were right on direction (164 of 178 independent replays end positive) but the serial book collects about **one R** from an eight-percent slide, because the trigger fires at the top of each chop and the 1.875×ATR trail exits before the leg completes.

---

## Read-only confirmation

- DB opened `file:…/trades.db?mode=ro`, SELECT only · cwd = session scratchpad, never inside the SOL tree · `config.py` read as text (`grep`/`sed`), never imported · no writes, no orders, no restarts · venue and public data via GET only (candles + ticker through the bot's own Tor egress; api.bybit.com refuses this box's IP with a CloudFront country block).
- `mercury-sol.service`: MainPID 3442516, **NRestarts 0 → 0**, ActiveEnterTimestamp 2026-09-03 19:45:15 UTC unchanged.
- File hashes (36 files, `*.py`, `.env*`, `*.json`, `trades.db`) taken before and after: **34 identical**; the two that moved are `trades.db` and `oi_cache.json`, both written by the running bot itself (`market_context.py:94` writes the OI cache after every update) — not by this audit.
- `FLAT_ADX_GATE_DRYRUN` still `True` at `config.py:407`; 0 armed `REFUSE` lines since the flip.
- Titan: `openitems_guard` exit 0 (14 watched values agree, HEAD cd0f175); nothing else touched. Book gate armed 2026-09-10 14:36:20 is untouched.

Nothing proposed, nothing applied.

---

## Appendix — all 178 SHORT proposals, in order

| # | row | UTC | 1H tier | 15m tier | 5m trigger | score | ADX1h | died at | verbatim / cause | replay (indep.) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 25107 | 09-09 00:35 | Smart Trail Switch Bullish | HyperWave Signal Up | Bearish New Imbalance | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | be -0.00R |
| 2 | 25111 | 09-09 00:50 | Smart Trail Switch Bullish | HyperWave Signal Up | Bearish Imbalance Mitigated | 2.5 | 17.8 | ai_skipped | advisor skip: SHORT opposes 1d BULL (ADX 52.1) + 4h/1h/15m trend. Flat market (ADX 17.8/14.5, ATR 0.773%/0.320%), MTF 0/4. 1H stale. Ask wall $104.25  | be +0.00R |
| 3 | 25115 | 09-09 01:00 | Smart Trail Switch Bullish | HyperWave Signal Up | Bearish Liquidity Grab | -7.5 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | be -0.00R |
| 4 | 25122 | 09-09 01:25 | Smart Trail Switch Bullish | HyperWave Signal Up | Bearish New Imbalance | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.83R |
| 5 | 25128 | 09-09 01:45 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish Imbalance Mitigated | -8.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.00R |
| 6 | 25134 | 09-09 02:10 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish Liquidity Grab | -8.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | be +0.00R |
| 7 | 25141 | 09-09 03:05 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish New Imbalance | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.75R |
| 8 | 25144 | 09-09 03:05 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish I-CHOCH+ | -0.04 |  | below_threshold | score -0.04 < 2.0 | trail +0.75R |
| 9 | 25146 | 09-09 03:05 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish OB Created | -0.09 |  | below_threshold | score -0.09 < 2.0 | trail +0.75R |
| 10 | 25154 | 09-09 04:05 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish OB Entered | -0.5 |  | below_threshold | score -0.5 < 2.0 | be +0.00R |
| 11 | 25155 | 09-09 04:05 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish Imbalance Mitigated | 0.79 |  | below_threshold | score 0.79 < 2.0 | be +0.00R |
| 12 | 25156 | 09-09 04:05 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish Liquidity Grab | 2.5 | 14.1 | ai_skipped | advisor skip: FLAT market (ADX 1h/15m <15, ATR% <0.75%), 1d BULL opposes SHORT, stale 1H signal dominates fresh confluence. | be +0.00R |
| 13 | 25157 | 09-09 04:05 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 2.04 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | be +0.00R |
| 14 | 25160 | 09-09 04:10 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish Breaker | 2.5 | 14.2 | ai_skipped | advisor skip: FLAT market (ADX 1h=14.2, 15m=13.2, ATR% low, EMA Flat/Contracting) + 1d BULL opposes SHORT. Weak MTF alignment (1/4). Stale 1h signal.  | be -0.00R |
| 15 | 25163 | 09-09 04:15 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 1.27 |  | below_threshold | score 1.27 < 2.0 | be -0.00R |
| 16 | 25165 | 09-09 04:20 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -8.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.11R |
| 17 | 25166 | 09-09 04:25 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -8.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.12R |
| 18 | 25167 | 09-09 04:45 | Smart Trail Switch Bullish | HyperWave Signal Up | Bearish OB Entered | -8.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.27R |
| 19 | 25169 | 09-09 04:50 | Smart Trail Switch Bullish | HyperWave Signal Up | Bearish Imbalance Mitigated | -7.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.36R |
| 20 | 25170 | 09-09 04:50 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -7.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.36R |
| 21 | 25171 | 09-09 04:55 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -7.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.37R |
| 22 | 25172 | 09-09 05:00 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -7.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.23R |
| 23 | 25173 | 09-09 05:05 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -7.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.27R |
| 24 | 25174 | 09-09 05:10 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -7.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.37R |
| 25 | 25175 | 09-09 05:15 | Smart Trail Switch Bullish | HyperWave Signal Up | Bearish OB Entered | -6.75 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.44R |
| 26 | 25176 | 09-09 05:15 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -6.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.44R |
| 27 | 25178 | 09-09 05:20 | Smart Trail Switch Bullish | HyperWave Signal Up | Bearish Breaker | -8.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.40R |
| 28 | 25179 | 09-09 05:20 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -7.5 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.40R |
| 29 | 25180 | 09-09 05:25 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.31R |
| 30 | 25181 | 09-09 05:30 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.24R |
| 31 | 25184 | 09-09 05:35 | Smart Trail Switch Bullish | Reversal Down | Within Bearish OB | 0.72 |  | below_threshold | score 0.72 < 2.0 | trail +0.15R |
| 32 | 25185 | 09-09 05:40 | Smart Trail Switch Bullish | Reversal Down | Bearish OB Mitigated | 0.22 |  | below_threshold | score 0.22 < 2.0 | trail +0.10R |
| 33 | 25188 | 09-09 06:25 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish OB Entered | 3.47 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | trail +0.41R |
| 34 | 25189 | 09-09 06:25 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 5.0 | 15.2 | ai_skipped | advisor skip: SHORT opposes dominant 1d/4h/1h/15m/5m BULL regime (0/4 MTF align). FLAT market (ADX 1h 15.2, ATR% 0.767%), stale 1h signal (13.4h old). | trail +0.41R |
| 35 | 25190 | 09-09 06:25 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish Liquidity Grab | 6.47 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | trail +0.41R |
| 36 | 25191 | 09-09 06:30 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 6.75 | 15.2 | ai_skipped | advisor skip: SHORT opposes dominant bullish regime (1d ADX 52.1, 4h/1h/15m/5m all BULL). FLAT market (1h ADX 15.2, MTF alignment 0). Stale 1h signal. | trail +0.43R |
| 37 | 25192 | 09-09 06:35 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 6.75 | 15.2 | ai_skipped | advisor skip: 1d/4h BULL regime opposes SHORT; market FLAT (ADX 1h 15.2, MTF align 0); 1h signal STALE 13.6h | trail +0.43R |
| 38 | 25193 | 09-09 06:40 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 6.75 | 15.3 | ai_skipped | advisor skip: 1d/4h BULL regime opposes SHORT; 1h ADX 15.3 + flat regime + ask wall p79 above entry blocks upside | trail +0.41R |
| 39 | 25195 | 09-09 06:45 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | 4.25 | 15.3 | ai_skipped | advisor skip: SHORT opposes 1d/4h/1h/15m BULL regime (MTF 0/4). 1H signal STALE (13.8h). Market FLAT (ADX 15.3/20.9, ATR% low, regime=FLAT, alignment= | trail +0.40R |
| 40 | 25196 | 09-09 06:50 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | 4.25 | 15.3 | ai_skipped | advisor skip: SHORT opposes 1d/4h/1h/15m BULL regime (0/4 MTF alignment). 1H signal stale (13.8h old). Market FLAT (ADX 1h 15.3, low ATR%). Only 5m su | trail +0.36R |
| 41 | 25197 | 09-09 06:55 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | 1.16 |  | below_threshold | score 1.16 < 2.0 | trail +0.37R |
| 42 | 25198 | 09-09 07:05 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | 1.16 |  | below_threshold | score 1.16 < 2.0 | be -0.00R |
| 43 | 25201 | 09-09 07:10 | Smart Trail Switch Bullish | HyperWave Signal Up | Bearish Breaker | -0.59 |  | below_threshold | score -0.59 < 2.0 | trail +0.51R |
| 44 | 25211 | 09-09 07:35 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.45R |
| 45 | 25213 | 09-09 07:40 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.44R |
| 46 | 25214 | 09-09 07:45 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.41R |
| 47 | 25216 | 09-09 07:50 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.36R |
| 48 | 25217 | 09-09 07:55 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.40R |
| 49 | 25220 | 09-09 08:00 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | be -0.00R |
| 50 | 25224 | 09-09 08:05 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | -0.59 |  | below_threshold | score -0.59 < 2.0 | trail +0.48R |
| 51 | 25227 | 09-09 08:10 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | -0.59 |  | below_threshold | score -0.59 < 2.0 | trail +0.43R |
| 52 | 25230 | 09-09 08:15 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 1.11 |  | below_threshold | score 1.11 < 2.0 | be -0.00R |
| 53 | 25231 | 09-09 08:20 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 0.76 |  | below_threshold | score 0.76 < 2.0 | trail +0.49R |
| 54 | 25233 | 09-09 08:25 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 0.76 |  | below_threshold | score 0.76 < 2.0 | be +0.00R |
| 55 | 25240 | 09-09 08:50 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | 3.5 | 16.8 | ai_skipped | advisor skip: SHORT opposes dominant 1d/4h BULL regime (ADX 52.2/14.3). 1H stale, 15m LONG opposes. 5m alone agrees. Flat market (ADX 1h 16.8, ATR% 0. | be -0.00R |
| 56 | 25241 | 09-09 09:05 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | 3.5 | 17.4 | ai_skipped | advisor skip: 1d/4h BULL regime opposes SHORT; 1H/15m BULL; only 5m agrees. Flat market (ADX 1h 17.4, MTF 0). Skip. | trail +0.40R |
| 57 | 25243 | 09-09 09:10 | Smart Trail Switch Bullish | HyperWave Signal Up | Within Bearish OB | 1.02 |  | below_threshold | score 1.02 < 2.0 | trail +0.43R |
| 58 | 25247 | 09-09 09:15 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 1.02 |  | below_threshold | score 1.02 < 2.0 | trail +0.35R |
| 59 | 25250 | 09-09 09:20 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish OB Mitigated | -0.73 |  | below_threshold | score -0.73 < 2.0 | trail +0.31R |
| 60 | 25251 | 09-09 09:25 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish OB Created | -0.62 |  | below_threshold | score -0.62 < 2.0 | trail +0.29R |
| 61 | 25252 | 09-09 09:25 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish I-CHOCH+ | -0.62 |  | below_threshold | score -0.62 < 2.0 | trail +0.29R |
| 62 | 25254 | 09-09 09:50 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 1.75 | 15.6 | ai_skipped | advisor skip: 1D strong BULL (ADX 52.2) opposes SHORT; market FLAT (ADX 1h 15.6, ATR% 0.796%); 1H stale & bullish. Risk asymmetry unfavorable. | be -0.00R |
| 63 | 25255 | 09-09 09:55 | Smart Trail Switch Bullish | HyperWave Signal Down | Within Bearish OB | 1.75 | 15.6 | ai_skipped | advisor skip: 1d BULL (ADX 52.2) vs SHORT opposes regime. 1h ADX 15.6 + FLAT market + contracting 15m EMA. Stale 1h tier weights risk. | be +0.00R |
| 64 | 25256 | 09-09 10:00 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish OB Mitigated | 2.5 | 14.6 | ai_skipped | advisor skip: FLAT regime (1h ADX 14.6, contracting EMA-gap) + 1d BULL opposes SHORT. Stale 1h signal. 5m expand alone insufficient. | trail +0.09R |
| 65 | 25258 | 09-09 10:35 | Smart Trail Switch Bullish | HyperWave Signal Down | Bearish Liquidity Grab | 1.75 | 14.6 | ai_skipped | advisor skip: 1d BULL (ADX 52.2) opposes SHORT; market FLAT (ADX 1h 14.6, ATR% 0.772%); 1h tier STALE (17.6h); bid-heavy book favors long. | trail +0.07R |
| 66 | 25266 | 09-09 11:10 | Any Bearish Confirmation | None | Bearish OB Created | -5.0 |  | htf_blocked | HTF cascade: NEUTRAL/expired tier NEUTRAL-expired (needs SHORT) | be +0.00R |
| 67 | 25267 | 09-09 11:10 | Any Bearish Confirmation | None | Bearish I-BOS | -5.0 |  | htf_blocked | HTF cascade: NEUTRAL/expired tier NEUTRAL-expired (needs SHORT) | be +0.00R |
| 68 | 25269 | 09-09 11:35 | Any Bearish Confirmation | HyperWave Signal Down | Bearish OB Entered | 4.5 | 14.0 | ai_skipped | advisor skip: 1D BULL regime (ADX 52.2) conflicts SHORT. Low 1H/4H ADX + contracting EMA-gaps = flat compression. 15m BEAR alone insufficient. | trail +0.01R |
| 69 | 25270 | 09-09 11:45 | Any Bearish Confirmation | HyperWave Signal Down | Bearish OB Entered | 4.5 | 14.0 | ai_skipped | advisor skip: 1d BULL trend opposes SHORT; 1h/4h NEUTRAL weak ADX (<15); EMA compression across all TFs; flat regime. HTF regime risk outweighs 3-tier | trail +0.16R |
| 70 | 25272 | 09-09 11:50 | Any Bearish Confirmation | HyperWave Signal Up | Bearish Liquidity Grab | 5.0 | 14.0 | ai_skipped | advisor skip: 1d BULL + 4h NEUTRAL oppose SHORT. Flat market (ADX 1h:14, 15m:18 <23; EMA contracting all TF). 15m LONG opposes. Skip. | trail +0.24R |
| 71 | 25273 | 09-09 11:50 | Any Bearish Confirmation | HyperWave Signal Up | Within Bearish OB | 6.02 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | trail +0.24R |
| 72 | 25274 | 09-09 11:55 | Any Bearish Confirmation | HyperWave Signal Up | Bearish Breaker | 5.0 | 13.9 | ai_skipped | advisor skip: 1d/4h BULL regime opposes SHORT; 1h/15m ADX <20 + contracting EMA = flat squeeze; 15m opposes | trail +0.23R |
| 73 | 25280 | 09-09 12:55 | Any Bearish Confirmation | HyperWave Signal Up | Bearish OB Entered | 4.5 | 13.9 | ai_skipped | advisor skip: 1d/4h BULL regime opposes SHORT; 15m HyperWave LONG conflicts; weak ADX/low volatility; skip. | trail +0.43R |
| 74 | 25283 | 09-09 13:45 | Any Bearish Confirmation | Reversal Down | Within Bearish OB | 7.75 | 12.9 | ai_skipped | advisor skip: 1d BULL (ADX 52.2) strongly opposes SHORT; 1h/4h NEUTRAL weak. Flat squeeze: 1h ADX 12.9, EMA Flat. Skip. | trail +0.10R |
| 75 | 25286 | 09-09 13:50 | Any Bearish Confirmation | HyperWave Signal Down | Within Bearish OB | 6.75 | 12.9 | ai_skipped | advisor skip: 1d BULL + weak lower-TF ADX/EMA compression conflict; ask wall x15.8 at p84 blocks SHORT momentum. | trail +0.04R |
| 76 | 25287 | 09-09 13:55 | Any Bearish Confirmation | HyperWave Signal Down | Within Bearish OB | 8.5 | 12.9 | ai_skipped | advisor skip: 1d BULL + 4h NEUTRAL oppose SHORT. Low 1h/15m ADX (12.9/17.7) + contracting 15m EMA = flat compression. Weak confluence despite 3-tier a | trail +0.01R |
| 77 | 25288 | 09-09 14:00 | Any Bearish Confirmation | HyperWave Signal Down | Bearish OB Mitigated | 8.0 | 12.0 | ai_skipped | advisor skip: 1d BULL trend (ADX 52.2) opposes SHORT; 1h/15m ADX weak (~12/18); EMA compression across all TF; ATR% depressed; flat chop regime masks  | be -0.00R |
| 78 | 25293 | 09-09 14:50 | Any Bearish Confirmation | HyperWave Signal Down | Bearish New Imbalance | -5.75 |  | htf_blocked | HTF cascade: NEUTRAL/expired tier NEUTRAL-expired (needs SHORT) | trail +0.77R |
| 79 | 25299 | 09-09 15:10 | Any Bearish Confirmation | HyperWave Signal Down | Bearish OB Created | 4.25 | 12.4 | ai_skipped | advisor skip: 1d BULL (ADX 52.2) conflicts with SHORT; 1h ADX 12.4 + 1h EMA contracting = weak trend. Skip. | trail +0.44R |
| 80 | 25300 | 09-09 15:10 | Any Bearish Confirmation | HyperWave Signal Down | Bearish I-CHOCH+ | 4.48 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | trail +0.44R |
| 81 | 25310 | 09-09 15:25 | Any Bearish Confirmation | HyperWave Signal Down | Bearish S-CHOCH | 4.5 | 13.1 | ai_skipped | advisor skip: 1d BULL (ADX 52.2) opposes SHORT; 1h ADX 13.1 too weak; ask wall x14.3 at p79 blocks short momentum | trail +0.35R |
| 82 | 25321 | 09-09 16:35 | Any Bearish Confirmation | Reversal Up | Bearish Liquidity Grab | -5.0 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | trail +0.56R |
| 83 | 25332 | 09-09 17:15 | Any Bearish Confirmation | Reversal Up | Bearish Liquidity Grab | -10.0 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | trail +0.64R |
| 84 | 25342 | 09-09 19:00 | Any Bearish Confirmation | Reversal Up | Bearish OB Created | 0.2 |  | below_threshold | score 0.2 < 2.0 | trail +0.58R |
| 85 | 25343 | 09-09 19:00 | Any Bearish Confirmation | Reversal Up | Bearish I-CHOCH+ | 0.2 |  | below_threshold | score 0.2 < 2.0 | trail +0.58R |
| 86 | 25357 | 09-09 19:45 | Any Bearish Confirmation | HyperWave Signal Down | Bearish New Imbalance | -8.25 |  | htf_blocked | HTF cascade: NEUTRAL/expired tier NEUTRAL-expired (needs SHORT) | trail +0.42R |
| 87 | 25360 | 09-09 20:00 | Any Bearish Confirmation | HyperWave Signal Down | Bearish New Imbalance | 1.48 |  | below_threshold | score 1.48 < 2.0 | trail +0.07R |
| 88 | 25363 | 09-09 20:10 | Smart Trail Switch Bearish | HyperWave Signal Down | Within Bearish OB | 5.75 | 16.6 | ai_skipped | advisor skip: Bid-heavy wall cluster at $102.25 (x8.0, p51) directly above SHORT entry blocks downside liquidity. | trail +0.11R |
| 89 | 25364 | 09-09 20:25 | Smart Trail Switch Bearish | HyperWave Signal Down | Within Bearish OB | 5.75 | 16.8 | ai_skipped | advisor skip: 1d NEUTRAL w/ high ADX 52.2 + contracting EMA contradicts SHORT. 4h weak ADX 13.0. Flat-market risk. | trail +0.04R |
| 90 | 25365 | 09-09 20:30 | Smart Trail Switch Bearish | HyperWave Signal Down | Within Bearish OB | 5.75 | 16.8 | ai_skipped | advisor skip: 1d NEUTRAL + ADX 52.2 (overbought regime); 4h ADX 13.0 (weak); ask wall at $102.25 p70 x11.7 blocks SHORT immediately above mid. | trail +0.20R |
| 91 | 25368 | 09-09 21:20 | Smart Trail Switch Bearish | HyperWave OS Signal Up | Bearish New Imbalance | -7.75 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | trail +0.18R |
| 92 | 25370 | 09-09 21:45 | Smart Trail Switch Bearish | HyperWave OS Signal Up | Within Bearish OB | -6.0 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | be +0.00R |
| 93 | 25372 | 09-09 21:50 | Smart Trail Switch Bearish | HyperWave OS Signal Up | Bearish OB Created | -6.5 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | trail +0.01R |
| 94 | 25373 | 09-09 21:50 | Smart Trail Switch Bearish | HyperWave OS Signal Up | Bearish S-BOS | -5.25 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | trail +0.01R |
| 95 | 25374 | 09-09 21:50 | Smart Trail Switch Bearish | HyperWave OS Signal Up | Bearish I-BOS | -5.25 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | trail +0.01R |
| 96 | 25375 | 09-09 21:50 | Smart Trail Switch Bearish | HyperWave OS Signal Up | Within Bearish OB | -5.25 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | trail +0.01R |
| 97 | 25376 | 09-09 21:55 | Smart Trail Switch Bearish | HyperWave OS Signal Up | Within Bearish OB | -5.25 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | trail +0.03R |
| 98 | 25377 | 09-09 22:00 | Smart Trail Switch Bearish | HyperWave OS Signal Up | Within Bearish OB | -6.0 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | trail +0.00R |
| 99 | 25398 | 09-09 23:35 | 15m-rearm: HyperWave OS Signal Up | HyperWave OS Signal Up | Within Bearish OB | -6.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.54R |
| 100 | 25399 | 09-09 23:35 | 15m-rearm: HyperWave OS Signal Up | HyperWave OS Signal Up | Bearish Liquidity Grab | -3.5 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.54R |
| 101 | 25400 | 09-09 23:40 | 15m-rearm: HyperWave OS Signal Up | HyperWave OS Signal Up | Bearish Breaker | -5.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.51R |
| 102 | 25408 | 09-10 00:05 | 15m-rearm: HyperWave OS Signal Up | HyperWave OS Signal Up | Within Bearish OB | -6.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.43R |
| 103 | 25409 | 09-10 00:10 | 15m-rearm: HyperWave OS Signal Up | HyperWave OS Signal Up | Within Bearish OB | -6.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.42R |
| 104 | 25410 | 09-10 00:15 | 15m-rearm: HyperWave OS Signal Up | HyperWave OS Signal Up | Within Bearish OB | -6.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.38R |
| 105 | 25411 | 09-10 00:20 | 15m-rearm: HyperWave OS Signal Up | HyperWave OS Signal Up | Within Bearish OB | -6.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.40R |
| 106 | 25412 | 09-10 00:25 | 15m-rearm: HyperWave OS Signal Up | HyperWave OS Signal Up | Bearish OB Mitigated | -6.5 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.38R |
| 107 | 25417 | 09-10 01:10 | 15m-rearm: HyperWave OS Signal Up | HyperWave Signal Down | Bearish Liquidity Grab | 4.0 | 26.8 | ai_skipped | advisor skip: 1H signal opposes SHORT; 4H trend weak (ADX 15.3); ask wall p80 blocks upside; flat 5m/15m compression. | trail +0.38R |
| 108 | 25423 | 09-10 01:40 | 15m-rearm: HyperWave OS Signal Up | HyperWave Signal Up | Bearish OB Created | 2.36 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | trail +0.23R |
| 109 | 25425 | 09-10 01:40 | 15m-rearm: HyperWave OS Signal Up | HyperWave Signal Up | Bearish I-CHOCH | 2.25 | 27.2 | ai_skipped | advisor skip: 1H/15m LuxAlgo LONG signals oppose SHORT entry; 2/3 tier conflict. 4H ADX weak (15.3). Skip. | trail +0.23R |
| 110 | 25433 | 09-10 02:40 | 15m-rearm: HyperWave OS Signal Up | HyperWave Signal Up | Bearish OB Entered | 2.0 | 29.3 | ai_skipped | advisor skip: 2/3 LuxAlgo tiers oppose SHORT (1h/15m LONG signals). Market regime FLAT, weak MTF alignment (2/4). Ask wall p91×18.1 blocks short above | trail +0.49R |
| 111 | 25435 | 09-10 02:45 | 15m-rearm: HyperWave OS Signal Up | HyperWave Signal Up | Within Bearish OB | 2.5 | 29.3 | ai_skipped | advisor skip: 1H/15m LONG signals oppose SHORT entry; 15m EMA contracting, 5m BULL bias, MTF alignment weak (2/4). Flat regime. | trail +0.54R |
| 112 | 25436 | 09-10 02:50 | 15m-rearm: HyperWave OS Signal Up | HyperWave Signal Up | Within Bearish OB | 1.75 | 29.3 | ai_skipped | advisor skip: Multi-TF signal opposition (1H/15m LONG vs 5m SHORT); market regime FLAT with weak MTF alignment (2/4); 1H ADX 29.3 + contracting 15m EM | trail +0.59R |
| 113 | 25440 | 09-10 02:55 | 15m-rearm: HyperWave OS Signal Up | HyperWave Signal Up | Bearish Breaker | 0.13 |  | below_threshold | score 0.13 < 2.0 | trail +0.59R |
| 114 | 25442 | 09-10 03:05 | 15m-rearm: HyperWave OS Signal Up | HyperWave Signal Up | Bearish Imbalance Mitigated | 0.13 |  | below_threshold | score 0.13 < 2.0 | trail +0.63R |
| 115 | 25446 | 09-10 04:25 | 15m-rearm: HyperWave OS Signal Up | Reversal Down | Bearish Liquidity Grab | 1.29 |  | below_threshold | score 1.29 < 2.0 | trail +0.74R |
| 116 | 25453 | 09-10 05:10 | Any Bullish Confirmation | Reversal Down | Within Bearish OB | -8.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.84R |
| 117 | 25468 | 09-10 06:15 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.59R |
| 118 | 25470 | 09-10 06:15 | Any Bullish Confirmation | HyperWave Signal Down | Bearish I-CHOCH+ | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.59R |
| 119 | 25471 | 09-10 06:15 | Any Bullish Confirmation | HyperWave Signal Down | Bearish OB Created | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.59R |
| 120 | 25473 | 09-10 06:20 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.60R |
| 121 | 25474 | 09-10 06:25 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.66R |
| 122 | 25475 | 09-10 06:30 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.64R |
| 123 | 25476 | 09-10 06:35 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.69R |
| 124 | 25477 | 09-10 06:40 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -8.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.69R |
| 125 | 25480 | 09-10 06:45 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.83R |
| 126 | 25481 | 09-10 06:50 | Any Bullish Confirmation | HyperWave Signal Down | Bearish OB Entered | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.79R |
| 127 | 25483 | 09-10 06:55 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.78R |
| 128 | 25484 | 09-10 07:05 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -8.25 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.66R |
| 129 | 25486 | 09-10 07:10 | Any Bullish Confirmation | HyperWave Signal Down | Bearish New Imbalance | -7.5 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.65R |
| 130 | 25487 | 09-10 07:10 | Any Bullish Confirmation | HyperWave Signal Down | Within Bearish OB | -5.75 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.65R |
| 131 | 25489 | 09-10 07:15 | Any Bullish Confirmation | HyperWave Signal Up | Within Bearish OB | -5.75 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.65R |
| 132 | 25490 | 09-10 07:20 | Any Bullish Confirmation | HyperWave Signal Up | Within Bearish OB | -5.75 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.49R |
| 133 | 25493 | 09-10 07:25 | Any Bullish Confirmation | HyperWave Signal Up | Bearish OB Mitigated | -8.75 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.41R |
| 134 | 25494 | 09-10 07:30 | Any Bullish Confirmation | HyperWave Signal Up | Bearish OB Created | -8.75 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.33R |
| 135 | 25495 | 09-10 07:30 | Any Bullish Confirmation | HyperWave Signal Up | Bearish New Imbalance | -8.75 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.33R |
| 136 | 25496 | 09-10 07:30 | Any Bullish Confirmation | HyperWave Signal Up | Bearish I-BOS | -7.5 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.33R |
| 137 | 25503 | 09-10 09:40 | Any Bullish Confirmation | Reversal Up | Bearish OB Created | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.40R |
| 138 | 25504 | 09-10 09:40 | Any Bullish Confirmation | Reversal Up | Bearish I-BOS | -10.0 |  | htf_blocked | HTF cascade: 1H tier OPPOSES (needs SHORT) | trail +0.40R |
| 139 | 25509 | 09-10 10:05 | Any Bearish Confirmation | None | Bearish OB Entered | 2.0 | 39.1 | ai_skipped | advisor skip: Market regime FLAT + 1h ADX 39 conflicts with 15m ADX 24.4 & EMA-gap Flat. 5m NEUTRAL opposes SHORT. Ask wall x11.9 at p70 blocks entry  | trail +0.45R |
| 140 | 25510 | 09-10 10:25 | Any Bearish Confirmation | None | Bearish OB Entered | 2.0 | 39.1 | ai_skipped | advisor skip: Massive ask wall (p86, x16.3) at $101.25 blocks SHORT momentum; flat 5m (ADX 13.5) undermines trigger despite 1h/4h bearish alignment. | trail +0.48R |
| 141 | 25513 | 09-10 10:45 | Any Bearish Confirmation | HyperWave Signal Up | Bearish OB Entered | 4.75 | 39.1 | ai_skipped | advisor skip: 15m LONG opposes SHORT; 5m ADX 12.1 (weak); market FLAT regime; 15m contracting EMA-gap; bid walls p64/p52 above entry absorb SHORT move | trail +0.55R |
| 142 | 25514 | 09-10 10:45 | Any Bearish Confirmation | HyperWave Signal Up | Within Bearish OB | 4.09 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | trail +0.55R |
| 143 | 25515 | 09-10 10:50 | Any Bearish Confirmation | HyperWave Signal Up | Within Bearish OB | 4.75 | 39.1 | ai_skipped | advisor skip: 15m HyperWave opposes SHORT; market FLAT (ADX 1h 39 but EMA-gap compressed, MTF align 2/4). Bid wall x10.3@100.75 blocks downside. | trail +0.46R |
| 144 | 25518 | 09-10 11:20 | Any Bearish Confirmation | HyperWave Signal Up | Bearish OB Entered | 4.5 | 40.4 | ai_skipped | advisor skip: 15m HyperWave opposes SHORT; 15m ADX weak (24.1); EMA compression on 1h/15m; ask wall at $101.25 (p64, x10.6) blocks downside move immed | trail +0.62R |
| 145 | 25520 | 09-10 11:25 | Any Bearish Confirmation | HyperWave Signal Up | Within Bearish OB | 5.0 | 40.4 | ai_skipped | advisor skip: 15m HyperWave LONG opposes SHORT; 5m BULL trend contradicts; massive ask wall at $101.75 (p69, x11.5) blocks short momentum. | trail +0.63R |
| 146 | 25522 | 09-10 11:30 | Any Bearish Confirmation | HyperWave Signal Down | Within Bearish OB | 4.25 | 40.4 | ai_skipped | advisor skip: 5m BULL trend + massive ask wall ($101.75, p82, x15.1) above entry blocks SHORT momentum development. | trail +0.67R |
| 147 | 25524 | 09-10 11:35 | Any Bearish Confirmation | HyperWave Signal Down | Bearish Breaker | 1.89 |  | below_threshold | score 1.89 < 2.0 | trail +0.70R |
| 148 | 25527 | 09-10 11:50 | Any Bearish Confirmation | HyperWave Signal Up | Within Bearish OB | 4.25 | 40.0 | ai_skipped | advisor skip: 15m LONG opposes 1H/5m SHORT; 15m HyperWave fresh (5m old); 4H ADX weak (16.8); EMA-gap contracting across 15m/5m/1d; ask wall x11.6 at  | trail +0.51R |
| 149 | 25528 | 09-10 11:55 | Any Bearish Confirmation | HyperWave Signal Up | Bearish OB Mitigated | 3.75 | 40.0 | ai_skipped | advisor skip: 15m LONG opposes 1H/5m SHORT; 1d NEUTRAL + weak 4h ADX(16.8) undermine bearish regime; flat 15m EMA compression | trail +0.45R |
| 150 | 25538 | 09-10 12:40 | Any Bearish Confirmation | HyperWave Signal Down | Bearish New Imbalance | 2.21 |  | below_threshold | score 2.21 < 2.0 | be +0.00R |
| 151 | 25539 | 09-10 12:40 | Any Bearish Confirmation | HyperWave Signal Down | Bearish OB Created | 2.21 |  | below_threshold | score 2.21 < 2.0 | be +0.00R |
| 152 | 25540 | 09-10 12:40 | Any Bearish Confirmation | HyperWave Signal Down | Bearish I-CHOCH | 2.21 |  | below_threshold | score 2.21 < 2.0 | be +0.00R |
| 153 | 25543 | 09-10 12:40 | Any Bearish Confirmation | HyperWave Signal Down | Bearish S-BOS | 2.21 |  | below_threshold | score 2.21 < 2.0 | be +0.00R |
| 154 | 25565 | 09-10 15:25 | Trend Tracer Down | HyperWave OS Signal Up | Bearish I-BOS | 3.97 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | open@last +0.02R |
| 155 | 25566 | 09-10 15:25 | Trend Tracer Down | HyperWave OS Signal Up | Bearish OB Created | 5.0 | 46.0 | ai_skipped | advisor skip: 15m HyperWave opposes SHORT; 15m EMA contracting + 5m volume weak (0.38x); bid wall at $99.75 (p54, x8.6) blocks SHORT momentum. | open@last +0.02R |
| 156 | 25567 | 09-10 15:40 | Trend Tracer Down | HyperWave OS Signal Up | Bearish OB Entered | 4.5 | 46.0 | ai_skipped | advisor skip: 15m HyperWave opposes SHORT; massive ask wall at $99.75 (p64) blocks upside recovery if SHORT fails. | open@last +0.03R |
| 157 | 25588 | 09-10 19:30 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Bearish OB Entered | 4.25 | 47.0 | ai_skipped | advisor skip: 15m opposes SHORT; 1d NEUTRAL + weak MTF alignment (2/4); EMA-gaps contracting on 1h/15m signal compression, not expansion. | open@last +0.08R |
| 158 | 25589 | 09-10 19:45 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Bearish Imbalance Mitigated | 1.91 |  | below_threshold | score 1.91 < 2.0 | open@last +0.08R |
| 159 | 25590 | 09-10 19:45 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Bearish OB Entered | 4.25 | 46.9 | ai_skipped | advisor skip: 15m opposes SHORT; 1d NEUTRAL + 4h weak (ADX 20.9); EMA gaps contracting on 1h/15m; MTF alignment weak (2/4) | open@last +0.08R |
| 160 | 25591 | 09-10 20:15 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Bearish OB Entered | -6.75 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | open@last +0.23R |
| 161 | 25592 | 09-10 20:20 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Within Bearish OB | -8.25 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | open@last +0.18R |
| 162 | 25593 | 09-10 20:25 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Bearish Liquidity Grab | -5.75 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | open@last +0.24R |
| 163 | 25594 | 09-10 20:35 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Within Bearish OB | -5.75 |  | htf_blocked | HTF cascade: 15m tier OPPOSES (needs SHORT) | open@last +0.20R |
| 164 | 25596 | 09-10 20:45 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Bearish OB Entered | 4.5 | 46.7 | ai_skipped | advisor skip: FLAT market (1h ADX 46.7 vs regime FLAT, EMA contracting); 15m BULL opposes SHORT; weak MTF alignment (1/4). Skip. | open@last +0.19R |
| 165 | 25597 | 09-10 20:55 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Within Bearish OB | 4.0 | 46.7 | ai_skipped | advisor skip: FLAT regime (1h ADX 46.7 outlier; 15m ADX 19.7 weak; EMA-gap contracting 1h). 15m BULL opposes SHORT. Weak MTF alignment (1/4). Skip. | open@last +0.21R |
| 166 | 25598 | 09-10 21:00 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Within Bearish OB | 4.0 | 46.7 | ai_skipped | advisor skip: FLAT market (1h ADX 46.7 BUT regime=FLAT, MTF=1), 15m BULL opposes SHORT, ask-wall p80 x14.4 blocks SHORT momentum | open@last +0.20R |
| 167 | 25599 | 09-10 21:10 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Within Bearish OB | 4.0 | 46.5 | ai_skipped | advisor skip: 15m BULL opposes SHORT; 1h ADX 46.5 strong but market_regime FLAT; MTF alignment 1/4 weak; ask wall at $100.25 (p68, x11.4) blocks upsid | open@last +0.19R |
| 168 | 25600 | 09-10 21:15 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Up | Within Bearish OB | 1.75 | 46.5 | ai_skipped | advisor skip: 15m HyperWave opposes SHORT; 1h EMA contracting + FLAT regime + weak MTF alignment (2/4) + ask wall p69 blocks upside recovery. Inconclu | open@last +0.17R |
| 169 | 25605 | 09-10 21:45 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Bearish OB Created | 3.0 | 46.5 | ai_skipped | advisor skip: FLAT market regime + EMA compression across 1h/15m/5m conflicts strong LuxAlgo confluence. MTF alignment weak (3/4). Skip until volatili | open@last +0.16R |
| 170 | 25606 | 09-10 21:45 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Bearish I-BOS | 4.43 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | open@last +0.16R |
| 171 | 25607 | 09-10 21:50 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Bearish OB Entered | 4.25 | 46.5 | ai_skipped | advisor skip: FLAT market (ADX 1h 46.5 outlier; 15m ADX 17.8 weak; EMA contracting; regime FLAT, MTF=2). 4h BEAR weak (ADX 22.7). Ask wall $100.25 (p6 | open@last +0.12R |
| 172 | 25608 | 09-10 22:10 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Bearish OB Entered | 3.75 | 46.4 | ai_skipped | advisor skip: FLAT regime (ADX 1h 46.4 masks 15m 18.2 weak; EMA gap contracting both TF); 5m BULL vs SHORT; ask wall p75 x13.2 at $100.25 blocks move. | open@last +0.18R |
| 173 | 25610 | 09-10 22:20 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Within Bearish OB | 3.5 | 46.4 | ai_skipped | advisor skip: FLAT-MARKET GUARD triggered: 1h ADX 46.4 strong, but 15m ADX 17.0 weak + EMA-gap Contracting (1h 0.552%, 15m 0.024%) + market_regime FLA | open@last +0.20R |
| 174 | 25611 | 09-10 22:25 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Within Bearish OB | 3.5 | 46.4 | ai_skipped | advisor skip: FLAT regime (1h ADX 46.4 outlier; 15m ADX 17.0 weak, EMA compressed 0.017%). MTF trend: 4h BEAR only; 1d/1h/15m/5m NEUTRAL. Strong bid w | open@last +0.12R |
| 175 | 25612 | 09-10 22:35 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Bearish OB Created | 3.0 | 46.6 | ai_skipped | advisor skip: 1h EMA contracting + market_regime FLAT + 1h ADX 46.6 vs 15m ADX 17.8 divergence signals chop risk despite 3-way agreement. | open@last -0.06R |
| 176 | 25613 | 09-10 22:35 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Bearish New Imbalance | 3.53 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | open@last -0.06R |
| 177 | 25614 | 09-10 22:35 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Bearish I-BOS | 4.78 |  | entry_gate_refused | concurrent SHORT entry already in flight — refused, not queued | open@last -0.06R |
| 178 | 25615 | 09-10 22:40 | 15m-rearm: HyperWave Signal Down | HyperWave Signal Down | Bearish New Imbalance | 1.48 |  | below_threshold | score 1.48 < 2.0 | open@last -0.09R |