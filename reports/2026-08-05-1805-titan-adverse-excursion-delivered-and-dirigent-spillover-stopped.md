# TITAN — THE 17:25 ADVERSE-EXCURSION REPORT IS COMPLETE AND VERIFIED; AND THE DIRIGENT SPILLOVER IS STOPPED AT ITS SOURCE

**2026-08-05 18:05 UTC · HEAD `b9081ad` (titan-bot UNCHANGED, `git status` clean, 0 open positions)**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
Mercury-SOL never opened.

This session did **two** things and neither of them touched the trading bot:
1. **Found, verified and delivered** the time-conditioned adverse-excursion report that the previous
   session finished at 17:25 and never got a link out for.
2. **Killed the `fault_prom_promise_*` spillover** at its source — one commit, `f2a5282`.

---

## §0a — THE ADVERSE-EXCURSION REPORT: **IT WAS FINISHED, NOT A STUB**

**`reports/2026-08-05-1725-titan-time-conditioned-adverse-excursion.md` — 527 lines, committed,
pushed, and live on GitHub (HTTP 200).** The repo was already `0` commits ahead of `origin/main`;
what never happened was the **delivery**. The box died between publication and the Telegram message.

🔴 **Full report:**
https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-05-1725-titan-time-conditioned-adverse-excursion.md

### I did not take it on trust. Every load-bearing claim was re-checked against the live system:

| the report claims | re-checked now | verdict |
|---|---|---|
| 118 stored exit consultations | `SELECT count(*) … status='exit_ai_dryrun'` → **118** | ✅ |
| age on **118 of 118** prompts | `… AND ai_user_prompt LIKE '%Elapsed:%'` → **118** | ✅ |
| `claude_advisor.py:686` renders age | line 686 is verbatim `f"  Elapsed: {g('elapsed_h','.1f')}h\n"`, third line of the **Position** block, directly under `Unrealised: …R` | ✅ |
| age shipped in `ef7fa10`, 2026-07-26 | `git log -1 ef7fa10` → *"…wire the exit advisor in DRYRUN"*, **2026-07-26 22:09:27 +0000** | ✅ |
| all three recheck tiers inside 5 min | `config.py:822` → `RECHECK_TIERS_SEC = [10, 60, 300]` | ✅ |
| the advisor is ACTING, hourly | `config.py:278` `EXIT_ADVISOR_DRYRUN = False`; `:281` `EXIT_ADVISOR_HOURLY_SEC = 3600` | ✅ |
| last consult 2026-08-04 00:26 | `MAX(timestamp)` → **2026-08-04 00:26:02** | ✅ |
| 0 open positions | **0** | ✅ |

**Nothing was found to correct.** The report stands as written.

### WHAT IT SAYS, IN FOUR LINES

1. 🔴 **§1 — the advisor is NOT blind to drawdown; it is the strongest relationship in the book.**
   `close` rate **95 % below −0.5R vs 25–27 % around flat** (r = **−0.398**, perm-p < 0.0001; on the
   clean subset **−0.504**). `giveback_r` stronger still (r = **+0.533**). **It survives the §2.54
   regime control on the 90-consult stratum** — the first thing in this book that has.
2. 🔴 **§1d — the prompt has carried position age since the exit advisor's first commit.**
   `Elapsed: {h}h`, 118/118, quoted back in **25** reasons. **The brief's structural premise —
   "there is nobody to ask" — is wrong on this point, and it is the load-bearing correction:**
   §3's second branch was asking for a fact that shipped on 2026-07-26.
3. 🔴 **§2/§2e — the mechanical tier is worse than doing nothing in 51 of 52 cells.** The one
   positive cell (+0.154R) **loses on LONG** (−0.913R), has a bootstrap CI of **[−8.10, +7.01]R**,
   and closes **11 eventually-profitable positions worth +8.892R**. Its threshold is **inert** — by
   hour 12 every surviving position is already >1.5 ATR adverse, so it selects nobody. **It is a
   pure time stop, and the operator's own §2c objection is the entire result.**
4. 🔴 **§2e — 15 of 16 Fibonacci levels are numerically identical to their plain decimal
   neighbours** (same positions, same n, same R). **The numbers carry nothing.** And the
   move-normalised form **loses to the ATR form** by +2.567R at each one's own best cell.

**§3's third branch fired: NEITHER SURVIVES. No diff, for either branch.**

⚠️ **And the limit that governs all of §2:** the clean book is **40 positions, ALL of them on the
old side of the 17:01:29 1R boundary — zero on the current SL-2.25/trail-0.75R geometry.** The brief
asked for the correct side or a per-era split; **the correct side is empty.** Any rule fitted there
is fitted to a machine retired on 2026-08-04.

---

