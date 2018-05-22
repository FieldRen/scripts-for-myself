# coding=utf-8
'''
    代码放置的目录下，ImageData为图片的目录，xml为生成的xml文件的目录
'''
import json
import xml.dom.minidom
import os
import sys
import time
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

ImgDir = 'ImageData/'
xmlDir = 'xml/'
crop_ImgDir = 'CropImage/'

def call_back(now, total_size):
    # 设置下载进度条
    f = sys.stdout
    pervent = 100.0 * now / total_size
    if pervent > 100.0:
        pervent = 100.0
    percent_str = str("%.2f%%" % pervent)
    n = int(pervent/2)
    ss = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + ss + ']' )
    f.flush()
    f.write('\r')

def cropImage(data):
    imPath = ImgDir + data['image_id'] + '.jpg'
    img = Image.open(imPath)
    crop_imgpath = []
    for i in range(4):
        crop_imgpath.append(crop_ImgDir + data['image_id'] + '_{}.jpg'.format(i))

    for i in range(2):
        for j in range(2):
            crop_img = img.crop((i*data['width']/2., j*data['height']/2., \
                                 (i+1)*data['width']/2., (j+1)*data['height']/2.))
            crop_img.save(crop_imgpath[i*2+j])

    return crop_imgpath


def ctw2xml(CTWFile, train):
    with open(CTWFile, 'rb') as trf:
        trfLines = trf.readlines()
        total = len(trfLines)
        print("start to process {} object".format(total))
        if train:
            Txt = 'train.txt'
        else:
            Txt = 'test.txt'
        Ftrain = open(Txt, 'w')
        has_image = os.listdir(ImgDir)
        for now, TrfLine in enumerate(trfLines):
            call_back(now+1, total)
            data = json.loads(TrfLine)
            if not data['image_id'] + '.jpg' in has_image:
                continue
            
            file_line = xmlFile_generate(data, train)
            Ftrain.write(file_line)
    
        Ftrain.close()
    print('{} has been generated.'.format(Txt))
            
def xmlFile_generate(data, train):
    crop_images = cropImage(data)
    
    file_line = ''
    for i, crop_image in enumerate(crop_images):
        if train:
            doc = ctw_annotations(data['annotations'], True, i, int(data['width']), int(data['height']))
        else:
            doc = ctw_annotations(data['proposals'], False, i, int(data['width']), int(data['height']))

        filename = xmlDir + data['image_id'] + '_{}.xml'.format(i)
        fp = open(filename, 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
        fp.close()
        pwd = os.getcwd()
        img_path = os.path.join(pwd, crop_image)
        xml_path = os.path.join(pwd, filename)
        file_line += img_path + " " + xml_path + '\n'

    return file_line

def ctw_annotations(data, train, idx, width, height):
    doc = xml.dom.minidom.Document() 
    root = doc.createElement('annotation') 
    doc.appendChild(root) 

    for i in range(len(data)):
        if not train:
            nodeobject = xml_create(data[i], doc, False, idx, width, height)
            if nodeobject:
                root.appendChild(nodeobject)
        else:
            for j in range(len(data[i])):
                nodeobject = xml_create(data[i][j], doc, True, idx, width, height)
                if nodeobject:
                    root.appendChild(nodeobject)

    return doc


def xml_create(data, doc, train, idx, width, height):
    nodeobject = doc.createElement('object')
    nodecontent = doc.createElement('content')
    if train:
        nodecontent.appendChild(doc.createTextNode(data['text'].encode('utf-8')))
    else:
        nodecontent.appendChild(doc.createTextNode('###'))

    nodename = doc.createElement('name')
    nodename.appendChild(doc.createTextNode('text'))

    nodebndbox = doc.createElement('bndbox')

    bbox = data['adjusted_bbox']
    xmin_i = int(bbox[0])
    ymin_i = int(bbox[1])
    xmax_i = int(bbox[0] + bbox[2])
    ymax_i = int(bbox[1] + bbox[3])

    if idx < 2 and xmin_i > width/2.:
        return None
    elif idx > 1 and xmax_i < width/2.:
        return None
    elif idx % 2 == 0 and ymin_i > height/2.:
        return None
    elif idx % 2 == 1 and ymax_i < height/2.:
        return None      

    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(xmin_i)))

    ymin = doc.createElement('ymin')
    ymin.appendChild(doc.createTextNode(str(ymin_i)))

    xmax = doc.createElement('xmax')
    xmax.appendChild(doc.createTextNode(str(xmax_i)))

    ymax = doc.createElement('ymax')
    ymax.appendChild(doc.createTextNode(str(ymax_i)))

    for m in range(1,5):
        x = doc.createElement('x{}'.format(m))
        x.appendChild(doc.createTextNode(str(int(data['polygon'][m-1][0]))))

        y = doc.createElement('y{}'.format(m))
        y.appendChild(doc.createTextNode(str(int(data['polygon'][m-1][1]))))

        nodebndbox.appendChild(x)
        nodebndbox.appendChild(y)

    nodebndbox.appendChild(xmin)
    nodebndbox.appendChild(ymin)
    nodebndbox.appendChild(xmax)
    nodebndbox.appendChild(ymax)

    nodeobject.appendChild(nodecontent)
    nodeobject.appendChild(nodename)
    nodeobject.appendChild(nodebndbox)
    return nodeobject


if __name__ == '__main__':
    TrainFile = 'train.jsonl'
    TestFile = 'test_cls.jsonl'
    ctw2xml(TrainFile, True)
    ctw2xml(TestFile, False)
