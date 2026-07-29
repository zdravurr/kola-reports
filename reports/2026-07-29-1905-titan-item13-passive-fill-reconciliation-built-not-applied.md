# ПУНКТ 13 — СВЕРКА ПАССИВНЫХ ЗАЛИВОК. ПОСТРОЕНО, НЕ ПРИМЕНЕНО
**2026-07-29 19:05 UTC** · база HEAD `0833f42` · **дерево ЧИСТОЕ, патч НЕ НАЛОЖЕН**

```
 titan-bot/breakeven_worker.py |  90 +++++++++++++++++++++--------
 titan-bot/config.py           |   2 +-
 titan-bot/virtual_trader.py   | 114 +++++++++++++++++++++++++++++++++--
 3 files changed, 173 insertions(+), 33 deletions(-)
```

> Закрывает дыру из §6 отчёта по пункту 12 — последнее, что стоит между нами и боем.
> Последняя строка патча: `PASSIVE_FILL_RECONCILE_EXISTS = True`, то есть **гейт снимает сам этот
> коммит**, ровно как пункт 12 снял маршрутный.

---

## 1. ЧТО ИМЕННО ЛОМАЛОСЬ

```
цена задевает sl_price -> БИРЖЕВОЙ STOP_MARKET срабатывает на фитике -> позиция закрыта
поллер (<=10 с)        -> last <= sl_price -> _do_close
                       -> market_close -> _execute_close_position(_from_adapter=True)
                       -> _fetch_open_position = None -> None
                       -> "row left OPEN for reconciliation"   <- и никто не сверял
```
Строка навсегда `status='open'`: P&L не записан, `ux_vpos_one_open_per_side` глушит все следующие
входы на этой стороне. Бой встаёт после первой сделки, **выглядя успешным**.

---

## 2. ПЕРЕИСПОЛЬЗОВАНИЕ, А НЕ ВТОРАЯ РЕАЛИЗАЦИЯ

Ты сказал переиспользовать `_report_passive_fill`. **Вызвать его напрямую нельзя, и я объясняю
почему, а не молча пишу своё:** он завязан на таблицу `breakeven_jobs` с обоих концов — читает
`job['sl_order_id'] / ['trail_order_id'] / ['new_sl_order_id'] / ['amount'] / ['entry_price']`
и штампует идемпотентность через `_set_status(job_id, fill_reported=1)`. У строки
`virtual_positions` другая форма и другой признак «уже закрыто».

Поэтому — **тот же приём, что ты одобрил в пункте 11: извлечение, а не копия.**

**`breakeven_worker.read_filled_protective_order()`** — ядро вынуто дословно: находит ордер,
подтверждает, что он **действительно FILLED**, читает РЕАЛЬНЫЕ цену и комиссию (с падением на
тикер и на тейкерскую оценку, с печатью, когда комиссия не отдана). `_report_passive_fill` теперь
зовёт его и в остальном не изменён. Один код на двух потребителей.

**`virtual_trader._do_close(..., _exit_fill=None)`** — один необязательный параметр. Когда заливка
уже прочитана, `market_close` не вызывается, а **всё остальное — фандинг, close-report, UPDATE
строки, кросс-линк в `trades`, LONG-частичка — общее с активным закрытием**, а не продублировано.

---

## 3. `_reconcile_passive_fill` — ЧЕТЫРЕ ИСХОДА, ВСЕ ПРОВЕРЕНЫ ИСПОЛНЕНИЕМ

Вызывается **первым делом** в `_process_position`: если позиции уже нет, все вычисления ниже —
про несуществующую позицию.

```
A) БУМАГА                              -> False мгновенно, биржа не тронута ВООБЩЕ
B) БОЙ, позиция ещё ОТКРЫТА            -> False (сверять нечего)
C) БОЙ, позиции НЕТ, наш стоп НЕ залит -> 🚨 крик, строку НЕ ТРОГАЕМ, False
D) БОЙ, позиции НЕТ, наш стоп ЗАЛИТ    -> True, _do_close(63787.1, 'sl',
                                          _exit_fill={... 'simulated': False})
```

