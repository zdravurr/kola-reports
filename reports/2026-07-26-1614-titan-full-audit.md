# titan-full-audit

_2026-07-26 16:14 UTC_

---

# TITAN — FULL READ-ONLY AUDIT, 2026-07-26
Paper mode (LIVE_TRADING_ENABLED=False). No changes made this session. SOL not touched.

## PART A — OVERALL STATE

A1. FULL CURRENT BOOK (post-geometry-fix, vpos 33-81; 6 pre-fix rows archived, excluded)
Closed: 49 | Entries 2026-05-21 .. 07-24 | Closes 2026-05-22 .. 07-25 | 1 open (vpos 82)
  ALL    n=49  net= +739.40  win 22/49 (44.9%)  PF 1.36  avgW +126.15  avgL -75.41  median -4.52
  SHORT  n=28  net=+1595.88  win 16/28 (57.1%)  PF 2.67  avgW +159.55  avgL -79.74
  LONG   n=21  net= -856.48  win  6/21 (28.6%)  PF 0.21  avgW  +37.10  avgL -71.94
  SHORT vs LONG win-rate Fisher p=0.081 (directionally strong, not yet formally significant)

By exit reason: trail n=14 +2584.83 (14/14 win) | sl n=25 -1953.47 (1/25 win)
                external n=9 +105.30 | post_entry_critical n=1 +2.74
  => The whole book is: the trail captures, the stop bleeds. Zero losing trail exits.

A2. RECENT vs EARLIER — DEGRADING, and it is concentrated
  closes  1-10 (05-22..05-27)  -317.18  win 5/10
  closes 11-20 (05-28..06-09) +1647.16  win 9/10
  closes 21-30 (06-10..07-03)   +73.13  win 4/10
  closes 31-40 (07-03..07-11)  -380.40  win 1/10
  closes 41-49 (07-11..07-25)  -283.31  win 3/9
  Last 30d (from 06-26): n=22 net -967.55 win 4/22 PF 0.17
  Prior     (..06-26):   n=27 net +1706.95 win 18/27 PF 2.97
  Monthly: May +22.15 | Jun +1622.77 | Jul -905.52 (win% 19.0)

  CRITICAL CONFOUND — do not read July as a strategy failure. Era split by ENTRY time:
    E1 pre-wall-trail  (..07-02 23:28)  n=30 net +1403.11 win 18/30 PF 2.20
    E2 WALL-TRAIL LIVE (07-02..07-13)   n=11 net  -423.94 win  1/11 PF 0.01
    E3 post-wall-trail (07-13..)        n= 8 net  -239.77 win  3/8  PF 0.46
  E2 = the self-tightening stop, already reverted 07-13. In E2, 11 of 11 positions had the
  stop ratcheted and 11 of 11 would have SURVIVED at their original SL (max_adverse never
  reached the original stop in a single one). That is roughly -424 of pure self-inflicted loss.
  Honest verdict: real degradation exists (E3 still PF 0.46 on n=8), but ~half of the July
  drawdown is the wall-trail, not the entry model.

## PART B — DID THE FLAT-GATE FIX WORK
Fix db71454 applied 2026-07-06 13:54 (FLAT floor 5.0, TREND stays 2.0).

B1. CHOP/FLAT ENTRIES
  BEFORE: 4 FLAT-regime entries, ALL losers, net -306.42 (0/4), all exited on SL.
          vpos 61 SHORT score 4.25 -169.02 | 63 LONG 3.50 -45.57
          vpos 66 SHORT score 2.50  -59.11 | 67 LONG 3.50 -32.73
          Every one scored 2.50-4.25, i.e. every one is now below the 5.0 floor.
  AFTER (20 days): 0 FLAT-regime entries. Zero.

B2. IS THE GATE ACTUALLY BITING (not just an empty tape)? YES.
  FLAT signals rejected as below_threshold: 136 before (avg score 1.59) -> 497 after (avg 3.23).
  TREND below_threshold unchanged: 40 -> 10, avg score 1.47 -> 1.45 (bar untouched, as designed).
  ~370 extra FLAT signals in the newly-blocked 2.0-4.99 band were stopped in 20 days.

