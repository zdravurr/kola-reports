# A REPORT WITHOUT ITS LINK NO LONGER SENDS — THE RULE IS NOW A LOCK, NOT A PROMISE

**2026-08-04 19:45 UTC · APPLIED · `titan-bot/full_report.py` + 4 alert call sites**

**Operator, today:** *"every report you publish from now on must have its raw link sent to Telegram
in the same message as the report. If the link is missing, the message should not go at all."*

The rule already existed in three places in memory and had already been restated after being missed.
**Discipline had its chances. This pass turns it into a mechanism** — the sender now refuses.

---

## WHAT CHANGED

`send_full_report(text, require_link=True)` — the default path **refuses to send** a message that
does not contain a `raw.githubusercontent.com/….md` link, returns `False`, and prints why.

The irony worth recording: **this module already knew.** It has computed
`"has_link": bool(_LINK_RE.search(body))` for the deliveries ledger since 2026-07-17 — it measured
the very condition, wrote it down, and sent anyway. **The regex was already there; only the refusal
was missing.** That is the same silhouette as every §2.x item in Titan's file: the label said one
thing, the thing did another.

```python
if require_link and not _LINK_RE.search(str(text or "")):
    print("[full_report] REFUSED TO SEND: no raw report link in the message. ...")
    return False
```

## WHY THERE IS AN ESCAPE HATCH, AND WHY IT IS NOT A LOOPHOLE

A blanket gate was measured before it was rejected. Of **297** deliveries through this sender,
**54 carried no link** — and they are not sloppy reports. They include:

| when | what would have been silenced |
|---|---|
| 2026-07-29 21:14 | `🔴🔴 TITAN LIVE — NAKED SHORT ON THE EXCHANGE, NO STOP, NO DB ROW` |
| ongoing | `turn_report_watchdog` — the nag that enforces **this very rule** |
| ongoing | `dirigent_container_watch` — container-down alarm |
| ongoing | `report_due` — the deadline reminder |

**A blanket gate would have switched off the guard with the same motion that switches on the
guarded thing** — the failure class this system has already paid for. So alerts keep a way through,
but they must **declare themselves alerts in code, at the call site**:

```python
send_full_report(msg, require_link=False)   # ← an alert, not a report
```

Four call sites were made explicit in the same pass (`turn_report_watchdog.py`, `report_due.py`,
`dirigent_enforce.py`, `dirigent_container_watch.sh`). **A report cannot reach `require_link=False`
by accident — someone has to type it, in the file, next to a comment saying what it is.**

## PROVEN BY EXECUTION, ALL THREE DIRECTIONS

```
A) report WITHOUT a link      -> REFUSED, returned False   ✔ (must not go)
B) same text as explicit alert-> delivered, returned True   ✔ (alerts survive)
C) report WITH a link         -> delivered, returned True   ✔
GATE CORRECT = True
```

## SCOPE — WHAT THIS DOES **NOT** COVER

🔴 **There are two copies of `full_report.py` on this box** — `/root/titan-bot/` (patched) and
`/mnt/volume_nyc1_1780480650620/mercury-sol/` (**untouched, by standing instruction**). The gate
binds the universal sender that every report of mine goes through; the SOL copy is unchanged and
would still send a link-less message if something called it directly. **Two copies of one sender is
itself the "two sources of truth" class and is recorded here as open, not fixed.**

The `lib/full_report.py` path that `turn_report_watchdog` prepends to `sys.path` **does not exist** —
the watchdog's primary sender is `notify.send_report_confirmed` (botuser creds) and `full_report` is
only its root-run fallback. Noted so a future session does not go looking for a third copy.
