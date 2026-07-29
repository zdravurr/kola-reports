# titan-signal-tiers-applied-verified-post-restart

_2026-07-29 12:07 UTC_

---

## THREE CORRECTIONS BEFORE ANYTHING ELSE

**1. The patch IS applied — but `titan.service` was NOT restarted at 11:50:05.** It restarted **once**,
at **11:36:09 UTC**, and `NRestarts=0`. The 11:50:05 event in the journal was a different unit:

```
Jul 29 11:50:05 systemd[1065]: Stopped openclaw-gateway.service - OpenClaw Gateway (v2026.6.5).
Jul 29 11:50:05 systemd[1065]: Started openclaw-gateway.service - OpenClaw Gateway (v2026.6.5).
```

That is the OpenClaw/Telegram bridge, not the bot. Titan's own journal shows exactly one
stop/start pair, at 11:36.

**2. I did publish a confirmation, and I failed to deliver it.** It went out at 11:54 as
`reports/2026-07-29-1154-titan-signal-tiers-applied-post-restart-confirmation.md`, and I replied
with only that link — because the instruction said "reply with ONLY that raw link", **I did not send
it to Telegram at all.** Standing rule №1 says every substantive report goes to Telegram regardless
of what the terminal reply looks like. A report that exists only as a link in a terminal is an
undelivered report. That is my error, not an ambiguity, and it is almost certainly why you never saw
it. This one goes to Telegram as well as here.

**3. Item 2 as specified cannot be satisfied yet, and I am not going to dress it up.** There has been
**no live entry decision since the restart.** Four signals have arrived (11:40, 11:45) and all four
were `htf_blocked` — those never reach the advisor, so no entry prompt has been stored. What I can
show, and do show below, is (a) the prompt built by the **deployed code** against the **live** state
machine, and (b) a **real stored consult** from the exit advisor at 12:02:01 that proves the new code
is running in production. The entry-side stored row will appear on the next signal that clears the
HTF cascade.

---

# 1. IS THE PATCH APPLIED?

**Yes.**

```
$ git status --short          (empty — clean)
$ git log --oneline -2
7285c5d feat(titan): all THREE signal tiers reach both advisors — identity, direction, weight, age
8b15ecc feat(titan): give the ENTRY advisor the order-book PERCENTILE scale (fact, not judgement)

$ git diff --stat 8b15ecc HEAD
 titan-bot/claude_advisor.py | 110 ++++++++++++-----------
 titan-bot/main.py           |  63 +++++++++++--
 titan-bot/signal_tiers.py   | 215 +++++++++++++++++++++++++++++++++++++ (new)
 3 files changed, 326 insertions(+), 62 deletions(-)
```

**HEAD `7285c5d`**, pushed to `origin/main`. Exactly three files changed versus `8b15ecc`.
Rollback available: tag `pre-signal-tiers-20260729T113516Z` plus
`main.py.bak_tiers_20260729T113516Z` and `claude_advisor.py.bak_tiers_20260729T113516Z`.
Schema migrated: `trades.entry_tiers_json` present, 148 columns.

# 2. RENDERED ENTRY PROMPT — ALL THREE TIERS COMPLETE

Built by the **deployed code** at `7285c5d` against the **live** state machine, **live** matrix and
**live** OKX book at 12:06 UTC. Only the Anthropic call is stubbed; every byte is what the advisor
receives.

**Labelled honestly: this is a forced render, not a stored decision row** — see correction 3.

Live slots at render time:

```
1h_context   dir=LONG   name='Smart Trail Bullish'
15m_confirm  dir=SHORT  name='HyperWave Signal Down'
5m_trigger   dir=LONG   name='Within Bullish OB'
```

```
Symbol: BTC/USDT:USDT
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  Smart Trail Bullish  (direction withheld (AI_ADVISOR_HIDE_1H), weight 0.9, last set 4.1h ago)
  15m: HyperWave Signal Down  (SHORT, weight 0.7, last set 66m ago)
  5m:  Within Bullish OB  (LONG, weight 0.7, last set 21m ago, trigger-capable, NOT counted by the gate — matrix TTL expired)
  Agreement: 5m points LONG; 15m points SHORT; vs the proposed LONG: 5m agree, 15m OPPOSE.
```

Every tier carries **name, direction, weight and age**, and the agreement line is explicit.

🔴 **This render is itself the case that justified the change.** The 15m points **SHORT** while the
5m points **LONG** — they disagree. Under the old prompt this exact moment would have printed
*"The 3 timeframes are aligned (confluence has already passed)"*.

The 1H direction reads `withheld` because `AI_ADVISOR_HIDE_1H` is `True`. That flag was nearly broken
by this patch and is not: the "the score gate counted this tier as …" clause would have leaked the
direction the flag exists to hide, so `gate_direction` is stripped for the 1H tier only.

