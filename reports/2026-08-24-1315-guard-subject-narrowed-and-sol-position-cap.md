# ПРЕДМЕТ СТОРОЖА СУЖЕН · И НАЙДЕН КОРЕНЬ `position-cap check failed`

**2026-08-24 13:15 UTC** · Два дела в одном проходе. Часть 1 — сторож (разблокировка).
Часть 2 — Mercury-SOL, отказ проверки лимита позиций.
🔴 **Титан не тронут:** ни байта в его торговом коде и конфиге; живой эксперимент с 21.08 19:44 не задет.

---
---

# ЧАСТЬ 1 — `openitems_guard`: предмет сужен

## 1.1 Что изменено — ровно одна строка сравнения

Было (`tools/openitems_guard.py`, `runtime_head()`):

```python
out = subprocess.run(['git', '-C', REPO_DIR, 'rev-parse', '--short', 'HEAD'], ...)
```

Стало:

```python
SUBJECT_PATH = 'titan-bot/'
out = subprocess.run(
    ['git', '-C', REPO_DIR, 'log', '-1', '--format=%h', '--', SUBJECT_PATH], ...)
```

Плюс: старое значение сохранено как `runtime_repo_head()` и **печатается для контекста, но
не сравнивается**; текст расхождения назван по новому предмету; в докстринге модуля и функции
записана причина. `.bak`: `tools/openitems_guard.py.bak`.

Вывод теперь показывает оба числа, и видно, какое из них судит:

```
  titan-bot HEAD : 4a1786c   <- the SUBJECT, this is what is compared
  repo HEAD      : 4a1786c   (context only, NOT compared)
```

## 1.2 🔴 ЭТО НЕ ОСЛАБЛЕНИЕ — доказано ИСПОЛНЕНИЕМ, четырьмя способами

**(i) Коммит ВНЕ `titan-bot/` больше не роняет сторожа.** На одном и том же дереве, на одном и том
же каноне, **без единой правки документа**:

```
### OLD guard (backup) on the SAME tree:
  runtime HEAD   : 8de7ef4
🔴 1 MISMATCH(ES)   HEAD  doc='a7e7b46'  runtime='8de7ef4'
OLD EXIT=1

### NEW guard on the SAME tree:
  titan-bot HEAD : a7e7b46   <- the SUBJECT
  repo HEAD      : 8de7ef4   (context only)
✅ header and current-state table agree with runtime.
NEW EXIT=0
```

🔴 Обратите внимание, что это значит: под новым определением шапка канона **уже была верна**.
Утреннее срабатывание было чистым шумом, и это не рассуждение, а разница двух выходов.

**(ii) и (iii) Изолированный репозиторий: два не-титановских коммита не сдвигают предмет, коммит в
`titan-bot/` — сдвигает и роняет проверку.** Настоящий git, настоящий код сторожа:

```
commits: A(titan)=3463824  B(infra)=6e9bb72  C(infra)=9116eb1
(ii-a) after TWO non-titan commits: subject=3463824  repo HEAD=9116eb1
        subject still == A(titan)? True    <- outside commits do NOT move it
(ii-b) after a titan-bot/ commit D=ed72105: subject=ed72105
        subject MOVED off A? True   moved to D? True   <- drift IS caught
(ii-c) full check() ... 🔴 1 MISMATCH ... check() EXIT=1   <- must be 1
ALL THREE ASSERTIONS PASSED
```

Изменённый файл в (ii-b) — `titan-bot/config.py`, `SL_ATR_MULT 2.25 → 9.99`, т.е. ровно тот класс
дрейфа, ради которого сторож написан.

**(iv) Живьём и без подстройки:** коммит самой правки сторожа (`4a1786c`, внутри `titan-bot/`)
сдвинул предмет, и сторож **отказал** этому документу, пока шапка не была обновлена:

```
🔴 1 MISMATCH(ES)   HEAD  doc='a7e7b46'  runtime='4a1786c'
                    header commit is stale vs the last titan-bot/ commit
EXIT=1
```

## 1.3 Канон обновлён, и ПОЧЕМУ записано В САМОМ КАНОНЕ

