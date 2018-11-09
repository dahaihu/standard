# -*- coding: utf8 -*-

import os
import csv
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from functools import reduce


def draw_point(img, point_list):
    im = Image.open(os.path.join(os.getcwd(), img))
    size = im.size
    mask = Image.new(mode='RGBA', size=size, color='BLACK')
    draw = ImageDraw.Draw(mask, mode='RGBA')

    # point_list = point_list['point']
    for d in point_list:
        if '<父标签0>身体轮廓' in d:
            points = d['<父标签0>身体轮廓'].get('anno')
            points = [(point.get('x'), point.get('y')) for point in points]
            # 多边形填充颜色
            fill = list(ImageColor.getcolor('WHITE', 'RGBA'))
            # 画出多边形
            draw.polygon(points, fill=tuple(fill), outline='BLACK')

        # mask.show()
        elif '<父标签1>缝隙' in d:
            points = d.get('<父标签1>缝隙')
            print('point is {}'.format(points))
            points = [(point.get('x'), point.get('y')) for point in points.get('anno')]
            # 多边形填充颜色
            fill = list(ImageColor.getcolor('BLACK', 'RGBA'))
            # 画出多边形
            draw.polygon(points, fill=tuple(fill), outline='BLACK')

    name = img[:-4] + '-mask.jpg'
    mask.save(os.path.join(os.getcwd(), name), 'PNG')
    mask.close()


error = []


def batch(file):
    with open(file, 'r', encoding='utf-8') as f:
        read = csv.reader(f)
        valid = 0
        invalid = 0
        for line in read:
            # filter the table header
            if line[0] == 'task_id':
                continue

            # download img based on the image url
            name = str(line[0])
            img_url = eval(line[1]).get('image_url')
            img_name = name + '.jpg'

            point_list = eval(line[2])

            with open(img_name, "wb") as img:
                content = requests.get(img_url).content
                img.write(content)

            draw_point(img_name, point_list)
            valid += 1

        print(f'Total number: {valid+invalid}, Valid number: {valid}, Invalid number: {invalid}')


if __name__ == '__main__':
    batch("/Users/mac/Desktop/云测皮肤标注项目_266_1541755882.csv")
    print(error)
