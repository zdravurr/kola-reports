# MERCURY-SOL — THE STALE 1H IS LABELLED, THE NEWS GATE IS PINNED, AND SILENCE NOW REPORTS ITSELF

**2026-08-05 00:35 UTC** · subject: **Mercury-SOL**, PAPER, not under version control.
**One restart, from flat, at the end** — worker pid **2203165**, booted 2026-08-04 23:33:20 UTC.
**Titan untouched: HEAD `b9081ad`, working tree clean, service active.**

All three items come from the 00:10 report (`2026-08-05-0010-sol-skip-volume-is-counting-…`).

---

# §1 — THE STALE 1H TIER IS LABELLED, NOT DROPPED

## What was wrong

`1h_context` carries `ttl_hours=None`, so it never expires and always renders a definite LONG/SHORT.
The matrix drops the same tier after `CATEGORY_TTL_MINUTES['TREND']` = 360 min. Measured over 251
rendered prompts: **56.6% carried a 1H past that window** (median 7.2h, max 21.9h), and where it
**OPPOSED** the proposed side it was past it **88%** of the time. A 21.9h-old tier was casting a full
`OPPOSES` vote in a tally the prompt presents as current.

## a) The tier line

When the age exceeds 360 min, the line now reads:

```
1H: Trend Tracer Up (direction: LONG, set 21.9h ago, STALE — past the 6h window the gate itself uses for this tier)
```

Live (≤ 360 min) it is **byte-identical to before**:

```
1H: Trend Tracer Up (direction: LONG, set 2.0h ago)
```

The marker reads `CATEGORY_TTL_MINUTES` — **the gate's own constant** — deliberately. A second
hardcoded `360` here would have been exactly the two-registry divergence the marker exists to expose.

## b) 🔴 THE TALLY — the sharper half

Per-tier row, and one explicit sentence before the counts:

```
Tier agreement vs SHORT (computed for this consultation):
  1H: Trend Tracer Up -> LONG = OPPOSES  [STALE: set 21.9h ago, past the 6h window]
  15m: Reversal Down -> SHORT = AGREES
  5m trigger: Within Bearish OB -> SHORT = AGREES
  NOTE: 1 of the tiers above is/are STALE (1H) — older than the window the gate uses for that
  tier. The counts below still treat it as a FULL vote; weigh it accordingly.
  Of the 3 tier(s) shown: 2 agree, 1 oppose, 0 neutral, 0 absent.
```

**THE COUNTS DID NOT CHANGE.** `_tally[_v] += 1` is untouched and does not appear in the functional
diff. Proven by executing the real `consult_for_entry` at four ages:

| 1H age | marker | tally |
|---|---|---|
| 2.0h | silent | `2 agree, 1 oppose, 0 neutral, 0 absent` |
| 5.9h (just inside) | silent | identical |
| 6.1h (just past) | **fires** | identical |
| 21.9h | **fires** | identical |

Boundary is *exceeds* 360 min, as specified. Filtering the vote instead would have silently redefined
the tally mid-book and undone, on the stale half, the very arbiter the 200-consultation window showed
helps.

## c) The 5m tier — it cannot be stale, so no marker was added

- `set_trigger_and_snapshot` writes the slot with `now_iso` and returns the snapshot **under the same
  lock**, so the age is bounded by one request.
- `consult_for_entry` has exactly **one call site**, fed by that snapshot.
- Empirically: **`5m trigger: n/a` occurs in 0 of 3,199 stored consults.**

A marker there would be dead code, so it was not added — the answer to "if it can ever be stale" is
**it cannot**, and that is documented in the file rather than implemented.

## d) Nothing else changed — and one thing deliberately left open

The 15m and 5m lines are byte-identical, no field was added, removed or reordered, and the §1
analysis parsers (the 15m-vs-5m disagree definition) still read the new form correctly — verified.

🔶 **OPEN, and named rather than quietly folded in:** the **15m** has its own divergence (slot 4h vs
matrix MOMENTUM 90 min) — **9.2%** of prompts, max observed age 3.0h. It was **outside the decision
taken**, so it is **not** marked. Enabling it is one dict entry (`'15m': 90.0`). That is a decision
for you, not a cleanup for me.

