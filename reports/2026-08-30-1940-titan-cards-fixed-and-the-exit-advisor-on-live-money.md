# ТИТАН: КАРТОЧКИ ИСПРАВЛЕНЫ · СОВЕТНИК ВЫХОДА НА ЖИВЫХ ДЕНЬГАХ

**2026-08-30 19:40 UTC** · `openitems_guard` — **EXIT=0** до, **MISMATCH** после коммита (ожидаемо,
шапка канона указывала на старый HEAD), **EXIT=0** после правки канона. `titan-bot HEAD` **`3888504` → `a0c77f2`**.
🔴🔴 **Mercury-SOL НЕ ТРОНУТ:** в дерево не входил, файлы не читал, БД не открывал, службу не трогал.
🔴 **ЧАСТЬ 2 И 3 — ТОЛЬКО ЧТЕНИЕ.** Ни одного ордера. Живая позиция **vpos 100 не тронута**.

**Bonferroni объявлен в шапке:** 4 гипотезы в Части 2 (советник против контрфактуала в долларах,
в R, разбиение по взводу, сравнение холда). **α = 0.05 / 4 = 1.25 × 10⁻².**

---

## 0. 🔴 ГЛАВНОЕ, ЧТО НАДО ПРОЧИТАТЬ ПЕРВЫМ

### 0.1 ПРАВКА ЛЕЖИТ НА ДИСКЕ И **НЕ ЗАГРУЖЕНА**. РЕСТАРТ ЗА ТОБОЙ.

🔴 **vpos 100 ОТКРЫТА** (LONG от 78 694.4, стоп 78 204.5, с 13:05:16 UTC). По пункту (g) —
**ОСТАНАВЛИВАЮСЬ И НЕ ПЕРЕЗАПУСКАЮ.** Коммит `a0c77f2` в дереве и запушен, но
**работающий воркер по-прежнему исполняет `3888504` и по-прежнему шлёт СТАРЫЕ карточки.**
Пока рестарта нет, всё, что приходит в Telegram, — старая отрисовка.

Это ровно [РАЗРЫВ РАЗВЁРТЫВАНИЯ](project_sol_p2_loaded_p1_g2c_applied_deployment_gap_06aug.md),
и он здесь **намеренный**. Записан в канон как **§0.CARDLABEL**.

### 0.2 🔴 ЕЩЁ ОДНА МОЯ ОШИБКА В СЧЁТЕ, ТРЕТЬЯ ЗА ДЕНЬ. СНИМАЮ СРАЗУ.

**Постановка говорит «советник закрыл 8 и потерял −$7.55». Это моя цифра из отчёта 18:10,
и она НЕВЕРНА.**

```
советник закрыл живых позиций : 10  (не 8)
его результат                 : -$5.8481  (не -$7.55)
```

Причём **таблица в том же отчёте 18:10 показывала все десять** (87, 88, 89, 90, 91, 92, 93, 96, 97, 98) —
**ошиблась ПРОЗА, не данные.** Я написал «восемь» в тексте §5.2 и не сверил с собственной таблицей.

**Три ошибки счёта за один день** — «−14.19R круговых рейсов» (снято в 17:20), «одна живая сделка
за −$2.54» (снято в 18:10) и теперь «восемь закрытий за −$7.55». Класс один и тот же:
**я пересказываю свою же таблицу вместо того, чтобы её пересчитать.**

### 0.3 И ОТВЕТ ПО СОВЕТНИКУ, БЕЗ ХЕДЖА

**Советник — НЕ доказанная причина убытка, и на десяти закрытиях доказать её нельзя.
Но описательно он стоил $2.01 из $9.49, и его ошибки крупнее его удач.**

---

# ЧАСТЬ 1 — КАРТОЧКИ

## 1c. 🔴 СНАЧАЛА — ВЕРЕН ЛИ ПРЕДИКАТ. ПРОВЕРЕНО **ДО** ПРИМЕНЕНИЯ.

Вопрос поставлен правильно: `stop_order_id IS NOT NULL` — **единственный** признак живой строки
(колонки `is_paper` в Титане **НЕТ**). Что будет с живой строкой, у которой постановка стопа
**ПРОВАЛИЛАСЬ**?

**Ответ: такой строки не может существовать. По построению.** `virtual_trader.py`, блок STOP OWNERSHIP:

```python
        _stop = order_adapter.place_stop(
            exchange, symbol, position_side, amount, sl_price, send_tg=send_tg, anchor=...)
        if _stop is None:
            print(f"VIRTUAL ENTRY ABORTED {symbol} {position_side}: protective "
                  f"stop could not be placed; emergency close fired, no row "
                  f"written", flush=True)
            return None
        _stop_order_id = _stop['stop_order_id']
```

