# THE CARD FIX — DIFF, APPLIED STATE RE-VERIFIED, AND THE RECORD CORRECTED

**2026-08-04 14:00 UTC · Titan HEAD `44731be` (LIVE, real money) · Mercury-SOL (paper, no VCS)**

Companion to the 12:54 forensics pass §1d and §6b:
`reports/2026-08-04-1300-titan-forensics-what-used-to-gate.md`
Canonical `reports/OPEN-ITEMS.md` updated in the same commit; dated snapshot generated from it:
`reports/2026-08-04-1400-open-items.md`

> **STATUS NOTE, STATED UP FRONT.** The code change was authored and committed earlier today
> (`44731be`, 13:28:57 UTC) and both services were restarted at 13:29. **It was never published** —
> the report and the OPEN-ITEMS edit sat uncommitted in the working tree, so **no link ever reached
> you**. This session **re-verified every claim independently against the running processes and
> `trades.db`** before publishing, rather than trusting the earlier write-up. Where my measurement
> differs from the earlier one, **my number is in this document and the difference is stated.**

---

## 0. ONE CORRECTION TO THE BRIEF, BEFORE THE FIX

The brief said: *"when the signal is then refused seconds later … **NO SECOND CARD IS SENT**."*

**A second card IS sent.** The score gate's `🚫 Below threshold` (Titan `main.py:3812`) and the
advisor's `🤖 AI SKIP` both fire, on all three gate paths. The defect is real but its shape is
different, and the difference decides which of the two offered fixes is correct:

> **The refusal card never references the cascade.** The feed showed a green `🟢 PASS — HTF cascade`
> standing alone, and a separate `🚫 Below threshold` with no visible link back to it. Nothing in
> either message said the PASS was not an admission.

Because a refusal card already exists, **"send the refusal card for the tolerate case too" is already
the status quo and would fix nothing.** So the chosen fix is the other one you offered: **stop the
card from claiming a pass.**

### Why "suppress until the signal survives the score gate" was rejected — say which and why

1. **It leaves the freeze.** `_htf_cascade_gate` returns `None` on the tolerate path; deferring the
   card means carrying state out of the gate function into three separate caller paths. That is
   control flow, not rendering — exactly what point 3 of your brief forbids.
2. **It deletes information.** Suppression would remove the operator's only visibility into *which*
   signals the cascade tolerates — the very population this forensics pass needed to count.
3. The defect is a **false claim**, not an untimely one. **Kept the card, removed the claim, and
   named the bar that actually decides.**

**Magnitude of the defect, measured over the 41 h journal window (2026-08-02 19:55 → 08-04 12:45):**

| | count |
|---|---|
| `HTF_WOULD_PASS` (cascade found no opposing tier) | **215** |
| of those, stopped by the Variant-B 15m sub-gate — sends the **BLOCKED** card, not this one | **109** |
| **`🟢 PASS` cards actually sent** | **106** |
| entries in the same window | **at most 2** |
| **PASS cards that announced an admission which never happened** | **≥98 %** |

---

## 1. TITAN — the tolerate-NEUTRAL card (§1d). DIFF, AS APPLIED

`titan-bot/main.py`, `_htf_cascade_gate`:

```diff
@@ -1794,13 +1794,38 @@ def _htf_cascade_gate(parsed, symbol, side, intent, direction, matrix_result,
                      _neutral_15m_block = True
              if not _neutral_15m_block:
-                send_tg(f"🟢 <b>PASS — HTF cascade (tolerate-NEUTRAL)</b>\n"
+                # 🔴 2026-08-04 — THIS CARD USED TO OPEN WITH "🟢 PASS". IT IS NOT A
+                # PASS. This gate is not the binding one: the score gate (FLAT floor
+                # 5.0 / TREND bar 3.0) runs immediately after and refuses most of
+                # what the cascade tolerates. Measured over the 41 h journal window
+                # 2026-08-02 19:55 → 08-04 12:45: 215 HTF_WOULD_PASS, 109 stopped by
+                # the Variant-B 15m sub-gate (which sends the BLOCKED card, not this
+                # one), leaving 106 of these cards against at most 2 entries — ≥98%
+                # announced an admission that never happened. A refusal card IS sent
+                # afterwards on the below_threshold / ai_skipped paths, but it never
+                # references the cascade, so the green PASS stood alone in the feed
+                # and read as "a range entry was admitted". That misreading cost a
+                # full day of forensics chasing gates that were already working.
+                # FIX IS DISPLAY-ONLY: the title no longer claims an admission, and
+                # the bar that WILL decide is named. `_next_bar` and `_raw_now` are
+                # pure reads of `matrix_result`, already computed by the caller —
+                # no gate branch, no DB write, no advisor prompt is touched, and the
+                # `return None` below is byte-identical in effect.
+                _next_bar = (CONFLUENCE_FLAT_THRESHOLD
+                             if matrix_result.get('market_regime') == 'FLAT'
+                             else CONFLUENCE_SCORE_THRESHOLD)
+                _raw_now = signal_matrix.score_for_direction(matrix_result, direction)
+                send_tg(f"⚪ <b>HTF cascade TOLERATED — NOT an entry</b>\n"
                          f"{dxy_tag()}\n"
                          f"🎯 Trigger: {direction}\n"
                          f"📐 Tiers: 1H {_glyph(_tier_dirs[0])}{_tier_dirs[0]} · "
                          f"15m {_glyph(_tier_dirs[1])}{_tier_dirs[1]} · "
                          f"5m {_glyph(_tier_dirs[2])}{_tier_dirs[2]}\n"
-                        f"🔒 Gate: no tier OPPOSES → tolerated (NEUTRAL/expired allowed)\n"
+                        f"🔒 Cascade: no tier OPPOSES → tolerated "
+                        f"(NEUTRAL/expired allowed)\n"
+                        f"⏭ <b>BINDING GATE IS NEXT</b>: score {_raw_now:.2f} vs bar "
+                        f"{_next_bar:.1f} ({matrix_result.get('market_regime') or 'regime n/a'})"
+                        f" — macro adj applied there; refusal is the usual outcome\n"
                          f"<i>was: {alignment['reason']}</i>")
                  return None
```

**Rendered, from a real FLAT / 1H-NEUTRAL case (raw 3.75, FLAT regime):**

```
BEFORE                                            AFTER
🟢 PASS — HTF cascade (tolerate-NEUTRAL)          ⚪ HTF cascade TOLERATED — NOT an entry
🎯 Trigger: SHORT                                 🎯 Trigger: SHORT
📐 Tiers: 1H ⚪NEUTRAL · 15m ✅SHORT · 5m ✅SHORT    📐 Tiers: 1H ⚪NEUTRAL · 15m ✅SHORT · 5m ✅SHORT
🔒 Gate: no tier OPPOSES → tolerated              🔒 Cascade: no tier OPPOSES → tolerated
was: 1H NEUTRAL (no active TREND signal)          ⏭ BINDING GATE IS NEXT: score 3.75 vs bar 5.0
                                                     (FLAT) — macro adj applied there; refusal
                                                     is the usual outcome
                                                  was: 1H NEUTRAL (no active TREND signal)
```

The operator now reads, **on the card itself**, that this signal is 3.75 against a 5.0 bar — i.e.
about to be refused. That is the single sentence whose absence cost a day.

---

## 2. BOTH BOTS — the dead display threshold (§6b). DIFFS, AS APPLIED

`matrix_result['threshold']` carries `LIQUIDITY_HEATMAP_TREND_THRESHOLD` / `_FLAT_THRESHOLD`
(**4.0 / 6.5**). Confirmed by importing `config` on both bots at 13:56 UTC:

| | real gate (verified by import) | dead display value (verified by import) |
|---|---|---|
| **Titan** | `CONFLUENCE_SCORE_THRESHOLD` **3.0** / `CONFLUENCE_FLAT_THRESHOLD` **5.0** | `LIQUIDITY_HEATMAP_*` **4.0 / 6.5** — card only |
| **SOL** | `CONFLUENCE_SCORE_THRESHOLD` **2.0**, one bar, **no FLAT branch at all** | same **4.0 / 6.5** — card only |

### 2a. Titan `signal_matrix.py` — the dead number appended by `format_for_telegram`

