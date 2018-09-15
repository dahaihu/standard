import os
import csv
import re
mark_path = '/media/hsc/STARDUST2/draw_openpose_7787.csv'
original_path = '/media/hsc/STARDUST2/59点-第一波289题_108_1535627964.csv'
to_file = '/media/hsc/STARDUST2/res.csv'
a = set()

with open(original_path, 'r', newline='') as file:
    csv_file = csv.reader(file)
    for ind, ele in enumerate(csv_file):
        print("{}".format(ind))
        if ind == 0:
            continue
        image_url = eval(ele[1]).get('image_url')
        # print(image_url)
        # 根据image_url 去掉时间，获得文件名字
        tmp = re.sub(r'_\d{10}', '', image_url.split('/')[-1])
        print(tmp)
        a.add(tmp)
        # if ind == 0:
        #     with open(to_file, 'w', newline='') as file:
        #         writer = csv.writer(file)
        #         writer.writerow(ele)
        # if ind != 0:
        #     image_url = eval(ele[1]).get('image_url')
        #     tmp = re.sub(r'_\d{10}', '', ele[-1].split('/')[-1])
        #     if tmp in a:
        #         continue
        #     with open(to_file, 'a', newline='') as file:
        #         writer = csv.writer(file)
        #         writer.writerow(ele)

with open(mark_path, 'r', newline='') as file:
    csv_file = csv.reader(file)
    count = 0
    for ind, ele in enumerate(csv_file):
        print("正在判断第{}个".format(ind))
        if ind == 0:
            with open(to_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(ele)
            continue
        # print(ele[-1].split('/')[-1])
        tmp = re.sub(r'_\d{10}', '', ele[0].split('/')[-1])
        if tmp not in a:
            with open(to_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(ele)
                continue
        if tmp in a:
            count += 1
    print("过滤掉{}".format(count))
    print("对照length {}".format(len(a)))




