# sol-1h-flip-aborted-first-consultation-landed

_2026-08-01 17:06 UTC_

---

# MERCURY-SOL — 🔴 THE 1H FLIP WAS **NOT** APPLIED. YOUR STOP CONDITION FIRED DURING APPLICATION.

**`AI_ADVISOR_HIDE_1H` is still `True`. The service was never restarted. The running worker never
held the flipped value at any moment.** Titan was not touched.

---

# THE ANSWER FIRST

You made the timing condition load-bearing and explicit:

> *"Do this before any consultation occurs, or not at all — if a consultation has landed by the
> time you read this, STOP and tell me."*

**It landed. Mid-application.**

| time (UTC) | event |
|---|---|
| **16:57:36** | Gate check #1 — consultations since restart = **0**. Condition satisfied. Proceeded. |
| 16:58:06 | `config.py` snapshotted (`config.py.bak_hide1h_flip_20260801`, md5 verified identical) and flipped `True → False`, comment rewritten with your three reasons |
| 16:58–17:00 | Pre-registration restated + freeze scope written into `OPEN-ITEMS-SOL.md` (before restart, as instructed) |
| **17:00:01** | 🔴 **row 14981 — a consultation lands**, under the interim 3-of-4 prompt |
| **17:00:4x** | Gate check #2, immediately before the restart — count = **1**. **Condition failed. Aborted.** |
| 17:0x | `config.py` restored byte-for-byte from the snapshot. **No restart was ever issued.** |

The window between the two checks was about **2½ minutes**, and the consultation fell inside it.
That is not a check I skipped — it is a race I re-checked for and caught. The re-check before the
irreversible step is the only reason this was caught at all.

**Nothing about the running system changed today after 16:17:51.** The flip existed only as text
on disk, for roughly two minutes, in a process that was never told to reload.

---

# §1 — WHY I REVERTED THE FILE RATHER THAN LEAVING IT STAGED

You said "or not at all", so the flip should not stand. But there is a second, sharper reason,
and it is the one that made me act rather than just stop:

**`mercury-sol.service` is `Restart=always`.** A flipped `config.py` sitting on disk under an
un-restarted worker is not a neutral paused state — it is a **primed change**. Any crash, any OOM
event, any unrelated `systemctl restart`, and the flip would have gone live **silently, mid-window,
with no report**. That is precisely the *"фикс на диске ≠ фикс в работе"* failure class, run in
reverse.

So the file is back to byte-identical:

```
ea033c86f5c844858ed230ec685cff32  config.py
ea033c86f5c844858ed230ec685cff32  config.py.bak_hide1h_flip_20260801
config.py  mtime 2026-08-01 15:31:35.897536492   ← restored, cp -p
config.py:449  AI_ADVISOR_HIDE_1H = True
```

`py_compile` clean. The snapshot `config.py.bak_hide1h_flip_20260801` is retained.

**Re-applying is one line plus a restart** whenever you say go. The comment text carrying your
three reasons is preserved verbatim in this report (§4) and in `OPEN-ITEMS-SOL.md`, so nothing
has to be re-derived.

---

# §2 — THE CONSULTATION THAT FIRED THE STOP — AND IT IS WORTH READING

Row **14981**, 2026-08-01 17:00:01. **This is the first production render of the new prompt**, and
it is a **disagreeing** case — exactly the population the experiment is about.

```
PROPOSED ENTRY: SHORT
Symbol: SOL/USDT:USDT
15m: HyperWave Signal Up (direction: LONG, set 15m ago)
5m trigger: Bearish I-BOS (direction: SHORT)
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 0.0773  |  Volume ratio 5m: 10.22x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 24.6 | 15m 27.5  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.363% | 15m 0.161% | 5m 0.106%
  EMA-gap: 1h 0.183% (Expanding) | 15m 0.079% (Expanding)  (Contracting/Flat = compression)
  Market regime: FLAT | MTF alignment score: 4
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: BEAR, ADX 12.0, EMA-gap 1.274% (Expanding)
  4h: BEAR, ADX 21.7, EMA-gap 0.568% (Expanding)
  1h: BEAR, ADX 24.6, EMA-gap 0.183% (Expanding)
  15m: BEAR, ADX 27.5, EMA-gap 0.079% (Expanding)
  5m: BEAR, ADX 30.2, EMA-gap 0.062% (Expanding)
  MTF alignment vs SHORT: 4/4 (4H/1H/15m/5m; excludes 1d)
Order book (pre-trade, 8000 levels):
  Mid: $72.63  |  Imbalance ±1%: 0.55 (bid-heavy)
  Massive bid walls (>4x avg vol): $72.75 (×10.0), $72.25 (×24.2), $71.75 (×5.2)
  Massive ask walls (>4x avg vol): $72.75 (×14.6), $73.25 (×7.6), $74.25 (×4.0)

Tier agreement vs SHORT (computed for this consultation):
  1H LuxAlgo tier: NOT SHOWN in this prompt — do NOT assume it agrees or opposes
  15m: HyperWave Signal Up -> LONG = OPPOSES
  5m trigger: Bearish I-BOS -> SHORT = AGREES
  Of the 2 tier(s) shown: 1 agree, 1 oppose, 0 neutral, 0 absent.
The cascade gate, the score gate and the risk gate have already passed. That is a separate hard gate on the 1H/15m/5m slots — it is NOT a statement that the tiers listed above agree with each other.
Decide whether the bot should execute this entry now.
```

