# sol-daily-loss-brake-candidate-d-adopted

_2026-08-01 22:00 UTC_

---

# MERCURY-SOL — CANDIDATE D ADOPTED, AND THE RECORDING GAP CLOSED.

Applied and live since the **20:15:16** restart (worker pid 1173092), **zero tracebacks**. SOL
stays **PAPER**. The entry prompt and its inputs are untouched, **the window was not reset (4 of
200)**. Titan untouched.

```
halt if (day_loss_R >= DAILY_LOSS_R_LIMIT)                          # 3.0R  — BOTH modes
     or (LIVE only and day_loss >= DAILY_LOSS_PCT_LIMIT of equity)  # 5%    — live only
```

---

# 🔴 ONE THING TO REPORT BEFORE THE REST: vpos 25 CLOSED ITSELF

You said *"vpos 25 may still be open; do not disturb it."* **It closed on its own at 20:13:32** —
two minutes before my restart, on the **trail**, by the engine's own poller. I did not touch it.

```
CLOSE vpos=25 SHORT entry=72.47 exit=71.36 size=91.93333333333334
      gross=102.0460 fees=10.9174 net=126.5230 reason=trail
      [incl. partial pnl=+31.7495 fees=3.6449] (close_row=15004)
```

| field | value |
|---|---|
| close | **$71.36**, reason **trail**, at 2026-08-01T20:13:32 |
| **net_pnl** | **+$126.52** = **+1.257R** |
| partial leg | +$31.75 realised at $71.70, folded back exactly once |
| `initial_risk_usdt` | **$100.667** — untouched, so R stays comparable |

**This is the first complete partial-at-arm lifecycle in production**: entry → +1R arm → ⅓ partial
at 45.9667 → trail exit on the 91.9333 remainder → `net_pnl` reconstituted whole. The mechanism
applied at 15:31 is now proven end-to-end on a real position, and it was a **winner**. The
accounting reconciles: gross 102.046 − fees 7.273 + partial 31.749 = **126.523**, with
`total_fees` 10.917 = 7.273 + 3.645.

**Consequence for this change:** today is now a **+1.257R day**, so the new brake has nothing to
act on, and the book has **17** trading days rather than 16.

---

# §1 — THE RULE, AND WHAT DECIDED IT

`DAILY_LOSS_R_LIMIT = 3.0` is a named constant in `config.py` with the full reasoning beside it.
The comment records, in this order: that the **measurement returned a null**; that **structure**
decided it; and what each clause is for. It is written so the choice cannot later be re-read as
having been evidence-driven.

**The null, restated because it is the foundation and not a footnote:** the brake's 284 refusals
across 9 days drifted −0.128% at 4h, which looks like it working — but same-day non-halted signals
drifted −0.067%, and **the excess was indistinguishable from zero at 4h, 12h and 24h**. It bought
nothing and cost nothing this data can detect.

**What actually decided it:**

- **A day is one trade.** 14 of 16 days had exactly one close; the worst day in the entire book is
  **−1.15R**. Below ~1R a rule fires on the first ordinary stop-out; at ~1.5R and above it never
  fires. **There is no middle**, so the choice is about intent.
- **One −1R stop-out is the cost of doing business**, not evidence the system is broken. Halting
  on it bought nothing measurable and cost **sample** — the binding constraint on every other
  question being asked of this book.
- **"Systematically wrong today" already has its own instrument** — the loss-streak brake, 3
  consecutive losses → 4h cooldown. Separate tool, separate job, **deliberately untouched**.
- **3.0R = three full stop-outs in one day**, at ~0.33 entries/day — three times the normal rate,
  all losing. Genuinely anomalous.

## The two clauses

| clause | paper | live |
|---|---|---|
| `day_loss_R >= 3.0` | ✅ active | ✅ active |
| `day_loss >= 5% of equity` | ❌ **absent** | ✅ active |

The equity clause is skipped in paper via an explicit `if OBSERVATION_MODE: return False, None`
placed **after** the R clause. Absent in paper because the equity it references is not the equity
being risked — a **category** error, not a calibration one. Kept in live because ruin risk is
denominated in percent of balance, and dormancy at $100 is not a reason to discard it. A side
benefit: paper no longer makes a `fetch_balance` round-trip on loss days.

The two reasons are now distinguishable in the record: `daily_loss_R_breaker: …R` and
`daily_loss_equity_breaker (LIVE): …% of equity`.

---

# §2 — 🔴 THE RECORDING GAP IS CLOSED

The finding you cared about most. `risk_reason` went to Telegram and the HTTP response and was
written **nowhere**.

**Two changes, both small:**

```diff
         update_trade(row_id, status='risk_halt', combo_key=combo,
-                     confluence_score=adj_score)
+                     confluence_score=adj_score, error=risk_reason)
+        _record_skip_attribution(row_id, symbol, direction, 'risk_halt',
+                                 matrix_result=matrix_result,
+                                 confluence_score=adj_score,
+                                 ai_reason=risk_reason)
```

```diff
-TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked')
+TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked', 'risk_halt')
```

