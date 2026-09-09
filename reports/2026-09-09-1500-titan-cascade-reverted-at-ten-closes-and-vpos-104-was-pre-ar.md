# titan-cascade-reverted-at-ten-closes-and-vpos-104-was-pre-arm

_2026-09-09 15:00 UTC_

---

# 🔴🔴 ТИТАН — КАСКАД ОТКАЧЕН НА ДЕСЯТОМ ЗАКРЫТИИ. И vpos 104 ЗАКРЫЛАСЬ **ДО** ВЗВОДА, А НЕ ПОСЛЕ.

**2026-09-09 15:00 UTC · откат применён и ЗАГРУЖЕН рестартом 14:52:36 UTC из плоского · `6fa5d45` · `openitems_guard` EXIT=0 до и после**

---

## 🔴 ЧТО РЕШАТЬ ТЕБЕ

1. **Вооружение книжного гейта РАЗБЛОКИРОВАНО.** Ты привязал его к разрешению каскадного эксперимента —
   эксперимент разрешён и откачен. Гейт не тронут: `BOOK_GATE_DRYRUN = True`, `CLAUSE_B = False`,
   счётчик **8/200** (8 LONG / 0 SHORT, 0 отказов). Решение твоё; блокера больше нет.
2. **Триггер советника («следующие 5 закрытий — советник и до взвода → `EXIT_ADVISOR_DRYRUN = True`»)
   НЕ выполнен, но НЕ из-за vpos 104.** Его сломали трейл (100) и два стопа (102, 103). vpos 104 была
   ДО взвода и считалась бы В ПОЛЬЗУ триггера, а не против. Подробно в §3e.
3. 🔴 **Этого триггера нет ни в каноне, ни в одном опубликованном отчёте.** Я искал по канону, по всем
   отчётам 30.08–09.09 и по памяти. Ближайшее записанное — обратное: «флипать `EXIT_ADVISOR_DRYRUN` НЕ
   предлагаю» (отчёты 30.08 23:55 и 31.08 00:20). Если триггер должен действовать — его надо записать
   в `§0` явно, иначе следующая сессия его не увидит.

---

# 1. ТРИГГЕР ПРОВЕРЕН НЕЗАВИСИМО — СРАБОТАЛ СЧЁТ, НЕ ΣR

Правило `§0.CASCADE-STOP` (31.08): **откат при ΣR ≤ −5.0R ИЛИ на 10 закрытых позициях, что раньше.**

**Популяция.** Порт `a7e7b46` загружен 2026-08-21 19:44 UTC. До этого момента в БД **62** закрытия;
последнее из них — vpos 94 (открыта 17.08, закрыта 17.08 17:35, трейл, +0.7968R) — это первая позиция
батча №3 и она **старше порта**, в популяцию не входит. Закрытий с `closed_at ≥ 2026-08-21 19:44` —
**ровно десять, vpos 95…104, без пропусков**. Открытых строк 0. vpos 104 — **десятая**. Не 9 и не 11.

| vpos | сторона | открыта | закрыта | вход → выход | R | net $ | причина |
|---|---|---|---|---|---|---|---|
| 95 | LONG | 08-23 16:35 | 08-24 02:00 | 77409.9 → 76924.2 | −0.5326 | −1.08 | external |
| 96 | LONG | 08-24 12:45 | 08-24 13:45 | 78747.4 → 78121.0 | −0.5456 | −1.34 | ai_exit |
| 97 | LONG | 08-24 15:30 | 08-24 17:30 | 79764.4 → 78570.1 | −0.7964 | −2.29 | ai_exit |
| 98 | LONG | 08-27 08:15 | 08-27 13:16 | 79530.0 → 79348.4 | −0.2601 | −0.47 | ai_exit |
| 99 | LONG | 08-30 06:55 | 08-30 08:45 | 78232.4 → 78031.1 | −0.5318 | −0.55 | external |
| 100 | LONG | 08-30 13:05 | 08-30 17:18 | 78694.4 → 78979.9 | +0.4172 | +0.39 | trail |
| 101 | SHORT | 09-01 16:15 | 09-01 18:00 | 77661.0 → 77282.2 | +0.2956 | +0.57 | ai_exit |
| 102 | LONG | 09-06 23:45 | 09-07 01:16 | 80393.3 → 79825.5 | −1.1581 | −1.18 | sl |
| 103 | LONG | 09-07 02:40 | 09-07 03:37 | 80340.0 → 79653.7 | −1.1235 | −1.38 | sl |
| **104** | LONG | 09-09 04:45 | 09-09 08:30 | 79112.4 → 79637.7 | **+0.5757** | **+0.79** | ai_exit |

