# sol-key-rotation-old-key-baseline-open-paper-short-blocked-on-new-credentials

_2026-08-07 00:03 UTC_

---

# Mercury-SOL key rotation — OLD-key venue baseline, the open paper SHORT, and the one thing missing

**2026-08-07 00:05 UTC · Mercury-SOL (PAPER, `MERCURY_OBSERVATION_MODE=1` — UNCHANGED) · Titan NOT TOUCHED**

## VERDICT UP FRONT

**The rotation is NOT done — the new key is not on this machine.** I searched every `.env`, every
recently-written file under `/root` and the mounted volume, and the whole box for a second Bybit
credential pair. There is exactly ONE Bybit key present and it is the OLD one. I will not invent
credentials, so steps 1–3 are **BLOCKED pending the new key/secret**.

Everything that did NOT depend on the new key is finished and is below — including a **read-only
venue baseline on the OLD key that independently proves why this rotation is necessary**, and the
full report on the open paper position.

🔴 **NO FLIP. `MERCURY_OBSERVATION_MODE=1` was not touched.** Nothing was written to the venue.
Nothing was ordered, cancelled or moved. The only write to disk was a `.bak`.

---

## 1. OLD KEY — VERBATIM FROM THE VENUE (`GET /v5/user/query-api`, over Tor)

Read live, not from the file. Key/secret never printed; identified by `sha256` prefix only.

| Field | Value from the venue | Verdict |
|---|---|---|
| `expiredAt` | `2026-08-13T18:32:09Z` → **2026-08-13 18:32:09 UTC** | **expires in 6 days** |
| `readOnly` | `0` | read-write |
| `ips` | `['*']` | 🔴 **NO ALLOWLIST** |
| `type` | `1` (personal) | — |
| `note` | `AI Mercury` | — |
| `uta` / `unified` | `1` / `0` | — |

Full permission set, verbatim:

```
Affiliate            []
BitCard              []
BlockTrade           []
ByXPost              []
ContractTrade        ['Order', 'Position']
CopyTrading          []
Derivatives          ['DerivativesTrade']
Earn                 []
Exchange             ['ExchangeHistory']
FiatBitPay           []
FiatConvertBroker    []
FiatP2P              []
NFT                  []
Options              ['OptionsTrade']
Spot                 ['SpotTrade']
Wallet               ['AccountTransfer', 'SubMemberTransfer']
```

**This is the baseline the new key has to beat, and it confirms the operator's reasoning exactly:**

- 🔴 `Wallet: ['AccountTransfer', 'SubMemberTransfer']` — **both money-moving permissions the
  rotation exists to remove are PRESENT on the key the bot is using right now.**
- `Withdrawal` — already absent. Good; the new key must keep it absent.
- `ips: ['*']` — no IP binding, which is also **why it carries a 3-month-style expiry at all**:
  Bybit only grants a non-expiring key once an IP allowlist is set. The 6-day remaining life is
  itself the tell.
- `ContractTrade ['Order','Position']` — present, so the bot can trade. Must stay.
- `Spot ['SpotTrade']`, `Derivatives ['DerivativesTrade']`, `Options ['OptionsTrade']` — kept
  deliberately by the operator. **Noted, not flagged.**

### The pass/fail card the new key will be held to
1. `expiredAt` empty/null (⇒ no expiry). If it still shows ~3 months, **the IP binding did not take.**
2. `readOnly == 0`.
3. `ips == ['<the droplet's public IP>']`, **not** `['*']`.
4. `AccountTransfer`, `SubMemberTransfer`, `Withdrawal` — **all three ABSENT**.
5. `ContractTrade` contains **both** `Order` and `Position`.

The audit script that produces this card is written and proven working against the old key — it
runs unchanged against the new one. It masks both secret values by construction.

---

## 2. WHERE THE OLD KEY LIVES — TWO FILES, NOT ONE

Compared by `sha256` of the values, never printed:

| File | Perms | Key hash | Secret hash |
|---|---|---|---|
| `/mnt/volume_nyc1_1780480650620/mercury-sol/.env` | `600` | `ba26b335dd39` | `19a4b3e137ea` |
| `/root/mercury-bot/.env` | 🔴 `644` | `ba26b335dd39` | `19a4b3e137ea` |

**Identical hashes ⇒ the same credential pair in both places.** The second file belongs to
**Mercury-ETH, retired 2026-06-03** — its service is stopped and disabled, but the file is
**world-readable (644)** and still holds a live, trade-enabled Bybit secret.

