# Mercury-SOL — the advisor did not start refusing: its own verdict has passed under 1 % for three months, the "passes" that vanished were a second-opinion override killed on 08-14 for losing money, and the refusals it makes lose money

_2026-09-11 04:25 UTC_

---

**2026-09-11 04:25 UTC · READ-ONLY · Mercury-SOL (LIVE, `is_paper=0`) · basis: report 2026-09-10-2310 §4d (SHORT 0/229, LONG 1/189 over 7 days; 5/509 and 5/507 over 30 days)**

## The answer, decision-shaped

1. **The refusals are net POSITIVE to the book.** Every refusal of the last 30 days, replayed on real Bybit 5m candles under the live geometry, serial with one position per side: **62 trades, −7.11R, −$5.98**. SHORT refusals **−14.11R on 35**; LONG refusals **+7.00R on 27**. Over the whole record the serial refused book is **−24.67R on 207**. The ten executes of the same 30 days, replayed identically, are **+6.11R** (live actual **+7.13R**). The advisor separates in the right direction.
2. **The advisor's own verdict never fell.** On its default system prompt — the only prompt in use since 2026-08-10 — it executed **29 of 4,347 consultations over the whole record (0.67 %)**: **0.55 % before 08-10, 1.01 % since.** Tested at five split dates with the setup mix held constant, the default verdict shows **no drop at any of them** (P 0.29–1.00).
3. **What vanished is a different mechanism.** **68 of the 97 executes ever recorded did not come from the default verdict:** 42 came from the *aligned wall relaxations* — a second model call that overturned the advisor's own SKIP into EXECUTE on trend-aligned setups — and 26 from a late-June main prompt (06-20 → 06-26) that carried a trend-aligned-LONG wall exception. The relaxations were **switched off on 2026-08-14** (`ADVISOR_WALL_ALIGNED_RELAXATIONS = False`) because their 12 positions made **−4.40R** and the last four all lost; the late-June prompt's 7 positions made **−1.68R**. The default verdict's own 18 positions made **+8.57R**. The "pass rate" that looked like it collapsed was mostly an override that lost money and was removed on evidence.
4. **Why the default verdict is so rare: the MIX it is offered.** It passes **1 of 2,833 consultations (0.04 %)** where any of the OHLCV 1h / 4h / 1d trends points against the side, and 28 of 1,574 (1.8 %) where none does. Since 2026-08-10 the daily trend has **never read BEAR** on any consultation (BULL 880, NEUTRAL 218), so no short had the daily with it, and **not one SHORT consultation in the last 30 days had 1h, 4h and 1d all BEAR**. Refusing the opposed setups is right: whole-record serial **mean −0.201R, 95 % CI [−0.348, −0.053], n 157**.
5. **So the finding is upstream — the FUNNEL.** Two-thirds of what reaches the advisor has a higher timeframe against it; the advisor refuses it; it loses.
6. **One place the refusals may be wrong — not established:** LONG with 1h/4h/1d all BULL. 30 days: serial **+7.01R on 11** (mean +0.64R, CI [−0.40, +1.68]); whole record serial +4.10R on 19 (CI includes 0). The five LONG executes of the same 30 days were all in this group and made +11.53R actual.
7. **Watch, do not act:** since the 2026-09-03 19:45 restart the default verdict has executed **0 of 20** clean episodes (no HTF opposition, 1h ADX ≥ 20) against 10.2 % before — **P = 0.13, not established**. At that restart the entry prompt started printing each tier signal's age as a share of its window with the word `STALE`, and "stale signal" became a top cited ground (54–58 % of last week's refusals, 0–3 % in June/July). Those 20 clean refusals replay **−2.22R serial on 8** — refusing them saved money so far.

**Nothing was proposed and nothing was applied.** The decision and the n it needs are in §5.

---

## 1. The trend, not the snapshot

### 1a/1c/1d. Per week, full record

Consultation = an `open_long`/`open_short` row with `ai_decision ∈ {execute, skip}` (the population of the 2310 baseline). Episode = consecutive same-side consultations ≤ 60 min apart — the same setup re-offered on each 5m bar. The "of the executes" column splits each week's executes by which system prompt produced the final verdict.

