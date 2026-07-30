# titan-adx-window-fix-written-verified-not-applied-diff-inline

_2026-07-30 13:51 UTC_

---

# TITAN — the ADX window defect: FIX WRITTEN AND VERIFIED, **NOT APPLIED**. Diff inline.

_2026-07-30 13:45 UTC · HEAD `81875c9` · 🔴 LIVE, REAL MONEY · vpos 87 LONG open_

---

## DECISION LINE

**The fix is written, compiled, symtable-audited, unit-tested against a truth table and smoke-tested
against the live exchange. It is NOT applied.** `/root/titan-bot` is byte-identical to HEAD `81875c9`
(`git status` clean, md5 match on every touched file) and `titan.service` still runs the old code.
You said show the diff, then stop, and item 3 says state the behaviour change *before it ships* — so
the patch lives in a scratch tree and nothing on the live path has changed. **4 files, +404 / −40.**

**The behaviour change, quantified, which is the number you actually asked for:**

> **9 of 36 OK verdicts (25%) become TIGHTEN.** Zero become EMERGENCY_CLOSE. Zero TIGHTENs become OK.
> The 9 are **three positions, all LONG, all with a true ADX1h under the floor** — vpos 82 (16.88),
> vpos 85 (16.81), vpos 87 (13.83), three tiers each.

**So: no, we are not turning on a rule that fires constantly.** 25% of tier runs, 3 of 14 positions.
And what those 9 TIGHTENs actually *do* is the part that matters most: **nothing, on the exchange.**
The recheck only runs pre-breakeven, where the `93c20c3` bound forces `new_sl == current_sl`, so all
nine are **no-op TIGHTENs** — advisory logged, `t+{tier}_ok` written, later tiers stay due, stop
untouched. In practice the fix converts **9 silent OKs into 9 honest advisories and moves no money**.
It also finally **exercises the §2.20 branch that has never run** — exactly as you predicted.

**Your ATR warning was the right one to give, and it was load-bearing.** `entry_atr_pct_1h` is derived
from `execute_entry`'s own `ATR_LEN*3` 1h fetch, so moving ATR to the converged window would have
broken `atr_contraction` by changing **one side** of its comparison. ATR is untouched everywhere;
both patched functions now make **two fetches on purpose**. Verified live on all three timeframes:
**ATR% byte-identical, `trend` identical, only `adx` moves.**

---

## 🔴 ONE THING I DID THAT I DID NOT INTEND — DISCLOSED, ASSESSED, NO HARM

**Importing the patched `virtual_trader` for the guard test ran its module-scope `init_db()` (line
2641) against the LIVE `trades.db`.** Two additive nullable columns now exist on the live database
that I did not mean to create yet:

```
virtual_positions.entry_adx_1h_window   INTEGER   (col 41)
smart_exit_dryrun_samples.adx_window    INTEGER   (col 49)
```

`recheck_events.adx_window` was **not** created (`sensor_events.init_db()` is not called on import).

**Assessment, checked rather than assumed:**

| check | result |
|---|---|
| `ALTER TABLE ... ADD COLUMN <name> INTEGER` | additive, nullable, no default — SQLite metadata-only; **no existing row modified, nothing lost** |
| every INSERT into those two tables | names its columns explicitly (`virtual_trader.py:895`, `:2027`) — unaffected |
| positional row access (`row[<int>]`) on either table | **none** — the only positional reads are on unrelated explicit-column queries and order-book lists |
| `titan.service` | **active**, `NRestarts=0`, up since 11:32:45 |
| errors / tracebacks / `no such column` since the import | **0** |
| vpos 87 (open, real money) | reads normally; new column NULL |
| the sampler kept writing | row 245 at 13:05:31, `adx_1h=22.3`, `adx_window` NULL — as expected from the old code |

**No harm, and the running bot cannot see a difference.** But it was not authorised and I am recording
it rather than letting you find it: a module whose *import* migrates the production schema is a
landmine for exactly this kind of read-only work, and I walked into it. If you want them gone before
the patch lands, dropping a column in SQLite needs a table rebuild — I would leave them, since the
patch adds them anyway.

*(Incidentally, sampler row 245 is a freshly-minted instance of the defect: `adx_1h = 22.3` at 13:05
while the converged 1h ADX at that moment was **15.45**.)*

---

# THE PATCH — what it does, and why in that shape

## 1 · ONE WINDOW FOR ONE INDICATOR

**Routed through `_fetch_ohlcv_cached(..., CANDLE_LIMIT)` as you preferred, and your reason for
preferring it turned out to be stronger than "one source of truth":**

```python
ADX_CANDLE_LIMIT = CANDLE_LIMIT     # by IDENTITY, not by two literals that agree

def adx_reading(exchange, symbol, tf) -> AdxReading:
    ohlcv = _fetch_ohlcv_cached(exchange, symbol, tf, ADX_CANDLE_LIMIT)
    return AdxReading((compute_tf_metrics(ohlcv) or {}).get('adx'), ADX_CANDLE_LIMIT, tf)
```

- **Identity, not coincidence.** `fetch_snapshot`'s `limit` defaults to `CANDLE_LIMIT`, so the entry
  reference and every later reading are the same measurement *by construction*. Raising the literal
  to `200` in two more places would have re-created the original defect's precondition: two numbers
  that must be kept in step by hand.
- **The cache makes it cheaper, not more expensive.** The T+10s recheck runs ~13 s after the entry
  snapshot populated the 1h OHLCV cache, and the 1h TTL is 300 s — so it reads *the bytes the entry
  read*. Same value, no extra request. Verified live: `adx_reading` and the entry path return the
  identical float.
- **If `CANDLE_LIMIT` is ever changed**, every window already persisted stops matching and every
  comparison **refuses** rather than silently mixing. That is intended, not a regression.

**ATR: unchanged, and here is the proof rather than the assertion.** Both `_recheck_fetch_1h_metrics`
and `_tf_metrics_safe` keep their `ATR_LEN*3` fetch for ATR / `vol_ratio` / `trend` / `ema_gap_dir`
and add the sanctioned ADX alongside. Live, one instant, `last = 64686.1`:

| TF | ADX before (42) | ADX after (200) | ATR% before | ATR% after | identical? | trend |
|---|---:|---:|---:|---:|:---:|---|
| 1h | 21.92 | **15.09** | 0.505626 | 0.505626 | ✅ | bull / bull |
| 15m | 45.68 | **45.13** | 0.189620 | 0.189620 | ✅ | neutral / neutral |
| 5m | 33.63 | **32.54** | 0.103400 | 0.103400 | ✅ | bear / bear |

The comment at `virtual_trader.py:683` is correct **for ATR**, was written for ATR, and its
neighbouring claim — *"one 1h OHLCV fetch per tier yields both metrics, so baselines and rechecks are
measured identically"* — was the sentence that hid this for weeks. **Its first half was true and its
second half was false**, and the patch rewrites it to say so.

## 2 · THE PROVENANCE GUARD — §2.19's shape, both halves

§2.19 made `source` a **required positional** *and* ANDed it into the **WHERE clause**: a caller who
had not thought about provenance could not write a working call, and a *wrong* provenance could not
borrow another book's distribution — it got that book's rows or none. The equivalent, mechanism by
mechanism:

| §2.19 (book) | here (indicator window) |
|---|---|
| `source` a required positional | `AdxReading(value, window, tf)` — a NamedTuple with **no defaults**; a reading cannot be built without stating all three |
| `source` ANDed into the WHERE clause → a foreign percentile is **unobtainable** | `usable_for_threshold()` demands the sanctioned window → an unconverged ADX **cannot be tested against `ADX_BELOW_FLOOR` at all**; `adx_delta()` **refuses** across windows or timeframes and returns `None`, so the rule SKIPS |
| a figure that cannot be ranked is rendered **RAW with its source named**, and the prompt says so in words | a sample whose window is not sanctioned is rendered raw with its window named, and the prompt says **no rise or fall may be inferred** |
| — | **a bare float reaches none of it.** It has no window, so both rules refuse it |
| — | skips are written into `reasons_json`, so a silent skip cannot read as a passed check |

**Three new columns persist the window** — because a provenance that lives only in the code is a
provenance that goes stale silently: `virtual_positions.entry_adx_1h_window`,
`recheck_events.adx_window`, `smart_exit_dryrun_samples.adx_window`.

### The guard truth table, executed

