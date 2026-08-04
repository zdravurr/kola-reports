# THE CARD IS MUTED, THE LEDGER IS LIVE — AND THE DRIFT CLOCK RUNS ON ARRIVALS, NOT DAYS

**2026-08-04 19:55 UTC · Titan LIVE, real money · APPLIED `b9081ad` at 19:48:47 from flat ·
first digest delivered, `message_id` 28360**

Canon: **§2.56a–c**, plus a correction written into **§2.47**. Snapshot:
`reports/2026-08-04-1955-open-items.md`.

---

## 1. APPLIED — BOTH PARTS, FROM FLAT

**Flat was verified against the exchange before the restart, not assumed:** `fetch_positions` → **0
open positions**, `fetch_open_orders` → **0 orders**. (The 6 `virtual_positions` rows that are not
`closed` are May rows with status `archived_pre_geometry_fix` and a `closed_at` — historical, not
open.) Snapshot of both files is the git commit itself; the tree was clean at `946fe74`.

**Part A — `titan-bot/silence_digest.py`**, a standalone cron script, `05 8 * * *`, **1 message/day**.
Deliberately *not* a change inside `main.py`: the live entry path is untouched at every point, so a
defect in the ledger can make a report wrong but **can never refuse or admit a trade.**

**Part B — `EMA_ENVELOPE_REFUSAL_CARD = False`.** The card is **muted, not missing** — its delivery
was proven by execution at 19:16:33 (`message_id` 28353). The `trades` row, the `skip_attribution`
anchor and the `[EMA-ENV]` log line all sit **outside** the `if`, so refusals remain fully countable
with the card off.

```
py_compile: OK (main.py, config.py, silence_digest.py)
```

### Runtime confirmation — four ways, none of them "I read the file"

| # | check | result |
|---|---|---|
| 1 | `main.py:508` imports `EMA_ENVELOPE_REFUSAL_CARD` inside `from config import (…)` — a worker running an old `config.py` **could not have started** | **0** import errors in the journal since 19:48:40 |
| 2 | file mtimes must **predate** the process | both files `19:48:00`, worker started `19:48:47` |
| 3 | value on a fresh import | `EMA_ENVELOPE_REFUSAL_CARD = False` |
| 4 | the process is really serving | `/health` → **HTTP 200** |

Untouched and re-read at runtime: `EMA_ENVELOPE_GATE_ENABLED=True`, `SL_ATR_MULT=2.25`,
`TRAIL_MULT_ATR=1.6875`, `LIVE_TRADING_ENABLED=True`, `ORDER_ADAPTER_LIVE=True`. Nothing in scope's
exclusion list was modified: not the gate's threshold or predicate, not the cascade, not the FLAT
floor, not Variant-B, not the score bars, not the 17:01:29 geometry, not the risk gates, neither
advisor prompt, not the exit side.

**The first digest was run manually so it lands today rather than tomorrow morning:**

```
[SILENCE-DIGEST] sent=True http=200 msg_id=28360
```

---

## 2. 🔴 §2.47's CLOCK CORRECTED — IT RUNS ON ARRIVALS, AND THE CALENDAR COLUMN WAS WRONG BY 2.6×

> **Section-number note:** this was referred to as "the §2.53 trigger". The trigger table and the
> pre-committed triggers live in **§2.47**; §2.53 is the applied geometry. The correction is written
> where the number actually lives, so it is findable from the number.

The old column assumed **51.3 signals/day** reaching the gate. **Measured: 4 arrivals in 5.16 h =
0.77/h ≈ 18.6/day.** The gate has still refused **0**, so no refusal *rate* can be measured yet —
applying the counterfactual post-cascade rate of **81.2 %** to the measured arrival rate gives
**≈15 refusals/day, not ~40**.

| what becomes readable | n (**unchanged**) | was, at 40/day | **now, at ~15/day** |
|---|---|---|---|
| ±0.50 % CI at 4h | 11 | 6 hours | **0.7 days** |
| ±0.25 % CI at 4h | 41 | 1 day | **2.7 days** |
| **FAST TRIGGER — first split** | **100** | **2.5 days** | **≈6.6 days** |
| **SLOW TRIGGER** — 0.06 % effect | **700** | 17 days | **≈46 days** |

🔴 **THE OPERATIVE RULE: COUNT REFUSAL ROWS, NEVER DAYS.** Both pre-committed triggers are stated in
**n**, and **n is not being revised** — only the calendar translation was ever an estimate, built on
an arrival rate that has since been measured lower. **A session that reads the old figure, finds the
gate quiet on day 3 and concludes it is broken would be wrong: quiet is what ~15/day looks like.**
The check is `SELECT COUNT(*) FROM trades WHERE status='ema_envelope_blocked'`, not the date.

---

## 3. 🔴 THE MARGINAL-CONTRIBUTION QUESTION — AND PRECISELY WHAT IT DOES NOT TOUCH

Over 30 days the cascade already refuses **3,372** signals the envelope would also have refused. The
envelope's **incremental** contribution is therefore smaller than its standalone rate implies. The
two halves must not be conflated later, so they are recorded separately:

| quantity | status |
|---|---|
| **EFFECT SIZE** — §4d, Δ+0.699R, n=40, p=0.029 | **NOT affected.** Measured on **executed** positions, which are cascade survivors **by construction** — already the right cohort. |
| **VOLUME** — how much work the gate does that the cascade was not already doing | **OVERSTATED.** The ~80 % rate describes signals *in general*, not the marginal ones the cascade let through. |

**This is a different question from "does the envelope refuse correctly"** — §2.54 answers that one
and is not disturbed. Opened, not measured, not chased.

---

## 4. 👁 OBSERVATION, NOT AN INVESTIGATION — THE CASCADE AT 88.6 % IN THIS WINDOW

Since 14:41:20 the cascade refused **31 of 35** entry-intent signals (**88.6 %**) against a 30-day
figure of **73.2 %**. 🔴 **Most likely a quiet-window artifact; recorded, not chased.** The 15:33
investigation established the cascade did not tighten, and an **independent re-measure today
reproduces it**:

```
2026-05  n=2837  htf_blocked=2100  74.0%
2026-06  n=5504  htf_blocked=3993  72.5%
2026-07  n=5851  htf_blocked=4289  73.3%
2026-08  n= 823  htf_blocked= 602  73.1%
```

The cited **74 / 72.5 / 73.3 is confirmed**. The fourth figure, 70.1 %, was August measured at 15:33;
**August now reads 73.1 %** as the month fills — itself an instance of the very small-window effect
this observation is being discounted for.

**Four of today's wrong claims came from reading a one-day window as a trend.** It becomes a real
question only if it persists past a few days — and the ledger now measures it for free: the
`🧱 cascade` row against the `🔎 reached the flat gate` line **is** this ratio, printed daily.
