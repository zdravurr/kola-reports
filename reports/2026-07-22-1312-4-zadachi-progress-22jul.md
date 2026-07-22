# 4-zadachi-progress-22jul

_2026-07-22 13:12 UTC_

---

🟢 ЧЕТЫРЕ ЗАДАЧИ БОССА — ПРОГРЕСС (2 готовы+доказаны, мультиварка OfferUp жива, остаток заблокирован warmup'ом)

Титан/Солана НЕ тронуты. Git чист+запушен. Скрины OfferUp-поста — по шагам (в scratchpad, приложу в финале).

━━━ ЗАДАЧА #2 — NEEDRESTART-BLACKLIST (option A) — ✅ ГОТОВО + ПРОВЕРЕНО ━━━
/etc/needrestart/conf.d/00-titan-mercury-norestart.conf (drop-in парсится ПОСЛЕ основного конфига
→ ДОБАВЛЯЕТ ключи в override_rc, не перезаписывает). override_rc=0 для titan.service,
mercury-sol.service, mercury-sol-optimizer-listener, optimizer-listener → needrestart их НЕ
рестартит при security-апдейте слинкованной либы (был рестарт ПОСРЕДИ сделки 21.07 из-за libsqlite3).
ПРОВЕРЕНО ЖИВЬЁМ: needrestart -b парсит чисто; perl-eval реального конфига — все 4 сервиса
matched=no-restart, nginx НЕ тронут (регекс точечный). Копия в repo: projects/infra/etc-configs/.

━━━ ЗАДАЧА #3 — СКАНЕР СИНТ-КЛИКОВ (A+B) — ✅ ГОТОВО + ПРОВЕРЕНО (зуб ЗЕЛЁНЫЙ) ━━━
A) _scan_synthetic теперь КЛАССИФИЦИРУЕТ каждый .click(): ДЕЙСТВИЕ площадке (submit/like/follow/
   renew/send — анти-фрод) vs НАВИГАЦИЯ/ЧТЕНИЕ вебвиджета (открыть виджет/вкладку/тред). Нарушение
   = только действие; чтения не в счёт. Неоднозначное → fail-closed на действие. Аннотация
   // cdp-read делает чтение аудируемым. Вердикт check_no_synthetic_clicks: было 26 «нарушений»,
   стало 0 ДЕЙСТВИЙ + 4 CDP-чтения = DONE.
B) 2 реальных клика → НАСТОЯЩЕЕ КАСАНИЕ:
   • cl_renew_bike_phone (АКТИВНЫЙ, крон): кнопки renew + email-login → smart_tap (CDP-rect→device,
     физический тап) + Chrome на переду. ЖИВЬЁМ: прогнал — навигация+чтение отработали, 0 синт-кликов,
     RENEW_RESULT=no-renew-option (велик только что бампался; сам тап renew сработает на eligible-цикле).
   • z_warmup_continuous (ДОРМАНТ, presence off): лайк → js_next_like_target()+like_on_topic()
     физтапом. Проверится при воскрешении presence (его собств. хедер это и требует).
   Снесены МЁРТВЫЕ one-off (cron=0, без ссылок): cl_post_bike.py, cl_post_bike_phone.py,
   kola_dm_brushoff.py (последний — тот же класс: мёртвый синт-DM-send; вышел за букву cl_post_bike*).

━━━ ЗАДАЧА #1 — МУЛЬТИВАРКА: OfferUp ✅ ЖИВА / Craigslist ⏳ ━━━
OfferUp — ВЫСТАВЛЕНА ЖИВЬЁМ через eyes+vtap, скрин-пруф КАЖДОГО шага (фото×3 → тайтл → описание →
цена $100 → категория Kitchen & Dining авто → Used → локация правлена Irvine→Rancho Santa Margarita
92688 → Post). Экран «Posted!» с фото-героем подтвердил публикацию. Записано в live_listings +
coverage. Товар: Zojirushi M. EL-CAC60, 6 Qt, $100, контакт Zina (номер в item_records).
Craigslist — ⏳ веб-флоу (post.craigslist.org через Chrome), НЕ начат: телефон занят.

━━━ ЗАДАЧА #4 — eBay ВЕЛИК — ⏳ ━━━
Не начат: телефон занят.

━━━ FB GROUP-NAV (фикс флаки, приказ Босса) — ✅ КОД / ⏳ live-тест ━━━
Корень nav_group_not_found НАЙДЕН: open_group() искал группу только через find_by_desc(uidump), а
FB рендерит результаты поиска через LITHO → uidump ПУСТ (ТОТ ЖЕ КЛАСС, что невидимая Marketplace-
навигация). Фикс как в listing_check: uidump пуст → ГЛАЗА (kola_eyes OCR/vision) жмут «SoCal Electric»
пикселями. Коммит ec3b628. Live-тест — на слоте Ср 19:00 UTC или когда телефон свободен.

━━━ ПОЧЕМУ ОСТАТОК ЗАБЛОКИРОВАН ━━━
Телефон держит плановый прогрев @zdravurr_ca (слот 13:00 UTC). ⚠️ ПОБОЧНАЯ НАХОДКА: zdravurr_ca_auto
НЕ имеет механизма yield-to-money (в отличие от zdravurr_auto) — держит экран весь сеанс (~до 13:30
UTC) и НЕ уступает даже money-path. Здоровый сеанс НЕ реапаю (стандинг «не убивать живые сессии» —
ban-риск). Жду освобождения (фоновый монитор), потом доделаю Craigslist + eBay + live-тест группы
и обновлю отчёт. (Асимметрия ca vs fin по yield — кандидат на отдельный фикс.)

━━━ КОММИТЫ ЭТОГО ХОДА (запушены) ━━━
• f2c0b33 + 6797576 — scanner A+B + needrestart (классификатор, конверсии, удаления, /etc-копия)
• ec3b628 — fb-group nav: eyes-fallback на litho-пустой uidump

ОСТАЛОСЬ ДОДЕЛАТЬ (телефон): мультиварка Craigslist · eBay велик · live-тест group-nav.
