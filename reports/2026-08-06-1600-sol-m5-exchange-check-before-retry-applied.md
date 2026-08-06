# SOL M5 — THE EXCHANGE CHECK BEFORE THE RETRY. THE GUARANTEE NO LONGER RESTS ON AN UNPROVEN VENUE BEHAVIOUR.

**2026-08-06 16:00 UTC · Mercury-SOL (PAPER) · APPLIED AND PROVEN BY EXECUTION.**

Subject: `/mnt/volume_nyc1_1780480650620/mercury-sol`.
Titan (`/root/titan-bot`, LIVE REAL MONEY): **not touched** — clean at `897850b`, workers
2538048/2538082 up since 01:53:18.

**This was the last money-path item on SOL.**

---

## THE ANSWER FIRST

The belt-and-braces form is built. **The key stays; the check is added and it is the load-bearing half.**

```
── A. Order LANDED, then 403. Venue does NOT enforce the key (the real test) ──
   PRE-FIX   orders at the venue: 2      🔴  double-size entry
   POST-FIX  orders at the venue: 1      ✅  found and ADOPTED, retry never sent
```

Five scenarios, both trees, on a fake venue. **Post-fix: exactly one order in every case, including
when the check itself fails.**

---

# 1. WHAT WAS BUILT

## a) The check, per write path — and what "already exists" means for each

`with_socks_retry_write` now takes `find_existing(exchange, idem_key) -> order|None` and queries it
**before every retry attempt**. Found → **adopt and return it**; no second order is sent.

The generic scanner `tor_retry.find_order_by_client_id` reads the unified `clientOrderId` field ccxt
already maps from Bybit's `orderLinkId` (bybit.py:3711,3750). It scans **open *and* closed** orders,
which matters more than it looks:

> 🔴 **A market order that reached the matching engine fills immediately, so it is NOT in
> `fetch_open_orders`.** Checking only open orders would have missed precisely the case this exists to
> catch. (`fetchOrders` is `False` for bybit in ccxt 4.5.52; `fetchOpenOrders` and `fetchClosedOrders`
> are both `True` — verified against the installed module.)

**What counts as existing** — an order that reached the engine, whether or not it is still working:

| state | verdict |
|---|---|
| status `open` or `closed` | **exists** → adopt |
| any `filled > 0` | **exists**, whatever the status → adopt |
| `canceled`/`rejected`/`expired` with **zero** filled | did **not** take effect → does not block a retry |

That last row is deliberate: a rejection is the venue saying the order never happened, and treating it
as existing would strand a write that genuinely needs placing.

**Per path — because a partial's reduce and an entry's open are not the same object:**

| path | key | "already exists" means | shape checked |
|---|---|---|---|
| **entry** | `sol-e-{row_id}` | an **opening** order — a position may now exist | **not** reduceOnly, side == entry side |
| **close** | `sol-c-{side}-{epoch}` | a **reduce-only** order closing the position | reduceOnly, side == close side |
| **partial** | `sol-p-{vpos_id}` | a **reduce-only** leg for the partial size (one partial per position) | reduceOnly, side == close side |

Each probe validates the shape, and **a shape mismatch is not treated as "not found"** — finding that
key attached to an order we do not recognise is an anomaly, and the safe response to an anomaly on a
money path is to refuse, not to place a second market order. Adopting an opening order in the close
path would report a position closed while it had just been opened; the reverse would report a position
opened when something was being closed.

*(The partial keeps its correctness for free: the caller reads `filled` back off the returned order —
F3 — so an adopted order yields the size that **actually** reduced, never the size that was asked for.)*

## b) 🔴 When the CHECK ITSELF fails — refuse, never retry

Your reading is the one implemented. A failed check raises **`WriteUnconfirmed`**, and the retry loop
stops there:

```python
except Exception as _pe:
    print("🚨 WRITE ... venue check FAILED. Whether the first attempt landed is "
          "UNKNOWN — NOT placing a second order.")
    raise WriteUnconfirmed(idem_key, _pe) from _pe
```

**An unknown result buys no second placement.** There is a designed answer to "I could not place it" —
`status='failed'`, an alert, a human looks. There is no answer to "I placed it twice and did not
notice." The entry path gets its own distinct alert, deliberately separate from `DuplicateSuppressed`:
there the first order is **proven** to have landed; here it is **unknown**. Same action, different
sentence — and the difference is what the operator needs to know.

`find_order_by_client_id` therefore **never returns `None` to mean "I could not look."** `None` means
"I looked and it is not there." The whole decision rests on that distinction being preserved.

## c) Reads keep their blind retry — verified by diff, not asserted

```
$ diff <(old with_socks_retry) <(new with_socks_retry)
✅ READ PATH BYTE-IDENTICAL
```

`with_socks_retry` is untouched. Reads are idempotent and they are what keeps this bot alive through
Tor. The trail also stays on the read wrapper by design — `trading-stop` is a position-level SET.

## d) No future write path can skip this

`find_existing` has **no default**. A new write cannot be added without deciding. Opting out requires
passing the explicit, greppable `tor_retry.NO_PROBE` sentinel, which logs a 🔴 line saying the retry is
resting on unproven venue enforcement. **All three current call sites pass a real probe** — verified:
`grep -c "find_existing=" → 3`.

---

# 2. PROVEN BY EXECUTION — BOTH DIRECTIONS

Isolated tree, **13-file DB_PATH rewrite**, residual grep 0, sqlite leak assert
(**`production-book opens: 0`** in every run), **isolated `.env` loaded before `import config`**.