**Строка пишется ТОЛЬКО после того, как `place_stop()` вернул id.** Провал стопа → аварийное
закрытие → `return None` → **строки нет вообще**. Комментарий там же: *«In paper this returns
instantly with stop_order_id=None … In live it is a real STOP_MARKET, and None means the emergency
close already fired.»*

**Эмпирическая проверка, обе стороны:**

```
строк, открытых ПОСЛЕ go-live (2026-07-29 20:05) с stop_order_id IS NULL : 0
строк, открытых ДО go-live с stop_order_id NOT NULL                     : 0
```

✅ **Предикат не может ввести в заблуждение. Применяю.**

## 1a/1b. ДВЕ ПРАВКИ

```diff
  # virtual_trader.py:1276 -> 1282   (фандинг)
- opened_at=row['opened_at'], closed_at=closed_at, is_virtual=True)
+ opened_at=row['opened_at'], closed_at=closed_at,
+ is_virtual=(row['stop_order_id'] is None))

  # virtual_trader.py:1299 -> 1310   (карточка)
- trail_pct=row['trail_pct'], is_virtual=True,
+ trail_pct=row['trail_pct'], is_virtual=(row['stop_order_id'] is None),
```

### 🔴 И ОДНА ВЕЩЬ, КОТОРУЮ Я ОБЯЗАН БЫЛ ПРОВЕРИТЬ ПЕРЕД (b), И ПРОВЕРИЛ

Правка (b) **не косметическая**: она переключает живую строку с ОЦЕНКИ фандинга на **реальную
ленту биржи**, а `funding_paid` входит в `net_pnl` — то есть **меняется СОХРАНЯЕМОЕ ЧИСЛО**.
И в самом коде висело предупреждение:

> `close_report.py:244` — *«this path has never run against a real BingX fill. The SIGN and
> MAGNITUDE MUST be sanity-checked on the first real close before the number is trusted.»*

**Я разрядил это предупреждение ДО применения**, прогнав реальную ветку против ленты биржи
на шести настоящих закрытиях:

| positionId | биржа `totalFunding` | реальная ветка | сходится |
|---|---|---|---|
| 2089316378674950146 | −0.0017454 | +0.0017450 | ✅ знак инвертирован по проекту |
| 2091564931027791874 | −0.0147663 | +0.0147660 | ✅ |
| 2091869468666064898 | +0.0000000 | +0.0000000 | ✅ |
| 2091911036454268930 | +0.0069726 | −0.0069730 | ✅ |
| 2092888692435939330 | +0.0000000 | +0.0000000 | ✅ |
| 2093955676976148482 | −0.0148357 | +0.0148360 | ✅ |

**`funding_paid == −totalFunding` до 1e-6 на всех шести.** Знак и величина верны
(`funding_paid > 0` = «заплачено», биржевой `totalFunding > 0` = «получено»).
🔴 **Честно: численно старая ОЦЕНКА тоже была точна** (−0.0149 против −0.0148357).
**Врал ЯРЛЫК «(estimated)», а не число.** Не преувеличиваю пользу правки.

## 1d. 🔴 ЗАГОЛОВОК, КОТОРЫЙ НЕЛЬЗЯ СПУТАТЬ С ТЕЛЕФОНА, И НОТИОНАЛ НА КАРТОЧКЕ

`🔚 Trade Closed` против `🧪 Virtual Trade Result` — недостаточный контраст, согласен.
**Слова REAL MONEY / PAPER идут ПЕРВЫМИ, и нотионал теперь на карточке:**

```diff
- head = '🧪 <b>Virtual Trade Result' if self.is_virtual else '🔚 <b>Trade Closed'
+ head = ('🧪 <b>PAPER — SIMULATED, NO ORDER SENT'
+         if self.is_virtual else '🔴💵 <b>REAL MONEY — Trade Closed')

- lines.append(f"⏱ Hold: {self.hold_str}   📦 Size: {self.size}")
+ _notional = (self.entry_price or 0.0) * (self.size or 0.0)
+ _mode = 'paper' if self.is_virtual else 'REAL'
+ lines.append(f"⏱ Hold: {self.hold_str}   📦 Size: {self.size} "
+              f"(${_notional:,.0f} notional, {_mode})")
```

**ТЕПЕРЬ ТЕ ЖЕ ДВЕ КАРТОЧКИ, ЧТО В ОТЧЁТЕ 18:10:**

