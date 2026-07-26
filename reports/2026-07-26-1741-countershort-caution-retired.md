# countershort-caution-retired

_2026-07-26 17:41 UTC_

---

# TITAN — counter-short soft caution RETIRED, live and confirmed

**2026-07-26 17:39 UTC · APPLIED.** Commit `b878535`, tree clean, `titan.service` healthy.
Paper mode. The caution is gone from the code; a historical note holds its place.

---

## 1. What shipped

The `STATISTICAL CAUTION` block is **removed entirely** — not gated further, not inverted.
One file, `claude_advisor.py`: **0 lines of code added, 17 removed**, replaced by a 28-line comment
at the same location so a future session finds the verdict exactly where it would rebuild the rule.

Lifecycle for the record: introduced 2026-06-27 → gated on `trend_1d != 'bull'` earlier today
(`596fbdf`) → retired now (`b878535`).

Snapshot before applying: tag `pre-countershort-retire-20260726` (at `596fbdf`) +
`claude_advisor.py.bak_retire_20260726` (md5 `3769cb5f3c9f5a53df2a2b287382f99a`).

---

## 2. The diff

```diff
--- a/claude_advisor.py
+++ b/claude_advisor.py
@@ -289,43 +289,33 @@
     )
     if news_summary:
         user += f"\nRecent news (last 2h):\n{news_summary[:500]}\n"
-    # Counter-trend EMA-1h soft caution — evidence-backed, ADVISORY ONLY (not a
-    # veto). Study 2026-06-27 [project_counter_trend_ema1h_study]: SHORT into a
-    # Bullish 1h EMA while 1h ADX < 22 (no established trend) has persistent
-    # NEGATIVE expected drift on Titan: -0.49%/12h, 12% positive, n=143
-    # (-0.26/-0.49/-0.35% at 4h/12h/24h). Counter-LONGs and ADX>=22 are
-    # deliberately untouched (near-flat / unproven). Titan-only; NOT for SOL
-    # (its same cohort is +EV — do not port).
-    #
-    # DAILY-REGIME GATE added 2026-07-26. The study above was measured ENTIRELY in a
-    # non-bull daily tape — its 93 drift-complete skips were trend_1d bear (61) and
-    # neutral (32), with ZERO bull samples, because trend_1d='bull' did not exist in
-    # Titan's history until 2026-07-10. Once it did, the cohort's drift INVERTED:
-    #   trend_1d='bull'      n=15  4h +0.165%  12h +0.631% (67% positive, t=+2.0)
-    #   trend_1d!='bull'    n=138  4h -0.100%  12h -0.116% (26% positive)
-    #   original window      n=93  4h -0.150%  12h -0.310% (17% positive, t=-2.4)
-    # Positive drift = the SKIPPED short would have won, i.e. the caution costs money.
-    # So in a bull daily regime this caution was steering the advisor away from shorts
-    # that went on to work. Restrict it to the regime it was actually validated in
-    # rather than deleting it: bear/neutral evidence is unchanged and still negative.
-    # Rollback = drop the trend_1d clause + restart.
-    _ct_dir = (m5.get('direction') or '').upper()
-    _ct_adx = _vs.get('srv_adx_1h')
-    _ct_d1 = (_vs.get('trend_1d') or '').lower()
-    if (_ct_dir in ('SHORT', 'SELL')
-            and (_vs.get('ema_status_1h') or '') == 'Bullish'
-            and isinstance(_ct_adx, (int, float)) and _ct_adx < 22
-            and _ct_d1 != 'bull'):
-        user += (
-            "\n⚠️ STATISTICAL CAUTION (counter-trend short, flat 1h): this is a "
-            "SHORT while the 1h EMA is Bullish and 1h ADX < 22 (no established "
-            "trend). Historically this exact cohort has NEGATIVE expected drift: "
-            "-0.49%/12h, only 12% of cases positive (n=143), persistent at "
-            "-0.26/-0.49/-0.35% over 4h/12h/24h. Treat as a strong headwind and "
-            "require clear independent confirmation (fresh 5m structure break, "
-            "real order-book support) before deciding 'execute'. Advisory only — "
-            "you may still execute if the setup is genuinely strong.\n"
-        )
+    # ── RETIRED 2026-07-26: counter-trend EMA-1h soft caution (lived 06-27 .. 07-26) ──
+    # A caution was injected here for SHORT + 1h EMA Bullish + 1h ADX < 22, citing
+    # "-0.49%/12h, 12% positive, n=143" from the 2026-06-27 study. It is GONE. Do not
+    # rebuild it — the founding statistic does not reproduce, and re-deriving the cohort
+    # from scratch on post-06-27 skip-drift INVERTED its sign:
+    #   ADX-1h < 15   n=48  12h +1.055%  85% positive  p<1e-4   <- skipping these COST us
+    #   ADX-1h < 22   n=167 12h +0.318%  62% positive  p=0.001     (the caution's own cohort)
+    #   ADX-1h >= 25  n=264 12h -0.425%  27% positive  p<1e-4   <- the OPPOSITE condition
+    # Positive drift = the SKIPPED short would have won. Not a bull-tape artifact: inside
+    # trend_1d != 'bull' the ADX<15 slice is +1.179% with 94% positive. The counter-trend
+    # half (ema_1h Bullish alone) is ~neutral: -0.047%, p=0.34 — the ADX half carried all
+    # the signal and it now points the other way. 36 candidate definitions were tested;
+    # at the Bonferroni threshold for 36 tests (p < 0.0014) NOT ONE surviving sub-cohort is
+    # low-ADX counter-trend — every survivor is high-ADX, i.e. the inverse condition. The
+    # same ADX structure was absent even in the original pre-06-27 window.
+    # An inverse caution was deliberately NOT built: skip-drift is measured on an
+    # ALREADY-SKIPPED population, so it can show whether a veto was right but never whether
+    # a caution adds anything — the advisor already skips those correctly.
+    # Also note the mechanism itself was fine: the line provably reached the model (38/38
+    # eligible payloads) and was quoted back in 87% of its reasons vs 0.9% control
+    # (p~6e-14). It was the STATISTIC that was stale, not the channel.
+    # Baseline that still stands: ALL post-06-27 ai_skipped SHORTs drift -0.090%/12h
+    # (p=0.047) — the advisor's own skipping is broadly correct and is NOT changed by this
+    # removal. We stopped feeding it a stale number; we did not touch its judgement.
+    # History: 2026-06-27 introduced · 2026-07-26 gated on trend_1d != bull (596fbdf)
+    # · 2026-07-26 retired (this commit). See project_counter_trend_ema1h_study and
+    # kola-reports/reports/2026-07-26-1732-r5-gate-applied-and-cohort-rederived.md
     user += (
         "\nThe 3 timeframes are aligned (confluence has already passed). "
         "Decide whether the bot should execute the DCA entry now."
```

