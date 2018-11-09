import csv
import requests
import io
import json
from PIL import Image
import os

mark = {'起立', '举手', '趴桌', '扭头'}


def batch(file_path):
    # 通过 uft8 进行解码
    with open(file_path, 'r', encoding='utf8') as f:
        read = csv.reader(f)
        for line in read:
            # filter the table header
            if line[0] == 'task_id':
                continue
            # task_id
            task_id = str(line[0])
            # image_url
            img_url = eval(line[1])['image_url']
            # 获取图片的名字
            img_name = img_url.split('/')[-1]

            # 获取文件的大小
            content = requests.get(img_url).content
            img = Image.open(io.BytesIO(content))
            # answer 的数据， 这个point_list是一个列表，里面的元素是字典
            point_list = eval(line[2])
            tmp_dict = {"path": "D:\\项目管理\\智慧课堂项目-试标中\\家瑞标注结果-1107-6张\\img_0000548.jpg",
                        "outputs": {"object":
                                    []},
                        "labeled": True,
                        "size": {
                            "width": img.size[0],
                            "height": img.size[1],
                            "depth": len(img.getbands())
                        }}
            for d in point_list:
                # 对每个字典进行便利
                for k, v in d.items():
                    # 一个字典中最多只有一个标注结果
                    if k[-2:] in mark:
                        points = [(ele.get('x'), ele.get('y')) for ele in v.get('anno')]
                        x_sets = set()
                        y_sets = set()
                        for point in points:
                            x_sets.add(point[0])
                            y_sets.add(point[1])
                        tmp_dict['outputs']['object'].append({
                            "name": k[-2:],
                            "bndbox": {
                                'xmin': min(x_sets),
                                'ymin': min(y_sets),
                                'xmax': max(x_sets),
                                'ymax': max(y_sets)
                            }
                        })
                        break
                # 如果这个字典里面，没有标注的数据，labeled设置为false
                else:
                    tmp_dict['labeled'] = False

            print('resulf path is {}'.format(os.path.dirname(file_path) + '/result.txt'))
            with open(os.path.dirname(file_path) + '/result.txt', 'a') as file:
                file.write(json.dumps(tmp_dict) + '\n')


batch('/Users/mac/Desktop/tmp/Siri-导出测试_273_1541755531.csv')