```diff
@@ -577,9 +577,17 @@ def format_for_telegram(res):
      regime = res.get('market_regime', '?')
+    # 🔴 2026-08-04 — `res['threshold']` REMOVED FROM THIS CARD. It carries
+    # LIQUIDITY_HEATMAP_TREND_THRESHOLD / _FLAT_THRESHOLD (4.0 / 6.5), which gate
+    # NOTHING: the entry gate compares CONFLUENCE_SCORE_THRESHOLD (3.0) /
+    # CONFLUENCE_FLAT_THRESHOLD (5.0) in main.py. Because this block is appended
+    # to the below-threshold card, one message printed BOTH "→ 3.75<5.0" (real)
+    # and "(thr=6.5 · FLAT)" (dead) — two thresholds, one card, one of them
+    # connected to nothing. The field is still returned by compute_score() and
+    # still stored in trade_signal_matrix; only the RENDERING drops it.
      parts = [
-        f"📊 score={res['score']:.2f}/10  →  <b>{res['direction']}</b>"
-        f"  (thr={res['threshold']:.1f} · {regime})",
+        f"📊 matrix net={res['score']:.2f}/10  →  <b>{res['direction']}</b>"
+        f"  ({regime} regime)",
      ]
```

```
BEFORE   📊 score=3.75/10  →  SHORT  (thr=6.5 · FLAT)      ← next to the real "→ 3.75<5.0" line
AFTER    📊 matrix net=3.75/10  →  SHORT  (FLAT regime)
```

Titan's own refusal header was already correct and is **unchanged**:
`Below threshold (4.25 | macro −0.5 → 3.75<5.00 for SHORT)` — deciding quantity, the step that
produced it, and the bar that decided, on one line. **The dead number that followed it is gone.**

### 2b. 🔴 A THIRD INSTANCE — the dead number was not printed, it was DECIDING A SENTENCE

Titan `main.py:1846`, the BLOCKED-cascade card. This is **not** in your brief; it was found while
fixing the other two and it is the worse of the three:

```diff
@@ -1843,9 +1868,16 @@
      _mn_score = matrix_result.get('score', 0.0)
-    _mn_thr = matrix_result.get('threshold', 0.0)
-    _mn_note = ("passes score, but cascade is stricter"
-                if _mn_score >= _mn_thr else f"below {_mn_thr:.1f} anyway")
+    # 🔴 2026-08-04 — this note used to be decided by `matrix_result['threshold']`
+    # (LIQUIDITY_HEATMAP_TREND/FLAT = 4.0/6.5), which GATES NOTHING on this bot —
+    # its only consumers are card renderers. So the card asserted "below 6.5
+    # anyway" / "passes score" against a bar no gate ever compares, and could say
+    # the opposite of the truth. Use the bar that actually decides. Display-only.
+    _mn_bar = (CONFLUENCE_FLAT_THRESHOLD
+               if matrix_result.get('market_regime') == 'FLAT'
+               else CONFLUENCE_SCORE_THRESHOLD)
+    _mn_note = ("clears the score bar, but the cascade is stricter"
+                if _mn_score >= _mn_bar else f"below the {_mn_bar:.1f} bar anyway")
```

The card was **asserting a fact derived from a bar nothing compares**, and could state the opposite
of the truth: a score of 5.5 in a FLAT regime rendered *"below 6.5 anyway"* when it in fact **clears**
the real 5.0 floor.

### 2c. SOL `main.py` — the header printed a number that did not decide

`MACRO_GATE_DRYRUN = False` (verified by import, 13:56), so the gate compares `_gate_score`
(= raw + macro penalty) while the header printed the **raw** `direction_score`. That is why card B
read `score=2.25 < thr=2.0`: **2.25 is not the quantity that lost to 2.0.**

```diff
@@ -2891,9 +2891,22 @@
          _wadj_line = _weight_adj_block(_w_breakdown)
+        # 🔴 2026-08-04 — THE HEADER PRINTED A NUMBER THAT DID NOT DECIDE.
+        # MACRO_GATE_DRYRUN is False, so the gate five lines up compares
+        # `_gate_score` (= _macro_gated_score = raw + macro penalty) — but this
+        # line printed the RAW `direction_score` against `_thr`. Result: cards
+        # reading "score=2.25 < thr=2.0", an inequality that is arithmetically
+        # false, because 2.25 is not the quantity that lost to 2.0. Print the
+        # deciding quantity next to the bar that decided, and show the raw value
+        # and the macro step that connect them (mirrors Titan main.py:3814).
+        # Display-only: `_gate_score`, `_macro_gate_adj` are already computed
+        # above and are not re-derived here.
+        _macro_tag = (f" | macro {_macro_gate_adj:+.1f}"
+                      if _macro_gate_adj else "")
          send_tg(
              f"🚫 <b>Below Threshold</b> ({direction})\n"
-            f"score={direction_score:.2f} &lt; thr={_thr:.1f}\n"
+            f"score={direction_score:.2f}{_macro_tag} → "
+            f"{_gate_score:.2f} &lt; thr={_thr:.1f}\n"
```

