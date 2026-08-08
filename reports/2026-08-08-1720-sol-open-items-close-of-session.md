# sol-open-items-close-of-session-08aug

_2026-08-08 17:20 UTC_

---

# Mercury-SOL — what is outstanding at close of session

**Nothing is half-applied. Service healthy, 0 tracebacks since 16:08:59, vpos 29 managed,
Titan untouched. Nine items are open; one of them is NEW, found while verifying this answer.**

---

## A. DEFERRED BY YOUR DECISION — restart when the book is flat

Three files are on disk but not in the running worker (started 16:08:59):

```
PENDING RESTART   config.py, trail_arm.py, virtual_trader.py   (16:51:55)
loaded            main.py, fee_rates.py (16:07:45) · optimizer.py, optimizer_listener.py (15:36:57)
```

All three are **zero-behaviour**, proven by execution. The single disk-vs-memory difference:
if an orphan adoption happened before the restart, the card would print the old formula string
while computing the same 0.0020 target. Display only.

---

## B. DECISIONS WAITING ON YOU

**1. `_BE_TARGET_FRAC_ON` → 0.0029?** Now a single explicit constant with the evidence beside it.
At 0.0020 the breakeven lock books **−0.0002%** of notional (a fee wash); 0.0029 restores
**+0.0897%**. Cost: it tightens the lock in both directions and would have turned vpos 21's
+0.285R into +0.152R (**−0.133R**), the only measurable case in 22 closed positions. The assert no
longer refuses it on a false premise.

**2. The advisor's order-book channel is dead weight — no action taken.** `P(execute)` is 3.24%
with a p80+ opposing wall vs 3.36% without: **Fisher exact p = 1.0000, n=396**. It mentions walls in
81.6% of reasons and cites the percentile in 6.6%. Prompts were out of scope this session, so
nothing was changed. The options are yours: leave it, stop rendering the book to the model, or stop
treating `ai_reason` as evidence in attribution and `consult_for_learning`.

---

## C. 🔴 NEW — FOUND WHILE VERIFYING THIS ANSWER

**3. `naked_position_alerts` has no resolution path. Nothing anywhere sets `resolved=1`.**

```
grep "UPDATE naked_position_alerts"  ->  no hits
unresolved rows: 5
  1  06:50:21  entry_fill_unreadable   <- that position was flattened at 06:50:25
  2  08:35:17  entry_fill_unreadable   <- that position was flattened at 08:35:20
  3  08:50:15  entry_fill_unreadable   <- that position is vpos 29, ADOPTED and MANAGED
  4  13:58:18  boot_orphan             <- same position, pre-adoption
  5  15:40:43  boot_orphan             <- written by the adoption itself
```

**All five describe conditions that are now resolved**, and `silence_digest_sol.py:343` reads
`resolved=0` — so the digest will keep reporting a naked position that does not exist, indefinitely,
and the count only grows. This is the "one fact, many judges" class: the venue says managed, the
ledger says managed, the alert table says naked.

It is a reporting defect, not a money defect — nothing trades off this table. Not fixed; flagging.
The fix is small (mark resolved when the side is flat or booked) but it is a new mechanism and
belongs in its own pass.

---

## D. RECORDED, DELIBERATELY NOT FIXED

**4. `apply_opt_proposal` is a second, unguarded door.** Dead behind `PARAM_TUNING_ENABLED = False`,
and Titan does not guard it either, so guarding it here would be a divergence. 🔴 **Flipping that
flag to True re-opens the hole** — it can append a filter from `worst_segment` without passing
`_live_evidence_ok`.

**5. Paper mode now refuses every optimizer proposal.** Cohort is paper by construction there, so
`live_pairs = 0` and the floor refuses. Correct while real money is on the venue; a future return to
observation mode needs the guard relaxed.

**6. Fee boundary — do not pool studies across it.** vpos ≤29 fees modelled at 0.055% (understated
1.82×); vpos ≥30 at the venue rate. **Row 29 straddles it**: venue entry fee 0.09724, partial fee
modelled. It is the only mixed row and it was left as booked.

**7. Filter #21 (opposing wall) refused, with a pre-registered test.** Realised-R split at ≥30 per
cell, Mann-Whitney, α = 0.05/12, day-blocked, kill if p80+ is not worse by ≥0.25R median. At 0.413
closures/day that is **~68 days for n=30 and ~286 days for a powered 4-cell split**.

---

## E. NOT YET PROVEN IN FLIGHT

**8. Two of the morning's three fixes have still never fired in a live entry.** The 34040 fix proved
itself in production at 16:09:18 (`resync LONG ALREADY AT 74.9496 — counting as SET`). The
**entry-fill read** and the **two-thread entry race** have not: no live entry has been taken since
they shipped. vpos 29 was *adopted*, not entered. LONG remains blocked by the position cap, so only
a SHORT can exercise them.

---

## F. SCHEDULED — WORTH WATCHING

**9. The optimizer timer fires 2026-08-09 14:00 UTC** — the first run under both new defences.
Expected: live cohort = 0 closed live positions, so it reports `insufficient LIVE data`, saves no
proposal, and the apply-guard is never reached. If it saves a proposal, something is wrong.

---

## STATE

```
mercury-sol   active  pid 3533821 / worker 3533987  since 16:08:59  NRestarts=0  0 tracebacks
              HEARTBEAT open=1 mode=LIVE, ~13s ticks against a 10s nominal (steady, Tor latency)
vpos 29       0.9 @ 74.80 · sl 74.9496 · open, managed · partial 0.4 @ 76.36 · wm 76.46
venue         LONG 0.9 · stop 74.95 · one Untriggered conditional, same orderId since 08:50
optimizer     timer active, next 2026-08-09 14:00 UTC · listener active (guard loaded)
              optimizer/ holds only dynamic_weights.json + tg_offset.txt — no proposals
titan         active · HEAD 897850b · git clean · master pid 2538048 from Aug 6 · NOT TOUCHED
```

**Nothing is half-done. Items 1, 2 and 3 are the only ones that want a decision from you; the rest
are recorded and waiting on data or on a flat book.**
