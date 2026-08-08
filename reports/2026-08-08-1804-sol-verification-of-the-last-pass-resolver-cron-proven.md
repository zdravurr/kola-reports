# sol-verification-of-the-last-pass-resolver-cron-proven

_2026-08-08 18:04 UTC_

---

# Mercury-SOL — verification of the last pass. The resolver survives cron. Two corrections to my own 17:20 register.

**The resolver runs clean under a completely empty environment — exit 0, venue read, DB and `.env`
resolved by absolute path. Idempotent, twice in the same minute. Tomorrow's 08:19 is safe.**

🔴 **Two corrections to what I told you at 17:20, both found by checking rather than recalling:**
**(1) the pending-restart set is FIVE files, not three** — the 17:47 pass added two more.
**(2) the `.pyc` files are no longer evidence of what is loaded**, because my own `py_compile`
regenerated them after each edit.

**Every traded value in the running worker is still identical to disk — reconstructed from the exact
sources it loaded, not from the contaminated `.pyc`.** vpos 29 untouched, Titan untouched, nothing
changed by this pass.

Prior: [close-of-session 17:20](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1720-sol-open-items-close-of-session.md) · [last pass 17:52](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-08-1752-sol-naked-alerts-resolved-on-evidence-be-decided-reason-is-narration.md)

---

## 1. THE RESOLVER'S FIRST UNATTENDED RUN

### (a) The entry, exactly as installed

```
19 8 * * * /usr/bin/timeout 120 /usr/bin/python3 \
           /mnt/volume_nyc1_1780480650620/mercury-sol/naked_alert_resolver.py \
           >> /var/log/mercury_sol_naked_alert_resolver.log 2>&1
```

- **interpreter**: `/usr/bin/python3` → `python3.12`, **absolute** — immune to cron's thin `PATH`.
- **working directory**: cron sets cwd to `HOME` = `/root`. The script never relies on cwd; every
  path in it (`DB_PATH`, `ENV_PATH`, the `sys.path` insert) is absolute.
- **environment**: the crontab declares **no** `SHELL`/`PATH`/`HOME`/`MAILTO`, so cron defaults
  apply (`/bin/sh`, `PATH=/usr/bin:/bin`, `HOME=/root`).
- **output**: stdout **and** stderr appended to a log. The file does not exist yet; `>>` creates it
  on first run.
- **wrapper**: `timeout 120`, matching the digest's own guard — a hung Tor read cannot overrun into
  the 08:20 slot.

### (b) 🔴 RUN AS CRON WILL — IT PASSES, INCLUDING THE STRICT FORM

```
$ cd /root && env -i HOME=/root LOGNAME=root PATH=/usr/bin:/bin SHELL=/bin/sh PWD=/root \
      /usr/bin/timeout 120 /usr/bin/python3 …/naked_alert_resolver.py
[2026-08-08T17:58:07Z] naked_alert_resolver starting
  venue: LONG: size=0.9 sl=74.95 | SHORT: size=0.0 sl=NONE
  unresolved alerts: 0
  resolved 0; still unresolved: 0
EXIT=0

$ cd /root && env -i /usr/bin/python3 …/naked_alert_resolver.py      # nothing at all
… same output …
EXIT=0
```

It resolved `.env`, the DB path **and** built a working exchange handle over Tor with an empty
environment. This is the test the digest faced on 2026-08-06; the resolver has now faced it too,
and in the stricter form.

### (c) If it exits non-zero at 08:19

**The digest still runs.** They are two independent cron entries; cron does not chain them and has
no notion of one depending on the other. The 08:20 digest fires whatever the 08:19 exit code is.

**Would anyone know? No — and this is the residual.** `MAILTO` is unset *and* both streams are
redirected to a log, so cron emits no mail. Nothing watches the job; grepping the tree for a
watchdog on it returns only my own canon comments.

**But the failure degrades safely, which is the important half:**

```
alerts: total=5  resolved=5  unresolved=0
```

`resolved=1` is persistent, so an outage **cannot un-resolve** anything. Its only effect is that a
**new** alert stays unresolved — which is exactly the correct, pre-fix behaviour: an unproven alert
should shout. So a resolver outage cannot create a phantom, only fail to clear a real one.

