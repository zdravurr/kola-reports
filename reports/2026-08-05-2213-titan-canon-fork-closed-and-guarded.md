# TITAN — THE CANON FORK IS CLOSED, AND THE CAUSE WAS NOT THE ONE ANYONE NAMED, INCLUDING ME

**2026-08-05 22:13 UTC · canon repaired at HEAD `2ed2cef` · guard built, proven, and already vindicated**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
No trading code touched: this pass changed `reports/OPEN-ITEMS.md` and added one read-only tool.
**Mercury-SOL never opened.**

Parent: `2026-08-05-2150-titan-mfe-tracker-lifted-out-with-coverage-contract.md`.

---

## §1 — 🔴 DIAGNOSED BY GIT, AND THE ASSUMED CAUSE IS FALSE. MINE WAS TOO.

The brief's hypothesis — and my own §0.0 note at 21:50 — said the 2026-07-30 pattern had recurred:
*"the canonical file froze while all live text went into dated snapshots."* **Git says that is not what
happened.**

| claim | what git shows |
|---|---|
| the canon froze on 2026-07-30 | 🔴 **FALSE.** **50 writes** to `OPEN-ITEMS.md`. Per day: 07-26 ×6 · 07-27 ×6 · 07-29 ×5 · 07-30 ×10 · 08-01 ×2 · 08-03 ×5 · **08-04 ×15** · 08-05 ×1 |
| snapshots are the truth, canon is a stale copy | 🔴 **FALSE.** Canon at `b43a1be` (2026-08-04 19:53:07) is **byte-identical** to `2026-08-04-1955-open-items.md` apart from that file's own 8-line banner — **and the banner states it was generated from the canonical copy** |
| so the 30.07 fork is still open | 🔴 **NO — it was closed by 2026-08-03.** Snapshots were being generated FROM the canon; one 08-04 commit message even reads *"canon and dated snapshot in one commit"* |

🔴 **I ASSERTED THE WRONG DIAGNOSIS AT 21:50 AND THE CORRECTION IS THE POINT OF THIS SECTION.** I wrote
*"the dated snapshots remain the live truth"* — **from memory, not from git.** The memory
(`project_openitems_canonical_fork_30jul`) described 2026-07-30 accurately and I carried it forward as
present tense. **That is the same defect this pass is about: a summary that was true once, asserted as
current.** §0.0 now carries the correction rather than the error.

### WHAT ACTUALLY BROKE — TWO THINGS, AND THE SECOND IS THE REAL ONE

**1. A one-day maintenance lapse.** Six Titan commits landed on 2026-08-05 and produced dated reports
but no canonical section: `946fe74 → 1ec2477 → de1d0f2 → ece910d → 7472729 → 7a4169b`.

**2. 🔴 SUMMARY BLOCKS ARE NOT REFRESHED BY BODY WRITES.** The header's HEAD field and the
current-state flag table went stale **while the body was edited fifteen times on 2026-08-04.**

**A lapse is visible — nothing new appears. A stale summary sitting on a freshly-written body is
invisible and authoritative.** That is why item 2 matters more than item 1, and why the fix is a
machine check rather than a resolution to be more careful.

---

## §3 — THE SWEEP: WHAT THE STALE SUMMARY WAS TELLING A FRESH SESSION

*(Reported before the fixes, as asked.)*

