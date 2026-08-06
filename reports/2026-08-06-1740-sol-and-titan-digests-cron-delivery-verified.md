# BOTH SILENCE DIGESTS DELIVER FROM CRON — VERIFIED, NOT ASSUMED

**2026-08-06 17:40 UTC · READ-ONLY. Nothing changed, nothing sent by the digests during this check.**

Titan (`/root/titan-bot`, LIVE REAL MONEY): **inspected read-only, never executed, not modified.**

---

## THE ANSWER FIRST

> **Both digests have fired from cron, unattended, and both delivered. Neither is broken.**
>
> 🔶 **And a correction to the premise:** every delivery in SOL's log came **from cron** — **2 log
> lines, 2 cron invocations, zero manual sends.** My manual runs today were all `--dry`, which prints
> to stdout and neither appends to the log nor sends. The log is pure cron.

---

# a) The cron entries

```cron
# ── ЖУРНАЛ ТИШИНЫ MERCURY-SOL (05.08) … 08:20 UTC, чтобы не слипаться с титановским 08:05.
20 8 * * * /usr/bin/timeout 120 /usr/bin/python3 \
           /mnt/volume_nyc1_1780480650620/mercury-sol/silence_digest_sol.py \
           >> /var/log/mercury_sol_silence_digest.log 2>&1

05 8 * * * /usr/bin/python3 /root/titan-bot/silence_digest.py \
           >> /var/log/titan_silence_digest.log 2>&1
```

| | SOL | Titan |
|---|---|---|
| schedule | **08:20 UTC daily** | **08:05 UTC daily** |
| interpreter | `/usr/bin/python3` — **absolute** | `/usr/bin/python3` — **absolute** |
| script | absolute | absolute |
| working directory | **cron's default, `$HOME` = `/root`** — and neither script depends on it (see (c)) | same |
| owner | `root` crontab | `root` crontab |
| wrapper | `timeout 120` — cannot hang the crontab | none |

`cron.service`: **active, enabled.**

# b) Has it ever fired from cron? — **YES, and every line is accounted for**

```
2026-08-05T08:05:01  CRON[2301080] (root) CMD (… /root/titan-bot/silence_digest.py …)
2026-08-05T08:20:01  CRON[2303822] (root) CMD (… timeout 120 … silence_digest_sol.py …)
2026-08-06T08:05:01  CRON[2623244] (root) CMD (… /root/titan-bot/silence_digest.py …)
2026-08-06T08:20:01  CRON[2626383] (root) CMD (… timeout 120 … silence_digest_sol.py …)
```

**Exit status, from the logs the cron lines redirect into:**

```
/var/log/mercury_sol_silence_digest.log   (mtime 2026-08-06 08:20:02 — the cron minute)
  DELIVERED= True
  DELIVERED= True

/var/log/titan_silence_digest.log          (mtime 2026-08-06 08:05:03 — the cron minute)
  [SILENCE-DIGEST] sent=True http=200 msg_id=28360
  [SILENCE-DIGEST] sent=True http=200 msg_id=28474
  [SILENCE-DIGEST] sent=True http=200 msg_id=28821
```

**The log mtimes ARE the cron minutes** — 08:20:02 and 08:05:03, one and two seconds after the
invocations above. That is the delivery, not an inference from it.

**Reconciliation, so nothing is hand-waved:**

* **SOL — 2 log lines, 2 cron invocations. Perfect match.** The cron entry was added 2026-08-05
  (crontab mtime Aug 4 23:31), so its first possible fire was 08-05 08:20. Both fires are present and
  both returned `DELIVERED= True`. **100% of SOL's deliveries are unattended.**
* **Titan — 3 log lines, 2 cron invocations.** The third is a manual run at creation: the script's
  mtime is **2026-08-04 19:48**, before its first cron fire on 08-05. Titan's script has **no `--dry`
  flag**, so a run at build time necessarily sent. Syslog rotation does not hide anything —
  `syslog.1` ends Aug 2 and the `.gz` files are from July, all before the script existed.

# c) The minimal-environment question — **tested, not reasoned**

Ran the SOL digest under a stripped environment: `env -i HOME=/root PATH=/usr/bin:/bin`, cwd `/root`:

```
🔇 MERCURY-SOL — SILENCE LEDGER
window: last 24h → 2026-08-06 17:35 UTC
mode: PAPER (OBSERVATION_MODE=1) · open positions: 0
✅ NOTHING NEEDS HANDS — …
  webhooks logged    341 rows → 216 market events (×1.58)
EXIT=0
```

**`mode: PAPER (OBSERVATION_MODE=1)` is the proof that matters** — that line only renders if
`import config` **and** `load_dotenv` both succeeded with no shell help.

| dependency | how it resolves | shell-independent? |
|---|---|---|
| `DB_PATH` | hardcoded absolute (`/mnt/…/trades.db`) | ✅ |
| `import config` | Python puts the **script's own directory** at `sys.path[0]`, so `config.py` resolves from `/root` | ✅ |
| `.env` (mode line) | `load_dotenv('/mnt/…/mercury-sol/.env')` — **absolute** | ✅ |
| Telegram token | `sys.path.insert(0, '/root/titan-bot')` + `load_dotenv('/root/titan-bot/.env')` — **absolute** | ✅ |
| `PATH` | cron calls `/usr/bin/python3` **absolutely**; the script shells out to nothing | ✅ |
| virtualenv | **none** — system python3, `dotenv` installed globally | ✅ |
| working directory | never read | ✅ |

The **send** path checked separately under the same stripped environment, **without sending**:

```
import full_report      : OK
FULL_REPORT_BOT_TOKEN   : SET
FULL_REPORT_CHAT_ID     : SET
(nothing sent)
```

# d) Titan — same question, inspected read-only and **never executed**

```python
load_dotenv('/root/titan-bot/.env')          # absolute, module level
DB_PATH = '/root/titan-bot/trades.db'        # absolute — exists=True
import requests                              # sends via its own HTTP call
```

**Titan's digest is even less environment-dependent than SOL's:** no `import config`, no `sys.path`
manipulation, no cwd use — two absolute paths and `requests`. Its cron line uses an absolute
interpreter and an absolute script.

🔴 **I did not run it.** It has **no `--dry` flag**, so any execution would have sent a real message to
the Boss's channel. Its own log already proves what execution would have shown — `sent=True http=200`
on three separate runs — so running it would have added noise and no evidence. **Titan was read, not
touched, not modified.**

---

## VERDICT

**Neither is broken. Nothing to fix.**

* SOL: fires 08:20 UTC, has fired twice, delivered twice, **entirely unattended**.
* Titan: fires 08:05 UTC, has fired twice from cron plus one manual run at creation, delivered all three.
* Both are fully absolute-path and resolve identically under cron's minimal environment — **proven by
  running SOL under `env -i`, not by reading the code.**

**Tomorrow at 08:20 UTC the SOL digest will carry the new `NEEDS HANDS` block for the first time from
cron**, and the operator will see it in the channel without asking for it.

```
READ-ONLY — no file written, no service restarted, no digest sent by this check.
SOL   worker 2756553 · flat 0/0/0 · OBSERVATION_MODE=True
TITAN git clean · HEAD 897850b · read only, NOT executed, NOT modified
```

*Generated 2026-08-06 17:40 UTC.*
