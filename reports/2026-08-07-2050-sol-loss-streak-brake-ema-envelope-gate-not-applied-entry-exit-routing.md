# Mercury-SOL — the loss-streak brake, the EMA-envelope gate (MEASURED, NOT APPLIED), and the entry/exit routing trace

**2026-08-07 20:50 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · PAPER · §1–§7 and §9 READ-ONLY · §8 APPLIED NOTHING**

Titan (`/root/titan-bot`, LIVE REAL MONEY) was not touched and none of its numbers were imported.
Every figure below comes from SOL's own `trades.db` (opened `mode=ro`) or from Bybit SOLUSDT-perp
candles fetched fresh through Tor — the bot's own venue — and cached locally.

---

## ⚡ THE SHORT VERSION

1. **Nothing was applied.** §5b was decisive and it was decisive *against* the gate. The both-Expanding
   EMA-envelope rule admits **0 of 9** SOL LONG entries — it cannot be measured on that side at all —
   and on SHORT it splits 8-vs-5. That is the "one side only" branch of the pre-registered rule, so the
   answer is **APPLY NOTHING**, and §8's own reasoning (nineteen Titan filters) is why.
2. **The gate would have admitted exactly the two range entries this brief is about** (vpos 27 and 28)
   and refused the one that was *not* a range entry (vpos 26). It does not see SOL's chop problem.
3. **The operator's reading of the RISK HALT cards was right in substance.** 10 cards, all LONG, all
   inside ONE 4-hour cooldown. And the brake was **wrong on this occasion**: 10 of 10 refusals were
   positive at +4h (mean **+0.84%**, unconditional baseline **+0.035%**), and the cooldown window
   itself had **|net|/range = 0.84** — a clean one-way advance, not chop. n_effective = **1**.
4. **The brake has no recency window.** Its three "consecutive" losses were closed **2026-08-03 06:40**,
   **2026-08-03 13:52** and **2026-08-07 06:00** — a span of **3.97 days**. Two of the three were four
   days stale. Per §8 the brake was **not touched**; this is reported, not changed.
5. **§9: no entry/exit confusion exists.** SOL receives **zero** EXIT-only names on 5m or 15m. The only
   EXIT-only signal in the whole system is the 1h `Exit Signal`, and `get_active_signals` explicitly
   `continue`s past `CAT_EXIT`, so it can never score. `15M: HyperWave Signal Down` is a MOMENTUM/SHORT
   **entry** signal by dictionary definition — counting it as an opposing entry vote is correct.
6. **One new defect found while measuring §4.** The same entry carries **two disagreeing ADX(1h)
   numbers**, differing by up to **+31.8 points**. Read-only finding, detail in §4.4.

---

## 1. WHAT HAPPENED OVERNIGHT

### 1.1 Positions opened since 2026-08-07 00:28: **ZERO**. Closed: **ONE**.

| vpos | side | entry | exit | R | close reason | opened (UTC) | closed (UTC) | duration |
|---|---|---|---|---|---|---|---|---|
| **28** | SHORT | 72.77 | 72.84 | **−0.153** | `exit_signal` | 2026-08-06 19:00:34 | 2026-08-07 06:00:10 | 11h 00m |

Nothing else opened. `virtual_positions` ends at id 28; there is no id 29. The book is currently
**flat** and has been since 06:00:10Z.

### 1.2 What became of vpos 28 — the full chain

| when (UTC) | event | evidence |
|---|---|---|
| 08-06 19:00:06 | 1h trend SET **SHORT** — `Smart Trail Switch Bearish` | trades#16404 `trend_set` |
| 08-06 19:00:09 | entry fired, `Bearish New Imbalance` (5m), score 2.50, advisor **execute** | trades#16405 `executed` |
| 08-06 19:00:34 | vpos 28 booked: size 137.4, margin 2000, lev 5, SL **73.75** (ATR 0.393, 2.5×), risk **$134.65** | `virtual_positions` |
| 08-06 19:25:03 | a SECOND execute verdict arrived → `observed_skipped` (already in position) | trades#16407 |
| **08-07 00:25:30** | **service restart** (`systemctl`, SIGTERM) — new API key loaded | journal |
| 08-07 00:25:50 | boot: `OBSERVATION_MODE=True`, `SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R)` | journal |
| 08-07 00:25:50 | **`[VPOS-RECONCILE] OPEN vpos=28 SHORT entry=72.77 sl=73.75 age=5.4h — poller continues managing it`** | journal |
| 08-07 04:00:15 | 1h `Exit Signal` → **exit ARMED** for SHORT (TTL 360 min) | trades#16471 `exit_armed` |
| 08-07 06:00:10 | 15m `Bullish I-CHOCH` confirmed the armed exit → closed @ 72.84 | trades#16507/16508 |

The position **survived the restart correctly**. The reconciler re-attached it by name and the poller
kept managing it; the stop was never orphaned. The `[BOOT-ASSERT] venue FLAT` line is expected — the
venue *is* flat, this is paper.

**The restart is why the operator's clock starts at 00:28.** Before it, the log carried 83 × Bybit
`retCode 10010 "Unmatched IP"` in 25 minutes (the key/IP-allowlist-vs-Tor problem from 06.08); the
bot was running on the OKX price fallback. **After the restart: 0 occurrences of 10010, from 00:25:33
right through to 20:40.** The new key is live and signing.

### 1.3 What the position actually did — measured, not narrated

Max favourable excursion **0.66%**, max adverse **0.247%**, over **11 hours**. Stop distance was
**1.35%** of price. The trade lived its entire life inside a band **half the width of its own stop**
and never came close to either side of it. It did not lose to a hostile move; it expired.

---

