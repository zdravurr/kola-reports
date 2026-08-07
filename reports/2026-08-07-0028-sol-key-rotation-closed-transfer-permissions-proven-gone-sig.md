# sol-key-rotation-closed-transfer-permissions-proven-gone-signed-read-live-over-tor

_2026-08-07 00:28 UTC_

---

# Mercury-SOL key rotation — CLOSED. All five points read from the venue, the transfer permissions are GONE and proven gone, signed reads live over Tor, vpos 28 watched again

**2026-08-07 00:28 UTC · Mercury-SOL PAPER · `MERCURY_OBSERVATION_MODE=1`, boot reads `OBSERVATION_MODE=True` · NO FLIP · Titan untouched**

## VERDICT: ROTATION COMPLETE AND VERIFIED

The allowlist was removed on Bybit at **00:23:52 UTC**, and every check that was unverifiable an hour
ago now reads clean from the venue. **The reason this rotation existed — killing the money-movement
permissions — is achieved and PROVEN, not assumed.**

---

## 1. THE FIVE-POINT CARD — ALL FIVE, VERBATIM FROM `GET /v5/user/query-api` OVER TOR

```
HTTP 200  retCode=0  retMsg='OK'
```

### (a) `expiredAt`
```
verbatim : '2026-11-07T00:23:52Z'
UTC      : 2026-11-07 00:23:52 UTC
          (91 days from now)
```
🔴 **Read this the right way round.** The original brief said a 3-month expiry would mean *"the IP
binding did not take."* That test is now **inverted and retired**: the binding is gone **by
deliberate decision** (§2 of the 00:20 report — it is what made the key unusable over Tor). So a
91-day expiry is the **expected, accepted** outcome, not a failure signal.

⚠️ **It is also a live commitment: this key dies 2026-11-07 00:23:52 UTC.** The stamp is `00:23:52` —
the same second the allowlist came off — so the clock was reset at that moment. **Put a calendar
reminder before 2026-11-07.** That is the whole price paid for a working key.

### (b) `readOnly`
```
readOnly : 0
```
✅ **Read-write. The bot can trade.**

### (c) IP allowlist
```
ips : ['*']
```
✅ Unrestricted — **as intended by the fix.** This is not the original target value
(`162.243.160.96`); that target was abandoned on purpose, because this bot reaches Bybit only
through Tor and Tor has no stable exit IP, while the droplet's own IP is CloudFront-blocked. Full
mechanism and both measurements: the 00:20 report.

### (d) 🔴 THE FULL PERMISSION LIST — THE POINT OF THE ROTATION
```
Affiliate            []
BitCard              []
BlockTrade           []
ByXPost              []
ContractTrade        ['Order', 'Position']
CopyTrading          []
Derivatives          ['DerivativesTrade']
Earn                 []
Exchange             []
FiatBitPay           []
FiatConvertBroker    []
FiatP2P              []
NFT                  []
Options              ['OptionsTrade']
Spot                 ['SpotTrade']
Wallet               []
```

**MUST BE ABSENT — all three confirmed ABSENT:**

| Permission | Old key | **New key** | |
|---|---|---|---|
| `AccountTransfer` | 🔴 PRESENT (in `Wallet`) | **ABSENT** | ✅ |
| `SubMemberTransfer` | 🔴 PRESENT (in `Wallet`) | **ABSENT** | ✅ |
| `Withdrawal` | absent | **ABSENT** | ✅ |

🎯 **`Wallet` is now the empty list `[]`.** The old key carried
`Wallet: ['AccountTransfer','SubMemberTransfer']`. **That is the rotation's entire purpose, and it is
now proven from the venue rather than assumed from the operator's intent.** Even if this key leaks,
it cannot move funds off the account or to a sub-account, and it cannot withdraw.

**MUST BE PRESENT — confirmed PRESENT:**
```
ContractTrade : ['Order', 'Position']
  Order    -> present ✅
  Position -> present ✅
```
✅ The bot can place orders and manage positions — the flip is not blocked by permissions.

**Kept by the operator, noted and NOT flagged**, exactly as instructed:
`Spot: ['SpotTrade']` · `Derivatives: ['DerivativesTrade']` · `Options: ['OptionsTrade']`.

**One unrequested difference worth recording:** `Exchange` went from `['ExchangeHistory']` on the old
key to `[]` on the new one. Harmless — a futures bot never reads convert/exchange history, and
nothing in the codebase calls it. Noted for completeness, no action.

Also: `note` changed `'AI Mercury'` → `'New mercury'`, `type: 1` (personal), `uta: 1` — confirming
this is a genuinely distinct key, not the old one re-edited.

---

## 2. RESTART — `OBSERVATION_MODE=True`, AND THE SIGNED READ LANDED

Restart at **00:25:33 UTC**. The boot lines, verbatim:

```
[MERCURY-SOL] [SMART-CLEANUP] No open positions for SOL/USDT:USDT — proceeding with orphan cleanup
[MERCURY-SOL] [BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h OBSERVATION_MODE=True [pid 2854383]
[MERCURY-SOL][VIRTUAL] poller started in pid 2854383 (interval=10s)
[MERCURY-SOL] [VPOS-RECONCILE] OPEN vpos=28 SHORT entry=72.77 sl=73.75 age=5.4h — poller continues managing it (no auto-close)
```

