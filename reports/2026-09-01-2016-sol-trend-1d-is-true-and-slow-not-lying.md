# Mercury-SOL — is `trend_1d` lying? No. It is true, and slow by one to three days — and the 1926 report invoked it on two days it cannot explain

**2026-09-01 20:16 UTC · READ-ONLY RE-EXAMINATION · nothing was changed**

Subject: Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`), SOL/USDT:USDT on Bybit, LIVE real money.
`openitems_guard` run first → **exit 0**, header and current-state table agree with runtime.
Under test: §4b of `2026-09-01-1926-sol-why-no-short-on-the-30aug-drop.md`, which rested on
*"`trend_1d` has read `bull` on every single day since 2026-08-18."* I repeated that without checking it against price. This pass checks it.

---

## THE ANSWER, FIRST

**`trend_1d` is NOT lying. It is TRUE and slow by construction — but the lag is one to three days, not three weeks, and it is EMA9 that binds, not EMA21.**

* The label read `bull` on 30 Aug and 31 Aug. Independent recomputation on real Bybit daily candles agrees: on both days close > EMA9 > EMA21 with a rising EMA9. **That is not a false statement about the daily trend.** SOL closed 30 Aug at 101.70 — 10.6% and 1.84 ATR *above* its 21-day EMA. And 31 Aug closed **up** on the day (open 101.70 → close 102.99, +1.27%); the −6.7% the operator read off the 1h chart for "31 Aug" is the 31 Aug high (105.01) to the 1 Sep low (98.27), a two-day intraday range.
* **The label already flipped.** At 18:00 UTC today, 1 Sep, the recomputed label goes `bull → neutral` — close 99.54 fell below EMA9 100.27. The bot's last stored reading (18:40, `bull`) was served off its own documented ≤3600 s OHLCV cache; its next uncached read returns `neutral`. The label was three days behind the first drop day, not fourteen.
* **The implementation is correct.** 2,020 of 2,084 stored readings (96.93%) reproduce **exactly** from candles I fetched myself. All 64 mismatches are one-cent borderline cases inside the ≤1 h cache window. **This is a finding about the FORMULA'S DEFINITION, not a bug.**
* 🔴 **But my 1926 conclusion was still wrong — for a different reason than the operator suspected.** The label is true; it simply **was not present on two of the three drop days.** On 30 Aug, 135 SHORT rows were generated and **not one reached the advisor.** On 1 Sep, 99 SHORT rows, **not one reached the advisor.** The advisor — the only consumer of `trend_1d` — never saw them. "Regime, not a gate" is an answer about a mechanism that did not run on the days it was asked to explain. **It explains 31 Aug and nothing else.**
* The 4.4× asymmetry itself **survives and strengthens** under a recomputed label (6.57×, Fisher p = 0.0064). It was not driven by a false input.

---

## 1. WHAT THE LABEL ACTUALLY SAID, DAY BY DAY

### 1a. `trend_1d` from the bot's own rows, 2026-08-15 → now

Two tables carry it. `trades.trend_1d` is written only for rows that **reach the advisor** (`main.py:5166`). `skip_attribution.trend_1d` is written at **block time**, from a separate `fetch_snapshot(tfs=('1d','4h'))` at `main.py:4151`, for rows killed **before** the advisor. Reading only `trades` — as the 1926 report did — leaves holes. Both are shown.

| day | `trades` | `skip_attribution` | verdict for the day |
|---|---|---|---|
| 2026-08-15 | bull 11, neutral 16, NULL 335 | bull 64, neutral 51, NULL 151 | mixed |
| 2026-08-16 | neutral 57, NULL 219 | neutral 112, NULL 94 | **neutral** |
| 2026-08-17 | neutral 31, NULL 277 | neutral 133, NULL 104 | **neutral** |
| 2026-08-18 | bull 5, NULL 260 | bull 55, neutral 6, NULL 102 | bull (flips early in the day) |
| 2026-08-19 | bull 23 | bull 69 | **bull** |
| 2026-08-20 | bull 36 | bull 42 | **bull** |
| 2026-08-21 | bull 28 | bull 68 | **bull** |
| 2026-08-22 | bull 32 | bull 105 | **bull** |
| 2026-08-23 | — (0 readings) | bull 76 | **bull** |
| 2026-08-24 | — (0 readings) | bull 54 | **bull** |
| 2026-08-25 | bull 38 | bull 68 | **bull** |
| 2026-08-26 | bull 67 | bull 110 | **bull** |
| 2026-08-27 | bull 18 | bull 37 | **bull** |
| 2026-08-28 | bull 31 | bull 114 | **bull** |
| 2026-08-29 | bull 23 | bull 107 | **bull** |
| **2026-08-30** | **— (0 readings)** | **bull 92** | **bull** |
| **2026-08-31** | **bull 40** | **bull 171** | **bull** |
| **2026-09-01** | **bull 6** | **bull 88** | **bull** (recompute flips to neutral at 18:00 UTC; see §2d) |

No `bear` reading exists anywhere in the window. The 1926 report's "bull every single day since 18 Aug" is **correct on the union of both tables** — but from `trades` alone it had three blank days (23, 24, 30 Aug) it did not name.

### 1b. 🔴 The label beside real Bybit daily candles (`SOL/USDT:USDT`, `1d`)

| day | open | high | low | close | O→C % | `trend_1d` |
|---|---|---|---|---|---|---|
| 2026-08-19 | 77.02 | 87.34 | 76.59 | 85.37 | **+10.84%** | bull |
| 2026-08-20 | 85.37 | 88.09 | 83.95 | 87.63 | +2.65% | bull |
| 2026-08-21 | 87.63 | 95.02 | 87.55 | 93.72 | +6.95% | bull |
| 2026-08-22 | 93.72 | 102.74 | 87.64 | 93.81 | +0.10% | bull |
| 2026-08-23 | 93.81 | 97.24 | 91.54 | 95.42 | +1.72% | bull |
| 2026-08-24 | 95.42 | 98.98 | 93.22 | 98.97 | +3.72% | bull |
| 2026-08-25 | 98.97 | 103.21 | 94.84 | 96.54 | −2.46% | bull |
| 2026-08-26 | 96.54 | 102.45 | 94.84 | 102.04 | +5.70% | bull |
| 2026-08-27 | 102.04 | 110.61 | 100.48 | 109.08 | +6.90% | bull |
| 2026-08-28 | 109.08 | 110.07 | 102.17 | 104.09 | −4.57% | bull |
| 2026-08-29 | 104.09 | 105.83 | 102.97 | 105.56 | +1.41% | bull |
| **2026-08-30** | **105.56** | **107.43** | **100.21** | **101.70** | **−3.66%** | **bull** |
| **2026-08-31** | **101.70** | **105.01** | **100.81** | **102.99** | **+1.27%** | **bull** |
| **2026-09-01** | **102.99** | **104.35** | **98.27** | **99.94** (live) | **−2.96%** | **bull → neutral 18:00 UTC** |

**On the operator's three numbers.** 103.67 → 99.93 on 1 Sep is real (an intraday leg; the daily open is 102.99). 107.43 → 100.21 on 30 Aug is that day's own **high to low**. 105.01 → 98.27 straddles **two days** — 31 Aug's high and 1 Sep's low. Peak-to-trough across the three days is 107.43 → 98.27 = **−8.53%**. But **31 Aug closed higher than it opened.** "Three consecutive declines" is true of the 1h chart's shape and false of the daily closes, and `trend_1d` is a daily-close construct. Both facts are real; they are measuring different things.

### 1c. 🔴 Plainly: on the three drop days, what did `trend_1d` read?

* **30 Aug: `bull`** — 92 readings in `skip_attribution`, all `bull`. Zero readings in `trades`, because **no signal reached the advisor all day**.
* **31 Aug: `bull`** — 211 readings across both tables, all `bull`, all 24 hours.
* **1 Sep: `bull`** — 166 readings, all `bull`, up to the last one at 18:40 UTC. **The recomputed label turns `neutral` at the 18:00 UTC hourly close;** the 18:00–18:40 readings are the bot's ≤1 h candle cache still serving 17:xx data.

---

## 2. 🔴 IS THE LABEL COMPUTED CORRECTLY?

### 2a. Which candles feed it

The classifier, `indicators.py:322-329`, verbatim:

```python
def _classify_trend(close, ema9, ema21, slope_pct) -> Optional[str]:
    if close is None or ema9 is None or ema21 is None or slope_pct is None:
        return None
    if close > ema9 > ema21 and slope_pct > TREND_SLOPE_FLAT_PCT:
        return TREND_BULL
    if close < ema9 < ema21 and slope_pct < -TREND_SLOPE_FLAT_PCT:
        return TREND_BEAR
    return TREND_NEUTRAL
