# module-staleness

_2026-09-17 02:00 UTC_

---

🔴 РАЗВЁРНУТО НЕ ВСЁ: демон работает на СТАРОМ коде библиотеки.

Фикс, лежащий на диске, но не загруженный в процесс, НЕ ДЕЙСТВУЕТ. Так 27.07 утекло подтверждение ответа покупателю: ⛔-блок канала был добавлен в agent_capacity.wake() 26.07 11:14, а демон детекции работал с 24.07 23:43 и этого кода никогда не видел.

• pid 2844223 (вне systemd) — работает 0.0 ч, старт 2026-09-17 01:58
  запуск: /bin/bash -c source /root/.claude/shell-snapshots/snapshot-bash-1789588889670-qvgx3f.sh 2>/dev/null || true && shopt -u extglob 2>
  НЕ ЗАГРУЖЕНО (1): ../../../../tmp/fbdel.py
  ЧИНИТЬ: перезапустить pid 2844223 вручную (юнита нет)

• pid 2844227 (вне systemd) — работает 0.0 ч, старт 2026-09-17 01:58
  запуск: sudo -u botuser env -u KOLA_CONTRACT PYTHONPATH=/tmp:/home/botuser/.openclaw/workspace/lib timeout 800 python3 /tmp/fbdel.py
  НЕ ЗАГРУЖЕНО (1): ../../../../tmp/fbdel.py
  ЧИНИТЬ: перезапустить pid 2844227 вручную (юнита нет)
