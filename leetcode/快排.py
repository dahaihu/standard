import random


def func(nums, start, end):
    left, right = start + 1, end
    while left <= right:
        while left < right and nums[start] > nums[left]:
            left += 1
        while nums[right] > nums[start]:
            right -= 1
        # 相等的时候是在边界的时候
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
