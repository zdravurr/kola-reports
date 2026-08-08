# sol-0850-reasoning-judged-apply-guard-and-adoption-diffs

_2026-08-08 15:30 UTC_

---

# Mercury-SOL — the 08:50 entry judged on what it SAID, plus two diffs for approval

**State check is clean: nothing half-applied, the venue is byte-identical, Titan untouched.
The 08:50 reasoning was NOT vindicated by the move — its one falsifiable claim about the book
was FALSE, and the two entries that died at 06:50 and 08:35 gave materially the same reason.
Items 2 and 3 are built and proven by execution on an isolated copy. NOTHING APPLIED.**

Prior: [cohort filter 14:39](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1439-sol-optimizer-live-cohort-filter-applied.md)
· [paper weights 14:17](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1417-sol-paper-weights-measured-not-in-the-gate.md)
· [restart 14:05](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1405-sol-restarted-fixes-loaded-optimizer-paper-weights-finding.md)
· [forensics 13:21](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1321-sol-live-forensics-three-entries-one-open.md)

---

## 0. STATE CHECK — CLEAN. Nothing is half-applied.

### (a) Everything with an mtime after 14:32

```
14:32:04  optimizer.py                    the live-cohort filter (the 14:39 report's subject)
14:56+    trades.db                       the running bot writing; expected
15:21     optimizer/tg_offset.txt         the listener's poll cursor; expected
```

Nothing else. The full set of files touched today is `tor_retry.py` 13:49:02, `main.py` 13:50:55,
`optimizer/dynamic_weights.json` 14:00:03, `optimizer.py` 14:32:04 — exactly the four the prior
reports account for, and no more.

**`.bak_*` from today — one, and its mtime is deliberately older:**

```
optimizer.py.bak_livecohort_20260808_142638   size 29993   mtime 2026-08-06 15:18:55
optimizer.py                                  size 36044   mtime 2026-08-08 14:32:04
```

The backup's mtime is the *pre-edit source's* mtime, preserved by `cp -p` — it is not evidence of a
second edit. Sizes differ by +6051 bytes, consistent with the recorded "+105 / −11 lines".
`main.py.bak_threefixes_20260808_134816` and `tor_retry.py.bak_threefixes_20260808_134816` carry the
same signature from the 13:48 pass. **No orphaned or duplicate backups.**

### (b) Service

```
mercury-sol            active (running) since 2026-08-08 13:57:57 UTC   (1h33m)
  master pid 3484279   worker pid 3484439        NRestarts=0
tracebacks since boot: 0
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R)
                    ATR_TF=1h OBSERVATION_MODE=False [pid 3484439]
[HEARTBEAT] alive ticks=283 (+26 in 301s) cadence=10s open=0 mode=LIVE pid=3484439
```

Worker pid is the same 3484439 the 14:05 report recorded. `OBSERVATION_MODE=False` confirmed
character for character.

### (c) The venue — byte-identical

Read at 14:59 UTC, `/v5/position/list` → `retCode 0`:

| field | required | read | |
|---|---|---|---|
| size | 1.3 | **1.3** | ✅ |
| avgPrice | 74.80 | **74.8** | ✅ |
| stopLoss | 73.89 | **73.89** | ✅ |
| openTime | 1786179014459 | **1786179014459** | ✅ |
| curRealisedPnl | −0.09724 | **−0.09724** | ✅ |
| positionIdx 1 | LONG open | Buy, Normal, tpslMode Full | ✅ |
| positionIdx 2 | size 0 | **size 0**, side `''` | ✅ |

Conditional order — exactly one: `671eee37-1308-4efd-9fca-fd3586743e1e`, StopLoss,
**Untriggered**, trigger 73.89 MarkPrice, direction 2, qty 1.3, reduceOnly, closeOnTrigger,
positionIdx 1, createdTime 1786179014843. Unchanged.

Only the mark has moved: **76.546**, uPnL **+2.2698**. Every call this session was a read.

### (d) Titan — untouched

```
git status --porcelain : (empty)      HEAD 897850b
titan.service          : active, ActiveEnterTimestamp 2026-08-06 01:53:19, NRestarts=0
master pid 2538048     : started Thu Aug 6 01:53:18
no .py modified since 2026-08-07
```

