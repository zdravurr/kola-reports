# Mercury-SOL — the relaxations are OFF, the registry clear stops lying, and the book gate's ruler was cut on a population the gate never judges

**2026-08-14 18:40 UTC · Mercury-SOL (`/mnt/volume_nyc1_1780480650620/mercury-sol`) · 🔴 LIVE REAL MONEY · APPLIED and RESTARTED from FLAT at 18:28:16 UTC · worker pid 2162408**

Parent: [17:50 — the duplicate is a ROW, not a CALL](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-14-1750-sol-the-duplicate-is-a-row-not-a-call-and-the-range-still-does-not-separate.md) (§1e, §4a, §4b are the three items below).

Titan (`/root/titan-bot`): **HEAD `897850b`, working tree clean, MainPID 2538048 unchanged, NRestarts 0, uptime unbroken since 2026-08-06 01:53:19. Zero `.py` files under its directory modified.** Proven by directory-scoped harness, §5.

---

## ⚡ WHAT LANDED, AND THE ONE THING THAT TURNED OUT DIFFERENT FROM THE BRIEF

1. **Both aligned relaxations are OFF** behind one named flag, `ADVISOR_WALL_ALIGNED_RELAXATIONS = False`, with the 41-flip / −4.403R ledger written into the comment. **Nothing deleted.** Proven functionally: the same production row that fired the relaxation at 09:45 this morning now makes **1 model call instead of 2**, and flipping the single flag back in-process reproduces the old journal line byte-for-byte.
2. **The registry clear stops lying.** The failure now propagates and the "🔴 FAILED to clear" Telegram alert is reachable for the first time since it was written.
3. **🔴 BUT THE CAUSE WAS NOT CONTENTION — IT WAS A SELF-DEADLOCK, AND A RETRY ALONE WOULD NEVER HAVE FIXED IT.** `close_position` called the clear from *inside its own open write transaction*, so a second connection waited on a lock the first could not release until the second returned. **Reproduced on a copy of the production DB: nested → `database is locked` after 5.02 s, every time; un-nested → OK in 0.01 s.** The clear now runs *after* the transaction commits. The bounded retry is in as well — and it earns its place on genuine contention (test T3) — but it is the second half of the fix, not the first.
4. **The stale row is gone**, and the belt is proven: run verbatim against the live DB, `_ledger_close_after` returns vpos 35 → the reconciler would have taken the "Stale registry row dropped" branch. **No phantom was ever possible on the next boot.**
5. **🔴 AND THE BOOK GATE'S DISTRIBUTION DID NOT MOVE.** That was the assumed cause of the breach and the measurement refutes it. Re-cutting p2 on the current tape's *scored-signal* books — the literal instruction — gives LONG **0.4461** (a *tighter* floor) / SHORT **0.4110**, and replays to **exactly the same 6.82 % / 23.17 %**. It changes nothing. The ruler was cut on **all 3,449 scored signals**; the gate sits at the **end** of the funnel and judges only the survivors. Same rule, right population → **LONG 0.4238 / SHORT 0.3489**, and the rate lands on its design: **2.01 % / 2.14 %, ratio 1.07×**.
6. **🔴 The gate still admits every chop short.** Replayed on the new floors, vpos 27, 28, 34 and 35 — ΣR −2.157 between them — all read "book clear". The only entry in the whole 29-position book it refuses is vpos 32. **That is a finding about clause B, not about the threshold**, exactly as the brief anticipated, and it is written into `config.py` so it cannot be mistaken for a win.

---

## 0. APPLY RECORD

