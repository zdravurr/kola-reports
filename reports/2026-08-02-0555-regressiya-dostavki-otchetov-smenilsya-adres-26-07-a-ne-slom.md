# Регрессия доставки отчётов — сменился адрес 26.07, а не сломалась отправка

_2026-08-02 05:55 UTC_

---

Регрессия доставки: «отчёт публикуется, ссылка в Телеграм не приходит». Что именно сломалось.

## КОРОТКО

Отправка НЕ сломана. Сломались ДВЕ ДРУГИЕ вещи, обе — регрессии:

**A. 26-27.07 сменился АДРЕС.** Коммит `30e1231` (26.07 12:13) переселил ~40 вызовов
`notify_boss` из канала Коли (@Orchetkoyyyyy_bot) в канал Дирижёра (@Derizherrr3_bot).
Босс читает первый. Отчёты стали приходить во второй.

**B. Пришивается RAW-ссылка, а не кликабельная.** `notify.ensure_report_link` добавляет
`https://raw.githubusercontent.com/...`, а не `https://github.com/.../blob/main/...`.

---

## 1. ГИПОТЕЗА «переделка report_publish.py 27.07» — ОПРОВЕРГНУТА

Коммитов `lib/report_publish.py` **27.07 не существует**. Вся история файла:

```
ad029bb 2026-07-29 11:28  добор торгового словаря — скраб резал ИМЕНА СИГНАЛОВ
cf1c666 2026-07-29 10:56  скраб фамилий СЪЕДАЛ куски отчёта через перевод строки
1452627 2026-07-29 10:13  скраб фамилий КАЛЕЧИЛ названия торговых сигналов
53637cb 2026-07-21 17:10  publish-lock и 255 файлов
ea46f82 2026-07-17 01:02  the publish lock repeated the very trap it was added next to
8a7263b 2026-07-17 00:19  the link hung on notify_boss's politeness, not on delivery
2e9450b 2026-07-14 22:23  three-stage disclosure, phone-outage guard
e240bd6 2026-07-14 21:27  send with the listing we already proved
ed3c431 2026-07-14 20:39  PII scanner was blocking its OWN reports
e9d93e8 2026-07-14 13:25  feat: publish long reports to zdravurr/kola-reports
```

Три коммита 29.07 меняли ТОЛЬКО словари `RULES` и `NON_NAME_WORDS` (скраб PII):

```
@@ -67,7 +67,13 @@ RULES = [
@@ -96,6 +102,23 @@ NON_NAME_WORDS = {
```

**Из отправки ничего не удаляли, потому что отправки там НИКОГДА НЕ БЫЛО.**
Проверка всех ревизий файла на слова telegram/sendMessage/notify_boss/channel_policy:
каждая ревизия с 14.07 даёт РОВНО 1 совпадение, и это строка 102 —
слово `"telegram"` в белом списке PII-скраба, не вызов.

`report_publish.publish()` по замыслу только публикует и возвращает URL. Отправляет
ДРУГОЙ слой. Это разделение зафиксировано ещё 14.07 (`1c94302`).

## 2. ЧТО РЕАЛЬНО ИЗМЕНИЛОСЬ — коммит 30e1231, 26.07 12:13

```
fix(channels): ~40 вызовов notify_boss ехали в канал Коли — переселены ОДНИМ горлом,
               не 15 диффами в money-path

Приказ Босса: канал Коли несёт ТОЛЬКО сисадмин/технику; операционка воркеров
(Боря/Сеня/Огонь — покупатели, листинги, рост) — ТОЛЬКО канал Дирижёра, без исключений.
```

Добавлено (`lib/notify.py`):

```python
+def _caller_channel():          # канал по МОДУЛЮ-ВЫЗЫВАТЕЛЮ через inspect.stack
+    if channel is None:
+        channel, _why = _caller_channel()
+    if channel == "dirigent":
+        ok = cp.report(text, channel="dirigent")     # → @Derizherrr3_bot
```

Второй экземпляр того же класса — `0313f43` (27.07 16:00): транзитные кадры
(`fault_realert._alert`) уводили работу Огня не в тот канал.

**Улика, что это два РАЗНЫХ чата, а не один:** `message_id` в Telegram последователен
внутри чата.

