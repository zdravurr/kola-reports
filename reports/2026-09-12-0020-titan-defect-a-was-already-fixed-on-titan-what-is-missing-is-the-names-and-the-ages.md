# titan-defect-a-was-already-fixed-on-titan-what-is-missing-is-the-names-and-the-ages

_2026-09-12 00:20 UTC_

---

# Titan — Defect A was already fixed on Titan on 2026-08-03. What is missing is the NAMES and the AGES. 🔴 NOT APPLIED: a LIVE position is open.

**2026-09-12 · 🔴 LIVE REAL MONEY · §1 and §3 READ-ONLY · 🔴 §2 NOT APPLIED — vpos 106 is OPEN · Mercury-SOL untouched** · marker `REPORT-ID titan-matrixnames-20260912`

Guard pre-flight: `titan-bot/tools/openitems_guard.py` **EXIT = 0** (14 watched values agree with runtime), and **EXIT = 0 again at 00:18** after this pass. `titan-bot` HEAD `cd0f175`, `git status` clean, and the six md5sums of `signal_tiers.py`, `claude_advisor.py`, `main.py`, `config.py`, `signal_matrix.py`, `state_machine.py` are identical at the end of this pass to their values at the start. **Nothing was written to either bot.**

---

## WHAT YOU NEED TO DECIDE

1. 🔴 **I did not apply §2, for two independent reasons — either alone is sufficient.**
   - **§2h: a LIVE position is open.** vpos 106, `BTC/USDT:USDT` SHORT, 0.0019 BTC filled at 77 014.2 on 2026-09-11 22:00:26 UTC, stop 78 301.6, water mark 76 936.5, still `status='open'` at 00:18 UTC (the hourly exit advisor consulted it at 00:00:51 and returned `close=False`). Your rule says apply from flat only. I stopped.
   - **§2i, and this is the bigger finding: the defect you measured on SOL does not exist in Titan's live prompt.** Titan's prompt has labelled every zeroed tier since 2026-07-29, and labelled it *correctly* since 2026-08-03. **142 of 142 (100%)** zeroed directional tier-instances in the current prompt form already carried "NOT counted by the gate". On SOL the number was 0 of 2,265.
2. **So the patch is not the SOL patch.** What Titan is missing is narrower: the **names** of the disagreeing signals and their **ages against the window**. It prints the points only — "LONG 2.50 / SHORT 2.25 across 3 signals" — and that one string covers two different worlds (a simultaneous opposite print in a 5-minute window, versus a leftover 60 of 90 minutes old).
3. **The patch is written, proved and contract-green, and is sitting in scratchpad, unapplied.** It touches **ONE file** — `signal_tiers.py`. `claude_advisor.py`, `main.py`, `config.py`, `signal_matrix.py` and `state_machine.py` need **zero** changes: Titan already passes `matrix_result` into the builder at both call sites, and the names and ages are already inside that same dict. It needs your word plus a flat moment.
4. **It is a legibility fix, not an edge.** Nothing here is ranked, and the outcome split is reported descriptively only. See the VERDICT's last bullet.

## VERDICT

- **The raw shape is common on Titan: 1,217 of 3,074 entry consultations (39.6%) showed the advisor a directional tier whose matrix category the score gate had ZEROED by intra-conflict, on 92 of 104 days.** So it is not a twice-in-a-lifetime shape. SOL's own figure was 2,265 of 4,598 (49.3%) on 92 of 92 days.
- 🔴 **But Titan's prompt already says so, and SOL's did not.** That is the whole difference between the two bots.
  - Era A+B, 2026-05-17 → 2026-07-29 02:35 (n = 2,766): **0 of 1,345** zeroed tier-instances labelled. This is SOL's defect exactly.
  - Era C, from 2026-07-29 13:45 (n = 308): **142 of 142 labelled (100%)**.
  - Of those 142, **63 carried the WRONG reason** ("matrix TTL expired") and they stop dead at 2026-08-03 06:40:08; the correct four-state reason starts at 2026-08-03 17:25:07 and covers **79 of 79** since. That is commit `6d9281d`, which measured the same error (wrong on 70 of 77) and fixed it — on Titan, thirteen months of measurement ahead of SOL.
- **It is not one-sided, and Titan's shape differs from SOL's.** 825 consultations (26.8%) showed a zeroed tier AGREEING with the proposed side (inflates); 535 (17.4%) showed one OPPOSING (deflates). Per tier, **the 5m trigger inflates** (631 agree / 95 oppose) and **the 15m mostly deflates** (297 / 450) — the same signs as SOL. The 1H barely participates at all (0 agree / 14 oppose, a 3–4% zeroed share), where SOL's 1H-rearm route carried 40%. **Titan's 15m-rearm route into the 1H slot reached a stored prompt exactly ONCE in 3,074 consultations**, against 452 of 1,652 on SOL.
- **It reached real money, and the prompt had already warned about it every single time.** All **21** live entries are era C. **9** carried a zeroed tier shown agreeing, and **all 9 were labelled in the prompt**. On all 9 the stored reason still builds its case on that tier — vpos 93's reason is "3TF SHORT agreement (1H/15m/5m)" sitting directly under the line saying the 5m was not counted. **The label did not change the narration.** That is the honest limit on what §2 can be expected to do.
- **The reverse, which Titan does NOT say: 19 consultations in the whole record (15 of them in the current form), every one on the 15m tier** — the slot prints "ABSENT — no 15m signal is held by the state machine" while the score gate was counting a direction in MOMENTUM. SOL measured 55. This is genuinely unlabelled on Titan and the patch covers it.
- 🔴 **NOT AN OUTCOME LEVER, and nothing here says it is.** Live: the 9 entries carrying a zeroed agreeing tier made ΣR **+0.045** over the 8 that closed; the 10 with no zeroed tier made **−3.353**; the 2 with an opposing one made **−1.524**. **8 against 10 against 2. NOT RANKED.** Paper: 24 closed with a zeroed agreeing tier made **−8.477**, 25 without made **+4.110** — the opposite sign to live, which is exactly why neither is ranked. §2 is worth applying because the prompt can say something true that it currently cannot, not because it pays.
- **§2 is written, AST-proved, contract 8/8 green as root AND as `botuser`, demonstrated on three real stored Titan prompts — and NOT APPLIED.**

