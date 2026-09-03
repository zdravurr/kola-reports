# mercury-sol-the-adx-floor-refused-the-breakout-not-the-open-short

_2026-09-03 18:40 UTC_

---

# WHY MERCURY-SOL MISSED THE LONG — READ-ONLY POST-MORTEM

**Titan pre-flight `tools/openitems_guard.py` → exit 0.** Titan otherwise untouched.

**Mercury-SOL: nothing changed.** DB opened `file:…?mode=ro` (a write attempt on that handle
raises `OperationalError: attempt to write a readonly database` — demonstrated, §6). Config read as
text, never imported. Venue calls GET-only. Service untouched, `NRestarts=0`, PID 3422117 unchanged.

---

# 🔴 THE VERDICT, FIRST

**A LONG was proposed — 29 times in the window, 9 of them after the short was closed — and a NAMED
GATE refused it: the flat-ADX gate, `main.py:4923`, `flat market: 1h ADX 18.42 below the 20 floor —
no trend, no trade`. It fired four times inside the impulse, on the four highest-scoring LONGs of
the day. The one LONG that finally cleared the floor, at 15:05 with ADX 22.33, was refused by the
advisor under its own HARD RULE on an ask wall 0.11 % above entry — by then price was 105.13,
within 0.5 % of the top.**

**The operator's hypothesis is REFUTED, on both the code and the record.** `MAX_POSITIONS_PER_SIDE`
is per-side and is counted per-side in both places it is enforced. Over the entire 23,603-row book
there are **zero** rows where a LONG was refused for a SHORT reason. The counter-entry suppressor
(GUARD A) is real and did fire six times on this date — but its arm **expired at 10:00:10**, three
hours and forty-two minutes before the short was stopped out and **four hours before the impulse
began**. It was not armed during the run.

**The restart did NOT cost this trade.** It happened at 17:45:58 — 2 h 45 m after the peak — and it
dropped nothing: the tier slots are a SQLite table restored at boot, and the `trend_reset` (not
`group_b_logged`) at 18:00:07 proves the 1H trend survived the restart intact.

**Cost of the refusals, replayed on real 5m candles under SOL's own live contract: the two LONGs
refused before the impulse would have closed +1.52R and +0.99R (+$3.35, +$2.18). The four refused
inside the impulse would still be open at +0.27R … +0.77R, having peaked at +0.57R … +1.09R.**

---

# 1. THE MOVE, THEN THE FUNNEL

## 1a. The run window, from real Bybit candles

Bybit `linear SOLUSDT`, fetched GET-only. (This box's IP is CloudFront geo-blocked by Bybit; the
read went out through the same local SOCKS egress the bot itself uses — `tor_retry.py`.)

| | |
|---|---|
| Short vpos 42 stopped out | **13:42:12 UTC @ 101.87** |
| Base of the run | **101.17** — 5m low of the 14:00 bar, 13 min after the stop-out |
| First impulse bar | **14:20** — 5m volume 251,466 against ~25–50 k on the four bars before it |
| Peak | **105.62** — 5m bar 15:00, printed inside 15:00–15:05 |
| **Run** | **2026-09-03 13:55 → 15:05 UTC** |
| Size | **+4.40 %** (101.17 → 105.62) |
| Size in ATR | **4.74 × ATR(1h)** (ATR = 0.939 at the 13:00 close) |
| Day (09-03) | O 100.40 · H 105.62 · L 99.13 · C 104.80 → **open→close +4.38 %**, low→high +6.55 % |

The operator's read of **+4.42 %** is confirmed within measurement.

**Volume — stated exactly, not softened.** The 14:00 1h bar printed **1,386,257** and the 15:00 bar
**1,305,476**: ranks **8** and **9** of the 235 hourly bars since 2026-08-25 (96.6th / 96.2nd
percentile), and **the largest hourly bars in six days** — since 2026-08-28 16:00. They are not the
outright largest in that window (2026-08-28 14:00 printed 3,090,115, 2.2×). On the **daily** bar the
operator's read holds outright: 09-03 volume 7,958,305 is the largest of the visible days
(08-30 6.50 M · 08-31 7.03 M · 09-01 7.21 M · 09-02 7.87 M).

