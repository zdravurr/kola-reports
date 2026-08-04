# MERCURY-SOL — THE SKIP VOLUME IS COUNTING, THE 1H ARBITER IS STALE, AND THE NEWS GATE OPENS AT ~13 ROUND TRIPS

**2026-08-05 00:10 UTC** · subject: **Mercury-SOL** (`/mnt/volume_nyc1_1780480650620/mercury-sol`), PAPER.
**Items 1 and 2 were READ-ONLY — nothing was edited, nothing restarted. Item 3 applies nothing.**
**Titan untouched.**

---

# §1 — WHY SO MANY `ai_skipped` ROWS

## 1a. The calls, counted per branch

Branch invocations are not stored, so they were **reconstructed** from the same deterministic gates
the code uses — then **validated against journald**, which retains from 2026-08-02 19:55:

| | aligned-LONG | aligned-SHORT | V1 shadow |
|---|---|---|---|
| reconstruction | 0 | **10** | 0 |
| journald (ground truth) | 0 | **10** | 0 |

**Exact match — the reconstruction is trustworthy.**

### Today, 2026-08-04

| branch | calls |
|---|---|
| base entry consult | **90** |
| `ADVISOR_WALL_RULE_V2_DRYRUN` (muted 08-02) | **0** |
| aligned-LONG relaxation | **0** |
| aligned-SHORT relaxation | **0** |
| **exit advisor (`consult_for_close`)** | **0** |
| **TOTAL** | **90 calls / 90 signals = 1.00 calls per signal** |

**The exit advisor has never run — not today, not once in the book's history.** `_handle_5m_close`
always inserts a `5m_group_b` row before consulting, and **there are zero such rows, ever**. It needs a
Group-B 5m webhook to arrive *while a position is open*; that has not happened in 21 round trips.

### Before vs after the 2026-08-02 shadow mute

| period | signals | total calls | **calls/signal** |
|---|---|---|---|
| 7 days BEFORE the mute | 423 | 929 | **2.20** |
| since the mute | 189 | 199 | **1.05** |

**Call volume fell ~55%.** The muted shadow fired on *every* base skip — it was the doubling.

## 1b. 🔴 DOES ONE SIGNAL PRODUCE MORE THAN ONE ROW? — NO

**The write path forbids it.** There is exactly **one** `ai_skipped` write site:

- `insert_signal(...)` (`main.py:2618`) **creates** one row per inbound webhook and returns `row_id`
- `update_trade(row_id, status='ai_skipped', ...)` (`main.py:3261`) **mutates that same row**

`update_trade` is an `UPDATE ... WHERE id=?`. A base consult that skips and a relaxation that also
skips both write into **one `result` dict** and then **one row**. There is no code path that inserts a
second row for a second verdict.

**So what are the same-timestamp pairs?** They are **different signals**, not duplicate writes:

| row | timestamp | `tv_action` | `combo_key` (5m leg) |
|---|---|---|---|
| 14997 | 18:25:01.324 | **Bearish I-BOS** | `…5M:Bearish I-BOS` |
| 14998 | 18:25:01.385 | **Bearish OB Created** | `…5M:Bearish OB Created` |

TradingView fires **several distinct alerts on one bar close**, 60–100 ms apart. Each is a genuine
separate trigger, gets its own row and its own advisor call. **Yes — this is the same phenomenon as
§1d's 17.5% of window rows sharing a timestamp.**

**True duplicates (the same `tv_action` repeated inside one burst): 3 pairs in 3,124 rows — 0.1%**, all
from a single incident on 2026-07-23 08:45:41→08:46:07 (four `Within Bearish OB` in 26 s). Not systemic.

### 🔴 THE DEDUPLICATED COUNT, PLAINLY

| | rows | distinct market events | rows per event |
|---|---|---|---|
| whole book | **3,124** | **2,490** | **1.26** |

**The operator's "too many skips" IS a counting artifact — but not a duplication bug.** The inflation
factor is **1.26×**, and it comes from one bar close producing several distinct alerts. Nothing is
being written twice. The honest headline: *SOL skipped ~2,490 market moments, recorded as 3,124 rows.*

## 1c. Has the RATE changed? — NO

| window | rows/day | events/day | rows/event |
|---|---|---|---|
| **last 7 days** (07-29 → 08-04) | **67.9** | 53.7 | 1.26 |
| **30-day norm** (07-06 → 08-04) | **65.7** | 51.9 | 1.27 |
| before the mute (07-06 → 08-01) | 64.6 | 51.3 | 1.26 |
| after the mute (08-02 → 08-04) | 75.3 | 57.7 | 1.31 |

**Last 7 days are +3.3% on the 30-day norm — noise.** The rows/event ratio is flat at ~1.26 across
every period, so the inflation is longstanding, not new.