---

## 1. DEFECT A — MEASURED ON TITAN'S OWN RECORD (read-only)

Method: `trades.db` opened `file:…?mode=ro`. `signal_matrix` was **never imported** — it calls `init_db()` at module scope (`signal_matrix.py:682`), which would `CREATE TABLE`/`ALTER` the live DB. `SIGNAL_DICTIONARY` (63 signals) and `CATEGORY_TTL_MINUTES` were extracted by `ast` from the source instead, and `classify()` reproduced literally.

### 1a. Titan's two code paths, verbatim, and every mechanism by which they disagree

**The matrix: every signal inside its category window counts, per signal TYPE.**
```
signal_matrix.py:257-287   record_signal(): ON CONFLICT(symbol, canonical_id) DO UPDATE — one row
                           per TYPE, last_seen bumped; a second alert never double-counts
signal_matrix.py:292-294
def _ttl_for(category):
    minutes = CATEGORY_TTL_MINUTES.get(category, 30)
    return timedelta(minutes=minutes)
signal_matrix.py:319-321   (inside get_active_signals)
        age = now - last
        if age > _ttl_for(cat):
            continue
signal_matrix.py:355-366   (compute_score)
    for sig in active:
        cat = sig['category']
        ...
        contribution = sig['intensity_weight'] * CATEGORY_MAX_POINTS
        if sig['direction'] == LONG:
            by_cat[cat]['long_points'] += contribution
        elif sig['direction'] == SHORT:
            by_cat[cat]['short_points'] += contribution
signal_matrix.py:377-381   🔴 THE ZEROING
        lp = min(data['long_points'], CATEGORY_MAX_POINTS)
        sp = min(data['short_points'], CATEGORY_MAX_POINTS)
        intra_conflict = lp > 0 and sp > 0
        if intra_conflict:
            net_dir = NEUTRAL
            contribution = 0.0
signal_matrix.py:415-421   inter-category: the MINORITY direction is zeroed too
                           (b['inter_conflict'] = True; b['contribution'] = 0.0)
config.py:531-536   CATEGORY_TTL_MINUTES = {'TREND': 360, 'MOMENTUM': 90,
                                            'LIQUIDITY': 30, 'EXECUTION': 5}
config.py:46        CATEGORY_MAX_POINTS = 2.5   (signal_matrix.py:46)
```

**The slot state machine: the LATEST write per slot, and that is what the advisor is shown.**
```
state_machine.py:34-53     1h_context ttl_hours=None (never expires) · 15m_confirm ttl_hours=4
                           · 5m_trigger ttl_hours=None (consumed each fire)
state_machine.py:206-222   update_slot(): OVERWRITES direction / signal_name / timestamp —
                           one value per slot, the older one is gone
            market_state[slot]['direction'] = direction
            market_state[slot]['signal_name'] = signal_name
            market_state[slot]['timestamp'] = now_iso
state_machine.py:225-234   _clear_lower_tfs_locked(): wipes 15m and 5m entirely
state_machine.py:259-274   set_1h_trend(): overwrites 1h_context; clears lower TFs only on a FLIP
main.py:4468               state_machine.set_1h_trend(direction, f'15m-rearm: {signal_name}')
main.py:2434 / main.py:4858  claude_advisor.consult_for_entry(..., matrix_result=matrix_result, ...)
claude_advisor.py:572-586  the tier block is built by signal_tiers.build(snapshot, matrix_result, …)
signal_tiers.py:58-59      _TIER_CATEGORY = {'1h_context': 'TREND', '15m_confirm': 'MOMENTUM',
                                             '5m_trigger': 'EXECUTION'}   <- STATIC map
signal_tiers.py:127-131    b = breakdown[cat]; nd = b.get('net_direction')
                           t['counted_by_gate'] = (nd not in (None, 'NEUTRAL'))
signal_tiers.py:163-198    _agreement(): counts the SLOTS, not the matrix  <- the tally
signal_tiers.py:269-274    render(): appends _not_counted_phrase(t) when counted_by_gate is False
```

**Why they can disagree — the four SOL mechanisms, each measured separately on Titan:**

| | mechanism | Titan's measurement |
|---|---|---|
| 1 | **Multiplicity.** The matrix keeps every signal TYPE inside the window; an older opposite-side type that has not expired zeroes the category, but the slot was overwritten by the newer signal and cannot show it. | **1,487 zeroed directional tier-instances** in 1,217 consultations (39.6%). The dominant mechanism on Titan, as on SOL. |
| 2 | **Different clocks.** The 1H slot never expires while TREND expires at 360 min; the 15m slot lasts 4 h while MOMENTUM lasts 90 min. The slot can show a direction the matrix holds nothing for. | **EMPTY**, tier-instances in the current form: 1H **103**, 15m **43**. Already labelled — `_not_counted_phrase`'s `ttl_expired` branch names the category and its TTL. |
| 3 | **Routing.** The 1H slot can be written by a re-armed 15m signal (`15m-rearm: …`), a MOMENTUM signal, while `_TIER_CATEGORY` judges the 1H tier against TREND unconditionally. | 🔴 **ONE tier-instance in 3,074 consultations.** This is SOL's big mechanism (452 of 1,652 stored 1H lines) and it is **effectively absent on Titan**. `signal_tiers.py`'s static map is therefore a latent mis-attribution, not an active one — named here so it is not mistaken for safe by construction. |
| 4 | **Reverse.** `_clear_lower_tfs_locked()` wipes the 15m slot on a 1H flip or Exit signal while the 90-min MOMENTUM window still holds a signal. The matrix counts a direction the prompt shows as absent. | **19** consultations in the whole record, **15** in the current form, **all on the 15m tier**. 🔴 **NOT labelled** — this is the one class Titan is silent about. |

A fifth, Titan-specific: **`AI_ADVISOR_HIDE_1H`** blanked the 1H direction and stripped `gate_direction` on **104** tier-instances between 2026-07-29 13:45 and 2026-08-05 16:40. It is **False** now (`config.py:792`), so that window is closed. It is counted separately above and never as a reverse.

### 1b. How often — every entry consultation in the record

