# titan legacy fall-through refuses entries, close half untouched, structural proof

_2026-08-03 14:51 UTC_

---

# TITAN — THE LEGACY FALL-THROUGH REFUSES TO ENTER · APPLIED, LIVE, `489e0ac`

_2026-08-03 14:50 UTC · HEAD `489e0ac` (was `34dbdbf`) · LIVE, real money, **flat** · main.py only, +66/−22_

---

## DECISION LINE

**Applied.** `webhook()`'s legacy entry branch no longer calls `_execute_entry`. It logs loudly,
Telegrams the operator with the payload's `task`/`action`/`tf` **verbatim** and what to do about it,
stamps `status='unrecognised_payload_refused'` on the row, and returns 200 without trading.

**The close branch is untouched** — see (b): it is reachable by the same fall-through, it already has
its own live/paper guard, and refusing a close could strand an open position.

**Both prompts byte-identical (md5). §2.4 window untouched. Flat throughout.**

🔴 **One thing did not go to plan, and it changes what I can claim.** I fired an unrecognised payload
at the live bot to prove the guard end-to-end. **It never reached the guard** — the **HTF cascade
blocked it first** (`htf_blocked`, *"1H NEUTRAL (no active TREND signal)"*). Reaching the refusal
branch would have required setting a 1H TREND signal in the state machine of a live bot, **which I
did not do**. So the guard's proof is **structural, not behavioural**, and I am saying so rather than
implying a live test happened. Details and the exact proof in §3.

---

## (a) IS IT STRICTLY SAFER? — YES, AND HERE IS THE ARGUMENT RATHER THAN THE ASSERTION

**Yes. I agree, and the agreement is load-bearing on two measured facts, not on the intuition.**

1. **Behaviour today is unchanged, because nothing reaches the branch.** 0 of 65 positions came
   through it. Across every executed row in Titan's history, exactly **one** entry did — trade
   **181, 2026-05-11 21:13** — and it predates `virtual_positions` (earliest position row
   2026-05-17). Every `task` value in the retained journal (`price_action` 1067, `confirmation` 107,
   `exit` 2, `trend_catch` 1, `signal` 1) routes to a handler that returns first.
2. **If anything ever does reach it, the outcome strictly improves**: an alert instead of an
   unadvised, unbooked, unrechecked real-money position.

**The asymmetry is what makes it "strictly" rather than "probably":** the change can only convert an
*entry that would have happened* into an *alert*. It cannot suppress a close, cannot alter sizing,
cannot change any figure any advisor reads, and cannot block a path that any current alert takes.
There is no state in which the old behaviour was preferable to the new one — an entry taken with no
advisor, no order book and no recheck baseline is not a trade anyone chose to make.

**Where I would have disagreed, for the record:** if the branch had been a *live* route with real
traffic, refusing it would trade one failure mode for another (missed entries), and "strictly safer"
would have been wrong. It is not — and the measurement above is what establishes that, not the
reading of the code.

---

## (b) THE CLOSE HALF — CHECKED, AND LEFT ALONE

**Checked, and it stays untouched. Refusing it would have been LESS safe.**

The legacy block is `if is_close: <close> else: <entry>`. Both halves sit behind the same
fall-through. Evidence on the close half:

| check | finding |
|---|---|
| has it ever run? | **once** — trade **186**, `close_long`, 2026-05-11 21:18:16, the close of the one legacy entry. The 6 other advisor-less close rows are `15m_armed_exit` (`VIRT-CLOSE-*`) from a **different** path |
| does it already have a guard? | **yes** — an explicit `order_adapter.orders_are_real()` check added earlier, whose own comment reads: *"It is dormant — the state machine routes today's signals via P1/P2 — but 'dormant' is a property of the current alert format, not a guarantee."* |
| what would refusing it cost? | **a close that cannot execute leaves a position open.** That is a strictly worse failure than an unwanted entry |

🔴 **So: refuse entries, never closes.** A guard that can strand a live position is not a safety
feature. The close branch, its guard, and the shared tail below it are byte-for-byte unchanged.

**Proven, not assumed, that I did not break the close path.** The old entry branch assigned 13 names
the shared tail later reads. All 13 are **pre-initialised above the `is_close` split**:

```
sl_id, tp_id = None, None      sl_price = None       trail_pct = None      atr = None
total_amount = None            margin_required = None   size_capped = False   realized_risk_usdt = None
order / fill_price / fee_cost / amount   <- assigned inside the CLOSE branch itself
```

AST-verified: every one is bound on the close path, and `exchange.create_market_order` /
`create_order` remain reachable at lines 4476 and 4490.

---

## (c) PROMPTS AND THE WINDOW

```
entry prompt : 57951b81977c880a74fce5012ae95db7   before  ==  after
close prompt : 5cf1d59a70d729babe844070bf1f45ac   before  ==  after
```

Rebuilt from fixed inputs with the API stubbed, before and after. **Identical.** The change touches
one branch of one Flask route and no prompt-construction code. **The §2.4 window is untouched, not
voided, needs no restatement.**

---

