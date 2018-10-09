import random

# 含义，含义，含义
def func(nums, start, end):
    left, right = start + 1, end
    while True:
        while left < right and nums[left] < nums[start]:
            left += 1
        while nums[right] > nums[start]:
            right -= 1
        if left >= right:
            break
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
    nums[right], nums[start] = nums[start], nums[right]
    return right


def quickSort(nums, left, right):
    if left < right:
        mid = func(nums, left, right)
        print('left is {}, right is {}, mid is {}, nums is {}'.format(left, right, mid, nums))
        quickSort(nums, left, mid - 1)
        quickSort(nums, mid + 1, right)


# nums = list(range(10))
# random.shuffle(nums)
nums = [5, 1, 2, 3]
quickSort(nums, 0, len(nums) - 1)
print(nums)
