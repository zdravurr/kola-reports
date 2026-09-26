# titan-exit-agreement-at-entry-states-the-gate-count-applied-from-flat

_2026-09-26 18:40 UTC_

---

# Titan — **the EXIT advisor's "Agreement at entry:" now states what the gate counted. APPLIED FROM FLAT, `386d5eb`, restart 2026-09-26 18:38:01 UTC.** Before the fix, **90 of 128** gate-renderable exit consultations claimed agreement the gate had not counted, including **every consultation on all five ledger rows**. The ledger now spans **two wording boundaries** and keeps counting to 10. 🟡 In-process proof is **OPEN**: it needs an exit consultation, and that needs an open position.

**2026-09-26 · titan-bot HEAD `991b333` → `386d5eb` · Titan LIVE REAL MONEY · Mercury-SOL NOT TOUCHED · `openitems_guard` EXIT=0 before and after · book FLAT before and after**

---

## THE VERDICT FIRST

| | result |
|---|---|
| change | `signal_tiers.entry_thesis_lines` only (AST 17 → 17 nodes, one changed). It reuses `_gate_agreement()` from `991b333` on the stored entry facts. Render-only. |
| census | 185 stored exit consultations carry the line: **128 render the gate count, 57 fall back** (the `AI_ADVISOR_HIDE_1H` era). **90 of 128 (70.3 %)** claimed agreement the gate had not counted. |
| ledger rows | **All 5 (vpos 101, 104, 105, 106, 108) carried a misleading line on every one of their consultations** (3, 6, 7, 13 and 12). **Not re-scored.** |
| contract | RED on `991b333` (8 failing) → **GREEN 30/30**. All **9** Titan contracts GREEN, root AND botuser. Live `trades.db` opened **0** times (strace). |
| applied | From flat (18:36:39 and 18:37:56 UTC). Restart 18:38:01, MainPID 912030 → **927117**, worker 927166. Boot line ✅ 0/0. |
| in-process | 🟡 **OPEN.** No exit consultation has happened since the restart; the book is flat. How to close it is in §3d. |
| ledger | **5 RESOLVED of 10, Σ +1.0497R, unchanged.** It now spans TWO wording boundaries. The rule still decides at 10. |

---

# 1. THE CHANGE

## 1a. Every place the exit advisor receives the slot-agreement sentence

There is **exactly one path**:

1. `signal_tiers.entry_thesis_lines` @ `991b333`, lines 578–579:
   ```python
       if facts.get('agreement'):
           out.append(f"  Agreement at entry: {facts['agreement']}")
   ```
   `facts['agreement']` is `_agreement()`'s **slot** sentence, persisted in `entry_tiers_json` at entry.
2. `main._entry_signals_for_exit`, line **3002**: `out['entry_tier_block'] = signal_tiers.entry_thesis_lines(facts)`. `facts` is `json.loads(entry_tiers_json)` of the position's entry row.
3. `claude_advisor.consult_for_close_rich`, line **1087**: `f"{ctx.get('entry_tier_block') or ...}"`, under the heading `ENTRY THESIS — the exact tiers that opened this position`.

Checked and not affected:
- The legacy path (pre-2026-07-29 rows) prints `(legacy record)` tier lines and **no** agreement sentence.
- `consult_for_close` (the non-rich prompt) prints none.
- No other `.py` file reads `facts['agreement']`.
- The next prompt line, `Advisor's reason at entry:`, is the entry model's **own stored words**. On vpos 112 it says "15m+5m BULL confluence". It is quoted as the model's reason, not generated as a fact, so it is **not changed**.

## 1b–d. The fix

```python
    if facts.get('agreement'):
        _counted = _gate_agreement(facts)
        out.append(f"  Agreement at entry: "
                   f"{_counted if _counted is not None else facts['agreement']}")
```

