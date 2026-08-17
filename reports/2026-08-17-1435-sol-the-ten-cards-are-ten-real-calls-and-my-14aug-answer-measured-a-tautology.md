# Mercury-SOL — the ten cards are TEN REAL MODEL CALLS. The dedup has fired 16 times in its life, and my 14.08 answer measured a tautology.

**2026-08-17 14:35 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · READ-ONLY THROUGHOUT — no `.py` written, no restart, no order, no DB write. The diff in §3c is printed in this report only and exists in no file.**

Titan (`/root/titan-bot`): **not touched, not read for state, no numbers imported.** HEAD `897850b`, clean.

---

## ⚡ THE SHORT VERSION

1. **🔴 I WAS WRONG ON 2026-08-14, AND HERE IS THE NUMBER THAT SHOWS IT.** I told the operator he was seeing rows, not calls, on the strength of "1.000 calls per market state, every day." **That figure is a tautology.** A "market state" is defined by the dedup key, and the dedup cache has a **60-second TTL** — so every consultation more than 60 s after the last one is, by definition, a *new* state. "1.000 calls per state" therefore means only "we never call twice inside one minute." It cannot detect the thing the operator is describing, and it did not.
2. **🔴 THE REAL NUMBER: the verdict cache has been reused 16 times in its entire life — 16 of 3,803 rows (0.4 %).** In the **last 7 days: 1 reuse in 320 consultations (0.3 %)**. Since it shipped on 06.08 it has saved **16 model calls in 12 days = 1.3/day**.
3. **The operator's burst is real and it is model calls.** Worst rolling hour: **13 AI SKIP cards, 13 model calls, 0 reused.** In the hour 2026-08-16 12:00–13:00 there are **twelve** rows, spaced **exactly five minutes apart**, same direction, same combo, same verdict, `ai_verdict_reuse_json` NULL on every one.
4. **So it is answer (a): ten genuine calls.** Not a display artifact, not ten cards from one call.
5. **🔴 BUT IT IS NOT A BUSTED KEY.** The key excludes the 5m trigger name, as designed. The nearest opposing wall was the **same level (75.25) on 10 of the 12 rows**. The book gate's six new columns are not in the key and never were. **Nothing leaked in.** What defeats the dedup is the arithmetic of its own TTL: **93.8 % of consecutive same-direction consultations arrive more than 60 s apart** — 29.7 % at 1–5 min, 48.3 % at 5 min–1 h. The cache is *expired before the next alert exists*.
6. **The in-flight coalescing is working exactly as built.** All 16 reuses have an age of **0.000–2.794 s**, fifteen of them ≤0.003 s — the in-flight path across the four gthread threads. It catches simultaneous alerts, which is what it was designed for, and that is **6.2 % of the traffic**.
7. **The root is upstream of the bot: the alert is a STATE, not an EVENT.** "Within Bullish OB" fires on **every 5m close for as long as price stays inside the order block.** One TradingView condition, twelve firings, twelve consultations, twelve cards, one decision.
8. **🔴 AND THE CARD IS SENT EVEN ON A REUSE.** `_reuse` writes a JSON column and a stdout line and changes nothing else; the `send_tg` in the `ai_skipped` branch is unconditional. So even if the dedup were fixed tomorrow, **the operator would still get every card.** The call problem and the card problem are independent, and only the second one is what he is complaining about.
9. **§3c proposes the smallest fix: a card-level throttle on `(direction, combo_key, verdict)`, DB rows untouched.** It turns 13 cards into 1 + a tail counter. **Diff shown, NOT applied.**

---

## 0. METHOD

`trades.db` opened `mode=ro`. An "advisor consultation" = a row with `ai_decision IS NOT NULL` (3,803 rows since 2026-06-08; 3,653 of them `status='ai_skipped'`). A **model call** = such a row with `ai_verdict_reuse_json IS NULL`; a **reuse** = the same column populated. That column exists precisely so this question can be answered — it was added on 2026-08-06 with the note *"without this column it is indistinguishable from a fresh consultation and the next audit mis-counts model calls."* **This is that audit, and it is the first one to actually read the column.**

🔴 **Nothing below is a mean.** Every count is a worst-case rolling window computed from each row forward.

---

# 1. THE BURSTS

## 1a. Rolling windows of every length — where "ten" actually lives

