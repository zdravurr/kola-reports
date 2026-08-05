# TITAN — DOES THE ORDER BOOK DISCRIMINATE REAL BREAKOUTS FROM FAILED ONES?

**2026-08-05 14:25 UTC · READ-ONLY · nothing changed, NOTHING PROPOSED · HEAD `b9081ad`**

Subject: **Titan** (`/root/titan-bot`) — 🔴 LIVE REAL MONEY, $30 × 5 = $150 notional.
Mercury-SOL never opened. `git status` on `titan-bot` clean before and after.

Parent: `2026-08-05-1210-titan-does-the-flat-gate-make-us-late-to-the-breakout.md`.

---

## 🔴 BONFERRONI HEADER — READ BEFORE THE RESULT

**The budget was set at 54. This brief is cell 57. The bar was already crossed before this
question was asked.**

**No cell was spent.** The coverage gate the operator pre-registered fired *before* any
discrimination test was run, so §§2–3 of the brief were **not executed** — no p-value was
computed, nominal or otherwise, and none is reported below. There is nothing here to correct
for, because nothing was tested.

---

## ANSWER IN ONE LINE

**Unanswerable on this data, and not by a small margin: 5 of the 105 episodes fall inside book
coverage — cells of 2 successful and 3 failed.** The operator's pre-registered exit
(*"fewer than ~10 → say so plainly and STOP"*) fires, and it fires at every one of the nine
squeeze definitions tested, including the one chosen to maximise n.

🔴 **This CLOSES the question. It does NOT kill the hypothesis, and the difference is the whole
point of §4.**

---

## §1 — COVERAGE FIRST, AS INSTRUCTED

### 1a. THE BOOK'S OWN WINDOW

| | |
|---|---|
| table | `orderbook_density` |
| source | **`okx_books_full_4000`** — one source, no mixing |
| snapshots | **33,236** |
| first | **2026-07-13 02:34:56 UTC** |
| last | 2026-08-05 14:18:13 UTC |
| span | **23.5 days** |
| cadence | **0.98 snapshots/min** against a 60 s collector — 98 % uptime |
| gaps > 10 min | 🔴 **ZERO. 0.0 % of the span.** |

**The collector is not the problem.** The coverage it has is continuous and dense — the nearest
snapshot to any instant inside the window is under a minute away. There is simply not much of it
yet. The brief's premise ("collects from 2026-07-13") is confirmed exactly.

### 1b. 🔴 (a) — HOW MANY OF THE 105 FALL INSIDE IT

The episodes are **not re-derived**. `episodes.pkl` is the artefact the 12:10 report produced,
under the definition it fixed before looking at any result (BBW < p20 of the trailing 90 days,
run ≥ 12 bars, t0 = first bar whose **close** leaves the box). The 105-episode t0 span is
**2024-08-18 → 2026-08-02**.

| | count |
|---|---|
| episodes with a resolved breakout | 105 |
| t0 **bar open** inside book coverage | **4** |
| 🔴 **t0 bar CLOSE inside book coverage** | **5 of 105 = 4.8 %** |

Both are stated because t0 is a bar *open* while the breakout is only **knowable at the bar
close** — the close is the earliest instant a bot could read a book about it, so the close is the
generous reading and the one carried forward. **It buys one episode.**

### 1c. (b) — THE AGE DISTRIBUTION, FOR THOSE FIVE

| t0 (UTC, bar open) | dir | 48h move % | \|Δt\| to bar OPEN | \|Δt\| to bar CLOSE |
|---|---|---|---|---|
| 2026-07-13 02:00 | DOWN | 2.47 | 34.9 min | **0.5 min** |
| 2026-07-20 06:00 | DOWN | 0.51 | 0.5 min | **0.5 min** |
| 2026-07-23 12:00 | DOWN | 2.45 | 0.4 min | **0.5 min** |
| 2026-07-26 22:00 | UP | 1.24 | 0.5 min | **0.1 min** |
| 2026-08-02 02:00 | UP | 1.47 | 0.5 min | **0.5 min** |

