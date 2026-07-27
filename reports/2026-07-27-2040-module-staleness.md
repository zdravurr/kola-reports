# module-staleness

_2026-07-27 20:40 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• kola-inbox-watcher.service — работает 1.3 ч, старт 2026-07-27 19:21
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/sales/inbox_watcher.py
  НЕ ЗАГРУЖЕНО (2): lib/agent_capacity.py, lib/channel_policy.py
  ЧИНИТЬ: systemctl --user restart kola-inbox-watcher.service

• kola-bridge.service — работает 1.3 ч, старт 2026-07-27 19:21
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/scripts/kola-bridge/server.py
  НЕ ЗАГРУЖЕНО (2): lib/agent_capacity.py, lib/channel_policy.py
  ЧИНИТЬ: systemctl restart kola-bridge.service
