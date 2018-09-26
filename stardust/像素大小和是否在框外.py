# anno = [{'color': 'rgba(208,2,27,0.4)', 'points': [{'x': 125, 'y': 188}, {'x': 154, 'y': 188}, {'x': 125, 'y': 212}, {'x': 154, 'y': 212}], 'value': '头'}, {'color': 'rgba(208,2,27,0.4)', 'points': [{'x': 111, 'y': 273}, {'x': 144, 'y': 273}, {'x': 111, 'y': 300}, {'x': 144, 'y': 300}], 'value': '头'}, {'color': 'rgba(208,2,27,0.4)', 'points': [{'x': 395, 'y': 422}, {'x': 420, 'y': 422}, {'x': 395, 'y': 446}, {'x': 420, 'y': 446}], 'value': '头'}, {'color': 'rgba(208,2,27,0.4)', 'points': [{'x': 478, 'y': 445}, {'x': 500, 'y': 445}, {'x': 478, 'y': 468}, {'x': 500, 'y': 468}], 'value': '头'}, {'color': 'rgba(139,87,42,0.4)', 'points': [{'x': 122, 'y': 166}, {'x': 217, 'y': 166}, {'x': 122, 'y': 238}, {'x': 217, 'y': 238}], 'value': '↓、下、南'}, {'color': 'rgba(126,211,33,0.4)', 'points': [{'x': 111, 'y': 257}, {'x': 225, 'y': 257}, {'x': 111, 'y': 313}, {'x': 225, 'y': 313}], 'value': '←、左、西'}, {'color': 'rgba(80,227,194,0.4)', 'points': [{'x': 363, 'y': 373}, {'x': 420, 'y': 373}, {'x': 363, 'y': 448}, {'x': 420, 'y': 448}], 'value': '↘、右下、东南'}, {'color': 'rgba(208,2,27,0.4)', 'points': [{'x': 330, 'y': 441}, {'x': 351, 'y': 441}, {'x': 330, 'y': 460}, {'x': 351, 'y': 460}], 'value': '头'}, {'color': 'rgba(80,227,194,0.4)', 'points': [{'x': 313, 'y': 421}, {'x': 351, 'y': 421}, {'x': 313, 'y': 462}, {'x': 351, 'y': 462}], 'value': '↘、右下、东南'}, {'color': 'rgba(189,16,224,0.4)', 'points': [{'x': 460, 'y': 420}, {'x': 500, 'y': 420}, {'x': 460, 'y': 469}, {'x': 500, 'y': 469}], 'value': '↖、左上、西北'}]
#
# a = {"status": 2, "answer": [{"color": "rgba(255,0,0,0.4)", "points": [{"x": 218.04402087587914, "y": 490.00907646925344}, {"x": 365.96709779895616, "y": 490.00907646925344}, {"x": 218.04402087587914, "y": 733.3167687769458}, {"x": 365.96709779895616, "y": 733.3167687769458}], "value": "\u6446\u59ff\u52bf\u7684\u624b"}, {"color": "rgba(255,0,0,0.4)", "points": [{"x": 356.5055593374176, "y": 484.62446108463814}, {"x": 529.0440208758793, "y": 484.62446108463814}, {"x": 356.5055593374176, "y": 782.547538007715}, {"x": 529.0440208758793, "y": 782.547538007715}], "value": "\u6446\u59ff\u52bf\u7684\u624b"}]}
# for ele in a.get('answer'):
#     print(ele)
import os
import csv
import re
import requests
from io import BytesIO
import unicodedata
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from PIL import ImageFont
from urllib import request
from itertools import cycle

