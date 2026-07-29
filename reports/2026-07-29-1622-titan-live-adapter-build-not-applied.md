# titan-live-adapter-build-not-applied

_2026-07-29 16:22 UTC_

---

# ТИТАН — LIVE-АДАПТЕР ПОСТРОЕН. НЕ ПРИМЕНЁН. ЧИТАЙ ПЕРЕД ТЕМ, КАК ПИСАТЬ ХОТЬ СТРОКУ
### 29.07.2026, 17:05 UTC. Маркер свежести: `LIVE-ADAPTER-BUILD-29JUL-1705`
### База: HEAD `5285495`. Бриф: `reports/2026-07-29-1527-titan-live-order-scoping.md`

---

## СТАТУС: НИЧЕГО НЕ ПРИМЕНЕНО

```
git status --porcelain            -> (пусто)
git rev-parse HEAD                -> 5285495114d00d87d7d8f3026579c3e33de92b3a
ls /root/titan-bot/order_adapter.py -> No such file or directory
git apply --check -p1 <patch>     -> ✅ ПРОХОДИТ (патч ложится на HEAD чисто)
```
Код написан и **проверен исполнением** в отдельной копии в scratchpad. Рабочее дерево не тронуто.
Патч ниже — полный и применяемый; команда на применение будет ждать твоего слова.

**Объём:** `config.py +28/−1` · `virtual_trader.py +57/−10` · `breakeven_worker.py +10/−0` ·
`gunicorn.conf.py +14/−1` · `main.py +20/−0` · **новый** `order_adapter.py +304`.
Пять файлов тронуто, один добавлен. Все пять компилируются (`py_compile`).

---

# ЧАСТЬ 1. БЕЗОПАСНОСТЬ — КАК ГАРАНТИРУЕТСЯ КАЖДЫЙ ПУНКТ

## 1. `LIVE_TRADING_ENABLED` остаётся False. Ничто в этой работе его не трогает

Патч меняет `config.py` в двух местах — оба **ниже** строки 17 и оба к ней не относятся: добавлен
новый флаг и разделён сайзинг. Строка `LIVE_TRADING_ENABLED = False` в диффе присутствует только
как **контекст** (с пробелом в начале), а не как изменение. Проверяется механически:

```
$ grep -cE '^[-+]LIVE_TRADING_ENABLED[[:space:]]*=' live_adapter.patch
0
```
Ноль добавленных и ноль удалённых строк, присваивающих мастер-флаг. Имя `LIVE_TRADING_ENABLED`
в патче встречается 6 раз — и все шесть внутри строковых литералов баннера и лог-сообщений
(`f"... LIVE_TRADING_ENABLED={master}"`), то есть это ЧТЕНИЯ для отображения, а не записи.
Присваивание существует ровно в одном месте кодовой базы, `config.py:17`, и патч его не касается.

## 2. 🔴 НИ ОДИН ПУТЬ НЕ ДОХОДИТ ДО `create_order` ПРИ FALSE — ТРАССИРОВКА, А НЕ УТВЕРЖДЕНИЕ

Ты просил доказать трассировкой. **Трассировка нашла три дыры, и я не буду делать вид, что их нет.**

Полный список мест, где код пишет на биржу (`grep` по `create_order|create_market_order|set_leverage`):

| # | Место | Что делает | Чем защищено СЕГОДНЯ | Флаговая защита? |
|---|---|---|---|---|
| 1 | `main.py:1208` | `create_market_order` (закрытие) | `main.py:1175` `if virtual_trader.is_active(): return virtual_trader.close_position(...)` | ✅ ДА |
| 2 | `main.py:1321` | `set_leverage` | `main.py:1250` тот же ранний возврат | ✅ ДА |
| 3 | `main.py:1325` | `create_market_order` (вход) | `main.py:1250` | ✅ ДА |
| 4 | `main.py:1364` | `create_order` STOP_MARKET | `main.py:1250` | ✅ ДА |
| 5 | **`main.py:4044/4058`** | `create_market_order` / `create_order` | **НИЧЕМ.** Legacy-ветка P3 в `webhook()` **инлайнит** закрытие вместо вызова `_execute_close_position`, поэтому охранника с 1175 она не унаследовала. Между строками 3994 и 4072 `is_active()` **не встречается ни разу** | ❌ **НЕТ** |
| 6 | **`breakeven_worker.py:213`** | `create_order` STOP_MARKET | **пустой таблицей.** `breakeven_jobs` = 0 строк за всю жизнь. Охранник `is_active()` в этом модуле есть, но только в РЕПОРТЁРЕ (`:320`), не в управлении | ❌ **НЕТ** |
| 7 | **`breakeven_worker.py:436`** | `create_order` TRAILING_STOP_MARKET | то же | ❌ **НЕТ** |
| 8 | `main.py:4446` | `_place_stop_with_retry` из `_reconcile_side` | **отсутствием реальной позиции.** `reconcile_boot_state` бежит на КАЖДОМ старте; при `pos is None` уходит в ветку «только отменить» (`main.py:4381-4384`) | ❌ НЕТ (см. §13) |

**Вывод честный:** сегодня ни одна из дыр 5–8 выстрелить не может — P3 спит, таблица пуста, реальной
позиции нет. Но **«не может сегодня» ≠ «не может»**: первое — свойство текущего формата алертов,
пустоты таблицы и отсутствия чужой позиции, второе — свойство кода.

**Что делает патч.** Требование №2 объявлено необсуждаемым, поэтому дыры 5, 6 и 7 в патче
**закрыты флаговой проверкой** — это выходит за буквальный список «построй адаптер», и я говорю
об этом прямо, чтобы ты мог их выкинуть одним словом:
- `main.py:4004` — ранний `return` из P3-ветки закрытия, если `orders_are_real()` False;
- `breakeven_worker.py:681` — `continue` перед `_handle_watching`/`_attempt_trail`.

**Дыра 8 НАМЕРЕННО НЕ ТРОНУТА** — закрывать её значит менять защитное поведение (см. §13), а это
уже проектное решение, а не обвязка.

**Проверка исполнением** (не рассуждением) — все четыре комбинации флагов:
```
master=False adapter=False -> orders_are_real=False
master=False adapter=True  -> orders_are_real=False
master=True  adapter=False -> orders_are_real=False
master=True  adapter=True  -> orders_are_real=True
```
И `_require_live()` при каждой из трёх «неполных» комбинаций поднимает `OrdersDisabled`.

## 3. ДВА ФЛАГА, ОБА ОБЯЗАНЫ БЫТЬ TRUE. ПО УМОЛЧАНИЮ ОБА FALSE

```python
LIVE_TRADING_ENABLED = False   # config.py:17  — «разрешены ли реальные деньги» (было)
ORDER_ADAPTER_LIVE   = False   # config.py:35  — «адаптер ШЛЁТ или СИМУЛИРУЕТ» (новое)

def orders_are_real():
    return bool(config.LIVE_TRADING_ENABLED) and bool(config.ORDER_ADAPTER_LIVE)
```
**Защита в глубину:** `_require_live()` перечитывает **оба** флага непосредственно перед каждой
отправкой. Проверка стоит у «системного вызова», а не у ветвления, поэтому вызывающий, держащий
устаревшее значение режима, физически не может открыть ворота.