**n = 3,074** entry consultations with a stored prompt, 2026-05-17 06:30:03 → 2026-09-11 22:00:11, **104 days**. All 3,074 carry `matrix_breakdown_json` from the same request. One further row (3,075 total) failed the prompt parse and is excluded and named: it carries a prompt in none of the three rendered forms. Exit consultations (`status='exit_ai_dryrun'`, 181 rows) are excluded throughout.

| class (per consultation) | n | share of 3,074 |
|---|---|---|
| ≥ 1 shown directional tier **ZEROED by intra-conflict** | **1,217** | **39.6%** |
| … of which a zeroed tier is shown **AGREEING** with the proposed side (inflates) | **825** | 26.8% |
| … of which a zeroed tier is shown **OPPOSING** the proposed side (deflates) | 535 | 17.4% |
| LONG consultations affected | 548 of 1,419 | 38.6% |
| SHORT consultations affected | 669 of 1,655 | 40.4% |
| distinct days affected | **92 of 104** | |
| zeroed shown tiers per affected consultation | 1: 947 · 2: 270 · 3: 0 | |

**Per era — this is the column SOL did not have:**

| era | prompt form | n | affected | agreeing | zeroed instances | **of those, labelled in the prompt** |
|---|---|---|---|---|---|---|
| **A** 2026-05-17 → 07-26 | three loose lines, `1H: NAME (direction: X)` | 2,715 | 1,082 (39.9%) | 736 | 1,313 | **0** |
| **B** 2026-07-27 → 07-29 02:35 | `1H trend set by: NAME, weight, set Xh ago` | 51 | 14 (27.5%) | 13 | 32 | **0** |
| **C1** 07-29 13:45 → 08-03 06:40 | SIGNAL TIERS block, one-sentence reason | 67 | 51 | 39 | 63 | **63, but the reason says "matrix TTL expired" — WRONG** |
| **C2** 08-03 17:25 → now | SIGNAL TIERS block, four-state reason | 221 | 70 (31.7%) | 37 | **79** | 🔴 **79 of 79 = 100%, correctly** |

**Per tier × side** (tier-instances; the denominator is consultations where that tier was shown with a direction):

| tier | side | zeroed & shown AGREEING | zeroed & shown OPPOSING | tier shown | zeroed share |
|---|---|---|---|---|---|
| 1H | LONG | 0 | 4 | 127 | 3.1% |
| 1H | SHORT | 0 | 10 | 248 | 4.0% |
| 15m | LONG | 151 | 207 | 1,339 | 26.7% |
| 15m | SHORT | 146 | 243 | 1,580 | 24.6% |
| 5m trigger | LONG | 272 | 44 | 1,419 | 22.3% |
| 5m trigger | SHORT | 359 | 51 | 1,654 | 24.8% |

### 1c. One-sided? No — and Titan's per-tier signs match SOL's

- **Both directions occur**: 825 inflating consultations against 535 deflating.
- **The 5m trigger inflates** — 631 agree against 95 oppose — for SOL's reason: the 5m is the signal that just fired, and the opposing one is another 5m print inside the same 5-minute `EXECUTION` window. On SOL: 904 against 7.
- **The 15m mostly deflates** — 297 agree against 450 oppose. On SOL: 592 against 1,001.
- **The 1H only deflates, and barely participates**: 0 agree, 14 oppose, a 3–4% zeroed share. On SOL the 1H split across a TREND route (5.9%/8.6%) and a 15m-rearm route (40.2%/36.1%); Titan has no meaningful rearm route (mechanism 3 above).

### 1d. How many became ENTRIES — live and paper NEVER pooled

**n = 80** executed entry consultations, every one with a stored prompt and a `virtual_positions` row. **21 LIVE** (`is_virtual = 0`, from 2026-07-30 00:50) and **59 PAPER** (to 2026-07-29 13:50). 🔴 **The live era and era C are the same era** — Titan went live three weeks *after* the labelled prompt shipped, so **no live Titan entry was ever shown an unlabelled zeroed tier.** On SOL, 11 of 16 live entries were. **Below n = 8 nothing is ranked.**

| book | class | n | closed & R known | ΣR | wins |
|---|---|---|---|---|---|
| **LIVE** | zeroed tier shown AGREEING | **9** | 8 (vpos 106 open) | **+0.045** | 3 |
| LIVE | zeroed tier shown OPPOSING only | 2 | 2 | −1.524 | 0 |
| LIVE | no zeroed tier shown | 10 | 10 | −3.353 | 3 |
| **PAPER** | zeroed tier shown AGREEING | **26** | 24 | **−8.477** | 7 |
| PAPER | zeroed tier shown OPPOSING only | 3 | 3 | +2.951 | — |
| PAPER | no zeroed tier shown | 30 | 25 | +4.110 | — |

🔴 Live and paper carry **opposite signs** on the same class. Neither is ranked; neither is evidence.

**LIVE entries with a zeroed tier shown agreeing — every one, named, and hand-read:**

| vpos | trades | date | side | R | zeroed tier(s) shown agreeing | opposing signals inside the window | labelled in the prompt? | reason builds on the tier? |
|---|---|---|---|---|---|---|---|---|
| 87 | 19713 | 07-30 12:05 | LONG | −0.440 | 15m HyperWave Signal Up | MOMENTUM LONG 1.75 / SHORT 2.50, 2 signals | yes — but **"matrix TTL expired"** (wrong) | **yes** — "15m/5m agree LONG" |
| 88 | 20006 | 07-31 09:35 | SHORT | −0.296 | 5m Within Bearish OB | EXECUTION LONG 1.75 / SHORT 1.75, 2 signals | yes — wrong reason | **yes** — "5m SHORT trigger fresh"; it quotes the 15m label and is silent on the 5m's own zeroing |
| 89 | 20054 | 07-31 12:20 | SHORT | **+1.386** | 5m Within Bearish OB | EXECUTION LONG 2.50 / SHORT 1.75, 3 signals | yes — wrong reason | **yes** — "15m+5m SHORT agreement" |
| 90 | 20100 | 07-31 14:25 | SHORT | −0.304 | 15m HyperWave Signal Down · 5m Within Bearish OB | both 1.75 / 1.75, 2 signals each | yes — wrong reason, both | **yes** — "15m+5m SHORT agree", on both zeroed tiers |
| 91 | 20920 | 08-03 06:40 | SHORT | −0.484 | 5m Bearish OB Created | EXECUTION LONG 2.50 / SHORT 2.50, **4 signals** | yes — wrong reason (the last row before `6d9281d`) | **yes** — "5m trigger fresh (0m)"; rubric called it ambiguous, the hand read does not |
| 93 | 22063 | 08-07 04:50 | SHORT | −0.137 | 5m Bearish I-CHOCH+ | **Bullish OB Entered 0 of 5 min · Within Bullish OB 0 of 5 min** | 🔴 yes — **correct four-state reason** | **yes** — "3TF SHORT agreement (1H/15m/5m)". **This is Titan's vpos 44.** |
| 94 | 25090 | 08-17 11:40 | LONG | **+0.865** | 5m Within Bullish OB | Within Bearish OB 0 of 5 min | yes — correct | **yes** — "1H+5m LONG agree"; it quotes the 15m label and is silent on the 5m's |
| 96 | 26750 | 08-24 12:45 | LONG | −0.546 | 5m Bullish I-BOS | Within Bearish OB 0 of 5 min (and 15m: HyperWave Up **60 of 90 min** vs Down 15) | yes — correct, both tiers | **yes** — "1H+5m LONG confluence" |
| **106** | 31759 | **09-11 22:00** | SHORT | 🔴 **OPEN** | 5m Bearish I-CHOCH+ | Bullish OB Entered 0 of 5 min | yes — correct | **yes** — "15m+1h+5m aligned SHORT" |