AI SKIP cards only, last 7 days, worst rolling window starting at each row:

| window | worst count | starting |
|---|---|---|
| **1 minute** | **2** | 2026-08-16 20:45:00 |
| 5 minutes | 3 | 2026-08-16 20:40:08 |
| 15 minutes | 5 | 2026-08-12 23:45:20 |
| 30 minutes | 8 | 2026-08-12 23:40:03 |
| **1 hour** | **13** | **2026-08-16 11:55:07** |
| 2 hours | 19 | 2026-08-16 11:25:02 |

Distribution of the 60-second count starting at each of the 264 rows: `{1: 259, 2: 5}`.

🔴 **This is where my 14.08 answer went wrong, and it is a question-framing error, not an arithmetic one.** I measured a per-minute rate, found ~1, and reported that nothing was bursting. **The operator was never describing one minute.** He reads Telegram on a phone; a stack of thirteen identical cards accumulated over an hour arrives as "ten in a row, at essentially the same time" — and on his screen it *is* one screenful. **At the scale he actually experiences, the burst is real: 13 cards, and 13 model calls.**

## 1b. The worst hour, row by row

Every AI SKIP row in 2026-08-16 12:00–13:00:

| id | timestamp | gap | 5m trigger | dir | verdict | conf | **REUSED?** | nearest opposing wall |
|---|---|---|---|---|---|---|---|---|
| 18960 | 12:00:10 | — | Within Bullish OB | LONG | skip | 0.78 | **no** | 75.25 |
| 18962 | 12:05:01 | 291 s | Within Bullish OB | LONG | skip | 0.82 | **no** | 75.75 |
| 18963 | 12:10:11 | 310 s | Within Bullish OB | LONG | skip | 0.78 | **no** | 75.25 |
| 18964 | 12:15:02 | 291 s | Within Bullish OB | LONG | skip | 0.78 | **no** | 75.25 |
| 18966 | 12:20:06 | 304 s | Within Bullish OB | LONG | skip | 0.82 | **no** | 75.25 |
| 18967 | 12:25:04 | 298 s | Within Bullish OB | LONG | skip | 0.78 | **no** | 75.25 |
| 18968 | 12:30:05 | 301 s | Within Bullish OB | LONG | skip | 0.82 | **no** | 75.75 |
| 18970 | 12:35:02 | 297 s | Within Bullish OB | LONG | skip | 0.82 | **no** | 75.25 |
| 18972 | 12:40:08 | 306 s | Within Bullish OB | LONG | skip | 0.78 | **no** | 75.25 |
| 18974 | 12:45:06 | 298 s | Within Bullish OB | LONG | skip | 0.78 | **no** | 75.25 |
| 18978 | 12:50:24 | 318 s | Bullish Breaker | LONG | skip | 0.82 | **no** | 75.25 |
| 18979 | 12:55:03 | 279 s | Within Bullish OB | LONG | skip | 0.78 | **no** | 75.25 |

**combo_key on eleven of the twelve:** `1H:Any Bearish Confirmation|15M:HyperWave OS Signal Up|5M:Within Bullish OB`

The `ai_reason` strings are the same sentence rewritten twelve times — *"FLAT market (ADX 18.9/18.7 …)"*, *"4H/1H BEAR regime opposes LONG; flat market (ADX <20 …)"*, *"Flat-market guard triggered: ADX 1h/15m ~18-19 (weak) …"*. **One decision, twelve renderings, twelve model calls.**

🔴 **The gap column is the whole story: 279–318 seconds. One firing per 5m candle close.** The trigger is `Within Bullish OB` — a **state**, not an event. TradingView re-fires it on every bar for as long as price remains inside the order block, and price stayed inside it for an hour.

## 1c. 🔴 THE NUMBER THAT MATTERS — calls, counted at the call site

| scope | rows | **MODEL CALLS** | reused | reuse rate |
|---|---|---|---|---|
| whole history (06.06 → today) | 3,803 | **3,787** | **16** | **0.4 %** |
| since the dedup shipped (06.08) | 523 | **507** | 16 | 3.1 % |
| **last 7 days** | **320** | **319** | **1** | **0.3 %** |
| **the worst hour** | **12** | **12** | **0** | **0.0 %** |

**Twelve rows, twelve calls, zero reuse.** The answer to the brief's §1d is therefore no: these are not ten rows from one call.

