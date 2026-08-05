# TITAN — AUDITING THE MECHANISMS: **THE CODE IS NOT CLEAN. AND THE WORST §4 INSTANCE IS A COMMIT I MADE THREE HOURS AGO.**

**2026-08-05 19:55 UTC · READ-ONLY · nothing changed, NOTHING PROPOSED, NO DIFF · HEAD `de1d0f2`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
`git status` clean before and after · `trades.db` read-only, **absolute path pinned** ·
**0 open positions** throughout · **Mercury-SOL never opened.**

Parent: `2026-08-05-1925-titan-audit-every-prompt-rule-for-the-unsatisfiable-defect.md`, whose scope
note said *"non-prompt mechanisms (gates, cascade, geometry) were not audited."* This is that audit.

---

## ANSWER IN ONE LINE

🔴 **THE CODE IS NOT CLEAN. Four mechanisms have never executed once, one worker has polled an empty
queue every 5 seconds since it was built, four refusing mechanisms produce refusals nobody can count
— and §4's "fixed in one place only" form has a fresh instance that I committed at 19:08 today,
three hours after naming the pattern.**

| # | finding | runs |
|---|---|---|
| **1** | 🔴 **The entire EQH/EQL liquidity-sweep mechanism has never fired.** 0 of 20,721 signals ever carried an EQH/EQL type; `liquidity_sweep_state` empty; `status='liquidity_sweep'` never written | entry path, **every signal** |
| **2** | 🔴 **The 60-minute MFE tracker is nested inside that dead handler** — `mfe_tracking` empty, and its four output columns on `trades` are **all-NULL across 20,721 rows** | every close, in principle |
| **3** | 🔴 **`breakeven_worker` has never received a job.** `breakeven_jobs` is empty for the life of the table; the only enqueue site sits in a function the live entry path does not use. The worker starts on every boot and polls **every 5 s** | **every 5 s, forever** |
| **4** | 🔴 **§4 — `1ec2477` (mine, today 19:08) updated the percentile guidance in the entry prompt and left the exit prompt's copy at the old wording** | every consultation |
| **5** | **Four refusing mechanisms write no attribution row** — `risk_halt` (137), `virt_cap_blocked` (118), `claude_unavailable` (26), `failed` (3). Their refusals cannot be counted or drift-tested | 75 halts in 30 d |
| **6** | **20 all-NULL columns on `trades`** across 20,721 rows | — |
| **7** | ✅ **`context_weight` — a live entry-sizing input that can only ever return 1.0** | every entry |

**And what is clean matters:** `virtual_positions` and `skip_attribution` have **zero** all-NULL
columns; every module resolves `DB_PATH` to the same file; the money brakes fixed by `3316e8a` are
**demonstrably firing** (75 halts in 30 days, against "inert since May"); `sensor_events` writes
`recheck_events` and `adaptive_trail_events` and is alive.

---

## §1 — EVERY GATE, VETO AND BRAKE: DOES IT DO WHAT ITS NAME SAYS?

### 1a/1b. THE FIRING COUNTS — ALL TIME AND LAST 30 DAYS

| mechanism | claims to | all time | last 30 d | verdict |
|---|---|---|---|---|
| `htf_blocked` (HTF cascade) | refuse when higher TFs oppose | **11,116** | 4,213 | ✅ fires |
| `below_threshold` (score gate) | refuse below the confluence bar | 1,031 | 712 | ✅ fires |
| `ai_skipped` (entry advisor) | refuse on the model's verdict | 2,658 | 656 | ✅ fires |
| `ema_envelope_blocked` | decline a flat market (shipped 2026-08-04) | **20** | 20 | ✅ fires — new, on track |
| `risk_halt` (money brakes) | halt entries on aggregate risk | **137** | **75** | ✅ **fires — the `3316e8a` fix is confirmed live**, against "inert since May" |
| `virt_cap_blocked` | cap concurrent virtual positions | 118 | 30 | ✅ fires |
| `exit_unarmed_noop` | record a no-op exit | 387 | 172 | ✅ fires |
| 🔴 **EQH/EQL smart TP** | close on a liquidity sweep | 🔴 **0** | 🔴 **0** | 🔴 **NEVER** — §1d |
| 🔴 **breakeven job registration** | arm the trail / move SL to BE at +1R | 🔴 **0** | 🔴 **0** | 🔴 **NEVER** — §1d |
| 🔴 **MFE tracker** | measure PnL missed after a close | 🔴 **0** | 🔴 **0** | 🔴 **NEVER** — §1d |

