import re
import os
import csv
import io
from PIL import Image
import requests
from urllib.parse import unquote

"""
两个的不保存，url单独给出来，格式为csv
84个的也这样 ，分开来保存，也是csv
"""


def filter(x, size):
    if x < 0:
        return 0
    elif x > size:
        return size
    return x


def func(file_path):
    # 根据文件名创建文件夹，然后在文件夹里面存储结果
    dirname, file_name = os.path.split(file_path)
    # 存放结果的路径
    result_path = os.path.join(dirname, file_name.split('.')[0])
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    # # wrong 2
    wrong_path = os.path.join(result_path, 'wrong.csv')
    with open(wrong_path, 'w', encoding='utf8') as wrong:
        wrong.write('image_url\n')
    # # error 非84
    error_path = os.path.join(result_path, 'error.csv')
    with open(error_path, 'w', encoding='utf8') as error:
        error.write('image_url\n')
    with open(file_path, 'r', encoding='utf8') as file:
        csv_reader = csv.reader(file)
        for ind, line in enumerate(csv_reader):
            if ind == 0:
                continue
            image_url = eval(line[1]).get('image_url')
            content = requests.get(image_url).content
            # 要获取图片，然后获取图片大小
            image = Image.open(io.BytesIO(content))
            quoted_image_name = unquote(eval(line[1]).get('image_url').split('/')[-1])
            pattern = re.compile(r'_\d{10}$')
            txt_name = re.sub(pattern, '', quoted_image_name.split('.')[0]) + '.txt'
            print('txt_name is {}'.format(txt_name))
            answer_list = eval(line[-1])[0].get('<父标签0>点').get('anno')
            num = len(answer_list)
            if num == 84:
                with open(os.path.join(result_path, txt_name), 'w', encoding='utf8') as res:
                    res.write('{}\n'.format(num))
                    for point in answer_list:
                        print('point is {}'.format(point))
                        res.write('%.3f   %.3f\n' % (filter(point.get('x'), image.size[0]),
                                                       filter(point.get('y'), image.size[1])))
                continue
            if num == 2:
                with open(error_path, 'a', encoding='utf8') as error:
                    # error.write('{}\n'.format(line))
                    error.write('{}\n'.format(eval(line[1]).get('image_url')))
                continue
            with open(wrong_path, 'a', encoding='utf8') as wrong:
                # wrong.write('{}\n'.format(line))
                wrong.write('{}\n'.format(eval(line[1]).get('image_url')))


path = '/Users/mac/Desktop/tmp'
for file in os.listdir(path):
    if not file.endswith('.csv'):
        continue
    func(os.path.join(path, file))
