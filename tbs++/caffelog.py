#coding=utf-8
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from itertools import islice
import os
import argparse


description = {"This py is create for return logfile"}
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--logfile', default="VGG_text_text_polygon_precise_fix_order_384x384.log", type=str, 
		   help="log file name.")
args = parser.parse_args()
img_name = args.logfile +'.png'

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

log_dir = '/home/zyy/TextBoxes_plusplus/tools/extra/'
test_log_path=args.logfile + '.test'
train_log_path=args.logfile + '.train'
get_log = '/home/zyy/TextBoxes_plusplus/tools/extra/parse_log.sh ' + args.logfile
os.system(get_log)
plog(train_log_path, test_log_path)

