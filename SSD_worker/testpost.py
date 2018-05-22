# coding: utf-8
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import time
import urllib2
import json
from pynvml import *

# 日志文件
logfile = 'train.log'
# 请求地址
url = 'http://0.0.0.0:8124/api/v1/tasks/create'
#url = 'http://0.0.0.0:8124/api/v1/tasks/master_find_taskstatus'

register_openers()
# post启动训练到worker
params = {'task_id':0,
          'image_dir':'/home/zyy/image',
          'train_param':'',
          'ret_dir':'/home/zyy/train',
          'notify_ip':'http://192.168.1.16:8123/process'}
body_value=json.JSONEncoder().encode(params)

print body_value
headers = {"Content-Type": "application/json"} 
req = urllib2.Request(url=url,data=body_value, headers=headers)
#response = urllib2.urlopen(url)
response = urllib2.urlopen(req)
result = response.read()

print result

