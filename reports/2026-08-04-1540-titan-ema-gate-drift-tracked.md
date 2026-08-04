# THE MOST AGGRESSIVE GATE IS NOW GRADED — AND THE CHANGE YOU ASKED FOR WOULD NOT HAVE WORKED ALONE

**2026-08-04 15:40 UTC · Titan LIVE, real money, flat · commit `14319a5`**
**Applied from flat, restart 15:36:11, `py_compile` clean. Observation only: 5 lines of code.**

Canon: **§2.47 extended** in the same commit; snapshot `reports/2026-08-04-1540-open-items.md`.

---

## 🔴 0. THE HALF THAT WAS MISSING FROM THE REQUEST

You asked for `ema_envelope_blocked` to be added to `skip_attribution.TRACKED_STATUSES`. **That alone
would have collected zero rows.** `_record_skip_attribution` is called at six sites in `main.py` —
`htf_blocked` ×1, `below_threshold` ×3, `ai_skipped` ×2 — and **none of them is in
`_ema_envelope_gate`.** I never wired the hook when I built the gate at 14:41.

**So the status would have been in the tracked tuple, the machinery would have been ready, and
nothing would ever have arrived** — the gate would have *read as tracked* while grading nothing.
That is this book's single most frequent defect shape, and it would have been invisible for exactly
as long as nobody queried the table.

**Both halves shipped together:**

```diff
# skip_attribution.py
-TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked')
+TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked',
+                    'ema_envelope_blocked')

# main.py — inside _ema_envelope_gate, AFTER the refusal is decided and stored
+    _record_skip_attribution(
+        row_id, symbol, direction, 'ema_envelope_blocked',
+        matrix_result=matrix_result,
+        confluence_score=signal_matrix.score_for_direction(matrix_result, direction))
```

**Also corrected in the same edit:** the module docstring *and* the comment above `TRACKED_STATUSES`
both said only two statuses were tracked and that `htf_blocked` was *"EXCLUDED by design"* — sitting
directly above a **three**-tuple that included it. **The tuple was right and the prose was stale**,
the same table-vs-check defect §0 records. Fixed rather than left for the next reader to trip on.

## 1. ITEM 2 — THE MACHINERY IS STATUS-AGNOSTIC. NOTHING PER-STATUS IS NEEDED.

Audited rather than assumed. In `skip_attribution.py`, the skip `status` appears in **exactly three
places**:

| use | line | consequence |
|---|---|---|
| scope filter | `if status not in TRACKED_STATUSES: return` | the only gate on entry to the ledger |
| stored column | the `INSERT` tuple | a label, read by nobody at write time |
| log line | `logger.info("skip anchored … status=%s")` | cosmetic |

**No sampler branches on it.** `tick()` selects by `tracking_status='active'`; `_create_drift_rows`
uses only the skip timestamp; `_compute_drift_pct(anchor, sample_price, direction)` uses only the
direction. The five horizons (15m/1h/4h/12h/24h), the degraded-sample grace, the 24 h 30 m hard cap
and the max-favourable watermark are all status-blind. **Cost of adding a status: one tuple entry.**

## 2. ITEM 3 — WHAT THIS CHANGES: NOTHING THAT DECIDES ANYTHING

| claim | evidence |
|---|---|
| no gate changes | the diff contains **no** `CONFLUENCE_*`, `HTF_*`, `EMA_ENVELOPE_*`, `_eff_thr`, risk or advisor line — grepped |
| no verdict changes | `claude_advisor.py` not in the diff; the ledger feeds no prompt |
| no stored decision changes | the only writes are to `skip_attribution` / `skip_drift_samples`, two isolated tables; `trades` and `virtual_positions` are untouched by this change |
| the drift row is written **after** the refusal | order inside the gate: **the `dirs` test decides → `insert_signal(status='ema_envelope_blocked')` → `update_signal_execution` → `_record_skip_attribution`**. The observatory cannot sit upstream of what it grades |
| a failure here cannot reach the trade path | `_record_skip_attribution` wraps everything in `try/except`, and `on_skip` self-guards a second time |

**Total: 5 non-comment lines across 2 files. No existing line was modified except the two-line tuple
and the stale prose.**