**Today looks high and isn't.** 90 rows against a 30-day mean of 65.7 with **sd 25.9** (range 18–141):
**z = +0.94**, and **5 of the last 30 days were at or above it**. Daily variance on this book is large.

**Only the appearance changed — and it changed in the cheap direction:** the mute cut calls 55% while
row count stayed flat, so cost per row roughly halved while the row count kept looking the same.

## 1d. The two aligned relaxations — updated

**Invocations** (reconstructed, journald-validated):

| window | aligned-LONG | aligned-SHORT |
|---|---|---|
| whole book | 478 | 198 |
| since 2026-08-01 | 19 | 13 |
| since the 08-02 mute | **0** | **10** |
| last 7 days | 45 | 33 |

**FLIPs — reported only where provenance is trustworthy** (the system-prompt stamp was fixed
2026-08-01 21:02; before that every row stored the V1 base regardless of what produced it, so earlier
flips are **not** identifiable this way):

| arm | flips since 2026-08-01 21:02 | rows |
|---|---|---|
| aligned-LONG | **1** | 15093 → **vpos 26** |
| aligned-SHORT | **2** | 15410, 15412 → **vpos 27** |

**So "37 invocations, 0 FLIPs as of 08-01" is now 3 flips**, and both flipped positions lost
(vpos 26 −1.085R, vpos 27 −0.66R).

### The ×20 ceiling, reported separately as asked

The ceiling suppresses aligned-LONG invocations **before** the model call:

| window | would-suppress | of aligned-LONG invocations |
|---|---|---|
| whole book (retrospective) | **25** | 478 (**5%**) |
| last 7 days | **4** | 45 (**9%**) |

*(Yesterday's report quoted 29 of 486 — that denominator was "consults reaching the gate" including
those where the base verdict was `execute` and no relaxation is ever invoked. **25 of 478** is the
invocation-based figure and the correct one. The nearest-wall and any-wall readings still block an
identical set on this denominator too.)*

## 1e. What the advisor cites when it skips

Non-exclusive — one reason usually cites several grounds, so shares exceed 100%.

| ground | whole book (n=3,124) | last 7 days (n=475) | today (n=90) |
|---|---|---|---|
| **opposing order-book WALL** | **95.1%** | **93.5%** | 88.9% |
| tier disagreement / opposes | 71.2% | 70.9% | 80.0% |
| FLAT / ranging regime | 64.7% | 70.3% | 91.1% |
| weak ADX / no trend strength | 63.1% | 73.9% | **95.6%** |
| counter-trend vs HTF | 51.7% | 46.3% | 24.4% |
| EMA compression / contracting | 41.1% | 44.8% | 35.6% |
| low volatility / small ATR | 14.4% | 20.6% | 28.9% |
| volume too thin | 9.5% | 5.5% | 0.0% |
| unfavourable risk/reward | 0.6% | 0.2% | 0.0% |
| imbalance against the trade | 1.1% | 1.3% | 1.1% |

**The order-book wall is the dominant veto — cited in 95% of all skips**, and it is the top ground on
six of the last seven days. Today was the exception (weak ADX, 95.6%).

---

# §2 — DO THE SIGNALS UNDERSTAND EACH OTHER?

## 2a. Last 20 consultations — all complete

All 20 carry **name + direction + age** for 1H and 15m, and **name + direction** for the 5m.
**The 5m carries no age by design** — it is the signal that just fired, so its age is ~0 by
construction (`claude_advisor.py:356`). That is a designed exception, not a gap.

```
row 15814  2026-08-04 20:55:05  [ai_skipped]
    PROPOSED ENTRY: SHORT
    1H: Trend Tracer Up (direction: LONG, set 21.9h ago)
    15m: HyperWave Signal Down (direction: SHORT, set 55m ago)
    5m trigger: Within Bearish OB (direction: SHORT)

row 15786  2026-08-04 19:15:11  [ai_skipped]
    PROPOSED ENTRY: SHORT
    1H: Trend Tracer Up (direction: LONG, set 20.3h ago)
    15m: HyperWave Signal Up (direction: LONG, set 45m ago)
    5m trigger: Bearish OB Entered (direction: SHORT)
```

🔴 **Look at the ages.** The 1H tier is **20–22 hours old** on every one of the last 20. That is §2e.

## 2b. Whole book — completeness per tier

| tier | line absent | name `n/a` | direction `n/a` | no age |
|---|---|---|---|---|
| **1H** | 2,946 (92.1%) | 0 | 0 | 0 |
| **15m** | 0 | 147 (4.6%) | 147 (4.6%) | 2,946 (92.1%) |
| **5m** | 0 | 0 | 0 | 3,197 (100%) — *by design* |

