# sol-entry-advisor-sees-a-partial-view-1h-tier-absent-100pct

_2026-08-01 16:07 UTC_

---

# MERCURY-SOL — WHAT THE ENTRY ADVISOR ACTUALLY SEES, 2026-08-01

**READ-ONLY. Nothing changed, nothing proposed.** Titan was not touched and none of its
parameters were read. Sources: `trades.ai_user_prompt` / `ai_system_prompt` / `ai_raw_response`
(2,944 stored consultations, 2026-06-08 → 2026-08-01), `claude_advisor.py`, `main.py`,
`market_context.py`, `liquidity_zones.py`, all read `?mode=ro`.

Built on the 14:46 diagnosis §0.2 #4 (stored system prompt is always the V1 base) and §2b (two
skips naming the wrong side). Both are confirmed and both turn out to be larger than stated.

---

# THE ANSWER FIRST

**The advisor judges on a partial view, and the partial view is not merely incomplete — parts of
it assert things the same prompt's own data contradicts.**

The cascade knows all three tiers with names and directions. What reaches the model is:

- **the 1H tier: never.** Absent from **2,944 of 2,944** prompts (100%), suppressed by
  `AI_ADVISOR_HIDE_1H = True`.
- **the trade's own direction: never as a field.** There is no `Intended entry:` line. The
  direction appears exactly once, buried inside the phrase `MTF alignment vs LONG: 0/4`.
- **a closing sentence asserting "The 3 timeframes are aligned (confluence has already passed)"
  on 100% of prompts** — while only *two* timeframes are shown at all, and in **31%** of prompts
  those two point in **opposite directions**.

That combination is not cosmetic. Of 104 stored verdicts whose text names the wrong side of the
trade, **103 came from prompts where the two visible tiers disagree** — a 9.70% error rate inside
disagreeing prompts against 0.05% inside agreeing ones.

---

# §1 — THE PROMPT ITSELF: THE LAST 10 CONSULTATIONS

Full verbatim text of all ten is in the Appendix. Tier completeness:

| row | time (UTC) | decide | trade | 1H tier | 15m name | 15m dir | 5m name | 5m dir | all 3? |
|---|---|---|---|---|---|---|---|---|---|
| 14828 | 08-01 07:35 | skip | LONG | **ABSENT** | HyperWave Signal Up | LONG | Within Bullish OB | LONG | ❌ |
| 14830 | 08-01 07:35 | skip | LONG | **ABSENT** | HyperWave Signal Up | LONG | Bullish Liquidity Grab | LONG | ❌ |
| 14831 | 08-01 07:40 | skip | LONG | **ABSENT** | HyperWave Signal Up | LONG | Within Bullish OB | LONG | ❌ |
| 14832 | 08-01 07:45 | skip | LONG | **ABSENT** | HyperWave Signal Up | LONG | Within Bullish OB | LONG | ❌ |
| 14833 | 08-01 07:50 | skip | LONG | **ABSENT** | HyperWave Signal Up | LONG | Within Bullish OB | LONG | ❌ |
| 14834 | 08-01 07:55 | skip | LONG | **ABSENT** | HyperWave Signal Up | LONG | Within Bullish OB | LONG | ❌ |
| 14846 | 08-01 08:45 | skip | LONG | **ABSENT** | HyperWave Signal Up | LONG | Bullish OB Entered | LONG | ❌ |
| 14970 | 08-01 15:45 | skip | LONG | **ABSENT** | HyperWave Signal Down | **SHORT** | Within Bullish OB | **LONG** | ❌ |
| 14972 | 08-01 15:55 | skip | LONG | **ABSENT** | HyperWave Signal Down | **SHORT** | Within Bullish OB | **LONG** | ❌ |
| 14973 | 08-01 16:00 | skip | LONG | **ABSENT** | HyperWave Signal Down | **SHORT** | Within Bullish OB | **LONG** | ❌ |
| *13973* | *07-29 20:05* | *execute* | *SHORT* | ***ABSENT*** | *HyperWave Signal Down* | *SHORT* | *Bearish S-CHOCH* | *SHORT* | ❌ |

**0 of 10 carry all three tiers complete.** The ceiling is 0/10 — the 1H line cannot appear while
`AI_ADVISOR_HIDE_1H` is True, so completeness is unreachable by construction, not by data loss.

The last ten consultations are all skips (the most recent `execute` was 2026-07-29), so the last
execute is appended above and in the Appendix to cover both outcomes as asked.

