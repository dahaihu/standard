import unittest
from .mathfunc import *


class TestMathFunc(unittest.TestCase):
    # def setUp(self):
    #     print("before a test case")
    #
    # def tearDown(self):
    #     print("after a test case")

    # @staticmethod
    # def setUpClass(cls):
    #     print("before a test suite")
    #
    #
    # @staticmethod
    # def tearDownClass(cls):
    #     print("after a test suite")

    """Test mathfuc.py"""

    def test_add(self):
        """Test method add(a, b)"""
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """Test method multi(a, b)"""
        self.assertEqual(6, multi(2, 3))

    def test_divide(self):
        """Test method divide(a, b)"""
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2, divide(5, 2))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathFunc))
    with open("/home/result.txt", 'a') as file:
        runner = unittest.TextTestRunner(stream=file, verbosity=2)
        runner.run(suite)

    with open("/home/file.txt", 'a') as file:
        file.write('a\n')
        file.write('a\n')
        file.write('a\n')
        file.write('a\n')