🔶 **Named as a residual, not fixed:** a silent resolver outage is invisible until an alert happens
to need clearing. The cheap remedy is a heartbeat line the digest could assert on ("resolver last
ran at…"). Not built — it is a new mechanism and you scoped this pass to verification.

### (d) Idempotent — proven twice in the same minute

The two runs above are `17:58:07` and `17:58:09`, same minute, both `unresolved 0 · resolved 0 ·
exit 0`. A third live run at 17:49 gave the same. It performed **no writes** — there was nothing to
resolve.

---

## 2. THE PENDING-RESTART SET — 🔴 TWO CORRECTIONS

### (a) It is FIVE files, not three

My 17:20 register said config.py, trail_arm.py, virtual_trader.py. That was true **at 17:20**. The
17:47 pass added two more. The full set, disk newer than the worker's 16:08:59 start:

```
PENDING (loaded by the bot)      config.py        16:51:55
                                 virtual_trader.py 16:51:55
                                 trail_arm.py      17:47:11
                                 claude_advisor.py 17:47:11   <- NEW since 17:20
                                 skip_attribution.py 17:47:11 <- NEW since 17:20

NOT pending (not loaded by the bot)
  naked_alert_resolver.py  17:47:11  — standalone, cron re-reads it each run
  silence_digest_sol.py    17:47:11  — standalone, cron re-reads it each run
```

The two new entries are **comment-only** (the `ai_reason` canon and its pointer), so the
zero-behaviour claim extends to them unchanged — but the *count* I gave you was stale and you asked
for exactness.

### (b) 🔴 THE `.pyc` FILES ARE NO LONGER EVIDENCE — and every traded value is still identical

A methodological correction worth recording, because the obvious check now gives the wrong answer:

```
module            .pyc says source was   source is now       "match"
config            16:51:55               16:51:55            YES
trail_arm         17:47:11               17:47:11            YES
virtual_trader    16:51:55               16:51:55            YES
```

Every `.pyc` agrees with disk — **and that proves nothing**, because my own `py_compile` after each
edit regenerated them. They post-date the worker's 16:08:59 start, so they describe the *edits*, not
the *memory*. Anyone using `.pyc` mtime as a deployment check here would conclude the bot is current
when it is not.

**The sound reconstruction** is the backups the worker actually loaded
(`*.bak_beseparation_20260808_165135`, whose contents are the disk state at 16:08:59):

| | RUNNING worker | disk (pending) | identical |
|---|---|---|---|
| `breakeven_target(74.80, LONG)` | 74.9496 | 74.9496 | ✅ |
| `breakeven_target(74.80, SHORT)` | 74.6504 | 74.6504 | ✅ |
| `activation_distance(74.80, 0.364)` | 0.9100 | 0.9100 | ✅ |
| `compute_initial_sl` LONG | (73.89, fallback_atr) | (73.89, fallback_atr) | ✅ |
| `compute_initial_sl` SHORT | (75.71, fallback_atr) | (75.71, fallback_atr) | ✅ |
| `MIN_PROFIT_DISTANCE_PCT` | 0.0015 | 0.0015 | ✅ |
| `_BE_TARGET_FRAC_ON` | 0.0020 | 0.0020 | ✅ |
| **vpos 29 stored `sl_price`** | **74.9496** | — | matches both |

**Nothing differs. The "zero-behaviour" claim is correct, and you do not need to act tonight.**

### (c) The one display-only divergence, restated

If an orphan adoption happened **before** the next restart, `_adopt_card` in the running process
would print the old formula string `fill*(1+0.0015+0.0005)` while computing the same 0.0020 target
and the same price. Display only. **It remains the only divergence** — the two files added to the
pending set are comment-only and introduce no second one.

---

## 3. vpos 29 — THE ONLY LIVE MONEY

### (a) Venue vs row

| field | VENUE | ROW (vpos 29) | |
|---|---|---|---|
| size | 0.9 | 0.9 | ✅ |
| entry | 74.8 | 74.8 | ✅ |
| stop | **74.95** | **74.9496** | ✅ tick rounding only (0.0004, in the bot's favour) |
| openTime / opened_at | 1786179014459 | 2026-08-08T08:50:14.459Z | ✅ same instant |
| mark / uPnL | 76.33 / +1.377 | — | |
| curRealisedPnl | +0.4853476 | — | |

**One conditional order, and it is the original:**

```
orderId 671eee37-1308-4efd-9fca-fd3586743e1e   Untriggered   trigger 74.95   qty 0.9   idx 1
createdTime 1786179014843 = 2026-08-08 08:50:14.843 UTC
```

**The same order id it has carried since 08:50:14.843** — modified in place at the partial and at
the BE lock, never cancelled and recreated. No orphan stop has ever existed on this position.

### (b) Has the trail moved the stop? No.

```
sl_price at the BE lock (15:40:50) : 74.9496
sl_price now                        : 74.9496      -> the trail has NOT moved it
water_mark at adoption (seeded)     : 74.80
water_mark now                      : 76.46        -> the engine has been tracking the high
trail_pct                           : 0.909%
trail fires at last <= 76.46 x (1 - 0.00909) = 75.7650   (mark now 76.33)
```

The seeded water mark was overtaken on the first tick, exactly as designed.

### (c) What will close it, in order of likelihood

1. **THE TRAIL — most likely.** Trigger 75.7650 against a 76.33 mark: a **−0.74%** retrace. The
   trail trigger sits **above** the BE stop (75.7650 > 74.9496), so the trail binds first and the
   BE stop is now only a backstop.
2. **The exit advisor / a 5m exit signal.** Needs a bearish Group-B webhook; unpredictable but
   entirely possible overnight.
3. **The venue stop at 74.95 — least likely, and it is the backstop.** It needs **−1.81%**, and it
   only beats the trail if price gaps through 75.765 between poller ticks (~13 s) or during an
   outage. That is precisely the job it should have.

**🔴 Is the exit advisor reachable for a position that was ADOPTED, not entered? YES — and the
reason is structural.** `_handle_5m_close` resolves the position with `_fetch_position_state`, i.e.
**it reads the VENUE, not `virtual_positions`**. Adoption is irrelevant to its arming.

**And the settlement path is armed too.** After any venue close, the engine's external-close
detection (`virtual_trader.py:1635-1657`) sees `_live_pos_state → FLAT`, books the close from the
real fill via `_live_book_close`, and takes the close reason from the venue's own exit type. That
path needs only `is_paper=0` and the registered live adapter — both present.

**Nothing adoption left NULL sits on any exit path.** The NULL `entry_wall_baseline_mult` /
`entry_adx_1h` / `entry_atr_pct_1h` feed **only** the post-entry recheck, which adoption closed with
`recheck_status='done'`. No exit route reads them.

---

## 4. 🔴 THE SHORT PATH — WHICH OF THE THREE MORNING FIXES IT ACTUALLY EXERCISES

The LONG side is occupied by vpos 29, so tonight's only possible entry is a SHORT. The entry gate is
keyed `(symbol, position_side)` — **per side** — so vpos 29's LONG does not hold the SHORT gate.
SHORT is otherwise clear: cap passes (0 contracts), 0 live closes today so the daily-loss brake has
nothing to bite on, timeout disabled.

| fix | exercised by a SHORT entry? | why |
|---|---|---|
| **1. the fill read** (`fetchOrder` `acknowledged` on Unified) | ✅ **FULLY** | the option is set on the exchange **object**, so `_read_entry_fill` uses it on any live entry regardless of side. This is the one that has never fired in a live entry, and a SHORT would close it. |
| **2. `34040` counted as success** | ⚠️ **NOT at entry** | a fresh SHORT's first stop-set is a **new** value → `retCode 0`. `34040` only arises when the *same* value is set twice. It **is** exercised later, on the poll's stop-resync once the SHORT is open — the same path that fired for the LONG at 16:09:18. **It is already proven in production; a SHORT is not needed for it.** |
| **3. the entry in-flight gate** | ⚠️ **PARTIALLY** | acquire/release runs on every entry, so the happy path is exercised. The **refusal** branch needs **two concurrent SHORT webhooks in the same second** — the exact race of 06:50 and 08:35. A single SHORT cannot produce it. |

**So the honest answer: a SHORT tonight would fully prove fix 1, would not prove fix 3's refusal
branch, and does not need to prove fix 2 — that one is already proven.** Fix 3 stays unproven until
TradingView sends two same-side signals in one second again, which is not something we can schedule.

---

## STATE — nothing was changed by this pass

```
mercury-sol   active  pid 3533821 / worker 3533987  since 16:08:59  NRestarts=0  0 tracebacks
              HEARTBEAT ticks=495 open=1 mode=LIVE, ~13s cadence (steady)
vpos 29       0.9 @ 74.80 · sl 74.9496 · open · wm 76.46 · partial 0.4 @ 76.36 — IDENTICAL
venue         LONG 0.9 · stop 74.95 · orderId 671eee37 since 08:50 · SHORT flat
alerts        5/5 resolved · 0 unresolved · digest will read zero
cron          19 8 resolver (proven under env -i) · 20 8 digest (unchanged)
pending       5 files await a flat-book restart — all comment-only or proven zero-behaviour
titan         active · pid 2538048 · NRestarts=0 · HEAD 897850b · git clean · NOT TOUCHED
```

Every venue call in this pass was a read; the DB was opened `mode=ro` except where the resolver
itself ran, and it wrote nothing because there was nothing to resolve.
