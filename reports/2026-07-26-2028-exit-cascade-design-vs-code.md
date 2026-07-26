# exit-cascade-design-vs-code

_2026-07-26 20:28 UTC_

---

# TITAN — the exit cascade: intended design vs what the code and the alerts actually do

**2026-07-26 · READ-ONLY. Nothing implemented, nothing proposed, nothing applied.**
Tree clean at `f7df202`. Titan only.

**The break is in TWO places, and only one of them is code.**

* **Configuration / TradingView — the primary break.** There is **exactly one dedicated exit alert
  in the entire system**: `Exit S.`, and it arrives on the 1H channel only. There is **no 5m
  exit alert and no 15m exit alert**. The "separate entry and exit sets" the design assumes do not
  exist on the TradingView side — the 15m and 5m exit tiers are fed the *same* structure alerts as
  entry, and are told apart only by which timeframe field arrives.
* **Code — the secondary break.** The implemented cascade is **two-tier, not three**: 1H arms →
  15m closes. The 15m confirmation calls `_execute_close_position` directly. There is no place in
  the code where a 5m tier could make a final call, and there never was. `EXIT_CONFIRM_TF` selects
  **which single tier confirms** ('15m' or '5m') — it does not chain them.

---

## 1. What actually arrives — the full vocabulary, 65 days

### 1H channel — `tv_tf` is **NULL**, 61 alerts
```
Exit S.        61   ->  60m_exit / 60m_exit_armed     (31 trend_reset · 24 exit_armed · 3 exit_logged · 1 window_canceled)
```

### 1H trend channel — `tv_tf = '60m'`, 258 alerts, ALL entry-context
```
Any B. Confirmation 40 · Any B. Confirmation 39 · Trend C. Up 31 · Trend C. Down 30
Bearish C. 20 · Bullish C. 20 · Bullish C.+ 20 · Bearish C.+ 19
Smart T. Bullish 12 · Smart T. Bearish 11 · Trend T. Down 6 · Trend T. Up 6
Neo C. Bearish 2 · Neo C. Bullish 2
                                   -> all 1h_trend_set / trend_set
```

### 15m channel — `tv_tf = '15m'`, 332 alerts, ALL treated as exit-confirmation
```
Bearish I-BOS   74 · Bullish I-BOS   57 · Bearish I-CHOCH  44 · Bullish I-CHOCH+ 41
Bullish I-CHOCH 37 · Bearish I-CHOCH+ 36 · Bullish S-BOS   12 · Bearish S-BOS     8
Bullish S-CHOCH  7 · Bearish S-CHOCH   5 · Bearish S-CHOCH+ 3 · Bullish S-CHOCH+  3
                                   -> 15m_exit_confirm / exit_unarmed_noop   (327)
Bearish I-CHOCH  2 · Bullish I-CHOCH  2 · Bearish I-CHOCH+ 1
                                   -> 15m_armed_exit / executed              (5)
```

### 5m channel — `tv_tf = '5m'`, 15,833 alerts, split by NAME into entry vs context
```
ENTRY (-> open_long / open_short), 12,762:
  Within B. OB · Within B. OB · Bullish/Bearish OB Entered · OB Created · OB Mitigated B./Bearish B. · Bullish/Bearish I-BOS · I-CHOCH · I-CHOCH+ · S-BOS · S-CHOCH · S-CHOCH+

CONTEXT ONLY (-> 5m_liquidity_ctx / context_recorded), 3,071:
  Bearish New I. 509 · Bullish New I. 482 · Bearish I. Mitigated 476
  Bullish I. Mitigated 456 · Bullish L. Grab 418 · Bearish L. Grab 401
  Broken D. 289 · Broken U. 269 · Equal H. 146 · Equal L. 124
```

**The decisive observation is in the overlap.** `Bearish I-BOS`, `Bullish I-CHOCH`, `S-BOS` and the
rest appear on **both** 15m and 5m — and are routed to **opposite purposes**:

| alert name | on 15m | on 5m |
|---|---|---|
| `Bearish I-BOS` | `15m_exit_confirm` — **exit** | `open_short` — **entry** |
| `Bullish I-CHOCH` | `15m_exit_confirm` — **exit** | `open_long` — **entry** |

The bot separates entry from exit **by timeframe field, not by alert identity.**

---

## 2. Are there separate exit alerts at all? **No — one, and only on 1H.**

`Exit S.` (61 occurrences) is the sole alert whose *name* declares an exit. Everything else is
LuxAlgo structure/OB vocabulary that describes market structure, not intent.

Two structural consequences:

1. **The 15m "exit" tier is not an exit alert set.** It is the entry vocabulary, re-pointed. Which
   is why 327 of 332 15m alerts (98.5%) land as `exit_unarmed_noop` — they are structure prints
   arriving constantly, with no arm to consume them.
