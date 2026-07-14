# buyer-seller-reads-screen-phone-rootcause

_2026-07-14 23:31 UTC_

---

# Buyer-vs-seller now reads the screen. Watchdog fixed. Root cause of "phone dying" found.

Date: 2026-07-14 ~23:15 UTC. Author: Kolya.

---

## THE HEADLINE

The system now decides **"are we the seller or the buyer?" by reading the thread itself** — no
question to you. And the "phone keeps dying" was a misdiagnosis: **sshd never died** (4-day uptime).
The real cause was ours.

## 1. BUYER vs SELLER — reads the screen, does not ask you

Four on-screen signals, hardest first, so you're never asked what's already on your screen:

1. **Seller-side controls** ("Mark as sold / pending", "Manage listing") — Facebook shows these
   **only to the listing's owner**. Present → it's OUR listing → they're a buyer → we sell.
2. **Who spoke first** — if WE sent the first message, we found THEIR listing → we're the buyer.
3. **The listing plaque** in the header, matched against our `item_records` — ours vs foreign.
4. No seller controls + unrecognized listing → we're almost certainly the buyer.

You're asked ONLY when the screen genuinely can't resolve it — not as the default.

Unit-tested, 8/8, **zero questions-to-you** across all cases:
- **Irena (Beelink), Robert (Async e-bike), Michelle (La-Z-Boy)** → all classify as **WE'RE THE
  BUYER (procurement)** from the screen. Irena/Robert also carry your explicit ruling as a belt.
- Real buyers (Chih on the Giant, Mahsa on the coffee table, a new bike buyer) → **OUR SALE**.
- Namesakes hold: Michelle on La-Z-Boy = procurement, but Michelle on our Giant would be a sale —
  distinguished by the **listing**, never the name.

**Live test — honest status: BLOCKED by the phone.** I tried to read Irena/Robert/Michelle's actual
threads to show you the on-screen evidence. The phone flapped mid-read (Robert's navigation timed
out; Irena's thread wasn't located by search). The classifier is built and unit-tested; reading
those three specific screens has to wait until the phone is stable. I did NOT churn on it — one pass,
then I stopped.

## 2. WHY THE PHONE "KEEPS DYING" — root cause, and it was us

I investigated via adb (which worked the whole time ssh didn't — a key clue):

- **sshd has 4 days 0 hours uptime. It never died.** Termux is fully protected: whitelisted from
  battery optimization, holds a wake-lock, in the "exempted" standby bucket. Android is NOT reaping it.
- The real cause: **`su()` opened a brand-new SSH handshake on every single call.** One navigation is
  dozens of handshakes; my retry storms piled up half-open connections and hit sshd's `MaxStartups`
  limit → new connections timed out → looked like "phone dead," while the warm mux and adb kept
  working. Restarting sshd "fixed" it only by clearing the stuck connections.
- Compounded by Tailscale flipping direct↔relay on the mobile network (427ms+), and Android's
  low-memory killer reaping `uiautomator` under pressure ("Killed").

## 3. THE FIXES (committed, pushed)

- **One warm connection, not a handshake per call:** ControlMaster + ControlPersist + ServerAlive.
  The whole navigation reuses a single SSH connection. This directly removes the storm that
  exhausted sshd.
- **`recover_phone()` — auto-recovery before alarming you.** When ssh is unreachable, it uses adb
  (independent channel) to clear our stuck sshd-sessions, wake the screen, and re-establish — no
  human. **Proven working once this session:** phone was down, recover brought it back, no hand.
- **`phone_alive()` now tests capability** (real `uiautomator dump`), not a pulse (`echo`), so a
  degraded phone can't fool it into punishing buyers.

## 4. WATCHDOG false-alarms — FIXED

Marie and Anita kept triggering "buyer waiting" alarms even though they're answered. Root cause: the
watchdog counted a buyer answered **only** on a CARRIED (our send) — but Marie/Anita needed no send
(reply already in thread / we spoke last), so no CARRIED, so it nagged forever. Now "already
answered" writes a **RESOLVED** marker the watchdog honors. Verified: **the watchdog reports nobody
falsely waiting.** Marie and Anita will stop alarming.

## 5. THE TWO OWED MESSAGES

- **Chih — DONE earlier this session.** He got Radomir's number, verified in his thread (176 chars):
  "You can reach Radomir directly at <number> to set up the test ride… Pickup is in Rancho Santa
  Margarita. It's still available, $100 firm." Our live sale can now arrange directly.
- **Heather — NOT sent.** Her thread row couldn't be located this pass (phone flapping). One attempt,
  no churn. Still owed, queued behind a stable phone.

## STATE

GLOBAL_STOP holds. Titan + Mercury-SOL active, untouched. 0 root-owned files. No hand-driven scripts
running. Autoresponder is in cron, self-guarded (phone_alive + buyer/seller gate), so it can't churn
a dead phone or "sell" a procurement thread.

## WHAT I NEED / WHAT'S NEXT

1. **The phone is still unstable.** The ControlMaster fix should cut the storm dramatically going
   forward, and recover_phone auto-heals the connection — but the underlying flakiness (Tailscale
   relay + memory-killed uiautomator) may still cause intermittent drops. If it drops hard again,
   the same one-line Termux `sshd` restart clears it, but recover_phone should now handle most cases
   without you.
2. Once the phone holds: finish the live buyer/seller read on Irena/Robert/Michelle (show you the
   screen evidence), and send Heather's correction (only if her thread proves).
