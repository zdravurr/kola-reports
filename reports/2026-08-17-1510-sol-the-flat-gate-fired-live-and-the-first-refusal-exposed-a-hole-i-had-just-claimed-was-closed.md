# Mercury-SOL — the flat gate FIRED LIVE at 14:55:15, and the first refusal exposed a hole in the claim I had just published

**2026-08-17 15:10 UTC · Mercury-SOL · 🔴 LIVE REAL MONEY · book FLAT · follow-up to the 14:50 apply. ONE further one-line fix applied, service restarted, boot clean.**

Titan (`/root/titan-bot`): **not touched, not read for state, no numbers imported.** HEAD `897850b`, clean.

Closes the ⏳ PENDING row in [14:50 §6b](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-17-1450-sol-applied-the-card-throttle-and-a-mechanical-flat-adx-gate-in-front-of-the-advisor.md).

---

## ⚡ THE SHORT VERSION

1. **🔴 THE GATE FIRED LIVE, 24 MINUTES AFTER THE RESTART.** `row=19315`, LONG, **ADX(1h,200) = 13.62 < 20.0**, status `flat_adx_blocked`, and **`ai_decision` is NULL — the advisor was never consulted.** The whole point of the placement, proven on real traffic rather than from the parse tree.
2. **The full evidence chain is intact:** the `trades` row, the `skip_attribution` row (id 11724) with the wall anchor, and **all five drift horizons already scheduled** (15m/1h/4h/12h/24h). No `TG send failed` in the journal, so the card went out.
3. **🔴 AND THE FIRST REFUSAL FOUND A HOLE IN MY OWN CLAIM.** The 14:50 report said *"a refusal is therefore reproducible from the stored row."* On the actual refused row, **`trades.srv_adx_1h` is NULL.** The number survived only as a **string** inside `error` and as a real in `skip_attribution`. The canonical column — the one the pre-registered 33.2 % rate was computed from — was empty.
4. **Cause: `srv_adx_1h` is written only on the ADVISOR path, which a refusal by construction never reaches.** So the gate's own refusals would have been invisible to the exact query that judges the gate. **That is the same defect I named in the 14:25 report about the recheck tighten** — a mechanism that does not persist its own decision — reproduced by me, in the pass that named it.
5. **Fixed: one kwarg, `srv_adx_1h=_flat_adx`.** Applied, backed up, compiled, restarted 14:58:50, boot clean, book flat.
6. **`book_blocked` has the identical hole — 0 of 30 rows carry `srv_adx_1h`.** Found while checking mine. **NOT fixed here:** out of scope, reported, its own pass.
7. **Still pending:** the fix's own live proof (the next refusal), and the card throttle's first live suppression.

---

# 1. THE LIVE REFUSAL

## 1a. The journal line

```
Aug 17 14:55:15  [MERCURY-SOL] [FLAT-ADX-GATE] REFUSE LONG row=19315 ADX(1h,200)=13.62 < 20.0
```

## 1b. The `trades` row

```
              id = 19315
       timestamp = 2026-08-17 14:55:04
          status = flat_adx_blocked
       tv_action = Bullish OB Mitigated          tv_tf = 5m
matrix_direction = LONG                          score = 5.00
       combo_key = 1H:Smart Trail Switch Bullish|15M:HyperWave Signal Up|5M:Bullish OB Mitigated
           error = flat market: 1h ADX 13.62 below the 20 floor — no trend, no trade
     ai_decision =                              🔴 NULL
        ai_model =                              🔴 NULL
       ai_reason =                              🔴 NULL
      srv_adx_1h =                              🔴 NULL  ← §2
```

🔴 **`ai_decision`, `ai_model` and `ai_reason` are all NULL, and that is the proof that matters.** The row passed the HTF cascade and the score gate (5.00), reached the point where every other entry gets a ~5 s Claude call, and **was refused before the model was asked.** The 14:50 report proved the placement from the parse tree; this row proves it from production. The advisor never got the chance to be inconsistent about this tape.

## 1c. The `skip_attribution` row — the refusal is measurable from the first one

```
                 id = 11724          trades_row_id = 19315
          direction = LONG           price_at_skip = 75.88
         srv_adx_1h = 13.6170945702587           🔴 the NUMBER, persisted
          ai_reason = flat market: 1h ADX 13.62 below the 20 floor — no trend, no trade
      market_regime = FLAT           confluence_score = 5.0
 nearest_wall_price = 75.75          wall_strength = 8.9   wall_distance_pct = 0.1713
    tracking_status = active         skip_ts = 2026-08-17T14:55:15.159037+00:00
```

