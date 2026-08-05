# TITAN — MAKE THE WALL VETO DO WHAT IT SAYS: THE RULE WAS UNSATISFIABLE, AND MY OWN 18:35 NUMBER WAS WRONG

**2026-08-05 18:55 UTC · DIFF SHOWN, NOT APPLIED · HEAD `b9081ad`, `git status` clean, 0 open positions**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
`trades.db` read-only throughout. **Mercury-SOL never opened.** Nothing in `titan-bot` was modified:
the patch was built and exercised on **copies** in a scratch directory.

Parent: `2026-08-05-1835-titan-did-the-wall-hold-or-was-it-eaten.md`.

---

## 🔴 CORRECTION TO THE 18:35 REPORT, FIRST, BECAUSE IT CHANGES THE HEADLINE

**18:35 reported: "70.2 % of vetoes fire below the 50th percentile, median 29th, only 6.6 % above the
90th."** That number ranked each **nearest opposing wall** against the **`max_wall_mult_*`** baseline —
the distribution of *the single largest wall in each snapshot*. A typical wall is not a maximum, so
this read every wall as thinner than it is.

| the same 273 refusals, ranked against | below 50th | median | ≥ 90th |
|---|---|---|---|
| **`max_wall_mult_*`** — what 18:35 used | **75.5 %** | **23.2nd** | 4.8 % |
| 🔴 **nearest-wall distribution** — apples-to-apples | **53.8 %** | **48.4th** | **12.1 %** |

*(75.5 % here vs 70.2 % at 18:35: same bias, marginally different cohort — 18:35 ranked 272 rows against
a trailing-7-day window, this ranks 273 against the full baseline. Both are the wrong comparator.)*

**The size of the gap:** a **×5.0** wall sits at the **31st** percentile of bid maxima and the **57th**
of nearest-bid walls — **26 points, straddling the exact 50th-percentile line this rule turns on.**

🔴 **THE FINDING SURVIVES, SMALLER AND MORE PRECISE.** The veto does **not** fire mostly on thin walls.
It fires on the **perfectly ordinary** wall — **median 48th percentile**. That is still a genuine
contradiction with a rule demanding one *"genuinely THICK FOR THIS BOOK"*, and it is still the
documented-mismatch class the brief describes. **But "70.2 % below the median" overstated it and is
withdrawn.** This is the `_exit_pct` provenance lesson recurring on a second quantity — and it was
caught only because building the patch forced me to name the baseline I was ranking against.

---

## §1 — WHY DOES IT FIRE THERE? **BECAUSE THE RULE WAS LITERALLY UNSATISFIABLE.**

### 1a. THE VERBATIM WALL BLOCK — row 21584, 2026-08-05 14:10:12, a SHORT that was refused

```
Order book (pre-trade, 8000 levels):
  Mid: $64,449.95  |  Imbalance ±1%: 0.34 (ask-heavy)  — 0th pct
  Bid walls (>4x avg bucket vol): $64,317.50 (×4.1), $64,292.50 (×4.3), $64,152.50 (×4.0), $64,042.50 (×4.3)  — largest ×4.3 = 16th pct
  Ask walls (>4x avg bucket vol): $64,502.50 (×4.4), $64,677.50 (×9.3)  — largest ×9.3 = 82th pct
  Book depth: 2,909 BTC — 46th pct, sampled 11s ago
Order-book PERCENTILE scale (baseline: 33228 snapshots of this same OKX depth-4000 book)
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile: ~50th percentile is ORDINARY,
  not significant.
```

**Six walls are named. Six multiples are printed. Two percentiles are printed — one per side, for the
largest wall only.** The four bid walls the model might veto on carry **no percentile at all**.

### 1b. IS THE PERCENTILE AS PROMINENT AS THE MULTIPLE? **NO — 6 to 2, AND POSITIONALLY LAST.**