### 1c. 🔴 REFUSALS THAT CANNOT BE COUNTED — THE FLAT-FLOOR DEFECT, STILL PRESENT IN FOUR PLACES

`skip_attribution` carries **four** statuses: `htf_blocked`, `ai_skipped`, `below_threshold`,
`ema_envelope_blocked`. Every other refusing status exists **only** in `trades`, with no attribution
row and therefore **no drift sample and no countable refusal population**:

| status | all time | 30 d | what is lost |
|---|---|---|---|
| 🔴 `risk_halt` | **137** | **75** | the money brakes refuse 2–3 entries a day and **not one is drift-tested**. §2.54's whole method is unavailable to them |
| 🔴 `virt_cap_blocked` | 118 | 30 | same |
| `claude_unavailable` | 26 | 1 | the fallback path's refusals |
| `failed` | 3 | 2 | — |

**This is exactly the shape that hid 518 FLAT-floor refusals for a month:** the mechanism works, and
the evidence that it works is not in the table anyone queries. **`risk_halt` at 75 in 30 days is the
second-most-active refusing mechanism after the cascade and the score gate, and it is invisible to
every study in this book.**

### 1d. 🔴 CAN THEY FIRE AT ALL? — THREE TRACED TO SOMETHING THAT CANNOT BE TRUE

#### THE EQH/EQL MECHANISM — DEAD AT THE FIRST CONDITION

`liquidity_sweep.SWEEP_TYPES = ('EQH', 'EQL')`, and `record_sweep()` returns early on
`sweep_type not in SWEEP_TYPES`.

| | |
|---|---|
| distinct `signal_type` values ever seen | `open_short`, `open_long`, `5m_liquidity_ctx`, `15m_exit_confirm`, `1h_trend_set`, `15m_confirm`, `exit_ai_dryrun`, `60m_exit`, `60m_exit_armed`, `1h_window_open`, `15m_armed_exit`, `close_long`, `buy` |
| 🔴 rows whose `signal_type` contains `EQ` | 🔴 **0 of 20,721** |
| `liquidity_sweep_state` rows | **0** |
| `trades` rows with `status='liquidity_sweep'` | **0** |
| `EQH_EQL_SMART_TP_ENABLED` | **True** |

**The flag reads armed. The handler has never run. This is the same string-comparison death as the
money brakes' `signal_type` filter — except that one was fixed and this one is still open.**

#### 🔴 AND IT TAKES A SECOND, UNRELATED MECHANISM DOWN WITH IT

`mfe_tracker.enqueue(...)` — the 60-minute tracker built *"so the optimizer can later judge 100 %
close vs partial-close + trail"* — is called at `main.py:3643`, **which is inside
`_handle_liquidity_sweep()`** (def at 3526). The dead handler is the tracker's only caller.

Confirmed from two independent directions: `mfe_tracking` has **0 rows**, and the four MFE output
columns on `trades` — `mfe_window_minutes`, `mfe_max_price`, `mfe_pnl_missed`, `mfe_completed_at` —
are **NULL on all 20,721 rows**.

**One unreachable handler silently disabled an unrelated measurement mechanism, and nothing anywhere
reports an absence.**

#### 🔴 THE BREAKEVEN WORKER — A 5-SECOND POLL LOOP OVER AN EMPTY QUEUE

`breakeven_jobs`: **0 rows.** There is **no `DELETE`** in `breakeven_worker.py` — completed jobs are
marked `status='superseded'`, never removed — so an empty table means **`enqueue()` has never
succeeded, ever.**

The only enqueue site is `main.py:1518`, inside **`_execute_entry()`**. The observed live entry of
2026-08-03 20:25 routed elsewhere:

```
[ADAPTER] LIVE ENTRY BTC/USDT:USDT LONG 0.0023 @ 63920.2 fee=0.073508
VIRTUAL ENTRY vpos=92 LONG amount=0.0023 @ 63920.2 atr=75.41 sl=63139.3 ...
```

`[ADAPTER] LIVE ENTRY` is printed by `order_adapter.market_entry()`, whose **only caller is
`virtual_trader.execute_entry()`** — not `main._execute_entry()`. **No `BE_ENQUEUED` line appears in
the journal at any point in its retained history, and no `breakeven enqueue failed` either** — the
line was not reached rather than reached and thrown.

Meanwhile the comment at the enqueue site still asserts the mechanism:

> *"Trailing stop is NOT placed at entry anymore (Stage 3). **The breakeven worker arms it — and
> moves the SL to breakeven — once price reaches +1R.** Register the management job"*

✅ **THE FUNCTION IS COVERED ELSEWHERE — stated so this is not read as an unprotected position.**
`virtual_trader.py:2643` performs the arming (`SL→{be_price} (trail armed)`), and
`adaptive_trail_events` has rows. **What is dead is the `breakeven_worker` mechanism, not the
breakeven behaviour.** The worker nonetheless starts on every boot — *"breakeven_worker started
(interval=5s)"*, observed on **14 boots** in the retained journal — and polls an empty table every
five seconds indefinitely.

⚠️ **Precision about what I did and did not establish:** `_execute_entry()` is still referenced at
`main.py:2358` and `4372` on the `ai_decide == 'execute'` fall-through, so I do **not** claim it is
unreachable dead code. What is established is that **the live path observed on 2026-08-03 bypassed
it, and the job table has been empty for the entire life of the bot.**

#### `context_weight` — REACHABLE, RUNS ON EVERY ENTRY, AND CAN ONLY RETURN ONE ANSWER

`liquidity_sweep.context_weight()` is called at `main.py:4129` on every entry and returns a **margin
multiplier**. It reads `get_last_sweep_time()` — from the permanently empty
`liquidity_sweep_state`. `is_recent(None, …)` is always false, so it returns `(1.0, False, 0.0)`
**unconditionally**.

Confirmed in the data: `trades.context_weight_score` is **`0.0` on 3,009 rows and NULL on 17,712 —
no other value has ever been stored.**

**This is §2.45b's shape — a value computed, stored and displayed that reaches no live `if` — except
here it is an input to position sizing.** It is harmless *because* it is constant; it is a defect
because nothing says so.

---

## §2 — EVERY FLAG THAT READS AS ARMED

**32 booleans in `config.py`.** Those whose armed state does not match their effect:

| flag | value | reality |
|---|---|---|
| 🔴 `EQH_EQL_SMART_TP_ENABLED` | **True** | 🔴 **handler unreachable — 0 EQH/EQL signals ever.** Reads armed, has never gated anything |
| ✅ `AI_ADVISOR_HIDE_1H` | **False** | fixed today (`de1d0f2`); it had removed a parenthesis and left the adjective |
| `EMA_ENVELOPE_REFUSAL_CARD` | False | ✅ **deliberately** muted 2026-08-04 (`b9081ad`), replaced by the daily silence ledger |
| `WALL_TRAIL_LIVE_ENABLED` | False | ✅ deliberate — the wall trail is observational |
| `HTF_NEUTRAL_REQUIRE_15M_DRYRUN` | False | ✅ enforcing, consistent with `HTF_NEUTRAL_REQUIRE_15M_AGREE=True` |
| `DXY_HALT_DRYRUN` · `FILTER_ENFORCEMENT_DRYRUN` · `TREND_REVERSAL_EXIT_DRYRUN` · `ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN` · `SMART_EXIT_DRYRUN_ENABLED` · `WALL_ANCHOR_DRYRUN_ENABLED` | True | ✅ **honestly named** — `_DRYRUN` in the identifier, observational by design. Not defects |

**The remaining 24 match their behaviour.** The dry-run family is worth noting as the *good* pattern:
**a flag whose name contains its own limitation cannot read as armed.**

---

## §3 — WRITERS AND READERS

**(a) tables with a writer that has never written:** `liquidity_sweep_state`, `mfe_tracking`,
`breakeven_jobs` — all three covered above. *(`exit_pending` is empty and correct: it is transient
and there is no open position.)*

