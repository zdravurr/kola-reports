# titan-variant-c-and-final-cleanup

_2026-07-29 13:58 UTC_

---

**Part 1 studied and NOT applied. Part 2 applied (`41c4a4d`).** Final verdict in §4.

Two things happened on their own while this ran, and both matter: **vpos 84 closed** (+16.54) and
**vpos 85 opened** — the first entry executed since the signal-tier work, which finally exercises the
`entry_tiers_json` write path I have twice reported as unverified. It works. Details in §3.

---

# PART 1 — VARIANT C: STUDIED, NOT APPLIED

## Method

Simulated on **real 5m candles** (18,900 bars, 2026-05-24 → 07-29), not on the excursion samples.
§0 filter 4 says never use stored extrema for a path question, and the samples are ~5-minute point
prices — they cannot see the intra-sample retracement that a narrow trail exits on. The excursion
table (2,885 rows) was used only to confirm coverage.

The simulator replicates the live contract exactly: 1R stop at entry; at +1R the stop moves to
**breakeven** and the trail arms; thereafter the stop follows the high-water mark at `width × R`,
never loosens, never drops below breakeven. Intrabar ambiguity resolved **adversely** — the stop side
of each bar is tested first, which biases every result **against** the narrow trail.

**Validation at width 1.0 against the 10 clean closed positions:** all four stop-outs reproduce at
exactly −1.00R vs a real −1.09…−1.20 (the gap is fees), vpos 79 +0.61 vs +0.50 real, vpos 81 +0.90 vs
+0.77 real. Mean error +0.069R ≈ the fee drag. The three `external` closes diverge because the
simulator cannot know about an operator/armed exit.

## (a) Usable paths

| | clean closed | with a usable candle path |
|---|---|---|
| LONG | 5 | **5** |
| SHORT | 5 | **5** |

All four §0 filters applied. Ten positions, 2026-07-14 → 07-29. (vpos 84 closed during this session
and is included.)

## 🔴 The crux, before any width number: the trail barely ever arms

| side | armed the trail (reached +1R) | never armed |
|---|---|---|
| LONG | **2** — vpos 79, 82 | **3** — vpos 75, 78, 84 |
| SHORT | **1** — vpos 81 | **4** — vpos 76, 77, 80, 83 |

**A position that never reaches +1R is byte-identical under every trail width.** The width question
therefore has an effective **n of 2 on the long side and 1 on the short side**. Everything below has
to be read through that.

## (b) LONG width sweep

| width | net R (n=5) | mean | win | winners cut short | losers improved |
|---|---|---|---|---|---|
| **1.0 — today** | **+0.46** | +0.093 | 3/5 | — | — |
| 0.75 | +0.96 | +0.193 | 3/5 | 0 | 0 |
| 0.6 | +1.26 | +0.253 | 3/5 | 0 | 0 |
| 0.5 | +1.46 | +0.293 | 3/5 | 0 | 0 |

Per position:

| vpos | w=1.0 | w=0.75 | w=0.6 | w=0.5 |
|---|---|---|---|---|
| 75 | −0.01 | −0.01 | −0.01 | −0.01 |
| 78 | −1.00 | −1.00 | −1.00 | −1.00 |
| **79** | **+0.61** | **+0.86** | **+1.01** | **+1.11** |
| **82** | **+0.49** | **+0.74** | **+0.89** | **+0.99** |
| 84 | +0.38 | +0.38 | +0.38 | +0.38 |

Monotone, and **entirely produced by two rows**. "0 winners cut" at every width is not a property of
the idea — it is what happens when both informative positions ran and then reversed hard. Two
observations cannot establish that a narrower trail never cuts a winner.

## (c) SHORT control — 0.5R is disqualified

Clean shorts (n=5, only one armed) show nothing usable: −1.57R at width 1.0, −1.17R at 0.6, −1.43R at
0.5. The decisive test is the **tail**, re-simulated from entry on the eight short runners. Their
recorded PnL is contamination-filtered, but the path question is re-derived from entry here, so the
tail test is valid on the wider set — their net_pnl is not quoted.

| vpos | MFE | w=1.0 | w=0.75 | w=0.6 | **w=0.5** |
|---|---|---|---|---|---|
| 43 | 2.31R | +1.33 | +0.76 | +0.91 | +1.01 |
| 44 | 2.31R | +1.33 | +0.76 | +0.91 | +1.01 |
| 46 | 3.31R | +2.31 | +1.70 | +1.60 | **+0.81** |
| 48 | 2.98R | +1.99 | +2.24 | +2.39 | +1.32 |
| 49 | 2.98R | +1.99 | +2.24 | +2.39 | +1.32 |
| 57 | 2.26R | +1.30 | +1.55 | +1.70 | +1.08 |
| **58** | **3.40R** | **+2.41** | +2.66 | +2.81 | **+1.07** |
| 81 | 1.87R | +0.90 | +1.15 | +1.30 | +1.04 |
| **TOTAL** | | **+13.57** | +13.06 | +14.01 | **+8.67** |