---

# 2. THEY ARE GENUINE CALLS — so what defeats the dedup?

## 2a. The key, verbatim

`claude_advisor.py:829-848`:

```python
def _slot_identity(_slot):
    return (_slot.get('signal_name'), _slot.get('direction'), _slot.get('timestamp'))

_dir_key = (direction or '').upper()
...
_state_key = (symbol, _dir_key, _slot_identity(_h1), _slot_identity(_m15),
              _near_opposing)
```

Five components: **symbol · direction · the 1H slot (name, direction, timestamp) · the 15M slot (name, direction, timestamp) · the nearest opposing wall PRICE.**

## 2b. 🔴 NOTHING LEAKED IN. The key is clean.

The brief asked whether the wall multiple, the percentile, the dual tally or the book gate's six columns had crept in. **They have not** — and two of them were excluded on purpose, with the reason recorded at `claude_advisor.py:110-119`:

> *"identity is deliberately NOT in the key — it is the only thing that differs, and caching on it would cache nothing … The nearest opposing wall PRICE is in the key so a genuine book shift busts the cache; **its MULTIPLE is not**, because that wobbles in the first decimal between two reads of the same wall (16.4 % of states) and is not a state change."*

Checked against the burst:

| candidate field | in the key? | did it differ across the 12 rows? |
|---|---|---|
| 5m trigger **name** | **no** (deliberate) | yes — 11× `Within Bullish OB`, 1× `Bullish Breaker` |
| wall **multiple** | **no** (deliberate) | yes — 10.7 … 15.4 |
| wall **percentile** `book_gate_opp_pctl` | **no** | yes — 13.3 … 58.3 |
| `book_gate_*` (all six) | **no** | yes |
| dual tally | **no** | n/a |
| **nearest opposing wall PRICE** | **YES** | 🔴 **barely — 75.25 on 10 of 12, 75.75 on 2** |

**The wall price is bucketed to the 0.50 grid, so it is far more stable than a raw price would be.** It moved twice in an hour, and only because `mid` crossed the 75.25 level. **It is not what is defeating the cache.**

## 2c. 🔴 WHAT IS DEFEATING IT: the TTL is 60 s and the traffic repeats every 300 s

`claude_advisor.py:121`: `_STATE_VERDICT_TTL_S = 60.0`.

Inter-arrival gaps between consecutive **same-direction** consultations, all 418 pairs since the dedup shipped:

| gap | pairs | share | can the dedup catch it? |
|---|---|---|---|
| ≤ 5 s | 25 | 6.0 % | ✅ yes (in-flight) |
| 5–60 s | 1 | 0.2 % | ✅ yes (cache) |
| **60–300 s** | **124** | **29.7 %** | ❌ **TTL already expired** |
| **300 s – 1 h** | **202** | **48.3 %** | ❌ **TTL already expired** |
| > 1 h | 66 | 15.8 % | ❌ (and correctly so) |

🔴 **93.8 % of the traffic arrives after the cache entry has already been swept.** The dedup is not broken — **it is structurally unable to see the pattern the operator is complaining about**, because its window is five times shorter than the interval between the repeats.

**And the in-flight half is working, exactly as specified.** Every reuse that has ever happened, with its age:

```
n = 16     ages(s): 0.0 x7, 0.001 x5, 0.002, 0.003 x2, 2.794
every one has a DIFFERENT 5m trigger from the leader it reused: TRUE (16/16)
```

Fifteen of sixteen at ≤3 ms is the in-flight path — a follower thread waiting on a leader's live Claude call under gthread×4, which is precisely the mechanism the 2026-08-06 note called *"not an optimisation — without it this saves nothing."* **It works. It is just aimed at 6.2 % of the traffic.**

**One thing I cannot resolve from the DB, stated rather than guessed:** the 1H/15M slot **timestamps** are not archived (`market_state_snapshot` is keyed by slot and holds only the current value), so I cannot prove they stayed constant across the hour. If the TTL were ever raised, a 15m slot refreshing on its own cadence would become the next binding constraint. **That is the second thing to check, not the first — the TTL settles this one on its own.**

## 2d. Cost, against the figures I quoted