The fake venue models **the case that matters**: `create_market_order` **records the order** (it
reaches the matching engine) and *then* raises `403 Forbidden / Request blocked`. Its `enforce_key`
flag models the unproven behaviour, and **the headline test runs with it OFF** — the pessimistic
assumption the fix must not depend on.

| # | scenario | PRE-FIX orders | POST-FIX orders | post-fix outcome |
|---|---|---|---|---|
| **A** | **landed → 403, venue does NOT enforce the key** | **🔴 2** | **✅ 1** | found at venue, **ADOPTED** |
| B | landed → 403, venue DOES enforce | 1 | ✅ 1 | adopted (check fires before the key even matters) |
| C | never landed (403 before the engine) | 1 | ✅ 1 | not found → retry placed it, once |
| D | **landed → 403, and the CHECK ITSELF FAILS** | **🔴 2** | **✅ 1** | **`WriteUnconfirmed` — refused** |
| E | reduce-only close leg, landed → 403 | **🔴 2** | ✅ 1 | adopted |

**Row A is the whole finding.** Pre-fix, the only thing standing between a 403-after-success and a
double-size entry was the venue choosing to enforce `orderLinkId`. With that assumption removed, the
old code places two orders. The new code places one and never sends the retry at all
(`create_market_order calls: 1`).

**Row C proves the fix does not overcorrect** — a write that genuinely failed is still placed, exactly
once. **Row D proves the refusal path**: one order at the venue, and the second was never attempted.

Post-fix log line from run A:

```
[SOCKS_RETRY] WRITE test idem=sol-e-999 FOUND AT VENUE (id=VENUE-1 status=closed filled=10.0)
              — ADOPTED, no second order placed.
```

---

# 3. 🔴 THE CANON CLAIM IS CORRECTED

`OPEN-ITEMS-SOL.md` §Phase-1 item 2 previously read:

> *"order writes carry a stable venue idempotency key (`orderLinkId`), **so a 403 retry cannot place a
> second order**."*

**That was overstated, and it is now corrected in the canon itself.** What had been verified was only
that the field is **accepted and transmitted** — ccxt sets `request['orderLinkId']` from
`clientOrderId` (bybit.py:4049-4054) and retCode `110072` is mapped (bybit.py:751).
**Accepting a field and enforcing it are different claims, and only the first was ever proven.**

The canon now states what is guaranteed and by which mechanism:

| mechanism | what it gives | rests on |
|---|---|---|
| **the venue CHECK — load-bearing** | queried before every retry; an existing order is **adopted**, no second sent | only that `fetch_open_orders`/`fetch_closed_orders` return the `clientOrderId` ccxt already maps — **no assumption about enforcement** |
| the idempotency key — second line | if Bybit *does* enforce, 110072 → `DuplicateSuppressed` | **unproven venue behaviour** |
| **`WriteUnconfirmed`** | if the check fails, the write **refuses** | nothing |

And it says plainly: **Bybit's enforcement of `orderLinkId` uniqueness remains UNPROVEN, it would take
two real duplicate orders at the venue to establish, that is not an experiment worth running on a money
path, and the guarantee no longer depends on it.** The key is kept as the cheap second line — if Bybit
does enforce, 110072 catches the narrow race the check cannot see.

> **This is the same shape as every "reads as armed" defect found this week: a mechanism the system
> SETS but never READS BACK.** The key was set and never verified. Now it is verified.

---

# 4. THE CHANGE, AND WHAT WAS NOT TOUCHED

**Code-only diffs (comments and blanks stripped):**

```
tor_retry.py   + WriteUnconfirmed, + NO_PROBE, + find_order_by_client_id(),
               + the pre-retry check block;  with_socks_retry_write gains a REQUIRED find_existing
               🔴 with_socks_retry (the READ wrapper) — BYTE-IDENTICAL
main.py        + 3 per-path probes (_entry_exists / _close_exists / _partial_exists),
               + find_existing= on all 3 write sites, + 1 WriteUnconfirmed handler on entry
OPEN-ITEMS-SOL.md   the overstated guarantee corrected in place
```

`main.py`'s code-only diff contains **nothing but the above** — **M1–M7 do not appear in it.**
`claude_advisor.py` **12:15:12, untouched** — the cascade, the score bars, both prompts and the state
dedup all live there and were not opened. `state_machine.py` untouched.

**Backups:** `tor_retry.py.bak_M5_exchange_check_20260806`, `main.py.bak_M5_exchange_check_20260806`,
`OPEN-ITEMS-SOL.md.bak_M5_20260806`.

---

# 5. FINAL STATE — restarted from flat

```
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h
                    OBSERVATION_MODE=True [pid 2738195]
```

The boot line — shipped an hour ago for exactly this purpose — reports the **worker's own** constants,
and its pid matches the forked worker. No inference required this time.

```
mercury-sol.service  active (running)   master 2738106   worker 2738195 (15:51:04)   NRestarts=0
tracebacks since restart : 0
open vpos / active_positions / exit_pending : 0 / 0 / 0      (flat since 2026-08-03)

OBSERVATION_MODE = True    SL_BUFFER_ATR = 2.5    TRAIL_MULT_ATR = 1.875 (0.750R)
ATR_TF = '1h'   MAX_POSITIONS_PER_SIDE = 1   WALL_V2_CEILING = 20.0   NEWS_PINNED = True
write sites passing find_existing : 3 / 3

TITAN: git clean · HEAD 897850b · workers 2538048/2538082 up since 01:53:18 · NOT TOUCHED
```

**Nothing in this pass changes a trading decision — the live write paths are unreachable in
`OBSERVATION_MODE`. The n=8 trail re-measurement is unaffected; the next trailed exit is still
observation 1 of 8.**

---

*Generated 2026-08-06 16:00 UTC.*