`claude_advisor.py:175-182`: `body` renders `$price (×mult)` for up to five walls per side; `tail`
appends **one** `— largest ×N = Xth pct`. The figure the prompt calls *meaningless* appears on every
wall; the figure it calls *decisive* appears once, at the end of the line, attached to a different
wall. **The brief's phrasing — "a 'x5.1 wall' reads as authoritative in a way '22nd pct' does not" —
understates it: for most walls the percentile is not merely quieter, it is absent.**

### 1c. DOES THE HARD RULE NAME A THRESHOLD? **NO. IT NAMES AN ADJECTIVE.** (`claude_advisor.py:59-65`)

```
"HARD RULE — opposing walls: if a limit wall that is genuinely THICK FOR "
"THIS BOOK sits directly above a LONG entry or directly below a SHORT "
"entry, you MUST reply 'skip'. A thick wall in the opposing direction "
"represents strong resting liquidity that will absorb the move before it "
"can develop. Judge 'thick' by the PERCENTILE printed beside the wall, "
"never by the raw multiplier: every book state contains a wall above 4x, "
"so a large ×-figure on its own says nothing."
```

**"genuinely THICK", "thick", "large" — and no number.** The only number in the prompt is the NOTE's
*"~50th percentile is ORDINARY"*, forty lines away and phrased as an aside rather than as the rule.

### 1d. 🔴 IS THERE A PATH WHERE A WALL IS DESCRIBED WITHOUT ITS PERCENTILE? **YES — TWICE OVER.**

**FIRST: for most of the measured window there was no percentile at all.**

| entry prompts, `ai_skipped`, since 2026-07-13 | 492 |
|---|---|
| containing an `Order book` block | **492** |
| 🔴 containing the PERCENTILE scale | **93** |
| 🔴 **wall described with a multiple and NO percentile** | **399 = 81.1 %** |

The scale first appears on **2026-07-29** — zero of the 399 before it. **So for 81 % of the cohort the
brief's premise is not merely true, it is total: the rule said "judge by the percentile printed beside
the wall" and no percentile was printed anywhere.**

**SECOND — and this survives into the machine running right now: the percentile that IS printed
describes the wrong wall.**

| the vetoed wall (nearest opposing) vs the wall that gets a percentile (largest) | n=277 |
|---|---|
| nearest **is** the largest → a percentile is shown for it | **21 = 7.6 %** |
| 🔴 nearest is **not** the largest → the shown percentile belongs to a DIFFERENT wall | **256 = 92.4 %** |

🔴 **THE RULE IS UNSATISFIABLE AS WRITTEN.** It instructs the model to judge a specific wall by a
percentile that, 92.4 % of the time, is not on the page for that wall.

### AND THE TEST THAT PROVES THE PERCENTILE ALONE IS NOT THE FIX

| era | n | below 50th | median | ≥90th |
|---|---|---|---|---|
| **A** — pre-percentile (07-13…07-28) | 239 | 69.0 % | 31.6th | 7.1 % |
| **B** — percentile RENDERED (07-29+) | 33 | **78.8 %** | 18.4th | 3.0 % |

**perm-p 0.3130 — the behaviour did not improve when the percentile appeared.** *(Both columns use the
biased max-wall baseline, so read them against each other, not absolutely; n=33 is small and the
difference is not significant either way.)* **Rendering the number was not enough — which is exactly
the brief's thesis, and it is why the change below is about emphasis and wording, not about adding a
figure that is already there.**

---

## §2 — THE CHANGE. **DIFF SHOWN, NOT APPLIED.**

Three edits, in one direction: **the figure the prompt calls decisive becomes the prominent one, and
the rule states its own line instead of an adjective.** No mechanical filter, no veto override, no new
gate, no wall hidden, no threshold in code. Scope is the entry advisor prompt and the data that feeds
it — **the EMA envelope gate, the cascade, the FLAT floor, Variant-B, the score bars, the risk gates,
the geometry and the entire exit side are untouched.**

### (a) PERCENTILE PRIMARY, MULTIPLE SECONDARY — AND ONE FOR EVERY WALL

New `main._rank_walls()` ranks each listed wall; `_wall_line` renders `$price — Nth pct (×mult)`.
Rendered on the real block above, with real baselines:

