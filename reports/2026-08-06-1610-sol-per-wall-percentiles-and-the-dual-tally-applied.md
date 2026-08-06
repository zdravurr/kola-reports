# SOL — PER-WALL PERCENTILES AND THE DUAL TALLY. THE LAST WORK ITEM BEFORE THE FLIP.

**2026-08-06 16:10 UTC · Mercury-SOL (PAPER) · APPLIED AND PROVEN BY EXECUTION.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`. **One file changed: `claude_advisor.py`.**
Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched.**

Both items were reported at 12:15 §3a/§3b and deliberately not fixed then. They are fixed now.

---

# 1. PER-WALL PERCENTILES — the `1ec2477` port

## What the prompt said before, and what it says now

```
BEFORE  Massive bid walls (>4x avg vol): $73.25 (×20.9), $72.75 (×8.3), $72.25 (×5.3), $71.25 (×4.8)
        Massive ask walls (>4x avg vol): $73.75 (×17.2), $74.25 (×4.8), $74.75 (×8.7), $100.25 (×4.2)

AFTER   Bid walls (>4x avg vol): $73.25 (p90, x17.7), $72.75 (p67, x11.2), $72.25 (p31, x5.7), $71.25 (p15, x4.6)
        Ask walls (>4x avg vol): $73.25 (p53, x8.4),  $73.75 (p56, x9.0),  $74.25 (p5, x4.0),  $74.75 (p58, x9.3)
        Wall figures: pN = this wall's PERCENTILE among all walls this prompt has rendered
        (n=23,080; the primary figure), xN = the raw volume multiple (secondary). Every wall
        listed already passed the >4x filter, so the multiple alone does not distinguish an
        ordinary wall from a thick one — the percentile does. CALIBRATION: ~p50 is an ORDINARY
        wall, p90+ is genuinely thick. Judge thickness by the percentile, not by the word
        "massive" or by the multiple.
```

**The word "Massive" is gone from the line.** It was the adjective doing the work the number should
do, and it was applied to 100% of walls rendered.

## a) 🔴 The baseline — like-for-like, which is the whole lesson of Titan's withdrawn attempt

Titan's first attempt ranked the **NEAREST** wall against a distribution of **MAX** walls — two
different populations — and had to be pulled. Here **every wall is ranked against the population it is
drawn from**: every wall this prompt has ever *rendered* (top-5 per side, both sides, ≥×4). A rendered
wall is compared only with other rendered walls.

| | |
|---|---|
| source | `trades.ai_user_prompt` — the ×N figures of the rendered wall lines |
| **coverage** | **3,350 renders · 23,080 wall multiples · 2026-06-08 → 2026-08-06** |
| shape | min 4.00 · p25 5.20 · **median 7.90** · p75 13.10 · p90 17.70 · p95 20.10 · max 33.80 |

**I did not use `skip_attribution`.** It stores the wall *shape* fields you named
(`opp_wall_next_mult`, `opp_wall_dominance`, `n_walls_opposing`, `n_walls_supporting`) — but
`opp_wall_next_mult` is populated on only **322 of 9,706 rows** and covers just 2026-08-02 onward, and
it is a **nearest-opposing-wall** population. Ranking a rendered wall against it would repeat Titan's
exact mistake in a new costume. `wall_strength` reaches further (3,280 rows, 06-07 → 08-06) but is
also a nearest-wall field. **The rendered-wall population is the only like-for-like one, and it is
also the largest.**

**The baseline is STATIC by design.** One that moved with every new render would make the same wall
rank differently on two consecutive prompts and would silently re-scale the calibration line. Re-cut
it deliberately and dated, or not at all.

**Validated against the population it was cut from** — interpolated between 5-point breakpoints:

| multiple | rendered | measured | err |
|---|---|---|---|
| ×8.0 | p51 | 50.7% | +0.3 |
| **×11.7** | **p70** | **69.8%** | **+0.2** |
| ×15.0 | p82 | 82.0% | 0.0 |
| ×20.0 | p95 | 94.9% | +0.1 |

> **A first cut of this used a bare step lookup and rendered ×11.7 as p65** — flooring to the bucket
> below, disagreeing by 5 points with the 12:15 report that motivated the change. Interpolation was
> added and it now reads **p70**. Caught before shipping; recorded because a number that quietly
> disagrees with its own source report is the defect this whole change is about.

**And the headline stands in the prompt itself: the ×11.7 wall that carried all three of the 11:25
skips renders as `p70` — an ordinary-to-firm wall, not an exceptional one.**

## b) 🔴 The degraded path

Titan found the rule became **unsatisfiable** when no percentile existed. The answer is neither to
guess a rank nor to fall silent:

```
  Bid walls (>4x avg vol): $72.50 (pctl N/A, xNone)
  🔴 NOT RANKABLE: 1 wall(s) above could not be assigned a percentile; their xN multiples are raw
  and UNRANKED. Do NOT infer that such a wall is extreme, and do NOT infer that it is ordinary —
  the rank is simply unknown. For those walls the thickness test below cannot be applied: judge
  them on DIRECTION and REGIME alone, exactly as before percentiles existed, and never treat an
  unranked wall as a thickness argument in either direction.
