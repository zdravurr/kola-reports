# TITAN — STATUS CHECK, READ-ONLY

**2026-08-06 17:50 UTC · `/root/titan-bot` · LIVE REAL MONEY · READ-ONLY. NOTHING CHANGED.**

`git status` clean · **HEAD `897850b`** · workers 2538048/2538082 up since 01:53:18 · DB opened `mode=ro`.

---

1. **`ema_envelope_blocked` since 2026-08-04 14:41 — 85 rows.** (Rows, not days, as asked.)
2. **Positions since 01:53:18 — 0 opened, 0 closed.** 0 open now. **Tracebacks since 01:53:18 — 0.**
3. **Hands-required alerts — 0**, by two independent readings: `naked_position_alerts` **does not exist
   on Titan** (that table is SOL's, created by SOL's `_record_naked_position`), and **0** rows carry
   `naked_position_unprotected` / `sl_failsafe_close_failed` / `sl_failed_position_closed` /
   `sl_failed_no_position` in `trades` since 01:53:18.

---

```
READ-ONLY — no file written, no service restarted, no order placed. Titan not modified.
```

*Generated 2026-08-06 17:50 UTC.*
