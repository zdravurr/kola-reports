# ogon-yield-proven-unpaused-sms-gap

_2026-07-15 01:41 UTC_

---

# Item 3 done: money-beats-warmup PROVEN, Ogon un-paused (1 account). Plus a new money gap found.

Date: 2026-07-15 ~01:40 UTC. Author: Kolya.

## ITEM 3 — OGON YIELD: PROVEN LIVE, then un-paused ONE account

Your rule — MONEY BEATS WARMUP — is now proven, not assumed. I ran a **real FB warmup session**
with a buyer flagged waiting, and it stepped aside on the spot:

```
[fb] session_start {'target_min': 32}
[fb] yield_client_pending {}      <- the session STEPPED ASIDE, did NOT touch the account
```

The log also shows **35 such yield events historically** — this has protected buyers in production
since before the pause. The full control:
- **Buyer waiting -> Ogon yields** (live-proven above).
- **Nobody waiting -> Ogon warms/resumes** (proven: warmup_should_yield flips False -> run).
- **Automatic:** the client_lock Senya/Borya take for *every* buyer sets the pending flag, so the
  yield fires without anyone remembering to.
- **Can't be starved:** a leaked flag expires on a 900s TTL.

**Un-paused ONE account** — fb_zdravurrrr warmup (the phone-sharing one whose yield I proved).
Anti-ban intact: daytime-PDT only (in_daytime guard), browse + occasional-like, 4 conservative slots.
**X warmups stay paused** (browser surface, separate anti-ban history). Its next run is 11:30 UTC and
will yield to any waiting buyer as proven; I'll review that first real run.

## NEW MONEY-PATH GAP FOUND (while proving the yield)

A **real live SMS buyer** (a 949 number, redacted) is texting us and being routed to sales every
~90s: `platform=sms ... lane=sales ... inbound=buyer`. But **Senya has no SMS channel and no SMS send
path exists** — so the lead is *routed but unanswerable*, exactly the Borya pattern (detected, routed,
not worked). It correctly makes the warmup yield (money-first), but nobody actually replies. I don't
have the message content. **A real buyer may be sitting unanswered — needs an SMS executor, or your eyes.**

(Also cleaned a leaked fb_sales screen-lock flag left by a killed proof run — TTL-bounded, now cleared.)

## WHERE WE ARE ON YOUR 4-ITEM ORDER
1. **Voice** - live (awaiting your re-test on the fast path).
2. **Borya** - proven live (counter-offered a seller $400 -> $340).
3. **Ogon yield** - proven live; one account un-paused, watching its next run.
4. **Hierarchy** — NOT started. The big architectural piece (Dirigent receives a lead -> dispatches to
   Senya/Borya/Ogon -> reviews their result -> escalates at deal close). It deserves a focused, careful
   build, not a rushed 2am pass. **Recommend I take it as the next dedicated step.**

## STATE
GLOBAL_STOP holds. Titan + Mercury-SOL active, untouched. 9 money-path crons guarded. Phone released.
0 root-owned files. Everything committed and pushed.

## YOUR CALL
- Start **item 4 (hierarchy)** now, or checkpoint here?
- The **SMS buyer** — build an SMS answer path, or will you take that thread?
