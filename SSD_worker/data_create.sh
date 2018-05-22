#!/bin/bash

data_rootdir="$HOME/data/VOCdevkit/mydataset"
cp -r $1 $data_rootdir
file_dir=$(basename $1)

anno_type="detection" 
label_type="xml" 

dataset_dir="$data_rootdir/$file_dir/filelist"
mapfile="$dataset_dir/labelmap_voc.prototxt" 
train_val="$dataset_dir/filelist.txt"
lmdb_dir="$HOME/caffe-ssd/examples/caffe-mobilenetssd"
db="lmdb"

check_label="True" 
min_dim=0 
max_dim=0 
resize_height=0 
resize_width=0 
backend="lmdb" 
shuffle="False" 
check_size="False" 
extra_cmd="--encode_type=jpg --encoded=True"

for lsh_mode in test trainval
do
    rm -r $lmdb_dir/$lsh_mode"_"$db
    $HOME/caffe-ssd/build/tools/convert_annoset --anno_type=$anno_type --label_map_file=$mapfile \
    --min_dim=$min_dim --max_dim=$max_dim --resize_width=$resize_width \
    --resize_height=$resize_height --check_label $extra_cmd $dataset_dir/../ \
    $dataset_dir/$lsh_mode.txt $lmdb_dir/$lsh_mode"_"$db
done

python gen_model_lsh.py $mapfile
rm -r $data_rootdir/$file_dir
