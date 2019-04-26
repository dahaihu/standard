import uuid
import time
import redis

def acquire_lock(conn, lockname, acquier_timeout=10):
    identifier = str(uuid.uuid4())
    end = time.time() + acquier_timeout
    while time.time() < end:
        if conn.setnx('lock:' + lockname, identifier):
            return identifier
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
        if price is None or price > funds:
            return None
        pipe.hincrby(seller, 'funds', int(price))
        pipe.hincrby(buyer, 'funds', -int(price))
        pipe.sadd(inventory, itemid)
        pipe.zrem("market:", item)
        pipe.execute()
        return True
    finally:
        release_lock(conn, "market:", locked)


def release_lock(conn, lockname, identifier):
    pipe = conn.pipeline(True)
    lockname = 'lock:' + lockname
    while True:
        try:
            pipe.watch(lockname)
            if conn.get(lockname) == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True
            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            pass
    return False