And the drift schedule, written at refusal time:

| horizon | due |
|---|---|
| 15m | 2026-08-17 15:10:15 |
| 1h | 2026-08-17 15:55:15 |
| 4h | 2026-08-17 18:55:15 |
| 12h | 2026-08-18 02:55:15 |
| 24h | 2026-08-18 14:55:15 |

**The wall anchor is there because the gate was placed after the `_pre_walls` fetch** — the fourth ordering decision in 14:50 §2a, and this row is what it bought. In 24 hours this refusal will be gradeable: did price move the refused LONG's way, or not.

**No `TG send failed` / `tg failed` in the journal since the restart**, so the `📉 FLAT REFUSED ENTRY (ADX 13.62 < 20)` card was delivered.

---

# 2. 🔴 THE HOLE THE FIRST REFUSAL EXPOSED

## 2a. What I claimed, and what the row actually held

The 14:50 report, §2b, ended:

> *"A refusal is therefore reproducible from the stored row."*

That sentence was written about the **identity of the ADX** — that the gate reads the same 200-bar value the position row persists — and it is true about the identity. **But read as it stands, on the refused row, it is not true**, because the value is not in the column a later query would look in:

| where the 13.62 lives on row 19315 | form |
|---|---|
| `trades.error` | a **STRING** — `"flat market: 1h ADX 13.62 below the 20 floor…"` |
| `skip_attribution.srv_adx_1h` | a **REAL** — 13.6170945702587 ✅ |
| **`trades.srv_adx_1h`** | 🔴 **NULL** |

## 2b. Why — and why it matters more than it looks

`srv_adx_1h` on the `trades` row is written at `main.py:5020`, on the **advisor/execute path**:

```python
update_trade(row_id, ..., srv_adx_1h=_adv_snap.get('srv_adx_1h'), ...)
```

A refusal returns before that line. Measured across the whole book:

| status | rows | rows carrying `srv_adx_1h` |
|---|---|---|
| `ai_skipped` | 3,653 | **3,605** |
| `below_threshold` | 2,167 | **0** |
| `htf_blocked` | 7,340 | **0** |
| `book_blocked` | 30 | **0** |
| `flat_adx_blocked` | 1 | **0** |

🔴 **The consequence is specific and it is not cosmetic.** The pre-registered refusal rate in 14:50 §2f — 33.2 % of consultations, the number the gate is to be judged against — was computed as `select … from trades where srv_adx_1h < 20`. **Run that same query next month and the gate's own refusals will not appear in it**, because the rows it refused carry NULL there. The gate would have been invisible to the instrument that pre-registered it.

**That is precisely the defect I named four hours ago in the 14:25 report** about the recheck tighten: *"the mechanism deletes its own evidence… the DB stores the string `'tightened'` and nothing else."* I wrote that, then shipped a gate whose refusals kept their number in a log line and a sentence. **Naming a defect class does not immunise you against it.**

## 2c. The fix — one kwarg

```diff
@@ main.py, inside the flat-ADX refusal branch
+                # 🔴 2026-08-17, ADDED AFTER THE FIRST LIVE REFUSAL (row 19315).
+                # `srv_adx_1h` is otherwise written only on the ADVISOR path, which
+                # a refusal never reaches — so the first refused row landed with the
+                # ADX in the `error` STRING and in skip_attribution, but NULL in the
+                # very column the pre-registered rate was computed from
+                # (`select ... from trades where srv_adx_1h < 20`). A gate whose
+                # refusals are invisible to the query that judges it is the exact
+                # defect the 14:25 pass named in the recheck tighten. Persist the
+                # NUMBER, on the refused row, in the canonical column.
+                # (book_blocked has the same hole — 0 of 30 rows carry it — and it is
+                #  NOT fixed here: out of scope, reported, its own pass.)
                 update_trade(row_id, status='flat_adx_blocked', combo_key=combo,
                              confluence_score=direction_score,
                              matrix_direction=matrix_result['direction'],
+                             srv_adx_1h=_flat_adx,
                              error=_fa_reason)
```

`update_trade(row_id, **kwargs)` builds its `SET` clause from the kwargs, so this is one column added to one UPDATE. **Nothing else changed.** Backup: `main.py.bak_flatadx_persistadx_20260817`.

