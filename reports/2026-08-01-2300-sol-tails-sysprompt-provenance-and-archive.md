# sol-tails-sysprompt-provenance-and-archive

_2026-08-01 23:00 UTC_

---

# MERCURY-SOL — TAILS CLOSED. **BACKFILL NOT RUN, AWAITING YOUR WORD.**

Items **1a/1b** (system-prompt provenance + V2 raw), **2** (withheld-field record) and **3**
(vendored Titan copy archived) applied. Restarted **21:02:38** (worker pid 1184217), **zero
tracebacks**. **Item 1c — the backfill — is planned below and NOT executed.**

SOL stays **PAPER**. The frozen surface is **provably** untouched, the window is **still 4 of
200**, no open position, Titan untouched.

---

# 🔴 FIRST: A CORRECTION TO THE 16:07 AUDIT — IT IS 32 AND 8, NOT 31 AND 7

Row **14988** is a **new** flip: vpos 25's entry today at 17:20. Recounted from the data rather
than carried forward:

| | 16:07 audit | measured now |
|---|---|---|
| flipped rows (`stored raw decide ≠ ai_decision`) | 31 | **32** |
| became positions | 7 | **8** |
| their net PnL | −$742.67 | **−$616.15** |
| share of the book's **net** loss | 74% | **69.7%** (of −$883.72) |
| stored base contains `_WALL_RULE_V1` | 31/31 | **32/32** — all reconstructible |

The whole difference is vpos 25 (**+$126.52**, a winner), which is why the share *fell*.

**One framing trap, flagged so the two numbers are never mixed:** the 74% figure used **net** book
loss. On a **gross** basis those positions' losing legs total −$866.20 against the book's
−$2,291.16 of gross losses = **37.8%**. Both are true; they answer different questions. Today's
net-basis figure is **69.7%**.

The 8 positions:

| vpos | entry row | side | close | net | R |
|---|---|---|---|---|---|
| 16 | 8446 | LONG | sl | −194.70 | −1.146 |
| 17 | 9358 | SHORT | sl | +0.86 | +0.004 |
| 18 | 9842 | LONG | sl | −234.04 | −1.074 |
| 19 | 10178 | SHORT | exit_signal | +89.00 | +0.463 |
| 21 | 11181 | LONG | trail | +33.66 | +0.285 |
| 22 | 11679 | LONG | sl | −203.42 | −1.064 |
| 24 | 13973 | SHORT | sl | −234.03 | −1.050 |
| **25** | **14988** | SHORT | trail | **+126.52** | **+1.257** |

---

# §1a/1b — THE FIX, AND THE PROOF IT DOES NOT TOUCH THE FROZEN SURFACE

## The change

`_verdict_system` is initialised to `_ENTRY_SYSTEM` before the aligned blocks and reassigned when a
**LIVE** flip is adopted; the closing stamp uses it. The two LIVE flip branches also now store the
V2 `raw`.

**Full non-comment diff — 5 additions, 1 replacement, all storage:**

```
+    _verdict_system = _ENTRY_SYSTEM
+                    _verdict_system      = _ENTRY_SYSTEM_V2_ALIGNED
+                    result['raw']        = v2a.get('raw')
+                    _verdict_system      = _ENTRY_SYSTEM_V2_ALIGNED_SHORT   # (a)
+                    result['raw']        = v2s.get('raw')                   # (b)
-    result['system_prompt'] = _ENTRY_SYSTEM
+    result['system_prompt'] = _verdict_system
```

The DRYRUN/shadow branches are deliberately **not** touched: they never change the verdict, so
`_ENTRY_SYSTEM` remains correct for them.

## 🔴 The proof it is storage-only

You asked me to confirm this before applying, and I checked it three independent ways rather than
reasoning about it:

| check | result |
|---|---|
| every `_call(system, user)` **code** line, old vs new | **byte-identical** — the model is handed exactly what it was handed before |
| the user-prompt builder | **untouched** — no line between `def consult_for_entry` and the aligned blocks changed |
| `_ENTRY_SYSTEM*` constants | **unchanged** |