| | rows/day | **model calls/day** | saved by the dedup |
|---|---|---|---|
| PRE-dedup (01.07 – 05.08, 36 days) | 67.7 | **67.7** | 0 |
| POST-dedup (06.08 – today, 12 days) | 43.6 | **42.2** | **1.3/day (16 total, 3.1 %)** |

🔴 **The fall from 67.7 to 42.2 is a fall in ALERT VOLUME, not a dedup saving.** The dedup's own contribution is the last column: **16 calls in twelve days.**

**And the honest replacement for "1.000 calls per market state":** group consultations into runs of the same `(direction, combo_key, verdict)` within an hour — the unit the operator actually perceives as one decision.

```
runs since 06.08 : 379      mean rows/run 1.38      mean MODEL CALLS/run 1.34
the longest runs — rows / model calls / span:
   11 rows,  11 model calls,  50.0 min   LONG  skip   1H:Any Bearish Confirmation|15M:HyperWave OS Signal Up|...
    8 rows,   8 model calls,  35.0 min   LONG  skip   1H:Any Bullish Confirmation|15M:HyperWave Signal Down|...
    6 rows,   6 model calls,  24.9 min   SHORT skip   1H:Trend Catcher Down|15M:Reversal Down|...
    6 rows,   6 model calls,  25.0 min   SHORT skip   1H:Bearish Confirmation+|15M:HyperWave Signal Up|...
    6 rows,   6 model calls,  25.0 min   SHORT skip   1H:Bullish Confirmation+|15M:Reversal Down|...
```

**The mean is 1.34 calls per decision — which is why an average looked fine on 14.08 — and the tail is eleven calls for one decision.** That is the whole lesson of this pass: **the mean was never the disputed quantity.**

---

# 3. THE CARD SIDE

## 3a. 🔴 YES — a reused verdict still sends a full card

`main.py:4972-4985` is the entire effect of a reuse:

```python
_reuse = advice.get('verdict_reused')
_reuse_from = advice.get('verdict_reused_from') or {}
_reuse_json = json.dumps({...}) if _reuse else None
if _reuse:
    print(f"{LOG_PREFIX}[STATE-CACHE] row={row_id} verdict REUSED ... — no model call")
```

A JSON column and a stdout line. Then `main.py:5148-5155`, unconditional:

```python
send_tg(
    f"🤖 <b>AI SKIP</b> ({ai_conf:.2f}) ({direction})\n"
    f"💎 {symbol}\n"
    f"<i>{ai_reason}</i>\n"
    f"{_tf_line}\n"
    f"<code>{combo}</code>"
)
```

**Thirteen of the sixteen reuse rows are `ai_skipped` — every one of them sent a card for a verdict that cost nothing.** So the two problems are independent: **fixing the dedup would reduce the API bill and would not remove a single card from the operator's phone.**

## 3b. Cards vs decisions in the worst burst

```
window 2026-08-16 11:55 -> 13:00
  AI SKIP cards sent           : 13
  model calls behind them      : 13
  DECISIONS they represent     :  1   ("stay out of this flat LONG")
  distinct combo_keys          :  2   (the 5m trigger changed once, to Bullish Breaker)
  distinct verdicts            :  1   (skip)
  confidence values            :  2   (0.78, 0.82)
also in that window, from other paths: 5 entry_gate_refused, 2 below_threshold, 1 context_recorded
```

**13 cards for 1 decision.** That is the operator's complaint, stated in his own units.

## 3c. The smallest change that collapses a burst — diff shown, **NOT APPLIED**

**Requirements, in order:** every DB row stays (they are evidence, and the optimizer and `skip_attribution` read them); the first card of a run still arrives immediately; a change of verdict, direction or combo must **always** break through; nothing may sit in front of the entry path.

**Why a process-local dict is sufficient here, and how I know:** `gunicorn_mercury.conf.py` sets `workers = 1, threads = 4`. All traffic is in one process, and this codebase already proves the pattern under exactly these settings — the verdict cache's in-flight coalescing is a module dict plus a `threading.Lock`, and §2c shows it working across the four threads 16 times.

