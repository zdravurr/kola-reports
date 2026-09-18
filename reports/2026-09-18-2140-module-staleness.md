# module-staleness

_2026-09-18 21:40 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• cron.service — работает 0.3 ч, старт 2026-09-18 21:20
  запуск: /usr/bin/timeout 2700 /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/fb_social/fb_zdravurrrr_warmup.py
  НЕ ЗАГРУЖЕНО (1): lib/ogon_quota.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-09-18 21:20
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/fb_social/fb_zdravurrrr_warmup.py
  НЕ ЗАГРУЖЕНО (1): lib/ogon_quota.py
  ЧИНИТЬ: systemctl restart cron.service