🔴 **0.5R destroys the short tail — −36%.** vpos 58 falls 2.41 → 1.07, vpos 46 falls 2.31 → 0.81.
**Disqualified for shorts**, exactly as the control was designed to catch. The 0.6 and 0.75 columns
are non-monotone against each other (+14.01 vs +13.06), which is the signature of noise, not signal.

## (d) Interaction with the LONG partial — they are SUBSTITUTES

| width | no partial | WITH the 1/3 @ +1R partial | what the partial adds |
|---|---|---|---|
| **1.0** | +0.46 | **+0.76** | **+0.30** ← today's live contract |
| 0.75 | +0.96 | +1.10 | +0.13 |
| 0.6 | +1.26 | +1.30 | +0.03 |
| 0.5 | +1.46 | +1.43 | **−0.03** |

Both mechanisms solve the **same** problem — banking before giveback — so stacked they give
diminishing and then negative returns. **A narrower trail plus the partial is not the sum of the
two, and at 0.5R the partial starts costing money.** Anyone tuning one must re-tune the other.

## (e) Honest verdict on n

**Enough to choose a STRUCTURE. Nowhere near enough to choose a WIDTH.**

- **Structure supported:** *longs give back too much at a 1.0R trail, and narrowing helps them
  without touching shorts.* The direction is consistent across both informative longs, both
  partial variants, and it survives the adverse intrabar convention.
- **Width NOT supported:** n = 2 armed longs. Any width picked today is fitted to vpos 79 and 82.
  0.5R is separately ruled out by the short tail, so the live candidate range would be 0.6–0.75 —
  and those two differ by less than the noise between them.
- **What the parameter actually needs: ARMED longs, not merely closed ones.** Historical arming rate
  is **22% for LONGs** (5 of 23) — a stricter bar than §2.1's ">0.5R". At 0.74 closed positions/day
  that is ~0.13 armed longs/day:

| target | calendar time |
|---|---|
| 20 armed clean longs | **~5 months** |
| 30 armed clean longs | **~7.5 months** |

🔴 **Not applied. Do not apply a width on this evidence.**

---

# PART 2 — CLEANUP, APPLIED (`41c4a4d`)

## 1. `Long/Short ratio` — deleted

It rendered `Long/Short ratio: n/a` on 100% of entry consultations for the life of the bot.
`mc_ls_ratio` is NULL on all 18,505 rows and the codebase has **no fetcher** — only the column
declaration, the parameter and the render. **Deleted, not implemented.** `_ENTRY_SYSTEM` no longer
claims the model receives it; the `ls_ratio` parameter stays in the signature and is ignored so both
`main.py` call sites remain valid.

Verified on the **first real entry after the change** (vpos 85, trades row 19468): the string `n/a`
appears **nowhere** in the entry prompt, and neither does `20-23`.

`mc_recent_liq_long_usd` / `mc_recent_liq_short_usd` are equally empty but **render nowhere** —
`market_context.py` already records that BingX removed the REST liquidation endpoint on 2026-05-15.
Nothing to delete there.

## 2. `titan_bull_regime_watch` — edge-triggered, not retired

It fired on the standing condition and therefore fired **every day** once BTC's daily turned bull
(157, 54, 56, 56 against a threshold of 30). It now fires **once on the transition in**, and logs the
transition out silently. State in `.state_bull_regime_watch`; deleting that file re-arms it.

Verified: first run fired, second run printed
`no CHANGE (N=56, state=bull) — edge-triggered, staying quiet`.

Redefined rather than retired because the question is still genuinely open — the LONG regime drill
needs a real daily uptrend, which Titan has never had.

## 3. The two starved sensors — expiry, enforced by the script

Both now carry **`EXPIRES 2026-09-30`** with the delete-if-not-reached rule **enforced in code**:
after that date the script stops measuring, sends one Telegram —
*"DELETE the script and its cron line. Do not extend the date."* — and exits.

| sensor | state | why it needs an expiry |
|---|---|---|
| `regime-FLAT high-ADX` | 5 / 12 | **zero arrivals in 7 days** on a rolling 21-day window, so N **falls**; needs `trend_4h='bull'`, down from 34.9% to 7.9% of rows |
| `chop-short flat-gap` | 0 / 5 | 2 rows in two months, 0 since the FLAT floor |

**Deliberately the same date as the volume ceiling (§2.5): one expiry review to remember, not three.**
Verified both branches — normal output today, `EXPIRED 2026-09-30 — asking to be deleted` on a
dry-run at a simulated 2026-10-01.

---

# 3. WHAT HAPPENED ON ITS OWN DURING THIS SESSION

**vpos 84 closed** at 13:30:08, **+16.54** (external/armed exit). It is the **first closed position
under the corrected prompt** (`c307bb7`, 13:21:47), so §2.4's restarted count is now **1 of ~10** —
and it is **neutral**: the advisor's only verdict was `hold` (row 19460), no `close` was ever issued,
so it neither improved nor worsened the exit. Same shape as the discarded vpos 82.

**vpos 85 opened** at 13:50:18 (LONG @ 64,604.4) — and it closes a gap I have flagged twice:

> ✅ **`entry_tiers_json` WRITE PATH VERIFIED LIVE.** Row 19468 carries the full structured record —
> all three tiers with name, direction, weight, age, kind and the agreement line, JSON round-tripped.
> The rendering was already proven; the persistence now is too.

The stored prompt for that entry:

```
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  Smart Trail Bullish  (direction withheld (AI_ADVISOR_HIDE_1H), weight 0.9, last set 5.8h ago)
  15m: HyperWave Signal Down  (SHORT, weight 0.7, last set 2.8h ago, NOT counted by the gate — matrix TTL expired)
  5m:  Bullish OB Created  (LONG, weight 0.5, last set 0m ago, trigger-capable, NOT counted by the gate — matrix TTL expired)
  Agreement: 5m points LONG; 15m points SHORT; vs the proposed LONG: 5m agree, 15m OPPOSE.
```

⚠️ **One observation, recorded as a fact and not a finding (n=1):** the advisor's reason came back
*"5m bullish trigger + 1h/15m/5m agree on upside"* — it asserted an agreement the prompt had
**explicitly denied on the line above**. The tier block did its job; the advisor contradicted it.
One entry proves nothing about advisor quality. But this disagreement was **invisible before
`7285c5d`** and is now auditable on every single entry, which is the point. Worth watching next to
§2.8.

---

# 3b. 🔴 NEW FINDING — THE CRON SENSORS ARE NOT IN GIT

Found while committing. `.gitignore` is deny-all-then-whitelist and admits only
`titan-bot/**/*.py`, so **every `*.sh` sensor is untracked**.

- **No history.** `d12e276` says "retire 3 sensors, redefine 2" — the actual predicate changes are in
  **no diff anywhere**. The only record of what a sensor used to measure is prose.
- **No rollback.** Today's three sensor edits exist **only on disk**. They are verified working, but
  `41c4a4d` contains `claude_advisor.py` alone.
- ⚠️ **Disclosure:** I made `.bak_20260729` copies before editing and deleted them in the same step
  that staged the commit. Because the files are untracked, **the pre-edit versions no longer exist.**
  The edits are additive and verified; nothing is broken; but the undo is gone, and I should not have
  removed backups of files git was not holding.

**Recommendation, NOT applied** — changing `.gitignore` is a repo-policy decision: whitelist
`!titan-bot/**/*.sh`. Recorded as OPEN-ITEMS §2.20.

---

# 4. FINAL VERDICT — IS ANYTHING LEFT BEFORE MERCURY-SOL?

**No. Nothing that should be done before you move.** Three things remain open and all three are
correctly parked:

1. **Variant C** — answered as far as the data allows. Structure supported, width undecidable, and
   the parameter needs ~5 months of armed longs. Nothing to do but wait; §2.2 now records exactly
   what would close it.
2. **The live-parity rewrite (§1)** — seven divergences, real work, and blocked by nothing while
   `LIVE_TRADING_ENABLED = False`. It must happen **before** live, not as part of enabling it.
3. **`.gitignore` and the sensors (§2.20)** — a one-line policy change I deliberately did not make.

**What I would do differently if you were staying:** nothing urgent. The two prompt falsehoods are
gone, the last always-`n/a` field is gone, the noisy sensor is quiet, the two dead-end sensors will
now ask to be deleted on 2026-09-30 instead of drifting, and both advisors finally describe the same
book and the same tiers in the same language.

**The one thing that is genuinely accumulating and unattended** is the exit-advisor criterion:
**1 of ~10, restarted at `c307bb7`**, currently neutral. It needs nine more closes and no
intervention. Do not re-cut that sample to reach ~10 sooner.

---

## STATE AT CLOSE

`git status` clean · HEAD **`41c4a4d`** · pushed · `titan.service` **active** since 13:49:47 UTC,
**0 errors** · **Mercury-SOL untouched and active**

Scope of `41c4a4d` vs `c307bb7`: **`claude_advisor.py` only** (+20/−8) in git, plus three untracked
sensor scripts (§3b). `config.py`, `main.py`, `state_machine.py`, `signal_matrix.py`,
`virtual_trader.py`, `signal_tiers.py` — **zero changed lines**.

Flags unchanged: `LIVE_TRADING_ENABLED=False` · `LONG_PARTIAL_ENABLED=True` ·
`EXIT_ADVISOR_PAPER_ENABLED/DRYRUN/ON_15M_CONFIRM/HOURLY=True` · `CONFLUENCE_FLAT_THRESHOLD=5.0` ·
`WALL_TRAIL_LIVE_ENABLED=False` · `AI_ADVISOR_HIDE_1H=True`

**Book: 1 open position** — vpos 85 LONG @ 64,604.4, stop 63,787.5, opened 13:50:18.

OPEN-ITEMS updated and pushed: §2.2 **answered**, §2.14 and §2.15 **closed**, §2.19 and §2.20
**opened**, §6/§7 at `41c4a4d`. Byte-identical dated snapshot:
`reports/2026-07-29-1400-open-items.md`.

**Titan is closed. Mercury-SOL next.**
