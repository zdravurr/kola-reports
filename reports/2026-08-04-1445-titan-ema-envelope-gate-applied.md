# EMA ENVELOPE ENTRY GATE — APPLIED LIVE. AND THE BOOLEAN IN THE BRIEF WAS INVERTED.

**2026-08-04 14:45 UTC · Titan LIVE, real money · applied at 14:41:20 with 0 open positions**
**Config `EMA_ENVELOPE_GATE_ENABLED = True` · kill switch is one flag · `py_compile` clean**

Basis: `reports/2026-08-04-1425-titan-asymmetric-entry-measured.md` §6b.
Canon updated in the same commit: **OPEN-ITEMS §2.47** (applied) alongside §2.45c (the correction
that unblocked it). Dated snapshot: `reports/2026-08-04-1445-open-items.md`.

---

## 🔴 0. READ THIS FIRST — THE RULE AS WRITTEN AND THE RULE AS MEASURED ARE DIFFERENT RULES

The brief states:

> refuse the entry when `ema_gap_dir_1h != 'Expanding'` **AND** `ema_gap_dir_15m != 'Expanding'`

**Every number in the same brief describes the other boolean.** "Refuses 59 % of the book (35 of
59)", "refuses vpos 86, 91 and 92", "turns the live era from −1.89R to +0.35R", "PASS·LONG −1.91R,
n=12" — all of those are the **strong form**: *admit only when both are Expanding.* By De Morgan its
refusal condition is an **OR**, not an AND.

**Measured, both readings, same 30-day window and same book:**

| | refuses of the 59-entry book | refuses of LONG signals (30 d) | refuses of SHORT signals (30 d) | refuses of the 7 live entries |
|---|---|---|---|---|
| **strong form** — admit iff both Expanding (**IMPLEMENTED**) | **35 of 59 (59 %)** ✔ matches the brief | 576 / 681 = **84.6 %** | 607 / 774 = **78.4 %** | **3** (vpos 86, 91, 92) ✔ matches the brief |
| literal wording — refuse iff *both* non-Expanding | 15 of 59 (25 %) | 222 / 681 = 32.6 % | 249 / 774 = 32.2 % | **0** — all 7 live entries are 1h `Expanding` |

**The literal wording would have shipped an inert gate** — zero effect on every trade the decision was
made about. **I implemented the strong form, which is what every quantity you cited describes.** The
boolean is written out in `config.py` and in OPEN-ITEMS §2.47 in both directions so it cannot drift
back. **If you did mean the literal AND form, it is a two-character change (`all` → `any`) — say so
and I will flip it; the numbers above are what you would be choosing.**

---

## 1. THE RULE, AS IT NOW RUNS

```
ADMIT  ⇔  ema_gap_dir_1h == 'Expanding' AND ema_gap_dir_15m == 'Expanding'
REFUSE ⇔  ema_gap_dir_1h != 'Expanding' OR  ema_gap_dir_15m != 'Expanding'
```

- **Direction, not width** — width quartiles are non-monotone (forensics §4d).
- **Symmetric across sides** — the LONG/SHORT asymmetry is **p = 0.189** on the §0-clean cohort and is
  not established (§2.46), so there is no side-specific term anywhere in the code.
- **Placement: after the HTF cascade, before the score gate, on ALL THREE entry paths.**
- **Missing reading ⇒ ADMIT** (`EMA_ENVELOPE_FAIL_OPEN = True`), logged as `[EMA-ENV] FAIL-OPEN`.
  Refusing on absence would turn an indicator outage into a silent total trading halt. Measured
  frequency of that path over the last 30 days: **0 rows**.

## 2. THE DIFF, AS APPLIED

**`config.py` — the flag, and the reasoning that travels with it** (46 lines, 4 of them code):