Verdict stored: `skip`, confidence **0.92**, reason:

> *"15m HyperWave LONG opposes SHORT entry; massive bid wall (×24.2 at $72.25) blocks downside. Skip."*

**All four applied items are confirmed working in production, not just in a render:**
`PROPOSED ENTRY: SHORT` first line; `set 15m ago` on the 15m tier; the agreement block computing
`OPPOSES` / `AGREES` with a scope-naming tally; the false "3 timeframes are aligned" sentence gone
and the gates fact stated separately.

**One observation, flagged as an observation and nothing more.** Under the old prompt this row sits
in the population that ran **9.70% wrong-side**; here the model named the tier and the trade side
**correctly** ("15m HyperWave LONG opposes SHORT entry" — LONG tier, SHORT trade, both right), and
it borrowed the agreement block's own word *opposes*. That is **n=1**. It is not evidence, it does
not move the prediction, and I am recording it only because it is the first data point and it
should be in the record before anyone is tempted to describe it later as if it had been predicted.

---

# §3 — WHAT THIS DOES TO THE MEASUREMENT WINDOW

This is the substantive consequence, and it is why your condition existed.

- **The window in force is the 16:18 pre-registration on the interim 3-of-4 form.**
- **Its counter is now 1 of 200**, not 0.
- Had the flip proceeded, the 200 would have **straddled two prompt forms** — one consultation on
  the interim form, 199 on the final one — and the "nothing is pooled across forms" claim I had
  already written to disk would have been **false**. Your condition prevented exactly that.

**Your options, stated neutrally:**

1. **Flip anyway and restart the 200 from zero**, discarding row 14981 from the count and noting
   it as a single orphan observation under a superseded form. Costs one data point; keeps the
   window clean and on the final prompt form. **This is the only option that gets the 1H tier into
   the measured form.**
2. **Flip anyway and accept a 1/200 straddle**, recorded honestly as a caveat. Cheapest, but it
   puts a known impurity into the very experiment built to be falsifiable — and the pooling is on
   the *pre-change* side, which is the worse side for it to be on.
3. **Do not flip. Run the 200 on the interim 3-of-4 form**, then decide about the 1H afterwards
   with the result in hand. Slowest, cleanest, and it keeps the 1H flip as a separately
   attributable change measurable on its own.

I am not choosing among these. Option 1 or 3 both keep the experiment sound; **option 2 is the one
I would argue against**, because it trades the experiment's integrity for a single data point.

---

# §4 — THE REASONING, PRESERVED SO IT NEED NOT BE RE-DERIVED

Your decision stands on its merits regardless of the timing; only the execution is pending. It is
recorded in `OPEN-ITEMS-SOL.md` and reproduced here. This is the comment that was written into
`config.py:444-470` and then reverted with the file:

1. **The old rationale does not survive its own premise.** *"The 1H is the hard cascade gate's
   domain, the advisor must not re-litigate it"* — but the **15m and 5m tiers are also cascade
   gates and they ARE shown, with directions.** Hiding only the 1H is an inconsistency, not a
   principle. And the advisor already re-litigates the cascade: **it refuses 97.7% of everything
   the cascade passes.** The boundary the flag protected does not exist.
2. **Parity is restored, not broken.** Titan's entry advisor **does** see which signal set its 1H
   tier (titan `f0a8d30` — identity as a fact, no statistics attached). The mechanism differs; the
   information does not.
3. **It is safe because the OHLCV block already prints the 1H MARKET direction.** The flip adds
   **which LuxAlgo signal set the tier** — identity, not a second vote. **No statistic, win rate or
   historical performance is attached to any signal name.**

---

# §5 — CONFIRMED: NO CODE CHANGE IS NEEDED FOR THE FLIP

Verified before reverting — all three consumption points already branch on the flag, so flipping
the constant is genuinely sufficient:

| `claude_advisor.py` | what it does when the flag goes `False` |
|---|---|
| **line 355** — `if not AI_ADVISOR_HIDE_1H:` | emits the **1H line** into `_lux_lines`, and it already calls `_slot_age(_h1)` — so the 1H gets **name, direction and age** with no edit |
| **line 468** — `_shown = ([('1H', _h1)] if not AI_ADVISOR_HIDE_1H else []) + [('15m', _m15), ('5m trigger', _m5)]` | the 1H **enters the tally** and gets its own AGREES / OPPOSES / NEUTRAL / ABSENT verdict; the "Of the N tier(s) shown" count becomes **3** |
| **line 479** — `_hidden_1h = ("  1H LuxAlgo tier: NOT SHOWN…" if AI_ADVISOR_HIDE_1H else "")` | the disclaimer **disappears automatically** — it is emitted only while the flag is True |

