# sol-recheck-okx4000-no-substitute-venue

_2026-08-02 17:40 UTC_

---

# MERCURY-SOL — POST-ENTRY RECHECK MOVED TO OKX-4000, WITH NO SUBSTITUTE VENUE

**2026-08-02 ~17:50 UTC.** Mercury-SOL only. **Titan (`/root/titan-bot`, LIVE) was not touched
and not read.** Applied and live, worker pid **1503515**, restart 17:47:5x.

| | |
|---|---|
| freeze | **NOT touched** — `claude_advisor.py` / `config.py` unmodified, mtimes still 08-01 20:54 / 08-02 13:34 |
| 200-window | **86 / 200** — unchanged across the restart, **not reset** |
| vpos 26 | **open**, entry 73.53, **SL 72.59 unchanged**, `original_sl_price` 72.59, water_mark 73.65, `recheck_status='done'` |
| errors since restart | none |
| files changed | `virtual_trader.py` only (backup `virtual_trader.py.bak_recheckokx_20260802`) |
| DB backup | `trades.db.bak_pre_recheckokx_20260802` |

---

## 0. FREEZE CHECK — ARGUED, AND IT PASSES

**The claim to verify: the entry advisor reads nothing this change touches.**

1. **`claude_advisor.py` imports no book module at all.** Its complete import list is
   `json`, `re`, `datetime`, `anthropic`. There is no path from `virtual_trader`,
   `microstructure`, `liquidity_zones` or `skip_attribution` into it — `pre_trade_walls` arrives
   as a **function parameter**, supplied by `main.py:3042` from
   `liquidity_zones.fetch_pre_trade_walls` (OKX-4000). That call site is **not modified**.
2. **`virtual_trader` is downstream of the entry decision by construction.** The recheck runs at
   T+10/60/300 **seconds after the fill**; the advisor has already answered before the position
   exists.
3. **Nothing the recheck writes is read at entry.** `entry_wall_baseline_mult` has exactly one
   reader in the codebase — `virtual_trader.py:1202`, inside `_run_recheck_tier` itself.
