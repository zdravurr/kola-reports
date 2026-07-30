# titan-observatory-identity-guard-shipped-row80-retired-row79-awaiting-call

_2026-07-30 22:29 UTC_

---

# TITAN — OBSERVATORY: IDENTITY GUARD SHIPPED, ROW 80 RETIRED, ROW 79 AWAITING YOUR CALL

**2026-07-30 22:30 UTC · HEAD `54dc734` · LIVE · vpos 87 LONG open · runtime = commit, proved from bytecode**

---

## DECISION LINE

**Items 1 and 2 are done and verified. Item 3 is reported, not acted on — as instructed.**

🔴 **And item 2 turned up something that changes the picture: OPEN-ITEMS §2.28a is wrong about row 80, and my own guard's remedy text was wrong with it.** §2.28a says `virtual_positions` "has no row 89 and **never will**". `sqlite_sequence` for `virtual_positions` is at **87**, so AUTOINCREMENT will issue **88 and 89 to the next two positions**. Worse: `status='failed'` drops a row out of `tick()` but does **not** free its `vpos_id`, which is `UNIQUE`. A human following my first shout verbatim would have retired the row and then seen the guard shout again on the same id.

Fixed in `54dc734` before anything else was applied. The remedy now names **both** statements. **Row 80 will block vpos 89 from arming unless its key is freed — that is a new open item, and it is item 3's sibling, not part of it.**

---

## SCOPE — CONFIRMED, NOT ASSERTED

**Code changed by this session (`dee6cee..54dc734`): exactly one file.**

```
 titan-bot/post_exit_observatory.py | 105 ++++++++++++++++++++++++++++++++
 1 file changed, 105 insertions(+)
```

| trading-path module | status vs `dee6cee` |
|---|---|
| `main.py` (entry gate, HTF cascade, score gate) | **UNCHANGED** |
| `config.py` (thresholds, sizing, flags) | **UNCHANGED** |
| `virtual_trader.py` (SL / trail / breakeven / LONG partial) | **UNCHANGED** |
| `signal_matrix.py`, `risk_manager.py` | **UNCHANGED** |
| `claude_advisor.py` (entry + exit advisor) | **UNCHANGED** |
| `breakeven_worker.py`, `macro_filter.py` | **UNCHANGED** |

**Gate constants read from runtime after the restart:** `CONFLUENCE_SCORE_THRESHOLD = 3.0` · `CONFLUENCE_FLAT_THRESHOLD = 5.0` · `LIVE_TRADING_ENABLED = True` · `ORDER_ADAPTER_LIVE = True` · `MAX_POSITIONS_PER_SIDE = 1`.

**Data changed:** one column on one row — `post_exit_observatory.id=80.status`. `virtual_positions` still holds **61 rows** (nothing deleted; `feedback_no_delete_virtual_positions` respected). `post_exit_observatory` still **42 rows**; `post_exit_drift_samples` still **200 rows**.

**Mercury-SOL untouched:** `active`, `NRestarts=0`, running since **2026-07-21 06:39:33**; **0** `.py` files modified today.

**The observatory remains read-only with respect to trading.** It is imported at four points — `tick` (breakeven_worker), `on_entry` / `on_real_close` (virtual_trader), `on_15m_exit_signal` (main) — and every one is a recorder. Nothing in this change can place, cancel, or size an order.

---

## 1. THE `on_entry` IDENTITY GUARD — SHIPPED (`45e20e7`, message fix `54dc734`)

### The defect, restated exactly

`vpos_id` is not an identity. `virtual_positions.id` is unique only among rows that still **exist**; AUTOINCREMENT re-issues an id once the owning row is deleted and `sqlite_sequence` is lowered. So `ON CONFLICT(vpos_id) DO NOTHING` does not mean *"already armed"* — it means *"something holds this id"*, and the insert silently **adopts** it.

### The fix — §2.19 shape: compare the entry instant, and make the conflict speak