B3. DID IT CLIP THE TREND-SHORT EDGE? NO — the gate did not touch it, but the edge did fall.
  TREND SHORT before: n=15 net +2115.06 win 11/15 PF 8.03
  TREND SHORT after:  n= 5 net  -201.82 win  2/5  PF 0.37
  All 5 post-fix shorts scored above 2.0 and cleared the unchanged TREND bar — none were
  gated. The drop is market/other, NOT the gate. (Post-fix shorts are also all post-wall-trail
  disable, so they are clean of that confound too.)

B4. COUNTERFACTUAL ON THE BLOCKED BAND (forward drift; positive = the block cost us)
  Newly-blocked FLAT band (score 2.0-4.99): 1h +0.015% | 4h -0.031% | 12h +0.102% | 24h +0.240%
  n~390-401, 52-58% positive.
  Read: mildly positive, i.e. the gate is not perfectly free. But +0.24%/24h is far below the
  0.6-1.2% stop distance these entries carry, and the 4 real FLAT entries all died on SL.

B5. VERDICT: THE FIX WORKED. It stopped the chop bleed (4 entries / -306 -> 0 entries) and it
  demonstrably did NOT clip the trend-short edge (TREND bar untouched, zero shorts gated).
  Caveat: the trend-short edge collapsed anyway in the same window for unrelated reasons.
  Do NOT raise the floor toward 6.5 yet — the blocked band's drift is mildly positive, so a
  higher floor would start costing real money without evidence.

## PART C — EVERY WATCH-LIST SENSOR, CURRENT N AND STATUS

C4. ENTRY-TIME BOOK LOGGER (live 07-04) — sensor FIRED (threshold 6/side)
  Entries with BOTH corrected closed-candle vol_ratio_5m AND book snapshot: 18
    SHORT = 7 (all closed)   LONG = 11 (10 closed + 1 open)
  Sensor threshold met. BUT 9 of 18 (vpos 65-73) fall inside the wall-trail window, where the
  outcome was decided by a broken stop, not by the entry -> their win/loss labels are polluted.
  Clean-outcome n: SHORT 5, LONG 3.
  FINDING (SHORT, and it survives the cleanup): vol_ratio_5m separates perfectly.
    winners: 1.38 (+45.36), 1.54 (+75.24)
    losers : 2.42 (-73.09), 2.67 (-59.11), 2.98 (-116.58), 3.51 (-132.75), 5.70 (-4.52)
    Perfect rank separation, gap between 1.54 and 2.42. Fisher p=0.0476 at n=7.
    NOTE: this is a volume CEILING, not the "vacuum floor" we went looking for — high 5m
    volume at entry marks the loser, not low.
  LONG: 1 winner in 10. No usable signal on any book/vol field.

C5. COUNTER-SHORT FILTER (live 06-27) — REVIEW IS DUE, and the answer is: now HURTING
  Fills since go-live: 0.  Caution-eligible ai_skipped: 38.
  Skip rate in cohort 100% vs control other-SHORTs 98.2% (delta 1.8pp on n=38 — not attributable;
  we cannot prove the caution changed a single decision).
  Post-skip drift (positive = the skipped short WOULD have won):
    BEFORE go-live: 4h -0.150% | 12h -0.266% (20% positive) n=124  -> vetoing was correct
    AFTER  go-live: 4h +0.168% | 12h +0.956% (75% positive) | 24h +1.185%  n=27-38 -> vetoing costs
  The sign flipped. By date the flip is broad (07-07 +1.80, 07-08 +2.51, 07-12 +2.04, 07-19 +0.84),
  with one contrary day (07-18 -0.95). The study behind this filter was built entirely in a
  bear-1d tape; the tape turned bull on 07-10.
  VERDICT: RECALIBRATE, do not keep as-is, do not kill outright.

