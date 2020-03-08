# coding: utf8

import time


class A(object):
	def __init__(self, val):
		self.val = val

	def __get__(self, instance, owner):
		print 'instance is {}, owner is {}'.format(instance, owner)
		return self.val

	def __set__(self, instance, value):
		self.val = value


class B(object):
	a = A(10)


class LazyProperty(object):
	def __init__(self, func):
		self.func = func

	def __get__(self, instance, owner):
		if instance is None:
			return self

		value = self.func(instance)
		setattr(instance, self.func.__name__, value)
		return value


class C(object):
	# @LazyProperty
	def func(self):
		time.sleep(2)
		return 2

	func = LazyProperty(func)


c = C()

print c.func

print c.func
