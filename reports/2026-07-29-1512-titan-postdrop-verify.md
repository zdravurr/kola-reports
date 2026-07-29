# titan-postdrop-verify

_2026-07-29 15:12 UTC_

---

# ТИТАН — ПРОВЕРКА ПОСЛЕ ОБРЫВА СЕССИИ (29.07.2026, 15:10 UTC)

**РЕШЕНИЕ: НИЧЕГО НЕ ПОТЕРЯНО. Все 7 пунктов чисты. Титан закрыт, следующая сессия — Mercury-SOL.**

Сессия оборвалась после отчёта 13:58. Проверка read-only, ни одного изменения не внесено.
Маркер свежести этого снимка: `POSTDROP-VERIFY-29JUL-1510`.

---

## 1. GIT — ЧИСТО, В СИНХРОНЕ

```
git status --porcelain   -> (пусто)
HEAD                     -> 41c4a4d637ddd35dbf8492daf39a5b29f286dbbf
branch                   -> ## main...origin/main   (без ahead/behind)
origin/main              -> 41c4a4d637ddd35dbf8492daf39a5b29f286dbbf   (ИДЕНТИЧЕН HEAD)
remote                   -> https://github.com/zdravurr/bingx-bot.git
```
Рабочее дерево = HEAD = origin/main. Незакоммиченного и неотправленного нет.

## 2. titan.service — ЖИВ, БЕЗ ЕДИНОЙ ОШИБКИ

```
ActiveState/SubState  -> active / running
MainPID               -> 4081846 (master), 4081957 (worker)
ActiveEnterTimestamp  -> Wed 2026-07-29 13:49:47 UTC
uptime на момент проверки -> 1 ч 19 мин
journalctl -u titan -p err --since 13:49:47  -> "-- No entries --"  (НОЛЬ ошибок)
```
Сервис стартовал через **4 секунды после коммита 41c4a4d** (коммит 13:49:43 → рестарт 13:49:47).

**Рестарт — не единственная улика, проверена и загрузка кода** (урок «фикс на диске ≠ фикс в
работе»): mtime всех модулей СТРОГО РАНЬШЕ старта процесса, значит в памяти лежит коммит, а не
предыдущая версия.
```
config.py         2026-07-26 22:05:49   <  старт 13:49:46 ✓
claude_advisor.py 2026-07-29 13:44:16   <  старт 13:49:46 ✓
main.py           2026-07-29 13:13:30   <  старт 13:49:46 ✓
```

## 3. ПОЗИЦИЯ vpos 85 — ЦЕЛА, ВКЛЮЧАЯ entry_tiers_json

```
id                    = 85
symbol                = BTC/USDT:USDT
position_side / side  = LONG / buy
status                = open      (единственная открытая позиция в таблице)
initial_fill_price    = 64604.4
sl_price              = 63787.5
original_sl_price     = 63787.5   (стоп НЕ двигался)
trail_pct             = 1.264
water_mark            = 64674.1
partial_taken         = NULL      (частичного взятия НЕ было)
realized_partial_usdt = NULL
opened_at             = 2026-07-29T13:50:18.504082+00:00
filled_legs           = 1 нога: price 64604.4, size 0.1547, fee 4.99715034, kind=entry
pending_dca_limits    = {"breakeven_applied": false, "exit_advisor_last_ts": 1785336633.067512}
```
Позиция открыта уже ПОСЛЕ рестарта (13:50:18) — то есть её вёл текущий, пропатченный процесс.
Безубыток не применён, частичка не бралась, стоп исходный. Ничего не тронуто обрывом сессии.

**entry_tiers_json — НА МЕСТЕ**, в строке входа `trades.id = 19468` (13:50:11), длина 810 байт,
все три яруса присутствуют (это ровно то, что дал коммит 7285c5d):
```
1H : "Smart Trail Bullish", weight 0.9, TREND, age 5.8h, counted_by_gate=true,
     direction = "direction withheld (AI_ADVISOR_HIDE_1H)"
15m: "HyperWave Signal Down", SHORT, weight 0.7, MOMENTUM, age 2.8h
5m : (присутствует, хвост записи)
```

## 4. ТРИ ОТРЕДАКТИРОВАННЫХ СЕНСОРА — НА ДИСКЕ, КРОН ЦЕЛ

