# DO NOT SHORT AGAINST A BULL DAILY — SPECIFIED AND PROVEN, **NOT APPLIED: THE BOOK IS NOT FLAT**

**2026-09-17 16:16 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · READ-ONLY throughout · Titan untouched**

`openitems_guard` → **exit 0** (titan-bot HEAD `f16c271`).

---

## 🔴 HEADLINE: §3 STOPPED AT THE FLAT GATE. POSITION #48 IS STILL OPEN.

Your §3a named the condition exactly: *"Position #48 (LONG @ 100.37, opened 2026-09-17 09:05) may still be open
— if it is, say so and STOP."* **It is.** Nothing was applied, backed up, edited or restarted.

| flat check | required | actual |
|---|---|---|
| open `virtual_positions` | 0 | **1 — #48 LONG @ 100.37, live, size 0.9, opened 2026-09-17 09:05:20** |
| `exit_pending` | 0 | **1 — LONG, armed 14:00:14, expires 20:00:14** |
| `active_positions` | 0 | **1 — LONG @ 100.37** |
| Bybit, both position indices | 0, **empty error list** | 🔴 **READ FAILED — error list NOT empty** |

🔴 **The venue leg did not return "zero positions". It returned nothing at all.** 24 consecutive attempts
(12 positions + 12 orders) died on CloudFront `403 Forbidden` through my Tor circuit — the documented
DigitalOcean-ASN block. My first script printed `NON-ZERO venue positions: 0`, and **that figure was an
artefact of a failed call, not a reading of the venue.** I am flagging it rather than quoting it: a "0" derived
from an exception is exactly the fabricated evidence that must never reach a flat check, and on a naked-position
question it is the most dangerous number on the page.

**The bot itself is healthy and reaching Bybit** — this was my circuit, not an outage. Proof from its own log:

```
16:06:18 [EXIT-ADVISOR-DRYRUN] trigger=hourly SOL/USDT:USDT LONG close=False conf=0.72
         upnl=+0.38R giveback=0.25R | Peak +0.63R ... Trailing stop arms at +0.75R
16:07:35 [HEARTBEAT] alive ticks=18431 (+24 in 303s) last_tick=12.4s open=1 mode=LIVE pid=2246062
```

#48 is live, up **+0.38R**, peak +0.63R, **+1.38R of cushion to its stop**, and being consulted hourly. No
alert condition. **It simply is not flat, so the change waits.**

**To apply: re-run this pass when #48 has closed and the venue read returns an empty error list.** The patch
below is complete, executed and waiting.

---

## 0. THIS IS NOT CANDIDATE 33 — STATED FOR THE RECORD

Per your instruction, so no later reader conflates them. From my
[2026-09-17-1541 report](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-09-17-1541-mercury-sol-candidate-33-require-bear-daily-for-a-short.md):

