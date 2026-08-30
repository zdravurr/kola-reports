# module-staleness

_2026-08-30 22:20 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• cron.service — работает 0.3 ч, старт 2026-08-30 22:00
  запуск: /bin/sh -c /home/botuser/.openclaw/workspace/scripts/run_guarded.sh xwarmup /bin/bash -c '/bin/bash /home/botuser/.openclaw/worksp
  НЕ ЗАГРУЖЕНО (3): lib/fault_realert.py, lib/x_comment_supply.py, projects/social_x/zdravurr_auto.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-08-30 22:00
  запуск: /bin/bash -c /bin/bash /home/botuser/.openclaw/workspace/projects/social_x/x_bridge_ensure.sh >> /home/botuser/.openclaw/workspace
  НЕ ЗАГРУЖЕНО (3): lib/fault_realert.py, lib/x_comment_supply.py, projects/social_x/zdravurr_auto.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-08-30 22:00
  запуск: /usr/bin/timeout 3600 /usr/bin/python3 -u /home/botuser/.openclaw/workspace/projects/social_x/zdravurr_auto.py session 3 img nopos
  НЕ ЗАГРУЖЕНО (3): lib/fault_realert.py, lib/x_comment_supply.py, projects/social_x/zdravurr_auto.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-08-30 22:00
  запуск: /usr/bin/python3 -u /home/botuser/.openclaw/workspace/projects/social_x/zdravurr_auto.py session 3 img nopost
  НЕ ЗАГРУЖЕНО (3): lib/fault_realert.py, lib/x_comment_supply.py, projects/social_x/zdravurr_auto.py
  ЧИНИТЬ: systemctl restart cron.service
