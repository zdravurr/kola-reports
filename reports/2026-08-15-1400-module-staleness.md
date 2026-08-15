# module-staleness

_2026-08-15 14:00 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• kola-inbox-watcher.service — работает 65.6 ч, старт 2026-08-12 20:22
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/sales/inbox_watcher.py
  НЕ ЗАГРУЖЕНО (10): lib/agent_capacity.py, lib/channel_policy.py, lib/item_records.py, lib/lead_alias.py, lib/name_match.py, lib/reply_proof.py, lib/screen_hold.py, lib/screen_priority.py …
  ЧИНИТЬ: systemctl --user restart kola-inbox-watcher.service
