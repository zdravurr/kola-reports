# ФИНАЛЬНАЯ ВЕРИФИКАЦИЯ ПЕРЕД ПЕРВОЙ БОЕВОЙ СДЕЛКОЙ — ТОЛЬКО ЧТЕНИЕ
**2026-07-29 19:30 UTC** · HEAD `cb3a8bb` · **ничего не изменено, ничего не размещено**

> **ВЕРДИКТ: всё сходится, кроме ОДНОГО — и это документ, а не код.**
> `OPEN-ITEMS` в четырёх местах утверждает, что бот бумажный и `LIVE_TRADING_ENABLED = False`.
> Это **устарело и активно вводит в заблуждение**: бот работает на реальных деньгах.
> Код, счёт и защитная машинерия — чисты, проверены исполнением. Подробности в §F.

---

## A. СОСТОЯНИЕ — ТО, ЧЕМ МЫ ЕГО СЧИТАЕМ

### A1. Git — чисто и синхронно
```
dirty files: 0
HEAD        = cb3a8bbce441a2c9a412ec8473fa106467a59a0d
origin/main = cb3a8bbce441a2c9a412ec8473fa106467a59a0d
ahead/behind = 0 / 0
```
**18 коммитов `93c20c3..HEAD`, ВСЕ 18 запушены** (проверено `git merge-base --is-ancestor` против
`origin/main`, не по памяти):

| коммит | что |
|---|---|
| `cb3a8bb` | **LIVE: flip both mode flags — real orders enabled at $150 notional** |
| `984c96a` | docs: the margin-mode comment was lying — it is CROSSED, not isolated |
| `d63cb8b` | item 13 — passive-fill reconciliation, the last live gate |
| `0833f42` | item 12 — routing asks WHO OWNS THE POSITION, and live gains a second gate |
| `5f054b7` | item 11 — the stop moves to the exchange, and orphan stops are cancelled |
| `96b83d4` | live-order adapter — one seam for fills, and a boot that REFUSES an unsafe config |
| `5285495` | the .sh watchers were outside git |
| `41c4a4d` | delete the Long/Short ratio line; edge-trigger one sensor, expire two |
| `c307bb7` | two prompt claims replaced by facts |
| `4fc89ea` | the EXIT prompt's "Total depth" line |
| `7285c5d` | all THREE signal tiers reach both advisors |
| `8b15ecc` | ENTRY advisor order-book PERCENTILE scale |
| `f0a8d30` | entry advisor 1H signal IDENTITY |
| `d12e276` | retire 3 sensors, redefine 2 |
| `ef7fa10` | persist 15m entry confirmation + exit advisor DRYRUN |
| `f7df202` | LONG-side partial realisation |
| `b878535` | RETIRE the counter-trend EMA-1h soft caution |
| `596fbdf` | gate the counter-short soft caution on trend_1d |

### A2. Рантайм = коммит, **ПО ХЕШУ** — 6/6 MATCH
```
config.py           disk=de96898a5cbdbdca2abf  commit=de96898a5cbdbdca2abf  MATCH
order_adapter.py    disk=be801a1af768ce437c1b  commit=be801a1af768ce437c1b  MATCH
virtual_trader.py   disk=f3d97888168aa07a5d71  commit=f3d97888168aa07a5d71  MATCH
breakeven_worker.py disk=87e39b3a21574dde9e37  commit=87e39b3a21574dde9e37  MATCH
main.py             disk=842ac86a29d17eb8b355  commit=842ac86a29d17eb8b355  MATCH
gunicorn.conf.py    disk=c94a870a59136ad62bb6  commit=c94a870a59136ad62bb6  MATCH
```
Процесс стартовал 19:14:17, файлы записаны раньше, дерево чистое ⇒ **работает ровно закоммиченный код.**

### A3. Баннер из живого журнала, дословно
```
Jul 29 19:14:21 titan[4173035]: [TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
Jul 29 19:14:21 titan[4173035]: [TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
Jul 29 19:14:21 titan[4173035]: [TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
Jul 29 19:14:21 titan[4173035]: [TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
```
```
NRestarts = 0     ошибок с 19:14:17 = 0     REFUSING TO START = 0
master 4173035 (19:14:17)  ->  worker 4173057 (19:14:26, ПОСЛЕ мастера)
```

