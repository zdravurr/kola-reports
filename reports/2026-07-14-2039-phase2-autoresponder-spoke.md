# phase2-autoresponder-spoke

_2026-07-14 20:39 UTC_

---

# Phase 2 — the autoresponder SPOKE. Two buyers answered, one refused on purpose.

Date: 2026-07-14 ~20:40 UTC. Author: Kolya.

**For the first time, the bot answered a real buyer by itself, with no human hands and no LLM.
Two replies landed, both verified by reading the thread back. A third buyer got nothing — because
the reader could not honestly read her thread, and the loop stayed silent instead of guessing.
That silence is the fix working, not the fix failing.**

Titan and Solana untouched. GLOBAL_STOP holds. Everything committed and pushed.

---

## 1. WHAT WENT OUT (the whole point)

**Mahsa** — coffee table, gone. Thread proven (buyer + listing), history 1578 chars, reply composed
from `item_records` with **no agent at all**, gate passed with a real proof shot, sent, read back:

> `[3:09 PM] ME: Hi! I'm so sorry — it's already gone, someone picked it up.`

**Chih** — the Giant bike, $100, the ONLY item actually for sale. He had asked to come test-ride it.
Thread proven, sent, read back:

> `[3:25 PM] ME: Sounds good — it's still available. What day/time works for you? I'll get the exact
> spot in the OC confirmed with the owner once we pick a time.`

Both post-send checks confirmed **the exact intended text** sits in the thread (121 and 144 chars).
CRM updated. Facts came only from `item_records` — price $100 firm, "the OC area" (the record sets
`pickup_disclose: False`, so the exact city was NOT disclosed and the owner's number was NOT sent).

**The namesake guard fired live on both.** There are THREE "Mahsa" threads and THREE "Chih" threads.
A name-only send would have dropped our reply into a stranger's chat. The code refused, and only
proceeded once the listing proved the thread. That guard is now the difference between selling a
bike and messaging the wrong human.

---

## 2. WHAT I REFUSED TO SEND — AND WHY THAT IS THE GOOD NEWS

**Heather** — bike buyer. NOT answered.

Her thread proved fine. But her history came back as **the inbox thread-list**, every row labelled
as if WE had said it:

```
ME: Heather · Giant Mountain Bike…      ME: Dulce · Giant Mountain Bike…
ME: Michelle · Giant Mountain Bike…     ME: Raghavender · …
```

Those are OTHER BUYERS' rows, not her messages. Her thread is short, the scroll-to-oldest overshot,
Messenger threw us out to the inbox list, and the collector scraped the list as "history".

The loop found zero buyer lines → **refused to answer**. It did not guess. That is exactly the
behaviour we built.

**But it exposed something worse.** With the reader hardened, her real thread reads:

```
ME: Yes, are you interested?
ME: In talks. I'll let you know.
ME: Sorry, it's not available.
```

**We told Heather the bike is NOT available. That is FALSE** — a leftover from the fabricated-"sold"
episode. The bike is for sale at $100, and she is a live buyer who was turned away with a lie.

I still cannot read her side of the conversation: her messages sit above ours, and scrolling up is
precisely what ejects us from her short thread. So I stopped, as ordered. **She is owed a correction,
and it needs your word on what we say.**

---

## 3. THREE HOLES CLOSED (committed, pushed, proven)

**(a) The thread must prove it IS the right thread.** The header carries both parties —
`Mahsa · FREE Solid Wood Coffee Table…` plus the Marketplace listing plaque — so it can prove buyer
AND listing. Cannot prove → return None, never a scrape. All routes now funnel through one
chokepoint (the sweep route used to return raw xml, bypassing every check).
Proven: rejects the launcher, rejects right-buyer/wrong-listing, rejects wrong-buyer, accepts the real thread.

**(b) Proven on entry ≠ proven throughout.** (a) alone would NOT have caught Heather. The reader now
stops the instant the compose box vanishes and re-asserts AFTER the scroll; if we drifted, the
history is thrown away and the caller gets nothing.

**(c) We do not talk over a buyer who is not waiting.** If the last speaker in the thread is us, the
buyer is not waiting — stay quiet. (Mahsa had already said "That's ok" and still got a reply. No harm
there; in a haggle it would look bad.)

---

## 4. 🔴 THE SWEEP WAS DELETING THE PAYING BUYERS

At 20:01 the sweep read a **thread screen instead of the inbox list** (`тредов=1` of ~30). Its ledger
pruning rule was "not in this tick's waiting list → delete", logged as *"answered"*. A zero-row read
was guarded. A **partial** read was not.

It silently deleted **Heather and Chih (the $100 bike), Marie and Anita.** Nobody had answered any of
them. One bad screen read, and the only paying buyers vanish from the queue with no alarm — the exact
silent-money-path class we keep hunting.

Fixed: a thread is pruned only if we actually SAW it this tick and it stopped waiting. Unseen ≠
answered — absence from a screen read is ignorance, not an answer. Ledger restored.

---

## 5. ONE MORE THING TO FIX (it bit me twice tonight)

The PII scanner **blocks its own reports**: it flags listing text as a person's name — "Giant
Mountain", "Disc Brakes", "Coffee Table" all read as FIRSTNAME+LASTNAME. Two alarms tonight went out
carrying the loud "ССЫЛКА НЕ СОЗДАНА" banner instead of a link. It failed LOUDLY, which is the design
working — but it means cron/watchdog reports currently cannot publish. This is on the list with the
botuser push hole.

---

## 6. STATE

- Phone: home screen, keyguard released, Gboard restored, no half-typed text, screen lock free.
- GLOBAL_STOP: holding. Titan + Mercury-SOL: active, untouched. Root-owned files: 0.
- Everything committed and pushed to the backup remote (0 unpushed).

## 7. WHAT I NEED FROM YOU

1. **Heather** — we told her the bike is unavailable, which is a lie. Do I send a correction
   ("it IS available, $100 — sorry for the mix-up"), and in what words?
2. **Mouth** — leave it off, or let the loop answer new bike buyers as they arrive?
3. Next in queue: the botuser push hole + the PII scanner false-positives.

Nothing else was sent. Nothing else is queued.
