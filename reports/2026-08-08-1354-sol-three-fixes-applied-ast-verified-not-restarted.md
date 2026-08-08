# sol-three-fixes-applied-ast-verified-not-restarted

_2026-08-08 13:54 UTC_

---

# Mercury-SOL — three fixes + optional hunk APPLIED. AST verification PASSED. NOT RESTARTED.

**All four changes are on disk. `py_compile` clean. The AST comparison came back IDENTICAL —
83 of 83 statements, node for node. The service is stopped, now also `disabled`, and has NOT
been restarted. The open position is untouched. Titan was not touched at any point.**

Prior reports: [forensics 13:21](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1321-sol-live-forensics-three-entries-one-open.md)
· [approved diffs 13:40](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1340-sol-service-stopped-three-fixes-for-approval.md)

---

## 0. BOOT PROTECTION — `mask` REFUSED, `disable` USED INSTEAD

You asked for a mask. It is not available for this unit, and here is exactly why:

```
# systemctl mask mercury-sol
Failed to mask unit: File /etc/systemd/system/mercury-sol.service already exists.
```

Masking works by putting a symlink to `/dev/null` at the unit's **highest-precedence** path, which
is `/etc/systemd/system/` — and that is where the real unit file lives. systemd will not overwrite
it. A `--runtime` mask writes to `/run/systemd/system/`, which sits **below** `/etc` in the search
order, so it would be silently ineffective — the worst possible outcome: a mask that looks applied
and is not.

**What I did instead — `systemctl disable`, which fully achieves your stated intent:**

```
Removed "/etc/systemd/system/multi-user.target.wants/mercury-sol.service"
mercury-sol: inactive / disabled
```

The boot symlink is gone, so **a host reboot will NOT start it.** The residual difference from a
true mask is that a *manual* `systemctl start` would still work. Completing the mask requires moving
the unit file out of `/etc/systemd/system/`, which restructures where the service is defined — that
is beyond what "mask it" implies, so I stopped and am reporting rather than doing it. Say the word
if you want that too.

---

## 1. BACKUPS

```
main.py.bak_threefixes_20260808_134816       291268   md5 659d9b78…  ← identical to pre-edit main.py
tor_retry.py.bak_threefixes_20260808_134816   13321   md5 90964428…  ← identical to pre-edit tor_retry.py
```

md5-verified against the originals before the first edit. `cp -p`, so mtimes are preserved.

---

## 2. 🔴 (a) AST EQUIVALENCE — THE TEST YOU ASKED FOR

Parsed both files, pulled `_handle_5m_trigger` from each, stripped the added `_gate` assign, the
refusal `If`, and the `try/finally` wrapper from the NEW tree, then compared `ast.dump()` node by
node.

```
OLD _handle_5m_trigger: 83 top-level statements
NEW _handle_5m_trigger: 44 top-level statements
wrapper shape: OK  (_gate assign + refusal If + Try/finally with a single release)

OLD statements: 83   RECONSTRUCTED: 83
✅ AST IDENTICAL — all 83 statements match node-for-node.
   No statement moved, no branch changed, no return captured or lost.
```

The whole-subtree `ast.dump()` of old vs reconstructed is also byte-identical, not just the
statement list. The wrapper shape was asserted too — the `Try` has **no `except` handlers** and
**no `else`**, and its `finalbody` holds **exactly one** statement, a `_gate.release()` call. A
wrapper that had silently acquired an `except` would have been caught here.

**Why 83 → 44:** 39 of the old top-level statements moved *inside* the `try`, so they are no longer
top-level. That is the reindent, and the reconstruction proves it is only that.

### 🔴 (c) EVERY RETURN, AND BOTH EXCEPTION PATHS

```
Returns — OLD total 17 | NEW: prologue 6 + gate-refusal 1 + inside try 11 = 18
✅ every return that was in the span is still in the span, inside the try.

Inside try: EntryFailSafeError handler=True   generic Exception handler=True
✅ finally therefore releases on both the fail-safe and generic-error paths.
```

17 → 18 is the one **added** return: the gate refusal. The 11 returns that were inside the span are
all still inside the `try`, so `finally` fires on every one of them. Both entry exception handlers —
`EntryFailSafeError` and the generic `Exception` — are inside the `try`, so the lock is released on
the SL-fail-safe path and the order-error path as well as on success.

### (b) `diff -w` — THE SECOND, WEAKER CHECK

```
main.py:  diff -w → 160 added lines, 1 removed line
The ONLY removed line:
<     'options': {'defaultType': 'future'},
```

**One removed line across a 535-line reindent** — and it is the Fix #1 line being replaced. For
contrast, the whitespace-*sensitive* diff shows 670 added / 511 removed; all of that delta is the
reindent, and `diff -w` shows it collapsing to nothing.

```
tor_retry.py: diff -w → the single options line replaced, nothing else
```

### `py_compile`

```
PY_COMPILE: OK (both files)
```

### UNIT TESTS OF THE NEW LOGIC (helpers extracted by AST — `main.py` never imported, since
importing it has boot-time side effects and the service is deliberately down)