4. **The one thing I checked that could have stopped this, and did not:** two lines in the frozen
   file still name the wrong venue —
   `claude_advisor.py:287` (*"pre_trade_walls — microstructure.fetch_pre_trade_walls() dict
   (depth-100…)"*) and `:420` (*"microstructure depth-100 from the bot's own hands' exchange:
   Bybit for SOL"*). **Both are comments/docstrings, not prompt text.** `_format_pre_trade_walls`
   renders the block and never emits a venue name — the model has never been told which exchange
   the book came from. So these are stale **labels**, which the freeze explicitly does not cover,
   and they change nothing the advisor reads. **See §4.3 — named, not fixed.**

**Conclusion: outside the frozen surface. Proceeded.** Window count re-read after the restart:
**86/200**, unchanged.

---

## 1. OKX-4000 IS NOW THE ONLY WALL SOURCE ON THE RECHECK PATH

`_walls_with_okx_fallback` is **deleted**, not re-ordered, and replaced by `_walls_okx(symbol)`.
Deleting rather than keeping it alongside follows the precedent set at `main.py:1605`:
*"The ambiguous helper is DELETED rather than kept alongside: leaving it would let a future caller
re-introduce this exact bug by reaching for the shorter name."*

```diff
-def _walls_with_okx_fallback(exchange, symbol):
-    """Primary: microstructure.fetch_pre_trade_walls(exchange, symbol) — Bybit
-    depth-100 over Tor ... On that None we fall back to liquidity_zones ...
-    A position opened pre-block and refreshed mid-block can mix sources —
-    accepted: a slightly cross-scaled ratio beats losing the wall signal entirely."""
-    try:
-        walls = microstructure.fetch_pre_trade_walls(exchange, symbol)   # Bybit-100
-    ...
-    if walls is not None:
-        return walls
-    okx = liquidity_zones.fetch_pre_trade_walls(symbol)                  # OKX-4000
-    return okx
+def _walls_okx(symbol):
+    """OKX books-full depth-4000 opposing-wall source — the ONLY wall source on
+    the recheck path. Returns a walls dict, or **None meaning THE READ FAILED**.
+    [full rationale in source]
+    🔴 NO SUBSTITUTE VENUE. When OKX is unreachable this returns None and the
+    caller MUST treat that as "could not measure" — the POS_UNKNOWN discipline
+    (main.py:1609-1631)."""
+    try:
+        import liquidity_zones  # lazy: keyless OKX, no Tor — pure leaf
+        return liquidity_zones.fetch_pre_trade_walls(symbol)
+    except Exception as e:
+        print(f"{LOG_PREFIX}[WALLS] OKX-4000 wall read FAILED ({e}) — "
+              f"NO substitute venue, wall dimension is UNMEASURED", flush=True)
+        return None
```

Both call sites now use it — the entry **baseline** (`virtual_trader.py:252`) and every
**refresh** (`:1192`) — so baseline and refresh are same-venue, same-depth, same threshold by
construction rather than by luck.

**Why the old one was wrong beyond the venue mixing**, recorded in the new docstring:

- `mult` is a bucket's volume over the **mean bucket volume of that book**. A 100-level book and a
  4000-level book have wildly different means, so a Bybit-100 baseline against an OKX-4000 refresh
  is not a ratio of the same quantity — the number silently changed meaning mid-life.
- The two sources use **different wall thresholds**: `MICROSTRUCTURE_WALL_MULTIPLIER = 3.0` vs
  `PRE_TRADE_WALL_MULTIPLIER = 4.0`. Even the *set* of levels that counted as a wall differed
  between primary and fallback.
- The shallow book is not informative, as SOL proved: row 15093 stored `walls_ask: []` from Bybit
  depth-20 at the very instant the advisor was shown **×20.3 at $73.75** from OKX-4000 — the wall
  that produced the verdict, invisible on the venue's own book.

`import microstructure` is now **gone from `virtual_trader.py`** — nothing in that module reads a
venue book any more, and leaving the import would invite a future caller to reach for it. The
module-level comment that described the recheck as using `microstructure.fetch_pre_trade_walls`
was corrected in place; it had been describing two different books in one sentence.

---

## 2. 🔴 WHEN OKX IS UNREACHABLE — AND THE PROOF THAT IT CANNOT SCORE AS A PASS

### 2.1 What was broken

`_max_opposing_wall_mult` already distinguished the two cases, and **both were consumed
identically**. On a failed read the wall rule was silently skipped inside `_health_score`, the
surviving rules scored 0, `_recheck_verdict(0)` returned `'OK'`, and the tier was written
`t+N_ok` with a **"🩺 Post-entry T+Ns OK … ✅"** Telegram. **A failed read was recorded as a
passing check.**

### 2.2 The guard

```python
if cur_walls is None and verdict == 'OK':
    print(f"...RECHECK vpos={vpos_id} ... T+{tier}s UNMEASURED — OKX-4000 book "
          f"unreadable, wall rule has NO SIGNAL. Partial score={score} is an upper "
          f"bound only; NOT recording t+{tier}_ok, NOT acting. Will retry next tick.")
    return None
```

`recheck_status` is **deliberately left untouched**, so the same tier is still due on the next
poll tick and retries automatically once OKX answers. No new status value was introduced — which
is what keeps the tier state machine intact (see §2.4).

### 2.3 Why negative verdicts still act, and OK does not — the monotonicity argument

`_health_score` is **monotone: every rule only ever subtracts.** A score computed with one rule
missing is therefore an **upper bound** on the true score.

- If that upper bound already reaches TIGHTEN/EMERGENCY → the true score reaches it too → the
  negative verdict is **sound**, and suppressing it would leave a bad position unprotected.
- If the upper bound merely says OK → the true score could be anything at or below it. **OK is not
  established**, and the missing wall rule is precisely the one that could have pushed it negative.

So the guard is conditioned on `verdict == 'OK'`, not on `cur_walls is None` alone. This is not
"treat the failure as degraded" either — nothing is recorded, nothing is scored, nothing is acted
on. **No signal.**

### 2.4 Executed proofs — run against the module as it now stands

**A. "read failed" and "no wall in the book" are genuinely distinct values**

```
read failed   -> _max_opposing_wall_mult(None, 'LONG')                 = None
read ok, none -> _max_opposing_wall_mult({'walls_ask': []}, 'LONG')    = 0.0
read ok, wall -> _max_opposing_wall_mult({'walls_ask':[{'mult':20.3}]}) = 20.3
```

**B. Monotonicity holds — the partial score really is an upper bound**

```
wall rule present, wall grew ×2.45 : score = -10
wall rule MISSING, same inputs     : score =   0     <- 0 >= -10 ✓
```

**C. The old behaviour, reproduced**

```
partial score = 0 -> _recheck_verdict = 'OK'
...which reached _set_recheck_status(vpos, 't+N_ok') and a "🩺 OK ✅" Telegram.
```

**D. A failed read can no longer reach any status write — proof by source order** of the running
`_run_recheck_tier` (`inspect.getsource`, character offsets):

| status write | offset | reachable when unmeasured+OK? |
|---|---|---|
| guard `if cur_walls is None and verdict == 'OK': return None` | — | — |
| `_set_recheck_status(vpos_id, 'closed_critical')` | 3614 | **AFTER guard → unreachable** |
| `recheck_status='tightened'` UPDATE | 4974 | **AFTER guard → unreachable** |
| `_set_recheck_status(vpos_id, f"t+{tier}_ok")` | 5565 | **AFTER guard → unreachable** |

Every write — and every `send_tg` — sits after the `return None`. There is no path from a failed
book read to a recorded pass.

**E. Negative verdicts still act, unmeasured or not**

| scenario (book unreadable in all four) | partial score | verdict | behaviour |
|---|---|---|---|
| ADX collapse | −8 | TIGHTEN | **ACTS** — bound already negative |
| price against entry | −3 | OK | suppressed, retried next tick |
| both | −11 | EMERGENCY_CLOSE | **ACTS** — bound already negative |
| all quiet | 0 | OK | suppressed, retried next tick |

**F. No venue leak**

```
_walls_okx source calls : ['import liquidity_zones  # lazy: keyless OKX, no Tor — pure leaf',
                           'return liquidity_zones.fetch_pre_trade_walls(symbol)']
'microstructure.' in the function body      : False
virtual_trader has attribute 'microstructure': False
```

**G. The retry cannot loop forever, and needs no new state.** `_recheck_tier_due` derives the due
tier from `last_status` alone (`if elapsed_sec >= t and t > last_tier: due = t`). Leaving the
status untouched means the same tier stays due — automatic retry. The caller marks `'done'` once
elapsed passes `RECHECK_TIERS_SEC[-1]` (300s), **outage or not**, so a persistent OKX outage ends
the recheck by time rather than spinning.

---

## 3. `entry_wall_baseline_mult` — NO IN-FLIGHT POSITION CHANGES MEANING

**Your expectation is correct, and it is provable rather than a policy statement.**

New positions capture an **OKX-4000** baseline and refresh against OKX-4000. Old positions keep
their own stored baseline — the column is never rewritten, and nothing backfills it.

**vpos 26 specifically:** `entry_wall_baseline_mult = 10.2`, captured from **Bybit depth-100**,
while the advisor was shown **×20.3** from OKX-4000 at the same instant. **Its ratio cannot change
meaning, because its recheck is over:**

- `recheck_status = 'done'` — verified before **and** after the restart.
- The recheck window is `RECHECK_TIERS_SEC = [10, 60, 300]` seconds. vpos 26 opened
  2026-08-02T05:00:19; it is **~12.8 hours old**.
- `entry_wall_baseline_mult` has exactly **one** reader, `virtual_trader.py:1202`, inside
  `_run_recheck_tier` — a function vpos 26 will never enter again.

**vpos 26 is the only open position.** So at the moment of this change, **zero** positions could
have their ratio cross-scaled. Verified at the restart boundary, which is why the restart was
timed deliberately rather than fired blind.

**🔴 Residual hazard, named rather than hidden.** A *future* restart that lands inside a
position's first **300 seconds** would leave that one position comparing a pre-fix Bybit-100
baseline against an OKX-4000 refresh — one cross-scaled ratio, for one position, for the remainder
of its recheck window. The exposure is a 5-minute window per restart and it does not apply to
anything currently open. It was **not** guarded in code: a version-stamp column plus gating logic
is more machinery than a hazard this small warrants, and stating it is the honest alternative to
pretending it is impossible. **If a restart is ever needed within 5 minutes of a fill, wait for
`recheck_status='done'` first.**

---

## 4. VENUE AUDIT — EVERY ORDER-BOOK FIGURE ON SOL

### 4.1 Producers

| producer | venue | depth | wall threshold | status |
|---|---|---|---|---|
| `liquidity_zones.fetch_pre_trade_walls` | **OKX** `books-full` | **4000/side** (`depth` renders 8000) | ×4.0 | ✅ compliant |
| `liquidity_zones.fetch_clusters` | **OKX** `books-full` | **4000/side**, $0.10 buckets, top-3 | n/a | ✅ compliant |
| `microstructure.fetch_pre_trade_walls` | **Bybit** via Tor | **100** (`PRE_TRADE_BOOK_DEPTH`) | ×4.0 | ⚰️ **now DEAD — zero callers** |
| `microstructure._analyze_orderbook` | **Bybit** via Tor | **20** (`MICROSTRUCTURE_BOOK_DEPTH`) | ×3.0 | ⚠️ live, see §4.2 |

### 4.2 Consumers

| consumer | source | venue/depth | verdict |
|---|---|---|---|
| entry advisor (`main.py:3042`) | `liquidity_zones.fetch_pre_trade_walls` | OKX-4000 | ✅ |
| entry storage `advisor_book_json` | same dict | OKX-4000 | ✅ (fixed 17:08) |
| learning loop `signal_weights:227` | `advisor_book_json` first | OKX-4000 | ✅ (fixed 17:08) |
| `skip_attribution` walls + new shape cols | the same dict passed to `on_skip` | OKX-4000 | ✅ |
| smart-exit dryrun sampler (`virtual_trader:699`) | `liquidity_zones.fetch_pre_trade_walls` | OKX-4000 | ✅ already |
| **recheck baseline + refresh** | **`_walls_okx`** | **OKX-4000** | ✅ **this change** |
| initial SL wall anchoring (`stop_loss.compute_initial_sl`) | `liquidity_zones.fetch_clusters` | OKX-4000 | ✅ |
| wall-avoidance gate (`main.py:2669`) | `liquidity_zones.fetch_clusters` | OKX-4000 | ✅ (and inert — `WALL_AVOIDANCE_ENABLED=False`) |
| fill/close-time capture → `orderbook_json`, `tape_json` | `microstructure.kick_off_capture` ×4 sites | **Bybit-20** | ⚠️ see below |

**No book use at all** in `post_exit_observatory.py`, `trail_arm.py`, `adaptive_trail.py`,
`liquidity_sweep.py` — checked, not assumed.

**After this change, no Bybit book figure feeds any decision, any ratio, or any stored analysis
input on SOL.** The one remaining Bybit reader is the fill/close-time microstructure capture, and
I did **not** convert it, for reasons I want on the record rather than buried:

- Its **book** half writes `orderbook_json`, which since the 17:08 fix is **read by nothing** —
  the learning loop now prefers `advisor_book_json`.
- Its **tape** half (`fetch_trades` → aggressor pressure, whale counts) **has no OKX equivalent in
  the current code**, and `spread` / `top_bids` / `top_asks` are venue-ladder fields that a
  bucketed OKX walls dict does not carry. Repointing it at OKX-4000 would not be a source swap; it
  would delete the tape and the ladder.
- Its arguable purpose is precisely to record *the venue we would have traded on*, at fill.

**This is a decision for you, not a silent one for me.** Under a literal reading of the standing
decision it should move; under its stated rationale ("the venues we trade on have books too
shallow to be **informative**") a snapshot that informs nothing is out of scope. It produces no
figure that any decision consumes. **Left as-is, named here, awaiting your call.**

### 4.3 Inside the freeze — named, not fixed

Two stale lines in `claude_advisor.py` name a venue and depth that have been wrong since
2026-06-03, when the advisor was rewired to OKX-4000:

| line | text | reality |
|---|---|---|
| `:287` | *"pre_trade_walls — microstructure.fetch_pre_trade_walls() dict (**depth-100**, the ONE order-book source)"* | `liquidity_zones.fetch_pre_trade_walls`, **OKX-4000** |
| `:420` | *"the ONE order-book source, identical to Titan (microstructure **depth-100** from the bot's own hands' exchange: **Bybit for SOL**…)"* | same |

**Both are comments/docstrings. Neither reaches the model** — `_format_pre_trade_walls` never
emits a venue name, so the advisor has never been told which exchange its book came from.
Under the freeze's own terms these are **labels**, which are explicitly not frozen — but they live
in the file that holds the frozen prompt, and editing it would change the mtime I have been citing
as the evidence that the freeze holds. **Correct them at window close.** Recorded here so the
next reader does not trust them; this is the fourth instance on this system of a label that does
not say what the code does.

---

## 5. VERIFICATION

| check | result |
|---|---|
| `py_compile virtual_trader.py` | ✅ OK |
| `_walls_with_okx_fallback` references remaining | ✅ **0** (one mention in the new docstring explaining the removal) |
| `microstructure` attribute on `virtual_trader` | ✅ **gone** |
| `microstructure.fetch_pre_trade_walls` live callers | ✅ **0** — dead code |
| service restarted deliberately | ✅ 17:47:5x, pid **1503515**, active |
| **vpos 26 open, SL unchanged** | ✅ 73.53 / **SL 72.59** / orig 72.59 / `done` / baseline 10.2 preserved |
| errors or tracebacks since restart | ✅ none |
| `claude_advisor.py` / `config.py` modified | ✅ **NO** — mtimes 08-01 20:54 / 08-02 13:34 |
| **200-window** | ✅ **86/200, NOT reset** |

## ROLLBACK

```bash
cd /mnt/volume_nyc1_1780480650620/mercury-sol
cp virtual_trader.py.bak_recheckokx_20260802 virtual_trader.py
systemctl restart mercury-sol
# DB rollback (only if ever needed): trades.db.bak_pre_recheckokx_20260802
```

## VERIFY

```bash
grep -n "_walls_okx\|_walls_with_okx_fallback" virtual_trader.py     # one def, two call sites
grep -rn "microstructure.fetch_pre_trade_walls" *.py                 # comments only — dead
grep -n "^import \|^from " claude_advisor.py                         # json, re, datetime, anthropic
journalctl -u mercury-sol | grep "UNMEASURED"                        # the no-signal branch, if OKX ever fails
```

_2026-08-02. Mercury-SOL is PAPER. The entry prompt is byte-identical, the 200-window stands at
86/200 and is not reset, `ADVISOR_WALL_ALIGNED_V2` is untouched. **Titan was not read and not
modified.**_
