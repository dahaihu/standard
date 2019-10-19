import random


def func(nums, start, end):
    left, right = start + 1, end
    while left <= right:
        while left < right and nums[left] < nums[start]:
            left += 1
        while nums[right] > nums[start]:
            right -= 1
        if left >= right:
            break
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
    nums[start], nums[right] = nums[right], nums[start]
    return right


def quickSort(nums, start, end):
    if start < end:
        mid = func(nums, start, end)
        quickSort(nums, start, mid - 1)
        quickSort(nums, mid + 1, end)


if __name__ == '__main__':
    nums = [random.randint(1, 10) for _ in range(10)]
    print('original nums is ', nums)
    random.shuffle(nums)
    quickSort(nums, 0, len(nums) - 1)
    print('sorted nums is ', nums)
