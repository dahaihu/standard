# coding: utf8


def binary_search(array, target):
	left, right = 0, len(array) - 1
	while left <= right:
		mid = (left + right) // 2
		if array[mid] > target:
			right = mid - 1
		elif array[mid] < target:
			left = mid + 1
		else:
			return mid
	# 下边界
	return left


if __name__ == "__main__":
	print binary_search([i for i in range(10)], 10)
