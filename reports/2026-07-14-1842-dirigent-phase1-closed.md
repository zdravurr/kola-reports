# dirigent-phase1-closed

_2026-07-14 18:42 UTC_

---

# Dirigent — PHASE 1 CLOSED: all 5 proofs done, from inside the container

Date: 2026-07-14. Author: Kolya.
**Verdict: phase 1 is FULLY CLOSED.** All five proofs were run inside the container and the output was read, not assumed.
Trading: **UNTOUCHED** — Titan and Mercury-SOL both `active`, no restart, no file of theirs touched.
Mouth: **STILL OFF** — GLOBAL_STOP holds. No sweep, no autoresponder, no agent, no cron inside. **Not one buyer was written to.**

---

## your Pixel question — answered, and it was a good catch

**The live node is `pixel-10a-2`.** It is the one the whole system already uses, and the one the Dirigent now targets:

```
pixel-10a     -> offline, last seen 30d ago    (dead)
pixel-10a-1   -> offline, last seen 29d ago    (dead)
pixel-10a-2   -> ACTIVE, direct connection     (THE PHONE — 41 code files target it; adb shows it connected)
```

Same phone, re-registered twice. But your suspicion paid for itself: **two watchdog scripts still pointed at the node that has
been dead for 30 days** (`adb-watchdog.sh`, `kola-watchdog.sh`). Neither is in any cron today, so nothing was broken — but a
watchdog whose whole job is "repair the ADB link" and which repairs it toward a phone that does not exist is a loaded gun:
schedule it tomorrow and it reconnects into the void forever while reporting that it tried. Both now point at the live node
(commit f80c65f). **Zero executable references to a dead node remain anywhere in the code.**

**Should you delete the two dead entries from the tailnet? Yes — recommended.** Nothing references them, they are the same
phone, and their only remaining function is to confuse a human (or me) at 2am into targeting the wrong address. Deleting them
in the admin console is safe and reversible (the phone can always re-register). It is your click to make — I do not have access
to the Tailscale console.

**One caveat you should know:** the Dirigent's own tailnet node is registered with the **ephemeral** key you gave me, so the
node disappears from the tailnet automatically when the container stops. That is good hygiene (no zombie nodes — exactly the
mess we just cleaned up), but it means the node list will show `dirigent` only while it is running.

---

## THE FIVE PROOFS — ALL FROM INSIDE THE CONTAINER

### 1. It reaches the LIVE Pixel — and only the live one

```
adb port 5555 (pixel-10a-2)  -> REACHABLE
ssh port 8022 (pixel-10a-2)  -> REACHABLE
dead pixel-10a (100.93.x)    -> unreachable  (as it should be)
```

How, without giving the container root: `tailscaled` runs in a **sidecar** that holds `NET_ADMIN` + `/dev/net/tun`; the Dirigent
**shares its network namespace**. So it gets a revocable tailnet identity of its own (node `dirigent`) while itself
staying `uid 1000`, `cap_drop ALL`, read-only rootfs. The sidecar can see neither the workspace nor the state — it is only a
network card. **Revoke the key in the admin console and the container loses the phone in one click.**

### 2. EYES — a real screenshot, which I looked at

```
ssh from inside      -> SSH-FROM-CONTAINER-OK / Pixel 10a
warm mux, 1st call   -> 1.9s
warm mux, 2nd call   -> 0.4s      <- the mux is warm and being reused, not re-handshaking
screencap            -> 1,946,977 bytes
screen geometry      -> 1080 x 2424   <- the real screen (the old 2298-width blindness is gone)
```

I pulled the PNG out and **looked at it**: the phone's home screen, `Tue, Jul 14`, 87°F, the clock reading 1:36. Not a
"screencap returned True" — an actual picture of the actual phone.

### 3. HANDS — a vision-verified tap that moved the phone

I tapped the **Settings icon** — deliberately harmless, reversible, nowhere near Marketplace, and I put the phone back on the
home screen afterwards.