```diff
--- a/config.py
+++ b/config.py
@@
+# ── 🔴 CARD THROTTLE — a NOTIFICATION fix, NOT a dedup fix (2026-08-17) ──────
+# The operator receives one AI SKIP card per 5m candle for as long as a STATE-type
+# TradingView trigger ("Within Bullish OB") keeps re-firing. Measured on the worst
+# hour: 13 cards, 13 model calls, ONE decision (reports/2026-08-17-1435-*.md).
+#
+# 🔴 THIS DOES NOT TOUCH THE MODEL CALLS AND MUST NOT BE READ AS DOING SO. Every
+# trades row, every skip_attribution row and every advisor call happens exactly as
+# before. Only the Telegram card is collapsed. The dedup's own problem — a 60 s TTL
+# against a 300 s repeat cadence — is a SEPARATE question and is untouched here.
+#
+# 0 disables the throttle (every card sent, the pre-2026-08-17 behaviour).
+AI_SKIP_CARD_THROTTLE_S = 1800   # 30 min: one card per (direction, combo, verdict)
```

```diff
--- a/main.py
+++ b/main.py
@@
+# ── AI SKIP card throttle (2026-08-17) ───────────────────────────────────────
+# Process-local, like claude_advisor's verdict cache, and sufficient for the same
+# reason: gunicorn_mercury.conf.py is workers=1 threads=4, so one dict sees all
+# traffic. Keyed on what makes a card DIFFERENT to a reader — never on the 5m
+# trigger name, which is the thing that varies while the decision does not.
+_skip_card_lock  = threading.Lock()
+_skip_card_last  = {}          # key -> [monotonic_at_first_sent, suppressed_count]
+
+def _skip_card_due(direction, combo, verdict):
+    """(send?, suppressed_since_last_card). A window that has expired RESETS and
+    the next card is sent carrying the count it swallowed, so nothing is silent
+    about having been silent."""
+    if not AI_SKIP_CARD_THROTTLE_S:
+        return True, 0
+    key = (direction, combo, verdict)
+    now = time.monotonic()
+    with _skip_card_lock:
+        prev = _skip_card_last.get(key)
+        if prev is None or now - prev[0] >= AI_SKIP_CARD_THROTTLE_S:
+            n = prev[1] if prev else 0
+            _skip_card_last[key] = [now, 0]
+            return True, n
+        prev[1] += 1
+        return False, prev[1]
@@ -5148,13 +5148,24 @@
-                send_tg(
-                    f"🤖 <b>AI SKIP</b> ({ai_conf:.2f}) ({direction})\n"
-                    f"💎 {symbol}\n"
-                    f"<i>{ai_reason}</i>\n"
-                    f"{_tf_line}\n"
-                    f"<code>{combo}</code>"
-                )
+                _send_card, _swallowed = _skip_card_due(direction, combo, 'skip')
+                if _send_card:
+                    send_tg(
+                        f"🤖 <b>AI SKIP</b> ({ai_conf:.2f}) ({direction})\n"
+                        f"💎 {symbol}\n"
+                        f"<i>{ai_reason}</i>\n"
+                        f"{_tf_line}\n"
+                        + (f"<i>(+{_swallowed} identical skip(s) in the previous "
+                           f"{AI_SKIP_CARD_THROTTLE_S//60} min — all rows in the DB)</i>\n"
+                           if _swallowed else "")
+                        + f"<code>{combo}</code>"
+                    )
+                else:
+                    print(f"{LOG_PREFIX}[SKIP-CARD] throttled — row={row_id} written, "
+                          f"card suppressed ({_swallowed} in this window) "
+                          f"{direction} {combo}", flush=True)
```

**On the worst hour this turns 13 cards into 1**, and the next card outside the window opens with *"(+12 identical skip(s) in the previous 30 min — all rows in the DB)"*.

⚠️ **Three properties to check before this is ever applied, named here rather than discovered later:**

1. **The verdict is in the key**, so a `skip` → `execute` flip is never throttled. But **an execute does not take this branch at all** — it falls through to the entry path — so verify no other card is suppressed by a future edit that reuses this helper.
2. **The window resets on expiry, it does not slide.** A run longer than 30 min emits a second card. That is intended: an hour of silence about an active decision is worse than two cards.
3. 🔴 **`_swallowed` must never be allowed to imply rows were dropped.** The wording above says *"all rows in the DB"* on purpose — the single most likely way this change becomes a defect is a future reader taking a suppressed card as a suppressed decision, which is the same class of error as this whole report.

---

# 4. VERDICT

## 4a. Which of the three is it — plainly