```
BEFORE
  Bid walls (>4x avg bucket vol): $64,317.50 (×4.1), $64,292.50 (×4.3), $64,152.50 (×4.0), $64,042.50 (×4.3)  — largest ×4.3 = 16th pct
  Ask walls (>4x avg bucket vol): $64,502.50 (×4.4), $64,677.50 (×9.3)  — largest ×9.3 = 82th pct

AFTER
  Bid walls (>4x avg bucket vol): $64,317.50 — 9th pct (×4.1), $64,292.50 — 24th pct (×4.3), $64,152.50 — 0th pct (×4.0), $64,042.50 — 24th pct (×4.3)
  Ask walls (>4x avg bucket vol): $64,502.50 — 27th pct (×4.4), $64,677.50 — 91th pct (×9.3)
```

🔴 **Note what the corrected baseline does to the one genuinely thick wall: ×9.3 moves from "82nd" to
"91st" — into the region the rule is actually about.** The change does not uniformly soften walls; it
makes ordinary ones read ordinary and strong ones read strong.

### (b) THE RULE STATES THE LINE INSTEAD OF THE ADJECTIVE

*"…is grounds to reply 'skip' ONLY when it is genuinely unusual for this book. Read that off the
wall's OWN percentile, printed beside it: at or below the ~50th percentile a wall is ORDINARY and is
NOT on its own a reason to skip; the 90th percentile and above is the region the word 'thick' is meant
to describe; between the two, weigh it with everything else rather than treating it as decisive."*

**This is not new policy** — it is the number the prompt's own NOTE has asserted since the scale
shipped, moved from an aside into the rule that uses it.

### (c) THE MEASURED BASE RATE, AS A FACT

*"…price later traded THROUGH the cited wall's own price level in 54 % of cases within 1h, 75 %
within 4h, 88 % within 12h and 95 % within 24h; where it did, it travelled a median 1.23 % beyond the
wall. Those walls stood a median 0.13 % from the entry price… This describes what happened; it does
not tell you what to decide."*

⚠️ **A TENSION I AM NOT GOING TO BURY.** `_entry_book_pct`'s docstring carries a standing line from
`f0a8d30`: *"No win rate, no PnL, no historical performance is attached to any book figure — the model
may learn whether a wall is ordinary or extreme, never what that implies about the outcome."*
**I read this addition as on the right side of that line — it is the fate of the price LEVEL, not the
outcome of any trade, and it attaches no verdict — but it is adjacent to it, and the operator asked
for it explicitly.** If you want (c) dropped and only (a)+(b) applied, that is a one-hunk removal and
the pre-registration below still holds; (a)+(b) are the mechanical fix and (c) is the calibration.

### 🔴 AND THE BASELINE CORRECTION IS PART OF THE DIFF, NOT JUST OF THIS REPORT

`_rank_walls` ranks against the reconstructed **nearest-wall** multiple
(`nearest_wall_{side}_vol_btc / wall_mean_bucket_vol_{side}_btc`), not `max_wall_mult_*`. **Had I
shipped the obvious version, the patch would have achieved part of its intended effect through a
measurement artefact — walls rendered systematically thinner than they are.** That is the failure mode
`_exit_pct` was written to prevent, and it would have been invisible in review.

### DEGRADATION IS ALL-OR-NOTHING, AND VERIFIED BYTE-IDENTICAL

If the ranking is unavailable (baseline < 200 rows, bad side, any exception) the line falls back to
the **exact previous rendering**, confirmed against the unpatched module:

```
ranking unavailable : $64,317.50 (×4.1), $64,292.50 (×4.3), …  — largest ×4.3 = 16th pct
original            : $64,317.50 (×4.1), $64,292.50 (×4.3), …  — largest ×4.3 = 16th pct   ← identical
```

⚠️ Retained wart, deliberately not fixed: the ordinal suffix is always `th` (`91th`, `82th`). It is
pre-existing in `_pct`, cosmetic, and outside this scope.

### THE DIFF — `main.py` +71 / `claude_advisor.py` +96, both `ast.parse` clean

