class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.order = []
        self.cache = dict()
        self.remain = capacity

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            self.cache[key] = value
            return
        if self.remain > 0:
            self.order.append(key)
            self.cache[key] = value
            self.remain -= 1
        else:
            del self.cache[self.order.pop(0)]
            self.order.append(key)
            self.cache[key] = value

