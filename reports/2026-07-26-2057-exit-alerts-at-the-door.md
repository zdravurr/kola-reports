# exit-alerts-at-the-door

_2026-07-26 20:57 UTC_

---

# TITAN — where the 5m exit alerts actually go: the door, not the database

**2026-07-26 · READ-ONLY. Nothing fixed, nothing proposed, nothing applied.**
Tree clean at `f7df202`.

**The operator was right and my earlier audit was wrong in an important way.** Reading only the
database made an entire alert stream invisible. Corrected findings:

1. **A separate 15m EXIT alert set DOES exist, IS arriving, and IS working.** It is distinguishable
   from 15m entry by the `task` field: entry sends `task="confirmation"`, exit sends
   `task="price_action"`. Hypothesis 6 — **CONFIRMED**.
2. **The 5m exit alert cannot be distinguished from the 5m entry alert by any code, because on 5m
   both would carry `task="price_action"`, and the router then FORCES the slot from the timeframe.**
   If a 5m exit alert is being sent, it is being consumed as an entry trigger and is invisible.
3. **There IS a gap at the door — 374 requests over 15 days — but it is not the exit alerts.** It is
   the 15m ENTRY stream (HyperWave / Reversal / Divergence), which updates the state-machine slot and
   is **never written to `trades`**. Mercury-SOL writes these; Titan does not. That is why my earlier
   "complete vocabulary" listed **0 of 10** of the operator's 15m entry alerts.

---

# PART 1 — The door

## 1.1 nginx vs the database

nginx retention is **15 days**, not 65 — the comparison can only be made over 2026-07-12 .. 07-26.
Titan endpoint is `POST /webhook?…`; SOL is `POST /webhook/sol` and is excluded.

```
                POST to nginx   rows in trades   gap
2026-07-12                353              329   -24
2026-07-13                278              257   -21
2026-07-14                276              254   -22
2026-07-15                150              126   -24
2026-07-16                219              199   -20
2026-07-17                281              250   -31
2026-07-18                329              304   -25
2026-07-19                287              264   -23
2026-07-20                262              234   -28
2026-07-21                194              164   -30
2026-07-22                256              234   -22
2026-07-23                321              294   -27
2026-07-24                311              286   -25
2026-07-25                238              215   -23
2026-07-26                266              237   -29
TOTAL                    4021             3647  -374     (9.3%, ~25/day)
```
Response codes: **4013 × 200 · 6 × 504 · 2 × 499.** So the 374 are not rejections — they are
requests the app accepted, answered 200, and did not persist.

## 1.2 Where they go — located exactly

The app logs a `WEBHOOK_IN` line with the **raw body** for every request. The journal only retains
**2026-07-24 23:45 → now**, but that window resolves it:

```
WEBHOOK_IN received:      511
rows in trades, same window: 458
gap:                       -53

incoming by tf:   5m = 437 · 15m = 64 · 60m = 10
persisted by tf:  5m = 437 · 15m = 11 · 60m = 9 (+1 NULL)
```
**5m and 60m reconcile exactly. The entire loss is on 15m: 64 in, 11 out — 53 discarded (83%).**

The code path (`main.py:2878-2887`):
```python
state_machine.update_slot('15m_confirm', direction or 'NEUTRAL', signal_name)
hw_subtype, hw_weight = engine_15m.evaluate(signal_name)
send_tg(...)
return jsonify({"status": "confirm_updated", ...}), 200      # <-- NO insert_signal
```
The 15m entry-confirmation branch updates the slot, sends a Telegram card, and returns 200 without
writing a row. Confirmed in the data: **`SELECT … WHERE signal_type LIKE '%confirm%'` returns
exactly one kind of row — `15m_exit_confirm` (328). There is not a single `15m_confirm` row in
Titan's entire database.**

**Nothing is dropped at the door.** No bad-secret rejections, no unparseable payloads, no dedupe.
`Invalid key`, `UNPARSED`, `Bad/missing action`, `unknown/missing tf`: **0 occurrences** in the
retained journal. The loss is a missing write, not a rejection.

## 1.3 Raw payloads, verbatim

