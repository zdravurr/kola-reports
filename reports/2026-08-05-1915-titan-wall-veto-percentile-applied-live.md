# TITAN — APPLIED LIVE: THE PERCENTILE IS NOW PRINTED FOR THE WALL BEING JUDGED. (c) DROPPED.

**2026-08-05 19:15 UTC · 🔴 APPLIED FROM FLAT · HEAD `b9081ad` → `1ec2477` · restarted 19:08:39 UTC**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
**0 open positions and 0 `exit_pending` at the moment of application**, re-checked immediately before
the file copy and again before the restart. **Mercury-SOL never opened.**

Parent: `2026-08-05-1855-titan-make-the-wall-veto-do-what-it-says.md` (the approved diff).
Grandparent: `2026-08-05-1835-titan-did-the-wall-hold-or-was-it-eaten.md`.

---

## WHAT SHIPPED, AND WHAT DID NOT

| hunk | status |
|---|---|
| **(a)** per-wall percentile, rendered **first**, multiple second | ✅ **APPLIED** |
| **(b)** HARD RULE states the ~50th / 90th line; absorption premise removed | ✅ **APPLIED** |
| **(c)** measured base rate of walls being traded through | 🔴 **DROPPED — and the reason is now recorded in the source** |
| the `91th` → `91st` ordinal | ✅ **APPLIED, entry path only** |
| everything else | untouched |

**Commit `1ec2477`.** `titan-bot/main.py` +71, `titan-bot/claude_advisor.py` +150/−23. Working tree
clean. Snapshots of both files taken before any edit and md5-verified:
`/root/backups/wall-veto-20260805/`.

---

## 🔴 (c) IS NOT MERELY ABSENT — THE REASONING IS IN THE FILE

A removed hunk leaves no trace, and the next session would have re-derived it as an obvious
improvement. The rejection is therefore written where the code is, in place of the text:

```python
    # ── CONSIDERED AND DELIBERATELY NOT ADDED 2026-08-05: the measured base
    # rate of walls being traded through (54/75/88/95% at 1/4/12/24h).
    # It was drafted, reviewed and dropped by the operator, and the reason is
    # worth keeping so it is not re-proposed as an improvement. The 18:35 study
    # established that "wall eaten" and "the refusal was wrong" are ALGEBRAICALLY
    # ENTANGLED — the opposing wall sits in the direction the signal points, so
    # eating it and the signal being right are two descriptions of one event.
    # Telling the model "walls like these are traded through 95% of the time" is
    # therefore close to telling it "your wall veto is wrong 95% of the time":
    # outcome information wearing a price level's clothes, and over the line
    # f0a8d30 drew — the model may learn whether a wall is ordinary or extreme,
    # never what that implies about the RESULT.
    # The false premise it was meant to answer is already gone: the HARD RULE
    # above no longer asserts that resting liquidity "absorbs the move before it
    # can develop". Removing the claim was the substantive fix; quantifying its
    # failure would have been a second, different, and prohibited change.
```

**Verified in the built prompt string:** `MEASURED BASE RATE` absent · no `95%` anywhere in
`_ENTRY_SYSTEM` · `absorb the move` absent · `MUST reply` (the old unconditional veto) absent ·
`at or below the ~50th percentile` present · `90th percentile` present.

---

## 🔴 THE CONFIRMATION THAT MATTERS — A REAL LIVE BOOK THROUGH THE REAL CODE PATH

Not a scratch render with hand-made dicts: `liquidity_zones.fetch_pre_trade_walls()` →
`main._entry_book_pct()` → `claude_advisor._format_pre_trade_walls()`, the exact chain an entry
consultation uses, on the live OKX book at 19:07 UTC:

