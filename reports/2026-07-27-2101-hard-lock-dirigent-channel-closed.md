# hard-lock-dirigent-channel-CLOSED

_2026-07-27 21:01 UTC_

---

# ЖЁСТКИЙ ЗАМОК КАНАЛА — ПОСТАВЛЕН И ДОКАЗАН ЖИВЬЁМ

_2026-07-27, продолжение к `2026-07-27-1956-hard-lock-dirigent-account-blocker-27jul.md`_

**Итог одной строкой: третий бот получен, замок собран и работает. Операционный лид теперь
принимает НЕ `main`, а отдельный агент `dirigent` на отдельном боте. Авто-анонс воркера —
тот самый путь, которым 27.07 утёк ответ покупателю Sean, — доказано уехал в канал
Дирижёра. За всё время после включения в канал Коли не ушло НИ ОДНОГО сообщения.**

Титан/Солана не тронуты: ни одного обращения к ним в этой сессии (`titan.service` active,
рабочее дерево чистое, ни один `.py` не изменён).

---

## 1. СОСТОЯНИЕ НА ВХОДЕ (P1 — проверено, не додумано)

Сессия вчера оборвалась на откате. Проверил ФАКТ, а не память:

| что | состояние на 20:09 |
|---|---|
| `channels.telegram.accounts` | **отсутствовал** — откат вчерашней попытки чист, конфиг байт-в-байт довчерашний |
| канал Коли (`@a_openclawzdravurrr_bot`) | `enabled, configured, running, connected` |
| голосовой канал (`@Derizherrr3_bot`, `dirigent_voice.py`) | чист, последний 409 — 19:46:06, после отката ни одного |
| агент `dirigent` | не существовал |
| `secrets.json` | остался нерабочий ключ `dirigentBotToken` (старый бот), конфигом не используется |

Нового токена до обрыва **не приходило** — частичных изменений не было, строить поверх
неизвестного не пришлось.

## 2. ЧТО СДЕЛАНО

Токен нового бота Босс прислал (`@Dlyaderyzhorrr2_bot`, id `8507089688`), дальше — Вариант А:

1. Бэкапы `openclaw.json` + `secrets.json` (`*.bak_newdirigentbot_20260727T200950Z`).
2. Токен в `secrets.json:dirigentOpsBotToken`. **В конфиге токена нет** — только secret-ref
   `{source:file, provider:default, id:/dirigentOpsBotToken}` (проверено: `grep` по конфигу
   даёт 0 совпадений с телом токена).
3. Аккаунт `channels.telegram.accounts.dirigent`. CLI заодно корректно переселил `default`
   внутрь `accounts`, сохранив его secret-ref — канал Коли не пострадал.
4. Агент `dirigent` (воркспейс общий с main — ему нужен тот же операционный код; свой
   `agentDir`), с теми же правами делегирования, что у main.
5. Привязка `dirigent <- telegram accountId=dirigent`.
6. Переадресация на **единственном горле пробуждений** — `agent_capacity.wake()`.

## 3. ПОЧЕМУ ПРИВЯЗКИ БЫЛО МАЛО (и что оказалось настоящим механизмом)

Вчерашний вывод подтвердился и уточнился. Канал сессии задаётся не привязкой, а полем
`route`/`deliveryContext` в session-store. У `agent:main:main` оно было:

    route = {"channel":"telegram","accountId":"default","target":{"to":"telegram:6284337254"}}

Вот эта строка и есть «пришитость к боту Коли» — она проставилась, когда Босс когда-то
написал main в Telegram. У свежей `agent:dirigent:main` было `route = null`, и первый же
пробный ответ **осел в stdout**: агент ответил, Босс не увидел ничего. Поэтому:

* в `wake()` доставка задаётся **ЯВНО** (`--deliver --reply-account dirigent --reply-to …`) —
  не зависит от того, что рантайм запомнил в прошлый раз;
* плюс `route` засеян в store — он нужен там, где флагов нет ФИЗИЧЕСКИ: авто-анонс
  сабагента будит сессию рантаймом, мимо CLI.

## 4. ДОКАЗАТЕЛЬСТВА ЖИВЬЁМ (не стенд, не синтетика)

**4.1. Переадресация лида.** Тот же детектор, что утекал, до и после — в одном логе:

    19:45:58 [channel] inbox_watcher → канал Дирижёра (операционный доклад)
    19:45:58 [WAKE]    inbox_watcher → main                      ← БЫЛО (мягкий замок)
    20:35:52 [channel] inbox_watcher → ЖЁСТКИЙ ЗАМОК: заказчик dirigent, бот dirigent
    20:35:52 [WAKE]    inbox_watcher → dirigent                  ← СТАЛО