Every distinct body shape received in the journal window:
```
437 x  {"action": <NAME>, "task": "price_action",  "tf": "5m"}
 52 x  {"action": <NAME>, "task": "confirmation",  "tf": "15m"}
 12 x  {"action": <NAME>, "task": "price_action",  "tf": "15m"}    <-- the 15m EXIT stream
  6 x  {"action": <NAME>, "task": "confirmation",  "tf": "60m"}
  1 x  {"action": "Trend C. Up",   "task": "trend_catch", "tf": "60m"}
  1 x  {"action": "Smart T. Bullish","task": "signal",      "tf": "60m"}
  1 x  {"action": "Neo C. Bearish",  "task": "signal",      "tf": "60m"}
  1 x  {"action": "Exit S.",        "task": "exit",        "tf": "60m"}
```
**There is no 5m body with anything other than `task="price_action"`.** No `task="exit"` on 5m, no
second 5m stream of any kind, in 437 alerts over two days.

---

# PART 2 — The operator's lists against reality

## 2.4 / 2.5 The 15m entry set DOES arrive — it was simply never recorded

Reconciliation of the DB against the operator's lists:
```
60m ENTRY        : 16/17 present.  NEVER ARRIVED: "Any B. Contrarian"
15m ENTRY        :  0/10 present.  NEVER ARRIVED (in the DB): all ten
5m PRICE ACTION  : 32/32 present.
Arrived but on no list: "close_long" (one legacy row)
```
The 15m row of that table is **an artefact of the missing write, not of missing alerts.** From the
live journal, over two days:
```
hyperwave signal up 17 · hyperwave signal down 13 · hyperwave ob signal down 5 · hyperwave os signal up 1
reversal up 4 · reversal down + 4 · reversal down 3
bearish divergence 4 · bullish divergence 1
                                          all tf='15m', task='confirmation'   (52 total, ~26/day)
```
They arrive, they reach `engine_15m.evaluate()` and the matrix slot — which is why they show in the
Telegram cards as `HW_SIGNAL_LONG` / `REVERSAL_SHORT` — and then they vanish. **"Any B.
Contrarian" is the only alert in any list that genuinely never arrived** (0 in the DB, 0 in the
journal; "Any B. Contrarian" also 0 in the journal but present historically).

## 2.6 HYPOTHESIS: the 15m Price Action alerts are the operator's exit set — **CONFIRMED**

```
15m + task="confirmation"   -> HyperWave / Reversal / Divergence   = the 15m ENTRY set
15m + task="price_action"   -> I-BOS / I-CHOCH / S-BOS / S-CHOCH   = the 15m EXIT set
```
Two distinct TradingView alerts on the same timeframe, distinguished by `task`. The bot routes both
into the 15m slot (see 2.7), where the armed-exit branch intercepts the Price Action ones and, if a
side is armed, fires the close. **The 15m exit tier is configured correctly and is working as
designed.** 328 `15m_exit_confirm` + 5 `15m_armed_exit` rows are that set doing its job.

My earlier conclusion — *"the 15m tier is entry vocabulary re-pointed"* — was **wrong**. The
vocabulary overlaps by coincidence of indicator family, but the alerts are genuinely separate.

## 2.7 Why the same trick cannot work on 5m — the router forces the slot from the timeframe

```python
_TF_TO_ACTION   = {'1h':'context_update', '60m':'context_update',
                   '15m':'process_signal', '5m':'execute_trade'}
_TASK_TO_ACTION = {'price_action':'execute_trade', 'reversal':'process_signal', ...}
_DIRECT_TASKS   = {'exit'}

if task_field in _DIRECT_TASKS:                 # checked FIRST — bypasses everything
    return _handle_exit_signal(data)

mapped_action = _TASK_TO_ACTION.get(task_field)
if mapped_action:
    if expected_action and mapped_action != expected_action:
        mapped_action = expected_action          # <-- TIMEFRAME WINS over task
    return _handle_state_machine(data, mapped_action)
```

* **15m + `price_action`** → task says `execute_trade`, tf says `process_signal` → **forced to
  `process_signal`** → lands in the 15m slot → armed-exit branch catches it. **The exit tier works
  because of the override, not because the code recognises it as an exit.**
* **5m + `price_action`** → task says `execute_trade`, tf says `execute_trade` → agreement →
  **entry**. A 5m exit alert carrying `task="price_action"` is byte-identical to a 5m entry alert.
  No code can separate them.
