import os
import shutil


def test(num=9800):
    for i in range(num):
        with open('/Users/mac/Desktop/ahaha/{}.txt'.format(i + 1), 'w') as file:
            file.write('星辰科技')


def func(path, standard):
    filenames = os.listdir(path)
    num = len(filenames)
    i = 1
    while i * standard < num:
        try:
            os.mkdir(os.path.join(path, '{}'.format(i)))
        except FileExistsError:
            pass
        for filename in filenames[(i - 1) * standard:i * standard]:
            shutil.move(os.path.join(path, filename), os.path.join(path, '{}'.format(i)))
        i += 1
        print("移动完成{}个文件".format(i * standard))
    try:
        os.mkdir(os.path.join(path, '{}'.format(i)))
    except FileExistsError:
        pass
    for filename in filenames[(i - 1) * standard:]:
        shutil.move(os.path.join(path, filename), os.path.join(path, '{}'.format(i)))
    print("移动完成{}个文件".format(i * standard))


func("/Users/mac/Desktop/ahaha", 2000)

# test()
