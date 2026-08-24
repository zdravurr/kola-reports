# ПОЛНАЯ ОСТАНОВКА — кроме прогрева (Огонь) и Титана/Соланы

**2026-08-24 11:30 UTC** · команда Босса: «STOP EVERYTHING except warmup (Ogon) and Titan/Solana».
Ничего не чинил, старый контекст не читал. Только остановка, проверка, доклад.

---

## 1. ЧТО СЕЙЧАС РАБОТАЕТ (проверено `ps` / `systemctl` / `docker`)

### Титан / Солана — НЕ ТРОНУТЫ, все живы
| Сервис | Статус |
|---|---|
| `titan.service` (BTC/USDT) | active |
| `mercury-sol.service` (SOL/USDT, ЖИВЫЕ ДЕНЬГИ) | active |
| `optimizer-listener.service` (Титан) | active, pid 2538053, 18 сут |
| `mercury-sol-optimizer-listener.service` | active, pid 3521920, 15 сут |
| `gemini_bridge.service` | active, pid 3647921, 27 сут |
| gunicorn master+worker (mercury-sol) | active, pid 3640449 / 3640686 |

Все крон-строки Титана и SOL остались активными **без единого изменения**:
regime watchers (bull / downtrend / uptrend / flat-high-adx / chop-short / volfloor),
`prior_move_logger`, `daily_trend_cohort_sensor`, `silence_digest` (оба),
`naked_alert_resolver`, `mercury_sol_30trade_reminder`.

### Прогрев / Огонь — НЕ ТРОНУТ
Крон-строки живы: `xwarmup` ×3 (10:00 / 16:00 / 22:00 UTC), `xwarmup_ca` ×3 (13:00 / 20:00 / 23:30),
`fbwarmup` ×4 (00:30 / 11:30 / 17:30 / 23:30), `evwarmup` (19:00),
`growth_collect` (09:00), `ogon_supervise` ×2 (01:00 / 09:20), `ogon_quota` (ежечасно).

Телефонная инфраструктура, без которой прогрев слепнет, **оставлена намеренно**:
`pixel_keepalive`, `pixel_mux_keepalive`, `portrait_lock`, `cdp_bridge_guard`,
`adb_server_guard` (крон рута), `warmup_health.py watchdog` (крон рута — сторож самого прогрева),
`kola-bridge.service` (pid 273526).

### Эта сессия
`claude` pid **1182191** — единственный процесс Claude на машине.

### Оставлено сознательно (доложить отдельно, см. §4)
`openclaw-gateway.service` pid 1072183 — канал Босса в Telegram.

---

## 2. ЧТО УБИТО

| Что | PID | Чем было |
|---|---|---|
| Фоновая сессия Claude (`--resume … --permission-mode auto`, сессия `b5b0ad3b`) | 1177976 + 1177990 / 1177995 / 1178010 / 1178015 | TERM, затем KILL по двум bg-pty-host |
| `listing_job.py` (`20260824T111814Z_mark_sold.json`) | 1180775 | TERM |
| `claude -p` оператор телефона — «пометить проданным Giant Rainier 26in Mountain Bike / craigslist» | 1182158 | умер вместе с родителем |
| `dirigent_voice.py poll 20` | 1182284 / 1182297 / 1182302 / 1182303 | умер вместе с кроном |
| `inbox_watcher.py` | 1175200 | остановлен вместе с сервисом |
| Контейнер `dirigent` (оркестратор, `loop.sh`, pid 1758588, жил 34 сут) | — | `restart=no` + `docker stop` → Exited (137) |
| Контейнеры `claude-agent-1/2/3` (рабочие ланы) | — | `restart=no` + `docker stop` → Exited (143) |

`ts-dirigent` (tailscale-сайдкар) оставлен: это только сеть, сессий не порождает.

**Сервис остановлен и снят с автозапуска:** `kola-inbox-watcher.service` (botuser, user-systemd) —
`stop` + `disable`, симлинк из `default.target.wants` удалён.

---

## 3. ЧТО ВЫКЛЮЧЕНО В КРОНЕ

