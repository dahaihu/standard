import threading
from werkzeug.local import Local, LocalStack

l = Local()
print(l.__storage__)


def add_arg(arg, i):
    l.__setattr__(arg, i)


for i in range(3):
    arg = 'arg' + str(i)
    t = threading.Thread(target=add_arg, args=(arg, i))
    t.start()
    t.join()
print(l.__storage__)