Nothing renders as `n/a`, `none`, `unknown` or empty in these ten: the 15m and 5m tiers are fully
populated in all of them. **The missing information here is not corrupted — it is withheld.**

Note rows 14970/14972/14973: the 15m tier reads **SHORT** while the 5m trigger reads **LONG**, on
a **LONG** trade, and each of those prompts still ends with *"The 3 timeframes are aligned."*

---

# §2 — HOW OFTEN A TIER IS MISSING, ACROSS ALL 2,944 STORED PROMPTS

| status | n | 1H line missing | 15m name n/a | 5m name n/a | 15m dir n/a | 5m dir n/a | 15m≠5m dir | book missing | news missing |
|---|---|---|---|---|---|---|---|---|---|
| ai_skipped | 2,875 | 2,875 | 133 | 0 | 137 | 0 | 911 | 3 | 2,875 |
| observed_skipped | 50 | 50 | 10 | 0 | 10 | 0 | 0 | 0 | 50 |
| executed | 18 | 18 | 3 | 0 | 3 | 0 | 0 | 0 | 18 |
| claude_unavailable | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| **ALL** | **2,944** | **2,944** | **146** | **0** | **150** | **0** | **912** | **3** | **2,944** |
| **% of all** | | **100.0%** | **5.0%** | **0.0%** | **5.1%** | **0.0%** | **31.0%** | **0.1%** | **100.0%** |

Per tier:

- **1H — missing 100% of the time.** Deliberate (`AI_ADVISOR_HIDE_1H`). The 1H is the hard
  cascade gate's domain, and the design intent is that the advisor should not re-litigate it. The
  consequence is that the model has no view of the tier that decides whether the trade is with or
  against the higher trend.
- **15m — name missing in 5.0%, direction missing in 5.1%.** The 15m slot is a persistent
  state-machine slot; when it has never been set (or was reset) it renders `n/a`. Note the
  executed rows are not exempt: **3 of the 18 real entries were taken with no 15m tier in the
  prompt at all.**
- **5m — never missing.** 0 of 2,944. It is the signal that fired, so it is always present.
- **Order book — missing in 3** (0.1%), rendering `Order book (pre-trade): unavailable`.
- **News — missing in 2,944 (100%).** See §5; this is not a fetch failure.

**The 31% figure, stated two ways.** Counting only prompts where both tiers carry a definite
LONG/SHORT and they oppose: **912 (31.0%)**. Counting any difference including `NEUTRAL`/`n/a`:
**1,062 (36.1%)**. Both are quoted below where relevant; they are not interchangeable.

---

# §3 — IS THE DIRECTION EVER WRONG

## 3.1 The two 08-01 skips, resolved

Both are rows on 2026-08-01 whose stored reason says *"opposes LONG"* on a **SHORT** trade:

| | trades row 14759 | trades row 14760 |
|---|---|---|
| time | 02:50:04 | 02:55:01 |
| DB `side` / `signal_type` | `sell` / `open_short` | `sell` / `open_short` |
| DB `matrix_direction` | **SHORT** | **SHORT** |
| cascade gated on | `1H:15m-rearm: Reversal Up \| 15M:HyperWave Signal Up \| 5M:Within Bearish OB` | same |
| **prompt 15m tier** | `HyperWave Signal Up` **(direction: LONG)** | same |
| **prompt 5m trigger** | `Within Bearish OB` **(direction: SHORT)** ✅ | same |
| **prompt trade direction** | only as `MTF alignment vs **SHORT**` ✅ | same |
| prompt 1H tier | **ABSENT** | **ABSENT** |
| model said | *"1d/4h BEAR regime opposes **LONG**…"* ❌ | *"…1d/4h BEAR regime opposes **LONG**…"* ❌ |

**Verdict: the prompt did not carry a wrong direction.** Both direction-bearing elements — the 5m
trigger and the `MTF alignment vs SHORT` phrase — were correct. The trades row recorded SHORT
throughout, and the cascade gated on the SHORT 5m trigger. **The model named the wrong side.**

**But it is not a clean model artefact either**, and I will not report it as one. The same prompt
handed the model:

1. a **15m tier reading LONG**, the opposite of the trade;
2. a closing sentence asserting **all three timeframes are aligned** — which, given a LONG-reading
   15m tier, points to LONG;
3. **no 1H tier** to break the tie;
4. the true direction stated **once**, inside a phrase about alignment scoring.

