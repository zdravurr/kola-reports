# titan-three-signal-tiers-diagnosis-and-patch-awaiting-approval

_2026-07-29 11:24 UTC_

---

> ⚠️ **NOTHING IS APPLIED. STOPPED FOR APPROVAL, as instructed.** `git status` clean, HEAD still
> `8b15ecc`, `main.py` and `claude_advisor.py` byte-identical to HEAD, `titan.service` running the
> old code, **no restart performed**. The patch was written and executed in an isolated copy under
> `/tmp/.../patch/b/`; every preview below is real output from that copy running against the **live**
> state machine and matrix, read-only. Item 13 (live verify after restart) is the one thing I have
> not done, because it cannot be done without applying.

---

# PART 1 — DIAGNOSIS

## 1.1 The trace, end to end

```
TradingView webhook (tf=15m)
   └─ main.py:60  _TF_TO_ACTION['15m'] = 'process_signal'
        ├─ PLAIN-TEXT path  main.py:1587   state_machine.update_slot('15m_confirm', direction, signal_name)
        └─ JSON path        main.py:3183   state_machine.update_slot('15m_confirm', direction or 'NEUTRAL', signal_name)
   └─ state_machine.py:206  update_slot()  → market_state['15m_confirm']['signal_name'] = signal_name   ✅ stored
   └─ state_machine.py:182  _persist_slot_locked()  → market_state_snapshot(signal_name)                ✅ persisted
   └─ state_machine.py:159  _restore_from_snapshot() → signal_name restored on boot                     ✅ survives restart
   └─ state_machine.py:414  set_trigger_and_snapshot() → snap['15m_confirm']['signal_name']             ✅ in the snapshot
   └─ claude_advisor.py:262 f"15m: {m15.get('signal_name') or 'n/a'} …"                                 ← prints n/a
```

**It is NOT a write gap.** Every hop stores and returns the name. Proof from the live bot right now:

```
1h_context   dir=LONG     name='Smart Trail Bullish'    ts=2026-07-29T08:00:14Z
15m_confirm  dir=SHORT    name='HyperWave Signal Down'  ts=2026-07-29T11:00:08Z
5m_trigger   dir=SHORT    name='Bearish OB Mitigated'   ts=2026-07-29T11:00:17Z
```

**And it is not a simple read gap either.** The builder reads the right field of the right object.
The tier is genuinely **EMPTY** at those moments. Two mechanisms, both verified:

### 🔴 (a) The slot is WIPED between confirmation and trigger

`state_machine._clear_lower_tfs_locked()` (line 225) blanks `15m_confirm` and `5m_trigger` on **any**
1H direction flip **or** Group-B / Exit Signal. `reset_1h_trend()` (line 277) calls it.

**Proven on entry 19021 (vpos 83)** — every row in the window:

| time (UTC) | row | what it did |
|---|---|---|
| 2026-07-27 23:00:16 | `1h_trend_set` | **Trend Catcher Down** → 1H = SHORT |
| 2026-07-27 23:30:03 | `15m_confirm` | **Reversal Up** → 15m slot = LONG |
| **2026-07-28 00:00:29** | **`60m_exit` "Exit Signal", status `trend_reset`** | **`reset_1h_trend()` → 1H set to NEUTRAL, `_clear_lower_tfs_locked()` WIPES the 15m slot** |
| 2026-07-28 01:00:17 | `open_short` **executed** | slot empty → prompt prints `15m: n/a (direction: n/a)` |

**Entry 19214 (vpos 84)**: 15m confirms at 14:30 (`HyperWave Signal Up`, `Bullish Divergence`), then
the 1H **flipped** to LONG at 16:00:33 — wiping them — and the entry fired at 17:00.

### 🔴 (b) The entry survives an empty tier because the gate does not need the slot

`confluence_check()` — which does require a non-NEUTRAL 15m — is called from **exactly one place**,
`main.py:1782`, the **plain-text** path. The JSON path never calls it; it uses `_htf_cascade_gate` →
`signal_matrix.htf_alignment`, and **`HTF_TOLERATE_NEUTRAL = True`** (`config.py:259`) means a
NEUTRAL/absent tier no longer vetoes — only an **opposite** tier does.

> So the premise "the cascade knows the direction, this is pure plumbing" holds **only on the
> plain-text path**. On the JSON path the 15m tier can be legitimately absent at entry time, and the
> honest fix is to print **ABSENT**, not to invent a value. That is item 10, and it is the correct
> answer rather than a workaround.

### 🔴 (c) TWO REGISTRIES HOLD THE SAME FACT AND DISAGREE — in both directions

| | `state_machine` 15m slot | `signal_matrix` MOMENTUM |
|---|---|---|
| TTL | **4 h** (`market_state`) | **90 min** (`CATEGORY_TTL_MINUTES`, cut from 240 on 2026-05-20) |
| cleared by 1H flip / Exit | **YES** | **NO** |
| read by | the **prompt** | the **score gate** and the HTF cascade |

Measured over the last 20 executed entries:

- **2 entries** (15510, 17895) — slot **empty** while the matrix held **3 live MOMENTUM signals**.
  The prompt said `n/a`; the gate had counted three.
- **6 entries** (13739, 14451, 16399, 17092, 18108, 18699) — slot **live** while matrix MOMENTUM
  had already expired to NEUTRAL. The prompt showed a 15m the gate did **not** count.

Neither store alone is the whole truth. **That is why the fix prints both.**

## 1.2 Why 5 of 12 and not 12 of 12

