# dirigent-isolation-plan

_2026-07-14 16:49 UTC_

---

# Dirigent isolation — PLAN ONLY (nothing built) + item truth recorded

Date: 2026-07-14. Author: Kolya. Status: **Part 2 DONE and committed. Part 3 = plan, awaiting Boss approval.**
Trading (Titan + Mercury-SOL): **NOT TOUCHED.** No file, no cron, no unit of theirs was read-modified or restarted.

---

## 0. WHAT THE BOSS MUST DECIDE (five things, everything else follows)

| # | Decision | My recommendation |
|---|---|---|
| D1 | **Who owns the Pixel?** today the host drives it (adb + ssh). After isolation the Dirigent container must be the ONLY driver — the host keeps a read-only screenshot path at most. | Container owns it. One owner or we re-live "agents and manual sessions fight for the screen". |
| D2 | **How the container reaches the Pixel:** (a) its own Tailscale node inside the container (own auth key), or (b) it stays on the docker bridge and routes through the host. | (a) own Tailscale node — clean, auditable, survives host changes. |
| D3 | **Retire one of the three detection paths.** Keep: screen sweep (primary) + mail watch (backup). Retire: the phone-node notification reader. | Approve the retirement. Three ways to break, one truth. |
| D4 | **Dirigent needs its OWN Telegram bot.** Only the Boss can create it in @BotFather. I need the token; it never enters git, never enters a report. | Create it before phase 1. |
| D5 | **Delete ~30 `.bak_*` files** in `projects/sales/` and `lib/` (every one is already in git history). | Approve — one source of truth for code = git. |

---

## PART 1 — LIVE STATE, VERIFIED JUST NOW (read only, nothing changed)

Confirmed healthy:
- **git** intact, working tree clean before my change; Titan repo `main` @ c7976f3.
- **Gateway** HTTP **200** on :18789.
- **Titan** active, **Mercury-SOL** active. Both OOM-armored: `OOMScoreAdjust=-900`, `MemoryMin=600M`.
- **Detection crons** alive: inbox_sweep, fb_inbox_sweep, mail_watch, node_notif_watch, buyer_watchdog,
  post_watchdog, commit_watchdog, report_outbox drain+watchdog. (They are the EYES — they run; the MOUTH is off.)
- **Root-owned files in the workspace: 2, not 0** — `lib/report_publish.py` and its `.pyc`. I wrote them as root
  last session. Harmless today (botuser can read them) but it is exactly the class of thing we are stamping out.
  I did NOT chown them, because this task says change nothing but the item records. One-line fix on your word.

The truth, plainly:
- **The GLOBAL_STOP pause (yours, Jul 13 21:27) still holds. The mouth is OFF.** `.kola_state/pause/GLOBAL_STOP` exists;
  the X/FB warmup and keepalive crons still carry `#PAUSED13JUL`.
- **~36 buyers are waiting.** Nothing has answered them and nothing will until you lift the pause.
- **`kola-inbox-watcher.service` is inactive** → `watcher.log` is frozen → **`buyer_watchdog` is guarding a corpse.**
  It will not shout. It will not fix itself when the pause lifts.
- **The autonomous seller has NEVER worked.** `projects/sales/autoresponder.py` exists (written 13.07), was
  **never in any cron**, and its single run died on all four buyers while reading thread history. The screen-width
  bug behind that (1080x2400) is fixed — but the autoresponder has **never been re-run live since**. Not proven.
- Everything a buyer has ever received was typed by me, by hand, through the gate.

---

## PART 2 — THE TRUTH ABOUT ITEMS IS NOW RECORDED (the one change; done, committed, live-proven)

Your order: **only the owner's Giant bike is for sale, $100. Everything else is gone.**

