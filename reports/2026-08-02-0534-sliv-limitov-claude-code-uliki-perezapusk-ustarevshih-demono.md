# Слив лимитов Claude Code — улики, перезапуск устаревших демонов, происхождение слива (ПРОМЕЖУТОЧНЫЙ)

_2026-08-02 05:34 UTC_

---

> ⏳ **ПРОМЕЖУТОЧНЫЙ ОТЧЁТ.** Шаги 1 и 2 закрыты и доказаны. Шаг 3 (60-минутный замер ПОСЛЕ
> перезапуска) идёт: старт 2026-08-02 05:29:27 UTC, конец ~06:29 UTC. Финальный отчёт со сравнением
> «до/после» уйдёт отдельной ссылкой. Публикую сейчас, потому что перезапуск боевого демона уже
> ВЫПОЛНЕН — работа сделана, значит отчёт обязан существовать, а не ждать конца замера.

## ГЛАВНОЕ В ТРЁХ СТРОКАХ

1. **Слив НЕ начался 28.07** — механизм жив с 04.07 и уже срывался всплесками (15.07 = 693 спавна).
   28.07 он стал ПОСТОЯННЫМ: включился аварийный стоп, и сбой из временного стал вечным.
2. **Перезапуск НЕ чинит слив.** Он лечит другое (устаревшие модули). Корень — аварийный стоп
   плюс ПОРЯДОК вызовов. Я предупредил об этом Босса ДО перезапуска, а не задним числом.
3. **Холостой ход ДО перезапуска: 63 спавна/час, ~750 250 billable + ~1 167 505 cache-read токенов/час
   ради 945 токенов выхлопа.** Все 63 — одна и та же петля.

---

## ШАГ 1 — УЛИКИ (собраны ДО любых действий)

### 1.1 Где Claude Code пишет транскрипты (найдено, не предположено)

`<home>/.claude/projects/<slug-от-cwd>/<session-uuid>.jsonl`

- `/root/.claude/projects/` — 133 файла, 571 МБ (интерактив)
- `/home/botuser/.claude/projects/` — 7 033 файла, 2.3 ГБ, 13 проектных каталогов (автоматика)
- всего просканировано **7 442** транскрипта; за 7 суток тронуто **4 479**

В каждой assistant-записи — точный биллинг:

```json
{"type":"assistant","timestamp":"2026-08-01T16:42:49.938Z","cwd":"/root",
 "entrypoint":"cli","version":"2.1.220",
 "message":{"model":"claude-opus-5","usage":{
   "input_tokens":2,"cache_creation_input_tokens":20559,
   "cache_read_input_tokens":20623,"output_tokens":304}}}
```

`entrypoint`: `cli` = интерактив, `sdk-cli` = headless `claude -p`. **Инструментировать нечего —
леджер уже есть.** Атрибуция спавна — по ПЕРВОМУ user-промпту сессии (grep по транскриптам врёт:
ловит чтения файлов и саму сессию аудита).

### 1.2 Точки спавна `claude` (file:line) и живой вердикт за 7 суток

| file:line | владелец | спавнов 7д | вердикт |
|---|---|---:|---|
| `projects/sales/inbox_agent.py:823` ← `inbox_watcher.py:285` | **inbox_watcher** | **4 139** | 🔴 петля |
| `lib/screen_sense.py:124` | eyes / зрение | 127 | ✅ |
| `scripts/autonomy/self_improve_daily.py:187,305` | само-разбор | 42 | ✅ |
| `lib/dirigent_brain.py:110,151,169` | dirigent_brain | 42 | ✅ |
| `scripts/main_liveness.py:101` (`openclaw agent`) | сторож main | 29 | 🔴 2.74 М ток/пинг |
| `projects/social_x/zdravurr_auto.py:1023`, `_ca_auto.py:917` | Ogon (X) | 20 | ✅ |
| `projects/fb_social/fb_engage.py:163` | Ogon (FB) | 1 | ✅ |
| `lib/kola_eyes.py:184,226` | eyes (модельное зрение) | **0** | ⚪ мёртвый |
| `lib/ogon_post.py:40` | Ogon | **0** | ⚪ мёртвый |
| `lib/llm_intent.py:63` | intent | **0** | ⚪ мёртвый |
| `projects/sales/listing_gen.py:88` | Senya | **0** | ⚪ мёртвый |
| `projects/sales/answer_backlog.py:87` | Senya | **0** | ⚪ мёртвый |
| `projects/sales/inbox_agent.py:396` | Senya (генерация ответа) | **0** | ⚪ мёртвый |
| `projects/social_x/zdravurr_post_now.py:188` | Ogon | **0** | ⚪ мёртвый |
| `scripts/kola-bridge/kola.py:244` | kola-bridge | **0** | ⚪ мёртвый |

