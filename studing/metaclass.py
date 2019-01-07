def say_hello(self):
    print("hello 啊")


def say_init(self):
    print("我日了狗了")


# 这个是flask中常用的创建父类的方法
def with_metaclass(meta, base=object):
    return meta("NewBase", (base,), {})


class A(type):
    # 需要注意的是元类的new方法的第一个参数是什么
    # 似乎只能通过new方法来修改attrs
    # 在init方法里面添加attrs是没有用的
    def __new__(mcs, name, bases, attrs):
        print("new attrs are ", attrs)
        print('name is ', name)
        attrs['say_hello'] = say_hello
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        # 在__init__方法里面，更新attrs，并没有卵用
        # 应该就是只能在__new__方法里面，修改attr
        print("__init__ attrs are ", attrs)
        attrs['init'] = say_init
        print("__init__ attrs are updated : {}".format(attrs))
        print(type(attrs))
        print(cls.__dict__)
        super().__init__(name, bases, attrs)


C = with_metaclass(A)
print('C.__name__ is {}'.format(C.__name__))


class B(C):
    pass


def test_with_metaclass():
    b = B()
    b.say_hello()
    c = C()
    c.say_hello()




class Singleton(type):
    def __init__(cls, name, bases, attrs):
        cls._instance = None
        super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        print("call is being called")
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        print("call has been called")
        return cls._instance


class B(metaclass=Singleton):
    def __init__(self):
        print("init is being called")
