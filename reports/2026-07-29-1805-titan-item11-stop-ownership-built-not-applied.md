# ПУНКТ 11 — ВЛАДЕНИЕ СТОПОМ. ПОСТРОЕНО, НЕ ПРИМЕНЕНО
**2026-07-29 18:05 UTC** · база HEAD `96b83d4` · **рабочее дерево ЧИСТОЕ, патч НЕ НАЛОЖЕН**

> **СТАТУС.** Патч собран в изолированной копии, `git apply --check` против живого дерева —
> **чисто**. В `/root/titan-bot` не изменено ни одного байта. Оба флага режима False.
> **Трейл НЕ тронут** — это отдельное решение, и оно ниже (§4), с рекомендацией.

```
 titan-bot/breakeven_worker.py | 103 ++++++++++++++++++++++--------
 titan-bot/order_adapter.py    |  89 ++++++++++++++++++++++++++
 titan-bot/virtual_trader.py   | 110 ++++++++++++++++++++++++++++---
 3 files changed, 263 insertions(+), 39 deletions(-)
```

---

## 0. СРАЗУ — ОДНА ФАКТИЧЕСКАЯ ПОПРАВКА К ЗАДАНИЮ

Ты написал: *«три места, которые ДВИГАЮТ стоп: безубыток, граница recheck и трейл. В бою каждое
становится cancel-then-create»*.

**Трейл не является перемещением стопа — ни при одном из владельцев, и это не придирка.**

| | безубыток | recheck TIGHTEN | **трейл** |
|---|---|---|---|
| что делает в БУМАГЕ | переписывает `sl_price` | переписывает `sl_price` | **не трогает `sl_price` вообще** — это условие ЗАКРЫТИЯ: `last <= water_mark*(1-pct)` → `_do_close(..., 'trail')` |
| что делает в БОЮ | cancel + create `STOP_MARKET` | cancel + create `STOP_MARKET` | **создаёт ДРУГОЙ ТИП ОРДЕРА** — `TRAILING_STOP_MARKET` с `priceRate`, **рядом** с безубыточным стопом, ничего не отменяя (`breakeven_worker._attempt_trail:436-441`) |

Поэтому движителей **два**, а не три, и `move_stop()` имеет ровно двух вызывающих. Свернуть трейл
в тот же вызов означало бы спрятать решение, которое ты явно просил вынести наружу. §4 — про него.

---

## 1. ЧТО ПОСТРОЕНО

**Один шов, ноль переизобретений.** Ни одна строка размещения, отмены, гонки или аварийного
закрытия не написана заново — всё маршрутизируется в уже обкатанные функции.

**`breakeven_worker.move_stop_with_race_guard()`** — гонка из `_handle_watching:507-519`
**поднята дословно** в отдельную функцию: тот же порядок, та же перепроверка при упавшей отмене,
тот же счётчик попыток, тот же порог крика, то же аварийное закрытие. `_handle_watching` теперь
её вызывает и в остальном не изменён. Контракт:

```
('closed',    None)         позиция уже исчезла — старый стоп залился
('retry',     attempts)     отмена упала, позиция ОТКРЫТА, СТАРЫЙ СТОП ОСТАВЛЕН
('moved',     new_stop_id)  замена стоит
('emergency', last_err)     старый снят + новый не встал -> АВАРИЙНОЕ ЗАКРЫТИЕ УЖЕ ПРОИЗОШЛО
```

**`order_adapter.place_stop()` / `move_stop()` / `stop_lives_on_exchange()`** — шов владения.
В бумаге `place_stop` возвращает `{'stop_order_id': None, 'stop_price': <то же число>}`, а
`move_stop` — `('moved', None)`; на биржу не уходит ничего. В бою — реальный `STOP_MARKET`
`closePosition='true'` через `_place_stop_with_retry`.

**`virtual_positions.stop_order_id TEXT`** — новая аддитивная колонка, NULL в бумаге и на всех
старых строках. NULL означает «стопом владеет поллер», бэкфилл не нужен.

### 🔴 ГДЕ ЖИВЁТ ИНВАРИАНТ АВАРИЙНОГО ЗАКРЫТИЯ (твой пункт 3)

Ровно **два** места в новом пути, и оба делегируют, а не повторяют логику:

| стоп | где | что вызывает |
|---|---|---|
| **СТАВИТСЯ** (вход) | `order_adapter.place_stop()` | `_place_stop_with_retry` → при None → `breakeven_worker._emergency_close()` → `main._execute_close_position` + крик |
| **ДВИГАЕТСЯ** (безубыток, recheck) | `breakeven_worker.move_stop_with_race_guard()` | то же самое |

`main.py:1378-1405` сохраняет собственную копию для legacy-пути входа — **этот патч его не трогает.**

