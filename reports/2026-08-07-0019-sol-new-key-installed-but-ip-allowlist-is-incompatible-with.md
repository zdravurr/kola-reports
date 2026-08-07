# sol-new-key-installed-but-ip-allowlist-is-incompatible-with-tor-old-key-revoked

_2026-08-07 00:19 UTC_

---

# Mercury-SOL key rotation — the new key is installed and CANNOT AUTHENTICATE: its IP allowlist is incompatible with the bot's Tor transport

**2026-08-07 00:20 UTC · Mercury-SOL PAPER · `MERCURY_OBSERVATION_MODE` still `1` / boot says `OBSERVATION_MODE=True` · NO FLIP · Titan untouched**

## VERDICT

The rotation is **APPLIED** — new key in both `.env` files, both `600`, old key gone from both.
**Step 2 FAILED and cannot be made to pass from this host.**

🔴 **The new key is bound to an IP allowlist. Mercury-SOL reaches Bybit exclusively through Tor, so
its requests arrive from random Tor exit IPs — never from the allowlisted address. Every
authenticated call is refused with `retCode 10010 "Unmatched IP"`.**

🔴 **And the OLD key was revoked mid-session, so there is no working credential to fall back to.**
It answered `retCode 0` at 00:01 UTC and `retCode 10003 "API key is invalid."` at 00:13 UTC. I tried
the rollback; it restores a dead key. That door is closed.

**Consequence right now: Mercury-SOL has no authenticated Bybit access, and its Bybit price feed is
down with it.** Paper accounting is intact, no money is at risk, nothing was flipped, vpos 28 is
byte-for-byte unchanged — but the position is **not being evaluated**. Details in §4.

**One change on Bybit fixes everything — see §6.**

---

## 1. THE FIVE-POINT CARD — UNVERIFIABLE, and that is the finding

`GET /v5/user/query-api` on the new key, over Tor:

```
HTTP 200  retCode=10010  retMsg="Unmatched IP, please check your API key's bound IP addresses."
```

The venue refuses the call **before** returning any key metadata. So:

| # | Check | Result |
|---|---|---|
| a | `expiredAt` verbatim + UTC | ⛔ **UNREADABLE** — call refused |
| b | `readOnly == 0` | ⛔ **UNREADABLE** |
| c | allowlist `== 162.243.160.96`, not `['*']` | ⚠️ **PARTIAL** — see below |
| d | `AccountTransfer` / `SubMemberTransfer` / `Withdrawal` ABSENT; `ContractTrade [Order, Position]` PRESENT | ⛔ **UNREADABLE** |

**On (c) — what 10010 does and does not prove.** It proves an allowlist **exists and is not `['*']`**;
a wildcard key cannot produce this error. **The IP binding took.** What it does *not* prove is
*which* address is on it — reading that needs a successful `query-api`, which the binding itself
forbids. So "it is exactly `162.243.160.96`" is **not confirmed**, only "it is some specific
address, and this host is not it (via Tor)".

🔴 **(d) is the entire point of the rotation and it remains UNPROVEN.** I cannot confirm
`AccountTransfer`, `SubMemberTransfer` and `Withdrawal` are absent from the new key, nor that
`ContractTrade` still has `Order` and `Position`. It must be verified from the Bybit web UI, or by
API once §6 is done. **Do not treat the permission reduction as verified.**

For contrast, here is the **old** key read successfully at 00:01 UTC, before revocation — the
baseline this rotation was meant to improve on:

```
expiredAt  2026-08-13T18:32:09Z  (= 2026-08-13 18:32:09 UTC, 6 days)
readOnly   0
ips        ['*']
note       AI Mercury
Wallet     ['AccountTransfer', 'SubMemberTransfer']   <- the two the rotation targets
Withdrawal absent
ContractTrade ['Order', 'Position']
Spot ['SpotTrade'] · Derivatives ['DerivativesTrade'] · Options ['OptionsTrade']   (kept by design)
```

---

## 2. WHY AN IP ALLOWLIST CANNOT WORK HERE — the architectural conflict

This is not a misconfiguration, it is two requirements that exclude each other. Both halves measured
tonight:

**Half one — the droplet's own IP cannot reach Bybit at all.** Direct, no Tor:

```
HTTP 403   server: CloudFront
{ error: The A. CloudFront distribution is configured to block access from your country }
```

`main.py:73` documents exactly this: *"Bybit's infrastructure sits behind CloudFront which blocks
DigitalOcean's ASN; all outbound exchange calls are routed through Tor SOCKS5 proxy."*

**Half two — Tor is therefore the only transport, and it has no stable IP.** `main.py:76` builds the
ccxt client with `proxies={'https': 'socks5h://127.0.0.1:9050'}`, and `tor_retry.iso_exchange()`
*deliberately* rotates to a **fresh random exit** on every 403 (`IsolateSOCKSAuth`). Bybit allows a
handful of allowlist entries; Tor has thousands of exits, chosen per-circuit.

So: **the only IP that could be allowlisted is blocked by CloudFront, and the only IPs that can
reach Bybit are unpredictable.** An allowlisted key and this bot cannot coexist.

Proof that the transport itself is healthy and this is purely credential-side — the same Tor path,
unauthenticated, at 00:14 UTC:

```
{"retCode":0,"retMsg":"OK", ... "symbol":"SOLUSDT","lastPrice":"72.600","markPrice":"72.600" ...}
```

---

## 3. 🔴 CORRECTION TO MY EARLIER REPORT

In the 00:05 report I wrote that a bad credential could not affect paper management, because
"`_poll_once` → `fetch_ticker` is a **public** endpoint, so the credential is irrelevant to it."