⚠️ **"The old key is gone from `.env` everywhere" therefore requires BOTH files.** Rotating only
mercury-sol's would leave the retired bot's copy behind. No other `.env` on the box
(`/root/.env`, `/root/titan-bot/.env`, `/root/trading_system/.env`, `x-bot`, `OpenClaw`) contains
any Bybit credential — checked, all clean.

**Snapshot taken (nothing edited yet):** `mercury-sol/.env.bak_keyrotation_20260806`, `600`,
byte-identical to `.env` (`cmp` clean).

---

## 3. THE OPEN PAPER POSITION — vpos 28

Straight from `virtual_positions`. Mark price `72.610` read live from Bybit (`retCode 0`,
`markPrice == lastPrice == 72.610`) at 00:00 UTC.

| | |
|---|---|
| **vpos id** | **28** |
| symbol / side | `SOL/USDT:USDT` · **SHORT** (`side=sell`) |
| **`is_paper`** | **1 — PAPER. No counterpart on the venue.** |
| entry (`initial_fill_price`) | **72.77** |
| size | 137.4 SOL (`margin_usdt` 2000 × `leverage` 5 — paper sizing) |
| opened | `2026-08-06T19:00:34.901Z` (~5h ago) |
| **stop (`sl_price`)** | **73.75** — still the original ATR stop (`original_sl_price` 73.75, unmoved) |
| **trail armed?** | 🔴 **NO** |
| `trades` entry row | 16405 |
| combo | `1H:Smart Trail Switch Bearish \| 15M:None \| 5M:Bearish New Imbalance` |

### Unrealised
```
gross            (72.77 − 72.610) × 137.4   = +21.984
entry fee        booked at entry            −  5.499
exit fee @ mark  modelled, not yet paid     −  5.487
                                            ──────────
NET unrealised                              = +10.998  ≈ +$11.00
```

### Why the trail is NOT armed — mechanism, not inference
- 1R = `SL_BUFFER_ATR` 2.5 × ATR(1h) 0.392987 × 137.4 = **$134.99**; entry−stop = 0.98 → matches
  the stored `initial_risk_usdt` 134.652.
- The trail and the breakeven lock arm **together**, at `active_price = fill − 1R = 71.7875`
  (`trail_arm.activation_distance`, `TRAIL_ARM_FIX_ENABLED=True`).
- `mgmt_state_json` = `{"breakeven_applied": false}`, and `virtual_trader._process_position` §4
  gates the trail on `if be_applied and trail_pct > 0`. **`be_applied` is false ⇒ the trail branch
  never runs.** `trail_pct` 1.017% is stored but **inert**.
- Best excursion so far: `water_mark` 72.29 = MFE **+$65.95 = 0.489R** — it has **never been
  within reach of the +1R arm**. Still `0.822` of downside away.
- Worst: `max_adverse_price` 72.95 = −$24.73 = −0.183R.
- `recheck_status='done'` — all three post-entry tiers (T+10/60/300s) passed `verdict=OK`, window
  closed, handed to the trail.

**So the only live trigger on vpos 28 is the hard stop at 73.75.** `MAX_POSITION_DURATION_MINS = 0`
⇒ **the timeout is DISABLED**, and `exit_pending` is empty. It will sit there until the stop is hit
or a signal closes it.

---

## 4. WHAT MUST BE TRUE BEFORE THE FLIP

Measured right now:

| Precondition | Required | **Actual** | |
|---|---|---|---|
| open `virtual_positions` | 0 | **1** (vpos 28) | 🔴 **BLOCKS** |
| `active_positions` | 0 | **0** | ✅ |
| `exit_pending` | 0 | **0** | ✅ |

`virtual_positions` tally: `closed/is_paper=1` = 21, `open/is_paper=1` = 1. **`is_paper=0` = 0 rows —
the live book is still empty.**

**Only vpos 28 stands between here and a flip.** Both other gates are already clean.

### One correction to the stated mechanism — the risk is real, the route is different
The concern was that the boot adopter would read the exchange, find it empty, see the open row and
block the side. **The adopter is not what does that.** `_load_active_positions_from_db()` opens with
`if not rows: … return` on `active_positions` — and `active_positions` has **0 rows**, so it returns
at the *"No active positions in DB — clean boot"* branch. It never calls `fetch_positions`, and
DOOR 3 / `_engine_owns_position` is never consulted. On a restart today the adopter does nothing at
all.

**What actually blocks the side is the per-side entry cap**, and it is worse than the adopter would
have been because it is silent and permanent:

- `virtual_trader._open_count()` counts `status='open'` rows for the symbol+side and **does not
  filter on `is_paper`**; `MAX_POSITIONS_PER_SIDE = 1`. The unique index
  `ux_vpos_one_open_per_side` enforces the same thing at the DB level.
- It is already firing — journal shows `ENTRY BLOCKED: SHORT already has 1/1 open virtual
  position(s)` at 19:25, 22:25, 22:25 and 23:25 UTC.
- Post-flip, **an `is_paper=1` row would keep occupying the SHORT slot and refuse every LIVE SHORT
  entry**, indefinitely — because `_is_paper()` is deliberately a property of the *row*, not the
  mode ("a row opened in paper keeps being managed as paper even if `OBSERVATION_MODE` is flipped
  underneath it"). So the paper row would never convert, never be adopted, and could only leave via
  its own stop at 73.75 — while silently vetoing the live short side the entire time.

**The operator's instruction not to flip is correct, and the stated precondition — zero open
`virtual_positions` — is exactly the right one.** Only the reason differs: it is the entry cap plus
the unique index, not the boot adopter.

---

## 5. 🔴 CAN THE KEY ROTATION DISTURB vpos 28? — **NO. CONFIRMED.**

Not "probably not" — here is the mechanism:

1. **The paper management path makes no authenticated call.** `_poll_once` →
   `exchange.fetch_ticker(symbol)`, plus `fetch_ohlcv` and local `*_to_precision`. These are
   **public** Bybit endpoints — nothing is signed, so the credential is irrelevant to them.
   `market_context` likewise goes out over Tor unauthenticated.
2. **The live branch is fenced off by the row, not the mode.** In `_process_position` the whole
   venue-reading block is behind `if not _is_paper(row) and _live_pos_state is not None`. vpos 28
   has `is_paper=1` ⇒ **that branch is skipped entirely.** No position read, no
   `_live_book_close`, no A6 unsubstantiated-close alert can involve this row.
3. **The one signed call on the restart path is `_smart_boot_cleanup` → `fetch_positions`**, and it
   is wrapped end-to-end: a credential failure prints `[SMART-CLEANUP] failed: … — DOING NOTHING to
   be safe` and returns. It cannot wedge the boot. It is also symbol-scoped, only fires when the
   venue reports FLAT, and targets `orderFilter=StopOrder` conditional orders — of which a paper
   row has none, anywhere.
4. **`fetch_balance` is not reached in paper** (`main.py:1441` returns early while
   `OBSERVATION_MODE` is on), so a new key cannot fail there either.
5. The position lives entirely in a **local SQLite row**. A rotation edits `.env` and restarts the
   process; the row is untouched by both.

**Worst realistic case if the new key were wrong: the restart logs a `[SMART-CLEANUP] failed` line
and paper trading carries on unaffected** — which is also precisely why this rotation is safe to do
*before* the flip rather than after.

The single caveat, stated plainly: a restart is required for the new credentials to load
(`config` reads its flags once at import — the deployment-gap class). During the seconds the worker
is down the poller is not ticking, so a stop-out at 73.75 would be detected on the next tick rather
than at the instant it crossed. On a paper row that changes a recorded fill price by a few cents at
most, and the position is currently **$11 in profit and 1.14 away from its stop**.

---

## 6. WHAT I NEED TO FINISH — one thing

The new key's **API key + API secret**. Safest handoff, so neither value lands in a chat transcript:

```
printf 'BYBIT_API_KEY=<new key>\nBYBIT_API_SECRET=<new secret>\n' \
  > /tmp/newkey.env && chmod 600 /tmp/newkey.env
```

Then, in one pass and reporting each result: rewrite both `.env` files in place (`.bak` for
mercury-sol already taken), re-run the venue audit against the new key and fill in the five-point
card in §1, restart `mercury-sol`, confirm from the boot line that `OBSERVATION_MODE=False` did
**not** appear and that a signed read reached Bybit over Tor, verify the old hashes are gone from
both files, and only then tell the operator to delete the old key on Bybit.

🔴 **Do not delete the old key on Bybit yet.** It is still the only credential the bot has; deleting
it now would leave Mercury-SOL with no working key. Delete it **only after** the new key passes the
restart-and-read check.

---

### Log of what this session actually changed
- Wrote: `mercury-sol/.env.bak_keyrotation_20260806` (600) — a snapshot. Nothing else.
- `.env` itself: **unmodified.** `MERCURY_OBSERVATION_MODE` still `1`.
- Venue: **read-only** — one `query-api` call and one public `tickers` call, both over Tor.
- Titan (`/root/titan-bot`, LIVE REAL MONEY): **not read, not touched.**