### A4. Флаги в рантайме
| флаг | значение |
|---|---|
| `LIVE_TRADING_ENABLED` | **True** |
| `ORDER_ADAPTER_LIVE` | **True** |
| `ROUTING_MIGRATED_TO_ADAPTER` | True |
| `PASSIVE_FILL_RECONCILE_EXISTS` | True |
| `LEVERAGE` | 5 |
| `PAPER_FIXED_MARGIN_USDT` | 2000.0 |
| `LIVE_FIXED_MARGIN_USDT` | **30.0** |
| `FIXED_NOTIONAL_MODE` | True |
| `LONG_PARTIAL_ENABLED / LEVEL_R / FRACTION` | True / 1.0 / 0.3333 |
| `EXIT_ADVISOR_DRYRUN` | **True** — советник **не может закрыть позицию**, только пишет вердикт |
| `EXIT_ADVISOR_HOURLY / _SEC / _PAPER_ENABLED` | True / 3600 / True |
| `CONFLUENCE_SCORE_THRESHOLD / _FLAT_` | 2.0 / 5.0 |
| `WALL_TRAIL_LIVE_ENABLED` | **False** · `WALL_ANCHOR_DRYRUN_ENABLED` True |
| `AI_ADVISOR_HIDE_1H` | True |
| `HTF_CASCADE_ENABLED / _TOLERATE_NEUTRAL` | True / True |
| `SL_ATR_MULT / TRAIL_MULT_ATR / SL_ATR_TF / TRAIL_ATR_TF` | 2.5 / 2.5 / 1h / 1h |
| `MAX_POSITIONS_PER_SIDE` | 1 |
| `POST_ENTRY_RECHECK_ENABLED` | True |

**Производные:** `orders_are_real()=True` · `stop_lives_on_exchange()=True` ·
`active_fixed_margin()=30.0 → $150` · `is_active()=False` (заливки НЕ симулируются) ·
`engine_owns_position()=True` · `routing_warning()=''` · `passive_fill_warning()=''`.

**Сверка с OPEN-ITEMS → одно расхождение, см. §F.** Численные пороги (2.0/5.0/2.5/1h, LONG-partial,
HTF, WALL_TRAIL) совпадают с записанными.

> ⚠️ Проверял импортом `config` в свежем процессе, а не интроспекцией памяти gunicorn. Это
> эквивалентно **потому, что** A2 доказал совпадение файлов с коммитом, а процесс стартовал после
> последней записи. Говорю прямо, а не выдаю одно за другое.

---

## B. БИРЖА ЧИСТА

```
позиций с contracts>0 = 0        ->  FLAT
открытых ордеров      = 0        ->  NONE
USDT free=512.8756  used=0.0  total=512.8756
плечо ПЕРЕЧИТАНО с биржи: long=5  short=5   -> оба 5: True
margin mode: {'symbol':'BTC-USDT','marginType':'CROSSED'}   (принято для этого размера, §1b OPEN-ITEMS)
position mode: dualSidePosition = "true"    -> HEDGE ВКЛЮЧЁН
```
Hedge обязателен: **весь код передаёт `positionSide`** и без него сломался бы.

---

## C. ЗАЩИТНАЯ МАШИНЕРИЯ — ПЕРЕДОКАЗАНА НА ПРИМЕНЁННОМ КОДЕ, В БОЕВОЙ КОНФИГУРАЦИИ

Все тесты выполнены при `orders_are_real() = True` **с мок-биржами** — на реальную биржу не ушло
ничего (B подтверждает: ордеров 0).

**C8 — инвариант постановки стопа**
```
[BE-SL-RETRY] attempt 1/3, 2/3, 3/3 failed
[ADAPTER] 🚨 STOP PLACEMENT FAILED ... firing the emergency close invariant
place_stop -> None        emergency close fired: True        попыток: 3
```
`None` ⇒ вызывающий **не пишет строку**. Позиция не остаётся без защиты.

**C9 — отмена сиротского стопа на ОБОИХ путях аборта**
```
cancel_stop(real id) -> True, cancelled: ['STOP-ORPHAN']
путь «проверка вместимости» вызывает cancel_stop : True
путь «IntegrityError»        вызывает cancel_stop : True
```

**C10 — сверка пассивных заливок, четыре исхода**
```
A') нет stop_order_id            -> False (к бирже не обращается)
B)  позиция ОТКРЫТА              -> False
C)  позиции нет, стоп НЕ залит   -> False + 🚨 тревога, строку НЕ ТРОГАЕТ
D)  позиции нет, стоп ЗАЛИТ      -> True, reason/price/fee = ('sl', 63000.0, 0.0724)
    при breakeven_applied=True   -> reason = 'breakeven'
```

