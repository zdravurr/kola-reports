# borya-procurement-proven-live

_2026-07-15 01:28 UTC_

---

# Item 2 done: BORYA works live. He negotiated a real seller down, with Senya's discipline.

Date: 2026-07-15 ~01:28 UTC. Author: Kolya.

## BORYA (procurement) — PROVEN LIVE ✅

The threads where WE'RE the buyer no longer just sit there. Borya works them. Proven end-to-end on
a real thread — **Irena · Beelink SER5 MAX**:

> ME: Good evening, is this still available?
> THEM (Irena): Yeah it is, are you interested?
> **ME: Hi! Thanks — would you take $340 for it? I can do a quick, easy pickup...**

- Thread **proven** (seller + listing) before a word was typed.
- Price **read from the listing** ($400), **not guessed**.
- Pushed **down to $340** (−15%, rounded), a polite counteroffer.
- Gate passed → sent → **post-send check confirmed the exact text landed** (93 chars).
- Escalated to you: *"waiting for the seller — commit only on your word."* **Borya never buys.**

Same discipline as Senya: thread-proof, facts-not-guessed, post-send verification, circuit breaker,
phone_alive, namesake-by-listing. And a hard rule: a counteroffer is fine (that's haggling), but
"deal / come pick up / payment", or a seller price *after* our offer, → **STOP, your decision.**

## FOUR REAL BUGS building Borya exposed (all fixed, all committed)

1. **Chih — our live bike SALE — was misrouted to procurement.** His Giant thread showed our reply
   first in the visible window, so "we-spoke-first" fired *before* the listing check. Our own
   distinctive listing must win over reply order. Fixed; Chih is a sale again. (Borya would have tried
   to negotiate DOWN on our own sale — caught before it could.)
2. **Borya over-escalated on a held price.** Robert's "still at $800" is him holding his *listed*
   price — the moment to counter, not to call you. Now it only escalates on a seller price that comes
   *after* our offer (a real counter), or on commit language.
3. **history_read gate** needed a CRM touch (same stone that caught Senya). Added.
4. **The sales gate blocked procurement offers.** "$340" was read as an unverifiable *fact about our
   item* — but it's a procurement *offer* about someone else's item, with nothing in our records to
   check. Threaded a `procurement` flag so the gate skips the sales-only fact-checks while keeping
   proof/lock/history and the PII/address strip.

And a live guard win: on Robert's Async, the send's fresh nav showed **"No longer available"** — the
item was gone, and Borya **refused to offer** for it. Fail-closed, exactly right.

## WHERE WE ARE ON YOUR 4-ITEM ORDER
1. **Voice** ✅ — working; awaiting your re-test on the fast path.
2. **Borya** ✅ — proven live (this).
3. **Ogon** — next: prove money-beats-warmup yield, then un-pause one account.
4. **Hierarchy** — after: Dirigent routes + reviews, workers stop self-triggering.

Titan + Mercury-SOL untouched. Phone released, 0 root files. Everything committed and pushed.