Шапка `reports/OPEN-ITEMS.md` теперь: **HEAD `4a1786c`**, с явной оговоркой, что это
**инструментарий аудита**, а последний коммит, менявший **торговое поведение** Титана, по-прежнему
**`a7e7b46`** (SOL-PORT), и живой эксперимент на нём не задет. Рядом — таблица трёх срабатываний
с нулевыми диффами, все четыре доказательства и **известный остаток**: сторож лежит `titan-bot/tools/`,
т.е. **внутри собственного предмета**, поэтому правка сторожа двигает то, что он проверяет.
Записано прямо, чтобы будущий читатель не решил, что сдвинулся код Титана.
`.bak`: `reports/OPEN-ITEMS.md.bak`.

## 1.4 Остальные десять значений — сверены живым `import config`, НЕ изменились

```
LIVE_TRADING_ENABLED=True   ORDER_ADAPTER_LIVE=True   SL_ATR_MULT=2.25  TRAIL_MULT_ATR=1.6875
CONFLUENCE_SCORE_THRESHOLD=3.0   CONFLUENCE_FLAT_THRESHOLD=3.0   EXIT_ADVISOR_DRYRUN=False
AI_ADVISOR_HIDE_1H=False   EQH_EQL_SMART_TP_ENABLED=False   EMA_ENVELOPE_GATE_ENABLED=True
MAX_POSITIONS_PER_SIDE=1
```

`git diff a7e7b46..8de7ef4 -- titan-bot/config.py` = **0 байт**. Дрейфа не было.

## 1.5 Сторож — EXIT 0

```
openitems_guard — canon: .../reports/OPEN-ITEMS.md
  titan-bot HEAD : 4a1786c   <- the SUBJECT, this is what is compared
  repo HEAD      : 4a1786c   (context only, NOT compared)
  watched values : 11

✅ header and current-state table agree with runtime.
EXIT=0
```

Коммиты: `4a1786c` (сторож, `/root`) · `dbb54ba` (канон, kola-reports).

---
---

# ЧАСТЬ 2 — MERCURY-SOL: почему отказывало чтение лимита

## 2.1 🔴 КОРЕНЬ, одной фразой

**Чтение ОБЁРНУТО в `tor_retry` — но эта обёртка ретраит ТОЛЬКО 403.** Первая же строка модуля
говорит это прямо: *«Timeouts / connection errors are NOT retried»*, и код это исполняет:

```python
except Exception as e:
    if not is_403_block(e):
        raise                 # <- таймаут выходит отсюда, НЕ СДЕЛАВ НИ ОДНОЙ ПОПЫТКИ
```

Отказы были **не 403**. Значит у этого чтения было **ноль** попыток на ту поломку, которая
у него реально случилась. Гипотеза «голый вызов без обёртки» — **неверна**: обёртка есть, и для
403 она работает (за 2.7 суток `positions.riskcheck` **7 раз** успешно ретраился через свежий
выход). Дефект тоньше и хуже: обёртка стоит, но не покрывает нужный класс.

## 2.2 🔴 Ошибка — дословно

Пять записей за всю историю. Первая называет причину сама:

```
2026-08-02 01:45:02  LONG  (id=15066)
position-cap check failed (fail-closed): bybit {"retCode":10002,"retMsg":"invalid request,
please check your server timestamp or recv_window param: req_timestamp[1785635125666],
server_timestamp[1785635132229],recv_window[5000]", ...}
```

Остальные четыре — **голый URL и больше ничего**:

```
position-cap check failed (fail-closed): bybit GET
https://api.bybit.com/v5/position/list?symbol=SOLUSDT&limit=200&category=linear
```

Эта форма не загадочна, она **построена ccxt**: `ccxt/base/exchange.py`, `Exchange.fetch()`,
строка 97 — `details = ' '.join([self.id, method, url])`, и строка 98 — `raise RequestTimeout(details)`.
Тот же `details` дают `NetworkError` (обрыв/сброс соединения). **403 сюда не попадает** — у 403
в тексте есть тело ответа, по нему `is_403_block()` его и ловит. Голый URL ⇒ **транспорт, не венью**.