- ✅ 🔴 **`OBSERVATION_MODE=True` — NO FLIP.** Still paper, on a fresh pid.
- ✅ **Signed read over Tor CONFIRMED.** Both of those first two lines are authenticated V5
  `fetch_positions` calls **succeeding**. Compare the same lines while the key was IP-bound:
  `[SMART-CLEANUP] failed: … 10010 … — DOING NOTHING to be safe` and `[BOOT-ASSERT] venue read
  FAILED … state UNKNOWN. NOT claiming clean.` **The boot assert now claims clean, which it
  structurally cannot do without a successful signed read.**

**Two independent signed reads I ran myself over Tor, outside the bot:**
```
GET /v5/position/list  category=linear symbol=SOLUSDT  ->  retCode=0 'OK'   sizes = ['0','0']
GET /v5/order/realtime category=linear symbol=SOLUSDT  ->  retCode=0 'OK'   open orders = 0
```
✅ Read-write credential reaching Bybit through Tor. **Nothing was placed** — reads only.

⚠️ **Full disclosure on one write that is not mine.** `[SMART-CLEANUP] … proceeding with orphan
cleanup` means `_cancel_stop_orders` ran — a **symbol-scoped** `cancel-all orderFilter=StopOrder`.
This is pre-existing, documented, ungated-by-mode boot behaviour that fires on *every* restart; it
only ran tonight because the credential finally works. **It was a genuine no-op:** it only executes
when the venue reports FLAT, and my independent read confirms the venue holds **0 positions and 0
open orders**, so there was nothing to cancel. It cannot touch a paper row, and it is not account-wide.

---

## 3. TICKER POLL RECOVERED — vpos 28 IS BEING EVALUATED AGAIN

| Measurement, since the 00:25:33 restart | Result |
|---|---|
| `poll ticker fetch failed` occurrences | **0** |
| `retCode 10010` / `10003` occurrences | **0** |
| `position_excursion_samples` for vpos 28 | **547 rows, latest `2026-08-07T00:27:06`** |

**The excursion row is the proof that matters.** It is written at step 1d *inside*
`_process_position` — the same function that checks the stop, the breakeven and the trail. A fresh
sample timestamped after the restart means the position is being processed on the live path again.
It went 545 → 547 while I watched. **The 73.75 stop is armed and being tested every tick.**

That closes the failure named in the 00:20 report: no price ⇒ `_poll_once` did `continue` ⇒ no stop
check. Price is back, so the check is back.

### vpos 28 — still exactly where it was
| | |
|---|---|
| id / side | **28** · SHORT · `is_paper=1` |
| entry / size | 72.77 · 137.4 SOL |
| stop | **73.75**, original, unmoved — now **1.160 away** |
| `water_mark` / `max_adverse` | 72.29 / 72.95 — **unchanged all night** |
| trail | `{"breakeven_applied": false}` ⇒ **still NOT armed**; arms at 71.7875, needs 0.802 more |
| unrealised @ mark 72.59 | gross +24.73 − 5.499 entry − 5.485 exit = **+$13.75 net** (+0.183R, 1R = $134.99) |

Flip gates: open `virtual_positions` **1 (vpos 28) 🔴 still blocks** · `active_positions` **0** ✅ ·
`exit_pending` **0** ✅.

**Survived four restarts tonight byte-for-byte** — entry, stop, water_mark, max_adverse and
mgmt_state are identical to their 19:00 values. Nothing adopted it, nothing closed it, nothing
invented a fill.

---

## 4. FINAL STATE ON DISK

| File | Key | Perms |
|---|---|---|
| `mercury-sol/.env` | NEW (`sha256:bcfdaccea173` / `6457c7b9f51f`) | `600` |
| `/root/mercury-bot/.env` (retired ETH) | NEW, same pair | `600` (was 644 ✅) |
| `mercury-sol/.env.bak_keyrotation_20260806` | old (revoked) | `600` |
| `/root/mercury-bot/.env.bak_keyrotation_20260806` | old (revoked) | `600` |
| `/tmp/newkey.env` | **shredded** | — |

- Old key **gone from both live `.env` files** — verified by hash.
- `MERCURY_OBSERVATION_MODE=1` untouched throughout. No `.py` file modified. Titan not touched.
- **Nothing to do on Bybit:** the old key was already revoked at ~00:13 UTC (it went `retCode 0` →
  `10003 "API key is invalid"` mid-session). The 17 stale copies of it scattered in old scratchpad
  `.env` files and backups are **neutralised by that revocation** — worth a hygiene sweep, not an
  exposure.

## 5. WHAT IS STILL OPEN

1. 📅 **`2026-11-07 00:23:52 UTC` — this key expires.** Unavoidable consequence of dropping the
   allowlist. Set the reminder.
2. 🔴 **No flip.** vpos 28 is open, so the precondition (zero open `virtual_positions`) is unmet.
   `MERCURY_OBSERVATION_MODE` stays `1`. When it does close, the other two gates are already clean.
3. **Optional, if you ever want the allowlist back:** a stable egress IP in a country CloudFront does
   not block, routed instead of Tor — which would also retire the Tor fragility this bot lives with.
   Real infrastructure work, and a separate decision.
