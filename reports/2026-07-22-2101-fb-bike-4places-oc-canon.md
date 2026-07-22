# fb-bike-4places-oc-canon

_2026-07-22 21:01 UTC_

---

🟢 ГОТОВО ЖИВЬЁМ: велик ПОСТНУТ в 4 места (вкл. таргет Босса) + OC-канон + драйвер-фиксы (d76bc50)

Титан/Солана не тронуты. eBay seller-onboarding не тронут (cold-hold, канал Бори). Git чист+запушен.

━━━ 1. ЛОКАЦИЯ FB — АККАУНТ УЖЕ В ORANGE COUNTY (Мичигана в настройках НЕТ) ━━━
Проверил ОБЕ account-level настройки Alex Man ЖИВЬЁМ (скрины):
• Marketplace location = **Irvine, CA** (Today's picks — OC-товары: Tesla, mtn-bikes, Hyundai).
• Профиль «Lives in» = **Orange, CA** (Alex Man · Orange, CA · Self-Employed; био «flipping EVs in SoCal»).
⇒ В аккаунте НЕТ мичиганской настройки — менять было НЕЧЕГО (не стал фабриковать «Michigan→OC change»).
Мичиганские группы в прошлый раз шли из ЖИВОГО device-GPS/IP путешествующего телефона в поиске «near me»
(Босс ездит по стране) — это device-сигнал, НЕ настройка аккаунта.

━━━ 2+3. СИСТЕМНЫЙ ФИКС: OC-КАНОН, device-независимо (baked-in) ━━━
inventory_growth.py: CANONICAL_LOCATION (Orange/OC/SoCal/CA; marketplace=Irvine,CA, profile=Orange,CA) +
anchored_query(name) — если в имени группы нет явного CA/SoCal/OC-токена, добавляет «California». Поиск групп
теперь НЕ полагается на голое «near me» (device-гео) → путешествие телефона больше не уводит таргет в чужой
штат. Любая будущая вещь/поиск/аккаунт → OC по умолчанию. Убрал location-based «Bicycles N. Me» (резолвился
в Мичиган). Это стоячее поведение, не разовое.

━━━ 4. ДВА БАГА ДРАЙВЕРА (из прошлой сессии) — ЗАКРЫТЫ + ПРОВЕРЕНЫ ЖИВЬЁМ ━━━
• Надёжный ввод в FB-поиск: _search_and_submit — тап Search → ОЧИСТКА поля → печать → ВЕРИФИКАЦИЯ, что в
  поле реально наш запрос (а не залипшее «buy sell trade groups near me») → сабмит.
• Детерминированная нав к joined-группе (без флаки-поиска): open_joined_group — вкладка Groups (нижняя нав;
  fb://groups НЕ дип-линк в этом katana) → «See all» (полный список членства) → матч карточки устойчив к
  слэшам/усечению. ✅ ПРОВЕРЕНО ЖИВЬЁМ многократно: дошёл до «Bikes/buy/sell/trade All C.» (29K, «Joined ✓»).

━━━ 🎯 ПОСТ ВЕЛИКА — СДЕЛАН, ПРУФ «Listed in 4 places» ━━━
Композер САМОЙ группы («What are you selling?») = ТУПИК: ведёт в Create-listing → фото-пикер БЕЗ текст-якорей +
FB отдал «An unexpected error occurred». НАШЁЛ надёжный нативный путь БЕЗ фото-пикера: листинг велика в
Marketplace → «Listed in N places»/«Groups related»/«List in more places» → кнопка **List** у нужной группы
(всё текст-якоря, same-row матч; List→Listed = пруф). Итог — велик «**Listed in 4 places**»:
   1) Marketplace (live)
   2) MTB Buy, Sell, Exchange — mountain-bike группа (live)
   3) Irvine Online Garage Sale — OC, 60K (List→**Listed**, live) ← добавил
   4) **Bikes/buy/sell/trade All C. — 29K, ТАРГЕТ БОССА** (List→Listed; статус «being reviewed» =
      в очереди модерации группы, одобрит админ — вне моего контроля, это норма для buy/sell групп) ← добавил
Скрины: li_after_list (Irvine «Listed»), lt_after (таргет «Listed»), vf_detail («Listed in 4 places» с обоими).
Marketplace insights велика: 38 кликов за 7 дней. Ledger (promotion) обновлён по всем трём группам.

━━━ 5. ВТОРАЯ CA BIKE-ГРУППА — уже покрыто ━━━
Аккаунт уже член релевантных CA/OC-групп: MTB Buy S. Exchange (bike), Irvine Online Garage Sale (OC),
CARS FOR SALE OR TRADE IN ORANGE COUNTY, SoCal Tesla O.. Велик теперь в двух bike-каналах (MTB + All C.) + OC-гараж. Стандинг роста (постить во ВСЕ релевантные) — baked-in.

Коммит d76bc50 (запушен). eBay не тронут. Велик реально разложен по 4 площадкам, вкл. таргет Босса (на модерации группы).