| week (Mon) | LONG exec/cons | SHORT exec/cons | pass L | pass S | of the executes: default verdict / relaxation flip / late-June prompt | cons/day | episodes L / S | episodes with an execute L / S | entries | ΣR | Σ$ | book |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-06-08 | 2/184 | 0/132 | 1.1% | 0.0% | 2 / 0 / 0 | 45.1 | 26 / 24 | 1 / 0 | 1 | +2.09 | +494.20 | paper |
| 2026-06-15 | 3/126 | 0/97 | 2.4% | 0.0% | 0 / 0 / 3 | 31.9 | 18 / 17 | 2 / 0 | 2 | -1.00 | -236.05 | paper |
| 2026-06-22 | 1/80 | 22/108 | 1.2% | 20.4% | 0 / 0 / 23 | 26.9 | 16 / 18 | 1 / 9 | 5 | -0.68 | -256.42 | paper |
| 2026-06-29 | 0/152 | 0/303 | 0.0% | 0.0% | 0 / 0 / 0 | 65.0 | 34 / 43 | 0 / 0 | 0 | +0.00 | +0.00 | — |
| 2026-07-06 | 2/232 | 4/264 | 0.9% | 1.5% | 4 / 2 / 0 | 70.9 | 30 / 35 | 1 / 2 | 2 | -1.01 | -159.88 | paper |
| 2026-07-13 | 11/207 | 15/288 | 5.3% | 5.2% | 2 / 24 / 0 | 70.7 | 33 / 37 | 4 / 4 | 5 | -1.45 | -321.40 | paper |
| 2026-07-20 | 5/239 | 0/221 | 2.1% | 0.0% | 1 / 4 / 0 | 65.7 | 32 / 33 | 3 / 0 | 1 | -1.06 | -203.42 | paper |
| 2026-07-27 | 1/185 | 4/242 | 0.5% | 1.7% | 2 / 3 / 0 | 61.0 | 29 / 35 | 1 / 3 | 4 | -1.46 | -339.42 | paper |
| 2026-08-03 | 6/149 | 8/252 | 4.0% | 3.2% | 6 / 8 / 0 | 57.3 | 32 / 35 | 3 / 4 | 4 | +1.30 | -103.59 | paper |
| 2026-08-10 | 2/155 | 5/98 | 1.3% | 5.1% | 6 / 1 / 0 | 36.1 | 29 / 28 | 2 / 5 | 7 | -4.71 | -5.27 | live |
| 2026-08-17 | 3/44 | 0/111 | 6.8% | 0.0% | 3 / 0 / 0 | 22.1 | 18 / 28 | 3 / 0 | 3 | +8.18 | +16.31 | live |
| 2026-08-24 | 1/84 | 0/94 | 1.2% | 0.0% | 1 / 0 / 0 | 25.4 | 20 / 17 | 1 / 0 | 1 | +1.63 | +4.88 | live |
| 2026-08-31 | 1/128 | 1/118 | 0.8% | 0.8% | 2 / 0 / 0 | 35.1 | 30 / 20 | 1 / 1 | 2 | +0.64 | -0.67 | live |
| 2026-09-07 | 0/136 | 0/131 | 0.0% | 0.0% | 0 / 0 / 0 | 38.1 | 19 / 26 | 0 / 0 | 0 | +0.00 | +0.00 | — |

Σ$ is at the book's own notional: paper weeks $10,000, live weeks (from 2026-08-08) $100. The week of 09-07 is partial (to 2026-09-11 03:51). **The bot's last entry is vpos 43, opened 2026-09-05 13:05; none since.** Live book since 08-08: 15 entries, **+7.86R** actual.

**1c — fewer opportunities, and a worse mix of them.** Webhook arrivals are steady at ~1,400–1,700 a week. Consultations fell from **61–71 a day in July to 22–38 a day since 2026-08-17** because more gates now stand in front of the advisor: `entry_gate_refused` (from 08-03, ~100/week), `book_blocked` (armed 08-10), `flat_adx_blocked` (armed 08-17 14:55 → dryrun 09-03 19:30; 372 rows), and — from the live flip on 08-08 — no consultation happens while a live position is open on that side. The paper era consulted anyway and logged **56 `observed_skipped` executes** (the last on 08-07), repeats of setups already held. The bot is offered fewer setups, and a larger share of them have a higher timeframe against them (§3b). It is **not** refusing more of the same.

### 1b. Is there a step? Tested, with the mix held constant

Each test compares the post-split count with what the pre-split pass rate *per alignment cell* (number of 1h/4h/1d trends aligned × opposed) predicts for the post-split mix. "Default" = the advisor's own verdict (a relaxation flip counts as the SKIP the default prompt gave); "final" = the decision that stood. Unit = episode; the 06-20 → 06-26 prompt era is excluded from both.

| split tested | default: before → after (expected) | P | final: before → after (expected) | P |
|---|---|---|---|---|
| 2026-08-08 live flip | 7/480 → 15/253 (3.1) | 1.00 | 23/480 → 16/253 (10.6) | 0.96 |
| 2026-08-10 18:30 book gate armed | 11/504 → 11/229 (4.2) | 1.00 | 28/504 → 11/229 (11.7) | 0.50 |
| **2026-08-14 relaxations killed** | 14/539 → 8/194 (4.5) | 0.96 | 31/539 → 8/194 (10.9) | 0.24 |
| 2026-08-17 14:55 flat-ADX gate armed | 16/560 → 6/173 (4.2) | 0.87 | 33/560 → 6/173 (9.8) | 0.15 |
| 2026-09-03 19:30 dryrun + age-window prompt | 21/657 → 1/76 (2.5) | 0.29 | 38/657 → 1/76 (4.3) | 0.07 |
| 2026-09-03, clean sub-population only (no HTF opposition, 1h ADX ≥ 20) | 19/187 → 0/20 (2.0) | 0.13 | 28/187 → 0/20 (3.0) | 0.05 |

**Reading.** On the advisor's own verdict there is no step anywhere; after most splits it passes *more* than the mix predicts. The final pass rate dips because the relaxations — which only ever turned the advisor's SKIP into EXECUTE — stopped on 08-14 by decision. Three weeks (06-22, 07-13, 08-03) hold 63 of the 97 executes, and 55 of those 63 came from the relaxation override or the late-June prompt, not from the default verdict. At the consultation level the drop looks dramatic (2.45 % → 0.71 %), but that level counts every 5m re-offer of one setup and the paper repeats, so it is not used for the verdict.

What changed on or before each split, from the canon, config comments and `.bak` files (the SOL tree is not under git): 08-08 live flip; 08-10 18:24 book gate armed; **08-14 `ADVISOR_WALL_ALIGNED_RELAXATIONS = False`** (ledger in `config.py`: 41 flips, 12 positions, ΣR −4.403, last 4 all losers, the extra call was 19.8 % of all model calls); 08-17 flat-ADX gate armed; 09-03 19:30 flat-ADX gate to dryrun and the tier-age window in the entry prompt, service restarted 19:45:14. `journalctl` retains only the 2026-09-10 23:04 restart; earlier restarts are dated from the reports.

