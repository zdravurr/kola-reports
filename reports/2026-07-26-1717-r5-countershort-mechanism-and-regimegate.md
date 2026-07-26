# r5-countershort-mechanism-and-regimegate

_2026-07-26 17:17 UTC_

---

# TITAN R5 — counter-short caution: mechanism audit + regime recalibration

**2026-07-26 · READ-ONLY. Nothing applied.** Tree clean, HEAD `93c20c3`.
Paper mode. Part 2 is a proposal with a diff; it is NOT in the working tree.

---

## PART 1 — Is the soft-caution mechanism working at all?

**Verdict: the CHANNEL is proven EFFECTIVE. The DECISION EFFECT is UNMEASURABLE — by construction,
not by lack of data. Build R2/R4, but build them differently (§1.5).**

The audit said "we cannot prove the caution changed a single decision" from skip rates alone
(100% cohort vs 98.2% control, n=38). That was the right conclusion from the wrong instrument.
`trades.ai_user_prompt` stores the **exact string sent to Claude** (`main.py:1478`) and
`trades.ai_reason` stores what came back, so the question is directly answerable.

### 1.1 Does the caution physically reach the advisor? YES — 38/38, zero leakage either way

```
rows with a stored advisor payload            : 2685
payloads CONTAINING the caution               : 38     (2026-07-06 09:15 .. 2026-07-26 10:55)
caution-eligible advisor decisions since go-live: 38
  of which payload stored                     : 38
  of which caution PRESENT                    : 38
eligible by DB but caution ABSENT from payload : 0      <- no false negatives
caution injected but NOT DB-eligible           : 0      <- no false positives
```
The runtime condition (`_vs` snapshot) and the stored columns agree perfectly. The injection is
not theoretical.

### 1.2 A real example, verbatim from the payload tail

`trades.id=18631`, 2026-07-26 10:55:06, `status=ai_skipped`, `decision=skip`, `conf=0.92`:
```
⚠️ STATISTICAL CAUTION (counter-trend short, flat 1h): this is a SHORT while the 1h EMA is
Bullish and 1h ADX < 22 (no established trend). Historically this exact cohort has NEGATIVE
expected drift: -0.49%/12h, only 12% of cases positive (n=143), persistent at
-0.26/-0.49/-0.35% over 4h/12h/24h. Treat as a strong headwind and require clear independent
confirmation (fresh 5m structure break, real order-book support) before deciding 'execute'.
Advisory only — you may still execute if the setup is genuinely strong.

The 3 timeframes are aligned (confluence has already passed). Decide whether the bot should
execute the DCA entry now.
```
Advisor's returned reason:
> *1h BULL + 1h ADX 13.5 (weak) opposes SHORT. Massive ask wall ×5.9 above entry blocks upside.
> MTF alignment 0/4. **Statistical headwind -0.49%/12h**. Skip.*

### 1.3 Did the reasoning reference the caution? YES — overwhelmingly

The figures `-0.49`, `n=143`, `12%` exist **nowhere else** in the payload, so a reason containing
them can only have come from the injected line. Caution rows (n=38) vs non-caution SHORT advisor
decisions in the same era (n=442):

| marker in `ai_reason` | caution rows | control rows | Fisher p |
|---|---|---|---|
| `0.49` | **31/38** | 1/442 | 1.0e-12 |
| `n=143` | 2/38 | 0/442 | 6.1e-03 |
| "statistical" / "headwind" | **25/38** | 1/442 | 2.5e-13 |
| "12%" | 5/38 | 1/442 | 1.4e-05 |
| **ANY caution-specific marker** | **33/38 (87%)** | **4/442 (0.9%)** | **6.0e-14** |

The model reads the line, ingests the statistic, and quotes it back in its justification in 87% of
cases. **The soft-caution transport and uptake are proven.**

### 1.4 So why is the decision effect still unmeasurable?

Because **every one of the 38 was already overdetermined.** Read the reasons above: each one lists
independently sufficient grounds — "1h/4h BULL regime opposes SHORT", "MTF alignment 0/4", "massive
ask wall ×7.3 blocks the move", "weak volume 0.51x". **There is not one case in 38 where the
caution was the only negative.** The cohort definition (SHORT into a Bullish 1h EMA with ADX<22)
*guarantees* the advisor already sees a counter-trend setup in a flat market — the caution restates
in prose what the payload already states in numbers.

