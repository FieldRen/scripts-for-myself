#coding=utf-8                                                                                                                                                                 
#!flask/bin/python
from flask_restful import reqparse
import os
import shutil
import string
import subprocess
import json
from flask import Flask, request
from pynvml import *
#from multiprocessing import Process

logfile = 'train.log'
configfile = 'worker.conf'

workerid = 0 # TODO 通过json配置文件读取

def queryGPUMem(gpuid):
    nvmlInit()
    # num = nvmlDeviceGetCount()
    # print num
    # for i in range(num):
    #     handle = nvmlDeviceGetHandleByIndex(i)
    #     info = nvmlDeviceGetMemoryInfo(handle)
    #     temp = nvmlDeviceGetTemperature(handle, 0)
    #     perc = nvmlDeviceGetFanSpeed(handle)
    #     power = nvmlDeviceGetPowerUsage(handle)
    #     util = nvmlDeviceGetUtilizationRates(handle)
    #     print "Device:", nvmlDeviceGetName(handle),  str(temp)+"C"
    #     print "Total memory:", info.total/1000000
    #     print "Used memory:", info.used/1000000
    #     print str(perc)+"%"
    #     print str(power/1000)+"W"
    #     print util.gpu, util.memory
    info = ""
    handle = nvmlDeviceGetHandleByIndex(gpuid)
    mem = nvmlDeviceGetMemoryInfo(handle)
    memunused = mem.total/1000000 - mem.used/1000000
    return memunused

# TODO 根据logfile解析训练进度
def getPercent(logfile):
    return 0.5

app = Flask(__name__)

returntrain = {'status':'OK', 'errmsg':''}
returnstatus = {'worker_id': 0,'status':'OK', 'errmsg':'', 'handle_status':'suspending', 'percent':0.0, 'load_status':0}

@app.route('/api/v1/tasks/create', methods = ['POST'])
def receivetask():
    print request.data
    # data = json.loads(request.data)
    # print data
    # 拷贝数据
    # TODO
    # 开启新进程启动训练
    argument = ' train.py'
    proc = subprocess.Popen("python" + argument, shell=True)
    rdata = returntrain.copy()
    return json.dumps(rdata)


@app.route('/api/v1/tasks/master_find_taskstatus', methods = ['GET'])
def sendstatus():
    data = returnstatus.copy()
    data['workerid'] = workerid
    # 通过train.log获取进度,根据进度值得到状态
    per = getPercent(logfile)
    data['percent'] = per
    if per < 0.000001:
        data['handle_status'] = 'suspending'
    elif per < 0.999999:
        data['handle_status'] = 'handling'
    else:
        data['handle_status'] = 'solved'
    # 获取GPU显存剩余
    mem = queryGPUMem(0)
    data['load_status'] = mem
    print data
    return json.dumps(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8125)


