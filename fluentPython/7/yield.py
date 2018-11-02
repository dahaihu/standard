def countdown(n):
    print("counting down from ", n)
    while n >= 0:
        newvalue = yield n
        if newvalue is not None:
            n = newvalue
        else:
            n -= 1

# 结果中为什么第二个数为什么不是3开始呢？
# 因为c.send消耗了一个yield
# 感觉需要记住的是
# send和next在一定程度上是等价的
c = countdown(5)
for n in c:
    print(n)
    if n == 5:
        print(c.send(3))
