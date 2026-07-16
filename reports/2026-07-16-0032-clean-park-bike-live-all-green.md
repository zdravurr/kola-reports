# clean-park-bike-live-all-green

_2026-07-16 00:32 UTC_

---

# ЧИСТАЯ ПАРКОВКА НА НОЧЬ + подтверждение — 2026-07-16

## ✅ ГЛАВНЫЙ ИТОГ: ВЕЛИК ПРОДАЁТСЯ НА CRAIGSLIST (проверено сейчас — LIVE)
https://orangecounty.craigslist.org/bik/d/trabuco-canyon-giant-rainier-26in/7947463363.html
Опубликован через phone-native Chrome (мобильный IP, без туннеля). Ответы → CL relay → Сеня.

## ✅ ВСЁ ЗАКОММИЧЕНО, ДЕРЕВО ЧИСТОЕ
Последние коммиты сессии: 19db4c7 (велик LIVE), a0a2863 (восстановление CL: chromium+форма+eSIM),
446eca1 (never-silent+Opus-каркас), bff2db5 (Opus-разбор речи), 6d78a7c (инвентаризация),
547d3e7 (Сеня продаёт с задачи). git status = CLEAN.

## ✅ ЗДОРОВЬЕ — ЗЕЛЁНОЕ
- load 1.0 · mem 69% · gateway 200
- Дирижёр контейнер Up 9h · голосовой поллер жив · интейки живы (FB/OfferUp/Craigslist/Nextdoor)
- Полосы: procurement=paused · sales=live · warmup=live (17 warmup-кронов активны)
- Titan active · host armored (adj 600) · Pixel sshd вычищен+закалён (MaxStartups 60:30:200)
- нет зависших ssh -D · **Titan + Solana НЕ тронуты**

## 📋 ЗАПАРКОВАНО НА СЛЕДУЮЩУЮ СЕССИЮ (сохранено: .kola_state/NEXT_SESSION_TASKS.md)
1. **ФОТО на CL-велик** — нативным Android-пикером (тап «Add I.» → системный файл-пикер →
   выбрать b1-3.jpg из /sdcard/bikepix через ADB/uiautomator-тапы). Обходит песочницу Chrome +
   iframe CL. Фото уже на телефоне и в .kola_state/bikepix/.
2. **OfferUp** — выставить велик тем же нативным ADB-путём, получить live-URL.
3. **Recurring renew/bump КРОН** + надзор Дирижёра (каденция на платформу).
4. **(Отдельно) FB Marketplace + группы** — VISION-сессия (litho UI без узлов).

## КЛЮЧ (не потерять): CL работает через phone-native Chrome (CDP/ADB, мобильный IP), НЕ туннель.
Логин: пароль → «further verification» → one-time login link с gmail (IMAP) → открыть в Chrome
телефона. scripts/cl_post_bike_phone.py — рабочий постер. Туннель/koly-proxy СПИСАНЫ.

Спокойной ночи. Велик реально продаётся. Остальное — чисто запарковано.
