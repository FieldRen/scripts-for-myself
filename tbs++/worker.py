# coding=utf-8
import numpy as np
from flask import Flask, request
import json
import subprocess
import sched
import time
import urllib2

config = {
    'dir': '/home/zyy/TextBoxes_plusplus/',
    'demo_py': 'examples/text/demo.py',
    'Image': 'demo_images/demo.jpg',
    'result': 'demo_images/recognition_result/demo.txt',
}

returnstatus = {}
header = {"Content-Type": "application/json"}
s = sched.scheduler(time.time, time.sleep)

app = Flask(__name__)

@app.route('/api/v1/trainimages/create', methods=['POST'])
def create():
    data = json.loads(request.data)
    print data
    global url
    url = data['notify_ip']
    returnstatus['worker_id'] = data['worker_id']
    returnstatus['task_id'] = data['task_id']
    returnstatus['handle_status'] = 'solved'
    returnstatus['percent'] = 1.0
    demo_dir = config['dir'] + config['demo_py']
    demo_img = config['dir'] + config['Image']
    mvImg = subprocess.Popen('mv ' + data['image_dir'] +' '+ demo_img, shell=True)
    mvImg.wait()
    TextDemo = subprocess.Popen('python ' + demo_dir, shell=True)
    TextDemo.wait()
    text_data = {}
    index = 0
    with open(config['dir'] + config['result'], 'r') as f:
        for line in f.readlines():
            _text = {}
            line = line.strip()
            x1 = int(line.split(',')[0])
            y1 = int(line.split(',')[1])
            x2 = int(line.split(',')[2])
            y2 = int(line.split(',')[3])
            x3 = int(line.split(',')[4])
            y3 = int(line.split(',')[5])
            x4 = int(line.split(',')[6])
            y4 = int(line.split(',')[7])
            rec_str = line.split(',')[9]
            axis = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            _text['axis'] = axis
            _text['rec_str'] = rec_str
            text_data[index] = _text
            index += 1
    returnstatus['ax_str'] = text_data
    encoded_data = json.JSONEncoder().encode(returnstatus)
    s.enter(5, 1, post_10s, (encoded_data,))
    s.run()

    return json.dumps(text_data)

def post_10s(encoded_data):
    print url
    try:
        req = urllib2.Request(url=url, data=encoded_data, headers=header)
        responce = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e
        s.enter(5, 1, post_10s, (encoded_data,))
    else:
        print 'post have done.'

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8123)