Given a self-contradictory prompt with no direction field, "LONG" is a defensible reading of what
was written. The code creates the ambiguity; the model resolves it wrongly.

## 3.2 The systematic version — this is where it stops being anecdotal

Scanning every stored reason for text naming the side opposite to the actual trade:

```
  consultations with a stored reason                       2,944
  reason names the OPPOSITE side as the trade                104   (3.53%)

  of those 104, how many came from a prompt whose
  15m and 5m tiers DISAGREE                                  103   (99.0%)

  base rate of 15m/5m disagreement across all prompts      1,062   (36.1%)

  wrong-side rate INSIDE disagreeing prompts                        9.70%
  wrong-side rate INSIDE agreeing prompts                           0.05%
```

**A ~200× difference.** The direction confusion is essentially confined to the population where
the prompt contradicts itself. When the two visible tiers agree, the model gets the side right
2,881 times out of 2,882.

Fair counterweight, so this is not overstated: on 2026-08-01 twelve rows say *"opposes LONG"*, and
**ten of them are genuine LONG trades where the phrase is correct usage.** Only the two above are
wrong-side. The 3.53% book-wide figure is the honest magnitude.

---

# §4 — THE SYSTEM-PROMPT DEFECT, AND WHAT IT COSTS

`consult_for_entry` ends with `result['system_prompt'] = _ENTRY_SYSTEM`, executed
*unconditionally* and *after* the aligned-V2 blocks may have replaced `decide`, `confidence` and
`reason` with the verdict of a **different** (SOFT) system prompt. So by construction the stored
system prompt is the V1 base on **100%** of rows.

Four distinct base texts are stored across the book (2,774 / 153 / 17 / 1) — the base prompt
itself has been edited four times, and each row correctly carries the base *of its era*. That part
is sound.

## 4.1 The flips are detectable

The flip path overwrites `decide`/`confidence`/`reason` but **never touches `result['raw']`**.
That leaves a signature: `ai_decision='execute'` while `ai_raw_response` still parses to `skip`.

```
  rows where stored raw decide != stored ai_decision:  31
  first such row: 2026-07-10 08:30:03
  rows before 2026-07-02:  0
```

`ADVISOR_WALL_ALIGNED_V2` went LIVE 2026-07-02 and the SHORT companion 2026-07-04. **Zero flips
before that date and the first one eight days after** is strong corroboration that the signature
is real rather than an artefact of parsing.

## 4.2 How many rows record the wrong system prompt: 31

All 31 had their verdict produced by `_ENTRY_SYSTEM_V2_ALIGNED` or
`_ENTRY_SYSTEM_V2_ALIGNED_SHORT`, and all 31 store `_ENTRY_SYSTEM`.

## 4.3 Recoverability — **partial, and better than §0.2 implied**

| element | recoverable? | how |
|---|---|---|
| the SOFT system prompt text | ✅ **yes, 31/31** | it is built by `_ENTRY_SYSTEM.replace(_WALL_RULE_V1, _WALL_RULE_V2_ALIGNED…)`. The stored base still contains the `_WALL_RULE_V1` block in **31 of 31** rows, so the exact SOFT text is deterministically reconstructible per row, against that row's own era-correct base |
| the user prompt | ✅ yes | stored verbatim and identical for both calls |
| V2 confidence and reason | ✅ yes | they were written into the row by the flip |
| **the V2 raw JSON** | ❌ **lost** | `result['raw']` keeps the V1 response; the second call's raw output was never stored and cannot be reconstructed |
| which gate armed it (LONG vs SHORT aligned) | ✅ yes | derivable from `side` + `trend_1h` + `srv_adx_1h`, which are all stored |

**So past advisor decisions can be replayed** — inputs and system prompt reconstructible, verdict
known — **but not audited against the model's own words**, because the only raw response on file
is the one that was overruled.

## 4.4 Why this matters far more than a logging nit

Seven of the eighteen positions in the book exist **only** because a wall veto was flipped by that
second, unstored call:

| vpos | side | net | R | exit |
|---|---|---|---|---|
| 16 | LONG | −194.70 | −1.146 | sl |
| 17 | SHORT | +0.86 | +0.004 | sl (at BE) |
| 18 | LONG | −234.04 | −1.074 | sl |
| 19 | SHORT | +89.00 | +0.463 | exit_signal |
| 21 | LONG | +33.66 | +0.285 | trail |
| 22 | LONG | −203.42 | −1.064 | sl |
| 24 | SHORT | −234.03 | −1.050 | sl |

