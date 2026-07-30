# titan-confluence-bar-3-0-applied-live-verified-dee6cee

_2026-07-30 21:34 UTC_

---

# TITAN — THE CONFLUENCE BAR IS 3.0. APPLIED, LIVE, VERIFIED.

**2026-07-30 21:35 UTC · `dee6cee` · pushed · service restarted 21:26:34 · vpos 87 still open**

`CONFLUENCE_SCORE_THRESHOLD` **2.0 → 3.0**. One float. `CONFLUENCE_FLAT_THRESHOLD` untouched at 5.0.
Everything else in the commit is comments.

---

## DECISION LINE

**Shipped and verified.** The functional diff is exactly one value; `main.py` and `signal_matrix.py`
changed by comments only (proved below, not asserted). Pre-registration was written into
OPEN-ITEMS **§2.0 at 21:20, six minutes before the commit at 21:26:19**, so the predicted effect
cannot be restated after the fact.

🔴 **The runtime holds 3.0 — proved from the bytecode the process actually imported, not from a
sibling `import config`.** The `.pyc` header's source-mtime and source-size match `config.py`
exactly, the process started after it was written, and the stored constant disassembles to `3.0`.

🔴 **vpos 87 survived the restart with the identical exchange stop order id `2082799690256592896`,
confirmed on both probes, zero orphans.** The stop was not cancelled and not re-placed.

**One thing to flag rather than bury:** the change cannot affect the open position, and it will not
be observable at all until the next TREND signal reaches the score gate. **The first evidence that
the bar is doing anything is a `below_threshold` refusal at a gated score in `[2.0, 3.0)`** — a band
that produced zero refusals in the entire prior 30 days, because the old bar was beneath it.

---

## 1. THE DECISION, ON THE RECORD

Recorded verbatim in `config.py`, in the commit message, and in OPEN-ITEMS §2.0 — three places, so
no future session reconstructs it from the value alone.

1. **2.5 removes 0 of 23 trades — it does nothing. 3.0 is the smallest bar that binds at all.**
2. **3.5 is the cliff:** 10 of 23 trades. On the **RAW** scale the buckets `[2.75, 3.00)`,
   `[3.00, 3.25)` and `[3.25, 3.50)` are **empty**, so 3.0 and 3.5 refuse the *identical* 144
   events — **anything above 3.0 is bought with `total_gate_adj`, not with signal quality.**
3. 🔴 **The load-bearing evidence is NOT the n=11 cohort.** It is the skip-drift band split from the
   19:14 report: the **2.0–3.0** band drifted **−0.324%**/24h over n=93 (*refusing was right*); the
   **3.0–4.0** band drifted **+0.463%** over n=188 (*refusing was wrong*). **3.0 sits exactly on
   that boundary; 4.0 crosses it.** This is why §2's "+3.19R at bar 4.0 over n=5" did **not** decide
   this — and the commit message says so explicitly, so the n=5 number is not later mistaken for
   the reason.
4. **Structurally:** raw 2.25–2.75 means essentially **only the trigger scored**. A *confluence*
   gate that admits signals with no confluence is not doing what its name says.

**What 2.0 actually was**, now written at the constant so it is never rediscovered: not a low bar,
an **unreachable** one. Minimum raw TREND score 2.25 over 1,533 events. **The 27 refusals the ledger
credited to this gate were all carried under 2.0 by `total_gate_adj`** — the score gate was wearing
the macro gate's name.

### Why `CONFLUENCE_FLAT_THRESHOLD` was not touched

Left at 5.0 deliberately, and the reason is now a comment at the constant. The FLAT floor already
refuses **78.86%** of what it judges (705/894) against the TREND bar's 4.52% — **17× on the same
scale** — and the band it refuses most heavily, **3.0–4.0**, is the band whose refusals measured
**most costly** (+0.463%/24h, n=188). **Raising it is not a smaller version of this change; it is
the opposite one.** The stale note *"raise toward 6.5 later if chop still leaks"* is explicitly
**withdrawn** in the file, because it predates that measurement and would otherwise read as
standing guidance.

