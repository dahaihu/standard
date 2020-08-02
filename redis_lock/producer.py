# coding: utf8
import redis
import random
import pprint
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from redis_lock.lock import list_item_with_lock, USER, INVENTORY, CONSUMER_BASE, PRODUCERS, CONSUMERS, ITEMS

pool = redis.ConnectionPool()
conn = redis.Redis(connection_pool=pool)


def init(workers, items, consumers):
    """
    worker_id和item_id都是从1开始的
    :param workers: 数字，表示worker的个数
    :param items: 数字，表示的是投放商品的个数
    :return:
    """
    user_items = defaultdict(list)
    for item_id in range(1, items + 1):
        user_id = item_id % workers
        # 在余数为0的时候，这个worker的id是最大的，需要调整
        if user_id == 0:
            user_id = workers
        user_items[user_id].append(item_id)
    pprint.pprint(dict(user_items))
    for i in range(1, workers + 1):
        print INVENTORY.format(user_id=i), user_items[i]
        conn.sadd(INVENTORY.format(user_id=i), *user_items[i])
        conn.hset(USER.format(user_id=i), 'name', USER.format(user_id=i))
        conn.hset(USER.format(user_id=i), 'funds', 10000000000)
    for i in range(consumers):
        consumer_id = i + 1 + CONSUMER_BASE
        user_id = USER.format(user_id=consumer_id)
        conn.hset(user_id, 'name', user_id)
        conn.hset(user_id, 'funds', 10000000000)


def producer(workers, items):
    # 开启一个线程池，用来往市场投放商品，产品id范围给定，产品所属的用户在用户数中随机，价格在1到workers数
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for item_id in range(1, items + 1):
            user_id = item_id % workers
            if user_id == 0:
                user_id = workers
            executor.submit(list_item_with_lock, conn, item_id, user_id, random.randint(1, 10))


if __name__ == '__main__':
    users, items, consumers = PRODUCERS, ITEMS, CONSUMERS
    init(users, items, consumers)
    producer(users, items)
