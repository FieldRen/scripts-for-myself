import os
import sys

def readFile(file_dir):
    for file in os.listdir(file_dir):
        if not os.path.isdir(file) and file[-3:] == 'txt':
            txt2xml(file_dir, file)
                

def txt2xml(file_dir, file):
    xmls_dir = os.path.join(file_dir, 'xmls')
    if not os.path.exists(xmls_dir):
        os.mkdir(xmls_dir)

    xmlFile = file[:-4] + '.xml'
    xmlDir = os.path.join(xmls_dir, xmlFile)
    xml = open(xmlDir, 'w')
    xml.write('<annotation>\n')
    with open(os.path.join(file_dir,file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line = line.replace('\xef\xbb\xbf', '')
            coord = line.split(',')
            vertex = compoint(coord)
            xml.write('	<object>\n')
            xml.write('		<content>{0}</content>\n'.format(coord[-1]))
            xml.write('		<name>text</name>\n')
            xml.write('		<bndbox>\n')
            xml.write('\
            <x1>{0[0]}</x1>\n\
            <y1>{0[1]}</y1>\n\
            <x2>{0[2]}</x2>\n\
            <y2>{0[3]}</y2>\n\
            <x3>{0[4]}</x3>\n\
            <y3>{0[5]}</y3>\n\
            <x4>{0[6]}</x4>\n\
            <y4>{0[7]}</y4>\n\
            <xmin>{1[0]}</xmin>\n\
            <ymin>{1[1]}</ymin>\n\
            <xmax>{1[2]}</xmax>\n\
            <ymax>{1[3]}</ymax>\n'.format(coord, vertex))
            xml.write('		</bndbox>\n')
            xml.write('	</object>\n')
    xml.write('</annotation>\n')
    xml.close()   

def compoint(coord):
    x = [coord[0], coord[2], coord[4], coord[6]]
    y = [coord[1], coord[3], coord[5], coord[7]]  
    return [min(x), min(y), max(x), max(y)]  

def CreateFileList(file_dir, image_dir):
    xml_dir = os.path.join(file_dir, 'xmls')
    count = 0
    with open('../text/train.txt', 'w') as tr:
        with open('../text/test.txt', 'w') as te:
            for file in os.listdir(xml_dir):
                if file[-3:] == 'xml':
                    count += 1
                    image = os.path.join(image_dir,'img_%s.jpg'%(file[7:-4]))
                    if not os.path.exists(image):
                        print file
                        print image,' is not exist.'
                        continue
                    Real_img = os.path.realpath(image)
                    xmlDir = os.path.realpath(os.path.join(xml_dir, file))
                    if count > 100:
                        tr.write(Real_img)
                        tr.write(' ' + xmlDir + '\n')
                    else:       
                        te.write(Real_img)
                        te.write(' ' + xmlDir + '\n')


if __name__ == '__main__':
    file_dir = './local_gt'
    image_dir = './image'
    readFile(file_dir)
    CreateFileList(file_dir, image_dir)