2. **The 5m exit tier has no alert to listen for.** The G.-B regex looks for
   `exit | take profit | stop loss | tp | sl`. **No 5m alert name contains any of those words**, and
   none is configured to. The 5m tier is not broken code waiting to be repaired — it is a listener
   with nothing to hear.

**Verdict on this question: the defect is in the TradingView alert configuration.** No 5m exit
alert (and no 15m exit alert) has ever been created. Code changes cannot conjure the missing
vocabulary.

One more configuration asymmetry worth noting: `Exit S.` arrives with **`tv_tf = NULL`**, while
the 1H trend alerts arrive with `tv_tf = '60m'`. The exit alert is sent through the flat/plain-text
payload path, the trend alerts through the JSON path. Two different alert templates on the same
timeframe — a sign the exit alert was configured separately and never brought into line.

---

## 3. How the code intends to split them

**Step 1 — Group A vs Group B, purely by name** (`state_machine.py`):
```python
_GROUP_B_RE = re.compile(r'(\bexit\b|\btake[\s-]?profit\b|\bstop[\s-]?loss\b|\btp\b|\bsl\b)', re.I)

def classify_group(signal_name):
    if _GROUP_B_RE.search(signal_name): return 'B'      # exit / management
    if _BULL_RE.search(signal_name) or _BEAR_RE.search(signal_name): return 'A'   # entry
    return None
```
Only `Exit S.` matches B. Every structure alert matches A.

**Step 2 — routing by timeframe** (`main.py:1536-1592`):
```python
if group == 'B':
    had_trend = state_machine.reset_1h_trend(signal_name)
    if tf == '5m':
        return _handle_5m_close_via_ai(...)          # <- the 5m exit tier, never reached
    status = 'trend_reset' if had_trend else 'group_b_logged'
    ...
# group == 'A':
if tf == '1h':  -> set_1h_trend ................. 1h_trend_set
if tf == '15m': -> update_slot('15m_confirm') ... 15m_confirm
# tf == '5m'    -> _handle_5m_trigger ............ ENTRY
```
**Group B on 5m routes to the AI close handler. Group B on 5m has never arrived.**

**Step 3 — the armed-exit path** (`config.py`, `main.py`):
```python
EXIT_CONFIRM_TF = '15m'   # "flip to '5m' to revert exit-confirmation to 5m, no code change"
```
1H `Exit S.` + an open position → `arm_exit_pending(side)`. A subsequent structure alert in the
**opposite** direction on `EXIT_CONFIRM_TF` → `_execute_close_position()` — the close fires there.

---

## 4. Where intent and code diverge

| # | design intent | what the code does | severity |
|---|---|---|---|
| **D1** | Separate ENTRY and EXIT alert sets on 15m and 5m | **One set exists.** 15m and 5m receive the *same* LuxAlgo structure vocabulary; separation is by timeframe field only | **root cause — configuration** |
| **D2** | 1H arms → 15m confirms → **5m makes the final call** | **Two tiers.** The 15m confirmation closes the position itself (`_execute_close_position`). No third tier exists in code | **design never implemented** |
| **D3** | 5m tier decides exits | 5m is the **entry** channel — 12,762 of 15,833 5m alerts open positions | direct conflict |
| **D4** | — | `EXIT_CONFIRM_TF` selects *which single tier* confirms, `'15m'` **or** `'5m'` — it is an either/or switch, not a chain | the flag is often read as enabling the cascade; it does not |
| **D5** | Exit alerts distinguishable by intent | Distinguished by regex on the alert **name**; the vocabulary that arrives carries no intent words | the classifier matches on the wrong property |
| **D6** | — | `Exit S.` arrives `tv_tf=NULL` while 1H trend arrives `tv_tf='60m'` — two payload formats on one timeframe | configuration inconsistency |

---

## 5. Git history — when it was written, and what narrowed it

```
b9a2935  2026-05-16  refactor(isolation): hard wall between Titan (BTC) and Mercury (ETH)
                     -> _GROUP_B_RE and classify_group first appear here, unchanged since
ef1991f  2026-05-27  feat(titan): move exit-confirmation to 15m (EXIT_CONFIRM_TF flag)
                     + entry/exit isolation guards
```

**`ef1991f` is the commit that removed the 5m exit tier**, and it did so deliberately. Its own
comment states the reason:
> *"'15m' moves confirmation off the 5m entry channel for full entry/exit isolation; flip to '5m'
> to revert exit-confirmation to 5m, no code change."*

The motivation was **entry/exit isolation** — the very separation the design intends. Because there
is only one alert vocabulary, isolating exit from entry required moving exit **off** 5m entirely.
The commit added two guards (matrix-isolation, GUARD A/B) to stop 15m exit confirmations leaking
into the entry matrix.