* **The only escape is `task="exit"`**, which is tested before the forcing and ignores `tf`
  entirely — but `_handle_exit_signal` **arms**, it does not close. A 5m `task="exit"` alert would
  behave like the 1H one, not like a final-call tier.

**Test for whether a second 5m alert is firing:** identical `(tf, action)` pairs arriving within 90
seconds of each other would be the signature of entry+exit doubling on the same bar event.
**Result: 0 such pairs in 511 alerts.** So either the 5m exit alert is not currently firing, or it
fires at different moments and is being silently absorbed as an entry trigger — the data cannot
distinguish those two, because the payloads are identical.

---

# PART 3 — Mercury-SOL

## 3.8 Same code, one meaningful divergence

```
Group-B regex        : IDENTICAL (byte-for-byte)
EXIT_CONFIRM_TF      : '15m' on both
EXIT_PENDING_TTL_MIN : 360 on both
_TF_TO_ACTION        : same mapping (SOL omits the '60m' key; Titan has both '1h' and '60m')
_TASK_TO_ACTION      : same mapping, whitespace only
```

## 3.9 SOL receives the same vocabulary — **and records the part Titan discards**

```
                       SOL      Titan
15m_confirm            997        0     <-- HyperWave / Reversal / Divergence
15m_no_trend           150        0
15m_exit_confirm       235      328
15m_armed_exit           6        5
60m_exit                29       32+
60m_exit_armed          12       24
exit_long / exit_short   5        0
```
SOL's 15m entry confirmations are persisted with full detail — `HyperWave Signal Up` 318,
`HyperWave Signal D.` 307, `Reversal D.` 73, `Bearish D.` 28, and so on. **Titan has
zero.** Same alerts, same code family, different persistence.

SOL also carries `exit_long` / `exit_short` executed rows (5) that Titan has none of.

## 3.10 The divergence, stated plainly

**SOL kept a write that Titan lost.** The 15m confirmation branch persists on SOL and does not on
Titan. That single missing `insert_signal` is the entire 374-request gap, and it is why every
database-only analysis of Titan — including my earlier report — showed `0/10` of the operator's 15m
entry alerts and concluded they did not exist.

---

# Deliverable: where do the 5m exit alerts go?

**Not "never sent" and not "rejected at the door".** The honest answer is the fourth option, with a
caveat:

* **They cannot arrive distinguishably.** On 5m, an exit alert built from the Price Action indicator
  set produces a payload byte-identical to the 5m entry alert (`task="price_action"`, `tf="5m"`), and
  the router forces that combination to the entry slot. If such an alert is firing, **it is being
  consumed as an entry trigger** and is indistinguishable in every log and every table.
* **In the two days of retained journal, no evidence of a second 5m stream appears** — 437 alerts,
  one payload shape, zero same-event duplicates. That is consistent with the 5m exit alert being
  inactive, and equally consistent with it firing at moments that look like ordinary entries. **The
  data cannot separate those two possibilities**, and I will not claim it can.
* **The 15m exit tier, by contrast, is genuinely working** — because there the tf-override happens to
  push the exit stream into the correct slot.

The break is therefore in **three** places, only one of which I identified correctly before:

| where | what | severity |
|---|---|---|
| **Payload design (config)** | 5m entry and 5m exit alerts are indistinguishable — no `task`, no marker separates them. Only `task="exit"` escapes the tf-forcing, and that path arms rather than closes | **root cause** |
| **Router (code)** | `mapped_action = expected_action` — the timeframe overrides the declared task. Makes the 15m exit tier work by accident and the 5m exit tier impossible by construction | design consequence |
| **Persistence (code)** | Titan's 15m confirmation branch returns 200 without `insert_signal`. 374 alerts / 15 days invisible. SOL does not have this defect | **made the first two invisible** |

**No fixes proposed.** Nothing was implemented, and nothing was applied.

---

Tree clean at `f7df202`; `titan.service` healthy; Mercury-SOL untouched (read-only).
This report **corrects** the 20:28 report, which read the database only and therefore concluded that
no separate 15m/5m exit alerts existed. The 15m ones do exist and work.