d = {'南': 0, '西': 1, '北': 2, '东': 3, '西南': 4, '东南': 5, '东北': 6,'西北': 7,'头': 8, '脚': 9}
def oldfunc(path):
    result_dir = path.split('/')[-1].split('.')[0]
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)
    with open(path, 'r', newline='') as file:
        csvreader = csv.reader(file)
        c = 0
        for ind, line in enumerate(csvreader):
            if ind == 0:
                continue
            # # 获取图像的url
            url = eval(line[1]).get('image_url')
            resp = requests.get(url)
            # # # 获取图像的内容
            # img = resp.content
            print('url is ', url)
            f = open(url.split('/')[-1], 'wb')
            f.write(resp.content)
            img = Image.open(url.split('/')[-1])
            size = img.size
            print('size is ', size)
            # break
            # 获取所有的点
            for point_list in eval(line[-1]):
                # 获取画一个对象的坐标，和值
                points = [[ele.get('x'), ele.get('y')] for ele in point_list.get('points')]
                value = point_list.get('value').strip()
                print("value is {}".format(value))
                try:
                    if '、' in value:
                        z = d[value.split('、')[-1]]
                    else:
                        z = d[value[-1]]
                except KeyError:
                    continue
                if not isinstance(z, int):
                    print('invalid z is {}'.format(z))
                    return
                # 调整四个点的顺序，可以顺序连一个点
                ind = 0
                for i in range(1, 4):
                    if points[0][0] == points[i][0] or points[0][1] == points[i][1]:
                        continue
                    else:
                        ind = i
                        break
                points[ind], points[2] = points[2], points[ind]
                print(points)
                for point in points:
                    point[0] = size[0] if point[0] > size[0] else point[0]
                    point[1] = size[1] if point[1] > size[1] else point[1]
                final_points = [[min(points[0][0], points[2][0]), min(points[0][1], points[2][1])], [max(points[0][0], points[2][0]), max(points[0][1], points[2][1])]]
                print('final_points', final_points)
                kuan = abs(final_points[0][0] - final_points[1][0])
                gao = abs(final_points[0][1] - final_points[1][1])
                # kuan = abs(points[0][0] - points[2][0])
                # gao = abs(points[0][1] - points[2][1])
                if kuan < 15 or gao < 15:
                    if kuan < 15:
                        final_points[0][0] -= 15 - kuan
                    elif gao < 15:
                        final_points[0][1] -= 15 - gao
                    if final_points[0][0] < 0 and not final_points[0][1] < 0:
                        print(final_points)
                        final_points = [[0, final_points[0][1]], [final_points[1][0]+abs(final_points[0][0]), final_points[1][1]]]
                        print(final_points)
                        print(1)
                        return
                    elif final_points[0][1] < 0 and not final_points[0][0] > 0:
                        print(final_points)
                        final_points = [[final_points[0][0], 0], [final_points[1][0], final_points[1][1] + abs(final_points[0][1])]]
                        print(final_points)
                        print(2)
                        return
                    elif final_points[0][0] < 0 and final_points[0][1] < 0:
                        print(final_points)
                        final_points = [[0, 0], [15, 15]]
                        print(final_points)
                        print(3)
                        return
                kuan = abs(final_points[0][0] - final_points[1][0])
                gao = abs(final_points[0][1] - final_points[1][1])
                # print(url.split('/')[-1].split('.')[0])
                print(re.sub(r'(?<=_0)_\d{10}', '', '.'.join(url.split('/')[-1].split('.')[:-1])) + '.txt')
                with open(result_dir+'/'+re.sub(r'(?<=_0)_\d{10}', '', '.'.join(url.split('/')[-1].split('.')[:-1])) + '.txt', newline='', mode='a') as file:
                    file.write(str(z) + ' ')
                    file.write(str(round((final_points[0][0] + final_points[1][0])/2/size[0], 12)) + ' ')
                    file.write(str(round((final_points[0][1] + final_points[1][1])/2/size[1], 12)) + ' ')
                    file.write(str(round((kuan)/size[0], 12)) + ' ')
                    file.write(str(round((gao)/size[1], 12)))
                    file.write('\n')
        print('error count is ', c)



