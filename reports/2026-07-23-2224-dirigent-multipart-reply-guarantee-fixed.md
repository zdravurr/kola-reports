# dirigent-multipart-reply-guarantee-fixed

_2026-07-23 22:24 UTC_

---

🛠️ СИСТЕМНЫЙ БАГ ЗАКРЫТ В КОДЕ — multipart-ветка больше не «понял и растворилась». Пруф: тест + дифф + коммит.

_(Публичный отчёт: реальный телефон владельца НЕ приводится; в тесте — заведомо тестовый placeholder TEST-555-0000.)_

━━ ЧТО БЫЛО СЛОМАНО ━━
Разговорно сформулированная просьба («отпишись Ларри, дай номер владельца») попадала в _looks_multipart → _handle_multipart. Мозг возвращал дружелюбный ответ-переспрос («понял, нужен номер») и НИ ОДНОЙ worker_reply-задачи. Итог:
• в worker_tasks НИЧЕГО не ложилось → dirigent_worker_guarantee (он охраняет ТОЛЬКО задачи с action=reply) не видел ничего → тишина-по-результату;
• ответ ПЕРЕСПРАШИВАЛ Босса номером, который УЖЕ лежит в owner_phones.json.
Единичный путь worker_reply задачу ставил всегда — дыра была ИМЕННО в multipart-ветке.

━━ ЧТО ИСПРАВЛЕНО (commit 91dda1e, kola-workspace-backup, запушено) ━━
1) lib/dirigent_commands.py, _handle_multipart:
   • отслеживаем, поставил ли разбор reply-задачу;
   • если Босс просит ответить покупателю, а её нет — СТАВИМ сами (action=reply) → её видит сторож и честно эскалирует за SLA;
   • резолвим номер владельца из реестра и кладём в arg задачи; ответ больше НЕ переспрашивает Босса и не обещает ложно.
2) НОВЫЙ lib/owner_registry.py — resolve_from_text(): item_records → иначе пересечение токенов ключа; читает owner_phones.json, НИКОГДА не выдумывает номер (None, если не нашёл).
3) НОВЫЙ tests/test_multipart_reply_guarantee.py — герметичный тест (temp KOLA_STATE, застабены brain/channel/rules; прод и реальный Telegram не трогаются).

━━ КЛЮЧЕВОЙ ДИФФ (lib/dirigent_commands.py) ━━
    reply_task_made = False
    for a in actions:
        ai = a if isinstance(a, dict) else {"intent": str(a)}
        if ai.get("intent") == "worker_reply":
            reply_task_made = True      # мозг сам поставил — не дублируем
        ... execute(ai) ...
    # 3b) ГАРАНТИЯ ИСПОЛНИМОСТИ:
    if _REPLY.search(text or "") and not reply_task_made and not (initiative and initiative.get("sent")):
        arg = (text or "").strip()
        resolved = owner_registry.resolve_from_text(text)   # номер из реестра, не переспрашиваем
        if resolved:
            arg += f"\n[owner-registry {resolved['key']}: {resolved['phone']}]"
        guaranteed_tid = dc.add_worker_task("senya", "reply", arg)   # action=reply → сторож видит
        did_any = True
(полный дифф: 3 файла, +303/-3; см. git show 91dda1e)

━━ РЕАЛЬНЫЙ ВЫВОД ТЕСТА (EXIT=0, запуск от botuser) ━━
[1] intent = multipart, did=True, guaranteed_reply_task=wt_..., owner_resolved=true
[1] worker_tasks (senya):
    { "id":"wt_...", "worker":"senya", "action":"reply", "status":"open",
      "arg":"Да, отпишись Ларри по велику Giant Rainier … [owner-registry bike_giant_rainier: TEST-555-0000]" }
[1] reply = «✍️ Принял: отвечу покупателю. Поставил задачу wt_… в очередь Сени. Номер владельца
            взял из реестра (bike_giant_rainier) — тебя не переспрашиваю. …»
[2] overdue сразу после создания: 0 (в окне SLA — сторож справедливо молчит)
[3] overdue после старения на 20 мин: 1;  tick fired: ['wt_...:...']  (РОВНО одна эскалация)
[3] реальный текст эскалации в канал: «⏳ ЗАДАЧА ИЗ TELEGRAM НЕ ИСПОЛНЕНА — докладываю честно…
     Ты просил (≈20 мин назад): «…отпишись Ларри по велику Giant Rainier…» … держу открытой (wt_...)»
[4] второй tick (дедуп): []  (повторно не орёт)
[5] overdue после mark_done: 0  (исполнено → снято)
✅ ВСЕ ПРОВЕРКИ ПРОШЛИ.

━━ ЧТО ИМЕННО ЭТО ЗАКРЫВАЕТ ━━
Ровно инцидент с Ларри: теперь любая multipart-просьба «ответь покупателю» (а) резолвит нужные данные из реестра вместо переспроса Босса и (б) ВСЕГДА создаёт трекаемую reply-задачу, которую сторож видит и честно эскалирует, если её не исполнят за SLA. Прошлый отчёт заявлял «тишина невозможна» преждевременно — теперь это подтверждено тестом на самом уязвимом пути.

Границы честно: тест герметичный (симуляция разбора мозга застаблена — проверяем НАШУ гарантию, а не сам Opus-разбор); резолв номера best-effort (item_records + токены ключа), при неоднозначности вернёт None, но задача всё равно создаётся и сторож её видит. Titan/Solana не тронуты во всём заходе.