**Within ±5 min of the t0 bar close: 5 of 5.** Within ±5 min of the bar open: 4 of 5 — the single
miss is the 07-13 episode, whose breakout bar opened **35 minutes before the collector's first
snapshot ever**.

🔴 **Freshness is not the binding constraint. Count is.** Every episode that is covered is covered
excellently. There are five of them.

### 1d. 🔴 (c) — THE EXIT FIRES, AND IT IS NOT A CLOSE CALL

**5 < ~10. The pre-registered exit fires and §§2–3 are not run.**

The operator named this exit in advance precisely so it could not be rationalised away afterwards.
It is not being rationalised away. What follows is the accounting that shows the exit is not
marginal — not an argument for crossing it.

---

## §2 — THE EXIT IS NOT AN ARTEFACT OF ONE SQUEEZE DEFINITION

The obvious objection to "n = 5" is that 5 is a consequence of *my* squeeze definition. So all
nine variants from the 12:10 sensitivity table were rebuilt and each was counted against the same
23.5-day window — **and split by outcome, because the cells are what the test would actually
run on, not the total.**

| pctl | min run | episodes (all time) | **covered** | successful | **FAILED** |
|---|---|---|---|---|---|
| 10 | 6 | 101 | 6 | 2 | 4 |
| 10 | 12 | 61 | 3 | 🔴 **0** | 3 |
| 10 | 24 | 27 | 🔴 **0** | 0 | 0 |
| **20** | **12** *(canonical)* | **105** | **5** | **2** | **3** |
| 20 | 6 | 178 | 8 | 3 | 5 |
| 20 | 24 | 51 | 2 | 0 | 2 |
| 30 | 6 | 225 | **11** | 8 | 3 |
| 30 | 12 | 145 | 6 | 4 | 2 |
| 30 | 24 | 82 | 3 | 2 | 1 |

**Not one definition reaches a usable pair of cells.**

- The canonical definition gives **2 vs 3**.
- **Two of the nine produce a cell of ZERO** — at p10/run≥12 there is not a single *successful*
  covered breakout, and at p10/run≥24 there are no covered episodes at all. A test on those is
  not weak, it is undefined.
- The definition that **maximises** coverage — p30 / run ≥ 6, n = 11 — reaches 11 only by calling
  a breakout **every ~3 days across 2.3 years**, i.e. by loosening "squeeze" until the word stops
  selecting anything. It still yields cells of **8 and 3**, and §3c of the brief asks to split
  those again **by direction**, which takes them to low single digits.

The canonical five split **2 UP / 3 DOWN** on top of 2-vs-3 by outcome. The brief's §3b requires
controlling for **day, hour and direction**. There is no de-confounding to be done on five points;
a day control alone consumes the sample. **The failure is upstream of the statistics.**

---

## §3 — IS 2026-07-13 A REAL FLOOR? EVERY OTHER STORE WAS CHECKED

Closure for want of data is only honest if the data was actually looked for. Three other stores in
`trades.db` hold book material. **All three were checked against the same 105 episodes.**

| store | rows | span | 🔴 episodes hit within ±5 min of a t0 bar close |
|---|---|---|---|
| `trades.orderbook_json` | 72 | 2026-05-17 → 2026-08-03 | **0 of 105** (and **0 of 105** even at ±60 min) |
| `virtual_positions` entry-book columns | 28 | 2026-07-04 → 2026-08-03 | **0 of 105** |
| `trades.advisor_book_json` | 15 | 2026-08-03 → 2026-08-05 | starts *after* `orderbook_density` — extends nothing |

**Zero, on every route, at every tolerance.** The reason is structural rather than unlucky: those
rows are written **when the bot took or considered a signal**, and signal times have no reason to
coincide with a squeeze box's breakout bar. They are a sample of the bot's attention, not of the
tape's structure.

