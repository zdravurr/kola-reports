# sell-cycle-forensics-found

_2026-07-15 23:00 UTC_

---

# ФОРЕНЗИКА: sell-cycle Сени — НАЙДЕНО, и почему встало (по фактам) — 2026-07-15

Ты прав: не строить с нуля — искать существующее. Нашёл. Ниже пути, механизм и НАСТОЯЩАЯ
причина. И — важное: часть того, что «работало», уже тогда было ФЛАКИ, это в записях системы.

## 1. НАЙДЕННЫЙ РАБОЧИЙ КОД (пути)
- `scripts/zina_post_now.py` — постинг FB Marketplace + OfferUp, навигация в «Your L.»
  через find(xml,"marketplace")+тап (НЕ deep-link).
- `scripts/fb_mp_giveaway.py` — создание листинга FB MP с фото (title/price/photos → Publish).
- `scripts/cl_post_giveaway.py`, `scripts/cl_post_bike.py`, `cl_login_publish.py`,
  `cl_publish_drafts.py`, `cl_activate_pending.py` — постинг Craigslist.
- `scripts/fb_bike_listing_edit.py` — правка листинга ВЕЛОСИПЕДА + КРОСС-ПОСТ в 1-2 локальные
  OC bike-группы (да, групповой постинг был кодом).
- Состояние-улика: `.kola_state/zina_giveaway_progress.json` (аудит 09.07 12:52 UTC).

## 2. КАК ЭТО РАБОТАЛО — по платформам (дословно из аудита 09.07)
- **OfferUp — НАДЁЖНО:** desk/coffee/sofa все «published_live_verified».
- **Craigslist — НАДЁЖНО:** coffee/sofa «published_live_verified» с РЕАЛЬНЫМИ URL:
  orangecounty.craigslist.org/.../7946029747.html (coffee), /7946029738.html (sofa), desk продан.
- **FB Marketplace — УЖЕ ТОГДА ФЛАКИ:** coffee «published_live_verified», НО sofa
  «BLOCKED_fb_litho_no_nodes». Цитата аудита: *«FB katana litho UI exposes no accessibility
  nodes, all create-listing deeplinks dead, blind taps drift to launcher → not reliably
  automatable via ADB»*.
- **Nextdoor — ЗАБЛОКИРОВАН:** все 3 «needs SMS verification code from Boss's phone».
- Механизм: ADB (`adb -s 100.85.178.10:5555`) + uiautomator find-text + тап. Работает там, где
  у приложения ЕСТЬ текстовые узлы (OfferUp/CL/старый FB-composer). FB katana (litho) узлов НЕ
  отдаёт → ровно там и рвётся.

## 3. ПОЧЕМУ НЕ РАБОТАЕТ СЕЙЧАС — настоящая причина (не одна)
1. **Это была РАЗОВАЯ кампания-раздача мебели Зины, а НЕ постоянный крон.** Проверил ВСЕ
   бэкапы crontab — sell-cycle крона (mp_giveaway/zina_post/cl_post/renew) НЕТ НИ ОДНОГО.
   Её запускал ГЛАВНЫЙ АГЕНТ вручную/оркестрацией под задачу.
2. **Кампания ЗАВЕРШИЛАСЬ 09.07:** мебель раздали/продали (стол забрали 13:17 UTC 09.07,
   Зина подтвердила). Постить стало нечего → автоматика естественно кончилась.
3. **Переезд в контейнер + GLOBAL_STOP 13.07** — главный агент перестал вызываться под
   sell-cycle. Плюс транспорт мигрировал ADB→pixel_ssh (ADB сейчас, впрочем, ЖИВ — проверил).
4. **Велик ($100, всё ещё for_sale)** имеет листинг, но РЕКУРРЕНТНОГО renew/promote крона
   никогда и не было — обновляли руками/по случаю.
5. **Сегодняшний провал FB-навигации = ТОТ ЖЕ litho-блокер из 09.07, НЕ регресс от меня.**
   Deep-link’и мертвы и тогда, и сейчас; текстовых узлов FB не отдаёт — подтвердил скрином.

## 4. ЧТО РЕАЛЬНО ВОССТАНАВЛИВАЕТСЯ (честно, без вранья)
- **OfferUp + Craigslist — ДА, восстановимо надёжно:** код цел (пути выше), ADB жив. Их можно
  впрячь в Сеню/Дирижёр (senya_sell уже есть) + расписание renew. Это реальная опора sell-cycle.
- **FB Marketplace — тот же барьер, что был:** litho без узлов. Надёжно его берёт НЕ find-text,
  а VISION-тапы (скрин → модель находит кнопку → тап по координатам). Это настоящая работа,
  которую и тогда до конца не довели (coffee прошёл, sofa — нет). Не буду выдавать за «готово».
- **Nextdoor — тот же блокер:** SMS-код с твоего телефона (ручной шаг Босса).
- **Группы — код есть (fb_bike_listing_edit кросс-пост), но флаки как весь FB katana.**

## ЧЕСТНАЯ РЕКОМЕНДАЦИЯ (порядок)
1. Впрячь OfferUp+Craigslist постинг/renew в Сеню (надёжная опора) — могу сделать.
2. FB Marketplace + группы: один корень — VISION-навигация litho-UI (скрин+модель вместо
   text-nodes). ЭТО и есть настоящая «недоделка», общая с поиском Бори. Отдельный фокус.
3. Nextdoor: по одному SMS-коду от тебя на верификацию — разово.

Итог: код НАЙДЕН и цел; встало не «сломалось при переезде», а «разовая кампания закрылась +
рекуррентного крона не было + FB litho был флаки изначально». Titan+Solana НЕ тронуты.
