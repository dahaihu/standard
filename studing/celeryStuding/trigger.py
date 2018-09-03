from tasks import add
from concurrent import futures
import time
import threading
import random

def func(a, b):
    print("{}:::{}=>{}".format(threading.current_thread(), a, b))
    # raise KeyError
    result = add.delay(a, b)
    # while not result.ready():
    #     time.sleep(1)
    # time.sleep(random.randint(1, 10))
    print("task done:{}".format(result.get()))


with futures.ThreadPoolExecutor(10) as executor:
    executor.map(func, [i for i in range(10)], [i for i in range(10)])


# result = add.delay(4, 4)
# while not result.ready():
#     time.sleep(1)
# print("task done:{}".format(result.get()))