# TITAN — THE REFUSAL LOOP DOES NOT EXIST HERE. THE GUARD IS NOT THERE, AND NEITHER IS THE INPUT.

**2026-08-06 15:45 UTC · Titan (LIVE REAL MONEY) · READ-ONLY. NOTHING WAS CHANGED.**

`openitems_guard` run first: **exit 0** — canon `OPEN-ITEMS.md`, runtime HEAD `897850b`, 11 watched
values, *"header and current-state table agree with runtime."* Proceeded.

Subject: `/root/titan-bot`, HEAD `897850b`, working tree **clean**, workers 2538048/2538082 up
**13 h 40 m** — not restarted, not modified, no file written.
Mercury-SOL: **not touched in this pass.**

---

## THE VERDICT FIRST

> ### 🔴 **Titan does not carry the guard. The question closes, and SOL's fix was local.**

Not "carries it but unreachable" — **the mechanism is absent entirely.** `Titan has no `_CLOSE_LABEL`.**
There is no dict, no `reason not in …` test, no `return None` on an unrecognised reason. And
independently, **the input that made the guard dangerous on SOL does not exist here either**: Titan has
no venue-derived exit classification of any kind.

**Two independent reasons, either one sufficient.** And a third: the passive-fill reconciler you
anticipated in §2c does exist, it runs *first*, and it makes Titan structurally immune.

---

# 1. DOES TITAN CARRY THE GUARD? — No. There is nothing to carry it.

## a) `_CLOSE_LABEL` and the opening of `close_position`, verbatim

```
$ grep -n "_CLOSE_LABEL" virtual_trader.py
(no output)
```

**There is no `_CLOSE_LABEL` in Titan.** The whole construct SOL's defect lived in is absent.

`close_position` is a different function with a different signature and a different job:

```python
def close_position(exchange, send_tg, symbol, position_side, reason='external'):
    """Close the open virtual position for (symbol, position_side). Returns
    the same dict shape as main._execute_close_position, or None if no open
    virtual position exists for that side."""
    row = _open_position(symbol, position_side)
    if row is None:
        return None
    try:
        last = float(exchange.fetch_ticker(symbol)['last'])
    except Exception as e:
        print(f"virtual close ticker fetch failed: {e}", flush=True)
        return None
    return _do_close(exchange, row, last, reason, send_tg)
```

Compare the signatures — these are not the same function wearing different names:

| | SOL | Titan |
|---|---|---|
| signature | `close_position(vpos_id, close_price, reason)` | `close_position(exchange, send_tg, symbol, position_side, reason='external')` |
| reason handling | looked up in `_CLOSE_LABEL`, **refused if absent** | passed through to `_do_close` **unexamined** |
| default reason | none — caller must supply | **`'external'`** |

**The two `return None` paths above are "no open row" and "ticker fetch failed" — neither looks at
`reason`.** I checked `_do_close` for a refusal path on the reason as well:

```
$ sed -n '1225,1300p' virtual_trader.py | grep -nE "return None|not in|raise|KeyError"
25:        return None
```

That single hit is line 1249, and it is **not** a reason guard:

```python
if _exit_fill is None:
    print(f"VIRTUAL CLOSE ABORTED vpos={row['id']}: adapter found no live "
          f"position to close; row left OPEN for reconciliation", flush=True)
    return None