**8 точек из 15 не стреляли ни разу за 7 суток.** `lib/kola_eyes.py` мёртв ПО ЗАМЫСЛУ
(`lib/eyes.py:29`: живые глаза — `uidump` + tesseract, не модель).

Оба пути ведут в ОДИН бинарь `/usr/bin/claude` (v2.1.220): напрямую через `subprocess`, либо через
`openclaw agent` → гейтвей → `claude -p`. Доказательство — `extensions/anthropic/cli-backend.ts:25-33`:

```ts
docker: { npmPackage: "@anthropic-ai/claude-code", binaryName: "claude" },
config: { command: "claude",
          args: ["-p","--output-format","stream-json","--include-partial-messages",
                 "--verbose","--setting-sources","user","--allowedTools","mcp__openclaw__*"], … }
```

`--setting-sources user` — вот почему хук `SessionStart` botuser'а бьёт и по headless-спавнам.

### 1.3 БАЗА ДО ПЕРЕЗАПУСКА — wake/trigger по целям за 24 ч

```
daemon                    event             count  target
inbox_watcher             trigger             720  fb_sales:<buyer-G>          30.0/h 🔴
inbox_watcher             debounce            539  fb_sales:<buyer-G>          22.5/h 🔴
agent_capacity            wake_refused        530  inbox_watcher               22.1/h 🔴
inbox_watcher             trigger             509  offerup:OfferUp             21.2/h 🔴
inbox_watcher             trigger             461  fb_sales:<buyer-R>          19.2/h 🔴
inbox_watcher             debounce            328  offerup:OfferUp             13.7/h 🔴
inbox_watcher             debounce            293  fb_sales:<buyer-R>          12.2/h 🔴
main_liveness             liveness_ping       287  (АВАРИЙНЫЙ)                 12.0/h 🔴
lead_guarantee            guarantee           144  lead-fb-sales-<A>            6.0/h
lead_guarantee            guarantee           144  lead-fb-sales-<B>            6.0/h
lead_guarantee            guarantee           144  lead-fb-sales-<C>            6.0/h
lead_guarantee            guarantee           144  lead-fb-sales-<D>            6.0/h
lead_guarantee            guarantee           144  lead-fb-sales-<E>            6.0/h
lead_guarantee            guarantee            97  lead-fb-sales-<G>            4.0/h
------------------------------------------------------------------------------
ЦЕЛЕЙ, СРАБОТАВШИХ БОЛЬШЕ ОДНОГО РАЗА: 14
  inbox_watcher  trigger        1690 событий (70.4/ч)
  inbox_watcher  debounce       1160 событий (48.3/ч)
  lead_guarantee guarantee       817 событий (34.0/ч)
  agent_capacity wake_refused    530 событий (22.1/ч)
  main_liveness  liveness_ping   288 событий (12.0/ч)
```

**Сходимость из трёх независимых источников.** В окне замера 00:25:17–01:25:20:

```
watcher.log:trigger        166
watcher.log:debounce       103
trigger - debounce   =      63
agent_capacity:wake_refused 63
ЗАМЕРЕНО спавнов            63   ← совпало байт-в-байт
```

---

## ШАГ 2 — ПЕРЕЗАПУСК УСТАРЕВШИХ ДЕМОНОВ (выполнено)

