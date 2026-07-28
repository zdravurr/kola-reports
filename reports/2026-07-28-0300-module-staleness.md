# module-staleness

_2026-07-28 03:00 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• kola-bridge.service — работает 6.3 ч, старт 2026-07-27 20:44
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/scripts/kola-bridge/server.py
  НЕ ЗАГРУЖЕНО (6): lib/capability_audit.py, lib/lead_alias.py, lib/lead_router.py, lib/listing_supervisor.py, lib/reader_sanity.py, lib/reply_proof.py
  ЧИНИТЬ: systemctl restart kola-bridge.service

• kola-inbox-watcher.service — работает 4.1 ч, старт 2026-07-27 22:55
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/sales/inbox_watcher.py
  НЕ ЗАГРУЖЕНО (6): lib/capability_audit.py, lib/lead_alias.py, lib/lead_router.py, lib/listing_supervisor.py, lib/reader_sanity.py, lib/reply_proof.py
  ЧИНИТЬ: systemctl --user restart kola-inbox-watcher.service
