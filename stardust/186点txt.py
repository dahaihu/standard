import os
import re
from PIL import ImageDraw, ImageFont, Image
path = '/Users/mac/Desktop/test_186'
paths = os.listdir(path)


def export_key_point(img_path, points, path):
    """
    关键点标注数据渲染
    :return:
    """
    # TODO: 需要调整点的大小
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    size = 2
    font = ImageFont.truetype('simsun.ttc', 10)
    for ind, point in enumerate(points):
        if point[0] == 0 and point[1] == 0:
            continue
        draw.ellipse([point[0] - size, point[1] - size, point[0] + size, point[1] + size], fill=(256, 0, 0))
        # draw.text(point, str(ind + 1), font=font, fill=(0, 0, 0))
    # 得到图片的 binary 数据
    output = os.path.join(path, 'result/' + img_path.split('/')[-1] + '.jpg')
    img.save(output, format='PNG')

for ele in paths:
    if not ele.endswith('.txt'):
        continue
    with open(os.path.join(path, ele), 'r', newline='') as file:
        points = []
        for ind, line in enumerate(file):
            # 第一行去掉，显示的事186
            if ind == 0:
                continue
            print('ind is {}, line is {}'.format(ind, line))
            # 不存在文件夹，就创建文件夹
            if not os.path.isdir(os.path.join(path, 'result')):
                os.mkdir(os.path.join(path, 'result'))
            points.append([int(ele) for ele in re.split(r'\s*', line.strip())])
            export_key_point(os.path.join(path, ele.split('.')[0] + '.jpg'), points, path)




