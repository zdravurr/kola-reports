# titan-2-4-interim-advisor-closing-too-early-n4-of-10

_2026-08-01 12:45 UTC_

---

# TITAN §2.4 — INTERIM READ ON THE EXIT ADVISOR (n = 4 of ~10)

_2026-08-01 12:40 UTC · HEAD `54dc734` · LIVE, real money · READ-ONLY, nothing changed_

## DECISION LINE

**No conclusion is available and none is offered. n = 4 of ~10.**

On the sample that exists the advisor is **ahead** of the held branch — **+1.585 USDT net, 3 positions
improved, 1 worsened** — which is the opposite sign to the operator's impression. But the operator's
impression is **also correct about the shape**: three of the four closes are small losses taken with
**64–79% of the position's allowed room still unused**, and the fourth close was followed by a
re-entry **10.1 minutes later, on the same side, on an IDENTICAL cascade tier set**.

The net is positive only because **one winner (+2.30) covers three losers (−0.82, −0.53, −0.61)**.
Four numbers cannot tell those two stories apart. **Do not act on this file.**

Two findings below are **not** interim and do not depend on n:
- 🔴 **Nothing prevents re-entry after an advisor close** (§3c) — and the two portfolio brakes that
  might have are **structurally inert**: they have read **one row since 2026-05-11**.
- 🔴 The advisor uses **remaining stop room as an argument to HOLD in 15 of 23 holds**, and inverts
  the same quantity to close at 0.64R (§5).

---

## 0. THE CRITERION, VERBATIM, AND THE WINDOW

From OPEN-ITEMS §2.4 (replaced 2026-07-30 11:10 UTC):

> For every position the advisor CLOSES, replay from **real 5m candles** what the unchanged contract
> would have done had the position been held — **stop, breakeven, trail, LONG partial, and any
> intrabar ambiguity resolved ADVERSELY** — and record **advisor-close vs held-branch** in USDT.
> It stays live only if, over the first **~10 advisor-closed positions**, the advisor beats the
> held branch **both in total USDT and in positions improved**.
> **No partial credit. No re-cutting the sample. Every advisor close counts** — not its best ones.

**Window start: `1161802`, restarted 2026-07-30 14:10:59 UTC** (§2.4-OP·2 — the ADX-window fix commit
is what starts the clock). Advisor armed earlier, at `81875c9` 11:32:18.

**Admissibility of vpos 87 — checked, not assumed.** It opened 12:05, *before* the window. It is
**admissible**, and here is the evidence rather than the inference: its closing consult read
`smart_exit_dryrun_samples.adx_window = 200` (row 258, 02:06:46), the entry-side figure comes from
`trades.srv_adx_1h` which was always on `CANDLE_LIMIT`, and the prompt's cross-window NOTE
correspondingly did **not** fire. Its `virtual_positions.entry_adx_1h_window` is NULL, but that
column feeds the **recheck** rule, which was already `done`. Entry-side conditions are explicitly
**not** frozen by §2.4-OP. A **3-position sensitivity** (opened *and* closed in-window) is given in §2.

**Replay validated before it was trusted (§0 standing methodology).** The engine first reproduced the
two **mechanical** closes from candles alone: vpos 85 → `sl` in the 16:40 bar (actual 16:42:36), vpos
86 → `sl` in the 11:50 bar (actual 11:50:48). **2 of 2, correct reason, correct bar.** Price differs
only by the fill-vs-trigger gap (−0.4 pts on 85, +34.1 on 86, the known basis gap). A replay that
could not reproduce the past would have no standing here.

---

## 1. EVERY ADVISOR CLOSE SO FAR

All four positions ever closed with `close_reason='ai_exit'`. Size 0.0023 BTC, ~$146 notional each.

