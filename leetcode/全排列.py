def permulate(nums, cur, path):
    if cur == len(nums):
        path.append(nums.copy())
    else:
        for i in range(cur, len(nums)):
            nums[cur], nums[i] = nums[i], nums[cur]
            permulate(nums, cur+1, path)
            nums[cur], nums[i] = nums[i], nums[cur]

def solve(nums):
    path = []
    permulate(nums, 0, path)
    return path

print(solve([1, 2, 3]))