- **Reuses `_gate_agreement()` from `991b333`** on the stored entry tiers. Nothing is recomputed.
- The persisted `entry_tiers_json` and `facts['agreement']` are **unchanged**.
- **The line appears exactly when it did before.** It is only emitted when a stored agreement exists, so no line is ever added.
- **Falls back to today's sentence byte-identical** when the stored record lacks a boolean `counted_by_gate` on all three tiers, or a LONG/SHORT `gate_direction` on a counted tier. That covers older rows, `AI_ADVISOR_HIDE_1H` records (the 1H gate direction was stripped at entry, and it still does not leak), and malformed input.
- **Facts only.** The contract bans the same 12 words: `therefore / should / skip / execute / lean / consider / avoid / caution / risk / favour / recommend / suggest`.
- **AST:** `signal_tiers.py` 17 → 17 top-level nodes; **only `entry_thesis_lines` differs**; 0 added, 0 removed. sha256 `2870ccc423c9fc4c` → `bfa7fe7172c98b61`.

## 1e. Census: every stored exit consultation (read-only)

**185** stored consultations carry `Agreement at entry:` (2026-07-30 → 2026-09-23 08:00:26): 182 live, 3 paper. **185 of 185** were matched to their position by the Agreement line and the position's open window.

| | n |
|---|---|
| would render the new gate-count line | **128** |
| fall back to today's sentence (HIDE_1H-era entries, 1H gate direction stripped) | **57** |
| **old line claimed agreement the gate had NOT counted** (of the 128) | **90 (70.3 %)** |
| old line consistent with the gate count | 38 |

By position (consultations / misleading): 93 1/1 · 94 7/7 · 95 13/0 · 96 2/2 · 97 3/0 · 98 6/6 · 99 3/3 · 100 5/0 · **101 3/3** · 102 2/0 · 103 1/0 · **104 6/6** · **105 7/7** · **106 13/13** · 107 1/1 · **108 12/12** · 109 13/0 · 110 1/0 · 111 7/7 · 112 22/22.

🔴 **Ledger `ai_exit` closes: all five carried a misleading line on EVERY consultation, the closing one included.**

| vpos | old line (slot) | what the gate counted at entry |
|---|---|---|
| 101 | "15m and 1H and 5m all point SHORT; … 15m+1H+5m agree" | 2 of 3 (15m, 5m); 1H expired on its TTL |
| 104 | "… all point LONG; … 15m+1H+5m agree" | 2 of 3 (15m, 5m); 1H not counted |
| 105 | "… all point SHORT; … 15m+1H+5m agree" | 2 of 3 (1H, 5m); 15m not counted |
| 106 | "… all point SHORT; … 15m+1H+5m agree" | 2 of 3 (1H, 15m); 5m not counted |
| 108 | "… all point LONG; … 15m+1H+5m agree" | 2 of 3 (1H, 5m); 15m not counted |

**Stated, not re-scored.** Whether the claim influenced any of those verdicts is not measured here.

## 1f. Before / after on a real stored exit consultation: vpos 112, trades 34772, 2026-09-23 08:00:26 UTC

That is the `armed_exit` consultation; the advisor said HOLD 0.72, and the verdict was discarded. The entry had counted **1 of 3** tiers. The stored ENTRY THESIS block is reproduced verbatim by the baseline renderer.

```
ENTRY THESIS — the exact tiers that opened this position
  1H:  Bullish Confirmation+  (LONG, weight 1.0, set 5.7h ago at entry)
  15m: HyperWave Signal Up  (LONG, weight 0.7, set 30m ago at entry)
        NOT counted by the gate — this category's own signals disagree (LONG 1.75 / SHORT 1.75 across 2 signals), so it nets NEUTRAL — both sides are inside the MOMENTUM 90-min window (LONG: HyperWave Signal Up 30 of 90 min; SHORT: HyperWave Signal Down 60 of 90 min)
  5m:  Bullish S-CHOCH+  (LONG, weight 1.0, set 0m ago at entry)
        NOT counted by the gate — this category's own signals disagree (LONG 2.50 / SHORT 2.00 across 3 signals), so it nets NEUTRAL — both sides are inside the EXECUTION 5-min window (LONG: Bullish S-CHOCH+ 0 of 5 min, Bullish OB Created 0 of 5 min; SHORT: Bearish OB Entered 0 of 5 min)
BEFORE:  Agreement at entry: 15m and 1H and 5m all point LONG; vs the proposed LONG: 15m+1H+5m agree.
AFTER:   Agreement at entry: Counted by the gate: 1 of 3 tiers (1H LONG); vs the proposed LONG: 1H agrees. 15m and 5m point LONG on their slots but net NEUTRAL inside their categories and were not counted.
  Advisor's reason at entry: 1d/4h/1h all BULL with strong ADX (44.5/49.0/39.4); 15m+5m BULL confluence; ...
```