**Про (C) — это твоё же решение 13-I, «орать и не трогать».** Позиция исчезла, но ни один НАШ ордер
не заливался: закрыло что-то иное — руки, ликвидация, действие биржи. **Цены выхода мы не знаем, и
выдумывать её нельзя** — это положило бы придуманные числа в книгу. Строка остаётся человеку, а
тревога громкая именно потому, что это состояние ещё и блокирует новые входы.

**Идемпотентность** — та же, что у `_do_close`: `UPDATE ... WHERE id=? AND status='open'`. Второй
проход не закрывает ничего повторно.

**Бумага не затронута:** первая же строка функции — `if not orders_are_real(): return False`.
Наш стоп там число, пассивной заливки не существует.

---

## 4. ЧТО МОЖЕТ ПОЙТИ НЕ ТАК

1. **🔴 Ни одна боевая ветка по-прежнему не проверялась против настоящей биржи.** Всё моки —
   и в 11, и в 12, и здесь. Это главный остаточный риск всей серии.
2. **Лишний `fetch_positions` каждый тик в бою** (раз в 10 с на позицию). При
   `MAX_POSITIONS_PER_SIDE=1` это один вызов — приемлемо, но это новая нагрузка на лимиты.
3. **Случай (C) оставляет строку открытой**, а значит сторона остаётся заблокированной до прихода
   человека. Это сознательный выбор: выдуманный P&L хуже остановки. Но тревога обязана быть
   замечена — если Telegram молчит, состояние тихое.
4. **`reason` жёстко `'sl'`.** Строка знает только про свой `stop_order_id`; при безубытке это
   тот же стоп, переставленный. То есть выход по безубытку запишется как `sl`, а не `breakeven`.
   Мелочь для P&L, но для атрибуции выходов — нет. Флагую, не прячу.
5. **Трейл в бою — по-прежнему поллер** (решение принято). Если процесс умрёт после безубытка,
   выход произойдёт по биржевому стопу на безубытке, и эта функция его корректно засверит.
6. **Пункт 14 (частичные заливки) не реализован**, порог `0.02` записан и никем не читается.

---

## 5. ПОЛНЫЙ ДИФФ (НЕ ПРИМЕНЁН)

`git apply --check` против живого дерева на `0833f42` — **чисто**, `git status --porcelain` пуст,
`py_compile` — все шесть файлов OK.