`_stop_already_at_price` — 10/10:

```
[ok] True   TODAY'S ACTUAL 06:50 payload   {"retCode":34040,…,"time":1786171821803}
[ok] True   TODAY'S ACTUAL 08:35 payload   {"retCode":34040,…,"time":1786178117087}
[ok] True   resp dict, int retCode 34040
[ok] True   resp dict, str retCode "34040"
[ok] False  resp dict, retCode "0"
[ok] False  110043 "leverage not modified" must NOT match
[ok] False  10002 unrelated error
[ok] False  🔴 34040 INSIDE THE TIMESTAMP  {"retCode":0,…,"time":1786171834040}
[ok] False  🔴 34040 inside timestamp again, quoted retCode
[ok] False  Tor RequestTimeout — must stay a FAILURE
```

Your instinct on the substring was right and the test proves it: a naive `'34040' in str(e)` returns
**True** on `"time":1786171834040` and would have silently converted a real Tor timeout into
"the stop is fine". The parsed-retCode match rejects it.

`_entry_gate` — all pass:

```
same side returns the SAME lock object: True
other side returns a DIFFERENT lock:    True
thread A acquire(blocking=False): True
thread B acquire(blocking=False): False   <- REFUSED IMMEDIATELY, not queued
thread B did not block (joined):  True
SHORT side unaffected while LONG held: True
after release, re-acquire works: True
```

Thread B returns `False` and **exits without blocking** — refused, not queued, which was the
requirement. And a held LONG gate does not block SHORT.

### STRUCTURAL CONFIRMATION, READ BACK FROM THE PARSED TREE

```
FIX#1 main.py  exchange options -> {'defaultType': 'future', 'fetchOrder': {'acknowledged': True}}
FIX#1 tor_retry iso_exchange    -> {'defaultType': 'future', 'fetchOrder': {'acknowledged': True}}
FIX#2 _move_stop_to guards: total=2  in try-body=1  in except=1
OPTIONAL _fetch_position_state at 2395; create_market_order at 2403; re-read BEFORE order = True
FIX#3 _entry_gate defined at module level: True
```

Both clients carry the option — the `iso_exchange` half-fix you flagged is closed. Fix #2 sits in
**both** the `resp` check and the `except` branch, one each, as designed.

---

## 3. WHAT WENT IN

| fix | where | what |
|---|---|---|
| #1 | `main.py` `exchange`, `tor_retry.py` `iso_exchange` | `'fetchOrder': {'acknowledged': True}` as an exchange OPTION on **both** clients. Fixes all four `fetch_order` call sites, three of which were failing silently inside `except: pass`. Refusal branch untouched. |
| #2 | `main.py` `_stop_already_at_price` + `_move_stop_to` | 34040 "not modified" → `True`, with its own distinct log line (`ALREADY AT … no change was needed`) so "set" and "already set" stay distinguishable. Matched on parsed retCode. In both branches. |
| #3 | `main.py` `_entry_gate` + `_handle_5m_trigger` | Per-side `threading.Lock`, `acquire(blocking=False)` **before** `_risk_check`, released in `finally` after booking. Loser recorded as `status='entry_gate_refused'` on its row, in skip-attribution, in the journal, and in Telegram. |
| opt | `main.py` `_execute_single_entry` | Venue cap re-read inside the gate, immediately before `create_market_order`; fail-closed on anything that is not `POS_FLAT`. |

---

## 4. STATE RIGHT NOW

```
mercury-sol: inactive / disabled       ← NOT restarted, will NOT start at boot
titan:       active   / enabled        ← untouched; /root/titan-bot mtimes unchanged

Venue, re-read after all edits:
  positionIdx 1  size 1.3  avgPrice 74.80  stopLoss 73.89  openTime 1786179014459 (unchanged)
  conditional:   Untriggered  triggerPrice 73.89  qty 1.3
  positionIdx 2  size 0
```

**The open position is exactly as it was.** No line applied in this pass adopts, closes, moves or
books it. Every venue call I made this session was a read.

---

## 5. WHAT I DID NOT DO, AND WHAT IS LEFT

- **Did not restart.** Awaiting your go-ahead, as instructed.
- **Did not complete the mask** — blocked by the unit file's location, see §0. `disable` covers the
  reboot case; a manual start is still possible.
- **Did not touch the open position.**
- **Did not touch Titan.**
- `mercury-sol-optimizer-listener.service` is still **active and enabled**. It is a separate unit —
  the optimizer's Telegram callback listener. It does not place orders, but it can write settings
  and filters. It was outside the scope of "stop the service"; flagging it rather than acting.
- **Not yet proven:** that the fixed fill read works *in the live entry path*. It is proven against
  three real order ids read back by hand, and the option is proven to reach `fetch_order` with the
  call site unchanged — but the first live entry after restart is the only thing that closes it, and
  that is a [«ЗАКРЫТО» = ЖИВЬЁМ ДОКАЗАНО] item, not a done one.