C6. BULL-REGIME WATCH — FIRED. Bull regime ARRIVED.
  trend_1d='bull' first appears 2026-07-10, 3041 rows over 15 days (07-10..07-24).
  Sensor fired 4 days running: N=457 / 462 / 338 / 157 vs threshold 30.
  Closed positions entered under trend_1d=bull: 6, ALL LONG, net -186.89, 1/6 win.
  DRIFT-CUT SCRIPT: runnable — I RAN IT (read-only, no writes, no TG). Result:
    cohort                        4h            12h            24h
    ALL htf_blocked LONG      +0.024 t+1.3   +0.076 t+2.9   +0.080 t+2.4   n=2178-2235
    trend_1h = bull           +0.087 t+3.0   +0.124 t+2.4   +0.151 t+2.1   n=323-356
    trend_4h = bull           +0.110 t+6.5   +0.256 t+8.6   +0.101 t+2.7   n=559
    trend_1d = bull           +0.024 t+1.4   -0.094 t-3.5   -0.192 t-4.6   n=786
    4h bull AND 1h bull       +0.153 t+4.3   +0.207 t+3.7   +0.174 t+2.9   n=176
  READ CAREFULLY: the ALL cohort also flipped positive (was -0.02..-0.33% in the bear tape).
  That means the raw metric is partly measuring BTC beta, not gate skill. Excess over ALL at 12h:
    trend_4h bull +0.180 | trend_1h bull +0.048 | trend_1d bull -0.170
  So the only cohort with genuine excess is trend_4h=bull. trend_1d=bull is NEGATIVE — the daily
  label is the wrong cohort. Magnitudes (+0.26%/12h) are small vs a 0.6-1.2% stop.

C7. CHOP-SHORT FLAT-GAP WATCH — STILL WAIT (N=1 of 5 new)
  Full cohort (SHORT, entry ema_gap_dir_1h='Flat' OR regime='FLAT'): n=6, net -500.10, 1 win (+0.78)
    vpos 33 +0.78 | 40 -103.86 | 53 -106.86 | 60 -62.03 | 61 -169.02 | 66 -59.11
  Control (all other closed shorts): n=22 net +2095.98, 15 wins.  Fisher p=0.0573.
  Only 1 new close since the marker (vpos 66) -> sensor correctly still silent.
  The separator HOLDS at n=6 and is nearly significant, but it has not been tested at larger N.
  STRUCTURAL POINT: the new FLAT gate covers only 2 of the 6 (61, 66 — regime=FLAT).
  The other 4 (-271.97) entered with regime=TREND and gap1h='Flat' — the gate does NOT see them.