## (d) THE ALERT — WHAT THE OPERATOR ACTUALLY RECEIVES

Rendered through `send_tg`'s real escaping, so this is the wire format:

```
🛑 UNRECOGNISED ALERT — ENTRY REFUSED
An alert reached the bot that no handler recognises. It would have opened a position
with NO advisor, NO order book and NO recheck baseline, so it was refused.
Nothing was traded.
💎 BTC/USDT:USDT  LONG
task:   __guard_test__
action: buy
tf:     None
What to do: either the TradingView alert is misconfigured (wrong task/action for what
it should do), or a handler is missing for a new alert type. Fix one of the two and it
will route normally.
```

Log line:

```
🛑 [P3-ENTRY-REFUSED] unrecognised payload reached the legacy entry path — NOT trading.
   symbol=BTC/USDT:USDT side=LONG task='__guard_test__' action='buy' tf=None
```

HTTP: `{"status":"unrecognised_payload_refused","reason":"no handler matched this payload; entry
refused","task":"…","action":"…"}` · row stamped `status='unrecognised_payload_refused'`.

**Hostile input degrades safely.** `send_tg` HTML-escapes everything and restores only
`<b> <i> <code> <pre>`, so a `task` containing `<script>x</script>` renders as
`&lt;script&gt;x&lt;/script&gt;` inside the code tag — visible text, no injected markup, no Telegram
400. Verified.

---

## 3. 🔴 WHAT I COULD NOT PROVE, AND WHY I DID NOT FORCE IT

**Attempted:** a live POST of `{"task":"__guard_test__","action":"buy","symbol":"BTC/USDT:USDT"}` to
the running bot — a deliberately synthetic task name so the operator could see it was a test.

**Result — it never reached the guard:**

```
HTTP 200  {"status":"htf_blocked","reason":"1H NEUTRAL (no active TREND signal)","penalized_score":-10.0}
journal:  WEBHOOK_IN tf=None action='buy' raw_body='{"task":"__guard_test__",…}'
          (no [P3-ENTRY-REFUSED] line — the branch was not reached)
after:    open positions NONE · vpos count 65 (unchanged) · newest row 21032 status='htf_blocked'
```

**The HTF cascade sits in front of the legacy block and stopped it.** Reaching the refusal would have
required setting a 1H TREND signal in the state machine of a **live, real-money bot**. **I did not do
that**, and I would not: manipulating trading state to exercise a guard is a worse risk than the one
the guard covers.

**So the guard is proven structurally, and that proof is the stronger kind here:**

| # | proof | result |
|---|---|---|
| 1 | `py_compile main.py` | ✅ |
| 2 | **`_execute_entry` has NO remaining call site in `webhook()`** (AST) | ✅ — the route cannot place an order at all, which is a stronger statement than "it didn't this once" |
| 3 | no dangling `entry` read (the `entry` at 4609 is a **different** variable, assigned by `lookup_entry_for_close` on the close path) | ✅ |
| 4 | every name the refusal branch uses is bound before it — `task_field`, `action_field`, `parsed`, `symbol`, `position_side`, `tf_arg`, `row_id` | ✅ no NameError risk (the 2026-07-29 class) |
| 5 | all 13 shared-tail names bound on the close path | ✅ |
| 6 | close-branch order calls still reachable | ✅ lines 4476, 4490 |
| 7 | refusal branch executed in isolation with real values | ✅ log line, Telegram text and HTTP body as shown above |
| 8 | both prompts byte-identical | ✅ md5 |
| 9 | four boot gates green after a deliberate restart from flat | ✅ 14:48:31 |
| 10 | no position opened by the live probe | ✅ still flat, vpos count 65 |

**An incidental finding from the failed probe, worth recording:** the **HTF cascade is a second layer
in front of this branch** — an unrecognised payload with no 1H TREND signal set is refused there
first. That is real protection, but it is **conditional on state-machine state**, not on the payload,
so it is not a substitute for the guard: with a 1H TREND signal live, the same payload would have
walked straight through to the entry.

**The old branch body was DELETED, not left unreachable under the `return`.** Dead code still reading
`entry[...]` would `NameError` the moment anyone removed the return — the 2026-07-29 class exactly, a
guard that does not protect the lines beneath it.

---

## WHAT CHANGED, AND WHAT DID NOT

| | |
|---|---|
| **Code** | `main.py` only, **+66/−22**, commit `489e0ac`, live since 14:48:31 UTC |
| **Snapshots** | `trades.db.bak_fallthrough_20260803` (integrity_check ok) · `main.py.bak_fallthrough_20260803` |
| **Close branch** | **untouched** — reachable, guarded, and left alone deliberately |
| **Advisor routing** | **not** attempted for unrecognised payloads — by design |
| **Prompts / §2.4 window** | byte-identical / untouched |
| **DB** | one row written by the live probe (21032, `htf_blocked`) — a log row, no position |
| **Position** | **flat** throughout |
| **§1d · §3 drift · §2.40/§2.41 · retire `entry_wall_baseline_mult`** | all still deferred per §2.42a |