| | |
|---|---|
| backups (md5-verified against the originals **before** any edit) | `config.py.bak_threeitems_20260814_1830` `409f5dfe…` · `claude_advisor.py.bak_threeitems_20260814_1830` `50d6a39f…` · `main.py.bak_threeitems_20260814_1830` `50916b9b…` · `virtual_trader.py.bak_threeitems_20260814_1830` `6180d6e3…` · `trades.db.bak_threeitems_20260814_1830` (55,431,168 bytes) |
| pre-edit md5 cross-check | `main.py` `50916b9b…` and `virtual_trader.py` `6180d6e3…` are **byte-identical to the values published in the 2026-08-10 20:00 apply record** — no drift since |
| files changed | **exactly four**, all inside `mercury-sol`: `config.py` (+129/−3), `claude_advisor.py` (+23/−4), `main.py` (+103/−13), `virtual_trader.py` (+62/−21) |
| compile | `py_compile` clean on all four **plus `book_gate.py`**, compiled to a **TEMP** directory — no `.pyc` written into production by me |
| DB write | **one**: the stale `active_positions` row deleted (§3c). `trades` untouched — max id 18392 before, 18392 after |
| restart | `systemctl restart mercury-sol.service` **18:28:07**, active **18:28:16**, from **FLAT on all three books** (registry 0, `virtual_positions` 0, **venue 0 — read live via the bot's own Bybit key over Tor**) |
| boot | clean. `[AP] No active positions in DB — clean boot` · `[BOOT-ASSERT] venue FLAT` · `unregister=yes` · `OBSERVATION_MODE=False` · 0 tracebacks |
| harness | **43 assertions, 43 PASS, 0 FAIL** (§5) |

---

# 1. THE ALIGNED RELAXATIONS — OFF

## 1a. One named flag, default OFF, with the ledger in the comment

`config.py`:

```python
ADVISOR_WALL_ALIGNED_RELAXATIONS = False   # 🔴 OFF 2026-08-14.
```

The comment above it carries the ledger verbatim — 41 distinct model flips (17 LONG-arm, 24 SHORT-arm; 42 stamped rows, `#16444` being a reuse of a flip), 12 became positions at **ΣR −4.403** with 4 winners of 12, the four most recent (vpos 26 −1.085R, 27 −0.660R, 28 −0.153R, 32 −0.180R) **0 for 4 at −2.078R**, a cost of **+19.8 % of all model calls all-time** and **+5.0 % over the last 7 days**, and the ×20 ceiling having suppressed an override **exactly once, ever**.

`claude_advisor.py` — the flag is **ANDed into all four predicates**, live and shadow, both arms:

```python
_live_aligned   = ADVISOR_WALL_ALIGNED_V2 and ADVISOR_WALL_ALIGNED_RELAXATIONS
_shadow_aligned = (ADVISOR_WALL_ALIGNED_V2_DRYRUN and not ADVISOR_WALL_ALIGNED_V2
                   and ADVISOR_WALL_ALIGNED_RELAXATIONS)
_live_aligned_s   = ADVISOR_WALL_ALIGNED_SHORT_V2 and ADVISOR_WALL_ALIGNED_RELAXATIONS
_shadow_aligned_s = (ADVISOR_WALL_ALIGNED_SHORT_V2_DRYRUN and not ADVISOR_WALL_ALIGNED_SHORT_V2
                     and ADVISOR_WALL_ALIGNED_RELAXATIONS)
```

🔴 **Why the shadow predicate had to be included.** Setting only the two masters to `False` would have routed both arms into **DRYRUN** — both `*_DRYRUN` flags are `True` — which still makes the extra model call on every aligned V1 skip and buys a log line. The saving would have been zero. That is why this is one kill flag rather than two `False`s.

The import guard **fails toward "no override"**, matching the ×20-ceiling guard rather than the `AI_ADVISOR_HIDE_1H` guard: a missing or renamed config can never silently re-arm a mechanism whose realised record is 12 positions at −4.403R.

## 1b. 🔴 NOT DELETED — and the proof that it is re-armable

The two aligned system prompts are still constructed at import, both still differ from `_ENTRY_SYSTEM`, and both blocks are intact. **The two historical master flags and both DRYRUN flags are left at their original `True` values on purpose**, so the record of what was live, and when, survives in the file rather than only in a git history nobody reads. Setting the one new flag to `True` restores the exact prior behaviour — demonstrated, not asserted, in §1e.

## 1c. What the bot does instead — and nothing else re-creates the override

**The advisor's own V1 verdict stands.** A V1 `skip` on an aligned-LONG or an aligned-bear-low-ADX SHORT setup is now simply a skip, exactly as it already was for every entry that never entered these blocks.

**Traced, not assumed.** Three sites in the whole module can send a non-V1 system prompt, and only two can overturn a verdict:

```
claude_advisor.py:929   _call(_ENTRY_SYSTEM_V2)          gated by ADVISOR_WALL_RULE_V2_DRYRUN and not ADVISOR_WALL_RULE_V2
                                                          -> BOTH are False in config (lines 800-801) -> dead,
                                                             and log-only in any case: it never mutates `result`
claude_advisor.py:1033  _call(_ENTRY_SYSTEM_V2_ALIGNED)        -> now gated by the kill flag
claude_advisor.py:1078  _call(_ENTRY_SYSTEM_V2_ALIGNED_SHORT)  -> now gated by the kill flag

  result['decide'] = 'execute'   appears at EXACTLY 2 lines: 1041 and 1086
                                 both INSIDE the two gated blocks. There is no third.
  (line 921's `result['decide'] = decide` only normalises the model's own verdict.)
```

And nothing outside `config.py` / `claude_advisor.py` reads or writes any of these flags — grep across every `.py` in the directory returns only those two files.

## 1d. 🔴 PRE-REGISTRATION — written before the data arrives

| quantity | expected | how it will be checked |
|---|---|---|
| model calls/day | **−4.7 %** (last 7 days: 222 base + 11 relaxation = 233 → 222) | count rows with `ai_decision IN ('execute','skip')` and reconstruct the relaxation-eligible set from `side` / `trend_1h` / `srv_adx_1h`; that reconstruction was validated **4 of 4 against the journal** this morning (09:45 adx 13.4 · 11:20 15.5 · 11:40 15.5 · 12:35 16.5) |
| `[WALL-ALIGNED-*]` journal lines | **exactly 0**, forever, until the flag moves | `journalctl -u mercury-sol \| grep WALL-ALIGNED` |
| rows stamped with an aligned `ai_system_prompt` | **exactly 0** new; the historical 42 are untouched | md5 of `ai_system_prompt` vs the two aligned constants |
| entry rate | **unchanged in expectation.** The relaxations built 12 positions in 43 days ≈ 0.28/month; at 1.03 entries/day this removes well under one entry a month | `virtual_positions` count/day |
| the base verdict now governs | a V1 `skip` on an eligible setup is final | `ai_decision='skip'` with the gate predicate true and no aligned stamp |

🔴 **WHAT WOULD SHOW THIS IS COSTING OBVIOUS WINNERS — stated now, so it cannot be invented later:**

- **The primary instrument already exists.** Every eligible skip is registered in `skip_attribution` with forward drift sampled into `skip_drift_samples`. The reconstructed eligible set is exact, so the cohort is computable at any time without new code.
- **The trigger:** over **≥5 distinct eligible episodes** (episodes, not rows — the 2026-08-07 loss-streak pass established that ten rows from one four-hour window are `n_effective = 1`), the eligible-skip cohort's **+4h and +12h drift signed toward the refused side** materially exceeds the same-day, same-side, other-cause baseline **and** the 60-day per-cause baseline, the way the loss-streak refusals did on 2026-08-07 (+0.842 % at 4h against an unconditional +0.035 %).
- **The reversal condition, in the original's own idiom:** the flip cohort standing at 4 winners of 12 and **0 of 4 since the ceiling era** is the case for switching off. **One profitable realised flip would not be enough** — that is what R1 was in 2026-08-02 and it produced vpos 26 at −1.085R. Re-arming needs the drift evidence above, not a single lucky trade.
- 🔴 **And the honest asymmetry:** the outcomes of trades that are now never taken **do not exist and cannot be computed at any sample size**. The drift proxy is a proxy. That is stated here so nobody later mistakes "the drift looks good" for "we lost money by turning it off".

## 1e. 🔴 FUNCTIONAL PROOF — the real function, a real production book, the calls counted

Driven against row **#18316** — one of the four rows that actually fired the SHORT relaxation this morning, journal-confirmed — with its own stored OKX book and its own `srv_*`/`trend_*` snapshot, and `_call` stubbed so no network is touched:

```
driver row #18316   side=sell   trend_1h=bear   srv_adx_1h=13.41
  gate predicate: SHORT and trend_1h=='bear' and adx<25  ->  True  (ELIGIBLE)

AS SHIPPED (ADVISOR_WALL_ALIGNED_RELAXATIONS = False)
  relaxations OFF                        model calls = 1  ['V1']            decide='skip'  stamped=V1

COUNTERFACTUAL — the one flag flipped back to True, in this process only
  [MERCURY-SOL][WALL-ALIGNED-SHORT-V2][LIVE] HELD skip SHORT adx1h=13.4 v2_decide='skip'
  relaxations ON (pre-2026-08-14)        model calls = 2  ['V1','ALIGNED_SHORT']          stamped=V1

  ✅ the second call is GONE, and the flag ALONE restores it — the log line it
     reproduces is byte-identical to the real 09:45:20 journal line

SHADOW PATH — masters False, DRYRUN True, kill flag False
  model calls = 1  ['V1']                ✅ no shadow call either
```

**Since the restart: 0 `[WALL-ALIGNED-*]` lines.** Two signals have arrived, both `below_threshold`, both dying before the advisor — so this is **not** live proof, and it is not claimed as any. The functional proof above is the evidence; the live counter starts now.

---

# 2. THE REGISTRY CLEAR MUST NOT LIE

## 2a. The failure propagates — and it still cannot raise into the poller

Three changes, deliberately separate:

```
main.py   _remove_active_position(symbol, position_side, raise_on_failure=False)
            bounded retry; re-raises after exhaustion ONLY when asked
          _unregister_active_position(symbol, position_side, raise_on_failure=False)
            in-memory pop FIRST and unconditionally, then the table delete
          _unregister_active_position_strict(symbol, position_side)      <- NEW
            the one-line adapter that passes raise_on_failure=True
main.py:6208  unregister_fn=_unregister_active_position_strict            <- the ENGINE now uses it
```

🔴 **The default stays fail-soft ON PURPOSE, and this is the part worth reading.** main has two other call sites, both inside live close routes: `_execute_close_position` — which unregisters **before sending the closing order** — and the retired monitor's SL-detect branch. Making the raise global would let a *bookkeeping* failure **abort a real close**, which is strictly worse than a stale row. They keep the old behaviour. Only the engine path opts in, because only the engine path has an alert waiting.

**Confirmed it cannot raise into the poller:** the sole caller of the strict variant is inside `close_position`'s own `try/except Exception`, which prints, sends the Telegram alert, and falls through. Every path out of that block returns normally, the close is already committed by then, and the function's return value is unaffected. Test **T4** below exercises the fail-soft default and shows it returns `None` without raising.

## 2b. 🔴 THE RETRY — AND WHY IT WOULD NOT HAVE BEEN ENOUGH ON ITS OWN

The brief's premise was *"a lock during a close is contention, not corruption."* **Measured, it was neither. It was a self-deadlock.**

`close_position` called the clear from **inside its own open `with sqlite3.connect(...)` write transaction** — the `UPDATE` and the `INSERT` above it had already opened the transaction, and `with` does not commit until the block exits. `_remove_active_position` then opened a **second connection to the same file**, needed a RESERVED lock, and waited for one **held by the first connection in the same thread**, which could not commit until the second call returned.

**Reproduced on a copy of the production DB, 2026-08-14:**

```
A) nested DELETE while the OUTER connection has an OPEN write transaction:
       OperationalError: database is locked   after 5.02 s      <- deterministic
B) the same DELETE with NO outer transaction open:
       OK in 0.01 s
```

**So the retry is applied, but the placement is the fix.** The clear is now **latched inside the transaction** (preserving the `rowcount != 1` race guard — only the caller that WON the close can reach it) and **run after the block commits**. That ordering is also strictly safer than the old one: the ledger and the close row are committed *before* the registry row is touched, so a crash in between leaves a stale row against a correctly-closed position — recoverable, and exactly what the boot belt absorbs. The old order could have cleared the registry for a close that then failed to commit.

**The retry: 3 attempts, 2.0 s busy wait each, backoff 0.25 s then 0.75 s → ~7.0 s of lock-waiting worst case.** Why 3: the genuine contention on this box is four gunicorn `gthread` workers writing `trades` rows while a close is booked — a sub-second window. Three attempts cover a writer holding the DB for several seconds; beyond that the correct action is to **alert** rather than stall the poller further. The ledger and close row are already committed when this runs, so the cost is bookkeeping latency on one tick — never a position, an order or a stop.

**All four lab tests green, against the real failure shape:**

| test | result |
|---|---|
| **T1** old placement (inside the open txn), strict | 3 attempts, all `database is locked`, **RAISED after 7.19 s → the caller's alert fires**. Row correctly still stale — it genuinely failed |
| **T2** new placement (after commit), strict | **cleared, rowcount=1, in 0.02 s** |
| **T3** genuine contention — a holder that releases at 2.4 s | **succeeded on attempt 2 at 2.34 s** — the retry earns its place |
| **T4** fail-soft default (main's own close routes) | returned `None` **without raising** — a live close can never be aborted by this |

T1 is the important one: it proves the propagation works **and** that a retry alone would have changed nothing.

## 2c. The stale row — what it was, and it is gone

```
symbol           = 'SOL/USDT:USDT'
position_side    = 'SHORT'
entry_row_id     = None
entry_time       = '2026-08-14T14:20:27.427112+00:00'      <- vpos 35's entry
entry_price      = 75.16
sl_price         = None      trail_active = 0      breakeven_locked = 0
updated_at       = '2026-08-14 14:20:27'                   <- never touched since the entry
```

It was **vpos 35's registry row** — the SHORT that opened at 14:20 and was stopped out at **15:30:13** at 75.57 for −0.701R. The clear ran at 15:30:18, failed with `database is locked`, and the failure was swallowed; the row sat there for 3 hours. (vpos 34's row failed identically at 2026-08-13 17:12:31 and was overwritten by vpos 35's entry upsert, which is why only one row survived to be found.)

```
DELETE FROM active_positions WHERE symbol=? AND position_side=? AND entry_time=?
  rowcount = 1     active_positions 1 -> 0
  open virtual_positions: 0     trades max id: 18392 -> 18392 (nothing invented)
```

## 2d. 🔴 THE BELT WOULD HAVE HELD — run verbatim against the live DB before the row was cleared

```
_ledger_close_after('SOL/USDT:USDT', 'SHORT', '2026-08-14T14:20:27.427112+00:00')
  -> vpos 35, closed_at 2026-08-14T15:30:13.790076+00:00, reason=sl, net_pnl=-0.7289489999999956

=> the reconciler takes the "🧹 Stale registry row dropped" branch and RETURNS.
=> NO phantom close row would have been written on the next boot.
```

Cross-checked: the real close row for vpos 35 already exists (`#18364`, `VIRT-CLOSE-35`, `sl_triggered_short`, pnl −0.72895), so a reconcile close would have been a duplicate — and the belt refuses to write one when the ledger already names a close newer than the registry row's `entry_time`.

**So which defence actually held: the belt.** The primary clear failed silently twice; the belt was never exercised because I cleared the row by hand first, but it is proven to have been armed and correct for the exact input it would have seen. **On this boot the reconciler was not reached at all** — `[AP] No active positions in DB — clean boot`, zero `RECONCILED` / `Stale registry row dropped` lines, zero close rows written.

---

# 3. THE BOOK GATE — RE-CUT, NOT LOOSENED

## 3a. 🔴 THE LITERAL RE-CUT WAS EXECUTED FIRST, AND IT FIXES NOTHING

The instruction was to re-cut p2 on the current tape. Done — same recipe, same `orderbook_json` population the original was cut from, last 30 days:

```
                              LONG            SHORT
  original (config today)     0.4323          0.4129
  last 30 days, p2            0.4461          0.4110      <- LONG goes UP
  last 14 days, p2            0.4492          0.3968
  all time, p2                0.4329          0.4145
```

**Method validated first:** re-running the ORIGINAL recipe over the ORIGINAL window reproduces the shipped numbers to within 0.0003 — LONG **0.4325** on n=1543 vs the shipped 0.4323, SHORT **0.4132** on n=1906 vs 0.4129 (the design doc says 1,545/1,909). Same ruler, same hands.

**Replayed, the literal re-cut changes nothing:**

| floors | LONG refusal | SHORT refusal | ratio |
|---|---|---|---|
| CURRENT 0.4323 / 0.4129 | 6/88 = **6.82 %** | 19/82 = **23.17 %** | 3.40× |
| **LITERAL 30d 0.4461 / 0.4110** | 6/88 = **6.82 %** | 19/82 = **23.17 %** | **3.40×** |

🔴 **The distribution did not move.** SHORT median lean is **0.4940** by design and **0.4861** as evaluated — a shift of **−0.008**. The premise the instruction rested on is refuted by the measurement, so applying the literal floors would have been knowingly shipping a change that fixes nothing and tightens LONG.

## 3b. WHAT ACTUALLY BROKE: the ruler was cut on a population the gate never judges

The original p2 came from **3,449 SCORED SIGNALS carrying a book**. The gate runs at the **END** of the funnel — after the cascade, the score bar and the risk gate — and sees only the survivors. Same quantity, two populations:

| lean, SHORT | design population (all scored signals) | population the gate EVALUATES |
|---|---|---|
| n | 1,906 | 82 |
| median | 0.4940 | 0.4861 |
| **p2** | **0.4132** | **0.3314** |

**The body is the same. The tail is fatter** — signals that survive the funnel are drawn disproportionately from books that lean hard against the proposed side. A p2 cut on the wrong population is not a threshold error; it is a category error, and it is the entire mechanical cause of the 23 %.

**The re-cut, same rule, right population.** p2 of each side's own lean distribution over **every row that reached the gate, 2026-08-03 → 2026-08-14** (n = **249 LONG / 374 SHORT**). That window is not a choice: `advisor_book_json` — which is what identifies an ADMITTED row — only exists from 2026-08-03, so the correct population is not reconstructible further back. Said plainly rather than padded out to a nominal 30 days.

```python
BOOK_GATE_LEAN_FLOOR = {
    'LONG':  0.4238,      # was 0.4323
    'SHORT': 0.3489,      # was 0.4129
}
```

🔴 **The SHORT floor goes DOWN, and that is not loosening to taste.** The percentile rule is untouched — it is still **2**. What changed is the sample the 2nd percentile is taken over. The LONG floor moves down too (0.4323 → 0.4238) and lands at **2.01 %**, which is the *designed* rate, not a smaller one. Clause A is untouched (`BOOK_GATE_WALL_PCTL` 90.0, `BOOK_GATE_WALL_DIST_PCT` 0.20), `BOOK_GATE_MIN_SUPPORTING` is untouched, and the gate stays **ARMED** (`ENABLED=True`, `DRYRUN=False`).

## 3c. The new floors, the recomputed rate, and the new side ratio

**Clause B, on the population the gate judges (n = 249 LONG / 374 SHORT, 2026-08-03 → 08-14):**

| floors | LONG | SHORT | **ratio** |
|---|---|---|---|
| CURRENT 0.4323 / 0.4129 | 8/249 = 3.21 % | 32/374 = 8.56 % | 2.66× |
| LITERAL 0.4461 / 0.4110 | 10/249 = 4.02 % | 30/374 = 8.02 % | 2.00× |
| **NEW 0.4238 / 0.3489** | **5/249 = 2.01 %** | **8/374 = 2.14 %** | **1.07×** |

**Full gate (A or B), replayed on the 170 rows the gate actually evaluated since arming** — this replay reproduces the 25 observed `book_blocked` rows exactly under the current floors, which is what makes it trustworthy:

| floors | LONG | SHORT | ratio | overall |
|---|---|---|---|---|
| CURRENT | 6/88 = 6.82 % (A2 B4) | 19/82 = 23.17 % (A2 B17) | 3.40× | 14.71 % |
| LITERAL | 6/88 = 6.82 % | 19/82 = 23.17 % | 3.40× | 14.71 % |
| **NEW** | **6/88 = 6.82 %** (A2 B4) | **9/82 = 10.98 %** (A2 B7) | **1.61×** | **8.82 %** |

**Both numbers are reported because they answer different questions.** The 30-day gate population (n=623) is the *calibration*: 2.01 % / 2.14 %, ratio 1.07×. The 4-day armed window (n=170) is *what actually happened*: still 10.98 % on SHORT, dominated by 2026-08-12 alone (16 refusals in 34 evaluations). **I am not cutting the floor further to make that four-day number look like 2 %** — that would be tuning to an outcome, which is the thing the pre-registration exists to forbid.

## 3d. 🔴 DID IT REFUSE ANY OF THE FIVE MEASURED RANGE ENTRIES? NO. NOT ONE.

Replayed on the **new** floors, against each entry's own stored OKX book:

| vpos | side | R | gate verdict |
|---|---|---|---|
| 17 | SHORT | +0.004 | *no stored OKX book — predates the 2026-08-03 capture* |
| **27** | SHORT | **−0.660** | **ADMIT — "book clear"** |
| **28** | SHORT | **−0.153** | **ADMIT — "book clear"** |
| **34** | SHORT | **−0.643** | **ADMIT — "book clear"** |
| **35** | SHORT | **−0.701** | **ADMIT — "book clear"** |

**ΣR of the four it admits: −2.157.** Across the whole 29-position book, the only entry the gate refuses at all is **vpos 32** (clause B, lean 0.343 — consistent with the arming record, which named exactly that row).

🔴 **So it was refusing 23 % of shorts while waving through the four worst shorts in the book.** That is a statement about **what clause B measures** — resting depth, which has been tested against outcomes on this instrument three times (filter 21 REFUSED, filter 22 REFUSED, advisor-vs-book independence at Fisher p = 1.0000, n = 396) and separates nothing — and **no threshold can fix it.** The re-cut makes the gate fire at the rate a discipline rule should fire at. **It does not and cannot make it pick better trades**, and that sentence is now in `config.py` above the floors so the next session cannot mistake the improved rate for an improved gate.

## 3e. 🔴 RE-REGISTERED — same wording, so the next breach is readable

| quantity | expected | source |
|---|---|---|
| refusal rate LONG | **2.01 %** | replay over 249 LONG books that reached the gate, 2026-08-03 → 2026-08-14 |
| refusal rate SHORT | **2.14 %** | same, 374 SHORT books |
| side ratio | **1.07×** | the number that says "rule", not "side ban" |
| clause A | ~**1.2 %** | unchanged — this re-cut touches only clause B |
| review point | **200 further gate evaluations, or 2026-09-14, whichever comes first** | |

> 🔴 **IF THE REALISED RATE IS MATERIALLY DIFFERENT — ABOVE 5 % ON EITHER SIDE, OR A SIDE RATIO ABOVE 2× — THAT IS A FINDING ABOUT THE CALIBRATION AND GROUNDS TO REVISIT. IT IS NOT A REASON TO LOOSEN THE THRESHOLD QUIETLY.** The floors were cut from the gate's own lean distribution per side; a realised rate far off these numbers means that distribution has moved, and the correct response is to re-cut the ruler and say so, not to lower `BOOK_GATE_LEAN_FLOOR` until the refusals stop.

**And a SECOND wire, new, because the first one missed the real problem:** the four-day armed window still replays at **SHORT 10.98 %** under these floors. **If the SHORT rate is still above 5 % at the review point on ≥200 evaluations, the finding is about CLAUSE B ITSELF, not about the floor** — §3d is the reason, and no threshold move addresses it.

---

# 4. WHAT IS RUNNING NOW

```
mercury-sol   active · master 2162333 / worker 2162408 · since 2026-08-14 18:28:16 · NRestarts=0
              restart taken FROM FLAT: registry 0, virtual_positions 0, VENUE 0 (read live over Tor)
BOOT          [AP] No active positions in DB — clean boot
              [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
              [VIRTUAL] live adapter registered (…/funding=yes/unregister=yes)
              [BOOT] geometry SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) OBSERVATION_MODE=False
              [VPOS-RECONCILE] no open positions at boot — clean.       0 tracebacks
LOADED        ADVISOR_WALL_ALIGNED_RELAXATIONS = False   (both arms, live AND shadow)
              _unregister_active_position_strict wired as the engine's unregister_fn
              registry clear MOVED outside close_position's transaction
              BOOK_GATE_LEAN_FLOOR = {'LONG': 0.4238, 'SHORT': 0.3489}   gate still ARMED
BOOK          29 closed positions, ΣR −5.985. FLAT. active_positions EMPTY.
SINCE BOOT    2 signals, both below_threshold — neither reached the advisor or the gate.
              0 [WALL-ALIGNED-*] lines · 0 [BOOK-GATE] lines · 0 registry errors
              🔴 EIGHT MINUTES OF A QUIET TAPE IS NOT LIVE PROOF AND IS NOT CLAIMED AS ANY.
              The functional and lab proofs are the evidence; the live counters start now.
titan         HEAD 897850b · clean · MainPID 2538048 · uptime unbroken since 2026-08-06 01:53:19
```

---

# 5. THE ISOLATION HARNESS — SEARCHED BY DIRECTORY. 43 ASSERTIONS, 43 PASS, 0 FAIL.

**Why by directory and not by filename:** both bots have a `config.py`, a `main.py`, a `claude_advisor.py` and a `virtual_trader.py`. A check that greps for `claude_advisor.py` proves nothing about *which bot* it found. Every assertion below is rooted at an absolute directory.

```
1. TITAN — DIRECTORY-SCOPED, MUST BE UNTOUCHED
  [PASS] zero .py SOURCE files modified anywhere under /root/titan-bot — 0
  [PASS] every changed path under Titan is one of ITS OWN runtime artefacts
         (titan's own) /root/titan-bot/healthcheck_state.json   18:33:17 UTC
         (titan's own) /root/titan-bot/optimizer/tg_offset.txt  18:33:48 UTC
         (titan's own) /root/titan-bot/trades.db                18:34:10 UTC
  [PASS] Titan repo HEAD unchanged — 897850b     [PASS] working tree clean — 0 dirty paths
  [PASS] MainPID unchanged (never restarted) — 2538048
  [PASS] uptime unchanged — Thu 2026-08-06 01:53:19 UTC     [PASS] NRestarts still 0

2. MERCURY-SOL — EXACTLY THE FOUR INTENDED FILES
  [PASS] ['claude_advisor.py', 'config.py', 'main.py', 'virtual_trader.py']
  [PASS] a .bak exists for every changed file + the DB

3. THE DEPLOYMENT GAP — IS THE RUNNING PROCESS RUNNING THIS CODE?
  [PASS] worker booted AFTER the newest changed file — boot 18:28:16 > newest mtime 18:23:11
  [PASS] poller heartbeat present since the restart — open=0 mode=LIVE pid=2162408

4. ITEM 1 (9 assertions)   flag False · masters PRESERVED · all FOUR predicates ANDed ·
                           aligned prompts still EXIST (re-armable) · Op-X V2 off on both flags ·
                           exactly 2 sites can overturn a skip, lines 1041 and 1086
5. ITEM 2 (9 assertions)   raise_on_failure present · 3-attempt retry · strict wrapper ·
                           ENGINE uses STRICT · main's own routes still FAIL-SOFT ·
                           latch-in-txn -> run-after-txn -> CLOSE log, in that order ·
                           run block at 4-space indent (outside the `with`) · alert reachable
6. ITEM 3 (6 assertions)   floors 0.4238/0.3489 loaded · p2 rule still named in the file ·
                           gate ARMED · clause A untouched · WALL_AVOIDANCE still off
7. THE BOOK (6 assertions) active_positions EMPTY · no open vpos · vpos still ends at 35 ·
                           29 closed · zero close rows point at a non-existent vpos ·
                           NO close row written at this boot (only #18393 below_threshold) ·
                           no reconcile/phantom branch taken · LIVE mode still on

RESULT: ALL PASS  (43/43)
```

🔴 **Two harness assertions FAILED on the first run and both were harness bugs, corrected rather than removed.** (i) The scan window constant was ~80,000 s wrong, so it found zero changed files — fixed to 18:10 UTC. (ii) It asserted one `VIRT-CLOSE` row per position and found 36 rows for 29 positions; investigated rather than assumed, and **7 `exit_signal` closes legitimately carry two rows each** (vpos 7, 8, 9, 11, 19, 23, 28) — 29 + 7 = 36, with **zero orphans**. The assertion was replaced with the two that actually matter: no close row points at a non-existent vpos, and no close row was written at this boot. Recorded because a harness bent to pass is worse than no harness.

---

## APPENDIX — the exact diffs

```
config.py           +129 −3    the kill flag + its ledger; the re-cut floors + the re-registration
claude_advisor.py    +23 −4    one defensive import; four predicates ANDed with the kill flag
main.py             +103 −13   retry + raise_on_failure; the strict wrapper; adapter rewired
virtual_trader.py    +62 −21   the clear latched inside the txn and RUN after it commits

  config.py          @@ -312,10 +312,96 @@   @@ -757,6 +843,46 @@
  claude_advisor.py  @@ -70,6 +70,15 @@   @@ -1001,8 +1010,15 @@   @@ -1051,8 +1067,11 @@
  main.py            @@ -231,16 +231,71 @@  @@ -611,10 +666,41 @@   @@ -6205,7 +6291,11 @@
  virtual_trader.py  @@ -783,27 +783,32 @@  @@ -813,6 +818,42 @@
```

**Rollback is one command per file:** `cp <file>.bak_threeitems_20260814_1830 <file>` — all four backups md5-verified against the originals before any edit, and `trades.db.bak_threeitems_20260814_1830` predates the single row deletion.