```
BEFORE   score=2.25 < thr=2.0                       ← false as written
AFTER    score=2.25 | macro -0.5 → 1.75 < thr=2.0   ← true, and the two steps are visible
```

### 2d. SOL `signal_matrix.py` — same dead number, same removal

```diff
@@ -509,9 +509,17 @@
+    # 🔴 2026-08-04 — `res['threshold']` REMOVED FROM THIS CARD. It carries
+    # LIQUIDITY_HEATMAP_TREND_THRESHOLD / _FLAT_THRESHOLD (4.0 / 6.5), and on
+    # THIS bot neither is wired to anything: the one and only score gate is
+    # CONFLUENCE_SCORE_THRESHOLD = 2.0 (main.py:2879), with no regime branch —
+    # SOL has no FLAT floor at all. Proof: 1,894 FLAT-regime rows passed the gate
+    # with a raw score BELOW 6.5. Printing 6.5 next to a refusal implied a floor
+    # that does not exist. The field is still returned by compute_score() and
+    # still stored in trade_signal_matrix; only the RENDERING drops it.
      parts = [
-        f"📊 score={res['score']:.2f}/10  →  <b>{res['direction']}</b>"
-        f"  (thr={res['threshold']:.1f} · {regime})",
+        f"📊 matrix net={res['score']:.2f}/10  →  <b>{res['direction']}</b>"
+        f"  ({regime} regime)",
      ]
```

**Where the dead number now stands:** removed from **both** renderers on **both** bots. It is not
"labelled as dead" anywhere in the feed, because a number no gate reads has no business being in a
card at all — it is still returned by `compute_score()` and still stored, for anyone replaying.

---

## 3. FREEZE CHECK — PASSED, RE-VERIFIED INDEPENDENTLY THIS SESSION

Your point 3: *confirm neither touches an advisor prompt, a gate, or a stored value.*

**Total change, all four files: 47 insertions / 7 deletions on Titan (`git show --stat 44731be`),
18 + 15 diff lines on SOL (`diff` vs `.bak_cards_20260804`).**

| file | every non-comment line added |
|---|---|
| titan `main.py` | `_next_bar` (ternary on `matrix_result['market_regime']`), `_raw_now` (`score_for_direction`), `_mn_bar` (same ternary), 6 f-string lines inside `send_tg` |
| titan `signal_matrix.py` | 2 f-string lines inside the `parts` list |
| sol `main.py` | `_macro_tag` (display string), 2 f-string lines inside `send_tg` |
| sol `signal_matrix.py` | 2 f-string lines inside the `parts` list |

- **No gate comparison.** `score_for_direction` (`signal_matrix.py:454-461`) is a two-branch dict
  read that returns `long_score` / `short_score` / `0.0` — **no I/O, no mutation**. `_next_bar`,
  `_mn_bar`, `_macro_tag` are locals used only inside f-strings. `_gate_score`/`_macro_gate_adj` on
  SOL are read, never re-derived; the gate line `if _gate_score < _thr:` is untouched.
- **No stored value.** `compute_score()` still returns `'threshold'` (`signal_matrix.py:447`) and
  `snapshot()` still writes it into `trade_signal_matrix` (`:551-561`). **Only the rendering drops
  it.** No `INSERT`/`UPDATE`/`update_trade`/`insert_signal` line is in either diff.
- **No advisor prompt.** `claude_advisor.py` is **untouched on both bots** — Titan's last change was
  `a85733f` (2026-08-03), SOL's file dates 2026-08-01; `44731be` touches only `main.py` and
  `signal_matrix.py`. Neither advisor file so much as mentions `format_for_telegram` or
  `['threshold']` (grep, exit 1 on both).