**The rubric, and the hand check.** The SOL rubric was applied to all 42 zeroed-agreeing tier-instances on entries: it flagged LIVE 9 of 10 as "LuxAlgo/confluence wording + names the TF" and 1 as ambiguous; PAPER 22 as the same, 6 as confluence-wording only, 2 as naming the shown signal, 2 as no mention. **Every one of the 35 entries was then read by hand.** LIVE: **9 of 9 build on the tier, 0 ambiguous, 0 no** — the rubric's one "ambiguous" (vpos 91) is a hand-confirmed yes. PAPER: the 26 reasons are dominated by OHLCV phrasing ("4H/1H/15m/5m all BEAR"), which is exactly the false-positive class SOL measured at 74% precision; 2 name the shown signal outright (vpos 53 "15m HyperWave DOWN + 5m Bearish OB", vpos 75 "LuxAlgo 15m/5m LONG signals coherent").

Per the 2026-08-08 canon, **`reason` is narration, not mechanism.** This shows what the model *says* it relied on, never what moved the verdict. 🔴 **And the Titan-specific conclusion it forces: the label was already there on all 9 live cases and the narration built on the tier anyway.** A fuller label is not shown to change that, and §2 must not be sold as if it would.

### 1e. The reverse, and the other disagreement classes

- **Reverse (slot ABSENT or NEUTRAL while the matrix scores a direction): 19 consultations** in the whole record, **15** in the current form, **every one on the 15m tier** — `_clear_lower_tfs_locked()` wiped the slot while MOMENTUM's 90-minute window still held the signal. 🔴 **Titan's prompt says nothing about it.** SOL measured 55, also all on the 15m.
- **EMPTY** (slot directional, the matrix's window for that category is empty), current form: 1H **103**, 15m **43** tier-instances. **Labelled** — "the matrix expired this signal on its category TTL (MOMENTUM TTL 90 min); the state-machine slot still holds it".
- **OPPOSITE** (the gate counted the other side, without zeroing): 1H **1** in the current form. Labelled by the existing `slot and matrix disagree` branch (`signal_tiers.py:271-274`).
- **ZEROED as the inter-category minority**: **0** directional tier-instances in the current form. Titan's inter-conflict branch has not fired on a shown tier.

### 1f. Effective n

| population | consultations | days | zeroed instances | episodes (tier, signal, day) | entries |
|---|---|---|---|---|---|
| all eras | 3,074 | 104 | 1,487 | 513 | 80 (21 live, 59 paper) |
| era A+B — SOL's defect, verbatim | 2,766 | 72 | 1,345 | 443 | 58 paper, **0 live** |
| era C — labelled | 308 | 33 | 142 | 70 | 21 live, 1 paper |
| era C2 — current form | 221 | 28 | 79 | 47 | 14 live |

**§2i's test.** You said: if this is rare on Titan — a handful — do not apply. It is **not** rare in raw occurrence (39.6%, 92 of 104 days). But the thing §2 was designed to add **already exists on Titan** on 100% of current-form cases. What is left is **79 instances over 28 days** where the label is right but mute about names and ages, plus **15** reverse cases it does not mention at all. That is above a handful and below a crisis. **Combined with the open position (§2h), I applied nothing and brought you the patch instead.**

---

## 2. THE FIX — WRITTEN, PROVED, AND NOT APPLIED

### 2a/2b. What it adds, and where Titan's own constants come from

Titan's labels, categories and TTLs are read from Titan's own files: `config.py:531-536` (`CATEGORY_TTL_MINUTES` = TREND 360 / MOMENTUM 90 / LIQUIDITY 30 / EXECUTION 5), `signal_matrix.py`'s 63-signal `SIGNAL_DICTIONARY` via the existing `signal_tiers._weight_of()` → `classify()`, and `signal_tiers._TIER_CATEGORY`. No SOL constant is carried over.

Per tier shown, the patch states:
- **ZEROED by intra-conflict** — unchanged points and count, **plus** every signal on each side inside the window, each with its age against that window. *New: the names and the ages.*
- **ZEROED as the inter-category minority** — the existing vague-but-true fallback, untouched.
- **COUNTED** — the existing rendering (the gate direction when it differs from the slot), untouched.
- **EMPTY / TTL-expired** — the existing branch naming the category and its TTL, untouched.
- **ABSENT while the gate counts a direction** — *new:* names the category, the direction, and the signal with its age.

🔴 **FACTS ONLY.** No instruction, no "therefore", no threshold, no lean, no outcome information. **Nothing computed changes** — not the score, not the cascade gate, not the score gate, not the book gate, not the slots, and **not the `Agreement:` sentence the phrase sits under**: that still counts the slots and is pinned byte-identical by contract case [4].

### 2c. Where the data lives — checked BEFORE writing the patch, and Titan's answer differs from SOL's

| | SOL (2026-09-11) | **Titan** |
|---|---|---|
| points + flags | `matrix_breakdown_json` | `matrix_breakdown_json` — same |
| names + ages | **not there** | **not there either** (`trade_signal_matrix.active_signals_json` exists but holds only **93** rows, written at entry time; 80 of the 3,074 consultations) |
| `matrix_result` reaching the builder | ❌ had to be added — `main.py` call changed to pass `matrix_result=matrix_result` | ✅ **already passed**, at BOTH call sites: `main.py:2434` and `main.py:4858` |
| `active_signals` reaching the builder | added with the above | ✅ **already inside the same dict**, forwarded to `signal_tiers.build(snapshot, matrix_result, …)` at `claude_advisor.py:573-575` — and simply never read |
| files the patch must touch | `claude_advisor.py` **and** `main.py` | 🔴 **`signal_tiers.py` only** |

**So Titan needed nothing that SOL needed.** One line — `active = (matrix_result or {}).get('active_signals') or []` — reads what was already in the room.

### 2d. Before / after on three real stored Titan prompts, verbatim

**vpos 93 · trades.id 22063 · 2026-08-07 04:50:05 · LIVE · −0.137R — Titan's vpos 44.**
```
===== BEFORE (the builder on disk now) =====
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  Trend Catcher Down  (SHORT, weight 1.0, last set 4.8h ago)
  15m: HyperWave Signal Down  (SHORT, weight 0.7, last set 80m ago)
  5m:  Bearish I-CHOCH+  (SHORT, weight 0.9, last set 0m ago, trigger-capable, NOT counted by the gate — this category's own signals disagree (LONG 2.50 / SHORT 2.25 across 3 signals), so it nets NEUTRAL)
  Agreement: 15m and 1H and 5m all point SHORT; vs the proposed SHORT: 15m+1H+5m agree.

===== AFTER (proposed) =====
SIGNAL TIERS — what fired, in which direction, how the bot weighted it,
and how long ago. IDENTITY ONLY: no win rate or past performance is implied.
  1H:  Trend Catcher Down  (SHORT, weight 1.0, last set 4.8h ago)
  15m: HyperWave Signal Down  (SHORT, weight 0.7, last set 80m ago)
  5m:  Bearish I-CHOCH+  (SHORT, weight 0.9, last set 0m ago, trigger-capable, NOT counted by the gate — this category's own signals disagree (LONG 2.50 / SHORT 2.25 across 3 signals), so it nets NEUTRAL — both sides are inside the EXECUTION 5-min window (LONG: Bullish OB Entered 0 of 5 min, Within Bullish OB 0 of 5 min; SHORT: Bearish I-CHOCH+ 0 of 5 min))
  Agreement: 15m and 1H and 5m all point SHORT; vs the proposed SHORT: 15m+1H+5m agree.

===== unified diff, whole block =====
--- before
+++ after
@@ -4,3 +4,3 @@
   15m: HyperWave Signal Down  (SHORT, weight 0.7, last set 80m ago)
-  5m:  Bearish I-CHOCH+  (SHORT, weight 0.9, last set 0m ago, trigger-capable, NOT counted by the gate — this category's own signals disagree (LONG 2.50 / SHORT 2.25 across 3 signals), so it nets NEUTRAL)
+  5m:  Bearish I-CHOCH+  (SHORT, weight 0.9, last set 0m ago, trigger-capable, NOT counted by the gate — this category's own signals disagree (LONG 2.50 / SHORT 2.25 across 3 signals), so it nets NEUTRAL — both sides are inside the EXECUTION 5-min window (LONG: Bullish OB Entered 0 of 5 min, Within Bullish OB 0 of 5 min; SHORT: Bearish I-CHOCH+ 0 of 5 min))
   Agreement: 15m and 1H and 5m all point SHORT; vs the proposed SHORT: 15m+1H+5m agree.

  [contract] AFTER with no active_signals == BEFORE, byte for byte: True  (576 chars)
  stored reason: "3TF SHORT agreement (1H/15m/5m); 4H/1H/15m/5m all BEAR-aligned. … 1D BULL opposes but is weak signal; lower TFs dominate. Execute."
```
🔴 **What the new clause says that the old one could not.** The opposing side is **two order-block signals that fired in the same minute as the trigger** — not a leftover. "LONG 2.50 / SHORT 2.25 across 3 signals" cannot express that, and the model wrote "3TF SHORT agreement" under it.

**vpos 96 · trades.id 26750 · 2026-08-24 12:45:11 · LIVE · −0.546R — the opposite world, same old string.**
```
-  15m: HyperWave OB Signal Down  (SHORT, weight 1.0, last set 15m ago, NOT counted by the gate — this category's own signals disagree (LONG 1.75 / SHORT 2.50 across 3 signals), so it nets NEUTRAL)
-  5m:  Bullish I-BOS  (LONG, weight 0.7, last set 0m ago, trigger-capable, NOT counted by the gate — this category's own signals disagree (LONG 1.75 / SHORT 1.75 across 2 signals), so it nets NEUTRAL)
+  15m: HyperWave OB Signal Down  (SHORT, weight 1.0, last set 15m ago, NOT counted by the gate — this category's own signals disagree (LONG 1.75 / SHORT 2.50 across 3 signals), so it nets NEUTRAL — both sides are inside the MOMENTUM 90-min window (LONG: HyperWave Signal Up 60 of 90 min; SHORT: HyperWave OB Signal Down 15 of 90 min, Reversal Down + 30 of 90 min))
+  5m:  Bullish I-BOS  (LONG, weight 0.7, last set 0m ago, trigger-capable, NOT counted by the gate — this category's own signals disagree (LONG 1.75 / SHORT 1.75 across 2 signals), so it nets NEUTRAL — both sides are inside the EXECUTION 5-min window (LONG: Bullish I-BOS 0 of 5 min; SHORT: Within Bearish OB 0 of 5 min))
```
Here the 15m's opposing LONG is **60 of 90 minutes old** — two thirds through its window — while the 5m's is simultaneous. The old rendering gave both the same shape.

**trades.id 26338 · 2026-08-23 04:00:08 · skip — the REVERSE, which Titan currently does not say at all.**
```
-  15m: ABSENT — no 15m signal is held by the state machine at this moment
+  15m: ABSENT — no 15m signal is held by the state machine at this moment — but the score gate counted MOMENTUM LONG for this tier, from a signal the slot no longer holds — it is inside the MOMENTUM 90-min window (LONG: HyperWave Signal Up 66 of 90 min)
```
(The stored `MOMENTUM` breakdown on that row is `net_direction: LONG, contribution 1.75, signal_count 1`; the name and age are what the live call has in hand and the skip row does not persist, so they are reconstructed here consistently with that breakdown and labelled as such.)

**vpos 106** — the currently open position — renders `… nets NEUTRAL — both sides are inside the EXECUTION 5-min window (LONG: Bullish OB Entered 0 of 5 min; SHORT: Bearish I-CHOCH+ 0 of 5 min, Bearish OB Created 0 of 5 min)`. It is shown in the scratchpad output and is **not** a reason to apply anything to a bot holding a position.

### 2e. Malformed or absent input renders nothing — pinned

**Contract `tests/test_entry_tiers_matrix_names_ages.py`** (new; Titan has no `tests/` directory today — SOL's `mercury-sol/tests/` holds exactly its two prompt contracts, and Titan would need the same directory created). Run with bytecode writing off, no DB, no network, no clock beyond the `now` passed in. **8 of 8 green as `root` AND as `sudo -u botuser`** (titan's unit runs `User=root`, so the 2026-08-27 botuser rule does not bind this contract — it reads no crontab — but it was run both ways anyway):
```
  [0] absent/malformed matrix_result: byte-identical to the pre-change builder and raises in exactly the same places: True
  [1] matrix_result WITH a breakdown but no active_signals == pre-change builder, byte for byte: True  (715 chars)
  [2] rendered phrase exact: True
  [3] block minus the one phrase == the no-names block: True
  [4] Agreement sentence untouched (still counts the slots): True  Agreement: 15m and 1H and 5m all point SHORT; vs the proposed SHORT: 15m+1H+5m agree.
  [5] reverse case rendered: True
  [5b] reverse still names the gate direction without active_signals, and the names/ages clause is absent: True
  [6] malformed active_signals: no exception, no clause, byte-identical: True
  [7] the EXIT advisor's entry-thesis block carries it too: True
OK — the zeroed tier now names each side with its age against the window; the Agreement sentence and every no-data rendering are byte-identical
```

🔴 **Three things the contract caught in my own patch, stated because they are the reason it exists.**
1. The reverse branch never fired: I keyed it on `counted_by_gate is None`, but `build()` has already set that flag **True** whenever the matrix holds a direction. Rewritten to key on the absent slot plus a directional category.
2. `_sides_in_window` **raised** on a non-list (`'nonsense'` iterates to characters) and on a dict (iterates to keys). Now it returns `{}` unless given a list of dicts.
3. "**both sides** are inside the window" was printed for the reverse case, which usually has **one** side. Now "it is" when only one side is present.

🔴 **And one honest scope limit, which is NOT what §2e asked for and must not be read as if it were.** The names/ages clause is gated on `active_signals` and vanishes without it — byte-identical, case [1]. **The reverse clause is gated on the `breakdown`, which every live row carries, so it is a genuine new line whenever that shape occurs** (15 times in 221 current-form consultations), not a no-op. Case [5b] pins that without `active_signals` it states the direction and omits the names and ages. Case [0] pins the thing §2e actually demanded: with **no** `matrix_result`, or a malformed one, the whole block is byte-identical to the builder on disk.

**A pre-existing defect found and deliberately NOT fixed:** `signal_tiers.build()`'s docstring says "Never raises", and it already raises `AttributeError` on a truthy non-dict `matrix_result` (e.g. the string `'nonsense'`) — `(matrix_result or {}).get(...)`. My patch neither introduces nor repairs it; contract case [0] asserts **parity**, not repair. Both live call sites pass `signal_matrix.compute_score()`'s dict, so it cannot occur in production. Flagged for your decision, not silently patched.

### 2f. ONLY the prompt builder changed — AST proof

```
signal_tiers.py  sha256 ac32ba1227285576 -> d7d6f33bc29cfb96
  top-level named nodes ADDED   : ['_gate_holds_phrase', '_sides_in_window', '_sides_phrase']
  top-level named nodes REMOVED : []
  text diff: +142 lines, -2 lines
  removed lines: ['                f"({pts}{cnt}), so it nets NEUTRAL")',
                  '                         f"state machine at this moment")']
  after stripping ONLY the change: AST identical to the file on disk = True
  removed counts: {'helper': 3, 'stmt': 1, 'assign': 2, 'call': 2}  (expected helper=3 assign=2 stmt=1 call=2)
AST PROOF PASS
```
🔴 **`claude_advisor.py`, `main.py`, `config.py`, `signal_matrix.py` and `state_machine.py` are not in the patch at all** — zero bytes, zero AST nodes. There is no call-site change on Titan.

**The four advisor SYSTEM prompts, sha256, untouched by construction (the patch does not open `claude_advisor.py`):**
```
  _ENTRY_SYSTEM        1871 chars  30c979595a4831aa751db8bd64d7bcb47e9af63088ae665489b4fe3bd5f573f2
  _LEARNING_SYSTEM      730 chars  191cf5d71ebf3865535f8e0bfb09106a7d6c758bca8566e70e5fc4309f7138c2
  _CLOSE_SYSTEM         452 chars  7d7707cfa2d336f75f690eba53114fedb56b790222ecf681ec467211a901b545
  _CLOSE_SYSTEM_RICH    252 chars  3d709571e17ff4051362c5a50496c74c0223b29a062eb2c94b2a5de09655670b
  claude_advisor.py whole file     ca14e959a5c6104c8438ddc493750d4193a0a32bfab49312b30eff2eb1a8c6c6
```

**Confirmed untouched AT RUNTIME.** Every value below was read out of `config.py` and each module's `.pyc` **header was verified against its source `mtime` and `size`**, so these are the bytes the running worker (master PID 961100, up since 2026-09-10 14:36:19) imported:

| value | config.py | reading |
|---|---|---|
| `SL_ATR_MULT` | :193 | **2.25** |
| `TRAIL_MULT_ATR` | :249 | **1.6875** |
| `EMA_ENVELOPE_GATE_ENABLED` / `_TFS` / `_REQUIRED_DIR` / `_FAIL_OPEN` | :667-670 | **True** / `('1h','15m')` / `Expanding` / **True** |
| `LONG_PARTIAL_ENABLED` | :308 | **False** |
| `CONFLUENCE_SCORE_THRESHOLD` | :492 | **3.0** |
| `EXIT_ADVISOR_DRYRUN` | :335 | **False** |
| `BOOK_GATE_ENABLED` | :1071 | **True** |
| 🔴 `BOOK_GATE_DRYRUN` | :1072 | **False** |
| `BOOK_GATE_CLAUSE_A_ENABLED` | :1077 | **True** |
| 🔴 `BOOK_GATE_CLAUSE_B_ENABLED` | :1078 | **False** |
| `LIVE_TRADING_ENABLED` | :17 | **True** |
| position size | :132, :144, :145 | `LEVERAGE` **5**, `LIVE_FIXED_MARGIN_USDT` **30.0**, `PAPER_FIXED_MARGIN_USDT` **2000.0** |
| `CATEGORY_TTL_MINUTES` | :531 | TREND 360 · MOMENTUM 90 · LIQUIDITY 30 · EXECUTION 5 |
| `AI_ADVISOR_HIDE_1H` | :792 | **False** |

```
  config         pyc 2026-09-10 14:34:54  header == source: True  sha 1dc387744a976d54
  signal_tiers   pyc 2026-08-04 15:07:11  header == source: True  sha ac32ba1227285576
  claude_advisor pyc 2026-08-31 15:10:04  header == source: True  sha ca14e959a5c6104c
  main           pyc 2026-09-09 20:46:02  header == source: True  sha 00c8be297a8de922
  signal_matrix  pyc 2026-08-05 22:47:31  header == source: True  sha 0e4128911c283b2f
  state_machine  pyc 2026-08-21 19:44:21  header == source: True  sha 7f5a21ea88662453
```
`signal_tiers.py`'s loaded sha (`ac32ba1227285576`) is **exactly** the sandbox BEFORE baseline, so the diff above is a diff against the running code, not against some older copy.

### 2g. 🔴 NOT APPLIED — a LIVE position is open

```
vpos 106 · BTC/USDT:USDT · SHORT (sell) · is_virtual = 0  (LIVE REAL MONEY)
  opened   2026-09-11T22:00:26.333335+00:00   trades_entry_row_id 31759
  fill     77 014.2   size 0.0019   margin $30.00   atr 85.77   trail 1.254%
  stop     78 301.6 (original)      water_mark 76 936.5
  status   open      closed_at None      close_reason None
  journal  22:00:26 [ADAPTER] LIVE ENTRY BTC/USDT:USDT SHORT 0.0019 @ 77014.2 fee=0.073163
           22:00:26 VIRTUAL ENTRY vpos=106 SHORT amount=0.0019 @ 77014.2 sl=78301.6
           00:00:51 [EXIT-ADVISOR-LIVE] trigger=hourly SHORT close=False conf=0.72
  re-checked 00:18 UTC: still status='open'
```
Your §2h is unambiguous: **apply from flat only.** No `.bak` was written, no file was replaced, no `systemctl restart` was issued, and no boot line is quoted because there was no boot. `NRestarts = 0`, MainPID **961100** unchanged since 2026-09-10 14:36:19. `openitems_guard` **EXIT = 0** before and after.

**The patch, the contract, the AST proof and the before/after are in scratchpad:**
`/tmp/claude-0/-root/e5554ab2-1696-47ea-88db-b0cb8955b7f1/scratchpad/sbx/` — `signal_tiers.py` (patched), `signal_tiers_BEFORE.py` (byte-copy of the live file), `test_entry_tiers_matrix_names_ages.py`, `astproof.py`, `demo.py`, `demo_out.txt`. Measurement: `scratchpad/m/` — `dict.py`, `measure.py`, `stats.py`, `eraC.py`, `entries.py`, `rubric.py`, `final.py`, `res.json`, `entries.json`, `rubric.json`.

**To apply, when you say so and the book is flat:** copy `signal_tiers.py` over `/root/titan-bot/signal_tiers.py` after writing `signal_tiers.py.bak_matrixnames_<ts>`, create `/root/titan-bot/tests/` and drop the contract in, verify open positions = 0 on both the DB and the venue, restart, read the boot line and the `.pyc` header back, and run `openitems_guard`. Rollback is the one `.bak` plus a restart from flat.

---

## 3. RECORD

### 3a. For Titan's canon, beside `§0.PROMPT-PAIRING`

The entry below is **proposed, not written** — `OPEN-ITEMS.md` is the guard's canon and this pass changed no Titan state, so adding a current-state line for a patch that is not applied would make the canon disagree with runtime. It goes in when §2 goes in.

> **§0.MATRIX-TIER-NAMES — what the score gate counted, named and aged. PROPOSED 2026-09-12, NOT APPLIED (vpos 106 open).**
> The prompt shows the state-machine SLOTS, which keep only the latest signal per slot. The score gate counts EVERY signal still inside its `CATEGORY_TTL_MINUTES` window and **zeroes** a category holding both a LONG and a SHORT (`signal_matrix.py:377-381`).
> **Measured 2026-09-12 over every stored Titan entry consultation: 1,217 of 3,074 (39.6%) showed a directional tier whose category the gate had zeroed, on 92 of 104 days; 825 (26.8%) showed it AGREEING with the proposed side.** SOL's own figure, measured 2026-09-11: **2,265 of 4,598 (49.3%) on 92 of 92 days; 1,453 (31.6%) agreeing.**
> 🔴 **Titan is NOT SOL on this.** `signal_tiers.py` has labelled the zeroing since 2026-07-29 (`§2.8`) and labelled it correctly since 2026-08-03 (`6d9281d`, which measured the old one-sentence reason wrong on 70 of 77). **142 of 142 (100%)** zeroed tier-instances in the current prompt form already carry "NOT counted by the gate"; all 21 live entries fall inside that era, so **no live Titan entry was ever shown an unlabelled zeroed tier.** SOL had 11 of 16 live entries in exactly that state.
> **What is still missing, and all the proposed patch adds:** the **names** of the disagreeing signals and their **ages against the window** (the points alone cannot separate a simultaneous 5-minute print from a 60-of-90-minute leftover), and the **reverse** — 19 consultations in the record, 15 in the current form, all on the 15m, where the slot reads ABSENT while the gate counted a direction.
> 🔴 **THIS IS LEGIBILITY, NOT A MEASURED EDGE.** Live: 9 entries with a zeroed agreeing tier made ΣR **+0.045** over 8 closes, the 10 without made **−3.353**, the 2 opposing made **−1.524**. Paper carries the **opposite** sign (**−8.477** over 24 against **+4.110** over 25). 8 vs 10 vs 2, and two books disagreeing: **NOT RANKED, and no later pass may cite these cells as an effect.** And the label was already present on all 9 live cases while the reason built on the tier anyway — a fuller label is not shown to change the narration.
> Nothing computed changes: not the score, not the cascade / score / book / risk gates, not the slots, and not the `Agreement:` sentence, which still counts the slots. Scope: `signal_tiers.py` alone — `matrix_result` already reaches the builder at `main.py:2434` and `main.py:4858`, and `active_signals` is already inside it.
> Record: `reports/2026-09-12-0020-titan-defect-a-was-already-fixed-on-titan-what-is-missing-is-the-names-and-the-ages.md`

### 3b. The two counters, so neither is disturbed

**Book-gate review counter — 22 of 200 gate evaluations, 0 refusals, all time.**

| era | rows | LONG | SHORT | window |
|---|---|---|---|---|
| DRYRUN, before the 2026-09-10 14:36:20 arming boundary | **15** | 13 | 2 | 2026-09-08 04:15:15 → 2026-09-10 13:55:09 |
| LIVE, after it | **7** | 5 | 2 | 2026-09-11 11:10:08 → 2026-09-11 22:00:11 |
| | **22 of 200** | 18 | 4 | |

`status='book_blocked'` rows, all time: **0**. Latest gate row: trades 31760, 2026-09-11 22:00:11, `open_short`, `ai_skipped`. The canon's `§0.BOOK-GATE-ARMING` records **15/200** at the boundary; the **7 LIVE rows that have landed since** bring the live reading to 22/200, and per canon the two eras are **never pooled** and the counter is **not reset**. 🔴 `BOOK_GATE_DRYRUN` stays **False**; `BOOK_GATE_CLAUSE_B_ENABLED` stays **False**. Neither was read by, written by, or reachable from anything in this pass.

**Exit-advisor rule counter (`§0.EXIT-ADVISOR-RULE`) — 3 observed, 2 RESOLVED of 10, Σ over the resolved two +1.5237R / +$2.00 in the advisor's favour.** LIVE `ai_exit` closes from vpos 101 onward, read from `virtual_positions`:

| vpos | side | closed | advisor R |
|---|---|---|---|
| 101 | SHORT | 2026-09-01 18:00:19 | +0.2956 |
| 104 | LONG | 2026-09-09 08:30:21 | +0.5757 |
| 105 | SHORT | 2026-09-09 23:46:03 | −0.0136 — 🔴 counterfactual **still UNRESOLVED in canon** |

No new `ai_exit` close has landed: vpos 102 and 103 closed on `sl`, and **vpos 106 is open**. This pass did **not** advance vpos 105's counterfactual — that needs a BingX 1m replay and was not in scope; whoever reports next still owes it, per the canon's own instruction. `EXIT_ADVISOR_DRYRUN` stays **False**. The stopping rule fires at 10 closes and nothing here moves the count.

### 3c. Mercury-SOL untouched — proved, not asserted

```
service   mercury-sol active · MainPID 1341949 · NRestarts 0
          ActiveEnterTimestamp Fri 2026-09-11 18:26:59 UTC  <- the 18:56 report's own restart, unchanged
files     no .py modified: `find mercury-sol -maxdepth 1 -name '*.py' -newermt '2026-09-11 23:55'` -> EMPTY
          the only files newer than this session's start are the bot's OWN runtime writes:
            oi_cache.json · trades.db · optimizer/tg_offset.txt
advisor   claude_advisor.py  mtime 2026-09-11 18:24:18  size 84462
          sha256 bff44d00fd0e0aa0b928387184c11e0feca5c1e6b677f28cceead6e3eb831696
          == EXACTLY the sha the 2026-09-11 18:56 report recorded after its own patch
loaded    claude_advisor pyc 18:27:04  header == source: True  sha bff44d00fd0e0aa0
          main           pyc 18:27:00  header == source: True  sha 91dfa43f251c6245
          config         pyc 05:40:10  header == source: True  sha a308a130e4dde9f6
its line  `_render_matrix_tier_line` present in source: True
          call site `_render_matrix_tier_line(_shown, matrix_result)` present: True  -> still loaded
```
SOL's `claude_advisor.py` was read **as text only** (`sed -n`, `grep`), for the patch shape. **No write, no import, no restart, no venue call on its key.** Its `signal_matrix.py` was never touched; the dictionary used in §1 came from **Titan's** source by AST.

---

## CONTROLS

| | |
|---|---|
| guard | `openitems_guard.py` **EXIT = 0** at 00:01 and again at 00:18; 14 watched values agree with runtime |
| Titan HEAD | `cd0f175`, `git status -- titan-bot` **clean** before and after |
| Titan md5, start == end | `signal_tiers.py` 0af70f87… · `claude_advisor.py` 5026f931… · `main.py` c70044f2… · `config.py` fc14c6d2… · `signal_matrix.py` f677c1d2… · `state_machine.py` b5220b52… |
| Titan restarts | **none.** MainPID 961100 since 2026-09-10 14:36:19, `NRestarts = 0` |
| DB access | `file:/root/titan-bot/trades.db?mode=ro` throughout. `signal_matrix` **never imported** (its module-scope `init_db()` writes) |
| n | 3,074 entry consultations · 104 days · 80 executed (21 live / 59 paper) · 1 prompt excluded and named |
| contract | 8/8 green as `root` **and** as `sudo -u botuser`; 3 bugs in my own patch caught and fixed by it |
| AST proof | PASS — `signal_tiers.py` only; 3 helpers, 1 dict key, 1 if-block, 2 call terms; nothing else differs |
| applied? | 🔴 **NO.** vpos 106 LIVE SHORT open. Awaiting your word plus a flat book. |
