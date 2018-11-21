from xml.etree import ElementTree as ET
from urllib.parse import unquote
import csv
import re
import os


def prettyXml(element, indent, newline, level=0):  # element为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text is None or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作


# tree = ET.parse('/Users/mac/Desktop/wangrui 正式_514_1542773894/weblmtImage 487.xml')  # 解析test.xml这个文件，该文件内容如上文
# root = tree.getroot()  # 得到根元素，Element类
# prettyXml(root, '\t', '\n')  # 执行美化方法
# # ET.dump(root)  # 显示出美化后的XML内容
#
# print(ET.tostring(root))


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
    with open(output_path + '.xml', 'r') as old:
        tmp_root = ET.fromstring(old.read())
        # tmp_root = tmp_tree.getroot()  # 得到根元素，Element类
        prettyXml(tmp_root, '\t', '\n')  # 执行美化方法
        with open(output_path + '.xml', 'w') as new:
            # ET.tostring(root))返回的结果是二进制字符串，需要转化为str类型
            new.write(ET.tostring(tmp_root).decode('utf8'))
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


# tree = ET.parse('/Users/mac/Desktop/华科大-2d拉框/试表数据/weblmtImage 010.xml')
#


path = '/Users/mac/Desktop/wangrui 正式_514_1542773894.csv'
dir_name, file_name = os.path.split(path)
res_path = os.path.join(dir_name, file_name.split('.')[0])
if not os.path.exists(res_path):
    os.mkdir(res_path)
for file_name, points in main(path):
    write_to_file(os.path.join(res_path, file_name), points)

# print(ET.tostring(tree))
