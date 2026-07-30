# titan-row79-repaired-row80-rekeyed-openitems-corrected

_2026-07-30 22:45 UTC_

---

# TITAN — ROW 79 REPAIRED, ROW 80 RE-KEYED, §2.28a CORRECTED

**2026-07-30 22:50 UTC · HEAD `54dc734` (unchanged) · LIVE · vpos 87 LONG open · no code, no restart**

---

## DECISION LINE

**All three items done. Data only — not one line of code changed, and the service was never restarted.**

The observatory book is now **clean end to end**: replaying all 42 rows against `virtual_positions`, **41 match and 0 would be refused** by the identity guard (it was 1 before this pass), with row 80 retired under a negative key that no real id can ever reach.

🔴 **The one thing not yet observed: the 12h drift slot fires at 23:50:54 UTC, about an hour from now.** I have proved *structurally* that the repair cannot affect it — the drift path does not read any of the seven repaired fields — but I have not yet watched it happen. **A watcher is armed and I will confirm the actual sample separately.** That claim is the only one in this report resting on proof rather than observation, and it is flagged rather than blurred.

---

## 1. ROW 79 — REPAIRED

**Backup first:** `/root/backups/pre-obs-row79-repair-20260730-223630/trades.db` (60,669,952 bytes).

### The seven changed fields

| field | **BEFORE (ghost)** | **AFTER (real vpos 86)** |
|---|---:|---:|
| `entry_price` | `63605.6` | **`63686.0`** |
| `original_sl_price` | `64724.6` | **`64767.1`** |
| `opened_at` | `'2026-07-29T21:50:04.012998+00:00'` | **`'2026-07-30T00:50:14.893642+00:00'`** |
| `shadow_pnl_pct` | `-1.0500647741708224` | **`-0.9224947398172256`** |
| `shadow_pnl_r` | `-0.5968722073279727` | **`-0.5434279900101755`** |
| `exit_advantage_pct` | `0.5939386174694139` | **`0.7215086518230107`** |
| `exit_advantage_r` | `0.4252543887272212` | **`0.47869860604501846`** |

The identity is now settled, so the figure is quotable again: **`exit_advantage_r = +0.47870`**, superseding the published `+0.42525`. The 1R basis moved with it — ghost `|63605.6 − 64724.6|` = 1119.0 pts → real `|63686.0 − 64767.1|` = **1081.1 pts**.

### Method — the module's own functions, and a predicate that could only match one row

**Step 1**, the three identity fields, guarded on every old value simultaneously:

```sql
UPDATE post_exit_observatory
   SET entry_price=?, original_sl_price=?, opened_at=?, updated_at=?
 WHERE id=79 AND vpos_id=86
   AND entry_price=63605.6 AND original_sl_price=64724.6
   AND opened_at='2026-07-29T21:50:04.012998+00:00';     -- rows matched: 1
```

Asserted `== 1` before continuing; anything else aborts.

**Step 2**, the shadow leg — **recomputed by the module, not by me**:

```
P._compute_shadow_pnl(63686.0, 64273.5, 'SHORT', 64767.1)
  -> pct = -0.9224947398172256   r = -0.5434279900101755
```

written back under a second guarded predicate (`id=79 AND vpos_id=86 AND entry_price=63686.0 AND shadow_exit_price=64273.5`), rows matched **1**.

**Step 3**, the advantage — **written by the module itself**:

```
P._maybe_compute_advantage(79)
```

It re-read the row and wrote `exit_advantage_pct` / `exit_advantage_r` on its own. No arithmetic of mine touched the derived four.

*(Import hygiene: `TITAN_PEO_AUTO_INIT=0` and `_db_ready=True`, so importing the module ran no schema DDL against the production DB. `DB_PATH` was asserted to be the live path before writing — the inverse of the assertion used when testing the guard on a copy.)*

### The real leg and the drift leg — all 15 fields verified byte-identical

| field | value (unchanged) | | field | value (unchanged) |
|---|---|---|---|---|
| `real_close_price` | 64733.0 | | `shadow_exit_price` | 64273.5 |
| `real_close_at` | 2026-07-30T11:50:54.834420+00:00 | | `shadow_exit_at` | 2026-07-30T02:00:05.053582+00:00 |
| `real_close_reason` | `sl` | | `shadow_exit_reason` | `15m_signal` |
| `real_net_pnl` | −2.541574 | | `drift_started_at` | 2026-07-30T11:50:54.834420+00:00 |
| `real_pnl_r` | −1.022126596055194 | | `max_favorable_post_exit_price` | 64583.6 |
| `real_pnl_pct` | −1.6440033916402363 | | `max_favorable_post_exit_pct` | 0.23079418534596163 |
| `status` | `shadow_completed` | | `max_favorable_post_exit_at` | 2026-07-30T15:01:22.622710+00:00 |
| `vpos_id` | 86 | | | |

