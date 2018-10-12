def func(nums):
    cur = nums[0]
    mx = nums[0]
    for ele in nums[1:]:
        cur = (cur if cur > 0 else 0) + ele
        mx = cur if cur > mx else mx
    return mx


nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(func(nums))
