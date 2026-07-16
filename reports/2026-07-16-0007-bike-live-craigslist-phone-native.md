# bike-LIVE-craigslist-phone-native

_2026-07-16 00:07 UTC_

---

# ✅ ВЕЛИК ЖИВОЙ НА CRAIGSLIST — реальный URL (phone-native, без туннеля) — 2026-07-16

## 🔴 ГЛАВНОЕ: ВЕЛИК ОПУБЛИКОВАН И ПРОВЕРЕН ЖИВЬЁМ
**https://orangecounty.craigslist.org/bik/d/trabuco-canyon-giant-rainier-26in/7947463363.html**

Проверил внешним запросом (чистый IP): заголовок «Giant Rainier 26in Mountain Bike -
Aluminum, Disc Brakes, RockShox — bicycles — by owner», цена $100, НЕ удалён/не истёк —
публично доступен. Это НЕ pending, это LIVE.

## КАК — правильная архитектура (твоя идея, сработала)
Выкинул server→SSH→SOCKS→proxy. Publish пошёл через СОБСТВЕННЫЙ Chrome телефона по CDP/ADB —
мобильный 5G-IP телефона = чистый резидентный IP, CL его принял. Путь:
1. Логин в аккаунт CL в Chrome телефона: пароль → CL сказал «further verification» → нажал
   «one-time login link» → письмо со ссылкой пришло на наш gmail → прочитал по IMAP → открыл
   ссылку в Chrome телефона → ЗАЛОГИНЕН на мобильном IP.
2. Запостил велик через залогиненный флоу: OC → for-sale-by-owner → bicycles → форма
   (заголовок/цена/ZIP/описание) → geoverify → done-with-images → **publish**.
Никакого SSH-туннеля, никакого server-прокси. ADB (стабилен) + Chrome телефона.

## ОТВЕТЫ НА ТВОИ ПУНКТЫ
1. ✅ Велик LIVE с реальным URL (см. выше, проверен). Ответы покупателей идут через CL
   email-relay → mail_watch → Сеня.
2. Твой шаг НЕ понадобился: «further verification» закрыл сам (one-time link с нашего gmail).
3. OfferUp — СЛЕДУЮЩИЙ, тем же нативным путём (ADB, без litho-проблемы). В этот заход не
   успел — приоритет был «велик LIVE», сделано. OfferUp сделаю следующим.

## ЧЕСТНЫЕ ХВОСТЫ (не критично)
- Фото пока НЕ приложены (текстовый листинг подняли первым, чтобы быстрее LIVE). Фото есть
  в .kola_state/bikepix/ — добавлю тем же CDP-путём (Add I.) отдельным шагом.
- Chrome телефона по CDP иногда отваливался (фоновый) — лечится force-launch + re-forward
  через ADB; листинг CL сохраняется по-шагово на сервере, поэтому дожал без потерь.

## ПОБОЧНО ЗАКРЫТО В СЕССИИ
- Pixel sshd вычищен+закалён (MaxStartups 60:30:200) — здоровит весь телефон-транспорт.
- Playwright chromium восстановлен; форма CL починена (оба — жертвы переезда).
- Архитектура CL-публикации переведена на phone-native (koly-proxy/туннель списаны).

Записал URL в .kola_state/live_listings.json (bike_giant_rainier=live). Titan+Solana НЕ тронуты.
