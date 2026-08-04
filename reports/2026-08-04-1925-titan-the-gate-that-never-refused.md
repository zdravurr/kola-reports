# THE FLAT GATE HAS REFUSED NOTHING — AND THE CARD THAT WOULD HAVE TOLD YOU IS REAL

**2026-08-04 19:25 UTC · Titan LIVE, real money, flat · HEAD `be53e63` · items 1–2 READ-ONLY;
item 3 is a DIFF, NOT APPLIED**

**Header re-verified by importing `config` at runtime, not copied forward:**
`LIVE_TRADING_ENABLED=True`, `ORDER_ADAPTER_LIVE=True`, `EMA_ENVELOPE_GATE_ENABLED=True`,
`_TFS=('1h','15m')`, `_REQUIRED_DIR='Expanding'`, `_FAIL_OPEN=True`, `SL_ATR_MULT=2.25`,
`TRAIL_MULT_ATR=1.6875`, `$30 × 5 = $150`. No position open (flat since **00:26:04 UTC**, vpos 92
closed −$1.31) — so nothing upstream was suppressing entries during the window below.

Canon: **§2.56**. Snapshot: `reports/2026-08-04-1925-open-items.md`.

---

## 🔴 THE ONE-PARAGRAPH ANSWER

**Zero refusals in 4h35m — but the gate is not inert and the projection is not falsified. It is
STARVED.** In that window only **4 signals reached the gate at all** against ~9.8 expected, because
the HTF cascade ate **30 of 34** entry-intent signals upstream (88.2 %, against a 30-day norm of
73.6 %). **Eleven of those 30 cascade-blocked signals carried a non-Expanding leg** — they are
refusals the envelope was built to make and never got to see. The refusal card **is wired and does
send**: proven by execution at 19:16:33 UTC, Telegram `message_id` **28353**. It has never been
observed for the only reason available — **there has been nothing to refuse.** This is NOT the
"reads as armed, is not" class; this one is armed.

---

## 1. HAS IT REFUSED ANYTHING YET? NO — 0 ROWS, AND ONLY 4 CHANCES

`SELECT ... WHERE status='ema_envelope_blocked'` → **0 rows, ever.** Confirmed in the live
`trades.db` and cross-checked against the journal: exactly **4** `[EMA-ENV]` lines exist since the
gate went live at 14:41:20, **all PASS, none BLOCK, none FAIL-OPEN**:

| UTC | verdict | 1h gap | 15m gap | proposed side | trades row |
|---|---|---|---|---|---|
| 14:45:15 | PASS | Expanding | Expanding | SHORT | 21347 |
| 14:45:15 | PASS | Expanding | Expanding | SHORT | 21348 |
| 14:50:06 | PASS | Expanding | Expanding | SHORT | 21349 |
| 14:55:08 | PASS | Expanding | Expanding | SHORT | 21350 |

**Nothing has reached the gate since 14:55:08 — 4 hours 21 minutes of no evaluations at all.** All
four are SHORT; the gate has not yet seen a single LONG proposal.

### The measured rate against the pre-registered projection

| quantity | projected (§2.47) | **measured since 14:41:20** |
|---|---|---|
| signals reaching the gate | 51.3/day = **2.14/h** | 4 in 4.58 h = **0.87/h ≈ 21/day** |
| refusals | ~80 % ⇒ **≈41/day** | **0/day** (0 of 4) |

**Do not read that as a refuted projection.** Two honest corrections run against my own headline:

- **The refusal rate was NOT over-estimated.** Measured on the cohort that actually reaches this
  point in the chain (post-cascade rows only), the counterfactual refusal rate is **81.2 % over 30
  days (1241/1529)** and **84.0 % over 7 days (310/369)** — *higher* than the 79.6 % measured on all
  signals. I expected the opposite (that cascade-survivors would be disproportionately expanding) and
  the data says no. The ~40/day figure is arithmetically intact: 51.3 × 0.812 = **41.7/day**.
