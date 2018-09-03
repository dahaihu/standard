import os
import shutil
def func(path, standard):
    filenames = os.listdir(path)
    num = len(filenames)
    i = 1
    while i * standard < num:
        try:
            os.mkdir('{}'.format(i))
        except FileExistsError:
            pass
        for filename in filenames[(i-1)*standard:i*standard]:
            shutil.move(os.path.join(path, filename), '{}'.format(i))
        i += 1
        print("移动完成{}个文件".format(i*standard))
    try:
        os.mkdir('{}'.format(i))
    except FileExistsError:
        pass
    for filename in filenames[(i-1)*standard:]:
        shutil.move(os.path.join(path, filename), '{}'.format(i))
    print("移动完成{}个文件".format(i * standard))
func("test", 10)

# shutil.move("test.json", '1')

# import os
# os.mkdir('test')
# for i in range(100):
#     with open(os.path.join('test', "{}.txt".format(i+1)), 'w') as file:
#         file.write(str(i))