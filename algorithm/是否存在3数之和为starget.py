nums, target = input().strip().split(',')
nums = [int(ele) for ele in nums.split(' ')]
target = int(target)
nums.sort()
def func(nums, target, k):
    if k == 2:
        left, right = 0, len(nums) - 1
        while left < right:
            if nums[left] + nums[right] == target:
                return True
            elif nums[left] + nums[right] < target:
                left += 1
            else:
                right -= 1
        return False
    for i in range(len(nums) - k + 1):
        tmp = func(nums[i + 1:], target - nums[i], k - 1)
        if not tmp:
            continue
        else:
            return True
    return False
print(func(nums, target, 3))

