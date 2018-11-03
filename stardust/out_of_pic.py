# -*- coding: utf8 -*-

from PIL import Image
import os
greater = 0


def out_of_pic(file):
    pic_path = '/Users/mac/Downloads/img_20181026_five'
    global greater
    write_data = []
    wrong_data = []
    with open(f'/Users/mac/Desktop/{file}', 'r', encoding='utf8') as reader:
        for line in reader:
            write_single = []
            line = line[:-1]
            dealer = line.split(' ')

            url = dealer[0]
            image = Image.open(os.path.join(pic_path, url))
            size = image.size
            total = dealer[1]
            write_single.append(url)
            write_single.append(total)
            data = dealer[2:]
            length = len(data)
            left = length % 5
            # 如果余数为0 代表长度有问题
            if left:
                wrong_data.append(line)
                continue
            round_num = int(length / 5)
            # 然后进行判断赋值
            for i in range(round_num):
                start = i * 5
                end = start + 5
                # 这个inner代表一个框
                inner = data[start:end]

                # 这个部分是对长度做判断
                if int(inner[1]) > size[0]:
                    inner[1] = str(size[0])
                    greater += 1
                    print('gotcha')

                if int(inner[2]) > size[1]:
                    inner[2] = str(size[1])
                    greater += 1
                    print('gotcha')

                if int(inner[3]) > size[0]:
                    inner[3] = str(size[0])
                    greater += 1
                    print('gotcha')

                if int(inner[4]) > size[1]:
                    inner[4] = str(size[1])
                    greater += 1
                    print('gotcha')

                # 这个地方是对宽度做判断


                data[start:end] = inner
            write_single.extend(data)
            write_data.append(' '.join(write_single))
    with open(f'/Users/mac/Desktop/right-{file}', 'w', encoding='utf8') as right, \
            open(f'/Users/mac/Desktop//wrong-{file}', 'w', encoding='utf8') as wrong:
        for item in write_data:
            right.write(item + '\n')
        for item in wrong_data:
            wrong.write(item + '\n')


if __name__ == '__main__':
    out_of_pic('five.txt')
    # print(greater)