```
🧪 PAPER — SIMULATED, NO ORDER SENT
💎 BTC/USDT:USDT LONG
📥 Entry: 64604.40   📤 Exit: 63787.10  (-1.27%)
💰 Net: -$137.3169   📊 R: -1.09R
🧾 Gross: -$126.4363   💸 Fees $9.9311 (in 4.9655 / out 4.9655)
💱 Funding: -$0.9495 (estimated)
⏱ Hold: 2h 52m   📦 Size: 0.1547 ($9,994 notional, paper)
🛡 orig SL 63787.50  ·  trail 1.264%
🏁 Close: sl
```

```
🔴💵 REAL MONEY — Trade Closed
💎 BTC/USDT:USDT SHORT
📥 Entry: 63686.00   📤 Exit: 64733.00  (-1.64%)
💰 Net: -$2.5416   📊 R: -1.02R
🧾 Gross: -$2.4081   💸 Fees $0.1477 (in 0.0738 / out 0.0738)
💱 Funding: +$0.0142
⏱ Hold: 11h 0m   📦 Size: 0.0023 ($146 notional, REAL)
🛡 orig SL 64767.10  ·  trail 1.698%
🏁 Close: sl
```

Обрати внимание: у живой карточки **исчез ярлык `(estimated)`** у фандинга — это следствие правки (b).
**Формулировку заголовка меняем одной строкой, если не нравится.**

## 1e. 🔴 НАКОПИТЕЛЬНАЯ СТРОКА — ДВА ВАРИАНТА. ЖДУ ТВОЕГО СЛОВА. НЕ ПРИМЕНЕНО НИЧЕГО.

Проблема (`main.py:429-441`): `SELECT pnl FROM trades WHERE batch_number=?` — **без фильтра режима**.

| батч | сделок | окно | сумма | что внутри |
|---|---|---|---|---|
| 1 | 30 | 05-21 → 07-03 | +$1 342.33 | чистая бумага |
| **2** | **30** | **07-04 → 08-07** | 🔴 **−$833.09** | 🔴 **бумага + живые** |
| 3 | 6 | 08-17 → 08-30 | −$4.93 | чистые живые |

**ВАРИАНТ A — РАЗДЕЛИТЬ СУММЫ ПО РЕЖИМУ.** Блок печатает две строки: «REAL n/Net» и «paper n/Net».

* **Плюс:** ни одна историческая сделка не теряется; батч №2 сразу становится читаемым
  (живая часть ≈ −$6.4 против бумажной ≈ −$827).
* **Минус:** батч №2 навсегда останется смешанным по СОСТАВУ — 30 сделок из двух разных вселенных;
  win-rate и Avg R по нему смысла не имеют ни в каком разрезе. Карточка станет на строку длиннее.
* **Цена:** ~15 строк в `_batch_running_block`, плюс тот же разрез в `_batch_summary_message`.

**ВАРИАНТ B — ЗАКРЫТЬ БАТЧ НА ГРАНИЦЕ РЕЖИМА.** Батч №2 принудительно закрывается на 2026-07-29
20:05, живые сделки открывают батч №3.

* **Плюс:** каждый батч однороден по построению; win-rate и Avg R снова означают ровно одно.
  Это тот же приём, что уже применён к границам 1R и LONGPARTIAL в каноне.
* **Минус:** **переписывает историю** — `batch_number` уже проставлен в `trades` на 30 строках,
  и их придётся переразметить. Это **изменение сохранённых значений на money-path**, а не отрисовки.
  Батч №2 станет коротким (≈24 бумажных), и «30» в заголовке `n/30` перестанет быть правдой для него.
* **Цена:** миграция + правка счётчика. Существенно рискованнее A.

> 🔴 **МОЯ РЕКОМЕНДАЦИЯ, РАЗ ТЫ ЕЁ НЕ ЗАПРАШИВАЛ, НО ОНА ДЕШЁВАЯ: ВАРИАНТ A.**
> Он ничего не переписывает и решает ровно то, что болит — **читаемость с телефона**.
> **НО НИЧЕГО НЕ ПРИМЕНЕНО, И Я ЖДУ.**

## 1f. КОНТРОЛЬ ПРИМЕНЕНИЯ

`.bak`: `virtual_trader.py.bak_cardlabel_20260830`, `close_report.py.bak_cardlabel_20260830` —
md5 совпали с оригиналами в момент снятия.

