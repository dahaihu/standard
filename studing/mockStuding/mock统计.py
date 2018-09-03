from unittest.mock import Mock

class Foo:
    def fun1(self, argValue):
        print('argValue is {}'.format(argValue))


mockFoo = Mock(spec=Foo)
print(mockFoo)
print(mockFoo.called)
mockFoo()
print(mockFoo.called)
print(mockFoo.call_count)
mockFoo.fun1()

mockFoo(1, 2)
mockFoo(2, 3)
print(mockFoo.call_count)
print(mockFoo.call_args)
print(mockFoo.call_args_list)
print(mockFoo.method_calls)
print(mockFoo.mock_calls)