- **Where `format_for_telegram` output goes — all four Titan call sites traced, not assumed:**
  `main.py:1984`, `:3850`, `:4404` are inline inside `send_tg(...)` f-strings; `:4209` assigns it to
  the local `matrix_block`, whose **only** consumer is `msg`, sent by `send_tg(msg)` at `:4237` and
  never stored or prompted. SOL: `:2475`, `:2913`, `:3403`, all inline in `send_tg`. *(The earlier
  write-up said "only inside send_tg f-strings" — precise for three of four sites; the fourth is one
  hop away and lands in the same place.)*
- `python3 -m py_compile` clean on all four files (re-run 13:58).
- Applied with **zero open rows** in `virtual_positions`.

**No part of this touches an advisor prompt, a gate, or a stored value. I did not need to stop.**

## 4. LOADED, NOT JUST ON DISK

| | file mtime | service | started |
|---|---|---|---|
| titan `main.py` / `signal_matrix.py` | 13:22:31 / 13:23:32 | `titan.service` **active** | **13:29:03** (master PID 2058159, worker 2058215 13:29:13) |
| sol `main.py` / `signal_matrix.py` | 13:23:55 / 13:26:14 | `mercury-sol.service` **active** | **13:29:15** (master PID 2058227, worker 2058276 13:29:29) |

Both processes started **after** every edit, confirmed by `ps -o lstart` on the live PIDs, not by the
restart command's exit code. Backups `*.bak_cards_20260804` exist for all four files. Titan commit
`44731be`; **SOL is not under version control anywhere on this box** — the `.bak` files are its only
record, and I am not inventing a commit for it.

## 5. LIVE EXERCISE — WHAT HAS AND HAS NOT BEEN SEEN IN FLIGHT

Since the 13:29 restart, the journal shows **5 `HTF_WOULD_PASS` events (13:35:08, 13:50:10, 13:55:05,
13:55:06, 13:55:07) and 5 `HTF_NEUTRAL_15M_WOULD_BLOCK` — a 5-of-5 match.** Every one was caught by
the Variant-B 15m sub-gate and took the **BLOCKED** path.

Two consequences, both worth having:

1. **The BLOCKED card's fixes (§2a, §2b) are live-exercised.** The 13:35:08 signal is trades row
   **21322**, `htf_blocked`, regime FLAT, matrix net **2.00**, real bar **5.0**, dead value 6.5:

```
Matrix-net line   BEFORE  ℹ️ Matrix net: LONG 2.00/10 — below 6.5 anyway     ← decided by the dead bar
                  AFTER   ℹ️ Matrix net: LONG 2.00/10 — below the 5.0 bar anyway

matrix block      BEFORE  📊 score=2.00/10 → LONG  (thr=6.5 · FLAT)
                  AFTER   📊 matrix net=2.00/10 → LONG  (FLAT regime)
```

> **Precision about that claim:** the row and the timestamps are real; the rendering is produced by
> importing the *same* `signal_matrix.py` the worker loaded, with `res` reconstructed from the stored
> breakdown. **I did not intercept the Telegram bytes.** So: faithfully reproduced, **not
> byte-captured.**

2. 🔴 **The tolerate-NEUTRAL card itself has still NOT been observed in flight.** 5 of 5 candidates
   went to Variant-B instead. Its new text is unit-rendered and its code is loaded, but **no live
   firing has been seen**, so it is reported as **applied-and-loaded, not live-proven.** Same for
   both SOL changes — SOL has produced no below-threshold signal since its 13:29 restart.

**Side effect worth keeping:** those 5 events are also a live sighting of the **Variant-B sub-gate
refusing 1H-NEUTRAL signals at a 100 % rate in this window** — the very gate the withdrawn
"established fact" (§6.3) assumed was absent.

---

## 6. THE RECORD — five corrections written INTO the canonical OPEN-ITEMS

Canon edited and the dated snapshot generated **from it, in the same commit**, per the 2026-07-30
rule. Its header was **re-verified against runtime by importing `config`** (`LIVE_TRADING_ENABLED`
and `ORDER_ADAPTER_LIVE` both `True`, HEAD `44731be` by `git rev-parse`, 13:56 UTC) — not copied
forward; it had been carrying `957f980` and a 2026-07-30 verification date.

**Every number below was re-measured against `trades.db` at 13:56 UTC in this session.**

