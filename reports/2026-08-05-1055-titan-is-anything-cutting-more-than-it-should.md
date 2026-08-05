# TITAN — IS ANYTHING CUTTING MORE THAN IT SHOULD?

**2026-08-05 10:55 UTC · READ-ONLY · nothing changed, nothing proposed · HEAD `b9081ad`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
Mercury-SOL was not opened, not queried, not touched.

Runtime confirmed, not read off a file: `titan.service` **active** since 2026-08-04 19:48:47,
`/health` **200**, `virtual_positions` open rows **0**, rows still landing (`context_recorded`
at 10:50:04). **Nothing upstream was suppressing entries during the measured window** — the
funnel numbers below are clean.

---

## ANSWER IN ONE LINE

**Nothing is cutting more than the evidence supports.** The stack is behaving correctly and the
market is compressed. The one pocket that grew today was tested directly and dies under control
exactly like the 54 cells §2.54 already killed. **The pre-registered §2.47 fast trigger is not
crossed on any of its three conditions — n=11 of 100.** No change is proposed.

But the headline number is real and it is not a market fact in the way it looks:

> **The tape was NOT more cross-timeframe conflicted than normal (49.0 % vs a 50.2 % 30-window
> mean, z = −0.12, rank 17 of 31) — while the cascade posted the highest block rate of all 31
> aligned windows (89.8 % vs 73.5 %).** The gap between those two is not price structure. It is
> the 15m category's *intra*-conflict rate, which went 33.2 % → 58.4 %, and that is what a boxed
> tape does inside a 90-minute TTL.

---

## §0 — CONTAMINATION FILTERS APPLIED, AND ONE NEW ONE FOUND

Carried from OPEN-ITEMS §0 and applied throughout: the 1R boundary (2026-08-04 17:01:29 — no R
figure in this report crosses it, because **there are no entries at all in the window**), the
forming-candle caveat, `confluence_score` holding four different quantities, and
`market_regime` being NULL on refused rows (so regime is reconstructed from
`matrix_breakdown_json`, never from the column).

**🔴 THREE NEW METHODOLOGY FACTS, recorded because each one silently returns a wrong answer:**

1. **`status='executed'` is not always an entry.** Rows **15955, 16373, 19461** in the 30-day
   window are `15m_armed_exit` events with `side='na'` and an **empty** `matrix_breakdown_json`.
   Every entry statistic in this report filters `side IN ('buy','sell')`. Without that filter the
   replay below reports 3 false disagreements.
2. **🔴 SQLite NUMERIC affinity silently empties a query.** `trades.timestamp` is declared
   `DATETIME` → NUMERIC affinity. `WHERE timestamp < '2100'` converts the literal to the *integer*
   2100, and in SQLite every INTEGER sorts before every TEXT, so **the predicate is false for every
   row and the query returns 0**. I hit this twice while building this report and caught it only
   because "0 entry-intent rows since the gate went live" was implausible. Use a full date
   (`'2099-01-01'`). This is the same silhouette as the book's recurring defect: **a thing that
   reads as measured while collecting nothing.**
3. **The silence ledger over-counted by one on its first run — see §3d.** Boundary artifact, it
   self-corrects. Stated so nobody "fixes" a non-problem.

### THE REPLAY WAS VALIDATED BEFORE IT WAS TRUSTED (§0 standing rule)

The whole of §1b/c rests on reconstructing the cascade's tier reads from the stored
`matrix_breakdown_json`. That is legitimate because `apply_htf_penalty`
(`signal_matrix.py:520-525`) copies the breakdown per-category and only *adds* a `_HTF_CASCADE`
key — **per-category `net_direction` survives the penalty untouched.**

Re-running `htf_alignment` + the tolerate-NEUTRAL / Variant-B logic against today's live flags,
over 30 days of entry-intent rows:

| check | result |
|---|---|
| `htf_blocked` rows that reproduce as a BLOCK | **4077 / 4077 — 100.00 %** |
| post-cascade rows that reproduce as an ADMIT | **1496 / 1496 — 100.00 %** |
| rows with missing/blank breakdown JSON | **0** |

Exact in both directions. **The replay has standing to attribute tiers.**

---

## §1 — THE CASCADE AT 89.8 %: MARKET OR MECHANISM?

### 1a. THE SERIES, NOT THE AVERAGE

30-day aggregate: **4197 / 5744 = 73.1 %** — reproduces the book's August figure exactly.

Aligned 24 h windows ending 08:05 UTC, the same alignment the ledger uses (**mean 73.5 %,
SD 7.8 pts, n=30**):

| | rate |
|---|---|
| **LEDGER WINDOW 08-04 08:05 → 08-05 08:05** | **89.8 %** (149 / 166) |
| prior 24 h | 71.4 % (162 / 227) |
| prior 48 h | 65.4 % (121 / 185) |
| last 7 d | 75.7 % (1052 / 1390) |
| baseline 29 d excl. the window | **72.7 %** (3958 / 5443) |

**Is it an outlier or a drift? One window, at the top of the range, not outside it.**

- **z = +2.08** against the daily distribution. **0 of the 29 preceding windows** reach it →
  empirical **p = 0.033**.
- 🔴 **The naive test overstates it 2×.** A signal-level two-proportion z gives **z = 4.88,
  p < 0.0001** — but signals are autocorrelated (they arrive in clusters from one market state).
  **The unit of independence is the day, not the signal.** The honest figure is z = 2.08.
- The rolling 24 h series shows the same band was reached recently without incident: **85.2 %
  (07-31 20:05), 83.2 % (07-29 20:05), 82.6 % (07-26 08:05)**, against lows of **53.6 %** and
  **56 %**. Range 52 %–90 %; today is the maximum of the sample, by 4.6 points.

**Not a drift. One window at the top of a wide, noisy band.**

### 1b. 🔴 WHICH TIER BLOCKS — AND THIS IS WHERE THE CONTENT IS

Attribution replayed per row, then decomposed by *why* the tier failed. A tier nets NEUTRAL for
two structurally different reasons (OPEN-ITEMS §2.44): **`signal_count == 0`** (nothing live —
supply) or **`intra_conflict`** (signals live on both sides, cancelling — disagreement).

**Block cause mix:**

| cause | baseline 29 d | LEDGER WINDOW | move |
|---|---|---|---|
| 1H tier **opposes** | 34.2 % | 32.9 % | flat |
| 15m tier **opposes** | 31.9 % | **10.7 %** | 🔴 **collapsed** |
| Variant-B (1H NEUTRAL + 15m not confirming) | 33.8 % | **56.4 %** | 🔴 **+22.6 pts** |
| — **OPPOSED total** (a *live* tier against the trade) | **66.2 %** | **43.6 %** | −22.6 |
| — **ABSENT/NEUTRAL total** | **33.8 %** | **56.4 %** | +22.6 |

**Tier state at decision time, split three ways:**

| tier | | AGREE | OPPOSE | **EMPTY** | **CONFLICT** |
|---|---|---|---|---|---|
| **1H** | baseline | 17.8 % | 24.9 % | 54.0 % | 3.2 % |
| **1H** | **ledger** | 8.4 % | 29.5 % | **62.0 %** | 0.0 % |
| **15m** | baseline | 26.9 % | 28.2 % | 11.8 % | 33.2 % |
| **15m** | **ledger** | 12.7 % | 24.7 % | **4.2 %** | 🔴 **58.4 %** |
| **5m** | baseline | 70.0 % | 0.0 % | 0.0 % | 30.0 % |
| **5m** | **ledger** | 75.9 % | 0.0 % | 0.0 % | 24.1 % |

