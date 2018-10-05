class A(type):
    # 需要注意的是元类的new方法的第一个参数是什么
    def __new__(mcs, name, bases, attrs):
        pass


class Singleton(type):
    def __init__(cls, name, bases, attrs):
        cls._instance = None
        super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class B(metaclass=Singleton):
    pass


b1 = B()
b2 = B()
print(b1 is b2)
