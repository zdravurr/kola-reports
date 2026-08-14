# module-staleness

_2026-08-14 00:00 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• kola-inbox-watcher.service — работает 27.6 ч, старт 2026-08-12 20:22
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/sales/inbox_watcher.py
  НЕ ЗАГРУЖЕНО (9): lib/agent_capacity.py, lib/channel_policy.py, lib/lead_alias.py, lib/name_match.py, lib/reply_proof.py, lib/screen_hold.py, lib/screen_priority.py, lib/x_tab_guard.py …
  ЧИНИТЬ: systemctl --user restart kola-inbox-watcher.service

• cron.service — работает 0.5 ч, старт 2026-08-13 23:30
  запуск: /bin/sh -c /home/botuser/.openclaw/workspace/scripts/run_guarded.sh xwarmup_ca /bin/bash -c '/bin/bash /home/botuser/.openclaw/wor
  НЕ ЗАГРУЖЕНО (3): lib/agent_capacity.py, lib/screen_hold.py, lib/screen_priority.py
  ЧИНИТЬ: systemctl restart cron.service

• cron.service — работает 0.5 ч, старт 2026-08-13 23:30
  запуск: /bin/sh -c /home/botuser/.openclaw/workspace/scripts/run_guarded.sh fbwarmup /usr/bin/python3 /home/botuser/.openclaw/workspace/pr
  НЕ ЗАГРУЖЕНО (2): lib/screen_hold.py, lib/screen_priority.py
  ЧИНИТЬ: systemctl restart cron.service

• pid 1773114 (вне systemd) — работает 0.5 ч, старт 2026-08-13 23:30
  запуск: /bin/bash -c /bin/bash /home/botuser/.openclaw/workspace/projects/social_x/x_bridge_ensure.sh >> /home/botuser/.openclaw/workspace
  НЕ ЗАГРУЖЕНО (3): lib/agent_capacity.py, lib/screen_hold.py, lib/screen_priority.py
  ЧИНИТЬ: перезапустить pid 1773114 вручную (юнита нет)

• cron.service — работает 0.5 ч, старт 2026-08-13 23:30
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/fb_social/fb_zdravurrrr_warmup.py
  НЕ ЗАГРУЖЕНО (2): lib/screen_hold.py, lib/screen_priority.py
  ЧИНИТЬ: systemctl restart cron.service