R = `net_pnl / initial_risk_usdt` из БД, как в каноне.

| условие | порог | факт | сработало |
|---|---|---|---|
| **10 закрытых** | 10 | **10** | 🔴 **ДА** |
| ΣR ≤ −5.0R | −5.0 | **−3.6595** | нет (не хватило 1.34R) |

## 1c. Против замороженной базы

База (окно B, открыты ≥ 2026-05-26, закрыты до порта): **n = 57, ΣR −0.2702, винрейт 42.1 %** —
я пересчитал её из БД по этому определению: **57 / −0.2702 / 42.1 % — совпадает до знака.**

| | n | ΣR | на сделку | вин | Σ$ |
|---|---|---|---|---|---|
| база (заморожена 21.08) | 57 | −0.2702 | **−0.0047R** | 42.1 % | — |
| эксперимент, все десять | 10 | **−3.6595** | **−0.366R** | 30.0 % | **−6.53** |
| LONG (загрязнена: партиал OFF с 27.08 17:14) | 9 | −3.9551 | −0.439R | 22.2 % | −7.10 |
| — из них чистые (открыты до партиал-OFF: 95–98) | 4 | −2.1347 | −0.534R | 0 % | −5.18 |
| — после партиал-OFF (99, 100, 102, 103, 104) | 5 | −1.8205 | −0.364R | 40 % | −1.92 |
| SHORT (чистая) | 1 | +0.2956 | +0.296R | 100 % | +0.57 |

## 1d. Порт сделал книгу ХУЖЕ — и в R, и в долларах

**−0.366R на сделку против −0.0047R — в 78 раз хуже, −$6.53 за 19 суток**, в ту же сторону, что
предсказывал реплей (−13.01R против −2.70R за 88 дней). ⚠️ n = 10 ничего не доказывает статистически;
что отличает этот случай — прогноз был ПРОТИВ изменения, и живой результат с ним согласен.
**LONG-нога загрязнена** выключением партиала внутри окна (4 чистых закрытия — все убыточные, ΣR −2.13).
**SHORT-нога чиста, но в ней ОДНО закрытие за 19 суток** — по ней сказать нельзя ничего.

---

# 2. ОТКАТ — ТРИ ЗНАЧЕНИЯ, НОЛЬ УДАЛЕНИЙ, ИЗ ПЛОСКОГО

| строка `config.py` | было | стало |
|---|---|---|
| `HTF_NEUTRAL_REQUIRE_15M_DRYRUN` | `True` | **`False`** — правило снова СУДИТ |
| `CONFLUENCE_FLAT_THRESHOLD` | `3.0` | **`5.0`** |
| `HTF_REARM_FROM_15M_ENABLED` | `True` | **`False`** — ре-взвод выключен |

**(d) Бэкап и снимок.** `config.py.bak_cascaderevert_20260909T145141Z` снят до правки.
Снимок `config.py.bak_solport_20260821T193618Z` на месте (61 129 байт) и несёт ровно те значения,
к которым я возвращаюсь: `HTF_NEUTRAL_REQUIRE_15M_DRYRUN = False`, `CONFLUENCE_FLAT_THRESHOLD = 5.0`.
`HTF_REARM_FROM_15M_ENABLED` в снимке **отсутствует** (его добавил порт) — эквивалент отсутствия это
`False`, а не удаление: `main.py:546` импортирует все три `HTF_REARM_*` по имени, удаление =
ImportError при загрузке. 🔴 **Снимок НЕ копировался поверх `config.py`** — он старше книжного гейта и
снёс бы 11 имён (ловушки 1 и 2 из утреннего отчёта 08:40).

