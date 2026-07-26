# followup-15mconfirm-and-missed-secret

_2026-07-26 23:07 UTC_

---

# TITAN — follow-up: 15m_confirm confirmed live, and a secret my own scan missed

**2026-07-26 23:05 UTC.** Two items, one good and one that corrects my earlier report.

---

## 1. Part 4 CONFIRMED LIVE — the first `15m_confirm` row exists

The background watcher ran 45 minutes without seeing one and timed out; the alert simply had not
arrived. It arrived at 23:00 and the row was written immediately:

```
WEBHOOK_IN 23:00:04  tf='15m' action='reversal down'  (task=confirmation)

id    | timestamp            | tv_action     | signal_type  | status
18786 | 2026-07-26 23:00:07  | Reversal D. | 15m_confirm  | confirm_recorded
```

Three seconds from door to row, with the SOL-mirrored status name `confirm_recorded`. **The missing
write is closed.** The 15m entry stream — HyperWave / Reversal / Divergence, ~26 alerts a day — is
now auditable for the first time since the bot was built.

Gap between the last pre-restart 15m alert (21:45) and this one (23:00) was 75 minutes — the upper
end of the normal 45-75 min spacing, not an anomaly.

---

## 2. 🔴 I MISSED A SECRET IN MY OWN PART 1 SCAN

**The webhook passphrase is in the nginx access logs**, in the URL query string of every single
request, and has been for as long as the logs are retained.

```
POST /webhook?key=<PASSPHRASE>&tf=15m          <- Titan
POST /webhook/sol?secret=<SECRET>&tf=15m       <- Mercury-SOL
```

**Why my scan missed it.** I searched for the *environment-variable* form — `WEBHOOK_PASSPHRASE=` —
plus the `sk-ant-` and Telegram-token patterns. The URL form `?key=<value>` matches none of those.
The scan was pattern-complete for the leaks I was looking for and blind to the one shape I had not
thought of. That is a scanning error, not a new event: this has been happening since nginx was put
in front of the bot.

**Scale and severity**
```
/var/log/nginx/access.log         518 lines    640 www-data:adm
/var/log/nginx/access.log.1       544 lines    640 www-data:adm
rotated .gz archives            ~3,518 lines   640 www-data:adm
```
**Not world-readable** — group `adm`, whose only member is `syslog`. Materially less exposed than
the Anthropic key was at 644, but it is a live credential sitting in a log that survives rotation
for two weeks, and it covers **both bots**.

Worth noting for contrast: **the bot redacts this correctly in its own logs.** `KeyStrippingHandler`
in `main.py` rewrites the path to `key=REDACTED` before gunicorn logs it. The redaction exists —
nginx sits in front of it and logs the raw request line first.

**What I did:** redacted the values in place across current, rotated and compressed nginx logs
(1,062 + ~3,518 lines → 0), backing up the current log first. I **redacted rather than deleted**, so
the request-volume evidence used in the earlier ingress analysis survives intact. nginx and
titan.service both verified still running and still logging afterwards.

**What I did NOT do, and why it needs your decision:**
* **The passphrase is unchanged.** Rotating it means updating every TradingView alert URL by hand —
  dozens of alerts across three timeframes on two bots. That is your call, and the exposure is
  group-readable rather than world-readable, so it is not the same urgency as the Anthropic key.
* **nginx is still logging it.** The fix is a `log_format` change to strip the query string, which
  is shared infrastructure affecting both bots. I did not touch nginx config unilaterally.

---

## Standing decisions now waiting on you

1. **Rotate the Anthropic API key** — was world-readable for 20 days (`OPEN-ITEMS §8`).
2. **Webhook passphrase** — rotate and/or stop nginx logging the query string. Lower urgency.

---

Both applied changes are log redaction only. No bot code, no config, no gate touched. `titan.service`
and `nginx` healthy; `15m_confirm` writing; the exit advisor's hourly consultation next due ~23:06.