---

## 2. What the advisor is citing now

### 2a/2b-agent. Hand-read classification and claim check by independent agents — PARTIAL

Twelve agents were to read all 418 consultations of the 7-day window, one row at a time, against each row's own prompt, and skeptic agents were then to re-check every flag. **At publication 2 of the 8 reading agents had finished (106 of 418 rows, 2026-09-04 → 09-05). The skeptic pass and the three comparison-week agents had not.** The figures below are that partial sample, and they are labelled as such. The mechanical checks in 2b-mech and 2c-mech cover **every** row and carry the conclusions.

```
§2a primary cluster × side (refusals):
side                           LONG  SHORT
primary_cluster                           
htf_trend_opposes                11     71
stale_signal                      5      1
flat_regime_label                 9      0
intraday_trend_mtf_misaligned     3      0
opposing_wall_orderbook           1      0
tier_signal_conflict              3      0
weak_trend_strength               2      0

§2a any-mention × side:
                               LONG  SHORT
flat_regime_label                30     63
generic_weak_confluence_rr        6     12
htf_trend_opposes                20     72
intraday_trend_mtf_misaligned     9     14
low_volume                        2      1
opposing_wall_orderbook          26     30
stale_signal                     18     47
tier_signal_conflict              7     17
weak_trend_strength               5     18

§2b agent claims: checkable 789 supported 708 contradicted 80 absent 1 ; rows with ≥1 flag 67 of 106
verdict       claim_type 
absent        adx             1
contradicted  adx            63
              book_wall       3
              other           5
              regime_flat     1
              trend_label     8
```

In the sample the agents call 80 of 789 checkable claims (10 %) contradicted. **63 of the 80 are one kind:** the reason calls the market flat or weak while the same prompt shows 1h ADX > 25, as in `flat market (ADX 34.8 offset by Contracting EMA-gap)`. Only one claim is absent from the prompt. The mechanical check below measures the same error over all rows: 45 % of refusals, with the prompt printing `Market regime: FLAT` in 187 of 189.

### 2c-mech. What it stopped citing and started citing — fixed regexes over every refusal reason, four windows

Share of REFUSALS whose reason matches each ground (a reason can match several). The three comparison weeks are the highest-pass weeks of the record; §3a shows their passes were mostly the removed override, so this compares the *refusal language*, not the passes.

| ground | 7 days L | 7 days S | wk 08-03 L | wk 08-03 S | wk 07-13 L | wk 07-13 S | wk 06-22 L | wk 06-22 S |
|---|---|---|---|---|---|---|---|---|
| **refusals (n)** | 188 | 229 | 143 | 244 | 196 | 273 | 79 | 86 |
| flat/regime FLAT | 66 % | 61 % | 56 % | 79 % | 60 % | 53 % | 25 % | 50 % |
| HTF trend opposes (1d/4h/1h/regime) | 55 % | 78 % | 44 % | 64 % | 45 % | 44 % | 59 % | 56 % |
| 1d cited | 28 % | 88 % | 64 % | 12 % | 41 % | 47 % | 62 % | 50 % |
| wall/book | 79 % | 44 % | 75 % | 75 % | 94 % | 96 % | 99 % | 99 % |
| ADX weak/low | 12 % | 12 % | 8 % | 5 % | 17 % | 13 % | 9 % | 7 % |
| MTF alignment low | 33 % | 26 % | 28 % | 23 % | 55 % | 45 % | 56 % | 58 % |
| stale/aged signal | 58 % | 54 % | 22 % | 29 % | 0 % | 0 % | 1 % | 3 % |
| tier conflict/disagree | 24 % | 24 % | 27 % | 33 % | 17 % | 38 % | 14 % | 30 % |
| EMA contracting/compression | 53 % | 56 % | 54 % | 34 % | 38 % | 35 % | 42 % | 21 % |
| volume low | 5 % | 3 % | 2 % | 2 % | 6 % | 7 % | 15 % | 5 % |

**Stopped citing:** walls and the book — 94–99 % of refusals in June/July, 75 % in the week of 08-03, **79 % LONG / 44 % SHORT now**. The book gate (armed 08-10) now refuses opposing-wall setups *before* the advisor sees them. Low MTF alignment also fell, from 45–58 % to 26–33 %.
**Started citing:** a **stale 1H signal — 0–3 % in June/July, 22–29 % in the week of 08-03 (the `STALE` marker arrived 08-05), 54–58 % now** (the age window arrived 09-03). **The 1d trend for shorts — 88 % of short refusals now**, against 12 % in the week of 08-03, when the daily read BEAR. EMA compression rose to 53–56 %.
**Unchanged:** "FLAT regime" at 53–79 % in every window. The word was in every prompt until 2026-09-10 23:04.

### 2a-mech. Ten verbatim refusals from the pre-registered 7 days (the median-length reason in each ground × side; ids are `trades.id`)