### 2.1 Поправка к вводным

`kola-inbox-watcher.service` **есть**, но это unit пользователя **botuser** (`systemctl --user`),
поэтому из-под root он «не найден». Подтверждено: `MainPID=3733399`,
`ExecMainStartTimestamp=Tue 2026-07-28 12:48:09 UTC`, `NRestarts=0`, аптайм **110.0 ч**.
Файл: `/home/botuser/.config/systemd/user/kola-inbox-watcher.service`, `WATCH_INTERVAL=25`.

### 2.2 Проверка ВСЕХ долгоживущих демонов (mtime модуля vs время старта процесса)

Штатный `lib/module_staleness.py` нашёл ОДИН устаревший модуль. Моя независимая проверка по
рекурсивному графу импортов нашла **три**:

```
     pid user      uptime_h  script
     939 root         466.6  🔴 STALE  mercury-sol/optimizer_listener.py
                               config.py изменён +460.1ч ПОСЛЕ старта
 1793223 root         284.1  ✅ fresh  titan-bot/optimizer_listener.py
 3647921 root         116.4  ✅ fresh  titan-bot/gemini_bridge.py
 3733399 botuser      110.0  🔴 STALE  projects/sales/inbox_watcher.py
                               lib/report_publish.py    +23.1ч ПОСЛЕ старта
                               lib/thread_read.py        +1.2ч ПОСЛЕ старта
                               projects/sales/notif_watch.py +1.3ч ПОСЛЕ старта
  970191 botuser       20.3  ✅ fresh  scripts/kola-bridge/server.py
```

**mercury-sol НЕ ТРОГАЛ** (приказ: Solana/Mercuri не касаться) — только фиксирую факт.
**Титан НЕ ТРОГАЛ** — и он свежий, повода не было.

### 2.3 Перезапуск

Босс предупреждён в канале Дирижёра **ДО** действия (демон buyer-facing), затем:

```
=== BEFORE ===  MainPID=3733399  NRestarts=0  ExecMainStartTimestamp=Tue 2026-07-28 12:48:09 UTC
=== RESTART === rc=0
=== AFTER  ===  MainPID=1335059  NRestarts=0  ExecMainStartTimestamp=Sun 2026-08-02 05:28:00 UTC
                ActiveState=active  SubState=running   is-active: active
```

**Подтверждение загрузки модулей:**

```
штатный module_staleness.scan()      → stale daemons: 0  ✅ NONE
независимая проверка (33 модуля)     → STALE now: ✅ NONE
   report_publish.py mtime=07-29 11:54 < start ✅
   thread_read.py    mtime=07-28 14:02 < start ✅
```

**Подтверждение, что очередь не потеряна:**

```
watcher_routed.json  17 записей ДО → 17 записей ПОСЛЕ (не тронут)
watcher_seen.json    1000 записей сохранены
client_pending.json  жив, перезаписан 05:28:13
детекция возобновилась через 6 секунд:
  05:28:00 watcher start DETECTION-ONLY (interval=25s …)
  05:28:06 [fb_sales] PRIORITY mark client pending: <buyer-R>
  05:28:13 [offerup]  PRIORITY mark client pending: OfferUp
```

Ни один лид не потерян.

---

## ШАГ 4 (частично) — НАЧАЛСЯ ЛИ СЛИВ 28.07?

**ОТВЕТ: НЕТ. Механизм старше. 28.07 слив стал ПОСТОЯННЫМ.**

Спавны `translate_ru` по дням, ВСЯ история (7 442 транскрипта):

