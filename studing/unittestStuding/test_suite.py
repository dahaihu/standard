import unittest
from .test_mathfunc import TestMathFunc

def func():
    pass


if __name__ == '__main__':
    suite = unittest.TestSuite()
    # tests = [TestMathFunc('test_add'), TestMathFunc('test_minus'), TestMathFunc('test_multi'), TestMathFunc("test_divide")]
    # suite.addTests(tests)
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathFunc))
    runner = unittest.TextTestRunner()
    runner.run(suite)