🔴 **THE FINDING: the 15m tier is NOT starved. It is CONFLICTED.** `EMPTY` fell 11.8 % → 4.2 %
while `CONFLICT` rose 33.2 % → **58.4 %**. More 15m signals are arriving than usual, and they
point both ways at once, so the category nets NEUTRAL. With 1H also NEUTRAL 62 % of the time, that
lands on the Variant-B path, which blocks unless the 15m tier positively agrees. **That single
mechanism accounts for the entire 22.6-point shift in the block mix.**

The 1H rise (54.0 % → 62.0 % EMPTY) is real but ordinary: **07-18 was 92 %, 08-01 83 %, 07-12 83 %,
07-28 83 %, 07-24 77 %**. 62 % is unremarkable in that company.

### 1c. SIGNAL ARRIVAL PER TIER — SUPPLY IS NORMAL

| feed | tier | TTL | last 30 d | 08-04 | 08-05 (to 10:35) |
|---|---|---|---|---|---|
| `trend_set` (1h) | TREND / 1H | **360 min** | ~4/day (range **0–8**) | 2 | **0** |
| `confirm_recorded` (15m) | MOMENTUM / 15m | 90 min | 18–34/day since 07-26 | **31** | 11 |
| `context_recorded` (5m) | LIQUIDITY / 5m | 30 min | ~55/day | 72 | 21 |

Newest TREND signal in `live_context_state`: **2026-08-04 23:00:05** → under a 360-minute TTL the
**1H tier has been NEUTRAL since 05:00:05 today.** That is exactly how a 6-hour TTL behaves when
1h alerts are sparse, and **days with 0 trend alerts are common (07-07, 07-18, 08-01)**.

Entry-intent arrival volume itself: **166/day in the ledger window vs a 187/day 30-window mean** —
down 11 %, well inside normal variation. **The funnel is not shrinking; its composition moved.**

### 1d. 🔴 DE-CONFOUNDED AGAINST REAL CANDLES — AND THIS IS THE KEY RESULT

Pulled BTC-USDT-SWAP candles from **OKX** (the bot's own canonical book source since §2.42 /
`34dbdbf`) — 799 × 1h, 2999 × 15m, 9199 × 5m, closed candles only. **No bot column is involved in
any number below.** Cross-timeframe disagreement = the sign of EMA9−EMA21 on 1h / 15m / 5m failing
to agree, evaluated on the 5m grid with no look-ahead. Aligned 24 h windows ending 08:05 UTC:

| measure | ledger window | 30-window mean | SD | z | rank |
|---|---|---|---|---|---|
| 🔴 **cross-TF disagreement** | **49.0 %** | **50.2 %** | 10.5 | **−0.12** | **17 of 31** |
| 1h CONTRACTING share | 54.2 % | 55.1 % | 12.4 | −0.08 | 20 of 31 |
| 15m CONTRACTING share | 44.8 % | 52.1 % | 4.8 | −1.53 | 29 of 31 |
| realised range % | **1.74 %** | 2.70 % | 1.0 | −0.97 | 26 of 31 |

**Two things are established, and they point in opposite directions:**

1. ✅ **The operator's tape read is confirmed independently.** 1h contracting at the norm; 15m
   contracting well *below* the norm (i.e. 15m expanding) — **matching the ledger's
   `1h Contracting · 15m Expanding` exactly**. The squeeze is real: realised range **1.74 %** vs a
   2.70 % mean; the 08-05 calendar day alone printed a **0.90 % range — the narrowest of all 33
   days measured** — at a 1h Bollinger width of 1.25 % against a ~2.1 % mean. Price sat 64,050–64,257
   on the last three 1h candles, inside the operator's 63,500–64,200 box.
2. 🔴 **But the tape was NOT more cross-timeframe conflicted than normal.** 49.0 % vs 50.2 %,
   **z = −0.12, rank 17 of 31 — dead centre of the distribution.**

**`market_regime` cannot answer this and was not used** (it is NULL on every refused row, §0).