## 1b. Every signal, 6 h before the run to now (from 07:55 UTC)

**106 decision-bearing rows.** By type:

| signal_type | n |
|---|---|
| `open_short` (SHORT proposals) | **58** |
| **`open_long` (LONG proposals)** | **29** |
| `15m_confirm` | 6 |
| `exit_ai_dryrun` (hourly exit advisor) | 5 |
| `5m_liquidity_ctx` | 5 |
| `15m_exit_confirm` | 2 |
| `sl_triggered_short` (vpos 42's stop) | 1 |
| `1h_trend_set` · `60m_exit` · `5m_entry_suppressed_armed` · `15m_no_trend` | 1 each |

## 1c. 🔴 WHERE EACH DIED — per cause, with counts, in the window

| cause | LONG | SHORT | verbatim refusal |
|---|---|---|---|
| **HTF cascade** | 7 | 47 | `htf_blocked` — reason string not persisted on the row; reconstructed in §3d |
| **Flat/ADX gate** | **12** | 0 | `flat market: 1h ADX 18.42 below the 20 floor — no trend, no trade` |
| **Score bar** | 8 | 5 | `below_threshold` (scores 0.24 – 1.99 against the bar) |
| **Entry lock** | 1 | 2 | `concurrent LONG entry already in flight for SOL/USDT:USDT — refused, not queued` |
| **Position cap** | **0** | 4 | `max 1 SHORT position(s) already open` — **SHORT-on-SHORT, never cross-side** |
| **Counter-entry suppression** | 1 | 0 | `GUARD_A_SKIP_ENTRY tf=5m cid=liq_grab_bull dir=LONG armed_side=SHORT — exit runs on 15m, counter-entry suppressed` (08:55:05, before the run) |
| **Advisor** | **1** | 0 | `skip` — `Ask wall at $105.25 (p83, x15.3) directly above entry blocks upside; 4h NEUTRAL regime opposes momentum.` |
| **Book gate** | 0 | 0 | never fired — `book_gate_clause` is empty on the one LONG that reached it |
| **Risk halt (macro/DXY/daily-loss/loss-streak)** | 0 | 0 | none fired |

## 1d. 🔴 HOW MANY LONG PROPOSALS EXISTED? — 29

**This is not a "no signal fired" failure. LONG signals fired constantly.** 29 `open_long` rows in
the window; 72 across the whole of 09-03. Nine of the 29 arrived **after** vpos 42 closed. The
question is correctly "what blocked it", and the answer is §1c row 2.

---

# 2. 🔴 THE OPERATOR'S HYPOTHESIS — did the open short block the long?

## 2a. The position-cap code, verbatim

**`config.py:1263`**
```python
MAX_POSITIONS_PER_SIDE     = 1     # Max 1 open position per side at any time.
```

It is enforced in **two** places, and **both count per side**.

**Venue side — `main.py:2062-2071`** (inside `check_risk`), counting **exchange positions**:
```python
        positions = tor_retry.with_transport_retry(
            exchange, lambda ex: ex.fetch_positions([symbol]),
            label='positions.riskcheck')
        open_count = sum(
            1 for p in positions
            if (p.get('side') or '').upper() == position_side
            and float(p.get('contracts') or 0) > 0
        )
        if open_count >= MAX_POSITIONS_PER_SIDE:
            return False, f"max {MAX_POSITIONS_PER_SIDE} {position_side} position(s) already open"
```
`p.get('side').upper() == position_side` — a SHORT venue position is not counted when
`position_side == 'LONG'`.

**DB side — `virtual_trader.py:330-338`** (the authoritative re-check under `_entry_lock`), counting
**`virtual_positions` rows**:
```python
            n_open = conn.execute(
                "SELECT COUNT(*) FROM virtual_positions "
                "WHERE symbol=? AND position_side=? AND status='open'",
                (symbol, position_side),
            ).fetchone()[0]
            if n_open >= MAX_POSITIONS_PER_SIDE:
```
`WHERE … position_side=?` — again per side. The fast-path skip at `virtual_trader.py:209` uses the
same `_open_count(symbol, position_side)`.

**Answer: PER SIDE, in both places. It counts venue positions in the risk gate and DB rows at the
insert. Neither can see the other side.**

**Live proof from the record, not from reading:** row **23591**, `2026-09-03 13:00:09`,
`signal_type=open_long`, status `flat_adx_blocked` — with vpos 42 (SHORT) **still open**. The
flat-ADX gate sits *after* the cascade, the score gate, the entry lock **and the risk gate**
(`main.py:4880-4887`, the comment states the ordering). A LONG could only reach it by passing the
position cap while a SHORT was open. It did.

## 2b. Every counter-entry suppression during vpos 42's life

vpos 42 lived `2026-09-01 21:40:18` → `2026-09-03 13:42:12`. `entry_suppressed_armed` rows in that
span: **exactly 6, all LONG, all `armed_side=SHORT`** — the operator's post-mortem number is right
and there were no others.

| row | UTC | tf | signal | dir suppressed | armed side |
|---|---|---|---|---|---|
| 23441 | 04:25:05 | 5m | Bullish Liquidity Grab | LONG | SHORT |
| 23458 | 05:00:06 | 5m | Bullish I-CHOCH | LONG | SHORT |
| 23469 | 05:25:18 | 5m | Bullish Liquidity Grab | LONG | SHORT |
| 23502 | 07:05:04 | 5m | Bullish I-CHOCH+ | LONG | SHORT |
| 23529 | 07:50:02 | 5m | Bullish Liquidity Grab | LONG | SHORT |
| 23542 | 08:55:05 | 5m | Bullish Liquidity Grab | LONG | SHORT |

**🔴 NONE fell inside the run window, and none could have.** The arm was created by
`60m_exit_armed` at **04:00:10** (row 23439). `EXIT_PENDING_TTL_MINUTES = 360`
(`state_machine.py:29`) ⇒ it **expired at 10:00:10**. Proof it was gone: at **13:00:11** a 15m
`Bullish I-CHOCH` — which targets the SHORT side — logged `exit_unarmed_noop`
(`EXIT_CONFIRM_15M_UNARMED … nothing armed, dropped`, row 23592). The impulse began at 14:20.

*(Aside, not asked but it is on the tape: that same 13:00:11 signal would have **closed** vpos 42 at
~101.4 had the arm still been live. The arm had lapsed 3 h earlier, so the short rode to its stop at
101.87 forty-one minutes later.)*

## 2c. 🔴 Did ANY guard refuse a LONG because a SHORT was open?

**NO.** Over all 23,603 rows:

```
open_long rows whose refusal reason mentions 'SHORT'  : 0
open_short rows whose refusal reason mentions 'LONG'  : 0
```

Every `risk_halt` is same-side (`144 × open_short :: max 1 SHORT position(s) already open`,
`115 × open_long :: max 1 LONG position(s) already open`) or side-agnostic (loss-streak cooldown,
macro NFP blackout, fail-closed venue read).

**GUARD A is the only mechanism in the codebase with the shape the operator suspects**, and it is
worth naming as a structural fact even though it is not this trade's cause. `main.py:5960-5978`:

```python
        if tf == '5m' and armed:
            insert_signal(symbol, 'na', '5m_entry_suppressed_armed', tv_tf='5m',
                          tv_action=signal_name, status='entry_suppressed_armed')
            print(f"{LOG_PREFIX}GUARD_A_SKIP_ENTRY tf=5m cid={matrix_cid} "
                  f"dir={matrix_dir} armed_side={target_side} — exit runs on 15m, "
                  f"counter-entry suppressed", flush=True)
```

It keys on `state_machine.is_exit_armed(target_side)` — **armed for exit**, not merely open — so it
is narrower than "a short blocks a long". **Over the whole record it has fired 61 times: 32 of them
suppressed a LONG-direction 5m confirmation while a SHORT was armed, 29 the mirror.** It also
suppresses the matrix record for the same signal (`_skip_matrix = True`, `main.py:5905-5911`), so a
suppressed bullish confirmation does not even reach the confluence score. That is structural and
worth its own measurement — **but it is not what happened here**, because the arm was expired.

## 2d. LONG proposals AFTER 13:42:12, and what happened to each

**Nine.** The side was free for every one of them.

| row | UTC | price | score | outcome | verbatim |
|---|---|---|---|---|---|
| 23601 | 14:25:03 | 102.43 | −10.0 | `htf_blocked` | 15m/MOMENTUM tier OPPOSED (§3d) |
| 23602 | 14:25:04 | 102.44 | −10.0 | `htf_blocked` | same |
| 23606 | 14:35:02 | 102.65 | 2.25 | **`flat_adx_blocked`** | `flat market: 1h ADX 18.42 below the 20 floor — no trend, no trade` |
| 23608 | 14:45:08 | 102.78 | **4.00** | **`flat_adx_blocked`** | `… 1h ADX 18.42 below the 20 floor …` |
| 23610 | 14:50:01 | 103.88 | **4.75** ← highest LONG score of the day | **`flat_adx_blocked`** | `… 1h ADX 18.42 below the 20 floor …` |
| 23612 | 14:55:03 | 103.78 | 2.25 | **`flat_adx_blocked`** | `… 1h ADX 18.97 below the 20 floor …` |
| 23613 | 14:55:05 | — | 2.85 | `entry_gate_refused` | `concurrent LONG entry already in flight for SOL/USDT:USDT — refused, not queued` (it collided with 23612, which the ADX floor was refusing) |
| 23618 | 15:05:04 | 105.13 | 2.25 | **`ai_skipped`** | `Ask wall at $105.25 (p83, x15.3) directly above entry blocks upside; 4h NEUTRAL regime opposes momentum.` |
| 23627 | 16:00:23 | — | −5.25 | `htf_blocked` | 15m/MOMENTUM tier OPPOSED (§3d) |

---

# 3. THE GATES, EACH CHECKED AGAINST THE TAPE

## 3a. `trend_1d` / `trend_4h` during the run

Captured on the rows themselves (`skip_attribution.trend_1d/trend_4h`, and `trades` on the advisor
path):

| when | `trend_1d` | `trend_4h` |
|---|---|---|
| 2026-09-01 21:15 → 2026-09-03 05:40 | **neutral** | bear → neutral |
| 2026-09-03 **08:00 → 12:40** | **neutral** | neutral |
| 2026-09-03 **14:05 → 15:50 (the run)** | **bull** (ADX 49.9) | **neutral** (ADX 23.2) |
| 2026-09-03 16:00 onward | bull | **bull** |

The daily label the operator remembers going NEUTRAL at 18:00 on 1 Sep **had flipped back to BULL
by 14:05 on 3 Sep** — before the impulse. It was not against the LONG.

**The 4H was, and the standing order engaged on it.** Advisor system prompt, line 3:

> *"Treat the 1d and 4h trends as the dominant regime"*

and the advisor's own recorded reason names it: *"4h NEUTRAL regime opposes momentum."* The 4h label
only turned `bull` at 16:00 — an hour after the top.

## 3b. ADX(1h) against the 20.0 floor — 🔴 CONFIRMED, and this is the cause

`ADX_BELOW_FLOOR = 20.0` (`config.py:634`). `FLAT_ADX_GATE_ENABLED = True`,
`FLAT_ADX_GATE_DRYRUN = False` — *"🔴 ARMED. This gate REFUSES ENTRIES."* (`config.py:406-407`).

```python
        _flat_adx = _adv_snap.get('srv_adx_1h')
        if FLAT_ADX_GATE_ENABLED and isinstance(_flat_adx, (int, float)) \
                and _flat_adx < ADX_BELOW_FLOOR:
```
— `main.py:4922-4924`.

**The operator's expectation ("a +4.4 % day should clear it easily") is REFUTED by the tape.** ADX is
doubly Wilder-smoothed; a breakout out of a compressed regime starts *below* the floor by
construction, and clears it only after the move is spent. Closed-bar ADX(1h) across 09-03:

| 1h close | 11:00 | 12:00 | 13:00 | **14:00** | **15:00** | 16:00 | 17:00 | 18:00 |
|---|---|---|---|---|---|---|---|---|
| ADX(1h) | 15.43 | 15.97 | 16.68 | **19.43** | **22.33** | 25.03 | 27.54 | 29.88 |
| close | 100.75 | 101.61 | 101.41 | **104.78** | **105.12** | 104.54 | 105.06 | 104.81 |

**The entire impulse printed inside the 14:00 bar, whose ADX closed at 19.43 — 0.57 short of the
floor. The floor was first cleared at the 15:00 close, at 105.12, with the move already over.**

**I independently recomputed the bot's own reading** (`pandas_ta.adx(length=14)`, last value, forming
1h bar rebuilt from real 5m candles) and it reproduces exactly:

