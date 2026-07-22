# ca-yield-multicooker-cl-ebay-groupnav-22jul

_2026-07-22 14:39 UTC_

---

🟢 ca-yield ФИКС (доказан живьём) + мультиварка на CL ЖИВА + eBay draft собран + group-nav фиксы

Титан/Солана НЕ тронуты. Git чист+запушен (kola-workspace-backup). Скрины — отдельными фото к этому отчёту.

━━━ 1) ca↔fin ЯASYMMETRY ПОЧИНЕНА — ДОКАЗАНО ЖИВЬЁМ (f4b4dd7) ━━━
Корень 13:00 «ca молчит» + блокировки всей очереди: zdravurr_ca_auto НЕ имел механизма
yield-to-money, который есть у zdravurr_auto. Итог: без ПРЕД-ГЕЙТА ca лез брать tab_lock, даже
когда телефон держит money-path (ждал/падал → «молчит»); без MID-SESSION yield держал экран весь
заход (~28м) и не уступал ни покупателю, ни другой работе.
ФИКС — порт того же механизма, что у fin: _warmup_should_yield_to_money (метка x_warmup),
_yield_phone_and_wait (ФИЗИЧЕСКИ снимает tab_lock → ждёт ухода клиента → забирает обратно →
продолжает ТОТ ЖЕ заход), ПРЕД-ГЕЙТ в __main__, _SESSION_LOCK + проверка в sustained-цикле.
ЖИВОЙ ПРУФ (harness на реальном телефоне): ca держит tab_lock (flock_free=False) → пометил
покупателя → flock_free=True ВЕСЬ период (телефон СВОБОДЕН для money-path) → покупатель ушёл →
tab_lock ЗАБРАН обратно за 15с, вернул True. Money-path прерывает ca-заход так же, как fin.

━━━ 2) МУЛЬТИВАРКА CRAIGSLIST — ✅ ОПУБЛИКОВАНА ЖИВЬЁМ ━━━
Прошёл весь веб-флоу CL через Chrome CDP + eyes, скрин каждого шага: skip reuse → area orange
county → for sale by owner → appliances → форма (тайтл/цена $100/город Rancho Santa Margarita/ZIP
92688/описание/make Zojirushi/model EL-CAC60) → geo-verify 92688 → 3 фото → preview → publish.
Экран «Thanks for posting!» + живой URL подтвердил:
orangecounty.craigslist.org/app/d/trabuco-canyon-zojirushi-multicooker-el/7948754253.html
Мультиварка теперь ЖИВА на OfferUp + Craigslist + FB (все три со скрин-пруфом).

━━━ 3) eBay ВЕЛИК — ✅ DRAFT ПОЛНОСТЬЮ СОБРАН, ⛔ публикация упёрлась в ПАРОЛЬ ━━━
Прошёл живьём: Create listing → prelist → категория Sporting G. > Cycling > Bicycles
(авто-детект) → Continue without match → condition Used → форма: 2 ФОТО ВЕЛИКА (скачал из живого
CL-листинга велика, залил в галерею телефона), тайтл «Giant Rainier 26 inch Mountain Bike
RockShox», item specifics авто (Aluminum/Derailleur/Flat Bar), цена $100 Buy It Now, DELIVERY =
Pickup only (located 92688, no returns). Кнопка «List it» АКТИВНА (все обязательные поля есть).
⛔ НО при «List it» eBay потребовал РЕ-АУТЕНТИФИКАЦИЮ (пароль аккаунт eBay, step-up
security для sell-действия). Пароля eBay НЕТ в kola_secrets. НЕ угадываю/не выдумываю пароль
(риск лока аккаунта — стандинг «не выдумывать»). Draft СОХРАНЁН (draftId 5324728114710) — как
введёшь пароль / войдёшь на телефоне, жмёшь «List it» и велик публикуется. Всё остальное готово.
РЕШЕНИЕ: дай пароль eBay (или войди сам) — добью публикацию.

━━━ 4) FB GROUP-NAV — 2 КОРНЯ ПОЧИНЕНЫ (ec3b628 + fb7ee36), 3-й (landscape) вскрыт ━━━
• Корень nav_group_not_found: FB litho-рендерит результаты поиска → uidump ПУСТ → find_by_desc
  не видит группу. ТОТ ЖЕ КЛАСС, что невидимая Marketplace-нав. Фикс как в listing_check: uidump
  пуст → ГЛАЗА (OCR/vision) жмут «SoCal Electric» пикселями.
• 2-й баг (нашёл по пути): «уже на группе?» ложно срабатывал на ЭКРАНЕ ПОИСКА (имя группы там
  первым результатом). Теперь судим ТОЛЬКО по композеру (Write something). Фикс.
• ПОИСК НАХОДИТ ГРУППУ (скрин: «SoCal Electric & Hybrid D. — Your group» первым результатом).
• 3-й, ВСКРЫТЫЙ: FB-приложение поднимает поиск в LANDSCAPE, а kola_eyes мапит тап только в
  portrait → eyes-fallback промахивается в ландшафте. Отдельный класс (kola_eyes не landscape-
  aware / katana форсит ландшафт). fb_active имеет СВОЮ landscape-коррекцию тапов — плановый слот
  Ср 19:00 UTC пройдёт лучше моего ad-hoc kola_eyes-теста. Кандидат на добивку: eyes-fallback на
  landscape-корректный тап.

━━━ КОММИТЫ ХОДА (запушены) ━━━
• f4b4dd7 — ca yield-to-money (паритет с fin), доказан живьём
• ec3b628 — fb-group eyes-fallback на litho-пустой uidump
• fb7ee36 — fb-group «уже на группе» ложно на экране поиска
(ранее в сессии: f2c0b33+6797576 scanner+needrestart; предыдущие — warmup starvation и пр.)

ЖДУТ ТЕБЯ: пароль eBay (добить публикацию велика) · (опц.) добивка landscape для group eyes-fallback.
