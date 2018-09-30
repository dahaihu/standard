import os
import re
import csv
from urllib.parse import unquote

pic_path = '/Volumes/Seagate Expansion Drive/Siri/186点嘴/186_1/'
txt_path = '/Volumes/Seagate Expansion Drive/Siri/186点嘴/out_mouth_txt/'
res = dict()
csv_path = '/Volumes/Seagate Expansion Drive/Siri/186点嘴/186_1/186_1.csv'
with open(csv_path, 'r', newline='') as file:
    csvfile = csv.reader(file)
    for ind, name in enumerate(csvfile):
        if ind == 0:
            continue
        # 根据图片找答案
        # 还是算了，最好还是根据csv来作为键吧
        imgurl = name[0]
        imgname = re.sub(r'_\d{10}', '', name[0].split('/')[-1])
        txtname = unquote(imgname[:-3]) + 'txt'
        print(imgname, txtname)
        # continue
        print(os.path.join(txt_path, txtname))
        with open(os.path.join(txt_path, txtname), 'r', newline='') as file:
            points = []
            for ind, line in enumerate(file):
                # 第一行去掉，显示的是186
                if ind == 0:
                    continue
                # print('ind is {}, line is {}'.format(ind, line))
                points.append([ind] + [int(ele) for ele in re.split(r'\s*', line.strip())])
            res[imgurl] = [{'index': ind, 'x': x, 'y': y} for ind, x, y in points]
            print('imgurl is {}, points is {}'.format(imgurl, res[imgurl]))
            # print(res[name])
    result = {ind: {'status': 1, 'answer': [{'points': ele}]} for ind, ele in res.items()}
    for key, value in result.items():
        print(f'{key} ==> {value}')
