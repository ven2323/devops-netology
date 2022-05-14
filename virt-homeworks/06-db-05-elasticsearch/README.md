# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib`
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста
- ссылку на образ в репозитории dockerhub
- ответ `elasticsearch` на запрос пути `/` в json виде

Подсказки:
- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения

Далее мы будем работать с данным экземпляром elasticsearch.

Ответ:
Текст Dockerfile манифеста:
Не запускается при сборке yum, ругается на java, собрал из пакетов.
```
FROM centos:7
LABEL ElasticSearch Lab 6.5 \
    (c)Zaytsev Alexey
ENV PATH=/usr/lib:/usr/lib/jvm/jre-11/bin:$PATH

RUN yum install java-11-openjdk -y.
RUN yum install wget -y.

RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.11.1-linux-x86_64.tar.gz \
    && wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.11.1-linux-x86_64.tar.gz.sha512.
RUN yum install perl-Digest-SHA -y.
RUN shasum -a 512 -c elasticsearch-7.11.1-linux-x86_64.tar.gz.sha512 \.
    && tar -xzf elasticsearch-7.11.1-linux-x86_64.tar.gz \
    && yum upgrade -y
....
ADD elasticsearch.yml /elasticsearch-7.11.1/config/
ENV JAVA_HOME=/elasticsearch-7.11.1/jdk/
ENV ES_HOME=/elasticsearch-7.11.1
RUN groupadd elasticsearch \
    && useradd -g elasticsearch elasticsearch
....
RUN mkdir /var/lib/logs \
    && chown elasticsearch:elasticsearch /var/lib/logs \
    && mkdir /var/lib/data \
    && chown elasticsearch:elasticsearch /var/lib/data \
    && chown -R elasticsearch:elasticsearch /elasticsearch-7.11.1/
RUN mkdir /elasticsearch-7.11.1/snapshots &&\
    chown elasticsearch:elasticsearch /elasticsearch-7.11.1/snapshots
....
USER elasticsearch
CMD ["/usr/sbin/init"]
CMD ["/elasticsearch-7.11.1/bin/elasticsearch"]
```

Ссылку на образ в репозитории dockerhub:
https://hub.docker.com/layers/214091051/ven23/elasticsearchtar/latest/images/sha256-d016ffac84433ac7f347bd94d1e577f1a759666992fdeec3990695eb907ae282?context=repo

- ответ `elasticsearch` на запрос пути `/` в json виде:
```json
{
  "name" : "ec9df9ba4f2a",
  "cluster_name" : "netology_test",
  "cluster_uuid" : "yN1y9k9USnit2GgBJWhNbQ",
  "version" : {
    "number" : "7.11.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "ff17057114c2199c9c1bbecc727003a907c0db7a",
    "build_date" : "2021-02-15T13:44:09.394032Z",
    "build_snapshot" : false,
    "lucene_version" : "8.7.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

Получите состояние кластера `elasticsearch`, используя API.

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Удалите все индексы.

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

Ответ:
Добавляем индексы:
```bash
curl -X PUT localhost:9200/ind-1 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
curl -X PUT localhost:9200/ind-2 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 2,  "number_of_replicas": 1 }}'
curl -X PUT localhost:9200/ind-3 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 4,  "number_of_replicas": 2 }}'
```

Получаем список индексов и их статусов:
```bash
curl -X GET 'http://localhost:9200/_cat/indices?v'

health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   ind-1 e7u6cp0dQYSV_g77IvpKYg   1   0          0            0       208b           208b
yellow open   ind-3 F6lbuz4HSVSIToBEXq2Pwg   4   2          0            0       832b           832b
yellow open   ind-2 rifdQTucQy-M1X4iadNJOg   2   1          0            0       416b           416b

curl -X GET 'http://localhost:9200/_cluster/health/ind-1?pretty'
{
  "cluster_name" : "netology_test",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 1,
  "active_shards" : 1,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}

curl -X GET 'http://localhost:9200/_cluster/health/ind-2?pretty'
{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 2,
  "active_shards" : 2,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 2,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 41.17647058823529
}

