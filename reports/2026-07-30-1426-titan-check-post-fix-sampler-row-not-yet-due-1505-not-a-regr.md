# titan-check-post-fix-sampler-row-NOT-YET-due-1505-not-a-regression

_2026-07-30 14:26 UTC_

---

# TITAN check — the post-fix sampler row HAS NOT LANDED YET. It is 14:24, the row is due 15:05:30.

_2026-07-30 14:25 UTC · HEAD `1161802` · 🔴 LIVE, REAL MONEY · vpos 87 LONG open_

---

## ANSWER IN ONE LINE

**The 15:05:30 row does not exist yet — the clock has not reached it.** `date -u` at the moment of
this check: **`Thu Jul 30 14:24:57 UTC 2026`**. The row is due at **15:05:30**, i.e. **~40 minutes
from now**. There is nothing to judge, and nothing to paste.

🔴 **This is NOT the regression I flagged in advance.** That test is specific: *a row written AFTER the
14:10:59 restart that carries `adx_window` NULL.* **No row has been written since the restart at all.**
The newest row (246) predates it by five minutes.

---

## 1 · SAMPLER ROWS — the query, verbatim, and its output

```sql
SELECT id, ts, adx_1h, adx_15m, adx_5m, adx_window
FROM smart_exit_dryrun_samples WHERE vpos_id=87 ORDER BY id DESC LIMIT 3;
```

```
id   ts                                adx_1h  adx_15m  adx_5m  adx_window
---  --------------------------------  ------  -------  ------  ----------
246  2026-07-30T14:05:31.968691+00:00  17.96   46.18    32.3
245  2026-07-30T13:05:31.028782+00:00  22.3    49.56    48.66
244  2026-07-30T12:05:26.571802+00:00  25.35   46.84    45.88
```

**All three are PRE-FIX rows, and `adx_window` is empty on all three because the old code wrote them.**
Row 246 landed at **14:05:31.97**, and the restart was at **14:10:59** — **5 min 27 s later.** The
patch was not running when any of those rows was written.

**The due time, from the throttle's own arithmetic so it is checkable rather than asserted:**

```
throttle : elapsed - MAX(elapsed_s) >= SMART_EXIT_DRYRUN_SAMPLE_SEC   (config.py:442 = 3600)
opened_at        = 2026-07-30T12:05:17.4998
MAX(elapsed_s)   = 7212.7          (row 246)
next fire        = 12:05:17.4998 + 7212.7 + 3600  =  15:05:30 UTC
now              = 14:24:57 UTC    ->  2,433 s short
```

---

## 2 · THE EXIT CONSULT — also has not happened; nothing to paste verbatim

```
id     timestamp            ai_decision  ai_confidence
-----  -------------------  -----------  -------------
19740  2026-07-30 14:05:36  hold         0.62
19737  2026-07-30 14:00:26  hold         0.62
```

**The newest consult is 19740 at 14:05:36 — pre-restart, on the pre-fix prompt.** The next hourly
consult is due **~15:05:36**, seconds after the sampler row it reads.

🔴 **So I cannot tell you whether the NOTE is gone, and I am not going to reconstruct a block that
does not exist.** The `regime_now` string is built at consult time from the **latest sampler row**;
until row 247 exists there is no post-fix block. What I can state is the mechanism and the two
possible outcomes, both already committed to in advance:

- If row 247 carries **`adx_window = 200`** → both sides sit on `CANDLE_LIMIT`, `_comparable` is True,
  **the NOTE is omitted** and `regime_now` prints the converged figures plainly.
- If row 247 carries **NULL** → the NOTE stays, **and that is the regression**, because a post-restart
  row must carry the window.

**The last block I DID capture is from 14:24 against the current (pre-fix, `adx_window` NULL) row, and
it is a live rendering, not a mock** — it is what the prompt looks like today, and it is exactly the
"refusal" half of the guard doing its job:

```
regime_entry: regime=TREND 1d=neutral 4h=bull 1h=bull ADX1h=13.5
regime_now  : 15m=bull 5m=neutral ADX1h=22.3 ADX15m=49.6
  🔴 NOTE: the two ADX figures above were computed on DIFFERENT candle windows — the
  'At entry' value on 200 candles and the 'Now' value on an unrecorded window. ADX(14)
  is doubly smoothed and reads far higher on a short window, so these are NOT two
  observations of one quantity: NO rise or fall between them may be inferred. Judge the
  'Now' figure on its own, or ignore it.
```