**(e) AST-проверка.** Разобрал старый и новый `config.py`: **127 и 127 стейтментов, 124 и 124 имени,
добавлено 0, удалено 0, изменённых значений ровно три** — перечисленные выше.
Не тронуты (значения байт-в-байт по AST): `SL_ATR_MULT` 2.25 · `TRAIL_MULT_ATR` 1.6875 ·
EMA-конверт (`EMA_ENVELOPE_GATE_ENABLED` True, TFS ('1h','15m'), REQUIRED_DIR, FAIL_OPEN) ·
`LONG_PARTIAL_ENABLED` False · `CONFLUENCE_SCORE_THRESHOLD` 3.0 · `EXIT_ADVISOR_DRYRUN` False ·
**все четыре `BOOK_GATE_*`** (ENABLED True / DRYRUN True / CLAUSE_A True / CLAUSE_B False) ·
`LIVE_TRADING_ENABLED` True · `ORDER_ADAPTER_LIVE` True · размер `LIVE_FIXED_MARGIN_USDT` 30 × `LEVERAGE` 5 ·
`HTF_REARM_COOLDOWN_MINUTES` 60 / `HTF_REARM_DRYRUN` False (инертны, имена оставлены).
**Оба промпта советника:** `claude_advisor.py` не тронут — sha256 `ca14e959a5c6104c` совпадает с HEAD;
`git diff` против HEAD: один файл, `config.py`, 3 строки.

**(f) Плоско — дважды, обоими зондами, без ошибок.** Перед правкой и повторно в 14:52:24, за 11 секунд
до рестарта:

| проверка | результат |
|---|---|
| `virtual_positions status='open'` / `exit_pending` / `breakeven_jobs` | **0 / 0 / 0** |
| BingX зонд 1 `fetch_positions` | **[]** |
| BingX зонд 2 raw `swapV2 UserPositions` | **[]** |
| BingX открытые ордера, оба зонда | **[]** |
| список ошибок зондов | **[] — пусто** |

Рестарт `systemctl restart titan.service` 14:52:35 → **active 14:52:36 UTC, PID 705634, NRestarts=0**.
Строка загрузки, дословно:

```
[TITAN][ORDER-MODE] 🔴 LIVE ORDERS — REAL MONEY: orders ARE sent to BingX
[TITAN][ORDER-MODE]   LIVE_TRADING_ENABLED = True
[TITAN][ORDER-MODE]   ORDER_ADAPTER_LIVE   = True
[TITAN][ORDER-MODE]   sizing: margin $30 x 5 = $150 notional per entry
[TITAN][RECONCILE-XDB] ✅ exchange and DB agree for BTC/USDT:USDT: 0 exchange position(s), 0 open row(s)
[STOP-CLEANUP] no orphaned orders for LONG BTC/USDT:USDT
[STOP-CLEANUP] no orphaned orders for SHORT BTC/USDT:USDT
```

**Значения В РАНТАЙМЕ — из байткода, который импортировал воркер**, не из файла:
`__pycache__/config.cpython-312.pyc` записан 14:52:10 (после правки 14:51:41), заголовок несёт
mtime/size исходника **VALID: True**, cwd мастера `/root/titan-bot`:

```
HTF_NEUTRAL_REQUIRE_15M_DRYRUN   = False   🔴
CONFLUENCE_FLAT_THRESHOLD        = 5.0     🔴
HTF_REARM_FROM_15M_ENABLED       = False   🔴
HTF_REARM_COOLDOWN_MINUTES = 60 · HTF_REARM_DRYRUN = False
SL_ATR_MULT = 2.25 · TRAIL_MULT_ATR = 1.6875 · EMA_ENVELOPE_GATE_ENABLED = True
LONG_PARTIAL_ENABLED = False · CONFLUENCE_SCORE_THRESHOLD = 3.0 · EXIT_ADVISOR_DRYRUN = False
BOOK_GATE_ENABLED = True · BOOK_GATE_DRYRUN = True · CLAUSE_A = True · CLAUSE_B = False
LIVE_TRADING_ENABLED = True · ORDER_ADAPTER_LIVE = True · margin 30.0 × leverage 5 · MAX_POSITIONS_PER_SIDE = 1
✅ ASSERTIONS PASSED on loaded bytecode
```

`openitems_guard`: EXIT=0 до работы; EXIT=1 сразу после рестарта (канон утверждал 3.0 — ровно та
рассинхронизация, ради которой сторож существует); канон обновлён → **EXIT=0**.

**(g) Книжный гейт пережил откат нетронутым:** `BOOK_GATE_DRYRUN = True`, `CLAUSE_B = False` — в
байткоде. Счётчик **8/200** до и после рестарта (8 LONG / 0 SHORT, отказов 0) — колонки в БД,
рестарт его не обнуляет.

Коммит **`6fa5d45`** в `/root` (только `titan-bot/config.py`).
⚠️ Побочное наблюдение: `systemctl` предупредил `NeedDaemonReload=yes` — юнит и drop-in не менялись
(май и июль), изменился mtime каталога `/etc/systemd/system` в 13:38 сегодня, кто-то добавил другой юнит.
Титана не касается, я не трогал.

---

# 3. vpos 104 — И ТУТ ПРЕМИССА ЗАДАНИЯ НЕ ПОДТВЕРДИЛАСЬ

## 🔴 3.0. Трейл НЕ был взведён. Это ДВЕНАДЦАТОЕ закрытие советника и ТРЕТЬЕ прибыльное.

* **Взвод — при +1R = 79 874.7.** Пик позиции (water_mark) **79 661.9 = +0.721R**; 1m-свечи BingX дают
  максимум 79 681.1 за время позиции — до взвода не хватило **~194 USD = 0.25R**.
  `breakeven_applied = false`, `sl_price = original_sl_price = 78 350.1` (стоп ни разу не двигался),
  `breakeven_jobs` пуст, в журнале за 04:45–08:30 ни одной строки breakeven/trail.
  **Сам промпт советника в момент закрытия говорит: «The trailing stop is NOT ARMED — it arms only at +1R…
  A further 0.28R of favourable movement would arm it».**
* **Счёт советника по БД (`close_reason='ai_exit'`, status closed):** 87, 88, 89, 90, 91, 92, 93, 96, 97,
  98, **101**, 104 — **двенадцать**, не одиннадцать. В счёте задания пропущена **vpos 101** (SHORT,
  01.09, ai_exit, +0.2956R = +$0.57, до взвода). «Предыдущие десять стоили −$5.85» = сумма 87…98
  (−$5.848) — это десять БЕЗ 101. Прибыльных закрытий советника **три**: 89 (после взвода, +$2.30),
  101 (до взвода, +$0.57), 104 (до взвода, +$0.79). **До взвода — 11 из 12**; после взвода — только 89.
  Σ net всех двенадцати: **−$4.49**.

## 3a. Причина — полностью, без обрезки (1 095 символов, кэп 1 200 не сработал)

Строка `trades` 31113, 08:30:19, вердикт `close`, confidence 0.72 — **тот вердикт, который закрыл**:

> Entry thesis collapse on 5m timeframe. At entry, 5m showed Bullish I-BOS with fresh trigger and strong volume (6.17x). Now 5m is neutral (down from bull) with volume collapsed to 0.39 (down from 2.52). Recent 5m structure is consistently bearish: Bearish Imbalance Mitigated, Within Bearish OB, Bearish Breaker all within last 10m—directly contradicting the entry trigger. The 15m HyperWave Signal Up (weight 0.7) remains but 1H confirmation has expired via TTL (360min since entry, now 222min old). ADX15m spiked to 30.1 (up from 20.2), indicating directional conviction—but that conviction is now bearish on the 5m. Order book imbalance flipped 0.47→0.52 (now 71st pct, elevated), opposing wall collapsed to 16th pct, suggesting weakening bid support. Position has gained +0.67R but is only 0.05R below peak MFE; giveback has begun. Closing costs 0.104R (15% of unrealised), leaving net +0.566R. The 3TF agreement that justified entry is broken: 5m no longer bullish, 1H signal expired, only 15m remains. Risk/reward now favours locking profit before further 5m deterioration reaches the stop.

🔴 **Был и ВТОРОЙ вердикт** — строка 31115, 08:30:23, тоже `close` 0.72 (1 133 символа), по второму
15m-вебхуку (`Bullish S-CHOCH`) через 4 секунды после первого (`Bullish I-BOS`). Он попытался закрыть
уже закрытую позицию — адаптер не нашёл её на бирже, ничего не отправил. Текст:

> Entry thesis decay + adverse structural flip. The 1H Bullish Confirmation has EXPIRED (TTL 360min, set 12.8h ago); only 15m HyperWave and 5m I-BOS remain active. Current 5m regime has shifted to NEUTRAL (was BULL at entry), and recent 5m structure is uniformly BEARISH: Bearish OB entered 5m ago, Bearish Breaker 5m ago, Bearish Imbalance just mitigated. Order-book imbalance flipped from 0.47 to 0.52 (more bullish on surface, but opposing wall is weak at 16th pct vs supporting wall 89th pct—unusual asymmetry suggesting fragile support). ADX15m rose to 30.1 (directional strength increased but now in a neutral 5m regime, making it a whipsaw marker). Vol_15m collapsed from 2.52 to 0.39, suggesting momentum exhaustion. Position has given back 0.03R from peak (+0.72R) already despite only 3.7h elapsed. Closing cost is 0.104R (15% of current unrealised +0.70R), leaving net +0.60R—still profitable but thesis deterioration outweighs the fee friction. The 15m and 5m confluence that justified entry no longer holds; 5m has turned structurally hostile. Holding risks stop-loss at -1.00R (1.70R away) against a weakening entry case.

Это НЕ первое закрытие под кэпом 1 200 и пятью фактами — первым была vpos 101 (01.09, 1 128 символов).

## 3b. Какие из пяти фактов использованы

| факт | в промпте был? | 31113 (закрывший) | 31115 |
|---|---|---|---|
| стоимость закрытия (комиссия) | да: 0.104R = 15 % | ✅ «Closing costs 0.104R (15% of unrealised), leaving net +0.566R» | ✅ «0.104R (15%)… net +0.60R» |
| стоп на бирже, −1.00R пол | да | ❌ только «reaches the stop», без биржевого стопа и пола | ◐ «stop-loss at −1.00R (1.70R away)» — пол назван, «resting on the exchange» нет |
| уровень трейла / расстояние до взвода | да: NOT ARMED, +1R = 79 874.7, ещё 0.28R | ❌ не упомянут | ❌ не упомянут |
| дельта импульса с прошлой консультации | да: +0.08R → +0.67R (+0.60R), MFE +0.30 → +0.72 | ❌ (цитирует giveback от пика — это другая строка) | ❌ |
| required-MFE (пятый факт) | **НЕТ — не рендерится** | — | — |

🔴 **Пятый факт в промпте отсутствовал по устройству:** `_required_peak_block` рендерится только для
ВЗВЕДЁННОЙ позиции («nothing is rendered from an unarmed position», `main.py:3160`). vpos 104 была до
взвода — советник его физически не видел. **Итого: 1 из 4 показанных фактов использован явно (комиссия),
второй частично во втором вердикте, два проигнорированы, пятый не показан.**

