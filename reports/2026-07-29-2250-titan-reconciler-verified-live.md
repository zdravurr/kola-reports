# titan-reconciler-verified-live

_2026-07-29 22:50 UTC_

---

# TITAN — NOTHING WAS LOST, THE RECONCILER IS LIVE, AND IT HAD A LYING LABEL

**2026-07-29 22:50 UTC · HEAD `12b4df2` · 🔴 LIVE ORDERS · $30 × 5 = $150 notional · exchange FLAT**

**DECISION LINE: no action needed from you.** The dropped session lost nothing — it had already
built, committed, pushed **and deployed** the exchange→DB reconciler before it died. I verified
all ten Part-1 checks independently, re-proved the reconciler with my own harness (12/12), found
**one real defect inside the new code**, fixed it, and redeployed while the book was flat.

---

## 🔴 THE ONE THING THAT DIFFERS FROM YOUR BRIEF

You told me HEAD was `4ce8664` and that the reconciler was the remaining open item. It is not:

```
12b4df2  fix(titan): the size-mismatch alert told the operator to look for the wrong number  <- MINE
1db2b4c  feat(titan): exchange->DB reconciliation at boot — the mirror nobody was checking   <- Part 2, ALREADY DONE
4ce8664  LIVE: both mode flags True again — entry path fixed, six proofs green               <- where you thought HEAD was
97a4fdb  fix(titan): the naked-position defect, its CLASS, and the race neither cap caught
```

`1db2b4c` was committed at **22:19:43** and the service restarted at **22:20:11** — *after* the
commit, so the reconciler has been running in live since before this session began. The session
dropped after deploying but **before reporting**, which is why you did not know.

I did not take that on trust. Everything below is re-verified from scratch.

---

# PART 1 — TEN CHECKS, ALL CLEAN

| # | check | result |
|---|---|---|
| 1 | git clean · HEAD · origin sync · `97a4fdb` pushed | clean · `12b4df2` · `0 0` ahead/behind · yes, on `main` and `origin/main` |
| 2 | runtime = commit **by hash** | all four order-path files byte-identical to HEAD (`sha256`), all mtimes **precede** process start 22:20:10 |
| 3 | boot banner from LIVE journal | 🔴 LIVE ORDERS, **$30 × 5 = $150** — the live number, not paper $10000 |
| 4 | service · uptime · NRestarts · errors · breaker | `active` · NRestarts **0** · **0** errors/tracebacks/CRITICAL/refusals · breaker `{'tripped': False}` |
| 5 | exchange, both probes | **0** positions (all symbols), **0** orders unified *and* raw swapV2, USDT free 512.6111 / **used 0.0** |
| 6 | `virtual_positions` | **0** open rows · `MAX(id)` = **85** · `breakeven_jobs` 0 — identical to the 21:57 report, untouched |
| 7 | flags at runtime | `LIVE_TRADING_ENABLED=True`, `ORDER_ADAPTER_LIVE=True`, `LIVE_FIXED_MARGIN_USDT=30.0`, `LEVERAGE=5`, `MAX_POSITIONS_PER_SIDE=1` — match the 21:57 report |
| 8 | Mercury-SOL | `active` since **2026-07-21 06:39**, NRestarts 0, processing webhooks at 22:10 — untouched |
| 9 | scope audit re-run | ✅ all four modules, **192 function scopes**, exit 0 |
| 10 | the five fixes in running code | all five present — evidence below |

### Check 2 — the hash proof, not mtime

```
order_adapter.py   workdir c66cf067e14e942b == HEAD c66cf067e14e942b
virtual_trader.py  workdir abc600b7312906f3 == HEAD abc600b7312906f3
main.py            workdir 5265514808eb2049 == HEAD 5265514808eb2049
config.py          workdir de96898a5cbdbdca == HEAD de96898a5cbdbdca
```

Process start **22:20:10**; latest source mtime **22:15:40**; every `.pyc` predates start and
postdates its source. Nothing changed under the running process — the
`module_staleness` failure mode is not present here.

### Check 3 — the banner, verbatim from the live journal

```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
[TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
[RECONCILE] boot reconciliation starting
[RECONCILE] done
```

The `RECONCILE-XDB` line is the new gate, running in live, passing cleanly.

### Check 9 — scope audit, with a caveat I am not going to hide

The 21:57 script died with its session, so **this is a rewrite**, not the same file:

```
✅ all globals resolve  virtual_trader.py      (53 scopes checked)
✅ all globals resolve  order_adapter.py       (27 scopes checked)
✅ all globals resolve  breakeven_worker.py    (22 scopes checked)
✅ all globals resolve  main.py                (90 scopes checked)
192 function scopes checked across 4 modules.   EXIT=0
```