```

**What the rule should do in that state, stated in the prompt:** fall back to direction and regime —
the parts of the V2 wall rule that never needed a rank — and treat the wall as a thickness argument in
**neither** direction. An unrankable wall is the *absence* of rank evidence, not evidence of either
extreme. `_wall_pctl` returns `None` rather than a number it cannot justify, and `None` is never
rendered as "ordinary".

*(Pre-fix, the same input rendered `$72.50 (×None)` with no warning at all — visible in the proof.)*

## c) No statistic, no base rate, no win rate

Nothing about what walls *do* is attached to any wall. The only added claims are the **rank** of this
wall and the **calibration** of that rank. The sentence "every wall listed already passed the >4x
filter" is arithmetic about the filter, not a measured base rate about outcomes. Titan's (c) hunk was
dropped for crossing that line and it is not crossed here — telling the model how often walls get
traded through would be outcome information wearing a level's clothes.

---

# 2. THE STALE 1H'S FULL VOTE — BOTH TALLIES, AS FACTS

```
  1H: LuxAlgo Bear -> SHORT = OPPOSES  [STALE: set 13.4h ago, past the 6h window]
  15m: LuxAlgo Bull -> LONG = AGREES
  5m trigger: Trigger Bull -> LONG = AGREES
  NOTE: 1 of the tiers above is/are STALE (1H) — older than the window the gate uses for that
  tier. BOTH readings are given below: the tally AS COUNTED (stale tiers cast a full vote) and
  the tally EXCLUDING stale tiers. Neither is privileged; weigh them yourself.
  Of the 3 tier(s) shown — AS COUNTED (stale tiers vote in full): 2 agree, 1 oppose, 0 neutral, 0 absent.
  Of the 2 tier(s) still INSIDE the gate's own freshness window — EXCLUDING STALE: 2 agree, 0 oppose, 0 neutral, 0 absent.
  Both readings are FACTS about this consultation. The first counts a tier the gate's own TTL
  would have discarded; the second drops it. Decide for yourself how much weight a tier that old
  deserves.