```

Its one call site, `indicators.py:403-406`:

```python
last_close = float(df.close.iloc[-1])
ema9_last  = _safe_last(ema9_series)
ema21_last = _safe_last(ema21_series)
out['trend'] = _classify_trend(last_close, ema9_last, ema21_last, out['ema9_slope'])
```

The candles reaching it:

* **Timeframe string: literally `'1d'`.** `HTF_TFS = ('1d', '4h', '1h', '15m', '5m')` (`indicators.py:44`), passed to `fetch_snapshot` at `main.py:4525`, and `('1d','4h')` at `main.py:4151`. Each tf is fetched with `exchange.fetch_ohlcv(symbol, '1d', limit=200)`. **Genuinely daily candles from Bybit. Not resampled, not derived from 1h.**
* **Number of bars: 200** (`CANDLE_LIMIT = 200`, `indicators.py:55`) — 200 daily bars, far beyond EMA21 warm-up.
* **`slope_pct` is `ema9_slope`, not EMA21's:** `_slope_pct(ema9_series, lookback=3)` — the % change of **EMA9 over 3 daily bars** — against `TREND_SLOPE_FLAT_PCT = 0.05` (%).
* **`close` is the FORMING daily bar** — `df.close.iloc[-1]` is today's partial candle, i.e. the live price. Note that the volume path immediately above (`indicators.py:391`) deliberately **drops** that forming row (`vol_closed = df.volume.iloc[:-1]`) because a partial bar distorts it. The trend path deliberately keeps it. Both choices are documented; keeping it makes the label **more** responsive, not less.

### 2b. Independent recomputation, reading by reading

I fetched 200 daily and 2,229 hourly `SOL/USDT:USDT` bars from Bybit myself (via the same Tor SOCKS proxy, public read, in `/tmp`), reconstructed the forming daily bar at each stored reading's wall-clock timestamp, and reran the classifier with the same constants — same `pandas_ta` EMA, same lookback 3, same 0.05 threshold.

**2,084 stored readings tested (both tables, since 2026-08-15). 2,020 reproduced EXACTLY. 64 mismatched. Agreement 96.93%.**

| day | reproduced | mismatch |
|---|---|---|
| 2026-08-15 | 99 | 43 |
| 2026-08-16 → 08-17 | 333 | 0 |
| 2026-08-18 | 61 | 5 |
| 2026-08-19 → 08-29 | 1,146 | 0 |
| **2026-08-30** | **92** | **0** |
| **2026-08-31** | **211** | **0** |
| **2026-09-01** | **78** | **16** |

Every mismatch is a **borderline case inside the cache window**, and every one is explained:

```
2026-08-15 01:25  stored=bull  recomputed=neutral  close=75.38  ema9=75.39   (one cent apart)
2026-09-01 18:15  stored=bull  recomputed=neutral  close=99.54  ema9=100.27  slope=+0.922
2026-08-18 00:00  stored=neutral recomputed=bull   close=76.00  ema9=75.50   slope=+0.162
```

The 1 Sep cluster is the cache (§2d): the label flipped at the 18:00 hourly close and the bot was still serving candles fetched before 18:00. The 15 Aug and 18 Aug clusters are the same effect at a day boundary plus a sub-cent gap between close and EMA9 — my hourly-bar proxy for the forming close cannot resolve that, the bot reads it live.

**On the three days that matter — 30 Aug, 31 Aug, 1 Sep before 18:00 — reproduction is 100%, 100%, 100%.**

🔴 **The code is correct. This finding is about the FORMULA'S DEFINITION, not a bug.** There is no defect to outrank it.

### 2c. 🔴 The lag question — with the numbers

The operator's premise was that EMA21 on daily candles is a three-week average and price must fall through three weeks of August gains before the label flips. **The number says otherwise, because EMA21 is not the binding condition.**

| day | close | EMA9 | EMA21 | ATR14 | close − EMA9 | close − EMA21 | EMA9 − EMA21 |
|---|---|---|---|---|---|---|---|
| 2026-08-30 | 101.70 | 99.81 | 91.94 | 5.31 | **+1.89% / +0.35 ATR** | +10.61% / +1.84 ATR | +8.56% |
| 2026-08-31 | 102.99 | 100.45 | 92.95 | 5.23 | **+2.53% / +0.49 ATR** | +10.81% / +1.92 ATR | +8.07% |
| 2026-09-01 | 99.94 | 100.35 | 93.58 | 5.29 | **−0.41% / −0.08 ATR** | +6.79% / +1.20 ATR | +7.23% |

The daily EMA21 does sit **10.6% and 1.84 ATR below price** on 30 Aug — three weeks of gains, exactly as suspected. **But nothing waits on it.** BULL requires `close > ema9 > ema21`; `ema9 > ema21` was satisfied with 8.5% of room to spare, so the **first** condition to break was `close > ema9`, and on 30 Aug that was only **0.35 ATR away**. It broke on the third drop day. **The lag to leaving `bull` is ~1 to 3 days, not three weeks.**

The three-week lag is real for the **other** direction. `bear` requires `close < ema9 < ema21` — EMA9 must cross **below** EMA21, which on 1 Sep are 7.23% apart:

* at −3%/day sustained: **6 more days** (price ≈ 83.25)
* at −5%/day sustained: **5 more days** (price ≈ 77.33)
* at **flat price**: **never** — under a constant price EMA9 converges from above and stays above EMA21 permanently.

**So the mechanical explanation, stated with the number: `bull` → `neutral` costs one bad daily close through a 9-day EMA (0.35 ATR on 30 Aug). `neutral` → `bear` costs about a week of −3% days. The label spent 30–31 Aug within half an ATR of flipping and flipped on 1 Sep. It was never going to say `bear` in this window, and it never did.**

### 2d. Is the label stale?

**Recomputed on every evaluation — but on candles cached for up to one hour.** `fetch_snapshot` is called fresh at each advisor seam and each block seam; `compute_tf_metrics` recomputes EMA9/EMA21/slope every time; nothing memoises the label itself. What *is* cached is the OHLCV underneath, in `_fetch_ohlcv_cached` (`indicators.py:332`) keyed on `(symbol, tf)` with:

```python
_CACHE_TTL_BY_TF = {'1m':30.0, '5m':30.0, '15m':60.0, '1h':300.0, '4h':600.0, '1d':3600.0}
```

**`'1d'` → 3600 s.** So the label is at most one hour behind the tape, and the cache is process-wide and shared between the block path and the advisor path. This is a deliberate fetch-reduction choice, documented in the file. It is also exactly and only what produced the 16 mismatches on 1 Sep: the flip happened at 18:00 UTC, the bot's readings from 18:05 to 18:40 were computed on pre-18:00 candles.

---

## 3. HOW MUCH DOES IT ACTUALLY DRIVE

### 3a. 🔴 Is `trend_1d` read by any gate?

**No mechanical gate reads it. Verified by tracing every consumer, not by re-reading the 1926 report.** `grep -rn "trend_1d"` over every live module gives four consumer classes, and all four are terminal:

1. **DB schema + write** — `main.py:1053` (column), `main.py:5166` (`update_trade(... trend_1d=...)`). Recording.
2. **skip_attribution** — `main.py:4149-4164` → `skip_attribution.py:344,386,397`. Recording at block time.
3. **The advisor prompt** — `claude_advisor.py:679-681`, rendered by `_trend_line('1d')` into the "Higher Timeframes Trend" block.
4. **`mercury_sol_prior_move_logger.py:104,136`** — post-hoc analysis, reads only.

Nothing else. No `if trend_1d ==` anywhere. And `mtf_alignment_score` **structurally excludes 1d**: `ALIGNMENT_TFS = ('4h','1h','15m','5m')` (`indicators.py:47`), commented as deliberate. `weight_engine.weighted_adj` receives the snapshot but reads no `1d` key at all, and is informational anyway.

🔴 **However, "narration only" understates it, and I should have said this the first time.** The advisor's **system prompt** carries an explicit standing instruction (`claude_advisor.py:146-151`):

> *"Treat the 1d and 4h trends as the dominant regime: when they clearly oppose the proposed entry direction, lean toward 'skip' unless the lower-TF confluence is exceptionally strong."*

That is not a mechanical gate — an LLM can and sometimes does override it. But it is a written order to lean, aimed at a label that has read `bull` for two weeks, and §3b shows it is obeyed almost without exception.

### 3b. Advisor reasons citing the daily regime, since 2026-08-18

| side | skips | citing "1d" or "daily" verbatim |
|---|---|---|
| **SHORT** | 205 | **200 = 97.6%** |
| LONG | 139 | 55 = 39.6% |

Broadened to any daily/HTF-regime language, **205 of 205 SHORT skips (100%)** cite it. Three verbatim, all from 31 Aug — the one drop day on which shorts actually reached the advisor:

> `[2026-08-31 02:15:04] trend_1d=bull` — **"1d BULL (ADX 49.3) conflicts SHORT; 4h/1h/15m neutral/bear but 1d dominance rules. Skip."**

> `[2026-08-31 03:30:03] trend_1d=bull` — **"1d BULL trend (ADX 49.3) opposes SHORT; 4h NEUTRAL weak. MTF misaligned (2/4). Ask wall at $101.75 (p61, x9.9) blocks downside momentum entry."**

> `[2026-08-31 17:15:03] trend_1d=bull` — **"1D bull regime (ADX 49.3) + flat market (ADX 1h 23.9, EMA contracting, regime FLAT, MTF 1/4) opposes SHORT. Stale 1H long signal adds friction. Skip."**

The first one is the clearest statement in the record of what this label does: **every lower timeframe was neutral-or-bear, and the 1d label overrode all of them.** It was not lying when it did so — but it was, on 31 Aug, the whole decision.

### 3c. 🔴 Does the asymmetry survive a correct label?

Rebuilt from scratch: every `trades` row since 2026-06-08 with `ai_decision ∈ {execute, skip}` (4,093 rows), labelled three ways — the stored label, my independent recomputation at each row's timestamp, and the §4b alternative. Same rows, same query, all three columns.

| regime | SHORT passed | LONG passed | ratio against SHORT |
|---|---|---|---|
| **stored `trend_1d`** | | | |
| bull | 2 / 654 = **0.31%** | 10 / 515 = **1.94%** | **6.35×** |
| neutral | 30 / 902 = 3.33% | 21 / 678 = 3.10% | 0.93× |
| bear | 26 / 654 = 3.98% | 4 / 667 = 0.60% | 0.15× (against LONGs) |
| **RECOMPUTED `trend_1d`** | | | |
| bull | 2 / 661 = **0.30%** | 10 / 503 = **1.99%** | **6.57×** |
| neutral | 28 / 902 = 3.10% | 23 / 695 = 3.31% | 1.07× |
| bear | 28 / 662 = 4.23% | 4 / 670 = 0.60% | 0.14× (against LONGs) |

Fisher exact, two-sided, on the bull row: **stored p = 0.0072; recomputed p = 0.0064.**

🔴 **The asymmetry survives. It gets slightly stronger, and slightly more significant.** It was **not** driven by a false input — the recomputed label moves only 15 rows between buckets and the picture is unchanged. The sign still flips with the regime (shorts favoured 6.7× in `bear`), which is what a symmetric regime filter looks like.

**One correction I owe on my own arithmetic.** The 1926 report printed *0.31% shorts vs 1.37% longs, 4.4×, p = 0.048*. Re-running from `trades` with a stated plain query I get *0.31% vs 1.94%, 6.35×, p = 0.0072* — 515 long rows, not 512, and 10 passes, not 7. **The 1926 denominators do not reproduce.** The direction and the conclusion are unchanged and in fact stronger; the exact figures in that table should not be quoted.

---

## 4. WHAT A TRUTHFUL LABEL WOULD HAVE SAID

### 4a. The same classifier on the same daily candles

| day | close | O→C | bot's stored label | recomputed at daily close |
|---|---|---|---|---|
| 2026-08-30 | 101.70 | −3.66% | bull | **bull** |
| 2026-08-31 | 102.99 | +1.27% | bull | **bull** |
| 2026-09-01 | 99.94 | −2.96% | bull (to 18:40) | **neutral** (from 18:00 UTC) |

Hour-by-hour reconstruction across all three days: 30 Aug — `bull` in all 24 hours. 31 Aug — `bull` in all 24 hours. 1 Sep — `bull` through 17:00, `neutral` from 18:00.

🔴 **The answer on 30 and 31 Aug is still `bull`. The formula is faithful to its own definition; the question is whether that definition is the right one — and that is a question about the definition, not about the implementation.**

### 4b. 🔴 The one named alternative, tested — close vs daily EMA21 alone

Named in advance: **close relative to the daily EMA21 only, no EMA9 ordering, no slope condition.** Tested; nothing else searched.

| day | close | daily EMA21 | EMA21-only label | bot-formula label |
|---|---|---|---|---|
| 2026-08-30 | 101.70 | 91.94 | **bull** | bull |
| 2026-08-31 | 102.99 | 92.95 | **bull** | bull |
| 2026-09-01 | 99.94 | 93.58 | **bull** | **neutral** |

Over the whole 14-day window (19 Aug → 1 Sep) the EMA21-only label reads `bull` on **every single day without exception**, hour by hour included.

**The candidate is worse.** It says `bull` on all three drop days, including the one where the real classifier finally flipped. Removing the EMA9 ordering and the slope condition removes precisely the two terms that made the label respond on 1 Sep, leaving only the three-week average the operator identified as the slow one. **It is strictly slower than what is deployed.**

### 4c. What each definition does to the advisor's short pass rate — descriptive only

| definition | SHORT pass in its `bull` bucket | LONG pass in its `bull` bucket | ratio | Fisher p |
|---|---|---|---|---|
| deployed classifier (stored) | 2 / 654 = 0.31% | 10 / 515 = 1.94% | 6.35× | 0.0072 |
| deployed classifier (recomputed) | 2 / 661 = 0.30% | 10 / 503 = 1.99% | 6.57× | 0.0064 |
| **EMA21-only** | 13 / 1,184 = **1.10%** | 30 / 926 = **3.24%** | **2.95×** | **0.0009** |

The EMA21-only definition has **no `neutral` bucket at all** — every row is `bull` or `bear` — so it swallows the deployed classifier's entire neutral population into `bull`. The raw short pass rate inside `bull` rises to 1.10% only because the bucket now contains 1,184 rows instead of 661, most of them from calmer regimes. **The asymmetry does not weaken; on a larger sample it becomes more significant, not less.** No change is proposed and none was made.

---

## VERDICT

🔴 **`trend_1d` is TRUE, and slow by construction. It is not lying.**

The lag, stated as a number: **leaving `bull` costs one daily close below a 9-day EMA — 0.35 ATR away on 30 Aug — so the label ran about three days behind the first drop day and flipped to `neutral` at 18:00 UTC on 1 Sep. Reaching `bear` would require EMA9 to cross below EMA21, roughly six more days at −3%/day, and never at a flat price.** On 30 and 31 Aug the label was describing a market whose close sat 10.6% and 1.84 ATR above its 21-day mean after a 74 → 110 August. Calling that `bull` was accurate. LuxAlgo's band being red on the 1h chart is a different indicator on a different timeframe; it neither confirms nor contradicts a daily-EMA construct.

**So the 1926 report's conclusion stands — and it stands for a reason it did not name.** It said "regime, not a gate" and cited an unbroken `bull` reading. The reading was real, the asymmetry it rested on survives recomputation and strengthens (6.57×, p = 0.0064), and the label that produced it is correctly implemented. What 1926 never checked is **whether that mechanism was present on the days it was invoked to explain.**

🔴 **It was not, on two of the three.** On **30 Aug** — the biggest drop day, the day the whole question is about — **135 SHORT rows were generated and zero reached the advisor.** On **1 Sep**, 99 SHORT rows, **zero reached the advisor.** The advisor is the only consumer of `trend_1d`. On those two days the label leaned on nothing, because there was nothing in front of it: the shorts died upstream, in gates the 1926 report examined separately and cleared, and the daily regime had no part in it. Only on **31 Aug** did shorts reach the advisor — 15 of them, all skipped, 97.6% of the reasons naming the 1d label by hand, one of them stating outright that *"4h/1h/15m neutral/bear but 1d dominance rules."*

**My §4b answer was therefore right about the label and wrong about the days.** I offered a regime explanation for a three-day drought and verified it on the one day it applies. The operator was right to distrust it — not because the input was false, but because I never checked that the input was in the room.

The one substantive correction to the mechanism as 1926 described it: `trend_1d` is not "narration". It is narration **carrying a written instruction to lean** (`claude_advisor.py:146-151`), and that instruction is followed in 97.6% of short refusals versus 39.6% of long refusals. It is not a gate. It is not decorative either.

**No change is proposed. Nothing was applied.**

---

## READ-ONLY CONFIRMATION

* **DB read-only.** Every query opened `file:/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db?mode=ro` (`SQLITE_OPEN_READONLY`). SELECTs only.
* **cwd outside SOL's tree.** All analysis ran from `/tmp/claude-0/…/scratchpad` and `/root`. **SOL's config was never imported.** Candles were fetched with a standalone `ccxt.bybit` object built in the scratchpad, not from SOL's exchange handle.
* **No writes attempted.** Not to files, not to the DB — including no probe write to demonstrate the read-only mode, which would itself have been an attempt.
* **No orders placed or cancelled.** Venue traffic was exactly three public OHLCV reads (`fetch_ohlcv` 1d ×2, 1h ×2 paginated) through the local Tor SOCKS proxy on 127.0.0.1:9050. No private endpoint, no key, no `fetch_positions`, no `fetch_open_orders`.
* **Service untouched.** `mercury-sol.service` — `SubState=running`, `MainPID=1196924` (unchanged), `ActiveEnterTimestamp=Mon 2026-08-24 13:29:27 UTC`, **`NRestarts=0`, unchanged.**
* **File hashes identical.** All 33 `.py` files byte-identical before and after — `config.py` `ed7a14b0df440f2fc5040e87ea5b504b`, `main.py` `35b0201626303c730df6d1c2c3ec3f9e`, `indicators.py` `10582501821a2e7e490e1b5e88d4f463`, `claude_advisor.py` `a02ce04e6a12864bfcc0c6118137ebd7`.
* 🔴 **`trades.db`'s hash DID change** (`4c2728…` → `186a5a…`) and I am naming it rather than omitting it. **It was the live bot, not me.** `lsof` shows the file held by `gunicorn` PID **1196924** — the service's own `MainPID`. Rows **23044** and **23045** (`trend_rearmed`, `confirm_recorded`) were written at **20:00:05 UTC**, between my two hash snapshots, by the running bot's normal 5-minute scan. My connection was `mode=ro` and physically cannot write.
* **Titan not opened.** The single exception is the mandated `openitems_guard` pre-flight (`/root/titan-bot/tools/openitems_guard.py`) → **exit 0**. No other Titan file was read; nothing in `/root/titan-bot` was written.