## 3c. Контрфакт — где вышел бы ТРЕЙЛ

Реплей на реальных 1m-свечах BingX `BTC/USDT:USDT` с 04:45 до **14:54 UTC** (615 свечей), порядок
`bardir` (растущий бар → минимум первым, падающий → максимум первым), правила из `virtual_trader.py`:
стоп 78 350.1; взвод при 79 874.7 (+1R) → стоп на 79 270.6 (breakeven + 2 комиссии + 0.1 %);
трейл `water_mark × (1 − 0.723 %)` только после взвода.

| | |
|---|---|
| взвод +1R (79 874.7) после закрытия советника | **не напечатан.** Максимум после 08:30 — **79 737.7 в 08:36**, до взвода **137 USD = 0.18R** |
| исходный стоп 78 350.1 | **не тронут.** Минимум 78 707.0 в 11:03 (357 USD над стопом) |
| позиция в реплее на 14:54 | **всё ещё ОТКРЫТА**, цена 78 945.1 → **−0.219R брутто = −$0.30** (−$0.44 нетто, если закрыть сейчас) |
| советник | **+0.5757R = +$0.79 нетто** |
| разница на 14:54 (mark-to-market) | **советник впереди на ≈0.79R ≈ $1.09**, и удержанная позиция всё ещё под −1R стопом |

**Трейл слова не получил: он не взводился ни до закрытия, ни после.** Вопрос «где вышел бы трейл»
пока не имеет ответа — контрфактная позиция открыта. Что можно сказать твёрдо: **советник НЕ обрезал
бегуна** — после его выхода цена поднялась ещё на 100 USD, не дошла до взвода 0.18R и развернулась вниз.
⚠️ Итог не окончательный: он станет окончательным, когда реплей упрётся в стоп (−1R) или во взведённый
трейл. По состоянию на 14:54 это выигрыш советника.

## 3d. Проверка числовых утверждений против промпта

Вердикт 31113 (закрывший):

| утверждение | промпт | вердикт |
|---|---|---|
| 5m volume 6.17x at entry | entry reason: «strong 5m volume (6.17x)» | ✅ |
| 5m neutral, was bull | Now 5m=neutral; At entry 5m=bull | ✅ |
| «volume collapsed to 0.39 (down from 2.52)» — приписано 5m | это `vol_15m: 2.52 → 0.39` | ◐ числа верны, таймфрейм перепутан |
| bearish structure within 10m | 0m / 0m / 5m ago | ✅ |
| 15m HyperWave remains | да | ✅ |
| **«1H expired via TTL (360min since entry, now 222min old)»** | 1H set **12.8h ago at entry**, TTL 360; 222 мин = 3.7 ч — это возраст ПОЗИЦИИ | 🔴 **сфабриковано/перепутано**: сигналу ~16.5 ч, не 222 мин |
| ADX15m 30.1, up from 20.2 | 20.2 → 30.1 | ✅ |
| imbalance 0.47→0.52, now 71st pct | да | ✅ |
| **«opposing wall collapsed to 16th pct»** | NOW = 16th pct, entry-значения НЕТ; промпт прямо: «NONE of these is a change over time» | 🔴 **вывод об изменении без данных** |
| +0.67R, 0.05R below peak | +0.67R, giveback 0.05R | ✅ |
| 0.104R = 15 %, net +0.566R | 0.104R, 15 %; 0.67 − 0.104 = 0.566 | ✅ |

Вердикт 31115: +0.70R, giveback 0.03R, стоп 1.70R, net +0.60R (0.70 − 0.104 = 0.596), Vol_15m 2.52 → 0.39,
opposing 16th / supporting 89th как ТЕКУЩИЕ величины — **все ✅**, включая корректный таймфрейм и
корректное «not a change». Второй вердикт точнее первого; закрыл — первый.

## 3e. Триггер советника от 30.08 — статус