```python
def _same_position(existing_opened_at, incoming_opened_at):
    """Fails CLOSED: anything unparseable is treated as a DIFFERENT position, so an
    unreadable stamp produces a refusal (loud, recoverable) rather than an
    adoption (silent, corrupting)."""
    if existing_opened_at == incoming_opened_at:
        return True
    a = _parse_dt(existing_opened_at)
    b = _parse_dt(incoming_opened_at)
    if a is None or b is None:
        return False
    return abs((a - b).total_seconds()) <= IDENTITY_EPSILON_S   # 1.0 s
```

`_identity_conflict()` returns the pre-existing row **iff** it describes a different position; both hooks then `return` without writing.

🔴 **Guarded in BOTH hooks, not only `on_entry` — and this is a deliberate extension of your instruction.** `on_real_close` is what actually did the damage: its own upsert hits the same `DO NOTHING`, and its `UPDATE` then stamps the real close over the ghost. **Guarding `on_entry` alone would not have prevented the observed corruption**, because "`on_entry` wrote nothing" is precisely the state `on_real_close` inherits. A guard that leaves the damage path open is decoration.

**Deliberately non-mutating on the conflict path.** The guard writes nothing anywhere when it refuses. A row whose ownership is in dispute is the wrong thing for an automated hook to touch, and the resulting state is already queryable:

```sql
-- positions that opened but have no observatory row
SELECT v.id, v.opened_at FROM virtual_positions v
LEFT JOIN post_exit_observatory o ON o.vpos_id = v.id AND o.opened_at = v.opened_at
WHERE o.id IS NULL;
```

### Proof it cannot break arming, and cannot fire on the normal path

Run against a **copy** of `trades.db` (`DB_PATH` repointed, asserted not to be the live path; live DB confirmed untouched afterwards — 42 rows, 0 rows with `vpos_id > 9000`).

| # | case | result |
|---|---|---|
| A | genuinely new `vpos_id` → arms normally | **PASS** — row created, count +1, `shadow_armed_pending_close`, entry recorded |
| B | same position re-arming, identical `opened_at` | **PASS** — no duplicate, row untouched, **guard silent** |
| B2 | same position, `opened_at` differing by 0.4 s | **PASS** — still the same position, silent |
| C | ghost case: same id, `opened_at` 3 h apart | **PASS** — refused, no new row, existing row **not overwritten, not adopted** |
| D | `on_real_close` on a mismatched row | **PASS** — `real_close_price` stayed `NULL`, row wholly unchanged, **0 drift slots seeded** |
| E | `on_real_close` on a **matching** row | **PASS** — close stamped (71500.0), **5 drift slots seeded** |
| F | unparseable / `None` `opened_at` | **PASS** — refuses (fails closed) |
| G | **replay of all 42 real rows** | **PASS** — 40 match; **exactly one refuses: row 79 / vpos 86**, the known ghost; **the LIVE row (id 85 / vpos 87) matches and does not fire** |

**G is the load-bearing test:** the guard fires on precisely the one historical row that is known-bad and on nothing else — and it leaves the currently-open position alone.

Also: `py_compile` **37/37**; symtable audit **clean, 0 unbound function-scope names**. *(A first audit run reported "1 finding" — it had been run from `/root`, not `/root/titan-bot`, and the finding was a pre-existing syntax error in the standalone `/root/bingx_trade.py`, outside this repo and untouched. Re-run in the correct directory: 37 files, clean.)*

### 🔴 The remedy text was wrong, and I fixed it before applying anything (`54dc734`)

My first shout told a human to retire a stale row with `status='failed'`. **That is insufficient.** `vpos_id` is `UNIQUE`, so the row keeps blocking the incoming position regardless of status. Found while checking row 80. The message now names both statements:

```
🔴 [OBSERVATORY-IDENTITY] REFUSING on_entry for vpos_id=89 — observatory row 80
already holds that vpos_id but describes a DIFFERENT position.
existing: opened_at=2026-07-29T21:50:11.625939+00:00 entry=63595.5 status=shadow_pre_close
| incoming: opened_at=2026-08-02T09:00:00+00:00.
vpos ids are re-issued after deletion, so the existing row is stale residue, NOT this
position. NOT adopting it: this position will have NO observatory row, and NO figure
will be computed across two positions.
HUMAN ACTION — verify the stale row against virtual_positions, then retire it with
BOTH statements:
  "UPDATE post_exit_observatory SET status='failed', vpos_id=-80,
   updated_at=datetime('now') WHERE id=80;"
status='failed' drops it out of tick(); re-keying vpos_id NEGATIVE is what actually
FREES the id — vpos_id is UNIQUE, so leaving it in place keeps blocking this position
no matter what its status says. A negative key can never collide with a real
AUTOINCREMENT id and keeps the row's history intact. Do NOT delete rows.
```

