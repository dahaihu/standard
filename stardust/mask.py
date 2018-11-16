# -*- coding: utf8 -*-

import os
import csv
from urllib.parse import unquote
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor

colors = ("GREEN", "RED", "BLUE", "YELLOW", "PINK", "THISTLE", "OLIVE")


def draw_point(img, point_list, res_path):
    im = Image.open(os.path.join(os.getcwd(), img))
    size = im.size
    mask = Image.new(mode='RGBA', size=size, color='BLACK')
    draw = ImageDraw.Draw(mask, mode='RGBA')


    # point_list = point_list['point']

    for ind, d in enumerate(point_list):
        if '<父标签0>身体轮廓' in d:
            points = d['<父标签0>身体轮廓']
            if not points:
                continue
            points = [(point.get('x'), point.get('y')) for point in points.get('anno')]
            # 多边形填充颜色
            fill = list(ImageColor.getcolor('WHITE', 'RGBA'))
            # # 多边形填充颜色
            # fill = list(ImageColor.getcolor(colors[ind % 7], 'RGBA'))
            # 画出多边形
            draw.polygon(points, fill=tuple(fill))

        # mask.show()
        elif '<父标签1>缝隙' in d:
            points = d.get('<父标签1>缝隙')
            print('point is {}'.format(points))
            if not points.get('anno'):
                continue
            points = [(point.get('x'), point.get('y')) for point in points.get('anno')]
            # 多边形填充颜色
            fill = list(ImageColor.getcolor('BLACK', 'RGBA'))
            # # 多边形填充颜色
            # fill = list(ImageColor.getcolor(colors[ind % 7], 'RGBA'))
            # 画出多边形
            draw.polygon(points, fill=tuple(fill))

    name = img[:-4] + '-mask.jpg'
    mask.save(os.path.join(res_path, name), 'PNG')
    mask.close()


error = []


def batch(file_path):
    # 创建一个保存渲染好的图片的文件夹
    res_path = os.path.splitext(file_path)[0]
    try:
        os.mkdir(res_path)
        print("创建好了文件夹")
    except Exception as e:
        print("文件夹已经存在")
        pass
    with open(file_path, 'r', encoding='utf-8') as f:
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
            img_name = unquote(img_url.split('/')[-1])

            point_list = eval(line[2])
            print('type point_list is {}'.format(point_list))

            mark_list = ['<父标签0>身体轮廓', '<父标签1>缝隙']
            mark_dict = {ele: ind for ind, ele in enumerate(mark_list)}
            print('mark_dict is {}'.format(mark_dict))

            def func(ele):
                if '<父标签0>身体轮廓' in ele:
                    return mark_dict['<父标签0>身体轮廓']
                elif '<父标签1>缝隙' in ele:
                    return mark_dict['<父标签1>缝隙']
                return 10000

            point_list = sorted(point_list, key=func)

            with open(img_name, "wb") as img:
                content = requests.get(img_url).content
                img.write(content)

            draw_point(img_name, point_list, res_path)
            valid += 1

        print(f'Total number: {valid+invalid}, Valid number: {valid}, Invalid number: {invalid}')


if __name__ == '__main__':
    batch("/Users/mac/Desktop/tmp/pf _256_1541680449.csv")
    print(error)
