#!/usr/bin/env python3

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
fpath = "/home/sa/devops-netology/python/"
# path logs
flog = "/home/sa/devops-netology/python/error.log"

print('*** start script ***')
print(srv_list)

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