- **The four arrivals are one market episode, not four draws.** They fall in a single 10-minute
  cluster, 14:45:15–14:55:08, on one snapshot state. P(0 refusals | 4 independent draws at
  p=0.812) = **0.00125** and P(≤4 arrivals | λ=9.8) = **0.033**, but with n_effective ≈ **1** neither
  number is evidence of anything. **4h35m is not a test of a 40/day claim; it is one observation.**

### Where the signals actually went — and what the cascade took away from the gate

Entry-intent rows since 14:41:20 (n=34), against the same rows' EMA gap directions:

| what happened | n | of which **non-Expanding** on 1h or 15m |
|---|---|---|
| 🧱 `htf_blocked` — cascade refused, **gate never saw it** | 30 | **11** |
| 🤖 `ai_skipped` — passed cascade **and gate**, advisor declined | 4 | 0 |
| 🚫 `ema_envelope_blocked` | **0** | — |
| ✅ entered | 0 | — |

**The eleven are the finding.** `1h=Expanding · 15m=Contracting` ×9, `1h=Expanding · 15m=Flat` ×1,
`1h=Flat · 15m=Contracting` ×1. Every one of them is a signal the flat gate would have refused, and
every one of them was already dead when it arrived. **The gate sits behind a gate that today is
refusing 88 % of everything**, and the two overlap heavily by construction — over 30 days the cascade
alone consumes **3372 signals that the envelope would also have refused**.

**So: is it "both legs simply Expanding on every signal in current conditions"?** On the four the
gate saw, yes. On the market as a whole, **no** — 11 of the 30 signals in the same window were flat
on at least one leg. The all-Expanding reading is a property of *cascade survivors*, not of the day.

---

## 2. 🔴 DOES THE REFUSAL CARD ACTUALLY SEND? **YES — PROVEN BY EXECUTION**

It was wired, it is complete, and it delivers. **This is not the seven-times class.** Receipt:

```
[probe] TELEGRAM RECEIPTS (http, ok, message_id, date, chat_id):
[probe]   #0 (200, True, 28352, 1785870989, 6284337254)   <- TEST START notice
[probe]   #1 (200, True, 28353, 1785870993, 6284337254)   <- THE REFUSAL CARD
[probe]   #2 (200, True, 28354, 1785870994, 6284337254)   <- TEST END notice
[probe] gate returned: <class 'tuple'>
[probe] HTTP 200 body={"combo":"PROBE|SHORT","direction":"SHORT",
        "ema_gap_dirs":{"15m":"Flat","1h":"Contracting"},
        "required_dir":"Expanding","status":"ema_envelope_blocked"}
[probe] ema_envelope_blocked rows in copy AFTER: 1
[probe] refused row: (21408, '2026-08-04 19:16:29', 'ema_envelope_blocked', 'sell',
                      'SHORT', None, 'Contracting', 'Flat')
[probe] skip_attribution rows with that status: 1
[probe] LIVE db ema_envelope_blocked rows (must still be 0): 0
```

**The card in your chat between the two 🧪 TEST notices is byte-identical to what a real refusal
emits** — `send_tg` was not wrapped, patched or reformatted; the probe called
`main._ema_envelope_gate` and let the function's own `send_tg` run.

**How it was made safe** (`scratchpad/prove_ema_card.py`):

1. `trades.db` **copied** first; `DB_PATH` repointed in **`main`, `skip_attribution` AND
   `signal_matrix`** — one module is never enough
   ([[feedback_test_isolation_every_module_own_dbpath]]). Asserted equal before any call.
2. No workers, no order adapter: `main.py` starts those only under `__main__`, so importing it as a
   module cannot place an order.
3. The snapshot was built from a **real** recent row (trades.id 21407) with only
   `ema_gap_dir_1h → Contracting` and `ema_gap_dir_15m → Flat` overridden, injected on
   `flask.g.market_snap` inside `app.test_request_context` — the same object
   `_request_snapshot()` reads in production.