`place_stop` возвращает `None` **только** когда инвариант сработал. Вызывающий обязан трактовать
`None` как «позиции НЕТ»: в `execute_entry` строка не пишется вовсе.

### Порядок, который я поменял намеренно (и это не косметика)

В безубытке `move_stop` вызывается **ДО** пересчёта адаптивного трейла. Пересчёт документирован как
«строго один раз на арминг», и одноразовость держится внешним `if not be_applied`, который снимается
только записью `breakeven_applied` в конце блока. Живой `'retry'` возвращается **без записи** — и
пересчёт, стоящий раньше, срабатывал бы заново на каждом повторном тике, тихо ломая одноразовость.
В бумаге разницы нет (`move_stop` мгновенно возвращает `('moved', None)`), но в бою порядок — это
то, что делает утверждение об одноразовости правдой.

### Граница `93c20c3` — не тронута

`_tighten_sl(position_side, entry_price, current_sl, original_sl=...)` — **ценовое правило**, а не
вопрос размещения: тянуть можно только К входу и никогда за исходный стоп. Оно остаётся ровно там,
где было, и одинаково при обоих владельцах. Пункт 11 меняет только то, **кому** отдаётся полученное
число.

---

## 2. ДОКАЗАНО ИСПОЛНЕНИЕМ (мок-биржа, живой сервис не тронут)

```
1) place_stop LIVE, успех
   -> {'stop_order_id':'STOP-999', 'simulated':False}
   тип ордера: STOP_MARKET   params: {'stopPrice':63787.5,'positionSide':'LONG','closePosition':'true'}

2) place_stop LIVE, все 3 попытки упали  -> ИНВАРИАНТ
   [BE-SL-RETRY] attempt 1/3, 2/3, 3/3 failed
   [ADAPTER] 🚨 STOP PLACEMENT FAILED — firing the emergency close invariant
   returned: None | emergency_close ВЫЗВАН: True

3) move_stop: отмена УПАЛА, позиция ОТКРЫТА  -> ('retry', 1)
   новый стоп создан? НЕТ   аварийное закрытие? НЕТ    ← СТАРЫЙ СТОП ОСТАЛСЯ

4) move_stop: отмена УПАЛА, позиция ИСЧЕЗЛА  -> ('closed', None)   аварийное закрытие? НЕТ

5) move_stop: отмена ОК, пересоздание УПАЛО  -> ('emergency', ...)  emergency_close ВЫЗВАН: True

6) move_stop: happy path -> ('moved','STOP-999')  cancelled:['OLD-1']  created: STOP_MARKET
```

Бумажный путь — отдельно: `place_stop`/`move_stop` вызваны с `exchange=None` и **ни разу к нему не
обратились**, вернув `{'stop_order_id':None,...}` и `('moved', None)`. Это и есть доказательство,
что в бумаге не уходит ничего.

Синтаксис всех трёх файлов — `py_compile` OK. `git apply --check` против живого дерева — чисто.

---

## 3. ЧТО ИЗМЕНИТСЯ В БУМАГЕ: НИЧЕГО

`sl_price` вычисляется той же формулой, пишется тем же `UPDATE`, читается тем же поллером и
сравнивается с тем же опрошенным `last`. Единственная разница в БД — новая колонка `stop_order_id`,
всегда NULL в бумаге. **Ни одно число книги не двигается, книга остаётся сравнимой сама с собой.**

---
## 4. 🔴 ТРЕЙЛ — ОТДЕЛЬНОЕ РЕШЕНИЕ. МОЯ РЕКОМЕНДАЦИЯ И ПОЧЕМУ

**В патче трейл НЕ ТРОНУТ.** Ни одной строки. Ниже — то, что ты просил: прямо, какой вариант я
предлагаю, и что каждый делает со сравнимостью.

### Главное, что меняет рамку решения

**Аргумент, которым выигран пункт 11 для стоп-лосса, на трейл НЕ ПЕРЕНОСИТСЯ.**

Трейл взводится **только после безубытка** (`if be_applied and trail_pct > 0`). К этому моменту на
бирже уже висит `STOP_MARKET` на уровне безубытка. Значит: **умер процесс — позиция НЕ голая.**
Худшее, что даёт смерть процесса после безубытка, — позиция доедет до безубытка вместо того, чтобы
выйти по отдаче. Это разница в **ПРИБЫЛИ, а не в РИСКЕ**.

Поэтому «защита должна пережить нас самих» здесь ничего не решает: **оба варианта её обеспечивают.**
Решение сводится к сравнимости против качества выхода.

### Цифры (§4 замера от 15:48), без приукрашивания

