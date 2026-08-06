#!/usr/bin/env python3
"""P2 — trail geometry grid, replayed on SOL's own book. READ-ONLY.

Discipline imported from Titan's canon §2.53 / §0.1 (METHOD, not numbers):
  §1a arming is READ from mgmt_state.breakeven_applied, never inferred (the inference
      is separately validated to reproduce the record 21/21, so it may be used for
      COUNTERFACTUAL b values where no record can exist).
  §1b the replay is TRUNCATED at the real close — samples already end before it, and
      whatever has not fired by then closes at the ACTUAL close price and time.
  §2  everything is denominated in R_ref = TODAY's 1R (2.5 x ATR x size), FIXED, so
      the grid cannot rank its own denominator. Fees are real dollars.
  §3  the trail is modelled AS THE ENGINE RUNS IT: trail_pct is a percentage OF THE
      ENTRY applied TO THE WATER MARK, so the giveback drifts with MFE.
"""
import sqlite3, json, statistics

DB = '/mnt/volume_nyc1_1780480650620/mercury-sol/trades.db'
FEE = 0.00055                       # BYBIT_TAKER_FEE_RATE
PARTIAL_FRAC = 1/3
CTRL_B, CTRL_T = 2.5, 1.0

c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
POS = [dict(r) for r in c.execute(
    "SELECT * FROM virtual_positions WHERE status='closed' ORDER BY id")]
PATH = {}
for p in POS:
    PATH[p['id']] = [(r[0], r[1]) for r in c.execute(
        "SELECT elapsed_s, price FROM position_excursion_samples "
        "WHERE vpos_id=? ORDER BY elapsed_s", (p['id'],))]


def replay(p, b, t, partial_on):
    """Return dict with usd pnl and the outcome label, or None if unresolvable."""
    e   = p['initial_fill_price']; a = p['atr']; s = p['size_full']
    long_ = p['position_side'] == 'LONG'
    m   = 1 if long_ else -1
    stop0 = e - b*a if long_ else e + b*a
    arm   = e + b*a if long_ else e - b*a
    trail_cb  = t * b * a
    trail_pct = trail_cb / e                      # fraction, of the ENTRY
    path = PATH[p['id']]
    if not path:
        return None

    entry_fee = e * s * FEE
    booked_partial = 0.0
    fees = entry_fee
    size = s
    stop = stop0
    armed = False
    wm = e
    for _, px in path:
        # 1) stop first — it is the protection and it is checked every tick
        if (long_ and px <= stop) or ((not long_) and px >= stop):
            exit_fee = px * size * FEE
            gross = (px - e) * size * m
            return {'usd': gross - fees - exit_fee + booked_partial,
                    'why': 'sl' if not armed else 'be/trail-stop', 'px': px}
        # 2) water mark
        wm = max(wm, px) if long_ else min(wm, px)
        # 3) arm once
        if not armed and ((long_ and px >= arm) or ((not long_) and px <= arm)):
            armed = True
            stop = e * (1 + 0.002*m)              # breakeven_target: entry +0.20%
            if partial_on:
                q = size * PARTIAL_FRAC
                pf = px * q * FEE
                booked_partial += (px - e) * q * m - pf
                fees += pf
                size -= q
            continue
        # 4) trail, only after arming — THE ENGINE'S FORM: pct of entry, on the wm
        if armed:
            trig = wm * (1 - trail_pct) if long_ else wm * (1 + trail_pct)
            if (long_ and px <= trig) or ((not long_) and px >= trig):
                exit_fee = px * size * FEE
                gross = (px - e) * size * m
                return {'usd': gross - fees - exit_fee + booked_partial,
                        'why': 'trail', 'px': px}
    # 5) §1b TRUNCATION — nothing fired; the position closes exactly as it really did
    px = p['close_price']
    exit_fee = px * size * FEE
    gross = (px - e) * size * m
    return {'usd': gross - fees - exit_fee + booked_partial,
            'why': p['close_reason'], 'px': px}


# size_full: vpos 25 stores the REMAINDER in `size`; the replay needs the original.
for p in POS:
    p['size_full'] = p['size'] + (p['partial_size'] or 0)
    p['R_ref'] = CTRL_B * p['atr'] * p['size_full']
    p['armed_rec'] = bool(json.loads(p['mgmt_state_json'] or '{}').get('breakeven_applied'))