```python
# ═══ EMA ENVELOPE ENTRY GATE — operator decision 2026-08-04, applied KNOWINGLY ═══
# THE RULE: admit an entry only when the EMA9/EMA21 gap is EXPANDING on BOTH
# the 1h AND the 15m timeframe. Refuse otherwise. Direction, not width — width
# quartiles are non-monotone (forensics §4d). SYMMETRIC across sides: the
# LONG/SHORT asymmetry is p=0.189 on the §0-clean cohort and is NOT established
# (see OPEN-ITEMS §2.46), so no side-specific term exists here.
#
# 🔴 THE BOOLEAN, WRITTEN OUT, BECAUSE THE BRIEF STATED IT THE OTHER WAY:
#   ADMIT  ⇔  dir_1h == 'Expanding' AND dir_15m == 'Expanding'
#   REFUSE ⇔  dir_1h != 'Expanding' OR  dir_15m != 'Expanding'
# ... (evidence + all six weaknesses + review point recorded in full) ...
EMA_ENVELOPE_GATE_ENABLED  = True          # kill switch: False = never evaluated
EMA_ENVELOPE_TFS           = ('1h', '15m')  # every listed TF must agree
EMA_ENVELOPE_REQUIRED_DIR  = 'Expanding'
EMA_ENVELOPE_FAIL_OPEN     = True          # missing reading ⇒ admit (see above)
```

**`main.py` — the gate itself**, contract-identical to `_htf_cascade_gate` (returns `None` to pass, a
finished response to refuse):

```python
def _ema_envelope_gate(parsed, symbol, side, intent, direction, matrix_result,
                       combo=None):
    if not EMA_ENVELOPE_GATE_ENABLED:
        return None
    snap = _request_snapshot() or {}
    dirs = {tf: snap.get(f'ema_gap_dir_{tf}') for tf in EMA_ENVELOPE_TFS}
    missing = [tf for tf, v in dirs.items() if not v]
    if missing:
        # Enrichment failure, not a market state. Admitting keeps an indicator
        # outage from becoming a silent trading halt; the log line makes the
        # fail-open path countable rather than invisible.
        print(f"[TITAN][EMA-ENV] FAIL-OPEN admit {direction} {symbol} "
              f"missing={missing} have={dirs} fail_open={EMA_ENVELOPE_FAIL_OPEN}", flush=True)
        if EMA_ENVELOPE_FAIL_OPEN:
            return None
    elif all(v == EMA_ENVELOPE_REQUIRED_DIR for v in dirs.values()):
        print(f"[TITAN][EMA-ENV] PASS {direction} {symbol} "
              + " ".join(f"{tf}={v}" for tf, v in dirs.items()), flush=True)
        return None

    # ---- refuse ----
    _decid = " · ".join(f"{tf} {dirs.get(tf) or 'n/a'}" for tf in EMA_ENVELOPE_TFS)
    print(f"[TITAN][EMA-ENV] BLOCK {direction} {symbol} {_decid} "
          f"(need {EMA_ENVELOPE_REQUIRED_DIR} on all)", flush=True)
    row_id = insert_signal(parsed, symbol, side, intent,
                           status='ema_envelope_blocked')
    if row_id:
        # matrix_direction + breakdown only. `confluence_score` is deliberately
        # NOT written: that column already holds four different quantities
        # depending on branch (OPEN-ITEMS §0) and this gate is not a score gate —
        # adding a fifth meaning would corrupt every cross-status comparison.
        update_signal_execution(
            row_id, combo_key=combo,
            matrix_direction=matrix_result.get('direction'),
            matrix_breakdown_json=json.dumps(matrix_result.get('breakdown', {})),
        )

    def _eglyph(v):
        return {'Expanding': '✅', 'Contracting': '🔻', 'Flat': '➖'}.get(v, '❔')

    _all_tfs = ('1d', '4h', '1h', '15m', '5m')
    _ctx = " · ".join(
        f"{tf} {_eglyph(snap.get(f'ema_gap_dir_{tf}'))}"
        f"{snap.get(f'ema_gap_dir_{tf}') or 'n/a'}"
        f"{'*' if tf in EMA_ENVELOPE_TFS else ''}"
        for tf in _all_tfs)
    send_tg(
        f"🚫 <b>BLOCKED — EMA envelope (flat market)</b>\n"
        f"{dxy_tag()}\n"
        f"🎯 Trigger: {direction}\n"
        f"📏 EMA9/21 gap: {_ctx}\n"
        f"🔒 Gate: needs <b>{EMA_ENVELOPE_REQUIRED_DIR}</b> on "
        f"<b>{' AND '.join(EMA_ENVELOPE_TFS)}</b> (*) — got {_decid}\n"
        f"ℹ️ Matrix net: {matrix_result.get('direction', '?')} "
        f"{matrix_result.get('score', 0.0):.2f}/10 — the score gate was never reached\n"
        f"<i>applied 2026-08-04: n=40 clean, Δ+0.699R, p=0.029, fails Bonferroni; "
        f"review at 20 executed entries per side</i>"
        + (f"\n<code>{combo}</code>" if combo else "")
    )
    payload = {
        "status": "ema_envelope_blocked",
        "direction": direction,
        "required_dir": EMA_ENVELOPE_REQUIRED_DIR,
        "ema_gap_dirs": dirs,
    }
    if combo is not None:
        payload['combo'] = combo
    return jsonify(payload), 200
```

