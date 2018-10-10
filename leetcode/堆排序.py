import random


def adjust(nums, i, length):
    while 2 * i + 1 < length:
        tmp = 2 * i + 1
        if tmp + 1 < length and nums[tmp + 1] > nums[tmp]:
            tmp += 1
        if nums[i] > nums[tmp]:
            break
        nums[i], nums[tmp] = nums[tmp], nums[i]
        i = tmp


def stackSort(nums):
    for i in range(len(nums) // 2 - 1, -1, -1):
        adjust(nums, i, len(nums))
    for i in range(len(nums) - 1, 0, -1):
        nums[0], nums[i] = nums[i], nums[0]
        adjust(nums, 0, i)
    print(nums)


nums = list(range(20))
random.shuffle(nums)
stackSort(nums)