| | candidate 33 (**dead, 0 of 5**) | this rule (**discipline, not a candidate**) |
|---|---|---|
| condition | requires `trend_1d == 'bear'` | requires only `trend_1d != 'bull'` |
| live shorts refused | **10 of 10** — collapses into long-only | **2 of 10** (#32, #34) |
| paper shorts refused | 6 of 13 | **0 of 13** |
| status | measured, refuted, not convicted | **not measured, applied as discipline** |

Different rule, different row set, different basis. §5 of that report recorded this one as an explicit
**non-candidate** and I stand by that: as a statistical finding it is n=2 and worthless.

**The fact it rests on needs no sample, and that is the whole point.** §0 of the 1541 report established that
`trend_1d` **gates nothing** — the HTF alignment gate runs on 1H/15m/5m tiers only (`main.py:4126`). The book
proves it: **#32 (2026-08-10) and #34 (2026-08-13) both entered SHORT under a `bull` daily.** The bot shorts
while the daily trend points up, and nothing stops it. That is a thing a trader would not do, and it is being
closed on that basis — the same basis as the order-book gate (2026-08-10) and the flat-ADX gate (2026-08-17).

---

## 1. THE RULE

### 1a) Condition
Refuse a **SHORT** entry when `trend_1d == 'bull'` at decision time. **`bear` and `neutral` both pass.** The
LONG side is untouched. 4h is untouched. No other tier is read.

### 1b) 🔴 WHERE IT SITS — AND A CORRECTION TO THE SPEC YOU GAVE ME

You asked for it in the risk-gate chain, in the shape of `_dxy_halt(requested_side)` at `main.py:2003`, called
at `main.py:2045`. **The shape is right; that call site cannot work.** `trend_1d` does not exist yet at
`main.py:2045`.

The daily label is written from `_adv_snap`, which is not built until **`main.py:4529`**
(`_adv_snap = {**_snap, **_htf_snap}`) — roughly 2,500 lines downstream of the risk chain. The database proves
it, not just the code:

| status of live-era SHORT consultations | rows | with a `trend_1d` label |
|---|---|---|
| `htf_blocked` | 1,852 | **0** |
| `below_threshold` | 866 | **0** |
| `entry_gate_refused` | 309 | **0** |
| **`risk_halt`** ← your proposed call site | **231** | **0** |
| `flat_adx_blocked` | 180 | **0** |
| `book_blocked` | 22 | **0** |
| `ai_skipped` | 729 | 728 |
| `executed` | 10 | **10** |

**231 `risk_halt` short rows, not one carrying a daily label.** A gate placed there would read `None` on every
single consultation and — correctly fail-open per §1c — **admit 100% of the time. It would never fire once.**

**Corrected insertion point: `main.py:5333`**, immediately after the advisor verdict falls through
(`# ai_decide == 'execute' … → fall through`) and immediately before `# Execute single-entry order` at 5334.
There `_adv_snap` is in scope with the label in hand, and a refusal costs an entry and nothing else.

* **runs before it:** macro halt → DXY halt → daily-loss breaker → per-side position cap (`main.py:2038-2070`);
  then HTF alignment, confluence threshold, entry gate, flat-ADX gate, book gate, and the AI advisor verdict.
* **runs after it:** the single-entry order execution block (`main.py:5334+`) — order placement, fill read,
  SL placement, `status='executed'`.

It is the **last gate before the order goes out**, which is where a discipline rule belongs: everything
measurable has already had its say.

### 1c) 🔴 EVERY ERROR PATH ADMITS — PROVEN BY EXECUTION, 20/20

```python
def _bull_daily_short_halt(requested_side, snap):
    """(halted, reason, label) — refuse a SHORT when the DAILY trend is BULL.
    🔴 FAIL-OPEN BY CONSTRUCTION. Every unknown, missing, stale, malformed or
    unreadable label ADMITS. A bug here must never be able to invent a refusal:
    the only path to True is an explicit, normalised 'bull'."""
    if not BULL_DAILY_SHORT_BLOCK_ENABLED:
        return False, 'gate disabled (kill switch)', None
    if requested_side != 'SHORT':
        return False, f'side={requested_side} — gate is SHORT-only', None
    try:
        raw = snap.get('trend_1d') if hasattr(snap, 'get') else None
    except Exception as e:
        return False, f'ADMIT — snapshot unreadable ({type(e).__name__})', None
    if not isinstance(raw, str):
        return False, f'ADMIT — daily label absent/not-a-string ({type(raw).__name__})', None
    label = raw.strip().lower()
    if label != 'bull':
        return False, f'ADMIT — daily={label!r} (not bull)', label
    if BULL_DAILY_SHORT_BLOCK_DRYRUN:
        return False, 'DRYRUN would block — daily=bull', label
    return True, 'SHORT refused — daily trend is BULL', label
```

Executed, all 20 paths, **0 failures**:

| path | halted | path | halted |
|---|---|---|---|
| `'bull'` + SHORT | ✅ **True** | value `None` (the 3,461-row case) | False — ADMIT |
| `'BULL'` uppercase | ✅ **True** | empty string / whitespace only | False — ADMIT |
| `' Bull '` padded | ✅ **True** | `'bullish'` near-miss | False — ADMIT |
| `'bear'` | False — ADMIT | int / list / dict instead of str | False — ADMIT |
| `'neutral'` | False — ADMIT | `snap` is `None` / str / list | False — ADMIT |
| **LONG** + `'bull'` | False — ADMIT | **`snap.get()` RAISES** | False — ADMIT |
| key missing | False — ADMIT | kill switch off / DRYRUN on | False — ADMIT |

**The only route to `True` is `side == 'SHORT'` and a normalised literal `'bull'`.** `'bullish'` does not block —
strict equality against the label vocabulary `{bull, bear, neutral}` is deliberate and fail-open.

### 1d) Flags — ships ARMED
```python
BULL_DAILY_SHORT_BLOCK_ENABLED = True    # kill switch — False restores the pre-2026-09-17 path
BULL_DAILY_SHORT_BLOCK_DRYRUN  = False   # 🔴 ARMED ON ARRIVAL. This gate REFUSES ENTRIES.
```
Agreed on shipping armed: on the current book this fires on ~2 entries per 41 days. A DRYRUN twin would
produce its first observation somewhere around November, and the failure direction is safe by construction —
every fault admits. The DRYRUN flag exists for symmetry with `DXY_HALT_DRYRUN` and as the soft kill.

### 1e) DB status + attribution hook — AST-verified, not grepped
New status **`bull_daily_blocked`**, added to `skip_attribution.TRACKED_STATUSES` **in the same pass**, with
`_record_skip_attribution(...)` **called at the refusal site**, mirroring `flat_adx_blocked` (`main.py:4952`).

The AST walker I will gate the apply on already runs. Against the current tree it proves the walker works —
and it found something (see §4):

```
✅ ai_skipped        registered AND called (line 5298)     ✅ risk_halt        (4763)
✅ below_threshold   registered AND called (line 4685)     ✅ book_blocked     (5036)
✅ htf_blocked       registered AND called (line 4160)     ✅ flat_adx_blocked (4952)
```
After the patch this must also print `✅ bull_daily_blocked registered AND called`, or the apply aborts.

### 1f) Telegram card on refusal
```
📈 BULL DAILY REFUSED SHORT
💎 SOL/USDT:USDT @ <price>
daily trend = BULL — a short here is against the daily
<combo_key>
```
Names the daily label and the price, per spec.

### 1g) 🔴 THE CONFIG COMMENT — VERBATIM, AS YOU DICTATED IT

```python
# 🔴 DO NOT SHORT AGAINST A BULL DAILY (2026-09-17).
#
# this is DISCIPLINE, not a measured edge. n=2 on live (#32 -0.180R, #34 -0.643R,
# both losers), 0 of 13 on paper, and it cannot be proven at this sample. It exists
# because a bot that shorts while the daily trend points up is doing something a
# trader would not do. If a later pass measures it and finds no edge, that is the
# EXPECTED result and NOT grounds to remove it. Grounds to remove it are three and
# only three: it fires too often, it fires asymmetrically in a way the rule does
# not explain, or it refuses trades a trader would take.
```

---

## 2. WHAT IT WOULD HAVE DONE

### 2a) Replay — both books, never pooled

**LIVE — 2 of 10 shorts refused, ΣR −0.823:**

| # | opened | `trend_1d` | R | $ | close | outcome |
|---|---|---|---|---|---|---|
| 32 | 2026-08-10 15:15 | `bull` | **−0.180** | −$0.2663 | exit_signal | loser |
| 34 | 2026-08-13 16:40 | `bull` | **−0.643** | −$0.9113 | sl | loser |

**PAPER — 0 of 13 shorts refused.** No paper short ever carried a bull daily.

**LONGs touched: 0 of 9 live, 0 of 9 paper.** The gate is side-scoped and never evaluates a long.

### 2b) ✅ IT REFUSES NO WINNER
**Both refused trades are losers. Zero winners refused, in either book.** The condition that killed filter 21
on SOL and disarmed Titan's clause B does not arise here. No decision needed from you on this point.

### 2c) Refusal rate — and the denominator matters enormously

| denominator | bull-daily shorts | rate |
|---|---|---|
| **filled live shorts** (became positions) | 2 of 10 | **20.0%** |
| **labelled live-era SHORT consultations** | 469 of 739 | **63.5%** |
| labelled consultations, as share of ALL entry consultations | 469 of 1,505 | 31.2% |

### 2d) 🔴 PRE-REGISTERED RATE — AND YOUR ALARM IS ALREADY TRIPPED ON ONE READING

**Pre-registered: ~20% of shorts.** On *filled* shorts that is exact — **2 of 10 = 20.0%**.

**On consultations it is 63.5%, which exceeds your 50% alarm.** You wrote that crossing 50% *"is a finding
about the daily label, not about the rule."* It is, and here it is: **SOL's daily was labelled `bull` on 23 of
the 38 live-era days with signal rows.** A bull daily is the *modal* condition of the live era, so most short
signals naturally arrive under one.

**The two figures reconcile and the rule is not the problem.** Of the 469 bull-daily short consultations,
**467 were already refused by the AI advisor** (`ai_skipped`). Only 2 survived everything else and became
positions. So the gate's *marginal* effect — trades it newly refuses that would otherwise have executed — is
**2 of 10 = 20%**, exactly as pre-registered. The 63.5% measures how often the *condition* is true, not how
often the *gate* changes an outcome.

🔴 **Both numbers must be carried forward, and the review must use the marginal one.** I am re-stating the
pre-registration in unambiguous terms:

> **Pre-registered marginal rate: ~20% of shorts that would otherwise have executed (≈1 refusal per 20 entries,
> ≈2 per 41 days).**
> **Alarm: >50% of *executable* shorts refused** — that would mean the daily label had shifted regime or the
> gate had broadened. The 63.5% *condition* rate is expected and is not the alarm.

---

## 3. APPLY — 🔴 NOT DONE. STOPPED AT §3a.

Nothing in §3b, §3c or §3d was performed. No `.bak` written, no file edited, no AST diff taken, no restart, no
canon entry. **The book is not flat** (§ headline). Specifically **not** done:

* `.bak` of `config.py` / `main.py` / `skip_attribution.py` — **not written**
* the runtime-untouched proof over `SL_BUFFER_ATR`, `TRAIL_MULT_ATR`, `TRAIL_ARM_R`,
  `CONFLUENCE_SCORE_THRESHOLD`, `FLAT_ADX_GATE_DRYRUN`, all `BOOK_GATE_*`, `EXIT_ADVISOR_DRYRUN`,
  `MAX_POSITIONS_PER_SIDE`, `LIVE_FIXED_MARGIN`, `LEVERAGE`, six advisor prompt sha256s — **not taken**
  (it is a post-edit proof and there is no edit)
* restart, loaded-bytecode verification, boot line, post-restart `openitems_guard` — **not run**
* canon entry — **not written**

**Current state, verified now and unchanged from session start:**

| | |
|---|---|
| `mercury-sol.service` | `NRestarts=0`, PID 2245907, active since 2026-09-14 22:20:45 |
| `titan.service` | `NRestarts=0`, PID 1572470, active since 2026-09-12 14:58:32 |
| `FLAT_ADX_GATE_DRYRUN` | **True** — unchanged |
| `BOOK_GATE_DRYRUN` | **False** — unchanged |
| SOL `config.py` sha256 | `a308a130…149c7` — unchanged |

**The review point, stated in refusal rows as you asked — carried into the canon entry when this is applied:**

> **Review at 10 `bull_daily_blocked` rows, not at N days.** At the pre-registered marginal rate (~2 per 41
> days) that is roughly five months, and that is the honest horizon for a rule this rare. Review earlier only
> if one of the three named grounds trips.

---

## 4. 🔴 INCIDENTAL FINDING — 608 REFUSALS ARE BEING DROPPED RIGHT NOW

The AST walker built for §1e found the Titan half-fix **already live on SOL, in mirror image**: the hook is
called, the status is **not registered**, and the scope filter in `skip_attribution.on_skip` discards every row.

```
🔴 'entry_gate_refused' called at main.py:4740 but NOT in TRACKED_STATUSES
```

| status | `trades` rows (live era) | `skip_attribution` rows |
|---|---|---|
| ai_skipped | 1,481 | 1,481 ✅ |
| below_threshold | 1,675 | 1,675 ✅ |
| htf_blocked | 3,698 | 3,698 ✅ |
| risk_halt | 401 | 401 ✅ |
| book_blocked | 45 | 45 ✅ |
| flat_adx_blocked | 372 | 372 ✅ |
| **`entry_gate_refused`** | **608** | **0** 🔴 |

Every other status reconciles exactly 1:1. **608 live-era refusals have no drift tracking and cannot be judged
later** — the precise failure that cost Titan's FLAT floor 518 refusals for a month.

**I have not fixed it.** It is outside the rule you authorised, it is a separate change needing its own pass,
and the book is not flat. Reported for your decision.

---

## READ-ONLY CONFIRMATION

| check | state |
|---|---|
| `openitems_guard` | **exit 0**, run first |
| SOL DB | `file:…?mode=ro` + `PRAGMA query_only=1` (verified = 1). **No writes.** |
| SOL config | read via `ast.literal_eval` on source text. **Never imported.** |
| Venue | **GET only** — position/order reads, all 403-blocked; **no orders, no amends, no cancels** |
| Files written | **only** in the session scratchpad. **Nothing** under `mercury-sol/` was created or modified. |
| `NRestarts` | **0 / 0**, both bots — nothing restarted |
| **Titan** | **UNTOUCHED** — only `tools/openitems_guard.py` run, its own read-only self-check |
| Applied | **NOTHING.** The patch is specified and executed in isolation; it has not touched the bot. |