| vpos | side | entry | exit | R at close | stop then | **room UNUSED** | held | trigger | conf |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| **87** | LONG | 64838.7 | 64544.3 | **−0.364R** | 64028.8 | **0.636R = 64%** | 842 min | hourly | 0.72 |
| **88** | SHORT | 63643.2 | 63810.4 | **−0.215R** | 64422.3 | **0.785R = 79%** | 60 min | hourly | 0.72 |
| **89** | SHORT | 63700.1 | 62635.9 | **+1.474R** | 63572.7 (BE) | 1.297R = 130% | 115 min | 15m_exit_confirm | 0.72 |
| **90** | SHORT | 62618.4 | 62827.1 | **−0.239R** | 63491.9 | **0.761R = 76%** | 120 min | hourly | 0.72 |

Net P&L: −0.8191 · −0.5311 · **+2.3024** · −0.6099 = **+0.3423 USDT**.
Every verdict came at **confidence 0.72** — the advisor has never once closed at any other confidence.

**Verbatim reasons**

- **87** — *"Entry thesis broken. 15m/5m shifted to BEAR (was BULL). ADX15m=26.2 confirms momentum
  reversal. Order book flipped: supporting wall collapsed (5.0x→0.0x), opposing wall reinforced (7.4x,
  70th pct). Imbalance at 90th pct (extreme) now opposes position. Peak MFE +0.61R gave back 0.98R.
  Regime changed from TREND to BEAR at multiple TFs. **Stop only 0.64R away; risk/reward unfavorable.**"*
- **88** — *"Entry thesis has deteriorated significantly. 15m reversal-up weight (1.0) now actively
  opposes the SHORT, and 5m structure has flipped bullish (new imbalance, I-CHOCH, OB creation all
  against position). **ADX15m spiked to 36.5** indicating strong directional conviction—upward.
  Supporting wall thinned 5.7→4.8 while opposing wall strengthened (62nd pct). 1h regime shifted to
  neutral/bull."*
- **89** — *"Entry thesis deteriorated. 5m regime reversed sharply: 4 consecutive bullish OBs/breakers
  contradict original bearish OB setup. 15m/5m SHORT agreement dissolved—both now neutral. **ADX15m
  spiked to 31.1** (volatility regime change), while ADX1h falling. Book imbalance at 79th pct
  (extremely bid-heavy) is unstable vs entry's 93pct baseline. Supporting wall thinned 5.6→5.0."*
- **90** — *"Entry thesis has degraded significantly. 5m/15m shifted to neutral (were SHORT/HyperWave
  at entry); position now sits within bullish OBs repeatedly (16m, 10m, 6m, 1m)—structural rejection
  of short thesis. **ADX15m spiked to 49.5** (entry was 23.0) on neutral regime, suggesting momentum
  exhaustion rather than continuation. Supporting wall thinned 4.6→4.5, opposing wall equally thin."*

**Structural observation, independent of n: three of four closes fired on the `hourly` clock.** vpos 88
closed at its **first** hourly consult (60 min); vpos 90 at its **third** (120 min). The exit time is
set by the **consult cadence**, not by the market. Related and worth recording: a consult also fires
**8–25 seconds after entry** on every position (rows 19714, 20007, 20055, 20101). All four were
`hold`, but the advisor is structurally capable of closing a position seconds after it opens.

---

## 2. THE COUNTERFACTUAL — HELD BRANCH FROM REAL 5m CANDLES

**Contract mirrored from `virtual_trader._process_position`**: original stop → +1R breakeven
(entry × 0.002) → trail (`water_mark × (1 ∓ trail_pct/100)`, armed only post-breakeven) → LONG partial
(1/3 at +1R). Each held branch is **seeded with the position's real state at the close** (vpos 89 was
already breakeven-armed at 63572.7 with water mark 62474.7 — restarting it from entry would have been
wrong). **Intrabar strictly adverse**: the adverse extreme is applied *before* the favourable one and
**re-applied after it**, so a trail ratcheted by the same bar's wick can still be hit by that wick.
858 real 5m BingX candles, 2026-07-29 13:00 → 2026-08-01 12:25.