**4.2. Доставка дошла до Босса** (движковый лог, не мой пересказ):

    20:36:14 HARDLOCK-LIVE-3 операционный лид принят агентом Дирижёра.
    20:36:14 [telegram] outbound send ok accountId=dirigent chatId=6284337254 messageId=4

**4.3. САМОЕ ГЛАВНОЕ — авто-анонс сабагента.** Это ровно тот путь, который 27.07 пробил
мягкий замок (ответ покупателю Sean по велику Giant). Транскрипт `agent:dirigent:main`:

    20:53:00 [user] A background task completed…
                    session_key: agent:worker3:subagent:d91e2ca1-…

Анонс пришёл **сессии Дирижёра**, а не `agent:main:main`. Заказчик сменился — путь к боту
Коли у этого нарратива отсутствует физически.

**4.4. Полный цикл: лид → воркер → доклад Боссу.**

    20:58:05 [channel] inbox_watcher → ЖЁСТКИЙ ЗАМОК: заказчик dirigent, бот dirigent
    20:58:37 PING-OK-3                                    ← воркер отработал
    20:58:45 Result: PING-OK-3 получен, канал живой.
    20:58:45 HARDLOCK-ANNOUNCE-6 анонс воркера доложен в канале Дирижёра. ⚙️
    20:58:45 [telegram] outbound send ok accountId=dirigent chatId=6284337254 messageId=9

**4.5. Канал Коли молчал.** Все отправки за сутки по аккаунтам:

    accountId=dirigent : 7   (все — после включения замка, 20:24…20:58)
    accountId=default  : 4   (05:23, 05:23, 15:43, 15:43 — ЗАДОЛГО до изменения)

После 20:10 в канал Коли не ушло ничего.

**4.6. Голосовой канал Босса цел.** Ради него всё и делалось через третьего бота:
`dirigent_voice.py` за весь час 20:xx — **ноль 409**, поллинг идёт ежеминутно.
Оба telegram-аккаунта: `enabled, configured, running, connected`.

## 5. ДВА ДЕФЕКТА, КОТОРЫЕ ВСКРЫЛИСЬ ПО ДОРОГЕ (оба закрыты)

**5.1. `NO_REPLY` в собственном канале.** Первый прогон анонса дал: агент `dirigent`
получил результат воркера и ответил `NO_REPLY`. Он выполнял `AGENTS.md §4a` — правило,
написанное для main, у которой сессия пришита к боту Коли. Воркспейс общий, а каналов два:
в канале Дирижёра это правило **инвертировано** — им агент затыкает себя в своём же
канале, и Босс остаётся без отчёта. Это было бы не утечкой, а немотой, что не лучше.
Правило переписано: §4a теперь начинается с вопроса «кто я» (по `session_key`).

**5.2. Правка §4a не подействовала с первого раза — и это ЗНАКОМЫЙ КЛАСС.** После
исправления `AGENTS.md` агент СНОВА ответил `NO_REPLY`. Причина в логе:
`useResume=true … reuse=reusable`. CLI-сессия резюмировалась и держала **бутстрап,
снятый до правки**. Это ровно вчерашний корень (`фикс на диске ≠ фикс в работе`), но на
слой выше: не долгоживущий демон держит старый модуль, а **живая сессия держит старый
системный промпт**. Сброс привязки к CLI-сессии (`route` сохранён) → `reuse=invalidated:
system-prompt` → правило заработало, см. 4.4.

**Вывод шире каналов: у «устаревшего кода» есть ТРИ слоя, а не два — файл на диске,
процесс-демон и РЕЗЮМИРУЕМАЯ СЕССИЯ.** Сторож `module_staleness` видит второй, третий
не видит никто.

## 6. РАЗВЁРТКА ДОВЕДЕНА ДО КОНЦА

По вчерашнему уроку: правка `lib/` не развёрнута, пока не перезапущен каждый живой
импортёр. `module_staleness check` нашёл двоих и был прогнан повторно:

    🔴 kola-inbox-watcher.service — НЕ ЗАГРУЖЕНО: lib/agent_capacity.py, lib/channel_policy.py
    🔴 kola-bridge.service        — НЕ ЗАГРУЖЕНО: lib/agent_capacity.py, lib/channel_policy.py
    → перезапущены →
    ✅ РАЗВЁРТКА ЧИСТА: ни один живой демон не старше модулей, которые он импортирует.

