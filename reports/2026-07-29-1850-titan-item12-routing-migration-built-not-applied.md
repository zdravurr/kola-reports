# ПУНКТ 12 — МИГРАЦИЯ МАРШРУТИЗАЦИИ. ПОСТРОЕНО, НЕ ПРИМЕНЕНО
**2026-07-29 18:50 UTC** · база HEAD `5f054b7` · **рабочее дерево ЧИСТОЕ, патч НЕ НАЛОЖЕН**

```
 titan-bot/breakeven_worker.py | 36 ++++++++++---
 titan-bot/config.py           | 13 ++++--
 titan-bot/gunicorn.conf.py    |  4 +++
 titan-bot/main.py             | 81 ++++++++++++++++++++++++++--------
 titan-bot/order_adapter.py    | 73 ++++++++++++++++++++++++++++---
 titan-bot/virtual_trader.py   | 32 ++++++++++++++
 6 files changed, 210 insertions(+), 29 deletions(-)
```

> **ЧИТАЙ §1 ПЕРВЫМ.** Моё же предложение §12 из отчёта 16:22, применённое буквально, **ломает бой
> двумя способами**, а трассировка нашла **третью дверь** к двойному управлению, которой нет ни в
> твоём задании, ни в моём предложении. И **§6 — гейт: после этого пункта бой всё ещё НЕЛЬЗЯ
> включать**, и причина новая.

---

## 1. 🔴 МОЁ ПРЕДЛОЖЕНИЕ §12b БЫЛО НЕВЕРНЫМ. ДВА ДЕФЕКТА

`12b` звучал так: заменить `if virtual_trader.is_active():` на `engine_owns_position()`. Буквально
это даёт следующее.

### Дефект 1 — БЕСКОНЕЧНАЯ РЕКУРСИЯ на закрытии

```
virtual_trader._do_close
   └─> order_adapter.market_close          (боевая ветка)
         └─> main._execute_close_position
               └─> engine_owns_position() == True
                     └─> virtual_trader.close_position
                           └─> _do_close      ← ЦИКЛ, без дна
```

Сегодня цикла нет: в бою `is_active()` = False, и `_execute_close_position` идёт в настоящие
механики. `12b` инвертирует именно это условие. Проверено по коду: `virtual_trader.py:789`
(`_do_close` → `market_close`), `order_adapter.py:363` (`market_close` → `_execute_close_position`).

### Дефект 2 — АВАРИЙНОЕ ЗАКРЫТИЕ ПЕРЕСТАЁТ ЗАКРЫВАТЬ (страшнее первого)

Инвариант пункта 11: не встал стоп → закрыть по рынку немедленно. Путь:
`place_stop` → `_emergency_close` → `main._execute_close_position`.

`place_stop` вызывается **ДО вставки строки** (пункт 11, сознательно). Значит при `12b`:

```
_emergency_close -> _execute_close_position -> engine_owns_position() True
                 -> virtual_trader.close_position -> _open_position() -> строки НЕТ
                 -> return None -> «закрытие» НЕ ПРОИЗОШЛО
```

**Реальная позиция остаётся на бирже, без стопа, а мы считаем, что закрыли её.** Это ровно тот
исход, ради предотвращения которого инвариант существует.

### Решение: `_execute_close_position(..., _from_adapter=False)`

Два внутренних вызывающих обязаны получить **сырые** механики и не маршрутизироваться обратно:
`order_adapter.market_close` и `breakeven_worker._emergency_close` (плюс legacy SL-failsafe
`main.py:1393`). Стратегические закрытия — AI-close, armed exit, Smart TP, trend-reversal —
остаются маршрутизируемыми, в этом и смысл пункта 12.

Проверено исполнением (подменённый модуль `main`):
```
market_close called main._execute_close_position with _from_adapter = [True]
-> маршрутизация обойдена, повторного входа в _do_close нет: True
```

---

## 2. 🔴 ТРЕТЬЯ ДВЕРЬ К ДВОЙНОМУ УПРАВЛЕНИЮ — ЧЕРЕЗ СВЕРКУ, А НЕ ЧЕРЕЗ ВХОД

Ни в задании, ни в моём §12 её нет. `breakeven_worker.enqueue` вызывается из **двух** мест:

| место | путь | закрыто чем |
|---|---|---|
| `main.py:1412` | legacy-вход | `engine_owns_position()` делает ветку недостижимой |
| **`main.py:4387`** | **`_resume_job_if_needed` ← `_reconcile_side` ← `reconcile_boot_state`** | **ничем не было** |

`_reconcile_side` бежит **на КАЖДОМ старте** и, найдя реальную позицию на бирже, ставит
breakeven-джобу. То есть **любой рестарт в бою создавал бы второго управляющего** для позиции,
которой уже управляет движок. Дверь открыта не входом, а сверкой.

Закрыто **в корне** — `_resume_job_if_needed` возвращается сразу, когда движок владеет позициями,
и **бэкстопом** — стенд-даун в `breakeven_worker._poll_once`.

---

## 3. МАРШРУТНЫХ ТОЧЕК СЕМЬ, А НЕ ДВЕ

