# SOL — HOW MANY TIMES DO WE ASK THE MODEL ABOUT ONE MARKET STATE?

**2026-08-06 12:15 UTC · Mercury-SOL (PAPER) · measurement + a reviewed diff, NOTHING APPLIED**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol` — not a git repo, `.bak` only.
Titan (`/root/titan-bot`, LIVE, HEAD `897850b`) was **not touched, not read for state, not run**.
No file in the SOL tree was modified. `claude_advisor.py` mtime is still `2026-08-04 23:21`.

---

## THE ANSWER IN ONE LINE

**1.25 model calls per market state. 20.2% of every entry consultation SOL has ever made was
redundant. Deduplication is safe: over the full 59-day book it would have cost ZERO positions.**

---

## 0. WHY THE 2026-08-05 ANSWER WAS TO A DIFFERENT QUESTION

The 08-05 measurement said the skip volume is *"a counting artifact, not duplication"* — one write
site, `UPDATE` not `INSERT`, same-timestamp rows are genuinely different TradingView alerts 60–100 ms
apart. **All of that is true and none of it is retracted.** The rows are not duplicates.

But "are these duplicate ROWS" and "how many times do we ask the model about one market state" are
different questions, and the first was answered as though it settled the second. It does not. Three
distinct alerts producing three distinct rows is correct bookkeeping *and* three model calls about
one unchanged market.

### The operator's cards, located — 2026-08-06 **11:25 UTC** (07:25 New York, the box is nyc1)

| row | time | 5m trigger | verdict | the reason given |
|---|---|---|---|---|
| 16294 | 11:25:02 | `Within Bullish OB` | skip 0.92 | *"…massive ask wall $73.75 (×11.7) blocks upside"* |
| 16295 | 11:25:02 | `Bullish I-CHOCH+` | skip 0.78 | *"Ask wall ×11.8 at $73.75 blocks upside. 1h stale."* |
| 16296 | 11:25:05 | `Bullish OB Created` | skip 0.92 | *"…massive ask wall $73.75×11.7 above entry"* |

Identical in all three prompts: `1H: Trend Catcher Down (SHORT, set 8.4h ago, STALE)` ·
`15m: HyperWave OS Signal Up (LONG, set 40m ago)` · combo weight 1.00 · ADX 1h 10.7 / 15m 23.9 ·
Mid $73.40 · regime FLAT · `Of the 3 tier(s) shown: 2 agree, 1 oppose`.

The **only** differences across the three prompts are the 5m trigger's name and the fourth
significant figure of a re-read book (×11.7 vs ×11.8, imbalance 0.55 vs 0.56). Three calls, one
question, one answer, three times.

---

## 1. THE MEASUREMENT

State = same minute + same proposed side + same 1H tier **instance** + same 15m tier **instance**,
where instance = (signal name, direction, derived set-time). A tier refreshed inside the window
starts a new state.

> Two parsing corrections were needed and are recorded so the numbers can be trusted.
> (a) Pre-2026-08-01 prompts render the 15m tier with **no age**, so an age-requiring pattern
> bucketed that whole era as "absent" and over-merged it. (b) The `PROPOSED ENTRY:` line only exists
> from 2026-08-01 17:13, so for the earlier era the **DB `side` column** is the only reliable source
> — reading the side from the prompt merged a LONG and a SHORT consult into one "state". Both fixed
> before any number below was taken.

### 1a — calls per state

| window | calls | states | **calls/state** | max | redundant |
|---|---|---|---|---|---|
| **full book** (06-08 → 08-06, 59.4 d) | 3,328 | 2,656 | **1.253** | 5 | 672 (**20.2%**) |
| 30 days | 2,087 | 1,645 | **1.269** | 5 | 442 (21.2%) |
| since 1H visible (08-01 17:13, 4.8 d) | 390 | 301 | **1.296** | 4 | 89 (22.8%) |
| since stale marker (08-05 00:35, 1.5 d) | 130 | 100 | **1.300** | 3 | 30 (23.1%) |

Distribution over 30 days: **1×: 1,291 · 2×: 277 · 3×: 67 · 4×: 9 · 5×: 1.**

78.5% of states are asked once. Of the 21.5% asked more than once, the mean is **2.25 calls**, and
the worst case is **5 calls for one market state**. The ratio is **rising**, not falling — 1.253 over
the book, 1.300 in the current prompt form.

### 1b — how often the extra calls bought anything

Of **354** multi-call states in 30 days:

- **identical decision: 351 (99.2%)**
  - identical decision *and* identical confidence: 253 (71.5%)
  - identical decision, different confidence: 98 (27.7%)
- **different decision: 3 (0.8%)**

Over the **full book**: 541 multi-call states, verdicts disagree in **3** — **0.55%** of multi-call
states, **0.11%** of all states.

**A state asked four times was answered the same four times. Three of those calls bought nothing.**

### 1c — what actually differs between calls in one state

- only the 5m trigger line: **208 states (58.8%)**
- something else differs too: **146 (41.2%)** — and this is where it matters what "differs" means:

| measure | result |
|---|---|
| seconds between first and last call in a state | median **0.0 s**, p90 3 s, **max 32 s** |
| the whole wall list byte-identical | 275 / 354 (**77.7%**) |
| **nearest opposing wall PRICE changes** | **0 / 353 (0.0%)** |
| its multiple changes in the first decimal | 58 (16.4%) |
| the rendered Mid changes at all | 16 (4.5%) |
| mid drift within a state | median **0.0000%**, max 0.0392% |
| combo weight differs between the calls | 11 (3.1%) — and 96.9% of states are 1.00 across the board |

The residual differences are **the same book re-measured**, not a market that moved. The wall the
model cites as its reason never moves; only its multiple wobbles in the first decimal. **This is one
state, and it is being asked repeatedly within a median of zero seconds.**

### 1d — the cost, plainly

| | calls/day |
|---|---|
| entry consultations today (30-day mean) | **69.6** |
| …in the current prompt form (since 08-05) | **89.1** |
| if one state were asked once (30-day) | **54.8** |
| …current form | **68.6** |
| **saved** | **14.7/day (21.2%) — 20.6/day at the current rate** |

**The two aligned relaxations, costed separately.** Each fires an *extra* model call on a V1 `skip`
that matches a deterministic gate (`ADVISOR_WALL_ALIGNED_V2`: LONG, 1h bull/neutral, ADX≥25, below
the ×20 ceiling; `ADVISOR_WALL_ALIGNED_SHORT_V2`: SHORT, 1h bear, ADX<25). Reconstructed from the
stored gate inputs:

- 30-day total: **37 extra calls**, of which **36 fell in the last 4.6 days** — the rate is not flat.
- Current rate: **7.8 extra calls/day.**
- Verified flips in that same 4.6-day window (rows stamped with an aligned system prompt *after* the
  2026-08-01 21:02:38 provenance fix — earlier rows cannot be read as flips, the stamp was
  unconditional): **3** (ids 15093, 15410, 15412).
- **≈12 extra model calls per flip produced.**
- The ×20 ceiling suppressed 2 calls in the window — it is binding, and it is cheap.

---

## 2. WHAT DEDUPLICATION WOULD COST

### 2a — could a trade be missed? Every case, full book.

Only **3** states in 59 days have disagreeing verdicts. Here they all are.

```
2026-07-08 18:35 SHORT   15m=HyperWave Signal Down     ⚠ first=SKIP, later=EXECUTE
  7974 18:35:05  Bearish I-CHOCH+     skip    0.92   ai_skipped
  7975 18:35:05  Within Bearish OB    execute 0.72   observed_skipped
  7976 18:35:06  Bearish OB Created   execute 0.78   observed_skipped

