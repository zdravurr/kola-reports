# sol-1h-tier-live-window-restarted-orphan-14981

_2026-08-01 17:25 UTC_

---

# MERCURY-SOL — ✅ 1H TIER IS LIVE AND **CONFIRMED FROM PRODUCTION**. WINDOW RESTARTED AT 0/200.

**Option 1 applied.** `AI_ADVISOR_HIDE_1H` flipped `True` → `False`, service restarted
**17:13:02**, and the flip is **confirmed from a real stored production prompt** — not from the
file. SOL remains PAPER. Titan untouched.

---

# THE ANSWER FIRST

| item | result |
|---|---|
| Flip applied | ✅ `config.py:477` `AI_ADVISOR_HIDE_1H = False`, three-reason comment restored |
| Restart | ✅ **17:13:02**, worker `pid 1126633` |
| **Flip CONFIRMED from production** | ✅ **row 14988, 17:20:01** — carries the 1H line, its age, and **"Of the 3 tier(s) shown"** |
| Orphan set | **{14981}** — size **1**, excluded from the count |
| Window | **1 of 200** as of 17:25 (row 14988) |
| Freeze | ✅ **IN FORCE** from 17:13:02 |
| SOL mode | **PAPER** — proven live in the new pid |
| Titan | **untouched** — git clean, `3316e8a`, active |

**And the very first windowed consultation was an `execute`** — the first since 2026-07-29. Paper
position **vpos 25** is now **open**. That is a genuine change from every prior report in this
sequence, which all said "no open position", and it is called out rather than left to be noticed.

---

# §1 — THE RACE IS REMOVED, NOT RE-RUN

Your diagnosis was right: *requiring zero* consultations makes a clean apply impossible, because
they arrive unpredictably. The condition is now **an accurate count**, and the count is defined by
**the restart itself** rather than by when anyone looked:

> **orphan set ≡ every consultation with `timestamp` in the open interval (16:18:13, 17:13:02)**

That boundary is a fact about the process table, not about my query timing. It cannot race, and it
would have been correct whether the answer was 1 or 5.

**Verified twice, from both sides of the restart:**

| check | when | result |
|---|---|---|
| pre-restart capture | 17:12:32 | count **1** — row 14981 |
| post-restart reconcile against `(16:18:13, 17:13:02)` | after 17:13:02 | count **1** — row 14981 |

Nothing landed in the 30 s between the capture and the restart. **Orphan set size: 1.**

## The orphan set, recorded by row id

| row id | timestamp (UTC) | direction | verdict | form |
|---|---|---|---|---|
| **14981** | 2026-08-01 17:00:01 | SHORT | skip, conf 0.92 | interim **3-of-4** (1H hidden) |

🔴 **Row 14981 is EXCLUDED from the 200 and from every pooled statistic.** It ran on a superseded
prompt form. It is retained as an observation — the only production render the interim form ever
produced — and may be quoted as such, **never counted**. Any later analysis reporting a rate over
"consultations since the prompt fix" must state whether 14981 is in or out. **It is out.**

This is written into `OPEN-ITEMS-SOL.md` by row id, with the same wording.

---

# §2 — THE CONFIRMATION, FROM A RENDERED PRODUCTION PROMPT

You were explicit that the file is not evidence, and §5's hazard is why: `claude_advisor.py:29-32`
wraps the import in `except ImportError: AI_ADVISOR_HIDE_1H = True`, so a broken or renamed config
would **silently re-hide the 1H** rather than fail loudly. A pre-restart import check returned
`False` — but that only proves the import worked in *my* process, so it is not the confirmation.

**The confirmation is row 14988, stored 2026-08-01 17:20:01 — 7 minutes after the restart, in
production, by the live worker.** Verbatim:

```
PROPOSED ENTRY: SHORT
Symbol: SOL/USDT:USDT
1H: 15m-rearm: HyperWave Signal Down (direction: SHORT, set 2.8h ago)
15m: HyperWave Signal Down (direction: SHORT, set 5m ago)
5m trigger: Bearish New Imbalance (direction: SHORT)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0968  |  Volume ratio 5m: 1.23x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 24.9 | 15m 30.3  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.403% | 15m 0.197% | 5m 0.134%
  EMA-gap: 1h 0.222% (Expanding) | 15m 0.138% (Expanding)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 4
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.1, EMA-gap 1.329% (Expanding)
  4h: BEAR, ADX 21.8, EMA-gap 0.606% (Expanding)
  1h: BEAR, ADX 24.9, EMA-gap 0.222% (Expanding)
  15m: BEAR, ADX 30.3, EMA-gap 0.138% (Expanding)
  5m: BEAR, ADX 40.3, EMA-gap 0.137% (Expanding)
  MTF alignment vs SHORT: 4/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.44  |  Imbalance ±1%: 0.57 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.25 (×30.5), $71.75 (×9.2)
  Massive ask walls (>4x avg vol): $72.75 (×16.9), $79.25 (×4.1)

Tier agreement vs SHORT (computed for this consultation):
  1H: 15m-rearm: HyperWave Signal Down -> SHORT = AGREES
  15m: HyperWave Signal Down -> SHORT = AGREES
  5m trigger: Bearish New Imbalance -> SHORT = AGREES
  Of the 3 tier(s) shown: 3 agree, 0 oppose, 0 neutral, 0 absent.
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.
```

