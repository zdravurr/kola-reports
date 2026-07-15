# control-reverification-evidence-and-honest-gaps

_2026-07-15 03:09 UTC_

---

# Control re-verification — real evidence, and the honest gaps. Nothing marked done on faith.

Date: 2026-07-15 ~03:10 UTC. Author: Kolya. Brutally honest, as you asked.

## 1. HIERARCHY — REAL, both lanes. One honest gap.
Hand-off record (`dirigent_handoffs.jsonl`), real timestamps, BOTH workers:
```
02:00:32  Chih   ours        → Senya(sales) → RESOLVED
02:05:03  Irena  procurement → Borya(buy)   → RESOLVED   ← dispatched to the OTHER worker
02:26..03:06  Heather/Marie  ours → Senya → RESOLVED     ← the container's autonomous cycles
```
Full chain in the log: `[receive]→[РЕШЕНИЕ полоса=…]→[dispatch → worker]→[answer/borya]→[result]→[review]`.
Who calls whom: the host `autoresponder.py` cron is **commented out**; `dirigent.py` is NOT a host cron.
Dirigent calls `answer_one(w,ctx)` / `work_one(s,l,ctx)`. **Workers do NOT self-trigger.**
And the deal-close escalation runs through it: Irena replied *"lowest I can do is $370"* → Borya escalated
to you ("you decide"), via Dirigent dispatch.

**HONEST GAP:** the container's autonomous flow only SEES sales leads (the sweep feeds `fb_waiting.json`
with our-listing threads: Heather/Marie/Anita). Procurement leads are NOT auto-queued, so **Borya was
reached by a manually-injected lead in the proof run, not by the autonomous cycle.** The dispatch
mechanism is proven for both lanes; procurement *intake* into the autonomous flow is not wired yet.

## 2. WORKERS IN CONTAINER — REAL (hard proof)
The `dirigent.py` process's cgroup is `docker-0efb46e444ac…` = **exactly the dirigent container id**.
Container PID 1 = `bash loop.sh`. The host `autoresponder.py`/`dirigent.py` crons don't run them.
(`docker exec ps` returned nothing only because the minimal image has **no ps binary** — confirmed via
`/proc/1/cmdline`.) Container crontab: empty (loop is the CMD, not cron).

## 3. THREE WORKERS — one honest line each
- **Senya (sales): PROVEN LIVE.** Answered M./Chih/Heather; dispatched by Dirigent in-container (RESOLVED).
- **Borya (procurement): PROVEN LIVE, but only via manual dispatch.** Sent I. a $340 counter (she
  came back $370, escalated to you). NOT yet reached by the autonomous flow (see gap in #1).
- **Ogon (social): yield PROVEN + un-paused (FB + X, one account each). A full live warmup SESSION has
  NOT been watched** — it runs at the next daytime cron slot. So: yield proven, un-paused, live-session unseen.

## 4. SIMPLIFICATION
- **Agent decision — proven, AND I found+fixed a real bug.** "can you tell me about the scratch on the
  frame and whether the owner smoked?" was getting *"The frame is Medium…"* — a tone-deaf non-answer,
  because it over-matched the word "frame". Now nuanced questions (scratch/condition/any issues/does it
  work/previous owner/smoke/why) escalate to the agent; trivial ones (available/price/where/size) don't. 7/7.
- **One source of truth:** items = `item_records` ✅; clients = ONE crm dir ✅; code = git, `autoresponder.py`
  **tracked** ✅, `git status` clean, 0 unpushed ✅.
- **.bak files — NOT all gone (honest).** Workspace: cleaned 22 → 1 (kept newest crontab backup as a
  safety net). **/root: 37 remain** — trades.db + service backups; I left them **deliberately** ("don't
  touch trading"). So: code has one source of truth (git); 37 trading/service state-backups still exist.

## 5. MONEY BEATS WARMUP — yield is AUTOMATIC ✅
`screen_priority.client_lock` (taken by Senya/Borya for every buyer) calls `mark_client_pending(who)`
itself (line 153). The warmups read that flag. Nobody sets it by hand.

## 6. ISOLATION from INSIDE the container ✅ (re-confirmed live)
`/root/.env` → can't even reach /root (Permission denied). `trades.db` → NONE_FOUND anywhere.
`systemctl` → not found. `sudo` → absent. uid = 1000 (non-root). docker.sock → absent.
The container physically cannot touch Titan/Solana.

## 7. TITAN + SOLANA ✅ — uninterrupted
Both active, OOMScoreAdjust=-900. Up since **Mon 2026-07-13 21:21 UTC** — that predates all my
container work tonight (~02:00 15.07). I did not restart them; uptime is continuous.

## THE HONEST NOT-DONE LIST (do not read these as ✅)
- Procurement lead **intake** into the autonomous flow (Borya only reached by manual dispatch).
- Ogon: a live warmup session **stepping aside on its own** not yet watched (only the decision was proven).
- SMS **send** not proven (needs your safe number); Borya-on-SMS not built.
- Container has **no LLM agent** → nuanced questions escalate to you (safe, but not "answered").
- 37 /root trading/service .bak files still there (left on purpose).

Titan + Solana untouched. GLOBAL_STOP holds. 0 root files. Everything committed and pushed.