⚠️ **One thing this DOES store, declared rather than discovered later:** `confluence_score` on these
rows holds the **RAW matrix direction score**, not the gated score the other statuses store — this
gate runs *before* the macro adjustment, so no gated score exists yet. Documented at the call site
and in §2.47. **Never compare that column across statuses** (§0's rule, applied forward this time).
Walls are NULL by construction: the OKX book is only fetched later on the AI path.

## 3. ITEM 4 — WHEN THIS BECOMES ANSWERABLE. YOUR ESTIMATE IS RIGHT.

**Arrival rate, measured two ways and they agree:** signals reaching the envelope's position in the
chain run **51.3/day (last 7 days)** and **50.5/day (last 30 days)** — **~2.1/hour**, which is your
"~2 refusals per signal-hour" almost exactly. At the measured refusal rate (**84.6 % LONG / 78.4 %
SHORT**, ~80 % overall) that is **~40 refusals/day ≈ 1.7/hour**.

**Empirical drift dispersion**, from the 8,800+ samples the existing statuses have already produced:

| horizon | SD | n for a ±0.25 % CI | n for ±0.50 % |
|---|---|---|---|
| 15m | 0.226 % | 4 | 1 |
| 1h | 0.402 % | 10 | 3 |
| **4h** | **0.809 %** | **41** | 11 |
| 12h | 1.188 % | 87 | 22 |
| 24h | 1.646 % | 167 | 42 |

**Therefore, at ~40 refusals/day:**

| what becomes readable | n | time |
|---|---|---|
| ±0.50 % CI at 4h | 11 | **6 hours** |
| ±0.25 % CI at 4h | 41 | **1 day** |
| a first genuine split | 100 | **2.5 days** |
| resolving a **0.06 %** effect — the size the other gates actually show | ~700 | **17 days** |

**Days-to-weeks, not months. You were right, and the correction runs the other way from the one you
offered:** the arrival rate is not lower than you thought. For comparison, the 20-executed-entries-
per-side review point is **~3 months** at 0.47 entries/day.

🔴 **THE ONE NUMBER THAT SETS THE BAR, AND IT IS ALREADY MEASURED.** The existing refused cohorts sit
at, at the 4h horizon:

```
ai_skipped        mean -0.059%   (t = -3.23, n = 2000)     ← refused signals drifted AGAINST themselves
below_threshold   mean -0.073%   (t = -2.75, n =  875)     ← same
htf_blocked       mean +0.020%   (t = +1.90, n = 5974)     ← barely positive
```

**A healthy refuser sits at or below zero.** So "the gate is refusing winners" is not a free
parameter — it means the envelope's cohort landing **materially above `htf_blocked`'s +0.020 %**.

⚠️ **What the drift cannot answer, stated with the triggers and not after them:** it measures whether
**price moved the refused signal's way**, not whether the **trade** would have won — no stop, no
trail, no fees, no partial. A positive drift is evidence the gate refuses *moves*; it is not proof it
refuses *winners*. **This is the cheap early check. The 20-per-side review remains the honest
expensive one, and it is joined, not replaced.**

**First observation, reported because it is the arrival rate's only real test:** at 15:36 there were
**zero** `ema_envelope_blocked` rows — the gate has been live since 14:41 and both legs have been
`Expanding` on every signal since. **The projections above rest on the pre-gate population. The first
day's actual count settles the rate, and it will be reported.**

## 4. ITEM 5 — PRE-COMMITTED REVISIT TRIGGERS, WRITTEN BEFORE ANY DATA EXISTS

Recorded in **OPEN-ITEMS §2.47**, in these words, so they cannot be invented afterwards:

1. **FAST TRIGGER** — at **n ≥ 100** refusals, if the mean 4h drift is **≥ +0.25 %** with a 95 % CI
   excluding zero → **revisit the gate immediately, before the review point.** (~2.5 days.)
2. **SLOW TRIGGER** — at **n ≥ 700**, if the mean 4h drift is **positive with a 95 % CI excluding
   zero** → revisit. (~17 days.)
3. **COMPARATOR** — the three cohorts above. Sitting materially above `htf_blocked`'s +0.020 % is the
   alarm.

**The 20-executed-entries-per-side review point stands. It is JOINED by this, not replaced** — and
the reason to say so now is that a gate applied on 34 paper trades, failing Bonferroni, refusing 59 %
of the book, should not have to wait three months to be caught being wrong.

## 5. SCOPE

Observation only. **Not touched:** the EMA envelope gate itself and its threshold, the HTF cascade,
the FLAT floor, Variant-B, the score bars, the risk gates, both advisor prompts, and the entire exit
side. Two files (`main.py`, `skip_attribution.py`), 5 lines of code, backups
`*.bak_drifttrack_20260804`. Applied with **0 open positions**; restart **15:36:11**; LIVE banner
clean; `TRACKED_STATUSES` verified by runtime import as
`('ai_skipped', 'below_threshold', 'htf_blocked', 'ema_envelope_blocked')`.