## 4. ЗАГРУЗОЧНАЯ АССЕРЦИЯ — ГРОМКО, НА КАЖДОМ СТАРТЕ

`order_adapter.assert_startup_mode()` вызывается из `gunicorn.conf.py:when_ready` **до** сверки
(потому что сама сверка — путь, способный поставить ордер) и из `main.__main__`. Живой вывод:

```
========================================================================
[TITAN][ORDER-MODE] 🧪 PAPER — simulated fills only — no order can be sent (LIVE_TRADING_ENABLED=False)
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = False
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = False
[TITAN][ORDER-MODE]   sizing: margin $2000 x 5 = $10000 notional per entry
========================================================================
```
Плюс та же строка уходит в Telegram в сообщении «Bot online». Двусмысленности не остаётся.

## 5. 🔴 ЧТО ЧЕЛОВЕК ДОЛЖЕН ИЗМЕНИТЬ, ЧТОБЫ ПОШЛИ РЕАЛЬНЫЕ ДЕНЬГИ — **ЭТО БОЛЬШЕ, ЧЕМ ФЛАГИ**

Ты просил сказать сейчас, если больше. **Больше.**

Переключить два флага **недостаточно и опасно**. `main.py:1175` и `main.py:1250` ветвятся по
`virtual_trader.is_active()`, то есть по `not LIVE_TRADING_ENABLED`. Поставив мастер-флаг в True,
ты **уводишь трафик в СТАРЫЙ боевой путь** (`main._execute_entry` / `_execute_close_position`),
который адаптера не видит вовсе. А этот путь:
- **не имеет семи механизмов** бумажного движка (OPEN-ITEMS §1: частичка LONG, post-entry recheck,
  wall anchor, adaptive_trail, excursion logging, smart-exit dryrun, `original_sl_price`);
- **сайзится от `FIXED_MARGIN_USDT`**, который в патче намеренно оставлен равным ПАПЕРНОМУ размеру
  → **$10 000 нотионала вместо $200, в 50 раз больше задуманного.**

То есть «переключил два флага» = **торгуешь другой стратегией в 50 раз большим размером.**

Поэтому в адаптер встроен `routing_warning()`: при `orders_are_real() == True` он на каждом старте
печатает и шлёт в Telegram:
```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[TITAN][ORDER-MODE] CRITICAL: routing NOT migrated — real orders will BYPASS this adapter.
[TITAN][ORDER-MODE] main.py:1175/1250 branch on virtual_trader.is_active(); with
                    LIVE_TRADING_ENABLED=True they route to the LEGACY live path, not here.
[TITAN][ORDER-MODE] That path lacks LONG partial, post-entry recheck, wall anchor, excursion
                    logging and smart-exit dryrun, and sizes off FIXED_MARGIN_USDT (= $2000, the PAPER size).
[TITAN][ORDER-MODE] DO NOT TRADE until the routing decision (design item 12) is made.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```
Сейчас это **крик, а не запрет**: боту дают подняться. Скажи слово — сделаю жёстким отказом от
старта. Я не стал решать это сам, потому что «не подняться» — тоже операционное последствие.

### Полный, честный чеклист «чтобы пошли настоящие деньги»
| Шаг | Где | В этом патче? |
|---|---|---|
| 1. `ORDER_ADAPTER_LIVE = True` | `config.py:35` | флаг создан, значение False |
| 2. `LIVE_TRADING_ENABLED = True` | `config.py:17` | не тронут |
| 3. **Перевести маршрутизацию** на адаптер (`main.py:1175`, `main.py:1250`) | `main.py` | ❌ **НЕТ — это проектный пункт 12** |
| 4. Принять решение по владению стопом (пункт 11) | — | ❌ НЕТ, только предложение |
| 5. Покрыть сверку `virtual_positions` (пункт 13) | — | ❌ НЕТ, только предложение |
| 6. Довести частичные заливки до конца (пункт 14) | — | частично: адаптер уже читает `filled` и орёт |
| 7. Перезапустить `titan.service` | — | — |

**Шаги 3–6 — это не флаги. Пока они не сделаны, шаги 1–2 делать НЕЛЬЗЯ.**

---

# ЧАСТЬ 2. ЧТО ПОСТРОЕНО (пункты 6-10)

**6. Адаптер переиспользует боевой код, а не переписывает.** `market_close()` вызывает
`main._execute_close_position` целиком — с отменой триггеров по `positionSide`, закрытием
РЕАЛЬНОГО размера с биржи и повторной зачисткой сирот. Комиссия берётся `main.fetch_order_fee`.
Оговорка честная: **`main._execute_entry` целиком переиспользовать нельзя** — он сам считает
размер и сам ветвится в `virtual_trader` на строке 1250, то есть вызов из адаптера был бы
рекурсией. Поэтому вход переиспользует ПРИМИТИВЫ (`set_leverage`, `create_market_order`,
`fetch_order_fee`) и сохраняет инвариант отказа, а не тело функции.

**7. Три функции проведены через адаптер**, контракт возврата сохранён
(`virtual_trader.py:829-841` == `main.py:1221-1227`): `execute_entry` (1 точка), `_do_close`
(обслуживает все 4 места вызова: `:707` внешнее, `:1177` post-entry critical, `:1750` стоп,
`:1766` трейл), `_take_long_partial` (1 точка, теперь принимает `exchange`).

**8. Реальные комиссии.** В бою — из ответа биржи через `fetch_order_fee`. Если биржа комиссию не
вернула, адаптер **не пишет ноль молча** (это был дефект §7.4 брифа), а оценивает по ставке
тейкера и **печатает, что это оценка**, ставя флаг `fee_estimated`.

**9. Проверка минимумов — которой не было НИГДЕ.** `check_size()` читает `limits.amount.min` и
`limits.cost.min`, округляет к шагу, и **работает В ОБОИХ режимах** — бумага обязана отвергать то,
что отвергнет бой, иначе бумага перестаёт предсказывать бой. Fail-closed: не смог прочитать
лимиты — не отправляет. Проверено на живом рынке BingX:
```
$200 нотионала -> ok=True  amount=0.0031  (запас 31x над минимумом)
$6            -> ok=False amount rounds below the 0.0001 step
$1            -> ok=False
```

**10. Сайзинг разделён.** `PAPER_FIXED_MARGIN_USDT = 2000.0` (без изменений — бумага торгует тем
же размером и остаётся сравнимой со своей историей), `LIVE_FIXED_MARGIN_USDT = 40.0` (= $200 при
5x). Выбирает `order_adapter.active_fixed_margin()` по режиму.

### 🔴 ДОКАЗАТЕЛЬСТВО, ЧТО НИ ОДНО БУМАЖНОЕ ЧИСЛО НЕ СДВИНУЛОСЬ
Симулированная ветка воспроизводит прежнюю арифметику побитово. Проверено исполнением на реальных
числах vpos 85:
```
старое: fill_price = current_price = 64604.4 ; fee = 64604.4*0.1547*0.0005 = 4.9971503400
новое : fill_price = 64604.4                 ; fee =                        4.9971503400
IDENTICAL ✓
```
4.99715034 — ровно та комиссия, что лежит в `filled_legs` живой позиции vpos 85. Бумажная книга
после этого патча остаётся сравнимой сама с собой.

