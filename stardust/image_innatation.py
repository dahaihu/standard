from io import BytesIO
import unicodedata
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from PIL import ImageFont
from urllib import request
from itertools import cycle

import io


# from dashboard.commons.upload import Upload


# 没有颜色的图片渲染
class ImageAnnotation:
    def __init__(self, url, annotation, name):
        r = request.urlopen(url)
        self.url = url
        self.annotation = annotation
        # 有没有可能不保存图片，直接将二进制的图片渲染，然后上传，免去保存和读取的过程
        self.name = name
        f = open('uploads/' + name + '.png', 'wb')
        f.write(r.read())
        f.close()
        self.img = Image.open('uploads/' + name + '.png')
        self.draw = ImageDraw.Draw(self.img, mode='RGBA')
        self.colors = cycle(
            [(229, 115, 115), (240, 98, 146), (186, 104, 200), (121, 134, 203), (79, 195, 247), (77, 208, 225),
             (77, 182, 172), (255, 241, 118), (255, 183, 77), (161, 136, 127)])

    def draw_rectangle(self, anno, value):
        color = next(self.colors)
        points = [(point.get('x'), point.get('y')) for point in anno]
        # 这个是对矩形的四个坐标进行排序，让这四个点顺序链接的时候，是一个矩形
        # 基本思想是，确定第一个点和第三个点，这两个点的横纵坐标都是不同的
        ind = 0
        for i in range(1, 4):
            if points[0][0] == points[i][0] or points[0][1] == points[i][1]:
                continue
            else:
                ind = i
                break
        points[ind], points[2] = points[2], points[ind]

        # rgb三元组添加个50，代表百分之五十，添加透明度的
        self.draw.polygon(points, fill=color + (50,), outline=color)
        point_1, point_2 = points[0], points[2]
        x = point_1[0] if point_1[0] < point_2[0] else point_2[0]
        y = point_1[1] if point_1[1] < point_2[1] else point_2[1]
        # 设置字体，要不然中文会乱码
        # 这个里面的位置要写相对位置，相对于项目的其实位置，比如说这个项目，那就是从standard之后开始写(注意中间有个之后)
        font = ImageFont.truetype('/home/hsc/下载/simsun.ttc', 18)
        self.draw.text((x, y), value, font=font, fill=(0, 0, 0))

    def export_polygon_rectangle(self):
        """
        包括多边形标注和矩形标注都可以用这个
        :return:
        """
        draw = ImageDraw.Draw(self.img, mode='RGBA')
        # data = self.data.get('point')
        for item in self.annotation:
            color = item.get('color')
            points = item.get('points')
            value = item.get('value')
            # for value, anno in item.items():
            #     self.draw_rectangle(anno.get('anno'), value)
        #  得到图片的 binary 数据
        output = BytesIO()
        self.img.save('uploads/' + 'hehe.png', format='PNG')
        # upload = Upload()
        # url = upload.qiniu_binary_upload('picture', self.name, output.getvalue())
        # print(url)
        # return url


# image_url = 'https://qiniu-test.startask.net/20180822_alipalm2-thumb_down-fheart_0227_136_1537026634.jpg'
# annotation = [{"color": "rgba(255,0,0,0.4)", "points": [{"x": 443.2837693270005, "y": 1082.4650746247853}, {"x": 691.5389083838324, "y": 1082.4650746247853}, {"x": 443.2837693270005, "y": 1499.039439800118}, {"x": 691.5389083838324, "y": 1499.039439800118}], "value": "\u6446\u59ff\u52bf\u7684\u624b"}, {"color": "rgba(255,0,0,0.4)", "points": [{"x": 644.1060184201081, "y": 832.8882910697675}, {"x": 951.5630921806885, "y": 832.8882910697675}, {"x": 644.1060184201081, "y": 1245.9801894978204}, {"x": 951.5630921806885, "y": 1245.9801894978204}], "value": "\u6446\u59ff\u52bf\u7684\u624b"}]
# instance = ImageAnnotation(image_url, annotation, 'test')
# instance.export_polygon_rectangle()

info = {"status": 1, "answer": [{"<\u7236\u6807\u7b7e0>ppl": {
    "anno": [{"x": 381, "y": 283.5}, {"x": 483, "y": 283.5}, {"x": 381, "y": 424.5}, {"x": 483, "y": 424.5}],
    "attr": {"<\u7236\u6807\u7b7e0>ppl": {}}}, "<\u5b50\u6807\u7b7e00>h": {
    "anno": [{"x": 428, "y": 375.5}, {"x": 465, "y": 375.5}, {"x": 428, "y": 412.5}, {"x": 465, "y": 412.5}]},
                                 "<\u5b50\u6807\u7b7e01>f": {"anno": [{"x": 390, "y": 295.5}, {"x": 441, "y": 295.5},
                                                                      {"x": 390, "y": 384.05999999999995},
                                                                      {"x": 441, "y": 384.05999999999995}]}}, {
                                    "<\u7236\u6807\u7b7e0>ppl": {
                                        "anno": [{"x": 223, "y": -8.5}, {"x": 304, "y": -8.5}, {"x": 223, "y": 121.06},
                                                 {"x": 304, "y": 121.06}], "attr": {"<\u7236\u6807\u7b7e0>ppl": {}}},
                                    "<\u5b50\u6807\u7b7e00>h": {
                                        "anno": [{"x": 227, "y": -8.5}, {"x": 278.333984375, "y": -8.5},
                                                 {"x": 227, "y": 27.059999999999995},
                                                 {"x": 278.333984375, "y": 27.059999999999995}]},
                                    "<\u5b50\u6807\u7b7e01>f": {
                                        "anno": [{"x": 258, "y": 42.5}, {"x": 292, "y": 42.5}, {"x": 258, "y": 116.06},
                                                 {"x": 292, "y": 116.06}]}}, {"<\u7236\u6807\u7b7e0>ppl": {
    "anno": [{"x": 433, "y": 21.5}, {"x": 519, "y": 21.5}, {"x": 433, "y": 130.06}, {"x": 519, "y": 130.06}],
    "attr": {"<\u7236\u6807\u7b7e0>ppl": {}}}, "<\u5b50\u6807\u7b7e00>h": {
    "anno": [{"x": 473, "y": 22.5}, {"x": 509, "y": 22.5}, {"x": 473, "y": 73.06}, {"x": 509, "y": 73.06}]},
                                                                              "<\u5b50\u6807\u7b7e01>f": {
                                                                                  "anno": [{"x": 440, "y": 73.5},
                                                                                           {"x": 479, "y": 73.5},
                                                                                           {"x": 440, "y": 131.06},
                                                                                           {"x": 479, "y": 131.06}]}}]}
image_url = 'https://qiniu-test.startask.net/001F7A47E8B0_1524987015.backgroud_0_1537263745.jpg'
for ele in info['answer']:
    print(ele)
    for key, value in ele.items():
        print(key, value)
annotaion = info.get('answer')
instance = ImageAnnotation(image_url, annotaion, 'test')
instance.export_polygon_rectangle()