One honest note: the titan **worker** pid 3282345 started today at **04:27:58** — a gunicorn worker
recycle 10h31m *before* this session opened (my first command ran at 14:54:42). The master has never
restarted. Nothing in this session touched Titan; I read `optimizer_listener.py` and `optimizer.py`
read-only to port the guard.

---

## 1. 🔴 WAS THE 08:50 LONG REASONED, OR LUCKY?

**Short answer: the shape of the reasoning was sound, its one checkable claim about the order book
was FALSE, and it was the same reason given for the two entries that died. The move validated the
trade. It did not validate the sentence.**

### (a) The full entry decision — trades row 16767

**The tiers** (`combo_key` = `1H:Bearish Confirmation+|15M:HyperWave Signal Up|5M:Bullish OB Entered`):

| slot | signal | direction | age at decision | vs LONG |
|---|---|---|---|---|
| 1H | Bearish Confirmation+ | **SHORT** | **14.8h — STALE** (gate's window is 6h) | **OPPOSES** |
| 15m | HyperWave Signal Up | LONG | 35m | AGREES |
| 5m | Bullish OB Entered | LONG | trigger | AGREES |

Combo weight **1.00** — the baseline, i.e. this combination has no history either way.

**The score arithmetic**, from `matrix_breakdown_json`:

```
TREND      long 2.5  short 0.0   net LONG      contribution +2.5   (2 signals)
MOMENTUM   long 1.75 short 1.75  net NEUTRAL   contribution  0.0   (2 signals, INTRA-CONFLICT)
LIQUIDITY  long 0.0  short 0.0   net NEUTRAL   contribution  0.0   (0 signals)
EXECUTION  long 2.0  short 0.0   net LONG      contribution +2.0   (1 signal)
                                          raw direction_score = 4.50
```

```
raw                4.50
macro penalty     -1.00     (macro_news_category=CRITICAL_NEGATIVE, confidence 0.85)
                  ------
_macro_gated_score 3.50     <- THE QUANTITY THE GATE COMPARES
threshold          2.00     (CONFLUENCE_SCORE_THRESHOLD, no params.json override)
                   PASSED by 1.50

weighted_adj      -0.6983 -> "final" 3.80   INFORMATIONAL ONLY, not in the gate
                                            (confirmed 14:17; weight_engine.py:17)
```

**The cascade's verdict:** the cascade, score and risk gates all passed *before* the advisor was
consulted — the prompt says so in its own last line. The advisor returned
`decide=execute, confidence=0.72`.

### (b) 🔴 THE VERBATIM PROMPT AND THE VERBATIM REASON

The prompt **did** render the OKX-4000 wall structure with per-wall percentiles. Lines 20–24 of
`ai_user_prompt`, exactly as sent:

```
Order book (pre-trade, 8000 levels):
  Mid: $74.78  |  Imbalance ±1%: 0.48 (ask-heavy)
  Bid walls (>4x avg vol): $74.75 (p80, x14.4), $74.25 (p67, x11.1), $73.75 (p41, x6.7),
                           $73.25 (p34, x5.9), $72.25 (p10, x4.4)
  Ask walls (>4x avg vol): $74.75 (p62, x10.1), $75.25 (p64, x10.6), $75.75 (p64, x10.5),
                           $79.25 (p5, x4.0)
  Wall figures: pN = this wall's PERCENTILE among all walls this prompt has rendered
  (n=23,080; the primary figure) ... CALIBRATION: ~p50 is an ORDINARY wall, p90+ is
  genuinely thick. Judge thickness by the percentile, not by the word "massive" or by
  the multiple.
```

("8000 levels" is OKX-4000 — 4000 **per side**.) The prompt also gave both stale-tier tallies
explicitly, and told the model neither was privileged.

**The verbatim reason** (`ai_raw_response`, `claude-haiku-4-5-20251001`):

```json
{
  "decide": "execute",
  "confidence": 0.72,
  "reason": "1H signal stale (14.8h); fresh 15m/5m agree LONG. 4h/1h BULL, ADX elevated
             (33.4/45.6), EMA expanding 1h. No opposing walls above entry. Execute."
}
```

**What it cited:** the stale 1H tier (correctly, choosing the exclude-stale reading the prompt
offered), tier agreement, the regime (4h/1h BULL, ADX 33.4/45.6, EMA expanding), and the book.

**🔴 What it got wrong: "No opposing walls above entry" is FALSE, and its own prompt says so.**
Entry was 74.80. The prompt listed ask walls at **75.25 (p64, ×10.6)**, **75.75 (p64, ×10.5)** and
79.25 — three opposing walls above entry, two of them just above. **It did not mention the
percentiles at all.** It was handed a calibrated percentile scale and returned a claim that the
walls did not exist.

### (c) The book at that instant

```
mid 74.78 · imbalance 0.4847 — ASK-HEAVY · depth 4000/side (OKX) · wall threshold 4x
nearest SUPPORTING (bid) wall : 74.75  p80  x14.4   — 0.05 BELOW entry, genuinely thick
nearest OPPOSING (ask) wall   : 75.25  p64  x10.6   — 0.45 ABOVE entry, ordinary
next opposing                 : 75.75  p64  x10.5   — 0.95 ABOVE entry, ordinary
```

The honest reading the model could have given: *one thick bid wall (p80) right under entry, two
ordinary ask walls (p64) overhead, book slightly ask-heavy.* That is a defensible LONG case. It is
not the case the model made.

### (d) 🔴 THE HONEST FRAME — the reasoning did not predict this move

**What actually happened after the entry** (Bybit 5m klines, read this session):

```
08:50 entry 74.80        08:55 74.73 (the low)      09:00-11:00  74.7-75.1  — TWO HOURS FLAT
12:00 75.56              13:00 75.44                14:00 75.68   14:50 76.33
post-entry low 74.730    post-entry high 76.660     now ~76.55
```

Judge the sentence on what it said:

1. **The claim that was checkable was false.** "No opposing walls above entry" — there were two at
   p64. Price later went *through* both. The claim was not vindicated by that; it was **irrelevant**
   to it. Had those walls held, the identical sentence would have been the stated reason for a loss.
   A reason that is wrong about the data and right about the outcome is a coin landing well.
2. **The move was not the one described.** "ADX elevated, EMA expanding, TREND regime" reads as a
   continuation call. What followed was **two hours of chop within 0.4** before anything moved. Note
   the 5m ADX was **23.7** and the 5m regime NEUTRAL — the elevated 33.4/45.6 figures are 1h and 15m.
3. **The 15m ADX of 45.6 came with a CONTRACTING EMA gap of 0.188%** — the prompt's own line flags
   contraction as compression. The model cited "EMA expanding 1h" and passed over the 15m
   contraction on the same screen.
4. **The base rate says do not update on this.** The advisor's `execute` verdict has closed **22**
   positions in this book: **8 wins, 14 losses, net −$1,128.46**. A 36% win rate. And the specific
   clause used here — "no opposing wall(s)" — has appeared **8 times in the entire history**, of
   which exactly **one** produced a closed position (a paper LONG, +494). Its live track record is
   **zero closed trades**.
5. **n=1, and it is not even n=3.** The three entries today are one observation, not three: same
   signal cluster, same book, same two-hour window, same move, prices within 6 cents of each other.

**Verdict: it coincided. This bot has killed twenty filters that looked better than this on more
data. Nothing here should change a parameter.**

The fair credit, stated precisely: the *machinery* behaved well. The stale-tier disclosure worked —
the prompt surfaced a 14.8h-old opposing 1H tier, showed both tallies, and the model made the
exclude-stale choice explicitly rather than silently. The percentile calibration was present and
correct. **The prompt did its job; the model did not use the part it was given.**

### (e) Contrast with 06:50 and 08:35 — the same decision

| | 06:50 (16748) | 08:35 (16765) | 08:50 (16767) |
|---|---|---|---|
| confidence | 0.78 | 0.78 | 0.72 |
| stale-1H clause | "1h signal stale (12.8h)" | "stale (14.6h, outside 6h window)" | "stale (14.8h)" |
| trend clause | "strong 1h/4h trend + bull MTF 4/4" | "1h BULL (ADX 33.4, expanding EMA)" | "4h/1h BULL, ADX 33.4/45.6" |
| **wall clause** | **"No opposing wall at entry."** | **"No opposing walls above entry; ask walls at p64-p69 are ordinary, not massive"** | **"No opposing walls above entry."** |
| ask walls actually present | 75.25 ×11.5, 75.75 ×10.6 | 75.25 ×11.6, 75.75 ×10.2 | 75.25 p64, 75.75 p64 |

**Materially identical.** All three assert no opposing walls above entry; all three books contain
ask walls at 75.25 and 75.75.

The 08:35 reason is the interesting one — it is **self-contradictory in a single sentence**: "No
opposing walls above entry; ask walls at **p64-p69** are ordinary". It names the percentiles of the
walls whose existence it has just denied. That is the only one of the three that used the
percentile scale, and it used it to grade walls it said were not there.

**08:50 is not a better decision than 06:50 or 08:35. It is the same decision that survived**, and it
survived for a purely mechanical reason established in the 13:21 forensics: one webhook instead of
two, so one thread, so no duplicate stop-set, so no `34040`, so no fail-safe. Had the 06:50 and 08:35
positions not been emergency-closed by that bug, both would be in profit on this same move — they
entered at 74.79 and 74.85.

**The bug cost roughly the same trade twice, and the survivor is being read as a good call.**

---

## 2. THE APPLY-GUARD — Titan's second line, ported. DIFF ONLY.

### (a) Provenance stamped at the source — `optimizer.py`

`save_proposal` stamped no cohort provenance, so the listener had nothing to check. Now every filter
proposal carries a `live_evidence` block, **stamped rather than assumed**, so the guard verifies the
proposal instead of trusting the module that wrote it.

Executed output (real `optimizer._stamp_live_evidence`, lab DB, synthetic live cohort):

```json
{
  "live_pairs": 8,
  "paper_pairs": 0,
  "live_abs_pnl": 1651.5251,
  "paper_abs_pnl": 0.0,
  "counterpart_rows_excluded": 9,
  "split_predicate": "virtual_positions.COALESCE(is_paper,1)=0",
  "cohort_mode": "live"
}
```

In **paper** mode the same segment stamps honestly — `live_pairs: 0, paper_pairs: 8` — and the guard
refuses it. That is intended and is stated below as a behaviour change.

### (b) The guard — majority-live by BOTH rows AND dollars

`MIN_LIVE_SHARE = 0.50`, strict `>` on both shares. Titan's reasoning is the point and it is
**measured on SOL, not inherited**: paper notional median $9,994 against live $97.24 — **103×** — and
`find_worst_segment` ranks by *summed dollars*. Executed vectors:

| vector | live rows | live \|PnL\| | verdict |
|---|---|---|---|
| majority-live by ROWS, 99% paper by DOLLARS | 70.6% | **1.0%** | **REFUSED** |
| majority-live by DOLLARS, minority by ROWS | **28.6%** | 98.9% | **REFUSED** |
| exactly 50.0% on rows (strict `>` required) | **50.0%** | 90.9% | **REFUSED** |
| live-dominated on both | 70.6% | 98.9% | ALLOWED |

### (c) 🔴 FAIL CLOSED — proven end to end

| vector | verdict |
|---|---|
| no `live_evidence` key at all | **REFUSED** |
| `live_evidence` present but not a dict | **REFUSED** |
| empty `live_evidence: {}` | **REFUSED** |

And through the real `apply_proposal`, with a proposal shaped exactly like a live one:

```
apply_proposal('prop-legacy') -> ok=False
🔴 REFUSED — mtf_alignment_score=mtf_3
this proposal carries NO live/paper evidence block — it predates the apply-guard
(2026-08-08). It cannot be shown to rest on live trades, so it is REFUSED.
Nothing was filtered and the cycle marker was NOT moved.

filters.json existed before=False  after=False
cycle marker         before='2325'  after='2325'      <- BOTH writes untouched
```

The guard runs **before any write**, so a refusal cannot half-apply. Positive control:
`apply_proposal('prop-good')` with live-dominated evidence → `ok=True`, filter appended, marker
advanced. It is a guard, not a wall.

### (d) SOL's `MIN_LIVE_PAIRS` — **8**, and why that number

**8, because `optimizer.MIN_PATTERN_SAMPLE` is 8** — asserted equal in the test. That is the minimum
segment size `find_worst_segment` will even consider (`if n < MIN_PATTERN_SAMPLE: continue`).
Matching it exactly is the only defensible choice: a **lower** floor would admit segments below the
producer's own sample bar; a **higher** floor would refuse proposals the producer legitimately made,
turning the guard into a silent veto whose threshold disagrees with the thing it guards. Titan uses
8 for the identical reason — its comment says "mirrors optimizer.MIN_PATTERN_SAMPLE" — so this is
parity by derivation, not by copying a constant.

Proven: 7 live pairs at 100% live share → **REFUSED**.

### (e) The predicate does NOT read `OBSERVATION_MODE` — proven two ways

```
_live_evidence_ok source mentions OBSERVATION_MODE: False   /  mentions config: False
with config.OBSERVATION_MODE=True  : live-dominated=True, no-block=False
with config.OBSERVATION_MODE=False : live-dominated=True, no-block=False
```

Source-inspected *and* exercised under both flag values with identical results. It reads the
evidence block on the proposal, nothing else. That premise expired at the flip on 2026-08-07 22:25
and had already invalidated one comment in `optimizer.py` earlier today; a guard resting on it would
have been dead the moment it shipped.

### 🔶 TWO THINGS I AM FLAGGING, NOT BUILDING

1. **`apply_opt_proposal` is a second, unguarded door.** It can also append a filter from
   `worst_segment`. It is currently dead — `PARAM_TUNING_ENABLED = False` (`config.py:29`) forces an
   early return — and **Titan does not guard it either**, so guarding it would be a divergence, not
   parity. But if that flag is ever flipped, the guard is bypassed. Say the word and it is two lines.
2. **In paper mode every proposal is now refused.** The cohort is paper by construction, so
   `live_pairs=0` and the floor refuses. That is the literal ask ("fail closed") and the safe
   direction while real money is on the venue — but it means that if you ever run SOL back in
   observation mode, no filter can be confirmed until the guard is relaxed. Flagging so it is your
   call, not a surprise.

---

## 3. BOOT ADOPTION OF AN ORPHAN LIVE POSITION — DIFF ONLY

### (a) It reuses the canonical booker, it does not re-derive

`virtual_trader.book_live_position` is already the one and only INSERT for a live row. Adoption
calls **it**, so every formula stays where it lives. Three optional kwargs were added
(`opened_at`, `recheck_status`, `measure_baselines`), **all defaulting to today's exact behaviour**,
so the live entry path — which passes none of them — is byte-identical.

### (b) 🔴 EVERY DERIVED FIELD, ITS FORMULA, AND ITS VALUE FOR THE POSITION OPEN RIGHT NOW

Executed against a verbatim copy of the 14:59 venue read:

**Read from the venue — no derivation:**

```
size                1.3                            <- info.size
initial_fill_price  74.8                           <- info.avgPrice
sl_price            73.89                          <- info.stopLoss
opened_at           2026-08-08T08:50:14.459+00:00  <- info.openTime 1786179014459
entry_fee           0.09724                        <- -info.curRealisedPnl
```

**Derived — formula → value:**

| field | formula | value |
|---|---|---|
| `atr` | `\|fill − sl\| / SL_BUFFER_ATR` = 0.91 / 2.5 | **0.364** |
| `initial_risk_usdt` | `size × \|fill − sl\|` = 1.3 × 0.91 | **1.183 USDT** |
| `trail_cb` | `round(TRAIL_MULT_ATR × atr, 2)` = round(1.875 × 0.364, 2) | **0.68** |
| `trail_pct` | `round(cb / fill × 100, 3)` = round(0.68/74.8×100, 3) | **0.909 %** |
| arm distance | `activation_distance(fill, atr)` = `SL_BUFFER_ATR × atr` | **0.910** |
| **ARM price** | `fill + arm` = 74.80 + 0.91 | **75.710** |
| **breakeven** | `fill × (1 + 0.0015 + 0.0005)` | **74.9496** |
| partial leg | `PARTIAL_AT_ARM_FRACTION × size` = 0.3333 × 1.3 | **0.4333** → 0.4 quantised |
| `mgmt_state` | — | `{"breakeven_applied": false}` |
| `recheck_status` | — | **`'done'`** (see (e)) |
| `water_mark` | seeded at fill | 74.8 |
| `max_adverse_price` | seeded at fill | 74.8 |
| `entry_*` baselines | not measurable after the fact | **NULL** |
| `is_paper` | — | **0** |

**🔴 Why `atr` is the stop INVERSION and not a fresh ATR(1h) measurement.** This is the one field the
venue does not report, and it is the one that could quietly change geometry. The arm policy is
`activation_distance = SL_BUFFER_ATR × atr` (`trail_arm.py`, A6: *"arm at +1R = the SL distance"*),
so `atr` and the stop distance are **the same quantity by design**. Inverting the stop keeps
`arm == |fill − sl| == 1R` **exactly** — verified in the run: `arm == 1R: True`. A freshly measured
ATR would not. The cross-witness is stated rather than hidden:

```
inversion (74.8-73.89)/2.5          = 0.364000   <- USED (venue-only inputs)
trades.srv_atr_1h on row 16767      = 0.367613   (the enrichment's value at 08:50:01)
they differ by 0.99%
using 0.367613 would arm at 0.9190, but this position's 1R is 0.9100 — a geometry change
```

Both inputs to the inversion are venue reads, and it is the exact inverse of
`stop_loss.compute_initial_sl`'s `fallback_atr` route, which is the **only** reachable route while
`SL_WALL_ANCHOR_ENABLED = False`. If that flag is ever ON, the inversion is meaningless and adoption
**refuses** — proven below.

**Why `water_mark` and `max_adverse_price` seed at the fill rather than the true excursion.** The
true post-entry extremes are knowable (MFE 76.66, MAE 74.73) but the engine trails from peaks it
**observed while managing**; seeding a peak it never watched could trail-close on the very first
tick. Both are seeded conservatively at the fill, and the true figures are stated here rather than
buried. `max_adverse_price` is reporting-only in any case (`virtual_trader.py:758` — "drives no close
logic").

### (c) The entry fee — YES, the row needs it, and omitting it corrupts the close

```
virtual_trader.py:565   entry_fee = sum(f['fee'] for f in fills_json)
virtual_trader.py:574   net_pnl   = gross_pnl - entry_fee - close_fee
virtual_trader.py:1119  entry_fee_share = entry_fee_total * frac    (the +1R partial)
```

Omitting it overstates `net_pnl` by exactly **0.09724 USDT** — **8.2 % of this position's 1R**
($1.183) — and overstates the partial's realised PnL by its 1/3 share, **0.03241**. The venue reports
it as `curRealisedPnl` and adoption uses that number. Adoption **refuses** if `curRealisedPnl` is
positive, because a positive value means something has already been realised and the entry fee is no
longer separable.

**🔶 A separate finding while measuring this.** `book_live_position`'s modelled fallback would have
booked `74.8 × 1.3 × BYBIT_TAKER_FEE_RATE` = **0.05348**. The venue charged **0.09724** — a rate of
**0.100 %** against the configured `BYBIT_TAKER_FEE_RATE = 0.00055`. **The modelled taker rate
understates the real one by 1.82×.** That fallback only fires when the fee read fails, and the paper
book uses the same constant at `virtual_trader.py:233`, so every paper fee in the book is understated
by the same factor. Not in scope here; recording it.

### (d) 🔴 WHAT IT MUST NOT DO — nine refusal vectors, all proven

Every one returns `None` and writes nothing; the orphan alert then fires exactly as it does today.

| vector | result |
|---|---|
| no stop on the venue (`stopLoss=''`) | **REFUSED** — "refusing to adopt an unprotected position" |
| no stop on the venue (`stopLoss='0'`) | **REFUSED** |
| `avgPrice` unreadable | **REFUSED** — "EMPTY — unreadable, not zero" |
| `size` unreadable | **REFUSED** |
| `openTime` missing | **REFUSED** — "age unknown, so opened_at cannot be stamped honestly" |
| stop on the WRONG side for a LONG | **REFUSED** |
| `curRealisedPnl` positive | **REFUSED** — fee not separable |
| `curRealisedPnl` unreadable | **REFUSED** |
| `SL_WALL_ANCHOR_ENABLED` ON | **REFUSED** — the inversion would be invalid |

On refusal the boot path falls through to the existing orphan alert: **visible, blocked, unmanaged,
loud** — today's behaviour, unchanged. A missing value is never defaulted to zero; the code
distinguishes "empty" from "zero" explicitly.

### (e) 🔴 THE RECHECK TIERS **CAN** FIRE RETROACTIVELY — you were right to ask

**This is the finding of item 3, and it is a live trap in the existing code.**

```
the orphan's age: 21986s = 6.11h        RECHECK_TIERS_SEC = [10, 60, 300]

_recheck_tier_due(elapsed=21986, last_status=None)  ->  300      <-- NOT None
```

`_recheck_tier_due` returns the **largest** due tier. With `recheck_status` NULL — which is exactly
what `book_live_position` stores today — an hours-old adopted row has T+300 **due on its first
tick**. The hand-off branch that looks like it protects against this:

```python
elif _elapsed > RECHECK_TIERS_SEC[-1]:
    _set_recheck_status(vpos_id, 'done')      # virtual_trader.py:1731
```

**is unreachable**, because `_tier` is `300`, not `None`, so the `if` arm wins. `_run_recheck_tier`
would then score the position against baselines that were never measured at entry and can
**emergency-close it or tighten its stop**. Had adoption been written the obvious way, it would have
adopted the position and immediately re-evaluated a six-hour-old trade as if it were five minutes
old.

**Adoption stores `recheck_status='done'` at INSERT time.** The poll gate is
`_rstatus not in ('done','tightened','closed_critical')`, so the entire recheck block is skipped
before the tier is even computed. Verified in the written row. This is also why
`measure_baselines=False` is correct: those `entry_*` columns feed only the recheck, and measuring
them six hours late would stamp adoption-time readings into columns named `entry_*`.

### (f) 🔴 ADOPTION IS ANNOUNCED — and the card leads with what happens NEXT

The Telegram card produced by the real code path (rendered, tags stripped):

```
🟡 ORPHAN POSITION ADOPTED — SOL/USDT:USDT LONG
vpos=29 · is_paper=0 (REAL MONEY) · trades_row=16767
Source: the VENUE (/v5/position/list), not the ledger.

READ FROM THE VENUE
size        1.3
avgPrice    74.8
stopLoss    73.89
openTime    1786179014459 = 2026-08-08T08:50:14.459000+00:00
entry fee   0.09724  (= -curRealisedPnl)

DERIVED — formula → value
atr        |74.8-73.89|/2.5 = 0.364000
1R (risk)  1.3*|fill-sl| = 1.1830 USDT
trail_cb   round(1.875*atr,2) = 0.68
trail_pct  round(cb/fill*100,3) = 0.909%
arm dist   2.5*atr = 0.9100
ARM PRICE  fill+arm = 75.7100
BE stop    fill*(1+0.0015+0.0005) = 74.9496
partial    0.3333*1.3 = 0.4333 (pre-quantise)

NOT MEASURED, STORED NULL: entry_wall_baseline_mult, entry_adx_1h, entry_atr_pct_1h —
these are ENTRY baselines and this was not entry. recheck_status=done, so the
T+10/60/300 tiers cannot fire retroactively.

🔴 WHAT THE NEXT TICK (≤10s) WILL DO — check these against the venue NOW:
if price ≥ 75.7100 the engine will (1) MOVE THE VENUE STOP 73.89 → 74.9496 and
(2) MARKET-SELL ~0.433 as the +1R partial. Both are REAL orders on REAL money.
```

## 🔴 3(g) READ THIS BEFORE YOU APPROVE ITEM 3

**Adoption is not passive, and on THIS position it will not be quiet.**

The arm price is **75.710**. The mark is **76.546**. The position is already **past its +1R arm**.
So within one 10-second tick of adoption the engine will:

1. **move the venue stop 73.89 → 74.9496** (`_exec_move_stop` moves the real stop for a live row); and
2. **market-sell ≈0.4 SOL** as the +1R partial — a real reduce order.

Both are correct behaviour for a managed position and both are *improvements* on the status quo
(the stop goes from −$1.18 risk to roughly +$0.19 locked). **But they are irreversible orders on real
money, fired by a boot, and they are the direct consequence of approving this diff.** If you want
adoption without those two acts on this particular position, that is a different diff and I have not
written it — say so and I will.

This is also the one place where my design changes a decision the bot makes, so per your standing
instruction I am naming it rather than shipping it quietly: **item 2 makes `apply_proposal` refuse
where it currently accepts; item 3 makes the engine manage a position it currently ignores.** Both
are the requested changes. Neither touches the cascade, the thresholds, the prompts, the score
geometry, the breakeven/partial/trail formulas or the risk gates — item 3 *reads* those formulas to
derive its fields and defines none of its own.

---

## PROOF BY EXECUTION — 17 VECTORS, SEARCHED BY DIRECTORY

The census by DB **filename** finds 13 files. The census by prod **directory** finds **16** — the
three the narrow grep misses are `healthcheck.py`, `mercury_sol_prior_move_logger.py` and
**`weight_engine.py`, which holds `WEIGHTS_PATH` to the production `dynamic_weights.json`**. With
`.env` that is **17 vectors**.

```
tree under test = COPY (30 .py + .env + a point-in-time trades.db via sqlite backup
                  from a mode=ro source; the prod file was never opened for write)
all 17 vectors rewritten   -> remaining prod-path literals in the lab: 0
sys.dont_write_bytecode = True
LOCK on sqlite3.connect AND on open() in write modes, asserting against BOTH the
     prod directory AND /root/titan-bot
```

```
config.OBSERVATION_MODE      = False        (live mode = True)
optimizer.DB_PATH            = <lab>/trades.db
optimizer_listener.DB_PATH   = <lab>/trades.db
optimizer_listener.FILTERS   = <lab>/optimizer/filters.json
weight_engine.WEIGHTS_PATH   = <lab>/optimizer/dynamic_weights.json
virtual_trader.DB_PATH       = <lab>/trades.db

ITEM 2: 9 guard vectors + 2 stamp shapes + end-to-end refuse/apply   ALL PASSED
ITEM 3: 9 refusal vectors + full row written and read back           ALL PASSED
        recheck retroactivity: _recheck_tier_due(21986, None) == 300  CONFIRMED

=== ISOLATION VERDICT: prod/titan leaks = 0 ===
ALL ASSERTIONS PASSED
```

An incidental proof: re-running item 3 against a lab DB that already held the adopted row produced
`sqlite3.IntegrityError` from `ux_vpos_one_open_per_side` and `book_live_position` alerted and
returned `None` — the double-adopt path is covered by the existing unique index.

### Diffstat — nothing applied

```
optimizer.py            +51   -0
optimizer_listener.py   +60   -0
virtual_trader.py      +268  -15
main.py                 +65   -4
```

**All 19 removed lines accounted for:** `virtual_trader.py` — 1 signature line (replaced by the
3-kwarg signature), 1 `opened_at` line (now `opened_at or _utc_now_iso()`), 10 baseline-measurement
lines (re-indented under `if measure_baselines:`, unchanged in content), 3 INSERT lines (one column
and one placeholder added). `main.py` — the 4-line docstring paragraph claiming adoption requires
fabrication, which this pass disproves.

Full unified diff: **643 lines**, in the session scratchpad, shown on request or applied on your word.

---

## STATE — NOTHING APPLIED, NOTHING RESTARTED, THE VENUE UNTOUCHED

```
venue    LONG 1.3 @ 74.80  stopLoss 73.89  openTime 1786179014459  mark 76.546
         uPnL +2.2698 · one Untriggered conditional 73.89 qty 1.3 · idx2 size 0
         UNCHANGED. Every venue call this session was a read.
prod     no file modified since optimizer.py at 14:32:04
         virtual_positions: is_paper=0 rows 0, open rows 0, max id 28  (the lab
         wrote id 29; prod's max is still 28)
         optimizer/ still holds only dynamic_weights.json + tg_offset.txt —
         no proposals dir, no filters.json, no params.json
mercury-sol            active, pid 3484439, NOT restarted, 0 tracebacks
mercury-sol-optimizer  timer active, next 2026-08-09 14:00 UTC, untouched
titan                  active, HEAD 897850b, git clean, master pid 2538048 from
                       Aug 6 — NOT TOUCHED
```

**Awaiting your approval on items 2 and 3. Please read 3(g) first — approving item 3 as written
will move the live stop and sell ~0.4 SOL within ten seconds of the next boot.**
