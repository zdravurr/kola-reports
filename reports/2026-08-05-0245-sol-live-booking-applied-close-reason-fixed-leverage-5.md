# MERCURY-SOL — LIVE BOOKING APPLIED, CLOSE REASON MADE REAL, LEVERAGE SET TO 5

**2026-08-05 02:45 UTC** · Mercury-SOL, **still PAPER — NOT FLIPPED.**
One restart, **from flat**, worker pid **2217651**, booted 00:22:57 UTC.
**Titan untouched: HEAD `b9081ad`, tree clean, service active.**

---

# 🔴 THE PROOF THAT MATTERS FIRST: PAPER IS BYTE-IDENTICAL ON THE APPLIED TREE

The sandbox proof does not transfer to the live tree by itself, so the regression was re-run **against
the applied files** — a fresh copy of the real tree, DB path rewritten in all 13 modules, identical
pristine DB, frozen clock, identical stubs, the real `execute_entry`:

```
diff -u RA_base.txt RA_applied.txt   →   (no output)
✅✅ APPLIED TREE: paper mode BYTE-IDENTICAL to the pre-change baseline
```

| paper entry | before | after |
|---|---|---|
| size | 135.4 SOL | **135.4 SOL** |
| notional | $10,000 | **$10,000** |
| SL (`route=fallback_atr`) | 71.34 | **71.34** |
| **1R** | $338.50 | **$338.50** |
| trail_pct | 3.386 | **3.386** |
| `margin_usdt` stored | 2000.0 | **2000.0** |
| `is_paper` | 1 | **1** |

**Existing rows untouched: 21 total, 21 paper, 0 live, max id 27** — before and after, with no sandbox
row ever reaching the live DB.

---

# WHAT WAS APPLIED

## 1. The live path books a position (`is_paper=0`)

`virtual_trader.book_live_position()`, called from `_execute_single_entry` **after the stop is
confirmed** — the SL-failure branch emergency-closes and returns `None`, so a booked row always means a
position that is both OPEN and STOPPED. Values come from the venue (`_read_entry_fill`, `_resolve_fee`),
never from intent.

**It never refuses and never raises.** The money is already committed; declining to book would recreate
the gap with a live position nobody manages. Not gated on `MAX_POSITIONS_PER_SIDE` — that check belongs
*before* an order is sent. A unique-index rejection alerts loudly and returns `None`.

This restores in live: the **+1R partial**, the **breakeven arm**, **excursion sampling**, the **recheck
tiers**, **close accounting**, and the **daily-loss brake** — which until now summed an empty set and
would have read **$0 forever on real money**.

## 2. The daily-loss brake measures the book it protects

Scoped `COALESCE(is_paper,1) = ?`. Unfiltered it broke **both** ways, and the second is the dangerous
one: a paper **win masks a live loss and suppresses a halt that should fire**.

```
PAPER book today   pnl $ -300.00    -2.34R
LIVE  book today   pnl $   -3.25    -1.00R   ← what the live brake must see
UNFILTERED (old)   pnl $ -303.25    -3.34R   ← past the 3.0R limit → HALTS live trading
```

In paper this filter changes nothing today — 21 of 21 rows are already `is_paper=1`, which is precisely
why the regression came out identical.

## 3. Margin split — `MARGIN_USDT` deleted, not aliased

`PAPER_FIXED_MARGIN = 2000` · `LIVE_FIXED_MARGIN = 20` · `active_fixed_margin()` on `OBSERVATION_MODE`.
The old name was **removed entirely**: a constant that no longer decides anything is the "label doesn't
say what the thing is" defect, and leaving it would have been a trap for the next reader.

The entry card prints the ACTIVE figure — in live it must read `💵 $20 margin`. **If it ever reads
$2000, the split did not land.** Runtime now: `active_fixed_margin() = 2000` (paper), `MARGIN_USDT`
absent.

## 4. 🔴 FLAG (e) FIXED — the close reason comes from the venue

The caller booked **every** exchange-side exit as the literal `'sl'`, so a Bybit-native **trailing-stop**
exit would have been filed as a stop-out. `close_reason` is the axis every exit cohort in this book is
cut on — the 08-01 "the trail gives back exactly 1R" finding *is* such a cohort — so from trade one the
live R-distribution would have looked like a book of pure −1R stops with the trail invisible in its own
data.

**The mapping, stated explicitly:**

| venue field | value | → close_reason |
|---|---|---|
| `stopOrderType` | `StopLoss`, `PartialStopLoss`, `Stop` | `sl` |
| `stopOrderType` | **`TrailingStop`** | **`trail`** ← the one that was being mislabelled |
| `stopOrderType` | `TakeProfit`, `PartialTakeProfit` | `tp` |
| `stopOrderType` | `''` / absent | `exchange_market` — a manual close in the app is not a stop |
| `execType` | `BustTrade` / `AdlTrade` / `Settle` | `liquidation` / `adl` / `settlement` — **overrides** stopOrderType |
| `stopOrderType` | anything unrecognised | `exchange_<value>`, sanitised, logged, **never `sl`** |

A liquidation booked as a stop-out would hide the single most important event this book can record, so
`execType` deliberately wins over `stopOrderType`.

**Verified on 13 cases, including two unknown values:**

