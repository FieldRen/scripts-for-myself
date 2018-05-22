# coding:utf-8

import caffe.proto.caffe_pb2 as caffe_pb2

caffemodel_filename = './models/model_pre_train_syn.caffemodel'

model = caffe_pb2.NetParameter()

f = open(caffemodel_filename, 'rb')
model.ParseFromString(f.read())
f.close()

import sys
old=sys.stdout
save_filename = 'caffemodel.prototxt' 
sys.stdout=open( save_filename, 'w')
print model.__str__
sys.stdout=old
f.close()

import os
cmd_1 = 'sed -i "1s/^.\{38\}//" ' + save_filename     # 删除第一行前面38个字符
cmd_2 = "sed -i '$d' " + save_filename      # 删除最后一行
os.system(cmd_1)
os.system(cmd_2)

# 打开刚刚存储的文件，输出里面的内容，输出时过滤掉“blobs”块和"phase: TRAIN"行。
f=open(save_filename, 'r')
lines = f.readlines()
f.close()
wr = open(save_filename, 'w')
now_have_blobs = False
nu = 1
for line in lines:
    #print nu
    nu = nu + 1
    content = line.strip('\n')

    if (content == '  blobs {'):
        now_have_blobs = True
    elif (content == '  }' and now_have_blobs==True):
        now_have_blobs = False
        continue

    if (content == '  phase: TRAIN'):
        continue
        
    if (now_have_blobs):
        continue
    else:
        wr.write(content+'\n')
wr.close()