- **SHORT · 1d BULL opposes** (matches 191) — #24496 2026-09-06 23:15:08 conf 0.92 ADX1h 34.1 1h/4h/1d neutral/bull/bull: "1d/4h BULL regime contradicts SHORT; 15m opposes; 1h stale (7.3h old). Flat market (ADX 14.3@15m, EMA contracting). Weak confluence."
- **SHORT · stale 1H** (matches 122) — #24691 2026-09-07 12:40:03 conf 0.92 ADX1h 18.0 1h/4h/1d neutral/neutral/bull: "1d BULL regime opposes SHORT; 1H signal STALE (20.7h); 15m LONG vs SHORT conflict; flat market (ADX 18/10.8, EMA contracting); 0/4 MTF alignment."
- **SHORT · flat/regime** (matches 198) — #25513 2026-09-10 10:45:12 conf 0.78 ADX1h 39.1 1h/4h/1d bear/bear/neutral: "15m LONG opposes SHORT; 5m ADX 12.1 (weak); market FLAT regime; 15m contracting EMA-gap; bid walls p64/p52 above entry absorb SHORT move."
- **SHORT · EMA compression** (matches 121) — #24804 2026-09-08 01:10:04 conf 0.92 ADX1h 17.1 1h/4h/1d neutral/neutral/bull: "1d BULL regime + 15m LONG signal oppose SHORT. 1h signal STALE (9.2h). Flat market (ADX 17.1/14.9, EMA contracting). Weak tier agreement."
- **SHORT · wall** (matches 94) — #24631 2026-09-07 07:45:01 conf 0.78 ADX1h 25.1 1h/4h/1d bear/neutral/bull: "1d BULL regime (ADX 52.3) opposes SHORT; 1h stale (15.8h old); flat market (1h ADX 25.1 marginal, ATR% 0.966% weak); ask wall p77 x13.6 blocks SHORT move upside escape."
- **LONG · HTF BEAR opposes** (matches 109) — #25006 2026-09-08 14:55:05 conf 0.82 ADX1h 26.4 1h/4h/1d neutral/bear/bull: "1H bearish opposes entry; 4H weak (ADX 16.8); massive ask wall p66×10.9 blocks upside; FLAT regime with contracting EMA-gaps."
- **LONG · stale 1H** (matches 108) — #24677 2026-09-07 12:05:04 conf 0.92 ADX1h 17.7 1h/4h/1d neutral/neutral/bull: "Flat market (ADX 1h/15m <20, EMA contracting all TFs), 1d bullish but 4h/1h neutral. 15m opposes LONG (fresh). Stale 1H; only 5m agrees. Weak confluence in compression regime."
- **LONG · flat/regime** (matches 152) — #23840 2026-09-04 15:00:10 conf 0.78 ADX1h 30.8 1h/4h/1d bear/neutral/neutral: "1H bearish stale but lower-TF confluence opposes higher-TF regime. 1d/4h/1h/15m all BEAR; MTF=0. FLAT market (regime + MTF align score 0) despite ADX>30. Skip."
- **LONG · wall** (matches 146) — #25098 2026-09-09 00:10:06 conf 0.78 ADX1h 18.0 1h/4h/1d neutral/neutral/bull: "FLAT market (ADX 1h=18, 15m=11.8, EMA contracting). 1H signal STALE (7.2h old). Ask wall x12.7 at p73 blocks upside. Weak MTF alignment (2/4). Skip."
- **LONG · tier opposes** (matches 123) — #24769 2026-09-07 22:20:02 conf 0.92 ADX1h 15.9 1h/4h/1d bear/neutral/bull: "FLAT regime (ADX 15.9/15.2, ATR% 0.77%/0.31%), 1H stale, 15m opposes, massive ask wall at $103.75 (p72, x12.3) blocks LONG momentum."

### 2b-mech. Mechanical claim check — every trend label, ADX number and 1H-signal age stated in a refusal, against that row's own stored prompt

Parsed with fixed regexes; no model involved. Tolerance: ADX ±0.3 (or integer truncation), age ±0.25 h (or whole hours).

| window | trend-label claims | contradicted | ADX-number claims | contradicted | 1H-age claims | contradicted / absent |
|---|---|---|---|---|---|---|
| pre-registered 7 days (09-03 → 09-10) | 685 | **36 (5.3 %)** | 217 | **0** | 111 | **0 / 0** |
| week of 07-13 (pass ~5 %) | 821 | 18 (2.2 %) | 144 | 1 | — (prompt carried no ages) | — |
| week of 08-03 (pass ~3.5 %) | 472 | 31 (6.6 %) | 251 | 0 | 17 | 0 / 0 |

The 36 label errors are almost all one kind: a **NEUTRAL 4h stated as BEAR (11) or BULL (9)**; the rest are NEUTRAL↔BEAR on 15m/5m/1h. The same error dominated the week of 08-03 (27 of 31). **No fabricated timestamps: all 111 "1H signal Nh old" claims match the prompt** — because since 2026-09-03 the prompt itself prints the age, the share of the window and the word `STALE` (`set 6.9h ago — 415 of 360 min, 115% of its window, STALE — past the 6h window the gate itself uses for this tier`). The advisor's "stale" citations are the prompt read back, not invented. Unlike Titan (4 of 4 book claims false on 2026-08-27; 104/105 vpos timestamps fabricated), this population's checkable numbers are faithful; its label error rate is 2–7 % in every window and did not rise.

**Where the model does go wrong: the label over the measurement.** The numbers it quotes are right. What it does with them is not: it calls a trending market flat. Counting refusals that call the market flat, ranging or choppy while the same prompt shows 1h ADX > 25:

| window | refusals | call it flat / ranging / chop | …of which at prompt 1h ADX > 25 | …and the prompt printed `Market regime: FLAT` |
|---|---|---|---|---|
| **7 days (09-03 → 09-10)** | 417 | 353 (85 %) | **189 (45 % of refusals)** | **187 of 189** |
| week of 08-03 | 387 | 338 (87 %) | 40 (10 %) | 40 of 40 |
| week of 07-13 | 469 | 337 (72 %) | 155 (33 %) | 151 of 155 |
| week of 06-22 | 165 | 78 (47 %) | 15 (9 %) | 13 of 15 |
| after the 2310 rename (09-10 23:04 →) | 7 | 2 | 2 | 0 — the label is gone |