### 1e. VERDICT: MARKET COMPOSITION — AMPLIFIED BY A MECHANISM THAT DID NOT CHANGE

**No mechanical change. This was checked, not assumed:**

| component | last change | evidence |
|---|---|---|
| `_htf_cascade_gate` body | **2026-05-13** (`44a5939`) | `git log -L` on the gate block |
| `CATEGORY_TTL_MINUTES` | **2026-05-16** (`b9a2935`) | `git log -S`; still `{TREND:360, MOMENTUM:90, LIQUIDITY:30, EXECUTION:5}` |
| `signal_matrix.py` since 07-01 | 3 commits, **none touch the cascade** | `dee6cee` score bar; `44731be` + `957f980` card rendering only — the single `net_direction` hit is inside `format_for_telegram` |
| `signal_tiers.py` `6d9281d` (08-03) | **labels only** | commit diff is 1 file; *"GATE ARITHMETIC UNTOUCHED. signal_matrix.py is not in the diff"* — verified true |

**So: market composition. But the honest form of that answer names the amplifier.**

The cascade's block rate hit a 31-window maximum while the price structure's own cross-timeframe
conflict sat at its median. That gap is not price. It is **the 90-minute MOMENTUM TTL holding
opposing 15m alerts live simultaneously**: in a boxed tape the 15m strategies alternate long/short,
both stay inside the TTL, the category nets NEUTRAL, and — with 1H also expired — the Variant-B
branch converts that into a veto. **The market caused it; the TTL overlap window sizes it.**

🔴 **AND THE OBVIOUS FOLLOW-UP WAS TESTED RATHER THAN LEFT AS A WORRY** — see §5.

---

## §2 — IS THE FLAT GATE CUTTING TOO MUCH? THE INSTRUMENT ANSWERS: NOT MEASURABLE YET

### 2a. THE ROWS AND THEIR DRIFT

```
SELECT COUNT(*) FROM trades WHERE status='ema_envelope_blocked'   ->   12
```
First **2026-08-04 23:10:04**, latest **2026-08-05 07:45:07**. Gate live since **08-04 14:41:20**.
**Anchors in `skip_attribution`: 12 of 12 — every refusal is tracked.** The §2.47 wiring works.

Sign convention (§0): **positive = the refused signal would have won.**

| horizon | n | mean | SD | t | 95 % CI |
|---|---|---|---|---|---|
| 15m | 12 | **−0.0475 %** | 0.160 | −1.03 | [−0.138, +0.043] |
| 1h | 12 | **−0.0865 %** | 0.335 | −0.89 | [−0.276, +0.103] |
| **4h** | **11** | **+0.0535 %** | 0.192 | +0.92 | **[−0.060, +0.167]** |
| 12h | 0 | — not yet due — | | | |
| 24h | 0 | — not yet due — | | | |

### 2b. 🔴 AGAINST THE PRE-REGISTERED TRIGGER — A VERDICT, NOT A READING

**FAST TRIGGER (§2.47, written 2026-08-04 14:35 before any data existed): n ≥ 100 AND mean 4h
drift ≥ +0.25 % AND 95 % CI excluding zero.**

| condition | required | actual | met? |
|---|---|---|---|
| sample | **n ≥ 100** | **n = 11** (11 % of it) | ❌ |
| mean 4h drift | **≥ +0.25 %** | **+0.054 %** | ❌ |
| CI excludes zero | yes | **[−0.060, +0.167] — includes zero** | ❌ |

**NOT CROSSED. Zero of three conditions.**

**Against the comparators** (4h drift; a healthy refuser sits at or below zero):

| cohort | 4h drift | n |
|---|---|---|
| `below_threshold` | −0.073 % | 875 |
| `ai_skipped` | −0.059 % | 2000 |
| `htf_blocked` | **+0.020 %** ← the alarm line | 5974 |
| **`ema_envelope`** | **+0.054 %** | **11** |