## 7. ЧТО ЗАМОК НЕ ПОКРЫВАЕТ (честная граница)

* Замок стоит на **пробуждениях** (`agent_capacity.wake()`). Если воркера спавнит сама
  `main` в своём разговоре с Колей — анонс придёт ей, и дальше работает мягкое правило.
  Это осознанно: main обязана оставаться сисадминской собеседницей.
* `hard_lock_target()` **fail-open по лиду**: нет агента/аккаунта/chat_id → откат на старое
  поведение (main + ⛔-блок). Терять лид ради канала нельзя.
* Вызыватель без файла (`python3 -c`, heredoc) по-прежнему не классифицируется путём —
  канал Коли, но ГРОМКО (предупреждение в stderr).

## 8. КОММИТЫ

    3429b2b  feat(channels): ЖЁСТКИЙ ЗАМОК — операционный лид принимает агент dirigent, не main
    eb1a639  docs(AGENTS): §4a теперь разводит main и dirigent — NO_REPLY верен только для одного

Оба — через авторизованный коммит-гейт (`lib/agent_capacity.py` в защищённых путях).

### Патч (суть, инлайном)

`lib/channel_policy.py` — резолвер цели замка:

```python
DIRIGENT_AGENT = "dirigent"      # agents.list[].id
DIRIGENT_ACCOUNT = "dirigent"    # channels.telegram.accounts.<id>

def hard_lock_target():
    """Куда переадресовать операционное пробуждение. dict | None.
    None = замок НЕ настроен → вызыватель ОБЯЗАН откатиться на мягкий замок:
    лид дороже канала (fail-open ИМЕННО здесь и только здесь)."""
    try:
        conf = json.load(open(_OC_CONF))
        agents = {a.get("id") for a in conf.get("agents", {}).get("list", [])}
        if DIRIGENT_AGENT not in agents:
            return None
        accts = conf.get("channels", {}).get("telegram", {}).get("accounts", {})
        acct = accts.get(DIRIGENT_ACCOUNT)
        if not acct or acct.get("enabled") is False:
            return None
        cid = str(json.load(open(_OC_SECRETS)).get("reportChatId") or "").strip()
        if not cid:
            return None
        return {"agent": DIRIGENT_AGENT, "account": DIRIGENT_ACCOUNT,
                "to": f"telegram:{cid}"}
    except Exception:
        return None      # любое сомнение → мягкий замок, но лид доставлен
```

`lib/agent_capacity.py` — переадресация на горле пробуждений:

```python
    _reply = []
    _tgt = f"{session_key or ''} {agent or ''}".lower()
    if "main" in _tgt:
        try:
            import channel_policy as _cp
            _ch, _why = _cp.classify(detector=detector)
            if _ch == _cp.DIRIGENT:
                _hl = _cp.hard_lock_target()
                if _hl:
                    agent = _hl["agent"]
                    if session_key:
                        session_key = session_key.replace("agent:main:",
                                                          f"agent:{_hl['agent']}:")
                    # У свежей сессии route=null — без явных флагов ответ осядет
                    # в stdout и Босс его НЕ УВИДИТ.
                    _reply = ["--deliver", "--reply-channel", "telegram",
                              "--reply-account", _hl["account"], "--reply-to", _hl["to"]]
                    msg = msg + _cp.native_block(_why)
                else:
                    msg = msg + _cp.routing_block(_ch, _why)   # замка нет → мягкий
        except Exception as _e:
            log(f"[channel-policy err] {_e}")   # политика не роняет пробуждение
```

## 9. ЧЕСТНЫЙ СТАТУС ПО ВЧЕРАШНЕЙ ТАБЛИЦЕ

| # | пункт | статус |
|---|---|---|
| 1 | отдельный бот-аккаунт | ✅ `@Dlyaderyzhorrr2_bot`, `accounts.dirigent`, connected |
| 2 | роутинг операционки | ✅ через смену ЗАКАЗЧИКА (`main → dirigent`), а не привязку воркеров |
| 3 | доказать живьём | ✅ полный цикл лид→воркер→доклад, движковые логи (п. 4.4) |
| 4 | подтвердить hard-lock | ✅ **ЗАМОК ЕСТЬ.** Исполняет КОД, не модель. Границы — в п. 7 |