---

# ЧАСТЬ 3. ПОЛНЫЙ ПАТЧ (НЕ ПРИМЕНЁН)

Проверен `git apply --check -p1` против HEAD `5285495` — ложится чисто.

```diff
--- a/titan-bot/config.py
+++ b/titan-bot/config.py
@@ -16,6 +16,24 @@
 # flag is the only gate between paper and real money.
 LIVE_TRADING_ENABLED = False
 
+# ===========================================================================
+# ORDER-ADAPTER MODE — the SECOND of the two flags. BOTH must be True.
+# ===========================================================================
+# LIVE_TRADING_ENABLED above answers "is real money authorised at all".
+# ORDER_ADAPTER_LIVE answers a DIFFERENT question: "does the order adapter SEND
+# the order or SIMULATE it". They are kept apart on purpose — today the single
+# master flag means both "real money" AND "which code path manages the
+# position", and collapsing two meanings into one boolean is how a mode gets
+# flipped by accident.
+#
+#   orders_are_real() == LIVE_TRADING_ENABLED and ORDER_ADAPTER_LIVE
+#
+# Either F. => every fill is simulated and NOTHING reaches the exchange.
+# order_adapter re-reads BOTH immediately before each send, so a stale value
+# held by a caller cannot open the gate. Default F.; flipping it is a
+# deliberate human act, exactly like the master switch.
+ORDER_ADAPTER_LIVE = False
+
 # Leverage applied to every order (isolated, hedge mode).
 LEVERAGE = 5
 
@@ -24,7 +42,19 @@
 # risk÷SL formula AND the 30% margin cap below. The 2.5×ATR SL is unaffected
 # (computed independently of size). False = legacy risk-based sizing.
 FIXED_NOTIONAL_MODE = True
-FIXED_MARGIN_USDT = 2000.0     # margin per entry; notional = FIXED_MARGIN_USDT × LEVERAGE = $10,000
+
+# Sizing is SEPARATE for paper and live, and the adapter picks by mode
+# (order_adapter.active_fixed_margin()). Paper keeps the size its entire book
+# was traded at, so its history stays comparable with itself; live starts small
+# and is turned up deliberately, never by inheriting the paper number.
+PAPER_FIXED_MARGIN_USDT = 2000.0   # unchanged: 2000 × 5 = $10,000 notional
+LIVE_FIXED_MARGIN_USDT = 40.0      # 40 × 5 = $200 notional  (0.0031 BTC @ 64k)
+
+# Back-compat alias. main.py's LEGACY live entry path still imports this name;
+# it resolves to the PAPER size, which is deliberate — that path is not the
+# adapter and must not silently acquire the live size. See the routing note in
+# the scoping report before enabling anything.
+FIXED_MARGIN_USDT = PAPER_FIXED_MARGIN_USDT
 
 # ---------------------------------------------------------------------------
 # Risk-based single-entry sizing (refactor 2026-05-20, Stage 2B).
--- a/titan-bot/virtual_trader.py
+++ b/titan-bot/virtual_trader.py
@@ -73,7 +73,7 @@
     LEVERAGE, RISK_BASE_USDT, RISK_PER_TRADE_PCT, SL_ATR_MULT,
     MAX_MARGIN_PCT_PER_TRADE, TRAIL_MULT_ATR, ATR_LEN, MAX_POSITIONS_PER_SIDE,
     TAKER_FEE_RATE, BREAKEVEN_BUFFER_PCT, SL_ATR_TF, TRAIL_ATR_TF,
-    FIXED_NOTIONAL_MODE, FIXED_MARGIN_USDT,
+    FIXED_NOTIONAL_MODE,
     ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN,
     ADAPTIVE_TRAIL_BAND_LO, ADAPTIVE_TRAIL_BAND_HI,
     LIVE_TRADING_ENABLED,
@@ -93,6 +93,11 @@
     EXIT_ADVISOR_HOURLY, EXIT_ADVISOR_DRYRUN, EXIT_ADVISOR_HOURLY_SEC,
 )
 
+# The order adapter: the ONE seam where a fill is either SENT to the exchange
+# or SIMULATED. Imported at module load (no circular risk — order_adapter
+# imports only config, and reaches main lazily inside its live branches).
+import order_adapter
+
 # Serializes the final count-and-insert in execute_entry so two same-bar
 # webhooks on different gthread threads can't both pass the open-position
 # check before either inserts (the vpos 48/49 TOCTOU). workers=1 in
@@ -101,7 +106,11 @@
 # unique index (ux_vpos_one_open_per_side) created in init_db().
 _entry_lock = threading.Lock()
 
-# 0.05% fee per execution — applied to entry, every DCA leg, and the close.
+# 0.05% fee per execution. SUPERSEDED as the authority by
+# order_adapter.SIM_FEE_RATE (same value): every simulated fee is now charged
+# inside the adapter, so paper and live read their fee from ONE place. Kept
+# defined because the module docstring and external readers reference the name;
+# no code path computes a fee from it any more.
 VIRTUAL_FEE_RATE = 0.0005
 
 # How many closed virtual pairs gate the observation window.
@@ -502,8 +511,11 @@
     if FIXED_NOTIONAL_MODE:
         # Flat notional — identical every entry. Bypasses risk÷SL AND the 30%
         # cap. The 2.5×ATR SL is unaffected (computed below from fill_price).
-        margin_required = FIXED_MARGIN_USDT
-        notional_usdt = FIXED_MARGIN_USDT * LEVERAGE
+        # Size is mode-dependent: paper keeps its historical $10k notional so the
+        # book stays self-comparable, live starts at $200. One call, one source.
+        _fixed_margin = order_adapter.active_fixed_margin()
+        margin_required = _fixed_margin
+        notional_usdt = _fixed_margin * LEVERAGE
         amount = float(exchange.amount_to_precision(symbol, notional_usdt / current_price))
         size_capped = False
         realized_risk_usdt = amount * sl_distance_price   # derived report, not a sizing driver
@@ -532,8 +544,22 @@
         else:
             realized_risk_usdt = risk_usdt
 
-    fill_price = current_price
-    entry_fee = fill_price * amount * VIRTUAL_FEE_RATE
+    # THE FILL. Simulated: fill_price == current_price and the fee is the flat
+    # VIRTUAL_FEE_RATE — arithmetic identical to before this seam existed, so no
+    # paper number moves. Live: a real market order, with the fill price, the
+    # EXECUTED size and the REAL fee read back from the exchange.
+    # Returns None when refused locally (below the exchange minimum) — then no
+    # position exists and we must not write a row.
+    _entry_fill = order_adapter.market_entry(
+        exchange, symbol, side, position_side, amount, current_price,
+        leverage=LEVERAGE)
+    if _entry_fill is None:
+        print(f"VIRTUAL ENTRY ABORTED {symbol} {position_side}: adapter refused "
+              f"the order (see [ADAPTER] line above)", flush=True)
+        return None
+    fill_price = _entry_fill['fill_price']
+    amount = _entry_fill['amount']          # EXECUTED size, not the requested one
+    entry_fee = _entry_fill['fee_cost']
 
     if position_side == 'LONG':
         sl_price = fill_price - SL_ATR_MULT * atr_sl
@@ -713,7 +739,19 @@
     real _execute_close_position would have returned."""
     filled_legs = json.loads(row['filled_legs'])
     avg_entry, total_size = _avg_entry_and_size(filled_legs)
-    close_fee = close_price * total_size * VIRTUAL_FEE_RATE
+    # THE EXIT FILL. Simulated: close_price stays the decision price and the fee
+    # is flat — unchanged arithmetic. Live: main._execute_close_position runs
+    # (cancel this side's triggers -> close the REAL on-exchange size -> re-sweep
+    # orphans), and the actual fill price, size and fee come back from it.
+    _exit_fill = order_adapter.market_close(
+        exchange, row['symbol'], row['position_side'], total_size, close_price)
+    if _exit_fill is None:
+        print(f"VIRTUAL CLOSE ABORTED vpos={row['id']}: adapter found no live "
+              f"position to close; row left OPEN for reconciliation", flush=True)
+        return None
+    close_price = _exit_fill['fill_price']
+    total_size = _exit_fill['amount']
+    close_fee = _exit_fill['fee_cost']
     entry_fee = sum(leg.get('fee', 0.0) for leg in filled_legs)
     total_fees = entry_fee + close_fee  # == _total_fees(filled_legs, close_fee)
     closed_at = _utc_now_iso()
@@ -1025,7 +1063,7 @@
     return new_sl
 
 
-def _take_long_partial(row, last, send_tg):
+def _take_long_partial(exchange, row, last, send_tg):
     """Realise LONG_PARTIAL_FRACTION of a LONG at LONG_PARTIAL_LEVEL_R.
 
     Banks the tranche's PnL into realized_partial_usdt and shrinks every DCA leg
@@ -1042,8 +1080,18 @@
         if not (0.0 < frac < 1.0):
             return False
         cut_size = total_size * frac
+        # THE PARTIAL FILL. Simulated: exact arithmetic as before. Live: a
+        # reduce-only market order that does NOT touch the protective orders —
+        # the remainder rides the unchanged contract. Refused (below the
+        # exchange minimum) leaves the position exactly as it was.
+        _cut_fill = order_adapter.market_reduce(
+            exchange, row['symbol'], row['position_side'], cut_size, last)
+        if _cut_fill is None:
+            return False
+        cut_size = _cut_fill['amount']
+        last = _cut_fill['fill_price']
         gross = (last - avg_entry) * cut_size
-        fee = last * cut_size * VIRTUAL_FEE_RATE
+        fee = _cut_fill['fee_cost']
         # Entry fee already paid on this tranche, charged pro-rata so the
         # remainder is not billed twice for it at final close.
         entry_fee_share = sum(leg.get('fee', 0.0) for leg in legs) * frac
@@ -1669,7 +1717,7 @@
                       and row['original_sl_price'] is not None else row['sl_price'])
         _fill_p = float(row['initial_fill_price'])
         _lvl = _fill_p + _one_r_distance(_fill_p, _orig_sl_p) * float(LONG_PARTIAL_LEVEL_R)
-        if last >= _lvl and _take_long_partial(row, last, send_tg):
+        if last >= _lvl and _take_long_partial(exchange, row, last, send_tg):
             row = _open_position(row['symbol'], position_side) or row
             changed = True
 
--- a/titan-bot/breakeven_worker.py
+++ b/titan-bot/breakeven_worker.py
@@ -37,6 +37,7 @@
 )
 import close_report
 import adaptive_trail
+import order_adapter
 import sensor_events
 from post_exit_observatory import tick as observatory_tick
 from skip_attribution import tick as skip_attribution_tick
@@ -680,6 +681,15 @@
         except Exception as e:
             print(f"[BE-MAE] update failed job {job['id']}: {e}", flush=True)
 
+        # SAFETY (requirement 2). Both handlers below CANCEL and CREATE real
+        # exchange orders (_place_stop_with_retry, TRAILING_STOP_MARKET). Today
+        # they are unreachable in paper only because breakeven_jobs has had ZERO
+        # rows in its entire life — i.e. guarded by an empty table, not by the
+        # master switch. An empty table is a circumstance; make it a flag.
+        if not order_adapter.orders_are_real():
+            print(f"[BE] paper mode — skipping order-placing handlers for job "
+                  f"{job['id']} ({job['symbol']} {job['position_side']})", flush=True)
+            continue
         try:
             if job['status'] == 'watching':
                 _handle_watching(exchange, send_tg, job, last)
--- a/titan-bot/gunicorn.conf.py
+++ b/titan-bot/gunicorn.conf.py
@@ -61,6 +61,15 @@
     # once (independent of worker count), before workers fork and before the
     # breakeven worker polls / Flask serves. Bring state into order, THEN
     # announce online.
+    # LOUD, UNMISSABLE, EVERY BOOT: which order mode is active. Printed BEFORE
+    # reconciliation, because reconciliation is itself a path that can place a
+    # stop order when a real position exists on the exchange — the operator must
+    # see the mode first, not after.
+    try:
+        import order_adapter
+        order_adapter.assert_startup_mode()
+    except Exception as e:
+        print(f"ORDER-MODE banner failed: {e}", flush=True)
     try:
         import main
         main.reconcile_boot_state()
@@ -70,14 +79,18 @@
         from main import (send_tg, LEVERAGE, RISK_BASE_USDT,
                           RISK_PER_TRADE_PCT, SL_ATR_MULT)
         from config import HTF_CASCADE_ENABLED
+        import order_adapter
         htf_mode = ('HARD-VETO' if HTF_CASCADE_ENABLED
                     else 'OBSERVATION (logging only)')
+        _mode_tag, _mode_detail, _m_master, _m_adapter = order_adapter.mode_banner()
         send_tg(
             f"🟢 <b>Bot online (gunicorn)</b>\n"
             f"🖥 {socket.gethostname()}  PID {os.getpid()}\n"
             f"🌐 :80  ⚙️ x{LEVERAGE}  💵 Risk-based single-entry "
             f"({RISK_PER_TRADE_PCT:.0%} of ${RISK_BASE_USDT:g} @ {SL_ATR_MULT}×ATR)  Hedge mode\n"
-            f"🧭 HTF cascade: <b>{htf_mode}</b>  ·  4H/1H/15m/5m + OI/Funding/Liq enrichment ON"
+            f"🧭 HTF cascade: <b>{htf_mode}</b>  ·  4H/1H/15m/5m + OI/Funding/Liq enrichment ON\n"
+            f"{_mode_tag} <b>{_mode_detail}</b>  ·  LIVE_TRADING_ENABLED={_m_master} "
+            f"ORDER_ADAPTER_LIVE={_m_adapter}"
         )
     except Exception as e:
         print(f"startup notify failed: {e}", flush=True)
--- a/titan-bot/main.py
+++ b/titan-bot/main.py
@@ -510,6 +510,7 @@
 import news_sentiment
 import indicators
 import close_report
+import order_adapter
 import virtual_trader
 from post_exit_observatory import on_15m_exit_signal
 import skip_attribution
@@ -4002,6 +4003,21 @@
         realized_risk_usdt = None
 
         if is_close:
+            # SAFETY (requirement 2). This legacy P3 branch inlines its own
+            # create_market_order below (main.py:4044/4058) instead of calling
+            # _execute_close_position, so it never inherited the
+            # virtual_trader.is_active() guard that protects every other order
+            # path. It is dormant — the state machine routes today's signals via
+            # P1/P2 — but "dormant" is a property of the current alert format,
+            # not a guarantee. Make the guard explicit and flag-based.
+            if not order_adapter.orders_are_real():
+                print(f"[P3-CLOSE] BLOCKED in paper mode: refusing to send a real "
+                      f"close order for {symbol} {position_side}", flush=True)
+                update_signal_execution(row_id, status='paper_mode_blocked',
+                                        combo_key=combo)
+                return jsonify({"status": "blocked_paper_mode",
+                                "reason": "P3 legacy close reached while "
+                                          "orders_are_real() is False"}), 200
             armed = state_machine.is_exit_armed(position_side)
             if armed:
                 print(f"EXIT_BYPASS side={position_side} armed_by={armed['source_signal']} expires={armed['expires_at']}")
@@ -4487,7 +4503,11 @@
 
 if __name__ == '__main__':
     import socket
+    import order_adapter
     port = int(os.getenv('PORT', '80'))
+    # Same loud banner as the gunicorn path, before reconciliation for the same
+    # reason. The dev entrypoint must never be quieter about mode than prod.
+    order_adapter.assert_startup_mode()
     reconcile_boot_state()
     signal_weights.start_audit_worker(exchange, send_tg)
     mfe_tracker.start_worker(exchange, send_tg)
--- /dev/null
+++ b/titan-bot/order_adapter.py
@@ -0,0 +1,311 @@
+"""Order adapter — the ONE place where a fill either HAPPENS on the exchange
+or is SIMULATED.
+
+Design brief: reports/2026-07-29-1527-titan-live-order-scoping.md. That study
+found 13 places where `virtual_trader` assumes a price, funnelling through three
+functions (`execute_entry`, `_do_close`, `_take_long_partial`). This module is
+the seam those three now call. One engine, two adapters — never a second copy of
+the strategy.
+
+===========================================================================
+SAFETY — TWO FLAGS, BOTH MUST BE TRUE. DEFAULT: BOTH FALSE.
+===========================================================================
+    config.LIVE_TRADING_ENABLED   master switch, pre-existing, authorises real money
+    config.ORDER_ADAPTER_LIVE     adapter mode: send orders vs simulate them
+
+`orders_are_real()` is `LIVE_TRADING_ENABLED and ORDER_ADAPTER_LIVE`. Either one
+False means EVERY function here simulates and NOTHING is sent. The two flags are
+deliberately NOT collapsed into one: today `LIVE_TRADING_ENABLED` alone means both
+"real money is authorised" AND "which code path manages the position", and that
+conflation is exactly what the scoping study said must be split before anything
+is wired up.
+
+Defence in depth: `_require_live()` re-reads BOTH flags immediately before every
+send and raises `OrdersDisabled` if either is False. A caller cannot reach an
+exchange write by holding a stale mode value — the check is at the syscall, not
+at the branch.
+
+While simulating, every function reproduces the previous arithmetic EXACTLY
+(`ref_price` as the fill, `VIRTUAL_FEE_RATE` on notional), so paper results stay
+byte-comparable with the existing book. This module changes NO paper number.
+"""
+
+import config
+
+# Simulated fee rate. Kept equal to the live taker rate by construction; the two
+# real orders in the bot's entire history (trades id 181/186, 2026-05-11) both
+# came back at an implied 0.000500, so this is measured, not assumed.
+SIM_FEE_RATE = 0.0005
+
+
+class OrdersDisabled(RuntimeError):
+    """A send was attempted while the two-flag gate was not fully open."""
+
+
+class OrderTooSmall(ValueError):
+    """Order rejected locally: below the exchange minimum amount or cost."""
+
+
+# ---------------------------------------------------------------------------
+# Mode
+# ---------------------------------------------------------------------------
+
+def orders_are_real():
+    """The ONLY predicate that may authorise an exchange write. Both flags."""
+    return bool(getattr(config, 'LIVE_TRADING_ENABLED', False)) and \
+        bool(getattr(config, 'ORDER_ADAPTER_LIVE', False))
+
+
+def mode_banner():
+    master = bool(getattr(config, 'LIVE_TRADING_ENABLED', False))
+    adapter = bool(getattr(config, 'ORDER_ADAPTER_LIVE', False))
+    if master and adapter:
+        return ('🔴 LIVE ORDERS', 'REAL MONEY: orders ARE sent to BingX',
+                master, adapter)
+    why = ('LIVE_TRADING_ENABLED=False' if not master else 'ORDER_ADAPTER_LIVE=False')
+    return ('🧪 PAPER', f'simulated fills only — no order can be sent ({why})',
+            master, adapter)
+
+
+def assert_startup_mode(send_tg=None):
+    """Loud, unmissable, on EVERY boot. Prints the active mode and both flag
+    values so it can never be ambiguous which one is running. Returns the
+    banner tuple. Never raises — a reporting failure must not stop boot."""
+    tag, detail, master, adapter = mode_banner()
+    size = active_fixed_margin()
+    lev = getattr(config, 'LEVERAGE', 0)
+    bar = '=' * 72
+    print(bar, flush=True)
+    print(f"[TITAN][ORDER-MODE] {tag} — {detail}", flush=True)
+    print(f"[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = {master}", flush=True)
+    print(f"[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = {adapter}", flush=True)
+    print(f"[TITAN][ORDER-MODE]   sizing: margin ${size:g} x {lev} = "
+          f"${size * lev:g} notional per entry", flush=True)
+    print(bar, flush=True)
+    warn = routing_warning()
+    if warn:
+        print('!' * 72, flush=True)
+        for line in warn.splitlines():
+            print(f"[TITAN][ORDER-MODE] {line}", flush=True)
+        print('!' * 72, flush=True)
+    if send_tg:
+        try:
+            send_tg(f"{tag} <b>order mode on boot</b>\n{detail}\n"
+                    f"LIVE_TRADING_ENABLED={master} · ORDER_ADAPTER_LIVE={adapter}\n"
+                    f"size: ${size:g} × {lev} = ${size * lev:g} notional"
+                    + (f"\n\n🔴 <b>{warn.splitlines()[0]}</b>" if warn else ''))
+        except Exception as e:
+            print(f"[TITAN][ORDER-MODE] telegram announce failed: {e}", flush=True)
+    return tag, detail, master, adapter
+
+
+def routing_warning():
+    """Returns a CRITICAL message when the flags say 'real orders' but main.py
+    would not actually route through this adapter, else ''.
+
+    main.py branches on virtual_trader.is_active() (== not LIVE_TRADING_ENABLED)
+    at main.py:1175 and main.py:1250. With the master switch True, entries and
+    closes go to the LEGACY live path (main._execute_entry /
+    _execute_close_position) and NEVER reach this module. That legacy path is
+    missing seven mechanisms the paper engine has (OPEN-ITEMS §1) and sizes off
+    FIXED_MARGIN_USDT, which is the PAPER size. Flipping both flags without
+    migrating the routing therefore trades a DIFFERENT strategy at 50x the
+    intended size. Refusing to be silent about that is the whole point of this
+    function; the routing change itself is design item 12 and is deliberately
+    NOT in this build."""
+    if not orders_are_real():
+        return ''
+    return (
+        "CRITICAL: routing NOT migrated — real orders will BYPASS this adapter.\n"
+        "main.py:1175/1250 branch on virtual_trader.is_active(); with "
+        "LIVE_TRADING_ENABLED=True they route to the LEGACY live path, not here.\n"
+        "That path lacks LONG partial, post-entry recheck, wall anchor, excursion "
+        "logging and smart-exit dryrun, and sizes off FIXED_MARGIN_USDT "
+        f"(= ${float(getattr(config, 'FIXED_MARGIN_USDT', 0)):g}, the PAPER size).\n"
+        "DO NOT TRADE until the routing decision (design item 12) is made."
+    )
+
+
+def active_fixed_margin():
+    """Margin per entry for the CURRENT mode. Paper keeps its historical size so
+    its book stays comparable with itself; live starts small and separate."""
+    if orders_are_real():
+        return float(getattr(config, 'LIVE_FIXED_MARGIN_USDT', 40.0))
+    return float(getattr(config, 'PAPER_FIXED_MARGIN_USDT',
+                         getattr(config, 'FIXED_MARGIN_USDT', 2000.0)))
+
+
+def _require_live(what):
+    """Re-read BOTH flags at the syscall boundary. Defence in depth: a stale
+    mode value held by a caller can never reach the exchange through here."""
+    if not orders_are_real():
+        raise OrdersDisabled(
+            f"refusing to {what}: LIVE_TRADING_ENABLED="
+            f"{getattr(config, 'LIVE_TRADING_ENABLED', False)} "
+            f"ORDER_ADAPTER_LIVE={getattr(config, 'ORDER_ADAPTER_LIVE', False)}")
+
+
+# ---------------------------------------------------------------------------
+# Exchange minimums — this check exists NOWHERE in the bot today
+# ---------------------------------------------------------------------------
+
+def check_size(exchange, symbol, amount, price):
+    """(ok, adjusted_amount, reason). Enforces limits.amount.min / limits.cost.min
+    and rounds to the amount step. Runs in BOTH modes on purpose: paper must
+    reject anything live would reject, or paper stops predicting live.
+
+    Measured 2026-07-29 on BTC/USDT:USDT — min amount 0.0001 BTC ($6.40 at
+    64k), min cost $2.00, amount step 0.0001. At the intended $200 notional
+    (0.0031 BTC) there is 31x headroom; the check exists for the day the size
+    is turned down, not for today.
+    """
+    try:
+        amt = float(exchange.amount_to_precision(symbol, amount))
+    except Exception as e:
+        return False, None, f'amount_to_precision failed: {e}'
+    if amt <= 0:
+        return False, None, f'amount rounds to zero at exchange step (raw {amount})'
+    try:
+        limits = (exchange.market(symbol) or {}).get('limits') or {}
+    except Exception as e:
+        # Cannot read the market: fail CLOSED. An unknown minimum is not a
+        # licence to send — mirrors risk_manager's fail-closed convention.
+        return False, None, f'market limits unreadable, failing closed: {e}'
+    min_amt = ((limits.get('amount') or {}).get('min'))
+    min_cost = ((limits.get('cost') or {}).get('min'))
+    if min_amt is not None and amt < float(min_amt):
+        return False, None, (f'amount {amt} below exchange minimum {min_amt} '
+                             f'({symbol})')
+    if min_cost is not None and price and (amt * float(price)) < float(min_cost):
+        return False, None, (f'notional ${amt * float(price):.2f} below exchange '
+                             f'minimum ${float(min_cost):.2f} ({symbol})')
+    return True, amt, f'ok (amount {amt}, notional ${amt * float(price or 0):.2f})'
+
+
+# ---------------------------------------------------------------------------
+# The three fills
+# ---------------------------------------------------------------------------
+# Every one returns the SAME shape, which is the shape virtual_trader already
+# passes around (virtual_trader.py:829-841 == main.py:1221-1227):
+#
+#   {'order': <ccxt order or synthetic>, 'fill_price': float, 'amount': float,
+#    'fee_cost': float, 'simulated': bool}
+#
+# `ref_price` is the price the DECISION was made at. Simulated, it IS the fill —
+# reproducing today's arithmetic exactly. Live, it is only a fallback for when
+# the exchange does not report an average.
+
+def _sim(kind, ref_price, amount, tag):
+    return {
+        'order': {'id': f'VIRT-{tag}', 'average': ref_price, 'price': ref_price},
+        'fill_price': float(ref_price),
+        'amount': float(amount),
+        'fee_cost': float(ref_price) * float(amount) * SIM_FEE_RATE,
+        'simulated': True,
+    }
+
+
+def _live_fill(exchange, order, symbol, amount, ref_price):
+    """Extract the REAL fill price, size and fee from an exchange response.
+    Fee comes from main.fetch_order_fee (already battle-tested, 2 attempts);
+    when the exchange does not report one we fall back to the taker estimate
+    rather than silently booking zero — a None fee that becomes 0 overstates
+    PnL, which is failure mode §7.4 of the scoping study."""
+    import main as _m
+    o = order or {}
+    fill_price = float(o.get('average') or o.get('price') or ref_price)
+    filled = o.get('filled')
+    try:
+        filled = float(filled) if filled is not None else None
+    except (TypeError, ValueError):
+        filled = None
+    executed = filled if filled else float(amount)
+    fee = None
+    if o.get('id'):
+        fee = _m.fetch_order_fee(o['id'], symbol)
+    fee_estimated = fee is None
+    if fee_estimated:
+        fee = fill_price * executed * SIM_FEE_RATE
+        print(f"[ADAPTER] fee not reported by exchange for order {o.get('id')} — "
+              f"ESTIMATED at taker rate ${fee:.6f}", flush=True)
+    return {
+        'order': o, 'fill_price': fill_price, 'amount': executed,
+        'fee_cost': abs(float(fee)), 'simulated': False,
+        'fee_estimated': fee_estimated,
+        'partial_fill': filled is not None and abs(executed - float(amount)) > 1e-12,
+    }
+
+
+def market_entry(exchange, symbol, side, position_side, amount, ref_price,
+                 leverage=None):
+    """Open. Returns the fill dict, or None when the order was refused locally
+    (size below the exchange minimum) — the caller must treat None as NO
+    POSITION and must not write a row."""
+    ok, amt, why = check_size(exchange, symbol, amount, ref_price)
+    if not ok:
+        print(f"[ADAPTER] ENTRY REFUSED {symbol} {position_side}: {why}", flush=True)
+        return None
+    if not orders_are_real():
+        return _sim('entry', ref_price, amt, 'ENTRY')
+    _require_live('send an entry order')
+    if leverage:
+        try:
+            exchange.set_leverage(leverage, symbol, params={'side': position_side})
+        except Exception as e:
+            print(f"[ADAPTER] set_leverage warn: {e}", flush=True)
+    order = exchange.create_market_order(
+        symbol, side, amt, params={'positionSide': position_side})
+    res = _live_fill(exchange, order, symbol, amt, ref_price)
+    if res.get('partial_fill'):
+        print(f"[ADAPTER] 🔴 PARTIAL FILL on entry {symbol} {position_side}: "
+              f"asked {amt}, filled {res['amount']}", flush=True)
+    print(f"[ADAPTER] LIVE ENTRY {symbol} {position_side} {res['amount']} "
+          f"@ {res['fill_price']} fee={res['fee_cost']:.6f}", flush=True)
+    return res
+
+
+def market_close(exchange, symbol, position_side, amount, ref_price):
+    """Full close. Live, this reuses the battle-tested close mechanics in
+    main._execute_close_position — cancel this side's triggers, close the REAL
+    on-exchange size, then re-sweep orphaned stops — rather than reimplementing
+    them. Falls back to the simulated shape when the live path finds nothing."""
+    if not orders_are_real():
+        return _sim('close', ref_price, amount, 'CLOSE')
+    _require_live('send a close order')
+    import main as _m
+    res = _m._execute_close_position(symbol, position_side)
+    if res is None:
+        print(f"[ADAPTER] 🔴 close requested but NO live position found for "
+              f"{symbol} {position_side} — nothing sent", flush=True)
+        return None
+    fee = res.get('fee_cost')
+    fee_estimated = fee is None
+    if fee_estimated:
+        fee = float(res['fill_price']) * float(res['amount']) * SIM_FEE_RATE
+        print(f"[ADAPTER] close fee not reported — ESTIMATED ${fee:.6f}", flush=True)
+    return {
+        'order': res.get('order'), 'fill_price': float(res['fill_price']),
+        'amount': float(res['amount']), 'fee_cost': abs(float(fee)),
+        'simulated': False, 'fee_estimated': fee_estimated,
+    }
+
+
+def market_reduce(exchange, symbol, position_side, amount, ref_price):
+    """Partial reduce-only exit (the LONG 1/3). Separate from market_close
+    because it must NOT cancel the position's protective orders — the remainder
+    keeps riding the unchanged contract."""
+    ok, amt, why = check_size(exchange, symbol, amount, ref_price)
+    if not ok:
+        print(f"[ADAPTER] PARTIAL REFUSED {symbol} {position_side}: {why}", flush=True)
+        return None
+    if not orders_are_real():
+        return _sim('reduce', ref_price, amt, 'PARTIAL')
+    _require_live('send a reduce-only order')
+    close_side = 'sell' if position_side == 'LONG' else 'buy'
+    order = exchange.create_market_order(
+        symbol, close_side, amt,
+        params={'positionSide': position_side, 'reduceOnly': True})
+    res = _live_fill(exchange, order, symbol, amt, ref_price)
+    print(f"[ADAPTER] LIVE PARTIAL {symbol} {position_side} {res['amount']} "
+          f"@ {res['fill_price']} fee={res['fee_cost']:.6f}", flush=True)
+    return res
```