```diff
--- a/main.py
+++ b/main.py
@@ -1,4 +1,4 @@
-import os, ccxt, requests, sqlite3, time, re, json, builtins, subprocess, traceback
+import os, ccxt, requests, sqlite3, time, re, json, builtins, subprocess, traceback, bisect

@@ -2525,6 +2525,70 @@
+def _rank_walls(wlist, side):
+    """Percentile of EVERY listed wall's multiple, not just the largest one.
+
+    🔴 WHY THIS EXISTS (2026-08-05). The HARD RULE tells the model to judge
+    thickness "by the PERCENTILE printed beside the wall". It was not printed
+    beside the wall. `_wall_line` rendered a per-wall multiple for up to five
+    walls and exactly ONE percentile — for the LARGEST of them — as a trailing
+    note. Measured over the 277 de-duplicated wall-citing refusals of
+    2026-07-13..2026-08-05: the wall actually being vetoed on (the NEAREST
+    opposing one, the wall the rule is about) was the largest in only 7.6% of
+    cases. For the other 92.4% the single rendered percentile belonged to a
+    DIFFERENT wall, so the instruction was unsatisfiable as written — the model
+    was told to read a number that was not on the page for the wall in question.
+
+    🔴 AND THE BASELINE IS THE *NEAREST*-WALL DISTRIBUTION, NOT `max_wall_mult_*`.
+    This is the `_exit_pct` provenance lesson applying to a second quantity, and
+    it was caught by measurement rather than by reading. `max_wall_mult_bid/ask`
+    is the distribution of "the single biggest wall in the book" — a different
+    object from "a wall you actually encounter in the path". Ranking an ordinary
+    listed wall against the maxima makes it look systematically thinner than it
+    is: a x5.0 wall sits at the 31st percentile of bid MAXIMA and the 57th of
+    nearest-bid walls, a 26-point gap straddling the exact 50th-percentile line
+    this rule turns on. Measured on the 273 rankable wall-citing refusals, the
+    wrong baseline reports "75.5% below the 50th, median 23rd" where the right
+    one reports "53.8% below, median 48th" — the difference between a veto that
+    fires on thin walls and one that fires on ordinary ones.
+
+    The nearest-wall multiple is not stored as a column; it is reconstructed the
+    way the collector defines every multiple — bucket volume over mean bucket
+    volume — from `nearest_wall_{side}_vol_btc / wall_mean_bucket_vol_{side}_btc`.
+
+    ONE QUERY PER SIDE, ranked in memory. `_exit_pct()` is a full scan of
+    `orderbook_density`; calling it five more times per side would be ten more
+    scans per prompt for a block that is rendered on every entry decision.
+
+    Same provenance guard as `_exit_pct`: the source is ANDed into the WHERE
+    clause, so a multiple is only ever ranked against rows from the SAME
+    instrument. A baseline with too few rows returns all-None, and the renderer
+    then falls back to the PREVIOUS rendering in full — the same all-or-nothing
+    trade `_entry_book_pct` already makes, because a missing percentile costs
+    nothing and a mis-scaled one changed a live decision once already.
+
+    Returns a list aligned with the first five walls; read-only; never raises.
+    """
+    ws = (wlist or [])[:5]
+    if not ws:
+        return []
+    try:
+        with sqlite3.connect(DB_PATH) as conn:
+            vals = [r[0] for r in conn.execute(
+                f"SELECT nearest_wall_{side}_vol_btc / wall_mean_bucket_vol_{side}_btc "
+                f"FROM orderbook_density "
+                f"WHERE nearest_wall_{side}_vol_btc IS NOT NULL "
+                f"  AND wall_mean_bucket_vol_{side}_btc > 0 "
+                f"  AND source = ?", (BOOK_SRC_OKX_4000,))]
+        if len(vals) < 200:
+            return [None] * len(ws)
+        vals.sort()
+        return [100.0 * bisect.bisect_left(vals, w.get('mult') or 0.0) / len(vals)
+                for w in ws]
+    except Exception:
+        return [None] * len(ws)

@@ -2577,6 +2641,11 @@  (in _entry_book_pct)
         out['ask_pct'], _ = _exit_pct('max_wall_mult_ask', _ask, BOOK_SRC_OKX_4000)
+        # 🔴 2026-08-05 — a percentile for EVERY wall, so the HARD RULE's
+        # "printed beside the wall" is true of the wall being judged and not
+        # only of the biggest one on the line. See `_rank_walls`.
+        out['bid_wall_pcts'] = _rank_walls(walls.get('walls_bid'), 'bid')
+        out['ask_wall_pcts'] = _rank_walls(walls.get('walls_ask'), 'ask')
```

