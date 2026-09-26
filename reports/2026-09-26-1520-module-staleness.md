# module-staleness

_2026-09-26 15:20 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• pid 884945 (вне systemd) — работает 0.5 ч, старт 2026-09-26 14:50
  запуск: /bin/bash -c /bin/bash /home/botuser/.openclaw/workspace/projects/social_x/x_bridge_ensure.sh >> /home/botuser/.openclaw/workspace
  НЕ ЗАГРУЖЕНО (2): lib/x_comment_supply.py, projects/social_x/zdravurr_ca_auto.py
  ЧИНИТЬ: перезапустить pid 884945 вручную (юнита нет)