Also written at the constant: **do not raise the TREND bar above 5.0** without addressing the
inversion — past 5.0 the FLAT floor becomes a **discount** (a FLAT signal at 5.5 passes while a
TREND signal at 5.5 is refused). Not active at 3.0; observed rows that would flip: **0**.

---

## 2. PRE-REGISTRATION — written at 21:20, BEFORE the 21:26 commit

Committed to `kola-reports` as **`3e406c6`**, in OPEN-ITEMS **§2.0**. Reproduced here so this
document is self-contained.

| # | quantity | before | **predicted after** |
|---|---|---:|---:|
| 1 | refusal rate on TREND signals reaching the score gate | 4.52% (27/598) | 🔴 **15.72%** (94/598) |
| 2 | additional refusals per 30 days | — | 🔴 **+67** (≈**2.2/day**) |
| 3 | TREND trades removed, last 23 executed | — | 🔴 **3 of 23 (−13%)** — **vpos 68, 71, 78** |
| 4 | cap refusals that would have become trades | — | **5 of 75 (6.7%)** — small, not zero |
| 5 | `CONFLUENCE_FLAT_THRESHOLD` | 5.0 | **5.0 — deliberately unchanged** |

**REVIEW POINT — after 15 executed entries under the new bar.** Compare realised entry rate against
**15.72%** and outcomes against the pre-change book.
🔴 **If the entry rate diverges materially, that is a finding about the distribution — NOT a reason
to move the bar again.** Written into OPEN-ITEMS so the instinct is pre-empted by the record.

---

## 3. WHAT SHIPPED — and the proof it is only what I said

```
 titan-bot/config.py        | 53 ++++++++++++++++++++++++++++++++++++++++++----
 titan-bot/main.py          | 21 ++++++++++++++++++
 titan-bot/signal_matrix.py | 31 +++++++++++++++++++++++++++
 3 files changed, 101 insertions(+), 4 deletions(-)
```

**The entire functional diff**, `git diff` filtered to non-comment lines:

```diff
-CONFLUENCE_SCORE_THRESHOLD = 2.0  # virtual experiment 2026-05-20 (was 5.0)
-CONFLUENCE_FLAT_THRESHOLD = 5.0   # FLAT-regime floor 2026-07-06: enforce the
+CONFLUENCE_SCORE_THRESHOLD = 3.0  # TREND bar. Was 2.0 2026-05-20..2026-07-30.
+
+CONFLUENCE_FLAT_THRESHOLD = 5.0
```

`main.py` and `signal_matrix.py`, same filter applied: **empty output — comments only.** Nothing
outside `titan-bot/` is in the commit.

**Verification run before the commit:**

| check | result |
|---|---|
| `py_compile` | **38/38 modules OK** |
| symtable audit — names referenced in a FUNCTION scope but never bound there (the 29.07 naked-position shape) | **CLEAN — 37 files, 0 findings** |
| functional diff | **one float** |

---

## 4. 🔴 THE FIFTH LABEL DEFECT — WHAT I DID, AND WHY IT IS NOT A FIX

You asked me to either split `confluence_score` into distinct columns **or** document it precisely,
and to say which. **I documented it. I did not split it.**

**Why.** Splitting needs a schema migration **plus** edits to every reader —
`optimizer._bucket_confluence` (which buckets the column for the learning loop),
`claude_advisor`'s prompt builder (which puts the number in front of the LLM at every entry), and
`skip_attribution`. That is a **behaviour change on the live money path wearing a cleanup's
clothes**, and it would need its own verification cycle — while real money sits in an open position
and the standing rule is that a fix is proved in the same commit that ships it. Doing it tonight
would mean shipping the bar change and an unverified migration together, and if either misbehaved I
could not tell which. **Proposed, not done** — recorded as such in OPEN-ITEMS §0 rather than left
as an intention.