The point estimate does sit above `htf_blocked`'s +0.020 %, which was the pre-named alarm. **It is
not evidence.** Its CI **[−0.060, +0.167]** contains zero *and all three comparators* — the data
cannot currently distinguish this gate from the healthiest refuser in the book.

🔴 **AND n = 11 OVERSTATES THE INDEPENDENCE.** The 12 refusals are **~3 market episodes**, not 12
draws: 23:10 (×2), 23:30–23:55 (×6), 01:20–01:45 (×3), 07:45 (×1). **I am not reading this tail,
and §2.47's rule — count rows, never days — is the reason the tail is visible as a tail.**

One measurement worth carrying forward: the observed 4h SD on these rows is **0.192 %**, against
the **0.809 %** §2.47 assumed from the 8,800 pre-gate samples — itself a symptom of the squeeze.
At *that* SD, n=100 would give a ±0.038 % CI, so **the +0.25 % bar would be comfortably
resolvable** when the sample arrives.

### 2c. WHICH LEG FAILED ON EACH OF THE 12

| timestamp | side | 1h | 15m | legs failing |
|---|---|---|---|---|
| 08-04 23:10:04 | LONG | Flat | Expanding | 1h only |
| 08-04 23:10:07 | LONG | Flat | Expanding | 1h only |
| 08-04 23:30:07 | LONG | Contracting | Contracting | **BOTH** |
| 08-04 23:35:06 | LONG | Contracting | Contracting | **BOTH** |
| 08-04 23:40:03 | LONG | Contracting | Contracting | **BOTH** |
| 08-04 23:45:04 | LONG | Contracting | Contracting | **BOTH** |
| 08-04 23:50:05 | LONG | Contracting | Contracting | **BOTH** |
| 08-04 23:55:03 | LONG | Contracting | Contracting | **BOTH** |
| 08-05 01:20:05 | LONG | Contracting | Expanding | 1h only |
| 08-05 01:40:06 | LONG | Contracting | Contracting | **BOTH** |
| 08-05 01:45:08 | LONG | Contracting | Contracting | **BOTH** |
| 08-05 07:45:07 | SHORT | Contracting | Expanding | 1h only |

- **BOTH legs non-Expanding: 8 of 12 (67 %).** One leg only: 4 of 12 (33 %).
- 🔴 **The 1h leg is non-Expanding on 12 of 12 — it is the binding leg on every single refusal.**
  The 15m leg is non-Expanding on 8 of 12. **The gate has never yet refused on 15m alone.**
- **11 of 12 are LONG proposals.** The gate's first four evaluations (all PASS, 08-04 14:45–14:55)
  were all SHORT; its first twelve refusals are almost all LONG. The gate has now seen both sides.
- Two refusals are `Flat`, not `Contracting` — the rule is *admit iff Expanding*, so `Flat` refuses.
  That is the implemented boolean (§2.47) behaving as written.

---

## §3 — THE ADVISOR SAW 4 OF 166

### 3a. SHARE OF THE FUNNEL THAT REACHES IT

| window | entry-intent | reached advisor | share |
|---|---|---|---|
| 30 d before the gate (07-05 → 08-04 14:41) | 5786 | 769 | **13.29 %** |
| last 7 d before the gate | 1537 | 129 | 8.39 % |
| **since the gate** (08-04 14:41 → now) | 103 | 4 | **3.88 %** |
| **LEDGER WINDOW** | 166 | 4 | **2.41 %** |

🔴 **BUT 2.4 % IS NOT NEW, AND IT IS NOT THE FLAT GATE'S DOING.** The per-day series runs from
**2.3 % to 32.2 %**, and the floor was hit three times in the week *before* the gate existed:

```
07-30  2.4%      07-31  2.3%      08-01  2.4%        <- all PRE-gate
08-04  2.8%      08-05  0.0%      (30d mean 13.3%)
```