Every element you named as the acceptance test is present:

| required | present |
|---|---|
| the **1H line** | ✅ `1H: 15m-rearm: HyperWave Signal Down (direction: SHORT, …)` |
| its **age** | ✅ `set 2.8h ago` — and it is *informative*: the 1H slot was set nearly three hours before the 15m's `set 5m ago` |
| tally reading **"Of the 3 tier(s) shown"** | ✅ `Of the 3 tier(s) shown: 3 agree, 0 oppose, 0 neutral, 0 absent.` |
| `NOT SHOWN` disclaimer gone | ✅ absent |
| **identity only, no statistics** | ✅ no win rate, n, or historical performance against any signal name |

**The flip is confirmed, not merely applied.** The defensive fallback did not fire.

---

# §3 — THE FIRST WINDOWED CONSULTATION WAS AN `EXECUTE`, AND A POSITION IS OPEN

Row 14988 resolved **`execute`, confidence 0.78** — the first execute since **2026-07-29**.

```
3/3 LuxAlgo tiers agree SHORT. All 4H/1H/15m/5m trends BEAR, ADX rising (24.9→30.3→40.3).
EMA gaps expanding across chain. Bid wall is support absorption risk, not skip trigger.
Combo 1.0, volume 1.23x. Execute.
```

**The verdict cites "3/3 LuxAlgo tiers"** — the model is reading the newly complete tier set. That
phrasing was not available to it before 17:13:02.

**Two things to be precise about, because they are easy to overstate:**

1. **This verdict was produced by a WALL-ALIGNED-SHORT-V2 flip, not by the base prompt.** The
   journal shows `[WALL-ALIGNED-SHORT-V2][LIVE] FLIP skip→execute`; V1 had said *skip* on the
   ×30.5 bid wall. So this row also carries the known `ai_system_prompt` V1-storage defect (16:07
   audit §4). That defect is **explicitly out of the freeze** and is not touched here.
2. **n=1 proves nothing about the hypothesis.** This is an *agreeing* prompt (3/3), so it is not
   even in the disagreeing population the prediction is about. It confirms the **mechanics**, not
   the effect.

## The open paper position — vpos 25

| field | value |
|---|---|
| id / side | **25** / **SHORT** |
| entry | **$72.47**, size 137.9, margin $2,000 × 5 = $10,000 notional |
| SL | **$73.20** (original 73.20), initial risk **$100.67** |
| trail | 1.007 %, `breakeven_applied: false` |
| entry row | trades 14988 |
| recheck | `t+10_ok` |

**This is the first position under the 15:38 changes**, so both are now exercised for the first
time:

- **Excursion grid (10 s):** samples are being written — 2 rows in the first ~35 s of the position
  (`elapsed_s` 14.4, 35.4). Under the old 305 s median cadence there would have been **none** yet.
  Early, but the mechanism is confirmed live.
- **Partial-at-arm (⅓ at +1R):** **not yet fired** — `breakeven_applied: false`, the position has
  not reached the +1R arm. Still unproven in execution.

🔴 **Consequence for the record: "no open position" is no longer true.** Every earlier report in
this sequence stated 0 open; that changed at 17:20:20. It is paper, and `MARGIN_USDT` sizes only
virtual fills while `OBSERVATION_MODE=1`.

---

# §4 — PRE-REGISTRATION IN FORCE, FREEZE IN FORCE

Both are written into `OPEN-ITEMS-SOL.md` at the top of the file.

## The window

**Begins at the 2026-08-01 17:13:02 restart, at 0 of 200.** Count consultations with
`timestamp >= 17:13:02`. **Progress at publication: 1 of 200** (row 14988).

## The prediction — baseline, method and n all unchanged

| population | wrong-side rate | n |
|---|---|---|
| book-wide | **3.53 %** | 104 / 2,944 |
| inside prompts whose two visible tiers **disagree** | **9.70 %** | 103 / 1,062 |
| inside prompts whose two visible tiers **agree** | **0.05 %** | 1 / 1,882 |

Matching method unchanged: wrong-side when `ai_reason` names the side opposite the trade, matched
on `opposes <OPP>` / `against <OPP>` / `<OPP> entry` / `for a <OPP>`.