**Has the 5m exit path ever matched anything?** No.
```
5m rows with an exit signal_type, entire database (2026-05-11 .. 2026-07-26, 17,792 rows): 0
```
It has never fired — not before `ef1991f`, not after. `_GROUP_B_RE` has been unchanged since
2026-05-16, so this is not a regression: **the 5m exit tier was never functional.**

---

## 6. Does the 1H side work as intended? Partly — the arm works, the confirmation rarely arrives

Mechanics (`state_machine.py`): `EXIT_PENDING_TTL_MINUTES = 360` (6h). `arm_exit_pending` upserts
per side and refreshes the TTL on re-arm; `is_exit_armed` lazily deletes expired rows on read;
`clear_exit_pending` runs after the confirmed close, and the arm is consumed whatever the outcome.
**Yes, the arm expires — 6 hours.**

All 24 arms, traced to their outcome inside the TTL:
```
  1  05-25 18:00   position closed itself (external, +1) after 1.1h
  2  05-25 18:00   position closed itself (external, +1) after 1.1h
  3  05-26 05:00   position closed itself (external, +7) after 1.7h
  4  05-27 04:00   position closed itself (external, +8) after 3.7h
  5  05-28 01:00   ARM EXPIRED unconfirmed
  6  05-28 15:00   position closed itself (trail, +169) after 2.8h
  7  05-28 15:00   position closed itself (trail, +169) after 2.8h
  8  06-01 11:00   position closed itself (trail, +241) after 5.9h
  9  06-04 02:00   position closed itself (trail, +442) after 0.4h
 10  06-05 15:00   position closed itself (trail, +293) after 5.6h
 11  06-13 12:00   FIRED 15m_armed_exit after 4.5h
 12  06-18 16:00   ARM EXPIRED
 13  06-23 07:00   ARM EXPIRED
 14  06-23 14:00   position closed itself (trail, +170) after 0.3h
 15  06-24 19:00   position closed itself (trail, +370) after 1.0h
 16  06-28 21:00   FIRED after 0.5h
 17  07-03 08:00   position closed itself (sl, -46) after 1.0h
 18  07-04 01:00   FIRED after 0.5h
 19  07-10 09:00   ARM EXPIRED
 20  07-14 22:00   FIRED after 4.0h
 21  07-17 06:00   FIRED after 3.7h
 22  07-21 06:00   ARM EXPIRED
 23  07-21 13:00   ARM EXPIRED
 24  07-24 17:00   ARM EXPIRED
```
```
24 arms  ->  5 fired (21%) · 12 the position closed first · 7 expired unconfirmed
```

The arming logic behaves exactly as written. The two things worth noting are behavioural, not bugs:
* **The SL/trail wins the race in half the cases** (12 of 24). The arm is usually overtaken.
* **98.5% of 15m structure alerts are discarded** — 327 `exit_unarmed_noop` against 5 that landed on
  an arm. The 15m tier fires constantly and matters almost never, because it is entry vocabulary
  being used as an exit trigger.

---

## Summary

**(a) The design is meant to be:** separate ENTRY and EXIT alert sets on 15m and 5m, and a
three-tier exit cascade — 1H Exit **arms**, 15m **confirms**, 5m **decides**.

**(b) The code actually does:** one alert vocabulary split by timeframe (5m = entry, 15m = exit
confirmation); a **two**-tier cascade in which the 15m confirmation closes the position directly;
and `EXIT_CONFIRM_TF` as an either/or switch between 15m and 5m as *the* confirming tier. The 5m
Group-B handler exists and is reachable in code, but has never been reached.

**(c) The alerts that actually arrive:** one dedicated exit alert (`Exit S.`, 1H, 61×,
`tv_tf=NULL`); 258 1H trend alerts; 332 15m structure alerts consumed as exit confirmations; 15,833
5m alerts of which 12,762 open positions and 3,071 are liquidity context. **Zero 5m exit alerts.
Zero 15m exit alerts.**

**(d) Where the break is:**
1. **CONFIGURATION — primary.** No dedicated 5m or 15m exit alert has ever been created in
   TradingView. The design's "separate exit set" does not exist. No code change can fix this.
2. **CODE — secondary and deliberate.** The three-tier cascade was never implemented; `ef1991f`
   (2026-05-27) moved confirmation to 15m *for* entry/exit isolation, precisely because only one
   vocabulary exists. The 15m tier is terminal.
3. **CLASSIFIER — consequence of 1.** `_GROUP_B_RE` matches on intent words in the alert name. The
   arriving vocabulary carries no intent words. It matches on the wrong property given what is
   actually sent.

**No fixes proposed.** Nothing was implemented, and nothing was applied.

---

Tree clean at `f7df202`; `titan.service` healthy; Mercury-SOL untouched.
Related: `reports/OPEN-ITEMS.md`, and the 19:37 exit-advisor report (diff prepared, **not applied**).