```
TrailingStop      Trade      -> trail                    ✅  🔴 THE ONE THAT WAS MISLABELLED
''                BustTrade  -> liquidation              ✅  LIQUIDATION
StopLoss          BustTrade  -> liquidation              ✅  liquidation overrides stop type
''                Trade      -> exchange_market          ✅  manual close in the app
SomethingNew      Trade      -> exchange_SomethingNew    ✅  unknown venue value
Weird/Type!       Trade      -> exchange_WeirdType       ✅  unknown, sanitised

non-stop exits that would still book as 'sl': 0  ✅ the corruption path is closed
```

`close_reason` is purely recorded — nothing in the codebase branches on it — so new distinct values are
pure information gain, checked before choosing them.

## 5. FLAG (b) FIXED — the alert no longer promises a recovery that does not exist

It said *"the next restart reconciles from the exchange."* It does not, and I proved that:
`_reconcile_open_virtual_positions` reads the DB only and never INSERTs, and
`_reconcile_active_positions` returns early on an empty table — exactly the state after this failure,
because `_register_active_position` is only reached after the function returns.

The alert now says **recovery is MANUAL** and gives three steps: check Bybit for the position, verify or
set a stop, then close it by hand or leave it stopped — and states plainly that **the bot will not
manage it and will not close it.** Text only, as instructed.

## 6. The partial card (kept, per your note)

Names its book and prints the **quantised lot actually realised** — `0.4 of 1.3` — instead of a nominal
`33%`, and no longer announces a real money-moving partial as `(paper)`.

---

# 🔶 RECORDED AS OPEN, DELIBERATELY NOT BUILT

| # | item | why |
|---|---|---|
| 1 | **Exchange-adoption path at boot** — nothing adopts a live position the DB never recorded | Separate piece with its own risk, same class as Titan's boot reconciler. At $100 the alert naming the state is sufficient. **Yours to decide.** |
| 2 | **`ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True`** — the +1R fresh-ATR trail recompute logs fresh-vs-frozen and keeps the FROZEN value, in **both** modes | Flag (c), left as you directed: not a live-specific gap, and an untested behaviour change does not belong in this flip. **Separate decision.** |

---

# ✅ P3 — VENUE LEVERAGE SET TO 5, BY HAND

```
BEFORE:  positionIdx=1 leverage=10   positionIdx=2 leverage=10
SET:     buyLeverage=5 sellLeverage=5  →  retCode=0 OK

READ-BACK (fresh call, not trusted from the set response):
  positionIdx=1 (LONG)   leverage=5   tradeMode=0 (CROSS)  size=0   OK
  positionIdx=2 (SHORT)  leverage=5   tradeMode=0 (CROSS)  size=0   OK
```

Done by hand deliberately: the per-entry `set_leverage` is wrapped non-fatal, so a single Tor 403 at
that moment would place the entry at whatever the venue held. **That is not hypothetical — a CloudFront
403 hit my own read-back and needed a fresh-exit retry.** The read above is the post-retry, independent
confirmation.

---

# RUNTIME CONFIRMATION (after the single restart)

| check | result |
|---|---|
| `OBSERVATION_MODE` | **True** — still PAPER, **not flipped** |
| ×20 ceiling | **20.0** |
| `NEWS_OBSERVATION_PINNED` | **True**, news withheld |
| `PAPER_FIXED_MARGIN` / `LIVE_FIXED_MARGIN` | **2000 / 20** · `active_fixed_margin() = 2000` |
| `MARGIN_USDT` removed | **True** |
| `book_live_position` present | **True** |
| **geometry** | `SL_BUFFER_ATR 2.5` · `TRAIL_MULT_ATR 2.5` · `ATR_TF 1h` · arm `5.0×ATR` · floor `0.25%` · partial `1/3` · `LEVERAGE 5` |
| geometry byte-check | **every geometry line byte-identical** to the pre-change snapshot |
| existing rows | **21 / 21 paper / 0 live / max id 27** — untouched |
| flat at restart | 0 open, 0 active, 0 pending — boot log: *"no open paper positions at boot — clean"* |
| file mtimes vs boot | 00:19:54 / 00:20:58 / 00:21:24 all **precede** boot 00:22:57 |
| **Titan** | **HEAD `b9081ad`, 0 changes, service active — untouched** |

---

# FILES TOUCHED

| file | change | snapshot |
|---|---|---|
| `config.py` | margin split, `MARGIN_USDT` removed, `active_fixed_margin()` | `.bak_livebook_marginsplit_20260805` |
| `main.py` | live booking call, brake scoped by book, live sizing, card, close-reason classifier, corrected alert | `.bak_livebook_marginsplit_20260805` |
| `virtual_trader.py` | `book_live_position()`, paper sizing/column, real close reason, partial card | `.bak_livebook_marginsplit_20260805` |
| `OPEN-ITEMS-SOL.md` | all of the above + the two open items recorded in canon | `.bak_20260805_0030` |

All `.bak` taken **before** editing; sandbox baselines md5-verified equal to the live tree before the
diff was copied in. `py_compile` clean on all three.

# WHAT I DID NOT DO

- **DID NOT FLIP.** `OBSERVATION_MODE` is still `True`. P4 (the key expiring 2026-08-13) is yours.
- Did not build the exchange-adoption path, and did not touch the trail-recompute flag.
- Did not touch Titan.