⚠️ **This is a new prompt form.** The 200-consultation window result belongs to the *previous* form.
The boundary is recorded now, deliberately — an unmarked prompt change is precisely the failure §2
exists to prevent.

---

# §2 — THE NEWS GATE IS PINNED (Option B)

## a) What changed

| file | change |
|---|---|
| `config.py` | **`NEWS_OBSERVATION_PINNED = True`** (new), with the decision and the rejected alternatives recorded in place |
| `market_context.py` | `is_in_funding_news_observation()` returns `True` immediately when the flag is set — **checked before the row count** |

**Proven, not asserted.** With the threshold forced to `0` — which would otherwise open the gate:

```
pin OFF, threshold forced to 0 -> False   (news WOULD reach the prompt)
pin ON,  threshold forced to 0 -> True    (still withheld)
```

So the pin overrides the counter no matter how many live trades accumulate.

**Collection and storage are untouched — we withhold from the prompt, we do not switch it off.**
Verified: **92 of 92** consultations on 2026-08-04 stored `news_summary` and `news_score` while the
gate was closed. The enrichment keeps flowing to the optimizer exactly as before.

## b) Recorded in canon: the constant's name is misleading

`FUNDING_NEWS_OBSERVATION_TRADES = 30` reads as "30 trades". **It counts ROWS**, and **both legs of a
round trip write `status='executed'`**, as does the arm step:

| | count |
|---|---|
| closed positions | 21 |
| entry rows + close rows + arm rows | 21 + 21 + 6 = **48** |
| **rows per round trip** | **2.29** |

**So it opens after ≈13 round trips, not 30.** That misleading name is the whole reason this needed a
decision instead of being left alone — written into `config.py` and `OPEN-ITEMS-SOL.md` so the next
reader cannot repeat the mistake.

## c) Recorded as a precondition, deliberately NOT fixed

Before this flag is ever set `False`, the **`news_summary[:500]`** truncation must be fixed. Stored
summaries average **569 chars**, **50.7% exceed 500**, and the `Overall:` / `Pulse:` verdict lines —
the only aggregate judgement in the block — sit at the **END**. Half of all renders would drop exactly
that and end mid-word (`"…Cloudflare kic"`).

**Not fixed today, on purpose:** it is code that cannot run while the flag is True, and the pre-flip
change surface stays minimal. Recorded in both `config.py` and canon as a hard precondition.

---

# §3 — SILENCE LEDGER: `silence_digest_sol.py`

**Standalone.** Not part of `main.py`, imports nothing from it, opens the DB **read-only**
(`file:…?mode=ro`). It cannot affect a trading decision, and if it breaks the bot does not.
**Cron: `20 8 * * *` UTC** — 15 min after Titan's 08:05 so the two daily messages stay distinct.
Titan's cron line verified still present and unmodified.

## Rendered from real data (24h to 2026-08-04 23:30) — before applying

```
🔇 MERCURY-SOL — SILENCE LEDGER
window: last 24h → 2026-08-04 23:30 UTC
mode: PAPER (OBSERVATION_MODE=1) · open positions: 0

WHY IT WAS QUIET — per cause
  webhooks logged    274 rows → 155 market events (×1.77)
  ├─ bookkeeping      35  (slot writes, never an entry attempt)
  └─ entry attempts  228 rows → 137 events
       ├─ 1H trend not set          4
       ├─ HTF cascade vetoed       68
       ├─ score below threshold    63
       └─ reached the advisor   93
             ├─ ADVISOR DECLINED           93  (100% of those)
             └─ EXECUTED                    0
  advisor declines: 93 rows → 68 events (×1.37; book-wide norm ×1.26)

EXIT SIDE
  exit signal, nothing armed      7

WHAT THE ADVISOR CITED (of 93 declines; one reason cites several)
  weak ADX / no trend strength     89  (96%)
  FLAT / ranging regime            85  (91%)
  opposing order-book wall         83  (89%)
  tier disagreement                75  (81%)

⚠️ UNCLASSIFIED STATUSES (not in the ledger's ladder — shown so nothing is silently dropped)
  pending                           4

VERDICT: largest single cause = ADVISOR DECLINED, 93 of 228 entry attempts (41%).
  gates stopped 135 before the advisor; of the 93 that reached it, it declined 93 (100%).
```

