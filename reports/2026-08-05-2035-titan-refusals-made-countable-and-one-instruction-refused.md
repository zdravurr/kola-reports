# TITAN — FOUR INVISIBLE REFUSALS MADE COUNTABLE. AND ONE INSTRUCTION REFUSED, BECAUSE THE LOOP I CALLED IDLE CARRIES BOTH OBSERVATORIES.

**2026-08-05 20:35 UTC · 🔴 APPLIED FROM FLAT · HEAD `de1d0f2` → `ece910d` · restarted 20:31:57 UTC**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
**0 open positions and 0 `exit_pending`** at application, re-checked immediately before the restart.
**Mercury-SOL never opened.**

Parent: `2026-08-05-1955-titan-audit-the-mechanisms-for-the-same-defect-class.md`.

**Three fixes applied, one instruction refused on evidence, one item recorded.**
`main.py` +83 · `config.py` +26 · `claude_advisor.py` +11 · `skip_attribution.py` +29.

---

## 🔴 READ THIS FIRST — I DID NOT STOP THE BREAKEVEN LOOP, AND I THINK STOPPING IT WOULD HAVE BEEN DAMAGING

The instruction was *"STOP THE LOOP"*. The brief also required tracing what still uses the module
before touching anything. **That trace is why the loop is still running.**

`breakeven_worker._poll_once` is not idle. It is the **carrier for both observatories**, and the
placement is deliberate — the code says so in its own comment:

```python
    # Both observatories ride this loop (observational; never block
    # breakeven/trail) but sample on their OWN slower cadence …
    # Runs before the no-jobs early-return so it ticks even with zero live
    # breakeven jobs (the paper-mode norm).
        observatory_tick(exchange, shared_prices=shared_prices)      # post_exit_observatory
        skip_attribution_tick(exchange, shared_prices=shared_prices) # skip_attribution
```

`breakeven_worker.py:42-43` are the **only** imports of either tick in the codebase. Measured before
touching anything: **702 drift rows written in ten minutes**, `skip_drift_samples` at 45,355 rows and
current to the second.

🔴 **Stopping that loop would have killed the drift sampling for the whole bot — including the rows
fix 1 was created to produce, in the same commit.** The two instructions would have cancelled.

**And there was nothing to disarm anyway.** The breakeven *management* is already disabled by an
explicit flag rather than by circumstance:

```python
    # ONE mechanism manages a position, decided BY FLAG and not by circumstance.
    #   … this guard is deliberately belt-and-braces with the fact that
    #   breakeven_jobs can no longer GAIN rows …
        if virtual_trader.engine_owns_position():
            return 0
```

🔴 **MY 19:55 AUDIT WAS WRONG ON THIS POINT AND I AM CORRECTING IT.** I reported *"a 5-second poll
loop over an empty queue"* as a finding. The queue is empty **by design**, the double-management the
brief feared is already prevented **by flag**, and the loop earns its existence carrying the
observatories. The empty table was real; the conclusion I drew from it was not.

**What WAS wrong is the comment**, and that is fixed in place with the call left standing:

> *"Trailing stop is NOT placed at entry anymore (Stage 3). ~~The breakeven worker arms it — and moves
> the SL to breakeven — once price reaches +1R.~~"* → now records that `virtual_trader` performs the
> arming, that `_poll_once` refuses to manage once `engine_owns_position()` is true, and that this
> enqueue sits on the legacy path — **"What was wrong here was the sentence, not the line."**

---

## 1. 🔴 THE FOUR INVISIBLE REFUSALS NOW WRITE ATTRIBUTION ROWS

| status | all time | 30 d | what was lost |
|---|---|---|---|
| 🔴 **`risk_halt`** | **137** | **75** | the **third-most-active refusing mechanism in the bot**, invisible to every study in this book |
| `virt_cap_blocked` | 118 | 30 | same |
| `claude_unavailable` | 26 | 1 | entry-side fallback refusals |
| `failed` | 3 | 2 | approved entries that errored at order time |

### (a) + (b) BOTH HALVES DONE — AND THE SECOND HALF IS THE ONE THAT GETS MISSED

`TRACKED_STATUSES` is only a **scope filter**. The 2026-08-04 lesson is that the hook must also be
**called**. **Ten call sites added**, each immediately after the refusal's own
`update_signal_execution`:

| status | sites patched |
|---|---|
| `risk_halt` | 3 |
| `failed` | 3 |
| `claude_unavailable` | 2 (entry only — see below) |
| `virt_cap_blocked` | 2 |

🔴 **AND THE LIVE SITE WAS IDENTIFIED, NOT ASSUMED.** Sites differ in which columns they write, so
the writer is identifiable from the data: every recent `risk_halt` row carries
`matrix_breakdown_json` and `weight_used`, which only the `_handle_state_machine` site sets. **The
live refusals come from `_handle_state_machine`, and that site is patched** — the point mattering
because this bot already has one refusal path (`_execute_entry`) that the live flow bypasses.