- трейл вообще взводился у **17 из 51** позиции — у 34 вопроса не существует;
- из 17 вышли бы раньше на неопрошенном фитиле **7**; материально (≥5 мин) — **3**;
- Δ по всем семи: **−67.30**. **По чистым: +20.25.**
- весь отрицательный итог несёт **один vpos 46 (−93.09)**, исключаемый фильтрами §0;
- все 7 — реальные ВЫИГРЫШИ (механизм «фитиль срезает победителя» подтверждён).

**n = 7, материальных 3, и знак итога переворачивается одной позицией. Это тонкая улика, и я не
буду делать вид, что она весомее, чем есть.**

### 🔴 РЕКОМЕНДУЮ: биржевой `TRAILING_STOP_MARKET`

Причины в порядке веса:

1. **Альтернатива возвращает наш поллер к отправке рыночных ордеров по живой позиции.** Это ровно
   то двойное владение, которое пункт 12 создан устранить, — и оно возвращалось бы для механизма,
   который срабатывает чаще всего и всегда возле прибыли. Ставить это обратно сразу после того, как
   мы вынесли стоп на биржу, — противоречие.
2. **Код есть и обкатан** — `_attempt_trail`, включая корректный режим отказа: не встал трейл →
   `SL held at breakeven — position is safe but un-trailed`. Никакого аварийного закрытия там нет и
   не нужно, потому что позиция уже защищена.
3. **На чистой выборке замер ПОЛОЖИТЕЛЕН (+20.25).** Отрицательный общий итог — артефакт одной
   позиции, которую наши же фильтры исключают.
4. Отказ безвреден: провал размещения трейла оставляет безубыточный стоп.

### Против, честно

**Сравнимость по измерению «трейл» теряется НАВСЕГДА.** Бумага ведёт вершину по опросу раз в 10 с;
биржа — непрерывно. При одном и том же `trail_pct` это разные выходы, и разница не сходится с
ростом выборки — она структурная. Бумажная книга останется сравнимой **сама с собой**, но
**бумажные и боевые выходы по трейлу нельзя будет складывать в одну выборку никогда.** Если решаешь
сравнивать их напрямую — вариант с поллером единственный, и тогда надо сознательно принять, что
трейл не переживает смерти процесса (что, повторю, стоит только прибыли).

### 🔴 И отдельная находка, которую я обязан вынести

`_attempt_trail` **НЕ отменяет безубыточный `STOP_MARKET`** перед созданием
`TRAILING_STOP_MARKET`. То есть в бою после арминга трейла на бирже висят **ДВА ордера с
`closePosition='true'` одновременно** — при том что соседний код (`_handle_watching`) несёт
комментарий *«never hold two closePosition stops»*. Это **не внесено мной**: так работает
существующий боевой путь, и пункт 11 его наследует. Но прежде чем включать бой, надо ответить:
что делает BingX, если оба сработают на одном движении. Я этого **не проверял** и данных не имею.

---

## 5. ЧТО НЕ МОЖЕТ БЫТЬ ОДИНАКОВЫМ (твой пункт 5)

| # | расхождение | почему допустимо |
|---|---|---|
| 1 | **Чувствительность к фитилю** (известное). Биржевой стоп срабатывает на любой сделке, бумажный — на опрошенном `last` раз в 10 с | Замерено на 101 739 свечах: **+36.91 в пользу биржевого**, ребро шорта живёт (+1451 → +1476). Возражение было эмпирическим и не выдержало |
| 2 | **Цена исполнения стопа.** Бумага закрывает по опрошенному `last`, который на разрыве может быть ЗА стопом; бой триггерится на `stopPrice` и льётся по рынку | Ошибка разнонаправленная, не систематическая. Проскальзывание на 0.0031 BTC замерено: **в 625 раз дешевле комиссии** |
| 3 | **Ведение вершины трейла** (если §4 = биржевой) | Структурно, навсегда. См. §4 — это цена решения, а не дефект |
| 4 | **Окно cancel/create.** В бумаге перенос стопа атомарен; в бою упавшая отмена откладывает перенос на тик и более | Защита не страдает — держится СТАРЫЙ стоп. Но **уровень стопа может отличаться от бумажного несколько тиков**, и это неустранимо |
| 5 | **Размер стопа после LONG-частички.** Бумага считает P&L по остатку легов; бой полагается на `closePosition='true'` при неизменном `amount` | Эквивалентно **только если** BingX честно закрывает остаток. **Не проверено** — см. риск 4 |
| 6 | **Комиссия.** Ставка одна (0.0005), но бой читает реальную с биржи (или оценивает, когда та не отдала), бумага считает от `last` | Разница на уровне копеек; механизм оценки уже помечен как §7.4 брифа |
| 7 | **Аварийное закрытие существует ТОЛЬКО в бою.** В бумаге ветка недостижима | Значит в бумажной книге таких выходов нет вовсе — при сравнении это отдельная категория, а не шум |