192 scopes, not the 156 the 21:57 report recorded. Some of that is new code, but
`breakeven_worker.py` was **not touched tonight** and still went 20 → 22 — so my walker counts
nested `def`s and lambdas that the original did not. It is a **superset** of the original check,
so the green verdict is not weaker than the one that found the `LIVE_TRADING_ENABLED` defect.
I am flagging it because "192 ≠ 156" would otherwise look like drift.

### Check 10 — the five fixes, located in the running code

| # | fix | evidence |
|---|---|---|
| 1 | `execute_entry` takes `send_tg` | `virtual_trader.py:628` — `entry_atr_pct_1h=None, send_tg=None)`; call site `main.py:1307` passes `send_tg=send_tg` |
| 2 | `BaseException` wrapper | `virtual_trader.py:782` `IRREVERSIBLE FROM HERE`, `:938` `except BaseException as _entry_exc`, `:945` failsafe close |
| 3 | lock **before** the order | `:752` `_entry_lock.acquire(timeout=...)` → `:759` authoritative pre-order capacity check → `:775` `market_entry` → `:949` `release()` in `finally` |
| 4 | `market_reduce` sheds `reduceOnly` | `params={'positionSide': position_side}` only |
| 5 | tracebacks in all three handlers | `main.py:2144` plain-text 5m · `:3784` state machine · `:4307` P3, each with its own label |

`import traceback` did not match my anchored grep — it is line 1, comma-separated. Since that is
*exactly* the defect class, I checked it at runtime rather than trusting the audit:

```
traceback resolves: True
LIVE_TRADING_ENABLED in main: True = True      <- the second NameError, confirmed fixed
execute_entry sig tail: 1h=None, entry_atr_pct_1h=None, send_tg=None)
reconciler present: True
_UNSAFE_STATE (breaker) now: {'tripped': False, 'detail': None}
```

**Nothing is off. Nothing was lost.**

---

# PART 2 — THE RECONCILER

## What it does

`assert_exchange_matches_db_at_boot` in `order_adapter.py`, called from `gunicorn.conf.py`
`when_ready` **before** `main.reconcile_boot_state()` — deliberately, because
`reconcile_boot_state` can *place a stop* on a live position, and it must never do that for a
position the DB cannot explain.

Three refusable conditions:

| condition | meaning |
|---|---|
| `NO_ROW` | exchange position with no open row — **the state that cost money tonight** |
| `SIZE_MISMATCH` | row and position differ by >1% — the doubled-entry signature, previously invisible |
| `SIDE_MISMATCH` | a row whose `side` contradicts its own `position_side` |

**Doubled probes**, as you required: positions and orders are each asked through the ccxt unified
call **and** the raw `swapV2` endpoint, and the **union** is taken — if either sees a position, it
exists. I proved this matters: a position visible *only* to the raw endpoint is still caught.

## 🔴 THE DEFECT I FOUND IN IT — and it is the same class as tonight's other two

The size-mismatch metric divides by the **larger** side:

```python
denom = max(rsz, psz) or 1.0
if abs(rsz - psz) / denom > BOOT_RECONCILE_SIZE_TOL_PCT:
```

So tonight's actual failure — row `0.0023` vs exchange `0.0046` — prints **50.0%**. The sentence
bolted to it read *"A ~100% gap is the signature of a DOUBLED entry"*. Emitted verbatim by the
gate in my run:

```
[SIZE_MISMATCH] SHORT: exchange size 0.0046 vs row 86 step_size 0.0023 —
differ by 50.0% (tolerance 1%). A ~100% gap is the signature of a DOUBLED entry
```

An operator reading that during an incident sees **50% next to a claim that the signature is
100%** and concludes *this is not the doubling case*. The one alert built to make a doubled entry
recognisable was telling them to look for the wrong number.

This is the third instance tonight of the same class: the `(confluence)` label on the
state-machine path, `_refuse_to_start`'s hardcoded routing text, and now this. **A label that
lies costs diagnostic time exactly when there is none to spend.**

Fixed — **text only**, no threshold, no metric, no branch; every refusal decision is bit-identical:

```diff
--- a/titan-bot/order_adapter.py
+++ b/titan-bot/order_adapter.py
@@ -335,8 +335,10 @@ def _find_mismatches(positions, rows):
                         f"{ps}: exchange size {psz} vs row {row['id']} "
                         f"step_size {rsz} — differ by "
                         f"{abs(rsz - psz) / denom * 100:.1f}% (tolerance "
-                        f"{BOOT_RECONCILE_SIZE_TOL_PCT:.0%}). A ~100% gap is the "
-                        f"signature of a DOUBLED entry"))
+                        f"{BOOT_RECONCILE_SIZE_TOL_PCT:.0%}). NOTE the gap is "
+                        f"relative to the LARGER side, so a DOUBLED entry — the "
+                        f"2026-07-29 failure — prints ~50%, not ~100%. Compare "
+                        f"the two raw numbers above, not the percentage"))
     return bad
```

