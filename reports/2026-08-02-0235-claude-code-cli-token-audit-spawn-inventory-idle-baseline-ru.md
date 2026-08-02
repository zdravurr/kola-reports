# Claude Code CLI token audit — spawn inventory, idle baseline, runaway loops

_2026-08-02 02:35 UTC_

---

## TL;DR

Subscription limits are consumed by **`claude` CLI spawns**, in two tiers:

| tier | spawns 7d | tokens 7d | share |
|---|---:|---:|---:|
| **Interactive** (Boss/Kolya sessions in terminal) | 30 | 2,260,894,955 | 88.9% |
| **Automated** (cron/daemon/gateway, nobody asked) | 4,440 | 281,904,844 | 11.1% |
| **TOTAL** | **4,470** | **2,542,799,799** | |

Raw tokens are dominated by interactive work — that is the Boss working, not waste.
**The waste is concentrated in the automated tier, and there two spawn points are 68% of it.**

🔴 **Measured idle cost:** with zero Boss and zero Zina commands for 60 minutes, the box spawned
**63 `claude` sessions — 100% of them the same runaway loop** — burning **~750 k billable +
~1.17 M cache-read tokens/hour to emit 945 tokens of output**. That is the price of doing nothing.

🔴 **The headline defect:** an emergency stop engaged **2026-07-28T15:10:23Z** blocks the *cheap*
step (waking `main`) but sits **downstream** of the *expensive* step (a full Opus-5 spawn). Since the
dedup ledger is only written **after** a successful wake, and the wake can never succeed while the
stop is engaged, the same two chat messages have been re-translated by Opus **every ~90 seconds for
5 days**. The stop does not save money — it converts the system into a token furnace that burns the
LLM call and throws the result away.

---

## 1. INVENTORY OF SPAWN POINTS

### 1.1 How subscription tokens are actually spent

Auth is **OAuth subscription**, not an API key:
`/root/.claude/.credentials.json` → `{"claudeAiOauth": {…, "subscriptionType", "rateLimitTier"}}`.

Every consumer reaches the model one of two ways, and **both end in the same `claude` binary**:

1. **Direct** — `subprocess.run(["claude","-p", …])` from Python.
2. **Via the gateway** — `openclaw agent …` → OpenClaw gateway → spawns `claude`.
   Proof, `extensions/anthropic/cli-backend.ts:25-33`:
   ```ts
   docker: { npmPackage: "@anthropic-ai/claude-code", binaryName: "claude" },
   config: { command: "claude",
             args: ["-p","--output-format","stream-json","--include-partial-messages",
                    "--verbose","--setting-sources","user","--allowedTools","mcp__openclaw__*"],
             resumeArgs: [ …, "--resume","{sessionId}" ], … }
   ```
   `--setting-sources user` is why the botuser `SessionStart` hook fires on **every** gateway spawn
   (see §3.2).

Binary: `/usr/bin/claude` → `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`,
**version 2.1.220**. Gateway: `openclaw 2026.6.11` (`/usr/lib/node_modules/openclaw`).

### 1.2 Every spawn site in code, with live verdict

