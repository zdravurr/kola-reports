# TITAN — OPEN ITEMS

**Read this before touching Titan.** Written to be actionable by a session with **no memory** of
2026-07-26/27. Every entry states what is known, what is **not** known, and what would close it.

Titan is a **BTC swing paper-trading bot**. `LIVE_TRADING_ENABLED = False`. All P&L below is paper
P&L from the `virtual_positions` table.

_Last updated: **2026-07-27 01:00 UTC** — full rewrite at session close. HEAD `f0a8d30`._

---

## 0. HOW TO READ THE DATA WITHOUT FOOLING YOURSELF

Four filters. Most of the wrong conclusions killed in §4 came from skipping one of them.
**Apply all four before quoting any statistic about entries or exits.**

| Filter | Why | Predicate |
|---|---|---|
| Forming-candle fix | `srv_vol_ratio_5m` before this read the **forming** candle and is not comparable | `t.timestamp >= '2026-07-04 11:58'` (commit `55d9c7f`) |
| Wall-trail window | Outcome decided by a **moved stop**, not by the entry | `NOT (opened_at < '2026-07-13T01:55' AND closed_at > '2026-07-02T23:28')` |
| Recheck TIGHTEN | Same — stop was moved after entry | `COALESCE(recheck_status,'') <> 'tightened'` |
| Excursion truth | `max_adverse_price` **stops updating at the close**, so it understates what price did | use real OHLCV candles, not stored extrema |

⚠️ The wall-trail filter must test **lifetime overlap**, not entry time. Using entry time alone
silently drops vpos 62. This exact bug produced a wrong answer once already.

**Sign convention:** skip-drift `_compute_drift_pct` is **positive = the skipped signal would have
won**. Reading it backwards inverts every veto conclusion. This caused a real inverted finding.

---

## 1. 🔴 LIVE-PATH PARITY GAP — BLOCKING before `LIVE_TRADING_ENABLED = True`

**Three mechanisms exist in the paper path only:**

| Mechanism | Commit | Lives in |
|---|---|---|
| LONG partial realisation (1/3 at +1R) | `f7df202` | `virtual_trader.py` |
| Recheck TIGHTEN original-SL floor | `93c20c3` | `virtual_trader.py` |
| `breakeven_jobs` | (pre-existing) | `virtual_trader.py` |

Enabling live trading today would run a **materially different strategy** from the one being
measured — no partial, no stop floor, no breakeven jobs.

**OPERATOR'S DECISION (2026-07-26), do not deviate:** rewrite the engine as **ONE code path with
two adapters** — orders either go to the exchange or are simulated — **NOT** piecemeal porting of
each mechanism into a second live path. Piecemeal porting is how the divergence happened.
**Do this well before live is enabled**, not as part of enabling it.

---

## 2. STILL OPEN — carry forward

### 2.1 LONG partial parameters are placeholders
`LONG_PARTIAL_LEVEL_R = 1.0`, `LONG_PARTIAL_FRACTION = 1/3` were chosen as **round numbers that
survived simulation**, not as optima. Retune at **~30 clean longs reaching above 0.5R**.
**Current: 7 clean** (was 6; vpos 82 added tonight).

**First live firing — 2026-07-27 00:07, vpos 82:** partial took **+18.91 USDT** at 1R, remainder
rode the unchanged contract to a trail exit, **total +53.79**. One datapoint. It proves the
mechanism executes and folds into `net_pnl`; it proves **nothing** about the parameters.

### 2.2 Variant C (narrower LONG trail) — UNEVALUATED, not rejected
Was not tested because the excursion data needed to judge it (full price path between entry and
exit, per position) was not assembled. **It is not a rejected idea — it is an unasked question.**
Closing it needs excursion-path coverage on real candles, the same method §4.10 settled on.

### 2.3 🔴 Entry advisor gets an uninformative wall label — LIVE ASYMMETRY
The entry advisor receives the **hard-coded word "Massive"** for every wall above `4.0x`, with
**no percentile scale**. **100% of observed book states contain such a wall**, so the label carries
**zero information** — it is a constant being read as an alarm.