```
=== comparable_to / adx_delta
  same window+tf              adx_delta -> -0.3
  42 vs 200 (the defect)      adx_delta -> None (rule SKIPS)
  unrecorded entry window     adx_delta -> None (rule SKIPS)
  different timeframe         adx_delta -> None (rule SKIPS)
  current value None          adx_delta -> None (rule SKIPS)
  entry is a bare float       adx_delta -> None (rule SKIPS)

=== usable_for_threshold
  200-candle, 13.5     -> True    label: ADX1h=13.5
  42-candle, 25.4      -> False   label: ADX1h=25.4 [42-candle window]
  unrecorded, 13.5     -> False   label: ADX1h=13.5 [unrecorded window]
  200-candle, None     -> False   label: ADX1h=na
```

### `_health_score` end to end, on vpos 87's real numbers

entry 64838.7 · last 64859.5 · entry ATR% 0.49965 · cur ATR% 0.49949 · walls 20.4/16.0 (0 pts by config)

```
BEFORE fix (42-bar cur, float entry)          score=  0  OK        parts=[none]
AFTER, legacy row (entry window NULL)         score= -5  TIGHTEN   parts=[ADX 13.8<20 (-5)]  skipped=[not comparable]
AFTER, new row (both 200)                     score= -5  TIGHTEN   parts=[ADX 13.8<20 (-5)]
AFTER, cur still 42-bar (now impossible)      score=  0  OK        parts=[none]  skipped=[not comparable, window not sanctioned]
AFTER, real ADX drop 30->13                   score= -8  TIGHTEN   parts=[ADX -17.0 (-3), ADX 13.0<20 (-5)]
AFTER, healthy 30->29                         score=  0  OK        parts=[none]
```

🔴 **Read the fourth line carefully — it is the guard's whole point.** A foreign-window reading
produces **no judgement**, not a wrong one, and both refusals are recorded. That is "unobtainable,
not merely omitted", carried over from §2.19 intact.

### The exit prompt, rendered live against the real vpos 87 row

The latest sample (row 245) has `adx_window` NULL, so the prompt now refuses the comparison in words:

```
regime_entry: regime=TREND 1d=neutral 4h=bull 1h=bull ADX1h=13.5
regime_now  : 15m=bull 5m=neutral ADX1h=22.3 ADX15m=49.6
  🔴 NOTE: the two ADX figures above were computed on DIFFERENT candle windows — the
  'At entry' value on 200 candles and the 'Now' value on an unrecorded window. ADX(14)
  is doubly smoothed and reads far higher on a short window, so these are NOT two
  observations of one quantity: NO rise or fall between them may be inferred. Judge the
  'Now' figure on its own, or ignore it.
```

With `adx_window = 200` on the sample (what every post-fix sample carries), the NOTE disappears and
the comparison stands on its own — verified by flipping that one column on a **copy** of the DB.

## 3 · THE BEHAVIOUR CHANGE — stated before it ships, and validated before it is trusted

Replayed **all 38 `recheck_events` rows** with the 200-bar ADX recomputed at each row's own timestamp
from real 1h candles (854 candles from 2026-06-25; the forming-candle `iloc[-1]` call reproduced
exactly), then re-scored each with the real `_health_score` rules.

**The replay validates itself first: reconstructing the STORED score from the STORED inputs is
38/38 exact.** Only then is the ADX swapped.

| | |
|---|---|
| OK verdicts today | **36** of 38 |
| **become TIGHTEN on the corrected window** | **9 of 36 = 25%** |
| become **EMERGENCY_CLOSE** | **0** — worst corrected score is −6; the emergency floor is −10 |
| TIGHTEN → OK (a rule turned OFF) | **0** |
| difference from re-enabling `adx_drop` | **NONE** — 9 either way |

Every row, corrected ADX vs stored:

```
 id vpos tier side  stored  adx42  adx200  e_adx | now     -> corrected
  2   74   10 SHORT     -5  15.56   17.03  16.71 | TIGHTEN -> TIGHTEN (-5)
  3   75   10 LONG       0  41.85   34.58  34.24 | OK      -> OK (0)
  4   75   60 LONG       0  41.85   34.58  34.24 | OK      -> OK (0)
  5   75  300 LONG       0  41.85   34.58  34.24 | OK      -> OK (0)
  6   76   10 SHORT      0  29.56   21.45  21.35 | OK      -> OK (0)
  7   76   60 SHORT      0  29.56   21.45  21.35 | OK      -> OK (0)
  8   76  300 SHORT      0  29.56   21.45  21.35 | OK      -> OK (0)
  9   77   10 SHORT      0  48.21   30.90  30.29 | OK      -> OK (0)
 10   77   60 SHORT      0  48.21   30.90  30.29 | OK      -> OK (0)
 11   77  300 SHORT      0  48.21   30.90  30.29 | OK      -> OK (0)
 12   78   10 LONG       0  29.20   25.19  25.05 | OK      -> OK (0)
 13   78   60 LONG       0  29.20   25.19  25.05 | OK      -> OK (0)
 14   78  300 LONG       0  29.20   25.19  25.05 | OK      -> OK (0)
 15   79   10 LONG       0  22.31   22.39  21.75 | OK      -> OK (0)
 16   79   60 LONG       0  22.31   22.39  21.75 | OK      -> OK (0)
 17   79  300 LONG       0  22.31   22.39  21.75 | OK      -> OK (0)
 18   80   10 SHORT      0  34.93   29.98  30.38 | OK      -> OK (0)
 19   80   60 SHORT      0  34.93   29.98  30.38 | OK      -> OK (0)
 20   80  300 SHORT      0  34.93   29.98  30.38 | OK      -> OK (0)
 21   81   10 SHORT      0  31.35   20.72  20.51 | OK      -> OK (0)
 22   81   60 SHORT      0  31.35   20.72  20.51 | OK      -> OK (0)
 23   81  300 SHORT      0  31.35   20.72  20.51 | OK      -> OK (0)
 24   82   10 LONG       0  22.25   16.88  16.88 | OK      -> TIGHTEN (-5)   <<<
 25   82   60 LONG       0  22.25   16.88  16.88 | OK      -> TIGHTEN (-5)   <<<
 26   82  300 LONG       0  22.25   16.88  16.88 | OK      -> TIGHTEN (-5)   <<<
 27   83   10 SHORT      0  37.65   26.95  26.34 | OK      -> OK (0)
 28   83   60 SHORT      0  37.65   26.95  26.34 | OK      -> OK (0)
 29   83  300 SHORT      0  37.65   26.95  26.34 | OK      -> OK (0)
 30   84   10 LONG       0  40.32   31.39  30.71 | OK      -> OK (0)
 31   84   60 LONG       0  40.32   31.39  30.71 | OK      -> OK (0)
 32   84  300 LONG       0  40.32   31.39  30.71 | OK      -> OK (0)
 33   85   10 LONG       0  26.14   16.81  16.70 | OK      -> TIGHTEN (-5)   <<<
 34   85   60 LONG       0  26.14   16.81  16.70 | OK      -> TIGHTEN (-5)   <<<
 35   85  300 LONG      -1  26.14   16.81  16.70 | OK      -> TIGHTEN (-6)   <<<
 36   86   10 SHORT     -5  11.53   11.38  11.12 | TIGHTEN -> TIGHTEN (-5)
 37   87   10 LONG       0  25.64   13.83  13.52 | OK      -> TIGHTEN (-5)   <<<
 38   87   60 LONG       0  25.64   13.83  13.52 | OK      -> TIGHTEN (-5)   <<<
 39   87  300 LONG       0  25.64   13.83  13.52 | OK      -> TIGHTEN (-5)   <<<
```

**Three things worth pulling out of that table:**

1. **The 9 flips are 3 positions, not a spray** — vpos 82, 85, 87, every one a LONG whose true 1h ADX
   was 16.9 / 16.8 / 13.8. The rule is firing on exactly the states it was written for.
2. **`adx_drop` never mattered.** With both sides on one window the entry-vs-now gap is fractions of a
   point (13.52 vs 13.83 on vpos 87), so enabling or skipping it changes nothing across all 38 rows.
   **The floor was always the whole story** — which is also why refusing `adx_drop` on legacy rows
   costs nothing measurable.
3. **vpos 86 and 74 were already TIGHTEN and stay TIGHTEN.** At genuinely low ADX the warm-up bias
   collapses (42-bar 11.53 vs 200-bar 11.38), which is precisely *why the defect hid for weeks*: the
   two rows where the rule did fire are the two where the two windows happened to agree.