```
@Orchetkoyyyyy_bot  (канал Коли, health_ping каждые 10 мин)   message_id = 4623
@Derizherrr3_bot    (канал Дирижёра)                          message_id = 450
```

4623 против 450 — это два независимых счётчика, то есть две разные переписки на телефоне.
За 24 ч в канал Коли ушло 43 `notify_boss` + 15 `health_ping`.

## 3. ОТПРАВКА ИСПОЛНЯЕТСЯ — трассировка живого прогона

Прогнан РЕАЛЬНЫЙ путь `notify.notify_boss(...)` с логом до и после каждого слоя.
Продакшн-файлы не менялись: обёртки поставлены в рантайме.

```
05:53:46 [0] calling notify.notify_boss(chars=758, channel='dirigent')
05:53:46 [1] ensure_report_link() ENTER  chars_in=758 task=delivery_regression_proof
05:53:46     _looks_substantial=True (_SUBSTANTIAL_MIN=400, newlines=13)
05:53:47 [1] ensure_report_link() EXIT   chars_out=888  appended=
             '📄 Полный отчёт: https://raw.githubusercontent.com/zdravurr/kola-reports/main/
              reports/2026-08-02-0553-delivery-regression-proof.md'
05:53:47 [2] channel_policy.report() ENTER channel=dirigent chars=888
05:53:47   [HTTP] --> POST api.telegram.org/sendMessage
05:53:48   [HTTP] <-- HTTP 200  ok=True message_id=452
05:53:48 [2] channel_policy.report() EXIT  returned='dirigent'
05:53:48 [0] notify_boss RETURNED 'dirigent'
```

Дословный ответ Telegram:

```json
{"ok": true,
 "result": {"message_id": 452,
   "from": {"id": 8825840080, "is_bot": true, "username": "Derizherrr3_bot"},
   "chat": {"id": 6284337254, "username": "dedushka_panas", "type": "private"},
   "date": 1785650028,
   "entities": [{"offset": 647, "length": 28, "type": "url"},
                {"offset": 776, "length": 113, "type": "url"}]}}
```

**Ни одна ветка шаг не пропустила. Ни одно исключение не съедено.** На пути
`send() -> send_to() -> _call() -> urlopen` нет ни одного `try/except` — падение бы
всплыло, а не растворилось.

## 4. ДЕФЕКТ B: ссылка приходит НЕ КЛИКАБЕЛЬНОЙ ФОРМЫ

`lib/notify.py:177`

```python
_LINK_RE = re.compile(r"https://raw\.githubusercontent\.com/\S+\.md")
```

Из этого следует два последствия:

1. Автопришивка всегда даёт **raw**-ссылку (`ensure_report_link`, ветка `r["url"]`),
   а `report_publish.publish()` возвращает именно `RAW_BASE` (`lib/report_publish.py:47`).
   Кликабельного `github.com/.../blob/main/...` автопуть НЕ ОТДАЁТ НИКОГДА.
2. Если вызыватель САМ вставил blob-ссылку, `_LINK_RE` её НЕ УЗНАЁТ →
   `_looks_substantial` вернёт True → отчёт опубликуется ВТОРОЙ РАЗ и получит ещё и
   raw-ссылку. Дубль публикации на ровном месте.

Отдельно: raw отдаёт КЭШ — это уже кусало нас раньше и записано в стоячих правилах.

## 5. ЧТО ПРЕДЛАГАЮ (не применял)

| # | фикс | file:line | эффект |
|---|---|---|---|
| P1 | Дублировать содержательные отчёты в ОБА канала: Дирижёра (как велено в ТЗ) и Коли (где Босс смотрит) | `lib/notify.py` ветка `channel=='dirigent'` | ссылка снова приходит туда, куда Босс смотрит |
| P2 | Отдавать blob-URL вместо raw: добавить `blob_url` в возврат `publish()` и пришивать его | `lib/report_publish.py:269`, `lib/notify.py` ensure_report_link | кликабельная ссылка, без кэша |
| P3 | Расширить `_LINK_RE` на `github\.com/.+/blob/` | `lib/notify.py:177` | убирает двойную публикацию |

P1 — это ровно то правило, которое я уже записал себе после прошлого разбора:
канал из ТЗ ДОБАВЛЯЕТСЯ к основному, а не подменяет его.