---

## 3. The five confirmations

### (1) Only `claude_advisor.py` changed
```
git status --porcelain  ->  M titan-bot/claude_advisor.py    (single file)
git diff --stat HEAD    ->  1 file changed, 27 insertions(+), 37 deletions(-)
added lines that are CODE   : 0
removed lines that are CODE : 17
config.py       md5 1a4746e072c74248a0efeefe4b206fdc   unchanged
virtual_trader  md5 cfb7f1307957e8ca4532574ecc6e26e8   unchanged (R1 state)
```

### (2) No caution block remains, and no signal can now receive an injection
Checked by AST against the deployed file, not by grep alone:
```
string literals containing 'STATISTICAL CAUTION' in the AST : 0
if-conditions referencing _ct_adx / ema_status_1h=='Bullish' : 0
occurrences of _ct_dir / _ct_adx / _ct_d1 as Names           : 0 / 0 / 0
'STATISTICAL CAUTION' anywhere in the source (incl. comments): 0
historical note 'RETIRED 2026-07-26' present                 : True
```
Injection count going forward is **0 by construction** — there is no longer any branch in
`consult_for_entry` that appends a caution to the prompt. The remaining `user +=` sites are the
unconditional context sections (ATR/volume, timeframe block, HTF trend block, L/S ratio, order-book
walls, news) and the closing instruction. Nothing was added in their place.

Historical evidence for scale: 38 payloads carried the caution between 2026-07-06 and 2026-07-26.
Verification query for the next eligible SHORT — it must return 0 rows:
```sql
SELECT id, timestamp FROM trades
WHERE ai_user_prompt LIKE '%STATISTICAL CAUTION%' AND timestamp > '2026-07-26 17:39';
```

