# encoding: utf8

import time
import threading
from redis import Redis

redis_conn = Redis()


def no_trans():
    print redis_conn.incr("no_trans:")
    time.sleep(0.1)
    redis_conn.incr("no_trans:", -1)


def trans():
    pipeline = redis_conn.pipeline()
    pipeline.incr("trans:")
    time.sleep(0.1)
    pipeline.incr("trans:", -1)
    print pipeline.execute()[0]


def test(func):
    threads = []
    # 启动线程
    for i in range(3):
        thread = threading.Thread(target=func)
        thread.start()
        threads.append(thread)

    # 等待线程执行完成
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    test(trans)
