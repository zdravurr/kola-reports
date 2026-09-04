# Mercury-SOL — the macro news blackout, measured for the first time

**2026-09-04 13:35 UTC · READ-ONLY audit · no change proposed, none applied**

> **CONTROLS DECLARED BEFORE ANY RESULT WAS READ.** 67 cells are tested in this
> document (16 independent-cut cells, 15 serial-cut cells, 2 headlines, 34 volatility
> buckets). Bonferroni α = 0.05/67 = **0.00075**. The serial population is **n = 7**;
> the smallest two-sided sign-test p attainable at n = 7 — all seven the same sign —
> is 0.0156. **No cell in this study can reach significance at any split.** Every
> number below is a description, never a result. The refusal-to-rank floor is n = 8
> and it is honoured in every table.

---

## VERDICT (first, because it is short)

**UNRANKABLE at this n, in the direction of "saved a trivial amount".**

On the cut that decides — every refusal replayed serially under
`MAX_POSITIONS_PER_SIDE = 1`, with the real book's occupancy respected — the
blackout has refused **7 tradeable entries in 88 days**, and those 7 would have
returned **ΣR = −0.146, Σ$ = −2.44 on a $100 notional**.

So the blackout has *saved* two dollars and forty-four cents in three months. That
is not a finding. It is smaller than one round-trip fee pair on three trades, it is
carried almost entirely by a single refusal (row 734, −$2.82), and it flips sign
under the independent cut (+$0.50). **The honest answer is that the blackout's P&L
effect is indistinguishable from zero and will stay that way for a long time.**

**What n would settle it.** At the observed refusal rate — 7 serial refusals across
9 covered releases, ≈0.8 per release — a rankable cell (n = 8) is ≈10 releases away.
The calendar carries ~3 high-impact releases a month (one NFP, one CPI, and an FOMC
in 5 months of 12), so **n = 8 in a single side×event cell is roughly 10 months away
at NFP-only cadence, and ~4 months away pooled across all three event types.** A
decision that waits for this population to speak is a decision deferred to 2027.

**But §4 found something that does not need n.** The disturbance the window exists
to avoid is **~15 minutes wide (−5m to +10m)**, not 60. That is a measurement of
SOL's behaviour across 9 releases against a clock-matched baseline, and it does not
depend on the tiny refusal population at all. It is reported below without a
proposal attached.

---

## 1. WHAT THE MECHANISM ACTUALLY IS

### 1a. The code, verbatim

There are **two** blackout mechanisms, not one. The operator saw the first.

**Stream A — the hard halt.** `main.py:1976-2000`:

```
1976| def _macro_event_halt(now=None):
1977|     """(halted, reason). Halts when now is within ±MACRO_BLACKOUT_MINUTES of any
1978|     high-impact MACRO_EVENTS row. A10 (2026-06-08): ported verbatim from Titan
1979|     risk_manager.macro_event_halt — closes are NOT routed through this gate."""
1980|     if MACRO_BLACKOUT_MINUTES <= 0 or not MACRO_EVENTS:
1981|         return False, 'macro gate disabled'
1982|     if now is None:
1983|         now = datetime.now(timezone.utc)
1984|     window = timedelta(minutes=MACRO_BLACKOUT_MINUTES)
1985|     nearest = None
1986|     for ev_time, label, impact in MACRO_EVENTS:
1987|         if (impact or '').lower() != 'high':
1988|             continue
1989|         delta = ev_time - now
1990|         if abs(delta) <= window:
1991|             mins = int(delta.total_seconds() / 60)
1992|             when = 'in' if mins >= 0 else 'ago'
1993|             return True, (f'{label} {abs(mins)}m {when} '
1994|                           f'(blackout ±{MACRO_BLACKOUT_MINUTES}m)')
```

It is wired in as **gate 1 of the risk check**, `main.py:2036-2040`:

```
2036|     # Gate 1 (A10, Titan parity): macro-event hard-halt — checked FIRST, like
2037|     # Titan's check_risk(). Closes are never gated.
2038|     halted, halt_reason = _macro_event_halt()
2039|     if halted:
2040|         return False, f'macro halt: {halt_reason}'
```

`_risk_check` has **exactly one call site in the entire file — `main.py:4751`**, on
the entry path, inside the entry-gate lock. The refusal is persisted
(`status='risk_halt'`, reason in `error`) and registered with the Skip-Attribution
Observatory at `main.py:4761-4766`.

**Stream B — the score penalty.** `macro_filter.py:96, 486, 490-492`:

```
  96| _MACRO_WIN_PENALTY = -2.5   # applied regardless of direction during blackout window
 486|         ctx['macro_gate_adj']      = _MACRO_WIN_PENALTY if active else 0.0
 490|     ctx['total_gate_adj'] = round(
 491|         ctx['crypto_gate_adj'] + ctx['macro_gate_adj'], 4
 492|     )
```

and, because `MACRO_GATE_DRYRUN = False` (`config.py:767`), that adjustment **is the
quantity compared against the threshold**, `main.py:4674-4676`:

```
4674|     _thr = _get_live_param('CONFLUENCE_SCORE_THRESHOLD', CONFLUENCE_SCORE_THRESHOLD)
4675|     _gate_score = direction_score if MACRO_GATE_DRYRUN else _macro_gated_score
4676|     if _gate_score < _thr:
```

🔴 **The score gate at :4676 fires BEFORE the risk gate at :4751.** So inside a
blackout window the −2.5 penalty kills a candidate *first*, at
`status='below_threshold'`, and the hard halt only ever sees what survives −2.5
against a 2.0 bar — i.e. raw scores ≥ 4.5. **That is why the `error` column shows
only two macro halts in the entire history: the hard halt is the second line of a
defence whose first line does nearly all the killing.**

