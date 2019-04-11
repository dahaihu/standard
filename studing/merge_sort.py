def merge(nums_left, nums_right):
    res = []
    left = right = 0
    while left < len(nums_left) and right < len(nums_right):
        if nums_left[left] < nums_right[right]:
            res.append(nums_left[left])
            left += 1
        else:
            res.append(nums_right[right])
            right += 1
    if left < len(nums_left):
        res.extend(nums_left[left:])
    else:
        res.extend(nums_right[right:])
    return res

# 这个是个错误的答案，把两种过程给放在了一起
def false_merge_sort(nums, left, right):
    if left < right:
        middle = (left + right) // 2
        nums_left = false_merge_sort(nums, left, middle)
        nums_right = false_merge_sort(nums, middle + 1, right)
        return merge(nums_left, nums_right)
    return nums

def merge_sort(nums):
    if len(nums) == 1: return nums
    middle = len(nums) // 2
    nums_left = merge_sort(nums[:middle])
    nums_right = merge_sort(nums[middle:])
    return merge(nums_left, nums_right)

from random import shuffle

nums = list(range(10))
shuffle(nums)
print(nums)
nums = merge_sort(nums)
print(nums)