**C11 — гонка `move_stop`**
```
отмена упала + позиция ОТКРЫТА  -> ('retry',1)  новый стоп создан: False  аварийное: False  ← СТАРЫЙ СТОП ОСТАЛСЯ
отмена упала + позиция ИСЧЕЗЛА  -> ('closed',None)  аварийное: False
отмена ОК + пересоздание упало  -> emergency, аварийное закрытие ВЫЗВАНО
```

**C12 — `_from_adapter` обходит маршрутизацию на обоих внутренних вызывающих**
```
order_adapter.market_close        -> _from_adapter = True
breakeven_worker._emergency_close -> _from_adapter = True
оба True ⇒ рекурсии нет, аварийное закрытие достаёт СЫРЫЕ механики
```

**C13 — `check_size` отбраковывает до отправки**
```
amount=1e-05  -> ok=False  'amount rounds to zero at exchange step'
amount=0.0023 -> ok=True   'ok (amount 0.0023, notional $148.26)'
ордеров отправлено во время check_size: 0
```

---

## D. ЧТО ПРОИЗОЙДЁТ НА ПЕРВОМ ВХОДЕ — ТРАССИРОВКА ПО ТЕКУЩЕМУ КОДУ

**Порядок функций:**
```
webhook()                                   TradingView -> Flask
  insert_signal(...)                        is_virtual = 0  (orders_are_real() True)
  [гейты: HTF-каскад, скоринг, veto]
  _execute_entry(symbol, side, position_side, signal_row_id)
    └─ if virtual_trader.engine_owns_position():   -> True
         return virtual_trader.execute_entry(...)  ← ВОЗВРАТ ЗДЕСЬ
              _trail_pct_for / ATR / _fixed_margin = order_adapter.active_fixed_margin() = 30.0
              order_adapter.check_size(...)        отбраковка до отправки
              order_adapter.market_entry(...)      set_leverage(5) [warn-only] -> create_market_order
                   └─ _live_fill(...)              РЕАЛЬНЫЕ цена/размер/комиссия; fetch_order_fee
              sl_price = fill − 2.5×ATR(1h)
              order_adapter.place_stop(...)        STOP_MARKET closePosition='true', 3 попытки
                   └─ провал -> _emergency_close -> _execute_close_position(_from_adapter=True)
                               -> place_stop=None -> строка НЕ пишется
              [проверка вместимости / INSERT]      любой аборт -> cancel_stop(поставленный стоп)
              INSERT virtual_positions (stop_order_id = биржевой id)
```

**D14 — legacy-путь недостижим, доказано:** ветка `engine_owns_position()` в `_execute_entry`
**возвращает** (`return virtual_trader.execute_entry(...)`) на строке ~1289, а legacy-размер
`FIXED_MARGIN_USDT` (**2000.0 → $10 000**) живёт на строках 1319-1320 — **ниже возврата**.
🔴 **Это и есть та самая катастрофа «$10 000 вместо $150»: она физически недостижима**, пока
`engine_owns_position()` возвращает True. Проверено чтением структуры, не утверждением.

**D15 — `TRAILING_STOP_MARKET` создать невозможно.** Единственное место создания —
`breakeven_worker._attempt_trail` (`breakeven_worker.py:532`). Достижимо только из `_poll_once`
при наличии джобы. Исполнено:
```
bw._poll_once(мок) -> 0   позиция не прочитана, ордер не создан (мок упал бы на обоих)
```
**⇒ блокер A недостижим по построению: в любой момент существует ровно ОДИН `closePosition` ордер.**

**D16 — `breakeven_worker` не может управлять позицией.**
```
breakeven_jobs строк за всю жизнь: 0
enqueue() call sites: main.py:1445 (legacy вход — недостижим) · main.py:4431 (_resume_job_if_needed)
_resume_job_if_needed guarded by engine_owns_position(): True
```
Две двери закрыты + стенд-даун по флагу = три независимых замка.

---

## E. ЧТО МОЖЕТ УКУСИТЬ ИМЕННО НА ПЕРВОЙ СДЕЛКЕ

Ранжировано по **вероятность × цена**.

