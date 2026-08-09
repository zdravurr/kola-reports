# sol-blind-ticks-closed-and-funding-booked-from-the-venue

_2026-08-09 17:30 UTC_

---

# Mercury-SOL — the blind ticks are closed on BOTH clients, and funding is read from the venue instead of ignored. The last two money-path gaps from the 15:40 register.

**Both applied, proven by execution in an isolated tree, ZERO leaks. Nothing restarted. vpos 30's
stored numbers untouched.**

- 🔴 **§1 `recvWindow` 5,000 → 20,000 ms, on BOTH clients.** The value is measured, not picked: over
  every `10002` this worker has logged, the observed worst case is **7,463 ms** and the median
  6,000. 20,000 is **2.7× the measured tail**. The retry client — the one that runs on a *fresh,
  unwarmed* Tor circuit, i.e. exactly when the outbound leg is slowest — is set in the same edit.
- 🔴 **§2 funding is READ from the venue, never modelled.** Its own column, not folded into
  `total_fees`. An unreadable venue books **nothing** and labels the row; it never books a zero.
- 🔴 **§2(c) the reconciliation is exact — and it required saying something the brief did not
  expect.** Funding alone does **not** bring vpos 29 to +$1.5779; it reaches +$1.5956. The residual
  **+$0.0177 is the pre-16:08 partial defect, not a funding error**, and the harness proves the
  identity closes on **1.5778666 exactly** once the partial leg carries the venue's own numbers.

```
PROOF BY EXECUTION: 33 assertions, 0 failed.  LEAKS: 0.  exit 0.
18 vectors rewritten by DIRECTORY (17 .py + .env). 0 residual prod-path literals.
main.py: +143 −0 (pure addition).  virtual_trader.py: +113 −6.  tor_retry.py: +12 −1.
```

