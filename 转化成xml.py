from xml.etree import ElementTree as ET
from urllib.parse import unquote
import csv
import re
import os


def test():
    tree = ET.parse('old.xml')
    root = tree.getroot()
    print(root.tag, root.attrib)
    for child in root:
        print(child.tag, child.attrib)
    print(root.findall('country'))

    newEle = ET.Element('country')
    newEle.attrib = {'name': 'hushichang', 'age': '32'}
    newEle.text = '胡世昌是个大帅哥'
    root.append(newEle)

    tree.write('new.xml')


def write_to_file(output_path, points_list):
    tree = ET.parse('standard.xml')
    root = tree.getroot()
    for point in points_list:
        object = ET.Element('object')
        # 创建三个子节点
        difficult = ET.Element('difficult')
        difficult.text = 'difficult'
        name = ET.Element('name')
        name.text = 'name'
        bndbox = ET.Element('bndbox')

        object.append(difficult)
        object.append(name)
        object.append(bndbox)

        xmin = ET.Element('xmin')
        xmin.text = point.get('xmin')
        ymin = ET.Element('ymin')
        ymin.text = point.get('ymin')
        xmax = ET.Element('xmax')
        xmax.text = point.get('xmax')
        ymax = ET.Element('ymax')
        ymax.text = point.get('ymax')
        bndbox.append(xmin)
        bndbox.append(ymin)
        bndbox.append(xmax)
        bndbox.append(ymax)

        root.append(object)
    # print(ET.tostring(tree))
    tree.write(output_path + '.xml')
    # print(tree.toprettyxml())


def main(csv_path):
    with open(csv_path, 'r', encoding='utf8') as file:
        csvReader = csv.reader(file)
        for ind, line in enumerate(csvReader):
            if ind == 0:
                continue
            url = eval(line[1]).get('image_url')
            name_raw = url.split('/')[-1].split('.')[0]
            name = re.sub(r'_\d{10}$', '', unquote((name_raw)))
            # print(name)

            points = [ele.get('<父标签0>ocr').get('anno') for ele in eval(line[-1])]
            res = []
            for point in points:
                x_set = set()
                y_set = set()
                for ele in point:
                    x_set.add(ele.get('x'))
                    y_set.add(ele.get('y'))
                res.append({'xmin': '%.3f' % min(x_set), 'xmax': '%.3f' % max(x_set), 'ymin': '%.3f' % min(y_set),
                            'ymax': '%.3f' % max(y_set)})
            yield name, res


path = '/Users/mac/Desktop/wangrui 正式_514_1542773894.csv'
dir_name, file_name = os.path.split(path)
res_path = os.path.join(dir_name, file_name.split('.')[0])
if not os.path.exists(res_path):
    os.mkdir(res_path)
for file_name, points in main(path):
    write_to_file(os.path.join(res_path, file_name), points)

# print(ET.tostring(tree))
