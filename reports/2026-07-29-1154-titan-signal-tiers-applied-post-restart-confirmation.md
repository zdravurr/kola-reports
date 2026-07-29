# titan-signal-tiers-APPLIED-post-restart-confirmation

_2026-07-29 11:54 UTC_

---

**YES — APPLIED.** Commit **`7285c5d`**, pushed to `origin/main`. `titan.service` restarted
**2026-07-29 11:36:09 UTC**, worker 4044689 booted clean. Rollback: tag
`pre-signal-tiers-20260729T113516Z` + `main.py.bak_tiers_20260729T113516Z` /
`claude_advisor.py.bak_tiers_20260729T113516Z`.

Boot log clean — reconcile done, `breakeven_worker`, `virtual_trader` and the `OB-DENSITY`
collector all started, zero errors or tracebacks. Schema migrated: `trades.entry_tiers_json`
present, 148 columns.

---

## 1. A REAL RENDERED ENTRY PROMPT — ALL THREE TIERS COMPLETE

Built by the **deployed code** (`/root/titan-bot/claude_advisor.py` at `7285c5d`) against the
**live** state machine, the **live** matrix and the **live** OKX book at 11:51 UTC. Only the
Anthropic API call is stubbed — every byte below is what the advisor receives.

**Honest label:** this is a forced render, not a stored decision row. No natural advisor consult has
landed since the restart — the four signals that arrived (11:40, 11:45) were all `htf_blocked`, and
those never reach the advisor. A monitor is armed for the first real one.

Live slots at render time:

```
1h_context   dir=LONG     name='Smart Trail Bullish'    ts=2026-07-29T08:00:14Z
15m_confirm  dir=SHORT    name='HyperWave Signal Down'  ts=2026-07-29T11:00:08Z
5m_trigger   dir=LONG     name='Within Bullish OB'      ts=2026-07-29T11:45:03Z
```

```
Symbol: BTC/USDT:USDT
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  Smart Trail Bullish  (direction withheld (AI_ADVISOR_HIDE_1H), weight 0.9, last set 3.9h ago)
  15m: HyperWave Signal Down  (SHORT, weight 0.7, last set 52m ago)
  5m:  Within Bullish OB  (LONG, weight 0.7, last set 8m ago, trigger-capable, NOT counted by the gate — matrix TTL expired)
  Agreement: 5m points LONG; 15m points SHORT; vs the proposed LONG: 5m agree, 15m OPPOSE.
Combo weight: 1.00 (1.0 baseline; <1 = historical loser, >1 = winner)
ATR(14) 5m: 62.3935  |  Volume ratio 5m: 0.48x avg
Volatility / regime (multi-TF):
  ADX(14): 1h 18.5 | 15m 26.4  (higher = stronger trend; ~<20-23 = weak/ranging)
  ATR% of price: 1h 0.485% | 15m 0.199% | 5m 0.097%
  EMA-gap: 1h 0.316% (Expanding) | 15m 0.085% (Contracting)  (Contracting/Flat = compression)
  Market regime: TREND | MTF alignment score: 3
Higher Timeframes Trend (OHLCV-derived EMA/ADX, independent of LuxAlgo signals):
  1d: NEUTRAL, ADX 16.0, EMA-gap 0.301% (Contracting)
  4h: NEUTRAL, ADX 25.2, EMA-gap 0.227% (Contracting)
  1h: BULL, ADX 18.5, EMA-gap 0.316% (Expanding)
  15m: NEUTRAL, ADX 26.4, EMA-gap 0.085% (Contracting)
  5m: BEAR, ADX 18.1, EMA-gap 0.056% (Expanding)
  MTF alignment vs LONG: 3/4 (4H/1H/15m/5m; excludes 1d)
Long/Short ratio: n/a
Order book (pre-trade, 8000 levels):
  Mid: $64,477.35  |  Imbalance ±1%: 0.51 (bid-heavy)  — 68th pct
  Bid walls (>4x avg bucket vol): $64,252.50 (×9.9), $64,187.50 (×4.9), $64,002.50 (×6.8)  — largest ×9.9 = 91th pct
  Ask walls (>4x avg bucket vol): $64,492.50 (×4.8), $64,902.50 (×5.1)  — largest ×5.1 = 33th pct
  Book depth: 3,042 BTC — 53th pct, sampled 2s ago
Order-book PERCENTILE scale (baseline: 23178 snapshots of this same OKX depth-4000 book)
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile: ~50th percentile is ORDINARY,
  not significant.

The entry gate has already passed. Tier agreement is stated in the SIGNAL TIERS block above — read
it there rather than assuming all three agree. Decide whether the bot should execute the DCA entry now.
```