| item | before | now |
|---|---|---|
| Giant bike (owner: the Boss's contact) | for_sale (after the fabricated-SMS rollback) | **for_sale, $100 firm** — re-affirmed against your word |
| coffee table (oak) | `unverified` | **gone** |
| writing desk (maple) | `unverified` | **gone** |
| sectional sofa | `unverified` | **gone** |

Every status change carries evidence `{kind: "boss", ref: "<your order, 2026-07-14>"}` — `set_status()` refuses to
move an item without a re-checkable source (the hole that let me fabricate an SMS on 14.07).

**Two fail-OPEN holes found while writing this down — both closed:**

1. **The gate would NOT have blocked the sofa, table or desk.** They sat at status `unverified`, and the gate
   blocked only the statuses `sold` and `gone`. A reply saying *"the sectional is yours, when can you pick it up?"*
   would have **PASSED**. The block list always lags reality, so it is now an **allow list**:
   `OFFERABLE_STATUSES = (for_sale, giveaway, pending)` — anything else (gone, sold, unverified, blank, typo,
   any future status) **cannot be offered**. Fail-closed, in both places that check (`item_records.contradictions`
   and `reply_sanity.unanswered`).
2. **The sofa's built-in default was `giveaway`** — a `sync()` would have resurrected it as available. Default is now `gone`.

**Live proof (real gate function the send path calls, run against real records):**

```
BLOCK zina_sectional_sofa  "the sectional is still available! It's yours — when can you pick it up?"
BLOCK zina_coffee_table    "the oak coffee table is yours, still free. Tomorrow works — I'll hold it."
BLOCK zina_writing_desk    "yes the maple desk is available, come get it this evening."
PASS  zina_sectional_sofa  "sorry — the sectional is gone already, someone picked it up."   <- honest 'no' allowed
PASS  bike_giant_rainier   "still available — $100 firm, Medium frame, fits 5'6"-5'10", OC area."
```

Regression of the exact old hole: an item in a non-offerable status now BLOCKS. Committed as `51a652a`.

**Answer to your question: yes — as of now, nothing can offer a gone item to a buyer.**

---

## PART 3 — THE PLAN: ISOLATE SALES INTO "DIRIGENT" (plan only, nothing built)

### 3.1 Target shape

- **KOLYA (me)** — admin with root on the host. Supervises nobody, controls nobody. A tool that executes your
  server tasks. Keeps the current OpenClaw Telegram channel.
- **DIRIGENT** — the one orchestrator over **Ogon, Borya, Senya**. its own container, its own Telegram channel. **No root.**
  Runs sales / social / procurement: lead -> right worker -> review -> escalate to you only at deal close.
- **TRADING LEAD** — later, separate step. Not now.
- **BOSS** — above all three, one channel each.

Order, as you set it: **1) Dirigent -> then the mouth on, answer the waiting buyers. 2) Then restrict Kolya +
deploy checkpoint. 3) Trading LAST, only at zero open positions.**

### 3.2 The container

Base it on the proven `claude-agent` pattern already running (3 containers up ~20h): **uid 1000, no privileges,
memory-capped, own bridge network, only its own dirs bind-mounted.** for the Dirigent container:

**IN (bind-mounted, the only things it can see):**

| path inside | what | mode |
|---|---|---|
| `/work/workspace` | the sales/social code: `projects/sales`, `projects/fb_social`, `lib/` + its own git clone | rw |
| `/work/state` | `.kola_state/` — items.json, status overrides, CRM, owner phones, locks | rw |
| `/work/secrets/dirigent_bot` | its own Telegram bot token (file, ro) | ro |
| `/work/secrets/pixel` | the Pixel ssh key + adb key | ro |

**OUT — physically absent, not "forbidden by policy":**
`/root/titan-bot` · `/mnt/.../mercury-sol` · `/root/.env` (exchange keys) · `trades.db` · the docker socket ·
systemd (a container has none) · the root crontab · `/usr/lib/node_modules` · apt/npm at runtime
(read-only rootfs + tmpfs `/tmp`; packages baked at build time only) · `cap_drop: ALL` · `no-new-privileges` ·
**no sudo, no sudoers entry, uid 1000.** It cannot `systemctl stop titan` because there is no systemctl and no
init to talk to. It cannot read the exchange keys because the file is not in its filesystem.

### 3.3 How each capability SURVIVES inside the container

- **Driving the Pixel.** This is the easy part, and it is why the plan works: **the phone is already reached over the
  network, not over a USB device node.** Today: `adb` to the phone's tailnet address on the adb port, and ssh (Termux sshd) on its ssh port,
  over Tailscale. A container needs no `/dev` passthrough — it needs an IP route. Two ways (decision **D2**):
  - **(a) preferred:** run `tailscaled` inside the container in userspace-networking mode with its **own auth key**
    → Dirigent becomes its own node on the tailnet, reaches the Pixel directly, and you can revoke it in one click.
  - **(b) fallback:** stay on the docker bridge and route to the Pixel through the host. Works, but the host becomes
    a silent dependency and the ACL story is muddier.
  The warm ssh mux (`lib/pixel_ssh.py`, ControlMaster `/tmp/pixel_tap_mux`) moves inside the container unchanged.
- **One owner of the screen (decision D1).** The single biggest risk: two adb servers (host + container) driving one
  phone is the exact "the list of threads did not render / agents fight over the screen" failure from last session.
  Rule: **the container owns the Pixel.** The existing `flock`-based screen lock (`run_guarded.sh`,
  `kola_focus_guard`) moves onto a bind-mounted lock dir so anything left on the host still has to take the same lock.
- **Its own data.** `.kola_state` is bind-mounted → items.json, CRM, overrides persist on the volume exactly where
  they are today. **No data migration, no copy, no export.** Stop the container and the files are still there.
