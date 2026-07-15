# voice-works-item1-screen-priority-noted

_2026-07-15 00:45 UTC_

---

# Voice input WORKS (item 1). Two live bugs fixed. Screen-priority rule noted as Ogon's gate.

Date: 2026-07-15 ~00:45 UTC. Author: Kolya.

## ITEM 1 — VOICE: WORKING ✅ (please re-test for the fast path)

Your voice note landed and was handled end-to-end: **"Привет, ты тут?"** was received →
transcribed → echoed back **"🎤 Расслышал: «Привет, ты тут?»"** → classified (unclear) → I asked
what you wanted. So the loop works: voice in Russian → text → reply.

**Two real bugs your test exposed, both fixed:**
1. **Groq rejected the audio.** Telegram sends voice as `.oga`; Groq checks format by extension and
   refused it, so it fell back to the slow local whisper. Fixed: I convert `.oga` → WAV (ffmpeg)
   before Groq. Verified: Groq now accepts it. The fast, accurate path is primary again.
2. **Every idle poll errored.** The HTTP read timeout (20s) was shorter than the long-poll (50s), so
   quiet polls always "failed." Fixed: HTTP timeout now exceeds the long-poll. Idle cycles are clean.

One note: please don't have two things polling the bot at once — I caused a couple of `409 Conflict`
lines earlier by hand-polling while the cron also polled. The cron owns it now.

**Re-test, and it'll use the fast Groq path:** send a voice note to **@Derizherrr3_bot** saying
*"какой статус"* — within ~1 min it should reply with the transcription and the live status
(who's waiting + Titan/Mercury health). Action commands ("останови продавца", "снизь цену") will
ask you to confirm "да" before doing anything irreversible.

## YOUR SCREEN-PRIORITY RULE — noted, and it IS Ogon's safety gate

MONEY BEATS WARMUP: a buyer/seller message preempts the phone; Ogon yields immediately; Senya/Borya
does the work; the moment it's done Ogon resumes where it left off (paused by money, not cancelled).
I will **prove this yield live** — a warmup stepping aside for a waiting buyer, then resuming —
**before** Ogon is un-paused. That's item 3, and it will not be skipped.

## ORDER OF WORK (as you set it)
1. Voice ✅ (this) — awaiting your re-test.
2. **Borya** — building the procurement worker next (read seller thread → push price DOWN → gate →
   send → read back → escalate to you before any purchase). Prove live on one real procurement thread.
3. **Ogon** — prove the money-beats-warmup yield, then un-pause ONE account and watch.
4. **Hierarchy** — Dirigent routes leads to the right worker and reviews, instead of workers
   self-triggering.

Titan + Mercury-SOL untouched. Everything committed and pushed.
