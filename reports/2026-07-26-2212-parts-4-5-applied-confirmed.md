# parts-4-5-applied-confirmed

_2026-07-26 22:12 UTC_

---

# TITAN — Parts 4 + 5 APPLIED, live, confirmed

**2026-07-26 22:07 UTC · APPLIED.** Commit `ef7fa10`, tree clean, `titan.service` healthy.
15m entry confirmations now persist · exit advisor wired in **DRYRUN**. Paper mode.

---

## Pre-flight answers (asked before applying)

### 2. Hourly state storage — SAFE on all three counts, no dedicated column needed
```
(a) mgmt_state IS the parsed column:   virtual_trader.py:1547
        mgmt_state = json.loads(row['pending_dca_limits'] or '{}')
(b) unknown keys cannot corrupt DCA:   the ONLY key ever read is 'breakeven_applied'
        (lines 1550, 1667). grep over the whole tree: pending_dca_limits appears in
        virtual_trader.py ONLY — the code itself calls it "the now-dead
        pending_dca_limits column" reused for management state. There is no DCA
        reader left to corrupt.
(c) malformed/missing degrades safely: except (ValueError, TypeError) -> mgmt_state = {}
        -> mgmt_state.get('exit_advisor_last_ts') is None -> the hook treats None as
        "consult now". No crash path.
```

### 4. `exit_ai_dryrun` rows cannot be miscounted — every consumer excludes them
```
cycle_count()            reads virtual_positions, not trades
optimizer.py:79          status='executed'
signal_weights.py:292    status='executed' AND combo_key IS NOT NULL   (ours has neither)
virtual_trader.py:345    is_virtual=1 AND status='executed'
skip_attribution.py:54   TRACKED_STATUSES = ('ai_skipped','below_threshold','htf_blocked')  allow-list
every sensor .sh         explicit status IN (...) lists, e.g. bull_regime_watch:
                         status IN ('htf_blocked','ai_skipped','below_threshold','executed')
post_exit_observatory    the two LIKE/NOT-IN queries are on its OWN table, not trades
```
No wildcard reader exists. ~24 rows/day land in a status nothing else looks at.

### 3. The lazy `import main` resolves at runtime — **proved on a real poller cycle**
```
22:06:08  virtual_trader worker started
22:06:12  [EXIT-ADVISOR-DRYRUN] trigger=hourly BTC/USDT:USDT LONG close=False conf=0.72
          | "Position +1.17R with intact trend structure. Entry thesis (1H bullish,
            15m/5m confluence) remains valid; no regime flip confirmed. Supporting wall
            thinned (31st pct) but opposing wall at 99th pct extr…"
```
Four seconds after boot, on the live open position. No circular-import error anywhere in the log.

### 1. Consult on the ARMED exit — added, record-only
Placed immediately before `_execute_close_position` in `_execute_armed_exit`. AST on the **live**
file:
```
_execute_armed_exit:  consult at line 2655 · close at line 2661
  close AFTER consult                    : True
  close depends on the verdict           : False   (0 verdict-dependent branches)
```
The consult is wrapped in its own `try/except` whose handler prints and continues, so an API error,
a timeout or a bad context cannot propagate into the close. **It cannot alter the close and delays
it only by the call itself.** Rare by construction — 5 armed exits in 65 days.

---

## The six confirmations

### 5. Only the four files changed
```
M titan-bot/claude_advisor.py   M titan-bot/config.py
M titan-bot/main.py             M titan-bot/virtual_trader.py
4 files changed, 362 insertions(+), 5 deletions(-)
```

### 6. DRYRUN blocks every close path — AST-verified on the live file
```
_handle_5m_close_via_ai:  consult 2422 · DRYRUN return 2434 · close 2472
      every close mechanic AFTER the return: True
_execute_armed_exit:      consult 2655 · close 2661, unconditional by design (see §1)
```
`consult_exit_advisor` has no close mechanic in scope at all.

### 7. Everything protected is intact
```
recheck clamps (93c20c3)  : 2 present     LONG partial (f7df202) : present
LONG_PARTIAL_ENABLED=True   CONFLUENCE_FLAT_THRESHOLD=5.0   HTF_CASCADE_ENABLED=True
WALL_TRAIL_LIVE_ENABLED=False   ADX_BELOW_FLOOR=20.0   AI_ADVISOR_HIDE_1H=True

diff lines touching the router / _TF_TO_ACTION / gates : 0
diff lines touching sl_price / _tighten_sl / breakeven / trail : 0
mercury-sol/main.py mtime 2026-07-02 21:36 — untouched
```

### 8. First rows
**Hourly consultation — CONFIRMED, within 4 seconds of boot:**
```sql
SELECT id, timestamp, signal_type, status, ai_decision, ai_confidence FROM trades
WHERE signal_type='exit_ai_dryrun';
18773 | 2026-07-26 22:06:11 | exit_ai_dryrun | exit_ai_dryrun | hold | 0.72
```
Full payload and 400-char reason persisted exactly as on the entry side.

**First `15m_confirm` row — PENDING at time of writing.** The 15m entry stream arrives ~26/day
(roughly one an hour) and the last 15m alert of any kind was 21:45, before the restart. The write is
in place and dry-run-verified; it simply has not had an alert yet. Check with:
```sql
SELECT id, timestamp, tv_action, status FROM trades WHERE signal_type='15m_confirm';
```
I am reporting this as **not yet observed** rather than assumed.

---

## One defect found and fixed during the apply

The first boot logged:
```
[EXIT-ADVISOR] context build partial: name 'EXIT_ADVISOR_5M_CONTEXT_MIN' is not defined
```
`EXIT_ADVISOR_5M_CONTEXT_MIN` was declared in `config.py` but omitted from `main.py`'s config import.
The try/except caught it and the consultation still completed — the **5m structure field rendered
`n/a`** in that one prompt (row 18773 shows it). Import added, service restarted, no such line on the
new boot. The next consultation carries the field. Reporting it because the first stored prompt is
degraded and anyone reading row 18773 should know why.

---

## Rollback
```bash
git checkout pre-signal-inventory-20260726 -- titan-bot/{config,claude_advisor,main,virtual_trader}.py
# or: cp *.bak_s6_20260726 back    # or: git revert ef7fa10
# or, no code edit:  EXIT_ADVISOR_HOURLY = False and EXIT_ADVISOR_ON_15M_CONFIRM = False
sudo systemctl restart titan.service
```
`EXIT_ADVISOR_DRYRUN` stays `True`. Nothing may set it False until the activation criterion in
`OPEN-ITEMS.md` §6 is met.

---

## OPEN-ITEMS additions
* **§6** (commit `900901e`) — activation criterion, recorded before any verdict existed.
* **§7** (commit `174f490`) — the ENTRY advisor cannot see the 1H signal identity
  (`AI_ADVISOR_HIDE_1H = True`): `Bearish C.+` (n=4, +1063) and `Trend C. Up`
  (n=6, -68) both reach it as "1h BULL". Candidate change described, **deliberately out of scope**
  — it modifies the entry path, and the per-signal n (largest cell 6) cannot calibrate it yet.

---

Session commits: `93c20c3` · `b878535` · `f7df202` · **`ef7fa10`**. Tree clean, service healthy,
Mercury-SOL untouched.
