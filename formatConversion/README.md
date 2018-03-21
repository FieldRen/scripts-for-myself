## 数据格式转换脚本

该文件夹下的所有脚本文件都是用来进行数据格式转换的

### icdrtxt2xml.py

TextBoxes_plusplus的caffe检测用的是xml格式的文件([example.xml](./examples/example.xml))，而icdar2015给的ground truth数据格式为txt格式([gt_img_1.txt](./examples/gt_img_1.txt))，所以使用时需要对它进行格式转换。