This is the population 2310 renamed away. In the first chunk the agents read by hand, 35 of 46 contradicted claims were exactly this ("flat market (ADX 34.8 offset by Contracting EMA-gap)", "market FLAT (ADX 1h=30 but regime=FLAT…)"). **It is a misreading, not a fabrication. By §4c it has not cost money:** the flat-cited refused shorts replay −10.32R serial on 33.

### 2d. Confidence

Pre-registered 7 days: **7 distinct values** across 418 consultations — 0.78 ×158 (157 skip + the 1 execute), 0.92 ×157, 0.82 ×59, 0.72 ×18, 0.87 ×15, 0.88 ×8, 0.85 ×3. Whole record: 11 values across 4,560; **0.92 alone is 62 %** (2,838), 0.78 is 17 %. Per week, skips use 6–9 distinct values and executes 1–3. The field is a coarse label, not a probability, exactly as on Titan; it carries no usable ranking.


---

## 3. The inputs — did the prompt change, or the market?

### 3a. The prompt — what the model actually saw, from the stored prompts themselves

**The system prompt did not change.** 4,347 of the 4,560 entry consultations ran on one entry system prompt (`cc70ed45…`, 2,179 chars), byte-identical from 2026-06-09 03:00 to today. Every other system prompt in the record differs from it in **one line only — the opposing-wall rule** — and none has been used since 2026-08-10 15:15:

| system prompt | used | consultations | executes | what differs from the default |
|---|---|---|---|---|
| `cc70ed45` default (`_ENTRY_SYSTEM`) | 06-09 → today | 4,347 | **29 (0.67 %)** | — |
| `04f98214` | 06-20 07:00 → 06-26 07:40 | 153 | 26 (17.0 %) | wall veto made SOFT for a trend-aligned LONG with 1h ADX > 22 |
| `f221365f` `_ENTRY_SYSTEM_V2_ALIGNED` | 07-10 → 08-02, **second call only** | 17 | 17 (100 %) | overhead ask wall on a confirmed uptrend LONG treated as SOFT |
| `e1487999` `_ENTRY_SYSTEM_V2_ALIGNED_SHORT` | 07-13 → 08-10, **second call only** | 25 | 25 (100 %) | bid wall below a confirmed-downtrend SHORT treated as SOFT |
| `004920b0`, `af724864` | 06-08 only | 18 | 0 | pre-A-series drafts |

The two V2 variants are 100 % by construction: the stored system prompt is set to them **only when their second call flipped the default SKIP**. `ADVISOR_WALL_ALIGNED_RELAXATIONS = False` (2026-08-14) removed that second call.

**The user prompt changed in six rendered steps since 2026-08-01, all confirmed in the stored prompts.** Dates are from the `.bak` chain (the SOL tree is not under git), the reports and the first stored render. The share of consultation prompts per week carrying each element:

| week | 1H tier line present | "Tier agreement vs SIDE" block | `STALE` marker | age-window format (`N of M min, P % of its window`) | `Market regime:` line |
|---|---|---|---|---|---|
| 06-08 … 07-20 | 0 % | 0 % | 0 % | 0 % | 100 % |
| 07-27 | 27 % | 27 % | 0 % | 0 % | 100 % |
| 08-03 | 100 % | 100 % | 37 % | 0 % | 100 % |
| 08-10 | 100 % | 100 % | 62 % | 0 % | 100 % |
| 08-17 | 100 % | 100 % | 48 % | 0 % | 100 % |
| 08-24 | 100 % | 100 % | 45 % | 0 % | 100 % |
| 08-31 | 100 % | 100 % | 56 % | 66 % | 100 % |
| 09-07 | 100 % | 100 % | 63 % | **100 %** | 97 % |

| # | first render | change | where |
|---|---|---|---|
| 1 | 2026-08-01 17:00 (row 14981) | "Truthful agreement" rewrite. The sentence `The 3 timeframes are aligned (confluence has already passed). Decide…` was replaced by `PROPOSED ENTRY: SIDE`, a computed `Tier agreement vs SIDE` block, and `The cascade gate, the score gate and the risk gate have already passed … it is NOT a statement that the tiers listed above agree with each other.` | entry user-prompt builder |
| 2 | 2026-08-01 17:20 (row 14988) | `AI_ADVISOR_HIDE_1H` True → False. **The 1H LuxAlgo tier becomes visible to the advisor for the first time**, with its age, and enters the agreement tally. | config flag read by the builder |
| 3 | 2026-08-05 09:40 (row 15923) | A 1H slot older than 360 min gains `, STALE — past the 6h window the gate itself uses for this tier`. | entry user-prompt builder |
| 4 | 2026-08-06 16:10 | Wall lines carry per-wall percentiles (`$P (pN, ×M)`) plus a calibration legend: `~p50 is an ORDINARY wall, p90+ is genuinely thick`. | entry user-prompt builder |
| 5 | **2026-09-03 20:05 (row 23649)** | **Every tier prints its age as a share of its own window**: `set 6.9h ago — 415 of 360 min, 115% of its window, STALE — …`, or `, NOT stale`. | entry user-prompt builder |
| 6 | 2026-09-10 23:10 (row 25616) | `Market regime: FLAT/TREND` renamed to `LuxAlgo 1H trend slot: …` with the measured ADX and trends beside it (report 2310). Seven consultations since, all refused. They cite higher-timeframe opposition or staleness, and none cites "FLAT regime". | entry user-prompt builder |