C8. SMART-EXIT DRYRUN LOGGER — chop question STILL UNANSWERABLE
  170 samples / 21 positions (07-02 .. 07-26). Chop entries: only 3 (vpos 63, 66, 67), 12 samples,
  and ZERO of them ever armed -> zero would-exit events on any chop position. n=0 usable.
  INCIDENTAL TREND FINDING (n=3, all TREND, not the sensor's question):
    vpos 71 first would-exit at unrealised +32.48 vs actual close -30.78  (delta ~ +63)
    vpos 79 first would-exit at unrealised +147.15 vs actual +80.10       (delta ~ +67)
    vpos 81 first would-exit at unrealised +102.93 vs actual +75.24       (delta ~ +28)
  Simulated giveback-exit beat the real exit on 3/3, ~+158 gross total, before fees. n=3.

C9. PRIOR-MOVE LOGGER — the raw hypothesis is DEAD, the bucketed one is ALIVE
  55 records logged, 49 join to closed positions, 34 carry a real bucket.
  Continuous features at n=49 — ALL OVERLAP, no separation on either side:
    move_4h_fav_pct, move_12h_fav_pct, adx_15m_minus_4h, adx_1h, ema_gap_1h_pct
    (e.g. adx_15m_minus_4h: winners mean -2.42 range [-41.5,+17.7]; losers +4.29 [-27.3,+30.7])
  So "prior-4h move / ADX divergence as a threshold" is DISPROVEN at larger N.
  BUT the derived entry-timing bucket IS significant:
    early              n=21 net  +69.89 win 11/21
    mid/late/pullback  n=13 net -767.98 win  1/13     Fisher p=0.0107
    excluding the wall-trail window: early 10/15 +320.17 vs not-early 1/8 -594.32, p=0.0272
  "Titan enters late" is CONFIRMED — as a discrete bucket, not as a continuous divergence.

C10. BUG-1 RESCAN (same-second mixed direction) — CLOSED / DEAD
  Same-second mixed-direction signal events: 560 total, 333 AFTER the 06-25 atomic-capture fix.
  Of those 333, exactly ZERO reached a fill — all are htf_blocked / below_threshold / ai_skipped.
  Correlated same-second DOUBLE fills: vpos 28+29 (05-17), 43+44 (05-27), 48+49 (06-03).
  Last one is 06-03 19:30 — one day before the 06-04 unique-index fix. Zero in the 53 days and
  33 entries since. Larger N now exists and it is clean. No action.

C11. WALL-TRAIL — month verdict: correctly killed, but its FAILURE MODE IS STILL LIVE ELSEWHERE
  Live 07-02 23:28 -> disabled 07-13 01:55 (5f1b073).
  In that window: 11 closes, net -423.94, 1 win. 11 of 11 had the stop ratcheted.
  11 of 11 would have survived at the ORIGINAL SL (max_adverse never reached original stop on ANY).
  Since disable: only ONE trail-clip, vpos 74 — and it was NOT the wall-trail.
  vpos 74 was clipped by the POST-ENTRY RECHECK: recheck_events row, verdict TIGHTEN, score -5,
  reason = {"rule":"adx_below_floor","value":15.56,"threshold":20.0,"points":-5}. SL moved
  63489.3 -> 63103.6 (0.615% tighter); max_adverse 63119.8 — it would have survived the original SL.
  Cost: -73.09. The phantom-wall trigger was zeroed 07-13 (c845941), but the ADX-floor rule can
  still halve a stop with no distance ceiling. 1 TIGHTEN in 25 recheck events since 07-13, and
  that 1 destroyed the trade.
  ALSO NEW: order-book density collector is healthy — 19,174 snapshots since 07-13, mean span
  0.786%. Baseline now exists: max_wall_mult_ask p25=4.73 p50=5.98 p75=7.80 p95=14.13;
  imbalance p5=0.418 p50=0.485 p95=0.571; total depth p50=3012 BTC. This is the percentile
  baseline the bot never had. Only 9 entries overlap it so far — 2 of them (vpos 74 at ~96th pct,
  vpos 75 at ~99th) were the extreme-wall entries and both lost; the two lowest-percentile SHORT
  entries (24th, 29th) both won. Suggestive, n=9, not yet a rule.
  Adaptive-trail: 2 events, both dryrun (frozen placed), deltas -0.241 / +0.160. Observational only.

## PART D — WHAT IS READY, AND IN WHAT ORDER

D12. ITEM-BY-ITEM

  READY TO APPLY NOW
  R1. Recheck TIGHTEN stop-move (from C11). n=1 of 1 observed TIGHTEN and it cost -73.09 on a
      trade that would have survived. Same family as the wall-trail that already cost -424.
      Action: make TIGHTEN advisory/log-only, or floor the new SL at the original SL distance.
      Highest EV / lowest risk change on the list.
  R2. Prior-move bucket as a soft advisor caution on mid/late/pullback entries (C9).
      n=34, Fisher p=0.011; p=0.027 with the wall-trail window removed. Advisory, not a veto.
  R3. Bull-regime drift-cut — ALREADY RUN this session (C6). Decision available now:
      relax the LONG cascade ONLY in trend_4h=bull (excess +0.18%/12h over baseline), NOT in
      trend_1d=bull (excess -0.17%). Given LONG's realised PF of 0.21 and that Op-X was already
      reverted once (e589e97), ship this in DRYRUN first.

  READY AS SHORT-SIDE SOFT ADVISORY (not a veto)
  R4. vol_ratio_5m ceiling ~2.0 on SHORTs (C4). Perfect separation, p=0.048, but only 2 winners.
      Advisory caution only. Needs 2-3 more SHORT winners before it can gate.
  R5. Recalibrate the counter-short filter (C5): condition it on trend_1d != bull, i.e. restore it
      to the regime it was measured in. Currently it is a live, unmeasurable, mildly -EV drag.

  STILL WAIT
  W1. gap=Flat chop-short caution — n=1 of 5 new (C7). Need 4 more chop-short closes.
  W2. Smart-exit chop giveback — 0 armed chop samples (C8). Need ~5 chop closes that arm.
  W3. Order-book percentile veto — baseline excellent (19k snapshots) but only 9 entries
      overlap it (C11). Need ~15-20 entries, i.e. roughly 4-6 more weeks at the current rate.
  W4. TOLN short cohort n=1-2 of 6. regime_flat_high_adx n=0 of 12. Both untouched, both silent.
  W5. Smart-exit on TREND positions — new hypothesis from C8, n=3, +158 gross. Promising, too thin.

  DEAD / DISPROVEN
  X1. Prior-move as a CONTINUOUS threshold (prior-4h move, ADX 15m-4h divergence): fully overlapping
      at n=49, both sides. Kill this framing; keep only the bucket (R2).
  X2. Wall-trail live ratchet: 11/11 self-clipped, already off. Keep as observation only.
  X3. Bug-1 mixed-direction race: 333 post-fix opportunities, 0 leaks, 0 doubles in 53 days. Closed.
  X4. LONG-side entry factors from the book logger: 1 winner in 10. No signal on any field.
  X5. trend_1d='bull' as the Op-X trigger cohort: NEGATIVE excess drift. The daily label is wrong;
      the 4h label is the one that carries signal.

D13. CONFLICTS — APPLY IN THIS ORDER, DO NOT STACK

  CONFLICT 1 (real, and it is the important one): THREE SHORT-SIDE DAMPENERS ON ONE THIN EDGE.
    vol5m ceiling (R4) + counter-short filter (R5) + gap=Flat caution (W1) all suppress SHORTs.
    SHORT is the ONLY profitable side of this book (+1595.88 on 28 closes). Stacking three filters
    on 28 trades can filter the edge to zero and you will not be able to tell which one did it.
    ORDER: R5 first (it is already live and currently costing money), then R4 as advisory,
    then W1 much later. One at a time, measure between each.

  CONFLICT 2: FLAT GATE vs CHOP-SHORT gap=Flat CAUTION — partial overlap, NOT redundant.
    Of the 6-trade chop cohort the FLAT gate covers 2 (regime=FLAT, -228.13); the gap=Flat tell
    covers the other 4 (regime=TREND, -271.97). They are complementary. But if gap=Flat is shipped
    as a score penalty rather than an advisory note, vpos-61-type entries get penalised twice.
    RULE: keep the FLAT gate as the score floor; ship gap=Flat only as an advisor caution.

  CONFLICT 3 (structural, and it will bite silently): THE FLAT GATE STARVES THE CHOP SENSORS.
    W1 and W2 both need chop entries to accumulate. The FLAT gate now blocks exactly those.
    W2 in particular may NEVER reach n. Decide explicitly: either accept those two sensors will
    not ship, or redefine their cohort to gap1h='Flat' entries under regime=TREND, which still fire.

  CONFLICT 4: PRIOR-MOVE BUCKET vs gap=Flat. "late/mid" bucket correlates with a large prior move,
    which anti-correlates with a flat 1h EMA gap. Applying both may double-count the same tape
    condition from opposite directions. Check their correlation on the 34-trade set before stacking.

  CONFLICT 5: BULL-REGIME LONG RELAXATION vs THE LONG SIDE'S ACTUAL RECORD.
    R3 loosens LONG entry; LONG is PF 0.21 with 6/21 wins, and the 6 realised bull-regime entries
    are -186.89 (1/6). The drift-cut's +0.26%/12h is smaller than one stop distance. Op-X was
    already shipped and reverted once. DRYRUN ONLY. Do not relax LONG while LONG is the bleed.

  CONFLICT 6: RECHECK TIGHTEN FIX vs WALL-TRAIL — NOT redundant. The wall component was zeroed
    07-13 (c845941); the adx_below_floor component was not, and it is the one that fired.

  NON-CONFLICT: R1 (recheck) and R3 (cascade) touch the exit path and the entry path respectively
  and can ship independently.

## BOTTOM LINE
1. The book is +739 on 49 closes, carried entirely by SHORT (+1596) against LONG (-856).
   Every trail exit won; every SL exit but one lost.
2. July looks catastrophic (-906) but roughly half of it is the wall-trail self-clipping itself
   (-424 over 11 trades, 11 of which would have survived their original stop). That is already off.
3. The FLAT gate worked exactly as designed: 4 chop entries / -306 before, 0 after, ~370 extra
   blocks in the newly-gated band, and zero trend shorts touched.
4. The single highest-value action on this list is not a new sensor — it is closing the LAST live
   self-clipper: the post-entry recheck TIGHTEN (adx_below_floor). It has already cost one trade.
5. Two sensors are now genuinely decidable: the prior-move bucket (p=0.011) and the bull-regime
   drift-cut (run today; the answer is trend_4h=bull, NOT trend_1d=bull).
6. Do not stack the three SHORT-side filters. The short side is the only thing making money.
