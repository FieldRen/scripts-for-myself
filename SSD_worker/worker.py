#coding=utf-8                                                                                                                                                                 
#!flask/bin/python
from flask_restful import reqparse
import os
import subprocess
import json
from flask import Flask, request
from pynvml import *
from PIL import Image
#from multiprocessing import Process

logfile = 'train111.log.train'
configfile = 'worker.conf'

workerid = 0 # TODO 通过json配置文件读取
trainsh_pid = {}
return_pid = {}

app = Flask(__name__)

returntrain = {'status':'OK', 'errmsg':''}
returnstoptrain = {'worker_id':0, 'status':'OK', 'errmsg':''}
returnstatus = {'worker_id': 0,'status':'OK', 'errmsg':'', 'handle_status':'suspending', 'percent':0.0, 'load_status':0}

@app.route('/api/v1/tasks/create', methods = ['POST'])
def receivetask():
    data = json.loads(request.data)
    print data
    if trainsh_pid.has_key(data['task_id']):
	    print "This task id is in working"
	    return 0
    # 拷贝数据
    copy_data="./data_create.sh "+data['image_dir']
    co = subprocess.Popen(copy_data, shell=True)
    co.wait()
    # 模型参数设置
    if data['train_params']['iteration_count'] == '':
	    data['train_params']['iteration_count']='1200'
    if data['train_params']['learningrate'] == '':
	    data['train_params']['learningrate']='0.0005'
    if data['train_params']['weightdecay'] == '':
	    data['train_params']['weightdecay']='0.00005'
    if data['train_params']['batchsize'] == '':
	    data['train_params']['batchsize']='24'
    print data['train_params']['batchsize']
    model_parm=data['train_params']['iteration_count']+' '+data['train_params']['learningrate']+' ' \
		+data['train_params']['weightdecay']+' '+data['train_params']['batchsize']
    print model_parm
    change_solver="cd /home/zyy/caffe-ssd/examples/caffe-mobilenetssd && ./change_data.sh "+model_parm
    ch = subprocess.Popen(change_solver, shell=True)
    ch.wait()
    # 开启训练
    train_com = '/home/zyy/caffe-ssd/examples/caffe-mobilenetssd/train.sh'
    train_par = ' '+str(data['worker_id'])+' '+str(data['task_id'])+' '+data['train_params']['iteration_count']
    proc = subprocess.Popen(train_com + train_par, shell=True)
    trainsh_pid[data['task_id']] = proc.pid
    print "trainsh_pid",trainsh_pid
    # 开始处理日志返回
    print data['train_params']['iteration_count']
    itera = " --max_iter=" + str(data['train_params']['iteration_count'])
    workerid = " --worker_id=" + str(data['worker_id'])
    taskiid = " --task_id=" + str(data['task_id'])
    log_py =  ' plot_log.py'
    proc_log = subprocess.Popen("python" + log_py + itera + workerid + taskiid, shell=True)
    return_pid[data['task_id']] = proc_log.pid
    rdata = returntrain.copy()
    return json.dumps(rdata)

@app.route('/api/v1/tasks/master_stop_task', methods = ['GET'])
def stoptask():
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('task_id', type=int, location='args', required=True)
    args = get_parser.parse_args()
    task_id = args.get('task_id')
    print "task id:",task_id
    print "trainsh_pid:",trainsh_pid
    if not trainsh_pid.has_key(task_id):
	print "task id error"
	return 0
    # TODO 验证是否与当前taskid一致
    # TODO 通过进程handle结束进程
    get_trainpid = trainsh_pid[task_id]
    get_returnid = return_pid[task_id]
    print get_trainpid, get_returnid
    img_name = "log_"+str(task_id)+".png"
    K1=subprocess.Popen("pkill -P "+ str(get_trainpid) + " && kill "+ str(get_trainpid), shell=True)
    K1.wait()
    K2=subprocess.Popen("kill "+ str(get_returnid), shell=True)
    K2.wait()
    os.remove(img_name)
    data = returnstoptrain.copy()
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8124)