2026-07-16 07:45 SHORT   15m=Reversal Down             ⚠ first=SKIP, later=EXECUTE
  10256 07:45:01 Bearish OB Mitigated skip    0.78   ai_skipped
  10258 07:45:02 Within Bearish OB    execute 0.72   observed_skipped

2026-07-28 11:05 SHORT   15m=HyperWave Signal Down     (first=EXECUTE — dedup keeps the trade)
  13643 11:05:05 Bearish S-BOS        execute 0.72   observed_skipped
  13644 11:05:05 Bearish I-CHOCH+     execute 0.78   EXECUTED
  13647 11:05:07 Bearish OB Created   skip    0.78   ai_skipped
```

**Two** states where reusing the first verdict would replace an `execute` with a `skip`.
**Zero** of those `execute` verdicts became a position — and not by luck:

- 2026-07-08 18:35 — virtual position **15 (SHORT) was open** (05:05 → 07-09 01:09).
- 2026-07-16 07:45 — virtual position **19 (SHORT) was open** (00:25 → 13:45).

`MAX_POSITIONS_PER_SIDE = 1`, so `virtual_trader.execute_entry` refused both regardless of the
verdict. That is what `observed_skipped` means on those rows.

**Stated honestly: the mechanism that protected those two was the position cap, not the dedup.** If
the cap had been free they would have traded. The measured rate of *"a reuse suppresses an execute
verdict"* is **2 in 59 days**; the measured rate of *"a reuse costs a position"* is **0 in 59 days**.

The mirror case is free: 1 state where the first call said `execute` and a later one said `skip`
(2026-07-28). Under dedup the `execute` stands and the position is still taken — the same one that
was in fact taken.

### 🔴 2a(ii) — A FOURTH DISAGREEING STATE WAS EXCLUDED, AND WHY IT MATTERS

The raw grouping showed a **fourth** state — 2026-06-24 13:25, where a `skip` was followed 4 seconds
later by an `execute` that **did become a position** (row 4370). It is excluded, because it is not a
model disagreement at all:

```
id=4369  side=SHORT   combo_key 5M = 'Bearish I-CHOCH'
                      prompt    5m = 'Within Bullish OB (direction: LONG)'
         the model answered: "LONG into dominant BEAR regime…"