🔴 **And they could not be pooled even if they had aligned.** 27 of the 28 entry-book rows carry a
**blank** `entry_book_src` — pre-`34dbdbf`, i.e. **BingX**, not OKX-4000 — and `orderbook_json` is
the BingX top-N shape (`top_bids` / `top_asks` / `walls_bid` / `walls_ask`). The brief asks for
depth and imbalance **as percentiles against the `orderbook_density` baseline**. That baseline
exists only for `okx_books_full_4000` and only from 2026-07-13. Ranking a BingX reading on the OKX
scale is **exactly the §2.19 cross-source inversion**, and §2.22 recorded three different
"imbalance" values living under one word in a single minute (0.31 BingX top-20, 0.51 OKX-4000,
0.2914 BingX-100). Pooling here would manufacture the finding, not measure it.

**2026-07-13 02:34:56 is a hard floor.**

---

## §4 — VERDICT

### 🔴 THE QUESTION IS CLOSED. THE HYPOTHESIS IS NOT KILLED. THAT DISTINCTION IS THE RESULT.

**Can the book see what the flat gate cannot? On this data the question cannot be asked** —
5 covered episodes, cells of 2 and 3, zero on every alternative store, and two of nine definitions
degenerate. **STOP, as pre-registered.**

**But this is a different kind of closure from §2.45's, and it must not be filed next to it.**
§2.45 killed ten branches **on evidence** — each was tested, each failed. The order book has
**not** been tested here and has **not** failed. Writing "the book cannot discriminate" would be
inventing a negative result out of an absence of data, which is the one thing this book forbids
outright.

The correct entry is: **UNMEASURED, for want of coverage — mechanism intact, evidence absent.**

### WHAT THE OPERATOR'S REASONING STILL HAS GOING FOR IT, STATED WITHOUT SUPPORT

The mechanical argument — *a genuine break eats the opposing wall, a failed one rejects off it* —
is a real hypothesis about a real observable, and the §3c form (move size ÷ opposing wall multiple)
is a testable quantity, not a vague one. **None of that is evidence.** It is why the question is
worth keeping open rather than closing permanently, and nothing more. This report supplies **zero**
support for it, and a future session must not cite this file as though it did.

### THE ARITHMETIC OF WAITING — A FACT, NOT A PROPOSAL

105 episodes over 714 days = **4.4 episodes/month**. The 23.5 days of book collected predicted 3.5
and delivered 5 — the covered sample is running slightly *ahead* of its base rate, so the shortfall
is not a collection failure.

| target n | more days needed | reached around |
|---|---|---|
| 10 | ~68 | **2026-09** |
| 20 | ~136 | 2026-11 |
| 34 (the parent report's 15m-covered sample size) | ~231 | 2027-03 |

**Recorded so the next session does not re-run this and rediscover n = 5.** It is a clock, not a
plan, and it is the same shape as §2.47's pre-registered instruments: the thing that changes this
answer is **arrivals**, and nothing else. Note also that this clock runs on a definition fixed
before any result was seen — if a future session widens the squeeze definition to reach n faster,
that is not the same question and the Bonferroni budget notices.

### 🔴 NOTHING IS PROPOSED

No gate reads the book today (§2.21: *"collected every 60 s, rendered into two prompts, stored in
two tables — weighted by nothing"*). **That remains true and this report does not argue for
changing it.** No filter, no weight, no advisor threshold, no new sensor. Per the brief: if
something had survived control on a usable n, the shape would be shown and nothing more. Nothing
survived, because nothing was tested, because there was nothing to test it on.

---

## APPENDIX — WHAT WAS RUN

| file | purpose |
|---|---|
| `c1_coverage.py` | book window, uptime, gap structure; the 105 episodes against it; nearest-snapshot ages; the nine-variant coverage count; the arrival clock |
| `c2_salvage.py` | the three alternative book stores vs the same 105 episodes, at ±5 min and ±60 min |
| `c3_cells.py` | outcome split (12:10's FAILED definition verbatim) of the covered sample, at all nine definitions |

`trades.db` was opened **read-only** (`file:…?mode=ro`) throughout — the bot is live and writing.
Episodes were **reused, not re-derived**, from the 12:10 report's `episodes.pkl`; candles are that
report's BingX pulls. `titan-bot` is unmodified at `b9081ad`.

*Read-only. Nothing changed, nothing proposed. Mercury-SOL never opened.*