```
=== virtual_trader.py            === close_report.py
functions differing: ['_do_close']    functions differing: ['ClosedTrade.telegram']
added [] removed []                   added [] removed []
imports identical: True               imports identical: True
module-level assignments changed: []  module-level assignments changed: []
py_compile: PASS
```

**Изменились ровно две функции — те, в которых и были два call site. Больше ничего.**

🔴 **ПОДТВЕРЖДЕНО НЕТРОНУТЫМ** (`git status --porcelain config.py claude_advisor.py main.py
breakeven_worker.py` — **пусто**; значения прочитаны импортом):

| | |
|---|---|
| `SL_ATR_MULT` / `TRAIL_MULT_ATR` / `TRAIL_ATR_TF` | **2.25 / 1.6875 / 1h** |
| EMA-гейт (`_ENABLED`, `EMA_ENVELOPE_TFS`, `_REQUIRED_DIR`, `_FAIL_OPEN`) | **True / ('1h','15m') / Expanding / True** |
| каскад 21.08 (a)(b)(c) | **True / 3.0 / 60 · False** |
| `LONG_PARTIAL_ENABLED` | **False** |
| `CONFLUENCE_SCORE_THRESHOLD` | **3.0** |
| оба промпта советника | **файлы не тронуты (git clean)** |
| `EXIT_ADVISOR_DRYRUN` | **False** |
| риск-гейты (`DXY_HALT_DRYRUN`/`MACRO_BLACKOUT_MINUTES`/`RISK_PER_TRADE_PCT`/`MAX_MARGIN_PCT_PER_TRADE`) | **True / 30 / 0.02 / 0.3** |
| размер (`LIVE_FIXED_MARGIN_USDT` × `LEVERAGE`) | **30.0 × 5 = $150** |
| `WALL_TRAIL_LIVE_ENABLED` | **False** |

## 1g. 🔴 РЕСТАРТ — СТОП. ЖДУ ТЕБЯ.

**vpos 100 ОТКРЫТА.** Не перезапускаю. Правка инертна до твоего слова.
*(Замечание о риске: если служба упадёт сама, systemd поднимет её уже с новым кодом.
Правка меняет отрисовку и один сохраняемый `funding_paid` — торговых правил не трогает,
поэтому аварийный подъём под позицией не опасен, но назвать это надо.)*

---

# ЧАСТЬ 2 — 🔴 СОВЕТНИК ВЫХОДА НА ЖИВЫХ ДЕНЬГАХ. ТОЛЬКО ЧТЕНИЕ.

## 2a. ДЕСЯТЬ ЖИВЫХ ЗАКРЫТИЙ СОВЕТНИКА

| vpos | сторона | вход | выход | холд | R | **$** | upnl_r | mfe_r | giveback_r |
|---|---|---|---|---|---|---|---|---|---|
| 87 | LONG | 64 838.7 | 64 544.3 | 14.0 ч | −0.440 | **−0.8191** | −0.364 | 0.615 | +0.978 |
| 88 | SHORT | 63 643.2 | 63 810.4 | 1.0 ч | −0.296 | **−0.5311** | −0.215 | 0.076 | +0.291 |
| 89 | SHORT | 63 700.1 | 62 635.9 | 1.9 ч | +1.386 | **+2.3024** | +1.474 | 1.697 | +0.223 |
| 90 | SHORT | 62 618.4 | 62 827.1 | 2.0 ч | −0.304 | **−0.6099** | −0.239 | 0.175 | +0.414 |
| 91 | SHORT | 62 649.2 | 62 871.4 | 7.0 ч | −0.484 | **−0.6410** | −0.386 | 0.661 | +1.048 |
| 92 | LONG | 63 920.2 | 63 415.6 | 4.0 ч | −0.728 | **−1.3073** | −0.646 | 0.001 | +0.647 |
| 93 | SHORT | 64 192.9 | 64 193.0 | **10 с** | −0.137 | **−0.1479** | −0.000 | 0.000 | +0.000 |
| 96 | LONG | 78 747.4 | 78 121.0 | 1.0 ч | −0.546 | **−1.3392** | −0.485 | 0.464 | +0.949 |
| 97 | LONG | 79 764.4 | 78 570.1 | 2.0 ч | −0.796 | **−2.2852** | −0.749 | 0.116 | +0.865 |
| 98 | LONG | 79 530.0 | 79 348.4 | 5.0 ч | −0.260 | **−0.4699** | −0.181 | 0.929 | +1.110 |
| | | | | | **ΣR −2.605** | 🔴 **−$5.8481** | | | **1 победа из 10** |

**Дословные обоснования** (`trades.ai_reason`, уверенность **0.72 на всех десяти**) — все десять
приведены полностью в приложении ниже; вот две показательные:

