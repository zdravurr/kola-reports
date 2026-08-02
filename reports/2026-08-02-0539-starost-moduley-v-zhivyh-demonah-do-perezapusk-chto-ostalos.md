# Старость модулей в живых демонах — до, перезапуск, что осталось

_2026-08-02 05:39 UTC_

---

Отчёт о СТАРОСТИ МОДУЛЕЙ в живых демонах: что было, что перезапущено, что осталось.

**Метод.** Python импортирует модуль ОДИН РАЗ за жизнь процесса. Значит демон, стартовавший раньше,
чем модуль был изменён, держит в памяти СТАРЫЙ код — фикс лежит на диске, но не действует.
Проверка: время старта процесса (`/proc/<pid>/stat` поле 22 + `btime`) против `mtime` каждого файла
в РЕКУРСИВНОМ графе импортов (глубина 3). Кроны неуязвимы — каждый запуск новый процесс.

---

## 1. БЫЛО (до перезапуска, 2026-08-02 ~05:20 UTC)

```
     pid user      uptime_h  script
     939 root         466.6  🔴 STALE  mercury-sol/optimizer_listener.py
                               config.py                     +460.1ч ПОСЛЕ старта
 1793223 root         284.1  ✅ fresh  titan-bot/optimizer_listener.py
 3647921 root         116.4  ✅ fresh  titan-bot/gemini_bridge.py
 3733399 botuser      110.0  🔴 STALE  projects/sales/inbox_watcher.py
                               lib/report_publish.py         +23.1ч ПОСЛЕ старта
                               lib/thread_read.py             +1.2ч ПОСЛЕ старта
                               projects/sales/notif_watch.py  +1.3ч ПОСЛЕ старта
  970191 botuser       20.3  ✅ fresh  scripts/kola-bridge/server.py
```

**Штатный `lib/module_staleness.py` видел ОДИН устаревший модуль** (`report_publish.py`).
Независимая проверка по полному графу импортов нашла **ТРИ**. Разница важна: сторож недосчитывает.

## 2. ПЕРЕЗАПУЩЕНО

`kola-inbox-watcher.service` — это unit пользователя **botuser** (`systemctl --user`), поэтому
из-под root он «не найден». Это не отсутствие сервиса, а неверный контекст поиска.

```
=== BEFORE ===  MainPID=3733399  NRestarts=0  ExecMainStartTimestamp=Tue 2026-07-28 12:48:09 UTC
=== RESTART === rc=0
=== AFTER  ===  MainPID=1335059  NRestarts=0  ExecMainStartTimestamp=Sun 2026-08-02 05:28:00 UTC
                ActiveState=active  SubState=running   is-active: active
```

Подтверждение загрузки (два независимых способа):

```
штатный module_staleness.scan()   → stale daemons: 0  ✅ NONE
независимая проверка (33 модуля)  → STALE now:      ✅ NONE
   report_publish.py  mtime=07-29 11:54  <  start 08-02 05:28  ✅
   thread_read.py     mtime=07-28 14:02  <  start 08-02 05:28  ✅
```

Очередь не потеряна:

```
watcher_routed.json  17 записей ДО → 17 ПОСЛЕ (не тронут)
watcher_seen.json    1000 записей сохранены
client_pending.json  жив, перезаписан 05:28:13
детекция ожила через 6 секунд:
  05:28:00 watcher start DETECTION-ONLY (interval=25s, all via Pixel; NO send, routes leads→main)
  05:28:06 [fb_sales] PRIORITY mark client pending: <buyer-R>
  05:28:13 [offerup]  PRIORITY mark client pending: OfferUp
```

## 3. ОСТАЛОСЬ УСТАРЕВШИМ (сейчас, 2026-08-02 ~05:45 UTC)

```
     pid user        up_h  verdict   script
     939 root       469.5  STALE     mercury-sol/optimizer_listener.py
                              +460.1h : mercury-sol/config.py
  970191 botuser     23.2  fresh     scripts/kola-bridge/server.py
 1793223 root       287.0  fresh     titan-bot/optimizer_listener.py
 3647921 root       119.3  fresh     titan-bot/gemini_bridge.py
```

**`mercury-sol/optimizer_listener.py` держит `config.py` 460-часовой давности.**
НЕ ТРОГАЛ — прямой запрет (Solana / Mercuri). Фиксирую как открытый пункт: этот демон работает
на конфиге почти трёхнедельной давности, и любая правка `config.py` за это время НЕ ДЕЙСТВУЕТ.
Решение за Боссом.

**Титан — свежий**, повода трогать не было (и запрет всё равно действует).

---

## 4. ЧТО ЭТО НЕ ЧИНИТ

Перезапуск устраняет РАСХОЖДЕНИЕ КОДА, но НЕ слив токенов. Аварийный стоп жив и после рестарта:

```
2026-08-02T05:28:13+0000 [STOP] inbox_watcher: АВАРИЙНЫЙ СТОП (с 2026-07-28T15:10:23Z) — НЕ бужу main.
2026-08-02T05:28:20+0000 [STOP] inbox_watcher: АВАРИЙНЫЙ СТОП (с 2026-07-28T15:10:23Z) — НЕ бужу main.
```

Корень слива — порядок вызовов в `projects/sales/inbox_watcher.py`:
платный спавн Opus на строке **285**, стоп глушит `wake()` на **321**, метка дедупа `_routed_mark()`
на **322** — НИЖЕ того, что отказывает. Пока стоп взведён, метка не ставится никогда.

**Вывод одной строкой: демон теперь на свежем коде, но петля от этого не закрылась.**