`grep is_active()` дал 7 живых мест. Классифицировал каждое:

| # | место | вопрос, на который оно на самом деле отвечает | стало |
|---|---|---|---|
| 1 | `main.py:1176` `_execute_close_position` | кто управляет | `engine_owns_position()` + `_from_adapter` |
| 2 | `main.py:1251` `_execute_entry` | кто управляет | `engine_owns_position()` |
| 3 | `main.py:2764` чтение позиции для arming | **в каком хранилище** позиция | `engine_owns_position()` |
| 4 | `main.py:3155` чтение для trend-reversal | то же | `engine_owns_position()` |
| 5 | `main.py:3170` закрытие по reversal | кто управляет | `engine_owns_position()` |
| 6 | `breakeven_worker:375` дормантность `_report_passive_fill` | кто управляет | `engine_owns_position()` |
| 7 | **`main.py:928` `is_virtual`** | **симулированы ли ЗАЛИВКИ** | **`not orders_are_real()`** |

**№7 — отдельный дефект данных, найден по дороге.** `is_virtual` помечает строку `trades` как
бумажную. Он спрашивал `is_active()` (= `not LIVE_TRADING_ENABLED`), но правильный вопрос —
«симулированы ли заливки». При `LIVE_TRADING_ENABLED=True` и `ORDER_ADAPTER_LIVE=False` заливки
симулируются, а `is_active()` вернёт False → **симулированные сделки пометились бы как реальные и
потекли бы в статистику баланса/P&L.** Исправлено на `orders_are_real()`.

Предикат введён своим именем, `is_active()` **не перегружен**, и в его докстроку добавлено
предупреждение «это не маршрутный предикат».

---

## 4. 12a — ОДИН ХОЗЯИН. КТО ЧЕМ ВЛАДЕЕТ

| режим | `virtual_positions` | `breakeven_jobs` |
|---|---|---|
| **бумага** (оба флага False) | `virtual_trader` | никто |
| **бой** (оба True) | `virtual_trader` — заливки реальные через адаптер | никто |

**Доказательство, что позицией не могут управлять оба — три независимых замка:**

1. **Строки не могут появиться.** Обе двери к `enqueue` закрыты (§2): legacy-вход недостижим,
   сверка возвращается раньше.
2. **По ФЛАГУ, а не по обстоятельству.** `breakeven_worker._poll_once` возвращает `0` сразу, когда
   `engine_owns_position()`. Пустая таблица — обстоятельство; это флаг. Урок из `96b83d4`.
3. **Fail-safe.** Если владелец не определяется (исключение) — воркер тоже стоит. Застрявший
   безубыток восстановим; два хозяина на одной позиции — нет.

Проверено исполнением: `_poll_once` вернул `0`, **не прочитав ни одной позиции и не отправив ни
одного ордера** (мок падал бы на `create_order`/`cancel_order`/`fetch_positions`). Наблюдательные
тики выше стенд-дауна работают дальше — в `post_exit_observatory` и `skip_attribution`
**ноль** вхождений `create_order`/`cancel_order`, проверено `grep`.

---

## 5. 12c — ВЗАИМНОЕ ИСКЛЮЧЕНИЕ ПРИ СТАРТЕ

`order_adapter.assert_single_owner_at_boot()`, вызывается в `gunicorn.conf.py:when_ready` сразу за
баннером и **до сверки** (сверка сама умеет ставить ордера).

**Дискриминатор — ФАКТ В ДАННЫХ, а не догадка:** открытая строка с `stop_order_id IS NULL` создана,
когда стопом владел поллер, то есть в бумаге. В бою `place_stop` либо вернёт биржевой id, либо вход
прервётся и строки не будет (пункт 11). Значит `NULL + open + бой` ⟺ бумажная строка.

Проверено исполнением, четыре случая:
```
бумага + открытая бумажная строка      -> exit 0, ПУСКАЕТ (проверять нечего)
БОЙ    + открытая БУМАЖНАЯ строка      -> exit 3, ОТКАЗ, с перечислением строк
БОЙ    + открытая БОЕВАЯ строка        -> exit 0, ПУСКАЕТ (нормальный рестарт)
БОЙ    + позиций нет                   -> exit 0, ПУСКАЕТ
```
Строка «Fix:» сделана контекстной, и в ней прямо сказано **не редактировать `stop_order_id`, чтобы
заглушить проверку** — это объявило бы биржевой стоп, которого нет.

---

## 6. 🔴🔴 ГЛАВНОЕ: ПОСЛЕ ЭТОГО ПУНКТА БОЙ ВСЁ ЕЩЁ НЕЛЬЗЯ ВКЛЮЧАТЬ

Нашёл, трассируя первый боевой вход. **Это не дефект патча — это дыра, которую пункты 11 и 12
вместе ОБНАЖАЮТ, и её нет в списке блокеров.**

**Стоп стоит на бирже. Поллер про это не знает.**

`virtual_trader._process_position` секция 3 по-прежнему проверяет `last <= sl_price` и зовёт
`_do_close`. В бою на пробое стопа происходит вот что:

```
1. цена задевает sl_price -> БИРЖЕВОЙ STOP_MARKET срабатывает (на фитике, мгновенно)
2. позиция на бирже ЗАКРЫТА
3. через <=10 с поллер видит last <= sl_price -> _do_close
4. _do_close -> market_close -> _execute_close_position(_from_adapter=True)
5. _fetch_open_position -> None (уже закрыта) -> возвращает None
6. _do_close: "VIRTUAL CLOSE ABORTED ... row left OPEN for reconciliation" -> return None
7. СТРОКА ОСТАЁТСЯ status='open' НАВСЕГДА
```

Комментарий обещает «reconciliation», но **сверки для `virtual_positions` не существует**:
`reconcile_boot_state` её не касается вообще (проверено grep). Это и есть пункт 13, который ты
намеренно отложил.

**Последствие:** на КАЖДОМ боевом выходе по стопу строка не закроется, P&L не запишется, а
`ux_vpos_one_open_per_side` заблокирует следующий вход на этой стороне. Бой встанет после первой же
сделки — молча, «успешно».

Легаси-путь эту проблему решал через `_report_passive_fill`. **У движка эквивалента нет.**

**Вывод: пункт 13 (пассивные заливки / сверка `virtual_positions`) становится ЖЁСТКИМ
ПРЕДУСЛОВИЕМ боя, а не «потом».** Записывать в OPEN-ITEMS как блокер C того же класса.

---

## 7. ТРЕЙЛ — ТЫ ПРАВ, БЛОКЕР A ОБОЙДЁН. ВОТ ДОКАЗАТЕЛЬСТВО

Подтверждаю: конфигурация «стоп на бирже + трейл у поллера» **действительно полностью обходит
блокер A**, и вот почему, а не «на слово»:

1. `TRAILING_STOP_MARKET` создаётся **ровно в одном месте** — `breakeven_worker._attempt_trail`.
2. Оно достижимо только из `_poll_once` при наличии джобы, а `_poll_once` теперь **возвращается
   раньше** (§4, замок 2), и джобы **не могут появиться** (§2 и §4, замок 1).
3. Трейл движка — не ордер, а **условие закрытия** поллера → `market_close` → рыночный ордер.

Значит **в любой момент времени существует ровно ОДИН `closePosition` ордер** — тот `STOP_MARKET`,
что поставил пункт 11 (при безубытке он отменяется и создаётся заново, по одному за раз).
Два `closePosition` ордера сосуществовать не могут. **Блокер A недостижим по построению.**

Цена принята и записана: трейл не переживает смерти процесса. Это стоит **прибыли, не риска** —
к моменту арминга трейла биржевой стоп уже стоит на безубытке.

---

## 8. ЧТО СДЕЛАЕТ ПЕРВЫЙ БОЕВОЙ ВХОД — ПОШАГОВО

Размер: `LIVE_FIXED_MARGIN_USDT = 30.0` × `LEVERAGE 5` = **$150** нотионала ≈ **0.0023 BTC** @ 64k.
`LEVERAGE` **не тронут** — он общий с бумагой.

| # | шаг | что произойдёт | если упадёт |
|---|---|---|---|
| 1 | вебхук TradingView → `webhook()` | сигнал пишется в `trades`, **`is_virtual=0`** (§3 №7) | — |
| 2 | гейты: HTF-каскад, score, veto | не прошёл → `htf_blocked`/`below_threshold`, входа нет | — |
| 3 | `_execute_entry` | `engine_owns_position()` **True** → `virtual_trader.execute_entry`. Legacy-ветка **не достижима** | — |
| 4 | размер | `active_fixed_margin()` = **30.0** → нотионал $150 → `amount ≈ 0.0023` | — |
| 5 | `check_size` | сверка с минимумом биржи | ниже минимума → **отказ, позиции нет, строки нет** |
| 6 | `market_entry` | `set_leverage(5)`, затем `create_market_order` | `set_leverage` падает → **только warn**, вход продолжается; `create_market_order` падает → исключение вверх, строки нет |
| 7 | `_live_fill` | читает реальные цену/размер/комиссию; `fetch_order_fee` | комиссия не отдана → **оценка по тейкерской ставке + печать** |
| 8 | частичная заливка | **печатается громко**; порог `0.02` записан, но **пункт 14 не реализован — НИЧЕГО не делает** | позиция остаётся частичной, 1R посчитан от неверного размера |
| 9 | `sl_price` | `fill − 2.5×ATR`, `price_to_precision` | — |
| 10 | **`place_stop`** | `STOP_MARKET closePosition='true'`, 3 попытки | все 3 упали → **`_emergency_close` → реальное рыночное закрытие + крик → `place_stop` вернёт None → строка НЕ пишется** |
| 11 | проверка вместимости / `INSERT` | строка с `stop_order_id` | любой из двух абортов → **`cancel_stop` снимает только что поставленный стоп**; если и отмена упала → 🚨 `MANUAL ACTION REQUIRED` |
| 12 | позиция живёт | защищена биржевым стопом; ведёт её `virtual_trader` | — |
| 13 | T+10/60/300 recheck | `TIGHTEN` → `move_stop` cancel+create, граница `93c20c3` в силе | отмена упала → **старый стоп остаётся**, тир повторится |
| 14 | +1R безубыток | `move_stop` cancel+create на BE | то же; отмена ок + создание упало → **аварийное закрытие** |
| 15 | трейл | **поллер**, `market_close` рыночным ордером | процесс умер → трейла нет, но стоп на безубытке стоит |
| 16 | **выход по стопу** | 🔴 **см. §6 — строка НЕ ЗАКРОЕТСЯ** | **это и есть блокер C** |