---

# ЧАСТЬ 4. ЧЕТЫРЕ ОПАСНЫХ ПУНКТА — ПРЕДЛОЖЕНИЯ. НЕ РЕАЛИЗОВАНО, ЖДЁТ ТВОЕГО СЛОВА

## 11. ВЛАДЕНИЕ СТОПОМ — наш поллер против биржевого `STOP_MARKET`

Инвариант, который обязан уцелеть в любом варианте: **`main.py:1378-1405` — стоп не встал за 3
попытки → аварийное рыночное закрытие + крик.** Позиция без защиты не живёт ни секунды.

| | **A. Биржевой стоп (как в нынешнем боевом пути)** | **B. Наш поллер шлёт рыночный ордер** | **C. Гибрид: биржевой стоп + поллер как надзор** |
|---|---|---|---|
| Защита при обрыве связи / падении процесса | **ЕСТЬ** — стоп живёт на бирже | **НЕТ** — умер процесс, умер стоп | **ЕСТЬ** |
| Совпадение с бумажной книгой | ниже: срабатывает на фитиле, которого бумага не видела | **точное**: та же логика, тот же поллинг | ниже, как в A |
| Замерено 29.07 | эффект фитиля −60.47 на 51 позицию, но перекрыт +97.38 от заливки по уровню; **итог +36.91 в пользу A** | база сравнения | как A |
| Механизмы, требующие движения стопа (безубыток, recheck) | отмена + пересоздание, окно «голой» позиции | просто число в БД | отмена + пересоздание |
| Сложность | средняя (код уже есть: `_place_stop_with_retry`, `_handle_watching`) | низкая | высокая |
| Как ломается | окно между cancel и create | **тихо и целиком**: нет процесса — нет стопа | двойное владение одним стопом |

