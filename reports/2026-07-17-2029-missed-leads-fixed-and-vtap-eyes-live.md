# missed-leads-fixed-and-vtap-eyes-live

_2026-07-17 20:29 UTC_

---

# Missed money leads fixed + universal vtap-eyes proven live — 2026-07-17

## 0. Context reloaded — confirmed
- Governance done (de-root real, commit-gate live). Ogon = one window 06–22 ET + one gate (all lanes).
- Detection: OfferUp+CL email-primary (`mail_watch`); FB push = SOLE detector (`inbox_watcher`), patrol removed.
- Supervision-with-teeth live (`d3e3824`): checks by real fact, rework via guard-safe channel, standing rule "every capability gets a fact-based check in the same commit".
- **Correction:** enforcer base was **3** contracts (not 4); a prior session had left `check_eyes_landed` + `lib/eyes.py` written but **uncommitted and never run**.
- Titan / Solana never touched.

## 1. Missed money leads — diagnosed by evidence

### A) Irena / Beelink SER5 MAX "$350" — NOT a detection miss. FIXED + proven.
- Push **DID** see it: `watcher.log 16:05:23Z [fb_sales] LEAD→main (detection-only): Irena I.: I can do $350` (12:02 on-phone clock; log UTC).
- Root cause: thread was **parked** (`fb_messenger:Irena`, `unpark_on:new_inbound`, Boss-parked 16.07). The **only** code that unparked-on-new-inbound was `fb_inbox_sweep.py:514` — **the removed patrol**. `dirigent.py:273` skips parked threads forever, so the push detected but nothing woke it.
- Fix (`263768b`): moved unpark-on-new-inbound into the push path (`inbox_watcher.handle_event`, fb_sales, live DM). Muted threads unaffected (early return).
- Proven live: the real detected string "Irena I." removed exactly `fb_messenger:Irena`; the other 5 parks intact. Daemon restarted on new code. Irena now has open commits → Dirigent → Borya escalates the $350 (it's an "i can do" commit-trigger → escalates to Boss, no auto-negotiation — matches scope).

### B) Robert / Async a1 e-bike — banner ate nothing.
- "No sorry" captured 16:53:04Z → correctly MUTED (declined). "You can now rate each other" banner came AFTER at 16:53:31Z. Thread correctly closed. No lost message.

### C) Craigslist bike emails — mail_watch SAW & routed; died at the ANSWER step.
- Mailbox truth (live IMAP): only one real buyer email — **Larry, "Giant Rainier 26in Mountain Bike", 2026-07-16 17:40Z**. Plus a contentless "new craigslist chat message" from do-not-reply (a duplicate of Larry's relay; mail_watch is blind to that FROM, but it carries no independent lead).
- `mail_watch.log 17:45:10Z HIT [Craigslist-лид] Larry … → ROUTED main→Senya ok=True`. Detection + routing WORKED.
- It died downstream: main woke with **0 live agents** → orphaned (`agent_capacity_cron.log`) → commit_watchdog re-woke twice (rc=1) → escalated to Boss → **never answered**. Commit `lead-craigslist-larry` still OPEN.

### D) Honest reliability verdict — not reassuring.
- Detection itself is reliable (both channels proven catching today: Irena via push, Larry via email).
- The misses were **not** detection: (1) unpark logic died with the patrol [now fixed]; (2) the **answer path** — a perfectly detected+routed lead still dies if no live agent materializes (Larry).
- FB push stays **lossy by design** (banner overwrite; Raghavender precedent) with no buffer-of-truth now.
- Recommendation: no full patrol needed, but we DO need (a) the cheap `--peek` unread safety already written but not enabled (≤12 sweeps/day) to cover the banner-overwrite hole, and (b) a fix for answer-orphaning (a detected lead with an open commit and zero live agents must get a guaranteed worker run, not just re-wake+escalate).

## 2. Universal vtap-eyes — map, unified loop, live proof, supervision contract

### Hardcoded blind-tap map
- `scripts/fb_mp_giveaway.py`: 7 fixed taps (540,2350),(1030,250)×3,(540,600),(540,500),(1030,200)
- `scripts/zina_post_now.py`: 11 fixed taps (photo-grid + Next/Post)
- `scripts/fb_bike_listing_edit.py`: (540,2350),(540,1200)
- Follow `1871,938` — already handled in `x_follow.py` via danger_zone (landscape guard).
- `projects/sales/offerup_send.py` — prior-session conversion in progress (uncommitted, unproven — left as WIP).

### Unified loop (`lib/eyes.py`) — proven live (`8a5552a`)
- One loop for any worker: goal in words → `uidump`/OCR finds the box (exact box, not LLM pixel-guess, not fixed pixel) → human-random point inside the element (anti-ban) → verify by FACT → journal. Guards (emergency stop / portrait / wrong-screen) → LAWFUL_REFUSAL.
- **Live proof (neutral app, Settings):**
  - MOVED element "Network & internet": box A y=678 → after scroll box B y=440 (moved 238px). Eyes found it at the NEW spot and tapped a random human point (444,457), verified by fact (entered Network screen). ✅
  - Second target "Notifications": found [221,1077], tapped (394,1100), verified. ✅
  - Both journaled to `eyes_events.jsonl`.

### Supervision contract (same commit)
- `check_eyes_landed` (`dirigent_enforce`): evidence written by the CONSUMER (the eyes). ok→DONE, ≥2 fails no-ok→FAULT, guard→LAWFUL_REFUSAL.
- Live verdict now: **DONE, "2/2 действий легли"**. Enforcer contracts: 3 → **4** (eyes added; true count — not the estimated 5).

## Status
- Commits pushed to `kola-workspace-backup` master: `263768b` (Fix A), `8a5552a` (eyes+contract). `d3e3824..8a5552a`.
- Lanes live. Titan / Solana untouched.
- Remaining WIP (prior session, left untouched, unproven): LEARNINGS.md ×6, `offerup_send.py`.

## Open / next
- Enable `fb_inbox_sweep --peek` unread safety (written, not wired) for the banner-overwrite hole.
- Fix answer-orphaning so detected leads with open commits can't die for lack of a live agent (Larry).
- Convert remaining blind-tap call-sites (fb_mp_giveaway, zina_post_now, fb_bike_listing_edit) to `eyes.act` — each needs its own verify + live proof before commit.
- **Waiting buyers to answer:** Irena (Beelink, seller countered $350 — decision is Boss's); Larry (Giant Rainier bike, CL, unanswered since 16.07).
