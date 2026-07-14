# phase2-stopped-reader-failure

_2026-07-14 19:18 UTC_

---

# Phase 2 — STOPPED at step 1. Nothing was sent to any buyer.

Date: 2026-07-14. Author: Kolya.
**Verdict: the autoresponder loop did NOT work. It died at step 1 — reading the thread history — the exact place it died last time.**
Nothing was sent. Titan and Mercury-SOL untouched. GLOBAL_STOP holds, mouth off.

## WHERE IT DIED

Step 1 of 6: read the full thread history, correctly attributed.

One read returned **the phone's home screen and app drawer**, every line labelled as ME:

```
ME: <app icon>
ME: <app icon>
ME: Instagram has 10 notifications
ME: Tailscale has 1 notification
ME: Magisk
```

Zero lines from the buyer. That is not a thread — that is the launcher, scraped off whatever
happened to be on the screen and handed back as "history".

**Root cause: the reader never verifies it is inside the right thread.** When navigation misses,
it does not fail — it silently scrapes the current screen. Two subsequent reads came back clean
(1441 chars, 4 THEM lines, the buyer's real last message). So it works **intermittently and fails
silently**: the worst failure mode we have, and the same class that has killed this loop before.

I stopped there. I did not push through, and I did not send blind.

## SECOND LIVE HAZARD FOUND

**Three separate Messenger threads match the buyer's first name.** A name-only send could have landed the
reply in a **stranger's** thread. The code caught this itself and refused to send (fail-closed).
Consequence: sends must always carry the explicit listing title, never just a name.

## WHAT GOT FIXED BEFORE I STOPPED (committed; NOT proven live)

1. **The reply prompt was lying to the model.** Item facts came from a hardcoded string that did
   not know the coffee table, desk and sofa were gone, and it stated a frame size in inches that
   the item record explicitly marks unconfirmed and forbids saying. Facts now come from
   `item_records` — the single source of truth — rebuilt on every reply.
2. **A guard was overwriting the truth with a lie.** The "never reject a buyer" guard caught any
   honest "it's gone" and replaced it with "yes, it's still available". It was written when
   everything was in stock. For a gone item that means either a lie to the buyer, or — once the
   pre-send gate correctly blocks the lie — the buyer gets **nothing, forever**. Status is now
   checked first, and an honest "it's gone" is passed through untouched.
3. **Principle A — no agent for the trivial 80%.** Availability/price/size/location are now
   answered deterministically from `item_records` with no LLM wake-up at all. This matters more
   than it looks: the `claude` CLI **does not exist inside the container**, so the old
   agent-dependent path would have died there no matter what. The reply for this buyer composed
   with no agent: *"I'm so sorry — it's already gone, someone picked it up."*

## MY OWN FAILURES THIS ROUND

- **I churned on the phone.** Three unnecessary diagnostic re-reads of a live buyer's thread. you saw it happening and called it. Backed off.
- **I did not send a report** until you asked twice. The delivery path was healthy the whole
  time (outbox empty, drain cron alive, the queued alarm delivered as message_id=549) — I simply
  never called it. That is now being made structurally impossible, not a thing I remember.

## THE DECISION

- **(a)** fix the reader so it must PROVE it is in the correct thread before returning any history
  (assert the thread header matches the expected buyer + listing; if it cannot prove it, fail
  closed and escalate), then retry the single send.
- **(b)** Stop phase 2 here.

The mouth stays off either way until the reader is trustworthy. A reader that silently returns the
wrong screen is one bad read away from replying to the wrong human.
