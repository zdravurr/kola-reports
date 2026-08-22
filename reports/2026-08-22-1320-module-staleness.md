# module-staleness

_2026-08-22 13:20 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• kola-inbox-watcher.service — работает 65.3 ч, старт 2026-08-19 20:01
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/projects/sales/inbox_watcher.py
  НЕ ЗАГРУЖЕНО (2): lib/item_records.py, lib/reply_proof.py
  ЧИНИТЬ: systemctl --user restart kola-inbox-watcher.service

• pid 540415 (вне systemd) — работает 0.0 ч, старт 2026-08-22 13:19
  запуск: sudo -u botuser timeout 900 /usr/bin/python3 /home/botuser/.openclaw/workspace/.kola_state/tmp/_answer_mario.py
  НЕ ЗАГРУЖЕНО (1): .kola_state/tmp/_answer_mario.py
  ЧИНИТЬ: перезапустить pid 540415 вручную (юнита нет)

• pid 540416 (вне systemd) — работает 0.0 ч, старт 2026-08-22 13:19
  запуск: timeout 900 /usr/bin/python3 /home/botuser/.openclaw/workspace/.kola_state/tmp/_answer_mario.py
  НЕ ЗАГРУЖЕНО (1): .kola_state/tmp/_answer_mario.py
  ЧИНИТЬ: перезапустить pid 540416 вручную (юнита нет)

• pid 540418 (вне systemd) — работает 0.0 ч, старт 2026-08-22 13:19
  запуск: /usr/bin/python3 /home/botuser/.openclaw/workspace/.kola_state/tmp/_answer_mario.py
  НЕ ЗАГРУЖЕНО (1): .kola_state/tmp/_answer_mario.py
  ЧИНИТЬ: перезапустить pid 540418 вручную (юнита нет)