Not a different code path, not a signal family, not a race, not slot expiry. It is **whether a 1H
flip or a Group-B Exit Signal landed between the last 15m confirmation and the 5m trigger.** Those
events wipe the slot; nothing refills it until the next 15m alert, and the 15m stream fires roughly
every 30–90 min while the 5m trigger can arrive at any moment.

**This decides the question you asked: it is neither a one-line fix nor a redesign.** There is no
line to move, because nothing was dropped in transit — the value is genuinely gone. The fix is a
*source* change (render from both authorities) plus honest vocabulary (`ABSENT`, explicit agreement).

## 1.3 All three tiers across the last 20 executed entries

| id | when | side | 1H in prompt | 15m in prompt | 5m in prompt | matrix count T/M/L/E |
|---|---|---|---|---|---|---|
| 13170 | 07-04 18:00 | LONG | **line absent** | HyperWave Signal Up | Within Bullish OB | 3/1/1/1 |
| 13353 | 07-05 09:45 | SHORT | **line absent** | Reversal Down | Bearish S-CHOCH+ | 0/2/2/4 |
| 13526 | 07-05 22:35 | LONG | **line absent** | HyperWave Signal Up | Within Bullish OB | 0/1/1/1 |
| 13641 | 07-06 12:00 | SHORT | **line absent** | **n/a** | Bearish OB Created | 1/**0**/0/1 |
| 13739 | 07-06 21:10 | LONG | **line absent** | HyperWave Signal Up | Bullish OB Created | 3/2/1/1 |
| 14407 | 07-09 21:10 | LONG | **line absent** | **n/a** | Bullish OB Created | 1/**0**/1/1 |
| 14451 | 07-10 01:50 | LONG | **line absent** | HyperWave Signal Up | Bullish S-BOS | 1/2/3/3 |
| 14999 | 07-11 14:25 | LONG | **line absent** | HyperWave Signal Up | Bullish S-BOS | 1/1/0/2 |
| 15026 | 07-11 17:35 | LONG | **line absent** | HyperWave Signal Up | Bullish OB Created | 2/2/3/2 |
| 15510 | 07-13 05:05 | SHORT | **line absent** | **n/a** | Bearish I-BOS | 1/**3**/3/4 |
| 15921 | 07-14 21:35 | LONG | **line absent** | HyperWave Signal Up | Bullish OB Created | 1/1/1/2 |
| 16302 | 07-17 02:40 | SHORT | **line absent** | HyperWave Signal Down | Within Bearish OB | 3/1/0/1 |
| 16399 | 07-17 13:10 | SHORT | **line absent** | HyperWave OB Signal Down | Within Bearish OB | 1/2/1/2 |
| 17092 | 07-20 00:15 | LONG | **line absent** | HyperWave Signal Up | Bullish OB Created | 2/2/1/3 |
| 17241 | 07-20 15:45 | LONG | **line absent** | HyperWave Signal Up | Bullish S-CHOCH | 3/1/0/2 |
| 17895 | 07-23 18:00 | SHORT | **line absent** | **n/a** | Within Bearish OB | 1/**3**/1/1 |
| 18108 | 07-24 11:00 | SHORT | **line absent** | HyperWave Signal Down | Bearish OB Created | 1/3/2/3 |
| 18699 | 07-26 15:40 | LONG | **line absent** | HyperWave Signal Up | Bullish OB Created | 4/**0**/1/3 |
| 19021 | 07-28 01:00 | SHORT | Trend Catcher Down (no direction) | **n/a** | Within Bearish OB | 1/**0**/1/1 |
| 19214 | 07-28 17:00 | LONG | Bullish Confirmation (no direction) | **n/a** | Bullish OB Mitigated | 2/**0**/2/2 |

**15m is NOT the only leaky tier — it is the least leaky of the three.**

| tier | state in the prompt |
|---|---|
| **1H** | **absent on 18 of 20.** The identity line only exists since `f0a8d30` (2026-07-27); before that `AI_ADVISOR_HIDE_1H` suppressed the tier entirely. Even now it carries **no direction** and no agreement. |
| **15m** | `n/a` on 6 of 20 (14 of all 59 executed entries ever). |
| **5m** | present on **59 of 59**. Never leaked. |

## 1.4 Direction — is it present and correct where a name exists?

Where the 15m name is present, its direction is present and **matches the executed side 14 / 14**.
That part was never broken. Two other things are:

- **The matrix disagreed in 6 of those 14** (`matrix_MOMENTUM = NEUTRAL` while the slot said
  LONG/SHORT) — §1.1(c).
- **The 1H tier prints a name with NO direction at all.** On entry 19021 the prompt read
  `1H trend set by: Trend Catcher Down, weight 1.0, set 1.0h ago` for a tier an Exit Signal had
  **reset to NEUTRAL 60 minutes earlier**. The advisor was shown a dead tier as live. A name without
  a direction is exactly the "half a fix" you named.
- **The age was wrong too.** `reset_1h_trend()` overwrites `timestamp` with the reset time while
  keeping the old name, so "set 1.0h ago" was the age of the **reset event**, not of
  *Trend Catcher Down* (which had fired 2.0h earlier, 23:00:16).

## 1.5 How far back — git-dated

| fact | commit | date |
|---|---|---|
| the `15m: … (direction: …)` prompt line | `b9a2935` | **2026-05-16** — the isolation refactor, i.e. the whole recorded history of this file |
| `_clear_lower_tfs_locked()` | `b9a2935` | **2026-05-16** — same |
| `HTF_TOLERATE_NEUTRAL = True` | `f911d51` | **2026-05-20** |

**Always — not a regression.** But the *symptom on executed entries* is dateable precisely:

- **0 of the 4** entries executed **before** 2026-05-20 show `15M:None`.
- **14 of the 55** executed **after** it do — earliest 2026-05-26, most recent 2026-07-28.

