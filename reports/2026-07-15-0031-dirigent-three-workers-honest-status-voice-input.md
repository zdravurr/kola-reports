# dirigent-three-workers-honest-status-voice-input

_2026-07-15 00:31 UTC_

---

# Honest status: only 1 of Dirigent's 3 workers is proven. Plus voice input, built.

Date: 2026-07-15 ~00:35 UTC. Author: Kolya.
You were right to push. I overclaimed "Dirigent done" — two-thirds is unverified. Here is the truth.

---

## THE HONEST SCORECARD

| Worker | Job | Reality |
|---|---|---|
| **SENYA** (sales) | answer buyers on our listings | ✅ **PROVEN LIVE** — answered Mahsa, Chih, Heather with post-send proof; in cron, self-guarded. |
| **BORYA** (procurement) | negotiate the things WE buy | ❌ **DOES NOT EXIST as a worker.** Only a routing label. |
| **OGON** (social/warmup) | grow the accounts | ⚠️ **BUILT but PAUSED 2 days; safety to un-pause NOT verified.** |

And the framing itself needs a correction: **the workers do NOT run inside the Dirigent container.**
The container has proven *eyes + hands* (Phase 1), but its crontab is **empty** and it runs **zero**
worker processes. Senya's loop is a **host** botuser cron. So "Dirigent orchestrates three workers
inside it" is aspirational — today it's one worker loop, on the host.

## BORYA (procurement) — identified, but nobody works them

`lib/lead_router.py` has a "buying → Боря (worker2)" lane, and Senya's gate correctly **identifies**
procurement threads (Irena/Beelink, Robert/Async, Michelle/La-Z-Boy) and **routes them away** — it
alarms you and stays silent, which is the *safe* half. But **there is no executor**: no
`procurement_responder.py`, no negotiation loop, nothing that drives a price down or replies to a
seller. The I./Robert/Michelle threads are correctly *flagged as ours-to-buy* and then **sit
there**. Borya is a label, not a worker. Building his loop is real, unstarted work.

## OGON (social) — frozen, and not safe to blindly un-pause

- **Executors exist:** X warmup (`zdravurr_auto.py`), FB warmup (`fb_zdravurrrr_warmup.py`),
  `ogon_supervise.py`, `growth_collect.py`.
- **Frozen:** 10 warmup crons `#PAUSED13JUL`. Last actual run: X Jul 13 16:01, FB Jul 13 19:00 —
  **two days dark.** `ogon_supervise.py` / `growth_collect.py` are **not in cron at all**.
- **Runs on the host**, not in the Dirigent container.
- **Is it safe to un-pause now? I can't confirm it.** The OOM cause (agent-husk leak) was capped, so
  that specific incident won't repeat. BUT: `run_guarded.sh` gates warmup only on **overload**, not
  on the **screen lock** — and I found **no screen-yield logic** in the X warmup. So I cannot prove
  the warmup would **yield the phone to a waiting buyer** (Senya's client-pending). Un-pausing without
  that check risks the warmup grabbing the screen while a real buyer waits, and re-heating the
  anti-ban risk that got these accounts label-flagged before.
- **My recommendation:** do NOT auto-un-pause. It needs a deliberate pass first — confirm the warmup
  yields to `screen_priority` client-pending, and re-check the anti-ban intervals — then un-pause one
  account and watch. That's a scoped next-session task, not a flip-the-switch.

## VOICE INPUT — BUILT (`lib/dirigent_voice.py`), and how to test it

You can now send **Russian voice** to **@Derizherrr3_bot** and the Dirigent transcribes + confirms
before anything irreversible. Same G. Whisper path the gateway already uses.

- Voice → download → transcribe → **always echoes "🎤 Расслышал: «…»"** so you see what it understood.
- **Read-only** ("какой статус? кто ждёт?") → answers immediately from real state (watchdog + systemctl).
- **Action** (pause / send / change price / restart / trade) → **"⚠️ подтверди «да»"** first; only on
  an explicit "да" does it queue execution; "нет" cancels; unclear → it asks. Fail-closed.
- Runs as a cron (*/1, flock, 50s long-poll ≈ continuous), protected by cron_guard.

**Proven:** the live long-poll connects and reads updates; the intent classifier is 10/10 on a Russian
test set (a real bug fixed — Russian stems need a left word-boundary only, or "отправь" wouldn't
match); the status answer builds from real facts. **Not yet proven:** a real end-to-end voice message,
because that needs you to speak. **Please test:** send a voice note to @Derizherrr3_bot saying
*"какой статус"* — within ~1 min it should reply with the transcription and the live status.

## STATE

GLOBAL_STOP holds. Titan + Mercury-SOL active, untouched. Everything committed and pushed.
9 money-path crons guarded (added the voice poller).

## NEXT (honest backlog)
1. **Build B.** — a procurement/negotiation loop, so identified buy-threads actually get worked.
2. **Ogon un-pause, safely** — verify screen-yield + anti-ban, then un-pause and watch.
3. Optionally: actually move the worker loops **into** the Dirigent container (today they're host crons).
4. Still open from before: full money-path re-audit; restrict/deploy-checkpoint for me.
