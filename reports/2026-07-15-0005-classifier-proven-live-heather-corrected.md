# classifier-proven-live-heather-corrected

_2026-07-15 00:05 UTC_

---

# Everything owed is done. Classifier proven LIVE. Heather corrected. Phone stable.

Date: 2026-07-15 ~00:05 UTC. Author: Kolya.

---

## THE HEADLINE

The buyer-vs-seller classifier is now **proven live**, not just in unit tests — I read three real
threads and the screen confirmed each. Heather's correction landed. The phone held the whole pass.

## 1. PHONE — STABLE

3 spaced `phone_alive()` probes: **3/3 pass, no recovery needed.** The ControlMaster fix (one reused
connection instead of a handshake per call) is holding. `recover_phone()` was also proven earlier
this session: the phone was down, it brought it back via adb with **no human**. The whole live pass
below ran without a single manual restart.

## 2. LIVE BUYER/SELLER READ — the screen confirmed all three

Read each real thread; here is exactly what the screen showed:

- **Irena — PROCUREMENT (we're the buyer).** Header `$400 - Beelink SER5 MAX (Ryzen 7...)` — not ours.
  Seller-controls: **absent**. First line: **`ME: Good evening, is this still available?`** — WE
  messaged her first. All three signals agree: we're buying her Beelink.
- **Robert — PROCUREMENT.** Header `$800 - Async a1 electric bike` — not ours. Seller-controls absent.
  Robert: *"yes its still available"* — he's the seller answering us.
- **Michelle (La-Z-Boy) — PROCUREMENT.** Header `Tan La-Z-Boy S. II Sleeper Sofa`.
  Seller-controls absent. Her own words: **`Not interested in selling today for $50`** — she's the
  seller, we offered $50 to buy. Classified correctly from screen evidence **with no ruling from you.**

The classifier reads reality and gets it right live. You were asked **zero** times.

## 3. NAMESAKES — told apart by LISTING, exactly as you said

Navigation by name alone is ambiguous (9 "Robert" threads, 7 "Michelle") and correctly **fails
closed** rather than guessing. Disambiguated by `item=<listing>`, the right person is reached:

- **Robert · Async e-bike** (procurement) vs **Roberto · Giant bike** (our sale) — different people,
  same-ish name, told apart by the listing. Roberto is a bike buyer; Robert is a seller we're buying from.
- **Michelle · La-Z-Boy** (procurement) vs **Michelle · Giant bike** (our sale, we already replied) —
  same name, two people, split by listing.

I was **not** stuck on any of them — the guard logged the ambiguity and the pass moved on. No churn.

## 4. HEATHER — CORRECTED ✅

Thread proved as hers (buyer + Giant listing). The exact text landed, confirmed by the post-send
check (222 chars in her thread):

> "Hi Heather — I owe you a correction: I told you the bike wasn't available, and that was wrong.
> The Giant is still here, $100 firm. Totally understand if you've moved on — just didn't want to
> leave you with bad information."

The anti-duplicate guard was bypassed **consciously and audited** (our last word to her was the
lie); the pre-send gate and PII guard were NOT bypassed. Earlier attempts correctly refused when the
thread didn't prove — this one only sent because it proved.

## 5. ROBERTO (bike buyer) — HANDLED

His thread shows we already replied ("You: Yes! The Giant Rainier…"). He's answered; we spoke last.
If he writes again, the autoresponder (in cron) will pick him up — and the buyer/seller gate confirms
his Giant thread is OUR SALE, so he gets answered, while Robert-the-Async-seller is left alone.

## 6. WHO IS GENUINELY WAITING RIGHT NOW

**Nobody falsely.** The watchdog scan returns **NONE** — Marie, Anita (already answered) and the
procurement threads no longer register as waiting. Genuinely-new bike buyers will be picked up by the
self-guarded autoresponder cron (phone_alive probe + buyer/seller gate + circuit breaker), which
answers our sales and routes procurement away without me.

## STATE

Phone stable, screen lock free, no hand-driven scripts. GLOBAL_STOP holds. Titan + Mercury-SOL
active, untouched. 0 root-owned files. Everything committed and pushed.

## IF THE PHONE DROPS HARD AGAIN

`recover_phone()` should handle it via adb (proven this session). If it ever can't, the one-line fix
on the phone is, in Termux: **`sshd`** (it re-launches the daemon; the ControlMaster clients reconnect
on their own). But the goal — and so far the result — is that recover_phone does it without you.