4. Delivery was read from the **Telegram API response**, not from the absence of an error line
   ([[feedback_verify_by_presence_not_absence]]). "No `[TG SEND FAIL]` printed" would have been
   absence-evidence; `ok:true, message_id:28353` is presence-evidence.

**The whole refusal path executes, in order:** log line → `insert_signal` row (id 21408, status and
both gap columns stamped) → `update_signal_execution` → `_record_skip_attribution` (1 row, so
`TRACKED_STATUSES` really does contain `ema_envelope_blocked`) → **`send_tg` → delivered** →
HTTP 200 refusal returned to the webhook. The live DB was re-read afterwards and still holds **0**
such rows.

⚠️ **What this does NOT prove**, stated rather than glossed: the probe supplied the snapshot itself,
so it does not prove a *real* webhook populates `g.market_snap` before this function reads it. That
half is proven separately and independently — the four live PASS lines in item 1 read gap directions
off the very same `_request_snapshot()` on real traffic. Between the two, every link in the chain has
now been exercised on the live binary.

🔴 **`confluence_score` is NULL on the refused row** (visible in the probe output above). That is
deliberate and already documented at the call site: this gate runs before the macro adjustment, so no
gated score exists. It is not a defect — but it does mean **a refused row cannot be compared on that
column against any other status.**

---

## 3. THE OPERATOR CANNOT READ THE SILENCE — RECOMMENDATION: **THE DAILY DIGEST**

### Messages per day, at the MEASURED rate

| option | at the measured rate (0 refusals/day) | at the 30-day counterfactual (41.7/day) | answers "which of the three causes?" |
|---|---|---|---|
| card per refusal (already built) | **0 msg/day** | **≈42 msg/day** | **no** — reports one cause only |
| daily silence ledger | **1 msg/day** | **1 msg/day** | **yes** — counts per cause |

**The card fails you at both ends, and the measured rate is the sharper argument.** At today's
measured refusal rate the card sends **zero messages** — it is *indistinguishable from the silence
you are complaining about*. When the market turns flat it sends ~42/day, which is spam. And in
neither state does it tell you what you actually asked: how much of the silence belongs to *no
signals*, how much to the *cascade*, and how much to the *flat gate*. A card can only ever report
its own gate — today's window is the proof, since the loudest cause (30 cascade blocks) would have
emitted nothing at all.

**Recommended: one daily message, and mute the card, so exactly one channel is live.** Rendered from
the real database, this is what the last 24 h and the since-the-gate window produce:

```
📊 TITAN — SILENCE LEDGER (24h)          │ 📊 TITAN — SILENCE LEDGER (5h)
03.08 19:20 → 04.08 19:20 UTC            │ 04.08 14:20 → 04.08 19:20 UTC
                                         │
🔔 entry-intent signals: 216             │ 🔔 entry-intent signals: 39
  🧱 cascade (HTF)         172   79.6%   │   🧱 cascade (HTF)          34   87.2%
  🚫 flat gate (EMA env)     0    0.0%   │   🚫 flat gate (EMA env)     0    0.0%
  📉 score below bar        26   12.0%   │   📉 score below bar         1    2.6%
  🤖 advisor declined        9    4.2%   │   🤖 advisor declined        4   10.3%
  ⛔ risk halt               8    3.7%   │   ✅ ENTERED                 0    0.0%
  ✅ ENTERED                 1    0.5%   │
                                         │ 🔎 reached the flat gate: 5 — refused 0 (0%)
🔎 reached the flat gate: 44 — refused 0 │ 📏 latest EMA9/21 gap: 1h Expanding · 15m Expanding
📏 latest gap: 1h Expanding · 15m Expanding
```

