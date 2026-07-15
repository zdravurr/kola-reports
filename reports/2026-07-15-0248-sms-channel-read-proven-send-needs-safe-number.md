# sms-channel-read-proven-send-needs-safe-number

_2026-07-15 02:48 UTC_

---

# Item 3: SMS channel built, READ proven live. SEND needs one thing from you: a safe test number.

Date: 2026-07-15 ~02:55 UTC. Author: Kolya.

## THE PHONE CAN DO SMS FULLY

Confirmed on the device: **termux-sms-send is present, `service call isms` works, and
`content://sms` is readable** — receive AND send are both possible.

## WHAT'S BUILT + PROVEN

`projects/sales/sms_channel.py` mirrors the Messenger primitive
(`read_labeled_history_for_sender` / `send_to_sender_native` / `LAST_THREAD`), so the Dirigent
dispatches an SMS lead to Senya with **no change to the worker**. It reads `content://sms`
(incoming = THEM, outgoing = ME) and sends via `termux-sms-send`, through the **same client_lock**
(money-beats-warmup) and the **same review_gate** as Messenger.

- **READ — proven live.** Read a real SMS thread off the phone, formatted ME/THEM, proven=True.
- **Senya wired** to use the SMS channel for `platform=sms`.

## A CORRECTION I OWE YOU

Earlier I flagged a "949" number as a "live SMS buyer." Reading the phone's actual SMS store, that
number **is not there** — the store holds only short-code service messages (Facebook codes, etc.).
There is **no live SMS buyer**, exactly as you said. My earlier flag was wrong; I checked the device
instead of trusting the router audit. No one is waiting on SMS.

## SEND — built, wired, but I will NOT prove it unsafely

The send path is complete (termux-sms-send + gate + lock + a post-send read-back of the Sent box).
But I can't prove it without a **safe target**:
- No real buyer/seller SMS exists to reply to.
- The phone's own number isn't exposed (US Mobile SIM), so a self-SMS test isn't available.
- Texting a stranger blind to "prove send" is exactly the unsafe live action I won't take.

**What I need from you:** one safe number to text (your own, a Google V., or a second line). I'll
send one gated test SMS to it, read it back from the Sent box, and that closes the send proof. Then
I'll finish Borya-on-SMS (seller negotiation) and the SMS buyer/seller classification (SMS has no
listing plaque, so role is decided by who-texted-first + content).

## WHERE WE ARE
1. Hierarchy - done
2. Workers in the container - done
3. **SMS channel — read proven live; send built, needs your safe test number.**
4. X warmup yield + un-pause — next (can do now while you pick a number).

Titan + Mercury-SOL untouched. Container orchestrator running + watched. GLOBAL_STOP holds. 0 root
files. Everything pushed.

## YOUR CALL
Give me a safe SMS number for the send test — and I'll proceed to item 4 (X warmup) meanwhile.