**0 of 15 changed.**

**Cross-check you asked for:** `virtual_positions[86].net_pnl = -2.541574` **=** row 79's `real_net_pnl = -2.541574` → **MATCH**.

**And the identity now agrees with the source of truth:**

| | observatory 79 | `virtual_positions` 86 | |
|---|---|---|---|
| `entry_price` / `initial_fill_price` | 63686.0 | 63686.0 | **MATCH** |
| `original_sl_price` | 64767.1 | 64767.1 | **MATCH** |
| `opened_at` | 2026-07-30T00:50:14.893642+00:00 | 2026-07-30T00:50:14.893642+00:00 | **MATCH** |

### The 12h slot — structural proof now, observation pending

Drift slots after the repair: **5 rows, 3 sampled, 2 pending** — exactly as before.

| slot | due (UTC) | state |
|---|---|---|
| 15m | 12:05:54 | sampled 12:06:11 → 64831.3 · −0.15185% |
| 1h | 12:50:54 | sampled 12:51:00 → 64867.1 · −0.20716% |
| 4h | 15:50:54 | sampled 15:51:22 → 64705.9 · +0.04186% |
| **12h** | **23:50:54** | **pending — fires in ≈1 h** |
| 24h | 07-31 11:50:54 | pending |

**Why the repair cannot have disturbed it**, read off the code rather than assumed:

```python
_sample_due_drift(obs_id, row['real_close_price'], side, price, now)
```
It reads `real_close_price` (unchanged), `position_side` (unchanged), the child row's `due_at` (unchanged) and the live price. **None of the seven repaired fields appears in the drift path.**

The two repaired fields that `_process_row` *does* read — `original_sl_price` and `opened_at` — live only in the `elif not shadow_triggered:` branch (shadow SL hit, 1h reversal, 72 h max-hold). Row 79 has **both** `shadow_exit_at` **and** `shadow_exit_price` set, so `shadow_triggered` and `shadow_finalized` are both true and **that branch is unreachable for this row**. Row 79 also remains in `tick()`'s working set (`status='shadow_completed'`).

**Empirically so far:** the service has been ticking over the repaired row every 5 s since 22:36 — **0 tracebacks, 0 CRITICAL, 0 observatory failures, 0 guard shouts.**

**Watcher armed** for 23:51:30 UTC; the observed sample will be reported separately.

### Why repair rather than retire — on the record

Recorded in OPEN-ITEMS §2.28b, in your words and mine: the shadow leg was **proven** valid for vpos 86, not assumed. The real window `00:50:14 → 02:00:05` is a strict **subset** of the ghost window; the exit reason `15m_signal` is a **market event** at a **market price**; and the ghost's SL **64724.6 is tighter than the real 64767.1 for a SHORT** (by 42.5 pts) and was not hit before the signal, so the wider real SL cannot have been. Only entry-relative arithmetic needed recomputing, and both inputs survived. Live-money observatory records will be scarce for months.

---

## 2. ROW 80 — RE-KEYED

**Backup first:** `/root/backups/pre-obs-row80-rekey-20260730-223740/trades.db`.

```sql
UPDATE post_exit_observatory SET vpos_id=-80, updated_at=?
 WHERE id=80 AND vpos_id=89 AND status='failed';        -- rows matched: 1
```

**History preserved — exactly two fields differ, `vpos_id` and `updated_at`.** Everything else is byte-identical: `entry_price` 63595.5 · `original_sl_price` 64714.5 · `opened_at` 21:50:11.625939 · `shadow_exit_price` 64273.5 · `shadow_exit_at` 02:00:05 · `shadow_exit_reason` `15m_signal` · `shadow_pnl_pct` −1.0661131683845637 · `shadow_pnl_r` −0.6058981233243967 · `shadow_signal_details` (the full I-CHOCH JSON) · `shadow_completed_at` · `created_at`. **Nothing deleted; the row remains fully readable as the record of what happened.**

### Would the guard still fire? Run live against the DB, not reasoned about

```
_identity_conflict(vpos_id=89, ...)  -> None   ->  vpos 89 will arm cleanly
_identity_conflict(vpos_id=88, ...)  -> None   ->  the very next id is clear
_identity_conflict(vpos_id=86, ...)  -> None   ->  row 79's identity now agrees
```

**Full replay of all 42 rows:**

| | before this pass | **after** |
|---|---:|---:|
| rows matching their `virtual_positions` row | 40 | **41** |
| rows the guard would **refuse** | **1** (row 79) | 🔴 **0** |
| rows outside the real id space | 1 | 1 — row 80 at `vpos_id = -80`, unreachable by any AUTOINCREMENT id |

