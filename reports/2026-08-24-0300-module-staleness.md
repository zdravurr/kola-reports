# module-staleness

_2026-08-24 03:00 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• kola-inbox-watcher.service — работает 103.0 ч, старт 2026-08-19 20:01
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/sales/inbox_watcher.py
  НЕ ЗАГРУЖЕНО (32): lib/agent_capacity.py, lib/attempt_ledger.py, lib/boss_command.py, lib/claude_auth_guard.py, lib/claude_cli.py, lib/crm.py, lib/dirigent_control.py, lib/eyes.py …
  ЧИНИТЬ: systemctl --user restart kola-inbox-watcher.service
