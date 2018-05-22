#coding=utf-8
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from itertools import islice
import os
import json
import urllib2
import sched
import time
import argparse
from pynvml import *
import Queue

url = 'http://127.0.0.1:3000/api/v1/taskprocess'

description = {"This py is create for return logfile"}
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--max_iter', default=120000, type=int, 
		   help="Iteration number of traning")
parser.add_argument('--worker_id', default=0, type=int)
parser.add_argument('--task_id', default=0, type=int)
args = parser.parse_args()
img_name = 'log_'+str(args.task_id)+'.png'

def queryGPUMem(gpuid):
    nvmlInit()
    info = ""
    handle = nvmlDeviceGetHandleByIndex(gpuid)
    mem = nvmlDeviceGetMemoryInfo(handle)
    memunused = mem.total/1000000 - mem.used/1000000
    return memunused

def plog(train_log_path, test_log_path):
    data = [[], [], [0], [0]]
    with open(train_log_path, 'r') as f1:
        with open(test_log_path, 'r') as f2:
            for line1 in islice(f1,1,None):
                line = line1.strip()
                fields1 = line.split()
                if len(fields1)>2:
                    data[0].append(float(fields1[0].strip()))
                    data[1].append(float(fields1[2].strip()))
            for line2 in islice(f2,1,None):
		        line = line2.strip()
                fields2 = line.split()
                if len(fields2)==3:
                    data[2].append(float(fields2[0].strip()))
                    data[3].append(float(fields2[2].strip()))

    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax1.plot(data[0], data[1], label='Loss')
    ax1.legend(loc=1, bbox_to_anchor=(0.96, 1))
    ax2.plot(data[2], data[3], label="Accuracy", color='r')
    ax2.legend(loc=1, bbox_to_anchor=(0.98, 0.92))
    plt.title("Train Loss & Test Accuracy")
    ax1.set_xlabel("Iterations")
    ax1.set_ylabel("Loss")
    ax2.set_ylabel("Accuracy")
    plt.savefig(img_name)
    plt.close(fig)
    return data[0][-1]/args.max_iter

log_dir = '/home/zyy/caffe-ssd/tools/extra/'
test_log_path=log_dir+'train111.log.test'
train_log_path=log_dir+'train111.log.train'
returnstatus = {'worker_id':args.worker_id,'task_id': args.task_id,'status':'OK', 'image':'/home/zyy/worker/'+img_name, 'handle_status':'suspending', 'percent':0.0, 'load_status':0, 'param_dir':'','bin_dir':''}
data = returnstatus.copy()

q=Queue.Queue()

def post_log():
    mem = queryGPUMem(0)
    data['load_status'] = mem
    get_log = 'cd ~/caffe-ssd/tools/extra && ./parse_log.sh ../../examples/caffe-mobilenetssd/train111.log'
    os.system(get_log)
    per = plog(train_log_path, test_log_path)
    q.put(per)
    if q.qsize() > 6:
	if q.get() == per:
	    return 1
    print 1
    data['percent'] = round(per,2)
    if per < 0.001:
        data['handle_status'] = 'suspending'
    elif per < 0.999:
        data['handle_status'] = 'handling'
    else:
        data['handle_status'] = 'solved'
    
    if data['handle_status'] == 'solved':
        return 1
    encoded_data = json.JSONEncoder().encode(data)
    header = {"Content-Type": "application/json"}
    req = urllib2.Request(url=url, data=encoded_data, headers=header)
    try:
	    responce = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
	    print e.code
	    s.enter(30,1,post_log,())
    else:
	    s.enter(30,1,post_log,())

s = sched.scheduler(time.time, time.sleep)
s.enter(30,1,post_log,())
s.run()