**The advisor's share of this funnel has been swinging by an order of magnitude all month.** Today
is at the bottom of that range; it has been there before, without the flat gate.

### 3b. WHAT THE 4 CITED — VERBATIM

All four `ai_skipped`, all SHORT, all `claude-haiku-4-5-20251001`, all **confidence 0.92**:

> **row 21347** (14:45:17, raw 7.66) — *"SHORT entry contradicts dominant bullish regime
> (4H/1H/15m/5m all BULL). 15m+5m agree on SHORT but lack higher-TF confirmation. 1d NEUTRAL, 4h
> BULL, 1h BULL, 15m BULL, 5m BULL—4/4 lower TFs oppose the signal. FLAT market regime with weak
> ADX (1h 21.7, 15m 24.3) suggests chop risk. 1H signal direction withheld—opaque context.
> Ask-heavy book (0.39 imbalance) and ask wall at ×7.5 (74th pctile) above"*

> **row 21348** (14:45:17, raw 5.66) — *"1H/15m/5m all BULL regime vs SHORT entry. 4/4 lower-TF MTF
> align opposes trade."*

> **row 21349** (14:50:10, raw 9.00) — *"SHORT entry contradicts 4H/1H/15m/5m BULL regime (0/4 MTF
> alignment). 1H signal withheld; market FLAT with weak ADX. Skip."*

> **row 21350** (14:55:08, raw 8.25) — *"SHORT contradicts dominant BULL regime (4h/1h/15m/5m all
> BULL, MTF=0/4). Flat market, low vol, weak volume ratio (0.29x). Skip."*

**One reason, four times: counter-trend SHORT into a bull MTF stack, in a FLAT regime with weak
ADX.** Note it declined a **raw 9.00** — the highest score in the window.

### 3c. IS IT DECORATIVE?

**No — but it decides very little, and both halves of that are true.**

| | advisor saw | admitted | declined |
|---|---|---|---|
| 30 d pre-gate | 769 | **27** | 709 — **92.2 % of what it sees** |
| since the gate | 4 | 0 | 4 — 100 % |

It is the **most refusing gate in the stack by rate** among those that see anything. It is not a
rubber stamp. But it is consulted on **2.4 % of the funnel today (13.3 % over 30 days)**, so
**97.6 % of today's outcome was settled before it was asked.** That is a structural fact about
where the decision lives, not a defect — and it is **not a change**: the cascade has been
consuming 65–90 % of the funnel all month.

🔴 **ONE SEAM WORTH RECORDING, NOT CHASING.** On **row 21347**, at one instant, on one row:

- the **cascade** read `TREND=NEUTRAL (0 signals) · MOMENTUM=SHORT · EXECUTION=SHORT` and
  **tolerated** the SHORT;
- the **advisor** read `trend_1h=bull · trend_15m=bull · trend_5m=bull` and **declined** it as
  counter-trend.

Two quantities, both spoken of as "timeframe alignment", pointing opposite ways on the same row.
They are genuinely different things — TradingView signal categories vs EMA-derived trend columns —
so this is not a defect. It is the book's **"one fact, several judges"** class (§2.26), and it
means the advisor is currently the *only* stage reading the EMA trend at entry. **Recorded, not
chased, nothing proposed.**

### 3d. THE SILENCE LEDGER OVER-COUNTED BY ONE — FIRST-RUN BOUNDARY ARTIFACT

The ledger reported *"reached the flat gate: 17 — refused 12 (71 %)"*. **The correct figures are
16 and 75 %.** `silence_digest.py:74` sums all post-cascade statuses in the 24 h window, and that
window opened at 08-04 08:05 — **six minutes before the gate existed (14:41:20)**. The extra row is
the `below_threshold` at **14:35:06**, which was refused by the *score* gate and never saw the flat
gate at all.