Not rendered but relevant: 08-01 20:54, the stored `ai_system_prompt` began stamping the prompt that produced the verdict. That is what makes the flip rows identifiable. On 08-02 the discarded V2 shadow call was switched off. 08-04 added the ×20 ceiling on the aligned-LONG override. **08-14 killed both overrides.** 08-06 added the 60-second state-verdict cache, which reused 21 verdicts in the whole record.

**Upstream, in front of the advisor (what reaches it).** The HTF cascade and the 2.0 score bar are **unchanged since 08-01**, checked. Added or changed:

- **08-01.** A daily-loss brake in R (`risk_halt`).
- **08-06.** The loss-streak brake re-read on the current book.
- **08-07 22:25.** The bot went live on real money.
- **08-08 ~14:05.** A per-side entry lock was added (`entry_gate_refused`).
- **08-10 18:25.** The book gate was armed (`book_blocked`).
- **08-14 18:28.** The book-gate lean floors were re-cut (SHORT 0.4129 → 0.3489) and the loss-streak brake got a recency window.
- **08-17.** The flat-ADX gate was armed (`flat_adx_blocked`).
- **09-03 19:45.** The flat-ADX gate went to dryrun, so ADX < 20 setups reach the advisor again.

**The structure diff, the high-pass weeks against now.** The weeks of 06-22 and 07-13 carried *no* 1H tier, *no* tier-agreement block and *no* ages, and told the model the timeframes were aligned. Their executes were, however, almost all the override, not the advisor: 23 of 23 in the week of 06-22 and 24 of 26 in the week of 07-13 came from the non-default prompts. On the default verdict alone, the materially higher weeks are **08-03** (6 of 149 LONG) and **08-17** (3 of 44 LONG) — both already on today's structure bar the age window. **For that comparison the structural change that matters is step 5, the 09-03 age window, not the 08-01 rewrite.** Unchanged throughout: the volatility / regime block, the OHLCV higher-timeframe trend block, the order-book block, combo weight, and the ATR / volume line.


### 3b. The arriving mix — this is where the answer is

Pass by how many of the OHLCV 1h / 4h / 1d trends agree with and oppose the proposed side (whole record, consultations, 06-20 → 06-26 prompt era excluded):

| aligned / opposed | n | final executes | of which the advisor's own verdict |
|---|---|---|---|
| 0 / 0 | 191 | 0 | 0 |
| 0 / 1 | 642 | 0 | 0 |
| 0 / 2 | 790 | 0 | 0 |
| 0 / 3 | 485 | 0 | 0 |
| 1 / 0 | 555 | 16 | 1 |
| 1 / 1 | 691 | 4 | 0 |
| 1 / 2 | 147 | 0 | 0 |
| 2 / 0 | 564 | 28 | 19 |
| 2 / 1 | 78 | 1 | 1 |
| 3 / 0 | 264 | 22 | 8 |

**Any opposition: the advisor's own verdict passed 1 of 2,833. No opposition: 28 of 1,574.** Its working rule is plain in its record: it does not take a trade a higher timeframe argues against. Most of the passes in the aligned cells used to come from the relaxation override.

Share of consultations per week by alignment, and the daily trend they arrived under:

| week | n | all 3 aligned | ≥ 2 aligned | ≥ 1 opposed | 1d BEAR / BULL / NEUTRAL |
|---|---|---|---|---|---|
| 06-08 | 316 | 2.5 % | 7.9 % | 89.2 % | 265 / 0 / 50 |
| 06-15 | 223 | 6.7 % | 25.1 % | 52.9 % | 50 / 0 / 168 |
| 06-22 | 188 | 8.0 % | 22.9 % | 60.6 % | 110 / 0 / 76 |
| 06-29 | 455 | 4.6 % | 20.4 % | 73.2 % | 0 / 382 / 67 |
| 07-06 | 496 | 2.2 % | 16.3 % | 45.8 % | 0 / 94 / 399 |
| 07-13 | 495 | 3.0 % | 24.8 % | 57.6 % | 189 / 0 / 301 |
| 07-20 | 460 | 10.7 % | 30.9 % | 58.9 % | 177 / 178 / 105 |
| 07-27 | 427 | 15.5 % | 29.5 % | 56.0 % | 393 / 0 / 34 |
| 08-03 | 401 | 5.0 % | 15.0 % | 70.3 % | 137 / 0 / 264 |
| 08-10 | 253 | 0.8 % | 13.8 % | 70.8 % | **0** / 168 / 85 |
| 08-17 | 155 | 12.3 % | 18.1 % | 65.8 % | **0** / 124 / 31 |
| 08-24 | 178 | 5.1 % | 17.4 % | 69.7 % | **0** / 177 / 0 |
| 08-31 | 246 | 7.7 % | 17.5 % | 75.2 % | **0** / 206 / 40 |
| 09-07 | 267 | 3.7 % | 21.7 % | 67.0 % | **0** / 205 / 62 |