**Whole-prompt diff** (4,669 chars; the stored prompt with the old block replaced by the new):
```
--- stored 34772
+++ patched 34772
@@ -55 +55 @@
-  Agreement at entry: 15m and 1H and 5m all point LONG; vs the proposed LONG: 15m+1H+5m agree.
+  Agreement at entry: Counted by the gate: 1 of 3 tiers (1H LONG); vs the proposed LONG: 1H agrees. 15m and 5m point LONG on their slots but net NEUTRAL inside their categories and were not counted.
```

---

# 2. CONTRACT

**New sibling: `tests/test_exit_agreement_line_states_gate_count.py`**, 30 checks. Fixtures are **embedded**: read-only copies of trades 34546's `entry_tiers_json` and trades 34772's stored exit prompt.

| pin | what |
|---|---|
| 0 | baseline = `signal_tiers.py` @ `991b333`, sha256-pinned |
| X1a–c | The baseline renders the stored exit ENTRY THESIS block verbatim. The new line is exact. The whole exit prompt differs in ONE line. |
| X2.1–6 | Six tier shapes (3 of 3; opposing; TTL + intra; slot absent but counted; none counted; reset). **The exit line is the SAME sentence as the entry `Agreement:` line**, and nothing else in the block moves. |
| X4 ×6 | the 12-word ban list |
| X5 ×6 | the **ENTRY prompt (`render`) byte-identical to `991b333`**, and `facts['agreement']` unchanged |
| X3a–d | No breakdown; partial breakdown; 9 malformed / no-agreement inputs (exceptions included; no line added); the HIDE_1H record. All byte-identical to the baseline, with no 1H leak. |
| X6 | the four SYSTEM prompts sha256-pinned |

**The `991b333` contract (`test_agreement_line_states_gate_count.py`) was edited deliberately.**
- Its six `[E]` checks pinned `entry_thesis_lines` byte-identical to `f53d048`, which this change intends to move.
- They now pin `facts['agreement']` and **every exit line except the twin**. The twin is pinned by the sibling.
- Unedited, it fails exactly those six `[E]` checks and nothing else. That was verified before the edit.
- `.bak_exitagreement_20260926` kept.

| run | root | botuser (sha256-pinned sandbox copies) |
|---|---|---|
| **RED**, subject = `991b333` file | **8 failing**: X1b, X1c, X2.1–X2.6. Every identity pin passes. | **8 failing**, same |
| **GREEN**, subject = patch | **30/30** | **30/30** |
| all 9 Titan contracts | **9/9 GREEN**, `trades.db` opens **0** | **9/9 GREEN**, `trades.db` opens **0** |

The botuser pass used the `/tmp/titan-contract-agreement` sandbox from the `991b333` pass, refreshed with the new files (sha256 shown equal): `.py` sources, baselines and tests, with no `.env`, no DB and no logs. Its `_dict_local.py` points at the sandbox's own `signal_matrix.py` copy, because botuser cannot read `/root`.

---

# 3. APPLIED — FROM FLAT

| step | result |
|---|---|
| **flat, 18:36:39 and again 18:37:56 UTC** | DB 0 open rows, 0 `exit_pending`, 0 breakeven jobs. BingX unified and raw probes both 0 positions and 0 open orders; error list **empty**. |
| `.bak` | `signal_tiers.py.bak_exitagreement_20260926` (`2870ccc423c9fc4c` = the `991b333` file) · `tests/test_agreement_line_states_gate_count.py.bak_exitagreement_20260926` · `OPEN-ITEMS.md.bak_exitagreement_20260926` |
| commit | **`386d5eb`**: `signal_tiers.py` plus the two contracts, nothing else |
| **restart** | `systemctl restart titan` at **18:38:01 UTC**. MainPID **912030 → 927117**, worker **927166**, NRestarts 0. |
| boot line | `[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)` at 18:38:12. 0 tracebacks. |
| loaded bytecode (`config.pyc`, `claude_advisor.pyc`, headers == source) | SL_ATR_MULT **2.25** · TRAIL_MULT_ATR **1.6875** · EXIT_ADVISOR_DRYRUN **False** · BOOK_GATE_DRYRUN **False** · CLAUSE_A **True** / CLAUSE_B **False** · LIVE_TRADING_ENABLED **True** · ORDER_ADAPTER_LIVE **True** · LIVE_FIXED_MARGIN_USDT **30.0** · LEVERAGE **5** · AI_ADVISOR_HIDE_1H False. SYSTEM prompts: `_ENTRY 30c979595a4831aa`, `_LEARNING 191cf5d71ebf3865`, `_CLOSE 7d7707cfa2d336f7`, `_CLOSE_RICH 3d709571e17ff405`, all identical. |
| `openitems_guard` | EXIT=0 before. **EXIT=0 after** (canon header → `386d5eb`). |

