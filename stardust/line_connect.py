import numpy as np
import csv
import cv2
import os

base_dir = '/media/hsc/Seagate Expansion Drive/Siri/59点原图'
pic_dir = '/media/hsc/Seagate Expansion Drive/Siri/59点原图/draw_openpose/'
show_dir = '/media/hsc/Seagate Expansion Drive/Siri/59点原图/new_5908/'
# txt_dir = '/Volumes/STARDUST/txt/'

index = 0
csvFile = open("/media/hsc/Seagate Expansion Drive/Siri/59点原图/new_5908.csv", "r")
reader = csv.reader(csvFile)
for item in reader:
    data_x = []
    data_y = []
    index_point = 0
    picname = item[1].split('question')[0][47:-19] + '.jpg'
    txtname = item[1].split('question')[0][47:-19] + '.txt'
    # f = open(txt_dir+txtname,'w')
    # print(picname)
    # if not reader.line_num == 47:
    #    continue
    if not os.path.isfile(pic_dir + picname):
        continue
    # print(picname)
    img = cv2.imread(pic_dir + picname)
    index += 1
    data = item[2].split('{')[2:]
    # print(data)
    for i in range(len(data)):
        data_point = data[i].split(',')
        print(data_point)
        print(len(data_point))
        if len(data_point) == 2:
            data_x.append(data_point[0][5:].split('.')[0].strip())
            data_y.append(data_point[1].split('}')[0][6:].split('.')[0].strip())
            # print(data_x)
            # print(data_y)
        if len(data_point) == 3:
            # print(data_point[1][6:])
            # print(data_point[2].split('}')[0][6:])
            data_x.append(data_point[1][5:].split('.')[0].strip())
            data_y.append(data_point[2].split('}')[0][6:].split('.')[0].strip())
            # index_point += 1
        if len(data_point) == 4:
            # print(data_point[2][6:-1])
            # print(data_point[1][6:])
            data_x.append(data_point[1][6:].split('.')[0].strip())
            data_y.append(data_point[2][6:-1].split('.')[0].strip())
            # index_point += 1
    # print(data_x)
    # print(index_point)
    # print(data_y)
    # f.write(picname+' '+str(len(data_x))+'\n')
    try:
        for i in range(len(data_x) - 1):
            print(data_x[i], data_y[i])
            cv2.line(img, (int(data_x[i]), int(data_y[i])), (int(data_x[i + 1]), int(data_y[i + 1])), (0, 0, 255), 2)
        for i in range(len(data_x)):
            # f.write(str(data_x[i]) + ' ' + str(data_y[i]) + '\n')
            cv2.putText(img, str(i), (int(data_x[i]), int(data_y[i])), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            cv2.circle(img, (int(data_x[i]), int(data_y[i])), 1, (0, 255, 0), 3)
            # cv2.line(img,(int(data_x[i]),int(data_y[i])),(int(data_x[i+1]),int(data_y[i+1])),(255,0,255),2)
    except ValueError:
        with open(os.path.join(base_dir, 'error.csv'), 'a') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(item)
        continue
    # data_x = item[2].split('y')[1:]
    # data_y = item[2].split('y')
    print(picname)
    # f.close()
    # print(type(item[2][1]))
    cv2.imwrite(show_dir + picname, img)
print(index)
csvFile.close()

# import os
# import csv
# mark = set()
# with open("/media/hsc/Seagate Expansion Drive/Siri/59点原图/error.csv", 'r') as file:
#     reader = csv.reader(file)
#     for ele in reader:
#         mark.add(ele[0])
#
# paths = os.listdir('/media/hsc/Seagate Expansion Drive/Siri/59点原图/')
# for path in paths:
#     if (not path.endswith('csv')) or path == 'error.csv':
#         continue
#     print("current path is {}".format(path))
#     with open(os.path.join('/media/hsc/Seagate Expansion Drive/Siri/59点原图', path), 'r') as file:
#         csvreader = csv.reader(file)
#         for ele in csvreader:
#             if ele[0] in mark:
#                 continue
#             with open(os.path.join('/media/hsc/Seagate Expansion Drive/Siri/59点原图', 'new_' + path), 'a') as f:
#                 csvwriter = csv.writer(f)
#                 csvwriter.writerow(ele)
