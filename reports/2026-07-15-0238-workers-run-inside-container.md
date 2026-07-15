# workers-run-inside-container

_2026-07-15 02:38 UTC_

---

# Item 2 DONE: the orchestrator now runs INSIDE the container. Isolation is real, not just eyes/hands.

Date: 2026-07-15 ~02:38 UTC. Author: Kolya.

## THE WORKERS RUN INSIDE THE CONTAINER NOW

Phase 1 the container just slept (`sleep infinity`) — walls proven, mouth off. **Phase 2: it runs
the orchestrator itself.** The control loop — receive lead → decide lane → dispatch to Senya/Borya →
review — now EXECUTES inside the isolated container (uid 1000, cap_drop ALL, read-only rootfs), and
reaches the phone over its OWN tailnet node. The host cron is gone.

Proven from INSIDE the container (live):
- **Phone via tailnet** — `su("echo") → PHONE_OK` over the mounted key + ts-dirigent node.
- **item_records** — Giant bike, for_sale, $100.
- **review_gate** — loads and gates.
- **Orchestration** — received 3 real leads, dispatched each to the right worker, reviewed. Audit in
  `dirigent_handoffs.jsonl`: Heather→Senya, Marie→Senya, Irena→Borya, all reviewed.

The container restart broke the tailnet sidecar (the one-time auth key was spent); I recovered it by
running `tailscaled` from its **persisted state** — no new key needed.

## TWO REAL BUGS the in-container run exposed (both fixed)

1. **The breaker didn't engage on slow cycles.** Fails were saved only at cycle end, but the flaky
   phone makes cycles long, so a heavy lead (Heather) re-escalated every cycle. Now the counter
   persists **after each lead** — even a killed cycle leaves it, so the breaker stops after 2.
2. **Heather spammed escalations.** Her message — *"we picked up a specialized bike today, my son is
   stoked!"* — is a buyer who **bought elsewhere and is closing**, but it fell to the LLM agent, which
   **doesn't exist in the container** → fail → escalate every cycle. Now the closed-deal detector
   (extended to catch "we/just picked up/found another") marks it RESOLVED — no agent, no alarm. Real
   buyers ("is this available?") are untouched. Verified in-container: Heather → RESOLVED.

## TWO HONEST CONTAINER GAPS (by design, safe)

- **No LLM agent (`claude` CLI) inside** → non-trivial replies escalate to you instead of being
  composed. Deterministic replies (price/availability/gone/closed) work without it. Adding an LLM to
  the container is a future step.
- **No secrets.json inside** → the container can't send Telegram directly, so alarms go to the
  **outbox** and the host drain delivers them. Nothing is lost.

## WATCHING THE CONTAINER (cron_guard doesn't reach docker)

Moving the orchestrator in-container made cron_guard falsely alarm "dirigent.py missing from cron."
Fixed: removed it from cron_guard (that guards host crons). The container is now watched by
(1) Docker `--restart unless-stopped` for crashes, and (2) a root-cron `dirigent_container_watch.sh`
that catches "container gone" or "loop stuck >20 min", restarts from persisted state, and alarms you.

## WHERE WE ARE
1. Hierarchy ✅
2. **Workers inside the container ✅ (this)** — running live, self-guarded, settled.
3. SMS as a full channel (Senya + Borya) — next.
4. X warmup yield + un-pause — after.

Titan + Mercury-SOL untouched. GLOBAL_STOP holds. 0 root files. Everything pushed. Onward to #3.