**And the three call sites — identical shape, one per entry path:**

```diff
     if htf_block is not None:
         return htf_block
+    # EMA envelope gate (2026-08-04): BEFORE the score gate, AFTER the cascade.
+    # Returns None on pass, a finished response on refusal. Reads the snapshot
+    # the webhook already computed — no fetch on the entry path.
+    _env_block = _ema_envelope_gate(parsed, symbol, side, intent, direction,
+                                    matrix_result, combo=combo)
+    if _env_block is not None:
+        return _env_block
     direction_score = signal_matrix.score_for_direction(matrix_result, direction)
```

`main.py:2037` (`_handle_5m_trigger`) · `main.py:3911` (`_handle_state_machine`) ·
`main.py:4471` (direct-webhook P3, no `combo` on that path — the gate handles `combo=None`).

**Total: 156 insertions, 0 deletions, 0 modified lines. Nothing was removed or rewritten.**

### 🔴 Why THREE call sites and not one — checked, not assumed

`_execute_entry` — the only function that can open a position — has exactly **three** live call sites
(`main.py:2333`, `:4255`, and the shared P3 tail below `:4471`), and a fourth that was **already
neutered** by §2.43 (the legacy fall-through now returns `unrecognised_payload_refused` before any
order). Each live path was verified to run the cascade → *(new gate)* → score gate in that order.
**A gate installed on one path and not the others is the exact defect class this book keeps
recording; it is not repeated here.**

## 3. PRE-REGISTERED BEFORE THE RESTART (measured 14:35, applied 14:41)

| quantity | value |
|---|---|
| **refusal rate per side**, signals reaching the gate, last 30 days | **LONG 576 / 681 = 84.6 %** · **SHORT 607 / 774 = 78.4 %** |
| **entries/day after** | **0.90 → 0.47** (14 of the last 27 entries survive: LONG 8 · SHORT 6) |
| **of the last 25 entries it refuses 12** | vpos **70** (−0.31), **73** (−0.48), **74** (−0.59), **75** (−0.11), **77** (−1.09), **80** (−1.09), **83** (−1.09), **84** (+0.12), **85** (−1.09), **86** (−1.02), **91** (−0.48), **92** (−0.73) |
| net effect on those 25 | **−7.95R refused · +0.30R kept** |
| fail-open path frequency, last 30 days | **0 rows** — both legs present on every signal |
| **review point** | **20 executed entries PER SIDE**, not calendar time, counted from **2026-08-04 14:41 UTC** |

At 0.47 entries/day split across two sides, 20 per side is **roughly three months** — materially
slower than the six weeks §2.46 estimated at the old rate. **That is a cost of the rule and it is
stated, not buried:** the gate that may improve the edge also lengthens the time needed to prove it.

## 4. THE WEAKNESSES — RECORDED FIRST, UNSOFTENED

Verbatim from the decision, because a rule applied over its own objections must carry them:

1. **Best of ~12 cells; p = 0.029 fails Bonferroni** at α ≈ 0.004.
2. **34 of the 40 clean observations are paper at 68× the live notional.**
3. **Refuses 59 % of the book** (35 of 59); entry rate 0.90/day → ~0.47/day.
4. **The LONG side still loses under it** — PASS·LONG **−1.91R** (n=12). It rescues the short side
   (PASS·SHORT **+9.45R**, n=12, win 75 %). **It is not a fix for longs and must not be described as
   one.**
5. **Live-era evidence is n=7 with 3 refusals. A direction, not a proof.**
6. **§0 carry:** EMA reads the **forming** candle on every timeframe by design. The gate therefore
   decides on a live, still-moving bar — the same value the historical rows were scored on, so the
   replay is consistent, but it is not a closed-bar signal.