1. **§0 — `confluence_score` holds FOUR quantities, not three; `executed` rows hold RAW.**
   `main.py:4008` writes `adj_score`; `main.py:4162` → `signal_matrix.py:565-569` overwrites it with
   the raw matrix score **154 lines later**. **Re-measured: `confluence_score == raw` on 67 of 67**
   executed rows that have a matrix snapshot (the earlier pass measured 66/66; one entry has been
   added since — the two agree). The box's own validation line said *"27 executed as raw"* and its
   table said raw+adjustment; **they contradicted each other for five days. The check was right and
   the table was the defect** — recorded as a general rule, not a remark about one row.
   *Consequence:* on Titan the weight adjustment is not merely unapplied, it is **never recorded** —
   Titan has no `weighted_adj` column (SOL does), so any replay needing the historical adjustment is
   **unsatisfiable and must be declared so**, not skipped.
2. **§0 — the regime of a REFUSED row must be reconstructed from
   `matrix_breakdown_json.TREND.net_direction`** (`'FLAT'` iff `NEUTRAL`). `market_regime` is written
   **only on rows that passed the score gate**. **Re-measured: NULL on 699 of 699 `below_threshold`
   rows and 3 966 of 3 966 `htf_blocked` rows** since the floor's inception. *(The earlier pass
   reported 703/703 on a slightly wider predicate; the fraction is 100 % either way.)* Therefore
   `WHERE status='below_threshold' AND market_regime='FLAT'` returns **zero rows**, and **that single
   omission made a gate with 518 refusals read as inert.**
3. **§2 — established fact #1 WITHDRAWN.** *"The FLAT floor removed the label, not the trades"* is
   **wrong.** **Re-measured, floor inception `db71454` 2026-07-06 13:54 → now: 518 signals refused by
   the 5.0 FLAT floor and by nothing else** (FLAT-regime rows at or above the TREND bar in force —
   2.0 before `dee6cee`, 3.0 after — and below 5.0). **659 of 843 FLAT rows that reached the gate
   were refused (78.2 %)**, which *corroborates* the 78.86 % this file already carried rather than
   contradicting it. **The refutation was already in the canon; the wrong belief circulated outside
   it.** Both measurement traps recorded, including the general one: **a flat entry rate proves
   nothing about a gate when the refused cohort is substitutable** (post-floor, 601 TREND rows passed
   against 184 FLAT — the TREND channel alone holds the rate up). **Measure a gate's own refusals,
   never downstream throughput.**
4. **§2.45b — `trend_1d` was never a veto and `trend_4h` was never a cascade tier.** Both were
   asserted by me today; both are wrong. Refusals attributable to either, all-time: **0, because
   neither is a gate.** Generalised: ***"I remember it gating" is not evidence* — confirm a mechanism
   by finding the comparison that consumes the value, never by finding the value.**
5. **§2.45a — the EMA envelope (1h + 15m both Expanding) logged as a HYPOTHESIS WITH A POSITIVE
   PRIOR**, under §2.45's ruling, **not as a finding.** n=40 (**34 of them paper**, at 68× the live
   notional): +0.473 vs −0.226 mean R, **Δ+0.699R, perm-p 0.029** — **fails Bonferroni** (~12 cells
   tested, α≈0.004) and is the *best of* those cells, the exact construction that produced §4's items
   3, 9 and 10. **It admits 7 of 7 live entries, which returned −1.89R** — zero discriminating power
   on the only cohort that matters. **Only live-era data (~30 entries ≈ three weeks) can promote
   it.** Recorded so it is neither rebuilt from scratch nor mistaken for a result.

---

## 7. WHAT IS NOT CLOSED

- 🔴 **The tolerate-NEUTRAL card has not been seen in flight** (§5.2). Applied and loaded, not
  live-proven.
- 🔴 **Both SOL changes have not been seen in flight** — no below-threshold signal since 13:29.
- **The `executed`-row overwrite is RECORDED, NOT FIXED.** Fixing it changes a **stored value** and
  therefore needs its own cycle, outside this freeze. Titan still has no `weighted_adj` column.
- **SOL remains outside version control.** Every SOL claim here rests on file mtimes, `.bak`
  snapshots and live imports — there is no commit to quote and I did not manufacture one.