Формулировка из задания: «если следующие 5 закрытий — снова советник и снова до взвода, флип
`EXIT_ADVISOR_DRYRUN = True`». 🔴 **В каноне и в отчётах этой формулировки нет** (см. «Что решать»).
Проверяю как сформулировано. Закрытия после 30.08 15:00 UTC:

| # | vpos | закрыта | причина | взвод | R |
|---|---|---|---|---|---|
| 1 | 100 | 08-30 17:18 | **trail** | ✅ взведена (MFE +1.32R) | +0.4172 |
| 2 | 101 | 09-01 18:00 | **ai_exit** | до взвода (MFE +0.43R) | +0.2956 |
| 3 | 102 | 09-07 01:16 | **sl** | до взвода | −1.1581 |
| 4 | 103 | 09-07 03:37 | **sl** | до взвода | −1.1235 |
| 5 | 104 | 09-09 08:30 | **ai_exit** | **до взвода** (MFE +0.72R) | +0.5757 |

**Пять закрытий прошли: советник — 2 из 5, оба ДО взвода, оба ПРИБЫЛЬНЫЕ; трейл — 1; стоп — 2.**
Условие «все пять — советник» **не выполнено** — сломано трейлом на 100 и стопами на 102/103.
🔴 **Не vpos 104 его сломала**: она была до взвода и легла бы В условие. Утверждение задания
«104 была ПОСЛЕ взвода» — ложно по БД, по журналу и по тексту самого промпта.
Триггер НЕ выполнен → `EXIT_ADVISOR_DRYRUN` остаётся `False`, советник действует.

## 3f. Два дефекта на закрытии — наблюдение, НЕ чинил (вне задания)

1. **Двойная консультация по одной позиции.** Два 15m-вебхука (`Bullish I-BOS` 08:30:12,
   `Bullish S-CHOCH` через ~4 с) в `gthread`-воркере параллельно вызвали советника для одной vpos —
   два платных вызова, два `CLOSING at market`. Второй не навредил только потому, что адаптер не нашёл
   позиции. На пути `main.py:4328` нет замка «консультация уже в полёте для этой позиции».
2. **Ложная тревога `[VPOS-FILL] 🚨 … MANUAL ACTION REQUIRED`** в 08:30:20 — через секунду после
   рыночного закрытия самим советником, до того как `_do_close` записал строку (08:30:22). Гонка
   между поллером заполнения и собственным закрытием; вручную ничего не требовалось.

---

# 4. ЗАПИСАНО

* **Канон `OPEN-ITEMS.md`:** шапка → `6fa5d45` с абзацем отката; три строки таблицы состояния
  (`CONFLUENCE_FLAT_THRESHOLD` 5.0, `HTF_NEUTRAL_REQUIRE_15M_DRYRUN` False, `HTF_REARM_*` False/60/False);
  в `§0.CASCADE-STOP` добавлен блок **REVERTED 2026-09-09 14:52:36** — какая рука сработала, десять
  позиций, сравнение с базой, откаченные значения; старая строка «nothing has been reverted» зачёркнута.
  `openitems_guard` **EXIT=0**. Бэкап `OPEN-ITEMS.md.bak_cascaderevert_20260909`.
* **Разблокировано:** вооружение книжного гейта. Блокер («после разрешения каскада») снят. Решение — твоё.
* **Mercury-SOL не тронут:** ни байта, ни чтения его БД, ни рестарта. В `systemctl list-units` его имя
  мелькнуло в общем списке служб хоста — это состояние хоста, не SOL.

**Итог: правило сработало по счёту (10/10, ΣR −3.66 из −5.0); три значения откачены и загружены из
плоского, всё остальное — байт-в-байт; vpos 104 закрылась +0.58R ДО взвода, советник не обрезал
бегуна (взвод после выхода не напечатан, реплей-позиция на 14:54 в −0.22R); триггер советника не
выполнен из-за трейла и стопов, а не из-за 104 — и его формулировки в каноне нет.**

Титан `6fa5d45`.