```

That is the adapter finding no live position — and note the phrase **"left OPEN for reconciliation"**,
which is §2c's answer showing up on its own. More on it below.

`reason` is never validated. `_do_close` writes it straight into the ledger:

```python
"UPDATE virtual_positions SET status='closed', "
"close_price=?, close_reason=?, net_pnl=?, total_fees=?, "
"gross_pnl=?, funding_paid=?, closed_at=? WHERE id=? AND status='open'",
(close_price, reason, net_pnl, total_fees, ...)
```

**Any string is accepted and recorded verbatim. Titan cannot refuse a close because of its reason.**

## b) Every reason string Titan maps

**None — there is no map.** What exists instead is a closed set of literals at the call sites. Complete
enumeration of everything that reaches `_do_close`:

| reason | source | line |
|---|---|---|
| `sl` | poller stop-out | virtual_trader.py:2760 |
| `trail` | poller trail exit | virtual_trader.py:2776 |
| `breakeven` | passive fill, when `breakeven_applied` | virtual_trader.py:1211 |
| `sl` | passive fill, when not | virtual_trader.py:1211 |
| `post_entry_critical` | post-entry recheck emergency | virtual_trader.py:1925 |
| `ai_exit` | advisor exit | virtual_trader.py:2438 |
| `external` | **the default** — every `_execute_close_position` caller that passes nothing | main.py:1283, 1317 |

All six are **internal literals**. Not one is derived from the exchange.

---

# 2. 🔴 CAN A VENUE-DERIVED REASON REACH IT? — No. They do not exist in this codebase.

## a) Titan has no venue-derived exit classification at all

```
$ grep -rn "stopOrderType\|execType\|STOPTYPE\|BustTrade\|AdlTrade\|_classify_exchange_exit" --include=*.py .
(no output)
```

**Zero hits.** SOL acquired these strings on 2026-08-05 when `_BYBIT_STOPTYPE_TO_REASON` taught it to read
Bybit's own `stopOrderType`/`execType`. **Titan never grew that organ.** Where SOL asks the venue *how*
the position closed, Titan asks **its own row**:

```python
# EXIT REASON — the SAME order id is the ATR stop before +1R and the
# breakeven stop after it (move_stop cancels and recreates, then stores the
# new id in this column). Stamping every passive fill as 'sl' would file
# roughly-flat breakeven exits into the stop-loss bucket and make stops look
# better than they are — in the bucket we split outcomes by most often. The
# row already knows which it is.
_reason = 'breakeven' if bool(_mgmt.get('breakeven_applied', False)) else 'sl'
```

**The reason is derived from Titan's own recorded state, never from the venue.** That is the structural
difference, and it is why the six SOL strings are not merely unreachable here — they are unrepresentable.

## b) Every value that can reach `close_position`, live and paper, with mapping status

| value | live | paper | unmapped? |
|---|---|---|---|
| `sl` | ✅ | ✅ | **n/a — there is no map to be absent from** |
| `trail` | ✅ | ✅ | n/a |
| `breakeven` | ✅ (passive fill only) | ✗ (`orders_are_real()` false) | n/a |
| `post_entry_critical` | ✅ | ✅ | n/a |
| `ai_exit` | ✅ | ✅ | n/a |
| `external` | ✅ | ✅ | n/a |
| `tp`, `liquidation`, `adl`, `settlement`, `exchange_market`, `exchange_unreported` | **cannot occur** | **cannot occur** | **do not exist in Titan** |

**The "unmapped" column is not a list of survivors — the concept does not apply.** With no map, an
unrecognised reason is booked exactly like a recognised one.

## c) 🔴 LIQUIDATION, ADL, TAKE-PROFIT, MANUAL CLOSE IN THE BINGX APP — traced

**Your anticipated answer is the correct one: the passive-fill reconciler handles it before
`close_position` ever sees it.** `_reconcile_passive_fill` is the **first** thing the per-row poll cycle
does, and it short-circuits:

```python
if _reconcile_passive_fill(exchange, row, send_tg):
    return True
```

Its own docstring names the exact bug SOL just fixed, as history Titan already closed (item 13):

> *"The row stayed status='open' forever: no P&L, and `ux_vpos_one_open_per_side` blocked every later
> entry on that side. Live stalled after its FIRST trade while looking successful. That is the gate this
> function opens."*

The trace, per exit type:

**LIQUIDATION · ADL · MANUAL CLOSE IN THE BINGX APP · any exchange action** — position vanishes; the
reconciler confirms it is gone; `read_filled_protective_order` reports **our stop did not fill**; so:

```python
# 🔴 The position vanished but NONE of our orders filled. Something else
# closed it — manual intervention, liquidation, an exchange action. We
# do NOT know the exit price, and fabricating one would put invented
# numbers in the book. SHOUT AND DO NOT TOUCH (operator decision 13-I),
# leaving the row for a human.
    print(f"[VPOS-FILL] 🚨 vpos={row['id']} ... MANUAL ACTION REQUIRED.")
    send_tg("🚨 <b>POSITION GONE, STOP DID NOT FILL</b> ... "
            "<b>This also blocks new entries on this side. MANUAL ACTION REQUIRED.</b>")
    return False