In the pre-registered 7-day window, SHORT consultations carried 1d **BULL 191 / NEUTRAL 38 / BEAR 0**, and **0 of 229 had all three aligned**. The only LONG execute of the window (vpos 43's row) was 3-of-3 aligned; the other 24 3-of-3 LONG consultations were refused. Since 2026-08-17, 114 of 178 episodes (64 %) carried opposition; for shorts, 80 of 91 (88 %).

ADX: the weekly 1h-ADX median moved between 11 and 32 without a trend. The share under 20 was 74 % in the week of 08-03, 0 % while the flat-ADX gate was armed (08-17 → 09-03, it removed them), and 47 % in the week of 09-07 after the gate went to dryrun. That dryrun is why sub-20 setups reach the advisor again — and it refuses them.

### 3c. Marginal scores — not the story

The stored `confluence_score` is **not** the number the bar compares. It stores raw + weight adjustment; the gate compares raw + macro adjustment (`MACRO_GATE_DRYRUN = False`, score gate in `main.py`). The reconstructed gate score (stored − `weighted_adj` + `macro_gate_penalty`) clears the 2.0 bar on 4,553 of 4,560 consultations; 7 early-June rows fall below it and are unexplained. The share of consultations with a gate score in **[2.0, 2.5)** is 0.0–7.3 % per week, **with no drift** (4.7 % over the last 30 days, 48 of 1,016). The median gate score is 3.5–4.75 throughout. **The bar is not admitting a growing tail of marginal setups.**

---

## 4. What the refused ones would have made

### 4a. Method

Every `ai_skipped` consultation 2026-08-11 23:01 → 2026-09-10 23:01 — the same 30-day window as the §4d baseline: **1,006 refusals** (504 SHORT, 502 LONG). Entry = the row's price. Candles = **fresh Bybit SOLUSDT linear 5m (27,407 bars, 2026-06-08 → 2026-09-11 03:50, 0 gaps) and 1h (2,740 bars, 0 gaps)**, fetched by public GET through the bot's Tor egress. ATR = the stored `srv_atr_1h` the bot itself read (4,489 rows; 53 fall back to Wilder ATR14 of closed 1h candles; median |stored / candle − 1| = 3.3 %). SL 2.5×ATR · arm at 0.75R · BE lock at entry ± 0.20 % · trail 1.875×ATR from the water mark after the lock · taker 0.100 % both legs · $100 notional · **adverse extreme first** within each bar · to its own exit. 15 were still open at the last candle and are marked there.

**Validation against reality:** the 15 live positions, replayed through the same engine, give **+7.63R against the actual +7.86R**. Across all 37 positions ever opened the correlation is 0.87; the paper era had advisor `exit_signal` closes the replay does not model.

### 4b. The cuts

| cut (30 days) | n | ΣR | Σ$ | wins | exits |
|---|---|---|---|---|---|
| **serial, cap 1 per side, both sides** | **62** | **−7.11R** | **−$5.98** | 31 | 29 SL · 27 trail · 5 BE · 1 open |
| serial SHORT | 35 | **−14.11R** | −$28.26 | 15 | 19 SL · 13 trail · 2 BE · 1 open |
| serial LONG | 27 | +7.00R | +$22.29 | 16 | 14 trail · 10 SL · 3 BE |
| serial, with the bot's real positions also occupying the slot | 62 | −7.11R | −$5.98 | — | no overlap in the window |
| independent, all 1,006 (overlapping — **shape only**) | 1,006 | −171.18R | −$254.34 | 497 | 467 SL · 437 trail · 87 BE · 15 open |
| independent SHORT (shape only) | 504 | −184.79R | −$514.72 | 237 | |
| independent LONG (shape only) | 502 | +13.61R | +$260.38 | 260 | |
| *control: the 10 executes, same engine* | 10 | +6.11R | +$13.69 | 6 | live actual **+7.13R** |

Pre-registered 7-day window alone: serial **21 → −4.63R** (SHORT 12 → −1.12R, LONG 9 → −3.51R); independent 417 → −102.51R.
Sensitivity: candle ATR instead of stored ATR moves the 30-day independent total from −171.18R to −165.51R.

### 4c. Does the 2310 finding generalise?

2310 measured the flat-cited, ADX > 25 group at **−10.05R serial on 112** over the whole record. Across **all** refusals the sign holds: 30 days −7.11R on 62; whole record, advisor's own verdict, serial **refusals −23.31R on 196 vs executes +8.09R on 18** (those 18 executes' actual positions: **+8.57R**). Split the last 30 days by whether the reason cites flat/regime: SHORT **−10.32R on 33** (flat-cited) vs **−11.79R on 31** (not); LONG +1.62R on 27 vs +4.36R on 24. **The flat-cited group is not unrepresentative: refused shorts lose whatever they cite; refused longs are near flat whatever they cite.**

The removed override, for completeness: relaxation flips replay −1.89R serial on 5 (LONG) and −0.61R on 7 (SHORT); their real positions made −4.40R on 12. The late-June prompt's executes replay −0.39R serial on 7; real −1.68R on 7.

### 4d. By group, score and side — is there a band where refusals were clearly wrong?

By higher-timeframe alignment (30 days, serial within each group):

| group | side | refusals | independent ΣR (shape) | serial n | serial ΣR | serial Σ$ |
|---|---|---|---|---|---|---|
| any of 1h/4h/1d opposed | SHORT | 436 | −182.21 | 29 | **−12.90** | −$26.20 |
| any of 1h/4h/1d opposed | LONG | 265 | +7.89 | 17 | −3.68 | −$4.41 |
| none opposed, not all aligned | SHORT | 68 | −2.57 | 7 | −2.32 | −$4.17 |
| none opposed, not all aligned | LONG | 184 | −8.05 | 18 | +1.03 | +$6.48 |
| **all three aligned** | **LONG** | **53** | **+13.77** | **11** | **+7.01** | **+$19.27** |
| all three aligned | SHORT | 0 | — | — | — | — |

By reconstructed gate score (30 days):