## 3d. 🟡 IN-PROCESS PROOF: **OPEN, stated plainly**

- `signal_tiers` is imported **lazily** (`claude_advisor.py:567`, `main.py:2999`). At the restart, `signal_tiers.cpython-312.pyc` still held the **`991b333` compile** (written 17:00:12), with a header that does **not** match the new source. The worker recompiles it on first import.
- **The proof is an EXIT consultation rendering the new line.** Exit consultations only happen while a position is open, and **the book is flat.** **No exit consultation has occurred since the restart, so the exit render is NOT yet proven in-process.**
- **How to confirm it later:**
  ```sql
  SELECT id, timestamp FROM trades
   WHERE timestamp > '2026-09-26 18:38:01' AND signal_type LIKE 'exit_ai%'
     AND ai_user_prompt LIKE '%Agreement at entry: Counted by the gate:%';
  ```
  The first row returned closes it. Also, the `.pyc` mtime must be after 18:38:01 with header == source.
- ⚠️ A first **entry** consultation after 18:38 only proves that the module recompiled. It does **not** prove the exit render.

---

# 4. RECORD (canon)

- **`§0.AGREEMENT-LINE`:** exit twin fixed in `386d5eb`. **EXIT-SIDE COHORT BOUNDARY 2026-09-26 18:38:01 UTC.** The census is recorded, and the in-process item is OPEN with its closing query.
- **`§0.EXIT-ADVISOR-RULE`:** it now states that the ledger spans **TWO wording boundaries**, and that **the rule is unchanged**: it decides at **10 RESOLVED `ai_exit` closes**, same measure, same sign test. Nothing is re-scored.
  - Boundary (1): **2026-09-12 14:58:32 UTC**, `f16c271`, the unarmed-trail fact.
  - Boundary (2): **2026-09-26 18:38:01 UTC**, `386d5eb`, this change.

| row | vpos | closed (UTC) | vs boundary (1) 09-12 14:58:32 | vs boundary (2) 09-26 18:38:01 |
|---|---|---|---|---|
| 1 | 101 | 09-01 18:00 | before | before |
| 2 | 104 | 09-09 08:30 | before | before |
| 3 | 105 | 09-09 23:46 | before | before |
| 4 | 106 | 09-12 09:15 | before | before |
| 5 | 108 | 09-14 17:00 | **after** | before |

**Ledger: 5 RESOLVED of 10, Σ +1.0497R / +$1.72. Unchanged; it has not moved since vpos 108 on 09-14.** Rows 6–10 will all fall after both boundaries. All five resolved rows were decided under the slot sentence.

- Canon header HEAD → `386d5eb`. The `386d5eb` entry was added.

## Confirmations

- **Every write was stated before it ran:**
  - `.bak` ×3;
  - `signal_tiers.py`;
  - the new contract;
  - the edited `991b333` contract;
  - commit `386d5eb`;
  - the canon (as botuser);
  - the refreshed botuser sandbox (no secrets, no DB);
  - this report and one Telegram message.
- **`trades.db`:** opened only `mode=ro` + `query_only` for the census and fixtures. The contracts opened it **0** times.
- **Venue:** GET only. **0 orders placed, 0 cancelled.**
- **Exactly one restart:** titan, from flat, 18:38:01 UTC. NRestarts 0.
- **Mercury-SOL untouched:** MainPID 222221, NRestarts 0. Not read, not opened.
- `EXIT_ADVISOR_DRYRUN` / `BOOK_GATE` flags untouched (read back from the loaded bytecode).