```
-rwxr-xr-x 2950  Jul 29 13:45  titan_bull_regime_watch.sh
-rwxr-xr-x 4886  Jul 29 13:48  titan_regime_flat_high_adx_watch.sh
-rwxr-xr-x 6221  Jul 29 13:48  titan_chop_short_flat_gap_watch.sh
```
Содержимое — сегодняшнее, правки коммита 41c4a4d видны В ФАЙЛАХ, не только в сообщении коммита:
- `titan_regime_flat_high_adx_watch.sh:41` → `# EXPIRES 2026-09-30. If N has not reached THRESHOLD by then, DELETE THIS SENSOR AND ...`
- `titan_chop_short_flat_gap_watch.sh:47`  → тот же EXPIRES-блок
- `titan_bull_regime_watch.sh:23`          → `STATE="/root/titan-bot/.state_bull_regime_watch"`
- **Состояние edge-триггера существует и взведено:** файл `.state_bull_regime_watch` (5 байт,
  13:45) содержит `bull`. Значит следующий ежедневный запуск ПРОМОЛЧИТ и заорёт только на смене
  режима — ровно то поведение, ради которого делалась правка.

Строки крона на месте, все три:
```
17 8 * * *  /root/titan-bot/titan_bull_regime_watch.sh          >> /var/log/titan_bull_regime_watch.log 2>&1
53 8 * * *  /root/titan-bot/titan_regime_flat_high_adx_watch.sh >> /var/log/titan_regime_flat_high_adx_watch.log 2>&1
29 8 * * *  /root/titan-bot/titan_chop_short_flat_gap_watch.sh  >> /var/log/titan_chop_short_flat_gap_watch.log 2>&1
```

### ⚠️ ОДНА НАХОДКА (НЕ потеря сессии, но сказать обязан)
Эти три `.sh` **не находятся под гитом**. `.gitignore` строка 1 = `*` (репо-аллоулист: всё
игнорируется, файлы добавляются принудительно). Проверка:
```
git check-ignore -v ... -> .gitignore:1:*   (все три)
git log -- <три файла>  -> (пусто — никогда не коммитились)
git ls-files titan-bot/ -> 38 файлов, ни одного .sh-вотчера
```
То есть «git status чисто» их чистоту НЕ доказывает, и доказательством служит проверка выше
(mtime + маркеры EXPIRES/STATE в теле + state-файл). Ничего не потеряно — но правки этих
сенсоров живут ТОЛЬКО на диске и в ежедневный git-бэкап не попадают. Это давняя, не сегодняшняя
дыра: под гитом нет НИ ОДНОГО `.sh`-вотчера (`titan_volfloor_data_watch.sh` тоже). Питоновые
сенсоры (`daily_trend_cohort_sensor.py`, `sensor_events.py`) отслеживаются нормально.
**Ничего не менял — решение по force-add за Боссом.**

## 5. EXIT-ADVISOR — БЬЁТ ПО ЧАСАМ, ПРОПУСКОВ НЕТ

```
13:50:30  [EXIT-ADVISOR-DRYRUN] trigger=hourly BTC LONG close=False conf=0.72
14:50:38  [EXIT-ADVISOR-DRYRUN] trigger=hourly BTC LONG close=True  conf=0.72
```
Интервал 60 мин 08 сек — кадэнс держится. Отметка в самой позиции подтверждает независимо:
`exit_advisor_last_ts = 1785336633.07 = 2026-07-29T14:50:33Z`. Следующая консультация ~15:50 UTC.
Обрыв сессии на цикл не повлиял: консультация 14:50 прошла уже ПОСЛЕ падения сессии.

Содержание вердикта 14:50 (dryrun — **позиция НЕ закрывалась**, только записано):
«Entry thesis broken: 15m HyperWave SHORT opposes price action; regime shifted to bear
(ADX1h 49.1, 15m/5m bear); price down -0.61R in 1h with CHOCH + bearish structural breaks».

## 6. ФЛАГИ В РАНТАЙМЕ = ЗАПИСЬ 41c4a4d

Флаги живут в `config.py` (не в env — в окружении процесса ни одного из них нет, что и ожидается).
`git diff HEAD -- titan-bot/` пуст ⇒ config.py на диске ИДЕНТИЧЕН коммиту 41c4a4d, а mtime
config.py (26.07 22:05) РАНЬШЕ старта процесса ⇒ рантайм читает именно его.