## 2. THE LOSS STREAK

### 2.1 The three closes that triggered it — the exact rows the gate counted

```sql
SELECT net_pnl FROM virtual_positions
 WHERE status='closed' AND net_pnl IS NOT NULL AND COALESCE(is_paper,1) = ?   -- ? = 1 (paper)
 ORDER BY closed_at DESC LIMIT 3
```

| vpos | side | net_pnl | R | is_paper | closed_at |
|---|---|---|---|---|---|
| 28 | SHORT | −20.62 | −0.153 | 1 | 2026-08-07T06:00:10.519Z |
| 27 | SHORT | −85.45 | −0.660 | 1 | 2026-08-03T13:52:21.609Z |
| 26 | LONG | −138.67 | −1.085 | 1 | 2026-08-03T06:40:01.726Z |

3 of 3 negative → `streak = 3` → cooldown = last loss **06:00:10Z + 4h = 10:00Z**. The first refusal
came **3 seconds** after the close, at 06:00:13.

### 2.2 🔴 The M7 fix is confirmed correct AND confirmed LOADED

- **Correct book.** `main.py` `_risk_check` reads `virtual_positions` filtered on
  `COALESCE(is_paper,1) = ?`, with `_streak_book = 1 if OBSERVATION_MODE else 0`. It is **not**
  reading `trades`, and it is **not** unfiltered.
- **Loaded, not merely on disk.** `main.py` mtime **2026-08-06 15:46:27**; `main.cpython-312.pyc`
  **2026-08-06 15:50**; the running worker (pid 2854383) **booted 2026-08-07 00:25:50** — after both.
  The code that produced the refusal string is the code on disk.
- **`ORDER BY closed_at` is right, and it matters here.** By `id` the order would be 26, 27, 28; by
  `closed_at` it is 26, 27, 28 as well *this time*, but 26 (opened 08-02) closed **before** 27 (opened
  08-03) — the ordering is doing real work.
- **The live book is empty** (`COUNT(*) WHERE COALESCE(is_paper,1)=0` → **0**), so on the flip
  `len(rows) >= 3` is false and this gate cannot halt the first live trade on paper history. The M7
  claim holds.
- **The old query would have returned the same three losses** (`trades` rows 16508, 15473, 15404) —
  so on this occasion the fix changed nothing observable. That is not an argument against it; it is
  the accident the M7 note already described.

### 2.3 🔴 What the gate is NOT checking: recency

`LIMIT 3 ORDER BY closed_at DESC` has **no age filter**. The three losses span
**2026-08-03 06:40 → 2026-08-07 06:00 = 3.97 days**. Two of them were four days old and had already
been followed by a full trading week. The brake's implicit premise — *"three losses in a row means
conditions right now are hostile"* — was not true here: it was two stale losses plus one fresh one.

**Per §8 this was not touched.** It is recorded as the mechanism to look at *if* the brake is ever
revisited, and it is a different defect from the one §6 tests.

---

## 3. THE FUNNEL

