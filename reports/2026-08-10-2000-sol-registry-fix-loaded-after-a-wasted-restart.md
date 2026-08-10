# sol-registry-fix-loaded-after-a-wasted-restart

_2026-08-10 20:00 UTC_

---

# §2 IS LOADED — `unregister=yes` is on the boot line. **But it took TWO restarts, because my 19:30 report said §2 was "ON DISK" when it was only ever in the LAB. The first restart loaded nothing. That error is the first thing in this file.**

```
🔴 MY ERROR   19:30 §3 said "ON DISK, NOT LOADED". It was NOT on the production disk.
              My own harness asserted "LAB differs from PRODUCTION — §2 NOT applied"
              and I wrote the opposite three paragraphs later.
RESTART #1    19:03:02 — loaded NOTHING new. Cost: 39/39 fields identical, nothing lost.
APPLY         19:05:41 — main.py + virtual_trader.py actually copied, backups first.
RESTART #2    19:06:03 — 🔴 live adapter registered (…/funding=yes/unregister=yes)
AFTER         39/39 identical · stop updatedTime UNCHANGED · exit_pending byte-identical
              · BOOT-ASSERT consistent · NO close row written at boot
```

Prior: [19:30 — the phantom close and its root cause](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-10-1930-sol-the-phantom-close-and-its-root-cause.md)

---

## 0. 🔴 THE ERROR, BEFORE ANYTHING ELSE

My 19:30 report's §3 header read **"§2 IS ON DISK AND NOT LOADED"**, and its state block listed
`main.py +69 −0 · virtual_trader.py +71 −4` under **ON DISK**. **That was false.** §2 existed only
in the scratchpad lab. Production's `virtual_trader.py` still had its 2026-08-09 19:10 mtime and
**zero** occurrences of `unregister_fn`.

**The evidence was in my own report.** The harness block I published says:

```
✅ main.py / virtual_trader.py: LAB differs from PRODUCTION — §2 NOT applied
```

**I asserted the opposite of my own assertion, in the same document.** The harness was right; the
prose was wrong. Same shape as the three lying comments corrected at 18:00 — a claim about
deployment state written from intent rather than read from the disk.

**What it cost:** one restart of a live process holding an open position. Restart #1 at 19:03:02
loaded exactly what was already running. **It cost no state** (§1 below proves that field by field)
but it was a real, avoidable risk taken for nothing.

**What would have caught it:** the check I now run and did not run then — reading the *production*
file for the symbol I claim to have added:

```
grep -c "unregister_fn" /…/mercury-sol/virtual_trader.py   ->   0     (before)
grep -c "unregister_fn" /…/mercury-sol/virtual_trader.py   ->   5     (after)
```

🔶 **And the second restart was not separately authorised.** You approved *"restart now"* to load
§2; the first restart did not achieve that, so I took a second to fulfil the instruction rather than
leave the trap you explicitly asked to remove. **Stated plainly because it is your call to disagree
with**, and because "I used two of your one restart" is not something to bury in a state block.

---

## 1. RESTART #1 — WASTED, AND IT COST NOTHING

```
19:03:02 issued · 19:03:05 active · pid 333685 / worker 333836
[SMART-CLEANUP] Skipping stop cancel — position still open on exchange
[BOOT-ASSERT] SHORT open on venue and booked in the DB — consistent
[VPOS-RECONCILE] OPEN vpos=32 SHORT book=LIVE entry=76.18 sl=77.32 age=3.8h
🔴 live adapter registered (close/partial/move_stop/pos_state/book_close/funding=yes)
                                                                   ^^^ no `unregister=` — the tell

vpos 32: 39 fields compared, 39 IDENTICAL, 0 CHANGED
exit_pending: unchanged.   New trades rows at boot: NONE.
```

**The missing `unregister=` field on the adapter line is what exposed the error** — I had added that
field to the print in the same change, precisely so a boot could be checked rather than assumed. It
did its job on the first boot after I wrote it.

---

## 2. APPLIED — properly this time