```diff
diff --git a/titan-bot/breakeven_worker.py b/titan-bot/breakeven_worker.py
index 3643ae8..5a5d778 100644
--- a/titan-bot/breakeven_worker.py
+++ b/titan-bot/breakeven_worker.py
@@ -344,6 +344,62 @@ def _entry_context(entry_trade_id):
     return 0.0, None, None
 
 
+def read_filled_protective_order(exchange, symbol, candidates, amount,
+                                 fallback_price):
+    """Which of OUR protective orders actually FILLED, and the REAL exit price
+    and fee read off it. Returns {'order','label','exit_price','exit_fee'} or
+    None when none of them filled.
+
+    LIFTED OUT OF _report_passive_fill so that virtual_positions reconciliation
+    (item 13) uses THE SAME code rather than a second implementation.
+    _report_passive_fill now calls it and is otherwise unchanged.
+
+    READ-ONLY on the exchange: it fetches orders and places/cancels NOTHING.
+
+    Returning None is meaningful, not a failure: it says "the position went away
+    but none of the orders WE own filled", i.e. the close was handler-initiated
+    (those paths cancel the stop first, so it reads 'canceled') or something
+    external happened. The caller decides what that means — this function never
+    guesses a price.
+
+    `candidates` is [(order_id, label), ...] in priority order.
+    """
+    filled = None
+    for oid, label in candidates:
+        if not oid:
+            continue
+        try:
+            o = exchange.fetch_order(oid, symbol)
+        except Exception as fe:
+            print(f"[BE-FILL] fetch_order {oid} failed: {fe}", flush=True)
+            continue
+        if (o.get('status') or '').lower() in ('closed', 'filled'):
+            filled = (o, label)
+            break
+    if filled is None:
+        return None
+
+    order, label = filled
+    exit_price = order.get('average') or order.get('price')
+    if not exit_price:
+        try:
+            exit_price = float(exchange.fetch_ticker(symbol)['last'])
+        except Exception:
+            exit_price = float(fallback_price)
+    exit_price = float(exit_price)
+
+    # Exit fee from the fill; fall back to a taker estimate if absent.
+    exit_fee = (order.get('fee') or {}).get('cost')
+    if exit_fee is None and order.get('fees'):
+        exit_fee = sum((f.get('cost') or 0.0) for f in order['fees']) or None
+    if exit_fee is None:
+        exit_fee = exit_price * float(amount) * TAKER_FEE_RATE
+        print(f"[BE-FILL] fee not reported for {oid} — ESTIMATED "
+              f"${abs(float(exit_fee)):.6f} at taker rate", flush=True)
+    return {'order': order, 'label': label, 'exit_price': exit_price,
+            'exit_fee': abs(float(exit_fee))}
+
+
 def _report_passive_fill(exchange, send_tg, job, transition):
     """Passive on-exchange SL/trail FILL reporter (Stage 3 / commit 6).
 
@@ -400,18 +456,9 @@ def _report_passive_fill(exchange, send_tg, job, transition):
         else:  # 'watching' — only the original ATR SL is live pre-breakeven
             candidates = [(job['sl_order_id'], 'stop-loss')]
 
-        filled = None
-        for oid, label in candidates:
-            if not oid:
-                continue
-            try:
-                o = exchange.fetch_order(oid, symbol)
-            except Exception as fe:
-                print(f"[BE-FILL] fetch_order {oid} failed: {fe}", flush=True)
-                continue
-            if (o.get('status') or '').lower() in ('closed', 'filled'):
-                filled = (o, label)
-                break
+        filled = read_filled_protective_order(
+            exchange, symbol, candidates, float(job['amount']),
+            float(job['entry_price']))
 
         if filled is None:
             # No OWNED protective order filled -> this close was handler-initiated
@@ -420,22 +467,9 @@ def _report_passive_fill(exchange, send_tg, job, transition):
                   f"order filled (transition={transition}); not reporting.", flush=True)
             return
 
-        order, reason_label = filled
-        exit_price = order.get('average') or order.get('price')
-        if not exit_price:
-            try:
-                exit_price = float(exchange.fetch_ticker(symbol)['last'])
-            except Exception:
-                exit_price = float(job['entry_price'])
-        exit_price = float(exit_price)
-
-        # Exit fee from the fill; fall back to a taker estimate if absent.
-        exit_fee = (order.get('fee') or {}).get('cost')
-        if exit_fee is None and order.get('fees'):
-            exit_fee = sum((f.get('cost') or 0.0) for f in order['fees']) or None
-        if exit_fee is None:
-            exit_fee = exit_price * float(job['amount']) * TAKER_FEE_RATE
-        exit_fee = abs(float(exit_fee))
+        reason_label = filled['label']
+        exit_price = filled['exit_price']
+        exit_fee = filled['exit_fee']
 
         entry_fee, combo_key, opened_at = _entry_context(
             job['entry_trade_id'] if 'entry_trade_id' in job.keys() else None)
diff --git a/titan-bot/config.py b/titan-bot/config.py
index b731583..f8c931c 100755
--- a/titan-bot/config.py
+++ b/titan-bot/config.py
@@ -80,7 +80,7 @@ ROUTING_MIGRATED_TO_ADAPTER = True
 #
 # Item 13 sets this True as the LAST line of its own commit, exactly as item 12
 # does for the routing marker. It is NOT an operator dial.
-PASSIVE_FILL_RECONCILE_EXISTS = False
+PASSIVE_FILL_RECONCILE_EXISTS = True
 
 # ---------------------------------------------------------------------------
 # PARTIAL-FILL DIVERGENCE THRESHOLD — deliberate policy number, NOT YET WIRED.
diff --git a/titan-bot/virtual_trader.py b/titan-bot/virtual_trader.py
index b1820ca..65bfd9f 100755
--- a/titan-bot/virtual_trader.py
+++ b/titan-bot/virtual_trader.py
@@ -808,18 +808,118 @@ def close_position(exchange, send_tg, symbol, position_side, reason='external'):
     return _do_close(exchange, row, last, reason, send_tg)
 
 
-def _do_close(exchange, row, close_price, reason, send_tg):
+def _reconcile_passive_fill(exchange, row, send_tg):
+    """ITEM 13 — PASSIVE-FILL RECONCILIATION for virtual_positions.
+
+    Since item 11 the protective stop is a real STOP_MARKET on the exchange, and
+    the poller does not learn when it fires. Without this, a live stop exit went:
+
+        exchange stop triggers on the wick -> position closed
+        poller (<=10s later) sees last <= sl_price -> _do_close
+        -> market_close -> _execute_close_position -> no position -> None
+        -> "row left OPEN for reconciliation"      <- and nothing reconciled it
+
+    The row stayed status='open' forever: no P&L, and ux_vpos_one_open_per_side
+    blocked every later entry on that side. Live stalled after its FIRST trade
+    while looking successful. That is the gate this function opens.
+
+    Returns True iff it FINALISED the row (caller must stop processing it).
+
+    PAPER IS UNTOUCHED: our stop there is a number the poller evaluates, so no
+    passive fill can exist and this returns False before doing anything.
+
+    IDEMPOTENT for the same reason _do_close is: the row UPDATE is guarded by
+    `WHERE id=? AND status='open'`, so a second pass finalises nothing.
+    """
+    if not order_adapter.orders_are_real():
+        return False                       # paper: the poller owns the stop
+
+    _rk = row.keys()
+    stop_id = row['stop_order_id'] if 'stop_order_id' in _rk else None
+    if not stop_id:
+        # No exchange stop recorded -> nothing of ours could have passively
+        # filled. Leave it to the normal poller logic.
+        return False
+
+    # Is the position still on the exchange?
+    try:
+        import main as _m
+        pos = _m._fetch_open_position(row['symbol'], row['position_side'])
+    except Exception as e:
+        # Cannot tell -> do NOT guess. Leaving the row open is recoverable;
+        # inventing a close is not.
+        print(f"[VPOS-FILL] position check failed vpos={row['id']}: {e}", flush=True)
+        return False
+    if pos is not None:
+        return False                       # still open, nothing to reconcile
+
+    # The position is GONE. Did OUR stop fill, or did something else close it?
+    # read_filled_protective_order is breakeven_worker's, reused verbatim: it
+    # finds the order, confirms it FILLED, and reads the REAL price and fee.
+    import breakeven_worker as _bw
+    filled_legs = json.loads(row['filled_legs'])
+    _avg_entry, _size = _avg_entry_and_size(filled_legs)
+    fill = _bw.read_filled_protective_order(
+        exchange, row['symbol'], [(stop_id, 'stop-loss')], _size, _avg_entry)
+
+    if fill is None:
+        # 🔴 The position vanished but NONE of our orders filled. Something else
+        # closed it — manual intervention, liquidation, an exchange action. We
+        # do NOT know the exit price, and fabricating one would put invented
+        # numbers in the book. SHOUT AND DO NOT TOUCH (operator decision 13-I),
+        # leaving the row for a human. The alert is loud precisely because this
+        # state also stalls new entries on this side.
+        print(f"[VPOS-FILL] 🚨 vpos={row['id']} {row['symbol']} "
+              f"{row['position_side']}: position GONE from the exchange but our "
+              f"stop {stop_id} did NOT fill. NOT closing the row — exit price "
+              f"unknown. MANUAL ACTION REQUIRED.", flush=True)
+        if send_tg:
+            try:
+                send_tg(f"🚨 <b>POSITION GONE, STOP DID NOT FILL</b>\n"
+                        f"{row['symbol']} {row['position_side']} · vpos "
+                        f"{row['id']}\nOur stop <code>{stop_id}</code> is not "
+                        f"filled, yet the exchange shows no position.\n"
+                        f"The row is left OPEN and its exit price is UNKNOWN — "
+                        f"nothing has been invented.\n"
+                        f"<b>This also blocks new entries on this side. "
+                        f"MANUAL ACTION REQUIRED.</b>")
+            except Exception:
+                pass
+        return False
+
+    # Our stop filled. Finalise the row from the REAL price and fee, through the
+    # SAME path an active close uses — one close report, one arithmetic.
+    print(f"[VPOS-FILL] passive fill vpos={row['id']} {row['symbol']} "
+          f"{row['position_side']}: {fill['label']} filled @ "
+          f"{fill['exit_price']} fee={fill['exit_fee']:.6f}", flush=True)
+    _do_close(exchange, row, fill['exit_price'], 'sl', send_tg,
+              _exit_fill={'fill_price': fill['exit_price'], 'amount': _size,
+                          'fee_cost': fill['exit_fee'], 'simulated': False,
+                          'order': fill['order']})
+    return True
+
+
+def _do_close(exchange, row, close_price, reason, send_tg, _exit_fill=None):
     """Shared by external close + poller-triggered SL/trail close. Updates
     virtual_positions, sends the 🧪 Telegram report, returns the dict the
-    real _execute_close_position would have returned."""
+    real _execute_close_position would have returned.
+
+    `_exit_fill` — item 13. When the position was ALREADY closed on the exchange
+    by our own stop, there is nothing left to send: the caller
+    (_reconcile_passive_fill) has read the REAL fill off the filled order and
+    passes it here. Everything below — funding, the close report, the row
+    update, the trades cross-link — is then shared verbatim between an active
+    close and a passive one, instead of existing twice.
+    """
     filled_legs = json.loads(row['filled_legs'])
     avg_entry, total_size = _avg_entry_and_size(filled_legs)
     # THE EXIT FILL. Simulated: close_price stays the decision price and the fee
     # is flat — unchanged arithmetic. Live: main._execute_close_position runs
     # (cancel this side's triggers -> close the REAL on-exchange size -> re-sweep
     # orphans), and the actual fill price, size and fee come back from it.
-    _exit_fill = order_adapter.market_close(
-        exchange, row['symbol'], row['position_side'], total_size, close_price)
+    if _exit_fill is None:
+        _exit_fill = order_adapter.market_close(
+            exchange, row['symbol'], row['position_side'], total_size, close_price)
     if _exit_fill is None:
         print(f"VIRTUAL CLOSE ABORTED vpos={row['id']}: adapter found no live "
               f"position to close; row left OPEN for reconciliation", flush=True)
@@ -1692,6 +1792,12 @@ def _process_position(exchange, row, last, send_tg):
     short-circuit logging). Single-entry model, mirroring the live
     breakeven_worker: before +1R only the original ATR SL is active (no trail);
     at +1R the SL is moved to breakeven and the trail is activated."""
+    # ITEM 13 — passive fill FIRST. If our exchange stop already closed this
+    # position, every computation below would be about a position that no longer
+    # exists. Returns False instantly in paper.
+    if _reconcile_passive_fill(exchange, row, send_tg):
+        return True
+
     position_side = row['position_side']
     water_mark = float(row['water_mark'])
     sl_price = float(row['sl_price'])
```