The **exit** advisor was given the percentile scale in `ef7fa10` (`_exit_pct()` against the
`orderbook_density` baseline). The **entry** advisor was not. **The two advisors now describe the
same order book in two different languages** — this asymmetry is the gap, and it is live.

Closing it: feed the entry advisor the same `orderbook_density` percentile the exit side uses.
The baseline table is already populated by the always-on collector (§3).

### 2.4 Exit-advisor activation criterion — RECORDED BEFORE ANY DATA EXISTED
Written down **deliberately in advance** so the bar cannot be moved after seeing results.

> It goes live only if, over the first **~10 closed positions**, its **FIRST** `"close"` verdict
> beats the actual exit **both in total USDT and in positions improved**.
> **No partial credit. No re-cutting the sample. First verdict only** — not its best verdict.

**Progress: 1 of ~10 closed** (vpos 82, closed 2026-07-27 00:07). 3 consults recorded so far
(rows 18773, 18789, 18796) — all `hold`, so no verdict has yet been tested against an exit.
Currently `EXIT_ADVISOR_DRYRUN = True`: it can never close a position.

### 2.5 Volume ceiling — NOT BUILT, and has an EXPIRY
Clean n is **4 SHORT / 4 LONG**. SHORT **p = 0.333**; LONG **contradicts** the thesis (p = 1.000).

The earlier, exciting **p = 0.048 came from three contaminated rows** (vpos 66, 68, 74). The
sensor that reported it has since been fixed to count clean rows only.

Re-cut at **~10 clean corrected SHORT closes**. **EXPIRES 2026-09-30** if n is not reached —
**delete it then.** Rationale: the counter-short caution shipped on a statistic that quietly
stopped being true and nobody re-checked for months (§4.5). An expiry date is how that is
prevented, so **do not extend it silently**.

### 2.6 🔴 EQH/EQL SMART TP — READS AS ARMED, IS UNREACHABLE. DO NOT "FIX" IT.
`EQH_EQL_SMART_TP_ENABLED = True` in config **READS AS ARMED AND IS NOT.** The flag is only ever
read inside `_handle_liquidity_sweep()` (`main.py:2746`), and that function is **never entered**.

**Mechanism (verified, not inferred):** the dispatch gate at `main.py:2977` requires
`action_field == 'context_update' AND raw_signal_type in ('EQH','EQL')`, where `raw_signal_type`
comes from the **payload's own** `signal_type` field. The live alerts never carry that value, so
the condition is False on every fire and sweeps fall through to the generic context path.
**PROOF:** all **304** EQH/EQL rows land with `signal_type='5m_liquidity_ctx'`, and
`signal_type_ctx` — a column written **only** at `main.py:2766`, inside the handler — is NULL on
**304 of 304**. The handler has not run once since the alerts went live in May.

Restoring reachability is a **one-line change** (`classify()` already maps `Equal Highs →
LIQUIDITY/SHORT/eqh/0.9`), which is exactly why it is dangerous: anyone "repairing" dead-looking
dispatch code would **silently arm a rule that loses −971 on the clean sample** and destroys the
short side by closing winning shorts early on an EQL (vpos 58 −435, vpos 50 −403).

**STANDING DECISION: leave BOTH the flag and the routing EXACTLY as they are.** Do not set the
flag to `False` either — it changes no behaviour and would make a future reader think the rule was
evaluated and merely switched off, destroying the knowledge this entry exists to preserve.
The unreachable branch has been protecting the book **by luck, not design**.
Evidence: `reports/2026-07-27-0038-eqh-eql-sweeps-tested-and-killed.md`

### 2.7 Anthropic API key — exposed 20 days, rotation DECLINED
Leaked in plaintext to a world-readable sensor log for ~20 days. **Operator declined rotation** —
the server is single-user with no other access.
**Done:** root cause fixed on both bots (`set -a; . <env>` replaced with a scoped `_env_get()`
parser), logs purged, all sensor logs `chmod 600`, nginx `noquery` log format stops the webhook
passphrase reaching the access log.
**Revisit only if a second user or external access ever exists.** Not an open task today.

---

## 3. WATCH-LIST — CURRENT REALITY

**Retired** (deleted `d12e276` — they answered their question or their question died):
`prior-move logger` · `TOLN (tolerate-NEUTRAL)` · `counter-short review`

