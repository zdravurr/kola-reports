# 🔴 MERCURY-SOL IS LIVE ON REAL MONEY — flip executed 2026-08-07 22:25:18 UTC, from flat

**2026-08-07 22:45 UTC** · `/mnt/volume_nyc1_1780480650620/mercury-sol`
Preceded by: `2026-08-07-2230-sol-adx-window-fix-completed-quantified-proven-deployed.md`
Titan (`/root/titan-bot`): **untouched** — 0 changes, HEAD `897850b`, workers up since 2026-08-06
01:53, never restarted.

---

## THE FLIP

`MERCURY_OBSERVATION_MODE=1` → `0`. **That single line.** Backup `.env.bak_preflip_live_20260807`
taken first; the diff is exactly one line and nothing else moved:

```
8c8
< MERCURY_OBSERVATION_MODE=1
---
> MERCURY_OBSERVATION_MODE=0
```

Restart **from flat** at **22:25:18 UTC**. Master pid **3138228**, worker **3138270**.

---

## 1. FLAT CHECK, IMMEDIATELY BEFORE

**Database** — re-checked twice, the second time seconds before the restart:

| | |
|---|---|
| open `virtual_positions` | **0** |
| `active_positions` | **0** |
| `exit_pending` | **0** |
| max `virtual_positions.id` | **28** |

**Venue (Bybit, SOLUSDT, signed through Tor)** — the key answered cleanly, no `10010`:

| | |
|---|---|
| positions, **positionIdx 1** | size **0** |
| positions, **positionIdx 2** | size **0** |
| non-zero positions | **0** |
| open orders | **0** |
| **conditional / stop orders** | **0** |
| wallet | 811.90 USDT |

The bot then confirmed this independently at boot, without being asked:
`[BOOT-ASSERT] venue FLAT for SOL/USDT:USDT — no orphan possible`.

---

## 4. RUNTIME VERIFICATION — with `load_dotenv` FIRST

```
os.environ MERCURY_OBSERVATION_MODE = '0'
config.OBSERVATION_MODE             = False      <-- LIVE
```

🔴 **And the trap is worth restating, because it bit once already and it is *sharper* in this
direction.** I ran the bare import deliberately, in a clean environment: it also returned
`OBSERVATION_MODE = False` — the **right answer for the wrong reason**, because with no environment
it defaults to `'0'` → `False`. **A bare import says "LIVE" whether or not the bot is live. It is not
evidence in either direction.** The load-bearing evidence is `os.environ` reading `'0'` from the file
plus the running process's own boot line.

---

## 5. CONFIRMATIONS — all green

Boot line from the **running process**, not from an import:

```
[MERCURY-SOL][BOOT] geometry: SL_BUFFER_ATR=2.5 TRAIL_MULT_ATR=1.875 (0.750R) ATR_TF=1h
                    OBSERVATION_MODE=False [pid 3138270]
[MERCURY-SOL] [VIRTUAL] engine poller starting — LIVE adapter for NEW positions
```

| check | required | actual |
|---|---|---|
| boot geometry | `OBSERVATION_MODE=False` | ✅ **False** |
| engine adapter | live | ✅ `LIVE adapter for NEW positions` (was `PAPER`) |
| `LIVE_FIXED_MARGIN` × `LEVERAGE` | 20 × 5 = $100 | ✅ 20 × 5 = **100** |
| `active_fixed_margin()` | 20 | ✅ **20** |
| `PAPER_FIXED_MARGIN` | still 2000 | ✅ **2000** |
| `SL_BUFFER_ATR` / `TRAIL_MULT_ATR` | 2.5 / 1.875 (0.750R) | ✅ exact, in the boot line |
| ×20 wall ceiling | 20.0 | ✅ `ADVISOR_WALL_ALIGNED_V2_MULT_CEILING = 20.0` |
| `NEWS_OBSERVATION_PINNED` | True | ✅ **True** |
| venue leverage, both indices | 5 | ✅ idx1 = **5**, idx2 = **5** |
| 22 existing rows | still `is_paper=1` | ✅ `[(1, 22)]` — no row reclassified |
| Tor → Bybit | reachable | ✅ signed `fetch_positions` in 7.3 s |
| OKX direct, keyless | reachable | ✅ book in 2.3 s (bid 73.66 / ask 73.67) |
| tracebacks since flip | 0 | ✅ **0** |
| Titan | untouched | ✅ clean, HEAD `897850b`, workers never restarted |