**(b) 🔴 columns written by nobody — 20 of 149 on `trades`, across 20,721 rows:**

| group | columns | reading |
|---|---|---|
| 🔴 **MFE outputs** | `mfe_window_minutes`, `mfe_max_price`, `mfe_pnl_missed`, `mfe_completed_at` | **second, independent confirmation that the tracker never ran** |
| TradingView strategy fields | `tv_pair`, `tv_market_position`, `tv_contracts`, `tv_order_price`, `signal_time` | the alert format never carried them |
| LuxAlgo detail | `lux_strength`, `lux_volatility`, `lux_intensity`, `lux_sensitivity` | never populated |
| macro / liquidation | `mc_recent_liq_long_usd`, `mc_recent_liq_short_usd`, `mc_ls_ratio` | never populated |
| misc | `volume`, `ema_9`, `ema_21`, `signal_type_ctx` | computed elsewhere or abandoned |

✅ **`virtual_positions` (44 cols) and `skip_attribution` (24 cols) have ZERO all-NULL columns.** The
tables that carry the book and the refusals are fully written.

**(c) columns whose meaning differs by branch:** `confluence_score` remains the known instance —
**§0 records it as holding FOUR quantities by status**, with `executed` rows holding RAW. Already
documented; not re-derived here. No new instance found, but note that the `trades` table carries
**149 columns** across every status, which is the structural condition that produced it.

**(d) init/migration functions with no caller:** ✅ **none found.** `init_db()` exists in
`sensor_events`, `breakeven_worker`, `liquidity_sweep`, `mfe_tracker`, `post_exit_observatory`; each
is invoked (several at import). `sensor_events` — the one that previously had no caller — is
**alive**: `recheck_events` 53 rows, `adaptive_trail_events` 4 rows.

**And a check that came back clean:** every module resolves `DB_PATH` to
`/root/titan-bot/trades.db` — `main`, `breakeven_worker`, `mfe_tracker`, `liquidity_sweep`,
`sensor_events`. **No split-brain database.** This was checked because an empty table is exactly what
a diverging `DB_PATH` looks like.

---

## §4 — 🔴 THE THIRD FORM: FIXED IN ONE OF TWO PLACES

Two weeks of commits reviewed. **One instance found, and it is three hours old.**

`1ec2477` (**mine, today 19:08**) rewrote the entry prompt's order-book NOTE. The **same NOTE exists
twice** in `claude_advisor.py` — once for the entry advisor, once for the exit advisor:

```
ENTRY  (line 304-308, REWRITTEN by 1ec2477):
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile printed with each wall:
  ~50th percentile is ORDINARY and not significant; 90th+ is genuinely thick.

EXIT   (line 828-830, UNTOUCHED):
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile: ~50th is ORDINARY.
```

🔴 **The exit advisor never received the `90th+` anchor.** The entry advisor is now told where
"genuinely thick" begins; the exit advisor — **the only measured positive in this system** — is still
told only where "ordinary" is, and is left to infer the upper bound.

⚠️ **Severity, stated honestly: this is a DIVERGENCE, not a falsehood.** The exit copy is not wrong,
only less complete, so it is materially milder than `c307bb7`'s case. **But it is structurally
identical, and I introduced it hours after writing the report that named the pattern** — which is the
strongest possible evidence that naming a defect class does not protect you from it. The 19:25 report
said this form *"cannot be found by re-reading the report that fixed it"*; it also cannot be found by
having just written that sentence.

**Everything else checked and clean:**

| fix | did the claim live elsewhere? |
|---|---|
| `de1d0f2` trail claim (today) | ✅ **checked** — `_CLOSE_SYSTEM` (the non-rich prompt, line 155) states it **correctly**: *"active ONLY once it has armed at +1R"*. Other `+1R` references (`config.py:211`, `virtual_trader.py:2663`, `main.py:2998`) are comments and are accurate |
| `de1d0f2` combo-weight thresholds | ✅ the `$15/$20` constants live in `signal_weights.record_outcome` (the mechanism itself, correctly) and in two docstrings that **already stated the inertness**. No third prompt copy |
| `1ec2477` wall percentile **baseline** | ✅ the exit side ranks max-against-max — **apples-to-apples, verified in the 19:25 audit**. The baseline defect was entry-only |
| `3316e8a` money brakes | ✅ confirmed firing (75 in 30 d) |
| `ca90c2f` grade-requires-closure | ✅ no second grading site found |