**Design choices worth stating:**

- **Rows AND events, side by side**, so the number he sees matches the number that exists. Two
  different ×-ratios would otherwise collide in his head, so both are labelled: the funnel ratio
  (×1.77, spans every status) and the `ai_skipped`-only ratio (×1.37 today, **book-wide norm ×1.26** —
  the figure from §1b of the 00:10 report).
- **Unclassified statuses get their own block.** A ledger that quietly drops a status it does not know
  is the same defect class it exists to catch — it surfaced `pending` (4) on the first real render.
- **The verdict names the dominant cause and the advisor's share of what reached it**, because
  "largest bucket" alone would have hidden that the gates killed 135 before the advisor ever saw them.
- **Empty window** renders `NOTHING ARRIVED AT ALL — the silence is upstream of every gate`, so a dead
  webhook path cannot look like a quiet market. Verified.
- Sent with `require_link=False`: this is an operational **alert**, not a report. Gating it on a raw
  link would silence the very thing that reports silence.

---

# RUNTIME CONFIRMATION (after the single restart)

| check | result |
|---|---|
| `OBSERVATION_MODE` | **True** (paper) |
| ×20 ceiling | **20.0** |
| `ADVISOR_WALL_ALIGNED_V2` / SHORT companion | True / True |
| `NEWS_OBSERVATION_PINNED` | **True**, news withheld right now |
| **geometry** | `SL_BUFFER_ATR 2.5` · `TRAIL_MULT_ATR 2.5` · `ATR_TF 1h` · `TRAIL_ACTIVATION_ATR_FIXED 5.0` · `PARTIAL_AT_ARM 1/3` · `MARGIN 2000 × LEV 5` |
| geometry byte-check | `config.py` lines 40–120 **byte-identical** to the pre-edit snapshot |
| open positions / pending exits | **0 / 0** — restart taken from flat; boot log: *"no open paper positions at boot — clean"* |
| OKX (advisor book) | **reachable** — mid 73.78, depth 8000, 5 bid + 3 ask walls |
| Tor | **reachable** — `{"IsTor":true,"IP":"192.42.116.95"}`, service active |
| **Titan** | **HEAD `b9081ad`, tree clean, service active — untouched, not read for parameters** |
| worker holds the new code | all four files' mtimes (23:21–23:30) **precede** boot 23:33:20 |

⚠️ **One honest limit.** The stale marker is **armed and proven by executing the real code path**, but
it has **not yet been observed in a production prompt**: the 1H slot is currently **52 min old**, so
the marker correctly stays silent, and the post-restart signals so far died at the score gate before
reaching the advisor. Given the 1H was past the window on 56.6% of prompts, it will fire within hours.
**Reported as armed, not as observed live** — the two are not the same claim.

---

# FILES TOUCHED

| file | change | snapshot |
|---|---|---|
| `claude_advisor.py` | stale-1H marker on the tier line + tally row + NOTE; `_slot_age_minutes` helper; `CATEGORY_TTL_MINUTES` import | `.bak_stale1h_marker_20260805` |
| `config.py` | `NEWS_OBSERVATION_PINNED = True` + the misleading-name record | `.bak_newsgate_pinned_20260805` |
| `market_context.py` | pin honoured before the row count | `.bak_newsgate_pinned_20260805` |
| `silence_digest_sol.py` | **new** standalone daily ledger | n/a (new file) |
| `OPEN-ITEMS-SOL.md` | all three recorded in canon | `.bak_20260805_0035` |
| root crontab | one line added, 08:20 UTC | backed up to scratchpad |

All snapshots taken **before** editing and md5-verified. `py_compile` clean on every edited module.

# WHAT I DID NOT DO

- Did not mark the **15m** tier (outside the decision) — flagged as open, with the one-line change.
- Did not add a 5m marker — it cannot be stale; documented instead of implemented.
- Did not fix the `[:500]` truncation — recorded as a precondition, as instructed.
- Did not change how the tally **counts**.
- Did not touch Titan.
