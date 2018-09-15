import numpy as np
import csv
import cv2
import os

pic_dir = '/Volumes/Seagate Expansion Drive/Siri/59点原图/draw_openpose/'
# show_dir = '/Volumes/STARDUST/pic_show/'
# txt_dir = '/Volumes/STARDUST/txt/'

base_dir = '/Users/mac/Desktop'
index = 0
for path in ['5911_194_1536910217.csv', '5912_195_1536910316.csv', 'new_5909_预标_246_1536920939.csv',
             'new_5910_预标_248_1536921079.csv']:
    # if not path.endswith('csv'):
    #     continue
    # print(f'path is {path}')
    csvFile = open(os.path.join(base_dir, path), "r", newline='', encoding='utf8')
    show_dir = os.path.join(base_dir, path.split('.')[0])
    print("show_dir is {}".format(show_dir))
    if not os.path.isdir(show_dir):
        os.mkdir(show_dir)
    reader = csv.reader(csvFile)
    for item in reader:
        if index == 0:
            index += 1
            continue
        # data_x = []
        # data_y = []
        index_point = 0
        picname = item[1].split('question')[0][47:-19] + '.jpg'
        print("picname is {}".format(picname))
        # txtname = item[1].split('question')[0][47:-19]+'.txt'
        # print(picname)
        # if not reader.line_num == 47:
        #    continue
        if not os.path.isfile(pic_dir + picname):
            continue
        # print(picname)
        img = cv2.imread(pic_dir + picname)
        index += 1
        data_x = [ele.get('x') for ele in eval(item[2])[0].get('points')]
        data_y = [ele.get('y') for ele in eval(item[2])[0].get('points')]
        if len(data_x) != 59:
            with open(os.path.join(base_dir, '非59.csv'), 'a') as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(item)
                print('数字错误 {}'.format(len(data_x)))
                continue
        try:
            for i in range(len(data_x) - 1):
                print(data_x[i], data_y[i])
                cv2.line(img, (int(data_x[i]), int(data_y[i])), (int(data_x[i + 1]), int(data_y[i + 1])), (0, 0, 255),
                         2)
            for i in range(len(data_x)):
                cv2.putText(img, str(i), (int(data_x[i]), int(data_y[i])), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                cv2.circle(img, (int(data_x[i]), int(data_y[i])), 1, (0, 255, 0), 3)
        except TypeError:
            with open(os.path.join(base_dir, 'error.csv'), 'a') as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(item)
                continue

            # cv2.line(img,(int(data_x[i]),int(data_y[i])),(int(data_x[i+1]),int(data_y[i+1])),(255,0,255),2)
        # data_x = item[2].split('y')[1:]
        # data_y = item[2].split('y')
        print(picname)
        # print(type(item[2][1]))
        cv2.imwrite(os.path.join(show_dir, picname), img)
    print(index)
    csvFile.close()
