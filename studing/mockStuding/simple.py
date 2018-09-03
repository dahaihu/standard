
class Foo1:
    _value1 = 100
    def fun1(self):
        pass
    def fun2(self, arg):
        pass



class Foo2:
    _value2 = 200
    def fun3(self):
        pass
    def fun4(self, arg):
        pass

class Person:
    def __init__(self):
        self.__age = 10

    def get_fullname(self, first_name, last_name):
        return first_name + ' ' + last_name

    def get_age(self):
        return self.__age

    @staticmethod
    def get_class_name():
        return Person.__name__

from unittest import TestCase
from unittest.mock import Mock, patch
import unittest
# from pytest import patch

class PersonTest(TestCase):
    def test_should_get_age(self):
        p = Person()

        # 不mock时，get_age应该返回10
        self.assertEqual(p.get_age(), 10)

        # mock掉get_age方法，让它返回20
        p.get_age = Mock(return_value=20)
        self.assertEqual(p.get_age(), 20)

    def test_should_get_fullname(self):
        p = Person()
        # mock掉get_fullname，让它返回'James Harden'
        p.get_fullname = Mock(return_value='James Harden')
        self.assertEqual(p.get_fullname(), 'James Harden')


    # 根据参数不同返回不同的值
    def test_should_get_full_name(self):
        p = Person()
        values = {('James', 'Harden'): 'James Harden', ('Tracy', 'Grady'): 'Tracy Grady'}
        p.get_fullname = Mock(side_effect=lambda x, y: values[(x, y)])
        self.assertEqual(p.get_fullname('James', 'Harden'), 'James Harden')
        self.assertEqual(p.get_fullname('Tracy', 'Grady'), 'Tracy Grady')

    def test_side_effect(self):
        # 结果是可以打印的
        p = Person()
        p.get__fullname = Mock(side_effect=['hushichang', 'limanman'])
        p.get_lastname = Mock(side_effect=['shichang', 'manman'])
        # print(p.get__fullname)
        tmp = p.get_lastname() in p.get__fullname()
        print(tmp)
        assert(tmp)
        tmp = p.get_lastname() in p.get__fullname()
        print(tmp)
        assert(tmp)
        # assert(p.get_lastname() in p.get__fullname())
        # assert(p.get_lastname() in p.get__fullname())

    # @patch("studing.mockStuding.simple.Person.get_class_name")
    # def test_should_get_class_name(self, mock_get_class_name):
    #     mock_get_class_name.return_value = 'Guy'
    #     self.assertEqual(mock_get_class_name(), 'Guy')

if __name__ == '__main__':
    unittest.main()
    assert 0