```
  opened by a V2/aligned FLIP        n= 7   netR= -3.580   net$=  -742.67   win=3/7
  opened on the V1 verdict alone     n=11   netR= -1.153   net$=  -267.57   win=4/11
  WHOLE BOOK                         n=18   netR= -4.733   net$= -1010.24   win=7/18
```

**39% of the positions, and 74% of the entire loss, were decided by a prompt that was never
stored.** Every one of the four full −1R losses in that group came from a flip.

---

# §5 — EVERYTHING THE PROMPT CARRIES, AND WHAT IT ASSERTS

## 5.1 Present

| field | source | units / labelled? | baseline or percentile? | can it be false when printed? |
|---|---|---|---|---|
| `Symbol` | constant | — | — | no |
| `15m: <name> (direction: X)` | `state_machine` persistent slot | direction labelled; **no timestamp or age** | none | **yes — the slot has no TTL in the prompt.** It shows whatever was last written, with no indication of how old it is |
| `5m trigger: <name> (direction: X)` | the firing webhook | labelled | none | no (see §6) |
| `Combo weight: N.NN` | `signal_weights` | **baseline stated** ("1.0 baseline; <1 = loser, >1 = winner") | 1.0 baseline, **no n** | **yes in effect** — it was exactly 1.00 on 16 of the 18 entries, i.e. "no evidence" is printed identically to "evidence says neutral" |
| `ATR(14) 5m` | Bybit OHLCV | **units unstated** (absolute price) | none | no |
| `Volume ratio 5m` | Bybit OHLCV | "x avg" — avg window unstated | implicit 1.0 | no |
| `ADX(14): 1h \| 15m` | Bybit OHLCV | interpretive band given ("~<20-23 = weak/ranging") | band, not percentile | no |
| `ATR% of price: 1h \| 15m \| 5m` | **Bybit ATR ÷ OKX book mid** | "%" only; **neither venue named** | none | **yes — cross-source ratio presented as one number** |
| `EMA-gap 1h \| 15m (Contracting/Flat)` | Bybit OHLCV | "%" + interpretation | none | no |
| `Market regime: FLAT\|TREND` | `signal_matrix` | **not labelled as signal-presence** | none | **yes — `config.py:346` records it is "provably stuck at FLAT during real ADX>=25 breakouts"** |
| `MTF alignment score` / `vs <DIR>: n/4` | `indicators` | "/4", constituents named | out of 4 | no — and it is the **only** place the trade direction appears |
| `Higher Timeframes Trend` 1d/4h/1h/15m/5m | Bybit OHLCV | labelled "OHLCV-derived, independent of LuxAlgo" | none | no |
| `Order book (pre-trade, 8000 levels)` | **OKX** `books-full`, 4000/side | depth stated; **venue not stated** | wall × multipliers vs side mean — **a real baseline** | **label is correct; the code comment beside it is stale** (claims "depth-100 … Bybit for SOL") |
| `Mid: $X \| Imbalance ±1%` | OKX | labelled | imbalance is a ratio | venue unstated |
| closing: *"The 3 timeframes are aligned (confluence has already passed)"* | hardcoded string | — | — | **YES. False in 31% of prompts by the same prompt's own data, and there are only TWO timeframes shown.** |

## 5.2 Collected, stored on the very same row, and withheld from the model

All thirteen checked categories are **absent** from the prompt; eleven of them are populated on
the same `trades` row at the same instant:

```
  mc_funding_rate        = 0.0001          ABSENT from prompt
  mc_oi_delta_pct        = 0.0             ABSENT
  dxy_trend              = DOWNTREND       ABSENT
  macro_news_category    = NEUTRAL         ABSENT
  macro_gate_penalty     = 0.0             ABSENT
  news_overall           = NEG             ABSENT
  confluence_score       = 4.25            ABSENT
  hw_15m_subtype         = HW_SIGNAL_SHORT ABSENT
  hw_15m_weight          = 1.05            ABSENT
  tape_buy_ratio         = None            ABSENT
  tape_aggression        = None            ABSENT
  1H tier name/direction                   ABSENT
  intended-entry direction as a field      ABSENT
```

Also absent: current price, position size/margin, the 1R risk distance, and any EQH/EQL sweep
state.

## 5.3 The news case is worse than "absent"

`main.py:2238` passes `news_summary = None if _obs_window else _news_summary`, where `_obs_window`
comes from `market_context.is_in_funding_news_observation()`. That function counts:

```sql
SELECT COUNT(*) FROM trades WHERE status='executed' AND (is_virtual IS NULL OR is_virtual=0)
```

— i.e. **non-virtual** executed trades, against `FUNDING_NEWS_OBSERVATION_TRADES = 30`. SOL is
paper, so every entry it takes is `is_virtual=1`. **The counter currently reads 6** (those are the
15m armed-exit close rows, the only non-virtual executed rows the bot writes).

**The window is not "still warming up" — it cannot close while the bot is in paper mode.** News
and funding are fetched, classified, stored and then withheld from the advisor on 100% of
consultations, permanently, by a gate whose release condition counts a kind of trade SOL never
makes. This is the same "flag on, condition unreachable" shape as `FILTER_ENFORCEMENT_ENABLED`
with no filters file, and it is invisible from the config.

---

# §6 — THE 5m TIER SPECIFICALLY

SOL receives **13,046** 5m rows. The prompt handles them as follows:

- **It names the signal that actually fired: 2,935 of 2,945 = 99.66%** (the prompt's
  `5m trigger:` string equals the webhook's `tv_action`). The 10 mismatches are same-second
  concurrent webhooks, the race the `set_trigger_and_snapshot` lock was added to bound.
- **It does not say what class the signal is.** None of `EXECUTION`, `LIQUIDITY`, `MOMENTUM`,
  `TREND`, `category` or `tier` appears anywhere in the prompt. `signal_matrix` classifies every
  signal into exactly those four categories and weights them differently — that classification
  reaches the score gate and never reaches the model.
- **It does not distinguish trigger-capable from context-only.** 634 of the 5m stream are
  `context_recorded` (Group None — they can never open a trade), 37 are suppressed-while-armed,
  and the rest are Group A directional triggers. The prompt says `5m trigger: <name>` in every
  case with no marker of which kind it is.
- **It does not say what else fired recently.** The matrix aggregates multiple concurrent 5m
  signals into the score — vpos 24's matrix showed `EXECUTION` internally conflicted (1.75 long
  vs 2.0 short) and contributing **0.0** — but the prompt shows one name.

So on the 5m tier the model is told *what* fired and *which way it points*, and nothing about
*whether it is the kind of signal that can open a trade*, *how strongly the system weights it*, or
*what contradicted it*.

---

# §7 — PLAINLY: PARTIAL, AND PARTLY WRONG

**The advisor is judging on a partial view.** Precisely what is missing, and how often:

| missing | frequency |
|---|---|
| the 1H tier (name and direction) | **100%** — 2,944/2,944 |
| news and funding context | **100%** — withheld by a gate that cannot open in paper |
| the trade direction as an explicit field | **100%** — appears only inside `MTF alignment vs X` |
| tape, OI, DXY, macro, confluence score, HyperWave weight, size/risk | **100%** — collected, stored, withheld |
| the 5m signal's class and trigger-capability | **100%** |
| the 15m tier name/direction | 5.0% / 5.1% — including **3 of the 18 real entries** |
| the order book | 0.1% |

And what is present but **not true**:

- *"The 3 timeframes are aligned (confluence has already passed)"* — printed on **100%** of
  prompts. Only two timeframes are shown, and in **31%** they point opposite ways. This is the
  clearest instance of the shape asked about: **a label asserting something the data in the same
  prompt does not support.**
- `Market regime: FLAT|TREND` — a signal-presence label the codebase itself documents as stuck at
  FLAT during genuine ADX≥25 breakouts, presented to the model as if it were a regime measurement.
- `ATR% of price` — a Bybit-derived numerator over an OKX-derived denominator, printed as a single
  percentage with neither venue named.

**The measurable consequence** is §3.2: wrong-side reasoning runs at 9.70% inside self-contradictory
prompts versus 0.05% inside consistent ones. And **the least auditable decisions are the most
expensive ones** — the 31 flips carry no record of the prompt that produced them, and the 7 that
became positions account for **74% of the book's loss**.

One thing this does *not* establish: whether feeding the missing fields would improve the
advisor's decisions. Nothing here measures that. What it establishes is that the 97.7% refusal
rate documented at 14:46 is being produced from a view that omits the 1H tier, omits the trade
direction as a field, omits every macro and flow input the bot collects, and closes with an
assertion of alignment that is false roughly a third of the time.

---