## 2.3 🔴 recvWindow — НЕ регрессировал. Проверено на ОБОИХ клиентах живьём

```
PRIMARY  recvWindow = 20000   timeout(ms) = 10000
ISO/retry recvWindow = 20000   timeout(ms) = 10000        <- построен настоящим iso_exchange()
ccxt bybit DEFAULTS  recvWindow = 5000    timeout(ms) = 10000
```

И эмпирически: **0 (ноль) ошибок `10002` за 2.7 суток журнала**. Единственный `10002` в истории —
02.08, т.е. **до** подъёма окна 09.08. Настройка пережила. Это не она.

## 2.4 🔴 ЧТО ЭТО НА САМОМ ДЕЛЕ — измерено

`timeout` никто никогда не задавал, значит работает **умолчание ccxt = 10 000 мс**. Замер
`fetch_positions(['SOL/USDT:USDT'])` через Tor, n=15:

```
  1   8305 ms  ok      <- ХОЛОДНАЯ цепь
  2    414 ms  ok
  ... 3–15: 328–450 ms
  min=328  p50=343  p90=450  max=8305 ms
  запас до потолка 10 000 мс:  1 695 мс
```

**Вот и весь механизм.** На тёплой цепи чтение стоит ~343 мс. На холодной/деградировавшей —
8,3 секунды, в 1,7 с от потолка. В брауне оно потолок пересекает, ретрая нет, вход отказан.

Оба отказа 24.08 стоят ровно на этом: **разница между предыдущей строкой лога и строкой отказа —
10 секунд** (00:45:47 → 00:45:57; 11:40:30 → 11:40:41). Это срабатывание таймаута, а не венью.

**И контекст в тот момент — убийственный.** 11:40, за 30 секунд вокруг отказа, **семь других
чтений выжили через свежий выход**:

```
11:40:13  retried ohlcv.signal_5m via fresh exit → ok
11:40:15  retried tape.trades      via fresh exit → ok
11:40:16  retried ticker.spread    via fresh exit → ok
11:40:20  /v5/market/open-interest HTTP 403 — rotating Tor exit … recovered
11:40:25  retried ohlcv.signal_4h  via fresh exit → ok
11:40:28  retried ohlcv.signal_1h  via fresh exit → ok
11:40:30  retried ohlcv.signal_15m via fresh exit → ok
11:40:41  🔴 risk_check positions fetch failed (fail-closed): bybit GET …/v5/position/list…
11:40:41  retried ticker.observatory via fresh exit → ok
```

Поллер и соседи выживают не потому, что у них лучше политика — **политика у всех одна и та же**.
Они выживают потому, что у них есть **второй шанс**: следующий тик, запасной OKX, повтор свечей.
У проверки лимита второго шанса нет — её спрашивают ОДИН раз внутри решения о входе.
**Одна политика, разная ЦЕНА ошибки.**

## 2.5 Здоровье Tor за окно (2.7 суток)

| метрика | сейчас | базис (~2 суток) | вывод |
|---|---|---|---|
| SOCKS-ретраи | **1147** (~425/сут) | ~285 / 2 сут (~142/сут) | 🔴 **~3× хуже базиса** |
| CloudFront 403 | **30** (~11/сут) | ~26 / 2 сут (~13/сут) | в норме |
| `ConnectTimeoutError` | 10 | — | брауны связи |
| ошибки `10002` | **0** | — | окно в порядке |

Ключевая раскладка — все «голые» (не-403) отказы чтений за окно, **всего 8**:

```
  3  /v5/market/tickers        -> есть запасной OKX          -> цена 0
  2  /v5/market/kline          -> повтор на следующем тике   -> цена 0
  1  /v5/market/recent-trade   -> необязательное обогащение  -> цена 0
  2  /v5/position/list         -> ВТОРОГО ШАНСА НЕТ          -> 🔴 ДВА ОТКАЗАННЫХ ВХОДА
```

Один и тот же сбой бьёт по восьми чтениям; шесть поглощаются бесследно, два попадают в
единственное чтение, где отказ **окончателен**.

## 2.6 Частота, и с каких пор

