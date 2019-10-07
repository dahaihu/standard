import uuid
import time
import redis
from string import ascii_letters
import multiprocessing
import threading
from random import choice
import random
from itertools import product

MARKET = 'market:'
ITEM_NAME = '{item_name}.{producer_id}'

manager = multiprocessing.Manager()
market_dict = manager.dict()
consume_time_sequence = manager.list()


def acquire_lock(conn, lockname, acquier_timeout=10):
    identifier = str(uuid.uuid4())
    end = time.time() + acquier_timeout
    while time.time() < end:
        if conn.setnx('lock:' + lockname, identifier):
            return identifier
        print('获取锁失败')
        time.sleep(0.001)
    return False


def purchase_item_with_lock(conn, buyerid, itemid, sellerid):
    buyer = "users:%s" % buyerid
    seller = "users:%s" % sellerid
    item = "%s.%s" % (itemid, sellerid)
    inventory = "inventory:%s" % buyerid
    locked = acquire_lock(conn, "market")
    if not locked:
        return False
    pipe = conn.pipeline(True)

    try:
        pipe.zscore("market:", item)
        pipe.hget(buyer, 'funds')
        price, funds = pipe.execute()
        print('item is {}, price is {}, funds is {}'.format(item, price, funds))
        if price is None or price > int(funds.decode('utf8')):
            # 为什么有的price会是None呢, 因为已经被购买了
            print('price is {}, funds is {}'.format(price, funds))
            return None
        pipe.hincrby(seller, 'funds', int(price))
        pipe.hincrby(buyer, 'funds', -int(price))
        pipe.sadd(inventory, itemid)
        pipe.zrem("market:", item)
        pipe.execute()
        return True
    except Exception as e:
        print("exception is ", e)
    finally:
        release_lock(conn, "market", locked)


def release_lock(conn, lockname, identifier):
    pipe = conn.pipeline(True)
    lockname = 'lock:' + lockname
    while True:
        try:
            pipe.watch(lockname)
            print(conn.get(lockname), identifier)
            if conn.get(lockname).decode('utf8') == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True
            print('release_lock 失败')
            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            pass
    return False


produced_items = []
name_generator = product(ascii_letters, repeat=10)


def produce(producer_id, timeout=3):
    """
    :param conn: redis连接
    :param producers: 生产者的数量
    :param timeout: 用于生产的时间
    :return:
    """
    end = time.time() + timeout
    conn = redis.Redis()
    while time.time() < end:
        price = random.randint(0, 100)
        name = "".join(next(name_generator))
        locked = acquire_lock(conn, 'market', acquier_timeout=10)
        if not locked:
            continue
        try:
            conn.zadd(MARKET, {ITEM_NAME.format(item_name=name, producer_id=producer_id): price})
            produced_items.append([ITEM_NAME.format(item_name=name, producer_id=producer_id), price])
        finally:
            release_lock(conn, 'market', locked)


def consume(buyer_id):
    """
    开启一个独立的进程用来消费
    :param buyer_id:
    :return:
    """
    conn = redis.Redis()
    print('length is {}'.format(conn.zcard(MARKET)))
    print('market\'s items is ', conn.zrange(MARKET, 0, -1))
    buyer = "users:%s" % buyer_id
    # 给每个消费者初始化的钱
    conn.hset(buyer, 'funds', pow(2, 30) - 1)
    while conn.zcard(MARKET) != 0:
        # 相当于在用户浏览所有项目的时候，随机从中间选择一个进行购买
        choosed_item = choice(conn.zrange(MARKET, 0, -1)).decode('utf8')
        print('choosed_item is ', choosed_item)
        item_id, producer_id = choosed_item[:-2], choosed_item[-1:]
        start_time = time.time()
        succesed = purchase_item_with_lock(conn, buyer_id, item_id, producer_id)
        if succesed:
            print("消费成功")
        else:
            print("消费失败")
        print('消费时间长度为{}'.format(time.time() - start_time))
        consume_time_sequence.append(time.time() - start_time)


def sing():
    for i in range(3):
        print("正在唱歌...%d" % i)
        time.sleep(1)
    print("唱歌子线程结束")


def dance():
    for i in range(3):
        print("正在跳舞...%d" % i)
        time.sleep(1)
    print("跳舞子线程结束")


def test_threading():
    print('主线程---开始时间---:%s' % time.ctime())

    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)

    # 如果子线程调用join，主线程会等待子线程执行完成
    # 也就是如果按照下面的来调用，和使用单线程没区别，是顺序执行的t1执行完成才会执行t2
    t1.start()
    t1.join()

    t2.start()
    t2.join()

    print('主线程---结束时间---:%s' % time.ctime())


def test_distributed_lock(producer_num, consume_num):
    threads = []
    for i in range(producer_num):
        p = threading.Thread(target=produce, args=(i,))
        p.start()
        threads.append(p)
    for i in range(consume_num):
        p = threading.Thread(target=consume, args=(10 - i,))
        p.start()
        threads.append(p)
    for thread in threads:
        thread.join()
    print('proudcedItems\'s is {}, 去重之后的长度为{}'.format(len(produced_items), len(dict(produced_items))))
    print(sum(consume_time_sequence) / len(consume_time_sequence))


"""
代码中遇到的坑
    1. 不知道如何在market获取需要购买的商品，解决方案为通过两个步骤来做，第一步模拟个人浏览各个商品，然后再通过分布式锁来购买商品
    2. redis获取的字符串默认为b''这种类型，需要进行解码为utf8才能进行比较
"""

if __name__ == '__main__':
    test_distributed_lock(4, 3)
