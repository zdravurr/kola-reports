# sol-daily-loss-brake-measured

_2026-08-01 21:40 UTC_

---

# MERCURY-SOL — THE DAILY-LOSS BRAKE, MEASURED. **READ-ONLY, NOTHING CHANGED.**

No file was modified, no service restarted, no external market fetch made. Every number below
comes from `trades.db` read `?mode=ro` plus a price series reconstructed **from local data**
(51,237 points from `skip_attribution.price_at_skip` + `skip_drift_samples.sample_price`, covering
2026-06-07 → 2026-08-01). SOL is PAPER, the entry prompt is frozen, the window stands at 4 of 200,
vpos 25 untouched. Titan untouched.

---

# THE ANSWER FIRST

**Three findings, in descending order of how much they should change your thinking.**

1. 🔴 **The brake's own decisions were never recorded.** `risk_reason` goes to Telegram and the
   HTTP response and is **written nowhere** — 0 of 289 rows carry it, `skip_attribution` never
   tracked `risk_halt` at all, and the journal has **zero** "RISK HALT" lines. The decomposition you
   asked for **cannot be read**; it had to be *reconstructed*. I label it as such throughout.

2. 🔴 **De-confounded, the brake shows no measurable effect either way.** Halted signals drift
   **−0.128% at 4h**, which looks like the brake earning its keep — but the same-day non-halted
   signals drift **−0.067%**, and **the excess is not distinguishable from zero at any horizon.**
   The negative drift is explained by *those being bad days*, not by the brake selecting worse
   signals. **It neither demonstrably helped nor demonstrably hurt. I am recording the null.**

3. 🔴 **At this trade frequency the unit barely matters, because a "day" is one trade.**
   **14 of 16 trading days have exactly one close**; the worst day in the entire book is
   **−1.15R**. Every candidate either collapses onto one of two behaviours or **never fires at
   all**. The current dollar rule turns out to be *operationally identical* to "halt after the
   first losing close of the day" — same 11 days, same 996 signals, same drift, to the digit.

**So the question "what unit should the brake use" is less consequential than it looked. The
question underneath it is whether a *daily* brake is the right instrument for a book that takes
about one trade a day.**

---

# §1 — WHAT THE BRAKE ACTUALLY DID

## 1.1 The decomposition you asked for is not stored

```python
risk_ok, risk_reason = _risk_check(symbol, position_side)
if not risk_ok:
    update_trade(row_id, status='risk_halt', combo_key=combo,
                 confluence_score=adj_score)      # ← risk_reason is NOT written
```

| recovery path | result |
|---|---|
| `trades.error` / `trades.ai_reason` on the 289 rows | **0 of 289** populated |
| `skip_attribution` | tracks only `htf_blocked` (4,177), `ai_skipped` (2,883), `below_threshold` (1,545) — **`risk_halt` was never in scope** |
| systemd journal | **0** "RISK HALT" lines (it is a `send_tg` call, not a `print`) |

**This is a finding in its own right: the risk gate is the one gate in the system that cannot say
why it fired.** Every other gate is attributable and drift-tracked; this one is neither.

## 1.2 Reconstruction — 98.3% is the daily-loss brake

The condition is recomputable: for each `risk_halt` row, was the day's cumulative closed PnL
already ≤ −$40.60 at that moment? `_risk_check` evaluates macro → DXY → daily-loss → position cap
→ loss streak, and **`DXY_HALT_DRYRUN = True`, so DXY can never block.**

```
TOTAL risk_halt rows: 289
  daily-loss condition WAS TRUE at that moment : 284  (98.3%)  on 9 distinct days
  daily-loss condition was FALSE (other gate)  :   5  ( 1.7%)  on 4 distinct days
```

| day | entry opportunities refused |
|---|---|
| 2026-06-21 | 36 |
| 2026-06-22 | 56 |
| 2026-06-24 | 4 |
| 2026-07-10 | 35 |
| 2026-07-16 | 36 |
| 2026-07-17 | 21 |
| 2026-07-23 | 38 |
| 2026-07-28 | 22 |
| 2026-07-30 | 36 |
| **total** | **284 on 9 days** |

The other 5 (2026-06-10, 07-14, 07-20, 07-21 — one or two each) are position-cap or loss-streak.

**Two loss days produced no halts at all** (2026-06-20 −$177.34, 2026-06-25 −$405.97): the loss
closed with no further signal reaching the risk gate that day.

**Caveat, stated plainly:** this is inference from a recomputable condition, not a record of what
fired. Where the daily-loss condition and another gate were both true, the reconstruction credits
daily-loss. Given 98.3% concentration and DXY being inert, I am confident in the shape — but it is
not the same thing as having logged it.

---

# §2 — WHAT IT COST: THE NULL RESULT

Method identical to every other gate — `drift_pct` signed toward the would-be direction, positive
= the refused signal would have moved our way (`skip_attribution._compute_drift_pct`).