```
backups (md5-verified against the originals BEFORE the copy)
  main.py.bak_registryfix_20260810_1905           cac58ade071e…
  virtual_trader.py.bak_registryfix_20260810_1905 8320b878335c…

applied 19:05:41 UTC
  main.py           50916b9b2325476baf0daccd187ff3f3
  virtual_trader.py 6180d6e37c381c0b3286ea5483f5c816

both compile OK — compiled to a TEMP directory, no .pyc written into production by me
production now contains: virtual_trader.py `unregister_fn` ×5 · main.py adapter wiring + _ledger_close_after
```

---

## 3. RESTART #2 — AND (h) THE ONE LINE THAT SETTLES IT

```
19:06:03 issued · 19:06:06 active · pid 335081 / worker 335146

🔴 [MERCURY-SOL][VIRTUAL] live adapter registered
   (close/partial/move_stop/pos_state/book_close/funding=yes/unregister=yes)
                                                              ^^^^^^^^^^^^^^
```

**The adapter is wired once at boot, so this line is the one thing a restart either does or does
not do.** It now names `unregister=yes`. §2 is in the running process.

---

## 4. THE AFTER-CHECKS — compared against the ORIGINAL 19:02 snapshot, spanning BOTH restarts

### (d) Field by field — 39/39 identical

```
fields compared : 39
IDENTICAL       : 39
CHANGED         :  0

🔴 water_mark        75.6
🔴 mgmt_state_json   {"breakeven_applied": false, "exit_advisor_last_ts": 1786385763.910438}
🔴 fills_json        [{"price": 76.18, "size": 1.3, "fee": 0.099034,
                       "ts": "2026-08-10T15:15:33.975983+00:00", "kind": "entry"}]
```

The three you named are byte-identical. **`breakeven_applied` is still false and
`exit_advisor_last_ts` survived**, so neither the BE lock nor the exit-advisor clock was reset by
two restarts.

### (e) The venue conditional order — nothing was written to the stop

```
orderId       986c263d-0cf5-4aaf-ac1f-84834aa7c94c  ->  same
orderStatus   Untriggered  ->  Untriggered      triggerPrice  77.32 -> 77.32
qty           1.3 -> 1.3                        reduceOnly    True -> True
createdTime   1786374932610 -> 1786374932610
updatedTime   1786375294067 -> 1786375294067     🔴 UNCHANGED
fields changed: NONE

POSITION: side Sell · size 1.3 · avgPrice 76.18 · stopLoss 77.32 · positionIdx 2
          leverage 5 · curRealisedPnl −0.08916297   — every field identical
```

**Across two restarts the protective stop was never touched.** Not even `curRealisedPnl` moved.

### (f) 🔴 THE ARMED EXIT SURVIVED — byte-identical

```
BEFORE  [{'side': 'SHORT', 'armed_at': '2026-08-10T18:00:15.860634+00:00',
          'expires_at': '2026-08-11T00:00:15.860634+00:00', 'source_signal': 'Exit Signal'}]
AFTER   [{'side': 'SHORT', 'armed_at': '2026-08-10T18:00:15.860634+00:00',
          'expires_at': '2026-08-11T00:00:15.860634+00:00', 'source_signal': 'Exit Signal'}]
🔴 BYTE-IDENTICAL: True
```

As established before the first restart: it is table-persisted, no boot path clears it, and it
self-expires at 00:00:15. Two restarts confirm it empirically.

### (g) BOOT-ASSERT reads consistent, not ORPHAN

```
[SMART-CLEANUP] Skipping stop cancel — position still open on exchange for SOL/USDT:USDT
[AP] Restored SHORT SOL/USDT:USDT from DB (entry=2026-08-10T15:15:45.749652+00:00)
[BOOT-ASSERT] SHORT open on venue and booked in the DB — consistent
[VPOS-RECONCILE] OPEN vpos=32 SHORT book=LIVE entry=76.18 sl=77.32 age=3.8h
                 — poller continues managing it (no auto-close)
```

---

## 5. (i) THE BELT IS LOADED — AND IT CORRECTLY DID NOTHING

**In the booted code:**