**🔴 РЕКОМЕНДУЮ A — биржевой `STOP_MARKET`.** Три причины, в порядке веса:
1. **Единственный вариант, где защита переживает нас самих.** B держит стоп в живости питоновского
   потока на 5x плече. Это не компромисс, это дефект.
2. **Замер снял главное возражение против A.** Я сам предполагал, что биржевой стоп срежет книгу.
   Измерил на 101 739 свечах: **+36.91, а не минус.** Возражение было эмпирическим и не выдержало.
3. **Код A уже написан и обкатан** — `_place_stop_with_retry`, `_handle_watching` с гонками,
   `_emergency_close`, `_report_passive_fill`. B пришлось бы писать с нуля и заново получать
   все те грабли.

Цена A, которую надо принять сознательно: окно между `cancel_order` и `create_order` при переносе
в безубыток. Оно уже обработано в `breakeven_worker.py:507-519` — отмена упала → проверить, не
залился ли стоп; всё ещё открыт → **держать СТАРЫЙ стоп** и повторить на следующем тике. Это
правильное поведение, и переизобретать его не нужно.

## 12. ДВОЙНОЕ УПРАВЛЕНИЕ — и заодно вопрос маршрутизации

**Факт:** `gunicorn.conf.py:102-103` запускает `virtual_trader.start_worker` **безусловно**, а
`_poll_once` (`virtual_trader.py:1772-1790`) **не проверяет `is_active()` вообще** — он управляет
любой строкой со `status='open'`. `breakeven_worker` стартует так же безусловно (`:109`).