**This is a first-day boundary effect only** — every future 24 h window lies entirely after the
gate went live, so tomorrow's digest is correct without any change. **It would return only if the
gate is ever toggled off and on.** Stated with its magnitude so it is neither rediscovered as a
bug nor "fixed" unnecessarily. **Nothing proposed.**

---

## §4 — THE HONEST ARITHMETIC OF OVER-FILTERING

### 4a. THE FUNNEL AS MEASURED, AND THE PROJECTION

**Since the gate went live (19.90 h):**

| stage | count | note |
|---|---|---|
| entry-intent | 103 | 124/day |
| cascade blocked | 87 | 84.5 % |
| **reached the flat gate** | **16** | **19.3/day** — §2.47's corrected projection was **18.6/day** ✅ |
| flat gate refused | 12 | **75.0 %** of arrivals (§2.56 counterfactual: 81.2 %) |
| score gate refused | 0 | |
| reached the advisor | 4 | |
| **ENTERED** | **0** | |

🔴 **§2.47's corrected arrival clock is confirmed by independent measurement for the first time:
19.3/day observed against 18.6/day projected.** The original 51.3/day figure remains wrong by 2.6×,
exactly as the 19:55 correction said.

**Projected entries/day under today's full stack**, using this regime's measured stage rates and
the 30-day book for the advisor (today's n=4 cannot estimate an admit rate):

```
166/day arrivals  ×  0.102 cascade  ×  0.294 flat gate  ×  0.800 score  ×  0.035 advisor
                                                          =  0.140 entries/day
```

| | entries/day | meaning |
|---|---|---|
| pre-gate book rate (§2.47 pre-registration) | **0.90** | 27 entries / 30 d |
| post-gate PROJECTION (§2.47) | **0.47** | 14 of 27 survive the envelope |
| **THIS REGIME, measured** | **0.14** | **one entry every 7.1 days** |
| actually observed | **0.00** | 0 entries in 19.9 h |

**The drop from 0.47 to 0.14 is not the flat gate. It is the cascade**, whose pass rate fell from
~26 % to 10.2 % on the composition shift in §1b.

### 4b. 🔴 TIME TO ANSWERABILITY — IN ROWS FIRST, CALENDAR SECOND

Measured refusal rate: **12 rows in 19.90 h = 14.5 refusals/day** (§2.47 corrected estimate: ~15/day
✅; §2.47 original: ~40/day ❌).

| target | **IN ROWS** | in calendar days at 14.5/day |
|---|---|---|
| **FAST TRIGGER n ≥ 100** | have **12**, need **88 more rows** | **6.1 days** (§2.47 said ≈6.6) |
| SLOW TRIGGER n ≥ 700 | have 12, need **688 more rows** | 47.5 days (§2.47 said ≈46) |

| **20 executed entries PER SIDE = 40 entries** | days | months |
|---|---|---|
| at 0.90/day (pre-gate book) | 44 | 1.5 |
| at 0.47/day (§2.47 projection) | 85 | 2.8 |
| **at 0.14/day (this regime)** | **285** | **9.4** |

🔴 **THE CALENDAR COLUMN IS CONDITIONAL AND HAS MISLED TWICE. THE OPERATIVE CHECK IS THE ROW
COUNT:**

```sql
SELECT COUNT(*) FROM trades WHERE status='ema_envelope_blocked';
```

**Not the date.** A session that reads "6 days" and finds the gate quiet on day 3 will conclude the
gate is broken and be wrong — quiet *is* what 14.5/day looks like.

### 4c. THE PLAIN STATEMENT

**Yes: the stack is correct, and in this regime the bot will trade roughly once a week.**

A correct filter in a squeezed market is *supposed* to be quiet. **The cost is measurement speed,
not money** — the flat gate's own review point moves from ~3 months to ~9 months if this regime
holds, and the fast trigger needs 88 more refusal rows. **The bot is not losing money by being
quiet; it is losing evidence.** Those are different problems and only one of them is urgent, and it
is not this one.

---

## §5 — VERDICT

### NOTHING IS CUTTING MORE THAN THE EVIDENCE SUPPORTS

**The flat gate — not answerable, and the trigger says so.** n=11 of 100 at the 4h horizon, mean
**+0.054 %**, CI **[−0.060, +0.167]** containing zero and all three comparators, from **~3 market
episodes**. **Zero of three pre-registered conditions met.** Per §2.47 and §2.45 nothing may be
proposed off it, and nothing is.

**The cascade — the one pocket that grew was tested, and it dies.** The mix shift in §1b points at
exactly one cell: blocks where the **1H tier is EMPTY and the 15m tier is INTRA-CONFLICTED** (23.6 %
→ 38.9 % of all blocks). Tested on 30 days of 4h drift with §2.54's own controls, and with the
cell's own rows excluded from the baseline (the degenerate-control bug §2.54 caught):

```
none (raw)          +0.0469%   t= +2.66   n=998
+ day               +0.0190%   t= +1.05   n=998
+ day+direction     -0.0244%   t= -1.20   n=998     <- SIGN FLIPS NEGATIVE
+ day+dir+HOUR      -0.0134%   t= -1.31   n=530
```

Neighbouring cells, for placement: `1H EMPTY & 15m live` +0.045 % (t=+2.51, n=1261) · `1H live &
15m CONFLICT` +0.009 % (t=+0.29, n=562) · `1H live & 15m live` +0.026 % (t=+1.28, n=1316).

🔴 **The raw t of +2.66 is under §2.54's Bonferroni bar of |t| > 3.31 — and that bar can only get
stricter, since this is cell 55 of a budget set at 54.** More decisively: **the sign flips negative
under control.** *An effect whose sign depends on the control is not an effect* — §2.54's own words,
and this pocket has the identical silhouette. **§2.54's verdict extends to it: the cascade is
refusing correctly, as far as this data can determine.**

**The advisor — 2.4 % is not a change and not the gate's doing.** It hit 2.3–2.4 % on 07-30, 07-31
and 08-01, days before the flat gate existed.

### WHAT IS ACTUALLY TRUE TODAY

1. **The market is compressed** — realised range 1.74 % vs 2.70 %, the 08-05 day printing the
   narrowest range of 33 days at 0.90 %. The operator's chart read is confirmed from candles.
2. **The cascade posted its highest block rate of 31 windows (89.8 %) while the tape's own
   cross-timeframe conflict sat at its median (49.0 % vs 50.2 %).** That gap is the 90-minute
   MOMENTUM TTL holding opposing 15m alerts live at once — market-caused, mechanism-sized, and
   **not** a code change: the cascade body last moved **2026-05-13**, the TTLs **2026-05-16**.
3. **Zero entries is correct behaviour**, and the cost is measurement speed: **88 more refusal
   rows** to the fast trigger, **9.4 months** to the 20-per-side review point if this regime holds.

### 🔴 NOTHING IS PROPOSED

No trigger crossed; no eleventh filter; no relaxation. The two things that *would* change this
answer are already written down and are both counted in **rows, not days**: **n ≥ 100 refusals**
for the fast trigger, and **20 executed entries per side** for the review point.

The one genuinely open item this pass created is **not** an action: **the TTL-overlap amplifier in
§1e is now named and quantified** (15m intra-conflict 33 % → 58 % with price-structure conflict
flat). It is an observation with a measured size, tested for harm in §5 and found harmless on 998
rows. **If it is ever acted on, it is a cascade change — the risk class §2.54 explicitly assigned
to propose-and-stop, worth ~+0.45 entries/day, i.e. roughly doubling the entry rate.** Not today,
and not on this sample.

---

*Read-only pass. Live DB snapshotted to scratchpad before any query; `titan-bot` untouched;
Mercury-SOL never opened. All candle data from OKX public REST, closed candles only.*