`f911d51` is what made an absent tier survivable, so it is the commit that turned a latent
rendering weakness into a live one. Nothing shipped this week caused or worsened it.

---

# PART 2 — THE FIX (written, tested offline, NOT applied)

## What it does, against your 8 requirements

| # | requirement | how |
|---|---|---|
| 6 | name + direction from the **authoritative source** | new `signal_tiers.build()` reads the state-machine snapshot object directly (`set_trigger_and_snapshot`'s own locked view) **and** `matrix_result`. Nothing re-derived, nothing parsed from text. |
| 7 | **weight** the bot itself used | `signal_matrix.classify(name)[3]` — the same number the matrix scored with. |
| 8 | **age** | slot `timestamp`, rendered `last set 22m ago` / `3.2h ago`. Labelled **"last set"**, not "fired": `reset_1h_trend()` overwrites the timestamp, so "fired at" would be a lie for reset tiers. Fixing that properly needs a separate `set_at` field in `state_machine` — **deliberately not done**, it is cascade state and out of your scope line. |
| 9 | **5m tier kind** | `EXECUTION` → `trigger-capable`; anything else → `context-only (carries weight, cannot trigger)`. Confirmed against the dictionary: **22 EXECUTION + 10 LIQUIDITY = 32 Price Action signals**, exactly your split. This is the bot's own routing rule, not a new list. |
| 10 | **agreement stated**, `absent` never `n/a` | one explicit `Agreement:` line; the literal string `n/a` can no longer be produced for a tier (asserted in test). |
| 11 | **exit side reads the same source** | new `trades.entry_tiers_json` column written at entry; `_entry_signals_for()` reads it instead of regex-parsing `ai_user_prompt`. Legacy rows keep the old parse, clearly labelled. |
| 12 | **identity only, no judgement** | name, direction, weight, age, gate-counted, trigger-capable. No win rate, no PnL, no performance. Verified by reading the rendered block below. |

**One defect I found in my own patch and fixed before showing it to you:** the "the score gate
counted this tier as LONG" clause **leaked the 1H direction that `AI_ADVISOR_HIDE_1H` exists to
hide**. It is now stripped for the 1H tier only; 15m and 5m keep theirs. Re-verified — see the live
render below.

## Before / after on the real failing entry (19021, vpos 83)

**What was actually sent:**

```
  1H trend set by: Trend Catcher Down, weight 1.0, set 1.0h ago
  15m: n/a (direction: n/a)
  5m trigger: Within Bearish OB (direction: SHORT)
  ...
  The 3 timeframes are aligned (confluence has already passed).
```

**What the patch sends** (replayed with that entry's real matrix breakdown and the slot state proven
in §1.1(a)):

```
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  Trend Catcher Down  (NEUTRAL, weight 1.0, last set 60m ago, but the score gate counted this tier as SHORT — slot and matrix disagree)
  15m: ABSENT — no 15m signal is held by the state machine at this moment
  5m:  Within Bearish OB  (SHORT, weight 0.7, last set 0m ago, trigger-capable)
  Agreement: 5m points SHORT; vs the proposed SHORT: 5m agree; 1H NEUTRAL (reset, not in force); 15m ABSENT.
```

The old prompt asserted three aligned timeframes. The truth was **one**.

## Live render through the full patched path (API call stubbed, live slots + live matrix)

```
Symbol: BTC/USDT:USDT
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  Smart Trail Bullish  (direction withheld (AI_ADVISOR_HIDE_1H), weight 0.9, last set 3.3h ago)
  15m: HyperWave Signal Down  (SHORT, weight 0.7, last set 17m ago)
  5m:  Bearish OB Mitigated  (SHORT, weight 0.5, last set 17m ago, trigger-capable, NOT counted by the gate — matrix TTL expired)
  Agreement: 15m and 5m both point SHORT; vs the proposed SHORT: 15m+5m agree.
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 67.6940  |  Volume ratio 5m: 0.54x avg
...
The entry gate has already passed. Tier agreement is stated in the SIGNAL TIERS block above — read
it there rather than assuming all three agree. Decide whether the bot should execute the DCA entry now.
```

## Exit-side entry-thesis block, from the same structured record

```
  1H:  Smart Trail Bullish  (LONG, weight 0.9, set 3.2h ago at entry)
  15m: HyperWave Signal Down  (SHORT, weight 0.7, set 14m ago at entry)
  5m:  Bearish OB Mitigated  (SHORT, weight 0.5, set 14m ago at entry)
  Agreement at entry: 1H points LONG; 15m+5m point SHORT; vs the proposed SHORT: 15m+5m agree, 1H OPPOSE.
```

## Checks already run on the patch

- `py_compile` clean on both files, **no SyntaxWarnings**.
- All-tiers-absent case renders three `ABSENT` lines and
  `Agreement: No tier currently holds a directional signal.`
- `'n/a'` appears in **no** tier line, in either the populated or the empty case.
- Tier facts JSON round-trip cleanly (824 bytes on live state).
- `AI_ADVISOR_HIDE_1H` honoured: no 1H direction reaches the prompt, including via the gate clause.
- The third `update_signal_execution` call site (P3, `main.py:4107`) was **reverted** — `_tiers_json`
  does not exist on that path and would have raised `NameError`. Only the two real entry paths write
  the column.

## What I did NOT touch

`confluence_check` · `_htf_cascade_gate` · `htf_alignment` · the score gate and both thresholds ·
`market_regime` · SL / trail / breakeven · the LONG partial · `reset_1h_trend` /
`_clear_lower_tfs_locked` · TTLs · Mercury-SOL. Zero diff lines in any of them.

---

# 🔴 AWAITING YOUR APPROVAL

Nothing is applied. On your word I will: copy the three files in, restart `titan.service`, then
deliver **item 13** — a real rendered entry prompt from the first live decision with all three tiers
complete, the exit advisor's entry-thesis line for the open position (vpos 84) naming all three, and
a check that no tier can render `n/a`.

**One thing to decide, because it is a genuine judgement call and not mine to make:** for entries
where a tier is truly absent, the prompt will now say so plainly and the agreement line will report
only one or two tiers. That is the truth, but it is *new information* the advisor has never had, and
it may change its verdicts. It is still identity-only — no statistic is attached — but you should
know it is a behavioural change to the advisor's inputs, not a cosmetic one.

---

# THE COMPLETE PATCH

```diff
--- a/claude_advisor.py	2026-07-29 11:11:03.983623293 +0000
+++ b/claude_advisor.py	2026-07-29 11:17:25.411667809 +0000
@@ -241,7 +241,8 @@
                       ls_ratio=None, pre_trade_walls=None,
                       atr_5m=None, vol_ratio_5m=None,
                       vol_snap=None, market_regime=None,
-                      mtf_alignment_score=None, book_pct=None):
+                      mtf_alignment_score=None, book_pct=None,
+                      matrix_result=None):
     """Ask Claude whether to take the entry. snapshot is state_machine
     .get_snapshot() output (1h_context / 15m_confirm / 5m_trigger keys).
 
@@ -253,61 +254,59 @@
       book_pct        — dict from main._entry_book_pct(): the percentile of each
                         order-book figure within the orderbook_density baseline.
                         Pure CALIBRATION — no statistic or outcome attached.
+      matrix_result   — signal_matrix.compute_score() output. Used ONLY so the
+                        tier block can state whether the score gate counted each
+                        tier; it decides nothing here.
+
+    Also returns result['signal_tiers'] — the structured tier facts, so the
+    caller can persist them and the EXIT advisor can read the same authoritative
+    record instead of parsing this prompt back out of the database.
 
     Returns a dict with: decide ('execute'|'skip'|'unavailable'),
     confidence (float), reason (str), raw (str or None).
     """
-    h1 = snapshot.get('1h_context') or {}
-    m15 = snapshot.get('15m_confirm') or {}
     m5 = snapshot.get('5m_trigger') or {}
     user = f"Symbol: {symbol}\n"
-    # 1H higher-timeframe line is suppressed from the entry advisor's view when
-    # AI_ADVISOR_HIDE_1H is True (config). This changes ONLY the prompt text —
-    # the hard _htf_cascade_gate (main.py) still uses 1H independently, the
-    # signal matrix is unchanged, and 1h_context stays in the snapshot.
-    if not AI_ADVISOR_HIDE_1H:
-        user += f"1H: {h1.get('signal_name') or 'n/a'} (direction: {h1.get('direction') or 'n/a'})\n"
-    # 1H SIGNAL IDENTITY (2026-07-27). The prompt already carries the 1H tier in
-    # substance — the 5-TF OHLCV block below prints "1h: BULL, ADX 16.9" — but never
-    # WHICH LuxAlgo alert set the trend. Bearish Confirmation+ and Trend Catcher Up
-    # therefore reach the model identically, though they are different signals.
+    # ── THE THREE SIGNAL TIERS ────────────────────────────────────────────
+    # 2026-07-29, OPEN-ITEMS §2.8. This block REPLACES three loose lines that
+    # rendered the 1H identity, the 15m confirmation and the 5m trigger
+    # separately and inconsistently:
+    #   * the 15m line printed "n/a (direction: n/a)" on 14 of 59 executed
+    #     entries — directly above the sentence claiming all three were aligned;
+    #   * the 1H line (f0a8d30) printed a signal NAME with no direction, so a
+    #     tier that an Exit Signal had reset to NEUTRAL still read as live
+    #     (entry 19021: 1H neutralised 00:00:29, prompt at 01:00:17 still said
+    #     "1H trend set by: Trend Catcher Down");
+    #   * nothing said whether the three agreed — the model had to infer it.
     #
-    # This is a FACT, not a judgement. The line carries the signal name, its matrix
-    # category weight and how long ago it fired. It deliberately carries NO win rate,
-    # NO PnL, NO historical performance: the largest per-signal cell in the book is
-    # n=6, and several hypotheses died on exactly that sample size today. The model
-    # learns WHICH signal fired, never whether that signal is good. Attaching a
-    # statistic is a separate decision needing its own validation and its own n.
+    # Everything below comes from `snapshot`, which IS the state machine's own
+    # locked view (set_trigger_and_snapshot), plus `matrix_result`, which IS
+    # what the score gate counted. Nothing is re-derived and nothing is parsed
+    # out of text. See signal_tiers.py for why both sources are needed.
     #
-    # Relationship to AI_ADVISOR_HIDE_1H (a8a6989, 2026-05-25): that flag hides the 1H
-    # LuxAlgo direction line so the advisor does not re-weigh a tier the hard HTF
-    # cascade has already gated. Identity is not direction — the cascade veto is
-    # unchanged, the matrix is unchanged, and the OHLCV 1h state has been visible to
-    # the advisor since 882cd7c (2026-05-29) regardless of this flag.
-    _h1_name = h1.get('signal_name')
-    if _h1_name:
-        _w = ""
-        try:
-            from signal_matrix import classify as _mclassify
-            _cl = _mclassify(_h1_name)
-            if _cl:
-                _w = f", weight {_cl[3]:.1f}"
-        except Exception:
-            pass
-        _age = ""
-        try:
-            _ts = h1.get('timestamp')
-            if _ts:
-                _dt = datetime.fromisoformat(_ts)
-                if _dt.tzinfo is None:
-                    _dt = _dt.replace(tzinfo=timezone.utc)
-                _age = f", set {(datetime.now(timezone.utc) - _dt).total_seconds() / 3600:.1f}h ago"
-        except Exception:
-            pass
-        user += f"1H trend set by: {_h1_name}{_w}{_age}\n"
+    # AI_ADVISOR_HIDE_1H (a8a6989) still governs the 1H *direction*: the flag
+    # exists so the advisor does not re-weigh a tier the hard HTF cascade has
+    # already gated. Identity, weight and age are shown either way — that is the
+    # line f0a8d30 drew and this block keeps it.
+    import signal_tiers
+    _tier_facts = signal_tiers.build(
+        snapshot, matrix_result,
+        proposed_direction=(m5.get('direction') if m5 else None))
+    if AI_ADVISOR_HIDE_1H:
+        _h1 = (_tier_facts.get('tiers') or {}).get('1H')
+        if _h1 and _h1.get('present'):
+            _h1['direction'] = 'direction withheld (AI_ADVISOR_HIDE_1H)'
+            # The gate-direction field would otherwise LEAK the very direction
+            # this flag exists to hide ("...the score gate counted this tier as
+            # LONG"). Strip it for the 1H tier only; 15m/5m keep theirs.
+            _h1.pop('gate_direction', None)
+            if _h1.get('counted_by_gate') is False:
+                _h1['counted_by_gate'] = None
+            _tier_facts['agreement'] = signal_tiers._agreement(
+                {k: v for k, v in _tier_facts['tiers'].items() if k != '1H'},
+                _tier_facts.get('proposed_direction'))
+    user += signal_tiers.render(_tier_facts)
     user += (
-        f"15m: {m15.get('signal_name') or 'n/a'} (direction: {m15.get('direction') or 'n/a'})\n"
-        f"5m trigger: {m5.get('signal_name') or 'n/a'} (direction: {m5.get('direction') or 'n/a'})\n"
         f"Combo weight: {weight:.2f} (1.0 baseline; <1 = historical loser, >1 = winner)\n"
     )
     # Volatility / volume context
@@ -399,9 +398,15 @@
     # History: 2026-06-27 introduced · 2026-07-26 gated on trend_1d != bull (596fbdf)
     # · 2026-07-26 retired (this commit). See project_counter_trend_ema1h_study and
     # kola-reports/reports/2026-07-26-1732-r5-gate-applied-and-cohort-rederived.md
+    # The old text asserted "The 3 timeframes are aligned (confluence has
+    # already passed)". That is not always true: HTF_TOLERATE_NEUTRAL (f911d51)
+    # lets an absent or NEUTRAL tier through, so this sentence was printed
+    # directly above "15m: n/a" on 14 executed entries. Replaced with a factual
+    # statement; the tier block above already says exactly what agreed.
     user += (
-        "\nThe 3 timeframes are aligned (confluence has already passed). "
-        "Decide whether the bot should execute the DCA entry now."
+        "\nThe entry gate has already passed. Tier agreement is stated in the "
+        "SIGNAL TIERS block above — read it there rather than assuming all "
+        "three agree. Decide whether the bot should execute the DCA entry now."
     )
     result = _call(_ENTRY_SYSTEM, user)
     decide = (result.get('decide') or '').lower().strip()
@@ -415,6 +420,7 @@
     result['system_prompt'] = _ENTRY_SYSTEM
     result['user_prompt'] = user
     result['model'] = MODEL
+    result['signal_tiers'] = _tier_facts
     return result
 
 
@@ -468,10 +474,8 @@
         f"  Volume:   {g('volume_now')}\n\n"
         "Recent 5m structure (CONTEXT ONLY — never a trigger)\n"
         f"  {g('structure_5m')}\n\n"
-        "ENTRY THESIS — the signals that opened this position\n"
-        f"  1H trend set by:   {g('sig_1h')}\n"
-        f"  15m confirmed by:  {g('sig_15m')}\n"
-        f"  5m triggered by:   {g('sig_5m')}\n"
+        "ENTRY THESIS — the exact tiers that opened this position\n"
+        f"{ctx.get('entry_tier_block') or '  (tier record unavailable for this position)'}\n"
         f"  Advisor's reason at entry: {g('entry_thesis')}\n\n"
         f"Consultation trigger: {g('trigger')}\n\n"
         "The stop and trail remain active if you HOLD. Judge whether THAT specific "
--- a/main.py	2026-07-29 11:11:03.983623293 +0000
+++ b/main.py	2026-07-29 11:14:10.371560866 +0000
@@ -239,6 +239,10 @@
             ('macro_news_source',   'TEXT'),  # CryptoPanic / RSS source name
             ('macro_confidence',    'REAL'),  # macro classifier self-confidence 0.0-1.0 (collection-only)
             ('macro_gate_penalty',  'REAL'),  # total_gate_adj applied at entry gate
+            ('entry_tiers_json',    'TEXT'),  # 2026-07-29: the three signal tiers as
+                                              # captured at entry from the state-machine
+                                              # snapshot + matrix. The EXIT advisor reads
+                                              # THIS, instead of parsing ai_user_prompt.
             # Batch tracking — optimizer groups trades by batch for learning
             ('batch_number',        'INTEGER'),
             # market regime label (TREND/FLAT) from signal_matrix.compute_score,
@@ -1943,7 +1947,13 @@
         market_regime=matrix_result.get('market_regime'),
         mtf_alignment_score=indicators.mtf_alignment_score(_snap, direction),
         book_pct=_entry_book_pct(pre_trade_walls),
+        matrix_result=matrix_result,
     )
+    _tiers_json = None
+    try:
+        _tiers_json = json.dumps(advice.get('signal_tiers') or {})
+    except Exception as _e:
+        print(f"[ENTRY-TIERS] serialise failed: {_e}", flush=True)
     ai_decide = advice.get('decide')
     ai_conf = float(advice.get('confidence') or 0.0)
     ai_reason = (advice.get('reason') or '')[:200]
@@ -2117,6 +2127,7 @@
         combo_key=combo,
         weight_used=weight_used,
         confluence_score=adj_score,
+        entry_tiers_json=_tiers_json,
         matrix_direction=matrix_result['direction'],
         market_regime=matrix_result.get('market_regime'),
         matrix_breakdown_json=matrix_breakdown_json,
@@ -2255,31 +2266,58 @@
 
 
 def _entry_signals_for(vpos):
-    """The THREE signals that opened this position: the 1H alert that set the
-    trend, the 15m confirmation and the 5m trigger. All read from stored rows —
-    the 15m name is recovered from the entry advisor's own prompt, which records
-    it verbatim."""
-    out = {'sig_1h': None, 'sig_15m': None, 'sig_5m': None, 'entry_thesis': None}
+    r"""The THREE tiers that opened this position, from the record CAPTURED AT
+    ENTRY (`trades.entry_tiers_json`) — the state-machine snapshot plus the
+    matrix, serialised by consult_for_entry.
+
+    2026-07-29: this used to recover the 15m name by REGEX-PARSING it back out
+    of the stored entry prompt (`^15m: (.+?) \(direction`). That inherited every
+    defect of the prompt: when the entry prompt said "15m: n/a" — 14 of 59
+    executed entries — the exit advisor was told "15m confirmed by: n/a" and
+    could not judge whether the entry thesis was still alive. Reading a rendered
+    string back as data was the defect; the structured record replaces it.
+
+    Rows written before this commit have no `entry_tiers_json`. For those the
+    old prompt-parse still runs, clearly marked as the legacy path, so historical
+    positions degrade to what they always showed instead of to nothing."""
+    out = {'sig_1h': None, 'sig_15m': None, 'sig_5m': None, 'entry_thesis': None,
+           'tier_facts': None, 'entry_tier_block': None}
     try:
         eid = vpos.get('trades_entry_row_id')
         if not eid:
             return out
         with sqlite3.connect(DB_PATH) as conn:
             conn.row_factory = sqlite3.Row
-            e = conn.execute("SELECT timestamp,tv_action,ai_reason,ai_user_prompt "
-                             "FROM trades WHERE id=?", (eid,)).fetchone()
+            e = conn.execute("SELECT timestamp,tv_action,ai_reason,ai_user_prompt,"
+                             "entry_tiers_json FROM trades WHERE id=?", (eid,)).fetchone()
             if not e:
                 return out
-            out['sig_5m'] = e['tv_action']
             out['entry_thesis'] = e['ai_reason']
+            if e['entry_tiers_json']:
+                import signal_tiers
+                facts = json.loads(e['entry_tiers_json'])
+                out['tier_facts'] = facts
+                out['entry_tier_block'] = signal_tiers.entry_thesis_lines(facts)
+                t = facts.get('tiers') or {}
+                out['sig_1h'] = (t.get('1H') or {}).get('name')
+                out['sig_15m'] = (t.get('15m') or {}).get('name')
+                out['sig_5m'] = (t.get('5m') or {}).get('name')
+                return out
+            # ---- LEGACY PATH: pre-2026-07-29 rows only ----
+            out['sig_5m'] = e['tv_action']
             m = re.search(r'^15m: (.+?) \(direction', e['ai_user_prompt'] or '', re.M)
-            if m:
+            if m and m.group(1) != 'n/a':
                 out['sig_15m'] = m.group(1)
             h = conn.execute("SELECT tv_action FROM trades WHERE signal_type='1h_trend_set' "
                              "AND timestamp<=? ORDER BY id DESC LIMIT 1",
                              (e['timestamp'],)).fetchone()
             if h:
                 out['sig_1h'] = h['tv_action']
+            out['entry_tier_block'] = (
+                f"  1H:  {out['sig_1h'] or 'ABSENT'}  (legacy record — direction, weight and age "
+                f"were not captured before 2026-07-29)\n"
+                f"  15m: {out['sig_15m'] or 'ABSENT'}  (legacy record)\n"
+                f"  5m:  {out['sig_5m'] or 'ABSENT'}  (legacy record)")
     except Exception as _e:
         print(f"[EXIT-ADVISOR] entry-signal lookup partial: {_e}", flush=True)
     return out
@@ -3469,7 +3507,13 @@
         market_regime=matrix_result.get('market_regime'),
         mtf_alignment_score=indicators.mtf_alignment_score(_snap, direction),
         book_pct=_entry_book_pct(pre_trade_walls),
+        matrix_result=matrix_result,
     )
+    _tiers_json = None
+    try:
+        _tiers_json = json.dumps(advice.get('signal_tiers') or {})
+    except Exception as _e:
+        print(f"[ENTRY-TIERS] serialise failed: {_e}", flush=True)
     ai_decide = advice.get('decide')
     ai_conf = float(advice.get('confidence') or 0.0)
     ai_reason = (advice.get('reason') or '')[:200]
@@ -3500,6 +3544,7 @@
         hw_15m_weight=hw_weight,
         hw_15m_signal_name=hw_signal_name,
         confluence_score=adj_score,
+        entry_tiers_json=_tiers_json,
         matrix_direction=matrix_result['direction'],
         market_regime=matrix_result.get('market_regime'),
         matrix_breakdown_json=matrix_breakdown_json,
--- /dev/null
+++ b/signal_tiers.py   (NEW FILE, 215 lines)
+"""The three signal tiers — 1H / 15m / 5m — rendered from the AUTHORITATIVE sources.
+
+WHY THIS MODULE EXISTS (2026-07-29, OPEN-ITEMS §2.8)
+---------------------------------------------------
+The entry advisor printed the 15m tier as `15m: n/a (direction: n/a)` on 14 of
+59 executed entries, directly above the sentence "The 3 timeframes are aligned
+(confluence has already passed)". Diagnosis (kola-reports 2026-07-29):
+
+  * NOT a write gap. `state_machine.update_slot()` stores the name, and
+    `_persist_slot_locked` / `_restore_from_snapshot` both round-trip it.
+  * The tier is genuinely EMPTY at those moments, because
+    `_clear_lower_tfs_locked()` wipes the 15m/5m slots on any 1H flip or Group-B
+    Exit Signal, while `HTF_TOLERATE_NEUTRAL = True` (f911d51, 2026-05-20) lets
+    the entry through anyway. Zero of the 4 entries before that flag ever showed
+    `15M:None`; 14 of the 55 after it did.
+  * TWO REGISTRIES HOLD THE SAME FACT AND DISAGREE, IN BOTH DIRECTIONS.
+    `state_machine`'s 15m slot has a 4h TTL and is cleared by 1H flips.
+    `signal_matrix`'s MOMENTUM category has a 90-minute TTL and is cleared by
+    neither. Measured on the last 20 entries: 2 had an empty slot while the
+    matrix held 3 live MOMENTUM signals, and 6 had a live slot while the matrix
+    had already expired it. The prompt read the slot; the gate counted the
+    matrix. Neither alone is the whole truth, so this module prints BOTH.
+
+WHAT IT GUARANTEES
+  * Every tier states NAME, DIRECTION, WEIGHT and AGE, or the single word
+    ABSENT. The string "n/a" is never produced for a tier.
+  * Agreement across the three tiers is stated in one explicit line, so the
+    model never has to infer it from three separate strings.
+  * A tier whose direction was reset to NEUTRAL is shown as NEUTRAL. It is no
+    longer printed as if it were still in force — the exact failure on entry
+    19021, where an Exit Signal neutralised the 1H at 00:00 and the 01:00 prompt
+    still read "1H trend set by: Trend Catcher Down".
+
+🔴 IDENTITY ONLY — NO JUDGEMENT. Same line drawn by f0a8d30 (1H identity) and
+8b15ecc (book percentiles). Name, direction, weight, age, whether the gate
+counted it, and whether a 5m signal is trigger-capable are all FACTS about what
+the bot itself did. No win rate, no PnL, no historical performance, no "this
+signal is good/bad" is attached to any name. The model learns WHICH signal
+fired and HOW the bot weighted it — never whether that signal tends to work.
+
+Pure function of its arguments: no DB, no network, no clock beyond `now`.
+"""
+from datetime import datetime, timezone
+
+# Slot -> (label, timeframe). Order is the cascade's own order.
+_TIERS = (('1h_context', '1H'), ('15m_confirm', '15m'), ('5m_trigger', '5m'))
+
+# The matrix category that each tier's evidence lands in. Used only to report
+# whether the SCORE GATE counted the tier — never to decide anything.
+_TIER_CATEGORY = {'1h_context': 'TREND', '15m_confirm': 'MOMENTUM',
+                  '5m_trigger': 'EXECUTION'}
+
+
+def _age_str(ts_iso, now):
+    """Human age of a slot timestamp. Returns None when unknown."""
+    if not ts_iso:
+        return None
+    try:
+        dt = datetime.fromisoformat(str(ts_iso))
+        if dt.tzinfo is None:
+            dt = dt.replace(tzinfo=timezone.utc)
+    except (TypeError, ValueError):
+        return None
+    mins = (now - dt).total_seconds() / 60.0
+    if mins < 0:
+        return None
+    return f"{mins:.0f}m ago" if mins < 90 else f"{mins / 60.0:.1f}h ago"
+
+
+def _weight_of(name):
+    """The matrix weight the bot itself assigned to this signal name.
+    Imported lazily so this module stays importable in isolation."""
+    if not name:
+        return None
+    try:
+        from signal_matrix import classify
+        cat, _dir, _cid, weight = classify(name)
+        return (weight, cat)
+    except Exception:
+        return None
+
+
+def build(snapshot, matrix_result=None, proposed_direction=None, now=None):
+    """Structured facts for all three tiers.
+
+    snapshot          — state_machine.get_snapshot() / set_trigger_and_snapshot()
+                        output. THE authoritative slot state.
+    matrix_result     — signal_matrix.compute_score() output, i.e. what the score
+                        gate actually counted. Optional; when absent the
+                        'counted' field is simply omitted rather than guessed.
+    proposed_direction— 'LONG'/'SHORT', the direction being traded.
+
+    Returns a JSON-serialisable dict. Never raises.
+    """
+    now = now or datetime.now(timezone.utc)
+    breakdown = (matrix_result or {}).get('breakdown') or {}
+    out = {'tiers': {}, 'proposed_direction': proposed_direction}
+    for slot, label in _TIERS:
+        s = (snapshot or {}).get(slot) or {}
+        name = s.get('signal_name')
+        direction = s.get('direction')
+        # A slot with no name is absent regardless of what else it carries.
+        present = bool(name)
+        t = {'label': label, 'present': present, 'name': name,
+             'direction': direction, 'weight': None, 'category': None,
+             'age': _age_str(s.get('timestamp'), now), 'kind': None,
+             'counted_by_gate': None}
+        wc = _weight_of(name) if present else None
+        if wc:
+            t['weight'], t['category'] = wc
+        if label == '5m' and t['category']:
+            # 22 of the 32 Price Action signals are EXECUTION and can trigger an
+            # entry; the other 10 are LIQUIDITY and only carry weight. This is
+            # the bot's own rule (main.py routes non-EXECUTION 5m alerts to
+            # 'context_recorded' and never lets them touch the trigger slot).
+            t['kind'] = ('trigger-capable' if t['category'] == 'EXECUTION'
+                         else 'context-only (carries weight, cannot trigger)')
+        cat = _TIER_CATEGORY.get(slot)
+        if breakdown and cat in breakdown:
+            nd = (breakdown[cat] or {}).get('net_direction')
+            t['counted_by_gate'] = (nd not in (None, 'NEUTRAL'))
+            t['gate_direction'] = nd
+        out['tiers'][label] = t
+    out['agreement'] = _agreement(out['tiers'], proposed_direction)
+    return out
+
+
+def _agreement(tiers, proposed_direction):
+    """One explicit sentence about whether the tiers point the same way.
+    Descriptive only — it states what the directions ARE, never what they mean."""
+    live = {lab: t for lab, t in tiers.items()
+            if t['present'] and t['direction'] in ('LONG', 'SHORT')}
+    absent = [lab for lab, t in tiers.items() if not t['present']]
+    neutral = [lab for lab, t in tiers.items()
+               if t['present'] and t['direction'] not in ('LONG', 'SHORT')]
+    if not live:
+        return "No tier currently holds a directional signal."
+    dirs = set(t['direction'] for t in live.values())
+    parts = []
+    if len(dirs) == 1:
+        only = dirs.pop()
+        _l = sorted(live)
+        _verb = ('points' if len(_l) == 1
+                 else 'both point' if len(_l) == 2 else 'all point')
+        parts.append(f"{' and '.join(_l)} {_verb} {only}")
+    else:
+        by_dir = {}
+        for lab, t in live.items():
+            by_dir.setdefault(t['direction'], []).append(lab)
+        parts.append("; ".join(
+            f"{'+'.join(sorted(v))} {'points' if len(v) == 1 else 'point'} {k}"
+            for k, v in sorted(by_dir.items())))
+    if proposed_direction:
+        agree = [l for l, t in live.items() if t['direction'] == proposed_direction]
+        against = [l for l, t in live.items() if t['direction'] != proposed_direction]
+        parts.append(f"vs the proposed {proposed_direction}: "
+                     f"{'+'.join(sorted(agree)) or 'none'} agree"
+                     + (f", {'+'.join(sorted(against))} OPPOSE" if against else ""))
+    if neutral:
+        parts.append(f"{'+'.join(sorted(neutral))} NEUTRAL (reset, not in force)")
+    if absent:
+        parts.append(f"{'+'.join(sorted(absent))} ABSENT")
+    return "; ".join(parts) + "."
+
+
+def render(facts):
+    """The prompt block. Fixed-width so the three tiers are unmistakable."""
+    lines = ["SIGNAL TIERS — what fired, in which direction, how the bot weighted it,",
+             "and how long ago. IDENTITY ONLY: no win rate or past performance is implied."]
+    for _slot, label in _TIERS:
+        t = (facts.get('tiers') or {}).get(label) or {}
+        if not t.get('present'):
+            lines.append(f"  {label + ':':4s} ABSENT — no {label} signal is held by the "
+                         f"state machine at this moment")
+            continue
+        bits = [t.get('direction') or 'NEUTRAL']
+        if t.get('weight') is not None:
+            bits.append(f"weight {t['weight']:.1f}")
+        if t.get('age'):
+            bits.append(f"last set {t['age']}")
+        if t.get('kind'):
+            bits.append(t['kind'])
+        # The slot and the matrix are two registries for the same fact and they
+        # disagree in BOTH directions (see the module docstring). State the
+        # disagreement rather than silently showing one of the two.
+        if t.get('counted_by_gate') is False:
+            bits.append("NOT counted by the gate — matrix TTL expired")
+        elif (t.get('gate_direction') and t.get('direction')
+              and t['gate_direction'] != t['direction']):
+            bits.append(f"but the score gate counted this tier as "
+                        f"{t['gate_direction']} — slot and matrix disagree")
+        lines.append(f"  {label + ':':4s} {t['name']}  ({', '.join(bits)})")
+    lines.append(f"  Agreement: {facts.get('agreement')}")
+    return "\n".join(lines) + "\n"
+
+
+def entry_thesis_lines(facts):
+    """Compact one-line-per-tier form for the EXIT advisor's entry-thesis block.
+    Reads the SAME structured facts captured at entry — never re-derived, never
+    parsed back out of a stored prompt."""
+    out = []
+    for _slot, label in _TIERS:
+        t = (facts.get('tiers') or {}).get(label) or {}
+        if not t.get('present'):
+            out.append(f"  {label + ':':4s} ABSENT at entry")
+            continue
+        bits = [t.get('direction') or 'NEUTRAL']
+        if t.get('weight') is not None:
+            bits.append(f"weight {t['weight']:.1f}")
+        if t.get('age'):
+            bits.append(f"set {t['age']} at entry")
+        out.append(f"  {label + ':':4s} {t['name']}  ({', '.join(bits)})")
+    if facts.get('agreement'):
+        out.append(f"  Agreement at entry: {facts['agreement']}")
+    return "\n".join(out)
```