Prior: [15:40 — the register](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1540-sol-first-night-live-the-close-reconciled-against-the-venue.md) ·
[17:00 — the first four](https://raw.githubusercontent.com/zdravurr/kola-reports/main/reports/2026-08-09-1700-sol-the-money-report-stops-lying-four-defects-fixed.md)

---

## 1. THE BLIND TICKS — `recvWindow`

### (a) The value, and the margin, from the measurement

I did not guess. Every `10002` the worker has logged since its 16:08:59 start carries both
timestamps, and their difference **is** how long the request took to arrive:

```
skew = server_timestamp - req_timestamp, over all 42 failures:

  n = 42
  min  5,000 ms   <- truncated BY CONSTRUCTION: under 5,000 the request SUCCEEDS
  p50  6,000 ms
  p90  6,930 ms
  p95  7,326 ms
  MAX  7,463 ms   <- the observed worst case
```

**Chosen: 20,000 ms — 2.68× the observed worst case.**

- **Why not 10,000.** Only 1.34× the measured tail, and the tail is set by Tor circuit quality,
  which degrades in bursts — the 42 failures arrived in clusters of up to 8. A margin that thin
  buys back the common case and loses the cluster.
- **Why not 60,000, which my own throwaway read script used.** That number was picked to get
  through on the first attempt; it was never sized to anything. Every extra second widens the
  replay window in §(c) for no measured benefit, so quoting it here would have been copying a
  convenience into production.
- **Verified accepted by the venue, not assumed:** a signed read with `recvWindow=20000` returned
  `retCode 0`.

🔶 **An interaction worth recording, because it bounds how useful any large value can be.** ccxt's
own HTTP timeout is 10,000 ms, so a request whose *round trip* exceeds that raises client-side
before any `10002` can come back. In practice that caps the useful range near 10 s. 20,000 is chosen
to sit clear of the measured tail without depending on an exact reading of `requests`' timeout
semantics — which are **per-socket-operation, not total-elapsed**, and therefore not a clean bound.

### (b) 🔴 BOTH CLIENTS — the trap that has bitten once already

`tor_retry.iso_exchange()` builds a **separate** `ccxt.bybit` per retry, and ccxt reads the window
from `self.options` at `sign()` time. A `recvWindow` set only on the primary would leave **every
Tor-retried request signed with the 5,000 ms default** — and a retry runs on a fresh, unwarmed
circuit, which is precisely when the outbound leg is slowest and a `10002` most likely.

**This is the identical trap that caught `acknowledged` on 2026-08-08**: fixed on the primary,
surviving in the retry path, invisible. Both are now set, and the harness checks the *object*, not
the source text:

```
✅ primary client sets recvWindow
✅ ISO retry client sets recvWindow too        iso.options['recvWindow']=20000
✅   ISO still carries the acknowledged option (not clobbered)
✅ recvWindow appears ONLY in the two client constructions — no gate reads it
     sites=['main.py:160', 'tor_retry.py:63']
```

### (c) 🔴 WHAT IT COSTS, STATED PLAINLY

`recvWindow` is **the interval in which the venue will still accept a REPLAYED signed request.**
Going 5 s → 20 s widens that window **4×**. That is a real cost and I am not going to bury it.

**Judged acceptable here, and the reason is the key's own permissions — read from the venue, not
assumed:**

```
ContractTrade  ['Order', 'Position']        Wallet     []      <- 🔴 EMPTY
Spot           ['SpotTrade']                CopyTrading []
Options        ['OptionsTrade']             Exchange    []
Derivatives    ['DerivativesTrade']         Earn        []
readOnly 0 · isMaster True · expiredAt 2026-11-07 · ips ['*']
```

🔴 **`Wallet` is EMPTY — no withdrawal and no transfer permission.** The worst a replayed request
can achieve is duplicating an order or a position action, and those are already defended by the
per-side entry gate, the `reduceOnly` flags and the idempotent write keys. **It cannot move money
off the account.**

**Stated honestly rather than favourably:** the key carries `ips ['*']` — no IP allowlist, because
Tor exit addresses rotate (the finding of 2026-08-06/07, where an allowlist and Tor were shown to
be mutually exclusive). So the replay window is the wider of the two exposures either way, and this
change makes the wider one wider still. With `Wallet []` the ceiling on that exposure is a duplicate
trade action, not a loss of funds.

### (d) `adjustForTimeDifference` is DELIBERATELY NOT SET — and the comment says why

```
timedatectl: System clock synchronized: yes · NTP service: active
```

The host clock is correct; **this is a latency problem, not a clock problem.** That option silently
re-bases every timestamp on the venue's clock, which would **paper over a genuine host clock fault
if one ever appeared** — turning a loud, greppable `10002` into a silent correction. The failure we
have is visible; the one it would hide is not.

```
✅ primary client does NOT set adjustForTimeDifference (checked on CODE, not comments)
     the token appears only inside the comment explaining why it is refused
✅ ISO does NOT set adjustForTimeDifference
```

That assertion is deliberately made against **comment-stripped source**. My first version of the
harness failed it — because my own comment mentions the token. An assertion about what the code does
must not be satisfiable, or breakable, by a comment.

### (e) 🔴 IT CHANGES HOW REQUESTS ARE SIGNED, NOT WHAT THE BOT DECIDES

`recvWindow` is consumed **only** by ccxt's `sign()`: it enters the auth payload and the
`X-BAPI-RECV-WINDOW` header. Proven by construction — signing the same request with 20000 and with
5000 produces **different signatures**, and the header carries the value:

```
✅ recvWindow is sent as X-BAPI-RECV-WINDOW          header=20000
✅   and the ccxt default it replaces really is 5000  default=5000
✅   it is part of what is SIGNED (changing it changes the signature)
✅ recvWindow appears ONLY in the two client constructions — no gate reads it
```

**No gate, no score, no geometry, no threshold, no prompt reads it.** Its only effect is that
requests the venue used to REFUSE are now ACCEPTED — which is exactly the 32 ticks where the trail,
the breakeven arm and the external-close detector could not evaluate.

---

## 2. FUNDING — READ, NEVER MODELLED

### (a) Where it is booked, and why NOT in `total_fees`

**Two additive columns on `virtual_positions`:**

```
funding_paid    REAL     the venue's own sum (positive = paid)
funding_source  TEXT     'venue' | 'unreadable' | NULL
```

🔴 **A separate column, not `total_fees`, and the reason is falsifiability.** `total_fees` means
**trading** fees, and the whole 1.82× understatement work of 2026-08-08 rests on being able to check
it against `size × price × taker_rate`. **Folding a funding charge into that sum destroys the only
arithmetic that can audit it** — a fee that no longer reconciles to a rate cannot be caught being
wrong again. Kept apart, both stay checkable *and* `net_pnl` can still be whole.

**`net_pnl` DOES include it** — that is the point of the fix, since the complaint was that every R
was slightly wrong. `total_fees` is left untouched:

```
✅ net_pnl is REDUCED by the funding paid                                   net=1.5956074
✅ total_fees does NOT absorb funding (it stays auditable against the rate)  0.1825202
```

**Three states, deliberately distinguishable.** A bare NULL would conflate *"no funding was
charged"* with *"we could not find out"* — the ambiguity that lets an unread number pass for a zero:

| `funding_source` | `funding_paid` | meaning |
|---|---|---|
| `'venue'` | the sum | read successfully; `net_pnl` includes it |
| `'unreadable'` | **NULL** | read FAILED; `net_pnl` EXCLUDES it; loud line |
| NULL | NULL | legacy row, or a paper position |

**Read, never computed.** Funding depends on the rate at each 8-hour stamp *and* on the size held at
that instant — which changes when a partial fires: vpos 30's first stamp was charged on 1.3 and its
later ones on 0.9. Any formula here would reconstruct two things the venue already knows exactly.

**Paper positions are never read**, by construction: there is no venue behind them, and inventing a
charge would make the paper book diverge from the thing it simulates.

🔴 **THE REAL READER, RUN AGAINST THE LIVE VENUE** — the strongest check available, and read-only:

```
$ _read_funding_paid('SOL/USDT:USDT', since=1786223420117)   # vpos 30's own opened_at
  [FUNDING] venue reports 3 funding record(s) since 1786223420117:
            total 0.02352016 (positive = paid)
```

It works. **And it found a third stamp** — at 15:20 UTC the execution list showed two
(0.00938353 + 0.0099229 = 0.01930643); the 16:00 UTC stamp added 0.00421373 on the reduced 0.9 size.
**vpos 30 has now paid $0.02352016 in funding, still unbooked, because the code is not loaded.**

### (b) 🔴 IT REFUSES RATHER THAN ESTIMATING

Every failure path books **nothing** and labels the row — an estimated funding charge is the same
defect class as an estimated fill, and the fee path already refuses to guess:

```
✅ venue UNREADABLE -> funding_paid stays NULL (never 0.0)
✅   labelled unreadable
✅   net_pnl EXCLUDES funding and is left exactly as before      net=1.6024798
✅   the card says UNREADABLE rather than printing a zero
✅ an adapter that RAISES cannot break the close
✅   and books nothing, labelled
✅ a PAPER position never calls the venue
✅   and both funding columns stay NULL
✅ a five-arg (pre-2026-08-09) adapter registration still closes cleanly
✅ the query is bounded by the position's OWN opened_at            since_ms=1786179014459
```

The log line the operator would see:

```
🔴 vpos=29 FUNDING UNREADABLE — net_pnl EXCLUDES funding and the row is labelled
   'unreadable'. Do not pool it with 'venue' rows in any fee or R study.
```

**The close card gets its own funding line**, because `net_pnl` now has funding subtracted and
printing only Gross and Fees would leave `Gross − Fees ≠ Net` on the operator's phone with nothing
to explain the gap — the same "two bases on one card" defect as P1 (vpos 25, $35.39):

```
💵 Gross P&L:  +$1.7850
💸 Total Fees: -$0.1825
💱 Funding:    -$0.006872  (venue)
💰 Net P&L:    +$1.5956
```

🔶 **A design coupling found by the harness and worth recording.** `_is_paper(row)` returns True
whenever `_live_close is None` — a documented fail-safe (*"a missing live adapter also means
paper"*). My funding gate sits behind it, so **funding is read only when a live close executor is
registered.** That is the correct coupling — no live adapter means no venue means no funding — but
it is load-bearing and was not obvious. My first harness run failed because it registered a `None`
close executor; the fix was to respect the contract, not to work around it.

### (c) 🔴 THE RECONCILIATION — and the number the brief expected is NOT reachable by this fix

The brief set the target: *"booked net + funding must equal the venue's `closedPnl` sum of
+$1.5779."* **It does not, and it should not.** Measured:

```
vpos 29, as it was ACTUALLY booked, + funding : 1.5956074
the venue paid (0.55954 + 1.0183266)         : 1.5778666
residual                                     : +0.0177408
```

**That residual is the PRE-16:08 partial defect, not a funding error.** vpos 29's partial ran 19
minutes before the fee/fill fix loaded, so it was booked at **76.36** against a venue fill of
**76.35**, with its exit fee at **0.00055** instead of **0.001**. Funding cannot reach it, and
absorbing it into a funding correction would be exactly the kind of quiet fudge this book keeps
removing.

**So the identity was proven the honest way — replay the same close with the partial leg carrying
the venue's own numbers:**

```
with the partial leg booked as the VENUE : 1.5778666
the venue paid                           : 1.5778666
✅ with venue-true inputs the identity CLOSES on the venue sum exactly
```

`gross 1.7810 − fees 0.1963 − funding 0.0068724 = 1.5778666`. **Exact to seven decimals.**

**What this proves:** the fix reaches the venue's number for every position booked under the current
code. vpos 29 cannot reach it because two of its inputs were recorded wrong before the code was
fixed, and that is a fact about vpos 29, not about this change.

### (d) 🔴 HISTORY IS NOT REWRITTEN — and the boundary is recorded

```
✅ §2(d) PROD has no funding column yet — nothing was rewritten there
✅   vpos 29 net_pnl in PROD is still exactly as booked      1.6024798000000064
✅   vpos 30 is still OPEN with net_pnl NULL                 ('open', None)
```

**THE BOUNDARY, so no study pools across it:**

```
vpos <= 29 (and vpos 30)   funding_source NULL — funding was NEVER READ and is NOT in net_pnl.
                           vpos 29 paid $0.0068724 unbooked; vpos 30 has paid $0.02352016
                           unbooked and counting.
first close after the      funding_source = 'venue'  -> net_pnl INCLUDES funding
next restart               funding_source = 'unreadable' -> it does NOT, and the row says so

🔴 NEVER pool 'venue' rows with NULL rows in any fee, net_pnl or R study. They are
   two different measurements wearing one column name. This is the same boundary
   discipline as the vpos <=29 / >=30 taker-fee split and the vpos <=28 / >=29 ADX
   window split — the third of its kind, and they must not be conflated with each
   other either.
```

---

## PROOF BY EXECUTION — 18 VECTORS, SEARCHED BY DIRECTORY

```
LAB: full tree copy, every prod-directory literal rewritten.
  residual "/mnt/volume_nyc1_1780480650620/mercury-sol" literals : 0
  residual "/root/titan-bot" literals                            : 0
  files rewritten : 17   + .env  => 18 VECTORS

LOCK (installed first, never lifted):
  sqlite3.connect        -> raises on any path under PROD or /root/titan-bot
  open(mode=w/x/a/+)     -> same
  sys.dont_write_bytecode = True
  the Telegram sender replaced by a stub that RAISES if called
  the live close executor replaced by a stub that RAISES if called

RESULT: 33 assertions ✅  0 ❌  LEAKS: 0  exit 0
```

**The DB guard the harness had to work WITH, not around:** re-opening vpos 29 for replay failed with
`UNIQUE constraint failed` until vpos 30 was closed first — `ux_vpos_one_open_per_side`, the partial
index that enforces `MAX_POSITIONS_PER_SIDE` at the DB layer, doing its job. Recorded because a
harness that had bypassed it would have been testing a state the bot cannot reach.

### The diff, and every deleted line accounted for

```
main.py            +143   -0     <- PURE ADDITION: nothing removed at all
virtual_trader.py  +113   -6
tor_retry.py        +12   -1

AST:
  main.py            added=[_read_funding_paid]  removed=[]
                     changed=[init_db, start_virtual_poller]
  virtual_trader.py  added=[_iso_to_ms]  removed=[]
                     changed=[_format_close_card, close_position, set_live_adapter]
  tor_retry.py       added=[]  removed=[]  changed=[iso_exchange]

The 7 deleted lines, in full:
  virtual_trader.py  the UPDATE's column list and its parameter tuple (2)
  virtual_trader.py  set_live_adapter's signature, one docstring line, its log line (4)
  tor_retry.py       the options dict line, reformatted to add one key (1)
```

`init_db` changed only by two entries appended to its additive-column list. `start_virtual_poller`
changed only by one keyword argument added to the adapter registration. **No geometry, no cascade,
no threshold, no prompt, no entry path and no exit decision was touched.**

Backups `*.bak_recvwin_funding_20260809_1730`, md5-verified identical before the first edit.

---

## 3. THE LOAD SPLIT — BOTH EDITS ARE ON DISK AND NOT LOADED

🔴 **Neither fix is running.** `main.py`, `virtual_trader.py` and `tor_retry.py` are all held in the
worker's memory from its **16:08:59** start. **vpos 30 is open, so nothing was restarted.**

**What that means concretely, said plainly so it is not a surprise:**

- The blind ticks **can still happen** until the restart. `recvWindow` is still 5,000 ms in the
  running process. There have been **0** `10002` errors since 16:00 today, but that is Tor being
  well-behaved for ninety minutes, not the fix working.
- If **vpos 30 closes before the restart**, its close will book **no funding** — it has already paid
  **$0.02352016** — and its `funding_source` will be NULL, placing it on the pre-fix side of the
  boundary in §2(d).

**The pending set is now TEN files — seven loaded, three standalone:**

```
PENDING (loaded by the bot — need a flat-book restart)
  config.py            2026-08-08 16:51        main.py           2026-08-09 17:28  <- NEW
  claude_advisor.py    2026-08-08 17:47        virtual_trader.py 2026-08-09 17:21  <- NEW
  skip_attribution.py  2026-08-08 17:47        tor_retry.py      2026-08-09 17:16  <- NEW
  trail_arm.py         2026-08-08 17:47

  optimizer.py         2026-08-09 16:48   (comment-only; also re-read per optimizer run)

NOT pending (standalone, re-read per cron run — ALREADY EFFECTIVE)
  naked_alert_resolver.py  2026-08-08 17:47
  silence_digest_sol.py    2026-08-09 16:51   <- the §4/§5 digest fixes, live at 08:20
```

---

## STATE

```
mercury-sol   active · pid 3533821 / worker 3533987 · since 16:08:59 · NRestarts=0 · NOT restarted
vpos 30       OPEN · 0.9 @ 76.29 · sl 76.44258 · wm 77.50 · net_pnl NULL · is_paper=0
              UNCHANGED BY THIS PASS · funding paid so far $0.02352016, unbooked
schema        PROD virtual_positions still has NO funding column — the migration runs at restart
tracebacks    0 since 16:08:59
venue         read-only calls only: key permissions, one recvWindow=20000 probe, one funding read
titan         active · pid 2538048 · NRestarts=0 · HEAD 897850b · git clean · NOT TOUCHED
```

**The 15:40 register is now empty.** All six defects it named — the paper-priced close card, the
VIRTUAL/paper labels on a live close, `close_reason=exchange_UNKNOWN`, the digest's permanent red
line, the blind ticks and the unbooked funding — are fixed, proven, and waiting on one flat-book
restart.