| # | что | вер. × цена | как выглядит в логе | само/руки |
|---|---|---|---|---|
| 1 | **Допущение `closePosition='true'` неверно** | сред × **высокая** | после входа на бирже **больше одного** ордера; или у стопа конкретный `quantity`; или **после срабатывания позиция ≠ 0 / перевёрнута** | 🖐 **РУКИ: сразу вернуть флаги в False** |
| 2 | **Биржа отвергает ордер/параметры** (первый боевой ордер вообще) | сред × низкая | traceback из `create_market_order`; строки нет, позиции нет | само (входа просто не будет) |
| 3 | **Комиссия не пришла с биржи** | сред × низкая | `[ADAPTER] fee not reported ... ESTIMATED $...` | само (оценка по тейкеру), но комиссия в книге приблизительная |
| 4 | **Постановка стопа провалилась** | низк × средняя | `BE-SL-RETRY` ×3 → `🚨 STOP PLACEMENT FAILED` → `✅ Emergency close executed`, строка не пишется | **само, ПО ЗАМЫСЛУ** |
| 4b | ↳ **и аварийное закрытие тоже провалилось** | очень низк × **критическая** | `[SL-FAILSAFE] CRITICAL: emergency close itself failed` | 🖐 **РУКИ НЕМЕДЛЕННО — живая позиция без стопа** |
| 5 | **Случай C: позиция исчезла, наш стоп не залит** | низк × средняя | `🚨 POSITION GONE, STOP DID NOT FILL ... MANUAL ACTION REQUIRED` | 🖐 руки; сторона заблокирована до разбора |
| 6 | **Частичная / нулевая заливка** | очень низк × средняя | `🔴 PARTIAL FILL on entry ... asked X, filled Y` | само (размер вниз по потоку берётся исполненный), но позиция меньше задуманной |
| 7 | **Сиротский стоп не отменился** | очень низк × средняя | `🚨 ORPHAN STOP COULD NOT BE CANCELLED` | 🖐 руки |
| 8 | **`set_leverage` warn на входе** | низк × **нулевая сейчас** | `[ADAPTER] set_leverage warn:` | само — на бирже уже 5/5 |
| 9 | **МОЛЧАНИЕ на выходе** (мета-симптом) | низк × высокая | позиция закрылась, а в логе **ни** `[VPOS-FILL]`, **ни** close-report | 🖐 проверить `select status from virtual_positions` — если `open`, п.13 не сработал |

---

## F. 🔴 ЕДИНСТВЕННАЯ НАХОДКА: `OPEN-ITEMS` УСТАРЕЛ И ВРЁТ ПРО РЕЖИМ

Файл, который **специально существует для того, чтобы сессия без памяти действовала безопасно**,
в четырёх местах описывает бумажного бота:

| строка | текст | реальность |
|---|---|---|
| 6 | «Titan is a **BTC swing paper-trading bot**. `LIVE_TRADING_ENABLED = False`. All P&L below is paper» | **бот на реальных деньгах** |
| 50 | «§1 LIVE-PATH PARITY GAP — BLOCKING before `LIVE_TRADING_ENABLED = True`» | уже True |
| 84 | «Neither can fire today (**both flags False, and item 12 has not migrated the routing**)» | оба флага True, п.12 **мигрирован** |
| 670 | «🔴 `LIVE_TRADING_ENABLED=False`» | True |

Это **ровно тот класс дефекта**, который мы сегодня чинили в комментарии про isolated/CROSSED:
документ утверждает то, чего нет. Здесь цена выше — следующая сессия прочитает «бумажный бот» и
может действовать соответственно, **пока идут реальные деньги**.

**Я НИЧЕГО НЕ ИЗМЕНИЛ** — ты сказал только чтение. Но это **надо поправить**, и это документация,
а не система. Одно твоё слово — опубликую исправленный `OPEN-ITEMS` новым датированным файлом.

---

## G. В ЧЁМ Я НЕ УВЕРЕН — ПРЯМО

1. **Поведение BingX на `closePosition='true'` не наблюдалось ни разу.** Всё остальное можно было
   проверить; это — нет. Первая сделка и есть проверка.
2. **`_live_fill`: `filled == 0.0` трактуется как полная заливка** (`executed = filled if filled
   else amount`). Отличить «биржа ещё не отчиталась» от «не залилось» код не может. Вероятно
   самолечится через провал постановки стопа, но «вероятно» — честное слово здесь.
3. **Частота отказа `fetch_order_fee` неизвестна** (n=2, отказов 0). Оценить по двум наблюдениям нельзя.
4. **Ни один боевой путь не исполнялся против настоящей биржи.** Все доказательства §C — моки,
   написанные мной по моему же пониманию API. Где понимание неверно, тест не поймает по построению.

---

## ИТОГ

**Код, счёт, защитная машинерия, маршрутизация и недостижимость блокера A — всё сходится и
проверено исполнением.** Единственная находка — устаревший `OPEN-ITEMS` (§F), документ, не система.

Бот вооружён, биржа пуста, ждёт сигнала. Сегодня больше ничего не трогаю.