```
Order book (pre-trade, 8000 levels):
  Mid: $64,867.95  |  Imbalance ±1%: 0.34 (ask-heavy)  — 0th pct
  Bid walls (>4x avg bucket vol): $64,657.50 — 60th pct (×5.1), $64,357.50 — 30th pct (×4.4)
  Ask walls (>4x avg bucket vol): $64,867.50 — 75th pct (×6.2), $64,882.50 — 97th pct (×14.1), $65,002.50 — 27th pct (×4.4)
  Book depth: 3,939 BTC — 100th pct, sampled 16s ago
Order-book PERCENTILE scale (baseline: 33521 snapshots of this same OKX depth-4000 book)
  Each wall's percentile ranks its multiple against the history of
  walls standing in the path on that side of this same book — so the
  walls on a line share one scale, and the nearest wall, the one a
  HARD RULE veto is normally about, is the most exactly ranked.
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile printed with each wall:
  ~50th percentile is ORDINARY and not significant; 90th+ is genuinely thick.
```

**Five walls, five percentiles.** Under the previous renderer this book state would have printed
**one** percentile per side — for `×14.1` — and the `×6.2` and both `×4.4` walls would have carried
no percentile at all.

🔴 **AND IT SEPARATES, WHICH IS THE WHOLE POINT.** On one line: `×14.1 = 97th` — genuinely thick, the
region the rule is actually about — sitting beside `×4.4 = 27th`, which is ordinary. **The old
rendering gave the model one number for the biggest wall and left it to infer the rest from
×-figures the prompt itself calls meaningless.**

Note also `×5.1 = 60th pct`. Under the old max-wall baseline that same wall would have read **≈31st**.
**The corrected baseline is visible in live output, and it does not uniformly soften walls — it moves
ordinary walls up and leaves genuinely thick ones thick.**

⚠️ **STILL OUTSTANDING, AND STATED RATHER THAN GLOSSED:** the brief asked for confirmation on a
**stored** prompt from a real signal. The last consultation before the restart was **16:40 UTC** —
these fire a few times an hour at best — and **no consultation has occurred since the 19:08:39
restart at the time of writing.** A watcher is running. **The code path and the live data are
confirmed; the stored-row confirmation is pending the next signal and will be reported when it
lands.** I am not calling that step done.

---

## THE ORDINAL — FIXED, AND EXACTLY HOW MUCH IT TOOK

The brief's condition was "fix it if it is a one-line change; if not, leave it and say so."
**It is one expression, but it needs a name, so it is a 4-line helper plus three call sites** — I am
stating that precisely rather than claiming it met the letter of "one line":

```python
def _ordinal(v):
    n = int(round(v))
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"
```

Verified across the range that matters:
`0th 1st 2nd 3rd 4th 11th 12th 13th 21st 22nd 23rd 31st 48th 53rd 82nd 90th 91st 100th`.

🔴 **ENTRY PATH ONLY.** The exit block has four `…th pct` renderers of its own
(`claude_advisor.py:746-753`). They are **out of this change's scope and were left alone** — the brief
put the entire exit side off limits, and the frequency argument that justified this fix does not
apply to them.

---

## 🔴 A DEFECT I INTRODUCED AND CAUGHT BEFORE APPLYING

The new scale note said *"Each wall's percentile ranks its multiple against…"* — **unconditionally.**
In the degraded path there are no per-wall percentiles, so that sentence would have described a scale
that was not on the page. **That is precisely the lying-label class this book has spent the week
deleting, and I would have shipped it.**

It surfaced only because a byte-identity check failed for the wrong reason: my filter matched the new
note (it contains the word "walls"), which made the fallback look changed when the wall lines were
fine. Chasing the false alarm exposed the real one.

Fixed: the sentence is now conditional on per-wall percentiles actually being present, answered from
the rendered result rather than from intent.

```python
    _has_per_wall = any(
        isinstance(p, (int, float))
        for key in ('bid_wall_pcts', 'ask_wall_pcts')
        for p in (bp.get(key) or []))
```

**Degraded rendering, as it now stands** — no per-wall claim, and the original NOTE wording restored:

```
Order-book PERCENTILE scale (baseline: 33228 snapshots of this same OKX depth-4000 book)
  NOTE: EVERY book state contains a wall above 4x, so 'large multiple' means
  nothing on its own. Judge by the percentile:
  ~50th percentile is ORDINARY and not significant; 90th+ is genuinely thick.
```

---

## VERIFICATION LEDGER

| check | result |
|---|---|
| `ast.parse` + `py_compile`, both files, after copy to `titan-bot` | ✅ |
| flat before application (`virtual_positions` open / `exit_pending`) | **0 / 0**, re-checked twice |
| restart deliberate, service healthy | `active`, `ActiveEnterTimestamp 19:08:39 UTC` |
| boot reconciliation | ✅ *"exchange and DB agree: 0 exchange position(s), 0 open row(s)"* |
| order mode after restart | 🔴 `LIVE ORDERS — REAL MONEY`, `$30 × 5 = $150` — unchanged |
| per-wall percentile on a **real live book, real code path** | ✅ 5 walls, 5 percentiles |
| per-wall percentile on a **stored real prompt** | ⏳ **pending next signal — NOT claimed** |
| fallback wall lines vs unpatched module | ✅ **identical modulo the intended ordinal fix** (`82th`→`82nd`) |
| no `book_pct` at all → output vs unpatched | ✅ **byte-identical** |
| HARD RULE reads as (b), no absorption claim | ✅ |
| (c) absent from the built prompt string | ✅ |
| `config.py` | **unchanged** |
| files modified | **exactly two** |
| grep of the `main.py` diff for gate/score/risk/geometry identifiers | **no match** |

**Untouched, confirmed by diff:** EMA envelope gate · HTF cascade · FLAT floor · Variant-B · score
bars · risk gates · geometry (SL 2.25 / trail 0.75R) · **the entire exit side** · every schema.

---

## THE PRE-REGISTRATION, RESTATED AS APPLIED — UNCHANGED FROM 18:55

| | |
|---|---|
| **PRIMARY** | sub-50th share **53.8 % → below 40 %** over **~100 consultations**, on the nearest-wall baseline. **40–50 % is ambiguous, not a win. No movement is a NULL and is recorded as a NULL.** |
| **SECONDARY** | refusal **96.3 % → 92–95 %**; entries **0.79/day → 0.9–1.2/day** |
| 🔴 **TRIPWIRE** | **beyond ~1.5 entries/day means the change did more than re-weight one figure — revert and look** |
| why the secondary is small | only **6.4 %** of these refusals cite the wall and nothing else; **91.2 %** also cite regime/trend/ADX |
| **DRIFT** | newly-admitted signals tracked by `skip_attribution` as usual. Favourable → right; adverse → revert |
| ⚠️ **and the caveat that governs the drift check** | the unit of independence is the **DAY**. ~12.6 wall-refusals/day is ~1 day of information. **A drift verdict needs weeks. Do not read week one as evidence either way** — the sub-50th share is readable long before it |

**Baseline as of application:** 277 deduped wall-citing refusals over 22 days = 12.6/day · 53.8 %
below the 50th, median 48.4th, 12.1 % ≥ 90th · advisor refusal 96.3 % (492 skip / 19 execute) ·
0.79 entries/day.

*(The superseded 18:35 figures — 70.2 %, median 29th — remain withdrawn. The correction and its cause
are recorded in `main._rank_walls`'s docstring so the wrong baseline is not re-derived.)*

---

## LIVE STATE AFTER APPLICATION

| | |
|---|---|
| HEAD | **`1ec2477`** (was `b9081ad`) · working tree **clean** |
| open positions | **0** |
| service | `titan.service` **active**, restarted **19:08:39 UTC** |
| order mode | 🔴 **LIVE REAL MONEY** — unchanged by this commit |
| rollback | `/root/backups/wall-veto-20260805/{main,claude_advisor}.py`, md5-verified, or `git revert 1ec2477` |