| as-of | recomputed | bot logged | delta |
|---|---|---|---|
| 13:00:09 | 16.4659 | 16.4659 | −0.00 |
| 14:35:14 | 18.4167 | 18.4166 | +0.00 |
| 14:45:20 | 18.9206 | 18.4166 | **+0.50 (stale)** |
| 14:50:10 | 18.9679 | 18.4166 | **+0.55 (stale)** |
| 14:55:13 | 19.4322 | 18.9679 | **+0.46 (stale)** |
| 15:05:20 | 22.3324 | 22.3324 | −0.00 |

**There IS a staleness defect** — `_CACHE_TTL_BY_TF['1h'] = 300.0` (`indicators.py:62`) served the
same 18.4166 across a 15-minute span. **It did NOT cost this trade, and I will not dress it up as
if it did:** the true value at every refusal (18.42 / 18.92 / 18.97 / 19.43) was still below 20.0.
The gate would have refused all four on fresh numbers too.

**This is structural, not an incident.** Since the gate armed on 2026-08-17 it has refused **372**
entries — **192 LONG, 180 SHORT**. Its own drift observatory records what the LONG refusals gave up:

| direction | n | avg max-favourable | max | n with MFE ≥ 1 % |
|---|---|---|---|---|
| **LONG** | **192** | **+3.448 %** | **+10.043 %** | **156 of 192 (81 %)** |
| SHORT | 180 | +2.258 % | +5.707 % | 113 of 180 (63 %) |