```
2026-07-04      2        43,530     ← самый ранний спавн на записи
2026-07-05      5       108,804
2026-07-06     58     1,284,079   ###
2026-07-07      2        43,638
2026-07-08      3        65,537
2026-07-09     69     1,512,002   ####
2026-07-10      8       174,477
2026-07-11     19       423,651   #
2026-07-12      6       157,210
2026-07-13      6       157,852
2026-07-14     87     2,048,860   #####
2026-07-15    693    15,881,687   ##############################################  ← ранний срыв
2026-07-16      1        22,476
2026-07-17      1        44,464
2026-07-18      1        22,275
2026-07-20      1        22,159
2026-07-21      1        21,842
2026-07-24      2        45,584
2026-07-25      1        30,416
2026-07-26      5       152,258
2026-07-27      5       152,482
2026-07-28    207     6,315,090   #############   ← аварийный стоп 15:10:23Z
2026-07-29    901    27,461,336   ############################################################
2026-07-30   1655    50,391,713   ############################################################
2026-07-31    949    22,636,592   ############################################################
2026-08-01    356     5,331,239   #######################
2026-08-02    340    10,357,700   ###################### (неполный день, до 05:30)
```

Читается так:

- **Норма** 16–27.07: **1–5 спавнов в сутки** — настоящие лиды, механизм здоров.
- **Ранние срывы**: 06.07 (58), 09.07 (69), 14.07 (87), **15.07 (693)** — тот же сбой,
  но ВРЕМЕННЫЙ: назавтра возвращалось к 1/сутки.
- **28.07** — 207 спавнов, аварийный стоп в 15:10:23Z.
- **С 29.07 к норме НЕ ВЕРНУЛОСЬ НИ РАЗУ.** 901 → 1655 → 949 → 356 → 340.

Сверка: 02.08 — 340 спавнов за 5.5 ч = **62/час**, что совпадает с замеренными 63/час.

**Вывод: 28.07 не создало дефект, а СНЯЛО С НЕГО ПРЕДОХРАНИТЕЛЬ.** Раньше сбой сам рассасывался,
потому что `wake()` рано или поздно проходил и ставил метку дедупа. С 28.07 стоп сделал успешный
`wake()` НЕВОЗМОЖНЫМ — метка не ставится никогда, и петля больше не имеет выхода.

---

## КОРЕНЬ (для полноты — детально в предыдущем отчёте)

`projects/sales/inbox_watcher.py`, `route_to_main()`:

```
276     if now - prev < ROUTE_DEBOUNCE_S:      # 90 с на отправителя
277         log("debounce … пропуск"); return
280     if _routed_seen(route_key, now):       # дедуп 7 дней — ТОЛЬКО ЧИТАЕТ
            return
285     ru = inbox_agent.translate_ru(text)    # 🔴 ПЛАТНЫЙ спавн Opus (~30k ток)
…
321     if _ac.wake(MAIN_AGENT, msg, …):       # 🔴 ГЛУШИТСЯ аварийным стопом
322         _routed_mark(route_key, now)       # ← метка дедупа, НЕДОСТИЖИМА
```

Стоп глушит БЕСПЛАТНЫЙ шаг (разбудить локального агента) и пропускает ПЛАТНЫЙ.
Метка «сделано» стоит НИЖЕ того, что отказывает → дедуп не наступает никогда.

Живое подтверждение, что стоп цел и после перезапуска:

```
2026-08-02T05:28:13+0000 [STOP] inbox_watcher: АВАРИЙНЫЙ СТОП (с 2026-07-28T15:10:23Z) — НЕ бужу main.
2026-08-02T05:28:20+0000 [STOP] inbox_watcher: АВАРИЙНЫЙ СТОП (с 2026-07-28T15:10:23Z) — НЕ бужу main.
```

Отягчающее: `inbox_agent.py:823` вызывает `claude -p` **БЕЗ `--model`** → дефолт аккаунта
= **Opus 5** на перевод из десяти слов. Выхлоп 11–18 токенов при 30 448 входных.

---

## ЧТО ДАЛЬШЕ

Идёт 60-минутный замер ПОСЛЕ перезапуска (05:29:27 → ~06:29 UTC). В финальном отчёте будет:
таблица «до/после» по спавнам и токенам, повтор wake/trigger-счётчиков, и предложения по фиксам
с ожидаемой экономией. **Фиксы, кроме перезапуска, НЕ применял.**

Ранний сигнал (первые ~3 мин окна): 0 новых спавнов. Слишком короткий отрезок, чтобы делать
вывод, — не выдаю за результат.