**What a TIGHTEN does, so "the rule starts firing" is not read as "the bot starts moving stops":**
`_tighten_sl` is bounded by `93c20c3` so it can never end up tighter than the **original** stop, and
the recheck only ever runs pre-breakeven where `current_sl == original_sl`. So `new_sl == current_sl`,
the §2.20 branch takes over, and the outcome is: `t+{tier}_ok` written (later tiers stay due), one
`🟨 TIGHTEN (advisory only)` Telegram line, **exchange stop untouched, no cancel, no re-place.**
**Nine advisories, zero stop moves, zero dollars.**

**And it closes the loop you spotted:** the §2.20 no-op-TIGHTEN fix has never executed in live
because vpos 87 never reached the TIGHTEN branch — and it never reached it *because* the 42-bar ADX
suppressed the floor. Fixing the window is what finally exercises it.

## 4 · CONTAMINATION LEDGER — marked, nothing re-run

Written into OPEN-ITEMS as **§2.26b**. Summary:

| table · column | rows | what is wrong | safe cut |
|---|---:|---|---|
| `smart_exit_dryrun_samples.adx_1h/.adx_15m/.adx_5m` | **all 245** | 42-bar; +6.23 mean high on 1h, +4.3 pts on 15m | `WHERE adx_window = 200` |
| `recheck_events.adx_1h` | **all 38** | same | `WHERE adx_window = 200` |
| `recheck_events.adx_delta` | **all 38** | 🔴 **not biased — MEANINGLESS**: a cross-window subtraction, `entry_adx` (200) − `adx_1h` (42) | do not use any legacy value |
| `recheck_events.health_score/.verdict/.reasons_json` | **38** | both ADX rules biased toward "healthy" | read every historical `OK` as *"OK, or an unfired ADX rule"*; the corrected replay is above |
| **`trades.srv_adx_*`** | ✅ **clean, all rows** | `fetch_snapshot(limit=CANDLE_LIMIT)` is its only producer, and that literal never changed in the file's git history | usable as-is — **this is why the ENTRY advisor's ADX was never wrong** |
| §2.16 chop-exit re-cut | not yet done | would have run on the 245 biased rows | cut on `adx_window = 200`, or drop ADX from it |

**Any past analysis quoting a recheck ADX, a recheck `adx_delta`, or a sampler `adx_*` is suspect.**
Known instances: every *"ADX rising to X"* / *"regime strengthened"* line quoted from an exit verdict.
One that survives scrutiny: §2.22's *"the recheck scored that same value −5 eleven seconds later"* is
**correct** — vpos 86's 11.271 and 11.117 barely differ, for the reason in point 3 above.

## 5–7 · YOUR §2.4 RULING — recorded as **§2.4-OP** and **§2.4b**, before the window opens

**5 · STRICT. vpos 86 contributes ZERO.** §2.4 stays **0 of ~10**. Its first `close` verdict
(01:50:24) was contaminated; nominating 03:50:29 is the re-cut the criterion forbids.

**6 · NO THIRD RESTART — and your framing is now the rule, in your words:** *if every fix voids the
accumulated sample, the criterion becomes unfalsifiable by attrition.* Written into §2.4-OP as four
clauses: the window **BEGINS at the ADX-fix commit**; the exit prompt's **inputs are FROZEN** for its
duration; a defect found during it means **finish the window and note the caveat**, never reset; and
the freeze scope is stated so it cannot be lawyered — **frozen = everything the advisor READS**, not
frozen = act/hold plumbing, logging, labels, close mechanics, or anything on the entry side. *Fixing a
close mechanic does not void the window; changing a number the advisor sees does.*

**7 · The nine verdicts are recorded as an operational fact with full arithmetic** in **§2.4b**:

| trades row | UTC | px | net if closed | R | vs actual |
|---|---|---:|---:|---:|---:|
| **19607** | **03:50:29 (first)** | 64191.30 | −1.3092 | −0.527 | **+1.2324 / +0.495R** |
| 19617 | 04:50:34 | 64060.00 | −1.0071 | −0.405 | +1.5345 / +0.617R |
| 19624 | 05:50:43 | 64038.70 | −0.9581 | −0.385 | +1.5835 / +0.637R |
| **19628** | **06:50:53 (best)** | 63961.00 | **−0.7793** | **−0.313** | **+1.7623 / +0.709R** |
| 19633 | 07:50:54 | 63970.00 | −0.8000 | −0.322 | +1.7416 / +0.700R |
| 19646 | 08:45:12 | 64309.20 | −1.5806 | −0.636 | +0.9610 / +0.386R |
| 19649 | 08:51:02 | 64288.30 | −1.5325 | −0.616 | +1.0091 / +0.406R |
| 19660 | 09:51:11 | 64549.70 | −2.1340 | −0.858 | +0.4076 / +0.164R |
| 19678 | 10:51:14 | 64569.20 | −2.1789 | −0.876 | +0.3627 / +0.146R |
| — | **11:50:48 ACTUAL** | **64733.00** | **−2.541574** | **−1.02213** | — |

**9 of 9 beat the actual exit, +0.146R to +0.709R.** With the three contaminated ones, the advisor
said `close` **twelve times over nine hours** on a position that then ran to its stop.

🔴 **And they are inadmissible twice over, which is the honest note §2.4b carries:** all nine also
carried a warm-up-biased ADX. **That is the concrete case that makes your no-third-restart ruling the
right call** — the sample was voided by two independent seams, and a third reset would have taught
nothing.

## 8–9 · THE OBSERVATORY GHOSTS — diagnosed, and **I got two things wrong at 13:09**

Read-only. Nothing touched. Full detail in OPEN-ITEMS **§2.28a**.

🔴 **Correction 1 — row 80 is NOT the naked short's record, and is not the naked short at all.** The
naked short was in the **first** live window, before the 21:26:52 revert. Rows 79/80 are stamped
**21:50:04 / 21:50:11**, inside the **PAPER interlude** (21:26:52 → 21:54:16) — proven by the journal's
own 21:53:11 boot banner: `🧪 PAPER — simulated fills only ... LIVE_TRADING_ENABLED=False`. **No real
money is implicated by either row.** So the answer to your question is no: this is **not** recoverable
evidence about the naked short. Its −$0.26 is still recorded only in prose, and §7's caveat stands
exactly as written. My 13:09 line — *"it DOES have a surviving record, with an entry price and a
stop"* — was wrong, and it was wrong in the direction of making a find sound bigger than it was.

🔴 **Correction 2 — row 80 is NOT accumulating. Row 79 is.** Row 80 stopped being writable at
02:00:14: `on_15m_exit_signal` only touches rows `WHERE shadow_exit_at IS NULL AND status IN
('shadow_armed_pending_close','shadow_armed_post_close')`, and row 80 now fails both; its drift slots
can only be seeded by `on_real_close`, which needs a `virtual_positions` row that will never exist
(**0 drift rows**). It is **inert** — permanently non-terminal, re-read by `tick()` every 5 s and
never able to finish. **Row 79 is the live one:** 5 drift slots seeded off today's real close, 15m and
1h sampled (12:06 → 64831.3, 12:51 → 64867.1), **4h / 12h / 24h still due.**

**How they got there — from two DB backups and the journal, not from a theory:**

| evidence | what it shows |
|---|---|
| 07-29 **16:46** backup | `virtual_positions` max **85**, sequence **85**, observatory max id **77** — **no 79/80** |
| 07-30 **11:31** backup | 79 and 80 present with the 21:50 stamps; `virtual_positions` max **86**, sequence **86** |
| journal 07-29 19:00 → 07-30 01:00 | **exactly ONE** `VIRTUAL ENTRY vpos=` line — vpos 86 at **00:50:15**. **Nothing at 21:50** |
| `on_entry` re-SELECTs the row by id and arms only if it exists | rows **86 and 89 must have existed** at 21:50 ⇒ 86, 87, 88, 89 were all allocated |
| sequence is **86**, and AUTOINCREMENT never lowers itself | the sequence was **explicitly reset** after those ids were consumed |
| the rows are **7.6 s apart on the SAME side** | `MAX_POSITIONS_PER_SIDE=1` + `ux_vpos_one_open_per_side` forbid that concurrently ⇒ create → delete → create, a **test loop** |
| BTC 1h candle 07-29 21:00 = 63231.6–63829.7 | the ghost entries 63605.6 / 63595.5 are real prices of that minute |

**Conclusion: residue from an ad-hoc script run OUTSIDE the service during the paper interlude, to
exercise the naked-position fix (`97a4fdb`).** It created `virtual_positions` 86–89, which armed the
observatory; the rows were then deleted and the sequence reset to leave a clean book before going live
at 21:54:16 — and `post_exit_observatory`, a separate table nobody was thinking about, kept its two.
Today's real vpos 86 re-used id 86, and `on_entry`'s `ON CONFLICT(vpos_id) DO NOTHING` silently
preserved the ghost.