```

**TAKE-PROFIT** — Titan **places no take-profit order**. `EQH_EQL_SMART_TP_ENABLED = False` (config.py:377),
and the code calls the Smart TP *"dead twice over, independently"*. `TAKE_PROFIT_MARKET` appears only in
defensive **cancellation** sweeps, never in placement. A TP exit cannot originate from Titan's own orders;
were one to exist from outside, it lands in the branch above.

**OUR OWN STOP OR TRAIL FIRES** — the reconciler reads the real fill price and fee off the filled order
and routes it through the *same* `_do_close` an active close uses, with `_reason` from the row's own
`breakeven_applied` flag. Booked normally.

### The honest nuance — same symptom, opposite character

For liquidation/ADL/manual close, Titan **also leaves the row `'open'`**, and it also blocks new entries
on that side through the same partial unique index. **The operational consequence overlaps with SOL's.**

But the character is opposite, and the difference is the whole point:

| | SOL (before the fix) | Titan |
|---|---|---|
| detection | one `print` per poll tick | 🚨 **Telegram alert** + `MANUAL ACTION REQUIRED` |
| intent | **accident** — a guard nobody revisited | **deliberate** — operator decision 13-I, on the record |
| why the row stays open | the close was *refused* | the exit price is **genuinely unknown** and inventing one would put fabricated numbers in the book |
| repeats | silently, forever | alerts, and the alert says it blocks the side |

**Refusing to book an exit you cannot price is correct. Refusing to book an exit you can price, because a
dict lacked a key, was the defect.** Titan does the first. SOL was doing the second.

---

# 3. THE SECOND, SMALLER QUESTION — it does not apply to Titan

**Does Titan pool `trail` into `sl_triggered_{s}` while `close_reason` keeps the literal? No — because
Titan writes no close label at all.**

```
$ grep -n "INSERT INTO trades" virtual_trader.py
(no output)
```

**Titan's virtual close path inserts no `trades` close row.** It back-fills the PnL onto the **entry** row:

```python
conn.execute("UPDATE trades SET pnl=? WHERE id=? AND pnl IS NULL", (net_pnl, entry_row_id))
```

and `pair_trades` is built for exactly that — its docstring: *"Match every open entry row to its
corresponding close row **(or itself when the PnL was written back directly onto the entry row by
virtual_trader / SL propagation)**."*

**So there is no `trades` label surface for a virtual close, and therefore no `trades`-vs-`virtual_positions`
divergence to have.** The single record of how a position exited is `virtual_positions.close_reason`, and
it carries the literal:

```
sl 28 · trail 15 · external 10 · ai_exit 6 · post_entry_critical 1     (60 closed, 0 open)
```

**`trail` is already a first-class, distinguishable cohort on Titan — 15 of them.** The thing G2c had to
repair on SOL was never broken here.

## 🔴 And a correction to my own 15:30 report

I inferred Titan's structure from a comment in **SOL's** `optimizer.py` claiming the close-type sets *"stay
byte-identical"* with Titan, and flagged that my adding `trail_*` to SOL had broken that identity.
**Reading Titan shows I read that comment too broadly.** The byte-identity claim attaches to
`_AMBIGUOUS_CLOSE_TYPES` — and those *are* identical on both bots:

```
Titan  _AMBIGUOUS_CLOSE_TYPES = {'5m_group_b','15m_armed_exit','smart_tp_close_eqh','smart_tp_close_eql'}
```

The **close-type sets were never identical**:

```
Titan  _CLOSE_LONG_TYPES  = frozenset(['close_long', 'exit_long'])          ← 2 entries
SOL    _CLOSE_LONG_TYPES  = [... 'sl_triggered_long', 'timeout_close_long'] ← 4, before my change
```

Titan's never contained `sl_triggered_*` at all, and Titan's `main.py` emits no such label.
**So the divergence I flagged at 15:30 already existed and my change did not create it**, the genuinely
byte-identical set is untouched, and — as you asked — **it does not matter for Titan**, which emits no
close label from the virtual path and so cannot drop one. The flag was over-stated; withdrawn.

---

# 4. VERDICT

> ## 🔴 Titan does not carry the guard. Say so plainly: **the question closes, and SOL's fix was local.**

Three independent reasons, any one of which alone would settle it:

1. **No `_CLOSE_LABEL` exists**, so no lookup can refuse or raise. `reason` is never validated and is
   written verbatim to `close_reason`.
2. **No venue-derived reasons exist.** Zero occurrences of `stopOrderType`/`execType`/`BustTrade`/
   `AdlTrade`/`_classify_exchange_exit`. Titan derives its exit reason from its own row state. The six
   SOL strings are not unreachable here — they are unrepresentable.
3. **`_reconcile_passive_fill` runs first and short-circuits**, so the exchange-side exits that would have
   fed such reasons are handled before the close path is reached at all.

**No fix is specified, because there is nothing to fix.** SOL's defect arose from a combination Titan
does not have: an enumerated label map *plus* an open set of venue-derived inputs. Titan has neither half.

### What would make it reachable — the one thing to watch

The defect becomes possible on Titan only if **both** halves are introduced together: a venue-exit
classifier feeding literal venue strings into `close_position`, **and** an enumerated map gating them.
Porting SOL's `_BYBIT_STOPTYPE_TO_REASON` pattern to BingX would supply the first half. On its own that
is still safe — Titan would record the new strings verbatim, exactly as it records `external` today.
**It only becomes a defect if a label map is added alongside it.** Recorded so that if BingX exit-type
classification is ever ported, this is a known precondition rather than a rediscovery.

### Ranking

**Not a live-money defect. Not latent-but-armed. Absent.** No entry in the canon's defect list is
warranted; this belongs in the record as a *closed question*.

---

# 5. WHAT I TOUCHED

**Nothing.**

```
openitems_guard  : exit 0 — header and current-state table agree with runtime
git status       : clean
HEAD             : 897850b        (unchanged)
workers          : 2538048 / 2538082, up 13 h 40 m — not restarted
positions        : 0 open (60 closed, 6 archived_pre_geometry_fix)
files written    : none
Mercury-SOL      : not touched in this pass
```

---

*Generated 2026-08-06 15:45 UTC. Read-only investigation of a live bot; no file modified, no service
restarted, no order placed.*
