import re
import os
import csv
from urllib.parse import unquote


def func(file_path):
    dirname, file_name = os.path.split(file_path)
    result_path = os.path.join(dirname, file_name.split('.')[0])
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    with open(file_path, 'r', encoding='utf8') as file:
        csv_reader = csv.reader(file)
        for ind, line in enumerate(csv_reader):
            if ind == 0:
                continue
            quoted_image_name = unquote(eval(line[1]).get('image_url').split('/')[-1])
            pattern = re.compile(r'_\d{10}$')
            txt_name = re.sub(pattern, '', quoted_image_name.split('.')[0]) + '.txt'
            print('txt_name is {}'.format(txt_name))
            with open(os.path.join(result_path, txt_name), 'w', encoding='utf8') as res:
                answer_list = eval(line[-1])[0].get('<父标签0>1').get('anno')
                num = len(answer_list)
                res.write('{}\n'.format(num))
                for point in answer_list:
                    res.write('{0}   {1}\n'.format(point.get('x'), point.get('y')))


func('/Users/mac/Desktop/猫-生产测试_301_1542364329.csv')
