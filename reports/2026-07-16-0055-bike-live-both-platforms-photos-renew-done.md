# bike-live-both-platforms-photos-renew-done

_2026-07-16 00:55 UTC_

---

# ✅ ЗАКРЫЛ ВСЁ — фото + OfferUp + renew-крон + надзор (2026-07-16)

Все три пункта СДЕЛАНЫ живьём, нативно, без фейка.

## 1. ✅ ФОТО НА CL-ВЕЛИКЕ — LIVE, проверено
Через НАТИВНЫЙ Android-пикер (тап «Choose F.» → системный фото-пикер Android → выбор фото
велика через ADB-тапы). Обошёл и песочницу Chrome, и iframe CL — ровно как я и говорил.
2 фото ВЕЛИКА на публичном листинге (проверил: images.craigslist.org/00505_dQA6liBWmQy +
00c0c_2Q7chsEe0JS). Листинг: https://orangecounty.craigslist.org/bik/d/trabuco-canyon-giant-rainier-26in/7947463363.html

## 2. ✅ OFFERUP — ВЕЛИК ВЫСТАВЛЕН, LIVE
Нативный ADB-флоу приложения: Post → 3 фото (полный велик + 2 форка) → заголовок «Giant Rainier
26in Mountain Bike - Disc Brakes RockShox» → цена $100 → категория Bikes & Cycling (авто) →
состояние Used → локация Irvine CA → Post. Подтверждено: My Listings показывает велик живьём с
фото + сразу вылезла пост-публикационная «Promote» — она бывает ТОЛЬКО после успешной публикации.
(OfferUp — app-центричный, публичного URL как у CL нет; пруф = My Listings + Promote.)

## 3. ✅ RENEW-КРОН + НАДЗОР ДИРИЖЁРА
- **lib/listing_supervisor.py** (крон ежедневно 09:15): server-side curl проверяет, что CL-листинг
  ЖИВ (не expired/deleted), алерт Боссу если упал. ПРОВЕРЕНО живьём: «CL bike: live (ok)».
- **scripts/cl_renew_bike_phone.py** (крон каждые 3 дня 10:20): phone-native renew/подъём CL-листинга
  (если сессия протухла — авто-логин по one-time link с gmail). ЧЕСТНО: CL даёт renew только через
  ~48ч после публикации, поэтому СЕГОДНЯ проверить нельзя — крон сработает по каденции.
- Каденция: CL renew раз в 3 дня (держит вверху); надзор ежедневно.

## ✅ ЗДОРОВЬЕ — ЗЕЛЁНОЕ
load 0.8 · mem 68% · gateway 200 · Дирижёр Up 9h · голосовой поллер жив · интейки живы
(FB/OfferUp/CL/Nextdoor) · полосы procurement=paused · sales=live · warmup=live (17 warmup-кронов) ·
Titan active · host armored · Pixel sshd вычищен+закалён · git CLEAN · **Titan+Solana НЕ тронуты**.

## ИТОГ
Велик РЕАЛЬНО продаётся на ДВУХ площадках с фото: **Craigslist** (URL живой, 2 фото) +
**OfferUp** (live, 3 фото). Автоматика держит их наверху (renew) и следит (supervisor).
FB Marketplace + группы остаются на vision-сессию (litho). Всё закоммичено, всё зелёное.