- **Its own Telegram channel (D4).** A second OpenClaw gateway instance inside the container with its **own bot
  token** — OpenClaw's config holds exactly one `channels.telegram.botToken`, so a second bot means a second
  instance, which is what we want anyway: separate process, separate channel, separate blast radius. My channel is untouched.
- **Committing its own code.** Its own git clone on the mount + a deploy key limited to the workspace repo.

### 3.4 The simplifications, baked in

- **A — no agent for the trivial 80%.** "is it available / how much / where / when" is answered by
  **`autoresponder.py` straight from `item_records`, with no agent wake-up at all.** Agents (Ogon/Borya/Senya) are
  woken only for negotiation, unusual questions and deal close. This deletes ~10 of the 15 links in today's chain and
  kills the OOM-avalanche at its root: the avalanche is agents being spawned for questions a dictionary can answer.
  It also fixes the thing that has never worked — the mouth becomes a **loop**, not a **wake-up**.
- **B — one source of truth per thing.** `item_records` for item facts (nothing else may state a fact about an item),
  **git** for code (delete the ~30 `.bak_*` files — decision **D5**), one CRM for clients. The competing sources get
  deleted, not left lying around.
- **C — never guess.** Unknown fact -> ask the Boss -> **write the answer into the item record permanently.** The
  record is the memory; my head is not.
- **D — buyer vs seller can never be confused.** Thread on OUR listing = a BUYER (-> Senya, hold the price UP).
  Thread on someone else's listing where WE wrote first = we are the buyer (-> Borya, push the price DOWN).
  **The autoresponder runs ONLY on our items** (the alias-matching in item_records already refuses generic words
  like "bike" precisely because they matched other people's listings). Whose thread it is, unclear -> **no guess, escalate.**
- **E — detection: three paths down to two.** Keep the **screen sweep** as primary (it reads the actual screen — the
  only source that cannot lie to us) and **mail watch** as backup. **Retire the phone-node notification reader**
  (decision **D3**). Dedup stays but has less to dedup.

### 3.5 Rename main -> Dirigent

`~/.openclaw/agents/main` -> `agents/dirigent`, plus the places that name it: `lead_router`, the sweep's wake-up call,
`agent_capacity`, `AGENTS.md`, the cron lines. Ogon/Borya/Senya keep their worker slots.

### 3.6 Phases (each one verified before the next)

1. **Build the image + start `dirigent` with the mouth still OFF.** Prove from *inside*: it can screenshot the Pixel;
   it can read/write item_records; it can post to its own Telegram channel; and it **cannot** see `/root/.env`,
   `trades.db` or `systemctl`. Show you the failures as proof of the walls.
2. **Prove the autoresponder live on ONE real thread** (read history -> compose from item_records -> gate -> send ->
   read back what actually landed). This is the step that has never once been completed. Nothing scales until it passes.
3. **Move the sales crons into the container** (its own supervisor). Teach the host's root `cron_guard` that sales
   left the host, so it stops restoring host copies — otherwise two systems drive one phone.
4. **Then, on your word: lift GLOBAL_STOP, answer the ~36 waiting buyers.**
5. restrict Kolya, add the deploy checkpoint. 6. Trading, last, at zero open positions.

### 3.7 Rollback

The whole plan is **additive**. The code stays in git; the state stays on the volume, bind-mounted (not copied). Rollback =
`docker stop dirigent`, un-pause the host crons, and we are exactly where we are today. There is no migration to undo.
The only irreversible acts in the whole plan are deleting the `.bak_*` files (recoverable from git) and revoking
botuser's NOPASSWD — and that one is not in this phase.

### 3.8 Honest risks

1. **Two owners of one phone** (host adb + container adb). Highest risk. Mitigation: D1 + the shared flock. If we get
   this wrong, the symptom is not an error — it is threads that silently fail to render, which is how last session died.
2. **`cron_guard` runs as root and blindly restores the 8 detectors** — it does not know about GLOBAL_STOP and it will
   not know about the container. Until it is taught, it will happily resurrect a second copy of the sales loop on the host.
3. **Tailscale-in-container** needs an auth key and a little ACL work; the fallback is uglier but exists.
4. **A second OpenClaw gateway = a second OAuth session** on the same Max pool. It must not heartbeat (that is what
   drained the pool once already).
5. **The autoresponder is unproven.** It has run exactly once, and it died. I am not going to call it working until it
   has answered a real buyer and I have read back what actually landed on the screen.
6. **Sales downtime during the move is real** — and fine, because the mouth is off anyway.

### 3.9 What this plan does NOT touch

**Titan and Mercury-SOL: nothing.** No mount, no unit, no cron, no config, no restart. The container cannot reach them
even if it tried. Trading is not in phase 1, 2, 3 or 4 — it is step 6, at zero open positions, on your word.

---

**Nothing above is built. Say which of D1-D5 you approve and I start at phase 1.**