**Redefined** — the old predicates could never fill again:
| Sensor | New predicate | N |
|---|---|---|
| chop-short | `ema_gap_dir_1h='Flat' AND market_regime='TREND'` (old half included `regime='FLAT'`, which the FLAT score floor drove to zero) | **0 of 5** |
| regime-FLAT high-ADX | window widened `-3d → -21d` | **5 of 12** |

**Reclassified as DATA SOURCES — these are not watchers, they FEED the exit advisor. Keep them
running; switching them off silently degrades every exit consultation:**
`orderbook-density collector` (60s, builds the percentile baseline `_exit_pct()` reads) ·
`smart-exit dryrun sampler` (live regime + volume in the exit context)

**Genuinely accumulating toward a decision:**
`volfloor` **4 SHORT / 4 LONG clean** (threshold 6; expiry §2.5) ·
`exit advisor` **1 of ~10 closed positions** (§2.4)

---

## 4. HYPOTHESES TESTED AND KILLED — DO NOT RE-OPEN WITHOUT NEW EVIDENCE

Ten. Each cost real analysis time. **A hypothesis is re-openable only with data that did not
exist on 2026-07-27** — not with a fresh intuition.

1. **Prior-4h chase** — the idea that entries chase an already-extended 4h move. No relationship
   survived contamination filtering.
2. **Signal → entry slippage** — the delay between alert and fill was proposed as a P&L drain.
   Measured; it is not material.
3. **Entry-timing bucket (R2, prior-move)** — first reported at p=0.011/0.027, both **under-filtered**.
   Correctly filtered: **p = 0.1544**, and the mid bucket collapses from n=8 to **n=1**. An artefact.
4. **Wall-side misread — DEAD, twice, on two bots by two methods.** The claim was that the advisor
   confuses a wall above with a wall below and vetoes good trades. Reality: **289 skips citing an
   ask wall above drifted −0.270%/4h (t = −4.6)** vs −0.051% control, load-bearing subset
   **−1.509%/24h**. Positive drift = the skip would have won, so **these were the BEST vetoes in
   the book**. Mercury-SOL reached the same conclusion on 2026-06-30 by replaying 471 historical
   skips: only 6 flipped (1.3%) and **all six were losers**. 🔴 **Do not re-open.**
