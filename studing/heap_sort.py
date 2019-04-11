def adjust(nums, i, end):
    # # tmp 指向最大值
    # tmp = 2 * i + 1
    # if tmp + 1 < end and nums[tmp] < nums[tmp + 1]:
    #     tmp = tmp + 1
    # if nums[i] > nums[tmp]:
    #     nums[i], nums[tmp] = nums[tmp], nums[i]
    #     if 2 * tmp + 1 < end:
    #         adjust(nums, tmp, end)

    while 2 * i + 1< end:
        tmp = 2 * i + 1
        if tmp + 1 < end and nums[tmp + 1] > nums[tmp]:
            tmp += 1
        if nums[i] < nums[tmp]:
            nums[i], nums[tmp] = nums[tmp], nums[i]
            i = tmp
        else:
            break


def heap_sort(nums):
    for i in range((len(nums) - 1) // 2, -1, -1):
        adjust(nums, i, len(nums))
    for i in range(len(nums)-1, 0, -1):
        nums[0], nums[i] = nums[i], nums[0]
        adjust(nums, 0, i)


from random import shuffle
nums = list(range(10))
shuffle(nums)
print(nums)
heap_sort(nums)
print(nums)