---

## 3. OPEN-ITEMS §2.28a — CORRECTED (`831f9a1`)

**(a) "no row 88 or 89 … never will"** — corrected in place. `sqlite_sequence` at **87** is precisely *why* 88 and 89 are the next two ids to be issued: the sequence is a **high-water mark, not a ceiling**. Row 80 was two positions from blocking a real vpos 89.

**(b) row 79's 4h slot listed as pending** — corrected in place. It sampled at **15:51:22** (64705.9, +0.04186%), about two hours after that paragraph was written.

**(c) the new general fact, recorded so the next reader does not rediscover it the hard way:**

> 🔴 **`status='failed'` does NOT free a `UNIQUE` `vpos_id`.** Status controls only whether `tick()` picks the row up (`_active_rows()` filters `status NOT IN ('completed','failed')`). The `UNIQUE(vpos_id)` constraint — and the identity guard, which keys on `vpos_id` regardless of status — keep matching a retired row forever. **Retiring an observatory row takes TWO columns, always.**

This is the fact that made my first remedy text wrong, and it is now recorded in the file, in the guard's shout, and here.

**Plus a new §2.28b** carrying the permanent audit trail: all seven BEFORE values verbatim, the supersession of `+0.42525` by `+0.47870`, the validity proof for the shadow leg, the two-column retirement pattern, and the verified post-state. **The corruption's record survives its repair — which is what the file is for.**

---

## 4. CONFIRMATIONS

### Only observatory data changed — no code, no restart

| | |
|---|---|
| `git status` | **clean**, 0 modified |
| HEAD | **`54dc734`** — *unchanged*, `0` commits since |
| service | MainPID **481805**, started **22:24:27**, `NRestarts=0` — **the same process that was running before the repair.** No restart was needed and none was performed: nothing in `/root/titan-bot` was edited. |
| errors since the repair (22:36) | **0** tracebacks / CRITICAL / observatory failures |
| `[OBSERVATORY-IDENTITY]` shouts | **0** |

### Nothing deleted

| table | rows | expected |
|---|---:|---:|
| `virtual_positions` | **61** | 61 ✅ |
| `post_exit_observatory` | **42** | 42 ✅ |
| `post_exit_drift_samples` | **200** | 200 ✅ |

`vpos 86` itself untouched: `closed`, entry 63686.0, `original_sl_price` 64767.1, `opened_at` 00:50:14.893642, `net_pnl` −2.541574, `close_reason` `sl`. `feedback_no_delete_virtual_positions` respected — no row in any table was deleted at any point.

### Trading path untouched

No file changed, so by construction: entry gate, HTF cascade, score gate, SL / trail / breakeven, LONG partial, entry advisor and exit advisor are all exactly as at `54dc734`. `tick()`'s working set is now `[(79, 86, shadow_completed), (85, 87, shadow_armed_pending_close)]`.

### vpos 87 — open, same stop order, both probes

| | |
|---|---|
| DB | `open` · SL **64028.8** = `original_sl_price`, never moved · `recheck_status='done'` · `closed_at` NULL |
| probe 1 `fetch_positions` | LONG 0.0023 @ 64838.7, `2082799688088776706` |
| probe 2 raw `swapV2` | LONG `0.0023` @ `64838.7`, **same positionId** |
| probe 1 `fetch_open_orders` | **`2082799690256592896`** `STOP_MARKET @ 64028.8` |
| probe 2 raw `swapV2` | **same order id**, same stopPrice |
| DB `stop_order_id` | **`2082799690256592896` — UNCHANGED** |
| orphans | **0** |
| balance | `USDT free 480.18 · used 29.83 · total 510.00` |

### Mercury-SOL

**Active**, `NRestarts=0`, running since **2026-07-21 06:39:33**, **0** `.py` files modified today.

---

## WHAT I DID NOT DO

- **I did not change any code.** HEAD is still `54dc734`; this pass is data only.
- **I did not restart the service**, and said why: `_compute_shadow_pnl` runs only from `_close_shadow` (which early-returns on an already-finalised shadow) and `_maybe_compute_advantage` only from the two hooks — so no running code path could recompute or clobber the repaired fields, and none reads them for row 79.
- **I did not delete anything**, in any table.
- **I did not touch the real leg, the shadow-exit leg, the drift leg or the max-favourable watermark** — all 15 fields verified byte-identical afterwards.
- **I have not yet observed the 12h slot fire.** It is due 23:50:54 UTC. The structural proof is above; the observation is pending and will be reported separately rather than assumed here.

**Commits:** `831f9a1` (kola-reports — §2.28a corrections + new §2.28b audit trail). No titan-bot commit: there was no code to commit.