## 3c. The book gate — it did not fire

The only LONG that reached it was row 23618. `book_gate_clause` is the **empty string** — no clause.
Clause A needs `opp_pctl >= BOOK_GATE_WALL_PCTL (90.0)` **and**
`opp_dist_pct <= BOOK_GATE_WALL_DIST_PCT (0.20)`. The row carries
`book_gate_opp_pctl = 56.7`, `book_gate_opp_dist_pct = 0.114`, `book_gate_opp_mult = 15.3`,
`book_gate_lean = 0.5234`, `n_supporting = 1`. Distance qualified; **percentile did not** → admitted.

🔴 **And then the advisor refused the same wall.** Its prompt rendered that ask wall as **p83** on
the prompt's own 23,080-wall distribution, and the system prompt's HARD RULE says:

> *"HARD RULE — opposing walls: if a massive limit wall … sits directly above a LONG entry … you
> MUST reply 'skip'."*

Two rulers on one wall — 56.7 to the gate, 83 to the advisor — reaching opposite conclusions. The
divergence is deliberate and documented (`book_gate.py:30-31`: *"THE RULER … deliberately NOT
`claude_advisor._WALL_MULT_PCTL_BREAKS`"*); the record here is what it costs.

## 3d. The cascade — which tier opposed

The cascade tiers are the **matrix category net directions** (`signal_matrix.htf_alignment`,
`main.py:4092-4098`), not the raw slots: `1H` = TREND, `15m` = MOMENTUM, `5m` = EXECUTION.

**On the two LONG blocks at 14:25** the MOMENTUM tier held `HyperWave OB Signal Down`
(15m, SHORT, w = 1.0, written 14:15:08) and nothing bullish yet — `HyperWave Signal Up` did not
arrive until 14:30:15. **The 15m/MOMENTUM tier OPPOSED**; penalised score −10.0.
**On the 16:00:23 block** MOMENTUM held `Reversal Down +` (15:30:11) and
`HyperWave OB Signal Down` (15:45:09), both SHORT — **15m/MOMENTUM OPPOSED**, score −5.25.
*(The block-reason string is built at `main.py:4131` for the Telegram card only and is not persisted
to the row or to stdout; the above is reconstructed from the MOMENTUM slot writes in journald plus
the stored matrix breakdown.)*

**From 14:35 to 15:05 the cascade ADMITTED every LONG** —
`HTF_WOULD_PASS (tolerate-NEUTRAL) LONG 1H=LONG 15m=NEUTRAL 5m=LONG`. The cascade is not the culprit
in the impulse.

🔴 **But look at why the score was so low.** Row 23618's stored breakdown, at the top of a +4.4 % day:

```json
{"TREND":     {"long_points":2.25,"short_points":0.0,"net_direction":"LONG",   "contribution":2.25},
 "MOMENTUM":  {"long_points":1.75,"short_points":2.5,"net_direction":"NEUTRAL","intra_conflict":true,"contribution":0.0},
 "LIQUIDITY": {"long_points":1.75,"short_points":1.25,"net_direction":"NEUTRAL","intra_conflict":true,"contribution":0.0},
 "EXECUTION": {"long_points":1.25,"short_points":2.5,"net_direction":"NEUTRAL","intra_conflict":true,"contribution":0.0}}
```

**Three of four tiers cancelled themselves to zero.** Bearish LuxAlgo signals kept firing straight
through the rally — 47 `open_short` proposals in the same window against 29 LONG — and each one
neutralised its bullish twin. The whole impulse scored **2.25 points, from the 1H TREND tier alone.**

### The `60m_exit / trend_reset` at 18:00:07

`60m_exit` → Group B → `reset_1h_trend()` returned `had_trend=True` ⇒ status **`trend_reset`**
(`main.py:5998-6002`). It set `1h_context` to NEUTRAL and cleared the 15m and 5m slots
(`_clear_lower_tfs_locked`); `market_state_snapshot` shows all three rows stamped `18:00:06`.

**What that costs going forward:** with the 1h trend unset, `is_trend_set()` is False and 5m/15m
signals fall into the `logged_no_trend` branch — **no entry of either direction can be taken until a
1h TREND signal re-arms it.** Already visible: row 23640, `18:30:11`, `HyperWave Signal Down`,
status **`no_trend`**.

**Was the run already underway? It was already OVER.** The peak was 15:00–15:05; the reset is at
18:00:07, **3 hours later.** It cost nothing on this trade.

---

# 4. 🔴 THE RESTART — RULED OUT, WITH EVIDENCE

Stop 17:45:45 → 17:45:58, worker up 17:46:17, PID 3422246 (master 3422117). `NRestarts=0`
(a clean stop+start, not a crash loop).

## 4a. Did it drop, reset or expire any tier state a LONG needed? — **No.**

**The tier slots are a SQLite table, not memory.** `state_machine.py:193` persists every slot write
into `market_state_snapshot`; `state_machine.py:170 _restore_from_snapshot()` reloads all three at
`init_db()`. `exit_pending`, `live_context_state` and `virtual_positions` are likewise tables.

**Before → after, the slots that mattered:**

| slot | immediately before 17:45:45 | immediately after 17:46:17 |
|---|---|---|
| `1h_context` (TREND) | LONG — `Smart Trail Switch Bullish`, set 13:00:12 | **LONG — survived** |
| `15m_confirm` (MOMENTUM) | LONG — `HyperWave Signal Up`, written 17:45:02 (row 23637 `confirm_recorded`) | **preserved** — `live_context_state` still carries `hw_signal_up LONG last_seen 2026-09-03T17:45:02` |
| `5m_trigger` | empty | empty |
| `exit_pending` | empty (arm expired 10:00:10) | empty |
| `virtual_positions` open | 0 | 0 — `[VPOS-RECONCILE] no open positions at boot — clean.` |

**🔴 The decisive proof the 1H tier survived:** at 18:00:07, *after* the restart, the `60m_exit`
logged status **`trend_reset`** — not `group_b_logged`. That status is only reachable when
`reset_1h_trend()` finds a trend **already set** (`main.py:5998`). Had the restart cleared it, the
row would read `group_b_logged`.

## 4b. 🔴 Did the restart cost this trade? — **NO. Stated plainly.**

The peak was **15:00–15:05**. The restart was **17:45:58 — 2 h 45 m later.** Every LONG proposal in
this post-mortem was raised, evaluated and refused by the *pre-restart* process (PID 1196944). The
tier-age prompt change cost nothing here. **If it had, it would be named as a cost of that change;
it did not, and inventing one would be as dishonest as hiding one.**

## 4c. The `60m_exit / trend_reset` at 18:00:07

Answered in §3d: it reset the 1H trend slot and cleared the lower tiers, it gates *future* entries
until a 1h trend re-arms, and **the run was already over by three hours.**

---

# 5. WHAT IT WOULD HAVE MADE

**Contract as specified, read from the code as text (never imported):** SL = entry − 2.5 × ATR(1h)
(`config.py:62`); arm = entry + 0.75 × 2.5 × ATR(1h) (`trail_arm.activation_distance`, `TRAIL_ARM_R
= 0.75`); breakeven lock at entry × 1.0020 (`trail_arm._BE_TARGET_FRAC_ON`); trail =
`water_mark × (1 − trail_pct/100)` with `trail_pct = round(round(1.875 × ATR, 2)/entry × 100, 3)`,
armed **only after** the BE lock fires (`virtual_trader.py` management tick); taker **0.100 % both
legs** (venue rate, boot line 17:46:17); notional **$100**; **adverse extreme first within each 5m
bar**. Entry prices are the bot's own recorded `skip_attribution.price_at_skip`. Tape: real Bybit 5m
candles to 18:20 UTC.

| refused LONG | fill | ATR(1h) | SL | arm | trail % | 1R | outcome | net | **R** | peak (peak R) |
|---|---|---|---|---|---|---|---|---|---|---|
| 23549 · 11:00 · ADX 15.36 | 100.32 | 0.882 | 98.12 | 101.97 | 1.645 | $2.20 | **trail @ 103.88, 15:45** | **+$3.35** | **+1.52R** | 105.62 (+2.31R) |
| 23591 · 13:00 · ADX 16.47 | 101.44 | 0.899 | 99.19 | 103.13 | 1.666 | $2.22 | **trail @ 103.86, 15:45** | **+$2.18** | **+0.99R** | 105.62 (+1.77R) |
| 23606 · 14:35 · ADX 18.42 | 102.65 | 1.009 | 100.13 | 104.54 | 1.841 | $2.46 | still open | +$1.89 | +0.77R | 105.62 (+1.09R) |
| 23608 · 14:45 · ADX 18.42 | 102.78 | 1.062 | 100.13 | 104.77 | 1.936 | $2.58 | still open | +$1.76 | +0.68R | 105.62 (+0.99R) |
| 23610 · 14:50 · ADX 18.42 | 103.88 | 1.068 | 101.21 | 105.88 | 1.925 | $2.57 | still open | +$0.68 | +0.27R | 105.62 (+0.57R) |
| 23612 · 14:55 · ADX 18.97 | 103.78 | 1.133 | 100.95 | 105.90 | 2.043 | $2.73 | still open | +$0.78 | +0.29R | 105.62 (+0.58R) |
| **23618 · 15:05 · ADVISOR skip** | 105.13 | 1.120 | 102.33 | 107.23 | 1.998 | $2.66 | still open | **−$0.51** | **−0.19R** | 105.21 (−0.05R) |

"Still open" positions are marked to the last tape print, **104.80 at 18:20 UTC**; none of them ever
armed its trail low enough to be stopped (the deepest retrace, 103.73 at 15:45, cleared 23606's
trail stop of 103.68 by 5 cents — the outcome of the four open rows is that finely balanced and is
reported as such, not rounded into a claim).

**Read the last row honestly: the ADVISOR'S skip was the least costly refusal of the seven.** By
15:05 the trade was −0.19R. The money was lost at the **ADX floor**, between 11:00 and 14:55 — and
most of it before the impulse even started.

**Method check:** the replay's ATR(1h) at 15:05:19 recomputes to 1.1203 against the bot's stored
`srv_atr_1h = 1.1125` (+0.7 %), the difference being my 5m-reconstructed forming bar and a shorter
history than the bot's 200-bar fetch. The ADX reproduction in §3b is exact to 4 decimals.

---

# 6. 🔴 READ-ONLY CONFIRMATION

| claim | evidence |
|---|---|
| **DB read-only** | every connection `file:/…/trades.db?mode=ro`, `uri=True`. A `CREATE TABLE` on that handle returned `OperationalError: attempt to write a readonly database` |
| **cwd outside SOL's tree** | all work in `/tmp/claude-0/…/scratchpad`; `pwd` verified |
| **config not imported** | `config.py`, `main.py`, `virtual_trader.py`, `state_machine.py`, `trail_arm.py`, `book_gate.py`, `indicators.py`, `tor_retry.py` read with `sed`/`grep` only, cited by line |
| **no writes** | code + `.env` md5 identical before and after — 34 of 34 files byte-identical |
| **trades.db md5 changed** | ✅ expected and **not mine**: the LIVE bot wrote rows 23639 (`18:25:01 context_recorded`) and 23640 (`18:30:11 no_trend`) during the session. `virtual_positions` still 36 rows, 0 open |
| **no orders placed or cancelled** | no venue write call issued; only `GET /v5/market/kline` |
| **service untouched** | `ActiveState=active`, `SubState=running`, `ExecMainPID=3422117`, `ExecMainStartTimestamp=Thu 2026-09-03 17:45:58 UTC` — unchanged |
| **`NRestarts` unchanged** | `NRestarts=0` before, `NRestarts=0` after |
| **Titan** | `openitems_guard.py` exit 0; not touched otherwise |

*No change proposed. No change applied.*

---

## ONE-LINE ANSWER

**A LONG was proposed 29 times and a NAMED GATE refused it — the flat-ADX floor
(`main.py:4923`, `1h ADX < 20.0`), which by construction cannot clear until a breakout out of a
compressed regime is already over; the open short did not block it, the restart did not cost it, and
the advisor's skip at 15:05 was worth −0.19R by the time it fired.**