**What the documentation actually says**, at `signal_matrix.py`'s schema declaration (the one place
every reader passes) and at **all seven** `main.py` write sites:

| exit branch | what lands in `confluence_score` | sites |
|---|---|---|
| `below_threshold` | `_gated_score` = **raw + `total_gate_adj`** — what the gate compared | `:3709`, mirrors `:1911`, `:4245` |
| `risk_halt` | `direction_score` = **raw**; `macro_gate_penalty` left **NULL** | `:3809` |
| everything downstream | `adj_score` = raw + weight-engine adjustment, clipped ±1.5 | `:3898`, `:2216`, `:4482` |

The third is the trap, and `weight_engine.py:191–193` already said so in its own docstring — it just
said it somewhere nobody reading the column would look:

> *"`total_adj` is clipped to [−1.5, +1.5] and added to `direction_score` before storing as
> `confluence_score`. **Never applied to the gate check.**"*

**The rule now in the code:** reconstruct the score from `matrix_breakdown_json`, never from this
column. That JSON is assigned **once**, at `main.py:3678`, *before* the gate, identical on every
branch — it validates **660/660** exact on score and **898/898** exact on regime. And
`macro_gate_penalty` is **NULL on every `risk_halt` row**, so the gated score is not computable
there: say so rather than defaulting it to 0.

**Measured cost of not having had this**, stated in the code so the next person believes it: a
reconstruction assuming one meaning matched **645 of 1,531 rows — 886 mismatches**.

---

## 5. POST-CHANGE VERIFICATION — every item you asked for

| # | check | result |
|---|---|---|
| 1 | 🔴 **LIVE banner at $150** | ✅ `[ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX` · `LIVE_TRADING_ENABLED = True` · `ORDER_ADAPTER_LIVE = True` · `sizing: margin $30 x 5 = $150 notional per entry` |
| 2 | 🔴 **runtime = commit by hash** | ✅ tree **clean** (0 modified) ⇒ disk == HEAD `dee6cee`. Process start **21:26:34.338 UTC**; newest of **38** `.py` mtimes **21:23:08**; **0 files modified after process start** |
| 3 | 🔴 **`CONFLUENCE_SCORE_THRESHOLD` reads 3.0 at runtime** | ✅ **from the loaded bytecode** — see below |
| 4 | 🔴 **`CONFLUENCE_FLAT_THRESHOLD` still 5.0** | ✅ `5.0` in the same bytecode |
| 5 | 🔴 **four boot gates green** | ✅ all four, this process — see below |
| 6 | 🔴 **vpos 87 open, SAME exchange stop order id** | ✅ `2082799690256592896`, unchanged, both probes, 0 orphans |
| 7 | 🔴 **breaker untripped** | ✅ 0 `UNSAFE_STATE` / breaker trips, 0 tracebacks, 0 CRITICAL, 0 `REFUSING TO START` since restart |
| 8 | 🔴 **Mercury-SOL untouched** | ✅ active/running since **2026-07-21 06:39:33**, `NRestarts=0`, latest `.py` mtime **2026-07-05 23:13**, **0** files touched tonight |

### The runtime-constant proof, in full

A sibling `python3 -c "import config"` proves what is on **disk**, not what the **process** holds.
The `.pyc` is the artefact the interpreter actually imported, and CPython validates its header
against the source's mtime and size on every import:

```
__pycache__/config.cpython-312.pyc
  pyc header source-mtime : 2026-07-30T21:20:40 UTC
  pyc header source-size  : 47085
  actual config.py        : mtime 2026-07-30T21:20:40 UTC · size 47085
  header MATCHES current config.py : True
  pyc written             : 2026-07-30T21:23:50 UTC   (process started 21:26:34 — after)

  BYTECODE: CONFLUENCE_SCORE_THRESHOLD = 3.0
  BYTECODE: CONFLUENCE_FLAT_THRESHOLD = 5.0
```

The header matches, so the import was satisfied by this bytecode; it was written before the process
started; the stored constants disassemble to **3.0** and **5.0**.