**That was wrong, and the live restart disproved it.** ccxt's bybit client attaches the key to the
ticker request, and Bybit rejects it on the allowlist before serving it. Observed every tick:

```
[MERCURY-SOL][VIRTUAL] poll ticker fetch failed [SOL/USDT:USDT]: bybit {"retCode":10010, ...}
```

The reasoning was sound about *which code paths sign*, and wrong about *what ccxt actually sends*.
The lesson is the familiar one from this codebase: **a mechanism verified against a model of the
venue, not the venue.** I verified it against the venue and it failed.

Everything else in that report survives contact: the row is untouched, no bogus close was booked,
`_smart_boot_cleanup` failed safe exactly as described, and `fetch_balance` was never reached.

---

## 4. vpos 28 — UNCHANGED, BUT NOT BEING EVALUATED

Byte-identical across all four restarts tonight:

| | |
|---|---|
| vpos id / side | **28** · SHORT · `is_paper=1` |
| entry / size | 72.77 · 137.4 SOL |
| stop | **73.75** (original, unmoved) |
| `water_mark` / `max_adverse` | 72.29 / 72.95 |
| `mgmt_state_json` | `{"breakeven_applied": false}` ⇒ **trail still NOT armed** |
| unrealised @ 72.600 | gross +23.36 − 5.499 entry − 5.486 exit ≈ **+$12.37 net** |

Gates: **open `virtual_positions` = 1 (vpos 28) 🔴** · `active_positions` = 0 ✅ · `exit_pending` = 0 ✅.

**The engine confirms ownership at boot** — `[VPOS-RECONCILE] OPEN vpos=28 SHORT entry=72.77 sl=73.75
age=5.2h — poller continues managing it (no auto-close)`. Nothing tried to adopt, close or invent.

🔴 **But it is not actually being processed.** In `_poll_once`, the ticker read is the first step and
its failure does `continue` — which skips `_process_position` for every position on that symbol. No
price ⇒ **no stop check at 73.75, no breakeven test, no trail**. The position is frozen in place:
*safe, but unwatched.*

**The `via OKX fallback` lines in the log are not a rescue.** That fallback lives in
`post_exit_observatory.py` (the Five E. observational module) — it is not on the management path
and never feeds `_process_position`.

Paper, so no money is exposed. What it costs is fidelity: if SOL crosses 73.75 while this persists,
the paper stop-out is recorded late, at whatever price the first successful tick sees.

---

## 5. WHAT CHANGED ON DISK

| File | State | Perms |
|---|---|---|
| `mercury-sol/.env` | **NEW key** (`sha256:bcfdaccea173` / `6457c7b9f51f`) | `600` |
| `/root/mercury-bot/.env` (retired ETH) | **NEW key**, same pair | **`644` → `600` ✅ fixed** |
| `mercury-sol/.env.bak_keyrotation_20260806` | old key — rollback snapshot | `600` |
| `/root/mercury-bot/.env.bak_keyrotation_20260806` | old key — rollback snapshot | `600` |
| `/tmp/newkey.env` | **shredded** (`shred -u -z -n 3`, confirmed gone) | — |

- **Old key gone from both live `.env` files** — verified by hash, not by eye.
- `MERCURY_OBSERVATION_MODE=1` untouched; boot line reads **`OBSERVATION_MODE=True`** on every restart.
- No `.py` file was modified. Titan (`/root/titan-bot`) not read, not touched.
- 17 files elsewhere still contain the old secret (earlier sessions' test-isolation `.env` copies
  under `/tmp/claude-*/…/scratchpad/`, `.env.bak.A15C_20260608`, a `botuser` `history.jsonl`, plus
  the two rollback snapshots). **Its revocation has already neutralised all of them** — worth a
  cleanup pass for hygiene, no longer a live exposure.

---

## 6. THE FIX — one change on Bybit, then I finish in one pass

**Recommended, fastest: remove the IP allowlist from the new key** (set it back to unrestricted).

That sounds like giving up the win, but it isn't: **the allowlist was never what this rotation was
for.** The goal was dropping `AccountTransfer`, `SubMemberTransfer` and `Withdrawal` — and that is a
*permission* setting, entirely independent of the IP binding. Unrestricted + reduced permissions is
strictly better than what ran until tonight (unrestricted + both transfer permissions live).

The cost is the one noted in the first report: without an allowlist Bybit re-imposes a ~3-month
expiry. That is a calendar reminder, not a security hole.

**Proper long-term alternative, if you want to keep an allowlist:** give the bot a *stable* egress
IP in a country CloudFront does not block — a small VPS or a static-IP VPN — allowlist that one
address, and route Bybit calls through it instead of Tor. That would also retire the Tor fragility
this bot lives with (285 SOCKS retries and 26 CloudFront 403s in two days). It is real
infrastructure work and a separate decision; it is not a tonight fix.

**What I will do the moment the allowlist is lifted** (no `.env` change needed — the key is already
installed):
1. Re-run `query-api` and fill in **all five** points verbatim, including the permission list that is
   currently unproven.
2. Restart, confirm the boot line still reads `OBSERVATION_MODE=True`.
3. Confirm a **signed** read reaches Bybit over Tor — `fetch_positions` via `_smart_boot_cleanup`
   returning cleanly instead of `DOING NOTHING to be safe`.
4. Confirm the ticker poll recovers and vpos 28 is being evaluated against its 73.75 stop again.

⛔ **The old key needs no action — it is already revoked.** Nothing to delete, and nothing to restore
it to. If that revocation was not you, treat it as its own question.

🔴 **STILL NO FLIP.** vpos 28 is open, so the precondition (zero open `virtual_positions`) is unmet,
and on top of that there is now no working credential — a flip today would refuse every entry.
`MERCURY_OBSERVATION_MODE` stays `1`.
