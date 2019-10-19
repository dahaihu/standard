import random


def func(nums, start, end):
    left, right = start + 1, end
    while left <= right:
        while left < right and nums[left] < nums[start]:
            left += 1
        while nums[right] > nums[start]:
            right -= 1
        # 等于的时候也得退出
        # exp: [5, 2, 4, 4, 3, 3]
        # 此时 left = right = 5
        # 不退出的话，left得继续减1，从而造成mid =  4, 而5没有移动到最右边最大值的位置
        if left >= right:
            break
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
    nums[start], nums[right] = nums[right], nums[start]
    return right


def quick_sort(nums, start, end):
    if start < end:
        mid = func(nums, start, end)
        quick_sort(nums, start, mid - 1)
        quick_sort(nums, mid + 1, end)


if __name__ == '__main__':
    nums = [random.randint(1, 10) for _ in range(10)]
    print('original nums is ', nums)
    random.shuffle(nums)
    quick_sort(nums, 0, len(nums) - 1)
    print('sorted nums is ', nums)