### The four boot gates — this process (MainPID 461924), journal verbatim

```
[ORDER-MODE]    🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[ORDER-MODE]      LIVE_TRADING_ENABLED = True   ORDER_ADAPTER_LIVE = True
[ORDER-MODE]      sizing: margin $30 x 5 = $150 notional per entry
[RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 1 exchange position(s), 1 open row(s)
[RECONCILE]     LONG open, SL present @ 64028.8 — kept.
[RECONCILE]     engine owns positions — NOT enqueueing a breakeven job for LONG (item 12a: single owner)
```

### vpos 87 across the restart — both probes

| | pre-restart (21:26:30) | post-restart (21:30) |
|---|---|---|
| DB `stop_order_id` | `2082799690256592896` | **`2082799690256592896`** |
| unified `fetch_open_orders` | — | `2082799690256592896` `STOP_MARKET SELL posSide=LONG stopPrice=64028.8 workingType=MARK_PRICE closePosition=true status=NEW` |
| raw `swapV2/trade/openOrders` | — | **same id**, same stopPrice |
| unified `fetch_positions` | — | LONG 0.0023 @ 64838.7, `id 2082799688088776706` |
| raw `swapV2/user/positions` | — | **same positionId**, `positionAmt 0.0023`, `avgPrice 64838.7` |
| `sl_price` / `original_sl_price` | 64028.8 / 64028.8 | **64028.8 / 64028.8 — never moved** |
| orphan orders | — | **0** |

**Balance:** `USDT free 479.92 · used 29.83 · total 509.74`. Mark ~64728, uPnL **−$0.25**.

**Service:** `active (running)`, MainPID **461924**, `NRestarts=0`.

---

## 6. WHAT TO EXPECT, AND WHAT WOULD MEAN SOMETHING WENT WRONG

**Expect nothing immediately.** The bar only acts when a TREND signal reaches the score gate — about
**21 TREND events/day** reach it, and the new bar refuses roughly **2.2/day**. The open position is
unaffected: the gate is an *entry* gate and does not run on exits.

**The first positive confirmation** will be a `below_threshold` refusal with a gated score in
**`[2.0, 3.0)`**. That band produced **zero** refusals in the prior 30 days — the old bar sat
beneath it — so a single such row is unambiguous proof the new constant is in force on the live
path, in a way the bytecode check cannot be.

**What would indicate a problem, stated in advance:**

- A refusal at a gated score **≥ 3.0** on a TREND row → the threshold is being applied to the wrong
  quantity.
- A FLAT row refused at a gated score in **[5.0, ...)** → the FLAT branch was disturbed.
- `below_threshold` volume rising far above **≈2.2/day** above baseline → the distribution moved,
  which per the pre-registration is **a finding, not a trigger to change the bar**.

---

## WHAT I DID NOT DO

- **I did not touch `CONFLUENCE_FLAT_THRESHOLD`**, as instructed — and recorded *why* at the
  constant so it is not "tidied up" later by someone reading the two as a pair.
- **I did not split `confluence_score` into columns** — §4 says what I did instead and why. This is
  the one part of your request I deliberately took the narrower option on; the reasoning is above
  and the wider option is recorded as proposed in OPEN-ITEMS §0.
- **I did not re-run the distribution study.** Every number here is carried from the 21:12 report
  and the 19:14 report; nothing was re-derived and nothing was re-argued.
- **I did not change the HTF cascade, the LLM gate, the FLAT branch, or any risk halt** — the four
  mechanisms that do 93% of the refusing. This change moves a gate that was doing none of it.
- **I did not verify the bar on a live refusal**, because none has occurred in the four minutes
  since restart. That is the one claim in this report resting on the bytecode rather than on
  observed behaviour, and §6 states exactly what will settle it.

---

**Commits:** `dee6cee` (titan, pushed to `origin/main`, in sync) · `3e406c6` (kola-reports,
OPEN-ITEMS §2.0 pre-registration + §0 polysemy box).
