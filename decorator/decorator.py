# coding: utf8

from functools import wraps


def log(func):
	def wrapper(*args, **kwargs):
		print '{} is called with args is {} and kwargs is {}'.format(func.__name__, args, kwargs)
		return func(*args, **kwargs)

	return wrapper


@log
def add(a, b, c=2):
	return a + b + c


def decorator(params):
	def outer(func):
		@wraps(func)
		def inner(*args, **kwargs):
			print 'inserted params is {}'.format(params)
			return func(*args, **kwargs)

		return inner

	return outer


@decorator('I\'m a handsome boy')
def decrease(a):
	return a - 1


def aaa(params):
	def outer(func):
		def inner(*args, **kwargs):
			print "params is {}".format(params)
			return func(*args, **kwargs)

		return inner

	return outer


@aaa("worilegoule")
def dd(a):
	return a - 1


if __name__ == '__main__':
	# print add(1, 2, c=10)
	# print decrease(10)
	# print decrease.__name__
	# print dd(10)
	pass