```diff
--- a/claude_advisor.py
+++ b/claude_advisor.py
@@ -56,13 +56,44 @@
-    "HARD RULE — opposing walls: if a limit wall that is genuinely THICK FOR "
-    "THIS BOOK sits directly above a LONG entry or directly below a SHORT "
-    "entry, you MUST reply 'skip'. A thick wall in the opposing direction "
-    "represents strong resting liquidity that will absorb the move before it "
-    "can develop. Judge 'thick' by the PERCENTILE printed beside the wall, "
-    "never by the raw multiplier: every book state contains a wall above 4x, "
-    "so a large ×-figure on its own says nothing.\n\n"
+    # 🔴 2026-08-05 — THE RULE NOW STATES THE LINE IT ALREADY IMPLIED.
+    # The old text asked for a wall "genuinely THICK FOR THIS BOOK" and told the
+    # model to judge that by the percentile — but named no percentile, so the
+    # operative word was an adjective. Measured over 273 rankable de-duplicated
+    # wall-citing refusals (2026-07-13..08-05), against the NEAREST-wall
+    # baseline: 53.8% fired on a wall below the 50th percentile, MEDIAN 48th,
+    # only 12.1% above the 90th. The veto fires on the perfectly ordinary wall —
+    # which is the one this same prompt calls "ORDINARY, not significant" three
+    # lines later. The threshold below is not new policy: it is the number the
+    # prompt's own NOTE has asserted since the percentile scale shipped.
+    # ⚠️ Those shares supersede the "70.2% / median 29th" published at 18:35,
+    # which ranked nearest walls against the MAX-wall baseline and so read them
+    # as thinner than they are. See `main._rank_walls`.
+    "HARD RULE — opposing walls: a limit wall sitting directly above a LONG "
+    "entry or directly below a SHORT entry is grounds to reply 'skip' ONLY "
+    "when it is genuinely unusual for this book. Read that off the wall's OWN "
+    "percentile, printed beside it: at or below the ~50th percentile a wall is "
+    "ORDINARY and is NOT on its own a reason to skip; the 90th percentile and "
+    "above is the region the word 'thick' is meant to describe; between the "
+    "two, weigh it with everything else rather than treating it as decisive. "
+    "Never judge by the raw multiplier: every book state contains a wall above "
+    "4x, so a large ×-figure on its own says nothing.\n\n"
+    # 🔴 CALIBRATION, NOT INSTRUCTION — and deliberately about the WALL, not
+    # about any trade outcome. The standing line (f0a8d30, and `_entry_book_pct`)
+    # is that no win rate, PnL or historical performance is attached to a book
+    # figure: the model may learn whether a wall is ordinary or extreme, never
+    # what that implies about the result. What follows is the fate of the LEVEL
+    # itself — measured, and carrying no verdict.
+    "MEASURED BASE RATE — what happens to walls like these (calibration only, "
+    "no action attached): across 277 refusals that cited an opposing wall "
+    "between 2026-07-13 and 2026-08-05, price later traded THROUGH the cited "
+    "wall's own price level in 54% of cases within 1h, 75% within 4h, 88% "
+    "within 12h and 95% within 24h; where it did, it travelled a median 1.23% "
+    "beyond the wall. Those walls stood a median 0.13% from the entry price. "
+    "The stated premise that resting liquidity 'absorbs the move before it can "
+    "develop' is therefore not what the record shows for walls at these "
+    "distances. This describes what happened; it does not tell you what to "
+    "decide.\n\n"

@@ -172,21 +203,63 @@
-    def _wall_line(label, wlist, max_key, pct_key):
-        body = ', '.join(f"${w['price']:,.2f} (×{w['mult']})"
-                         for w in (wlist or [])[:5]) or 'none'
-        tail = ''
-        if isinstance(bp.get(pct_key), (int, float)):
-            tail = (f"  — largest ×{bp.get(max_key, 0.0):.1f} = "
-                    f"{bp[pct_key]:.0f}th pct")
-        return f"  {label} walls (>{thresh:.0f}x avg bucket vol): {body}{tail}\n"
+    def _wall_line(label, wlist, max_key, pct_key, pcts_key):
+        """🔴 2026-08-05 — PERCENTILE FIRST, MULTIPLE SECOND, PER WALL.
+
+        This used to render `$price (×mult)` for up to five walls and then ONE
+        trailing percentile for the largest of them. Two things were wrong with
+        that and both are behavioural, not cosmetic:
+
+          1. The multiple appeared five times and the percentile once, so the
+             figure the prompt calls meaningless was the prominent one and the
+             figure it calls decisive was a footnote.
+          2. The one percentile described the LARGEST wall. The wall actually
+             vetoed on was the largest in only 7.6% of 277 measured refusals —
+             so 92.4% of the time the rule's "percentile printed beside the
+             wall" simply did not exist for the wall in question.
+
+        Now every wall carries its own percentile, written before its multiple.
+        No wall is hidden, no threshold is applied here, and nothing is dropped:
+        this is the same set of walls with the emphasis put on the figure the
+        rule actually asks the model to use.
+
+        ALL-OR-NOTHING DEGRADATION, the same trade `_entry_book_pct` already
+        makes ("any failure returns {} and the block renders exactly as it did
+        before this function existed"). If the per-wall ranking is unavailable
+        we fall back to the PREVIOUS rendering — bare multiples plus the
+        largest-wall summary — and not to five repetitions of "pct n/a", which
+        would be louder than what it replaced while carrying less.
+        """
+        ws = (wlist or [])[:5]
+        if not ws:
+            return f"  {label} walls (>{thresh:.0f}x avg bucket vol): none\n"
+        pcts = bp.get(pcts_key) or []
+        have = [i for i, _ in enumerate(ws)
+                if i < len(pcts) and isinstance(pcts[i], (int, float))]
+        if not have:
+            # unchanged pre-2026-08-05 behaviour
+            body = ', '.join(f"${w['price']:,.2f} (×{w['mult']})" for w in ws)
+            tail = ''
+            if isinstance(bp.get(pct_key), (int, float)):
+                tail = (f"  — largest ×{bp.get(max_key, 0.0):.1f} = "
+                        f"{bp[pct_key]:.0f}th pct")
+            return f"  {label} walls (>{thresh:.0f}x avg bucket vol): {body}{tail}\n"
+        parts = []
+        for i, w in enumerate(ws):
+            p = pcts[i] if i < len(pcts) else None
+            head = (f"{p:.0f}th pct" if isinstance(p, (int, float)) else "pct n/a")
+            parts.append(f"${w['price']:,.2f} — {head} (×{w['mult']})")
+        return (f"  {label} walls (>{thresh:.0f}x avg bucket vol): "
+                f"{', '.join(parts)}\n")

@@ -197,9 +270,11 @@
-        + _wall_line('Bid', walls.get('walls_bid'), 'bid_max', 'bid_pct')
-        + _wall_line('Ask', walls.get('walls_ask'), 'ask_max', 'ask_pct')
+        + _wall_line('Bid', walls.get('walls_bid'), 'bid_max', 'bid_pct',
+                     'bid_wall_pcts')
+        + _wall_line('Ask', walls.get('walls_ask'), 'ask_max', 'ask_pct',
+                     'ask_wall_pcts')

             f"Order-book PERCENTILE scale (baseline: {bp['baseline_n']} snapshots "
             f"of this same OKX depth-4000 book)\n"
+            "  Each wall's percentile ranks its multiple against the history of walls\n"
+            "  standing in the path on that side of this same book — so the walls on a\n"
+            "  line are on one scale, and the nearest wall is the most exactly ranked.\n"
             "  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means\n"
-            "  nothing on its own. Judge by the percentile: ~50th percentile is ORDINARY,\n"
-            "  not significant.\n"
+            "  nothing on its own. Judge by the percentile printed with each wall:\n"
+            "  ~50th percentile is ORDINARY and not significant; 90th+ is genuinely thick.\n"
```