**One hazard found while checking, worth knowing before any future flip.**
`claude_advisor.py:29-32`:

```python
try:
    from config import AI_ADVISOR_HIDE_1H
except ImportError:   # pragma: no cover — defensive: behave like Titan's default
    AI_ADVISOR_HIDE_1H = True
```

The defensive fallback **defaults to `True`**. It fires only on `ImportError` (module or name
missing), so it cannot mask a flip of an existing name — but it does mean that if `config.py` were
ever broken or the name renamed, the 1H would **silently re-hide** rather than fail loudly. Not a
defect today; a thing to verify empirically **after** any future flip rather than assume. **When
the flip is eventually applied, the value must be confirmed from a rendered production prompt, not
from the file.**

---

# §6 — STATE VERIFICATION (all re-checked after the revert)

| check | result |
|---|---|
| `AI_ADVISOR_HIDE_1H` | **`True`** (`config.py:449`) — original value, original comment |
| `config.py` md5 vs snapshot | **identical** (`ea033c86f5c844858ed230ec685cff32`) |
| `config.py` mtime | **15:31:35** — restored, as if never edited |
| **Restarts since 16:00** | **1** (`Booting worker` count) — the 16:17:51 one. **No restart was issued today by me.** |
| Worker | **pid 1112227, forked Sat Aug 1 16:18:13** — the same process throughout |
| Service | **active (running)** |
| `OBSERVATION_MODE` | **True** — proven live by `[VIRTUAL] poller started in pid 1112227`, whose alternative branch prints `poller not started (live mode)` and returns. **SOL is PAPER.** Unchanged: the process never restarted, so the boot-time proof still describes the running worker. |
| 15:38 changes still loaded | **yes** — `config.py` (15:31:35), `main.py` (15:31:54), `virtual_trader.py` (15:34:21), `claude_advisor.py` (16:15:42) all predate the 16:18:13 fork and none were modified since (config.py's edit was reverted to byte-identical) |
| Open positions | **0** (`closed 18`, none open) |
| Consultations since restart | **1** (row 14981) |
| **Tor → Bybit** | ✅ `{"retCode":0,"retMsg":"OK","timeSecond":"1785603896"}` |
| **OKX book** | ✅ live, mid ≈ **$72.725** |
| `py_compile` | **OK** on `config.py`, `claude_advisor.py` |

**Titan — untouched:**

| check | result |
|---|---|
| `git status --short` | **clean** (no output) |
| `HEAD` | **`3316e8a`** |
| `titan.service` | **active** |
| `.py` files modified since 16:00 under `/root/titan-bot` | **none** |

No Titan file was read for parameters and none was written.

---

# §7 — DOCUMENT STATE, CORRECTED

`OPEN-ITEMS-SOL.md` had the restated pre-registration and the freeze written into it **before**
the gate failed. Rather than delete them — which would hide that they were ever written — they are
struck through and marked **NOT IN FORCE**, with the reason:

- The **17:00 restatement** is marked ⛔ **WITHDRAWN**, and states plainly that the flag is still
  `True`, no flip happened, no restart happened, and the **16:18 pre-registration remains the one
  in force at 1 of 200**.
- The **freeze** is marked ⛔ **not yet in force**, but its **scope definition is retained
  deliberately** — frozen = everything the advisor reads (entry user prompt, entry system prompts,
  model id, sampling params, and every input feeding them, plus `AI_ADVISOR_HIDE_1H` itself and
  the wall-rule selection); not frozen = logging, labels, storage, the exit side, the cascade, the
  gates, the optimizer, the excursion sampler, the observatory. The **finish-the-window-and-caveat**
  rule (never reset the counter on a finding, per Titan §2.4-OP) is recorded with it. The
  definition is good and should not have to be re-litigated.
- **Item 3 is back to 🔴 not applied, awaiting the operator** — with your authorisation and its
  reasoning recorded as valid and pending, so nobody re-derives the overruled rationale and treats
  it as unchallenged.
- The footer reflects 17:06 and points at this file.

Note the freeze scope arguably **already applies** to the interim form, since the 16:18 window is
live at 1/200: the entry prompt should not be edited while that stands either, whichever option
you pick in §3.

---

# WHAT I NEED FROM YOU

**§3 — options 1, 2 or 3.** The flip is one line and a restart; everything needed to apply it is
snapshotted, written down, and verified to need no code change. I stopped because you told me the
timing was the condition, and it failed by roughly ninety seconds.