The 92.1% figures are the pre-flip era (`AI_ADVISOR_HIDE_1H=True`, and the 15m age only added 08-01).

**Post-flip (251 consultations):**

| tier | line absent | name `n/a` | direction `n/a` | no age |
|---|---|---|---|---|
| 1H | 0 | 0 | 0 | 0 |
| 15m | 0 | **1 (0.4%)** | 1 (0.4%) | 1 (0.4%) |
| 5m | 0 | 0 | 0 | 251 — *by design* |

By status: `ai_skipped` 246 complete / 1 incomplete · `executed` 3/0 · `observed_skipped` 1/0 —
**99.6% complete.** When a name is missing the direction is missing too; they fail together.

## 2c. Titan's TTL-label defect — **SOL does NOT have it**

Grep for `"TTL expired"`, `"NOT counted by the gate"`, `"matrix TTL"` across the tree: **no match.**
SOL's renderer never asserts a cause for a missing tier, so it cannot assert a false one.

**How SOL's three states actually render:**

| state | renders as | distinguishable? |
|---|---|---|
| slot **absent** | `n/a (direction: n/a)` → tally `ABSENT` | ✅ |
| slot **expired** | name preserved, `direction: NEUTRAL` (`get_snapshot`, `state_machine.py:459`) | ✅ |
| **intra-conflict** | never reaches the prompt — it is a *matrix* concept (`signal_matrix.py:299`), collapsed to `net_direction=NEUTRAL, contribution=0.0`, and the matrix breakdown is not in the entry prompt at all | n/a |

**Verdict: SOL does not collapse three states under one false string. Titan lied; SOL is silent.**

🔴 **But there is a worse SOL-specific hole, and it is the subject of 2e:** the expired→NEUTRAL
mechanism **is disabled for two of the three tiers**. `1h_context` and `5m_trigger` carry
`ttl_hours = None`, so `_is_expired_locked` returns `False` unconditionally for them. **Those tiers can
never render as expired, at any age** — their staleness is visible only in the age string.

## 2d. Direction field and tally — both sound; the score card is fixed and live

| check | result |
|---|---|
| `PROPOSED ENTRY:` present as first line | **251 / 251** |
| `PROPOSED ENTRY` disagreeing with the DB `side` | **0** |
| agreement tally arithmetically consistent with its own tier lines | **251 / 251**, 0 mismatched |

**The `score=2.25 < thr=2.0` card: FIXED.** `main.py:2898` now prints the *deciding* quantity —
`score=2.25 | macro -0.50 → 1.75 < thr=2.0` — instead of the raw score against the gated threshold.
The old card printed `direction_score` while the gate compared `_gate_score` (raw + macro penalty),
which is why the printed inequality was arithmetically false.
**And it is LIVE:** `main.py` mtime **13:23:55**, worker booted **22:48:27** — the fix precedes the boot.

## 2e. 🔴 DO THE TTLs AGREE? — **NO. SOL HAS TITAN'S TWO-REGISTRY DIVERGENCE, AND IT IS WIDER**

| tier | state-machine slot TTL | matrix `CATEGORY_TTL_MINUTES` | agree? |
|---|---|---|---|
| **1H** (`1h_context`) | **`None` — never expires** | `TREND` = 360 min (**6h**) | ❌ |
| **15m** (`15m_confirm`) | **4 h** | `MOMENTUM` = 90 min (**1.5h**) | ❌ — *exactly Titan's shape* |
| **5m** (`5m_trigger`) | **`None` — never expires** | `EXECUTION` = 5 min | ❌ |

**Measured on the 251 rendered post-flip prompts:**

| | share |
|---|---|
| 15m tier inside the divergence band (90 min < age ≤ 4 h) | **23 / 250 = 9.2%** |
| **1H tier older than the matrix TREND TTL (> 6h)** | **142 / 251 = 56.6%** |
| 1H median age | **7.2 h** (max **21.9 h**) |
| **1H OPPOSES the proposed side** | 92 / 251 = 36.7% |
| …**of those, already past the matrix TREND TTL** | **81 / 92 = 88.0%** |

🔴 **The consequence, stated plainly.** The 1H tier was added on 2026-08-01 specifically to give the
model **an arbiter in the disagreeing population**. That arbiter is **stale more than half the time**,
and **when it opposes the trade it is stale 88% of the time** — a "Trend Tracer Up" from 21.9 hours ago
counts as a full `OPPOSES` vote in a tally the prompt presents as current. The matrix would not count
that tier at all.

This did **not** prevent the §1 wrong-side improvement (which stands). It is a separate defect, and it
means the tally's authority is weaker than its wording implies. **Reported, not fixed — read-only item.**

---