def newfunc(path):
    result_dir = path.split('/')[-1].split('.')[0]
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)
    with open(path, 'r', newline='') as file:
        csvreader = csv.reader(file)
        c = 0
        for ind, line in enumerate(csvreader):
            if ind == 0:
                continue
            # # 获取图像的url
            url = eval(line[1]).get('image_url')
            resp = requests.get(url)
            # # # 获取图像的内容
            # img = resp.content
            print('url is ', url)
            f = open(url.split('/')[-1], 'wb')
            f.write(resp.content)
            img = Image.open(url.split('/')[-1])
            size = img.size
            print('size is ', size)
            # break
            # 获取所有的点
            for attr in eval(line[-1]):
                print(f'attr is {attr}')
                for value, point_list in attr.items():
                    # # 获取画一个对象的坐标，和值
                    points = [[ele.get('x'), ele.get('y')] for ele in point_list.get('anno')]
                    value = value.strip()
                    print(f'{value}\t{points}')
                    print("value is {}".format(value))
                    try:
                        if '、' in value:
                            z = d[value.split('、')[-1]]
                        else:
                            z = d[value[-1]]
                    except KeyError:
                        continue
                    if not isinstance(z, int):
                        print('invalid z is {}'.format(z))
                        return
                    # 调整四个点的顺序，可以顺序连一个点
                    ind = 0
                    for i in range(1, 4):
                        if points[0][0] == points[i][0] or points[0][1] == points[i][1]:
                            continue
                        else:
                            ind = i
                            break
                    points[ind], points[2] = points[2], points[ind]
                    print(points)
                    for point in points:
                        point[0] = size[0] if point[0] > size[0] else point[0]
                        point[1] = size[1] if point[1] > size[1] else point[1]
                    final_points = [[min(points[0][0], points[2][0]), min(points[0][1], points[2][1])], [max(points[0][0], points[2][0]), max(points[0][1], points[2][1])]]
                    print('final_points', final_points)
                    kuan = abs(final_points[0][0] - final_points[1][0])
                    gao = abs(final_points[0][1] - final_points[1][1])
                    # kuan = abs(points[0][0] - points[2][0])
                    # gao = abs(points[0][1] - points[2][1])
                    if kuan < 15 or gao < 15:
                        if kuan < 15:
                            final_points[0][0] -= 15 - kuan
                        elif gao < 15:
                            final_points[0][1] -= 15 - gao
                        if final_points[0][0] < 0 and not final_points[0][1] < 0:
                            print(final_points)
                            final_points = [[0, final_points[0][1]], [final_points[1][0]+abs(final_points[0][0]), final_points[1][1]]]
                            print(final_points)
                            print(1)
                            return
                        elif final_points[0][1] < 0 and not final_points[0][0] > 0:
                            print(final_points)
                            final_points = [[final_points[0][0], 0], [final_points[1][0], final_points[1][1] + abs(final_points[0][1])]]
                            print(final_points)
                            print(2)
                            return
                        elif final_points[0][0] < 0 and final_points[0][1] < 0:
                            print(final_points)
                            final_points = [[0, 0], [15, 15]]
                            print(final_points)
                            print(3)
                            return
                    kuan = abs(final_points[0][0] - final_points[1][0])
                    gao = abs(final_points[0][1] - final_points[1][1])
                    # print(url.split('/')[-1].split('.')[0])
                    print(re.sub(r'(?<=_0)_\d{10}', '', '.'.join(url.split('/')[-1].split('.')[:-1])) + '.txt')
                    with open(result_dir+'/'+re.sub(r'(?<=_0)_\d{10}', '', '.'.join(url.split('/')[-1].split('.')[:-1])) + '.txt', newline='', mode='a') as file:
                        file.write(str(z) + ' ')
                        file.write(str(round((final_points[0][0] + final_points[1][0]) / 2 / size[0], 12)) + ' ')
                        file.write(str(round((final_points[0][1] + final_points[1][1]) / 2 / size[1], 12)) + ' ')
                        file.write(str(round((kuan) / size[0], 12)) + ' ')
                        file.write(str(round((gao) / size[1], 12)))
                        file.write('\n')
        print('error count is ', c)
oldfunc('/Users/mac/Desktop/结果92.csv')