**The three causes are separable on sight**, which was the requirement:
`entry-intent signals: 0` = **no signals arrived**; the `🧱 cascade` row = **cascade-blocked**; the
`🚫 flat gate` row = **flat-gate-blocked**. The `🔎 reached the flat gate` line exists because
without it a `0` on the flat-gate row is ambiguous — it cannot be told apart from *the gate was never
reached*, which is exactly today's situation and exactly the confusion this whole item is about. The
remaining rows are printed so the arithmetic closes; an unrecognised status shows up as `❓ other`
rather than silently vanishing.

### The diff — **NOT APPLIED**

**Part A — new standalone file `titan-bot/silence_digest.py`** (full source in the appendix below). Deliberately a cron script and **not** a change inside `main.py`: the live entry path is
not touched at any point, and a defect in it can only make a report wrong — it can never refuse or
admit a trade. Reads `trades.db`, sends exactly one message, prints the Telegram `message_id` to its
log so a silent failure is visible. Cron, one line, 1 message/day:

```cron
05 8 * * * /usr/bin/python3 /root/titan-bot/silence_digest.py >> /var/log/titan_silence_digest.log 2>&1
```

**Part B — mute the per-refusal card so only one channel is live** (`config.py` + `main.py`,
syntax-checked with `ast.parse`; requires a restart to take effect):

```diff
--- a/config.py
+++ b/config.py
@@ -531,6 +531,14 @@
 EMA_ENVELOPE_TFS           = ('1h', '15m')  # every listed TF must agree
 EMA_ENVELOPE_REQUIRED_DIR  = 'Expanding'
 EMA_ENVELOPE_FAIL_OPEN     = True          # missing reading ⇒ admit (see above)
+# PER-REFUSAL TELEGRAM CARD — OFF. The refusal path DOES send (proven by
+# execution 2026-08-04 19:16 UTC, Telegram message_id 28353); it is muted, not
+# missing. At the measured post-cascade refusal rate (81.2% of ~51 signals/day
+# reaching this gate) it would emit ~41 cards/day — and a card per refusal still
+# would not answer the operator's actual question, which is how much silence
+# belongs to WHICH gate. `silence_digest.py` answers that in 1 message/day.
+# Exactly ONE of these two channels is on at a time; True re-arms the card.
+EMA_ENVELOPE_REFUSAL_CARD  = False
 
 # --- Excursion timeline instrumentation (observational; drives NO exit) ---

--- a/main.py
+++ b/main.py
@@ -505,7 +505,7 @@
     # EMA envelope entry gate (2026-08-04) — reasoning + weaknesses live in config.py
     EMA_ENVELOPE_GATE_ENABLED, EMA_ENVELOPE_TFS, EMA_ENVELOPE_REQUIRED_DIR,
-    EMA_ENVELOPE_FAIL_OPEN,
+    EMA_ENVELOPE_FAIL_OPEN, EMA_ENVELOPE_REFUSAL_CARD,
     EXIT_ADVISOR_PAPER_ENABLED, EXIT_ADVISOR_DRYRUN, EXIT_ADVISOR_ON_15M_CONFIRM,
@@ -1989,19 +1989,24 @@
         f"{'*' if tf in EMA_ENVELOPE_TFS else ''}"
         for tf in _all_tfs)
-    send_tg(
-        f"🚫 <b>BLOCKED — EMA envelope (flat market)</b>\n"
-        f"{dxy_tag()}\n"
-        f"🎯 Trigger: {direction}\n"
-        f"📏 EMA9/21 gap: {_ctx}\n"
-        f"🔒 Gate: needs <b>{EMA_ENVELOPE_REQUIRED_DIR}</b> on "
-        f"<b>{' AND '.join(EMA_ENVELOPE_TFS)}</b> (*) — got {_decid}\n"
-        f"ℹ️ Matrix net: {matrix_result.get('direction', '?')} "
-        f"{matrix_result.get('score', 0.0):.2f}/10 — the score gate was never reached\n"
-        f"<i>applied 2026-08-04: n=40 clean, Δ+0.699R, p=0.029, fails Bonferroni; "
-        f"review at 20 executed entries per side</i>"
-        + (f"\n<code>{combo}</code>" if combo else "")
-    )
+    # Muted by default — see EMA_ENVELOPE_REFUSAL_CARD in config.py. The row,
+    # the skip_attribution anchor and the log line above are unconditional, so
+    # the refusal stays fully countable with the card off; only the per-event
+    # Telegram noise (~41/day) is suppressed in favour of the daily ledger.
+    if EMA_ENVELOPE_REFUSAL_CARD:
+        send_tg(
+            f"🚫 <b>BLOCKED — EMA envelope (flat market)</b>\n"
+            f"{dxy_tag()}\n"
+            f"🎯 Trigger: {direction}\n"
+            f"📏 EMA9/21 gap: {_ctx}\n"
+            f"🔒 Gate: needs <b>{EMA_ENVELOPE_REQUIRED_DIR}</b> on "
+            f"<b>{' AND '.join(EMA_ENVELOPE_TFS)}</b> (*) — got {_decid}\n"
+            f"ℹ️ Matrix net: {matrix_result.get('direction', '?')} "
+            f"{matrix_result.get('score', 0.0):.2f}/10 — the score gate was never reached\n"
+            f"<i>applied 2026-08-04: n=40 clean, Δ+0.699R, p=0.029, fails Bonferroni; "
+            f"review at 20 executed entries per side</i>"
+            + (f"\n<code>{combo}</code>" if combo else "")
+        )
     payload = {
         "status": "ema_envelope_blocked",
```

