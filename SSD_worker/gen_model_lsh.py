# coding=utf-8
import sys
import os
import re

label_map_file = sys.argv[1]
if not os.path.exists(label_map_file):
    print "Please re-choose label map file."
    sys.exit()
target_str = "label"
count = 0

with open(label_map_file) as f:
    for line in f:
        m = re.search(target_str, line)
        if m is not None:
            count += 1
sh_dir = "/home/zyy/caffe-ssd/examples/caffe-mobilenetssd"
sh_name = "./gen_model.sh "
gen_command = "cd " + sh_dir + " && "+ sh_name + str(count)
os.system(gen_command)