---

## 6. ЧТО МОЖЕТ ПОЙТИ НЕ ТАК — мой собственный список

1. **🔴 Два `closePosition` ордера одновременно после арминга трейла** (§4). Унаследовано, не
   внесено, но включать бой с этим нельзя без ответа от биржи.
2. **🔴 Осиротевший стоп при гонке на входе.** `place_stop` вызывается **ДО** вставки строки —
   сознательный выбор: «нет голой позиции» важнее, чем «нет осиротевшего ордера». Но если вставка
   затем упадёт на уникальном индексе (одновременный вход), на бирже останется реальный
   `STOP_MARKET` без строки в БД. С `closePosition='true'` и без позиции он инертен, и
   `reconcile_boot_state` такие подметает, — **но это НОВЫЙ режим отказа, которого раньше не было.**
   Обратный порядок породил бы худшее: строку без защиты.
3. **Извлечение гонки трогает боевой код.** `_handle_watching` переписан на вызов. Поведение
   сохранено по разбору и по 6 мок-тестам, но **против реальной биржи не проверялось ничем** —
   как и весь боевой путь в этом патче.
4. **Размер стопа устаревает после LONG-частички.** `step_size` не уменьшается, стоп ставится на
   исходный размер. Безвредно только благодаря `closePosition='true'`. Проверить до боя.
5. **Тир recheck теперь «успевает один раз», а не «срабатывает один раз».** На `'retry'` я НЕ
   помечаю `recheck_status='tightened'`, чтобы тир остался должным и тянул повторно. Значит
   бесконечно падающая отмена будет повторять тир — ограничено окном 300 с, но это изменение
   семантики, и я говорю о нём прямо.
6. **`_emergency_close` лениво импортирует `main`** внутри пути входа. Так уже делает
   `breakeven_worker`, но в момент входа это новый контекст для того же импорта.
7. **Пункт 12 не сделан.** Пока маршрутизация не мигрирована, боевой трафик вообще не доходит до
   адаптера, и бот откажется стартовать при обоих флагах True. То есть **этот патч сегодня не может
   выстрелить ни при каком стечении обстоятельств** — он весь под бумажной веткой.

---

## 7. ПОЛНЫЙ ДИФФ (НЕ ПРИМЕНЁН)

`git apply --check` против живого дерева на `96b83d4` — **чисто**. Рабочее дерево `/root/titan-bot`
не изменено: `git status --porcelain` пуст.