SAMPLED = [p for p in POS if PATH[p['id']]]
print(f'positions: {len(POS)} closed · with a price path: {len(SAMPLED)} '
      f'· armed (recorded): {sum(1 for p in POS if p["armed_rec"])} '
      f'· armed AND pathed: {sum(1 for p in SAMPLED if p["armed_rec"])}')

# ── CONTROL VALIDATION ───────────────────────────────────────────────────────
print('\n=== CONTROL REPLAY (b=2.5, trail=1.0R) vs THE ACTUAL BOOK ===')
print(f"{'vpos':>4} {'reason':12s} {'actual$':>10} {'replay$':>10} {'d$':>9} {'dR_ref':>8}  {'why':12s}")
tot_a = tot_r = 0.0; deltas = []
for p in SAMPLED:
    part_on = (p['partial_size'] or 0) > 0
    r = replay(p, CTRL_B, CTRL_T, part_on)
    d = r['usd'] - p['net_pnl']
    deltas.append(d / p['R_ref'])
    tot_a += p['net_pnl']; tot_r += r['usd']
    print(f"{p['id']:>4} {p['close_reason']:12s} {p['net_pnl']:>10.2f} {r['usd']:>10.2f} "
          f"{d:>9.2f} {d/p['R_ref']:>8.3f}  {r['why']:12s}")
print(f"{'TOT':>4} {'':12s} {tot_a:>10.2f} {tot_r:>10.2f} {tot_r-tot_a:>9.2f}")
print(f"  median |dR_ref| = {statistics.median(abs(x) for x in deltas):.3f} R    "
      f"max |dR_ref| = {max(abs(x) for x in deltas):.3f} R")

# ═══════════════════ THE GRID ═══════════════════
BS = [2.0, 2.25, 2.5]
TS = [0.75, 1.0, 1.25]
COH = {'ALL-13': SAMPLED, 'ARMED-4': [p for p in SAMPLED if p['armed_rec']]}

ctrl = {}
for p in SAMPLED:
    ctrl[p['id']] = replay(p, CTRL_B, CTRL_T, (p['partial_size'] or 0) > 0)

def cell(b, t, partial_on, pool):
    out = []
    for p in pool:
        r = replay(p, b, t, partial_on)
        out.append((p, r, r['usd']/p['R_ref']))
    n = len(out)
    R = sum(x[2] for x in out)
    wins = sum(1 for x in out if x[1]['usd'] > 0)
    med = statistics.median(x[2] for x in out) if out else 0
    chg = sum(1 for p, r, _ in out
              if abs(r['usd'] - ctrl[p['id']]['usd']) / p['R_ref'] > 0.01)
    return n, wins, R, med, chg

print('\n\n' + '='*104)
print('THE GRID — everything in R_ref (TODAY\'s 1R = 2.5 x ATR x size, FIXED). '
      'ctrl = b2.5/t1.0')
print('='*104)
for pname, pool in COH.items():
    for partial_on in (False, True):
        print(f'\n--- cohort {pname} (n={len(pool)})  partial={"ON" if partial_on else "OFF"} ---')
        print(f"{'':6}" + ''.join(f'{"t="+str(t):>22}' for t in TS))
        print(f"{'b':6}" + ''.join(f'{"sumR   med   chg":>22}' for t in TS))
        for b in BS:
            row = f'{b:<6}'
            for t in TS:
                n, w, R, med, chg = cell(b, t, partial_on, pool)
                tag = ' *' if (b == CTRL_B and t == CTRL_T) else '  '
                row += f'{R:>9.2f}{med:>7.2f}{chg:>4d}{tag}'
            print(row)

print('\n\n=== PER SIDE (§4b) — sum R_ref, cohort ALL-13, partial OFF ===')
for sd in ('LONG', 'SHORT'):
    pool = [p for p in SAMPLED if p['position_side'] == sd]
    print(f'\n{sd}  (n={len(pool)})')
    print(f"{'':6}" + ''.join(f'{"t="+str(t):>12}' for t in TS))
    for b in BS:
        row = f'{b:<6}'
        for t in TS:
            n, w, R, med, chg = cell(b, t, False, pool)
            row += f'{R:>10.2f}{" *" if (b==CTRL_B and t==CTRL_T) else "  "}'
        print(row)
