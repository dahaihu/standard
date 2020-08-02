# coding: utf8
import uuid
import time
import random
import redis
import math

# 有序结合，元素为商品，分数为价格
MARKET = 'market'
# 哈希，包括用户名字，以及用户存款
USER = 'users:{user_id}'
# 集合，包括用户所属的商品
INVENTORY = 'inventory:{user_id}'
# 是市场中有序集合中的元素
ITEM = '{item_id}:{user_id}'

CONSUMER_BASE = 10000
CONSUMERS = 5
PRODUCERS = 5
ITEMS = 20000

consume_list = []


def acquire_lock(conn, lock_name, timeout=10):
	identifier = str(uuid.uuid4())
	end = time.time() + timeout
	while time.time() < end:
		if conn.setnx('lock:{}'.format(lock_name), identifier):
			# print 'lock is ', conn.get('lock:{}'.format(lock_name))
			return identifier
		time.sleep(0.001)
	return False


def acquire_lock_with_timeout(conn, lock_name, acquire_timeout=12, lock_timeout=10):
	identifier = str(uuid.uuid4())
	lock_name = 'lock:{}'.format(lock_name)
	lock_timeout = int(math.ceil(lock_timeout))
	end_time = time.time() + acquire_timeout
	while time.time() < end_time:
		print '尝试'
		print conn.ttl(lock_name)
		if conn.setnx(lock_name, identifier):
			conn.expire(lock_name, lock_timeout)
			return True
		# 下面的代码是有问题的
		# elif not conn.ttl(lock_name):
		# 	print 'aa 续上了'
		# # 	# 这咋还续上了呢？
		# 	conn.expire(lock_name, lock_timeout)
		time.sleep(0.001)


def release_lock(conn, lock_item, lock):
	lock_name = 'lock:{}'.format(lock_item)
	pipe = conn.pipeline()
	while True:
		try:
			pipe.watch(lock_name)
			# 不相等的时候，怎么办呢？？？
			if pipe.get(lock_name) == lock:
				pipe.multi()
				pipe.delete(lock_name)
				pipe.execute()
				return True
			print '解锁失败？？？？'
			pipe.unwatch()
			# 眼睛不要 可以捐了，傻屌
			break
		except redis.exceptions.WatchError:
			pass
	return False


def purchase_item_with_lock(conn, buyer_id, item):
	start_time = time.time()
	# 感觉消费不好做
	# 因为有两个步骤
	# 除了购买的操作外，还有一个挑选
	buyer = 'users:{}'.format(buyer_id)
	inventory = 'inventory:{}'.format(buyer_id)
	lock = acquire_lock(conn, MARKET)
	if not lock:
		print 'get lock failed'
		return False
	item_id, seller_id = item.split(':')
	seller = 'users:{}'.format(seller_id)
	item = "{}:{}".format(item_id, seller_id)
	pipe = conn.pipeline(True)
	try:
		pipe.zscore('market', item)
		pipe.hget(buyer, 'funds')
		values = pipe.execute()
		# print 'buyer is {}'.format(buyer)
		# print 'values is {}'.format(values)
		price, funds = values
		if price is None or price > int(funds):
			print 'price not supply'
			return None
		pipe.hincrby(seller, 'funds', int(price))
		pipe.hincrby(buyer, 'funds', -int(price))
		pipe.zrem('market', item)
		pipe.sadd(inventory, item)
		pipe.execute()
	# print 'buy success'
	finally:
		release_lock(conn, MARKET, lock)
	consume_list.append(time.time() - start_time)


def choose_item(conn):
	lock = acquire_lock(conn, MARKET)
	if not lock:
		return False
	item = None
	try:
		length = conn.zcard(MARKET)
		idx = random.randint(0, length - 1)
		item = conn.zrange(MARKET, idx, idx)
	finally:
		release_lock(conn, MARKET, lock)
	return item


def list_item(conn, item_id, seller_id, price, timeout=5):
	inventory = INVENTORY.format(user_id=seller_id)
	item = ITEM.format(user_id=seller_id, item_id=item_id)
	lock = acquire_lock(conn, MARKET)
	if not lock:
		return False
	end_time = time.time() + timeout
	pipeline = conn.pipeline()
	while time.time() < end_time:
		try:
			pipeline.watch(inventory)
			if not pipeline.sismember(inventory, item):
				pipeline.unwatch()
				return False
			pipeline.multi()
			pipeline.zadd(MARKET, item, price)
			pipeline.srem(inventory, item_id)
			pipeline.execute()
			return True
		except redis.WatchError:
			continue
	return False


def list_item_with_lock(conn, item_id, seller_id, price, timeout=5):
	inventory = INVENTORY.format(user_id=seller_id)
	item = ITEM.format(user_id=seller_id, item_id=item_id)
	lock = acquire_lock(conn, MARKET, timeout=timeout)
	print '{}, {}, {}'.format(inventory, item, lock)
	if not lock:
		return False
	try:
		if not conn.sismember(inventory, item_id):
			print '{} not member'.format(item_id)
			return False
		print '{} is member'.format(item_id)
		pipeline = conn.pipeline()
		pipeline.multi()
		pipeline.zadd(MARKET, {item: price})
		pipeline.srem(inventory, item_id)
		pipeline.execute()
		return True
	except Exception as e:
		print 'exception is ', e
	finally:
		release_lock(conn, MARKET, lock)


def buy_item(conn, buyer_id):
	item = choose_item(conn)
	# print 'choose item is {}'.format(item)
	if not item:
		print '{} 选择商品失败'.format(buyer_id)
		return False
	purchase_item_with_lock(conn, buyer_id, item[0])


def check_exist(conn):
	lock = acquire_lock(conn, MARKET)
	if not lock:
		return False
	length = conn.zcard(MARKET)
	release_lock(conn, MARKET, lock)
	# print 'mark length is {}'.format(length)
	return length


if __name__ == '__main__':
	import redis
	import time

	redis = redis.Redis()
	redis.set('lock:market', 10)
	redis.expire('lock:market', 1)
	acquire_lock_with_timeout(redis, 'market')

	# end_time = time.time() + 1.5
	# while time.time() < end_time:
	# 	res = redis.ttl('lock:market')
	# 	print 'res is {}, not res is {}, key is {}'.format(res, not res, redis.get('lock:market'))
	# 	time.sleep(0.001)
