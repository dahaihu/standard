def say_hello(self):
    print("hello 啊")


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
        print("__init__ attrs are ", attrs)
        super().__init__(name, bases, attrs)


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


def __init__(self):
    self.message = "Hello world"


attrs = {"__init__": __init__}

Hello = A("Hello", (object,), attrs)
h = Hello()
h.say_hello()