> **vpos 96** — *«Entry thesis deteriorated: 1H confirmation still holds, but 5m I-BOS (0.7 weight)
> now fully breached by bearish OB mitigated 0m ago. Regime shifted neutral (15m/5m ADX 27.4 =
> whippy). Book imbalance flipped to 75th pct opposing (hostile). Supporting wall thinned 72→70th
> pct. Position down 0.48R with only 0.52R to stop; risk/reward unfavorable. Peak MFE 0.46R shows
> weak conviction; giveback 0.94R i…»*

> **vpos 93** — *«Entry thesis compromised. At entry, 3TF SHORT agreement (1H/15m/5m) supported
> position. NOW: 5m structure has inverted sharply—bullish breaker, bullish OB entered/within, all
> AGAINST short. … position up 0h with …»* — 🔴 **закрыто через ДЕСЯТЬ СЕКУНД после входа.**

## 2b. 🔴 КОНТРФАКТУАЛ: БЕЗ СОВЕТНИКА. 1m-свечи, `bardir`, стоп + безубыток + трейл

| vpos | факт $ | к/ф выход | чем | к/ф $ | к/ф холд | **Δ$** |
|---|---|---|---|---|---|---|
| 87 | −0.8191 | 64 028.8 | стоп | −2.0110 | 19.0 ч | **−1.19** |
| 88 | −0.5311 | 63 192.2 | трейл | **+0.8914** | 8.3 ч | 🔴 **+1.42** |
| 89 | +2.3024 | 63 136.0 | трейл | +1.1515 | 5.5 ч | **−1.15** |
| 90 | −0.6099 | 63 491.9 | стоп | −2.1541 | 35.7 ч | **−1.54** |
| 91 | −0.6410 | 63 224.6 | стоп | −1.4682 | 7.2 ч | **−0.83** |
| 92 | −1.3073 | 64 198.7 | трейл | **+0.4932** | 64.7 ч | 🔴 **+1.80** |
| 93 | −0.1479 | 64 662.1 | стоп | −1.2273 | 4.2 ч | **−1.08** |
| 96 | −1.3392 | 80 263.5 | трейл | **+2.7295** | 15.4 ч | 🔴 **+4.07** |
| 97 | −2.2852 | 78 170.3 | стоп | −3.0115 | 22.3 ч | **−0.73** |
| 98 | −0.4699 | 80 038.6 | трейл | **+0.7718** | 10.0 ч | 🔴 **+1.24** |

```
ФАКТ (советник)      : ΣR -2.605   Σ$ -5.8481   побед 1/10
БЕЗ СОВЕТНИКА        : ΣR -2.444   Σ$ -3.8347   побед 5/10
🔴 Δ                  : ΣR +0.161   Σ$ +2.0134
   советник ЛУЧШЕ на 6/10 (на $6.52)   ХУЖЕ на 4/10 (на $8.53)
```

> 🔴 **ЧИТАТЬ ИМЕННО ТАК: СОВЕТНИК ПРАВ ЧАЩЕ, НО ОШИБАЕТСЯ ДОРОЖЕ.**
> Шесть раз он спас в среднем по $1.09. Четыре раза он срезал ход, стоивший в среднем $2.13 —
> и **одна vpos 96 стоит $4.07 в одиночку** (трейл довёл бы до 80 263 против его выхода на 78 121).
> **Знак итога держат ЧЕТЫРЕ строки, а не десять.**

## 2c. 🔴 БЫЛ ЛИ ТРЕЙЛ ВООБЩЕ ВЗВЕДЁН — НЕТ, 9 ИЗ 10, РОВНО КАК НА БУМАГЕ

```
MFE >= +1R (трейл БЫЛ БЫ взведён) : 1/10  -> только vpos 89
MFE <  +1R (трейл НЕ взводился)   : 9/10
   их MFE_R: 87:0.61  88:0.08  90:0.17  91:0.66  92:0.00  93:0.00  96:0.46  97:0.12  98:0.93
```

**Бумажная книга давала 9 из 10 невзведённых. Живая даёт ровно то же — 9 из 10.**

✅ **Вывод 27.08 ВЫЖИВАЕТ на живых деньгах: советник конкурирует со СТОПОМ, а не срезает
взведённых бегунов.** Единственный взведённый случай — vpos 89 (MFE 1.70), и там советник
**обыграл трейл на $1.15**, зафиксировав +$2.30 против +$1.15.

