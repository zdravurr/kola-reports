# openclaw-clean-restart

_2026-07-16 02:12 UTC_

---

# ✅ ЧИСТЫЙ ПОЛНЫЙ РЕСТАРТ СТЕКА OpenClaw — всё вернулось из закоммиченного состояния (2026-07-16)

Финальная верификация: стек РЕАЛЬНО поднимается из коммита, а не «просто был up 11ч».
Опустил дочиста → поднял из committed config → проверил КАЖДЫЙ пункт живьём.
**Titan и Solana НЕ тронуты сквозь весь цикл — те же PID до и после.**

## СНЯЛ СОСТОЯНИЕ ДО (baseline)
Titan pids 72507/474878 · Sol pids 72522/72623 + optlistener 939 · gateway 200 ·
Дирижёр started 15:28:16 · loop.sh 448534 · полосы procurement=paused·sales=live·warmup=live.

## 1. DOWN — чисто (проверено)
gateway→inactive · kola-inbox-watcher→inactive · dirigent контейнер→exited · live workers=[].
БЕЗОПАСНОСТЬ в момент DOWN: Titan 72507/474878 + Sol 72522/72623 — ТЕ ЖЕ pid, active.
Все команды — только `systemctl --user` (botuser) или docker: структурно НЕ могут достать Titan/Sol.

## 2. UP — из закоммиченного состояния (проверено)
`docker start dirigent` → running, **свежий старт 02:08:05** (не старый uptime — реальный рестарт).
`systemctl --user start openclaw-gateway` → active · `... kola-inbox-watcher` → active.

## 3. ВСЁ ВЕРНУЛОСЬ — инспекция живьём (не заявлено — проверено)
- **gateway**: HTTP **200** ✓
- **Дирижёр контейнер**: running, restarts=0, **новый loop.sh pid 537670** (свежий оркестратор) ✓
- **оркестратор тикает**: dirigent_cron.log `02:08:09 [idle] все лиды на паузе` — тик ПОСЛЕ рестарта ✓
- **голосовой поллер жив + ACK**: живой тест — прогнал команду через тот же handler, что и поллер:
  `02:09:44 [cmd] role=boss intent=status` → ответ ушёл Боссу. **Пост-рестарт команда получает ack** ✓
- **daemon/inbox-watcher**: active ✓
- **интейки живы**: 4 intake-крона (fb_inbox_sweep/inbox_sweep/mail_watch/buyer_watchdog) + inbox-watcher active ✓
- **крон renew+supervisor**: 3 листинг-крона (listing_supervisor + cl_renew_bike) зарегистрированы ✓
- **полосы после рестарта**: **procurement=paused · sales=live · warmup=live** — верно, из committed state ✓
- **байк LIVE**: Craigslist публичный листинг отвечает «rainier» → **LIVE** ✓
  (FB/OfferUp — app-gated, серверный curl невозможен; их phone-native надзор на очереди.)

## 4. Titan + Solana — НЕ ТРОНУТЫ СКВОЗЬ ВЕСЬ РЕСТАРТ (главное)
- **Titan**: active, pids **72507 / 474878** = РОВНО как до (were 72507 474878) — ни разу не рестартнут ✓
- **Solana**: active, pids **72522 / 72623** = как до · optlistener **939** = как до ✓
Идентичные PID = процессы НИ РАЗУ не перезапускались. Оба работали сквозь весь цикл.

## 5. ЗДОРОВЬЕ — ЗЕЛЁНОЕ
load **0.75** · mem **70.5%** · overload level **ok** · gateway **200/alive**.

## ИТОГ
Стек опущен и поднят из закоммиченного состояния — вернулось ВСЁ: gateway 200, Дирижёр-контейнер
(свежий loop.sh + оркестратор тикает), голосовой поллер (живая команда получила ack), daemon,
интейки, renew/supervisor-кроны, полосы (paused/live/live), байк на CL. Ничего не осталось лежать.
**Titan и Solana прошли весь рестарт с идентичными PID — не тронуты, не рискованы, ни разу не рестартнуты.**
Health зелёный. Финальная верификация пройдена.
