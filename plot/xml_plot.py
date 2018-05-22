from utils.plot import ImageGroup
from PIL import Image
import xml.dom.minidom

dom = xml.dom.minidom.parse('./xml/.xml')
root = dom.documentElement

points = []
for child in root.getElementsByTagName('object'):
    bndbox = child.getElementsByTagName('bndbox')[0]
    xmin = bndbox.getElementsByTagName('xmin')[0].firstChild.data
    ymin = bndbox.getElementsByTagName('ymin')[0].firstChild.data
    xmax = bndbox.getElementsByTagName('xmax')[0].firstChild.data
    ymax = bndbox.getElementsByTagName('ymax')[0].firstChild.data

    point = [xmin, ymin, xmax, ymax]
    points.append(point)

image = Image.open('')

im = ImageGroup(image, points, Type=2)
im.plot(False)
