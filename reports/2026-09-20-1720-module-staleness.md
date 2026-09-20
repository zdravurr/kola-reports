# module-staleness

_2026-09-20 17:20 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• openclaw-gateway.service — работает 0.0 ч, старт 2026-09-20 17:18
  запуск: /bin/bash -c source /home/botuser/.claude/shell-snapshots/snapshot-bash-1789924230232-2ump0b.sh 2>/dev/null || true && shopt -u ex
  НЕ ЗАГРУЖЕНО (1): ../workspace-worker3/_fred_hist.py
  ЧИНИТЬ: systemctl --user restart openclaw-gateway.service

• openclaw-gateway.service — работает 0.0 ч, старт 2026-09-20 17:18
  запуск: python3 /home/botuser/.openclaw/workspace-worker3/_fred_hist.py
  НЕ ЗАГРУЖЕНО (1): ../workspace-worker3/_fred_hist.py
  ЧИНИТЬ: systemctl --user restart openclaw-gateway.service