Сегодня это безвредно: в бумаге `breakeven_jobs` пуст, в бою `virtual_positions` не наполняется.
**В момент переключения — нет:** незакрытая бумажная строка (сейчас это vpos 85) продолжит
управляться поллером, пока боевой путь ведёт настоящую позицию.

**ПРЕДЛОЖЕНИЕ — три части, все маленькие:**

**12а. Один хозяин на позицию, решается флагом, а не удачей.**
```python
# virtual_trader._poll_once, в начале
if order_adapter.orders_are_real() and not ADAPTER_OWNS_POSITIONS:
    return          # боевым путём рулит breakeven_worker — поллер молчит
```
**12б. Маршрутизация (то же решение, другой конец).** `main.py:1175` и `main.py:1250` ветвятся по
`is_active()`. Чтобы адаптер вообще заработал, ветвление должно спрашивать **«кто хозяин»**, а не
**«симулируем ли»**:
```python
# было:  if virtual_trader.is_active():        -> not LIVE_TRADING_ENABLED
# станет: if virtual_trader.engine_owns_position():
#              -> True всегда, пока мы не решим вернуться на legacy-путь
```
То есть бумажный движок ведёт позицию **всегда**, а адаптер решает, симулируются заливки или нет.
Это и есть «один движок, два адаптера» из твоего решения от 26.07, доведённое до маршрутизации.