Verdict = did this site actually start a session in the last 7 days, measured by the **first user
prompt** of every transcript (not by grep — grep over transcripts is contaminated by file reads and
by this audit's own session).

| file:line | owner | spawns 7d | verdict |
|---|---|---:|---|
| `projects/sales/inbox_agent.py:823` (via `inbox_watcher.py:285`) | **inbox_watcher** | **4,139** | 🔴 FIRES — runaway |
| `lib/screen_sense.py:124` | **eyes.py** / vision layer | 127 | ✅ FIRES |
| `scripts/autonomy/self_improve_daily.py:187,305` | Kolya self-audit | 42 | ✅ FIRES |
| `lib/dirigent_brain.py:110,151,169` | **dirigent_brain** | 42 | ✅ FIRES |
| `scripts/main_liveness.py:101` (`openclaw agent`) | **Kolya main session** watchdog | 29 | 🔴 FIRES — 2.7M tok/ping |
| `projects/social_x/zdravurr_auto.py:1023`, `_ca_auto.py:917` | **Ogon** (X lanes) | 20 | ✅ FIRES |
| `projects/fb_social/fb_engage.py:163` | **Ogon** (FB) | 1 | ✅ FIRES |
| `lib/kola_eyes.py:184,226` | eyes (model-vision) | **0** | ⚪ DEAD |
| `lib/ogon_post.py:40` | **Ogon** | **0** | ⚪ DEAD |
| `lib/llm_intent.py:63` | intent router | **0** | ⚪ DEAD |
| `projects/sales/listing_gen.py:88` | **Senya** | **0** | ⚪ DEAD |
| `projects/sales/answer_backlog.py:87` | **Senya** | **0** | ⚪ DEAD |
| `projects/sales/inbox_agent.py:396` (reply-gen) | **Senya** | **0** | ⚪ DEAD |
| `projects/social_x/zdravurr_post_now.py:188` | **Ogon** | **0** | ⚪ DEAD |
| `scripts/kola-bridge/kola.py:244` | kola-bridge | **0** | ⚪ DEAD |
| `scripts/commit_watchdog.py:130` (`openclaw agent`) | commit watchdog | 0 | ⚪ DEAD in window |
| `lib/agent_capacity.py:539` (`openclaw agent`) | **shared wake gate** | — | gate used by all detectors |

`lib/kola_eyes.py` being dead is **by design** and documented at `lib/eyes.py:29`: the live eyes are
`uidump` + local tesseract, *not* a model. Model-vision has "ZERO callers — dead code".

**Owner map for the names requested:**

- **eyes.py** → does *not* spawn. Vision that costs tokens is `lib/screen_sense.py:124` (127 spawns).
- **dirigent_brain** → `lib/dirigent_brain.py:110,151,169`, 42 spawns.
- **Senya** (sales replies) → `listing_gen`, `answer_backlog`, `inbox_agent:396` — **all 0**. Senya's
  lane is idle; what fires under "sales" is only the translate helper.
- **Borya** (procurement) → `projects/procurement/borya*.py` — **no claude spawn site at all**.
- **Ogon** (growth/social) → `zdravurr_auto`, `_ca_auto`, `fb_engage` (21 spawns); `ogon_post`,
  `zdravurr_post_now` dead.
- **inbox_watcher** → `inbox_watcher.py:285` → `inbox_agent.py:823`. **4,139 spawns = 93% of all
  automated spawns.**
- **park_guard** → `lib/park_guard.py` — **no spawn site**.
- **report_publish** → `lib/report_publish.py` — **no model spawn**; it shells `git` only.
- **Kolya sessions** → 30 interactive (`entrypoint=cli`, `cwd=/root`) + 19 worker subagents
  (`workspace-worker1-3`).

### 1.3 Launchers (systemd / cron / daemons) that can reach a spawn

| launcher | user | schedule | reaches |
|---|---|---|---|
| `inbox_watcher.py` (daemon, PID 3733399, up 4d11h) | botuser | `WATCH_INTERVAL=10s` loop | 🔴 translate_ru |
| `scripts/main_liveness.py` | botuser cron | `*/10 * * * *` | 🔴 LIVENESS ping |
| `lib/dirigent_voice.py poll 20` | botuser cron | `* * * * *` | dirigent_brain |
| `lib/dirigent_worker_guarantee.py` | botuser cron | 6,16,26,36,46,56 | worker wake |
| `lib/lead_guarantee.py run` | botuser cron | `*/10` | worker wake |
| `scripts/autonomy/self_improve_daily.py` | botuser cron | `0 9 * * *` | self_improve |
| `zdravurr_auto.py` / `_ca_auto.py` | botuser cron | 10,16,22 / 13,20,23:30 UTC | Ogon X |
| `fb_zdravurrrr_warmup.py`, `ev_group_recurring_post.sh` | botuser cron | 11:30,17:30,23:30,00:30 / 19:00 | Ogon FB |
| `scripts/commit_watchdog.py` | botuser cron | `*/10` | `openclaw agent` (self-heal) |
| `openclaw` gateway (PID 1238225) | botuser | always-on | all `openclaw agent` spawns |

`titan.service` / `mercury-sol.service` do **not** spawn `claude` — see §7.

---

## 2. WHERE THE USAGE RECORDS LIVE

Not assumed — discovered. Claude Code writes one JSONL transcript per session under
`<home>/.claude/projects/<slug-of-cwd>/<session-uuid>.jsonl`:

- `/root/.claude/projects/` — 133 files, 571 MB (root/interactive sessions)
- `/home/botuser/.claude/projects/` — 7,033 files, 2.3 GB (13 project dirs, all automation)
- **4,479 files touched in the last 7 days**

Each assistant record carries exact per-message billing:

```json
{"type":"assistant","timestamp":"2026-08-01T16:42:49.938Z","cwd":"/root",
 "sessionId":"cca4843d-…","entrypoint":"cli","version":"2.1.220",
 "message":{"model":"claude-opus-5","usage":{
   "input_tokens":2,"cache_creation_input_tokens":20559,
   "cache_read_input_tokens":20623,"output_tokens":304, … }}}
```

`entrypoint` distinguishes the tiers: `cli` = interactive terminal, `sdk-cli` = headless `claude -p`
(direct or gateway). Throughout this report **total tokens = input + cache_creation + cache_read +
output**; "billable" excludes cache_read, which bills at a reduced rate.

**Telemetry/OTEL:** CLI 2.1.220 exposes only `claude gateway` ("enterprise auth/telemetry"); no
OTEL exporter env vars are present in the installed bundle. **Nothing was enabled.** The transcripts
above are already a complete, exact usage ledger — no new instrumentation is needed to answer this
question, which is why none was added.

### Models in use (7d)

| model | assistant msgs | billable | cache_read |
|---|---:|---:|---:|
| `claude-opus-5` | 12,544 | 78,635,228 | 2,285,387,620 |
| `claude-opus-4-8` | 2,500 | 22,710,555 | 145,192,985 |
| `claude-opus-4-7` | 5 | 260,708 | 384,819 |
| `claude-sonnet-4-6` | 10 | 124,526 | 477,148 |

**Everything runs on Opus.** Not one automated spawn point selects a cheap model, and the single
highest-volume one selects no model at all (§5.1).

### Per-day totals (all spawn points)

| day | assistant msgs | billable | cache_read | output |
|---|---:|---:|---:|---:|
| 2026-07-26 | 1,978 | 11,699,348 | 460,610,370 | 1,799,310 |
| 2026-07-27 | 2,107 | 15,626,706 | 291,056,353 | 1,482,236 |
| 2026-07-28 | 2,006 | 11,528,089 | 321,678,890 | 1,357,198 |
| 2026-07-29 | 2,789 | 17,251,520 | 469,159,452 | 2,268,298 |
| 2026-07-30 | 3,718 | 27,711,984 | 402,660,724 | 2,407,890 |
| 2026-07-31 | 990 | 9,114,997 | 14,482,018 | 41,879 |
| 2026-08-01 | 1,811 | 8,115,190 | 466,492,455 | 1,953,133 |

---

## 3. PER-SPAWN COST PROFILE

### 3.1 Ranking — automated tier (the part nobody asked for)

| spawn point | spawns | total tok 7d | share | tok/spawn | fixed ctx/spawn |
|---|---:|---:|---:|---:|---:|
| **`inbox_agent.translate_ru`** | 4,119 | **113,689,703** | **40.3%** | 27,601 | 30,448 |
| **`main_liveness` LIVENESS ping** | 29 | **79,549,021** | **28.2%** | **2,743,069** | resumes `main` |
| OpenClaw worker subagents (worker1-3) | 19 | 52,951,368 | 18.8% | 2,786,914 | 2,628,298 |
| `lib/screen_sense` (eyes vision) | 137 | 17,192,615 | 6.1% | 125,493 | 130,568 |
| other / unattributed | 9 | 9,947,509 | 3.5% | 1,105,278 | 679,325 |
| `self_improve_daily` | 46 | 4,789,636 | 1.7% | 104,122 | 52,718 |
| `lib/dirigent_brain` | 42 | 1,542,858 | 0.5% | 36,734 | 47,255 |
| `social_x zdravurr(_ca)` | 31 | 1,469,962 | 0.5% | 47,418 | 46,014 |
| gateway transcript-reseed | 7 | 749,471 | 0.3% | 107,067 | 114,558 |
| `fb_social/fb_engage` | 1 | 22,701 | 0.0% | 22,599 | 22,599 |
| **AUTOMATED TOTAL** | **4,440** | **281,904,844** | | | |

24h automated: `translate_ru` 6,580,232 tok / 382 spawns. Everything else automated: **0** (the
daily/cron jobs had not yet run in the window).

### 3.2 Context bloat — what is re-sent unchanged, every spawn

Six `translate_ru` spawns sampled across four different days, each a *separate* session:

```
ts 2026-07-31T07:03:04Z  in=2  cache_creation=11904  cache_read=18546  out=18
ts 2026-07-31T01:45:44Z  in=2  cache_creation=11903  cache_read=18546  out=18
ts 2026-07-31T09:09:46Z  in=2  cache_creation=11895  cache_read=18546  out=18
ts 2026-07-31T02:17:19Z  in=2  cache_creation=11898  cache_read=18546  out=18
ts 2026-07-31T07:37:56Z  in=2  cache_creation=11904  cache_read=18546  out=18
ts 2026-08-01T22:17:05Z  in=2  cache_creation=11902  cache_read=18546  out=11
```

`cache_read` is **byte-identical (18,546) every time**; `cache_creation` varies by ±9 tokens.
**30,448 input tokens are spent to produce 11–18 output tokens — 99.93% of the payload is
unchanged between consecutive spawns.** Because each `claude -p` is a *fresh* session, the prompt
cache is re-created from scratch on every single call and never reused.

Where that fixed payload comes from (`cwd=/home/botuser/.openclaw/workspace`):

| source | bytes | ~tokens |
|---|---:|---:|
| `AGENTS.md` (project instructions) | 64,142 | ~16,035 |
| `memory/ACCOUNTS.md` — injected by SessionStart hook | 43,547 | ~10,886 |
| `memory/STATUS.md` — injected by SessionStart hook | 2,186 | ~546 |
| **total** | **109,875** | **~27,468** |

The hook, `/home/botuser/.claude/settings.json`:

```json
"SessionStart":[{"hooks":[{"type":"command","command":
  "timeout 45 /usr/bin/python3 …/kola_boot_status.py --no-alert --if-stale 600 >/dev/null 2>&1;
   cat …/memory/ACCOUNTS.md …/memory/STATUS.md 2>/dev/null"}]}]
```

So **every** spawn — including 4,139 one-line translations — runs a status script (up to 45 s) and
prepends 43 KB of account data. 7-day cost of re-sending unchanged context for `translate_ru` alone:
**125,141,280 tokens ≈ 744,889 tokens/hour.**

### 3.3 One-shot vs resume

| spawn point | mode | msgs/spawn | median duration |
|---|---|---:|---|
| `translate_ru` | one-shot, fresh session | 1 | <1 s |
| `screen_sense` | one-shot, fresh | 4 | 14 s |
| `dirigent_brain` | one-shot, fresh | ~2 | <1 s |
| `main_liveness` | **resumes `main`** via `openclaw agent` | — | — |
| worker subagents | resumed lanes | ~70 | minutes |

The distinction is the whole story for `main_liveness`: because it *resumes* the accumulated `main`
session, a health-check that asks for **one word** re-loads the entire conversation —
**2,743,069 tokens per ping** (10,996,430 cache_creation + 68,348,818 cache_read over 29 pings).

---

## 4. IDLE BASELINE

Measured live, **not** inferred: a passive sampler (5 s interval, 697 samples) counted every new
Claude Code session created between **2026-08-02T00:25:17Z** and **2026-08-02T01:25:20Z**
(60.0 min). Zero Boss commands and zero Zina commands were issued in the window. This
audit's own session was excluded by session-id.

| metric | measured |
|---|---:|
| wall time | 60.05 min |
| **spawns** | **63** |
| **spawns/hour** | **63.0** (one every ~57 s) |
| input_tokens | 126 |
| cache_creation | 749,753 |
| cache_read | 1,168,398 |
| **output_tokens** | **945** |
| **billable/hour** (in + out + cache_creation) | **750,250** |
| **cache_read/hour** | **1,167,505** |

**All 63 spawns were the same thing** — one prompt, one model:

```
63x  claude-opus-5  'Translate the following chat message to natural Russian. Do …'
```

**This is the entire cost of the system doing nothing.** With no human in the loop the box spends
**~750k billable + ~1.17M cache-read tokens per hour**
to produce **945 tokens of output** — a ratio of roughly
**2,029:1 input-to-output**.
Not one of those 63 spawns had a consumer: `wake()` was refusing the whole time (§5.1), so
every translation was computed and discarded.

Idle vs active, for scale: the quiet overnight hours in §2 sit at a flat **~70 assistant msgs and
~834 k billable tokens/hour**, which matches this measured floor almost exactly (63 spawns ×
~11,922 billable = ~751k). Active hours with the Boss working reach 300–400 msgs and
1.5–2.2 M billable tokens/hour. **The floor is ~40–50% of a busy hour, and 100% of the floor is waste.**

Projected: **18.0 M billable + 28.0 M cache-read tokens per day**, indefinitely,
until the loop is cut.

---

## 5. RUNAWAY DETECTION

Criterion: ≥10 spawns/hour on a near-identical prompt (digits and paths normalised).

### 5.1 🔴 RUNAWAY #1 — `translate_ru`, blocked behind a 5-day emergency stop

`projects/sales/inbox_watcher.py:285` → `projects/sales/inbox_agent.py:823`

| normalised prompt | spawns 7d | worst hour | active hours |
|---|---:|---|---:|
| `…natural Russian:\n\nHello, is this still available?` | 2,087 | 2026-07-31 10 (**38**) | 63 |
| `…natural Russian:\n\nShare your opinion on X.` | 1,412 | 2026-07-31 11 (**39**) | 42 |
| `…natural Russian:\n\nI would like to look at it if you still have it` | 196 | 2026-07-28 20 (**36**) | 7 |
| `…natural Russian:\n\nIs this still available? 😊` | 181 | 2026-08-01 05 (**32**) | 6 |
| `…natural Russian:\n\nAll this for $50? It's true` | 108 | 2026-08-01 21 (**32**) | 4 |
| `…natural Russian:\n\nIs this still available?` | 93 | 2026-08-01 22 (**32**) | 4 |

**Six distinct sentences, 4,139 Opus spawns.** All six exceed the 10×/hour threshold.

**Mechanism — the ordering is the bug.** `route_to_main()` in `inbox_watcher.py`:

```
276     if now - prev < ROUTE_DEBOUNCE_S:      # 90 s per sender
277         log("debounce … пропуск"); return
280     if _routed_seen(route_key, now):       # 7-day dedup — READ ONLY
            return
285     ru = inbox_agent.translate_ru(text)    # 🔴 EXPENSIVE Opus spawn (~30k tok)
…
321     if _ac.wake(MAIN_AGENT, msg, …):       # 🔴 BLOCKED by emergency stop
322         _routed_mark(route_key, now)       # ← dedup mark, NEVER REACHED
```

`_routed_mark()` is deliberately downstream of a successful `wake()` — the code even says so at
line 252: *"⚠️ ТОЛЬКО ЧИТАЕТ. Метку ставит `_routed_mark()` — и ТОЛЬКО после успешного wake()"*.

But `wake()` has been refusing for five days. Live, right now:

```
2026-08-02T00:30:09+0000 [STOP] inbox_watcher: АВАРИЙНЫЙ СТОП (с 2026-07-28T15:10:23Z)
  — НЕ бужу main. Лид не потерян: виден в логе детектора, перечитается после снятия.
```

So the dedup ledger `.kola_state/watcher_routed.json` is **frozen at Jul 28 12:48**, its newest
entry **107.7 hours old**. `_routed_seen()` therefore returns False forever, the 90-second debounce
expires, and the identical message is translated again. Live proof of the loop turning:

```
00:27:51  [fb_sales] PRIORITY mark client pending: <buyer-A>
00:27:57  [offerup]  PRIORITY mark client pending: OfferUp
00:28:38  [fb_sales] PRIORITY mark client pending: <buyer-A>
00:28:41  [fb_sales] debounce (лид уже отдан <90s назад) — пропуск
00:29:19  [fb_sales] PRIORITY mark client pending: <buyer-A>
00:30:01  [fb_sales] PRIORITY mark client pending: <buyer-A>
```

Two senders × one pass per 90 s ≈ **70–80 spawns/hour, indefinitely**.

**The emergency stop is not saving anything.** It gates the free step (waking a local agent) and
leaves the paid step (an Opus call) running ahead of it. Five days engaged ≈ **105 h × ~30,448 tok
≈ 80 M tokens burned and discarded.** This is the class already recorded in memory as
*"постановка стопа ≠ его СРАБАТЫВАНИЕ"* and *"money brakes read a set that could never populate"* —
the same defect, one layer over.

Aggravating factor at the same line: the spawn passes **no `--model`**, so it inherits the account
default — **Opus 5** — for a ten-word translation.

```python
# projects/sales/inbox_agent.py:823
r = subprocess.run(["claude", "-p",
    "Translate the following chat message to natural Russian. "
    "Do NOT add any preamble, quotes, or commentary. Output ONLY the translation:\n\n" + text],
    capture_output=True, text=True, timeout=40, env=os.environ)
```

### 5.2 🔴 RUNAWAY #2 — LIVENESS retry storm

`scripts/main_liveness.py:101`, cron `*/10`. Ceiling is 6/hour; observed **15 spawns in
2026-07-28 00:00** — a retry storm on top of the schedule. Retry markers confirm it:

```
'[Tue 2026-07-28 00:31 UTC] [Retry after the previous model attempt failed or timed out] [LIVENESS] …'
'[Tue 2026-07-28 00:40 UTC] [Retry after the previous model attempt failed or timed out] [LIVENESS] …'
'[Tue 2026-07-28 00:41 UTC] …'   '[…00:50 UTC] …'   '[…00:51 UTC] …'
```

At **2.74 M tokens per ping** (it resumes `main`), that single hour cost ≈ **41 M tokens** to ask
"answer in one word: alive". 7-day total **79,549,021**, from 29 pings.

### 5.3 Not runaways (checked, cleared)

`dirigent_voice.py poll` runs every minute but only reaches `dirigent_brain` on real Boss traffic
(42 spawns/7d). `overload_guard`, `cron_guard`, `promise_tracker`, `fault_realert` are high-frequency
cron but spawn **no** model.

---

## 6. NAMED WASTE LIST

| # | file:line | what | evidence | 7d cost |
|---|---|---|---|---:|
| **W1** | `projects/sales/inbox_watcher.py:285` + `inbox_agent.py:823` | The paid model spawn sits **upstream** of the emergency stop, and the dedup mark sits **downstream** of it → infinite re-translation | `watcher_routed.json` frozen 107.7 h; `[STOP]` in `agent_capacity.log` since 2026-07-28T15:10:23Z; 6 sentences → 4,139 spawns | **113.7 M** |
| **W2** | `scripts/main_liveness.py:101` | Health ping **resumes** `main` instead of a fresh cheap session → 2.74 M tok to return one word; plus retry storm (15/h vs 6/h ceiling) | 29 pings = 79.5 M tok; retry markers 00:31–00:51 Jul 28 | **79.5 M** |
| **W3** | `projects/sales/inbox_agent.py:823` | **No `--model`** → account default Opus 5 for a 10-word translation | transcripts show `"model":"claude-opus-5"`, `output_tokens: 11–18` | (inside W1) |
| **W4** | `/home/botuser/.claude/settings.json` `SessionStart` | 43 KB `ACCOUNTS.md` + `STATUS.md` + a ≤45 s status script injected into **every** spawn, incl. one-line translations | fixed ctx 30,448 tok/spawn, `cache_read` identical at 18,546 | **125.1 M** re-sent (overlaps W1) |
| **W5** | `/home/botuser/.openclaw/workspace/AGENTS.md` | 64 KB (~16 k tok) project instructions loaded per spawn regardless of task size | `stat` 64,142 bytes | (inside W4) |
| **W6** | 8 dead spawn sites (§1.2) | Model-calling code with **0** spawns in 7d — maintenance and audit surface, and a re-activation risk | first-prompt scan over 4,479 transcripts | 0 now |
| **W7** | all automated sites | Every one targets Opus; none targets Haiku/Sonnet. `ogon_post.py:40` is the *only* site that names Haiku — and it is dead | model table §2 | — |

**Top 3 consumers (automated tier, 7d):** `translate_ru` 113.7 M · `main_liveness` 79.5 M ·
worker subagents 53.0 M.

---

## 7. SCOPE NOTE — a second, metered billing path exists

The brief states consumption is subscription-only, via CLI spawns. That is true of OpenClaw. It is
**not** true of the whole box, so recording it here rather than folding it into the numbers above:

`/root/titan-bot/.env` and `/mnt/volume_nyc1_1780480650620/mercury-sol/.env` each hold a **populated
`ANTHROPIC_API_KEY` (`sk-ant-api0…`, 110 chars)**, used through the Anthropic SDK — real metered
API billing, invisible to subscription limits and to the transcripts parsed above:

- `titan-bot/claude_advisor.py:242` — `client.with_options(timeout=10.0).messages.create(model='claude-haiku-4-5-20251001', max_tokens=800)`
- `titan-bot/news_sentiment.py:113` — `messages.create(…, max_tokens=600)`
- `titan-bot/macro_filter.py:262` — `messages.create(…, max_tokens=250)`
- `mercury-sol/claude_advisor.py:222`, `news_sentiment.py:117`, `macro_filter.py:278` — same shape

These are on **Haiku** with tight `max_tokens` — the most disciplined LLM usage on the box. Live
firing evidence, `journalctl -u titan.service`:

```
Jul 31 14:15:11 titan[481839]: [TITAN] [EXIT-ADVISOR-LIVE] trigger=15m_exit_confirm … conf=0.72
Jul 31 16:25:40 titan[481839]: [TITAN] [EXIT-ADVISOR-ACT] vpos=90 … CLOSING at market
```

They do **not** consume subscription limits and are **not** counted anywhere in this report. Worth a
separate cost pass against the Anthropic console.

---

## 8. PROPOSED FIXES — NOT APPLIED

Nothing in this audit changed behaviour. Proposals, ranked by saving:

| # | fix | file:line | expected saving |
|---|---|---|---:|
| **P1** | Move `translate_ru()` to **after** the successful `wake()`, or mark `_routed_mark()` when the stop is what blocked delivery. A blocked stop must block the *paid* step first. | `inbox_watcher.py:285` vs `:321` | **~113 M tok/7d (~16 M/day)** |
| **P2** | Memoise translations on a hash of the source text (six sentences → six calls, not 4,139). Survives P1 as defence in depth. | `inbox_agent.py:815` | ~99.9% of residual |
| **P3** | Add `--model claude-haiku-4-5-20251001` to the translate spawn. A 10-word translation does not need Opus. | `inbox_agent.py:823` | ~90% of unit cost |
| **P4** | Give the liveness ping a **fresh** minimal session instead of resuming `main`; cap retries. | `main_liveness.py:101` | **~79 M tok/7d** |
| **P5** | Scope the `SessionStart` hook to interactive sessions only (skip when `entrypoint=sdk-cli`), so one-line spawns stop paying 27 k tokens of account data. | `/home/botuser/.claude/settings.json` | ~11 k tok × every automated spawn |
| **P6** | Split `AGENTS.md` so headless spawns load a small operational subset. | `AGENTS.md` | ~16 k tok/spawn |
| **P7** | Delete or quarantine the 8 dead spawn sites. | §1.2 | 0 now; removes re-activation risk |

Combined, **P1+P4 alone remove ~193 M of the 282 M automated tokens per 7 days — 68% of everything
the system spends without being asked.**

---

## 9. METHOD & LIMITS

- Source: 4,479 Claude Code transcripts touched in 7 d, both `/root/.claude` and
  `/home/botuser/.claude`. Parser: `analyze.py` / `final.py` (session-level, first-prompt attribution).
- `total tokens = input + cache_creation + cache_read + output`. `cache_read` bills at a reduced rate,
  so token totals are **not** linear in cost; they are reported separately throughout.
- Attribution is by first user prompt, with a provenance fallback (`entrypoint`, `cwd`) for sessions
  no fingerprint matched. An earlier pass mis-binned 1.43 B interactive tokens as "unattributed";
  corrected before publication.
- Buyer names in log excerpts are redacted (`<buyer-A>`).
- This audit's own session (`3386abce`, ~14.7 M tokens) is included in the interactive tier and is
  itself part of the 7-day total.
- One `find -newermt "7 days ago"` invocation silently returned 0 against files modified minutes
  earlier; all windowing was redone with explicit mtime comparison.
