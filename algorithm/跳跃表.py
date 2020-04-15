# coding: utf8

import random

"""
如何初始化
    1. 初始化节点的_forwards(包括self._head的初始化)
    2. 插入节点的时候update的初始化(update的元素也可以都初始化为None)
如何思考边界条件？
"""


class ListNode:
	def __init__(self, data=None):
		self._data = data
		# 这个_forwards到底存的是什么？
		# 存的是对应层次的下一个节点
		# _forwards的长度和插入此节点的level一致
		self._forwards = []  # 存放类似指针/引用的数组，占用空间很小


class SkipList:
	# 此节点的是不包含的
	_MAX_LEVEL = 4

	def __init__(self):
		# 实际的高度吗
		self._level_count = 1
		self._head = ListNode()
		self._head._forwards = [None] * self._MAX_LEVEL

	def find(self, value):
		'''
		查找一个元素，返回一个 ListNode 对象
		'''
		p = self._head
		for i in range(self._level_count - 1, -1, -1):
			while p._forwards[i] and p._forwards[i]._data < value:
				p = p._forwards[i]
			if p._forwards[i] and p._forwards[i]._data == value:
				return p._forwards[i]
		return None

	def find_range(self, begin_value, end_value):
		'''
		查找一个元素，返回一组有序 ListNode 对象
		'''
		p = self._head
		begin = None
		# 最外层是同一级的一直向下移动
		for i in range(self._level_count - 1, -1, -1):
			# 一直向右移动
			while p._forwards[i] and p._forwards[i]._data < begin_value:
				p = p._forwards[i]
			if p._forwards[i] and p._forwards[i]._data >= begin_value:
				begin = p._forwards[i]

		if begin is None:
			return None  # 没有找到
		else:
			result = []
			while begin and begin._data <= end_value:
				result.append(begin)
				begin = begin._forwards[0]
			return result

	def insert(self, value):
		'''
		插入一个元素到跳跃表
		插入成功则返回True
		插入失败则返回False(失败表示元素已经存在)
		'''
		# 插入的层次很有意思
		# 从这个元素的初始化层次开始遍历，因为高层中不包含此元素
		# 在_random_level中比较_MAX_LEVEL了
		level = self._random_level()
		if self._level_count < level:
			self._level_count = level
		new_node = ListNode(value)
		new_node._forwards = [None] * level
		# update 保存插入结节的左边的节点
		update = [None] * level

		p = self._head
		for i in range(level - 1, -1, -1):
			while p._forwards[i] and p._forwards[i]._data < value:
				p = p._forwards[i]
			if p._forwards[i]._data == value:
				return False
			update[i] = p
		for i in range(level):
			new_node._forwards[i] = update[i]._forwards[i]
			update[i]._forwards[i] = new_node
		return True

	def delete(self, value):
		'''
		删除一个元素，返回 True 或 False
		'''
		update = [None] * self._level_count
		p = self._head
		for i in range(self._level_count - 1, -1, -1):
			while p._forwards[i] and p._forwards[i]._data < value:
				p = p._forwards[i]
			update[i] = p

		if p._forwards[0] and p._forwards[0]._data == value:
			# 如果存在，是不是可以根据这个节点的高度，来进行更新
			for i in range(self._level_count - 1, -1, -1):
				if update[i]._forwards[i] and update[i]._forwards[i]._data == value:
					# Similar to prev.next = prev.next.next
					update[i]._forwards[i] = update[i]._forwards[i]._forwards[i]
			return True
		else:
			return False

	def _random_level(self, p=0.5):
		'''
		返回随机层数
		'''
		level = 1
		while random.random() < p and level < self._MAX_LEVEL:
			level += 1
		return level

	def pprint(self):
		'''
		打印跳表
		'''
		i = self._level_count - 1
		while i >= 0:
			p = self._head
			skiplist_str = 'head {}: '.format(i)
			while p:
				if p._data:
					skiplist_str += '->' + str(p._data)
				p = p._forwards[i]
			print(skiplist_str)
			i -= 1


if __name__ == '__main__':
	l = SkipList()
	for i in range(0, 40, 3):
		l.insert(i)
	l.pprint()
	print '你好啊'
	node = l.find(3)
	print node._data
	l.delete(33)
	l.pprint()