🔴 **This render happens to be the exact case that justified the change.** The 15m tier points
**SHORT** while the 5m points **LONG** — they *disagree*. Under the old prompt this moment would
have printed `The 3 timeframes are aligned (confluence has already passed)`. It now says, in one
line, that one tier agrees and one opposes.

The remaining `n/a` on the prompt — `Long/Short ratio: n/a` — is the BingX account ratio, not a
tier. That field is genuinely unavailable and correctly says so.

The structured record persisted alongside it:

```json
{"tiers": {"1H": {"label": "1H", "present": true, "name": "Smart Trail Bullish",
 "direction": "direction withheld (AI_ADVISOR_HIDE_1H)", "weight": 0.9, ...
```

## 2. EXIT ADVISOR — ENTRY-THESIS LINE FOR vpos 84

Live call to the deployed `main._entry_signals_for(vpos 84)`:

```
  1H:  Bullish Confirmation  (legacy record — direction, weight and age were not captured before 2026-07-29)
  15m: ABSENT  (legacy record)
  5m:  Bullish OB Mitigated  (legacy record)
```

**What it was before the patch:**

```
  1H trend set by:   Bullish Confirmation
  15m confirmed by:  n/a
  5m triggered by:   Bullish OB Mitigated
```

**Stating the limit plainly rather than dressing it up:** vpos 84 opened 2026-07-28 17:00, *before*
the patch, so it has **no `entry_tiers_json`** and correctly falls to the legacy path. All three
tiers are named, and `n/a` is gone — but **direction, weight and age cannot be shown for it**,
because that record did not exist when it opened. The full three-tier record with direction, weight
and age appears on the **first position opened from now on**. `entry_tiers_json` is currently
non-null on 0 rows, as expected — no entry has executed since 11:36.

## 3. NO TIER CAN RENDER `n/a` — PROVEN BY CONSTRUCTION

Exhaustive render over **648** combinations — 6 signal names (including `None` and an unknown
signal) × 4 directions (`None`/LONG/SHORT/NEUTRAL) × 3 timestamps (including `None` and a garbage
string) × 3 matrix states × 3 proposed directions:

| check | result |
|---|---|
| tier lines containing `n/a` | **0 of 648** |
| every result JSON-serialisable | yes |
| `entry_thesis_lines()` raised | no |

Static confirmation:

| location | `n/a` occurrences | where |
|---|---|---|
| `signal_tiers.py` | 3 | **docstring only** — lines 5 and 26, describing the old behaviour |
| tier block of `claude_advisor.py` | 2 | **comment only** — line 274 |
| legacy exit path in `main.py` | guarded | `m.group(1) != 'n/a'` → falls through to `ABSENT` (3 occurrences) |

**Zero executable `n/a` in any tier path.** A genuinely empty tier says `ABSENT`.

## 4. FLAGS — ALL UNCHANGED

`config.py` is **not in the diff at all**.

| flag | value |
|---|---|
| `LIVE_TRADING_ENABLED` | **False** |
| `LONG_PARTIAL_ENABLED` / `LEVEL_R` / `FRACTION` | **True** / 1.0 / 1/3 |
| `EXIT_ADVISOR_PAPER_ENABLED` / `DRYRUN` / `ON_15M_CONFIRM` / `HOURLY` | **True / True / True / True** (3600s) |
| `CONFLUENCE_FLAT_THRESHOLD` / `CONFLUENCE_SCORE_THRESHOLD` | **5.0** / 2.0 |
| `WALL_TRAIL_LIVE_ENABLED` | **False** |
| `AI_ADVISOR_HIDE_1H` | **True** |
| `ADX_BELOW_FLOOR` · `SL_ATR_MULT` · `TRAIL_MULT_ATR` | 20.0 · 2.5 · 2.5 |
| `HTF_CASCADE_ENABLED` / `HTF_TOLERATE_NEUTRAL` | True / True |
| `EQH_EQL_SMART_TP_ENABLED` | True *(still unreachable — §2.6, untouched)* |

`AI_ADVISOR_HIDE_1H` was **nearly broken by this patch and is not**: the "the score gate counted
this tier as LONG" clause would have leaked the 1H direction the flag exists to hide. `gate_direction`
is now stripped for the 1H tier only; 15m and 5m keep theirs. Visible in §1 — the 1H line reads
`direction withheld (AI_ADVISOR_HIDE_1H)` and no 1H direction appears anywhere in the prompt.

