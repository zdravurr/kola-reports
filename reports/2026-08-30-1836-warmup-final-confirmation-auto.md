# warmup-final-confirmation-auto

_2026-08-30 18:36 UTC_

---

# ФИНАЛЬНОЕ ПОДТВЕРЖДЕНИЕ ПРОГРЕВОВ — 30.08.2026

_Собрано автоматически после конца обоих заходов._

## ПРЯМОЙ ОТВЕТ

✅ **@zdravurr — ЗАВЕРШЁН.** `last_ok` = 18:35:28Z, деталь: `session n=3 img=True post=False`

🔴 **@zdravurr_ca — НЕ завершён.** Старт 17:12:06Z, успеха после него нет.
   Причина: `заход СРЕЗАН крон-таймаутом (SIGTERM) на 30.0-й минуте при бюджете крона 40 мин — СТАРТОВАЛ вовремя и убит снаружи, крон и run_guarded ни при чём`

**Набор контрактов после заходов:** ✅ ✅ ВСЕ КОНТРАКТЫ ЗЕЛЁНЫЕ

**Оба захода зелёные:** НЕТ

---

## ХРОНОЛОГИЯ ПРОГОНА

```
=== zdravurr_ca start 17:11:41Z ===
=== zdravurr_ca finished rc=124 at 17:42:10Z ===
=== zdravurr start 17:42:10Z ===

[finisher] раннер prove.sh был убит вместе с фоновой задачей сессии;
[finisher] заход @zdravurr пережил его сиротой и доработал сам.
[finisher] строку «zdravurr finished» и ALL_DONE писать было НЕКОМУ —
[finisher] вердикт взят из warmup_health.json, который пишет САМ заход.
```

## СОСТОЯНИЕ СТОРОЖА (сырое)

```json
{
 "zdravurr": {
  "cold_start": 1784461319.4048152,
  "last_ok": 1788114928.6370635,
  "last_ok_detail": "session n=3 img=True post=False",
  "broken_streak": 0,
  "last_start": 1788111736.9089186,
  "last_start_detail": "слот крона"
 },
 "zdravurr_ca": {
  "cold_start": 1784461319.405258,
  "last_ok": 1788047937.3069386,
  "last_ok_detail": "session n=3",
  "broken_streak": 0,
  "alerted_gap": 1788107404.979809,
  "last_start": 1788109926.402677,
  "last_start_detail": "слот крона",
  "last_refusal": 1788111726.183513,
  "last_refusal_reason": "заход СРЕЗАН крон-таймаутом (SIGTERM) на 30.0-й минуте при бюджете крона 40 мин — СТАРТОВАЛ вовремя и убит снаружи, крон и run_guarded ни при чём",
  "last_refusal_kind": "lawful"
 }
}
```

## НАБОР КОНТРАКТОВ

```
✅ test_x_onboarding_nudge_dropped_as_noise.py
ИТОГО: 164/164 зелёных за 36с (по 8 разом); медленные: test_absent_target_is_an_answer.py (11с), test_generic_solve.py (20с), test_obstacle_dismissal_general.py (12с), test_one_warmup_at_a_time.py (17с), test_screen_healer_not_locked_out_by_its_own_session.py (20с)
✅ ВСЕ КОНТРАКТЫ ЗЕЛЁНЫЕ
```

---

## ЧТО ЭТО ЗНАЧИТ

Утром сторож не мог отличить «убит» от «не запускался» и сочинил Боссу диагноз
«джоба НЕ СТАРТОВАЛА — смотреть крон botuser и run_guarded.sh»; оба компонента были
исправны. Теперь у каждого захода есть отметка старта, а смерть от `timeout` называет
себя словами — что и видно в состоянии сторожа выше.

Коммиты: `2e3f42f` (подобрана зависшая работа), `8fa0b5c` (корень: старт записан, смерть
именована, вердикт честен, тревога заводит задачу), `9b1a72e` + `378879a` (бюджеты едут
вместе с `timeout` — сначала ярлык, потом механизм).

Титан / Солана не тронуты.