| окно | случаев |
|---|---|
| последние 24ч | **2** (из 238 строк) |
| последние 7 сут | **2** (из 1542) |
| с боевого флипа 07.08 | **3** (из 4394) |
| за всю историю | **5** (из 20 813) |

**Первый случай — 2026-08-02 01:45:02.**

🔴 **Это НЕ новое и НЕ «только теперь дошло до Telegram».** Ветка fail-closed добавлена
**2026-06-08 ~16:50** (есть в `main.py.bak_D2_spreadgate_20260608`, нет в
`main.py.bak_D1_failclosed_20260608`) — на **два месяца раньше**, чем 10.08 из постановки задачи.
Телеграм-карточка `RISK HALT` в этой же ветке существует **минимум с 2026-06-06** и с тех пор не
менялась ни разу — проверено по всей цепочке бэкапов `main.py`. Путь алерта не менялся.
Оно просто срабатывало пять раз за два с половиной месяца.

## 2.7 🔴 ЦЕНА — это ДОСАДА, а не причина тишины. Число: 5 за всё время, 2 за сутки

Все пять прошли порог входа (`CONFLUENCE_SCORE_THRESHOLD = 2.0`), т.е. каждое было живым
кандидатом. Что было бы взято и что цена сделала дальше (реальные свечи Bybit 5m, 3 часа вперёд):

| время | сторона | счёт | цена входа | лучшее | худшее | через 3ч |
|---|---|---|---|---|---|---|
| 08-02 01:45 | LONG | 2.88 | 72.600 | +1.12% | −0.07% | **+1.02%** |
| 08-02 14:20 | SHORT | 2.15 | 73.080 | +0.26% | −0.27% | −0.16% |
| 08-11 01:45 | LONG | **7.38** | 75.990 | +0.30% | −0.04% | +0.24% |
| 08-24 00:45 | LONG | 2.38 | 94.700 | +0.92% | −1.33% | **−0.82%** |
| 08-24 11:40 | SHORT | 2.86 | 96.280 | **+2.43%** | −0.50% | +0.06% |

🔴 **Тот «хороший вход», который заметил Босс, — это SHORT 11:40: +2.43% в ход.** Но честно и
до конца: LONG 00:45 ушёл бы в −1.33% и закрыл 3 часа на −0.82%, т.е. **этот отказ спас деньги**.
Отказы не «съедали прибыль системно» — счёт смешанный.

И главное: **прохождение риск-гейта ≠ вход.** Дальше стоит консультация Claude, и с 07.08
из проходящих туда предложений входом становится ~6% (29 `executed` против 486 `ai_skipped`).
Пять отказов — это **ожидаемо ~0,3 входа**. Это досада.

🔴 **ТИШИНА ИМЕЕТ ДРУГУЮ ПРИЧИНУ, и её стоит посмотреть отдельно.** Входов нет с 22.08.
Разбор двух молчащих суток:

```
2026-08-23:  76 htf_blocked · 38 flat_adx_blocked · 16 below_threshold · 0 входов
2026-08-24:  43 flat_adx_blocked · 42 below_threshold · 24 htf_blocked · 2 risk_halt · 0 входов
```

Останавливают **HTF-каскад и flat-ADX**, а не проверка лимита (2 из 238 строк за сутки).
Я это НЕ расследовал — это за рамками задания, отмечаю как след.

## 2.8 Политика ретраев — до и после

| чтение | обёртка | попыток на 403 | попыток на ТАЙМАУТ | таймаут | цена отказа |
|---|---|---|---|---|---|
| `positions.riskcheck` (**было**) | `with_socks_retry` | `SOCKS_RETRY_MAX` | **0** | 10 000 мс | **вход отказан** |
| `ticker.*`, `ohlcv.*`, поллер, реконсилятор | `with_socks_retry` | `SOCKS_RETRY_MAX` | **0** | 10 000 мс | тик / есть запасной |
| `positions.riskcheck` (**стало**) | `with_transport_retry` | как было | **3** (1 тёплая, 1 тёплая, 1 СВЕЖИЙ выход) | 10 000 мс × попытка | **вход отказан только если не смогли все три** |