Committed `12b4df2`, deployed at 22:47 **while the book was flat** (verified 0 positions / 0
orders / `used` 0.0 immediately before the restart), pushed, `0 0` with origin.

## Your point 3 — refuse, do not act. **I agree, and not merely because you said so**

You asked me to say if I disagreed. I do not, and the reason is narrower than "acting is risky":

A position with no row has **no known intended stop**. Auto-placing one means inventing a level
from an entry price we cannot vouch for, and then handing the position to a manager that has no
row to manage it with — a stop that exists but is owned by nobody, which is a *worse* state than
naked because it looks protected. Auto-closing is the more defensible of the two, but it is still
a real market order sized from a number we just admitted we cannot explain.

Refusing is the only option whose failure mode is *the bot does not trade*. That is the honest
one, and it matches what you did with the naked short at 21:29 — closed **by hand**, after
looking.

One caveat I will state plainly rather than bury: **this trades availability for safety.** A
BingX outage that fails both probes keeps the bot down (`cannot_verify` → refuse). For a
live-money gate that is the right direction, but it is a real cost and it is deliberate.

## Your point 4 — exactly what a human does to clear the refusal

This ships **inside the Telegram alert**, not just in this report — a gate that refuses without
saying how to proceed only moves the problem:

```
Fix (a human, by hand — this gate deliberately does NOT act):
  1. Look at the exchange and decide: close the position, or attach a stop.
     Both are manual. The bot will not do either while this gate holds.
  2. To CLOSE it (hedge mode — do NOT pass reduceOnly, BingX rejects it
     with code 109400):
       exchange.create_market_order(SYMBOL, 'buy' if SHORT else 'sell',
                                    amount, params={'positionSide': SIDE})
  3. Verify flat: fetch_positions() shows 0, fetch_open_orders() shows 0,
     AND the raw swapV2 endpoint agrees. Check both, not one.
  4. Then restart: systemctl restart titan.service
  To stay down instead, set ORDER_ADAPTER_LIVE=False in config.py and
  restart — paper cannot touch the exchange, and this gate is skipped.
  Do NOT hand-write a virtual_positions row to silence this. A row invents
  an entry price, a stop and a risk figure that never existed, and every
  P&L number downstream would be a fabrication.
```

Step 2 carries tonight's `109400` lesson, so the operator does not repeat the rejected call under
pressure. The last paragraph closes the obvious wrong shortcut.

The alert also **names the position**, as you required — size, entry, which probe saw it, and
whether any stop exists:

```
🛑 TITAN REFUSED TO START
EXCHANGE AND DB DISAGREE for BTC/USDT:USDT — confirmed across 3 probes, so this is not venue lag:
  [NO_ROW] SHORT 0.0046 @ entry 63500.0 (seen via unified) has NO open virtual_positions row —
  it is UNMANAGED: no SL check, no trail, no breakeven, no recheck, no passive-fill reconciliation
  PROTECTION SHORT: 🔴 NONE — no stop, no TP, no trigger order of any kind. THE POSITION IS NAKED.
The bot is NOT running and is NOT trading.
```

(That alert text is itself a fix in `1db2b4c`: `_refuse_to_start` previously **hardcoded** the
item-12 routing reason, so *every* refusal told the operator the same wrong cause.)

## Your point 5 — can this produce a FALSE refusal?

You asked specifically about the window between `market_entry` and the `INSERT`. **The window is
real — but it is not a transient, and treating it as one would be the bug.**

- **Graceful restart (`systemctl restart`, SIGTERM).** `gthread` worker, `graceful_timeout = 30`.
  An in-flight entry — order plus stop, a few seconds — finishes and writes its row. Nothing is
  orphaned, so there is nothing to refuse.
- **SIGKILL inside the window** (OOM, `timeout = 30` worker kill, `kill -9`). The thread that
  would have written the row is dead. **No row will ever appear**, and any uncommitted sqlite
  transaction was rolled back. That is a genuinely naked position — refusing is *correct*, and
  waiting it out would just be booting past it more slowly.

So the honest answer is: the transient exists but is self-resolving only in the case where there
is nothing to detect. Three other sources of *genuine* false refusal are handled, and I proved
each one:

| source | handling | proof |
|---|---|---|
| venue reporting lag after a close | mismatch re-probed 3×, 2s apart; refuses only if it survives every probe | `transient` → exit 0 |
| residual dust from a close | `BOOT_RECONCILE_DUST = 1e-6` floor | `dust` → exit 0 |
| open **row** with no position | **not** refused — that is the passive-fill case (item 13); refusing would break healthy restarts | `orphan_row` → exit 0 |

