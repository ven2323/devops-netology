# Домашнее задание к занятию "6.6. Troubleshooting"

## Задача 1

Перед выполнением задания ознакомьтесь с документацией по [администрированию MongoDB](https://docs.mongodb.com/manual/administration/).

Пользователь (разработчик) написал в канал поддержки, что у него уже 3 минуты происходит CRUD операция в MongoDB и её 
нужно прервать. 

Вы как инженер поддержки решили произвести данную операцию:
- напишите список операций, которые вы будете производить для остановки запроса пользователя
- предложите вариант решения проблемы с долгими (зависающими) запросами в MongoDB

Ответ:
- Найти данную операцию при помощи команды db.currentOp({"active": true, "secs_running": {"$gt": 1}})
- Буду выведены все операции исполняющиеся больше секунды, с указанием их opid.
- Завершить операцию по opid с помощью команды db.killOp(<opid>), укажем в команде opid полученные предыдущей командой.
- Чтобы проблема не повторялась воспользоваться параметром maxTimeMS(), для ограничения времени выполнения запросов.

## Задача 2

Перед выполнением задания познакомьтесь с документацией по [Redis latency troobleshooting](https://redis.io/topics/latency).

Вы запустили инстанс Redis для использования совместно с сервисом, который использует механизм TTL. 
Причем отношение количества записанных key-value значений к количеству истёкших значений есть величина постоянная и
увеличивается пропорционально количеству реплик сервиса. 

При масштабировании сервиса до N реплик вы увидели, что:
- сначала рост отношения записанных значений к истекшим
- Redis блокирует операции записи

Как вы думаете, в чем может быть проблема?

Ответ:
В Redis есть два способа очистить просроченные записи: отложенное удаление "ленивый метод" и периодическое удаление. В случае с ленивым - просроченные записи запрашиваются командой, периодический способ - вызывается из крон каждые 100 миллисекунд. ACTIVE_EXPIRE_CYCLE_LOOKUPS_PER_LOOP по умолчанию имеет значение 20, таким образом за раз можно пометить и очистить около 200 устаревших записей. Данный процесс ограничивается 25% ресурса процессора. Процесс проверки может зациклится и мы ощутим задержки, а потом и вовсе не будут приниматься данные на запись, если появятся истекшие записи более 25% по отношению ко всем. В данном случае как раз так и получается.

## Задача 3

Перед выполнением задания познакомьтесь с документацией по [Common Mysql errors](https://dev.mysql.com/doc/refman/8.0/en/common-errors.html).

Вы подняли базу данных MySQL для использования в гис-системе. При росте количества записей, в таблицах базы,
пользователи начали жаловаться на ошибки вида:
```python
InterfaceError: (InterfaceError) 2013: Lost connection to MySQL server during query u'SELECT..... '
```

Как вы думаете, почему это начало происходить и как локализовать проблему?

Какие пути решения данной проблемы вы можете предложить?

Ответ:
Ошибки возникают, как вариант, из за возросшей нагрузки на сервер.
Как варианты решения:
1. Добавить ресурсов машине
2. Создать индексы для ускорения запросов (если таковых нет)
3. Увеличить параметры connect_timeout, interactive_timeout, wait_timeout
4. Посмотреть slow logs, и логи бд.

## Задача 4

Перед выполнением задания ознакомтесь со статьей [Common PostgreSQL errors](https://www.percona.com/blog/2020/06/05/10-common-postgresql-errors/) из блога Percona.

Вы решили перевести гис-систему из задачи 3 на PostgreSQL, так как прочитали в документации, что эта СУБД работает с 
большим объемом данных лучше, чем MySQL.

После запуска пользователи начали жаловаться, что СУБД время от времени становится недоступной. В dmesg вы видите, что:

`postmaster invoked oom-killer`

Как вы думаете, что происходит?

Как бы вы решили данную проблему?

Ответ:
Ошибка oom-killer говорит о недостатке оперативной памяти, ОС завершает процессы которые используют память, чтобы предотвратить падение всей системы. Для устранения проблемы нужно увеличть размер RAM или настроить ограничение использования ресрусов в настройках postresql.
Следующие параметры postgresql отвечают за использование оперативной памяти:
```
shared_buffers
temp_buffers
work_mem
hash_mem_multiplier 
maintenance_work_mem
autovacuum_work_mem
logical_decoding_work_mem
```
---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
