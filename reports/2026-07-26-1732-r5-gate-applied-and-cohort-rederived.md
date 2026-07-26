# r5-gate-applied-and-cohort-rederived

_2026-07-26 17:32 UTC_

---

# TITAN R5 — regime gate APPLIED + counter-short cohort RE-DERIVED

**2026-07-26 · Part A applied and live (commit `596fbdf`). Part B read-only.**
Tree clean. Paper mode.

**Headline: the re-derivation says the gate is not enough. The 06-27 cohort definition is
INVERTED on current data — the caution now fires precisely where the veto is LEAST justified.
Recommendation: RETIRE the caution, not re-gate it.** Detail in Part B.

---

# PART A — `trend_1d != 'bull'` gate: applied, confirmed

Commit `596fbdf`. Snapshot taken first: tag `pre-countershort-regimegate-20260726` (at `93c20c3`)
+ `claude_advisor.py.bak_regimegate_20260726` (md5 `eec8b748face756419050da8e2b4b0bc`).

### The applied diff
```diff
--- a/claude_advisor.py
+++ b/claude_advisor.py
@@ -296,11 +296,26 @@
     # (-0.26/-0.49/-0.35% at 4h/12h/24h). Counter-LONGs and ADX>=22 are
     # deliberately untouched (near-flat / unproven). Titan-only; NOT for SOL
     # (its same cohort is +EV — do not port).
+    #
+    # DAILY-REGIME GATE added 2026-07-26. The study above was measured ENTIRELY in a
+    # non-bull daily tape — its 93 drift-complete skips were trend_1d bear (61) and
+    # neutral (32), with ZERO bull samples, because trend_1d='bull' did not exist in
+    # Titan's history until 2026-07-10. Once it did, the cohort's drift INVERTED:
+    #   trend_1d='bull'      n=15  4h +0.165%  12h +0.631% (67% positive, t=+2.0)
+    #   trend_1d!='bull'    n=138  4h -0.100%  12h -0.116% (26% positive)
+    #   original window      n=93  4h -0.150%  12h -0.310% (17% positive, t=-2.4)
+    # Positive drift = the SKIPPED short would have won, i.e. the caution costs money.
+    # So in a bull daily regime this caution was steering the advisor away from shorts
+    # that went on to work. Restrict it to the regime it was actually validated in
+    # rather than deleting it: bear/neutral evidence is unchanged and still negative.
+    # Rollback = drop the trend_1d clause + restart.
     _ct_dir = (m5.get('direction') or '').upper()
     _ct_adx = _vs.get('srv_adx_1h')
+    _ct_d1 = (_vs.get('trend_1d') or '').lower()
     if (_ct_dir in ('SHORT', 'SELL')
             and (_vs.get('ema_status_1h') or '') == 'Bullish'
-            and isinstance(_ct_adx, (int, float)) and _ct_adx < 22):
+            and isinstance(_ct_adx, (int, float)) and _ct_adx < 22
+            and _ct_d1 != 'bull'):
         user += (
             "\n⚠️ STATISTICAL CAUTION (counter-trend short, flat 1h): this is a "
             "SHORT while the 1h EMA is Bullish and 1h ADX < 22 (no established "
```

### The five confirmations

**(1) Only `claude_advisor.py` changed**
```
git status --porcelain  ->  M titan-bot/claude_advisor.py   (single file)
git diff --stat HEAD    ->  1 file changed, 16 insertions(+), 1 deletion(-)
config.py       md5 1a4746e072c74248a0efeefe4b206fdc   unchanged
virtual_trader  md5 cfb7f1307957e8ca4532574ecc6e26e8   unchanged (R1 state)
```
Three lines of actual code; the rest is comment:
```
+    _ct_d1 = (_vs.get('trend_1d') or '').lower()
-            and isinstance(_ct_adx, (int, float)) and _ct_adx < 22):
+            and isinstance(_ct_adx, (int, float)) and _ct_adx < 22
+            and _ct_d1 != 'bull'):
```

**(2) The caution still fires for non-bull**
The `if` condition was extracted **by AST from the deployed file** and from the snapshot, then both
were evaluated against all 38 real historical injections:
```
STILL FIRE (non-bull)          : 23
SUPPRESSED (trend_1d='bull')   : 15    (2026-07-11 .. 07-19)
anomalies                      : 0
```
Truth table of the deployed expression:
```
dir    ema_1h     adx  trend_1d   ->  OLD    NEW
SHORT  Bullish   13.5  neutral    ->  True T.
SHORT  Bullish   13.5  bear       ->  True T.
SHORT  Bullish   13.5  bull       ->  True F.
SHORT  Bullish   13.5  BULL       ->  True F.    (case-insensitive, .lower())
SHORT  Bullish   13.5  None       ->  True T.     (null 1d -> caution kept)
SHORT  Bullish   25.0  neutral    ->  False F.
SHORT  Bearish   13.5  neutral    ->  False F.
LONG   Bullish   13.5  neutral    ->  False F.
SELL   Bullish   21.9  bear       ->  True T.
```

