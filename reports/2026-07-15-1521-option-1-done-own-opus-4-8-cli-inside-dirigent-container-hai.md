# Option 1 done — own Opus 4.8 CLI inside dirigent container, Haiku rolled back

_2026-07-15 15:21 UTC_

---

# ВАРИАНТ 1 ВЫПОЛНЕН: свой Opus 4.8 CLI ВНУТРИ работающего контейнера Дирижёра — 15.07.2026

Босс выбрал Вариант 1: доставить Opus 4.8 CLI в УЖЕ ЖИВОЙ контейнер `dirigent` (не мигрировать).
Сделано аддитивно, контейнер НЕ пересоздавался, ничего не сломалось. Титан/Солана не тронуты.

## ЧТО СДЕЛАНО
1. **node v24.18.0 + claude-code 2.1.205** (та же версия, что у проверенных claude-agent) поставлены
   НА ТОМ: `<workspace>/.tools/node` и `<workspace>/.tools/npm`. Официальный node-tarball (glibc-совместим
   с Debian 12 контейнера; бинарь агентов Ubuntu 24.04 копировать НЕЛЬЗЯ — GLIBC новее). Владелец uid 1000.
   **Переживает рестарт контейнера БЕЗ пересоздания** (том персистентный + glibc в образе).
2. **Аутентификация — свой файл creds** на томе `<workspace>/.tools/claude-home/.claude/.credentials.json`
   (600, gitignored, НИКОГДА не в git/отчёте). Аккаунт пока общий Max (разделение аккаунтов — отложенное
   решение Босса). CLI сам обновляет токен при использовании (файл writable на томе).
3. **Модель Opus 4.8.** `_llm_text` переписан: хост → свой claude на PATH; контейнер → свой claude на томе
   с своим node и creds; `--model claude-opus-4-8`.
4. **Haiku-API fallback ПОЛНОСТЬЮ откачен.** Общий ключ Титана убран из досягаемости sales-контейнера
   (`.kola_state/anthropic_key` удалён). Больше никакого пересечения с трейдинг-миром.
5. **3 простаивающих claude-agent — оставлены как есть** (спэры Босса на будущее): не удалял, не подключал.

## ДОКАЗАНО ЖИВЬЁМ (железное правило)
- **CLI + Opus 4.8 в dirigent:** `claude --version` → 2.1.205; `claude -p --model claude-opus-4-8` → «DIRIGENT-OPUS-ALIVE».
- **Нюанс-ответ через in-container Opus** (тот же вопрос, что тестировал на Haiku):
  - Вопрос: «Any scratches or dents on the frame? And does everything shift and brake ok?»
  - **Opus 4.8:** «No dents, just normal light wear on the frame — nothing major. Shifts and brakes smooth, front and rear disc brakes work great 👍 You looking to grab it soon?»
  - **Haiku (было):** «Yep, it's in good shape — normal light wear, nothing major. Shifts and brakes work smooth, rides real nice 🚴 What's your height?…»
  - Opus точнее отвечает на дефекты (прямо «no dents»), называет дисковые тормоза из спеки, ведёт к закрытию. Оба grounded (только факты item_records), без выдумок и утечки локации.
- **Изоляция ЦЕЛА с установленным CLI (изнутри dirigent):** uid=1000 (не root); sudo — ABSENT; su root — Authentication failure; systemctl — ABSENT; docker.sock — ABSENT; trades.db — НЕТ; /root — Permission denied; titan-bot — нет; claude работает под uid 1000 (локальный инструмент, не root).
- **Дирижёр НЕ сломан:** оркестратор циклится (свежий лог, обрабатывает лиды; предохранитель MAX_FAILS=2 корректно увёл залипшую Michelle человеку и пошёл к Irena); Pixel достижим (adb `device`).
- **Titan + Solana:** active, oom -900 оба — не тронуты.

## КОММИТ
`18d80b3` (kola-workspace, запушен). `.tools` (node+claude+creds) — gitignored, в git не уходит.

## ОТКРЫТЫЕ КАВЕАТЫ (честно)
- **Аккаунт общий** (host + агенты + теперь dirigent = один Max). Разделение аккаунтов на мир — отложено Боссом.
- **Рестарт не проверял живьём** (не стал трогать работающий контейнер по твоему указанию). Персистентность
  доказана конструктивно: всё на томе + glibc в образе; при рестарте `_llm_text` находит claude на томе.
- Токен обновляется самим CLI при использовании; если dirigent долго не зовёт агента — обновится при следующем.
