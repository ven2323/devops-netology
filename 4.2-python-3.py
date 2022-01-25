#!/usr/bin/env python3

import socket as s
import time as t
import datetime as dt

i = 1
wt = 2
srv_list = {'drive.google.com':'108.177.14.194', 'mail.google.com':'64.233.165.83', 'google.com':'173.194.221.139'}
init=0

print('*** start script ***')
print(srv_list)
print('********************')

while 1==1 :
  for host in srv_list:
    ip = s.gethostbyname(host)
    if ip != srv_list[host]:
      if i==1 and init !=1:
        print(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +' [ERROR] ' + str(host) +' IP mistmatch: '+srv_list[host]+' '+ip)
      srv_list[host]=ip
  t.sleep(wt)