⚠️ Но у этого вывода есть вторая половина, которой не было на бумаге: **у четырёх из девяти
невзведённых (88, 92, 96, 98) трейл всё-таки взвёлся бы ПОЗЖЕ** — контрфактуал держит их
8–65 часов против 1–5 часов у советника. **Невзведённость на момент выхода не означает,
что бегуна не было. Она означает, что советник вышел ДО того, как он появился.**

## 2d. ВЕРДИКТЫ ПРОТИВ ИЗМЕРИМЫХ ВЕЛИЧИН — **17 ИЗ 17 ЧИСЛОВЫХ УТВЕРЖДЕНИЙ ВЕРНЫ**

Каждое проверяемое число из обоснований сверено с сохранённой величиной (допуск 0.06R):

| vpos | утверждение | заявлено | факт | |
|---|---|---|---|---|
| 87 | peak MFE / gave back / stop away | 0.61 / 0.98 / 0.64 | 0.615 / 0.978 / 0.636 | ✅✅✅ |
| 91 | peak MFE / down / stop | 0.66 / 0.40 / 0.60 | 0.661 / 0.386 / 0.614 | ✅✅✅ |
| 92 | down … with zero MFE | 0.65 | 0.646 | ✅ |
| 96 | MFE / giveback / down / to stop | 0.46 / 0.94 / 0.48 / 0.52 | 0.464 / 0.949 / 0.485 / 0.515 | ✅✅✅✅ |
| 97 | down / peaked / stop away | 0.74 / 0.12 / 0.26 | 0.749 / 0.116 / 0.251 | ✅✅✅ |
| 98 | rejected peak by / sitting / cushion | 1.11 / 0.18 / 0.82 | 1.110 / 0.181 / 0.819 | ✅✅✅ |

```
🔴 числовых утверждений верно: 17/17 = 100%   (бумажный аудит 27.08 давал 93%)
```

> 🔴 **И ЭТО ВАЖНЕЕ, ЧЕМ ВЫГЛЯДИТ. СОВЕТНИК НЕ ГАЛЛЮЦИНИРУЕТ.** Он видит `upnl_r`, `mfe_r`,
> `giveback_r` и расстояние до стопа **точно** и цитирует их без единой ошибки на живых деньгах.
> **Он не ошибается в ФАКТАХ — он ошибается в РЕШЕНИИ.** Его повторяющийся довод —
> *«giveback большой, до стопа близко, risk/reward неблагоприятен»* — арифметически верен и
> в четырёх случаях из десяти привёл к выходу прямо перед ходом в нужную сторону.
> **Чинить надо не его зрение, а его порог.** Здесь я это только называю.

## 2e. ХОЛД

```
советник, медиана       :  2.01 ч
контрфактуал, медиана   : 12.66 ч
```

**Шестикратная разница подтверждена на живых деньгах.** Стоит ли она денег — **на десяти
наблюдениях неразрешимо**: ранний выход спас $6.52 и стоил $8.53. **Итог −$2.01 против советника
держится на четырёх строках.**

## 2f. 🔴 ЭФФЕКТИВНОЕ n — ЧЕСТНО

**ДЕСЯТЬ ЗАКРЫТИЙ — ЭТО НЕ ВЫБОРКА. РАНЖИРОВАТЬ НА НИХ НЕЛЬЗЯ, И Я НЕ БУДУ.**

* 10 наблюдений, из них **знак итога определяют 4**;
* одна строка (vpos 96, $4.07) — **двукратно больше** итоговой разницы $2.01;
* нотионал **$143–150**: весь спор идёт о **двух долларах** на счёте в $503;
* режимный срез: ADX<25 **n=9**, ADX≥25 **n=1** — формально «обе ноги заполнены»,
  фактически **вторая нога пуста**;
* 10 наблюдений **физически не заполняют 12 окон** — стабильность знака недостижима **по построению**.

**ПРЯМО, КАК ПРОСИЛ: СОВЕТНИК МОЖЕТ БЫТЬ ПРИЧИНОЙ, И ДЕСЯТЬ ЖИВЫХ ЗАКРЫТИЙ ЭТОГО НЕ ДОКАЖУТ.**

### И ЧТО ЭТИ ДЕСЯТЬ ГОВОРЯТ ОПИСАТЕЛЬНО, В ДОЛЛАРАХ — ПОТОМУ ЧТО ЭТО ЖИВЫЕ ДЕНЬГИ