Supporting non-evidence, reported so it is not mistaken for evidence:
```
executed among caution rows : 0 / 38
executed among control rows : 8 / 442
skip confidence  CAUTION n=38 mean 0.917 median 0.920 (min 0.88 max 0.92)
                 CONTROL n=434 mean 0.874 median 0.920 (min 0.78 max 0.92)
```
The 0/38 vs 8/442 gap is confounded — the caution cohort is also the worst-setup cohort, so the
difference cannot be attributed to the caution. Confidence is near-saturated at 0.92 with identical
medians; the mean gap is not informative.

### 1.5 What this means for R2 and R4 — build them, but change the design

* **Plumbing: green.** Injected statistics reach the model and are demonstrably used in its
  reasoning. There is no reason to doubt R2 (prior-move bucket) or R4 (vol_ratio_5m ceiling) will
  be read.
* **Measurement: red under the current design.** A caution that only fires when the setup is
  already hopeless can never be shown to change anything. R2 and R4 must be able to fire on
  setups that are NOT overdetermined — the vol5m ceiling in particular fires on TREND shorts that
  otherwise look fine, so it has a real chance of being measurable.
* **Concrete proposal — make the next caution A/B by construction.** Inject on a deterministic
  half of eligible signals (e.g. `trades_row_id % 2 == 0`) and record the arm in a column. Two
  weeks of that gives a clean counterfactual instead of another year of "we cannot tell". The cost
  is that half the eligible signals go un-cautioned; given we currently cannot measure ANY caution,
  that is a cheap price. **Recommend this before building R2/R4, not after.**

---

## PART 2 — Recalibration: gate the caution on `trend_1d != 'bull'`

### 2.1 The justification — drift split by daily regime

Convention: `drift_pct` **positive = the SKIPPED short would have won** (the veto cost us);
negative = the veto was correct. Cohort throughout: `ai_skipped` SHORT, `ema_status_1h='Bullish'`,
`srv_adx_1h < 22`.

| slice | 4h | 12h | 24h |
|---|---|---|---|
| **A · full history, `trend_1d = bull`** | +0.165% n=15 (60% pos, t=+2.0) | **+0.631% n=15 (67% pos, t=+2.0)** | +0.646% n=15 (40% pos, t=+1.3) |
| **B · full history, `trend_1d != bull`** | -0.100% n=147 (44% pos, t=-1.9) | **-0.116% n=138 (26% pos)** | +0.104% n=136 (43% pos) |
| **C · the original study window (pre-06-27)** | -0.150% n=93 (48% pos, t=-2.2) | **-0.310% n=93 (17% pos, t=-2.4)** | -0.223% n=93 (39% pos) |
| D · post-go-live, `trend_1d = bull` | +0.165% n=15 | +0.631% n=15 | +0.646% n=15 |
| E · post-go-live, `trend_1d != bull` | -0.012% n=54 | +0.286% n=45 (t=+1.7) | +0.810% n=43 (t=+4.5) |

**The premise checks out.** The -0.49%/12h study was measured in a tape that contained **zero** bull
days — its 93 drift-complete skips were `trend_1d` bear (61) and neutral (32). `trend_1d='bull'`
did not exist in Titan's history until 2026-07-10. Post-go-live composition: bear 31 / neutral 23 /
**bull 15**. The bull slice is exactly the new material, and it is exactly where the sign flipped.

### 2.2 Two honest qualifications

1. **n=15 for the bull slice, and it is not internally consistent.** 12h is coherent (mean +0.631,
   median +0.895, 67% positive). 24h is not — mean +0.646 but **median -0.546** with only 40%
   positive, i.e. the 24h mean is carried by a few large outliers. The case for the gate rests on
   the 4h/12h horizons, not 24h.
