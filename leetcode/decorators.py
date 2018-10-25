import time


class LazyProperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        print("instance is {}".format(instance))
        print("owner is {}".format(owner))
        value = self.func(instance)
        setattr(instance, self.func.__name__, value)
        return value


class A:
    @LazyProperty
    def func(self):
        time.sleep(1)
        return 10


a = A()
print(a.func)
print(a.func)