*(Captured earlier today against a COPY of `trades.db`, on the real vpos 87 row, with the real
pre-fix sample. Stated as provenance so it is not mistaken for the 15:05 consult.)*

---

## 3 · IS `adx_window` NULL ON THE NEW ROW?

**There is no new row.** The question cannot be answered yet, and the honest answer is that — not a
substitute for it.

**Restating the commitment so it stays falsifiable:** when row 247 lands, if `adx_window` is NULL,
**that is the regression**, I will say so in one line without explaining it away, and the next step is
to check whether the running worker actually loaded the patched `virtual_trader` rather than to
theorise about the sampler.

---

## 4 · CURRENT STATE

**vpos 87 — OPEN.**

| | |
|---|---|
| side / size | LONG 0.0023 BTC @ **64838.7** · $149 notional · 5x |
| status | **open** · `recheck_status = done` · `breakeven_applied = false` |
| last | **64728.0** |
| unrealised | **−$0.2546** gross · **−0.1367R** (`initial_risk_usdt` 1.86282508) |
| exchange uPnL, both probes | **−0.2498** (unified and raw `swapV2` agree) |
| stop | **64028.8** · `original_sl_price` identical · **+0.863R away** |
| 🔴 **exchange stop order id** | **`2082799690256592896`** — `STOP_MARKET stopPrice=64028.8 closePosition=true status=NEW`, **UNCHANGED across the restart. Not cancelled, not re-placed.** |
| exchange position id | `2082799688088776706` |
| both probes | unified `fetch_positions` **and** raw `swapV2PrivateGetUserPositions` — **1 position, 1 order, no orphans** |
| water_mark / max_adverse | 65121.0 / 64598.0 |
| balance | `free 479.9148 · used 29.8258 · total 509.7406` |

**Service health:**

| check | result |
|---|---|
| `titan.service` | **active**, since **14:10:59**, `NRestarts=0` |
| tracebacks · CRITICAL · `REFUSING TO START` · `no such column` · `OperationalError` since restart | **0** |
| circuit breaker | **untripped** (0 hits) |
| `🚨` / `MANUAL ACTION REQUIRED` | **0** |
| Mercury-SOL | **active**, untouched |
| HEAD | **`1161802`**, `git status` clean, origin in sync |

**The monitor is still running** against the live DB and will fire when row 247 appears. Its
`recheck_events` probe errors each pass with `no such column: adx_window` — **that is the expected
lazy-migration behaviour**, not a fault: the column is created the first time `log_recheck` runs, and
vpos 87 can never trigger a recheck (`recheck_status = done`). That column arrives with the **next**
position's T+10s recheck.

---

## 🔴 STANDING RULE, RECORDED — EVERY CHECK GETS A DATED FILE AND A LINK

**Operator, 2026-07-30, second occurrence — and the second is what makes it a rule rather than a
lapse:** a result that exists only in the terminal **did not happen.** §8 already said this; I treated
it as applying to reports rather than to checks, and that reading is now closed.

- **EVERY check gets a NEW dated file and a delivered raw link. However small. Including one-line
  answers. Including "nothing has changed yet".**
- §8 is **not** "when asked". The report **is** the deliverable.
- **If a check is too small to write up, write it up in three lines — but write it up.**
- Written into OPEN-ITEMS §8 and into durable memory
  (`feedback_dated_snapshot_never_reused_urls`, `feedback_full_report_all_diagnostics_to_telegram`), so
  it survives a session with no memory of today.

**Both violations today, recorded rather than smoothed over:** the 14:23 query answering *"did the row
land"* in the terminal only, and the 14:19 report's pending-item follow-up which I intended to deliver
"when the monitor fires" instead of on the check that had already happened.

---

*Titan · 2026-07-30 14:25 UTC · HEAD `1161802` · 🔴 LIVE · vpos 87 LONG open −0.1367R, stop 64028.8
unchanged · row 247 due 15:05:30, NOT YET WRITTEN · no regression observed because no post-fix row
exists yet*
