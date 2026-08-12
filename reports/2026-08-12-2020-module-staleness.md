# module-staleness

_2026-08-12 20:20 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• cron.service — работает 0.3 ч, старт 2026-08-12 20:00
  запуск: /bin/sh -c /home/botuser/.openclaw/workspace/scripts/run_guarded.sh xwarmup_ca /bin/bash -c '/bin/bash /home/botuser/.openclaw/wor
  НЕ ЗАГРУЖЕНО (1): lib/agent_capacity.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-08-12 20:00
  запуск: /bin/bash -c /bin/bash /home/botuser/.openclaw/workspace/projects/social_x/x_bridge_ensure.sh >> /home/botuser/.openclaw/workspace
  НЕ ЗАГРУЖЕНО (1): lib/agent_capacity.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-08-12 20:00
  запуск: /usr/bin/timeout 1800 /usr/bin/python3 -u /home/botuser/.openclaw/workspace/projects/social_x/zdravurr_ca_auto.py session 3
  НЕ ЗАГРУЖЕНО (1): lib/agent_capacity.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.3 ч, старт 2026-08-12 20:00
  запуск: /usr/bin/python3 -u /home/botuser/.openclaw/workspace/projects/social_x/zdravurr_ca_auto.py session 3
  НЕ ЗАГРУЖЕНО (1): lib/agent_capacity.py
  ЧИНИТЬ: systemctl restart cron.service

• kola-inbox-watcher.service — работает 0.3 ч, старт 2026-08-12 20:02
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/sales/inbox_watcher.py
  НЕ ЗАГРУЖЕНО (1): lib/agent_capacity.py
  ЧИНИТЬ: systemctl --user restart kola-inbox-watcher.service
