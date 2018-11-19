import re
import os
import csv
from urllib.parse import unquote

"""
两个的不保存，url单独给出来，格式为csv
84个的也这样 ，分开来保存，也是csv
"""


def func(file_path):
    dirname, file_name = os.path.split(file_path)
    result_path = os.path.join(dirname, file_name.split('.')[0])
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    # wrong 2
    wrong_path = os.path.join(result_path, 'wrong.csv')
    with open(wrong_path, 'w', encoding='utf8') as wrong:
        wrong.write('image_url\n')
    # error 非84
    error_path = os.path.join(result_path, 'error.csv')
    with open(error_path, 'w', encoding='utf8') as error:
        error.write('image_url\n')
    with open(file_path, 'r', encoding='utf8') as file:
        csv_reader = csv.reader(file)
        for ind, line in enumerate(csv_reader):
            if ind == 0:
                continue
            quoted_image_name = unquote(eval(line[1]).get('image_url').split('/')[-1])
            pattern = re.compile(r'_\d{10}$')
            txt_name = re.sub(pattern, '', quoted_image_name.split('.')[0]) + '.txt'
            print('txt_name is {}'.format(txt_name))
            answer_list = eval(line[-1])[0].get('<父标签0>1').get('anno')
            num = len(answer_list)
            if num == 84:
                with open(os.path.join(result_path, txt_name), 'w', encoding='utf8') as res:
                    res.write('{}\n'.format(num))
                    for point in answer_list:
                        print('point is {}'.format(point))
                        res.write('{0}   {1}\n'.format(point.get('x'), point.get('y')))
                continue
            if num == 2:
                with open(error_path, 'a', encoding='utf8') as error:
                    # error.write('{}\n'.format(line))
                    error.write('{}\n'.format(eval(line[1]).get('image_url')))
                continue
            with open(wrong_path, 'a', encoding='utf8') as wrong:
                # wrong.write('{}\n'.format(line))
                wrong.write('{}\n'.format(eval(line[1]).get('image_url')))


func('/Users/mac/Desktop/猫-生产测试_301_1542364329.csv')