`MAX_POSITIONS_PER_SIDE` = 1, `ATR_TF` = `1h` — unchanged.

---

## 6. STOPPED

**No trade was forced.** The bot is running, flat, waiting for its own signal. Max id is still 28;
the first live row will be **29** and will carry `is_paper=0`.

---

# 🔴 KNOWINGLY ACCEPTED, RECORDED BEFORE THE FIRST LIVE ENTRY

These are stated acceptances, not oversights. All three are now also in `OPEN-ITEMS-SOL.md`.

### a) SOL goes live with NO flat filter

Two candidates were measured on SOL's own book and **both were refuted**:

- **Titan's EMA envelope** — admits the chop and refuses the trend. It admits 0 of 9 LONGs (a side
  ban, not a filter), its two legs contradict each other on LONG, and decisively it **admits both
  real range entries (vpos 27, 28) and refuses the one that was not (vpos 26)**.
- **The ADX + range-width pair** — refuses the winners. Keeps 15 trades at −7.704R (win 20%),
  refuses 7 at +2.329R (win 71%): it would have made the book **worse by 2.33R**, discarding the two
  best SHORTs. ADX quartiles run backwards; on LONG the ADX leg is a structural no-op (all 9 LONGs
  had ADX ≥ 20). Nothing survives Bonferroni (α = 0.0056; best p = 0.0534, pointing the wrong way).

**The chop problem is real** — vpos 27 and 28 are genuine range entries that lost — **and it is
unfilterable at n = 2.** Going live without a flat filter is the deliberate choice. Neither candidate
should be re-proposed without new n.

### b) The corrected ADX now feeds the recheck TIGHTEN rules

Measured cost on the closed book: **≈0.5R, on vpos 17** — the one near-flat trade whose tightened
stop (76.66) sat inside its max adverse excursion (76.83). On the same book 9 of 66 tier verdicts
flip OK → TIGHTEN, **0 flip the other way**, and none can reach EMERGENCY (structural bound:
`_health_score` is monotone and `recheck_status='done'` implies every tier scored > −5).

🔴 **Live positions will now be tightened on tapes where they previously were not.** Unlike Titan's
equivalent, **SOL's TIGHTEN branch is not a no-op** — `_tighten_sl` really moves the stop to
midpoint(entry, SL) and commits it.

**WATCH, and flag immediately:** if an early live position is closed by a **recheck tighten** rather
than by its original stop, that is this change. Distinguishing evidence: `recheck_status='tightened'`
plus an `SL TIGHTENED` Telegram at T+10/60/300s preceding the close.

### c) Live-path mechanisms have never executed against Bybit

They were proven against fakes and mocks, never against the real venue. **`unmapped_close` and
`WriteUnconfirmed` firing is the mechanism WORKING, not breaking** — they are refusals, not faults,
and should be read as the safety net doing its job.

One related thing is deliberately unresolved and should not be forgotten: **M5's second line rests on
Bybit *enforcing* `orderLinkId`, which is UNPROVEN.** Only that the field is *accepted and
transmitted* was ever verified. Proving enforcement needs two real duplicate orders at the venue —
not an experiment worth running on a money path. The load-bearing guarantee is therefore the **venue
check before retry**, which assumes nothing about enforcement; `WriteUnconfirmed` refuses if that
check itself fails.

---

## Rollback

One line: `MERCURY_OBSERVATION_MODE=0` → `1` in `.env` (or restore
`.env.bak_preflip_live_20260807`), then restart **from flat**. Canon backup:
`OPEN-ITEMS-SOL.md.bak_preflip_live_20260807`. Note the mode is read at **import**, so the edit does
nothing until the restart — and a flip back must itself be taken from flat, or a live position is
left with no manager.