Ни одно другое чтение не менялось: у них есть второй шанс, им это не нужно, и расширять
поведение на 40 мест ради одного — лишний риск.

---

# ЧАСТЬ 3 — ПРАВКА

## 3.1 Диффы (`.bak` сделаны ДО правки)

`.bak`: `tor_retry.py.bak_capread_20260824_1330` · `main.py.bak_capread_20260824_1330`

**`main.py`** — место вызова и атрибуция ошибки:

```diff
     try:
         # Max open positions per side
-        positions = tor_retry.with_socks_retry(
+        # 🔴 2026-08-24 — with_transport_RETRY, NOT with_socks_retry. This read is
+        # asked ONCE inside the entry decision and has no next tick: when it fails
+        # the entry is refused, so a transport hiccup costs an ENTRY, not a tick.
+        # with_socks_retry covers 403s only ("Timeouts / connection errors are NOT
+        # retried") and gave this call ZERO attempts for the failure it actually
+        # had. Fail-closed below is UNCHANGED — exhausting the ladder still raises.
+        positions = tor_retry.with_transport_retry(
             exchange, lambda ex: ex.fetch_positions([symbol]),
             label='positions.riskcheck')
@@
     except Exception as e:
         # D1 FAIL-CLOSED ... Can't verify the per-side cap → BLOCK ...
-        print(f"{LOG_PREFIX}risk_check positions fetch failed (fail-closed): {e}", flush=True)
-        return False, f'position-cap check failed (fail-closed): {e}'
+        print(f"{LOG_PREFIX}risk_check positions fetch failed (fail-closed): "
+              f"{type(e).__name__}: {e}", flush=True)
+        return False, f'position-cap check failed (fail-closed): {type(e).__name__}: {e}'
```

Вторая правка — потому что все четыре исторических случая записались **голым URL** и после факта
не поддавались разбору. `type(e).__name__` стоит ноль и делает следующий случай читаемым из строки.

**`tor_retry.py`** — новая функция `with_transport_retry` (+ `is_transient_transport`,
`TRANSPORT_RETRY_MAX=3`). Лестница попыток выбрана по двум формам отказа, а не «на глаз»:

1. **primary** — тёплая цепь, измеренные 343 мс;
2. **primary снова** — икота на в общем-то хорошей цепи; цепь тёплая, значит ~350 мс, а не новое рукопожатие;
3. **СВЕЖИЙ изолированный выход** — когда плоха сама цепь; повтором по той же её не вылечить.

Ретраится только `ccxt.NetworkError` (RequestTimeout / ExchangeNotAvailable / NetworkError).
**Ответ венью (`ExchangeError`, `retCode`) не ретраится** — если Bybit ответил, повтор даст тот же ответ.

🔴 Поднимать таймаут вместо этого — отвергнуто сознательно: это заставило бы обречённое чтение
**дольше** идти к тому же отказу и всё равно осталось бы одной выборкой из бимодальной связи.

## 3.2 🔴 FAIL-CLOSED НЕ ОСЛАБЛЕН — и это доказано, а не заявлено

Изолированный стенд, настоящие функции, точная строка из БД в качестве исключения:

```
A) ОДИН сбой транспорта, потом успех — форма 24.08 00:45 / 11:40
   OLD wrapper: RAISED RequestTimeout -> _risk_check returns (False, ...)
                attempts made = 1   ENTRY REFUSED
   NEW wrapper: RETURNED [...]   attempts made = 2   ENTRY PROCEEDS

B) ДВА сбоя — должен дойти до СВЕЖЕГО ВЫХОДА
   attempt 1 and 2 same exchange object? True   (тёплая primary)
   attempt 3 a DIFFERENT object?         True   (свежий выход Tor)

C) 🔴 ВЕЧНЫЙ сбой — обязан всё равно ОТКАЗАТЬ
   [TRANSPORT_RETRY] positions.riskcheck EXHAUSTED 3 attempts — propagating, caller stays fail-closed
   NEW wrapper: RAISED RequestTimeout   attempts = 3  -> _risk_check STILL returns (False, ...)

D) ОТВЕТ ВЕНЬЮ не должен ретраиться
   RAISED ExchangeError after 1 attempt(s)  (ожидалось 1)

ALL ASSERTIONS PASSED
```

