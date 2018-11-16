def func(nums):
    n = len(nums) + 1
    for ele in nums:
        nums[ele % n - 1] += n
    res = []
    for ind, ele in enumerate(nums):
        if ele // n == 2:
            res.append(ind + 1)
    return res


nums = [4, 3, 2, 7, 8, 2, 3, 1]
print(func(nums))