**What a human does when it shouts**, in order:

1. **Nothing is on fire.** Trading is unaffected; one position simply has no shadow record. Do not restart anything.
2. **Verify** the stale row is genuinely residue: `SELECT * FROM post_exit_observatory WHERE id=<n>;` against `SELECT * FROM virtual_positions WHERE id=<vpos_id>;` — different `opened_at` confirms it.
3. **Retire it with both columns** (SQL above). Nothing is deleted; the row keeps its history under a negative key.
4. The **next** position taking that id arms cleanly. The position that was refused stays unrecorded — the observatory is a sensor, and one lost sample is the correct price for never producing a cross-position figure.

---

## 2. ROW 80 — RETIRED ✅

**The three confirmations you asked for, before the change:**

| # | check | result |
|---|---|---|
| 1 | is `'failed'` the sentinel the code already uses? | **Yes.** Declared in the module's status taxonomy (`"'failed' — symbol delisted / unrecoverable error"`); `_active_rows()` filters `status NOT IN ('completed','failed')`; `_refresh_status()` returns early on `'failed'` (sticky/terminal); `_bump_error()` already sets it. **No new status was invented.** |
| 2 | does anything else read that row? | **No.** The table has **zero readers outside the module** — the only imports anywhere are `tick`, `on_entry`, `on_real_close`, `on_15m_exit_signal`. Within the module, row 80 was reachable only via `_active_rows()`. `on_15m_exit_signal`'s `UPDATE` requires `shadow_exit_at IS NULL`; row 80 has it set, so it could never match again. |
| 3 | is any drift data lost? | **No — there was none.** `SELECT count(*) FROM post_exit_drift_samples WHERE observatory_id=80` → **0**, before and after. Drift can only be seeded by `on_real_close`, which needs a `virtual_positions` row that did not exist. |

**Applied** (DB backed up first to `/root/backups/pre-obs-row80-20260730-222105/trades.db`, 60,653,568 bytes), with a guarded predicate so it could only ever match the intended row:

```sql
UPDATE post_exit_observatory SET status='failed', updated_at=?
 WHERE id=80 AND vpos_id=89 AND status='shadow_pre_close';   -- 1 row
```

| | before | after |
|---|---|---|
| row 80 status | `shadow_pre_close` | **`failed`** |
| `tick()` working set | 79, **80**, 85 | **79, 85** |
| drift rows for 80 | 0 | **0** |
| shadow leg (`shadow_exit_at`, `shadow_pnl_r` −0.6059) | intact | **intact** |
| row 79 | untouched | **untouched** (`updated_at` still 15:01:22) |
| row 85 (live, vpos 87) | untouched | **untouched** |
| total observatory rows | 42 | **42** |

**It is inert and now also silent.** Nothing was deleted; the row remains fully readable as a record of what happened.

### 🔴 NEW OPEN ITEM — row 80 still holds `vpos_id = 89`, and vpos 89 is coming

This is **not** part of item 3 and I have not acted on it.