**(3) Service healthy**
```
systemctl is-active -> active, MainPID 3163914, NRestarts 0
17:28:12 Started · 17:28:15 Listening 127.0.0.1:5000 · 17:28:20 [RECONCILE] done
17:28:20 breakeven_worker started · 17:28:21 virtual_trader worker started (closed=26/30)
17:28:22 [OB-DENSITY] ctVal=0.01 from OKX spec · heartbeat +1 rows / 0 failures
journal grep traceback|exception|error -> none
```

**(4) The R1 fix from `93c20c3` intact**
```
973:  def _tighten_sl(position_side, entry_price, current_sl, original_sl=None):
1004:     new_sl = min(new_sl, float(original_sl))   # never tighter than ORIGINAL
1009:     new_sl = max(new_sl, float(original_sl))   # never tighter than ORIGINAL
1122:     symbol, _tighten_sl(position_side, entry_price, current_sl, original_sl=_orig_sl)))
git diff HEAD --name-only -- titan-bot/virtual_trader.py  ->  0 files
```

**(5) Nothing else touched**
```
CONFLUENCE_SCORE_THRESHOLD = 2.0    CONFLUENCE_FLAT_THRESHOLD = 5.0
WALL_TRAIL_LIVE_ENABLED = False     POST_ENTRY_RECHECK_ENABLED = True
ADX_BELOW_FLOOR = 20.0 (-5)         HEALTH_SCORE_EMERGENCY/-TIGHTEN = -10 / -5
mercury-sol/claude_advisor.py mtime Jul 4 22:11 (untouched) · mercury-sol.service active
```

### Rollback
```bash
git checkout pre-countershort-regimegate-20260726 -- titan-bot/claude_advisor.py
# or: cp claude_advisor.py.bak_regimegate_20260726 claude_advisor.py
# or: git revert 596fbdf
sudo systemctl restart titan.service
```

---

# PART B — Re-derivation on post-06-27 data only (read-only)

Population: `ai_skipped` SHORT with completed drift, `skip_ts >= 2026-06-27`.
n = 503 / 494 / 492 at 4h / 12h / 24h.
Convention: **drift > 0 = the SKIPPED short would have WON** (the veto cost us);
**drift < 0 = the veto was RIGHT**. We are hunting for reliably NEGATIVE sub-cohorts.

### B.1 Baseline first — the advisor's skipping is broadly correct
```
ALL post-06-27 ai_skipped SHORT   4h -0.132% (p<0.001) · 12h -0.090% (p=0.047) · 24h -0.163% (p=0.015)
```
Every cohort below is reported as **excess over this baseline**, because "negative" alone is not
interesting when the whole population is negative.

### B.2 Decompose the 06-27 definition — the ADX half is the problem

| sub-cohort (12h) | n | mean | pos% | t | p | verdict |
|---|---|---|---|---|---|---|
| current: `ema_1h Bullish AND ADX<22` | 60 | **+0.372%** | 50 | +2.5 | 0.012 | **NOT -EV** |
| + the gate just applied (`AND 1d!=bull`) | 45 | **+0.286%** | 44 | +1.7 | 0.084 | **NOT -EV** |
| condition A alone: `ema_1h Bullish` | 303 | -0.047% | 39 | -1.0 | 0.340 | leans -EV, n.s. |
| condition B alone: `ADX-1h < 22` | 167 | **+0.318%** | 62 | +3.3 | 0.001 | **NOT -EV** |

The counter-trend condition is roughly neutral. **The ADX condition carries all the signal and it
now points the other way.**

### B.3 The ADX relationship, bucketed — and it is not a bull-tape artifact

Post-06-27, 12h, excess vs the -0.090% baseline:

| ADX-1h | n | mean | pos% | excess | p |
|---|---|---|---|---|---|
| **< 15** | 48 | **+1.055%** | **85** | +1.145% | 0.0000 |
| 15-18 | 36 | +0.145% | 53 | +0.235% | 0.251 |
| 18-22 | 83 | -0.033% | 53 | +0.057% | 0.831 |
| 22-25 | 63 | +0.234% | 48 | +0.324% | 0.015 |
| **25-30** | 101 | **-0.636%** | **14** | -0.546% | 0.0000 |
| **>= 30** | 163 | -0.294% | 35 | -0.205% | 0.0000 |