5. **ADX + score chop gate** — the proposed separator fully overlaps winners and losers; the
   highest-ADX trade (#47) is a **−$127 loser**. Only the 1h EMA-gap 'Flat' tell survived, and it
   is still only being watched (§3), never shipped.
6. **Stop-too-tight** — rejected on geometry: stops are a uniform **2.5×ATR**, so "too tight" is
   not a property the data can express. The stop being the expensive exit is a **horizon**
   artefact, not a distance one.
7. **Volume ceiling** — 2 vs 2, p = 0.333. Tested **twice**, failed twice. See §2.5 for the expiry.
8. **EQH/EQL liquidity sweeps** — no directional edge (EQH and EQL drift the **same** way; the
   thesis needs opposite signs). Smart-TP simulated at **−971** on the clean sample. Not a
   volatility proxy either: at sweep moments ADX 25.91 vs 25.08 baseline, ATR 351.4 vs 351.7. §2.6.
9. **"11 of 11 would have survived their original stop"** — **WRONG, an artefact.**
   `max_adverse_price` **stops updating at the close**, so it never sees the excursion that
   followed. On real candles, **8 of 17 hit the original stop.** Never quote stored extrema for a
   survival question.
10. **The 5-position counterfactual** — the follow-up figure (−335.84, "the fix would have lost
    money") was **also wrong**: **survivorship bias in the resolution criterion**, because only
    fast-resolving positions could resolve on internal data. Settled properly on **13,536 real
    OHLCV candles**. 🔴 **Regardless of the outcome, do not propose restoring wall-trail or
    recheck TIGHTEN** — operator's standing instruction.

**The pattern in 3, 9 and 10:** every one was a *stored-column shortcut* standing in for a real
price path, and every one produced a confident wrong number. When the question is "what would
price have done", **fetch candles**.

---

## 5. RESOLVED 2026-07-26/27 — closed, recorded so they are not re-investigated

- **Exit advisor existence.** It was **wired but NEVER invoked**: the 5m Group-B trigger has never
  arrived, and the paper-mode position lookup returned empty. It was not broken — it was
  unreachable, which reads identically from the outside. Now **live in DRYRUN** on three triggers:
  **hourly + on 15m confirm + on armed exit** (`ef7fa10`). 3 consults recorded.
- **Entry-advisor 1H identity gap** — closed (`f0a8d30`). The advisor now sees which named signal
  set the 1H trend, its weight and its age. **`AI_ADVISOR_HIDE_1H` stays `True`**, and the identity
  is supplied as a **FACT ONLY — no statistic, win rate or historical performance attached**,
  deliberately. Renders as: `1H trend set by: Trend Catcher Up, weight 1.0, set 2.2h ago`.
- **Wall-side misread** — see §4.4. Moved out of open items entirely.

---

## 6. SHIPPED TODAY — seven commits, `6c35b9d..f0a8d30`

| Commit | What it fixed |
|---|---|
| `93c20c3` | **Recheck TIGHTEN bound** — new SL can never be tighter than the **ORIGINAL** stop. (Variant B only; Variant A explicitly rejected.) |
| `596fbdf` | Gated the counter-short caution on `trend_1d != 'bull'` — **superseded hours later by `b878535`**, kept in history to show the stopgap preceded the retirement |
| `b878535` | **RETIRED the counter-trend EMA-1h soft caution** — its founding statistic does not reproduce and the cohort's sign is **inverted**. 17 lines removed, replaced by a 28-line historical note |
| `f7df202` | **LONG partial realisation** — 1/3 at +1R, remainder rides the unchanged contract; columns `partial_taken`, `realized_partial_usdt`, folded into `net_pnl` |
| `ef7fa10` | Persist the 15m entry confirmation + **wire the exit advisor in DRYRUN** (hourly / 15m confirm / armed exit) |
| `d12e276` | Retire 3 sensors, redefine 2 |
| `f0a8d30` | Give the entry advisor the **1H signal identity** (fact, not judgement) |

Six distinct changes; `596fbdf` and `b878535` are two commits on one decision that reversed itself
within the session — recorded that way on purpose.

---

## 7. VERIFIED STATE AT CLOSE — 2026-07-27 01:00 UTC

`git status` **clean** · origin **in sync** · HEAD **`f0a8d30`** · `titan.service` **active**
(restarted 00:13:32) · `nginx -t` **successful**, `noquery` format live · **Mercury-SOL untouched
and active**

**Flags live:** `LONG_PARTIAL_ENABLED=True` (1.0R, 1/3) · `EXIT_ADVISOR_PAPER_ENABLED=True`
`DRYRUN=True` `ON_15M_CONFIRM=True` `HOURLY=True` (3600s) · `CONFLUENCE_FLAT_THRESHOLD=5.0` ·
`WALL_TRAIL_LIVE_ENABLED=False` · `AI_ADVISOR_HIDE_1H=True` · `ADX_BELOW_FLOOR=20.0` ·
🔴 `LIVE_TRADING_ENABLED=False` · ⚠️ `EQH_EQL_SMART_TP_ENABLED=True` **(unreachable — see §2.6)**

**Titan crons — 4 daily + 1 weekly:**
`17 8` bull-regime · `29 8` chop-short · `35 8` volfloor · `53 8` regime-FLAT high-ADX ·
`11 8 * * 1` daily-trend-cohort (weekly)

**Book:** 0 open positions. Last close vpos 82 LONG **+53.79** (trail, partial +18.91).

---

## 8. REPORTING CONVENTION — for any session writing this up

Full reports go to the **`kola-reports` repo**, `reports/YYYY-MM-DD-HHMM-<name>.md`. The operator
reads them via **`raw.githubusercontent.com`** links. **Gist raw URLs are blocked** (robots-
disallowed) — a gist link delivers an empty file and the report effectively did not exist.
**Patches go INLINE in the same `.md`** as a fenced block, never as a separate `.patch` file:
**one link, one complete document.** Secret/PII scan is **fail-closed before every push** — the
repo is public. Telegram gets a short decision summary **plus the single raw link**, not the report.
