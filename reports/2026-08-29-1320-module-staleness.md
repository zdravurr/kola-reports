# module-staleness

_2026-08-29 13:20 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• cron.service — работает 0.3 ч, старт 2026-08-29 13:00
  запуск: /bin/sh -c /home/botuser/.openclaw/workspace/scripts/run_guarded.sh xwarmup_ca /bin/bash -c '/bin/bash /home/botuser/.openclaw/wor
  НЕ ЗАГРУЖЕНО (1): lib/tech_queue.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-08-29 13:00
  запуск: /bin/bash -c /bin/bash /home/botuser/.openclaw/workspace/projects/social_x/x_bridge_ensure.sh >> /home/botuser/.openclaw/workspace
  НЕ ЗАГРУЖЕНО (1): lib/tech_queue.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-08-29 13:00
  запуск: /usr/bin/timeout 2400 /usr/bin/python3 -u /home/botuser/.openclaw/workspace/projects/social_x/zdravurr_ca_auto.py session 3
  НЕ ЗАГРУЖЕНО (1): lib/tech_queue.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-08-29 13:00
  запуск: /usr/bin/python3 -u /home/botuser/.openclaw/workspace/projects/social_x/zdravurr_ca_auto.py session 3
  НЕ ЗАГРУЖЕНО (1): lib/tech_queue.py
  ЧИНИТЬ: systemctl restart cron.service

• pid 2072620 (вне systemd) — работает 0.2 ч, старт 2026-08-29 13:09
  запуск: sudo -u botuser env KOLA_TAB_WHO=listing_delist KOLA_PARENT_TASK=88cf479e63cc setsid nohup python3 /mnt/volume_nyc1_1780480650620/
  НЕ ЗАГРУЖЕНО (1): lib/listing_capabilities.py
  ЧИНИТЬ: перезапустить pid 2072620 вручную (юнита нет)

• pid 2072622 (вне systemd) — работает 0.2 ч, старт 2026-08-29 13:09
  запуск: python3 /mnt/volume_nyc1_1780480650620/home/botuser/.openclaw/workspace/scripts/listing_job.py /mnt/volume_nyc1_1780480650620/home
  НЕ ЗАГРУЖЕНО (1): lib/listing_capabilities.py
  ЧИНИТЬ: перезапустить pid 2072622 вручную (юнита нет)