🔴 **The two windows are not the same width.** Stream A tests
`abs(delta) <= timedelta(minutes=30)` — exact, ±30:00. Stream B tests
`int(abs(delta_s)/60) <= 30` (`macro_filter.py:395-396`) — truncating, so it stays
active to **±30:59**. This is not theoretical: rows **13944 and 13945**
(2026-07-29 18:30:03 and :04, exactly 30m03s after FOMC) carry
`macro_gate_penalty = -2.5` and passed the hard halt. A 59-second band exists in
which the blackout penalises but does not halt.

### 1b. Does it block BOTH sides symmetrically? — Yes for the halt; the stream it rides in is not

`_macro_event_halt(now=None)` **takes no side argument**. It cannot distinguish
LONG from SHORT. `_MACRO_WIN_PENALTY` is likewise "applied regardless of direction".
**The blackout itself is symmetric. It is not a side ban.**

🔶 **But name the thing beside it honestly.** The quantity that faces the threshold
is `crypto_gate_adj + macro_gate_adj`, and `crypto_gate_adj` **is** direction-specific
(`macro_filter.py:470`; CRITICAL_NEGATIVE = SHORT +1.0 / LONG −1.0). On
2026-09-04 the news was CRITICAL_NEGATIVE, so the effective in-window penalty was
**−1.5 for SHORT and −3.5 for LONG on the same minute**. The blackout is symmetric;
the sum it is added into is not. Anyone reading a −1.5 or −3.5 on a row must not
read it as the blackout's own number.

### 1c. Where the calendar lives, and what happens on failure

**Hardcoded static tuple in `config.py:785-810`. Nothing is fetched. There is no
feed, no network call, no cache.** Twenty rows, built at import from
`datetime`/`timezone` aliases that are `del`'d immediately after (`config.py:811`).

There is therefore no fetch to fail — but there **are** three failure paths, and
**all three FAIL-OPEN**:

1. `config.py:782` — *"Coverage runs through Dec 2026 — refresh before it runs out."*
   When the last row (2026-12-10) passes, `nearest is None` and `_macro_event_halt`
   returns `(False, 'no upcoming high-impact macro events')`. **The gate silently
   stops gating and reports itself as clear.** There is no expiry alarm.
2. `macro_filter.py:377-380` — `except ImportError: return False, None, 9999`.
3. `build_macro_context` is wrapped so *"any sub-system error returns a neutral
   context with zero gate adjustment so network blips never silently kill trades"*
   (`macro_filter.py:418-419`), and `main.py:4557-4560` catches and sets
   `_macro_gate_adj = 0.0`.

**Stated from the code: fail-open, in every path, including calendar exhaustion.**

### 1d. Which events are covered

Three families, all `impact='high'`, all gated at the same ±30m
(`MACRO_BLACKOUT_MINUTES = 30`, `config.py:776`). Nothing is `medium` or `low`;
`config.py:1987` skips any non-high row, so the impact tier is decoration today.

| Family | Rows | Times (UTC) | In the bot's record (2026-06-03 → 2026-09-04) |
|---|---|---|---|
| **FOMC** | 5 | 18:00 (19:00 in Dec) | 06-17, 07-29 |
| **CPI** | 8 | 12:30 (13:30 from Nov) | 06-10, 07-14, 08-12 |
| **NFP** | 7 | 12:30 (13:30 from Nov) | 06-05, 07-02, 08-07, **09-04** |

**9 covered releases have occurred inside the bot's lifetime.** No ECB, no PPI, no
retail sales, no Powell testimony, no unscheduled event of any kind.

### 1e. Has it ever touched an OPEN position? — No, and the book proves it

**From the code path:** `_macro_event_halt` is called from `_risk_check` only, and
`_risk_check` is called from `main.py:4751` only, on the entry path. None of the
five close routes (`_execute_close_position`, `virtual_trader.close_position`, the
SL failsafe at :2639, the flip close at :6042, the poller close at :5712) reaches it.
The docstring's *"closes are NOT routed through this gate"* is accurate.

**From the record:** trades row **9806**, `sl_triggered_short`, `status='executed'`,
timestamped **2026-07-14 12:30:11 — eleven seconds after a CPI release, dead centre
of a blackout window.** A stop fired and closed a live position while the gate was
refusing every entry around it. **Entry-only, confirmed live, not merely by intent.**

---

## 2. THE POPULATION IT HAS REFUSED

### 2b (first, because it governs everything below). Is it large enough to rank? — No.

🔴 **The whole population is 23 refusals across 7 calendar dates, and the serial cut
is 7. Twelve would have been a small study; this is smaller.** Everything in §3 is
reported because it was asked for, not because it can carry weight.

