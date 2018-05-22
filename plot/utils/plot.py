# coding=utf-8
from PIL import Image, ImageDraw

class ImageGroup(object):
    ''' image: Image.Open()得到的对象
        points: 存储格式为[[center_x, center_y, w, h], [...] ... ]
                或[[minx, miny, maxx, maxy], [...] ... ]
        Type: if 1, points is [[center_x, center_y, w, h], [...] ... ]
            if 2, points is [[xmin, ymin, xmax, ymax], [...] ... ]
    '''
    def __init__(self, image, points, Type):
        ''' init parameter '''
        self.image = image
        self.points = points
        self.Type = Type


    def plot(self, vis):
        '''
        画图函数
        vis = True，则直接显示
        vis = False，则保存图片至当前目录res.jpg
        '''
        draw = ImageDraw.Draw(self.image)

        for i in range(len(self.points)):
            if self.Type == 1:
                x1 = self.points[i][0] - self.points[i][2]/2.
                y1 = self.points[i][1] - self.points[i][3]/2.
                x2 = self.points[i][0] + self.points[i][2]/2.
                y2 = self.points[i][1] + self.points[i][3]/2.
                rect = [x1, y1, x2, y2]
            elif self.Type == 2:
                rect = self.points[i]
            else:
                print("No such Type {}".format(self.Type))
                return -1
            
            draw.rectangle(rect)
        
        if vis:
            self.image.show()
        else:
            self.image.save('res.jpg')