**"Disagree" continues to mean the two ORIGINALLY VISIBLE tiers (15m, 5m)** differ with both
directions present — the looser **n=1,062** definition, **not** the strict n=912. This is
deliberate and load-bearing: it is the only definition comparable to the baseline. **The newly
visible 1H is a treatment, not a re-cut of the population.** Redefining "disagree" to include the
1H would change the denominator mid-experiment and make the comparison meaningless.

🔴 **If the disagreeing-population rate does not fall, the prompt's self-contradiction was NOT the
cause. Record that as-is** — do not explain it away, do not re-cut the population until it agrees,
do not add further prompt fields hoping to move it.

## The freeze — ✅ IN FORCE from 17:13:02, scope kept verbatim

**FROZEN — everything the entry advisor READS.** No additions, removals, reorderings or rewordings
of: the entry user prompt (`consult_for_entry`), the entry system prompts (`_ENTRY_SYSTEM` and
every V2/aligned variant), the model id, temperature or any sampling parameter, and every input
feeding them — `vol_snap`, `market_regime`, `news_summary`, `mtf_alignment_score`,
`pre_trade_walls`, `combo_weight`, `sm_snapshot`. **Also frozen: `AI_ADVISOR_HIDE_1H` itself and
the wall-rule V1/V2 selection.**

**NOT FROZEN — anything the advisor cannot read.** Logging, labels, storage and schema (including
the `ai_system_prompt` V1-storage defect), the exit side in full (`consult_for_close`, trail, SL,
breakeven, partial-at-arm), the HTF cascade, the score gate, the risk gate, the optimizer, the
samplers, the observatory.

🔴 **If a defect is found in the frozen surface during the window: FINISH THE WINDOW and record the
caveat. Do NOT reset the counter.** Same rule as Titan's §2.4-OP, same reason — a criterion that
resets on every finding is unfalsifiable by attrition. Only the operator may break the freeze.

---

# §5 — STATE VERIFICATION

| check | result |
|---|---|
| `AI_ADVISOR_HIDE_1H` | **`False`** (`config.py:477`) — confirmed live via row 14988, not from the file |
| Snapshots | `config.py.bak_hide1h_flip_20260801` and `…flip2_20260801`, both md5 `ea033c86…` = exact pre-flip state |
| `py_compile` | **OK** — `config.py`, `claude_advisor.py`, `main.py`, `virtual_trader.py` |
| Service / worker | **active**; master `1126544`, worker **`1126633` forked 17:13:02** |
| **`OBSERVATION_MODE`** | **True — proven live in the NEW pid**: `[VIRTUAL] poller started in pid 1126633`, whose alternative branch prints `poller not started (live mode)` and returns. **SOL is PAPER.** |
| 15:38 changes still loaded | **yes** — `main.py` 15:31:54, `virtual_trader.py` 15:34:21, `claude_advisor.py` 16:15:42, all predating the 17:13:02 fork; `config.py` 17:12:14 (the flip) also predates it |
| Open positions | 🔶 **1 open** — vpos 25, opened 17:20:20 (was 0 before the restart). 18 closed, max id 25 |
| Window count | **1 of 200** |
| Orphan set | **{14981}**, size 1 |
| **Tor → Bybit** | ✅ `{"retCode":0,"retMsg":"OK","timeSecond":"1785604876"}` |
| **OKX book** | ✅ live, mid ≈ **$72.435** |

**Titan — untouched:**

| check | result |
|---|---|
| `git status --short` | **clean** |
| `HEAD` | **`3316e8a`** |
| `titan.service` | **active** |
| `.py` modified since 16:00 under `/root/titan-bot` | **none** |

No Titan file was read for parameters and none was written.

---

# §6 — WHAT TO WATCH NEXT

1. **The window, to 200.** At the observed rate this is days, not hours. Do not read early numbers
   as a trend — and note the first two data points (14981 orphan, 14988 windowed) are both
   *agreeing* prompts, so they say nothing about the disagreeing population that carries the
   prediction.
2. **vpos 25.** It is the first live test of both 15:38 changes. The partial-at-arm leg has **not**
   fired yet (`breakeven_applied: false`); if the position reaches +1R it will realise ⅓, and the
   known `_execute_armed_exit` accounting caveat applies to the 15m-armed-exit path's own card and
   `trades` row — **`virtual_positions.net_pnl` remains whole and correct**.
3. **The 1H age is doing real work.** Row 14988 showed `1H … set 2.8h ago` against `15m … set 5m
   ago`. The 1H is a persistent slot and can be hours old; the model can now see that. Whether it
   *uses* it is exactly what the window measures.

---

# WHAT CHANGED, IN ONE LINE

`AI_ADVISOR_HIDE_1H True → False` — one line of config, no code change, confirmed live from
production prompt 14988; the 200-consultation window restarted clean at 17:13:02 with row 14981
recorded as the sole orphan; the entry prompt is frozen until the window closes.