---

## 9. ЧТО МОЖЕТ ПОЙТИ НЕ ТАК — мой список

1. **🔴 Блокер C (§6)** — пассивная заливка биржевого стопа не закрывает строку. Бой встанет после
   первой сделки. **Пункт 13 обязателен до боя.**
2. **🔴 Ни одна боевая ветка не проверялась против настоящей биржи.** Всё — моки. Это относится и к
   пункту 11, и к пункту 12.
3. **Legacy-путь входа стал мёртвым кодом**, но остался в файле. Он не удалён намеренно (это не
   мой мандат), однако теперь это ~200 строк, которые выглядят рабочими и не исполняются никогда.
4. **`_from_adapter` — вручную поддерживаемый инвариант.** Новый вызывающий, которому нужны сырые
   механики, обязан не забыть флаг. Компилятор этого не проверит.
5. **`is_virtual` меняет семантику данных.** Старые строки писались по `is_active()`. Смысл теперь
   строже и правильнее, но при сравнении выборок через границу этого коммита это надо помнить.
6. **12c читает `stop_order_id` как признак бумаги.** Если пункт 13 когда-нибудь начнёт писать
   строки другим путём, признак надо пересматривать вместе с ним.
7. **`assert_single_owner_at_boot` в `gunicorn` завёрнут в общий `try/except`** вместе с баннером.
   `os._exit(3)` исключением не является и не перехватывается, так что отказ работает; но если
   функция бросит **до** `_refuse_to_start`, исключение будет проглочено и бот поднимется.
   Внутри она уже ловит всё сама и в ошибке отказывает — но связка хрупкая.
8. **Пункт 14 не реализован**, порог `0.02` записан и никем не читается (шаг 8 таблицы §8).

---

## 10. ПОЛНЫЙ ДИФФ (НЕ ПРИМЕНЁН)

`git apply --check` против живого дерева на `5f054b7` — **чисто**. `git status --porcelain` пуст.
`py_compile` — все шесть файлов OK.