# §3 — THE NEWS GATE (decision item; nothing applied)

## 3a. The exact counting rule — and it is NOT round trips

```python
# market_context.py:288-295
row = conn.execute(
    "SELECT COUNT(*) FROM trades "
    "WHERE status='executed' "
    "AND (is_virtual IS NULL OR is_virtual=0)").fetchone()
return count < FUNDING_NEWS_OBSERVATION_TRADES        # config.py:209 → 30
```

Wired as `_claude_news = None if _obs_window else _news_summary` (`main.py:2728`), passed to the
advisor as `news_summary=` (`main.py:3081`). On exception it **fails safe to `True`** (stays closed).

🔴 **It counts ROWS, and BOTH sides of a trade write `status='executed'`.** Measured on the real book:

| | count |
|---|---|
| closed positions | **21** |
| entry-side `executed` rows (`open_*`) | 21 |
| close-side `executed` rows (`sl_triggered_*`, `exit_*`) | 21 |
| arm-side `executed` rows (`15m_armed_exit`) | 6 |
| **total `executed` rows** | **48** → **2.29 rows per round trip** |

**So the threshold of 30 rows opens after ≈ 13 round trips** (15 if nothing ever arms; 13.1 at the
book's observed arming rate). **The operator's "roughly a dozen" is right, and the constant reading
`30` is misleading** — it is not 30 trades.

Currently **0 / 30**: all 48 rows are `is_virtual=1`. While SOL is paper the count **cannot advance**.

## 3b. What it would add, verbatim

```python
# claude_advisor.py:451-452
if news_summary:
    user += f"\nRecent news (last 2h):\n{news_summary[:500]}\n"
```

It is inserted **after the order-book block and before the tier-agreement block**. Real shape, from a
stored summary:

```
Recent news (last 2h):
[NEU] Jim Cramer Is Selling His Bitcoin Over Quantum Threat—Crypto Twitter Is Thrilled
[NEG] SpaceX tops Wall Street revenue forecast, posts $540 million loss on bitcoin holdings
[POS] US, UK reaffirm support for stablecoins, tokenization in joint financial regulation talks
...
Overall: MIXED (score=+0.15, impact=medium)
Pulse: Regulatory tailwinds offset macro headwinds; quantum/security concerns weigh slightly negative.
```

🔴 **A defect that must be priced into any of the three options: the `[:500]` cut.**
Stored summaries average **569 chars** and **50.7% exceed 500**. The `Overall:` and `Pulse:` lines —
the only *aggregate judgement* in the block, and the part actually worth showing — sit at the **end**,
so on **half of all consultations they would be cut off entirely**, leaving a truncated headline list
ending mid-word (`"…Cloudflare kic"`). As it stands the block delivers raw headlines without the
verdict half the time.

## 3c. The three options

### Option A — let it open on its own
- **Cost:** the entry prompt changes **silently mid-live-book** — no commit, no restart, no report, at
  a moment set by trade frequency rather than by decision. The live book splits at an **unmarked
  boundary** (~round trip 13) into no-news and news eras, so any comparison across it is confounded
  exactly where it starts costing real money. Half the renders carry the truncated block.
- **Benefit:** no work.
- **Note:** this is the only option that is **not a decision** — it is the default that happens if
  nothing is chosen.

### Option B — pin the constant so it cannot open
- **Cost:** news stays withheld indefinitely; whatever value it holds is forgone, and the enrichment
  keeps being collected and stored for nothing. Requires an edit (+ `.bak`).
- **Benefit:** the live book is **homogeneous from row one**, and the prompt can then only change by
  explicit decision. Fully reversible; the ten other withheld fields are already in this state, so it
  is also the *consistent* one.

### Option C — open it deliberately at the flip
- **Cost:** the live book then starts on a prompt form that **has never been measured** — the
  200-consultation window result was obtained **without** the news block, so its finding would not
  transfer to the live prompt. The `[:500]` truncation should be fixed first, or the deliberate change
  ships a known defect on purpose.
- **Benefit:** one decision, one boundary, at the one moment where a discontinuity is already expected;
  the live book is homogeneous **and** carries news from row one.

**Whichever you choose, the `[:500]` truncation is worth fixing if news is ever to be shown** — the
current form drops the verdict lines on half the renders, which is the worst of both worlds.

**Nothing in this item was applied.**

---

## WHAT I DID AND DID NOT DO

- **Items 1 and 2: strictly read-only.** No file edited, no service restarted, no config changed.
- **Item 3: analysis only** — no constant pinned, no gate touched.
- Titan not touched and not read for parameters.
- Findings left open by design: the **1H/15m/5m TTL divergence** (§2e) and the **`[:500]` news
  truncation** (§3b) are reported, not fixed.