**12в. Взаимное исключение при старте.** Если `orders_are_real()` и в `virtual_positions` есть
открытая строка, **не подниматься молча**: крик в Telegram + отказ стартовать торговлю до ручного
разбора. Открытая бумажная позиция в момент включения боя — это не штатная ситуация.

**Порядок важен:** 12б **нельзя** делать раньше 11, потому что «кто хозяин» определяет, кто ставит
стоп. Сначала 11, потом 12.

## 13. СВЕРКА ПОСЛЕ РЕСТАРТА

`reconcile_boot_state` (`main.py:4465`) сверяет **биржу** против `trades` + `breakeven_jobs`.
`virtual_positions` не сверяет никто.

**ПРЕДЛОЖЕНИЕ: `_reconcile_virtual_side(symbol, side)`, вызывается из `reconcile_boot_state`
сразу после `_reconcile_side`, и действует ТОЛЬКО когда `orders_are_real()`.** Матрица четырёх
состояний — единственный способ не оставить дыру:

| строка в `virtual_positions` | позиция на бирже | действие |
|---|---|---|
| open | есть, размер совпал | **норма** — сверить `sl_price` с реальным `STOP_MARKET`; расходится → выровнять и сказать |
| open | есть, размер НЕ совпал | 🔴 частичная заливка или ручное вмешательство → **не торговать**, крик, ручной разбор |
| open | **НЕТ** | позиция закрылась, пока нас не было → **дозакрыть строку** по факту с биржи. Цена и комиссия берутся `breakeven_worker._report_passive_fill` — механизм для ровно этого случая уже написан |
| closed/нет | **ЕСТЬ** | 🔴 сирота на бирже → **крик, НЕ ТРОГАТЬ.** Может быть не наша позиция |