| vpos | side | held branch outcome | advisor net | held net | **advisor − held** |
|---|---|---|---:|---:|---:|
| 87 | LONG | `sl` @ 64028.8, bar 07-31 07:05 | −0.8191 | −2.0110 | **+1.1919 (+0.640R)** |
| 88 | SHORT | breakeven 07-31 14:05 → `trail` @ 63192.2, bar 17:50 | −0.5311 | **+0.8914** | **−1.4225 (−0.794R)** |
| 89 | SHORT | `trail` @ 63171.3, bar 07-31 17:50 | +2.3024 | +1.0703 | **+1.2321 (+0.742R)** |
| 90 | SHORT | 🔴 **STILL OPEN** at 63074.5 (marked to 08-01 12:25) | −0.6099 | −1.1936 | **+0.5837 (+0.291R)** |

**NET n=4: advisor +0.3423 vs held −1.2429 → advisor +1.5852 USDT. Improved 3, worsened 1.**

**Sensitivity, 3 positions opened *and* closed in-window (87 excluded):** advisor **+0.3933 USDT**,
improved **2 of 3**, worsened 1. Same sign, a quarter of the margin, and it turns on the single
winner.

### What this number is NOT

- 🔴 **vpos 90's held branch never terminated.** It is marked to market 20.0 h later, not resolved.
  One of four datapoints is **incomplete**, and its sign can still change.
- 🔴 **The held branches are mutually exclusive.** `MAX_POSITIONS_PER_SIDE = 1`. Had vpos 88 been
  held it would have run to 07-31 **17:50** — so **vpos 89 and vpos 90 could never have opened**. As a
  portfolio, "hold 88" yields **+0.8914** against the actual three-trade short sequence of
  **+1.1614**. Per-position arithmetic is what §2.4 asks for and is what is reported; it is not a
  portfolio result and must not be read as one.
- **Funding is not ledgered on the held branch** and a held branch that a *later* advisor verdict
  would have closed is not modelled. Both bias **toward the held branch, i.e. against the advisor** —
  the safe direction, as §2.4 states. Fills are taken at the stop/trail trigger price.

---

## 3. THE CHURN

### a) What followed each close

| closed | → opened | gap | side | identical tier set? |
|---|---|---:|---|---|
| 87 LONG 02:06:51 | 88 SHORT 09:35:18 | 448.5 min | opposite | no |
| 88 SHORT 10:35:35 | 89 SHORT 12:20:15 | 104.7 min | **same** | no (15m tier differs) |
| **89 SHORT 14:15:13** | **90 SHORT 14:25:19** | **10.1 min** | **same** | 🔴 **YES — all three identical** |
| 90 SHORT 16:25:42 | — | none in 20.0 h | — | — |

**Same-side entries following an advisor close: within 5 min — 0 of 4. Within 15 min — 1 of 4.
Within 60 min — 1 of 4.**

🔴 **The 89 → 90 case is the structural one.** The advisor closed vpos 89 at 14:15:13 saying *"15m/5m
SHORT agreement dissolved—both now neutral"*. **10 minutes 6 seconds later** the entry path opened
vpos 90 SHORT on **1H Smart Trail Bearish (0.9) + 15m HyperWave Signal Down (0.7) + 5m Within Bearish
OB (0.7)** — the **same three tier names** that opened vpos 89, with the **same 1H tier instance still
live** (age 3.3 h at 89's entry, 5.4 h at 90's — 2.1 h apart, matching the gap between entries).
The advisor's close verdict reaches the entry path in no form whatsoever.

*Confound, stated:* `dee6cee` raised the confluence bar 2.0 → 3.0 and went live at the 22:24:27
restart on 07-30. All three same-side entries above occurred **under the 3.0 bar** — so the 10-minute
re-entry cleared the *raised* bar, and the 20-hour drought since is measured under it too.

### b) Fees

| vpos | notional | entry fee | exit fee | round trip | as R |
|---|---:|---:|---:|---:|---:|
| 87 | $149.13 | 0.0746 | 0.0742 | 0.1488 | 0.080R |
| 88 | $146.38 | 0.0732 | 0.0734 | 0.1466 | 0.082R |
| 89 | $146.51 | 0.0733 | 0.0720 | 0.1453 | 0.087R |
| 90 | $144.02 | 0.0720 | 0.0723 | 0.1443 | 0.072R |