### WHAT WAS VERIFIED ON THE PATCHED COPIES

| check | result |
|---|---|
| `ast.parse` both files | ✅ |
| `_rank_walls` against the live baseline | bid `[8.9, 23.7, 0.0, 23.7]`, ask `[27.1, 90.9]` — sane and monotone in the multiple |
| empty wall list | `[]` |
| bad side / unrankable | `[None…]` → renderer falls back |
| fallback rendering vs unpatched module | **byte-identical** |
| `titan-bot` working tree | **clean, `b9081ad`, 0 files changed** |

---

## §3 — PRE-REGISTRATION, BEFORE ANY OF THIS IS APPLIED

### BASELINE, AS OF NOW

| quantity | value |
|---|---|
| wall-citing refusals (deduped) | **277** over **22 days** = **12.6/day** |
| 🔴 below 50th pct (**corrected**, nearest-wall baseline) | **53.8 %** · median **48.4th** · ≥90th **12.1 %** |
| *(superseded 18:35 figure, max-wall baseline)* | *70.2 % · median 29th · 6.6 %* |
| advisor verdicts since 07-13 | skip **492** / execute **19** → refusal **96.3 %** |
| entries | **0.79/day** |

### THE FALSIFIABLE PREDICTION

🔴 **PRIMARY: the sub-50th share FALLS.** Measured on the corrected baseline, over the next **~100
consultations**. **If it has not moved, the emphasis was not the cause — and that is a NULL to be
recorded as such, not explained away.** I am naming the number now: I expect **53.8 % → below 40 %**.
If it lands between 40 % and 50 % I will call that ambiguous, not a win.