### 🔴 SCOPE DELIBERATELY NARROWER THAN THE STATUS NAME

`claude_unavailable` is **also** written on the close path (`_handle_5m_close_via_ai`, *"Claude
UNAVAILABLE — close NOT executed"*). **That is not a refused entry — it is a position that stayed
open.** Anchoring entry-drift to it would be a category error. **The close site does not call the
hook**, verified in the diff.

### (c) WHICH BRAKE FIRED — ALREADY IN THE DATA, NOW CARRIED THROUGH

`risk_reason` is passed as `ai_reason`, and it already names the cause, so the cohort is cuttable:

| observed reason prefix | rows |
|---|---|
| `position-cap halt: 1 LONG already open (cap=1)` | 36 |
| `position-cap halt: 1 SHORT already open (cap=1)` | 34 |
| `DXY halt: DXY strong uptrend (…) — LONG blocked` | 56 across 5 values |
| `macro halt: CPI 5m ago (blackout ±30m)` | 2 |

**"risk_halt" alone could not be cut by cause. It can now.**

### 🔴 PROVEN BY EXECUTION, NOT BY READING

On an **isolated copy** of the DB with **every module's `DB_PATH` patched** — the 2026-08-04
isolation lesson, which is that patching one module's path is not enough:

| status | row written | anchor | wall / distance | drift slots | reason stored |
|---|---|---|---|---|---|
| `risk_halt` | ✅ | 64800.0 | 64900.0 / 0.154 % | **5** (15m·1h·4h·12h·24h) | `DXY halt: DXY strong uptrend (99.32) — LONG blocked` |
| `virt_cap_blocked` | ✅ | 64800.0 | 64900.0 / 0.154 % | **5** | — |
| `claude_unavailable` | ✅ | 64800.0 | 64900.0 / 0.154 % | **5** | `claude timeout` |
| `failed` | ✅ | 64800.0 | 64900.0 / 0.154 % | **5** | `order error: test` |

`skip_attribution` rows 9,071 → 9,075. **All four pass the filter and produce a complete, tracked
anchor.** ⏳ **Live confirmation waits on the next real refusal** — none has occurred since the
20:31:57 restart; `risk_halt` runs ~2.5/day.

### (d) OBSERVATION ONLY — CONFIRMED

Every hook is placed **after** the refusal's own write and **before** the `return`, is wrapped in the
existing best-effort helper, and feeds a write-only ledger. **No gate, no verdict, no stored decision
changes.** The comment at each site says so.

### (e) 🔴 WHEN THE FIRST SPLIT BECOMES READABLE — IN ROWS, NOT DAYS

**Do not read this in calendar time.** From this book's own hard-won lesson, **the unit of
independence is the DAY, not the signal** — 2–3 refusals a day is ~1 day of information per day.

| what | rows needed | why |
|---|---|---|
| first drift row completes | **1 row, +24 h** | all five slots close at 24 h |
| a crude direction on `risk_halt` | **~30 rows** | ≈ 30 independent days |
| a split by brake (`position-cap` vs `DXY` vs `macro`) | 🔴 **~30 rows PER ARM ≈ 90+** | the three arms are ~50/40/1 % of the population, so `macro` will not be readable at all for a long time |
| §2.54's control (day+direction+hour) | **more still** | that control needed a same-hour admitted comparator, available on only 16 % of `htf_blocked` |

**Honest statement: `risk_halt` at 75/30 d gives ~30 usable rows in about a month, and the by-brake
split the fix was built for needs roughly a quarter.** The fix is worth making now because the rows
cannot start accumulating until it exists — not because an answer is near.

---

## 2. THE EXIT PROMPT'S PERCENTILE NOTE — PARITY, AND THE REVERSE CHECK FOUND SOMETHING

**Both copies now carry both anchors:**

```
ENTRY  …Judge by the percentile printed with each wall:
       ~50th percentile is ORDINARY and not significant; 90th+ is genuinely thick.

EXIT   …Judge by the percentile: ~50th percentile is ORDINARY
       and not significant; 90th+ is genuinely thick.
```

*(The one remaining wording difference — "printed with each wall" — is accurate, not divergence: the
exit block renders one supporting and one opposing percentile, not per-wall.)*

### 🔴 THE OTHER DIRECTION, AS ASKED — AND IT IS NOT SYMMETRIC

**The EXIT prompt has something the ENTRY prompt lacks.** When percentiles cannot be computed, the
exit block says so **in words** and explicitly tells the model not to misread the raw figures:

> *"Order-book PERCENTILE scale: NOT AVAILABLE for this consultation. The figures above are RAW
> multiples from a book that is not the baseline's instrument, so they cannot be ranked. Do NOT infer
> 'extreme' or 'ordinary'…"*

**The ENTRY block in the same situation prints bare multiples and says nothing at all** — when
`baseline_n` is absent, the whole scale block including the NOTE is omitted.

⚠️ **RECORDED, NOT FIXED.** Adding that warning to the entry prompt is a **content change**, not the
wording-parity fix that was authorised — and it deserves its own decision, because **the entry
advisor is the one carrying a HARD RULE about walls**, so a silent unrankable book matters more
there, not less. **The class is confirmed to run in both directions.**

---

## 3b. `context_weight` — HONEST AT THE CALL SITE, SIZING UNCHANGED

It returns `(1.0, False, 0.0)` on every call and can return nothing else: it reads
`liquidity_sweep_state`, written only by `record_sweep()`, which returns early unless the signal type
is exactly `EQH`/`EQL` — and **no signal in 20,721 rows has ever carried one**. Confirmed from the
other side: `context_weight_score` is **0.0 on 3,009 rows and NULL on 17,712**, no other value ever.

🔴 **The call is LEFT IN THE PATH and sizing is byte-identical.** It is the identity today and must
stay the identity; removing it would change sizing code for no behavioural gain and bypassing it
would hide the fact rather than state it. **What was wrong was that nothing said it.**

---

## 4. RECORDED, NOT REVIVED

**`EQH_EQL_SMART_TP_ENABLED` → `False`.** It read armed over a handler that has never executed. The
flag flip changes **no behaviour** — the handler was already unreachable — it stops the flag
asserting a live mechanism. **Revival refused, and the reason is in `config.py` so it is not
re-proposed: §2.6 measured this smart-TP at −971 simulated. Making the signal type arrive would not
make the rule good; it would make a measured-negative rule live. Arrival is not approval.**

**The MFE tracker** nested inside that dead handler is recorded as a **lost measurement, not a losing
rule** — recoverable, but it must be lifted out of the dead handler first, and **reviving a
measurement and reviving a strategy are different acts.** Not decided here.

**20 all-NULL columns on `trades`** — recorded, no action.

---

## VERIFICATION LEDGER

| check | result |
|---|---|
| `ast.parse` + `py_compile`, all four files | ✅ |
| four statuses write full attribution rows | ✅ **proven by execution on an isolated DB copy** |
| the close-path `claude_unavailable` site does **not** call the hook | ✅ verified in diff |
| live refusal site (`_handle_state_machine`) is patched | ✅ identified from column signature, not assumed |
| exit NOTE matches entry NOTE | ✅ both anchors present |
| 🔴 `_ENTRY_SYSTEM` md5 | **`d7b8f3ed…` — UNCHANGED** |
| `config.py` non-comment changes | **exactly one line** (`EQH_EQL_SMART_TP_ENABLED`) |
| sizing / gate / geometry identifiers added | **none** outside comments |
| breakeven loop still starts | ✅ **intentionally** — `breakeven_worker started (interval=5s)` at 20:32:09 |
| nothing importing `breakeven_worker` broke | ✅ `order_adapter` (`_place_stop_with_retry`, `move_stop_with_race_guard`), `main`, `virtual_trader`, both observatory ticks — all intact |
| restart | `active`, **20:31:57 UTC**, 🔴 `LIVE ORDERS — REAL MONEY` unchanged |
| boot reconciliation | ✅ *"exchange and DB agree: 0 exchange position(s), 0 open row(s)"* |
| 🔴 **observatory tick after restart** | ✅ **CONFIRMED LIVE.** No slot was due until 20:35:04; at **20:35:16** the tick fired and wrote **4 drift samples**, next slot due 20:40:07. **The loop I declined to stop is sampling, and the drift machinery survived the change intact** |

**Untouched:** EMA envelope gate · HTF cascade · FLAT floor · Variant-B · score bars · geometry ·
risk-gate thresholds · both prompts beyond the exit NOTE · every schema.
**Snapshots:** `/root/backups/mech-fix-20260805-2010/` (all 38 `.py` files). **Revert:** `git revert ece910d`.

---

## ⏳ THE ITEM OPEN SINCE 19:15 — FOURTH REPORT, STILL OPEN

**No stored prompt with per-wall percentiles has landed.** Last consultation of any kind:
**16:40:10 UTC** — now ~4 hours ago, across three restarts. Zero consultations since 19:08, since
19:38 and since 20:31. The 18:55 wall change and the 19:38 prompt fixes remain confirmed on live data
through the real code path but **unconfirmed on a stored row**, and today's restart resets that clock
again. **The bot is simply not being given signals; that is the reason, and it is not evidence that
anything is broken — but it is not confirmation either, and I am not going to describe it as one.**

---

## LIVE STATE

| | |
|---|---|
| HEAD / `git status` | **`ece910d`** / **clean** |
| open positions | **0** |
| service | active since **20:31:57 UTC** |
| `AI_ADVISOR_HIDE_1H` / `EQH_EQL_SMART_TP_ENABLED` / `EXIT_ADVISOR_DRYRUN` | `False` / `False` / `False` |
| tracked refusal statuses | **8** (was 4) |