**Про дыру №8 из трассировки.** Сегодня `_reconcile_side`, найдя голую реальную позицию, вешает
на неё стоп **независимо от режима**. В бумажном режиме это означает: бот ставит ордер на
позицию, которую он не открывал. Два варианта, и я не выбираю за тебя:
- **13-I:** в бумажном режиме — только кричать, не трогать. Чисто по принципу «не рулим чужим»,
  но реальная позиция может остаться без стопа.
- **13-II:** оставить как есть (вешать стоп всегда). Защищает позицию, но нарушает «в бумаге ноль
  ордеров» — то самое требование №2.
**Склоняюсь к 13-I** и громкой тревоге: непрошеный ордер на чужую позицию — тот класс ошибки,
который уже кусал (`project_snapshot_26jul_fb_post_live_channels`). Но это твой вызов.

## 14. ЧАСТИЧНЫЕ ЗАЛИВКИ

`filled_legs` пишется из НАМЕРЕНИЯ (`virtual_trader.py:561-567`). От этого числа считаются 1R,
уровень безубытка, размер частички и размер закрытия. Залилось пол-ордера — всё поехало, и никто
не скажет.

**Уже сделано в патче (первый слой):** `_live_fill()` читает `order['filled']`, возвращает
**исполненный** размер, ставит флаг `partial_fill` и **орёт в лог**; `execute_entry` пишет в
`filled_legs` то, что реально исполнилось, а не то, что просили.

**ПРЕДЛОЖЕНИЕ — что осталось, три шага:**
1. **Читать позицию, а не ответ ордера.** Ответ на рыночный ордер приходит до полного заполнения.
   Правда — `main._fetch_open_position(symbol, side)['contracts']`, через короткую паузу после
   отправки. Функция есть, переиспользуется.
2. **Порог расхождения — политика, не эвристика.** `|исполнено − заказано| / заказано > X` →
   **не открывать позицию**: закрыть остаток рыночным и не писать строку. Половинчатая позиция с
   правильно посчитанным 1R всё равно хуже отсутствия позиции. `X` предлагаю 0.02, но это число
   надо назначить сознательно.
3. **Стоп ставится на ФАКТИЧЕСКИЙ размер.** `create_order(..., closePosition='true')` уже делает
   это правильно — он закрывает позицию целиком независимо от `amount`. То есть при варианте 11-A
   эта часть уже безопасна, и это ещё один аргумент за A.

**Оговорка:** на BTC при $200 частичная заливка практически невероятна — 0.0031 BTC против 1533
BTC видимой глубины. Механизм нужен не для BTC-сегодня, а чтобы «залилось не всё» никогда не
превращалось в тихо неверную математику.

---

# ЧТО Я НЕ СДЕЛАЛ И ПОЧЕМУ

- **Не тронул маршрутизацию** (`main.py:1175/1250`) — это пункт 12, и без решения по пункту 11 он
  недоопределён. Следствие названо прямо в §5: адаптер сейчас **достижим только из бумажного
  пути**, а при включении обоих флагов будет обойдён. Об этом кричит `routing_warning()`.
- **Не тронул дыру №8** (сверка ставит стоп в бумажном режиме) — §13, меняет защитное поведение.
- **Не сделал баннер жёстким отказом от старта** — сказал бы, что это правильнее, но «бот не
  поднялся» тоже последствие, и оно твоё.
- **Не трогал `VIRTUAL_TARGET_CYCLES`, `is_active()` и ничего в стратегии.** Ни один порог, ни
  один вес, ни одно правило входа не изменены.

# ПРОВЕРКИ, КОТОРЫЕ Я ПРОГНАЛ

| Проверка | Результат |
|---|---|
| `py_compile` всех шести файлов | ✅ |
| `git apply --check -p1` против HEAD `5285495` | ✅ ложится чисто |
| Четыре комбинации флагов → `orders_are_real()` | ✅ True ровно в одной |
| `_require_live()` на трёх «неполных» комбинациях | ✅ `OrdersDisabled` во всех трёх |
| Арифметика симуляции против старой формулы | ✅ побитово (4.9971503400) |
| `check_size` против живого рынка BingX | ✅ $200 проходит, $6 и $1 отвергнуты |
| `routing_warning()` в бумаге / в бою | ✅ пусто / CRITICAL |
| Обработка нового возврата `None` из `_do_close` | ✅ все три места вызова (`main.py:2644`, `:2838`, `:2977`) уже имеют `if close is None` |
| Рабочее дерево после всей работы | ✅ чисто, `order_adapter.py` в бою отсутствует |

**Ничего не применено. Жду твоего чтения.**
Состояние на момент отправки: HEAD `5285495` = `origin/main`, дерево чисто, `titan.service` active,
`mercury-sol.service` active, vpos 85 открыта и не тронута, `LIVE_TRADING_ENABLED = False`.