**Four advisor round trips paid 0.5849 USDT.** Mean **0.1462 per round trip** on ~$146 — the
operator's ~$0.15 estimate is right. A single held position would have paid **0.1488**, so the churn
has cost **+0.4361 USDT in fees alone**, against a total realised P&L of **+0.3423**.

**Fees exceed the realised P&L of the entire sample.** Each round trip burns **~0.08R** before the
advisor's judgement is worth anything.

### c) Is there any mechanism preventing immediate re-entry?

🔴 **No. None exists.** An `ai_exit` close writes `close_reason` on the position row and nothing else;
no cooldown, no lockout, no flag, no signal suppression is keyed on it. The entry path never learns a
close happened. **This is a design gap that stands independent of whether the advisor's judgement is
good** — a perfectly correct close can be undone 10 minutes later by the same live tier set, and on
07-31 it was.

The nearest candidate brake is `risk_manager.loss_streak_halt()` (3 consecutive losses → 4 h
cooldown), wired into `check_risk()` and called on every entry. **It is structurally inert, and this
was verified rather than reasoned:**

- It reads `trades` rows whose `signal_type` is in `_CLOSE_SIGNAL_TYPES =
  ('5m_group_b','close_long','close_short','exit_long','exit_short')`.
- Close P&L is written back onto the **entry** row, whose `signal_type` is `open_long` / `open_short`.
- **The whole database contains exactly one matching row: id 186, `close_long`, 2026-05-11 21:18:16.**
- So `len(rows) < LOSS_STREAK_THRESHOLD` (1 < 3) → it returns `False, '1/3 closes recorded'` **on
  every call**. It has been unable to halt anything for **two and a half months**.
- `daily_loss_halt()` reads the same set via `daily_realized_pnl()` → always `0.0` → takes the
  `pnl >= 0` branch and never halts either.

And even had it worked, it would not have stopped the 89 → 90 re-entry: **vpos 89 was a winner**, so
the streak was broken by design.

*Reported as found. No fix is proposed here — this pass is read-only.*

---

## 4. WHAT IS IT REACTING TO

**27 consults since arming** (4 close, 23 hold); **23 inside the §2.4 window** (4 close, 19 hold).

Citation counts alone are **not** the answer, because the prompt asks the question and nearly every
input is named every time:

| cited | close (n=4) | hold (n=23) |
|---|---:|---:|
| "entry thesis" framing | 4 | 23 |
| 15m | 4 | 23 |
| 5m structure (OB / I-CHOCH) | 4 | 23 |
| ADX (any TF) | 4 | 23 |
| a wall | 4 | 22 |
| imbalance | 3 | 17 |
| the word "regime" | 4 | 16 |
| 1h / 4h | 2 | 16 |
| MFE / giveback | 1 | 8 |
| stop distance / room | 1 | 18 |

**What actually discriminates close from hold:**

| discriminator | close | hold |
|---|---:|---:|
| 🔴 **lower-TF regime FLIPPED / REVERSED / dissolved against the position** | **4 / 4** | **5 / 23** |
| **ADX15m explicitly "spiked"** | **3 / 4** | 2 / 23 |
| wall collapsed / thinned | 4 / 4 | 12 / 23 |
| "intact / persists / remains" wording | 0 / 4 | 23 / 23 |

**One input dominates and it is named: the 15m/5m tier direction flipping against the position —
4 of 4 closes, 5 of 23 holds.** Every close opens with *"Entry thesis broken / deteriorated /
degraded"* and every hold with *"Entry thesis (partially) intact"* — the verdict is the
entry-thesis check, and what breaks that check is the lower-TF flip. **It is not the book**: walls are
cited in 4/4 closes but also 22/23 holds, and imbalance in 3/4 vs 17/23 — neither separates anything.
The second discriminator is a **rising ADX15m**, read as reversal (88), volatility-regime change (89)
and exhaustion (90) — three different meanings for one rising number.

**This is the same input the entry cascade uses.** The advisor closes on a 15m/5m flip; the entry path
opens on a 15m/5m tier. That is the mechanical reason §3a's 10-minute re-entry is not an accident.