Значения на диске = в коммите:
```
LIVE_TRADING_ENABLED            = False      EXIT_ADVISOR_PAPER_ENABLED    = True
FIXED_NOTIONAL_MODE             = True       EXIT_ADVISOR_DRYRUN           = True
LONG_PARTIAL_ENABLED            = True       EXIT_ADVISOR_ON_15M_CONFIRM   = True
HTF_CASCADE_ENABLED             = True       EXIT_ADVISOR_HOURLY           = True
HTF_TOLERATE_NEUTRAL            = True       AI_ADVISOR_HIDE_1H            = True
HTF_NEUTRAL_REQUIRE_15M_AGREE   = True       EQH_EQL_SMART_TP_ENABLED      = True
HTF_NEUTRAL_REQUIRE_15M_DRYRUN  = False      SMART_EXIT_DRYRUN_ENABLED     = True
WALL_TRAIL_LIVE_ENABLED         = False      WALL_ANCHOR_DRYRUN_ENABLED    = True
DXY_HALT_DRYRUN                 = True       TREND_REVERSAL_EXIT_DRYRUN    = True
FILTER_ENFORCEMENT_DRYRUN       = True       ADAPTIVE_TRAIL_RECOMPUTE_DRYRUN = True
POST_ENTRY_RECHECK_ENABLED      = True       MICROSTRUCTURE_ENABLED        = True
ORDERBOOK_COLLECTOR_ENABLED     = True       LEARNING_ENABLED              = True
EXCURSION_LOGGING_ENABLED       = True       SENSOR_EVENT_LOGGING_ENABLED  = True
```

**Проверено не по файлу, а по ЖИВОМУ логу** — флаги печатают себя сами (15:00–15:05 UTC):
```
HTF_WOULD_PASS (tolerate-NEUTRAL) LONG 1H=NEUTRAL 15m=NEUTRAL 5m=LONG ... enabled=True
HTF_NEUTRAL_15M_WOULD_BLOCK ... reason=1H_neutral_15m_not_confirming dryrun=False
[EXIT-ADVISOR-DRYRUN] trigger=hourly ...
```
`enabled=True` ⇔ HTF_TOLERATE_NEUTRAL, `dryrun=False` ⇔ HTF_NEUTRAL_REQUIRE_15M_DRYRUN=False,
`AI_ADVISOR_HIDE_1H` виден в entry_tiers_json как «direction withheld». Совпадает с записью.

**Удалённая строка Long/Short ratio — проверена по факту, а не по коду:**
`journalctl -u titan --since 13:49:47 | grep -ci "Long/Short ratio"` → **0**. Строки, которая всю
жизнь бота печатала `n/a`, в промпте больше нет.

## 7. MERCURY-SOL — ЖИВ И НЕ ТРОНУТ

```
mercury-sol.service                     active / running
ActiveEnterTimestamp -> Tue 2026-07-21 06:39:33 UTC   (аптайм 8 суток, БЕЗ рестартов)
mercury-sol-optimizer-listener.service  active / running
mercury-sol-optimizer.service           inactive/dead  (по расписанию — норма)
journalctl -u mercury-sol -p err --since 13:00 -> "-- No entries --"
PIDs 1793275 (master) / 1794078 (worker) — те же, что и до сессии
```
За сегодня в каталоге меняются ТОЛЬКО данные, ни одного файла кода:
`oi_cache.json` (15:00) и `trades.db` (15:08) — то есть бот пишет, а его никто не правил.
Кроновые строки SOL (`sol_downtrend_regime_watch.sh` 23:8, `sol_uptrend_regime_watch.sh` 47:8,
`mercury_sol_prior_move_logger.py` каждые 6ч) на месте.

---

## ИТОГ

| # | Пункт | Вердикт |
|---|-------|---------|
| 1 | git чист, HEAD, синхрон с origin | ✅ 41c4a4d = origin/main, дерево чисто |
| 2 | titan.service, аптайм, ошибки с 13:49:47 | ✅ active 1ч19м, ошибок 0 |
| 3 | vpos 85: вход, стоп, частичка, entry_tiers_json | ✅ цела, стоп исходный, частички не было, tiers 810б |
| 4 | Три сенсора на диске + крон | ✅ на месте (не под гитом — см. находку) |
| 5 | Exit-advisor по часам с 13:58 | ✅ 13:50 и 14:50, интервал 60м08с |
| 6 | Флаги в рантайме = запись 41c4a4d | ✅ совпали, подтверждено живым логом |
| 7 | Mercury-SOL жив и не тронут | ✅ аптайм 8 суток, правок кода нет |

Потерь нет. Титан закрыт. Единственный открытый вопрос на решение Босса — брать ли три
`.sh`-вотчера под гит (сейчас их правки существуют в одном экземпляре, на диске).