**It is (a): TEN GENUINE MODEL CALLS.** Thirteen in the worst rolling hour, twelve in the 12:00 clock hour, `ai_verdict_reuse_json` NULL on every one. Not a display artifact. Not ten cards from one call.

**But the cause is not the one the brief anticipated.** The dedup key is clean — the 5m name is out, the wall multiple is out, the percentile is out, the book gate's six columns are out, and the one live field in the key (the nearest opposing wall) held the same value on 10 of 12 rows. **The dedup is defeated by its own TTL: 60 seconds against a repeat cadence of 300. It catches 6.2 % of the traffic and was only ever able to catch that 6.2 %.**

And underneath both: **the alert is a STATE, not an EVENT.** `Within Bullish OB` re-fires every 5m bar for as long as price sits inside the block. Twelve firings is one market condition, not twelve signals.

## 4b. 🔴 WHERE I GOT IT WRONG ON 2026-08-14, WITH THE NUMBER

**I said: "1.000 calls per market state, every day — it is rows, not calls."**

That statement is **true and empty**. A "market state" is the dedup key; the cache holding it expires after **60 seconds**; therefore any two consultations more than a minute apart belong to different states **by construction**. Measuring calls-per-state can only ever return ~1.000 no matter how much traffic there is. **I measured the denominator with the same instrument that produced the numerator, and reported the ratio as evidence.**

The number that would have caught it was one query away, in a column added five days earlier *for exactly this purpose*:

```
ai_verdict_reuse_json IS NOT NULL  ->  16 rows out of 3,803  (0.4%)
                    last 7 days   ->   1 row  out of   320   (0.3%)
```

**A dedup that has fired sixteen times cannot be saving anything, and I reported it as working.** The operator raised it twice; the second time is what made me look at the right column.

## 4c. What is and is not proposed

**Nothing is applied.** The diff in §3c is the only proposal, it is a **notification** change, and it is the smallest one that answers what the operator actually sees.

**The dedup's TTL is deliberately NOT proposed for change here.** Raising it from 60 s to, say, 20 minutes would collapse most of the 29.7 % + 48.3 % — but it would also mean **a verdict decided at 12:00 is still being applied at 12:20 on a book that has moved**, and this book's own history says that is where money is lost. It is a risk trade, not a cleanup, and it needs its own measurement: replay every burst and ask whether any verdict inside it would have flipped. **Two of the twelve rows in the worst hour already show the wall level changing, and the confidences alternate 0.78/0.82 — so the verdicts were not identical inputs, only identical conclusions.** That measurement is not in this pass and must not be assumed from it.

**And the cost, so the decision is grounded:** the model is `claude-haiku-4-5-20251001` at ~42 calls/day. This is not an expenditure problem. **It is a signal-to-noise problem on the operator's phone**, which is why §3c is a card fix and not a cache fix.

---

## STATE — nothing was changed by this pass

```
mercury-sol   active - MainPID 2195203 - since 2026-08-14 19:54:37 UTC - NRestarts=0
              NOT restarted by this pass. FLAT: zero open positions.
ADVISOR       claude-haiku-4-5-20251001 - TIMEOUT_SECONDS 10.0
              _STATE_VERDICT_TTL_S 60.0 - _STATE_INFLIGHT_WAIT_S 10.0 - UNCHANGED
              gunicorn: workers=1 threads=4 gthread preload_app=True
TRAFFIC       3,803 consultations ever - 3,787 model calls - 16 reuses (0.4%)
              last 7 days: 320 consultations, 319 model calls, 1 reuse
              worst rolling hour: 13 AI SKIP cards, 13 model calls, 1 decision
FILES         mercury-sol: ZERO .py modified. No DB write. No order. No restart.
              Read-only URI (mode=ro) throughout. The §3c diff exists in no file.
titan         /root/titan-bot - NOT touched, NOT read for state, NO numbers imported.
              HEAD 897850b - working tree clean
```

**Provenance: `trades.db` `mode=ro`; `claude_advisor.py`, `main.py`, `config.py`, `gunicorn_mercury.conf.py` read at their current revisions with line numbers quoted as found; the nearest-opposing-wall level recomputed per row from the stored `advisor_book_json` using the same rule as `claude_advisor.py:836-842`; every window count is a worst-case rolling window, never a mean. Titan was not read.**
