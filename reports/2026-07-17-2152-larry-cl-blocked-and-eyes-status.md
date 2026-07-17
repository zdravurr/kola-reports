# larry-cl-blocked-and-eyes-status

_2026-07-17 21:52 UTC_

---

# Larry (CL bike) + eyes — honest walls, no fakes — 2026-07-17

Two things attempted. Both hit real walls; I stopped at each rather than fake it. Titan/Solana untouched, no code changed this turn.

## 1. ANSWER LARRY — reached the login, blocked by a device wall. NOT sent.
Larry wants the Giant Rainier 26" ($100, RSM) + more pics. I tried to answer as the seller and hit a wall on **every** correct-account channel:

1. **Host SMTP (465/587):** BLOCKED by the host (DigitalOcean anti-spam). IMAP:993 works, SMTP doesn't.
2. **SMTP via residential proxy (proxy-cheap):** proxy endpoint times out — it's down. Reviving it = infra side-quest (off-limits).
3. **Phone Gmail:** the phone has **only the 4r phone account (4r)**. Larry's inquiry + the CL listing are under **the 2r seller account (2r)**, which is **not on the device** (`dumpsys account` confirms one Google account). CL relay requires the reply from the listing account, so a 4r send would be wrong-identity + unprovable. Adding 2r needs its login password + 2FA (I only hold an app-password) — can't.
4. **Phone Python/openssl:** absent (Termux has neither in the su context) — can't script a TLS SMTP send from the phone.
5. **Craigslist APP (`org.craigslist.CraigslistMobile`, the intended phone_hands path):** I drove it all the way — chat tab → login → **"log in with my craigslist password"** (I have `cl_zdravurr.pass`) → entered password → submit. CL returned: **"unable to log in, please ensure you are signed in to Google P. Store."** That's a **Play-integrity / device wall** (the app ties login to the device's Play account = 4r), not a credential problem. Retrying risks lockout for no gain, so I stopped.

**Verdict:** Larry cannot be answered *from the correct seller account* this turn without a device/infra change (add 2r to the phone Gmail, restore the proxy SMTP bridge, or fix the CL app's Play integrity) — all separate side-quests you told me not to do. So I stopped and surfaced it precisely rather than send from the wrong identity or claim a send I can't prove. **Larry is still waiting; the money is real; the blocker is device-level, not detection.**

## 2. EYES — loop proven; blind-tap SITE conversions are STOP-per-your-rule
- The shared loop (`lib/eyes.py`) + `check_eyes_landed` contract were proven live and committed **last turn** (Settings, moved element).
- **This turn the eyes ran on real production apps** (not neutral demos) while pursuing Larry — journaled in `eyes_events.jsonl`:
  - CL "chat" tab → **danger_zone LAWFUL_REFUSAL** (bottom nav-bar guard fired correctly), then **ok** via the deliberate `danger_ok` nav-tap. Real-world proof the guard + escape hatch work.
  - CL "continue", "log in with password" → located by vision + verified ok.
  - Gmail "open account picker" → **verify_failed** — the eyes correctly reported the picker did NOT open (caught a real UI truth instead of pretending). This is the loop refusing to fake success.
- **The blind-tap SITE conversions are NOT done.** All four scripts (`fb_mp_giveaway.py` ×7, `zina_post_now.py` ×11, `fb_bike_listing_edit.py` ×2, `offerup_send.py` WIP) are **dormant one-offs** whose blind taps are *fallbacks* inside FB/OfferUp **posting/edit/send** flows. Proving each live means executing those **destructive** flows (real posts / editing the live bike listing / messaging a real OfferUp buyer) in FB/OfferUp **mid-Ogon-window** — exactly your named STOP condition. I did **not** bulk-convert the code without live proof (that's the half-done you reject, and a wrong goal-string silently breaks a dormant script).
- **grep: 25 hardcoded `tap(x,y)` coords remain** (unchanged — no fakes). Zero-coords requires converting+proving those 4 destructive flows one at a time when the phone is free.

## What would unblock each (separate, one-at-a-time next steps)
- **Larry:** add the 2r seller account (2r) to the phone Gmail (needs account login pw+2FA) → then reply is a 2-tap phone_hands job; OR restore the residential-proxy SMTP bridge for a server-side send.
- **Eyes 100%:** run each script's flow to its final destructive tap on a quiet phone (outside contention), converting+proving one site per pass.

## State
- No commits this turn (nothing was proven to a commit-worthy bar). Tree: prior-session WIP only (LEARNINGS ×6, offerup_send.py) — untouched by me. Titan/Solana untouched & running.
- Phone left at home; CL app login not completed; nothing posted/sent; a harmless unsent Gmail draft (under 4r) exists but will not auto-send.