## 5. FREEZE / SCOPE — VERIFIED, NOT ASSERTED

**Entry side only.** Not touched: the HTF cascade (`HTF_CASCADE_ENABLED`, `HTF_TOLERATE_NEUTRAL`,
`HTF_NEUTRAL_REQUIRE_15M_AGREE` all still `True` by runtime import), the FLAT floor and score bars
(`CONFLUENCE_SCORE_THRESHOLD 3.0` / `CONFLUENCE_FLAT_THRESHOLD 5.0`, unchanged by import), Variant-B,
the risk gates, **either advisor prompt** (`claude_advisor.py` byte-identical — not in the diff), and
**anything on the exit side** (§2.4 still frozen at 5 of 10).

- The diff touches **exactly two files**: `config.py` (+46) and `main.py` (+110). Nothing else.
- **No existing line was modified or deleted** — every change is an insertion.
- **No stored value changed meaning.** The new status is a new value in an existing free-text column;
  `confluence_score` is deliberately left unwritten on refused rows.
- **New status vs existing consumers, checked:** `skip_attribution.TRACKED_STATUSES` is
  `('ai_skipped','below_threshold','htf_blocked')` — it ignores the new status by construction;
  `optimizer.py` pairs positions on `status='executed'` only, so a refused row cannot be mistaken for
  a fill; `virtual_trader`, `signal_weights` and `market_context` all filter on `'executed'`.
  **No consumer treats "unknown status" as a trade.**
- `python3 -m py_compile main.py config.py` clean.
- Backups: `main.py.bak_emaenv_20260804`, `config.py.bak_emaenv_20260804`.

## 6. APPLIED FROM FLAT, AND LOADED

| step | evidence |
|---|---|
| flat before touching anything | `virtual_positions` open rows = **0** (asserted in the restart command; it would have aborted otherwise) |
| files written | `config.py` 14:37:42 · `main.py` 14:39:26 |
| restart | `titan.service` **14:41:20**, `active`; worker PID started **14:41:30** — after every edit |
| LIVE banner clean | `LIVE_TRADING_ENABLED = True` · `ORDER_ADAPTER_LIVE = True` · $30 × 5 = $150 |
| flags loaded, by import | `EMA_ENVELOPE_GATE_ENABLED=True` · `TFS=('1h','15m')` · `REQUIRED_DIR='Expanding'` · `FAIL_OPEN=True` |

## 7. LIVE — THE PASS PATH IS PROVEN END TO END. THE BLOCK PATH IS NOT YET.

**First live evaluation: 14:45:15 UTC, four minutes after the restart.** A real SHORT signal arrived,
the HTF cascade tolerated it (1H NEUTRAL · 15m SHORT · 5m SHORT), and the new gate evaluated it:

```
14:45:14  HTF_WOULD_PASS (tolerate-NEUTRAL) SHORT 1H=NEUTRAL 15m=SHORT 5m=SHORT
14:45:15  [TITAN][EMA-ENV] PASS SHORT BTC/USDT:USDT 1h=Expanding 15m=Expanding
14:45:23  weighted_adj P2: dir=SHORT raw=7.50 → advisor → status='ai_skipped'
```

**The whole chain is confirmed in the right order:** cascade → **EMA envelope** → score gate →
advisor. The signal passed the envelope on merit (both legs `Expanding`), reached the score gate with
raw 7.50, and was then skipped by the advisor. **No order was placed; `virtual_positions` still holds
0 open rows.**

🔴 **The BLOCK path has NOT been seen in flight.** Both legs have been `Expanding` on every signal
since the restart, so no refusal has occurred yet — the gate has had nothing to decline. **Status:
PASS path live-proven; refusal path applied and loaded but not live-exercised.** A watcher is armed
on the journal for the first `[EMA-ENV] BLOCK` (and for `FAIL-OPEN`, which has never fired).

Two things will be verified on that first refusal and reported either way:

1. **That the refused row really carries the gap directions** — `insert_signal` merges the snapshot
   and comparable rows are 705/705 populated, but **this status has never been written before**, so
   it is an assumption until a row exists.
2. **That the card renders what the gate decided**, not a reconstruction.

**Kill switch:** `EMA_ENVELOPE_GATE_ENABLED = False` in `config.py`, restart. One flag; no path is
left half-armed by flipping it.
