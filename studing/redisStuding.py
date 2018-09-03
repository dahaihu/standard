from redis import Redis

conn = Redis()
res = conn.hgetall('test')
print(res)
print(res.get(b"b"))
print(type(res.get(b"b")))
conn.hset('test', 'c', 10)
print(conn.hget('test', 'c'))
print(type(conn.hget('test', 'c')))
print(int(conn.hget('test', 'c')))
print(type(int(conn.hget('test', 'c'))))