curl -X GET 'http://localhost:9200/_cluster/health/ind-3?pretty'

{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 4,
  "active_shards" : 4,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 8,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 41.17647058823529
}
```

Получаем состояние кластера:
```bash
curl -XGET localhost:9200/_cluster/health/?pretty=true
{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 7,
  "active_shards" : 7,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 41.17647058823529
}
```

Индексы в статусе Yellow потому что число реплик не совпадает с количеством серверов, а т.к. реплицировать некуда, такой статус.

Удаление индексов:
```bash
curl -X DELETE 'http://localhost:9200/ind-1?pretty'
curl -X DELETE 'http://localhost:9200/ind-2?pretty'
curl -X DELETE 'http://localhost:9200/ind-3?pretty'
```

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.

[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.

**Приведите в ответе** список файлов в директории со `snapshot`ами.

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.

[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.

Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

Ответ:
Регистрируем директорию через api:
```bash
curl -XPOST localhost:9200/_snapshot/netology_backup?pretty -H 'Content-Type: application/json' -d'{"type": "fs", "settings": { "location":"/elasticsearch-7.11.1/snapshots" }}'
{
  "acknowledged" : true
}
```

Создаем индекс test с 0 реплик и 1 шардом:
```bash
curl -X PUT localhost:9200/test -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'

{"acknowledged":true,"shards_acknowledged":true,"index":"test"}
```

Список индексов:
```bash
curl -X GET 'http://localhost:9200/_cat/indices?v'

health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test  YXRyfzekQoOIZW8bJXZPfA   1   0          0            0       208b           208b
```

Создание снапшота:
```bash
curl -X PUT localhost:9200/_snapshot/netology_backup/elasticsearch?wait_for_completion=true
{"snapshot":{"snapshot":"elasticsearch","uuid":"MsdzG4NkS_q_Ek8OysRqaw","version_id":7110199,"version":"7.11.1","indices":["test"],"data_streams":[],"include_global_state":true,"state":"SUCCESS","start_time":"2022-05-14T10:46:59.735Z","start_time_in_millis":1652525219735,"end_time":"2022-05-14T10:47:00.536Z","end_time_in_millis":1652525220536,"duration_in_millis":801,"failures":[],"shards":{"total":1,"failed":0,"successful":1}}}17:47:01
```
Список файлов папке snapshots
```bash
total 52
drwxr-xr-x 1 elasticsearch elasticsearch  4096 May 14 10:47 .
drwxr-xr-x 1 elasticsearch elasticsearch  4096 May 14 08:11 ..
-rw-r--r-- 1 elasticsearch elasticsearch   437 May 14 10:47 index-0
-rw-r--r-- 1 elasticsearch elasticsearch     8 May 14 10:47 index.latest
drwxr-xr-x 3 elasticsearch elasticsearch  4096 May 14 10:47 indices
-rw-r--r-- 1 elasticsearch elasticsearch 22002 May 14 10:47 meta-MsdzG4NkS_q_Ek8OysRqaw.dat
-rw-r--r-- 1 elasticsearch elasticsearch   269 May 14 10:47 snap-MsdzG4NkS_q_Ek8OysRqaw.dat
```

Удаление индекса и создание нового:
```bash
-список индексов
curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test  YXRyfzekQoOIZW8bJXZPfA   1   0          0            0       208b           208b

-удаляем индекс
curl -X DELETE 'http://localhost:9200/test?pretty'

-создаем индекс
curl -X PUT localhost:9200/test-2?pretty -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'

-список индексов
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2 5lQ0h-JIRLizcNbe9dE4WQ   1   0          0            0       208b           208b

```

Восстанавливаем кластер из снапшота:
```bash
curl -X POST localhost:9200/_snapshot/netology_backup/elasticsearch/_restore?pretty -H 'Content-Type: application/json' -d'{"include_global_state":true}'

Список индексов:
curl -X GET http://localhost:9200/_cat/indices?v
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2 5lQ0h-JIRLizcNbe9dE4WQ   1   0          0            0       208b           208b
green  open   test   GhjteSZiQZyz6x4QSUHoPw   1   0          0            0       208b           208b
```

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