**SECONDARY: the refusal rate falls only modestly, and here is why I expect that** — the wall is
almost never the sole stated reason:

| of 328 wall-citing reasons, what else is cited | share |
|---|---|
| regime / trend / ADX | **91.2 %** |
| flat / chop | 34.1 % |
| volume / ATR | 15.5 % |
| score / confluence | 9.8 % |
| 🔴 **the wall AND NOTHING ELSE** | 🔴 **6.4 %** |

**Only 6.4 % of these refusals rest on the wall alone.** So even a fully effective change flips a
small subset: **refusal 96.3 % → 92–95 %**, entries **0.79/day → 0.9–1.2/day**. **A jump beyond
~1.5/day would mean the change did more than re-weight one figure, and is itself a reason to revert
and look.**

### THE DRIFT CHECK THAT GOVERNS

Newly-admitted signals are tracked by `skip_attribution` as usual and become closed trades. **If the
newly-admitted cohort drifts favourably, the change was right; if adversely, it was wrong and reverts.**

⚠️ **And the honest caveat on that check, from the 18:35 pass: with ~12.6 wall-refusals/day on ~1
day of independent information each, a drift verdict needs weeks, not days.** The unit of
independence is the DAY. **Do not read the first week as evidence in either direction** — the
sub-50th share (primary) will be readable long before the drift is.

---

## WHAT WAS NOT TOUCHED

EMA envelope gate · HTF cascade · FLAT floor · Variant-B · score bars · risk gates · geometry
(SL 2.25 / trail 0.75R) · the entire exit side · `config.py` · any schema. **And nothing at all in
`/root/titan-bot` — the diff is shown, not applied.** Mercury-SOL never opened.

| | |
|---|---|
| open positions | **0** |
| `titan-bot` HEAD / `git status` | **`b9081ad`** / **clean** |
| patch location (not applied) | scratchpad copies + `wall.diff` |