`result['system_prompt']` is what the **caller persists**. It is never sent anywhere. The frozen
surface is *what the advisor reads*; this is *what the database records about what it read*.
**Different thing, and now correct.**

**1b was small** — `_call` already attaches `raw`, so it is one line per branch. Done, not deferred.

---

# §1c — 🔴 BACKFILL PLAN. **NOT EXECUTED.**

## Which rows

**32 rows**, identified by the signature the audit established — the stored raw response parses to
a different `decide` than the stored `ai_decision`, which can only happen when a flip overwrote the
verdict:

```
8446, 8447, 9358, 9360, 9361, 9367, 9374, 9375, 9376, 9377, 9842, 9875, 9876,
9878, 9880, 9881, 9882, 10003, 10178, 10180, 10181, 10183, 10258, 10259, 11180,
11181, 11679, 11680, 11698, 11700, 13973, 14988
```

## What changes

**One column, `ai_system_prompt`, on those 32 rows.** Nothing else — no decide, no confidence, no
reason, no raw, no pnl.

New value is **deterministically reconstructed per row from that row's own stored base**:

```python
soft = stored_base.replace(_WALL_RULE_V1, _WALL_RULE_V2_ALIGNED)          # LONG flips
soft = stored_base.replace(_WALL_RULE_V1, _WALL_RULE_V2_ALIGNED_SHORT)    # SHORT flips
```

Using **each row's own** stored base is what makes this era-correct: the base prompt was edited
four times over the book's life, and every row already carries the base of its era.

**Verified precondition: the stored base contains the `_WALL_RULE_V1` block in 32 of 32 rows.** If
it did not, the replace would be a silent no-op — so that is a guard, not an assumption.

## How it is guarded

1. `trades.db.bak_pre_sysprompt_backfill_20260801` taken immediately before.
2. Predicate requires **all** of: id in the 32; `ai_system_prompt IS NOT NULL`; the base **contains
   `_WALL_RULE_V1`**; and the reconstructed text **differs** from the stored one. A row failing any
   check is skipped and named.
3. Single `BEGIN IMMEDIATE` transaction; abort unless `changes() == 32`.
4. `PRAGMA quick_check` after.
5. Per-row assertion that the result contains the V2 wall block and no longer contains V1.

## How it is reversible

The transform is a **pure string replace with a known needle and replacement**, so it inverts
exactly: `soft.replace(_WALL_RULE_V2_ALIGNED, _WALL_RULE_V1)` restores the stored base byte-for-byte.
Plus the DB backup. **Reversible two independent ways.**

## What it does NOT fix

The backfill corrects **which prompt** each decision was made under. It cannot recover **what the
model said** — see §1d.

**Say the word and I run it. It is not run.**

---

# §1d — 🔴 THE PERMANENT LIMITATION

**The V2 raw JSON was never stored for the historical 32 and cannot be reconstructed.**

- The SOFT **prompt** is deterministic — we can know exactly what was asked. ✅ recoverable
- The model's **response to it** was overwritten by the V1 raw and is **gone**. ❌ unrecoverable

**Consequence, stated so it is not softened later:** those 32 decisions — and the **8 positions**
they became, carrying **−$616.15** — can be **REPLAYED** but never **AUDITED**. We can re-ask the
question; we cannot check what the model actually answered, only what the code recorded of it. If
a future analysis asks *"was the V2 verdict reasonable on its own terms?"* for any of those 8
positions, **the answer is unavailable and will stay unavailable.**

Fixed going forward from **21:02:38** — every flip from now on stores its own raw.

---

# §2 — THE WITHHELD FIELDS: RECORDED, NOT ADDED

**Nothing was added.** Verified **empirically** against the newest rendered prompt (occurrence
counts in the stored text), not taken from the audit — and each value confirmed present on the
same `trades` row at the same instant.