| gate score | side | refusals | independent ΣR (shape) | mean R | serial n | serial ΣR | serial Σ$ |
|---|---|---|---|---|---|---|---|
| [2.0, 2.5) | LONG | 21 | +2.15 | +0.102 | 9 | -3.13 | -1.46 |
| [2.0, 2.5) | SHORT | 26 | -1.42 | -0.054 | 12 | -1.71 | -3.31 |
| [2.5, 3.0) | LONG | 112 | -1.38 | -0.012 | 22 | +1.82 | +9.81 |
| [2.5, 3.0) | SHORT | 120 | -39.72 | -0.331 | 27 | -11.11 | -29.03 |
| [3.0, 3.5) | LONG | 51 | -11.27 | -0.221 | 19 | -1.43 | +4.21 |
| [3.0, 3.5) | SHORT | 53 | -22.04 | -0.416 | 18 | -4.03 | -7.99 |
| [3.5, 4.0) | LONG | 58 | +6.87 | +0.119 | 16 | +2.89 | +17.56 |
| [3.5, 4.0) | SHORT | 67 | -32.03 | -0.478 | 19 | -8.11 | -18.09 |
| [4.0, 5.0) | LONG | 123 | -13.38 | -0.109 | 19 | +0.04 | +7.43 |
| [4.0, 5.0) | SHORT | 117 | -45.41 | -0.388 | 25 | -9.97 | -26.16 |
| [5.0, 99.0) | LONG | 137 | +30.63 | +0.224 | 20 | +6.63 | +17.92 |
| [5.0, 99.0) | SHORT | 121 | -44.17 | -0.365 | 24 | -4.99 | -16.42 |

**SHORT refusals lose in every score band on the serial cut. LONG refusals are mixed, with no monotone band.** The only positive group of any size is fully aligned LONG, and it is n = 11.

---

## 5. Verdict

- **The refusals are net POSITIVE to the book.** On the 30-day serial cut, refusing saved **7.11R**. The saving comes from shorts (**14.11R** avoided), all of them offered against a daily that was never BEAR. Over the whole record the serial refused book is −24.67R. **The advisor is doing its job, and the near-zero pass rate is the correct response to what it is offered.**
- **The advisor did not change; two things around it did.** (1) The override that used to turn its SKIP into EXECUTE was removed on 2026-08-14 because it lost money (its last flip was on 08-10 15:15). (2) The funnel now offers a mix that is two-thirds HTF-opposed, and nearly all-opposed for shorts.
- **The problem is the funnel.** The cascade admits setups the advisor will not take and that lose when taken.
- **Sub-population where it might be wrong:** fully aligned LONG — 30-day serial **n 11, +7.01R** (mean +0.64R, CI [−0.40, +1.68]); whole record n 19, +4.10R (CI [−0.48, +0.91]). Control: the five LONG executes of the same 30 days were all in this group and made +11.53R actual. The advisor takes this group sometimes and has been right when it did; the open question is only whether it refuses too many of them.
- **Behaviour to watch, not act on:** 0 of 20 clean episodes since 2026-09-03 19:45 against 10.2 % before (P = 0.13); those refusals replay −2.22R serial on 8.

**What n a change would need, and how long:**

| question | effect seen | sd | n for the 95 % CI to exclude 0 | at the rate it occurs |
|---|---|---|---|---|
| are fully aligned LONG refusals wrong? (30-day effect) | +0.64R | 1.76 | ≈ 30 serial | ≈ 2.6/week → **≈ 12 weeks** |
| same, at the whole-record effect | +0.22R | 1.55 | ≈ 197 | ≈ 1.4/week → **years** |
| are SHORT refusals right? (30-day) | −0.40R | 0.87 | ≈ 18 | already met (n 35) |
| are HTF-opposed refusals right? (whole record) | −0.20R | 0.94 | ≈ 86 | already met (n 157) |
| is the book of executes positive? (whole record) | +0.14R | 1.25 | ≈ 287 | ≈ 2.7/week → **≈ 2 years** |
| did the default verdict tighten after 09-03? (clean episodes) | 0/20 vs 10.2 % | — | 46 in all with none executed for P < 0.01 — 26 more | ≈ 2.7/day → **≈ 10 days** |

Measured on **live entries** instead of replays, at the current **one entry in five days (≈ 1.4 a week)**: 30 entries take **≈ 21 weeks**, and 100 take **≈ 70 weeks**. Nothing about the advisor can be decided from live entries this year; the replay cut is the only instrument with enough n.

**No change is proposed and nothing was applied.**

---

## Verification

- **Pre-flight:** `openitems_guard` EXIT=0 at the start (titan-bot HEAD cd0f175). It also returned EXIT=0 at the end. Titan was not otherwise touched, and its tree is clean in `git status`.
- **DB read-only:** every connection was `file:…/trades.db?mode=ro` and ran SELECTs only.
- **Working directory:** always the session scratchpad, never inside the SOL tree.
- **Config:** read as text only (grep/sed). No SOL module was imported.
- **Venue:** Bybit public kline GETs only, through Tor, with no key. No order was placed.
- **Service untouched:** MainPID 1084680 before and after, `NRestarts = 0` before and after, active since 2026-09-10 23:04:47.
- **File hashes:** 34 of 36 baseline files are byte-identical (all `.py`, `config.py`, `.env`, the JSON state). The two that changed were written by the running services, not by this pass:
  - `trades.db`: the live bot added rows 25638 (15m confirm, 04:00:26) and **25639, an `open_short` refused at 04:15:18**.
  - `oi_cache.json`: the bot's OI cache (writer: market_context.py).
  - `optimizer/tg_offset.txt` (outside the hashed set) was written by `optimizer_listener.py`.
- **Book flat:** 0 open positions and 0 `active_positions`.
- **`FLAT_ADX_GATE_DRYRUN = True`** at `config.py:407`, unchanged.
- **Telegram sender:** imported from `/root/titan-bot` with bytecode writing disabled, so nothing was written into Titan's tree.