---

## §5 — VERDICT, RANKED BY HOW OFTEN THE AFFECTED MECHANISM RUNS

| # | finding | frequency | severity |
|---|---|---|---|
| **1** | 🔴 **`breakeven_worker` polls an empty queue every 5 s and has never held a job**; its stated role (arm the trail, move SL to breakeven at +1R) is performed by `virtual_trader` instead | **every 5 s, since it was built** | 🔴 **HIGH.** Not a money risk — the behaviour is covered — but a whole worker, its table and its comment describe a mechanism that has never run once |
| **2** | 🔴 **`context_weight` returns 1.0 unconditionally**, from a table that can never populate — and it is an **entry-sizing** input | **every entry** | 🔴 **HIGH by position.** Inert, so harmless today; a live sizing input whose only possible value is the identity |
| **3** | 🔴 **Four refusing mechanisms write no attribution row** — `risk_halt` 75 in 30 d is the third-most-active refusal in the bot and is **invisible to every drift study** | **~2–3/day** | 🔴 **HIGH.** This is the FLAT-floor defect, unfixed, in four places |
| **4** | 🔴 **§4 — the exit prompt's percentile NOTE never got the `90th+` anchor** the entry prompt got at 19:08 today | **every consultation** | **MEDIUM.** A divergence, not a falsehood — but the freshest proof the class is still live |
| **5** | 🔴 **EQH/EQL smart TP has never fired; `EQH_EQL_SMART_TP_ENABLED` reads True** | **evaluated every signal** | **MEDIUM.** Nothing is lost while it is dead, but a True flag over an unreachable handler is precisely what this audit hunts |
| **6** | 🔴 **The MFE tracker is nested inside the dead handler**; 4 output columns NULL on 20,721 rows | every close, in principle | **MEDIUM.** A measurement capability silently absent — the optimizer question it was built for has never had data |
| **7** | **20 all-NULL columns on `trades`** | — | **LOW.** Mostly abandoned ingest fields; the MFE four are the informative ones |

## 🔴 SO — IS THE CODE CLEAN? NO.

**The prompts yielded five findings; the mechanisms yield seven, and three of them are mechanisms
that have executed exactly zero times in the life of the bot.** The brief asked to be told if the
code were clean, "after five findings in the prompts". It is not.

**The pattern across all three audits is now stable enough to state:**

1. **Nothing here fails loudly.** An empty table, a constant multiplier, a flag over an unreachable
   branch and a worker with no work all look exactly like a healthy system at rest.
2. 🔴 **A dead mechanism can take a live one with it.** The MFE tracker is not broken — it is
   *nested inside* something else that is. Nothing reports the absence.
3. 🔴 **Naming the class does not confer immunity.** §4's instance is mine, from today, committed
   three hours after I wrote the report defining it.

⚠️ **Scope, so it is not over-read:** this covers refusing/halting/closing mechanisms, `config.py`
booleans, table writers/readers and the last two weeks of commits. **Not audited:** the cascade's
internal tier logic, geometry arithmetic, `order_adapter`'s live-order semantics, and the optimizer.
Findings 1 and 3 in particular were reached from **journal evidence with a retained history starting
2026-08-02** — the conclusions rest on the empty tables, which span the whole book, not on the log
window.

---

## LIVE STATE

| | |
|---|---|
| HEAD / `git status` | **`de1d0f2`** / **clean** |
| open positions | **0** |
| service | `titan.service` active since **19:38:30 UTC** |
| ⏳ consultations since that restart | **0** — the stored-prompt confirmation of the 18:55 wall change and of today's three prompt fixes is **still pending**, now for the third report running. Last consultation of any kind: **16:40:10 UTC** |

*Read-only throughout. Nothing proposed, no diff, `titan-bot` unmodified at `de1d0f2`, 0 open
positions for the entire pass. Mercury-SOL never opened.*