| факт | значение |
|---|---|
| закрытий советника из 15 реальных | **10 (67 %)** |
| его результат | **−$5.85** из общих **−$9.49** = **62 % всего убытка** |
| без него, тот же период | **−$3.83** |
| **разница** | 🔴 **$2.01 — 21 % всего реального убытка Титана** |
| его винрейт | **1 из 10** |
| винрейт без него | **5 из 10** |
| дороже всего обошлось | **vpos 96, $4.07** |

**Это описание, а не приговор. Но если завтра надо действовать, действовать надо по нему,
а не по бумажной книге.**

## 2g. ЧЕТЫРЕ КОНТРОЛЯ — ТРИ ПРОВАЛЕНЫ, НАЗЫВАЮ ПРЯМО

| контроль | результат | вердикт |
|---|---|---|
| **Bonferroni** | объявлен в шапке, 4 гипотезы, **α = 1.25 × 10⁻²** | ✅ объявлен ДО чисел |
| **Стабильность знака** | без советника лучше на **4/10**, двусторонний биномиальный **p = 0.754**; 12 окон **недостижимы** на 10 наблюдениях | 🔴 **ПРОВАЛ** |
| **Режим, обе ноги** | ADX<25 **n=9**, ADX≥25 **n=1** | 🔴 **ФОРМАЛЬНО ДА, ФАКТИЧЕСКИ НЕТ** |
| **Независимая выборка** | **НЕТ.** Все 10 — одна книга, hold-out отсутствует | 🔴 **НЕ СУЩЕСТВУЕТ** |

---

# ЧАСТЬ 3 — ЗАПИСАНО В КАНОН, НЕ РАССЛЕДОВАНО

Добавлен раздел **§0.FIRSTLIVE** в `OPEN-ITEMS.md`:

```
positionId 2082558078264504322   SHORT BTC-USDT
открыта 2026-07-29 20:05:13 UTC   закрыта 2026-07-29 21:29:21 UTC
размер 0.0046 BTC = $292.14 нотионал   <- 2.0x от заданных $150
netProfit -0.2645 USDT
   20:05:13  TRADING_FEE  Position opening fee  -0.07303
   20:05:14  TRADING_FEE  Position opening fee  -0.07304   <- ВТОРОЙ ОРДЕР, +1 секунда
   21:29:21  REALIZED_PNL Close Short           +0.02760
   21:29:21  TRADING_FEE  Position closing fee  -0.14605   <- ДВОЙНАЯ
```

🔴 **ФРАЗА, КОТОРУЮ КАНОН ТЕПЕРЬ ТРЕБУЕТ ЦИТИРОВАТЬ:
«ЛЮБОЙ ПОДСЧЁТ ЖИВОЙ ТОРГОВЛИ ПО `virtual_positions` ЗАНИЖЕН НА ОДНУ СДЕЛКУ И НА $0.2645.»**
Это относится ко всем цифрам моих отчётов 15:00 и 17:20.

**Поправка к цене, потому что в постановке она неточна:** «$0.29» — это **ПОЛНАЯ** комиссия сделки
($0.29212), а не переплата. Одиночный правильный ордер на $150 заплатил бы ≈ **$0.1460**.
🔴 **Переплата из-за дублирования ≈ $0.1461.** Полный нетто сделки: **−$0.2645**.

**Почему никто не заметил:** `RECONCILE-XDB` сверяет только **ОТКРЫТЫЕ** позиции, а эта закрылась
за 8 часов до ближайшего рестарта. Сходимость: 14 строк БД = −9.2228; **−9.2228 + (−0.2645) = −9.4873**
против биржевых **−9.4875**.

⚠️ **Дальше не копал — по твоей инструкции.**

---

# ПРИЛОЖЕНИЕ · ВСЕ ДЕСЯТЬ ОБОСНОВАНИЙ ДОСЛОВНО

*(`trades.ai_reason`, `ai_confidence = 0.72` на всех десяти; поле обрезано схемой на 400 символах)*