**The code defect, separable from the data mess:** `on_entry` treats `vpos_id` as a stable identity.
It is not — `virtual_positions.id` is unique only among rows that still **exist**. The §2.19-shaped fix
is to make the conflict **speak**: a differing `opened_at` means a different position, so refuse and
shout rather than adopt. **Not written, not proposed** — you sequenced the observatory after the ADX
fix.

**What would stop each — stated, NOT done** (`feedback_no_delete_virtual_positions` standing, both are
data decisions): row 80 needs `status` set to the existing terminal sentinel `'failed'`; row 79 cannot
be repaired by a status change (its `entry_price` / `original_sl_price` / `opened_at` would need
correcting to vpos 86's real values **and** `shadow_pnl_r` / `exit_advantage_r` recomputing). 🔴 **And
neither should be touched before the `on_entry` guard exists**, or the next id re-use recreates
exactly the same row.

---

## VERIFICATION RUN ON THE PATCH

| check | result |
|---|---|
| `py_compile` | **4/4 pass** (`indicators.py`, `virtual_trader.py`, `main.py`, `sensor_events.py`) |
| symtable FUNCTION-scope audit (the 29.07 guard) | **0 unresolved names across all 4 files** |
| guard truth table | **6/6 comparison cases, 4/4 threshold cases** — see above |
| `_health_score` end-to-end | **6 scenarios**, including the before/after pair on vpos 87's real numbers |
| historical replay self-validation | **38/38 exact** reconstruction of stored scores from stored inputs |
| live smoke test, all 3 TFs | ADX moves, **ATR% byte-identical**, `trend` identical, `vol_ratio` intact |
| exit-prompt guard | rendered live on the real vpos 87 row: NOTE present with NULL window, absent with `window=200` |
| ADX accessor identity | `ADX_CANDLE_LIMIT is CANDLE_LIMIT` → **True** |
| other ADX producers audited | `adaptive_trail` uses `true_atr_wilder` only (**no ADX**); `optimizer._bucket_adx_1h` reads `trades.srv_adx_1h` (**clean entry path**); `breakeven_worker` has **no** ADX |
| live tree | `/root/titan-bot` **byte-identical to `81875c9`** (md5 verified), `git status` clean |
| service | **untouched** — active since 11:32:45, `NRestarts=0`, 0 errors |

---

## WHAT I DID NOT DO

- **Did not apply the patch.** `/root/titan-bot` unchanged; no commit, no restart. Awaiting your word.
- **Did not backfill `entry_adx_1h_window`** on legacy rows, even though the invariant makes it
  correct. Asserting provenance from a code invariant is the habit that produced this defect, and the
  measured cost of refusing is **zero verdicts across 38 rows**. The open vpos 87 therefore loses
  `adx_drop` — a rule that has never fired.
- **Did not touch the observatory rows**, or `virtual_positions`, or re-run any analysis over the
  contaminated tables.
- **Did create two DB columns by accident** — disclosed and assessed at the top of this report.

**Three things wait on you:** apply the ADX patch (it opens the §2.4 window, so applying it is also
the act that starts the frozen-prompt clock); then the observatory `on_entry` guard; then the two
observatory data decisions.

---

## THE FULL DIFF — `81875c9` + this patch, 4 files, **+404 / −40**

```diff
--- a/titan-bot/indicators.py
+++ b/titan-bot/indicators.py
@@ -14,7 +14,7 @@
 import logging
 import time
 from threading import Lock
-from typing import Optional, Dict, List, Tuple
+from typing import NamedTuple, Optional, Dict, List, Tuple
 
 import pandas as pd
 import pandas_ta as ta
@@ -52,6 +52,163 @@
 _cache_lock = Lock()
 _ohlcv_cache: Dict[Tuple[str, str], Tuple[float, List]] = {}
 
+# ---------------------------------------------------------------------------
+# 🔴 ADX PROVENANCE — ONE WINDOW FOR ONE INDICATOR (2026-07-30)
+#
+# ADX(14) is DOUBLY Wilder-smoothed (DX, then a second smoothing), so it
+# converges FAR more slowly than ATR(14), which is smoothed once. Measured on
+# live BTC 1h at a single instant:
+#
+#     limit= 42 -> 25.640      limit=150 -> 13.838
+#     limit= 60 -> 15.063      limit=200 -> 13.834   <- CANDLE_LIMIT: converged
+#     limit=100 -> 13.961      limit=300 -> 13.834
+#
+# The bot used to read ADX on TWO windows and render the difference as a CHANGE:
+# the entry snapshot on CANDLE_LIMIT (converged) and BOTH the post-entry recheck
+# and the smart-exit sampler on ATR_LEN*3 = 42 (not warmed up). Over 800 paired
+# readings on 1,000 real 1h candles the 42-bar figure ran +6.23 mean / +5.38
+# median HIGH, was high in 74.1% of cases, and made ADX_BELOW_FLOOR=20 miss
+# 52.9% of the states it exists to catch. The exit prompt printed
+# "At entry ADX1h=13.5 / Now ADX1h=25.4" — an 11.9-point rise across 25 seconds
+# that never happened — and the advisor read it as "regime strengthened".
+#
+# THE SENSITIVITY IS ADX'S ALONE, and this was checked rather than assumed. Over
+# the SAME two windows: ATR 314.434 vs 317.352 (-0.9%), `trend` identical,
+# ema_gap 0.3551 vs 0.3548. So ATR keeps its calibrated ATR_LEN*3 window
+# EVERYWHERE — the comment at virtual_trader.py:683 was written for ATR, it is
+# correct for ATR, and nothing here changes ATR's behaviour. Only `adx` moves.
+#
+# ADX_CANDLE_LIMIT is the ONE window an ADX may be read on. It is CANDLE_LIMIT by
+# IDENTITY, not by coincidence: `fetch_snapshot` has always used CANDLE_LIMIT
+# (verified: a single `+CANDLE_LIMIT = 200` in this file's entire git history and
+# no later change), so pinning to the same name makes the entry reference and
+# every later reading the same measurement BY CONSTRUCTION rather than by two
+# literals that happen to agree. If CANDLE_LIMIT is ever changed, every ADX
+# window already persisted stops matching and every comparison REFUSES instead of
+# silently mixing — which is the intended behaviour, not a regression.
+ADX_CANDLE_LIMIT = CANDLE_LIMIT
+
+# Sentinel for a persisted ADX whose window was never recorded. It matches NO
+# sanctioned window, so it is refused everywhere rather than guessed. -1 rather
+# than None so `window` is always an int and comparisons never raise.
+ADX_WINDOW_UNKNOWN = -1
+
+
+class AdxReading(NamedTuple):
+    """An ADX value THAT CARRIES THE WINDOW IT WAS COMPUTED ON.
+
+    🔴 THE GUARD, and it is deliberately the §2.19 shape. There, `source` was made
+    a REQUIRED POSITIONAL argument *and* was ANDed into the SQL WHERE clause: a
+    caller who had not thought about provenance could not write a working call, and
+    a WRONG provenance could not borrow another book's distribution — it got that
+    book's rows or none. The equivalent here:
+
+      * `value`, `window` and `tf` have NO defaults, so a reading cannot be
+        constructed without stating all three — the call-site half of the guard;
+      * `comparable_to` REFUSES across windows and timeframes, and the callers
+        return None (the rule SKIPS) rather than a number — so a foreign-window
+        ADX is UNUSABLE for a rule, not merely unlabelled;
+      * `usable_for_threshold` demands the sanctioned window, so an unconverged
+        reading cannot be tested against a fixed constant at all.
+
+    A bare float has no window and therefore cannot reach any of it. That is the
+    point: the defect this closes was a bare float from a 42-candle fetch being
+    compared with a bare float from a 200-candle fetch, with nothing in the code,
+    the DB or the prompt able to notice.
+    """
+    value: Optional[float]
+    window: int
+    tf: str
+
+    def usable_for_threshold(self) -> bool:
+        """True ONLY for a value on the one sanctioned window. Required by every
+        rule that tests an ADX against a FIXED constant (config.ADX_BELOW_FLOOR):
+        a floor calibrated on converged values means nothing against an
+        unconverged one."""
+        return self.value is not None and self.window == ADX_CANDLE_LIMIT
+
+    def comparable_to(self, other) -> bool:
+        """True ONLY when both readings are the SAME measurement — same window AND
+        same timeframe. Two different windows are not two observations of one
+        quantity, and their difference is not a change in the market."""
+        return (isinstance(other, AdxReading)
+                and self.value is not None and other.value is not None
+                and self.window == other.window and self.tf == other.tf)
+
+    def label(self) -> str:
+        """Render for a log line or a prompt. States the window whenever it is NOT
+        the sanctioned one, so an unusable figure is visibly unusable (§2.19: a
+        figure that cannot be ranked is rendered RAW with its provenance named)."""
+        if self.value is None:
+            return f"ADX{self.tf}=na"
+        if self.window == ADX_CANDLE_LIMIT:
+            return f"ADX{self.tf}={self.value:.1f}"
+        w = 'unrecorded' if self.window == ADX_WINDOW_UNKNOWN else f"{self.window}-candle"
+        return f"ADX{self.tf}={self.value:.1f} [{w} window]"
+
+
+def adx_delta(entry: 'AdxReading', current: 'AdxReading') -> Optional[float]:
+    """`entry - current`, and ONLY when the two are the same measurement.
+
+    Returns None across windows or timeframes — the caller's rule then SKIPS.
+    This is the half of the guard that cannot be bypassed by a careless call: the
+    old code did this subtraction on two bare floats from different fetches, which
+    is how a +11.9-point warm-up artefact became "ADX fell/rose"."""
+    if not isinstance(entry, AdxReading) or not entry.comparable_to(current):
+        return None
+    return entry.value - current.value
+
+
+def adx_reading(exchange, symbol: str, tf: str) -> AdxReading:
+    """THE ONLY SANCTIONED WAY TO READ AN ADX.
+
+    Routes through the SAME cached fetch at the SAME CANDLE_LIMIT the entry
+    snapshot uses, so the entry reference and every later reading are one
+    measurement rather than two literals that must be kept in step by hand. It
+    also inherits the per-TF OHLCV cache (`_CACHE_TTL_BY_TF`), which is why this
+    is cheaper than raising the literal at each call site: the T+10s recheck runs
+    ~13 s after the entry snapshot populated the 1h cache, so it reads the exact
+    bytes the entry read — same value, no extra request.
+
+    A failed fetch or compute returns value=None with the window STILL stated:
+    every rule skips a None, and nothing downstream can mistake it for a number."""
+    try:
+        ohlcv = _fetch_ohlcv_cached(exchange, symbol, tf, ADX_CANDLE_LIMIT)
+        v = (compute_tf_metrics(ohlcv) or {}).get('adx')
+    except Exception as e:
+        log.warning("adx_reading %s %s failed: %s", symbol, tf, e)
+        v = None
+    return AdxReading(v, ADX_CANDLE_LIMIT, tf)
+
+
+def adx_reading_from_stored(value, window, tf: str) -> AdxReading:
+    """Rehydrate a PERSISTED reading.
+
+    `window` is whatever the row recorded. NULL on every row written before the
+    window was persisted, and a NULL window is honestly UNKNOWN — it becomes
+    ADX_WINDOW_UNKNOWN, which matches no sanctioned window, so every comparison
+    and every threshold test involving it REFUSES.
+
+    🔴 LEGACY ROWS ARE NOT BACKFILLED, DELIBERATELY. Their `entry_adx_1h` really
+    was computed on CANDLE_LIMIT (fetch_snapshot is its only producer and that
+    literal never changed), so a backfill would be *correct* — and it would still
+    be a provenance value asserted from a code invariant rather than recorded at
+    write time, which is the habit that produced this defect. The cost of refusing
+    instead was measured, not assumed: across all 38 recheck_events rows ever
+    written, enabling or skipping the adx_drop rule changes ZERO verdicts, because
+    once both sides sit on the same window the entry-vs-now gap is fractions of a
+    point. Legacy rows lose a rule that has never fired; they do not get a guessed
+    window."""
+    try:
+        v = float(value) if value is not None else None
+    except (TypeError, ValueError):
+        v = None
+    try:
+        w = int(window)
+    except (TypeError, ValueError):
+        w = ADX_WINDOW_UNKNOWN
+    return AdxReading(v, w, tf)
+
 
 def _to_df(ohlcv):
     df = pd.DataFrame(
--- a/titan-bot/virtual_trader.py
+++ b/titan-bot/virtual_trader.py
@@ -34,9 +34,18 @@
 import adaptive_trail
 import sensor_events
 # Post-entry recheck reuses the SAME order-book wall analysis as the live entry
-# gate (microstructure.fetch_pre_trade_walls) and the SAME 1h ADX/ATR computation
-# as the entry snapshot (indicators.compute_tf_metrics) — one 1h OHLCV fetch per
-# tier yields both metrics, so baselines and rechecks are measured identically.
+# gate (microstructure.fetch_pre_trade_walls) and the SAME 1h ADX/ATR ALGORITHMS
+# as the entry snapshot (indicators.compute_tf_metrics).
+# 🔴 CORRECTED 2026-07-30: "one 1h OHLCV fetch per tier yields both metrics, so
+# baselines and rechecks are measured identically" — the first half was true and
+# the SECOND HALF WAS FALSE, which is exactly how this went unnoticed. The same
+# ALGORITHM on a DIFFERENT WINDOW is not the same measurement: ADX(14) is doubly
+# Wilder-smoothed and read +6.23 mean high on the ATR_LEN*3 window this fetch
+# uses. ADX now comes from indicators.adx_reading() on the entry's own
+# CANDLE_LIMIT window and arrives carrying it; ATR still comes off the
+# ATR_LEN*3 fetch, because that is the window ITS entry baseline was calibrated
+# on. TWO fetches, deliberately — one window per indicator, each matching its
+# own baseline.
 import microstructure
 import indicators
 import liquidity_zones
@@ -301,6 +310,13 @@
                         # 'done', or terminal 'tightened' / 'closed_critical'.
                         "entry_wall_baseline_mult REAL",
                         "entry_adx_1h REAL",
+                        # 🔴 THE WINDOW THE ADX ABOVE WAS COMPUTED ON (2026-07-30).
+                        # A stored ADX without its window is exactly what let a
+                        # 42-candle reading be compared with a 200-candle one for
+                        # weeks. NULL on every legacy row and NOT backfilled — see
+                        # indicators.adx_reading_from_stored for why, and for the
+                        # measured cost of refusing (zero verdicts change).
+                        "entry_adx_1h_window INTEGER",
                         "entry_atr_pct_1h REAL",
                         # At-entry side-aware book snapshot (2026-07-04, diff #2).
                         # Observational — read by NO gate/exit; accumulates
@@ -408,6 +424,12 @@
                 "lux_volatility_entry TEXT",
                 # momentum
                 "adx_1h REAL", "adx_15m REAL", "adx_5m REAL",
+                # 🔴 the candle window all three ADX values above were computed on
+                # (2026-07-30). NULL on the 245 legacy rows, which were all written
+                # on the unconverged ATR_LEN*3 window — the exit prompt refuses to
+                # compare an ADX carrying a NULL/foreign window against the entry
+                # figure, and says so in words instead of implying a change.
+                "adx_window INTEGER",
                 "trend_15m_live TEXT", "trend_5m_live TEXT",
                 "mom_flip_15m INTEGER", "mom_flip_5m INTEGER",
                 "ema_gap_dir_1h_live TEXT",
@@ -646,7 +668,28 @@
     "acts correctly, stays quiet" instead of raising — the failure mode of
     2026-07-29, where the NAME itself was absent from this scope and the
     NameError fired while evaluating an argument, is what that default prevents.
+
+    🔴 `entry_adx_1h` IS EXPECTED TO BE AN indicators.AdxReading (2026-07-30), so
+    the window it was measured on is persisted alongside the value and the recheck
+    never has to assume. It DEGRADES rather than raises on a bare float: the value
+    is still stored and the window is recorded as UNKNOWN, so the adx_drop rule
+    refuses for that position instead of silently comparing across windows. Chosen
+    over raising deliberately — a TypeError here would stop the bot trading, and
+    "lose one rule on one position" is the cheaper failure. The normalisation runs
+    BEFORE any exchange call for the 2026-07-29 reason: nothing that can go wrong
+    with an argument should be able to go wrong after a fill.
     """
+    if isinstance(entry_adx_1h, indicators.AdxReading):
+        _entry_adx_val = entry_adx_1h.value
+        _entry_adx_window = entry_adx_1h.window
+    else:
+        _entry_adx_val = entry_adx_1h
+        _entry_adx_window = None
+        if entry_adx_1h is not None:
+            print(f"[VIRTUAL] ⚠️ entry_adx_1h arrived as a bare "
+                  f"{type(entry_adx_1h).__name__}, not an AdxReading — window "
+                  f"recorded as UNKNOWN, so the recheck's adx_drop rule will "
+                  f"refuse for this position. Fix the caller.", flush=True)
     # 🔴 UNSAFE-STATE BREAKER. Tripped only when an entry failsafe close FAILED,
     # i.e. a real position may exist that we could not unwind. Refuse to trade
     # until a human has looked; a restart clears it.
@@ -845,6 +888,9 @@
         _entry_n_ask = len(pre_trade_walls.get('walls_ask') or []) if pre_trade_walls else None
         _entry_atr_pct = (entry_atr_pct_1h if entry_atr_pct_1h is not None
                           else (atr_1h / fill_price * 100.0 if fill_price else None))
+        # entry_adx_1h_window: recorded, never derived. See the docstring — a
+        # bare float leaves this NULL and the recheck refuses rather than guesses.
+        _entry_adx_win = _entry_adx_window
 
         # step_margin_usdt / step_size columns are NOT NULL — repurposed here to
         # store the single-entry margin and size. pending_dca_limits now holds the
@@ -898,11 +944,12 @@
                     "pending_dca_limits, filled_legs, water_mark, status, "
                     "opened_at, trades_entry_row_id, "
                     "initial_risk_usdt, original_sl_price, max_adverse_price, "
-                    "entry_wall_baseline_mult, entry_adx_1h, entry_atr_pct_1h, "
+                    "entry_wall_baseline_mult, entry_adx_1h, "
+                    "entry_adx_1h_window, entry_atr_pct_1h, "
                     "entry_sup_wall_mult, entry_sup_wall_dist_pct, "
                     "entry_opp_wall_dist_pct, entry_ob_imbalance, "
                     "entry_n_walls_bid, entry_n_walls_ask, stop_order_id) "
-                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
+                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (
                         symbol, position_side, side, margin_required, amount, LEVERAGE,
                         fill_price, atr, sl_price, trail_pct,
@@ -912,7 +959,8 @@
                         # ORIGINAL ATR stop (sl_price here is pre-breakeven).
                         # max_adverse_price = MAE seed at entry price (mirror water_mark).
                         realized_risk_usdt, sl_price, fill_price,
-                        _entry_wall_mult, entry_adx_1h, _entry_atr_pct,
+                        _entry_wall_mult, _entry_adx_val, _entry_adx_win,
+                        _entry_atr_pct,
                         _entry_sup_mult, _entry_sup_dist,
                         _entry_opp_dist, _entry_ob_imb,
                         _entry_n_bid, _entry_n_ask,
@@ -1338,6 +1386,11 @@
     """Delta-based health score (<= 0). Each rule subtracts; missing inputs
     (None) skip their rule. Returns (score, [reason strings], [detail dicts]).
 
+    🔴 `entry_adx` and `cur_adx` are indicators.AdxReading, NOT floats (2026-07-30).
+    A bare float has no window and is refused by both ADX rules below — which is
+    the whole guard: this function used to accept two floats and subtract them
+    without either being able to say what it was measured on.
+
     `details` is a STRUCTURED mirror of `parts` (rule name, measured value, points
     contributed) for recheck_events.reasons_json — purely additive, it is written to
     the DB and read by nothing. `score` and `parts` are byte-identical to before, so
@@ -1364,17 +1417,50 @@
             details.append({'rule': 'wall_growth_warning', 'value': round(ratio, 4),
                             'threshold': WALL_GROWTH_WARNING,
                             'points': -WALL_GROWTH_WARNING_SCORE})
-    if entry_adx is not None and cur_adx is not None:
-        if (entry_adx - cur_adx) > ADX_DROP_THRESHOLD:
-            score -= 3
-            parts.append(f"ADX -{entry_adx - cur_adx:.1f} (-3)")
-            details.append({'rule': 'adx_drop', 'value': round(entry_adx - cur_adx, 3),
-                            'threshold': ADX_DROP_THRESHOLD, 'points': -3})
-        if cur_adx < ADX_BELOW_FLOOR:
-            score -= 5
-            parts.append(f"ADX {cur_adx:.1f}<{ADX_BELOW_FLOOR:.0f} (-5)")
-            details.append({'rule': 'adx_below_floor', 'value': round(cur_adx, 3),
-                            'threshold': ADX_BELOW_FLOOR, 'points': -5})
+    # 🔴 BOTH ADX RULES NOW DEMAND PROVENANCE (2026-07-30). `entry_adx` and
+    # `cur_adx` are indicators.AdxReading, not floats, and each rule asks the
+    # guard for permission rather than trusting that two numbers are comparable:
+    #
+    #   adx_drop        -> indicators.adx_delta(), which returns None across
+    #                      windows or timeframes. The rule then SKIPS. This
+    #                      subtraction used to run on two bare floats from a
+    #                      200-candle fetch and a 42-candle fetch, so a +6-point
+    #                      warm-up artefact was read as "ADX fell by 6 less than
+    #                      it did" — biasing the rule toward silence.
+    #   adx_below_floor -> usable_for_threshold(), which demands the sanctioned
+    #                      window. A floor calibrated on converged values means
+    #                      nothing against an unconverged reading, and testing it
+    #                      anyway is what made this rule miss 52.9% of the states
+    #                      it exists to catch.
+    #
+    # A skipped rule is recorded in `details` so a silent skip cannot be mistaken
+    # for a passed check — the 29.07 lesson: check what the gate SAYS, not only
+    # what it decides.
+    _drop = indicators.adx_delta(entry_adx, cur_adx)
+    if _drop is not None and _drop > ADX_DROP_THRESHOLD:
+        score -= 3
+        parts.append(f"ADX -{_drop:.1f} (-3)")
+        details.append({'rule': 'adx_drop', 'value': round(_drop, 3),
+                        'threshold': ADX_DROP_THRESHOLD, 'points': -3})
+    elif _drop is None and isinstance(cur_adx, indicators.AdxReading):
+        details.append({'rule': 'adx_drop', 'value': None, 'points': 0,
+                        'skipped': 'not comparable',
+                        'entry_window': getattr(entry_adx, 'window', None),
+                        'cur_window': cur_adx.window})
+    if isinstance(cur_adx, indicators.AdxReading):
+        if cur_adx.usable_for_threshold():
+            if cur_adx.value < ADX_BELOW_FLOOR:
+                score -= 5
+                parts.append(f"ADX {cur_adx.value:.1f}<{ADX_BELOW_FLOOR:.0f} (-5)")
+                details.append({'rule': 'adx_below_floor',
+                                'value': round(cur_adx.value, 3),
+                                'threshold': ADX_BELOW_FLOOR, 'points': -5,
+                                'window': cur_adx.window})
+        elif cur_adx.value is not None:
+            details.append({'rule': 'adx_below_floor', 'value': round(cur_adx.value, 3),
+                            'threshold': ADX_BELOW_FLOOR, 'points': 0,
+                            'skipped': 'window not sanctioned',
+                            'window': cur_adx.window})
     if entry_atr_pct and entry_atr_pct > 0 and cur_atr_pct is not None:
         if (entry_atr_pct - cur_atr_pct) / entry_atr_pct > ATR_DROP_PCT:
             score -= 3
@@ -1534,18 +1620,36 @@
 
 
 def _recheck_fetch_1h_metrics(exchange, symbol, last):
-    """One 1h-OHLCV fetch -> (adx, atr_pct), via the SAME indicators path as the
-    entry snapshot (ADX_14 / ATR_14). Any failure -> (None, None) so a fetch
-    hiccup merely skips the ADX/ATR rules, never blocks the recheck."""
+    """1h metrics for the recheck -> (AdxReading, atr_pct).
+
+    🔴 TWO WINDOWS ON PURPOSE, AND THAT IS THE FIX (2026-07-30). This used to take
+    BOTH numbers off one ATR_LEN*3 = 42-candle fetch. ATR(14) is fine on 42 bars
+    (single Wilder smoothing; 314.4 vs 317.4 at 200 bars = -0.9%) AND that window
+    is the one the entry reference was calibrated on — `entry_atr_pct_1h` is
+    derived from execute_entry's own ATR_LEN*3 1h fetch, so moving ATR here would
+    break the atr_contraction rule by changing one side of its comparison. ATR
+    therefore stays EXACTLY where it was.
+
+    ADX(14) is NOT fine on 42 bars — it is doubly smoothed and had not warmed up,
+    running +6.23 mean high and making ADX_BELOW_FLOOR miss 52.9% of the states it
+    exists to catch. It now comes from indicators.adx_reading(), the one sanctioned
+    accessor, on the same CANDLE_LIMIT window as the entry snapshot, and it arrives
+    as an AdxReading carrying that window rather than as a bare float.
+
+    Cost: at T+10s this is usually FREE — the entry snapshot populated the 1h
+    OHLCV cache ~13 s earlier and the 1h TTL is 300 s, so the recheck reads the
+    same bytes the entry read. Any failure -> value=None (rules skip) or
+    atr_pct=None; never blocks the recheck."""
+    adx = indicators.adx_reading(exchange, symbol, '1h')
     try:
         ohlcv_1h = exchange.fetch_ohlcv(symbol, '1h', limit=ATR_LEN * 3)
         m = indicators.compute_tf_metrics(ohlcv_1h) or {}
         atr = m.get('atr')
         atr_pct = (atr / last * 100.0) if (atr is not None and last) else None
-        return m.get('adx'), atr_pct
     except Exception as e:
-        print(f"[VIRTUAL] recheck 1h metrics fetch failed [{symbol}]: {e}", flush=True)
-        return None, None
+        print(f"[VIRTUAL] recheck 1h ATR fetch failed [{symbol}]: {e}", flush=True)
+        atr_pct = None
+    return adx, atr_pct
 
 
 def _run_recheck_tier(exchange, row, last, tier, send_tg):
@@ -1563,7 +1667,12 @@
     cur_adx, cur_atr_pct = _recheck_fetch_1h_metrics(exchange, symbol, last)
 
     entry_wall_mult = row['entry_wall_baseline_mult'] if 'entry_wall_baseline_mult' in _rk else None
-    entry_adx = row['entry_adx_1h'] if 'entry_adx_1h' in _rk else None
+    # The entry ADX is rehydrated WITH the window the row recorded (NULL ->
+    # UNKNOWN -> adx_drop refuses). It is never re-derived and never assumed.
+    entry_adx = indicators.adx_reading_from_stored(
+        row['entry_adx_1h'] if 'entry_adx_1h' in _rk else None,
+        row['entry_adx_1h_window'] if 'entry_adx_1h_window' in _rk else None,
+        '1h')
     entry_atr_pct = row['entry_atr_pct_1h'] if 'entry_atr_pct_1h' in _rk else None
 
     score, parts, details = _health_score(
@@ -1573,10 +1682,15 @@
     verdict = _recheck_verdict(score)
     reasons = ", ".join(parts) if parts else "no negative deltas"
 
+    # The log line now prints the ADX's WINDOW alongside its value (via
+    # AdxReading.label(), which names the window whenever it is not the sanctioned
+    # one). The old line printed a bare number, which is why an 11.8-point
+    # divergence from the entry figure sat in the journal unremarked.
     print(f"[VIRTUAL] RECHECK vpos={vpos_id} {position_side} T+{tier}s "
           f"score={score} verdict={verdict} "
-          f"wall={cur_wall_mult}/{entry_wall_mult} adx={cur_adx} atr%={cur_atr_pct} "
-          f"| {reasons}", flush=True)
+          f"wall={cur_wall_mult}/{entry_wall_mult} "
+          f"adx={cur_adx.label()} (entry {entry_adx.label()}) "
+          f"atr%={cur_atr_pct} | {reasons}", flush=True)
 
     # Evidence row for EVERY tier run (OK included). sl_before is captured HERE,
     # before any branch can move the stop — that separation is the whole point:
@@ -1589,6 +1703,9 @@
                 verdict=verdict, details=details, entry_price=entry_price,
                 current_price=last, sl_before=_sl_before,
                 cur_wall_mult=cur_wall_mult, entry_wall_mult=entry_wall_mult,
+                # Readings, not floats: log_recheck derives adx_delta through the
+                # same guard, so the stored delta can no longer be a cross-window
+                # subtraction, and adx_window is persisted for every future cut.
                 adx_1h=cur_adx, entry_adx=entry_adx,
                 atr_pct_1h=cur_atr_pct, entry_atr_pct=entry_atr_pct)
 
@@ -1798,19 +1915,39 @@
 
 
 def _tf_metrics_safe(exchange, symbol, tf, last):
-    """One OHLCV fetch -> compute_tf_metrics dict (adx / atr_pct / vol_ratio /
-    trend / ema_gap_dir). Any failure -> {} so a hiccup merely blanks that TF's
-    fields; never raises, never touches the position."""
+    """Per-TF metrics for the smart-exit sampler -> compute_tf_metrics dict
+    (atr_pct / vol_ratio / trend / ema_gap_dir) with `adx` REPLACED by the
+    sanctioned converged reading and `adx_reading` / `adx_window` added.
+
+    🔴 SAME SPLIT AS THE RECHECK, AND FOR THE SAME REASONS (2026-07-30). The
+    ATR_LEN*3 fetch stays: `atr_pct` here is compared against
+    `entry_atr_pct_1h`, which execute_entry derives from its OWN ATR_LEN*3 1h
+    fetch, and vol_ratio / trend / ema_gap_dir were measured to be window-stable
+    (trend identical, ema_gap 0.3551 vs 0.3548 across 42 vs 200 bars). Only `adx`
+    was window-sensitive, and only `adx` moves — these three ADX values are what
+    the EXIT PROMPT prints as "Now: ADX1h=... ADX15m=...", directly under the
+    entry figure, and on the old window that pairing asserted changes that had not
+    happened.
+
+    Any failure -> {} for the TF's fields, or an AdxReading with value=None; never
+    raises, never touches the position."""
+    adx = indicators.adx_reading(exchange, symbol, tf)
     try:
         ohlcv = exchange.fetch_ohlcv(symbol, tf, limit=ATR_LEN * 3)
         m = indicators.compute_tf_metrics(ohlcv) or {}
         atr = m.get('atr')
         m['atr_pct'] = (atr / last * 100.0) if (atr is not None and last) else None
-        return m
     except Exception as e:
         print(f"[VIRTUAL] smart-exit {tf} metrics fetch failed [{symbol}]: {e}",
               flush=True)
-        return {}
+        m = {}
+    # The unconverged value from the 42-bar frame above is OVERWRITTEN, not
+    # merged: there must be exactly one `adx` in this dict and it must be the
+    # sanctioned one, so no downstream reader can pick up the old number.
+    m['adx'] = adx.value
+    m['adx_reading'] = adx
+    m['adx_window'] = adx.window
+    return m
 
 
 def _nearest_wall(walls, side_key, mid):
@@ -2034,9 +2171,14 @@
             "atr_change_pct, lux_volatility_entry, adx_1h, adx_15m, adx_5m, "
             "trend_15m_live, trend_5m_live, mom_flip_15m, mom_flip_5m, "
             "ema_gap_dir_1h_live, data_ok, would_wall_sl, wall_route, actual_sl, "
-            "wall_sl_dist_pct, actual_sl_dist_pct, wall_sl_tighter, wall_sl_breached"
+            "wall_sl_dist_pct, actual_sl_dist_pct, wall_sl_tighter, wall_sl_breached, "
+            # 🔴 the window the three adx_* values were computed on. Written on
+            # every new row so the exit prompt can REFUSE a cross-window
+            # comparison instead of implying one, and so any future cut of this
+            # table can tell the corrected rows from the 245 legacy ones.
+            "adx_window"
             ") VALUES ("
-            "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
+            "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
             (row['id'], entry_id, symbol, side, entry_regime, entry_gap,
              round(elapsed, 1), last, round(fav_now_pct, 4), round(mfe_pct, 4),
              round(giveback_pct, 4), armed, would_exit,
@@ -2052,7 +2194,8 @@
              m1h.get('ema_gap_dir'), data_ok,
              _r(would_wall_sl, 2), wall_route, _r(actual_sl, 2),
              _r(wall_sl_dist_pct, 4), _r(actual_sl_dist_pct, 4),
-             wall_sl_tighter, wall_sl_breached))
+             wall_sl_tighter, wall_sl_breached,
+             m1h.get('adx_window')))
 
     if first_fire:
         print(f"[SMART-EXIT-DRYRUN] would-exit {symbol} {side} "
--- a/titan-bot/main.py
+++ b/titan-bot/main.py
@@ -1315,11 +1315,21 @@
         # a snapshot price here).
         _snap = _request_snapshot() or {}
         _walls = microstructure.fetch_pre_trade_walls(exchange, symbol)
+        # 🔴 THE ENTRY ADX NOW TRAVELS WITH ITS WINDOW (2026-07-30). srv_adx_1h
+        # comes from indicators.fetch_snapshot, whose `limit` defaults to
+        # CANDLE_LIMIT == indicators.ADX_CANDLE_LIMIT — so the window is stated
+        # here from the same constant the producer used, not from a literal that
+        # would have to be kept in step by hand. This is the baseline the recheck
+        # compares against for the life of the position; sending it as a bare
+        # float is precisely how a 200-candle number came to be subtracted from a
+        # 42-candle one.
+        _entry_adx = indicators.AdxReading(_snap.get('srv_adx_1h'),
+                                           indicators.ADX_CANDLE_LIMIT, '1h')
         return virtual_trader.execute_entry(
             exchange, symbol, side, position_side,
             trades_entry_row_id=signal_row_id,
             pre_trade_walls=_walls,
-            entry_adx_1h=_snap.get('srv_adx_1h'),
+            entry_adx_1h=_entry_adx,
             # THE ONLY call site of execute_entry in the codebase. It is passed
             # explicitly rather than imported inside virtual_trader because
             # every other function in that module receives it the same way —
@@ -2673,13 +2683,42 @@
                                            f"4h={e['trend_4h']} 1h={e['trend_1h']} "
                                            f"ADX1h={e['srv_adx_1h'] or 0:.1f}")
             se = conn.execute("SELECT trend_15m_live,trend_5m_live,adx_1h,adx_15m,"
-                              "vol_ratio_1h,vol_ratio_15m,atr_change_pct "
+                              "adx_window,vol_ratio_1h,vol_ratio_15m,atr_change_pct "
                               "FROM smart_exit_dryrun_samples WHERE vpos_id=? "
                               "ORDER BY id DESC LIMIT 1", (vpos['id'],)).fetchone()
             if se:
+                # 🔴 THE PROMPT MAY NO LONGER IMPLY A CHANGE IT CANNOT SUPPORT
+                # (2026-07-30). This block renders directly under `At entry: ...
+                # ADX1h=<x>` beneath a heading that reads "Regime at ENTRY vs NOW",
+                # i.e. it asserts the two figures are two observations of one
+                # quantity. They were not: the entry side is srv_adx_1h on
+                # CANDLE_LIMIT and the sample side used to be ATR_LEN*3 = 42. On
+                # vpos 87 that printed a +11.9-point rise across 25 SECONDS which
+                # never happened, and the advisor duly reported "regime
+                # strengthened". Corrected samples now carry adx_window, so:
+                #   window == ADX_CANDLE_LIMIT -> same measurement, print it plainly;
+                #   anything else (incl. NULL on the 245 legacy rows) -> print the
+                #   figure RAW with its window named and say in words that no
+                #   rise or fall may be inferred.
+                # This is §2.19's precedent applied verbatim: a figure that cannot
+                # be compared is rendered with its provenance, not silently dropped
+                # and not silently used.
+                _sw = se['adx_window'] if 'adx_window' in se.keys() else None
+                _comparable = (_sw is not None
+                               and int(_sw) == indicators.ADX_CANDLE_LIMIT)
                 ctx['regime_now'] = (f"15m={se['trend_15m_live']} 5m={se['trend_5m_live']} "
                                      f"ADX1h={se['adx_1h'] or 0:.1f} "
                                      f"ADX15m={se['adx_15m'] or 0:.1f}")
+                if not _comparable:
+                    _wtxt = ('an unrecorded' if _sw is None else f"a {int(_sw)}-candle")
+                    ctx['regime_now'] += (
+                        f"\n  🔴 NOTE: the two ADX figures above were computed on "
+                        f"DIFFERENT candle windows — the 'At entry' value on "
+                        f"{indicators.ADX_CANDLE_LIMIT} candles and the 'Now' value on "
+                        f"{_wtxt} window. ADX(14) is doubly smoothed and reads far "
+                        f"higher on a short window, so these are NOT two observations "
+                        f"of one quantity: NO rise or fall between them may be "
+                        f"inferred. Judge the 'Now' figure on its own, or ignore it.")
                 ctx['volume_now'] = (f"vol_1h={se['vol_ratio_1h'] or 0:.2f} "
                                      f"vol_15m={se['vol_ratio_15m'] or 0:.2f} "
                                      f"ATR change vs entry={se['atr_change_pct'] or 0:+.1f}%")
--- a/titan-bot/sensor_events.py
+++ b/titan-bot/sensor_events.py
@@ -54,6 +54,7 @@
         entry_wall_mult REAL,
         wall_ratio REAL,
         adx_1h REAL,
+        adx_window INTEGER,
         adx_delta REAL,
         atr_pct_1h REAL,
         atr_delta_pct REAL,
@@ -95,6 +96,14 @@
     with sqlite3.connect(DB_PATH) as conn:
         conn.execute(_RECHECK_SCHEMA)
         conn.execute(_TRAIL_SCHEMA)
+        # 🔴 Additive migration (2026-07-30): the window every adx_1h below was
+        # computed on. NULL on the 38 legacy rows, all of which were written on
+        # the unconverged ATR_LEN*3 window — so any past analysis quoting
+        # recheck adx_1h or adx_delta is suspect and now says so in the data.
+        try:
+            conn.execute("ALTER TABLE recheck_events ADD COLUMN adx_window INTEGER")
+        except sqlite3.OperationalError:
+            pass  # column already exists
         conn.execute("CREATE INDEX IF NOT EXISTS ix_recheck_events_vpos "
                      "ON recheck_events(vpos_id)")
         conn.execute("CREATE INDEX IF NOT EXISTS ix_trail_events_vpos "
@@ -121,6 +130,13 @@
     sl_after is None for OK/EMERGENCY (no tighten happened); the caller passes the
     real post-write value for TIGHTEN. Layer 1 of the guard lives here: this
     function NEVER raises, so a logging fault cannot abort a recheck or a stop move.
+
+    🔴 `adx_1h` and `entry_adx` are indicators.AdxReading, NOT floats (2026-07-30).
+    `adx_delta` is derived through indicators.adx_delta(), which REFUSES across
+    windows — so the stored delta can no longer be a cross-window subtraction
+    presented as a market move, which is what the 38 legacy rows contain. The
+    window itself is stored in the new adx_window column, because a number whose
+    provenance lives only in the code is a number that goes stale silently.
     """
     if not SENSOR_EVENT_LOGGING_ENABLED:
         return
@@ -128,8 +144,16 @@
         ratio = (cur_wall_mult / entry_wall_mult
                  if (entry_wall_mult and entry_wall_mult > 0
                      and cur_wall_mult is not None) else None)
-        adx_delta = ((entry_adx - adx_1h)
-                     if (entry_adx is not None and adx_1h is not None) else None)
+        # Imported here, not at module scope: sensor_events is imported by both
+        # bots' engines and must stay import-light and side-effect-free.
+        import indicators
+        _cur = (adx_1h if isinstance(adx_1h, indicators.AdxReading)
+                else indicators.AdxReading(adx_1h, indicators.ADX_WINDOW_UNKNOWN, '1h'))
+        _ent = (entry_adx if isinstance(entry_adx, indicators.AdxReading)
+                else indicators.AdxReading(entry_adx, indicators.ADX_WINDOW_UNKNOWN, '1h'))
+        adx_value = _cur.value
+        adx_window = _cur.window
+        adx_delta = indicators.adx_delta(_ent, _cur)
         atr_delta = (((entry_atr_pct - atr_pct_1h) / entry_atr_pct * 100.0)
                      if (entry_atr_pct and entry_atr_pct > 0
                          and atr_pct_1h is not None) else None)
@@ -158,7 +182,8 @@
             'cur_wall_mult': cur_wall_mult,
             'entry_wall_mult': entry_wall_mult,
             'wall_ratio': None if ratio is None else round(ratio, 4),
-            'adx_1h': adx_1h,
+            'adx_1h': adx_value,
+            'adx_window': adx_window,
             'adx_delta': None if adx_delta is None else round(adx_delta, 3),
             'atr_pct_1h': atr_pct_1h,
             'atr_delta_pct': None if atr_delta is None else round(atr_delta, 3),
```

---

*Titan · 2026-07-30 13:45 UTC · HEAD `81875c9` (unchanged) · 🔴 LIVE · vpos 87 LONG open · patch WRITTEN AND VERIFIED, NOT APPLIED*