## 3.3 🔴 И ТО ЖЕ САМОЕ — ЖИВЬЁМ, ПО НАСТОЯЩЕМУ Bybit ЧЕРЕЗ Tor

```
E) РЕАЛЬНАЯ СЕТЬ, счастливый путь через НОВУЮ обёртку
   returned 2 position record(s) from Bybit in 8425 ms — реальное чтение, не задето

F) 🔴 РЕАЛЬНАЯ СЕТЬ, ПРИНУДИТЕЛЬНЫЙ ТАЙМАУТ (timeout=1 мс — гарантированно истечёт)
   OLD: RAISED RequestTimeout after 15 ms — ОДНА попытка, вход отказан
   NEW: [TRANSPORT_RETRY] attempt 1/3 … attempt 2/3 … retrying on a FRESH exit …
        EXHAUSTED 3 attempts — propagating, caller stays fail-closed
        RAISED RequestTimeout after 12169 ms — лестница исчерпана, ВСЁ РАВНО FAIL-CLOSED

G) 🔴 РЕАЛЬНАЯ СЕТЬ, САМ ДЕФЕКТ: попытка 1 истекает по-настоящему, потом чтение УДАЁТСЯ
   attempt 1 timed out for real; wrapper returned 2 record(s) after 8454 ms and 2 attempts
   ==> чтение УДАЁТСЯ там, где раньше сдавалось. Лимит проверен, вход идёт дальше.
```

**G — это ровно тот случай, который стоил двух входов 24.08**, воспроизведённый на живой сети:
раньше отказ, теперь успех. **F — это гарантия, что замок цел:** когда связи действительно нет,
ордер по-прежнему НЕ идёт.

---

# 🔴 ЧАСТЬ 4 — ТРЕБУЕТСЯ РЕСТАРТ. Я ОСТАНОВИЛСЯ.

```
service started : Mon 2026-08-17 14:58:30 UTC
main.py mtime   : 2026-08-24 13:18:16
tor_retry mtime : 2026-08-24 13:18:01
```

Правка **на диске, но НЕ в работе** — воркер поднят 17.08 и держит старый код в памяти.
Это ровно класс «фикс на диске ≠ фикс в работе». **Рестарт решает Босс — я не трогал сервис.**

Состояние на сейчас, чтобы решение было на фактах: **открытых позиций нет** — heartbeat
`open=0 mode=LIVE`, таблица `active_positions` пуста, живое чтение венью вернуло две записи
сторон с нулевым размером. То есть окно для рестарта сейчас чистое. **Команду не даю и не выполняю.**

Откат, если понадобится:
```
cp tor_retry.py.bak_capread_20260824_1330 tor_retry.py
cp main.py.bak_capread_20260824_1330     main.py
```

---

## ИТОГ

| вопрос | ответ |
|---|---|
| Обёрнуто ли чтение в `tor_retry`? | **Да** — гипотеза «голый вызов» неверна |
| Тогда почему падало? | Обёртка ретраит **только 403**; отказы — **таймауты**, у них было **0 попыток** |
| Это recvWindow? | **Нет.** 20000 на **обоих** клиентах живьём, `10002` за окно — **0** |
| Настоящая причина | холодная цепь Tor 8 305 мс против умолчания ccxt 10 000 мс |
| Новое ли это? | **Нет.** Ветка с 08.06, алерт в TG с 06.06, путь алерта не менялся |
| Сколько входов отказано | **5 за всю историю**, 2 за сутки · ожидаемо ~0,3 реальных входа |
| Досада или причина тишины? | 🔴 **ДОСАДА.** Тишину дают `htf_blocked` и `flat_adx_blocked` |
| Fail-closed ослаблен? | **Нет** — доказано C и F: исчерпав лестницу, по-прежнему отказывает |
| Сторож | предмет сужен, **EXIT 0**, дрейф торгового кода по-прежнему ловится (4 доказательства) |