**Part B costs nothing evidentially:** the row, the `skip_attribution` anchor and the `[EMA-ENV]`
log line are all *outside* the `if`, so refusals stay fully countable with the card off — and the
card's delivery is now proven by execution rather than by waiting to see one.

**If you would rather keep the card instead**, the honest version of that choice is: revert Part B,
skip Part A entirely, and accept that you will learn about flat-gate refusals only — silence caused
by the cascade (79.6 % of it over the last 24 h) stays unreadable. I do not recommend it.

---

## WHAT WOULD CHANGE THESE ANSWERS

- **Item 1 becomes real evidence at n≈41 gate evaluations** (§2.47's own pre-registered arithmetic).
  At the *arrival* rate measured today (21/day) that is **~2 days**, not the 1 day projected. If the
  cascade keeps consuming 88 % it will be longer still — **track arrivals, not calendar time.**
- **The starvation itself is now the open question**, and it is new: the envelope was justified on a
  refusal rate measured over *all* signals, but it only ever sees cascade survivors. Over 30 days the
  cascade already refuses 3372 signals the envelope would also refuse. **The marginal contribution of
  the envelope is therefore smaller than its standalone rate suggests** — it is not measured here and
  it is not the same question as "does the envelope refuse correctly".
- Item 2 is **closed** — armed, and proven live-adjacent by execution with a delivery receipt.

---

## APPENDIX — PROPOSED `titan-bot/silence_digest.py` IN FULL (NOT APPLIED)

```python
#!/usr/bin/env python3
"""TITAN — SILENCE LEDGER. One message per day that says WHY the bot was quiet.

The operator cannot tell, from Telegram, whether Titan was silent because no
signals arrived, because the HTF cascade refused them, or because the EMA
envelope (flat) gate refused them. All three look identical: nothing arrives.
This prints the counts PER CAUSE, so silence becomes readable.

Deliberately a standalone cron script, NOT a change inside main.py: the live
entry path is not touched at all, and a defect here can only make a report
wrong — it can never refuse or admit a trade.

Reads `trades.db` only. Sends exactly ONE Telegram message per run.
Cron: 05 08 * * *  ->  1 message/day.
"""
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

load_dotenv('/root/titan-bot/.env')

DB_PATH = '/root/titan-bot/trades.db'
TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WINDOW_HOURS = int(os.getenv('SILENCE_DIGEST_HOURS', '24'))

# Entry-intent statuses, in the order a signal meets them. The three CAUSES OF
# SILENCE the operator asked to separate are the first three rows; the rest are
# included so the arithmetic closes and a missing row is visible as a gap.
LADDER = [
    ('htf_blocked',      '🧱 cascade (HTF)'),
    ('ema_envelope_blocked', '🚫 flat gate (EMA env)'),
    ('below_threshold',  '📉 score below bar'),
    ('ai_skipped',       '🤖 advisor declined'),
    ('risk_halt',        '⛔ risk halt'),
    ('virt_cap_blocked', '🧮 virtual cap'),
    ('executed',         '✅ ENTERED'),
]
# Statuses that mean the signal got PAST the cascade and was therefore actually
# SEEN by the envelope gate. Without this the flat gate's 0 is unreadable: it
# cannot be told apart from "the gate was never reached".
POST_CASCADE = ('ema_envelope_blocked', 'below_threshold', 'ai_skipped',
                'risk_halt', 'virt_cap_blocked', 'executed')


def send_tg(text):
    if not (TG_TOKEN and TG_CHAT_ID):
        print('[SILENCE-DIGEST] no telegram credentials; not sent')
        return False
    r = requests.post(
        f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage',
        json={'chat_id': TG_CHAT_ID, 'text': text, 'parse_mode': 'HTML'},
        timeout=10)
    ok = r.status_code == 200 and r.json().get('ok')
    print(f'[SILENCE-DIGEST] sent={ok} http={r.status_code} '
          f'msg_id={(r.json().get("result") or {}).get("message_id")}')
    return bool(ok)


def main():
    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=WINDOW_HOURS)
    s = since.strftime('%Y-%m-%d %H:%M:%S')

    con = sqlite3.connect(DB_PATH)
    rows = dict(con.execute(
        "SELECT status, COUNT(*) FROM trades WHERE timestamp >= ? "
        "AND side IN ('buy','sell') GROUP BY status", (s,)).fetchall())
    total = sum(rows.values())
    reached = sum(rows.get(k, 0) for k in POST_CASCADE)
    flat_blocked = rows.get('ema_envelope_blocked', 0)
    gap = con.execute(
        "SELECT ema_gap_dir_1h, ema_gap_dir_15m, timestamp FROM trades "
        "WHERE ema_gap_dir_1h IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()

    head = (f"📊 <b>TITAN — SILENCE LEDGER</b> ({WINDOW_HOURS}h)\n"
            f"<i>{since:%d.%m %H:%M} → {now:%d.%m %H:%M} UTC</i>\n")

    if total == 0:
        body = ("\n<b>NO ENTRY-INTENT SIGNALS ARRIVED AT ALL.</b>\n"
                "The silence is upstream of every gate — TradingView sent "
                "nothing the bot treats as an entry.\n")
    else:
        lines = []
        for key, label in LADDER:
            n = rows.get(key, 0)
            if n == 0 and key not in ('ema_envelope_blocked', 'executed'):
                continue          # the two the operator is watching always print
            lines.append(f"  {label:<26} <b>{n:>4}</b>  {100*n/total:5.1f}%")
        other = {k: v for k, v in rows.items()
                 if k not in dict(LADDER)}
        if other:
            lines.append("  ❓ other: " + ", ".join(f"{k}={v}" for k, v in
                                                   sorted(other.items())))
        body = (f"\n🔔 entry-intent signals: <b>{total}</b>\n"
                + "\n".join(lines)
                + f"\n\n🔎 reached the flat gate (past the cascade): "
                  f"<b>{reached}</b>"
                + (f" — it refused <b>{flat_blocked}</b> "
                   f"({100*flat_blocked/reached:.0f}%)\n" if reached else
                   " — <b>the flat gate was never reached</b>\n"))

    if gap:
        body += (f"📏 latest EMA9/21 gap: 1h <b>{gap[0]}</b> · "
                 f"15m <b>{gap[1]}</b> <i>({gap[2]} UTC)</i>\n")

    send_tg(head + body)


if __name__ == '__main__':
    sys.exit(main())
```