# 3. EXIT ADVISOR — ENTRY-THESIS BLOCK FOR vpos 84

**A real stored consult, not a render.** `trades` row **19452**, `2026-07-29 12:02:01`, trigger
`hourly review`, verdict **hold** (conf 0.72) — the first hourly consultation after the restart,
written by the deployed code:

```
ENTRY THESIS — the exact tiers that opened this position
  1H:  Bullish Confirmation  (legacy record — direction, weight and age were not captured before 2026-07-29)
  15m: ABSENT  (legacy record)
  5m:  Bullish OB Mitigated  (legacy record)
  Advisor's reason at entry: 1H/15m/5m bullish confluence + 1H ADX 30.7 (strong trend) + 15m/5m
  expanding EMA. No opposing ask wall blocks long. 1D/4H neutral but lower-TF alignment (2/4)
  sufficient for DCA grid entry with hedge risk management.
```

**Before the patch the same block read:**

```
  1H trend set by:   Bullish Confirmation
  15m confirmed by:  n/a
  5m triggered by:   Bullish OB Mitigated
```

All three tiers are named and `n/a` is gone. **Stating the limit plainly:** vpos 84 opened
2026-07-28 17:00, *before* the patch, so it has no `entry_tiers_json` and correctly takes the legacy
path — **direction, weight and age cannot be shown for it**, because that record did not exist when
it opened. The full record appears on the first position opened from now on. `entry_tiers_json` is
non-null on 0 rows so far, as expected: no entry has executed since 11:36.

# 4. NO TIER CAN RENDER `n/a` — THE EMPTY-SLOT CASE

Rendered by the deployed `signal_tiers` module with all three slots empty:

```
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  ABSENT — no 1H signal is held by the state machine at this moment
  15m: ABSENT — no 15m signal is held by the state machine at this moment
  5m:  ABSENT — no 5m signal is held by the state machine at this moment
  Agreement: No tier currently holds a directional signal.
```

And the mixed case — the exact shape of the failing entry 19021 (1H reset to NEUTRAL, 15m wiped):

```
  1H:  Trend Catcher Down  (NEUTRAL, weight 1.0, last set 60m ago)
  15m: ABSENT — no 15m signal is held by the state machine at this moment
  5m:  Within Bearish OB  (SHORT, weight 0.7, last set 5m ago, trigger-capable)
  Agreement: 5m points SHORT; vs the proposed SHORT: 5m agree; 1H NEUTRAL (reset, not in force); 15m ABSENT.
```

Exhaustive proof, run against the deployed module — **648** combinations (6 signal names including
`None` and an unknown signal × 4 directions including `None`/`NEUTRAL` × 3 timestamps including
`None` and a garbage string × 3 matrix states × 3 proposed directions):

| check | result |
|---|---|
| tier lines containing `n/a` | **0 of 648** |
| every result JSON-serialisable | yes |
| `entry_thesis_lines()` raised | no |

Static confirmation: the remaining `n/a` strings are **docstring only** in `signal_tiers.py`
(lines 5, 26) and **comment only** in the tier block of `claude_advisor.py` (line 274). The legacy
exit path guards on `m.group(1) != 'n/a'` and falls through to `ABSENT`. **Zero executable `n/a` in
any tier path.**

*(The `Long/Short ratio: n/a` still visible elsewhere in the prompt is the BingX account ratio — not
a tier, genuinely unavailable, and correctly saying so.)*

# 5. FLAGS — ALL UNCHANGED

`config.py` is **not in the diff at all** (`git diff --stat 8b15ecc HEAD -- config.py` → empty).

| flag | value |
|---|---|
| `LIVE_TRADING_ENABLED` | **False** |
| `LONG_PARTIAL_ENABLED` / `LEVEL_R` / `FRACTION` | **True** / 1.0 / 1/3 |
| `EXIT_ADVISOR_PAPER_ENABLED` | **True** |
| `EXIT_ADVISOR_DRYRUN` | **True** |
| `EXIT_ADVISOR_ON_15M_CONFIRM` | **True** |
| `EXIT_ADVISOR_HOURLY` / `_SEC` | **True** / 3600 |
| `CONFLUENCE_FLAT_THRESHOLD` | **5.0** |
| `WALL_TRAIL_LIVE_ENABLED` | **False** |
| `AI_ADVISOR_HIDE_1H` | **True** |

# 6. UNTOUCHED — PROVEN, NOT ASSERTED

Byte-for-byte comparison of each named region against the pre-apply tag:

| function | file | result |
|---|---|---|
| `confluence_check` | `state_machine.py` | **IDENTICAL** |
| `htf_alignment` | `signal_matrix.py` | **IDENTICAL** |
| `_htf_cascade_gate` | `main.py` | **IDENTICAL** |
| `reset_1h_trend` | `state_machine.py` | **IDENTICAL** |
| `_clear_lower_tfs_locked` | `state_machine.py` | **IDENTICAL** |
| `update_slot` | `state_machine.py` | **IDENTICAL** |

`git diff --stat 8b15ecc HEAD` for `config.py`, `state_machine.py`, `signal_matrix.py`,
`virtual_trader.py`, `risk_manager.py`, `adaptive_trail.py`, `breakeven_worker.py` → **empty, zero
changed lines.** That covers the cascade's confirmation logic, the score gate, `market_regime`,
SL/trail/breakeven and the LONG partial — none of them is in the diff.

**Mercury-SOL:** `git diff --stat 8b15ecc HEAD -- mercury-bot/` → **empty**; service **active**.

# 7. RECORDED IN OPEN-ITEMS

Working copy `reports/OPEN-ITEMS.md` updated and pushed, with a byte-identical dated snapshot at
**`reports/2026-07-29-1145-open-items.md`** (§8 — the dated path is the linkable one). §2.3 marked
**CLOSED**. Three new entries, all **watch, do not act**:

**§2.8 BEHAVIOURAL CHANGE — WATCH ENTRY FREQUENCY.** The advisor now sees `ABSENT` tiers and an
honest agreement line where it was previously told all three agreed — false on 14 of 59 executed
entries. It may skip entries it would have approved; that is the expected consequence of removing a
false statement, **not a regression — but it must be measured, not assumed.** Compare skip rate and
executed-entry count over ~2 weeks from 2026-07-29 11:36 UTC against the equal window before.
Baseline: 2026-07-06 → 07-29, **610** signals cleared the score gate, **17** became trades = **2.79%**.
All 2,565 `ai_skipped` rows store `ai_user_prompt` and it now carries the tier block, so the
comparison runs straight from the prompts.

**§2.9 TWO REGISTRIES DISAGREE BY DESIGN — NOT PROPOSED.** `state_machine`'s 15m slot (4h TTL, wiped
by 1H flip / Group-B Exit) and `signal_matrix` MOMENTUM (90 min TTL, wiped by nothing) hold the same
fact and diverge **both ways** — over the last 20 entries, 2 had an empty slot while the matrix held
3 live signals, 6 had a live slot the matrix had already expired. The patch reports both rather than
picking one. Reconciling them is a cascade-state change and is **not proposed**.

**§2.10 AGE IS THE AGE OF LAST SET, NOT OF FIRING.** `reset_1h_trend()` overwrites the slot timestamp
while keeping the name, so a reset tier's age is the reset's age — entry 19021 read *"set 1.0h ago"*
for a signal that fired **2.0h** earlier. The patch labels it `last set` rather than lying, and now
prints the direction so a reset tier shows as `NEUTRAL`. A proper fix needs a separate `set_at` field
in `state_machine` — **out of scope, deliberately not done**, recorded so it is not rediscovered.

# 8. SERVICE HEALTH

| check | result |
|---|---|
| `systemctl is-active titan` | **active** |
| `ActiveEnterTimestamp` | **2026-07-29 11:36:09 UTC** |
| `NRestarts` | **0** |
| errors / tracebacks / exceptions in the journal since 11:36:09 | **0** |
| workers | `breakeven_worker` (5s), `virtual_trader` (10s), `OB-DENSITY` collector (60s) all started |
| **hourly exit-advisor consultation** | **FIRING** — row 19452 at **12:02:01**, trigger `hourly review`, verdict `hold` (conf 0.72), one hour after the pre-restart consult at 11:01:54. Cadence unbroken across the restart. |

Its verdict text, showing it is reading live data normally:

> Entry thesis partially intact but degrading. Original 1H bullish confirmation still valid
> structurally (+0.55R profit confirms directional bias). However: ADX collapsed 1H(30.7→24.2) and
> 15m(21.5) signals weakening trend…

---

## STATE AT CLOSE

`git status` clean · HEAD **`7285c5d`** · pushed · `titan.service` **active** since 11:36:09 UTC,
0 restarts, 0 errors · **Mercury-SOL untouched and active**

**Book: 1 open position** — vpos 84 LONG @ 63,997.3, ~+0.55R, stop 63,129.9 (original), partial not
fired.

**Still outstanding:** a stored **entry**-side consult. It needs a signal that clears the HTF
cascade; the four since restart were all blocked before the advisor. It will land in
`trades.ai_user_prompt` on its own, whether or not anyone is watching.