# APPENDIX — VERBATIM `ai_user_prompt`, LAST 10 CONSULTATIONS + THE LAST EXECUTE

Reproduced exactly as stored, no edits.

```
########## trades row 14828 @ 2026-08-01 07:35:00 — decide=skip conf=0.92 trade=LONG tv_action='Within Bullish OB'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Up (direction: LONG)
5m trigger: Within Bullish OB (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0497  |  Volume ratio 5m: 2.27x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 21.1 | 15m 12.9  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.448% | 15m 0.146% | 5m 0.068%
  EMA-gap: 1h 0.212% (Contracting) | 15m 0.018% (Contracting)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.248% (Expanding)
  4h: BEAR, ADX 19.1, EMA-gap 0.511% (Expanding)
  1h: BEAR, ADX 21.1, EMA-gap 0.212% (Contracting)
  15m: NEUTRAL, ADX 12.9, EMA-gap 0.018% (Contracting)
  5m: NEUTRAL, ADX 22.0, EMA-gap 0.007% (Contracting)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.94  |  Imbalance ±1%: 0.53 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×23.1), $72.25 (×13.7), $71.75 (×4.4)
  Massive ask walls (>4x avg vol): $73.25 (×15.5), $73.75 (×5.0), $74.25 (×4.8), $79.25 (×4.2)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 14830 @ 2026-08-01 07:35:00 — decide=skip conf=0.92 trade=LONG tv_action='Bullish Liquidity Grab'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Up (direction: LONG)
5m trigger: Bullish Liquidity Grab (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0497  |  Volume ratio 5m: 2.27x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 21.1 | 15m 12.9  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.448% | 15m 0.146% | 5m 0.068%
  EMA-gap: 1h 0.212% (Contracting) | 15m 0.018% (Contracting)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.248% (Expanding)
  4h: BEAR, ADX 19.1, EMA-gap 0.511% (Expanding)
  1h: BEAR, ADX 21.1, EMA-gap 0.212% (Contracting)
  15m: NEUTRAL, ADX 12.9, EMA-gap 0.018% (Contracting)
  5m: NEUTRAL, ADX 22.0, EMA-gap 0.007% (Contracting)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.94  |  Imbalance ±1%: 0.53 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×23.1), $72.25 (×13.7), $71.75 (×4.4)
  Massive ask walls (>4x avg vol): $73.25 (×15.5), $73.75 (×5.0), $74.25 (×4.8), $79.25 (×4.2)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 14831 @ 2026-08-01 07:40:00 — decide=skip conf=0.92 trade=LONG tv_action='Within Bullish OB'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Up (direction: LONG)
5m trigger: Within Bullish OB (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0488  |  Volume ratio 5m: 0.39x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 21.1 | 15m 12.9  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.454% | 15m 0.147% | 5m 0.067%
  EMA-gap: 1h 0.216% (Contracting) | 15m 0.021% (Flat)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.248% (Expanding)
  4h: BEAR, ADX 19.1, EMA-gap 0.511% (Expanding)
  1h: BEAR, ADX 21.1, EMA-gap 0.216% (Contracting)
  15m: NEUTRAL, ADX 12.9, EMA-gap 0.021% (Flat)
  5m: NEUTRAL, ADX 22.0, EMA-gap 0.014% (Expanding)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.94  |  Imbalance ±1%: 0.53 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×23.3), $72.25 (×12.8), $71.75 (×4.5)
  Massive ask walls (>4x avg vol): $73.25 (×16.0), $73.75 (×4.6), $74.25 (×4.8), $79.25 (×4.2)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 14832 @ 2026-08-01 07:45:00 — decide=skip conf=0.92 trade=LONG tv_action='Within Bullish OB'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Up (direction: LONG)
5m trigger: Within Bullish OB (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0467  |  Volume ratio 5m: 0.24x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 21.1 | 15m 12.6  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.454% | 15m 0.137% | 5m 0.064%
  EMA-gap: 1h 0.216% (Contracting) | 15m 0.023% (Expanding)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.248% (Expanding)
  4h: BEAR, ADX 19.1, EMA-gap 0.514% (Expanding)
  1h: BEAR, ADX 21.1, EMA-gap 0.216% (Contracting)
  15m: NEUTRAL, ADX 12.6, EMA-gap 0.023% (Expanding)
  5m: NEUTRAL, ADX 22.3, EMA-gap 0.017% (Expanding)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.94  |  Imbalance ±1%: 0.53 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×23.7), $72.25 (×12.7), $71.75 (×4.5)
  Massive ask walls (>4x avg vol): $73.25 (×15.7), $73.75 (×4.6), $74.25 (×4.8), $79.25 (×4.2)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 14833 @ 2026-08-01 07:50:00 — decide=skip conf=0.92 trade=LONG tv_action='Within Bullish OB'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Up (direction: LONG)
5m trigger: Within Bullish OB (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0440  |  Volume ratio 5m: 0.23x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 21.1 | 15m 12.6  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.454% | 15m 0.138% | 5m 0.060%
  EMA-gap: 1h 0.216% (Contracting) | 15m 0.025% (Expanding)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.248% (Expanding)
  4h: BEAR, ADX 19.1, EMA-gap 0.514% (Expanding)
  1h: BEAR, ADX 21.1, EMA-gap 0.216% (Contracting)
  15m: NEUTRAL, ADX 12.6, EMA-gap 0.025% (Expanding)
  5m: NEUTRAL, ADX 22.8, EMA-gap 0.019% (Expanding)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.94  |  Imbalance ±1%: 0.55 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×24.9), $72.25 (×12.5), $71.75 (×4.4)
  Massive ask walls (>4x avg vol): $73.25 (×15.6), $73.75 (×4.6), $74.25 (×4.8), $79.25 (×4.2)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 14834 @ 2026-08-01 07:55:00 — decide=skip conf=0.92 trade=LONG tv_action='Within Bullish OB'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Up (direction: LONG)
5m trigger: Within Bullish OB (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0490  |  Volume ratio 5m: 0.23x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 21.1 | 15m 12.5  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.454% | 15m 0.143% | 5m 0.067%
  EMA-gap: 1h 0.213% (Contracting) | 15m 0.022% (Expanding)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.248% (Expanding)
  4h: BEAR, ADX 19.1, EMA-gap 0.511% (Expanding)
  1h: BEAR, ADX 21.1, EMA-gap 0.213% (Contracting)
  15m: NEUTRAL, ADX 12.5, EMA-gap 0.022% (Expanding)
  5m: NEUTRAL, ADX 21.8, EMA-gap 0.013% (Expanding)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.94  |  Imbalance ±1%: 0.57 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×26.7), $72.25 (×12.0), $71.75 (×4.3)
  Massive ask walls (>4x avg vol): $73.25 (×15.7), $73.75 (×5.0), $74.25 (×4.9), $79.25 (×4.3)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 14846 @ 2026-08-01 08:45:01 — decide=skip conf=0.92 trade=LONG tv_action='Bullish OB Entered'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Up (direction: LONG)
5m trigger: Bullish OB Entered (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0433  |  Volume ratio 5m: 1.04x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 20.8 | 15m 10.7  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.434% | 15m 0.129% | 5m 0.059%
  EMA-gap: 1h 0.198% (Contracting) | 15m 0.014% (Contracting)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.249% (Expanding)
  4h: BEAR, ADX 19.6, EMA-gap 0.513% (Expanding)
  1h: NEUTRAL, ADX 20.8, EMA-gap 0.198% (Contracting)
  15m: NEUTRAL, ADX 10.7, EMA-gap 0.014% (Contracting)
  5m: NEUTRAL, ADX 14.2, EMA-gap 0.001% (Contracting)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.95  |  Imbalance ±1%: 0.51 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×23.9), $72.25 (×13.0), $71.75 (×4.0)
  Massive ask walls (>4x avg vol): $73.25 (×16.9), $73.75 (×5.1), $74.25 (×4.7), $79.25 (×4.1)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 14970 @ 2026-08-01 15:45:03 — decide=skip conf=0.92 trade=LONG tv_action='Within Bullish OB'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Down (direction: SHORT)
5m trigger: Within Bullish OB (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0539  |  Volume ratio 5m: 0.81x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 22.4 | 15m 20.3  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.363% | 15m 0.129% | 5m 0.074%
  EMA-gap: 1h 0.138% (Contracting) | 15m 0.028% (Contracting)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.271% (Expanding)
  4h: BEAR, ADX 20.6, EMA-gap 0.542% (Expanding)
  1h: NEUTRAL, ADX 22.4, EMA-gap 0.138% (Contracting)
  15m: BEAR, ADX 20.3, EMA-gap 0.028% (Contracting)
  5m: BEAR, ADX 20.6, EMA-gap 0.061% (Expanding)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.78  |  Imbalance ±1%: 0.54 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×18.9), $72.25 (×15.6), $71.75 (×4.1)
  Massive ask walls (>4x avg vol): $72.75 (×10.4), $73.25 (×10.5), $73.75 (×4.2), $74.25 (×4.5)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 14972 @ 2026-08-01 15:55:15 — decide=skip conf=0.92 trade=LONG tv_action='Within Bullish OB'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Down (direction: SHORT)
5m trigger: Within Bullish OB (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0516  |  Volume ratio 5m: 0.59x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 22.4 | 15m 20.3  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.363% | 15m 0.132% | 5m 0.071%
  EMA-gap: 1h 0.137% (Contracting) | 15m 0.022% (Contracting)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.271% (Expanding)
  4h: BEAR, ADX 20.6, EMA-gap 0.543% (Expanding)
  1h: NEUTRAL, ADX 22.4, EMA-gap 0.137% (Contracting)
  15m: BEAR, ADX 20.3, EMA-gap 0.022% (Contracting)
  5m: NEUTRAL, ADX 21.3, EMA-gap 0.054% (Flat)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.81  |  Imbalance ±1%: 0.59 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×21.0), $72.25 (×15.0)
  Massive ask walls (>4x avg vol): $72.75 (×8.0), $73.25 (×10.7), $73.75 (×4.4), $74.25 (×4.7), $79.25 (×4.1)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 14973 @ 2026-08-01 16:00:01 — decide=skip conf=0.92 trade=LONG tv_action='Within Bullish OB'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Down (direction: SHORT)
5m trigger: Within Bullish OB (direction: LONG)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0520  |  Volume ratio 5m: 0.82x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 22.4 | 15m 21.2  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.363% | 15m 0.125% | 5m 0.071%
  EMA-gap: 1h 0.137% (Contracting) | 15m 0.041% (Expanding)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 0
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.271% (Expanding)
  4h: BEAR, ADX 20.6, EMA-gap 0.543% (Expanding)
  1h: NEUTRAL, ADX 22.4, EMA-gap 0.137% (Contracting)
  15m: BEAR, ADX 21.2, EMA-gap 0.041% (Expanding)
  5m: NEUTRAL, ADX 21.8, EMA-gap 0.062% (Flat)
  MTF alignment vs LONG: 0/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.77  |  Imbalance ±1%: 0.57 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×18.4), $72.25 (×17.6), $71.75 (×4.1)
  Massive ask walls (>4x avg vol): $72.75 (×9.2), $73.25 (×10.2), $73.75 (×4.3), $74.25 (×4.6), $79.25 (×4.0)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.

########## trades row 13973 @ 2026-07-29 20:05:03 — decide=execute conf=0.82 trade=SHORT tv_action='Bearish S-CHOCH'
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Down (direction: SHORT)
5m trigger: Bearish S-CHOCH (direction: SHORT)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.2817  |  Volume ratio 5m: 2.72x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 21.5 | 15m 19.7  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.909% | 15m 0.577% | 5m 0.388%
  EMA-gap: 1h 0.281% (Expanding) | 15m 0.186% (Flat)  (Contracting/Flat = compression)
  Market regime: TREND | MTF alignment score: 4
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 11.8, EMA-gap 1.019% (Expanding)
  4h: BEAR, ADX 21.6, EMA-gap 0.881% (Expanding)
  1h: BEAR, ADX 21.5, EMA-gap 0.281% (Expanding)
  15m: BEAR, ADX 19.7, EMA-gap 0.186% (Flat)
  5m: BEAR, ADX 30.9, EMA-gap 0.452% (Expanding)
  MTF alignment vs SHORT: 4/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.66  |  Imbalance ±1%: 0.57 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×11.0), $72.25 (×24.7), $71.75 (×4.7)
  Massive ask walls (>4x avg vol): $72.75 (×14.2), $73.25 (×7.3), $79.25 (×7.5)

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should execute this entry now.
```

---

*All figures from `/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db` opened read-only:
2,944 rows with a stored `ai_user_prompt`, 2,945 with `ai_decision`. Code read at
`claude_advisor.py` (`consult_for_entry`, `_ENTRY_SYSTEM*`, the two aligned-V2 blocks),
`main.py` (`_handle_5m_trigger` enrichment and advisor call), `market_context.py`
(`is_in_funding_news_observation`), `liquidity_zones.py` (`fetch_pre_trade_walls`). No file was
written; the bot was not restarted; Titan was not read or touched.*