## §0b — 🔴 THE SPILLOVER: WHERE IT CAME FROM, AND IT IS STOPPED

### ORIGIN, IN ONE LINE

**`promise_tracker.py:295` → `fault_realert.register("prom_<id>")` → `_emit` → `notify_boss(text,
task="fault_prom_promise_…")`** — the Dirigent's escalation ladder for Marketplace/Facebook listing
promises, calling the **bots' report sender**.

### IT WAS NOT ONE LEAK, IT WAS THREE — AND THE THIRD IS WHY IT MULTIPLIED

| # | mechanism | effect |
|---|---|---|
| 1 | `ensure_report_link()` judges the text **substantial** — an alert has ≥8 newlines — and publishes it as a **dated file in kola-reports**, the public repo of BOT reports | the files the operator kept opening by hand |
| 2 | the **02.08 order** forces `channel='kolya'` for everything | the alert lands in the Titan/Mercury-SOL Telegram channel |
| 3 | 🔴 **AMPLIFICATION** — an alert delivered without a link is caught by `report_outbox.watchdog()`, which shouts *"REPORT DELIVERED WITHOUT A LINK"* **through this same `notify_boss`**, publishing **yet another file** | **one alert = up to three artifacts.** This is the 17:35 stub listing five more |

### THE TWO ORDERS DO NOT CONFLICT ONCE THE CLASS OF TRAFFIC IS NAMED

The 02.08 order — *"ALL reports go to Kolya's channel ONLY"* — is about **reports**, and its stated
reason was that the Boss reads Kolya's channel and splitting reports across two chats hides half of
them. **A Dirigent reminder about an unposted listing is not a bot report.** The 05.08 order is
explicit: this channel carries **Titan and Mercury-SOL only**. Both hold.

### THE CHANGE — `f2a5282`, `lib/notify.py`

A single gate at the top of `notify_boss`, **before publication and before routing**, keyed on
`task` starting with `fault_` — because that prefix is set in **one place** (`fault_realert._emit`)
and does not depend on how any individual fault is worded:

- **NOT published to kola-reports.** `ensure_report_link` is skipped entirely.
- **Archived to disk first, outside every repo:** `/mnt/volume_nyc1_1780480650620/dirigent-alerts/`.
- **Delivered by direct `dirigent_channel.send`** → **@Derizherrr3_bot** — the path the 02.08 order
  deliberately left open for the Dirigent's own voice, bypassing `cp.report` (which forces `kolya`
  and would loop).
- 🔴 **FAIL-CLOSED, DELIBERATELY.** Dirigent channel down → we do **NOT** fall back to Kolya's
  channel; that is the spillover being removed. The alert is **already on disk** and the failure is
  logged loudly. This is the same choice already written into the branch below it — *"otherwise we
  mix the blast radii again."*

**Leg 3 dies with leg 1:** fault alerts no longer enter the outbox ledger, so they can never again
become "linkless deliveries" for the watchdog to shout about.

### VERIFIED LIVE, AS `botuser`, THROUGH THE REAL PATH — NOT BY READING THE DIFF

| check | result |
|---|---|
| two `fault_prom_promise_*` alerts pushed through the real `notify_boss` | **delivered to @Derizherrr3_bot**, return `dirigent-alert` |
| Dirigent channel bound and alive before routing money alerts to it | `chat_id 6284337254`, live send **True** — checked **first**, so nothing was routed into a dead chat |
| archived to disk | `/mnt/…/dirigent-alerts/2026-08-05-1759-fault_prom_promise_TESTROUTE2_0805.md` |
| 🔴 **kola-reports HEAD** | `85f3637` **before and after — unchanged** |
| 🔴 **kola-reports file count** | **887 before, 887 after** |
| test artifacts removed afterwards | archive dir clean |

⚠️ **One thing I got wrong and fixed rather than shipped.** The first live test delivered fine but
returned `архив: None` — **botuser could not create the archive directory.** That is precisely the
trap already recorded in `report_publish.py`: *"automation that lacks permissions is not
automation."* Directory created `botuser:botuser 755`, re-tested, archive path returned. **Had I
verified by reading the diff instead of running it, this would have shipped as a silent hole.**

⚠️ **And the commit itself was blocked** — `lib/notify.py` is a protected path behind a commit
gate. Taken through the authorized token route, not around it. The gate's own alert is a legitimate
report and stays in this channel.

---

## WHAT DID NOT CHANGE

`titan-bot` is at **`b9081ad`**, `git status` **clean**, **0 open positions** throughout. `trades.db`
opened **read-only**. **Mercury-SOL was never opened.** No trading logic, config, threshold, prompt
or schema was touched in this session — the only commit is to the Dirigent's notification routing,
in a different repo, on a machine path Titan does not import.