| population | 4h | 12h | 24h |
|---|---|---|---|
| **RISK_HALT (actual, n≈250)** | **−0.1284% ±0.1060** ✅ sig | −0.1709% ±0.2376 | −0.1383% ±0.3768 |
| **SAME-DAY other skips (n=2,133)** | −0.0674% ±0.0459 ✅ sig | −0.1303% ±0.0730 ✅ sig | −0.0742% ±0.0893 |
| **BASELINE all skips (n≈8,500)** | +0.0045% ±0.0248 | −0.0328% ±0.0397 | −0.0259% ±0.0547 |
| 🔴 **EXCESS (halt − same-day)** | **−0.0610pp ±0.1155** | **−0.0407pp ±0.2486** | **−0.0641pp ±0.3873** |

*(±  = 95% CI on the mean.)*

**Against the whole-period baseline the brake looks good** — it refused signals drifting −0.13%
where the average skip drifts ~0.00%. That is the naive read, and it is confounded: **halt days
are by construction loss days**, and everything on those days drifted negative.

**De-confounded against the same days, the effect vanishes.** The excess CI straddles zero at all
three horizons. **The brake was not selecting worse-than-average signals on those days; it was
refusing ordinary signals on bad days.**

## What this means for your question

You framed it as: *if it refused losers it was harmless; if it refused winners the mis-calibration
has a price.* The measured answer is **neither**:

- **It did not refuse winners.** No horizon shows positive drift. There is no measurable cost.
- **It did not meaningfully refuse losers either.** Once the day is controlled for, its selection
  is indistinguishable from the other 2,133 signals it sat alongside.

**The brake's 284 refusals bought nothing and cost nothing that this data can detect.** For
comparison, `htf_blocked` — the gate that *does* work — runs −0.0881 / −0.2189 / −0.1889 across
4,177 samples, and its 12h/24h figures are far outside their CIs. That is what a gate earning its
keep looks like. The daily-loss brake does not look like that.

---

# §3 — CANDIDATE UNITS, REPLAYED OVER THE WHOLE BOOK

**The structural fact that dominates everything below:**

| | |
|---|---|
| trading days with closes | **16** |
| days with exactly **1** close | **14** |
| days with 2 closes | **2** |
| worst single day, in R | **−1.15R** |
| R distribution of the 18 closes | worst −1.15R, avg −0.26R, best +2.09R, 11 losers |

**A day is one trade.** So any rule requiring ≥1.5R of daily loss, or ≥2 losing closes, **can never
fire on this book** — not as a calibration failure but by construction.

Replay: for each rule, find the halt moment per day, then count every `open_long`/`open_short`
opportunity after it and measure its drift.

| candidate | halt days | signals refused | 4h drift | 12h | 24h |
|---|---|---|---|---|---|
| **CURRENT** — day loss ≥ 5% of REAL equity ($40.60) | **11/16** | **996** | +0.0013% ±0.0604 | −0.0536% ±0.1289 | −0.0290% ±0.1897 |
| **C₁** — 1 losing close in a day | **11/16** | **996** | +0.0013% ±0.0604 | −0.0536% ±0.1289 | −0.0290% ±0.1897 |
| **A₀.₅** — day loss ≥ 0.5R | 10/16 | 890 | −0.0063% ±0.0606 | −0.0520% ±0.1371 | −0.0457% ±0.1976 |
| **A₀.₇₅ / A₁.₀** — day loss ≥ 0.75R or 1R | **8/16** | **836** | −0.0024% ±0.0642 | −0.0623% ±0.1453 | −0.0551% ±0.2102 |
| **B₁.₀% / B₁.₅%** — ≥1–1.5% of per-trade notional | 9/16 | 836 | −0.0024% ±0.0642 | −0.0623% ±0.1453 | −0.0551% ±0.2102 |
| **D** — hybrid: ≥1R **and** ≥1 losing close | **8/16** | **836** | −0.0024% ±0.0642 | −0.0623% ±0.1453 | −0.0551% ±0.2102 |
| **B₂%** — ≥2% of notional | 7/16 | 750 | −0.0197% ±0.0713 | −0.0717% ±0.1630 | −0.0818% ±0.2355 |
| **B₃%** — ≥3% of notional | 1/16 | 9 | *(n=9 — not interpretable)* | | |
| **A₁.₅ / C₂ / B₅%** — ≥1.5R, 2 losing closes, ≥5% notional | **0/16** | **0** | never fires | | |

## Three things to read off this table

**1. The current dollar rule is exactly "halt after the first losing close of the day."** CURRENT
and C₁ are identical to every digit — same 11 days, same 996 signals, same drift. The $40.60 limit
is smaller than a single average stop-out ($213.86), so the first loser always trips it. **That is
what "0.19 stop-outs" means in practice.**

**2. A₀.₇₅, A₁.₀, B₁%, B₁.₅% and the hybrid D are the same rule in different clothes** — 836
signals, 8–9 days, identical drift. On a one-trade-a-day book, "one full R of loss", "1% of
notional" and "one losing trade that hit its stop" are the same event.

**3. Not one candidate shows a drift distinguishable from zero.** Every CI in the table straddles
0. **Tightening or loosening the brake across this whole range neither saves nor costs anything
measurable.** The choice cannot be made on historical P&L evidence, because the evidence is null —
it has to be made on what you want the brake *for*.