Строки не удалены, а помечены префиксом `#STOPPED24AUG` — включаются обратно одним `sed`.
Бэкапы обоих крон-таблиц: `/root/.stopall_24aug/*.crontab.bak`.

### ⚠️ ПОРЯДОК ИМЕЛ ЗНАЧЕНИЕ: сначала обезоружены воскресители
Три сторожа в кроне **рута** вернули бы выключенное назад в строй в течение 5–10 минут.
Погашены первыми:
- `cron_guard.py guard` (*/10) — воскрешал `fb_inbox_sweep`, `inbox_sweep`, `mail_watch`,
  `buyer_watchdog`, `post_watchdog`, `commit_watchdog`, `report_outbox`, `dirigent_voice`;
- `dirigent_container_watch.sh` (*/5) — поднимал контейнер `dirigent` обратно;
- `turn_report_watchdog.py` (*/10).

Итого рут: **3 строки выключено**, 21 активна (все — Титан/SOL/бэкап/диск/телефон).

### botuser: выключено 44 строки, осталось 31
Названные Боссом поимённо:
`tech_queue.pump` · `worker_task_runner.py` · `answer_guarantee.py` · `main_liveness.py` ·
`self_improve_daily.py`.

Детекция и маршрутизация лидов/покупателей:
`mail_watch.py` · `mail_labeler.py` · `fb_inbox_sweep.py` · `cl_chat_watch.py` ·
`node_notif_watch.py` · `buyer_watchdog.py` · `lead_guarantee.py` · `arrival_watch.py` ·
`detector_liveness.py` · `coverage_eyes_sweep.py`.

Сторожа и гарантии:
`commit_watchdog.py` · `post_watchdog.py` · `fault_realert.py` · `promise_tracker.py` ·
`delegation_guarantee.py` · `dirigent_worker_guarantee.py` · `boss_intake_guarantee.py` ·
`boss_command_guarantee.py` · `wake_delivery_guard.py` · `module_staleness.py` ·
`report_outbox.py watchdog` · `hold_deadline.py` · `task_dedup.py sweep` · `agent_capacity.py reap`.

Дирижёр и листинги:
`dirigent_voice.py` · `dirigent_enforce.py` · `listing_supervisor.py` · `listing_coverage.py` ·
`cl_renew_bike_phone.py` (2 строки) · `pif_expiry.py`.

Аудиты и прочее:
`system_director.py loop` · `seam_audit.py` · `path_prober.py` · `gateway_log.py` ·
`daily_self_audit.py` · `launcher_path_audit.py` · `daytime_exec_nudge.py` · `kola_boot_status.py`.

### Оставлено активным у botuser (и почему)
Прогрев/Огонь (см. §1) · телефонный транспорт · `report_outbox.py drain` (доставка отчётов
Боссу — не сторож, ничего не порождает) · `oauth_refresh` · `claude_auth_guard` ·
`overload_guard` · `openclaw_config_sync` · `disk_janitor` · `backup_push` · `media-cleanup` ·
`disk_autoclean`.

---

## 4. ЧЕСТНО: ЧТО ОСТАЛОСЬ СТОЯТЬ И ПОЧЕМУ

**`openclaw-gateway.service` (pid 1072183) НЕ погашен.** Это не сессия и не крон — это канал,
по которому Босс говорит с системой из Telegram. Погасив его, я отрезал бы Босса от машины.

Что это значит на практике: **сама по себе система больше ничего не начнёт** — всё, что
кормило гейтвей задачами, выключено (`dirigent_voice`, `worker_task_runner`, `tech_queue.pump`,
`boss_intake_guarantee`, все детекторы). Но если Босс **сам** напишет команду в Telegram,
гейтвей теоретически может поднять сессию под неё. Гасить его — одно слово Босса.

---

## 5. ИТОГ

Работает: **прогрев (Огонь) + Титан/Солана + эта сессия** (+ гейтвей как канал Босса,
+ телефонный транспорт под прогрев).

Убито: 1 фоновая сессия Claude, 1 телефонный `claude -p`, 4 контейнера, 3 процесса продаж,
1 user-сервис.
Выключено: **47 крон-строк** (3 рут + 44 botuser), включая три воскресителя — первыми.
Титана и Солану **не трогал ни одним движением**.