## 5. SCOPE — PROVEN, NOT ASSERTED

Byte-for-byte comparison of each named region against tag `pre-signal-tiers-20260729T113516Z`:

| function | file | result |
|---|---|---|
| `confluence_check` | `state_machine.py` | **IDENTICAL** |
| `htf_alignment` | `signal_matrix.py` | **IDENTICAL** |
| `_htf_cascade_gate` | `main.py` | **IDENTICAL** |
| `reset_1h_trend` | `state_machine.py` | **IDENTICAL** |
| `_clear_lower_tfs_locked` | `state_machine.py` | **IDENTICAL** |
| `update_slot` | `state_machine.py` | **IDENTICAL** |

`git diff --stat` against the tag for `state_machine.py`, `signal_matrix.py`, `config.py`,
`virtual_trader.py`, `risk_manager.py`, `adaptive_trail.py`, `breakeven_worker.py` → **empty. Zero
changed lines.** SL, trail, breakeven, the LONG partial, the cascade and the score gate are
untouched.

**Mercury-SOL:** `git diff --stat pre-signal-tiers-20260729T113516Z HEAD -- mercury-bot/` → **empty**;
service **active**.

Total diff: **3 files** — `main.py` (+63/-12), `claude_advisor.py` (+110/-50), `signal_tiers.py` (new).

## 6. RECORDED IN OPEN-ITEMS

Working copy `reports/OPEN-ITEMS.md` updated and pushed, with a byte-identical dated snapshot
alongside at **`reports/2026-07-29-1145-open-items.md`** (§8 — the dated path is the one to link).
§2.3 marked **CLOSED** (`8b15ecc`). Three new entries, all **watch, do not act**:

### §2.8 🔴 BEHAVIOURAL CHANGE — WATCH ENTRY FREQUENCY
The advisor now sees `ABSENT` tiers and an honest agreement line where it was previously told
*"The 3 timeframes are aligned"* — false on 14 of 59 executed entries. **It may skip entries it
would have approved. That is the expected consequence of removing a false statement, not a
regression — but it must be measured, not assumed.**
Measure over ~2 weeks from **2026-07-29 11:36 UTC** against the equal-length window before:
the advisor's **skip rate** and the **executed-entry count**. Baseline already computed: over
2026-07-06 → 07-29, **610** signals cleared the score gate and **17** became trades = **2.79%**.
Do not "fix" a drop by reverting — only a drop to near zero, or one with no change in the quality of
what survives, is evidence of a defect.
*Practical note for whoever runs it:* all 2,565 `ai_skipped` rows store `ai_user_prompt`, and it now
contains the tier block, so the comparison can be run straight from the prompts —
`entry_tiers_json` is written only on executed entries.

### §2.9 TWO REGISTRIES DISAGREE BY DESIGN — NOT PROPOSED
`state_machine`'s 15m slot (**4h** TTL, wiped by 1H flip / Group-B Exit) and `signal_matrix`
MOMENTUM (**90 min** TTL, wiped by nothing) hold the same fact and diverge **both ways** — over the
last 20 entries, **2** had an empty slot while the matrix held **3 live** signals, and **6** had a
live slot the matrix had already expired. The patch **reports both** rather than picking one.
**Reconciling them is a cascade-state change and is NOT proposed.**

### §2.10 AGE IS THE AGE OF LAST SET, NOT OF FIRING
`reset_1h_trend()` overwrites the slot timestamp while keeping the name, so a reset tier's age is
the age of the reset. Entry 19021 read *"set 1.0h ago"* for a signal that had fired **2.0h** earlier.
The patch **labels it `last set` rather than lying**, and now prints the direction so a reset tier
shows as `NEUTRAL` instead of reading as live. A proper fix needs a separate `set_at` field in
`state_machine` — **out of scope, deliberately not done**, recorded so it is not rediscovered.

---

## STATE AT CLOSE

`git status` clean · HEAD **`7285c5d`** (was `8b15ecc`) · pushed · `titan.service` **active** since
11:36:09 UTC · collector alive · **Mercury-SOL untouched and active**

**Book: 1 open position** — vpos 84 LONG @ 63,997.3, stop 63,129.9 (original), partial not fired.

**Still outstanding from this work:** a stored advisor-consult row rendered by the live path. Four
signals since restart, all `htf_blocked` — none reached the advisor. The monitor is armed; the first
natural consult will be the last piece of evidence, and it will land in `trades.ai_user_prompt`
whether or not anyone is watching.