```diff
diff --git a/titan-bot/breakeven_worker.py b/titan-bot/breakeven_worker.py
index e064dbb..71e77d8 100644
--- a/titan-bot/breakeven_worker.py
+++ b/titan-bot/breakeven_worker.py
@@ -226,6 +226,60 @@ def _place_stop_with_retry(exchange, symbol, position_side, amount, stop_price):
     return None, last_err
 
 
+def move_stop_with_race_guard(exchange, send_tg, symbol, position_side, amount,
+                              old_stop_id, new_stop_price, cancel_attempts=0,
+                              label='Breakeven'):
+    """Cancel the old closePosition stop, then create its replacement.
+
+    This is the race handling that has lived inline in `_handle_watching` since
+    the breakeven worker was written. Item 11 needs the SAME behaviour for a
+    second mover (the post-entry recheck TIGHTEN bound), so it is LIFTED here
+    unchanged rather than copied. `_handle_watching` now calls it and is
+    otherwise untouched; the ordering, the re-check on cancel failure, the
+    attempt counter, the alert threshold and the emergency close are all the
+    original code.
+
+    The rule it encodes, which is the whole point: a cancel that fails while the
+    position is STILL OPEN means we KEEP THE OLD STOP and retry next tick. We
+    never end a tick with a naked position.
+
+    Returns (outcome, payload):
+      ('closed',    None)       position already gone — the old stop filled
+      ('retry',     attempts)   cancel failed, position open, OLD STOP KEPT
+      ('moved',     new_stop_id) replacement is live
+      ('emergency', last_err)   old cancelled + new failed -> EMERGENCY CLOSE FIRED
+    """
+    # Cancel the ORIGINAL SL first — never hold two closePosition stops.
+    try:
+        exchange.cancel_order(old_stop_id, symbol)
+    except Exception as ce:
+        # The SL may have already filled (position closing) — re-check.
+        if _fetch_open_position(exchange, symbol, position_side) is None:
+            return 'closed', None
+        # Still open but cancel failed: keep the OLD SL (never naked), retry the
+        # whole move next tick. Alert after MAX_CANCEL_ATTEMPTS.
+        attempts = int(cancel_attempts or 0) + 1
+        print(f"[BE] cancel old SL failed {symbol} {position_side} "
+              f"({label}, attempt {attempts}/{MAX_CANCEL_ATTEMPTS}): {ce}", flush=True)
+        if attempts >= MAX_CANCEL_ATTEMPTS and send_tg:
+            try:
+                send_tg(f"⚠️ <b>{label} stalled</b> {symbol} {position_side}: "
+                        f"could not cancel original SL after {attempts} tries.\n"
+                        f"Original SL still active — position protected; will keep retrying.")
+            except Exception:
+                pass
+        return 'retry', attempts
+
+    # Old SL cancelled → recreate at the new level (3 retries).
+    new_sl_id, last_err = _place_stop_with_retry(
+        exchange, symbol, position_side, amount, new_stop_price)
+    if new_sl_id is None:
+        # Unprotected (old SL cancelled, new failed) → emergency close.
+        _emergency_close(symbol, position_side, send_tg, last_err)
+        return 'emergency', last_err
+    return 'moved', new_sl_id
+
+
 def _emergency_close(symbol, position_side, send_tg, last_err):
     """SL recreate failed after cancelling the old SL → position is unprotected.
     Reuse the battle-tested close path via a lazy import (avoids a circular
@@ -504,41 +558,28 @@ def _handle_watching(exchange, send_tg, job, last):
 
     be_price = _breakeven_price(exchange, symbol, position_side, entry_price)
 
-    # Cancel the ORIGINAL SL first — never hold two closePosition stops.
-    try:
-        exchange.cancel_order(job['sl_order_id'], symbol)
-    except Exception as ce:
-        # The SL may have already filled (position closing) — re-check.
-        if _fetch_open_position(exchange, symbol, position_side) is None:
-            _set_status(job_id, status='closed', completed_at=_utc_now_iso())
-            _report_passive_fill(exchange, send_tg, job, 'watching')
-            print(f"[BE] {symbol} {position_side} SL already gone (filled/closed); done.",
-                  flush=True)
-            return
-        # Still open but cancel failed: keep the OLD SL (never naked), retry the
-        # whole move next tick. Alert after MAX_CANCEL_ATTEMPTS.
-        attempts = int(job['cancel_attempts'] or 0) + 1
-        _set_status(job_id, cancel_attempts=attempts)
-        print(f"[BE] cancel old SL failed {symbol} {position_side} "
-              f"(attempt {attempts}/{MAX_CANCEL_ATTEMPTS}): {ce}", flush=True)
-        if attempts >= MAX_CANCEL_ATTEMPTS and send_tg:
-            try:
-                send_tg(f"⚠️ <b>Breakeven stalled</b> {symbol} {position_side}: "
-                        f"could not cancel original SL after {attempts} tries.\n"
-                        f"Original SL still active — position protected; will keep retrying.")
-            except Exception:
-                pass
-        return
+    # Cancel-then-create with the race handling, now shared with the post-entry
+    # recheck mover via order_adapter.move_stop (item 11). Behaviour is the
+    # original code, lifted into move_stop_with_race_guard above.
+    outcome, payload = move_stop_with_race_guard(
+        exchange, send_tg, symbol, position_side, float(job['amount']),
+        job['sl_order_id'], be_price,
+        cancel_attempts=job['cancel_attempts'], label='Breakeven')
 
-    # Old SL cancelled → recreate at breakeven (3 retries).
-    new_sl_id, last_err = _place_stop_with_retry(
-        exchange, symbol, position_side, float(job['amount']), be_price)
-    if new_sl_id is None:
-        # Unprotected (old SL cancelled, new failed) → emergency close.
-        _emergency_close(symbol, position_side, send_tg, last_err)
+    if outcome == 'closed':
+        _set_status(job_id, status='closed', completed_at=_utc_now_iso())
+        _report_passive_fill(exchange, send_tg, job, 'watching')
+        print(f"[BE] {symbol} {position_side} SL already gone (filled/closed); done.",
+              flush=True)
+        return
+    if outcome == 'retry':
+        _set_status(job_id, cancel_attempts=payload)
+        return
+    if outcome == 'emergency':
         _set_status(job_id, status='closed', breakeven_price=be_price,
                     completed_at=_utc_now_iso())
         return
+    new_sl_id = payload
 
     _set_status(job_id, status='breakeven_set', breakeven_price=be_price,
                 new_sl_order_id=new_sl_id, applied_at=_utc_now_iso())
diff --git a/titan-bot/order_adapter.py b/titan-bot/order_adapter.py
index cf76cec..386d11f 100644
--- a/titan-bot/order_adapter.py
+++ b/titan-bot/order_adapter.py
@@ -396,3 +396,92 @@ def market_reduce(exchange, symbol, position_side, amount, ref_price):
     print(f"[ADAPTER] LIVE PARTIAL {symbol} {position_side} {res['amount']} "
           f"@ {res['fill_price']} fee={res['fee_cost']:.6f}", flush=True)
     return res
+
+
+# ===========================================================================
+# STOP OWNERSHIP — design item 11. Option A: the stop lives on the EXCHANGE.
+# ===========================================================================
+# Paper is UNCHANGED and must stay so: the stop is a number in
+# virtual_positions.sl_price, evaluated by the poller against the polled `last`.
+# Not one paper number moves, so the book stays comparable with itself.
+#
+# Live, the stop becomes a real STOP_MARKET closePosition='true' placed through
+# breakeven_worker._place_stop_with_retry — the helper that has always placed
+# it. Nothing here reimplements placement, cancellation, the cancel/create race
+# or the emergency close; this module only decides WHO owns the stop and routes
+# to the existing, battle-tested code.
+
+def stop_lives_on_exchange():
+    """WHO owns the protective stop, as a predicate rather than a guess.
+
+    Deliberately NOT an alias of orders_are_real() at the call sites even though
+    it returns the same value today: the question "are fills real?" and the
+    question "who holds the stop?" are different, and item 12 will need to move
+    one without the other. One name per question."""
+    return orders_are_real()
+
+
+def place_stop(exchange, symbol, position_side, amount, stop_price, send_tg=None):
+    """Protective stop for a freshly opened position.
+
+    🔴 THE INVARIANT (main.py:1378-1405, and the one requirement of item 11 that
+    may not be traded away): if the stop cannot be placed after
+    SL_RETRY_ATTEMPTS, the position is closed at market IMMEDIATELY and the
+    operator is alerted. A position must never live unprotected, not for one
+    tick.
+
+    In this build that invariant exists in exactly TWO places and both delegate
+    to the same helpers rather than restating the logic:
+      * HERE, for a stop being PLACED   -> _bw._emergency_close(...)
+      * breakeven_worker.move_stop_with_race_guard, for a stop being MOVED
+    main.py:1378-1405 keeps its own copy for the legacy live entry path, which
+    this build does not touch.
+
+    Returns a stop descriptor, or None when the invariant FIRED. None means the
+    position no longer exists: the caller MUST NOT write or keep a position row.
+    """
+    if not stop_lives_on_exchange():
+        # PAPER — byte-identical to the behaviour that has always existed. The
+        # returned stop_price is the number the caller writes to sl_price; the
+        # poller evaluates it. Nothing is sent to the exchange.
+        return {'stop_order_id': None, 'stop_price': float(stop_price),
+                'simulated': True}
+
+    _require_live('place a protective stop')
+    import breakeven_worker as _bw          # lazy: _bw imports this module
+    stop_id, last_err = _bw._place_stop_with_retry(
+        exchange, symbol, position_side, amount, stop_price)
+    if stop_id is None:
+        print(f"[ADAPTER] 🚨 STOP PLACEMENT FAILED {symbol} {position_side} after "
+              f"retries — firing the emergency close invariant", flush=True)
+        _bw._emergency_close(symbol, position_side, send_tg, last_err)
+        return None
+    print(f"[ADAPTER] LIVE STOP {symbol} {position_side} @ {stop_price} "
+          f"id={stop_id}", flush=True)
+    return {'stop_order_id': stop_id, 'stop_price': float(stop_price),
+            'simulated': False}
+
+
+def move_stop(exchange, symbol, position_side, amount, old_stop_id,
+              new_stop_price, send_tg=None, cancel_attempts=0, label='stop move'):
+    """Move an existing stop to a new level, under either owner.
+
+    TWO callers, both of which must behave the same under both owners:
+      * breakeven at +1R
+      * the post-entry recheck TIGHTEN bound (93c20c3)
+    The TRAIL is deliberately NOT a caller — under neither owner is it a stop
+    move. See the report for item 11 §4: in paper the trail is a close TRIGGER,
+    in live it is a different ORDER TYPE placed alongside the breakeven stop.
+    Folding it in here would have hidden a real decision.
+
+    Returns (outcome, payload) exactly as
+    breakeven_worker.move_stop_with_race_guard. Paper returns ('moved', None):
+    the caller writes the new number, which is what it does today.
+    """
+    if not stop_lives_on_exchange():
+        return 'moved', None
+    _require_live('move a protective stop')
+    import breakeven_worker as _bw
+    return _bw.move_stop_with_race_guard(
+        exchange, send_tg, symbol, position_side, amount,
+        old_stop_id, new_stop_price, cancel_attempts=cancel_attempts, label=label)
diff --git a/titan-bot/virtual_trader.py b/titan-bot/virtual_trader.py
index f7f25a4..35eb2f1 100755
--- a/titan-bot/virtual_trader.py
+++ b/titan-bot/virtual_trader.py
@@ -186,7 +186,15 @@ def init_db():
                         # legacy rows -> treated as "no partial taken", so every
                         # existing position keeps the old contract exactly.
                         "partial_taken INTEGER",
-                        "realized_partial_usdt REAL"):
+                        "realized_partial_usdt REAL",
+                        # Stop ownership (item 11, 2026-07-29). The exchange id of
+                        # the STOP_MARKET protecting this position. NULL in paper
+                        # AND on every legacy row — paper's stop is the sl_price
+                        # number evaluated by the poller, exactly as before, so a
+                        # NULL here means "the poller owns it" and needs no
+                        # backfill. Only ever non-NULL when the position was
+                        # opened while stop_lives_on_exchange() was True.
+                        "stop_order_id TEXT"):
             try:
                 conn.execute(f"ALTER TABLE virtual_positions ADD COLUMN {_coldef}")
             except sqlite3.OperationalError:
@@ -634,6 +642,21 @@ def execute_entry(exchange, symbol, side, position_side,
     # (e.g. a future multi-process deploy), the INSERT raises IntegrityError and
     # we skip rather than stack.
     with _entry_lock:
+        # STOP OWNERSHIP (item 11). Placed BEFORE the row is written, because the
+        # invariant's failure mode is "there is no position" — and a row written
+        # first would then have to be un-written. In paper this returns instantly
+        # with stop_order_id=None and sl_price unchanged: the poller still owns
+        # the stop and no paper number moves. In live it is a real STOP_MARKET,
+        # and None means the emergency close already fired.
+        _stop = order_adapter.place_stop(
+            exchange, symbol, position_side, amount, sl_price, send_tg=send_tg)
+        if _stop is None:
+            print(f"VIRTUAL ENTRY ABORTED {symbol} {position_side}: protective "
+                  f"stop could not be placed; emergency close fired, no row "
+                  f"written", flush=True)
+            return None
+        _stop_order_id = _stop['stop_order_id']
+
         with sqlite3.connect(DB_PATH) as conn:
             n_open = conn.execute(
                 "SELECT COUNT(*) FROM virtual_positions "
@@ -655,8 +678,8 @@ def execute_entry(exchange, symbol, side, position_side,
                     "entry_wall_baseline_mult, entry_adx_1h, entry_atr_pct_1h, "
                     "entry_sup_wall_mult, entry_sup_wall_dist_pct, "
                     "entry_opp_wall_dist_pct, entry_ob_imbalance, "
-                    "entry_n_walls_bid, entry_n_walls_ask) "
-                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
+                    "entry_n_walls_bid, entry_n_walls_ask, stop_order_id) "
+                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (
                         symbol, position_side, side, margin_required, amount, LEVERAGE,
                         fill_price, atr, sl_price, trail_pct,
@@ -670,6 +693,9 @@ def execute_entry(exchange, symbol, side, position_side,
                         _entry_sup_mult, _entry_sup_dist,
                         _entry_opp_dist, _entry_ob_imb,
                         _entry_n_bid, _entry_n_ask,
+                        # NULL in paper (poller owns the stop); the exchange
+                        # STOP_MARKET id in live.
+                        _stop_order_id,
                     ),
                 )
                 vpos_id = cur.lastrowid
@@ -1230,14 +1256,42 @@ def _run_recheck_tier(exchange, row, last, tier, send_tg):
         current_sl = float(row['sl_price'])
         _orig_sl = (row['original_sl_price'] if 'original_sl_price' in _rk
                     and row['original_sl_price'] is not None else current_sl)
+        # The 93c20c3 bound is COMPUTED here and is deliberately untouched by
+        # item 11: _tighten_sl may only tighten TOWARD the entry, never past the
+        # original stop. That is a price rule, not a placement concern, so it
+        # stays exactly where it is and applies identically under both owners.
+        # Item 11 changes only WHO the resulting number is handed to.
         new_sl = float(exchange.price_to_precision(
             symbol, _tighten_sl(position_side, entry_price, current_sl,
                                 original_sl=_orig_sl)))
+
+        # STOP OWNERSHIP (item 11) — MOVER 2 of 2: the recheck TIGHTEN.
+        # Same race guard as breakeven; in paper it is a no-op returning
+        # ('moved', None) and the UPDATE below is byte-identical to today.
+        _mv, _mv_payload = order_adapter.move_stop(
+            exchange, symbol, position_side, float(row['step_size']),
+            (row['stop_order_id'] if 'stop_order_id' in _rk else None),
+            new_sl, send_tg=send_tg, label='Recheck tighten')
+        if _mv in ('closed', 'emergency'):
+            # Position gone (old stop filled) or emergency close already fired
+            # inside the race guard. Do NOT mark 'tightened' — the tier did not
+            # complete, and the row is about to be reconciled either way.
+            print(f"[VIRTUAL] recheck tighten vpos={vpos_id}: {_mv} — "
+                  f"stop not moved, status left unchanged", flush=True)
+            return 'closed' if _mv == 'closed' else None
+        if _mv == 'retry':
+            # Cancel failed, OLD STOP HELD. Leave recheck_status untouched so the
+            # SAME tier is still due next tick and the tighten is retried. This is
+            # the one place where "tier fires once" must mean "succeeds once".
+            print(f"[VIRTUAL] recheck tighten vpos={vpos_id}: cancel failed, "
+                  f"OLD STOP HELD, tier stays due", flush=True)
+            return None
+
         with sqlite3.connect(DB_PATH) as conn:
             conn.execute(
-                "UPDATE virtual_positions SET sl_price=?, recheck_status='tightened' "
-                "WHERE id=? AND status='open'",
-                (new_sl, vpos_id),
+                "UPDATE virtual_positions SET sl_price=?, recheck_status='tightened', "
+                "stop_order_id=? WHERE id=? AND status='open'",
+                (new_sl, _mv_payload, vpos_id),
             )
         # Layer 2: the stop has ALREADY moved above. A logging fault here cannot
         # undo or block it — it only costs us the evidence row.
@@ -1736,6 +1790,42 @@ def _process_position(exchange, row, last, send_tg):
             offset = 2 * TAKER_FEE_RATE + BREAKEVEN_BUFFER_PCT
             be_price = (fill * (1.0 + offset) if position_side == 'LONG'
                         else fill * (1.0 - offset))
+
+            # STOP OWNERSHIP (item 11) — MOVER 1 of 2: breakeven at +1R.
+            # Ordering matters and is deliberate: the stop is moved BEFORE the
+            # adaptive-trail recompute below. That recompute is documented to run
+            # STRICTLY ONCE per arming, and it is kept once by the enclosing
+            # `if not be_applied` — which only becomes False when the UPDATE at
+            # the end of this block persists breakeven_applied. A live 'retry'
+            # returns without persisting, so a recompute placed BEFORE the move
+            # would run again on every retried tick and quietly break the
+            # once-only property. Paper is unaffected either way (move_stop
+            # returns ('moved', None) immediately), but the ordering is what
+            # makes that true in live too.
+            _mv, _mv_payload = order_adapter.move_stop(
+                exchange, row['symbol'], position_side,
+                float(row['step_size']),
+                (row['stop_order_id'] if 'stop_order_id' in row.keys() else None),
+                be_price, send_tg=send_tg, label='Breakeven')
+            if _mv == 'closed':
+                # The old stop filled while we were moving it. The position is
+                # gone on the exchange; let the next poll reconcile the row.
+                print(f"[VIRTUAL] breakeven vpos={row['id']}: stop already filled "
+                      f"— position closed on exchange", flush=True)
+                return True
+            if _mv == 'retry':
+                # Cancel failed, position STILL OPEN, OLD STOP KEPT. Persist
+                # nothing: next tick re-enters this branch and tries again.
+                print(f"[VIRTUAL] breakeven vpos={row['id']}: cancel failed, "
+                      f"OLD STOP HELD, retrying next tick", flush=True)
+                return True
+            if _mv == 'emergency':
+                # Old stop cancelled, replacement failed -> emergency close has
+                # already fired inside the race guard. Nothing to persist.
+                print(f"[VIRTUAL] breakeven vpos={row['id']}: EMERGENCY CLOSE "
+                      f"fired (stop recreate failed)", flush=True)
+                return True
+
             mgmt_state['breakeven_applied'] = True
             # Adaptive Level-1 trail: recompute trail_pct from a FRESH
             # TRAIL_ATR_TF ATR at this one-shot +1R arming (structurally once via
@@ -1772,8 +1862,12 @@ def _process_position(exchange, row, last, send_tg):
             with sqlite3.connect(DB_PATH) as conn:
                 conn.execute(
                     "UPDATE virtual_positions SET sl_price=?, trail_pct=?, "
-                    "pending_dca_limits=? WHERE id=? AND status='open'",
-                    (be_price, new_trail, json.dumps(mgmt_state), row['id']),
+                    "pending_dca_limits=?, stop_order_id=? "
+                    "WHERE id=? AND status='open'",
+                    # stop_order_id: None in paper (stays NULL, the poller owns
+                    # the stop); the id of the freshly created STOP_MARKET in live.
+                    (be_price, new_trail, json.dumps(mgmt_state),
+                     _mv_payload, row['id']),
                 )
             sl_price = be_price
             be_applied = True
```