**87** · *Entry thesis broken. 15m/5m shifted to BEAR (was BULL). ADX15m=26.2 confirms momentum reversal. Order book flipped: supporting wall collapsed (5.0x→0.0x), opposing wall reinforced (7.4x, 70th pct). Imbalance at 90th pct (extreme) now opposes position. Peak MFE +0.61R gave back 0.98R. Regime changed from TREND to BEAR at multiple TFs. Stop only 0.64R away; risk/reward unfavorable. Book depth (16th*

**88** · *Entry thesis has deteriorated significantly. 15m reversal-up weight (1.0) now actively opposes the SHORT, and 5m structure has flipped bullish (new imbalance, I-CHOCH, OB creation all against position). ADX15m spiked to 36.5 indicating strong directional conviction—upward. Supporting wall thinned 5.7→4.8 while opposing wall strengthened (62nd pct). 1h regime shifted to neutral/bull. Position is -0*

**89** · *Entry thesis deteriorated. 5m regime reversed sharply: 4 consecutive bullish OBs/breakers contradict original bearish OB setup. 15m/5m SHORT agreement dissolved—both now neutral. ADX15m spiked to 31.1 (volatility regime change), while ADX1h falling (trend weakening). Book imbalance at 79th pct (extremely bid-heavy) is unstable vs entry's 93pct baseline. Supporting wall thinned 5.6→5.0. Profit lock*

**90** · *Entry thesis has degraded significantly. 5m/15m shifted to neutral (were SHORT/HyperWave at entry); position now sits within bullish OBs repeatedly (16m, 10m, 6m, 1m)—structural rejection of short thesis. ADX15m spiked to 49.5 (entry was 23.0) on neutral regime, suggesting momentum exhaustion rather than continuation. Supporting wall thinned 4.6→4.5, opposing wall equally thin (19th pct). Unrealis*

**91** · *Entry thesis collapse: 15m was opposing at entry (HyperWave OS LONG vs SHORT trade); now 15m=bull, 5m=neutral with bullish structure (OB entered 11m ago, liquidity grab 6m ago). Regime shifted: 15m/5m now bullish vs bearish at entry. Imbalance flipped 0.56→0.48 (less bid-heavy). Position down 0.40R with peak MFE 0.66R showing exhaustion. Book now ordinary (37th-42nd pct depth/imbalance). Stop 0.60*

**92** · *Entry thesis collapse across multiple timeframes. 15m HyperWave already opposed at entry; now 15m/5m both bearish with fresh I-BOS/OB against long. ADX declining (27→22.2 1h, 36.6→18.2 15m) signals weakening trend. Order book imbalance flipped to 85th pct (extreme selling pressure), opposing wall now x6.8 vs supporting x5.8. Price rejected at entry level, down -0.65R with zero MFE, suggesting no c*

**93** · *Entry thesis compromised. At entry, 3TF SHORT agreement (1H/15m/5m) supported position. NOW: 5m structure has inverted sharply—bullish breaker, bullish OB entered/within, all AGAINST short. 15m/5m both bear but 5m rejection is acute. Book imbalance at 93rd pct (genuine thickness on bid side) contradicts entry's bid-heavy rationale. ADX remains low (12.0) but no momentum build; position up 0h with*

**96** · *Entry thesis deteriorated: 1H confirmation still holds, but 5m I-BOS (0.7 weight) now fully breached by bearish OB mitigated 0m ago. Regime shifted neutral (15m/5m ADX 27.4 = whippy). Book imbalance flipped to 75th pct opposing (hostile). Supporting wall thinned 72→70th pct. Position down 0.48R with only 0.52R to stop; risk/reward unfavorable. Peak MFE 0.46R shows weak conviction; giveback 0.94R i*

**97** · *Entry thesis broken. 1H confirmation no longer valid (now neutral 15m/5m bear). Book imbalance flipped to 87th pct against position (opposing wall 78th pct, supporting thinned). Regime shifted to bear 5m with ADX rising. Price -0.74R, peaked only +0.12R. Recent 5m structure hostile (bearish OB, I-BOS). Stop only +0.26R away with unfavorable risk/reward. MTF alignment collapsed.*

**98** · *Entry thesis degraded: 1H trend signal expired (TTL=360min, set 9.3h ago); 15m HyperWave aged 75min; 5m bullish OB no longer current. Regime shifted: 15m now bearish, 5m neutral vs all-bull at entry. Price rejected peak by 1.11R, sitting -0.18R with only 0.82R cushion. Book structure ordinary (61–66th pct), no edge. ATR volatility +7.1% suggests chop. Multiple bearish OBs in recent structure contr*

---

**Происхождение:** `trades.db` Титана только на чтение; 1m-свечи BTC/USDT:USDT с BingX,
144 866 баров, 0 разрывов; стенд — тот же, что валидирован 24/27 в отчёте 15:00; лента фандинга
и `positionHistory` — с биржи по ключу бота, только чтение; `ai_reason` дословно из БД.
Правка: `.bak` сняты, AST-диф — ровно две функции, `config.py` не тронут, коммит `a0c77f2`
**запушен** (`git status -sb` чист, без `ahead`). `openitems_guard` **EXIT=0** после правки канона.
🔴 **НЕ ПЕРЕЗАПУЩЕНО. vpos 100 открыта. Mercury-SOL не прочитан.**
