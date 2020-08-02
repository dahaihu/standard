# coding: utf8
import redis
import random
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from redis_lock.lock import buy_item, check_exist, CONSUMER_BASE, CONSUMERS, consume_list

pool = redis.ConnectionPool()
conn = redis.Redis(connection_pool=pool)


def consumer(workers=3):
    # 消费者如何消费，这个是需要再考虑的
    with ThreadPoolExecutor(max_workers=workers) as executor:
        tasks = []
        no_item_times = 0
        idx = 0
        while no_item_times <= 10:
            # 通过10此连续的判断
            if not check_exist(conn):
                no_item_times += 1
                continue
            no_item_times = 0
            idx += 1
            buyer_id = idx % workers
            if buyer_id == 0:
                buyer_id = workers
            buyer_id += CONSUMER_BASE
            tasks.append(executor.submit(buy_item, conn, buyer_id))
        wait(tasks, return_when=ALL_COMPLETED)
    print '平均时间{}'.format(sum(consume_list) / len(consume_list))


with ThreadPoolExecutor(max_workers=10) as executor:
    tasks = []
    for i in range(10):
        tasks.append(executor.submit(lambda x, y: (x + y), i, i + 1))
    wait(tasks, return_when=ALL_COMPLETED)
if __name__ == '__main__':
    consumer(CONSUMERS)
