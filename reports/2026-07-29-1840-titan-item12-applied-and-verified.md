# ПУНКТ 12 ПРИМЕНЁН · МАРШРУТИЗАЦИЯ МИГРИРОВАНА · ВТОРОЙ БОЕВОЙ ГЕЙТ ПОСТАВЛЕН
**2026-07-29 18:40 UTC** · коммит `0833f42` · база `5f054b7` · рестарт **18:34:24 UTC**

> **ИТОГ.** Применено, закоммичено, запушено, перезапущено. Баннер: **🧪 PAPER, оба флага False.**
> Ошибок 0. Рантайм = коммит по хешу, **6/6 MATCH**. `stop_order_id` NULL на всех 59 строках.
> **Новый гейт проверен исполнением: оба флага True → отказ, exit 3.**

---

## 1. НОВЫЙ ГЕЙТ — ТВОЁ ДОБАВЛЕНИЕ, И ОНО ЗАКРЫВАЕТ ИМЕННО ТО, ЧТО ОТКРЫЛ ЭТОТ ЖЕ КОММИТ

`ROUTING_MIGRATED_TO_ADAPTER = True` разоружает старый отказ. Значит с этого коммита переключение
двух флагов **подняло бы бота** — в состояние, про которое §6 прошлого отчёта уже доказал, что оно
сломано: первый же выход по стопу оставит строку открытой навсегда, P&L не запишется, уникальный
индекс заблокирует все следующие входы. **Отказ, который выглядит как успех.**

`PASSIVE_FILL_RECONCILE_EXISTS = False` + `passive_fill_warning()` в `assert_startup_mode()`.

Проверено исполнением на реальном конфиге:
```
БУМАГА:            routing_warning()='' · passive_fill_warning()=''  -> стартует штатно
ОБА ФЛАГА TRUE:    routing_warning()=''  (мигрировано, старый гейт молчит — правильно)
                   [ORDER-MODE] 🛑 REFUSING TO START — UNSAFE CONFIGURATION
                   CRITICAL: no passive-fill reconciliation for virtual_positions
                             (design item 13 is NOT built).
                   ... THE BOT WOULD STALL AFTER ITS FIRST TRADE AND LOOK SUCCESSFUL.
                   Fix: implement design item 13 ... Do NOT set the flag by hand —
                        it asserts that the reconciliation EXISTS.
                   exit 3                                          EXIT_CODE=3
```
Строка «Fix» намеренно запрещает выставлять флаг руками: он **утверждает факт**, а не разрешение.
Дисциплина ровно та же, что у маршрутного маркера: гейт снимает **сам коммит пункта 13**.

---

## 2. ПОДТВЕРЖДЕНО ИСПОЛНЕНИЕМ ПОСЛЕ РЕСТАРТА

**Баннер из живого журнала**
```
Jul 29 18:34:28 titan[4161682]: [ORDER-MODE] 🧪 PAPER — simulated fills only —
                                no order can be sent (LIVE_TRADING_ENABLED=False)
Jul 29 18:34:28 titan[4161682]: [ORDER-MODE]   LIVE_TRADING_ENABLED = False
Jul 29 18:34:28 titan[4161682]: [ORDER-MODE]   ORDER_ADAPTER_LIVE   = False
[RECONCILE] starting -> done · breakeven_worker started · virtual_trader worker started
traceback/error/exception с рестарта: 0
```

**Рантайм = коммит, по ХЕШУ**
```
config.py · order_adapter.py · virtual_trader.py · breakeven_worker.py · main.py · gunicorn.conf.py
                                                                       6/6 MATCH
worktree clean: YES · HEAD = origin/main = 0833f42
master 4161682 (18:34:24) · worker 4161701 форкнут 18:34:33 — ПОСЛЕ рестарта
```

**Предикаты**
```
engine_owns_position() = True    (движок управляет)
is_active()            = True    (заливки симулируются — СМЫСЛ НЕ ИЗМЕНЁН)
orders_are_real()      = False
```

**`breakeven_worker` стоит**
```
_poll_once -> 0   мок падал бы на fetch_positions / create_order / cancel_order —
                  ни одна не вызвана: позиция не прочитана, ордер не отправлен
```

**`_from_adapter=True` на обоих внутренних вызывающих**
```
order_adapter.py:480      res = _m._execute_close_position(..., _from_adapter=True)
breakeven_worker.py:305   result = main._execute_close_position(..., _from_adapter=True)
main.py:1426              legacy SL-failsafe                    _from_adapter=True
```

**Дверь сверки закрыта в корне** — `main.py:4422`, `_resume_job_if_needed` возвращается раньше
`active_job`, с печатью `[RECONCILE] engine owns positions — NOT enqueueing`.

**Константы против `HEAD~1`**
```
compared: 107 · ADDED: ['PASSIVE_FILL_RECONCILE_EXISTS'] · REMOVED: []
CHANGED: LIVE_FIXED_MARGIN_USDT 40.0 -> 30.0
         ROUTING_MIGRATED_TO_ADAPTER False -> True
```
**Говорю точно: `CHANGED` здесь НЕ пусто — изменились ровно две константы, обе тобой одобренные**
(размер первого боевого прогона и маркер миграции). Ни один порог каскада, скоринг-гейта,
SL/трейла/безубытка, LONG-частички, ярусов сигналов и exit-advisor не сдвинулся. `LEVERAGE = 5`
не тронут.

**Бумага / БД / SOL**
```
vpos rows = 59 (было 59) · stop_order_id NOT NULL = 0 -> NULL везде
mercury-sol.service active · PID 1793275 · аптайм 8 суток · не тронут
```

---

## 3. ЧТО ТЕПЕРЬ СТОИТ МЕЖДУ НАМИ И БОЕМ

Ровно **один** пункт — 13. Оба боевых гейта сейчас заряжены так:

| гейт | состояние | снимается |
|---|---|---|
| `ROUTING_MIGRATED_TO_ADAPTER` | ✅ True | снят этим коммитом |
| `PASSIVE_FILL_RECONCILE_EXISTS` | 🔴 **False** | коммитом пункта 13 |
| блокер A (два `closePosition`) | ✅ недостижим по построению | — |
| блокер B (сиротский стоп) | ✅ обработан, остаточный случай под тревогой | — |

Пункт 13 построен и **не применён** — отдельный отчёт:
`reports/2026-07-29-1905-titan-item13-passive-fill-reconciliation-built-not-applied.md`