- `sqlite_sequence` for `virtual_positions` is **87**. The next two positions take **88**, then **89**.
- `vpos_id` is `UNIQUE`, and the guard keys on it regardless of status. When vpos **89** opens, `on_entry` will **refuse and shout**, and vpos 89 will get **no observatory row**.
- **Headroom: two positions.** At the current rate that is days, not hours, and the guard makes the failure loud rather than silent — so this is a scheduled chore, not an emergency.
- **The one-statement fix, for your decision** (same shape as the shout's remedy):

```sql
UPDATE post_exit_observatory SET vpos_id = -80, updated_at = datetime('now') WHERE id = 80;
```

Negative keys cannot collide with AUTOINCREMENT ids, the row keeps its history, nothing is deleted. **I did not run it: you scoped item 2 to one column, and this is a second one on a row whose disposition is adjacent to item 3.**

**This also corrects OPEN-ITEMS §2.28a**, which states row 89 "never will" exist. It will.

---

## 3. ROW 79 — BOTH OPTIONS, COSTED. NOT ACTED ON.

🔴 **Per your standing instruction, row 79's `exit_advantage_r` is not quoted as a result anywhere in this report.** The figures below appear only as inputs to your decision.

**First, a fact that has changed since §2.28a was written at 13:40:** the **4h slot has since sampled** — 15:51:22 UTC, price 64705.9. §2.28a lists 4h as still due. Three of five slots are now banked.

### Option A — REPAIR

**Fields that change (3 identity + 4 derived):**

| field | current (ghost) | repaired (real vpos 86) |
|---|---:|---:|
| `entry_price` | 63605.6 | **63686.0** |
| `original_sl_price` | 64724.6 | **64767.1** |
| `opened_at` | 2026-07-29T21:50:04.012998+00:00 | **2026-07-30T00:50:14.893642+00:00** |
| `shadow_pnl_pct` | −1.0500647742 | **−0.9224947398** |
| `shadow_pnl_r` | −0.5968722073 | **−0.5434279900** |
| `exit_advantage_pct` | 0.5939386175 | **0.7215086518** |
| `exit_advantage_r` | *(not quoted)* | *(not quoted — computed, available on request)* |

**How the derived four are recomputed** — with the module's own functions, no new arithmetic:

```python
shadow_pnl_pct, shadow_pnl_r = _compute_shadow_pnl(
    entry_price=63686.0, exit_price=64273.5,
    position_side='SHORT', original_sl_price=64767.1)
exit_advantage_pct = shadow_pnl_pct - real_pnl_pct     # _maybe_compute_advantage
exit_advantage_r   = shadow_pnl_r   - real_pnl_r
```

The 1R basis changes with the identity: ghost `|63605.6 − 64724.6|` = **1119.0** pts → real `|63686.0 − 64767.1|` = **1081.1** pts.

**Fields already correct — they belong to the real leg and must NOT be touched:** `real_close_price` 64733.0 · `real_close_at` 11:50:54 · `real_close_reason` `sl` · `real_net_pnl` −2.541574 · `real_pnl_r` −1.0221266 · `real_pnl_pct` −1.6440034 · `shadow_exit_price` 64273.5 · `shadow_exit_at` 02:00:05 · `shadow_exit_reason` `15m_signal` · `drift_started_at` · `max_favorable_post_exit_*`.
**Cross-check:** `virtual_positions[86].net_pnl` = −2.541574 = row 79's `real_net_pnl`. **MATCH** — the real leg is genuinely vpos 86's.

### 🔴 Is the recomputation well-defined from data we still have? **Yes — and here is why, not just the assertion**

The only question is whether the **shadow leg** is valid for vpos 86, since the shadow arms at `opened_at` and the ghost armed three hours earlier.

| check | finding |
|---|---|
| ghost armed 21:50:04 · real armed 00:50:14 · shadow exited **02:00:05** | the exit falls **inside** the real position's open window |
| the real window `00:50:14 → 02:00:05` | is a strict **subset** of the ghost window `21:50:04 → 02:00:05` — so no trigger in the extra 3 h can have been missed for the real position |
| exit reason `15m_signal` (Bullish I-CHOCH) | a **market event**, not position-dependent; it would have fired identically for a shadow armed at 00:50 |
| exit price 64273.5 | a market price, independent of entry |
| SL trigger | the ghost's SL **64724.6** is *tighter* than the real **64767.1** for a SHORT (by 42.5 pts). The tighter SL was **not** hit before the 15m signal, so the wider real SL **cannot** have been hit either |
| 72 h max-hold from entry | not reached under either identity |

**Conclusion: the shadow exit's price, time and reason are valid for vpos 86 unchanged. Only the entry-relative arithmetic (pct and R) needs recomputing, and both inputs survive. The repair is well-defined.**

**Cost of repair:** none in data — nothing is lost, the drift leg is untouched and keeps sampling. The cost is that the row's identity fields are *rewritten* rather than preserved, so the audit trail of the mistake lives only in OPEN-ITEMS and this report.

### Option B — RETIRE

Retiring means `status='failed'`, which removes the row from `tick()`. Its five drift slots:

| slot | due (UTC) | state | value |
|---|---|---|---|
| 15m | 07-30 12:05 | **SAMPLED** | 64831.3 · −0.15185% |
| 1h | 07-30 12:50 | **SAMPLED** | 64867.1 · −0.20716% |
| 4h | 07-30 15:50 | **SAMPLED** | 64705.9 · +0.04186% |
| **12h** | **07-30 23:50** | **PENDING** — in **≈1.4 h** | 🔴 **lost** |
| **24h** | **07-31 11:50** | **PENDING** — in **≈13.4 h** | 🔴 **lost** |

**Precisely what retiring now costs: the 12h and 24h drift samples.** The three banked samples survive — they are rows in `post_exit_drift_samples` and retirement does not delete them. Nothing else is lost: the shadow leg, the real leg and the max-favourable watermark are all already written.

**Retirement would also need the same `vpos_id` re-key as row 80** (`vpos_id = -79`), or row 79 keeps blocking a future vpos 86 — though that id is far off, since the sequence is at 87 and does not wrap.

### The timing asymmetry, stated because it is a cost input

**Repair is not time-sensitive** — drift sampling is keyed off `real_close_at` / `real_close_price`, which are already correct, so repairing changes nothing about what the pending slots will record.

**Retirement is time-sensitive** — every hour it waits, it costs less. Retiring after **23:50 tonight** costs only the 24h sample; after **11:50 tomorrow** the row completes on its own and costs nothing, because a row that reaches `completed` leaves `tick()`'s working set by itself.

**I am not recommending an option. Stopping here, as instructed.**

---

## WHAT I DID NOT DO

- **Row 79 was not touched.** `updated_at` is still `2026-07-30T15:01:22.622710+00:00` — the 4h drift sample, written by the running service, not by me.
- **I did not re-key row 80's `vpos_id`**, though I found the need for it and wrote the SQL. You scoped item 2 to one column.
- **I did not quote row 79's `exit_advantage_r`** as a result, per your standing instruction.
- **I did not delete anything.** `virtual_positions` is at 61 rows, observatory at 42, drift samples at 200.
- **I did not touch OPEN-ITEMS** in this pass, though §2.28a now has two errors to correct (row 89 "never will exist"; row 79's 4h slot listed as pending). Flagged, not edited.

---

## STATE AT PUBLICATION — read from runtime

| check | result |
|---|---|
| `git status` | **clean** |
| HEAD | **`54dc73480a2085fa7727ff94a40f2d2a46d9c2d6`** · pushed, `main...origin/main` in sync |
| commits this session | `45e20e7` (guard), `54dc734` (remedy-text fix) |
| **runtime = commit** | ✅ proc start **22:24:27.857 UTC**; newest of **38** `.py` mtimes **22:18:01**; **0** modified after start |
| **guard is in the loaded bytecode** | ✅ `.pyc` header matches source; `_same_position` **present**, `_identity_conflict` **present**, remedy text containing the `vpos_id` re-key **present** |
| `titan.service` | **active**, MainPID **481805**, `NRestarts=0` |
| four boot gates | ✅ LIVE banner · `$30 x 5 = $150` · `RECONCILE-XDB` 1 position / 1 open row · `LONG open, SL present @ 64028.8 — kept` · engine owns positions |
| errors since restart | **0** tracebacks / CRITICAL / `REFUSING TO START` |
| **`[OBSERVATORY-IDENTITY]` shouts in the journal** | **0** — the live row matches, exactly as test G predicted |
| breaker | **untripped** |
| vpos 87 | **open** · LONG 0.0023 @ 64838.7 · SL 64028.8 = `original_sl_price`, never moved · `recheck_status='done'` |
| exchange, **both probes** | position `2082799688088776706` LONG 0.0023 @ 64838.7 on both · order **`2082799690256592896`** `STOP_MARKET @ 64028.8` on both · **stop order id UNCHANGED** across two restarts · 0 orphans |
| balance | `USDT free 480.18 · used 29.83 · total 510.00` |
| Mercury-SOL | **active**, `NRestarts=0`, since 2026-07-21 06:39:33, 0 `.py` touched today |
