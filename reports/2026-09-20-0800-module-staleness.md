# module-staleness

_2026-09-20 08:00 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• pid 3671455 (вне systemd) — работает 0.1 ч, старт 2026-09-20 07:52
  запуск: timeout 480 python3 /home/botuser/.openclaw/workspace/projects/dirigent/dirigent.py
  НЕ ЗАГРУЖЕНО (1): lib/source_day_budget.py
  ЧИНИТЬ: перезапустить pid 3671455 вручную (юнита нет)

• pid 3671456 (вне systemd) — работает 0.1 ч, старт 2026-09-20 07:52
  запуск: python3 /home/botuser/.openclaw/workspace/projects/dirigent/dirigent.py
  НЕ ЗАГРУЖЕНО (1): lib/source_day_budget.py
  ЧИНИТЬ: перезапустить pid 3671456 вручную (юнита нет)