2. **The gate is an improvement, not a restoration.** Slice E shows the *non-bull* cohort has also
   stopped being reliably negative since go-live (+0.286%/12h, +0.810%/24h t=+4.5). Gating on
   `trend_1d` removes the worst slice but does not bring the remainder back to the original
   -0.310%/12h. If the Boss wants the caution to be *right* again rather than merely *less wrong*,
   the honest next step is re-deriving the whole cohort definition on post-06-27 data — not this
   one-line gate. **This diff buys time; it is not a re-validation.**

### 2.3 Effect of the gate on what already happened

```
injected with trend_1d=neutral  n=23
injected with trend_1d=bull     n=15   <- suppressed by the gate (2026-07-11 .. 07-19)
=> removes 15 of 38 injections (39%), keeps 23
```

### 2.4 Runtime pre-check — is `trend_1d` even available to the advisor?

Yes. Verified against the 38 stored payloads:
```
payloads with a correct 1d trend line : 38/38
'n/a' cases                           : 0
mismatches vs trades.trend_1d         : 0
```
Example (`id=18631`, DB `trend_1d=neutral`):
```
  1d: NEUTRAL, ADX 17.7, EMA-gap 0.643% (Contracting)
  4h: NEUTRAL, ADX 21.5, EMA-gap 0.358% (Contracting)
  1h: BULL,    ADX 13.5, EMA-gap 0.096% (Expanding)
```
`_vs.get('trend_1d')` is the same source that renders that line, so the gate will bind.

### 2.5 The diff (proposal — NOT applied)

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

### 2.6 Scope — it touches nothing else

One file, `claude_advisor.py`. **Three lines of actual code**, the rest is comment:
```
+    _ct_d1 = (_vs.get('trend_1d') or '').lower()
-            and isinstance(_ct_adx, (int, float)) and _ct_adx < 22):
+            and isinstance(_ct_adx, (int, float)) and _ct_adx < 22
+            and _ct_d1 != 'bull'):
```
* `grep -c _ct_d1 claude_advisor.py` -> **0** in the current file: no name collision.
* `STATISTICAL CAUTION` appears at exactly **one** site (line 305) — the block being gated.
* `consult_for_entry` has two callers (`main.py:1934`, `main.py:3145`); the patch changes neither,
  and the function's signature, return value and every other prompt section are untouched.
* **NOT touched:** the entry gate, the FLAT score floor, the HTF cascade, the confluence matrix,
  the recheck (R1, shipped as `93c20c3`), wall-trail (still `False`), breakeven/trail, SL logic,
  any sensor, and the SOL bot. No DB schema change. No behaviour change for LONGs, for ADX>=22,
  or for any non-bull daily regime.
* `py_compile` OK · `patch -p1 --dry-run` CLEAN · working tree still clean at `93c20c3`
  (`md5 claude_advisor.py = eec8b748face756419050da8e2b4b0bc`, unchanged).

### 2.7 Snapshot / apply / rollback

**Snapshot first:**
```bash
cd /root && git tag pre-countershort-regimegate-20260726
cp claude_advisor.py claude_advisor.py.bak_regimegate_20260726
```
**Apply** (save §2.5 as `R5.patch`):
```bash
cd /root/titan-bot
patch -p1 < R5.patch
python3 -m py_compile claude_advisor.py
sudo systemctl restart titan.service
```
**Rollback** — any of the three:
```bash
git checkout pre-countershort-regimegate-20260726 -- titan-bot/claude_advisor.py
cd /root/titan-bot && cp claude_advisor.py.bak_regimegate_20260726 claude_advisor.py
cd /root/titan-bot && patch -R -p1 < R5.patch
sudo systemctl restart titan.service
```
Verification after apply: the next eligible SHORT with `trend_1d='bull'` must produce a payload
**without** the `STATISTICAL CAUTION` block —
`SELECT id, trend_1d, ai_user_prompt LIKE '%STATISTICAL CAUTION%' FROM trades WHERE ...`.

---

## Decision requested

1. **Part 1** — accept the verdict (channel effective, decision effect unmeasurable) and decide
   whether to adopt the deterministic A/B arm **before** building R2/R4.
2. **Part 2** — apply the `trend_1d != 'bull'` gate as a stopgap, or hold it and re-derive the
   cohort definition properly on post-06-27 data.

Nothing applied. Tree clean at `93c20c3`; `titan.service` running the R1 fix from the previous step.