| # | field | column | withheld by | value on the same row |
|---|---|---|---|---|
| 1 | funding rate | `mc_funding_rate` | never rendered | 1.444e-05 |
| 2 | OI delta % | `mc_oi_delta_pct` | never rendered | −1.5352 |
| 3 | DXY trend | `dxy_trend` | never rendered | DOWNTREND |
| 4 | macro news category | `macro_news_category` | never rendered | **CRITICAL_NEGATIVE** |
| 5 | macro gate penalty | `macro_gate_penalty` | never rendered | 1.0 |
| 6 | **news sentiment** | `news_score` / `news_summary` | 🔴 **GATE** — `_claude_news = None` while `is_in_funding_news_observation()` is True; **pinned at 0/30 while paper** | −0.25 |
| 7 | confluence score | `confluence_score` | never rendered | 1.75 |
| 8 | HyperWave subtype | `hw_15m_subtype` | never rendered | REVERSAL_LONG |
| 9 | HyperWave weight | `hw_15m_weight` | never rendered (`Combo weight:` is a **different** quantity) | 1.0 |
| 10 | tape buy ratio | `tape_buy_ratio` | never rendered | NULL here |
| 11 | tape aggression | `tape_aggression` | never rendered | NULL here |

**10 of 11 are simply never rendered — no gate, no flag, no condition. Only news is gated.** That
distinction matters: ten are a *prompt-content* decision, one is a *sequencing* decision already
settled (Option A).

✅ **Two of the audit's thirteen closed today:** the **1H tier** and the **trade direction as a
field** — both confirmed present in the newest prompt.

⚠️ Worth your eye: **a CRITICAL_NEGATIVE macro category with a 1.0 gate penalty was recorded on the
same row the advisor judged, and the advisor never saw it.**

**When the window closes, decide from this list rather than re-auditing.**

---

# §3 — THE VENDORED TITAN COPY, ARCHIVED

Re-verified by grep across `.py`/`.cfg`/`.conf`/`.json`: **zero references** anywhere in the tree.

**Moved, not deleted, to:**

```
/mnt/volume_nyc1_1780480650620/_archive-not-in-use/titan_brain-vendored-copy-ARCHIVED-20260801/
```

— outside the bot tree entirely, so a grep of `mercury-sol/` can no longer land in it. A
`README-WHY-THIS-IS-HERE.md` was added stating that it is stale, must not be used as a source of
truth, and that **Titan's authoritative code is the separate live-money bot at `/root/titan-bot`,
not to be modified**. **Its parameters were not read.**

---

# CONFIRMATION SET

| check | result |
|---|---|
| **entry prompt byte-identical / frozen surface untouched** | ✅ every `_call` code line identical; user-prompt builder untouched; `_ENTRY_SYSTEM*` constants unchanged. Newest stored prompt still carries `PROPOSED ENTRY`, the `1H:` tier line and `Of the 3 tier(s) shown` |
| **window NOT reset** | ✅ **4 of 200**, before and after |
| **`OBSERVATION_MODE` True proven live in the new pid** | ✅ `[VIRTUAL] poller started in pid 1184217` — the live-mode branch prints a different line and returns |
| **engine still the single manager** | ✅ `[MONITOR] RETIRED` · `live adapter registered` |
| **no open position** | ✅ 0 |
| **Tor → Bybit / OKX** | ✅ both live (mid ≈ $71.65) |
| **Titan untouched** | ✅ clean · `HEAD 3316e8a` · active · **no `.py` modified** |
| **tracebacks since restart** | ✅ **0** |
| **`py_compile`** | ✅ `claude_advisor.py`, `main.py`, `virtual_trader.py`, `config.py` |
| **backfill** | 🛑 **NOT RUN** |

Snapshot: `claude_advisor.py.bak_sysprompt_20260801`.

---

# 🛑 WHAT IS WAITING ON YOU

**The §1c backfill of 32 rows.** Guarded, reversible two ways, single transaction, aborts unless
exactly 32 rows change. Say the word.

Everything else in this task is done, and SOL is left to accumulate: **PAPER**, single manager,
prompt frozen, window **4 of 200**.