## 2d. 🔴 `book_blocked` HAS THE SAME HOLE — reported, not fixed

**0 of 30 `book_blocked` rows carry `srv_adx_1h`.** The book gate does persist its **own** six `book_gate_*` columns on every scored row — deliberately, and for exactly this reason (*"the column that would answer 'what did the book look like when we entered?' is destroyed for exactly the rows that became positions"*). So the book gate's own facts are safe; it is the **shared snapshot columns** that a refusal never receives.

**Not fixed here.** It touches a second live gate, it was not in scope, and shipping it in the same restart as its own discovery is how an unrelated regression gets attributed to the wrong change. **It is written down instead** — and the pattern is now general enough to name: *any early-return gate loses every column written downstream of it.* `below_threshold` (2,167 rows) and `htf_blocked` (7,340 rows) are the same shape, and those two are cheap rejects where it may not be worth it. That is a judgement for its own pass.

---

# 3. WHAT IS PROVEN NOW, AND WHAT IS STILL NOT

| claim | status |
|---|---|
| the gate refuses a real entry on live traffic | ✅ **LIVE-PROVEN** — row 19315, 14:55:15 |
| the advisor is never consulted on a refusal | ✅ **LIVE-PROVEN** — `ai_decision`/`ai_model`/`ai_reason` all NULL |
| the refusal is drift-measurable from the first one | ✅ **LIVE-PROVEN** — `skip_attribution` 11724 + 5 horizons scheduled |
| the card is delivered | ✅ **LIVE-PROVEN** — no `TG send failed` in the journal |
| `srv_adx_1h` persisted on a refused row | ⏳ **fix applied 14:58; awaits the NEXT refusal** |
| the card throttle suppressing a real duplicate | ⏳ **PENDING** — needs a repeated skip inside 30 min |
| the recheck tighten falling toward zero (14:50 §2g) | ⏳ **PENDING** — needs live entries |

Traffic since the second restart has been four rows, all `htf_blocked` (SHORT/NEUTRAL, scores −5.0 to −7.5) — rejected by the HTF cascade **upstream** of the gate, so the gate has had no candidate to judge yet. **The one query to run next:**

```sql
select id, timestamp, matrix_direction, round(srv_adx_1h,4), error
  from trades where status='flat_adx_blocked' order by id;
```

Row 19315 will keep its NULL — it was refused before the fix and **is not backfilled**, because a backfilled number is the habit that produced the 42-bar/200-bar column collision this bot spent 2026-08-07 unpicking. **The NULL is honestly "unrecorded".** Row 2 onward will carry the number.

---

## STATE

```
mercury-sol   active - MainPID 3640449 / worker 3640686 - since 2026-08-17 14:58:50 UTC
              NRestarts=0 - restarted twice today on a FLAT book - boot clean, 0 tracebacks
              [BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ARM=0.75R
                     PARTIAL=OFF ATR_TF=1h OBSERVATION_MODE=False [pid 3640686]
APPLIED 14:31 AI_SKIP_CARD_THROTTLE_S=1800 - FLAT_ADX_GATE_ENABLED=True/DRYRUN=False
              skip_attribution.TRACKED_STATUSES += 'flat_adx_blocked'
APPLIED 14:58 srv_adx_1h persisted on the refused row (one kwarg)
BACKUPS       *.bak_cardthrottle_flatadx_20260817 (3 files) + main.py.bak_flatadx_persistadx_20260817
FIRST REFUSAL row 19315, 14:55:04, LONG, ADX 13.62, advisor NOT consulted
              skip_attribution 11724 - 5 drift horizons scheduled - card delivered
UNCHANGED     SL_BUFFER_ATR 2.5 - _STATE_VERDICT_TTL_S 60.0 - POST_ENTRY_RECHECK_ENABLED True
              ADX_BELOW_FLOOR 20.0 (reused) - ADX_FLAT_FLOOR 20.0 (still reported, still not fixed)
BOOK          31 closed - SumR -7.967 - FLAT, zero open
              stopping rule: 2 of 20 live closes - THE COUNT STANDS, neither change moves 1R
titan         /root/titan-bot - NOT touched, NOT read for state, NO numbers imported. HEAD 897850b
```

**Provenance: the journal line from `journalctl -u mercury-sol`; rows 19315 and `skip_attribution` 11724 read under `mode=ro`; the per-status `srv_adx_1h` census from one GROUP BY over `trades`; the diff quoted from the file as it now stands. Titan was not read.**