**Adding `risk_halt` to skip_attribution was a small change, as hoped** — the anchor, the five
drift slots and the sampler are all status-agnostic, so the scope tuple plus one call site was the
whole of it. **The risk gate is no longer the one gate that cannot say why it fired**, and its
refusals are now drift-tracked like every other gate. No future reconstruction needed.

One honest note: the risk gate fires *before* the order-book fetch, so no price is in hand at that
point and `on_skip` falls back to a `fetch_ticker` for its anchor. That is one extra read per risk
halt — best-effort, wrapped so it can never affect the trade path, and rare (289 halts in eight
weeks). I judged the attribution worth it; say the word if you would rather it stayed price-less.

---

# §3 — REPLAY: IT FIRES ON ZERO DAYS, AND THAT IS NOT SUCCESS

```
NEW RULE (day_loss_R >= 3.0R), replayed over the whole book:
  trading days with closes : 17
  days it would have FIRED : 0  (none)
  worst day in the book    : 2026-07-10   -1.15R
  margin to the threshold  : 1.85R of headroom
```

**Stating it plainly, as you asked: silence is not evidence the rule is right.** A brake that never
fires on the available history has not been validated by that history — it has simply not been
tested by it. What the replay establishes is narrower and worth being precise about:

- the rule is **inert on this book**, so adopting it changes nothing retroactively;
- it has **1.85R of headroom** to the worst day ever recorded, so it is not marginal — it would
  take a day roughly **2.6× worse than anything seen** to trip it;
- it becomes meaningful **only as trade frequency rises**, which is the intended property of a
  tail brake and the precise failure mode of the constant it replaces.

**Net effect versus the old rule: 996 entry opportunities across 11 days would not have been
refused.** Whether that is a gain is exactly what the 21:40 null could not determine — the refused
signals' drift was indistinguishable from their same-day peers. The honest claim is that this
**recovers sample at no measurable cost**, not that it makes money.

---

# §4 — CONFIRMATION SET

| check | result |
|---|---|
| **threshold is a named constant with its reasoning** | ✅ `DAILY_LOSS_R_LIMIT = 3.0` in `config.py`, ~25 lines of recorded reasoning beside it |
| **paper has no equity clause; live has both** | ✅ R clause first, then `if OBSERVATION_MODE: return False, None`, then the equity clause |
| **loss-streak brake byte-identical** | ✅ `diff` of the block → **IDENTICAL**; `LOSS_STREAK_THRESHOLD = 3`, cooldown 4h |
| **replay fires on ZERO days** | ✅ 0/17, worst day −1.15R, 1.85R headroom — **stated as untested, not as success** (§3) |
| **fresh `risk_halt` carries its reason** | ✅ write path persists `error=risk_reason`; none has occurred since the restart (today is +1.257R, so the brake has nothing to act on) — the mechanism is in place, not yet exercised |
| **`risk_halt` drift-tracked** | ✅ `TRACKED_STATUSES = ('ai_skipped', 'below_threshold', 'htf_blocked', 'risk_halt')` |
| **window not reset** | ✅ **4 of 200**, before and after |
| **vpos 25** | 🔶 **closed itself on the trail at 20:13:32** (+$126.52 / +1.257R), two minutes before the restart — **not disturbed by me** (§0) |
| **`OBSERVATION_MODE` True proven live in the new pid** | ✅ `[VIRTUAL] poller started in pid 1173092` |
| **entry prompt frozen** | ✅ `AI_ADVISOR_HIDE_1H = False`; `claude_advisor.py` 16:15:42 — untouched |
| **engine still single manager** | ✅ `[MONITOR] RETIRED` · `live adapter registered` |
| **name-resolution audit** | ✅ `_check_daily_loss_breaker` **CLEAN**, `_handle_5m_trigger` **CLEAN** |
| **`py_compile`** | ✅ all six modules |
| **tracebacks since restart** | ✅ **0** |
| **Tor → Bybit / OKX** | ✅ both live |
| **Titan untouched** | ✅ clean · `HEAD 3316e8a` · active · **no `.py` modified** |

Snapshots: `main.py.bak_candidateD_20260801`, `config.py.bak_candidateD_20260801`,
`skip_attribution.py.bak_candidateD_20260801` — all md5-verified pre-edit.

---

# §5 — WHAT TO WATCH

1. **The first `risk_halt` under the new rule** — check it carries a reason in `trades.error` and
   an anchor row in `skip_attribution`. Until one occurs, the recording fix is applied but
   **unexercised**, and I am reporting it that way.
2. **The brake's drift, once tracked.** After enough halts accumulate, the question the 21:40
   report had to reconstruct becomes directly readable — and if the null holds with real
   attribution behind it, that is a stronger result than the reconstruction could give.
3. **Frequency.** 3.0R only becomes reachable if entries per day rise. If the rate stays near
   0.33/day the brake stays dormant by design — which is intended, but worth re-checking rather
   than assuming, because "dormant by design" and "dormant because something else is blocking"
   look identical from the outside.

**Nothing else changed. SOL is still PAPER and still cannot place an order.**