```

**The advisor was asked about a LONG while the bot was proposing a SHORT.** This is the Bug-1
state-machine slot race that `main.py:2560` documents and fixes by capturing the combo key and the
snapshot under one lock. Measured across the whole book:

| | count |
|---|---|
| consult rows with both a combo_key and a rendered 5m line | 3,336 |
| prompt's 5m NAME ≠ combo_key's 5M | **9 (0.27%)** |
| 🔴 prompt's 5m **DIRECTION is the opposite side to the trade** | **7 (0.21%)** — one of them `executed` (id 4259) |
| 15m NAME divergence | 156 → **154 are cosmetic `None` vs `n/a`**; **2 real**, both pre-fix |

**First 2026-06-08 00:40, LAST 2026-06-24 13:25:01, and 2,727 consultations since — clean.**
The race is **closed**, and this is independent confirmation of the fix from the stored evidence.
It is reported here because it silently contaminated the dedup question: without excluding it, the
answer to §2a would have read *"1 position lost"* instead of the correct **0**.

### 2b — the 5m trigger's identity IS load-bearing. What must be preserved.

`combo_key` is built as `1H:…|15M:…|5M:<the 5m trigger name>` (`main.py:2569`) and it is not
decoration:

- `signal_weights.get_weight(combo_key)` (`main.py:3189`) → the **"Combo weight" line in the prompt**
  and `weight_used` on the row.
- `optimizer.py:261` cohorts on `combo_key`.
- `skip_attribution.trades_row_id` is **UNIQUE** — one drift-tracking row per trigger.
- `signal_type` and the Telegram card both name the trigger.
- `silence_digest_sol.py` already counts rows *and* distinct market events side by side (×1.26 on
  `ai_skipped`) — it must keep seeing every row.

**Therefore: deduplicate the MODEL CALL, never the ROW.** Every TradingView alert keeps its own
trades row, its own combo_key, its own skip_attribution row, its own card. Only the second and third
`messages.create` disappear.

One provenance rule must hold, because SOL has already been bitten by exactly its inverse (the
2026-08-01 system-prompt fix: 31 stored decisions named a prompt that did not produce them, 7 of
which became positions carrying −$742.67). **A reused row's `ai_user_prompt` must keep naming the
prompt that actually produced the verdict**, with the row's own rendering stored *beside* it, never
in place of it.

### 2c — the shape of the reuse window (proposed, not implemented)

**A 60-second TTL keyed on the state.** Not "until the 5m tier changes" (the 5m trigger is the thing
that differs — keying on it caches nothing), and not "until the 15m changes" (that is unbounded, and
a 15m tier can hold for hours).

Justification, measured: of 440 redundant calls in 30 days —

| within | share |
|---|---|
| 1 s | 83.9% |
| 5 s | 94.8% |
| 10 s | 97.5% |
| 30 s | 99.8% |
| **60 s** | **100.0%** (max observed gap 32 s) |

60 s is a **2× margin over the worst case ever observed** and captures everything. The key carries
the tier **slot timestamps** (not the rendered ages), so a refreshed tier starts a new state on its
own — no separate tier-change tracking is needed. The nearest opposing wall's **price** is in the
key so a real book shift busts the cache; its **multiple** is not, because that is the same wall
re-measured.

---

## 3. TWO TITAN FINDINGS VISIBLE IN THESE CARDS — REPORT ONLY, NOT FIXED

### 3a — the stale 1H still casts a FULL vote. Titan's sharper half is OPEN on SOL.

SOL marks staleness in the prompt (2026-08-05 00:35) — the label shipped and works. **The tally did
not change, deliberately and on the record.** `_tally[_v] += 1` at `claude_advisor.py:557` is
untouched, and the prompt says so out loud: *"The counts below still treat it as a FULL vote."*

Measured over the **131 current-form prompts**:

| | |
|---|---|
| 1H rendered STALE | **87 (66.4%)** — median age **13.4 h**, max 19.4 h |
| stale 1H **OPPOSES** the proposed side | **68 (51.9% of all prompts, 78.2% of stale ones)** |
| 🔴 tallies reading *"2 agree, 1 oppose"* whose lone opposing vote **is** the stale tier — i.e. **unanimous agreement if it were dropped** | **58 = 44.3% of every current-form prompt** |
| verdicts in this window | **131 skip, 0 execute** |
| verdict reasons that cite staleness | 58 (44.3%) — the model does read the marker |

**Titan's equivalent: `ttl_hours=None`, median rendered age 7.2 h, past the matrix TTL 88% of the
time when it opposed. SOL's 1H is OLDER (13.4 h median) and opposes MORE (78.2%).** Nearly half of
all current prompts present a split tally that would be unanimous if the tier the gate's own TTL
would have discarded were not voting. This is the half Titan called sharper, and on SOL it is open.

Not proposed here: the 08-05 decision to label-not-drop was explicit and reasoned (dropping strips
the arbiter from 56.6% of prompts, and the 200-consultation window measured that *adding* the tier
helped). Changing the **tally** is a third option that decision did not rule on. **Operator's call.**

### 3b — walls are rendered as a bare MULTIPLE. No percentile anywhere.

`0 of 131` current-form prompts contain the word "percentile". The render is
`Massive ask walls (>4x avg vol): $73.75 (×11.7), …` — the multiple and nothing else.

Titan established the raw multiple is meaningless alone. **SOL's own book says the same, harder:**

| | |
|---|---|
| book renders containing **any** wall ≥×4 | **2,087 / 2,087 = 100.0%** |
| containing any wall ≥×10 | 2,076 / 2,087 = **99.5%** |
| distribution of the 14,391 multiples rendered | median **8.0** · p75 13.2 · p90 18.0 · p95 20.6 · p99 26.5 · max 33.8 |

**Every single book state SOL has ever rendered contains a wall above ×4, and 99.5% contain one above
×10.** The ×11.7 wall the model cited three times at 11:25 — the wall that carried all three skips —
sits at the **69th percentile** of walls SOL renders. It is an ordinary wall described in language
("massive", ">4x avg vol") that implies an exceptional one.

Titan's fix `1ec2477` made the percentile primary and per-wall. SOL has the data to do the same:
`skip_attribution` already stores wall *shape* (`opp_wall_next_mult`, `opp_wall_dominance`,
`n_walls_opposing`, `n_walls_supporting`, since 2026-08-02 17:22). **Not fixed in this pass** — it is
a prompt-form change, and one is already in flight from 08-05.

---

## 4. VERDICT

> **1.25 model calls per market state (1.30 in the current prompt form). 20.2% of every entry
> consultation in the book was redundant — 14.7/day today, 20.6/day at the current rate.
> Deduplication is SAFE.**

The evidence for "safe":

1. Verdicts inside a state are identical **99.2%** of the time; they disagree in **0.11%** of all states.
2. The nearest opposing wall's price — the thing the model names as its reason — **never moved**
   inside a state (0 of 353). Mid drift median 0.0000%.
3. Over 59 days, reusing the first verdict would have cost **0 positions**. It would have suppressed
   **2** `execute` verdicts, both already refused by `MAX_POSITIONS_PER_SIDE=1`.
4. 100% of redundant calls arrive within 60 s; the worst gap ever seen is 32 s.

The honest caveat, not argued away: the two suppressed `execute` verdicts were saved by the position
cap, not by the dedup. The rate of a reuse *suppressing an execute verdict* is 2 in 59 days.

§2 shows nothing is lost, so the diff follows. **It is NOT applied.** Reviewed copy:
`/tmp/…/scratchpad/claude_advisor.PROPOSED.py`; the live file's mtime is unchanged.

### The diff — `claude_advisor.py`, three hunks

1. `import threading`, `import time`.
2. Module-level `_STATE_VERDICT_TTL_S = 60.0`, `_state_verdict_cache`, `_state_verdict_lock`,
   `state_verdict_cache_clear()` — the cache is process-local (gunicorn gthread, threads=4) and
   lock-guarded, expired entries swept on every lookup.
3. In `consult_for_entry`: a key built from `(symbol, direction, 1H slot identity, 15m slot identity,
   nearest opposing wall price)` and an early return on a hit **before** `_call`; and a store
   **after** the `system_prompt`/`user_prompt`/`model` stamps, so a reused copy carries the system
   prompt that actually produced it — including an aligned-V2 flip, which replaces both.

Deliberate properties:

- The 5m trigger is **not** in the key. It is the only thing that differs.
- Slot **timestamps**, not rendered ages — a refreshed tier self-invalidates.
- **`unavailable` is never cached.** An API outage must not be pinned for 60 seconds.
- A cache hit does not re-fire the aligned relaxation: the relaxation is part of the verdict, and at
  ≈12 calls per flip, re-asking it per 5m trigger is the same waste twice.
- `user_prompt` keeps naming the prompt that decided; `rendered_user_prompt` carries the row's own.

**Companion change required before this ships (not written):** one nullable column so the reuse is
visible in the data rather than only in the log — `ai_verdict_reuse_json`, holding
`{reused, age_s, from_5m, from_at, rendered_user_prompt}`. Without it a reused row looks like a
normal consultation and the next audit will mis-count model calls the way this one nearly did.

### The patch was tested, not just parsed — 8/8

| test | result |
|---|---|
| the operator's 11:25 state, 3 triggers | **1 model call, was 3** |
| refreshed 15m tier → new state | re-asks ✅ |
| opposing wall **moves** → new state | re-asks ✅ |
| same wall re-measured ×11.7→×11.8 | reuses ✅ |
| opposite side never reuses | re-asks ✅ |
| `unavailable` never cached | re-asks ✅ |
| TTL expiry | re-asks ✅ |
| provenance: `user_prompt` = the prompt that decided, `rendered_user_prompt` = the row's own | ✅ |

### Open, for the operator

1. **Apply the dedup?** Diff reviewed and tested; needs the companion column and a `.bak` snapshot
   (SOL is not under version control).
2. **§3a — the stale 1H's full vote**, which turns 44.3% of current prompts from unanimous into
   split. Titan called this the sharper half. The 08-05 decision covered the *label*, not the *tally*.
3. **§3b — per-wall percentile.** 100% of book states contain a ×4 wall; the data to compute the
   percentile is already stored.
4. **The aligned relaxations at ≈12 calls per flip** — worth keeping at that price is a separate
   decision, now costed.

**Nothing in `/root/titan-bot` was read for state, modified, or run.**
