import random


def adjust_recursion(nums, i, length):
    if not (2 * i + 1 < length):
        return
    tmp = 2 * i + 1
    if tmp + 1 < length and nums[tmp + 1] > nums[tmp]:
        tmp += 1
    if nums[i] > nums[tmp]:
        return
    nums[i], nums[tmp] = nums[tmp], nums[i]
    adjust_recursion(nums, tmp, length)


def adjust(nums, i, length):
    while 2 * i + 1 < length:
        tmp = 2 * i + 1
        if tmp + 1 < length and nums[tmp + 1] > nums[tmp]:
            tmp += 1
        if nums[i] > nums[tmp]:
            return
        nums[i], nums[tmp] = nums[tmp], nums[i]
        i = tmp


def heap_sort(nums):
    for i in range(len(nums) // 2 - 1, -1, -1):
        adjust(nums, i, len(nums))
    for i in range(len(nums) - 1, -1, -1):
        nums[0], nums[i] = nums[i], nums[0]
        adjust(nums, 0, i)


if __name__ == '__main__':
    nums = [random.randint(1, 10) for _ in range(10)]
    print('original nums is ', nums)
    heap_sort(nums)
    print('sorted nums is ', nums)
