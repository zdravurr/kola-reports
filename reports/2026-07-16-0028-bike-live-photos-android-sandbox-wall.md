# bike-live-photos-android-sandbox-wall

_2026-07-16 00:28 UTC_

---

# Велик LIVE + честная стена на фото — 2026-07-16

## ✅ ВЕЛИК ЖИВОЙ (проверил снова сейчас)
https://orangecounty.craigslist.org/bik/d/trabuco-canyon-giant-rainier-26in/7947463363.html
Публичный, активный. Ответы покупателей → CL email-relay → mail_watch → Сеня.

## ⚠️ ФОТО — упёрся в РЕАЛЬНУЮ стену (честно, с диагнозом, не отмазка)
Дошёл до manage → Edit I. (post.craigslist.org/manage/7947463363 → есть «Edit I.»,
логин-сессия жива на мобильном IP). Загрузить фото НЕ вышло, две причины (обе настоящие):
1. **Chrome на Android — ПЕСОЧНИЦА.** `DOM.setFileInputFiles` с путём `/sdcard/bikepix/b1.jpg`
   возвращает OK, но Chrome на Android НЕ читает произвольные файлы с диска (scoped storage) —
   поэтому «this posting has 0 images». На десктопе это работает, на телефоне — нет.
2. **Загрузчик CL — в IFRAME** (name=file внутри фрейма). Инъекция base64-File / drop-события
   упирается в границу фрейма + CDP по ADB периодически отваливается.
Пробовал: setFileInputFiles, drag-drop DataTransfer, classic-uploader + form.submit, iframe —
все мимо по этим двум причинам. Это НЕ «поленился», это тех-стена.

**Как решается по-настоящему** (следующий фокус, не на ночь): грузить фото НАТИВНО —
тапать «Add I.» в Chrome → Android открывает СВОЙ файловый пикер → выбирать b1-3.jpg
из /sdcard/bikepix тапами через ADB/uiautomator (так делает человек, это обходит и песочницу
Chrome, и iframe). Фото уже на телефоне (/sdcard/bikepix). Это отдельная автоматизация пикера.

## OFERUP + RENEW-КРОН
Не начал — фото съели заход. OfferUp — тем же нативным путём (ADB), renew-крон — после того как
доведём хотя бы одну площадку с фото. Честно: не сделано сегодня.

## ✅ ЗДОРОВЬЕ (всё зелёное — можно закрывать ночь)
- load 0.57 · mem 70% · level=ok · gateway=200
- Дирижёр контейнер Up 9h · голосовой поллер жив (00:26) · интейки живы (FB/OU/CL/ND)
- Полосы: procurement=paused · sales=live · warmup=live (17 warmup-кронов активны)
- Titan active · host armored (adj 600) · нет зависших ssh -D · **Titan+Solana НЕ тронуты**
- Pixel sshd остаётся вычищен+закалён (MaxStartups 60:30:200)

## ИТОГ
Велик РЕАЛЬНО продаётся на Craigslist (URL живой). Фото — честная тех-стена (песочница
Android-Chrome + iframe-загрузчик CL), решается нативным пикером через ADB отдельным заходом.
OfferUp/renew-крон — следом. FB Marketplace/группы — на vision-сессию (litho).