**One residual risk I want on the record, because nobody has said it out loud:** the gate keys
both sides by `positionSide` (`LONG`/`SHORT`). If the account were ever switched to **one-way
mode**, BingX reports `positionSide: BOTH`, no row would ever match, and every boot would refuse
with `NO_ROW`. The account is in hedge mode — proven tonight by the `109400` rejection — so this
is not a live risk today. It is a **latent coupling to hedge mode**, and it would present as a
total refusal to boot rather than as anything subtle. Not fixed; recorded.

## The proofs — 12/12, my own harness, not the prior session's

The 21:57 session claimed 10/10. I did not reuse it. Each scenario runs in its **own subprocess**
(the gate refuses via `os._exit`, which cannot be caught), against a **copy** of `trades.db`, with
a captured `send_tg`, a redirected throttle file, and a fake exchange — no network, nothing live
touched.

```
clean              exit=0 want=0  PASS  flat exchange, no rows -> boots
paper              exit=0 want=0  PASS  paper mode -> gate does not engage
matching           exit=0 want=0  PASS  row and position agree -> boots
orphan_row         exit=0 want=0  PASS  open row, no position (passive fill) -> NOT fatal
dust               exit=0 want=0  PASS  residual dust below floor -> not a position
transient          exit=0 want=0  PASS  venue lag that clears on re-probe -> boots
phantom_unified    exit=3 want=3  PASS  REFUSE: exchange position with NO row
phantom_raw_only   exit=3 want=3  PASS  REFUSE: position seen ONLY by the raw endpoint
size               exit=3 want=3  PASS  REFUSE: 2x size = doubled-entry signature
side               exit=3 want=3  PASS  REFUSE: row contradicts its own position_side
cannot_verify      exit=3 want=3  PASS  REFUSE: unverifiable is NOT flat
naked_no_stop      exit=3 want=3  PASS  REFUSE: names the position as NAKED
ALL PASS
```

`phantom_raw_only` is the one that justifies your instruction to probe twice: the position is
invisible to `fetch_positions` and visible only to raw `swapV2`, and it is still caught. **One
probe would have booted straight past it.**

*Method note:* my first run failed two scenarios on `NOT NULL constraint failed:
virtual_positions.step_margin_usdt`. That was **my harness**, not the gate — my synthetic row
omitted required columns. Fixed to fill every NOT NULL column from `PRAGMA table_info`, so the
test row satisfies the real live schema. Recording it because a proof that was edited until it
passed is worth less than one that says why.

---

# CONFIRMATIONS YOU ASKED FOR

| | |
|---|---|
| banner | 🔴 **LIVE ORDERS**, `$30 × 5 = $150` — re-verified after my redeploy at 22:47 |
| exchange flat, check passes cleanly | `[RECONCILE-XDB] ✅ exchange and DB agree ... 0 exchange position(s), 0 open row(s)` |
| refusal path proven | 6 refusal scenarios → `exit 3`, alert names position/size/entry/protection + operator steps |
| live book | **0** open rows, `MAX(id)` = **85**, `breakeven_jobs` 0 — unchanged by all testing |
| errors since restart | **0** — no traceback, no NameError, no CRITICAL, no refusal, breaker untripped |
| Mercury-SOL | `active` since 07-21, NRestarts 0 — untouched |

## Nothing else was touched — proven by diff, not asserted

Since going live (`4ce8664..HEAD`) only **two** files changed:

```
titan-bot/gunicorn.conf.py |  24 ++++      <- the boot call
titan-bot/order_adapter.py | 332 +++++-    <- reconciler block + refusal-alert text
```

`git diff 4ce8664..HEAD -- virtual_trader.py config.py main.py` → **0 lines**. So the entry
wrapper, the entry lock, `market_reduce`, the diagnostics/labels, the HTF cascade, the score gate,
SL/trail/breakeven, the signal tiers and the exit advisor are all **provably** as they were when
the six proofs passed. The two `order_adapter.py` hunks are at lines 171 and 233 —
`market_reduce` is in neither.

---

## STATE AS OF 22:50 UTC

| | |
|---|---|
| HEAD | **`12b4df2`**, pushed, `0 0` with `origin/main` |
| mode | 🔴 **LIVE ORDERS** — both flags True |
| sizing | **$30 × 5 = $150** notional |
| exchange | **FLAT** — 0 positions (all symbols), 0 orders (unified **and** raw), `used` 0.00 |
| USDT | 512.6111 |
| service | `active`, restarted 22:47, NRestarts 0 |
| gates at boot | routing · passive-fill · paper-position · **exchange→DB (new)** — all pass |

**The last open item from the 21:32 list is closed.** The mirror direction is now checked, the
doubled-entry signature is visible for the first time, and the compound case you named — failsafe
close fails 3×, breaker trips, restart resets the in-process breaker — no longer resumes trading
with a healthy banner. It refuses, and it says why and what to do.
