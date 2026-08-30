# ТИТАН: ПЕРВОЕ НЕОБРЕЗАННОЕ ОБОСНОВАНИЕ ВЫХОДА — 1071 СИМВОЛ, И ОНО ИСПОЛЬЗУЕТ ТРИ ФАКТА ИЗ ЧЕТЫРЁХ

**2026-08-31 01:10 UTC** · Дозапись к отчёту 00:20, закрывающая единственный оставленный в нём открытым пункт.
`openitems_guard` — **EXIT=0**. `titan-bot HEAD` **`7ba8241`**. Кода не менялось, ничего не применялось.
🔴 **ТОЛЬКО ЧТЕНИЕ. Mercury-SOL не тронут.**

---

## 🔴 ПРЕДРЕГИСТРАЦИЯ ЗАКРЫТА. ВЕТКА «> 400» — ПОТОЛОК РЕАЛЬНО СНЯТ.

В отчёте 00:20 я оставил §1e открытым и записал три исхода заранее. Консультация пришла
**17:05:47**, вердикт **`hold`**, уверенность 0.72:

| исход, записанный ЗАРАНЕЕ | что значило бы | **факт** |
|---|---|---|
| длина **> 400** | потолок реально снят, впервые видим хвост | 🔴 **ДА — 1071 символ** |
| длина ≈ 400 | модель самоограничивается | нет |
| длина ≈ 1200 | упёрлись в новый потолок, 1200 мало | нет — запас 129 символов |

**База для сравнения: последняя консультация под старым потолком (16:05:43) — ровно 400.**
До неё 157 сохранённых, медиана 400, 96 % у потолка.

**1200 оказалось верным выбором: хватило, и не впритык.**

---

## ПЕРВОЕ ПОЛНОЕ ОБОСНОВАНИЕ ВЫХОДА В ИСТОРИИ ЭТОГО БОТА — ДОСЛОВНО

> **HOLD.** Entry thesis remains viable despite mixed signals. Supportive factors: (1) ADX15m=47.5
> shows strong trend persistence; (2) supporting wall grew substantially (7.1x→15.7x, 96th pct)
> indicating fresh buying interest; (3) unrealised +1.03R with stop at +0.71R away provides **0.32R
> downside floor**; (4) position only 4h old, **has tracked +0.47R gain in last hour suggesting
> momentum continuation**. Caution factors: (1) giveback from peak (0.30R) signals some
> profit-taking; (2) 5m structure shows recent bearish imbalance 26m ago against the LONG, though
> older bullish I-CHOCH 51m ago still relevant; (3) opposing wall at 86th pct is thick, creating
> potential resistance; (4) imbalance percentile at 16th (ordinary) lacks conviction. However:
> regime strengthened (ADX1h 13.4→23.5), 15m+5m remain bullish, 1d still bull. **Closing costs
> 0.162R in fees (16% of gain), eroding the edge. With stop-market resting on exchange and trailing
> protection armed, downside is contained.** Let trailing stop work; thesis intact enough to justify
> holding through the current 4h candle close.

---

## 🔴 ТРИ ИЗ ЧЕТЫРЁХ ФАКТОВ ИСПОЛЬЗОВАНЫ ЯВНО. ЧЕТВЁРТЫЙ НЕПРИМЕНИМ.

| факт | что было в промпте | что модель с ним сделала |
|---|---|---|
| **(a) цена закрытия** | `Closing now costs 0.162R … That is 16% of the +1.03R currently unrealised.` | 🔴 **«Closing costs 0.162R in fees (16% of gain), ERODING THE EDGE»** — процитировала и **сделала из неё довод** |
| **(b) стоп на бирже** | `That stop is a STOP_MARKET order resting ON THE EXCHANGE … it stands whether or not this process is running` | 🔴 **«With stop-market resting on exchange … downside is contained»** — использовала почти дословно |
| **(d) направление** | `Unrealised: +0.55R -> +1.03R (+0.47R)` | 🔴 **«has tracked +0.47R gain in last hour suggesting momentum continuation»** — процитировала дельту |
| **(c) расстояние до взвода** | не рендерится: **трейл УЖЕ взведён** | **«trailing protection ARMED»** — прочитала взведённое состояние |

**И она посчитала то, чего в промпте не было:** *«unrealised +1.03R with stop at +0.71R away provides
0.32R downside floor»*. 1.03 − 0.71 = **0.32**. Арифметика верна. **Модель вывела пол по удержанию
из двух выданных ей фактов — ровно то, ради чего факты и давались.**

---

## 🔴 ЧТО ЭТО ДОКАЗЫВАЕТ И ЧЕГО НЕ ДОКАЗЫВАЕТ

**Доказывает:**
* Потолок снят, хвост виден. **До этого дня мы не видели вторую половину НИ ОДНОГО обоснования выхода.**
* Четыре факта не просто рендерятся — **три из них вошли в текст решения** на первой же полной консультации.
* Промпт целостен: `Cost of closing` встречается в нём **ровно один раз** (проверено — раннее
  «удвоение» в моём выводе было наложением двух печатаемых срезов, а не дефектом).

**НЕ доказывает:**
* 🔴 **ЭТО ОДНА КОНСУЛЬТАЦИЯ И ОДИН ВЕРДИКТ `hold`.** Предрегистрация из отчёта 22:10 остаётся в силе
  без изменений: база доли закрытий **13.2 %**, ожидание **8–13 %**, **< 5 % = подавление (находка,
  а не успех)**, **> 25 % = перечитать правку**, выборка **~30 закрытий ≈ 230 консультаций ≈ МЕСЯЦЫ.**
* **Ни одного вердикта `close` под новым промптом ещё не было.** Как факты влияют на РЕШЕНИЕ ЗАКРЫТЬ —
  неизвестно; известно лишь, что в решении УДЕРЖАТЬ они процитированы.
* Позиция в этот момент была **в плюсе и с взведённым трейлом** — самый лёгкий случай для «hold».
  **Настоящая проверка — консультация в зоне −0.2R, где советник и срабатывал.**

---

## СОСТОЯНИЕ

`titan.service` active, `NRestarts=0`, старт 16:37:32. **vpos 100 открыта:** нереализовано **+1.03R**,
MFE **+1.32R**, трейл взведён, стоп-маркет на бирже выше входа. Оба репозитория запушены, чисто.
🔴 **Mercury-SOL: `NRestarts=0`, старт 2026-08-24 13:29:27 — не изменился.**

**Происхождение:** `trades.db` Титана открыта `mode=ro`; обоснование и промпт — как их сохранил
сам бот; ничего не изменялось, ничего не применялось.