```
vtap 'Settings icon' (412,553) -> changed=1,816,203 px (69% of the screen), bbox=(0,0,1080,2424)
after-screenshot                -> the Settings app is open (its search box, 'Network & internet', 'Connected devices')
```

The full contract ran: **screencap → diff → tap → verify by second screencap.** The tap landed, the phone responded, and the
change was confirmed by vision.

**Honest detail, because it matters:** `vtap` returned `verdict=fullscreen_change, ok=False`. That is **not** a failure of the
hands — it is the guard doing its job. `vtap` is built for taps *inside* an app, where a correct tap changes a small region; a
full-screen repaint is what an *accidental* nav tap looks like, so it refuses. Launching an app legitimately repaints
everything, which is why my test target trips it. I checked the `danger_ok` escape and found it only applies to taps inside the
nav "danger zones", so it does not relax this case either. **Nothing to fix for phase 2** (the sales flow taps threads and
buttons *inside* Messenger, which is exactly the local-change case `vtap` is designed for) — but you should know the verdict I
got was `ok=False`, and that I verified the tap worked by *looking*, not by trusting the return value.

### 4. ANTI-BAN PACING — intact inside

```
think() x5      -> 1.78s, 1.29s, 0.95s, 1.70s, 1.40s   <- randomised, not a robotic fixed interval
read(25 words)  -> 6.96s                                <- reading time scales with text length
cadence(fb,dm)  -> {interval_s: 60, daily_cap: 100}     <- daily budget state readable AND writable from inside
touch synth     -> randomised tracking id, pressure and +/-50px coordinate jitter
```

(Correction to my earlier assumption: pacing lives in `lib/kola_human.py`, not in `phone_hands`. My first probe called a
function that does not exist and would have printed a happy `0.00s` — I caught it and went and found the real thing.)

### 5. ONE OWNER OF THE SCREEN — re-proven with the container on its own network node

```
container takes the phone      -> host sees: "held by dirigent/pid=69"
HOST tries to drive the Pixel  -> BLOCKED (fail-closed, operation does NOT run)
container releases             -> host screencap works again immediately
```

the `flock` sits on the shared volume, so it holds across the container boundary regardless of network namespace.

### WALLS — final re-check from inside

```
/root/.env      -> Permission denied, and the file does not exist in the container at all
trades.db       -> 0 found anywhere in its filesystem
systemctl       -> ABSENT      (it cannot stop Titan: there is no systemctl and no init)
sudo            -> ABSENT
docker socket   -> ABSENT      (no escape hatch)
rootfs          -> read-only
```

---

## OPEN / NOT DONE (stated plainly)

- **The autoresponder is still unproven.** It has run exactly once in its life, and it died. That is **phase 2**, and the mouth
  stays off until it answers a real buyer and I have read back what actually landed on the screen.
- **The X/FB warmup scripts still reach `adb` directly** and do not take the screen lock. They are all `#PAUSED`, so nothing is
  racing today — but **they must take the lock before the X warmup is ever un-paused.**
- **40+ files hardcode the phone's IP.** Today they all point at the live node, so nothing is broken. But when this phone
  re-registers a third time, it will be 40 edits. Worth collapsing to one constant in a later, quiet step.
- **`vtap` cannot cleanly verify an app-launch tap** (see proof 3). Not blocking; noted so nobody is surprised.

## ROLLBACK

`docker stop dirigent ts-dirigent` → the ephemeral tailnet node disappears by itself, the state files never moved (they are
bind-mounted, not copied), the host crons still run, `sales_owner` still says `host`. Nothing in phase 1 is one-way.

## COMMITS

```
f80c65f  watchdogs pointed at a Pixel dead for 30 days -> live node
8b42560  the Dirigent's own tailnet node; eyes+hands proven from inside (D2 closed)
```

---

**Phase 1 is closed. Phase 2 on your word: prove the autoresponder live on ONE real thread — read history, compose from
item_records, pass the gate, send, and read back what actually landed. The mouth stays off until that passes.**