**Window A — 2026-08-06 19:00Z → 2026-08-07 12:00Z** (from the vpos-28 entry to the NFP halt),
**Window B — 2026-08-07 00:00Z → 12:00Z** (the operator's overnight).

| where the signal died | A: n | A: LONG / SHORT | B: n | B: LONG / SHORT |
|---|---|---|---|---|
| **cascade** (`htf_blocked`) | 64 | 40 / 24 | 28 | 7 / 21 |
| **score bar** (`below_threshold`) | 24 | 5 / 19 | 24 | 5 / 19 |
| **advisor** (`ai_skipped`) | 8 | 4 / 4 | 7 | 4 / 3 |
| **risk halt** (`risk_halt`) | **10** | **10 / 0** | **10** | **10 / 0** |
| already in position (`observed_skipped`) | 5 | 0 / 5 | 1 | 0 / 1 |
| no 1h trend (`no_trend`) | 17 | — | 17 | — |
| context / confirm / trend rows | 27 | — | 18 | — |
| entry suppressed, exit armed | 1 | — | 1 | — |
| **executed** | **1 entry + 2 exit rows** | 0 / 1 | 0 entries | — |

Mean scores of the directional candidates in window B: `htf_blocked` SHORT **−7.39**, LONG **−6.14**
(the −10.0 HTF penalty dominating); `below_threshold` SHORT **−0.31**, LONG **+0.77**;
`ai_skipped` LONG **+3.81**, SHORT **+2.67**; **`risk_halt` LONG +4.79** — *the highest-scoring
refusal bucket of the night*, including two at 6.79 and **7.54**.

**The cascade is by far the biggest killer** (28 of 79 directional candidates in window B), and the
risk halt is fourth by count but first by candidate quality.

---

## 4. 🔴 WERE THOSE THREE LOSSES RANGE ENTRIES?

Measured independently of every label the bot assigns. **`market_regime` was not used.**

**Definitions (stated so the numbers travel with their provenance):**
- **Candles**: Bybit SOLUSDT perp (the bot's own venue), fetched via Tor 2026-08-07, cached locally.
  2373 × 1h, 9490 × 15m, 28470 × 5m from 2026-05-01.
- **ADX**: Wilder ADX(14) computed over the **200 CLOSED 1h bars before the entry bar** (the entry bar
  itself excluded — it had not closed when the entry fired).
- **ER**: Kaufman efficiency ratio `|net| / Σ|Δ|`. 4h from **48 × 5m** closes; 12h from **48 × 15m**
  closes — equal increment counts so the two are comparable.
- **ATR**: Wilder ATR(14) on 1h at entry ÷ the median of the same series over the prior **14 days**
  (336 bars).
- **pos in 24h**: `(price − low₂₄ₕ) / (high₂₄ₕ − low₂₄ₕ)` over the 24 closed 1h bars before entry.

### 4.1 The three

| | vpos 26 LONG (08-02 05:00) | vpos 27 SHORT (08-03 06:45) | vpos 28 SHORT (08-06 19:00) |
|---|---|---|---|
| R | −1.085 | −0.660 | −0.153 |
| **ADX(1h, w200)** | **29.9** (73rd pct of book) | **15.5** (5th pct) | **13.2** (**lowest in the entire book**) |
| ER 4h | **0.451** (86th pct — most directional 4h in the book) | 0.223 (45th) | 0.217 (41st) |
| ER 12h | 0.192 (36th) | 0.271 (68th) | 0.257 (64th) |
| ATR / 14d median | 0.83× (23rd) | 0.75× (14th) | 0.95× (64th) |
| 24h range width | 4.07% (55th) | **2.32% (5th — narrowest)** | 2.64% (14th) |
| **pos in 24h range** | **0.99 — at the very top** | 0.15 — near the low | **0.06 — at the very bottom** |

### 4.2 The verdict, entry by entry

- **vpos 27 — YES, a range entry.** ADX 15.5 (5th percentile), the **narrowest 24h range in the book**
  (2.32%), shorting near the bottom of it. Every measure agrees.
- **vpos 28 — YES, and the most extreme in SOL's history.** ADX **13.2**, the lowest of all 22 entries;
  24h range 2.64% (14th percentile); shorting at **0.06** of that range — i.e. at the low. It then
  spent 11 hours inside a 0.9% band. This is the textbook case.
- **vpos 26 — NO.** ADX 29.9 is the 73rd percentile and ER(4h) **0.451** is the 86th — the *most*
  directional 4-hour tape in the whole book. What killed it was not chop: it was a LONG opened at
  **0.99 of the prior 24h range**, i.e. buying the exact top, into a move that had already run.

**So: two range entries and one top-of-range trend chase.** Not three of a kind. Which matters, because
any gate proposed as the fix has to catch the first two — see §5.

### 4.3 Cross-check on the measurement itself

My independent ADX(1h,200) reproduces the bot's own recorded `srv_adx_1h` closely across all 22 entries
(e.g. vpos 28: mine 13.2, bot 14.1; vpos 12: mine 39.5, bot 37.2; vpos 9: 39.3 vs 40.1). The
measurement is not an artefact of my pipeline.

### 4.4 🔴 NEW FINDING — one entry, two ADX numbers, disagreeing by up to 31.8 points

Every closed position carries **two** ADX(1h) figures for the same instant, and they do not match:

| vpos | `virtual_positions.entry_adx_1h` | `trades.srv_adx_1h` | difference |
|---|---|---|---|
| 21 | 60.8 | 28.9 | **+31.8** |
| 8 | 51.4 | 30.3 | +21.1 |
| 16 | 47.9 | 27.0 | +21.0 |
| **28** | **34.1** | **14.1** | **+20.0** |
| 26 | 45.8 | 29.3 | +16.5 |
| … | | | 16 of 22 biased HIGH |

**Cause, located.** `virtual_trader._recheck_fetch_1h_metrics` fetches
`fetch_ohlcv(symbol, '1h', limit=ATR_LEN * 3)` = **42 bars**. `indicators.fetch_snapshot` (which fills
`srv_adx_1h`) uses `CANDLE_LIMIT` = **200 bars**. Wilder ADX is doubly smoothed and does not converge
in 42 bars; the short fetch is systematically biased **upward**. `ATR%` from the same two paths agrees
to three decimals — so it is not a candle-source problem, it is a warm-up problem specific to ADX.

`CANDLE_LIMIT`'s own comment says *"Both 100 and 200 far exceed warmup, so values are stable"* — true,
and the recheck path is the one place that ignores it.

**Why it matters here:** the recheck tiers, which decide whether to tighten a stop, read
`entry_adx_1h`. On vpos 28 they were told **ADX 34** on a tape whose real ADX was **13** — they were
told "strong trend" while standing in the flattest tape SOL has ever traded. This is the
"one fact, several judges" class. **Read-only finding; nothing changed** — it is outside §8's scope.

---

## 5. 🔴 THE EMA-ENVELOPE GATE, MEASURED ON SOL'S OWN BOOK

Source for §5a/b/c: the entry row's **own recorded** `ema_gap_dir_1h` / `ema_gap_dir_15m`
(`indicators._ema_gap_fields`: `|EMA9−EMA21|/EMA21`, compared against the same gap `SLOPE_LOOKBACK=3`
bars earlier, `Flat` band ±5%). No re-derivation, no substitution.

### 5a — the three entries

| vpos | side | `ema_gap_dir_1h` | `ema_gap_dir_15m` | strong-form verdict |
|---|---|---|---|---|
| **26** | LONG | Expanding (0.270%) | **Flat** (0.474%) | **REFUSED** |
| **27** | SHORT | Expanding (0.154%) | Expanding (0.204%) | **ADMITTED** |
| **28** | SHORT | Expanding (0.369%) | Expanding (0.196%) | **ADMITTED** |

**The gate refuses exactly the wrong one.** It stops vpos 26 — the entry §4 measured as *not* a range
entry — and waves through vpos 27 and 28, the two the whole brief is about, including the lowest-ADX
entry in SOL's history. If the gate had been live last night, the loss streak still happens; only the
order of the three losses changes.

### 5b — 🔴 THE WHOLE CLOSED BOOK, SPLIT BY THE GATE, PER SIDE

22 closed positions; vpos 8 has a NULL `ema_gap_dir_15m` and cannot be evaluated → **n = 21**.

| cohort | n | win rate | ΣR | median R | mean R | vpos |
|---|---|---|---|---|---|---|
| **ALL — admitted** | 8 | 50.0% | **−0.112** | −0.074 | −0.014 | 11,14,17,19,20,25,27,28 |
| **ALL — refused** | 13 | 30.8% | −4.523 | −1.049 | −0.348 | 7,9,10,12,13,15,16,18,21,22,23,24,26 |
| **LONG — admitted** | **0** | — | — | — | — | **(none)** |
| **LONG — refused** | 8 | 25.0% | −3.307 | −1.056 | −0.413 | 7,9,12,16,18,21,22,26 |
| **SHORT — admitted** | 8 | 50.0% | −0.112 | −0.074 | −0.014 | 11,14,17,19,20,25,27,28 |
| **SHORT — refused** | 5 | 40.0% | −1.216 | −0.577 | −0.243 | 10,13,15,23,24 |

**Read the LONG row again. n = 0.** Not "a small sample" — *no SOL LONG entry has ever satisfied both
legs of this condition*, across 52.8 days and 9 LONG entries. On the LONG side this is not a filter
with unknown value; it is **`if side == LONG: refuse`** wearing an indicator's clothes.

On SHORT, the direction of the split is the hoped-for one (ΣR −0.11 admitted vs −1.22 refused), but
the whole SHORT book is **13 trades**, split 8/5, and **both halves are net negative**. The separation
is one 8-trade cell against one 5-trade cell.

**This is precisely §8's "one side only" branch.**

### 5c — WIDTH and DIRECTION measured SEPARATELY

**DIRECTION alone, 1h:**

| | LONG | SHORT |
|---|---|---|
| Expanding | n=4, ΣR **+0.215**, mean +0.054 | n=10, ΣR **−1.022**, mean −0.102 |
| Flat | n=3, ΣR −2.473 | n=1, ΣR +1.337 |
| Contracting | n=1, ΣR −1.049 | n=2, ΣR −1.643 |

**DIRECTION alone, 15m:**

| | LONG | SHORT |
|---|---|---|
| Expanding | n=2, ΣR **−2.209**, mean −1.105 | n=11, ΣR −0.419, mean −0.038 |
| Flat | n=4, ΣR +0.215 | n=1, ΣR −1.050 |
| Contracting | n=2, ΣR −1.313 | n=1, ΣR +0.140 |

**The 1h and 15m legs point in opposite directions on LONG.** 1h-Expanding LONG is the book's *best*
LONG cell (+0.054 mean); 15m-Expanding LONG is its *worst* (−1.105 mean, 0/2 wins). Requiring both is
requiring two conditions that disagree with each other on this side of the book.

**WIDTH alone (terciles: 1h at 0.314 / 0.686 %, 15m at 0.186 / 0.474 %):**

| 1h width | LONG | SHORT | | 15m width | LONG | SHORT |
|---|---|---|---|---|---|---|
| narrow | n=2, ΣR −2.134 | n=6, ΣR **+0.281** | | narrow | n=3, ΣR −1.925 | n=5, ΣR **+1.430** |
| middle | n=4, ΣR −2.998 | n=3, ΣR −1.273 | | middle | n=3, ΣR −2.398 | n=4, ΣR −1.933 |
| wide | n=2, ΣR **+1.825** | n=4, ΣR −0.336 | | wide | n=2, ΣR +1.016 | n=4, ΣR −0.825 |

Width is **non-monotone on every one of the four side × timeframe combinations** — best at both ends,
worst in the middle. Titan found direction carried the separation and width did not; **on SOL neither
carries it.** Every cell here is n ≤ 6.

### 5d — VOLUME COST

| population | n | admitted | refused |
|---|---|---|---|
| executed entries, whole book | 22 | 8 | **14 (63.6%)** |
| executed entries, last 30 days | 14 | 6 | 8 (57.1%) |
| all LONG candidates with a full indicator set, whole book | 1487 | 295 | **80.2%** |
| all SHORT candidates with a full indicator set, whole book | 1789 | 405 | **77.4%** |
| all LONG candidates, last 30 days | 926 | 158 | **82.9%** |
| all SHORT candidates, last 30 days | 1145 | 244 | **78.7%** |

At entry level the gate takes SOL from **22 entries / 52.8 days = 0.42 per day** to
**8 / 52.8 = 0.15 per day** — one entry per 6.6 days, and **zero LONG entries, ever**.

It also refuses the book's **two largest winners**: vpos 7 (**+2.089R**) and vpos 13 (**+1.337R**),
worth 3.43R between them, keeping only vpos 11 (+1.133R) and 25 (+1.257R).

---

## 6. 🔴 IS THE BRAKE COSTING GOOD ENTRIES?

### 6a — every loss-streak refusal that has ever fired

**10 refusals. All LONG. All inside ONE cooldown window.** Not three halts — one.

| trades# | UTC | side | price | score | 5m trigger |
|---|---|---|---|---|---|
| 16509 | 06:00:13 | LONG | 72.84 | 5.00 | Within Bullish OB |
| 16513 | 06:05:05 | LONG | 72.85 | 3.25 | Within Bullish OB |
| 16514 | 06:10:05 | LONG | 72.86 | 5.00 | Within Bullish OB |
| 16517 | 06:15:09 | LONG | 72.93 | 3.25 | Within Bullish OB |
| 16519 | 06:20:05 | LONG | 72.98 | 3.25 | Bullish OB Mitigated |
| 16529 | 07:15:05 | LONG | 72.94 | 5.75 | Bullish New Imbalance |
| 16541 | 09:10:08 | LONG | 73.27 | 3.14 | Bullish New Imbalance |
| 16546 | 09:40:02 | LONG | 73.65 | 6.79 | Within Bullish OB |
| **16547** | 09:40:02 | LONG | 73.65 | **7.54** | Bullish S-CHOCH |
| 16548 | 09:50:02 | LONG | 73.65 | 4.89 | Within Bullish OB |

All ten carry `error = 'loss streak 3/3 — cooldown until 10:00Z'` and all ten are registered in
`skip_attribution` with drift tracking — **yesterday's M7/attribution work is what made this section
possible at all.** Before 2026-08-01, 289 of 289 `risk_halt` rows carried no reason.

For completeness, the only other `risk_halt` rows in history: two `position-cap check failed
(fail-closed)` (08-02, Bybit timestamp error and a Tor fetch failure) and one `macro halt: NFP 19m in
(blackout ±30m)` (08-07 12:10).

### 6b — forward drift, signed toward the refused side (+ = the refused LONG would have been right)

| trades# | +1h | +4h | +12h | observatory +1h / +4h / +12h |
|---|---|---|---|---|
| 16509 | −0.014% | **+1.181%** | +0.851% | −0.165 / +1.098 / +0.755 |
| 16513 | +0.082% | +1.057% | +0.851% | −0.041 / +1.153 / +0.810 |
| 16514 | +0.000% | +0.919% | +0.754% | +0.096 / +1.029 / +0.837 |
| 16517 | −0.069% | +0.809% | +0.754% | +0.014 / +0.919 / +0.809 |
| 16519 | −0.041% | +0.726% | +0.630% | −0.082 / +0.781 / +0.740 |
| 16529 | +0.027% | +0.782% | +1.111% | +0.000 / +0.795 / +0.946 |
| 16541 | +0.327% | +0.559% | — | +0.478 / +0.764 / — |
| 16546 | −0.231% | +0.733% | — | −0.244 / +0.801 / — |
| 16547 | −0.231% | +0.733% | — | −0.244 / +0.801 / — |
| 16548 | −0.068% | +0.924% | — | −0.231 / +0.801 / — |

My candle-derived figures and the bot's own `skip_drift_samples` agree within ~0.1% throughout
(different sampling instants, same conclusion).

| | +1h | +4h | +12h |
|---|---|---|---|
| **loss-streak refusals** | mean −0.022%, **3/10 positive** | mean **+0.842%**, **10/10 positive** | mean **+0.825%**, 6/6 positive |

**De-confound 1 — the unconditional baseline** (every 6th 5m bar over the same 60-day tape, LONG sign):

| horizon | n | mean | median | % positive | sd |
|---|---|---|---|---|---|
| +1h | 2919 | +0.009% | +0.000% | 49.4% | 0.589 |
| +4h | 2913 | **+0.035%** | +0.013% | 50.2% | 1.149 |
| +12h | 2897 | +0.108% | +0.051% | 51.3% | 1.823 |

The +4h refusal mean of **+0.842%** is **+0.70 sd** above the unconditional mean, and 10/10 positive
against a 50.2% base rate.

**De-confound 2 — same day, same side, other causes** (2026-08-07, LONG):

| cause | +1h | +4h | +12h |
|---|---|---|---|
| `ai_skipped` (n=13/9/4) | −0.054% | **−0.175%** | +1.438% |
| `below_threshold` (n=14/14/3) | +0.071% | +0.063% | +1.017% |
| `htf_blocked` (n=14/8/1) | +0.232% | +0.201% | +1.805% |
| **`risk_halt`** (n=10) | −0.022% | **+0.842%** | +0.825% |

**De-confound 3 — whole book, LONG refusals by cause, 60 days:**

| cause | n | +1h | +4h | +12h |
|---|---|---|---|---|
| `ai_skipped` | 1514 | −0.016% (47% pos) | +0.019% (49%) | +0.132% (54%) |
| `below_threshold` | 922 | −0.006% (49%) | +0.112% (51%) | +0.014% (51%) |
| `htf_blocked` | 2419 | +0.032% (52%) | −0.109% (45%) | −0.224% (45%) |
| **`risk_halt`** | **12** | +0.019% (33%) | **+0.826% (100%)** | **+0.780% (100%)** |

The risk-halt row stands out against every comparison — the baseline, its same-day peers, and the
60-day per-cause history. **But see §6d before drawing a conclusion from it.**

### 6c — 🔴 THE COOLDOWN ITSELF (real 5m candles, 06:00:10Z → 10:00:10Z)

| | |
|---|---|
| start close | 72.83 |
| high / low | 73.72 / 72.70 |
| **range traversed** | **1.02 (1.40% of start)** |
| **net move** | **+0.86 (+1.18%)** |
| **\|net\| / range** | **0.84** |
| max favourable for a refused LONG | **+1.22%** |
| max adverse for a refused LONG | **+0.18%** |

**`|net|/range = 0.84` is not chop.** It is a one-way advance that gave back 16% of its own travel. The
brake's premise on this occasion — *"three losses in chop means more chop"* — was false: **the squeeze
resolved upward inside the cooldown, and the brake was switched off precisely then.** That is the
failure mode the brief predicted, observed once, exactly as described.

**But did the refused trades have a trade in them?** Book median initial stop distance is **2.079%**
of price (range 1.007–3.932%). Checking each refused LONG against a symmetric ±1R over the next 12h:

> **All 10: neither +1R nor −1R reached within 12 hours.**

So the honest accounting is: the brake refused into a **real +1.2% directional move with a 0.18%
drawdown** — an entry that would have gone right immediately and been comfortable — but **not** into a
1R winner. The realistic outcome is a small positive scratch or a trailed partial, not a clean win.
The brake cost something. It did not cost a lot.

**Contrast — the other risk-halt causes:** `position-cap fail-closed` LONG (08-02) +1.295% at 4h;
same, SHORT (08-02) −0.328%; `macro halt` NFP LONG (08-07) +0.189%. No pattern; n=3.

### 6d — 🔴 IS n BIG ENOUGH? **NO. n_effective = 1.**

The brief asked directly and the answer is unambiguous:

- **10 refusals, but ONE cooldown window**, one day, one side, one price move. The ten rows are ten
  samples **of the same four hours**. Their +4h drifts are 0.559–1.181% because they are ten
  overlapping views of a single +1.18% advance.
- **The brake has fired exactly once in its entire life** (first ever: 2026-08-07 06:00:13).
- Three loss-streak *episodes* would not be a sample. **One episode is not evidence** — it is an
  anecdote with ten rows.

**Conclusion for §6: the brake was wrong on 2026-08-07, and one instance of being wrong is not grounds
to change it.** Per §8 it was not touched. The review point is **refusal episodes, not refusal rows**:
revisit at **5 distinct cooldown windows**, not at 50 more rows from one.

---

## 7. THE HONEST SUMMARY

**Were the three losses a range problem, a regime problem, or ordinary variance?**

**Two of the three were a genuine range problem, and the third was not.** vpos 27 (ADX 15.5, narrowest
24h range in the book) and vpos 28 (ADX 13.2 — the lowest of 22 entries — 11 hours inside a band half
its own stop width) are as clean a pair of chop entries as SOL's book contains. vpos 26 was the
opposite: the most directional 4h tape in the book (ER 0.451, 86th percentile), lost by buying at
**0.99 of the prior 24h range**. That is a *placement* error, not a regime error.

And the sizes matter. −1.085R, −0.660R, −0.153R. Two of the three were **less than a full R**. A
"streak" whose total damage is **−1.90R over four days** is well inside ordinary variance for a book
whose all-time record is −5.37R over 22 trades. The streak counter fired on the *count*, not on the
damage — three closes with a minus sign, two of them scratches, two of them four days old.

**Does SOL's OWN book support a flat gate?**

**Not this one, and not yet any one.**

- The both-Expanding EMA envelope admits **0 of 9 LONGs** — it is a side ban, not a filter.
- On SHORT it is 8-vs-5, both halves negative.
- Its two legs **contradict each other on LONG** (1h-Expanding is the best LONG cell, 15m-Expanding is
  the worst).
- Width is non-monotone in all four side × TF cells.
- And decisively: **it admits both of the actual range entries and refuses the one that wasn't.**

What SOL's book *does* say, with a real n, is that the measurements in §4 separate where the envelope
does not — ADX(1h,200) at 13.2 and 15.5 for the two chop entries versus a book median of 25.7, and 24h
range width at the 5th and 14th percentiles. **A flat gate built on ADX and range width would have
refused vpos 27 and 28 and admitted vpos 26 — the correct three answers.** That is a hypothesis with
2 supporting cases, not a filter. It is the thing worth measuring next, and it is not the thing this
brief authorised applying.

**On the operator's two observations:**

1. **The cards say REFUSED, and he is right anyway.** The 10 RISK HALT cards are the bot being stopped,
   not entering. But the deeper reading holds on both counts: the brake **is** a blunt instrument (it
   counted a −0.153R scratch and two four-day-old losses as a "streak"), and it **is** blind in both
   directions — it fired into a +1.18% clean advance, and it has no flat filter behind it to have
   prevented the chop entries in the first place. SOL has no flat gate; Titan does. That gap is real.
   What is *not* supported is closing it with Titan's EMA envelope.
2. **Exit signals are not being routed as entries.** §9 traces it end to end and finds no such path.

---

## 8. APPLY — **NOTHING WAS APPLIED**

The rule was fixed before the numbers arrived:

> §5b shows nothing, or one side only → **APPLY NOTHING and say so.**

§5b shows **one side only, and that side has n=0 admitted.** The LONG branch cannot be measured; the
SHORT branch is 8 versus 5 with both halves negative. **No file in `/mnt/volume_nyc1_1780480650620/mercury-sol`
was modified. No config flag was added. No restart was performed. No `.bak` was needed.**

Nineteen filters died on Titan for exactly this reason. This would have been the twentieth, and worse
than the nineteen, because on SOL's book it does not even do the thing it claims — it admits the chop
and refuses the trend.

**The pre-registration is recorded anyway**, as the evidence *against* the gate and as the baseline for
whatever is measured next:

| pre-registered metric | value |
|---|---|
| refusal rate, LONG | **100.0%** (0 of 9 closed LONG entries admitted; 80.2% of all LONG candidates) |
| refusal rate, SHORT | 38.5% of closed SHORT entries (5 of 13); 77.4% of all SHORT candidates |
| entries/day now | 0.42 (22 over 52.8 days) |
| entries/day after the gate | **0.15** — one per 6.6 days, and **zero LONG entries ever** |
| which of the last 25 entries it refuses | **14 of 22** (the book has 22, not 25): trades# 1920, 3225, 3437, 3685, 4259, 4370, 7815, 8446, 9842, 11181, 11679, 13644, 13973, 15093 |
| …including | vpos 7 (**+2.089R**) and vpos 13 (**+1.337R**) — the two largest winners in the book |
| review point | **not applicable — not applied.** Had it landed: 40 refusal ROWS per side, whichever comes later |

**The loss-streak brake was NOT touched**, as instructed. It is the last line of defence, not a filter.
Its no-recency-window behaviour (§2.3) and its single wrong firing (§6) are recorded for the operator,
not acted on.

---

## 9. ARE ENTRY AND EXIT SIGNALS EVER CONFUSED? (read-only)

### 9a — every 5m and 15m alert name SOL receives, split ENTRY-capable / EXIT-only

**Where the split is defined — there are THREE definitions, not one:**

1. **`signal_matrix.SIGNAL_DICTIONARY`** (`signal_matrix.py:57`) — `name → (category, direction, cid,
   weight)`. Categories: `TREND`(1h) `MOMENTUM`(15m) `LIQUIDITY`(5m) `EXECUTION`(5m) `EXIT` `UNKNOWN`.
   Only `CATEGORIES = (TREND, MOMENTUM, LIQUIDITY, EXECUTION)` can score.
2. **`state_machine._GROUP_B_RE`** (`state_machine.py:68`) — a **regex** on the raw name:
   `\bexit\b | take[\s-]?profit | stop[\s-]?loss | \btp\b | \bsl\b` → "Group B", management/exit.
3. **`signal_matrix.EXIT_CONFIRMATION_CIDS`** (`signal_matrix.py:139`) — 14 canonical ids
   (S-CHOCH ±, I-CHOCH ±, S-BOS, I-BOS, Liquidity Grab, bull and bear) that **confirm an armed exit**.

**The 5m inventory — 33 distinct names, all ENTRY-capable, ZERO exit-only:**

`Within Bearish OB` (3696), `Within Bullish OB` (3316), `Bearish OB Entered` (852), `Bullish OB
Entered` (835), `Bearish Liquidity Grab` (414), `Bullish Liquidity Grab` (390), `Bullish New
Imbalance` (379), `Bullish OB Created` (372), `Bearish OB Created` (371), `Bullish Imbalance
Mitigated` (363), `Bearish New Imbalance` (350), `Bearish Imbalance Mitigated` (336), `Bullish OB
Mitigated` (319), `Bearish OB Mitigated` (316), `Bullish Breaker` (314), `Bearish Breaker` (311),
`Broken Downtrendline` (242), `Broken Uptrendline` (226), `Bearish I-BOS` (163), `Bullish I-BOS`
(161), `Equal Highs` (119), `Bullish I-CHOCH` (113), `Equal Lows` (111), `Bearish I-CHOCH` (110),
`Bearish I-CHOCH+` (102), `Bullish I-CHOCH+` (100), `Bullish S-BOS` (37), `Bearish S-BOS` (24),
`Bearish S-CHOCH` (23), `Bullish S-CHOCH` (19), `Bullish S-CHOCH+` (16), `Bearish S-CHOCH+` (11),
plus `Equal Highs (EQH)` (4) and `Equal Lows (EQL)` (3) — **not in the dictionary** (see 9b).

**The 15m inventory — 22 distinct names, all ENTRY-capable, ZERO exit-only:**

`HyperWave Signal Up` (452), `HyperWave Signal Down` (440), `Reversal Down` (99), `Reversal Up` (97),
`HyperWave OB Signal Down` (97), `HyperWave OS Signal Up` (85), `Bearish I-BOS` (62), `Bullish I-BOS`
(59), `Bullish Divergence` (45), `Bearish Divergence` (43), `Bullish I-CHOCH` (42), `Bearish I-CHOCH+`
(39), `Reversal Down +` (38), `Bearish I-CHOCH` (36), `Reversal Up +` (34), `Bullish I-CHOCH+` (32),
`Bullish S-BOS` (10), `Bullish S-CHOCH` (8), `Bearish S-CHOCH+` (7), `Bearish S-CHOCH` (6),
`Bullish S-CHOCH+` (4), `Bearish S-BOS` (4).

**EXIT-only names in the entire system: exactly ONE — `Exit Signal`, on 1h**, category `EXIT`,
direction `NEUTRAL`, weight **0.0**.

**Can a name appear in both? YES — 14 of them, by design.** The BOS/CHOCH/Liquidity-Grab family are
`EXECUTION`/`LIQUIDITY` **entry** signals *and* members of `EXIT_CONFIRMATION_CIDS`. `Bullish I-CHOCH`
is what opened positions and it is what closed vpos 28 last night. Which role it plays depends on
**whether the opposite side is armed** — not on the name.

### 9b — 🔴 can an EXIT signal reach the entry cascade or the score matrix? **Traced: no.**

**Route 1 — the 1h `Exit Signal`.**
- JSON path: `webhook()` → `task == 'exit'` → `_handle_exit_signal` (`main.py:5163`) — a dedicated
  branch that never reaches `_handle_5m_trigger`.
- Plain-text path: `classify_group` checks `_GROUP_B_RE` **first**, matches `\bexit\b` → Group **B** →
  `reset_1h_trend` + `trend_reset` row. Group B on 5m goes to `_handle_5m_close`, never to the trigger.
- **Score isolation, verified in code:** `get_active_signals` (`signal_matrix.py:251`) does
  `if cat == CAT_EXIT: continue`. Even though `record_signal` writes `exit_signal` into
  `live_context_state` (it is there right now, `last_seen 2026-08-07T12:00:09Z`), it is dropped before
  scoring and `CAT_EXIT` is not in `CATEGORIES`. **Two independent barriers.**

**Route 2 — the dual-role BOS/CHOCH/LiqGrab names.** `_handle_plain_text` (`main.py:4556-4571`)
classifies *purely* (no `record_signal`) and skips the matrix write in two cases —
**GUARD B**: any exit-confirmation on 15m; **GUARD A**: a 5m exit-confirmation while the opposite side
is armed. So a name acting as an exit-confirmation **never** contributes to the entry score. When
nothing is armed, a 15m exit-confirm is dropped entirely as `exit_unarmed_noop` (8 such rows in the
last two days) and a 5m one is suppressed as `entry_suppressed_armed` (1 row, 08-07 05:50:06).

**Route 3 — an UNRECOGNISED name.** `classify()` is a strict case-insensitive literal lookup;
a miss returns `(UNKNOWN, NEUTRAL, 'unknown:<name>', 0.0)`. Then:
- `classify_group` falls back to **regex**: exit-words → B; else bull/bear words → **A**;
- `parse_direction` falls back to **regex**: bull → LONG, bear → SHORT.

> 🔴 **So yes — an unrecognised name carrying a directional word, arriving on `?tf=5m`, is routed
> straight into `_handle_5m_trigger`, the entry path.** Its score contribution is **0.0** (UNKNOWN is
> not in `CATEGORIES`), so it cannot lift a candidate over the bar by itself — but it *is* treated as a
> trigger.

**Has it ever happened? No.** All 7 unknown alerts in history were `Equal Highs (EQH)` / `Equal Lows
(EQL)` — they carry no bull/bear word, so `classify_group` returned `None` and all 7 landed in
`unparsed`. The mechanism is a latent hazard, not a live one.

**One more default worth naming:** in the JSON path, `tf = tf_arg or action_to_tf.get(mapped_action,
'5m')` (`main.py:5179`) — **the fallback timeframe is `'5m'`, the entry tier.** Today every entry in
`_TASK_TO_ACTION` maps into one of the three actions that `action_to_tf` covers, so the default is
unreachable. It is one new task name away from being reachable, and it defaults toward the entry path
rather than away from it.

### 9c — the same-second pair: CONFIRMED, and it was **14:55:06 UTC**, not 09:55

The pair the operator saw is `trades#16611` / `#16612` at **2026-08-07 14:55:06 UTC** (09:55 in his
local UTC−5). No pair matching that description exists at 09:55 UTC on any day.

| | #16611 | #16612 |
|---|---|---|
| name | `Bullish OB Entered` | `Bullish Liquidity Grab` |
| `signal_time` | 14:55:06.**173**336Z | 14:55:06.**330**476Z |
| score | 4.50 | 7.00 |
| verdict | skip (conf 0.78) | skip (conf 0.78) |
| reason | *"15m OPPOSES (HyperWave DOWN vs LONG entry); 1d/4h NEUTRAL; 5m BEAR. Weak MTF alignment (1/4). Skip."* | identical |
| model | claude-haiku-4-5-20251001 | claude-haiku-4-5-20251001 |
| `ai_verdict_reuse_json` | **`{"reused":1, "age_s":0.0, "from_5m":"Bullish Liquidity Grab", "from_at":"…14:55:18.560Z", "rendered_user_prompt":"…"}`** | **NULL** |

**Confirmed on all three counts:**
1. **Two DIFFERENT names** — exactly the normal LuxAlgo multi-fire on one bar close.
2. **157 ms apart** — inside the 60–100 ms band measured on 2026-08-06, same phenomenon.
3. **ONE model call.** `#16612` made it (completing 14:55:18.560Z); `#16611` consumed the **reused**
   verdict at `age_s = 0.0`. The reuse row carries the full `rendered_user_prompt` so the reused
   decision is auditable, not merely asserted. The dedup mechanism from 06.08 is working.

### 9d — 🔴 does the 15m tier carry an EXIT-only name into the entry tally? **No. The card is correct.**

The rendered prompt from that consultation, quoted verbatim:

```
15m: HyperWave Signal Down (direction: SHORT, set 40m ago)
...
Tier agreement vs LONG (computed for this consultation):
  1H: Trend Catcher Up -> LONG = AGREES
  15m: HyperWave Signal Down -> SHORT = OPPOSES
  5m trigger: Bullish OB Entered -> LONG = AGREES
```

`HyperWave Signal Down` is `('HyperWave Signal Down': (CAT_MOMENTUM, SHORT, 'hw_signal_down', 0.7))` —
a **15m momentum entry signal with a SHORT direction**. It is:

- **not** in `EXIT_CONFIRMATION_CIDS` (that set is BOS/CHOCH/Liquidity-Grab only);
- **not** matched by `_GROUP_B_RE` (no exit/TP/SL token);
- **not** category `EXIT`;
- and in `engine_15m.py` it maps to `HW_SIGNAL_SHORT` for **weight learning only** — that path adjusts
  a learnable subtype weight and never routes an exit.

**The distinction the brief draws is the right one** — *"exit the long"* and *"enter the short"* are
different claims — **and SOL never has to make it on 15m**, because it receives no 15m exit-only names
at all. The only thing that can say "exit the long" is the 1h `Exit Signal`, which arms and never votes.

Where SOL *does* fold the two claims together is by design: the 15m tier is the momentum-confirmation
tier, and a SHORT momentum reading counts against a LONG entry. That is a design choice about
confluence, correctly implemented, not a routing bug.

---

## APPENDIX — provenance

| item | source |
|---|---|
| positions, refusals, drift | `/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db`, opened `file:…?mode=ro` |
| candles | Bybit SOLUSDT perp via Tor (`socks5h://127.0.0.1:9050`), 2026-08-07; 2373×1h, 9490×15m, 28470×5m from 2026-05-01 |
| restart / key errors | `journalctl -u mercury-sol` |
| deployment proof | `main.py` mtime 2026-08-06 15:46:27 · `main.cpython-312.pyc` 15:50 · worker pid 2854383 booted 2026-08-07 00:25:50 |
| Titan | **not read, not touched, no numbers imported** |
| files modified in `/mnt/volume_nyc1_1780480650620/mercury-sol` | **none** |