| stale claim | canon said | runtime | severity |
|---|---|---|---|
| 🔴 `SL_ATR_MULT` / `TRAIL_MULT_ATR` | **2.5 / 2.5** | **2.25 / 1.6875** | 🔴 **SEVEREST — a reader computes 1R WRONG.** §2.53 documents the real geometry **250 lines below in the same file** |
| header `HEAD` | `44731be` | `7a4169b` | **12 commits** stale |
| `AI_ADVISOR_HIDE_1H` (table **and** §body prose) | True | **False** | flag inverted |
| `EQH_EQL_SMART_TP_ENABLED` (table **and** §2.6's premise) | True | **False** | flag inverted |
| `EXCURSION_SAMPLE_SEC` | 60 | **10** | study method note |

**Verified CORRECT and left alone:** `LIVE_TRADING_ENABLED` / `ORDER_ADAPTER_LIVE` True/True ·
`CONFLUENCE_SCORE_THRESHOLD` 3.0 · `CONFLUENCE_FLAT_THRESHOLD` 5.0 · `EXIT_ADVISOR_DRYRUN` False ·
`MAX_POSITIONS_PER_SIDE` 1 · `RECHECK_TIERS_SEC` [10,60,300] · `LONG_PARTIAL_FRACTION` 1/3.

⚠️ **AND MY SWEEP'S OWN FALSE-POSITIVE RATE, RECORDED BECAUSE IT WILL MATTER NEXT TIME.** A regex over
`NAME = value` flagged **14** candidates. **Six were legitimate text, not staleness:**

- *"Rollback is `LIVE_TRADING_ENABLED = False` + `ORDER_ADAPTER_LIVE = False`"* — a **rollback
  instruction**, correct as written
- *"kill switch `EXIT_ADVISOR_DRYRUN = True`"* — an **instruction**, correct
- *"Rollback: `EMA_ENVELOPE_GATE_ENABLED = False`"* — same
- `LONG_PARTIAL_FRACTION = 1/3` — my regex read `1`, runtime is 0.3333…, **the doc is right**
- two file-path references (`DXY_HALT_DRYRUN … risk_manager.py`) misparsed as values

**Only 8 of 14 were real. A checker that cannot tell an assertion from an instruction cries wolf, and
a sweep reported as "14 stale claims" would have been false.** Every hit was read in context.

---

## §2 — THE CANON IS REBUILT AND CURRENT AT HEAD `2ed2cef`

| change | detail |
|---|---|
| **§0.0 corrected** | the wrong fork diagnosis replaced by what git shows; **kept at the top, as instructed**, with the "silence is not a fault" content intact |
| **header refreshed** | HEAD + a line stating every value was re-read **by importing `config` at runtime in this pass**, not copied forward |
| **§2.57 added** | the six 2026-08-05 commits, in order, with the load-bearing part of each — the unsatisfiable wall rule and the corrected nearest-wall baseline (**53.8% / median 48.4th supersedes 70.2% / median 29th**); the three removed falsehoods; the four newly-countable refusals **and** that the breakeven loop was *not* stopped because it carries both observatories; the unrankable-book warning; the MFE lift-out with its coverage contract |
| **§2.58 / §2.58a added** | the fork diagnosis above, the sweep, the false-positive rate, and the prevention |
| **4 table rows + 3 in-body premises fixed** | corrected **with dated annotations**, not silently rewritten — the old value stays visible as history |

**Also recorded in §2.57: the day's read-only findings** — the exit advisor **does** read drawdown
(r = −0.398/−0.504, survives §2.54's control, the first thing in this book that has) and position age
has been in the prompt since `ef7fa10`; the mechanical time-tier is worse than doing nothing in **51 of
52** cells; **15 of 16 Fibonacci levels are numerically identical to their neighbours**; and the
nineteenth dead branch — walls are **eaten 95% within 24h** and the veto's drift is **zero under day
clustering**.

---

## §4 — 🔴 PREVENTION: ONE HALF IS BUILT AND ONE HALF IS NOT, AND I AM NOT GOING TO BLUR THEM

### BUILT — `titan-bot/tools/openitems_guard.py`, commit `2ed2cef`

Re-reads the two things that cannot lie — `git rev-parse --short HEAD` and **`import config`** — and
exits non-zero on any disagreement with what the canon asserts.

🔴 **It reads ONLY between `<!-- RUNTIME-STATE:BEGIN -->` / `<!-- RUNTIME-STATE:END -->` markers, and
that fence exists because the guard's first run was WRONG.** It flagged four mismatches — by matching
my own §2.58 table, which necessarily *quotes* the stale `2.5 / 2.5` in order to document it. **A
document that records a defect must cite the wrong old value; a guard that cannot tell a citation from
an assertion flags the very section that fixes the problem.** The fence makes "this block asserts
present state" explicit instead of inferred. **A missing fence is itself a failure** — the guard exits
1 rather than silently checking nothing.

**PROVEN LOAD-BEARING, NOT MERELY GREEN:**

| scenario | guard |
|---|---|
| repaired canon | ✅ exit 0 |
| header HEAD reverted to `44731be` | 🔴 exit 1 — caught |
| geometry row reverted to `2.5 / 2.5` | 🔴 exit 1 — caught (both constants) |
| `AI_ADVISOR_HIDE_1H` row reverted to True | 🔴 exit 1 — caught |
| fence removed entirely | 🔴 exit 1 — caught |

### 🔴 AND IT VINDICATED ITSELF WITHIN A MINUTE OF EXISTING

**Committing the guard advanced HEAD from `7a4169b` to `2ed2cef` — which instantly made the canon's
freshly-written header stale. The guard's next run refused it.** The defect diagnosed in this pass
recurred inside sixty seconds and was caught inside sixty seconds. **That is the argument for a machine
check over a discipline, demonstrated rather than asserted.** The canon now reads `2ed2cef` and the
guard passes.

### NOT BUILT — AND IT WAS RECORDED ON 2026-08-01 AND IS STILL OPEN

🔴 **The publisher does not call the guard. Snapshot generation is manual — a human copies the canon to
a dated path.** Nothing in the pipeline refuses to emit a snapshot whose header disagrees with runtime.

**Plainly, in the words the brief asked for: it will fork again unless a publisher refuses to emit a
snapshot whose header disagrees with runtime.** The guard makes that refusal *possible* and cheap — one
call, honour the exit code — but until something in the emit path invokes it, **this is a discipline
with a helper, not a mechanism. And discipline is exactly what failed on 2026-08-04 while the body was
being written fifteen times.**

⚠️ **What I did NOT do:** wire it into `report_publish.py`. That file lives in the OpenClaw workspace
behind a commit gate, serves both bots and every report type, and emitting Titan-specific policy from it
is a design decision with its own blast radius — not something to bolt on at the end of a session.
**Named as the next step rather than half-done.**

### THE PRACTICE, RESTORED AND DEMONSTRATED THIS PASS

`reports/2026-08-05-2213-open-items.md` was **generated FROM the canon, and only after the guard exited
0** — body **byte-identical**, verified by `diff` (0 lines) and matching md5. **The direction of
generation is canon → snapshot, and the gate ran before the copy.**

---

## LIVE STATE

| | |
|---|---|
| titan-bot HEAD / `git status` | **`2ed2cef`** / **clean** |
| canon asserts HEAD | **`2ed2cef`** — machine-checked |
| guard | `python3 /root/titan-bot/tools/openitems_guard.py` → **exit 0** |
| open positions | **0** |
| trading code changed this pass | **none** — one read-only tool added, no gate, geometry, prompt or flag touched |
| ⏳ stored prompt with per-wall percentiles | **still none** — last consultation 16:40:10 UTC; per §0.0 this is confluence not firing, not a fault |
