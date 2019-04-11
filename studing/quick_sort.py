def partition(nums, left, right):
    original, left = left, left + 1
    while True:
        while left < right and nums[left] < nums[original]:
            left += 1
        # 这个地方不用害怕出界的原因是最后一个right最坏的结果是移动到original的位置
        # 因为此时 nums[right] = nums[original]
        while nums[right] > nums[original]:
            right -= 1
        if left >= right: break
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
    nums[original], nums[right] = nums[right], nums[original]
    return right

def quick_sort(nums, left, right):
    if left < right:
        p = partition(nums, left, right)
        quick_sort(nums, left, p - 1)
        quick_sort(nums, p + 1, right)

from random import shuffle

nums = list(range(10))
shuffle(nums)
print(nums)
quick_sort(nums, 0, len(nums) - 1)
print(nums)