### (3) Service healthy
```
systemctl is-active -> active, MainPID 3166671, NRestarts 0
17:39:24 Started · 17:39:28 Listening 127.0.0.1:5000 · 17:39:33 [RECONCILE] done
17:39:33 breakeven_worker started · 17:39:33 virtual_trader worker started (closed=26/30)
17:39:35 [OB-DENSITY] ctVal=0.01 from OKX spec · heartbeat +1 rows / 0 failures
journal grep traceback|exception|error -> none
```

### (4) R1 (`93c20c3`) and the rest of config intact
```
973:  def _tighten_sl(position_side, entry_price, current_sl, original_sl=None):
1004:     new_sl = min(new_sl, float(original_sl))   # never tighter than ORIGINAL
1009:     new_sl = max(new_sl, float(original_sl))   # never tighter than ORIGINAL
git diff HEAD --name-only -- virtual_trader.py config.py  ->  0 files

CONFLUENCE_SCORE_THRESHOLD = 2.0     CONFLUENCE_FLAT_THRESHOLD = 5.0
WALL_TRAIL_LIVE_ENABLED = False      POST_ENTRY_RECHECK_ENABLED = True
ADX_BELOW_FLOOR = 20.0 (-5)          HEALTH_SCORE_EMERGENCY / _TIGHTEN = -10 / -5
```

### (5) SOL untouched
```
/mnt/volume_nyc1_1780480650620/mercury-sol/claude_advisor.py  mtime 2026-07-04 22:11
'STATISTICAL CAUTION' in the SOL advisor : 0   (it was never ported there — by design)
mercury-sol.service : active
```

---

## 4. Explicit confirmation: this does NOT change the advisor's judgement

Requested explicitly, and it is worth stating precisely because it is the whole point of the change.

* **What was removed is an INPUT, not a rule.** The caution was a paragraph of prose appended to the
  prompt. It had no veto power, no score weight, no gate. `consult_for_entry`'s signature, its system
  prompt, its return contract and every other section of the user prompt are **byte-identical** —
  the diff adds 0 lines of code. The model receives exactly the same market data as before, minus
  one stale sentence about a statistic that no longer holds.
* **The advisor's own reasoning is untouched.** It still sees 1h EMA status, 1h ADX, the full 5-TF
  trend block, MTF alignment, order-book walls, volume and news, and still weighs them itself. In
  the 38 caution payloads it was *already* citing "1h BULL opposes SHORT", "MTF alignment 0/4" and
  "ask wall ×7.3" as independent grounds; those inputs remain.
* **The baseline finding stands as-is and is NOT invalidated by this removal.** All post-06-27
  `ai_skipped` SHORTs drift **-0.132%/4h (p<0.001), -0.090%/12h (p=0.047), -0.163%/24h (p=0.015)**,
  i.e. the advisor's skipping is broadly correct on its own judgement. That is measured on decisions
  the advisor made itself; removing an input we were feeding it does not change what that population
  showed. It is also the reason retirement is safe: the advisor was not relying on the caution to
  skip correctly.

We stopped feeding it a stale number. We did not touch how it thinks.

---

## 5. Rollback
```bash
git checkout pre-countershort-retire-20260726 -- titan-bot/claude_advisor.py
# or: cd /root/titan-bot && cp claude_advisor.py.bak_retire_20260726 claude_advisor.py
# or: git revert b878535
sudo systemctl restart titan.service
```
Reverting `b878535` alone restores the gated version (`596fbdf` state), not the ungated original.

---

## 6. Session state

Applied today, in order:
```
93c20c3  R1 — bound the post-entry recheck TIGHTEN at the original SL distance
596fbdf  R5 — gate the counter-short caution on trend_1d != 'bull'   (superseded below)
b878535  R5 — RETIRE the counter-short caution entirely
```
Tree clean. `titan.service` healthy. Mercury-SOL untouched throughout.

Still open from the audit, unchanged: R2 (prior-move bucket caution), R4 (vol_ratio_5m ceiling —
to be built with the deterministic `row_id % 2` A/B arm), and the wait-list items
(chop-short gap=Flat, smart-exit chop, order-book percentile, TOLN, regime-FLAT high-ADX).