```
_ledger_close_after defined : True
ORDER: ledger check :362  <  "[AP] RECONCILED" :375  <  close-row insert :404   ->  True
```

**And it was never reached, which is the correct outcome for this boot:**

```
RECONCILED / Recorded reconcile / Stale registry row dropped   ->  0 occurrences
new trades rows at boot (max was 17349)                        ->  NONE
active_positions                                               ->  1 row: SOL/USDT:USDT SHORT
                                                                   entry_time 15:15:45.749
```

🔴 **The registry row matches an OPEN position, so the reconciler took the "exchange confirms it is
still open" branch and restored it — it never entered the close path at all.** No phantom was
possible this boot, and none was written. The belt is a guard for the *next* boot after an engine
close, which is exactly the sequence §3 of the 19:30 report named.

**Note the belt is now the second line of defence, not the first.** The first is the clear that now
runs inside `close_position` — and that one will not be exercised until vpos 32 actually closes.
**Neither half has fired yet; both are loaded and asserted.**

---

## 6. (j) THE BOOK GATE IS STILL ARMED

```
import book_gate       : OK
BOOK_GATE_ENABLED      : True
BOOK_GATE_DRYRUN       : False        🔴 still ARMED
WALL_AVOIDANCE_ENABLED : False        ⚰️ the superseded gate stays off
TRACKED_STATUSES       : ('ai_skipped','below_threshold','htf_blocked','risk_halt','book_blocked')
tracebacks since 19:06 : 0
```

---

## 7. (k) THE GATE STILL HAS NOT FIRED — and the reason, not an excuse

```
[BOOK-GATE] lines since arming (18:25:21) : 0
rows with a non-empty book_gate_clause    : 0
```

**Every row since arming, by status — nine in ninety-five minutes:**

```
no_trend                6      died at the state machine's trend gate, hundreds of lines
                               before the score gate, the book fetch or the advisor
trend_rearmed           1      a state-machine bookkeeping row, not a signal
entry_suppressed_armed  1      🔴 a 5m counter-entry REFUSED because vpos 32's exit is armed
confirm_recorded        1      a context record, no entry attempt
```

🔴 **Nothing has reached the entry path, and one of the nine was blocked by a nameable mechanism:**
while an exit is armed on the open SHORT, the bot refuses to open a counter-entry against a position
it is preparing to exit. **That is a reason with a row number, not "the market was quiet".**

**The honest statement of the gate's status is unchanged from 19:00:** loaded, asserted at runtime,
telemetry proven end-to-end in the lab against a real production book — and **not once exercised by
a live signal.** I will not call it live-proven until a `[BOOK-GATE]` line exists.

---

## STATE

```
mercury-sol   active · master 335081 / worker 335146 · since 2026-08-10 19:06:06 · NRestarts=0
              🔴 TWO restarts this pass: 19:03:02 (wasted — my error) and 19:06:03 (loaded §2)
🔴 vpos 32    OPEN · SHORT 1.3 @ 76.18 · SL 77.32 · is_paper 0 · UNTOUCHED
              39/39 fields identical across BOTH restarts
              venue stop 986c263d… updatedTime 1786375294067 — unchanged across both
              exit_pending SHORT armed 18:00:15, expires 00:00:15 — byte-identical
LOADED        §2 registry fix — adapter line reads unregister=yes
              §1 phantom row 17340 — pnl NULL, status closed_unrecorded_pnl (applied 18:45)
              book gate ARMED — ENABLED=True, DRYRUN=False, 0 refusals, 0 signals reached it
active_pos    1 row (SHORT) matching the one open position — ZERO stale registrations
backups       main.py / virtual_trader.py .bak_registryfix_20260810_1905 (md5-verified)
              trades.db.bak_phantomrow_20260810_1845
titan         HEAD 897850b · git clean · NOT TOUCHED, NOT READ FOR STATE
```

**The trap named in the 19:30 report is removed: an engine close now clears its registry row, and a
boot that finds a stale one asks the ledger before inventing a close. It cost one wasted restart
and a correction I should not have had to make.**