Reconstruction was necessary: the `error` column only began carrying risk reasons on
2026-08-01 (`main.py:4753-4760` documents the gap — *"0 of 289 risk_halt rows carried
it"*), so **only 2 of the 4 hard halts say so in words**. The other two were
recovered from the static calendar, which cannot drift, and both are corroborated by
a `macro_gate_penalty` of −1.5 (= −2.5 window + 1.0 CRITICAL_NEGATIVE SHORT bonus)
written on the same row — the window was provably active.

### 2a. Every entry the blackout refused

Attribution rule: a row counts only if the blackout is the *reason*. Hard halts count
outright. A `below_threshold` row counts only when `raw + crypto_adj ≥ 2.0` and
`raw + crypto_adj − 2.5 < 2.0` — i.e. it would have passed the bar had the window not
been open. Rows killed by the HTF cascade (69 of them) or by crypto news alone are
**not** the blackout's and are excluded.

| row | when (UTC) | side | event | mins | refused by | raw | pen | price | tier composition (combo) |
|---|---|---|---|---|---|---|---|---|---|
| 734 | 06-10 12:00:05 | SHORT | CPI | +29.9 | **hard halt** | — | −1.5 | 63.46¹ | 1H:Any Bullish Confirmation ǀ 15M:HyperWave Signal Down ǀ 5M:Within Bearish OB |
| 6383 | 07-02 12:25:02 | SHORT | NFP | +5.0 | penalty | 4.25 | −3.5 | 81.80 | 1H:15m-rearm Reversal Down ǀ 15M:HyperWave OB Signal Down ǀ 5M:Bearish New Imbalance |
| 9794 | 07-14 12:00:05 | SHORT | CPI | +29.9 | **hard halt** | — | −1.5 | 75.35¹ | 1H:Trend Catcher Up ǀ 15M:HyperWave Signal Up ǀ 5M:Within Bearish OB |
| 13920 | 07-29 17:30:20 | SHORT | FOMC | +29.7 | penalty | 5.00 | −3.5 | 73.22 | 1H:Any Bearish Confirmation ǀ 15M:HyperWave OS Signal Up ǀ 5M:Within Bearish OB |
| 13941 | 07-29 18:10:09 | SHORT | FOMC | −10.2 | penalty | 4.25 | −3.5 | 74.13 | 1H:Any Bearish Confirmation ǀ 15M:HyperWave OS Signal Up ǀ 5M:Bearish Breaker |
| 13942 | 07-29 18:20:06 | SHORT | FOMC | −20.1 | penalty | 4.25 | −2.5 | 74.00 | 1H:Any Bearish Confirmation ǀ 15M:HyperWave OS Signal Up ǀ 5M:Within Bearish OB |
| 13943 | 07-29 18:25:03 | SHORT | FOMC | −25.1 | penalty | 4.25 | −2.5 | 73.81 | 1H:Any Bearish Confirmation ǀ 15M:HyperWave OS Signal Up ǀ 5M:Within Bearish OB |
| 16568 | 08-07 12:10:03 | LONG | NFP | +19.9 | penalty | 3.75 | −2.5 | 73.89 | 1H:Trend Catcher Up ǀ 15M:None ǀ 5M:Bullish OB Mitigated |
| 16569 | 08-07 12:10:04 | LONG | NFP | +19.9 | **hard halt** | 5.76 | −2.5 | 73.90 | 1H:Trend Catcher Up ǀ 15M:None ǀ 5M:Bullish New Imbalance |
| 16573 | 08-07 12:15:06 | LONG | NFP | +14.9 | penalty | 2.50 | −2.5 | 73.92 | 1H:Trend Catcher Up ǀ 15M:None ǀ 5M:Bullish OB Created |
| 16575 | 08-07 12:15:07 | LONG | NFP | +14.9 | penalty | 4.25 | −2.5 | 73.91 | 1H:Trend Catcher Up ǀ 15M:HyperWave Signal Up ǀ 5M:Bullish I-BOS |
| 17850 | 08-12 12:05:02 | SHORT | CPI | +25.0 | penalty | 2.00 | −1.5 | 77.02 | 1H:Smart Trail Switch Bullish ǀ 15M:HyperWave Signal Up ǀ 5M:Bearish OB Entered |
| 17855 | 08-12 12:20:05 | SHORT | CPI | +9.9 | penalty | 2.00 | −1.5 | 77.02 | 1H:Smart Trail Switch Bullish ǀ 15M:HyperWave Signal Up ǀ 5M:Bearish OB Entered |
| 17856 | 08-12 12:20:05 | SHORT | CPI | +9.9 | penalty | 2.50 | −1.5 | 77.02 | 1H:Smart Trail Switch Bullish ǀ 15M:HyperWave Signal Up ǀ 5M:Within Bearish OB |
| 17857 | 08-12 12:30:06 | SHORT | CPI | −0.1 | penalty | 1.75 | −1.5 | 76.70 | 1H:Smart Trail Switch Bullish ǀ 15M:HyperWave Signal Up ǀ 5M:Within Bearish OB |
| 17862 | 08-12 12:45:04 | LONG | CPI | −15.1 | penalty | 4.25 | −3.5 | 76.47 | 1H:Smart Trail Switch Bullish ǀ 15M:HyperWave Signal Up ǀ 5M:Bullish Breaker |
| 17865 | 08-12 12:45:07 | LONG | CPI | −15.1 | penalty | 4.25 | −3.5 | 76.47 | 1H:Smart Trail Switch Bullish ǀ 15M:HyperWave Signal Up ǀ 5M:Bullish Imbalance Mitigated |
| **23789** | **09-04 12:30:02** | **SHORT** | **NFP** | **−0.0** | **hard halt** | **3.88** | **−1.5** | **102.20** | **1H:Any Bearish Confirmation ǀ 15M:HyperWave Signal Down ǀ 5M:Bearish OB Entered** |
| 23790 | 09-04 12:35:00 | SHORT | NFP | −5.0 | penalty | 2.50 | −1.5 | 101.71 | 1H:Any Bearish Confirmation ǀ 15M:HyperWave Signal Down ǀ 5M:Bearish OB Created |
| 23791 | 09-04 12:35:01 | SHORT | NFP | −5.0 | penalty | 2.50 | −1.5 | 101.72 | 1H:Any Bearish Confirmation ǀ 15M:HyperWave Signal Down ǀ 5M:Bearish S-CHOCH |
| 23796 | 09-04 12:40:04 | SHORT | NFP | −10.1 | penalty | 1.75 | −1.5 | 101.70 | 1H:Any Bearish Confirmation ǀ 15M:HyperWave Signal Down ǀ 5M:Bearish New Imbalance |
| 23797 | 09-04 12:40:04 | SHORT | NFP | −10.1 | penalty | 2.50 | −1.5 | 101.70 | 1H:Any Bearish Confirmation ǀ 15M:HyperWave Signal Down ǀ 5M:Bearish OB Mitigated |
| 23801 | 09-04 12:50:04 | SHORT | NFP | −20.1 | penalty | 1.75 | −1.5 | 101.38 | 1H:Any Bearish Confirmation ǀ 15M:HyperWave Signal Down ǀ 5M:Within Bearish OB |

¹ rows 734 / 9794 predate the Skip-Attribution price anchor; price is the close of the
5m bar that had just closed. All other prices are the **live ticker the bot itself
read** (`skip_attribution.price_at_skip`).

### 2b. Counts

| | SHORT | LONG | total |
|---|---|---|---|
| **NFP** | 8 | 4 | 12 |
| **CPI** | 6 | 2 | 8 |
| **FOMC** | 4 | 0 | 4 |
| **total** | **18** | **6** | **23** |

By month: Jun 1 · Jul 6 · Aug 10 · Sep 6. By kind: hard halt 4, score penalty 19.
**Seven distinct calendar dates.** 17 of 23 are same-side repeats within one hour of
one release — which is exactly why the serial cut collapses to 7.

### 2c. Today's one — the SHORT the operator watched

```
trades.id              23789
timestamp              2026-09-04 12:30:02 UTC   (NFP 12:30:00 — 2 seconds after the print)
symbol / side          SOL/USDT:USDT   SHORT     is_virtual = 0  (LIVE book)
status / error         risk_halt  ·  "macro halt: NFP 0m in (blackout ±30m)"
price at refusal       102.20     (live ticker, skip_ts 12:30:13.938 — 12 s of lag; see note)
combo_key              1H:Any Bearish Confirmation | 15M:HyperWave Signal Down | 5M:Bearish OB Entered
tv_action / tv_tf      Bearish OB Entered / 5m
confluence (raw)       3.88
macro_gate_penalty     -1.5   = -2.5 blackout window  +1.0 CRITICAL_NEGATIVE SHORT bonus
  => gate score        3.88 - 1.5 = 2.38  >=  2.0  -> IT PASSED THE SCORE GATE
  => and was then refused by the HARD HALT at the risk gate. Both streams saw it; the
     second one is what stopped it. This is one of only 4 rows in history to get that far.
macro news             CRITICAL_NEGATIVE (conf 0.85) "Trezor says data breach affects
                       another 67K US customers" [Cointelegraph.com News]
market_regime          FLAT
srv_adx_5m             17.457      srv_atr_5m 0.2758     srv_vol_ratio_5m 1.564
trend_5m               bear        hw_15m HyperWave Signal Down (HW_SIGNAL_SHORT, w 1.05)
srv_adx_1h             NULL  <- NEVER FETCHED. See below.
cascade / book gate    never evaluated — both sit AFTER the risk gate
Observatory follow-up  max_favorable_price 100.61 at 12:47:00  (+1.556 % in the SHORT's favour)
```

🔴 **`srv_adx_1h` is NULL and no amount of wishing makes it otherwise.** The HTF
snapshot is fetched on the advisor path, which a risk halt never reaches, so the
1h ADX was never read for this row. The flat-ADX gate itself sits at `main.py:4922`,
**after** the risk gate at :4751, so on this row it was never consulted either.

To answer the operator's actual question — *would the flat gate have refused it in
its armed state?* — I **recomputed** ADX(14) on 1h with the 200-bar window the gate
reads (`main.py:4906-4918`), from the same Bybit source:

```
2026-09-04 12:30 UTC   ADX(1h,14,200) = 28.64   vs ADX_BELOW_FLOOR = 20.0
```

Validation of that recomputation against 12 random rows where the bot *did* record
`srv_adx_1h`: median |Δ| = **1.33 points**, worst 2.41. At 28.64 the value sits
**8.6 points clear of the floor — more than three times the worst observed error.**

🔴 **So: the flat gate, armed, would NOT have refused today's SHORT.** The same holds
for all four hard halts (06-10: 32.17 · 07-14: 23.70 · 08-07: 20.65 · 09-04: 28.64) —
though 08-07's 20.65 is inside the error band and must be called **undetermined**,
not clear. This is a recomputation, clearly labelled; it is not a recorded fact and
must never be cited as one.

**One caveat on the price, stated because it changes the sign of the trade.** The
anchor 102.20 was sampled at 12:30:13.9, ~11 seconds after the entry decision, during
a fall from 104.32 to 100.43 inside a single minute. The bot would have filled
somewhere in 102.20–104.32; **102.20 is the worst end of that band for a SHORT**, so
§3's +0.292R for this row is a floor, not an estimate.

---

## 3. WHAT IT WOULD HAVE MADE — replayed as full-contract trades

### Method

Geometry read from `config.py` **as text** and `trail_arm.py` **as text** — the
config was never imported:

```
SL           = entry -/+ 2.5 x ATR(1h)          SL_BUFFER_ATR = 2.5      (config.py:62)
arm          = 0.75R                            TRAIL_ARM_R   = 0.75     (config.py:231)
BE lock      = entry x (1 +/- 0.0020)           _BE_TARGET_FRAC_ON       (trail_arm.py:64)
trail        = 1.875 x ATR(1h) from water mark  TRAIL_MULT_ATR = 1.875   (config.py:104)
             ... armed ONLY after the lock
fees         = 0.100 % taker on BOTH legs       notional $100
```

ATR(1h) is Wilder-14 on 1h bars **strictly closed before** the signal. Candles are
Bybit `SOLUSDT` linear, pulled public-GET over Tor: 29,537 5m bars and 2,462 1h bars,
2026-05-25 → 2026-09-04, **zero gaps**, plus 4,146 1m bars around the 9 releases.
Within each 5m bar the **adverse extreme is taken first**. There is no time stop and
no opposite-signal close in SOL's contract, so SL / BE-lock / trail is the whole of it;
positions run to their own exit or to the last print.

🔴 **One methodological choice that must be stated, because it decides today's row.**
The entry bar is walked at **1m** resolution starting from the minute **after** the
entry minute. Today's SHORT filled at 102.20 two seconds into a 1m bar whose 104.32
high **was that bar's own open** — price printed before the position existed. Charging
it as an adverse extreme fabricates a stop-out (it turns +0.292R into −1.107R). The
seconds between the fill and the next minute are not resolvable at this granularity
and are skipped; in every case in this population that residue was moving *with* the
trade, so the choice is conservative in the sign it reports.

### 3a/3b. Both cuts

**INDEPENDENT CUT — every signal replayed alone. 🔴 THIS OVERCOUNTS AND MUST NOT BE
USED TO DECIDE.** 23 signals describe 9 distinct market moments; the same move is paid
for up to 4 times (four LONGs on 08-07 all exit at the identical 74.472).

| row | when | side | ev | entry | ATR1h | exit | exit reason | R | $ |
|---|---|---|---|---|---|---|---|---|---|
| 734 | 06-10 12:00 | SHORT | CPI | 63.460 | 0.6650 | 65.123 | sl | −1.076 | −2.820 |
| 6383 | 07-02 12:25 | SHORT | NFP | 81.800 | 1.0571 | 81.622 | trail | +0.005 | +0.017 |
| 9794 | 07-14 12:00 | SHORT | CPI | 75.350 | 0.4521 | 76.480 | sl | −1.133 | −1.700 |
| 13920 | 07-29 17:30 | SHORT | FOMC | 73.220 | 0.5250 | 74.532 | sl | −1.112 | −1.993 |
| 13941 | 07-29 18:10 | SHORT | FOMC | 74.130 | 0.5264 | 73.227 | trail | +0.573 | +1.018 |
| 13942 | 07-29 18:20 | SHORT | FOMC | 74.000 | 0.5264 | 73.227 | trail | +0.475 | +0.845 |
| 13943 | 07-29 18:25 | SHORT | FOMC | 73.810 | 0.5264 | 73.227 | trail | +0.331 | +0.590 |
| 16568 | 08-07 12:10 | LONG | NFP | 73.890 | 0.3457 | 74.472 | trail | +0.502 | +0.587 |
| 16569 | 08-07 12:10 | LONG | NFP | 73.900 | 0.3457 | 74.472 | trail | +0.491 | +0.574 |
| 16573 | 08-07 12:15 | LONG | NFP | 73.920 | 0.3457 | 74.472 | trail | +0.467 | +0.546 |
| 16575 | 08-07 12:15 | LONG | NFP | 73.910 | 0.3457 | 74.472 | trail | +0.479 | +0.560 |
| 17850 | 08-12 12:05 | SHORT | CPI | 77.020 | 0.3064 | 75.905 | trail | +1.255 | +1.248 |
| 17855 | 08-12 12:20 | SHORT | CPI | 77.020 | 0.3064 | 75.905 | trail | +1.255 | +1.248 |
| 17856 | 08-12 12:20 | SHORT | CPI | 77.020 | 0.3064 | 75.905 | trail | +1.255 | +1.248 |
| 17857 | 08-12 12:30 | SHORT | CPI | 76.700 | 0.3064 | 75.905 | trail | +0.838 | +0.837 |
| 17862 | 08-12 12:45 | LONG | CPI | 76.470 | 0.3064 | 75.704 | sl | −1.200 | −1.202 |
| 17865 | 08-12 12:45 | LONG | CPI | 76.470 | 0.3064 | 75.704 | sl | −1.200 | −1.202 |
| **23789** | **09-04 12:30** | **SHORT** | **NFP** | **102.200** | **0.7621** | **101.439** | **trail** | **+0.292** | **+0.545** |
| 23790 | 09-04 12:35 | SHORT | NFP | 101.710 | 0.7621 | 101.530 | open at last print | −0.012 | −0.023 |
| 23791 | 09-04 12:35 | SHORT | NFP | 101.720 | 0.7621 | 101.530 | open at last print | −0.007 | −0.013 |
| 23796 | 09-04 12:40 | SHORT | NFP | 101.700 | 0.7621 | 101.530 | open at last print | −0.018 | −0.033 |
| 23797 | 09-04 12:40 | SHORT | NFP | 101.700 | 0.7621 | 101.530 | open at last print | −0.018 | −0.033 |
| 23801 | 09-04 12:50 | SHORT | NFP | 101.380 | 0.7621 | 101.530 | open at last print | −0.185 | −0.348 |

**Independent total: n = 23 · ΣR = +2.259 · Σ$ = +0.50** — i.e. on this (inflated) cut
the blackout **cost** fifty cents.

**SERIAL CUT — `MAX_POSITIONS_PER_SIDE = 1` honoured, and the real book's occupancy
respected too.** 🔴 **THIS IS THE ONE THAT DECIDES.** A refusal is only tradeable if
that side was free — of a replayed position *and* of a position the bot actually held
(`virtual_positions`). Three refusals (9794, 17862, 17865) would have been refused by
the position cap anyway and are **not the blackout's**.

| | row | when | side | ev | entry | exit | reason | R | $ | held until |
|---|---|---|---|---|---|---|---|---|---|---|
| ✅ | 734 | 06-10 12:00 | SHORT | CPI | 63.460 | 65.123 | sl | −1.076 | −2.820 | 06-10 13:40 |
| ✅ | 6383 | 07-02 12:25 | SHORT | NFP | 81.800 | 81.622 | trail | +0.005 | +0.017 | 07-05 15:05 |
| ✅ | 13920 | 07-29 17:30 | SHORT | FOMC | 73.220 | 74.532 | sl | −1.112 | −1.993 | 07-30 13:50 |
| ✅ | 16568 | 08-07 12:10 | LONG | NFP | 73.890 | 74.472 | trail | +0.502 | +0.587 | 08-08 05:55 |
| ✅ | 17850 | 08-12 12:05 | SHORT | CPI | 77.020 | 75.905 | trail | +1.255 | +1.248 | 08-12 17:40 |
| ✅ | **23789** | **09-04 12:30** | **SHORT** | **NFP** | **102.200** | **101.439** | **trail** | **+0.292** | **+0.545** | **09-04 12:33** |
| ✅ | 23790 | 09-04 12:35 | SHORT | NFP | 101.710 | 101.530 | open at last print | −0.012 | −0.023 | still open |
| ⛔ | 9794 · 17862 · 17865 | | | | | | *real position of that side already open* | | | |
| ⛔ | 13941·13942·13943·16569·16573·16575·17855·17856·17857·23791·23796·23797·23801 | | | | | | *replayed position of that side still open* | | | |

### 3c. ΣR and Σ$ per cell, with n

🔴 **Not one serial cell reaches n = 8. Nothing below is ranked.**

**SERIAL CUT (decides):**

| cut | cell | n | wins | ΣR | Σ$ | rankable? |
|---|---|---|---|---|---|---|
| side | SHORT | 6 | 3 | −0.648 | −3.03 | **n<8 — NOT RANKED** |
| side | LONG | 1 | 1 | +0.502 | +0.59 | **n<8 — NOT RANKED** |
| event | NFP | 4 | 3 | +0.787 | +1.13 | **n<8 — NOT RANKED** |
| event | CPI | 2 | 1 | +0.179 | −1.57 | **n<8 — NOT RANKED** |
| event | FOMC | 1 | 0 | −1.112 | −1.99 | **n<8 — NOT RANKED** |
| ev×side | NFP·SHORT | 3 | 2 | +0.285 | +0.54 | **n<8 — NOT RANKED** |
| ev×side | NFP·LONG | 1 | 1 | +0.502 | +0.59 | **n<8 — NOT RANKED** |
| ev×side | CPI·SHORT | 2 | 1 | +0.179 | −1.57 | **n<8 — NOT RANKED** |
| ev×side | FOMC·SHORT | 1 | 0 | −1.112 | −1.99 | **n<8 — NOT RANKED** |
| month | Jun / Jul / Aug / Sep | 1/2/2/2 | 0/1/2/1 | −1.076 / −1.106 / +1.757 / +0.280 | −2.82 / −1.98 / +1.84 / +0.52 | **all n<8 — NOT RANKED** |
| kind | hard halt | 2 | 1 | −0.784 | −2.28 | **n<8 — NOT RANKED** |
| kind | score penalty | 5 | 3 | +0.639 | −0.16 | **n<8 — NOT RANKED** |

**INDEPENDENT CUT (overcounts; shown only because §3b asked for both):** three cells
clear n=8 arithmetically — SHORT n=17 (ΣR +2.719, Σ$ +0.63), NFP n=11 (+1.997, +2.38),
CPI n=8 (−0.006, −2.34), score-penalty n=19 (+3.686, +3.90), Aug n=10 (+4.143, +4.45).
🔴 **Their n is manufactured by same-move repetition and they are NOT independent
observations. I do not rank them either.**

### 3d. 🔴 THE HEADLINE

**On the serial cut, the blackout SAVED $2.44 (ΣR −0.146) over 88 days on a $100
notional.** On the independent cut it **cost $0.50**. Both are noise. The sign is set
by a single 2026-06-10 refusal worth −$2.82; delete that one row and the serial cut
turns to +$0.38, i.e. the blackout would have *cost* money. **A conclusion that a
single observation can invert is not a conclusion.**

---

## 4. 🔴 IS THE WINDOW THE RIGHT SHAPE?

This section does **not** depend on the 7-trade population. It measures SOL itself
across all 9 covered releases against a **clock-matched** baseline: for each event,
the same clock buckets on every non-event day in the sample (so 18:00 FOMC events are
compared against 18:00 baselines, not against a 12:30 one). Instrument identical for
both: Bybit 5m candles, median of per-event ratios, `range% = (high−low)/mid`.

### 4a. The profile, 15-minute buckets, −120m → +120m

| bucket | med range % | baseline % | ratio | events >2× |
|---|---|---|---|---|
| −120..−105 | 0.352 | 0.252 | 1.22× | 3/9 |
| −105..−90 | 0.465 | 0.284 | 1.33× | 3/9 |
| −90..−75 | 0.493 | 0.308 | 1.23× | 4/9 |
| −75..−60 | 0.465 | 0.292 | 1.21× | 3/9 |
| −60..−45 | 0.422 | 0.291 | 1.22× | 2/9 |
| −45..−30 | 0.382 | 0.316 | **1.03×** | 1/9 |
| **−30..−15** *(inside)* | 0.377 | 0.336 | **1.12×** | **1/9** |
| **−15..+0** *(inside)* | 0.584 | 0.345 | **1.69×** | 4/9 |
| **+0..+15** *(inside)* | **1.614** | 0.417 | **3.87×** | **8/9** |
| **+15..+30** *(inside)* | 0.607 | 0.358 | **1.70×** | 3/9 |
| +30..+45 | 0.574 | 0.380 | 1.51× | 4/9 |
| +45..+60 | 0.739 | 0.387 | **2.04×** | 4/8 |
| +60..+75 | 0.890 | 0.660 | **2.04×** | 5/8 |
| +75..+90 | 0.855 | 0.534 | 1.60× | 3/8 |
| +90..+105 | 0.668 | 0.535 | 1.29× | 2/8 |
| +105..+120 | 0.821 | 0.592 | 1.72× | 4/8 |

### At the window's own resolution — 5-minute buckets, −30m → +60m

| bucket | med range % | baseline % | ratio | events >2× |
|---|---|---|---|---|
| −30..−25 | 0.271 | 0.211 | 1.18× | 1/9 |
| −25..−20 | 0.243 | 0.203 | 1.09× | 1/9 |
| −20..−15 | 0.283 | 0.196 | 1.45× | 2/9 |
| −15..−10 | 0.252 | 0.223 | 1.13× | 3/9 |
| −10..−5 | 0.245 | 0.197 | 1.24× | 3/9 |
| **−5..+0** | 0.451 | 0.166 | **2.71×** | **7/9** |
| **+0..+5** | **1.384** | 0.243 | **5.70×** | **9/9** |
| **+5..+10** | 0.499 | 0.210 | **2.38×** | **6/9** |
| +10..+15 | 0.300 | 0.195 | 1.54× | 4/9 |
| +15..+20 | 0.404 | 0.222 | 1.82× | 3/9 |
| +20..+25 | 0.342 | 0.190 | 1.80× | 3/9 |
| +25..+30 | 0.345 | 0.177 | 1.92× | 3/9 |
| +30..+35 | 0.320 | 0.229 | 1.39× | 3/9 |
| +35..+40 | 0.444 | 0.183 | **2.43×** | 5/9 |
| +40..+45 | 0.319 | 0.178 | 1.79× | 3/9 |
| +45..+50 | 0.243 | 0.217 | 1.23× | 4/9 |
| +50..+55 | 0.418 | 0.199 | **2.07×** | 5/9 |
| +55..+60 | 0.455 | 0.212 | **2.24×** | 5/8 |

**Where the disturbance starts and ends: it starts at −5m and it is over by +10m.**
The +0..+5 bucket is 5.70× baseline and is elevated on **9 of 9** releases — the only
bucket in the entire 4-hour span that is unanimous. −5..+0 is 2.71× (7/9), +5..+10 is
2.38× (6/9). By +10..+15 it is 1.54× and by +15 it is inside the ordinary range of an
ordinary hour.

### 4b. Too wide, too narrow, or about right?

🔴 **Measured, the ±30m window is about four times wider than the disturbance and its
right edge is not on a boundary.**

- **The left half is nearly empty.** −30..−15 runs at **1.12×** baseline — one release
  in nine even reaches 2×. The window's first 25 minutes (−30 → −5) are
  indistinguishable from any other 25 minutes of the same trading hour.
- **The real event is ~15 minutes wide** (−5 → +10), and half of that lies in a single
  5-minute bucket.
- **The right edge at +30 is arbitrary.** +15..+30 sits at 1.70×, and the band *outside*
  the window, +30..+60, sits at 1.51× / 2.04× — statistically the same air. Whatever
  is elevated at +25 is still elevated at +55. **The window does not end where the
  disturbance ends; the disturbance simply decays through the boundary.**
- Of the 60 minutes the window blocks, roughly **15 carry the event and ~45 are
  ordinary market.** That matches the refusal record exactly: 20 of 23 refusals landed
  in those ordinary 45 minutes.

### 4c. Do LONG and SHORT outcomes differ around releases?

**No stable directional edge, and therefore no case that a symmetric instrument is the
wrong one.** Signed 15m median returns across the 9 releases:

| bucket | median signed return | up-buckets |
|---|---|---|
| −15..+0 | **+0.260 %** | 7/9 |
| **+0..+15** | **−0.319 %** | **3/9** |
| +15..+30 | +0.136 % | 7/9 |
| +30..+45 | +0.062 % | 5/9 |
| +75..+90 | −0.425 % | 0/8 |

The release bucket leans **down** (3/9 up, median −0.319 %) and the bucket before it
leans **up** — a drift-up-into-the-print, sell-the-print shape. But 3/9 versus 9/9
required for any sign test at α=0.00075 is nothing, and it reverses immediately at
+15..+30. In the replay itself: LONG n=6 ΣR −0.460, SHORT n=17 ΣR +2.719 on the
independent cut; LONG n=1, SHORT n=6 on the serial. **Neither leg is populated enough
to compare.** The symmetric blackout is not measurably the wrong instrument — it is
simply an untested one.

### 4d. No sweep was run

No optimal window was searched for, no grid was scanned, no threshold was fitted. The
profile above is a description of SOL's behaviour and nothing has been tuned to it.

---

## 5. CONTROLS

**Bonferroni** — declared in the header, over all 67 cells: α = 0.00075. At n=7 the
best attainable p is 0.0156. **Nothing here can be significant. Stated before results
were read, not after.**

**12-window sign stability — 🔴 how many windows are evaluable, up front: 5 of 12
(serial), 6 of 12 (independent).** This is structural, not bad luck: blackout
refusals can only exist on the 7 calendar dates that carried a release — the same
day-switch clustering the flat-ADX gate has.

| W | span | serial n | ΣR |
|---|---|---|---|
| 1 | 06-10..06-17 | 1 | −1.076 |
| 2 | 06-17..06-24 | 0 | *empty — not evaluable* |
| 3 | 06-24..07-02 | 0 | *empty — not evaluable* |
| 4 | 07-02..07-09 | 1 | +0.005 |
| 5 | 07-09..07-16 | 0 | *empty — not evaluable* |
| 6 | 07-16..07-23 | 0 | *empty — not evaluable* |
| 7 | 07-23..07-30 | 1 | −1.112 |
| 8 | 07-30..08-06 | 0 | *empty — not evaluable* |
| 9 | 08-06..08-14 | 2 | +1.757 |
| 10 | 08-14..08-21 | 0 | *empty — not evaluable* |
| 11 | 08-21..08-28 | 0 | *empty — not evaluable* |
| 12 | 08-28..09-04 | 2 | +0.280 |

Sign across the 5 non-empty windows: **3 positive, 2 negative.** A coin.

**Regime test, both legs populated:**

| cut | regime | n | ΣR | Σ$ |
|---|---|---|---|---|
| independent | TREND | 8 | +2.207 | +2.73 |
| independent | FLAT | 15 | +0.052 | −2.23 |
| serial | TREND | 2 | −0.609 | −1.41 |
| serial | FLAT | 5 | +0.464 | −1.03 |

Both legs are populated on both cuts. On the serial cut both are n<8; on the
independent cut the legs point opposite ways in dollars and the same way in R, which
is what noise looks like.

**Paper vs live:** **live-only, and there is no paper twin — by construction, not by
omission.** The blackout sits in `_risk_check` on the *shared* entry path, so paper and
live are refused identically. Confirmed against the book: **0 of 36 `virtual_positions`
(22 paper, 14 live) was ever opened inside a blackout window** — in 88 days the gate
has never once been crossed. This population is a record of refusals, not of fills, so
no paper/live comparison is possible for it in either direction.

---

## VERDICT

🔴 **UNRANKABLE at this n.** The blackout's measured effect on the serial cut is
**+$2.44 saved on a $100 notional over 88 days**, ΣR −0.146, n = 7 — below the n = 8
floor, inside the noise, and invertible by deleting one row. It cannot be called a
saving and it cannot be called a cost.

**What n would settle it, and how long that is.** n = 8 in a single pooled cell needs
about 10 more covered releases at the observed ~0.8 serial refusals per release. At
roughly one NFP a month plus one CPI and an occasional FOMC — 9 releases in the 88 days
measured — that is **~4 months pooled across all three event types, and ~10 months for
an NFP-only cell.** A per-side×event cell is out of reach entirely within a year.

**Two things ARE known now, and neither needed the P&L population:**

1. **The window is ~4× wider than the disturbance.** SOL's elevation runs −5m to +10m
   (5.70× baseline at +0..+5, unanimous across 9 of 9 releases); the −30..−15 half is
   1.12× baseline, and the band just *outside* the right edge (+30..+60) is as elevated
   as the band just inside it. The window's shape is not supported by SOL's behaviour.
2. **The reported mechanism is not the one doing the work.** The RISK HALT the operator
   saw is the *second* line — the −2.5 score penalty at `main.py:4676` fires 40 lines
   earlier and killed 19 of the 23 refusals. Only 4 candidates in 88 days have ever
   reached the hard halt, and only 2 of those say so in the `error` column.

🔶 **And the interaction with the running experiment, since that was the reason for
urgency.** `FLAT_ADX_GATE_DRYRUN = True` since 2026-09-03 19:43 opens the later gates
to more proposals, but the blackout sits **before** the flat gate in the path
(`:4751` vs `:4922`) and refuses ~2.6 candidates per release day. Against a 14-day
observation window carrying a −3R stopping rule from a +6.141R baseline, the blackout's
own contribution — **−0.146R across 88 days** — is roughly **5 % of one stopping-rule
unit per quarter.** It is not a material confound for that experiment. Separately: on
all four hard-halted rows the recomputed 1h ADX sat above the flat gate's floor of 20
(28.64 today), so the flat gate, armed, would not have refused the SHORT the operator
watched — 08-07's 20.65 is inside the recomputation error and is **undetermined**, not
clear.

**No change is proposed. Nothing was applied.**

---

## READ-ONLY CONFIRMATION

| check | result |
|---|---|
| DB opened | `file:/…/mercury-sol/trades.db?mode=ro` (URI read-only), **SELECT only** |
| cwd | `/root` — outside SOL's tree, for every command |
| config | read **as text** + parsed with `re`; `config.py` **never imported**; `MACRO_EVENTS`, `SL_BUFFER_ATR`, `TRAIL_MULT_ATR`, `TRAIL_ARM_R`, `_BE_TARGET_FRAC_ON`, thresholds all extracted textually |
| writes | **none** — no DB write, no file in the SOL tree touched, all scratch output in the session scratchpad |
| orders | **none placed, none cancelled**; no authenticated venue call of any kind |
| venue access | Bybit **public** `/v5/market/kline` GET only, over the box's existing Tor SOCKS (direct is CloudFront-blocked) |
| service | `mercury-sol.service` untouched — MainPID **3442516** unchanged, active since 2026-09-03 19:45:15 |
| **`NRestarts`** | **0 before, 0 after — unchanged** |
| file hashes | **34 of 35 byte-identical.** The one that moved is `oi_cache.json`, the **live bot's own** open-interest cache, rewritten by PID 3442516 during the audit. No `.py`, no `.json` config, no `.env` changed. |
| **`FLAT_ADX_GATE_DRYRUN`** | **still `True`** (`config.py:407`) |
| Titan | untouched beyond the mandated pre-flight — `openitems_guard.py` exit **0**, header and current-state table agree with runtime, titan-bot HEAD `f5d3542` |