---

# §4 — THE LIVE QUESTION: ONE RULE OR TWO?

**Plainly: they should be two rules with the same intent, because they protect two different
things — and they can be kept comparable by expressing both in R.**

| | paper | live |
|---|---|---|
| what is at risk | **nothing** — the account is not traded | **real capital** |
| what the brake is for | stopping a **strategy** bleeding: is this system broken today? | stopping **ruin**: preserving the ability to trade tomorrow |
| the natural unit | **R** — strategy-relative, size-independent | **% of equity** — capital-relative, the only unit ruin is denominated in |

"5% of equity" is the **right framing in live** and you are right that it stays right even when
dormant — ruin risk genuinely is a percentage of the balance, and a rule that rarely fires at $100
is a rule that will start mattering the moment size grows. It should not be discarded for being
quiet at small size.

But the **same number is meaningless in paper**, where the equity it references is not the equity
being risked. That is not a calibration error, it is a category error: the paper book's $10,000
notional has no relationship to the $811.90 balance.

## How two rules stay comparable

**Express the paper rule in R, and give the live rule an R expression alongside its equity
expression.** Then a single sentence describes both books: *"the brake halts after N R of loss in
a day."* In live it additionally halts on the equity floor, whichever comes first.

- comparability is direct — both books report "R allowed before halt", so paper results transfer;
- live keeps a **hard capital floor** that no R-based rule can talk it out of;
- the R leg is size-independent, so it survives the $10,000 → $100 change and any later change,
  which is exactly the property the current single constant lacks.

**The shape, not the number: `halt if (day_loss_R ≥ N) or (live and day_loss ≥ P% of equity)`.**
In paper the second clause is absent; in live it is the backstop.

---

# §5 — WHICH I WOULD CHOOSE, AND WHY — BUT THE CHOICE IS YOURS

**I would choose D, the hybrid — an R-based daily limit with a live-only equity backstop —
knowing that on this book it behaves identically to A₁.₀ and B₁%.**

Reasons, in order:

1. **It is the only candidate that is correct in both books.** A₀.₇₅/A₁.₀ alone leaves live with no
   capital floor; the current rule alone is a category error in paper. D is the only shape that
   does not have to be re-derived at the flip.
2. **It is size-independent where it needs to be.** It survives $10,000 → $100 without
   re-calibration — the specific failure that produced this whole investigation.
3. **The historical evidence does not distinguish the alternatives**, so I am choosing on
   *structure*, and saying so rather than dressing a null up as a finding.
4. It requires the two clauses to be **explicitly different in the two modes**, which makes the
   paper/live divergence visible in the code instead of hidden inside one constant — the property
   whose absence caused this.

## 🔴 What I would want you to weigh more than the unit

**On this book the honest observation is that a daily-loss brake is close to a per-trade brake.**
14 of 16 days are a single trade; the worst day ever recorded is −1.15R. Any threshold below ~1R
fires on the first ordinary stop-out; any threshold at or above ~1.5R never fires at all. There is
almost no range in between.

So the real question is not *what unit* but **what you want to happen after one losing trade**:

- if the answer is *"stop for the day"* → the current rule already does that, and the fix is
  cosmetic honesty about what it is;
- if the answer is *"keep trading, that's just one stop-out"* → then the threshold has to sit above
  1R, at which point on this data **it never fires**, and the brake is decorative until trade
  frequency rises;
- if the answer is *"it depends how many trades a day we take"* → then the brake should be
  **frequency-aware**, which none of the four candidates is, and that is a different design.

**No number proposed. Nothing changed.** The measurement says the brake has been neither helping
nor hurting measurably, that its unit is wrong in both directions, and that on current trade
frequency the unit choice matters less than the decision about what should follow a single losing
trade.

---

# APPENDIX — METHOD

- **Price series:** 51,237 local points, 2026-06-07 → 2026-08-01, from `skip_attribution.price_at_skip`
  (8,605) and `skip_drift_samples.sample_price` (42,632). Nearest-neighbour lookup, **±30 min
  tolerance**; samples outside tolerance are dropped, which is why n≈250 rather than 289 for the
  halt population. **No external market fetch was made.**
- **Drift:** `(sample/anchor − 1) × ±1 × 100`, sign toward the would-be direction — the same
  formula `skip_attribution` uses for every other gate.
- **Attribution:** the daily-loss condition recomputed per row from the position ledger
  (`virtual_positions.net_pnl`, closes strictly before the row's timestamp, same UTC day) against
  the live `DAILY_LOSS_PCT_LIMIT = 0.05` and measured equity `$811.90195236`.
- **Replay:** per rule, the halt moment is the close at which the rule's condition first becomes
  true that day; refused = every `open_long`/`open_short` row later that day. This counts **all**
  opportunities after the halt, not only those that reached the risk gate — which is why the replay
  populations (836–996) exceed the actual `risk_halt` count (289): most were stopped earlier by
  `htf_blocked`, `ai_skipped` or `below_threshold`.
- **CIs:** 95% on the mean (1.96 × SE). "Significant" means the interval excludes zero.