```

**That is the 44.3% shape rendered in both readings: "2 agree, 1 oppose" and "2 agree, 0 oppose".**
The model weighs it; we do not decide for it.

The tier is **not dropped** — dropping strips the arbiter from 56.6% of prompts and the
200-consultation window measured that *adding* the 1H helped. It is **not silently counted** either —
a tally that counts a vote the gate's own TTL would have discarded is two mechanisms disagreeing about
one fact, the defect class corrected in Titan's cascade.

## a) The TTL is the GATE's own, not a new number

`_TIER_STALE_TTL_MIN['1H'] = CATEGORY_TTL_MINUTES['TREND'] = **360 min (6 h)**` — config.py:320.
**The same constant `signal_matrix.py:235` uses to DROP the tier**, and that `state_machine.py:571`
reads. A tier counts as stale here **exactly when the gate would already have discarded it**. No new
threshold was invented, and the boundary cannot drift away from the gate's, because it *is* the gate's.

## b) The tier line itself is unchanged

Confirmed by the code-only diff: `_agree_lines` construction does not appear in it. The 1H still
renders its `AGREES`/`OPPOSES` verdict and its `[STALE: …]` marker exactly as before. **Only the tally
gained a second reading**, and the pre-existing `_tally` is incremented identically — the new
`_tally_live` is a parallel counter, not a replacement.

## c) No outcome statistic attached

No win rate, no base rate, nothing about what followed past agreements. Same line as §1c.

---

# 3. PRE-REGISTERED

## 🔴 The honest limit, first

> **The current window is 131 prompts and 0 executes. With zero executes, the advisor's decision rate
> cannot be evaluated from this window at all.** Any change in skip/execute ratio measured against a
> denominator of zero executes is not a measurement, it is a ratio with an empty numerator.
> **What follows is therefore pre-registered as a measurement of what the model SEES, and of what it
> CITES — not yet of what it DOES.** The decision-rate question reopens only once executes exist.

## Expected direction, per change

| | expected direction | how measured |
|---|---|---|
| **§1 walls** | prompts containing a percentile go **0 of 131 → 100%** | grep `pctl`/`percentile` in `trades.ai_user_prompt` |
| | verdict reasons that cite a wall as decisive should **shift toward higher-percentile walls**; a sub-p50 wall should stop being cited as "massive" | percentile of the wall named in `ai_reason`, distribution before vs after |
| | 🔶 **direction not predicted for the skip rate itself** — a percentile can make a wall look weaker *or* stronger, and the change is calibration, not a thumb on the scale | — |
| **§2 tally** | prompts rendering **both** readings ≈ the stale rate, **~66.4%** | count of prompts containing "EXCLUDING STALE" |
| | in the **44.3%** population where the lone opposer is the stale 1H, the second reading is **unanimous** by construction | recount that population post-change |
| | verdict reasons citing staleness (**58 = 44.3%** before) should **not fall** — the marker already worked; the tally now agrees with it | grep `ai_reason` |

**Falsification:** if after ~130 new current-form prompts the percentile is present but the walls
cited as decisive still sit at the same percentiles as before, §1 changed the text and not the
reading, and should be reported as a null. Same for §2 if the dual tally never changes which reading
the reasons cite.

**Neither change touches a gate, a score, a threshold or a snapshot.** Both are prompt text. The n=8
trail re-measurement is unaffected.

---

# 4. PROVEN BY EXECUTION — BOTH DIRECTIONS

Isolated tree, **13-file DB_PATH rewrite**, residual grep 0, sqlite leak assert
(**`production-book opens: 0`**), **isolated `.env`** loaded before `import config`. Prompts captured
by intercepting `_call` — no network, the prompt read verbatim as the model would receive it, from a
**real stored book** (`trades.advisor_book_json`) and from tier slots reproducing the 44.3% shape.

| | PRE-FIX | POST-FIX |
|---|---|---|
| prompt contains a percentile | **False** | **True** |
| ×11.7 wall of the 11:25 skips | `×11.7`, unranked | **`p70`** |
| unrankable wall | `$72.50 (×None)`, **no warning** | `pctl N/A` + the 🔴 NOT RANKABLE block |
| tally when the 1H is stale | one reading: *2 agree, 1 oppose* | **both**: *2 agree, 1 oppose* **and** *2 agree, 0 oppose* |

---

# 5. WHAT WAS NOT TOUCHED

**`claude_advisor.py` is the only file changed in this pass.** Everything else carries its mtime from
an earlier pass today:

```
main.py         15:46:27   (M5)          virtual_trader.py  15:18:01   (F1, P1, G2c)
tor_retry.py    15:45:18   (M5)          optimizer.py       15:18:55   (F1, G2c)
config.py       15:19:24   (P2 trail, boot line)
```

**M1–M7, P1, P2, F1, G2c are all in those files and none was reopened.** The **dedup** lives in
`claude_advisor.py` but is untouched: `_state_verdict_cache`, `_slot_identity` and `_near_opposing` do
not appear in the diff, and the key is built from tier **timestamps** and wall **prices** — never from
prompt text — so a text change cannot alter dedup behaviour.

Restarted from flat; the boot line does the confirming:

```
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h
                    OBSERVATION_MODE=True [pid 2742565]

master 2742517 · worker 2742565 (16:05:58) · tracebacks 0 · open/active/exit_pending 0/0/0
TITAN: HEAD 897850b · NOT TOUCHED
```

**Backup:** `claude_advisor.py.bak_wallpctl_dualtally_20260806`.

---

*Generated 2026-08-06 16:10 UTC.*