---

## 5. THE THRESHOLD QUESTION

**Does it receive distance-to-SL? Yes — twice per prompt**, verbatim:

```
  Current stop: 63491.9  ->  +0.74R away
...
If you HOLD: the stop-loss is in place. The trailing stop is NOT ARMED — it arms only at +1R...
  Current stop: 63491.9 (+0.74R away).
```

**Does it reference it? Constantly — and mostly as a reason to HOLD.** 15 of 23 holds cite the
remaining room explicitly as the justification:

> *"stop at +1.02R provides safety"* · *"stop 1.17R away provides good risk/reward"* · *"Only −0.11R
> loss with stop at +0.89R away provides favorable risk/reward"* · *"unrealised only −0.05R, stop
> 0.95R away with room"* · *"only 0.01R underwater with stop +0.99R away—minimal loss, wide
> protection"*

**And exactly one close inverts the same quantity:** vpos 87 — *"**Stop only 0.64R away;
risk/reward unfavorable**"*. The advisor calls 0.89R–1.04R "favorable risk/reward" and "wide
protection", then calls **0.64R** "only ... unfavorable". **The other three closes do not mention the
stop at all.**

**Do close verdicts cluster at a particular R? They appear to — and the appearance cannot be
trusted.** The four closes sit at unrealised **−0.36 / −0.22 / +1.50 / −0.26**; three of four in a
tight −0.22…−0.36R band with 64–79% of room unused. But across **all 27 consults, the deepest adverse
reading the advisor has ever been shown is −0.36R**. 25 of 27 consults land within ±0.4R of flat.
**There is no consult at −0.5R, −0.7R or −0.9R that it held through** — so "it closes at about −0.3R"
is indistinguishable from "−0.3R is the worst it has ever been asked about." A threshold cannot be
read out of a distribution with no tail. Recorded as a question the window has not yet answered.

---

## 6. HONEST STATE

| | |
|---|---|
| advisor closes to date | **4** |
| §2.4-admissible | **4 of ~10** (3 on the strict opened-and-closed-in-window cut) |
| held branches fully resolved | **3 of 4** — vpos 90's is still open |
| distinct winners in the sample | **1** |
| consults since arming | 27 (4 close, 23 hold) |
| window opened | 2026-07-30 14:10:59 UTC (`1161802` restart) |
| window elapsed | ~46 h · last entry 07-31 16:25, **20.0 h of no trading since** |

**The sample cannot support a conclusion, and this reading must not become the twelfth dead
hypothesis.** Concretely:

1. **n = 4, and the sign rests on one trade.** Remove vpos 89 (+1.23) and the advisor is +0.35 over
   three closes; remove vpos 87 as well and it is **−0.84 over two**. A result that changes sign on
   any single position is not a result.
2. **One of the four held branches has not finished.** vpos 90 is marked to market, not resolved.
3. **Both directions of the operator's observation are visible and they disagree.** The *shape* is
   real — three small losses taken with 64–79% of room unused, one re-entry 10 minutes later on an
   identical tier set. The *net* is positive. Four trades cannot separate "cuts losers early and it
   works" from "cuts losers early and one lucky winner is paying for it".
4. **Six more advisor closes are needed** at the current bar, and the bar does not move. At the
   observed rate (4 closes in 46 h, then 20 h idle) that is roughly **3–7 more days** of live
   trading, assuming entries resume.
5. **The window must not be voided to get there.** §2.4-OP·2 is explicit: a defect found *during* the
   window is recorded as a caveat, not reset. Nothing in this file changes a figure the advisor
   reads, so the window stands.

**What would make this conclusive:** the remaining six closes under the frozen prompt, with each
held branch run to a real termination rather than a mark. Nothing less.

---

## WHAT I DID NOT DO

- No code, config, DB or flag was touched. Every query ran against `file:trades.db?mode=ro`.
- No fix, patch or proposal for the re-entry gap or the inert risk brakes — reported as found.
- No re-cutting of the sample, no exclusion of any advisor close, no partial credit.
- The window was not voided and no count was restarted.