```diff
diff --git a/titan-bot/breakeven_worker.py b/titan-bot/breakeven_worker.py
index 71e77d8..3643ae8 100644
--- a/titan-bot/breakeven_worker.py
+++ b/titan-bot/breakeven_worker.py
@@ -297,7 +297,12 @@ def _emergency_close(symbol, position_side, send_tg, last_err):
             pass
     try:
         import main
-        result = main._execute_close_position(symbol, position_side)
+        # RAW mechanics, never re-routed: this fires when a stop could not be
+        # placed, which for a fresh entry happens BEFORE the virtual_positions
+        # row exists. Re-routing would find no row, return None, and leave a
+        # REAL position open with NO STOP — see main._execute_close_position.
+        result = main._execute_close_position(symbol, position_side,
+                                              _from_adapter=True)
         print(f"[BE-FAILSAFE] emergency close result: {result}", flush=True)
         if send_tg:
             try:
@@ -368,11 +373,12 @@ def _report_passive_fill(exchange, send_tg, job, transition):
     """
     if send_tg is None:
         return
-    # (b) dormancy: do nothing while virtual. Fail SAFE (return) if mode is
-    # indeterminate — in virtual mode there are no jobs anyway.
+    # (b) dormancy: do nothing while the ENGINE owns positions (item 12). Fail
+    # SAFE (return) if ownership is indeterminate — when the engine owns them
+    # there are no jobs here anyway.
     try:
         import virtual_trader
-        if virtual_trader.is_active():
+        if virtual_trader.engine_owns_position():
             return
     except Exception as e:
         print(f"[BE-FILL] mode check failed, not reporting: {e}", flush=True)
@@ -673,6 +679,28 @@ def _poll_once(exchange, send_tg=None):
             skip_attribution_tick(exchange, shared_prices=shared_prices)
         except Exception as _sa_err:
             print(f"[SKIP-ATTR] tick failed: {_sa_err}", flush=True)
+    # ── SINGLE OWNER (item 12a) ──────────────────────────────────────────────
+    # ONE mechanism manages a position, decided BY FLAG and not by circumstance.
+    # Once routing is migrated, virtual_trader owns every position in both
+    # modes, so this worker manages nothing and must not touch a job even if one
+    # somehow exists. Note the observational ticks above still run — they place
+    # no orders and read no position state this worker would then act on.
+    #
+    # This guard is deliberately belt-and-braces with the fact that
+    # breakeven_jobs can no longer GAIN rows (enqueue() is called only from
+    # main.py's legacy live entry, which engine_owns_position() makes
+    # unreachable). "The table is empty" is a circumstance; this is the flag.
+    try:
+        import virtual_trader
+        if virtual_trader.engine_owns_position():
+            return 0
+    except Exception as e:
+        # Fail SAFE: if ownership cannot be determined, do nothing. A stalled
+        # breakeven is recoverable; two owners on one position is not.
+        print(f"[BE] ownership check failed, standing down this tick: {e}",
+              flush=True)
+        return 0
+
     with sqlite3.connect(DB_PATH) as conn:
         conn.row_factory = sqlite3.Row
         jobs = conn.execute(
diff --git a/titan-bot/config.py b/titan-bot/config.py
index 31f2b9d..9751273 100755
--- a/titan-bot/config.py
+++ b/titan-bot/config.py
@@ -52,7 +52,13 @@ ORDER_ADAPTER_LIVE = False
 # This is flipped BY the design-item-12 change itself, as part of the commit
 # that migrates the routing. It is NOT an operator dial and must never be set
 # to True to "make the error go away".
-ROUTING_MIGRATED_TO_ADAPTER = False
+# 2026-07-29, item 12: SET TO TRUE AS THE LAST LINE OF THE MIGRATION, and it
+# means what it says — main.py:1176/1251 (and the three ownership reads) now
+# branch on virtual_trader.engine_owns_position(), breakeven_worker stands down
+# while the engine owns positions, and assert_single_owner_at_boot() refuses a
+# live boot that still has an open paper row. This flag is what disarms the hard
+# refusal; it must never be set to make an error message go away.
+ROUTING_MIGRATED_TO_ADAPTER = True
 
 # ---------------------------------------------------------------------------
 # PARTIAL-FILL DIVERGENCE THRESHOLD — deliberate policy number, NOT YET WIRED.
@@ -99,7 +105,10 @@ FIXED_NOTIONAL_MODE = True
 # was traded at, so its history stays comparable with itself; live starts small
 # and is turned up deliberately, never by inheriting the paper number.
 PAPER_FIXED_MARGIN_USDT = 2000.0   # unchanged: 2000 × 5 = $10,000 notional
-LIVE_FIXED_MARGIN_USDT = 40.0      # 40 × 5 = $200 notional  (0.0031 BTC @ 64k)
+LIVE_FIXED_MARGIN_USDT = 30.0      # 30 × 5 = $150 notional  (0.0023 BTC @ 64k)
+# Operator decision 2026-07-29 for the FIRST live run. LEVERAGE is deliberately
+# NOT touched: it is shared with paper, and changing it would break the paper
+# book's comparability with its own history.
 
 # Back-compat alias. main.py's LEGACY live entry path still imports this name;
 # it resolves to the PAPER size, which is deliberate — that path is not the
diff --git a/titan-bot/gunicorn.conf.py b/titan-bot/gunicorn.conf.py
index 70e544a..d032cef 100755
--- a/titan-bot/gunicorn.conf.py
+++ b/titan-bot/gunicorn.conf.py
@@ -68,6 +68,10 @@ def when_ready(server):
     try:
         import order_adapter
         order_adapter.assert_startup_mode()
+        # 12c — mutual exclusion. Runs BEFORE reconciliation for the same reason
+        # the banner does: reconciliation can place an order, and it must never
+        # run while a paper position is still open in live mode.
+        order_adapter.assert_single_owner_at_boot()
     except Exception as e:
         print(f"ORDER-MODE banner failed: {e}", flush=True)
     try:
diff --git a/titan-bot/main.py b/titan-bot/main.py
index 485dc96..0bf1314 100644
--- a/titan-bot/main.py
+++ b/titan-bot/main.py
@@ -925,7 +925,12 @@ def insert_signal(parsed, symbol, side, intent, status='pending'):
     # virtual trades never bleed into balance/PnL stats. Status rows like
     # 'no_confluence' / 'ai_skipped' / 'filtered' are tagged too — they
     # belong to the same simulated session.
-    virtual_flag = (1,) if virtual_trader.is_active() else (0,)
+    # is_virtual answers "were the FILLS simulated?", so it must key off the
+    # adapter, not the master switch. Item 12 fix: with LIVE_TRADING_ENABLED=True
+    # but ORDER_ADAPTER_LIVE=False the fills ARE simulated while is_active() says
+    # False — that combination would have stamped simulated trades as real and
+    # bled them into balance/PnL stats.
+    virtual_flag = (0,) if order_adapter.orders_are_real() else (1,)
     cols_tuple = (_SIGNAL_INSERT_COLS + snap_cols
                   + ('mtf_alignment_score', 'is_virtual'))
     values = base_values + snap_values + (mtf_score,) + virtual_flag
@@ -1164,16 +1169,37 @@ def _cancel_stop_orders(symbol: str, position_side: str):
         print(f"[STOP-CLEANUP] no orphaned orders for {position_side} {symbol}")
 
 
-def _execute_close_position(symbol, position_side):
+def _execute_close_position(symbol, position_side, _from_adapter=False):
     """Cancel pending triggers/limits for the side, market-close the live
     position, and return a result dict. Mirrors the close mechanics in the
     legacy webhook() path so we keep the same hedge-mode behavior. Returns
     None if no live position is found.
+
+    `_from_adapter` — 🔴 NOT a style choice, it prevents unbounded recursion and
+    a broken emergency close. Two internal callers need the RAW exchange
+    mechanics below and must NOT be re-routed back to the engine:
+
+      1. order_adapter.market_close(), which is itself called BY
+         virtual_trader._do_close. Without this flag the cycle is
+             _do_close -> market_close -> _execute_close_position
+                       -> close_position -> _do_close -> ...
+         unbounded, and it appears the moment routing switches to
+         engine_owns_position() — see item 12 report §1.
+      2. breakeven_worker._emergency_close(), the item-11 invariant. It fires
+         when a stop could not be placed, which happens BEFORE the
+         virtual_positions row is inserted. Re-routing it would look for a row
+         that does not exist yet, return None, and leave a REAL position open
+         on the exchange with NO STOP — the exact outcome the invariant exists
+         to prevent.
+
+    Strategy-level closes (AI close, armed exit, Smart TP, trend reversal) keep
+    _from_adapter=False and route to the engine, which is the point of item 12.
     """
-    # Observation Mode: route to the simulator. The simulator returns the
-    # same dict shape (or None when no open virtual position exists), so
-    # every downstream close path is unchanged.
-    if virtual_trader.is_active():
+    # ROUTING (item 12): the engine that MANAGES the position closes it. This is
+    # engine_owns_position(), not is_active() — the position may be managed here
+    # while its fills are real. The simulator returns the same dict shape (or
+    # None when no open row exists), so downstream close paths are unchanged.
+    if not _from_adapter and virtual_trader.engine_owns_position():
         return virtual_trader.close_position(exchange, send_tg,
                                              symbol, position_side)
 
@@ -1245,10 +1271,14 @@ def _execute_entry(symbol, side, position_side, signal_row_id=None):
     through to virtual_trader so virtual_positions.trades_entry_row_id is
     populated. Ignored on the live exchange path.
     """
-    # Observation Mode: bypass exchange order placement. The simulator
-    # returns an identically shaped dict so downstream logging/Telegram
-    # paths are untouched.
-    if virtual_trader.is_active():
+    # ROUTING (item 12): the engine MANAGES every position, in both modes. It
+    # is order_adapter underneath that decides whether the fills are simulated
+    # or sent. This branch is therefore taken ALWAYS once the migration has
+    # landed, and the legacy live entry below becomes unreachable — deliberately
+    # so: it is the path missing seven mechanisms and sized off the PAPER margin.
+    # The simulator returns an identically shaped dict so downstream
+    # logging/Telegram paths are untouched.
+    if virtual_trader.engine_owns_position():
         # Post-entry-recheck baselines: 1h ADX from the request snapshot (free,
         # already computed this webhook) and the opposing-wall map fresh from the
         # book. entry_atr_pct_1h is left to execute_entry, which derives it from
@@ -1390,7 +1420,10 @@ def _execute_entry(symbol, side, position_side, signal_row_id=None):
         except Exception as _tg_err:
             print(f"[SL-FAILSAFE] TG alert failed: {_tg_err}")
         try:
-            _close_result = _execute_close_position(symbol, position_side)
+            # Emergency close: RAW mechanics, never re-routed (see the
+            # _from_adapter docstring).
+            _close_result = _execute_close_position(symbol, position_side,
+                                                    _from_adapter=True)
             print(f"[SL-FAILSAFE] Emergency close result: {_close_result}")
             try:
                 send_tg(f"✅ Emergency close executed for {symbol} {position_side}.")
@@ -2756,12 +2789,12 @@ def _handle_exit_signal(data):
     armed_sides = []
     expires_iso = None
     for side in ('LONG', 'SHORT'):
-        # Observation Mode: arm against the open VIRTUAL position so the
-        # Exit-Signal pipeline can be exercised on paper. Mirrors the
-        # is_active() branch in _execute_close_position. Live path
-        # (is_active() False) falls through to the real read unchanged.
+        # ROUTING (item 12): read the position from whichever store OWNS it.
+        # Mirrors the engine_owns_position() branch in _execute_close_position.
+        # Once migrated this is always the engine's row — including in live,
+        # where that row carries REAL fills.
         pos = (virtual_trader.get_open_position(symbol, side)
-               if virtual_trader.is_active()
+               if virtual_trader.engine_owns_position()
                else _fetch_open_position(symbol, side))
         if not pos:
             continue
@@ -3152,7 +3185,7 @@ def _handle_state_machine(data, action_field):
             # existing insert_signal/send_tg/return below regardless.
             opp_side = 'SHORT' if direction == 'LONG' else 'LONG'
             _rev_pos = (virtual_trader.get_open_position(symbol, opp_side)
-                        if virtual_trader.is_active()
+                        if virtual_trader.engine_owns_position()   # item 12
                         else _fetch_open_position(symbol, opp_side))
             if _rev_pos:
                 _, _, _cid, _ = signal_matrix.classify(signal_name)
@@ -3167,7 +3200,7 @@ def _handle_state_machine(data, action_field):
                         # Close directly with reason='trend_reversal' (the §3
                         # caveat): _execute_close_position would stamp
                         # 'external'. Live path keeps its existing mechanics.
-                        if virtual_trader.is_active():
+                        if virtual_trader.engine_owns_position():   # item 12
                             virtual_trader.close_position(
                                 exchange, send_tg, symbol, opp_side,
                                 reason='trend_reversal')
@@ -4379,6 +4412,17 @@ def _resume_job_if_needed(symbol, side, entry_price, sl_price, atr, trail_pct,
                           sl_order_id, amount):
     """Enqueue a breakeven job to resume +1R management iff none is active.
     The worker resumes any existing active job on its own."""
+    # ── SINGLE OWNER (item 12a), AT THE ROOT ────────────────────────────────
+    # This runs from _reconcile_side on EVERY boot that finds a real exchange
+    # position. Without this guard a live restart would enqueue a breakeven job
+    # for a position virtual_trader is already managing — two mechanisms, one
+    # position, created by RECONCILIATION rather than by the entry path. That
+    # door is not mentioned in the item-12 brief and it is wide open.
+    # breakeven_worker._poll_once carries the backstop; this is the root fix.
+    if virtual_trader.engine_owns_position():
+        print(f"[RECONCILE] engine owns positions — NOT enqueueing a breakeven "
+              f"job for {side} (item 12a: single owner)", flush=True)
+        return
     if breakeven_worker.active_job(symbol, side) is not None:
         return
     atr_val = atr if atr else abs(entry_price - sl_price) / max(SL_ATR_MULT, 1e-9)
@@ -4508,6 +4552,7 @@ if __name__ == '__main__':
     # Same loud banner as the gunicorn path, before reconciliation for the same
     # reason. The dev entrypoint must never be quieter about mode than prod.
     order_adapter.assert_startup_mode()
+    order_adapter.assert_single_owner_at_boot()      # 12c
     reconcile_boot_state()
     signal_weights.start_audit_worker(exchange, send_tg)
     mfe_tracker.start_worker(exchange, send_tg)
diff --git a/titan-bot/order_adapter.py b/titan-bot/order_adapter.py
index f71f4ad..8670bf4 100644
--- a/titan-bot/order_adapter.py
+++ b/titan-bot/order_adapter.py
@@ -112,6 +112,59 @@ def assert_startup_mode(send_tg=None):
     return tag, detail, master, adapter
 
 
+def assert_single_owner_at_boot(send_tg=None):
+    """12c — MUTUAL EXCLUSION AT BOOT. Refuses to start when going live with a
+    PAPER-CREATED position still open. NEVER RETURNS when it refuses.
+
+    An open paper position at the moment of going live is not a normal state: it
+    was opened with simulated fills at the PAPER size, and nothing on the
+    exchange corresponds to it. Coming up would leave the engine managing a row
+    whose "position" does not exist, sending real closes against nothing, and
+    counting its P&L into the live book.
+
+    THE DISCRIMINATOR IS A FACT IN THE DATA, NOT A GUESS. An open row with
+    stop_order_id IS NULL was created while the poller owned the stop — i.e. in
+    paper. In live, place_stop either returns a real exchange id or the entry
+    aborts and no row is written (item 11). So NULL + open + live == paper-made.
+
+    A live restart with a genuine live position (stop_order_id set) is a NORMAL
+    state and is allowed through untouched.
+    """
+    if not orders_are_real():
+        return True
+    try:
+        import sqlite3
+        import virtual_trader as _vt
+        with sqlite3.connect(_vt.DB_PATH) as conn:
+            conn.row_factory = sqlite3.Row
+            rows = conn.execute(
+                "SELECT id, symbol, position_side, initial_fill_price, opened_at "
+                "FROM virtual_positions "
+                "WHERE status='open' AND stop_order_id IS NULL"
+            ).fetchall()
+    except Exception as e:
+        # Cannot verify => cannot proceed. Going live blind is the one thing
+        # this function exists to prevent.
+        _refuse_to_start(
+            f"CANNOT VERIFY position ownership at boot: {e}\n"
+            "Refusing to start live with an unverifiable virtual_positions "
+            "state.", send_tg, fix=_FIX_PAPER_POSITION)
+
+    if not rows:
+        return True
+
+    detail = '\n'.join(
+        f"  vpos {r['id']}: {r['symbol']} {r['position_side']} "
+        f"@ {r['initial_fill_price']} opened {r['opened_at']}" for r in rows)
+    _refuse_to_start(
+        f"OPEN PAPER POSITION(S) PRESENT WHILE GOING LIVE — {len(rows)} row(s) "
+        f"with status='open' and NO exchange stop:\n{detail}\n"
+        "These were opened with SIMULATED fills at the PAPER size; nothing on "
+        "the exchange corresponds to them.\n"
+        "A human must close or archive them before live trading starts.",
+        send_tg, fix=_FIX_PAPER_POSITION)
+
+
 def _alert_throttled():
     """True when a refusal alert may be sent now. Restart=always/5s turns a
     refusal into a crash loop, so the Telegram alert is rate-limited across
@@ -132,7 +185,16 @@ def _alert_throttled():
     return True
 
 
-def _refuse_to_start(warn, send_tg=None):
+_FIX_ROUTING = ("Fix: set ORDER_ADAPTER_LIVE=False (and/or LIVE_TRADING_ENABLED"
+                "=False) in config.py, or complete the routing migration and set "
+                "ROUTING_MIGRATED_TO_ADAPTER=True.")
+_FIX_PAPER_POSITION = ("Fix: close or archive the open paper row(s), or set "
+                       "ORDER_ADAPTER_LIVE=False to stay in paper. Do NOT edit "
+                       "the row's stop_order_id to silence this — that would "
+                       "claim an exchange stop that does not exist.")
+
+
+def _refuse_to_start(warn, send_tg=None, fix=None):
     """HARD REFUSAL — the process does not come up. NEVER RETURNS.
 
     Operator decision 2026-07-29, and it is the right one: "the bot did not
@@ -155,9 +217,7 @@ def _refuse_to_start(warn, send_tg=None):
     print("[TITAN][ORDER-MODE] 🛑 REFUSING TO START — UNSAFE CONFIGURATION", flush=True)
     for line in warn.splitlines():
         print(f"[TITAN][ORDER-MODE] {line}", flush=True)
-    print("[TITAN][ORDER-MODE] Fix: set ORDER_ADAPTER_LIVE=False (and/or "
-          "LIVE_TRADING_ENABLED=False) in config.py, or complete the routing "
-          "migration and set ROUTING_MIGRATED_TO_ADAPTER=True.", flush=True)
+    print(f"[TITAN][ORDER-MODE] {fix or _FIX_ROUTING}", flush=True)
     print("[TITAN][ORDER-MODE] exiting with code 3 (unsafe configuration)", flush=True)
     print(bar, flush=True)
     if send_tg and _alert_throttled():
@@ -360,7 +420,10 @@ def market_close(exchange, symbol, position_side, amount, ref_price):
         return _sim('close', ref_price, amount, 'CLOSE')
     _require_live('send a close order')
     import main as _m
-    res = _m._execute_close_position(symbol, position_side)
+    # _from_adapter=True: run the RAW exchange mechanics. Without it this call
+    # re-enters the engine (item 12 routing) and recurses unbounded —
+    # _do_close -> market_close -> _execute_close_position -> close_position -> ...
+    res = _m._execute_close_position(symbol, position_side, _from_adapter=True)
     if res is None:
         print(f"[ADAPTER] 🔴 close requested but NO live position found for "
               f"{symbol} {position_side} — nothing sent", flush=True)
diff --git a/titan-bot/virtual_trader.py b/titan-bot/virtual_trader.py
index 8031fa2..b1820ca 100755
--- a/titan-bot/virtual_trader.py
+++ b/titan-bot/virtual_trader.py
@@ -370,9 +370,41 @@ def _virtual_entry_count():
         return 0
 
 
+def engine_owns_position():
+    """WHO MANAGES an open position — this engine, or main.py's legacy live path.
+
+    This is NOT is_active(), and the two must never be conflated again:
+
+        is_active()             -> "are the FILLS simulated?"  (not LIVE_TRADING_ENABLED)
+        engine_owns_position()  -> "who MANAGES the position?"
+
+    Before the routing migration those were the SAME switch, and that conflation
+    is the whole defect item 12 exists to remove: flipping LIVE_TRADING_ENABLED
+    would have handed the position to main.py's legacy path — a path missing
+    seven mechanisms this engine has, sized off the PAPER margin.
+
+    The operator's 2026-07-26 decision is ONE ENGINE, TWO ADAPTERS. So: this
+    engine manages EVERY position in BOTH modes, and order_adapter decides only
+    whether the fills underneath are simulated or sent to the exchange.
+
+    Returns True once config.ROUTING_MIGRATED_TO_ADAPTER is set. If that flag is
+    ever put back to False the predicate degrades to the OLD behaviour (this
+    engine owns paper only), so the flag reverts routing honestly rather than
+    leaving a half-migrated state behind.
+    """
+    import config as _cfg
+    if bool(getattr(_cfg, 'ROUTING_MIGRATED_TO_ADAPTER', False)):
+        return True
+    return is_active()
+
+
 def is_active():
     """True == still in VIRTUAL (paper) mode; False == placing REAL orders.
 
+    ⚠️ THIS IS NOT A ROUTING PREDICATE. It answers "are fills simulated?" only.
+    For "who manages the position?" use engine_owns_position(). Routing on this
+    function is the item-12 defect; do not reintroduce it.
+
     Gated SOLELY by the manual master switch config.LIVE_TRADING_ENABLED:
         LIVE_TRADING_ENABLED is False  -> always virtual (returns True),
                                           NO MATTER what cycle_count() is.
```
