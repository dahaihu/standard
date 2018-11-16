# -*- coding: utf8 -*-
from io import BytesIO
from itertools import cycle
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from PIL import ImageFont
from urllib import request
import io
import base64
from dashboard.commons.upload import Upload
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class ImageAnnotation:
    def __init__(self, url, annotation, name):
        self.num = 0
        r = request.urlopen(url)
        self.url = url
        self.annotation = annotation
        self.name = name
        self.img = Image.open(BytesIO(r.read()))
        self.draw = ImageDraw.Draw(self.img, mode='RGBA')
        self.colors = [(255, 20, 147, 60), (0, 0, 255, 60), (186, 104, 200, 60), (121, 134, 203, 60),
                       (79, 195, 247, 60),
                       (77, 208, 225, 60), (77, 182, 172, 60), (255, 241, 118, 60), (255, 183, 77, 60),
                       (161, 136, 127, 60)]

    # 传入三个值，矩形列表，标注的值，颜色，
    def draw_rectangle(self, anno, value, color=None):
        # color = next(self.colors)
        color = color if color else self.colors[self.num % (len(self.colors))]
        self.num += 1
        points = [(point.get('x'), point.get('y')) for point in anno]
        ind = 0
        for i in range(1, 4):
            if points[0][0] == points[i][0] or points[0][1] == points[i][1]:
                continue
            else:
                ind = i
                break
        points[ind], points[2] = points[2], points[ind]
        # fill指的事填充的颜色，outline指的时候边界颜色
        # fill color + (50,) 最后添加的一个50，指的是添加一个透明度
        self.draw.polygon(points, fill=color, outline=color[:-1])
        point_1, point_2 = points[0], points[2]
        x = point_1[0] if point_1[0] < point_2[0] else point_2[0]
        y = point_1[1] if point_1[1] < point_2[1] else point_2[1]
        font = ImageFont.truetype('dashboard/commons/simsun.ttc', 18)
        self.draw.text((x, y), value, font=font, fill=(0, 0, 0))

    def export_polygon_rectangle(self):
        """
        包括多边形标注和矩形标注都可以用这个
        :return:
        """
        for item in self.annotation:
            if 'points' in item:
                # 需要将
                colorString = item.get('color')[5:-1]
                colorList = colorString.split(',')
                # 对颜色进行转换，最后一个需要乘以100 并转化为整数
                colorTmp = [int(ele) if '.' not in ele else int(float(ele) * 100) for ele in colorList]
                color = tuple(colorTmp)
                points = item.get('points')
                value = item.get('value')
                self.draw_rectangle(points, value, color)
            else:
                for value, anno in item.items():
                    self.draw_rectangle(
                        anno.get('anno').get('points') if isinstance(anno.get('anno'), dict) else anno.get('anno'),
                        value)
        # 得到图片的 binary 数据
        output = BytesIO()
        self.img.save(output, format='PNG')
        return base64.b64encode(output.getvalue())

    def export_polygon(self):
        """
        新的数据格式
        :return:
        """
        mark = []

        # 招到所有的标签，添加到mark之中
        # 每个data是一个字典
        for data in self.annotation:
            for key in data:
                if key == 'attr':
                    continue
                elif key not in mark:
                    mark.append(key)
                points = [(ele.get('x'), ele.get('y')) for ele in data[key].get('anno')]
                self.draw.polygon(points, fill=self.colors[mark.index(key)], outline=self.colors[mark.index(key)])

        # 得到图片的 binary 数据
        output = BytesIO()
        self.img.save(output, format='PNG')
        return base64.b64encode(output.getvalue())

    def export_key_point(self):
        """
        关键点标注数据渲染
        :return:
        """
        # TODO: 需要调整点的大小
        size = 2
        for point in self.annotation:
            # value = point.get('value')
            color = point.get('color')
            # points = [(point.get('x') - size, point.get('y') - size, point.get('x') + size, point.get('y') + size) for
            #           point in point.get('points')]
            # 每个点的前两个元素存ｘｙ，　后一个元素为index
            points = [(p.get('x'), p.get('y'), p.get('index')) for p in point.get('points')]
            font = ImageFont.truetype('dashboard/commons/simsun.ttc', 10)
            for point in points:
                if not point[0] or not point[1]:
                    continue
                # 通过以圆圈的形式标注点
                self.draw.ellipse([point[0] - size, point[1] - size, point[0] + size, point[1] + size], fill=color)
                # 给点添加序号，用的是黑色
                self.draw.text(point[:-1], str(point[-1]), font=font, fill=(0, 0, 0))
            # 画线, 只有在一个点的ｘ和ｙ均存在的时候再上传，线用的是红色
            self.draw.line([point[:-1] for point in points if point[0] and point[1]], fill=(255, 0, 0))
        # 得到图片的 binary 数据
        output = BytesIO()
        self.img.save(output, format='PNG')
        # upload = Upload()
        # url = upload.qiniu_binary_upload('picture', self.name, output.getvalue())
        # print(url)
        # return url
        return base64.b64encode(output.getvalue())

    def export_key_point_new(self):
        """
        新的数据格式的 打点
        :return:
        """
        # TODO: 需要调整点的大小
        size = 2
        for data in self.annotation:
            for value in data.values():
                if not value.get('anno'):
                    continue
                points = [(ele.get('x'), ele.get('y')) for ele in value.get('anno')]
                font = ImageFont.truetype('dashboard/commons/simsun.ttc', 10)
                for ind, point in enumerate(points):
                    if not point[0] or not point[1]:
                        continue
                    # 通过以圆圈的形式标注点
                    self.draw.ellipse([point[0] - size, point[1] - size, point[0] + size, point[1] + size])
                    # 给点添加序号，用的是黑色
                    self.draw.text(point, str(ind + 1), font=font, fill=(0, 0, 0))
        # 得到图片的 binary 数据
        output = BytesIO()
        self.img.save(output, format='PNG')
        return base64.b64encode(output.getvalue())
