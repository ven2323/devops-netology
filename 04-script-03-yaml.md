### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-03-yaml/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

Ответ:
Ошибка в 9 строке, не хватает кавычек
"ip" : 71.78.22.43"

## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
# #!/usr/bin/env python3

import socket as s
import time as t
import datetime as dt
import json
import yaml

i = 1
wt = 2
srv_list = {'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0', 'google.com': '0.0.0.0'}
init = 0
# path config
# fpath = "/home/sa/devops-netology/python/"
fpath = "c:/netology/devops-netology/python/"
# path logs
# flog = "/home/sa/devops-netology/error/python/.log"
flog = "c:/netology/devops-netology/python/error.log"

print('*** start script ***')
print(srv_list)
print('********************')

while 1 == 1:
  for host in srv_list:
    ip = s.gethostbyname(host)
    if ip != srv_list[host]:
      if i == 1 and init != 1:
        with open(flog, 'a') as file:
          print(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' [ERROR] ' + str(host) + ' IP mistmatch: ' + srv_list[host] + ' '+ip)
          file.write(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " [ERROR] " + str(host) + " IP mistmatch: "+ srv_list[host]+" " + ip + '\n')
        # json
        with open(fpath+host+".json", 'w') as jsf:
          json_data = json.dumps({host: ip})
          jsf.write(json_data)
        # yaml
        with open(fpath+host+".yaml", 'w') as ymf:
          yaml_data = yaml.dump([{host: ip}])
          ymf.write(yaml_data)
      srv_list[host]=ip
  i += 1
  t.sleep(wt)
```

### Вывод скрипта при запуске при тестировании:
```
*** start script ***
{'google.com': '0.0.0.0', 'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0'}
********************
2022-01-25 11:50:06 [ERROR] google.com IP mistmatch: 0.0.0.0 173.194.222.102
2022-01-25 11:50:06 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 74.125.131.194
2022-01-25 11:50:06 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 142.251.1.19
```

### json-файл(ы), который(е) записал ваш скрипт:
```json
{"drive.google.com": "74.125.131.194"}
{"google.com": "173.194.222.113"}
{"mail.google.com": "142.251.1.18"}
```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
- drive.google.com: 74.125.131.194
- google.com: 173.194.222.113
- mail.google.com: 142.251.1.18
```