Same buckets **restricted to `trend_1d != bull`** (i.e. with the bull tape removed entirely):
```
< 15    n= 35  +1.179%  94% positive  p=0.0000     <- even stronger
15-18   n= 20  -0.186%  40%           p=0.195
18-22   n= 59  -0.056%  56%           p=0.791
22-25   n= 19  +0.617%  79%           p=0.008
25-30   n= 71  -0.719%  17%           p=0.0000
>= 30   n=103  -0.575%  20%           p=0.0000
```
**The inversion is not the bull tape.** Low-ADX shorts that the advisor skipped went on to work,
in bear and neutral regimes too. 94% of the ADX<15 non-bull skips drifted the short's way.

And the original window did **not** contain this structure at all:
```
pre-06-27, 12h:  <15 +0.178% (n=13) · 15-18 +0.959% (n=35) · 18-22 -0.100% (n=94)
                 22-25 +0.193% (n=118) · 25-30 -0.283% (n=101) · >=30 +0.261% (n=85)
```
No monotone ADX effect either way. The -0.49%/12h headline was an aggregate over a cohort whose
internal structure never supported it.

### B.4 Is ANY sub-cohort of counter-trend shorts still reliably -EV?

36 candidate definitions tested (ADX thresholds, `ema_status_1h`, `ema_gap_dir_1h`, `trend_1h/4h/1d`,
`market_regime`, and combinations). Bonferroni threshold for 36 tests: **p < 0.0014**.

Twelve passed the naive filter (mean<0, p<0.05, n>=30). Those clearing **Bonferroni**, with excess:

| cohort | n | mean 12h | excess | p |
|---|---|---|---|---|
| `ADX-1h >= 25` | 264 | -0.425% | **-0.335%** | 0.0000 |
| `ADX-1h >= 22` | 327 | -0.298% | -0.208% | 0.0000 |
| `trend_1d = neutral` | 209 | -0.297% | -0.207% | 0.0002 |
| `ema_1h Bullish AND ADX >= 25` | 191 | -0.272% | -0.183% | 0.0000 |
| `ema_gap_dir_1h = Contracting` | 250 | -0.171% | -0.081% | 0.0007 |
| `trend_1h bull AND ADX >= 22` | 141 | -0.237% | -0.147% | 0.0005 |

Did **not** clear Bonferroni: `ema_gap_dir_1h=Flat` (p=0.0045, n=31 — thin), `ema1h Bull +
trend_1d!=bull` (p=0.014), `ema1h Bull + regime TREND` (p=0.007), `ema1h Bull + gap Contracting`
(p=0.044), `ADX>=30` at 4h.

**Answer to the question as posed: NO.** Not one surviving cohort is a *low-ADX counter-trend*
cohort. Every survivor is the **opposite** condition — high ADX. The defining premise of the
06-27 caution ("no established trend ⇒ don't short into a bullish 1h") is not merely weakened;
its sign is reversed on current data.

### B.5 Why I am NOT proposing an inverse caution — a methodological limit

The survivors above are tempting: "caution on ADX>=25 shorts instead". **That would be a mistake,
and not because of n.** Skip-drift is measured on an **already-skipped population**. It can tell us
whether a veto was right; it cannot tell us whether a *caution* adds anything, because every row in
it was already a skip. A caution on `ADX>=25` would fire where the advisor **already** skips
correctly — it would change nothing and be, once again, unmeasurable. That is the same trap Part 1
of the earlier report identified.

Per your instruction, no new filter is proposed on this evidence.

### B.6 Where that leaves the applied gate

```
current caution cohort            n=60  +0.372%  excess +0.462%  p=0.012
after the gate applied today      n=45  +0.286%  excess +0.375%  p=0.084
```
The gate strictly reduces harm — it removes the worst 15 samples — but the remainder is **still
wrong-signed**. It buys time; it does not make the caution correct.

**Recommendation: RETIRE the counter-short caution.** Not gate it further, not invert it. It is a
caution firing on a cohort where entering is currently +EV, it has never been shown to change a
decision, and its founding statistic does not reproduce. Retiring is a deletion, not a new filter,
so it does not need fresh n to justify — it needs only the failure of the old n to hold up, which
is established above at n=60 (p=0.012) plus the structural argument in B.3.

If you prefer to keep it live: the gate applied today is the correct interim state, and it costs
little — 23 remaining injections over ~7 weeks.

**Decision requested:** retire the caution entirely, or hold it at today's gate and revisit once
the R4 A/B arm has produced measurable evidence about whether soft cautions move decisions at all.

---

Applied this session: `93c20c3` (R1 recheck bound), `596fbdf` (R5 regime gate). Tree clean,
`titan.service` healthy. Nothing in Part B was applied.
