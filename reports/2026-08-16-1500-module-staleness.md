# module-staleness

_2026-08-16 15:00 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• kola-inbox-watcher.service — работает 24.9 ч, старт 2026-08-15 14:06
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/sales/inbox_watcher.py
  НЕ ЗАГРУЖЕНО (2): lib/item_records.py, lib/report_outbox.py
  ЧИНИТЬ: systemctl --user restart kola-inbox-watcher.service
